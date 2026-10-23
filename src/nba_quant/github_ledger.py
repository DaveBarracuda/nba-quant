"""Ledger de los picks del workflow de GitHub *Ejecutar modelo* (sin tracker: líneas de ESPN).

En la corrida se guarda el número del modelo sin mezcla junto a la línea que ESPN publica en ese
momento; el primer pick por partido y mercado es el oficial. La liquidación diaria (`settle.py`)
añade la línea de cierre de ESPN -> movimiento a favor / en contra -> y el resultado.
Vive en ledger/github/ para que el reporte local (que regenera ledger/ desde el tracker) no lo pise.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from nba_quant.ledger import DEFAULT_LEDGER_DIR, write_ledger
from nba_quant.models.devig import american_to_decimal
from nba_quant.simulation.market_moves import first_snapshot_picks, pick_table, summarize

GITHUB_LEDGER_DIR = DEFAULT_LEDGER_DIR / "github"
GITHUB_RENDER = {
    "title": "Ledger de picks — workflow de GitHub",
    "source": "de ESPN (la casa que muestra ESPN)",
    "note": ("Generado por el workflow *Ejecutar modelo* (modelo sin mezcla). El cierre y el movimiento "
             "a favor / en contra se toman de ESPN al liquidar. Ledger con el NBA Odds Tracker: "
             "[../LEDGER.md](../LEDGER.md)"),
}
NO_LINES = pd.DataFrame(columns=["event_id", "market", "ts", "value", "price_a", "price_b"])
ODDS_COLUMNS = {  # mercado -> (línea, precio cara A, precio cara B) en la fila de ESPN
    "spread": ("spread_close", "spread_home_odds_close", "spread_away_odds_close"),
    "total": ("total_close", "over_odds_close", "under_odds_close"),
}


def no_vig_home(home_price: float, away_price: float) -> float:
    if not (np.isfinite(home_price) and np.isfinite(away_price)):
        return np.nan
    ih, ia = 1 / american_to_decimal(home_price), 1 / american_to_decimal(away_price)
    return ih / (ih + ia)


def espn_market_lines(odds: pd.Series | dict) -> dict[str, float]:
    """line_/price_ de cada mercado desde una fila de cuotas de ESPN (spread desde el local)."""
    num = lambda k: float(pd.to_numeric(odds.get(k), errors="coerce"))  # noqa: E731
    out = {}
    for mk, (line, pa, pb) in ODDS_COLUMNS.items():
        out[f"line_{mk}"], out[f"price_{mk}_a"], out[f"price_{mk}_b"] = num(line), num(pa), num(pb)
    out["price_ml_a"], out["price_ml_b"] = num("home_ml_close"), num("away_ml_close")
    out["line_ml"] = no_vig_home(out["price_ml_a"], out["price_ml_b"])
    return out


def build_espn_snapshots(preds: pd.DataFrame, upcoming: pd.DataFrame, snapshot_ts: pd.Timestamp,
                         model_version: str) -> pd.DataFrame:
    """Snapshot en el formato de `market_moves` con el modelo sin mezcla y la línea actual de ESPN."""
    sched = upcoming.drop_duplicates("game_id").set_index("game_id")
    rows = []
    for p in preds.itertuples(index=False):
        if p.game_id not in sched.index:
            continue
        g = sched.loc[p.game_id]
        if pd.Timestamp(g["start_utc"]) <= snapshot_ts:  # ya empezó: la línea de ESPN sería en vivo
            continue
        rows.append({
            "game_id": p.game_id, "snapshot_ts": snapshot_ts.isoformat(), "event_id": p.game_id,
            "commence_time": pd.Timestamp(g["start_utc"]).isoformat(), "home_team": p.home_team,
            "away_team": p.away_team, "model_margin": p.model_margin_raw, "model_total": p.model_total_raw,
            "model_p_home": p.p_home_win_markov, "model_version": model_version, **espn_market_lines(g),
        })
    return pd.DataFrame(rows)


def record_picks(snapshots: pd.DataFrame, ledger_dir: Path = GITHUB_LEDGER_DIR) -> pd.DataFrame:
    """Añade los picks nuevos (primer pick por partido-mercado) y regenera el ledger de GitHub."""
    new = pick_table(snapshots, NO_LINES, pd.DataFrame(columns=["game_id", "home_score", "away_score"]))
    path = ledger_dir / "picks.csv"
    old = pd.read_csv(path, dtype={"game_id": str}) if path.exists() else pd.DataFrame()
    picks = first_snapshot_picks(pd.concat([old, new], ignore_index=True)) if len(new) or len(old) else new
    write_ledger(picks, summarize(picks), ledger_dir, **GITHUB_RENDER)
    return picks
