"""Publica el ledger en GitHub: commit (sólo de ledger/) + push, sin tocar el resto del árbol."""

from __future__ import annotations

import subprocess
from pathlib import Path

from nba_quant.ledger import DEFAULT_LEDGER_DIR, PROJECT_ROOT
from nba_quant.logging_utils import get_logger

log = get_logger("publish")
GIT_TIMEOUT_S = 120
COMMIT_PREFIX = "chore(ledger): picks al"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          timeout=GIT_TIMEOUT_S, check=False)


def publish_ledger(repo: Path = PROJECT_ROOT, ledger_dir: Path = DEFAULT_LEDGER_DIR,
                   label: str = "") -> str:
    """Hace commit de ledger/ si cambió y lo sube a origin. Devuelve 'sin cambios', 'publicado' o
    el error de git (no lanza excepción: un fallo de red no debe tumbar el reporte)."""
    rel = ledger_dir.resolve().relative_to(repo.resolve()).as_posix()
    if _git(repo, "rev-parse", "--is-inside-work-tree").returncode != 0:
        return f"error: {repo} no es un repositorio git"
    _git(repo, "add", "--", rel)
    if _git(repo, "diff", "--cached", "--quiet", "--", rel).returncode == 0:
        return "sin cambios"
    # Sólo se confirma ledger/: cualquier otro archivo en stage queda fuera del commit.
    commit = _git(repo, "commit", "-m", f"{COMMIT_PREFIX} {label}".strip(), "--", rel)
    if commit.returncode != 0:
        return f"error en commit: {commit.stderr.strip() or commit.stdout.strip()}"
    # GitHub Actions también liquida el ledger: se rebasa sobre origin y, si ambos tocaron ledger/,
    # gana la versión local (-X theirs en un rebase = el commit que se reaplica), que ve el tracker.
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    has_remote_branch = _git(repo, "ls-remote", "--exit-code", "--heads", "origin", branch).returncode == 0
    pull = _git(repo, "pull", "--rebase", "--autostash", "-X", "theirs", "origin", branch) if has_remote_branch else None
    if pull is not None and pull.returncode != 0:
        _git(repo, "rebase", "--abort")
        log.error("Rebase del ledger falló: %s", pull.stderr.strip())
        return f"error en pull: {pull.stderr.strip()}"
    push = _git(repo, "push", "origin", "HEAD")
    if push.returncode != 0:
        log.error("Push del ledger falló: %s", push.stderr.strip())
        return f"error en push: {push.stderr.strip()}"
    return "publicado"
