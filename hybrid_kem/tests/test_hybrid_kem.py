"""End-to-end tests for the hybrid KEM."""

from __future__ import annotations

import pytest

from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.hybrid_kem import HybridKEM
from hybrid_kem.kem_slwe.slwe_wrapper import SLWEWrapper
from hybrid_kem.kem_standard.mlkem_wrapper import MLKEMWrapper


def _drbg() -> DRBG:
    d = DRBG()
    d.instantiate(b"\xab" * 32, b"\xcd" * 16, b"hybrid-test")
    return d


def test_standard_kem_roundtrip():
    kem = MLKEMWrapper(backend="x25519")
    pk, sk = kem.keygen(_drbg())
    ct, ss = kem.encaps(pk, _drbg())
    assert kem.decaps(sk, ct) == ss


def test_slwe_stub_roundtrip():
    s = SLWEWrapper(mode="stub")
    pk, sk = s.keygen(_drbg())
    ct, ss = s.encaps(pk, _drbg())
    assert s.decaps(sk, ct) == ss


def test_slwe_invalid_mode_rejected():
    with pytest.raises(NotImplementedError):
        SLWEWrapper(mode="full")
    with pytest.raises(ValueError):
        SLWEWrapper(mode="bogus")


def test_hybrid_keygen_encaps_decaps():
    h = HybridKEM(standard_backend="x25519", slwe_mode="stub")
    pk, sk = h.keygen(_drbg())
    ct, ss = h.encaps(pk, _drbg())
    ss2 = h.decaps(sk, ct)
    assert ss == ss2
    assert len(ss) == 32


def test_hybrid_corrupted_ct_changes_secret():
    h = HybridKEM(standard_backend="x25519", slwe_mode="stub")
    pk, sk = h.keygen(_drbg())
    ct, ss = h.encaps(pk, _drbg())
    # Flip a byte inside the ciphertext blob.
    bad = bytearray(ct)
    bad[10] ^= 0x01
    ss_bad = h.decaps(sk, bytes(bad))
    assert ss_bad != ss


def test_hybrid_truncated_blob_rejected():
    h = HybridKEM(standard_backend="x25519", slwe_mode="stub")
    pk, sk = h.keygen(_drbg())
    ct, _ = h.encaps(pk, _drbg())
    with pytest.raises(ValueError):
        h.decaps(sk, ct[:-5])


def test_hybrid_independent_keys_yield_different_ss():
    h = HybridKEM(standard_backend="x25519", slwe_mode="stub")
    pk1, sk1 = h.keygen(_drbg())
    d2 = DRBG()
    d2.instantiate(b"\x55" * 32, b"\x66" * 16, b"second")
    pk2, sk2 = h.keygen(d2)
    ct1, ss1 = h.encaps(pk1, _drbg())
    ct2, ss2 = h.encaps(pk2, _drbg())
    assert ss1 != ss2


def test_hybrid_mismatched_sk_yields_different_ss():
    """A mismatched sk must not produce the original ss; transcript binding holds."""
    h = HybridKEM(standard_backend="x25519", slwe_mode="stub")
    pk, sk = h.keygen(_drbg())
    _, sk_other = h.keygen(_drbg())  # fresh keygen, identical drbg → identical
    ct, ss = h.encaps(pk, _drbg())
    # Use an actually-different secret key.
    d2 = DRBG()
    d2.instantiate(b"\x77" * 32, b"\x88" * 16, b"other")
    _, sk_diff = h.keygen(d2)
    ss_bad = h.decaps(sk_diff, ct)
    assert ss_bad != ss
