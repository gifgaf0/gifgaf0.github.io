#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Independent cross-check leg for the finite-geometry claims G1..G19
(Fano planes on Z7, the 7-vertex torus, the cube picture, octonions,
complex structures J3/J5/J6, Delta(96), su(3), Fock vacua).

Written from scratch.  Exact arithmetic throughout: Python int,
fractions.Fraction, and a small Gaussian-rational class.  numpy is used
only as an integer-matrix container (and once for a float sanity check).

Constructions deliberately chosen to be "non-obvious":
  * octonion table built directly from the Fano+ triples (no Cayley-Dickson);
  * collineations by brute force over all 720 (resp. 5040) permutations;
  * derivations of O solved as an exact 512 x 64 linear system;
  * Clifford algebra / Fock spaces by Jordan-Wigner on 3 qubits (8 x 8,
    entries in Z[i]), vacua found as exact null spaces over Q(i).
"""
import itertools, json, math, os, random, sys
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CLAIMS = []
SURPRISES = []
KEY = {}


def claim(cid, holds, value, notes=""):
    CLAIMS.append({"id": cid, "holds": bool(holds), "value": value, "notes": notes})
    print(f"\n[{cid}] holds={bool(holds)}\n  value: {value}\n  notes: {notes}")


# ====================================================================
#  Gaussian rationals and generic exact linear algebra
# ====================================================================
class GQ:
    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = Fr(re)
        self.im = Fr(im)

    @staticmethod
    def c(o):
        return o if isinstance(o, GQ) else GQ(o, 0)

    def __add__(self, o):
        o = GQ.c(o); return GQ(self.re + o.re, self.im + o.im)
    __radd__ = __add__

    def __sub__(self, o):
        o = GQ.c(o); return GQ(self.re - o.re, self.im - o.im)

    def __rsub__(self, o):
        return GQ.c(o) - self

    def __mul__(self, o):
        o = GQ.c(o)
        return GQ(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)
    __rmul__ = __mul__

    def __neg__(self):
        return GQ(-self.re, -self.im)

    def conj(self):
        return GQ(self.re, -self.im)

    def abs2(self):
        return self.re * self.re + self.im * self.im

    def __truediv__(self, o):
        o = GQ.c(o); d = o.abs2(); n = self * o.conj()
        return GQ(n.re / d, n.im / d)

    def __eq__(self, o):
        if isinstance(o, (int, Fr)):
            o = GQ(o)
        if not isinstance(o, GQ):
            return NotImplemented
        return self.re == o.re and self.im == o.im

    def __hash__(self):
        return hash((self.re, self.im))

    def __repr__(self):
        if self.im == 0:
            return str(self.re)
        if self.re == 0:
            return f"{self.im}i"
        return f"({self.re}+{self.im}i)"


I_ = GQ(0, 1)


def nullspace(A, ncols, zero, one):
    """Exact basis of {x : A x = 0}; A is a list of rows over a field."""
    M = [list(r) for r in A if any(x != zero for x in r)]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] != zero:
                piv = i; break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c]
        M[r] = [x / inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != zero:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        pivots.append(c)
        r += 1
        if r == len(M):
            break
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        v = [zero] * ncols
        v[fc] = one
        for i, pc in enumerate(pivots):
            v[pc] = zero - M[i][fc]
        basis.append(v)
    return basis


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def perm_sign(p):
    s = 1
    p = list(p)
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s


def det_leibniz(M, zero):
    n = len(M)
    tot = zero
    for p in itertools.permutations(range(n)):
        term = GQ(perm_sign(p)) if isinstance(zero, GQ) else perm_sign(p)
        for i in range(n):
            term = term * M[i][p[i]]
        tot = tot + term
    return tot


# ====================================================================
#  Basic objects
# ====================================================================
QR = (1, 2, 4)
QNR = (3, 5, 6)
LINK_EXPECTED = [1, 3, 2, 6, 4, 5]


def lp(i):
    return tuple(sorted({i % 7, (i + 1) % 7, (i + 3) % 7}))


def lm(i):
    return tuple(sorted({i % 7, (i + 2) % 7, (i + 3) % 7}))


FP = sorted(lp(i) for i in range(7))
FM = sorted(lm(i) for i in range(7))
FPs, FMs = set(FP), set(FM)
TRIS = FP + FM


def lines_through(lines, a, b):
    return [L for L in lines if a in L and b in L]


def cycle_from_edges(edges):
    """Return (single_cycle?, order) ; order starts at min vertex, goes to its smaller neighbour."""
    adj = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    if any(len(v) != 2 for v in adj.values()):
        return False, None
    start = min(adj)
    prev, cur = start, min(adj[start])
    order = [start]
    while cur != start:
        order.append(cur)
        nxt = [x for x in adj[cur] if x != prev][0]
        prev, cur = cur, nxt
    return len(order) == len(adj), order


def same_cycle(c1, c2):
    c1, c2 = list(c1), list(c2)
    if len(c1) != len(c2):
        return False
    for seq in (c2, c2[::-1]):
        for k in range(len(seq)):
            if seq[k:] + seq[:k] == c1:
                return True
    return False


def matchings(S):
    S = list(S)
    if not S:
        yield []
        return
    a = S[0]
    for b in S[1:]:
        rest = [x for x in S if x not in (a, b)]
        for m in matchings(rest):
            yield [tuple(sorted((a, b)))] + m


ALLM = [frozenset(m) for m in matchings(range(1, 7))]


def mapM(M, f):
    return frozenset(tuple(sorted((f(a), f(b)))) for a, b in M)


JP = {c: frozenset(tuple(sorted((r, c * r % 7))) for r in QR) for c in QNR}
JNAME = {3: "J3", 5: "J5", 6: "J6"}


def Jmat(c):
    """6x6 integer matrix, index = label-1, J e_r = e_{cr}, J e_{cr} = -e_r (r in QR)."""
    J = np.zeros((6, 6), dtype=int)
    for r in QR:
        cr = c * r % 7
        J[cr - 1, r - 1] = 1
        J[r - 1, cr - 1] = -1
    return J


JM = {c: Jmat(c) for c in QNR}

# ====================================================================
#  G1
# ====================================================================
fano_p = len(FPs) == 7 and all(len(lines_through(FP, a, b)) == 1 for a, b in itertools.combinations(range(7), 2))
fano_m = len(FMs) == 7 and all(len(lines_through(FM, a, b)) == 1 for a, b in itertools.combinations(range(7), 2))
shared = FPs & FMs
EDGES = list(itertools.combinations(range(7), 2))
edge_tri = {e: sum(1 for T in TRIS if e[0] in T and e[1] in T) for e in EDGES}
links = {}
for v in range(7):
    led = [tuple(x for x in T if x != v) for T in TRIS if v in T]
    ok, order = cycle_from_edges(led)
    links[v] = (ok and order is not None and len(order) == 6, order)
chi = 7 - len(EDGES) + len(TRIS)
g1 = fano_p and fano_m and not shared and all(v == 2 for v in edge_tri.values()) \
    and all(links[v][0] for v in range(7)) and chi == 0
claim("G1", g1,
      f"Fano+ is Fano plane={fano_p}, Fano- is Fano plane={fano_m}, shared lines={sorted(shared)}, "
      f"edges in exactly 2 triangles: {sum(1 for v in edge_tri.values() if v == 2)}/21, "
      f"vertex links single 6-cycles: {sum(1 for v in range(7) if links[v][0])}/7, chi=7-21+14={chi}",
      "Every pair lies in exactly one Fano+ line and exactly one Fano- line (so each edge in exactly one + and one - triangle).")

# ====================================================================
#  G2
# ====================================================================
link0 = links[0][1]
types0 = []
for k in range(6):
    a, b = LINK_EXPECTED[k], LINK_EXPECTED[(k + 1) % 6]
    T = tuple(sorted((0, a, b)))
    types0.append(((a, b), "+" if T in FPs else ("-" if T in FMs else "?")))
alt = [t for _, t in types0] == ["+", "-", "+", "-", "+", "-"]
claim("G2", same_cycle(link0, LINK_EXPECTED) and alt,
      f"link(0) computed = {link0}; consecutive types = {[(list(p), t) for p, t in types0]}",
      "")

# ====================================================================
#  G3  octonions directly from the Fano+ triples
# ====================================================================
REAL = 7
MT = {}
for a in range(8):
    for b in range(8):
        if a == REAL:
            MT[a, b] = (1, b)
        elif b == REAL:
            MT[a, b] = (1, a)
        elif a == b:
            MT[a, b] = (-1, REAL)
for i in range(7):
    x, y, z = i, (i + 1) % 7, (i + 3) % 7
    for (p, q, r) in ((x, y, z), (y, z, x), (z, x, y)):
        assert (p, q) not in MT and (q, p) not in MT
        MT[p, q] = (1, r)
        MT[q, p] = (-1, r)
assert len(MT) == 64


def omul(u, v):
    w = [0] * 8
    for a in range(8):
        if u[a] == 0:
            continue
        for b in range(8):
            if v[b] == 0:
                continue
            s, c = MT[a, b]
            w[c] += s * u[a] * v[b]
    return w


def basis(k):
    v = [0] * 8
    v[k] = 1
    return v


def sub(u, v):
    return [a - b for a, b in zip(u, v)]


def assoc(x, y, z):
    return sub(omul(omul(x, y), z), omul(x, omul(y, z)))


B8 = [basis(k) for k in range(8)]
alt_basis_xxy = all(omul(x, omul(x, y)) == omul(omul(x, x), y) for x in B8 for y in B8)
alt_basis_yxx = all(omul(omul(y, x), x) == omul(y, omul(x, x)) for x in B8 for y in B8)
# full alternativity <=> associator alternating multilinear form
assoc_alt = True
for a, b, c in itertools.product(range(8), repeat=3):
    A = assoc(B8[a], B8[b], B8[c])
    if [p + q for p, q in zip(A, assoc(B8[b], B8[a], B8[c]))] != [0] * 8:
        assoc_alt = False
    if [p + q for p, q in zip(A, assoc(B8[a], B8[c], B8[b]))] != [0] * 8:
        assoc_alt = False
nonassoc = any(assoc(B8[a], B8[b], B8[c]) != [0] * 8 for a, b, c in itertools.product(range(7), repeat=3))
rng = random.Random(20261020)
norm_ok = True
alt_rand_ok = True
NRAND = 400
for _ in range(NRAND):
    u = [rng.randint(-9, 9) for _ in range(8)]
    v = [rng.randint(-9, 9) for _ in range(8)]
    w = omul(u, v)
    if sum(t * t for t in w) != sum(t * t for t in u) * sum(t * t for t in v):
        norm_ok = False
    if omul(u, omul(u, v)) != omul(omul(u, u), v) or omul(omul(v, u), u) != omul(v, omul(u, u)):
        alt_rand_ok = False
# left multiplication by e0 on span(e1..e6)
L0 = np.zeros((6, 6), dtype=int)
for k in range(1, 7):
    w = omul(basis(0), basis(k))
    assert w[0] == 0 and w[REAL] == 0
    for j in range(1, 7):
        L0[j - 1, k - 1] = w[j]
L0_is_J3 = bool((L0 == JM[3]).all())
claim("G3", alt_basis_xxy and assoc_alt and norm_ok and alt_rand_ok and L0_is_J3 and nonassoc,
      f"x(xy)=(xx)y on all 64 basis pairs: {alt_basis_xxy}; (yx)x=y(xx): {alt_basis_yxx}; "
      f"associator alternating on all 512 basis triples (=> fully alternative): {assoc_alt}; "
      f"non-associative: {nonassoc}; |xy|^2=|x|^2|y|^2 exactly on {NRAND} random integer pairs: {norm_ok}; "
      f"x(xy)=(xx)y on the random pairs too: {alt_rand_ok}; L_e0|span(e1..e6) == J3: {L0_is_J3}",
      "Checked the linearised (alternating-associator) condition, which is the actual definition of alternativity; "
      "x(xy)=(xx)y on basis elements alone would not suffice.")

# ====================================================================
#  G4
# ====================================================================
inv2 = [M for M in ALLM if mapM(M, lambda t: 2 * t % 7) == M]
inv2_names = sorted(JNAME[c] for c in QNR if JP[c] in inv2)
ANG = {lab: 60 * k for k, lab in enumerate(LINK_EXPECTED)}


def rel_angle(a, b):
    d = (ANG[b] - ANG[a]) % 360
    return d - 360 if d > 180 else d


offsets = {}
for c in QNR:
    offsets[JNAME[c]] = sorted({rel_angle(r, c * r % 7) for r in QR})
g4 = len(ALLM) == 15 and len(inv2) == 3 and inv2_names == ["J3", "J5", "J6"] \
    and offsets["J3"] == [60] and offsets["J5"] == [-60] and offsets["J6"] in ([180], [-180])
claim("G4", g4,
      f"#matchings={len(ALLM)}; invariant under x->2x: {[sorted(map(list, M)) for M in inv2]} = {inv2_names}; "
      f"partner angle offsets (r in QR): {offsets}",
      "J6 offset is 180 for r=1,2 and -180 for r=4 (same thing).")

# ====================================================================
#  G5
# ====================================================================
pos = {lab: k for k, lab in enumerate(LINK_EXPECTED)}
turns = {}
for steps in range(1, 6):
    rot = {lab: LINK_EXPECTED[(pos[lab] + steps) % 6] for lab in LINK_EXPECTED}
    mult = [a for a in range(1, 7) if all(rot[x] == a * x % 7 for x in range(1, 7))]
    turns[60 * steps] = mult[0] if mult else None


def fam_map(a):
    imgP = {tuple(sorted(a * t % 7 for t in L)) for L in FP}
    imgM = {tuple(sorted(a * t % 7 for t in L)) for L in FM}
    if imgP == FPs and imgM == FMs:
        return "preserves"
    if imgP == FMs and imgM == FPs:
        return "swaps"
    return "neither"


fam = {a: fam_map(a) for a in range(1, 7)}
g5 = turns == {60: 3, 120: 2, 180: 6, 240: 4, 300: 5} and fam[2] == fam[4] == "preserves" \
    and fam[3] == fam[5] == fam[6] == "swaps"
claim("G5", g5,
      f"turn (deg, with link (1,3,2,6,4,5) at 0,60,..,300 counterclockwise) -> multiplier: {turns}; "
      f"family behaviour of x->ax: {fam}",
      "Orientation: angle increasing along the listed link order; the reverse orientation swaps 3x<->5x.")

# ====================================================================
#  G6  stabiliser by brute force over all 720 permutations fixing 0
# ====================================================================
def maps_lines(p, src, dst):
    return all(tuple(sorted(p[x] for x in L)) in dst for L in src)


PERMS0 = [(0,) + q for q in itertools.permutations(range(1, 7))]
G = [p for p in PERMS0 if maps_lines(p, FP, FPs)]
Gset = set(G)
mulperm = {a: tuple(a * x % 7 for x in range(7)) for a in range(1, 7)}
in_G = {a: mulperm[a] in Gset for a in range(1, 7)}
affine_in_G = []
for a in range(1, 7):
    for b in range(7):
        q = tuple((a * x + b) % 7 for x in range(7))
        if q in Gset:
            affine_in_G.append((a, b))
g6 = len(G) == 24 and in_G[2] and in_G[4] and not (in_G[3] or in_G[5] or in_G[6]) \
    and sorted(affine_in_G) == [(1, 0), (2, 0), (4, 0)]
claim("G6", g6,
      f"|G|={len(G)} (from 720 brute force); x->ax in G: {in_G}; affine x->ax+b in G: {affine_in_G}",
      "Affine maps fixing 0 necessarily have b=0. Also: G maps Fano- to Fano- ? "
      f"{all(maps_lines(p, FM, FMs) for p in G)}")
KEY["G_order"] = str(len(G))
G_torus = [p for p in G if maps_lines(p, FM, FMs)]
print("  elements of G that also preserve Fano- (torus automorphisms fixing 0 and the +/- colouring):",
      [[p[a] for a in range(1, 7)] for p in G_torus])
KEY["G_elements_preserving_fano_minus"] = str(len(G_torus))
TORUS_AUT0 = [p for p in PERMS0 if maps_lines(p, TRIS, set(TRIS))]
print("  all permutations fixing 0 that preserve the 14-triangle torus:", len(TORUS_AUT0),
      [[p[a] for a in range(1, 7)] for p in TORUS_AUT0])
KEY["torus_automorphisms_fixing_0"] = str(len(TORUS_AUT0))
KEY["G_preserves_fano_minus_too"] = str(all(maps_lines(p, FM, FMs) for p in G))

# ====================================================================
#  G7  cube matrices
# ====================================================================
PHI = {1: "+x", 3: "-x", 2: "+y", 6: "-y", 4: "+z", 5: "-z"}
NORM = {1: (1, 0, 0), 3: (-1, 0, 0), 2: (0, 1, 0), 6: (0, -1, 0), 4: (0, 0, 1), 5: (0, 0, -1)}
FACE_OF = {v: k for k, v in NORM.items()}
OPP = {f: FACE_OF[tuple(-t for t in NORM[f])] for f in NORM}
I3 = np.eye(3, dtype=int)


def Pmat(g):
    cols = [NORM[g[1]], NORM[g[2]], NORM[g[4]]]
    P = np.array(cols, dtype=int).T
    for a in range(1, 7):
        if tuple(int(t) for t in P @ np.array(NORM[a])) != NORM[g[a]]:
            return None
    return P


def key3(M):
    return tuple(int(t) for t in np.asarray(M).flatten())


PERM3 = [np.eye(3, dtype=int)[list(s)] for s in itertools.permutations(range(3))]
DIAG = [np.diag(d) for d in itertools.product([1, -1], repeat=3)]
TD = {key3(D @ P): D @ P for D in DIAG for P in PERM3 if round(np.prod(np.diag(D))) == 1}
OH = {key3(D @ P): D @ P for D in DIAG for P in PERM3}
OROT = {k: M for k, M in OH.items() if det3(M.tolist()) == 1}
assert len(TD) == 24 and len(OROT) == 24 and len(OH) == 48

Gd = [{a: p[a] for a in range(1, 7)} for p in G]
PG = {}
all_exist = True
signed_perm = True
for p, g in zip(G, Gd):
    P = Pmat(g)
    if P is None:
        all_exist = False
        continue
    PG[p] = P
    if not (all(sorted(abs(int(t)) for t in row) == [0, 0, 1] for row in P)):
        signed_perm = False
img = {key3(P) for P in PG.values()}
img_eq_TD = img == set(TD)
hom = True
for p in G:
    for q in G:
        comp = tuple(p[q[x]] for x in range(7))
        if key3(PG[comp]) != key3(PG[p] @ PG[q]):
            hom = False
P2 = PG[mulperm[2]]
P2_is_c3 = key3(P2) == key3(np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])) \
    and tuple(P2 @ np.array([1, 1, 1])) == (1, 1, 1)
two_x_faces = [(PHI[a], PHI[2 * a % 7]) for a in (1, 2, 4)]
claim("G7", all_exist and signed_perm and img_eq_TD and len(img) == 24 and hom and P2_is_c3,
      f"P_g exists for all 24: {all_exist}; signed permutation: {signed_perm}; #distinct={len(img)}; "
      f"{{P_g}} == T_d: {img_eq_TD}; homomorphism (P_gh = P_g P_h): {hom}; "
      f"P_(x->2x) = {P2.tolist()} (columns = images of x,y,z), faces {two_x_faces}",
      "x->2x is the +120 deg rotation about (1,1,1) (right-hand rule): +x->+y->+z.")

# ====================================================================
#  G8  classification
# ====================================================================
def mat_order(P):
    Q = np.eye(3, dtype=int)
    for k in range(1, 50):
        Q = Q @ P
        if (Q == I3).all():
            return k
    return None


def prim(v):
    v = [int(t) for t in v]
    g = 0
    for t in v:
        g = math.gcd(g, abs(t))
    return [t // g for t in v] if g else v


def canon_sign(v):
    for t in v:
        if t != 0:
            return v if t > 0 else [-s for s in v]
    return v


def antisym_axis(R):
    return [int(R[2][1] - R[1][2]), int(R[0][2] - R[2][0]), int(R[1][0] - R[0][1])]


def classify(P):
    P = np.asarray(P)
    d = det3(P.tolist())
    tr = int(np.trace(P))
    o = mat_order(P)
    info = {"det": int(d), "order": o, "trace": tr, "class": None, "axis": None, "angle_deg": None, "normal": None}
    if o == 1:
        info["class"] = "E"
        return info
    if d == 1:
        if o == 3:
            info.update({"class": "C3", "axis": prim(antisym_axis(P)), "angle_deg": 120})
        elif o == 2:
            col = [c for c in (P + I3).T if any(c)][0]
            info.update({"class": "C2", "axis": canon_sign(prim(col)), "angle_deg": 180})
        elif o == 4:
            info.update({"class": "C4", "axis": prim(antisym_axis(P)), "angle_deg": 90})
        return info
    # improper
    if o == 2 and tr == 1:
        col = [c for c in (P - I3).T if any(c)][0]
        n = canon_sign(prim(col))
        info.update({"class": "sigma_d" if sum(1 for t in n if t) == 2 else "sigma_h", "normal": n})
    elif o == 2 and tr == -3:
        info["class"] = "i"
    elif o == 4:
        A = P + I3
        rows = [r for r in A if any(r)]
        n = None
        for r1, r2 in itertools.combinations(rows, 2):
            cr = np.cross(r1, r2)
            if any(cr):
                n = prim(cr)
                break
        n = np.array(n)
        sig = I3 - 2 * np.outer(n, n) // int(n @ n)
        R = sig @ P
        info.update({"class": "S4", "axis": prim(antisym_axis(R)), "angle_deg": 90})
    elif o == 6:
        info["class"] = "S6"
    return info


def cycles_str(g):
    seen = set()
    out = ""
    for a in range(1, 7):
        if a in seen:
            continue
        if g[a] == a:
            seen.add(a)
            continue
        cyc = [a]
        seen.add(a)
        b = g[a]
        while b != a:
            cyc.append(b)
            seen.add(b)
            b = g[b]
        out += "(" + " ".join(map(str, cyc)) + ")"
    return out or "()"


# conjugacy classes of T_d by brute force
TDl = list(TD.values())
TDinv = {key3(M): M.T for M in TDl}
classes = []
seen = set()
for M in TDl:
    k = key3(M)
    if k in seen:
        continue
    cl = {key3(X @ M @ X.T) for X in TDl}
    seen |= cl
    classes.append(cl)
class_of = {}
for cl in classes:
    names = {classify(TD[k])["class"] for k in cl}
    assert len(names) == 1
    nm = names.pop()
    for k in cl:
        class_of[k] = (nm, len(cl))
class_sizes = sorted({v for v in class_of.values()}, key=lambda t: t[0])

STAB = []
for p in sorted(G):
    g = {a: p[a] for a in range(1, 7)}
    P = PG[p]
    info = classify(P)
    nm, sz = class_of[key3(P)]
    assert nm == info["class"]
    torus = None
    if p == mulperm[2]:
        torus = "x->2x"
    elif p == mulperm[4]:
        torus = "x->4x"
    elif p == mulperm[1]:
        torus = "id"
    STAB.append({
        "perm": [p[a] for a in range(1, 7)],
        "cycles": cycles_str(g),
        "matrix": [[int(t) for t in row] for row in P],
        "det": info["det"],
        "class": info["class"],
        "axis": info["axis"],
        "angle_deg": info["angle_deg"],
        "normal": info["normal"],
        "torus": torus,
        "fixes_QR_corner": bool(tuple(int(t) for t in P @ np.array([1, 1, 1])) == (1, 1, 1)),
    })
cnt = {}
for s in STAB:
    cnt[s["class"]] = cnt.get(s["class"], 0) + 1
rot90 = [k for k in OROT if classify(OROT[k])["class"] == "C4"]
rot90_in = any(k in img for k in rot90)
inv_in = key3(-I3) in img
g8 = cnt == {"E": 1, "C3": 8, "C2": 3, "S4": 6, "sigma_d": 6} and not rot90_in and not inv_in \
    and sorted(class_sizes) == sorted([("E", 1), ("C3", 8), ("C2", 3), ("S4", 6), ("sigma_d", 6)])
print("\nG8 table:")
for s in STAB:
    print("  ", s["perm"], s["cycles"].ljust(18), s["class"].ljust(8), "axis", s["axis"], "angle", s["angle_deg"],
          "normal", s["normal"], "torus", s["torus"], "fixQR", s["fixes_QR_corner"])
claim("G8", g8,
      f"class counts {cnt}; T_d conjugacy classes (brute force) {class_sizes}; "
      f"#90-deg rotations in O: {len(rot90)}, any in {{P_g}}: {rot90_in}; -I in {{P_g}}: {inv_in}. "
      "Full table in stabilizer[] of the JSON.",
      "Conventions: C3 axis oriented so the rotation is +120 deg (right-hand rule), so x->2x has axis (1,1,1) and "
      "x->4x axis (-1,-1,-1); C2 axis and sigma_d normal sign-normalised (first nonzero entry positive); S4 axis "
      "oriented so that S = (reflection in plane perp. to axis) o (rotation +90 about axis).")
KEY["class_counts"] = json.dumps(cnt, sort_keys=True)

# ====================================================================
#  G9  bijections psi
# ====================================================================
FACES = [1, 2, 3, 4, 5, 6]   # faces named by their phi-label


def face_perm(M):
    return tuple(FACE_OF[tuple(int(t) for t in M @ np.array(NORM[f]))] for f in FACES)


TdF = {face_perm(M) for M in TD.values()}
OF = {face_perm(M) for M in OROT.values()}
OhF = {face_perm(M) for M in OH.values()}
assert len(TdF) == 24 and len(OF) == 24 and len(OhF) == 48
T1 = {(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)}


def corner_signs(faceset):
    v = [0, 0, 0]
    for f in faceset:
        for i in range(3):
            if NORM[f][i]:
                v[i] = NORM[f][i]
    return tuple(v)


good_td, good_o = [], []
for img6 in itertools.permutations(FACES):
    psi = {a: img6[a - 1] for a in range(1, 7)}
    pinv = {v: k for k, v in psi.items()}
    conj = {tuple(psi[g[pinv[f]]] for f in FACES) for g in Gd}
    if conj == TdF:
        good_td.append(psi)
    if conj == OF:
        good_o.append(psi)
stats = {"J3_opposite": 0, "J5_adjacent": 0, "J6_adjacent": 0, "QR_corner": 0, "QR_T1": 0, "QR_T2": 0}
for psi in good_td:
    if all(psi[b] == OPP[psi[a]] for a, b in JP[3]):
        stats["J3_opposite"] += 1
    if all(psi[b] != OPP[psi[a]] for a, b in JP[5]):
        stats["J5_adjacent"] += 1
    if all(psi[b] != OPP[psi[a]] for a, b in JP[6]):
        stats["J6_adjacent"] += 1
    fq = [psi[r] for r in QR]
    if all(OPP[a] != b for a, b in itertools.combinations(fq, 2)):
        stats["QR_corner"] += 1
        if corner_signs(fq) in T1:
            stats["QR_T1"] += 1
        else:
            stats["QR_T2"] += 1
n = len(good_td)
g9 = n == 48 and len(good_o) == 0 and stats == {"J3_opposite": 48, "J5_adjacent": 48, "J6_adjacent": 48,
                                                 "QR_corner": 48, "QR_T1": 24, "QR_T2": 24}
claim("G9", g9,
      f"#psi with psi G psi^-1 = T_d face action: {n}; = O face action: {len(good_o)}; statistics over the {n}: {stats}",
      "The 48 are phi composed with the O_h face action (normaliser of the T_d face action in S6 is O_h, order 48). "
      "O is impossible because a point stabiliser in G is a Klein 4-group while a face stabiliser in O is C4. "
      f"Is phi among the 48: {any(psi == {a: a for a in FACES} for psi in good_td)}; "
      f"set of 48 == phi o O_h: {sorted(tuple(psi[a] for a in FACES) for psi in good_td) == sorted(OhF)}")
KEY["psi_Td_count"] = str(n)
KEY["psi_O_count"] = str(len(good_o))

# ====================================================================
#  G10  Fano plane on the cube
# ====================================================================
FP_through0 = [L for L in FP if 0 in L]
axes_ok = sorted(tuple(x for x in L if x) for L in FP_through0) == sorted(tuple(sorted(p)) for p in JP[3]) \
    and all(OPP[a] == b for a, b in (tuple(x for x in L if x) for L in FP_through0))
CORNERS = []
for s in itertools.product([1, -1], repeat=3):
    faces = sorted(FACE_OF[tuple(s[i] if j == i else 0 for j in range(3))] for i in range(3))
    tet = "T1" if s in T1 else "T2"
    CORNERS.append({"signs": list(s), "faces": faces, "tetra": tet,
                    "fano_plus_line": tuple(faces) in FPs, "fano_minus_line": tuple(faces) in FMs})
T1_lines = sorted(tuple(c["faces"]) for c in CORNERS if c["tetra"] == "T1")
FP_not0 = sorted(L for L in FP if 0 not in L)
T2_info = {tuple(c["signs"]): (c["faces"], c["fano_plus_line"], c["fano_minus_line"]) for c in CORNERS if c["tetra"] == "T2"}
corner_lookup = {tuple(c["signs"]): tuple(c["faces"]) for c in CORNERS}
expected_T1 = {(1, 1, 1): (1, 2, 4), (1, -1, -1): (1, 5, 6), (-1, 1, -1): (2, 3, 5), (-1, -1, 1): (3, 4, 6)}
t1_ok = all(corner_lookup[k] == v for k, v in expected_T1.items()) and T1_lines == FP_not0
t2_ok = T2_info[(-1, -1, -1)] == ([3, 5, 6], False, True) and \
    all((not fp) and (not fm) for k, (f, fp, fm) in T2_info.items() if k != (-1, -1, -1)) and \
    sorted(tuple(f) for k, (f, fp, fm) in T2_info.items() if k != (-1, -1, -1)) == [(1, 2, 5), (1, 4, 6), (2, 3, 4)]
FM_through0 = [tuple(x for x in L if x) for L in FM if 0 in L]
fm0_ok = sorted(FM_through0) == sorted(tuple(sorted(p)) for p in JP[5]) and all(OPP[a] != b for a, b in FM_through0)
fm_other = {}
for L in FM:
    if 0 in L:
        continue
    fm_other[L] = sum(1 for a, b in itertools.combinations(L, 2) if OPP[a] == b)
fm_other_ok = all((v == 1) for L, v in fm_other.items() if L != (3, 5, 6)) and fm_other[(3, 5, 6)] == 0
act4 = {tuple(FP_not0.index(tuple(sorted(p[x] for x in L))) for L in FP_not0) for p in G}
g10 = axes_ok and t1_ok and t2_ok and fm0_ok and fm_other_ok and len(act4) == 24
claim("G10", g10,
      f"Fano+ lines through 0 -> opposite pairs (axes): {axes_ok}; T1 corners = Fano+ lines not through 0: {t1_ok} "
      f"{ {str(k): corner_lookup[k] for k in expected_T1} }; T2 corners (faces, F+, F-): "
      f"{ {str(k): v for k, v in T2_info.items()} }; Fano- through 0 = J5 pairs, adjacent: {fm0_ok}; "
      f"opposite-pair counts in other Fano- lines: { {str(k): v for k, v in fm_other.items()} }; "
      f"G on the 4 Fano+ lines not through 0: image of order {len(act4)} (= S4: {len(act4) == 24})",
      "")

# ====================================================================
#  G11  Fano diagram layout (exact geometry in Q(sqrt3): point (x, s) means (x, s*sqrt3))
# ====================================================================
V = {3: (Fr(0), Fr(0)), 5: (Fr(2), Fr(0)), 6: (Fr(1), Fr(1))}   # equilateral triangle (0,0),(2,0),(1,sqrt3)


def mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


PTS = dict(V)
PTS[1] = mid(V[5], V[6])
PTS[2] = mid(V[3], V[5])
PTS[4] = mid(V[3], V[6])
PTS[0] = ((V[3][0] + V[5][0] + V[6][0]) / 3, (V[3][1] + V[5][1] + V[6][1]) / 3)


def collinear(a, b, c):
    (x1, s1), (x2, s2), (x3, s3) = PTS[a], PTS[b], PTS[c]
    # cross product of (b-a),(c-a) = sqrt3 * ((x2-x1)(s3-s1) - (x3-x1)(s2-s1))
    return (x2 - x1) * (s3 - s1) - (x3 - x1) * (s2 - s1) == 0


def d2(p, q):
    return (p[0] - q[0]) ** 2 + 3 * (p[1] - q[1]) ** 2


straight = sorted(T for T in itertools.combinations(range(7), 3) if collinear(*T))
inr2 = Fr(1, 3)   # inradius^2 of side-2 equilateral triangle
oncircle = tuple(sorted(k for k in range(7) if d2(PTS[k], PTS[0]) == inr2))
diagram_lines = sorted(set(straight) | {oncircle})
sides = [tuple(sorted(T)) for T in [(5, 1, 6), (3, 2, 5), (3, 4, 6)]]
medians = [tuple(sorted(T)) for T in [(3, 0, 1), (6, 0, 2), (5, 0, 4)]]
g11 = diagram_lines == FP and oncircle == (1, 2, 4) and sorted(sides + medians) == straight
claim("G11", g11,
      f"collinear triples in the exact layout: {straight}; points on the incircle: {oncircle}; "
      f"7 diagram lines == Fano+ lines: {diagram_lines == FP}",
      "Geometry done exactly (equilateral triangle with vertices 3,5,6, midpoints 1,2,4, centroid 0); the incircle "
      "passes exactly through the three midpoints.")

# ====================================================================
#  G12  corner view
# ====================================================================
d = np.array([1, 1, 1])


def proj3(f):
    nv = np.array(NORM[f])
    return 3 * nv - int(nv @ d) * d


ref = proj3(1)
e2 = np.cross(d, ref)   # d x ref : counterclockwise as seen from +d (looking towards the origin)


def ang(f):
    p = proj3(f)
    return math.degrees(math.atan2(float(p @ e2) / float(np.linalg.norm(e2)), float(p @ ref) / float(np.linalg.norm(ref)))) % 360


angles = {f: round(ang(f), 9) for f in FACES}
cv_order = sorted(FACES, key=lambda f: angles[f])
# exact 60-degree spacing check
exact60 = True
for k in range(6):
    p, q = proj3(cv_order[k]), proj3(cv_order[(k + 1) % 6])
    if not (2 * int(p @ q) == int(p @ p) == int(q @ q) and int(np.cross(p, q) @ d) > 0):
        exact60 = False
plus_120 = all(int(proj3(a) @ proj3(b)) * 2 == -int(proj3(a) @ proj3(a)) for a, b in itertools.combinations([1, 2, 4], 2))
minus_neg = all((proj3(OPP[a]) == -proj3(a)).all() for a in [1, 2, 4])
# cube edges = adjacent face pairs; corners of an edge
ADJ = [tuple(sorted(e)) for e in itertools.combinations(FACES, 2) if OPP[e[0]] != e[1]]
assert len(ADJ) == 12


def touches(edge, corner_faces):
    return set(edge) <= set(corner_faces)


petrie = sorted(e for e in ADJ if not touches(e, (1, 2, 4)) and not touches(e, (3, 5, 6)))
J5J6 = sorted(set(map(tuple, map(sorted, JP[5]))) | set(map(tuple, map(sorted, JP[6]))))


def jname_of(pair):
    pr = tuple(sorted(pair))
    for c in QNR:
        if pr in JP[c]:
            return JNAME[c]
    return None


cv_consec = [jname_of((cv_order[k], cv_order[(k + 1) % 6])) for k in range(6)]
cv_opp = [jname_of((cv_order[k], cv_order[k + 3])) for k in range(3)]
# silhouette (Petrie hexagon) as a polygon on cube corners
mixed = [c for c in itertools.product([1, -1], repeat=3) if c not in ((1, 1, 1), (-1, -1, -1))]


def edge_faces(c1, c2):
    i = [k for k in range(3) if c1[k] != c2[k]]
    if len(i) != 1:
        return None
    return tuple(sorted(FACE_OF[tuple(c1[j] if j == k else 0 for j in range(3))] for k in range(3) if k != i[0]))


poly = [mixed[0]]
while len(poly) < 6:
    nxt = [c for c in mixed if c not in poly and edge_faces(poly[-1], c)]
    poly.append(sorted(nxt)[0] if len(poly) == 1 else nxt[0])
sil_edges = [edge_faces(poly[k], poly[(k + 1) % 6]) for k in range(6)]
sil_types = [jname_of(e) for e in sil_edges]
sil_alt = all(sil_types[k] != sil_types[(k + 1) % 6] for k in range(6)) and set(sil_types) == {"J5", "J6"}
visible = {f for f in FACES if int(np.array(NORM[f]) @ d) > 0}
silhouette_set = sorted(e for e in ADJ if (e[0] in visible) != (e[1] in visible))
stabQR = [s for s in STAB if s["fixes_QR_corner"]]
stabQR_classes = sorted(s["class"] for s in stabQR)
trip_action = {tuple(s["perm"][r - 1] for r in QR) for s in stabQR}
weyl_ok = len(stabQR) == 6 and trip_action == set(itertools.permutations(QR)) and \
    stabQR_classes == sorted(["E", "C3", "C3", "sigma_d", "sigma_d", "sigma_d"])
mirror_normals = sorted(tuple(s["normal"]) for s in stabQR if s["class"] == "sigma_d")
g12 = plus_120 and minus_neg and exact60 and cv_order == [1, 5, 2, 3, 4, 6] and petrie == J5J6 and \
    silhouette_set == petrie and sil_alt and cv_consec == ["J5", "J6"] * 3 and cv_opp == ["J3"] * 3 and weyl_ok
claim("G12", g12,
      f"corner-view order (counterclockwise seen from +(1,1,1)) from +x: {cv_order} = {[PHI[f] for f in cv_order]}; "
      f"exact 60-deg spacing: {exact60}; +x,+y,+z at mutual 120 deg: {plus_120}; -x,-y,-z = negatives: {minus_neg}; "
      f"Petrie edges (touch neither (+++) nor (---)) = {petrie} == J5uJ6: {petrie == J5J6}; == silhouette edges: "
      f"{silhouette_set == petrie}; silhouette polygon edge types {sil_types}; consecutive pairs of the label hexagon "
      f"{cv_consec}; opposite pairs {cv_opp}; stabiliser of (+++) in G: classes {stabQR_classes}, mirror normals "
      f"{mirror_normals}, action on (+x,+y,+z) = full S3: {weyl_ok}",
      "Orientation: counterclockwise as seen by a viewer on the +(1,1,1) side; the opposite viewing side gives the "
      "reverse order (1,6,4,3,2,5). The mirrors are the Weyl reflections (normals e_i - e_j = SU(3) roots).")

# ====================================================================
#  G13  pairs of pairings -> hexagons
# ====================================================================
hexes = {}
g13_ok = True
for c1, c2, c3 in [(3, 5, 6), (5, 6, 3), (3, 6, 5)]:
    ok, order = cycle_from_edges(list(JP[c1]) + list(JP[c2]))
    opp = [jname_of((order[k], order[k + 3])) for k in range(3)] if ok else None
    hexes[JNAME[c3] + "_opposite"] = order
    if not (ok and opp == [JNAME[c3]] * 3):
        g13_ok = False
union9 = set().union(*[set(JP[c]) for c in QNR])
k33 = union9 == {tuple(sorted((a, b))) for a in QR for b in QNR}
# general-fact check: how many triples of pairwise disjoint perfect matchings have the 'third = opposite' property?
tot = good = 0
for M1, M2, M3 in itertools.permutations(ALLM, 3):
    if M1 & M2 or M1 & M3 or M2 & M3:
        continue
    tot += 1
    ok, order = cycle_from_edges(list(M1) + list(M2))
    if ok and all(tuple(sorted((order[k], order[k + 3]))) in M3 for k in range(3)):
        good += 1
g13 = g13_ok and hexes["J6_opposite"] == [1, 3, 2, 6, 4, 5] and hexes["J3_opposite"] == [1, 5, 2, 3, 4, 6]
claim("G13", g13,
      f"J3+J5 -> {hexes['J6_opposite']} (J6 opposite); J5+J6 -> {hexes['J3_opposite']} (J3 opposite); "
      f"J3+J6 -> {hexes['J5_opposite']} (J5 opposite)",
      "Two edge-disjoint perfect matchings of 6 points always form one 6-cycle, but a third disjoint matching need "
      f"not be the long diagonals: among ordered triples of pairwise-disjoint perfect matchings, {good}/{tot} have the "
      "'third joins opposite points' property. So it is a fact about J3,J5,J6 specifically, not fully general. "
      f"J3uJ5uJ6 = all 9 QR-QNR pairs (K_3,3): {k33}.")
KEY["J5_opposite_hexagon"] = str(hexes["J5_opposite"])

# ====================================================================
#  G14  Szilassi dual
# ====================================================================
sz_corners = []
for k in range(6):
    a, b = LINK_EXPECTED[k], LINK_EXPECTED[(k + 1) % 6]
    T = tuple(sorted((0, a, b)))
    sz_corners.append({"triangle": [0, a, b], "type": "up" if T in FPs else ("down" if T in FMs else "?")})
ups = sorted(tuple(sorted(c["triangle"][1:])) for c in sz_corners if c["type"] == "up")
downs = sorted(tuple(sorted(c["triangle"][1:])) for c in sz_corners if c["type"] == "down")
opp_edges = [jname_of((LINK_EXPECTED[k], LINK_EXPECTED[k + 3])) for k in range(3)]
each_edge_updown = all(len(lines_through(FP, a, b)) == 1 and len(lines_through(FM, a, b)) == 1 for a, b in EDGES)
# dual graph
dual_adj = {T: set() for T in TRIS}
for T1_, T2_ in itertools.combinations(TRIS, 2):
    if len(set(T1_) & set(T2_)) == 2:
        dual_adj[T1_].add(T2_)
        dual_adj[T2_].add(T1_)
bip = all((u in FPs) != (w in FPs) for u in TRIS for w in dual_adj[u])
cubic = all(len(v) == 3 for v in dual_adj.values())


def girth(adj):
    best = 10 ** 9
    for s in adj:
        dist = {s: 0}
        par = {s: None}
        q = [s]
        while q:
            u = q.pop(0)
            for w in adj[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1
                    par[w] = u
                    q.append(w)
                elif par[u] != w:
                    best = min(best, dist[u] + dist[w] + 1)
    return best


gir = girth(dual_adj)
g14 = [c["type"] for c in sz_corners] == ["up", "down"] * 3 and ups == sorted(tuple(sorted(p)) for p in JP[3]) \
    and downs == sorted(tuple(sorted(p)) for p in JP[5]) and opp_edges == ["J6"] * 3 and each_edge_updown and bip
claim("G14", g14,
      f"corners {[(c['triangle'], c['type']) for c in sz_corners]}; up-corner pairs {ups} (J3); down-corner pairs "
      f"{downs} (J5); opposite edges {opp_edges}; every torus edge in one up + one down triangle: {each_edge_updown}; "
      f"dual skeleton bipartite: {bip}, cubic: {cubic}, 14 vertices, girth {gir} (Heawood graph)",
      "")

# ====================================================================
#  G15  orbits of pairings under G
# ====================================================================
def gmap(p):
    return lambda t: p[t]


orbit_J5 = {mapM(JP[5], gmap(p)) for p in G}
orbit_J6 = {mapM(JP[6], gmap(p)) for p in G}
J3_inv = all(mapM(JP[3], gmap(p)) == JP[3] for p in G)
stab5 = [p for p in G if mapM(JP[5], gmap(p)) == JP[5]]
stab6 = [p for p in G if mapM(JP[6], gmap(p)) == JP[6]]
all_adjacent = {M for M in ALLM if all(OPP[a] != b for a, b in M)}
orbit_matchings_all = {}
for M in ALLM:
    orb = frozenset(mapM(M, gmap(p)) for p in G)
    orbit_matchings_all[orb] = len(orb)
claim("G15", J3_inv,
      f"J3 G-invariant: {J3_inv}; |orbit(J5)|={len(orbit_J5)}; J6 in orbit(J5): {JP[6] in orbit_J5}; "
      f"orbit(J5) == the 8 perfect matchings into adjacent-face pairs: {orbit_J5 == all_adjacent}; "
      f"stab(J5) = {[cycles_str({a: p[a] for a in range(1, 7)}) for p in stab5]} (size {len(stab5)}); "
      f"stab(J6) = {[cycles_str({a: p[a] for a in range(1, 7)}) for p in stab6]} (size {len(stab6)}); "
      f"G-orbit sizes on all 15 matchings: {sorted(orbit_matchings_all.values())}",
      "J5 and J6 are swapped by the three sigma_d mirrors through (1,1,1); each has stabiliser C3 = {id, 2x, 4x}.")
KEY["J5_orbit_size"] = str(len(orbit_J5))
KEY["stab_J5_size"] = str(len(stab5))
KEY["stab_J6_size"] = str(len(stab6))

# ====================================================================
#  G16  generation mismatch
# ====================================================================
ROWS = [(1, 3), (4, 5), (2, 6)]
COLS = [(2, 3), (4, 6), (1, 5)]
OV = [[len(set(r) & set(c)) for c in COLS] for r in ROWS]
two_ones = all(sorted(row) == [0, 1, 1] for row in OV) and all(sorted(col) == [0, 1, 1] for col in zip(*OV))
Bm = [[Fr(x, 2) for x in row] for row in OV]
ds = all(sum(row) == 1 for row in Bm) and all(sum(col) == 1 for col in zip(*Bm))
# unistochastic obstruction: for rows i != j, the terms |U_ik||U_jk| = sqrt(B_ik B_jk) must close a polygon
obstruction = []
for i, j in itertools.combinations(range(3), 2):
    terms = [Bm[i][k] * Bm[j][k] for k in range(3)]   # squares of the moduli
    nz = [t for t in terms if t != 0]
    obstruction.append(((i, j), len(nz)))
not_uni = all(nzc == 1 for _, nzc in obstruction)
claim("G16", two_ones and ds and not_uni,
      f"overlap = {OV}; two 1s per row/col: {two_ones}; half-matrix doubly stochastic: {ds}; "
      f"for each pair of rows the number of columns where both are nonzero: {obstruction}",
      "Not unistochastic: if |U_ij|^2 = B then rows i,j of U must be orthogonal, sum_k U_ik conj(U_jk) = 0, but any two "
      "rows of B share support in exactly one column, so that sum has exactly one nonzero term (modulus 1/2) and "
      "cannot vanish. (Equivalently the triangle/chain-links condition fails: moduli 1/2, 0, 0.)")

# ====================================================================
#  G17  signed automorphisms of the 7 imaginary units
# ====================================================================
SIGNS = np.array([list(s) + [1] for s in itertools.product([1, -1], repeat=7)], dtype=int)   # col 7 = real unit
ALL7 = list(itertools.permutations(range(7)))
AUT = []          # list of (perm(7), signs(7))
per_perm = {}
for p in ALL7:
    pp = list(p) + [REAL]
    ok = True
    for a in range(8):
        for b in range(8):
            t, c = MT[a, b]
            t2, c2 = MT[pp[a], pp[b]]
            if c2 != pp[c]:
                ok = False
                break
        if not ok:
            break
    if not ok:
        per_perm[p] = 0
        continue
    mask = np.ones(len(SIGNS), dtype=bool)
    for a in range(8):
        for b in range(8):
            t, c = MT[a, b]
            t2, c2 = MT[pp[a], pp[b]]
            mask &= (SIGNS[:, a] * SIGNS[:, b] * t2 == t * SIGNS[:, c])
    per_perm[p] = int(mask.sum())
    for s in SIGNS[mask]:
        AUT.append((p, tuple(int(x) for x in s[:7])))
COLL = [p for p in ALL7 if maps_lines(p, FP, FPs)]
eight_each = all(per_perm[p] == 8 for p in COLL) and all(per_perm[p] == 0 for p in ALL7 if p not in set(COLL))


def apply_aut(p, s, u):
    w = [0] * 8
    w[REAL] = u[REAL]
    for k in range(7):
        w[p[k]] += s[k] * u[k]
    return w


# sanity: full automorphism check on random octonions for a sample
rs = random.Random(7)
aut_sanity = True
for (p, s) in rs.sample(AUT, 40):
    for _ in range(5):
        u = [rs.randint(-5, 5) for _ in range(8)]
        v = [rs.randint(-5, 5) for _ in range(8)]
        if apply_aut(p, s, omul(u, v)) != omul(apply_aut(p, s, u), apply_aut(p, s, v)):
            aut_sanity = False
fix0 = [(p, s) for p, s in AUT if p[0] == 0]
plus0 = [(p, s) for p, s in fix0 if s[0] == 1]
minus0 = [(p, s) for p, s in fix0 if s[0] == -1]


def F6(p, s):
    F = np.zeros((6, 6), dtype=int)
    for k in range(1, 7):
        F[p[k] - 1, k - 1] = s[k]
    return F


J3m = JM[3]
Fplus = [F6(p, s) for p, s in plus0]
Fminus = [F6(p, s) for p, s in minus0]
commute_plus = all((F @ J3m == J3m @ F).all() for F in Fplus)
anti_minus = all((F @ J3m == -J3m @ F).all() for F in Fminus)
ZK = []
for r in QR:
    z = [GQ(0)] * 6
    z[r - 1] = GQ(1)
    z[3 * r % 7 - 1] = I_
    ZK.append(z)


def apply6(F, z):
    return [sum((GQ(int(F[i, j])) * z[j] for j in range(6)), GQ(0)) for i in range(6)]


def zcoords(w, bar=False):
    """coefficients of w in basis z_j (bar=False) or conj(z_j) (bar=True); None if w not in that span"""
    co = []
    for r in QR:
        cf = w[r - 1]
        co.append(cf)
    recon = [GQ(0)] * 6
    for cf, r in zip(co, QR):
        recon[r - 1] = recon[r - 1] + cf
        recon[3 * r % 7 - 1] = recon[3 * r % 7 - 1] + cf * (I_ if not bar else -I_)
    return co if recon == w else None


MZ = []
cl_ok = True
for F in Fplus:
    cols = []
    for z in ZK:
        co = zcoords(apply6(F, z))
        if co is None:
            cl_ok = False
            co = [GQ(0)] * 3
        cols.append(co)
    M = [[cols[k][j] for k in range(3)] for j in range(3)]   # M[j][k]: F z_k = sum_j M[j][k] z_j
    MZ.append(M)
MU4 = {GQ(1), GQ(-1), I_, -I_}
monomial = all(all(sum(1 for x in row if x != 0) == 1 for row in M) and
               all(sum(1 for x in col if x != 0) == 1 for col in zip(*M)) and
               all(x in MU4 for row in M for x in row if x != 0) for M in MZ)
dets = {repr(det_leibniz(M, GQ(0))) for M in MZ}
Mkeys = {tuple(tuple((x.re, x.im) for x in row) for row in M) for M in MZ}
# Delta(96) reference: all 3x3 monomial matrices with entries in mu4, det 1
REF = set()
for perm in itertools.permutations(range(3)):
    for ent in itertools.product(list(MU4), repeat=3):
        M = [[GQ(0)] * 3 for _ in range(3)]
        for i in range(3):
            M[i][perm[i]] = ent[i]
        if det_leibniz(M, GQ(0)) == GQ(1):
            REF.add(tuple(tuple((x.re, x.im) for x in row) for row in M))
is_delta96 = Mkeys == REF and len(REF) == 96
anti_ok = True
for F in Fminus:
    for z in ZK:
        if zcoords(apply6(F, z), bar=True) is None:
            anti_ok = False


def iorder(F):
    Q = np.eye(F.shape[0], dtype=int)
    for k in range(1, 200):
        Q = Q @ F
        if (Q == np.eye(F.shape[0], dtype=int)).all():
            return k


ord_counts = {}
for F in Fplus:
    o = iorder(F)
    ord_counts[str(o)] = ord_counts.get(str(o), 0) + 1
ord_counts = dict(sorted(ord_counts.items(), key=lambda t: int(t[0])))
ord_minus = {}
for F in Fminus:
    o = iorder(F)
    ord_minus[str(o)] = ord_minus.get(str(o), 0) + 1
g17 = len(AUT) == 1344 and eight_each and aut_sanity and len(fix0) == 192 and len(plus0) == 96 and \
    len(minus0) == 96 and commute_plus and cl_ok and monomial and dets == {"1"} and is_delta96 and \
    ord_counts == {"1": 1, "2": 15, "3": 32, "4": 24, "8": 24} and anti_minus and anti_ok
claim("G17", g17,
      f"#signed automorphisms (5040 perms x 128 signs, full 8x8 table) = {len(AUT)}; 8 per Fano+ collineation and 0 "
      f"otherwise: {eight_each} (#collineations={len(COLL)}); fixing e0 up to sign: {len(fix0)} = {len(plus0)} (+e0) + "
      f"{len(minus0)} (-e0); +e0 ones commute with J3: {commute_plus}, act on (z1,z2,z3) C-linearly: {cl_ok}, monomial "
      f"with entries in {{+-1,+-i}}: {monomial}, dets {dets}, image == all 96 mu4-monomial det-1 matrices "
      f"(= Delta(96)): {is_delta96}; element orders {ord_counts}; -e0 ones anticommute with J3 (C-antilinear, map "
      f"span(z) to span(zbar)): {anti_minus and anti_ok}",
      f"Orders of the 96 e0->-e0 maps (as real 6x6, a coset not a group): {dict(sorted(ord_minus.items(), key=lambda t: int(t[0])))}")
KEY["signed_automorphisms"] = str(len(AUT))
KEY["delta96_order_counts"] = json.dumps(ord_counts)

# ====================================================================
#  G18  derivations / su(3)
# ====================================================================
NV = 64   # D[r][c] -> var r*8+c   (D e_c = sum_r D[r][c] e_r)
rows = []
for a in range(8):
    for b in range(8):
        s, m = MT[a, b]
        eq = [[0] * NV for _ in range(8)]   # one equation per output component k
        for k in range(8):
            eq[k][k * 8 + m] += s   # D(e_a e_b) = s D e_m
        for c in range(8):          # (D e_a) e_b = sum_c D[c][a] e_c e_b
            sc, kc = MT[c, b]
            eq[kc][c * 8 + a] -= sc
        for c in range(8):          # e_a (D e_b) = sum_c D[c][b] e_a e_c
            sc, kc = MT[a, c]
            eq[kc][c * 8 + b] -= sc
        rows.extend(eq)
rows = [list(r) for r in {tuple(r) for r in rows} if any(r)]
rowsF = [[Fr(x) for x in r] for r in rows]
DER = nullspace(rowsF, NV, Fr(0), Fr(1))
dim_der = len(DER)
extra = []
for k in range(8):
    e = [Fr(0)] * NV
    e[k * 8 + 0] = Fr(1)
    extra.append(e)
SU3 = nullspace(rowsF + extra, NV, Fr(0), Fr(1))
SU3M = []
restr_ok = True
for v in SU3:
    D = [[v[r * 8 + c] for c in range(8)] for r in range(8)]
    for k in range(1, 7):
        if D[0][k] != 0 or D[REAL][k] != 0:
            restr_ok = False
    if any(D[r][REAL] != 0 for r in range(8)):
        restr_ok = False
    SU3M.append([[D[r][c] for c in range(1, 7)] for r in range(1, 7)])


def mm(A, B):
    n = len(A)
    return [[sum((A[i][k] * B[k][j] for k in range(n)), Fr(0)) for j in range(n)] for i in range(n)]


def msub(A, B):
    return [[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(A, B)]


def JF(c):
    return [[Fr(int(x)) for x in row] for row in JM[c]]


commutant = {}
commutant_basis = {}
for c in QNR:
    J = JF(c)
    comms = [msub(mm(D, J), mm(J, D)) for D in SU3M]
    sysrows = [[comms[t][i][j] for t in range(len(SU3M))] for i in range(6) for j in range(6)]
    ns = nullspace(sysrows, len(SU3M), Fr(0), Fr(1))
    commutant[JNAME[c]] = len(ns)
    commutant_basis[JNAME[c]] = [[[sum((t[q] * SU3M[q][i][j] for q in range(len(SU3M))), Fr(0)) for j in range(6)]
                                  for i in range(6)] for t in ns]


def common_kernel(mats):
    if not mats:
        return [[Fr(int(i == j)) for j in range(6)] for i in range(6)]
    rows_ = [row for M in mats for row in M]
    return nullspace(rows_, 6, Fr(0), Fr(1))


ker = {k: common_kernel(v) for k, v in commutant_basis.items()}
v124 = [Fr(1), Fr(1), Fr(0), Fr(1), Fr(0), Fr(0)]   # e1+e2+e4 (index = label-1)
annih_124 = {k: all(all(sum((M[i][j] * v124[j] for j in range(6)), Fr(0)) == 0 for i in range(6)) for M in v)
             for k, v in commutant_basis.items()}


def fmt_vec(v):
    return "+".join(f"{'' if x == 1 else ('-' if x == -1 else str(x))}e{j + 1}" for j, x in enumerate(v) if x != 0).replace("+-", "-")


def closed_bracket(bas):
    if not bas:
        return True
    flat = [[M[i][j] for M in bas] for i in range(6) for j in range(6)]
    for A, B in itertools.combinations(bas, 2):
        C = msub(mm(A, B), mm(B, A))
        aug = [r + [C[i // 6][i % 6]] for i, r in enumerate(flat)]
        # C in span iff rank unchanged: solve via nullspace with last coefficient
        ns = nullspace(aug, len(bas) + 1, Fr(0), Fr(1))
        if not any(v[-1] != 0 for v in ns) and any(C[i][j] != 0 for i in range(6) for j in range(6)):
            return False
    return True


closed = {k: closed_bracket(v) for k, v in commutant_basis.items()}


def rank_of(mats):
    # rank of the set of 6x6 matrices as vectors in R^36
    vecs = [[M[i][j] for i in range(6) for j in range(6)] for M in mats]
    return len(vecs) - len(nullspace([list(c) for c in zip(*vecs)], len(vecs), Fr(0), Fr(1)))


r5, r6 = rank_of(commutant_basis["J5"]), rank_of(commutant_basis["J6"])
r56 = rank_of(commutant_basis["J5"] + commutant_basis["J6"])
J5_eq_J6_commutant = (r5 == r6 == r56 == 3)
print("  rank J5-commutant", r5, "J6-commutant", r6, "joint span", r56, "-> identical subalgebra:", J5_eq_J6_commutant)
KEY["J5_and_J6_su3_commutants_identical"] = str(J5_eq_J6_commutant)
d96_comm = {JNAME[c]: sum(1 for F in Fplus if (F @ JM[c] == JM[c] @ F).all()) for c in QNR}
d96_comm_elems = {JNAME[c]: sorted(cycles_str({k: p[k] for k in range(1, 7)}) + ("" if all(x == 1 for x in s) else f" signs{list(s[1:])}")
                                   for (p, s), F in zip(plus0, Fplus) if (F @ JM[c] == JM[c] @ F).all()) for c in (5, 6)}
g18 = dim_der == 14 and len(SU3) == 8 and restr_ok and commutant == {"J3": 8, "J5": 3, "J6": 3} and annih_124["J6"] \
    and d96_comm == {"J3": 96, "J5": 3, "J6": 3}
claim("G18", g18,
      f"dim Der(O) = {dim_der}; dim(su3 = Der killing e0) = {len(SU3)}; preserves span(e1..e6): {restr_ok}; "
      f"commutant dims {commutant}; subalgebras closed under bracket: {closed}; common kernel on R^6: "
      f"{ {k: [fmt_vec(v) for v in vs] for k, vs in ker.items()} }; annihilates e1+e2+e4: {annih_124}; "
      f"#Delta(96) maps commuting: {d96_comm}; those for J5/J6: {d96_comm_elems}",
      "")
KEY["su3_commutant_dim"] = json.dumps(commutant)
KEY["delta96_commuting"] = json.dumps(d96_comm)

# ====================================================================
#  G19  Clifford algebra by Jordan-Wigner, Fock vacua
# ====================================================================
def gm(rows_):
    return [[GQ.c(x) for x in r] for r in rows_]


Id2 = gm([[1, 0], [0, 1]])
Xp = gm([[0, 1], [1, 0]])
Yp = [[GQ(0), -I_], [I_, GQ(0)]]
Zp = gm([[1, 0], [0, -1]])


def kron(A, B):
    return [[A[i // len(B)][j // len(B[0])] * B[i % len(B)][j % len(B[0])] for j in range(len(A[0]) * len(B[0]))]
            for i in range(len(A) * len(B))]


def kron_list(ms):
    out = ms[0]
    for m in ms[1:]:
        out = kron(out, m)
    return out


def mmul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), GQ(0)) for j in range(len(B[0]))] for i in range(len(A))]


def madd(A, B):
    return [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(A, B)]


def mscal(c, A):
    return [[c * a for a in r] for r in A]


def mdag(A):
    return [[A[j][i].conj() for j in range(len(A))] for i in range(len(A[0]))]


def iszero(A):
    return all(x == 0 for r in A for x in r)


def ident(n):
    return [[GQ(int(i == j)) for j in range(n)] for i in range(n)]


GAM = {}
for k in range(3):
    pre = [Zp] * k
    post = [Id2] * (2 - k)
    GAM[2 * k + 1] = kron_list(pre + [Xp] + post)
    GAM[2 * k + 2] = kron_list(pre + [Yp] + post)
cliff_ok = all(madd(mmul(GAM[a], GAM[b]), mmul(GAM[b], GAM[a])) == mscal(GQ(2 * int(a == b)), ident(8))
               for a in range(1, 7) for b in range(1, 7))


def annihilators(c):
    # a_J(e_r) = (gamma(e_r) + i gamma(J e_r))/2,  J e_r = e_{cr}
    return [mscal(GQ(Fr(1, 2)), madd(GAM[r], mscal(I_, GAM[c * r % 7]))) for r in QR]


def car_ok(A):
    for j in range(3):
        for k in range(3):
            if madd(mmul(A[j], mdag(A[k])), mmul(mdag(A[k]), A[j])) != mscal(GQ(int(j == k)), ident(8)):
                return False
            if not iszero(madd(mmul(A[j], A[k]), mmul(A[k], A[j]))):
                return False
    return True


ANN = {c: annihilators(c) for c in QNR}
CAR = {JNAME[c]: car_ok(ANN[c]) for c in QNR}
VAC = {}
vac_dim = {}
for c in QNR:
    ns = nullspace([row for A in ANN[c] for row in A], 8, GQ(0), GQ(1))
    vac_dim[JNAME[c]] = len(ns)
    VAC[c] = ns[0]


def ip(u, v):
    return sum((a.conj() * b for a, b in zip(u, v)), GQ(0))


def mv(A, v):
    return [sum((A[i][j] * v[j] for j in range(len(v))), GQ(0)) for i in range(len(A))]


def overlap2(u, v):
    x = ip(u, v)
    return x.abs2() / (ip(u, u).re * ip(v, v).re)


OVL = {"J3_J5": overlap2(VAC[3], VAC[5]), "J3_J6": overlap2(VAC[3], VAC[6]), "J5_J6": overlap2(VAC[5], VAC[6])}
# float cross-check with the Gaussian-state formula |<O_J|O_K>|^2 = sqrt|det((J+K)/2)|
formula = {f"{JNAME[a]}_{JNAME[b]}": float(np.sqrt(abs(np.linalg.det((JM[a] + JM[b]) / 2.0))))
           for a, b in [(3, 5), (3, 6), (5, 6)]}
# Fock basis of J3
A3 = ANN[3]
Ad3 = [mdag(A) for A in A3]
O3 = VAC[3]
nO3 = ip(O3, O3).re
FOCK = {"N0": [("vac", O3)],
        "N1": [(f"a{j + 1}+", mv(Ad3[j], O3)) for j in range(3)],
        "N2": [("a2+a3+", mv(Ad3[1], mv(Ad3[2], O3))), ("a3+a1+", mv(Ad3[2], mv(Ad3[0], O3))),
               ("a1+a2+", mv(Ad3[0], mv(Ad3[1], O3)))],
        "N3": [("a1+a2+a3+", mv(Ad3[0], mv(Ad3[1], mv(Ad3[2], O3))))]}
# orthonormality of the Fock basis (all have norm nO3)
allb = [v for lst in FOCK.values() for _, v in lst]
fock_orth = all(ip(allb[i], allb[j]) == (GQ(nO3) if i == j else GQ(0)) for i in range(8) for j in range(8))


def expand(v):
    nv = ip(v, v).re
    weights = {}
    coeffs = {}
    for Nk, lst in FOCK.items():
        w = Fr(0)
        for name, b in lst:
            cf = ip(b, v) / GQ(nO3)        # coefficient of the normalised... (b has norm^2 nO3)
            coeffs[name] = cf
            w += cf.abs2() * nO3
        weights[Nk] = w / nv
    return weights, coeffs


W6, C6 = expand(VAC[6])
W5, C5 = expand(VAC[5])
n2_names = ["a2+a3+", "a3+a1+", "a1+a2+"]
print("  J6 vacuum coefficients in J3 Fock basis (unnormalised):", {k: v for k, v in C6.items() if v != 0})
print("  J5 vacuum coefficients in J3 Fock basis (unnormalised):", {k: v for k, v in C5.items() if v != 0})
rel6 = C6[n2_names[0]] / C6["vac"]
rel5 = C5[n2_names[0]] / C5["vac"]
print("  coefficient(a2+a3+)/coefficient(vac): J6:", rel6, " J5:", rel5)
KEY["J6_N2_over_N0_coefficient"] = repr(rel6)
KEY["J5_N2_over_N0_coefficient"] = repr(rel5)
ratio6 = [C6[nm] / C6[n2_names[0]] if C6[n2_names[0]] != 0 else None for nm in n2_names]
ratio5 = [C5[nm] / C5[n2_names[0]] if C5[n2_names[0]] != 0 else None for nm in n2_names]
NUM = {c: [[GQ(0)] * 8 for _ in range(8)] for c in QNR}
for c in QNR:
    for A in ANN[c]:
        NUM[c] = madd(NUM[c], mmul(mdag(A), A))
comm36 = madd(mmul(NUM[3], NUM[6]), mscal(GQ(-1), mmul(NUM[6], NUM[3])))
comm35 = madd(mmul(NUM[3], NUM[5]), mscal(GQ(-1), mmul(NUM[5], NUM[3])))
comm56 = madd(mmul(NUM[5], NUM[6]), mscal(GQ(-1), mmul(NUM[6], NUM[5])))
quarter = Fr(1, 4)
g19 = cliff_ok and all(CAR.values()) and all(v == 1 for v in vac_dim.values()) and \
    all(v == quarter for v in OVL.values()) and W6 == {"N0": Fr(1, 4), "N1": 0, "N2": Fr(3, 4), "N3": 0} and \
    ratio6 is not None and all(r == GQ(1) for r in ratio6) and not iszero(comm36)


def fs(x):
    return str(x)


claim("G19", g19,
      f"Clifford relations: {cliff_ok}; CAR: {CAR}; vacuum dims: {vac_dim}; |<Om|Om'>|^2: "
      f"{ {k: fs(v) for k, v in OVL.items()} } (float formula sqrt|det((J+K)/2)|: {formula}); "
      f"J6 vacuum weights in J3 Fock space: { {k: fs(v) for k, v in W6.items()} }; N=2 coefficients in basis "
      f"(a2+a3+, a3+a1+, a1+a2+)Om3 relative to first: {ratio6}; J5 vacuum weights: { {k: fs(v) for k, v in W5.items()} }, "
      f"N=2 ratios {ratio5}; [N_J3,N_J6]=0: {iszero(comm36)}; [N_J3,N_J5]=0: {iszero(comm35)}; [N_J5,N_J6]=0: {iszero(comm56)}",
      "Fock basis (a_j^+ a_k^+ Om_J3) is orthonormal: " + str(fock_orth) +
      ". The cyclic basis (a2+a3+, a3+a1+, a1+a2+) is the epsilon/antitriplet basis; equal coefficients there = r+g+b "
      "symmetric (invariant under the colour cycle 1->2->4 i.e. z1->z2->z3).")
KEY["vacuum_overlap"] = json.dumps({k: fs(v) for k, v in OVL.items()})
KEY["j6_vacuum_weights"] = json.dumps({k: fs(v) for k, v in W6.items()})
KEY["j5_vacuum_weights"] = json.dumps({k: fs(v) for k, v in W5.items()})
KEY["j6_N2_ratios_cyclic_basis"] = str(ratio6)
KEY["j5_N2_ratios_cyclic_basis"] = str(ratio5)

# ====================================================================
#  JSON
# ====================================================================
OUT = {
    "phi": {"1": "+x", "3": "-x", "2": "+y", "6": "-y", "4": "+z", "5": "-z"},
    "fano_plus": [list(L) for L in FP],
    "fano_minus": [list(L) for L in FM],
    "link_order": link0 if link0[1] == 3 else [link0[0]] + link0[1:][::-1],
    "pairings": {JNAME[c]: [[r, c * r % 7] for r in QR] for c in QNR},
    "stabilizer": STAB,
    "corners": CORNERS,
    "fano_diagram": {"center": [k for k in PTS if PTS[k] == PTS[0]][0], "circle": list(oncircle), "vertices": [3, 5, 6],
                     "midpoint_of": {"1": [5, 6], "2": [3, 5], "4": [3, 6]}},
    "corner_view_order": cv_order,
    "hexagons": {"J6_opposite": hexes["J6_opposite"], "J3_opposite": hexes["J3_opposite"],
                 "J5_opposite": hexes["J5_opposite"]},
    "szilassi": {"edge_order": LINK_EXPECTED if same_cycle(link0, LINK_EXPECTED) else link0, "corners": sz_corners},
    "mismatch": {"rows": [list(r) for r in ROWS], "cols": [list(c) for c in COLS], "overlap": OV},
    "orbits": {"J5_orbit_size": len(orbit_J5), "J6_in_J5_orbit": JP[6] in orbit_J5, "stab_J5_size": len(stab5),
               "stab_J6_size": len(stab6)},
    "invariants": {
        "signed_automorphisms": len(AUT),
        "delta96_order_counts": ord_counts,
        "su3_commutant_dim": commutant,
        "delta96_commuting": d96_comm,
        "vacuum_overlap": {k: fs(v) for k, v in OVL.items()},
        "j6_vacuum_weights": {"N0": fs(W6["N0"]), "N2": fs(W6["N2"])},
    },
}
# midpoint check for the JSON (computed from the exact layout)
for m, (a, b) in {1: (5, 6), 2: (3, 5), 4: (3, 6)}.items():
    assert PTS[m] == mid(PTS[a], PTS[b])

with open(os.path.join(HERE, "crosscheck_geometry.json"), "w") as fh:
    json.dump(OUT, fh, indent=1)
with open(os.path.join(HERE, "crosscheck_claims.json"), "w") as fh:
    json.dump({"claims": CLAIMS, "key_values": KEY}, fh, indent=1)
print("\nSUMMARY:", {c["id"]: c["holds"] for c in CLAIMS})
print("KEY:", KEY)
