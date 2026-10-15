"""End-to-end tests for the standards-only hybrid KEM (ML-KEM + X25519)."""

from __future__ import annotations

import pytest

from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.hybrid_kem import PROFILES, HybridKEM, default_drbg


def _drbg() -> DRBG:
    d = DRBG()
    d.instantiate(b"\xab" * 32, b"\xcd" * 16, b"hybrid-test")
    return d


@pytest.mark.parametrize("profile", PROFILES)
def test_roundtrip(profile):
    h = HybridKEM(profile=profile)
    pk, sk = h.keygen(_drbg())
    ct, ss = h.encaps(pk, _drbg())
    assert h.decaps(sk, ct) == ss
    assert len(ss) == 32
    assert h.is_post_quantum


@pytest.mark.parametrize("profile", PROFILES)
def test_corrupted_ct_changes_secret(profile):
    h = HybridKEM(profile=profile)
    pk, sk = h.keygen(_drbg())
    ct, ss = h.encaps(pk, _drbg())
    bad = bytearray(ct)
    bad[-1] ^= 0x01  # land the flip in the classical ciphertext for both profiles
    assert h.decaps(sk, bytes(bad)) != ss


@pytest.mark.parametrize("profile", PROFILES)
def test_independent_keys_yield_different_ss(profile):
    h = HybridKEM(profile=profile)
    pk1, _ = h.keygen(_drbg())
    d2 = DRBG()
    d2.instantiate(b"\x55" * 32, b"\x66" * 16, b"second")
    pk2, _ = h.keygen(d2)
    _, ss1 = h.encaps(pk1, _drbg())
    _, ss2 = h.encaps(pk2, _drbg())
    assert ss1 != ss2


@pytest.mark.parametrize("profile", PROFILES)
def test_mismatched_sk_yields_different_ss(profile):
    """A different secret key must not reproduce the secret (hybrid binding)."""
    h = HybridKEM(profile=profile)
    pk, _ = h.keygen(_drbg())
    ct, ss = h.encaps(pk, _drbg())
    d2 = DRBG()
    d2.instantiate(b"\x77" * 32, b"\x88" * 16, b"other")
    _, sk_diff = h.keygen(d2)
    assert h.decaps(sk_diff, ct) != ss


def test_categories():
    assert HybridKEM(profile="xwing").nist_category == 3
    assert HybridKEM(profile="mlkem1024+x25519").nist_category == 5


def test_unknown_profile_rejected():
    with pytest.raises(ValueError):
        HybridKEM(profile="bogus")


def test_mlkem1024_truncated_blob_rejected():
    h = HybridKEM(profile="mlkem1024+x25519")
    pk, sk = h.keygen(_drbg())
    ct, _ = h.encaps(pk, _drbg())
    with pytest.raises(ValueError):
        h.decaps(sk, ct[:-5])


def test_default_drbg_runs_health_tested():
    # Smoke test: the convenience seeding path produces a usable keypair.
    h = HybridKEM(profile="xwing")
    pk, sk = h.keygen(default_drbg())
    ct, ss = h.encaps(pk, default_drbg())
    assert h.decaps(sk, ct) == ss
