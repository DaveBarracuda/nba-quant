"""Continuidad de plantilla / ΔRAPM y mezcla point-in-time modelo + mercado."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nba_quant.config import DEFAULT_CONFIG
from nba_quant.features.roster import compute_rapm, roster_priors
from nba_quant.models.kalman import TeamStrengthKalman
from nba_quant.models.markov import SimulationResult
from nba_quant.simulation.blend import W_PRIOR, MarketBlender, shift_simulation
from nba_quant.simulation.slate import SlateSimulator


@pytest.fixture(scope="module")
def rapm(pipeline_run) -> pd.DataFrame:
    pipe, _ = pipeline_run
    return compute_rapm(pipe.poss)


def test_rapm_is_finite_and_covers_rotation(rapm, league) -> None:
    starters = league.player_box.loc[league.player_box["starter"], "player_id"].unique()
    assert set(starters) <= set(rapm["player_id"])
    assert np.isfinite(rapm[["o_rapm", "d_rapm"]].to_numpy()).all()
    # Los mejores ataques sintéticos deben tener titulares con o_rapm medio más alto.
    team_o = rapm.assign(team=rapm["player_id"].str[:-1]).groupby("team")["o_rapm"].mean()
    truth = league.strengths.set_index("team")["true_off"]
    assert np.corrcoef(team_o.loc[truth.index], truth)[0, 1] > 0.5


def test_roster_priors_continuity_and_trade(rapm, league) -> None:
    # La liga sintética no reparte 240 minutos por equipo: se escalan para que sean realistas.
    box = league.player_box.assign(
        minutes=lambda d: d["minutes"] * 240.0 / d.groupby(["game_id", "team"])["minutes"].transform("sum"))
    same = box[["team", "player_id"]].drop_duplicates()
    stay = roster_priors(box, rapm, same)
    assert all(v == pytest.approx(1.0) for v in stay.continuity.values())
    assert all(abs(o) < 1.0 and abs(d) < 1.0 for o, d in stay.rapm_delta.values())
    best = rapm[rapm["player_id"].isin(box.loc[box["starter"], "player_id"])].assign(
        net=lambda d: d["o_rapm"] - d["d_rapm"]).nlargest(1, "net")["player_id"].iloc[0]
    src, dst = best[:-1], next(t for t in same["team"].unique() if t != best[:-1])
    traded = same.assign(team=np.where(same["player_id"] == best, dst, same["team"]))
    moved = roster_priors(box, rapm, traded)
    assert moved.continuity[src] < 1.0
    net = {t: o - d for t, (o, d) in moved.rapm_delta.items()}
    assert net[dst] > net[src]


def test_kalman_season_prior_uses_delta_and_continuity() -> None:
    kf = TeamStrengthKalman(DEFAULT_CONFIG.kalman, DEFAULT_CONFIG.decay)
    for t in ("A", "B"):
        kf._state(t).mean = np.array([4.0, -2.0])
    kf.start_season({"A": 1.0, "B": 0.3}, {"A": (0.0, 0.0), "B": (-3.0, 1.0)})
    keep = DEFAULT_CONFIG.kalman.prior_retention
    assert kf.states["A"].mean == pytest.approx(keep * np.array([4.0, -2.0]))
    assert kf.states["B"].mean == pytest.approx(keep * np.array([1.0, -1.0]))
    assert kf.states["B"].cov[0, 0] > kf.states["A"].cov[0, 0]  # menos continuidad = más incertidumbre


def _preds(n: int, truth: str, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    model = rng.normal(0, 6, n)
    market = rng.normal(0, 6, n)
    actual = (model if truth == "model" else market) + rng.normal(0, 3, n)
    return pd.DataFrame({"game_date": pd.date_range("2025-10-21", periods=n, freq="6h"), "exp_margin": model,
                         "exp_total": 225 + model, "market_spread": -market, "market_total": 225 + market,
                         "actual_margin": actual, "actual_total": 225 + actual})


def test_blender_learns_weights_point_in_time() -> None:
    b_mkt, b_mod = MarketBlender(_preds(2000, "market")), MarketBlender(_preds(2000, "model"))
    # Con ~577 partidos efectivos y 150 de prior en 0.3, los pesos quedan cerca de 0 y 1.
    assert b_mkt.state().w_margin < 0.1 and b_mod.state().w_margin > 0.8
    first = MarketBlender(_preds(2000, "market")).state(pd.Timestamp("2025-10-21"))
    assert first.w_margin == W_PRIOR and first.n_games == 0
    cut = pd.Timestamp("2026-01-01")
    base = _preds(2000, "market")
    more = pd.concat([base, base.assign(game_date=base["game_date"] + pd.Timedelta(days=900))])
    assert MarketBlender(more).state(cut) == MarketBlender(base).state(cut)
    ev = b_mkt.evaluate()
    assert ev["p_cover_blend"].between(0, 1).all() and len(ev) == 2000


def test_shift_simulation_moves_means() -> None:
    rng = np.random.default_rng(1)
    sim = SimulationResult(rng.integers(90, 130, 50_000), rng.integers(90, 130, 50_000), np.zeros(50_000, dtype=np.int8))
    out = shift_simulation(sim, 3.3, -5.4, rng)
    assert out.margin.mean() - sim.margin.mean() == pytest.approx(3.3, abs=0.05)
    assert out.total.mean() - sim.total.mean() == pytest.approx(-5.4, abs=0.05)


def test_projection_applies_market_blend(cfg, pipeline_run, league) -> None:
    pipe, feats = pipeline_run
    sim = SlateSimulator(cfg, feats, pipe.games, league.odds, league.officials)
    bt = sim.backtest(min_games_played=4, n_sims=500)
    sim.fit_blender(bt)
    gid = league.games.sort_values("game_date")["game_id"].iloc[-1]
    row = sim.project_game(gid, with_props=False).row
    assert {"blend_w_margin", "blend_shift_margin", "model_margin_raw"} <= set(row)
    assert row["exp_margin"] == pytest.approx(row["model_margin_raw"] + row["blend_shift_margin"], abs=0.3)
