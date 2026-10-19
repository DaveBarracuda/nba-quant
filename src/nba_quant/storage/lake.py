"""Data lake local columnar: Parquet particionado por temporada + vistas DuckDB.

Layout:  <root>/lake/<tabla>/season=<YYYY>/data.parquet
Cada escritura es un *upsert* idempotente por claves primarias dentro de la partición,
de modo que reingestar un rango de fechas nunca duplica filas.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import duckdb
import pandas as pd

from nba_quant.config import PathsConfig
from nba_quant.logging_utils import get_logger

log = get_logger("lake")

# Claves primarias por tabla canónica (índice lógico season/date/game_id del spec 2).
TABLE_KEYS: dict[str, tuple[str, ...]] = {
    "games": ("game_id",),
    "pbp": ("game_id", "event_idx"),
    "odds": ("game_id", "provider"),
    "officials": ("game_id", "official"),
    "player_box": ("game_id", "player_id"),
    "injuries": ("snapshot_date", "team", "player_name"),
    "rosters": ("snapshot_date", "team", "player_id"),
    "model_snapshots": ("game_id", "snapshot_ts"),
    "team_features": ("season", "game_date", "team"),
    "team_game_metrics": ("game_id", "team"),
    "tracking_team": ("as_of_date", "team", "endpoint"),
    "predictions": ("game_id", "model_version"),
}


class DataLake:
    """Repositorio Parquet/DuckDB con upsert por partición de temporada."""

    def __init__(self, paths: PathsConfig) -> None:
        self.paths = paths
        self.paths.lake.mkdir(parents=True, exist_ok=True)

    def _table_dir(self, table: str) -> Path:
        return self.paths.lake / table

    def write(self, table: str, df: pd.DataFrame, keys: Sequence[str] | None = None) -> int:
        """Upsert de `df` en `table`. Devuelve el nº de filas recibidas."""
        if df is None or df.empty:
            return 0
        keys = tuple(keys or TABLE_KEYS.get(table, ()))
        missing = [k for k in keys if k not in df.columns]
        if missing:
            raise ValueError(f"Tabla {table}: faltan columnas clave {missing}")
        if "season" not in df.columns:
            raise ValueError(f"Tabla {table}: se requiere columna 'season' para particionar")
        written = 0
        for season, part in df.groupby("season", sort=True):
            part_dir = self._table_dir(table) / f"season={int(season)}"
            part_dir.mkdir(parents=True, exist_ok=True)
            target = part_dir / "data.parquet"
            merged = part.drop(columns=["season"])
            if target.exists():
                merged = pd.concat([pd.read_parquet(target), merged], ignore_index=True)
            if keys:
                dedupe = [k for k in keys if k != "season"]
                merged = merged.drop_duplicates(subset=dedupe, keep="last")
            tmp = target.with_suffix(".tmp")
            merged.to_parquet(tmp, index=False)
            tmp.replace(target)  # escritura atómica
            written += len(part)
        log.info("lake.write table=%s rows=%d", table, written)
        return written

    def read(self, table: str, seasons: Sequence[int] | None = None) -> pd.DataFrame:
        """Lee una tabla completa (o un subconjunto de temporadas) a pandas."""
        base = self._table_dir(table)
        if not base.exists():
            return pd.DataFrame()
        frames = []
        for part_dir in sorted(base.glob("season=*")):
            season = int(part_dir.name.split("=")[1])
            if seasons is not None and season not in seasons:
                continue
            f = part_dir / "data.parquet"
            if f.exists():
                frames.append(pd.read_parquet(f).assign(season=season))
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def connect(self) -> duckdb.DuckDBPyConnection:
        """Conexión DuckDB con una vista por tabla sobre los Parquet (lectura columnar)."""
        con = duckdb.connect(str(self.paths.duckdb_file))
        for table_dir in sorted(p for p in self.paths.lake.iterdir() if p.is_dir()):
            if not list(table_dir.glob("season=*/data.parquet")):
                continue
            glob = (table_dir / "season=*" / "data.parquet").as_posix()
            con.execute(
                f"CREATE OR REPLACE VIEW {table_dir.name} AS "
                f"SELECT * FROM read_parquet('{glob}', hive_partitioning=true, union_by_name=true)"
            )
        return con
