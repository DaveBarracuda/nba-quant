"""Ajuste por bajas: probabilidad de baja, cruce por nombre, peso por minutos/presencia y RAPM."""

from __future__ import annotations

import pandas as pd
import pytest

from nba_quant.features.availability import absence_impacts, absence_probability, normalize_name


def test_absence_probability_reads_status_and_detail() -> None:
    assert absence_probability("Out", "ruled out for Wednesday") == 1.0
    assert absence_probability("Day-To-Day", "Traore (calf) is listed as doubtful for Wednesday") == 0.75
    assert absence_probability("Day-To-Day", "listed as questionable for Wednesday's game") == 0.5
    assert absence_probability("Day-To-Day", "is listed as probable") == 0.1
    assert absence_probability("Day-To-Day", None) == 0.4
    assert absence_probability("Active", "") == 0.0


def test_normalize_name_ignores_accents_punctuation_and_suffixes() -> None:
    assert normalize_name("Nikola Jokić") == normalize_name("nikola jokic")
    assert normalize_name("Mikel Brown Jr.") == normalize_name("Mikel Brown")
    assert normalize_name("De'Aaron Fox") == normalize_name("DeAaron Fox")


def _box() -> pd.DataFrame:
    """12 partidos de BOS: la estrella (1) juega 36' en todos; el suplente (2) 20' sólo en 5 de
    los últimos 10; el lesionado largo (3) no juega en los últimos 10 (ya está en el rating)."""
    rows = []
    for i in range(12):
        gid, day = f"G{i}", pd.Timestamp("2026-10-20") + pd.Timedelta(days=2 * i)
        rows.append({"game_id": gid, "game_date": day, "team": "BOS", "player_id": "1",
                     "player_name": "Star Player", "minutes": 36.0})
        if i >= 7:
            rows.append({"game_id": gid, "game_date": day, "team": "BOS", "player_id": "2",
                         "player_name": "Bench Guy", "minutes": 20.0})
        if i < 2:
            rows.append({"game_id": gid, "game_date": day, "team": "BOS", "player_id": "3",
                         "player_name": "Long Term", "minutes": 30.0})
    return pd.DataFrame(rows)


RAPM = pd.DataFrame({"player_id": ["1", "2", "3", "9", "10"], "o_rapm": [4.0, 0.0, 3.0, -1.0, -1.0],
                     "d_rapm": [-2.0, 0.0, -1.0, 1.0, 1.0], "poss_on": [5000.0] * 5})
UPCOMING = pd.DataFrame({"game_id": ["NEXT"], "game_date": [pd.Timestamp("2026-11-12")],
                         "home_team": ["BOS"], "away_team": ["TOR"]})


def _injuries(*rows: tuple[str, str, str]) -> pd.DataFrame:
    return pd.DataFrame([{"team": t, "player_name": n, "status": s, "detail": ""} for t, n, s in rows])


def test_star_out_lowers_own_offense_and_raises_opponent_offense() -> None:
    teams, players = absence_impacts(_injuries(("BOS", "Star Player", "Out")), _box(), RAPM, UPCOMING,
                                     replacement=(-1.0, 1.0))
    t = teams.set_index(["game_id", "team"]).loc[("NEXT", "BOS")]
    w = 36.0 / 48.0
    assert t["own_off_adj"] == pytest.approx(w * (-1.0 - 4.0))   # ataque de BOS baja 3.75
    assert t["opp_off_adj"] == pytest.approx(w * (1.0 - -2.0))   # ataque de TOR sube 2.25
    assert players.iloc[0]["player_id"] == "1" and players.iloc[0]["presence"] == 1.0


def test_presence_scales_and_long_absences_are_already_priced() -> None:
    inj = _injuries(("BOS", "Bench Guy", "Out"), ("BOS", "Long Term", "Out"), ("TOR", "Nobody Known", "Out"))
    teams, players = absence_impacts(inj, _box(), RAPM, UPCOMING, replacement=(-1.0, 1.0))
    p = players.set_index("player_name")
    assert p.loc["Bench Guy", "presence"] == 0.5 and p.loc["Bench Guy", "mpg"] == 20.0
    assert p.loc["Long Term", "presence"] == 0.0 and p.loc["Long Term", "own_off_adj"] == 0.0
    assert "Nobody Known" not in p.index  # sin historial en el equipo: no se puede valorar
    bos = teams.set_index("team").loc["BOS"]
    assert bos["own_off_adj"] == pytest.approx(0.5 * 20 / 48 * (-1.0 - 0.0))


def test_questionable_is_weighted_and_empty_inputs_return_empty() -> None:
    inj = pd.DataFrame([{"team": "BOS", "player_name": "Star Player", "status": "Day-To-Day",
                         "detail": "is questionable for Thursday"}])
    teams, _ = absence_impacts(inj, _box(), RAPM, UPCOMING, replacement=(-1.0, 1.0))
    assert teams.iloc[0]["own_off_adj"] == pytest.approx(0.5 * 36 / 48 * -5.0)
    empty_teams, empty_players = absence_impacts(pd.DataFrame(), _box(), RAPM, UPCOMING)
    assert empty_teams.empty and empty_players.empty
