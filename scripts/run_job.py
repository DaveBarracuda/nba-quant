"""Lanzador para tareas programadas: ejecuta la CLI de nba_quant sin instalar el paquete.

    python scripts/run_job.py track-snapshot --hours 36
    python scripts/run_job.py track-report
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

# Bajo pythonw.exe (tareas programadas, sin consola) sys.stdout/stderr son None: cualquier
# escritura rompería la tarea. Se redirigen a un log que se puede revisar después.
if sys.stdout is None or sys.stderr is None:
    LOG = ROOT / "data" / "reports" / "jobs.log"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    _log_file = open(LOG, "a", encoding="utf-8", buffering=1)  # noqa: SIM115 (vive todo el proceso)
    sys.stdout = sys.stdout or _log_file
    sys.stderr = sys.stderr or _log_file

from nba_quant.cli import main  # noqa: E402

if __name__ == "__main__":
    main(sys.argv[1:])
