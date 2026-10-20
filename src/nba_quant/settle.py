"""Liquida el ledger sin el lake ni el tracker (corre en GitHub Actions).

Lee ledger/picks.csv, consulta en ESPN el marcador final de los partidos pendientes ya jugados,
califica cada pick contra la línea guardada al momento del pick y regenera LEDGER.md/summary.csv.
La categoría de movimiento (a favor / en contra) viene ya calculada por el reporte local, que es
el único que ve las líneas del tracker.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pandas as pd

from nba_quant.config import DEFAULT_CONFIG
from nba_quant.ingestion.espn import SUMMARY_URL
from nba_quant.ingestion.http import HttpError, SyncHttpClient
from nba_quant.ledger import DEFAULT_LEDGER_DIR, write_ledger
from nba_quant.logging_utils import get_logger
from nba_quant.simulation.market_moves import _grade, _profit, summarize
from nba_quant.teams import normalize_abbr

log = get_logger("settle")
RESULTS_GRACE = pd.Timedelta(hours=4)  # un partido se da por terminado 4 h después del salto
ESPN_MIN_INTERVAL_S = 0.5
FinalScore = tuple[int, int]  # (local, visitante)


def espn_final_score(client: SyncHttpClient, game_id: str) -> FinalScore | None:
    """Marcador final (local, visitante) o None si el partido no ha terminado."""
    summary = client.get_json(SUMMARY_URL, {"event": game_id}, use_cache=False)
    comp = summary["header"]["competitions"][0]
    if not ((comp.get("status") or {}).get("type") or {}).get("completed"):
        return None
    by_side = {c["homeAway"]: int(c.get("score") or 0) for c in comp["competitors"]}
    return by_side["home"], by_side["away"]


def _pick_is_side_a(market: str, pick: str, matchup: str) -> bool:
    """Cara A = local (spread/ML) u Over (total), igual que en `market_moves`."""
    if market == "total":
        return pick.startswith("Over")
    home = normalize_abbr(matchup.split(" @ ")[1])
    return pick.split(" ")[0] == home


def settle_picks(picks: pd.DataFrame, fetch_score: Callable[[str], FinalScore | None],
                 now: pd.Timestamp) -> tuple[pd.DataFrame, int]:
    """Devuelve (picks con resultado y unidades, número de picks liquidados ahora)."""
    out = picks.copy()
    commence = pd.to_datetime(out["commence_time"], utc=True)
    due = out["result"].isna() & (commence < now - RESULTS_GRACE)
    scores: dict[str, FinalScore | None] = {}
    for gid in out.loc[due, "game_id"].astype(str).unique():
        try:
            scores[gid] = fetch_score(gid)
        except (HttpError, KeyError, ValueError) as exc:
            log.error("Marcador de %s no disponible: %s", gid, exc)
    settled = 0
    for i in out.index[due]:
        score = scores.get(str(out.at[i, "game_id"]))
        if score is None:
            continue
        home, away = score
        mk = out.at[i, "market"]
        side_a = _pick_is_side_a(mk, out.at[i, "pick"], out.at[i, "matchup"])
        result = _grade(mk, side_a, float(out.at[i, "line_pick"]), float(home - away), float(home + away))
        out.at[i, "result"] = result
        out.at[i, "units"] = _profit(result, float(out.at[i, "price"]))
        settled += 1
    return out, settled


def run_settle(ledger_dir: Path = DEFAULT_LEDGER_DIR) -> int:
    path = ledger_dir / "picks.csv"
    if not path.exists():
        log.error("No existe %s: el reporte local aún no ha publicado picks", path)
        return 0
    picks = pd.read_csv(path, dtype={"game_id": str})
    if picks.empty:
        return 0
    client = SyncHttpClient(DEFAULT_CONFIG.http, ESPN_MIN_INTERVAL_S)
    settled, n = settle_picks(picks, lambda gid: espn_final_score(client, gid), pd.Timestamp.now(tz="UTC"))
    if n:  # sin liquidaciones no se reescribe nada: evita commits vacíos de sólo fecha/formato
        write_ledger(settled, summarize(settled), ledger_dir)
    return n
