"""Tabla por partido que imprime `simulate` (y el log del workflow de GitHub)."""

from __future__ import annotations

import pandas as pd

from nba_quant.cli import matchup_table, render_matchup_table

PREDS = pd.DataFrame({
    "home_team": ["NY", "DET", "SA"], "away_team": ["PHI", "BOS", "OKC"],
    "exp_margin": [4.3, -15.1, -8.4], "exp_total": [227.5, 230.3, 235.4],
    "market_spread_home": [-4.5, 1.5, None], "p_home_win_markov": [0.599, 0.194, 0.316],
})


def test_matchup_table_rows_sorted_by_projected_spread() -> None:
    t = matchup_table(PREDS)
    assert t["Matchup"].tolist() == ["BOS @ DET", "OKC @ SAS", "PHI @ NYK"]
    bos = t.iloc[0]
    assert bos["Vegas_Line"] == "BOS -1.5" and bos["Model_Pick"] == "BOS" and bos["Win_Prob"] == "80.6%"
    assert bos["Proj_Spread"] == "BOS +15.1 pts" and bos["Model_Score"] == "BOS 122.7 – DET 107.6"
    assert bos["Proj_Total"] == "230.3"
    nyk = t.iloc[2]
    assert nyk["Vegas_Line"] == "NYK -4.5" and nyk["Model_Score"] == "PHI 111.6 – NYK 115.9"
    assert t.iloc[1]["Vegas_Line"] == "—"  # sin línea de mercado


def test_render_matchup_table_frames_with_rules() -> None:
    lines = render_matchup_table(PREDS).splitlines()
    assert set(lines[0]) == {"═"} and lines[0] == lines[-1] and len(lines) == 6
    assert lines[1].split() == ["Matchup", "Vegas_Line", "Model_Pick", "Win_Prob", "Proj_Spread", "Model_Score",
                                "Proj_Total"]
