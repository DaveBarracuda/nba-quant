"""DataIngestionLayer (spec 3 clase 1 / spec 2 §2): orquesta todas las fuentes hacia el lake.

ESPN (async) -> games, pbp, odds (apertura/cierre), officials, player_box, injuries
The Odds API (async) -> odds_live ; nba_api -> tracking_team ; B-Ref / Kaggle bajo demanda.
La ingesta es incremental: los partidos finalizados ya presentes en el lake no se re-descargan.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import date

import pandas as pd

from nba_quant.config import EngineConfig
from nba_quant.ingestion import espn
from nba_quant.ingestion.http import AsyncHttpClient, HttpError
from nba_quant.ingestion.sources import fetch_nba_tracking, fetch_odds_api
from nba_quant.logging_utils import get_logger
from nba_quant.storage.lake import DataLake

log = get_logger("ingestion")

FINAL_STATUSES = {"STATUS_FINAL", "STATUS_FINAL_OT"}


@dataclass(frozen=True)
class IngestionReport:
    games: int
    pbp_rows: int
    odds_rows: int
    skipped_existing: int
    failed: int


class DataIngestionLayer:
    """Ingesta asíncrona e idempotente hacia el data lake."""

    def __init__(self, cfg: EngineConfig, lake: DataLake) -> None:
        self.cfg = cfg
        self.lake = lake

    def ingest_range(self, start: date, end: date, season_types: tuple[int, ...] = (2, 3)) -> IngestionReport:
        return asyncio.run(self._ingest_range(start, end, season_types))

    async def _ingest_range(self, start: date, end: date, season_types: tuple[int, ...]) -> IngestionReport:
        existing_games = self.lake.read("games")
        have = set(existing_games["game_id"]) if not existing_games.empty else set()
        async with AsyncHttpClient(self.cfg.http, self.cfg.http.espn_min_interval_sec,
                                   self.cfg.paths.raw / "espn") as client:
            board = await espn.fetch_scoreboards(client, espn.date_range(start, end))
            todo = [b for b in board if b["status"] in FINAL_STATUSES and b["season_type"] in season_types
                    and b["event_id"] not in have]
            skipped = sum(1 for b in board if b["event_id"] in have)
            log.info("scoreboard: %d partidos finalizados nuevos, %d ya en lake", len(todo), skipped)
            summaries = await espn.fetch_summaries(client, [b["event_id"] for b in todo])
        qdate = {b["event_id"]: b["query_date"] for b in todo}
        games, pbp, odds, offs, box = [], [], [], [], []
        failed = 0
        for eid, summ in summaries.items():
            try:
                g = espn.parse_game(eid, summ, qdate[eid])
                p = espn.parse_pbp(eid, summ)
                if p.empty:
                    raise ValueError("PBP vacío")
            except (KeyError, ValueError, TypeError, IndexError) as exc:
                failed += 1
                log.error("parse %s falló: %s", eid, exc)
                continue
            games.append(g)
            pbp.append(p.assign(season=g["season"], game_date=g["game_date"]))
            odds.extend({**o, "season": g["season"]} for o in espn.parse_odds(eid, summ))
            offs.extend({**o, "season": g["season"]} for o in espn.parse_officials(eid, summ))
            box.extend({**b, "season": g["season"]} for b in espn.parse_player_box(eid, summ))
        failed += len(todo) - len(summaries)
        games_df = pd.DataFrame(games)
        pbp_df = pd.concat(pbp, ignore_index=True) if pbp else pd.DataFrame()
        self.lake.write("games", games_df)
        self.lake.write("pbp", pbp_df)
        self.lake.write("odds", pd.DataFrame(odds))
        self.lake.write("officials", pd.DataFrame(offs))
        self.lake.write("player_box", pd.DataFrame(box))
        return IngestionReport(len(games_df), len(pbp_df), len(odds), skipped, failed)

    def ingest_schedule(self, start: date, end: date) -> pd.DataFrame:
        """Partidos programados (no finalizados) para la pizarra de simulación."""
        return asyncio.run(self._schedule(start, end))

    async def _schedule(self, start: date, end: date) -> pd.DataFrame:
        async with AsyncHttpClient(self.cfg.http, self.cfg.http.espn_min_interval_sec, None) as client:
            board = await espn.fetch_scoreboards(client, espn.date_range(start, end))
            pending = [b for b in board if b["status"] not in FINAL_STATUSES]
            summaries = await espn.fetch_summaries(client, [b["event_id"] for b in pending])
        rows = []
        for b in pending:
            summ = summaries.get(b["event_id"])
            if not summ:
                continue
            g = espn.parse_game(b["event_id"], summ, b["query_date"])
            odds = espn.parse_odds(b["event_id"], summ)
            offs = [o["official"] for o in espn.parse_officials(b["event_id"], summ)]
            rows.append({**g, **(odds[0] if odds else {}), "officials": offs})
        return pd.DataFrame(rows)

    def ingest_injuries(self, snapshot: date | None = None) -> pd.DataFrame:
        snapshot = snapshot or date.today()
        return asyncio.run(self._injuries(snapshot))

    async def _injuries(self, snapshot: date) -> pd.DataFrame:
        async with AsyncHttpClient(self.cfg.http, self.cfg.http.espn_min_interval_sec, None) as client:
            try:
                payload = await client.get_json(espn.INJURIES_URL, use_cache=False)
            except HttpError as exc:
                log.error("injuries falló: %s", exc)
                return pd.DataFrame()
        df = espn.parse_injuries(payload, snapshot)
        if not df.empty:
            self.lake.write("injuries", df.assign(season=snapshot.year + (1 if snapshot.month >= 8 else 0)))
        return df

    def backfill_odds(self, seasons: list[int]) -> int:
        """Cuotas de cierre desde la API core para partidos del lake que no las tienen."""
        return asyncio.run(self._backfill_odds(seasons))

    async def _backfill_odds(self, seasons: list[int]) -> int:
        games = self.lake.read("games", seasons)
        have = self.lake.read("odds", seasons)
        todo = games[~games["game_id"].isin(have["game_id"] if not have.empty else [])]
        async with AsyncHttpClient(self.cfg.http, self.cfg.http.espn_min_interval_sec,
                                   self.cfg.paths.raw / "espn_core_odds") as client:

            async def one(gid: str, season: int) -> list[dict]:
                try:
                    payload = await client.get_json(espn.CORE_ODDS_URL.format(gid=gid))
                except HttpError as exc:
                    log.warning("cuotas core %s: %s", gid, exc)
                    return []
                return [{**o, "season": season} for o in espn.parse_core_odds(gid, payload)]

            chunks = await asyncio.gather(*(one(g, s) for g, s in zip(todo["game_id"], todo["season"])))
        rows = pd.DataFrame([r for c in chunks for r in c])
        self.lake.write("odds", rows)
        log.info("Cuotas rellenadas: %d filas para %d/%d partidos", len(rows),
                 rows["game_id"].nunique() if len(rows) else 0, len(todo))
        return len(rows)

    def ingest_rosters(self, snapshot: date | None = None) -> pd.DataFrame:
        """Plantillas actuales de los 30 equipos (ESPN) -> tabla `rosters` (season = roster_season)."""
        snapshot = snapshot or date.today()
        return asyncio.run(self._rosters(snapshot))

    async def _rosters(self, snapshot: date) -> pd.DataFrame:
        async with AsyncHttpClient(self.cfg.http, self.cfg.http.espn_min_interval_sec, None) as client:
            try:
                ids = espn.parse_team_ids(await client.get_json(espn.TEAMS_URL, use_cache=False))
            except (HttpError, KeyError, IndexError) as exc:
                log.error("lista de equipos falló: %s", exc)
                return pd.DataFrame()

            async def one(team: str, tid: str) -> pd.DataFrame:
                try:
                    payload = await client.get_json(espn.ROSTER_URL.format(team_id=tid), use_cache=False)
                except HttpError as exc:
                    log.error("plantilla %s falló: %s", team, exc)
                    return pd.DataFrame()
                return espn.parse_roster(team, payload, snapshot)

            frames = await asyncio.gather(*(one(t, i) for t, i in ids.items()))
        df = pd.concat([f for f in frames if not f.empty], ignore_index=True) if frames else pd.DataFrame()
        if not df.empty:
            df["season"] = df["roster_season"].fillna(snapshot.year + (1 if snapshot.month >= 8 else 0)).astype(int)
            self.lake.write("rosters", df)
        log.info("Plantillas: %d jugadores en %d equipos", len(df), df["team"].nunique() if len(df) else 0)
        return df

    def ingest_live_odds(self) -> pd.DataFrame:
        async def run() -> pd.DataFrame:
            async with AsyncHttpClient(self.cfg.http, 1.0, None) as client:
                return await fetch_odds_api(client, self.cfg)

        return asyncio.run(run())

    def ingest_tracking(self, season_label: str, season: int, as_of: date) -> pd.DataFrame:
        df = fetch_nba_tracking(self.cfg, season_label, as_of)
        if not df.empty:
            self.lake.write("tracking_team", df.assign(season=season))
        return df
