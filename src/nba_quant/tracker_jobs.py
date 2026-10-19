"""Trabajos que conectan el modelo con el NBA Odds Tracker.

  python -m nba_quant.cli track-snapshot [--hours 48]   # proyecta los próximos partidos del tracker
  python -m nba_quant.cli track-report                  # movimiento vs modelo + WR de los picks

`track-snapshot` debe correr al menos una vez por día de partidos (idealmente temprano, cuando
el modelo ya incorpora los resultados de ayer); el tracker sigue tomando líneas cada hora y
`track-report` mide hacia dónde se movió el mercado respecto al número del modelo.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from nba_quant.config import EngineConfig
from nba_quant.ingestion.engine import DataIngestionLayer
from nba_quant.integrations.odds_tracker import DEFAULT_TRACKER_DB, OddsTrackerReader, match_games
from nba_quant.ledger import write_ledger
from nba_quant.logging_utils import get_logger
from nba_quant.publish import publish_ledger
from nba_quant.simulation.market_moves import (build_snapshots, first_snapshot_picks, model_vs_market_drift,
                                               pick_table, summarize)
from nba_quant.simulation.slate import MODEL_VERSION
from nba_quant.storage.lake import DataLake

log = get_logger("tracker_jobs")

RESULTS_GRACE = pd.Timedelta(hours=4)  # un partido se da por terminado 4 h después del salto
US_DATE_SHIFT = pd.Timedelta(hours=6)
DEFAULT_SEASONS_BACK = 3  # temporadas del lake usadas para las features (la previa + la actual)


def _emit(text: str) -> None:
    from nba_quant.cli import emit

    emit(text)


def run_snapshot(cfg: EngineConfig, tracker_db: Path = DEFAULT_TRACKER_DB, hours: float = 48.0,
                 seasons: list[int] | None = None) -> pd.DataFrame:
    """Proyecta (modelo puro, sin mezcla con el mercado) los partidos del tracker de las próximas
    `hours` horas y guarda el snapshot con la línea que el tracker ve ahora."""
    from nba_quant.cli import build_features, make_simulator

    reader = OddsTrackerReader(tracker_db)
    now = pd.Timestamp.now(tz="UTC")
    events = reader.events()
    window = events[(events["commence_time"] > now) & (events["commence_time"] <= now + pd.Timedelta(hours=hours))]
    if window.empty:
        _emit(f"El tracker no tiene partidos en las próximas {hours:g} h")
        return pd.DataFrame()
    lake = DataLake(cfg.paths)
    layer = DataIngestionLayer(cfg, lake)
    sched = layer.ingest_schedule(window["us_date"].min().date(), window["us_date"].max().date())
    matched = match_games(window, sched)
    up = sched[sched["game_id"].isin(matched["game_id"].dropna())].drop(columns=["officials"], errors="ignore")
    if up.empty:
        _emit("Ningún partido del tracker se pudo emparejar con el calendario de ESPN")
        return pd.DataFrame()
    odds = lake.read("odds")
    odds = pd.concat([odds, up.reindex(columns=odds.columns)], ignore_index=True)
    seasons = seasons or sorted(int(s) for s in lake.read("games")["season"].unique())[-DEFAULT_SEASONS_BACK:]
    feats, pipe = build_features(cfg, lake, seasons, up)
    sim = make_simulator(cfg, feats, pipe, odds, lake.read("officials"), up)
    proj = []
    for gid in up["game_id"]:
        try:
            row = sim.project_game(gid, with_props=False).row
        except (KeyError, ValueError) as exc:
            log.error("Partido %s omitido: %s", gid, exc)
            continue
        proj.append({"game_id": gid, "model_margin": row["model_margin_raw"], "model_total": row["model_total_raw"],
                     "model_p_home": row["p_home_win_markov"]})
    snaps = build_snapshots(pd.DataFrame(proj), matched, reader.lines(), now, MODEL_VERSION)
    if not snaps.empty:
        lake.write("model_snapshots", snaps.merge(up[["game_id", "season"]], on="game_id"))
        _emit(snapshot_table(snaps))
    return snaps


def snapshot_table(snaps: pd.DataFrame) -> str:
    t = pd.DataFrame({
        "partido": snaps["away_team"] + " @ " + snaps["home_team"],
        "margen modelo": snaps["model_margin"].round(1), "margen mercado": (-snaps["line_spread"]).round(1),
        "edge spread": (snaps["model_margin"] + snaps["line_spread"]).round(1),
        "total modelo": snaps["model_total"].round(1), "total mercado": snaps["line_total"],
        "edge total": (snaps["model_total"] - snaps["line_total"]).round(1),
        "P local modelo": snaps["model_p_home"].round(3), "P local mercado": snaps["line_ml"].round(3),
    })
    return "Snapshot del modelo vs línea actual del tracker:\n" + t.to_string(index=False)


def run_report(cfg: EngineConfig, tracker_db: Path = DEFAULT_TRACKER_DB,
               publish: bool = False) -> pd.DataFrame:
    """Califica los picks de los snapshots (primer snapshot por partido-mercado = pick oficial)."""
    lake = DataLake(cfg.paths)
    snaps = lake.read("model_snapshots")
    if snaps.empty:
        _emit("Aún no hay snapshots del modelo: ejecute primero `track-snapshot`")
        return pd.DataFrame()
    reader = OddsTrackerReader(tracker_db)
    commence = pd.to_datetime(snaps["commence_time"], utc=True)
    done = commence < pd.Timestamp.now(tz="UTC") - RESULTS_GRACE
    if done.any():  # resultados de los partidos ya terminados (pretemporada, regular y playoffs)
        DataIngestionLayer(cfg, lake).ingest_range((commence[done].min() - US_DATE_SHIFT).date(),
                                                   (commence[done].max() - US_DATE_SHIFT).date(),
                                                   season_types=(1, 2, 3))
    games = lake.read("games")
    results = games[games["game_id"].isin(snaps["game_id"])][["game_id", "home_score", "away_score"]]
    picks = pick_table(snaps, reader.lines(), results, reader.alerts(), reader.splits())
    official = first_snapshot_picks(picks)
    summary = summarize(official)
    drift = model_vs_market_drift(snaps)
    out = cfg.paths.root / "reports"
    out.mkdir(parents=True, exist_ok=True)
    picks.to_csv(out / "tracker_picks_all_snapshots.csv", index=False)
    official.to_csv(out / "tracker_picks.csv", index=False)
    summary.to_csv(out / "tracker_summary.csv", index=False)
    drift.to_csv(out / "tracker_model_vs_market_drift.csv", index=False)
    ledger = write_ledger(official, summary)
    _emit(f"Ledger actualizado: {ledger}")
    if publish:
        _emit(f"Publicación en GitHub: {publish_ledger(label=pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d'))}")
    pd.set_option("display.width", 220)
    _emit("WR de los picks (primer snapshot por partido y mercado):\n"
          + (summary.round(3).to_string(index=False) if not summary.empty else "(sin picks)"))
    if not drift.empty:
        _emit("\nModelo vs mercado entre snapshots:\n"
              + drift.groupby(["market", "estado"]).size().rename("partidos").to_string())
    return summary
