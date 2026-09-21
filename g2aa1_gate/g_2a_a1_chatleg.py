#!/usr/bin/env python3
"""g_2a_a1_chatleg.py — Gate G-2a-A1 chat-leg instrument (Phases 0, 1, 1b, 2, 3).

Guards (fail-closed, no override flag): md5 of the locked memo, the gate T1 list, the action-of-record
extract; T1 scan of this file, the memo and the extract (pattern-index-only reporting). D-T1 is retired.

Exact arithmetic (sympy rationals / Fractions / integers) everywhere except the spinorial-2O block
(floats; thresholded) and the numeric cross-check of one symbolic integral. No ledger value, no
observational target, no verdict text: the verdict class is assembled LAST from the encoded booleans by
the schema rule (the comparator recomputes it).

Usage: python3 g_2a_a1_chatleg.py run [--out DIR]     |     python3 g_2a_a1_chatleg.py selftest
"""
import hashlib, json, os, sys, time, itertools, math
from fractions import Fraction

# ----------------------------------------------------------------------------- guards
MEMO = "staging_memo_G_2a_A1_v2.md";      MEMO_MD5 = "626aa868844220eb6c3801ef07a77783"
T1LIST = "tools/t1/T1_forbidden_G_2a_A1.txt"; T1_MD5 = "2026b782db3905d9f2ce35733823618c"
EXTRACT = "inputs/paper_II_3_4_4_and_3_4_7_extract.md"; EXTRACT_MD5 = "940b0bee4b2112e911ae738c3db2bc3d"
LEDGER_BASE_MD5 = "40009ec0197876b130766f1ae7494360"
ELECTIONS = {f"E-A1-{i}": "a" for i in range(1, 9)}
GATE = "G-2a-A1"

def md5_bytes(b): return hashlib.md5(b).hexdigest()
def md5_file(p): return md5_bytes(open(p, "rb").read())

NUMCHARS = set("0123456789.eE+-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
def t1_load(path):
    return [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]
def t1_is_numeric(p): return all(c in NUMCHARS for c in p)
def t1_scan_text(text, pats):
    hits, coll = [], []
    for i, p in enumerate(pats):
        s = 0
        while True:
            j = text.find(p, s)
            if j < 0: break
            if t1_is_numeric(p):
                a = j
                while a > 0 and text[a-1] in NUMCHARS and text[a-1] != " ": a -= 1
                b = j + len(p)
                while b < len(text) and text[b] in NUMCHARS and text[b] != " ": b += 1
                (hits if text[a:b] == p else coll).append((i, j))
            else:
                hits.append((i, j))
            s = j + 1
    return hits, coll

def guards():
    log = []
    for path, want in ((MEMO, MEMO_MD5), (T1LIST, T1_MD5), (EXTRACT, EXTRACT_MD5)):
        if not os.path.exists(path): raise SystemExit(f"HALT: missing {path}")
        h = md5_file(path)
        if h != want: raise SystemExit(f"HALT: md5 mismatch for {path}: {h} != {want}")
        log.append(f"guard md5 OK {path} {h}")
    pats = t1_load(T1LIST)
    if len(pats) != 24: raise SystemExit(f"HALT: T1 list has {len(pats)} patterns, expected 24")
    scan = {}
    for name, path in (("instrument", os.path.abspath(__file__)), ("memo", MEMO), ("extract", EXTRACT)):
        text = open(path, "rb").read().decode("utf-8", "replace")
        hits, coll = t1_scan_text(text, pats)
        if hits: raise SystemExit(f"HALT: T1 hit in {name}: pattern indices {sorted(set(i for i,_ in hits))}")
        scan[name] = "CLEAN"; log.append(f"T1 {name}: CLEAN (numeric collisions {len(coll)})")
    return scan, log

# ----------------------------------------------------------------------------- octonions (exact)
import sympy as sp
LINES = [((i-1) % 7 + 1, i % 7 + 1, (i+2) % 7 + 1) for i in range(1, 8)]   # (1,2,4),(2,3,5),...,(7,1,3)
LINESETS = {frozenset(l) for l in LINES}
MULT = {}
for (a, b, c) in LINES:
    for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
        MULT[(x, y)] = (1, z); MULT[(y, x)] = (-1, z)
def phi(a, b, c):
    """structure constant phi_abc for imaginary indices 1..7 (0 off lines)."""
    if len({a, b, c}) < 3 or frozenset((a, b, c)) not in LINESETS: return 0
    s, k = MULT[(a, b)]
    return s if k == c else -s
def omul(p, q):
    r = [sp.Integer(0)] * 8
    for i in range(8):
        if p[i] == 0: continue
        for j in range(8):
            if q[j] == 0: continue
            if i == 0: r[j] += p[i] * q[j]
            elif j == 0: r[i] += p[i] * q[j]
            elif i == j: r[0] -= p[i] * q[j]
            else:
                s, k = MULT[(i, j)]; r[k] += s * p[i] * q[j]
    return r
def unit(i):
    v = [sp.Integer(0)] * 8; v[i] = sp.Integer(1); return v
def Lmat(a):
    M = sp.zeros(8, 8)
    for j in range(8):
        col = omul(unit(a), unit(j))
        for i in range(8): M[i, j] = col[i]
    return M
def is_aut(P, tol=None):
    """exact automorphism test of an 8x8 sympy matrix (rational/algebraic entries)."""
    for i in range(8):
        for j in range(8):
            lhs = P * sp.Matrix(omul(unit(i), unit(j)))
            Pi = [P[k, i] for k in range(8)]; Pj = [P[k, j] for k in range(8)]
            rhs = sp.Matrix(omul(Pi, Pj))
            d = (lhs - rhs).applyfunc(sp.nsimplify) if tol is None else (lhs - rhs)
            if any(sp.simplify(x) != 0 for x in d): return False
    return True
def aut_defect_float(P):
    """max_{i,j} |P(e_i e_j) - P(e_i)P(e_j)| for a real 8x8 numpy matrix."""
    import numpy as np
    d = 0.0
    for i in range(8):
        for j in range(8):
            lhs = P @ np.array([float(x) for x in omul(unit(i), unit(j))])
            Pi = [sp.Float(P[k, i]) for k in range(8)]; Pj = [sp.Float(P[k, j]) for k in range(8)]
            rhs = np.array([float(x) for x in omul(Pi, Pj)])
            d = max(d, float(np.max(np.abs(lhs - rhs))))
    return d
def span_dim(mats): return sp.Matrix([list(M) for M in mats]).rank()

def derivation_algebra():
    """g2 = Der(O) as 7x7 antisymmetric matrices on Im O (exact nullspace); returns list of 14 sympy 7x7."""
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
    eqs = []
    for i in range(1, 8):
        for j in range(1, 8):
            ei, ej = unit(i), unit(j)
            lhs = Dapply(omul(ei, ej))
            rhs = [sp.Integer(0)] * 8
            for m in range(1, 8):
                if D[m-1, i-1] != 0:
                    prod = omul(unit(m), ej)
                    for n in range(8): rhs[n] += D[m-1, i-1] * prod[n]
                if D[m-1, j-1] != 0:
                    prod = omul(ei, unit(m))
                    for n in range(8): rhs[n] += D[m-1, j-1] * prod[n]
            for n in range(8):
                e = sp.expand(lhs[n] - rhs[n])
                if e != 0: eqs.append(e)
    A = sp.Matrix([[sp.Poly(e, *syms).coeff_monomial(s) for s in syms] for e in eqs])
    ns = A.nullspace()
    g2 = []
    for v in ns:
        M = sp.zeros(7, 7); t = 0
        for i in range(7):
            for j in range(i+1, 7):
                M[i, j] = v[t]; M[j, i] = -v[t]; t += 1
        g2.append(M)
    return g2
def to8(M7):
    M8 = sp.zeros(8, 8); M8[1:, 1:] = M7; return M8

# ----------------------------------------------------------------------------- Phase 0
def phase0(g2, extract_text):
    P = {}
    # (0a) field content of record (documentary asserts on the extract + the author's answers in its header)
    assert "sixteen real components" in extract_text and "16 real components" in extract_text and "8 complex amplitudes" in extract_text
    assert "spinor index" not in extract_text.split("### 3.4.4")[1]   # no spinor index in the field content of record
    P["field_real_components"] = 16; P["complex_amplitudes"] = 8; P["spinor_index_present"] = False
    # (0c) spatial-internal direct product: the term list of record (from the extract) — every term's index
    # structure factorizes: internal indices only via delta_ab / phi_abc, spatial only via d_x, d_y.
    assert "φ_{abc}\\,\\psi_a\\,\\partial_x\\psi_b\\,\\partial_y\\psi_c" in extract_text or "φ_abc ψ_a ∂_x ψ_b ∂_y ψ_c" in extract_text
    assert "K_{ij}(r) = a(r)\\,\\delta_{ij}" in extract_text
    terms = [{"term": "two-body contact", "internal": "delta_ab (single scalar)", "spatial": "none"},
             {"term": "GP kinetic (I2)", "internal": "delta_ab", "spatial": "d_i . d_i"},
             {"term": "oriented O", "internal": "phi_abc", "spatial": "eps_xy d_x d_y"}]
    for t in terms: t["mixed_spatial_internal_tensor"] = False   # no term of record couples a spatial index to an internal index
    P["spatial_internal_direct_product"] = all(t["mixed_spatial_internal_tensor"] is False for t in terms)
    P["_terms_of_record"] = terms
    # (0b) Sym_int: the stabilizer of the O density inside so(16). T(u,v,w) = phi_abc u_a v_b w_c, complex-trilinear on C^8.
    # Real coordinates: component a (a=0..7) = x_a + i y_a  -> index a (real part), 8+a (imag part).
    # Build the 8192 x 120 integer matrix of the linear map X -> [ (u,v,w) -> T(Xu,v,w)+T(u,Xv,w)+T(u,v,Xw) ] over real basis triples,
    # then the kernel via the Gram matrix A^T A (exact).
    import numpy as np
    def T_complex(u, v, w):   # u,v,w: length-16 exact (Fraction/int/sympy) real vectors -> complex value (re, im) exact
        re = 0; im = 0
        for (a, b, c) in LINES:
            for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
                for (p, q, r, s) in ((x, y, z, 1), (y, x, z, -1)):
                    ur, ui = u[p], u[8+p]; vr, vi = v[q], v[8+q]; wr, wi = w[r], w[8+r]
                    pr = ur*vr - ui*vi; pi_ = ur*vi + ui*vr
                    re += s * (pr*wr - pi_*wi); im += s * (pr*wi + pi_*wr)
        return re, im
    idx = [(i, j) for i in range(16) for j in range(i+1, 16)]
    basis = [[1 if t == k else 0 for t in range(16)] for k in range(16)]
    Tb = {}
    for k in range(16):
        for l in range(16):
            for m in range(16):
                Tb[(k, l, m)] = T_complex(basis[k], basis[l], basis[m])
    ncols = len(idx)
    A = np.zeros((2 * 16**3, ncols), dtype=np.int64)
    for g, (i, j) in enumerate(idx):
        act = {j: (i, 1), i: (j, -1)}   # X = E_ij - E_ji: X e_j = e_i, X e_i = -e_j
        for (k, l, m) in itertools.product(range(16), repeat=3):
            vr = 0; vi = 0
            if k in act:
                i2, sg = act[k]; r_, i_ = Tb[(i2, l, m)]; vr += sg*r_; vi += sg*i_
            if l in act:
                i2, sg = act[l]; r_, i_ = Tb[(k, i2, m)]; vr += sg*r_; vi += sg*i_
            if m in act:
                i2, sg = act[m]; r_, i_ = Tb[(k, l, i2)]; vr += sg*r_; vi += sg*i_
            row = k*256 + l*16 + m
            A[row, g] = vr; A[4096 + row, g] = vi
    G = (A.T @ A)
    Gs = sp.Matrix(G.tolist())
    ker = Gs.nullspace()
    P["sym_int_continuous_dim"] = len(ker)
    P["sym_int_continuous"] = "G2" if len(ker) == 14 else ("G2xU1_psi0" if len(ker) == 15 else f"dim{len(ker)}")
    def vec_of(X):
        return np.array([int(X[i, j]) for (i, j) in idx], dtype=np.int64)
    def in_kernel(X):
        return not np.any(A @ vec_of(X))
    def X_from_g2(D7):
        X = sp.zeros(16, 16); X[1:8, 1:8] = D7; X[9:16, 9:16] = D7; return X
    P["g2_preserves_O"] = all(in_kernel(X_from_g2(D)) for D in g2)
    # the decoupled real-unit phase: rotation Re psi_0 <-> Im psi_0 (indices 0 and 8) preserves O (O involves imaginary components only)
    X0 = sp.zeros(16, 16); X0[0, 8] = -1; X0[8, 0] = 1
    P["_psi0_phase_preserves_O"] = bool(in_kernel(X0))
    # imaginary-sector stabilizer: restrict to so(14) on indices {1..7, 9..15}
    keep = [g for g, (i, j) in enumerate(idx) if i not in (0, 8) and j not in (0, 8)]
    Gk = sp.Matrix(G[np.ix_(keep, keep)].tolist())
    P["_imag_sector_continuous_dim"] = len(Gk.nullspace())
    # generic so(16) element breaks O: rotation mixing Re psi_1 with Im psi_2 (indices 1 and 10)
    Xg = sp.zeros(16, 16); Xg[1, 10] = 1; Xg[10, 1] = -1
    defect = A @ vec_of(Xg); margin = int(np.max(np.abs(defect)))
    P["generic_so16_breaks_O"] = margin > 0
    Jm = sp.zeros(16, 16)
    for a in range(8): Jm[8+a, a] = 1; Jm[a, 8+a] = -1
    P["O_phase_invariant"] = bool(in_kernel(Jm))
    u = [sp.Rational(i+1, 3) for i in range(16)]; v = [sp.Rational(2*i-5, 7) for i in range(16)]; w = [sp.Rational(3*i+1, 5) for i in range(16)]
    def phase(vec16, cr, ci):
        out = [sp.Integer(0)] * 16
        for a in range(8):
            xr, xi = vec16[a], vec16[8+a]; out[a] = cr*xr - ci*xi; out[8+a] = cr*xi + ci*xr
        return out
    t0 = T_complex(u, v, w)
    s3 = sp.sqrt(3)/2
    t1 = T_complex(phase(u, sp.Rational(-1, 2), s3), phase(v, sp.Rational(-1, 2), s3), phase(w, sp.Rational(-1, 2), s3))
    assert sp.simplify(t1[0] - t0[0]) == 0 and sp.simplify(t1[1] - t0[1]) == 0
    ti = T_complex(phase(u, 0, 1), phase(v, 0, 1), phase(w, 0, 1))   # i^3 = -i
    assert sp.simplify(ti[0] - t0[1]) == 0 and sp.simplify(ti[1] + t0[0]) == 0
    P["phase_subgroup_order"] = 3
    conj = lambda x: x[:8] + [-y for y in x[8:]]
    tc = T_complex(conj(u), conj(v), conj(w))
    P["conjugation_maps_O_to_conjugate"] = bool(tc[0] == t0[0] and tc[1] == -t0[1])
    # Sym_int is pinned when its continuous part is fully identified: g2 on the imaginary sector (dim 14 there) plus, if present,
    # the decoupled real-unit phase u(1)_psi0 (dim 15 total), and nothing else.
    P["sym_int_pinned"] = bool(P["g2_preserves_O"] and P["generic_so16_breaks_O"] and P["_imag_sector_continuous_dim"] == 14
                               and P["sym_int_continuous_dim"] == 14 + (1 if P["_psi0_phase_preserves_O"] else 0))
    # (0d) vacuum manifold of record: two-body term depends on rho = |psi|^2 only (O(16)); O vanishes on constants:
    P["two_body_symmetry"] = "O(16)"
    z = [sp.Integer(0)] * 16
    assert T_complex(u, z, z) == (0, 0)   # O density vanishes on uniform states (derivatives zero)
    P["real_unit_splitting_term_present"] = False   # Q-A1-3 (author's answer of record; the extract has no such term)
    P["vacuum_manifold_of_record"] = "S15"; P["pi1_V"] = 0; P["pi4_V"] = 0   # pi_k(S^n)=0 for k<n (adopted)
    # locking inventory: stabilizers in g2 of representative psi_0 by rank of span(Im a, Im b)
    def stab_dim(vectors):
        # {D in g2 : D v = 0 for v in vectors}; vectors in Im O (7-vectors)
        cols = []
        for D in g2:
            col = []
            for v in vectors: col += list(D * sp.Matrix(v))
            cols.append(col)
        M = sp.Matrix(cols).T   # (7*len) x 14
        ns = M.nullspace()
        return len(ns), ns
    e = lambda k: [1 if i == k-1 else 0 for i in range(7)]
    d0, _ = stab_dim([])                     # rank 0: psi_0 = e_0 (real unit): all of g2
    d1, ns1 = stab_dim([e(7)])               # rank 1: psi_0 = e_7
    d2, ns2 = stab_dim([e(1), e(2)])         # rank 2: psi_0 = e_1 + i e_2
    assert (d0, d1, d2) == (14, 8, 3)
    # the rank-2 stabilizer also fixes e_4 = e_1 e_2 (pointwise stabilizer of the quaternion subalgebra):
    sub2 = [sum((c * D for c, D in zip(v, g2)), sp.zeros(7, 7)) for v in ns2]
    assert all(D * sp.Matrix(e(4)) == sp.zeros(7, 1) for D in sub2)
    P["_sub_long"] = sub2
    P["_sub_su3"] = [sum((c * D for c, D in zip(v, g2)), sp.zeros(7, 7)) for v in ns1]
    inv = []
    for rank, H0, dim in ((0, "G2", 14), (1, "SU3", 8), (2, "SU2_long", 3)):
        inv.append({"rank": rank, "H0": H0, "H0_dim": dim, "pi0_generic": 1, "sl2_generator_jordan_type": [2, 2, 1, 1, 1],
                    "sl2_generator_index": 1, "pi3_injective": True, "pi4_quotient": 0})
    P["locking_inventory"] = inv
    # (0e) controls
    # L_perp psi0 = 0: with mu = U*rho0 the operator -1/2 grad^2 + (U rho - mu) annihilates the uniform state (symbolic identity)
    U, rho0 = sp.symbols('U rho0', positive=True); mu = U*rho0
    P["controls"] = {"L_perp_zero_mode": sp.simplify((U*rho0 - mu)) == 0,
                     "F21_split_1_3_3bar": None, "generic_so16_fails_margin_positive": bool(margin > 0)}
    P["_margin"] = str(margin)
    return P

# ----------------------------------------------------------------------------- finite groups on the Fano plane
def fano_collineations():
    pts = list(range(1, 8)); out = []
    for perm in itertools.permutations(pts):
        m = dict(zip(pts, perm))
        if all(frozenset(m[x] for x in l) in LINESETS for l in LINES): out.append(m)
    return out
def perm_matrix(perm, signs):
    P = sp.zeros(8, 8); P[0, 0] = 1
    for i in range(1, 8): P[perm[i], i] = signs.get(i, 1)
    return P
def is_aut_signed(perm, signs):
    """exact automorphism test for a signed permutation e_i -> signs[i] e_{perm[i]} (imaginary units), fixing e_0."""
    for i in range(1, 8):
        for j in range(1, 8):
            if i == j: continue
            eps, k = MULT[(i, j)]
            eps2, k2 = MULT[(perm[i], perm[j])]
            if perm[k] != k2: return False
            if eps * signs.get(k, 1) != signs.get(i, 1) * signs.get(j, 1) * eps2: return False
    return True
def unsigned_automorphisms(colls):
    return [m for m in colls if is_aut_signed(m, {})]
def F21_check(colls):
    F21 = [ {x: (a*x + b - 1) % 7 + 1 for x in range(1, 8)} for a in (1, 2, 4) for b in range(7) ]
    ok = all(is_aut_signed(m, {}) for m in F21) and len({tuple(sorted(m.items())) for m in F21}) == 21
    chi = [sum(1 for x in range(1, 8) if m[x] == x) for m in F21]
    norm = sp.Rational(sum(c*c for c in chi), 21); triv = sp.Rational(sum(chi), 21)
    nu2 = {x: (2*x - 1) % 7 + 1 for x in range(1, 8)}
    return ok and norm == 3 and triv == 1, is_aut_signed(nu2, {}), int(norm), int(triv)

# ----------------------------------------------------------------------------- Phase 1
def phase1(g2, P0):
    R = {}
    # ---------------- T1
    import cmath
    s2 = sp.sqrt(2)
    Q = set()
    for signs in itertools.product([1, -1], repeat=4):
        for pos in range(4):
            v = [0, 0, 0, 0]; v[pos] = signs[pos]; Q.add(tuple(sp.Integer(x) for x in v))
        Q.add(tuple(sp.Rational(s, 2) for s in signs))
    for i, j in itertools.combinations(range(4), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [sp.Integer(0)] * 4; v[i] = si/s2; v[j] = sj/s2; Q.add(tuple(v))
    Q = list(Q); assert len(Q) == 48
    def qmul(a, b):
        a0, a1, a2, a3 = a; b0, b1, b2, b3 = b
        return (a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2, a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0)
    def chi32(q):   # 2cos3phi + 2cosphi with c = cos phi = Re q: 8c^3 - 4c
        c = q[0]; return sp.expand(8*c**3 - 4*c)
    norm = sp.simplify(sum(chi32(q)**2 for q in Q) / 48)
    fs = sp.simplify(sum(chi32(tuple(sp.simplify(x) for x in qmul(q, q))) for q in Q) / 48)
    T1 = {"chi32_norm": int(norm), "chi32_at_1": int(chi32((1, 0, 0, 0))), "chi32_at_minus1": int(chi32((-1, 0, 0, 0))), "fs_indicator": int(fs)}
    T1["seven_real"] = all(all(x.is_rational for x in D) for D in g2)     # the 7 is defined over Q (real form)
    # even-multiplicity theorem for a quaternionic irrep in a real representation + dimension bound
    upper = 7 // 4                     # 1
    T1["quartet_multiplicity_upper"] = upper if upper % 2 == 0 else upper - 1     # even and <= floor(7/4) -> 0
    T1["phase_char_on_2O_trivial"] = True   # Hom(2O, Z3) = 1: |2O^ab| = 2 is coprime to 3 (integer fact, asserted below)
    assert math.gcd(2, 3) == 1
    # branchings via the compact Casimir C = sum (G^-1)_ij D_i D_j, G_ij = -K_sub(D_i,D_j)/2 ; eigenvalues -j(j+1)
    def casimir_spectrum(sub):
        n = len(sub); assert n == 3
        # adjoint within the subalgebra
        Msub = sp.Matrix([list(S) for S in sub]).T
        Nsub = (Msub.T * Msub).inv() * Msub.T
        def ad_coords(X):
            cols = []
            for Y in sub:
                Z = X*Y - Y*X
                sol = Nsub * sp.Matrix(list(Z))
                assert Msub*sol == sp.Matrix(list(Z))
                cols.append(list(sol))
            return sp.Matrix(cols).T
        ads = [ad_coords(X) for X in sub]
        K = sp.Matrix(3, 3, lambda i, j: (ads[i]*ads[j]).trace())
        G = -K/2; Gi = G.inv()
        C = sp.zeros(7, 7)
        for i in range(3):
            for j in range(3): C += Gi[i, j] * sub[i] * sub[j]
        ev = (-C).eigenvals()
        spec = {}
        for val, mult in ev.items(): spec[sp.nsimplify(val)] = mult
        # -j(j+1) -> j ; irreps dims 2j+1, count = mult/(2j+1)
        dims = []
        for jj1, mult in spec.items():
            j = (-1 + sp.sqrt(1 + 4*jj1)) / 2; j = sp.nsimplify(j)
            d = int(2*j + 1); assert mult % d == 0
            dims += [d] * (mult // d)
        return sorted(dims, reverse=True)
    sub_long = P0["_sub_long"]
    T1["branching_long_root"] = casimir_spectrum(sub_long)
    # short-root: the ideal of so(4) = stab(H_L) complementary to the long-root ideal
    def stab_setwise_dim(subspace_vectors):
        # {D in g2 : D(span) subset span}
        V = sp.Matrix(subspace_vectors).T   # 7 x k
        proj = sp.eye(7) - V * (V.T * V).inv() * V.T
        cols = []
        for D in g2:
            col = []
            for v in subspace_vectors: col += list(proj * D * sp.Matrix(v))
            cols.append(col)
        ns = sp.Matrix(cols).T.nullspace()
        return [sum((c * D for c, D in zip(v, g2)), sp.zeros(7, 7)) for v in ns]
    e = lambda k: [1 if i == k-1 else 0 for i in range(7)]
    so4 = stab_setwise_dim([e(1), e(2), e(4)])
    assert len(so4) == 6
    # centralizer of the long-root ideal inside so4
    def centralizer_in(space, sub):
        cols = []
        for X in space:
            col = []
            for Y in sub: col += list(X*Y - Y*X)
            cols.append(col)
        ns = sp.Matrix(cols).T.nullspace()
        return [sum((c * X for c, X in zip(v, space)), sp.zeros(7, 7)) for v in ns]
    sub_short = centralizer_in(so4, sub_long)
    assert len(sub_short) == 3
    T1["branching_short_root"] = casimir_spectrum(sub_short)
    # su(3)-sl2: so(3) built from the J-basis (e1,e3),(e2,e6),(e4,e5) with J = L_{e7}; check membership in stab(e7)
    def rot(i, j):
        M = sp.zeros(7, 7); M[i-1, j-1] = -1; M[j-1, i-1] = 1; return M
    R12 = rot(1, 2) + rot(3, 6); R13 = rot(1, 4) + rot(3, 5); R23 = rot(2, 4) + rot(6, 5)
    def in_span(X, space):
        M = sp.Matrix([list(S) for S in space]).T
        return sp.Matrix.hstack(M, sp.Matrix(list(X))).rank() == M.rank()
    su3 = P0["_sub_su3"]
    assert all(in_span(X, su3) for X in (R12, R13, R23)), "so(3) construction not inside stab(e7)"
    T1["branching_su3_sl2"] = casimir_spectrum([R12, R13, R23])
    # principal sl2: weights of h_princ = 2 rho^vee on the 7 via the root system of g2 (Cartan = su(3) Cartan)
    h1 = rot(1, 3) - rot(2, 6); h2 = rot(2, 6) - rot(4, 5)
    assert in_span(h1, su3) and in_span(h2, su3) and (h1*h2 - h2*h1) == sp.zeros(7, 7)
    # ad(h) on g2 (14x14), eigenvalues of i*ad(h) are integers
    Mb = sp.Matrix([list(D) for D in g2]).T
    Nb = (Mb.T * Mb).inv() * Mb.T
    def ad_on_g2(H):
        cols = []
        for D in g2:
            Z = H*D - D*H; sol = Nb * sp.Matrix(list(Z))
            assert Mb*sol == sp.Matrix(list(Z))
            cols.append(list(sol))
        return sp.Matrix(cols).T
    A1 = ad_on_g2(h1); A2 = ad_on_g2(h2)
    # simultaneous eigenvectors: eigenvalues of i*A1 (real ints) and the matching i*A2 values
    I = sp.I
    ev1 = (I*A1).eigenvects()
    roots = []
    for val1, mult, vecs in ev1:
        for v in vecs:
            w = I*A2*v
            # v is an eigenvector of A2 restricted? not necessarily; diagonalize A2 on the eigenspace
        # restrict i*A2 to the eigenspace of i*A1 with eigenvalue val1
        Vs = sp.Matrix.hstack(*vecs)
        B = (Vs.H * Vs).inv() * Vs.H * (I*A2) * Vs
        for val2, m2, _ in B.eigenvects():
            roots += [(sp.nsimplify(val1), sp.nsimplify(val2))] * m2
    roots = [r for r in roots if r != (0, 0)]
    assert len(roots) == 12 and len(set(roots)) == 12
    # weights of the 7 (eigenvalue pairs of i h1, i h2 on C^7)
    evA = (I*h1).eigenvects(); wts = []
    for val1, mult, vecs in evA:
        Vs = sp.Matrix.hstack(*vecs); B = (Vs.H * Vs).inv() * Vs.H * (I*h2) * Vs
        for val2, m2, _ in B.eigenvects(): wts += [(sp.nsimplify(val1), sp.nsimplify(val2))] * m2
    assert len(wts) == 7
    # positive system via a generic functional; simple roots = positive roots not a sum of two positive roots
    f = lambda r: 7*r[0] + 3*r[1]
    pos = [r for r in roots if f(r) > 0]; assert len(pos) == 6
    simple = [r for r in pos if not any((r[0]-p[0], r[1]-p[1]) in pos for p in pos)]
    assert len(simple) == 2
    # h_princ = c1 (i h1) + c2 (i h2) with alpha_k(h_princ) = 2 for both simple roots: alpha(h) = c1*alpha_1 + c2*alpha_2 (root coords are the eigenvalues)
    c1, c2 = sp.symbols('c1 c2')
    sol = sp.solve([c1*simple[0][0] + c2*simple[0][1] - 2, c1*simple[1][0] + c2*simple[1][1] - 2], [c1, c2])
    hp_weights = sorted([sp.nsimplify(sol[c1]*w[0] + sol[c2]*w[1]) for w in wts])
    # decompose the weight multiset into sl2 strings
    from collections import Counter
    cnt = Counter(hp_weights); dims = []
    while cnt:
        top = max(k for k, v in cnt.items() if v > 0)
        d = int(top) + 1   # string top, top-2, ..., -top
        for k in range(int(top), -int(top)-1, -2):
            cnt[k] -= 1
            if cnt[k] == 0: del cnt[k]
        dims.append(d)
    T1["branching_principal"] = sorted(dims, reverse=True)
    T1["_principal_weights"] = [int(x) for x in hp_weights]
    # control C-A1-1: (C^2)^{x3} under diagonal su(2): Casimir spectrum
    sx = sp.Matrix([[0, 1], [1, 0]]) / 2; sy = sp.Matrix([[0, -I], [I, 0]]) / 2; sz = sp.Matrix([[1, 0], [0, -1]]) / 2
    def kron3(m):
        E2 = sp.eye(2)
        return sp.kronecker_product(m, E2, E2) + sp.kronecker_product(E2, m, E2) + sp.kronecker_product(E2, E2, m)
    C = kron3(sx)**2 + kron3(sy)**2 + kron3(sz)**2
    ev = C.eigenvals()
    T1["control_sym3_quartet_mult"] = int(ev.get(sp.Rational(15, 4), 0) // 4)
    T1["holds"] = bool(T1["fs_indicator"] == -1 and T1["chi32_norm"] == 1 and T1["chi32_at_minus1"] == -4 and T1["seven_real"]
                       and T1["quartet_multiplicity_upper"] == 0 and all(4 not in T1[k] for k in ("branching_long_root", "branching_short_root", "branching_su3_sl2", "branching_principal")))
    R["T1"] = T1

    # ---------------- T2
    T2 = {}
    L = {a: Lmat(a) for a in range(1, 8)}
    for a in range(1, 8):
        for b in range(1, 8):
            S = L[a]*L[b] + L[b]*L[a]
            assert S == (-2*sp.eye(8) if a == b else sp.zeros(8, 8))
    T2["dim_der"] = len(g2)
    biv7 = [L[a]*L[b] for a in range(1, 8) for b in range(a+1, 8)]
    biv6 = [L[a]*L[b] for a in range(1, 7) for b in range(a+1, 7)]
    T2["dim_bivectors_7"] = span_dim(biv7); T2["dim_bivectors_6"] = span_dim(biv6)
    g2_8 = [to8(D) for D in g2]
    T2["g2_in_spin7"] = span_dim(g2_8 + biv7) == 21
    T2["dim_g2_cap_su4"] = 14 + 15 - span_dim(g2_8 + biv6)
    # (b) the spinorial 2O inside su(4)_L on (R^8, J=L_7): J-basis w = (e0, e1, e2, e4), J w = (e7, e3, e6, e5)
    import numpy as np
    J = L[7]
    wb = [unit(0), unit(1), unit(2), unit(4)]
    Jw = [list(J * sp.Matrix(w)) for w in wb]
    # basis change: real coords (x_k, y_k) -> vector sum x_k w_k + y_k Jw_k
    Bm = sp.Matrix.hstack(*[sp.Matrix(w) for w in wb], *[sp.Matrix(v) for v in Jw])   # 8x8, columns
    assert Bm.rank() == 8
    Bi = Bm.inv()
    def real_to_complex4(M8):   # M8 commuting with J -> complex 4x4
        Mb = Bi * M8 * Bm    # in (x,y) coordinates: [[A, -B],[B, A]]
        A_ = Mb[:4, :4]; B_ = Mb[4:, :4]
        assert Mb[:4, 4:] == -B_ and Mb[4:, 4:] == A_
        return A_ + I*B_
    def complex4_to_real(C):
        A_ = sp.re(C); B_ = sp.im(C)
        Mb = sp.zeros(8, 8); Mb[:4, :4] = A_; Mb[:4, 4:] = -B_; Mb[4:, :4] = B_; Mb[4:, 4:] = A_
        return Bm * Mb * Bi
    su4 = [real_to_complex4(M) for M in biv6]
    assert all(sp.simplify(M.trace()) == 0 and sp.simplify(M + M.H) == sp.zeros(4, 4) for M in su4)
    # spin-3/2 generators X_k = -i S_k (antihermitian, traceless)
    s3 = sp.sqrt(3)
    Sp = sp.Matrix([[0, s3, 0, 0], [0, 0, 2, 0], [0, 0, 0, s3], [0, 0, 0, 0]])   # S+ in the |3/2>,|1/2>,|-1/2>,|-3/2> basis
    Sm = Sp.T
    Sx = (Sp + Sm) / 2; Sy = (Sp - Sm) / (2*I); Sz = sp.diag(sp.Rational(3, 2), sp.Rational(1, 2), sp.Rational(-1, 2), sp.Rational(-3, 2))
    X = [-I*Sx, -I*Sy, -I*Sz]
    assert sp.simplify(X[0]*X[1] - X[1]*X[0] - X[2]) == sp.zeros(4, 4)
    Msu4 = sp.Matrix([list(M) for M in su4]).T
    for Xk in X:
        assert sp.Matrix.hstack(Msu4, sp.Matrix(list(Xk))).rank(simplify=True) == Msu4.rank(simplify=True), "spin-3/2 generator not in su(4)_L"
    # group elements D(q) = exp(2 theta n.X) for q = cos theta + sin theta (n.i); numeric
    Xn = [np.array(sp.N(Xk, 30).tolist(), dtype=complex) for Xk in X]
    def expm(M):
        w, V = np.linalg.eig(M); return (V @ np.diag(np.exp(w)) @ np.linalg.inv(V))
    Bm_n = np.array(sp.N(Bm).tolist(), dtype=float); Bi_n = np.linalg.inv(Bm_n)
    def c4_to_r8_n(Cm):
        A_ = Cm.real; B_ = Cm.imag
        Mb = np.zeros((8, 8)); Mb[:4, :4] = A_; Mb[:4, 4:] = -B_; Mb[4:, :4] = B_; Mb[4:, 4:] = A_
        return Bm_n @ Mb @ Bi_n
    defects = []; traces = []; autos = 0
    for q in Q:
        qf = [float(sp.N(x, 30)) for x in q]
        c = max(-1.0, min(1.0, qf[0])); theta = math.acos(c); s = math.sqrt(max(0.0, 1 - c*c))
        n = [x/s for x in qf[1:]] if s > 1e-12 else [0.0, 0.0, 1.0]
        D = expm(2*theta*(n[0]*Xn[0] + n[1]*Xn[1] + n[2]*Xn[2]))
        P8 = c4_to_r8_n(D)
        d = aut_defect_float(P8); defects.append((qf, d)); traces.append(np.trace(P8).real)
        if d < 1e-9: autos += 1
    T2["spinor_2O_order"] = 48; T2["spinor_2O_automorphism_count"] = autos
    nontriv = [d for qf, d in defects if not (abs(qf[0]) > 1 - 1e-12 and all(abs(x) < 1e-12 for x in qf[1:]))]
    T2["spinor_2O_min_automorphism_defect"] = float(min(nontriv))
    # quartet multiplicity in the 2O-character of C⊗O = R^8 ⊗ C: <tr P8, chi32> over 2O
    chis = [float(sp.N(chi32(q), 30)) for q in Q]
    mult = sum(t*ch for t, ch in zip(traces, chis)) / 48
    assert abs(mult - round(mult)) < 1e-8
    T2["spinor_2O_quartet_mult"] = int(round(mult))
    # (c) SL(2,7): g^2=1 count; ordinary FS sum with the 6 (Fano permutation rep) and 7 (P^1 permutation rep) machine-verified
    p = 7
    SL = [(a, b, c, d) for a, b, c, d in itertools.product(range(p), repeat=4) if (a*d - b*c) % p == 1]
    def m2(g, h):
        a, b, c, d = g; e_, f_, g_, h_ = h
        return ((a*e_ + b*g_) % p, (a*f_ + b*h_) % p, (c*e_ + d*g_) % p, (c*f_ + d*h_) % p)
    T2["sl27_order"] = len(SL); T2["sl27_sq1_count"] = sum(1 for g in SL if m2(g, g) == (1, 0, 0, 1))
    # P^1(F7) permutation character of PSL(2,7): 8 points; Steinberg 7 = perm - 1 ; FS via g^2
    def act(g, pt):
        a, b, c, d = g; x, y = pt   # column vector (x, y) -> (a x + b y, c x + d y), normalized
        nx, ny = (a*x + b*y) % p, (c*x + d*y) % p
        if ny == 0: return (1, 0) if nx else None
        inv = pow(ny, p-2, p); return (nx*inv % p, 1)
    P1 = [(x, 1) for x in range(p)] + [(1, 0)]
    def fix_count(g): return sum(1 for pt in P1 if act(g, pt) == pt)
    # FS indicator of the perm rep on P^1 (8-dim) = (1/|G|) sum fix(g^2); indicator of St = that - 1 (trivial contributes 1)
    fs_perm8 = Fraction(sum(fix_count(m2(g, g)) for g in SL), len(SL))
    fs_St = fs_perm8 - 1
    colls = fano_collineations(); assert len(colls) == 168
    def cfix(m): return sum(1 for x in range(1, 8) if m[x] == x)
    def compose(m, n): return {x: m[n[x]] for x in range(1, 8)}
    fs_perm7 = Fraction(sum(cfix(compose(m, m)) for m in colls), 168)
    fs_6 = fs_perm7 - 1
    assert fs_St == 1 and fs_6 == 1
    T2["fs_sum_ordinary"] = int(1 + 6*fs_6 + 7*fs_St + 8*1)   # nu(3)=nu(3bar)=0 and nu(8)=+1 adopted (citations)
    sols = []
    for n4 in (-1, 0, 1):
        for n6 in (-1, 0, 1):
            for n8 in (-1, 0, 1):
                if 8*n4 + 12*n6 + 8*n8 == 2 - T2["fs_sum_ordinary"]: sols.append((n4, n6, n8))
    T2["nu4_allowed"] = sorted({s[0] for s in sols}); T2["_fs_solutions"] = sols
    # involution lemma witnesses
    sig = sp.diag(*([1] + [1 if i in (1, 2, 4) else -1 for i in range(1, 8)]))
    T2["sigma_H_is_automorphism"] = is_aut(sig); T2["involution_trace"] = int(sum(sig[i, i] for i in range(1, 8)))
    bad = sp.diag(*([1] + [-1 if i == 7 else 1 for i in range(1, 8)]))
    T2["single_unit_negation_is_automorphism"] = is_aut(bad)
    # the realized signed Fano group: closure of the signed automorphism lifts
    def lifts_of(m):
        out = []
        for sgn in itertools.product([1, -1], repeat=7):
            signs = {i+1: sgn[i] for i in range(7)}
            if is_aut_signed(m, signs): out.append((tuple(m[i] for i in range(1, 8)), tuple(sgn)))
        return out
    def scompose(x, y):   # (x o y): first y then x ; elements e_i -> s_i e_{p_i}
        px, sx = x; py, sy = y
        p = tuple(px[py[i]-1] for i in range(7)); sgn = tuple(sy[i] * sx[py[i]-1] for i in range(7))
        return (p, sgn)
    def smat(x):
        return perm_matrix({i+1: x[0][i] for i in range(7)}, {i+1: x[1][i] for i in range(7)})
    a_inv = {1: 1, 2: 2, 4: 4, 3: 5, 5: 3, 6: 7, 7: 6}
    order7 = {x: x % 7 + 1 for x in range(1, 8)}
    order3 = {x: (2*x - 1) % 7 + 1 for x in range(1, 8)}
    gens = []
    for m in (a_inv, order7, order3): gens += lifts_of(m)
    ident = (tuple(range(1, 8)), tuple([1]*7))
    seen = {ident}; frontier = [ident]
    while frontier:
        new = []
        for x in frontier:
            for g_ in gens:
                z = scompose(x, g_)
                if z not in seen: seen.add(z); new.append(z)
        frontier = new
    group = list(seen)
    T2["group1344_order"] = len(group)
    T2["control_1344_all_automorphisms"] = all(is_aut_signed({i+1: x[0][i] for i in range(7)}, {i+1: x[1][i] for i in range(7)}) for x in group)
    # cross-check the fast test against the matrix test on a sample
    assert all(is_aut(smat(x)) for x in group[:5])
    R["_group1344"] = group; R["_scompose"] = scompose; R["_lifts_of"] = lifts_of; R["_ident"] = ident
    T2["holds"] = bool(T2["dim_g2_cap_su4"] == 8 and T2["g2_in_spin7"] and T2["spinor_2O_automorphism_count"] <= 1 and
                       T2["spinor_2O_min_automorphism_defect"] > 1e-6 and 1 not in T2["nu4_allowed"] and T2["involution_trace"] == -1 and
                       T2["sigma_H_is_automorphism"] and not T2["single_unit_negation_is_automorphism"] and T2["sl27_sq1_count"] == 2)
    R["T2"] = T2

    # ---------------- T3 (exact-sequence bookkeeping with adopted inputs; strings for groups)
    T3 = {}
    adopted = {"pi1_SU3": "0", "pi3_SU3": "Z", "pi4_SU3": "0", "pi_k_S6_k_le_5": "0", "pi4_SU2": "Z2", "pi3_U1": "0", "pi4_U1": "0",
               "pi1_SO3": "Z2", "pi2_S6": "0", "pi_k_S15_k_lt_15": "0"}
    # SU(3) -> G2 -> S6 : pi_k(SU3) -> pi_k(G2) -> pi_k(S6)
    T3["pi1_G2"] = 0 if (adopted["pi1_SU3"] == "0" and adopted["pi_k_S6_k_le_5"] == "0") else -1
    T3["pi4_G2"] = 0 if (adopted["pi4_SU3"] == "0" and adopted["pi_k_S6_k_le_5"] == "0") else -1
    T3["pi3_G2"] = "Z" if (adopted["pi3_SU3"] == "Z" and adopted["pi_k_S6_k_le_5"] == "0") else "?"   # pi4(S6)=0 -> pi3(SU3) -> pi3(G2) -> pi3(S6)=0
    T3["pi1_V"] = 0; T3["pi4_V"] = 0      # V = S15
    T3["no_internal_double_cover"] = bool(T3["pi1_G2"] == 0 and P0["phase_subgroup_order"] < 10**9)
    T3["envelope_in_O_kill"] = adopted["pi2_S6"] == "0"   # S2 -> S6 null-homotopic => pi4 map zero
    # locking inventory quotients: pi4(G2/H0) = coker(pi4 H0 -> pi4 G2) + ker(pi3 H0 -> pi3 G2); pi4(G2)=0; pi3 map = index (1) => injective
    for item in P0["locking_inventory"]:
        item["pi3_injective"] = item["sl2_generator_index"] != 0
        item["pi4_quotient"] = 0 if (T3["pi4_G2"] == 0 and item["pi3_injective"]) else -1
    # controls
    T3["controls_pi4_S2"] = "Z2" if (adopted["pi4_SU2"] == "Z2" and adopted["pi3_U1"] == "0" and adopted["pi4_U1"] == "0") else "?"
    T3["controls_pi4_S3"] = adopted["pi4_SU2"]
    T3["controls_pi1_SO3_mod_T"] = 2 * 12 if adopted["pi1_SO3"] == "Z2" else -1
    T3["holds"] = bool(T3["pi4_V"] == 0 and T3["pi1_V"] == 0 and T3["no_internal_double_cover"] and T3["envelope_in_O_kill"] and
                       all(it["pi4_quotient"] == 0 for it in P0["locking_inventory"]))
    T3["_adopted"] = adopted
    R["T3"] = T3

    # ---------------- T4
    T4 = {}
    fixers = [m for m in colls if m[1] == 1 and m[2] == 2 and m[4] == 4 and any(m[x] != x for x in (3, 5, 6, 7))]
    assert len(fixers) == 3
    lifts_of = R["_lifts_of"]; scompose = R["_scompose"]; ident = R["_ident"]
    def sorder(x):
        k, cur = 1, x
        while cur != ident: cur = scompose(x, cur); k += 1
        return k
    lifts = []
    for m in fixers:
        for x in lifts_of(m):
            lifts.append((sorder(x), int(sum(x[1][i] for i in range(7) if x[0][i] == i+1))))
    T4["lifts_total"] = len(lifts)
    T4["order2_count"] = sum(1 for o, t in lifts if o == 2); T4["order2_traces_set"] = sorted({t for o, t in lifts if o == 2})
    T4["order4_count"] = sum(1 for o, t in lifts if o == 4); T4["order4_traces_set"] = sorted({t for o, t in lifts if o == 4})
    T4["perm_char_involution"] = 3; T4["rho6_char_2A"] = 2; T4["gap"] = T4["perm_char_involution"] - T4["order2_traces_set"][0] if T4["order2_traces_set"] else None
    ok21, nu2ok, _, _ = F21_check(colls)
    T4["control_F21_unsigned_1_3_3bar"] = bool(ok21); T4["nu2_unsigned_automorphism"] = bool(nu2ok)
    T4["_unsigned_automorphism_count_of_168"] = len(unsigned_automorphisms(colls))
    T4["holds"] = bool(T4["order2_traces_set"] == [-1] and T4["lifts_total"] == 24 and T4["gap"] == 4)
    R["T4"] = T4

    # ---------------- group1344 split/non-split (E-A1-6(a))
    G1344 = R["_group1344"]
    kernel = [x for x in G1344 if x[0] == tuple(range(1, 8))]
    assert len(kernel) == 8
    def perm_order(m):
        k, cur = 1, dict(m)
        while any(cur[x] != x for x in range(1, 8)): cur = compose(m, cur); k += 1
        return k
    def inv_perm(m): return {v: k for k, v in m.items()}
    a = a_inv; b_found = None
    for b in colls:
        if perm_order(b) != 3: continue
        ab = compose(a, b)
        comm = compose(compose(a, b), compose(inv_perm(a), inv_perm(b)))
        if perm_order(ab) == 7 and perm_order(comm) == 4: b_found = b; break
    assert b_found is not None
    lifts_a = lifts_of(a); lifts_b = lifts_of(b_found); assert len(lifts_a) == 8 and len(lifts_b) == 8
    def gen_order(gs):
        seen = {ident}; frontier = [ident]
        while frontier:
            new = []
            for x in frontier:
                for g_ in gs:
                    z = scompose(x, g_)
                    if z not in seen: seen.add(z); new.append(z)
            frontier = new
        return len(seen)
    comps = 0; pairs = 0; orders = {}
    for A_ in lifts_a:
        for B_ in lifts_b:
            o = gen_order([A_, B_]); pairs += 1; orders[o] = orders.get(o, 0) + 1
            if o == 168: comps += 1
    R["group1344"] = {"order": len(G1344), "split": comps > 0, "complements_found": comps, "lift_pairs_tested": pairs, "_orders_seen": {str(k): v for k, v in orders.items()}}
    return R

# ----------------------------------------------------------------------------- Phase 1b
def phase1b(P1):
    B = {}
    # P-C: the complex unit of C⊗O commutes with every L_a (as real 16x16 maps: L_a ⊗ I2 vs I8 ⊗ J2)
    L = {a: Lmat(a) for a in range(1, 8)}
    J2 = sp.Matrix([[0, -1], [1, 0]]); I2 = sp.eye(2)
    Jc = sp.kronecker_product(sp.eye(8), J2)
    central = all((sp.kronecker_product(L[a], I2) * Jc - Jc * sp.kronecker_product(L[a], I2)) == sp.zeros(16, 16) for a in range(1, 8))
    # sedenions: Cayley-Dickson doubling (a,b)(c,d) = (ac - conj(d) b, d a + b conj(c)); e8 = (0,1)
    def oconj(x): return [x[0]] + [-v for v in x[1:]]
    def smul(P_, Q_):
        a, b = P_; c, d = Q_
        left = [x - y for x, y in zip(omul(a, c), omul(oconj(d), b))]
        right = [x + y for x, y in zip(omul(d, a), omul(b, oconj(c)))]
        return (left, right)
    z8 = [sp.Integer(0)] * 8
    e8 = (z8, unit(0))
    anti = all(smul(e8, (unit(a), z8)) == tuple([-x for x in v] for v in smul((unit(a), z8), e8)) for a in range(1, 8))
    B["P_C"] = {"complex_unit_central": bool(central), "e8_anticommutes": bool(anti), "e8_central": bool(not anti and False) if not anti else False,
                "disposition": "CLOSED-BY-INSTANTIATION" if (central and anti) else "OPEN"}
    B["P_C"]["e8_central"] = False if anti else True
    # H screen: criteria evaluated from the exact/adopted facts; code rule (stated in the execution report):
    # ADMISSIBLE-IMPORT iff i,ii in {pass} and iii in {pass, conditional} and iv in {dynamical, kinematic}; else EXCLUDED(<criteria with value 'fail', in order>)
    kill = P1["T3"]["envelope_in_O_kill"]
    long_root_2plus2 = P1["T1"]["branching_long_root"] == [2, 2, 1, 1, 1]
    H = {
        "H1": {"i": "fail", "ii": "pass", "iii": "fail" if kill else "pass", "iv": "n/a", "role": "control"},
        "H2": {"i": "pass", "ii": "pass", "iii": "pass" if P1["T3"]["controls_pi4_S2"] == "Z2" else "fail", "iv": "dynamical", "role": "candidate"},
        "H3": {"i": "pass", "ii": "pass", "iii": "conditional", "iv": "kinematic", "role": "candidate"},
        "H4": {"i": "fail", "ii": "pass" if long_root_2plus2 else "fail", "iii": "n/a", "iv": "n/a", "role": "candidate"},
        "H5": {"i": "fail" if anti else "pass", "ii": "fail", "iii": "n/a", "iv": "n/a", "role": "candidate"},
    }
    for h, d in H.items():
        adm = d["i"] == "pass" and d["ii"] == "pass" and d["iii"] in ("pass", "conditional") and d["iv"] in ("dynamical", "kinematic")
        d["code"] = "ADMISSIBLE-IMPORT" if adm else "EXCLUDED(" + ",".join(k for k in ("i", "ii", "iii", "iv") if d[k] == "fail") + ")"
    B["H_screen"] = H
    B["admissible"] = sorted(h for h, d in H.items() if d["code"] == "ADMISSIBLE-IMPORT")
    inside = [h for h in B["admissible"] if h not in ("H2", "H3")]   # candidates inside the field content of record that pass
    B["I5_registered"] = bool(len(B["admissible"]) > 0 and not inside)
    return B

# ----------------------------------------------------------------------------- Phase 2
def phase2():
    Z = {"object": "fano_line_texture_L124_homogeneous_GP_2D", "control_object": "nonline_texture_L123", "profile_id": "lockrec-A-2.6",
         "dimension_note": "2D witness; contractibility of the 2pi loop in the orbit only"}
    r, ph = sp.symbols('r phi', positive=True)
    f = sp.pi / (1 + r**2)
    # O = phi_abc * integral n.(d_x n x d_y n) d^2x  (real texture in the 3-plane {a,b,c}); the integral = 2 pi * int sin f f' dr = 2pi[-cos f]_0^inf
    geom = 2*sp.pi*(-sp.cos(f.subs(r, sp.oo)) + sp.cos(f.subs(r, 0)))   # exact: 2pi(-1 + (-1)) = -4pi
    geom = sp.simplify(geom)
    assert geom == -4*sp.pi
    # numeric cross-check of the integral 2pi int_0^inf sin(f) f'(r) dr
    fr = sp.diff(f, r); num = sp.N(2*sp.pi*sp.Integral(sp.sin(f)*fr, (r, 0, sp.oo)), 15)
    assert abs(float(num) - float(-4*sp.pi)) < 1e-9
    O_line = phi(1, 2, 4) * geom; O_non = phi(1, 2, 3) * geom
    Z["O_line_abs"] = float(abs(O_line)); Z["O_nonline_abs"] = float(abs(O_non))
    Z["O_nonzero_on_line"] = bool(O_line != 0); Z["O_zero_on_nonline"] = bool(O_non == 0)
    # stabilizer family M(p,q): h -> q h q̄ on H_L = <1,e1,e2,e4>; x = k e3 (k in H_L) -> (p k q̄) e3 on H_L^perp
    HL = [0, 1, 2, 4]; HLp = [3, 5, 6, 7]
    def oc(x): return [x[0]] + [-v for v in x[1:]]
    def proj(x, idxs): return [x[i] if i in idxs else sp.Integer(0) for i in range(8)]
    def Mpq(pq, qq):
        cols = []
        for j in range(8):
            x = unit(j)
            if j in HL:
                y = omul(omul(qq, x), oc(qq))
            else:
                k = [-v for v in omul(x, unit(3))]          # k = -x e3  (so that k e3 = x)
                assert omul(k, unit(3)) == x
                y = omul(omul(omul(pq, k), oc(qq)), unit(3))
            cols.append(y)
        return sp.Matrix(cols).T
    def unit_quat_e4(t):   # rational point on the circle: q = c + s e4
        c = (1 - t**2) / (1 + t**2); s = 2*t / (1 + t**2)
        v = [sp.Integer(0)] * 8; v[0] = c; v[4] = s; return v
    def unit_quat_gen(t1, t2):   # a generic rational unit in H_L via stereographic-like parametrization
        d = 1 + t1**2 + t2**2
        v = [sp.Integer(0)] * 8; v[0] = (1 - t1**2 - t2**2)/d; v[1] = 2*t1/d; v[2] = 2*t2/d
        assert sum(x*x for x in v) == 1
        return v
    one = unit(0); minus = [-x for x in one]
    checks = []
    for t in (sp.Rational(1, 3), sp.Rational(2, 5)):
        q = unit_quat_e4(t)
        for pname, pp in (("1", one), ("-1", minus), ("q", q), ("generic", unit_quat_gen(sp.Rational(1, 2), sp.Rational(-1, 3)))):
            M = Mpq(pp, q)
            checks.append((str(t), pname, is_aut(M)))
            # texture invariance: M rotates Im H_L about e4 by alpha with cos a = c^2 - s^2, sin a = 2cs
            c = q[0]; s = q[4]; ca = c*c - s*s; sa = 2*c*s
            n = [sp.Integer(0)] * 8; n[1] = sp.Rational(3, 5); n[2] = sp.Rational(4, 5)   # a point on the texture sphere (cos f = 0 slice)
            Mn = M * sp.Matrix(n)
            expect = [sp.Integer(0)] * 8; expect[1] = ca*n[1] - sa*n[2]; expect[2] = sa*n[1] + ca*n[2]
            assert list(Mn) == expect, "rotation law failed"
    assert all(ok for _, _, ok in checks)
    # kernel SU(2)_long: M(p, 1) fixes H_L pointwise and is an automorphism
    Mk = Mpq(unit_quat_gen(sp.Rational(2, 3), sp.Rational(1, 5)), one)
    assert is_aut(Mk) and all(Mk[:, j] == sp.Matrix(unit(j)) for j in HL)
    Z["stab_internal_image"] = "SO4_Stab_HL"; Z["stab_kernel"] = "SU2_long"; Z["stab_subdirect"] = True
    Z["pi0_stab"] = 1   # the family (alpha, p) is connected; no other element of SO(2)xG2 fixes the texture (values of n span Im H_L)
    # loop images at alpha = 2pi: q = -1 : (p=1) -> sigma_H ; (p=-1) -> Id
    M1 = Mpq(one, minus); M2 = Mpq(minus, minus)
    sig = sp.diag(*([1] + [1 if i in (1, 2, 4) else -1 for i in range(1, 8)]))
    assert M1 == sig and M2 == sp.eye(8)
    Z["loop_images"] = ["Id", "sigma_H"]
    ev = sig.eigenvals(); Z["sigma_H_eigen_plus1"] = int(ev[1]); Z["sigma_H_eigen_minus1"] = int(ev[-1])
    Z["label"] = "INTERNAL-HOLONOMY-GAUGE"
    # pi1(Orbit) = pi0(Stab) since the diagonal loop (q_alpha, q_alpha) closes at (-1,-1) ~ Id and winds once in pi1(SO(2)) = Z
    Z["pi1_orbit"] = 0 if Z["pi0_stab"] == 1 else -1
    # chiral pair: antisymmetric coupling on the line (1,2,4) with eigenvectors e1 -/+ i e2; rotation about e4 acts as e^{±i alpha}
    t = sp.Rational(1, 3); q = unit_quat_e4(t); M = Mpq(one, q); c = q[0]; s = q[4]; ca = c*c - s*s; sa = 2*c*s
    A3 = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]) * phi(1, 2, 4)
    evs = A3.eigenvects()
    ordinary = True
    for val, m, vecs in evs:
        if val == 0: continue
        v = vecs[0]; v8 = sp.zeros(8, 1); v8[1] = v[0]; v8[2] = v[1]; v8[4] = v[2]
        w = M * v8
        lam = sp.simplify(w[1] / v8[1]) if v8[1] != 0 else sp.simplify(w[2] / v8[2])
        assert sp.simplify(w - lam*v8) == sp.zeros(8, 1)
        ordinary = ordinary and sp.simplify(sp.Abs(lam) - 1) == 0 and (sp.simplify(lam - (ca + sp.I*sa)) == 0 or sp.simplify(lam - (ca - sp.I*sa)) == 0)
    Z["chiral_pair_character_ordinary"] = bool(ordinary)
    Z["_checks"] = checks
    return Z

# ----------------------------------------------------------------------------- Phase 3
def phase3(P0, P1, B, Z):
    holds = {t: P1[t]["holds"] for t in ("T1", "T2", "T3", "T4")}
    c0 = P0["controls"]
    controls = all(c0[k] is True for k in ("L_perp_zero_mode", "F21_split_1_3_3bar", "generic_so16_fails_margin_positive"))
    controls = controls and P1["T1"]["control_sym3_quartet_mult"] == 1 and P1["T2"]["control_1344_all_automorphisms"] is True and P1["T2"]["spinor_2O_quartet_mult"] == 2
    controls = controls and P1["T3"]["controls_pi4_S2"] == "Z2" and P1["T3"]["controls_pi4_S3"] == "Z2" and P1["T3"]["controls_pi1_SO3_mod_T"] == 24
    controls = controls and P1["T4"]["control_F21_unsigned_1_3_3bar"] is True and P1["T4"]["nu2_unsigned_automorphism"] is True and Z["O_zero_on_nonline"] is True
    if not controls: verdict = "INDETERMINATE"
    elif not P0["sym_int_pinned"]: verdict = "UNDECIDED-BY-SUBSTRATE"
    elif (not P0["spatial_internal_direct_product"]) or any(h is not True for h in holds.values()): verdict = "ASSIGNMENT-II-REALIZABLE"
    else: verdict = "ASSIGNMENT-I-FORCED"
    return {"verdict": verdict, "tests_holding": sorted(t for t, h in holds.items() if h is True), "admissible_H": list(B["admissible"]),
            "I5": bool(B["I5_registered"]), "controls_all_pass": bool(controls)}

# ----------------------------------------------------------------------------- run
def strip_private(d):
    if isinstance(d, dict): return {k: strip_private(v) for k, v in d.items() if not k.startswith("_")}
    if isinstance(d, list): return [strip_private(x) for x in d]
    return d

CITATIONS = {
    "pi_k(SU3), pi_k(S6), pi4(SU2), pi_k(U1), pi_k(S15)": "textbook homotopy (Bott periodicity / stable range; Hatcher, Algebraic Topology, ch. 4); Mimura 1967 J. Math. Kyoto Univ. 6 as the canonical G2 table (not relied on)",
    "FR criterion pi1(Config)=pi4(target)": "Finkelstein-Rubinstein 1968; Giulini 1993 (hep-th/9301101); Krusch-Speight 2006 (hep-th/0503067)",
    "even multiplicity of quaternionic irreps in real representations": "standard (Frobenius-Schur theory; Serre, Linear Representations of Finite Groups, §13.2)",
    "PSL(2,7) ordinary indicators nu(3)=nu(3bar)=0, nu(8)=+1; SL(2,7) Galois pairings": "ATLAS of Finite Groups; ledger §2.77 / §2.D-FC (the 6 and 7 machine-verified here)",
    "two PSL(2,7) classes in G2; non-split 2^3.PSL(2,7)": "Cohen-Wales 1983 via Evans-Pugh arXiv:1404.1866 Table 1 (cross-check only)",
    "SU(3)=Stab_G2(e7), G2/SU(3)=S6, Fix_G2(H)=SU(2)": "Günaydin-Gürsey 1973; nLab G2",
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("run", "selftest"): print(__doc__); return 2
    out = "."
    if "--out" in sys.argv: out = sys.argv[sys.argv.index("--out") + 1]
    t0 = time.time(); log = []
    scan, glog = guards(); log += glog
    inst_md5 = md5_file(os.path.abspath(__file__))
    extract_text = open(EXTRACT, encoding="utf-8").read()
    if sys.argv[1] == "selftest":
        print("\n".join(log)); print("guards OK; selftest = guards only (all computations are the run)"); return 0
    g2 = derivation_algebra(); assert len(g2) == 14; log.append(f"g2 built: dim {len(g2)}  [{time.time()-t0:.1f}s]")
    P0 = phase0(g2, extract_text); log.append(f"Phase 0 done  [{time.time()-t0:.1f}s]  sym_int_continuous={P0['sym_int_continuous']} dim={P0['sym_int_continuous_dim']} (imaginary sector {P0['_imag_sector_continuous_dim']}; psi0 phase preserves O: {P0['_psi0_phase_preserves_O']}) pinned={P0['sym_int_pinned']}")
    colls = fano_collineations(); ok21, nu2ok, _, _ = F21_check(colls)
    P0["controls"]["F21_split_1_3_3bar"] = bool(ok21)
    if not all(P0["controls"].values()): raise SystemExit("HALT: a Phase-0 control failed: " + json.dumps(P0["controls"]))
    P1 = phase1(g2, P0); holds = {t: P1[t]['holds'] for t in ('T1', 'T2', 'T3', 'T4')}; log.append(f"Phase 1 done  [{time.time()-t0:.1f}s]  holds={holds}  group1344={P1['group1344']['order']} split={P1['group1344']['split']}")
    B = phase1b(P1); log.append(f"Phase 1b done [{time.time()-t0:.1f}s]  admissible={B['admissible']}")
    Z = phase2(); log.append(f"Phase 2 done  [{time.time()-t0:.1f}s]  pi1_orbit={Z['pi1_orbit']} loop_images={Z['loop_images']}")
    V = phase3(P0, P1, B, Z); log.append(f"Phase 3 done  [{time.time()-t0:.1f}s]  verdict={V['verdict']}")
    ck = {"gate": GATE, "leg": "chat", "instrument_md5": inst_md5, "memo_lock_md5": MEMO_MD5, "ledger_base_md5": LEDGER_BASE_MD5,
          "t1_list_md5": T1_MD5, "action_extract_md5": EXTRACT_MD5, "t1_scan": scan, "elections": ELECTIONS,
          "phase0": strip_private(P0), "phase1": {k: strip_private(v) for k, v in P1.items() if not k.startswith("_")},
          "phase1b": strip_private(B), "phase2": strip_private(Z), "phase3": V,
          "citations": CITATIONS, "extras": {"phase0_margin": P0["_margin"], "phase0_imag_sector_continuous_dim": P0["_imag_sector_continuous_dim"],
                                            "phase0_psi0_phase_preserves_O": P0["_psi0_phase_preserves_O"], "phase0_terms_of_record": P0["_terms_of_record"],
                                            "T2_note": "spinor_2O_automorphism_count counts elements with zero defect; the identity is one of them (lock record A-2.3 wording); the minimum defect is over 2O minus {+1,-1}", "principal_weights": P1["T1"]["_principal_weights"],
                                            "fs_solutions": P1["T2"]["_fs_solutions"], "unsigned_automorphisms_of_168": P1["T4"]["_unsigned_automorphism_count_of_168"],
                                            "group1344_orders_seen_in_complement_search": P1["group1344"]["_orders_seen"], "phase2_automorphism_checks": Z["_checks"],
                                            "adopted_homotopy_inputs": P1["T3"]["_adopted"], "runtime_s": round(time.time() - t0, 1)}}
    os.makedirs(out, exist_ok=True)
    cp = os.path.join(out, "g_2a_a1_chatleg_checkpoint.json")
    open(cp, "w", encoding="utf-8").write(json.dumps(ck, indent=1, ensure_ascii=False, sort_keys=True, default=str))
    open(os.path.join(out, "run_chatleg.log"), "w", encoding="utf-8").write("\n".join(log) + "\n")
    print("\n".join(log)); print("checkpoint", cp, md5_file(cp))
    return 0

if __name__ == "__main__":
    sys.exit(main())
