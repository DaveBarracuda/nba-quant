"""Modelo vs movimiento de mercado (con el NBA Odds Tracker) y win rate de los picks.

Flujo:
 1. `build_snapshots`: en cada corrida se guarda el número del modelo (margen, total, P(local))
    junto a la línea que el tracker veía en ese instante -> tabla `model_snapshots`.
 2. `pick_table`: por snapshot y mercado, el pick es el lado donde el modelo ve valor
    (edge = modelo − mercado). Después se mide el movimiento de la línea hasta el último
    snapshot del tracker antes del salto (su "cierre"):
        CLV = movimiento · signo(edge)    (>0: el mercado se movió HACIA el modelo)
    categorías: "a favor" (CLV > 0), "en contra" (CLV < 0), "sin movimiento".
 3. Al terminar el partido se califica a la línea y el precio del momento del pick.
 4. `summarize`: WR, unidades y ROI por mercado, por categoría de movimiento, con/sin alertas
    del tracker (STEAM/RLM/INFO) y según el lado del público (tickets de Action Network).

Unidades: spread y total en puntos; ML en probabilidad sin vig del local (CLV en p.p.).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from nba_quant.integrations.odds_tracker import closing_line, line_asof
from nba_quant.models.devig import american_to_decimal

MOVE_EPS = {"spread": 0.25, "total": 0.25, "ml": 0.005}
PUBLIC_SIDE_PCT = 60.0
SNAPSHOT_KEYS = ("game_id", "snapshot_ts")
MARKET_ORDER = ("spread", "total", "ml")


def build_snapshots(projections: pd.DataFrame, events: pd.DataFrame, lines: pd.DataFrame,
                    snapshot_ts: pd.Timestamp, model_version: str) -> pd.DataFrame:
    """`projections`: game_id, model_margin (local), model_total, model_p_home (sin mezcla con mercado).
    `events`: eventos del tracker ya emparejados (event_id, game_id, commence_time, equipos)."""
    ev = events.dropna(subset=["game_id"]).drop_duplicates("game_id").set_index("game_id")
    rows = []
    for p in projections.itertuples(index=False):
        if p.game_id not in ev.index:
            continue
        e = ev.loc[p.game_id]
        row = {"game_id": p.game_id, "snapshot_ts": snapshot_ts.isoformat(), "event_id": e["event_id"],
               "commence_time": pd.Timestamp(e["commence_time"]).isoformat(), "home_team": e["home_team"],
               "away_team": e["away_team"], "model_margin": p.model_margin, "model_total": p.model_total,
               "model_p_home": p.model_p_home, "model_version": model_version}
        for mk in MARKET_ORDER:
            ln = line_asof(lines, e["event_id"], mk, snapshot_ts)
            row[f"line_{mk}"] = float(ln["value"]) if ln is not None else np.nan
            row[f"price_{mk}_a"] = float(ln["price_a"]) if ln is not None else np.nan
            row[f"price_{mk}_b"] = float(ln["price_b"]) if ln is not None else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def _edge_and_side(mk: str, s: pd.Series) -> tuple[float, bool]:
    """(edge con signo, True si el pick es la cara A = local/over)."""
    if mk == "spread":
        edge = s["model_margin"] + s["line_spread"]  # margen del modelo − margen del mercado (local)
    elif mk == "total":
        edge = s["model_total"] - s["line_total"]
    else:
        edge = s["model_p_home"] - s["line_ml"]
    return float(edge), bool(edge > 0)


def _market_move(mk: str, start: float, close: float) -> float:
    """Movimiento hacia la cara A (local en spread/ML, over en total)."""
    return (start - close) if mk == "spread" else (close - start)


def _grade(mk: str, side_a: bool, line: float, margin: float, total: float) -> float:
    """1 gana, 0 pierde, 0.5 push. `line` = línea del local (spread) o del total."""
    if mk == "total":
        diff = total - line
        return 0.5 if diff == 0 else float((diff > 0) == side_a)
    side_margin = margin if side_a else -margin
    if mk == "ml":
        return float(side_margin > 0)
    adj = side_margin + (line if side_a else -line)
    return 0.5 if adj == 0 else float(adj > 0)


def _profit(result: float, price: float) -> float:
    if not np.isfinite(result) or not np.isfinite(price):
        return np.nan
    dec = american_to_decimal(float(price))
    return dec - 1 if result == 1 else (-1.0 if result == 0 else 0.0)


def _pick_label(mk: str, side_a: bool, s: pd.Series) -> str:
    if mk == "total":
        return f"{'Over' if side_a else 'Under'} {s['line_total']:g}"
    team = s["home_team"] if side_a else s["away_team"]
    if mk == "ml":
        return f"{team} ML"
    line = s["line_spread"] if side_a else -s["line_spread"]
    return f"{team} {line:+g}"


def _alert_kinds(alerts: pd.DataFrame | None, event_id: str, mk: str, start: pd.Timestamp,
                 end: pd.Timestamp) -> str:
    if alerts is None or alerts.empty:
        return ""
    a = alerts[(alerts["event_id"] == event_id) & (alerts["market"] == mk)
               & (alerts["ts"] > start) & (alerts["ts"] < end) & (alerts["kind"] != "NOISE")]
    return ",".join(sorted(set(a["kind"])))


def _public_on_pick(splits: pd.DataFrame | None, s: pd.Series, mk: str, side_a: bool,
                    commence: pd.Timestamp) -> float:
    if splits is None or splits.empty:
        return np.nan
    d = splits[(splits["home_team"] == s["home_team"]) & (splits["away_team"] == s["away_team"])
               & (splits["market"] == mk) & (splits["ts"] < commence)]
    if d.empty:
        return np.nan
    pct = float(d.sort_values("ts").iloc[-1]["tickets_pct"])
    return pct if side_a else 100.0 - pct


def pick_table(snapshots: pd.DataFrame, lines: pd.DataFrame, results: pd.DataFrame,
               alerts: pd.DataFrame | None = None, splits: pd.DataFrame | None = None) -> pd.DataFrame:
    """Un pick por (snapshot, mercado) con edge, CLV vs cierre del tracker, alertas, público y resultado.

    `results`: game_id, home_score, away_score (sólo partidos finalizados)."""
    res = results.drop_duplicates("game_id").set_index("game_id") if len(results) else pd.DataFrame()
    rows = []
    for _, s in snapshots.iterrows():
        commence, snap_ts = pd.Timestamp(s["commence_time"]), pd.Timestamp(s["snapshot_ts"])
        for mk in MARKET_ORDER:
            if not np.isfinite(s.get(f"line_{mk}", np.nan)):
                continue
            edge, side_a = _edge_and_side(mk, s)
            close = closing_line(lines, s["event_id"], mk, commence)
            has_close = close is not None and pd.Timestamp(close["ts"]) > snap_ts
            close_v = float(close["value"]) if has_close else np.nan
            move = _market_move(mk, s[f"line_{mk}"], close_v) if has_close else np.nan
            clv = move * (1 if side_a else -1) if has_close else np.nan
            eps = MOVE_EPS[mk]
            category = ("pendiente" if not has_close else
                        "a favor" if clv > eps else "en contra" if clv < -eps else "sin movimiento")
            price = s[f"price_{mk}_a"] if side_a else s[f"price_{mk}_b"]
            row = {
                "game_id": s["game_id"], "snapshot_ts": s["snapshot_ts"], "commence_time": s["commence_time"],
                "matchup": f"{s['away_team']} @ {s['home_team']}", "market": mk,
                "pick": _pick_label(mk, side_a, s), "edge": edge, "line_pick": s[f"line_{mk}"], "price": price,
                "line_close": close_v, "clv": clv,
                "gap_closed": clv / abs(edge) if edge and has_close else np.nan, "move_category": category,
                "alert_kinds": _alert_kinds(alerts, s["event_id"], mk, snap_ts, commence),
                "public_pct_on_pick": _public_on_pick(splits, s, mk, side_a, commence),
                "result": np.nan, "units": np.nan,
                "event_id": s["event_id"], "line_source": s.get("line_source", "tracker"),
            }
            if s["game_id"] in res.index:
                r = res.loc[s["game_id"]]
                margin, total = float(r["home_score"] - r["away_score"]), float(r["home_score"] + r["away_score"])
                row["result"] = _grade(mk, side_a, s[f"line_{mk}"], margin, total)
                row["units"] = _profit(row["result"], price)
            rows.append(row)
    return pd.DataFrame(rows)


def first_snapshot_picks(picks: pd.DataFrame) -> pd.DataFrame:
    """El pick 'oficial' de cada partido-mercado es el del primer snapshot del modelo."""
    if picks.empty:
        return picks
    return picks.sort_values("snapshot_ts").groupby(["game_id", "market"], as_index=False).first()


def _wr(d: pd.DataFrame) -> dict[str, object]:
    graded = d[d["result"].notna()]
    w, l, p = (int((graded["result"] == v).sum()) for v in (1, 0, 0.5))
    return {"picks": len(d), "calificados": len(graded), "récord": f"{w}-{l}-{p}",
            "WR": w / (w + l) if w + l else np.nan, "unidades": float(graded["units"].sum()),
            "ROI": float(graded["units"].mean()) if len(graded) else np.nan,
            "CLV medio": float(d["clv"].mean()) if d["clv"].notna().any() else np.nan,
            "% a favor": float((d["move_category"] == "a favor").mean()) if len(d) else np.nan}


def summarize(picks: pd.DataFrame) -> pd.DataFrame:
    """WR general, por mercado, por categoría de movimiento, por alertas y por lado del público."""
    if picks.empty:
        return pd.DataFrame()
    out = [{"grupo": "GENERAL", "valor": "todos", **_wr(picks)}]
    for mk, d in picks.groupby("market"):
        out.append({"grupo": "mercado", "valor": mk, **_wr(d)})
    for cat, d in picks.groupby("move_category"):
        out.append({"grupo": "movimiento", "valor": cat, **_wr(d)})
    for (mk, cat), d in picks.groupby(["market", "move_category"]):
        out.append({"grupo": "mercado × movimiento", "valor": f"{mk} · {cat}", **_wr(d)})
    alerted = picks["alert_kinds"].fillna("") != ""
    out.append({"grupo": "alertas tracker", "valor": "con STEAM/RLM/INFO/GRADUAL", **_wr(picks[alerted])})
    out.append({"grupo": "alertas tracker", "valor": "sin alerta", **_wr(picks[~alerted])})
    pub = picks["public_pct_on_pick"]
    out.append({"grupo": "público", "valor": f"modelo con el público (≥{PUBLIC_SIDE_PCT:.0f}% tickets)",
                **_wr(picks[pub >= PUBLIC_SIDE_PCT])})
    out.append({"grupo": "público", "valor": f"modelo contra el público (≤{100 - PUBLIC_SIDE_PCT:.0f}% tickets)",
                **_wr(picks[pub <= 100 - PUBLIC_SIDE_PCT])})
    return pd.DataFrame(out)


CLV_UNITS = {"spread": ("pts", 1.0), "total": ("pts", 1.0), "ml": ("pp", 100.0)}


def clv_summary(picks: pd.DataFrame) -> pd.DataFrame:
    """CLV medio por mercado (IC 95%) y % de picks con movimiento en que la línea fue hacia el modelo.

    Sólo cuentan los picks con cierre conocido; `p (azar)` = P(≥ ese % a favor | movimiento 50/50)."""
    from scipy.stats import binomtest

    if picks.empty:
        return pd.DataFrame()
    known = picks[picks["move_category"] != "pendiente"]
    rows = []
    for mk in (*MARKET_ORDER, "todos"):
        d = known if mk == "todos" else known[known["market"] == mk]
        fav, against = int((d["move_category"] == "a favor").sum()), int((d["move_category"] == "en contra").sum())
        moved = fav + against
        row = {"mercado": mk, "con cierre": len(d), "a favor": fav, "en contra": against,
               "% hacia el modelo": fav / moved if moved else np.nan,
               "p (azar)": binomtest(fav, moved, 0.5, alternative="greater").pvalue if moved else np.nan,
               "unidad": "", "CLV medio": np.nan, "IC 95% bajo": np.nan, "IC 95% alto": np.nan}
        if mk != "todos" and len(d):  # "todos" mezcla puntos y probabilidad: sin CLV agregado
            unit, scale = CLV_UNITS[mk]
            clv = d["clv"].astype(float).dropna() * scale
            half = 1.96 * clv.std(ddof=1) / np.sqrt(len(clv)) if len(clv) > 1 else np.nan
            row.update({"unidad": unit, "CLV medio": clv.mean(), "IC 95% bajo": clv.mean() - half,
                        "IC 95% alto": clv.mean() + half})
        rows.append(row)
    return pd.DataFrame(rows)


def model_vs_market_drift(snapshots: pd.DataFrame) -> pd.DataFrame:
    """Entre el primer y el último snapshot de cada partido: cuánto se movió el número del modelo
    y cuánto la línea, y si la brecha entre ambos se cerró (convergen) o se abrió (divergen)."""
    rows = []
    for gid, d in snapshots.sort_values("snapshot_ts").groupby("game_id"):
        if len(d) < 2:
            continue
        a, b = d.iloc[0], d.iloc[-1]
        for mk, col in (("spread", "model_margin"), ("total", "model_total"), ("ml", "model_p_home")):
            mkt_a = -a["line_spread"] if mk == "spread" else a[f"line_{mk}"]
            mkt_b = -b["line_spread"] if mk == "spread" else b[f"line_{mk}"]
            gap_a, gap_b = a[col] - mkt_a, b[col] - mkt_b
            if not (np.isfinite(gap_a) and np.isfinite(gap_b)):
                continue
            rows.append({"game_id": gid, "matchup": f"{a['away_team']} @ {a['home_team']}", "market": mk,
                         "model_move": b[col] - a[col], "market_move": mkt_b - mkt_a,
                         "gap_first": gap_a, "gap_last": gap_b,
                         "estado": "convergen" if abs(gap_b) < abs(gap_a) else "divergen"})
    return pd.DataFrame(rows)
