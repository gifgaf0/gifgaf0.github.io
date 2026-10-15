"""Known-answer tests for ML-DSA (FIPS 204), pinned to NIST ACVP vectors.

Deterministic directions only: keygen-from-seed and verification of the
published signature. FIPS 204 hedged signing is randomised; signing is covered
by the round-trip test.
"""

from __future__ import annotations

import json
import os

import pytest

from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.sig_standard.mldsa_wrapper import MLDSAWrapper

_VEC = os.path.join(os.path.dirname(__file__), "kat_vectors", "mldsa_fips204_acvp.json")
with open(_VEC) as f:
    VECTORS = json.load(f)


@pytest.mark.parametrize("level", [44, 65, 87])
def test_keygen_seed_to_pk(level):
    from cryptography.hazmat.primitives.asymmetric import mldsa

    v = VECTORS[str(level)]
    cls = {
        44: mldsa.MLDSA44PrivateKey,
        65: mldsa.MLDSA65PrivateKey,
        87: mldsa.MLDSA87PrivateKey,
    }[level]
    pk = cls.from_seed_bytes(bytes.fromhex(v["xi"])).public_key().public_bytes_raw()
    assert pk.hex() == v["pk"]


@pytest.mark.parametrize("level", [44, 65, 87])
def test_verify_published_signature(level):
    """The ACVP ``sm`` is signature||message; verifying it must succeed, and a
    flipped bit must fail."""
    w = MLDSAWrapper(level=level)
    v = VECTORS[str(level)]
    sm = bytes.fromhex(v["sm"])
    sig, msg = sm[: w.sig_len], sm[w.sig_len:]
    assert msg.hex() == v["msg"]
    ctx = bytes.fromhex(v["ctx"])
    assert w.verify(bytes.fromhex(v["pk"]), sig, msg, ctx)
    bad = bytearray(sig)
    bad[0] ^= 0x01
    assert not w.verify(bytes.fromhex(v["pk"]), bytes(bad), msg, ctx)


@pytest.mark.parametrize("level", [44, 65, 87])
def test_wrapper_roundtrip(level):
    w = MLDSAWrapper(level=level)
    d = DRBG.seeded_from_os()
    pk, sk = w.keygen(d)
    assert len(pk) == w.pk_len
    sig = w.sign(sk, b"hello", context=b"app")
    assert len(sig) == w.sig_len
    assert w.verify(pk, sig, b"hello", context=b"app")
    assert not w.verify(pk, sig, b"hello", context=b"")       # wrong context
    assert not w.verify(pk, sig, b"goodbye", context=b"app")  # wrong message
