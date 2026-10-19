"""Métricas por equipo-partido (spec 1 §B, §C, §E, §F; spec 2 §A, §D, §H, §I).

Flujo: agregados ofensivos desde posesiones y tiros -> se cruza con los agregados del rival
(que son los defensivos propios) -> ratios. Todas las tasas se calculan como cociente de
sumas (no media de medias) para que el decaimiento posterior pondere por volumen.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from nba_quant.processing.possessions import TERMINAL_STATES

KEY = ["game_id", "team"]


def _sum_where(df: pd.DataFrame, mask: pd.Series, col: str | None, by: list[str]) -> pd.Series:
    vals = mask.astype(float) if col is None else df[col].where(mask, 0.0).astype(float)
    return vals.groupby([df[c] for c in by]).sum()


def aggregate_possessions(poss: pd.DataFrame) -> pd.DataFrame:
    """Sumas ofensivas por (game_id, team) a partir de la tabla de posesiones."""
    p = poss.rename(columns={"offense": "team"})
    by = KEY
    one = pd.Series(True, index=p.index)
    trans, gt, ll = p["is_transition"], p["is_garbage"].astype(bool), p["is_low_leverage_ok"].astype(bool)
    out = {
        "poss": _sum_where(p, one, None, by),
        "pts": _sum_where(p, one, "points", by),
        "fga": _sum_where(p, one, "fga", by), "fgm": _sum_where(p, one, "fgm", by),
        "fg3a": _sum_where(p, one, "fg3a", by), "fg3m": _sum_where(p, one, "fg3m", by),
        "fta": _sum_where(p, one, "fta", by), "ftm": _sum_where(p, one, "ftm", by),
        "tov": _sum_where(p, one, "tov", by), "oreb": _sum_where(p, one, "oreb", by),
        "live_tov": _sum_where(p, p["end_type"] == "live_tov", None, by),
        "dead_tov": _sum_where(p, p["end_type"] == "dead_tov", None, by),
        "trans_poss": _sum_where(p, trans, None, by), "trans_pts": _sum_where(p, trans, "points", by),
        "hc_poss": _sum_where(p, ~trans, None, by), "hc_pts": _sum_where(p, ~trans, "points", by),
        "nogt_poss": _sum_where(p, ~gt, None, by), "nogt_pts": _sum_where(p, ~gt, "points", by),
        "ll_poss": _sum_where(p, ll, None, by), "ll_pts": _sum_where(p, ll, "points", by),
        "clutch_poss": _sum_where(p, p["is_clutch"].astype(bool), None, by),
        "clutch_pts": _sum_where(p, p["is_clutch"].astype(bool), "points", by),
        "neutral_poss": _sum_where(p, p["is_neutral"].astype(bool), None, by),
        "neutral_sec": _sum_where(p, p["is_neutral"].astype(bool), "duration_sec", by),
        "game_sec": _sum_where(p, one, "duration_sec", by),
        "scored_poss": _sum_where(p, p["scored"], None, by),
        "ato_poss": _sum_where(p, p["is_ato"], None, by), "ato_pts": _sum_where(p, p["is_ato"], "points", by),
        "early_poss": _sum_where(p, p["is_early_clock"], None, by),
        "early_pts": _sum_where(p, p["is_early_clock"], "points", by),
        "early8_neutral": _sum_where(p, p["is_early8"] & p["is_neutral"].astype(bool), None, by),
        "post_steal_poss": _sum_where(p, p["after_live_tov"], None, by),
        "post_steal_pts": _sum_where(p, p["after_live_tov"], "points", by),
    }
    for st in TERMINAL_STATES:
        out[f"st_{st}"] = _sum_where(p, p["terminal_state"] == st, None, by)
    for start in ("made", "ft", "dreb", "live_tov", "dead_tov"):
        m = p["start_type"] == start
        out[f"dur_{start}_sum"] = _sum_where(p, m, "duration_sec", by)
        out[f"dur_{start}_n"] = _sum_where(p, m, None, by)
    return pd.DataFrame(out).reset_index()


def aggregate_shots(shots: pd.DataFrame) -> pd.DataFrame:
    """Sumas de selección/calidad de tiro por (game_id, team)."""
    s = shots.drop(columns=["team"], errors="ignore").rename(columns={"offense": "team"})
    by = KEY
    one = pd.Series(True, index=s.index)
    made = s["made"].astype(bool)
    pts = s["shot_value"].where(made, 0).astype(float)
    s = s.assign(_pts=pts)
    out = {
        "sh_fga": _sum_where(s, one, None, by),
        "xpts": _sum_where(s, one, "xpts", by),
        "xefg_w": _sum_where(s, one, "xefg_w", by),
        "efg_w": _sum_where(s, one, "efg_w", by),
        "paint_pts": _sum_where(s, s["is_paint"], "_pts", by),
        "putback_fga": _sum_where(s, s["is_putback"], None, by),
        "putback_pts": _sum_where(s, s["is_putback"], "_pts", by),
        "second_chance_pts": _sum_where(s, s["last_oreb_elapsed"].notna(), "_pts", by),
        "pullup3_fga": _sum_where(s, (s["shot_style"] == "pull_up") & (s["shot_value"] == 3), None, by),
        "cs3_fga": _sum_where(s, (s["shot_style"] == "catch_shoot") & (s["shot_value"] == 3), None, by),
        "assisted_fgm": _sum_where(s, s["assisted"].astype(bool) & made, None, by),
        "late_fga": _sum_where(s, s["is_late_clock"], None, by),
        "late_efg_w": _sum_where(s, s["is_late_clock"], "efg_w", by),
        "late_xefg_w": _sum_where(s, s["is_late_clock"], "xefg_w", by),
        "early_fga": _sum_where(s, s["is_transition"].astype(bool), None, by),
        "early_efg_w": _sum_where(s, s["is_transition"].astype(bool), "efg_w", by),
        "early_xefg_w": _sum_where(s, s["is_transition"].astype(bool), "xefg_w", by),
        "fg3_xfg": _sum_where(s, s["shot_value"] == 3, "xfg", by),
        "rim_xfg": _sum_where(s, s["zone"] == "rim", "xfg", by),
    }
    for zone in ("rim", "paint", "mid", "corner3", "above_break3"):
        out[f"z_{zone}_fga"] = _sum_where(s, s["zone"] == zone, None, by)
        out[f"z_{zone}_fgm"] = _sum_where(s, (s["zone"] == zone) & made, None, by)
    if "defender_distance" in s.columns and s["defender_distance"].notna().any():
        dd = s["defender_distance"]
        for name, m in (("contested", dd <= 3.5), ("open", dd >= 6.0)):
            out[f"{name}_fga"] = _sum_where(s, m, None, by)
            out[f"{name}_efg_w"] = _sum_where(s, m, "efg_w", by)
    return pd.DataFrame(out).reset_index()


def attach_opponent(off: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """Cada fila gana columnas opp_* = agregados ofensivos del rival (= defensa propia)."""
    g = games[["game_id", "home_team", "away_team"]]
    df = off.merge(g, on="game_id", how="left")
    df["opponent"] = np.where(df["team"] == df["home_team"], df["away_team"], df["home_team"])
    df["is_home"] = (df["team"] == df["home_team"]).astype(int)
    num_cols = [c for c in off.columns if c not in KEY]
    opp = off.rename(columns={"team": "opponent", **{c: f"opp_{c}" for c in num_cols}})
    return df.merge(opp, on=["game_id", "opponent"], how="left").drop(columns=["home_team", "away_team"])


def _ratio(n: pd.Series, d: pd.Series, scale: float = 1.0) -> pd.Series:
    return scale * n / d.replace(0, np.nan)


def derive_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Ratios finales por equipo-partido (spec 1 §B-§F)."""
    r = {}
    for side, p in (("", ""), ("opp_", "opp_")):
        poss = df[f"{p}poss"]
        r[f"{side}ortg"] = _ratio(df[f"{p}pts"], poss, 100)
        r[f"{side}efg"] = _ratio(df[f"{p}fgm"] + 0.5 * df[f"{p}fg3m"], df[f"{p}fga"])
        r[f"{side}ts"] = _ratio(df[f"{p}pts"], 2 * (df[f"{p}fga"] + 0.44 * df[f"{p}fta"]))
        r[f"{side}tov_pct"] = _ratio(df[f"{p}tov"], poss)
        r[f"{side}ftr"] = _ratio(df[f"{p}fta"], df[f"{p}fga"])
        r[f"{side}ortg_nogt"] = _ratio(df[f"{p}nogt_pts"], df[f"{p}nogt_poss"], 100)
        r[f"{side}ortg_lowlev"] = _ratio(df[f"{p}ll_pts"], df[f"{p}ll_poss"], 100)
        r[f"{side}ortg_clutch"] = _ratio(df[f"{p}clutch_pts"], df[f"{p}clutch_poss"], 100)
        r[f"{side}trans_freq"] = _ratio(df[f"{p}trans_poss"], poss)
        r[f"{side}trans_ppp"] = _ratio(df[f"{p}trans_pts"], df[f"{p}trans_poss"])
        r[f"{side}hc_ppp"] = _ratio(df[f"{p}hc_pts"], df[f"{p}hc_poss"])
        r[f"{side}scoring_poss_rate"] = _ratio(df[f"{p}scored_poss"], poss)
        r[f"{side}ato_ppp"] = _ratio(df[f"{p}ato_pts"], df[f"{p}ato_poss"])
        r[f"{side}early_clock_ppp"] = _ratio(df[f"{p}early_pts"], df[f"{p}early_poss"])
        r[f"{side}live_tov_rate"] = _ratio(df[f"{p}live_tov"], poss)
        r[f"{side}dead_tov_rate"] = _ratio(df[f"{p}dead_tov"], poss)
        r[f"{side}xefg"] = _ratio(df[f"{p}xefg_w"], df[f"{p}sh_fga"])
        r[f"{side}shot_making"] = _ratio(df[f"{p}efg_w"] - df[f"{p}xefg_w"], df[f"{p}sh_fga"])
        r[f"{side}paint_pts_per100"] = _ratio(df[f"{p}paint_pts"], poss, 100)
        r[f"{side}putback_freq"] = _ratio(df[f"{p}putback_fga"], df[f"{p}oreb"])
        r[f"{side}second_chance_per100"] = _ratio(df[f"{p}second_chance_pts"], poss, 100)
        r[f"{side}pullup3_freq"] = _ratio(df[f"{p}pullup3_fga"], df[f"{p}sh_fga"])
        r[f"{side}assisted_rate"] = _ratio(df[f"{p}assisted_fgm"], df[f"{p}fgm"])
        r[f"{side}late_clock_freq"] = _ratio(df[f"{p}late_fga"], df[f"{p}sh_fga"])
        r[f"{side}late_clock_efg"] = _ratio(df[f"{p}late_efg_w"], df[f"{p}late_fga"])
        r[f"{side}early_clock_efg"] = _ratio(df[f"{p}early_efg_w"], df[f"{p}early_fga"])
        r[f"{side}moreyball_idx"] = _ratio(df[f"{p}z_rim_fga"] + df[f"{p}fg3a"], df[f"{p}sh_fga"])
        for zone in ("rim", "paint", "mid", "corner3", "above_break3"):
            r[f"{side}{zone}_freq"] = _ratio(df[f"{p}z_{zone}_fga"], df[f"{p}sh_fga"])
            r[f"{side}{zone}_fg"] = _ratio(df[f"{p}z_{zone}_fgm"], df[f"{p}z_{zone}_fga"])
        r[f"{side}fg3_pct"] = _ratio(df[f"{p}fg3m"], df[f"{p}fg3a"])
        r[f"{side}fg3_xpct"] = _ratio(df[f"{p}fg3_xfg"], df[f"{p}fg3a"])
        r[f"{side}ft_pct"] = _ratio(df[f"{p}ftm"], df[f"{p}fta"])
    r["drtg"] = r.pop("opp_ortg")
    r["net_rtg"] = r["ortg"] - r["drtg"]
    r["net_rtg_nogt"] = r["ortg_nogt"] - r["opp_ortg_nogt"]
    r["net_rtg_lowlev"] = r["ortg_lowlev"] - r["opp_ortg_lowlev"]
    r["net_rtg_clutch"] = r["ortg_clutch"] - r["opp_ortg_clutch"]
    # Nuestros fallos rebotados por el rival = posesiones propias que terminan en MISS_DREB.
    r["oreb_pct"] = _ratio(df["oreb"], df["oreb"] + df["st_MISS_DREB"])
    r["dreb_pct"] = _ratio(df["opp_st_MISS_DREB"], df["opp_st_MISS_DREB"] + df["opp_oreb"])
    r["opp_oreb_pct"] = 1 - r["dreb_pct"]
    r["pace"] = _ratio(df["poss"], df["game_sec"] + df["opp_game_sec"], 2880)
    r["neutral_pace"] = _ratio(df["neutral_poss"], df["neutral_sec"] + df["opp_neutral_sec"], 2880)
    r["sec_per_poss"] = _ratio(df["game_sec"], df["poss"])
    for start in ("made", "ft", "dreb", "live_tov", "dead_tov"):
        r[f"sec_per_poss_after_{start}"] = _ratio(df[f"dur_{start}_sum"], df[f"dur_{start}_n"])
    r["early8_tendency"] = _ratio(df["early8_neutral"], df["neutral_poss"])
    r["opp_pts_off_live_tov_per100"] = _ratio(df["opp_post_steal_pts"], df["poss"], 100)
    r["live_dead_tov_ratio"] = _ratio(df["live_tov"], df["dead_tov"])
    r["three_luck_def"] = r["opp_fg3_pct"] - r["opp_fg3_xpct"]  # >0 = el rival metió más de lo esperado
    r["three_luck_off"] = r["fg3_pct"] - r["fg3_xpct"]
    r["rim_fg_conceded_vs_exp"] = _ratio(df["opp_z_rim_fgm"] - df["opp_rim_xfg"], df["opp_z_rim_fga"])
    r["shot_making_diff"] = r["shot_making"] - r["opp_shot_making"]
    r["xefg_diff"] = r["xefg"] - r["opp_xefg"]
    if "contested_fga" in df.columns:
        r["contested_efg"] = _ratio(df["contested_efg_w"], df["contested_fga"])
        r["open_efg"] = _ratio(df["open_efg_w"], df["open_fga"])
        r["open_freq"] = _ratio(df["open_fga"], df["sh_fga"])
    # Probabilidades de segmento de Markov (spec 4): por segmento = posesión o rebote ofensivo.
    segments = df["poss"] + df["oreb"]
    for st in TERMINAL_STATES:
        r[f"mk_{st}"] = _ratio(df[f"st_{st}"], segments)
        r[f"mk_def_{st}"] = _ratio(df[f"opp_st_{st}"], df["opp_poss"] + df["opp_oreb"])
    r["mk_OREB"] = _ratio(df["oreb"], segments)
    r["mk_def_OREB"] = _ratio(df["opp_oreb"], df["opp_poss"] + df["opp_oreb"])
    return pd.concat([df, pd.DataFrame(r, index=df.index)], axis=1)
