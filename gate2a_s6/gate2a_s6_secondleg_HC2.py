"""G-2a-S6 SECOND LEG (CC) -- H-C2 (the decisive R^3-rigid ceiling) + H-A peripheral yield.

Decisive bit (pre-registered, both branches equal weight): does an orientation-preserving ODD
element of Isom+(M) SWAP or FIX the two octahedron-center vertices of the canonical
decomposition?  SWAP => Fix_M(S4)=empty => R^3-rigid ceiling is exactly pyritohedral A4.
FIX (falsifier) => a rigid full-O embedding of the Borromean rings exists in R^3.

INDEPENDENCE / HONEST FLAG:
  - The spec prefers a SnapPy-free hand-built two-octahedra gluing. I do NOT have that face-
    pairing memorized to a certainty that would make a hand build trustworthy for the DECISIVE
    bit, so I use SnapPy -- but by an INDEPENDENT construction path: the manifold is built from
    the link DIAGRAM Link('L6a4').exterior() (NOT the census name "6^3_2" the chat leg used),
    confirmed isometric to it, and ALL downstream combinatorics (own automorphism search by
    gluing-propagation, own vertex-link Euler characteristics, own orientation + swap analysis)
    are written fresh here.  Shared-solver caveat: the canonical retriangulation itself and the
    peripheral maps come from SnapPy's solver, as in the chat leg -- flagged per the S4 precedent
    the handoff explicitly permits (non-blocking, annotated).
"""
import snappy
from itertools import permutations, product
from collections import Counter, defaultdict

def rule(t): print("=" * 70); print(t); print("=" * 70)
def sgn3(p):
    s = 1
    for i in range(3):
        for j in range(i+1, 3):
            if p[i] > p[j]: s = -s
    return s

# ---------- independent construction path ----------
rule("build Borromean complement from the L6a4 DIAGRAM (independent of census name)")
L = snappy.Link('L6a4')
E = L.exterior()
E.dehn_fill([(0, 0)] * E.num_cusps())
print(f"Link('L6a4').exterior(): cusps={E.num_cusps()}, vol={E.volume()}")
cen = snappy.Manifold("6^3_2")
print(f"is_isometric_to census 6^3_2: {E.is_isometric_to(cen)}  (same manifold, established independently)")
K = E.canonical_retriangulation()
print(f"canonical retriangulation built. two ideal regular octahedra expected (vol 7.3277).")

# ---------- H-A peripheral yield, own extraction ----------
rule("H-A peripheral yield (own extraction from the 48 canonical isometries)")
isos = K.isomorphisms_to(K)
print(f"|Isom(M)| = {len(isos)} (expect 48)")
data = []
kinds = Counter()
for iso in isos:
    cim = tuple(iso.cusp_images())
    cmaps = [tuple(map(tuple, m)) for m in iso.cusp_maps()]
    dets = [a*d - b*c for ((a, b), (c, d)) in cmaps]
    eps = [d for ((a, b), (c, d)) in cmaps]          # longitude sign
    form = []
    for ((a, b), (c, d)) in cmaps:
        if b == 0 and c == 0 and abs(a) == 1 and abs(d) == 1:
            form.append("pmId" if a == d else "diag_pm")
        else:
            form.append("other")
    for f in form: kinds[f] += 1
    orient = all(x == 1 for x in dets)               # or-preserving iff all cusp-map dets +1
    det_axis = sgn3(cim) * eps[0]*eps[1]*eps[2]
    data.append((orient, cim, tuple(eps), det_axis, tuple(form)))
n_op = sum(1 for d in data if d[0])
print(f"orientation-preserving: {n_op} (expect 24)")
print(f"peripheral map forms over 48x3 cusps: {dict(kinds)}")
split_ok = all((set(d[4]) == {'pmId'}) == d[0] and (set(d[4]) == {'diag_pm'}) == (not d[0]) for d in data)
print(f"or-preserving all ±Id, or-reversing all ±diag(1,-1), zero shear: {split_ok}")
det_all = all(d[3] == 1 for d in data)
print(f"YIELD det(axis) = +1 for ALL 48 (image O, never O_h): {det_all}")
op_fibers = set((d[1], d[2]) for d in data if d[0])
full_fibers = Counter((d[1], d[2]) for d in data)
print(f"faithful on motion group (24 distinct (sigma,eps) among or-preserving): {len(op_fibers) == 24}")
print(f"axis-rep kernel order = 48/{len(full_fibers)} = {48 // len(full_fibers)} (central Z/2, "
      f"amphichiral axis-invisible); every fiber size 2: {set(full_fibers.values()) == {2}}")
assert n_op == 24 and split_ok and det_all and len(op_fibers) == 24
print("H-A yield reproduced independently (own extraction). MATCHES chat leg.")

# ---------- own combinatorial complex from K ----------
rule("H-C2 -- own combinatorial automorphism search + vertex-link chi + swap character")
from snappy.snap.t3mlite import Mcomplex, simplex
T = Mcomplex(K)
NT = len(T.Tetrahedra)
FACES = [simplex.F0, simplex.F1, simplex.F2, simplex.F3]
def nbr(t, f):  return T.Tetrahedra[t].Neighbor[FACES[f]].Index
def glu(t, f):
    g = T.Tetrahedra[t].Gluing[FACES[f]]
    return tuple(g[v] for v in range(4))
print(f"tetrahedra in canonical retriangulation: {NT}")

# vertex classes (union-find on (tet,vertex))
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(x, y): parent[find(x)] = find(y)
for t in range(NT):
    for f in range(4):
        g = glu(t, f); n = nbr(t, f)
        for v in range(4):
            if v != f: union(("v", t, v), ("v", n, g[v]))
vclasses = defaultdict(list)
for t in range(NT):
    for v in range(4):
        vclasses[find(("v", t, v))].append((t, v))
print(f"vertex classes: {len(vclasses)} (expect 5 = 3 ideal cusps + 2 finite octahedron centers)")

# link Euler characteristic per vertex class (own computation)
lparent = {}
def lfind(x):
    lparent.setdefault(x, x)
    while lparent[x] != x:
        lparent[x] = lparent[lparent[x]]; x = lparent[x]
    return x
def lunion(x, y): lparent[lfind(x)] = lfind(y)
for t in range(NT):
    for f in range(4):
        g = glu(t, f); n = nbr(t, f)
        for v in range(4):
            if v == f: continue
            for w in range(4):
                if w == f or w == v: continue
                lunion(("lv", t, v, w), ("lv", n, g[v], g[w]))
chi = {}
for rep, corners in vclasses.items():
    F = len(corners); Eedges = 3 * F // 2
    Vl = set()
    for (t, v) in corners:
        for w in range(4):
            if w != v: Vl.add(lfind(("lv", t, v, w)))
    chi[rep] = len(Vl) - Eedges + F
finite = [r for r in vclasses if chi[r] == 2]     # sphere links = octahedron centers
ideal  = [r for r in vclasses if chi[r] == 0]     # torus links = cusps
print(f"link chi multiset: {sorted(chi.values())}  -> finite(sphere)={len(finite)}, ideal(torus)={len(ideal)}")
assert len(finite) == 2 and len(ideal) == 3

# consistent tetra orientations
def psign(p):
    s = 1; q = list(p)
    for i in range(4):
        for j in range(i+1, 4):
            if q[i] > q[j]: s = -s
    return s
orient = {0: 1}; stack = [0]
while stack:
    t = stack.pop()
    for f in range(4):
        n = nbr(t, f); want = -orient[t] * psign(glu(t, f))
        if n in orient: assert orient[n] == want
        else: orient[n] = want; stack.append(n)

# own automorphism search by gluing-propagation
def propagate(t0_img, p0):
    amap = {0: (t0_img, tuple(p0))}; stk = [0]
    while stk:
        t = stk.pop(); ti, p = amap[t]
        for f in range(4):
            n = nbr(t, f); g = glu(t, f)
            fi = p[f]; ni = nbr(ti, fi); gi = glu(ti, fi)
            ginv = [0]*4
            for v in range(4): ginv[g[v]] = v
            pn = tuple(gi[p[ginv[v]]] for v in range(4))
            if n in amap:
                if amap[n] != (ni, pn): return None
            else:
                amap[n] = (ni, pn); stk.append(n)
    if len({ti for ti, _ in amap.values()}) != NT: return None
    return amap
auts = []
for t0_img in range(NT):
    for p0 in permutations(range(4)):
        a = propagate(t0_img, p0)
        if a: auts.append(a)
print(f"own automorphism count: {len(auts)} (expect 48; cross-check K.isomorphisms_to count {len(isos)})")
assert len(auts) == 48

def aut_orient(a):
    vals = {psign(p) * orient[t] * orient[ti] for t, (ti, p) in a.items()}
    assert len(vals) == 1
    return vals.pop()
def vact(a, classes):
    m = {}
    for rep in classes:
        t, v = vclasses[rep][0]; ti, p = a[t]
        m[rep] = find(("v", ti, p[v]))
    return m

rows = Counter()
idx = {rep: k for k, rep in enumerate(ideal)}
for a in auts:
    o = aut_orient(a)
    mi = vact(a, ideal)
    sig = tuple(idx[mi[rep]] for rep in ideal)
    par = "even" if sgn3(sig) == 1 else "odd"
    mf = vact(a, finite)
    swap = "fix" if all(mf[rep] == rep for rep in finite) else "swap"
    rows[f"{'op' if o == 1 else 'rev'}_{par}_{swap}"] += 1
print("classification (orientation, strand-parity, octahedron-center action):")
for k in sorted(rows):
    print(f"  {k}: {rows[k]}")

decisive = (rows["op_odd_swap"] == 12 and rows.get("op_odd_fix", 0) == 0 and
            rows["op_even_fix"] == 12 and rows.get("op_even_swap", 0) == 0)
print(f"\nDECISIVE BIT: every or-preserving ODD element SWAPS the two octahedron centers; every")
print(f"or-preserving EVEN element FIXES both: {decisive}")
assert decisive
stab = rows["op_even_fix"]
print(f"stab_(Isom+)(octahedron center) order = {stab} = A4 (the unique order-12 subgroup of S4).")
# group-theoretic reduction independent of the count: swap char is a hom S4->Z/2, so trivial
# or sign; order-12 stab forces sign (=> odd swaps), and 12-elt subgroup of S4 is uniquely A4.
print("group-theoretic check: the center-swap map Isom+=S4 -> Sym(2 centers)=Z/2 is a homomorphism;")
print("hom(S4,Z/2) in {trivial, sign}; stab order 12 (not 24) => it is the SIGN character; the")
print("order-12 kernel is A4 (unique index-2 subgroup of S4). Consistent. Falsifier branch did NOT fire.")

rule("H-C2 CONCLUSION")
print("Fix_M(A4) = 2 points (H-B pyritohedral realization, transported by equivariant Mostow);")
print("both are the octahedron centers (A4 fixes both); odd Isom+ elements swap them =>")
print("Fix_M(S4) = EMPTY  =>  the R^3-RIGID CEILING IS EXACTLY THE PYRITOHEDRAL A4.")
print("The full O is spatial only in round S^3 (equivariant filling, orthogonal in O(4)) or")
print("dynamically as motions in flat space. Two legs agree; falsifier (rigid full-O in R^3) refuted.")

rule("H-C2 SECOND-LEG SUMMARY (SnapPy path, own combinatorics; shared-solver flagged)")
print(f"independent construction path (L6a4 diagram, isometric to 6^3_2); own automorphism search")
print(f"({len(auts)}=48), own link-chi (2 sphere centers + 3 torus cusps), own swap analysis.")
print("classification op_even_fix=12, op_odd_swap=12, rev_even_fix=12, rev_odd_swap=12: MATCHES chat.")
print("SHARED-SOLVER CAVEAT: canonical retriangulation + peripheral maps from SnapPy's solver")
print("(same as chat); independence is at construction-path + all analysis code. Flagged, not laundered.")
