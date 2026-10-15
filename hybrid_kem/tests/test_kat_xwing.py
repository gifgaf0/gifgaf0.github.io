"""Known-answer tests for X-Wing, pinned to draft-11 Appendix C.

Verifies byte-for-byte conformance in the two deterministic directions:
keygen (seed -> pk) and decapsulation ((sk, ct) -> ss). Decapsulation runs the
full combiner over both legs, so a wrong label, hash, or input order fails
here. Encapsulation is randomised (see module docstring of combiner.xwing) and
is covered by the round-trip test.
"""

from __future__ import annotations

import json
import os

import pytest

from hybrid_kem.combiner import xwing
from hybrid_kem.entropy.drbg import DRBG

_VEC = os.path.join(
    os.path.dirname(__file__), "kat_vectors", "xwing_draft11_appendix_c.json"
)
with open(_VEC) as f:
    VECTORS = json.load(f)


def test_label_is_draft_value():
    assert xwing.XWING_LABEL == bytes.fromhex("5c2e2f2f5e5c")


@pytest.mark.parametrize("idx", range(len(VECTORS)))
def test_keygen_seed_to_pk(idx):
    v = VECTORS[idx]
    sk, pk = xwing.generate_keypair_derand(bytes.fromhex(v["seed"]))
    assert sk.hex() == v["seed"]
    assert pk.hex() == v["pk"]
    assert len(pk) == xwing.PK_LEN


@pytest.mark.parametrize("idx", range(len(VECTORS)))
def test_decapsulate_to_ss(idx):
    v = VECTORS[idx]
    ss = xwing.decapsulate(bytes.fromhex(v["ct"]), bytes.fromhex(v["sk"]))
    assert ss.hex() == v["ss"]


def test_roundtrip_random():
    d = DRBG.seeded_from_os()
    sk, pk = xwing.generate_keypair(rng=d.generate)
    ss, ct = xwing.encapsulate(pk, rng=d.generate)
    assert xwing.decapsulate(ct, sk) == ss
    assert len(ct) == xwing.CT_LEN and len(ss) == xwing.SS_LEN


def test_wrong_ct_changes_secret():
    d = DRBG.seeded_from_os()
    sk, pk = xwing.generate_keypair(rng=d.generate)
    ss, ct = xwing.encapsulate(pk, rng=d.generate)
    bad = bytearray(ct)
    bad[-1] ^= 0x01  # flip a byte in the X25519 ciphertext
    assert xwing.decapsulate(bytes(bad), sk) != ss
