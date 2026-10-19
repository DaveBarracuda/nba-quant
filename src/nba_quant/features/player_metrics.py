"""Métricas que dependen de jugadores y quintetos (spec 1 §C-§D, spec 2 §C, §D, §G, §I).

Todos los "roles" (ancla defensiva, estrella) se determinan *point-in-time*: con datos de
partidos anteriores al que se evalúa, para no filtrar información futura al modelo.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from nba_quant.logging_utils import get_logger

log = get_logger("player_metrics")

FT_PRIOR_PCT = 0.78
FT_PRIOR_WEIGHT = 50.0  # intentos de pseudo-observación hacia la media de liga
MIN_PRIOR_MINUTES = 60.0
FOUL_TROUBLE_LAG_SEC = 60.0


def point_in_time_roles(player_box: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """(game_id, team) -> rim_protector_id, star_id usando sólo partidos previos de la temporada."""
    box = player_box.drop(columns=["season"], errors="ignore").merge(
        games[["game_id", "game_date", "season"]], on="game_id", how="inner")
    box = box.assign(player_id=box["player_id"].astype(str)).sort_values(["game_date", "game_id"])
    grp = box.groupby(["season", "team", "player_id"], sort=False)
    for col in ("minutes", "blk", "pts"):
        box[col] = box[col].fillna(0)
        box[f"cum_{col}"] = grp[col].cumsum() - box[col]  # acumulado ANTES del partido
    box["blk_rate"] = np.where(box["cum_minutes"] >= MIN_PRIOR_MINUTES,
                               box["cum_blk"] / box["cum_minutes"].replace(0, np.nan), np.nan)
    # Fallback de inicio de temporada: pívot titular de este partido / máximo de minutos.
    box["is_c_starter"] = (box["position"].fillna("") == "C") & box["starter"].astype(bool)
    roles = []
    for (gid, team), tb in box.groupby(["game_id", "team"], sort=False):
        if tb["blk_rate"].notna().any():
            rim = tb.loc[tb["blk_rate"].idxmax(), "player_id"]
        elif tb["is_c_starter"].any():
            rim = tb.loc[tb["is_c_starter"], "player_id"].iloc[0]
        else:
            rim = tb.loc[tb["minutes"].idxmax(), "player_id"]
        star = (tb.loc[tb["cum_pts"].idxmax(), "player_id"] if tb["cum_pts"].max() > 0
                else tb.loc[tb["minutes"].idxmax(), "player_id"])
        roles.append({"game_id": gid, "team": team, "rim_protector_id": rim, "star_id": star})
    return pd.DataFrame(roles)


def _in_lineup(lineups: pd.Series, players: pd.Series) -> np.ndarray:
    return np.array([isinstance(lu, str) and isinstance(p, str) and p in lu.split("-")
                     for lu, p in zip(lineups, players)], dtype=bool)


def rim_protection(shots: pd.DataFrame, roles: pd.DataFrame) -> pd.DataFrame:
    """Defensa del aro (<=4 pies) con el ancla en pista vs en el banco, por equipo defensor."""
    if "def_lineup" not in shots.columns or shots["def_lineup"].isna().all():
        return pd.DataFrame(columns=["game_id", "team"])
    rim = shots[shots["zone"] == "rim"].merge(
        roles.rename(columns={"team": "defense"})[["game_id", "defense", "rim_protector_id"]],
        on=["game_id", "defense"], how="left")
    on = _in_lineup(rim["def_lineup"], rim["rim_protector_id"])
    made = rim["made"].astype(float).to_numpy()
    k = [rim["game_id"], rim["defense"]]
    out = pd.DataFrame({
        "rim_fga_anchor_on": pd.Series(on.astype(float), index=rim.index).groupby(k).sum(),
        "rim_fgm_anchor_on": pd.Series(made * on, index=rim.index).groupby(k).sum(),
        "rim_fga_anchor_off": pd.Series((~on).astype(float), index=rim.index).groupby(k).sum(),
        "rim_fgm_anchor_off": pd.Series(made * ~on, index=rim.index).groupby(k).sum(),
    })
    out.index.names = ["game_id", "team"]
    return out.reset_index()


def star_on_off(poss: pd.DataFrame, roles: pd.DataFrame) -> pd.DataFrame:
    """Puntos/posesiones con y sin la estrella en pista, en ataque y en defensa (On/Off)."""
    if "off_lineup" not in poss.columns or poss["off_lineup"].isna().all():
        return pd.DataFrame(columns=["game_id", "team"])
    r = roles[["game_id", "team", "star_id"]]

    def agg(team_col: str, lineup_col: str, prefix: str) -> pd.DataFrame:
        f = poss.merge(r.rename(columns={"team": team_col}), on=["game_id", team_col], how="left")
        on = pd.Series(_in_lineup(f[lineup_col], f["star_id"]), index=f.index)
        k = [f["game_id"], f[team_col]]
        pts = f["points"].astype(float)
        return pd.DataFrame({
            f"{prefix}_poss_on": on.astype(float).groupby(k).sum(),
            f"{prefix}_pts_on": pts.where(on, 0.0).groupby(k).sum(),
            f"{prefix}_poss_off": (~on).astype(float).groupby(k).sum(),
            f"{prefix}_pts_off": pts.where(~on, 0.0).groupby(k).sum(),
        })

    off = agg("offense", "off_lineup", "star_o")
    dfn = agg("defense", "def_lineup", "star_d")
    off.index.names = dfn.index.names = ["game_id", "team"]
    return off.join(dfn, how="outer").fillna(0).reset_index()


def player_usage(events: pd.DataFrame, poss: pd.DataFrame) -> pd.DataFrame:
    """Jugador-partido: USG% y True Usage = (FGA + viajes TL + TOV + AST) / posesiones en pista."""
    if "off_lineup" not in poss.columns or poss["off_lineup"].isna().all():
        return pd.DataFrame()
    idx = ["game_id", "team", "player_id"]
    on = poss[["game_id", "offense", "off_lineup"]].dropna().rename(columns={"offense": "team"})
    on = on.assign(player_id=on["off_lineup"].str.split("-")).explode("player_id")
    on_poss = on.groupby(idx).size().rename("on_poss")
    ev = events[events["team"] == events["offense"]].assign(player_id=lambda d: d["player_id"].astype(str))
    is_ft = (ev["event_type"] == "free_throw") & ~ev["ft_technical"]
    flags = pd.DataFrame({
        "fga": (ev["event_type"] == "shot").astype(float),
        "ft_trips": (is_ft & (ev["ft_num"] == 1)).astype(float),
        "fta": is_ft.astype(float),
        "tov": (ev["event_type"] == "turnover").astype(float),
    })
    stats = flags.groupby([ev["game_id"], ev["team"], ev["player_id"]]).sum()
    stats.index.names = idx
    ast_ev = ev[ev["assisted"].astype(bool)]
    ast = ast_ev.groupby([ast_ev["game_id"], ast_ev["team"], ast_ev["player2_id"].astype(str)]).size().rename("ast")
    ast.index.names = idx
    df = pd.concat([on_poss, stats, ast], axis=1).fillna(0)
    df = df[df["on_poss"] > 0]
    df["usg_pct"] = (df["fga"] + 0.44 * df["fta"] + df["tov"]) / df["on_poss"]
    df["true_usage"] = (df["fga"] + df["ft_trips"] + df["tov"] + df["ast"]) / df["on_poss"]
    return df.reset_index()


def usage_concentration(usage: pd.DataFrame) -> pd.DataFrame:
    """Por equipo-partido: USG máximo, True Usage máximo e índice HHI de concentración."""
    if usage.empty:
        return pd.DataFrame(columns=["game_id", "team"])
    u = usage[usage["on_poss"] >= 10]
    share = u["fga"] + 0.44 * u["fta"] + u["tov"]
    k = [u["game_id"], u["team"]]
    tot = share.groupby(k).transform("sum").replace(0, np.nan)
    return pd.DataFrame({
        "max_usg": u["usg_pct"].groupby(k).max(),
        "max_true_usage": u["true_usage"].groupby(k).max(),
        "usage_hhi": ((share / tot) ** 2).groupby(k).sum(),
    }).reset_index()


def ft_expectation(events: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """TL esperados con el FT% previo de cada tirador (shrinkage a la liga) -> FT Luck."""
    ft = events[(events["event_type"] == "free_throw") & ~events["ft_technical"]].drop(
        columns=["game_date", "season"], errors="ignore").merge(games[["game_id", "game_date"]], on="game_id", how="left")
    if ft.empty:
        return pd.DataFrame(columns=["game_id", "team"])
    ft = ft.assign(player_id=ft["player_id"].astype(str), made_f=ft["made"].astype(float))
    per_game = (ft.groupby(["player_id", "game_date", "game_id"]).agg(m=("made_f", "sum"), a=("made_f", "size"))
                .reset_index().sort_values(["player_id", "game_date"]))
    g = per_game.groupby("player_id")
    prior_m = g["m"].cumsum() - per_game["m"]
    prior_a = g["a"].cumsum() - per_game["a"]
    per_game["prior_ft_pct"] = (prior_m + FT_PRIOR_PCT * FT_PRIOR_WEIGHT) / (prior_a + FT_PRIOR_WEIGHT)
    ft = ft.merge(per_game[["player_id", "game_id", "prior_ft_pct"]], on=["player_id", "game_id"], how="left")
    return ft.groupby(["game_id", "team"]).agg(ft_att=("made_f", "size"), ft_made=("made_f", "sum"),
                                              ft_expected=("prior_ft_pct", "sum")).reset_index()


def foul_trouble(events: pd.DataFrame) -> pd.DataFrame:
    """Tendencia del HC a sentar jugadores con 2 faltas en la 1ª mitad o 3 en el 3er cuarto
    (¿está en el banquillo 60 s de juego después de la falta?)."""
    if "home_lineup" not in events.columns:
        return pd.DataFrame(columns=["game_id", "team"])
    fouls = events[(events["event_type"] == "foul")
                   & ~events["subtype"].fillna("").str.contains("Technical")].copy()
    fouls["player_id"] = fouls["player_id"].astype(str)
    fouls["n_foul"] = fouls.groupby(["game_id", "player_id"]).cumcount() + 1
    trig = fouls[((fouls["n_foul"] == 2) & (fouls["period"] <= 2)) | ((fouls["n_foul"] == 3) & (fouls["period"] == 3))]
    if trig.empty:
        return pd.DataFrame(columns=["game_id", "team"])
    # Búsqueda explícita DENTRO de cada partido (merge_asof con `by` mezclaba partidos y hacía
    # que el resultado dependiera de qué otros partidos había en el dataset: fuga detectada por
    # el test de truncamiento sobre datos reales).
    parts = []
    for gid, tg in trig.groupby("game_id", sort=False):
        ev = events.loc[events["game_id"] == gid, ["game_sec_elapsed", "home_lineup", "away_lineup", "home_team"]]
        ev = ev.sort_values("game_sec_elapsed", kind="stable")
        t_check = (tg["game_sec_elapsed"] + FOUL_TROUBLE_LAG_SEC).to_numpy()
        pos = np.searchsorted(ev["game_sec_elapsed"].to_numpy(), t_check, side="left")
        found = pos < len(ev)
        pos = np.minimum(pos, len(ev) - 1)
        is_home = (tg["team"].to_numpy() == ev["home_team"].iloc[0])
        lineup = np.where(is_home, ev["home_lineup"].to_numpy()[pos], ev["away_lineup"].to_numpy()[pos])
        lineup = np.where(found, lineup, None)  # falta pasados los 60 s finales: sin dato
        on = _in_lineup(pd.Series(lineup), tg["player_id"].reset_index(drop=True))
        parts.append(pd.DataFrame({"game_id": gid, "team": tg["team"].to_numpy(), "benched": ~on, "valid": found}))
    chk = pd.concat(parts, ignore_index=True)
    chk = chk[chk["valid"]]
    return chk.groupby(["game_id", "team"]).agg(foul_trouble_events=("benched", "size"),
                                               foul_trouble_benched=("benched", "sum")).reset_index()
