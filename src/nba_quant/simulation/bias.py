"""Calibrador de sesgos point-in-time (ventaja de campo y nivel de anotación).

El backtest 2025-26 mostró sesgos sistemáticos que el rating base no corrige:
  * margen local sobreestimado ~0.9 pts (ventaja de campo fija de 2.4 pts/100),
  * total en playoffs sobreestimado ~8 pts (en playoffs se anota ~6.5% menos),
  * derivas mensuales del nivel de anotación de la liga.
Para cada fecha se estiman, con partidos ESTRICTAMENTE anteriores y decaimiento exponencial:
  hca      = residuo local medio (pts/100) encogido hacia el prior de configuración,
  f_reg    = Σ total real / Σ total esperado en temporada regular, encogido hacia 1,
  f_po     = mismo cociente en playoffs (relativo a f_reg), encogido hacia PLAYOFF_TOTAL_PRIOR.
`f_*` se aplica como multiplicador del ritmo (φ_context): escala posesiones y por tanto el total.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from nba_quant.logging_utils import get_logger

log = get_logger("bias")

HCA_HALF_LIFE_GAMES = 300.0
HCA_PRIOR_GAMES = 150.0
TOTAL_HALF_LIFE_GAMES = 200.0
TOTAL_PRIOR_GAMES = 100.0
PLAYOFF_TOTAL_PRIOR = 0.95  # en playoffs se anota ~4-7% menos que en temporada regular
PLAYOFF_PRIOR_GAMES = 30.0
FACTOR_BOUNDS = (0.85, 1.10)
PLAYOFF_SEASON_TYPE = 3


@dataclass(frozen=True)
class BiasState:
    hca_per100: float
    total_factor_regular: float
    total_factor_playoff: float
    n_games: int

    def total_factor(self, season_type: object) -> float:
        return self.total_factor_playoff if season_type == PLAYOFF_SEASON_TYPE else self.total_factor_regular


def _decayed_weights(n: int, half_life: float) -> np.ndarray:
    age = np.arange(n)[::-1].astype(float)  # 0 = el partido más reciente
    return 0.5 ** (age / half_life)


def game_table(features: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """Una fila por partido jugado con predicción analítica SIN corregir (neutral) y resultado."""
    f = features[features["target_margin"].notna() & features["target_poss"].notna()]
    h = f[f["is_home"] == 1].set_index("game_id")
    a = f[f["is_home"] == 0].set_index("game_id")
    idx = h.index.intersection(a.index)
    h, a = h.loc[idx], a.loc[idx]
    mu = h["kf_league_mu"]
    tf_h, tf_a = h["trans_freq"].clip(lower=1e-3), a["trans_freq"].clip(lower=1e-3)
    w_h = tf_h / (tf_h + tf_a)
    lam = 1.0 / (w_h / h["pace"] + (1 - w_h) / a["pace"])
    neutral = (h["strength_off"] + a["strength_def"]) - (a["strength_off"] + h["strength_def"])
    exp_total = lam * (2 * mu + h["strength_off"] + a["strength_def"] + a["strength_off"] + h["strength_def"]) / 100
    st = games.set_index("game_id")["season_type"] if "season_type" in games.columns else pd.Series(dtype=float)
    out = pd.DataFrame({
        "game_date": pd.to_datetime(h["game_date"]),
        "season_type": st.reindex(idx).fillna(2).to_numpy(),
        "hca_obs": 100 * h["target_margin"] / h["target_poss"] - neutral,
        "exp_total": exp_total, "actual_total": h["target_total"],
    }, index=idx)
    return out.replace([np.inf, -np.inf], np.nan).dropna().sort_values("game_date")


class BiasCalibrator:
    def __init__(self, games_tbl: pd.DataFrame, hca_prior: float) -> None:
        self.t = games_tbl
        self.hca_prior = hca_prior
        self._cache: dict[pd.Timestamp, BiasState] = {}

    @classmethod
    def from_features(cls, features: pd.DataFrame, games: pd.DataFrame, hca_prior: float) -> "BiasCalibrator":
        return cls(game_table(features, games), hca_prior)

    @staticmethod
    def _ratio(past: pd.DataFrame, prior: float, prior_games: float) -> float:
        if past.empty:
            return prior
        w = _decayed_weights(len(past), TOTAL_HALF_LIFE_GAMES)
        ratio = float((w * past["actual_total"]).sum() / (w * past["exp_total"]).sum())
        shrink = w.sum() / (w.sum() + prior_games)
        return float(np.clip(shrink * ratio + (1 - shrink) * prior, *FACTOR_BOUNDS))

    def state(self, before: pd.Timestamp | None = None) -> BiasState:
        """Estado con partidos de fecha < `before` (None = toda la historia)."""
        key = pd.Timestamp(before) if before is not None else pd.Timestamp.max
        if key in self._cache:
            return self._cache[key]
        past = self.t if before is None else self.t[self.t["game_date"] < key]
        if past.empty:
            st = BiasState(self.hca_prior, 1.0, PLAYOFF_TOTAL_PRIOR, 0)
        else:
            w = _decayed_weights(len(past), HCA_HALF_LIFE_GAMES)
            hca = float(((w * past["hca_obs"]).sum() + HCA_PRIOR_GAMES * self.hca_prior) / (w.sum() + HCA_PRIOR_GAMES))
            reg = self._ratio(past[past["season_type"] != PLAYOFF_SEASON_TYPE], 1.0, TOTAL_PRIOR_GAMES)
            po_games = past[past["season_type"] == PLAYOFF_SEASON_TYPE]
            po_rel = self._ratio(po_games.assign(exp_total=po_games["exp_total"] * reg), PLAYOFF_TOTAL_PRIOR,
                                 PLAYOFF_PRIOR_GAMES)
            st = BiasState(hca, reg, float(np.clip(reg * po_rel, *FACTOR_BOUNDS)), len(past))
        self._cache[key] = st
        return st
