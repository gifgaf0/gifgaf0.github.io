"""ML-KEM (FIPS 203) wrapper, backed by pyca/cryptography.

``pyca/cryptography`` (>= 46, built on OpenSSL/AWS-LC) provides ML-KEM-768 and
ML-KEM-1024 validated against the NIST ACVP vectors. This wrapper is a thin,
entropy-driven facade over it:

- ``keygen(drbg)`` is deterministic: it draws the 64-byte ``(d || z)`` seed from
  the supplied SP 800-90A DRBG and calls ``from_seed_bytes``. The secret key is
  returned in its 64-byte seed form (FIPS 203 allows storing the seed and
  re-expanding), so the same DRBG state reproduces the same keypair — which is
  what the cross-checks and KATs rely on.
- ``encaps`` is randomised by FIPS 203's FO transform; pyca draws the message
  internally and exposes no injection hook, so the ``drbg`` argument is accepted
  for API symmetry but not consumed here. KATs pin the deterministic directions
  (keygen-from-seed and decaps); see ``tests/test_kat_mlkem.py``.

An optional ``liboqs`` backend is used only for a cross-implementation check
(``cross_check``); it is never the default.
"""

from __future__ import annotations

from typing import Tuple

from cryptography.hazmat.primitives.asymmetric import mlkem

from ..entropy.drbg import DRBG

_LEVELS = {
    768: (mlkem.MLKEM768PrivateKey, 1184, 1088),
    1024: (mlkem.MLKEM1024PrivateKey, 1568, 1568),
}

# FIPS 203 keygen seed is d || z, 64 bytes, at every security level.
SEED_LEN = 64


class MLKEMWrapper:
    """ML-KEM-768 / ML-KEM-1024 facade over pyca/cryptography (FIPS 203)."""

    def __init__(self, level: int = 1024) -> None:
        if level not in _LEVELS:
            raise ValueError(f"ML-KEM level must be 768 or 1024, got {level}")
        self.level = level
        self._cls, self.pk_len, self.ct_len = _LEVELS[level]
        self.ss_len = 32

    @property
    def is_post_quantum(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return f"ML-KEM-{self.level}"

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        """Deterministic keygen from the DRBG. Returns ``(pk, sk_seed)``."""
        seed = drbg.generate(SEED_LEN)
        priv = self._cls.from_seed_bytes(seed)
        pk = priv.public_key().public_bytes_raw()
        return pk, seed

    def encaps(self, pk: bytes, drbg: DRBG | None = None) -> Tuple[bytes, bytes]:
        """Randomised encapsulation. Returns ``(ct, ss)``."""
        if len(pk) != self.pk_len:
            raise ValueError(
                f"{self.name} pk must be {self.pk_len} bytes, got {len(pk)}"
            )
        pub_cls = (
            mlkem.MLKEM768PublicKey if self.level == 768 else mlkem.MLKEM1024PublicKey
        )
        pub = pub_cls.from_public_bytes(pk)
        ss, ct = pub.encapsulate()  # pyca returns (shared_secret, ciphertext)
        return ct, ss

    def decaps(self, sk_seed: bytes, ct: bytes) -> bytes:
        if len(sk_seed) != SEED_LEN:
            raise ValueError(
                f"{self.name} sk seed must be {SEED_LEN} bytes, got {len(sk_seed)}"
            )
        if len(ct) != self.ct_len:
            raise ValueError(
                f"{self.name} ct must be {self.ct_len} bytes, got {len(ct)}"
            )
        priv = self._cls.from_seed_bytes(sk_seed)
        return priv.decapsulate(ct)

    # ------------------------------------------------------------------
    # Optional cross-implementation check against liboqs, when installed.
    # ------------------------------------------------------------------

    @staticmethod
    def _have_liboqs() -> bool:
        try:
            import oqs  # type: ignore[import-not-found]  # noqa: F401
            return True
        except Exception:
            return False

    def cross_check(self) -> bool:
        """Round-trip a keypair through pyca and liboqs if both are present.

        Returns True when they agree (or when liboqs is absent, nothing to
        compare). This checks pyca decaps against a liboqs-produced ciphertext.
        """
        if not self._have_liboqs():
            return True
        import oqs  # type: ignore[import-not-found]
        alg = f"ML-KEM-{self.level}"
        # Generate with pyca, encapsulate with liboqs to pyca's pk, decaps pyca.
        d = DRBG.seeded_from_os()
        pk, sk = self.keygen(d)
        with oqs.KeyEncapsulation(alg) as kem:
            ct, ss_oqs = kem.encap_secret(pk)
        return self.decaps(sk, ct) == ss_oqs
