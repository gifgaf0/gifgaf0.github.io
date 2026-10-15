"""Classical EdDSA signature legs: Ed25519 and Ed448 (RFC 8032).

These are the *classical* halves of the composite signatures. EdDSA signing is
deterministic, so both keygen and signing are reproducible and the KATs cover
the full signing direction (``tests/test_kat_eddsa.py``). In the composite
scheme the raw ``sign``/``verify`` here operate over the composite message
representative M'; EdDSA's own context feature is not used (the composite does
its own domain separation).
"""

from __future__ import annotations

from typing import Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed448, ed25519

from ..entropy.drbg import DRBG

_RAW_PUB = dict(
    encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
)


class _EdDSALeg:
    _priv_cls = None
    _pub_cls = None
    name = "EdDSA"
    is_post_quantum = False
    sk_len = 0
    pk_len = 0
    sig_len = 0

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        sk = drbg.generate(self.sk_len)
        priv = self._priv_cls.from_private_bytes(sk)
        pk = priv.public_key().public_bytes(**_RAW_PUB)
        return pk, sk

    def public_from_private(self, sk: bytes) -> bytes:
        priv = self._priv_cls.from_private_bytes(sk)
        return priv.public_key().public_bytes(**_RAW_PUB)

    def sign(self, sk: bytes, message: bytes) -> bytes:
        return self._priv_cls.from_private_bytes(sk).sign(message)

    def verify(self, pk: bytes, signature: bytes, message: bytes) -> bool:
        pub = self._pub_cls.from_public_bytes(pk)
        try:
            pub.verify(signature, message)
            return True
        except InvalidSignature:
            return False


class Ed25519Leg(_EdDSALeg):
    _priv_cls = ed25519.Ed25519PrivateKey
    _pub_cls = ed25519.Ed25519PublicKey
    name = "Ed25519"
    sk_len = 32
    pk_len = 32
    sig_len = 64


class Ed448Leg(_EdDSALeg):
    _priv_cls = ed448.Ed448PrivateKey
    _pub_cls = ed448.Ed448PublicKey
    name = "Ed448"
    sk_len = 57
    pk_len = 57
    sig_len = 114
