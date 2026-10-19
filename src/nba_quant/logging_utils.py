"""Logging mínimo compartido por todos los módulos."""

from __future__ import annotations

import logging
import sys

_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Devuelve un logger hijo de 'nba_quant' con handler a stderr configurado una sola vez."""
    root = logging.getLogger("nba_quant")
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_FORMAT))
        root.addHandler(handler)
        root.setLevel(logging.INFO)
    return logging.getLogger(f"nba_quant.{name}")
