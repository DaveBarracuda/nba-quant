"""Orquestador de pizarra: features pre-partido -> clases 2-7 (spec 3) + proyección exacta de
margen con la cadena de Markov a 100.000 iteraciones (spec 4) + backtest de calibración
(modo `base` = sólo ratings; modo `context` = pila completa de contexto point-in-time).
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd

from nba_quant.config import EngineConfig
from nba_quant.logging_utils import get_logger
from nba_quant.models.markov import (LEAGUE_SEGMENT_PROBS, STATES, PossessionMarkovEngine, SimulationResult,
                                     TeamProfile, build_matchup)
from nba_quant.simulation.bias import BiasCalibrator, BiasState
from nba_quant.simulation.blend import MarketBlender, shift_simulation
from nba_quant.simulation.context import (DeepHistoricalPatternEngine, DynamicModifierEngine, Scenario,
                                          StatisticalCleansingLayer)
from nba_quant.simulation.evaluation import (game_seed, market_probs, mixture_summary, score, score_market,
                                             single_summary)
from nba_quant.simulation.financial import FinancialMarketAnalyzer, MarketQuote
from nba_quant.simulation.inefficiencies import MarketInefficienciesEngine
from nba_quant.simulation.monte_carlo import BlockResult, MonteCarloOutput, MonteCarloVectorizedCore

log = get_logger("slate")

MK_KEYS = list(STATES) + ["OREB"]
FATIGUE_WINDOW_DAYS = 7
PROP_LOOKBACK_GAMES = 10
PROP_TOP_PLAYERS = 6
STAR_LOOKBACK_GAMES = 15
CROSS_RIM_WEIGHT = 0.5
BACKTEST_SIMS = 10_000
CONTEXT_BACKTEST_SIMS = 2_000  # por celda de la rejilla 3×3 (18.000 sims por partido)
MODEL_VERSION = "nba_quant-0.1"


@dataclass
class GameProjection:
    row: dict
    tear_sheet: str
    props: pd.DataFrame
    edges: list = field(default_factory=list)  # EdgeResult por mercado (ML, spread, total)


@dataclass(frozen=True)
class ContextState:
    """Capas de contexto construidas sólo con información anterior a una fecha (point-in-time)."""

    patterns: DeepHistoricalPatternEngine
    signals: pd.DataFrame
    ineff: MarketInefficienciesEngine
    ref_profiles: pd.DataFrame


@dataclass(frozen=True)
class TeamContext:
    """Insumos de escenario de un equipo: base L5, patrones históricos SIN encoger (para poder
    re-encogerlos con otras k), resto de ajustes en pts/100 y factor estrella."""

    team: str
    base_ortg: float
    hist_parts: dict[str, tuple[float, int]]
    other_adj: dict[str, float]
    star_factor: float


@dataclass(frozen=True)
class GameContext:
    game_id: str
    date: pd.Timestamp
    season: int
    home: TeamProfile
    away: TeamProfile
    league: dict[str, float]
    mu: float
    phi: float
    cross: dict
    lam0: float
    spread_home: float | None
    odds: pd.Series | None
    teams: tuple[TeamContext, TeamContext]  # (local, visitante)
    hca: float = 2.4  # ventaja de campo point-in-time (pts/100) del calibrador de sesgos


ODDS_TOTAL_RANGE = (180.0, 270.0)
ODDS_MAX_ABS_SPREAD = 30.0
ODDS_FAV_CHECK_MIN_SPREAD = 1.5


def sanitize_odds(odds: pd.DataFrame) -> pd.DataFrame:
    """Anula (NaN) cuotas incoherentes en vez de usarlas: totales fuera de rango, spreads
    absurdos y moneylines cuyo favorito contradice al del spread (líneas corruptas de la fuente)."""
    o = odds.copy()
    bad_total = o["total_close"].notna() & ~o["total_close"].between(*ODDS_TOTAL_RANGE)
    o.loc[bad_total, ["total_open", "total_close", "over_odds_close", "under_odds_close"]] = np.nan
    bad_spread = o["spread_close"].notna() & (o["spread_close"].abs() > ODDS_MAX_ABS_SPREAD)
    o.loc[bad_spread, ["spread_open", "spread_close", "spread_home_odds_close", "spread_away_odds_close"]] = np.nan
    fav_ml = o["home_ml_close"] < o["away_ml_close"]
    contradict = (fav_ml != (o["spread_close"] < 0)) & (o["spread_close"].abs() >= ODDS_FAV_CHECK_MIN_SPREAD)
    o.loc[contradict, ["home_ml_open", "home_ml_close", "away_ml_open", "away_ml_close"]] = np.nan
    n = int(bad_total.sum() + bad_spread.sum() + contradict.sum())
    if n:
        log.warning("Cuotas saneadas: %d mercados incoherentes anulados", n)
    return o


def _finite(v: object) -> bool:
    try:
        return v is not None and bool(np.isfinite(float(v)))
    except (TypeError, ValueError):
        return False


class SlateSimulator:
    def __init__(self, cfg: EngineConfig, features: pd.DataFrame, games: pd.DataFrame,
                 odds: pd.DataFrame | None = None, officials: pd.DataFrame | None = None,
                 game_fouls: pd.DataFrame | None = None, player_box: pd.DataFrame | None = None) -> None:
        self.cfg = cfg
        self.f = features.reset_index() if "team" not in features.columns else features.copy()
        self.f["game_date"] = pd.to_datetime(self.f["game_date"])
        self.games = games.assign(game_date=pd.to_datetime(games["game_date"]))
        self.odds = odds if odds is not None else pd.DataFrame()
        self.officials = officials if officials is not None else pd.DataFrame()
        box = player_box if player_box is not None else pd.DataFrame()
        # Box sólo de temporada regular/playoffs: la pretemporada (minutos experimentales) no
        # debe alimentar fatiga, estrella ni props.
        real = self.games[self.games["season_type"].isin([2, 3])] if "season_type" in self.games.columns else self.games
        self.box = (box.drop(columns=["season"], errors="ignore")
                    .merge(real[["game_id", "game_date", "home_team", "away_team"]], on="game_id")
                    if not box.empty else box)
        self.game_fouls = game_fouls
        self.cleansing = StatisticalCleansingLayer(cfg.cleansing)
        self.dynamic = DynamicModifierEngine(cfg.sim)
        self.analyzer = FinancialMarketAnalyzer(cfg.sim, cfg.market)
        # Calibrador de sesgos point-in-time (ventaja de campo y nivel de anotación).
        self.bias_correction = True
        self.blender: MarketBlender | None = None  # se activa con fit_blender()
        self.bias = BiasCalibrator.from_features(self.f, self.games, cfg.decay.home_court_pts_per100)
        self.history = self._history()
        self.game_rates = self._game_rates()
        # Estado "a fecha de hoy" (toda la historia): el que usan las proyecciones de pizarra.
        self.state = self.context_state()
        self.patterns, self.signals = self.state.patterns, self.state.signals
        self.ineff, self.ref_profiles = self.state.ineff, self.state.ref_profiles

    # ------------------------------------------------------------------ preparación
    def _first_odds(self) -> pd.DataFrame:
        if self.odds.empty:
            return pd.DataFrame(columns=["game_id"])
        return sanitize_odds(self.odds.sort_values("provider").groupby("game_id").first().reset_index())

    def _history(self) -> pd.DataFrame:
        """Una fila por equipo-partido con margen real, residuo vs modelo y residuo ATS."""
        cols = [c for c in ("game_id", "home_team", "venue", "n_periods") if c in self.games.columns]
        f = self.f.merge(self.games[cols], on="game_id", how="left")
        opp = f[["game_id", "team", "strength_off", "strength_def"]].rename(
            columns={"team": "opponent", "strength_off": "opp_off", "strength_def": "opp_def"})
        f = f.merge(opp, on=["game_id", "opponent"], how="left")
        hca = np.where(f["is_home"] == 1, 1, -1) * self.cfg.decay.home_court_pts_per100
        exp_margin = ((f["strength_off"] + f["opp_def"]) - (f["opp_off"] + f["strength_def"]) + hca) * f["pace"] / 100
        f["margin"] = f["target_margin"]
        f["residual"] = f["margin"] - exp_margin
        f["went_ot"] = (f.get("n_periods", pd.Series(4, index=f.index)).fillna(4) > 4).astype(int)
        odds = self._first_odds()
        if not odds.empty:
            f = f.merge(odds[["game_id", "spread_open", "spread_close"]], on="game_id", how="left")
            sign = np.where(f["is_home"] == 1, 1.0, -1.0)
            f["spread_open"], f["spread_close"] = f["spread_open"] * sign, f["spread_close"] * sign
            f["ats_residual"] = f["margin"] + f["spread_close"]
            f["is_favorite"] = f["spread_close"] < 0
        else:
            f["ats_residual"] = f["residual"]
        return f

    def _game_rates(self) -> pd.DataFrame:
        """Ratings reales por partido (para la base L5 de la clase 2)."""
        h = self.history
        gr = pd.DataFrame({
            "season": h["season"], "team": h["team"], "game_date": h["game_date"], "net_margin": h["margin"],
            "ortg": 100 * h["target_pts"] / h["target_poss"], "drtg": 100 * h["target_opp_pts"] / h["target_poss"],
            "pace": h["target_poss"], "three_luck_off": h["three_luck_off"], "three_luck_def": h["three_luck_def"],
        })
        return gr.dropna(subset=["ortg"])

    def _strength_rank(self, as_of: pd.Timestamp | None = None) -> pd.Series:
        f = self.f if as_of is None else self.f[self.f["game_date"] <= as_of]  # features pre-partido
        last = f.sort_values("game_date").groupby("team").tail(1).set_index("team")
        return last["strength_net"].rank(ascending=False)

    def context_state(self, before: pd.Timestamp | None = None,
                      shrink_k: dict[str, float] | None = None) -> ContextState:
        """Clases 3 y 4 + perfiles arbitrales usando sólo partidos con fecha < `before`
        (None = toda la historia). El calendario futuro sí se conoce (señal de lookahead)."""
        played = self.history["margin"].notna()
        past = played if before is None else played & (self.history["game_date"] < before)
        patterns = DeepHistoricalPatternEngine(self.history[past], shrink_k)
        ineff = MarketInefficienciesEngine()
        signals = ineff.build_signals(self.history, self._strength_rank(before))
        sig_past = signals["margin"].notna()
        if before is not None:
            sig_past &= signals["game_date"] < before
        ineff.calibrate(signals[sig_past])
        refs = pd.DataFrame()
        if self.game_fouls is not None and not self.officials.empty:
            officials = self.officials
            if before is not None:
                officials = officials[officials["game_id"].isin(
                    self.games.loc[self.games["game_date"] < before, "game_id"])]
            if not officials.empty:
                refs = ineff.referee_profiles(officials, self.game_fouls)
        return ContextState(patterns, signals, ineff, refs)

    def _league_probs(self, date: pd.Timestamp) -> dict[str, float]:
        cur = self.f[self.f["game_date"] <= date].sort_values("game_date").groupby("team").tail(1)
        return {k: float(cur[f"mk_{k}"].mean()) if f"mk_{k}" in cur.columns else LEAGUE_SEGMENT_PROBS[k]
                for k in MK_KEYS}

    def team_profile(self, r: pd.Series) -> TeamProfile:
        mu = float(r.get("kf_league_mu", self.cfg.kalman.league_ortg_prior))
        return TeamProfile(
            team=r["team"], pace=float(r["pace"]), transition_freq=float(r["trans_freq"]),
            ft_pct=float(np.clip(r["ft_pct"], 0.5, 0.95)),
            off_probs={k: float(r[f"mk_{k}"]) for k in MK_KEYS},
            def_probs={k: float(r[f"mk_def_{k}"]) for k in MK_KEYS},
            off_rating=mu + float(r["strength_off"]), def_rating=mu + float(r["strength_def"]),
        )

    # ------------------------------------------------------------------ dinámicos
    def _box_before(self, team: str, date: pd.Timestamp) -> pd.DataFrame:
        if self.box.empty:
            return self.box
        return self.box[(self.box["team"] == team) & (self.box["game_date"] < date)]

    def _star_factor(self, team: str, opponent: str, date: pd.Timestamp) -> float:
        b = self._box_before(team, date)
        if b.empty:
            return 1.0
        recent_ids = b.sort_values("game_date")["game_id"].drop_duplicates().tail(STAR_LOOKBACK_GAMES)
        recent = b[b["game_id"].isin(recent_ids)]
        star = recent.groupby("player_id")["pts"].mean().idxmax()
        sb = self.box[(self.box["player_id"] == star) & (self.box["game_date"] < date)]
        vs_opp = sb[(sb["home_team"] == opponent) | (sb["away_team"] == opponent)]["pts"]
        team_pts = recent.groupby("game_id")["pts"].sum().mean()
        share = float(recent[recent["player_id"] == star]["pts"].mean() / team_pts) if team_pts else 0.0
        return self.dynamic.star_matchup_factor(vs_opp, float(sb["pts"].mean()), float(sb["pts"].std() or 0.0), share)

    def _props_players(self, team: str, date: pd.Timestamp) -> pd.DataFrame:
        b = self._box_before(team, date)
        if b.empty:
            return pd.DataFrame()
        last_ids = b.sort_values("game_date")["game_id"].drop_duplicates().tail(PROP_LOOKBACK_GAMES)
        b = b[b["game_id"].isin(last_ids)]
        agg = b.groupby(["player_id", "player_name"]).agg(pts=("pts", "sum"), min_mean=("minutes", "mean"),
                                                         min_sd=("minutes", "std")).reset_index()
        agg["pts_share"] = agg["pts"] / max(float(b["pts"].sum()), 1.0)
        return agg.nlargest(PROP_TOP_PLAYERS, "min_mean")

    def _team_context(self, r: pd.Series, opp: str, venue: str | None, lam: float, is_favorite: bool,
                      state: ContextState, base_ortg: float) -> TeamContext:
        """Clases 2-5 de un equipo: base L5, patrones históricos (sin encoger), ineficiencias,
        rachas, fatiga y factor estrella."""
        parts = state.patterns.raw_parts(r["team"], opp, venue, int(r["is_b2b"]), int(r["is_3in4"]),
                                         float(r["rest_days"]), is_favorite)
        return TeamContext(r["team"], self._base_rating(r, base_ortg), parts,
                           self._other_adjustments(r, lam, state), self._star_factor(r["team"], opp, r["game_date"]))

    def _other_adjustments(self, r: pd.Series, lam: float, state: ContextState) -> dict[str, float]:
        """Clases 4 y 5: ineficiencias y dinámicos, en pts/100."""
        adj: dict[str, float] = {}
        sig = state.signals[(state.signals["game_id"] == r["game_id"]) & (state.signals["team"] == r["team"])]
        if not sig.empty:
            for name, pts in state.ineff.effect_points(sig.iloc[0]).items():
                adj[f"ineff_{name}"] = pts * 100.0 / lam
        recent = self.history[(self.history["team"] == r["team"]) & (self.history["game_date"] < r["game_date"])
                              & (self.history["season"] == r["season"])]
        adj["streak_reversion"] = self.dynamic.streak_reversion(recent["ats_residual"].dropna()) * 100.0 / lam
        window = self._box_before(r["team"], r["game_date"])
        if not window.empty:
            window = window[window["game_date"] >= r["game_date"] - pd.Timedelta(days=FATIGUE_WINDOW_DAYS)]
        adj["fatigue"] = self.dynamic.fatigue(window)
        return adj

    def _base_rating(self, r: pd.Series, base: float) -> float:
        """Clase 2: mezcla del rating latente con la línea base L5 limpia de sesgos."""
        l5 = self.cleansing.l5_baseline(self.game_rates, r["team"], r["game_date"], int(r["season"]))
        if not l5:
            return base
        w = self.cfg.cleansing.l5_blend
        return (1 - w) * base + w * l5["l5_ortg"]

    @staticmethod
    def _quotes(odds: pd.Series | None, home: str, away: str) -> list[MarketQuote]:
        if odds is None:
            return []
        q = []
        if _finite(odds.get("home_ml_close")) and _finite(odds.get("away_ml_close")):
            q += [MarketQuote("moneyline", home, odds["home_ml_close"], odds["away_ml_close"]),
                  MarketQuote("moneyline", away, odds["away_ml_close"], odds["home_ml_close"])]
        if all(_finite(odds.get(k)) for k in ("spread_close", "spread_home_odds_close", "spread_away_odds_close")):
            s = float(odds["spread_close"])
            q += [MarketQuote("spread", f"{home} {s:+.1f}", odds["spread_home_odds_close"], odds["spread_away_odds_close"], s),
                  MarketQuote("spread", f"{away} {-s:+.1f}", odds["spread_away_odds_close"], odds["spread_home_odds_close"], -s)]
        if all(_finite(odds.get(k)) for k in ("total_close", "over_odds_close", "under_odds_close")):
            t = float(odds["total_close"])
            q += [MarketQuote("total", f"Over {t}", odds["over_odds_close"], odds["under_odds_close"], t),
                  MarketQuote("total", f"Under {t}", odds["under_odds_close"], odds["over_odds_close"], t)]
        return q

    def _referee_context(self, game_id: str, crew: list[str] | None, rh: pd.Series, ra: pd.Series,
                         state: ContextState) -> dict:
        neutral = {"phi_context": 1.0, "ft_mod_home": 1.0, "ft_mod_away": 1.0}
        if state.ref_profiles.empty:
            return neutral
        if crew is None:
            crew = self.officials.loc[self.officials["game_id"] == game_id, "official"].tolist()
        past = self.f.loc[self.f["game_date"] <= rh["game_date"], "ftr"]  # valores pre-partido: sin futuro
        mean, sd = float(past.mean()), float(past.std() or 1.0)
        return state.ineff.crew_context(crew, state.ref_profiles, ((rh["ftr"] - mean) / sd, (ra["ftr"] - mean) / sd))

    # ------------------------------------------------------------------ partido
    def bias_state(self, date: pd.Timestamp) -> BiasState:
        """Sesgos estimados con partidos anteriores a `date` (o neutros si la corrección está apagada)."""
        if not self.bias_correction:
            return BiasState(self.cfg.decay.home_court_pts_per100, 1.0, 1.0, 0)
        return self.bias.state(before=date)

    def _season_type(self, game_id: str) -> object:
        if "season_type" not in self.games.columns:
            return 2
        st = self.games.loc[self.games["game_id"] == game_id, "season_type"]
        return st.iloc[0] if not st.empty and pd.notna(st.iloc[0]) else 2

    def game_context(self, game_id: str, odds_override: pd.Series | None = None, crew: list[str] | None = None,
                     state: ContextState | None = None, odds_tbl: pd.DataFrame | None = None) -> GameContext:
        """Todo lo que la pila de contexto aporta a un partido con el `state` dado (por defecto
        toda la historia; en backtest, el estado point-in-time de la fecha del partido)."""
        state = state or self.state
        rows = self.f[self.f["game_id"] == game_id].set_index("is_home")
        if len(rows) != 2:
            raise KeyError(f"Sin features pre-partido para ambos equipos de {game_id}")
        rh, ra = rows.loc[1], rows.loc[0]
        date = rh["game_date"]
        g = self.games[self.games["game_id"] == game_id]
        venue = g["venue"].iloc[0] if not g.empty and "venue" in g.columns else None
        league = self._league_probs(date)
        ph, pa = self.team_profile(rh), self.team_profile(ra)
        mu = float(rh.get("kf_league_mu", self.cfg.kalman.league_ortg_prior))
        bias = self.bias_state(date)
        hca = bias.hca_per100
        odds_tbl = self._first_odds() if odds_tbl is None else odds_tbl
        odds = odds_override
        if odds is None and (odds_tbl["game_id"] == game_id).any():
            odds = odds_tbl[odds_tbl["game_id"] == game_id].iloc[0]
        spread_home = float(odds["spread_close"]) if odds is not None and _finite(odds.get("spread_close")) else None
        ref = dict(self._referee_context(game_id, crew, rh, ra, state))
        ref["phi_context"] *= bias.total_factor(self._season_type(game_id))
        cross = {  # cruces asimétricos: ataque a la pintura vs rim protection rival, y árbitros
            "home": {"FT2": ref["ft_mod_home"],
                     "2PT": 1 + CROSS_RIM_WEIGHT * float(np.clip(ra.get("rim_fg_conceded_vs_exp", 0), -0.1, 0.1))},
            "away": {"FT2": ref["ft_mod_away"],
                     "2PT": 1 + CROSS_RIM_WEIGHT * float(np.clip(rh.get("rim_fg_conceded_vs_exp", 0), -0.1, 0.1))},
        }
        lam0 = build_matchup(ph, pa, league, mu, hca, ref["phi_context"]).lam
        fav_home = spread_home < 0 if spread_home is not None else rh["strength_net"] >= ra["strength_net"]
        teams = tuple(self._team_context(r, opp, venue, lam0, bool(is_fav), state, prof.off_rating)
                      for r, prof, opp, is_fav in ((rh, ph, ra["team"], fav_home), (ra, pa, rh["team"], not fav_home)))
        return GameContext(game_id, date, int(rh["season"]), ph, pa, league, mu, ref["phi_context"], cross, lam0,
                           spread_home, odds, teams, hca=hca)

    def scenarios(self, ctx: GameContext, dynamic: DynamicModifierEngine | None = None,
                  shrink_k: dict[str, float] | None = None) -> tuple[Scenario, Scenario]:
        """Escenarios Mejor/Normal/Peor (local, visitante). `dynamic`/`shrink_k` permiten evaluar
        otro scenario_shift u otras constantes de encogimiento sin reconstruir el contexto."""
        dynamic = dynamic or self.dynamic
        k = shrink_k or self.state.patterns.k
        out = []
        for t in ctx.teams:
            adj = {**DeepHistoricalPatternEngine.shrink_parts(t.hist_parts, ctx.lam0, k), **t.other_adj}
            out.append(dynamic.build_scenario(t.team, t.base_ortg, adj, t.star_factor))
        return out[0], out[1]

    def project_game(self, game_id: str, odds_override: pd.Series | None = None,
                     crew: list[str] | None = None, with_props: bool = True) -> GameProjection:
        ctx = self.game_context(game_id, odds_override, crew)
        ph, pa, league, mu, cross = ctx.home, ctx.away, ctx.league, ctx.mu, ctx.cross
        date, odds, spread_home = ctx.date, ctx.odds, ctx.spread_home
        ref = {"phi_context": ctx.phi}
        hca = ctx.hca
        sh, sa = self.scenarios(ctx)
        scen = {ph.team: sh, pa.team: sa}
        core = MonteCarloVectorizedCore(self.cfg.sim, mu, hca, league)
        mc = core.run(ph, pa, scen[ph.team], scen[pa.team], spread_home, ref["phi_context"], cross)
        # Spec 4: proyección exacta del margen (100.000 iteraciones) en el escenario Normal/Normal.
        params = build_matchup(TeamProfile(**{**ph.__dict__, "off_rating": scen[ph.team].normal}),
                               TeamProfile(**{**pa.__dict__, "off_rating": scen[pa.team].normal}),
                               league, mu, hca, ref["phi_context"], cross_mods=cross)
        exact = PossessionMarkovEngine(self.cfg.sim).simulate(params, self.cfg.sim.n_sims_markov)
        market_total = float(odds["total_close"]) if odds is not None and _finite(odds.get("total_close")) else None
        raw_margin, raw_total = float(exact.margin.mean()), float(exact.total.mean())
        mc, exact, blend_info = self._apply_blend(mc, exact, date, spread_home, market_total, game_id)
        edges = [self.analyzer.evaluate(mc, q) for q in self._quotes(odds, ph.team, pa.team)]
        hs, as_, p_score = exact.most_likely_score()
        dens = self.analyzer.margin_density(mc)
        crit = exact.critical_margin_mass()
        best = max(edges, key=lambda e: e.rae) if edges else None
        row = {
            "game_id": game_id, "game_date": date, "season": ctx.season, "model_version": MODEL_VERSION,
            "home_team": ph.team, "away_team": pa.team,
            "p_home_win_markov": exact.home_win_prob(), "p_home_win_density": float(dens[dens.index > 0].sum()),
            "exp_margin": float(exact.margin.mean()), "modal_margin": exact.modal_margin(),
            "exp_total": float(exact.total.mean()), "likely_score": f"{hs}-{as_}", "likely_score_p": p_score,
            "lambda_pace": params.lam, "market_spread_home": spread_home,
            "market_total": float(odds["total_close"]) if odds is not None and _finite(odds.get("total_close")) else None,
            **{f"crit_{k}": v for k, v in crit.items()},
            "best_rae": best.rae if best else np.nan, "best_side": best.quote.side if best else None,
            "best_exploitable": best.exploitable if best else False,
            "scen_home_normal": scen[ph.team].normal, "scen_away_normal": scen[pa.team].normal,
            "model_margin_raw": raw_margin, "model_total_raw": raw_total, **blend_info,
        }
        winner = ph.team if row["p_home_win_markov"] >= 0.5 else pa.team
        sheet = self.analyzer.tear_sheet(mc, edges) + "\n" + "\n".join([
            f"PROYECCIÓN MARKOV (spec 4) — {self.cfg.sim.n_sims_markov:,} iteraciones, escenario Normal/Normal",
            f"  Ganador probable: {winner}  P(local)={row['p_home_win_markov']:.3f}  "
            f"E[margen local]={row['exp_margin']:+.2f}  Modo(ΔY)={row['modal_margin']:+d}  E[total]={row['exp_total']:.1f}",
            f"  Marcador exacto más probable: {ph.team} {hs} - {as_} {pa.team} (p={p_score:.4f})",
            "  Masa en márgenes críticos del ganador: " + ", ".join(f"{k}={v:.3f}" for k, v in crit.items()),
            "  Ajustes de escenario (pts/100): " + "; ".join(
                f"{t}: " + ", ".join(f"{k}={v:+.2f}" for k, v in s.components.items() if abs(v) > 0.005 and k != "star_factor")
                for t, s in scen.items()),
        ])
        props = pd.DataFrame()
        if with_props:
            nn = mc.grid[("normal", "normal")]
            parts = [core.simulate_props(nn, t, is_home, pl) for t, is_home in ((ph.team, True), (pa.team, False))
                     if not (pl := self._props_players(t, date)).empty]
            props = pd.concat(parts, ignore_index=True) if parts else props
        return GameProjection(row, sheet, props, edges)

    # ------------------------------------------------------------------ mezcla con mercado
    def fit_blender(self, predictions: pd.DataFrame | None = None, min_games_played: int = 10) -> MarketBlender:
        """Ajusta la mezcla modelo+cierre con predicciones point-in-time del modelo base
        (por defecto, el backtest de la propia historia)."""
        bt = predictions if predictions is not None else self.backtest(min_games_played=min_games_played)
        tot = self._first_odds().set_index("game_id")["total_close"] if not self.odds.empty else pd.Series(dtype=float)
        preds = bt.assign(market_total=bt["game_id"].map(tot))
        self.blender = MarketBlender(preds[["game_date", "exp_margin", "exp_total", "market_spread",
                                            "market_total", "actual_margin", "actual_total"]])
        return self.blender

    def _apply_blend(self, mc: MonteCarloOutput, exact: SimulationResult, date: pd.Timestamp,
                     spread_home: float | None, market_total: float | None,
                     game_id: str) -> tuple[MonteCarloOutput, SimulationResult, dict]:
        """Desplaza la rejilla, los bloques B2/B3 y la proyección exacta a la media mezclada.
        Los bloques B1 ya representan la línea de mercado y no se tocan."""
        if self.blender is None:
            return mc, exact, {}
        st = self.blender.state(date)
        m0, t0 = float(exact.margin.mean()), float(exact.total.mean())
        m1, t1 = MarketBlender.blend(st, m0, t0, spread_home, market_total)
        dm, dt = m1 - m0, t1 - t0
        rng = np.random.default_rng(game_seed(self.cfg.sim.seed + 99, game_id))
        grid = {k: shift_simulation(v, dm, dt, rng) for k, v in mc.grid.items()}
        blocks = {}
        for name, b in mc.blocks.items():
            if name == "B2":
                sim = grid[("normal", "best")]
            elif name.startswith("B3_"):
                sim = grid[(name[3:], "normal")]
            else:
                sim = b.sim
            blocks[name] = BlockResult(b.name, b.description, sim)
        out = MonteCarloOutput(mc.home, mc.away, mc.favorite, blocks, grid, mc.props)
        info = {"blend_w_margin": st.w_margin, "blend_w_total": st.w_total, "blend_shift_margin": dm,
                "blend_shift_total": dt}
        return out, shift_simulation(exact, dm, dt, rng), info

    def run(self, game_ids: list[str], with_props: bool = True) -> tuple[pd.DataFrame, list[GameProjection]]:
        out = []
        for gid in game_ids:
            try:
                out.append(self.project_game(gid, with_props=with_props))
            except (KeyError, ValueError) as exc:
                log.error("Partido %s omitido: %s", gid, exc)
        return pd.DataFrame([p.row for p in out]), out

    # ------------------------------------------------------------------ backtest
    def backtest_pairs(self, min_games_played: int = 10,
                       game_ids: list[str] | None = None) -> list[tuple[pd.Series, pd.Series]]:
        """(fila local, fila visitante) de cada partido jugado elegible, en orden cronológico."""
        homes = self.f[(self.f["is_home"] == 1) & self.f["target_margin"].notna()
                       & (self.f["games_played"] >= min_games_played)]
        if game_ids is not None:
            homes = homes[homes["game_id"].isin(game_ids)]
        aways = self.f[self.f["is_home"] == 0].set_index("game_id")
        pairs = []
        for _, rh in homes.sort_values(["game_date", "game_id"], kind="stable").iterrows():
            if rh["game_id"] in aways.index:
                ra = aways.loc[rh["game_id"]].copy()
                ra["game_id"] = rh["game_id"]
                pairs.append((rh, ra))
        return pairs

    def backtest(self, min_games_played: int = 10, n_sims: int | None = None, mode: str = "base",
                 game_ids: list[str] | None = None) -> pd.DataFrame:
        """Proyección pre-partido de cada partido jugado para medir calibración vs el cierre.

        mode="base":    rating base (Kalman + Ridge), sin capas de contexto; `n_sims` totales.
        mode="context": pila completa (L5, patrones históricos, ineficiencias, dinámicos, árbitros)
                        reconstruida point-in-time con partidos de fecha < la del partido, y
                        densidad de la rejilla 3×3 Mejor/Normal/Peor; `n_sims` por celda."""
        if mode not in ("base", "context"):
            raise ValueError(f"Modo de backtest desconocido: {mode}")
        pairs = self.backtest_pairs(min_games_played, game_ids)
        odds_tbl = self._first_odds()
        if mode == "base":
            rows = self._base_rows(pairs, n_sims or BACKTEST_SIMS)
        else:
            rows = self._context_rows(pairs, n_sims or CONTEXT_BACKTEST_SIMS, odds_tbl)
        bt = pd.DataFrame(rows)
        if bt.empty:
            return bt
        mkt = odds_tbl.set_index("game_id")
        bt = bt.join(pd.DataFrame([market_probs(mkt.loc[g] if g in mkt.index else None) for g in bt["game_id"]],
                                  index=bt.index))
        bt.attrs["metrics"] = self.backtest_metrics(bt)
        return bt

    def _base_rows(self, pairs: list[tuple[pd.Series, pd.Series]], n_sims: int) -> list[dict]:
        eng = PossessionMarkovEngine(self.cfg.sim)
        spreads = self._first_odds().set_index("game_id")["spread_close"] if not self.odds.empty else pd.Series()
        rows = []
        for i, (rh, ra) in enumerate(pairs):
            b = self.bias_state(rh["game_date"])
            params = build_matchup(self.team_profile(rh), self.team_profile(ra), self._league_probs(rh["game_date"]),
                                   float(rh["kf_league_mu"]), b.hca_per100,
                                   b.total_factor(self._season_type(rh["game_id"])))
            sim = eng.simulate(params, n_sims, seed=self.cfg.sim.seed + i)
            spread = spreads.get(rh["game_id"], np.nan)
            rows.append({"game_id": rh["game_id"], "game_date": rh["game_date"], "home": rh["team"], "away": ra["team"],
                         **single_summary(sim, float(spread) if _finite(spread) else None),
                         "actual_margin": rh["target_margin"], "actual_total": rh["target_total"]})
        return rows

    def _context_rows(self, pairs: list[tuple[pd.Series, pd.Series]], n_sims: int,
                      odds_tbl: pd.DataFrame) -> list[dict]:
        sim_cfg = replace(self.cfg.sim, n_sims_block=n_sims)
        rows, state, state_date = [], None, None
        for rh, ra in pairs:
            if rh["game_date"] != state_date:  # un estado point-in-time por fecha
                state, state_date = self.context_state(before=rh["game_date"]), rh["game_date"]
            ctx = self.game_context(rh["game_id"], state=state, odds_tbl=odds_tbl)
            sh, sa = self.scenarios(ctx, shrink_k=state.patterns.k)
            core = MonteCarloVectorizedCore(sim_cfg, ctx.mu, ctx.hca, ctx.league)
            grid = core.scenario_grid(ctx.home, ctx.away, sh, sa, ctx.phi, ctx.cross,
                                      seed=game_seed(sim_cfg.seed, rh["game_id"]))
            rows.append({"game_id": rh["game_id"], "game_date": rh["game_date"], "home": rh["team"], "away": ra["team"],
                         **mixture_summary(grid, sim_cfg.scenario_weights, ctx.spread_home),
                         "scen_home_normal": sh.normal, "scen_away_normal": sa.normal,
                         "actual_margin": rh["target_margin"], "actual_total": rh["target_total"]})
        return rows

    @staticmethod
    def backtest_metrics(bt: pd.DataFrame) -> dict[str, float]:
        """Métricas del modelo (claves históricas + extendidas) y del cierre de mercado."""
        y = (bt["actual_margin"] > 0).astype(float)
        p = bt["p_home"].clip(1e-4, 1 - 1e-4)
        model = score(bt)
        market = score_market(bt)
        return {
            "n": len(bt), "brier": model["brier"],
            "log_loss": float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()),
            "accuracy_winner": float(((bt["p_home"] > 0.5) == (bt["actual_margin"] > 0)).mean()),
            "mae_margin_model": model["mae_margin"],
            "mae_margin_market": float((-bt["market_spread"] - bt["actual_margin"]).abs().mean()),
            "mae_total_model": model["mae_total"], "mae_total_market": market["mae_total"],
            "brier_market": market["brier"], "log_loss_spread": model["log_loss_spread"],
            "log_loss_spread_market": market["log_loss_spread"], "ats_hit_rate": model["ats_hit_rate"],
            "n_spread": model["n_spread"],
        }
