"""Ingesta y limpieza Play-by-Play (spec 1 §A).

- Reloj de partido continuo, puntos por evento derivados del marcador (robusto a errores de etiqueta).
- Win probability: la de ESPN cuando existe; si no, modelo de Stern (margen ~ N(0, σ·sqrt(t))).
- Etiquetas de contexto: garbage time, clutch, guion neutral, filtro low-leverage.
- Filtro de eventos administrativos (se hace DESPUÉS de usar timeouts/subs para ATO y lineups).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from nba_quant.config import GameStateConfig
from nba_quant.logging_utils import get_logger

log = get_logger("pbp")

REG_PERIOD_SEC = 720.0
OT_PERIOD_SEC = 300.0
REG_GAME_SEC = 4 * REG_PERIOD_SEC

ADMIN_EVENT_TYPES = ("timeout", "review", "substitution", "period_end", "jumpball", "other")
# Subtipos que no implican posesión efectiva (p.ej. "No Turnover", técnicos sin posesión).
NON_PLAY_SUBTYPES = ("No Turnover",)

REQUIRED_COLUMNS = (
    "game_id", "event_idx", "period", "clock_sec", "team", "event_type", "made", "shot_value",
    "home_score", "away_score", "home_team", "away_team",
)


def validate_schema(pbp: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in pbp.columns]
    if missing:
        raise ValueError(f"PBP sin columnas requeridas: {missing}")


def add_game_clock(pbp: pd.DataFrame) -> pd.DataFrame:
    """Segundos transcurridos y restantes (de regulación / del periodo) para cada evento."""
    period = pbp["period"].to_numpy()
    clock = pbp["clock_sec"].fillna(0).to_numpy()
    is_ot = period > 4
    elapsed = np.where(
        is_ot,
        REG_GAME_SEC + (period - 5) * OT_PERIOD_SEC + (OT_PERIOD_SEC - clock),
        (period - 1) * REG_PERIOD_SEC + (REG_PERIOD_SEC - clock),
    )
    # Tiempo restante "de partido" para WP: en OT se usa el reloj del OT.
    remaining = np.where(is_ot, clock, (4 - period) * REG_PERIOD_SEC + clock)
    return pbp.assign(game_sec_elapsed=elapsed, game_sec_remaining=remaining)


def chronological_order(pbp: pd.DataFrame) -> pd.DataFrame:
    """ESPN inserta correcciones tardías con sequenceNumber fuera de orden: se ordena por
    (periodo, tiempo transcurrido, secuencia) y se renumera `seq` cronológicamente."""
    df = pbp.sort_values(["game_id", "period", "game_sec_elapsed", "event_idx"], kind="stable")
    return df.assign(seq=df.groupby("game_id").cumcount()).reset_index(drop=True)


def add_points(pbp: pd.DataFrame) -> pd.DataFrame:
    """Puntos por evento desde la etiqueta (tiro/TL anotado) y marcador recalculado acumulando.

    El marcador publicado por ESPN puede venir desfasado en eventos insertados tarde, por eso
    no se usan sus diferencias; sí se usa el marcador final para validar (log de discrepancias).
    """
    is_score = pbp["made"].astype(bool) & pbp["event_type"].isin(["shot", "free_throw"])
    pts = np.where(is_score, np.where(pbp["event_type"] == "shot", pbp["shot_value"], 1), 0).astype(int)
    home_pts = np.where(pbp["team"] == pbp["home_team"], pts, 0)
    away_pts = np.where(pbp["team"] == pbp["away_team"], pts, 0)
    g = pbp["game_id"]
    home_cum = pd.Series(home_pts, index=pbp.index).groupby(g).cumsum()
    away_cum = pd.Series(away_pts, index=pbp.index).groupby(g).cumsum()
    margin_after = home_cum - away_cum
    margin_before = margin_after - (home_pts - away_pts)
    final_pub = pbp.groupby("game_id")[["home_score", "away_score"]].max()
    final_calc = pd.DataFrame({"h": home_cum, "a": away_cum, "game_id": g}).groupby("game_id")[["h", "a"]].last()
    diff = (final_pub["home_score"] - final_calc["h"]).abs() + (final_pub["away_score"] - final_calc["a"]).abs()
    if (diff > 0).any():
        log.warning("Marcador recalculado difiere del publicado en %d partidos (máx %d pts)",
                    int((diff > 0).sum()), int(diff.max()))
    return pbp.assign(
        points=pts,
        scoring_team=np.where(pts > 0, pbp["team"], None),
        home_score_calc=home_cum.to_numpy(),
        away_score_calc=away_cum.to_numpy(),
        home_margin=margin_after.to_numpy(),
        home_margin_pre=margin_before.to_numpy(),
    )


def stern_win_probability(margin: np.ndarray, sec_remaining: np.ndarray, sigma_game: float) -> np.ndarray:
    """P(local gana) con margen como paseo aleatorio: Φ(m / (σ·sqrt(t/T)))."""
    frac = np.clip(sec_remaining / REG_GAME_SEC, 1e-4, None)
    z = margin / (sigma_game * np.sqrt(frac))
    wp = norm.cdf(z)
    # Con el reloj a cero el resultado es determinista (empate -> 0.5 hasta OT).
    done = sec_remaining <= 0
    return np.where(done, np.where(margin > 0, 1.0, np.where(margin < 0, 0.0, 0.5)), wp)


def add_game_state(pbp: pd.DataFrame, cfg: GameStateConfig) -> pd.DataFrame:
    """WP (ESPN o modelo), garbage time, clutch, neutral y low-leverage por evento (estado PRE-evento)."""
    model_wp = stern_win_probability(
        pbp["home_margin_pre"].to_numpy(float), pbp["game_sec_remaining"].to_numpy(float),
        cfg.win_prob_sigma_per_game,
    )
    if "home_wp" in pbp.columns:
        # La WP de ESPN es post-jugada: la desplazamos un evento para tener el estado previo.
        espn_pre = pbp.groupby("game_id", sort=False)["home_wp"].shift(1)
        wp = espn_pre.astype(float).fillna(pd.Series(model_wp, index=pbp.index))
    else:
        wp = pd.Series(model_wp, index=pbp.index)
    wp = wp.clip(0, 1)
    period = pbp["period"]
    clock = pbp["clock_sec"].fillna(0)
    abs_margin = pbp["home_margin_pre"].abs()
    late = period >= 4
    garbage = late & (
        (wp < cfg.garbage_wp_low) | (wp > cfg.garbage_wp_high)
        | ((abs_margin >= cfg.garbage_margin) & (clock < cfg.garbage_minutes_left * 60))
    )
    clutch = late & (clock <= cfg.clutch_minutes_left * 60) & (abs_margin <= cfg.clutch_margin)
    neutral = wp.between(cfg.neutral_wp_low, cfg.neutral_wp_high) & ~(
        late & (clock <= cfg.neutral_exclude_last_minutes * 60)
    )
    low_lev_ok = wp.between(cfg.low_leverage_wp_low, cfg.low_leverage_wp_high)
    return pbp.assign(
        wp_home=wp.to_numpy(), is_garbage=garbage.to_numpy(), is_clutch=clutch.to_numpy(),
        is_neutral=neutral.to_numpy(), is_low_leverage_ok=low_lev_ok.to_numpy(),
    )


def load_and_clean_pbp(pbp: pd.DataFrame, cfg: GameStateConfig, seasons: list[int] | None = None) -> pd.DataFrame:
    """Paso A del pipeline: valida, ordena, enriquece. Mantiene eventos administrativos marcados
    con `is_admin` porque timeouts (ATO) y sustituciones (lineups) se necesitan aguas abajo;
    `drop_admin_events` los elimina una vez usados."""
    validate_schema(pbp)
    df = pbp
    if seasons is not None and "season" in df.columns:
        df = df[df["season"].isin(seasons)]
    df = df[~df.get("subtype", pd.Series("", index=df.index)).isin(NON_PLAY_SUBTYPES)]
    df = df.sort_values(["game_id", "event_idx"]).reset_index(drop=True)
    for col, default in (("ft_technical", False), ("ft_flagrant", False), ("is_steal", False),
                         ("is_offensive_rebound", False), ("assisted", False), ("is_shooting_foul", False)):
        if col not in df.columns:
            df[col] = default
        df[col] = df[col].fillna(default).astype(bool)
    df = add_game_clock(df)
    df = chronological_order(df)
    df = add_points(df)
    df = add_game_state(df, cfg)
    df["is_admin"] = df["event_type"].isin(ADMIN_EVENT_TYPES)
    df["opponent"] = np.where(df["team"] == df["home_team"], df["away_team"],
                              np.where(df["team"] == df["away_team"], df["home_team"], None))
    log.info("PBP limpio: %d eventos, %d partidos, %.1f%% garbage",
             len(df), df["game_id"].nunique(), 100 * df["is_garbage"].mean())
    return df


def drop_admin_events(pbp: pd.DataFrame) -> pd.DataFrame:
    return pbp[~pbp["is_admin"]].reset_index(drop=True)
