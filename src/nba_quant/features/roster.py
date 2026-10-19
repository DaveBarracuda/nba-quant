"""Continuidad de plantilla y ΔRAPM para el prior de temporada (spec 4 §2, cold start).

1. RAPM (Regularized Adjusted Plus-Minus) de la temporada anterior: Ridge sobre pares de
   quintetos (ataque, defensa) con  y = 100·pts/pos − μ,  peso = posesiones,
   10 regresores por fila (+1 a los 5 atacantes en columnas O, +1 a los 5 defensores en
   columnas D). o_rapm > 0 = mejora el ataque; d_rapm > 0 = la defensa PERMITE más
   (misma convención que θ_def del Kalman). Se excluye garbage time.
2. Transición: para cada equipo, valor de su rotación del año pasado vs valor proyectado de la
   plantilla actual (minutos por partido previos de cada jugador, repartidos en 240 minutos;
   los huecos se cubren a nivel de reemplazo). ΔRAPM = nuevo − viejo, en pts/100.
3. Continuidad = fracción de los minutos del año pasado del equipo que siguen en la plantilla.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.linear_model import Ridge

from nba_quant.logging_utils import get_logger

log = get_logger("roster")

RAPM_ALPHA = 3000.0
TEAM_MINUTES = 240.0
LINEUP_SLOTS = 5.0
MAX_PLAYER_MPG = 36.0
REPLACEMENT_QUANTILE = 0.15  # valor de reemplazo = percentil bajo del RAPM de rotación
MIN_ROTATION_MINUTES = 300.0
MAX_ABS_DELTA = 8.0  # pts/100: tope del cambio de plantilla en el prior


@dataclass(frozen=True)
class RosterPriors:
    continuity: dict[str, float]
    rapm_delta: dict[str, tuple[float, float]]
    detail: pd.DataFrame


def compute_rapm(poss: pd.DataFrame, alpha: float = RAPM_ALPHA) -> pd.DataFrame:
    """RAPM ofensivo/defensivo por jugador a partir de la tabla de posesiones con quintetos."""
    p = poss.dropna(subset=["off_lineup", "def_lineup"])
    p = p[~p["is_garbage"].astype(bool)]
    if p.empty:
        return pd.DataFrame(columns=["player_id", "o_rapm", "d_rapm", "poss_on"])
    agg = p.groupby(["off_lineup", "def_lineup"]).agg(pts=("points", "sum"), n=("points", "size")).reset_index()
    mu = 100.0 * agg["pts"].sum() / agg["n"].sum()
    off_players = agg["off_lineup"].str.split("-")
    def_players = agg["def_lineup"].str.split("-")
    players = sorted(set(off_players.explode()) | set(def_players.explode()))
    col = {pid: i for i, pid in enumerate(players)}
    n_p = len(players)
    rows = np.repeat(np.arange(len(agg)), 5)
    off_cols = np.array([col[x] for lu in off_players for x in lu])
    def_cols = np.array([col[x] for lu in def_players for x in lu]) + n_p
    x = sparse.csr_matrix((np.ones(2 * len(rows)), (np.concatenate([rows, rows]), np.concatenate([off_cols, def_cols]))),
                          shape=(len(agg), 2 * n_p))
    y = (100.0 * agg["pts"] / agg["n"] - mu).to_numpy()
    model = Ridge(alpha=alpha, fit_intercept=False).fit(x, y, sample_weight=agg["n"].to_numpy(float))
    poss_on = pd.Series(agg["n"].repeat(5).to_numpy(), index=off_players.explode().to_numpy()).groupby(level=0).sum()
    out = pd.DataFrame({"player_id": players, "o_rapm": model.coef_[:n_p], "d_rapm": model.coef_[n_p:]})
    out["poss_on"] = out["player_id"].map(poss_on).fillna(0)
    log.info("RAPM: %d jugadores, %d pares de quintetos, μ=%.1f", n_p, len(agg), mu)
    return out


def _lineup_value(weights: pd.Series, rapm: pd.DataFrame, repl: tuple[float, float]) -> tuple[float, float]:
    """Σ w_i·RAPM_i con Σ w_i = 5 (los minutos sin cubrir van a nivel de reemplazo)."""
    r = rapm.set_index("player_id").reindex(weights.index)
    o = r["o_rapm"].fillna(repl[0])
    d = r["d_rapm"].fillna(repl[1])
    gap = max(LINEUP_SLOTS - float(weights.sum()), 0.0)
    return float((weights * o).sum() + gap * repl[0]), float((weights * d).sum() + gap * repl[1])


def roster_priors(prev_box: pd.DataFrame, rapm: pd.DataFrame, rosters: pd.DataFrame) -> RosterPriors:
    """Continuidad y ΔRAPM por equipo entre la temporada anterior (`prev_box`, temporada
    regular) y la plantilla actual (`rosters`: team, player_id)."""
    box = prev_box.assign(player_id=prev_box["player_id"].astype(str), minutes=prev_box["minutes"].fillna(0))
    tot_min = box.groupby("player_id")["minutes"].sum()
    rotation = rapm[rapm["player_id"].isin(tot_min[tot_min >= MIN_ROTATION_MINUTES].index)]
    repl = (float(rotation["o_rapm"].quantile(REPLACEMENT_QUANTILE)) if len(rotation) else 0.0,
            float(rotation["d_rapm"].quantile(1 - REPLACEMENT_QUANTILE)) if len(rotation) else 0.0)
    per_team = box.groupby(["team", "player_id"])["minutes"].sum()
    mpg = (tot_min / box.groupby("player_id")["game_id"].nunique()).clip(upper=MAX_PLAYER_MPG)
    roster = rosters.assign(player_id=rosters["player_id"].astype(str))
    rows, continuity, delta = [], {}, {}
    teams_prev = set(per_team.index.get_level_values(0))
    for team, rt in roster.groupby("team"):
        if team not in teams_prev:
            continue
        old = per_team.loc[team]
        old_w = old / old.sum() * LINEUP_SLOTS
        new_mpg = mpg.reindex(rt["player_id"]).dropna().sort_values(ascending=False)
        new_w = new_mpg / TEAM_MINUTES * LINEUP_SLOTS
        if new_w.sum() > LINEUP_SLOTS:  # más minutos proyectados que los disponibles: escalar
            new_w = new_w * LINEUP_SLOTS / new_w.sum()
        o_old, d_old = _lineup_value(old_w, rapm, repl)
        o_new, d_new = _lineup_value(new_w, rapm, repl)
        cont = float(old[old.index.isin(rt["player_id"])].sum() / old.sum())
        d_off = float(np.clip(o_new - o_old, -MAX_ABS_DELTA, MAX_ABS_DELTA))
        d_def = float(np.clip(d_new - d_old, -MAX_ABS_DELTA, MAX_ABS_DELTA))
        continuity[team], delta[team] = cont, (d_off, d_def)
        rows.append({"team": team, "continuity": cont, "d_off": d_off, "d_def": d_def,
                     "d_net": d_off - d_def, "roster_with_history": len(new_mpg), "roster_size": len(rt)})
    detail = pd.DataFrame(rows).sort_values("d_net") if rows else pd.DataFrame()
    log.info("Prior de plantilla: %d equipos, continuidad media %.2f", len(rows),
             detail["continuity"].mean() if len(detail) else float("nan"))
    return RosterPriors(continuity, delta, detail)
