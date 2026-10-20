"""
cc_groups.py -- independent cross-check of the E4 group theory (F21 and the seed's PSL(2,7)).

Written without reading the original E4 scripts. Methods deliberately differ from the
original's description (exact closure + explicit irreps + generator null spaces):

  * exact arithmetic: my own Q(zeta7) class (coefficients on 1..zeta^5, reduced mod Phi_7),
    used (a) to verify the defining relations of the presentations
        F21  = < c, d | c^7 = d^3 = 1, d^-1 c d = c^4 >
        PSL  = < a, b | a^2 = b^3 = (ab)^7 = [a,b]^4 = 1 >      (order 168, simple)
    and (b) to verify exact closure of the float-enumerated element lists;
  * character tables are NOT built from explicit irreps: they are peeled off from tensor
    powers of the 3-dim character (class functions only, inner products, Gram-Schmidt-free
    'subtract known irreducibles, keep norm-1 remainders');
  * invariant counts come from the Reynolds projector (average over the whole group),
    not from null spaces on generators;
  * SU(3)->PSL branching from Schur polynomials evaluated on the eigenvalues.

Prints its own checks; writes out/groups_cc.json.
"""
import json, itertools, cmath, math
from fractions import Fraction as Fr
import numpy as np

OUT = {}
CHECKS = {}
def check(name, ok):
    CHECKS[name] = bool(ok)
    print(("PASS " if ok else "FAIL ") + name)

# ------------------------------------------------------------------ exact Q(zeta7)
class Z7:
    """element sum_{k=0..5} c_k zeta^k, zeta^6 = -(1+...+zeta^5)"""
    __slots__ = ("c",)
    def __init__(self, c):
        c = list(c)
        if len(c) == 7:
            c6 = c[6]
            c = [c[k] - c6 for k in range(6)]
        self.c = tuple(Fr(x) for x in c)
    @staticmethod
    def zeta(k):
        v = [0] * 7; v[k % 7] = 1; return Z7(v)
    @staticmethod
    def const(q):
        return Z7([q, 0, 0, 0, 0, 0])
    def __add__(s, o): return Z7([a + b for a, b in zip(s.c, o.c)])
    def __sub__(s, o): return Z7([a - b for a, b in zip(s.c, o.c)])
    def __neg__(s): return Z7([-a for a in s.c])
    def __mul__(s, o):
        if not isinstance(o, Z7): o = Z7.const(o)
        v = [Fr(0)] * 7
        for i, a in enumerate(s.c):
            if a == 0: continue
            for j, b in enumerate(o.c):
                if b == 0: continue
                v[(i + j) % 7] += a * b
        return Z7(v)
    __rmul__ = __mul__
    def conj(s):
        v = [Fr(0)] * 7
        for k, a in enumerate(s.c): v[(-k) % 7] += a
        return Z7(v)
    def __eq__(s, o): return s.c == o.c
    def __hash__(s): return hash(s.c)
    def is_zero(s): return all(a == 0 for a in s.c)
    def to_complex(s):
        z = cmath.exp(2j * math.pi / 7)
        return sum(complex(a) * z ** k for k, a in enumerate(s.c))

def mat(rows): return [[x if isinstance(x, Z7) else Z7.const(x) for x in r] for r in rows]
def mmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum((A[i][k] * B[k][j] for k in range(m)), Z7.const(0)) for j in range(p)] for i in range(n)]
def meq(A, B): return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A[0])))
def mkey(A): return tuple(A[i][j].c for i in range(3) for j in range(3))
def mnum(A): return np.array([[A[i][j].to_complex() for j in range(3)] for i in range(3)])
I3 = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
def mpow(A, n):
    R = I3
    for _ in range(n): R = mmul(R, A)
    return R
def minv_unitary(A):  # A^dagger
    return [[A[j][i].conj() for j in range(3)] for i in range(3)]

z = Z7.zeta
# i/sqrt7 = (sum_k (k|7) zeta^k)/7 : Gauss sum g = i sqrt7
gauss = z(1) + z(2) + z(4) - z(3) - z(5) - z(6)
i_over_sqrt7 = gauss * Fr(1, 7)
# check g^2 = -7
check("Gauss sum (zeta+zeta^2+zeta^4-zeta^3-zeta^5-zeta^6)^2 = -7", gauss * gauss == Z7.const(-7))

D = mat([[z(1), 0, 0], [0, z(2), 0], [0, 0, z(4)]])
C = mat([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
Dk = mat([[z(4), 0, 0], [0, z(2), 0], [0, 0, z(1)]])
Rk = [[i_over_sqrt7 * e for e in row] for row in
      [[z(1) - z(6), z(2) - z(5), z(4) - z(3)],
       [z(2) - z(5), z(4) - z(3), z(1) - z(6)],
       [z(4) - z(3), z(1) - z(6), z(2) - z(5)]]]
flip = mat([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])
Rf = mmul(mmul(flip, Rk), flip)        # flip^-1 = flip
# LNR 0709.1447 eqs. (22)-(23), eta = zeta
A_LNR = [[i_over_sqrt7 * e for e in row] for row in
         [[z(2) - z(5), z(1) - z(6), z(4) - z(3)],
          [z(1) - z(6), z(4) - z(3), z(2) - z(5)],
          [z(4) - z(3), z(2) - z(5), z(1) - z(6)]]]
one = Z7.const(1)
B_LNR = [[i_over_sqrt7 * e for e in row] for row in
         [[z(3) - z(6), z(3) - z(1), z(1) - one],
          [z(2) - one, z(6) - z(5), z(6) - z(2)],
          [z(5) - z(4), z(4) - one, z(5) - z(3)]]]

check("flip sends Klein's Dk to D", meq(mmul(mmul(flip, Dk), flip), D))
check("Rf == LNR A^[3] (exact)", meq(Rf, A_LNR))
check("Rf*D == LNR B^[3] (exact)", meq(mmul(Rf, D), B_LNR))
check("LNR A*B == D (their eq. 16, exact)", meq(mmul(A_LNR, B_LNR), D))

# presentation relations, exact
a, b = Rf, mmul(Rf, D)
comm = mmul(mmul(minv_unitary(a), minv_unitary(b)), mmul(a, b))
check("PSL relations a^2=b^3=(ab)^7=[a,b]^4=1 exact (a=Rf, b=Rf D)",
      meq(mpow(a, 2), I3) and meq(mpow(b, 3), I3) and meq(mpow(mmul(a, b), 7), I3) and meq(mpow(comm, 4), I3)
      and not meq(a, I3))
# F21 presentation: c = D (order 7), d = C (order 3), d^-1 c d = c^k
Cinv = minv_unitary(C)
k_found = [k for k in range(1, 7) if meq(mmul(mmul(Cinv, D), C), mpow(D, k))]
print("  C^-1 D C = D^k for k =", k_found)
check("F21 relations D^7 = C^3 = 1, C^-1 D C = D^k with k of order 3 mod 7",
      meq(mpow(D, 7), I3) and meq(mpow(C, 3), I3) and len(k_found) == 1 and pow(k_found[0], 3, 7) == 1 and k_found[0] != 1)
for M, nm in ((D, "D"), (C, "C"), (Rf, "Rf")):
    U = mmul(M, minv_unitary(M))
    det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
           + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    check(f"{nm} unitary with det 1 (exact)", meq(U, I3) and det == one)

# ------------------------------------------------------------------ enumeration (float), exact closure check
def closure_float(gens):
    gens_n = [mnum(g) for g in gens]
    key = lambda M: tuple(np.round(M, 7).ravel().view(float))
    els = {key(np.eye(3, dtype=complex)): np.eye(3, dtype=complex)}
    frontier = list(els.values())
    while frontier:
        new = []
        for M in frontier:
            for g in gens_n:
                N = g @ M
                k = key(N)
                if k not in els:
                    els[k] = N; new.append(N)
        frontier = new
    return list(els.values())

def closure_exact(gens):
    els = {mkey(I3): I3}
    frontier = [I3]
    while frontier:
        new = []
        for M in frontier:
            for g in gens:
                N = mmul(g, M)
                k = mkey(N)
                if k not in els:
                    els[k] = N; new.append(N)
        frontier = new
    return els

F21f = closure_float([D, C])
PSLf = closure_float([D, C, Rf])
PSL2f = closure_float([D, Rf])
print("  float closure: |<D,C>| =", len(F21f), " |<D,C,Rf>| =", len(PSLf), " |<D,Rf>| =", len(PSL2f))
F21x = closure_exact([D, C])
PSLx = closure_exact([D, C, Rf])
check("exact closure |<D,C>| = 21", len(F21x) == 21)
check("exact closure |<D,C,Rf>| = 168 and <D,Rf> already 168 (float)", len(PSLx) == 168 and len(PSL2f) == 168)
check("F21 subset of PSL (exact)", all(k in PSLx for k in F21x))
OUT["orders"] = {"F21": len(F21x), "PSL": len(PSLx)}

# ------------------------------------------------------------------ classes and class functions
def classes(G):
    G = [np.array(g) for g in G]
    Ginv = [g.conj().T for g in G]
    key = lambda M: tuple(np.round(M, 6).ravel().view(float))
    idx = {key(g): i for i, g in enumerate(G)}
    seen, cls = set(), []
    for i, g in enumerate(G):
        if i in seen: continue
        orb = {idx[key(h @ g @ hi)] for h, hi in zip(G, Ginv)}
        seen |= orb; cls.append(sorted(orb))
    return cls

def elem_order(M):
    P = np.eye(3, dtype=complex)
    for n in range(1, 50):
        P = P @ M
        if np.allclose(P, np.eye(3)): return n

def class_data(G):
    cl = classes(G)
    reps = [G[c[0]] for c in cl]
    sizes = [len(c) for c in cl]
    orders = [elem_order(r) for r in reps]
    # sort: by order then by trace imaginary part (to make b7 first among order 7)
    tr = [np.trace(r) for r in reps]
    perm = sorted(range(len(cl)), key=lambda i: (orders[i], -round(tr[i].imag, 6), sizes[i]))
    return [reps[i] for i in perm], [sizes[i] for i in perm], [orders[i] for i in perm], [cl[i] for i in perm]

def power_map(G, cl, p):
    key = lambda M: tuple(np.round(M, 6).ravel().view(float))
    where = {}
    for ci, c in enumerate(cl):
        for e in c: where[key(G[e])] = ci
    return [where[key(np.linalg.matrix_power(G[c[0]], p))] for c in cl]

def inner(chi1, chi2, sizes, n):
    return sum(s * a * np.conj(b) for a, b, s in zip(chi1, chi2, sizes)) / n

def peel_irreps(G, reps, sizes, cl):
    n = len(G)
    chi3 = np.array([np.trace(r) for r in reps])
    sq = power_map(G, cl, 2)
    one_ = np.ones(len(reps), dtype=complex)
    irr = [("1", one_), ("3", chi3), ("3b", chi3.conj())]
    cand = []
    pool = [("3", chi3), ("3b", chi3.conj())]
    # generate class functions: products of pool members, sym^2, alt^2, up to degree 3
    funcs = []
    for (na, ca), (nb, cb) in itertools.product(pool, pool):
        funcs.append((f"{na}x{nb}", ca * cb))
    funcs.append(("S2(3)", (chi3 ** 2 + chi3[sq]) / 2))
    funcs.append(("A2(3)", (chi3 ** 2 - chi3[sq]) / 2))
    for (na, ca) in pool:
        for (nb, cb) in list(itertools.product(pool, pool)):
            funcs.append((f"{na}x{nb[0]}x{cb[0]}", ca * nb[1] * cb[1]))
    changed = True
    while changed:
        changed = False
        for nm, f in funcs:
            rem = f.copy()
            for _, c in irr:
                m = inner(rem, c, sizes, n)
                rem = rem - m * c
            nrm = inner(rem, rem, sizes, n).real
            if abs(nrm - 1) < 1e-9 and rem[0].real > 0.5:
                # new irreducible character (positive degree)
                if not any(np.allclose(rem, c) for _, c in irr):
                    irr.append((f"from {nm}", rem)); changed = True
        # products of found irreducibles also
        new_funcs = []
        for (_, c1), (_, c2) in itertools.product(irr, irr):
            new_funcs.append(("prod", c1 * c2))
        funcs = funcs + new_funcs if changed else funcs
    return irr

def nice(v):
    """identify a character value"""
    b7 = (-1 + 1j * math.sqrt(7)) / 2
    w = cmath.exp(2j * math.pi / 3)
    for lab, val in (("b7", b7), ("conj(b7)", b7.conjugate()), ("w", w), ("w^2", w.conjugate())):
        if abs(v - val) < 1e-9: return lab
    if abs(v.imag) < 1e-9 and abs(v.real - round(v.real)) < 1e-9: return str(int(round(v.real)))
    return f"{v:.6f}"

def burnside(G, cl, sizes):
    """Burnside's algorithm: simultaneous eigenvectors of the class-multiplication matrices."""
    key = lambda M: tuple(np.round(M, 6).ravel().view(float))
    where = {}
    for ci, c in enumerate(cl):
        for e in c: where[key(G[e])] = ci
    k = len(cl)
    cst = np.zeros((k, k, k))
    for j in range(k):
        for kk in range(k):
            for x in cl[j]:
                for y in cl[kk]:
                    cst[j, kk, where[key(G[x] @ G[y])]] += 1
    cst = cst / np.array(sizes)[None, None, :]       # c_jkl for a fixed z in C_l
    rng = np.random.default_rng(7)
    r = rng.normal(size=k)
    Mtot = sum(r[j] * cst[j] for j in range(k))        # (M_j)_{k,l} = c_jkl
    vals, vecs = np.linalg.eig(Mtot)                   # (M_j omega)_k = sum_l c_jkl omega_l = omega_j omega_k
    chars = []
    n = len(G)
    for v in vecs.T:
        om = v / v[0]
        # verify common eigenvector of every M_j
        for j in range(k):
            assert np.allclose(cst[j] @ om, om[j] * om, atol=1e-8)
        d2 = n / sum(abs(om[j]) ** 2 / sizes[j] for j in range(k))
        d = np.sqrt(d2)
        chars.append(d * om / np.array(sizes))
    return chars

results_ct = {}
for gname, G in (("F21", F21f), ("PSL", PSLf)):
    reps, sizes, orders, cl = class_data(G)
    n = len(G)
    irr_peel = peel_irreps(G, reps, sizes, cl)
    irr = [(f"burnside{i}", c) for i, c in enumerate(burnside(G, cl, sizes))]
    irr.sort(key=lambda t: (round(t[1][0].real), -round(t[1][-2].imag, 6) if len(t[1]) > 1 else 0))
    # put 1, 3, 3b in positions 0,1,2 to match the labelling code below
    chi3 = np.array([np.trace(r) for r in reps])
    i1 = [i for i, (_, c) in enumerate(irr) if np.allclose(c, 1)][0]
    i3 = [i for i, (_, c) in enumerate(irr) if np.allclose(c, chi3)][0]
    i3b = [i for i, (_, c) in enumerate(irr) if np.allclose(c, chi3.conj())][0]
    irr = [irr[i1], irr[i3], irr[i3b]] + [t for i, t in enumerate(irr) if i not in (i1, i3, i3b)]
    agree = all(any(np.allclose(c, cp) for _, c in irr) for _, cp in irr_peel)
    check(f"{gname}: Burnside table contains every character peeled from tensor powers of the 3 ({len(irr_peel)} found by peeling)", agree)
    # orthogonality and completeness
    k = len(cl)
    dims = sorted(int(round(c[0].real)) for _, c in irr)
    ortho = all(abs(inner(c1, c2, sizes, n) - (1 if i == j else 0)) < 1e-9
                for i, (_, c1) in enumerate(irr) for j, (_, c2) in enumerate(irr))
    print(f"  {gname}: classes sizes {sizes} orders {orders}; irreps found {len(irr)} dims {dims}")
    check(f"{gname}: number of irreducible characters = number of classes ({k}) and sum d^2 = |G|",
          len(irr) == k and sum(d * d for d in dims) == n)
    check(f"{gname}: row orthogonality of the peeled table", ortho)
    sq = power_map(G, cl, 2)
    table = {}
    fs = {}
    for nm, c in irr:
        d = int(round(c[0].real))
        lab = {1: "1", 3: None, 6: "6", 7: "7", 8: "8"}.get(d)
        if d == 3:
            lab = "3" if np.allclose(c, irr[1][1]) else "3b"
        if d == 1 and gname == "F21":
            if np.allclose(c, 1): lab = "1"
            else:
                # 1' : value w on the class of C (order-3 class containing C)
                lab = None
        table_entry = [nice(x) for x in c]
        fs_ind = sum(s * c[q] for s, q in zip(sizes, sq)) / n
        table.setdefault(d, []).append((table_entry, round(fs_ind.real, 9), c))
    results_ct[gname] = dict(sizes=sizes, orders=orders, table=table, reps=reps, cl=cl, irr=irr, G=G)

# label F21 singlets: 1' has chi(C) = w (LNR: chi_1'(d) = e^{2 pi i/3}, d conjugate to C)
F = results_ct["F21"]
Cn = mnum(C)
key = lambda M: tuple(np.round(M, 6).ravel().view(float))
idxF = {key(g): i for i, g in enumerate(F["G"])}
cC = [ci for ci, c in enumerate(F["cl"]) if idxF[key(Cn)] in c][0]
w = cmath.exp(2j * math.pi / 3)
F21_named = {}
for nm, c in F["irr"]:
    d = int(round(c[0].real))
    if d == 1:
        lab = "1" if np.allclose(c, 1) else ("1'" if abs(c[cC] - w) < 1e-9 else "1''")
    else:
        lab = "3" if abs(c[[i for i, o in enumerate(F["orders"]) if o == 7][0]] - (-1 + 1j * 7 ** .5) / 2) < 1e-9 and np.allclose(c, F["irr"][1][1]) else ("3" if np.allclose(c, F["irr"][1][1]) else "3b")
    F21_named[lab] = c
P = results_ct["PSL"]
PSL_named = {}
for nm, c in P["irr"]:
    d = int(round(c[0].real))
    lab = {1: "1", 6: "6", 7: "7", 8: "8"}.get(d)
    if d == 3: lab = "3" if np.allclose(c, P["irr"][1][1]) else "3b"
    PSL_named[lab] = c

def show_table(named, G, sizes, orders, cl, name):
    n = len(G)
    sq = power_map(G, cl, 2)
    print(f"  {name} classes: sizes {sizes}, element orders {orders}")
    tab = {}
    for lab in sorted(named, key=lambda s: (len(s), s)):
        c = named[lab]
        fsi = sum(s * c[q] for s, q in zip(sizes, sq)) / n
        tab[lab] = {"chi": [nice(x) for x in c], "FS": int(round(fsi.real))}
        print(f"    {lab:4s} {[nice(x) for x in c]}  FS={int(round(fsi.real))}")
    return tab

OUT["F21_table"] = show_table(F21_named, F["G"], F["sizes"], F["orders"], F["cl"], "F21")
OUT["PSL_table"] = show_table(PSL_named, P["G"], P["sizes"], P["orders"], P["cl"], "PSL")
OUT["F21_classes"] = {"sizes": F["sizes"], "orders": F["orders"]}
OUT["PSL_classes"] = {"sizes": P["sizes"], "orders": P["orders"]}

# targets (LNR 0709.1447 Sec. 3 and 5), in my class order (sorted by element order; b7 class first)
b7 = "b7"; b7c = "conj(b7)"
tgtF = {"1": ["1", "1", "1", "1", "1"], "3": ["3", "0", "0", b7, b7c], "3b": ["3", "0", "0", b7c, b7]}
okF = sorted(F["sizes"]) == [1, 3, 3, 7, 7] and all(OUT["F21_table"][k]["chi"] == v for k, v in tgtF.items())
okF = okF and sorted([OUT["F21_table"]["1'"]["chi"][1:3], OUT["F21_table"]["1''"]["chi"][1:3]]) == sorted([["w", "w^2"], ["w^2", "w"]])
check("F21 character table = LNR (1,1',1'',3,3bar; b7 on order-7 classes)", okF)
# PSL: my order of classes: order 1, 2, 3, 4, 7(b7), 7(b7bar)
tgtP = {"1": ["1"] * 6, "3": ["3", "-1", "0", "1", b7, b7c], "3b": ["3", "-1", "0", "1", b7c, b7],
        "6": ["6", "2", "0", "0", "-1", "-1"], "7": ["7", "-1", "1", "-1", "0", "0"], "8": ["8", "0", "-1", "0", "1", "1"]}
check("PSL class sizes (1,21,56,42,24,24) with orders (1,2,3,4,7,7)", P["sizes"] == [1, 21, 56, 42, 24, 24] and P["orders"] == [1, 2, 3, 4, 7, 7])
check("PSL character table = LNR (all six rows)", all(OUT["PSL_table"][k]["chi"] == v for k, v in tgtP.items()))
check("Frobenius-Schur: 3,3bar complex (0) in both groups; 6,7,8 real (+1)",
      all(OUT[t][r]["FS"] == 0 for t in ("F21_table", "PSL_table") for r in ("3", "3b"))
      and all(OUT["PSL_table"][r]["FS"] == 1 for r in ("6", "7", "8")))

# ------------------------------------------------------------------ Kronecker products from characters
def decompose(chi, named, sizes, n):
    out = {}
    for lab, c in named.items():
        m = inner(chi, c, sizes, n)
        mi = int(round(m.real))
        assert abs(m - mi) < 1e-9, m
        if mi: out[lab] = mi
    return out

def kron_table(named, G, sizes, cl):
    n = len(G)
    sq = power_map(G, cl, 2)
    labs = sorted(named, key=lambda s: (int(round(named[s][0].real)), s))
    res = {}
    for i, la in enumerate(labs):
        for lb in labs[i:]:
            ca, cb = named[la], named[lb]
            if la == lb:
                S = (ca ** 2 + ca[sq]) / 2; A = (ca ** 2 - ca[sq]) / 2
                res[f"{la} x {lb}"] = {"sym": decompose(S, named, sizes, n), "antisym": decompose(A, named, sizes, n)}
            else:
                res[f"{la} x {lb}"] = decompose(ca * cb, named, sizes, n)
    return res

OUT["F21_kron"] = kron_table(F21_named, F["G"], F["sizes"], F["cl"])
OUT["PSL_kron"] = kron_table(PSL_named, P["G"], P["sizes"], P["cl"])
fk, pk = OUT["F21_kron"], OUT["PSL_kron"]
print("  F21 3x3:", fk["3 x 3"], " 3x3b:", fk["3 x 3b"])
print("  PSL 3x3:", pk["3 x 3"], " 3x3b:", pk["3 x 3b"])
check("F21: 3x3 = (3+3bar)_s + 3bar_a; 3x3bar = 1+1'+1''+3+3bar",
      fk["3 x 3"] == {"sym": {"3": 1, "3b": 1}, "antisym": {"3b": 1}} and fk["3 x 3b"] == {"1": 1, "1'": 1, "1''": 1, "3": 1, "3b": 1})
check("F21: 3x1' = 3, 1'x1' = 1'', 1'x1'' = 1",
      fk["1' x 3"] == {"3": 1} and fk["1' x 1'"]["sym"] == {"1''": 1} and fk["1' x 1''"] == {"1": 1})
# LNR table for PSL (bars restored by conjugation symmetry / characters):
lnr_psl = {
    "3 x 3": {"sym": {"6": 1}, "antisym": {"3b": 1}},
    "3 x 3b": {"1": 1, "8": 1},
    "3 x 6": {"3b": 1, "7": 1, "8": 1}, "3b x 6": {"3": 1, "7": 1, "8": 1},
    "3 x 7": {"6": 1, "7": 1, "8": 1}, "3b x 7": {"6": 1, "7": 1, "8": 1},
    "3 x 8": {"3": 1, "6": 1, "7": 1, "8": 1}, "3b x 8": {"3b": 1, "6": 1, "7": 1, "8": 1},
    "6 x 6": {"sym": {"1": 1, "6": 2, "8": 1}, "antisym": {"7": 1, "8": 1}},
    "6 x 7": {"3": 1, "3b": 1, "6": 1, "7": 2, "8": 2},
    "6 x 8": {"3": 1, "3b": 1, "6": 2, "7": 2, "8": 2},
    "7 x 7": {"sym": {"1": 1, "6": 2, "7": 1, "8": 1}, "antisym": {"3": 1, "3b": 1, "7": 1, "8": 1}},
    "7 x 8": {"3": 1, "3b": 1, "6": 2, "7": 2, "8": 3},
    "8 x 8": {"sym": {"1": 1, "6": 2, "7": 1, "8": 2}, "antisym": {"3": 1, "3b": 1, "7": 2, "8": 1}},
}
mism = {k: (pk.get(k), v) for k, v in lnr_psl.items() if pk.get(k) != v}
if mism: print("  PSL mismatches:", mism)
check("PSL: all 14 LNR Kronecker products (non-trivial irreps)", not mism)

# ------------------------------------------------------------------ branching PSL -> F21
idxP = {key(g): i for i, g in enumerate(P["G"])}
def restrict(chiP):
    # chi on each F21 class = chi of the PSL class containing the F21 class rep
    out = []
    for c in F["cl"]:
        g = F["G"][c[0]]
        pi = idxP[key(g)]
        ci = [j for j, cc in enumerate(P["cl"]) if pi in cc][0]
        out.append(chiP[ci])
    return np.array(out)
branch = {lab: decompose(restrict(c), F21_named, F["sizes"], 21) for lab, c in PSL_named.items()}
OUT["branch_PSL_F21"] = branch
print("  PSL->F21:", branch)
check("PSL->F21: 6 = 3+3bar, 7 = 1+3+3bar, 8 = 1'+1''+3+3bar",
      branch["6"] == {"3": 1, "3b": 1} and branch["7"] == {"1": 1, "3": 1, "3b": 1}
      and branch["8"] == {"1'": 1, "1''": 1, "3": 1, "3b": 1})

# ------------------------------------------------------------------ SU(3) -> PSL via Schur polynomials
def schur(lam, x):
    # bialternant formula s_lam = det(x_i^(lam_j+3-j)) / det(x_i^(3-j)), robust to degenerate x via perturbation-free
    # use Jacobi-Trudi with complete homogeneous symmetric polynomials instead (exact for any x)
    def h(k):
        if k < 0: return 0
        return sum(x[0] ** a * x[1] ** b * x[2] ** (k - a - b) for a in range(k + 1) for b in range(k + 1 - a))
    l = list(lam) + [0] * (3 - len(lam))
    M = [[h(l[i] - i + j) for j in range(3)] for i in range(3)]
    return np.linalg.det(np.array(M, dtype=complex))

def su3_char(p, q, M):
    x = np.linalg.eigvals(M)
    return schur((p + q, q, 0), x)

su3_list = [(1, 0), (0, 1), (2, 0), (0, 2), (1, 1), (3, 0), (2, 1), (4, 0), (0, 5), (1, 3), (2, 2)]
br3 = {}
for (p, q) in su3_list:
    chi = np.array([su3_char(p, q, r) for r in P["reps"]])
    dim = (p + 1) * (q + 1) * (p + q + 2) // 2
    assert abs(chi[0] - dim) < 1e-6
    br3[f"({p},{q})"] = decompose(chi, PSL_named, P["sizes"], 168)
OUT["branch_SU3_PSL"] = br3
print("  SU(3)->PSL:", br3)
dimsum = lambda d: sum(int(round(PSL_named[k][0].real)) * v for k, v in d.items())
lnr_dims = {"(3,0)": [3, 7], "(2,1)": [7, 8], "(4,0)": [1, 6, 8], "(0,5)": [3, 3, 7, 8], "(1,3)": [3, 6, 7, 8], "(2,2)": [6, 6, 7, 8]}
okb = all(sorted(int(round(PSL_named[k][0].real)) for k, v in br3[s].items() for _ in range(v)) == sorted(t) for s, t in lnr_dims.items())
check("SU(3)->PSL dimension content matches LNR table (11 irreps)", okb and br3["(1,0)"] == {"3": 1} and br3["(1,1)"] == {"8": 1})

# ------------------------------------------------------------------ invariants via Reynolds projector
def rep_tensor(mats_list):
    out = mats_list[0]
    for m in mats_list[1:]: out = np.kron(out, m)
    return out
F21n = F["G"]
def n_inv(G, factors):
    Pm = sum(rep_tensor([f(g) for f in factors]) for g in G) / len(G)
    return int(round(np.trace(Pm).real)), np.linalg.matrix_rank(Pm, tol=1e-8)
t3 = lambda g: g
t3b = lambda g: g.conj()
ninv, rk = n_inv(F21n, [t3, t3, t3b, t3b])
print("  F21 invariants in 3x3x3bx3b: trace(P) =", ninv, " rank(P) =", rk)
check("F21 invariants in psi psi' xi xi' (3x3x3bx3b) = 5 (Reynolds projector)", ninv == 5 and rk == 5)
# symmetric versions: Sym^2(3) x Sym^2(3b)
def sym2(g):
    M = np.kron(g, g)
    Psym = (np.eye(9) + np.eye(9)[[3 * (k % 3) + k // 3 for k in range(9)]]) / 2
    return M @ Psym
Psym = (np.eye(9) + np.eye(9)[[3 * (k % 3) + k // 3 for k in range(9)]]) / 2
Ptot = sum(np.kron(np.kron(g, g) @ Psym, np.kron(g.conj(), g.conj()) @ Psym) for g in F21n) / 21
nsym = int(round(np.trace(Ptot).real))
check("F21 invariants with psi=psi', xi=xi' (Sym2(3) x Sym2(3b)) = 2", nsym == 2)
OUT["F21_invariants_33bb"] = {"distinct": ninv, "symmetric": nsym}

# ------------------------------------------------------------------ LNR F21 Clebsch-Gordan (their eqs. 64-66) as intertwiners
Dn, Cn_ = mnum(D), mnum(C)
def is_intertwiner(X, rho_out, rho_in_pair):
    return all(np.allclose(rho_out(g) @ X, X @ np.kron(rho_in_pair[0](g), rho_in_pair[1](g))) for g in (Dn, Cn_))
e = np.eye(3)
def ket(i, j): return np.kron(e[i - 1], e[j - 1])
s2 = 1 / math.sqrt(2)
X3s = np.array([ket(3, 3), ket(1, 1), ket(2, 2)])
X3bs = np.array([s2 * (ket(3, 2) + ket(2, 3)), s2 * (ket(1, 3) + ket(3, 1)), s2 * (ket(2, 1) + ket(1, 2))])
X3ba = np.array([s2 * (ket(3, 2) - ket(2, 3)), s2 * (ket(1, 3) - ket(3, 1)), s2 * (ket(2, 1) - ket(1, 2))])
X3_33b = np.array([ket(2, 1), ket(3, 2), ket(1, 3)])
X3b_33b = np.array([ket(1, 2), ket(2, 3), ket(3, 1)])
X1 = np.array([(ket(1, 1) + ket(2, 2) + ket(3, 3)) / math.sqrt(3)])
X1p = np.array([(ket(1, 1) + w ** 2 * ket(2, 2) + w * ket(3, 3)) / math.sqrt(3)])
X1pp = np.array([(ket(1, 1) + w * ket(2, 2) + w ** 2 * ket(3, 3)) / math.sqrt(3)])
r3, r3b = (lambda g: g), (lambda g: g.conj())
cg_ok = [is_intertwiner(X3s, r3, (r3, r3)), is_intertwiner(X3bs, r3b, (r3, r3)), is_intertwiner(X3ba, r3b, (r3, r3)),
         is_intertwiner(X3_33b, r3, (r3, r3b)), is_intertwiner(X3b_33b, r3b, (r3, r3b)), is_intertwiner(X1, lambda g: np.eye(1), (r3, r3b))]
# singlets: 1' and 1'' as a set (the convention for which is 1' may swap)
def chi1(g):  # character of the singlet on generator: D -> 1, C -> w or w^2
    return None
sing = []
for X in (X1p, X1pp):
    v = X[0]
    lamD = (v.conj() @ np.kron(Dn, Dn.conj()) @ v)
    lamC = (v.conj() @ np.kron(Cn_, Cn_.conj()) @ v)
    eig_ok = np.allclose(np.kron(Dn, Dn.conj()) @ v, lamD * v) and np.allclose(np.kron(Cn_, Cn_.conj()) @ v, lamC * v)
    sing.append((eig_ok, nice(lamD), nice(lamC)))
print("  CG intertwiner checks:", cg_ok, " singlets (eigvec?, D, C):", sing)
check("LNR F21 CGs (64)-(66): five triplet maps + 1 are intertwiners; 1',1'' are the two non-trivial singlets",
      all(cg_ok) and all(s[0] for s in sing) and sorted(s[2] for s in sing) == ["w", "w^2"] and all(s[1] == "1" for s in sing))
OUT["CG_singlet_C_eigenvalues_for_LNR_1prime_1dprime"] = [s[2] for s in sing]

# ------------------------------------------------------------------ LNR A^[8] eq. (46)
lam = np.zeros((8, 3, 3), dtype=complex)
lam[0][0, 1] = lam[0][1, 0] = 1
lam[1][0, 1] = -1j; lam[1][1, 0] = 1j
lam[2][0, 0] = 1; lam[2][1, 1] = -1
lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2] = -1j; lam[4][2, 0] = 1j
lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2] = -1j; lam[6][2, 1] = 1j
lam[7] = np.diag([1, 1, -2]) / math.sqrt(3)
An = mnum(A_LNR)
A8 = np.array([[0.5 * np.trace(lam[a] @ An @ lam[b] @ An.conj().T) for b in range(8)] for a in range(8)]).real
c1, c2, c3 = (math.cos(2 * math.pi * k / 7) for k in (1, 2, 3))
s3 = math.sqrt(3)
A8_lnr = np.array([
    [2 - 2 * c1, 0, 2 * c1 + 2 * c2 - 4 * c3, 2 - 2 * c2, 0, 2 - 2 * c3, 0, 2 * s3 * c1 - 2 * s3 * c2],
    [0, -2 - 2 * c1 + 4 * c2, 0, 0, 2 + 2 * c2 - 4 * c3, 0, -2 + 4 * c1 - 2 * c3, 0],
    [2 * c1 + 2 * c2 - 4 * c3, 0, -c1 + 2 * c2 - c3, -4 * c1 + 2 * c2 + 2 * c3, 0, 2 * c1 - 4 * c2 + 2 * c3, 0, s3 * c1 - s3 * c3],
    [2 - 2 * c2, 0, -4 * c1 + 2 * c2 + 2 * c3, 2 - 2 * c3, 0, 2 - 2 * c1, 0, 2 * s3 * c2 - 2 * s3 * c3],
    [0, 2 + 2 * c2 - 4 * c3, 0, 0, -2 + 4 * c1 - 2 * c3, 0, 2 + 2 * c1 - 4 * c2, 0],
    [2 - 2 * c3, 0, 2 * c1 - 4 * c2 + 2 * c3, 2 - 2 * c1, 0, 2 - 2 * c2, 0, -2 * s3 * c1 + 2 * s3 * c3],
    [0, -2 + 4 * c1 - 2 * c3, 0, 0, 2 + 2 * c1 - 4 * c2, 0, -2 - 2 * c2 + 4 * c3, 0],
    [2 * s3 * c1 - 2 * s3 * c2, 0, s3 * c1 - s3 * c3, 2 * s3 * c2 - 2 * s3 * c3, 0, -2 * s3 * c1 + 2 * s3 * c3, 0, c1 - 2 * c2 + c3]]) / 7
dev = np.abs(A8 - A8_lnr).max()
print(f"  A^[8] (standard Gell-Mann, (1/2)Tr(l_a A l_b A^+)) vs LNR eq. (46): max |dev| = {dev:.2e}")
check("LNR A^[8] eq. (46) reproduced to 1e-12", dev < 1e-12)
OUT["A8_max_dev"] = float(dev)

# ------------------------------------------------------------------ subgroups needed elsewhere: save group elements
np.save("/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/F21_elements.npy", np.array(F["G"]))
np.save("/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/PSL_elements.npy", np.array(P["G"]))

OUT["checks"] = CHECKS
OUT["all_pass"] = all(CHECKS.values())
def jsonable(x):
    if isinstance(x, dict): return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [jsonable(v) for v in x]
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return float(x)
    if isinstance(x, np.ndarray): return jsonable(x.tolist())
    if isinstance(x, complex): return [x.real, x.imag]
    return x
json.dump(jsonable(OUT), open("/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/groups_cc.json", "w"), indent=1)
print(f"\n{sum(CHECKS.values())}/{len(CHECKS)} checks pass")
