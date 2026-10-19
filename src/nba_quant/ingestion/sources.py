"""Fuentes secundarias del diagrama de ingesta (spec 2 §2).

- The Odds API (REST, clave gratuita en env ODDS_API_KEY) -> cuotas vigentes multi-casa.
- nba_api / stats.nba.com (sin auth) -> endpoints de tracking oficiales agregados
  (drives, pases, hustle, synergy, defensa en el aro). Muchos ISPs/nubes están bloqueados:
  el fallo se registra y el pipeline continúa sin esas columnas.
- Basketball-Reference (scraping con 3.5 s de pausa) -> tablas de temporada.
- Kaggle (kaggle.json) -> datasets históricos de tracking si el usuario los descarga.

Todas las fuentes devuelven DataFrames normalizados (abreviaturas ESPN, fechas Timestamp).
"""

from __future__ import annotations

import io
import os
import subprocess
from datetime import date
from pathlib import Path

import pandas as pd

from nba_quant.config import EngineConfig
from nba_quant.ingestion.http import AsyncHttpClient, HttpError, SyncHttpClient
from nba_quant.logging_utils import get_logger
from nba_quant.teams import normalize_abbr

log = get_logger("sources")

ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
BREF_URL = "https://www.basketball-reference.com/leagues/NBA_{season}{suffix}.html"

# Mapeo nombre completo -> abreviatura para The Odds API.
FULL_NAME_TO_ABBR = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET", "Golden State Warriors": "GS", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC", "LA Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NO",
    "New York Knicks": "NY", "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX", "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SA",
    "Toronto Raptors": "TOR", "Utah Jazz": "UTAH", "Washington Wizards": "WSH",
}


# --------------------------------------------------------------------------------------
# The Odds API
# --------------------------------------------------------------------------------------
async def fetch_odds_api(client: AsyncHttpClient, cfg: EngineConfig) -> pd.DataFrame:
    """Cuotas actuales (h2h/spreads/totals) de todas las casas US. Requiere ODDS_API_KEY."""
    key = os.environ.get(cfg.http.odds_api_key_env)
    if not key:
        log.warning("ODDS_API_KEY no definida: se omite The Odds API (se usan cuotas ESPN)")
        return pd.DataFrame()
    params = {"apiKey": key, "regions": "us", "markets": "h2h,spreads,totals", "oddsFormat": "american"}
    try:
        events = await client.get_json(ODDS_API_URL, params, use_cache=False)
    except HttpError as exc:
        log.error("The Odds API falló: %s", exc)
        return pd.DataFrame()
    rows = []
    for ev in events:
        home = FULL_NAME_TO_ABBR.get(ev.get("home_team"), ev.get("home_team"))
        away = FULL_NAME_TO_ABBR.get(ev.get("away_team"), ev.get("away_team"))
        for bk in ev.get("bookmakers", []):
            for mk in bk.get("markets", []):
                for o in mk.get("outcomes", []):
                    rows.append(
                        {
                            "commence_time": pd.Timestamp(ev["commence_time"]),
                            "home_team": home,
                            "away_team": away,
                            "book": bk["key"],
                            "market": mk["key"],
                            "outcome": FULL_NAME_TO_ABBR.get(o["name"], o["name"]),
                            "price": o.get("price"),
                            "point": o.get("point"),
                            "last_update": pd.Timestamp(bk.get("last_update")),
                        }
                    )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------------------
# nba_api: tracking oficial agregado (point-in-time con DateTo)
# --------------------------------------------------------------------------------------
# endpoint -> (clase nba_api, kwargs). Todos aceptan date_to_nullable para evitar fuga temporal.
TRACKING_ENDPOINTS: dict[str, tuple[str, dict]] = {
    "drives": ("LeagueDashPtStats", {"pt_measure_type": "Drives", "player_or_team": "Team"}),
    "passing": ("LeagueDashPtStats", {"pt_measure_type": "Passing", "player_or_team": "Team"}),
    "speed_distance": ("LeagueDashPtStats", {"pt_measure_type": "SpeedDistance", "player_or_team": "Team"}),
    "rebounding": ("LeagueDashPtStats", {"pt_measure_type": "Rebounding", "player_or_team": "Team"}),
    "touches": ("LeagueDashPtStats", {"pt_measure_type": "Possessions", "player_or_team": "Team"}),
    "catch_shoot": ("LeagueDashPtStats", {"pt_measure_type": "CatchShoot", "player_or_team": "Team"}),
    "pull_up": ("LeagueDashPtStats", {"pt_measure_type": "PullUpShot", "player_or_team": "Team"}),
    "defense_rim": ("LeagueDashPtTeamDefend", {"defense_category": "Less Than 6Ft"}),
    "hustle": ("LeagueHustleStatsTeam", {}),
}


def fetch_nba_tracking(cfg: EngineConfig, season: str, as_of: date) -> pd.DataFrame:
    """Snapshot de tracking por equipo hasta `as_of` (incluido). Vacío si stats.nba.com bloquea."""
    try:
        from nba_api.stats import endpoints as ep  # import perezoso: dependencia opcional
    except ImportError:
        log.warning("nba_api no instalado: se omite tracking oficial")
        return pd.DataFrame()
    frames = []
    for name, (cls_name, kwargs) in TRACKING_ENDPOINTS.items():
        try:
            cls = getattr(ep, cls_name)
            df = cls(season=season, date_to_nullable=as_of.strftime("%m/%d/%Y"), timeout=cfg.http.timeout_sec,
                     **kwargs).get_data_frames()[0]
        except Exception as exc:  # nba_api lanza tipos heterogéneos (Timeout, JSONDecodeError, KeyError)
            log.warning("tracking %s no disponible (%s); se continúa sin él", name, type(exc).__name__)
            continue
        abbr_col = "TEAM_ABBREVIATION" if "TEAM_ABBREVIATION" in df.columns else None
        if abbr_col is None:
            continue
        long = df.melt(id_vars=[abbr_col], var_name="metric", value_name="value")
        long = long[pd.to_numeric(long["value"], errors="coerce").notna()]
        long = long.assign(
            team=long[abbr_col].map(normalize_abbr), endpoint=name, as_of_date=pd.Timestamp(as_of),
            value=pd.to_numeric(long["value"]),
        ).drop(columns=[abbr_col])
        frames.append(long)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# --------------------------------------------------------------------------------------
# Basketball-Reference (3.5 s entre peticiones; reintento con huella TLS si hay 403)
# --------------------------------------------------------------------------------------
def fetch_bref_table(cfg: EngineConfig, season: int, suffix: str = "_advanced") -> pd.DataFrame:
    """Tabla de temporada de B-Ref (p.ej. NBA_2026_advanced). B-Ref sirve 403 a clientes sin
    huella de navegador; si ocurre se reintenta con `tls_requests` cuando está instalado."""
    url = BREF_URL.format(season=season, suffix=suffix)
    client = SyncHttpClient(cfg.http, cfg.http.bref_min_interval_sec, {"Accept-Language": "en-US,en;q=0.9"})
    try:
        html = client.get_text(url)
    except HttpError as exc:
        log.warning("B-Ref %s: %s; reintento con tls_requests", url, exc)
        try:
            import tls_requests  # type: ignore[import-not-found]

            resp = tls_requests.get(url, headers={"User-Agent": cfg.http.user_agent})
            if resp.status_code >= 400:
                raise HttpError(f"HTTP {resp.status_code}")
            html = resp.text
        except (ImportError, HttpError) as exc2:
            log.error("B-Ref inaccesible: %s", exc2)
            return pd.DataFrame()
    html = html.replace("<!--", "").replace("-->", "")  # B-Ref esconde tablas en comentarios
    tables = pd.read_html(io.StringIO(html))
    if not tables:
        return pd.DataFrame()
    df = tables[0]
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[-1] for c in df.columns]
    return df.assign(season=season)


# --------------------------------------------------------------------------------------
# Kaggle (opcional)
# --------------------------------------------------------------------------------------
def fetch_kaggle_dataset(dataset: str, dest: Path) -> list[Path]:
    """Descarga un dataset con la CLI de Kaggle (requiere ~/.kaggle/kaggle.json)."""
    if not (Path.home() / ".kaggle" / "kaggle.json").exists():
        log.warning("kaggle.json no encontrado: se omite Kaggle")
        return []
    dest.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(["kaggle", "datasets", "download", "-d", dataset, "-p", str(dest), "--unzip"],
                       check=True, capture_output=True, timeout=1800)
    except (OSError, subprocess.SubprocessError) as exc:
        log.error("Kaggle download falló: %s", exc)
        return []
    return sorted(dest.rglob("*.csv")) + sorted(dest.rglob("*.parquet"))
