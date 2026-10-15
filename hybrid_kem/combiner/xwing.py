"""X-Wing: ML-KEM-768 + X25519 hybrid KEM (vetted combiner).

Byte-exact implementation of the X-Wing construction,
``draft-connolly-cfrg-xwing-kem`` (this module tracks draft-11, 2026-09-23),
the general-purpose PQ/T hybrid KEM. X-Wing is the "vetted combiner" for a
ML-KEM-768 + X25519 pairing: rather than hashing the full transcript, it
relies on the binding properties of ML-KEM-768's FO transform and so omits the
ML-KEM ciphertext from the combiner. That specialisation is what the draft's
security analysis covers, so it is correct only for this exact pairing — for
other pairings (e.g. ML-KEM-1024) use the generic transcript-binding combiner
in ``kdf_combiner.py`` instead.

Combiner (draft §5.3):

    ss = SHA3-256( ss_M || ss_X || ct_X || pk_X || XWingLabel )

with ``XWingLabel`` the six bytes ``5c2e2f2f5e5c`` (ASCII ``\\.//^\\``).

ML-KEM-768 and X25519 come from ``pyca/cryptography`` (FIPS 203 and RFC 7748).

Determinism and known-answer tests. KeyGen (seed -> keypair) and Decapsulate
((sk, ct) -> ss) are deterministic and are verified byte-for-byte against the
draft's Appendix C vectors in ``tests/test_kat_xwing.py``. Encapsulate is
randomised: the ML-KEM FO transform draws a fresh message ``m`` internally and
pyca exposes no message-injection hook, so a derandomised ``EncapsulateDerand``
cannot be reproduced through pyca and is intentionally not offered here. The
KATs therefore pin conformance through the deterministic directions, which
exercise the combiner in full; ``encapsulate`` is covered by round-trip tests.
"""

from __future__ import annotations

import hashlib
import os
from typing import Callable, Optional, Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import mlkem, x25519

# draft §5.3 — the six-byte domain-separation label, ASCII "\./" + "/^\".
XWING_LABEL = bytes.fromhex("5c2e2f2f5e5c")

# Sizes (bytes). ML-KEM-768: pk 1184, ct 1088. X25519: 32.
SEED_LEN = 32
PK_LEN = 1216          # 1184 (ML-KEM) + 32 (X25519)
SK_LEN = 32            # X-Wing secret key is the 32-byte seed
CT_LEN = 1120          # 1088 (ML-KEM) + 32 (X25519)
SS_LEN = 32

_MLKEM_PK_LEN = 1184
_MLKEM_CT_LEN = 1088

RandomBytes = Callable[[int], bytes]


def _x25519_base(sk: bytes) -> bytes:
    """X25519 public key for scalar ``sk`` (clamping per RFC 7748 is internal)."""
    priv = x25519.X25519PrivateKey.from_private_bytes(sk)
    return priv.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )


def _x25519_dh(sk: bytes, peer_pk: bytes) -> bytes:
    priv = x25519.X25519PrivateKey.from_private_bytes(sk)
    peer = x25519.X25519PublicKey.from_public_bytes(peer_pk)
    return priv.exchange(peer)


def _expand_decapsulation_key(seed: bytes):
    """draft §5.2: seed -> (ml-kem key, sk_X, pk_M, pk_X) via SHAKE-256."""
    if len(seed) != SEED_LEN:
        raise ValueError(f"X-Wing seed must be {SEED_LEN} bytes, got {len(seed)}")
    expanded = hashlib.shake_256(seed).digest(96)
    kem_priv = mlkem.MLKEM768PrivateKey.from_seed_bytes(expanded[0:64])
    sk_x = expanded[64:96]
    pk_m = kem_priv.public_key().public_bytes_raw()
    pk_x = _x25519_base(sk_x)
    return kem_priv, sk_x, pk_m, pk_x


def combiner(ss_m: bytes, ss_x: bytes, ct_x: bytes, pk_x: bytes) -> bytes:
    """draft §5.3 combiner. Inputs are fixed-length, so plain concatenation is
    unambiguous (ss_m=32, ss_x=32, ct_x=32, pk_x=32)."""
    return hashlib.sha3_256(ss_m + ss_x + ct_x + pk_x + XWING_LABEL).digest()


def generate_keypair(rng: RandomBytes = os.urandom) -> Tuple[bytes, bytes]:
    """Return ``(sk, pk)``. ``sk`` is the 32-byte seed; ``pk`` is 1216 bytes."""
    seed = rng(SEED_LEN)
    return generate_keypair_derand(seed)


def generate_keypair_derand(seed: bytes) -> Tuple[bytes, bytes]:
    """Deterministic keygen from a 32-byte seed (draft §5.1 / §5.2)."""
    _, _, pk_m, pk_x = _expand_decapsulation_key(seed)
    return seed, pk_m + pk_x


def encapsulate(pk: bytes, rng: RandomBytes = os.urandom) -> Tuple[bytes, bytes]:
    """Randomised encapsulation (draft §5.4). Returns ``(ss, ct)``.

    ``rng`` supplies the X25519 ephemeral scalar; the ML-KEM message is drawn
    by pyca's FIPS 203 encapsulation internally.
    """
    if len(pk) != PK_LEN:
        raise ValueError(f"X-Wing pk must be {PK_LEN} bytes, got {len(pk)}")
    pk_m_bytes = pk[0:_MLKEM_PK_LEN]
    pk_x = pk[_MLKEM_PK_LEN:PK_LEN]

    ek_x = rng(32)
    ct_x = _x25519_base(ek_x)
    ss_x = _x25519_dh(ek_x, pk_x)

    pk_m = mlkem.MLKEM768PublicKey.from_public_bytes(pk_m_bytes)
    ss_m, ct_m = pk_m.encapsulate()  # pyca returns (shared_secret, ciphertext)

    ss = combiner(ss_m, ss_x, ct_x, pk_x)
    return ss, ct_m + ct_x


def decapsulate(ct: bytes, sk: bytes) -> bytes:
    """Deterministic decapsulation (draft §5.5). Returns the 32-byte secret."""
    if len(ct) != CT_LEN:
        raise ValueError(f"X-Wing ct must be {CT_LEN} bytes, got {len(ct)}")
    kem_priv, sk_x, _pk_m, pk_x = _expand_decapsulation_key(sk)
    ct_m = ct[0:_MLKEM_CT_LEN]
    ct_x = ct[_MLKEM_CT_LEN:CT_LEN]
    ss_m = kem_priv.decapsulate(ct_m)
    ss_x = _x25519_dh(sk_x, ct_x)
    return combiner(ss_m, ss_x, ct_x, pk_x)
