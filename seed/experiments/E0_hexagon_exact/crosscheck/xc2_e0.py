"""
xc2_e0.py -- second-round independent cross-check of experiment E0 (seed/PLAN.md §4).

Written from PLAN.md, SEED.md, seed/hexagon_check.py, the E0 report and its
results.json only, before reading the original E0 scripts.  Every decision is
exact (sympy's algebraic field QQ<zeta7>, Fractions, integers); the single
float use is the sign of the Gauss sum (which only swaps b7 and its conjugate).

Methods (chosen to differ from the original E0 code and from the earlier
cross-check xc_e0.py in this folder, see xc2_lib.py):
  - group orders by an exact projective orbit-stabiliser chain;
  - explicit isomorphism onto PSL(2,F7) on P^1(F7) via Sylow-7 subgroups;
  - subgroup lattice by 2-generated closures + a join-closure proof;
  - icosahedral group by brute force over vertex images;
  - lattices, Weyl and affine Weyl groups in integer Lambda coordinates;
  - rotation centres from the fixed-point equation (1 - w) x = t (mod Lambda);
  - octonions by Cayley-Dickson doubling of the quaternions.

Run (about 40 s, one thread):
  NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 xc2_e0.py
Writes xc2_checks.json and xc2_replica_lines.txt next to this file; exit code 0 iff all checks pass.
"""
import itertools
import json
import os
import subprocess
import sys
import time
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xc2_lib import *  # noqa: E402,F401,F403
import xc2_lib as L  # noqa: E402

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []
VALUES = {}


def check(sec, name, ok, detail=""):
    ok = bool(ok)
    CHECKS.append({"section": sec, "name": name, "ok": ok, "detail": str(detail)})
    print(f"[{'PASS' if ok else 'FAIL'}] {sec}: {name}" + (f"  -- {detail}" if detail != "" else ""), flush=True)


# ============================================================ A. the field Q(zeta7)
mp = K.ext.minpoly
check("A", "sympy's minimal polynomial of exp(2 pi i/7) is x^6+x^5+...+1 (Phi_7)",
      [int(c) for c in mp.all_coeffs()] == [1] * 7, str(mp.as_expr()))
G = zp(1) + zp(2) + zp(4) - zp(3) - zp(5) - zp(6)
check("A", "Gauss sum G = (z+z^2+z^4) - (z^3+z^5+z^6): G^2 = -7 exactly", G * G == K(-7))
gf = kfloat(G)
check("A", "sign: G evaluates to +i sqrt7 (the only float decision)", abs(gf - 7 ** 0.5 * 1j) < 1e-12, f"{gf:.12f}")
b7 = zp(1) + zp(2) + zp(4)
b7bar = kconj(b7)
check("A", "b7 = z+z^2+z^4 = (-1+G)/2 and conj(b7) = z^3+z^5+z^6 = (-1-G)/2; b7 != conj(b7) (not real)",
      b7 * 2 == G - K1 and b7bar * 2 == -G - K1 and b7 != b7bar and b7bar == zp(3) + zp(5) + zp(6))
I_OVER_SQRT7 = G / K(7)        # i/sqrt7
check("A", "(i/sqrt7)^2 = -1/7 with i/sqrt7 := G/7", I_OVER_SQRT7 * I_OVER_SQRT7 == K(-1) / K(7))
VALUES["b7"] = "z+z^2+z^4 = (-1+G)/2, G^2 = -7, G = +i sqrt7"

# ============================================================ B. torus and lattices (Lambda coordinates)
print(f"--- section B start at {time.time() - T0:.1f} s", flush=True)
GR = [[2, -1], [-1, 2]]                       # Gram of b1 = (1,-1,0), b2 = (0,1,-1)


def dot(x, y):
    return sum(Fr(x[i]) * GR[i][j] * Fr(y[j]) for i in range(2) for j in range(2))


def from3(v):                                 # R^3 plane vector -> Lambda coords (m, n)
    assert sum(v) == 0
    return (Fr(v[0]), Fr(v[0]) + Fr(v[1]))


def to3(c):
    m, n = c
    return (m, n - m, -n)


def is_int2(c):
    return all(Fr(x).denominator == 1 for x in c)


# Lambda = Z^3 ∩ plane: integer coords <=> integer R^3 vector
ok = all(is_int2(from3((a, b, -a - b))) for a in range(-5, 6) for b in range(-5, 6))
ok &= all(all(Fr(x).denominator == 1 for x in to3((m, n))) for m in range(-5, 6) for n in range(-5, 6))
check("B", "Lambda = Z^3 ∩ {sum 0} has basis b1, b2 (integer vectors <-> integer coordinates); Gram [[2,-1],[-1,2]] (hexagonal)",
      ok and dot((1, 0), (1, 0)) == 2 and dot((0, 1), (0, 1)) == 2 and dot((1, 0), (0, 1)) == -1)
# kernel of theta -> diag(exp 2 pi i theta) on the plane is exactly the integer vectors: trivially Z^3 ∩ plane
w1, w2 = from3((Fr(2, 3), Fr(-1, 3), Fr(-1, 3))), from3((Fr(1, 3), Fr(1, 3), Fr(-2, 3)))
check("B", "weight lattice (dual of Lambda in the plane): w1, w2 with <wi,bj> = delta_ij, Gram (1/3)[[2,1],[1,2]] (hexagonal)",
      dot(w1, (1, 0)) == 1 and dot(w1, (0, 1)) == 0 and dot(w2, (1, 0)) == 0 and dot(w2, (0, 1)) == 1
      and dot(w1, w1) == Fr(2, 3) and dot(w2, w2) == Fr(2, 3) and dot(w1, w2) == Fr(1, 3))
# weights of the 3: e_i - (1,1,1)/3
wt3 = [from3(tuple(Fr(int(i == k)) - Fr(1, 3) for i in range(3))) for k in range(3)]
# octet = 3 x 3bar minus singlet: weights wt3[i] - wt3[j] (all pairs) minus one zero
octet = [tuple(a - b for a, b in zip(wt3[i], wt3[j])) for i in range(3) for j in range(3)]
octet.remove((0, 0))
nz = [v for v in octet if v != (0, 0)]
hexa = len(nz) == 6 and len(set(nz)) == 6 and len(set(dot(v, v) for v in nz)) == 1
if hexa:
    r = dot(nz[0], nz[0])
    for v in nz:
        cos2 = sorted(dot(v, u) / r for u in nz if u != v)
        hexa &= cos2 == [-1, Fr(-1, 2), Fr(-1, 2), Fr(1, 2), Fr(1, 2)]
check("B", "octet weights (3 x 3bar - 1): 6 distinct equal-length weights forming a regular hexagon + the zero weight twice",
      hexa and octet.count((0, 0)) == 2)
dec = [tuple(sum(c) for c in zip(*[wt3[i] for i in t])) for t in itertools.combinations_with_replacement(range(3), 3)]
corners = [tuple(3 * x for x in wt3[k]) for k in range(3)]


def on_segment(x, a, b):
    d1 = tuple(p - q for p, q in zip(x, a))
    d2 = tuple(p - q for p, q in zip(b, a))
    return d1[0] * d2[1] - d1[1] * d2[0] == 0 and 0 <= dot(d1, d2) <= dot(d2, d2)


sides = [sum(on_segment(x, corners[i], corners[(i + 1) % 3]) for x in dec) for i in range(3)]
check("B", "decuplet (Sym^3 of the 3): 10 distinct weights, multiplicity 1, filling the triangle with corners 3*wt(3), 4 weights per side",
      len(dec) == 10 and len(set(dec)) == 10 and sides == [4, 4, 4], f"sides {sides}")

P = from3((Fr(1, 7), Fr(2, 7), Fr(-3, 7)))     # point 1 <-> D = diag(z, z^2, z^4)
check("B", "p = (1,2,-3)/7 gives exp(2 pi i p) = diag(z, z^2, z^4) = D (exponents 1,2,-3 = 1,2,4 mod 7)",
      [x % 7 for x in (1, 2, -3)] == [1, 2, 4], f"Lambda coords {P}")


def label(x):
    """j with x - j p in Lambda, else None"""
    for j in range(7):
        if is_int2((x[0] - j * P[0], x[1] - j * P[1])):
            return j
    return None


pts = [(j * P[0] % 1, j * P[1] % 1) for j in range(7)]
check("B", "the seven points j p are distinct mod Lambda and 7p is in Lambda",
      len(set(pts)) == 7 and is_int2((7 * P[0], 7 * P[1])))
rollp = from3((Fr(-3, 7), Fr(1, 7), Fr(2, 7)))   # np.roll((1,2,-3)/7, 1)
check("B", "the 120 deg turn theta -> roll(theta) sends point 1 to point 4", label(rollp) == 4, f"label {label(rollp)}")

# finer lattice L' = Lambda + Z p: vectors (a/7, b/7) with b = 3a (mod 7)
cands = [(Fr(a, 7), Fr(b, 7)) for a in range(-14, 15) for b in range(-14, 15) if (b - 3 * a) % 7 == 0 and (a, b) != (0, 0)]
mn = min(dot(v, v) for v in cands)
short = [v for v in cands if dot(v, v) == mn]
check("B", "Lambda + Zp: minimal norm^2 2/7, attained by exactly 6 vectors", mn == Fr(2, 7) and len(short) == 6, f"{mn}, {len(short)}")
# index: basis (p, (0,1)) of L'; det in Lambda coords
check("B", "Lambda + Zp = Z p + Z (0,1) has covolume 1/7 relative to Lambda: index 7",
      P[0] * 1 - P[1] * 0 == Fr(1, 7) and all(label(v) is not None for v in cands))
# reduced basis a, c at 60 deg, positively oriented
a_vec = None
for a in short:
    for c in short:
        if dot(a, c) == mn / 2 and a[0] * c[1] - a[1] * c[0] > 0:
            a_vec, c_vec = a, c
            break
    if a_vec:
        break
gram7 = [[dot(a_vec, a_vec), dot(a_vec, c_vec)], [dot(c_vec, a_vec), dot(c_vec, c_vec)]]
check("B", "a reduced basis (a, c) of Lambda + Zp has Gram (1/7)[[2,1],[1,2]] (60 deg; equivalently (1/7)[[2,-1],[-1,2]] for (a, c-a)): hexagonal",
      gram7 == [[Fr(2, 7), Fr(1, 7)], [Fr(1, 7), Fr(2, 7)]]
      and dot(a_vec, tuple(x - y for x, y in zip(c_vec, a_vec))) == Fr(-1, 7))
ring = sorted(label(v) for v in short)
check("B", "the six shortest vectors carry labels 1..6: K7", ring == [1, 2, 3, 4, 5, 6], str(ring))
la, lc = label(a_vec), label(c_vec)
up = {tuple(sorted(((j) % 7, (j + la) % 7, (j + lc) % 7))) for j in range(7)}
down = {tuple(sorted(((j + la) % 7, (j + lc) % 7, (j + la + lc) % 7))) for j in range(7)}
check("B", "14 distinct triangles in two families of 7 (up / down triangles of the finer lattice)",
      len(up) == 7 and len(down) == 7 and len(up | down) == 14, f"labels of a, c: {la}, {lc}")


def is_fano(S):
    prs = [pr for t in S for pr in itertools.combinations(sorted(t), 2)]
    return len(S) == 7 and len(prs) == 21 and len(set(prs)) == 21


OCT = {tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)}
OTHER = {tuple(sorted((i % 7, (i + 2) % 7, (i + 3) % 7))) for i in range(7)}
fam_names = {"up": up, "down": down}
oct_fam = [n for n, S in fam_names.items() if S == OCT]
check("B", "both families are Fano planes; one is exactly the octonion lines {i,i+1,i+3}, the other {i,i+2,i+3}",
      is_fano(up) and is_fano(down) and len(oct_fam) == 1 and {frozenset(up), frozenset(down)} == {frozenset(OCT), frozenset(OTHER)},
      f"octonion family = '{oct_fam[0] if oct_fam else None}' for (a, c) labels ({la}, {lc})")
TRI = up | down
edge_count = {}
for t in TRI:
    for e in itertools.combinations(t, 2):
        edge_count[e] = edge_count.get(e, 0) + 1
check("B", "21 edges = all pairs, each in exactly 2 triangles", len(edge_count) == 21 and set(edge_count.values()) == {2})


def links_ok(tris, verts):
    for v in verts:
        es = [tuple(x for x in t if x != v) for t in tris if v in t]
        adj = {}
        for x, y in es:
            adj.setdefault(x, []).append(y)
            adj.setdefault(y, []).append(x)
        if any(len(n) != 2 for n in adj.values()):
            return False
        start = es[0][0]
        seen, prev, cur = {start}, None, start
        while True:
            nxt = [n for n in adj[cur] if n != prev]
            prev, cur = cur, nxt[0]
            if cur == start:
                break
            seen.add(cur)
        if len(seen) != len(adj):
            return False
    return True


check("B", "every vertex link is a single 6-cycle (closed surface)", links_ok(TRI, range(7))
      and all(sum(v in t for t in TRI) == 6 for v in range(7)))
# orientation from the plane: up (j, j+a, j+c), down (j+a, j+a+c, j+c) are counter-clockwise (det(a,c) > 0)
ORIENTED = [((j) % 7, (j + la) % 7, (j + lc) % 7) for j in range(7)] + \
           [((j + la) % 7, (j + la + lc) % 7, (j + lc) % 7) for j in range(7)]
dedges = [(t[i], t[(i + 1) % 3]) for t in ORIENTED for i in range(3)]
check("B", "orientable: with the plane's orientation every directed edge occurs exactly once (42 directed edges)",
      len(dedges) == 42 and len(set(dedges)) == 42)
V, E, F = 7, len(edge_count), len(TRI)
check("B", "Euler characteristic V - E + F = 7 - 21 + 14 = 0", (V, E, F, V - E + F) == (7, 21, 14, 0), f"{V} - {E} + {F} = {V - E + F}")
check("B", "triangulation = {i,i+1,i+3} ∪ {i,i+2,i+3} (the Moebius/Csaszar labelling)", TRI == OCT | OTHER)
VALUES["triangulation"] = {"V": V, "E": E, "F": F, "chi": V - E + F, "octonion_family": oct_fam[0] if oct_fam else None,
                           "labels_a_c": [la, lc]}

# ============================================================ C. Fano planes on 7 labels
print(f"--- section C start at {time.time() - T0:.1f} s", flush=True)
ALL_TRIPLES = list(itertools.combinations(range(7), 3))


def sts7():
    out = []

    def rec(chosen, covered):
        if len(covered) == 21:
            out.append(frozenset(chosen))
            return
        pr = next(pq for pq in itertools.combinations(range(7), 2) if pq not in covered)
        i, j = pr
        for k in range(7):
            if k in pr:
                continue
            t = tuple(sorted((i, j, k)))
            ps = list(itertools.combinations(t, 2))
            if any(q in covered for q in ps):
                continue
            rec(chosen + [t], covered | set(ps))
    rec([], frozenset())
    return out


FANO = sts7()
check("C", "backtracking over Steiner triple systems: exactly 30 Fano planes on 7 labels", len(FANO) == 30 and len(set(FANO)) == 30, len(FANO))
cyc = [S for S in FANO if {tuple(sorted((x + 1) % 7 for x in t)) for t in S} == set(S)]
check("C", "exactly 2 are invariant under x -> x+1, and they are exactly the two torus families",
      len(cyc) == 2 and set(cyc) == {frozenset(up), frozenset(down)}, len(cyc))
S7 = list(itertools.permutations(range(7)))


def img(S, perm):
    return frozenset(tuple(sorted(perm[x] for x in t)) for t in S)


autA = {g for g in S7 if img(up, g) == frozenset(up)}
autB = {g for g in S7 if img(down, g) == frozenset(down)}
affine = {(a, b): tuple((a * x + b) % 7 for x in range(7)) for a in range(1, 7) for b in range(7)}
F21_lab = {affine[(a, b)] for a in (1, 2, 4) for b in range(7)}
check("C", "|Aut(up)| = |Aut(down)| = 168 (brute force over S7); Aut(up) ∩ Aut(down) = {x -> ax+b : a in {1,2,4}} (order 21)",
      len(autA) == 168 and len(autB) == 168 and (autA & autB) == F21_lab, f"{len(autA)}, {len(autB)}, {len(autA & autB)}")
check("C", "x -> ax+b with a in {3,5,6} swaps the two families",
      all(img(up, affine[(a, b)]) == frozenset(down) and img(down, affine[(a, b)]) == frozenset(up) for a in (3, 5, 6) for b in range(7)))
VALUES["fano"] = {"total": len(FANO), "cyclic": len(cyc), "aut_order": len(autA), "aut_intersection": len(autA & autB)}

# ============================================================ D. 7-vertex surfaces
print(f"--- section D start at {time.time() - T0:.1f} s", flush=True)
def pair_degree2_complexes():
    """all sets of distinct triangles on 7 vertices in which every pair lies in exactly 2 triangles"""
    found = set()
    pairs = list(itertools.combinations(range(7), 2))

    def rec(chosen, deg):
        pr = next((pq for pq in pairs if deg[pq] < 2), None)
        if pr is None:
            found.add(frozenset(chosen))
            return
        i, j = pr
        for k in range(7):
            if k in pr:
                continue
            t = tuple(sorted((i, j, k)))
            if t in chosen:
                continue
            ps = list(itertools.combinations(t, 2))
            if any(deg[q] >= 2 for q in ps):
                continue
            for q in ps:
                deg[q] += 1
            rec(chosen | {t}, deg)
            for q in ps:
                deg[q] -= 1
    rec(frozenset(), {pq: 0 for pq in pairs})
    return found


def orientable(tris):
    tris = list(tris)
    ori = {tris[0]: tris[0]}
    queue = [tris[0]]
    while queue:
        t = queue.pop()
        o = ori[t]
        de = {(o[i], o[(i + 1) % 3]) for i in range(3)}
        for s in tris:
            if s in ori or len(set(s) & set(t)) != 2:
                continue
            # orient s so that the shared edge runs opposite
            for cand in (s, (s[0], s[2], s[1])):
                ce = {(cand[i], cand[(i + 1) % 3]) for i in range(3)}
                if not (ce & de):
                    ori[s] = cand
                    queue.append(s)
                    break
    if len(ori) != len(tris):
        return False
    alld = [(o[i], o[(i + 1) % 3]) for o in ori.values() for i in range(3)]
    return len(alld) == len(set(alld))


cx = pair_degree2_complexes()
surf = [S for S in cx if links_ok(S, range(7))]
orient = [S for S in surf if orientable(S)]
autT = [g for g in S7 if img(TRI, g) == frozenset(TRI)]
orbit = {img(TRI, g) for g in S7}
check("D", "every 7-vertex complex with each pair in exactly 2 triangles (= every 7-vertex triangulated surface with chi = 0, since chi = 0 forces E = 21) is a closed orientable surface, and all are relabellings of ours",
      len(cx) == len(surf) == len(orient) == len(orbit) == 120 and set(cx) == orbit,
      f"{len(cx)} complexes, {len(surf)} surfaces, {len(orient)} orientable, orbit {len(orbit)}")
check("D", "|Aut(triangulation)| = 42 = {x -> ax+b, a != 0} = AGL(1,7) (brute force over S7)",
      len(autT) == 42 and set(autT) == set(affine.values()))
or_set = set(ORIENTED)


def cyc_norm(t):
    i = t.index(min(t))
    return t[i:] + t[:i]


or_norm = {cyc_norm(t) for t in ORIENTED}
pres = sum(all(cyc_norm(tuple(g[x] for x in t)) in or_norm for t in ORIENTED) for g in autT)
check("D", "all 42 automorphisms preserve the orientation: the 7-vertex torus is chiral", pres == 42, f"{pres} of 42")
# the report's check title says "every 7-vertex triangulated closed surface is an orientable torus": counterexamples
bipyr = {tuple(sorted((i, (i + 1) % 5, 5))) for i in range(5)} | {tuple(sorted((i, (i + 1) % 5, 6))) for i in range(5)}
ee = {e for t in bipyr for e in itertools.combinations(t, 2)}
hemi = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 1), (1, 2, 4), (2, 3, 5), (3, 4, 1), (4, 5, 2), (5, 1, 3)]
hemi = {tuple(sorted(t)) for t in hemi}
# subdivide triangle (0,1,2) of the 6-vertex RP^2 by a new vertex 6
rp2 = (hemi - {(0, 1, 2)}) | {(0, 1, 6), (1, 2, 6), (0, 2, 6)}
er = {e for t in rp2 for e in itertools.combinations(t, 2)}
check("D", "(audit) 7-vertex triangulations of the sphere (pentagonal bipyramid, chi 2) and of RP^2 (chi 1, non-orientable) exist, so 'every 7-vertex triangulated closed surface is an orientable torus' is false unless restricted to chi = 0",
      links_ok(bipyr, range(7)) and 7 - len(ee) + len(bipyr) == 2 and links_ok(rp2, range(7))
      and 7 - len(er) + len(rp2) == 1 and not orientable(rp2) and orientable(bipyr))
VALUES["torus7_uniqueness"] = {"complexes": len(cx), "surfaces": len(surf), "orientable": len(orient), "orbit": len(orbit),
                               "aut_order": len(autT), "orientation_preserving": pres}

# ============================================================ E. the groups inside SU(3)
print(f"--- section E start at {time.time() - T0:.1f} s", flush=True)
Dm = M([[zp(1), 0, 0], [0, zp(2), 0], [0, 0, zp(4)]])
Dk = M([[zp(4), 0, 0], [0, zp(2), 0], [0, 0, zp(1)]])
Cm = M([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
s_ = lambda a, b: I_OVER_SQRT7 * (zp(a) - zp(b))
Rm = M([[s_(1, 6), s_(2, 5), s_(4, 3)], [s_(2, 5), s_(4, 3), s_(1, 6)], [s_(4, 3), s_(1, 6), s_(2, 5)]])
flip = M([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])
Rf = mmul(mmul(flip, Rm), minv(flip))
check("E", "D, Dk, C, R, flip are in SU(3); D^7 = 1, C^3 = 1, R^2 = 1, flip^2 = 1",
      all(in_SU3(X) for X in (Dm, Dk, Cm, Rm, flip)) and morder(Dm) == 7 and morder(Cm) == 3 and morder(Rm) == 2 and morder(flip) == 2)
Ci = minv(Cm)
check("E", "C^-1 D C = D^4 and C D C^-1 = D^2 (the 120 deg turn acts on the labels as x -> 4x; the opposite turn as x -> 2x)",
      mmul(mmul(Ci, Dm), Cm) == mpow(Dm, 4) and mmul(mmul(Cm, Dm), Ci) == mpow(Dm, 2))
check("E", "flip Dk flip^-1 = D", mmul(mmul(flip, Dk), minv(flip)) == Dm)

print(f"    ({time.time() - T0:.1f} s) o21, s21 = stabiliser_chain_or", flush=True)
o21, s21 = stabiliser_chain_order([Dm, Cm])
oK, sK = stabiliser_chain_order([Dk, Cm, Rm])
oF, sF = stabiliser_chain_order([Dm, Cm, Rf])
check("E", "orbit-stabiliser chain on projective points: |<D, C>| = 21, |<Dk, C, R>| = 168, |<D, C, Rf>| = 168",
      (o21, oK, oF) == (21, 168, 168), f"orbit sizes of [e1],[e2],[e3],[1:1:1], scalars: {s21}, {sK}, {sF}")
F21 = closure([Dm, Cm])
KL = closure([Dk, Cm, Rm])
FL = closure([Dm, Cm, Rf])
VALUES["group_orders"] = {"F21": o21, "Klein_copy": oK, "flipped_copy": oF, "method": "projective orbit-stabiliser chain", "orbit_sizes": {"F21": s21, "Klein_copy": sK, "flipped_copy": sF}}
check("E", "explicit enumeration agrees (21, 168, 168) and every element is exactly unitary with det 1",
      (len(F21), len(KL), len(FL)) == (21, 168, 168) and all(in_SU3(X) for X in F21 + KL + FL))
kKL = {mkey(X) for X in KL}
kFL = {mkey(X) for X in FL}
kF21 = {mkey(X) for X in F21}
check("E", "D is not in Klein's copy; <D, C> is inside the flipped copy", mkey(Dm) not in kKL and kF21 <= kFL)
fi = minv(flip)
check("E", "flipped copy = flip (Klein's copy) flip^-1 as sets", {mkey(mmul(mmul(flip, X), fi)) for X in KL} == kFL)


# quartics: exact polynomial arithmetic over K
def poly_mul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(a + b for a, b in zip(m1, m2))
            r[m] = r.get(m, K0) + c1 * c2
    return {m: c for m, c in r.items() if c != K0}


def poly_add(p, q):
    r = dict(p)
    for m, c in q.items():
        r[m] = r.get(m, K0) + c
    return {m: c for m, c in r.items() if c != K0}


def lin(row):
    return {m: c for m, c in zip(((1, 0, 0), (0, 1, 0), (0, 0, 1)), row) if c != K0}


def quartic_after(A, kind):
    """q(A x) as a polynomial in x; kind 'klein' = x^3y+y^3z+z^3x, 'mirror' = xy^3+yz^3+zx^3"""
    Lf = [lin(A[3 * i:3 * i + 3]) for i in range(3)]
    cube = [poly_mul(poly_mul(l, l), l) for l in Lf]
    if kind == "klein":
        terms = [poly_mul(cube[0], Lf[1]), poly_mul(cube[1], Lf[2]), poly_mul(cube[2], Lf[0])]
    else:
        terms = [poly_mul(Lf[0], cube[1]), poly_mul(Lf[1], cube[2]), poly_mul(Lf[2], cube[0])]
    out = {}
    for t in terms:
        out = poly_add(out, t)
    return out


print(f"    ({time.time() - T0:.1f} s) QK = quartic_after(IDENT", flush=True)
QK = quartic_after(IDENT, "klein")
QM = quartic_after(IDENT, "mirror")
check("E", "Klein quartic x^3y+y^3z+z^3x is invariant (exact polynomial identity) under Dk, C, R, hence under the group; also checked on all 168 elements",
      all(quartic_after(X, "klein") == QK for X in (Dk, Cm, Rm)) and all(quartic_after(X, "klein") == QK for X in KL))
check("E", "mirror quartic xy^3+yz^3+zx^3 is invariant (exact) under D, C, Rf and all 168 elements of the flipped copy",
      all(quartic_after(X, "mirror") == QM for X in (Dm, Cm, Rf)) and all(quartic_after(X, "mirror") == QM for X in FL))
check("E", "D does not keep the Klein quartic and Rf does not either; R does not keep the mirror quartic",
      quartic_after(Dm, "klein") != QK and quartic_after(Rf, "klein") != QK and quartic_after(Rm, "mirror") != QM)
# diagonal symmetries diag(a,b,c) with abc = 1 keeping x^3y+y^3z+z^3x: a^3 b = b^3 c = c^3 a = 1 forces a^7 = 1, (a,b,c) = (a, a^-3, a^9)
diagK = [(e1, e2, e3) for e1 in range(7) for e2 in range(7) for e3 in range(7)
         if (e1 + e2 + e3) % 7 == 0 and (3 * e1 + e2) % 7 == 0 and (3 * e2 + e3) % 7 == 0 and (3 * e3 + e1) % 7 == 0]
diagM = [(e1, e2, e3) for e1 in range(7) for e2 in range(7) for e3 in range(7)
         if (e1 + e2 + e3) % 7 == 0 and (e1 + 3 * e2) % 7 == 0 and (e2 + 3 * e3) % 7 == 0 and (e3 + 3 * e1) % 7 == 0]
check("E", "diagonal SU(3) symmetries of x^3y+y^3z+z^3x (a^3b = b^3c = c^3a = 1, abc = 1 forces a^7 = 1) are exactly the powers of Dk; those of the mirror quartic are exactly the powers of D",
      sorted(diagK) == sorted(((4 * j) % 7, (2 * j) % 7, j % 7) for j in range(7))
      and sorted(diagM) == sorted((j % 7, (2 * j) % 7, (4 * j) % 7) for j in range(7)))

# LNR generators (arXiv:0709.1447v2 eqs. 22, 23, read by me in the PDF text)
eta = zp
c7 = I_OVER_SQRT7
B_lnr = M([[c7 * (eta(3) - eta(6)), c7 * (eta(3) - eta(1)), c7 * (eta(1) - K1)],
           [c7 * (eta(2) - K1), c7 * (eta(6) - eta(5)), c7 * (eta(6) - eta(2))],
           [c7 * (eta(5) - eta(4)), c7 * (eta(4) - K1), c7 * (eta(5) - eta(3))]])
A_lnr = M([[c7 * (eta(2) - eta(5)), c7 * (eta(1) - eta(6)), c7 * (eta(4) - eta(3))],
           [c7 * (eta(1) - eta(6)), c7 * (eta(4) - eta(3)), c7 * (eta(2) - eta(5))],
           [c7 * (eta(4) - eta(3)), c7 * (eta(2) - eta(5)), c7 * (eta(1) - eta(6))]])
AB = mmul(A_lnr, B_lnr)
comm = mmul(mmul(A_lnr, B_lnr), mmul(minv(A_lnr), minv(B_lnr)))
check("E", "LNR eqs. (22)-(23): A, B in SU(3) with A^2 = B^3 = (AB)^7 = [A,B]^4 = 1, AB = D (their eq. 16), A = Rf",
      in_SU3(A_lnr) and in_SU3(B_lnr) and morder(A_lnr) == 2 and morder(B_lnr) == 3 and morder(AB) == 7
      and morder(comm) == 4 and AB == Dm and A_lnr == Rf)
LNRG = closure([A_lnr, B_lnr])
check("E", "LNR's <A, B> is exactly the flipped copy (same 168 matrices); LNR eq. (78) phi1^3 phi3 + phi3^3 phi2 + phi2^3 phi1 is the mirror quartic",
      {mkey(X) for X in LNRG} == kFL and QM == poly_add(poly_add(poly_mul(poly_mul(poly_mul(lin((K1, K0, K0)), lin((K1, K0, K0))), lin((K1, K0, K0))), lin((K0, K0, K1))),
                                                                  poly_mul(poly_mul(poly_mul(lin((K0, K0, K1)), lin((K0, K0, K1))), lin((K0, K0, K1))), lin((K0, K1, K0)))),
                                                         poly_mul(poly_mul(poly_mul(lin((K0, K1, K0)), lin((K0, K1, K0))), lin((K0, K1, K0))), lin((K1, K0, K0)))))


# ---- explicit isomorphism onto PSL(2,F7) via the 8 Sylow-7 subgroups
def sylow7(Gl):
    subs = {}
    for X in Gl:
        if morder(X, 8) == 7:
            S = frozenset(mkey(mpow(X, k)) for k in range(7))
            subs[S] = X
    return list(subs.keys())


def perm_on_sylows(Gl, syl, gens_semilinear=None):
    """conjugation action of each element on the Sylow-7 subgroups (as permutations of range(8))"""
    index = {S: i for i, S in enumerate(syl)}
    elem = {mkey(X): X for X in Gl}
    gen_of = {}
    for S in syl:
        gen_of[S] = next(elem[k] for k in S if elem[k] != IDENT)
    which = {k: index[S] for S in syl for k in S if k != mkey(IDENT)}     # element of order 7 -> its Sylow subgroup
    out = {}
    for X in Gl:
        Xi = minv(X)
        perm = []
        for S in syl:
            h = mmul(mmul(X, gen_of[S]), Xi)
            perm.append(which[mkey(h)])
        out[mkey(X)] = tuple(perm)
    return out


PSLstd = psl27_standard()
PGLstd = frozenset(mobius(a, b, c, d) for a, b, c, d in itertools.product(range(7), repeat=4) if (a * d - b * c) % 7 != 0)
check("E", "reference PSL(2,F7) on P^1(F7): 168 Moebius maps (ad-bc = 1); PGL(2,F7): 336",
      len(PSLstd) == 168 and len(PGLstd) == 336 and PSLstd <= PGLstd)


def iso_to_psl(Gl):
    syl = sylow7(Gl)
    act = perm_on_sylows(Gl, syl)
    image = set(act.values())
    tau = next(p for p in image if porder(p) == 7)
    for t in (tau, pmul(tau, pmul(tau, tau))):
        fixed = [i for i in range(8) if t[i] == i][0]
        for q0 in range(8):
            if q0 == fixed:
                continue
            phi = {fixed: INF}
            q = q0
            for k in range(7):
                phi[q] = k
                q = t[q]
            phi_t = tuple(phi[i] for i in range(8))
            phinv = pinv(phi_t)
            conj = {k: pmul(pmul(phi_t, p), phinv) for k, p in act.items()}
            if set(conj.values()) == PSLstd:
                return syl, act, phi_t, conj
    return syl, act, None, None


print(f"    ({time.time() - T0:.1f} s) sylF, actF, phiF, isoF = iso_t", flush=True)
sylF, actF, phiF, isoF = iso_to_psl(FL)
sylK, actK, phiK, isoK = iso_to_psl(KL)
check("E", "each copy has 8 Sylow-7 subgroups; conjugation on them, transported by a bijection to P^1(F7), maps the 168 matrices bijectively onto PSL(2,F7): an explicit isomorphism (no appeal to uniqueness of the simple group of order 168)",
      len(sylF) == 8 and len(sylK) == 8 and isoF is not None and isoK is not None
      and len(set(isoF.values())) == 168 and len(set(isoK.values())) == 168)
# homomorphism check on random products (it is a conjugation action, so automatic; verify anyway)
elF = {mkey(X): X for X in FL}
hom_ok = all(isoF[mkey(mmul(X, Y))] == pmul(isoF[mkey(X)], isoF[mkey(Y)]) for X in FL[:40] for Y in FL[::7])
check("E", "the map is multiplicative (checked on 40 x 24 pairs)", hom_ok)


def class_data(Gl, iso):
    """classes via the permutation image; for each: size, element order, character value"""
    inv_iso = {p: k for k, p in iso.items()}
    Pimg = list(iso.values())
    cls = pclasses(Pimg)
    elk = {mkey(X): X for X in Gl}
    rows = []
    for cl in cls:
        mats = [elk[inv_iso[p]] for p in cl]
        traces = {kkey(mtrace(X)) for X in mats}
        tr = mtrace(mats[0])
        rows.append({"size": len(cl), "order": morder(mats[0]), "chi": tr, "constant": len(traces) == 1})
    return rows


def chi_name(c):
    for nm, val in (("3", K(3)), ("-1", K(-1)), ("0", K0), ("1", K1), ("b7", b7), ("b7bar", b7bar)):
        if c == val:
            return nm
    return "?"


def fs_and_inner(Gl):
    n = len(Gl)
    s_cc = sum((mtrace(X) * kconj(mtrace(X)) for X in Gl), K0) / K(n)
    s_c2 = sum((mtrace(X) * mtrace(X) for X in Gl), K0) / K(n)         # <chi, chibar>
    nu = sum((mtrace(mmul(X, X)) for X in Gl), K0) / K(n)
    return s_cc, s_c2, nu


for nm, Gl, iso in (("Klein's copy", KL, isoK), ("flipped copy", FL, isoF)):
    rows = class_data(Gl, iso)
    sig = sorted((r["size"], r["order"], chi_name(r["chi"])) for r in rows)
    cc, c2, nu = fs_and_inner(Gl)
    sizes = [r["size"] for r in rows]
    # class equation: no proper union of classes containing 1 has order dividing |G| -> simple
    others = [s for s in sizes if s != 1]
    simple = all(not (168 % (1 + sum(c)) == 0 and 1 + sum(c) not in (1, 168))
                 for r in range(0, len(others) + 1) for c in itertools.combinations(others, r))
    check("E", f"{nm}: classes (size, order, chi3) = (1,1,3) (21,2,-1) (56,3,0) (42,4,1) (24,7,b7) (24,7,b7bar); traces constant on classes",
          sig == sorted([(1, 1, "3"), (21, 2, "-1"), (56, 3, "0"), (42, 4, "1"), (24, 7, "b7"), (24, 7, "b7bar")]) and all(r["constant"] for r in rows),
          str(sig))
    check("E", f"{nm}: <chi,chi> = 1, <chi,chibar> = 0, Frobenius-Schur indicator (1/168) sum chi(g^2) = 0: complex triplet; class equation (1+21+56+42+24+24) admits no normal subgroup: simple",
          cc == K1 and c2 == K0 and nu == K0 and simple, f"<chi,chi>={chi_name(cc) if cc in (K1,) else cc}, nu={'0' if nu == K0 else nu}")
VALUES["PSL27_triplet_character"] = {"classes": "1A,2A,3A,4A,7A,7B", "sizes": [1, 21, 56, 42, 24, 24],
                                     "chi": ["3", "-1", "0", "1", "b7", "b7bar"], "frobenius_schur": 0}
check("E", "chi(D) = b7 exactly", mtrace(Dm) == b7)

# F21
f21cls = []
left = {mkey(X): X for X in F21}
while left:
    k0, X = next(iter(left.items()))
    cl = {mkey(mmul(mmul(Y, X), minv(Y))) for Y in F21}
    f21cls.append((len(cl), morder(X), chi_name(mtrace(X))))
    for k in cl:
        left.pop(k, None)
cc, c2, nu = fs_and_inner(F21)
check("E", "F21 = <D, C>: classes (size, order, chi3) = (1,1,3) (7,3,0) (7,3,0) (3,7,b7) (3,7,b7bar); <chi,chi> = 1, <chi,chibar> = 0, FS indicator 0",
      sorted(f21cls) == sorted([(1, 1, "3"), (7, 3, "0"), (7, 3, "0"), (3, 7, "b7"), (3, 7, "b7bar")]) and cc == K1 and c2 == K0 and nu == K0,
      str(sorted(f21cls)))
VALUES["F21_triplet_character"] = {"classes": "1A,3A,3B,7A,7B", "sizes": [1, 7, 7, 3, 3], "chi": ["3", "0", "0", "b7", "b7bar"], "frobenius_schur": 0}


# ---- subgroup lattice of PSL(2,7) in its degree-8 action (via the explicit isomorphism)
def subgroup_lattice(Gp):
    Gp = list(Gp)
    reps = [next(iter(c)) for c in pclasses(Gp)]
    subs = set()
    for a in reps:
        for b in Gp:
            H = pclosure([a, b], 8)
            subs.add(H)
    # close under conjugation
    allsubs = set()
    for H in subs:
        for g in Gp:
            gi = pinv(g)
            allsubs.add(frozenset(pmul(pmul(g, h), gi) for h in H))
    # join-closure proof: <H, g> is again in the list, for H over class reps and g over coset reps
    classes_ = []
    left = set(allsubs)
    while left:
        H = next(iter(left))
        cl = {frozenset(pmul(pmul(g, h), pinv(g)) for h in H) for g in Gp}
        classes_.append(cl)
        left -= cl
    join_ok = True
    for cl in classes_:
        H = next(iter(cl))
        Hl = list(H)
        gensH = Hl[:]  # small groups: use all elements as generators is slow; pick a generating pair
        for a in Hl:
            for b in Hl:
                if pclosure([a, b], 8) == H:
                    gensH = [a, b]
                    break
            else:
                continue
            break
        seen_cos = set()
        for g in Gp:
            if g in H:
                continue
            cos = frozenset(pmul(h, g) for h in H)
            if cos in seen_cos:
                continue
            seen_cos.add(cos)
            if pclosure(gensH + [g], 8) not in allsubs:
                join_ok = False
    return allsubs, classes_, join_ok


print(f"    ({time.time() - T0:.1f} s) tS = time.time()", flush=True)
tS = time.time()
SUBS, SUBCL, JOIN_OK = subgroup_lattice(PSLstd)
by_order = {}
for H in SUBS:
    by_order[len(H)] = by_order.get(len(H), 0) + 1
proper = [H for H in SUBS if len(H) < 168]
maximal = [H for H in proper if not any(H < K2 for K2 in proper)]
check("E", "subgroups of PSL(2,7) (all 2-generated closures, conjugation-closed, and closed under joins <H, g> -- hence complete): 179 subgroups in 15 classes",
      len(SUBS) == 179 and len(SUBCL) == 15 and JOIN_OK, f"by order {dict(sorted(by_order.items()))}; {time.time() - tS:.1f} s")
check("E", "maximal subgroups: one class of 8 of order 21 (7:3) and two classes of 7 of order 24 (S4) -- the ATLAS list",
      sorted((len(H), next(len(cl) for cl in SUBCL if H in cl)) for H in set(maximal)) .count((24, 7)) == 14
      and sum(1 for H in maximal if len(H) == 21) == 8 and len(maximal) == 22
      and sum(1 for cl in SUBCL if len(next(iter(cl))) == 24) == 2, f"{len(maximal)} maximal subgroups")
# S4 check: order-24 subgroups have element orders {1:1, 2:9, 3:8, 4:6}
s4_ok = all(sorted(porder(h) for h in H) == sorted([1] + [2] * 9 + [3] * 8 + [4] * 6) for H in SUBS if len(H) == 24)
check("E", "the order-24 subgroups have the element orders of S4 (1, 9 x 2, 8 x 3, 6 x 4)", s4_ok)
F21img = frozenset(isoF[mkey(X)] for X in F21)
NF21 = {g for g in PSLstd if frozenset(pmul(pmul(g, h), pinv(g)) for h in F21img) == F21img}
check("E", "F21 = <D, C> maps onto one of the 8 maximal subgroups of order 21; it is the stabiliser of a point of the 2-transitive action on P^1(F7) (so maximal: 2-transitive => primitive); N(F21) = F21",
      F21img in maximal and NF21 == set(F21img)
      and any(all(h[x] == x for h in F21img) for x in range(8))
      and len({(p[0], p[1]) for p in PSLstd}) == 56)
VALUES["PSL27_subgroups"] = {"total": len(SUBS), "conjugacy_classes": len(SUBCL), "by_order": {str(k): v for k, v in sorted(by_order.items())},
                             "maximal_classes": sorted([len(next(iter(cl))), len(cl)] for cl in SUBCL if next(iter(cl)) in maximal)}

# ---- complex conjugation kappa: PGL(2,7) inside G2
conj_closed = all(mkey(mconj(X)) in kFL for X in FL)
check("E", "the flipped copy is closed under complex conjugation; conj(D) = D^6", conj_closed and mconj(Dm) == mpow(Dm, 6))
# kappa acts on the Sylow-7 subgroups: S -> conj(S)
idxF = {S: i for i, S in enumerate(sylF)}
elFk = {mkey(X): X for X in FL}
kap = tuple(idxF[frozenset(mkey(mconj(elFk[k])) for k in S)] for S in sylF)
kap_std = pmul(pmul(phiF, kap), pinv(phiF))
grp336 = pclosure([mobius(1, 1, 0, 1), mobius(0, 6, 1, 0), kap_std], 8)
psl_gen = pclosure([mobius(1, 1, 0, 1), mobius(0, 6, 1, 0)], 8)
check("E", "transported to P^1(F7), kappa's action on the Sylow-7 subgroups is a Moebius map of non-square determinant (in PGL(2,7) \\ PSL(2,7)); <PSL(2,7), kappa> = PGL(2,7) of order 336",
      psl_gen == PSLstd and kap_std in PGLstd and kap_std not in PSLstd and grp336 == PGLstd)
# faithfulness of <G, kappa> acting on G by conjugation: no (M, 1) acts trivially; centre of G trivial
cls7 = [c for c in pclasses(list(isoF.values())) if isoF[mkey(Dm)] in c][0]
check("E", "conj(D) = D^6 is not conjugate to D in the flipped copy (7A <-> 7B), so kappa induces an outer automorphism; with trivial centre, <copy, kappa> (order 2 x 168 = 336) acts faithfully: Aut(PSL(2,7)) = PGL(2,7)",
      isoF[mkey(mpow(Dm, 6))] not in cls7 and sum(1 for p in isoF.values() if all(pmul(pmul(p, q), pinv(p)) == q for q in isoF.values())) == 1)
s4_classes = [cl for cl in SUBCL if len(next(iter(cl))) == 24]
swap = all(frozenset(pmul(pmul(kap_std, h), pinv(kap_std)) for h in H) in s4_classes[1] for H in s4_classes[0])
check("E", "kappa swaps the two classes of S4", swap)
# S4 classes -> Fano families: act on each class by conjugation; label via D (x -> x+1) and C (x -> 2x)
Dp, Cp, Rp = isoF[mkey(Dm)], isoF[mkey(Cm)], isoF[mkey(Rf)]
fam_of_class = []
for cl in s4_classes:
    cl = list(cl)
    conjH = lambda g, H: frozenset(pmul(pmul(g, h), pinv(g)) for h in H)
    H0 = next(H for H in cl if conjH(Cp, H) == H)
    lab = {}
    H = H0
    for k in range(7):
        lab[H] = k
        H = conjH(Dp, H)
    act7 = [tuple(lab[conjH(g, Hh)] for Hh in sorted(lab, key=lambda x: lab[x])) for g in (Dp, Cp, Rp)]
    G7 = pclosure(act7, 7)
    fam_of_class.append(("up" if G7 == frozenset(autA) else ("down" if G7 == frozenset(autB) else "?"),
                         act7[0][0] == 1 and act7[0][1] == 2, act7[1][1] == 2 and act7[1][0] == 0))
check("E", "PSL(2,7) acting by conjugation on each S4 class, labelled so that D is x -> x+1 and C is x -> 2x, is exactly the collineation group of one Fano family; the two classes give the two families",
      sorted(f[0] for f in fam_of_class) == ["down", "up"] and all(f[1] and f[2] for f in fam_of_class), str(fam_of_class))
VALUES["PGL27"] = {"order": len(grp336), "kappa_swaps_S4_classes": swap, "S4_class_families": [f[0] for f in fam_of_class]}

# ============================================================ F. A5 over Q(sqrt5)
print(f"--- section F start at {time.time() - T0:.1f} s", flush=True)
phi = Q5(Fr(1, 2), Fr(1, 2))
one, zero = Q5(1), Q5(0)
VERT = []
for s1 in (1, -1):
    for s2 in (1, -1):
        base = (zero, Q5(s1), phi * s2)
        for r in range(3):
            VERT.append(tuple(base[(i - r) % 3] for i in range(3)))
Vset = set(VERT)
v1 = (zero, one, phi)
nbrs = lambda v: [w for w in VERT if q5dot(tuple(a - b for a, b in zip(v, w)), tuple(a - b for a, b in zip(v, w))) == Q5(4)]
v2 = nbrs(v1)[0]
Bm = q5T((v1, v2, q5cross(v1, v2)))
Bmi = q5inv(Bm)
ROT = []
for w1 in VERT:
    for w2 in nbrs(w1):
        Wm = q5T((w1, w2, q5cross(w1, w2)))
        g = q5mul(Wm, Bmi)
        if q5mul(g, q5T(g)) == tuple(tuple(Q5(int(i == j)) for j in range(3)) for i in range(3)) and q5det(g) == one \
                and {q5apply(g, v) for v in VERT} == Vset:
            ROT.append(g)
rotset = set(ROT)
closed = all(q5mul(a, b) in rotset for a in ROT for b in ROT)
check("F", "icosahedron (0, ±1, ±phi): 12 vertices, each with 5 neighbours; brute force over images of an adjacent vertex pair gives exactly 60 rotations (12 x 5), closed under products",
      len(VERT) == 12 and all(len(nbrs(v)) == 5 for v in VERT) and len(ROT) == 60 and len(rotset) == 60 and closed)
tr = lambda g: g[0][0] + g[1][1] + g[2][2]
left = set(ROT)
a5cls = []
while left:
    g = next(iter(left))
    cl = {q5mul(q5mul(h, g), q5T(h)) for h in ROT}
    o, x = 1, g
    while x != tuple(tuple(Q5(int(i == j)) for j in range(3)) for i in range(3)):
        x = q5mul(x, g)
        o += 1
    a5cls.append((len(cl), o, tr(g), g))
    left -= cl
sig = sorted((s, o, repr(t)) for s, o, t, _ in a5cls)
want = sorted([(1, 1, repr(Q5(3))), (15, 2, repr(Q5(-1))), (20, 3, repr(Q5(0))), (12, 5, repr(Q5(Fr(1, 2), Fr(1, 2)))), (12, 5, repr(Q5(Fr(1, 2), Fr(-1, 2))))])
check("F", "A5 classes (size, order, chi3) = (1,1,3) (15,2,-1) (20,3,0) (12,5,(1+sqrt5)/2) (12,5,(1-sqrt5)/2); class equation 1+15+20+12+12 admits no normal subgroup (simple)",
      sig == want and all(not (60 % (1 + sum(c)) == 0 and 1 + sum(c) not in (1, 60))
                          for r in range(0, 5) for c in itertools.combinations([15, 20, 12, 12], r)), str(sig))
cc = sum((tr(g) * tr(g) for g in ROT), Q5(0)) / 60
nu = sum((tr(q5mul(g, g)) for g in ROT), Q5(0)) / 60
gal = lambda g: tuple(tuple(x.gal() for x in row) for row in g)
ROT2 = [gal(g) for g in ROT]
hom2 = all(gal(q5mul(a, b)) == q5mul(gal(a), gal(b)) for a in ROT[:15] for b in ROT[::4])
cc12 = sum((tr(g) * tr(h) for g, h in zip(ROT, ROT2)), Q5(0)) / 60
nu2 = sum((tr(q5mul(g, g)) for g in ROT2), Q5(0)) / 60
realcls = all(any(q5mul(q5mul(h, g), q5T(h)) == q5T(g) for h in ROT) for g in ROT)
check("F", "triplet 3: real orthogonal matrices, <chi,chi> = 1, FS indicator +1; Galois-conjugate triplet 3' (sqrt5 -> -sqrt5) is a representation, <chi,chi'> = 0, FS +1; every element is conjugate to its inverse (all A5 characters real)",
      cc == one and nu == one and hom2 and cc12 == zero and nu2 == one and realcls)
rest = [(a, b) for a in range(1, 8) for b in range(a, 8) if a * a + b * b == 60 - 1 - 9 - 9]
check("F", "remaining two irreducible degrees solve d4^2 + d5^2 = 60 - 1 - 9 - 9 = 41 only as (4, 5): exactly two triplets, both real", rest == [(4, 5)], str(rest))
VALUES["A5_triplet_character"] = {"classes": "1A,2A,3A,5A,5B", "sizes": [1, 15, 20, 12, 12],
                                  "chi": ["3", "-1", "0", "(1+sqrt5)/2", "(1-sqrt5)/2"], "frobenius_schur": 1}


# ============================================================ G. Weyl groups (integer 2x2 matrices in Lambda coords)
print(f"--- section G start at {time.time() - T0:.1f} s", flush=True)
def mat2_from3(g3):
    """3x3 rational matrix on R^3 preserving the plane -> 2x2 in Lambda coords (columns g b1, g b2)"""
    cols = []
    for b in ((1, -1, 0), (0, 1, -1)):
        v = tuple(sum(Fr(g3[i][j]) * b[j] for j in range(3)) for i in range(3))
        cols.append(from3(v))
    return ((cols[0][0], cols[1][0]), (cols[0][1], cols[1][1]))


def m2mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def m2app(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])


def m2det(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


I2 = ((Fr(1), Fr(0)), (Fr(0), Fr(1)))


def refl3(r):
    rr = sum(Fr(x) * Fr(x) for x in r)
    return [[Fr(int(i == j)) - 2 * Fr(r[i]) * Fr(r[j]) / rr for j in range(3)] for i in range(3)]


def gen_group2(gens):
    seen = {I2}
    fr = [I2]
    while fr:
        new = []
        for A in fr:
            for g in gens:
                B = m2mul(g, A)
                if B not in seen:
                    seen.add(B)
                    new.append(B)
        fr = new
    return seen


long_roots = [(1, -1, 0), (0, 1, -1), (1, 0, -1)]
short_roots = [tuple(Fr(int(i == k)) - Fr(1, 3) for i in range(3)) for k in range(3)]
W_A2 = gen_group2([mat2_from3(refl3(r)) for r in long_roots])
W_G2 = gen_group2([mat2_from3(refl3(r)) for r in long_roots + short_roots])
autL = {((a, b), (c, d)) for a, b, c, d in itertools.product(range(-2, 3), repeat=4)
        if m2mul(m2mul(((a, c), (b, d)), GR), ((a, b), (c, d))) == tuple(tuple(x for x in row) for row in GR)}
autL = {tuple(tuple(Fr(x) for x in row) for row in A) for A in autL}
check("G", "W(SU(3)) (long-root reflections) has order 6, W(G2) (adding short-root reflections) order 12; both are integer matrices (keep Lambda); W(G2) = Aut(Lambda) (all 12 integer isometries of the Gram form)",
      len(W_A2) == 6 and len(W_G2) == 12 and all(x.denominator == 1 for A in W_G2 for row in A for x in row) and W_G2 == autL)
minus1 = ((Fr(-1), Fr(0)), (Fr(0), Fr(-1)))
check("G", "W(G2) = W(SU(3)) x {±1} on the plane", W_G2 == W_A2 | {m2mul(minus1, A) for A in W_A2} and minus1 not in W_A2)
U, Wv = (1, 0), (1, 2)          # u = b1 = (1,-1,0), w = b1 + 2 b2 = (1,1,-2)
ANG = {(Fr(1), 0): 0, (Fr(1, 2), 3): 60, (Fr(-1, 2), 3): 120, (Fr(-1), 0): 180, (Fr(-1, 2), -3): 240, (Fr(1, 2), -3): 300}


def turn_rows(Wg):
    rows = []
    for g in Wg:
        if m2det(g) < 0:
            continue
        gu = m2app(g, U)
        ang = ANG[(dot(gu, U) / 2, dot(gu, Wv))]
        k = label(m2app(g, P))
        if k is None:
            fate = "moves the seven points"
        elif img(up, tuple((k * x) % 7 for x in range(7))) == frozenset(up) and img(down, tuple((k * x) % 7 for x in range(7))) == frozenset(down):
            fate = f"x -> {k}x, keeps both families"
        elif img(up, tuple((k * x) % 7 for x in range(7))) == frozenset(down):
            fate = f"x -> {k}x, swaps the families"
        else:
            fate = f"x -> {k}x, other"
        rows.append((ang, fate))
    return sorted(rows)


rowsA2, rowsG2 = turn_rows(W_A2), turn_rows(W_G2)
mirA2 = [g for g in W_A2 if m2det(g) < 0]
mirG2 = [g for g in W_G2 if m2det(g) < 0]
keepA2 = sum(label(m2app(g, P)) is not None for g in mirA2)
keepG2 = sum(label(m2app(g, P)) is not None for g in mirG2)
check("G", "SU(3) turns: 0/120/240 deg = x -> 1x, 4x, 2x, all keep both families; 3 mirrors, 0 keep the seven points",
      rowsA2 == [(0, "x -> 1x, keeps both families"), (120, "x -> 4x, keeps both families"), (240, "x -> 2x, keeps both families")]
      and len(mirA2) == 3 and keepA2 == 0, str(rowsA2))
check("G", "G2 adds 60/180/300 deg = x -> 5x, 6x, 3x, which swap the families; 6 mirrors, 0 keep the seven points",
      rowsG2 == [(0, "x -> 1x, keeps both families"), (60, "x -> 5x, swaps the families"), (120, "x -> 4x, keeps both families"),
                 (180, "x -> 6x, swaps the families"), (240, "x -> 2x, keeps both families"), (300, "x -> 3x, swaps the families")]
      and len(mirG2) == 6 and keepG2 == 0, str(rowsG2))
Q2 = from3((Fr(1, 7), Fr(4, 7), Fr(-5, 7)))       # point of diag(z, z^4, z^2)
pts2 = {((j * Q2[0]) % 1, (j * Q2[1]) % 1) for j in range(7)}
check("G", "(extra) each SU(3) mirror maps the seven points of D onto those of diag(z, z^4, z^2)",
      all({((m2app(g, (j * P[0], j * P[1]))[0]) % 1, (m2app(g, (j * P[0], j * P[1]))[1]) % 1) for j in range(7)} == pts2 for g in mirA2))
VALUES["weyl"] = {"SU(3)": {"order": len(W_A2), "mirrors": len(mirA2), "mirrors_keeping_points": keepA2, "turns": [f"{a} deg: {f}" for a, f in rowsA2]},
                  "G2": {"order": len(W_G2), "mirrors": len(mirG2), "mirrors_keeping_points": keepG2, "turns": [f"{a} deg: {f}" for a, f in rowsG2]}}

# ---- affine Weyl groups: elements (w, t) acting as x -> w x + t
al1 = (Fr(-1, 3), Fr(2, 3), Fr(-1, 3))       # short simple root e2 - (1,1,1)/3
al2 = (1, -1, 0)                              # long simple root e1 - e2
d3 = lambda x, y: sum(Fr(a) * Fr(b) for a, b in zip(x, y))
pos = {"a1": al1, "a2": al2}
pos["a1+a2"] = tuple(Fr(a) + Fr(b) for a, b in zip(al1, al2))
pos["2a1+a2"] = tuple(2 * Fr(a) + Fr(b) for a, b in zip(al1, al2))
pos["3a1+a2"] = tuple(3 * Fr(a) + Fr(b) for a, b in zip(al1, al2))
pos["3a1+2a2"] = tuple(3 * Fr(a) + 2 * Fr(b) for a, b in zip(al1, al2))
roots_G2 = {tuple(Fr(x) for x in r) for r in long_roots + short_roots}
roots_G2 |= {tuple(-x for x in r) for r in roots_G2}
theta = pos["3a1+2a2"]
check("G", "my G2 base: a1 = e2 - (1,1,1)/3 (short), a2 = e1 - e2 (long), at 150 deg; the 6 positive roots are roots; highest root theta = 3a1+2a2 = (1,0,-1) (long)",
      d3(al1, al1) == Fr(2, 3) and d3(al2, al2) == 2 and d3(al1, al2) < 0 and all(r in roots_G2 for r in pos.values())
      and theta == (1, 0, -1) and d3(al1, al2) ** 2 == Fr(3, 4) * d3(al1, al1) * d3(al2, al2))


def aff_refl(alpha, k):
    """s_{alpha,k}(x) = x - ((alpha,x) - k) alpha^vee, as (w, t) in Lambda coords"""
    av = tuple(2 * Fr(a) / d3(alpha, alpha) for a in alpha)
    w = mat2_from3(refl3(alpha))
    t = from3(tuple(k * x for x in av))
    return (w, t)


def amul(A, B):                                    # (A o B)(x) = A(B(x))
    wa, ta = A
    wb, tb = B
    tw = m2app(wa, tb)
    return (m2mul(wa, wb), (tw[0] + ta[0], tw[1] + ta[1]))


AID = (I2, (Fr(0), Fr(0)))


def aorder(A, cap=50):
    X, n = A, 1
    while X != AID:
        X = amul(A, X)
        n += 1
        if n > cap:
            return None
    return n


s1, s2, s0 = aff_refl(al1, 0), aff_refl(al2, 0), aff_refl(theta, 1)
cox = (aorder(amul(s1, s2)), aorder(amul(s2, s0)), aorder(amul(s1, s0)))
check("G", "affine G2: (s1 s2)^6 = (s2 s0)^3 = (s1 s0)^2 = 1 with s0 = s_{theta,1}: Coxeter triangle (2,3,6)", cox == (6, 3, 2), str(cox))
# W_aff = Lambda x| W(G2): s0 o s_theta = translation by theta^vee = theta in Lambda; W-orbit of theta = long roots, which generate Lambda
trans_theta = amul(s0, aff_refl(theta, 0))
long_orbit = {m2app(g, from3(theta)) for g in W_G2}
gens_lin = gen_group2([s1[0], s2[0]])
check("G", "W_aff(G2) = Lambda x| W(G2): s1, s2 generate W(G2); s0 s_theta = translation by theta = (1,0,-1); the W-orbit of theta is the 6 long roots, which span Lambda; every generator has translation part in Lambda",
      gens_lin == W_G2 and trans_theta == (I2, from3(theta)) and len(long_orbit) == 6
      and (Fr(1), Fr(0)) in long_orbit and (Fr(0), Fr(1)) in long_orbit and all(is_int2(g[1]) for g in (s0, s1, s2)))


def centres(Wg):
    """rotation centres per Lambda cell: fixed points of (w, t), t in Lambda, solving (1 - w) x = t; site group = {w : x - w x in Lambda}"""
    pts_ = set()
    for g in Wg:
        if m2det(g) < 0 or g == I2:
            continue
        a, b = 1 - g[0][0], -g[0][1]
        c, d = -g[1][0], 1 - g[1][1]
        det = a * d - b * c
        inv = ((d / det, -b / det), (-c / det, a / det))
        for t in itertools.product(range(-6, 7), repeat=2):
            x = m2app(inv, t)
            pts_.add((x[0] % 1, x[1] % 1))
    out = {}
    for x in pts_:
        site = [g for g in Wg if is_int2(tuple(xi - yi for xi, yi in zip(x, m2app(g, x))))]
        rot = max(len([g for g in site if m2det(g) > 0]), 1)
        mir = len([g for g in site if m2det(g) < 0])
        out[x] = (rot, mir, len(site))
    return out


cG2 = centres(W_G2)
cA2 = centres(W_A2)
patG2 = {}
for v in cG2.values():
    patG2[v] = patG2.get(v, 0) + 1
patA2 = {}
for v in cA2.values():
    patA2[v] = patA2.get(v, 0) + 1
check("G", "G2: rotation centres per cell from (1-w)x = t: one 6-fold on 6 mirrors (6mm), two 3-fold on 3 mirrors (3m), three 2-fold on 2 mirrors (2mm) -- the p6m Wyckoff pattern 1a, 2b, 3c; point group of order 12 with a 60 deg turn, translations Lambda: p6m",
      patG2 == {(6, 6, 12): 1, (3, 3, 6): 2, (2, 2, 4): 3} and len(W_G2) == 12, str(patG2))
check("G", "SU(3) contrast: three 3-fold centres per cell, each on 3 mirrors (3m): p3m1",
      patA2 == {(3, 3, 6): 3}, str(patA2))
keep7 = [g for g in W_G2 if label(m2app(g, P)) is not None]
keep7a = [g for g in W_A2 if label(m2app(g, P)) is not None]
check("G", "(extra) affine elements keeping the seven points: Lambda x| C6 for G2 (p6), Lambda x| C3 for SU(3) (p3), no mirrors",
      len(keep7) == 6 and all(m2det(g) > 0 for g in keep7) and len(keep7a) == 3 and all(m2det(g) > 0 for g in keep7a))
on_mirror = any((d3(r, to3((j * P[0], j * P[1])))).denominator == 1 for r in roots_G2 for j in range(1, 7))
check("G", "(extra) no point j p (j = 1..6) lies on an affine mirror (alpha, x) = k (k integer) of G2 (whose roots include SU(3)'s)", not on_mirror)
VALUES["affine_weyl"] = {"G2": {"coxeter": list(cox), "point_group_order": len(W_G2), "site_pattern": {str(k): v for k, v in patG2.items()}, "wallpaper": "p6m"},
                         "SU3": {"point_group_order": len(W_A2), "site_pattern": {str(k): v for k, v in patA2.items()}, "wallpaper": "p3m1"}}

# ============================================================ H. octonions
print(f"--- section H start at {time.time() - T0:.1f} s", flush=True)
# Cayley-Dickson: O = H + H, (a,b)(c,d) = (ac - conj(d) b, d a + b conj(c)); quaternions as 4-tuples
def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def qconj(p):
    return (p[0], -p[1], -p[2], -p[3])


def omul(x, y):
    a, b = x[:4], x[4:]
    c, d = y[:4], y[4:]
    first = tuple(u - v for u, v in zip(qmul(a, c), qmul(qconj(d), b)))
    second = tuple(u + v for u, v in zip(qmul(d, a), qmul(b, qconj(c))))
    return first + second


EB = [tuple(int(i == k) for i in range(8)) for k in range(8)]
STRUCT = [[omul(EB[i], EB[j]) for j in range(8)] for i in range(8)]
assoc = lambda x, y, z: tuple(u - v for u, v in zip(omul(omul(x, y), z), omul(x, omul(y, z))))
alt_ok = True
for i, j, k in itertools.product(range(8), repeat=3):
    A_ = assoc(EB[i], EB[j], EB[k])
    if any(A_) and not (A_ == tuple(-x for x in assoc(EB[j], EB[i], EB[k])) and A_ == tuple(-x for x in assoc(EB[i], EB[k], EB[j]))):
        alt_ok = False
    if (i == j or j == k or i == k) and any(A_):
        alt_ok = False
non_assoc = any(any(assoc(EB[i], EB[j], EB[k])) for i, j, k in itertools.product(range(8), repeat=3))
check("H", "Cayley-Dickson octonions: associator totally antisymmetric on all 512 basis triples (alternative), not associative",
      alt_ok and non_assoc)
# derivations: unknown D (8x8), D(e_i e_j) = D(e_i) e_j + e_i D(e_j)
rows = []
for i in range(8):
    for j in range(8):
        cij = STRUCT[i][j]
        for m in range(8):
            row = [0] * 64                       # unknown D[l][k] at index 8*l + k  (D e_k = sum_l D[l][k] e_l)
            for k in range(8):
                if cij[k]:
                    row[8 * m + k] += cij[k]
            for l in range(8):
                c = STRUCT[l][j][m]
                if c:
                    row[8 * l + i] -= c
                c = STRUCT[i][l][m]
                if c:
                    row[8 * l + j] -= c
            if any(row):
                rows.append(row)
der_basis = nullspace(rows, 64)
rows_e = rows + [[1 if idx == 8 * l + 1 else 0 for idx in range(64)] for l in range(8)]
stab_basis = nullspace(rows_e, 64)


def lie_type_data(basis):
    """dimension, Killing form negative definite?, centraliser dim of a test element, skew-symmetry -- all in Fractions.
    The nullspace basis is reduced: basis vector a is 1 at its own free column and 0 at the others, so the coordinates
    of any element of the span are its entries at the free columns."""
    n = len(basis)
    free = [next(i for i in range(64) if basis[a][i] == 1 and all(basis[b][i] == 0 for b in range(n) if b != a)) for a in range(n)]
    mats = [[[b[8 * l + k] for k in range(8)] for l in range(8)] for b in basis]

    def mm(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(8)) for j in range(8)] for i in range(8)]

    def coords(A):
        fa = [A[i][j] for i in range(8) for j in range(8)]
        c = [fa[f] for f in free]
        rec = [sum(c[a] * basis[a][q] for a in range(n)) for q in range(64)]
        assert rec == fa, "bracket left the span"
        return c

    ad = []
    for a in range(n):
        cols = []
        for b in range(n):
            X, Y = mm(mats[a], mats[b]), mm(mats[b], mats[a])
            cols.append(coords([[X[i][j] - Y[i][j] for j in range(8)] for i in range(8)]))
        ad.append([[cols[b][r] for b in range(n)] for r in range(n)])       # ad[a][r][b]
    def tr_prod(A, B):
        return sum(A[i][k] * B[k][i] for i in range(n) for k in range(n))
    kill = [[tr_prod(ad[a], ad[b]) for b in range(n)] for a in range(n)]
    # Sylvester: -kill positive definite <=> all leading principal minors of -kill positive (fraction-exact Gaussian elimination)
    A = [[-Fr(x) for x in row] for row in kill]
    neg_def = True
    for k in range(n):
        if A[k][k] <= 0:
            neg_def = False
            break
        for r in range(k + 1, n):
            f = A[r][k] / A[k][k]
            A[r] = [x - f * y for x, y in zip(A[r], A[k])]
    coeff = [(a % 5) - 2 + (a // 5) or 1 for a in range(n)]
    adX = [[sum(coeff[a] * ad[a][r][c] for a in range(n)) for c in range(n)] for r in range(n)]
    cent = nullspace_dim(adX, n)
    skew = all(mats[a][i][j] == -mats[a][j][i] for a in range(n) for i in range(8) for j in range(8))
    return n, neg_def, cent, skew


nD, ndD, centD, skD = lie_type_data(der_basis)
nS, ndS, centS, skS = lie_type_data(stab_basis)
check("H", "Der(O) has dimension 14, negative-definite Killing form (compact semisimple), a test element with 2-dim centraliser (rank <= 2): only g2 fits (su(3)+su(2)+su(2) also has dim 14 but rank 4)",
      nD == 14 and ndD and centD == 2 and skD, f"dim {nD}, centraliser {centD}")
check("H", "derivations killing the imaginary unit e1: dimension 8, compact semisimple, rank <= 2: su(3)",
      nS == 8 and ndS and centS == 2 and skS, f"dim {nS}, centraliser {centS}")


# the report's model O = C + C^3, (a,u)(b,v) = (ab - sum u_i conj v_i, a v + conj(b) u + conj(u x v)), over Q(i) exactly
class Gi:
    __slots__ = ("r", "i")

    def __init__(self, r, i=0):
        self.r, self.i = Fr(r), Fr(i)

    def __add__(s, o):
        return Gi(s.r + o.r, s.i + o.i)

    def __sub__(s, o):
        return Gi(s.r - o.r, s.i - o.i)

    def __mul__(s, o):
        return Gi(s.r * o.r - s.i * o.i, s.r * o.i + s.i * o.r)

    def c(s):
        return Gi(s.r, -s.i)

    def __eq__(s, o):
        return s.r == o.r and s.i == o.i

    def n(s):
        return s.r * s.r + s.i * s.i


def cmul(x, y):
    a, u = x[0], x[1:]
    b, v = y[0], y[1:]
    cr = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    s = Gi(0)
    for k in range(3):
        s = s + u[k] * v[k].c()
    first = a * b - s
    rest = tuple(a * v[k] + b.c() * u[k] + cr[k].c() for k in range(3))
    return (first,) + rest


RB = []
for k in range(4):
    RB.append(tuple(Gi(1) if q == k else Gi(0) for q in range(4)))
    RB.append(tuple(Gi(0, 1) if q == k else Gi(0) for q in range(4)))
cassoc = lambda x, y, z: tuple(p - q for p, q in zip(cmul(cmul(x, y), z), cmul(x, cmul(y, z))))
neg = lambda t: tuple(Gi(0) - p for p in t)
c_alt = all(cassoc(RB[i], RB[j], RB[k]) == neg(cassoc(RB[j], RB[i], RB[k])) == neg(cassoc(RB[i], RB[k], RB[j]))
            for i, j, k in itertools.product(range(8), repeat=3))
Nq = lambda x: sum((p.n() for p in x), Fr(0))
polar = RB + [tuple(p + q for p, q in zip(RB[i], RB[j])) for i in range(8) for j in range(i + 1, 8)]
c_comp = all(Nq(cmul(x, y)) == Nq(x) * Nq(y) for x in polar for y in polar)
c_unit = all(cmul(RB[0], x) == x and cmul(x, RB[0]) == x for x in RB)
kappa_aut = all(tuple(p.c() for p in cmul(x, y)) == cmul(tuple(p.c() for p in x), tuple(p.c() for p in y)) for x in RB for y in RB)
check("H", "the report's C + C^3 product over Q(i): (1,0) is the unit, associator alternating on 512 real-basis triples, N(xy) = N(x)N(y) on 36 x 36 polarisation points (complete for a biquadratic identity): an 8-dim composition algebra = octonions (Hurwitz); kappa (conjugate every coordinate) is an automorphism and sends e = (i,0) to -e",
      c_unit and c_alt and c_comp and kappa_aut and len(polar) == 36)
# SU(3) acting on the C^3 part is an automorphism iff U^T conj(U) = 1 and conj(U) = cofactor(U) (then conj(Uu x Uv) = U conj(u x v))
cof = lambda A: mtrans(madj(A))
check("H", "for D, C, Rf, Dk, R and LNR's B: U^T conj(U) = 1 and cofactor(U) = conj(U) exactly, so (a,u) -> (a,Uu) preserves the product (u.conj(v) and conj(u x v) both transform correctly) and fixes e = (i,0)",
      all(mmul(mtrans(X), mconj(X)) == IDENT and cof(X) == mconj(X) for X in (Dm, Cm, Rf, Dk, Rm, B_lnr)))
VALUES["octonions"] = {"der_dim": nD, "stabiliser_dim": nS, "PGL27_in_G2_order": len(grp336)}

# ============================================================ I. order-7 torus points with a hexagonal finer lattice
print(f"--- section I start at {time.time() - T0:.1f} s", flush=True)
def reduce_basis(b1_, b2_):
    while True:
        if dot(b2_, b2_) < dot(b1_, b1_):
            b1_, b2_ = b2_, b1_
        mu = dot(b1_, b2_) / dot(b1_, b1_)
        r = round(mu)
        if r == 0:
            return b1_, b2_
        b2_ = (b2_[0] - r * b1_[0], b2_[1] - r * b1_[1])


hexpts = []
for a in range(7):
    for b in range(7):
        if (a, b) == (0, 0):
            continue
        q = (Fr(a, 7), Fr(b, 7))
        # basis of Z^2 + Z q: q and an integer vector completing it (lattice index 7)
        cand_basis = None
        for e in ((Fr(1), Fr(0)), (Fr(0), Fr(1))):
            if q[0] * e[1] - q[1] * e[0] != 0 and abs(q[0] * e[1] - q[1] * e[0]) == Fr(1, 7):
                cand_basis = (q, e)
                break
        if cand_basis is None:     # use q' = k q with a or b = 1
            for k in range(1, 7):
                qq = ((k * a % 7) / Fr(7), (k * b % 7) / Fr(7))
                for e in ((Fr(1), Fr(0)), (Fr(0), Fr(1))):
                    if abs(qq[0] * e[1] - qq[1] * e[0]) == Fr(1, 7):
                        cand_basis = (qq, e)
                        break
                if cand_basis:
                    break
        r1, r2 = reduce_basis(*cand_basis)
        if dot(r1, r1) == dot(r2, r2) and abs(dot(r1, r2)) * 2 == dot(r1, r1):
            hexpts.append((a, b))
subgroups = {frozenset(((j * a) % 7, (j * b) % 7) for j in range(1, 7)) for a, b in hexpts}
pD = (int(P[0] * 7) % 7, int(P[1] * 7) % 7)
pQ = (int(Q2[0] * 7) % 7, int(Q2[1] * 7) % 7)
check("I", "(extra) of the 48 order-7 torus points, exactly 12 (two order-7 subgroups: those of D and of diag(z,z^4,z^2)) give a hexagonal finer lattice",
      len(hexpts) == 12 and len(subgroups) == 2 and any(pD in s for s in subgroups) and any(pQ in s for s in subgroups), f"{len(hexpts)} points, {len(subgroups)} subgroups")
VALUES["order7_points_with_hexagonal_finer_lattice"] = {"value": len(hexpts), "of": 48, "subgroups": len(subgroups)}

# ============================================================ K. completing the uniqueness argument of the report's Finding 8
print(f"--- section K start at {time.time() - T0:.1f} s", flush=True)
# (i) Aut(F21) by brute force on the permutation image: pairs (d, c) obeying the presentation and generating F21
rel = lambda d, c: pmul(pmul(pinv(c), d), c) == pmul(d, pmul(d, pmul(d, d)))       # c^-1 d c = d^4
assert rel(Dp, Cp) or rel(Dp, pinv(Cp))
use_c = Cp if rel(Dp, Cp) else pinv(Cp)
autF21 = [(d, c) for d in F21img for c in F21img if porder(d) == 7 and porder(c) == 3 and rel(d, c)
          and pclosure([d, c], 8) == F21img]
NPGL = [g for g in PGLstd if frozenset(pmul(pmul(g, h), pinv(g)) for h in F21img) == F21img]
CPGL = [g for g in PGLstd if all(pmul(g, h) == pmul(h, g) for h in F21img)]
check("K", "|Aut(F21)| = 42 (brute force over generator images); N_PGL(2,7)(F21) has order 42 and centralises nothing but 1, so it induces every automorphism of F21 by an automorphism of PSL(2,7)",
      len(autF21) == 42 and len(NPGL) == 42 and len(CPGL) == 1, f"{len(autF21)}, {len(NPGL)}, {len(CPGL)}")
# (ii) irreducible degrees of PSL(2,7): 6 classes, no non-trivial 1-dim irrep (simple, non-abelian), 1 + 9 + 9 + a^2 + b^2 + c^2 = 168, each degree divides 168
divs = [d for d in range(2, 13) if 168 % d == 0]
sols = [(a, b, c) for a in divs for b in divs for c in divs if a <= b <= c and a * a + b * b + c * c == 168 - 19]
check("K", "the degree equation forces the irreducible degrees (1, 3, 3, 6, 7, 8): the only triplets of PSL(2,7) are 3 and 3bar (LNR's table is then not needed for Finding 8)",
      sols == [(6, 7, 8)] and len(pclasses(list(isoF.values()))) == 6, str(sols))
# (iii) F21 acts irreducibly on C^3 (<chi,chi>_F21 = 1, section E) and chi3(D) = b7 != b7bar.  With (i)-(iii) and the single
# class of order-21 subgroups: any PSL(2,7) in U(3) containing <D,C> is the image of a 3-dim irrep agreeing with the flipped
# copy on F21 (after an automorphism), hence equal to it by Schur's lemma.
cl21 = [cl for cl in SUBCL if len(next(iter(cl))) == 21]
check("K", "ingredients of the uniqueness of the PSL(2,7) in U(3) containing <D,C>: one class of 8 order-21 subgroups, (i), (ii), F21 irreducible, chi(D) = b7 != b7bar",
      len(cl21) == 1 and len(cl21[0]) == 8 and fs_and_inner(F21)[0] == K1 and mtrace(Dm) != kconj(mtrace(Dm)))
VALUES["uniqueness_ingredients"] = {"aut_F21": len(autF21), "N_PGL_F21": len(NPGL), "irrep_degrees": [1, 3, 3] + list(sols[0]) if sols else None}

# ============================================================ J. the 25 lines of hexagon_check.py, rebuilt from the values above
print(f"--- section J start at {time.time() - T0:.1f} s", flush=True)
inF21_in_KL = kF21 <= kKL
maximal21 = F21img in maximal
lines = [
    f"120° turn sends point 1 to point {label(rollp)}",
    f"neighbours of point 0: {ring} -> every point touches every other (K7)",
    f"triangles: {len(TRI)} | family A Fano: {is_fano(up)} | family B Fano: {is_fano(down)}",
    f"one family is the octonion lines {{i, i+1, i+3}}: {len(oct_fam) == 1}",
    f"x -> ax+b (a in 1,2,4) preserves both families: {all(img(S, affine[(a, b)]) == frozenset(S) for S in (up, down) for a in (1, 2, 4) for b in range(7))}",
    f"|<D, 120° turn>| = {o21} | inside SU(3): {all(in_SU3(X) for X in F21)}",
    f"|<Klein's matrices>| = {oK} | inside SU(3): {all(in_SU3(X) for X in KL)}",
    f"Klein quartic preserved by the generators: {all(quartic_after(X, 'klein') == QK for X in (Dk, Cm, Rm))}",
    f"<D, 120° turn> inside Klein's own copy: {inF21_in_KL}",
    f"flip in SU(3): {in_SU3(flip)} | flip sends Dk to D: {mmul(mmul(flip, Dk), minv(flip)) == Dm}",
    f"flipped copy: order {oF} | inside SU(3): {all(in_SU3(X) for X in FL)} | holds <D, 120° turn>: {kF21 <= kFL}",
    f"flipped copy preserves the mirror quartic xy³ + yz³ + zx³: {all(quartic_after(X, 'mirror') == QM for X in (Dm, Cm, Rf))}",
    f"order-21 group maximal in it: {maximal21}",
    f"Fano planes on Z7 kept by x -> x+1: {len(cyc)} | the torus families are exactly these: {set(cyc) == {frozenset(up), frozenset(down)}}",
]
for nm, Wg, rows_, mir, keep in (("SU(3)", W_A2, rowsA2, mirA2, keepA2), ("G2", W_G2, rowsG2, mirG2, keepG2)):
    keepsL = all(x.denominator == 1 for A in Wg for row in A for x in row)
    lines.append(f"Weyl({nm}): order {len(Wg)} | keeps Λ: {keepsL} | mirrors that keep the seven points: {keep} of {len(mir)}")
    for ang, fate in rows_:
        lines.append(f"   turn {ang:>3}°: {fate}")
with open(os.path.join(HERE, "xc2_replica_lines.txt"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
hc = os.path.normpath(os.path.join(HERE, "..", "..", "..", "hexagon_check.py"))
t_h = time.time()
orig = subprocess.run([sys.executable, hc], capture_output=True, text=True, timeout=300).stdout.rstrip("\n").split("\n")
t_h = time.time() - t_h
same = sum(a == b for a, b in zip(orig, lines))
check("J", "hexagon_check.py (run now, float) and the lines rebuilt from this cross-check's exact values are identical",
      len(orig) == len(lines) == 25 and same == 25, f"{same} of {len(lines)} identical; hexagon_check.py {t_h:.1f} s")
VALUES["replica"] = {"lines_original": len(orig), "lines_xc2": len(lines), "identical": same}

# ============================================================ summary
npass = sum(c["ok"] for c in CHECKS)
rt = round(time.time() - T0, 1)
print(f"\n{npass} of {len(CHECKS)} checks pass; {rt} s")
with open(os.path.join(HERE, "xc2_checks.json"), "w") as fh:
    json.dump({"script": "xc2_e0.py", "n_checks": len(CHECKS), "n_pass": npass, "all_pass": npass == len(CHECKS),
               "runtime_seconds": rt, "values": VALUES, "checks": CHECKS}, fh, indent=1, ensure_ascii=False)
sys.exit(0 if npass == len(CHECKS) else 1)
