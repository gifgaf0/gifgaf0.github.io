"""X-Wing on low-order X25519 points follows draft-11, not pyca's all-zero check.

X-Wing (``draft-connolly-cfrg-xwing-kem-11``) takes X25519 from RFC 7748 §5
and applies no check to its output: Encapsulate (§5.4) and Decapsulate (§5.5)
pass the raw value to the combiner, and the draft gives Decapsulate no failure
case. pyca/cryptography raises ``ValueError`` when an X25519 output is
all-zero, which for clamped scalars happens exactly on low-order inputs, so
``combiner/xwing.py`` maps that case back to the RFC 7748 value, 32 zero bytes.

These tests check:

- the hard-coded low-order set: an independent RFC 7748 ladder (itself checked
  against RFC 7748 §5.2 and pyca) gives an all-zero output on every encoding
  of it, and counting roots over F_p shows that no other u-coordinate has
  order dividing 8, on the curve or on its twist;
- that pyca rejects every one of those encodings, so the fallback is reachable,
  and accepts random and near-miss inputs, so it is not taken spuriously;
- that ``decapsulate`` and ``encapsulate`` return the draft's value, recomputed
  here with hashlib rather than through the module under test;
- that any other error still propagates;
- that the ``mlkem1024+x25519`` profile still rejects all-zero X25519 outputs,
  as RFC 9180 §7.1.4 requires of DHKEM recipients.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import types

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import mlkem, x25519

from hybrid_kem.combiner import xwing
from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.hybrid_kem import HybridKEM, _pack, _unpack

P = 2**255 - 19
A = 486662                 # Curve25519: v^2 = u^3 + A u^2 + u
A24 = (A - 2) // 4         # 121665, RFC 7748 §5

# The u-coordinates of the order-8 points of Curve25519. The tests below check
# their order and show that no other u-coordinate has order dividing 8.
U8A = 325606250916557431795983626356110631294008115727848805560023387167927233504
U8B = 39382357235489614581723060781553021112529911719440698176882885853963445705823

LOW_ORDER_U = {0, 1, P - 1, U8A, U8B}

# Every 32-byte encoding of those points, as RFC 7748 decodes it: the top bit
# is masked, and values >= p are reduced, so 0 and 1 also have the
# non-canonical encodings p and p + 1. That is seven values below 2^255, each
# with the top bit clear or set: 14 encodings.
_NAMES = {0: "0", 1: "1", P - 1: "p-1", U8A: "u8a", U8B: "u8b", P: "p", P + 1: "p+1"}
LOW_ORDER_VALUES = sorted(
    r + j * P for r in LOW_ORDER_U for j in range(2) if r + j * P < 2**255
)
LOW_ORDER_CASES = [
    pytest.param(
        (v | (top << 255)).to_bytes(32, "little"),
        id=_NAMES[v] + ("+topbit" if top else ""),
    )
    for v in LOW_ORDER_VALUES
    for top in (0, 1)
]

LABEL = bytes.fromhex("5c2e2f2f5e5c")   # draft §5.3
SEED = bytes(range(32))                 # a fixed X-Wing decapsulation key
SCALAR = bytes([0x5A]) * 32             # a fixed X25519 scalar; any value works

_VEC = os.path.join(os.path.dirname(__file__), "kat_vectors", "x25519_rfc7748.json")
with open(_VEC) as f:
    RFC7748 = json.load(f)


# ----------------------------------------------------------------------------
# Independent reference: RFC 7748 §5, and polynomial arithmetic over F_p.
# ----------------------------------------------------------------------------

def _ladder(k: int, u: int) -> int:
    """u([k]P) for u = u(P), by the RFC 7748 §5 Montgomery ladder.

    The result is 0 exactly when [k]P is the point at infinity or (0, 0).
    """
    x1 = u % P
    x2, z2, x3, z3 = 1, 0, x1, 1
    swap = 0
    for t in reversed(range(255)):
        k_t = (k >> t) & 1
        swap ^= k_t
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = k_t
        a, b = x2 + z2, x2 - z2
        aa, bb = a * a % P, b * b % P
        e = aa - bb
        c, d = x3 + z3, x3 - z3
        da, cb = d * a % P, c * b % P
        x3, z3 = (da + cb) ** 2 % P, x1 * (da - cb) ** 2 % P
        x2, z2 = aa * bb % P, e * (aa + A24 * e) % P
    if swap:
        x2, z2 = x3, z3
    return x2 * pow(z2, P - 2, P) % P


def _x25519_ref(k: bytes, u: bytes) -> bytes:
    """RFC 7748 X25519: clamp the scalar, mask the top bit of u, run the ladder."""
    s = bytearray(k)
    s[0] &= 248
    s[31] &= 127
    s[31] |= 64
    u_int = int.from_bytes(u, "little") & ((1 << 255) - 1)
    return _ladder(int.from_bytes(s, "little"), u_int).to_bytes(32, "little")


def _x25519_pyca(k: bytes, u: bytes) -> bytes:
    priv = x25519.X25519PrivateKey.from_private_bytes(k)
    return priv.exchange(x25519.X25519PublicKey.from_public_bytes(u))


def _poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return out


def _poly_norm(a: list[int]) -> list[int]:
    """Coefficients reduced mod p, leading zeros dropped; [0] is zero."""
    a = [c % P for c in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def _poly_mod(a: list[int], m: list[int]) -> list[int]:
    """a mod m over F_p, coefficients lowest degree first (m normalized)."""
    a = [c % P for c in a]
    inv = pow(m[-1], P - 2, P)
    while len(a) >= len(m):
        q = a[-1] * inv % P
        off = len(a) - len(m)
        for i, c in enumerate(m):
            a[off + i] = (a[off + i] - q * c) % P
        a.pop()
    return _poly_norm(a)


def _poly_eval(f: list[int], x: int) -> int:
    return sum(c * pow(x, i, P) for i, c in enumerate(f)) % P


def _roots_in_fp(f: list[int]) -> int:
    """Number of distinct roots of f in F_p: the degree of gcd(f, x^p - x)."""
    f = _poly_norm(f)
    xp, base, e = [1], [0, 1], P
    while e:
        if e & 1:
            xp = _poly_mod(_poly_mul(xp, base), f)
        base = _poly_mod(_poly_mul(base, base), f)
        e >>= 1
    g = xp + [0] * (2 - len(xp))
    g[1] -= 1                                   # x^p - x, reduced mod f
    a, b = f, _poly_norm(g)
    while b != [0]:
        a, b = b, _poly_mod(a, b)
    return len(a) - 1


def _xwing_combiner(ss_m: bytes, ss_x: bytes, ct_x: bytes, pk_x: bytes) -> bytes:
    return hashlib.sha3_256(ss_m + ss_x + ct_x + pk_x + LABEL).digest()


def _x25519_public(k: bytes) -> bytes:
    return x25519.X25519PrivateKey.from_private_bytes(k).public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )


# ----------------------------------------------------------------------------
# The low-order set.
# ----------------------------------------------------------------------------

def test_reference_ladder_matches_rfc7748_and_pyca():
    for v in RFC7748["single"]:
        out = _x25519_ref(bytes.fromhex(v["scalar"]), bytes.fromhex(v["u"]))
        assert out.hex() == v["out"]
    nine = (9).to_bytes(32, "little")
    assert _x25519_ref(nine, nine).hex() == RFC7748["iterated_after_1"]
    rnd = random.Random(7748)
    for _ in range(64):
        k, u = rnd.randbytes(32), rnd.randbytes(32)
        assert _x25519_ref(k, u) == _x25519_pyca(k, u)


def test_module_uses_this_set():
    assert xwing._P25519 == P
    assert xwing._LOW_ORDER_U == LOW_ORDER_U
    assert len(LOW_ORDER_CASES) == 14


def test_listed_points_have_order_dividing_8():
    # _ladder(k, u) == 0 means [k]P is the point at infinity or (0, 0).
    for u in LOW_ORDER_U:
        assert _ladder(8, u) == 0
    assert _ladder(2, 1) == _ladder(2, P - 1) == 0      # order 4: [2]P = (0, 0)
    assert _ladder(2, U8A) == _ladder(2, U8B) == 1      # order 8: u([2]P) = 1
    assert _ladder(4, U8A) == _ladder(4, U8B) == 0


def test_no_other_u_has_order_dividing_8():
    """Completeness, for the curve and its twist at once (u-only arithmetic).

    Doubling: u([2]P) = (u^2 - 1)^2 / (4u(u^2 + Au + 1)).
    - order 2: 4u(u^2 + Au + 1) = 0, so u = 0, as u^2 + Au + 1 has no root in
      F_p (its discriminant A^2 - 4 is a non-square);
    - order 4: u([2]P) = 0, so u = 1 or p - 1;
    - order 8: u([2]P) = 1 or -1, i.e. u is a root of
      (u^2 - 1)^2 - 4u(u^2 + Au + 1) or of (u^2 - 1)^2 + 4u(u^2 + Au + 1).
    The first quartic has exactly two roots in F_p, U8A and U8B; the second
    has none. Since #E = 8l and #E' = 4l' with l, l' primes above 2^252
    (Bernstein, Curve25519, 2006), and a clamped scalar is 8m with m < 2^252,
    the X25519 output is all-zero exactly on this set.
    """
    # The root counter on known cases: x^2 + 1 splits (p = 1 mod 4) and
    # x^2 - 2 does not (p = 5 mod 8).
    two_roots = _poly_mul([-2, 1], [-3, 1])
    assert _roots_in_fp(two_roots) == 2
    assert _roots_in_fp(_poly_mul(two_roots, [1, 0, 1])) == 4
    assert _roots_in_fp(_poly_mul(two_roots, [-2, 0, 1])) == 2

    assert pow(A * A - 4, (P - 1) // 2, P) == P - 1
    doubles_to_one = [1, -4, -(4 * A + 2), -4, 1]
    doubles_to_minus_one = [1, 4, 4 * A - 2, 4, 1]
    assert _roots_in_fp(doubles_to_one) == 2
    assert _poly_eval(doubles_to_one, U8A) == _poly_eval(doubles_to_one, U8B) == 0
    assert _roots_in_fp(doubles_to_minus_one) == 0


@pytest.mark.parametrize("u", LOW_ORDER_CASES)
def test_low_order_encoding_gives_zero_and_pyca_raises(u):
    rnd = random.Random(u)
    for _ in range(4):
        assert _x25519_ref(rnd.randbytes(32), u) == bytes(32)
    with pytest.raises(ValueError):
        _x25519_pyca(SCALAR, u)
    assert xwing._is_low_order(u)
    assert xwing._x25519_dh(SCALAR, u) == bytes(32)


def test_no_false_positives():
    rnd = random.Random(20261015)
    near_misses = [2, 9, P - 2, P + 2, U8A + 1, U8B - 1, 2**255 - 1]
    cases = [v.to_bytes(32, "little") for v in near_misses]
    cases += [rnd.randbytes(32) for _ in range(256)]
    for u in cases:
        assert not xwing._is_low_order(u)
        out = _x25519_pyca(SCALAR, u)                 # pyca accepts these
        assert out != bytes(32)
        assert xwing._x25519_dh(SCALAR, u) == out == _x25519_ref(SCALAR, u)


# ----------------------------------------------------------------------------
# X-Wing follows the draft.
# ----------------------------------------------------------------------------

@pytest.mark.parametrize("ct_x", LOW_ORDER_CASES)
def test_decapsulate_low_order_ct_x_returns_draft_value(ct_x):
    sk, pk = xwing.generate_keypair_derand(SEED)
    pk_m, pk_x = pk[:1184], pk[1184:]
    ss_m, ct_m = mlkem.MLKEM768PublicKey.from_public_bytes(pk_m).encapsulate()
    ct = ct_m + ct_x
    expected = _xwing_combiner(ss_m, bytes(32), ct_x, pk_x)
    assert xwing.decapsulate(ct, sk) == expected
    assert HybridKEM(profile="xwing").decaps(sk, ct) == expected


@pytest.mark.parametrize("pk_x", LOW_ORDER_CASES)
def test_encapsulate_to_low_order_pk_x_returns_draft_value(pk_x):
    _, pk = xwing.generate_keypair_derand(SEED)
    ss, ct = xwing.encapsulate(pk[:1184] + pk_x, rng=lambda n: SCALAR[:n])
    ct_m, ct_x = ct[:1088], ct[1088:]
    assert ct_x == _x25519_public(SCALAR)
    sk_m = mlkem.MLKEM768PrivateKey.from_seed_bytes(
        hashlib.shake_256(SEED).digest(96)[:64]          # draft §5.2
    )
    assert ss == _xwing_combiner(sk_m.decapsulate(ct_m), bytes(32), ct_x, pk_x)


def test_other_x25519_errors_propagate(monkeypatch):
    """Only the all-zero case is mapped: a failure on any other input re-raises."""

    class _Failing:
        def exchange(self, peer):
            raise ValueError("simulated pyca failure")

    fake = types.SimpleNamespace(
        X25519PrivateKey=types.SimpleNamespace(from_private_bytes=lambda b: _Failing()),
        X25519PublicKey=x25519.X25519PublicKey,
    )
    monkeypatch.setattr(xwing, "x25519", fake)
    with pytest.raises(ValueError, match="simulated pyca failure"):
        xwing._x25519_dh(SCALAR, (9).to_bytes(32, "little"))
    # On a low-order input the RFC 7748 output is all-zero for every clamped
    # scalar, so zeros are right whatever the reason pyca raised.
    assert xwing._x25519_dh(SCALAR, bytes(32)) == bytes(32)


def test_wrong_lengths_still_raise():
    assert not xwing._is_low_order(bytes(31))
    assert not xwing._is_low_order(bytes(33))
    with pytest.raises(ValueError):
        xwing._x25519_dh(SCALAR, bytes(31))
    sk, pk = xwing.generate_keypair_derand(SEED)
    with pytest.raises(ValueError):
        xwing.decapsulate(bytes(xwing.CT_LEN - 1), sk)
    with pytest.raises(ValueError):
        xwing.encapsulate(pk[:-1], rng=lambda n: SCALAR[:n])


# ----------------------------------------------------------------------------
# The ML-KEM-1024 profile keeps rejecting (RFC 9180 §7.1.4).
# ----------------------------------------------------------------------------

def _drbg(tag: bytes) -> DRBG:
    d = DRBG()
    d.instantiate(b"\x11" * 32, b"\x22" * 16, tag)
    return d


@pytest.fixture(scope="module")
def mlkem1024_session():
    h = HybridKEM(profile="mlkem1024+x25519")
    pk, sk = h.keygen(_drbg(b"low-order keygen"))
    ct, _ = h.encaps(pk, _drbg(b"low-order encaps"))
    return h, pk, sk, ct


@pytest.mark.parametrize("u", LOW_ORDER_CASES)
def test_mlkem1024_profile_still_rejects_low_order(mlkem1024_session, u):
    h, pk, sk, ct = mlkem1024_session
    ct_m, _ = _unpack(ct, 2)
    with pytest.raises(ValueError):
        h.decaps(sk, _pack(ct_m, u))
    pk_m, _ = _unpack(pk, 2)
    with pytest.raises(ValueError):
        h.encaps(_pack(pk_m, u), _drbg(b"low-order encaps"))
