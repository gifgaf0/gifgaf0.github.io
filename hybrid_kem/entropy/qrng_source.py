"""Cloud QRNG source with on-disk cache, OS mixing, and health-test gating.

Providers:
- ``"anu"``  Australian National University public QRNG (HTTPS, rate-limited).
- ``"idq"``  ID Quantique cloud QRNG. Requires ``IDQ_API_KEY`` env var.
- ``"local"`` /dev/urandom only. No network. Default for tests/dev.

Mixing:
By default the source XORs cloud bytes with an equal-length /dev/urandom
buffer. This way compromise of either source alone does not compromise the
seed, and the cloud provider does not learn the final entropy.

Network calls use a small, injectable HTTP client so tests can mock them
without monkey-patching ``requests``.
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from .health_tests import HealthTestFailure, HealthTests

LOG = logging.getLogger(__name__)

ANU_ENDPOINT = "https://qrng.anu.edu.au/API/jsonI.php"
IDQ_ENDPOINT_ENV = "IDQ_QRNG_ENDPOINT"
IDQ_KEY_ENV = "IDQ_API_KEY"

# ANU caps a single request at 1024 uint8 values; we stay below that.
ANU_MAX_BATCH = 1024


HttpFetcher = Callable[[str, dict], dict]
"""HTTP fetcher signature. Takes (url, params) and returns parsed JSON."""


def _default_fetcher(url: str, params: dict) -> dict:
    # Lazy import so the module works in environments without ``requests`` as
    # long as no real network call is ever made.
    import requests  # type: ignore[import-not-found]

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _xor(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("XOR operands must match length")
    return bytes(x ^ y for x, y in zip(a, b))


@dataclass
class QRNGStatus:
    provider: str
    cache_bytes_available: int
    last_fetch_time: Optional[datetime]
    last_fetch_size: int
    fetch_failures: int
    health_test_state: str
    mode: str

    def asdict(self) -> dict:
        return {
            "provider": self.provider,
            "cache_bytes_available": self.cache_bytes_available,
            "last_fetch_time": self.last_fetch_time,
            "last_fetch_size": self.last_fetch_size,
            "fetch_failures": self.fetch_failures,
            "health_test_state": self.health_test_state,
            "mode": self.mode,
        }


@dataclass
class QRNGSource:
    """Mixed cloud-QRNG entropy source with offline cache and health tests."""

    provider: str = "local"
    cache_size_bytes: int = 1024 * 1024
    mix_with_os: bool = True
    health_test: Optional[HealthTests] = None
    cache_path: Optional[Path] = None
    fetcher: HttpFetcher = field(default=_default_fetcher)

    _cache: bytearray = field(init=False, default_factory=bytearray)
    _lock: threading.Lock = field(init=False, default_factory=threading.Lock)
    _last_fetch_time: Optional[datetime] = field(init=False, default=None)
    _last_fetch_size: int = field(init=False, default=0)
    _fetch_failures: int = field(init=False, default=0)
    _last_mode: str = field(init=False, default="normal")

    def __post_init__(self) -> None:
        if self.provider not in ("anu", "idq", "local"):
            raise ValueError(f"unknown provider: {self.provider}")
        if self.provider == "idq" and not os.environ.get(IDQ_KEY_ENV):
            raise RuntimeError(f"provider 'idq' requires {IDQ_KEY_ENV} env var")
        if self.cache_path and self.cache_path.exists():
            with self.cache_path.open("rb") as f:
                self._cache = bytearray(f.read()[: self.cache_size_bytes])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_bytes(self, n: int) -> bytes:
        if n <= 0:
            raise ValueError("n must be positive")
        with self._lock:
            primary = self._collect_primary(n)
            if self.mix_with_os:
                primary = _xor(primary, os.urandom(n))
            if self.health_test is not None:
                if not self.health_test.update(primary):
                    raise HealthTestFailure(
                        f"health test failed: {self.health_test.status()['failure_reason']}"
                    )
            return primary

    def fetch_to_cache(self, n_bytes: int) -> int:
        with self._lock:
            return self._refill_cache(n_bytes)

    def status(self) -> dict:
        ht_state = self.health_test.status()["state"] if self.health_test else "n/a"
        return QRNGStatus(
            provider=self.provider,
            cache_bytes_available=len(self._cache),
            last_fetch_time=self._last_fetch_time,
            last_fetch_size=self._last_fetch_size,
            fetch_failures=self._fetch_failures,
            health_test_state=ht_state,
            mode=self._last_mode,
        ).asdict()

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _collect_primary(self, n: int) -> bytes:
        if self.provider == "local":
            self._last_mode = "os_fallback"
            return os.urandom(n)

        out = bytearray()
        # Drain cache first.
        if self._cache:
            take = min(len(self._cache), n)
            out.extend(self._cache[:take])
            del self._cache[:take]

        if len(out) < n:
            need = n - len(out)
            try:
                fresh = self._fetch_from_provider(need)
                out.extend(fresh)
                self._last_mode = "normal"
            except Exception as exc:  # network/provider failure
                LOG.warning("QRNG provider %s failed: %s; falling back", self.provider, exc)
                self._fetch_failures += 1
                if len(out) < n:
                    out.extend(os.urandom(n - len(out)))
                    self._last_mode = "os_fallback"
        else:
            self._last_mode = "cache"

        return bytes(out[:n])

    def _refill_cache(self, n_bytes: int) -> int:
        if self.provider == "local":
            return 0
        try:
            data = self._fetch_from_provider(n_bytes)
        except Exception as exc:
            LOG.warning("cache refill failed: %s", exc)
            self._fetch_failures += 1
            return 0
        room = self.cache_size_bytes - len(self._cache)
        keep = data[: max(0, room)]
        self._cache.extend(keep)
        if self.cache_path is not None:
            with self.cache_path.open("wb") as f:
                f.write(bytes(self._cache))
        return len(keep)

    def _fetch_from_provider(self, n_bytes: int) -> bytes:
        if self.provider == "anu":
            return self._fetch_anu(n_bytes)
        if self.provider == "idq":
            return self._fetch_idq(n_bytes)
        raise RuntimeError(f"no fetcher for provider {self.provider}")

    def _fetch_anu(self, n_bytes: int) -> bytes:
        out = bytearray()
        while len(out) < n_bytes:
            batch = min(ANU_MAX_BATCH, n_bytes - len(out))
            payload = self.fetcher(
                ANU_ENDPOINT,
                {"length": batch, "type": "uint8"},
            )
            if not payload.get("success"):
                raise RuntimeError(f"ANU error: {payload}")
            data = payload.get("data", [])
            if len(data) != batch:
                raise RuntimeError("ANU returned wrong length")
            out.extend(bytes(int(v) & 0xFF for v in data))
        self._last_fetch_time = datetime.utcnow()
        self._last_fetch_size = len(out)
        return bytes(out)

    def _fetch_idq(self, n_bytes: int) -> bytes:
        endpoint = os.environ.get(IDQ_ENDPOINT_ENV, "https://api.idquantique.com/qrng")
        api_key = os.environ[IDQ_KEY_ENV]
        payload = self.fetcher(endpoint, {"key": api_key, "bytes": n_bytes})
        # IDQ returns hex-encoded bytes under "data"; tolerate either form.
        if "data" not in payload:
            raise RuntimeError("IDQ response missing 'data'")
        data = payload["data"]
        raw = bytes.fromhex(data) if isinstance(data, str) else bytes(data)
        if len(raw) < n_bytes:
            raise RuntimeError("IDQ returned short")
        self._last_fetch_time = datetime.utcnow()
        self._last_fetch_size = n_bytes
        return raw[:n_bytes]
