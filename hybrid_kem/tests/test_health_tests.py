"""Tests for entropy.health_tests."""

from __future__ import annotations

import os

import pytest

from hybrid_kem.entropy.health_tests import (
    HealthTests,
    apt_cutoff,
    rct_cutoff,
)


def test_rct_passes_uniform_random():
    ht = HealthTests()
    assert ht.update(os.urandom(100_000))
    assert ht.status()["state"] == "ok"


def test_rct_catches_stuck_byte():
    ht = HealthTests()
    cutoff = ht.status()["rct_cutoff"]
    payload = b"\x00" * (cutoff + 5)
    assert ht.update(payload) is False
    s = ht.status()
    assert s["state"] == "failed"
    assert "RCT" in s["failure_reason"]


def test_apt_passes_uniform_random():
    ht = HealthTests()
    assert ht.update(os.urandom(100_000))
    s = ht.status()
    assert s["state"] == "ok"


def test_apt_catches_biased_source():
    # Interleave a fixed reference byte with non-reference bytes so that
    # APT sees the reference at ~50% prevalence (massively over its 2^-7.5
    # threshold) while RCT never sees the reference adjacent to itself.
    biased = bytearray()
    others = iter(b for b in os.urandom(4096) if b != 0x00)
    for _ in range(2048):
        biased.append(0x00)
        try:
            biased.append(next(others))
        except StopIteration:
            others = iter(b for b in os.urandom(4096) if b != 0x00)
            biased.append(next(others))
    ht = HealthTests()
    ht.update(bytes(biased))
    assert ht.status()["state"] == "failed"
    assert "APT" in ht.status()["failure_reason"]


def test_state_sticky_after_failure():
    ht = HealthTests()
    cutoff = ht.status()["rct_cutoff"]
    ht.update(b"\xaa" * (cutoff + 1))
    assert ht.status()["state"] == "failed"
    assert ht.update(os.urandom(1024)) is False
    assert ht.status()["state"] == "failed"


def test_reset_clears_state():
    ht = HealthTests()
    cutoff = ht.status()["rct_cutoff"]
    ht.update(b"\x00" * (cutoff + 1))
    assert ht.status()["state"] == "failed"
    ht.reset()
    assert ht.status()["state"] == "ok"
    assert ht.update(os.urandom(1024))


def test_rct_cutoff_monotone_in_alpha():
    # Tighter alpha (smaller false-positive rate) should not lower the cutoff.
    c1 = rct_cutoff(2.0**-30, 7.5)
    c2 = rct_cutoff(2.0**-60, 7.5)
    assert c2 >= c1


def test_apt_cutoff_within_window():
    for w in (512, 1024):
        c = apt_cutoff(2.0**-30, 7.5, w)
        assert 1 < c <= w


def test_invalid_alpha_rejected():
    with pytest.raises(ValueError):
        rct_cutoff(0.0, 7.5)
    with pytest.raises(ValueError):
        rct_cutoff(1.0, 7.5)


def test_invalid_h_rejected():
    with pytest.raises(ValueError):
        rct_cutoff(0.5, 0.0)
