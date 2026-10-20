"""qSQ / Expected eFG% (spec 1 §D, spec 2 §C).

Modelo logístico de probabilidad de acierto por tiro con:
  ubicación (distancia, distancia², ángulo, esquina), valor (2/3), tipo de acción
  (catch & shoot vs pull-up vs drive vs putback vs poste), transición, reloj tardío y,
  si existe (tracking Second Spectrum / Kaggle), distancia del defensor más cercano.

Modo por defecto `expanding` (point-in-time): el modelo se re-entrena cada `refit_days` días
sólo con tiros de fechas ANTERIORES al bloque que predice, de modo que el xeFG de un partido
nunca usa información de ese día ni posterior (auditado con un test de truncamiento). Antes del
primer bloque con muestra suficiente se usan medias de liga por zona.
El modo `cross_fit` (GroupKFold por partido) queda para análisis retrospectivo: no evita que el
modelo aprenda de partidos futuros de la temporada y NO debe usarse para features de producción.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from nba_quant.logging_utils import get_logger

log = get_logger("shot_quality")

STYLES = ("catch_shoot", "pull_up", "drive", "rim_finish", "putback", "post")
N_FOLDS = 5
MIN_SHOTS_TO_FIT = 400
REFIT_DAYS = 14
# Rellenos constantes (no medianas del dataset, que mezclarían información futura).
FILL_SHOT_DISTANCE_FT = 12.0
FILL_DEFENDER_DISTANCE_FT = 5.0
DEFAULT_FG_BY_ZONE = {"rim": 0.66, "paint": 0.45, "mid": 0.43, "corner3": 0.39, "above_break3": 0.355}


def _design(shots: pd.DataFrame) -> np.ndarray:
    dist = shots["shot_distance"].fillna(FILL_SHOT_DISTANCE_FT).clip(0, 40).to_numpy(float)
    is3 = (shots["shot_value"] == 3).to_numpy(float)
    cols = [
        dist, dist**2, np.log1p(dist), is3, is3 * dist,
        (shots["zone"] == "corner3").to_numpy(float),
        (shots["zone"] == "rim").to_numpy(float),
        shots["angle_deg"].fillna(0).to_numpy(float) / 90.0,
        shots["is_transition"].fillna(False).to_numpy(float),
        shots["is_late_clock"].fillna(False).to_numpy(float),
        shots["is_putback"].fillna(False).to_numpy(float),
    ]
    cols += [(shots["shot_style"] == s).to_numpy(float) for s in STYLES]
    if "defender_distance" in shots.columns and shots["defender_distance"].notna().mean() > 0.5:
        dd = shots["defender_distance"].fillna(FILL_DEFENDER_DISTANCE_FT).clip(0, 15).to_numpy(float)
        cols += [dd, np.minimum(dd, 6.0), is3 * dd]
    return np.column_stack(cols)


class ShotQualityModel:
    """Probabilidad de acierto esperada por tiro y agregados xeFG / xPts."""

    def __init__(self, c: float = 1.0, mode: str = "expanding", refit_days: int = REFIT_DAYS) -> None:
        if mode not in ("expanding", "cross_fit"):
            raise ValueError(f"modo xFG desconocido: {mode}")
        self.c = c
        self.mode = mode
        self.refit_days = refit_days

    def _fit_predict_fold(self, x_tr: np.ndarray, y_tr: np.ndarray, x_te: np.ndarray) -> np.ndarray:
        scaler = StandardScaler().fit(x_tr)
        model = LogisticRegression(C=self.c, max_iter=500)
        model.fit(scaler.transform(x_tr), y_tr)
        return model.predict_proba(scaler.transform(x_te))[:, 1]

    def cross_fit(self, shots: pd.DataFrame) -> pd.Series:
        """P(acierto) fuera de muestra para cada tiro."""
        if len(shots) < MIN_SHOTS_TO_FIT or shots["game_id"].nunique() < N_FOLDS:
            log.warning("Muestra pequeña (%d tiros): xFG por media de zona", len(shots))
            return shots["zone"].map(DEFAULT_FG_BY_ZONE).fillna(0.45)
        x = _design(shots)
        y = shots["made"].astype(int).to_numpy()
        pred = np.empty(len(shots))
        for tr, te in GroupKFold(n_splits=N_FOLDS).split(x, y, groups=shots["game_id"]):
            pred[te] = self._fit_predict_fold(x[tr], y[tr], x[te])
        brier = float(np.mean((pred - y) ** 2))
        log.info("xFG cross-fit: %d tiros, Brier=%.4f (base %.4f)", len(y), brier, float(np.var(y)))
        return pd.Series(pred, index=shots.index)

    def expanding_fit(self, shots: pd.DataFrame) -> pd.Series:
        """P(acierto) point-in-time: bloques de `refit_days` entrenados con tiros previos al bloque."""
        dates = pd.to_datetime(shots["game_date"])
        x = _design(shots)
        y = shots["made"].astype(int).to_numpy()
        pred = shots["zone"].map(DEFAULT_FG_BY_ZONE).fillna(0.45).to_numpy(float, copy=True)  # escribible (CoW)
        start, end = dates.min(), dates.max()
        n_fit = 0
        block = start
        while block <= end:
            nxt = block + pd.Timedelta(days=self.refit_days)
            te = ((dates >= block) & (dates < nxt)).to_numpy()
            tr = (dates < block).to_numpy()
            if te.any() and tr.sum() >= MIN_SHOTS_TO_FIT and shots.loc[tr, "game_id"].nunique() >= N_FOLDS:
                pred[te] = self._fit_predict_fold(x[tr], y[tr], x[te])
                n_fit += 1
            block = nxt
        brier = float(np.mean((pred - y) ** 2))
        log.info("xFG expanding: %d tiros, %d re-ajustes, Brier=%.4f (base %.4f)", len(y), n_fit, brier, float(np.var(y)))
        return pd.Series(pred, index=shots.index)

    def annotate(self, shots: pd.DataFrame) -> pd.DataFrame:
        """Añade xfg (prob), xpts (= xfg·valor) y xefg_w (= xfg·valor/2, escala eFG)."""
        if shots.empty:
            return shots.assign(xfg=np.nan, xpts=np.nan, xefg_w=np.nan)
        use_expanding = self.mode == "expanding" and "game_date" in shots.columns
        xfg = self.expanding_fit(shots) if use_expanding else self.cross_fit(shots)
        value = shots["shot_value"].astype(float)
        return shots.assign(xfg=xfg, xpts=xfg * value, xefg_w=xfg * value / 2.0,
                            efg_w=shots["made"].astype(float) * value / 2.0)
