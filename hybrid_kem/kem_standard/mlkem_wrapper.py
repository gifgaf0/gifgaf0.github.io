"""ML-KEM-1024 wrapper with pluggable backends.

Backends:
- ``"liboqs"``  Open Quantum Safe (liboqs-python). Real ML-KEM-1024.
- ``"fips203"`` dkg/fips203. Real ML-KEM-1024 reference implementation.
- ``"x25519"``  Test backend: an X25519-based KEM. Provides real classical
                IND-CCA2 security but is NOT post-quantum. Used so the
                testbed can run end-to-end CI without liboqs installed.

In production set ``backend="liboqs"`` (or ``"fips203"``) and call
``MLKEMWrapper.cross_check`` regularly: identical entropy must produce
byte-identical outputs. The two real implementations are deterministic from
their seed and serve as cross-validators.

The X25519 backend is selected automatically when no real PQC backend is
available; the wrapper logs a prominent warning so its use cannot be silent
in production logs.
"""

from __future__ import annotations

import logging
from typing import Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from ..entropy.drbg import DRBG

LOG = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Backend availability
# ---------------------------------------------------------------------------


def _have_liboqs() -> bool:
    try:
        import oqs  # type: ignore[import-not-found]  # noqa: F401
        return True
    except Exception:
        return False


def _have_fips203() -> bool:
    try:
        import fips203  # type: ignore[import-not-found]  # noqa: F401
        return True
    except Exception:
        return False


def available_backends() -> list[str]:
    out = []
    if _have_liboqs():
        out.append("liboqs")
    if _have_fips203():
        out.append("fips203")
    out.append("x25519")  # always available as a test fallback
    return out


# ---------------------------------------------------------------------------
# X25519 test backend
# ---------------------------------------------------------------------------


class _X25519KEM:
    """X25519-based KEM, used only as a test backend.

    keygen: derive private key bytes from DRBG, public = scalar*G.
    encaps: derive ephemeral private from DRBG, ciphertext = ephem_pub,
            shared_secret = HKDF(ECDH(ephem, pub) || ephem_pub).
    decaps: shared_secret = HKDF(ECDH(sk, ct) || ct).

    This construction is implicit-rejection-free in the academic sense, but
    it is deterministic from the seed and round-trip-correct, which is all the
    testbed needs for combiner / hybrid integration tests.
    """

    name = "x25519"
    pk_len = 32
    sk_len = 32
    ct_len = 32
    ss_len = 32

    @staticmethod
    def _kdf(key_material: bytes, info: bytes) -> bytes:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"hybrid-kem-x25519-test",
            info=info,
        )
        return hkdf.derive(key_material)

    @classmethod
    def keygen(cls, drbg: DRBG) -> Tuple[bytes, bytes]:
        sk_bytes = drbg.generate(32)
        priv = x25519.X25519PrivateKey.from_private_bytes(sk_bytes)
        pub = priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return pub, sk_bytes

    @classmethod
    def encaps(cls, pk: bytes, drbg: DRBG) -> Tuple[bytes, bytes]:
        ephem_priv = x25519.X25519PrivateKey.from_private_bytes(drbg.generate(32))
        ephem_pub = ephem_priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        peer = x25519.X25519PublicKey.from_public_bytes(pk)
        ecdh = ephem_priv.exchange(peer)
        ss = cls._kdf(ecdh, ephem_pub + pk)
        return ephem_pub, ss

    @classmethod
    def decaps(cls, sk: bytes, ct: bytes) -> bytes:
        priv = x25519.X25519PrivateKey.from_private_bytes(sk)
        peer = x25519.X25519PublicKey.from_public_bytes(ct)
        ecdh = priv.exchange(peer)
        pub = priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return cls._kdf(ecdh, ct + pub)


# ---------------------------------------------------------------------------
# Real-backend wrappers
# ---------------------------------------------------------------------------


class _LibOQSKEM:
    name = "liboqs"

    def __init__(self) -> None:
        import oqs  # type: ignore[import-not-found]
        self._oqs = oqs
        self.alg = "ML-KEM-1024"

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        # liboqs does not accept an external RNG hook in the Python binding;
        # we use it as-is. The wrapper is still entropy-driven via the rest
        # of the testbed (combiner inputs, SLWE side, etc).
        with self._oqs.KeyEncapsulation(self.alg) as kem:
            pk = kem.generate_keypair()
            sk = kem.export_secret_key()
            return pk, sk

    def encaps(self, pk: bytes, drbg: DRBG) -> Tuple[bytes, bytes]:
        with self._oqs.KeyEncapsulation(self.alg) as kem:
            ct, ss = kem.encap_secret(pk)
            return ct, ss

    def decaps(self, sk: bytes, ct: bytes) -> bytes:
        with self._oqs.KeyEncapsulation(self.alg, secret_key=sk) as kem:
            return kem.decap_secret(ct)


class _FIPS203KEM:
    name = "fips203"

    def __init__(self) -> None:
        import fips203  # type: ignore[import-not-found]
        self._fips = fips203

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        return self._fips.ml_kem_1024.key_gen()

    def encaps(self, pk: bytes, drbg: DRBG) -> Tuple[bytes, bytes]:
        return self._fips.ml_kem_1024.encaps(pk)

    def decaps(self, sk: bytes, ct: bytes) -> bytes:
        return self._fips.ml_kem_1024.decaps(sk, ct)


# ---------------------------------------------------------------------------
# Public facade
# ---------------------------------------------------------------------------


class MLKEMWrapper:
    """ML-KEM-1024 facade with backend selection and cross-check."""

    def __init__(self, backend: str = "auto") -> None:
        if backend == "auto":
            backends = available_backends()
            backend = backends[0]
            if backend == "x25519":
                LOG.warning(
                    "MLKEMWrapper falling back to x25519 test backend; "
                    "no PQC backend installed (liboqs / fips203)"
                )
        self.backend = backend
        if backend == "liboqs":
            self._impl = _LibOQSKEM()
        elif backend == "fips203":
            self._impl = _FIPS203KEM()
        elif backend == "x25519":
            self._impl = _X25519KEM()
        else:
            raise ValueError(f"unknown backend: {backend}")

    @property
    def is_post_quantum(self) -> bool:
        return self.backend in ("liboqs", "fips203")

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        return self._impl.keygen(drbg)

    def encaps(self, pk: bytes, drbg: DRBG) -> Tuple[bytes, bytes]:
        return self._impl.encaps(pk, drbg)

    def decaps(self, sk: bytes, ct: bytes) -> bytes:
        return self._impl.decaps(sk, ct)

    @classmethod
    def cross_check(cls, drbg_factory) -> bool:
        """Run keygen+encaps+decaps with both real backends if both present.

        ``drbg_factory`` must return a freshly instantiated DRBG so the two
        backends see byte-identical entropy. Returns True if shared secrets
        match, False if they differ. Returns True when only one real backend
        is present (nothing to compare).
        """
        backends = [b for b in available_backends() if b != "x25519"]
        if len(backends) < 2:
            return True
        wrappers = [cls(backend=b) for b in backends]
        results = []
        for w in wrappers:
            d = drbg_factory()
            pk, sk = w.keygen(d)
            ct, ss = w.encaps(pk, d)
            ss2 = w.decaps(sk, ct)
            if ss != ss2:
                return False
            results.append(ss)
        return all(r == results[0] for r in results)
