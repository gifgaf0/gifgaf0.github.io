"""Tests for the Brief 03 IrrationalConditioner module."""

from __future__ import annotations

import os

import pytest

from hybrid_kem.entropy.drbg import DRBG, HMAC_SHA256
from hybrid_kem.entropy.health_tests import run_health_tests
from hybrid_kem.entropy.irrational_conditioner import (
    InsufficientEntropyError,
    IrrationalConditioner,
    OffsetExhaustedError,
)
from hybrid_kem.entropy.qrng_source import QRNGSource


# A single 10 000-digit instance is reused across most tests to keep the
# module fast. mpmath digit generation at this precision takes ~0.1 s but
# we only pay it once per module thanks to the fixture.


@pytest.fixture(scope="module")
def conditioner() -> IrrationalConditioner:
    return IrrationalConditioner(precision_digits=10_000)


# ---------------------------------------------------------------------------
# Functional
# ---------------------------------------------------------------------------


def test_output_length_matches_input(conditioner):
    for n in (16, 32, 48, 64, 128, 256):
        out = conditioner.condition(os.urandom(n))
        assert len(out) == n


def test_different_entropy_different_output(conditioner):
    a = conditioner.condition(os.urandom(32))
    b = conditioner.condition(os.urandom(32))
    assert a != b


def test_same_entropy_same_output():
    """With fixed jitter and offset namespace, same input → same output."""
    c1 = IrrationalConditioner(
        precision_digits=2000, _fake_jitter=b"\x01\x02\x03"
    )
    c2 = IrrationalConditioner(
        precision_digits=2000, _fake_jitter=b"\x01\x02\x03"
    )
    seed = b"deterministic-test-input-123456789ABCDEF"[:32]
    assert c1.condition(seed) == c2.condition(seed)


# ---------------------------------------------------------------------------
# Offset namespace
# ---------------------------------------------------------------------------


def test_offset_no_reuse_within_session(conditioner):
    starting = conditioner.offsets_used
    for _ in range(50):
        conditioner.condition(os.urandom(32))
    assert conditioner.offsets_used == starting + 50


def test_offset_exhausted_raises():
    """Tiny precision → tiny namespace → offsets exhaust quickly."""
    # precision 1000 -> max_offset = 1000 - 128 = 872 unique offsets.
    c = IrrationalConditioner(precision_digits=1000)
    consumed = 0
    with pytest.raises(OffsetExhaustedError):
        while consumed < c._max_offset + 2:
            c.condition(os.urandom(32))
            consumed += 1


# ---------------------------------------------------------------------------
# Jitter
# ---------------------------------------------------------------------------


def test_jitter_variance(conditioner):
    """Two condition() calls with the same input but live jitter should
    almost always differ. Live timing on any non-pathological host has
    nanosecond-scale variance well above the 3-byte jitter slot.
    """
    seed = os.urandom(32)
    a = conditioner.condition(seed)
    b = conditioner.condition(seed)
    assert a != b


# ---------------------------------------------------------------------------
# Statistical / health-test sanity
# ---------------------------------------------------------------------------


def test_output_passes_health_tests(conditioner):
    """A long buffer of urandom-seeded conditioner output should pass
    RCT/APT at a generous h_min — the conditioner must not introduce
    obvious structural defects (long runs, mass on one byte value)."""
    # Generate a long stream by concatenating many independent calls.
    blob = b"".join(conditioner.condition(os.urandom(32)) for _ in range(64))
    result = run_health_tests(blob, h_min=6.0)
    assert result.rct_passed, result
    assert result.apt_passed, result


def test_nist_sp80022_short(conditioner):
    """Minimal SP 800-22 subset: monobit + runs on 8 KiB of output."""
    blob = b"".join(
        conditioner.condition(os.urandom(32)) for _ in range(256)
    )
    bits = []
    for byte in blob:
        for k in range(8):
            bits.append((byte >> (7 - k)) & 1)
    n = len(bits)

    # Monobit: |#ones - #zeros| / sqrt(n) should be O(1).
    s = sum(1 if b == 1 else -1 for b in bits)
    s_obs = abs(s) / (n ** 0.5)
    # 99% two-sided z-cutoff ~ 2.576; allow generous margin.
    assert s_obs < 4.0, f"monobit s_obs={s_obs:.3f}"

    # Runs: count transitions, expected ~ n/2.
    transitions = sum(1 for i in range(1, n) if bits[i] != bits[i - 1])
    expected = (n - 1) / 2.0
    z = abs(transitions - expected) / ((n - 1) ** 0.5 * 0.5)
    assert z < 4.0, f"runs z={z:.3f}"


# ---------------------------------------------------------------------------
# Boundary / error paths
# ---------------------------------------------------------------------------


def test_insufficient_entropy_raises(conditioner):
    with pytest.raises(InsufficientEntropyError):
        conditioner.condition(b"short")


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


def test_pipeline_integration():
    """QRNGSource → run_health_tests → IrrationalConditioner →
    DRBG.instantiate is the canonical pipeline for this conditioner."""
    qrng = QRNGSource(provider="local")
    raw = qrng.get_bytes(48)
    health = run_health_tests(raw, h_min=6.0)
    assert health.passed
    cond = IrrationalConditioner(precision_digits=2000)
    mixed = cond.condition(raw)
    assert len(mixed) == 48
    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(entropy_input=mixed[:32], nonce=mixed[32:48])
    assert drbg.state == "instantiated"
    assert len(drbg.generate(64)) == 64
