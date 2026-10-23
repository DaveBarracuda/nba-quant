"""Liquida los ledgers sin el lake ni el tracker (corre en GitHub Actions).

Lee picks.csv de cada ledger, consulta en ESPN el marcador final de los partidos pendientes ya
jugados, califica cada pick contra la línea guardada al momento del pick y regenera
LEDGER.md/summary.csv.
  - ledger/: la categoría de movimiento (a favor / en contra) ya viene del reporte local, que es
    el único que ve las líneas del tracker.
  - ledger/github/: picks del workflow *Ejecutar modelo*; el cierre se toma de ESPN (pickcenter, o
    la API core si el resumen ya no lo trae) y con él se clasifica el movimiento.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd

from nba_quant.config import DEFAULT_CONFIG
from nba_quant.github_ledger import GITHUB_LEDGER_DIR, GITHUB_RENDER, espn_market_lines
from nba_quant.ingestion.espn import CORE_ODDS_URL, SUMMARY_URL, parse_core_odds, parse_odds
from nba_quant.ingestion.http import HttpError, SyncHttpClient
from nba_quant.ledger import DEFAULT_LEDGER_DIR, write_ledger
from nba_quant.logging_utils import get_logger
from nba_quant.simulation.market_moves import MOVE_EPS, _grade, _market_move, _profit, summarize
from nba_quant.teams import normalize_abbr

log = get_logger("settle")
RESULTS_GRACE = pd.Timedelta(hours=4)  # un partido se da por terminado 4 h después del salto
ESPN_MIN_INTERVAL_S = 0.5
FinalScore = tuple[int, int]  # (local, visitante)
CloseLines = dict[str, float]  # mercado -> línea de cierre (spread del local, total, P ML local sin vig)


def score_from_summary(summary: dict) -> FinalScore | None:
    """Marcador final (local, visitante) o None si el partido no ha terminado."""
    comp = summary["header"]["competitions"][0]
    if not ((comp.get("status") or {}).get("type") or {}).get("completed"):
        return None
    by_side = {c["homeAway"]: int(c.get("score") or 0) for c in comp["competitors"]}
    return by_side["home"], by_side["away"]


def espn_final_score(client: SyncHttpClient, game_id: str) -> FinalScore | None:
    return score_from_summary(client.get_json(SUMMARY_URL, {"event": game_id}, use_cache=False))


def espn_closing_lines(client: SyncHttpClient, game_id: str, summary: dict) -> CloseLines:
    """Cierre pre-partido de ESPN: pickcenter del resumen o, si ya no está, la API core (sin 'Live')."""
    odds = [o for o in parse_odds(game_id, summary) if "live" not in str(o["provider"]).lower()]
    if not odds:
        payload = client.get_json(CORE_ODDS_URL.format(gid=game_id), use_cache=False)
        odds = parse_core_odds(game_id, payload)
    if not odds:
        return {}
    lines = espn_market_lines(odds[0])
    return {mk: lines[f"line_{mk}"] for mk in ("spread", "total", "ml") if np.isfinite(lines[f"line_{mk}"])}


def _pick_is_side_a(market: str, pick: str, matchup: str) -> bool:
    """Cara A = local (spread/ML) u Over (total), igual que en `market_moves`."""
    if market == "total":
        return pick.startswith("Over")
    home = normalize_abbr(matchup.split(" @ ")[1])
    return pick.split(" ")[0] == home


def _apply_close(out: pd.DataFrame, i: int, mk: str, side_a: bool, close: float) -> None:
    """Rellena cierre, CLV y categoría de movimiento de un pick que aún no los tiene."""
    clv = _market_move(mk, float(out.at[i, "line_pick"]), close) * (1 if side_a else -1)
    edge = abs(float(out.at[i, "edge"]))
    out.at[i, "line_close"], out.at[i, "clv"] = close, clv
    out.at[i, "gap_closed"] = clv / edge if edge else np.nan
    eps = MOVE_EPS[mk]
    out.at[i, "move_category"] = "a favor" if clv > eps else "en contra" if clv < -eps else "sin movimiento"


def settle_picks(picks: pd.DataFrame, fetch_score: Callable[[str], FinalScore | None],
                 now: pd.Timestamp,
                 fetch_close: Callable[[str], CloseLines] | None = None) -> tuple[pd.DataFrame, int]:
    """Devuelve (picks con resultado y unidades, número de picks liquidados ahora). Con
    `fetch_close`, los picks sin cierre ("pendiente") reciben además el cierre y el movimiento."""
    out = picks.copy()
    out["move_category"] = out["move_category"].astype(object)
    for col in ("line_close", "clv", "gap_closed", "result", "units"):
        out[col] = out[col].astype(float)
    commence = pd.to_datetime(out["commence_time"], utc=True)
    due = out["result"].isna() & (commence < now - RESULTS_GRACE)
    scores: dict[str, FinalScore | None] = {}
    closes: dict[str, CloseLines] = {}
    for gid in out.loc[due, "game_id"].astype(str).unique():
        try:
            scores[gid] = fetch_score(gid)
            if fetch_close is not None and scores[gid] is not None:
                closes[gid] = fetch_close(gid)
        except (HttpError, KeyError, ValueError) as exc:
            log.error("Marcador/cierre de %s no disponible: %s", gid, exc)
    settled = 0
    for i in out.index[due]:
        gid = str(out.at[i, "game_id"])
        score = scores.get(gid)
        if score is None:
            continue
        home, away = score
        mk = out.at[i, "market"]
        side_a = _pick_is_side_a(mk, out.at[i, "pick"], out.at[i, "matchup"])
        if out.at[i, "move_category"] == "pendiente" and mk in closes.get(gid, {}):
            _apply_close(out, i, mk, side_a, closes[gid][mk])
        result = _grade(mk, side_a, float(out.at[i, "line_pick"]), float(home - away), float(home + away))
        out.at[i, "result"] = result
        out.at[i, "units"] = _profit(result, float(out.at[i, "price"]))
        settled += 1
    return out, settled


def _settle_dir(client: SyncHttpClient, ledger_dir: Path, with_close: bool,
                render: dict[str, str]) -> int:
    path = ledger_dir / "picks.csv"
    if not path.exists():
        log.info("No existe %s: aún no hay picks publicados", path)
        return 0
    picks = pd.read_csv(path, dtype={"game_id": str})
    if picks.empty:
        return 0
    summaries: dict[str, dict] = {}

    def summary(gid: str) -> dict:
        if gid not in summaries:
            summaries[gid] = client.get_json(SUMMARY_URL, {"event": gid}, use_cache=False)
        return summaries[gid]

    settled, n = settle_picks(picks, lambda gid: score_from_summary(summary(gid)), pd.Timestamp.now(tz="UTC"),
                              (lambda gid: espn_closing_lines(client, gid, summary(gid))) if with_close else None)
    if n:  # sin liquidaciones no se reescribe nada: evita commits vacíos de sólo fecha/formato
        write_ledger(settled, summarize(settled), ledger_dir, **render)
    return n


def run_settle(ledger_dir: Path = DEFAULT_LEDGER_DIR, github_dir: Path = GITHUB_LEDGER_DIR) -> int:
    """Liquida el ledger del tracker y el de GitHub; devuelve el total de picks liquidados."""
    client = SyncHttpClient(DEFAULT_CONFIG.http, ESPN_MIN_INTERVAL_S)
    return (_settle_dir(client, ledger_dir, with_close=False, render={})
            + _settle_dir(client, github_dir, with_close=True, render=GITHUB_RENDER))
