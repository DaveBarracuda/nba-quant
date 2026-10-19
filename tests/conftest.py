"""Fixtures compartidas: liga sintética pequeña y su matriz de features (scope de sesión)."""

from __future__ import annotations

from dataclasses import replace

import pytest

from nba_quant.config import DEFAULT_CONFIG, EngineConfig
from nba_quant.features.pipeline import NBAAdvancedFeaturePipeline
from nba_quant.synthetic import SyntheticLeague, generate_league


@pytest.fixture(scope="session")
def cfg() -> EngineConfig:
    sim = replace(DEFAULT_CONFIG.sim, n_sims_block=6_000, n_sims_markov=20_000, n_sims_props=500)
    return replace(DEFAULT_CONFIG, sim=sim)


@pytest.fixture(scope="session")
def league() -> SyntheticLeague:
    return generate_league(n_teams=6, n_rounds=4, seed=5)


@pytest.fixture(scope="session")
def pipeline_run(cfg: EngineConfig, league: SyntheticLeague):
    pipe = NBAAdvancedFeaturePipeline(cfg, pbp=league.pbp, games=league.games, player_box=league.player_box)
    feats = pipe.run()
    return pipe, feats
