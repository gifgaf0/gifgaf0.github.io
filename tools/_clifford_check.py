"""Verification script for tools/clifford_embedding_check.md.

Constructs the six 8x8 Cl(6) generators over F_3329 (Pauli-tensor form,
with ``i = 17^64 mod 3329 = 1729`` as a square root of -1) and confirms
the Clifford relations both on the 8-dim spinor and on the 128-dim
lift Γ_a = I_16 ⊗ γ_a.

Run with: ``python tools/_clifford_check.py``.

Pure CPython, no numpy / sympy / sage. Mod-3329 integer arithmetic only.
"""

from __future__ import annotations

import itertools

Q = 3329
I_UNIT = pow(17, 64, Q)  # = 1729; satisfies I_UNIT^2 == -1 mod Q


def _matmul(A, B):
    n = len(A)
    m = len(B[0])
    k = len(B)
    C = [[0] * m for _ in range(n)]
    for r in range(n):
        ar = A[r]
        cr = C[r]
        for j in range(k):
            v = ar[j]
            if not v:
                continue
            bj = B[j]
            for c in range(m):
                cr[c] = (cr[c] + v * bj[c]) % Q
    return C


def _add(A, B):
    return [[(A[r][c] + B[r][c]) % Q for c in range(len(A[0]))] for r in range(len(A))]


def _scalar(s, A):
    return [[(s * v) % Q for v in row] for row in A]


def _kron(A, B):
    ra, ca = len(A), len(A[0])
    rb, cb = len(B), len(B[0])
    out = [[0] * (ca * cb) for _ in range(ra * rb)]
    for i in range(ra):
        for j in range(ca):
            v = A[i][j]
            if not v:
                continue
            for k in range(rb):
                for l in range(cb):
                    out[i * rb + k][j * cb + l] = (v * B[k][l]) % Q
    return out


def _eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def _zeros(n):
    return [[0] * n for _ in range(n)]


def _neg(x):
    return (-x) % Q


def gamma8():
    SX = [[0, 1], [1, 0]]
    SY = [[0, _neg(I_UNIT)], [I_UNIT, 0]]
    SZ = [[1, 0], [0, _neg(1)]]
    I2 = _eye(2)
    return [
        _kron(SX, _kron(I2, I2)),
        _kron(SY, _kron(I2, I2)),
        _kron(SZ, _kron(SX, I2)),
        _kron(SZ, _kron(SY, I2)),
        _kron(SZ, _kron(SZ, SX)),
        _kron(SZ, _kron(SZ, SY)),
    ]


def gamma128(g8=None):
    g8 = g8 or gamma8()
    I16 = _eye(16)
    return [_kron(I16, g) for g in g8]


def _anticomm(A, B):
    return _add(_matmul(A, B), _matmul(B, A))


def verify_cl6_relations(generators, dim):
    I = _eye(dim)
    Z = _zeros(dim)
    for a, g in enumerate(generators):
        if _matmul(g, g) != I:
            return False, f"gamma_{a+1}^2 != I"
    twoI = _scalar(2, I)
    for a, b in itertools.combinations(range(len(generators)), 2):
        ac = _anticomm(generators[a], generators[b])
        if ac != Z:
            return False, f"{{gamma_{a+1}, gamma_{b+1}}} != 0"
        diag = _anticomm(generators[a], generators[a])
        if diag != twoI:
            return False, f"{{gamma_{a+1}, gamma_{a+1}}} != 2*I"
    return True, "all Clifford relations hold"


def main() -> int:
    g8 = gamma8()
    ok8, msg8 = verify_cl6_relations(g8, 8)
    print(f"Cl(6) on 8-dim spinor: {msg8}")
    if not ok8:
        return 1

    g128 = gamma128(g8)
    ok128, msg128 = verify_cl6_relations(g128, 128)
    print(f"Cl(6) on 128-dim lift: {msg128}")
    return 0 if ok128 else 1


if __name__ == "__main__":
    raise SystemExit(main())
