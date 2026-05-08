"""Top-level Hybrid PQC KEM: ML-KEM-1024 || Module-SLWE, BBF-G-S combiner.

The wire format concatenates the standard-KEM output and the SLWE output
with 4-byte big-endian length prefixes so that callers do not need to
hard-code per-backend sizes:

    hybrid_pk = len(pk_A)||pk_A || len(pk_B)||pk_B
    hybrid_sk = len(sk_A)||sk_A || len(sk_B)||sk_B || len(pk_A)||pk_A || len(pk_B)||pk_B
    hybrid_ct = len(ct_A)||ct_A || len(ct_B)||ct_B

The hybrid secret key embeds the public keys because the combiner mixes
both pk values into ``info``, and decaps must reproduce the same input.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .combiner.kdf_combiner import combine
from .entropy.drbg import DRBG
from .kem_slwe.slwe_wrapper import SLWEWrapper
from .kem_standard.mlkem_wrapper import MLKEMWrapper


def _pack(*chunks: bytes) -> bytes:
    return b"".join(len(c).to_bytes(4, "big") + c for c in chunks)


def _unpack(buf: bytes, n: int) -> list[bytes]:
    out: list[bytes] = []
    offset = 0
    for _ in range(n):
        if offset + 4 > len(buf):
            raise ValueError("truncated hybrid blob")
        length = int.from_bytes(buf[offset : offset + 4], "big")
        offset += 4
        if offset + length > len(buf):
            raise ValueError("truncated hybrid blob")
        out.append(buf[offset : offset + length])
        offset += length
    if offset != len(buf):
        raise ValueError("trailing bytes in hybrid blob")
    return out


@dataclass
class HybridKEM:
    """Hybrid KEM combining a standard PQC KEM with the Module-SLWE KEM."""

    standard_backend: str = "auto"
    slwe_mode: str = "stub"
    drbg_algorithm: str = "hmac-sha256"

    def __post_init__(self) -> None:
        self.standard = MLKEMWrapper(backend=self.standard_backend)
        self.slwe = SLWEWrapper(mode=self.slwe_mode)

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        pk_a, sk_a = self.standard.keygen(drbg)
        pk_b, sk_b = self.slwe.keygen(drbg)
        return _pack(pk_a, pk_b), _pack(sk_a, sk_b, pk_a, pk_b)

    def encaps(self, hybrid_pk: bytes, drbg: DRBG) -> Tuple[bytes, bytes]:
        pk_a, pk_b = _unpack(hybrid_pk, 2)
        ct_a, ss_a = self.standard.encaps(pk_a, drbg)
        ct_b, ss_b = self.slwe.encaps(pk_b, drbg)
        ss = combine(ss_a, ss_b, ct_a, ct_b, pk_a, pk_b)
        return _pack(ct_a, ct_b), ss

    def decaps(self, hybrid_sk: bytes, hybrid_ct: bytes) -> bytes:
        sk_a, sk_b, pk_a, pk_b = _unpack(hybrid_sk, 4)
        ct_a, ct_b = _unpack(hybrid_ct, 2)
        ss_a = self.standard.decaps(sk_a, ct_a)
        ss_b = self.slwe.decaps(sk_b, ct_b)
        return combine(ss_a, ss_b, ct_a, ct_b, pk_a, pk_b)

    @property
    def is_post_quantum(self) -> bool:
        return self.standard.is_post_quantum
