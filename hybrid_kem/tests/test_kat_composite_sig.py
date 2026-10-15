"""Known-answer tests for composite ML-DSA + EdDSA, pinned to draft-19 App. E.

Verification is deterministic and runs both component checks and the M'
construction, so a wrong prefix, label, pre-hash, context handling, or split
point fails here. Signing is hedged (ML-DSA) so it is covered by round-trips.
"""

from __future__ import annotations

import base64
import json
import os

import pytest

from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.sig_composite.composite_mldsa import PROFILES, CompositeMLDSA

_VEC = os.path.join(
    os.path.dirname(__file__), "kat_vectors", "composite_sigs_draft19.json"
)
with open(_VEC) as f:
    DATA = json.load(f)

_b64 = base64.b64decode
MESSAGE = _b64(DATA["m"])
CONTEXT = _b64(DATA["ctx"])
CASES = {c["tcId"]: c for c in DATA["tests"]}


@pytest.mark.parametrize("tc_id", list(CASES))
def test_profile_is_known(tc_id):
    assert tc_id in PROFILES


@pytest.mark.parametrize("tc_id", list(CASES))
def test_keygen_seed_to_pk(tc_id):
    c = CASES[tc_id]
    comp = CompositeMLDSA(profile=tc_id)
    sk = _b64(c["sk"])
    seed_m, sk_t = sk[:32], sk[32:]
    pk_m, _ = comp._mldsa.keygen(_FixedDRBG(seed_m))
    pk_t = comp._trad.public_from_private(sk_t)
    assert (pk_m + pk_t) == _b64(c["pk"])


@pytest.mark.parametrize("tc_id", list(CASES))
def test_verify_published_signature_no_context(tc_id):
    c = CASES[tc_id]
    comp = CompositeMLDSA(profile=tc_id)
    assert comp.verify(_b64(c["pk"]), _b64(c["s"]), MESSAGE, b"")


@pytest.mark.parametrize("tc_id", list(CASES))
def test_verify_published_signature_with_context(tc_id):
    c = CASES[tc_id]
    comp = CompositeMLDSA(profile=tc_id)
    assert comp.verify(_b64(c["pk"]), _b64(c["sWithContext"]), MESSAGE, CONTEXT)


@pytest.mark.parametrize("tc_id", list(CASES))
def test_context_binding(tc_id):
    """The no-context signature must not verify under the context, and vice versa."""
    c = CASES[tc_id]
    comp = CompositeMLDSA(profile=tc_id)
    assert not comp.verify(_b64(c["pk"]), _b64(c["s"]), MESSAGE, CONTEXT)
    assert not comp.verify(_b64(c["pk"]), _b64(c["sWithContext"]), MESSAGE, b"")


@pytest.mark.parametrize("tc_id", list(CASES))
def test_both_components_required(tc_id):
    """Flipping a byte in either component signature must fail verification."""
    c = CASES[tc_id]
    comp = CompositeMLDSA(profile=tc_id)
    sig = bytearray(_b64(c["s"]))
    sig[0] ^= 0x01                         # ML-DSA component
    assert not comp.verify(_b64(c["pk"]), bytes(sig), MESSAGE, b"")
    sig = bytearray(_b64(c["s"]))
    sig[-1] ^= 0x01                        # EdDSA component
    assert not comp.verify(_b64(c["pk"]), bytes(sig), MESSAGE, b"")


@pytest.mark.parametrize("tc_id", list(CASES))
def test_roundtrip(tc_id):
    comp = CompositeMLDSA(profile=tc_id)
    pk, sk = comp.keygen(DRBG.seeded_from_os())
    sig = comp.sign(sk, b"attest this", context=b"ctx")
    assert len(sig) == comp.sig_len and len(pk) == comp.pk_len
    assert comp.verify(pk, sig, b"attest this", context=b"ctx")
    assert not comp.verify(pk, sig, b"attest this", context=b"")


class _FixedDRBG:
    """Minimal DRBG stand-in that yields a preset seed then zeros."""

    def __init__(self, seed: bytes) -> None:
        self._buf = seed

    def generate(self, n: int) -> bytes:
        out = (self._buf + b"\x00" * n)[:n]
        self._buf = b""
        return out
