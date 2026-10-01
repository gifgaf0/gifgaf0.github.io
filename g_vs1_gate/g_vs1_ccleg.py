#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
g_vs1_ccleg.py -- Gate G-VS1, the CC-leg instrument.

Built blind from the locked memo (staging_memo_G_VS1_v2.md) and the lock record's Addendum A-2
(G_VS1_LOCK_RECORD.md section 2); no chat code consulted. Exact arithmetic throughout: fractions
over Q for every reported number, GF(p) for the kernel upper bounds (two primes below 2^20), exact
Laurent polynomials for the Weyl cross-check. Class codes only.

Usage:
    python3 g_vs1_ccleg.py preread   -> Phase 0 only; writes g_vs1_ccleg_prereadcheckpoint.json
    python3 g_vs1_ccleg.py run       -> Phases 0-3 + the class code; writes g_vs1_ccleg_checkpoint.json

Every invocation md5-guards (md5 + bytes) the memo, the lock record, the T1 list, the scanner, the
extract, the schema and the comparator, then T1-scans itself, the memo, the lock record, the extract,
the schema and the comparator under the gate list (31 patterns) and halts on any hit, no override.
The checkpoint is T1-scanned after writing and deleted on a hit.
"""
import sys, os, json, hashlib, time, datetime, itertools, importlib.util, random
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
def P(*a): return os.path.join(HERE, *a)

MEMO = 'staging_memo_G_VS1_v2.md'; LOCK = 'G_VS1_LOCK_RECORD.md'
T1LIST = 'tools/t1/T1_forbidden_G_VS1.txt'; SCANNER = 'tools/t1/t1_scan.py'
EXTRACT = 'inputs/paper_II_3_4_4_and_3_4_7_extract.md'
SCHEMA = 'g_vs1_schema_v1_0.json'; COMPARATOR = 'g_vs1_compare_v1_0.py'
GUARDS = {
    MEMO: ('58fd02671ea77db63e22afdcc5ee93a0', 44709),
    LOCK: ('71711946d1c4abb06fa17402e8d5a6c9', 23071),
    T1LIST: ('324f577d20e2bfba3b594d96c4ca3ba7', 576),
    SCANNER: ('6b86290090a8c84f1b1a0a99ec0bf697', 1967),
    EXTRACT: ('940b0bee4b2112e911ae738c3db2bc3d', 12912),
    SCHEMA: ('4690e07d5a22cc7a1c5d08db39eda3fe', 6253),
    COMPARATOR: ('69011375d28ec8f63f3ac76383e98321', 9236),
}
T1_PATTERNS_EXPECTED = 31
PRIMES = [1048573, 1000037]          # both prime, both = 1 mod 4 (so that -1 is a square), both < 2^20
ELECTIONS = {'E-VS-%d' % i: 'a' for i in range(1, 11)}
READINGS = {
    'Q-VS-1': 'The carrier is not settled (not the K₇ vertices). F-b is not live.',
    'Q-VS-2': 'Confirmed: total density.',
    'Q-VS-3': 'Confirmed: π₁ phase winding.',
    'Q-VS-4': 'Confirmed: Time reversal (complex conjugation) is a symmetry.',
    'Q-VS-5': "Confirmed: The definition of 'strictly forces' stands.",
}
OCTONION_CONVENTION = ('Fano lines {i, i+1, i+3} mod 7 on e1..e7: (1,2,4) (2,3,5) (3,4,6) (4,5,7) (5,6,1) (6,7,2) (7,1,3); '
                       'e_i e_j = e_k for (i,j,k) a line in cyclic order, e_j e_i = -e_k, e_i^2 = -e_0')
STRATA = ['R', 'P7', 'F7', 'I7', 'MP+', 'MP-', 'MP0', 'MF', 'MI+', 'MI-', 'MI0']
BASIS2 = ['rho0', 'N']
BASIS4 = ['rho0^2', 'rho0 N', 'N^2', '|S|^2', 'Re(psi0^2 Sbar)']      # the T-even degree-4 basis (A-2.4 / A-2.8)
T_ODD4 = 'Q'                                                           # Q = psi0^2 Sbar - psibar0^2 S

def halt(msg, code=2):
    print('HALT:', msg); sys.exit(code)

def fs(x):
    """exact number -> JSON value: integers as JSON ints, other rationals as reduced-fraction strings"""
    x = Fr(x)
    return int(x) if x.denominator == 1 else str(x)

def fstr(x):
    """exact number -> string of a reduced fraction or integer (for lists of exact coordinates)"""
    x = Fr(x); return str(x.numerator) if x.denominator == 1 else str(x)

# ----------------------------------------------------------------------------------------------
# 0. guards and T1
# ----------------------------------------------------------------------------------------------
def md5_of(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

def guard_all():
    out = {}
    for rel, (want, nbytes) in GUARDS.items():
        p = P(rel)
        if not os.path.exists(p): halt('missing guarded file ' + rel)
        got = md5_of(p); n = os.path.getsize(p)
        if got != want or n != nbytes:
            halt('md5/bytes mismatch on %s: %s (%d B) vs expected %s (%d B)' % (rel, got, n, want, nbytes))
        out[rel] = (got, n)
    return out

def load_scanner():
    spec = importlib.util.spec_from_file_location('t1_scan', P(SCANNER))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    pats = mod.load(P(T1LIST))
    if len(pats) != T1_PATTERNS_EXPECTED: halt('T1 list has %d patterns, expected %d' % (len(pats), T1_PATTERNS_EXPECTED))
    return mod, pats

def t1_scan_files(mod, pats, paths):
    res = {}
    for label, p in paths:
        text = open(p, 'rb').read().decode('utf-8', 'replace')
        hits, coll = mod.scan_text(text, pats)
        res[label] = {'hits': sorted(set(i for i, _ in hits)), 'numeric_collisions': len(coll)}
        if hits: halt('T1 hit in %s at pattern indices %s' % (label, sorted(set(i for i, _ in hits))), 3)
    return res

# ----------------------------------------------------------------------------------------------
# 1. exact linear algebra over Q
# ----------------------------------------------------------------------------------------------
def rref_Q(rows, ncols):
    M = [[Fr(x) for x in r] for r in rows if any(x != 0 for x in r)]
    piv = []; r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, len(M)):
            if M[i][c] != 0: pr = i; break
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; Mr = M[r]
                M[i] = [a - f * b for a, b in zip(M[i], Mr)]
        piv.append(c); r += 1
        if r == len(M): break
    return piv, M[:r]

def rank_Q(rows, ncols):
    return len(rref_Q(rows, ncols)[0])

def nullspace_Q(rows, ncols):
    piv, R = rref_Q(rows, ncols)
    pivset = set(piv)
    basis = []
    for f in range(ncols):
        if f in pivset: continue
        v = [Fr(0)] * ncols; v[f] = Fr(1)
        for i, pc in enumerate(piv): v[pc] = -R[i][f]
        basis.append(v)
    return basis

def in_span(vec, rref_rows, piv):
    """reduce vec against an RREF basis; True iff the remainder is zero"""
    v = [Fr(x) for x in vec]
    for i, pc in enumerate(piv):
        if v[pc] != 0:
            f = v[pc]; v = [a - f * b for a, b in zip(v, rref_rows[i])]
    return all(x == 0 for x in v)

def to_integer_vector(v):
    den = 1
    for x in v: den = den * x.denominator // gcd(den, x.denominator)
    w = [int(x * den) for x in v]
    g = 0
    for x in w: g = gcd(g, abs(x))
    return [x // g for x in w] if g else w

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def matmul(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]
def matvec(A, v): return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]
def transpose(A): return [list(r) for r in zip(*A)]
def bracket(A, B):
    AB, BA = matmul(A, B), matmul(B, A)
    return [[AB[i][j] - BA[i][j] for j in range(len(A))] for i in range(len(A))]
def zeros(n, m=None): return [[Fr(0)] * (m if m else n) for _ in range(n)]
def flat(A): return [x for r in A for x in r]
def trace(A): return sum(A[i][i] for i in range(len(A)))
def is_antisym(A): return all(A[i][j] == -A[j][i] for i in range(len(A)) for j in range(len(A)))

# ----------------------------------------------------------------------------------------------
# 2. octonions (the Fano-line convention of A-2.3) and the derivation algebra g2
# ----------------------------------------------------------------------------------------------
LINES = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7), (5, 6, 1), (6, 7, 2), (7, 1, 3)]
def build_mul():
    M = [[None] * 8 for _ in range(8)]
    for i in range(8): M[0][i] = (1, i); M[i][0] = (1, i)
    for i in range(1, 8): M[i][i] = (-1, 0)
    for (a, b, c) in LINES:
        for (i, j, k) in ((a, b, c), (b, c, a), (c, a, b)):
            if M[i][j] is not None or M[j][i] is not None: halt('Fano table conflict at (%d,%d)' % (i, j))
            M[i][j] = (1, k); M[j][i] = (-1, k)
    for i in range(8):
        for j in range(8):
            if M[i][j] is None: halt('Fano table incomplete at (%d,%d)' % (i, j))
    return M
MUL = build_mul()

def omul(x, y):
    """product of two octonions given as 8-vectors over any commutative ring with 0, +, *, unary -"""
    z = [0] * 8
    for i in range(8):
        xi = x[i]
        if xi == 0: continue
        for j in range(8):
            yj = y[j]
            if yj == 0: continue
            s, k = MUL[i][j]
            z[k] = z[k] + (xi * yj if s > 0 else -(xi * yj))
    return z

def basis_vec(k, n=8):
    v = [Fr(0)] * n; v[k] = Fr(1); return v
E = [basis_vec(k) for k in range(8)]

def derivation_conditions():
    """rows of the linear system on a general 8x8 matrix D (unknown index 8*j+k = D_jk = coefficient of e_j in D(e_k)):
    D(e_a e_b) - D(e_a) e_b - e_a D(e_b) = 0 for all 64 basis pairs, 8 components each."""
    rows = []
    for a in range(8):
        for b in range(8):
            s, c = MUL[a][b]
            eq = [[Fr(0)] * 64 for _ in range(8)]
            for j in range(8):
                eq[j][8 * j + c] += s                     # D(e_a e_b) = s D(e_c), component j
                sj, kj = MUL[j][b]; eq[kj][8 * j + a] -= sj  # D(e_a) e_b = sum_j D_ja e_j e_b
                sa, ka = MUL[a][j]; eq[ka][8 * j + b] -= sa  # e_a D(e_b) = sum_j D_jb e_a e_j
            rows.extend(eq)
    return rows

def is_derivation(D):
    for a in range(8):
        for b in range(8):
            lhs = matvec(D, omul(E[a], E[b]))
            rhs = [p + q for p, q in zip(omul(matvec(D, E[a]), E[b]), omul(E[a], matvec(D, E[b])))]
            if lhs != rhs: return False
    return True

def compute_g2():
    rows = derivation_conditions()
    ns = nullspace_Q(rows, 64)
    basis = []
    for v in ns:
        w = to_integer_vector(v)
        basis.append([[Fr(w[8 * j + k]) for k in range(8)] for j in range(8)])
    return basis, 64 - len(ns)

def lie_rank(basis):
    """rank of the Lie algebra = minimal nullity of ad(X) over a few deterministic generic elements"""
    n = len(basis)
    best = None
    for seed in (1, 2, 3):
        coeffs = [Fr((seed * (i + 1) ** 2 + 3 * i + 1) % 17 + 1) for i in range(n)]
        X = zeros(8)
        for c, B in zip(coeffs, basis):
            for i in range(8):
                for j in range(8): X[i][j] += c * B[i][j]
        rows = [flat(bracket(X, B)) for B in basis]
        nullity = n - rank_Q(rows, 64)
        best = nullity if best is None else min(best, nullity)
    return best

def subalgebra_coeffs_to_mats(basis, coeff_vectors):
    out = []
    for c in coeff_vectors:
        M = zeros(8)
        for ci, B in zip(c, basis):
            if ci == 0: continue
            for i in range(8):
                for j in range(8): M[i][j] += ci * B[i][j]
        out.append(M)
    return out

def stabilizer_pointwise(basis, vectors):
    """{D in span(basis): D v = 0 for all v in vectors} -> list of coefficient vectors (over the basis)"""
    n = len(basis)
    rows = []
    for v in vectors:
        imgs = [matvec(B, v) for B in basis]
        for comp in range(8): rows.append([imgs[i][comp] for i in range(n)])
    return nullspace_Q(rows, n)

def stabilizer_setwise(basis, span_indices):
    """{D in span(basis): D(span) subset span} where span = span of e_i, i in span_indices"""
    n = len(basis); outside = [i for i in range(8) if i not in span_indices]
    rows = []
    for idx in span_indices:
        imgs = [matvec(B, E[idx]) for B in basis]
        for comp in outside: rows.append([imgs[i][comp] for i in range(n)])
    return nullspace_Q(rows, n)

def centralizer_in(sub_mats, within_mats):
    """{A in span(within): [A, B] = 0 for all B in sub} -> matrices"""
    n = len(within_mats); rows = []
    for B in sub_mats:
        brs = [flat(bracket(W, B)) for W in within_mats]
        for comp in range(64): rows.append([brs[i][comp] for i in range(n)])
    ns = nullspace_Q(rows, n)
    return subalgebra_coeffs_to_mats(within_mats, ns)

def dynkin_index(k_mats):
    """A-2.5(0a): 2 tr_7(A^2) / tr_{ad_k}(ad_k(A)^2) for a nonzero A in k (k a 3-dim simple subalgebra)"""
    A = k_mats[0]
    tr7 = trace(matmul(A, A))
    # ad_k(A) in the basis k_mats: solve [A, B_j] = sum_i c_ij B_i exactly
    n = len(k_mats)
    cols = [flat(B) for B in k_mats]
    C = zeros(n)
    for j, B in enumerate(k_mats):
        target = flat(bracket(A, B))
        # solve sum_i c_i cols[i] = target
        rows = [[cols[i][t] for i in range(n)] + [target[t]] for t in range(64)]
        piv, R = rref_Q(rows, n + 1)
        if n in piv: halt('ad_k(A) does not close in k')
        sol = [Fr(0)] * n
        for i, pc in enumerate(piv): sol[pc] = R[i][n]
        for i in range(n): C[i][j] = sol[i]
    trad = trace(matmul(C, C))
    if trad == 0: halt('degenerate ad-trace in the index computation')
    return 2 * tr7 / trad

def orbit_rank(basis, vectors):
    """rank of the g2-orbit map at the tuple of real vectors: span of (D v_1, ..., D v_m) over D in the basis"""
    rows = []
    for B in basis:
        row = []
        for v in vectors: row.extend(matvec(B, v))
        rows.append(row)
    return rank_Q(rows, 8 * len(vectors))

def commutant_dim(basis, dim):
    """{M dim x dim : [M, D|_dim] = 0 for all D in basis}; dim = 7 (indices 1..7) or 8"""
    idx = list(range(8 - dim, 8))
    n = dim * dim; rows = []
    for B in basis:
        Bs = [[B[i][j] for j in idx] for i in idx]
        # [M, Bs] = M Bs - Bs M : linear in M entries m_{ab} (index a*dim+b)
        for i in range(dim):
            for j in range(dim):
                row = [Fr(0)] * n
                for t in range(dim):
                    row[i * dim + t] += Bs[t][j]      # (M Bs)_ij = sum_t m_it Bs_tj
                    row[t * dim + j] -= Bs[i][t]      # (Bs M)_ij = sum_t Bs_it m_tj
                rows.append(row)
    return n - rank_Q(rows, n)

# ----------------------------------------------------------------------------------------------
# 3. polynomials over Q in the 16 variables psi_0..psi_7 (0..7), psibar_0..psibar_7 (8..15)
# ----------------------------------------------------------------------------------------------
NV = 16
def pvar(k):
    e = [0] * NV; e[k] = 1; return {tuple(e): Fr(1)}
def padd(a, b):
    out = dict(a)
    for e, c in b.items():
        v = out.get(e, 0) + c
        if v: out[e] = v
        else: out.pop(e, None)
    return out
def pscale(a, s):
    return {e: c * s for e, c in a.items()} if s != 0 else {}
def pneg(a): return pscale(a, -1)
def psub(a, b): return padd(a, pneg(b))
def pmul(a, b):
    out = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            v = out.get(e, 0) + c1 * c2
            if v: out[e] = v
            else: out.pop(e, None)
    return out
def pconj(a):
    """complex conjugation of a polynomial function: swap psi_k <-> psibar_k (coefficients are rational)"""
    return {tuple(e[8:] + e[:8]): c for e, c in a.items()}
def ppow(a, n):
    out = {tuple([0] * NV): Fr(1)}
    for _ in range(n): out = pmul(out, a)
    return out
def act_Q(A, poly, nz=None):
    """the vector field sum_{jk} A_jk x_k d/dx_j (A a 16x16 matrix over Q) applied to poly"""
    if nz is None: nz = [[(k, A[j][k]) for k in range(NV) if A[j][k] != 0] for j in range(NV)]
    out = {}
    for ex, c in poly.items():
        for j in range(NV):
            ej = ex[j]
            if ej == 0: continue
            for k, a in nz[j]:
                ne = list(ex); ne[j] -= 1; ne[k] += 1; ne = tuple(ne)
                v = out.get(ne, 0) + c * ej * a
                if v: out[ne] = v
                else: out.pop(ne, None)
    return out
def pbidegree(poly):
    degs = set((sum(e[:8]), sum(e[8:])) for e in poly)
    return degs
def t_parity(poly):
    c = pconj(poly)
    if c == poly: return 1
    if c == pneg(poly): return -1
    return 0
def uses_singlet(poly):
    return any(e[0] != 0 or e[8] != 0 for e in poly)

def blockdiag16(Dpsi, Dpsibar):
    A = [[Fr(0)] * NV for _ in range(NV)]
    for i in range(8):
        for j in range(8):
            A[i][j] = Fr(Dpsi[i][j]); A[8 + i][8 + j] = Fr(Dpsibar[i][j])
    return A
def gen_same(D): return blockdiag16(D, D)                       # g2, so(7), su(3): the same real matrix on psi and psibar
def gen_u8(j, k):                                                # the complexified u(8): E_jk on psi, -E_jk^T on psibar
    Ejk = zeros(8); Ejk[j][k] = Fr(1)
    mEt = zeros(8); mEt[k][j] = Fr(-1)
    return blockdiag16(Ejk, mEt)
def so7_generators():
    out = []
    for a in range(1, 8):
        for b in range(a + 1, 8):
            R = zeros(8); R[b][a] = Fr(1); R[a][b] = Fr(-1)      # R e_a = e_b, R e_b = -e_a
            out.append(R)
    return out

# the named invariants
PSI = [pvar(k) for k in range(8)]; PSIB = [pvar(8 + k) for k in range(8)]
def inv_rho0(): return pmul(PSI[0], PSIB[0])
def inv_N(rng=range(1, 8)):
    out = {}
    for a in rng: out = padd(out, pmul(PSI[a], PSIB[a]))
    return out
def inv_S():
    out = {}
    for a in range(1, 8): out = padd(out, pmul(PSI[a], PSI[a]))
    return out
def inv_Sbar(): return pconj(inv_S())
def inv_absS2(): return pmul(inv_S(), inv_Sbar())
def inv_Re_psi0sq_Sbar():
    a = pmul(pmul(PSI[0], PSI[0]), inv_Sbar())
    return pscale(padd(a, pconj(a)), Fr(1, 2))
def inv_Q():
    a = pmul(pmul(PSI[0], PSI[0]), inv_Sbar())
    return psub(a, pconj(a))
def inv_Ntot(): return padd(inv_rho0(), inv_N())

def candidates(space, algebra, deg):
    """A-2.4: the explicit candidate invariants per algebra and degree (names -> polynomials)"""
    rho0, N = inv_rho0(), inv_N()
    if algebra == 'U8':
        return {'N_tot': inv_Ntot()} if deg == 2 else {'N_tot^2': ppow(inv_Ntot(), 2)}
    if algebra == 'SU3xU1':
        n7 = pmul(PSI[7], PSIB[7])
        return {'rho0': rho0, 'psi7 psibar7': n7, 'N - psi7 psibar7': psub(N, n7)}
    if algebra == 'SU3xU1_full':
        n7 = pmul(PSI[7], PSIB[7])
        x07 = pmul(PSI[0], PSIB[7]); x70 = pmul(PSI[7], PSIB[0])
        omega = {}
        for (a, b) in ((1, 3), (4, 5), (2, 6)):     # the Kaehler form of the complex structure J = L_{e7} on e7-perp
            omega = padd(omega, psub(pmul(PSI[a], PSIB[b]), pmul(PSI[b], PSIB[a])))
        return {'rho0': rho0, 'psi7 psibar7': n7, 'N - psi7 psibar7': psub(N, n7),
                'Re(psi0 psibar7)': pscale(padd(x07, x70), Fr(1, 2)), 'psi0 psibar7 - psi7 psibar0': psub(x07, x70), 'omega_J(psi, psibar)': omega}
    if space == 'R16':
        if deg == 2: return {'rho0': rho0, 'N': N}
        if deg == 4: return {'rho0^2': pmul(rho0, rho0), 'rho0 N': pmul(rho0, N), 'N^2': pmul(N, N),
                             '|S|^2': inv_absS2(), 'Re(psi0^2 Sbar)': inv_Re_psi0sq_Sbar(), T_ODD4: inv_Q()}
    else:
        if deg == 2: return {'N': N}
        if deg == 4: return {'N^2': pmul(N, N), '|S|^2': inv_absS2()}
        if deg == 6: return {'N^3': ppow(N, 3), 'N |S|^2': pmul(N, inv_absS2())}
    halt('no candidates for %s %s %d' % (space, algebra, deg))

# ----------------------------------------------------------------------------------------------
# 4. GF(p) machinery: weight coordinates, monomial actions, incremental elimination
# ----------------------------------------------------------------------------------------------
def modinv(a, p): return pow(a % p, p - 2, p)
def sqrt_minus1(p):
    for a in range(2, p):
        r = pow(a, (p - 1) // 4, p)
        if (r * r) % p == p - 1: return r
    halt('no square root of -1 mod %d' % p)
def mat_inv_mod(M, p):
    n = len(M); A = [[x % p for x in row] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        pr = next((i for i in range(c, n) if A[i][c]), None)
        if pr is None: halt('singular matrix mod p')
        A[c], A[pr] = A[pr], A[c]
        inv = modinv(A[c][c], p); A[c] = [(x * inv) % p for x in A[c]]
        for i in range(n):
            if i != c and A[i][c]:
                f = A[i][c]; A[i] = [(x - f * y) % p for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]
def mat_mul_mod(A, B, p):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) % p for j in range(len(B[0]))] for i in range(len(A))]
def frac_mod(x, p): return (x.numerator * modinv(x.denominator, p)) % p
def rank_mod(vectors, p):
    """rank over GF(p) of a list of integer vectors (dense elimination; small systems only)"""
    M = [[x % p for x in v] for v in vectors if any(x % p for x in v)]
    rank = 0; ncols = len(vectors[0]) if vectors else 0
    for c in range(ncols):
        pr = next((i for i in range(rank, len(M)) if M[i][c]), None)
        if pr is None: continue
        M[rank], M[pr] = M[pr], M[rank]
        inv = modinv(M[rank][c], p); M[rank] = [(x * inv) % p for x in M[rank]]
        for i in range(len(M)):
            if i != rank and M[i][c]:
                f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[rank])]
        rank += 1
        if rank == len(M): break
    return rank

def cartan_pair(g2_basis):
    """h1, h2: a basis of the 2-dim space {a R13 + b R45 + c R26} intersect g2 (the torus of su(3) = Stab(e7)),
    R_ab the rotation generator e_a -> e_b in the plane paired to e7 by the multiplication table."""
    planes = [(1, 3), (4, 5), (2, 6)]
    Rs = []
    for a, b in planes:
        R = zeros(8); R[b][a] = Fr(1); R[a][b] = Fr(-1); Rs.append(R)
    # express the derivation condition on a R1 + b R2 + c R3
    rows = derivation_conditions()
    cols = [flat(R) for R in Rs]
    sys_rows = [[sum(r[t] * cols[i][t] for t in range(64)) for i in range(3)] for r in rows]
    ns = nullspace_Q(sys_rows, 3)
    if len(ns) != 2: halt('Cartan search: expected a 2-dim torus in the three e7-planes, found %d' % len(ns))
    hs = []
    for v in ns:
        w = to_integer_vector(v)
        H = zeros(8)
        for ci, R in zip(w, Rs):
            for i in range(8):
                for j in range(8): H[i][j] += ci * R[i][j]
        if not is_derivation(H): halt('Cartan element is not a derivation')
        hs.append(H)
    return hs, planes

def weight_change_of_basis(planes, p):
    """C (8x8 over GF(p)): new coordinates zeta = C psi with zeta_{a,+-} = psi_a +- i psi_b on each plane (a,b),
    psi_0 and psi_7 unchanged; returned with its inverse."""
    r = sqrt_minus1(p)
    C = [[0] * 8 for _ in range(8)]
    C[0][0] = 1; C[7][7] = 1
    for (a, b) in planes:
        C[a][a] = 1; C[a][b] = r           # zeta_{a+} = psi_a + i psi_b  (stored at index a)
        C[b][a] = 1; C[b][b] = (-r) % p    # zeta_{a-} = psi_a - i psi_b  (stored at index b)
    return C, mat_inv_mod(C, p)

def conj16(A16, C, Cinv, p):
    """A16 a 16x16 matrix over Q -> C16 A C16^{-1} over GF(p), C16 = blockdiag(C, C)"""
    Am = [[frac_mod(Fr(x), p) for x in row] for row in A16]
    C16 = [[0] * 16 for _ in range(16)]; Ci16 = [[0] * 16 for _ in range(16)]
    for i in range(8):
        for j in range(8):
            C16[i][j] = C[i][j]; C16[8 + i][8 + j] = C[i][j]
            Ci16[i][j] = Cinv[i][j]; Ci16[8 + i][8 + j] = Cinv[i][j]
    return mat_mul_mod(mat_mul_mod(C16, Am, p), Ci16, p)

def signed(x, p): return x - p if x > p // 2 else x

def variable_weights(h_tilde_list, p, r):
    """weights of the 16 zeta-variables: the diagonal of each conjugated Cartan element divided by i"""
    W = []
    for j in range(16):
        w = []
        for Ht in h_tilde_list:
            for k in range(16):
                if k != j and Ht[j][k] % p: halt('Cartan element not diagonal in weight coordinates')
            w.append(signed((Ht[j][j] * modinv(r, p)) % p, p))
        W.append(tuple(w))
    return W

def monomials(active, deg_half):
    """exponent tuples over 16 variables of bidegree (deg_half, deg_half): deg_half among the active psi-block variables
    (indices < 8) and deg_half among the active psibar-block variables (indices >= 8)"""
    a1 = [i for i in active if i < 8]; a2 = [i for i in active if i >= 8]
    def combos(idx, d):
        out = []
        for comb in itertools.combinations_with_replacement(idx, d):
            e = [0] * NV
            for i in comb: e[i] += 1
            out.append(e)
        return out
    out = []
    for e1 in combos(a1, deg_half):
        for e2 in combos(a2, deg_half):
            out.append(tuple(x + y for x, y in zip(e1, e2)))
    return out

def act_mod(Anz, ex, p):
    """vector field with GF(p) matrix given as per-row nonzero lists; returns dict exps->coeff"""
    out = {}
    for j in range(NV):
        ej = ex[j]
        if ej == 0: continue
        for k, a in Anz[j]:
            ne = list(ex); ne[j] -= 1; ne[k] += 1; ne = tuple(ne)
            v = (out.get(ne, 0) + ej * a) % p
            if v: out[ne] = v
            else: out.pop(ne, None)
    return out

def gf_upper_bound(gens16, active, deg_half, p, lower_bound, planes, hs, weights):
    """nullity over GF(p) of the stacked generator action on the bidegree (d/2,d/2) monomials, computed on the
    weight-zero monomials in zeta-coordinates (the common kernel lies in the kernel of the Cartan elements, i.e. in
    the weight-zero subspace); rows are added generator by generator, and the elimination stops early once the
    nullity equals the exact lower bound (further rows cannot lower it below the true dimension). Returns a dict."""
    r = sqrt_minus1(p)
    C, Cinv = weight_change_of_basis(planes, p)
    if variable_weights([conj16(gen_same(H), C, Cinv, p) for H in hs], p, r) != weights: halt('weights differ mod %d' % p)
    # the common kernel lies in the weight-zero space only if h1, h2 are GF(p)-combinations of the generators: check it
    gvecs = [[frac_mod(Fr(x), p) for x in flat(G)] for G in gens16]
    hvecs = [[frac_mod(Fr(x), p) for x in flat(gen_same(H))] for H in hs]
    if rank_mod(gvecs + hvecs, p) != rank_mod(gvecs, p): halt('Cartan elements not in the generator span mod %d' % p)
    mons = monomials(active, deg_half)
    W0 = [m for m in mons if all(sum(e * w[t] for e, w in zip(m, weights)) == 0 for t in range(len(weights[0])))]
    col = {m: i for i, m in enumerate(W0)}
    ncols = len(W0)
    pivots = {}; rank = 0; rows_done = 0; gens_done = 0
    for G in gens16:
        Gt = conj16(G, C, Cinv, p)
        Anz = [[(k, Gt[j][k]) for k in range(NV) if Gt[j][k]] for j in range(NV)]
        rows = {}
        for m in W0:
            img = act_mod(Anz, m, p)
            for m2, cval in img.items():
                rows.setdefault(m2, {})[col[m]] = cval
        for row in rows.values():
            row = dict(row); rows_done += 1
            while row:
                c = min(row)
                if c in pivots:
                    f = row[c]
                    for cc, v in pivots[c].items():
                        nv = (row.get(cc, 0) - f * v) % p
                        if nv: row[cc] = nv
                        else: row.pop(cc, None)
                else:
                    inv = modinv(row[c], p)
                    pivots[c] = {cc: (v * inv) % p for cc, v in row.items()}
                    rank += 1; break
        gens_done += 1
        if ncols - rank <= lower_bound: break
    return {'p': p, 'nullity': ncols - rank, 'weight_zero_monomials': ncols, 'n_monomials': len(mons),
            'rows_processed': rows_done, 'generators_processed': gens_done, 'generators_total': len(gens16)}

def certify(name, gens16, active, deg, cands, planes, hs, weights, primes=PRIMES):
    """A-2.4 certificate: lower bound = rank over Q of the explicitly annihilated candidates; upper bound = GF(p)
    nullity for each prime; certified iff min(upper) == lower."""
    nz_list = [[[(k, G[j][k]) for k in range(NV) if G[j][k] != 0] for j in range(NV)] for G in gens16]
    annihilated = []; parities = {}; singlet = {}
    for cname, poly in cands.items():
        degs = pbidegree(poly)
        if degs != {(deg // 2, deg // 2)}: halt('candidate %s is not of bidegree (%d,%d)' % (cname, deg // 2, deg // 2))
        ok = all(not act_Q(G, poly, nz) for G, nz in zip(gens16, nz_list))
        if ok: annihilated.append(cname)
        parities[cname] = t_parity(poly); singlet[cname] = uses_singlet(poly)
    # rank over Q of the annihilated candidates
    mons = sorted(set(e for cname in annihilated for e in cands[cname]))
    idx = {e: i for i, e in enumerate(mons)}
    rows = []
    for cname in annihilated:
        row = [Fr(0)] * len(mons)
        for e, c in cands[cname].items(): row[idx[e]] = c
        rows.append(row)
    lower = rank_Q(rows, len(mons)) if rows else 0
    uppers = {}
    for p in primes:
        uppers[str(p)] = gf_upper_bound(gens16, active, deg // 2, p, lower, planes, hs, weights)
    upper_min = min(u['nullity'] for u in uppers.values())
    certified = (upper_min == lower)
    T_even = None
    if certified:
        if len(annihilated) != lower: halt('%s: annihilated candidates are linearly dependent (%d vs rank %d)' % (name, len(annihilated), lower))
        T_even = sum(1 for c in annihilated if parities[c] == 1)
        te_rows = [rows[i] for i, c in enumerate(annihilated) if parities[c] == 1]
        if te_rows and rank_Q(te_rows, len(mons)) != T_even: halt('%s: T-even count differs from the T-even rank' % name)
    return {'name': name, 'degree': deg, 'bidegree': [deg // 2, deg // 2], 'n_monomials': uppers[str(primes[0])]['n_monomials'],
            'explicit_annihilated': annihilated, 'explicit_not_annihilated': [c for c in cands if c not in annihilated],
            'lower_bound_rank_Q': lower, 'upper_bounds_mod_p': {k: v['nullity'] for k, v in uppers.items()},
            'upper_bound_detail': uppers, 'certified_dim': lower if certified else None, 'certificate_met': certified,
            'T_even_dim': T_even, 'T_parity': parities, 'singlet_blind': singlet}

# ----------------------------------------------------------------------------------------------
# 5. the Weyl integration cross-check (exact Laurent polynomials)
# ----------------------------------------------------------------------------------------------
def lmul(a, b):
    out = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            v = out.get(e, 0) + c1 * c2
            if v: out[e] = v
            else: out.pop(e, None)
    return out
def weyl_invariant_dim(weights, roots, order_W, d):
    """dim V^G = (1/|W|) CT[ chi_{Sym^d V} prod_{alpha in roots} (1 - e^alpha) ]; chi by Newton's recursion"""
    n = len(weights[0]); zero = tuple([0] * n)
    def pk(k):
        out = {}
        for w in weights:
            e = tuple(k * x for x in w); out[e] = out.get(e, 0) + 1
        return {e: Fr(c) for e, c in out.items()}
    h = [{zero: Fr(1)}]
    for dd in range(1, d + 1):
        acc = {}
        for k in range(1, dd + 1):
            for e, c in lmul(pk(k), h[dd - k]).items():
                v = acc.get(e, 0) + c
                if v: acc[e] = v
                else: acc.pop(e, None)
        h.append({e: c / dd for e, c in acc.items()})
    R = {zero: Fr(1)}
    for al in roots: R = lmul(R, {zero: Fr(1), tuple(al): Fr(-1)})
    ct = sum(c * h[d].get(tuple(-x for x in e), 0) for e, c in R.items())
    val = ct / order_W
    if val.denominator != 1: halt('Weyl integral is not an integer: %s' % val)
    return int(val)

def weights_with_u1(weights_int, with_singlet):
    ws = list(weights_int) + ([tuple([0] * len(weights_int[0]))] if with_singlet else [])
    return [tuple(list(w) + [1]) for w in ws] + [tuple(list(w) + [-1]) for w in ws]
def roots_with_u1(roots): return [tuple(list(a) + [0]) for a in roots]
G2_W7 = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]
G2_ROOTS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (2, 1), (-2, -1), (1, 2), (-1, -2)]
B3_W7 = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
def b3_roots():
    out = []
    for i in range(3):
        for j in range(i + 1, 3):
            for si in (1, -1):
                for sj in (1, -1):
                    a = [0, 0, 0]; a[i] = si; a[j] = sj; out.append(tuple(a))
    for i in range(3):
        for si in (1, -1):
            a = [0, 0, 0]; a[i] = si; out.append(tuple(a))
    return out
SO3_W3 = [(0,), (1,), (-1,)]; SO3_ROOTS = [(1,), (-1,)]

# ----------------------------------------------------------------------------------------------
# 6. Phase 0 -- controls (A-2.5)
# ----------------------------------------------------------------------------------------------
def phase0(ctx):
    g2, rows_rank = ctx['g2'], ctx['g2_rows_rank']
    out = {}
    # (0a)
    all_der = all(is_derivation(D) for D in g2)
    all_anti = all(is_antisym(D) and all(D[i][0] == 0 and D[0][i] == 0 for i in range(8)) for D in g2)
    piv, R = rref_Q([flat(D) for D in g2], 64)
    closure = all(in_span(flat(bracket(g2[i], g2[j])), R, piv) for i in range(14) for j in range(i + 1, 14)) if len(g2) == 14 else False
    HL = [0, 1, 2, 4]
    su2_long_c = stabilizer_pointwise(g2, [E[1], E[2], E[4]]); su2_long = subalgebra_coeffs_to_mats(g2, su2_long_c)
    so4_c = stabilizer_setwise(g2, HL); so4 = subalgebra_coeffs_to_mats(g2, so4_c)
    su2_short = centralizer_in(su2_long, so4)
    idx_long = dynkin_index(su2_long) if len(su2_long) == 3 else None
    idx_short = dynkin_index(su2_short) if len(su2_short) == 3 else None
    rk = lie_rank(g2) if len(g2) == 14 else None
    a = {'g2_dim': len(g2), 'rank': rk, 'derivation_system_unknowns': 64, 'derivation_system_rank': rows_rank,
         'all_derivations': all_der, 'all_antisymmetric': all_anti, 'closure': closure,
         'dim_so4_H124': len(so4), 'dim_su2_long': len(su2_long), 'dim_su2_short': len(su2_short),
         'index_su2_long': fs(idx_long) if idx_long is not None else None, 'index_su2_short': fs(idx_short) if idx_short is not None else None}
    a['PASS'] = (a['g2_dim'] == 14 and rk == 2 and all_der and all_anti and closure and len(so4) == 6 and len(su2_long) == 3
                 and len(su2_short) == 3 and idx_long == 1 and idx_short == 3)
    out['0a'] = a
    ctx['su2_long'] = su2_long; ctx['so4'] = so4
    # (0b)
    c7, c8 = commutant_dim(g2, 7), commutant_dim(g2, 8)
    out['0b'] = {'commutant_dim_on_7': c7, 'commutant_dim_on_1plus7': c8, 'PASS': (c7 == 1 and c8 == 2)}
    # (0c)
    planes, hs, weights = ctx['planes'], ctx['hs'], ctx['weights']
    u8 = [gen_u8(j, k) for j in range(8) for k in range(8)]
    act16 = list(range(16))
    u8d2 = certify('U8_R16.deg2', u8, act16, 2, candidates('R16', 'U8', 2), planes, hs, weights)
    u8d4 = certify('U8_R16.deg4', u8, act16, 4, candidates('R16', 'U8', 4), planes, hs, weights)
    ctx['u8d2'], ctx['u8d4'] = u8d2, u8d4
    # so(16) orbit map at a unit vector: the 120 elementary antisymmetric generators applied to e_0 in R^16
    unit = [Fr(1)] + [Fr(0)] * 15
    rows = []
    for i in range(16):
        for j in range(i + 1, 16):
            v = [Fr(0)] * 16; v[j] += unit[i]; v[i] -= unit[j]; rows.append(v)
    so16_rank = rank_Q(rows, 16)
    c = {'u8_deg2': {'certified_dim': u8d2['certified_dim'], 'lower_bound_rank_Q': u8d2['lower_bound_rank_Q'], 'upper_bounds_mod_p': u8d2['upper_bounds_mod_p']},
         'u8_deg4': {'certified_dim': u8d4['certified_dim'], 'lower_bound_rank_Q': u8d4['lower_bound_rank_Q'], 'upper_bounds_mod_p': u8d4['upper_bounds_mod_p']},
         'o16_deg2': 1, 'o16_deg4': 1,
         'o16_note': 'recorded, not computed: O(16) contains U(8), Inv_O16 is inside Inv_U8 = span(N_tot^k), and N_tot^k is O(16)-invariant (A-2.4)',
         'so16_orbit_rank_at_unit_vector': so16_rank, 'V_of_record': 'S15', 'pi1_V_of_record': '0'}
    c['PASS'] = (u8d2['certified_dim'] == 1 and u8d4['certified_dim'] == 1 and so16_rank == 15)
    out['0c'] = c
    # (0d) the spin-1 condensate control and the G-2a-A1 homotopy controls
    out['0d'] = spin1_control()
    # (0e) the g2-orbit-map ranks
    e = {'e0': orbit_rank(g2, [E[0]]), 'e1': orbit_rank(g2, [E[1]]), 'pair_e1_e2': orbit_rank(g2, [E[1], E[2]]),
         'associative_triple_e1_e2_e4': orbit_rank(g2, [E[1], E[2], E[4]]), 'generic_triple_e1_e2_e3': orbit_rank(g2, [E[1], E[2], E[3]])}
    e['PASS'] = (e['e0'] == 0 and e['e1'] == 6 and e['pair_e1_e2'] == 11 and e['associative_triple_e1_e2_e4'] == 11 and e['generic_triple_e1_e2_e3'] == 14)
    out['0e'] = e
    # (0f) the su(3) control: {D in g2 : D e7 = 0}, dim 8; three explicit degree-2 invariants annihilated and independent
    su3_c = stabilizer_pointwise(g2, [E[7]]); su3 = subalgebra_coeffs_to_mats(g2, su3_c)
    ctx['su3'] = su3
    su3d2 = certify('SU3xU1_R16.deg2', [gen_same(D) for D in su3], act16, 2, candidates('R16', 'SU3xU1', 2), planes, hs, weights)
    ctx['su3d2'] = su3d2
    g2d2 = certify('G2xU1_R16.deg2', [gen_same(D) for D in g2], act16, 2, candidates('R16', 'G2xU1', 2), planes, hs, weights)
    ctx['g2d2'] = g2d2
    g2d2_lower = g2d2['certified_dim']
    su3full = certify('SU3xU1_R16.deg2.full', [gen_same(D) for D in su3], act16, 2, candidates('R16', 'SU3xU1_full', 2), planes, hs, weights)
    f = {'su3_dim': len(su3), 'annihilated': (len(su3d2['explicit_annihilated']) == 3), 'annihilated_names': su3d2['explicit_annihilated'],
         'lower_bound_deg2': su3d2['lower_bound_rank_Q'], 'upper_bounds_mod_p': su3d2['upper_bounds_mod_p'],
         'g2_u1_deg2': g2d2_lower,
         'full_count_deg2': {'note': 'beyond A-2.5: the complete degree-2 inventory of su(3)+u(1) on (1+1+3+3bar), certified with six explicit invariants',
                             'explicit_annihilated': su3full['explicit_annihilated'], 'lower_bound_rank_Q': su3full['lower_bound_rank_Q'],
                             'upper_bounds_mod_p': su3full['upper_bounds_mod_p'], 'certified_dim': su3full['certified_dim'], 'T_even_dim': su3full['T_even_dim']}}
    f['PASS'] = (len(su3) == 8 and f['annihilated'] and su3d2['lower_bound_rank_Q'] == 3 and g2d2_lower is not None and su3d2['lower_bound_rank_Q'] > g2d2_lower)
    out['0f'] = f
    out['all_pass'] = all(out[s]['PASS'] for s in ('0a', '0b', '0c', '0d', '0e', '0f'))
    return out

def homotopy_bookkeeping(P_kind, m, K_connected, pi1_K0, k_has_su2, su2_index, K_is_Gint, d=None):
    """A-2.7 as code (G = G_int x U(1), G_int connected and simply connected). Returns (pi0_H, pi1, winding, pi2, pi3).
    (i) p(H) = Z_m finite and K connected: pi1 = Z with elementary winding 2pi/m; pi2 = pi1(K^0).
    (ii) p(H) = U(1): pi1 = Z/dZ with d = |pi0(K cap H^0)|; pi2 = pi1(K cap H^0) = 0 for the groups met here.
    (iii) pi3 = coker(pi3(H^0) -> pi3(G_int)): 0 if K = G_int; Z if k has no su(2); else Z/(Dynkin index of the pi3-generating su(2))."""
    if P_kind == 'U(1)':
        if d is None: halt('bookkeeping (ii) needs d = |pi0(K cap H^0)|')
        pi1 = '0' if d == 1 else 'Z%d' % d
        winding = None; pi0_H = '0'; pi2 = '0'
    else:
        if not K_connected: halt('bookkeeping (i) needs K connected')
        pi1 = 'Z'; winding = '2pi' if m == 1 else ('pi' if m == 2 else '2pi/%d' % m)
        pi0_H = '0' if m == 1 else 'Z%d' % m
        pi2 = pi1_K0
    if K_is_Gint: pi3 = '0'
    elif not k_has_su2: pi3 = 'Z'
    else: pi3 = '0' if su2_index == 1 else 'Z%d' % su2_index
    return pi0_H, pi1, winding, pi2, pi3

def spin1_control():
    """A-2.5(0d): psi in C^3 under SU(2) x U(1) acting through SO(3); universal-cover bookkeeping"""
    L = []
    for (a, b) in ((1, 2), (2, 0), (0, 1)):
        M = zeros(3); M[b][a] = Fr(1); M[a][b] = Fr(-1); L.append(M)
    def h_space(re, im):
        rows = []
        for comp in range(3):
            rows.append([matvec(Lk, re)[comp] for Lk in L] + [-im[comp]])   # real part of (D + tau J) psi
            rows.append([matvec(Lk, im)[comp] for Lk in L] + [re[comp]])    # imaginary part
        ns = nullspace_Q(rows, 4)
        dim_h = len(ns); dim_k = len([v for v in nullspace_Q(rows + [[Fr(0)] * 3 + [Fr(1)]], 4)])
        return dim_h, dim_k, any(v[3] != 0 for v in ns)
    def orb_rank(vecs):
        rows = []
        for Lk in L:
            row = []
            for v in vecs: row.extend(matvec(Lk, v))
            rows.append(row)
        return rank_Q(rows, 3 * len(vecs))
    # polar: psi = n = e_z (real)
    n = [Fr(0), Fr(0), Fr(1)]; z3 = [Fr(0)] * 3
    dh, dk, ph = h_space(n, z3)
    gram_scalar = (sum(x * x for x in n) == sum(x * x for x in z3) and sum(x * y for x, y in zip(n, z3)) == 0)   # Gram(n, 0): |u| = |v| and u.v = 0 ?
    if gram_scalar: halt('spin-1 polar state has a scalar Gram matrix')
    m = 2                                                              # psi0-analogue absent, Gram non-scalar: P = {+-1} (A-2.6 rule)
    Rx = [[Fr(1), Fr(0), Fr(0)], [Fr(0), Fr(-1), Fr(0)], [Fr(0), Fr(0), Fr(-1)]]   # rotation by pi about e_x, an axis perpendicular to n
    det = (Rx[0][0] * (Rx[1][1] * Rx[2][2] - Rx[1][2] * Rx[2][1]) - Rx[0][1] * (Rx[1][0] * Rx[2][2] - Rx[1][2] * Rx[2][0])
           + Rx[0][2] * (Rx[1][0] * Rx[2][1] - Rx[1][1] * Rx[2][0]))
    orth = matmul(transpose(Rx), Rx) == [[Fr(1 if i == j else 0) for j in range(3)] for i in range(3)]
    witness = (det == 1 and orth and matvec(Rx, n) == [-x for x in n])
    # universal-cover bookkeeping: K~ = Stab_SU(2)(n) is connected since pi1(S2) = 0 (orbit rank 2 = dim S2: transitive);
    # k is 1-dimensional and abelian, so K~^0 = U(1) with pi1 = Z; k contains no su(2)
    orank_p = orb_rank([n])
    Kt_connected = (orank_p == 2)
    pi0_H_p, pi1_p, wind_p, pi2_p, pi3_p = homotopy_bookkeeping('Z2', m, Kt_connected, 'Z' if dk == 1 else None, dk >= 3, None, False)
    polar = {'dim_h': dh, 'dim_k': dk, 'phase_in_h': ph, 'orbit_rank': orank_p, 'm': m, 'witness_rotation_pi_perp': witness,
             'witness_matrix': [[fstr(x) for x in row] for row in Rx], 'K_tilde': 'U(1) (double cover of SO(2), connected since pi1(S2) = 0)',
             'pi0_H_tilde': pi0_H_p, 'pi1': pi1_p, 'elementary_winding': wind_p, 'pi2': pi2_p, 'pi3': pi3_p}
    polar['PASS'] = (dh == 1 and dk == 1 and (not ph) and orank_p == 2 and m == 2 and witness and pi1_p == 'Z' and wind_p == 'pi' and pi2_p == 'Z' and pi3_p == 'Z')
    # ferro: psi = e_x + i e_y
    u = [Fr(1), Fr(0), Fr(0)]; v = [Fr(0), Fr(1), Fr(0)]
    dh2, dk2, ph2 = h_space(u, v)
    gram_scalar2 = (sum(x * x for x in u) == sum(x * x for x in v) and sum(x * y for x, y in zip(u, v)) == 0)
    # orbit rank 3 = dim SO(3): transitive, Stab_SO(3)(u, v) trivial (dim k = 0), so K~ = ker(SU(2) -> SO(3)) = {+-1}:
    # |pi0(K~)| = |pi1(SO(3))| = 2 (adopted), both components in H~^0 -> d = 2
    orank_f = orb_rank([u, v])
    PI1_SO3_ORDER = 2
    d_f = PI1_SO3_ORDER if (dk2 == 0 and orank_f == 3) else None
    pi0_H_f, pi1_f, wind_f, pi2_f, pi3_f = homotopy_bookkeeping('U(1)', None, None, None, dk2 >= 3, None, False, d=d_f)
    ferro = {'dim_h': dh2, 'dim_k': dk2, 'phase_in_h': ph2, 'orbit_rank': orank_f, 'gram_scalar': gram_scalar2,
             'pi1_SO3_adopted': 'Z2', 'K_tilde': '{+1,-1} (pi0 = Z2 from pi1(SO(3)) = Z2; both components in H_tilde^0)', 'd': d_f,
             'pi1': pi1_f, 'pi2': pi2_f, 'pi3': pi3_f}
    ferro['PASS'] = (dh2 == 1 and dk2 == 0 and ph2 and orank_f == 3 and gram_scalar2 and d_f == 2 and pi1_f == 'Z2' and pi2_f == '0' and pi3_f == 'Z')
    # Weyl counts for spin-1 at degrees 2/4/6
    wts = weights_with_u1(SO3_W3, False); rts = roots_with_u1(SO3_ROOTS)
    weyl = [weyl_invariant_dim(wts, rts, 2, d) for d in (2, 4, 6)]
    # binary tetrahedral group: 24 unit quaternions in H_L = span(e0, e1, e2, e4), closure under the octonion product
    units = []
    for k in (0, 1, 2, 4):
        for s in (1, -1):
            q = [Fr(0)] * 8; q[k] = Fr(s); units.append(tuple(q))
    for signs in itertools.product((1, -1), repeat=4):
        q = [Fr(0)] * 8
        for s, k in zip(signs, (0, 1, 2, 4)): q[k] = Fr(s, 2)
        units.append(tuple(q))
    uset = set(units)
    closed = all(tuple(omul(list(x), list(y))) in uset for x in units for y in units)
    norms_ok = all(sum(c * c for c in q) == 1 for q in units)
    bt = {'order': len(uset), 'closed': closed and norms_ok, 'pi1_SO3_mod_T': '2T (order 24) by the covering SU(2) -> SO(3)/T'}
    out = {'spin1_polar': polar, 'spin1_ferro': ferro, 'weyl_spin1_invariant_dims': weyl, 'binary_tetrahedral': bt,
           'pi4_S2_adopted': 'Z2', 'pi4_S3_adopted': 'Z2'}
    out['PASS'] = (polar['PASS'] and ferro['PASS'] and weyl == [1, 2, 2] and bt['order'] == 24 and bt['closed'])
    return out

# ----------------------------------------------------------------------------------------------
# 7. Phase 1 -- the certified invariant inventory (A-2.4)
# ----------------------------------------------------------------------------------------------
def phase1(ctx):
    g2 = ctx['g2']; planes, hs, weights = ctx['planes'], ctx['hs'], ctx['weights']
    G2 = [gen_same(D) for D in g2]; SO7 = [gen_same(R) for R in so7_generators()]
    act16 = list(range(16)); act14 = [i for i in range(16) if i not in (0, 8)]
    blocks = {}
    for alg, gens in (('G2xU1', G2), ('SO7xU1', SO7)):
        for space, act in (('R16', act16), ('R14', act14)):
            for deg in (2, 4):
                key = '%s_%s.deg%d' % (alg, space, deg)
                blocks[key] = certify(key, gens, act, deg, candidates(space, alg, deg), planes, hs, weights)
    # degree-6 explicit lower bound on R14 (not kernel-certified; the Weyl count is the comparison)
    d6 = {}
    for alg, gens in (('G2xU1', G2), ('SO7xU1', SO7)):
        cands = candidates('R14', alg, 6)
        nz = [[[(k, G[j][k]) for k in range(NV) if G[j][k] != 0] for j in range(NV)] for G in gens]
        ann = [n for n, poly in cands.items() if all(not act_Q(G, poly, z) for G, z in zip(gens, nz))]
        mons = sorted(set(e for n in ann for e in cands[n])); idx = {e: i for i, e in enumerate(mons)}
        rows = []
        for n in ann:
            row = [Fr(0)] * len(mons)
            for e, c in cands[n].items(): row[idx[e]] = c
            rows.append(row)
        d6[alg] = {'explicit_annihilated': ann, 'explicit_lower': rank_Q(rows, len(mons)) if rows else 0}
    # Weyl
    weyl = {}
    for alg, w7, roots, oW in (('G2xU1', G2_W7, G2_ROOTS, 12), ('SO7xU1', B3_W7, b3_roots(), 48)):
        for space, sing in (('R16', True), ('R14', False)):
            wts = weights_with_u1(w7, sing); rts = roots_with_u1(roots)
            weyl['%s_%s' % (alg, space)] = {'deg%d' % d: weyl_invariant_dim(wts, rts, oW, d) for d in (2, 4, 6)}
    methods_agree = all(weyl['%s_%s' % (alg, sp)]['deg%d' % d] == blocks['%s_%s.deg%d' % (alg, sp, d)]['certified_dim']
                        for alg in ('G2xU1', 'SO7xU1') for sp in ('R16', 'R14') for d in (2, 4))
    locality = all(weyl['G2xU1_%s' % sp]['deg%d' % d] == weyl['SO7xU1_%s' % sp]['deg%d' % d] for sp in ('R16', 'R14') for d in (2, 4, 6))
    # A-2.4: F-VS-2 fires iff dim Inv_{g2} > dim Inv_{so(7)} at any degree on R14 or R16 (the memo's second clause, a pair
    # rank < 11, is a Phase-0 (0e) failure and reaches VC-4 through phase0.all_pass)
    F_VS_2 = any(weyl['G2xU1_%s' % sp]['deg%d' % d] > weyl['SO7xU1_%s' % sp]['deg%d' % d] for sp in ('R16', 'R14') for d in (2, 4, 6))
    pair_rank_ok = (ctx['phase0']['0e']['pair_e1_e2'] == 11)
    b2, b4 = blocks['G2xU1_R16.deg2'], blocks['G2xU1_R16.deg4']
    hand = {'deg2': 2, 'deg4': 6, 'deg4_T_even': 5}
    F_VS_1 = not (b2['certified_dim'] == hand['deg2'] and b4['certified_dim'] == hand['deg4'] and b4['T_even_dim'] == hand['deg4_T_even'])
    # RUS classification (A-2.4): an invariant is RUS iff it is not in the Q-span of the O(16) invariant of its degree
    Ntot, Ntot2 = inv_Ntot(), ppow(inv_Ntot(), 2)
    def proportional(a, b):
        if not a or not b: return False
        e = next(iter(a));
        if e not in b: return False
        lam = a[e] / b[e]
        return pscale(b, lam) == a
    c2 = candidates('R16', 'G2xU1', 2); c4 = candidates('R16', 'G2xU1', 4)
    rus2 = {n: (not proportional(poly, Ntot)) for n, poly in c2.items()}
    rus4 = {n: (not proportional(poly, Ntot2)) for n, poly in c4.items()}
    singlet_blind = {n: (not uses_singlet(poly)) for n, poly in list(c2.items()) + list(c4.items())}
    rus = {'definition': 'RUS iff not in the Q-span of the O(16) invariant of its degree (N_tot or N_tot^2); singlet-blind iff no monomial contains psi0 or psibar0',
           'deg2': {'dim': b2['certified_dim'], 'RUS_subspace_dim': (b2['certified_dim'] - 1) if b2['certified_dim'] else None, 'flags': rus2},
           'deg4': {'dim': b4['certified_dim'], 'RUS_subspace_dim': (b4['certified_dim'] - 1) if b4['certified_dim'] else None,
                    'T_even_RUS_subspace_dim': (b4['T_even_dim'] - 1) if b4['T_even_dim'] else None, 'flags': rus4},
           'singlet_blind': singlet_blind}
    # the point of record: N_tot^2 in the T-even basis, mapped to the effective parameters
    coeffs, resid_zero = expand_in_basis(Ntot2, [c4[n] for n in BASIS4])
    eff = effective_params(coeffs) if resid_zero else None
    por = {'quartic_coefficients': [fstr(x) for x in coeffs] if resid_zero else None, 'in_T_even_basis': resid_zero,
           'effective_ABc4c5': [fstr(x) for x in eff] if eff else None, 'is_origin': (eff is not None and all(x == 0 for x in eff)),
           'basis_order': BASIS4}
    extra = (b2['certified_dim'] is not None and b4['certified_dim'] is not None and b2['certified_dim'] > 1 and b4['certified_dim'] > 1)
    certs_met = all(blk['certificate_met'] for blk in blocks.values())
    out = {}
    for key, blk in blocks.items():
        alg, rest = key.split('.')
        out.setdefault(alg, {})[rest] = {k: blk[k] for k in ('n_monomials', 'explicit_annihilated', 'lower_bound_rank_Q', 'upper_bounds_mod_p', 'certified_dim', 'T_even_dim', 'bidegree', 'certificate_met', 'upper_bound_detail', 'explicit_not_annihilated')}
    out['G2xU1_R14']['deg6_explicit_lower'] = d6['G2xU1']['explicit_lower']
    out['G2xU1_R14']['deg6_explicit_annihilated'] = d6['G2xU1']['explicit_annihilated']
    out['SO7xU1_R14']['deg6_explicit_lower'] = d6['SO7xU1']['explicit_lower']
    out['weyl'] = weyl
    out['T_parity'] = {'deg2': b2['T_parity'], 'deg4': b4['T_parity']}
    out['methods_agree_deg2_deg4'] = methods_agree
    out['locality_g2_equals_so7'] = locality
    out['hand_count'] = hand
    out['F_VS_1'] = F_VS_1; out['F_VS_2'] = F_VS_2; out['pair_rank_11'] = pair_rank_ok
    out['RUS'] = rus
    out['point_of_record'] = por
    out['basis_deg2'] = BASIS2; out['basis_deg4'] = BASIS4; out['T_odd_deg4'] = T_ODD4
    out['extra_invariants_found'] = extra
    out['all_certificates_met'] = certs_met
    ctx['phase1_blocks'] = blocks; ctx['c4'] = c4; ctx['c2'] = c2
    return out

def expand_in_basis(poly, basis_polys):
    """exact least-squares-free expansion: solve sum c_i B_i = poly; returns (coeffs, residual_is_zero)"""
    mons = sorted(set(e for b in basis_polys for e in b) | set(poly))
    idx = {e: i for i, e in enumerate(mons)}
    n = len(basis_polys)
    rows = []
    for e in mons:
        rows.append([b.get(e, Fr(0)) for b in basis_polys] + [poly.get(e, Fr(0))])
    piv, R = rref_Q(rows, n + 1)
    if n in piv: return [None] * n, False
    sol = [Fr(0)] * n
    for i, pc in enumerate(piv): sol[pc] = R[i][n]
    recon = {}
    for c, b in zip(sol, basis_polys): recon = padd(recon, pscale(b, c))
    return sol, (recon == poly)

def effective_params(c, mu0=Fr(0), mu7=Fr(0)):
    """A-2.6: V = -mu0 rho0 - mu7 N + c1 rho0^2 + c2 rho0 N + c3 N^2 + c4 |S|^2 + c5 Re(psi0^2 Sbar) on |psi|^2 = 1
    equals A rho^2 + B rho + c4 s^2 + c5 t + const with A = c1 - c2 + c3, B = (mu7 - mu0) + c2 - 2 c3"""
    c1, c2, c3, c4, c5 = c
    return [c1 - c2 + c3, (mu7 - mu0) + c2 - 2 * c3, c4, c5]

# ----------------------------------------------------------------------------------------------
# 8. Phase 2 -- the stratum table, the homotopy bookkeeping and the phase diagram (A-2.6 / A-2.7)
# ----------------------------------------------------------------------------------------------
def cvec(entries):
    """complex 8-vector from {index: (re, im)}"""
    re = [Fr(0)] * 8; im = [Fr(0)] * 8
    for k, (a, b) in entries.items(): re[k] = Fr(a); im[k] = Fr(b)
    return re, im
REPRESENTATIVES = {   # A-2.6, unnormalized rationals
    'R':   {0: (1, 0)},
    'P7':  {1: (1, 0)},
    'F7':  {1: (1, 0), 2: (0, 1)},
    'I7':  {1: (3, 0), 2: (0, 4)},
    'MP+': {0: (3, 0), 1: (4, 0)},
    'MP-': {0: (3, 0), 1: (0, 4)},
    'MP0': {0: (1, 1), 1: (2, 0)},
    'MF':  {0: (1, 0), 1: (1, 0), 2: (0, 1)},
    'MI+': {0: (1, 0), 1: (4, 0), 2: (0, 3)},
    'MI-': {0: (1, 0), 1: (3, 0), 2: (0, 4)},
    'MI0': {0: (1, 1), 1: (3, 0), 2: (0, 4)},
}

def invariants_of(re, im):
    norm2 = sum(x * x for x in re) + sum(x * x for x in im)
    rho0 = (re[0] ** 2 + im[0] ** 2) / norm2
    # S = sum psi_a^2 (a = 1..7): Re S = sum (u^2 - v^2), Im S = 2 sum u v
    SR = sum(re[a] ** 2 - im[a] ** 2 for a in range(1, 8)); SI = 2 * sum(re[a] * im[a] for a in range(1, 8))
    s2 = (SR ** 2 + SI ** 2) / norm2 ** 2
    # psi0^2 = (x0^2 - y0^2) + i 2 x0 y0 ; psi0^2 Sbar real part = Re(psi0^2) Re S + Im(psi0^2) Im S
    p0R = re[0] ** 2 - im[0] ** 2; p0I = 2 * re[0] * im[0]
    t = (p0R * SR + p0I * SI) / norm2 ** 2
    u = re[1:]; v = im[1:]
    uu = sum(x * x for x in u); vv = sum(x * x for x in v); uv = sum(x * y for x, y in zip(u, v))
    gram_scalar = (uu == vv and uv == 0)
    rank_uv = rank_Q([u, v], 7)
    return {'rho_norm': rho0, 's2_norm': s2, 't_norm': t, 'gram_scalar': gram_scalar, 'rank_uv': rank_uv,
            'S_is_zero': (SR == 0 and SI == 0), 'psi0_is_zero': (re[0] == 0 and im[0] == 0), 'norm2': norm2}

def stratum_label(rho, s, t):
    """A-2.6 labels from the orbit-space coordinates (rho, s, t) with s = |S| / |psi|^2 and t = Re(psi0^2 Sbar) / |psi|^4"""
    if rho == 1: return 'R'
    if rho == 0:
        if s == 1: return 'P7'
        if s == 0: return 'F7'
        return 'I7'
    if s == 1 - rho: return 'MP+' if t > 0 else ('MP-' if t < 0 else 'MP0')
    if s == 0: return 'MF'
    return 'MI+' if t > 0 else ('MI-' if t < 0 else 'MI0')

def quaternion_involution_witness(support):
    """A-2.6: sigma_{H'} = +1 on e0 and the three units of a Fano line disjoint from the support, -1 on the other four;
    verified exactly as an automorphism on all 64 basis pairs; returns (line, signs, is_automorphism)"""
    for line in LINES:
        if not (set(line) & set(support)):
            signs = [1 if (k == 0 or k in line) else -1 for k in range(8)]
            ok = True
            for a in range(8):
                for b in range(8):
                    s, c = MUL[a][b]
                    if signs[a] * signs[b] * s != s * signs[c]: ok = False
            return line, signs, ok
    return None, None, False

def phase2(ctx):
    g2 = ctx['g2']; su2_long = ctx['su2_long']
    piv_g2, R_g2 = rref_Q([flat(D) for D in g2], 64)
    strata = {}
    for lab in STRATA:
        re, im = cvec(REPRESENTATIVES[lab])
        inv = invariants_of(re, im)
        # h = {(D, tau) in g2 + R : D psi + tau J psi = 0}, J psi = i psi: (x, y) -> (-y, x)
        rows = []
        for comp in range(8):
            rows.append([matvec(D, re)[comp] for D in g2] + [-im[comp]])
            rows.append([matvec(D, im)[comp] for D in g2] + [re[comp]])
        h = nullspace_Q(rows, 15)
        k = nullspace_Q(rows + [[Fr(0)] * 14 + [Fr(1)]], 15)
        dim_h, dim_k = len(h), len(k)
        phase_in_h = any(v[14] != 0 for v in h)
        k_mats = subalgebra_coeffs_to_mats(g2, [v[:14] for v in k])
        # the G2-orbit map at the real vectors (u, v) = imaginary parts (indices 1..7); e0 components are g2-fixed
        u8 = [Fr(0)] + re[1:]; v8 = [Fr(0)] + im[1:]
        orank = orbit_rank(g2, [u8, v8])
        orbit = {0: 'point', 6: 'S6', 11: 'V2(R7)'}.get(orank, 'rank %d' % orank)
        # the phase image P = p(H)
        witness = None
        if not inv['psi0_is_zero']:
            P_kind, m = 'trivial', 1
            P_reason = 'psi0 != 0: g fixes e0, so omega psi0 = psi0 forces omega = 1'
        elif inv['gram_scalar']:
            P_kind, m = 'U(1)', None
            P_reason = 'psi0 = 0 and Gram(u, v) scalar (S = 0): every phase is realized by a G2 rotation of the (u, v)-plane; phase_in_h = %s' % phase_in_h
        else:
            P_kind, m = 'Z2', 2
            support = [a for a in range(1, 8) if re[a] != 0 or im[a] != 0]
            line, signs, is_aut = quaternion_involution_witness(support)
            sig = zeros(8)
            for i in range(8): sig[i][i] = Fr(signs[i])
            maps_to_minus = (matvec(sig, re) == [-x for x in re] and matvec(sig, im) == [-x for x in im])
            witness = {'fano_line': list(line), 'signs': signs, 'is_automorphism': is_aut, 'maps_psi_to_minus_psi': maps_to_minus, 'omega': -1}
            if not (is_aut and maps_to_minus): halt('witness failed on stratum %s' % lab)
            P_reason = 'psi0 = 0 and Gram(u, v) non-scalar: R_alpha^T Gram R_alpha = Gram only for alpha in {0, pi}; witness (sigma_H\', -1) in H'
        # K identification and connectivity
        K_name = {14: 'G2', 8: 'SU3', 3: 'SU2_long'}.get(dim_k)
        if K_name is None: halt('unexpected dim k = %d on stratum %s' % (dim_k, lab))
        if orbit not in ('point', 'S6', 'V2(R7)'): halt('unexpected orbit rank %d on stratum %s' % (orank, lab))
        pi1_orbit = '0'                                                   # adopted: pi1(S^n) = 0 (n >= 2), pi1(V2(R7)) = 0
        pi0_K = pi1_orbit                                                 # pi0(K) = pi1(G2-orbit) since G2 is connected and simply connected
        K_connected = (pi0_K == '0')
        # the pi3-generating su(2) of H^0 and its Dynkin index
        if dim_k == 3:
            dyn = dynkin_index(k_mats); su2_in_k = True
        else:
            # the long-root su(2): pointwise stabilizer of the quaternion subalgebra H_L = span(e0,e1,e2,e4) (contains n = e1 for P7/MP)
            piv_k, R_k = rref_Q([flat(M) for M in k_mats], 64)
            su2_in_k = all(in_span(flat(M), R_k, piv_k) for M in su2_long)
            dyn = dynkin_index(su2_long) if su2_in_k else None
        if dyn is None or dyn != 1: halt('Dynkin index of the pi3-generating su(2) on %s is %s' % (lab, dyn))
        dyn = int(dyn)
        # homotopy bookkeeping (A-2.7): pi1(K^0) = 0 for G2, SU(3), SU(2) (adopted); on F7 K = SU(2)_long is connected and
        # H = U(1) x SU(2)_long is connected, so d = |pi0(K cap H^0)| = 1
        d = (1 if K_connected else None) if P_kind == 'U(1)' else None
        pi0_H, pi1, winding, pi2, pi3 = homotopy_bookkeeping(P_kind, m, K_connected, '0', su2_in_k, dyn, K_name == 'G2', d=d)
        dim_V = 15 - dim_h
        strata[lab] = {
            'representative': {str(kk): [fstr(a), fstr(b)] for kk, (a, b) in REPRESENTATIVES[lab].items()},
            'invariants': {'rho_norm': fstr(inv['rho_norm']), 's2_norm': fstr(inv['s2_norm']), 't_norm': fstr(inv['t_norm']),
                           'gram_scalar': inv['gram_scalar'], 'rank_uv': inv['rank_uv']},
            'dim_h': dim_h, 'dim_k': dim_k, 'phase_in_h': phase_in_h, 'orbit_rank_of_imaginary_part': orank, 'orbit': orbit,
            'P_kind': P_kind, 'P_reason': P_reason, 'm': m, 'witness': witness, 'K': K_name, 'dynkin_index': dyn,
            'pi3_generating_su2_in_k': su2_in_k, 'dim_V': dim_V, 'pi0_K': pi0_K, 'K_connected': K_connected, 'pi0_H': pi0_H,
            'pi1': pi1, 'elementary_winding': winding, 'pi2': pi2, 'pi3': pi3, 'pi1_nontrivial': (pi1 != '0'),
        }
    # the criterion: pi1(V) = 0 iff rho0 = 0 and S = 0
    crit_ok = True; crit_table = {}
    for lab in STRATA:
        re, im = cvec(REPRESENTATIVES[lab]); inv = invariants_of(re, im)
        lhs = (strata[lab]['pi1'] == '0'); rhs = (inv['psi0_is_zero'] and inv['S_is_zero'])
        crit_table[lab] = {'pi1_zero': lhs, 'rho0_zero_and_S_zero': rhs, 'agree': lhs == rhs}
        crit_ok = crit_ok and (lhs == rhs)
    # the effective map, checked exactly on random rational points of S^15
    reduction_ok = reduction_check(ctx)
    # exact minimization over the orbit space and the 2401-point sampling
    pi1_of = {lab: strata[lab]['pi1'] for lab in STRATA}
    grid = [Fr(-2), Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1), Fr(2)]
    tally = {}; realized = set(); cone_ok = True; p0_points = []; crit_min_ok = True; n = 0
    for A in grid:
        for B in grid:
            for c4 in grid:
                for c5 in grid:
                    n += 1
                    res = minimize_orbit_space(A, B, c4, c5)
                    key = outcome_key(res)
                    tally[key] = tally.get(key, 0) + 1
                    realized |= set(res['strata'])
                    if 'P0' in res['faces']: p0_points.append([fstr(A), fstr(B), fstr(c4), fstr(c5)])
                    half = minimize_orbit_space(A / 2, B / 2, c4 / 2, c5 / 2)
                    if outcome_key(half) != key: cone_ok = False
                    for (rho, s, t) in res['isolated_points']:
                        lab = stratum_label(rho, s, t)
                        if (pi1_of[lab] == '0') != (rho == 0 and s == 0): crit_min_ok = False
                    for (rho, s) in res['isolated_minimizers_rs']:          # free-t candidates (c5 = 0): every label of the t-interval
                        for lab in res['labels_of_candidates'][(rho, s)]:
                            if (pi1_of[lab] == '0') != (rho == 0 and s == 0): crit_min_ok = False
    sampling = {'grid': [fstr(x) for x in grid], 'n_points': n, 'tally': dict(sorted(tally.items())),
                'strata_realized_as_minimizers': sorted(realized), 'cone_property': cone_ok,
                'P0_only_at_origin': (p0_points == [['0', '0', '0', '0']]), 'P0_points': p0_points,
                'pi1_zero_iff_rho0_zero_and_S_zero_on_all_nondegenerate_minimizers': crit_min_ok,
                'outcome_key_format': 'sorted stratum labels joined by ","; degenerate faces, if any, appended after " | " joined by ","'}
    rus = ctx['phase1']['RUS']
    n_deg2, n_deg4 = rus['deg2']['RUS_subspace_dim'], rus['deg4']['T_even_RUS_subspace_dim']
    codim = {'RUS_directions_total': n_deg2 + n_deg4, 'RUS_directions_deg2': n_deg2, 'RUS_directions_deg4_T_even': n_deg4,
             'effective_parameters_on_fixed_density': len(effective_params([Fr(0)] * 5)),
             'P0': 'the origin of the effective (A, B, c4, c5) space; the whole orbit space is the minimizer set there'}
    F_VS_3 = not (crit_ok and crit_min_ok)
    ctx['pi1_of'] = pi1_of
    return {'strata': strata, 'criterion_pi1_zero_iff_rho0_zero_and_S_zero': crit_ok, 'criterion_table': crit_table,
            'reduction_check': reduction_ok, 'sampling': sampling, 'codimension': codim, 'F_VS_3': F_VS_3}

def reduction_check(ctx, trials=24, seed=20260930):
    """V(psi) on rational unit vectors of S^15 (stereographic from Q^15) versus A rho^2 + B rho + c4 s^2 + c5 t + (c3 - mu7)"""
    rng = random.Random(seed)
    c4 = ctx['c4']; c2 = ctx['c2']
    basis4 = [c4[nm] for nm in BASIS4]; basis2 = [c2[nm] for nm in BASIS2]
    def ev(poly, x):
        tot = Fr(0)
        for e, c in poly.items():
            term = c
            for i, p in enumerate(e):
                if p: term *= x[i] ** p
            tot += term
        return tot
    for _ in range(trials):
        y = [Fr(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(15)]
        n2 = sum(t * t for t in y)
        xs = [2 * t / (n2 + 1) for t in y] + [(n2 - 1) / (n2 + 1)]      # 16 real coordinates on S^15
        if sum(t * t for t in xs) != 1: return False
        re, im = xs[:8], xs[8:]
        # psi_k = re_k + i im_k ; psibar_k = re_k - i im_k : evaluate the real polynomials through complex arithmetic
        # all basis polynomials are real-valued, so evaluate via (re, im) with complex Fractions
        def cev(poly):
            tot_r, tot_i = Fr(0), Fr(0)
            for e, c in poly.items():
                tr, ti = c, Fr(0)
                for i, p in enumerate(e):
                    for _ in range(p):
                        if i < 8: a, b = re[i], im[i]
                        else: a, b = re[i - 8], -im[i - 8]
                        tr, ti = tr * a - ti * b, tr * b + ti * a
                tot_r += tr; tot_i += ti
            if tot_i != 0: halt('a basis invariant evaluated to a non-real value')
            return tot_r
        mu0, mu7 = Fr(rng.randint(-4, 4)), Fr(rng.randint(-4, 4))
        cs = [Fr(rng.randint(-4, 4), rng.randint(1, 3)) for _ in range(5)]
        rho0, N = cev(basis2[0]), cev(basis2[1])
        vals4 = [cev(b) for b in basis4]
        V = -mu0 * rho0 - mu7 * N + sum(c * v for c, v in zip(cs, vals4))
        A, B, cc4, cc5 = effective_params(cs, mu0, mu7)
        s2, t = vals4[3], vals4[4]
        rhs = A * rho0 ** 2 + B * rho0 + cc4 * s2 + cc5 * t + (cs[2] - mu7)
        if V != rhs or N != 1 - rho0: return False
    return True

def minimize_orbit_space(A, B, c4, c5):
    """A-2.6: minimize E = A rho^2 + B rho + c4 s^2 + c5 t over P = {0<=rho<=1, 0<=s<=1-rho, |t|<=rho s}.
    t = -sgn(c5) rho s (t free if c5 = 0); then f(rho, s) = A rho^2 + B rho + c4 s^2 - |c5| rho s over the triangle."""
    A, B, c4, c5 = Fr(A), Fr(B), Fr(c4), Fr(c5)
    ac5 = abs(c5); sgn = (c5 > 0) - (c5 < 0)
    def f(r, s): return A * r * r + B * r + c4 * s * s - ac5 * r * s
    cands = {(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1))}
    if A != 0:
        r = -B / (2 * A)
        if 0 < r < 1: cands.add((r, Fr(0)))
    a2 = A + c4 + ac5; a1 = B - 2 * c4 - ac5                      # f(rho, 1-rho) = a2 rho^2 + a1 rho + c4
    if a2 != 0:
        r = -a1 / (2 * a2)
        if 0 < r < 1: cands.add((r, 1 - r))
    det = 4 * A * c4 - ac5 * ac5                                     # [[2A, -|c5|], [-|c5|, 2 c4]] (rho, s)^T = (-B, 0)^T
    if det != 0:
        r = (-2 * c4 * B) / det; s = (-ac5 * B) / det
        if r > 0 and s > 0 and r + s < 1: cands.add((r, s))
    Emin = min(f(r, s) for (r, s) in cands)
    iso = sorted((r, s) for (r, s) in cands if f(r, s) == Emin)
    faces = []
    if A == 0 and B == 0 and Emin == 0: faces.append('edge_s=0')
    if c4 == 0 and Emin == 0: faces.append('edge_rho=0')
    if a2 == 0 and a1 == 0 and c4 == Emin: faces.append('edge_s=1-rho')
    whole = (A == 0 and B == 0 and c4 == 0 and c5 == 0)
    if whole: faces = ['P0']
    # interior segment: g = f - Emin as a quadratic form in (rho, s, 1); rank 1 <=> g = k L^2
    M = [[A, -ac5 / 2, B / 2], [-ac5 / 2, c4, Fr(0)], [B / 2, Fr(0), -Emin]]
    seg = None
    if not whole:
        rk = rank_Q([list(r) for r in M], 3)
        if rk == 1:
            row = next(r for r in M if any(x != 0 for x in r))
            al, be, ga = row
            # the line al rho + be s + ga = 0 intersected with the closed triangle
            pts = set()
            def add(r, s):
                if 0 <= r <= 1 and 0 <= s <= 1 - r: pts.add((r, s))
            if be != 0: add(Fr(0), -ga / be); add(Fr(1), (-ga - al) / be)
            if al != 0: add(-ga / al, Fr(0))
            if al != be: add((-ga - be) / (al - be), 1 - (-ga - be) / (al - be))     # with s = 1 - rho: (al - be) rho + be + ga = 0
            else:
                if be + ga == 0:                                                       # the line contains the edge s = 1 - rho
                    add(Fr(0), Fr(1)); add(Fr(1), Fr(0))
            pts = sorted(pts)
            if len(pts) >= 2:
                p, q = pts[0], pts[-1]
                mr, ms = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                if mr > 0 and ms > 0 and mr + ms < 1:
                    seg = (p, q); faces.append('interior_segment')
    # strata of the minimizer set
    labels = set()
    def tlabels(r, s):
        if c5 != 0 or r * s == 0: return {stratum_label(r, s, -sgn * r * s)}
        return {stratum_label(r, s, -r * s), stratum_label(r, s, Fr(0)), stratum_label(r, s, r * s)}
    labels_of_candidates = {(r, s): sorted(tlabels(r, s)) for (r, s) in iso}
    for (r, s) in iso: labels |= tlabels(r, s)
    if 'edge_s=0' in faces: labels |= {'F7', 'MF', 'R'}
    if 'edge_rho=0' in faces: labels |= {'F7', 'I7', 'P7'}
    if 'edge_s=1-rho' in faces: labels |= {'P7', 'R'} | tlabels(Fr(1, 2), Fr(1, 2))
    if seg is not None:
        (p, q) = seg
        labels |= tlabels(*p) | tlabels(*q) | tlabels((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    if whole: labels = set(STRATA)
    isolated = []
    for (r, s) in iso:
        if c5 != 0 or r * s == 0: isolated.append((r, s, -sgn * r * s))
    return {'Emin': Emin, 'isolated_minimizers_rs': iso, 'labels_of_candidates': labels_of_candidates, 'faces': faces, 'segment': seg, 'strata': sorted(labels), 'isolated_points': isolated}

def outcome_key(res):
    k = ','.join(res['strata'])
    if res['faces']: k += ' | ' + ','.join(res['faces'])
    return k

# ----------------------------------------------------------------------------------------------
# 9. Phase 3 -- the forcing table and the F-a map (A-2.8)
# ----------------------------------------------------------------------------------------------
def phase3(ctx):
    g2 = ctx['g2']; c4 = ctx['c4']; c2 = ctx['c2']; pi1_of = ctx['pi1_of']
    gens = [gen_same(D) for D in g2]
    nz = [[[(k, G[j][k]) for k in range(NV) if G[j][k] != 0] for j in range(NV)] for G in gens]
    X = [PSI[k] for k in range(8)]                                      # psi as a polynomial-valued octonion
    Xdag = [PSIB[0]] + [pneg(PSIB[k]) for k in range(1, 8)]              # octonion-and-complex conjugate
    def normH(Z):                                                       # ||Z||^2_H = sum_k Z_k conj(Z_k)
        out = {}
        for z in Z: out = padd(out, pmul(z, pconj(z)))
        return out
    def NO(Z):                                                          # N_O(Z) = sum_k Z_k^2
        out = {}
        for z in Z: out = padd(out, pmul(z, z))
        return out
    XXd = omul_poly(X, Xdag); XdX = omul_poly(Xdag, X); XX = omul_poly(X, X)
    forms = {
        'F-a.1 |<psi,psi>|^2 (the complex bilinear norm, modulus squared)': pmul(NO(X), pconj(NO(X))),
        'F-a.2 ||psi psibar^dag||^2_H': normH(XXd),
        'F-a.3 ||psibar^dag psi||^2_H': normH(XdX),
        'F-a.4 ||psi^2||^2_H': normH(XX),
        'F-a.5 N_O(psi psibar^dag) = sum_k P_k^2': NO(XXd),
        'F-a.6 ||Im_O(psi psibar^dag)||^2_H': normH([{}] + XXd[1:]),
        'D-a.1 Re_O(psi psibar^dag) (degree 2)': XXd[0],
        'D-a.2 Re_O(psibar^dag psi) (degree 2)': XdX[0],
    }
    Ntot, Ntot2 = inv_Ntot(), ppow(inv_Ntot(), 2)
    out_forms = {}
    for name, poly in forms.items():
        degs = pbidegree(poly)
        if len(degs) != 1: halt('form %s is not homogeneous of one bidegree' % name)
        (dp, dq) = next(iter(degs)); deg = dp + dq
        j_inv = (dp == dq)
        g2_inv = all(not act_Q(G, poly, z) for G, z in zip(gens, nz))
        par = t_parity(poly)
        rec = {'degree': deg, 'bidegree': [dp, dq], 'g2_u1_invariant': (g2_inv and j_inv), 'T_parity': par}
        if deg == 4:
            coeffs, ok = expand_in_basis(poly, [c4[n] for n in BASIS4])
            rec['in_T_even_basis'] = ok
            rec['basis_order'] = BASIS4
            if ok:
                eff = effective_params(coeffs)
                res = minimize_orbit_space(*eff)
                rec['coefficients'] = [fstr(x) for x in coeffs]
                rec['effective_ABc4c5'] = [fstr(x) for x in eff]
                rec['is_O16_point'] = all(x == 0 for x in eff)
                rec['proportional_to_Ntot2'] = proportional_poly(poly, Ntot2)
                rec['Emin'] = fstr(res['Emin'])
                rec['minimizers'] = res['strata']
                rec['degenerate_faces'] = res['faces']
                rec['isolated_minimizers_rs'] = [[fstr(r), fstr(s)] for (r, s) in res['isolated_minimizers_rs']]
                rec['segment'] = [[fstr(r), fstr(s)] for (r, s) in res['segment']] if res['segment'] else None
                rec['pi1_of_minimizing_strata'] = {lab: pi1_of[lab] for lab in res['strata']}
            else:
                coeffs6, ok6 = expand_in_basis(poly, [c4[n] for n in BASIS4 + [T_ODD4]])
                rec['coefficients_with_T_odd'] = [fstr(x) for x in coeffs6] if ok6 else None
                for kk in ('coefficients', 'effective_ABc4c5', 'is_O16_point', 'Emin', 'minimizers', 'degenerate_faces', 'pi1_of_minimizing_strata'): rec[kk] = None
        elif deg == 2:
            coeffs, ok = expand_in_basis(poly, [c2[n] for n in BASIS2])
            rec['in_basis'] = ok; rec['basis_order'] = BASIS2
            rec['coefficients'] = [fstr(x) for x in coeffs] if ok else None
            rec['is_O16'] = proportional_poly(poly, Ntot)
        else:
            halt('form %s has degree %d' % (name, deg))
        out_forms[name] = rec
    forcing = {
        'F-a': {'status': 'MAP', 'note': 'computed; each algebra-native form located in the stratum table; forces nothing (I2 is the import; Q-A1-3 the reading of record)'},
        'F-b': {'status': 'SCREENED_OUT', 'note': 'A-2.1 / Q-VS-1: the carrier of the real unit is not settled (not the K7 vertices); the computation is the named successor S-VS-1'},
        'F-c': {'status': 'NOT_FORCING', 'note': 'A-2.1 / Q-VS-2: the kernel couples to the total density; U*rho with rho = sum |psi_k|^2 is O(16)-symmetric; recorded, not computed'},
        'F-d': {'status': 'EXCLUDED', 'note': 'the oriented term O vanishes on every uniform state; defect-sector only (memo section 3)'},
    }
    live = [k for k, v in forcing.items() if v['status'] not in ('MAP', 'SCREENED_OUT', 'NOT_FORCING', 'EXCLUDED')]
    return {'F_a': out_forms, 'forcing_table': forcing, 'live_sources': len(live), 'live_source_names': live, 'F_VS_4': (len(live) > 0),
            'fixed_strata_by_live_sources': {}}

def omul_poly(x, y):
    z = [{} for _ in range(8)]
    for i in range(8):
        if not x[i]: continue
        for j in range(8):
            if not y[j]: continue
            s, k = MUL[i][j]
            prod = pmul(x[i], y[j])
            z[k] = padd(z[k], prod if s > 0 else pneg(prod))
    return z

def proportional_poly(a, b):
    if not a or not b: return False
    e = next(iter(a))
    if e not in b: return False
    lam = a[e] / b[e]
    return pscale(b, lam) == a

# ----------------------------------------------------------------------------------------------
# 10. the class-code machine (A-2.8; precedence VC-4 > VC-2 > VC-1 > VC-3), run last
# ----------------------------------------------------------------------------------------------
def class_code(ph0, ph1, ph2, ph3):
    reasons = []
    if not ph0['all_pass']: reasons.append('a Phase-0 control failed')
    if ph1['F_VS_2']: reasons.append('F-VS-2 fired')
    if not ph1['all_certificates_met']: reasons.append('a Phase-1 certificate did not meet')
    if reasons: return 'VC-4', reasons
    fixed = ph3['fixed_strata_by_live_sources']          # {source: [strata]} for live sources that fix a stratum
    pi1_of = {lab: ph2['strata'][lab]['pi1'] for lab in STRATA}
    if any(pi1_of[s] == '0' for labs in fixed.values() for s in labs): return 'VC-2', ['a live source fixes a pi1 = 0 stratum']
    if any(pi1_of[s] == 'Z' for labs in fixed.values() for s in labs): return 'VC-1', ['a live source fixes a pi1 = Z stratum']
    all_screened = all(v['status'] in ('MAP', 'SCREENED_OUT', 'NOT_FORCING', 'EXCLUDED') for v in ph3['forcing_table'].values())
    if ph1['extra_invariants_found'] and all_screened and ph3['live_sources'] == 0:
        return 'VC-3', ['the extra (RUS) invariants are certified; every source is a map, screened out, non-forcing or excluded; live_sources = 0']
    return 'VC-4', ['no class reached']

# ----------------------------------------------------------------------------------------------
# 11. main
# ----------------------------------------------------------------------------------------------
def write_checkpoint(path, ck, mod, pats):
    for attempt in range(4):
        text = json.dumps(ck, indent=1, sort_keys=True, ensure_ascii=False)
        hits, coll = mod.scan_text(text, pats)
        if hits:
            if os.path.exists(path): os.remove(path)
            halt('T1 hit in the checkpoint at pattern indices %s; checkpoint not kept' % sorted(set(i for i, _ in hits)), 3)
        rec = {'hits': [], 'numeric_collisions': len(coll)}
        if ck.get('T1_post_write') == rec:
            open(path, 'w', encoding='utf-8').write(text)
            # re-scan the written bytes
            hits2, coll2 = mod.scan_text(open(path, 'rb').read().decode('utf-8', 'replace'), pats)
            if hits2:
                os.remove(path); halt('T1 hit on re-scan of the written checkpoint', 3)
            return rec, hashlib.md5(open(path, 'rb').read()).hexdigest()
        ck['T1_post_write'] = rec
    halt('checkpoint T1 bookkeeping did not converge')

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('preread', 'run'): print(__doc__); sys.exit(1)
    mode = sys.argv[1]
    t0 = time.time()
    guards = guard_all()
    mod, pats = load_scanner()
    me = os.path.abspath(__file__)
    t1_pre = t1_scan_files(mod, pats, [('instrument', me), ('memo', P(MEMO)), ('lock_record', P(LOCK)), ('extract', P(EXTRACT)),
                                       ('schema', P(SCHEMA)), ('comparator', P(COMPARATOR))])
    print('guards OK (7/7); T1 pre-scan CLEAN (6 files); mode =', mode)
    # the algebra
    g2, rows_rank = compute_g2()
    print('g2: dim %d (derivation system rank %d)' % (len(g2), rows_rank))
    hs, planes = cartan_pair(g2)
    ctx = {'g2': g2, 'g2_rows_rank': rows_rank}
    # weight coordinates for the first prime (the same planes serve every prime; weights are prime-independent integers)
    p0 = PRIMES[0]; r0 = sqrt_minus1(p0)
    C, Cinv = weight_change_of_basis(planes, p0)
    weights = variable_weights([conj16(gen_same(H), C, Cinv, p0) for H in hs], p0, r0)
    ctx['weights'], ctx['planes'], ctx['hs'] = weights, planes, hs
    ph0 = phase0(ctx); ctx['phase0'] = ph0
    print('Phase 0:', 'all PASS' if ph0['all_pass'] else 'FAIL', {s: ph0[s]['PASS'] for s in ('0a', '0b', '0c', '0d', '0e', '0f')})
    ck = {'gate': 'G-VS1', 'leg': 'cc', 'mode': mode,
          'identity': {'instrument_md5': md5_of(me), 'memo_md5': guards[MEMO][0], 'memo_bytes': guards[MEMO][1],
                       'lock_md5': guards[LOCK][0], 'lock_bytes': guards[LOCK][1], 't1_md5': guards[T1LIST][0], 't1_patterns': len(pats),
                       'scanner_md5': guards[SCANNER][0], 'extract_md5': guards[EXTRACT][0], 'extract_bytes': guards[EXTRACT][1],
                       'schema_md5': guards[SCHEMA][0], 'comparator_md5': guards[COMPARATOR][0], 'elections': ELECTIONS, 'readings': READINGS,
                       'octonion_convention': OCTONION_CONVENTION, 'primes_for_upper_bound': PRIMES,
                       'weight_coordinates': {'planes_paired_to_e7': [list(p) for p in planes], 'variable_weights_psi_block': [list(w) for w in weights[:8]]},
                       'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
          'T1_pre': t1_pre, 'phase0': ph0, 'phase1': None, 'phase2': None, 'phase3': None, 'verdict': None,
          'T1_post_write': {'hits': [], 'numeric_collisions': 0}, 'runtime_seconds': 0}
    if mode == 'preread':
        if not ph0['all_pass']: halt('Phase 0 failed; no pre-read checkpoint written', 4)
        ck['runtime_seconds'] = int(round(time.time() - t0))
        rec, md5 = write_checkpoint(P('g_vs1_ccleg_prereadcheckpoint.json'), ck, mod, pats)
        print('pre-read checkpoint written: g_vs1_ccleg_prereadcheckpoint.json md5', md5, 'runtime %ds' % ck['runtime_seconds'])
        return
    ph1 = phase1(ctx); ctx['phase1'] = ph1
    print('Phase 1: certificates met =', ph1['all_certificates_met'], '; methods_agree =', ph1['methods_agree_deg2_deg4'], '; F_VS_1 =', ph1['F_VS_1'], '; F_VS_2 =', ph1['F_VS_2'])
    ph2 = phase2(ctx)
    print('Phase 2: criterion =', ph2['criterion_pi1_zero_iff_rho0_zero_and_S_zero'], '; reduction =', ph2['reduction_check'], '; F_VS_3 =', ph2['F_VS_3'])
    ph3 = phase3(ctx)
    print('Phase 3: live_sources =', ph3['live_sources'], '; F_VS_4 =', ph3['F_VS_4'])
    code, reasons = class_code(ph0, ph1, ph2, ph3)
    ck['phase1'], ck['phase2'], ck['phase3'] = ph1, ph2, ph3
    ck['verdict'] = {'class_code': code, 'precedence': 'VC-4 > VC-2 > VC-1 > VC-3', 'reasons': reasons,
                     'H_items_not_class_changes': {'F_VS_1': ph1['F_VS_1'], 'F_VS_3': ph2['F_VS_3']}}
    ck['runtime_seconds'] = int(round(time.time() - t0))
    rec, md5 = write_checkpoint(P('g_vs1_ccleg_checkpoint.json'), ck, mod, pats)
    print('class code:', code)
    print('checkpoint written: g_vs1_ccleg_checkpoint.json md5', md5, 'runtime %ds' % ck['runtime_seconds'])

if __name__ == '__main__':
    main()
