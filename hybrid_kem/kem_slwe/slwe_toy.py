"""Toy-mode adapter for ``SLWEWrapper`` over the supplied SQT-SLWE source.

The reference implementation lives at ``tools/sqt_slwe.py`` (with
helpers in ``tools/sedenion_Fp.py`` and ``tools/sedenion_audit.py``).
It uses a module-level prime ``p = 911`` and rank ``k = 4`` to match the
toy parameters from ``SPEC.md`` §2.6.

This adapter exposes the source's ``keygen / encaps / decaps`` through
the byte-oriented :class:`hybrid_kem.kem_slwe.slwe_wrapper.SLWEWrapper`
API. The supplied source uses Python's global ``random`` module for
randomness; the adapter reseeds it from the caller's DRBG before each
call so determinism flows through the entropy layer.

Known correctness gap (raw finding, see tools/BRIEF_02_SUMMARY.md):
the supplied source measures its own DFR at ~0.48 at (p=911, k=4) and
flags the verdict as "noise too large for this p, FAIL". The wrapper
does not paper over this — the toy roundtrip test below records the
empirical DFR rather than asserting < 0.01. The brief's DFR < 0.01
target is not met by the source as shipped, and unblocking it requires
either tightening the CBD error distribution in ``rand_small()`` or
scaling p, both of which change the scheme.
"""

from __future__ import annotations

import hashlib
import random as _python_random
import sys
from pathlib import Path
from typing import Tuple

from ..entropy.drbg import DRBG

# Make tools/ importable without polluting the global path permanently.
_TOOLS = Path(__file__).resolve().parents[2] / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

# These imports load the user-supplied SLWE source. They have side effects
# (Cayley-Dickson table build) but are idempotent.
import sqt_slwe as _slwe       # noqa: E402
from sedenion_Fp import DIM as _DIM  # noqa: E402

P_TOY = 911
K_TOY = 4

# Each sedenion coefficient lies in [0, p) with p = 911 < 2^10. We pack
# coefficients as little-endian 2-byte words for clarity.
_COEFF_BYTES = 2
_SEDENION_BYTES = _DIM * _COEFF_BYTES


def _sed_to_bytes(v) -> bytes:
    return b"".join(int(c).to_bytes(_COEFF_BYTES, "big") for c in v)


def _bytes_to_sed(buf: bytes):
    if len(buf) != _SEDENION_BYTES:
        raise ValueError("invalid sedenion encoding length")
    return [
        int.from_bytes(buf[i : i + _COEFF_BYTES], "big")
        for i in range(0, _SEDENION_BYTES, _COEFF_BYTES)
    ]


def _serialize_sk(s_list) -> bytes:
    return b"".join(_sed_to_bytes(s) for s in s_list)


def _deserialize_sk(buf: bytes, k: int):
    if len(buf) != k * _SEDENION_BYTES:
        raise ValueError("invalid SLWE toy sk length")
    return [
        _bytes_to_sed(buf[i : i + _SEDENION_BYTES])
        for i in range(0, len(buf), _SEDENION_BYTES)
    ]


def _serialize_pk(A, b) -> bytes:
    parts = []
    for row in A:
        for el in row:
            parts.append(_sed_to_bytes(el))
    for el in b:
        parts.append(_sed_to_bytes(el))
    return b"".join(parts)


def _deserialize_pk(buf: bytes, k: int):
    matrix_bytes = k * k * _SEDENION_BYTES
    vec_bytes = k * _SEDENION_BYTES
    if len(buf) != matrix_bytes + vec_bytes:
        raise ValueError("invalid SLWE toy pk length")
    A = []
    off = 0
    for _ in range(k):
        row = []
        for _ in range(k):
            row.append(_bytes_to_sed(buf[off : off + _SEDENION_BYTES]))
            off += _SEDENION_BYTES
        A.append(row)
    b_vec = []
    for _ in range(k):
        b_vec.append(_bytes_to_sed(buf[off : off + _SEDENION_BYTES]))
        off += _SEDENION_BYTES
    return A, b_vec


def _serialize_ct(c1, c2: int, k: int) -> bytes:
    return b"".join(_sed_to_bytes(el) for el in c1) + int(c2).to_bytes(2, "big")


def _deserialize_ct(buf: bytes, k: int):
    expected = k * _SEDENION_BYTES + 2
    if len(buf) != expected:
        raise ValueError("invalid SLWE toy ct length")
    c1 = [
        _bytes_to_sed(buf[i : i + _SEDENION_BYTES])
        for i in range(0, k * _SEDENION_BYTES, _SEDENION_BYTES)
    ]
    c2 = int.from_bytes(buf[k * _SEDENION_BYTES :], "big")
    return c1, c2


def _seed_python_random(drbg: DRBG | None) -> None:
    if drbg is None:
        _python_random.seed()
        return
    _python_random.seed(int.from_bytes(drbg.generate(16), "big"))


def keygen(drbg: DRBG, k: int = K_TOY) -> Tuple[bytes, bytes]:
    # Brief 02 §1 fixes the canonical toy at k=4. Brief 02 §3 (DFR scaling)
    # asks for the same scheme at k ∈ {4, 8, 12, 16} with p ≈ 2^24 for the
    # larger sizes. The supplied source has p hardcoded at 911 (SPEC.md
    # §2.6); we let k vary so the scaling-in-k axis can be measured, and
    # report the q axis as blocked in tools/QUESTIONS.md.
    if k < 1:
        raise ValueError(f"k must be >= 1; got {k}")
    _seed_python_random(drbg)
    kp = _slwe.keygen(k)
    return _serialize_pk(kp["A"], kp["b"]), _serialize_sk(kp["sk"])


def encaps(pk_bytes: bytes, drbg: DRBG, k: int = K_TOY) -> Tuple[bytes, bytes]:
    A, b = _deserialize_pk(pk_bytes, k)
    _seed_python_random(drbg)
    c1, c2, m_bit = _slwe.encaps(A, b, k)
    ct = _serialize_ct(c1, c2, k)
    ss = hashlib.sha256(bytes([m_bit & 1]) + ct).digest()
    return ct, ss


def decaps(sk_bytes: bytes, ct_bytes: bytes, k: int = K_TOY) -> bytes:
    sk = _deserialize_sk(sk_bytes, k)
    c1, c2 = _deserialize_ct(ct_bytes, k)
    m_dec, _v = _slwe.decaps(sk, c1, c2, k)
    return hashlib.sha256(bytes([m_dec & 1]) + ct_bytes).digest()
