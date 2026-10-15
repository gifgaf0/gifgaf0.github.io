"""Known-answer tests for Ed25519 and Ed448, pinned to RFC 8032.

EdDSA signing is deterministic, so these cover the full signing direction.
"""

from __future__ import annotations

import json
import os

import pytest

from hybrid_kem.sig_classical.eddsa import Ed448Leg, Ed25519Leg

_DIR = os.path.join(os.path.dirname(__file__), "kat_vectors")


def _load(name):
    with open(os.path.join(_DIR, name)) as f:
        return json.load(f)


ED25519 = _load("ed25519_rfc8032.json")
ED448 = _load("ed448_rfc8032.json")


@pytest.mark.parametrize("v", ED25519)
def test_ed25519_sign_and_verify(v):
    leg = Ed25519Leg()
    sk, pk, msg, sig = (bytes.fromhex(v[k]) for k in ("sk", "pk", "msg", "sig"))
    assert leg.public_from_private(sk) == pk
    assert leg.sign(sk, msg) == sig            # deterministic signing KAT
    assert leg.verify(pk, sig, msg)


@pytest.mark.parametrize("v", ED448)
def test_ed448_sign_and_verify(v):
    leg = Ed448Leg()
    sk, pk, msg, sig = (bytes.fromhex(v[k]) for k in ("sk", "pk", "msg", "sig"))
    assert leg.public_from_private(sk) == pk
    assert leg.sign(sk, msg) == sig            # deterministic signing KAT
    assert leg.verify(pk, sig, msg)


def test_ed25519_rejects_tampered():
    leg = Ed25519Leg()
    v = ED25519[1]
    pk, msg, sig = (bytes.fromhex(v[k]) for k in ("pk", "msg", "sig"))
    bad = bytearray(sig)
    bad[0] ^= 0x01
    assert not leg.verify(pk, bytes(bad), msg)
