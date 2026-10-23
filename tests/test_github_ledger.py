"""Ledger del workflow de GitHub: picks contra la línea de ESPN y liquidación con su cierre."""

from __future__ import annotations

import pandas as pd
import pytest

from nba_quant.github_ledger import build_espn_snapshots, no_vig_home, record_picks
from nba_quant.settle import settle_picks

PREDS = pd.DataFrame({"game_id": ["G1"], "home_team": ["BKN"], "away_team": ["CHA"], "model_margin_raw": [7.0],
                      "model_total_raw": [215.0], "p_home_win_markov": [0.70]})


def _upcoming(spread: float, total: float) -> pd.DataFrame:
    return pd.DataFrame({"game_id": ["G1"], "start_utc": ["2026-10-21T23:30Z"], "spread_close": [spread],
                         "spread_home_odds_close": [-110], "spread_away_odds_close": [-110], "total_close": [total],
                         "over_odds_close": [-110], "under_odds_close": [-110], "home_ml_close": [-160],
                         "away_ml_close": [135]})


def _record(tmp_path, spread: float, total: float, ts: str) -> pd.DataFrame:
    snaps = build_espn_snapshots(PREDS, _upcoming(spread, total), pd.Timestamp(ts), "test")
    return record_picks(snaps, tmp_path)


def test_records_first_pick_per_market_against_espn_line(tmp_path) -> None:
    picks = _record(tmp_path, -3.5, 220.5, "2026-10-21T15:00Z").set_index("market")
    assert picks.loc["spread", "pick"] == "BKN -3.5" and picks.loc["total", "pick"] == "Under 220.5"
    assert picks.loc["ml", "pick"] == "BKN ML" and picks.loc["ml", "line_pick"] == pytest.approx(no_vig_home(-160, 135))
    assert set(picks["move_category"]) == {"pendiente"} and picks["result"].isna().all()
    again = _record(tmp_path, -6.5, 216.5, "2026-10-21T20:00Z").set_index("market")  # 2ª corrida: no reemplaza
    assert again.loc["spread", "pick"] == "BKN -3.5" and len(again) == 3
    text = (tmp_path / "LEDGER.md").read_text(encoding="utf-8")
    assert "workflow de GitHub" in text and "| GENERAL | todos | 3 | 0 | 0-0-0 |" in text


def test_settle_fills_espn_close_movement_and_result(tmp_path) -> None:
    _record(tmp_path, -3.5, 220.5, "2026-10-21T15:00Z")
    csv = pd.read_csv(tmp_path / "picks.csv", dtype={"game_id": str})
    closes = {"G1": {"spread": -5.5, "total": 218.5, "ml": 0.66}}
    out, n = settle_picks(csv, {"G1": (110, 104)}.get, pd.Timestamp("2026-10-22T12:00Z"), closes.get)
    out = out.set_index("market")
    assert n == 3 and (out["result"] == 1).all()
    assert out.loc["spread", ["line_close", "clv", "move_category"]].tolist() == [-5.5, 2.0, "a favor"]
    assert out.loc["total", "clv"] == pytest.approx(2.0) and out.loc["total", "move_category"] == "a favor"
    assert out.loc["ml", "move_category"] == "a favor"
    # Cierre que se aleja del modelo -> en contra; partidos sin cierre conservan "pendiente"
    against, _ = settle_picks(csv, {"G1": (110, 104)}.get, pd.Timestamp("2026-10-22T12:00Z"),
                              {"G1": {"spread": -1.5}}.get)
    against = against.set_index("market")
    assert against.loc["spread", "move_category"] == "en contra"
    assert against.loc["total", "move_category"] == "pendiente"
