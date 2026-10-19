"""Reconstrucción de posesiones y estados terminales de Markov (spec 1 §E, spec 4 §1.A).

Reglas de fin de posesión (convención pbpstats/Oliver):
  * canasta convertida que NO va seguida de and-1,
  * último tiro libre convertido de un viaje (no técnico, no flagrante),
  * rebote defensivo (excepto rebotes "fantasma" tras un TL que no es el último del viaje),
  * pérdida de balón,
  * final de periodo.
Un rebote ofensivo NO termina la posesión: abre un nuevo *segmento* (estado transitorio).

Estado terminal de cada posesión (espacio S del spec 4):
  3PT, 2PT, AND1_MADE, AND1_MISS, FT1, FT2, FT3, TOV, MISS_DREB   (+ OREB transitorio)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from nba_quant.config import GameStateConfig, ShotZoneConfig
from nba_quant.logging_utils import get_logger

log = get_logger("possessions")

TERMINAL_STATES = ("3PT", "2PT", "AND1_MADE", "AND1_MISS", "FT1", "FT2", "FT3", "TOV", "MISS_DREB")
AND1_LOOKAHEAD = 6
CORNER3_MIN_ABS_X_FT = 20.0  # la línea de esquina está a 22 pies laterales del aro


def _other_team(df: pd.DataFrame) -> np.ndarray:
    return np.where(df["team"] == df["home_team"], df["away_team"], df["home_team"])


def flag_and_ones(df: pd.DataFrame) -> pd.Series:
    """Canasta convertida seguida (mismo reloj, mismo equipo) de un viaje de 1 TL no técnico."""
    made_fg = (df["event_type"] == "shot") & df["made"]
    and1 = pd.Series(False, index=df.index)
    for k in range(1, AND1_LOOKAHEAD + 1):
        cond = (
            (df["game_id"].shift(-k) == df["game_id"])
            & (df["event_type"].shift(-k) == "free_throw")
            & (df["ft_total"].shift(-k) == 1)
            & ~df["ft_technical"].shift(-k, fill_value=False).astype(bool)
            & (df["team"].shift(-k) == df["team"])
            & (df["clock_sec"].shift(-k) == df["clock_sec"])
        )
        and1 |= made_fg & cond
    return and1


def mark_possession_ends(df: pd.DataFrame) -> pd.DataFrame:
    """Marca eventos que cierran posesión y el equipo atacante de esa posesión."""
    df = df.sort_values(["game_id", "seq"]).reset_index(drop=True)
    and1 = flag_and_ones(df)
    is_ft = df["event_type"] == "free_throw"
    ft_regular = is_ft & ~df["ft_technical"] & ~df["ft_flagrant"]
    last_ft = ft_regular & (df["ft_num"] == df["ft_total"])
    # Rebote defensivo "fantasma" tras un TL que no es el último del viaje (ESPN lo registra).
    prev_play = df[~df["is_admin"]].groupby("game_id")["event_type"].shift(1).reindex(df.index).ffill()
    prev_ft_num = df["ft_num"].where(is_ft).groupby(df["game_id"]).ffill()
    prev_ft_tot = df["ft_total"].where(is_ft).groupby(df["game_id"]).ffill()
    phantom = (prev_play == "free_throw") & (prev_ft_num < prev_ft_tot)
    dreb = (df["event_type"] == "rebound") & ~df["is_offensive_rebound"] & ~phantom

    end_made = (df["event_type"] == "shot") & df["made"] & ~and1
    end_ft = last_ft & df["made"]
    end_tov = df["event_type"] == "turnover"
    end_period = df["event_type"] == "period_end"
    is_end = end_made | end_ft | dreb | end_tov | end_period

    offense = np.where(dreb, _other_team(df), df["team"])
    offense = np.where(end_period, None, offense)
    end_type = np.select(
        [end_made, end_ft, dreb, end_tov & df["is_steal"], end_tov, end_period],
        ["made", "ft", "dreb", "live_tov", "dead_tov", "period_end"], default=None,
    )
    df = df.assign(
        is_and1_shot=and1, is_last_ft=last_ft, is_poss_end=is_end,
        poss_end_offense=offense, poss_end_type=end_type, is_oreb=(df["event_type"] == "rebound") & df["is_offensive_rebound"],
    )
    # Cada evento pertenece a la posesión que termina en el próximo evento final (inclusive).
    df["poss_no"] = df.groupby("game_id")["is_poss_end"].cumsum() - df["is_poss_end"].astype(int)
    return df


def _possession_offense(df: pd.DataFrame) -> pd.Series:
    """Ataque de cada posesión: el del evento final; si terminó por fin de periodo, el del
    primer tiro/pérdida/TL dentro de la posesión."""
    key = ["game_id", "poss_no"]
    by_end = df.loc[df["is_poss_end"]].set_index(key)["poss_end_offense"]
    actions = df[df["event_type"].isin(["shot", "turnover", "free_throw"])]
    by_action = actions.groupby(key)["team"].first()
    return by_end.where(by_end.notna(), by_action.reindex(by_end.index)).combine_first(by_action)


def classify_terminal_state(df: pd.DataFrame) -> pd.Series:
    """Estado terminal por posesión a partir de la última 'acción' (tiro, último TL, pérdida)."""
    key = ["game_id", "poss_no"]
    act = df[(df["event_type"].isin(["shot", "turnover"])) | df["is_last_ft"]]
    last = act.groupby(key).tail(1).set_index(key)
    # ¿El último TL viene de un and-1? (hay canasta and-1 en la misma posesión)
    and1_poss = df[df["is_and1_shot"]].groupby(key).size().reindex(last.index).fillna(0) > 0
    ft_total = last["ft_total"].fillna(0)
    is_ft = last["event_type"] == "free_throw"
    is_shot = last["event_type"] == "shot"
    state = np.select(
        [
            last["event_type"] == "turnover",
            is_ft & and1_poss & last["made"], is_ft & and1_poss & ~last["made"],
            is_ft & (ft_total >= 3), is_ft & (ft_total == 2), is_ft,
            is_shot & last["made"] & (last["shot_value"] == 3), is_shot & last["made"],
            is_shot & ~last["made"],
        ],
        ["TOV", "AND1_MADE", "AND1_MISS", "FT3", "FT2", "FT1", "3PT", "2PT", "MISS_DREB"],
        default="MISS_DREB",
    )
    return pd.Series(state, index=last.index, name="terminal_state")


def build_possessions(df: pd.DataFrame, gs: GameStateConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve (eventos con poss_no/offense, tabla de posesiones)."""
    df = mark_possession_ends(df)
    key = ["game_id", "poss_no"]
    offense = _possession_offense(df).rename("offense")
    df = df.join(offense, on=key)
    df["defense"] = np.where(df["offense"] == df["home_team"], df["away_team"], df["home_team"])
    df.loc[df["offense"].isna(), "defense"] = None

    plays = df[~df["is_admin"] | (df["event_type"] == "timeout")]
    g = plays.groupby(key, sort=False)
    is_off = plays["team"] == plays["offense"]
    shots = plays["event_type"].eq("shot") & is_off
    fts = plays["event_type"].eq("free_throw") & is_off & ~plays["ft_technical"]
    action_mask = plays["event_type"].isin(["shot", "turnover", "free_throw"]) | plays["is_shooting_foul"].fillna(False)
    first_action = plays["game_sec_elapsed"].where(action_mask).groupby([plays["game_id"], plays["poss_no"]]).min()
    timeout_t = plays["game_sec_elapsed"].where(plays["event_type"] == "timeout").groupby(
        [plays["game_id"], plays["poss_no"]]).min()
    pts_off = (plays["points"] * (plays["scoring_team"] == plays["offense"])).groupby(
        [plays["game_id"], plays["poss_no"]]).sum()

    poss = pd.DataFrame(
        {
            "offense": g["offense"].first(),
            "defense": g["defense"].first(),
            "home_team": g["home_team"].first(),
            "away_team": g["away_team"].first(),
            "period": g["period"].first(),
            "end_elapsed": g["game_sec_elapsed"].max(),
            "first_event_elapsed": g["game_sec_elapsed"].min(),
            "first_action_elapsed": first_action,
            "points": pts_off,
            "fga": shots.groupby([plays["game_id"], plays["poss_no"]]).sum(),
            "fgm": (shots & plays["made"]).groupby([plays["game_id"], plays["poss_no"]]).sum(),
            "fg3a": (shots & (plays["shot_value"] == 3)).groupby([plays["game_id"], plays["poss_no"]]).sum(),
            "fg3m": (shots & (plays["shot_value"] == 3) & plays["made"]).groupby([plays["game_id"], plays["poss_no"]]).sum(),
            "fta": fts.groupby([plays["game_id"], plays["poss_no"]]).sum(),
            "ftm": (fts & plays["made"]).groupby([plays["game_id"], plays["poss_no"]]).sum(),
            "oreb": (plays["is_oreb"] & is_off).groupby([plays["game_id"], plays["poss_no"]]).sum(),
            "tov": (plays["event_type"].eq("turnover") & is_off).groupby([plays["game_id"], plays["poss_no"]]).sum(),
            "end_type": g["poss_end_type"].last(),
            "wp_home_start": g["wp_home"].first(),
            "margin_home_start": g["home_margin_pre"].first(),
            "is_garbage": g["is_garbage"].first(),
            "is_clutch": g["is_clutch"].first(),
            "is_neutral": g["is_neutral"].first(),
            "is_low_leverage_ok": g["is_low_leverage_ok"].first(),
            "timeout_elapsed": timeout_t,
        }
    )
    for opt in ("off_lineup", "def_lineup"):
        if opt in plays.columns:
            poss[opt] = g[opt].first()
    poss = poss[poss["offense"].notna()].copy()
    poss = poss.join(classify_terminal_state(df))
    # Posesiones sin acción (p.ej. bocina de fin de cuarto) no cuentan.
    poss = poss[poss["first_action_elapsed"].notna() | (poss["points"] > 0)]
    poss = poss.reset_index()

    gp = poss.groupby("game_id", sort=False)
    prev_end = gp["end_elapsed"].shift(1)
    prev_type = gp["end_type"].shift(1)
    new_period = gp["period"].shift(1) != poss["period"]
    period_start = np.where(poss["period"] > 4, 2880 + (poss["period"] - 5) * 300, (poss["period"] - 1) * 720)
    poss["start_elapsed"] = np.where(new_period | prev_end.isna(), period_start, prev_end)
    poss["start_type"] = np.where(new_period | prev_type.isna(), "period_start", prev_type)
    poss["duration_sec"] = (poss["end_elapsed"] - poss["start_elapsed"]).clip(lower=0)
    poss["sec_to_first_action"] = (poss["first_action_elapsed"] - poss["start_elapsed"]).clip(lower=0)
    poss["is_transition"] = poss["sec_to_first_action"] <= gs.transition_sec
    poss["is_early_clock"] = poss["sec_to_first_action"] <= gs.early_clock_sec
    poss["is_early8"] = poss["sec_to_first_action"] <= gs.early_shot_tendency_sec
    poss["is_ato"] = poss["timeout_elapsed"].notna() & (
        poss["timeout_elapsed"] <= poss["first_action_elapsed"].fillna(np.inf))
    poss["scored"] = poss["points"] > 0
    poss["terminal_state"] = poss["terminal_state"].fillna("MISS_DREB")
    # Pérdida viva del rival justo antes => posesión tras robo (para puntos de contraataque).
    poss["after_live_tov"] = poss["start_type"] == "live_tov"
    log.info("Posesiones: %d (%.1f por equipo-partido)", len(poss),
             len(poss) / max(1, poss.groupby(["game_id", "offense"]).ngroups))
    return df, poss


def build_shots(df: pd.DataFrame, poss: pd.DataFrame, zones: ShotZoneConfig, gs: GameStateConfig) -> pd.DataFrame:
    """Tabla de tiros de campo con zona, contexto de posesión y reloj de tiro aproximado."""
    shots = df[(df["event_type"] == "shot") & (df["team"] == df["offense"])].copy()
    if shots.empty:
        return shots
    # Reloj de tiro: segundos desde el inicio de posesión o el último rebote ofensivo.
    resets = df["game_sec_elapsed"].where(df["is_oreb"])
    df_reset = resets.groupby([df["game_id"], df["poss_no"]]).ffill()
    shots["last_oreb_elapsed"] = df_reset.reindex(shots.index)
    pinfo = poss.set_index(["game_id", "poss_no"])[["start_elapsed", "is_transition", "start_type", "is_ato"]]
    shots = shots.join(pinfo, on=["game_id", "poss_no"])
    clock_start = shots[["start_elapsed", "last_oreb_elapsed"]].max(axis=1)
    shots["shot_clock_elapsed"] = (shots["game_sec_elapsed"] - clock_start).clip(lower=0)
    shots["is_late_clock"] = shots["shot_clock_elapsed"] >= gs.late_clock_elapsed_sec
    shots["is_putback"] = (shots["shot_style"] == "putback") | (
        shots["last_oreb_elapsed"].notna() & ((shots["game_sec_elapsed"] - shots["last_oreb_elapsed"]) <= 3))
    dist = shots["shot_distance"]
    is3 = shots["shot_value"] == 3
    corner = is3 & (shots["x"].abs() >= CORNER3_MIN_ABS_X_FT) & (shots["y"] <= zones.corner3_y_ft)
    shots["zone"] = np.select(
        [~is3 & (dist <= zones.rim_ft), ~is3 & (dist <= zones.paint_ft), ~is3, corner],
        ["rim", "paint", "mid", "corner3"], default="above_break3",
    )
    shots["is_paint"] = shots["zone"].isin(["rim", "paint"])
    shots["angle_deg"] = np.degrees(np.arctan2(shots["x"].abs(), shots["y"].clip(lower=0.1)))
    return shots.reset_index(drop=True)
