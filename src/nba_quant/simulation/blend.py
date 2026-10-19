"""Mezcla point-in-time modelo + línea de cierre (ML, spread, total).

El backtest muestra que el cierre es más preciso que el modelo puro, pero ambos tienen
información distinta. Para cada fecha, con partidos ESTRICTAMENTE anteriores que tienen cuota:
    margen_mezcla = w_m · margen_modelo + (1 − w_m) · (−spread_local)
    total_mezcla  = w_t · total_modelo  + (1 − w_t) · total_mercado
w = argmin Σ (real − mezcla)² (mínimos cuadrados cerrados, con decaimiento exponencial),
encogido hacia W_PRIOR con W_PRIOR_GAMES pseudo-partidos y recortado a [0, 1]. Las
probabilidades de ML/spread/total salen de desplazar la distribución simulada a la media
mezclada (la forma, colas y números clave siguen siendo los del motor de Markov).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import norm

from nba_quant.models.markov import SimulationResult

W_PRIOR = 0.30
W_PRIOR_GAMES = 150.0
HALF_LIFE_GAMES = 400.0
SIGMA_MARGIN_PRIOR = 12.5
SIGMA_TOTAL_PRIOR = 18.0
SIGMA_PRIOR_GAMES = 100.0


@dataclass(frozen=True)
class BlendState:
    w_margin: float
    w_total: float
    sigma_margin: float
    sigma_total: float
    n_games: int


def _weights(n: int) -> np.ndarray:
    return 0.5 ** (np.arange(n)[::-1] / HALF_LIFE_GAMES)


def _fit_w(model: np.ndarray, market: np.ndarray, actual: np.ndarray, w: np.ndarray) -> tuple[float, float]:
    """Peso del modelo (encogido) y sd del residuo de la mezcla."""
    a, b = model - market, actual - market
    denom = float((w * a * a).sum())
    w_hat = float((w * a * b).sum() / denom) if denom > 0 else W_PRIOR
    n_eff = float(w.sum())
    w_m = float(np.clip((n_eff * w_hat + W_PRIOR_GAMES * W_PRIOR) / (n_eff + W_PRIOR_GAMES), 0.0, 1.0))
    resid = actual - (w_m * model + (1 - w_m) * market)
    return w_m, float(np.sqrt((w * resid**2).sum() / n_eff))


class MarketBlender:
    """`preds`: game_date, exp_margin, exp_total (modelo, local), market_spread (local),
    market_total, actual_margin, actual_total."""

    def __init__(self, preds: pd.DataFrame) -> None:
        self.p = preds.assign(game_date=pd.to_datetime(preds["game_date"])).sort_values("game_date")
        self._cache: dict[pd.Timestamp, BlendState] = {}

    def state(self, before: pd.Timestamp | None = None) -> BlendState:
        key = pd.Timestamp(before) if before is not None else pd.Timestamp.max
        if key in self._cache:
            return self._cache[key]
        past = self.p if before is None else self.p[self.p["game_date"] < key]
        sm, st, wm, wt, n = SIGMA_MARGIN_PRIOR, SIGMA_TOTAL_PRIOR, W_PRIOR, W_PRIOR, 0
        pm = past.dropna(subset=["market_spread", "actual_margin", "exp_margin"])
        if len(pm):
            wm, s = _fit_w(pm["exp_margin"].to_numpy(), -pm["market_spread"].to_numpy(),
                           pm["actual_margin"].to_numpy(), _weights(len(pm)))
            sm = (len(pm) * s + SIGMA_PRIOR_GAMES * SIGMA_MARGIN_PRIOR) / (len(pm) + SIGMA_PRIOR_GAMES)
            n = len(pm)
        pt = past.dropna(subset=["market_total", "actual_total", "exp_total"])
        if len(pt):
            wt, s = _fit_w(pt["exp_total"].to_numpy(), pt["market_total"].to_numpy(),
                           pt["actual_total"].to_numpy(), _weights(len(pt)))
            st = (len(pt) * s + SIGMA_PRIOR_GAMES * SIGMA_TOTAL_PRIOR) / (len(pt) + SIGMA_PRIOR_GAMES)
        out = BlendState(wm, wt, float(sm), float(st), n)
        self._cache[key] = out
        return out

    @staticmethod
    def blend(state: BlendState, model_margin: float, model_total: float, market_spread: float | None,
              market_total: float | None) -> tuple[float, float]:
        m = model_margin if market_spread is None or not np.isfinite(market_spread) else (
            state.w_margin * model_margin + (1 - state.w_margin) * -market_spread)
        t = model_total if market_total is None or not np.isfinite(market_total) else (
            state.w_total * model_total + (1 - state.w_total) * market_total)
        return float(m), float(t)

    def evaluate(self, preds: pd.DataFrame | None = None) -> pd.DataFrame:
        """Mezcla point-in-time para cada fila (estado con partidos anteriores a su fecha) y
        probabilidades normales de victoria local, cover local y over."""
        df = (preds if preds is not None else self.p).copy()
        df["game_date"] = pd.to_datetime(df["game_date"])
        rows = []
        for r in df.itertuples(index=False):
            st = self.state(r.game_date)
            m, t = self.blend(st, r.exp_margin, r.exp_total, r.market_spread, r.market_total)
            rows.append({"blend_margin": m, "blend_total": t, "w_margin": st.w_margin, "w_total": st.w_total,
                         "p_home_blend": float(norm.sf(0, loc=m, scale=st.sigma_margin)),
                         "p_cover_blend": float(norm.sf(-r.market_spread, loc=m, scale=st.sigma_margin))
                         if np.isfinite(r.market_spread) else np.nan,
                         "p_over_blend": float(norm.sf(r.market_total, loc=t, scale=st.sigma_total))
                         if np.isfinite(r.market_total) else np.nan})
        return pd.concat([df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)


def shift_simulation(sim: SimulationResult, d_margin: float, d_total: float,
                     rng: np.random.Generator) -> SimulationResult:
    """Desplaza margen y total medios con redondeo estocástico (insesgado en enteros)."""

    def rround(x: float, size: int) -> np.ndarray:
        base = np.floor(x)
        return (base + (rng.random(size) < (x - base))).astype(np.int32)

    n = sim.home_pts.size
    dh = rround((d_total + d_margin) / 2.0, n)
    da = rround((d_total - d_margin) / 2.0, n)
    return SimulationResult((sim.home_pts + dh).astype(np.int32), (sim.away_pts + da).astype(np.int32),
                            sim.overtime, dict(sim.meta))
