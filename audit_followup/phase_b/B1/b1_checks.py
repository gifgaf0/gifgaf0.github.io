#!/usr/bin/env python3
"""B1 first leg: gauge paper v6.3 checks C1-C6 (pre-registration B1_PREREG.md, md5 5374289db16dcdd73f90875cc89b7ee3).

C1  color representation of each occupation sector of the three-mode Fock space (explicit Jordan-Wigner matrices)
C2  additivity of the paper's Y(N) = (-1)^(N+1) N/3
C3  Furey's options (ideal S^u/S^d, N or 3-N, sign) x mode color (3 or 3bar) against the paper's table
C4  the paper's Y with the induced colors, tested against the SM color-charge correlation
C5  PDG 2024 pulls for the sin and tan readings of 3/13
C6  automorphisms of the Csaszar triangulation and their action on the torus orientation
"""
import itertools, json, math
from fractions import Fraction as F
import numpy as np

out = {}
def show(*a):
    print(*a)

# ---------------------------------------------------------------- C1: Fock space and color sectors
I2, Z = np.eye(2), np.diag([1.0, -1.0])
a = np.array([[0.0, 1.0], [0.0, 0.0]])          # annihilator on one mode, basis (|0>, |1>)
def kron(*ms):
    r = np.array([[1.0]])
    for m in ms:
        r = np.kron(r, m)
    return r
alpha = [kron(a, I2, I2), kron(Z, a, I2), kron(Z, Z, a)]   # Jordan-Wigner
for i in range(3):
    for j in range(3):
        ac = alpha[i] @ alpha[j].conj().T + alpha[j].conj().T @ alpha[i]
        assert np.allclose(ac, np.eye(8) * (i == j))
        assert np.allclose(alpha[i] @ alpha[j] + alpha[j] @ alpha[i], 0)
Nop = sum(x.conj().T @ x for x in alpha)
Nvals = np.round(np.diag(Nop)).astype(int)
show("C1  occupation numbers on the 8 basis states:", [int(v) for v in Nvals])

lam = np.zeros((8, 3, 3), dtype=complex)             # Gell-Mann matrices
lam[0][0, 1] = lam[0][1, 0] = 1
lam[1][0, 1], lam[1][1, 0] = -1j, 1j
lam[2][0, 0], lam[2][1, 1] = 1, -1
lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2], lam[4][2, 0] = -1j, 1j
lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2], lam[6][2, 1] = -1j, 1j
lam[7] = np.diag([1, 1, -2]) / math.sqrt(3)

def generators(rho):
    """Second-quantized su(3) generators with the creation operators alpha_i^dagger in rep rho."""
    gens = []
    for A in lam:
        m = A / 2 if rho == "3" else -A.conj() / 2
        gens.append(sum(alpha[i].conj().T @ alpha[j] * m[i, j] for i in range(3) for j in range(3)))
    return gens

w3 = sorted([(0.5, 1 / (2 * math.sqrt(3))), (-0.5, 1 / (2 * math.sqrt(3))), (0.0, -1 / math.sqrt(3))])
w3b = sorted([(-x, -y) for x, y in w3])
def classify(weights):
    ws = sorted((round(x, 9), round(y, 9)) for x, y in weights)
    if len(ws) == 1 and abs(ws[0][0]) < 1e-9 and abs(ws[0][1]) < 1e-9:
        return "1"
    if np.allclose(ws, w3):
        return "3"
    if np.allclose(ws, w3b):
        return "3bar"
    return "?"

sector_colors = {}
for rho in ("3", "3bar"):
    T = generators(rho)
    C2 = sum(t @ t for t in T)
    for t in T:                      # closure check: generators commute with N
        assert np.allclose(t @ Nop - Nop @ t, 0)
    cols = {}
    for n in range(4):
        idx = [k for k in range(8) if Nvals[k] == n]
        wts = [(T[2][k, k].real, T[7][k, k].real) for k in idx]
        assert np.allclose([T[2][k, l] for k in idx for l in idx if k != l], 0)
        cas = sorted(set(float(v) for v in np.round(np.diag(C2)[idx].real, 9)))
        cols[n] = classify(wts)
        show(f"C1  modes in {rho:4s}: N={n}  dim={len(idx)}  color={cols[n]:4s}  C2={cas}")
    sector_colors[rho] = cols
out["C1_sector_colors"] = sector_colors
out["C1_conjugate_N1_N2"] = all(
    {sector_colors[r][1], sector_colors[r][2]} == {"3", "3bar"} for r in ("3", "3bar"))
show("C1  N=1 and N=2 sectors conjugate for both mode reps:", out["C1_conjugate_N1_N2"])

# ---------------------------------------------------------------- C2: additivity
Ypaper = {n: F((-1) ** (n + 1) * n, 3) for n in range(4)}
show("C2  paper's Y(N):", {n: str(v) for n, v in Ypaper.items()})
aa, bb = Ypaper[0], Ypaper[1] - Ypaper[0]
resid = {n: Ypaper[n] - (aa + bb * n) for n in range(4)}
additive = all(r == 0 for r in resid.values())
show(f"C2  best affine through N=0,1: a={aa}, b={bb}; residuals {dict((n, str(r)) for n, r in resid.items())}; additive: {additive}")
# no affine function at all: the second difference must vanish for an affine sequence
second_diffs = [Ypaper[n + 2] - 2 * Ypaper[n + 1] + Ypaper[n] for n in range(2)]
show("C2  second differences (zero for any a + bN):", [str(x) for x in second_diffs])
out["C2_additive"] = additive
out["C2_second_differences"] = [str(x) for x in second_diffs]

# ---------------------------------------------------------------- correlation rule
def passes(color, y):
    frac = y - math.floor(y)
    want = {"1": F(0), "3": F(2, 3), "3bar": F(1, 3)}[color]
    return frac == want

# ---------------------------------------------------------------- C3: Furey's options
paper_table = {0: ("1", F(0)), 1: ("3bar", F(1, 3)), 2: ("3bar", F(-2, 3)), 3: ("1", F(1))}
options = {"N/3": lambda n: F(n, 3), "-N/3": lambda n: F(-n, 3),
           "(3-N)/3": lambda n: F(3 - n, 3), "-(3-N)/3": lambda n: F(n - 3, 3)}
c3 = []
for qname, q in options.items():
    for rho in ("3", "3bar"):
        table = {n: (sector_colors[rho][n], q(n)) for n in range(4)}
        same_values = all(q(n) == Ypaper[n] for n in range(4))
        same_table = all(table[n] == paper_table[n] for n in range(4))
        ok = all(passes(*table[n]) for n in range(4))
        c3.append({"q": qname, "rho": rho, "table": {n: [c, str(y)] for n, (c, y) in table.items()},
                   "reproduces_paper_Y": same_values, "reproduces_paper_table": same_table,
                   "passes_correlation": ok})
        show(f"C3  q={qname:9s} rho={rho:4s} table={[(c, str(y)) for c, y in table.values()]}  "
             f"paper Y? {same_values}  paper table? {same_table}  SM-consistent? {ok}")
out["C3_options"] = c3
out["C3_any_reproduces_Y"] = any(o["reproduces_paper_Y"] for o in c3)
out["C3_any_reproduces_table"] = any(o["reproduces_paper_table"] for o in c3)
out["C3_all_options_SM_consistent"] = all(o["passes_correlation"] for o in c3)

# the paper's own label table cannot occur: both quark sectors 3bar is impossible
out["C3_paper_labels_possible"] = any(
    sector_colors[r][1] == "3bar" and sector_colors[r][2] == "3bar" for r in ("3", "3bar"))
show("C3  paper's labels (N=1 and N=2 both 3bar) realizable by an induced action:", out["C3_paper_labels_possible"])

# ---------------------------------------------------------------- C4: paper's Y with induced colors
c4 = {}
for rho in ("3", "3bar"):
    pairs = {n: (sector_colors[rho][n], Ypaper[n]) for n in range(4)}
    c4[rho] = {n: [c, str(y), passes(c, y)] for n, (c, y) in pairs.items()}
    show(f"C4  rho={rho:4s}: " + ", ".join(f"N={n}:({c},{y}) {'pass' if p else 'FAIL'}" for n, (c, y, p) in c4[rho].items()))
out["C4"] = c4
out["C4_fails_both"] = all(any(not v[2] for v in c4[r].values()) for r in c4)

# ---------------------------------------------------------------- DR-B1-1 verdict
if out["C3_any_reproduces_table"]:
    v1 = "R"
elif out["C2_additive"] and not out["C4_fails_both"]:
    v1 = "N-C"
else:
    v1 = "N-I"
out["DR_B1_1"] = v1
show("DR-B1-1 verdict:", v1)

# ---------------------------------------------------------------- C5: pulls
x = 3 / 13
Vud, sVud = 0.97367, 0.00032
Vus, sVus = 0.22431, 0.00085
VusK, sVusK = 0.2250, 0.0004
lam_, slam = 0.22501, 0.00068
r_direct = Vus / Vud
s_direct = r_direct * math.hypot(sVus / Vus, sVud / Vud)
r_K = VusK / Vud
s_K = r_K * math.hypot(sVusK / VusK, sVud / Vud)
t_fit = lam_ / math.sqrt(1 - lam_ ** 2)
s_tfit = slam * (1 - lam_ ** 2) ** -1.5
pulls = {
    "sin_vs_Vus_direct": (x - Vus) / sVus,
    "sin_vs_lambda_fit": (x - lam_) / slam,
    "tan_vs_Vus_over_Vud_direct": (x - r_direct) / s_direct,
    "tan_vs_Kmu2_over_Vud": (x - r_K) / s_K,
    "tan_vs_fit": (x - t_fit) / s_tfit,
}
show(f"C5  3/13 = {x:.6f}; tan inputs: direct {r_direct:.6f}±{s_direct:.6f}, Kmu2 {r_K:.6f}±{s_K:.6f}, fit {t_fit:.6f}±{s_tfit:.6f}")
for k, v in pulls.items():
    show(f"C5  pull {k:28s} {v:+.3f} sigma")
out["C5_pulls"] = {k: round(v, 4) for k, v in pulls.items()}
out["C5_tan_values"] = {"direct": [round(r_direct, 6), round(s_direct, 6)], "Kmu2": [round(r_K, 6), round(s_K, 6)],
                        "fit": [round(t_fit, 6), round(s_tfit, 6)]}
out["C5_rel_dev_sin"] = {"direct_pct": round(100 * (x - Vus) / Vus, 3), "fit_pct": round(100 * (x - lam_) / lam_, 3)}
sin_excluded = abs(pulls["sin_vs_Vus_direct"]) > 3 and abs(pulls["sin_vs_lambda_fit"]) > 3
out["DR_B1_2_sin_excluded"] = sin_excluded
show("DR-B1-2 sin reading excluded (|z|>3 against both):", sin_excluded,
     f"| relative deviations {out['C5_rel_dev_sin']}")

# ---------------------------------------------------------------- C6: Csaszar triangulation
plus = [tuple(sorted(((i) % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)]
minus = [tuple(sorted(((i) % 7, (i + 2) % 7, (i + 3) % 7))) for i in range(7)]
faces = plus + minus
assert len(set(faces)) == 14
def is_fano(lines):
    pairs = [frozenset(p) for L in lines for p in itertools.combinations(L, 2)]
    return len(lines) == 7 and len(set(pairs)) == 21
assert is_fano(plus) and is_fano(minus) and not set(plus) & set(minus)
edge_count = {}
for f in faces:
    for p in itertools.combinations(f, 2):
        edge_count[p] = edge_count.get(p, 0) + 1
assert len(edge_count) == 21 and set(edge_count.values()) == {2}

# coherent orientation by propagation
def edges_of(o):
    return [(o[0], o[1]), (o[1], o[2]), (o[2], o[0])]
oriented = {plus[0]: plus[0]}
queue = [plus[0]]
while queue:
    f = queue.pop()
    for (u, v) in edges_of(oriented[f]):
        for g in faces:
            if g != f and u in g and v in g:
                w = [t for t in g if t not in (u, v)][0]
                og = (v, u, w)                      # neighbour traverses the shared edge in the opposite direction
                if g in oriented:
                    assert set(edges_of(oriented[g])) == set(edges_of(og)), "non-orientable"
                else:
                    oriented[g] = og
                    queue.append(g)
assert len(oriented) == 14
oriented_edges = set(e for f in oriented.values() for e in edges_of(f))
assert len(oriented_edges) == 42                    # every edge used once in each direction

# vertex links are 6-cycles (closed surface), Euler characteristic 0
for v in range(7):
    link = [tuple(t for t in f if t != v) for f in faces if v in f]
    adj = {}
    for (p, q) in link:
        adj.setdefault(p, []).append(q); adj.setdefault(q, []).append(p)
    assert all(len(n) == 2 for n in adj.values()) and len(adj) == 6
    seen, cur, prev = [link[0][0]], link[0][0], None
    while True:
        nxt = [t for t in adj[cur] if t != prev][0] if prev is not None else adj[cur][0]
        if nxt == seen[0]:
            break
        seen.append(nxt); prev, cur = cur, nxt
    assert len(seen) == 6
chi = 7 - 21 + 14

face_set = set(faces)
auts, preserving, reversing = [], 0, 0
for perm in itertools.permutations(range(7)):
    img = set(tuple(sorted(perm[t] for t in f)) for f in faces)
    if img != face_set:
        continue
    auts.append(perm)
    imgs = set(e for f in oriented.values() for e in edges_of(tuple(perm[t] for t in f)))
    if imgs == oriented_edges:
        preserving += 1
    else:
        rev = set((b, a_) for (a_, b) in oriented_edges)
        assert imgs == rev
        reversing += 1
agl = set(tuple((a_ * x_ + b) % 7 for x_ in range(7)) for a_ in range(1, 7) for b in range(7))
f21 = set(tuple((a_ * x_ + b) % 7 for x_ in range(7)) for a_ in (1, 2, 4) for b in range(7))
keeps_plus = [p for p in auts if set(tuple(sorted(p[t] for t in L)) for L in plus) == set(plus)]
stab_plus = [p for p in itertools.permutations(range(7))
             if set(tuple(sorted(p[t] for t in L)) for L in plus) == set(plus)]
show(f"C6  faces: two line-disjoint Fano planes; each edge in 2 faces; vertex links 6-cycles; chi={chi}; orientable")
show(f"C6  |Aut(face set)| = {len(auts)}; equals AGL(1,7): {set(auts) == agl}; orientation-preserving {preserving}, reversing {reversing}")
show(f"C6  automorphisms keeping Fano+ : {len(keeps_plus)} (= F21: {set(keeps_plus) == f21}); |Stab_S7(Fano+)| = {len(stab_plus)}; "
     f"Stab(Fano+) ∩ Aut(faces) = {len(set(stab_plus) & set(auts))}")
# Fano planes line-disjoint from Fano+ (information only)
all_fano = set()
for perm in itertools.permutations(range(7)):
    all_fano.add(frozenset(tuple(sorted(perm[t] for t in L)) for L in plus))
disjoint = [P for P in all_fano if not (set(P) & set(plus))]
show(f"C6  Fano planes on 7 labelled points: {len(all_fano)}; line-disjoint from Fano+: {len(disjoint)}; Fano- among them: {frozenset(minus) in disjoint}")
fac, n = [], len(auts)
for p in range(2, n + 1):
    while n % p == 0:
        fac.append(p); n //= p
show(f"C6  |AGL(1,7)| factorisation {fac}; squarefree: {len(set(fac)) == len(fac)} (all Sylow subgroups cyclic, Schur multiplier trivial)")
out["C6"] = {"aut_order": len(auts), "equals_AGL17": set(auts) == agl, "orientation_preserving": preserving,
             "orientation_reversing": reversing, "keeps_each_Fano_plane": len(keeps_plus), "keeps_plane_is_F21": set(keeps_plus) == f21,
             "stab_S7_FanoPlus": len(stab_plus), "stab_cap_aut": len(set(stab_plus) & set(auts)), "chi": chi,
             "fano_planes_total": len(all_fano), "fano_planes_line_disjoint_from_plus": len(disjoint),
             "order_factorisation": fac, "squarefree": len(set(fac)) == len(fac)}
show("DR-B1-3 every automorphism orientation-preserving:", reversing == 0)

with open("b1_results.json", "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
show("wrote b1_results.json")
