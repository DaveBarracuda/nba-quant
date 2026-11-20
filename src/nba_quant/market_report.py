"""Modelo vs mercado: pick por partido y mercado, movimiento de la línea desde la primera lectura
hasta ahora (a favor / en contra / sin movimiento), P del modelo vs P sin vig del mercado, EV al
precio actual y si todavía queda valor. Lo imprime `simulate` y el workflow lo publica en el resumen
de la corrida.

Fuente: DraftKings del NBA Odds Tracker (primera lectura -> última, con alertas RLM/STEAM y % de
tickets del público). Si el partido no está en el tracker, apertura -> línea actual de ESPN.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
import pandas as pd

from nba_quant.github_ledger import espn_market_lines, no_vig_home, tracker_events
from nba_quant.integrations.odds_tracker import TrackerData
from nba_quant.models.devig import american_to_decimal
from nba_quant.simulation.market_moves import MOVE_EPS, _market_move, _public_on_pick

DISPLAY_ABBR = {"NY": "NYK", "SA": "SAS", "GS": "GSW", "NO": "NOP", "UTAH": "UTA", "WSH": "WAS"}
LOCAL_TZ = "America/Mexico_City"
MIN_EDGE_PP = 1.0  # por debajo, aunque el EV sea positivo, se marca "sin valor"
GROUPS = (("a favor", "▲ El mercado va a favor del modelo"), ("en contra", "▼ El mercado va en contra del modelo"),
          ("sin movimiento", "= Sin movimiento"), ("sin dato", "Sin línea de apertura"))
COLUMNS = ["Hora", "Partido", "Mercado", "Pick", "Línea (apertura → actual)", "Modelo", "P modelo vs mercado",
           "Edge", "EV", "Valor", "Alertas", "% público", "Fuente"]
MARKET_NAMES = {"spread": "Spread", "total": "Total", "ml": "ML"}
TRACKER_MARKETS = {"spread": "spread", "total": "total", "ml": "ml"}
LEGEND = ("Hora de CDMX · línea desde el lado del pick (ML: probabilidad sin vig del equipo) · movimiento = "
          "primera lectura del tracker (DK) o apertura de ESPN → línea actual; umbral 0.25 pts (spread/total) "
          "y 0.5 pp (ML) · Edge = P modelo − P mercado sin vig · EV por unidad al precio actual · ⚠ = a la "
          "línea actual ya no queda valor (EV ≤ 0 o edge < 1 pp) · Alertas del tracker sin NOISE · % público = "
          "tickets en el lado del pick (Action Network).")


# Lectura de totales (reglas acordadas a partir del historial de picks): la mejor franja es 3–8 pts de
# ventaja; 8+ históricamente rinde peor (stake reducido); sin movimiento → stake chico; en contra → fuera.
EDGE_MIN_PTS = 3.0
EDGE_MAX_PTS = 8.0
SHARP_ALERTS = frozenset({"STEAM", "RLM"})
TIER_ORDER = {"🟢": 0, "🟡": 1, "⏳": 2, "❌": 3}
TOTALS_COLUMNS = ["Veredicto", "Hora", "Partido", "Pick", "Modelo", "Ventaja", "Línea (apertura → actual)",
                  "Alertas", "Motivo"]
TOTALS_LEGEND = ("Reglas: mercado a favor del modelo con ventaja de 3–8 pts → normal (GRADUAL = prioridad) · "
                 "ventaja 8+ → reducido · ventaja < 3 → mínimo · sin movimiento → chico · en contra → fuera "
                 "(sobre todo con STEAM/RLM) · ⚠ sin valor a la línea actual → fuera. Ventaja = puntos entre "
                 "el total del modelo y la línea, desde el lado del pick.")


class TotalVerdict(NamedTuple):
    tier: str
    stake: str
    reason: str


def classify_total(category: str, edge_pts: float, value_left: bool, alerts: str) -> TotalVerdict:
    """Veredicto de un total según dirección del mercado, alertas del tracker y ventaja en puntos."""
    kinds = set(alerts.split(",")) if alerts and alerts != "—" else set()
    if not value_left:
        return TotalVerdict("❌", "Fuera", "sin valor a la línea actual")
    if category == "en contra":
        sharp = ",".join(sorted(kinds & SHARP_ALERTS))
        return TotalVerdict("❌", "Fuera", f"en contra con STEAM/RLM ({sharp})" if sharp
                            else "mercado en contra del modelo")
    if category == "sin dato":
        return TotalVerdict("⏳", "Revisar", "sin línea de apertura: revisar el movimiento a mano")
    if edge_pts < EDGE_MIN_PTS:
        return TotalVerdict("🟡", "Mínimo", f"ventaja menor a {EDGE_MIN_PTS:g} pts")
    if category == "sin movimiento":
        extra = f"; ventaja {EDGE_MAX_PTS:g}+" if edge_pts >= EDGE_MAX_PTS else ""
        return TotalVerdict("🟡", "Chico", f"sin movimiento neto{extra}")
    if edge_pts >= EDGE_MAX_PTS:
        return TotalVerdict("🟡", "Reducido", f"a favor, pero ventaja {EDGE_MAX_PTS:g}+ (históricamente peor)")
    note = " (GRADUAL: prioridad)" if "GRADUAL" in kinds else ""
    return TotalVerdict("🟢", "Normal", f"a favor del modelo, franja {EDGE_MIN_PTS:g}–{EDGE_MAX_PTS:g}{note}")


def totals_read(report: pd.DataFrame) -> pd.DataFrame:
    """Una fila por total con su veredicto, ordenada de mejor a peor y por hora."""
    if report.empty or "model_total" not in report:
        return pd.DataFrame(columns=TOTALS_COLUMNS)
    rows = []
    for r in report[report["Mercado"] == "Total"].to_dict("records"):
        edge = (r["model_total"] - r["line"]) * (1 if r["side_a"] else -1)
        v = classify_total(r["category"], edge, bool(r["value_left"]), r["Alertas"])
        rows.append({"_order": TIER_ORDER[v.tier], "_tip": r["tip"], "Veredicto": f"{v.tier} {v.stake}",
                     "Hora": r["Hora"], "Partido": r["Partido"], "Pick": r["Pick"],
                     "Modelo": f"{r['model_total']:.1f}", "Ventaja": f"{edge:+.1f}",
                     "Línea (apertura → actual)": r["Línea (apertura → actual)"], "Alertas": r["Alertas"],
                     "Motivo": v.reason})
    if not rows:
        return pd.DataFrame(columns=TOTALS_COLUMNS)
    return pd.DataFrame(rows).sort_values(["_order", "_tip"]).reset_index(drop=True)[TOTALS_COLUMNS]


def _abbr(team: str) -> str:
    return DISPLAY_ABBR.get(team, team)


def _num(v: object) -> float:
    return float(pd.to_numeric(v, errors="coerce"))


def _open_line(mk: str, odds: pd.Series) -> float:
    if mk == "spread":
        return _num(odds.get("spread_open"))
    if mk == "total":
        return _num(odds.get("total_open"))
    return no_vig_home(_num(odds.get("home_ml_open")), _num(odds.get("away_ml_open")))


def _side_line(mk: str, value: float, side_a: bool) -> str:
    if not np.isfinite(value):
        return "—"
    if mk == "total":
        return f"{value:g}"
    if mk == "ml":
        return f"{(value if side_a else 1 - value):.1%}"
    return f"{(value if side_a else -value):+g}"


def _market_row(mk: str, p_a: float, push: float, cur: dict, open_v: float) -> dict | None:
    """Pick (cara A = local/over si el modelo ve más probabilidad que el mercado), EV y movimiento."""
    line, pa, pb = cur[f"line_{mk}"], cur[f"price_{mk}_a"], cur[f"price_{mk}_b"]
    mkt = line if mk == "ml" else no_vig_home(pa, pb)
    if not all(np.isfinite(v) for v in (line, pa, pb, mkt, p_a)):
        return None
    p_a_nopush = p_a / (1 - push) if push < 1 else 0.5
    side_a = p_a_nopush > mkt
    p_win = p_a if side_a else 1 - p_a - push
    p_pick, mkt_pick = (p_a_nopush, mkt) if side_a else (1 - p_a_nopush, 1 - mkt)
    price = pa if side_a else pb
    ev = p_win * (american_to_decimal(price) - 1) - (1 - p_win - push)
    if np.isfinite(open_v):
        move = _market_move(mk, open_v, line) * (1 if side_a else -1)
        eps = MOVE_EPS[mk]
        category = "a favor" if move > eps else "en contra" if move < -eps else "sin movimiento"
    else:
        move, category = np.nan, "sin dato"
    edge_pp = (p_pick - mkt_pick) * 100
    return {"side_a": side_a, "p_pick": p_pick, "mkt_pick": mkt_pick, "edge_pp": edge_pp, "ev": ev, "price": price,
            "move": move, "category": category, "line": line, "open": open_v,
            "value_left": bool(ev > 0 and edge_pp >= MIN_EDGE_PP)}


def _tracker_market(lines: pd.DataFrame, mk: str) -> tuple[dict, float] | None:
    """(línea/precios actuales en formato `espn_market_lines`, primera lectura) de un mercado del tracker."""
    d = lines[lines["market"] == TRACKER_MARKETS[mk]].sort_values("ts")
    if d.empty:
        return None
    last = d.iloc[-1]
    cur = {f"line_{mk}": float(last["value"]), f"price_{mk}_a": float(last["price_a"]),
           f"price_{mk}_b": float(last["price_b"])}
    return cur, float(d.iloc[0]["value"])


def _tracker_context(tracker: TrackerData, event_id: str, mk: str, home: str, away: str,
                     side_a: bool, now: pd.Timestamp) -> tuple[str, str]:
    """(alertas sin NOISE, % de tickets en el lado del pick) del tracker hasta ahora."""
    a = tracker.alerts
    a = a[(a["event_id"] == event_id) & (a["market"] == mk) & (a["kind"] != "NOISE") & (a["ts"] <= now)]
    pct = _public_on_pick(tracker.splits, {"home_team": home, "away_team": away}, mk, side_a,
                          now + pd.Timedelta(seconds=1))
    return ",".join(sorted(set(a["kind"]))) or "—", "—" if pd.isna(pct) else f"{pct:.0f}%"


def build_report(preds: pd.DataFrame, projections: list, upcoming: pd.DataFrame,
                 tracker: TrackerData | None = None, now: pd.Timestamp | None = None) -> pd.DataFrame:
    """Una fila por partido y mercado con el pick del modelo sin mezcla y la lectura del mercado."""
    now = now if now is not None else pd.Timestamp.now(tz="UTC")
    sched = upcoming.drop_duplicates("game_id").set_index("game_id")
    events = tracker_events(tracker, upcoming).set_index("game_id")["event_id"].to_dict()
    probs = {p.row["game_id"]: p.market_probs for p in projections}
    rows = []
    for p in preds.itertuples(index=False):
        if p.game_id not in sched.index:
            continue
        odds = sched.loc[p.game_id]
        espn_cur = espn_market_lines(odds)
        event_id = events.get(p.game_id)
        ev_lines = (tracker.lines[(tracker.lines["event_id"] == event_id) & (tracker.lines["ts"] <= now)]
                    if event_id is not None else None)
        home, away = _abbr(p.home_team), _abbr(p.away_team)
        leader = home if p.exp_margin >= 0 else away
        model_side = f"{leader} por {abs(p.exp_margin):.1f}"
        market_p = {**probs.get(p.game_id, {}), "ml": (p.p_home_win_markov, 0.0)}
        for mk in ("spread", "total", "ml"):
            if mk not in market_p:
                continue
            tracked = _tracker_market(ev_lines, mk) if ev_lines is not None else None
            cur, open_v, source = (*tracked, "DK") if tracked else (espn_cur, _open_line(mk, odds), "ESPN")
            r = _market_row(mk, market_p[mk][0], market_p[mk][1], cur, open_v)
            if r is None:
                continue
            alerts, public = (_tracker_context(tracker, event_id, mk, p.home_team, p.away_team, r["side_a"], now)
                              if tracked else ("—", "—"))
            team = home if r["side_a"] else away
            pick = ({"spread": f"{team} {_side_line('spread', r['line'], r['side_a'])}",
                     "total": f"{'Over' if r['side_a'] else 'Under'} {r['line']:g}", "ml": f"{team} ML"}[mk])
            if mk == "ml":
                pick += f" ({r['price']:+.0f})"
            rows.append({
                "tip": pd.Timestamp(odds["start_utc"]), "game_id": p.game_id, "category": r["category"],
                "Hora": pd.Timestamp(odds["start_utc"]).tz_convert(LOCAL_TZ).strftime("%H:%M"),
                "Partido": f"{away} @ {home}", "Mercado": MARKET_NAMES[mk], "Pick": pick,
                "Línea (apertura → actual)": (f"{_side_line(mk, r['open'], r['side_a'])} → "
                                              f"{_side_line(mk, r['line'], r['side_a'])}"),
                "Modelo": f"total {p.exp_total:.1f}" if mk == "total" else model_side,
                "P modelo vs mercado": f"{r['p_pick']:.1%} vs {r['mkt_pick']:.1%}",
                "Edge": f"{r['edge_pp']:+.1f} pp", "EV": f"{r['ev']:+.3f}",
                "Valor": "✓" if r["value_left"] else "⚠", "Alertas": alerts, "% público": public,
                "Fuente": source,
                "move": r["move"], "edge_pp": r["edge_pp"], "ev": r["ev"],
                "side_a": r["side_a"], "line": r["line"], "value_left": r["value_left"],
                "model_total": p.exp_total,
            })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(["tip", "Partido", "Mercado"]).reset_index(drop=True)


def _groups(report: pd.DataFrame):
    for key, title in GROUPS:
        d = report[report["category"] == key]
        if len(d) or key != "sin dato":
            yield title, d[COLUMNS]


def render_text(report: pd.DataFrame) -> str:
    if report.empty:
        return "Sin líneas de mercado de ESPN para comparar."
    parts = [LEGEND, ""]
    for title, d in _groups(report):
        parts += [f"{title} ({len(d)})", d.to_string(index=False) if len(d) else "  (ninguno)", ""]
    totals = totals_read(report)
    if len(totals):
        parts += ["LECTURA DE TOTALES:", TOTALS_LEGEND, totals.to_string(index=False), ""]
    return "\n".join(parts)


def _markdown_table(d: pd.DataFrame) -> str:
    head = "| " + " | ".join(d.columns) + " |"
    sep = "|" + "|".join("---" for _ in d.columns) + "|"
    return "\n".join([head, sep, *("| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False))])


def render_markdown(report: pd.DataFrame, date: str) -> str:
    parts = [f"## Modelo vs mercado — {date}", ""]
    if report.empty:
        return "\n".join(parts + ["_Sin líneas de mercado de ESPN para comparar._", ""])
    counts = report["category"].value_counts()
    parts += [(f"**{counts.get('a favor', 0)}** picks con el mercado a favor · **{counts.get('en contra', 0)}** "
               f"en contra · **{counts.get('sin movimiento', 0)}** sin movimiento"), ""]
    totals = totals_read(report)
    if len(totals):
        parts += ["### Lectura de totales", "", f"_{TOTALS_LEGEND}_", "", _markdown_table(totals), ""]
    parts += [f"_{LEGEND}_", ""]
    for title, d in _groups(report):
        parts += [f"### {title} ({len(d)})", "", _markdown_table(d) if len(d) else "_Ninguno._", ""]
    return "\n".join(parts)
