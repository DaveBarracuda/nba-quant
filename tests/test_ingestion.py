"""Parser ESPN sobre un fixture real recortado (MEM @ PHI, 2026-03-10) y cliente HTTP sin red."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from nba_quant.config import DEFAULT_CONFIG
from nba_quant.ingestion import espn
from nba_quant.ingestion.http import NonRetryableHttpError, SyncHttpClient
from nba_quant.processing.pbp import load_and_clean_pbp

FIXTURE = Path(__file__).parent / "fixtures" / "espn_summary_401810791.json"


@pytest.fixture(scope="module")
def summary() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_parse_game_and_odds(summary: dict) -> None:
    g = espn.parse_game("401810791", summary, date(2026, 3, 10))
    assert (g["home_team"], g["away_team"]) == ("PHI", "MEM")
    assert (g["home_score"], g["away_score"]) == (139, 129)
    assert g["season"] == 2026 and g["venue"]
    odds = espn.parse_odds("401810791", summary)
    assert odds[0]["spread_close"] == -4.5 and odds[0]["spread_open"] == -5.5
    assert odds[0]["home_ml_close"] == -192 and odds[0]["total_close"] == 229.5
    assert len(espn.parse_officials("401810791", summary)) == 3


def test_parse_pbp_canonical_schema(summary: dict) -> None:
    pbp = espn.parse_pbp("401810791", summary)
    assert len(pbp) == 120
    shots = pbp[pbp["event_type"] == "shot"]
    assert shots["shot_value"].isin([2, 3]).all()
    assert shots["shot_distance"].notna().mean() > 0.9
    first3 = shots[shots["text"].str.contains("25-foot three")].iloc[0]
    assert first3["made"] and first3["shot_distance"] == 25 and first3["shot_style"] == "pull_up"
    fts = pbp[pbp["event_type"] == "free_throw"]
    assert fts["ft_total"].notna().all()
    assert pbp["home_wp"].notna().mean() > 0.9
    clean = load_and_clean_pbp(pbp.assign(season=2026), DEFAULT_CONFIG.game_state)
    assert clean["game_sec_elapsed"].is_monotonic_increasing


def test_parse_player_box(summary: dict) -> None:
    box = pd.DataFrame(espn.parse_player_box("401810791", summary))
    assert set(box["team"]) == {"PHI", "MEM"}
    assert box.groupby("team")["starter"].sum().eq(5).all()
    assert box.groupby("team")["pts"].sum().to_dict() == {"MEM": 129.0, "PHI": 139.0}


def test_clock_and_classification_helpers() -> None:
    assert espn._clock_to_seconds("11:45") == 705.0
    assert espn._clock_to_seconds("38.2") == 38.2
    assert espn._classify("Traveling", False, "") == "turnover"
    assert espn._classify("Free Throw - 1 of 2", False, "") == "free_throw"
    assert espn._classify("Full Timeout", False, "") == "timeout"


def test_sync_client_fails_fast_on_4xx(monkeypatch) -> None:
    client = SyncHttpClient(DEFAULT_CONFIG.http, 0.0)

    class Resp:
        status_code = 403
        text = ""

    monkeypatch.setattr(client.session, "get", lambda *a, **k: Resp())
    with pytest.raises(NonRetryableHttpError):
        client.get_text("https://example.invalid")


def test_parse_core_odds_excludes_live_providers() -> None:
    side = lambda ps, ml: {"close": {"pointSpread": {"american": ps}, "spread": {"american": "-110"},  # noqa: E731
                                     "moneyLine": {"american": ml}},
                           "open": {"pointSpread": {"american": ps}, "moneyLine": {"american": ml}}}
    payload = {"items": [
        {"provider": {"name": "ESPN BET"}, "spread": -4.5, "overUnder": 215.5,
         "homeTeamOdds": side("-4.5", "-175"), "awayTeamOdds": side("+4.5", "+150"),
         "close": {"over": {"american": "-110"}, "under": {"american": "-110"}, "total": {"american": "215.5"}},
         "open": {"total": {"american": "214.5"}}},
        {"provider": {"name": "ESPN Bet - Live Odds"}, "spread": -8.5, "overUnder": 218.5,
         "homeTeamOdds": side("-8.5", "-10000"), "awayTeamOdds": side("+8.5", "+2500")},
    ]}
    rows = espn.parse_core_odds("g1", payload)
    assert len(rows) == 1 and rows[0]["provider"] == "ESPN BET"
    r = rows[0]
    assert (r["spread_close"], r["total_close"], r["home_ml_close"], r["away_ml_close"]) == (-4.5, 215.5, -175, 150)
    assert r["over_odds_close"] == -110 and r["spread_home_odds_close"] == -110
