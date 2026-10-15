"""Known-answer tests for ML-KEM (FIPS 203), pinned to NIST ACVP vectors.

Deterministic directions only (keygen-from-seed and decapsulation); FIPS 203
encapsulation is randomised and pyca exposes no message-injection hook, so
encaps conformance is covered by the round-trip test instead.
"""

from __future__ import annotations

import json
import os

import pytest

from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.kem_standard.mlkem_wrapper import MLKEMWrapper

_VEC = os.path.join(os.path.dirname(__file__), "kat_vectors", "mlkem_fips203_acvp.json")
with open(_VEC) as f:
    VECTORS = json.load(f)


@pytest.mark.parametrize("level", [768, 1024])
def test_keygen_seed_to_pk(level):
    """ML-KEM.KeyGen(d, z) reproduces the ACVP encapsulation key."""
    from cryptography.hazmat.primitives.asymmetric import mlkem

    v = VECTORS[str(level)]
    seed = bytes.fromhex(v["d"]) + bytes.fromhex(v["z"])
    cls = mlkem.MLKEM768PrivateKey if level == 768 else mlkem.MLKEM1024PrivateKey
    pk = cls.from_seed_bytes(seed).public_key().public_bytes_raw()
    assert pk.hex() == v["pk"]


@pytest.mark.parametrize("level", [768, 1024])
@pytest.mark.parametrize("pair", [("ct_n", "ss_n"), ("ct", "ss")])
def test_decaps(level, pair):
    """ML-KEM.Decaps reproduces the ACVP shared secret (incl. implicit reject)."""
    from cryptography.hazmat.primitives.asymmetric import mlkem

    v = VECTORS[str(level)]
    seed = bytes.fromhex(v["d"]) + bytes.fromhex(v["z"])
    cls = mlkem.MLKEM768PrivateKey if level == 768 else mlkem.MLKEM1024PrivateKey
    priv = cls.from_seed_bytes(seed)
    ct, ss = pair
    assert priv.decapsulate(bytes.fromhex(v[ct])).hex() == v[ss]


@pytest.mark.parametrize("level", [768, 1024])
def test_wrapper_roundtrip(level):
    w = MLKEMWrapper(level=level)
    d = DRBG.seeded_from_os()
    pk, sk = w.keygen(d)
    assert len(pk) == w.pk_len
    ct, ss = w.encaps(pk, d)
    assert len(ct) == w.ct_len
    assert w.decaps(sk, ct) == ss
    assert len(ss) == 32


@pytest.mark.parametrize("level", [768, 1024])
def test_wrapper_keygen_deterministic_from_drbg(level):
    """Same DRBG seed -> same keypair (what the KATs and cross-checks rely on)."""
    w = MLKEMWrapper(level=level)

    def drbg():
        d = DRBG()
        d.instantiate(b"\x01" * 32, b"\x02" * 16, b"kat")
        return d

    pk1, sk1 = w.keygen(drbg())
    pk2, sk2 = w.keygen(drbg())
    assert pk1 == pk2 and sk1 == sk2
