"""
xc_e0.py -- independent cross-check of experiment E0 (SEED.md section 3).

Written from PLAN.md, SEED.md, hexagon_check.py, the E0 report and its
results.json only; the original E0 scripts were not read before this was run.

Methods (chosen to differ from the original's BFS closure of exact matrices
over a 6-dim basis of Q(zeta7)):
  * group orders: Todd-Coxeter on a presentation (upper bound) + exact relation
    checks in Q[Z7]/(1+..+x^6); Schreier-Sims on permutation representations
    obtained by reducing mod p = 29 and p = 43 (independent second count);
  * classes, characters, Frobenius-Schur indicators: classes in the mod-p
    permutation image, traces of class representatives evaluated exactly;
  * maximality: primitivity (2-transitivity) of the action on cosets, plus the
    full subgroup lattice in the faithful degree-8 action;
  * lattices, Weyl and affine Weyl groups: integer 2x2 matrices in the basis
    b1 = (1,-1,0), b2 = (0,1,-1) of Lambda, rational affine maps;
  * triangulation / Fano: integer combinatorics, exhaustive backtracking;
  * octonions: Der(O) in the Fano-table (Cayley-Graves) model; the C + C^3
    model checked symbolically with sympy.
Run:  NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 xc_e0.py
Writes crosscheck.json and xc_replica_lines.txt next to this file.  Exit 0 iff all checks pass.
"""
import itertools
import json
import os
import sys
import time
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xc_lib import (Z7, ZERO, ONE, z, G, I_OVER_SQRT7, B7, mat, mmul, mscale, mconj, mdagger,
                    mdet, mtrace, ID3, meq, mpow, in_SU3, mmodp, prim7, fmul, perm_rep,
                    perm_of_matrix, pmul, pinv, pid, pcomp, porder, BSGS, bfs_elements, conj_classes,
                    closure, todd_coxeter, word_letters, Q5)

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()
CHECKS = []
VALUES = {}


def check(section, name, ok, detail=""):
    CHECKS.append({"section": section, "name": name, "ok": bool(ok), "detail": str(detail)})
    print(f"[{'PASS' if ok else 'FAIL'}] {section}: {name}" + (f"  -- {detail}" if detail else ""))
    sys.stdout.flush()


def fmtz(x):
    """pretty-print a Z7 element that is rational or +-b7, b7bar."""
    if x.is_rational():
        v = x.rational_value()
        return str(v)
    for name, val in (("b7", B7), ("b7bar", B7.conj()), ("-b7", -B7), ("-b7bar", -B7.conj())):
        if x == val:
            return name
    return repr(x)


# ==========================================================================
# A. the field
# ==========================================================================
check("A", "G^2 = -7 exactly (G = quadratic Gauss sum)", G * G == Z7.const(-7))
gc = G.to_complex()
check("A", "numerically G = +i sqrt7 (fixes the sign convention i/sqrt7 = G/7)",
      abs(gc - 2.6457513110645906j) < 1e-12, f"G ~ {gc:.12f}")
check("A", "b7 = z+z^2+z^4 satisfies 2 b7 + 1 = G, i.e. b7 = (-1 + i sqrt7)/2", B7 * 2 + 1 == G)
check("A", "b7 is not real: b7 - conj(b7) = G != 0", (B7 - B7.conj()) == G)

# ==========================================================================
# B. torus, lattices, weights (integer arithmetic in the basis b1, b2 of Lambda)
# ==========================================================================
GRAM = ((2, -1), (-1, 2))       # Gram matrix of b1=(1,-1,0), b2=(0,1,-1)


def to_c(v):                      # plane vector (sum 0) -> coordinates in b1, b2
    assert sum(v) == 0
    return (v[0], -v[2])


def from_c(c):
    return (c[0], c[1] - c[0], -c[1])


def dot3(a, b):
    return sum(x * y for x, y in zip(a, b))


b1, b2 = (1, -1, 0), (0, 1, -1)
check("B", "Gram(b1,b2) = [[2,-1],[-1,2]]: equal lengths at 120 deg, hexagonal",
      [[dot3(b1, b1), dot3(b1, b2)], [dot3(b2, b1), dot3(b2, b2)]] == [[2, -1], [-1, 2]])
ok = all(from_c(to_c(v)) == v for v in itertools.product(range(-3, 4), repeat=3) if sum(v) == 0)
check("B", "every integer vector with zero sum is c1 b1 + c2 b2 with c1 = v1, c2 = -v3 integers (Lambda = Z^3 ∩ plane)", ok)
w1 = (Fr(2, 3), Fr(-1, 3), Fr(-1, 3))
w2 = (Fr(1, 3), Fr(1, 3), Fr(-2, 3))
check("B", "fundamental weights w1, w2 dual to b1, b2 and Gram (1/3)[[2,1],[1,2]] (60 deg): hexagonal weight lattice",
      [dot3(w1, b1), dot3(w1, b2), dot3(w2, b1), dot3(w2, b2)] == [1, 0, 0, 1]
      and [dot3(w1, w1), dot3(w1, w2), dot3(w2, w2)] == [Fr(2, 3), Fr(1, 3), Fr(2, 3)])
# octet = roots (6) + zero weight (mult 2)
roots = [tuple((1 if k == i else 0) - (1 if k == j else 0) for k in range(3))
         for i in range(3) for j in range(3) if i != j]
angles_ok = all(dot3(r, r) == 2 for r in roots) and all(
    sorted(dot3(r, s) for s in roots if s != r) == [-2, -1, -1, 1, 1] for r in roots)
check("B", "octet: 6 nonzero weights (roots) of equal length, each with 2 neighbours at 60 deg, 2 at 120 deg, 1 opposite (regular hexagon) + zero weight twice (rank 2)", angles_ok)
mu = [tuple(Fr(int(k == i)) - Fr(1, 3) for k in range(3)) for i in range(3)]
dec = {}
for trip in itertools.combinations_with_replacement(range(3), 3):
    wgt = tuple(sum(mu[i][k] for i in trip) for k in range(3))
    dec[wgt] = dec.get(wgt, 0) + 1
corners = [tuple(3 * x for x in mu[i]) for i in range(3)]


def on_segment(P, A, B):
    # P on segment AB (exact): P - A = t (B - A) with 0 <= t <= 1
    d = [b - a for a, b in zip(A, B)]
    e = [p - a for a, p in zip(A, P)]
    k = next(i for i in range(3) if d[i] != 0)
    t = e[k] / d[k]
    return all(e[i] == t * d[i] for i in range(3)) and 0 <= t <= 1


sides = [sum(on_segment(P, corners[i], corners[(i + 1) % 3]) for P in dec) for i in range(3)]
check("B", "decuplet Sym^3(3): 10 distinct weights of multiplicity 1, triangle with corners 3 mu_i and 4 weights on each side",
      len(dec) == 10 and set(dec.values()) == {1} and sides == [4, 4, 4], f"sides {sides}")

# seven points: 7p = (1,2,-3) -> coords (1,3); label: q ~ k p mod Lambda
P7 = to_c((1, 2, -3))           # = (1, 3)


def label7(c7):
    """c7 = 7 * (point in Lambda coordinates), integers; return k with c7 = k*P7 mod 7, else None."""
    for k in range(7):
        if (c7[0] - k * P7[0]) % 7 == 0 and (c7[1] - k * P7[1]) % 7 == 0:
            return k
    return None


check("B", "the seven points D^j <-> j p are distinct mod Lambda and 7p in Lambda",
      len({((j * P7[0]) % 7, (j * P7[1]) % 7) for j in range(7)}) == 7)


def imat_apply(M, c):
    return (M[0][0] * c[0] + M[0][1] * c[1], M[1][0] * c[0] + M[1][1] * c[1])


def imat_of_linear(f):
    """2x2 integer matrix (columns = images of b1, b2) of a linear map f on the plane (3-vectors)."""
    c1, c2 = to_c(f(b1)), to_c(f(b2))
    return ((c1[0], c2[0]), (c1[1], c2[1]))


roll = lambda v: (v[2], v[0], v[1])          # hexagon_check's turn = np.roll(v, 1)
TURN = imat_of_linear(roll)
lab_turn = label7(imat_apply(TURN, P7))
check("B", "120 deg turn theta -> roll(theta) sends point 1 to point 4 (x -> 4x)", lab_turn == 4, f"label {lab_turn}")

# finer lattice L' = Lambda + Z p ; work with 7L' = 7 Z^2 + Z (1,3) in Lambda coordinates


def gram7(c, d):                 # inner product of (c/7), (d/7) in true units, as Fraction
    return Fr(c[0] * (2 * d[0] - d[1]) + c[1] * (-d[0] + 2 * d[1]), 49)


Lp = {(k * P7[0] + 7 * a, k * P7[1] + 7 * b) for k in range(7) for a in range(-3, 4) for b in range(-3, 4)}
norms = {}
for v in Lp:
    if v != (0, 0):
        norms.setdefault(gram7(v, v), []).append(v)
nmin = min(norms)
shortest = norms[nmin]
check("B", "finer lattice Lambda + Z p: minimal norm^2 2/7 attained by exactly 6 vectors",
      nmin == Fr(2, 7) and len(shortest) == 6, f"min norm^2 {nmin}, count {len(shortest)}")
# reduced basis: two shortest vectors at 60 deg
s0 = shortest[0]
s1 = next(s for s in shortest if gram7(s0, s) == Fr(1, 7))
idx = abs(Fr(s0[0] * s1[1] - s0[1] * s1[0], 49))
check("B", "Gram of two shortest vectors at 60 deg = (1/7)[[2,1],[1,2]] (~ (1/7)[[2,-1],[-1,2]]), they span L', index [L':Lambda] = 7",
      gram7(s0, s0) == Fr(2, 7) and gram7(s1, s1) == Fr(2, 7) and idx == Fr(1, 7),
      f"covolume ratio {idx}")
labels6 = sorted(label7(s) for s in shortest)
check("B", "the six neighbours of point 0 carry labels 1..6 (K7)", labels6 == [1, 2, 3, 4, 5, 6], labels6)
VALUES["finer_lattice"] = {"min_norm2": str(nmin), "n_shortest": len(shortest), "index": 7}


def det2(a, b):
    return a[0] * b[1] - a[1] * b[0]


# oriented: orientation of (b1, b2) equals that of (u, w) = (b1, b1 + 2 b2), det = 2 > 0
# a triangle {x, x+s, x+s'} with s' = s rotated by +60 deg (det(s,s')>0, s.s' = |s|^2/2)
pairs60 = [(s, t) for s in shortest for t in shortest if gram7(s, t) == Fr(1, 7) and det2(s, t) > 0]
assert len(pairs60) == 6
# group the 6 oriented pairs into two classes: {s, R120 s, R240 s} (up) and the rest (down)
R120 = TURN
a0 = pairs60[0][0]
upset = {a0, imat_apply(R120, a0), imat_apply(R120, imat_apply(R120, a0))}
up, down = set(), set()
up_or, down_or = [], []
for s, t in pairs60:
    ls, lt = label7(s), label7(t)
    fam, fam_or = (up, up_or) if s in upset else (down, down_or)
    for x in range(7):
        tri = (x, (x + ls) % 7, (x + lt) % 7)
        fam.add(tuple(sorted(tri)))
        fam_or.append(tri)


def is_fano(S):
    prs = [pr for tri in S for pr in itertools.combinations(tri, 2)]
    return len(S) == 7 and len(prs) == len(set(prs)) == 21


check("B", "14 distinct triangles, two families of 7 (classified by orientation class of the 60-deg step pair)",
      len(up) == 7 and len(down) == 7 and not (up & down), f"family1 {sorted(up)}; family2 {sorted(down)}")
check("B", "both families are Fano planes", is_fano(up) and is_fano(down))
octo = {tuple(sorted(((i) % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)}
other = {tuple(sorted(((i) % 7, (i + 2) % 7, (i + 3) % 7))) for i in range(7)}
octo_fam = "family2" if down == octo else ("family1" if up == octo else None)
check("B", "one family is exactly the octonion lines {i,i+1,i+3}; the other is {i,i+2,i+3} (Moebius/Csaszar labelling)",
      octo in (up, down) and (up | down) == (octo | other), f"octonion lines = {octo_fam}")
tris = up | down
edge_count = {}
for tri in tris:
    for pr in itertools.combinations(tri, 2):
        edge_count[pr] = edge_count.get(pr, 0) + 1
check("B", "21 edges = all pairs (K7), each in exactly 2 triangles", len(edge_count) == 21 and set(edge_count.values()) == {2})


def links_ok(T, n=7):
    for v in range(n):
        es = [tuple(sorted(set(t) - {v})) for t in T if v in t]
        if not es:
            return False
        adj = {}
        for a, b in es:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        if any(len(x) != 2 for x in adj.values()):
            return False
        # single cycle?
        start = es[0][0]
        seen, prev, cur = {start}, None, start
        while True:
            nxt = [y for y in adj[cur] if y != prev]
            nxt = nxt[0]
            if nxt == start:
                break
            seen.add(nxt)
            prev, cur = cur, nxt
        if len(seen) != len(adj):
            return False
    return True


def cyc_canon(t):
    k = t.index(min(t))
    return t[k:] + t[:k]


oriented = sorted({cyc_canon(t) for t in up_or + down_or})     # each triangle was generated once per vertex
assert len(oriented) == 14
dir_edges = [(t[i], t[(i + 1) % 3]) for t in oriented for i in range(3)]
check("B", "every vertex link is a single 6-cycle; with the plane's orientation each directed edge occurs once (orientable)",
      links_ok(tris) and len(dir_edges) == 42 and len(set(dir_edges)) == 42)
V, E, F = 7, len(edge_count), len(tris)
check("B", "V - E + F = 7 - 21 + 14 = 0", (V, E, F, V - E + F) == (7, 21, 14, 0), f"{V} - {E} + {F} = {V - E + F}")
VALUES["triangulation"] = {"V": V, "E": E, "F": F, "chi": V - E + F, "octonion_family": octo_fam}

# --- exhaustive: 2-(7,3,2) designs (every pair in exactly 2 of 14 distinct triangles)
ALLT = list(itertools.combinations(range(7), 3))
PAIRS = list(itertools.combinations(range(7), 2))
pair_tris = {pr: [t for t in ALLT if set(pr) <= set(t)] for pr in PAIRS}
designs = set()


def search(chosen, deficit):
    pr = next((q for q in PAIRS if deficit[q] > 0), None)
    if pr is None:
        designs.add(frozenset(chosen))
        return
    for t in pair_tris[pr]:
        if t in chosen:
            continue
        tp = list(itertools.combinations(t, 2))
        if all(deficit[q] > 0 for q in tp):
            for q in tp:
                deficit[q] -= 1
            chosen.add(t)
            search(chosen, deficit)
            chosen.discard(t)
            for q in tp:
                deficit[q] += 1


search(set(), {q: 2 for q in PAIRS})
surf = [d for d in designs if links_ok(d)]


def orientable(T):
    T = list(T)
    # try to orient triangles consistently by BFS
    ori = {T[0]: T[0]}
    queue = [T[0]]
    while queue:
        t = queue.pop()
        o = ori[t]
        des = {(o[i], o[(i + 1) % 3]) for i in range(3)}
        for u in T:
            if u in ori or len(set(u) & set(t)) != 2:
                continue
            # orient u so that the shared edge is traversed oppositely
            for cand in ((u[0], u[1], u[2]), (u[0], u[2], u[1])):
                ce = {(cand[i], cand[(i + 1) % 3]) for i in range(3)}
                if not (ce & des):
                    ori[u] = cand
                    queue.append(u)
                    break
    if len(ori) != len(T):
        return False
    alld = [(o[i], o[(i + 1) % 3]) for o in ori.values() for i in range(3)]
    return len(alld) == len(set(alld))


n_orient = sum(orientable(d) for d in surf)
ours = frozenset(tris)
orbit = {frozenset(tuple(sorted(pi[x] for x in t)) for t in ours) for pi in itertools.permutations(range(7))}
check("B", "exhaustive: simple 2-(7,3,2) designs on 7 labels = 120; all are surfaces (6-cycle links), all orientable, all relabellings of ours (unique 7-vertex torus)",
      len(designs) == 120 and len(surf) == 120 and n_orient == 120 and set(designs) == orbit,
      f"designs {len(designs)}, surfaces {len(surf)}, orientable {n_orient}, orbit {len(orbit)}")
auts = [pi for pi in itertools.permutations(range(7))
        if frozenset(tuple(sorted(pi[x] for x in t)) for t in ours) == ours]
affine = {tuple((a * x + b) % 7 for x in range(7)) for a in range(1, 7) for b in range(7)}
or_set = set(dir_edges)
n_pres = sum(all((pi[a], pi[b]) in or_set for a, b in dir_edges) for pi in auts)
check("B", "Aut(triangulation) has order 42 = AGL(1,7) and all 42 preserve orientation (chiral)",
      len(auts) == 42 and set(auts) == affine and n_pres == 42, f"|Aut| {len(auts)}, orientation-preserving {n_pres}")
VALUES["torus7"] = {"designs": len(designs), "surfaces": len(surf), "orientable": n_orient,
                    "orbit": len(orbit), "aut": len(auts), "aut_orientation_preserving": n_pres}

# the original's check *title* says "every 7-vertex triangulated closed surface is an orientable torus";
# test that wording: 7-vertex sphere and RP^2 exist (their search was restricted to pair-degree 2).
bipyr = [tuple(sorted((i, (i + 1) % 5, 5))) for i in range(5)] + [tuple(sorted((i, (i + 1) % 5, 6))) for i in range(5)]
hemi = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 1), (1, 2, 4), (2, 3, 5), (3, 4, 1), (4, 5, 2), (5, 1, 3)]
hemi = [tuple(sorted(t)) for t in hemi]
rp2_7 = [t for t in hemi if t != (0, 1, 2)] + [(0, 1, 6), (1, 2, 6), (0, 2, 6)]


def closed_surface(T, n):
    ec = {}
    for t in T:
        for pr in itertools.combinations(sorted(t), 2):
            ec[pr] = ec.get(pr, 0) + 1
    return set(ec.values()) == {2} and links_ok(T, n), n - len(ec) + len(T)


sph = closed_surface(bipyr, 7)
rp = closed_surface(rp2_7, 7)
check("B", "(wording audit) 7-vertex triangulated closed surfaces that are NOT tori exist: pentagonal bipyramid (chi 2) and a 7-vertex RP^2 (chi 1, non-orientable)",
      sph == (True, 2) and rp == (True, 1) and not orientable(rp2_7),
      f"sphere {sph}, RP2 {rp}")

# --- Fano planes
fanos = []


def fano_search(chosen, covered, start):
    if len(chosen) == 7:
        fanos.append(frozenset(chosen))
        return
    pr = next(q for q in PAIRS if q not in covered)
    for t in pair_tris[pr]:
        tp = list(itertools.combinations(t, 2))
        if any(q in covered for q in tp):
            continue
        chosen.append(t)
        fano_search(chosen, covered | set(tp), 0)
        chosen.pop()


fano_search([], frozenset(), 0)
fanos = set(fanos)
cyc = [f for f in fanos if frozenset(tuple(sorted((x + 1) % 7 for x in t)) for t in f) == f]
check("B", "exactly 30 Fano planes on 7 labels; exactly 2 kept by x -> x+1; they are the two torus families",
      len(fanos) == 30 and len(cyc) == 2 and set(cyc) == {frozenset(up), frozenset(down)}, f"{len(fanos)} planes, {len(cyc)} cyclic")


def img(S, f):
    return frozenset(tuple(sorted(f[x] for x in t)) for t in S)


autU = {pi for pi in itertools.permutations(range(7)) if img(up, pi) == frozenset(up)}
autD = {pi for pi in itertools.permutations(range(7)) if img(down, pi) == frozenset(down)}
aff124 = {tuple((a * x + b) % 7 for x in range(7)) for a in (1, 2, 4) for b in range(7)}
aff356 = {tuple((a * x + b) % 7 for x in range(7)) for a in (3, 5, 6) for b in range(7)}
check("B", "|Aut(family)| = 168 each; Aut(up) ∩ Aut(down) = {x -> ax+b, a in 1,2,4} (order 21); a in {3,5,6} swaps the families",
      len(autU) == 168 and len(autD) == 168 and (autU & autD) == aff124
      and all(img(up, f) == frozenset(down) and img(down, f) == frozenset(up) for f in aff356))
check("B", "orbit-stabiliser: 7!/|Aut(Fano)| = 5040/168 = 30 agrees with the backtracking count", 5040 // len(autU) == len(fanos) and 5040 % len(autU) == 0)
VALUES["fano"] = {"total": len(fanos), "cyclic": len(cyc), "aut": len(autU), "aut_intersection": len(autU & autD)}

# ==========================================================================
# C. matrix groups inside SU(3)
# ==========================================================================
i7 = I_OVER_SQRT7
D = mat([[z[1], 0, 0], [0, z[2], 0], [0, 0, z[4]]])
Dk = mat([[z[4], 0, 0], [0, z[2], 0], [0, 0, z[1]]])
C = mat([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
Cinv = mat([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
R = mscale(mat([[z[1] - z[6], z[2] - z[5], z[4] - z[3]],
                [z[2] - z[5], z[4] - z[3], z[1] - z[6]],
                [z[4] - z[3], z[1] - z[6], z[2] - z[5]]]), i7)
flip = mat([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])
Rf = mmul(mmul(flip, R), flip)          # flip^-1 = flip
# Luhn-Nasri-Ramond arXiv:0709.1447v2 eqs. (22), (23), read from the PDF by this cross-checker
LNR_B = mscale(mat([[z[3] - z[6], z[3] - z[1], z[1] - 1],
                    [z[2] - 1, z[6] - z[5], z[6] - z[2]],
                    [z[5] - z[4], z[4] - 1, z[5] - z[3]]]), i7)
LNR_A = mscale(mat([[z[2] - z[5], z[1] - z[6], z[4] - z[3]],
                    [z[1] - z[6], z[4] - z[3], z[2] - z[5]],
                    [z[4] - z[3], z[2] - z[5], z[1] - z[6]]]), i7)

check("C", "D, Dk, C, R, flip, Rf, LNR A, LNR B are all in SU(3) (exact M M^dagger = 1, det = 1)",
      all(in_SU3(M) for M in (D, Dk, C, R, flip, Rf, LNR_A, LNR_B)))
check("C", "D^7 = 1, C^3 = 1, R^2 = 1, flip^2 = 1", meq(mpow(D, 7), ID3) and meq(mpow(C, 3), ID3)
      and meq(mmul(R, R), ID3) and meq(mmul(flip, flip), ID3) and not meq(D, ID3))
check("C", "Weyl 3-cycle by conjugation: C^-1 D C = D^4 (the hexagon_check 'turn') and C D C^-1 = D^2",
      meq(mmul(mmul(Cinv, D), C), mpow(D, 4)) and meq(mmul(mmul(C, D), Cinv), mpow(D, 2)))

# F21: relations => quotient of <d,c | d^7, c^3, c^-1 d c d^-4>; Todd-Coxeter gives 21
W2 = lambda s: word_letters(s, "dc")
tc21 = todd_coxeter(2, [W2("d" * 7), W2("ccc"), W2("Cdc" + "DDDD")])
check("C", "|<D,C>| = 21: relations D^7 = C^3 = 1, C^-1 D C = D^4 hold exactly, the presented group has order 21 (Todd-Coxeter), and 21 divides the order (elements of order 7 and 3)",
      tc21 == 21, f"Todd-Coxeter index {tc21}")

# PSL(2,7) via LNR's presentation
WA = lambda s: word_letters(s, "ab")
tc168 = todd_coxeter(2, [WA("aa"), WA("bbb"), WA("ab" * 7), WA("ABab" * 4)])
Ainv, Binv = LNR_A, mmul(LNR_B, LNR_B)
comm = mmul(mmul(mmul(Ainv, Binv), LNR_A), LNR_B)
rels_ok = (meq(mmul(LNR_A, LNR_A), ID3) and meq(mpow(LNR_B, 3), ID3)
           and meq(mpow(mmul(LNR_A, LNR_B), 7), ID3) and meq(mpow(comm, 4), ID3))
check("C", "LNR relations hold exactly: A^2 = B^3 = (AB)^7 = [A,B]^4 = 1; the presented group has order 168 (Todd-Coxeter); so <A,B> is a non-trivial quotient of the simple group PSL(2,7): order exactly 168",
      rels_ok and tc168 == 168 and not meq(LNR_A, ID3), f"Todd-Coxeter index {tc168}")
check("C", "LNR's AB = D and LNR's A = Rf (Klein's involution conjugated by the flip)",
      meq(mmul(LNR_A, LNR_B), D) and meq(LNR_A, Rf))

def ev(word, gens):
    X = ID3
    for k in word:
        X = mmul(X, gens[k])
    return X


# mod-p permutation images
REPS = {}
for p in (29, 43):
    w = prim7(p)
    REPS[p] = w

p = 29
w = REPS[p]


def fm(M, p=29):
    return mmodp(M, p, REPS[p])


orders = {}
for p_ in (29, 43):
    for name, gens in (("F21", [D, C]), ("Klein", [Dk, C, R]), ("flipped", [D, C, Rf]), ("LNR", [LNR_A, LNR_B])):
        pts, index, perms = perm_rep([fm(M, p_) for M in gens], p_)
        orders[(name, p_)] = (BSGS(perms, len(pts)).order(), len(pts))
check("C", "Schreier-Sims on the mod-29 and mod-43 permutation images: |<D,C>| = 21, |<Dk,C,R>| = 168, |<D,C,Rf>| = 168, |<A,B>_LNR| = 168",
      all(orders[(n, q)][0] == o for n, o in (("F21", 21), ("Klein", 168), ("flipped", 168), ("LNR", 168)) for q in (29, 43)),
      {f"{k[0]}@{k[1]}": v[0] for k, v in orders.items()})

# perm rep of the flipped copy on generators [D, C, Rf] mod 29 ; also map LNR B and C into it
gensF = [D, C, Rf]
ptsF, idxF, permsF = perm_rep([fm(M) for M in gensF], 29)
nF = len(ptsF)
bsF = BSGS(permsF, nF)
wordsF = bfs_elements(permsF, pid(nF), pcomp)
elemsF = list(wordsF)
pB = perm_of_matrix(fm(LNR_B), ptsF, idxF, 29)
check("C", "LNR's B lies in <D, C, Rf> (mod-29 membership by sifting), and the word found evaluates to B exactly",
      pB is not None and bsF.contains(pB) and meq(ev(wordsF[pB], gensF), LNR_B),
      f"B = word {wordsF[pB]} in (D, C, Rf)")
ptsL, idxL, permsL = perm_rep([fm(M) for M in (LNR_A, LNR_B)], 29)
wordsL = bfs_elements(permsL, pid(len(ptsL)), pcomp)
pC = perm_of_matrix(fm(C), ptsL, idxL, 29)
wC = wordsL.get(pC)
Cw = ev(wC, (LNR_A, LNR_B)) if wC is not None else None
check("C", "C is a word in LNR's A, B (found mod 29, verified exactly), so <A,B> = <D, C, Rf>: the flipped copy has order 168 and is LNR's basis",
      wC is not None and meq(Cw, C), f"C = word {wC} in (A, B)")


check("C", "LNR: tr(A B^2) = b7bar (their class C6(AB^2)) and tr(AB) = b7 (C5(AB))",
      mtrace(mmul(LNR_A, mmul(LNR_B, LNR_B))) == B7.conj() and mtrace(mmul(LNR_A, LNR_B)) == B7)

# Klein's copy = flip^-1 (flipped copy) flip ; generators correspond
check("C", "flip Dk flip^-1 = D, flip C flip^-1 = C^-1, flip R flip^-1 = Rf: Klein's copy <Dk,C,R> = flip^-1 <D,C,Rf> flip (same order 168)",
      meq(mmul(mmul(flip, Dk), flip), D) and meq(mmul(mmul(flip, C), flip), Cinv) and meq(mmul(mmul(flip, R), flip), Rf))

# quartics -------------------------------------------------------------


def padd(P, Q):
    out = dict(P)
    for k, v in Q.items():
        out[k] = out.get(k, ZERO) + v
    return {k: v for k, v in out.items() if not v.is_zero()}


def pmulpoly(P, Q):
    out = {}
    for k1, v1 in P.items():
        for k2, v2 in Q.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            out[k] = out.get(k, ZERO) + v1 * v2
    return {k: v for k, v in out.items() if not v.is_zero()}


def subst(Pf, M):
    lin = [{(1, 0, 0): M[r][0], (0, 1, 0): M[r][1], (0, 0, 1): M[r][2]} for r in range(3)]
    lin = [{k: v for k, v in L.items() if not v.is_zero()} for L in lin]
    out = {}
    for (i, j, k), c in Pf.items():
        term = {(0, 0, 0): c}
        for r, e in ((0, i), (1, j), (2, k)):
            for _ in range(e):
                term = pmulpoly(term, lin[r])
        out = padd(out, term)
    return out


def peq(P, Q):
    return padd(P, {k: -v for k, v in Q.items()}) == {}


klein_q = {(3, 1, 0): ONE, (0, 3, 1): ONE, (1, 0, 3): ONE}       # x^3y + y^3z + z^3x
mirror_q = {(1, 3, 0): ONE, (0, 1, 3): ONE, (3, 0, 1): ONE}      # xy^3 + yz^3 + zx^3
lnr_q = {(3, 0, 1): ONE, (0, 1, 3): ONE, (1, 3, 0): ONE}         # phi1^3 phi3 + phi3^3 phi2 + phi2^3 phi1 (LNR eq. 78)
check("C", "Klein quartic invariant (exact polynomial identity) under Dk, C, R -- hence under all of Klein's copy",
      all(peq(subst(klein_q, M), klein_q) for M in (Dk, C, R)))
check("C", "mirror quartic xy^3+yz^3+zx^3 invariant under D, C, Rf (and LNR B) -- hence under all of the flipped copy",
      all(peq(subst(mirror_q, M), mirror_q) for M in (D, C, Rf, LNR_B)))
check("C", "LNR eq. (78) phi1^3 phi3 + phi3^3 phi2 + phi2^3 phi1 is the mirror quartic", peq(lnr_q, mirror_q))
check("C", "(attribution audit) LNR's A, which LNR describe as 'reproducing Klein's involution', is Rf, not hexagon_check's R; Rf does not keep x^3y+y^3z+z^3x and R does not keep the mirror quartic",
      not meq(LNR_A, R) and not peq(subst(klein_q, Rf), klein_q) and not peq(subst(mirror_q, R), mirror_q))
Dq = subst(klein_q, D)
ratios = {k: Dq.get(k, ZERO) for k in klein_q}
not_scalar = len({repr(v) for v in ratios.values()}) > 1
check("C", "D does not preserve the Klein quartic, not even up to a scalar (so D is not in Klein's copy)",
      not peq(Dq, klein_q) and set(Dq) == set(klein_q) and not_scalar)
diagK = sorted((a, b, c) for a in range(7) for b in range(7) for c in range(7)
               if (a + b + c) % 7 == 0 and (a, b, c) != (0, 0, 0)
               and (3 * a + b) % 7 == 0 and (3 * b + c) % 7 == 0 and (3 * c + a) % 7 == 0)
diagM = sorted((a, b, c) for a in range(7) for b in range(7) for c in range(7)
               if (a + b + c) % 7 == 0 and (a, b, c) != (0, 0, 0)
               and (a + 3 * b) % 7 == 0 and (b + 3 * c) % 7 == 0 and (c + 3 * a) % 7 == 0)
check("C", "non-trivial diagonal diag(z^a,z^b,z^c) in SU(3) keeping x^3y+y^3z+z^3x: exactly the 6 powers of Dk = (4,2,1); keeping the mirror quartic: exactly the 6 powers of D = (1,2,4)",
      diagK == sorted(((4 * j) % 7, (2 * j) % 7, j % 7) for j in range(1, 7))
      and diagM == sorted((j % 7, (2 * j) % 7, (4 * j) % 7) for j in range(1, 7)))
ptsK, idxK, permsK = perm_rep([fm(M) for M in (Dk, C, R)], 29)
bsK = BSGS(permsK, len(ptsK))
pDinK = perm_of_matrix(fm(D), ptsK, idxK, 29)
check("C", "mod-29 membership test agrees: D is not in Klein's copy, D is in the flipped copy",
      (pDinK is None or not bsK.contains(pDinK)) and bsF.contains(perm_of_matrix(fm(D), ptsF, idxF, 29)))

# maximality of F21 in the flipped copy: primitive (2-transitive) action on its 8 cosets
F21set = closure([permsF[0], permsF[1]], nF)
cosets = []
cos_of = {}
for g in elemsF:
    if g in cos_of:
        continue
    cs = frozenset(pmul(h, g) for h in F21set)      # right coset F g
    k = len(cosets)
    cosets.append(cs)
    for x in cs:
        cos_of[x] = k
act = [tuple(cos_of[pmul(next(iter(cs)), s)] for cs in cosets) for s in permsF]
G8 = closure(act, 8)
stab0 = [g for g in G8 if g[0] == 0]
orb = {g[1] for g in stab0}
check("C", "F21 has index 8 and the coset action is faithful (order 168) and 2-transitive -> primitive -> F21 is maximal",
      len(cosets) == 8 and len(G8) == 168 and orb == set(range(1, 8)))
outside = [g for g in elemsF if g not in F21set]
gen_all = all(len(closure([permsF[0], permsF[1], g], nF)) == 168 for g in outside)
check("C", "brute force too: <D, C, g> is the whole group for each of the 147 g outside F21", len(outside) == 147 and gen_all)

# ==========================================================================
# D. characters, classes, Frobenius-Schur indicators
# ==========================================================================


def char_table(perm_elems, words, gens_exact, n):
    classes = conj_classes(perm_elems)
    rows = []
    cls_index = {}
    for ci, cl in enumerate(classes):
        for g in cl:
            cls_index[g] = ci
    for ci, cl in enumerate(classes):
        rep = min(cl, key=lambda g: len(words[g]))
        Mx = ev(words[rep], gens_exact)
        sq = pmul(rep, rep)
        rows.append({"size": len(cl), "order": porder(rep), "chi": mtrace(Mx), "sq_class": cls_index[sq],
                     "rep": rep, "M": Mx})
    return rows, cls_index


def fs_and_norms(rows, order):
    s_cc = sum((r["chi"] * r["chi"].conj() * r["size"] for r in rows), ZERO) * Fr(1, order)
    s_c2 = sum((r["chi"] * r["chi"] * r["size"] for r in rows), ZERO) * Fr(1, order)
    fs = sum((rows[r["sq_class"]]["chi"] * r["size"] for r in rows), ZERO) * Fr(1, order)
    return s_cc, s_c2, fs


# exact traces of ALL elements (consistency: class function on the mod-p classes)
rowsF, cidxF = char_table(elemsF, wordsF, gensF, nF)
all_tr = {}
consistent = True
for g, wd in wordsF.items():
    t = mtrace(ev(wd, gensF))
    ci = cidxF[g]
    if ci in all_tr and not (all_tr[ci] == t):
        consistent = False
    all_tr[ci] = t
summary = sorted((r["size"], r["order"], fmtz(r["chi"])) for r in rowsF)
expect = sorted([(1, 1, "3"), (21, 2, "-1"), (56, 3, "0"), (42, 4, "1"), (24, 7, "b7"), (24, 7, "b7bar")])
nn, nb, fs = fs_and_norms(rowsF, 168)
check("D", "flipped PSL(2,7): classes (size, order, chi) = (1,1,3)(21,2,-1)(56,3,0)(42,4,1)(24,7,b7)(24,7,b7bar); trace constant on every class (all 168 traces exact)",
      summary == expect and consistent, summary)
check("D", "flipped PSL(2,7) triplet: <chi,chi> = 1, <chi,chibar> = 0, Frobenius-Schur indicator 0 (complex)",
      nn == ONE and nb.is_zero() and fs.is_zero())
check("D", "chi(D) = b7 = (-1+i sqrt7)/2 exactly", mtrace(D) == B7)
# simplicity: trivial centre and normal closure of every non-trivial class is everything
classesF = conj_classes(elemsF)
simple = all(len(closure(list(cl), nF)) == 168 for cl in classesF if pid(nF) not in cl)
check("D", "flipped copy is simple (normal closure of each non-identity class = whole group); simple of order 168 => PSL(2,7)", simple)

# Klein's copy
wordsK = bfs_elements(permsK, pid(len(ptsK)), pcomp)
rowsK, _ = char_table(list(wordsK), wordsK, [Dk, C, R], len(ptsK))
summaryK = sorted((r["size"], r["order"], fmtz(r["chi"])) for r in rowsK)
nnK, nbK, fsK = fs_and_norms(rowsK, 168)
check("D", "Klein's copy: same class/character data, <chi,chi> = 1, <chi,chibar> = 0, FS = 0",
      summaryK == expect and nnK == ONE and nbK.is_zero() and fsK.is_zero() and len(wordsK) == 168, summaryK)

# F21
ptsT, idxT, permsT = perm_rep([fm(D), fm(C)], 29)
wordsT = bfs_elements(permsT, pid(len(ptsT)), pcomp)
rowsT, _ = char_table(list(wordsT), wordsT, [D, C], len(ptsT))
summaryT = sorted((r["size"], r["order"], fmtz(r["chi"])) for r in rowsT)
nnT, nbT, fsT = fs_and_norms(rowsT, 21)
check("D", "F21: classes (1,1,3)(7,3,0)(7,3,0)(3,7,b7)(3,7,b7bar); <chi,chi> = 1, <chi,chibar> = 0, FS = 0 (complex)",
      summaryT == sorted([(1, 1, "3"), (7, 3, "0"), (7, 3, "0"), (3, 7, "b7"), (3, 7, "b7bar")])
      and nnT == ONE and nbT.is_zero() and fsT.is_zero(), summaryT)
VALUES["PSL27_triplet"] = {"classes": summary, "fs": 0}
VALUES["F21_triplet"] = {"classes": summaryT, "fs": 0}

# ==========================================================================
# E. subgroup lattice of PSL(2,7) in the faithful degree-8 coset action
# ==========================================================================
G8l = sorted(G8)
e8 = pid(8)
reps8 = [min(cl) for cl in conj_classes(G8l)]
subs = set()
for g in reps8:
    for h in G8l:
        subs.add(closure([g, h], 8))
allsubs = set()
for H in subs:
    for x in G8l:
        xi = pinv(x)
        allsubs.add(frozenset(pmul(pmul(xi, h), x) for h in H))
# closure under joins with single elements (one representative per conjugacy class suffices)
classes_of_subs = []
seen = set()
for H in sorted(allsubs, key=len):
    if H in seen:
        continue
    cl = {frozenset(pmul(pmul(pinv(x), h), x) for h in H) for x in G8l}
    seen |= cl
    classes_of_subs.append(cl)
def small_gens(H):
    gens_, S_ = [], frozenset([e8])
    for x in sorted(H):
        if x not in S_:
            gens_.append(x)
            S_ = closure(gens_, 8)
    return gens_


join_closed = True
for cl in classes_of_subs:
    H = next(iter(cl))
    hg = small_gens(H)
    assert closure(hg, 8) == H
    for g in G8l:
        if frozenset(closure(hg + [g], 8)) not in allsubs:
            join_closed = False
by_order = {}
for H in allsubs:
    by_order[len(H)] = by_order.get(len(H), 0) + 1
proper = [H for H in allsubs if len(H) < 168]
maximal = [H for H in proper if not any(H < K for K in proper)]
max_classes = {}
for H in maximal:
    key = None
    for ci, cl in enumerate(classes_of_subs):
        if H in cl:
            key = ci
    max_classes.setdefault(key, []).append(H)
max_summary = sorted((len(v[0]), len(v)) for v in max_classes.values())
check("E", "subgroup lattice (all 2-generated subgroups, closed under joins with elements => all subgroups): 179 subgroups in 15 classes",
      len(allsubs) == 179 and len(classes_of_subs) == 15 and join_closed,
      f"{len(allsubs)} subgroups, {len(classes_of_subs)} classes, by order {dict(sorted(by_order.items()))}")
F21_8 = frozenset(closure([act[0], act[1]], 8))
check("E", "maximal subgroups: 8 x order 21, 7 x order 24, 7 x order 24 (three classes: 7:3, S4, S4 as in ATLAS); F21 = <D,C> is one of the order-21 ones",
      max_summary == [(21, 8), (24, 7), (24, 7)] and F21_8 in maximal, max_summary)
norm21 = [x for x in G8l if frozenset(pmul(pmul(pinv(x), h), x) for h in F21_8) == F21_8]
check("E", "the order-21 subgroups form one class and N(F21) = F21", by_order.get(21) == 8 and len(norm21) == 21)
VALUES["PSL27_subgroups"] = {"total": len(allsubs), "classes": len(classes_of_subs),
                             "by_order": dict(sorted(by_order.items())), "maximal": max_summary}
# S4 classes vs Fano families (extra claim of the original, Finding 8)
S4classes = [v for v in max_classes.values() if len(v[0]) == 24]
# work in the 168-element perm image on ptsF for labelling: translate subgroups via words
toF = {}
for g8, gF in zip([tuple(cos_of[pmul(next(iter(cs)), g)] for cs in cosets) for g in elemsF], elemsF):
    toF[g8] = gF
pDF, pCF = permsF[0], permsF[1]
fam_from_S4 = []
for cl in S4classes:
    Hs = [frozenset(toF[h] for h in H) for H in cl]
    H0 = next(H for H in Hs if pCF in H)
    lab = {}
    Hj = H0
    for j in range(7):
        lab[Hj] = j
        Hj = frozenset(pmul(pmul(pinv(pDF), h), pDF) for h in Hj)      # D H D^-1 in "a then b" convention
    # the conjugation convention above: pmul(pmul(pinv(D),h),D) = D^-1 h D as 'then'-product = matrix D h D^-1
    acts = []
    for g in elemsF:
        acts.append(tuple(lab[frozenset(pmul(pmul(pinv(g), h), g) for h in H)] for H in sorted(lab, key=lab.get)))
    actset = set(acts)
    dlab = tuple(lab[frozenset(pmul(pmul(pinv(pDF), h), pDF) for h in H)] for H in sorted(lab, key=lab.get))
    clab = tuple(lab[frozenset(pmul(pmul(pinv(pCF), h), pCF) for h in H)] for H in sorted(lab, key=lab.get))
    fam = "up" if actset == autU else ("down" if actset == autD else None)
    fam_from_S4.append((fam, dlab, clab))
check("E", "(extra) PSL(2,7) acting on each S4 class, labelled so that D is x->x+1 and C is x->2x, is exactly the collineation group of one Fano family; the two classes give the two families",
      sorted(f[0] or "none" for f in fam_from_S4) == ["down", "up"]
      and all(f[1] == tuple((x + 1) % 7 for x in range(7)) and f[2] == tuple((2 * x) % 7 for x in range(7)) for f in fam_from_S4),
      [f[0] for f in fam_from_S4])

# ==========================================================================
# F. A5 (independent generators: 5-fold rotation + 2-fold about z)
# ==========================================================================
phi = Q5(Fr(1, 2), Fr(1, 2))
iphi = Q5(Fr(-1, 2), Fr(1, 2))
h = Q5(Fr(1, 2))
# 72-deg rotation about the vertex axis v = (0,1,phi): R = c I + sin72 [n]x + (1-c) n n^T with
# c = cos72 = (phi-1)/2, sin72 * n = v/2 (since |v| = 2 sin72), n n^T = v v^T/(phi+2)
c72 = (phi - 1) * h
vax = (Q5(0), Q5(1), phi)
_nn = phi + 2
_inv = Q5(_nn.a / (_nn.a ** 2 - 5 * _nn.b ** 2), -_nn.b / (_nn.a ** 2 - 5 * _nn.b ** 2))
_crs = [[Q5(0), -vax[2], vax[1]], [vax[2], Q5(0), -vax[0]], [-vax[1], vax[0], Q5(0)]]
M5 = tuple(tuple((c72 if i == j else Q5(0)) + _crs[i][j] * h + (Q5(1) - c72) * _inv * vax[i] * vax[j]
                 for j in range(3)) for i in range(3))
P2 = ((Q5(-1), Q5(0), Q5(0)), (Q5(0), Q5(-1), Q5(0)), (Q5(0), Q5(0), Q5(1)))


def qmul(A, B):
    return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), Q5(0)) for j in range(3)) for i in range(3))


def qT(A):
    return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))


def qdet(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


QI = ((Q5(1), Q5(0), Q5(0)), (Q5(0), Q5(1), Q5(0)), (Q5(0), Q5(0), Q5(1)))
orth = all(qmul(M, qT(M)) == QI and qdet(M) == Q5(1) for M in (M5, P2))
A5 = {QI: []}
frontier = [QI]
while frontier:
    nf = []
    for X in frontier:
        for k, g in enumerate((M5, P2)):
            Y = qmul(X, g)
            if Y not in A5:
                A5[Y] = A5[X] + [k]
                nf.append(Y)
    frontier = nf
verts = set()
for s1 in (1, -1):
    for s2 in (1, -1):
        for cyc_ in range(3):
            v = [Q5(0), Q5(s1), phi * s2]
            v = v[cyc_:] + v[:cyc_]
            verts.add(tuple(v))
keeps = all({tuple(sum((M[i][k] * v[k] for k in range(3)), Q5(0)) for i in range(3)) for v in verts} == verts for M in A5)
m5order = 1
X = M5
while X != QI:
    X = qmul(X, M5)
    m5order += 1
check("F", "A5: 5-fold M5 (72 deg about the vertex (0,1,phi)) and 2-fold diag(-1,-1,1) are real orthogonal over Q(sqrt5), generate 60 matrices mapping the 12 icosahedron vertices to themselves",
      orth and len(A5) == 60 and keeps and m5order == 5, f"|group| {len(A5)}, ord(M5) {m5order}")
A5l = list(A5)
A5idx = {M: i for i, M in enumerate(A5l)}
A5perm = [tuple(A5idx[qmul(X, g)] for X in A5l) for g in A5l]   # right regular rep
cls = []
seenA = set()
for i, M in enumerate(A5l):
    if M in seenA:
        continue
    cl = {qmul(qmul(qT(Y), M), Y) for Y in A5l}       # Y^-1 = Y^T
    seenA |= cl
    cls.append(cl)


def qtr(M):
    return M[0][0] + M[1][1] + M[2][2]


def qord(M):
    k, X = 1, M
    while X != QI:
        X = qmul(X, M)
        k += 1
    return k


a5rows = sorted((len(cl), qord(next(iter(cl))), qtr(next(iter(cl))).a, qtr(next(iter(cl))).b) for cl in cls)
tr_const = all(len({qtr(M) for M in cl}) == 1 for cl in cls)
fsA = sum((qtr(qmul(M, M)) for M in A5l), Q5(0)) * Q5(Fr(1, 60))
fsA2 = sum((qtr(qmul(M, M)).gal() for M in A5l), Q5(0)) * Q5(Fr(1, 60))
nA = sum((qtr(M) * qtr(M) for M in A5l), Q5(0)) * Q5(Fr(1, 60))
nA12 = sum((qtr(M) * qtr(M).gal() for M in A5l), Q5(0)) * Q5(Fr(1, 60))
simpleA = all(len(closure([A5perm[A5idx[M]] for M in cl], 60)) == 60 for cl in cls if QI not in cl)
check("F", "A5 classes (size, order, chi) = (1,1,3)(15,2,-1)(20,3,0)(12,5,(1+sqrt5)/2)(12,5,(1-sqrt5)/2); trace constant on classes; simple",
      a5rows == sorted([(1, 1, 3, 0), (15, 2, -1, 0), (20, 3, 0, 0), (12, 5, Fr(1, 2), Fr(1, 2)), (12, 5, Fr(1, 2), Fr(-1, 2))])
      and tr_const and simpleA, a5rows)
check("F", "A5 triplet 3: <chi,chi> = 1, FS = +1 (real); Galois-conjugate triplet 3': FS = +1, <chi,chi'> = 0 (inequivalent)",
      nA == Q5(1) and fsA == Q5(1) and fsA2 == Q5(1) and nA12 == Q5(0))
deg = [(a, b) for a in range(1, 8) for b in range(a, 8) if 1 + 9 + 9 + a * a + b * b == 60]
check("F", "remaining two irrep degrees forced: 60 - 1 - 9 - 9 = 41 = 4^2 + 5^2 only, so exactly two triplets, both real", deg == [(4, 5)], deg)
VALUES["A5"] = {"classes": [(s, o, f"{a}+{b}*sqrt5") for s, o, a, b in a5rows], "fs": [1, 1]}

# ==========================================================================
# G. Weyl groups (integer 2x2 matrices on Lambda) and the seven points
# ==========================================================================


def refl_long(alpha):           # alpha in Lambda, norm^2 2: x -> x - (alpha.x) alpha
    return imat_of_linear(lambda x: tuple(x[i] - dot3(alpha, x) * alpha[i] for i in range(3)))


def refl_short(i):              # alpha = e_i - (1,1,1)/3 ; x -> x - (alpha.x)(3 alpha), (alpha.x) = x_i on the plane
    a3 = tuple(3 * int(k == i) - 1 for k in range(3))
    return imat_of_linear(lambda x: tuple(x[k] - x[i] * a3[k] for k in range(3)))


def imul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


I2 = ((1, 0), (0, 1))


def gen_group(gens):
    Gs = {I2}
    fr = [I2]
    while fr:
        nf = []
        for X in fr:
            for g in gens:
                Y = imul(X, g)
                if Y not in Gs:
                    Gs.add(Y)
                    nf.append(Y)
        fr = nf
    return Gs


longs = [r for r in roots]
W_SU3 = gen_group([refl_long(r) for r in longs])
W_G2 = gen_group([refl_long(r) for r in longs] + [refl_short(i) for i in range(3)])


def idet(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def angle(M):
    tr = M[0][0] + M[1][1]
    s = M[1][0]                 # sign of sin: det[b1, M b1] in oriented basis (b1,b2) ~ (u,w)
    base = {2: 0, 1: 60, -1: 120, -2: 180}[tr]
    if base in (60, 120) and s < 0:
        base = 360 - base
    return base


def fate(k):
    if k is None:
        return "moves the seven points"
    f = tuple((k * x) % 7 for x in range(7))
    if img(up, f) == frozenset(up) and img(down, f) == frozenset(down):
        return f"x -> {k}x, keeps both families"
    if img(up, f) == frozenset(down) and img(down, f) == frozenset(up):
        return f"x -> {k}x, swaps the families"
    return f"x -> {k}x, other"


weyl_out = {}
for name, Wg, nm in (("SU(3)", W_SU3, 3), ("G2", W_G2, 6)):
    mir = [g for g in Wg if idet(g) == -1]
    rots = [g for g in Wg if idet(g) == 1]
    keepsL = all(all(isinstance(x, int) for row in g for x in row) for g in Wg)
    mk = sum(label7(imat_apply(g, P7)) is not None for g in mir)
    rows = sorted((angle(g), fate(label7(imat_apply(g, P7)))) for g in rots)
    weyl_out[name] = {"order": len(Wg), "keeps_Lambda": keepsL, "mirrors": len(mir), "mirrors_keeping": mk, "turns": rows}
check("G", "W(SU(3)): order 6 (integer matrices: keeps Lambda); turns 0/120/240 = x->1x,4x,2x keep both families; 3 mirrors, none keeps the seven points",
      weyl_out["SU(3)"]["order"] == 6 and weyl_out["SU(3)"]["mirrors"] == 3 and weyl_out["SU(3)"]["mirrors_keeping"] == 0
      and weyl_out["SU(3)"]["turns"] == [(0, "x -> 1x, keeps both families"), (120, "x -> 4x, keeps both families"), (240, "x -> 2x, keeps both families")],
      weyl_out["SU(3)"]["turns"])
check("G", "W(G2): order 12; adds 60/180/300 = x->5x,6x,3x which swap the families; 6 mirrors, none keeps the seven points",
      weyl_out["G2"]["order"] == 12 and weyl_out["G2"]["mirrors"] == 6 and weyl_out["G2"]["mirrors_keeping"] == 0
      and weyl_out["G2"]["turns"] == [(0, "x -> 1x, keeps both families"), (60, "x -> 5x, swaps the families"),
                                       (120, "x -> 4x, keeps both families"), (180, "x -> 6x, swaps the families"),
                                       (240, "x -> 2x, keeps both families"), (300, "x -> 3x, swaps the families")],
      weyl_out["G2"]["turns"])
minus1 = ((-1, 0), (0, -1))
check("G", "W(G2) = W(SU(3)) x {+-1}", W_G2 == W_SU3 | {imul(minus1, g) for g in W_SU3})
# mirrors send D's points to those of diag(z, z^4, z^2): theta = (1,4,-5)/7 -> coords (1,5)
P7b = to_c((1, 4, -5))
mir_su3 = [g for g in W_SU3 if idet(g) == -1]
check("G", "(extra) each SU(3) mirror maps the seven points of D onto those of diag(z,z^4,z^2)",
      all({tuple(x % 7 for x in imat_apply(g, (j * P7[0], j * P7[1]))) for j in range(7)}
          == {((j * P7b[0]) % 7, (j * P7b[1]) % 7) for j in range(7)} for g in mir_su3))
VALUES["weyl"] = {k: {"order": v["order"], "mirrors": v["mirrors"], "mirrors_keeping": v["mirrors_keeping"],
                      "turns": [f"{a} deg: {f}" for a, f in v["turns"]]} for k, v in weyl_out.items()}

# ==========================================================================
# H. affine Weyl groups (rational affine maps in Lambda coordinates)
# ==========================================================================


def aff_refl(alpha3, k, coroot3):
    """x -> x - ((alpha,x) - k) coroot, as (M, t) with M integer 2x2 and t rational 2-vector (Lambda coords)."""
    M = imat_of_linear(lambda x: tuple(x[i] - dot3(alpha3, x) * coroot3[i] for i in range(3)))
    t = to_c(tuple(Fr(k) * c for c in coroot3))
    return (M, (Fr(t[0]), Fr(t[1])))


def amul(f, g):
    """(f then g): x -> g(f(x))"""
    Mf, tf = f
    Mg, tg = g
    M = imul(Mg, Mf)
    t = imat_apply(Mg, tf)
    return (M, (t[0] + tg[0], t[1] + tg[1]))


AID = (I2, (Fr(0), Fr(0)))


def aorder(f, cap=100):
    X = f
    for k in range(1, cap):
        if X == AID:
            return k
        X = amul(X, f)
    return None


# my own G2 base: alpha2 = (1,-1,0) long, alpha1 = (-2,1,1)/3 short (150 deg); theta = 3a1 + 2a2 = (0,-1,1)
a2 = (1, -1, 0)
a1_3 = (-2, 1, 1)                       # 3*alpha1 = coroot of alpha1
theta = (0, -1, 1)
# reflection in a short root alpha (=a1_3/3): (alpha,x) = (a1_3 . x)/3 ; coroot = a1_3
s1 = (imat_of_linear(lambda x: tuple(x[i] - Fr(dot3(a1_3, x), 3) * a1_3[i] for i in range(3))), (Fr(0), Fr(0)))
assert all(Fr(v).denominator == 1 for row in s1[0] for v in row)
s1 = ((tuple(tuple(int(v) for v in row) for row in s1[0])), s1[1])
s2 = aff_refl(a2, 0, a2)
s0 = aff_refl(theta, 1, theta)
cox = (aorder(amul(s1, s2)), aorder(amul(s2, s0)), aorder(amul(s1, s0)))
check("H", "affine G2 Coxeter orders: (s1 s2)^6 = (s2 s0)^3 = (s1 s0)^2 = 1 (triangle group (2,3,6))", cox == (6, 3, 2), cox)
# linear parts of s1, s2 generate W(G2); s_theta in <s1,s2>; s0 s_theta = translation by theta
lin12 = gen_group([s1[0], s2[0]])
s_theta = aff_refl(theta, 0, theta)
trans_theta = amul(s_theta, s0)          # x -> s0(s_theta(x)) = x + theta
check("H", "s1, s2 generate W(G2) (order 12); s_theta in it; s_theta then s0 = translation by theta^vee = theta in Lambda; W-images of theta are the 6 long roots, which span Lambda => W_aff = Lambda ⋊ W(G2)",
      lin12 == W_G2 and s_theta[0] in lin12 and trans_theta == (I2, (Fr(to_c(theta)[0]), Fr(to_c(theta)[1])))
      and {imat_apply(g, to_c(theta)) for g in W_G2} == {to_c(r) for r in roots})
# W_aff elements: translations integral for all generators
check("H", "all generators have integer translation parts (W_aff ⊂ Lambda ⋊ W(G2)), so translations = Lambda (hexagonal), point group = W(G2) dihedral of order 12 with a 60 deg turn: wallpaper group p6m",
      all(t[0].denominator == 1 and t[1].denominator == 1 for _, t in (s0, s1, s2)) and any(angle(g) == 60 for g in W_G2 if idet(g) == 1))


def site_pattern(Wg):
    """rotation centres per cell: x in (1/12)Z^2 mod Z^2 with stabiliser {w : w x - x in Z^2}."""
    out = {}
    for i in range(12):
        for j in range(12):
            x = (Fr(i, 12), Fr(j, 12))
            st = [g for g in Wg if all((imat_apply(g, x)[k] - x[k]).denominator == 1 for k in range(2))]
            rot = [g for g in st if idet(g) == 1]
            if len(rot) > 1:
                out[(str(x[0]), str(x[1]))] = (len(rot), len(st) - len(rot))
    return out


sp_g2 = site_pattern(W_G2)
sp_su3 = site_pattern(W_SU3)
cnt_g2 = {}
for v in sp_g2.values():
    cnt_g2[v] = cnt_g2.get(v, 0) + 1
cnt_su3 = {}
for v in sp_su3.values():
    cnt_su3[v] = cnt_su3.get(v, 0) + 1
check("H", "G2 rotation centres per cell (exhaustive on the 1/12 grid, which contains all of them): one 6-fold with 6 mirrors (6mm), two 3-fold with 3 mirrors (3m), three 2-fold with 2 mirrors (2mm) -- the p6m pattern 1a, 2b, 3c",
      cnt_g2 == {(6, 6): 1, (3, 3): 2, (2, 2): 3}, {str(k): v for k, v in cnt_g2.items()})
check("H", "SU(3) contrast: three 3-fold centres per cell, each on 3 mirrors (p3m1, not p31m)", cnt_su3 == {(3, 3): 3}, {str(k): v for k, v in cnt_su3.items()})
# elements of Lambda ⋊ W keeping the 7 points mod Lambda: exactly those w keeping L'
keepG2 = [g for g in W_G2 if label7(imat_apply(g, P7)) is not None]
keepSU3 = [g for g in W_SU3 if label7(imat_apply(g, P7)) is not None]
check("H", "(extra) elements keeping the seven points: Lambda ⋊ C6 (p6) for G2, Lambda ⋊ C3 (p3) for SU(3); no mirror",
      len(keepG2) == 6 and all(idet(g) == 1 for g in keepG2) and len(keepSU3) == 3 and all(idet(g) == 1 for g in keepSU3))
# no point j p (j != 0) lies on an affine mirror: mirror (alpha,x) = k ; test with all roots
on_mirror = False
for j in range(1, 7):
    x3 = tuple(Fr(j * c, 7) for c in (1, 2, -3))
    for r in roots:
        if Fr(dot3(r, x3)).denominator == 1:
            on_mirror = True
    for i in range(3):
        a3 = tuple(3 * int(k == i) - 1 for k in range(3))
        # short root alpha = a3/3 ; affine mirrors (alpha, x) in Z  (G2 affine walls for short roots: (alpha,x) = k)
        if (Fr(dot3(a3, x3)) / 3).denominator == 1:
            on_mirror = True
check("H", "(extra) no point j p (j=1..6) lies on any affine mirror (alpha,x) = k of either group", not on_mirror)
VALUES["affine_weyl"] = {"G2": {"coxeter": list(cox), "sites": {str(k): v for k, v in cnt_g2.items()}, "wallpaper": "p6m"},
                         "SU3": {"sites": {str(k): v for k, v in cnt_su3.items()}, "wallpaper": "p3m1"}}

# ==========================================================================
# I. octonions, G2, PGL(2,7)
# ==========================================================================
# (1) Fano-table model: e_i e_{i+1} = e_{i+3} on imaginary units 1..7 (labels 0..6 -> index 1..7)
mult = {}
for i in range(7):
    a, b, c = i, (i + 1) % 7, (i + 3) % 7
    for (x, y, zz) in ((a, b, c), (b, c, a), (c, a, b)):
        mult[(x, y)] = (1, zz)
        mult[(y, x)] = (-1, zz)


def omul_basis(i, j):
    """basis index 0 = 1, k+1 = e_k ; returns (sign, index)."""
    if i == 0:
        return 1, j
    if j == 0:
        return 1, i
    if i == j:
        return -1, 0
    s, k = mult[(i - 1, j - 1)]
    return s, k + 1


def omul(x, y):
    out = [Fr(0)] * 8
    for i in range(8):
        if x[i]:
            for j in range(8):
                if y[j]:
                    s, k = omul_basis(i, j)
                    out[k] += s * x[i] * y[j]
    return out


E8 = [[Fr(int(k == i)) for k in range(8)] for i in range(8)]


def assoc(x, y, w_):
    a = omul(omul(x, y), w_)
    b = omul(x, omul(y, w_))
    return [p - q for p, q in zip(a, b)]


alt_ok = all(all(v == 0 for v in [p + q for p, q in zip(assoc(E8[i], E8[j], E8[k]), assoc(E8[j], E8[i], E8[k]))])
             and all(v == 0 for v in [p + q for p, q in zip(assoc(E8[i], E8[j], E8[k]), assoc(E8[i], E8[k], E8[j]))])
             for i in range(8) for j in range(8) for k in range(8))
check("I", "Fano-table octonions (e_i e_{i+1} = e_{i+3}): associator alternating on all 512 basis triples (alternative algebra)", alt_ok)


def nullspace_dim(rows, ncols):
    rows = [list(r) for r in rows]
    rank = 0
    pivcols = []
    r0 = 0
    for c in range(ncols):
        piv = next((i for i in range(r0, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r0], rows[piv] = rows[piv], rows[r0]
        pv = rows[r0][c]
        rows[r0] = [v / pv for v in rows[r0]]
        for i in range(len(rows)):
            if i != r0 and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r0])]
        pivcols.append(c)
        r0 += 1
        if r0 == len(rows):
            break
    return ncols - r0, rows[:r0], pivcols


def der_equations(extra_kill=()):
    # unknown D (8x8), D[k][i] = coefficient of e_k in D(e_i); variable index k*8+i
    eqs = []
    for i in range(8):
        for j in range(8):
            s, k = omul_basis(i, j)
            # D(e_i e_j) = s D(e_k) ; D(e_i) e_j = sum_m D[m][i] e_m e_j ; e_i D(e_j) = sum_m D[m][j] e_i e_m
            for comp in range(8):
                row = [Fr(0)] * 64
                row[comp * 8 + k] += s
                for m in range(8):
                    s2, k2 = omul_basis(m, j)
                    if k2 == comp:
                        row[m * 8 + i] -= s2
                    s3, k3 = omul_basis(i, m)
                    if k3 == comp:
                        row[m * 8 + j] -= s3
                eqs.append(row)
    for e in extra_kill:
        for comp in range(8):
            row = [Fr(0)] * 64
            row[comp * 8 + e] = Fr(1)
            eqs.append(row)
    return eqs


dimDer, _, _ = nullspace_dim(der_equations(), 64)
dimStab, _, _ = nullspace_dim(der_equations(extra_kill=(1,)), 64)
check("I", "Der(O) has dimension 14 (= dim g2); derivations killing the imaginary unit e_0 form an 8-dim algebra (= dim su(3))",
      dimDer == 14 and dimStab == 8, f"dim Der = {dimDer}, dim Stab(e) = {dimStab}")

# (2) C + C^3 model of the report, checked symbolically (alternative + composition => octonions by Hurwitz)
import sympy as sp
xs = sp.symbols("x0:8", real=True)
ys = sp.symbols("y0:8", real=True)
ws = sp.symbols("w0:8", real=True)


def cc3(v):
    return (v[0] + sp.I * v[1], [v[2] + sp.I * v[3], v[4] + sp.I * v[5], v[6] + sp.I * v[7]])


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def cprod(X, Y):
    a, u = X
    b, v = Y
    s = a * b - sum(u[i] * sp.conjugate(v[i]) for i in range(3))
    cr = cross(u, v)
    vec = [a * v[i] + sp.conjugate(b) * u[i] + sp.conjugate(cr[i]) for i in range(3)]
    return (s, vec)


def cnorm(X):
    a, u = X
    return sp.expand(a * sp.conjugate(a) + sum(ui * sp.conjugate(ui) for ui in u))


X_, Y_ = cc3(xs), cc3(ys)
ONE_O = (sp.Integer(1), [sp.Integer(0)] * 3)
unit_ok = all(sp.expand(p - q) == 0 for P_, Q_ in ((cprod(ONE_O, X_), X_), (cprod(X_, ONE_O), X_))
              for p, q in zip([P_[0]] + P_[1], [Q_[0]] + Q_[1]))
XY = cprod(X_, Y_)
comp_ok = sp.expand(cnorm(XY) - cnorm(X_) * cnorm(Y_)) == 0
XX_Y = cprod(cprod(X_, X_), Y_)
X_XY = cprod(X_, cprod(X_, Y_))
alt1 = all(sp.expand(p - q) == 0 for p, q in zip([XX_Y[0]] + XX_Y[1], [X_XY[0]] + X_XY[1]))
YX_X = cprod(cprod(Y_, X_), X_)
Y_XX = cprod(Y_, cprod(X_, X_))
alt2 = all(sp.expand(p - q) == 0 for p, q in zip([YX_X[0]] + YX_X[1], [Y_XX[0]] + Y_XX[1]))
check("I", "C + C^3 product of the report: N(xy) = N(x)N(y) and x(xy) = (xx)y, (yx)x = y(xx) as symbolic identities in 16 real variables (unital composition algebra of dim 8 => octonions)",
      comp_ok and alt1 and alt2 and unit_ok)

# automorphisms on an R-basis: (1,0), (G,0), (0,e_k), (0,G e_k)  with G = sqrt(-7) in Q(zeta7)


def zprod(X, Y):
    a, u = X
    b, v = Y
    s = a * b - sum((u[i] * v[i].conj() for i in range(3)), ZERO)
    cr = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
    vec = tuple(a * v[i] + b.conj() * u[i] + cr[i].conj() for i in range(3))
    return (s, vec)


def zeq(X, Y):
    return X[0] == Y[0] and all(p == q for p, q in zip(X[1], Y[1]))


RB = [(ONE, (ZERO, ZERO, ZERO)), (G, (ZERO, ZERO, ZERO))]
for k in range(3):
    for s_ in (ONE, G):
        RB.append((ZERO, tuple(s_ if i == k else ZERO for i in range(3))))


def act_lin(M):
    return lambda X: (X[0], tuple(sum((M[i][j] * X[1][j] for j in range(3)), ZERO) for i in range(3)))


kappa = lambda X: (X[0].conj(), tuple(x.conj() for x in X[1]))
autos = {name: all(zeq(f(zprod(x, y)), zprod(f(x), f(y))) for x in RB for y in RB)
         for name, f in (("D", act_lin(D)), ("C", act_lin(C)), ("Rf", act_lin(Rf)), ("Dk", act_lin(Dk)),
                         ("R", act_lin(R)), ("LNR_B", act_lin(LNR_B)), ("kappa", kappa))}
check("I", "D, C, Rf, Dk, R, LNR B (on C^3) and complex conjugation kappa are octonion automorphisms (exact, 64 R-basis pairs); the matrices fix (G,0) ~ the imaginary unit, kappa negates it",
      all(autos.values()) and zeq(kappa(RB[1]), (-G, (ZERO, ZERO, ZERO))), autos)

# PGL(2,7): kappa normalises the flipped copy and acts as an outer automorphism
cB = mconj(LNR_B)
cA = mconj(LNR_A)
pcB = perm_of_matrix(fm(cB), ptsF, idxF, 29)
pcA = perm_of_matrix(fm(cA), ptsF, idxF, 29)
pcRf = perm_of_matrix(fm(mconj(Rf)), ptsF, idxF, 29)
wcB = wordsF.get(pcB) if pcB is not None else None
closed_conj = (pcB is not None and bsF.contains(pcB) and pcA is not None and bsF.contains(pcA)
               and wcB is not None and meq(ev(wcB, gensF), cB) and meq(cA, LNR_A))
check("I", "the flipped copy is closed under complex conjugation: conj(A) = A, conj(B) in the group (word verified exactly), conj(D) = D^-1, conj(C) = C",
      closed_conj and meq(mconj(D), mpow(D, 6)) and meq(mconj(C), C))
pD = permsF[0]
pD6 = pinv(pD)
classD = next(cl for cl in classesF if pD in cl)
check("I", "conj(D) = D^6 is NOT conjugate to D in PSL(2,7) (7A <-> 7B): conjugation by kappa is an outer automorphism; <flipped copy, kappa> = PSL(2,7) ⋊ Z2 of order 336 acting faithfully => Aut(PSL(2,7)) = PGL(2,7)",
      pD6 not in classD)
# kappa swaps the two S4 classes: compute the automorphism alpha on elements via words with conj generators
cgens = [mconj(M) for M in gensF]
pc = [perm_of_matrix(fm(M), ptsF, idxF, 29) for M in cgens]


def alpha(g):
    X = pid(nF)
    for k in wordsF[g]:
        X = pcomp(X, pc[k])
    return X


S4F = [[frozenset(toF[h] for h in H) for H in cl] for cl in S4classes]
img0 = {frozenset(alpha(h) for h in S4F[0][0])}
check("I", "kappa maps the first S4 class onto the second (it swaps the two classes of maximal S4)",
      next(iter(img0)) in set(S4F[1]) and next(iter(img0)) not in set(S4F[0]))
lab_grp = closure([tuple((x + 1) % 7 for x in range(7)), tuple((2 * x) % 7 for x in range(7)),
                   tuple((-x) % 7 for x in range(7))], 7)
check("I", "on the labels <D (x->x+1), C (x->2x), kappa (x->-x)> generate AGL(1,7) of order 42 = Aut(triangulation)",
      len(lab_grp) == 42 and set(lab_grp) == set(auts))
VALUES["octonions"] = {"der_dim": dimDer, "stab_dim": dimStab, "PGL27_order": 336}

# ==========================================================================
# J. order-7 torus points with a hexagonal finer lattice
# ==========================================================================


def reduce_basis(u, v):
    """Lagrange-Gauss reduction with the Lambda Gram (vectors in units of 1/7)."""
    while True:
        if gram7(u, u) > gram7(v, v):
            u, v = v, u
        m = round(gram7(u, v) / gram7(u, u))
        if m == 0:
            return u, v
        v = (v[0] - m * u[0], v[1] - m * u[1])


hexpts = []
for a in range(7):
    for b in range(7):
        if (a, b) == (0, 0):
            continue
        # 7L = 7Z^2 + Z(a,b): HNF basis
        if a % 7 != 0:
            ainv = pow(a, -1, 7)
            basis = ((1 * 1, (b * ainv) % 7), (0, 7))
        else:
            basis = ((7, 0), (0, 1))
        u, v = reduce_basis(basis[0], basis[1])
        gu, gv, guv = gram7(u, u), gram7(v, v), abs(gram7(u, v))
        if gu == gv and 2 * guv == gu:
            hexpts.append((a, b))
subgroups = {frozenset(((k * a) % 7, (k * b) % 7) for k in range(1, 7)) for a, b in hexpts}
expect_sub = {frozenset(((k * P7[0]) % 7, (k * P7[1]) % 7) for k in range(1, 7)),
              frozenset(((k * P7b[0]) % 7, (k * P7b[1]) % 7) for k in range(1, 7))}
check("J", "(extra) of the 48 order-7 torus points, exactly 12 give a hexagonal finer lattice: the two order-7 subgroups of D and of diag(z,z^4,z^2)",
      len(hexpts) == 12 and subgroups == expect_sub, f"{len(hexpts)} points, {len(subgroups)} subgroups")
VALUES["order7_hex"] = {"points": len(hexpts), "of": 48, "subgroups": len(subgroups)}

# ==========================================================================
# K. the 25 lines of hexagon_check.py, rebuilt from the values computed above
# ==========================================================================
lines = []
lines.append(f"120° turn sends point 1 to point {lab_turn}")
lines.append(f"neighbours of point 0: {labels6} -> every point touches every other (K7)")
lines.append(f"triangles: {len(up | down)} | family A Fano: {is_fano(up)} | family B Fano: {is_fano(down)}")
lines.append(f"one family is the octonion lines {{i, i+1, i+3}}: {octo in (up, down)}")
lines.append(f"x -> ax+b (a in 1,2,4) preserves both families: {aff124 <= (autU & autD)}")
ordF21 = orders[("F21", 29)][0]
lines.append(f"|<D, 120° turn>| = {ordF21} | inside SU(3): {in_SU3(D) and in_SU3(C)}")
lines.append(f"|<Klein's matrices>| = {orders[('Klein', 29)][0]} | inside SU(3): {all(in_SU3(M) for M in (Dk, C, R))}")
lines.append(f"Klein quartic preserved by the generators: {all(peq(subst(klein_q, M), klein_q) for M in (Dk, C, R))}")
lines.append(f"<D, 120° turn> inside Klein's own copy: {pDinK is not None and bsK.contains(pDinK)}")
lines.append(f"flip in SU(3): {in_SU3(flip)} | flip sends Dk to D: {meq(mmul(mmul(flip, Dk), flip), D)}")
lines.append(f"flipped copy: order {orders[('flipped', 29)][0]} | inside SU(3): {all(in_SU3(M) for M in (D, C, Rf))} | holds <D, 120° turn>: {bsF.contains(permsF[0]) and bsF.contains(permsF[1])}")
lines.append(f"flipped copy preserves the mirror quartic xy³ + yz³ + zx³: {all(peq(subst(mirror_q, M), mirror_q) for M in (D, C, Rf))}")
lines.append(f"order-21 group maximal in it: {len(G8) == 168 and orb == set(range(1, 8))}")
lines.append(f"Fano planes on Z7 kept by x -> x+1: {len(cyc)} | the torus families are exactly these: {set(cyc) == {frozenset(up), frozenset(down)}}")
for name in ("SU(3)", "G2"):
    v = weyl_out[name]
    lines.append(f"Weyl({name}): order {v['order']} | keeps Λ: {v['keeps_Lambda']} | mirrors that keep the seven points: {v['mirrors_keeping']} of {v['mirrors']}")
    for a_, f_ in v["turns"]:
        lines.append(f"   turn {a_:>3}°: {f_}")
with open(os.path.join(HERE, "xc_replica_lines.txt"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
import subprocess
orig = subprocess.run([sys.executable, os.path.join(HERE, "..", "..", "..", "hexagon_check.py")],
                      capture_output=True, text=True, env=dict(os.environ)).stdout.splitlines()
same = sum(1 for a_, b_ in zip(orig, lines) if a_ == b_)
check("K", "the 25 lines printed by hexagon_check.py (run now) equal the lines rebuilt from this cross-check's exact values",
      len(orig) == 25 and len(lines) == 25 and same == 25, f"{same} of {len(orig)} identical")
VALUES["replica"] = {"lines_original": len(orig), "lines_xc": len(lines), "identical": same}

# ==========================================================================
n_pass = sum(c["ok"] for c in CHECKS)
print(f"\n{n_pass} of {len(CHECKS)} checks pass; {time.time() - T0:.1f} s")
out = {"experiment": "E0_hexagon_exact", "role": "independent cross-check", "n_checks": len(CHECKS), "n_pass": n_pass,
       "all_pass": n_pass == len(CHECKS), "checks": CHECKS, "values": VALUES,
       "runtime_seconds": round(time.time() - T0, 1)}
with open(os.path.join(HERE, "xc_checks.json"), "w") as fh:
    json.dump(out, fh, indent=1, default=str)
sys.exit(0 if n_pass == len(CHECKS) else 1)
