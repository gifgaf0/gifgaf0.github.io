#!/usr/bin/env python3
"""
e0_exact.py -- Experiment E0 of seed/PLAN.md section 4:
"The hexagon facts, recomputed exactly (SEED.md section 3)".

Every decision below is made in exact arithmetic:
  * the torus, lattices, Weyl and affine Weyl groups: rational numbers (fractions.Fraction);
  * all 3x3 matrices of hexagon_check.py: the cyclotomic field Q(zeta_7)
    (exact_fields.Z7), using i*sqrt7 = (z+z^2+z^4) - (z^3+z^5+z^6) (quadratic Gauss sum),
    so i/sqrt7 = that / 7, and complex conjugation = (zeta -> zeta^-1);
  * A5's triplets: the field Q(sqrt5) (exact_fields.Q5);
  * Fano planes, triangulations, permutation groups: integers.
Floats are used only to print a number for a human and to fix one sign
(G = +i sqrt7 rather than -i sqrt7 under zeta = exp(2 pi i/7)).

Run:   python3 e0_exact.py            (about 8 s on one core)
Writes (next to this file): results.json, exact_replica_output.txt,
        hexagon_check_original_output.txt (by running ../../hexagon_check.py).
"""
import itertools
import json
import os
import subprocess
import sys
import time
from collections import Counter
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from exact_fields import (Z7, Q5, GAUSS7, ZERO7, ONE7, FiniteGroup, mat, mmul, mvec,  # noqa: E402
                          conjT, mconj, transpose, det3, trace, mkey, identity)

T0 = time.time()
CHECKS = []          # every check: section, name, ok, detail
REPLICA = []         # hexagon_check.py's printed lines, regenerated from exact results
VALUES = {}          # headline values for results.json


def check(section, name, ok, detail=""):
    CHECKS.append(dict(section=section, name=name, ok=bool(ok), detail=str(detail)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail != "" else ""), flush=True)
    return bool(ok)


def header(s):
    print(f"\n=== {s}   [t = {time.time() - T0:.1f} s]", flush=True)


# =============================================================================
# A. The field Q(zeta_7)
# =============================================================================
header("A. exact field Q(zeta7)")
z = Z7.zeta
G = GAUSS7                                   # sum_k (k/7) zeta^k
check("A", "Gauss sum G = (z+z^2+z^4)-(z^3+z^5+z^6) satisfies G^2 = -7 exactly", G * G == Z7.rat(-7))
check("A", "under zeta = exp(2 pi i/7), G = +i sqrt7 (sign check)", abs(G.complex() - 1j * 7 ** 0.5) < 1e-12,
      f"G ~ {G.complex():.12f}")
I_SQRT7 = G * F(1, 7)                        # i / sqrt7, exactly
check("A", "i/sqrt7 := G/7 satisfies (i/sqrt7)^2 = -1/7", I_SQRT7 * I_SQRT7 == Z7.rat(-1, 7))
b7 = z(1) + z(2) + z(4)
b7bar = b7.conj()
check("A", "b7 := z+z^2+z^4 = (-1 + i sqrt7)/2 exactly", b7 == (G - 1) * F(1, 2))
check("A", "b7 is not real (b7 != conj(b7)); b7 - conj(b7) = i sqrt7", (not b7.is_real()) and b7 - b7bar == G)
VALUES["b7"] = dict(value="z+z^2+z^4 = (-1+i sqrt7)/2 (exact in Q(zeta7))",
                    numeric=str(b7.complex()))


# =============================================================================
# B. The torus, the seven points, the triangulation, Fano planes
# =============================================================================
header("B. SU(3) torus, seven points, triangulation, Fano planes (exact rationals / integers)")


def vadd(u, v):
    return tuple(a + b for a, b in zip(u, v))


def vsub(u, v):
    return tuple(a - b for a, b in zip(u, v))


def vscal(k, v):
    return tuple(k * a for a in v)


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def in_Lambda(v):
    """Lambda = {theta in Z^3 : theta1+theta2+theta3 = 0} (kernel of theta -> diag(exp(2 pi i theta)))."""
    return all(F(x).denominator == 1 for x in v) and sum(v) == 0


def lam2(v):
    """coordinates of a plane vector in the Lambda basis b1=(1,-1,0), b2=(0,1,-1)."""
    assert sum(v) == 0
    return (F(v[0]), F(-v[2]))


b1, b2 = (F(1), F(-1), F(0)), (F(0), F(1), F(-1))
gram_L = [[dot(b1, b1), dot(b1, b2)], [dot(b2, b1), dot(b2, b2)]]
check("B", "Lambda basis Gram matrix = [[2,-1],[-1,2]] (equal lengths, 120 deg): hexagonal lattice",
      gram_L == [[2, -1], [-1, 2]], gram_L)
# kernel of the exponential map: theta in plane with exp(2 pi i theta_k)=1 for all k  <=>  theta in Z^3
# (and every diag(e1,e2,e3) with e1 e2 e3 = 1 is hit by theta = (t1, t2, -t1-t2)); this is the
# statement T = plane / Lambda.  Exact content checked: Lambda = Z^3 ∩ plane has basis b1, b2:
ok = True
for v in itertools.product(range(-3, 4), repeat=3):
    if sum(v) == 0:
        a, b = lam2(tuple(F(x) for x in v))
        ok &= (a.denominator == 1 and b.denominator == 1 and vadd(vscal(a, b1), vscal(b, b2)) == tuple(F(x) for x in v))
check("B", "every integer vector in the plane is an integer combination of b1, b2 (Lambda = Z^3 ∩ plane)", ok)

# weight lattice = dual of Lambda inside the plane
w1, w2 = (F(2, 3), F(-1, 3), F(-1, 3)), (F(1, 3), F(1, 3), F(-2, 3))
check("B", "fundamental weights are dual to b1, b2: <w_i, b_j> = delta_ij",
      [[dot(w, b) for b in (b1, b2)] for w in (w1, w2)] == [[1, 0], [0, 1]])
gram_W = [[dot(w1, w1), dot(w1, w2)], [dot(w2, w1), dot(w2, w2)]]
check("B", "weight-lattice Gram = (1/3)[[2,1],[1,2]] (equal lengths, 60 deg): hexagonal",
      gram_W == [[F(2, 3), F(1, 3)], [F(1, 3), F(2, 3)]], gram_W)
# octet = 3 x 3bar - 1: weights e_i - e_j
E3 = [tuple(F(int(i == k)) for k in range(3)) for i in range(3)]
octet = Counter(vsub(E3[i], E3[j]) for i in range(3) for j in range(3))
octet[(F(0), F(0), F(0))] -= 1
nonzero = [v for v in octet if any(v)]
# regular hexagon, decided exactly without any angular sorting: each of the six vectors has norm^2 2,
# exactly two neighbours at 60 deg (dot 1), two at 120 deg (dot -1) and one opposite (dot -2)
dots_ok = all(sorted(dot(v, w) for w in nonzero if w != v) == [-2, -1, -1, 1, 1] for v in nonzero)
hexagon_ok = (len(nonzero) == 6 and octet[(F(0), F(0), F(0))] == 2
              and all(dot(v, v) == 2 for v in nonzero) and dots_ok)
check("B", "octet weights: six nonzero weights of equal length forming a regular hexagon "
           "(each has two neighbours at 60 deg, two at 120 deg, one opposite), zero weight with multiplicity 2",
      hexagon_ok)
dec = Counter()
for a, b, c in itertools.product(range(4), repeat=3):
    if a + b + c == 3:
        dec[(F(a - 1), F(b - 1), F(c - 1))] += 1
corners = [(F(2), F(-1), F(-1)), (F(-1), F(2), F(-1)), (F(-1), F(-1), F(2))]
tri_ok = (sum(dec.values()) == 10 and all(m == 1 for m in dec.values())
          and all(dot(vsub(corners[i], corners[j]), vsub(corners[i], corners[j])) == 18
                  for i in range(3) for j in range(3) if i < j))
# every weight = convex combination of the corners with weights (a/3, b/3, c/3) >= 0 : a triangle, 4 weights per side
side = sum(1 for (a, b, c) in [(int(v[0]) + 1, int(v[1]) + 1, int(v[2]) + 1) for v in dec] if c == 0)
check("B", "decuplet (Sym^3 of the 3) weights: 10 simple weights filling an equilateral triangle, 4 per side",
      tri_ok and side == 4)

# ---- the seven points ----
p = (F(1, 7), F(2, 7), F(-3, 7))              # exp(2 pi i p) = diag(z, z^2, z^4) = D


def label(v):
    for j in range(7):
        if in_Lambda(vsub(v, vscal(j, p))):
            return j
    return None


def turn(v):                                   # hexagon_check: np.roll(v, 1)
    return (v[2], v[0], v[1])


check("B", "the seven powers D^j (j=0..6) are seven distinct points of plane/Lambda, and 7p is in Lambda",
      [label(vscal(j, p)) for j in range(7)] == list(range(7)) and in_Lambda(vscal(7, p)))
k_turn = label(turn(p))
check("B", "120 deg turn (theta -> roll(theta)) sends point 1 to point 4", k_turn == 4, f"label = {k_turn}")
REPLICA.append(f"120° turn sends point 1 to point {k_turn}")

# finer lattice L' = Lambda + Z p ; basis {p, tp}
tp = turn(p)
M2 = [[lam2(p)[0], lam2(tp)[0]], [lam2(p)[1], lam2(tp)[1]]]
detM2 = M2[0][0] * M2[1][1] - M2[0][1] * M2[1][0]


def solve2(M, rhs):
    d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    return ((rhs[0] * M[1][1] - M[0][1] * rhs[1]) / d, (M[0][0] * rhs[1] - M[1][0] * rhs[0]) / d)


coef_b1, coef_b2 = solve2(M2, lam2(b1)), solve2(M2, lam2(b2))
check("B", "Lambda ⊂ Z p + Z tp (b1, b2 are integer combinations), tp = 4p - (1,1,-2): so L' = Z p + Z tp",
      all(c.denominator == 1 for c in coef_b1 + coef_b2) and in_Lambda(vsub(vscal(4, p), tp)),
      f"b1 = {coef_b1[0]}p + {coef_b1[1]}tp, b2 = {coef_b2[0]}p + {coef_b2[1]}tp")
check("B", "index [L' : Lambda] = 7 (|det| of (p,tp) in Lambda coordinates = 1/7)", abs(detM2) == F(1, 7), detM2)
gram_Lp = [[dot(p, p), dot(p, tp)], [dot(tp, p), dot(tp, tp)]]
check("B", "Gram(p, tp) = (1/7)[[2,-1],[-1,2]]: the finer lattice is hexagonal, scaled by 1/sqrt7",
      gram_Lp == [[F(2, 7), F(-1, 7)], [F(-1, 7), F(2, 7)]], gram_Lp)
# shortest vectors: norm^2(m p + n tp) = (2/7)(m^2 - m n + n^2) >= (2/7)(3/4)max(|m|,|n|)^2 ; |m|,|n| <= 4 is ample
short = {}
for m_, n_ in itertools.product(range(-4, 5), repeat=2):
    v = vadd(vscal(m_, p), vscal(n_, tp))
    if any(v):
        short.setdefault(dot(v, v), []).append(v)
mn = min(short)
steps = short[mn]
check("B", "the finer lattice has minimal norm^2 2/7, attained by exactly 6 vectors (+-p, +-tp, +-(p+tp))",
      mn == F(2, 7) and len(steps) == 6 and set(steps) == {p, vscal(-1, p), tp, vscal(-1, tp), vadd(p, tp),
                                                            vscal(-1, vadd(p, tp))})
ring_labels = sorted(label(v) for v in steps)
check("B", "the six neighbours of point 0 carry labels 1..6 (every point touches every other: K7)",
      ring_labels == [1, 2, 3, 4, 5, 6], ring_labels)
REPLICA.append(f"neighbours of point 0: {ring_labels} -> every point touches every other (K7)")

# triangles of the triangular lattice with 60-degree basis a = p, c = p + tp
a_v, c_v = p, vadd(p, tp)
check("B", "a = p and c = p + tp: equal length, 60 deg (|a|^2 = |c|^2 = 2/7, a.c = 1/7)",
      dot(a_v, a_v) == dot(c_v, c_v) == F(2, 7) and dot(a_v, c_v) == F(1, 7))
up, down = [], []          # oriented (counter-clockwise) label triples
o_up = lam2(a_v)[0] * lam2(c_v)[1] - lam2(a_v)[1] * lam2(c_v)[0]          # orientation sign of (a, c)
for j in range(7):
    x0 = vscal(j, p)
    tri_u = [x0, vadd(x0, a_v), vadd(x0, c_v)]
    tri_d = [vadd(x0, a_v), vadd(vadd(x0, a_v), c_v), vadd(x0, c_v)]
    up.append(tuple(label(v) for v in tri_u))
    down.append(tuple(label(v) for v in tri_d))


def orient_sign(tri_pts):
    (x1, y1), (x2, y2), (x3, y3) = (lam2(v) for v in tri_pts)
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)


# both families listed with the same orientation sign as (a, c)
same_orient = all(orient_sign([vscal(j, p), vadd(vscal(j, p), a_v), vadd(vscal(j, p), c_v)]) * o_up > 0 and
                  orient_sign([vadd(vscal(j, p), a_v), vadd(vadd(vscal(j, p), a_v), c_v), vadd(vscal(j, p), c_v)]) * o_up > 0
                  for j in range(7))
A = {tuple(sorted(t)) for t in up}
B = {tuple(sorted(t)) for t in down}
octonion = {tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)}


def is_fano(S):
    pairs = [pr for tri in S for pr in itertools.combinations(sorted(tri), 2)]
    return len(S) == 7 and len(pairs) == len(set(pairs)) == 21


check("B", "14 distinct triangles in two families of 7 (up / down triangles of the finer lattice)",
      len(A) == 7 and len(B) == 7 and len(A | B) == 14, f"up = {sorted(A)}; down = {sorted(B)}")
check("B", "family 'up' is a Fano plane, family 'down' is a Fano plane", is_fano(A) and is_fano(B))
which = "down" if B == octonion else ("up" if A == octonion else "none")
check("B", "one family is exactly the octonion lines {i, i+1, i+3}", which != "none", f"it is the '{which}' family")
REPLICA.append(f"triangles: {len(A | B)} | family A Fano: {is_fano(A)} | family B Fano: {is_fano(B)}")
REPLICA.append(f"one family is the octonion lines {{i, i+1, i+3}}: {octonion in (A, B)}")

# ---- the triangulated surface ----
T14 = A | B
edges = Counter(pr for tri in T14 for pr in itertools.combinations(tri, 2))
check("B", "21 edges = all pairs of 7 labels, each edge in exactly 2 triangles",
      len(edges) == 21 and set(edges.values()) == {2})


def links_are_cycles(T):
    for v in range(7):
        lk = [tuple(x for x in tri if x != v) for tri in T if v in tri]
        adj = {}
        for x, y in lk:
            adj.setdefault(x, []).append(y)
            adj.setdefault(y, []).append(x)
        if any(len(n) != 2 for n in adj.values()):
            return False
        start = next(iter(adj))
        seen, prev, cur = {start}, None, start
        while True:
            nxt = [y for y in adj[cur] if y != prev][0]
            if nxt == start:
                break
            seen.add(nxt)
            prev, cur = cur, nxt
        if len(seen) != len(adj):
            return False
    return True


oriented = up + down
dir_edges = Counter((t[i], t[(i + 1) % 3]) for t in oriented for i in range(3))
check("B", "every vertex link is a single 6-cycle (a closed surface)", links_are_cycles(T14))
check("B", "orientable: with the plane's orientation each directed edge occurs exactly once",
      same_orient and len(dir_edges) == 42 and set(dir_edges.values()) == {1})
V_, E_, F_ = 7, len(edges), len(T14)
check("B", "Euler characteristic V - E + F = 7 - 21 + 14 = 0 (orientable, chi = 0: a torus)",
      (V_, E_, F_) == (7, 21, 14) and V_ - E_ + F_ == 0, f"{V_} - {E_} + {F_} = {V_ - E_ + F_}")
mobius = ({tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)} |
          {tuple(sorted((i % 7, (i + 2) % 7, (i + 3) % 7))) for i in range(7)})
check("B", "the triangulation equals the Moebius/Csaszar torus labelling {i,i+1,i+3} ∪ {i,i+2,i+3}", T14 == mobius)
VALUES["triangulation"] = dict(V=V_, E=E_, F=F_, chi=V_ - E_ + F_, octonion_family=which)

# ---- uniqueness of the 7-vertex torus triangulation (exhaustive) ----
all_tris = list(itertools.combinations(range(7), 3))
all_pairs = list(itertools.combinations(range(7), 2))


def enumerate_degree2_complexes():
    """all sets of triangles on 7 labels in which every pair lies in exactly 2 triangles."""
    sols = []
    cnt = {pr: 0 for pr in all_pairs}
    chosen = []

    def tri_edges(t):
        return [(t[0], t[1]), (t[0], t[2]), (t[1], t[2])]

    def rec():
        e = next((pr for pr in all_pairs if cnt[pr] < 2), None)
        if e is None:
            sols.append(frozenset(chosen))
            return
        need = 2 - cnt[e]
        cands = [tuple(sorted(e + (k,))) for k in range(7) if k not in e]
        cands = [t for t in cands if t not in chosen and all(cnt[x] < 2 for x in tri_edges(t))]
        for combo in itertools.combinations(cands, need):
            ok_ = True
            for t in combo:
                for x in tri_edges(t):
                    cnt[x] += 1
                    if cnt[x] > 2:
                        ok_ = False
            if ok_:
                chosen.extend(combo)
                rec()
                del chosen[-need:]
            for t in combo:
                for x in tri_edges(t):
                    cnt[x] -= 1
    rec()
    return sols


def orientable(T):
    T = list(T)
    orient = {T[0]: T[0]}
    stack = [T[0]]
    while stack:
        t = stack.pop()
        ot = orient[t]
        de = {(ot[i], ot[(i + 1) % 3]) for i in range(3)}
        for s in T:
            if s in orient or len(set(s) & set(t)) != 2:
                continue
            x, y = sorted(set(s) & set(t))
            third = [w for w in s if w not in (x, y)][0]
            # orient s so that the shared edge is traversed opposite to t
            if (x, y) in de:
                os_ = (y, x, third)
            else:
                os_ = (x, y, third)
            orient[s] = os_
            stack.append(s)
    if len(orient) != len(T):
        return False
    dirs = Counter((o[i], o[(i + 1) % 3]) for o in orient.values() for i in range(3))
    return set(dirs.values()) == {1}


cands = enumerate_degree2_complexes()
surfaces = [T for T in cands if links_are_cycles(T)]
tori = [T for T in surfaces if orientable(T)]
perms7 = list(itertools.permutations(range(7)))


def apply_perm(s, T):
    return frozenset(tuple(sorted(s[x] for x in t)) for t in T)


orbit_T14 = {apply_perm(s, T14) for s in perms7}
aut_T14 = [s for s in perms7 if apply_perm(s, T14) == frozenset(T14)]
# orientation behaviour of automorphisms
or_set = {(t[0], t[1], t[2]) for t in oriented}


def preserves_orientation(s):
    imgs = [(s[t[0]], s[t[1]], s[t[2]]) for t in oriented]
    cyc = lambda t: {(t[0], t[1], t[2]), (t[1], t[2], t[0]), (t[2], t[0], t[1])}
    return all(cyc(i) & or_set for i in imgs)


n_orient_pres = sum(preserves_orientation(s) for s in aut_T14)
affine42 = {tuple((a * x + b) % 7 for x in range(7)) for a in range(1, 7) for b in range(7)}
# Scope of the search (reworded in the reconciliation, Oct 19): on V = 7 vertices a closed triangulated surface has
# 3F = 2E and E <= C(7,2) = 21, so chi = 7 - E/3 >= 0, with chi = 0 iff E = 21, i.e. iff every vertex pair is an
# edge lying in exactly 2 triangles.  The pair-degree-2 enumeration is therefore exhaustive for chi = 0 ONLY;
# 7-vertex spheres (chi 2) and projective planes (chi 1) exist and are not in it (examples built below).
check("B", "exhaustive search: every 7-vertex triangulated surface with chi = 0 (= every vertex pair in exactly 2 "
           "triangles) is an orientable torus -- so no 7-vertex Klein bottle -- and they form ONE relabelling orbit "
           "(the 7-vertex torus triangulation is unique)",
      len(surfaces) == len(tori) == len(orbit_T14) and set(surfaces) == orbit_T14,
      f"{len(cands)} pair-degree-2 complexes, {len(surfaces)} surfaces, {len(tori)} orientable, "
      f"orbit of ours = {len(orbit_T14)}")


def surface_data(T):
    E_set = {pr for tri in T for pr in itertools.combinations(sorted(tri), 2)}
    deg2 = all(sum(1 for tri in T if set(pr) <= set(tri)) == 2 for pr in E_set)
    nv = len({x for tri in T for x in tri})
    return nv, len(E_set), len(T), nv - len(E_set) + len(T), deg2 and links_are_cycles(T), orientable(T)


# pentagonal bipyramid: apexes 0 and 6 over the ring 1..5 (a 7-vertex sphere)
bipyramid = frozenset({tuple(sorted((0, i, i % 5 + 1))) for i in range(1, 6)} |
                      {tuple(sorted((6, i, i % 5 + 1))) for i in range(1, 6)})
# 6-vertex projective plane (hemi-icosahedron), with triangle (0,1,2) subdivided by vertex 6 (a 7-vertex RP^2)
rp2_6 = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 1, 5), (1, 2, 4), (2, 3, 5), (1, 3, 4), (2, 4, 5), (1, 3, 5)]
rp2_7 = frozenset([t for t in rp2_6 if t != (0, 1, 2)] + [(0, 1, 6), (1, 2, 6), (0, 2, 6)])
sph, rp2 = surface_data(bipyramid), surface_data(rp2_7)
check("B", "the search above does not cover all 7-vertex surfaces: a 7-vertex sphere (pentagonal bipyramid, "
           "V-E+F = 7-15+10 = 2, orientable) and a 7-vertex projective plane (V-E+F = 7-18+12 = 1, non-orientable) exist",
      sph == (7, 15, 10, 2, True, True) and rp2 == (7, 18, 12, 1, True, False),
      f"sphere (V,E,F,chi,surface,orientable) = {sph}; RP^2 = {rp2}")
check("B", "automorphism group of the triangulation has order 42 and equals {x -> ax+b : a in Z7*} = AGL(1,7)",
      len(aut_T14) == 42 and set(aut_T14) == affine42, f"|Aut| = {len(aut_T14)}")
check("B", "all 42 automorphisms preserve orientation: the 7-vertex torus is chiral (no mirror symmetry)",
      n_orient_pres == 42, f"{n_orient_pres} of {len(aut_T14)} orientation-preserving")
VALUES["torus7_uniqueness"] = dict(degree2_complexes=len(cands), surfaces=len(surfaces), orientable=len(tori),
                                   orbit=len(orbit_T14), aut_order=len(aut_T14),
                                   orientation_preserving=n_orient_pres,
                                   scope="7-vertex surfaces with chi = 0 only (chi = 0 <=> every pair in exactly 2 "
                                         "triangles); 7-vertex spheres and RP^2s exist and are outside the search",
                                   sphere_example=list(sph), rp2_example=list(rp2))


def image(S, a_, b_):
    return {tuple(sorted((a_ * x + b_) % 7 for x in tri)) for tri in S}


pres = all(image(S, a_, b_) == S for S in (A, B) for a_ in (1, 2, 4) for b_ in range(7))
swap = all(image(A, a_, b_) == B and image(B, a_, b_) == A for a_ in (3, 5, 6) for b_ in range(7))
check("B", "x -> ax+b with a in {1,2,4} preserves both families", pres)
check("B", "x -> ax+b with a in {3,5,6} swaps the two families", swap)
REPLICA.append(f"x -> ax+b (a in 1,2,4) preserves both families: {pres}")

# ---- all Fano planes on 7 labels; the cyclic ones; their collineation groups ----


def all_fano_planes():
    sols = []
    cover = {pr: False for pr in all_pairs}
    lines = []

    def rec():
        e = next((pr for pr in all_pairs if not cover[pr]), None)
        if e is None:
            sols.append(frozenset(lines))
            return
        for k in range(7):
            if k in e:
                continue
            t = tuple(sorted(e + (k,)))
            prs = list(itertools.combinations(t, 2))
            if any(cover[x] for x in prs):
                continue
            for x in prs:
                cover[x] = True
            lines.append(t)
            rec()
            lines.pop()
            for x in prs:
                cover[x] = False
    rec()
    return sols


fanos = all_fano_planes()
shift = tuple((x + 1) % 7 for x in range(7))
cyclic = [S for S in fanos if apply_perm(shift, S) == S]
check("B", "there are exactly 30 Fano planes on 7 labels", len(fanos) == 30, len(fanos))
check("B", "exactly 2 of them are kept by x -> x+1, and they are exactly the two torus families",
      len(cyclic) == 2 and set(cyclic) == {frozenset(A), frozenset(B)}, len(cyclic))
REPLICA.append(f"Fano planes on Z7 kept by x -> x+1: {len(cyclic)} | the torus families are exactly these: "
               f"{set(cyclic) == {frozenset(A), frozenset(B)}}")
autA = {s for s in perms7 if apply_perm(s, A) == frozenset(A)}
autB = {s for s in perms7 if apply_perm(s, B) == frozenset(B)}
f21_labels = {tuple((a_ * x + b_) % 7 for x in range(7)) for a_ in (1, 2, 4) for b_ in range(7)}
check("B", "each family's collineation group has order 168; their intersection is exactly "
           "{x -> ax+b : a in {1,2,4}} (order 21)",
      len(autA) == len(autB) == 168 and (autA & autB) == f21_labels, f"|Aut A ∩ Aut B| = {len(autA & autB)}")
VALUES["fano"] = dict(total=len(fanos), cyclic=len(cyclic), aut_order=len(autA), aut_intersection=len(autA & autB))

# ---- which order-7 points of the torus give a hexagonal finer lattice? (extra) ----


def reduced_gram(u, v):
    """Lagrange-Gauss reduction of a 2D lattice basis (exact)."""
    while True:
        if dot(u, u) > dot(v, v):
            u, v = v, u
        mu = dot(u, v) / dot(u, u)
        r = (mu.numerator * 2 + mu.denominator) // (2 * mu.denominator)      # nearest integer
        if r == 0:
            break
        v = vsub(v, vscal(r, u))
    return (dot(u, u), dot(u, v), dot(v, v))


hexpts, subgroups7 = [], set()
for a_, b_ in itertools.product(range(7), repeat=2):
    if (a_, b_) == (0, 0):
        continue
    q = (F(a_, 7), F(b_, 7), F(-a_ - b_, 7))
    # basis of Lambda + Z q (index 7): in Lambda coordinates q = (al, be); rescale q by k so that one
    # coordinate becomes 1/7 mod 1, then {kq mod Lambda, complementary Lambda vector} is a basis (|det| = 1/7)
    al, be = lam2(q)
    if (al * 7) % 7 != 0:
        k = next(k for k in range(1, 7) if (k * int(al * 7)) % 7 == 1)
        qq = (k * al - (k * al - F(1, 7)), k * be - ((k * be) // 1))
        basis2 = [qq, (F(0), F(1))]
    else:
        k = next(k for k in range(1, 7) if (k * int(be * 7)) % 7 == 1)
        qq = (k * al - ((k * al) // 1), k * be - (k * be - F(1, 7)))
        basis2 = [(F(1), F(0)), qq]
    d = basis2[0][0] * basis2[1][1] - basis2[0][1] * basis2[1][0]
    assert abs(d) == F(1, 7)
    basis = tuple(vadd(vscal(x[0], b1), vscal(x[1], b2)) for x in basis2)
    assert in_Lambda(vsub(basis[0] if (al * 7) % 7 != 0 else basis[1], vscal(k, q)))
    g11, g12, g22 = reduced_gram(*basis)
    is_hex = (g11 == g22 and 2 * abs(g12) == g11)
    key = frozenset(((k * a_) % 7, (k * b_) % 7) for k in range(1, 7))
    if is_hex:
        hexpts.append((a_, b_))
        subgroups7.add(key)
check("B", "(extra) of the 48 order-7 points of the torus, exactly 12 (two subgroups of order 7) have a "
           "hexagonal finer lattice: those of D=diag(z,z^2,z^4) and of diag(z,z^4,z^2)",
      len(hexpts) == 12 and len(subgroups7) == 2 and (1, 2) in hexpts and (1, 4) in hexpts,
      f"{len(hexpts)} points, {len(subgroups7)} subgroups")
VALUES["order7_points_with_hexagonal_finer_lattice"] = dict(value=len(hexpts), of=48, subgroups=len(subgroups7))


# =============================================================================
# C. The finite groups inside SU(3), exactly over Q(zeta7)
# =============================================================================
header("C. F21 and the two copies of PSL(2,7) inside SU(3) (exact over Q(zeta7))")
O_, I_ = ZERO7, ONE7
ID3 = identity(3, I_, O_)


def diagm(a_, b_, c_):
    return mat([[a_, O_, O_], [O_, b_, O_], [O_, O_, c_]])


def scal_m(s, M):
    return tuple(tuple(s * x for x in r) for r in M)


def is_unitary(M):
    return mmul(M, conjT(M)) == ID3


def in_su3(M):
    return is_unitary(M) and det3(M) == I_


def mpow(M, n):
    R_ = ID3
    for _ in range(n):
        R_ = mmul(R_, M)
    return R_


def morder(M, cap=50):
    X = M
    for k in range(1, cap + 1):
        if X == ID3:
            return k
        X = mmul(X, M)
    return None


D = diagm(z(1), z(2), z(4))
Dk = diagm(z(4), z(2), z(1))
C = mat([[O_, I_, O_], [O_, O_, I_], [I_, O_, O_]])
R = scal_m(I_SQRT7, mat([[z(1) - z(6), z(2) - z(5), z(4) - z(3)],
                         [z(2) - z(5), z(4) - z(3), z(1) - z(6)],
                         [z(4) - z(3), z(1) - z(6), z(2) - z(5)]]))
flip = scal_m(Z7.rat(-1), mat([[O_, O_, I_], [O_, I_, O_], [I_, O_, O_]]))
check("C", "D in SU(3), D^7 = 1 (order 7)", in_su3(D) and morder(D) == 7)
check("C", "C (cyclic permutation) in SU(3), order 3; Klein's R in SU(3), R^2 = 1",
      in_su3(C) and morder(C) == 3 and in_su3(R) and morder(R) == 2)
Cinv = conjT(C)
check("C", "the Weyl 3-cycle acts on the torus by conjugation: C^-1 D C = D^4 and C D C^-1 = D^2",
      mmul(mmul(Cinv, D), C) == mpow(D, 4) and mmul(mmul(C, D), Cinv) == mpow(D, 2))

# ---- F21 ----
F21 = FiniteGroup([D, C], mmul, mkey, ID3)
f21_su3 = all(in_su3(M) for M in F21.elems)
check("C", "|<D, C>| = 21 and every element is in SU(3) (exact unitarity and det = 1)",
      len(F21) == 21 and f21_su3, len(F21))
REPLICA.append(f"|<D, 120° turn>| = {len(F21)} | inside SU(3): {f21_su3}")
nonab = mmul(D, C) != mmul(C, D)
z7sub = {mkey(mpow(D, j)) for j in range(7)}
normal7 = all(mkey(mmul(mmul(conjT(g), mpow(D, 1)), g)) in z7sub for g in F21.elems)
check("C", "F21 is non-abelian with normal Z7 = <D>: F21 = Z7 ⋊ Z3 (C^-1 D C = D^4, the LNR presentation)",
      nonab and normal7)


def char_data(Gp, name):
    """classes, orders, character values (traces), FS indicator, <chi,chi>, <chi,chibar>; all exact."""
    tbl = Gp.table
    n = Gp.n
    classes = Gp.conj_classes()
    tr = [trace(M) for M in Gp.elems]
    ip = sum((tr[i] * tr[i].conj() for i in range(n)), Z7.rat(0)) * F(1, n)
    ipbar = sum((tr[i] * tr[i] for i in range(n)), Z7.rat(0)) * F(1, n)
    fs = sum((tr[tbl[i][i]] for i in range(n)), Z7.rat(0)) * F(1, n)
    rows = []
    for cl in classes:
        rep = cl[0]
        vals = {tr[i] for i in cl}
        assert len(vals) == 1
        rows.append(dict(size=len(cl), order=Gp.order_of(rep), chi=tr[rep]))
    rows.sort(key=lambda r: (r["order"], -r["size"]))
    return classes, rows, ip, ipbar, fs


def chi_str(x):
    if x == b7:
        return "b7"
    if x == b7bar:
        return "b7bar"
    if x.is_rational():
        return str(x.to_fraction())
    return repr(x)


cl21, rows21, ip21, ipb21, fs21 = char_data(F21, "F21")
sig21 = [(r["size"], r["order"], chi_str(r["chi"])) for r in rows21]
check("C", "F21 classes (size, order, chi_3): 1,7,7 (orders 1,3,3; chi 3,0,0) and 3,3 (order 7; chi b7, b7bar) "
           "-- the LNR table", sorted(sig21) == sorted([(1, 1, "3"), (7, 3, "0"), (7, 3, "0"), (3, 7, "b7"),
                                                       (3, 7, "b7bar")]), sig21)
check("C", "F21 triplet: <chi,chi> = 1 (irreducible), <chi,chibar> = 0 (3 not equivalent to 3bar), "
           "Frobenius-Schur indicator 0 (complex)", ip21 == I_ and ipb21 == O_ and fs21 == O_,
      f"<chi,chi>={chi_str(ip21)}, <chi,chibar>={chi_str(ipb21)}, FS={chi_str(fs21)}")
check("C", "chi(D) = b7 = (-1 + i sqrt7)/2 exactly", trace(D) == b7)

# ---- Klein's copy ----
PSLk = FiniteGroup([Dk, C, R], mmul, mkey, ID3)
psk_su3 = all(in_su3(M) for M in PSLk.elems)
check("C", "|<Dk, C, R>| = 168 (Klein's matrices) and every element is in SU(3)", len(PSLk) == 168 and psk_su3,
      len(PSLk))
REPLICA.append(f"|<Klein's matrices>| = {len(PSLk)} | inside SU(3): {psk_su3}")

# ---- exact polynomial arithmetic for the quartics ----


def padd(P, Q):
    out = dict(P)
    for k, v in Q.items():
        out[k] = out[k] + v if k in out else v
        if out[k].is_zero():
            del out[k]
    return out


def pmul(P, Q):
    out = {}
    for k1, v1 in P.items():
        for k2, v2 in Q.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            v = v1 * v2
            out[k] = out[k] + v if k in out else v
    return {k: v for k, v in out.items() if not v.is_zero()}


def linforms(M):
    """the three coordinates of M v as linear polynomials in v = (x, y, z)."""
    unit = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    return [{unit[c]: M[r][c] for c in range(3) if not M[r][c].is_zero()} for r in range(3)]


def cube(P):
    return pmul(pmul(P, P), P)


def klein_q(L):          # x^3 y + y^3 z + z^3 x
    return padd(padd(pmul(cube(L[0]), L[1]), pmul(cube(L[1]), L[2])), pmul(cube(L[2]), L[0]))


def mirror_q(L):         # x y^3 + y z^3 + z x^3
    return padd(padd(pmul(L[0], cube(L[1])), pmul(L[1], cube(L[2]))), pmul(L[2], cube(L[0])))


K0 = klein_q(linforms(ID3))
M0 = mirror_q(linforms(ID3))
kq_gens = all(klein_q(linforms(M)) == K0 for M in (Dk, C, R))
kq_all = all(klein_q(linforms(M)) == K0 for M in PSLk.elems)
check("C", "Klein quartic x^3y + y^3z + z^3x is invariant (exact polynomial identity) under Dk, C, R "
           "and under all 168 elements", kq_gens and kq_all)
REPLICA.append(f"Klein quartic preserved by the generators: {kq_gens}")
KD = klein_q(linforms(D))
ratios = {k: (KD[k] / K0[k]) for k in K0 if k in KD}
check("C", "D does not preserve the Klein quartic, not even up to a scalar (monomials pick up z^5, z^3, z^6)",
      len(set(ratios.values())) > 1 and KD != K0,
      {f"x^{k[0]}y^{k[1]}z^{k[2]}": repr(v) for k, v in ratios.items()})
# which order-7 diagonal elements of SU(3) keep each quartic? (a property of the quartic, independent of history)
diag_keep_K, diag_keep_M = [], []
for a_, b_ in itertools.product(range(7), repeat=2):
    c_ = (-a_ - b_) % 7
    if (a_, b_) == (0, 0):
        continue
    Md = diagm(z(a_), z(b_), z(c_))
    if klein_q(linforms(Md)) == K0:
        diag_keep_K.append((a_, b_, c_))
    if mirror_q(linforms(Md)) == M0:
        diag_keep_M.append((a_, b_, c_))
check("C", "the non-trivial diagonal SU(3) elements diag(z^a, z^b, z^c) keeping x^3y+y^3z+z^3x are exactly the powers of "
           "Dk = diag(z^4,z^2,z); those keeping xy^3+yz^3+zx^3 are exactly the powers of D",
      sorted(diag_keep_K) == sorted(((4 * k) % 7, (2 * k) % 7, k % 7) for k in range(1, 7))
      and sorted(diag_keep_M) == sorted((k % 7, (2 * k) % 7, (4 * k) % 7) for k in range(1, 7)),
      f"{len(diag_keep_K)} and {len(diag_keep_M)} elements")
f21_in_k = all(PSLk.contains(M) for M in F21.elems)
check("C", "<D, C> is NOT inside Klein's copy (D itself is not)", (not f21_in_k) and not PSLk.contains(D))
REPLICA.append(f"<D, 120° turn> inside Klein's own copy: {f21_in_k}")

# ---- the flipped copy ----
flip_su3 = in_su3(flip)
flip_inv = conjT(flip)
check("C", "flip = -(x<->z) is in SU(3) and is an involution", flip_su3 and mmul(flip, flip) == ID3)
sends = mmul(mmul(flip, Dk), flip_inv) == D
REPLICA.append(f"flip in SU(3): {flip_su3} | flip sends Dk to D: {sends}")
check("C", "flip Dk flip^-1 = D", sends)
Rf = mmul(mmul(flip, R), flip_inv)
PSLf = FiniteGroup([D, C, Rf], mmul, mkey, ID3)
psf_su3 = all(in_su3(M) for M in PSLf.elems)
f21_in_f = all(PSLf.contains(M) for M in F21.elems)
check("C", "flipped copy <D, C, Rf>: order 168, inside SU(3), contains <D, C>",
      len(PSLf) == 168 and psf_su3 and f21_in_f, len(PSLf))
REPLICA.append(f"flipped copy: order {len(PSLf)} | inside SU(3): {psf_su3} | holds <D, 120° turn>: {f21_in_f}")
conj_set = {mkey(mmul(mmul(flip, M), flip_inv)) for M in PSLk.elems}
check("C", "the flipped copy equals flip·(Klein's copy)·flip^-1 element by element (as sets)",
      conj_set == set(PSLf.index))
mq_gens = all(mirror_q(linforms(M)) == M0 for M in (D, C, Rf))
mq_all = all(mirror_q(linforms(M)) == M0 for M in PSLf.elems)
check("C", "mirror quartic xy^3 + yz^3 + zx^3 invariant (exact) under D, C, Rf and all 168 elements", mq_gens and mq_all)
REPLICA.append(f"flipped copy preserves the mirror quartic xy³ + yz³ + zx³: {mq_gens}")
f21_idx = frozenset(PSLf.find(M) for M in F21.elems)
iD, iC = PSLf.find(D), PSLf.find(C)
maximal21 = all(len(PSLf.closure([iD, iC, g])) == 168 for g in range(168) if g not in f21_idx)
check("C", "order-21 group maximal in the flipped copy: <D, C, g> = whole group for each of the 147 g outside it",
      maximal21)
REPLICA.append(f"order-21 group maximal in it: {maximal21}")

# ---- LNR's published basis (arXiv:0709.1447 eqs. 16, 22, 23, read in the source) ----
e = z
B_LNR = scal_m(I_SQRT7, mat([[e(3) - e(6), e(3) - e(1), e(1) - I_],
                             [e(2) - I_, e(6) - e(5), e(6) - e(2)],
                             [e(5) - e(4), e(4) - I_, e(5) - e(3)]]))
A_LNR = scal_m(I_SQRT7, mat([[e(2) - e(5), e(1) - e(6), e(4) - e(3)],
                             [e(1) - e(6), e(4) - e(3), e(2) - e(5)],
                             [e(4) - e(3), e(2) - e(5), e(1) - e(6)]]))
comm = mmul(mmul(conjT(A_LNR), conjT(B_LNR)), mmul(A_LNR, B_LNR))
lnr_rel = (morder(A_LNR) == 2 and morder(B_LNR) == 3 and morder(mmul(A_LNR, B_LNR)) == 7 and morder(comm) == 4)
check("C", "LNR generators: A^2 = B^3 = (AB)^7 = [A,B]^4 = 1, AB = D, and A = Rf (Klein's involution, flipped)",
      lnr_rel and mmul(A_LNR, B_LNR) == D and A_LNR == Rf)
LNRg = FiniteGroup([A_LNR, B_LNR], mmul, mkey, ID3)
check("C", "LNR's <A, B> is exactly the flipped copy (same 168 matrices)", set(LNRg.index) == set(PSLf.index),
      len(LNRg))
lnr_quartic = padd(padd(pmul(cube(linforms(ID3)[0]), linforms(ID3)[2]), pmul(cube(linforms(ID3)[2]), linforms(ID3)[1])),
                   pmul(cube(linforms(ID3)[1]), linforms(ID3)[0]))
check("C", "LNR's quartic invariant phi1^3 phi3 + phi3^3 phi2 + phi2^3 phi1 (their eq. 78) is the mirror quartic",
      lnr_quartic == M0)

# ---- structure and characters of PSL(2,7) (both copies) ----
psl_target = sorted([(1, 1, "3"), (21, 2, "-1"), (56, 3, "0"), (42, 4, "1"), (24, 7, "b7"), (24, 7, "b7bar")])
for name, Gp in (("Klein's copy", PSLk), ("flipped copy", PSLf)):
    cls, rows, ip, ipb, fs = char_data(Gp, name)
    sig = sorted((r["size"], r["order"], chi_str(r["chi"])) for r in rows)
    check("C", f"{name}: classes (size, order, chi_3) = (1,1,3) (21,2,-1) (56,3,0) (42,4,1) (24,7,b7) (24,7,b7bar)"
               " = LNR/ATLAS table", sig == psl_target, sig)
    check("C", f"{name}: <chi,chi> = 1, <chi,chibar> = 0, Frobenius-Schur indicator 0 (a complex triplet)",
          ip == I_ and ipb == O_ and fs == O_)
    center = [i for i in range(168) if all(Gp.table[i][g] == Gp.table[g][i] for g in range(168))]
    simple = all(len(Gp.closure(cl)) == 168 for cl in cls if cl != [0])
    check("C", f"{name}: trivial centre and simple (every non-identity class generates the whole group); a simple "
               "group of order 168 is PSL(2,7)", center == [0] and simple)
check("C", "flipped copy: chi(D) = b7 and chi(A B^2) = b7bar (LNR's classes C5(AB), C6(AB^2))",
      trace(D) == b7 and trace(mmul(A_LNR, mmul(B_LNR, B_LNR))) == b7bar)
VALUES["PSL27_triplet_character"] = dict(classes="1A,2A,3A,4A,7A,7B", sizes=[1, 21, 56, 42, 24, 24],
                                         chi=["3", "-1", "0", "1", "b7", "b7bar"], frobenius_schur=0)
VALUES["F21_triplet_character"] = dict(classes="1A,3A,3B,7A,7B", sizes=[1, 7, 7, 3, 3],
                                       chi=["3", "0", "0", "b7", "b7bar"], frobenius_schur=0)

# ---- the full subgroup lattice of the flipped copy (all 2-generated subgroups; completeness checked below) ----
tbl = PSLf.table
subs_gens = {frozenset([0]): (0,)}
for i in range(168):
    for j in range(i, 168):
        subs_gens.setdefault(PSLf.closure([i, j]), (i, j))
subs = list(subs_gens)
# completeness (added in the reconciliation, Oct 19): the list is closed under H -> <H, g> for every g.  Every
# subgroup K = <k1, ..., km> is reached from {1} by adding one element at a time, so the list holds ALL subgroups.
join_closed = all(PSLf.closure(list(subs_gens[H]) + [g]) in subs_gens for H in subs for g in range(168) if g not in H)
check("C", "the list of 2-generated subgroups is closed under adding any element (<H, g> is again in the list), so it "
           "contains every subgroup of PSL(2,7)", join_closed, f"{len(subs)} subgroups")
by_order = Counter(len(H) for H in subs)
proper = [H for H in subs if len(H) < 168]
maximal = [H for H in proper if not any(H < K for K in proper)]


def sub_classes(Hs):
    seen, out = set(), []
    for H in Hs:
        if H in seen:
            continue
        orb = {PSLf.conjugate_subgroup(H, g) for g in range(168)}
        seen |= orb
        out.append(sorted(orb, key=sorted))
    return out


max_classes = sub_classes(maximal)
all_classes = sub_classes(subs)


def order_profile(H):
    return dict(sorted(Counter(PSLf.order_of(h) for h in H).items()))


S4_profile = {1: 1, 2: 9, 3: 8, 4: 6}
max_summary = sorted((len(c[0]), len(c), str(order_profile(c[0]))) for c in max_classes)
check("C", "maximal subgroups of PSL(2,7): two classes of S4 (7 each) and one class of 7:3 (8 conjugates) -- ATLAS",
      sorted((len(c[0]), len(c)) for c in max_classes) == [(21, 8), (24, 7), (24, 7)]
      and all(order_profile(c[0]) == S4_profile for c in max_classes if len(c[0]) == 24),
      max_summary)
check("C", "F21 = <D, C> is one of the 8 maximal subgroups of order 21", f21_idx in maximal)
VALUES["PSL27_subgroups"] = dict(total=len(subs), conjugacy_classes=len(all_classes),
                                 by_order=dict(sorted(by_order.items())),
                                 maximal_classes=[dict(order=a_, conjugates=b_, element_orders=c_)
                                                  for a_, b_, c_ in max_summary])
print(f"    subgroups of PSL(2,7): {len(subs)} in {len(all_classes)} conjugacy classes; by order {dict(sorted(by_order.items()))}")

# ---- uniqueness of the PSL(2,7) in U(3) that contains <D, C> ----
normalizer = [g for g in range(168) if PSLf.conjugate_subgroup(f21_idx, g) == f21_idx]
D3 = mpow(D, 3)
rel_ok = (morder(D3) == 7 and mmul(mmul(Cinv, D3), C) == mpow(D3, 4)
          and len(FiniteGroup([D3, C], mmul, mkey, ID3)) == 21)
check("C", "N(F21) = F21 inside PSL(2,7); the order-21 subgroups form a single class",
      sorted(normalizer) == sorted(f21_idx) and any(len(c[0]) == 21 and len(c) == 8 for c in all_classes))
check("C", "D -> D^3, C -> C is an automorphism of F21 (relations hold) that sends chi(D) = b7 to chi(D^3) = b7bar,"
           " so it is not induced by any unitary conjugation", rel_ok and trace(D3) == b7bar)
conj_closed = {mkey(mconj(M)) for M in PSLf.elems} == set(PSLf.index)
check("C", "the flipped copy is closed under complex conjugation (as the uniqueness argument predicts)", conj_closed)

# ---- complex conjugation kappa extends PSL(2,7) to PGL(2,7) ----


def smul(X, Y):
    (M1, s1), (M2, s2) = X, Y
    return (mmul(M1, mconj(M2) if s1 else M2), s1 ^ s2)


def skey(X):
    return (mkey(X[0]), X[1])


PGL = FiniteGroup([(D, 0), (C, 0), (Rf, 0), (ID3, 1)], smul, skey, (ID3, 0))
lin_part = {mkey(X[0]) for X in PGL.elems if X[1] == 0}
# faithfulness of the conjugation action on PSLf: only the identity commutes with D, C, Rf
tblP = PGL.table
gidx = [PGL.find((g, 0)) for g in (D, C, Rf)]
cent = [x for x in range(PGL.n) if all(tblP[x][g] == tblP[g][x] for g in gidx)]
check("C", "<flipped copy, complex conjugation> has order 336, its linear part is the flipped copy, and it acts "
           "faithfully on PSL(2,7) by conjugation: it is Aut(PSL(2,7)) = PGL(2,7)",
      PGL.n == 336 and lin_part == set(PSLf.index) and cent == [0], f"order {PGL.n}")
s4_classes = [c for c in max_classes if len(c[0]) == 24]
H0 = s4_classes[0][0]
H0bar = frozenset(PSLf.find(mconj(PSLf.elems[h])) for h in H0)
check("C", "complex conjugation swaps the two classes of S4 (the outer automorphism of PSL(2,7))",
      H0bar in s4_classes[1] and H0bar not in s4_classes[0])
check("C", "complex conjugation acts on the torus as t -> t^-1, i.e. on the labels as x -> 6x (= -x), which swaps "
           "the Fano families", mconj(D) == mpow(D, 6) and image(A, 6, 0) == B and image(B, 6, 0) == A)

# ---- the two Fano families are the two S4 classes (points / lines) ----


def s4_action_group(cls):
    """action of the flipped copy on a class of 7 S4 subgroups, labelled via D and C like the torus points."""
    fixedC = [H for H in cls if PSLf.conjugate_subgroup(H, iC) == H]
    Hs0 = fixedC[0]
    Dm = [PSLf.find(mpow(D, j)) for j in range(7)]
    lab = {PSLf.conjugate_subgroup(Hs0, Dm[j]): j for j in range(7)}
    assert len(lab) == 7

    def perm_of(g):
        return tuple(lab[PSLf.conjugate_subgroup(H, g)] for H in sorted(lab, key=lambda H: lab[H]))
    gens_p = [perm_of(PSLf.find(M)) for M in (D, C, Rf)]
    Gp = {tuple(range(7))}
    frontier = list(Gp)
    while frontier:
        new = []
        for s in frontier:
            for g in gens_p:
                t = tuple(g[s[x]] for x in range(7))
                if t not in Gp:
                    Gp.add(t)
                    new.append(t)
        frontier = new
    return gens_p, Gp


acts = [s4_action_group(c) for c in s4_classes]
fam_of = []
for gens_p, Gp in acts:
    fam_of.append("up" if Gp == autA else ("down" if Gp == autB else "neither"))
check("C", "PSL(2,7) acting on each S4 class, labelled through D (x->x+1) and C (x->2x), is exactly the collineation "
           "group of one Fano family; the two classes give the two families",
      sorted(fam_of) == ["down", "up"] and all(g[0] == shift and g[1] == tuple((2 * x) % 7 for x in range(7))
                                               for g, _ in acts), fam_of)

# ---- computed replacements for facts previously used by citation (added in the reconciliation, Oct 19) ----
# (1) the only 3-dim irreps of PSL(2,7) are 3 and 3bar (was: LNR's character table)
inv_f = PSLf.inv
cls_f = PSLf.conj_classes()
derived_f = PSLf.closure({tbl[tbl[inv_f[x]][inv_f[y]]][tbl[x][y]] for x in range(168) for y in range(168)})
divs168 = [d_ for d_ in range(2, 13) if 168 % d_ == 0]                  # d^2 <= 149 forces d <= 12
rest168 = [(a_, b_, c_) for a_ in divs168 for b_ in divs168 for c_ in divs168
           if a_ <= b_ <= c_ and a_ * a_ + b_ * b_ + c_ * c_ == 168 - 1 - 9 - 9]
check("C", "degree equation: PSL(2,7) has 6 classes (6 irreps) and is perfect (derived subgroup = whole group, so 1 is "
           "its only linear character); with 3 and 3bar the other three degrees d >= 2, d | 168, sum d^2 = 149, are "
           "forced to be (6,7,8): 3 and 3bar are its only 3-dim irreps",
      len(cls_f) == 6 and len(derived_f) == 168 and rest168 == [(6, 7, 8)], rest168)

# (2) explicit isomorphisms onto PSL(2,F7) and PGL(2,F7) acting on the projective line P^1(F7) = {0..6, 7 = inf}
#     (was: "a simple group of order 168 is PSL(2,7)" and "|Aut PSL(2,7)| = 336")
ID8 = tuple(range(8))


def moebius(a_, b_, c_, d_):
    img = []
    for x in range(8):
        num, den = (a_ % 7, c_ % 7) if x == 7 else ((a_ * x + b_) % 7, (c_ * x + d_) % 7)
        img.append(7 if den == 0 else (num * pow(den, -1, 7)) % 7)
    return tuple(img)


def pcomp(p_, q_):                       # (p∘q)(x) = p(q(x)); moebius(M1 M2) = moebius(M1)∘moebius(M2)
    return tuple(p_[q_[x]] for x in range(8))


def porder(p_):
    k, q_ = 1, p_
    while q_ != ID8:
        q_, k = pcomp(q_, p_), k + 1
    return k


PGL27 = {}
for a_, b_, c_, d_ in itertools.product(range(7), repeat=4):
    det_ = (a_ * d_ - b_ * c_) % 7
    if det_:
        PGL27[moebius(a_, b_, c_, d_)] = det_ in (1, 2, 4)              # square determinant <=> PSL(2,F7)
PSL27 = {p_ for p_, sq in PGL27.items() if sq}


def graph_closure(Gp, gidx, perms, cap):
    """the subgroup of Gp x Sym(8) generated by the pairs (gidx[k], perms[k]); returns (size, second projection)."""
    t = Gp.table
    S = {(0, ID8)}
    frontier = list(S)
    while frontier:
        new = []
        for x, p_ in frontier:
            for gi, q_ in zip(gidx, perms):
                y = (t[x][gi], pcomp(p_, q_))
                if y not in S:
                    S.add(y)
                    new.append(y)
                    if len(S) > cap:
                        return len(S), None
        frontier = new
    return len(S), {p_ for _, p_ in S}


def iso_to_psl27(Gp, mats):
    """mats = (g0 of order 7, g1, g2): search images with g0 -> x+1 (finding one isomorphism suffices); a graph
    of size |Gp| = 168 whose image is all of PSL(2,F7) proves that the generator map extends to an isomorphism."""
    gidx = [Gp.find(M) for M in mats]
    t = Gp.table
    k7 = next(k for k in range(1, 7) if t[t[Gp.inv[gidx[1]]][gidx[0]]][gidx[1]] == Gp.find(mpow(mats[0], k)))
    d7 = moebius(1, 1, 0, 1)
    d7k = ID8
    for _ in range(k7):
        d7k = pcomp(d7k, d7)
    inv8 = lambda p_: tuple(sorted(range(8), key=lambda x: p_[x]))
    c_cands = [p_ for p_ in PSL27 if porder(p_) == Gp.order_of(gidx[1]) and pcomp(pcomp(inv8(p_), d7), p_) == d7k]
    r_cands = [p_ for p_ in PSL27 if porder(p_) == Gp.order_of(gidx[2])]
    for cp in sorted(c_cands):
        for rp in sorted(r_cands):
            n_, img = graph_closure(Gp, gidx, [d7, cp, rp], Gp.n)
            if n_ == Gp.n and img == PSL27:
                return [d7, cp, rp]
    return None


iso_k = iso_to_psl27(PSLk, (Dk, C, R))
iso_f = iso_to_psl27(PSLf, (D, C, Rf))
check("C", "explicit isomorphisms: Dk, C, R (Klein's copy) and D, C, Rf (flipped copy) map to Moebius maps of "
           "PSL(2,F7) on P^1(F7) so that the generated graph has order 168 and image all of PSL(2,F7)",
      len(PSL27) == 168 and len(PGL27) == 336 and iso_k is not None and iso_f is not None,
      f"D -> x+1, C -> {iso_f[1] if iso_f else None}, Rf -> {iso_f[2] if iso_f else None} (images of 0..6, inf)")
kap_idx = PGL.find((ID3, 1))
pgl_gidx = [PGL.find((M, 0)) for M in (D, C, Rf)] + [kap_idx]
iso_pgl = None
for kp in sorted(p_ for p_, sq in PGL27.items() if not sq and porder(p_) == 2):
    n_, img = graph_closure(PGL, pgl_gidx, iso_f + [kp], 336)
    if n_ == 336 and img == set(PGL27):
        iso_pgl = kp
        break
check("C", "explicit isomorphism <flipped copy, complex conjugation> -> PGL(2,F7): extend the map above by kappa -> an "
           "involution of non-square determinant; graph of order 336, image all of PGL(2,F7)", iso_pgl is not None,
      f"kappa -> {iso_pgl}")

tP, invP = PGL.table, PGL.inv
iDP = PGL.find((D, 0))


def conj_exp(x):                         # x^-1 D x = D^k  (the convention of C^-1 D C = D^4 = the 120 deg turn)
    y = tP[tP[invP[x]][iDP]][x]
    return next((k for k in range(1, 7) if y == PGL.find((mpow(D, k), 0))), None)


k_kC, k_kCi, k_kap = (conj_exp(PGL.find(smul((ID3, 1), (M, 0)))) for M in (C, Cinv, ID3))
check("C", "inside PGL(2,7) ⊂ G2, kappa, kappa C and kappa C^-1 move the seven points as x -> 6x, 3x, 5x: the 180, "
           "300 and 60 deg G2 turns all lie in <flipped copy, kappa>", (k_kap, k_kC, k_kCi) == (6, 3, 5),
      f"x -> {k_kap}x, {k_kC}x, {k_kCi}x")

# (3) Aut(F21) has order 42 and every automorphism is induced by conjugation inside PGL(2,7) = <flipped copy, kappa>
#     (closes the uniqueness argument for the PSL(2,7) in U(3) containing <D, C>; see REPORT Finding 8)
t21 = F21.table
iD21, iC21 = F21.find(D), F21.find(C)
n_aut21 = 0
for dp in range(21):
    for cp in range(21):
        S = {(0, 0)}
        frontier = [(0, 0)]
        while frontier and len(S) <= 21:
            new = []
            for x, y in frontier:
                for g_, h_ in ((iD21, dp), (iC21, cp)):
                    w_ = (t21[x][g_], t21[y][h_])
                    if w_ not in S:
                        S.add(w_)
                        new.append(w_)
            frontier = new
        if len(S) == 21 and len({y for _, y in S}) == 21:
            n_aut21 += 1
f21P = frozenset(PGL.find((M, 0)) for M in F21.elems)
tP, invP = PGL.table, PGL.inv
N_pgl = [x for x in range(336) if frozenset(tP[tP[x][h]][invP[x]] for h in f21P) == f21P]
C_pgl = [x for x in range(336) if all(tP[x][h] == tP[h][x] for h in (PGL.find((D, 0)), PGL.find((C, 0))))]
check("C", "|Aut(F21)| = 42 (graph test over all images of D, C), and N_PGL(2,7)(F21) has order 42 with trivial "
           "centraliser, so every automorphism of F21 is induced inside PGL(2,7) = <flipped copy, kappa>",
      n_aut21 == 42 and len(N_pgl) == 42 and C_pgl == [0], f"|Aut F21| = {n_aut21}, |N| = {len(N_pgl)}")
check("C", "uniqueness of the PSL(2,7) in U(3) containing <D, C> now rests only on computed facts: one class of "
           "order-21 subgroups, Aut(F21) induced by PGL(2,7), only 3 and 3bar in degree 3, F21's triplet irreducible "
           "with chi(D) = b7 != b7bar",
      n_aut21 == 42 and len(N_pgl) == 42 and C_pgl == [0] and rest168 == [(6, 7, 8)]
      and ip21 == I_ and trace(D) == b7 and b7 != b7bar
      and sum(1 for H in subs if len(H) == 21) == 8 and len(normalizer) == 21)
VALUES["computed_replacements"] = dict(
    subgroup_list_complete=join_closed, psl27_other_degrees=list(rest168[0]) if rest168 else None,
    iso_flipped_to_PSL2F7=dict(D="x+1", C=list(iso_f[1]) if iso_f else None, Rf=list(iso_f[2]) if iso_f else None),
    iso_kappa_to_PGL2F7=list(iso_pgl) if iso_pgl else None, aut_F21=n_aut21, N_PGL_F21=len(N_pgl),
    note="P^1(F7) points listed as images of 0..6 and 7 = infinity")


# =============================================================================
# D. A5 inside SO(3) ⊂ SU(3): its triplets are real (exact over Q(sqrt5))
# =============================================================================
header("D. A5's triplets (exact over Q(sqrt5))")
q0, q1 = Q5(0), Q5(1)
phi = Q5(F(1, 2), F(1, 2))                                  # golden ratio (1+sqrt5)/2
ID3q = identity(3, q1, q0)
P3 = mat([[q0, q0, q1], [q1, q0, q0], [q0, q1, q0]])        # 3-fold rotation about (1,1,1)
mvec5 = (q1, phi * phi, phi)                                # midpoint direction of an icosahedron edge
nrm = sum((x * x for x in mvec5), q0)
R2 = mat([[(Q5(2) * mvec5[i] * mvec5[j]) / nrm - (q1 if i == j else q0) for j in range(3)] for i in range(3)])
A5g = FiniteGroup([P3, R2], mmul, mkey, ID3q)
verts = set()
for s1, s2 in itertools.product((1, -1), repeat=2):
    base = (q0, Q5(s1), phi * s2)
    for k in range(3):
        verts.add(tuple(x.key() for x in base[k:] + base[:k]))
orth = all(mmul(M, transpose(M)) == ID3q and det3(M) == q1 for M in A5g.elems)
keeps = all({tuple(x.key() for x in mvec(M, tuple(Q5(*v) for v in vv))) for vv in verts} == verts
            for M in A5g.elems)
check("D", "<3-fold rotation, edge 2-fold rotation> has order 60, is in SO(3) ⊂ SU(3) (exact), and maps the 12 "
           "icosahedron vertices (0, ±1, ±phi) to themselves", len(A5g) == 60 and orth and keeps and len(verts) == 12,
      len(A5g))
cls5 = A5g.conj_classes()
simple5 = all(len(A5g.closure(c)) == 60 for c in cls5 if c != [0])
tr5 = [trace(M) for M in A5g.elems]
rows5 = sorted(((len(c), A5g.order_of(c[0]), tr5[c[0]]) for c in cls5), key=lambda r: (r[1], r[2].value()))
sig5 = [(a_, b_, f"{c_.a}+{c_.b}√5") for a_, b_, c_ in rows5]
target5 = [(1, 1, Q5(3)), (15, 2, Q5(-1)), (20, 3, Q5(0)), (12, 5, Q5(F(1, 2), F(-1, 2))), (12, 5, Q5(F(1, 2), F(1, 2)))]
check("D", "A5 classes (size, order, chi_3) = (1,1,3) (15,2,-1) (20,3,0) (12,5,(1-√5)/2) (12,5,(1+√5)/2); simple",
      rows5 == target5 and simple5, sig5)
n5 = 60
ip5 = sum((x * x for x in tr5), q0) / Q5(n5)                 # chi real, so <chi,chi> = (1/|G|) sum chi^2
fs5 = sum((tr5[A5g.table[i][i]] for i in range(n5)), q0) / Q5(n5)
ip5p = sum((x * x.galois() for x in tr5), q0) / Q5(n5)       # <chi, chi'> with chi' the Galois conjugate triplet
check("D", "A5 triplet 3: character values lie in Q(sqrt5) ⊂ R (real), <chi,chi> = 1, Frobenius-Schur indicator +1 "
           "(a real representation; indeed the matrices are real orthogonal)", ip5 == q1 and fs5 == q1,
      f"<chi,chi>={ip5}, FS={fs5}")
check("D", "the Galois-conjugate triplet 3' (sqrt5 -> -sqrt5) is inequivalent (<chi,chi'> = 0) and also real "
           "(its matrices are the Galois images, also real orthogonal)", ip5p == q0)
# degrees of A5's irreps: 5 classes; 1, 3, 3' found; remaining two degrees satisfy d^2 + d'^2 = 60-19 = 41
rest = [(a_, b_) for a_ in range(1, 8) for b_ in range(a_, 8) if a_ * a_ + b_ * b_ == 60 - 1 - 9 - 9]
check("D", "the remaining two irreducible degrees of A5 are forced to be (4,5): A5 has exactly two triplets, both real",
      rest == [(4, 5)], rest)
VALUES["A5_triplet_character"] = dict(classes="1A,2A,3A,5A,5B", sizes=[1, 15, 20, 12, 12],
                                      chi=["3", "-1", "0", "(1+sqrt5)/2", "(1-sqrt5)/2"], frobenius_schur=1)


# =============================================================================
# E. The Weyl groups of SU(3) and G2 acting on the torus (exact rationals)
# =============================================================================
header("E. Weyl groups of SU(3) and G2 on the torus (exact rationals)")
ID3f = identity(3, F(1), F(0))


def refl(r):
    rr = dot(r, r)
    return tuple(tuple(F(int(i == j)) - 2 * r[i] * r[j] / rr for j in range(3)) for i in range(3))


def fkey(M):
    return tuple(x for r in M for x in r)


def det3f(M):
    return det3(M)


long_roots = [vsub(E3[i], E3[j]) for i, j in ((0, 1), (1, 2), (0, 2))]
third = (F(1, 3), F(1, 3), F(1, 3))
short_roots = [vsub(E3[i], third) for i in range(3)]
check("E", "G2 root data: long roots e_i - e_j (norm^2 2), short roots e_i - (1,1,1)/3 (norm^2 2/3), ratio 3",
      all(dot(r, r) == 2 for r in long_roots) and all(dot(r, r) == F(2, 3) for r in short_roots))

# exact angle of a rotation in the plane: cos = (g u . u)/2, and (g u . w) = 2 sqrt3 sin
ANGLES = {(F(1), F(0)): 0, (F(1, 2), F(3)): 60, (F(-1, 2), F(3)): 120, (F(-1), F(0)): 180,
          (F(-1, 2), F(-3)): 240, (F(1, 2), F(-3)): 300}


def rot_angle(g):
    gu = mvec(g, u_ax)
    return ANGLES[(dot(gu, u_ax) / 2, dot(gu, w_ax))]


u_ax, w_ax = (F(1), F(-1), F(0)), (F(1), F(1), F(-2))
weyl_rows = {}
WG = {}
for name, roots in (("SU(3)", long_roots), ("G2", long_roots + short_roots)):
    Wg = FiniteGroup([refl(r) for r in roots], mmul, fkey, ID3f)
    WG[name] = Wg
    keepsL = all(in_Lambda(mvec(g, b)) for g in Wg.elems for b in (b1, b2))
    mirrors = [g for g in Wg.elems if det3f(g) < 0]
    rots = [g for g in Wg.elems if det3f(g) > 0]
    m_keep = sum(label(mvec(g, p)) is not None for g in mirrors)
    REPLICA.append(f"Weyl({name}): order {len(Wg)} | keeps Λ: {keepsL} | mirrors that keep the seven points: "
                   f"{m_keep} of {len(mirrors)}")
    rows = []
    for g in rots:
        ang = rot_angle(g)
        k = label(mvec(g, p))
        if k is None:
            fate = "moves the seven points"
        elif image(A, k, 0) == A and image(B, k, 0) == B:
            fate = f"x -> {k}x, keeps both families"
        elif image(A, k, 0) == B and image(B, k, 0) == A:
            fate = f"x -> {k}x, swaps the families"
        else:
            fate = f"x -> {k}x, other"
        rows.append((ang, fate))
    rows.sort()
    for ang, fate in rows:
        REPLICA.append(f"   turn {ang:>3}°: {fate}")
    weyl_rows[name] = dict(order=len(Wg), keeps_Lambda=keepsL, mirrors=len(mirrors), mirrors_keeping_points=m_keep,
                           turns=[f"{a_} deg: {f_}" for a_, f_ in rows])
    print(f"    Weyl({name}): order {len(Wg)}; turns: " + "; ".join(f"{a_}°: {f_}" for a_, f_ in rows))

check("E", "Weyl(SU(3)): order 6, keeps Lambda, turns only by 0/120/240 deg (x -> x, 4x, 2x; both families kept), "
           "3 mirrors, none keeps the seven points",
      weyl_rows["SU(3)"]["order"] == 6 and weyl_rows["SU(3)"]["keeps_Lambda"]
      and weyl_rows["SU(3)"]["turns"] == ["0 deg: x -> 1x, keeps both families", "120 deg: x -> 4x, keeps both families",
                                          "240 deg: x -> 2x, keeps both families"]
      and weyl_rows["SU(3)"]["mirrors"] == 3 and weyl_rows["SU(3)"]["mirrors_keeping_points"] == 0)
check("E", "Weyl(G2): order 12, keeps Lambda, adds turns by 60/180/300 deg acting as x -> 5x, 6x, 3x, which swap the "
           "families; 6 mirrors, none keeps the seven points",
      weyl_rows["G2"]["order"] == 12 and weyl_rows["G2"]["keeps_Lambda"]
      and weyl_rows["G2"]["turns"] == ["0 deg: x -> 1x, keeps both families", "60 deg: x -> 5x, swaps the families",
                                       "120 deg: x -> 4x, keeps both families", "180 deg: x -> 6x, swaps the families",
                                       "240 deg: x -> 2x, keeps both families", "300 deg: x -> 3x, swaps the families"]
      and weyl_rows["G2"]["mirrors"] == 6 and weyl_rows["G2"]["mirrors_keeping_points"] == 0)
# -1 on the plane, +1 on the normal (1,1,1):  -I + (2/3) J   (as 3x3 matrices the Weyl elements fix (1,1,1))
negI = tuple(tuple(-F(int(i == j)) + F(2, 3) for j in range(3)) for i in range(3))
wa2 = {fkey(g) for g in WG["SU(3)"].elems}
wg2 = {fkey(g) for g in WG["G2"].elems}
check("E", "Weyl(G2) = Weyl(SU(3)) × {±1} on the plane (so any dihedral group of order 12 containing Weyl(SU(3)) is "
           "this one: the choice of short roots does not matter)",
      wg2 == wa2 | {fkey(mmul(negI, g)) for g in WG["SU(3)"].elems})
# every SU(3) mirror sends D's order-7 subgroup to the other hexagonal one (diag(z, z^4, z^2))
q_other = (F(1, 7), F(4, 7), F(-5, 7))
other_sub = {tuple(vscal(k, q_other)) for k in range(1, 7)}


def same_mod_Lambda(v, S):
    return any(in_Lambda(vsub(v, s)) for s in S)


check("E", "(extra) each SU(3) mirror maps the seven points of D onto the seven points of diag(z, z^4, z^2) "
           "(the other hexagonal order-7 subgroup)",
      all(same_mod_Lambda(mvec(g, p), other_sub) for g in WG["SU(3)"].elems if det3f(g) < 0))
VALUES["weyl"] = weyl_rows


# =============================================================================
# F. Affine Weyl groups: G2 -> p6m, SU(3) -> p3m1 (exact rationals, Lambda coordinates)
# =============================================================================
header("F. affine Weyl group of G2 is the wallpaper group p6m (exact)")


def coroot(r):
    return vscal(F(2) / dot(r, r), r)


def aff_refl(r, k):
    """s_{r,k}(x) = x - ((r,x) - k) r^vee, as (M, t) acting on 3-vectors in the plane."""
    rv = coroot(r)
    M = tuple(tuple(F(int(i == j)) - rv[i] * r[j] for j in range(3)) for i in range(3))
    return (M, vscal(F(k), rv))


def amul(X, Y):          # (X∘Y)(x) = X(Y(x))
    (M1, t1), (M2, t2) = X, Y
    return (mmul(M1, M2), vadd(mvec(M1, t2), t1))


def akey(X):
    return (fkey(X[0]), X[1])


# G2 simple roots (alpha1 short, alpha2 long) and highest root theta
al1 = short_roots[0]                         # (2,-1,-1)/3
al2 = vsub(E3[1], E3[0])                     # (-1,1,0)
theta = vadd(vscal(3, al1), vscal(2, al2))   # (0,1,-1)
pos_roots = [al1, al2, vadd(al1, al2), vadd(vscal(2, al1), al2), vadd(vscal(3, al1), al2), theta]
allroots = set(long_roots + short_roots + [vscal(-1, r) for r in long_roots + short_roots])
check("E", "G2 base: alpha1 short, alpha2 long at 150 deg; the six positive roots a1, a2, a1+a2, 2a1+a2, 3a1+a2, "
           "3a1+2a2 are roots, with highest root theta = (0,1,-1)",
      dot(al1, al2) == -1 and all(r in allroots for r in pos_roots) and theta == (F(0), F(1), F(-1)))
s1, s2, s0 = aff_refl(al1, 0), aff_refl(al2, 0), aff_refl(theta, 1)
IDA = (ID3f, (F(0), F(0), F(0)))


def aorder(X, cap=20):
    Y = X
    for k in range(1, cap + 1):
        if akey(Y) == akey(IDA):
            return k
        Y = amul(Y, X)
    return None


cox = (aorder(amul(s1, s2)), aorder(amul(s2, s0)), aorder(amul(s1, s0)))
check("F", "Coxeter orders: (s1 s2)^6 = (s2 s0)^3 = (s1 s0)^2 = 1: the (2,3,6) triangle group (affine G2)",
      cox == (6, 3, 2), cox)
# W_aff = Lambda ⋊ W(G2):
#   (i) every generator has linear part in W(G2) and translation part in Lambda; both properties are closed under
#       composition because W(G2) preserves Lambda, so W_aff ⊂ Lambda ⋊ W(G2);
#  (ii) s1, s2 generate W(G2) (linear, fixing 0), and s0 ∘ s_{theta,0} is translation by theta^vee; conjugating it by
#       W gives translation by every long root, which contains the Lambda basis b1, b2: so Lambda ⋊ W(G2) ⊂ W_aff.
gens_ok = all(fkey(X[0]) in wg2 and in_Lambda(X[1]) for X in (s1, s2, s0))
W_from_s12 = FiniteGroup([s1, s2], amul, akey, IDA)
lin_ok = len(W_from_s12) == 12 and {fkey(X[0]) for X in W_from_s12.elems} == wg2 and all(
    not any(X[1]) for X in W_from_s12.elems)
Ttheta = amul(s0, aff_refl(theta, 0))
trans_ok = Ttheta[0] == ID3f and Ttheta[1] == coroot(theta)
conj_trans = set()
for g in W_from_s12.elems:
    # g T g^-1 = translation by g(theta^vee)
    conj_trans.add(mvec(g[0], coroot(theta)))
check("F", "W_aff = Lambda ⋊ W(G2): generators have linear part in W(G2) and translation in Lambda; s1, s2 generate the "
           "12-element W(G2); s0∘s_theta is translation by theta^vee and its W-conjugates include b1, b2",
      gens_ok and lin_ok and trans_ok and b1 in conj_trans and b2 in conj_trans and all(in_Lambda(v) for v in conj_trans))
# brute-force confirmation: all words of length <= 10 have the claimed form, and their pure translations fill Lambda
seen = {akey(IDA): IDA}
frontier = [IDA]
for depth in range(10):
    new = []
    for X in frontier:
        for g in (s0, s1, s2):
            Y = amul(X, g)
            k_ = akey(Y)
            if k_ not in seen:
                seen[k_] = Y
                new.append(Y)
    frontier = new
form_ok = all(fkey(X[0]) in wg2 and in_Lambda(X[1]) for X in seen.values())
pure_tr = {lam2(X[1]) for X in seen.values() if X[0] == ID3f}
small_box = {(F(a_), F(b_)) for a_ in range(-1, 2) for b_ in range(-1, 2)}
check("F", "BFS over all words of length <= 10 in s0, s1, s2: every element is (W(G2) element, Lambda translation), and "
           "the pure translations reached include every Lambda vector with coordinates in {-1,0,1}",
      form_ok and small_box <= pure_tr, f"{len(seen)} elements, {len(pure_tr)} translations")


def lam_mat(M):
    """2x2 integer matrix of a linear map of the plane in the Lambda basis."""
    c1, c2 = lam2(mvec(M, b1)), lam2(mvec(M, b2))
    return ((c1[0], c2[0]), (c1[1], c2[1]))


def wyckoff(Wset, name):
    """rotation centres mod Lambda and their stabilisers in Lambda ⋊ W (exact)."""
    Ms = [lam_mat(M) for M in Wset]
    rot = [Mm for Mm, M in zip(Ms, Wset) if det3f(M) > 0 and fkey(M) != fkey(ID3f)]
    centres = set()
    for Mm in rot:
        IM = ((1 - Mm[0][0], -Mm[0][1]), (-Mm[1][0], 1 - Mm[1][1]))
        for t1, t2 in itertools.product(range(-3, 4), repeat=2):
            c = solve2(IM, (F(t1), F(t2)))
            centres.add((c[0] - (c[0].numerator // c[0].denominator), c[1] - (c[1].numerator // c[1].denominator)))
    out = []
    for c in sorted(centres):
        stab = []
        for Mm, M in zip(Ms, Wset):
            img = (Mm[0][0] * c[0] + Mm[0][1] * c[1], Mm[1][0] * c[0] + Mm[1][1] * c[1])
            dif = (c[0] - img[0], c[1] - img[1])
            if dif[0].denominator == 1 and dif[1].denominator == 1:
                stab.append(M)
        nrot = sum(1 for M in stab if det3f(M) > 0)
        nmir = sum(1 for M in stab if det3f(M) < 0)
        out.append(dict(centre=(str(c[0]), str(c[1])), rotation_order=nrot, mirrors_through=nmir,
                        site_group_order=len(stab)))
    return out


wy_g2 = wyckoff(WG["G2"].elems, "G2")
wy_a2 = wyckoff(WG["SU(3)"].elems, "SU(3)")
sig_g2 = Counter((w["rotation_order"], w["mirrors_through"]) for w in wy_g2)
sig_a2 = Counter((w["rotation_order"], w["mirrors_through"]) for w in wy_a2)
print("    G2 affine Weyl group, rotation centres per cell (rotation order, mirrors through it): " +
      ", ".join(f"{w['centre']}: ({w['rotation_order']}, {w['mirrors_through']})" for w in wy_g2))
print("    SU(3) affine Weyl group, rotation centres per cell: " +
      ", ".join(f"{w['centre']}: ({w['rotation_order']}, {w['mirrors_through']})" for w in wy_a2))
check("F", "G2: point group = W(G2), dihedral of order 12 (contains the 60 deg turn), translations = Lambda (hexagonal)"
           " -> p6m, the only wallpaper group whose point group has order 12",
      len(wg2) == 12 and any(rot_angle(g) == 60 for g in WG["G2"].elems if det3f(g) > 0) and gram_L == [[2, -1], [-1, 2]])
check("F", "G2 site symmetries per cell: one 6-fold centre with 6 mirrors (6mm), two 3-fold centres with 3 mirrors "
           "(3m), three 2-fold centres with 2 mirrors (2mm): the p6m Wyckoff pattern 1a, 2b, 3c",
      sig_g2 == Counter({(6, 6): 1, (3, 3): 2, (2, 2): 3}), dict(sig_g2))
check("F", "contrast, SU(3): Lambda ⋊ W(SU(3)) has three 3-fold centres per cell, each on 3 mirrors (3m, 3m, 3m): "
           "p3m1, no 6-fold or 2-fold centres",
      sig_a2 == Counter({(3, 3): 3}), dict(sig_a2))
# which elements of the affine Weyl groups keep the seven points? translation parts lie in Lambda ⊂ L', so exactly
# those whose linear part keeps L': the rotations.
keepG2 = [g for g in WG["G2"].elems if label(mvec(g, p)) is not None]
check("F", "(extra) the elements of W_aff(G2) that keep the seven points are Lambda ⋊ C6 (all turns, no mirror): p6; "
           "for SU(3) it is Lambda ⋊ C3: p3",
      len(keepG2) == 6 and all(det3f(g) > 0 for g in keepG2)
      and len([g for g in WG["SU(3)"].elems if label(mvec(g, p)) is not None]) == 3)
# mirrors of W_aff are the lines (alpha, x) = k (alpha a root, k integer); the seven points j p (+ Lambda)
on_mirror = [(j, r) for j in range(1, 7) for r in long_roots + short_roots if dot(r, vscal(j, p)).denominator == 1]
check("F", "(extra) none of the six non-zero points j p (j = 1..6, any Lambda translate) lies on any mirror of either "
           "affine Weyl group; point 0 (the Lambda points) lies on all six mirror directions",
      on_mirror == [])
VALUES["affine_weyl"] = dict(G2=dict(coxeter=list(cox), point_group_order=12, wallpaper="p6m", site_pattern=wy_g2),
                             SU3=dict(point_group_order=6, wallpaper="p3m1", site_pattern=wy_a2))


# =============================================================================
# G. (extra, not preregistered) Octonions: G2 ⊃ SU(3) ⊃ PSL(2,7), and complex conjugation is in G2
# =============================================================================
header("G. (extra) octonions O = C ⊕ C^3: G2 = Aut(O) contains SU(3), PSL(2,7) and PGL(2,7)")


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def oprod(x, y):
    """(a,u)(b,v) = (ab - sum u_i conj(v_i), a v + conj(b) u + conj(u x v)); complex scalars in Q(zeta7)."""
    (a_, u), (b_, v) = x, y
    s_ = a_ * b_ - sum((u[i] * v[i].conj() for i in range(3)), O_)
    cr = cross(u, v)
    w = tuple(a_ * v[i] + b_.conj() * u[i] + cr[i].conj() for i in range(3))
    return (s_, w)


def oadd(x, y):
    return (x[0] + y[0], tuple(p_ + q_ for p_, q_ in zip(x[1], y[1])))


def onorm(x):
    return x[0] * x[0].conj() + sum((c_ * c_.conj() for c_ in x[1]), O_)


zero3 = (O_, O_, O_)


def unit3(j, s_):
    return tuple(s_ if k == j else O_ for k in range(3))


EB = [(I_, zero3), (G, zero3)] + [x for j in range(3) for x in ((O_, unit3(j, I_)), (O_, unit3(j, G)))]
OKEY = lambda x: (x[0].key(),) + tuple(c_.key() for c_ in x[1])
check("G", "(1,0) is a two-sided identity", all(OKEY(oprod(EB[0], x)) == OKEY(x) == OKEY(oprod(x, EB[0])) for x in EB))


def assoc(x, y, w):
    l_ = oprod(oprod(x, y), w)
    r_ = oprod(x, oprod(y, w))
    return (l_[0] - r_[0], tuple(p_ - q_ for p_, q_ in zip(l_[1], r_[1])))


def oiszero(x):
    return x[0].is_zero() and all(c_.is_zero() for c_ in x[1])


alt = all(oiszero(oadd(assoc(x, y, w), assoc(y, x, w))) and oiszero(oadd(assoc(x, y, w), assoc(x, w, y)))
          for x in EB for y in EB for w in EB)
check("G", "alternative: the associator is alternating on all 512 basis triples (hence everywhere, by trilinearity)", alt)
S_pol = EB + [oadd(EB[i], EB[j]) for i in range(8) for j in range(i + 1, 8)]
comp = all(onorm(oprod(x, y)) == onorm(x) * onorm(y) for x in S_pol for y in S_pol)
check("G", "composition: N(xy) = N(x)N(y) on all 36x36 polarisation points (a complete check of this biquadratic "
           "identity), N = |a|^2 + |u|^2 positive definite: by Hurwitz this is the octonion algebra", comp)


def phi_M(M):
    return lambda x: (x[0], mvec(M, x[1]))


def kappa(x):
    return (x[0].conj(), tuple(c_.conj() for c_ in x[1]))


def is_aut(f):
    return all(OKEY(f(oprod(x, y))) == OKEY(oprod(f(x), f(y))) for x in EB for y in EB)


auts = {nm: is_aut(f) for nm, f in (("D", phi_M(D)), ("C", phi_M(C)), ("Rf", phi_M(Rf)), ("Dk", phi_M(Dk)),
                                     ("R", phi_M(R)), ("kappa", kappa))}
check("G", "D, C, Rf, Dk, R (acting on C^3) and complex conjugation kappa are octonion automorphisms (exact on all "
           "64 basis pairs); the matrices fix the imaginary unit e = (i,0), kappa sends it to -e", all(auts.values()),
      auts)
check("G", "hence G2 = Aut(O) contains both PSL(2,7) copies and <flipped copy, kappa> = PGL(2,7) (order 336, "
           "section C), inside the stabiliser of the line R e", all(auts.values()) and PGL.n == 336)


def ocoords(x):
    """real coordinates in the basis EB (exact; rational for elements of Q(G) ⊕ Q(G)^3)."""
    out = []
    for c_ in (x[0],) + x[1]:
        al_ = (c_ + c_.conj()) * F(1, 2)
        be_ = (c_ - c_.conj()) * G * F(-1, 14)                  # (c - cbar)/(2G), with 1/G = -G/7
        out += [al_, be_]
    return out


Gam = [[[c_.to_fraction() for c_ in ocoords(oprod(EB[a_], EB[b_]))] for b_ in range(8)] for a_ in range(8)]


def nullspace(rows, ncols):
    """exact reduced row echelon nullspace over Q."""
    Mx = [list(r) for r in rows if any(r)]
    piv = []
    r_ = 0
    for c_ in range(ncols):
        pr = next((i for i in range(r_, len(Mx)) if Mx[i][c_] != 0), None)
        if pr is None:
            continue
        Mx[r_], Mx[pr] = Mx[pr], Mx[r_]
        inv_ = 1 / Mx[r_][c_]
        Mx[r_] = [v * inv_ for v in Mx[r_]]
        for i in range(len(Mx)):
            if i != r_ and Mx[i][c_] != 0:
                f_ = Mx[i][c_]
                Mx[i] = [vi - f_ * vr for vi, vr in zip(Mx[i], Mx[r_])]
        piv.append(c_)
        r_ += 1
        if r_ == len(Mx):
            break
    free = [c_ for c_ in range(ncols) if c_ not in piv]
    basis_ = []
    for fcol in free:
        v = [F(0)] * ncols
        v[fcol] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -Mx[i][fcol]
        basis_.append(v)
    return basis_


def der_equations(extra_kill=None):
    rows = []
    idx = lambda c_, d_: 8 * c_ + d_          # X[c][d] : coefficient of e_c in X(e_d)
    for a_ in range(8):
        for b_ in range(8):
            for c_ in range(8):
                row = [F(0)] * 64
                for d_ in range(8):
                    row[idx(c_, d_)] += Gam[a_][b_][d_]
                for f_ in range(8):
                    row[idx(f_, a_)] -= Gam[f_][b_][c_]
                    row[idx(f_, b_)] -= Gam[a_][f_][c_]
                rows.append(row)
    if extra_kill is not None:
        for c_ in range(8):
            row = [F(0)] * 64
            row[idx(c_, extra_kill)] = F(1)
            rows.append(row)
    return rows


der = nullspace(der_equations(), 64)
stab = nullspace(der_equations(extra_kill=1), 64)
tomat = lambda v: [[v[8 * c_ + d_] for d_ in range(8)] for c_ in range(8)]


def mm8(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(8)) for j in range(8)] for i in range(8)]


def bracket(X, Y):
    XY, YX = mm8(X, Y), mm8(Y, X)
    return [[XY[i][j] - YX[i][j] for j in range(8)] for i in range(8)]


def lie_data(basis_vecs):
    """structure constants, Killing form, its definiteness, and min centraliser dimension for a test element."""
    n_ = len(basis_vecs)
    mats = [tomat(v) for v in basis_vecs]
    flat = [[v[k] for v in basis_vecs] for k in range(64)]           # 64 x n system to express brackets

    def coords_in_basis(Xm):
        target = [Xm[c_][d_] for c_ in range(8) for d_ in range(8)]
        # solve flat * x = target exactly (overdetermined, consistent)
        aug = [row + [t] for row, t in zip(flat, target)]
        sol = nullspace([r[:-1] + [-r[-1]] for r in aug], n_ + 1)
        sol = [s_ for s_ in sol if s_[-1] != 0]
        assert len(sol) == 1, "bracket not in span"
        return [x / sol[0][-1] for x in sol[0][:-1]]
    ad = []
    for i in range(n_):
        cols = [coords_in_basis(bracket(mats[i], mats[j])) for j in range(n_)]
        ad.append([[cols[j][k] for j in range(n_)] for k in range(n_)])
    killing = [[sum(ad[i][r][s_] * ad[j][s_][r] for r in range(n_) for s_ in range(n_)) for j in range(n_)]
               for i in range(n_)]
    # negative definiteness: LDL^T of -killing, all pivots > 0
    Kd = [[-x for x in r] for r in killing]
    pivots = []
    Mx = [r[:] for r in Kd]
    for k in range(n_):
        pk = Mx[k][k]
        pivots.append(pk)
        if pk == 0:
            break
        for i in range(k + 1, n_):
            f_ = Mx[i][k] / pk
            Mx[i] = [Mx[i][j] - f_ * Mx[k][j] for j in range(n_)]
    negdef = len(pivots) == n_ and all(x > 0 for x in pivots)
    coeffs = [1, 2, -3, 5, -7, 11, 13, -17, 19, 23, -29, 31, 37, -41][:n_]
    adX = [[sum(coeffs[i] * ad[i][r][s_] for i in range(n_)) for s_ in range(n_)] for r in range(n_)]
    cdim = len(nullspace(adX, n_))
    return negdef, cdim


negdef14, cdim14 = lie_data(der)
negdef8, cdim8 = lie_data(stab)
check("G", "Der(O) has dimension 14, negative-definite Killing form (compact semisimple) and a test element with "
           "2-dim centraliser (rank <= 2): the only such algebra is g2",
      len(der) == 14 and negdef14 and cdim14 == 2, f"dim {len(der)}, centraliser {cdim14}")
check("G", "derivations killing the imaginary unit e: dimension 8, compact semisimple, rank <= 2: su(3) "
           "(the only compact semisimple Lie algebra of dimension 8)",
      len(stab) == 8 and negdef8 and cdim8 == 2, f"dim {len(stab)}, centraliser {cdim8}")
# the su(3) acting on C^3 (anti-hermitian traceless, entries in Q(G)) spans exactly that stabiliser
su3_basis = []
for j in range(3):
    for k in range(j + 1, 3):
        Ejk = [[(I_ if (r, c_) == (j, k) else (Z7.rat(-1) if (r, c_) == (k, j) else O_)) for c_ in range(3)] for r in range(3)]
        Sjk = [[(G if (r, c_) in ((j, k), (k, j)) else O_) for c_ in range(3)] for r in range(3)]
        su3_basis += [Ejk, Sjk]
for j in range(2):
    su3_basis.append([[(G if (r, c_) == (j, j) else (-G if (r, c_) == (j + 1, j + 1) else O_)) for c_ in range(3)]
                      for r in range(3)])


def realify_der(Mc):
    cols = []
    for d_ in range(8):
        x = EB[d_]
        img = (O_, mvec(Mc, x[1]))
        cols.append([c_.to_fraction() for c_ in ocoords(img)])
    return [cols[d_][c_] for c_ in range(8) for d_ in range(8)]      # flattened X[c][d]


su3_vecs = [realify_der(Mc) for Mc in su3_basis]
span_rows = [list(v) for v in stab]
in_stab = all(len(nullspace([list(r) for r in zip(*(stab + [v]))], len(stab) + 1)) == 1 for v in su3_vecs)
indep = len(nullspace([list(r) for r in zip(*su3_vecs)], 8)) == 0
check("G", "the 8 matrices of su(3) acting on C^3 are derivations killing e and span that 8-dim stabiliser",
      in_stab and indep)
VALUES["octonions"] = dict(der_dim=len(der), stabiliser_dim=len(stab), PGL27_in_G2_order=PGL.n)


# =============================================================================
# H. Line-by-line comparison with hexagon_check.py (floating point), and results.json
# =============================================================================
header("H. line-by-line comparison with hexagon_check.py")
# put the Fano line where hexagon_check.py prints it (after the group lines)
fl = [l_ for l_ in REPLICA if l_.startswith("Fano planes on Z7")]
REPLICA = [l_ for l_ in REPLICA if not l_.startswith("Fano planes on Z7")]
pos = next(i for i, l_ in enumerate(REPLICA) if l_.startswith("order-21 group maximal")) + 1
REPLICA = REPLICA[:pos] + fl + REPLICA[pos:]
with open(os.path.join(HERE, "exact_replica_output.txt"), "w") as fh:
    fh.write("\n".join(REPLICA) + "\n")
env = dict(os.environ, NUMBA_NUM_THREADS="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
t_orig = time.time()
orig = subprocess.run([sys.executable, os.path.join(SEED, "hexagon_check.py")], capture_output=True, text=True,
                      env=env, cwd=HERE)
t_orig = time.time() - t_orig
with open(os.path.join(HERE, "hexagon_check_original_output.txt"), "w") as fh:
    fh.write(orig.stdout)
orig_lines = orig.stdout.rstrip("\n").split("\n")
same = [a_ == b_ for a_, b_ in zip(orig_lines, REPLICA)]
for a_, b_, s_ in zip(orig_lines, REPLICA, same):
    print(f"    {'==' if s_ else '!='}  {a_}" + ("" if s_ else f"   |  exact: {b_}"))
check("H", f"hexagon_check.py (float) and the exact recomputation print identical lines ({sum(same)} of "
           f"{len(orig_lines)})", orig.returncode == 0 and len(orig_lines) == len(REPLICA) and all(same),
      f"original runtime {t_orig:.1f} s")
VALUES["replica"] = dict(lines_original=len(orig_lines), lines_exact=len(REPLICA), identical=sum(same))

runtime = time.time() - T0
n_pass = sum(c_["ok"] for c_ in CHECKS)
print(f"\n{n_pass} of {len(CHECKS)} exact checks passed; runtime {runtime:.1f} s")


def calib(quantity, ours, target, source, ok, tol="exact", note="", kind="seed"):
    """kind = 'lit': the target is a literature value -> CALIBRATED (PLAN §1); kind = 'seed': the target is a SEED.md
    claim -> CONFIRMED (verdict vocabulary corrected in the reconciliation, Oct 19)."""
    if target is None:
        verdict = "NO_TARGET"
    elif not ok:
        verdict = "MISS" if kind == "lit" else "REFUTED"
    else:
        verdict = "CALIBRATED" if kind == "lit" else "CONFIRMED"
    return dict(quantity=quantity, value=ours, target=target, tolerance=tol, source=source, verdict=verdict,
                note=note)


ck = {c_["name"]: c_["ok"] for c_ in CHECKS}


def ok_prefix(*prefixes):
    return all(any(n.startswith(p_) and v for n, v in ck.items()) for p_ in prefixes)


headline = [
    calib("hexagon_check.py printed lines reproduced exactly", f"{sum(same)}/{len(orig_lines)} identical",
          "all lines identical", "seed/hexagon_check.py", all(same) and len(orig_lines) == len(REPLICA)),
    calib("120 deg Weyl turn on the seven points", f"x -> {k_turn}x", "x -> 4x", "SEED §3", k_turn == 4),
    calib("finer lattice Lambda + Z p", "hexagonal, Gram (1/7)[[2,-1],[-1,2]], index 7, 6 shortest vectors",
          "hexagonal", "SEED §3", ok_prefix("Gram(p, tp)", "the finer lattice has minimal")),
    calib("torus triangulation V - E + F", f"{V_} - {E_} + {F_} = {V_ - E_ + F_}", "7 - 21 + 14 = 0",
          "SEED §3 / PLAN E0", (V_, E_, F_) == (7, 21, 14)),
    calib("K7, two Fano families, octonion lines", f"K7; 2 Fano families; '{which}' family = {{i,i+1,i+3}}",
          "K7; two Fano families; one = octonion lines", "SEED §3", ok_prefix("one family is exactly", "family 'up'")),
    calib("Fano planes on Z7 fixed by x -> x+1", f"{len(cyclic)} of {len(fanos)}; = the two torus families",
          "2, = the torus families", "SEED §3", len(cyclic) == 2 and len(fanos) == 30),
    calib("|<D, 120 deg turn>| in SU(3)", f"{len(F21)} (exact unitary, det 1)", "21", "SEED §3", len(F21) == 21 and f21_su3),
    calib("|Klein's copy| and |flipped copy| in SU(3)", f"{len(PSLk)}, {len(PSLf)}", "168, 168", "SEED §3",
          len(PSLk) == len(PSLf) == 168 and psk_su3 and psf_su3),
    calib("quartic invariants (exact polynomial identities)",
          f"Klein copy keeps x^3y+y^3z+z^3x: {kq_all}; flipped keeps xy^3+yz^3+zx^3: {mq_all}",
          "both True", "LNR eq. 78 [read] (mirror quartic of LNR's basis = the flipped copy); SEED §3", kq_all and mq_all,
          kind="lit"),
    calib("maximal subgroups of PSL(2,7) (class size x order)",
          ", ".join(f"{b_}x{a_}" for a_, b_, _ in max_summary), "S4 (7), S4 (7), 7:3 (8)",
          "ATLAS p.3 (via SEED §9, not read) for the two S4 classes and 7:3; LNR §5 [read] gives only the types "
          "S4 and Z7⋊Z3", sorted((a_, b_) for a_, b_, _ in max_summary) == [(21, 8), (24, 7), (24, 7)], kind="lit",
          note="the two conjugacy classes of S4 are established by the computation itself"),
    calib("PSL(2,7) triplet character on 1A,2A,3A,4A,7A,7B", "3, -1, 0, 1, b7, b7bar; FS indicator 0",
          "3, -1, 0, 1, b7, b7bar (b7 = (-1+i sqrt7)/2): complex", "LNR eq. 13 [read]; PLAN E0",
          ok_prefix("flipped copy: classes", "flipped copy: <chi,chi>"), kind="lit"),
    calib("F21 triplet character on 1A,3A,3B,7A,7B", "3, 0, 0, b7, b7bar; FS indicator 0",
          "3, 0, 0, b7, b7bar: complex", "LNR §5 table [read]; PLAN E0", ok_prefix("F21 classes", "F21 triplet"), kind="lit"),
    calib("A5 triplet characters on 1A,2A,3A,5A,5B", "3, -1, 0, (1+-sqrt5)/2; FS indicator +1 (both triplets)",
          "real, with (1 +- sqrt5)/2", "PLAN E0; LNR §2 (eq. 4 and text: five real irreps, two triplets) [read]", ok_prefix("A5 classes", "A5 triplet 3", "the Galois"), kind="lit"),
    calib("Weyl(SU(3)) and Weyl(G2) on the seven points",
          "orders 6, 12; SU(3) turns x->4x,2x keep families; G2 adds 60/180/300 deg = x->5x,6x,3x, swap; "
          "mirrors keeping points 0/3, 0/6", "as SEED §3 / hexagon_check.py", "SEED §3",
          ok_prefix("Weyl(SU(3)): order 6", "Weyl(G2): order 12")),
    calib("G2 affine Weyl group", "Coxeter (2,3,6); Lambda ⋊ D6, |point group| = 12, 60 deg turn; sites 1a(6mm) "
          "2b(3m) 3c(2mm)", "p6m", "SEED §3; PLAN E0", ok_prefix("Coxeter orders", "W_aff = Lambda", "G2: point group",
                                                                "G2 site symmetries")),
    calib("7-vertex torus triangulations (labelled) / automorphisms", f"{len(surfaces)} labelled, one orbit; "
          f"|Aut| = {len(aut_T14)} = AGL(1,7), all orientation-preserving (chiral)", None, "extra (not preregistered)",
          True),
    calib("Der(O) / stabiliser of an imaginary unit", f"dim {len(der)} (g2) / dim {len(stab)} (su(3))", None,
          "extra; SEED cites Gunaydin-Gursey 1973", True),
    calib("<PSL(2,7), complex conjugation> inside G2", f"order {PGL.n} = PGL(2,7) (explicit isomorphism onto "
          f"PGL(2,F7): {iso_pgl is not None}); swaps S4 classes and Fano families", None, "extra (new finding)", True),
    calib("order-7 torus points with a hexagonal finer lattice", f"{len(hexpts)} of 48 (2 subgroups)", None,
          "extra", True),
]

seed_claims = [
    ("§3 intro: the torus and group computations are checked by hexagon_check.py", "CONFIRMED",
     "hexagon_check.py runs (1 s) and every printed line is reproduced identically by exact arithmetic."),
    ("SU(3) is the color group and the group of the eightfold way", "CONFIRMED (cited)",
     "textbook background, not computed by E0."),
    ("SU(3)'s diagonal elements form a flat torus = plane / hexagonal lattice (a 60 deg wallpaper rolled up)",
     "CONFIRMED", "kernel of theta -> diag(exp 2 pi i theta) is Lambda = Z^3 ∩ plane, Gram [[2,-1],[-1,2]]."),
    ("its weights sit on a hexagonal lattice; octets are hexagons, the decuplet a triangle", "CONFIRMED",
     "weight Gram (1/3)[[2,1],[1,2]]; octet = regular hexagon + doubly occupied centre; decuplet = triangle, 4 per side."),
    ("D = diag(z, z^2, z^4) is in SU(3); its seven powers are seven points of the torus", "CONFIRMED",
     "det D = z^7 = 1, D unitary, D^7 = 1, the 7 points are distinct mod Lambda."),
    ("the finer hexagonal lattice through them cuts the torus into the 7-vertex triangulation", "CONFIRMED",
     "Lambda + Zp is hexagonal (Gram (1/7)[[2,-1],[-1,2]]); 7-21+14 = 0, every edge in 2 triangles, links 6-cycles, "
     "orientable; equals {i,i+1,i+3} ∪ {i,i+2,i+3}; exhaustive search over 7-vertex surfaces with chi = 0: the 7-vertex "
     "torus triangulation is unique and there is no 7-vertex Klein bottle."),
    ("every point joined to every other (K7)", "CONFIRMED", "six shortest vectors carry labels 1..6; 21 edges."),
    ("14 triangles in two families of 7", "CONFIRMED", "up and down triangles of the finer lattice."),
    ("each family a Fano plane, one exactly the octonion lines {i,i+1,i+3}", "CONFIRMED",
     f"the '{which}' family is {{i,i+1,i+3}}; the other is {{i,i+2,i+3}}."),
    ("only two Fano planes on 0-6 survive x -> x+1, and the two families are exactly those", "CONFIRMED",
     "30 Fano planes in all, exactly 2 cyclic = the two families; so one family is always the octonion lines."),
    ("SU(3)'s 120 deg Weyl rotation moves the seven points as x -> 4x", "CONFIRMED",
     "C^-1 D C = D^4 (the opposite 120 deg turn gives x -> 2x; which one is 'the' turn is a direction convention)."),
    ("together with D it generates Z7 ⋊ Z3 (order 21) inside SU(3)", "CONFIRMED", "exact closure: 21 unitary det-1 matrices."),
    ("the group preserves both Fano families, so it is the collineation F21", "CONFIRMED",
     "x -> ax+b, a in {1,2,4}, keeps both; Aut(A) ∩ Aut(B) is exactly this group of order 21."),
    ("Klein's group of order 168, symmetry group of the Klein quartic, is PSL(2,7) on C^3", "CONFIRMED (partly cited)",
     "<Dk, C, R> has order 168, is isomorphic to PSL(2,F7) (explicit isomorphism), keeps x^3y+y^3z+z^3x exactly. "
     "Cited, not recomputed: that the curve has no further automorphisms (Hurwitz's bound)."),
    ("PSL(2,7) is the only simple subgroup of SU(3) with a complex 3-dim irrep; the only other non-abelian simple one "
     "is A5, whose triplets are real", "CONFIRMED (partly cited)",
     "characters: PSL(2,7) and F21 triplets have FS indicator 0 (b7 non-real); both A5 triplets FS +1. Cited, not "
     "recomputed: the 'only' part, which rests on the classification of finite subgroups of SU(3) (via LNR [read])."),
    ("the order-21 group is one of its maximal subgroups (ATLAS)", "CONFIRMED",
     "exact: maximal subgroups are 7 S4 + 7 S4 + 8 (7:3), from the complete subgroup list (179 subgroups, closed under "
     "joins); F21 is one of the 8. LNR §5 [read] lists the types S4 and Z7⋊Z3; the two S4 classes match ATLAS "
     "(via SEED §9, not read)."),
    ("Klein's own matrices contain diag(z^4, z^2, z), not D", "CONFIRMED",
     "the copy keeping x^3y+y^3z+z^3x contains Dk and not D; the order-7 diagonal symmetries of that quartic are exactly "
     "the powers of Dk (D rescales its monomials by z^5, z^3, z^6). Klein's 1878 paper itself was not read; note LNR call "
     "the mirror form xy^3+yz^3+zx^3 'Klein's quartic', so 'Klein's own copy' is a coordinate-labelling convention."),
    ("the copy holding <D, 120 deg turn> is Klein's conjugated by -(x<->z), and preserves xy^3+yz^3+zx^3",
     "CONFIRMED", "exact set equality; it is also LNR's published basis, and it is the unique PSL(2,7) in U(3) "
                  "containing <D, C> (argument closed by computed facts: Aut(F21) induced by PGL(2,7), degree equation)."),
    ("flavor model-builders have used both groups as family symmetries", "CONFIRMED (cited)",
     "literature (LNR 2007 [read]; PLAN §3 found no correction); not computed by E0."),
    ("G2 contains SU(3) as the subgroup fixing one imaginary octonion (Gunaydin-Gursey)", "CONFIRMED (partly cited)",
     "extra exact check at the Lie-algebra level: Der(O) is g2 (dim 14), derivations killing e form su(3) (dim 8), and "
     "the SU(3) matrices act as automorphisms fixing e. Cited, not recomputed: the group-level statement that the "
     "stabiliser of e in G2 is exactly SU(3) (Gunaydin-Gursey 1973)."),
    ("G2's affine Weyl group is exactly p6m", "CONFIRMED",
     "Lambda ⋊ D6 with Coxeter (2,3,6); site symmetries 6mm, 3m (x2), 2mm (x3) per cell."),
    ("SU(3)'s Weyl group has only the 120 deg turns and three mirrors; G2's (order 12) adds 60, 180, 300 deg turns",
     "CONFIRMED", "exact orders 6 and 12 (G2 also adds three mirrors)."),
    ("those turns keep the seven points (x -> 5x, 6x, 3x) but swap the two Fano families", "CONFIRMED",
     "exact; the 60/180/300 deg turns are x -> 5x, 6x, 3x."),
    ("no mirror in either group keeps the seven points", "CONFIRMED",
     "0 of 3 and 0 of 6; also no mirror of either affine Weyl group. Reason: the 7-vertex torus is chiral "
     "(all 42 automorphisms preserve orientation); SU(3)'s mirrors swap D's order-7 subgroup with diag(z,z^4,z^2)'s."),
    ("F21, PSL(2,7) and the Fano split belong to the SU(3) rung; the turns completing p6m arrive with G2 and swap the "
     "families; they don't stack into one clean tower", "CONFIRMED",
     "every factual clause holds (verdict changed from AMENDED in the reconciliation, Oct 19: the amendment concerned "
     "interpretation, not fact). Wording refinement suggested: the groups do form a chain G2 ⊃ SU(3)⋊Z2 ⊃ PGL(2,7) ⊃ "
     "PSL(2,7) ⊃ F21, because the family-swapping G2 turn (180 deg = complex conjugation kappa) normalises the "
     "flipped PSL(2,7) and gives PGL(2,7) = Aut(PSL(2,7)) of order 336 inside G2 (kappa C^{±1} realise the 60 and 300 "
     "deg turns); the two Fano families are the two classes of S4, which this outer automorphism swaps, so the family "
     "split survives only up to PSL(2,7), as the seed says."),
]

results = dict(
    experiment="E0_hexagon_exact",
    plan_section="seed/PLAN.md §4 E0",
    conventions=dict(
        zeta="exp(2 pi i/7); Q(zeta) elements stored exactly as rational vectors modulo 1+x+...+x^6",
        i_over_sqrt7="(z+z^2+z^4 - z^3-z^5-z^6)/7 (quadratic Gauss sum G = +i sqrt7)",
        b7="z+z^2+z^4 = (-1+i sqrt7)/2",
        torus="theta in {theta1+theta2+theta3 = 0} -> diag(exp(2 pi i theta)); Lambda = Z^3 ∩ plane",
        seven_points="j*p, p = (1,2,-3)/7 <-> D^j",
        families="'up' = {x, x+a, x+c}, 'down' = {x+a, x+c, x+a+c}, a = p, c = p + roll(p)",
        angles="measured from u = (1,-1,0) toward w = (1,1,-2), as in hexagon_check.py",
        A5="real orthogonal 3x3 over Q(sqrt5): 3-fold rotation about (1,1,1) and 2-fold rotation about (1, phi^2, phi)",
        octonions="O = C ⊕ C^3, (a,u)(b,v) = (ab - sum u_i conj v_i, a v + conj(b) u + conj(u x v))"),
    headline=headline,
    seed_claims=[dict(claim=c_, verdict=v_, evidence=e_) for c_, v_, e_ in seed_claims],
    n_checks=len(CHECKS), n_pass=n_pass, all_pass=(n_pass == len(CHECKS)),
    checks=CHECKS,
    values=VALUES,
    runtime_seconds=round(runtime, 1),
    software=dict(python=sys.version.split()[0]),
)


def _default(o):
    if isinstance(o, F):
        return str(o)
    return str(o)


with open(os.path.join(HERE, "results.json"), "w") as fh:
    json.dump(results, fh, indent=1, default=_default, ensure_ascii=False)
print("wrote results.json, exact_replica_output.txt, hexagon_check_original_output.txt")
sys.exit(0 if n_pass == len(CHECKS) else 1)
