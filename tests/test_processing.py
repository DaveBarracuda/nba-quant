"""Limpieza PBP, estado de juego y reconstrucción de posesiones sobre jugadas construidas a mano."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nba_quant.config import DEFAULT_CONFIG
from nba_quant.processing.pbp import load_and_clean_pbp, stern_win_probability
from nba_quant.processing.possessions import build_possessions

GS = DEFAULT_CONFIG.game_state


def _ev(seq: int, clock: float, team: str | None, etype: str, **kw: object) -> dict:
    base = {"game_id": "G1", "event_idx": seq, "period": kw.pop("period", 1), "clock_sec": clock, "team": team,
            "event_type": etype, "subtype": kw.pop("subtype", etype), "made": False, "shot_value": 0,
            "shot_distance": np.nan, "x": np.nan, "y": np.nan, "is_offensive_rebound": False, "is_steal": False,
            "is_shooting_foul": False, "ft_num": np.nan, "ft_total": np.nan, "ft_technical": False,
            "ft_flagrant": False, "assisted": False, "shot_style": None, "player_id": "p", "player2_id": None,
            "home_score": 0, "away_score": 0, "home_team": "HOM", "away_team": "AWY"}
    base.update(kw)
    return base


@pytest.fixture()
def tiny_pbp() -> pd.DataFrame:
    rows = [
        _ev(1, 720, "HOM", "jumpball"),
        _ev(2, 700, "HOM", "shot", made=True, shot_value=3),                          # P1 HOM 3PT
        _ev(3, 690, "AWY", "shot", made=True, shot_value=2),                          # P2 AWY and-1
        _ev(4, 690, "HOM", "foul", is_shooting_foul=True),
        _ev(5, 690, "AWY", "free_throw", made=True, shot_value=1, ft_num=1, ft_total=1),
        _ev(6, 670, "HOM", "shot", made=False, shot_value=2),                         # P3 HOM fallo + OREB
        _ev(7, 668, "HOM", "rebound", is_offensive_rebound=True),
        _ev(8, 660, "AWY", "foul", is_shooting_foul=True),
        _ev(9, 660, "HOM", "free_throw", made=False, shot_value=1, ft_num=1, ft_total=2),
        _ev(10, 660, "AWY", "rebound", subtype="Defensive Rebound"),                  # rebote fantasma
        _ev(11, 660, "HOM", "free_throw", made=True, shot_value=1, ft_num=2, ft_total=2),  # fin P3: FT2
        _ev(12, 650, "AWY", "turnover", is_steal=True),                               # P4 AWY TOV vivo
        _ev(14, 645, "HOM", "shot", made=False, shot_value=3),                        # P5 HOM fallo
        _ev(13, 646, "HOM", "timeout"),                                               # fuera de orden (seq)
        _ev(15, 640, "AWY", "rebound", subtype="Defensive Rebound"),
        _ev(16, 0, None, "period_end"),
    ]
    return pd.DataFrame(rows)


def test_possessions_terminal_states_and_points(tiny_pbp: pd.DataFrame) -> None:
    clean = load_and_clean_pbp(tiny_pbp, GS)
    _, poss = build_possessions(clean, GS)
    assert poss["offense"].tolist() == ["HOM", "AWY", "HOM", "AWY", "HOM"]
    assert poss["terminal_state"].tolist() == ["3PT", "AND1_MADE", "FT2", "TOV", "MISS_DREB"]
    assert poss["points"].tolist() == [3, 3, 1, 0, 0]
    assert poss.loc[2, "oreb"] == 1
    assert poss.loc[3, "end_type"] == "live_tov"
    assert poss.loc[4, "start_type"] == "live_tov"


def test_chronological_reorder_and_recalculated_score(tiny_pbp: pd.DataFrame) -> None:
    clean = load_and_clean_pbp(tiny_pbp, GS)
    assert clean["game_sec_elapsed"].is_monotonic_increasing
    last = clean.iloc[-1]
    assert (last["home_score_calc"], last["away_score_calc"]) == (4, 3)


def test_stern_win_probability_properties() -> None:
    wp = stern_win_probability(np.array([0.0, 5.0, 5.0, -3.0]), np.array([2880.0, 2880.0, 60.0, 0.0]), 13.0)
    assert wp[0] == pytest.approx(0.5)
    assert wp[2] > wp[1] > 0.5  # misma ventaja vale más con menos tiempo
    assert wp[3] == 0.0


def test_garbage_time_flag() -> None:
    rows = [_ev(1, 300, "HOM", "shot", period=4, made=True, shot_value=2, home_score=0, away_score=0)]
    df = pd.DataFrame(rows)
    df.loc[0, "home_wp"] = 0.995
    df = pd.concat([df, pd.DataFrame([_ev(2, 290, "AWY", "shot", period=4)])], ignore_index=True)
    clean = load_and_clean_pbp(df, GS)
    assert bool(clean.loc[1, "is_garbage"])  # WP previa (ESPN) fuera de [0.02, 0.98] en el 4º cuarto


def test_lake_upsert_is_idempotent(tmp_path) -> None:
    from nba_quant.config import PathsConfig
    from nba_quant.storage.lake import DataLake

    lake = DataLake(PathsConfig(root=tmp_path))
    df = pd.DataFrame({"game_id": ["a", "b"], "season": [2026, 2026], "home_team": ["X", "Y"]})
    lake.write("games", df)
    lake.write("games", df.assign(home_team=["Z", "Y"]))
    out = lake.read("games")
    assert len(out) == 2 and out.set_index("game_id").loc["a", "home_team"] == "Z"
    con = lake.connect()
    assert con.execute("SELECT COUNT(*) FROM games").fetchone()[0] == 2
