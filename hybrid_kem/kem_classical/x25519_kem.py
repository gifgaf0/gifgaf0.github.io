"""X25519 as a classical KEM leg (RFC 7748 / RFC 9180 DHKEM-style).

This is the *classical* half of the hybrid: a traditional elliptic-curve
Diffie-Hellman KEM over Curve25519. It provides no post-quantum security on its
own; its job in the hybrid is to keep the construction at least as strong as
X25519 should ML-KEM ever be broken, and vice versa.

Encapsulation is ephemeral-static DH:

    keygen:  sk <- 32 random bytes; pk = X25519(sk, 9)
    encaps:  e  <- 32 random bytes; ct = X25519(e, 9); ss = X25519(e, pk)
    decaps:  ss = X25519(sk, ct)

The raw DH output is the shared secret. In the hybrid it is never used alone:
it is one input to the combiner (``kdf_combiner`` for the ML-KEM-1024 profile,
or folded into X-Wing's SHA3-256 combiner for the ML-KEM-768 profile), which is
where domain separation and transcript binding happen. The bare DH value is
therefore returned as-is here rather than being KDF'd twice.
"""

from __future__ import annotations

import os
from typing import Callable, Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

from ..entropy.drbg import DRBG

PK_LEN = 32
SK_LEN = 32
CT_LEN = 32
SS_LEN = 32

RandomBytes = Callable[[int], bytes]


def _pub(sk: bytes) -> bytes:
    priv = x25519.X25519PrivateKey.from_private_bytes(sk)
    return priv.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )


class X25519KEM:
    """Ephemeral-static X25519 KEM leg."""

    name = "X25519"
    is_post_quantum = False
    pk_len = PK_LEN
    ct_len = CT_LEN
    ss_len = SS_LEN

    def keygen(self, drbg: DRBG) -> Tuple[bytes, bytes]:
        sk = drbg.generate(SK_LEN)
        return _pub(sk), sk

    def encaps(self, pk: bytes, drbg: DRBG) -> Tuple[bytes, bytes]:
        if len(pk) != PK_LEN:
            raise ValueError(f"X25519 pk must be {PK_LEN} bytes, got {len(pk)}")
        eph = drbg.generate(SK_LEN)
        ct = _pub(eph)
        priv = x25519.X25519PrivateKey.from_private_bytes(eph)
        ss = priv.exchange(x25519.X25519PublicKey.from_public_bytes(pk))
        return ct, ss

    def decaps(self, sk: bytes, ct: bytes) -> bytes:
        if len(ct) != CT_LEN:
            raise ValueError(f"X25519 ct must be {CT_LEN} bytes, got {len(ct)}")
        priv = x25519.X25519PrivateKey.from_private_bytes(sk)
        return priv.exchange(x25519.X25519PublicKey.from_public_bytes(ct))
