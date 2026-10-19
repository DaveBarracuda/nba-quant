"""Fuente primaria gratuita: API pública de ESPN (sin auth).

stats.nba.com / cdn.nba.com bloquean muchas IPs residenciales y de nube; ESPN ofrece
PBP completo con coordenadas de tiro, win probability por jugada, sustituciones (lineups),
árbitros, arena y cuotas de apertura/cierre. Este módulo descarga y *normaliza* al
esquema canónico que consume `processing/`.
"""

from __future__ import annotations

import asyncio
import re
from datetime import date, timedelta
from typing import Any, Iterable

import numpy as np
import pandas as pd

from nba_quant.config import EngineConfig
from nba_quant.ingestion.http import AsyncHttpClient, HttpError
from nba_quant.logging_utils import get_logger
from nba_quant.teams import normalize_abbr

log = get_logger("espn")

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
SUMMARY_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary"
INJURIES_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries"
TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams"
# Cuotas históricas (temporadas cuyo summary ya no trae `pickcenter`).
CORE_ODDS_URL = ("https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events/{gid}"
                 "/competitions/{gid}/odds")
ROSTER_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/roster"

_FT_RE = re.compile(r"(\d)\s*of\s*(\d)")
_DIST_RE = re.compile(r"(\d+)-foot")
_INVALID_COORD = 1_000_000

# Tipos ESPN que son pérdida aunque el texto del tipo no contenga "Turnover".
_TURNOVER_TYPES = {
    "traveling", "double dribble", "discontinued dribble", "back court", "offensive goaltending",
    "palming", "inbound turnover", "shot clock turnover", "step out of bounds",
    "3-second turnover", "offensive 3-second", "lane violation turnover",
}
_TIMEOUT_TYPES = {"full timeout", "official timeout", "timeout", "short timeout", "20-second timeout"}


# --------------------------------------------------------------------------------------
# Descarga
# --------------------------------------------------------------------------------------
async def fetch_scoreboards(client: AsyncHttpClient, dates: Iterable[date]) -> list[dict[str, Any]]:
    """Devuelve [{'query_date': date, 'event_id': str, 'status': str}] para cada partido."""

    async def one(d: date) -> list[dict[str, Any]]:
        try:
            payload = await client.get_json(
                SCOREBOARD_URL, {"dates": d.strftime("%Y%m%d"), "limit": 100}, use_cache=d < date.today()
            )
        except HttpError as exc:
            log.error("scoreboard %s falló: %s", d, exc)
            return []
        out = []
        for ev in payload.get("events", []):
            status = ev.get("status", {}).get("type", {}).get("name", "")
            season_type = ev.get("season", {}).get("type")
            out.append({"query_date": d, "event_id": ev["id"], "status": status, "season_type": season_type})
        return out

    results = await asyncio.gather(*(one(d) for d in dates))
    return [row for chunk in results for row in chunk]


async def fetch_summaries(client: AsyncHttpClient, event_ids: Iterable[str]) -> dict[str, dict]:
    """Descarga el JSON 'summary' (PBP + box + odds + WP) de cada evento."""

    async def one(eid: str) -> tuple[str, dict | None]:
        try:
            return eid, await client.get_json(SUMMARY_URL, {"event": eid})
        except HttpError as exc:
            log.error("summary %s falló: %s", eid, exc)
            return eid, None

    pairs = await asyncio.gather(*(one(e) for e in event_ids))
    return {eid: data for eid, data in pairs if data is not None}


def date_range(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


# --------------------------------------------------------------------------------------
# Normalización
# --------------------------------------------------------------------------------------
def _clock_to_seconds(display: str) -> float:
    """'11:45' -> 705.0 ; '38.2' -> 38.2."""
    if not display:
        return np.nan
    if ":" in display:
        m, s = display.split(":")
        return int(m) * 60 + float(s)
    return float(display)


def _classify(type_text: str, shooting: bool, text: str) -> str:
    t = type_text.lower()
    if "free throw" in t:
        return "free_throw"
    if shooting:
        return "shot"
    if "rebound" in t:
        return "rebound"
    if "turnover" in t or t in _TURNOVER_TYPES:
        return "turnover"
    if "foul" in t or t == "offensive charge":
        return "foul"
    if t in _TIMEOUT_TYPES or "timeout" in t:
        return "timeout"
    if t == "substitution":
        return "substitution"
    if t.startswith("jump"):
        return "jumpball"
    if t.startswith("end period") or t.startswith("end game"):
        return "period_end"
    if "challenge" in t or "review" in t:
        return "review"
    return "other"


def _shot_style(type_text: str, assisted: bool) -> str:
    """Proxy de tipo de acción a partir del tipo ESPN (no hay tracking óptico gratuito)."""
    t = type_text.lower()
    if "putback" in t or "tip" in t:
        return "putback"
    if any(k in t for k in ("pullup", "step back", "fade away", "turnaround", "floating")):
        return "pull_up"
    if any(k in t for k in ("dunk", "layup", "finger roll", "alley oop")):
        return "drive" if "driving" in t or "running" in t else "rim_finish"
    if "hook" in t:
        return "post"
    if "jump shot" in t:
        return "catch_shoot" if assisted else "pull_up"
    return "other"


def _team_map(summary: dict) -> tuple[dict[str, str], str, str]:
    comp = summary["header"]["competitions"][0]
    id_to_abbr, home, away = {}, "", ""
    for c in comp["competitors"]:
        abbr = normalize_abbr(c["team"]["abbreviation"])
        id_to_abbr[str(c["id"])] = abbr
        if c["homeAway"] == "home":
            home = abbr
        else:
            away = abbr
    return id_to_abbr, home, away


def parse_pbp(game_id: str, summary: dict) -> pd.DataFrame:
    """Convierte `summary['plays']` al esquema PBP canónico (una fila por evento)."""
    plays = summary.get("plays") or []
    if not plays:
        return pd.DataFrame()
    id_to_abbr, home, away = _team_map(summary)
    wp = {w["playId"]: w.get("homeWinPercentage") for w in summary.get("winprobability") or []}
    rows = []
    for p in plays:
        type_text = (p.get("type") or {}).get("text", "") or ""
        type_text = type_text.replace("\n", " ").strip()
        text = p.get("text", "") or ""
        shooting = bool(p.get("shootingPlay")) and "free throw" not in type_text.lower()
        etype = _classify(type_text, shooting, text)
        parts = [str(x["athlete"]["id"]) for x in p.get("participants", []) if x.get("athlete")]
        coord = p.get("coordinate") or {}
        cx, cy = coord.get("x"), coord.get("y")
        valid = cx is not None and cy is not None and abs(cx) < _INVALID_COORD and abs(cy) < _INVALID_COORD
        x_ft = float(cx) - 25.0 if valid else np.nan
        y_ft = float(cy) if valid else np.nan
        dist_m = _DIST_RE.search(text)
        if dist_m:
            dist = float(dist_m.group(1))
        elif valid:
            dist = float(np.hypot(x_ft, y_ft))
        else:
            dist = np.nan
        ft_num = ft_tot = np.nan
        if etype == "free_throw":
            m = _FT_RE.search(type_text) or _FT_RE.search(text)
            if m:
                ft_num, ft_tot = float(m.group(1)), float(m.group(2))
            else:  # técnicos: "Free Throw - Technical"
                ft_num, ft_tot = 1.0, 1.0
        assisted = etype == "shot" and bool(p.get("scoringPlay")) and "assist" in text.lower()
        rows.append(
            {
                "game_id": game_id,
                "event_idx": int(p.get("sequenceNumber") or 0),
                "play_id": str(p.get("id")),
                "period": int((p.get("period") or {}).get("number") or 0),
                "clock_sec": _clock_to_seconds((p.get("clock") or {}).get("displayValue", "")),
                "team": id_to_abbr.get(str((p.get("team") or {}).get("id")), None),
                "event_type": etype,
                "subtype": type_text,
                "text": text,
                "made": bool(p.get("scoringPlay")) if etype in ("shot", "free_throw") else False,
                "shot_value": int(p.get("pointsAttempted") or 0) if etype == "shot" else (1 if etype == "free_throw" else 0),
                "shot_distance": dist if etype == "shot" else np.nan,
                "x": x_ft if etype == "shot" else np.nan,
                "y": y_ft if etype == "shot" else np.nan,
                "is_offensive_rebound": etype == "rebound" and "offensive" in type_text.lower(),
                "is_team_rebound": etype == "rebound" and "team rebound" in text.lower(),
                "is_steal": etype == "turnover" and "steal" in text.lower(),
                "is_shooting_foul": etype == "foul" and "shooting" in type_text.lower(),
                "ft_num": ft_num,
                "ft_total": ft_tot,
                "ft_technical": etype == "free_throw" and ("technical" in type_text.lower()),
                "ft_flagrant": etype == "free_throw" and ("flagrant" in type_text.lower()),
                "assisted": assisted,
                "shot_style": _shot_style(type_text, assisted) if etype == "shot" else None,
                "player_id": parts[0] if parts else None,
                "player2_id": parts[1] if len(parts) > 1 else None,
                "home_score": int(p.get("homeScore") or 0),
                "away_score": int(p.get("awayScore") or 0),
                "home_wp": wp.get(p.get("id")),
                "wallclock": p.get("wallclock"),
            }
        )
    df = pd.DataFrame(rows).sort_values("event_idx").reset_index(drop=True)
    df["home_team"], df["away_team"] = home, away
    return df


def _f(v: Any) -> float:
    try:
        return float(str(v).replace("o", "").replace("u", "").replace("+", ""))
    except (TypeError, ValueError):
        return np.nan


def parse_game(game_id: str, summary: dict, query_date: date) -> dict[str, Any]:
    comp = summary["header"]["competitions"][0]
    _, home, away = _team_map(summary)
    scores = {normalize_abbr(c["team"]["abbreviation"]): int(c.get("score") or 0) for c in comp["competitors"]}
    info = summary.get("gameInfo", {})
    venue = info.get("venue", {})
    plays = summary.get("plays") or []
    n_periods = max([int((p.get("period") or {}).get("number") or 0) for p in plays] or [4])
    season = summary["header"].get("season", {})
    return {
        "game_id": game_id,
        "season": int(season.get("year") or query_date.year),
        "season_type": int(season.get("type") or 2),
        "game_date": pd.Timestamp(query_date),
        "start_utc": comp.get("date"),
        "home_team": home,
        "away_team": away,
        "home_score": scores.get(home, 0),
        "away_score": scores.get(away, 0),
        "n_periods": n_periods,
        "neutral_site": bool(comp.get("neutralSite")),
        "venue": venue.get("fullName"),
        "venue_city": (venue.get("address") or {}).get("city"),
        "attendance": info.get("attendance"),
    }


def parse_odds(game_id: str, summary: dict) -> list[dict[str, Any]]:
    """Líneas de apertura/cierre por casa (pickcenter). Spread desde la óptica local."""
    out = []
    for pc in summary.get("pickcenter") or []:
        ps, ml, tot = pc.get("pointSpread") or {}, pc.get("moneyline") or {}, pc.get("total") or {}
        g = lambda d, *ks: _f(_dig(d, *ks))  # noqa: E731
        out.append(
            {
                "game_id": game_id,
                "provider": (pc.get("provider") or {}).get("name", "unknown"),
                "spread_open": g(ps, "home", "open", "line"),
                "spread_close": g(ps, "home", "close", "line") if _dig(ps, "home", "close", "line") else _f(pc.get("spread")),
                "spread_home_odds_close": g(ps, "home", "close", "odds"),
                "spread_away_odds_close": g(ps, "away", "close", "odds"),
                "total_open": g(tot, "over", "open", "line"),
                "total_close": g(tot, "over", "close", "line") if _dig(tot, "over", "close", "line") else _f(pc.get("overUnder")),
                "over_odds_close": g(tot, "over", "close", "odds"),
                "under_odds_close": g(tot, "under", "close", "odds"),
                "home_ml_open": g(ml, "home", "open", "odds"),
                "home_ml_close": g(ml, "home", "close", "odds"),
                "away_ml_open": g(ml, "away", "open", "odds"),
                "away_ml_close": g(ml, "away", "close", "odds"),
            }
        )
    return out


def _dig(d: dict, *keys: str) -> Any:
    for k in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def parse_officials(game_id: str, summary: dict) -> list[dict[str, Any]]:
    offs = (summary.get("gameInfo") or {}).get("officials") or []
    return [{"game_id": game_id, "official": o.get("fullName"), "order": i} for i, o in enumerate(offs)]


def parse_player_box(game_id: str, summary: dict) -> list[dict[str, Any]]:
    out = []
    for team_block in (summary.get("boxscore") or {}).get("players") or []:
        team = normalize_abbr(team_block["team"]["abbreviation"])
        for stat_block in team_block.get("statistics") or []:
            labels = stat_block.get("labels") or []
            for a in stat_block.get("athletes") or []:
                vals = dict(zip(labels, a.get("stats") or []))
                if not vals:
                    continue
                fg = str(vals.get("FG", "0-0")).split("-")
                tp = str(vals.get("3PT", "0-0")).split("-")
                ft = str(vals.get("FT", "0-0")).split("-")
                ath = a.get("athlete") or {}
                out.append(
                    {
                        "game_id": game_id,
                        "team": team,
                        "player_id": str(ath.get("id")),
                        "player_name": ath.get("displayName"),
                        "position": (ath.get("position") or {}).get("abbreviation"),
                        "starter": bool(a.get("starter")),
                        "minutes": _f(vals.get("MIN")),
                        "pts": _f(vals.get("PTS")),
                        "fgm": _f(fg[0]), "fga": _f(fg[-1]),
                        "fg3m": _f(tp[0]), "fg3a": _f(tp[-1]),
                        "ftm": _f(ft[0]), "fta": _f(ft[-1]),
                        "reb": _f(vals.get("REB")), "ast": _f(vals.get("AST")),
                        "tov": _f(vals.get("TO")), "stl": _f(vals.get("STL")),
                        "blk": _f(vals.get("BLK")), "oreb": _f(vals.get("OREB")),
                        "dreb": _f(vals.get("DREB")), "pf": _f(vals.get("PF")),
                        "plus_minus": _f(vals.get("+/-")),
                    }
                )
    return out


def parse_injuries(payload: dict, snapshot: date) -> pd.DataFrame:
    rows = []
    for team_block in payload.get("injuries") or []:
        team_name = team_block.get("displayName", "")
        for inj in team_block.get("injuries") or []:
            ath = inj.get("athlete") or {}
            team = normalize_abbr(((ath.get("team") or {}).get("abbreviation")) or team_name)
            rows.append(
                {
                    "snapshot_date": pd.Timestamp(snapshot),
                    "team": team,
                    "player_name": ath.get("displayName"),
                    "player_id": str(ath.get("id")) if ath.get("id") else None,
                    "status": inj.get("status"),
                    "detail": inj.get("shortComment") or inj.get("longComment"),
                }
            )
    return pd.DataFrame(rows)


def parse_team_ids(payload: dict) -> dict[str, str]:
    """abbr -> id de equipo ESPN (para el endpoint de plantillas)."""
    teams = payload["sports"][0]["leagues"][0]["teams"]
    return {normalize_abbr(t["team"]["abbreviation"]): str(t["team"]["id"]) for t in teams}


def parse_roster(team: str, payload: dict, snapshot: date) -> pd.DataFrame:
    """Plantilla actual de un equipo: una fila por jugador (+ entrenador principal)."""
    coach = (payload.get("coach") or [{}])[0]
    coach_name = " ".join(x for x in (coach.get("firstName"), coach.get("lastName")) if x) or None
    season = (payload.get("season") or {}).get("year")
    rows = [{
        "snapshot_date": pd.Timestamp(snapshot), "roster_season": season, "team": team,
        "player_id": str(a.get("id")), "player_name": a.get("displayName"),
        "position": (a.get("position") or {}).get("abbreviation"), "coach": coach_name,
    } for a in payload.get("athletes") or []]
    return pd.DataFrame(rows)


def parse_core_odds(game_id: str, payload: dict) -> list[dict[str, Any]]:
    """Cuotas de la API core de ESPN, mismo esquema que `parse_odds`.

    Se descartan los proveedores "Live" (cuotas tomadas DURANTE el partido: usarlas sería
    fuga de información). Del resto se usa `close`; `open` se guarda pero en esta fuente es
    poco fiable (precios de mercados ya movidos)."""
    out = []
    for it in payload.get("items") or []:
        name = (it.get("provider") or {}).get("name", "unknown")
        if "live" in name.lower():
            continue
        h, a = it.get("homeTeamOdds") or {}, it.get("awayTeamOdds") or {}
        am = lambda d, *ks: _f(_dig(d, *ks, "american"))  # noqa: E731
        out.append({
            "game_id": game_id, "provider": name,
            "spread_open": am(h, "open", "pointSpread"),
            "spread_close": _f(it.get("spread")) if it.get("spread") is not None else am(h, "close", "pointSpread"),
            "spread_home_odds_close": am(h, "close", "spread"), "spread_away_odds_close": am(a, "close", "spread"),
            "total_open": am(it, "open", "total"),
            "total_close": _f(it.get("overUnder")) if it.get("overUnder") is not None else am(it, "close", "total"),
            "over_odds_close": am(it, "close", "over"), "under_odds_close": am(it, "close", "under"),
            "home_ml_open": am(h, "open", "moneyLine"), "home_ml_close": am(h, "close", "moneyLine"),
            "away_ml_open": am(a, "open", "moneyLine"), "away_ml_close": am(a, "close", "moneyLine"),
        })
    return out
