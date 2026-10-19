"""Clientes HTTP con rate limit por host, reintentos exponenciales y caché JSON en disco.

Sync (requests) para fuentes con bloqueo agresivo (B-Ref, stats.nba.com) y
async (aiohttp) para fuentes que toleran concurrencia (ESPN, The Odds API).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import random
import threading
import time
from pathlib import Path
from typing import Any

import aiohttp
import requests

from nba_quant.config import HttpConfig
from nba_quant.logging_utils import get_logger

log = get_logger("http")

RETRY_STATUS = {429, 500, 502, 503, 504}


class HttpError(RuntimeError):
    """Fallo definitivo tras agotar reintentos (o 4xx no reintentable)."""


class NonRetryableHttpError(HttpError):
    """4xx distinto de 429: reintentar no ayuda."""


def _cache_path(cache_dir: Path | None, url: str, params: dict | None) -> Path | None:
    if cache_dir is None:
        return None
    key = hashlib.sha1(f"{url}|{json.dumps(params or {}, sort_keys=True)}".encode()).hexdigest()
    return cache_dir / f"{key}.json"


def _backoff(cfg: HttpConfig, attempt: int) -> float:
    return cfg.backoff_base_sec * (2**attempt) + random.uniform(0, 0.5)


class RateLimiter:
    """Intervalo mínimo entre llamadas (thread-safe)."""

    def __init__(self, min_interval_sec: float) -> None:
        self.min_interval = min_interval_sec
        self._last = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        with self._lock:
            delta = time.monotonic() - self._last
            if delta < self.min_interval:
                time.sleep(self.min_interval - delta)
            self._last = time.monotonic()


class SyncHttpClient:
    """GET JSON/texto con rate limit, reintentos y caché opcional."""

    def __init__(
        self,
        cfg: HttpConfig,
        min_interval_sec: float,
        extra_headers: dict[str, str] | None = None,
        cache_dir: Path | None = None,
    ) -> None:
        self.cfg = cfg
        self.limiter = RateLimiter(min_interval_sec)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": cfg.user_agent, **(extra_headers or {})})
        self.cache_dir = cache_dir
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)

    def get_text(self, url: str, params: dict | None = None) -> str:
        last_exc: Exception | None = None
        for attempt in range(self.cfg.max_retries):
            self.limiter.wait()
            try:
                resp = self.session.get(url, params=params, timeout=self.cfg.timeout_sec)
            except requests.RequestException as exc:
                last_exc = exc
            else:
                if resp.status_code < 400:
                    return resp.text
                if resp.status_code not in RETRY_STATUS:
                    raise NonRetryableHttpError(f"HTTP {resp.status_code} en {url}")
                last_exc = HttpError(f"HTTP {resp.status_code}")
            sleep = _backoff(self.cfg, attempt)
            log.warning("GET %s falló (%s); reintento %d en %.1fs", url, last_exc, attempt + 1, sleep)
            time.sleep(sleep)
        raise HttpError(f"GET {url} agotó reintentos: {last_exc}")

    def get_json(self, url: str, params: dict | None = None, use_cache: bool = True) -> Any:
        path = _cache_path(self.cache_dir, url, params) if use_cache else None
        if path is not None and path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        data = json.loads(self.get_text(url, params))
        if path is not None:
            path.write_text(json.dumps(data), encoding="utf-8")
        return data


class AsyncHttpClient:
    """Cliente aiohttp con semáforo de concurrencia, intervalo mínimo y caché en disco."""

    def __init__(self, cfg: HttpConfig, min_interval_sec: float, cache_dir: Path | None = None) -> None:
        self.cfg = cfg
        self.min_interval = min_interval_sec
        self.cache_dir = cache_dir
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)
        self._sem = asyncio.Semaphore(cfg.max_concurrency)
        self._lock = asyncio.Lock()
        self._last = 0.0
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "AsyncHttpClient":
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.cfg.timeout_sec),
            headers={"User-Agent": self.cfg.user_agent},
        )
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._session:
            await self._session.close()

    async def _throttle(self) -> None:
        async with self._lock:
            delta = time.monotonic() - self._last
            if delta < self.min_interval:
                await asyncio.sleep(self.min_interval - delta)
            self._last = time.monotonic()

    async def get_json(self, url: str, params: dict | None = None, use_cache: bool = True) -> Any:
        if self._session is None:
            raise RuntimeError("AsyncHttpClient debe usarse como 'async with'")
        path = _cache_path(self.cache_dir, url, params) if use_cache else None
        if path is not None and path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        last_exc: Exception | None = None
        async with self._sem:
            for attempt in range(self.cfg.max_retries):
                await self._throttle()
                try:
                    async with self._session.get(url, params=params) as resp:
                        if resp.status < 400:
                            data = await resp.json(content_type=None)
                            if path is not None:
                                path.write_text(json.dumps(data), encoding="utf-8")
                            return data
                        if resp.status not in RETRY_STATUS:
                            raise NonRetryableHttpError(f"HTTP {resp.status} en {url}")
                        last_exc = HttpError(f"HTTP {resp.status}")
                except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                    last_exc = exc
                log.warning("GET %s falló (%s); reintento %d", url, last_exc, attempt + 1)
                await asyncio.sleep(_backoff(self.cfg, attempt))
        raise HttpError(f"GET {url} agotó reintentos: {last_exc}")
