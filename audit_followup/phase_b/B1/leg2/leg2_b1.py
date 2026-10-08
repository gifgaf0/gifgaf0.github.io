#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leg2_b1.py -- B1 check, independent second leg (blind).

Everything is computed from scratch.  Exact arithmetic (sympy / fractions) is
used throughout, except for the C5 pulls, which are computed in IEEE doubles
and re-checked with 50-digit mpmath.

  C1  8-dim fermionic Fock space realised on the complex octonions C(x)O:
      Furey's ladder operators act by LEFT MULTIPLICATION (8x8 complex
      matrices); no Kronecker / Jordan-Wigner product is used anywhere.
      su(3) generators T^a = sum_ij alpha_i^dag M^a_ij alpha_j with
      M^a = lambda^a/2 (rho = 3) or M^a = -conj(lambda^a)/2 (rho = 3bar);
      colour content (1 / 3 / 3bar) of each N-sector.
  S1  supplementary cross-check (not one of C1..C6): Der(O) = g2, its
      stabiliser of e7, and how it relates to the T^a and the N-sectors.
  C2  additivity of the paper's Y(N) = (-1)^(N+1) N/3.
  C3  the eight "Furey options" (q(N), rho).
  C4  the paper's (colour, Y) pairs under the induced colours.
  C5  pulls of 3/13 against PDG 2024 CKM inputs.
  C6  automorphism group and orientation behaviour of the 7-vertex
      (Csaszar) torus, by brute force over S_7.

Writes leg2_results.json next to this file; the log goes to stdout.
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction

import mpmath
import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(name, cond):
    cond = bool(cond)
    CHECKS.append((name, cond))
    print(f"    [{'ok' if cond else 'FAIL'}] {name}")
    return cond


def banner(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def is_zero(M):
    return all(sp.expand(x) == 0 for x in M)


def meq(A, B):
    return is_zero(A - B)


def xrank(M):
    """Exact rank (entries in Q or Q(i))."""
    return DomainMatrix.from_Matrix(M).rank()


def comm(X, Y):
    return X * Y - Y * X


def acomm(X, Y):
    return X * Y + Y * X


def fstr(q):
    """Fraction -> string like '-2/3', '0', '1'."""
    return str(Fraction(q))


I = sp.I
h = sp.Rational(1, 2)
E8 = sp.eye(8)

# =============================================================================
banner("C1. 8-dim Fock space on the complex octonions C(x)O (no Kronecker product)")
# =============================================================================
print("Octonion multiplication table: e_i e_{i+1} = e_{i+3}, indices mod 7 in 1..7;")
print("e_0 = 1, e_k^2 = -1, each quaternionic triple (a,b,c) gives e_a e_b = e_c,")
print("cyclic e_b e_c = e_a, e_c e_a = e_b, and anticommutation e_b e_a = -e_c, etc.")


def m7(k):
    return (k - 1) % 7 + 1


TRIPLES = [(i, m7(i + 1), m7(i + 3)) for i in range(1, 8)]
print("  triples (a,b,c) with e_a e_b = e_c:", TRIPLES)

MULT = [[None] * 8 for _ in range(8)]  # MULT[j][k] = (sign, index) of e_j e_k
for j in range(8):
    MULT[0][j] = (1, j)
    MULT[j][0] = (1, j)
for j in range(1, 8):
    MULT[j][j] = (-1, 0)
for (a, b, c) in TRIPLES:
    for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
        MULT[x][y] = (1, z)
        MULT[y][x] = (-1, z)

print("  multiplication table, entry = e_row * e_col:")
print("          " + "".join(f"{'e' + str(c):>6}" for c in range(1, 8)))
for r in range(1, 8):
    row = f"      e{r}  "
    for c in range(1, 8):
        s, m = MULT[r][c]
        row += f"{('+' if s > 0 else '-') + ('1' if m == 0 else 'e' + str(m)):>6}"
    print(row)

pairs = [frozenset(p) for t in TRIPLES for p in itertools.combinations(t, 2)]
check("every pair of imaginary units lies in exactly one triple (Fano plane, table well defined)",
      len(pairs) == 21 and len(set(pairs)) == 21
      and all(MULT[j][k] is not None for j in range(8) for k in range(8)))


def L_basis(k):
    M = sp.zeros(8, 8)
    for j in range(8):
        s, m = MULT[k][j]
        M[m, j] = s
    return M


def R_basis(k):
    M = sp.zeros(8, 8)
    for j in range(8):
        s, m = MULT[j][k]
        M[m, j] = s
    return M


L = [L_basis(k) for k in range(8)]   # L[k] x = e_k x
R = [R_basis(k) for k in range(8)]   # R[k] x = x e_k
check("L_{e0} = identity", meq(L[0], E8))
check("L_{ek} real antisymmetric for k = 1..7", all(meq(L[k].T, -L[k]) for k in range(1, 8)))
check("left Clifford relations {L_j, L_k} = -2 delta_jk (j,k = 1..7)  [left alternativity]",
      all(meq(acomm(L[j], L[k]), -2 * E8 if j == k else sp.zeros(8, 8))
          for j in range(1, 8) for k in range(j, 8)))
check("right Clifford relations {R_j, R_k} = -2 delta_jk (j,k = 1..7)  [right alternativity]",
      all(meq(acomm(R[j], R[k]), -2 * E8 if j == k else sp.zeros(8, 8))
          for j in range(1, 8) for k in range(j, 8)))
# L_x^T L_x = |x|^2 for all real x follows from the two checks above, so the
# table defines an 8-dim composition algebra with unit = the octonions (Hurwitz).
e = [E8[:, k] for k in range(8)]
check("non-associative: (e1 e2) e3 != e1 (e2 e3)",
      not meq(L[MULT[1][2][1]] * e[3] * MULT[1][2][0], L[1] * (L[2] * e[3])))


def ovec(d):
    v = sp.zeros(8, 1)
    for k, c in d.items():
        v[k] += c
    return v


def odag(v):
    """hermitian conjugate of a complex octonion: complex conj (i -> -i) and octonion conj."""
    w = v.conjugate()
    for k in range(1, 8):
        w[k] = -w[k]
    return w


def Lof(v):
    M = sp.zeros(8, 8)
    for k in range(8):
        if v[k] != 0:
            M += v[k] * L[k]
    return M


def ostr(v):
    terms = []
    for k in range(8):
        c = sp.nsimplify(sp.expand(v[k]))
        if c != 0:
            terms.append(f"({c})" + ("" if k == 0 else f" e{k}"))
    return " + ".join(terms) if terms else "0"


def print_matrix(name, M):
    """8x8 matrix in the basis (1, e1, ..., e7); column j = image of basis element j."""
    cells = [[str(sp.nsimplify(sp.expand(M[r, c]))).replace("I", "i") for c in range(M.cols)]
             for r in range(M.rows)]
    wd = max(len(x) for row in cells for x in row) + 1
    print(f"  {name}  (rows/cols = 1, e1..e7):")
    for row in cells:
        print("     [" + "".join(f"{x:>{wd}}" for x in row) + " ]")


print("\nFurey ladder operators (left multiplication on C(x)O):")
alpha = [ovec({5: -h, 4: I * h}),   # alpha1 = (-e5 + i e4)/2
         ovec({3: -h, 1: I * h}),   # alpha2 = (-e3 + i e1)/2
         ovec({6: -h, 2: I * h})]   # alpha3 = (-e6 + i e2)/2
A = [Lof(x) for x in alpha]
Ad = [Lof(odag(x)) for x in alpha]
for i in range(3):
    print(f"  alpha{i + 1}     = {ostr(alpha[i])}")
    print(f"  alpha{i + 1}^dag = {ostr(odag(alpha[i]))}")
for i in range(3):
    print_matrix(f"L(alpha{i + 1})", A[i])
check("L_{alpha_i^dag} equals the conjugate transpose of L_{alpha_i} (i = 1,2,3)",
      all(meq(Ad[i], A[i].H) for i in range(3)))
check("{alpha_i, alpha_j^dag} = delta_ij * 1_8 (all i,j)",
      all(meq(acomm(A[i], Ad[j]), E8 if i == j else sp.zeros(8, 8)) for i in range(3) for j in range(3)))
check("{alpha_i, alpha_j} = 0 and {alpha_i^dag, alpha_j^dag} = 0 (all i,j)",
      all(is_zero(acomm(A[i], A[j])) and is_zero(acomm(Ad[i], Ad[j])) for i in range(3) for j in range(3)))
print("  => the table e_i e_{i+1} = e_{i+3} works as given; no adjustment was needed.")

Nop = sum((Ad[i] * A[i] for i in range(3)), sp.zeros(8, 8))
xs = sp.Symbol("x")
cp = sp.factor(Nop.charpoly(xs).as_expr())
print_matrix("N = sum_i L(alpha_i)^dag L(alpha_i)", Nop)
print(f"  number operator N = sum alpha_i^dag alpha_i ; charpoly = {cp}")
check("N has eigenvalues 0,1,2,3 with multiplicities 1,3,3,1",
      sp.expand(cp - xs * (xs - 1) ** 3 * (xs - 2) ** 3 * (xs - 3)) == 0)

print("\nVacuum from the idempotent omega omega^dag, omega = alpha1 alpha2 alpha3 (operator chain):")
Om_ = A[0] * A[1] * A[2]
Om = Om_ * Om_.H
v0 = Om * e[0]                      # (omega omega^dag) acting on 1
print(f"  v0 = (omega omega^dag) 1 = {ostr(v0)}")
check("omega omega^dag is a hermitian idempotent of rank 1 and trace 1",
      meq(Om * Om, Om) and meq(Om.H, Om) and xrank(Om) == 1 and sp.expand(Om.trace()) == 1)
check("omega omega^dag = |v0><v0| / <v0|v0>  (projector onto v0)",
      meq(Om, v0 * v0.H / sp.expand((v0.H * v0)[0, 0])))
check("alpha_i v0 = 0 for i = 1,2,3", all(is_zero(A[i] * v0) for i in range(3)))
check("joint kernel of alpha_1, alpha_2, alpha_3 is 1-dimensional",
      8 - xrank(A[0].col_join(A[1]).col_join(A[2])) == 1)

fock = {
    0: [("v0", v0)],
    1: [(f"a{i + 1}^dag v0", Ad[i] * v0) for i in range(3)],
    2: [(f"a{i + 1}^dag a{j + 1}^dag v0", Ad[i] * Ad[j] * v0) for (i, j) in ((0, 1), (0, 2), (1, 2))],
    3: [("a3^dag a2^dag a1^dag v0", Ad[2] * Ad[1] * Ad[0] * v0)],
}
print("\nFock states realised as complex octonions:")
for n in range(4):
    for (lab, v) in fock[n]:
        print(f"  N={n}: {lab:24s} = {ostr(v)}")
allv = [v for n in range(4) for (_, v) in fock[n]]
Bmat = sp.Matrix.hstack(*allv)
check("each Fock vector is an N-eigenvector with the expected eigenvalue",
      all(meq(Nop * v, n * v) for n in range(4) for (_, v) in fock[n]))
check("the 8 Fock vectors are pairwise orthogonal with equal norm^2 = 1/2 (they span C(x)O = C^8)",
      meq(Bmat.H * Bmat, h * E8) and xrank(Bmat) == 8)

print("\nLeft ideal generated by the idempotent:")
mons = []
for mask in range(64):
    M = E8
    for k in range(1, 7):
        if mask >> (k - 1) & 1:
            M = M * L[k]
    mons.append(M)
flat = lambda M: [M[r, c] for r in range(8) for c in range(8)]
check("the 64 monomials in L_{e1..e6} are linearly independent (generate M_8(C) = Cl_6(C))",
      xrank(sp.Matrix([flat(M) for M in mons])) == 64)
ideal = [M * Om for M in mons]
rk_ideal = xrank(sp.Matrix([flat(M) for M in ideal]))
fock_ideal = [Om] + [Ad[i] * Om for i in range(3)] + \
             [Ad[i] * Ad[j] * Om for (i, j) in ((0, 1), (0, 2), (1, 2))] + [Ad[2] * Ad[1] * Ad[0] * Om]
check(f"dim of left ideal M_8(C) * (omega omega^dag) = {rk_ideal} (= 8, minimal left ideal)", rk_ideal == 8)
check("Fock elements {W, a_i^dag W, a_i^dag a_j^dag W, a3^dag a2^dag a1^dag W} (W = omega omega^dag) span that ideal",
      xrank(sp.Matrix([flat(M) for M in fock_ideal])) == 8
      and xrank(sp.Matrix([flat(M) for M in fock_ideal + ideal])) == 8)
check("ideal element X W acting on 1 gives the Fock octonion X v0 (ideal ~ C(x)O as modules)",
      all(meq(F * e[0], v) for F, v in zip(fock_ideal, allv)))

# ---------------------------------------------------------------- su(3)
lam = [
    sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
    sp.Matrix([[0, -I, 0], [I, 0, 0], [0, 0, 0]]),
    sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]),
    sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
    sp.Matrix([[0, 0, -I], [0, 0, 0], [I, 0, 0]]),
    sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
    sp.Matrix([[0, 0, 0], [0, 0, -I], [0, I, 0]]),
    sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / sp.sqrt(3),
]
fabc, dabc = {}, {}
for a, b, c in itertools.product(range(8), repeat=3):
    fv = sp.nsimplify(sp.expand((comm(lam[a], lam[b]) * lam[c]).trace() / (4 * I)))
    dv = sp.nsimplify(sp.expand((acomm(lam[a], lam[b]) * lam[c]).trace() / 4))
    if fv != 0:
        fabc[(a, b, c)] = fv
    if dv != 0:
        dabc[(a, b, c)] = dv
print("\nGell-Mann structure constants (1-based, sorted index triples):")
print("  f_abc:", {f"{a + 1}{b + 1}{c + 1}": str(v) for (a, b, c), v in fabc.items() if a < b < c})
print("  d_abc:", {f"{a + 1}{b + 1}{c + 1}": str(v) for (a, b, c), v in dabc.items() if a <= b <= c})
check("tr(lambda_a lambda_b) = 2 delta_ab; f_123 = 1; d_888 = -1/sqrt(3)",
      all(sp.expand((lam[a] * lam[b]).trace() - (2 if a == b else 0)) == 0 for a in range(8) for b in range(8))
      and fabc[(0, 1, 2)] == 1 and sp.expand(dabc[(7, 7, 7)] + 1 / sp.sqrt(3)) == 0)

print("\nColour-classification criterion for an N-sector V_N (dimension d):")
print("  restrict T^a to V_N (exact), C2 = sum_a T^a T^a, C3 = sum_abc d_abc T^a T^b T^c;")
print("  '1'    : d = 1 and every T^a = 0 on V_N;")
print("  '3'    : d = 3, C2 = 4/3, C3 = +10/9 (the rep with generators lambda/2);")
print("  '3bar' : d = 3, C2 = 4/3, C3 = -10/9 (generators -conj(lambda)/2).")
print("  Cross-check by (T3, T8) weights: '3' has {(1/2, sqrt3/6), (-1/2, sqrt3/6), (0, -sqrt3/3)},")
print("  '3bar' the negatives; equivalently T8 = (+,+,--) for 3 and (-,-,++) for 3bar.")

W3 = {(h, sp.sqrt(3) / 6), (-h, sp.sqrt(3) / 6), (sp.Integer(0), -sp.sqrt(3) / 3)}
W3BAR = {(-x, -y) for (x, y) in W3}
PAIR = [[Ad[i] * A[j] for j in range(3)] for i in range(3)]


def build_T(Ms):
    Ts = []
    for M in Ms:
        T = sp.zeros(8, 8)
        for i in range(3):
            for j in range(3):
                if M[i, j] != 0:
                    T += M[i, j] * PAIR[i][j]
        Ts.append(T.applyfunc(sp.expand))
    return Ts


def sector_rep(Ts, n):
    Bn = sp.Matrix.hstack(*[v for (_, v) in fock[n]])
    G = (Bn.H * Bn).inv()
    Rs = [(G * Bn.H * T * Bn).applyfunc(sp.expand) for T in Ts]
    invariant = all(meq(T * Bn, Bn * Rn) for T, Rn in zip(Ts, Rs))
    return Rs, invariant


def classify(Rs):
    dim = Rs[0].shape[0]
    C2 = sum((Rm * Rm for Rm in Rs), sp.zeros(dim, dim)).applyfunc(sp.expand)
    C3 = sp.zeros(dim, dim)
    for (a, b, c), dv in dabc.items():
        C3 += dv * Rs[a] * Rs[b] * Rs[c]
    C3 = C3.applyfunc(sp.expand)
    c2, c3 = C2[0, 0], C3[0, 0]
    scalar = meq(C2, c2 * sp.eye(dim)) and meq(C3, c3 * sp.eye(dim))
    H3, H8 = Rs[2], Rs[7]
    diag = is_zero(H3 - sp.diag(*[H3[k, k] for k in range(dim)])) and \
        is_zero(H8 - sp.diag(*[H8[k, k] for k in range(dim)]))
    weights = sorted([(sp.nsimplify(H3[k, k]), sp.nsimplify(H8[k, k])) for k in range(dim)],
                     key=lambda w: (float(w[0]), float(w[1])))
    if dim == 1 and all(is_zero(Rm) for Rm in Rs):
        lab = "1"
    elif dim == 3 and c2 == sp.Rational(4, 3) and c3 == sp.Rational(10, 9):
        lab = "3"
    elif dim == 3 and c2 == sp.Rational(4, 3) and c3 == -sp.Rational(10, 9):
        lab = "3bar"
    else:
        lab = "?"
    wset = set(weights)
    if dim == 1 and wset == {(0, 0)}:
        labw = "1"
    elif wset == W3:
        labw = "3"
    elif wset == W3BAR:
        labw = "3bar"
    else:
        labw = "?"
    return lab, labw, c2, c3, scalar, diag, weights


sector_colors = {}
Tsets = {}
for rho in ("3", "3bar"):
    Ms = [lm / 2 for lm in lam] if rho == "3" else [-lm.conjugate() / 2 for lm in lam]
    print(f"\n--- rho = {rho}:  M^a = {'lambda^a/2' if rho == '3' else '-conj(lambda^a)/2'} ---")
    check(f"[M^a, M^b] = i f_abc M^c (rho = {rho} is a representation)",
          all(meq(comm(Ms[a], Ms[b]), I * sum((fabc.get((a, b, c), 0) * Ms[c] for c in range(8)),
                                                sp.zeros(3, 3)))
              for a in range(8) for b in range(a + 1, 8)))
    Ts = build_T(Ms)
    Tsets[rho] = Ts
    check(f"[T^a, T^b] = i f_abc T^c on C(x)O (rho = {rho})",
          all(meq(comm(Ts[a], Ts[b]), I * sum((fabc.get((a, b, c), 0) * Ts[c] for c in range(8)),
                                                sp.zeros(8, 8)))
              for a in range(8) for b in range(a + 1, 8)))
    check(f"[T^a, alpha_k^dag] = sum_i M^a_ik alpha_i^dag  (creation operators transform as {rho})",
          all(meq(comm(Ts[a], Ad[k]), sum((Ms[a][i, k] * Ad[i] for i in range(3)), sp.zeros(8, 8)))
              for a in range(8) for k in range(3)))
    check(f"[T^a, N] = 0 (rho = {rho})", all(is_zero(comm(T, Nop)) for T in Ts))
    sector_colors[rho] = {}
    for n in range(4):
        Rs, inv = sector_rep(Ts, n)
        lab, labw, c2, c3, scalar, diag, weights = classify(Rs)
        dim = len(fock[n])
        wtxt = ", ".join(f"({w[0]}, {w[1]})" for w in weights)
        print(f"  N={n}: dim {dim}; C2 = {c2}, C3 = {c3}; (T3,T8) weights: {wtxt}")
        print(f"        -> Casimir label '{lab}', weight label '{labw}'")
        check(f"N={n} sector invariant, Casimirs scalar, Cartan diagonal, labels agree (rho={rho})",
              inv and scalar and diag and lab == labw and lab != "?")
        sector_colors[rho][str(n)] = lab

print("\nC1 result (induced colour of each N-sector):")
for rho in ("3", "3bar"):
    print(f"  rho = {rho:4s}: " + ", ".join(f"N={n} -> {sector_colors[rho][str(n)]}" for n in range(4)))

# =============================================================================
banner("S1. Supplementary: G2 = Der(O), the stabiliser of e7, and the N-sectors")
# =============================================================================
print("(Not one of C1..C6; ties the T^a to the paper's Section-3 colour group.)")


def derivation_matrix(fix=()):
    rows = []
    for j in range(8):
        for k in range(8):
            blk = [[0] * 64 for _ in range(8)]
            s, p = MULT[j][k]
            for m in range(8):           # D(e_j e_k) = s * D(e_p)
                blk[m][m * 8 + p] += s
            for m in range(8):           # - D(e_j) e_k
                s2, r = MULT[m][k]
                blk[r][m * 8 + j] -= s2
            for m in range(8):           # - e_j D(e_k)
                s3, r = MULT[j][m]
                blk[r][m * 8 + k] -= s3
            rows.extend(blk)
    for n in fix:                        # D(e_n) = 0
        for m in range(8):
            row = [0] * 64
            row[m * 8 + n] = 1
            rows.append(row)
    rows = [list(r) for r in {tuple(r) for r in rows} if any(r)]
    return sp.Matrix(sorted(rows))


def nullspace_mats(Mc):
    ns = Mc.nullspace()
    return [sp.Matrix(8, 8, lambda m, n: v[m * 8 + n]) for v in ns]


Der = nullspace_mats(derivation_matrix())
Der7 = nullspace_mats(derivation_matrix(fix=(7,)))
print(f"  dim Der(O) = {len(Der)};  dim {{D in Der(O): D e7 = 0}} = {len(Der7)}")
check("dim Der(O) = 14 (g2) and its stabiliser of e7 has dim 8 (su(3))", len(Der) == 14 and len(Der7) == 8)
realT = [(-I * T).applyfunc(sp.expand) for T in Tsets["3"]]
check("-i T^a is a real antisymmetric 8x8 matrix (T^a generates real rotations of O)",
      all(meq(X, X.conjugate()) and meq(X.T, -X) for X in realT))


def rational_rows(mats):
    """flatten; a matrix containing sqrt(3) (only -i T^8) is rescaled by sqrt(3) -- same span."""
    rows = []
    for X in mats:
        fl = [sp.expand(v) for v in flat(X)]
        if any(v.has(sp.sqrt(3)) for v in fl):
            fl = [sp.expand(v * sp.sqrt(3)) for v in fl]
        assert all(v.is_Rational for v in fl)
        rows.append(fl)
    return sp.Matrix(rows)


rkD = xrank(rational_rows(Der7))
rkT = xrank(rational_rows(realT))
rkDT = xrank(rational_rows(Der7 + realT))
check(f"span_R{{-i T^a}} = stabiliser of e7 in g2 (ranks: Der7 {rkD}, T {rkT}, joint {rkDT})",
      rkD == 8 and rkT == 8 and rkDT == 8)
u = [v for (_, v) in fock[1]]
w = [v for (_, v) in fock[2]]
check("N=1 sector = {x in span_C(e1..e6): e7 x = +i x}; N=2 sector = {... e7 x = -i x}",
      all(meq(L[7] * v, I * v) and v[0] == 0 and v[7] == 0 for v in u)
      and all(meq(L[7] * v, -I * v) and v[0] == 0 and v[7] == 0 for v in w))
check("complex conjugation maps the N=1 sector onto the N=2 sector (and N=0 onto N=3)",
      xrank(sp.Matrix.hstack(*[v.conjugate() for v in u], *w)) == 3
      and xrank(sp.Matrix.hstack(fock[0][0][1].conjugate(), fock[3][0][1])) == 1)
print("  => the paper's Section-3 colour algebra (stabiliser of e7 in G2) IS span{T^a};")
print("     on the six units e1..e6 it acts as (N=1 sector) + (N=2 sector) = 3 + 3bar,")
print("     the two sectors being complex conjugates of each other inside C(x)O.  Since the")
print("     colour group acts by real automorphisms of O, N=1 and N=2 always carry mutually")
print("     conjugate (inequivalent) representations, whatever labelling of generators is used.")

# =============================================================================
banner("C2. Is Y(N) = (-1)^(N+1) N/3 additive, i.e. of the form a + b N ?")
# =============================================================================
Y = {N: Fraction((-1) ** (N + 1) * N, 3) for N in range(4)}
print("  paper's Y:", {N: fstr(Y[N]) for N in range(4)})
a0, b0 = Y[0], Y[1] - Y[0]
fitY = {N: a0 + b0 * N for N in range(4)}
additive = all(Y[N] == fitY[N] for N in range(4))
print(f"  unique a + bN through N=0,1: a = {fstr(a0)}, b = {fstr(b0)} -> predicts",
      {N: fstr(fitY[N]) for N in range(4)})
print("  second differences Y(N+2) - 2Y(N+1) + Y(N):",
      [fstr(Y[N + 2] - 2 * Y[N + 1] + Y[N]) for N in range(2)], "(all zero iff affine)")
rows_, rhs_ = [], []
for occ in itertools.product((0, 1), repeat=3):
    rows_.append([1, *occ])
    q = Y[sum(occ)]
    rhs_.append(sp.Rational(q.numerator, q.denominator))
Mx = sp.Matrix(rows_)
per_mode = Mx.rank() == Mx.row_join(sp.Matrix(rhs_)).rank()
print(f"  general per-mode form c + y_a n_a + y_b n_b + y_g n_g solvable over the 8 states: {per_mode}")
print(f"  additive = {additive}")
check("C2 a+bN test and per-mode linear test agree", additive == per_mode)

# =============================================================================
banner("C3. Furey's options: q(N) in {N/3, -N/3, (3-N)/3, -(3-N)/3} x rho in {3, 3bar}")
# =============================================================================
QF = [("N/3", lambda N: Fraction(N, 3)),
      ("-N/3", lambda N: Fraction(-N, 3)),
      ("(3-N)/3", lambda N: Fraction(3 - N, 3)),
      ("-(3-N)/3", lambda N: Fraction(-(3 - N), 3))]
PAPER = {0: ("1", Fraction(0)), 1: ("3bar", Fraction(1, 3)), 2: ("3bar", Fraction(-2, 3)), 3: ("1", Fraction(1))}
RESID = {"1": Fraction(0), "3": Fraction(2, 3), "3bar": Fraction(1, 3)}


def corr_ok(col, q):
    return (q % 1) == RESID[col]


print("  correlation rule: 3 -> q = 2/3 (mod 1), 3bar -> q = 1/3 (mod 1), 1 -> q = 0 (mod 1)")
print("  paper's table:", ", ".join(f"N={n}:({PAPER[n][0]},{fstr(PAPER[n][1])})" for n in range(4)))
print(f"  {'q(N)':9s} {'rho':5s} | {'N=0':12s} {'N=1':12s} {'N=2':12s} {'N=3':12s} | (i) q=Y  (ii) =table  (iii) corr")
opt_results = []
for qname, qf in QF:
    for rho in ("3", "3bar"):
        tab = {n: (sector_colors[rho][str(n)], qf(n)) for n in range(4)}
        i_ = all(tab[n][1] == Y[n] for n in range(4))
        ii_ = all(tab[n] == PAPER[n] for n in range(4))
        iii_ = all(corr_ok(*tab[n]) for n in range(4))
        opt_results.append((qname, rho, tab, i_, ii_, iii_))
        cells = " ".join(f"{'(' + tab[n][0] + ',' + fstr(tab[n][1]) + ')':12s}" for n in range(4))
        print(f"  {qname:9s} {rho:5s} | {cells} | {str(i_):8s} {str(ii_):10s} {str(iii_)}")
any_Y = any(r[3] for r in opt_results)
any_table = any(r[4] for r in opt_results)
realizable = any(sector_colors[r]["1"] == "3bar" and sector_colors[r]["2"] == "3bar" for r in ("3", "3bar"))
print(f"  any option reproduces paper's Y on all four sectors: {any_Y}")
print(f"  any option reproduces paper's full (colour, charge) table: {any_table}")
print(f"  options satisfying the correlation: {sum(r[5] for r in opt_results)} of 8 ->",
      [f"q={r[0]}, rho={r[1]}" for r in opt_results if r[5]])
print(f"  some induced action makes N=1 and N=2 both 3bar: {realizable}")
print("  (note: (rho=3bar, q=N/3) is the SM assignment nu, dbar(3bar,+1/3), u(3,+2/3), e+ of Furey's S^u;")
print("   (rho=3, q=-N/3) is its conjugate S^d.)")

# =============================================================================
banner("C4. Paper's (colour, Y) pairs under the induced colours")
# =============================================================================
induced_pairs = {}
for rho in ("3", "3bar"):
    induced_pairs[rho] = {}
    for n in range(4):
        col = sector_colors[rho][str(n)]
        ok = corr_ok(col, Y[n])
        induced_pairs[rho][str(n)] = [col, fstr(Y[n]), bool(ok)]
    print(f"  rho = {rho:4s}: " + ", ".join(
        f"N={n}:({induced_pairs[rho][str(n)][0]},{induced_pairs[rho][str(n)][1]}) "
        f"{'pass' if induced_pairs[rho][str(n)][2] else 'FAIL'}" for n in range(4)))

# =============================================================================
banner("C5. Pulls z = (3/13 - x)/sigma_x against PDG 2024")
# =============================================================================
t = 3 / 13
Vud, sVud = 0.97367, 0.00032
Vus, sVus = 0.22431, 0.00085
Vk, sVk = 0.2250, 0.0004
lmb, slmb = 0.22501, 0.00068
ref = {}
ref["sin_vs_Vus_direct"] = (Vus, sVus)
ref["sin_vs_lambda_fit"] = (lmb, slmb)
x = Vus / Vud
ref["tan_vs_Vus_over_Vud_direct"] = (x, x * math.hypot(sVus / Vus, sVud / Vud))
x = Vk / Vud
ref["tan_vs_Kmu2_over_Vud"] = (x, x * math.hypot(sVk / Vk, sVud / Vud))
ref["tan_vs_fit"] = (lmb / math.sqrt(1 - lmb ** 2), slmb * (1 - lmb ** 2) ** -1.5)
zf = {k: (t - xv) / sv for k, (xv, sv) in ref.items()}

mpmath.mp.dps = 50
mf = mpmath.mpf
T_ = mf(3) / 13
mVud, msVud, mVus, msVus = mf("0.97367"), mf("0.00032"), mf("0.22431"), mf("0.00085")
mVk, msVk, mlam, mslam = mf("0.2250"), mf("0.0004"), mf("0.22501"), mf("0.00068")
mref = {
    "sin_vs_Vus_direct": (mVus, msVus),
    "sin_vs_lambda_fit": (mlam, mslam),
    "tan_vs_Vus_over_Vud_direct": (mVus / mVud, (mVus / mVud) * mpmath.sqrt((msVus / mVus) ** 2 + (msVud / mVud) ** 2)),
    "tan_vs_Kmu2_over_Vud": (mVk / mVud, (mVk / mVud) * mpmath.sqrt((msVk / mVk) ** 2 + (msVud / mVud) ** 2)),
    "tan_vs_fit": (mlam / mpmath.sqrt(1 - mlam ** 2), mslam * (1 - mlam ** 2) ** mf("-1.5")),
}
zm = {k: (T_ - xv) / sv for k, (xv, sv) in mref.items()}
print(f"  3/13 = {mpmath.nstr(T_, 15)}")
pulls = {}
for k in ref:
    pulls[k] = round(zf[k], 3)
    print(f"  {k:28s} x = {ref[k][0]:.8f} +- {ref[k][1]:.8f}  z = {zf[k]:+.6f}  -> {pulls[k]:+.3f}"
          f"   (mp50: {mpmath.nstr(zm[k], 12)})")
check("C5 double-precision and 50-digit pulls agree and round identically to 3 decimals",
      all(abs(zf[k] - float(zm[k])) < 1e-9 and round(zf[k], 3) == round(float(zm[k]), 3) for k in ref))

# =============================================================================
banner("C6. Csaszar 7-vertex torus: automorphisms and orientation (brute force over S_7)")
# =============================================================================
famA = [frozenset({i, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]   # {i, i+1, i+3}
famB = [frozenset({i, (i + 2) % 7, (i + 3) % 7}) for i in range(7)]   # {i, i+2, i+3}
faces = famA + famB
FACES = set(faces)
SETA, SETB = set(famA), set(famB)
check("14 distinct faces", len(FACES) == 14)
edge_count = {}
for f in faces:
    for p in itertools.combinations(sorted(f), 2):
        edge_count[p] = edge_count.get(p, 0) + 1
check("21 edges = all pairs of Z_7 (K_7), each in exactly two faces",
      len(edge_count) == 21 and all(cnt == 2 for cnt in edge_count.values()))


def link_is_cycle(v):
    ledges = [tuple(sorted(f - {v})) for f in faces if v in f]
    adj = {}
    for (p, q) in ledges:
        adj.setdefault(p, []).append(q)
        adj.setdefault(q, []).append(p)
    if len(adj) != 6 or any(len(nb) != 2 for nb in adj.values()):
        return False
    start = next(iter(adj))
    prev, cur, seen = None, start, 1
    while True:
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        prev, cur = cur, nxt
        if cur == start:
            break
        seen += 1
    return seen == 6


check("every vertex link is a single 6-cycle (closed surface); chi = 7 - 21 + 14 = 0",
      all(link_is_cycle(v) for v in range(7)) and 7 - 21 + 14 == 0)
check("each family is a Fano plane (every pair of Z_7 in exactly one triple of the family)",
      all(len({frozenset(p) for f in fam for p in itertools.combinations(f, 2)}) == 21 for fam in (famA, famB)))

FS = [tuple(sorted(f)) for f in faces]           # reference orientation: increasing order
EDGES = sorted(edge_count)
fidx = {f: j for j, f in enumerate(FS)}
eidx = {ed: j for j, ed in enumerate(EDGES)}
D2 = sp.zeros(21, 14)
for j, (a, b, c) in enumerate(FS):                 # d[a,b,c] = [b,c] - [a,c] + [a,b]
    D2[eidx[(b, c)], j] += 1
    D2[eidx[(a, c)], j] -= 1
    D2[eidx[(a, b)], j] += 1
D1 = sp.zeros(7, 21)
for j, (a, b) in enumerate(EDGES):
    D1[b, j] += 1
    D1[a, j] -= 1
ker2 = D2.nullspace()
r2, r1 = D2.rank(), D1.rank()
print(f"  rank d2 = {r2}, rank d1 = {r1}, dim ker d2 = {len(ker2)}, b1 = {21 - r1 - r2}")
check("d1 d2 = 0; H2 has rank 1; b1 = 2 (torus)", is_zero(D1 * D2) and len(ker2) == 1 and 21 - r1 - r2 == 2)
sv = ker2[0]
den = sp.ilcm(*[sp.fraction(x)[1] for x in sv])
sv = sv * den
g = sp.igcd(*[int(x) for x in sv])
sv = sv / g
if sv[0] < 0:
    sv = -sv
s_int = [int(x) for x in sv]
check("orientation class s in {+-1}^14 with d2 s = 0 over Z", set(s_int) <= {1, -1} and is_zero(D2 * sv))
print("  orientation class s (face in increasing order : sign):")
print("   ", ", ".join(f"{''.join(map(str, f))}:{'+' if s_int[j] > 0 else '-'}" for j, f in enumerate(FS)))


def sort_sign(seq):
    inv = sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq)) if seq[i] > seq[j])
    return -1 if inv % 2 else 1


def induced_chain_maps(p):
    S2 = sp.zeros(14, 14)
    for j, f in enumerate(FS):
        img = tuple(p[x] for x in f)
        S2[fidx[tuple(sorted(img))], j] = sort_sign(img)
    S1 = sp.zeros(21, 21)
    for j, ed in enumerate(EDGES):
        img = tuple(p[x] for x in ed)
        S1[eidx[tuple(sorted(img))], j] = sort_sign(img)
    return S1, S2


def orientation_sign(p):
    img_s = [0] * 14
    for j, f in enumerate(FS):
        im = tuple(p[x] for x in f)
        img_s[fidx[tuple(sorted(im))]] = sort_sign(im) * s_int[j]
    ratios = {img_s[j] * s_int[j] for j in range(14)}
    return ratios.pop() if len(ratios) == 1 else 0


auts, stabA = [], []
for p in itertools.permutations(range(7)):
    imgA = {frozenset(p[x] for x in f) for f in famA}
    imgB = {frozenset(p[x] for x in f) for f in famB}
    if imgA == SETA:
        stabA.append(p)
    if imgA | imgB == FACES:
        auts.append(p)
AGL = {tuple((a * x + b) % 7 for x in range(7)) for a in range(1, 7) for b in range(7)}
aut_order = len(auts)
equals_AGL = set(auts) == AGL
keeps = [p for p in auts if {frozenset(p[x] for x in f) for f in famA} == SETA
         and {frozenset(p[x] for x in f) for f in famB} == SETB]
swaps = [p for p in auts if {frozenset(p[x] for x in f) for f in famA} == SETB]
osigns = {p: orientation_sign(p) for p in auts}
n_pres = sum(1 for p in auts if osigns[p] == 1)
n_rev = sum(1 for p in auts if osigns[p] == -1)
chain_ok = True
for p in auts:
    S1m, S2m = induced_chain_maps(p)
    chain_ok &= meq(D2 * S2m, S1m * D2)
stab_cap = len(set(stabA) & set(auts))
print(f"  |Aut(face set)| = {aut_order}; equals AGL(1,7) = {{x -> a x + b}}: {equals_AGL} (|AGL(1,7)| = {len(AGL)})")
print(f"  automorphisms preserving each family: {len(keeps)}; swapping the two families: {len(swaps)}")
print(f"  multipliers a among family-preserving automorphisms: "
      f"{sorted({(p[1] - p[0]) % 7 for p in keeps})}; among family-swapping: {sorted({(p[1] - p[0]) % 7 for p in swaps})}")
print(f"  orientation: preserving {n_pres}, reversing {n_rev} (sigma_# s = +s / -s)")
print("  per automorphism x -> a x + b (family behaviour; sign of sigma_# s for b = 0..6):")
for a in range(1, 7):
    ps = [tuple((a * x + b) % 7 for x in range(7)) for b in range(7)]
    fam = "keeps families" if all(p in keeps for p in ps) else (
        "swaps families" if all(p in swaps for p in ps) else "mixed")
    sg = " ".join("+" if osigns.get(p) == 1 else ("-" if osigns.get(p) == -1 else "?") for p in ps)
    print(f"    a = {a}: {fam:14s}  orientation signs: {sg}")
print(f"  |Stab_S7(family {{i,i+1,i+3}})| = {len(stabA)};  |Stab cap Aut| = {stab_cap}")
check("every automorphism induces a chain map (d2 S2 = S1 d2) and maps s to +s or -s",
      chain_ok and all(osigns[p] in (1, -1) for p in auts))
check("keep-family + swap-family counts add up to |Aut|", len(keeps) + len(swaps) == aut_order)

# =============================================================================
banner("Summary of internal checks")
# =============================================================================
n_fail = sum(1 for _, c in CHECKS if not c)
print(f"  {len(CHECKS)} checks, {n_fail} failed")

results = {
    "sector_colors": sector_colors,
    "additive": bool(additive),
    "any_option_reproduces_paper_Y": bool(any_Y),
    "any_option_reproduces_paper_table": bool(any_table),
    "paper_labels_realizable": bool(realizable),
    "induced_pairs": induced_pairs,
    "pulls": pulls,
    "aut_order": int(aut_order),
    "equals_AGL17": bool(equals_AGL),
    "keeps_each_family": int(len(keeps)),
    "orientation_preserving": int(n_pres),
    "orientation_reversing": int(n_rev),
    "stab_S7_family_plus": int(len(stabA)),
    "stab_cap_aut": int(stab_cap),
    "method_C1": ("complex octonions C(x)O (table e_i e_{i+1}=e_{i+3}), Furey alpha_i as 8x8 left-multiplication "
                  "matrices, vacuum (omega omega^dag)1=(1+i e7)/2, Fock states = minimal left ideal; "
                  "T^a=sum alpha_i^dag M^a_ij alpha_j; colour by cubic Casimir (+10/9 -> 3, -10/9 -> 3bar) "
                  "and (T3,T8) weights; exact sympy; no Kronecker/Jordan-Wigner"),
}
with open(os.path.join(HERE, "leg2_results.json"), "w") as fh:
    json.dump(results, fh, indent=2)
    fh.write("\n")
print("\nleg2_results.json written:")
print(json.dumps(results, indent=2))
sys.exit(1 if n_fail else 0)
