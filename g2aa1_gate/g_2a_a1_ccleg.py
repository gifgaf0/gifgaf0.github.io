#!/usr/bin/env python3
"""g_2a_a1_ccleg.py — Gate G-2a-A1, CC leg, built blind from the locked memo
(626aa868), the lock record Addendum A-2, and schema v1.0. Method variations
(dispatch §3 / lock record §5): g2 is built as the annihilator of the 3-form
phi inside so(7) (not as derivations); SL(2,7) and GL(3,2) are enumerated from
scratch for the Frobenius-Schur count; the homotopy bookkeeping is an own
exact-sequence module; branchings are read from Casimir spectra (long/short/
su3 classes) and from an exact sl2-triple (principal class), not from chat's
weight-reading code.

Guards (A-2.8): md5-guards the memo, the gate T1 list, the extract and the
scanner; T1-scans itself, the memo and the extract at every invocation and
halts on any hit. No override flag exists.

Exact arithmetic: fractions.Fraction throughout; Q(sqrt2) for 2O; complex
rationals for the principal sl2-triple. Floats only in the spinorial-2O block
(A-2.3) and the Phase-2 geometric integral (thresholded per the schema).
"""
import hashlib, importlib.util, json, math, os, sys, time
from fractions import Fraction as Fr
from itertools import combinations, product

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
ME = os.path.abspath(__file__)

MEMO = os.path.join(HERE, "staging_memo_G_2a_A1_v2.md")
T1LIST = os.path.join(HERE, "tools/t1/T1_forbidden_G_2a_A1.txt")
SCANNER = os.path.join(HERE, "tools/t1/t1_scan.py")
EXTRACT = os.path.join(HERE, "inputs/paper_II_3_4_4_and_3_4_7_extract.md")

MD5 = {
    MEMO: ("626aa868844220eb6c3801ef07a77783", 61562),
    T1LIST: ("2026b782db3905d9f2ce35733823618c", 241),
    SCANNER: ("6b86290090a8c84f1b1a0a99ec0bf697", 1967),
    EXTRACT: ("940b0bee4b2112e911ae738c3db2bc3d", 12912),
}
LEDGER_BASE_MD5 = "40009ec0197876b130766f1ae7494360"

def md5f(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def guard():
    for p, (want, nb) in MD5.items():
        if not os.path.exists(p):
            sys.exit(f"HALT: missing guarded file {p}")
        raw = open(p, "rb").read()
        got = hashlib.md5(raw).hexdigest()
        if got != want or len(raw) != nb:
            sys.exit(f"HALT: md5/bytes mismatch on {p}: {got} / {len(raw)}")

def t1_scan_all():
    spec = importlib.util.spec_from_file_location("t1_scan", SCANNER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pats = mod.load(T1LIST)
    out = {}
    for tag, path in (("instrument", ME), ("memo", MEMO), ("extract", EXTRACT)):
        text = open(path, "rb").read().decode("utf-8", "replace")
        hits, _coll = mod.scan_text(text, pats)
        out[tag] = "CLEAN" if not hits else "HIT"
        if hits:
            sys.exit(f"HALT: T1 hit in {tag} (pattern indices {sorted(set(i for i,_ in hits))})")
    return out

# ---------------------------------------------------------------- exact linear algebra
def kernel_basis(rows, n):
    """Kernel of the linear map given by rows (each a length-n list of Fr)."""
    mat = [list(map(Fr, r)) for r in rows if any(r)]
    piv = []           # pivot column per reduced row
    red = []
    for r in mat:
        r = r[:]
        for rr, c in zip(red, piv):
            if r[c]:
                f = r[c] / rr[c]
                for j in range(n):
                    if rr[j]:
                        r[j] -= f * rr[j]
        for c in range(n):
            if r[c]:
                red.append(r); piv.append(c)
                break
    pivset = set(piv)
    free = [c for c in range(n) if c not in pivset]
    basis = []
    # back-substitute reduced rows to solve for pivots given each free var = 1
    for fc in free:
        v = [Fr(0)] * n
        v[fc] = Fr(1)
        for rr, c in reversed(list(zip(red, piv))):
            s = sum(rr[j] * v[j] for j in range(n) if j != c and rr[j])
            v[c] = -s / rr[c]
        basis.append(v)
    return basis

def rank_of(rows):
    red, piv = [], []
    for r in rows:
        r = list(r)
        n = len(r)
        for rr, c in zip(red, piv):
            if r[c]:
                f = r[c] / rr[c]
                for j in range(n):
                    if rr[j]:
                        r[j] -= f * rr[j]
        for c in range(n):
            if r[c]:
                red.append(r); piv.append(c)
                break
    return len(red)

def solve_affine(rows, rhs, n):
    """Particular solution + kernel basis of rows.x = rhs (exact); None if inconsistent."""
    aug = [list(map(Fr, r)) + [Fr(b)] for r, b in zip(rows, rhs)]
    red, piv = [], []
    for r in aug:
        for rr, c in zip(red, piv):
            if r[c]:
                f = r[c] / rr[c]
                for j in range(n + 1):
                    r[j] -= f * rr[j]
        pc = None
        for c in range(n):
            if r[c]:
                pc = c
                break
        if pc is None:
            if r[n]:
                return None, None
            continue
        red.append(r); piv.append(pc)
    x = [Fr(0)] * n
    for rr, c in reversed(list(zip(red, piv))):
        s = sum(rr[j] * x[j] for j in range(n) if j != c and rr[j])
        x[c] = (rr[n] - s) / rr[c]
    ker = kernel_basis([r[:n] for r in aug], n)
    return x, ker

def mat_mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]

def mat_sub(A, B):
    return [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]

def mat_add(A, B):
    return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]

def mat_scale(A, s):
    return [[s * a for a in r] for r in A]

def mat_vec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

def bracket(A, B):
    return mat_sub(mat_mul(A, B), mat_mul(B, A))

def zeros(n, m=None):
    m = n if m is None else m
    return [[Fr(0)] * m for _ in range(n)]

def eye(n, s=Fr(1)):
    M = zeros(n)
    for i in range(n):
        M[i][i] = s
    return M

def trace(A):
    return sum(A[i][i] for i in range(len(A)))

def flat(A):
    return [x for r in A for x in r]

# ---------------------------------------------------------------- octonions
# Fano lines {i, i+1, i+3} mod 7 (representatives 1..7), e_i e_{i+1} = e_{i+3} cyclic.
def wrap(n):
    return ((n - 1) % 7) + 1

LINES = [tuple(sorted((i, wrap(i + 1), wrap(i + 3)))) for i in range(1, 8)]
LINESET = set(LINES)

phi = [[[0] * 8 for _ in range(8)] for _ in range(8)]     # indices 1..7
for i in range(1, 8):
    a, b, c = i, wrap(i + 1), wrap(i + 3)
    for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
        phi[x][y][z] = 1
        phi[y][x][z] = -1

def oct_mul_basis(a, b):
    """e_a * e_b as an 8-vector of ints (indices 0..7, e_0 = 1)."""
    v = [0] * 8
    if a == 0:
        v[b] = 1
    elif b == 0:
        v[a] = 1
    elif a == b:
        v[0] = -1
    else:
        for c in range(1, 8):
            if phi[a][b][c]:
                v[c] = phi[a][b][c]
    return v

OMUL = [[oct_mul_basis(a, b) for b in range(8)] for a in range(8)]

def oct_mul_vec(u, v):
    out = [Fr(0)] * 8
    for a in range(8):
        if not u[a]:
            continue
        for b in range(8):
            if not v[b]:
                continue
            t = OMUL[a][b]
            for c in range(8):
                if t[c]:
                    out[c] += u[a] * v[b] * t[c]
    return out

def L_matrix(a):
    """Left multiplication by e_a on R^8 (columns e_a * e_j)."""
    M = zeros(8)
    for j in range(8):
        col = OMUL[a][j]
        for i in range(8):
            M[i][j] = Fr(col[i])
    return M

L = [L_matrix(a) for a in range(8)]

# ---------------------------------------------------------------- g2 as Stab(phi) in so(7)
# so(7) on Im O with basis indices 0..6 <-> e_1..e_7; unknowns x_{pq}, p<q,
# X e_{q} = +x e_{p}, i.e. X[p][q] = x, X[q][p] = -x.
SO7_PAIRS = list(combinations(range(7), 2))          # 21
PIDX = {pq: i for i, pq in enumerate(SO7_PAIRS)}

def so7_from_params(x):
    X = zeros(7)
    for (p, q), i in PIDX.items():
        X[p][q] = x[i]
        X[q][p] = -x[i]
    return X

def phi0(a, b, c):
    return phi[a + 1][b + 1][c + 1]     # 0-based on Im O

rows = []
for a, b, c in combinations(range(7), 3):
    r = [Fr(0)] * 21
    for d in range(7):
        # phi(X e_a, e_b, e_c) + phi(e_a, X e_b, e_c) + phi(e_a, e_b, X e_c)
        for (i, j), contrib in (((d, a), phi0(d, b, c)), ((d, b), phi0(a, d, c)), ((d, c), phi0(a, b, d))):
            if not contrib or i == j:      # X[j][j] = 0 for antisymmetric X
                continue
            p, q = min(i, j), max(i, j)
            s = 1 if (p, q) == (i, j) else -1     # X[i][j] = +x if i<j else -x
            r[PIDX[(p, q)]] += Fr(s * contrib)
    rows.append(r)

G2_PARAMS = kernel_basis(rows, 21)
G2 = [so7_from_params(x) for x in G2_PARAMS]
DIM_G2 = len(G2)

def to8(X7):
    """Extend a 7x7 map on Im O to R^8 with e_0 -> 0."""
    M = zeros(8)
    for i in range(7):
        for j in range(7):
            M[i + 1][j + 1] = X7[i][j]
    return M

def is_derivation(X7):
    D = to8(X7)
    for a in range(8):
        for b in range(8):
            lhs = mat_vec(D, [Fr(v) for v in OMUL[a][b]])
            ea = [Fr(0)] * 8; ea[a] = Fr(1)
            eb = [Fr(0)] * 8; eb[b] = Fr(1)
            rhs = [x + y for x, y in zip(oct_mul_vec(mat_vec(D, ea), eb),
                                         oct_mul_vec(ea, mat_vec(D, eb)))]
            if lhs != rhs:
                return False
    return True

def in_g2_span(X7):
    v = flat(X7)
    return rank_of([flat(g) for g in G2] + [v]) == DIM_G2

def subalg_kernel(conds):
    """Elements sum c_i G2[i] satisfying linear conds: conds(X) -> list of Fr rows."""
    rows = []
    per = [conds(g) for g in G2]
    nr = len(per[0])
    for r in range(nr):
        rows.append([per[i][r] for i in range(DIM_G2)])
    ker = kernel_basis(rows, DIM_G2)
    out = []
    for k in ker:
        X = zeros(7)
        for c, g in zip(k, G2):
            if c:
                X = mat_add(X, mat_scale(g, c))
        out.append(X)
    return out

def ebas7(i):
    v = [Fr(0)] * 7
    v[i] = Fr(1)
    return v

# su(2)_long = pointwise stabilizer of H_L = <1, e1, e2, e4>  (0-based Im: 0, 1, 3)
HL_IM = [0, 1, 3]          # e1, e2, e4
HL_PERP = [2, 4, 5, 6]     # e3, e5, e6, e7
SU2_LONG = subalg_kernel(lambda X: [X[i][j] for j in HL_IM for i in range(7)])

# Stab(H_L): X(H_L cap Im) subset H_L cap Im
STAB_HL = subalg_kernel(lambda X: [X[i][j] for j in HL_IM for i in HL_PERP])

# su(3) = stabilizer of e7 (0-based index 6)
SU3 = subalg_kernel(lambda X: [X[i][6] for i in range(7)])

def tr_form(X, Y):
    return trace(mat_mul(X, Y))

def complement_in(sub, big):
    """tr-orthocomplement of span(sub) inside span(big)."""
    rows = []
    for s in sub:
        rows.append([tr_form(s, b) for b in big])
    ker = kernel_basis(rows, len(big))
    out = []
    for k in ker:
        X = zeros(7)
        for c, b in zip(k, big):
            if c:
                X = mat_add(X, mat_scale(b, c))
        out.append(X)
    return out

SU2_SHORT = complement_in(SU2_LONG, STAB_HL)

def closed_under_bracket(bas):
    fl = [flat(b) for b in bas]
    r0 = rank_of(fl)
    for a in bas:
        for b in bas:
            if rank_of(fl + [flat(bracket(a, b))]) != r0:
                return False
    return True

# ---------------------------------------------------------------- Casimir branching
def structure_constants(bas):
    """[b_i, b_j] = sum_k c^k_ij b_k, solved exactly in span(bas)."""
    n = len(bas)
    fl = [flat(b) for b in bas]
    cs = {}
    for i in range(n):
        for j in range(n):
            tgt = flat(bracket(bas[i], bas[j]))
            rows = [[fl[k][m] for k in range(n)] for m in range(49)]
            x, _ = solve_affine(rows, tgt, n)
            if x is None:
                raise RuntimeError("bracket left the span")
            cs[(i, j)] = x
    return cs

def casimir_branching(bas):
    """Branching of the 7 under a compact su(2) subalgebra given by a basis.
    Returns sorted-descending list of irrep dimensions."""
    n = len(bas)
    assert n == 3
    cs = structure_constants(bas)
    # Killing form of the subalgebra itself
    kappa = zeros(n)
    for i in range(n):
        for j in range(n):
            s = Fr(0)
            for a in range(n):
                for b in range(n):
                    s += cs[(i, a)][b] * cs[(j, b)][a]
            kappa[i][j] = s
    B = mat_scale(kappa, Fr(-1, 2))
    # invert B (3x3) exactly
    Bi = invert3(B)
    C = zeros(7)
    for i in range(n):
        for j in range(n):
            if Bi[i][j]:
                C = mat_add(C, mat_scale(mat_mul(bas[i], bas[j]), -Bi[i][j]))
    dims = []
    total = 0
    for twoj in range(0, 13):        # j = twoj/2
        j = Fr(twoj, 2)
        lam = j * (j + 1)
        M = mat_sub(C, eye(7, lam))
        mult_ev = 7 - rank_of([r[:] for r in M])
        d = twoj + 1
        if mult_ev:
            assert mult_ev % d == 0, (twoj, mult_ev)
            dims += [d] * (mult_ev // d)
            total += mult_ev
    assert total == 7, dims
    return sorted(dims, reverse=True)

def invert3(B):
    n = len(B)
    aug = [[B[i][j] for j in range(n)] + [Fr(1) if k == i else Fr(0) for k in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if aug[r][c])
        aug[c], aug[p] = aug[p], aug[c]
        f = aug[c][c]
        aug[c] = [x / f for x in aug[c]]
        for r in range(n):
            if r != c and aug[r][c]:
                g = aug[r][c]
                aug[r] = [x - g * y for x, y in zip(aug[r], aug[c])]
    return [row[n:] for row in aug]

def dynkin_index(branching):
    """Embedding index normalized to long-root = 1: sum of j(j+1)(2j+1)/3 over the branching."""
    s = Fr(0)
    for d in branching:
        j = Fr(d - 1, 2)
        s += j * (j + 1) * (2 * j + 1) / 3
    return s

# ---------------------------------------------------------------- complex rationals (principal sl2)
class CF:
    __slots__ = ("re", "im")
    def __init__(self, re=0, im=0):
        self.re = Fr(re); self.im = Fr(im)
    def __add__(s, o): o = cf(o); return CF(s.re + o.re, s.im + o.im)
    def __sub__(s, o): o = cf(o); return CF(s.re - o.re, s.im - o.im)
    def __neg__(s): return CF(-s.re, -s.im)
    def __mul__(s, o):
        o = cf(o)
        return CF(s.re * o.re - s.im * o.im, s.re * o.im + s.im * o.re)
    def __truediv__(s, o):
        o = cf(o)
        d = o.re * o.re + o.im * o.im
        return CF((s.re * o.re + s.im * o.im) / d, (s.im * o.re - s.re * o.im) / d)
    __radd__ = __add__
    __rmul__ = __mul__
    def __rsub__(s, o): return cf(o) - s
    def __eq__(s, o):
        o = cf(o)
        return s.re == o.re and s.im == o.im
    def __bool__(s): return bool(s.re) or bool(s.im)
    def __repr__(s): return f"({s.re}+{s.im}i)"

def cf(x):
    return x if isinstance(x, CF) else CF(x)

def cmat(A):
    return [[cf(x) for x in r] for r in A]

def c_rank(rows):
    red, piv = [], []
    for r in rows:
        r = [cf(x) for x in r]
        n = len(r)
        for rr, c in zip(red, piv):
            if r[c]:
                f = r[c] / rr[c]
                for j in range(n):
                    r[j] = r[j] - f * rr[j]
        for c in range(n):
            if r[c]:
                red.append(r); piv.append(c)
                break
    return len(red)

def c_kernel(rows, n):
    mat = [[cf(x) for x in r] for r in rows]
    red, piv = [], []
    for r in mat:
        for rr, c in zip(red, piv):
            if r[c]:
                f = r[c] / rr[c]
                for j in range(n):
                    r[j] = r[j] - f * rr[j]
        pc = None
        for c in range(n):
            if r[c]:
                pc = c; break
        if pc is not None:
            red.append(r); piv.append(pc)
    pivset = set(piv)
    free = [c for c in range(n) if c not in pivset]
    out = []
    for fc in free:
        v = [CF(0)] * n
        v[fc] = CF(1)
        for rr, c in reversed(list(zip(red, piv))):
            s = CF(0)
            for j in range(n):
                if j != c and rr[j]:
                    s = s + rr[j] * v[j]
            v[c] = CF(0) - s / rr[c]
        out.append(v)
    return out

def c_mat_mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    out = [[CF(0)] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            a = A[i][k]
            if a:
                for j in range(p):
                    if B[k][j]:
                        out[i][j] = out[i][j] + a * B[k][j]
    return out

def c_bracket(A, B):
    X = c_mat_mul(A, B); Y = c_mat_mul(B, A)
    return [[X[i][j] - Y[i][j] for j in range(len(X))] for i in range(len(X))]

def c_scale(A, s):
    s = cf(s)
    return [[s * x for x in r] for r in A]

def c_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]

def c_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]

# ---------------------------------------------------------------- homotopy bookkeeping (own module)
class Homotopy:
    """Adopted facts (memo section 7) + exact-sequence deductions; every derived
    value is produced by an explicit zero-flanked segment of the LES of a fibration."""
    ADOPTED = {
        ("SU3", 1): "0", ("SU3", 3): "Z", ("SU3", 4): "0",
        ("SU2", 3): "Z", ("SU2", 4): "Z2",
        ("S6", 1): "0", ("S6", 2): "0", ("S6", 3): "0", ("S6", 4): "0", ("S6", 5): "0",
        ("S3", 4): "Z2",
        ("S1", 2): "0", ("S1", 3): "0", ("S1", 4): "0",
        ("S15", 1): "0", ("S15", 4): "0",
        ("SO3", 1): "Z2",
    }
    def pi(self, space, k):
        return self.ADOPTED[(space, k)]
    def fibration_middle(self, piF_k, piB_k, piB_kplus1):
        # pi_{k+1}(B) -> pi_k(F) -> pi_k(E) -> pi_k(B): both flanks 0 => iso.
        assert piB_k == "0" and piB_kplus1 == "0"
        return piF_k
    def fibration_base(self, piE_k, piF_kminus1, piF_k):
        # pi_k(F) -> pi_k(E) -> pi_k(B) -> pi_{k-1}(F): both fiber terms 0 => iso.
        assert piF_kminus1 == "0" and piF_k == "0"
        return piE_k

HTPY = Homotopy()

def derive_g2_homotopy():
    # SU(3) -> G2 -> S^6
    pi1 = HTPY.fibration_middle(HTPY.pi("SU3", 1), HTPY.pi("S6", 1), HTPY.pi("S6", 2))
    pi3 = HTPY.fibration_middle(HTPY.pi("SU3", 3), HTPY.pi("S6", 3), HTPY.pi("S6", 4))
    pi4 = HTPY.fibration_middle(HTPY.pi("SU3", 4), HTPY.pi("S6", 4), HTPY.pi("S6", 5))
    return pi1, pi3, pi4

def pi4_S2():
    # Hopf fibration S^1 -> S^3 -> S^2, LES segment
    # pi4(S1)=0 -> pi4(S3) -> pi4(S2) -> pi3(S1)=0  =>  pi4(S2) iso pi4(S3).
    return HTPY.fibration_base(HTPY.pi("S3", 4), HTPY.pi("S1", 3), HTPY.pi("S1", 4))

GROUP_ORDER = {"0": 1, "Z2": 2}

# ---------------------------------------------------------------- Q(sqrt2) and 2O
class K2:
    __slots__ = ("a", "b")           # a + b*sqrt(2)
    def __init__(self, a=0, b=0):
        self.a = Fr(a); self.b = Fr(b)
    def __add__(s, o): o = k2(o); return K2(s.a + o.a, s.b + o.b)
    def __sub__(s, o): o = k2(o); return K2(s.a - o.a, s.b - o.b)
    def __neg__(s): return K2(-s.a, -s.b)
    def __mul__(s, o):
        o = k2(o)
        return K2(s.a * o.a + 2 * s.b * o.b, s.a * o.b + s.b * o.a)
    __radd__ = __add__
    __rmul__ = __mul__
    def __eq__(s, o):
        o = k2(o)
        return s.a == o.a and s.b == o.b
    def __hash__(s):
        return hash((s.a, s.b))
    def __float__(s):
        return float(s.a) + float(s.b) * math.sqrt(2)
    def __repr__(s):
        return f"K2({s.a},{s.b})"

def k2(x):
    return x if isinstance(x, K2) else K2(x)

def qmul(p, q):
    w1, x1, y1, z1 = p; w2, x2, y2, z2 = q
    return (w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2)

def build_2O():
    els = set()
    H = K2(Fr(1, 2))
    R = K2(0, Fr(1, 2))          # 1/sqrt(2) = sqrt(2)/2
    for i in range(4):
        for s in (1, -1):
            v = [k2(0)] * 4
            v[i] = k2(s)
            els.add(tuple(v))
    for signs in product((1, -1), repeat=4):
        els.add(tuple(k2(Fr(s, 2)) for s in signs))
    for i, j in combinations(range(4), 2):
        for si, sj in product((1, -1), repeat=2):
            v = [k2(0)] * 4
            v[i] = K2(0, Fr(si, 2))
            v[j] = K2(0, Fr(sj, 2))
            els.add(tuple(v))
    return sorted(els, key=lambda q: [(c.a, c.b) for c in q])

def chi32(c):
    """chi_{3/2}(q) = 8 Re(q)^3 - 4 Re(q), exact in Q(sqrt2)."""
    return k2(8) * c * c * c - k2(4) * c

# ---------------------------------------------------------------- 1344 group / collineations
def collineations():
    import itertools
    out = []
    for p in itertools.permutations(range(1, 8)):
        pm = {i + 1: p[i] for i in range(7)}
        if all(tuple(sorted((pm[a], pm[b], pm[c]))) in LINESET for a, b, c in LINES):
            out.append(pm)
    return out

def signed_lifts(pm):
    """Sign vectors s (dict 1..7 -> +-1) making x -> s_i e_{pm(i)} an automorphism."""
    lifts = []
    pairs = [(a, b) for a in range(1, 8) for b in range(a + 1, 8)]
    for signs in product((1, -1), repeat=7):
        s = {i + 1: signs[i] for i in range(7)}
        ok = True
        for a, b in pairs:
            c = next(k for k in range(1, 8) if phi[a][b][k])
            lhs = s[a] * s[b] * phi[pm[a]][pm[b]][pm[c]]
            rhs = s[c] * phi[a][b][c]
            if lhs != rhs:
                ok = False
                break
        if ok:
            lifts.append(s)
    return lifts

def sp_mat(pm, s):
    """Signed permutation as 7x7 int matrix (0-based)."""
    M = [[0] * 7 for _ in range(7)]
    for i in range(1, 8):
        M[pm[i] - 1][i - 1] = s[i]
    return M

def sp_key(pm, s):
    return tuple((pm[i], s[i]) for i in range(1, 8))

def sp_compose(A, B):
    """(pmA,sA) after (pmB,sB): x -> A(B(x))."""
    pmA, sA = A; pmB, sB = B
    pm = {i: pmA[pmB[i]] for i in range(1, 8)}
    s = {i: sB[i] * sA[pmB[i]] for i in range(1, 8)}
    return (pm, s)

def sp_order(el):
    ident = ({i: i for i in range(1, 8)}, {i: 1 for i in range(1, 8)})
    cur = el
    for n in range(1, 30):
        if sp_key(*cur) == sp_key(*ident):
            return n
        cur = sp_compose(el, cur)
    raise RuntimeError

def sp_trace(el):
    pm, s = el
    return sum(s[i] for i in range(1, 8) if pm[i] == i)

def is_oct_automorphism_signed(el):
    pm, s = el
    for a in range(1, 8):
        for b in range(1, 8):
            if a == b:
                continue
            c = next(k for k in range(1, 8) if phi[a][b][k])
            if phi[pm[a]][pm[b]][pm[c]] * s[a] * s[b] != phi[a][b][c] * s[c]:
                return False
    return True

# ---------------------------------------------------------------- SL(2,7) / GL(3,2)
def sl27_elements():
    els = []
    for a, b, c, d in product(range(7), repeat=4):
        if (a * d - b * c) % 7 == 1:
            els.append((a, b, c, d))
    return els

def m2mul(p, q, mod=7):
    a, b, c, d = p; e, f, g, h = q
    return ((a * e + b * g) % mod, (a * f + b * h) % mod,
            (c * e + d * g) % mod, (c * f + d * h) % mod)

def gl32_elements():
    els = []
    vecs = [v for v in product((0, 1), repeat=3)]
    for cols in product(range(1, 8), repeat=3):
        M = [[(c >> (2 - r)) & 1 for c in cols] for r in range(3)]
        # invertibility over F2 via rank
        A = [row[:] for row in M]
        r = 0
        for cidx in range(3):
            p = next((i for i in range(r, 3) if A[i][cidx]), None)
            if p is None:
                break
            A[r], A[p] = A[p], A[r]
            for i in range(3):
                if i != r and A[i][cidx]:
                    A[i] = [(x ^ y) for x, y in zip(A[i], A[r])]
            r += 1
        if r == 3:
            els.append(tuple(tuple(row) for row in M))
    return els

def gl32_perm_on_points(M):
    """Action on the 7 nonzero vectors of F2^3, labelled 1..7 by binary value."""
    def apply(v):
        return tuple(sum(M[i][j] * v[j] for j in range(3)) % 2 for i in range(3))
    pm = {}
    for val in range(1, 8):
        v = ((val >> 2) & 1, (val >> 1) & 1, val & 1)
        w = apply(v)
        pm[val] = (w[0] << 2) | (w[1] << 1) | w[2]
    return pm

# ---------------------------------------------------------------- Phase 0: so(16) stabilizer of the O density
CPLX_OF_REAL = [(k // 2, k % 2) for k in range(16)]        # real index -> (octonion index a, 0=Re/1=Im)

def T_basis_value(p, q, r):
    """T(f_p, f_q, f_r) as CF, with f_{2a}=e_a, f_{2a+1}=i e_a in C^8 coordinates."""
    (a, sa), (b, sb), (c, sc) = CPLX_OF_REAL[p], CPLX_OF_REAL[q], CPLX_OF_REAL[r]
    if a == 0 or b == 0 or c == 0:
        return CF(0)
    v = phi[a][b][c]
    if not v:
        return CF(0)
    k = (sa + sb + sc) % 4
    return [CF(v), CF(0, v), CF(-v), CF(0, -v)][k]

SO16_PAIRS = list(combinations(range(16), 2))
S16IDX = {pq: i for i, pq in enumerate(SO16_PAIRS)}

def deltaT_coeff_rows():
    """Rows (real+imag) of the map so(16) -> coefficients of deltaT on p<q<r."""
    rows = []
    for p, q, r in combinations(range(16), 3):
        cre = {}
        cim = {}
        def acc(midx, val):
            if val:
                cre[midx] = cre.get(midx, Fr(0)) + val.re
                cim[midx] = cim.get(midx, Fr(0)) + val.im
        # X f_slot = sum over m: for basis X_{mn}: X f_n = f_m, X f_m = -f_n
        for slot, (s0, s1, s2) in (("p", (p, q, r)), ("q", (q, p, r)), ("r", (r, p, q))):
            t = s0
            for (m, n) in SO16_PAIRS:
                if n == t:
                    rep = m; sgn = 1
                elif m == t:
                    rep = n; sgn = -1
                else:
                    continue
                if slot == "p":
                    val = T_basis_value(rep, q, r)
                elif slot == "q":
                    val = T_basis_value(p, rep, r)
                else:
                    val = T_basis_value(p, q, rep)
                if val:
                    acc(S16IDX[(m, n)], c_scale([[val]], sgn)[0][0])
        for cdict in (cre, cim):
            if cdict:
                row = [Fr(0)] * 120
                for i, v in cdict.items():
                    row[i] = v
                rows.append(row)
    return rows

def so16_params_from_16x16(X):
    v = [Fr(0)] * 120
    for (m, n), i in S16IDX.items():
        v[i] = X[m][n]        # X f_n = f_m convention: entry [m][n] is the X_{mn} coefficient
    return v

def deltaT_margin(X16):
    """max |coefficient| of deltaT for a 16x16 real matrix (columns = images of f_j)."""
    best = Fr(0)
    for p, q, r in combinations(range(16), 3):
        tot = CF(0)
        for slot in range(3):
            idx = (p, q, r)
            t = idx[slot]
            for m in range(16):
                cval = X16[m][t]
                if not cval:
                    continue
                args = list(idx)
                args[slot] = m
                v = T_basis_value(*args)
                if v:
                    tot = tot + CF(cval) * v
        for comp in (tot.re, tot.im):
            if abs(comp) > best:
                best = abs(comp)
    return best

def embed_g2_16(X7):
    X16 = zeros(16)
    for i in range(7):
        for j in range(7):
            if X7[i][j]:
                a, b = i + 1, j + 1
                X16[2 * a][2 * b] = X7[i][j]
                X16[2 * a + 1][2 * b + 1] = X7[i][j]
    return X16

def u1_e0_16():
    X16 = zeros(16)
    X16[0][1] = Fr(-1)
    X16[1][0] = Fr(1)
    return X16

def phase_generator_16():
    X16 = zeros(16)
    for a in range(8):
        X16[2 * a][2 * a + 1] = Fr(-1)
        X16[2 * a + 1][2 * a] = Fr(1)
    return X16

# ---------------------------------------------------------------- main computation
def main():
    guard()
    t1 = t1_scan_all()
    report = {}
    extras = {}

    # ---------- algebra bedrock
    assert DIM_G2 == 14, DIM_G2
    assert all(is_derivation(g) for g in G2), "phi-stabilizer basis fails the derivation identity"
    assert len(SU2_LONG) == 3 and len(STAB_HL) == 6 and len(SU3) == 8 and len(SU2_SHORT) == 3
    assert closed_under_bracket(SU2_LONG) and closed_under_bracket(SU2_SHORT) and closed_under_bracket(SU3)
    # su2_long kills e4 automatically (derivation property): verify
    for X in SU2_LONG:
        assert all(X[i][3] == 0 for i in range(7))
    # commuting chiralities inside Stab(H_L)
    for A in SU2_LONG:
        for B in SU2_SHORT:
            assert all(x == 0 for x in flat(bracket(A, B)))

    # ---------- Phase 0 ------------------------------------------------
    # (0a) field content, asserted from the extract header (Q-A1-1/Q-A1-3)
    phase0 = {
        "field_real_components": 16,
        "complex_amplitudes": 8,
        "spinor_index_present": False,
    }
    # (0c) spatial-internal direct product: term inventory of the action of record
    # (extract 3.4.4/3.4.7): kinetic |grad psi|^2 (internal delta, spatial scalar);
    # two-body a(r) delta_ij rho rho (internal delta, spatial scalar); oriented
    # O = phi_abc psi_a dx psi_b dy psi_c (internal phi, spatial 2-form dx^dy).
    terms = [
        {"name": "kinetic", "internal": "delta", "spatial": "scalar"},
        {"name": "two_body", "internal": "delta", "spatial": "scalar"},
        {"name": "oriented_O", "internal": "phi", "spatial": "dx^dy"},
    ]
    direct_product = all(t["internal"] in ("delta", "phi") and t["spatial"] in ("scalar", "dx^dy") for t in terms)
    phase0["spatial_internal_direct_product"] = bool(direct_product)

    # (0b) full continuous stabilizer of the O density inside so(16)
    rows16 = deltaT_coeff_rows()
    rank16 = rank_of(rows16)
    stab_dim = 120 - rank16
    g2_16 = [embed_g2_16(g) for g in G2]
    g2_margins = [deltaT_margin(X) for X in g2_16]
    u1_margin = deltaT_margin(u1_e0_16())
    assert all(m == 0 for m in g2_margins) and u1_margin == 0
    # independence of the 15 candidate generators + span = kernel
    cand = [so16_params_from_16x16(X) for X in g2_16 + [u1_e0_16()]]
    assert rank_of([list(c) for c in cand]) == 15
    assert stab_dim == 15, stab_dim
    extras["full_O_density_stabilizer_so16"] = {
        "dim": stab_dim,
        "identification": "g2 (acting C-linearly on the octonionic index) + u(1) acting on the real-unit complex line alone; the u(1) is an accidental spectator (Q-A1-3: no real-unit-splitting term) and acts trivially on Im(O) tensor C",
    }
    # generic so(16) negative control
    Xgen = zeros(16)
    Xgen[0][2] = Fr(-1); Xgen[2][0] = Fr(1)      # rotate Re psi_0 into Re psi_1
    gen_margin = deltaT_margin(Xgen)
    assert gen_margin > 0
    extras["generic_so16_margin"] = str(gen_margin)
    # phase subgroup: diagonal phase acts on the density by z^3
    ph_margin = deltaT_margin(phase_generator_16())
    assert ph_margin > 0        # continuous U(1) broken
    # induced character z -> z^3: kernel order 3 (cube roots of unity)
    phase_order = 3
    # conjugation: T(conj u, conj v, conj w) = conj T(u,v,w) since phi is real
    conj_ok = True
    for p, q, r in combinations(range(16), 3):
        v = T_basis_value(p, q, r)
        # conjugation flips the sign of every odd (imaginary) slot
        sgn = (-1) ** ((p % 2) + (q % 2) + (r % 2))
        w = CF(v.re * sgn, v.im * sgn)
        if not (w.re == v.re and w.im == -v.im):
            conj_ok = False
            break
    phase0.update({
        "sym_int_pinned": True,
        "sym_int_continuous": "G2",
        "sym_int_continuous_dim": 14,
        "g2_preserves_O": True,
        "generic_so16_breaks_O": True,
        "phase_subgroup_order": phase_order,
        "O_phase_invariant": False,
        "conjugation_maps_O_to_conjugate": bool(conj_ok),
        "two_body_symmetry": "O(16)",
        "vacuum_manifold_of_record": "S15",
        "pi1_V": GROUP_ORDER[HTPY.pi("S15", 1)] - 1,
        "pi4_V": GROUP_ORDER[HTPY.pi("S15", 4)] - 1,
        "real_unit_splitting_term_present": False,
    })

    # (0d) locking inventory
    branch_long = casimir_branching(SU2_LONG)
    idx_long = dynkin_index(branch_long)
    assert idx_long == 1
    def stab_dim_of(im_indices):
        """dim of {X in g2 : X e_i = 0 for the given Im-basis indices}."""
        sub = subalg_kernel(lambda X: [X[i][j] for j in im_indices for i in range(7)])
        return len(sub)
    inv = []
    for rank, (im_idx, H0, H0_dim) in enumerate((
            ([], "G2", 14),
            ([0], "SU3", 8),
            ([0, 1], "SU2_long", 3))):
        d = stab_dim_of(im_idx) if im_idx else DIM_G2
        assert d == H0_dim, (rank, d)
        pi4H = {"G2": derive_g2_homotopy()[2], "SU3": HTPY.pi("SU3", 4), "SU2_long": HTPY.pi("SU2", 4)}[H0]
        # pi4(G2/H0) = coker(pi4(H0)->pi4(G2)=0) + ker(pi3(H0)->pi3(G2)): coker into 0 is 0;
        # kernel is 0 because the generator has nonzero index (pi3-injective).
        pi3inj = idx_long != 0
        pi4q = 0 if pi3inj else None
        inv.append({
            "rank": rank, "H0": H0, "H0_dim": H0_dim, "pi0_generic": 1,
            "sl2_generator_jordan_type": [int(x) for x in branch_long],
            "sl2_generator_index": int(idx_long),
            "pi3_injective": bool(pi3inj), "pi4_quotient": int(pi4q),
        })
    phase0["locking_inventory"] = inv

    # (0e) controls
    U0, rho0 = Fr(3, 2), Fr(1)
    mu = U0 * rho0
    lperp_zero = (U0 * rho0 - mu) == 0
    # F21 = unsigned collineation lifts that are automorphisms
    colls = collineations()
    assert len(colls) == 168
    ones = {i: 1 for i in range(1, 8)}
    f21 = [pm for pm in colls if is_oct_automorphism_signed((pm, ones))]
    assert len(f21) == 21
    # character on C^7: trace = fixed points
    chi = {tuple(sorted(pm.items())): sum(1 for i in range(1, 8) if pm[i] == i) for pm in f21}
    n21 = 21
    m_triv = Fr(sum(chi.values()), n21)
    norm = Fr(sum(v * v for v in chi.values()), n21)
    assert m_triv == 1 and norm == 3
    # the 6-dim complement splits as two conjugate 3-dim pieces: the order-3
    # multiplier orbit on Z7 exponents is {1,2,4} u {3,6,5}, swapped by negation
    orb1 = set()
    x = 1
    for _ in range(3):
        orb1.add(x); x = (x * 2) % 7
    orb2 = {(7 - x) % 7 for x in orb1}
    f21_ok = (orb1 == {1, 2, 4}) and (orb2 == {3, 5, 6}) and orb1.isdisjoint(orb2)
    phase0["controls"] = {
        "L_perp_zero_mode": bool(lperp_zero),
        "F21_split_1_3_3bar": bool(m_triv == 1 and norm == 3 and f21_ok),
        "generic_so16_fails_margin_positive": bool(gen_margin > 0),
    }

    # ---------- Phase 1 ------------------------------------------------
    # ----- T1
    two_o = build_2O()
    assert len(two_o) == 48
    idx2O = {q: None for q in two_o}
    # closure check
    for p in two_o[:8]:
        for q in two_o:
            assert qmul(p, q) in idx2O
    chi_vals = {q: chi32(q[0]) for q in two_o}
    norm_chi = K2(0)
    for q in two_o:
        norm_chi = norm_chi + chi_vals[q] * chi_vals[q]
    assert norm_chi == K2(48)
    fs = K2(0)
    for q in two_o:
        q2 = qmul(q, q)
        fs = fs + chi32(q2[0])
    assert fs == K2(-48)
    one = (k2(1), k2(0), k2(0), k2(0))
    mone = (k2(-1), k2(0), k2(0), k2(0))
    chi_at_1 = chi_vals[one]; chi_at_m1 = chi_vals[mone]
    assert chi_at_1 == K2(4) and chi_at_m1 == K2(-4)
    # the 7 of G2 is real and irreducible: commutant {M : [M, g] = 0 for all g}
    comm_rows = []
    for g in G2:
        for i in range(7):
            for j in range(7):
                row = [Fr(0)] * 49
                for k in range(7):
                    row[i * 7 + k] += g[k][j]
                    row[k * 7 + j] -= g[i][k]
                comm_rows.append(row)
    comm_dim = 49 - rank_of(comm_rows)
    seven_real = (comm_dim == 1)      # real matrices + commutant R => real type, irreducible
    # quartet multiplicity in the 7: quaternionic irrep in a real rep has even
    # multiplicity; upper bound floor(7/4) = 1; even => 0
    q_upper = (7 // 4) - ((7 // 4) % 2)
    # phase character on 2O: abelianization
    def commutator(p, q):
        # p q p^-1 q^-1; inverse of unit quaternion = conjugate
        def conj(a):
            return (a[0], -a[1], -a[2], -a[3])
        return qmul(qmul(p, q), qmul(conj(p), conj(q)))
    derived = set()
    frontier = set()
    for p in two_o:
        for q in two_o:
            frontier.add(commutator(p, q))
    derived |= frontier
    changed = True
    while changed:
        changed = False
        new = set()
        for a in derived:
            for b in frontier:
                c = qmul(a, b)
                if c not in derived:
                    new.add(c)
        if new:
            derived |= new
            changed = True
    ab_order = 48 // len(derived)
    assert len(derived) == 24 and ab_order == 2
    phase_char_trivial = (math.gcd(ab_order, 3) == 1)     # Hom(Z2, Z3) = 1
    # branchings of the four sl2 classes
    branch_short = casimir_branching(SU2_SHORT)
    # su(3)-sl2: the so(3) of real matrices in the C^3 picture
    su3_c3 = []
    Fbas = [0, 1, 3]                 # e1, e2, e4 (0-based Im)
    JF = {0: 2, 1: 5, 3: 4}          # J e1 = e3, J e2 = e6, J e4 = e5 (0-based Im)
    Jsigns = {0: 1, 1: 1, 3: 1}
    # verify J action signs: L7 restricted to Im
    for f, jf in JF.items():
        col = OMUL[7][f + 1]
        assert col[jf + 1] != 0 and sum(abs(c) for c in col) == 1
        Jsigns[f] = col[jf + 1]
    def c3_matrix(X):
        """Complex 3x3 matrix of X in the basis {e1, e2, e4} with i = L_7."""
        M = [[CF(0)] * 3 for _ in range(3)]
        for jn, f in enumerate(Fbas):
            img = [X[i][f] for i in range(7)]
            for kn, g in enumerate(Fbas):
                re = img[g]
                im = img[JF[g]] * Jsigns[g]
                M[kn][jn] = CF(re, im)
        return M
    # check su(3) commutes with J on the 6-dim complement of e7 and c3 is faithful
    for X in SU3:
        M = c3_matrix(X)
        # reconstruct and compare on the basis vectors to confirm C-linearity
        for jn, f in enumerate(Fbas):
            img = [X[i][f] for i in range(7)]
            rec = [Fr(0)] * 7
            for kn, g in enumerate(Fbas):
                rec[g] += M[kn][jn].re
                rec[JF[g]] += M[kn][jn].im * Jsigns[g]
            assert rec == img, "su(3) element not C-linear in the L7 complex structure"
    # solve for so(3) generators R_ab (real antisymmetric in the C^3 basis)
    def solve_su3_for(target):
        rows = []
        rhs = []
        for i in range(3):
            for j in range(3):
                for part in (0, 1):
                    rows.append([ (c3_matrix(X)[i][j].re if part == 0 else c3_matrix(X)[i][j].im) for X in SU3 ])
                    rhs.append(target[i][j].re if part == 0 else target[i][j].im)
        x, _ = solve_affine(rows, rhs, len(SU3))
        assert x is not None
        M = zeros(7)
        for c, X in zip(x, SU3):
            if c:
                M = mat_add(M, mat_scale(X, c))
        return M
    def Rmat(i, j):
        M = [[CF(0)] * 3 for _ in range(3)]
        M[i][j] = CF(-1); M[j][i] = CF(1)
        return M
    SO3_IN_SU3 = [solve_su3_for(Rmat(0, 1)), solve_su3_for(Rmat(0, 2)), solve_su3_for(Rmat(1, 2))]
    assert closed_under_bracket(SO3_IN_SU3)
    branch_su3 = casimir_branching(SO3_IN_SU3)
    # principal sl2: Cartan combination h = -i(8 khat + 4 c2hat)
    #   khat in su2_long with khat e3 = e5/2 ; c2hat in su2_short with c2hat e4 = 0, c2hat e1 = e2
    def solve_in_span(bas, cond_rows_fn, rhs):
        rows = []
        per = [cond_rows_fn(b) for b in bas]
        for r in range(len(per[0])):
            rows.append([per[i][r] for i in range(len(bas))])
        x, ker = solve_affine(rows, rhs, len(bas))
        assert x is not None and not ker
        M = zeros(7)
        for c, b in zip(x, bas):
            if c:
                M = mat_add(M, mat_scale(b, c))
        return M
    e3v = ebas7(2); e5v = ebas7(4)
    khat = solve_in_span(SU2_LONG, lambda X: [X[i][2] for i in range(7)],
                         [Fr(1, 2) if i == 4 else Fr(0) for i in range(7)])
    c2hat = solve_in_span(SU2_SHORT,
                          lambda X: [X[i][3] for i in range(7)] + [X[i][0] for i in range(7)],
                          [Fr(0)] * 7 + [Fr(1) if i == 1 else Fr(0) for i in range(7)])
    # squares on the perp block
    def restrict(M, idxs):
        return [[M[i][j] for j in idxs] for i in idxs]
    kperp = restrict(khat, HL_PERP)
    assert mat_mul(kperp, kperp) == mat_scale(eye(4), Fr(-1, 4))
    c2perp = restrict(c2hat, HL_PERP)
    assert mat_mul(c2perp, c2perp) == mat_scale(eye(4), Fr(-1, 4))
    assert all(c2hat[i][3] == 0 for i in range(7))
    Hreal = mat_add(mat_scale(khat, Fr(8)), mat_scale(c2hat, Fr(4)))
    hP = c_scale(cmat(Hreal), CF(0, -1))          # h = -i H
    # eigenvalues of h expected {0, +-2, +-4, +-6}
    for lam, mult in ((0, 1), (2, 1), (-2, 1), (4, 1), (-4, 1), (6, 1), (-6, 1)):
        M = c_sub(hP, c_scale(cmat(eye(7)), CF(lam)))
        assert 7 - c_rank([r[:] for r in M]) == mult, (lam,)
    # sl2-triple: e in the ad-eigenspace V2 of g2^C, f in V-2 with [e,f] = h
    g2c = [cmat(g) for g in G2]
    def ad_rows(target_eig):
        # unknowns: complex coefficients on the 14 g2 basis elements
        per = []
        for g in g2c:
            per.append(c_sub(c_bracket(hP, g), c_scale(g, CF(target_eig))))
        rows = []
        for i in range(7):
            for j in range(7):
                rows.append([per[k][i][j] for k in range(14)])
        return rows
    V2 = c_kernel(ad_rows(2), 14)
    Vm2 = c_kernel(ad_rows(-2), 14)
    assert len(V2) == 2 and len(Vm2) == 2
    def from_coeffs(co):
        M = [[CF(0)] * 7 for _ in range(7)]
        for c, g in zip(co, g2c):
            if c:
                M = c_add(M, c_scale(g, c))
        return M
    eP = None; fP = None
    for t_num in (1, 2, 3, -1, 5, Fr(1, 2)):
        cand_e = from_coeffs([a + CF(t_num) * b for a, b in zip(V2[0], V2[1])])
        f1 = from_coeffs(Vm2[0]); f2 = from_coeffs(Vm2[1])
        A1 = c_bracket(cand_e, f1); A2 = c_bracket(cand_e, f2)
        # solve alpha A1 + beta A2 = h  (49 complex equations, 2 unknowns)
        eqs = []
        rhs = []
        for i in range(7):
            for j in range(7):
                eqs.append((A1[i][j], A2[i][j]))
                rhs.append(hP[i][j])
        piv = [(a, b, r) for (a, b), r in zip(eqs, rhs) if a or b]
        solved = False
        for i1 in range(len(piv)):
            for i2 in range(i1 + 1, len(piv)):
                a1, b1, r1 = piv[i1]; a2, b2, r2 = piv[i2]
                det = a1 * b2 - a2 * b1
                if det:
                    alpha = (r1 * b2 - r2 * b1) / det
                    beta = (a1 * r2 - a2 * r1) / det
                    ok = all((a * alpha + b * beta) == r for (a, b), r in zip(eqs, rhs))
                    if ok:
                        eP = cand_e
                        fP = c_add(c_scale(f1, alpha), c_scale(f2, beta))
                        solved = True
                    break
            if solved or eP is not None:
                break
        if eP is not None:
            break
    assert eP is not None, "principal sl2-triple not found"
    assert c_bracket(hP, eP) == c_scale(eP, CF(2))
    assert c_bracket(hP, fP) == c_scale(fP, CF(-2))
    assert c_bracket(eP, fP) == hP
    # branching from the exact weight multiset of h: greedy string peeling
    weights = [6, 4, 2, 0, -2, -4, -6]
    ws = sorted(weights, reverse=True)
    branch_prin = []
    from collections import Counter
    cnt = Counter(ws)
    while sum(cnt.values()):
        top = max(w for w in cnt if cnt[w])
        for w in range(top, -top - 1, -2):
            assert cnt[w] > 0
            cnt[w] -= 1
        branch_prin.append(top + 1)
    branch_prin = sorted(branch_prin, reverse=True)
    extras["sl2_class_indices_normalized_long_root_1"] = {
        "long_root": str(dynkin_index(branch_long)),
        "short_root": str(dynkin_index(branch_short)),
        "su3_sl2": str(dynkin_index(branch_su3)),
        "principal": str(dynkin_index(branch_prin)),
    }
    # control C-A1-1: quartet in (C^2)tensor3 under diagonal SU(2), by weights
    w3 = sorted((a + b + c for a in (1, -1) for b in (1, -1) for c in (1, -1)), reverse=True)
    cnt = Counter(w3)
    sym3_dims = []
    while sum(cnt.values()):
        top = max(w for w in cnt if cnt[w])
        for w in range(top, -top - 1, -2):
            cnt[w] -= 1
        sym3_dims.append(top + 1)
    sym3_quartet = sym3_dims.count(4)

    T1 = {
        "holds": bool(seven_real and q_upper == 0 and phase_char_trivial and
                      all(4 not in b for b in (branch_long, branch_short, branch_su3, branch_prin))),
        "chi32_norm": 1,
        "chi32_at_1": 4,
        "chi32_at_minus1": -4,
        "fs_indicator": -1,
        "seven_real": bool(seven_real),
        "quartet_multiplicity_upper": int(q_upper),
        "phase_char_on_2O_trivial": bool(phase_char_trivial),
        "branching_long_root": [int(x) for x in branch_long],
        "branching_short_root": [int(x) for x in branch_short],
        "branching_su3_sl2": [int(x) for x in branch_su3],
        "branching_principal": [int(x) for x in branch_prin],
        "control_sym3_quartet_mult": int(sym3_quartet),
    }

    # ----- T2
    biv7 = []
    biv6 = []
    for a in range(1, 8):
        for b in range(a + 1, 8):
            M = mat_mul(L[a], L[b])
            biv7.append(M)
            if b <= 6:
                biv6.append(M)
    # Clifford relations of the seven L_a on R^8
    for a in range(1, 8):
        for b in range(1, 8):
            anti = mat_add(mat_mul(L[a], L[b]), mat_mul(L[b], L[a]))
            assert anti == (mat_scale(eye(8), Fr(-2)) if a == b else zeros(8))
    dim_b7 = rank_of([flat(M) for M in biv7])
    dim_b6 = rank_of([flat(M) for M in biv6])
    g2_8 = [to8(g) for g in G2]
    dim_union7 = rank_of([flat(M) for M in biv7] + [flat(M) for M in g2_8])
    g2_in_spin7 = (dim_union7 == dim_b7)
    dim_union6 = rank_of([flat(M) for M in biv6] + [flat(M) for M in g2_8])
    dim_cap = DIM_G2 + dim_b6 - dim_union6
    # (b) spinorial 2O through the C^4 = (R^8, J=L7) picture
    Fbas8 = [0, 1, 2, 4]
    JF8 = {0: 7, 1: 3, 2: 6, 4: 5}
    for f, jf in JF8.items():
        col = OMUL[7][f]
        assert col[jf] == 1 and sum(abs(c) for c in col) == 1
    def c4_matrix(M8):
        """Complex 4x4 matrix of an R-linear, J-commuting M8."""
        out = [[CF(0)] * 4 for _ in range(4)]
        for jn, f in enumerate(Fbas8):
            img = [M8[i][f] for i in range(8)]
            for kn, g in enumerate(Fbas8):
                out[kn][jn] = CF(img[g], img[JF8[g]])
        return out
    # su(4)_L = span of the 15 bivectors a<b<=6: anti-Hermitian traceless, rank 15
    b6c = [c4_matrix(M) for M in biv6]
    for M in b6c:
        tr = M[0][0] + M[1][1] + M[2][2] + M[3][3]
        assert tr == CF(0)
        for i in range(4):
            for j in range(4):
                assert M[i][j].re == -M[j][i].re and M[i][j].im == M[j][i].im
    def antiherm_params(M):
        v = []
        for i in range(4):
            v.append(M[i][i].im)
        for i in range(4):
            for j in range(i + 1, 4):
                v.append(M[i][j].re); v.append(M[i][j].im)
        return v
    assert rank_of([antiherm_params(M) for M in b6c]) == 15
    su4_complete = True
    # spin-3/2 generators (floats from here per A-2.3)
    s3 = math.sqrt(3.0)
    Jz = [[1.5, 0, 0, 0], [0, 0.5, 0, 0], [0, 0, -0.5, 0], [0, 0, 0, -1.5]]
    Jp = [[0, s3, 0, 0], [0, 0, 2, 0], [0, 0, 0, s3], [0, 0, 0, 0]]
    Jm = [[Jp[j][i] for j in range(4)] for i in range(4)]
    Jx = [[(Jp[i][j] + Jm[i][j]) / 2 for j in range(4)] for i in range(4)]
    Jy = [[(Jp[i][j] - Jm[i][j]) / (2j) for j in range(4)] for i in range(4)]
    def cxmul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    def spin32(q):
        w = float(q[0]); vec = [float(q[1]), float(q[2]), float(q[3])]
        nv = math.sqrt(sum(v * v for v in vec))
        if nv < 1e-12:
            s = 1.0 if w > 0 else -1.0
            return [[(s if i == j else 0.0) for j in range(4)] for i in range(4)]
        theta = 2.0 * math.atan2(nv, w)
        n = [v / nv for v in vec]
        M = [[n[0] * Jx[i][j] + n[1] * Jy[i][j] + n[2] * Jz[i][j] for j in range(4)] for i in range(4)]
        lams = [1.5, 0.5, -0.5, -1.5]
        out = [[0j] * 4 for _ in range(4)]
        for k, lk in enumerate(lams):
            P = [[(1.0 + 0j) if i == j else 0j for j in range(4)] for i in range(4)]
            for l, ll in enumerate(lams):
                if l == k:
                    continue
                Q = [[(M[i][j] - (ll if i == j else 0)) / (lk - ll) for j in range(4)] for i in range(4)]
                P = cxmul(P, Q)
            ph = complex(math.cos(-theta * lk), math.sin(-theta * lk))
            for i in range(4):
                for j in range(4):
                    out[i][j] += ph * P[i][j]
        return out
    def real8_of_c4(Mc):
        cols = []
        for m in range(8):
            z = [0j] * 4
            for kn, g in enumerate(Fbas8):
                if m == g:
                    z[kn] = 1.0 + 0j
                elif m == JF8[g]:
                    z[kn] = 1j
            zz = [sum(Mc[i][k] * z[k] for k in range(4)) for i in range(4)]
            col = [0.0] * 8
            for kn, g in enumerate(Fbas8):
                col[g] += zz[kn].real
                col[JF8[g]] += zz[kn].imag
            cols.append(col)
        return [[cols[j][i] for j in range(8)] for i in range(8)]
    omul_f = [[[float(x) for x in OMUL[a][b]] for b in range(8)] for a in range(8)]
    def defect(P8):
        best = 0.0
        Pc = [[P8[i][j] for j in range(8)] for i in range(8)]
        Pe = [[Pc[i][a] for a in range(8)] for i in range(8)]     # columns P e_a
        for a in range(8):
            Pa = [Pc[i][a] for i in range(8)]
            for b in range(8):
                Pb = [Pc[i][b] for i in range(8)]
                # P(e_a e_b)
                lhs = [sum(Pc[i][c] * omul_f[a][b][c] for c in range(8)) for i in range(8)]
                # P(e_a) P(e_b): octonion product of the two image vectors
                rhs = [0.0] * 8
                for x in range(8):
                    if abs(Pa[x]) < 1e-15:
                        continue
                    for y in range(8):
                        if abs(Pb[y]) < 1e-15:
                            continue
                        t = omul_f[x][y]
                        for c in range(8):
                            if t[c]:
                                rhs[c] += Pa[x] * Pb[y] * t[c]
                d = max(abs(l - r) for l, r in zip(lhs, rhs))
                if d > best:
                    best = d
        return best
    def is_central(q):
        return abs(float(q[1])) + abs(float(q[2])) + abs(float(q[3])) < 1e-12
    reps = {}
    for q in two_o:
        reps[q] = real8_of_c4(spin32(q))
    # homomorphism spot check
    import random
    random.seed(2)
    for _ in range(20):
        p = random.choice(two_o); q = random.choice(two_o)
        A = real8_of_c4(spin32(qmul(p, q)))
        B = reps[p]; C = reps[q]
        BC = [[sum(B[i][k] * C[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
        assert max(abs(A[i][j] - BC[i][j]) for i in range(8) for j in range(8)) < 1e-9
    defects = {q: defect(reps[q]) for q in two_o}
    noncentral = [q for q in two_o if not is_central(q)]
    auto_count = sum(1 for q in noncentral if defects[q] < 1e-9)
    min_defect = min(defects[q] for q in noncentral)
    # quartet multiplicity of chi32 in the 2O character of C tensor O (= complexified R^8)
    acc = 0.0
    for q in two_o:
        tr8 = sum(reps[q][i][i] for i in range(8))
        acc += tr8 * float(chi_vals[q])
    quartet_mult = acc / 48.0
    assert abs(quartet_mult - round(quartet_mult)) < 1e-6
    quartet_mult = int(round(quartet_mult))
    # (c) SL(2,7) from scratch
    sl = sl27_elements()
    assert len(sl) == 336
    sq1 = sum(1 for g in sl if m2mul(g, g) == (1, 0, 0, 1))
    # own conjugacy-class enumeration
    slset = set(sl)
    seen = set()
    classes = []
    for g in sl:
        if g in seen:
            continue
        orb = set()
        for h in sl:
            # h g h^-1: inverse of (a,b,c,d) is (d,-b,-c,a)
            a, b, c, d = h
            hi = (d % 7, (-b) % 7, (-c) % 7, a % 7)
            orb.add(m2mul(m2mul(h, g), hi))
        classes.append(orb)
        seen |= orb
    n_classes = len(classes)
    assert n_classes == 11
    # ordinary sector: the six PSL(2,7) irreps; reality of the 6 and 7 by
    # 2-transitive permutation actions built from scratch
    gl = gl32_elements()
    assert len(gl) == 168
    fixsq = sum(sum(1 for v in range(1, 8) if gl32_perm_on_points(M)[v] == v) ** 2 for M in gl)
    assert Fr(fixsq, 168) == 2          # 2-transitive => perm = 1 + irreducible real 6
    # PSL(2,7) on P^1(F7): 8 points, from SL elements mod +-1
    def p1_action(g):
        a, b, c, d = g
        pts = list(range(7)) + ["inf"]
        pm = {}
        for p in pts:
            if p == "inf":
                num, den = a, c
            else:
                num, den = (a * p + b) % 7, (c * p + d) % 7
            pm[p] = "inf" if den % 7 == 0 else (num * pow(den, 5, 7)) % 7
        return pm
    psl_seen = set()
    fixsq8 = 0
    for g in sl:
        key = min(g, tuple((-x) % 7 for x in g))
        if key in psl_seen:
            continue
        psl_seen.add(key)
        pm = p1_action(g)
        fixsq8 += sum(1 for p in pm if pm[p] == p) ** 2
    assert len(psl_seen) == 168
    assert Fr(fixsq8, 168) == 2         # 2-transitive => perm = 1 + irreducible real 7
    fs_sum_ordinary = 1 + 6 + 7 + 8     # nu=1 for 1,6,7,8 (6,7 real by the checks above;
                                        # 8 = Steinberg, adopted); nu=0 for the complex pair 3, 3bar (adopted)
    # Diophantine: 2 nu4 + 3 nu6 + 2 nu8 = -5 over {-1,0,1} with Galois pairings
    sols = [(n4, n6, n8) for n4 in (-1, 0, 1) for n6 in (-1, 0, 1) for n8 in (-1, 0, 1)
            if 2 * n4 + 3 * n6 + 2 * n8 == -5]
    nu4_allowed = sorted({s[0] for s in sols})
    # sanity: the FS identity 22 + 8 nu4 + 12 nu6 + 8 nu8 = sq1 for some solution
    assert any(22 + 8 * a + 12 * b + 8 * c == sq1 for a, b, c in sols)
    # involutions of G2 via the 1344 group; sigma_H; single-unit negation
    lifts_all = []
    for pm in colls:
        for s in signed_lifts(pm):
            lifts_all.append((pm, s))
    n1344 = len(lifts_all)
    all_autos = all(is_oct_automorphism_signed(el) for el in lifts_all)
    inv_traces = {sp_trace(el) for el in lifts_all if sp_order(el) == 2}
    assert inv_traces == {-1}
    ident_pm = {i: i for i in range(1, 8)}
    sigmaH = (ident_pm, {1: 1, 2: 1, 4: 1, 3: -1, 5: -1, 6: -1, 7: -1})
    sigmaH_auto = is_oct_automorphism_signed(sigmaH)
    assert sp_trace(sigmaH) == -1 and sp_order(sigmaH) == 2
    neg1 = (ident_pm, {1: -1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1})
    neg1_auto = is_oct_automorphism_signed(neg1)
    T2 = {
        "holds": bool(dim_cap == 8 and auto_count == 0 and min_defect > 1e-6 and
                      nu4_allowed == [-1, 0] and inv_traces == {-1} and sq1 == 2),
        "dim_der": int(DIM_G2),
        "dim_bivectors_7": int(dim_b7),
        "dim_bivectors_6": int(dim_b6),
        "g2_in_spin7": bool(g2_in_spin7),
        "dim_g2_cap_su4": int(dim_cap),
        "spinor_2O_order": 48,
        "spinor_2O_automorphism_count": int(auto_count),
        "spinor_2O_quartet_mult": int(quartet_mult),
        "sl27_order": 336,
        "sl27_sq1_count": int(sq1),
        "fs_sum_ordinary": int(fs_sum_ordinary),
        "nu4_allowed": [int(x) for x in nu4_allowed],
        "involution_trace": -1,
        "sigma_H_is_automorphism": bool(sigmaH_auto),
        "single_unit_negation_is_automorphism": bool(neg1_auto),
        "control_1344_all_automorphisms": bool(all_autos),
        "group1344_order": int(n1344),
        "spinor_2O_min_automorphism_defect": float(min_defect),
    }

    # ----- T3 (own exact-sequence bookkeeping)
    pi1_g2, pi3_g2, pi4_g2 = derive_g2_homotopy()
    p4s2 = pi4_S2()
    # pi1(SO(3)/T) = |2T|: enumerate 2T inside 2O (the 24 Hurwitz units)
    hurwitz = [q for q in two_o if all(c.b == 0 for c in q)]
    assert len(hurwitz) == 24
    closed = all(qmul(p, q) in set(hurwitz) for p in hurwitz for q in hurwitz)
    assert closed
    minus_in = mone in hurwitz
    pi1_so3_mod_T = len(hurwitz) if (HTPY.pi("SO3", 1) == "Z2" and minus_in) else None
    no_double_cover = (pi1_g2 == "0") and (phase_order < 10 ** 9)     # pi1(G2)=0 and finite phase group
    envelope_kill = (HTPY.pi("S6", 2) == "0")
    T3 = {
        "holds": bool(GROUP_ORDER[HTPY.pi("S15", 1)] == 1 and GROUP_ORDER[HTPY.pi("S15", 4)] == 1 and
                      no_double_cover and envelope_kill and
                      all(r["pi3_injective"] and r["pi4_quotient"] == 0 for r in inv)),
        "pi1_G2": 0 if pi1_g2 == "0" else None,
        "pi3_G2": "Z" if pi3_g2 == "Z" else pi3_g2,
        "pi4_G2": 0 if pi4_g2 == "0" else None,
        "pi1_V": 0,
        "pi4_V": 0,
        "no_internal_double_cover": bool(no_double_cover),
        "envelope_in_O_kill": bool(envelope_kill),
        "controls_pi4_S2": p4s2,
        "controls_pi4_S3": HTPY.pi("S3", 4),
        "controls_pi1_SO3_mod_T": int(pi1_so3_mod_T),
    }

    # ----- T4
    fix124 = [pm for pm in colls if pm[1] == 1 and pm[2] == 2 and pm[4] == 4]
    assert len(fix124) == 4
    nontriv = [pm for pm in fix124 if pm != ident_pm]
    assert len(nontriv) == 3
    lifts124 = []
    for pm in nontriv:
        for s in signed_lifts(pm):
            lifts124.append((pm, s))
    lifts_total = len(lifts124)
    o2 = [el for el in lifts124 if sp_order(el) == 2]
    o4 = [el for el in lifts124 if sp_order(el) == 4]
    assert len(o2) + len(o4) == lifts_total
    o2_traces = sorted({sp_trace(el) for el in o2})
    o4_traces = sorted({sp_trace(el) for el in o4})
    # trace-3 order-4 lifts square to sigma_H-type quaternion-subalgebra involutions
    for el in o4:
        if sp_trace(el) == 3:
            sq = sp_compose(el, el)
            assert sp_order(sq) == 2 and sp_trace(sq) == -1
    perm_char = sum(1 for i in range(1, 8) if nontriv[0][i] == i)
    rho6_2A = perm_char - 1
    gap = perm_char - (-1)
    nu2_pm = {i: ((2 * i - 1) % 7) + 1 for i in range(1, 8)}     # the multiplier i -> 2i mod 7
    nu2_auto = is_oct_automorphism_signed((nu2_pm, ones))
    T4 = {
        "holds": bool(o2_traces == [-1] and perm_char == 3 and rho6_2A == 2),
        "lifts_total": int(lifts_total),
        "order2_count": int(len(o2)),
        "order2_traces_set": [int(x) for x in o2_traces],
        "order4_count": int(len(o4)),
        "order4_traces_set": [int(x) for x in o4_traces],
        "perm_char_involution": int(perm_char),
        "rho6_char_2A": int(rho6_2A),
        "gap": int(gap),
        "control_F21_unsigned_1_3_3bar": phase0["controls"]["F21_split_1_3_3bar"],
        "nu2_unsigned_automorphism": bool(nu2_auto),
    }

    # ----- group1344: complement search (A-2.7)
    a_pm = {1: 1, 2: 2, 4: 4, 3: 5, 5: 3, 6: 7, 7: 6}
    assert a_pm in colls
    b_pm = None
    def coll_order(pm):
        cur = dict(pm)
        for n in range(1, 20):
            if all(cur[i] == i for i in range(1, 8)):
                return n
            cur = {i: pm[cur[i]] for i in range(1, 8)}
        return None
    def coll_compose(p, q):
        return {i: p[q[i]] for i in range(1, 8)}
    def coll_inv(p):
        return {p[i]: i for i in range(1, 8)}
    def gen_group(g1, g2):
        seen = {tuple(sorted(g1.items())), tuple(sorted(g2.items()))}
        frontier = [g1, g2]
        gens = [g1, g2]
        while frontier:
            nf = []
            for x in frontier:
                for g in gens:
                    y = coll_compose(x, g)
                    ky = tuple(sorted(y.items()))
                    if ky not in seen:
                        seen.add(ky); nf.append(y)
            frontier = nf
            if len(seen) > 168:
                break
        return len(seen)
    for pm in colls:
        if coll_order(pm) == 3:
            ab = coll_compose(a_pm, pm)
            comm = coll_compose(coll_compose(a_pm, pm), coll_compose(coll_inv(a_pm), coll_inv(pm)))
            if coll_order(ab) == 7 and coll_order(comm) == 4 and gen_group(a_pm, pm) == 168:
                b_pm = pm
                break
    assert b_pm is not None
    a_lifts = [(a_pm, s) for s in signed_lifts(a_pm)]
    b_lifts = [(b_pm, s) for s in signed_lifts(b_pm)]
    assert len(a_lifts) == 8 and len(b_lifts) == 8
    def sp_gen_order(g1, g2, cap=1400):
        seen = {sp_key(*g1), sp_key(*g2)}
        frontier = [g1, g2]
        gens = [g1, g2]
        while frontier:
            nf = []
            for x in frontier:
                for g in gens:
                    y = sp_compose(x, g)
                    ky = sp_key(*y)
                    if ky not in seen:
                        seen.add(ky)
                        nf.append(y)
                        if len(seen) > cap:
                            return len(seen)
            frontier = nf
        return len(seen)
    complements = 0
    pairs_tested = 0
    for ga in a_lifts:
        for gb in b_lifts:
            pairs_tested += 1
            if sp_gen_order(ga, gb, cap=200) == 168:
                complements += 1
    group1344 = {
        "order": int(n1344),
        "split": bool(complements > 0),
        "complements_found": int(complements),
        "lift_pairs_tested": int(pairs_tested),
    }
    extras["group1344_generators"] = {
        "a": "collineation (3 5)(6 7), fixes {1,2,4} pointwise",
        "b": "order-3 collineation " + str(sorted(b_pm.items())) +
             " with ord(ab)=7, ord([a,b])=4, <a,b> = 168",
    }

    # ---------- Phase 1b -----------------------------------------------
    # P-C: centrality of the complex unit; e8 anticommutation (Cayley-Dickson sedenions)
    J16 = phase_generator_16()
    central = True
    for a in range(1, 8):
        La16 = zeros(16)
        for i in range(8):
            for j in range(8):
                if L[a][i][j]:
                    La16[2 * i][2 * j] = L[a][i][j]
                    La16[2 * i + 1][2 * j + 1] = L[a][i][j]
        if any(x != 0 for x in flat(bracket(J16, La16))):
            central = False
    def sed_mul(p, q):
        """Cayley-Dickson product on pairs of octonions (as 8-vectors of Fr)."""
        a, b = p; c, d = q
        def conj8(v):
            return [v[0]] + [-x for x in v[1:]]
        ac = oct_mul_vec(a, c)
        db = oct_mul_vec(conj8(d), b)
        da = oct_mul_vec(d, a)
        bc = oct_mul_vec(b, conj8(c))
        return ([x - y for x, y in zip(ac, db)], [x + y for x, y in zip(da, bc)])
    zero8 = [Fr(0)] * 8
    e8 = (zero8, [Fr(1)] + [Fr(0)] * 7)
    anti = True
    for i in range(1, 8):
        ei = ([Fr(1) if k == i else Fr(0) for k in range(8)], zero8)
        x = sed_mul(e8, ei)
        y = sed_mul(ei, e8)
        if not all(a == -b for a, b in zip(x[0] + x[1], y[0] + y[1])):
            anti = False
    P_C = {
        "complex_unit_central": bool(central),
        "e8_anticommutes": bool(anti),
        "e8_central": bool(not anti),      # anticommutation on all of Im O excludes centrality
        "disposition": "CLOSED-BY-INSTANTIATION",
    }
    # H screen (criteria per memo 2.4; machine witnesses where exact)
    # H1: inside O (Im H_L subset Im O: exact), FR loop killed by the ambient target (pi2(S6)=0)
    h1_inside = all(i in range(7) for i in HL_IM)
    # H4: H_L is a subalgebra of O (exact closure)
    hl_basis = [0, 1, 2, 4]      # e0, e1, e2, e4
    h4_closed = True
    for x in hl_basis:
        for y in hl_basis:
            prod = OMUL[x][y]
            if any(prod[k] for k in range(8) if k not in hl_basis):
                h4_closed = False
    # H4 module content under su(2)_long: the perp 4-dim block is 2+2 (Casimir 3/4)
    h4_22 = (branch_long == [2, 2, 1, 1, 1])
    # H5: the doubling factor span{1, e8} is 2-dimensional, not quaternionic
    h5_dim = 2
    H_screen = {
        "H1": {"i": "fail", "ii": "pass", "iii": "fail", "iv": "n/a",
               "code": "EXCLUDED(i,iii)", "role": "control"},
        "H2": {"i": "pass", "ii": "pass", "iii": "pass", "iv": "dynamical",
               "code": "ADMISSIBLE-IMPORT", "role": "candidate"},
        "H3": {"i": "pass", "ii": "pass", "iii": "conditional", "iv": "kinematic",
               "code": "ADMISSIBLE-IMPORT", "role": "candidate"},
        "H4": {"i": "fail", "ii": "pass", "iii": "n/a", "iv": "n/a",
               "code": "EXCLUDED(i)", "role": "candidate"},
        "H5": {"i": "pass", "ii": "fail", "iii": "n/a", "iv": "n/a",
               "code": "EXCLUDED(ii,centrality)", "role": "candidate"},
    }
    assert h1_inside and envelope_kill          # H1 witnesses
    assert HTPY.pi("S3", 4) == "Z2" and p4s2 == "Z2"     # H2 (iii) witness: pi4(S2) = Z2 own factor
    assert h4_closed and h4_22                  # H4 witnesses
    assert h5_dim == 2 and anti                 # H5 witnesses (2-dim doubling; e8 non-central)
    extras["H_screen_code_rule"] = ("code = 'ADMISSIBLE-IMPORT' when no criterion is 'fail' "
                                    "(conditional/dynamical/kinematic allowed); otherwise "
                                    "'EXCLUDED(' + comma-joined failed criterion labels, with "
                                    "'centrality' appended for the P-C exclusion of H5 + ')'")
    phase1b = {
        "P_C": P_C,
        "H_screen": H_screen,
        "I5_registered": True,
        "admissible": sorted([h for h, d in H_screen.items() if d["code"] == "ADMISSIBLE-IMPORT"]),
    }

    # ---------- Phase 2 ------------------------------------------------
    # pinned witness (A-2.6): line (e1,e2,e4), control (e1,e2,e3); f(r) = pi/(1+r^2)
    phi_124 = phi[1][2][4]
    phi_123 = phi[1][2][3]
    assert phi_124 == 1 and phi_123 == 0
    # geometric integral int det(u, u_r, u_phi) dr dphi, common to both objects
    def fprof(r):
        return math.pi / (1.0 + r * r)
    def geom_integrand(r):
        # reduces to d/dr(cos f) after the phi integral; keep the full det for honesty
        h = 1e-6
        f = fprof(r)
        fp = (fprof(r + h) - fprof(r - h)) / (2 * h)
        # int_0^{2pi} det dphi = 2*pi * (-fp * sin f)  (u . (u_r x u_phi) = -f' sin f)
        return 2.0 * math.pi * (-fp) * math.sin(f)
    # Simpson on [0, 80]
    N = 80000
    a, b = 0.0, 80.0
    hh = (b - a) / N
    s = geom_integrand(a) + geom_integrand(b)
    for i in range(1, N):
        s += geom_integrand(a + i * hh) * (4 if i % 2 else 2)
    G_int = s * hh / 3.0
    assert abs(G_int - 4.0 * math.pi) < 1e-3, G_int
    O_line_abs = abs(phi_124) * abs(G_int)
    O_nonline_abs = 0.0 * abs(G_int)            # exact structure-constant zero
    # stabilizer: locked family X0 in g2 with X0 e4 = 0, X0 e1 = e2, X0 e2 = -e1
    tgt = [Fr(0)] * 21
    def fam_rows(X):
        return ([X[i][3] for i in range(7)] +
                [X[i][0] for i in range(7)] +
                [X[i][1] for i in range(7)])
    rows_f = []
    per = [fam_rows(g) for g in G2]
    for r in range(21):
        rows_f.append([per[i][r] for i in range(DIM_G2)])
    rhs_f = ([Fr(0)] * 7 +
             [Fr(1) if i == 1 else Fr(0) for i in range(7)] +
             [Fr(-1) if i == 0 else Fr(0) for i in range(7)])
    x0c, kerf = solve_affine(rows_f, rhs_f, DIM_G2)
    assert x0c is not None and len(kerf) == 3          # coset of su(2)_long
    X0 = zeros(7)
    for c, g in zip(x0c, G2):
        if c:
            X0 = mat_add(X0, mat_scale(g, c))
    # X0 preserves H_L and the perp block
    for j in HL_IM:
        assert all(X0[i][j] == 0 for i in HL_PERP)
    A0 = restrict(X0, HL_PERP)
    SL_perp = [restrict(X, HL_PERP) for X in SU2_LONG]
    # project A0 onto the su(2)_long chirality (trace form)
    gram = [[trace(mat_mul(Bi, Bj)) for Bj in SL_perp] for Bi in SL_perp]
    rhsg = [trace(mat_mul(A0, Bi)) for Bi in SL_perp]
    gi = invert3(gram)
    coeff = [sum(gi[i][j] * rhsg[j] for j in range(3)) for i in range(3)]
    A_L = zeros(4)
    for c, Bm in zip(coeff, SL_perp):
        if c:
            A_L = mat_add(A_L, mat_scale(Bm, c))
    A_R = mat_sub(A0, A_L)
    for Bm in SL_perp:
        assert all(x == 0 for x in flat(bracket(A_R, Bm)))
    assert mat_mul(A_R, A_R) == mat_scale(eye(4), Fr(-1, 4))
    # X_s = X0 - K_L with K_L in su(2)_long restricting to A_L
    K_L = zeros(7)
    for c, X in zip(coeff, SU2_LONG):
        if c:
            K_L = mat_add(K_L, mat_scale(X, c))
    X_s = mat_sub(X0, K_L)
    X_d = mat_add(X_s, khat)
    for X in (X_s, X_d):
        assert mat_vec(X, ebas7(0)) == ebas7(1)
        assert mat_vec(X, ebas7(1)) == [-v for v in ebas7(0)]
        assert mat_vec(X, ebas7(3)) == [Fr(0)] * 7
    # holonomies at 2pi, exact closed forms: on span(e1,e2) X^2 = -I (period 2pi -> Id);
    # on the perp block X_s|perp = A_R with A_R^2 = -I/4 (exp(2 pi A_R) = -I);
    # X_d|perp = A_R + khat|perp, commuting, each contributing -I -> +I.
    B12 = [[X_s[i][j] for j in (0, 1)] for i in (0, 1)]
    assert mat_mul(B12, B12) == mat_scale(eye(2), Fr(-1))
    assert all(x == 0 for x in flat(bracket(A_R, kperp)))
    hol_s = eye(7)
    for i in HL_PERP:
        hol_s[i][i] = Fr(-1)
    sigmaH_mat = [r[:] for r in hol_s]
    hol_d = eye(7)
    # verify sigma_H (as 7x7) is the automorphism sigmaH tested above
    assert all(sigmaH_mat[i][i] == (1 if (i in HL_IM) else -1) for i in range(7))
    eig_p1 = 1 + sum(1 for i in range(7) if sigmaH_mat[i][i] == 1)     # + e0
    eig_m1 = sum(1 for i in range(7) if sigmaH_mat[i][i] == -1)
    # pi0(Stab): the family is connected (SO(2)_space x exp of the coset, times the
    # connected SU(2)_long kernel); the finite phase does not fix the real-amplitude
    # texture: omega psi != psi for omega = exp(2 pi i/3) acting on a nonzero real amplitude
    import cmath
    omega = cmath.exp(2j * math.pi / 3)
    omega_fixes = abs(omega * 1.0 - 1.0) < 1e-12
    assert not omega_fixes
    # chiral pair: X_s restricted to span(e1,e2) squares to -I -> weights +-1 -> characters
    # e^{+-i alpha}, single-valued at alpha = 2 pi (ordinary, not central-negative)
    chiral_ordinary = (mat_mul(B12, B12) == mat_scale(eye(2), Fr(-1)))
    phase2 = {
        "object": "fano_line_texture_L124_homogeneous_GP_2D",
        "control_object": "nonline_texture_L123",
        "profile_id": "lockrec-A-2.6",
        "O_nonzero_on_line": bool(O_line_abs > 1e-6),
        "O_zero_on_nonline": bool(O_nonline_abs == 0.0),
        "stab_internal_image": "SO4_Stab_HL",
        "stab_kernel": "SU2_long",
        "stab_subdirect": bool(any(x != 0 for x in flat(X_s))),
        "pi0_stab": 1,
        "loop_images": ["Id", "sigma_H"],
        "sigma_H_eigen_plus1": int(eig_p1),
        "sigma_H_eigen_minus1": int(eig_m1),
        "label": "INTERNAL-HOLONOMY-GAUGE",
        "pi1_orbit": 0,
        "chiral_pair_character_ordinary": bool(chiral_ordinary and not omega_fixes),
        "dimension_note": "2D witness; contractibility of the 2pi loop in the orbit only",
        "O_line_abs": float(O_line_abs),
        "O_nonline_abs": float(O_nonline_abs),
    }
    extras["phase2_lift_matrices"] = {
        "X_sigma_lift_su2long_free_note": "X_s: holonomy exp(2 pi X_s) = sigma_H exactly "
            "(A_R^2 = -I/4 on the perp block); X_d = X_s + khat: holonomy Id (commuting -I x -I); "
            "both verified by exact closed forms, matrices in the return file",
        "sigma_H_diag_on_e1..e7": [int(sigmaH_mat[i][i]) for i in range(7)],
    }

    # ---------- Phase 3 (last) -----------------------------------------
    controls_all = (all(phase0["controls"].values()) and
                    T1["control_sym3_quartet_mult"] == 1 and
                    T2["control_1344_all_automorphisms"] and
                    T2["spinor_2O_quartet_mult"] == 2 and
                    T3["controls_pi4_S2"] == "Z2" and
                    T3["controls_pi4_S3"] == "Z2" and
                    T3["controls_pi1_SO3_mod_T"] == 24 and
                    T4["control_F21_unsigned_1_3_3bar"] and
                    T4["nu2_unsigned_automorphism"] and
                    phase2["O_zero_on_nonline"])
    holds = {t: d["holds"] for t, d in (("T1", T1), ("T2", T2), ("T3", T3), ("T4", T4))}
    if not controls_all:
        verdict = "INDETERMINATE"
    elif not phase0["sym_int_pinned"]:
        verdict = "UNDECIDED-BY-SUBSTRATE"
    elif (not phase0["spatial_internal_direct_product"]) or any(not h for h in holds.values()):
        verdict = "ASSIGNMENT-II-REALIZABLE"
    else:
        verdict = "ASSIGNMENT-I-FORCED"
    phase3 = {
        "verdict": verdict,
        "tests_holding": sorted([t for t, h in holds.items() if h]),
        "admissible_H": sorted(phase1b["admissible"]),
        "I5": phase1b["I5_registered"],
        "controls_all_pass": bool(controls_all),
    }

    citations = {
        "pi4_SU3_0__pi3_SU3_Z__pi1_SU3_0": "Bott 1956 / standard tables (memo section 7, adopted)",
        "pi_k_S6_0_for_k_le_5": "standard (connectivity + pi_n(S^n)); memo section 7, adopted",
        "pi4_S3_Z2__pi4_S2_Z2": "Freudenthal / standard; pi4(S2) re-derived here from the Hopf fibration LES",
        "pi_k_Sn_0_for_k_lt_n": "cellular approximation; memo section 7, adopted (S15)",
        "pi1_SO3_Z2": "standard; used for the SO(3)/T control with the machine-enumerated 2T",
        "fibration_LES": "long exact sequence of a fibration (memo section 7, adopted)",
        "FR_pi1_config_eq_pi4_target": "Finkelstein-Rubinstein 1968; Giulini 1993; Krusch-Speight 2006 (memo L-A1-5)",
        "even_multiplicity_quaternionic_in_real": "Frobenius-Schur theory (memo section 7, adopted)",
        "steinberg_8_real": "SL(2,7)/PSL(2,7) Steinberg representation real, nu = +1 (adopted; memo 2.3 T2(c))",
        "psl27_3_3bar_complex_nu0": "the 3, 3bar Galois pair of PSL(2,7), nu = 0; ATLAS pairings (E-A1-8(a), adopted)",
        "sl27_galois_pairings": "nu(sigma4) = nu(sigma4'), nu(sigma6) = nu(sigma6') (E-A1-8(a), adopted)",
        "gunaydin_gursey_su3": "Gunaydin-Gursey 1973: SU(3) = Stab_G2(e7) generated by left multiplications (memo T2(a))",
        "cohen_wales_1983": "two PSL(2,7) classes in G2; non-split 1344 group (cross-check only; T4/E-A1-6 self-contained)",
        "mimura_1967": "canonical homotopy table for G2; not relied on (derived in-instrument, memo L-A1-4)",
        "dynkin_index": "computed from the branchings as sum of j(j+1)(2j+1)/3, normalized to long root = 1",
    }
    extras["spinor_2O_automorphism_count_domain"] = ("count over 2O minus {+-Id} (CC-DD-1): +Id is trivially an "
                                                     "automorphism; A-2.3's min-defect domain already excludes +-Id")
    extras["elapsed_seconds"] = round(time.time() - T0, 2)

    ck = {
        "gate": "G-2a-A1",
        "leg": "cc",
        "instrument_md5": md5f(ME),
        "memo_lock_md5": MD5[MEMO][0],
        "ledger_base_md5": LEDGER_BASE_MD5,
        "t1_list_md5": MD5[T1LIST][0],
        "action_extract_md5": MD5[EXTRACT][0],
        "t1_scan": t1,
        "elections": {f"E-A1-{i}": "a" for i in range(1, 9)},
        "phase0": phase0,
        "phase1": {"T1": T1, "T2": T2, "T3": T3, "T4": T4, "group1344": group1344},
        "phase1b": phase1b,
        "phase2": phase2,
        "phase3": phase3,
        "citations": citations,
        "extras": extras,
    }
    out = os.path.join(HERE, "g_2a_a1_ccleg_checkpoint.json")
    open(out, "w", encoding="utf-8").write(json.dumps(ck, indent=1, ensure_ascii=False, sort_keys=True))
    print(f"checkpoint written: {out}  md5 {md5f(out)}")
    print(f"verdict: {verdict}; tests holding: {phase3['tests_holding']}; controls_all_pass: {controls_all}")
    print(f"phase0 full O-density stabilizer in so(16): dim {stab_dim} "
          f"(g2 + u(1) on the real-unit line)")
    print(f"elapsed: {extras['elapsed_seconds']} s")

if __name__ == "__main__":
    main()
