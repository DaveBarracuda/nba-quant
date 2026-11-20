"""Lectura de totales: reglas de stake según movimiento, alertas y ventaja en puntos."""

from __future__ import annotations

import pandas as pd

from nba_quant.market_report import (
    classify_total,
    render_markdown,
    render_text,
    totals_read,
)


def test_toward_model_in_best_band_is_normal() -> None:
    v = classify_total("a favor", 6.8, True, "INFO,RLM,STEAM")
    assert v.tier == "🟢" and v.stake == "Normal"


def test_gradual_toward_model_is_flagged_as_priority() -> None:
    v = classify_total("a favor", 5.0, True, "GRADUAL")
    assert v.tier == "🟢" and "prioridad" in v.reason


def test_big_edge_toward_model_is_reduced() -> None:
    v = classify_total("a favor", 12.9, True, "RLM,STEAM")
    assert v.tier == "🟡" and v.stake == "Reducido"


def test_no_movement_is_small_stake() -> None:
    v = classify_total("sin movimiento", 13.1, True, "RLM,STEAM")
    assert v.tier == "🟡" and v.stake == "Chico"


def test_against_with_sharp_alerts_is_out() -> None:
    v = classify_total("en contra", 7.5, True, "GRADUAL,RLM")
    assert v.tier == "❌" and "STEAM/RLM" in v.reason


def test_against_without_sharp_alerts_is_still_out() -> None:
    v = classify_total("en contra", 5.0, True, "INFO")
    assert v.tier == "❌"


def test_no_value_left_is_out_even_if_toward_model() -> None:
    v = classify_total("a favor", 5.0, False, "STEAM")
    assert v.tier == "❌" and "sin valor" in v.reason


def test_thin_edge_is_minimal() -> None:
    v = classify_total("a favor", 2.0, True, "—")
    assert v.tier == "🟡" and v.stake == "Mínimo"


def test_missing_open_needs_manual_check() -> None:
    assert classify_total("sin dato", 5.0, True, "—").tier == "⏳"


def _report() -> pd.DataFrame:
    base = {"Hora": "18:00", "Mercado": "Total", "Fuente": "DK", "tip": pd.Timestamp("2026-11-19T00:00Z"),
            "Modelo": "", "P modelo vs mercado": "", "Edge": "", "EV": "", "Valor": "✓", "% público": "—"}
    rows = [
        {**base, "Partido": "HOU @ IND", "Pick": "Over 224.5", "category": "sin movimiento", "side_a": True,
         "line": 224.5, "model_total": 237.6, "value_left": True, "Alertas": "RLM,STEAM",
         "Línea (apertura → actual)": "224.5 → 224.5"},
        {**base, "Partido": "MEM @ CLE", "Pick": "Over 239.5", "category": "a favor", "side_a": True,
         "line": 239.5, "model_total": 246.3, "value_left": True, "Alertas": "INFO,RLM,STEAM",
         "Línea (apertura → actual)": "236.5 → 239.5"},
        {**base, "Partido": "ATL @ OKC", "Pick": "Under 228.5", "category": "en contra", "side_a": False,
         "line": 228.5, "model_total": 224.3, "value_left": True, "Alertas": "RLM,STEAM",
         "Línea (apertura → actual)": "226.5 → 228.5"},
        {**base, "Partido": "MEM @ CLE", "Mercado": "Spread", "Pick": "MEM +4.5", "category": "a favor"},
    ]
    return pd.DataFrame(rows)


def test_totals_read_sorts_by_verdict_and_uses_signed_edge() -> None:
    t = totals_read(_report())
    assert t["Partido"].tolist() == ["MEM @ CLE", "HOU @ IND", "ATL @ OKC"]
    assert t["Ventaja"].tolist() == ["+6.8", "+13.1", "+4.2"]
    assert t["Veredicto"].tolist() == ["🟢 Normal", "🟡 Chico", "❌ Fuera"]


def test_totals_read_section_is_in_log_and_summary() -> None:
    rep = _report()
    assert "LECTURA DE TOTALES" in render_text(rep)
    md = render_markdown(rep, "2026-11-18")
    assert "### Lectura de totales" in md and "| 🟢 Normal |" in md
