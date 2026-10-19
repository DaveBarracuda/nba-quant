"""Desvigado, cadena de Markov, CMP y recuperación de fuerzas latentes."""

from __future__ import annotations

import numpy as np
import pytest

from nba_quant.config import DEFAULT_CONFIG
from nba_quant.models.devig import american_to_decimal, devig_power, devig_proportional, devig_shin
from nba_quant.models.markov import (LEAGUE_SEGMENT_PROBS, PossessionMarkovEngine, TeamProfile, build_matchup,
                                     cmp_pmf, expected_points_vector, tilt_to_target)


def test_american_to_decimal() -> None:
    assert american_to_decimal(-110) == pytest.approx(1.9091, abs=1e-4)
    assert american_to_decimal(150) == pytest.approx(2.5)
    with pytest.raises(ValueError):
        american_to_decimal(0)


def test_shin_and_power_sum_to_one_and_shade_longshot() -> None:
    dec = np.array([american_to_decimal(-400), american_to_decimal(300)])
    shin, z = devig_shin(dec)
    power, _ = devig_power(dec)
    prop = devig_proportional(dec)
    assert shin.sum() == pytest.approx(1.0) and power.sum() == pytest.approx(1.0)
    assert 0 < z < 0.1
    # Sesgo favorito-longshot: Shin/Power dan al longshot MENOS que la eliminación proporcional.
    assert shin[1] < prop[1] and power[1] < prop[1]


def test_tilt_hits_target_ppp() -> None:
    absorb = np.array([LEAGUE_SEGMENT_PROBS[s] for s in ("3PT", "2PT", "AND1_MADE", "AND1_MISS", "FT1", "FT2",
                                                         "FT3", "TOV", "MISS_DREB")])
    absorb = absorb / absorb.sum()
    for target in (0.95, 1.10, 1.25):
        p = tilt_to_target(absorb, 0.78, target)
        assert p @ expected_points_vector(0.78) == pytest.approx(target, abs=1e-6)


def test_cmp_mean_and_underdispersion() -> None:
    support, pmf = cmp_pmf(99.0, 2.2)
    mean = pmf @ support
    var = pmf @ (support - mean) ** 2
    assert mean == pytest.approx(99.0, abs=0.05)
    assert var < 99.0  # sub-disperso frente a Poisson


def _profile(team: str, off: float, deff: float) -> TeamProfile:
    return TeamProfile(team, 99.0, 0.18, 0.78, dict(LEAGUE_SEGMENT_PROBS), dict(LEAGUE_SEGMENT_PROBS), off, deff)


def test_markov_simulation_matches_expected_margin_and_resolves_ties() -> None:
    cfg = DEFAULT_CONFIG.sim
    home, away = _profile("H", 118.0, 112.0), _profile("A", 112.0, 116.0)
    params = build_matchup(home, away, league_ortg=114.5, hca_per100=2.4)
    sim = PossessionMarkovEngine(cfg).simulate(params, 40_000, seed=1)
    expected = params.lam * (params.home_target_ppp - params.away_target_ppp)
    assert sim.margin.mean() == pytest.approx(expected, abs=0.6)
    assert (sim.margin != 0).all()
    mass = sim.critical_margin_mass()
    assert sum(mass.values()) == pytest.approx(1.0)
    h, a, p = sim.most_likely_score()
    assert 80 < h < 160 and 80 < a < 160 and 0 < p < 0.05
    assert sim.over_prob(sim.total.mean())[0] == pytest.approx(0.5, abs=0.03)


def test_kalman_recovers_synthetic_strengths(pipeline_run, league) -> None:
    _, feats = pipeline_run
    last = feats.reset_index().sort_values("game_date").groupby("team").tail(1).set_index("team")
    truth = league.strengths.set_index("team")
    assert np.corrcoef(last.loc[truth.index, "kf_off"], truth["true_off"])[0, 1] > 0.8
    assert np.corrcoef(last.loc[truth.index, "kf_def"], truth["true_def"])[0, 1] > 0.8
    assert set(last["kf_regime"]) <= {"cold_start", "stabilization", "dynamic"}
