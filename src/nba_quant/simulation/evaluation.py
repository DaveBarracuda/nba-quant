"""Métricas de backtest: resumen de la mezcla de escenarios, probabilidades de mercado
desvigadas y tabla de métricas (MAE, Brier, log-loss de spread, % ATS)."""

from __future__ import annotations

import zlib

import numpy as np
import pandas as pd

from nba_quant.models.devig import american_to_decimal, devig_shin
from nba_quant.models.markov import SimulationResult
from nba_quant.simulation.monte_carlo import STATES3

PROB_CLIP = 1e-4


def _finite(v: object) -> bool:
    try:
        return v is not None and bool(np.isfinite(float(v)))
    except (TypeError, ValueError):
        return False


def game_seed(base_seed: int, game_id: str) -> int:
    """Semilla estable por partido (independiente del orden y del reparto entre procesos), para
    que todas las configuraciones de un partido usen los mismos números aleatorios."""
    return base_seed + 100 * (zlib.crc32(str(game_id).encode()) % 1_000_000)


def mixture_summary(grid: dict[tuple[str, str], SimulationResult], weights: tuple[float, float, float],
                    spread_home: float | None) -> dict[str, float]:
    """Media ponderada (pesos Mejor/Normal/Peor por equipo) de P(gana local), P(local cubre | no
    push), E[margen] y E[total] sobre la rejilla 3×3."""
    w = dict(zip(STATES3, weights))
    p_win = exp_margin = exp_total = cover = no_push = 0.0
    for (hs, as_), sim in grid.items():
        ww = w[hs] * w[as_]
        p_win += ww * sim.home_win_prob()
        exp_margin += ww * float(sim.margin.mean())
        exp_total += ww * float(sim.total.mean())
        if spread_home is not None:
            c, push = sim.cover_prob(spread_home)
            cover += ww * c
            no_push += ww * (1 - push)
    p_cover = cover / no_push if spread_home is not None and no_push > 0 else np.nan
    return {"p_home": p_win, "p_home_cover": p_cover, "exp_margin": exp_margin, "exp_total": exp_total}


def single_summary(sim: SimulationResult, spread_home: float | None) -> dict[str, float]:
    return mixture_summary({("normal", "normal"): sim}, (0.0, 1.0, 0.0), spread_home)


def market_probs(odds: pd.Series | None) -> dict[str, float]:
    """P(gana local) y P(local cubre) del cierre desvigados con Shin (NaN si faltan cuotas)."""
    out = {"market_spread": np.nan, "market_total": np.nan, "p_home_market": np.nan, "p_cover_market": np.nan}
    if odds is None:
        return out
    out["market_spread"] = float(odds["spread_close"]) if _finite(odds.get("spread_close")) else np.nan
    out["market_total"] = float(odds["total_close"]) if _finite(odds.get("total_close")) else np.nan
    for col, (a, b) in (("p_home_market", ("home_ml_close", "away_ml_close")),
                        ("p_cover_market", ("spread_home_odds_close", "spread_away_odds_close"))):
        if _finite(odds.get(a)) and _finite(odds.get(b)):
            try:
                out[col] = float(devig_shin(np.array([american_to_decimal(odds[a]),
                                                      american_to_decimal(odds[b])]))[0][0])
            except ValueError:
                pass
    return out


def _log_loss(p: pd.Series, y: pd.Series) -> float:
    p = p.clip(PROB_CLIP, 1 - PROB_CLIP)
    return float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean())


def score(bt: pd.DataFrame, p_home: str = "p_home", p_cover: str = "p_home_cover",
          margin: str = "exp_margin", total: str = "exp_total") -> dict[str, float]:
    """Métricas de una fuente de predicción. Las columnas pueden ser del modelo o del mercado
    (margin = −spread de cierre). Spread/ATS excluye pushes y partidos sin línea."""
    y_win = (bt["actual_margin"] > 0).astype(float)
    ats = bt["actual_margin"] + bt["market_spread"]
    s = bt[ats.notna() & (ats != 0) & bt[p_cover].notna()]
    y_cov = (s["actual_margin"] + s["market_spread"] > 0).astype(float)
    pick_home = s[p_cover] > 0.5
    return {
        "n": int(len(bt)),
        "mae_margin": float((bt[margin] - bt["actual_margin"]).abs().mean()),
        "mae_total": float((bt[total] - bt["actual_total"]).abs().mean()),
        "brier": float(((bt[p_home] - y_win) ** 2).mean()),
        "log_loss_win": _log_loss(bt[p_home], y_win),
        "n_spread": int(len(s)),
        "log_loss_spread": _log_loss(s[p_cover], y_cov) if len(s) else np.nan,
        "brier_spread": float(((s[p_cover] - y_cov) ** 2).mean()) if len(s) else np.nan,
        "ats_hit_rate": float((pick_home == (y_cov == 1)).mean()) if len(s) else np.nan,
    }


def score_market(bt: pd.DataFrame) -> dict[str, float]:
    m = bt.assign(_mkt_margin=-bt["market_spread"])
    m = m[m["_mkt_margin"].notna() & m["p_home_market"].notna() & m["market_total"].notna()]
    return score(m, "p_home_market", "p_cover_market", "_mkt_margin", "market_total")
