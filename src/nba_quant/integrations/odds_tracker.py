"""Lector del NBA Odds Tracker (C:\\NBA Odds tracker, SQLite) — sólo lectura.

El tracker guarda cada hora las cotizaciones de The Odds API (tabla `quotes`), los splits de
Action Network (`splits`) y sus alertas de movimiento (`alerts`: STEAM, RLM, INFO, GRADUAL,
NOISE). Aquí se convierten a series de línea comparables con el modelo:

  spread : puntos del LOCAL (−4.5 = local favorito por 4.5)
  total  : puntos del total (over)
  ml     : probabilidad sin vig del local (0-1, devig proporcional de las dos caras)

y se emparejan con los `game_id` de ESPN por (fecha local de EE.UU., local, visitante).
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from nba_quant.ingestion.sources import FULL_NAME_TO_ABBR
from nba_quant.logging_utils import get_logger

log = get_logger("odds_tracker")

DEFAULT_TRACKER_DB = Path(os.environ.get("NBA_ODDS_TRACKER_DB", r"C:\NBA Odds tracker\data\odds.sqlite3"))
US_DATE_OFFSET = pd.Timedelta(hours=-6)  # UTC -> fecha del partido en EE.UU. (tips 12:00 ET - 22:30 PT)
MARKETS = {"spreads": "spread", "totals": "total", "h2h": "ml"}
TEAM_ALIASES = {"LA Clippers": "Los Angeles Clippers"}


def _abbr(name: str) -> str | None:
    return FULL_NAME_TO_ABBR.get(TEAM_ALIASES.get(name, name))


def _implied(american: pd.Series) -> np.ndarray:
    a = american.astype(float).to_numpy()
    return np.where(a >= 100, 100.0 / (a + 100.0), -a / (-a + 100.0))


class OddsTrackerReader:
    """Acceso de sólo lectura a la base del tracker (conexión SQLite en modo `ro`)."""

    def __init__(self, db_path: Path = DEFAULT_TRACKER_DB, book: str = "draftkings") -> None:
        if not Path(db_path).exists():
            raise FileNotFoundError(f"No existe la base del tracker: {db_path}")
        self.db_path = Path(db_path)
        self.book = book

    def _query(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        con = sqlite3.connect(f"file:{self.db_path.as_posix()}?mode=ro", uri=True)
        try:
            return pd.read_sql_query(sql, con, params=params)
        finally:
            con.close()

    def events(self) -> pd.DataFrame:
        """event_id, commence_time (UTC), home_team/away_team (abreviatura), us_date."""
        ev = self._query("SELECT DISTINCT event_id, commence_time, home, away FROM quotes WHERE book = ?",
                         (self.book,))
        ev["commence_time"] = pd.to_datetime(ev["commence_time"], utc=True)
        ev["home_team"], ev["away_team"] = ev["home"].map(_abbr), ev["away"].map(_abbr)
        ev["us_date"] = (ev["commence_time"] + US_DATE_OFFSET).dt.tz_localize(None).dt.normalize()
        unknown = ev[ev["home_team"].isna() | ev["away_team"].isna()]
        if len(unknown):
            log.warning("Equipos sin mapear en el tracker: %s", sorted(set(unknown["home"]) | set(unknown["away"])))
        return ev.dropna(subset=["home_team", "away_team"]).drop_duplicates("event_id").reset_index(drop=True)

    def lines(self) -> pd.DataFrame:
        """Una fila por (event_id, market, ts): value + precio de la cara A (local/over) y B."""
        q = self._query("SELECT run_ts, event_id, market, outcome, point, price FROM quotes WHERE book = ?",
                        (self.book,))
        cols = ["event_id", "market", "ts", "value", "price_a", "price_b"]
        if q.empty:
            return pd.DataFrame(columns=cols)
        q["ts"] = pd.to_datetime(q["run_ts"], utc=True)
        wide = q.pivot_table(index=["event_id", "market", "ts"], columns="outcome",
                             values=["point", "price"], aggfunc="last")
        wide.columns = [f"{a}_{b}" for a, b in wide.columns]
        wide = wide.reset_index()
        out = []
        for mk, d in wide.groupby("market"):
            if mk == "spreads":
                v, pa, pb = d["point_home"], d["price_home"], d["price_away"]
            elif mk == "totals":
                v, pa, pb = d["point_over"], d["price_over"], d["price_under"]
            elif mk == "h2h":
                ph, pw = _implied(d["price_home"]), _implied(d["price_away"])
                v, pa, pb = pd.Series(ph / (ph + pw), index=d.index), d["price_home"], d["price_away"]
            else:
                continue
            out.append(pd.DataFrame({"event_id": d["event_id"], "market": MARKETS[mk], "ts": d["ts"],
                                     "value": v, "price_a": pa, "price_b": pb}))
        res = pd.concat(out, ignore_index=True).dropna(subset=["value"])
        return res.sort_values(["event_id", "market", "ts"]).reset_index(drop=True)[cols]

    def alerts(self) -> pd.DataFrame:
        a = self._query("SELECT run_ts, kind, severity, event_id, book, market, message FROM alerts")
        a["ts"] = pd.to_datetime(a["run_ts"], utc=True)
        a["market"] = a["market"].map(MARKETS)
        return a

    def splits(self) -> pd.DataFrame:
        """% de tickets/dinero en el LOCAL (o el over), con abreviaturas."""
        s = self._query("SELECT run_ts, away, home, market, tickets_pct, money_pct, num_bets FROM splits")
        s["ts"] = pd.to_datetime(s["run_ts"], utc=True)
        s["home_team"], s["away_team"] = s["home"].map(_abbr), s["away"].map(_abbr)
        s["market"] = s["market"].map(MARKETS)
        return s


def match_games(events: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """Añade `game_id` (ESPN) a los eventos del tracker por fecha EE.UU. + equipos."""
    g = games.assign(us_date=pd.to_datetime(games["game_date"]).dt.normalize())
    m = events.merge(g[["game_id", "us_date", "home_team", "away_team"]].drop_duplicates("game_id"),
                     on=["us_date", "home_team", "away_team"], how="left")
    miss = int(m["game_id"].isna().sum())
    if miss:
        log.info("Eventos del tracker sin partido ESPN emparejado: %d de %d", miss, len(m))
    return m


def line_asof(lines: pd.DataFrame, event_id: str, market: str, ts: pd.Timestamp) -> pd.Series | None:
    """Última línea del tracker con marca de tiempo <= ts (None si aún no había ninguna)."""
    d = lines[(lines["event_id"] == event_id) & (lines["market"] == market) & (lines["ts"] <= ts)]
    return d.iloc[-1] if len(d) else None


def closing_line(lines: pd.DataFrame, event_id: str, market: str, commence: pd.Timestamp) -> pd.Series | None:
    """Último snapshot del tracker antes del salto inicial (el 'cierre' que vio el tracker)."""
    return line_asof(lines, event_id, market, commence - pd.Timedelta(seconds=1))
