"""CLI del motor: ingesta -> features -> simulación -> tear sheet.

  python -m nba_quant.cli ingest   --start 2025-10-21 --end 2026-06-20
  python -m nba_quant.cli features --seasons 2026
  python -m nba_quant.cli simulate --date 2026-10-21            (pizarra futura desde ESPN)
  python -m nba_quant.cli simulate --game-ids 401810791          (partido ya jugado: re-proyección)
  python -m nba_quant.cli backtest --seasons 2026
  python -m nba_quant.cli backtest --seasons 2026 --mode context            (pila de contexto point-in-time)
  python -m nba_quant.cli calibrate --seasons 2026                          (rejilla shift/encogimiento)
  python -m nba_quant.cli demo                                   (liga sintética, sin red)
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from nba_quant import github_ledger, tracker_jobs
from nba_quant.config import DEFAULT_CONFIG, EngineConfig
from nba_quant.features.pipeline import NBAAdvancedFeaturePipeline
from nba_quant.ingestion.engine import DataIngestionLayer
from nba_quant.integrations.odds_tracker import DEFAULT_TRACKER_DB
from nba_quant.logging_utils import get_logger
from nba_quant.settle import run_settle
from nba_quant.simulation.slate import MODEL_VERSION, SlateSimulator
from nba_quant.storage.lake import DataLake

log = get_logger("cli")


def emit(text: str) -> None:
    if hasattr(sys.stdout, "reconfigure") and (sys.stdout.encoding or "").lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # consolas Windows cp1252
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def game_fouls(events: pd.DataFrame) -> pd.DataFrame:
    """Faltas y TL por partido (perfil arbitral)."""
    fouls = events[(events["event_type"] == "foul") & ~events["subtype"].fillna("").str.contains("Technical")]
    fta = events[(events["event_type"] == "free_throw") & ~events["ft_technical"]]
    return pd.DataFrame({"fouls": fouls.groupby("game_id").size(), "fta": fta.groupby("game_id").size()}).fillna(0).reset_index()


def build_features(cfg: EngineConfig, lake: DataLake, seasons: list[int] | None,
                   upcoming: pd.DataFrame | None = None) -> tuple[pd.DataFrame, NBAAdvancedFeaturePipeline]:
    pipe = NBAAdvancedFeaturePipeline(cfg, lake)
    feats = pipe.run(seasons, upcoming)
    played = feats[feats["target_margin"].notna()].reset_index()
    lake.write("team_features", played)
    return feats, pipe


def make_simulator(cfg: EngineConfig, feats: pd.DataFrame, pipe: NBAAdvancedFeaturePipeline,
                   odds: pd.DataFrame, officials: pd.DataFrame, extra_games: pd.DataFrame | None = None) -> SlateSimulator:
    games = pipe.games if extra_games is None else pd.concat([pipe.games, extra_games], ignore_index=True)
    return SlateSimulator(cfg, feats, games, odds, officials, game_fouls(pipe.events), pipe.player_box)


def report(projections: list, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in projections:
        emit(p.tear_sheet)
        if not p.props.empty:
            emit("Props (1.000 sims/jugador):\n" + p.props.round(2).to_string(index=False) + "\n")
        (out_dir / f"tear_sheet_{p.row['game_id']}.txt").write_text(p.tear_sheet, encoding="utf-8")


# ------------------------------------------------------------------------------ comandos
def cmd_ingest(cfg: EngineConfig, args: argparse.Namespace) -> None:
    lake = DataLake(cfg.paths)
    layer = DataIngestionLayer(cfg, lake)
    end = date.fromisoformat(args.end) if args.end else date.today() - timedelta(days=1)
    if args.start:
        start = date.fromisoformat(args.start)
    else:  # incremental: desde el día siguiente al último partido del lake
        games = lake.read("games")
        if games.empty:
            raise SystemExit("El lake está vacío: indique --start")
        start = pd.Timestamp(games["game_date"].max()).date() + timedelta(days=1)
    if start > end:
        emit(f"Lake al día (último partido {start - timedelta(days=1)})")
    else:
        emit(f"Ingesta {start} → {end}: " + str(layer.ingest_range(start, end, tuple(args.season_types))))
    if args.with_rosters:  # foto de plantillas: sólo cuenta como prior si es anterior al 1er partido regular
        emit(f"Plantillas: {len(layer.ingest_rosters())} jugadores")
    if args.with_injuries:
        emit(f"Lesiones: {len(layer.ingest_injuries())} filas")


def cmd_features(cfg: EngineConfig, args: argparse.Namespace) -> None:
    feats, _ = build_features(cfg, DataLake(cfg.paths), args.seasons)
    out = cfg.paths.root / "exports" / "team_features.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    feats.to_parquet(out)
    emit(f"Features: {feats.shape[0]} filas x {feats.shape[1]} columnas -> {out}")


def cmd_simulate(cfg: EngineConfig, args: argparse.Namespace) -> None:
    lake = DataLake(cfg.paths)
    layer = DataIngestionLayer(cfg, lake)
    odds, officials = lake.read("odds"), lake.read("officials")
    upcoming = pd.DataFrame()
    if args.date:
        d = date.fromisoformat(args.date)
        upcoming = layer.ingest_schedule(d, d)
        if upcoming.empty:
            emit(f"No hay partidos pendientes el {d}")
            return
        odds = pd.concat([odds, upcoming.reindex(columns=odds.columns)], ignore_index=True) if not odds.empty else upcoming
        officials = pd.concat([officials, upcoming[["game_id", "officials"]].explode("officials")
                               .rename(columns={"officials": "official"}).dropna()], ignore_index=True)
    feats, pipe = build_features(cfg, lake, args.seasons, upcoming if not upcoming.empty else None)
    extra = upcoming.drop(columns=["officials"], errors="ignore") if not upcoming.empty else None
    sim = make_simulator(cfg, feats, pipe, odds, officials, extra)
    if args.blend:  # mezcla con el cierre ajustada con el backtest point-in-time de la historia
        sim.fit_blender()
    ids = args.game_ids or upcoming["game_id"].tolist()
    preds, projections = sim.run(ids)
    if not preds.empty:
        lake.write("predictions", preds)
    report(projections, cfg.paths.root / "reports")
    if args.record_picks and not preds.empty:
        record_github_picks(preds, upcoming, args.blend)
    if not preds.empty:
        emit("\nPROYECCIÓN POR PARTIDO (spread proyectado, descendente):\n" + render_matchup_table(preds))


def record_github_picks(preds: pd.DataFrame, upcoming: pd.DataFrame, blended: bool) -> None:
    """Guarda en ledger/github/ los picks del modelo sin mezcla contra la línea actual de ESPN."""
    if blended:  # con --blend la P(local) ya está mezclada con el mercado: no es el pick del modelo
        emit("Picks no guardados: la corrida usó --blend (el ledger registra el modelo sin mezcla)")
        return
    if upcoming.empty:
        emit("Picks no guardados: sólo se registran partidos futuros (--date)")
        return
    snaps = github_ledger.build_espn_snapshots(preds, upcoming, pd.Timestamp.now(tz="UTC"), MODEL_VERSION)
    picks = github_ledger.record_picks(snaps)
    emit(f"Ledger de GitHub: {len(snaps) * 3} picks evaluados, {len(picks)} en el ledger "
         f"({github_ledger.GITHUB_LEDGER_DIR / 'LEDGER.md'})")


# ESPN usa abreviaturas de 2 letras para algunos equipos; en la tabla se muestran las de 3.
DISPLAY_ABBR = {"NY": "NYK", "SA": "SAS", "GS": "GSW", "NO": "NOP", "UTAH": "UTA", "WSH": "WAS"}
TABLE_RULE = "═"


def _vegas_line(home: str, away: str, spread_home: float) -> str:
    if pd.isna(spread_home):
        return "—"
    if spread_home == 0:
        return "PK"
    return f"{home} {spread_home:+.1f}" if spread_home < 0 else f"{away} {-spread_home:+.1f}"


def matchup_table(preds: pd.DataFrame) -> pd.DataFrame:
    """Un renglón por partido: línea de Vegas, equipo que el modelo ve ganar, su P(ganar), spread y
    marcador proyectados; ordenado por spread proyectado de mayor a menor."""
    rows = []
    for _, p in preds.iterrows():
        home, away = DISPLAY_ABBR.get(p["home_team"], p["home_team"]), DISPLAY_ABBR.get(p["away_team"], p["away_team"])
        margin, total = float(p["exp_margin"]), float(p["exp_total"])
        home_pts, away_pts = (total + margin) / 2, (total - margin) / 2
        pick_home = margin >= 0
        rows.append({
            "Matchup": f"{away} @ {home}",
            "Vegas_Line": _vegas_line(home, away, pd.to_numeric(p["market_spread_home"], errors="coerce")),
            "Model_Pick": home if pick_home else away,
            "Win_Prob": f"{(p['p_home_win_markov'] if pick_home else 1 - p['p_home_win_markov']):.1%}",
            "Proj_Spread": f"{home if pick_home else away} +{abs(margin):.1f} pts",
            "Model_Score": f"{away} {away_pts:.1f} – {home} {home_pts:.1f}",
            "Proj_Total": f"{total:.1f}",
            "_sort": abs(margin),
        })
    return pd.DataFrame(rows).sort_values("_sort", ascending=False).drop(columns="_sort")


def render_matchup_table(preds: pd.DataFrame) -> str:
    body = matchup_table(preds).to_string(index=False)
    rule = TABLE_RULE * max(len(line) for line in body.splitlines())
    return "\n".join([rule, body, rule])


def cmd_backtest(cfg: EngineConfig, args: argparse.Namespace) -> None:
    lake = DataLake(cfg.paths)
    feats, pipe = build_features(cfg, lake, args.seasons)
    sim = make_simulator(cfg, feats, pipe, lake.read("odds"), lake.read("officials"))
    bt = sim.backtest(args.min_games, args.n_sims, mode=args.mode)
    out = cfg.paths.root / "reports" / ("backtest.csv" if args.mode == "base" else f"backtest_{args.mode}.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    bt.to_csv(out, index=False)
    emit("Backtest: " + ", ".join(f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
                                  for k, v in bt.attrs.get("metrics", {}).items()))


def cmd_calibrate(cfg: EngineConfig, args: argparse.Namespace) -> None:
    from nba_quant.simulation.calibration import run_calibration

    lake = DataLake(cfg.paths)
    feats, pipe = build_features(cfg, lake, args.seasons)
    sim = make_simulator(cfg, feats, pipe, lake.read("odds"), lake.read("officials"))
    res = run_calibration(sim, args.min_games, workers=args.workers)
    out = cfg.paths.root / "reports"
    out.mkdir(parents=True, exist_ok=True)
    res["scores"].to_csv(out / "context_grid_scores.csv", index=False)
    res["reference"].to_csv(out / "context_vs_base_vs_market.csv", index=False)
    emit(res["reference"].round(4).to_string(index=False))
    emit(f"Split temporal: train < {res['split'].date()} <= test. Mejor configuración (train): {res['best']}")


def run_demo(cfg: EngineConfig | None = None) -> pd.DataFrame:
    """Pipeline completo sobre una liga sintética: ingesta (lake) -> features -> 7 bloques MC ->
    Markov 100k -> desvigado Shin -> RAE -> tear sheet. No requiere red."""
    import tempfile

    from nba_quant.config import PathsConfig
    from nba_quant.synthetic import generate_league

    base = cfg or DEFAULT_CONFIG
    tmp = Path(tempfile.mkdtemp(prefix="nba_quant_demo_"))
    cfg = replace(base, paths=PathsConfig(root=tmp), sim=replace(base.sim, n_sims_block=20_000, n_sims_markov=50_000))
    league = generate_league(n_teams=8, n_rounds=4, seed=11)
    lake = DataLake(cfg.paths)
    lake.write("games", league.games)
    lake.write("pbp", league.pbp)
    lake.write("player_box", league.player_box)
    lake.write("odds", league.odds)
    lake.write("officials", league.officials)
    last_day = league.games["game_date"].max()
    target = league.games[league.games["game_date"] == last_day]
    feats, pipe = build_features(cfg, lake, None)
    sim = make_simulator(cfg, feats, pipe, league.odds, league.officials)
    preds, projections = sim.run(target["game_id"].tolist()[:2])
    report(projections, tmp / "reports")
    bt = sim.backtest(min_games_played=6, n_sims=4_000)
    emit("Backtest sintético: " + str({k: round(v, 4) if isinstance(v, float) else v
                                       for k, v in bt.attrs.get("metrics", {}).items()}))
    emit(f"Lake de demo en {tmp}")
    return preds


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="nba-quant")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("ingest")
    p.add_argument("--start", help="por defecto: día siguiente al último partido del lake")
    p.add_argument("--end", help="por defecto: ayer")
    p.add_argument("--with-injuries", action="store_true")
    p.add_argument("--with-rosters", action="store_true")
    p.add_argument("--season-types", type=int, nargs="+", default=[2, 3], help="1 pretemporada, 2 regular, 3 playoffs")
    for name in ("features", "simulate", "backtest", "calibrate"):
        q = sub.add_parser(name)
        q.add_argument("--seasons", type=int, nargs="*", default=None)
        if name == "simulate":
            q.add_argument("--date")
            q.add_argument("--game-ids", nargs="*")
            q.add_argument("--blend", action="store_true",
                           help="mezclar modelo y línea de cierre (ajusta con un backtest previo, ~5 min)")
            q.add_argument("--record-picks", action="store_true",
                           help="guardar los picks en ledger/github/ (línea actual de ESPN)")
        if name in ("backtest", "calibrate"):
            q.add_argument("--min-games", type=int, default=10)
        if name == "backtest":
            q.add_argument("--mode", choices=("base", "context"), default="base")
            q.add_argument("--n-sims", type=int, default=None, help="base: totales; context: por celda 3×3")
        if name == "calibrate":
            q.add_argument("--workers", type=int, default=None)
    for name in ("track-snapshot", "track-report"):
        t = sub.add_parser(name, help="conexión con el NBA Odds Tracker (SQLite, sólo lectura)")
        t.add_argument("--tracker-db", type=Path, default=DEFAULT_TRACKER_DB)
        if name == "track-snapshot":
            t.add_argument("--hours", type=float, default=48.0, help="horizonte de partidos a proyectar")
            t.add_argument("--seasons", type=int, nargs="*", default=None)
        else:
            t.add_argument("--publish-ledger", action="store_true",
                           help="commit + push de ledger/ a GitHub (sólo si cambió)")
    sub.add_parser("settle-ledger", help="liquida ledger/picks.csv con marcadores de ESPN (sin lake ni tracker)")
    sub.add_parser("demo")
    args = parser.parse_args(argv)
    handlers = {"ingest": cmd_ingest, "features": cmd_features, "simulate": cmd_simulate,
                "backtest": cmd_backtest, "calibrate": cmd_calibrate, "demo": lambda c, a: run_demo(c),
                "track-snapshot": lambda c, a: tracker_jobs.run_snapshot(c, a.tracker_db, a.hours, a.seasons),
                "track-report": lambda c, a: tracker_jobs.run_report(c, a.tracker_db, a.publish_ledger),
                "settle-ledger": lambda c, a: emit(f"Picks liquidados: {run_settle()}")}
    handlers[args.cmd](DEFAULT_CONFIG, args)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_demo()  # set de datos de prueba completo, de la ingesta al reporte financiero
    else:
        main()
