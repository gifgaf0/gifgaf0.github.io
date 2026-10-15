"""Known-answer tests for X25519, pinned to RFC 7748 Section 5.2."""

from __future__ import annotations

import json
import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.kem_classical.x25519_kem import X25519KEM

_VEC = os.path.join(os.path.dirname(__file__), "kat_vectors", "x25519_rfc7748.json")
with open(_VEC) as f:
    VECTORS = json.load(f)


def _x25519(scalar: bytes, u: bytes) -> bytes:
    # The library computes scalar * basepoint, then DH; to multiply by an
    # arbitrary u-coordinate we treat u as a public key and exchange.
    priv = x25519.X25519PrivateKey.from_private_bytes(scalar)
    return priv.exchange(x25519.X25519PublicKey.from_public_bytes(u))


def test_rfc7748_single():
    v = VECTORS["single"][0]
    out = _x25519(bytes.fromhex(v["scalar"]), bytes.fromhex(v["u"]))
    assert out.hex() == v["out"]


def test_rfc7748_iterated_one_round():
    """After one iteration of the RFC 7748 iterative test, k == u == the base
    scalar 9 followed by zeros; verify the documented result."""
    k = bytearray(32)
    k[0] = 9
    u = bytes(k)
    out = _x25519(bytes(k), u)
    assert out.hex() == VECTORS["iterated_after_1"]


def test_leg_roundtrip():
    leg = X25519KEM()
    d = DRBG.seeded_from_os()
    pk, sk = leg.keygen(d)
    ct, ss = leg.encaps(pk, d)
    assert leg.decaps(sk, ct) == ss
    assert len(ss) == 32 and not leg.is_post_quantum
