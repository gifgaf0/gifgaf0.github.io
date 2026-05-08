"""Tests for entropy.qrng_source."""

from __future__ import annotations

import os
from unittest import mock

import pytest

from hybrid_kem.entropy.health_tests import HealthTestFailure, HealthTests
from hybrid_kem.entropy.qrng_source import QRNGSource


def _mock_anu(payload_bytes: bytes):
    """Return a fetcher that yields ``payload_bytes`` chunked per ANU spec."""

    def fetcher(url, params):
        n = params["length"]
        chunk = payload_bytes[:n]
        return {"success": True, "data": list(chunk), "type": "uint8", "length": n}

    return mock.MagicMock(side_effect=fetcher)


def test_local_provider_no_network():
    src = QRNGSource(provider="local", mix_with_os=False)
    out = src.get_bytes(64)
    assert len(out) == 64
    assert src.status()["mode"] == "os_fallback"


def test_xor_mixing_alters_output():
    raw = b"\xaa" * 64
    src_mixed = QRNGSource(
        provider="anu", mix_with_os=True, fetcher=_mock_anu(raw)
    )
    src_raw = QRNGSource(
        provider="anu", mix_with_os=False, fetcher=_mock_anu(raw)
    )
    out_mixed = src_mixed.get_bytes(64)
    out_raw = src_raw.get_bytes(64)
    assert out_raw == raw
    assert out_mixed != raw  # /dev/urandom XOR is overwhelmingly distinct


def test_anu_response_parsing_uses_mock():
    raw = bytes(range(256)) * 4  # 1024 bytes
    fetcher = _mock_anu(raw)
    src = QRNGSource(provider="anu", mix_with_os=False, fetcher=fetcher)
    out = src.get_bytes(128)
    assert out == raw[:128]
    fetcher.assert_called()
    args, kwargs = fetcher.call_args
    assert args[0].startswith("https://qrng.anu.edu.au")


def test_cache_fallback_when_provider_fails():
    # Pre-populate cache by a successful fetch, then make subsequent fetches fail.
    raw = b"\x55" * 256
    call_count = {"n": 0}

    def fetcher(url, params):
        call_count["n"] += 1
        if call_count["n"] == 1:
            n = params["length"]
            return {"success": True, "data": list(raw[:n]), "length": n}
        raise ConnectionError("simulated outage")

    src = QRNGSource(provider="anu", mix_with_os=False, fetcher=fetcher)
    src.fetch_to_cache(256)
    out = src.get_bytes(128)
    assert out == raw[:128]
    # Now drain past the cache; should fall back to OS entropy without raising.
    out2 = src.get_bytes(256)
    assert len(out2) == 256
    assert src.status()["fetch_failures"] >= 1


def test_health_test_integration_catches_stuck_source():
    raw = b"\x00" * 4096
    ht = HealthTests()
    src = QRNGSource(
        provider="anu",
        mix_with_os=False,
        fetcher=_mock_anu(raw),
        health_test=ht,
    )
    with pytest.raises(HealthTestFailure):
        src.get_bytes(4096)
    assert ht.status()["state"] == "failed"


def test_idq_requires_api_key(monkeypatch):
    monkeypatch.delenv("IDQ_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        QRNGSource(provider="idq")


def test_unknown_provider_rejected():
    with pytest.raises(ValueError):
        QRNGSource(provider="bogus")


def test_status_keys_present():
    src = QRNGSource(provider="local")
    s = src.status()
    expected = {
        "provider", "cache_bytes_available", "last_fetch_time",
        "last_fetch_size", "fetch_failures", "health_test_state", "mode",
    }
    assert expected.issubset(s.keys())


def test_zero_request_rejected():
    src = QRNGSource(provider="local")
    with pytest.raises(ValueError):
        src.get_bytes(0)
