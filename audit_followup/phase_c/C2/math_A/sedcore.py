"""
sedcore.py  --  shared exact core for the C2 math_A checks.

Independent rebuild of the program's Cayley-Dickson convention
    (a,b)(c,d) = (ac - conj(d) b,  d a + b conj(c))
on basis e0..e(2^n - 1), e_i e_j = s(i,j) e_{i XOR j}, s in {+1,-1}.
Cross-checked against tools/sedenion_Fp.py by xcheck_tool_table().

Everything here is integer-exact; F_p work is done only where a script says so.
"""
from itertools import product, permutations, combinations
import numpy as np

# ---------------------------------------------------------------- CD table
def cd_sign_table(n_levels):
    """S[i][j] = s with e_i e_j = s e_{i^j} in the 2^n_levels-dim CD algebra."""
    S = [[1]]
    for lev in range(1, n_levels + 1):
        h = 2 ** (lev - 1)
        D = 2 * h
        T = [[0] * D for _ in range(D)]
        csg = lambda c: 1 if c == 0 else -1          # conj(e_c) = csg(c) e_c
        for i in range(D):
            for j in range(D):
                if i < h and j < h:                   # (a,0)(c,0) = (ac, 0)
                    T[i][j] = S[i][j]
                elif i < h and j >= h:                # (a,0)(0,d) = (0, d a)
                    d = j - h
                    T[i][j] = S[d][i]
                elif i >= h and j < h:                # (0,b)(c,0) = (0, b conj(c))
                    b = i - h
                    T[i][j] = S[b][j] * csg(j)
                else:                                 # (0,b)(0,d) = (-conj(d) b, 0)
                    b, d = i - h, j - h
                    T[i][j] = -csg(d) * S[d][b]
        S = T
    return S

SED = cd_sign_table(4)          # 16 x 16 signs
OCT = [row[:8] for row in SED[:8]]
DIM = 16

def mul_basis(i, j):
    return (i ^ j, SED[i][j])

def mul(x, y):
    """Exact product of two integer coefficient vectors (len 16)."""
    out = [0] * DIM
    for i, xi in enumerate(x):
        if xi == 0:
            continue
        for j, yj in enumerate(y):
            if yj == 0:
                continue
            out[i ^ j] += SED[i][j] * xi * yj
    return out

def basis(i, c=1):
    v = [0] * DIM
    v[i] = c
    return v

def elem(terms):
    """terms: dict or list of (index, coeff)."""
    v = [0] * DIM
    for i, c in (terms.items() if isinstance(terms, dict) else terms):
        v[i] += c
    return v

# left-multiplication matrices of basis elements (signed permutation matrices)
LBASIS = np.zeros((DIM, DIM, DIM), dtype=np.int64)    # LBASIS[i] = L_{e_i}
for i in range(DIM):
    for j in range(DIM):
        LBASIS[i, i ^ j, j] = SED[i][j]                 # column j = e_i e_j

def Lmat(x):
    """Integer left-multiplication matrix of x (column j = x e_j)."""
    M = np.zeros((DIM, DIM), dtype=np.int64)
    for i, c in enumerate(x):
        if c:
            M += c * LBASIS[i]
    return M

def xcheck_tool_table(tool_dir="/home/claude/gifgaf0.github.io/tools"):
    """Compare SED with tools/sedenion_Fp.py MULT. Returns number of mismatches."""
    import sys, io, contextlib
    sys.path.insert(0, tool_dir)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import sedenion_Fp as T
    sys.path.pop(0)
    bad = 0
    for i in range(16):
        for j in range(16):
            terms = T.MULT[i][j]
            if len(terms) != 1 or terms[0] != (i ^ j, SED[i][j]):
                bad += 1
    return bad

# ---------------------------------------------------------------- Fano / GL(3,2)
PTS = list(range(1, 8))
LINES = sorted({frozenset((i, j, i ^ j)) for i in PTS for j in PTS if i < j},
               key=lambda s: sorted(s))
assert len(LINES) == 7

def oriented_triples(T=OCT):
    """(i,j,k) with e_i e_j = +e_k, i,j,k in 1..7 distinct."""
    return {(i, j, i ^ j) for i in PTS for j in PTS
            if i != j and T[i][j] == 1}

def gl32_perms():
    """All 168 collineations of the XOR Fano plane, as dicts on 1..7 (=GL(3,2))."""
    out = []
    for M in product([0, 1], repeat=9):
        rows = [M[0:3], M[3:6], M[6:9]]
        def app(v):
            bits = [(v >> 2) & 1, (v >> 1) & 1, v & 1]
            r = [sum(rows[k][t] * bits[t] for t in range(3)) % 2 for k in range(3)]
            return r[0] * 4 + r[1] * 2 + r[2]
        img = [app(v) for v in PTS]
        if 0 in img or len(set(img)) != 7:
            continue
        out.append(tuple(img))                   # img[i-1] = pi(i)
    out = sorted(set(out))
    assert len(out) == 168
    return out

def perm_dict(t):
    return {i: t[i - 1] for i in PTS}

def is_collineation(pi):
    return all(frozenset(pi[i] for i in L) in LINES for L in LINES)

# ---------------------------------------------------------------- signed maps
def octonion_signed_auto(pi, eps):
    """pi: dict on 1..7, eps: dict on 1..7 in {+1,-1}.
       True iff e_i -> eps_i e_pi(i) (e0 fixed) is an automorphism of the octonions."""
    for i in PTS:
        for j in PTS:
            if i == j:
                continue
            k = i ^ j
            if pi[i] ^ pi[j] != pi[k]:
                return False
            if OCT[i][j] * eps[k] != eps[i] * eps[j] * OCT[pi[i]][pi[j]]:
                return False
    return True

def sed_lift_matrix(pi, eps, e8sign=1):
    """16x16 integer matrix of the CD lift: e_i -> eps_i e_pi(i),
       e_{i+8} -> e8sign*eps_i e_{pi(i)+8}, e0 -> e0, e8 -> e8sign*e8."""
    P = np.zeros((DIM, DIM), dtype=np.int64)
    P[0, 0] = 1
    P[8, 8] = e8sign
    for i in PTS:
        P[pi[i], i] = eps[i]
        P[pi[i] + 8, i + 8] = e8sign * eps[i]
    return P

def is_sed_automorphism(P):
    """Check P(e_i e_j) = P(e_i) P(e_j) for all 256 basis products (exact)."""
    cols = [P[:, j].tolist() for j in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            lhs = (SED[i][j] * P[:, i ^ j]).tolist()
            rhs = mul(cols[i], cols[j])
            if lhs != rhs:
                return False
    return True

def is_sed_antiautomorphism(P):
    cols = [P[:, j].tolist() for j in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            lhs = (SED[i][j] * P[:, i ^ j]).tolist()
            rhs = mul(cols[j], cols[i])
            if lhs != rhs:
                return False
    return True

# ---------------------------------------------------------------- batch rank mod p
def _modinv_vec(a, p):
    """Vectorized a^(p-2) mod p for int64 arrays, p < 2^31."""
    a = a % p
    res = np.ones_like(a)
    e = p - 2
    base = a.copy()
    while e:
        if e & 1:
            res = (res * base) % p
        base = (base * base) % p
        e >>= 1
    return res

def rank_mod_p_batch(Ms, p):
    """Ms: (B,16,16) int64. Returns (B,) ranks over F_p (Gauss-Jordan, vectorized)."""
    A = np.mod(Ms, p).astype(np.int64)
    Bn, R, C = A.shape
    used = np.zeros((Bn, R), dtype=bool)
    rank = np.zeros(Bn, dtype=np.int64)
    ar = np.arange(Bn)
    for c in range(C):
        cand = (A[:, :, c] != 0) & (~used)
        has = cand.any(axis=1)
        if not has.any():
            continue
        idx = ar[has]
        piv = cand[idx].argmax(axis=1)
        prow = A[idx, piv, :]
        inv = _modinv_vec(prow[:, c], p)
        prow = (prow * inv[:, None]) % p
        fac = A[idx, :, c].copy()
        sub = A[idx] - (fac[:, :, None] * prow[:, None, :]) % p
        sub %= p
        sub[np.arange(len(idx)), piv, :] = prow
        A[idx] = sub
        used[idx, piv] = True
        rank[idx] += 1
    return rank

def exact_rank(M):
    import flint
    return flint.fmpz_mat(M.tolist()).rank()

# ---------------------------------------------------------------- misc
def chi7(x):
    x %= 7
    if x == 0:
        return 0
    return 1 if x in (1, 2, 4) else -1

if __name__ == "__main__":
    print("tool-table mismatches:", xcheck_tool_table())
    print("e1e2 =", mul_basis(1, 2), " e1e9 =", mul_basis(1, 9), " e9e1 =", mul_basis(9, 1))
    print("Fano lines (XOR):", [sorted(L) for L in LINES])
    print("oriented triples:", sorted(oriented_triples()))
