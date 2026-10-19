"""CLASE 6 — MonteCarloVectorizedCore (spec 3 fase 3) sobre el motor Markov de posesiones.

Matriz de ejecución dirigida (7 bloques × 50.000 simulaciones):
  B1a-c  Test de sesgo de casino:  Favorito(línea de mercado) vs Dog{Mejor, Normal, Peor}
  B2     Prueba de resistencia:     Favorito(base equilibrada)  vs Dog(Mejor)
  B3a-c  Drawdown y riesgo:         Favorito{Mejor, Normal, Peor} vs Dog(base equilibrada)
Además se simula la rejilla completa 3×3 (Fav{M,N,P} × Dog{M,N,P}) para la curva de densidad
global ponderada (60/20/20) que usa el analizador financiero.
Props: 1.000 simulaciones por jugador atadas al ritmo y a los puntos del equipo simulados.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from nba_quant.config import SimulationConfig
from nba_quant.logging_utils import get_logger
from nba_quant.models.markov import PossessionMarkovEngine, SimulationResult, TeamProfile, build_matchup
from nba_quant.simulation.context import Scenario
from nba_quant.simulation.inefficiencies import MarketInefficienciesEngine

log = get_logger("monte_carlo")

STATES3 = ("best", "normal", "worst")
PROP_NB_DISPERSION = 6.0  # r de la Binomial Negativa de puntos de jugador


@dataclass
class BlockResult:
    name: str
    description: str
    sim: SimulationResult


@dataclass
class MonteCarloOutput:
    home: str
    away: str
    favorite: str
    blocks: dict[str, BlockResult]
    grid: dict[tuple[str, str], SimulationResult]  # (estado_fav, estado_dog) -> sim
    props: pd.DataFrame = field(default_factory=pd.DataFrame)


class MonteCarloVectorizedCore:
    def __init__(self, cfg: SimulationConfig, league_ortg: float, hca_per100: float,
                 league_probs: dict[str, float] | None = None) -> None:
        self.cfg = cfg
        self.engine = PossessionMarkovEngine(cfg)
        self.league_ortg = league_ortg
        self.hca = hca_per100
        self.league_probs = league_probs

    def _sim(self, home: TeamProfile, away: TeamProfile, home_ortg: float, away_ortg: float,
             phi: float, seed: int, cross_mods: dict | None) -> SimulationResult:
        """Simula con los pts/100 de cada ataque fijados por escenario (vs una defensa media)."""
        h = TeamProfile(**{**home.__dict__, "off_rating": home_ortg})
        a = TeamProfile(**{**away.__dict__, "off_rating": away_ortg})
        params = build_matchup(h, a, self.league_probs, self.league_ortg, self.hca, phi, cross_mods=cross_mods)
        sim = self.engine.simulate(params, self.cfg.n_sims_block, seed)
        return self._relax(sim)

    def _relax(self, sim: SimulationResult) -> SimulationResult:
        """Garbage Time Relaxing Factor aplicado a márgenes amplios (repartido en ambos marcadores)."""
        margin = sim.margin
        relaxed = MarketInefficienciesEngine.garbage_relax(margin, self.cfg.garbage_relax_threshold,
                                                          self.cfg.garbage_relax_factor)
        delta = margin - relaxed
        half = (delta / 2).astype(np.int32)
        return SimulationResult((sim.home_pts - half).astype(np.int32),
                                (sim.away_pts + (delta - half)).astype(np.int32), sim.overtime, sim.meta)

    @staticmethod
    def market_line_ortg(fav_is_home: bool, dog_ortg: float, fav_def: float, dog_def: float,
                         market_spread: float, lam: float, hca: float) -> float:
        """pts/100 del favorito tal que E[margen] = |línea de mercado|.

        E[margen] ≈ λ/100 · [(fav_o + dog_def) − (dog_o + fav_def) + hca_term]  =>  despejar fav_o."""
        hca_term = hca if fav_is_home else -hca
        return dog_ortg + fav_def - dog_def + 100.0 * abs(market_spread) / lam - hca_term

    def run(self, home: TeamProfile, away: TeamProfile, scen_home: Scenario, scen_away: Scenario,
            market_spread_home: float | None, phi_context: float = 1.0,
            cross_mods: dict | None = None) -> MonteCarloOutput:
        # Favorito: el de mercado si hay línea; si no, el del modelo.
        if market_spread_home is not None and np.isfinite(market_spread_home) and market_spread_home != 0:
            fav_is_home = market_spread_home < 0
        else:
            fav_is_home = scen_home.normal + self.hca / 2 >= scen_away.normal - self.hca / 2
        fav, dog = (scen_home, scen_away) if fav_is_home else (scen_away, scen_home)
        seed = self.cfg.seed

        def sim(fav_ortg: float, dog_ortg: float, k: int) -> SimulationResult:
            ho, ao = (fav_ortg, dog_ortg) if fav_is_home else (dog_ortg, fav_ortg)
            return self._sim(home, away, ho, ao, phi_context, seed + k, cross_mods)

        grid = {}
        for i, fs in enumerate(STATES3):
            for j, ds in enumerate(STATES3):
                grid[(fs, ds)] = sim(getattr(fav, fs), getattr(dog, ds), 10 * i + j)
        blocks: dict[str, BlockResult] = {}
        if market_spread_home is not None and np.isfinite(market_spread_home):
            lam = grid[("normal", "normal")].meta["lambda_pace"]
            fav_p, dog_p = (home, away) if fav_is_home else (away, home)
            for j, ds in enumerate(STATES3):
                dog_o = getattr(dog, ds)
                fav_mkt = self.market_line_ortg(fav_is_home, dog_o, fav_p.def_rating, dog_p.def_rating,
                                                market_spread_home, lam, self.hca)
                blocks[f"B1_{ds}"] = BlockResult(f"B1_{ds}", f"Fav(línea mercado) vs Dog({ds})", sim(fav_mkt, dog_o, 100 + j))
        blocks["B2"] = BlockResult("B2", "Fav(base) vs Dog(best)", grid[("normal", "best")])
        for fs in STATES3:
            blocks[f"B3_{fs}"] = BlockResult(f"B3_{fs}", f"Fav({fs}) vs Dog(base)", grid[(fs, "normal")])
        return MonteCarloOutput(home.team, away.team, fav.team, blocks, grid)

    def scenario_grid(self, home: TeamProfile, away: TeamProfile, scen_home: Scenario, scen_away: Scenario,
                      phi_context: float = 1.0, cross_mods: dict | None = None,
                      seed: int | None = None) -> dict[tuple[str, str], SimulationResult]:
        """Rejilla 3×3 indexada por (estado_local, estado_visitante), sin bloques de mercado.
        Las celdas con los mismos pts/100 (p.ej. shift=0) se simulan una sola vez."""
        seed = self.cfg.seed if seed is None else seed
        cache: dict[tuple[float, float], SimulationResult] = {}
        grid = {}
        for i, hs in enumerate(STATES3):
            for j, as_ in enumerate(STATES3):
                key = (getattr(scen_home, hs), getattr(scen_away, as_))
                if key not in cache:
                    cache[key] = self._sim(home, away, *key, phi_context, seed + 10 * i + j, cross_mods)
                grid[(hs, as_)] = cache[key]
        return grid

    # ------------------------------------------------------------------ props
    def simulate_props(self, base: SimulationResult, team: str, is_home: bool, players: pd.DataFrame,
                       line_col: str = "line") -> pd.DataFrame:
        """`players`: player_name, pts_share (cuota de puntos del equipo), min_mean, min_sd,
        [line]. 1.000 sims por jugador: minutos ~ N truncada, puntos ~ NegBin con media
        = cuota · puntos del equipo simulados · (minutos/minutos medios)."""
        if players.empty:
            return pd.DataFrame()
        rng = np.random.default_rng(self.cfg.seed + 7)
        n = self.cfg.n_sims_props
        team_pts = (base.home_pts if is_home else base.away_pts)
        idx = rng.choice(team_pts.size, size=n, replace=False)
        tp = team_pts[idx].astype(float)[None, :]
        share = players["pts_share"].to_numpy(float)[:, None]
        mmean = players["min_mean"].to_numpy(float)[:, None]
        msd = players["min_sd"].fillna(4.0).to_numpy(float)[:, None]
        minutes = np.clip(rng.normal(mmean, msd, size=(len(players), n)), 0, 48)
        mu = np.clip(share * tp * minutes / np.maximum(mmean, 1.0), 0.01, None)
        r = PROP_NB_DISPERSION
        pts = rng.negative_binomial(r, r / (r + mu))
        out = players[["player_name"]].copy()
        out["team"] = team
        out["proj_mean"] = pts.mean(axis=1)
        out["proj_median"] = np.median(pts, axis=1)
        out["p10"], out["p90"] = np.percentile(pts, 10, axis=1), np.percentile(pts, 90, axis=1)
        if line_col in players.columns:
            lines = players[line_col].to_numpy(float)[:, None]
            out["line"] = players[line_col].to_numpy()
            out["p_over"] = (pts > lines).mean(axis=1)
        return out
