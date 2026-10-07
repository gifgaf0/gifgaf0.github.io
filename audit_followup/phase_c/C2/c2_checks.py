#!/usr/bin/env python3
"""C2 checks run in this session (C2_PREREG.md): the second computation for P4 (μ_n) and independent spot-checks of the
decisive facts behind the M-rev items, plus the arithmetic for P1 and P2. Written without reading the math_A / math_B code.

P4  quark-model moments from explicit three-quark spin⊗flavour states (sympy, exact)
c   SL(2,7): element orders; is u conjugate to u³; s = diag(3,5) vs t = diag(4,2)
a   clean sedenion zero divisors at n = 2, 4, 6 terms (exact rank), and the e₈-cancelling zero product
d   size-2 matchings of K₇,₇ minus a perfect matching
h   the flag stabiliser in GL(3,2) (order, abelian?, involutions)
P1  DES: b = 1.003 ± 0.005 (stat) ± 0.010 (sys) against b = 0
P2  cells per grain at the EM-side window edge
"""
import contextlib, io, itertools, json, math, os, sys
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}

# ---------------------------------------------------------------- P4: SU(6) moments
mu_u, mu_d = sp.symbols("mu_u mu_d")
# basis: each quark = (flavour f in {u,d}, spin s in {+1,-1}); a state = dict over 3-tuples of (f, s)
singles = [(f, s) for f in "ud" for s in (1, -1)]
basis = list(itertools.product(singles, repeat=3))
idx = {b: i for i, b in enumerate(basis)}


def symmetrize(vec):
    v = sp.zeros(64, 1)
    for b, i in idx.items():
        if vec[i] != 0:
            for perm in itertools.permutations(range(3)):
                v[idx[tuple(b[p] for p in perm)]] += vec[i]
    return v


def ket(*q):
    v = sp.zeros(64, 1)
    v[idx[tuple(q)]] = 1
    return v


def moment(v):
    num = sum(v[i] ** 2 * sum((mu_u if f == "u" else mu_d) * s for (f, s) in b) for b, i in idx.items())
    den = sum(v[i] ** 2 for i in range(64))
    return sp.simplify(num / den)


# spin-½ M=½ states built as (two-quark spin-1 ⊗ spin-½) with CG weights, then symmetrized over positions:
# |½,½⟩ = √(2/3)|1,1⟩|↓⟩ − √(1/3)|1,0⟩|↑⟩ for the uu pair (flavour-symmetric) ⊗ d — the textbook construction,
# here built directly and checked by its spin and symmetry rather than assumed
s3 = sp.sqrt(3)
def nucleon(f1, f2, f3):
    v = (sp.sqrt(2) / s3) * ket((f1, 1), (f2, 1), (f3, -1)) \
        - (1 / s3) * (1 / sp.sqrt(2)) * (ket((f1, 1), (f2, -1), (f3, 1)) + ket((f1, -1), (f2, 1), (f3, 1)))
    return symmetrize(v)

p_state, n_state = nucleon("u", "u", "d"), nucleon("d", "d", "u")
# check total spin ½ via S² = Σ_i<j 2 S_i·S_j + 9/4: use S_z = ½ and S_+ annihilation check on the symmetrized state
def s_plus(v):
    w = sp.zeros(64, 1)
    for b, i in idx.items():
        if v[i] != 0:
            for k in range(3):
                if b[k][1] == -1:
                    nb = list(b); nb[k] = (b[k][0], 1)
                    w[idx[tuple(nb)]] += v[i]
    return w
out["P4"] = {"mu_p": str(moment(p_state)), "mu_n": str(moment(n_state)),
             "p_is_highest_weight_spin_half": all(x == 0 for x in s_plus(p_state)),
             "mu_Delta": {}}
for name, fl in (("Delta++", "uuu"), ("Delta+", "uud"), ("Delta0", "udd"), ("Delta-", "ddd")):
    out["P4"]["mu_Delta"][name] = str(moment(symmetrize(ket((fl[0], 1), (fl[1], 1), (fl[2], 1)))))
den = sum(p_state[i] ** 2 for i in range(64))
out["P4"]["proton_sum_sigma_z_u"] = str(sp.simplify(sum(p_state[i] ** 2 * sum(s for (f, s) in b if f == "u")
                                                     for b, i in idx.items()) / den))
out["P4"]["proton_sigma_z_d"] = str(sp.simplify(sum(p_state[i] ** 2 * sum(s for (f, s) in b if f == "d")
                                                 for b, i in idx.items()) / den))
D0 = sp.sympify(out["P4"]["mu_Delta"]["Delta0"]).subs(mu_u, -2 * mu_d)
out["P4"]["mu_Delta0_at_mu_u_eq_-2mu_d"] = str(sp.simplify(D0))
out["P4"]["mu_p_over_mu_n_at_mu_u_eq_-2mu_d"] = str(sp.simplify(
    (sp.sympify(out["P4"]["mu_p"]) / sp.sympify(out["P4"]["mu_n"])).subs(mu_u, -2 * mu_d)))

# ---------------------------------------------------------------- c: SL(2,7)
P = 7
def mul(A, B):
    return ((A[0]*B[0] + A[1]*B[2]) % P, (A[0]*B[1] + A[1]*B[3]) % P, (A[2]*B[0] + A[3]*B[2]) % P, (A[2]*B[1] + A[3]*B[3]) % P)
G = [(a, b, c, d) for a in range(P) for b in range(P) for c in range(P) for d in range(P) if (a*d - b*c) % P == 1]
I = (1, 0, 0, 1)
def order(g):
    k, h = 1, g
    while h != I:
        h, k = mul(h, g), k + 1
    return k
def inv(g):
    a, b, c, d = g
    return (d % P, (-b) % P, (-c) % P, a % P)
orders = {}
for g in G:
    orders[order(g)] = orders.get(order(g), 0) + 1
u = (1, 1, 0, 1)
def upow(k):
    return (1, k % P, 0, 1)
conj_to = {k: sum(1 for g in G if mul(mul(g, u), inv(g)) == upow(k)) for k in range(1, 7)}
s_m, t_m = (3, 0, 0, 5), (4, 0, 0, 2)
out["c"] = {"|SL(2,7)|": len(G), "element_orders": dict(sorted(orders.items())), "has_order_24": 24 in orders,
            "number_of_g_with_g_u_ginv_eq_u^k": conj_to, "s_equals_minus_t": s_m == tuple((-x) % P for x in t_m),
            "s_u_sinv": mul(mul(s_m, u), inv(s_m)), "u2": upow(2), "u3": upow(3)}

# ---------------------------------------------------------------- a: clean sedenion zero divisors
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
with contextlib.redirect_stdout(io.StringIO()):
    from sedenion_Fp import MULT                   # noqa: E402
LB = np.zeros((16, 16, 16), dtype=np.int64)        # LB[a] = left-multiplication matrix of e_a
for a in range(16):
    for c in range(16):
        for (k, sg) in MULT[a][c]:
            LB[a][k][c] += sg
def lmat(x):
    return np.tensordot(np.array(x, dtype=np.int64), LB, axes=1)
counts = {}
for n in (2, 4, 6):
    zd = 0
    for S in itertools.combinations(range(1, 16), n):
        for signs in itertools.product((1, -1), repeat=n - 1):
            x = [0] * 16
            x[S[0]] = 1
            for i, sg in zip(S[1:], signs):
                x[i] = sg
            if np.linalg.matrix_rank(lmat(x).astype(float)) < 16:
                zd += 1
    counts[n] = zd
def smul(x, y):
    r = [0] * 16
    for a in range(16):
        if x[a]:
            for c in range(16):
                if y[c]:
                    for (k, sg) in MULT[a][c]:
                        r[k] += sg * x[a] * y[c]
    return r
x = [0] * 16; x[1] = x[2] = x[11] = x[12] = 1
y = [0] * 16; y[3], y[4], y[13], y[14] = 1, -1, 1, -1
partial_e8 = [MULT[a][c] for a in (1, 2, 11, 12) for c in (3, 4, 13, 14) if any(k == 8 for (k, _) in MULT[a][c])]
out["a"] = {"clean_ZD_counts_n2_n4_n6": counts, "example_product_is_zero": all(v == 0 for v in smul(x, y)),
            "example_has_e8_terms": len(partial_e8)}

# ---------------------------------------------------------------- d: size-2 matchings of K7,7 − M
edges = [(a, b) for a in range(7) for b in range(7) if a != b]
out["d"] = {"edges": len(edges),
            "size2_matchings": sum(1 for e, f in itertools.combinations(edges, 2) if e[0] != f[0] and e[1] != f[1])}

# ---------------------------------------------------------------- h: flag stabiliser in GL(3,2)
mats = [m for m in itertools.product((0, 1), repeat=9)
        if round(abs(np.linalg.det(np.array(m).reshape(3, 3)))) % 2 == 1]
def mv(m, v):
    M = np.array(m).reshape(3, 3)
    return tuple(int(x) % 2 for x in M.dot(np.array(v)))
p0 = (1, 0, 0)
line0 = {(1, 0, 0), (0, 1, 0), (1, 1, 0)}                       # the line z = 0 contains p0
stab = [m for m in mats if mv(m, p0) == p0 and {mv(m, v) for v in line0} == line0]
def mm(a, b):
    return tuple(int(x) % 2 for x in (np.array(a).reshape(3, 3).dot(np.array(b).reshape(3, 3))).flatten())
inv2 = sum(1 for m in stab if mm(m, m) == (1, 0, 0, 0, 1, 0, 0, 0, 1) and m != (1, 0, 0, 0, 1, 0, 0, 0, 1))
abelian = all(mm(a, b) == mm(b, a) for a in stab for b in stab)
out["h"] = {"|GL(3,2)|": len(mats), "flag_stabiliser_order": len(stab), "abelian": abelian, "involutions": inv2,
            "type": "D4" if (len(stab) == 8 and not abelian and inv2 == 5) else "?"}

# ---------------------------------------------------------------- P1, P2 arithmetic
b, sb = 1.003, math.hypot(0.005, 0.010)
out["P1"] = {"b": b, "sigma_combined": round(sb, 4), "sigma_from_b_eq_0": round(b / sb, 1)}
edge, a_lo, a_hi = 3.7641664288e-33, 1.899e-34, 7.588e-34
out["P2"] = {"cells_per_grain_max": [round(edge / a_hi, 2), round(edge / a_lo, 2)],
             "floor_20_cells_empties_window": 20 * a_lo > edge, "floor_10_cells_survives_only_below": edge / 10}

json.dump(out, open(os.path.join(HERE, "c2_checks.json"), "w"), indent=1, default=str)
for k, v in out.items():
    print(k, v)
