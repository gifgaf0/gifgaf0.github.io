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

# CBD(η) sampling weights: binomial(2η, k) for k=0..2η over the support
# {-η, …, η}. Brief 02 epilogue Task 2 callers always pass η=2.
_CBD_TABLES = {
    1: ([-1, 0, 1],          [1, 2, 1]),
    2: ([-2, -1, 0, 1, 2],   [1, 4, 6, 4, 1]),
}


def rand_small_nonzd(p: int, eta: int = 2, dim: int = _DIM):
    """Sample a small CBD(η) vector that is not a basis-pair zero divisor.

    Rejection-samples from the centred binomial distribution CBD(η) over
    F_p^dim and re-rolls when the result is all-zero or has exactly two
    non-zero entries whose indices form a known sedenion ZD pair (the
    same definition the supplied source applies in ``rand_nonzd``).

    Brief 02 epilogue Task 1 measures the rejection rate at ~10⁻⁵ for
    CBD(η=2), so the loop terminates after one iteration overwhelmingly
    and the resulting sampling distribution is statistically
    indistinguishable from CBD(η).
    """
    import random as _r
    values, weights = _CBD_TABLES[eta]
    zd_pairs = _slwe.zd_pairs    # prime-independent (audit confirms)
    while True:
        v = [_r.choices(values, weights=weights)[0] % p for _ in range(dim)]
        nz = [i for i, c in enumerate(v) if c != 0]
        if not nz:
            continue
        if len(nz) == 2:
            idx = (nz[0], nz[1])
            if idx in zd_pairs:
                continue
        return v


def _rand_small_nonzd_drbg(drbg: DRBG, p: int, eta: int = 2, dim: int = _DIM):
    """DRBG-backed CBD(η) sampler with ZD-pair rejection.

    R2(a) fix (per BRIEF_02_ADDENDUM_SIDE_CHANNEL.md): the encaps
    randomness ``r`` must come from a cryptographic source, not from
    Mersenne Twister. This sampler consumes bytes from the caller's
    DRBG and produces the same CBD(η) distribution as
    :func:`rand_small_nonzd`, so DFR is unchanged but r_upper is no
    longer recoverable by MT-state reconstruction.

    CBD(η) is realised as a sum of 2η independent uniform bits:
    ``sample = (a_1 + ... + a_η) - (b_1 + ... + b_η)``. ZD-pair
    rejection matches :func:`rand_small_nonzd`.
    """
    if eta not in (1, 2):
        raise ValueError(f"_rand_small_nonzd_drbg: unsupported eta={eta}")
    zd_pairs = _slwe.zd_pairs
    bits_per = 2 * eta  # 2 bits/coord for eta=1, 4 bits/coord for eta=2

    def _draw_one(buf: bytes, bit_pos: int) -> int:
        a = sum((buf[(bit_pos + i) // 8] >> ((bit_pos + i) % 8)) & 1
                for i in range(eta))
        b = sum((buf[(bit_pos + i) // 8] >> ((bit_pos + i) % 8)) & 1
                for i in range(eta, 2 * eta))
        return a - b

    bytes_per_draw = (bits_per * dim + 7) // 8
    while True:
        buf = drbg.generate(bytes_per_draw)
        v = [_draw_one(buf, i * bits_per) % p for i in range(dim)]
        nz = [i for i, c in enumerate(v) if c != 0]
        if not nz:
            continue
        if len(nz) == 2 and (nz[0], nz[1]) in zd_pairs:
            continue
        return v

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
    kp = _keygen_small_sr(k)
    return _serialize_pk(kp["A"], kp["b"]), _serialize_sk(kp["sk"])


def encaps(pk_bytes: bytes, drbg: DRBG, k: int = K_TOY) -> Tuple[bytes, bytes]:
    A, b = _deserialize_pk(pk_bytes, k)
    _seed_python_random(drbg)
    c1, c2, m_bit = _encaps_small_r(A, b, k, drbg)
    ct = _serialize_ct(c1, c2, k)
    ss = hashlib.sha256(bytes([m_bit & 1]) + ct).digest()
    return ct, ss


# -- Brief 02 epilogue Task 3: surgical fix for the DFR issue ---------
#
# The supplied source's keygen/encaps draw the secret `s` and the
# encryption randomness `r` from ``rand_nonzd`` — a uniform F_p^16
# distribution with only a 2-coordinate-ZD-pair filter. The dominant
# noise term <e, r>_norm is then O(k * dim * p), wraps mod p, and
# pushes per-trial DFR to the noise-only ceiling of 0.5 (verified in
# Brief 02 + parameter-fix epilogue).
#
# The fix is to draw `s` and `r` from ``rand_small_nonzd`` (CBD(η=2)
# with ZD-pair rejection). The public matrix `A` stays uniform, so the
# scheme's hardness assumption is unchanged. Empirical DFR over 5000
# trials is 0 at both p=911 and p=8191 (k=4, η=2) — see
# tools/BRIEF_02_SUMMARY.md.
#
# We re-implement keygen/encaps here rather than monkey-patching
# ``_slwe.rand_nonzd`` because (a) it leaves the supplied source
# untouched and (b) keeps `A` uniform, which a global rand_nonzd
# replacement would not.


def _keygen_small_sr(k: int) -> dict:
    s = [rand_small_nonzd(_slwe.p, eta=2, dim=_DIM) for _ in range(k)]
    A = singer_a_randomized(k, _slwe.p, seed=None, delta=1)
    e = [_slwe.rand_small(eta=2) for _ in range(k)]
    As = _slwe.mat_vec(A, s)
    b = [_slwe.s_add(As[i], e[i]) for i in range(k)]
    return {"sk": s, "A": A, "b": b}


# ---------------------------------------------------------------------------
# Brief 06 (OP-G): Singer-orbit A is rank-deficient at k > 7
# (column equality at distance 7 in A_sed; period 7·DIM in A_F).
# Path A fix: SingerBase + δ · UniformPerturbation, sedenion-componentwise.
# At δ ≥ 1 the perturbation dominates and rank is full with overwhelming
# probability over the sample, but the PSL(2,7) symmetry in A is gone.
# ---------------------------------------------------------------------------


def singer_a_randomized(k: int, p: int, *, seed: int | None = None,
                        delta: int = 1) -> list[list[list[int]]]:
    """SingerBase + δ · UniformPerturbation, k×k of sedenion entries.

    SingerBase[i] = singer_orbit(rand_nonzd(), k) (same as the original
    construction). UniformPerturbation[i][j] is a uniformly random
    sedenion in F_p^DIM. Result entry-wise: ``A[i][j] = (singer[i][j]
    + δ · perturb[i][j]) mod p``.

    At δ ≥ 1 over F_p, the perturbation completely overwrites the Singer
    structure (F_p has no notion of "small δ"); the resulting matrix is
    distributionally identical to a uniform random sedenion matrix
    plus a fixed Singer offset, which is itself uniform random. Brief
    06 Path A documents this trade-off explicitly.
    """
    import random as _r
    if seed is not None:
        _r.seed(seed)
    _slwe.p = p
    singer_part = [_slwe.singer_orbit(_slwe.rand_nonzd(), k)
                   for _ in range(k)]
    A = []
    for i in range(k):
        row = []
        for j in range(k):
            perturb = [_r.randrange(0, p) for _ in range(_DIM)]
            entry = [(singer_part[i][j][c] + delta * perturb[c]) % p
                     for c in range(_DIM)]
            row.append(entry)
        A.append(row)
    return A


def singer_a_pure(k: int, p: int, *, seed: int | None = None
                  ) -> list[list[list[int]]]:
    """The original (rank-deficient) Singer construction.

    Kept as a callable for the regression test that pins the OP-G
    vulnerability. Production callers should use
    :func:`singer_a_randomized` instead.
    """
    import random as _r
    if seed is not None:
        _r.seed(seed)
    _slwe.p = p
    return [_slwe.singer_orbit(_slwe.rand_nonzd(), k) for _ in range(k)]


def _encaps_small_r(A, b_vec, k: int, drbg: DRBG):
    # R2(a) fix: r comes from the caller's DRBG (cryptographic).
    # e1, e2, m_bit remain on the Python random module (MT) — explicitly
    # carved out of R2(a) scope; their security role is DFR / message
    # carrier, not r_upper freshness.
    import random as _r
    m_bit = _r.randint(0, 1)
    q2 = _slwe.p // 2
    r = [_rand_small_nonzd_drbg(drbg, _slwe.p, eta=2, dim=_DIM)
         for _ in range(k)]
    e1 = [_slwe.rand_small(eta=2) for _ in range(k)]
    e2 = _r.choices([-1, 0, 0, 0, 1], weights=[1, 4, 4, 4, 1])[0] % _slwe.p
    AH = _slwe.conj_transpose(A)
    AHr = _slwe.mat_vec(AH, r)
    c1 = [_slwe.s_add(AHr[i], e1[i]) for i in range(k)]
    c2 = (_slwe.norm_inner_k(b_vec, r) + e2 + m_bit * q2) % _slwe.p
    return c1, c2, m_bit


def decaps(sk_bytes: bytes, ct_bytes: bytes, k: int = K_TOY) -> bytes:
    sk = _deserialize_sk(sk_bytes, k)
    c1, c2 = _deserialize_ct(ct_bytes, k)
    m_dec, _v = _slwe.decaps(sk, c1, c2, k)
    return hashlib.sha256(bytes([m_dec & 1]) + ct_bytes).digest()
