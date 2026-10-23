"""Ledger público de picks: Markdown legible en GitHub + CSV completo.

Cada pick oficial (primer snapshot del modelo por partido y mercado) con la línea al momento del
pick, la línea de cierre del tracker, si el mercado se movió a favor o en contra del modelo y el
resultado. El resumen arriba repite el récord general, por mercado y por movimiento.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LEDGER_DIR = PROJECT_ROOT / "ledger"
US_DATE_SHIFT = pd.Timedelta(hours=6)
MOVE_LABELS = {"a favor": "▲ a favor", "en contra": "▼ en contra", "sin movimiento": "= sin mov.",
               "pendiente": "… pendiente"}
RESULT_LABELS = {1.0: "✅ W", 0.0: "❌ L", 0.5: "➖ P"}
SUMMARY_GROUPS = ("GENERAL", "mercado", "movimiento", "mercado × movimiento")
MARKET_NAMES = {"spread": "Spread", "total": "Total", "ml": "ML"}


def _pick_side(mk: str, value: float, pick_is_home: bool) -> float:
    """Las líneas se guardan desde el local (spread y P sin vig del ML); se muestran desde el pick."""
    if mk == "total" or pick_is_home:
        return value
    return -value if mk == "spread" else 1 - value


def _line(mk: str, value: float) -> str:
    if pd.isna(value):
        return "—"
    if mk == "ml":
        return f"{value:.1%}"  # probabilidad sin vig del lado elegido
    return f"{value:+g}" if mk == "spread" else f"{value:g}"


def _fmt(value: float, spec: str) -> str:
    return "—" if pd.isna(value) else format(value, spec)


def _markdown(df: pd.DataFrame) -> str:
    head = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    rows = ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join([head, sep, *rows])


def ledger_rows(official: pd.DataFrame) -> pd.DataFrame:
    """Tabla de picks lista para mostrar, del partido más reciente al más antiguo."""
    if official.empty:
        return pd.DataFrame()
    d = official.assign(_t=pd.to_datetime(official["commence_time"], utc=True)).sort_values(
        ["_t", "matchup", "market"], ascending=[False, True, True])
    home = d["matchup"].str.split(" @ ").str[1]
    is_home = [p.startswith(f"{h} ") for p, h in zip(d["pick"], home)]
    pick_lines = {col: [_line(m, _pick_side(m, v, h)) for m, v, h in zip(d["market"], d[col], is_home)]
                  for col in ("line_pick", "line_close")}
    return pd.DataFrame({
        "Fecha": (d["_t"] - US_DATE_SHIFT).dt.strftime("%Y-%m-%d"),
        "Partido": d["matchup"],
        "Mercado": d["market"].map(MARKET_NAMES),
        "Pick": d["pick"],
        "Línea pick": pick_lines["line_pick"],
        "Cierre": pick_lines["line_close"],
        "Mercado vs modelo": d["move_category"].map(MOVE_LABELS).fillna(d["move_category"]),
        "CLV": [_fmt(v * 100 if m == "ml" else v, "+.2f") for m, v in zip(d["market"], d["clv"])],
        "Alertas": d["alert_kinds"].fillna("").replace("", "—"),
        "% público en pick": [_fmt(v, ".0f") for v in d["public_pct_on_pick"]],
        "Resultado": d["result"].map(RESULT_LABELS).fillna("pendiente"),
        "Unidades": [_fmt(v, "+.2f") for v in d["units"]],
    })


def summary_table(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return pd.DataFrame()
    s = summary[summary["grupo"].isin(SUMMARY_GROUPS)]
    return pd.DataFrame({
        "Grupo": s["grupo"], "Valor": s["valor"], "Picks": s["picks"], "Calificados": s["calificados"],
        "Récord": s["récord"], "WR": [_fmt(v, ".1%") for v in s["WR"]],
        "Unidades": [_fmt(v, "+.2f") for v in s["unidades"]], "ROI": [_fmt(v, "+.1%") for v in s["ROI"]],
        "CLV medio": [_fmt(v, "+.3f") for v in s["CLV medio"]],
    })


LOCAL_NOTE = ("Picks del workflow de GitHub *Ejecutar modelo* (líneas de ESPN): "
              "[github/LEDGER.md](github/LEDGER.md)")


def render_ledger(official: pd.DataFrame, summary: pd.DataFrame, generated_at: pd.Timestamp,
                  title: str = "Ledger de picks del modelo", source: str = "del NBA Odds Tracker",
                  note: str = LOCAL_NOTE) -> str:
    rows = ledger_rows(official)
    parts = [
        f"# {title}",
        f"_Actualizado: {generated_at:%Y-%m-%d %H:%M} UTC · un pick por partido y mercado (primer snapshot "
        f"del modelo, con la línea {source} en ese momento)._",
        "",
        *([note, ""] if note else []),
        "**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo "
        "(CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de "
        "probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). "
        "Spread y total se califican contra la línea del pick a −110; ML al precio del pick.",
        "",
        "## Récord",
        "",
        _markdown(summary_table(summary)) if not summary.empty else "_Sin picks todavía._",
        "",
        "## Picks",
        "",
        _markdown(rows) if not rows.empty else "_Sin picks todavía._",
    ]
    return "\n".join(parts) + "\n"


def write_ledger(official: pd.DataFrame, summary: pd.DataFrame, out_dir: Path = DEFAULT_LEDGER_DIR,
                 generated_at: pd.Timestamp | None = None, **render_kwargs: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    now = generated_at if generated_at is not None else pd.Timestamp.now(tz="UTC")
    path = out_dir / "LEDGER.md"
    path.write_text(render_ledger(official, summary, now, **render_kwargs), encoding="utf-8")
    official.to_csv(out_dir / "picks.csv", index=False)
    summary.to_csv(out_dir / "summary.csv", index=False)
    return path
