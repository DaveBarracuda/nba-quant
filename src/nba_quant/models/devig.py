"""Desvigado avanzado de cuotas (spec 3 clase 7): Shin, Power y proporcional (referencia).

Shin (1993): el overround surge porque la casa se protege de una fracción z de apostadores
con información privilegiada (insiders). Resolviendo z se obtiene la probabilidad "verdadera":
    p_i = [sqrt(z² + 4(1−z)·π_i²/Π) − z] / (2(1−z)),   Π = Σπ_i,   con Σp_i = 1.
Power: p_i = π_i^k con k tal que Σp_i = 1 (penaliza más a los longshots).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


def american_to_decimal(odds: float) -> float:
    if odds is None or not np.isfinite(odds) or odds == 0:
        raise ValueError(f"Cuota americana inválida: {odds}")
    return 1 + (odds / 100.0 if odds > 0 else 100.0 / -odds)


def implied_probs(decimal_odds: np.ndarray) -> np.ndarray:
    odds = np.asarray(decimal_odds, dtype=float)
    if np.any(odds <= 1.0):
        raise ValueError("Las cuotas decimales deben ser > 1")
    return 1.0 / odds


def devig_proportional(decimal_odds: np.ndarray) -> np.ndarray:
    pi = implied_probs(decimal_odds)
    return pi / pi.sum()


def _shin_probs(pi: np.ndarray, z: float) -> np.ndarray:
    total = pi.sum()
    return (np.sqrt(z**2 + 4 * (1 - z) * pi**2 / total) - z) / (2 * (1 - z))


def devig_shin(decimal_odds: np.ndarray) -> tuple[np.ndarray, float]:
    """Devuelve (probabilidades verdaderas, z = proporción estimada de dinero insider)."""
    pi = implied_probs(decimal_odds)
    if pi.sum() <= 1.0:  # sin margen (o arbitraje): no hay nada que quitar
        return pi / pi.sum(), 0.0
    z = brentq(lambda z: _shin_probs(pi, z).sum() - 1.0, 0.0, 0.999)
    p = _shin_probs(pi, z)
    return p / p.sum(), float(z)


def devig_power(decimal_odds: np.ndarray) -> tuple[np.ndarray, float]:
    """Devuelve (probabilidades, exponente k)."""
    pi = implied_probs(decimal_odds)
    if pi.sum() <= 1.0:
        return pi / pi.sum(), 1.0
    k = brentq(lambda k: (pi**k).sum() - 1.0, 1.0, 50.0)
    p = pi**k
    return p / p.sum(), float(k)
