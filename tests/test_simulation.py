"""Pipeline de features completo + capa de simulación y analizador financiero."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nba_quant.simulation.financial import wilson_lower_bound
from nba_quant.simulation.slate import SlateSimulator


def test_feature_matrix_is_clean_and_point_in_time(pipeline_run) -> None:
    _, feats = pipeline_run
    assert list(feats.index.names) == ["season", "game_date", "team"]
    feature_cols = [c for c in feats.columns if not c.startswith("target_")]
    num = feats[feature_cols].select_dtypes("number")
    assert not num.isna().any().any()
    assert np.isfinite(num.to_numpy()).all()
    for col in ("ortg", "drtg", "net_rtg_nogt", "neutral_pace", "trans_ppp", "efg", "xefg", "shot_making",
                "oreb_pct", "dreb_pct", "scoring_poss_rate", "ortg_clutch", "three_luck_def", "ft_luck_def",
                "adj_net_rtg", "kf_net", "rim_freq_oe", "usage_hhi", "rim_fg_allowed_anchor_on"):
        assert col in feats.columns, col
    assert feats["pace"].between(80, 130).all()
    # Point-in-time: el primer partido de cada equipo no puede contener su propio resultado.
    gp = feats.reset_index().sort_values(["team", "game_date", "games_played"]).groupby("team")["games_played"]
    assert (gp.min() == 0).all()
    assert gp.apply(lambda s: s.is_monotonic_increasing and s.is_unique).all()


def test_slate_projection_runs_all_blocks(cfg, pipeline_run, league) -> None:
    pipe, feats = pipeline_run
    fouls = pd.DataFrame({"game_id": league.games["game_id"], "fouls": 40, "fta": 44})
    sim = SlateSimulator(cfg, feats, pipe.games, league.odds, league.officials, fouls, pipe.player_box)
    gid = league.games.sort_values("game_date")["game_id"].iloc[-1]
    proj = sim.project_game(gid)
    assert {"p_home_win_markov", "modal_margin", "likely_score", "best_rae"} <= set(proj.row)
    assert 0 < proj.row["p_home_win_markov"] < 1
    assert "B1_normal" in proj.tear_sheet and "B3_worst" in proj.tear_sheet
    assert "PROYECCIÓN MARKOV" in proj.tear_sheet
    assert not proj.props.empty


def test_market_line_block_reproduces_market_spread(cfg, pipeline_run, league) -> None:
    pipe, feats = pipeline_run
    sim = SlateSimulator(cfg, feats, pipe.games, league.odds)
    gid = league.games.sort_values("game_date")["game_id"].iloc[-2]
    from nba_quant.simulation.monte_carlo import MonteCarloVectorizedCore

    rows = sim.f[sim.f["game_id"] == gid].set_index("is_home")
    ph, pa = sim.team_profile(rows.loc[1]), sim.team_profile(rows.loc[0])
    spread = float(league.odds.set_index("game_id").loc[gid, "spread_close"])
    from nba_quant.simulation.context import DynamicModifierEngine

    dyn = DynamicModifierEngine(cfg.sim)
    sh, sa = dyn.build_scenario(ph.team, ph.off_rating, {}), dyn.build_scenario(pa.team, pa.off_rating, {})
    core = MonteCarloVectorizedCore(cfg.sim, 114.5, cfg.decay.home_court_pts_per100, None)
    mc = core.run(ph, pa, sh, sa, spread)
    fav_margin = mc.blocks["B1_normal"].sim.margin * (1 if mc.favorite == ph.team else -1)
    assert fav_margin.mean() == pytest.approx(abs(spread), abs=1.5)


def test_wilson_lower_bound() -> None:
    assert wilson_lower_bound(0.55, 50_000, 1.96) < 0.55
    assert wilson_lower_bound(0.55, 50_000, 1.96) > 0.54
    assert wilson_lower_bound(0.5, 0, 1.96) == 0.0


def test_context_state_is_point_in_time(cfg, pipeline_run, league) -> None:
    pipe, feats = pipeline_run
    sim = SlateSimulator(cfg, feats, pipe.games, league.odds, league.officials)
    cutoff = pd.Timestamp(sorted(league.games["game_date"].unique())[len(league.games["game_date"].unique()) // 2])
    state = sim.context_state(before=cutoff)
    assert (state.patterns.h["game_date"] < cutoff).all()
    assert len(state.patterns.h) < len(sim.state.patterns.h)


def test_shrink_parts_respects_k_and_caps() -> None:
    from nba_quant.simulation.context import MAX_PATTERN_ADJ, SHRINK_K, DeepHistoricalPatternEngine

    parts = {"hist_h2h": (10.0, 30), "hist_venue": (0.0, 0), "hist_rest": (-1.0, 60), "hist_role": (0.5, 80)}
    off = DeepHistoricalPatternEngine.shrink_parts(parts, 100.0, {k: float("inf") for k in SHRINK_K})
    assert all(v == 0.0 for v in off.values())
    default = DeepHistoricalPatternEngine.shrink_parts(parts, 100.0, {**SHRINK_K, "hist_h2h": 30.0, "hist_rest": 60.0})
    assert default["hist_h2h"] == pytest.approx(min(10.0 * 30 / 60 / 2, MAX_PATTERN_ADJ))
    assert default["hist_rest"] == pytest.approx(-1.0 * 60 / 120 / 2)
    assert DeepHistoricalPatternEngine.shrink_parts(parts, 100.0, SHRINK_K)["hist_role"] == 0.0  # role apagado


def test_backtest_context_mode_runs_and_scores(cfg, pipeline_run, league) -> None:
    pipe, feats = pipeline_run
    sim = SlateSimulator(cfg, feats, pipe.games, league.odds, league.officials)
    base = sim.backtest(min_games_played=6, n_sims=1_000)
    ctx = sim.backtest(min_games_played=6, n_sims=300, mode="context")
    assert len(ctx) == len(base) > 0
    assert ctx["p_home"].between(0, 1).all() and ctx["p_home_cover"].dropna().between(0, 1).all()
    m = ctx.attrs["metrics"]
    assert {"log_loss_spread", "ats_hit_rate", "brier_market", "mae_total_market"} <= set(m)
    with pytest.raises(ValueError):
        sim.backtest(mode="nope")


def test_scenario_grid_dedupes_zero_shift(cfg) -> None:
    from dataclasses import replace

    from nba_quant.models.markov import LEAGUE_SEGMENT_PROBS, STATES, TeamProfile
    from nba_quant.simulation.context import DynamicModifierEngine
    from nba_quant.simulation.monte_carlo import MonteCarloVectorizedCore

    probs = {k: LEAGUE_SEGMENT_PROBS[k] for k in list(STATES) + ["OREB"]}
    team = TeamProfile("A", 99.0, 0.15, 0.78, probs, probs, 115.0, 114.5)
    sim_cfg = replace(cfg.sim, scenario_shift=0.0, n_sims_block=500)
    dyn = DynamicModifierEngine(sim_cfg)
    s = dyn.build_scenario("A", 115.0, {})
    grid = MonteCarloVectorizedCore(sim_cfg, 114.5, 2.4).scenario_grid(team, replace(team, team="B"), s, s)
    assert len(grid) == 9 and len({id(v) for v in grid.values()}) == 1


def test_calibration_grid_scores_train_test(cfg, pipeline_run, league) -> None:
    from nba_quant.simulation import calibration as cal

    pipe, feats = pipeline_run
    sim = SlateSimulator(cfg, feats, pipe.games, league.odds, league.officials)
    base = sim.backtest(min_games_played=6, n_sims=500)
    configs = cal.multiplier_grid((0.05, 0.20), (1.0, float("inf")))
    preds = cal.evaluate_parallel(sim, base["game_id"].tolist(), configs, n_sims=200, min_games_played=6, workers=1)
    assert len(preds) == len(base) * len(configs)
    split = cal.time_split(base)
    table = cal.score_table(preds, base, split)
    assert set(table["half"]) == {"train", "test", "all"}
    assert cal.pick_best(table) in {c.label for c in configs}
    # Mismas semillas por partido: con patrones apagados y shift fijo, repetir da lo mismo.
    again = cal.evaluate_games(sim, base["game_id"].tolist()[:2], configs[:1], 200, 6)
    first = preds[preds["config"] == configs[0].label].set_index("game_id")["p_home"]
    assert again.set_index("game_id")["p_home"].to_dict() == first.loc[again["game_id"]].to_dict()
