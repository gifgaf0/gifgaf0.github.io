"""ML-DSA (FIPS 204) signature wrapper, backed by pyca/cryptography.

Mirrors ``kem_standard/mlkem_wrapper.py``: a thin, entropy-driven facade over
pyca's ML-DSA-44/65/87 (validated against the NIST ACVP vectors).

- ``keygen(drbg)`` is deterministic: it draws the 32-byte ML-DSA keygen seed
  ``xi`` from the SP 800-90A DRBG and calls ``from_seed_bytes``. The secret key
  is the 32-byte seed (FIPS 204 allows storing the seed and re-expanding), so
  the same DRBG state reproduces the same keypair.
- ``sign`` is, by default, FIPS 204's *hedged* signing (randomised); pyca draws
  the per-signature randomness internally. Verification is deterministic. KATs
  therefore pin keygen-from-seed and verification of the published signatures;
  signing is covered by round-trip tests. ``context`` is the FIPS 204 context
  string (<= 255 bytes).
"""

from __future__ import annotations

from typing import Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa

from ..entropy.drbg import DRBG

# level -> (private-key class, public-key class, pk bytes, signature bytes)
_LEVELS = {
    44: (mldsa.MLDSA44PrivateKey, mldsa.MLDSA44PublicKey, 1312, 2420),
    65: (mldsa.MLDSA65PrivateKey, mldsa.MLDSA65PublicKey, 1952, 3309),
    87: (mldsa.MLDSA87PrivateKey, mldsa.MLDSA87PublicKey, 2592, 4627),
}

# FIPS 204 keygen seed xi is 32 bytes at every level.
SEED_LEN = 32


class MLDSAWrapper:
    """ML-DSA-44 / 65 / 87 facade over pyca/cryptography (FIPS 204)."""

    def __init__(self, level: int = 65) -> None:
        if level not in _LEVELS:
            raise ValueError(f"ML-DSA level must be 44, 65 or 87, got {level}")
        self.level = level
        self._priv_cls, self._pub_cls, self.pk_len, self.sig_len = _LEVELS[level]

    @property
    def is_post_quantum(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return f"ML-DSA-{self.level}"

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        """Deterministic keygen from the DRBG. Returns ``(pk, sk_seed)``."""
        seed = drbg.generate(SEED_LEN)
        priv = self._priv_cls.from_seed_bytes(seed)
        return priv.public_key().public_bytes_raw(), seed

    def sign(self, sk_seed: bytes, message: bytes, context: bytes = b"") -> bytes:
        if len(sk_seed) != SEED_LEN:
            raise ValueError(f"{self.name} sk seed must be {SEED_LEN} bytes")
        priv = self._priv_cls.from_seed_bytes(sk_seed)
        return priv.sign(message, context)

    def verify(
        self, pk: bytes, signature: bytes, message: bytes, context: bytes = b""
    ) -> bool:
        if len(pk) != self.pk_len:
            raise ValueError(f"{self.name} pk must be {self.pk_len} bytes")
        pub = self._pub_cls.from_public_bytes(pk)
        try:
            pub.verify(signature, message, context)
            return True
        except InvalidSignature:
            return False
