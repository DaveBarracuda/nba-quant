"""Auditoría de fugas de información futura (point-in-time)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from nba_quant.features.pipeline import NBAAdvancedFeaturePipeline
from nba_quant.simulation.bias import PLAYOFF_TOTAL_PRIOR, BiasCalibrator


def _features(cfg, league, games: pd.DataFrame) -> pd.DataFrame:
    ids = set(games["game_id"])
    pipe = NBAAdvancedFeaturePipeline(cfg, pbp=league.pbp[league.pbp["game_id"].isin(ids)], games=games,
                                      player_box=league.player_box[league.player_box["game_id"].isin(ids)])
    return pipe.run().reset_index()


def test_features_invariant_to_future_data(cfg, league, pipeline_run) -> None:
    """Truncamiento: las features anteriores a D no pueden cambiar al añadir partidos >= D."""
    _, full = pipeline_run
    full = full.reset_index()
    dates = sorted(league.games["game_date"].unique())
    cut = dates[int(len(dates) * 0.6)]
    trunc = _features(cfg, league, league.games[league.games["game_date"] < cut])
    key = ["game_id", "team"]
    a = full[full["game_date"] < cut].set_index(key).sort_index()
    b = trunc.set_index(key).sort_index().loc[a.index]
    num = [c for c in a.columns if pd.api.types.is_numeric_dtype(a[c]) and not c.startswith("target_")]
    leaked = [c for c in num if not np.allclose(a[c].to_numpy(float), b[c].to_numpy(float), rtol=1e-9, atol=1e-9)]
    assert leaked == [], f"columnas con fuga de futuro: {leaked}"


def test_bias_calibrator_is_point_in_time_and_learns() -> None:
    dates = pd.date_range("2025-10-21", periods=400, freq="D")
    t = pd.DataFrame({"game_date": dates, "season_type": [2] * 360 + [3] * 40,
                      "hca_obs": 1.0, "exp_total": 230.0,
                      "actual_total": [235.0] * 360 + [215.0] * 40}, index=[f"g{i}" for i in range(400)])
    cal = BiasCalibrator(t, hca_prior=2.4)
    cut = dates[200]
    before = cal.state(cut)
    cal_more = BiasCalibrator(pd.concat([t, t.assign(game_date=t["game_date"] + pd.Timedelta(days=500))]), 2.4)
    assert cal_more.state(cut) == before  # añadir futuro no cambia el estado en `cut`
    assert 1.0 < before.hca_per100 < 2.4  # aprende la ventaja de campo menor
    assert before.total_factor_regular > 1.0  # se anota más de lo esperado
    assert before.total_factor_playoff < before.total_factor_regular  # prior de playoffs
    full = cal.state()
    assert full.total_factor_playoff < full.total_factor_regular * PLAYOFF_TOTAL_PRIOR + 0.01
    assert cal.state(dates[0]).n_games == 0
