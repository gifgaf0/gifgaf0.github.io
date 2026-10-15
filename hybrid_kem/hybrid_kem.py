"""Standards-only hybrid PQC KEM: ML-KEM (FIPS 203) + X25519 (RFC 7748).

Two profiles, both PQ/traditional hybrids whose shared secret stays secure as
long as *either* leg does:

- ``"xwing"`` — exactly X-Wing (``draft-connolly-cfrg-xwing-kem``): ML-KEM-768 +
  X25519 with X-Wing's SHA3-256 combiner. NIST Category 3. Byte-for-byte
  conformant to the draft's test vectors (``tests/test_kat_xwing.py``). Prefer
  this profile: it is the vetted, interoperable construction.

- ``"mlkem1024+x25519"`` — ML-KEM-1024 + X25519 with the generic
  transcript-binding KEM combiner of Bindel-Brendel-Fischlin-Goncalves-Stebila
  2019 (``combiner/kdf_combiner.py``). NIST Category 5. X-Wing specifies no
  1024 variant, so a generic combiner that hashes the whole transcript (both
  ciphertexts and both public keys) is used instead.

All randomness is drawn from an SP 800-90A DRBG. ``default_drbg()`` builds one
from the health-tested local entropy source; callers may pass their own.

Wire format for the ``mlkem1024+x25519`` profile (the ``xwing`` profile uses
X-Wing's native fixed-size encodings):

    pk = len(pk_M)||pk_M || len(pk_X)||pk_X
    sk = len(sk_M)||sk_M || len(sk_X)||sk_X || len(pk_M)||pk_M || len(pk_X)||pk_X
    ct = len(ct_M)||ct_M || len(ct_X)||ct_X

(The secret key embeds both public keys because decapsulation must feed them to
the transcript-binding combiner.)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Tuple

from .combiner import xwing
from .combiner.kdf_combiner import combine
from .entropy.drbg import DRBG
from .entropy.health_tests import HealthTests
from .entropy.qrng_source import QRNGSource
from .kem_classical.x25519_kem import X25519KEM
from .kem_standard.mlkem_wrapper import MLKEMWrapper

PROFILES = ("xwing", "mlkem1024+x25519")


def default_drbg(personalization: bytes = b"hybrid-kem") -> DRBG:
    """An SP 800-90A HMAC-DRBG seeded from the health-tested local source.

    The local :class:`QRNGSource` draws from the OS CSPRNG and runs SP 800-90B
    continuous health tests (RCT + APT) over the raw bytes before they are used
    as the DRBG's entropy input. Replace the source's provider for a validated
    hardware noise source in production.
    """
    src = QRNGSource(provider="local", health_test=HealthTests())
    d = DRBG()
    d.instantiate(
        entropy_input=src.get_bytes(32),
        nonce=src.get_bytes(16),
        personalization=personalization,
    )
    return d


def _pack(*chunks: bytes) -> bytes:
    return b"".join(len(c).to_bytes(4, "big") + c for c in chunks)


def _unpack(buf: bytes, n: int) -> list[bytes]:
    out: list[bytes] = []
    off = 0
    for _ in range(n):
        if off + 4 > len(buf):
            raise ValueError("truncated hybrid blob")
        length = int.from_bytes(buf[off:off + 4], "big")
        off += 4
        if off + length > len(buf):
            raise ValueError("truncated hybrid blob")
        out.append(buf[off:off + length])
        off += length
    if off != len(buf):
        raise ValueError("trailing bytes in hybrid blob")
    return out


@dataclass
class HybridKEM:
    """Standards-only hybrid KEM (ML-KEM + X25519)."""

    profile: str = "xwing"

    def __post_init__(self) -> None:
        if self.profile not in PROFILES:
            raise ValueError(
                f"unknown profile {self.profile!r}; choose one of {PROFILES}"
            )
        if self.profile == "mlkem1024+x25519":
            self._mlkem = MLKEMWrapper(level=1024)
            self._x = X25519KEM()

    @property
    def is_post_quantum(self) -> bool:
        return True

    @property
    def nist_category(self) -> int:
        return 3 if self.profile == "xwing" else 5

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------

    def keygen(self, drbg: DRBG | None = None) -> Tuple[bytes, bytes]:
        drbg = drbg or default_drbg()
        if self.profile == "xwing":
            sk, pk = xwing.generate_keypair(rng=drbg.generate)  # X-Wing order is (sk, pk)
            return pk, sk
        pk_m, sk_m = self._mlkem.keygen(drbg)
        pk_x, sk_x = self._x.keygen(drbg)
        return _pack(pk_m, pk_x), _pack(sk_m, sk_x, pk_m, pk_x)

    def encaps(self, pk: bytes, drbg: DRBG | None = None) -> Tuple[bytes, bytes]:
        drbg = drbg or default_drbg()
        if self.profile == "xwing":
            ss, ct = xwing.encapsulate(pk, rng=drbg.generate)  # X-Wing order is (ss, ct)
            return ct, ss
        pk_m, pk_x = _unpack(pk, 2)
        ct_m, ss_m = self._mlkem.encaps(pk_m, drbg)
        ct_x, ss_x = self._x.encaps(pk_x, drbg)
        ss = combine(ss_m, ss_x, ct_m, ct_x, pk_m, pk_x)
        return _pack(ct_m, ct_x), ss

    def decaps(self, sk: bytes, ct: bytes) -> bytes:
        if self.profile == "xwing":
            return xwing.decapsulate(ct, sk)
        sk_m, sk_x, pk_m, pk_x = _unpack(sk, 4)
        ct_m, ct_x = _unpack(ct, 2)
        ss_m = self._mlkem.decaps(sk_m, ct_m)
        ss_x = self._x.decaps(sk_x, ct_x)
        return combine(ss_m, ss_x, ct_m, ct_x, pk_m, pk_x)
