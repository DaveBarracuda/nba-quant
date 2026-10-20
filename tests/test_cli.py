"""Tabla de diferencia de puntos por equipo que imprime `simulate` (y el workflow de GitHub)."""

from __future__ import annotations

import pandas as pd
import pytest

from nba_quant.cli import team_point_diff_table


def test_team_point_diff_table_is_descending_and_mirrors_each_game() -> None:
    preds = pd.DataFrame({
        "home_team": ["BKN", "LAL"], "away_team": ["CHA", "GSW"], "exp_margin": [4.0, -7.0],
        "exp_total": [220.0, 230.0], "market_spread_home": [-3.5, None], "p_home_win_markov": [0.62, 0.27],
    })
    t = team_point_diff_table(preds)
    assert t["equipo"].tolist() == ["GSW", "BKN", "CHA", "LAL"]
    assert t["diferencia proyectada"].tolist() == [7.0, 4.0, -4.0, -7.0]
    bkn = t.set_index("equipo").loc["BKN"]
    assert bkn["pts proyectados"] == 112.0 and bkn["diferencia mercado"] == 3.5
    assert bkn["edge vs mercado"] == pytest.approx(0.5) and bkn["sede"] == "local"
    assert t.set_index("equipo").loc["CHA", "P(ganar)"] == pytest.approx(0.38)
    assert t.set_index("equipo")["diferencia mercado"].isna().sum() == 2  # sin línea en LAL-GSW
