"""Análisis modelo vs mercado con las líneas de ESPN (log y resumen del workflow)."""

from __future__ import annotations

from types import SimpleNamespace

import pandas as pd

from nba_quant.market_report import build_report, render_markdown, render_text

PREDS = pd.DataFrame({"game_id": ["G1"], "home_team": ["CHI"], "away_team": ["WSH"], "exp_margin": [9.1],
                      "exp_total": [235.0], "p_home_win_markov": [0.708]})
PROJ = [SimpleNamespace(row={"game_id": "G1"}, market_probs={"spread": (0.662, 0.0), "total": (0.335, 0.0)})]


def _upcoming(spread_open: float, total_open: float) -> pd.DataFrame:
    return pd.DataFrame({
        "game_id": ["G1"], "start_utc": ["2026-10-25T00:10Z"],
        "spread_open": [spread_open], "spread_close": [-2.5], "spread_home_odds_close": [-115],
        "spread_away_odds_close": [-105], "total_open": [total_open], "total_close": [244.5],
        "over_odds_close": [-110], "under_odds_close": [-110],
        "home_ml_open": [-100], "away_ml_open": [-120], "home_ml_close": [-130], "away_ml_close": [110],
    })


def test_report_picks_movement_and_value() -> None:
    rep = build_report(PREDS, PROJ, _upcoming(1.5, 243.5)).set_index("Mercado")
    sp, tt, ml = rep.loc["Spread"], rep.loc["Total"], rep.loc["ML"]
    assert sp["Pick"] == "CHI -2.5" and sp["category"] == "a favor" and sp["move"] == 4.0
    assert sp["Línea (apertura → actual)"] == "+1.5 → -2.5" and sp["Modelo"] == "CHI por 9.1" and sp["Hora"] == "18:10"
    assert tt["Pick"] == "Under 244.5" and tt["category"] == "en contra" and tt["Modelo"] == "total 235.0"
    assert ml["Pick"] == "CHI ML (-130)" and ml["category"] == "a favor" and ml["Valor"] == "✓"
    assert rep["Partido"].unique().tolist() == ["WAS @ CHI"]


def test_report_without_open_and_rendering() -> None:
    rep = build_report(PREDS, PROJ, _upcoming(float("nan"), 244.5))
    cats = dict(zip(rep["Mercado"], rep["category"]))
    assert cats == {"Spread": "sin dato", "Total": "sin movimiento", "ML": "a favor"}
    text, md = render_text(rep), render_markdown(rep, "2026-10-24")
    assert "▲ El mercado va a favor del modelo (1)" in text and "Sin línea de apertura (1)" in text
    assert md.startswith("## Modelo vs mercado — 2026-10-24") and "| Hora | Partido | Mercado |" in md
    assert render_markdown(build_report(PREDS, PROJ, _upcoming(1.5, 243.5).iloc[0:0]), "x").endswith("comparar._\n")
