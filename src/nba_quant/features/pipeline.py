"""NBAAdvancedFeaturePipeline (spec 1): PBP crudo -> matriz de features pre-partido sin nulos.

Métodos (en orden de ejecución, cada uno devuelve su DataFrame y deja el estado en `self`):
  A load_and_clean_pbp                 PBP limpio + garbage time + lineups
  B calculate_efficiency_and_pace      posesiones, tiros (xeFG), ratings, pace, transición
  C calculate_paint_and_rim_metrics    rim protection con/sin ancla, rebote, pintura
  D calculate_shot_quality_and_tracking  xeFG/shot making, USG/True Usage, tracking oficial
  E calculate_possession_dynamics      scoring rate, clutch, Four Factors, ATO, On/Off estrella
  F calculate_regression_signals       3PT luck, FT luck, live/dead TOV
  G apply_opponent_adjustment_and_decay  decaimiento exponencial, Ridge, Kalman, imputación

Salida `run()`: DataFrame indexado por [season, game_date, team] con features PRE-partido
(sólo usan información anterior a la fecha) + columnas `target_*` con el resultado real.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from nba_quant.config import EngineConfig
from nba_quant.features import player_metrics as pm
from nba_quant.features.adjustment import (point_in_time_reference, pregame_decayed_means,
                                           ridge_opponent_adjustment, season_end_priors, shrink_to_prior)
from nba_quant.features.roster import compute_rapm, roster_priors
from nba_quant.features.shot_quality import ShotQualityModel
from nba_quant.features.team_game import aggregate_possessions, aggregate_shots, attach_opponent, derive_rates
from nba_quant.logging_utils import get_logger
from nba_quant.models.kalman import run_kalman
from nba_quant.processing.lineups import build_lineups, offense_defense_lineups
from nba_quant.processing.pbp import load_and_clean_pbp
from nba_quant.processing.possessions import build_possessions, build_shots
from nba_quant.storage.lake import DataLake
from nba_quant.teams import TEAM_GEO

log = get_logger("pipeline")

ID_COLS = ["season", "game_date", "game_id", "team", "opponent", "is_home"]
INCOMPLETE_PBP_TOLERANCE = 3  # puntos de diferencia marcador recalculado vs oficial
RIDGE_BLEND_MAX = 0.5  # peso máximo del rating Ridge frente al Kalman en régimen dinámico


class PipelineStateError(RuntimeError):
    """Se llamó un paso sin ejecutar antes sus dependencias."""


class NBAAdvancedFeaturePipeline:
    def __init__(self, cfg: EngineConfig, lake: DataLake | None = None,
                 pbp: pd.DataFrame | None = None, games: pd.DataFrame | None = None,
                 player_box: pd.DataFrame | None = None, tracking: pd.DataFrame | None = None,
                 injuries: pd.DataFrame | None = None) -> None:
        """Fuente de datos: el `lake` o DataFrames directos (tests / datos sintéticos)."""
        self.cfg = cfg
        self.lake = lake
        self._raw = {"pbp": pbp, "games": games, "player_box": player_box, "tracking": tracking,
                     "injuries": injuries}
        self.events: pd.DataFrame | None = None
        self.poss: pd.DataFrame | None = None
        self.shots: pd.DataFrame | None = None
        self.game_sums: pd.DataFrame | None = None
        self.usage: pd.DataFrame | None = None
        self.roles: pd.DataFrame | None = None
        self.tracking_wide = pd.DataFrame()
        self.incomplete_games: set[str] = set()
        self.roster_detail = pd.DataFrame()
        self.upcoming: pd.DataFrame | None = None
        self.kalman = None

    # ------------------------------------------------------------------ utilidades
    def _table(self, name: str, seasons: list[int] | None) -> pd.DataFrame:
        df = self._raw.get(name)
        if df is None and self.lake is not None:
            df = self.lake.read(name, seasons)
        if df is None:
            return pd.DataFrame()
        if seasons is not None and "season" in df.columns:
            df = df[df["season"].isin(seasons)]
        return df.reset_index(drop=True)

    def _require(self, *attrs: str) -> None:
        missing = [a for a in attrs if getattr(self, a) is None]
        if missing:
            raise PipelineStateError(f"Ejecute antes los pasos que generan: {missing}")

    def _merge_sums(self, extra: pd.DataFrame) -> None:
        if extra is None or extra.empty:
            return
        cols = [c for c in extra.columns if c not in ("game_id", "team")]
        self.game_sums = self.game_sums.drop(columns=[c for c in cols if c in self.game_sums.columns])
        self.game_sums = self.game_sums.merge(extra, on=["game_id", "team"], how="left")

    # ------------------------------------------------------------------ A
    def load_and_clean_pbp(self, seasons: list[int] | None = None) -> pd.DataFrame:
        pbp = self._table("pbp", seasons)
        self.games = self._table("games", seasons)
        self.player_box = self._table("player_box", seasons)
        if pbp.empty or self.games.empty:
            raise ValueError("No hay PBP/partidos para las temporadas pedidas; ejecute la ingesta")
        self.games["game_date"] = pd.to_datetime(self.games["game_date"])
        if "season_type" in self.games.columns:  # sólo temporada regular + playoffs
            self.games = self.games[self.games["season_type"].isin([2, 3])]
        # Fuera All-Star / exhibiciones contra equipos no-NBA.
        self.games = self.games[self.games["home_team"].isin(TEAM_GEO) & self.games["away_team"].isin(TEAM_GEO)]
        pbp = pbp[pbp["game_id"].isin(self.games["game_id"])]
        events = load_and_clean_pbp(pbp, self.cfg.game_state)
        self.incomplete_games = self._incomplete_pbp_games(events)
        events = build_lineups(events, self.player_box)
        self.events = offense_defense_lineups(events)
        return self.events

    def _incomplete_pbp_games(self, events: pd.DataFrame) -> set[str]:
        """Partidos a los que les faltan eventos: el marcador reconstruido difiere del oficial.
        Sus sumas PBP se tratan como desconocidas (no alimentan ratings), pero el partido sigue
        en la matriz con su resultado oficial como target."""
        last = events.groupby("game_id")[["home_score_calc", "away_score_calc"]].last()
        off = self.games.set_index("game_id")[["home_score", "away_score"]].reindex(last.index)
        gap = (last["home_score_calc"] - off["home_score"]).abs() + (last["away_score_calc"] - off["away_score"]).abs()
        bad = set(gap[gap > INCOMPLETE_PBP_TOLERANCE].index)
        if bad:
            log.warning("PBP incompleto en %d partidos (excluidos de ratings): %s", len(bad), sorted(bad))
        return bad

    # ------------------------------------------------------------------ B
    def calculate_efficiency_and_pace(self) -> pd.DataFrame:
        self._require("events")
        events, poss = build_possessions(self.events, self.cfg.game_state)
        shots = build_shots(events, poss, self.cfg.zones, self.cfg.game_state)
        self.events, self.poss = events, poss
        self.shots = ShotQualityModel().annotate(shots)
        sums = aggregate_possessions(poss).merge(aggregate_shots(self.shots), on=["game_id", "team"], how="left")
        self.game_sums = sums
        return sums

    # ------------------------------------------------------------------ C
    def calculate_paint_and_rim_metrics(self) -> pd.DataFrame:
        self._require("game_sums", "shots")
        if not self.player_box.empty:
            self.roles = pm.point_in_time_roles(self.player_box, self.games)
            self._merge_sums(pm.rim_protection(self.shots, self.roles))
        return self.game_sums

    # ------------------------------------------------------------------ D
    def calculate_shot_quality_and_tracking(self) -> pd.DataFrame:
        self._require("game_sums")
        self.usage = pm.player_usage(self.events, self.poss)
        self._merge_sums(pm.usage_concentration(self.usage))
        self.tracking_wide = self._tracking_snapshots()
        return self.game_sums

    def _tracking_snapshots(self) -> pd.DataFrame:
        """Tracking oficial (nba_api: drives, pases, hustle, velocidad, defensa del aro) en
        formato ancho por (team, as_of_date). Vacío si stats.nba.com no estuvo accesible."""
        trk = self._table("tracking_team", None)
        if trk.empty:
            log.info("Sin tracking oficial en el lake: se omiten columnas trk_*")
            return pd.DataFrame()
        trk["col"] = "trk_" + trk["endpoint"] + "_" + trk["metric"].str.lower()
        return trk.pivot_table(index=["team", "as_of_date"], columns="col", values="value").reset_index()

    def _merge_tracking(self, feats: pd.DataFrame) -> pd.DataFrame:
        """Unión as-of: el snapshot más reciente ESTRICTAMENTE anterior a la fecha del partido."""
        wide = getattr(self, "tracking_wide", pd.DataFrame())
        if wide.empty:
            return feats
        wide = wide.assign(as_of_date=pd.to_datetime(wide["as_of_date"]) + pd.Timedelta(days=1))
        left = feats.sort_values("game_date")
        merged = pd.merge_asof(left, wide.sort_values("as_of_date"), left_on="game_date",
                               right_on="as_of_date", by="team", direction="backward")
        return merged.drop(columns=["as_of_date"])

    # ------------------------------------------------------------------ E
    def calculate_possession_dynamics(self) -> pd.DataFrame:
        self._require("game_sums")
        if self.roles is not None:
            self._merge_sums(pm.star_on_off(self.poss, self.roles))
        self._merge_sums(pm.foul_trouble(self.events))
        return self.game_sums

    # ------------------------------------------------------------------ F
    def calculate_regression_signals(self) -> pd.DataFrame:
        self._require("game_sums")
        self._merge_sums(pm.ft_expectation(self.events, self.games))
        return self.game_sums

    # ------------------------------------------------------------------ G
    def _game_level_table(self) -> pd.DataFrame:
        sums = self.game_sums.fillna({c: 0 for c in self.game_sums.columns if c not in ("game_id", "team")})
        df = attach_opponent(sums, self.games)
        df = df.merge(self.games[["game_id", "season", "game_date"]], on="game_id", how="left")
        stat_cols = [c for c in df.columns if c not in ID_COLS]
        df.loc[df["game_id"].isin(self.incomplete_games), stat_cols] = np.nan
        if self.upcoming is not None and not self.upcoming.empty:
            # Partidos futuros: filas sin sumas (NaN). El EWM con ignore_na hace que su feature
            # pre-partido sea el estado tras el último partido jugado.
            up = self.upcoming
            rows = pd.concat([
                up.assign(team=up["home_team"], opponent=up["away_team"], is_home=1),
                up.assign(team=up["away_team"], opponent=up["home_team"], is_home=0),
            ])[["game_id", "season", "game_date", "team", "opponent", "is_home"]]
            df = pd.concat([df, rows], ignore_index=True)
        return df

    @staticmethod
    def derive_extra_rates(df: pd.DataFrame) -> pd.DataFrame:
        """Ratios de los bloques C-F que no están en `derive_rates`."""
        r = {}
        safe = lambda n, d: n / d.replace(0, np.nan)  # noqa: E731
        if "rim_fga_anchor_on" in df.columns:
            r["rim_fg_allowed_anchor_on"] = safe(df["rim_fgm_anchor_on"], df["rim_fga_anchor_on"])
            r["rim_fg_allowed_anchor_off"] = safe(df["rim_fgm_anchor_off"], df["rim_fga_anchor_off"])
            r["rim_protection_delta"] = r["rim_fg_allowed_anchor_off"] - r["rim_fg_allowed_anchor_on"]
            r["rim_deterrence_on"] = safe(df["rim_fga_anchor_on"], df["opp_poss"])
        if "star_o_poss_on" in df.columns:
            on = safe(df["star_o_pts_on"], df["star_o_poss_on"]) - safe(df["star_d_pts_on"], df["star_d_poss_on"])
            off = safe(df["star_o_pts_off"], df["star_o_poss_off"]) - safe(df["star_d_pts_off"], df["star_d_poss_off"])
            r["star_on_net"], r["star_off_net"] = 100 * on, 100 * off
            r["star_on_off_diff"] = 100 * (on - off)
        if "ft_expected" in df.columns:
            r["ft_luck_off"] = safe(df["ft_made"] - df["ft_expected"], df["ft_att"])
            r["ft_luck_def"] = safe(df["opp_ft_made"] - df["opp_ft_expected"], df["opp_ft_att"])
        if "foul_trouble_events" in df.columns:
            r["foul_trouble_bench_rate"] = safe(df["foul_trouble_benched"], df["foul_trouble_events"])
        return pd.concat([df, pd.DataFrame(r, index=df.index)], axis=1)

    def _additive_columns(self, df: pd.DataFrame) -> list[str]:
        skip = set(ID_COLS) | {"game_id"}
        return [c for c in df.columns if c not in skip and pd.api.types.is_numeric_dtype(df[c])]

    def apply_opponent_adjustment_and_decay(self) -> pd.DataFrame:
        self._require("game_sums")
        h = self.cfg.decay.half_life_games
        game = self._game_level_table()
        add_cols = self._additive_columns(game)
        # 1) decaimiento exponencial de las sumas de partidos previos + prior multianual
        pre = pregame_decayed_means(game, add_cols, h)
        # Priors de la temporada siguiente: sólo temporada regular (los playoffs tienen otro ritmo).
        regular = set(self.games.loc[self.games.get("season_type", pd.Series(2, index=self.games.index)) == 2, "game_id"])
        played = game[game["poss"].notna() & game["game_id"].isin(regular)]
        pre = shrink_to_prior(pre, season_end_priors(played, add_cols, h), add_cols)
        feats = self.derive_extra_rates(derive_rates(pre))
        # 2) Shot Selection Over Expected: frecuencia propia (partido) vs lo que concede el rival (pre)
        game_rates = derive_rates(game)
        opp_allowed = feats[["game_id", "team"] + [f"opp_{z}_freq" for z in ("rim", "mid", "corner3", "above_break3")]]
        opp_allowed = opp_allowed.rename(columns={"team": "opponent", **{c: f"{c}_ctx" for c in opp_allowed.columns[2:]}})
        g2 = game_rates.merge(opp_allowed, on=["game_id", "opponent"], how="left")
        oe = g2[["season", "game_date", "game_id", "team", "opponent", "is_home"]].copy()
        for z in ("rim", "mid", "corner3", "above_break3"):
            oe[f"{z}_freq_oe"] = g2[f"{z}_freq"] - g2[f"opp_{z}_freq_ctx"]
        oe_pre = pregame_decayed_means(oe, [c for c in oe.columns if c.endswith("_oe")], h)
        feats = feats.merge(oe_pre.drop(columns=["opponent", "is_home", "games_played"]),
                            on=["season", "game_date", "game_id", "team"], how="left")
        # 3) Ridge opponent adjustment point-in-time
        ridge = ridge_opponent_adjustment(game, self.cfg.decay.ridge_alpha, h, self.cfg.decay.min_games_for_rating)
        feats = feats.merge(ridge.drop(columns=["season", "game_date"]), on=["game_id", "team"], how="left")
        # 4) Kalman (máquina de estados bayesiana)
        all_games = self.games if self.upcoming is None else pd.concat(
            [self.games, self.upcoming[[c for c in ("game_id", "season", "game_date", "home_team", "away_team",
                                                    "season_type") if c in self.upcoming.columns]]],
            ignore_index=True)
        sums_ok = self.game_sums[~self.game_sums["game_id"].isin(self.incomplete_games)]
        continuity, rapm_delta = self._roster_priors(all_games)
        kf_df, self.kalman = run_kalman(all_games, sums_ok, self.cfg.kalman, self.cfg.decay,
                                        self._raw.get("injuries"), continuity, rapm_delta)
        feats = feats.merge(kf_df.drop(columns=["season", "game_date"]), on=["game_id", "team"], how="left")
        feats = self._blend_strength(feats)
        feats = self._merge_tracking(feats)
        feats = self._schedule_features(feats)
        feats = self._attach_targets(feats, game)
        return self._impute(feats)

    def _roster_priors(self, all_games: pd.DataFrame) -> tuple[dict, dict]:
        """Continuidad y ΔRAPM para cada temporada nueva con plantilla conocida ANTES de su
        primer partido de temporada regular (una foto posterior filtraría fichajes futuros)."""
        rosters = self._table("rosters", None)
        if rosters.empty or self.poss is None:
            return {}, {}
        rosters = rosters.assign(snapshot_date=pd.to_datetime(rosters["snapshot_date"]))
        stype = all_games["season_type"] if "season_type" in all_games.columns else pd.Series(2, index=all_games.index)
        continuity, delta = {}, {}
        for season in sorted(set(all_games["season"].dropna().astype(int))):
            prev_ids = self.games.loc[(self.games["season"] == season - 1)
                                      & (self.games.get("season_type", 2) == 2), "game_id"]
            if prev_ids.empty:
                continue
            reg = all_games[(all_games["season"] == season) & (stype.fillna(2) == 2)]
            cutoff = reg["game_date"].min() if not reg.empty else pd.Timestamp.max
            snaps = rosters[(rosters["season"] == season) & (rosters["snapshot_date"] <= cutoff)]
            if snaps.empty:
                log.info("Temporada %d: sin plantilla previa al inicio; prior sin ajuste de plantilla", season)
                continue
            snap = snaps[snaps["snapshot_date"] == snaps["snapshot_date"].max()]
            rapm = compute_rapm(self.poss[self.poss["game_id"].isin(prev_ids)])
            pr = roster_priors(self.player_box[self.player_box["game_id"].isin(prev_ids)], rapm, snap)
            continuity[season], delta[season] = pr.continuity, pr.rapm_delta
            self.roster_detail = pr.detail.assign(season=season)
        return continuity, delta

    def _blend_strength(self, f: pd.DataFrame) -> pd.DataFrame:
        """Rating final = Kalman, con peso Ridge que crece 0 -> 50% entre los partidos 11 y 20."""
        c = self.cfg.kalman
        g = f["kf_games"].fillna(0)
        w = np.clip((g - c.cold_start_games) / (c.stabilization_games - c.cold_start_games), 0, 1) * RIDGE_BLEND_MAX
        ridge_off = f.get("adj_off_rtg", pd.Series(np.nan, index=f.index))
        ridge_def = f.get("adj_def_rtg", pd.Series(np.nan, index=f.index))
        w = np.where(ridge_off.notna(), w, 0.0)
        f["strength_off"] = (1 - w) * f["kf_off"] + w * ridge_off.fillna(0)
        f["strength_def"] = (1 - w) * f["kf_def"] + w * ridge_def.fillna(0)
        f["strength_net"] = f["strength_off"] - f["strength_def"]
        return f

    def _schedule_features(self, f: pd.DataFrame) -> pd.DataFrame:
        f = f.sort_values(["team", "game_date"])
        prev = f.groupby(["season", "team"])["game_date"].shift(1)
        f["rest_days"] = (f["game_date"] - prev).dt.days.fillna(7).clip(upper=7) - 1
        f["is_b2b"] = (f["rest_days"] == 0).astype(int)
        third = f.groupby(["season", "team"])["game_date"].shift(2)
        f["is_3in4"] = ((f["game_date"] - third).dt.days <= 3).fillna(False).astype(int)
        return f

    def _attach_targets(self, f: pd.DataFrame, game: pd.DataFrame) -> pd.DataFrame:
        """Targets desde el marcador OFICIAL (no del PBP reconstruido); posesiones del PBP."""
        g = self.games
        official = pd.concat([
            g[["game_id", "home_team", "home_score", "away_score"]].set_axis(["game_id", "team", "target_pts", "target_opp_pts"], axis=1),
            g[["game_id", "away_team", "away_score", "home_score"]].set_axis(["game_id", "team", "target_pts", "target_opp_pts"], axis=1),
        ])
        poss = game[["game_id", "team", "poss"]].rename(columns={"poss": "target_poss"})
        f = f.merge(official, on=["game_id", "team"], how="left").merge(poss, on=["game_id", "team"], how="left")
        f["target_margin"] = f["target_pts"] - f["target_opp_pts"]
        f["target_total"] = f["target_pts"] + f["target_opp_pts"]
        return f

    @staticmethod
    def _impute(f: pd.DataFrame) -> pd.DataFrame:
        """Imputación point-in-time: mediana de liga de la fecha (o la última fecha anterior
        conocida). Sólo el arranque del dataset sin pasado usa la primera referencia futura y
        queda marcado en `is_cold_imputed` para poder excluirlo del entrenamiento."""
        num = [c for c in f.columns if pd.api.types.is_numeric_dtype(f[c]) and not c.startswith("target_")]
        f[num] = f[num].replace([np.inf, -np.inf], np.nan)
        n_missing = int(f[num].isna().sum().sum())
        ref, cold = point_in_time_reference(f, num, how="median")
        f[num] = f[num].fillna(ref).fillna(0.0)
        f["is_cold_imputed"] = cold.astype(int)
        if "kf_regime" in f.columns:
            f["kf_regime"] = f["kf_regime"].fillna("cold_start")
        log.info("Imputación: %d celdas rellenadas", n_missing)
        return f

    # ------------------------------------------------------------------ orquestación
    def run(self, seasons: list[int] | None = None, upcoming: pd.DataFrame | None = None) -> pd.DataFrame:
        """`upcoming` (opcional): partidos futuros (game_id, season, game_date, home_team, away_team)
        para los que se generan features pre-partido con el estado más reciente."""
        if upcoming is not None and not upcoming.empty:
            self.upcoming = upcoming.assign(game_date=pd.to_datetime(upcoming["game_date"]))
        self.load_and_clean_pbp(seasons)
        self.calculate_efficiency_and_pace()
        self.calculate_paint_and_rim_metrics()
        self.calculate_shot_quality_and_tracking()
        self.calculate_possession_dynamics()
        self.calculate_regression_signals()
        feats = self.apply_opponent_adjustment_and_decay()
        feats = feats.sort_values(["season", "game_date", "team"]).set_index(["season", "game_date", "team"])
        log.info("Matriz final: %d filas x %d columnas", *feats.shape)
        return feats
