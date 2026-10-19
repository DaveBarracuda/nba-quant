"""Conexión con el NBA Odds Tracker: lector SQLite (sólo lectura) y análisis de movimiento/WR."""

from __future__ import annotations

import sqlite3
import subprocess

import numpy as np
import pandas as pd
import pytest

from nba_quant.ledger import ledger_rows, write_ledger
from nba_quant.publish import publish_ledger
from nba_quant.integrations.odds_tracker import OddsTrackerReader, closing_line, match_games
from nba_quant.simulation.market_moves import (build_snapshots, first_snapshot_picks, model_vs_market_drift,
                                               pick_table, summarize)

SCHEMA = """
CREATE TABLE quotes (run_ts TEXT, event_id TEXT, commence_time TEXT, home TEXT, away TEXT,
                     book TEXT, market TEXT, outcome TEXT, point REAL, price INTEGER);
CREATE TABLE splits (run_ts TEXT, away TEXT, home TEXT, market TEXT, tickets_pct REAL, money_pct REAL, num_bets INTEGER);
CREATE TABLE alerts (signature TEXT, run_ts TEXT, kind TEXT, severity TEXT, event_id TEXT, book TEXT,
                     market TEXT, message TEXT);
"""
TIP = "2026-10-21T23:30:00Z"
FINAL = pd.DataFrame({"game_id": ["G1"], "home_score": [110], "away_score": [104]})


def _quotes(ts: str, spread_home: float, total: float, ml_home: int, ml_away: int) -> list[tuple]:
    base = ("E1", TIP, "Brooklyn Nets", "Charlotte Hornets", "draftkings")
    return [
        (ts, *base, "spreads", "home", spread_home, -110), (ts, *base, "spreads", "away", -spread_home, -110),
        (ts, *base, "totals", "over", total, -110), (ts, *base, "totals", "under", total, -110),
        (ts, *base, "h2h", "home", None, ml_home), (ts, *base, "h2h", "away", None, ml_away),
    ]


@pytest.fixture()
def tracker_db(tmp_path):
    db = tmp_path / "odds.sqlite3"
    con = sqlite3.connect(db)
    con.executescript(SCHEMA)
    rows = (_quotes("2026-10-20T15:00:00+00:00", -3.5, 220.5, -160, 135)
            + _quotes("2026-10-21T20:00:00+00:00", -5.5, 218.5, -220, 180))
    con.executemany("INSERT INTO quotes VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
    con.execute("INSERT INTO splits VALUES ('2026-10-21T20:00:00+00:00','Charlotte Hornets','Brooklyn Nets',"
                "'spreads', 70.0, 55.0, 1000)")
    con.execute("INSERT INTO alerts VALUES ('s1','2026-10-21T19:00:00+00:00','STEAM','high','E1','draftkings',"
                "'spreads','steam')")
    con.commit()
    con.close()
    return db


def test_reader_lines_events_and_matching(tracker_db) -> None:
    r = OddsTrackerReader(tracker_db)
    ev = r.events()
    assert ev.loc[0, ["home_team", "away_team"]].tolist() == ["BKN", "CHA"]
    assert ev.loc[0, "us_date"] == pd.Timestamp("2026-10-21")
    lines = r.lines()
    assert lines[lines["market"] == "spread"]["value"].tolist() == [-3.5, -5.5]
    ml = lines[lines["market"] == "ml"]["value"].iloc[0]
    assert 0.5 < ml < 0.65  # local favorito, sin vig
    games = pd.DataFrame({"game_id": ["G1"], "game_date": ["2026-10-21"], "home_team": ["BKN"], "away_team": ["CHA"]})
    assert match_games(ev, games)["game_id"].tolist() == ["G1"]
    assert closing_line(lines, "E1", "spread", pd.Timestamp(TIP))["value"] == -5.5
    assert r.alerts()["market"].tolist() == ["spread"] and r.splits()["market"].tolist() == ["spread"]


def _snap(tracker_db, margin: float, total: float, p_home: float, ts: str = "2026-10-20T16:00:00+00:00"):
    r = OddsTrackerReader(tracker_db)
    ev = r.events().assign(game_id="G1")
    proj = pd.DataFrame({"game_id": ["G1"], "model_margin": [margin], "model_total": [total], "model_p_home": [p_home]})
    return build_snapshots(proj, ev, r.lines(), pd.Timestamp(ts), "test"), r


def test_pick_moves_toward_and_against_model_and_grading(tracker_db) -> None:
    # Modelo: local por 7 (mercado -3.5 -> pick local), total 215 (Under 220.5), P local 0.70.
    snaps, r = _snap(tracker_db, 7.0, 215.0, 0.70)
    assert snaps.loc[0, "line_spread"] == -3.5
    picks = pick_table(snaps, r.lines(), FINAL, r.alerts(), r.splits()).set_index("market")
    sp, tt, ml = picks.loc["spread"], picks.loc["total"], picks.loc["ml"]
    assert sp["pick"] == "BKN -3.5" and sp["move_category"] == "a favor" and sp["clv"] == pytest.approx(2.0)
    assert sp["result"] == 1 and sp["units"] == pytest.approx(100 / 110)  # ganó por 6 > 3.5
    assert sp["alert_kinds"] == "STEAM" and sp["public_pct_on_pick"] == 70.0
    assert tt["pick"] == "Under 220.5" and tt["move_category"] == "a favor" and tt["result"] == 1
    assert ml["pick"] == "BKN ML" and ml["move_category"] == "a favor" and ml["result"] == 1
    # Modelo del lado contrario: el mismo movimiento del mercado queda "en contra".
    snaps2, _ = _snap(tracker_db, -2.0, 226.0, 0.40)
    p2 = pick_table(snaps2, r.lines(), FINAL, r.alerts(), r.splits()).set_index("market")
    assert p2.loc["spread", "pick"] == "CHA +3.5" and p2.loc["spread", "move_category"] == "en contra"
    assert p2.loc["spread", "result"] == 0 and p2.loc["total", "move_category"] == "en contra"
    assert p2.loc["spread", "public_pct_on_pick"] == 30.0


def test_pending_first_snapshot_and_summary(tracker_db) -> None:
    late, r = _snap(tracker_db, 9.0, 230.0, 0.8, ts="2026-10-21T21:00:00+00:00")  # tras el último snapshot
    pending = pick_table(late, r.lines(), pd.DataFrame(columns=["game_id", "home_score", "away_score"]))
    assert set(pending["move_category"]) == {"pendiente"} and pending["result"].isna().all()
    snaps, _ = _snap(tracker_db, 7.0, 215.0, 0.7)
    early = pick_table(snaps, r.lines(), FINAL, r.alerts(), r.splits())
    official = first_snapshot_picks(pd.concat([early, pending]))
    assert len(official) == 3 and (official["snapshot_ts"] == snaps.loc[0, "snapshot_ts"]).all()
    s = summarize(official).set_index(["grupo", "valor"])
    assert s.loc[("GENERAL", "todos"), "récord"] == "3-0-0"
    assert s.loc[("movimiento", "a favor"), "WR"] == 1.0
    drift = model_vs_market_drift(pd.concat([snaps, late]))
    assert set(drift["market"]) == {"spread", "total", "ml"} and np.isfinite(drift["gap_last"]).all()


def test_ledger_shows_moves_and_results(tracker_db, tmp_path) -> None:
    snaps, r = _snap(tracker_db, 7.0, 215.0, 0.70)
    official = first_snapshot_picks(pick_table(snaps, r.lines(), FINAL, r.alerts(), r.splits()))
    path = write_ledger(official, summarize(official), tmp_path / "ledger", pd.Timestamp("2026-10-22", tz="UTC"))
    text = path.read_text(encoding="utf-8")
    assert "| GENERAL | todos | 3 | 3 | 3-0-0 | 100.0% |" in text
    assert "| 2026-10-21 | CHA @ BKN | Spread | BKN -3.5 | -3.5 | -5.5 | ▲ a favor | +2.00 | STEAM | 70 | ✅ W |" in text
    assert len(pd.read_csv(tmp_path / "ledger" / "picks.csv")) == 3
    away, _ = _snap(tracker_db, -2.0, 226.0, 0.40)  # pick visitante: líneas desde su lado
    rows = ledger_rows(pick_table(away, r.lines(), FINAL)).set_index("Mercado")
    assert rows.loc["Spread", ["Pick", "Línea pick", "Cierre", "Mercado vs modelo"]].tolist() == [
        "CHA +3.5", "+3.5", "+5.5", "▼ en contra"]
    assert float(rows.loc["ML", "Línea pick"].rstrip("%")) < 50
    empty = write_ledger(official.iloc[0:0], summarize(official.iloc[0:0]), tmp_path / "empty")
    assert "_Sin picks todavía._" in empty.read_text(encoding="utf-8")


def _run(repo, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def test_publish_ledger_commits_only_ledger_and_pushes(tmp_path) -> None:
    remote, repo = tmp_path / "remote.git", tmp_path / "repo"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    for k, v in (("user.name", "t"), ("user.email", "t@t"), ("commit.gpgsign", "false")):
        _run(repo, "config", k, v)
    _run(repo, "remote", "add", "origin", str(remote))
    (repo / "ledger").mkdir()
    (repo / "ledger" / "LEDGER.md").write_text("v1", encoding="utf-8")
    (repo / "other.txt").write_text("x", encoding="utf-8")
    _run(repo, "add", "other.txt")  # en stage pero fuera del ledger: no debe entrar al commit
    assert publish_ledger(repo, repo / "ledger", "2026-10-21") == "publicado"
    assert _run(remote, "log", "--format=%s", "main").strip() == "chore(ledger): picks al 2026-10-21"
    assert _run(remote, "show", "--name-only", "--format=", "main").split() == ["ledger/LEDGER.md"]
    assert publish_ledger(repo, repo / "ledger") == "sin cambios"
    assert publish_ledger(tmp_path / "nogit", tmp_path / "nogit" / "ledger").startswith("error")


def test_reader_fails_clearly_without_db(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        OddsTrackerReader(tmp_path / "missing.sqlite3")
