"""Ajuste por bajas del día (reporte de lesiones de ESPN) en pts/100.

Para cada jugador del reporte que juega para un equipo con partido próximo:

    w        = P(baja) · presencia · mpg / 48         (fracción de un puesto en pista)
    Δataque  = w · (RAPM_o reemplazo − RAPM_o jugador)   -> ataque de su equipo
    Δrival   = w · (RAPM_d reemplazo − RAPM_d jugador)   -> ataque del rival (d > 0 = permite más)

- P(baja): `Out` = 1; `Day-To-Day` según el texto (doubtful / questionable / probable).
- presencia = partidos jugados en los últimos 10 de su equipo / 10. Un jugador que ya no venía
  jugando ya está reflejado en el rating del equipo, así que su baja casi no mueve la proyección.
- mpg = minutos medios en esos partidos jugados.
- El reemplazo es el nivel bajo de la rotación (mismo criterio que el prior de plantilla).
El reporte es una foto de hoy: sólo se aplica a partidos futuros, nunca al backtest.
"""

from __future__ import annotations

import re
import unicodedata

import pandas as pd

from nba_quant.features.roster import REPLACEMENT_QUANTILE, compute_rapm
from nba_quant.logging_utils import get_logger

log = get_logger("availability")

RECENT_GAMES = 10
MINUTES_PER_GAME = 48.0
MIN_RAPM_POSS = 1500.0  # posesiones en pista para entrar en la rotación que define el reemplazo
MAX_TEAM_ADJ = 8.0  # pts/100: tope del ajuste total de un equipo
DTD_DEFAULT = 0.4
DTD_KEYWORDS = (("doubtful", 0.75), ("questionable", 0.5), ("probable", 0.1))
SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}
TEAM_COLUMNS = ["game_id", "team", "own_off_adj", "opp_off_adj", "n_players"]


def absence_probability(status: object, detail: object) -> float:
    """Probabilidad de que el jugador no juegue según el estado y el comentario de ESPN."""
    s = str(status or "").strip().lower()
    if s == "out":
        return 1.0
    if s not in ("day-to-day", "doubtful", "questionable"):
        return 0.0
    text = f"{s} {detail or ''}".lower()
    for word, p in DTD_KEYWORDS:
        if word in text:
            return p
    return DTD_DEFAULT


def normalize_name(name: object) -> str:
    """Nombre comparable: sin acentos, puntuación ni sufijos (Jr., III...)."""
    s = unicodedata.normalize("NFKD", str(name or "")).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z ]", "", s.replace("-", " "))
    return " ".join(w for w in s.split() if w not in SUFFIXES)


def replacement_level(rapm: pd.DataFrame) -> tuple[float, float]:
    """(RAPM_o, RAPM_d) de reemplazo: percentil bajo del ataque y alto de la defensa permitida."""
    rot = rapm[rapm["poss_on"] >= MIN_RAPM_POSS]
    if rot.empty:
        return 0.0, 0.0
    return float(rot["o_rapm"].quantile(REPLACEMENT_QUANTILE)), float(rot["d_rapm"].quantile(1 - REPLACEMENT_QUANTILE))


def _recent_usage(box: pd.DataFrame, team: str, before: pd.Timestamp) -> pd.DataFrame:
    """Por jugador del equipo: presencia y mpg en sus últimos RECENT_GAMES partidos antes de `before`."""
    b = box[(box["team"] == team) & (box["game_date"] < before)]
    if b.empty:
        return pd.DataFrame(columns=["player_id", "player_name", "key", "presence", "mpg"])
    last = b.sort_values("game_date")["game_id"].drop_duplicates().tail(RECENT_GAMES)
    played = b[b["game_id"].isin(last) & (b["minutes"].fillna(0) > 0)]
    usage = played.groupby("player_id").agg(games=("game_id", "nunique"), mpg=("minutes", "mean"))
    names = b.sort_values("game_date").groupby("player_id")["player_name"].last()
    out = pd.DataFrame({"player_name": names}).join(usage).reset_index()
    out["presence"] = out["games"].fillna(0) / len(last)
    out["mpg"] = out["mpg"].fillna(0.0)
    out["key"] = out["player_name"].map(normalize_name)
    return out.drop(columns="games")


def _team_rows(inj: pd.DataFrame, usage: pd.DataFrame, rapm: pd.DataFrame, repl: tuple[float, float],
               game_id: str, team: str) -> list[dict]:
    rows = []
    by_key = usage.drop_duplicates("key", keep="last").set_index("key")
    for _, i in inj.iterrows():
        key = normalize_name(i["player_name"])
        if key not in by_key.index:
            continue
        u = by_key.loc[key]
        p_out = absence_probability(i.get("status"), i.get("detail"))
        known = u["player_id"] in rapm.index
        o = float(rapm.at[u["player_id"], "o_rapm"]) if known else repl[0]
        d = float(rapm.at[u["player_id"], "d_rapm"]) if known else repl[1]
        w = p_out * float(u["presence"]) * float(u["mpg"]) / MINUTES_PER_GAME
        rows.append({"game_id": game_id, "team": team, "player_id": str(u["player_id"]),
                     "player_name": u["player_name"], "status": i.get("status"), "p_out": p_out,
                     "presence": float(u["presence"]), "mpg": float(u["mpg"]), "o_rapm": o, "d_rapm": d,
                     "own_off_adj": w * (repl[0] - o), "opp_off_adj": w * (repl[1] - d)})
    return rows


def absence_impacts(injuries: pd.DataFrame, box: pd.DataFrame, rapm: pd.DataFrame, upcoming: pd.DataFrame,
                    replacement: tuple[float, float] | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(por equipo-partido, por jugador). `box` necesita game_id, game_date, team, player_id,
    player_name, minutes; `rapm` player_id, o_rapm, d_rapm, poss_on; `upcoming` game_id,
    game_date, home_team, away_team. Ajustes en pts/100 sobre el ataque de cada equipo."""
    empty = pd.DataFrame(columns=TEAM_COLUMNS), pd.DataFrame()
    if injuries is None or injuries.empty or box.empty or upcoming.empty:
        return empty
    repl = replacement if replacement is not None else replacement_level(rapm)
    rapm_idx = rapm.assign(player_id=rapm["player_id"].astype(str)).drop_duplicates("player_id").set_index("player_id")
    box = box.assign(player_id=box["player_id"].astype(str), game_date=pd.to_datetime(box["game_date"]))
    players = []
    for g in upcoming.itertuples(index=False):
        for team in (g.home_team, g.away_team):
            inj = injuries[injuries["team"] == team]
            if inj.empty:
                continue
            usage = _recent_usage(box, team, pd.Timestamp(g.game_date))
            players += _team_rows(inj, usage, rapm_idx, repl, g.game_id, team)
    if not players:
        return empty
    p = pd.DataFrame(players)
    teams = (p.groupby(["game_id", "team"])
             .agg(own_off_adj=("own_off_adj", "sum"), opp_off_adj=("opp_off_adj", "sum"),
                  n_players=("player_id", "size")).reset_index())
    teams[["own_off_adj", "opp_off_adj"]] = teams[["own_off_adj", "opp_off_adj"]].clip(-MAX_TEAM_ADJ, MAX_TEAM_ADJ)
    log.info("Bajas: %d jugadores valorados en %d equipos (reemplazo o=%.2f d=%.2f)", len(p), len(teams), *repl)
    return teams, p.sort_values("own_off_adj").reset_index(drop=True)


def build_absences(injuries: pd.DataFrame, poss: pd.DataFrame | None, player_box: pd.DataFrame,
                   games: pd.DataFrame, upcoming: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Bajas de los partidos de `upcoming` con RAPM de la temporada actual y la anterior."""
    if injuries is None or injuries.empty or upcoming.empty or player_box is None or player_box.empty:
        return pd.DataFrame(columns=TEAM_COLUMNS), pd.DataFrame()
    season = int(upcoming["season"].max()) if "season" in upcoming.columns else int(games["season"].max())
    recent_ids = games.loc[games["season"].isin([season - 1, season]), "game_id"]
    rapm = (compute_rapm(poss[poss["game_id"].isin(recent_ids)]) if poss is not None and not poss.empty
            else pd.DataFrame(columns=["player_id", "o_rapm", "d_rapm", "poss_on"]))
    box = player_box.drop(columns=["game_date"], errors="ignore").merge(
        games[["game_id", "game_date"]].drop_duplicates("game_id"), on="game_id")
    return absence_impacts(injuries, box, rapm, upcoming)
