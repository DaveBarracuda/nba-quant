"""Configuración central del motor.

Todos los umbrales del documento de especificación viven aquí como constantes con nombre,
para que ningún módulo tenga "números mágicos" y para poder recalibrar sin tocar código.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PathsConfig:
    """Rutas del data lake local (DuckDB + Parquet)."""

    root: Path = Path(os.environ.get("NBA_QUANT_HOME", Path.cwd() / "data"))

    @property
    def raw(self) -> Path:
        return self.root / "raw"

    @property
    def lake(self) -> Path:
        return self.root / "lake"

    @property
    def duckdb_file(self) -> Path:
        return self.root / "nba_quant.duckdb"


@dataclass(frozen=True)
class HttpConfig:
    """Cabeceras, límites de tasa y reintentos por fuente."""

    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0 Safari/537.36"
    )
    timeout_sec: float = 30.0
    max_retries: int = 4
    backoff_base_sec: float = 1.5
    espn_min_interval_sec: float = 0.35
    nba_stats_min_interval_sec: float = 1.2
    bref_min_interval_sec: float = 3.5  # B-Ref bloquea a >20 req/min
    odds_api_key_env: str = "ODDS_API_KEY"
    max_concurrency: int = 6


@dataclass(frozen=True)
class GameStateConfig:
    """Definiciones de contexto de juego (garbage time, clutch, guion neutral)."""

    garbage_wp_low: float = 0.02
    garbage_wp_high: float = 0.98
    garbage_margin: int = 20
    garbage_minutes_left: float = 6.0
    low_leverage_wp_low: float = 0.05  # Garbage-Free Net Rating (spec 2)
    low_leverage_wp_high: float = 0.95
    neutral_wp_low: float = 0.20
    neutral_wp_high: float = 0.80
    neutral_exclude_last_minutes: float = 2.0
    clutch_minutes_left: float = 5.0
    clutch_margin: int = 5
    transition_sec: float = 6.0
    early_clock_sec: float = 6.0
    early_shot_tendency_sec: float = 8.0
    late_clock_elapsed_sec: float = 20.0  # últimos 4s de un reloj de 24
    win_prob_sigma_per_game: float = 13.0  # sd del margen final (modelo de Stern)


@dataclass(frozen=True)
class ShotZoneConfig:
    rim_ft: float = 4.0
    paint_ft: float = 10.0
    corner3_y_ft: float = 9.0  # triples con y<=9 pies (línea de fondo) = esquina
    contested_ft: float = 3.5
    open_ft: float = 6.0


@dataclass(frozen=True)
class DecayConfig:
    half_life_games: float = 12.0
    min_games_for_rating: int = 3
    ridge_alpha: float = 25.0
    home_court_pts_per100: float = 2.4


@dataclass(frozen=True)
class KalmanConfig:
    """Máquina de estados bayesiana (spec 4 §2)."""

    league_ortg_prior: float = 114.5
    prior_retention: float = 0.70
    prior_var: float = 16.0  # varianza inicial del estado (pts/100)^2
    obs_sd_per_poss: float = 1.12  # sd de puntos por posesión
    cold_start_games: int = 10
    stabilization_games: int = 20
    cold_start_r_inflation: float = 2.5
    half_life_games: float = 12.0
    injury_q_inflation: float = 4.0  # phi_injury en [3, 5]
    playoff_r_inflation: float = 3.0  # playoffs: rotaciones cortas y series repetidas -> menos peso


@dataclass(frozen=True)
class SimulationConfig:
    """Motor Markov/Monte Carlo (spec 3 y spec 4)."""

    n_sims_markov: int = 100_000
    n_sims_block: int = 50_000
    n_sims_props: int = 1_000
    chunk_size: int = 25_000
    seed: int = 20261015
    scenario_shift: float = 0.20  # Mejor/Peor = ±20% (spec 3); ver advertencia en README
    scenario_weights: tuple[float, float, float] = (0.20, 0.60, 0.20)  # (Mejor, Normal, Peor)
    ot_possession_fraction: float = 5.0 / 48.0
    max_overtimes: int = 8
    cmp_nu: float = 2.2  # sub-dispersión del nº de posesiones (Conway-Maxwell-Poisson)
    garbage_relax_threshold: float = 18.0
    garbage_relax_factor: float = 0.85


@dataclass(frozen=True)
class CleansingConfig:
    """Fase 1 del spec 3: base L5 ponderada y taxonomía de sesgos."""

    l5_weights: tuple[float, ...] = (0.35, 0.25, 0.20, 0.15, 0.05)
    blowout_margin: int = 15
    clutch_margin: int = 5
    weight_blowout: float = 1.00
    weight_clutch: float = 0.95
    weight_luck: float = 0.85
    luck_three_pct_z: float = 1.5
    l5_blend: float = 0.35  # peso de la base L5 frente al estado Kalman


@dataclass(frozen=True)
class MarketConfig:
    ci_z: float = 1.959964
    volatility_k: float = 4.0
    min_edge_to_bet: float = 0.02
    kelly_fraction: float = 0.25


@dataclass(frozen=True)
class EngineConfig:
    paths: PathsConfig = field(default_factory=PathsConfig)
    http: HttpConfig = field(default_factory=HttpConfig)
    game_state: GameStateConfig = field(default_factory=GameStateConfig)
    zones: ShotZoneConfig = field(default_factory=ShotZoneConfig)
    decay: DecayConfig = field(default_factory=DecayConfig)
    kalman: KalmanConfig = field(default_factory=KalmanConfig)
    sim: SimulationConfig = field(default_factory=SimulationConfig)
    cleansing: CleansingConfig = field(default_factory=CleansingConfig)
    market: MarketConfig = field(default_factory=MarketConfig)


DEFAULT_CONFIG = EngineConfig()
