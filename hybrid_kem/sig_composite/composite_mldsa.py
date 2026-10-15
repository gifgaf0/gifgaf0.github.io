"""Composite ML-DSA + EdDSA signatures.

Implements ``draft-ietf-lamps-pq-composite-sigs`` (this module tracks draft-19,
2026-04-21, which is in the RFC Editor queue). A composite signature is valid
only if *both* component signatures verify, so it stays unforgeable as long as
either ML-DSA or the classical EdDSA does -- the signature analogue of the
hybrid KEM.

Message representative (draft section 4.2):

    M' = Prefix || Label || len(ctx) || ctx || PH(M)

with ``Prefix`` the 32 bytes of ASCII ``CompositeAlgorithmSignatures2025``,
``Label`` the per-algorithm domain separator, ``len(ctx)`` a single byte
(ctx <= 255 bytes), and ``PH`` the pre-hash. The ML-DSA component signs M' with
its FIPS 204 context set to ``Label``; the EdDSA component signs M' directly.
Keys, secret keys and signatures are plain concatenations of the components
(section 4.1): ``pk = mldsaPK || tradPK``, ``sk = mldsaSeed || tradSK``,
``sig = mldsaSig || tradSig``.

Two profiles are provided; both are verified byte-for-byte against the draft's
Appendix E vectors in ``tests/test_kat_composite_sig.py``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Callable, Tuple

from ..entropy.drbg import DRBG
from ..sig_classical.eddsa import Ed448Leg, Ed25519Leg
from ..sig_standard.mldsa_wrapper import MLDSAWrapper

# draft section 4.2 -- ASCII "CompositeAlgorithmSignatures2025".
PREFIX = bytes.fromhex(
    "436F6D706F73697465416C676F726974686D5369676E61747572657332303235"
)


@dataclass(frozen=True)
class _Profile:
    oid_name: str
    label: bytes
    mldsa_level: int
    trad_cls: type
    prehash: Callable[[bytes], bytes]


PROFILES = {
    "id-MLDSA65-Ed25519-SHA512": _Profile(
        oid_name="id-MLDSA65-Ed25519-SHA512",
        label=b"COMPSIG-MLDSA65-Ed25519-SHA512",
        mldsa_level=65,
        trad_cls=Ed25519Leg,
        prehash=lambda m: hashlib.sha512(m).digest(),
    ),
    "id-MLDSA87-Ed448-SHAKE256": _Profile(
        oid_name="id-MLDSA87-Ed448-SHAKE256",
        label=b"COMPSIG-MLDSA87-Ed448-SHAKE256",
        mldsa_level=87,
        trad_cls=Ed448Leg,
        prehash=lambda m: hashlib.shake_256(m).digest(64),
    ),
}


class CompositeMLDSA:
    """Composite ML-DSA + EdDSA signer/verifier for one profile."""

    def __init__(self, profile: str = "id-MLDSA65-Ed25519-SHA512") -> None:
        if profile not in PROFILES:
            raise ValueError(
                f"unknown profile {profile!r}; choose one of {sorted(PROFILES)}"
            )
        self.profile = profile
        p = PROFILES[profile]
        self._p = p
        self._mldsa = MLDSAWrapper(level=p.mldsa_level)
        self._trad = p.trad_cls()
        self.pk_len = self._mldsa.pk_len + self._trad.pk_len
        self.sk_len = 32 + self._trad.sk_len  # 32-byte ML-DSA seed + trad sk
        self.sig_len = self._mldsa.sig_len + self._trad.sig_len

    # ------------------------------------------------------------------

    def _mprime(self, message: bytes, context: bytes) -> bytes:
        if len(context) > 255:
            raise ValueError("context must be at most 255 bytes")
        return (
            PREFIX
            + self._p.label
            + bytes([len(context)])
            + context
            + self._p.prehash(message)
        )

    def keygen(self, drbg: DRBG | None = None) -> Tuple[bytes, bytes]:
        from ..hybrid_kem import default_drbg

        drbg = drbg or default_drbg(b"composite-sig")
        pk_m, seed_m = self._mldsa.keygen(drbg)
        pk_t, sk_t = self._trad.keygen(drbg)
        return pk_m + pk_t, seed_m + sk_t

    def sign(self, sk: bytes, message: bytes, context: bytes = b"") -> bytes:
        if len(sk) != self.sk_len:
            raise ValueError(f"{self.profile} sk must be {self.sk_len} bytes")
        seed_m, sk_t = sk[:32], sk[32:]
        m_prime = self._mprime(message, context)
        mldsa_sig = self._mldsa.sign(seed_m, m_prime, context=self._p.label)
        trad_sig = self._trad.sign(sk_t, m_prime)
        return mldsa_sig + trad_sig

    def verify(
        self, pk: bytes, signature: bytes, message: bytes, context: bytes = b""
    ) -> bool:
        if len(pk) != self.pk_len or len(signature) != self.sig_len:
            return False
        pk_m, pk_t = pk[: self._mldsa.pk_len], pk[self._mldsa.pk_len:]
        sig_m, sig_t = (
            signature[: self._mldsa.sig_len],
            signature[self._mldsa.sig_len:],
        )
        m_prime = self._mprime(message, context)
        ok_m = self._mldsa.verify(pk_m, sig_m, m_prime, context=self._p.label)
        ok_t = self._trad.verify(pk_t, sig_t, m_prime)
        return ok_m and ok_t
