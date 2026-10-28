"""Reporte semanal de estrategias: calificación, semanas, tramos y movimiento."""

from __future__ import annotations

import pandas as pd

from nba_quant.weekly_report import bucket_table, strategy_picks, summary_table, write_weekly

LINES = pd.DataFrame({  # tracker: el spread de G1 se mueve hacia el local (-3.5 -> -5.5)
    "event_id": ["E1", "E1", "E1", "E2"], "market": ["spread", "spread", "total", "spread"],
    "ts": pd.to_datetime(["2026-10-20T15:00Z", "2026-10-20T23:00Z", "2026-10-20T23:00Z", "2026-10-28T23:00Z"]),
    "value": [-3.5, -5.5, 220.5, -1.0], "price_a": [-110] * 4, "price_b": [-110] * 4,
})


def _snap(gid: str, event: str, tip: str, snap: str, margin: float, total: float, p_home: float) -> dict:
    return {"game_id": gid, "event_id": event, "commence_time": tip, "snapshot_ts": snap, "home_team": "BKN",
            "away_team": "CHA", "model_margin": margin, "model_total": total, "model_p_home": p_home,
            "line_spread": -3.5 if gid == "G1" else -1.0, "price_spread_a": -110, "price_spread_b": -110,
            "line_total": 220.5, "price_total_a": -110, "price_total_b": -110,
            "line_ml": 0.60, "price_ml_a": -160, "price_ml_b": 135}


SNAPS = pd.DataFrame([
    _snap("G1", "E1", "2026-10-20T23:30Z", "2026-10-20T16:00Z", 7.0, 215.0, 0.70),
    _snap("G1", "E1", "2026-10-20T23:30Z", "2026-10-20T20:00Z", 1.0, 230.0, 0.40),  # no oficial (2º snapshot)
    _snap("G2", "E2", "2026-10-28T23:30Z", "2026-10-28T16:00Z", -4.0, 230.0, 0.45),
])
GAMES = pd.DataFrame({"game_id": ["G1", "G2"], "home_score": [110, 100], "away_score": [104, 108]})


def test_strategies_grade_official_snapshot_with_movement_and_weeks() -> None:
    df = strategy_picks(SNAPS, GAMES, LINES).set_index(["game_id", "strategy"])
    sp = df.loc[("G1", "spread")]
    assert sp["pick"] == "BKN -3.5" and sp["category"] == "a favor" and sp["result"] == 1 and sp["strength"] == 3.5
    assert df.loc[("G1", "total"), "pick"] == "Under 220.5" and df.loc[("G1", "total"), "category"] == "sin movimiento"
    assert df.loc[("G1", "ml ganador"), "pick"] == "BKN ML" and df.loc[("G1", "ml valor"), "pick"] == "BKN ML"
    assert df.loc[("G1", "ml ganador"), "category"] == "sin dato"  # el tracker no tiene ML de G1
    assert df.loc[("G2", "spread"), "pick"] == "CHA +1" and df.loc[("G2", "spread"), "category"] == "sin movimiento"
    assert str(df.loc[("G1", "spread"), "week_start"]) == "2026-10-20"
    assert str(df.loc[("G2", "spread"), "week_start"]) == "2026-10-27"  # día 8 -> semana 2
    assert df.loc[("G1", "spread"), "bucket"] == "3-4 pts" and df.loc[("G1", "ml ganador"), "bucket"] == "70-75 % P"


def test_tables_and_files(tmp_path) -> None:
    df = strategy_picks(SNAPS, GAMES, LINES)
    s = summary_table(df).set_index(["estrategia", "filtro"])
    assert s.loc[("spread", "todas"), "récord"] == "2-0-0" and s.loc[("spread", "a favor"), "picks"] == 1
    b = bucket_table(df).set_index(["estrategia", "tramo"])
    assert b.loc[("spread", "3-4 pts"), "a favor + sin mov."].startswith("1-0-0")
    weeks = write_weekly(df, tmp_path)
    assert [w.name for w in weeks] == ["2026-10-20_2026-10-26", "2026-10-27_2026-11-02"]
    assert (tmp_path / "all_picks.csv").exists() and "Evolución por semana" in (tmp_path / "README.md").read_text(
        encoding="utf-8")
    assert len(pd.read_csv(weeks[0] / "picks.csv")) == 4
    assert write_weekly(df.iloc[0:0], tmp_path / "vacío") == []
