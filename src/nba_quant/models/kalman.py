"""Adaptación bayesiana temporal: filtro de Kalman de fuerza ofensiva/defensiva (spec 4 §2).

Estado por equipo θ = [off, def] en pts/100 respecto a la media de liga (def = lo que PERMITE).
Observación por partido (local H, visitante A):
    ORtg_H − μ − h/2 = off_H + def_A + ε_H        ORtg_A − μ + h/2 = off_A + def_H + ε_A
    Var(ε) = (σ_pp·100)² / posesiones   (σ_pp ≈ 1.12 pts por posesión)

Régimen por nº de partido del equipo en la temporada:
  1-10  Cold start: media anclada al prior multianual (retención 70% × continuidad de plantilla
        + ΔRAPM de altas/bajas) y R inflada -> ganancia K conservadora.
  11-20 Estabilización: la inflación de R decae linealmente a 1 (el prior pierde peso hasta 0%).
  21+   Dinámico: Q calibrada para que el filtro equivalga a un decaimiento exponencial de
        vida media h partidos:  Q = R·α²/(1−α), α = 1 − 2^(−1/h).
Baja de un titular clave -> Q × φ_injury (3-5) para re-aprender en 1-2 partidos.
Playoffs -> R × playoff_r_inflation: cuentan, pero no dominan el prior de la temporada siguiente.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from nba_quant.config import DecayConfig, KalmanConfig
from nba_quant.logging_utils import get_logger

log = get_logger("kalman")

H_MATRIX = np.array([[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0]])
TYPICAL_POSS = 100.0
LEAGUE_MU_ALPHA = 0.02  # actualización lenta de la media de liga


@dataclass
class TeamState:
    mean: np.ndarray = field(default_factory=lambda: np.zeros(2))
    cov: np.ndarray = field(default_factory=lambda: np.eye(2) * 16.0)
    games: int = 0


class TeamStrengthKalman:
    """Filtro secuencial sobre partidos ordenados por fecha. Produce el estado PRE-partido."""

    def __init__(self, cfg: KalmanConfig, decay: DecayConfig) -> None:
        self.cfg = cfg
        self.hca = decay.home_court_pts_per100
        self.states: dict[str, TeamState] = {}
        self.mu = cfg.league_ortg_prior
        alpha = 1.0 - 0.5 ** (1.0 / cfg.half_life_games)
        r_typ = (cfg.obs_sd_per_poss * 100.0) ** 2 / TYPICAL_POSS
        self.q_base = r_typ * alpha**2 / (1.0 - alpha)

    def _r_inflation(self, games: int) -> float:
        c = self.cfg
        if games < c.cold_start_games:
            return c.cold_start_r_inflation
        if games < c.stabilization_games:
            frac = (games - c.cold_start_games) / (c.stabilization_games - c.cold_start_games)
            return c.cold_start_r_inflation + frac * (1.0 - c.cold_start_r_inflation)
        return 1.0

    @staticmethod
    def regime(games: int, cfg: KalmanConfig) -> str:
        if games < cfg.cold_start_games:
            return "cold_start"
        if games < cfg.stabilization_games:
            return "stabilization"
        return "dynamic"

    def start_season(self, continuity: dict[str, float] | None = None,
                     rapm_delta: dict[str, tuple[float, float]] | None = None) -> None:
        """Prior de temporada:  θ ← retención·(θ_fin + ΔRAPM).

        ΔRAPM traslada el estado del equipo a su plantilla actual (altas, bajas, regresos de
        lesión); la retención regresa a la media lo no atribuible a la plantilla (suerte,
        edad). La incertidumbre crece con la parte de la rotación que ya no está:
        Σ ← retención²·Σ + prior_var·(1 − retención² + 0.25 + (1 − continuidad))."""
        continuity = continuity or {}
        rapm_delta = rapm_delta or {}
        keep = self.cfg.prior_retention
        for team, st in self.states.items():
            d_off, d_def = rapm_delta.get(team, (0.0, 0.0))
            turnover = 1.0 - continuity.get(team, 1.0)
            st.mean = keep * (st.mean + np.array([d_off, d_def]))
            st.cov = st.cov * keep**2 + np.eye(2) * self.cfg.prior_var * (1 - keep**2 + 0.25 + turnover)
            st.games = 0

    def _state(self, team: str) -> TeamState:
        if team not in self.states:
            self.states[team] = TeamState(cov=np.eye(2) * self.cfg.prior_var)
        return self.states[team]

    def update_game(self, home: str, away: str, home_pts: float, away_pts: float,
                    home_poss: float, away_poss: float, injury_home: bool = False,
                    injury_away: bool = False, r_scale: float = 1.0, update_mu: bool = True) -> None:
        sh, sa = self._state(home), self._state(away)
        # Predicción: ruido de proceso (inflado si falta un titular clave).
        for st, inj in ((sh, injury_home), (sa, injury_away)):
            q = self.q_base * (self.cfg.injury_q_inflation if inj else 1.0)
            st.cov = st.cov + np.eye(2) * q
        m = np.concatenate([sh.mean, sa.mean])
        p = np.zeros((4, 4))
        p[:2, :2], p[2:, 2:] = sh.cov, sa.cov
        y = np.array([100 * home_pts / home_poss - self.mu - self.hca / 2,
                      100 * away_pts / away_poss - self.mu + self.hca / 2])
        base_var = (self.cfg.obs_sd_per_poss * 100.0) ** 2
        r = np.diag([base_var / home_poss * self._r_inflation(sh.games),
                     base_var / away_poss * self._r_inflation(sa.games)]) * r_scale
        s = H_MATRIX @ p @ H_MATRIX.T + r
        k = p @ H_MATRIX.T @ np.linalg.inv(s)
        m_new = m + k @ (y - H_MATRIX @ m)
        p_new = (np.eye(4) - k @ H_MATRIX) @ p
        sh.mean, sa.mean = m_new[:2], m_new[2:]
        sh.cov, sa.cov = p_new[:2, :2], p_new[2:, 2:]
        sh.games += 1
        sa.games += 1
        if update_mu:  # la media de liga sólo aprende de temporada regular
            game_ortg = 100 * (home_pts + away_pts) / (home_poss + away_poss)
            self.mu = (1 - LEAGUE_MU_ALPHA) * self.mu + LEAGUE_MU_ALPHA * game_ortg

    def snapshot(self, team: str) -> dict[str, float]:
        st = self._state(team)
        return {
            "kf_off": float(st.mean[0]), "kf_def": float(st.mean[1]),
            "kf_off_sd": float(np.sqrt(st.cov[0, 0])), "kf_def_sd": float(np.sqrt(st.cov[1, 1])),
            "kf_net": float(st.mean[0] - st.mean[1]), "kf_league_mu": float(self.mu),
            "kf_games": st.games, "kf_regime": self.regime(st.games, self.cfg),
        }


def run_kalman(games: pd.DataFrame, team_sums: pd.DataFrame, cfg: KalmanConfig, decay: DecayConfig,
               injuries: pd.DataFrame | None = None,
               continuity: dict[int, dict[str, float]] | None = None,
               rapm_delta: dict[int, dict[str, tuple[float, float]]] | None = None,
               ) -> tuple[pd.DataFrame, TeamStrengthKalman]:
    """Recorre todos los partidos en orden y devuelve el estado PRE-partido de cada equipo.

    `team_sums` necesita (game_id, team, pts, poss). `injuries` opcional con
    (game_id, team, key_player_out: bool). `continuity` = {season: {team: minutos retenidos}}.
    `rapm_delta` = {season: {team: (Δoff, Δdef)}} (pts/100) por cambios de plantilla.
    """
    kf = TeamStrengthKalman(cfg, decay)
    sums = team_sums.set_index(["game_id", "team"])[["pts", "poss"]]
    inj = set()
    if injuries is not None and not injuries.empty:
        inj = set(map(tuple, injuries.loc[injuries["key_player_out"], ["game_id", "team"]].to_numpy()))
    rows = []
    current_season = None
    for g in games.sort_values(["game_date", "game_id"]).itertuples(index=False):
        if g.season != current_season:
            if current_season is not None:
                kf.start_season((continuity or {}).get(g.season), (rapm_delta or {}).get(g.season))
            current_season = g.season
        for team in (g.home_team, g.away_team):
            rows.append({"season": g.season, "game_date": g.game_date, "game_id": g.game_id, "team": team,
                         **kf.snapshot(team)})
        try:
            h, a = sums.loc[(g.game_id, g.home_team)], sums.loc[(g.game_id, g.away_team)]
        except KeyError:
            log.warning("Kalman: sin sumas para %s; se omite la actualización", g.game_id)
            continue
        playoff = getattr(g, "season_type", 2) == 3
        kf.update_game(g.home_team, g.away_team, h["pts"], a["pts"], max(h["poss"], 1), max(a["poss"], 1),
                       (g.game_id, g.home_team) in inj, (g.game_id, g.away_team) in inj,
                       cfg.playoff_r_inflation if playoff else 1.0, update_mu=not playoff)
    return pd.DataFrame(rows), kf
