"""Reconstrucción de quintetos en pista a partir de sustituciones + titulares del box score.

ESPN no publica quintetos al inicio de cada periodo; se infieren con la heurística estándar
(pbpstats): jugadores que actúan en el periodo antes de entrar por cambio estaban en pista,
completando con el quinteto final del periodo anterior. El resultado alimenta On/Off,
rim protection (ancla en pista vs banco) y USG% por posesiones en pista.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from nba_quant.logging_utils import get_logger

log = get_logger("lineups")

LINEUP_SIZE = 5


def _period_starters(ev: pd.DataFrame, team_players: set[str], prev_end: list[str], q1_starters: list[str],
                     period: int) -> list[str]:
    if period == 1 and len(q1_starters) == LINEUP_SIZE:
        return list(q1_starters)
    first_seen: dict[str, str] = {}  # jugador -> 'enter' | 'play'
    order: list[str] = []
    for row in ev.itertuples(index=False):
        if row.event_type == "substitution":
            entering, leaving = row.player_id, row.player2_id
            if entering in team_players and entering not in first_seen:
                first_seen[entering] = "enter"
                order.append(entering)
            if leaving in team_players and leaving not in first_seen:
                first_seen[leaving] = "play"  # salió sin haber entrado -> era titular del periodo
                order.append(leaving)
            continue
        for pid in (row.player_id, row.player2_id):
            if pid in team_players and pid not in first_seen:
                first_seen[pid] = "play"
                order.append(pid)
    starters = [p for p in order if first_seen[p] == "play"][:LINEUP_SIZE]
    if len(starters) < LINEUP_SIZE:
        for p in prev_end + q1_starters:
            if p not in starters and first_seen.get(p) != "enter":
                starters.append(p)
            if len(starters) == LINEUP_SIZE:
                break
    return starters


def build_lineups(pbp: pd.DataFrame, player_box: pd.DataFrame) -> pd.DataFrame:
    """Añade `home_lineup` / `away_lineup` (ids ordenados unidos por '-') a cada evento.

    Requiere `player_box` con game_id, team, player_id, starter. Si falta, devuelve el PBP
    sin columnas de lineup (las métricas dependientes se omiten aguas abajo).
    """
    if player_box is None or player_box.empty:
        log.warning("Sin player_box: no se reconstruyen lineups")
        return pbp
    box = player_box.assign(player_id=player_box["player_id"].astype(str))
    out = []
    for gid, ev in pbp.groupby("game_id", sort=False):
        gbox = box[box["game_id"] == gid]
        if gbox.empty:
            out.append(ev.assign(home_lineup=None, away_lineup=None))
            continue
        home, away = ev["home_team"].iloc[0], ev["away_team"].iloc[0]
        lineups = {}
        for team in (home, away):
            tb = gbox[gbox["team"] == team]
            players = set(tb["player_id"])
            q1 = tb.loc[tb["starter"], "player_id"].tolist()
            current: list[str] = []
            per_event: list[str | None] = []
            for period, pev in ev.groupby("period", sort=True):
                current = _period_starters(pev, players, current, q1, int(period))
                for row in pev.itertuples(index=False):
                    if row.event_type == "substitution" and row.player2_id in current and row.player_id in players:
                        current = [row.player_id if p == row.player2_id else p for p in current]
                    per_event.append("-".join(sorted(current)) if len(current) == LINEUP_SIZE else None)
            lineups[team] = per_event
        # groupby('period') recorre en orden de periodo; el PBP ya está ordenado por seq
        ev_sorted = ev.sort_values(["period", "seq"])
        ev_sorted = ev_sorted.assign(home_lineup=lineups[home], away_lineup=lineups[away])
        out.append(ev_sorted.sort_values("seq"))
    result = pd.concat(out, ignore_index=True)
    coverage = result["home_lineup"].notna().mean()
    log.info("Lineups reconstruidos: cobertura %.1f%% de eventos", 100 * coverage)
    return result


def offense_defense_lineups(df: pd.DataFrame) -> pd.DataFrame:
    """Para filas con `team` (ataque): lineup ofensivo y defensivo."""
    if "home_lineup" not in df.columns:
        return df.assign(off_lineup=None, def_lineup=None)
    is_home = df["team"] == df["home_team"]
    return df.assign(
        off_lineup=np.where(is_home, df["home_lineup"], df["away_lineup"]),
        def_lineup=np.where(is_home, df["away_lineup"], df["home_lineup"]),
    )
