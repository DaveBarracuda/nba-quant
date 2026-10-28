"""Reporte semanal de estrategias: guarda cada semana y el acumulado para buscar "spots".

Por cada partido con snapshot oficial (primer snapshot del modelo) se califican cuatro maneras de
usar la proyección, todas a la línea y el precio del momento del pick:
  spread      lado que marca el modelo vs la línea            fuerza = |edge| en puntos
  total       Over/Under del modelo vs la línea               fuerza = |edge| en puntos
  ml ganador  equipo que el modelo proyecta ganador           fuerza = P(ganar) del modelo
  ml valor    lado con P modelo > P mercado (el del ledger)   fuerza = edge en probabilidad
y se cruzan con el movimiento del mercado hasta el cierre del tracker (a favor / en contra / sin
movimiento) y por tramos de fuerza. Semanas = bloques de 7 días desde el primer día con picks.

Salida (se publica con el ledger):
  ledger/weekly/<inicio>_<fin>/  picks.csv, summary.csv, edge_buckets.csv, top5.csv, README.md
  ledger/weekly/all_picks.csv    todas las semanas (base para buscar spots)
  ledger/weekly/README.md        evolución semanal + tabla acumulada por tramo × movimiento
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from nba_quant.integrations.odds_tracker import closing_line
from nba_quant.ledger import DEFAULT_LEDGER_DIR, _markdown
from nba_quant.simulation.market_moves import MOVE_EPS, _grade, _market_move, _profit

WEEKLY_DIR = DEFAULT_LEDGER_DIR / "weekly"
US_DATE_SHIFT = pd.Timedelta(hours=6)
WEEK_DAYS = 7
TOP_N = 5
STRATEGIES = ("spread", "total", "ml ganador", "ml valor")
CATEGORIES = ("a favor", "sin movimiento", "en contra", "sin dato")
FILTERS = {  # nombre -> categorías de movimiento incluidas
    "todas": CATEGORIES, "a favor + sin mov.": ("a favor", "sin movimiento"), "a favor": ("a favor",),
    "sin movimiento": ("sin movimiento",), "en contra": ("en contra",),
}
BUCKETS = {  # estrategia -> (cortes de fuerza, escala para mostrar, unidad)
    "spread": ([0, 1, 2, 3, 4, 5, 7, np.inf], 1, "pts"),
    "total": ([0, 1, 2, 3, 4, 5, 7, np.inf], 1, "pts"),
    "ml valor": ([0, .02, .04, .06, .10, .15, np.inf], 100, "pp"),
    "ml ganador": ([.5, .55, .6, .65, .7, .75, np.inf], 100, "% P"),
}


def _side_label(mk: str, side_a: bool, s: pd.Series) -> str:
    if mk == "total":
        return f"{'Over' if side_a else 'Under'} {s['line_total']:g}"
    team = s["home_team"] if side_a else s["away_team"]
    if mk == "ml":
        return f"{team} ML"
    return f"{team} {(s['line_spread'] if side_a else -s['line_spread']):+g}"


def _strategies(s: pd.Series) -> dict[str, tuple[str, bool, float]]:
    """estrategia -> (mercado, cara A = local/over, fuerza de la proyección)."""
    return {
        "spread": ("spread", s["model_margin"] + s["line_spread"] > 0, abs(s["model_margin"] + s["line_spread"])),
        "total": ("total", s["model_total"] - s["line_total"] > 0, abs(s["model_total"] - s["line_total"])),
        "ml ganador": ("ml", s["model_margin"] > 0, max(s["model_p_home"], 1 - s["model_p_home"])),
        "ml valor": ("ml", s["model_p_home"] - s["line_ml"] > 0, abs(s["model_p_home"] - s["line_ml"])),
    }


def _movement(lines: pd.DataFrame, s: pd.Series, mk: str, line: float, side_a: bool) -> tuple[str, float]:
    commence, snap_ts = pd.Timestamp(s["commence_time"]), pd.Timestamp(s["snapshot_ts"])
    close = closing_line(lines, s["event_id"], mk, commence)
    if close is None or pd.Timestamp(close["ts"]) <= snap_ts:
        return "sin dato", np.nan
    clv = _market_move(mk, line, float(close["value"])) * (1 if side_a else -1)
    eps = MOVE_EPS[mk]
    return ("a favor" if clv > eps else "en contra" if clv < -eps else "sin movimiento"), clv


def _bucket(strategy: str, strength: float) -> str:
    cuts, scale, unit = BUCKETS[strategy]
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        if lo <= strength < hi:
            return f"{lo * scale:g}+ {unit}" if not np.isfinite(hi) else f"{lo * scale:g}-{hi * scale:g} {unit}"
    return "—"


def strategy_picks(snapshots: pd.DataFrame, games: pd.DataFrame, lines: pd.DataFrame) -> pd.DataFrame:
    """Un renglón por partido terminado y estrategia, calificado a la línea del pick oficial."""
    if snapshots.empty or games.empty:
        return pd.DataFrame()
    official = snapshots.sort_values("snapshot_ts").groupby("game_id", as_index=False).first()
    res = games.drop_duplicates("game_id").set_index("game_id")
    rows = []
    for _, s in official[official["game_id"].isin(res.index)].iterrows():
        g = res.loc[s["game_id"]]
        margin, total = float(g["home_score"] - g["away_score"]), float(g["home_score"] + g["away_score"])
        day = (pd.Timestamp(s["commence_time"]) - US_DATE_SHIFT).date()
        for strat, (mk, side_a, strength) in _strategies(s).items():
            line = s[f"line_{mk}"]
            if not np.isfinite(line):
                continue
            price = s[f"price_{mk}_a"] if side_a else s[f"price_{mk}_b"]
            result = _grade(mk, side_a, line, margin, total)
            category, clv = _movement(lines, s, mk, line, side_a)
            rows.append({"game_id": s["game_id"], "day": day, "matchup": f"{s['away_team']} @ {s['home_team']}",
                         "strategy": strat, "pick": _side_label(mk, side_a, s), "line": line, "price": price,
                         "strength": float(strength), "category": category, "clv": clv, "result": result,
                         "units": _profit(result, price)})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["rank"] = df.groupby(["day", "strategy"])["strength"].rank(ascending=False, method="first")
    df["top5"] = df["rank"] <= TOP_N
    start = min(df["day"])
    df["week_start"] = [start + pd.Timedelta(days=WEEK_DAYS * ((d - start).days // WEEK_DAYS)) for d in df["day"]]
    df["bucket"] = [_bucket(st, v) for st, v in zip(df["strategy"], df["strength"])]
    return df


def _stats(d: pd.DataFrame) -> dict:
    w, l, p = int((d["result"] == 1).sum()), int((d["result"] == 0).sum()), int((d["result"] == 0.5).sum())
    n = len(d)
    return {"picks": n, "récord": f"{w}-{l}-{p}", "WR": w / (w + l) if w + l else np.nan,
            "unidades": float(d["units"].sum()), "ROI": float(d["units"].sum()) / n if n else np.nan}


def _cell(d: pd.DataFrame) -> str:
    if d.empty:
        return "—"
    s = _stats(d)
    return f"{s['récord']} · {s['WR']:.0%} · {s['unidades']:+.2f}u · {s['ROI']:+.0%}"


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for strat in STRATEGIES:
        d = df[df["strategy"] == strat]
        for name, cats in FILTERS.items():
            rows.append({"estrategia": strat, "filtro": name, **_stats(d[d["category"].isin(cats)])})
    return pd.DataFrame(rows)


def bucket_table(df: pd.DataFrame) -> pd.DataFrame:
    """Por estrategia y tramo de fuerza: todas, a favor + sin mov., a favor, sin mov., en contra."""
    rows = []
    for strat in STRATEGIES:
        d = df[df["strategy"] == strat]
        cuts = BUCKETS[strat][0]
        order = [b for b in (_bucket(strat, c) for c in cuts[:-1]) if (d["bucket"] == b).any()]
        for b in [*order, "TOTAL"]:
            dd = d if b == "TOTAL" else d[d["bucket"] == b]
            rows.append({"estrategia": strat, "tramo": b,
                         **{name: _cell(dd[dd["category"].isin(cats)]) for name, cats in FILTERS.items()}})
    return pd.DataFrame(rows)


def top_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for strat in STRATEGIES:
        d = df[df["strategy"] == strat]
        best = d["top5"] & d["category"].isin(FILTERS["a favor + sin mov."])
        for name, dd in (("TOP 5 diario", d[d["top5"]]), ("resto", d[~d["top5"]]),
                         ("TOP 5 · a favor + sin mov.", d[best])):
            rows.append({"estrategia": strat, "grupo": name, **_stats(dd)})
    return pd.DataFrame(rows)


def _fmt_stats(t: pd.DataFrame) -> pd.DataFrame:
    return t.assign(WR=[f"{v:.1%}" if pd.notna(v) else "—" for v in t["WR"]],
                    unidades=[f"{v:+.2f}" for v in t["unidades"]],
                    ROI=[f"{v:+.1%}" if pd.notna(v) else "—" for v in t["ROI"]])


LEGEND = ("Picks calificados a la línea y precio del pick oficial (primer snapshot del modelo, DraftKings del "
          "tracker). Movimiento = línea del pick → cierre del tracker: ▲ a favor del modelo / = sin movimiento / "
          "▼ en contra (umbral 0.25 pts; 0.5 pp en ML). El filtro de movimiento usa el cierre, que no se conoce al "
          "apostar: es una referencia, no una regla replicable tal cual. Celdas: récord · WR · unidades · ROI.")


def render_week(df: pd.DataFrame, title: str) -> str:
    return "\n".join([
        f"# {title}", "", f"_{LEGEND}_", "",
        f"Partidos: {df['game_id'].nunique()} · días: {df['day'].min()} → {df['day'].max()}", "",
        "## Por estrategia y movimiento", "", _markdown(_fmt_stats(summary_table(df))), "",
        "## Por tramo de fuerza y movimiento", "", _markdown(bucket_table(df)), "",
        f"## TOP {TOP_N} diario vs resto", "", _markdown(_fmt_stats(top_table(df))), "",
    ])


def render_index(all_df: pd.DataFrame, weeks: list[tuple[str, str]]) -> str:
    core = all_df["strategy"].isin(["spread", "total"])
    trend = []
    for start, folder in weeks:
        w = all_df[all_df["week_start"].astype(str) == start]
        wc = core[w.index] & w["category"].isin(FILTERS["a favor + sin mov."])
        trend.append({"semana": f"[{folder}]({folder}/README.md)",
                      **{s: _cell(w[w["strategy"] == s]) for s in STRATEGIES},
                      "spread+total · a favor + sin mov.": _cell(w[wc])})
    return "\n".join([
        "# Reporte semanal de estrategias", "", f"_{LEGEND}_", "",
        "## Evolución por semana (todas las proyecciones)", "", _markdown(pd.DataFrame(trend)), "",
        "## Acumulado: por tramo de fuerza y movimiento", "",
        "_Un \"spot\" merece atención cuando se repite semana a semana y junta suficientes picks (≥ 50); "
        "con menos, cualquier tramo puede brillar por azar._", "",
        _markdown(bucket_table(all_df)), "",
        "## Acumulado: por estrategia y movimiento", "", _markdown(_fmt_stats(summary_table(all_df))), "",
        f"## Acumulado: TOP {TOP_N} diario vs resto", "", _markdown(_fmt_stats(top_table(all_df))), "",
    ])


def write_weekly(df: pd.DataFrame, out_dir: Path = WEEKLY_DIR) -> list[Path]:
    """Escribe una carpeta por semana (la en curso se reescribe hasta completarse) y el acumulado."""
    if df.empty:
        return []
    out_dir.mkdir(parents=True, exist_ok=True)
    written, weeks = [], []
    for start, w in df.groupby("week_start"):
        end = start + pd.Timedelta(days=WEEK_DAYS - 1)
        folder = f"{start}_{end}"
        wd = out_dir / folder
        wd.mkdir(exist_ok=True)
        w.to_csv(wd / "picks.csv", index=False)
        summary_table(w).to_csv(wd / "summary.csv", index=False)
        bucket_table(w).to_csv(wd / "edge_buckets.csv", index=False)
        top_table(w).to_csv(wd / "top5.csv", index=False)
        (wd / "README.md").write_text(render_week(w, f"Semana {start} → {end}"), encoding="utf-8")
        written.append(wd)
        weeks.append((str(start), folder))
    df.to_csv(out_dir / "all_picks.csv", index=False)
    (out_dir / "README.md").write_text(render_index(df, weeks), encoding="utf-8")
    return written
