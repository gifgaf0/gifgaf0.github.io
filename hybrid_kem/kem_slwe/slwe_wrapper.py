"""Module-SLWE KEM wrapper.

Modes:
- ``"stub"``  Deterministic 32-byte shared secret derived from the seed.
              Fast; used to validate combiner / hybrid integration without
              running the full lattice arithmetic on every iteration.
- ``"toy"``   Reserved for the existing ``sqt_slwe__1_.py`` toy parameters
              (p=911, k=4). Wired up in a follow-on brief.
- ``"full"``  Reserved for k=32, q≈2^32, mod-455 prime parameters.

The stub-mode shared secret is HMAC-SHA256(drbg_seed, "stub-slwe"). This
gives the combiner a real, distinct, high-entropy second KEM input even
when the lattice code is not yet exercised.
"""

from __future__ import annotations

import hmac
from typing import Tuple

from ..entropy.drbg import DRBG

STUB_LABEL = b"stub-slwe"
STUB_PK_LEN = 32
STUB_SK_LEN = 32
STUB_CT_LEN = 32
STUB_SS_LEN = 32


class SLWEWrapper:
    def __init__(self, mode: str = "stub", params: dict | None = None) -> None:
        if mode not in ("stub", "toy", "full"):
            raise ValueError(f"unknown SLWE mode: {mode}")
        if mode == "full":
            raise NotImplementedError(
                "SLWE mode 'full' pending scaling of sqt_slwe to mod-455 prime ≥ 2^32"
            )
        self.mode = mode
        self.params = params or {}
        if mode == "toy":
            # Defer the heavy import (Cayley-Dickson table) to first toy use.
            from . import slwe_toy as _toy
            self._toy = _toy
            self._toy_k = self.params.get("k", _toy.K_TOY)

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        if self.mode == "toy":
            return self._toy.keygen(drbg, self._toy_k)
        sk = drbg.generate(STUB_SK_LEN)
        pk = hmac.new(sk, STUB_LABEL + b":pk", "sha256").digest()
        return pk, sk

    def encaps(self, pk: bytes, drbg: DRBG) -> Tuple[bytes, bytes]:
        if self.mode == "toy":
            return self._toy.encaps(pk, drbg, self._toy_k)
        if len(pk) != STUB_PK_LEN:
            raise ValueError("invalid SLWE stub public key length")
        ephem = drbg.generate(STUB_CT_LEN)
        ct = bytes(a ^ b for a, b in zip(ephem, pk))
        ss = hmac.new(pk, STUB_LABEL + b":ss:" + ephem, "sha256").digest()
        return ct, ss

    def decaps(self, sk: bytes, ct: bytes) -> bytes:
        if self.mode == "toy":
            return self._toy.decaps(sk, ct, self._toy_k)
        if len(sk) != STUB_SK_LEN or len(ct) != STUB_CT_LEN:
            raise ValueError("invalid SLWE stub key/ct length")
        pk = hmac.new(sk, STUB_LABEL + b":pk", "sha256").digest()
        ephem = bytes(a ^ b for a, b in zip(ct, pk))
        return hmac.new(pk, STUB_LABEL + b":ss:" + ephem, "sha256").digest()
