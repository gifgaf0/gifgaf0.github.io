#!/usr/bin/env python3
"""g_vs1_chatleg.py — Gate G-VS1 (Vacuum Selection in the 16-component substrate; the HYP-A1-5 successor): the chat-leg
instrument. Exact arithmetic throughout (Fractions / sympy rationals); numpy integers mod p only for the certified
upper bound of Phase 1 (rank over GF(p) <= rank over Q for an integer matrix, so the GF(p)-nullity is an upper bound
on the Q-nullity; the explicit basis gives the lower bound; equality certifies).

Modes:  python3 g_vs1_chatleg.py preread   -> Phase 0 only; writes g_vs1_chatleg_prereadcheckpoint.json
        python3 g_vs1_chatleg.py run       -> Phases 0-3 + verdict; writes g_vs1_chatleg_checkpoint.json
Every invocation md5-guards the locked memo, the lock record, the T1 list, the scanner, the pinned extract, the schema
and the comparator, and T1-scans itself, the memo, the lock record, the extract, the schema and the comparator under
the gate list (halt on any hit, no override). Class codes VC-1..VC-4 only; no verdict words in this file or its outputs.
"""
import sys, os, json, hashlib, time, math, itertools
from fractions import Fraction as Fr
from itertools import combinations_with_replacement
import numpy as np, sympy as sp

GATE = "G-VS1"; LEG = "chat"
MEMO = "staging_memo_G_VS1_v2.md";        MEMO_MD5 = "58fd02671ea77db63e22afdcc5ee93a0";  MEMO_BYTES = 44709
LOCK = "G_VS1_LOCK_RECORD.md";             LOCK_MD5 = "71711946d1c4abb06fa17402e8d5a6c9";                      LOCK_BYTES = 23071
T1LIST = "tools/t1/T1_forbidden_G_VS1.txt"; T1_MD5 = "324f577d20e2bfba3b594d96c4ca3ba7";  T1_PATTERNS = 31
SCANNER = "tools/t1/t1_scan.py";           SCANNER_MD5 = "6b86290090a8c84f1b1a0a99ec0bf697"
EXTRACT = "inputs/paper_II_3_4_4_and_3_4_7_extract.md"; EXTRACT_MD5 = "940b0bee4b2112e911ae738c3db2bc3d"; EXTRACT_BYTES = 12912
SCHEMA = "g_vs1_schema_v1_0.json";         SCHEMA_MD5 = "4690e07d5a22cc7a1c5d08db39eda3fe"
COMPARATOR = "g_vs1_compare_v1_0.py";      COMPARATOR_MD5 = "69011375d28ec8f63f3ac76383e98321"
ELECTIONS = {f"E-VS-{i}": "a" for i in range(1, 11)}
READINGS = {"Q-VS-1": "carrier of e0 not settled (not the K7 vertices); F-b not live",
            "Q-VS-2": "the kernel couples to the total 16-component density",
            "Q-VS-3": "the vortex sector is the U(1) phase winding (pi_1)",
            "Q-VS-4": "complex conjugation (time reversal) is a symmetry; the potential sector is T-even",
            "Q-VS-5": "'strictly forces' = memo section 3's definition"}
PRIMES = (1048573, 999983)   # both prime, both < 2^20 (products < 2^40, sums over <= 2^12 terms < 2^52: no int64 overflow)

def md5_bytes(b): return hashlib.md5(b).hexdigest()
def md5_file(p): return md5_bytes(open(p, "rb").read())
def halt(msg):
    print("HALT:", msg); sys.exit(2)

# ----------------------------------------------------------------------------- T1 (the frozen scanner's rules re-implemented: case-sensitive substring; contextual numeric rule)
NUMCHARS = set("0123456789.eE+-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
def t1_load(path):
    return [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]
def t1_is_numeric(p): return all(c in NUMCHARS for c in p)
def t1_scan_text(text, pats):
    hits, collisions = [], 0
    for idx, p in enumerate(pats):
        start = 0
        while True:
            k = text.find(p, start)
            if k < 0: break
            if t1_is_numeric(p):
                a, b = k, k + len(p)
                while a > 0 and text[a-1] in NUMCHARS: a -= 1
                while b < len(text) and text[b] in NUMCHARS: b += 1
                if text[a:b].strip() == p.strip():
                    if idx not in hits: hits.append(idx)
                else: collisions += 1
            else:
                if idx not in hits: hits.append(idx)
            start = k + 1
    return hits, collisions

def guards():
    pats = t1_load(T1LIST)
    checks = {
        MEMO: (MEMO_MD5, MEMO_BYTES), LOCK: (LOCK_MD5, LOCK_BYTES), T1LIST: (T1_MD5, None), SCANNER: (SCANNER_MD5, None),
        EXTRACT: (EXTRACT_MD5, EXTRACT_BYTES), SCHEMA: (SCHEMA_MD5, None), COMPARATOR: (COMPARATOR_MD5, None)}
    for path, (want, nbytes) in checks.items():
        if not os.path.exists(path): halt(f"missing {path}")
        got = md5_file(path)
        if got != want: halt(f"md5 mismatch {path}: {got} != {want}")
        if nbytes and os.path.getsize(path) != nbytes: halt(f"byte mismatch {path}")
    if len(pats) != T1_PATTERNS: halt("T1 pattern count")
    rep = {}
    for path in [os.path.abspath(__file__), MEMO, LOCK, EXTRACT, SCHEMA, COMPARATOR]:
        hits, coll = t1_scan_text(open(path, encoding="utf-8").read(), pats)
        rep[os.path.basename(path)] = {"hits": hits, "collisions": coll}
        if hits: halt(f"T1 hit in {path}: indices {hits}")
    return rep

# ----------------------------------------------------------------------------- octonions (Fano lines {i, i+1, i+3} mod 7, the §3.4-SIGNPHI convention)
LINES = [((i-1) % 7 + 1, i % 7 + 1, (i+2) % 7 + 1) for i in range(1, 8)]
LINESETS = {frozenset(l) for l in LINES}
MULT = {}
for (a, b, c) in LINES:
    for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
        MULT[(x, y)] = (1, z); MULT[(y, x)] = (-1, z)
def omul(p, q, zero=Fr(0)):
    r = [zero] * 8
    for i in range(8):
        pi = p[i]
        if pi == 0: continue
        for j in range(8):
            qj = q[j]
            if qj == 0: continue
            if i == 0: r[j] = r[j] + pi * qj
            elif j == 0: r[i] = r[i] + pi * qj
            elif i == j: r[0] = r[0] - pi * qj
            else:
                s, k = MULT[(i, j)]; r[k] = r[k] + (pi * qj if s == 1 else -(pi * qj))
    return r
def unit(i):
    v = [Fr(0)] * 8; v[i] = Fr(1); return v
def mat_apply(M, v): return [sum((M[i][j] * v[j] for j in range(8)), Fr(0)) for i in range(8)]
def flat(M): return [M[i][j] for i in range(len(M)) for j in range(len(M[0]))]
def bracket(A, B):
    n = len(A)
    return [[sum((A[i][k] * B[k][j] - B[i][k] * A[k][j] for k in range(n)), Fr(0)) for j in range(n)] for i in range(n)]
def Q(x): return sp.Rational(x.numerator, x.denominator)
def rank_Q(vectors):
    if not vectors: return 0
    return int(sp.Matrix([[Q(x) for x in v] for v in vectors]).rank())
def nullspace_Q(rows, ncols):
    if not rows: return [[Fr(1) if i == j else Fr(0) for i in range(ncols)] for j in range(ncols)]
    A = sp.Matrix([[Q(x) for x in r] for r in rows])
    return [[Fr(int(sp.fraction(x)[0]), int(sp.fraction(x)[1])) for x in v] for v in A.nullspace()]
def combine(coeffs, mats):
    return [[sum((c * M[r][s] for c, M in zip(coeffs, mats)), Fr(0)) for s in range(8)] for r in range(8)]
def derivation_algebra():
    syms = sp.symbols('d0:21'); D = sp.zeros(7, 7); t = 0
    for i in range(7):
        for j in range(i+1, 7):
            D[i, j] = syms[t]; D[j, i] = -syms[t]; t += 1
    def Dapply(v):
        out = [sp.Integer(0)] * 8
        for i in range(1, 8):
            if v[i] != 0:
                for j in range(1, 8): out[j] += D[j-1, i-1] * v[i]
        return out
    def su(i): return [sp.Integer(1) if k == i else sp.Integer(0) for k in range(8)]
    eqs = []
    for i in range(1, 8):
        for j in range(1, 8):
            ei, ej = su(i), su(j)
            lhs = Dapply(omul(ei, ej, sp.Integer(0)))
            rhs = [sp.Integer(0)] * 8
            for n_, val in enumerate(omul(Dapply(ei), ej, sp.Integer(0))): rhs[n_] += val
            for n_, val in enumerate(omul(ei, Dapply(ej), sp.Integer(0))): rhs[n_] += val
            for n_ in range(8):
                e = sp.expand(lhs[n_] - rhs[n_])
                if e != 0: eqs.append(e)
    A = sp.Matrix([[sp.Poly(e, *syms).coeff_monomial(s) for s in syms] for e in eqs])
    gens = []
    for v in A.nullspace():
        den = sp.ilcm(*[sp.fraction(x)[1] for x in v])
        M = [[Fr(0)] * 8 for _ in range(8)]; t = 0
        for i in range(7):
            for j in range(i+1, 7):
                val = Fr(int(v[t] * den)); M[i+1][j+1] = val; M[j+1][i+1] = -val; t += 1
        gens.append(M)
    return gens
def is_derivation(M):
    for i in range(8):
        for j in range(8):
            ei, ej = unit(i), unit(j)
            lhs = mat_apply(M, omul(ei, ej))
            rhs = [a + b for a, b in zip(omul(mat_apply(M, ei), ej), omul(ei, mat_apply(M, ej)))]
            if lhs != rhs: return False
    return True
def is_automorphism(P):
    for i in range(8):
        for j in range(8):
            ei, ej = unit(i), unit(j)
            if mat_apply(P, omul(ei, ej)) != omul(mat_apply(P, ei), mat_apply(P, ej)): return False
    return True
def subalgebra_from_conditions(g2, rows_fn):
    """rows_fn(D) -> list of Fraction conditions linear in D (each a number that must vanish); returns basis (8x8) of the solution subalgebra."""
    cols = [rows_fn(D) for D in g2]
    rows = [[cols[j][i] for j in range(len(g2))] for i in range(len(cols[0]))]
    return [combine(c, g2) for c in nullspace_Q(rows, len(g2))]
def pointwise_stabilizer(g2, vecs):
    return subalgebra_from_conditions(g2, lambda D: [x for v in vecs for x in mat_apply(D, v)])
def su2_index(k_basis):
    """Dynkin index of a 3-dim simple subalgebra k of g2 relative to the long root: 2 tr_7(A^2) / tr_{ad_k}(ad_k(A)^2), scale-free."""
    A = k_basis[0]
    tr7 = sum(sum(A[i][k] * A[k][i] for k in range(1, 8)) for i in range(1, 8))
    M = sp.Matrix([[Q(x) for x in flat(B)] for B in k_basis]).T
    ad = []
    for B in k_basis:
        target = sp.Matrix([Q(x) for x in flat(bracket(A, B))])
        sol = M.solve_least_squares(target)
        if (M * sol - target).norm() != 0: halt("ad_k: bracket not in the subalgebra")
        ad.append([Fr(int(sp.fraction(s)[0]), int(sp.fraction(s)[1])) for s in sol])
    n = len(k_basis)
    trad = sum(ad[j][i] * ad[i][j] for i in range(n) for j in range(n))
    if trad == 0: halt("degenerate su(2) trace")
    return 2 * tr7 / trad

# ----------------------------------------------------------------------------- polynomials in (psi_0..7, psibar_0..7): dict exponent-tuple(16) -> Fraction
NV = 16
def pmul(P, Qp):
    R = {}
    for ea, ca in P.items():
        for eb, cb in Qp.items():
            e = tuple(x + y for x, y in zip(ea, eb)); R[e] = R.get(e, Fr(0)) + ca * cb
    return {e: c for e, c in R.items() if c != 0}
def padd(P, Qp, s=Fr(1)):
    R = dict(P)
    for e, c in Qp.items(): R[e] = R.get(e, Fr(0)) + s * c
    return {e: c for e, c in R.items() if c != 0}
def pscale(P, s): return {e: c * s for e, c in P.items() if c * s != 0}
def var(k):
    e = [0] * NV; e[k] = 1; return {tuple(e): Fr(1)}
def psi(k): return var(k)
def psibar(k): return var(8 + k)
def act_vf(Mpsi, Mbar, P):
    R = {}
    for e, c in P.items():
        for j in range(8):
            if e[j] > 0:
                for k in range(8):
                    m = Mpsi[j][k]
                    if m == 0: continue
                    ne = list(e); ne[j] -= 1; ne[k] += 1; ne = tuple(ne); R[ne] = R.get(ne, Fr(0)) + c * e[j] * m
            if e[8 + j] > 0:
                for k in range(8):
                    m = Mbar[j][k]
                    if m == 0: continue
                    ne = list(e); ne[8 + j] -= 1; ne[8 + k] += 1; ne = tuple(ne); R[ne] = R.get(ne, Fr(0)) + c * e[8 + j] * m
    return {e: c for e, c in R.items() if c != 0}
def T_swap(P): return {tuple(list(e[8:]) + list(e[:8])): c for e, c in P.items()}
def T_parity(P):
    if T_swap(P) == P: return 1
    if T_swap(P) == pscale(P, Fr(-1)): return -1
    return 0
def monomials_bidegree(p, q, idx):
    out = []
    for A in combinations_with_replacement(idx, p):
        for B in combinations_with_replacement(idx, q):
            e = [0] * NV
            for a in A: e[a] += 1
            for b in B: e[8 + b] += 1
            out.append(tuple(e))
    return out
def poly_vector(P, index):
    v = [Fr(0)] * len(index)
    for e, c in P.items(): v[index[e]] = c
    return v
def annihilated(P, pairs): return all(not act_vf(Mp, Mb, P) for (Mp, Mb) in pairs)
def nullspace_mod_p(M, p):
    M = (M % p).astype(np.int64); r, c = M.shape; pivots = []; row = 0
    for col in range(c):
        if row >= r: break
        nz = np.nonzero(M[row:, col])[0]
        if nz.size == 0: continue
        piv = row + int(nz[0])
        if piv != row: M[[row, piv]] = M[[piv, row]]
        inv = pow(int(M[row, col]), p - 2, p)
        M[row] = (M[row] * inv) % p
        others = np.nonzero(M[:, col])[0]; others = others[others != row]
        if others.size: M[others] = (M[others] - np.outer(M[others, col], M[row])) % p
        pivots.append(col); row += 1
    pset = set(pivots); free = [j for j in range(c) if j not in pset]
    N = np.zeros((c, len(free)), dtype=np.int64)
    for k, f in enumerate(free):
        N[f, k] = 1
        for i, pc in enumerate(pivots): N[pc, k] = (-M[i, f]) % p
    return N
def common_kernel_dim_mod_p(op_matrices, p):
    n = op_matrices[0].shape[0]; B = np.eye(n, dtype=np.int64)
    for M in op_matrices:
        K = nullspace_mod_p(((M % p) @ B) % p, p); B = (B @ K) % p
        if B.shape[1] == 0: return 0
    return int(B.shape[1])
def op_matrix(Mpsi, Mbar, basis, index):
    n = len(basis); A = np.zeros((n, n), dtype=np.int64)
    for j, e in enumerate(basis):
        for ee, c in act_vf(Mpsi, Mbar, {e: Fr(1)}).items():
            if c.denominator != 1: halt("non-integer generator entry")
            A[index[ee], j] = int(c)
    return A
def certified_dim(pairs, explicit, p_, q_, idx):
    """pairs: list of (Mpsi, Mbar) integer generator matrices; explicit: dict name -> polynomial (candidate invariants).
    Returns the certificate dict: explicit annihilation flags, exact lower bound (rank over Q), GF(p) upper bounds, certified value."""
    basis = monomials_bidegree(p_, q_, idx); index = {e: i for i, e in enumerate(basis)}
    ann = {name: annihilated(P, pairs) for name, P in explicit.items()}
    vecs = [poly_vector(P, index) for name, P in explicit.items() if ann[name]]
    lower = rank_Q(vecs)
    ops = [op_matrix(Mp, Mb, basis, index) for (Mp, Mb) in pairs]
    ups = {str(p): common_kernel_dim_mod_p(ops, p) for p in PRIMES}
    upper = min(ups.values())
    cert = lower if lower == upper else None
    Tev = sum(1 for name, P in explicit.items() if ann[name] and T_parity(P) == 1) if cert is not None else None
    return dict(n_monomials=len(basis), explicit_annihilated=ann, lower_bound_rank_Q=lower, upper_bounds_mod_p=ups,
                certified_dim=cert, T_even_dim=Tev, bidegree=[p_, q_])

# ----------------------------------------------------------------------------- Weyl integration formula
def lp_mul(P, Qp):
    R = {}
    for ea, ca in P.items():
        for eb, cb in Qp.items():
            e = tuple(x + y for x, y in zip(ea, eb)); R[e] = R.get(e, Fr(0)) + ca * cb
    return {e: c for e, c in R.items() if c != 0}
def lp_add(P, Qp, s=Fr(1)):
    R = dict(P)
    for e, c in Qp.items(): R[e] = R.get(e, Fr(0)) + s * c
    return {e: c for e, c in R.items() if c != 0}
def weyl_invariant_dim(weights, roots, order_W, d):
    r = len(weights[0]); one = {tuple([0] * r): Fr(1)}
    def pk(k):
        P = {}
        for w in weights:
            e = tuple(k * x for x in w); P[e] = P.get(e, Fr(0)) + 1
        return P
    h = [one]
    for dd in range(1, d + 1):
        acc = {}
        for k in range(1, dd + 1): acc = lp_add(acc, lp_mul(pk(k), h[dd - k]))
        h.append({e: c / dd for e, c in acc.items()})
    P = dict(one)
    for a in roots: P = lp_mul(P, lp_add(one, {tuple(a): Fr(1)}, Fr(-1)))
    ct = lp_mul(h[d], P).get(tuple([0] * r), Fr(0)) / order_W
    if ct.denominator != 1: halt("Weyl constant term not integral")
    return int(ct)
W7_G2 = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]
ROOTS_G2 = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (2, 1), (-2, -1), (1, 2), (-1, -2)]
W7_B3 = [(0, 0, 0)] + [tuple(s if k == i else 0 for k in range(3)) for i in range(3) for s in (1, -1)]
ROOTS_B3 = [tuple(s if k == i else 0 for k in range(3)) for i in range(3) for s in (1, -1)]
for i_, j_ in itertools.combinations(range(3), 2):
    for s_ in (1, -1):
        for t_ in (1, -1):
            v_ = [0, 0, 0]; v_[i_] = s_; v_[j_] = t_; ROOTS_B3.append(tuple(v_))
def weyl_table(w_int, roots, orderW, with_singlet, degrees=(2, 4, 6)):
    r = len(w_int[0]); zero = tuple([0] * r)
    base = ([zero] if with_singlet else []) + list(w_int)
    weights = [w + (1,) for w in base] + [w + (-1,) for w in base]
    rts = [a + (0,) for a in roots]
    return {str(d): weyl_invariant_dim(weights, rts, orderW, d) for d in degrees}

# ----------------------------------------------------------------------------- real 16-vectors, strata, stabilizers, homotopy bookkeeping
def cvec(re, im): return [Fr(a) for a in re] + [Fr(b) for b in im]
def D_on_real16(D, w): return mat_apply(D, w[:8]) + mat_apply(D, w[8:])
def J_on_real16(w): return [-b for b in w[8:]] + list(w[:8])
def apply_elt(P, w): return mat_apply(P, w[:8]) + mat_apply(P, w[8:])
def phase_mult(w, re, im):
    x, y = w[:8], w[8:]
    return [re * a - im * b for a, b in zip(x, y)] + [im * a + re * b for a, b in zip(x, y)]
def invariants_of(w):
    x, y = w[:8], w[8:]
    rho0 = x[0] ** 2 + y[0] ** 2
    u, v = x[1:], y[1:]
    uu = sum(a * a for a in u); vv = sum(b * b for b in v); uv = sum(a * b for a, b in zip(u, v))
    N = uu + vv; S_re, S_im = uu - vv, 2 * uv
    p2_re, p2_im = x[0] ** 2 - y[0] ** 2, 2 * x[0] * y[0]
    t_re = p2_re * S_re + p2_im * S_im; t_im = p2_im * S_re - p2_re * S_im
    tot = rho0 + N
    s2 = S_re ** 2 + S_im ** 2
    return dict(rho0=rho0, N=N, S_re=S_re, S_im=S_im, s2=s2, t_re=t_re, t_im=t_im, total=tot,
                gram_scalar=(uu == vv and uv == 0), rank_uv=(rank_Q([u, v]) if (any(u) or any(v)) else 0),
                rho_norm=rho0 / tot, s2_norm=s2 / tot ** 2, t_norm=t_re / tot ** 2)
def stabilizer_algebra(gens, w):
    cols = [D_on_real16(D, w) for D in gens] + [J_on_real16(w)]
    ncol = len(cols); rows = [[cols[j][i] for j in range(ncol)] for i in range(16)]
    ns = nullspace_Q(rows, ncol)
    k_rows = rows + [[Fr(0)] * (ncol - 1) + [Fr(1)]]
    ks = nullspace_Q(k_rows, ncol)
    return ns, ks
def orbit_rank(gens, vectors):
    imgs = []
    for D in gens:
        row = []
        for v in vectors: row += mat_apply(D, v)
        imgs.append(row)
    return rank_Q(imgs)
def sigma_line(line):
    keep = {0} | set(line)
    return [[(Fr(1) if (i == j and i in keep) else (Fr(-1) if i == j else Fr(0))) for j in range(8)] for i in range(8)]
def perp_line(u_idx):
    """a Fano line disjoint from the given imaginary indices (for the sigma witness)."""
    for l in LINES:
        if not (set(l) & set(u_idx)): return l
    return None
ADOPTED = {   # pi_1 of the G2-orbit types (G2 connected and simply connected => pi_0(Stab) = pi_1(orbit)); textbook facts, cited in the lock record
    ("G2", 0): ("point", "0"), ("G2", 6): ("S6 = G2/SU(3)", "0"), ("G2", 11): ("V2(R7) = G2/SU(2)", "0"),
    ("SU2", 0): ("point", "0"), ("SU2", 2): ("S2 = SU(2)/U(1)", "0"), ("SU2", 3): ("V2(R3) = SO(3) = SU(2)/{+-1}", "Z2"),
}
def homotopy_bookkeeping(G, rank_orbit, dim_k, P_kind, m, k_simply_connected, index, k_has_su2, K_is_Gint, d=None):
    """pi_1, pi_2, pi_3 of V = (G x U(1))/H from the exact sequences (G simply connected; pi_1(G x U(1)) = Z from the U(1)).
    P_kind: 'finite' (allowed phases form Z_m) or 'U1'. K = Stab_G(psi); pi_0(K) = pi_1(G-orbit) (adopted table).
    Returns dict with pi1 (as a string), elementary U(1) winding, pi2, pi3, and the reasoning keys."""
    orbit_name, pi1_orbit = ADOPTED[(G, rank_orbit)]
    K_connected = (pi1_orbit == "0")
    out = dict(orbit=orbit_name, pi0_K=("1" if K_connected else pi1_orbit), K_connected=K_connected)
    if P_kind == "finite":
        if not K_connected: halt("finite phase group with disconnected K: not encoded for this gate")
        out["pi0_H"] = f"Z{m}" if m > 1 else "1"
        out["pi1"] = "Z"; out["elementary_winding"] = f"2pi/{m}" if m > 1 else "2pi"
        out["pi1_reason"] = "0 -> Z -> pi1(V) -> Z_m -> 0 with the m-th power of the lift equal to the U(1) generator (K connected): pi1 = Z"
        out["pi2"] = "0" if k_simply_connected else "Z"   # pi2(V) = pi1(K^0) (the map to pi1(G) is zero: K^0 in G x {1}, pi1(G) = 0)
    else:
        dd = d if d is not None else (1 if K_connected else 2)
        out["d"] = dd; out["pi0_H"] = "1"
        out["pi1"] = "0" if dd == 1 else f"Z{dd}"; out["elementary_winding"] = "none"
        out["pi1_reason"] = "H^0 -> U(1) surjective with kernel K cap H^0; image of pi1(H^0) in pi1(G x U(1)) = Z is dZ, d = |pi0(K cap H^0)|; pi1(V) = Z/dZ"
        out["pi2"] = "0" if k_simply_connected else "Z"
    if K_is_Gint: out["pi3"] = "0"; out["pi3_reason"] = "K = G: pi3(G) -> pi3(G) is the identity; coker 0"
    elif not k_has_su2: out["pi3"] = "Z"; out["pi3_reason"] = "k contains no su(2): pi3(H^0) = 0; pi3(V) = pi3(G) = Z"
    else:
        out["pi3"] = "0" if index == 1 else f"Z{index}"; out["pi3_reason"] = f"pi3(V) = coker(pi3(H^0) -> pi3(G)) = Z/(Dynkin index {index})"
    return out

# ----------------------------------------------------------------------------- orbit-space minimization
def stratum_label(rho, s, t):
    if rho == 1: return "R"
    if rho == 0: return "P7" if s == 1 else ("F7" if s == 0 else "I7")
    N = 1 - rho
    if s == N: return "MP+" if t > 0 else ("MP-" if t < 0 else "MP0")
    if s == 0: return "MF"
    return "MI+" if t > 0 else ("MI-" if t < 0 else "MI0")
def minimize_orbit_space(A, B, c4, c5):
    A, B, c4, c5 = Fr(A), Fr(B), Fr(c4), Fr(c5)
    sg = -1 if c5 > 0 else (1 if c5 < 0 else 0); ac5 = abs(c5)
    def f(rho, s): return A * rho * rho + B * rho + c4 * s * s - ac5 * rho * s
    cands = {(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1))}
    if A != 0:
        r = -B / (2 * A)
        if 0 < r < 1: cands.add((r, Fr(0)))
    a2 = A + c4 + ac5; a1 = B - 2 * c4 - ac5
    if a2 != 0:
        r = -a1 / (2 * a2)
        if 0 < r < 1: cands.add((r, 1 - r))
    det = 4 * A * c4 - ac5 * ac5
    if det != 0:
        r = (-B * 2 * c4) / det; s = (ac5 * (-B)) / det
        if 2 * A * r - ac5 * s == -B and -ac5 * r + 2 * c4 * s == 0 and 0 < r < 1 and 0 < s < 1 - r: cands.add((r, s))
    vals = {c: f(*c) for c in cands}; Emin = min(vals.values())
    mins = []
    for (r, s), v in sorted(vals.items()):
        if v == Emin:
            t = sg * r * s
            mins.append(dict(rho=str(r), s=str(s), t=str(t), stratum=stratum_label(r, s, t), t_free=bool(c5 == 0 and r * s != 0)))
    faces = []
    if A == 0 and B == 0 and Emin == 0: faces.append("edge s=0: R, MF, F7")
    if c4 == 0 and Emin == 0: faces.append("edge rho=0: P7, I7, F7")
    if a2 == 0 and a1 == 0 and c4 == Emin: faces.append("edge s=1-rho: R, MP, P7")
    # a rank-1 (perfect-square) q = f - Emin whose zero line crosses the interior: a segment of minimizers
    Hq = [[A, -ac5 / 2, B / 2], [-ac5 / 2, c4, Fr(0)], [B / 2, Fr(0), -Emin]]
    rk = rank_Q(Hq)
    if rk == 1 and not (A == 0 and B == 0 and c4 == 0 and c5 == 0):
        # q = k (alpha rho + beta s + gamma)^2 : read the line from a nonzero row
        row = next(r for r in Hq if any(r))
        alpha, beta, gamma = row
        # intersect the line with the triangle: candidate endpoints on the three edges
        pts = set()
        if beta != 0:
            for r in (Fr(0), Fr(1)):
                s = -(alpha * r + gamma) / beta
                if 0 <= s <= 1 - r: pts.add((r, s))
        if alpha != 0:
            for s in (Fr(0),):
                r = -(beta * s + gamma) / alpha
                if 0 <= r <= 1: pts.add((r, s))
        if alpha != beta:
            r = -(beta + gamma) / (alpha - beta)      # on s = 1 - r
            if 0 <= r <= 1: pts.add((r, 1 - r))
        if len(pts) >= 2:
            (r1, s1), (r2, s2) = sorted(pts)[0], sorted(pts)[-1]
            rm, sm = (r1 + r2) / 2, (s1 + s2) / 2
            on_edge = (r1 == r2 == 0) or (s1 == s2 == 0) or (s1 == 1 - r1 and s2 == 1 - r2)
            if f(rm, sm) == Emin and (r1, s1) != (r2, s2) and not on_edge:
                tm = sg * rm * sm
                faces.append(f"interior segment from ({r1},{s1}) to ({r2},{s2}): strata {stratum_label(r1, s1, sg * r1 * s1)}, {stratum_label(rm, sm, tm)}, {stratum_label(r2, s2, sg * r2 * s2)}")
    if A == 0 and B == 0 and c4 == 0 and c5 == 0: faces = ["whole orbit space: P0"]
    return str(Emin), mins, faces
def effective_params(mu0, mu7, c1, c2, c3, c4, c5):
    """V = -mu0 rho0 - mu7 N + c1 rho0^2 + c2 rho0 N + c3 N^2 + c4 |S|^2 + c5 Re(psi0^2 Sbar) on |psi|^2 = 1 (N = 1 - rho0):
    V = A rho0^2 + B rho0 + c4 s^2 + c5 t + const."""
    A = Fr(c1) - Fr(c2) + Fr(c3); B = (Fr(mu7) - Fr(mu0)) + Fr(c2) - 2 * Fr(c3)
    return A, B, Fr(c4), Fr(c5)

# ----------------------------------------------------------------------------- polynomial-valued octonions (the F-a forms)
def poly_omul(X, Y):
    r = [{} for _ in range(8)]
    for i in range(8):
        if not X[i]: continue
        for j in range(8):
            if not Y[j]: continue
            prod = pmul(X[i], Y[j])
            if i == 0: r[j] = padd(r[j], prod)
            elif j == 0: r[i] = padd(r[i], prod)
            elif i == j: r[0] = padd(r[0], prod, Fr(-1))
            else:
                s_, k = MULT[(i, j)]; r[k] = padd(r[k], prod, Fr(s_))
    return r
def poly_oconj(X): return [X[0]] + [pscale(c, Fr(-1)) for c in X[1:]]
def poly_cconj(X): return [T_swap(c) for c in X]
def hermitian_norm_sq(X):
    out = {}
    for c in X: out = padd(out, pmul(c, T_swap(c)))
    return out
def bilinear_norm(X):
    out = {}
    for c in X: out = padd(out, pmul(c, c))
    return out
def expand_in_basis(F, basis):
    names = list(basis); mons = set()
    for P_ in list(basis.values()) + [F]: mons |= set(P_)
    mons = sorted(mons)
    M = sp.Matrix([[Q(basis[n].get(m, Fr(0))) for n in names] for m in mons])
    b = sp.Matrix([Q(F.get(m, Fr(0))) for m in mons])
    sol = M.solve_least_squares(b); res = (M * sol - b).norm()
    return {n: str(s) for n, s in zip(names, sol)}, (res == 0)

# ============================================================================= PHASES
def phase0(g2):
    P = {}
    # 0a — the derivation algebra
    vecs = [flat(M) for M in g2]; r0 = rank_Q(vecs)
    closure = all(rank_Q(vecs + [flat(bracket(g2[i], g2[j]))]) == r0 for i in range(len(g2)) for j in range(i + 1, len(g2)))
    e = lambda i: unit(i)
    su2_long = pointwise_stabilizer(g2, [e(1), e(2), e(4)])
    so4 = subalgebra_from_conditions(g2, lambda D: [D[b][a] for a in (1, 2, 4) for b in (3, 5, 6, 7)])
    # su2_short = centralizer of su2_long inside so4
    rows = []
    for L in su2_long:
        cols = [flat(bracket(Xj, L)) for Xj in so4]
        for r in range(64): rows.append([cols[j][r] for j in range(len(so4))])
    su2_short = [combine(c, so4) for c in nullspace_Q(rows, len(so4))]
    P["0a"] = dict(g2_dim=len(g2), rank=r0, all_derivations=all(is_derivation(M) for M in g2),
                   all_antisymmetric=all(all(M[i][j] == -M[j][i] for i in range(8) for j in range(8)) for M in g2),
                   closure=closure, max_abs_entry=str(max(abs(x) for M in g2 for x in flat(M))),
                   dim_so4_H124=len(so4), dim_su2_long=len(su2_long), dim_su2_short=len(su2_short),
                   index_su2_long=str(su2_index(su2_long)), index_su2_short=str(su2_index(su2_short)),
                   PASS=(len(g2) == 14 and closure and len(su2_long) == 3 and len(su2_short) == 3 and su2_index(su2_long) == 1 and su2_index(su2_short) == 3))
    # 0b — commutants: the 7 irreducible (dim 1); 1+7 (dim 2)
    def commutant_dim(gens, idx):
        n = len(idx); syms = sp.symbols('x0:%d' % (n * n)); X = sp.Matrix(n, n, syms); eqs = []
        for M in gens:
            Mm = sp.Matrix([[Q(M[i][j]) for j in idx] for i in idx]); C = X * Mm - Mm * X
            eqs += [c for c in C if c != 0]
        Am = sp.Matrix([[sp.Poly(ee, *syms).coeff_monomial(s) for s in syms] for ee in eqs])
        return n * n - int(Am.rank())
    c7, c8 = commutant_dim(g2, list(range(1, 8))), commutant_dim(g2, list(range(8)))
    P["0b"] = dict(commutant_dim_on_7=c7, commutant_dim_on_1plus7=c8, PASS=(c7 == 1 and c8 == 2))
    # 0c — the O(16) point of record: U(8) certified counts (sandwich O(16) ⊂ ... ⊃ U(8)) and transitivity on S15
    E = lambda j, k: [[Fr(1) if (r == j and s == k) else Fr(0) for s in range(8)] for r in range(8)]
    gl8_pairs = [(E(j, k), [[-E(j, k)[s][r] for s in range(8)] for r in range(8)]) for j in range(8) for k in range(8)]
    rho0 = pmul(psi(0), psibar(0)); N = {}; S = {}; Sb = {}
    for a in range(1, 8):
        N = padd(N, pmul(psi(a), psibar(a))); S = padd(S, pmul(psi(a), psi(a))); Sb = padd(Sb, pmul(psibar(a), psibar(a)))
    Ntot = padd(rho0, N)
    u8_2 = certified_dim(gl8_pairs, {"Ntot": Ntot}, 1, 1, list(range(8)))
    u8_4 = certified_dim(gl8_pairs, {"Ntot^2": pmul(Ntot, Ntot)}, 2, 2, list(range(8)))
    so16 = []
    for i in range(16):
        for j in range(i + 1, 16):
            X = [[Fr(0)] * 16 for _ in range(16)]; X[i][j] = Fr(1); X[j][i] = Fr(-1); so16.append(X)
    w = [Fr(1)] + [Fr(0)] * 15
    rank_s15 = rank_Q([[sum((X[i][j] * w[j] for j in range(16)), Fr(0)) for i in range(16)] for X in so16])
    P["0c"] = dict(u8_deg2=u8_2, u8_deg4=u8_4, o16_deg2=1, o16_deg4=1,
                   o16_argument="O(16) ⊃ U(8): Inv_O16 ⊂ Inv_U8 = span(Ntot^k), and Ntot^k is O(16)-invariant; so dim = 1 at degrees 2 and 4",
                   so16_orbit_rank_at_unit_vector=rank_s15, dim_S15=15, V_of_record="S15 (the accidental sphere)", pi1_S15="0 (adopted: spheres S^n, n>=2, are simply connected)",
                   PASS=(u8_2["certified_dim"] == 1 and u8_4["certified_dim"] == 1 and rank_s15 == 15))
    # 0d — homotopy bookkeeping controls: spin-1 (SU(2) x U(1) on C^3 through SO(3)); binary tetrahedral; pi4(S2) chain
    def L3(i, j):
        X = [[Fr(0)] * 3 for _ in range(3)]; X[i][j] = Fr(1); X[j][i] = Fr(-1); return X
    so3 = [L3(0, 1), L3(1, 2), L3(0, 2)]
    def ctrl_stab(wv):   # wv: real 6-vector (x, y) in R^3 + i R^3
        cols = [[sum((D[i][j] * wv[j] for j in range(3)), Fr(0)) for i in range(3)] + [sum((D[i][j] * wv[3 + j] for j in range(3)), Fr(0)) for i in range(3)] for D in so3]
        cols.append([-b for b in wv[3:]] + list(wv[:3]))
        rows = [[cols[j][i] for j in range(4)] for i in range(6)]
        ns = nullspace_Q(rows, 4); ks = nullspace_Q(rows + [[Fr(0), Fr(0), Fr(0), Fr(1)]], 4)
        return len(ns), len(ks), any(v[3] != 0 for v in ns)
    def ctrl_rank(vectors):
        return rank_Q([[sum((D[i][j] * v[j] for j in range(3)), Fr(0)) for v in vectors for i in range(3)] for D in so3])
    n3 = [Fr(1), Fr(0), Fr(0)]; e2 = [Fr(0), Fr(1), Fr(0)]
    polar = n3 + [Fr(0)] * 3; ferro = n3 + e2
    dh_p, dk_p, tp = ctrl_stab(polar); dh_f, dk_f, tf = ctrl_stab(ferro)
    Rpi = [[Fr(-1), Fr(0), Fr(0)], [Fr(0), Fr(1), Fr(0)], [Fr(0), Fr(0), Fr(-1)]]   # rotation by pi about e2: n3 -> -n3
    det = Rpi[0][0] * Rpi[1][1] * Rpi[2][2]
    wit_ok = (det == 1 and all(sum(Rpi[i][k] * Rpi[j][k] for k in range(3)) == (1 if i == j else 0) for i in range(3) for j in range(3))
              and [sum((Rpi[i][j] * n3[j] for j in range(3)), Fr(0)) for i in range(3)] == [-x for x in n3])
    rank_pol, rank_fer = ctrl_rank([n3]), ctrl_rank([n3, e2])
    hb_polar = homotopy_bookkeeping("SU2", rank_pol, dk_p, "finite", 2, k_simply_connected=False, index=None, k_has_su2=False, K_is_Gint=False)
    hb_ferro = homotopy_bookkeeping("SU2", rank_fer, dk_f, "U1", None, k_simply_connected=True, index=None, k_has_su2=False, K_is_Gint=False, d=2)
    # the universal-cover subtlety for ferro: K~ = {+-1} (two elements, both in H~^0); d = |pi0(K~ cap H~^0)| = 2 — stated, with the Z2 of the adopted table
    # binary tetrahedral group as unit quaternions (24 elements), exact closure
    half = Fr(1, 2); T24 = set()
    for s in itertools.product((1, -1), repeat=4): T24.add(tuple(half * x for x in s))
    for i in range(4):
        for s in (1, -1):
            q = [Fr(0)] * 4; q[i] = Fr(s); T24.add(tuple(q))
    def qmul(a, b):
        a0, a1, a2, a3 = a; b0, b1, b2, b3 = b
        return (a0*b0 - a1*b1 - a2*b2 - a3*b3, a0*b1 + a1*b0 + a2*b3 - a3*b2, a0*b2 - a1*b3 + a2*b0 + a3*b1, a0*b3 + a1*b2 - a2*b1 + a3*b0)
    closed = all(qmul(a, b) in T24 for a in T24 for b in T24)
    weyl_spin1 = {str(d): weyl_invariant_dim([(w, 1) for w in (0, 1, -1)] + [(w, -1) for w in (0, 1, -1)], [(1, 0), (-1, 0)], 2, d) for d in (2, 4, 6)}
    P["0d"] = dict(spin1_polar=dict(dim_h=dh_p, dim_k=dk_p, phase_in_h=tp, orbit_rank=rank_pol, m=2, witness_rotation_pi_perp=wit_ok, **hb_polar),
                   spin1_ferro=dict(dim_h=dh_f, dim_k=dk_f, phase_in_h=tf, orbit_rank=rank_fer, d_reason="K~ = Stab_SU(2)(u,v) = {+1, -1}, both in the identity component H~^0 (the lifted U(1) passes through -1): d = |pi0(K~ cap H~^0)| = 2", **hb_ferro),
                   textbook=dict(polar="pi1 = Z with half-quantum vortices, pi2 = Z, pi3 = Z", ferro="V = SO(3): pi1 = Z2, pi2 = 0, pi3 = Z"),
                   weyl_spin1_invariant_dims=weyl_spin1, binary_tetrahedral=dict(order=len(T24), closed=closed, pi1_SO3_mod_T="2T, order 24 (SU(2) -> SO(3)/T is the universal cover with fiber 2T)"),
                   pi4_S2="Z2 (adopted chain: Hopf fibration U(1) -> S3 -> S2 gives pi4(S2) = pi4(S3) since pi3(U(1)) = pi4(U(1)) = 0; pi4(S3) = Z2)",
                   PASS=(hb_polar["pi1"] == "Z" and hb_polar["elementary_winding"] == "2pi/2" and hb_polar["pi2"] == "Z" and hb_polar["pi3"] == "Z"
                         and hb_ferro["pi1"] == "Z2" and hb_ferro["pi2"] == "0" and hb_ferro["pi3"] == "Z" and wit_ok and tp is False and tf is True
                         and len(T24) == 24 and closed and weyl_spin1 == {"2": 1, "4": 2, "6": 2}))
    # 0e — transitivity ranks
    ranks = dict(e0=orbit_rank(g2, [e(0)]), e1=orbit_rank(g2, [e(1)]), pair_e1_e2=orbit_rank(g2, [e(1), e(2)]),
                 associative_triple_e1_e2_e4=orbit_rank(g2, [e(1), e(2), e(4)]), generic_triple_e1_e2_e3=orbit_rank(g2, [e(1), e(2), e(3)]))
    P["0e"] = dict(**ranks, dim_S6=6, dim_V2R7=11, dim_V3R7=15, dim_g2=14,
                   reading="rank 6 at a unit vector and 11 at an orthonormal pair = the dimensions of S6 and V2(R7): the orbits are open and compact, hence all of these connected spaces (transitivity); rank 14 < 15 at a generic triple: the orbit of a triple is a hypersurface, the invariant being phi(u,v,w)",
                   PASS=(ranks["e0"] == 0 and ranks["e1"] == 6 and ranks["pair_e1_e2"] == 11 and ranks["generic_triple_e1_e2_e3"] == 14 and ranks["associative_triple_e1_e2_e4"] == 11))
    # 0f — the su(3) discriminating control
    su3 = pointwise_stabilizer(g2, [e(7)])
    pairs_su3 = [(M, M) for M in su3]
    inv_su3 = {"rho0": rho0, "rho7": pmul(psi(7), psibar(7)), "N_minus_rho7": padd(N, pmul(psi(7), psibar(7)), Fr(-1))}
    ann = {k: annihilated(v, pairs_su3) for k, v in inv_su3.items()}
    lower = rank_Q([poly_vector(v, {m: i for i, m in enumerate(monomials_bidegree(1, 1, list(range(8))))}) for v in inv_su3.values()])
    P["0f"] = dict(su3_dim=len(su3), explicit_su3_u1_deg2_invariants=list(inv_su3), annihilated=ann, lower_bound_deg2=lower, g2_u1_deg2=2,
                   PASS=(len(su3) == 8 and all(ann.values()) and lower == 3))
    P["all_pass"] = all(P[k]["PASS"] for k in ("0a", "0b", "0c", "0d", "0e", "0f"))
    return P, dict(su2_long=su2_long, so4=so4, su3=su3, rho0=rho0, N=N, S=S, Sb=Sb, Ntot=Ntot)

def phase1(g2, aux):
    rho0, N, S, Sb = aux["rho0"], aux["N"], aux["S"], aux["Sb"]
    Re = pscale(padd(pmul(pmul(psi(0), psi(0)), Sb), pmul(pmul(psibar(0), psibar(0)), S)), Fr(1, 2))
    Qim = padd(pmul(pmul(psi(0), psi(0)), Sb), pmul(pmul(psibar(0), psibar(0)), S), Fr(-1))   # imaginary-valued; = 2i Im(psi0^2 Sbar)
    inv2 = {"rho0": rho0, "N": N}
    inv4 = {"rho0^2": pmul(rho0, rho0), "rho0*N": pmul(rho0, N), "N^2": pmul(N, N), "|S|^2": pmul(S, Sb), "Re(psi0^2 Sbar)": Re, "Q = psi0^2 Sbar - c.c. (imaginary-valued)": Qim}
    inv2_14 = {"N": N}; inv4_14 = {"N^2": pmul(N, N), "|S|^2": pmul(S, Sb)}
    inv6_14 = {"N^3": pmul(pmul(N, N), N), "N*|S|^2": pmul(N, pmul(S, Sb))}
    pairs_g2 = [(M, M) for M in g2]
    so7 = []
    for a in range(1, 8):
        for b in range(a + 1, 8):
            X = [[Fr(0)] * 8 for _ in range(8)]; X[a][b] = Fr(1); X[b][a] = Fr(-1); so7.append(X)
    pairs_so7 = [(M, M) for M in so7]
    idx8, idx7 = list(range(8)), list(range(1, 8))
    out = {}
    out["G2xU1_R16"] = dict(deg2=certified_dim(pairs_g2, inv2, 1, 1, idx8), deg4=certified_dim(pairs_g2, inv4, 2, 2, idx8))
    out["G2xU1_R14"] = dict(deg2=certified_dim(pairs_g2, inv2_14, 1, 1, idx7), deg4=certified_dim(pairs_g2, inv4_14, 2, 2, idx7),
                            deg6_explicit_lower=rank_Q([poly_vector(P, {m: i for i, m in enumerate(monomials_bidegree(3, 3, idx7))}) for P in inv6_14.values() if annihilated(P, pairs_g2)]))
    out["SO7xU1_R16"] = dict(deg2=certified_dim(pairs_so7, inv2, 1, 1, idx8), deg4=certified_dim(pairs_so7, inv4, 2, 2, idx8))
    out["SO7xU1_R14"] = dict(deg2=certified_dim(pairs_so7, inv2_14, 1, 1, idx7), deg4=certified_dim(pairs_so7, inv4_14, 2, 2, idx7))
    out["weyl"] = dict(G2xU1_R16=weyl_table(W7_G2, ROOTS_G2, 12, True), G2xU1_R14=weyl_table(W7_G2, ROOTS_G2, 12, False),
                       SO7xU1_R16=weyl_table(W7_B3, ROOTS_B3, 48, True), SO7xU1_R14=weyl_table(W7_B3, ROOTS_B3, 48, False))
    out["T_parity"] = {k: T_parity(v) for k, v in {**inv2, **inv4}.items()}
    # cross-checks and derived statements
    c16 = out["G2xU1_R16"]; w16 = out["weyl"]["G2xU1_R16"]
    methods_agree = (c16["deg2"]["certified_dim"] == w16["2"] and c16["deg4"]["certified_dim"] == w16["4"]
                     and out["G2xU1_R14"]["deg2"]["certified_dim"] == out["weyl"]["G2xU1_R14"]["2"] and out["G2xU1_R14"]["deg4"]["certified_dim"] == out["weyl"]["G2xU1_R14"]["4"])
    locality = {d: (out["weyl"]["G2xU1_R14"][d] == out["weyl"]["SO7xU1_R14"][d]) for d in ("2", "4", "6")}
    locality16 = {d: (out["weyl"]["G2xU1_R16"][d] == out["weyl"]["SO7xU1_R16"][d]) for d in ("2", "4", "6")}
    out["methods_agree_deg2_deg4"] = methods_agree
    out["locality_g2_equals_so7"] = dict(R14=locality, R16=locality16)
    d2, d4 = c16["deg2"]["certified_dim"], c16["deg4"]["certified_dim"]
    out["hand_count"] = dict(deg2=2, deg4=6, deg4_T_even=5)
    out["F_VS_1"] = "SILENT" if (d2 == 2 and d4 == 6 and c16["deg4"]["T_even_dim"] == 5) else "FIRED"
    out["F_VS_2"] = "SILENT" if all(locality.values()) and all(locality16.values()) else "FIRED"
    # RUS classification: an invariant is real-unit-splitting iff it is not a polynomial in |psi|^2 alone
    Ntot = aux["Ntot"]
    def in_span_of(F, basis_list):
        names = [f"b{i}" for i in range(len(basis_list))]
        _, ok = expand_in_basis(F, dict(zip(names, basis_list)))
        return ok
    rus2 = {k: (not in_span_of(v, [Ntot])) for k, v in inv2.items()}
    rus4 = {k: (not in_span_of(v, [pmul(Ntot, Ntot)])) for k, v in inv4.items()}
    singlet_blind = {k: all(e[0] == 0 and e[8] == 0 for e in v) for k, v in {**inv2, **inv4}.items()}
    out["RUS"] = dict(deg2=dict(dim=d2, O16_dim=1, RUS_subspace_dim=(d2 - 1) if d2 else None, flags=rus2),
                      deg4=dict(dim=d4, O16_dim=1, RUS_subspace_dim=(d4 - 1) if d4 else None, T_even_RUS_subspace_dim=(c16["deg4"]["T_even_dim"] - 1) if c16["deg4"]["T_even_dim"] else None, flags=rus4),
                      singlet_blind=singlet_blind)
    # the point of record: c |psi|^4 with mu0 = mu7
    coeffs_rec, ok = expand_in_basis(pmul(Ntot, Ntot), {k: inv4[k] for k in ("rho0^2", "rho0*N", "N^2", "|S|^2", "Re(psi0^2 Sbar)")})
    A, B, c4, c5 = effective_params(0, 0, coeffs_rec["rho0^2"], coeffs_rec["rho0*N"], coeffs_rec["N^2"], coeffs_rec["|S|^2"], coeffs_rec["Re(psi0^2 Sbar)"])
    out["point_of_record"] = dict(quartic_coefficients=coeffs_rec, in_basis=ok, mu_split=0, effective_ABc4c5=[str(A), str(B), str(c4), str(c5)], is_origin=(A == 0 and B == 0 and c4 == 0 and c5 == 0))
    out["basis_deg2"] = list(inv2); out["basis_deg4"] = list(inv4)
    out["extra_invariants_found"] = (d2 is not None and d2 > 1 and d4 is not None and d4 > 1)
    return out, dict(inv2=inv2, inv4=inv4, Re=Re, Qim=Qim)

STRATA_REPS = {   # unnormalized rational representatives (scale-free; the orbit-space coordinates are normalized by |psi|^2)
    "R":   dict(re=[1, 0, 0, 0, 0, 0, 0, 0], im=[0] * 8),
    "P7":  dict(re=[0, 1, 0, 0, 0, 0, 0, 0], im=[0] * 8),
    "F7":  dict(re=[0, 1, 0, 0, 0, 0, 0, 0], im=[0, 0, 1, 0, 0, 0, 0, 0]),
    "I7":  dict(re=[0, 3, 0, 0, 0, 0, 0, 0], im=[0, 0, 4, 0, 0, 0, 0, 0]),
    "MP+": dict(re=[3, 4, 0, 0, 0, 0, 0, 0], im=[0] * 8),
    "MP-": dict(re=[3, 0, 0, 0, 0, 0, 0, 0], im=[0, 4, 0, 0, 0, 0, 0, 0]),
    "MF":  dict(re=[1, 1, 0, 0, 0, 0, 0, 0], im=[0, 0, 1, 0, 0, 0, 0, 0]),
    "MI-": dict(re=[1, 3, 0, 0, 0, 0, 0, 0], im=[0, 0, 4, 0, 0, 0, 0, 0]),
    "MI+": dict(re=[1, 4, 0, 0, 0, 0, 0, 0], im=[0, 0, 3, 0, 0, 0, 0, 0]),
    "MP0": dict(re=[1, 2, 0, 0, 0, 0, 0, 0], im=[1, 0, 0, 0, 0, 0, 0, 0]),   # psi0 = 1 + i, S real: Re(psi0^2 Sbar) = 0 (a T-pair family, t = 0)
    "MI0": dict(re=[1, 3, 0, 0, 0, 0, 0, 0], im=[1, 0, 4, 0, 0, 0, 0, 0]),
}

def phase2(g2, aux):
    out = {"strata": {}}
    e = lambda i: unit(i)
    for label, rep in STRATA_REPS.items():
        w = cvec(rep["re"], rep["im"]); inv = invariants_of(w)
        ns, ks = stabilizer_algebra(g2, w); dim_h, dim_k = len(ns), len(ks)
        phase_in_h = any(v[-1] != 0 for v in ns)
        k_basis = [combine(v[:-1], g2) for v in ks]
        # which G2-orbit type is K the stabilizer of (by the rank of the orbit map at the real vectors of psi)?
        x, y = w[:8], w[8:]
        imag_vectors = [vv for vv in ([Fr(0)] + x[1:], [Fr(0)] + y[1:]) if any(vv)]
        # the G2-stabilizer of psi = the stabilizer of its imaginary real vectors (G2 fixes e0): orbit rank at those vectors
        rank_orbit = orbit_rank(g2, imag_vectors) if imag_vectors else 0
        rho_norm, s2n, tn = inv["rho_norm"], inv["s2_norm"], inv["t_norm"]
        # allowed phases
        if inv["rho0"] != 0: P_kind, m, witness = "finite", 1, "psi0 != 0 forces omega = 1"
        elif inv["gram_scalar"]: P_kind, m, witness = "U1", None, "Gram matrix of (u,v) scalar: every phase rotation of (u,v) is a G2 rotation of the plane"
        else:
            P_kind, m = "finite", 2
            used = [a for a in range(1, 8) if x[a] != 0 or y[a] != 0]
            line = perp_line(used); sig = sigma_line(line)
            wit_ok = is_automorphism(sig) and (phase_mult(apply_elt(sig, w), Fr(-1), Fr(0)) == w)
            witness = dict(sigma_line=list(line), is_automorphism=is_automorphism(sig), fixes_psi_with_omega_minus_1=wit_ok,
                           only_pm1="the Gram matrix of (u,v) is not scalar, so R_alpha^T Gram R_alpha = Gram only for alpha in {0, pi}: the allowed phases are exactly {+1, -1}")
        # K identification and the pi3 index
        K_is_Gint = (dim_k == 14)
        if dim_k == 3:
            k_has_su2, index = True, su2_index(k_basis)
        elif dim_k == 8:
            # a long-root su(2) inside su(3)_n: the pointwise stabilizer of a quaternion subalgebra containing n (n = e1 -> line (1,2,4))
            sub = pointwise_stabilizer(g2, [e(1), e(2), e(4)])
            # verify it lies inside k
            kv = [flat(B) for B in k_basis]; rk = rank_Q(kv)
            inside = all(rank_Q(kv + [flat(Bs)]) == rk for Bs in sub)
            if not inside: halt("long-root su(2) not inside su(3)")
            k_has_su2, index = True, su2_index(sub)
        elif dim_k == 14: k_has_su2, index = True, 1
        else: halt(f"unexpected dim k = {dim_k}")
        hb = homotopy_bookkeeping("G2", rank_orbit, dim_k, P_kind, m, k_simply_connected=True, index=int(index), k_has_su2=k_has_su2, K_is_Gint=K_is_Gint)
        out["strata"][label] = dict(representative=dict(re=[str(Fr(a)) for a in rep["re"]], im=[str(Fr(b)) for b in rep["im"]]),
                                    invariants=dict(rho_norm=str(rho_norm), s2_norm=str(s2n), t_norm=str(tn), gram_scalar=inv["gram_scalar"], rank_uv=inv["rank_uv"]),
                                    dim_h=dim_h, dim_k=dim_k, phase_in_h=phase_in_h, orbit_rank_of_imaginary_part=rank_orbit,
                                    K_identification={14: "G2 (K = G)", 8: "Stab(n) = SU(3)", 3: "Stab(u,v) = SU(2)_long (index 1)"}[dim_k],
                                    P_kind=P_kind, m=m, witness=witness, dynkin_index=str(index), dim_V=15 - dim_h, **hb,
                                    pi1_nontrivial=(hb["pi1"] != "0"))
    # the criterion: pi1 = 0 iff (rho0 = 0 and S = 0)
    crit = {label: ((d["invariants"]["rho_norm"] == "0" and d["invariants"]["s2_norm"] == "0") == (not d["pi1_nontrivial"])) for label, d in out["strata"].items()}
    out["criterion_pi1_zero_iff_rho0_zero_and_S_zero"] = crit
    # effective parameters and the sampling of the allowed coefficient space
    out["effective_map"] = "V = -mu0 rho0 - mu7 N + c1 rho0^2 + c2 rho0 N + c3 N^2 + c4 |S|^2 + c5 Re(psi0^2 Sbar) on |psi|^2 = 1: A = c1 - c2 + c3, B = (mu7 - mu0) + c2 - 2 c3, c4, c5"
    # exact check of the reduction on random rational points
    import random
    rng = random.Random(20260930); red_ok = True
    for _ in range(50):
        mu0, mu7, c1, c2, c3, c4, c5 = [Fr(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(7)]
        rho = Fr(rng.randint(0, 10), 10); s = Fr(rng.randint(0, 10), 10) * (1 - rho); t = Fr(rng.randint(-10, 10), 10) * rho * s
        N = 1 - rho
        V = -mu0 * rho - mu7 * N + c1 * rho ** 2 + c2 * rho * N + c3 * N ** 2 + c4 * s ** 2 + c5 * t
        A, B, cc4, cc5 = effective_params(mu0, mu7, c1, c2, c3, c4, c5)
        const = -mu7 + c3
        if V != A * rho ** 2 + B * rho + cc4 * s ** 2 + cc5 * t + const: red_ok = False
    out["reduction_check"] = red_ok
    grid = [Fr(-2), Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1), Fr(2)]
    tally = {}; cone_ok = True; p0_only_origin = True; unprot_ok = True; strata_seen = set(); npts = 0
    pi1_of = {label: d["pi1"] for label, d in out["strata"].items()}
    def outcome(mins, faces):
        strata = sorted({mm["stratum"] for mm in mins})
        if faces: return "DEGENERATE: " + "; ".join(faces) + " | points: " + ",".join(strata)
        return ",".join(strata)
    for A in grid:
        for B in grid:
            for c4 in grid:
                for c5 in grid:
                    npts += 1
                    Emin, mins, faces = minimize_orbit_space(A, B, c4, c5)
                    oc = outcome(mins, faces); tally[oc] = tally.get(oc, 0) + 1
                    for mm in mins: strata_seen.add(mm["stratum"])
                    if faces and faces[0].startswith("whole") and not (A == 0 and B == 0 and c4 == 0 and c5 == 0): p0_only_origin = False
                    if not faces:
                        for mm in mins:
                            st = mm["stratum"]
                            pi1v = pi1_of.get(st)
                            if pi1v is None: halt(f"stratum {st} not in the table")
                            zero_rho_S = (Fr(mm["rho"]) == 0 and Fr(mm["s"]) == 0)
                            if (pi1v == "0") != zero_rho_S: unprot_ok = False
                    # cone property: the same outcome at half the coefficients
                    E2, m2, f2 = minimize_orbit_space(A / 2, B / 2, c4 / 2, c5 / 2)
                    if outcome(m2, f2) != oc: cone_ok = False
    out["sampling"] = dict(grid=[str(g) for g in grid], n_points=npts, tally=dict(sorted(tally.items())), strata_realized_as_minimizers=sorted(strata_seen),
                           cone_property=cone_ok, P0_only_at_origin=p0_only_origin, pi1_zero_iff_rho0_zero_and_S_zero_on_all_nondegenerate_minimizers=unprot_ok)
    out["codimension"] = dict(RUS_directions_total=5, note="1 at degree 2 (mu0 - mu7) + 4 at degree 4 (the T-even complement of |psi|^4)", effective_parameters_on_fixed_density=4,
                              P0_is_the_origin_of_the_effective_space=True, every_stratum_region_is_a_cone=cone_ok)
    out["F_VS_3"] = "SILENT" if (all(crit.values()) and unprot_ok and p0_only_origin and cone_ok and red_ok) else "FIRED"
    return out

def phase3(g2, aux, p1aux, strata_out):
    X = [psi(k) for k in range(8)]
    Xd = poly_oconj(poly_cconj(X))
    Pp = poly_omul(X, Xd); P2 = poly_omul(Xd, X); Sq = poly_omul(X, X)
    forms = {
        "F-a.1 |<psi,psi>|^2 (the complex bilinear norm, modulus squared)": pmul(bilinear_norm(X), T_swap(bilinear_norm(X))),
        "F-a.2 ||psi psibar^dag||^2_H": hermitian_norm_sq(Pp),
        "F-a.3 ||psibar^dag psi||^2_H": hermitian_norm_sq(P2),
        "F-a.4 ||psi^2||^2_H": hermitian_norm_sq(Sq),
        "F-a.5 N_O(psi psibar^dag) = sum_k P_k^2": bilinear_norm(Pp),
        "F-a.6 ||Im_O(psi psibar^dag)||^2_H": hermitian_norm_sq([{}] + Pp[1:]),
        "D-a.1 Re_O(psi psibar^dag) (degree 2)": Pp[0],
        "D-a.2 Re_O(psibar^dag psi) (degree 2)": P2[0],
    }
    inv2, inv4 = p1aux["inv2"], p1aux["inv4"]
    basis4 = {k: inv4[k] for k in ("rho0^2", "rho0*N", "N^2", "|S|^2", "Re(psi0^2 Sbar)")}
    pairs_g2 = [(M, M) for M in g2]
    pi1_of = {label: d["pi1"] for label, d in strata_out["strata"].items()}
    res = {}
    for name, F in forms.items():
        deg = max(sum(e) for e in F); inv = annihilated(F, pairs_g2); Tp = T_parity(F)
        if deg == 4:
            coeffs, ok = expand_in_basis(F, basis4)
            A, B, c4, c5 = effective_params(0, 0, coeffs["rho0^2"], coeffs["rho0*N"], coeffs["N^2"], coeffs["|S|^2"], coeffs["Re(psi0^2 Sbar)"])
            Emin, mins, faces = minimize_orbit_space(A, B, c4, c5)
            strata = sorted({mm["stratum"] for mm in mins})
            key = lambda st: st
            res[name] = dict(degree=4, g2_u1_invariant=inv, T_parity=Tp, coefficients=coeffs, in_T_even_basis=ok, effective_ABc4c5=[str(A), str(B), str(c4), str(c5)],
                             is_O16_point=(A == 0 and B == 0 and c4 == 0 and c5 == 0), Emin=Emin, minimizers=mins, degenerate_faces=faces,
                             pi1_of_minimizing_strata={st: pi1_of[key(st)] for st in strata}, location_note=("degenerate minimum set" if faces else "single stratum" if len(strata) == 1 else "several strata"))
        else:
            coeffs, ok = expand_in_basis(F, inv2)
            res[name] = dict(degree=2, g2_u1_invariant=inv, T_parity=Tp, coefficients=coeffs, in_basis=ok, is_O16=(coeffs.get("rho0") == coeffs.get("N")))
    forcing = {
        "F-a": dict(status="MAP", reason="the algebra-product forms are located; none is banked as the action (I2 is the import; Q-A1-3 the reading of record): not forcing", n_forms=len(forms)),
        "F-b": dict(status="SCREENED_OUT", reason="A-2.1 / Q-VS-1: the carrier of e0 is not settled (not the K7 vertices); registered as the successor S-VS-1"),
        "F-c": dict(status="NOT_FORCING", reason="A-2.2 / Q-VS-2: the kernel couples to the total 16-component density; O(16)-symmetric"),
        "F-d": dict(status="EXCLUDED", reason="the oriented term vanishes on every uniform state; defect-core energetics is behind M.CW"),
    }
    live = sum(1 for v in forcing.values() if v["status"] in ("FORCING_PI1_Z", "FORCING_PI1_0"))
    return dict(F_a=res, forcing_table=forcing, live_sources=live, F_VS_4="SILENT" if live == 0 else "FIRED")

def verdict(p0, p1, p2, p3):
    reasons = []
    if not p0["all_pass"]: reasons.append("Phase 0 control failed"); return dict(class_code="VC-4", reasons=reasons)
    if p1["F_VS_2"] == "FIRED": reasons.append("F-VS-2: a phi-carrying local invariant"); return dict(class_code="VC-4", reasons=reasons)
    c = p1["G2xU1_R16"]
    if c["deg2"]["certified_dim"] is None or c["deg4"]["certified_dim"] is None: reasons.append("Phase 1 bounds did not meet"); return dict(class_code="VC-4", reasons=reasons)
    if p1["F_VS_1"] == "FIRED": reasons.append("F-VS-1: machine count differs from the hand count (H-item; the machine count stands)")
    if p2["F_VS_3"] == "FIRED": reasons.append("F-VS-3: the stratum picture differs from the criterion (H-item; the computed table stands)")
    forced = [k for k, v in p3["forcing_table"].items() if v["status"] in ("FORCING_PI1_Z", "FORCING_PI1_0")]
    if any(p3["forcing_table"][k]["status"] == "FORCING_PI1_0" for k in forced): return dict(class_code="VC-2", reasons=reasons + ["a live source fixes a pi1 = 0 stratum"])
    if any(p3["forcing_table"][k]["status"] == "FORCING_PI1_Z" for k in forced): return dict(class_code="VC-1", reasons=reasons + ["a live source fixes a pi1 = Z stratum"])
    if p1["extra_invariants_found"] and p3["live_sources"] == 0:
        reasons.append("extra (real-unit-splitting) invariants certified; every forcing source screened not forcing / out / excluded")
        return dict(class_code="VC-3", reasons=reasons, precedence="VC-4 > VC-2 > VC-1 > VC-3")
    return dict(class_code="VC-4", reasons=reasons + ["no class condition met"])

# ============================================================================= main
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    t0 = time.time()
    t1_pre = guards()
    g2 = derivation_algebra()
    ck = dict(gate=GATE, leg=LEG, mode=mode,
              identity=dict(instrument_md5=md5_file(os.path.abspath(__file__)), memo_md5=MEMO_MD5, memo_bytes=MEMO_BYTES, lock_md5=LOCK_MD5, lock_bytes=LOCK_BYTES,
                            t1_md5=T1_MD5, t1_patterns=T1_PATTERNS, scanner_md5=SCANNER_MD5, extract_md5=EXTRACT_MD5, extract_bytes=EXTRACT_BYTES,
                            schema_md5=SCHEMA_MD5, comparator_md5=COMPARATOR_MD5, elections=ELECTIONS, readings=READINGS,
                            octonion_convention="Fano lines {i, i+1, i+3} mod 7 on e1..e7 (the §3.4-SIGNPHI convention); e_i e_j = e_k on a line (i,j,k) in cyclic order",
                            primes_for_upper_bound=list(PRIMES), timestamp_utc=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())),
              T1_pre=t1_pre)
    p0, aux = phase0(g2); ck["phase0"] = p0
    print("Phase 0:", {k: p0[k]["PASS"] for k in ("0a", "0b", "0c", "0d", "0e", "0f")}, "all_pass", p0["all_pass"])
    if mode == "preread" or not p0["all_pass"]:
        ck["phase1"] = ck["phase2"] = ck["phase3"] = None
        ck["verdict"] = None if p0["all_pass"] else dict(class_code="VC-4", reasons=["Phase 0 control failed"])
        out = "g_vs1_chatleg_prereadcheckpoint.json"
    else:
        p1, p1aux = phase1(g2, aux); ck["phase1"] = p1
        print("Phase 1: certified dims deg2/deg4 =", p1["G2xU1_R16"]["deg2"]["certified_dim"], p1["G2xU1_R16"]["deg4"]["certified_dim"], "T-even", p1["G2xU1_R16"]["deg4"]["T_even_dim"], "| weyl", p1["weyl"]["G2xU1_R16"], "| F-VS-1", p1["F_VS_1"], "F-VS-2", p1["F_VS_2"])
        p2 = phase2(g2, aux); ck["phase2"] = p2
        print("Phase 2: pi1 per stratum", {k: v["pi1"] for k, v in p2["strata"].items()}, "| F-VS-3", p2["F_VS_3"])
        p3 = phase3(g2, aux, p1aux, p2); ck["phase3"] = p3
        print("Phase 3: live sources", p3["live_sources"], "| F-VS-4", p3["F_VS_4"])
        ck["verdict"] = verdict(p0, p1, p2, p3)
        print("Verdict:", ck["verdict"]["class_code"])
        out = "g_vs1_chatleg_checkpoint.json"
    ck["runtime_seconds"] = round(time.time() - t0, 1)
    text = json.dumps(ck, indent=1, sort_keys=True, ensure_ascii=False)
    hits, coll = t1_scan_text(text, t1_load(T1LIST))
    ck["T1_post_write"] = dict(hits=hits, collisions=coll)
    text = json.dumps(ck, indent=1, sort_keys=True, ensure_ascii=False)
    hits2, coll2 = t1_scan_text(text, t1_load(T1LIST))
    if hits2: halt(f"T1 post-write hit {hits2}: checkpoint not written")
    open(out, "w", encoding="utf-8").write(text)
    print("wrote", out, md5_bytes(text.encode("utf-8")), len(text.encode("utf-8")), "B; T1 post-write hits", hits2, "collisions", coll2, "; runtime", ck["runtime_seconds"], "s")

if __name__ == "__main__":
    main()
