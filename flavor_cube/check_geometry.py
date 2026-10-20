"""
check_geometry.py — ground truth for the "flavor cube" page.
Needs only numpy. Run: python3 check_geometry.py
Writes geometry.json next to this file. Exits 1 if any expected value fails.

Mathematics only (exploration note, October 19, 2026). Everything is computed
with exact integers / Fractions / Gaussian integers; nothing is read from memory.

Conventions
  * Labels Z7 = {0..6}; v0 = 0 (Furey's e7 is e0 here); neighbours of 0: 1..6.
  * Fano+ lines {i, i+1, i+3} with e_i e_{i+1} = e_{i+3} (and cyclic), e_i^2 = -1,
    distinct imaginary units anticommute. Fano- lines {i, i+2, i+3}.
  * QR = {1,2,4}, QNR = {3,5,6}. For c in QNR, J_c: e_r -> e_{cr}, e_{cr} -> -e_r
    (r in QR). J3 pairs {1,3},{2,6},{4,5}; J5 {1,5},{2,3},{4,6}; J6 {1,6},{2,5},{4,3}.
  * Furey colour basis z_k = e_{r_k} + i e_{3 r_k}, r_k = 1, 2, 4.
  * a_J(v) = (gamma(v) + i gamma(J v))/2, gamma = Majoranas of Cl(6) on C^8.
  * Cube bijection phi: 1 -> +x, 3 -> -x, 2 -> +y, 6 -> -y, 4 -> +z, 5 -> -z.
    P_g n(phi(a)) = n(phi(g(a))). T_d = {D P : D diagonal +-1, det D = +1};
    T1 = corners with xyz = +1. O = signed permutation matrices with det +1.

Claims checked (one PASS/FAIL line each)
  G1  Fano+ and Fano- are Fano planes, share no line; the 14 triangles are a torus.
  G2  link of 0 is (1,3,2,6,4,5), edges alternate Fano+ / Fano-.
  G3  the table is an alternative normed algebra; L_{e0} on span(e1..e6) = J3.
  G4  the matchings fixed by x -> 2x are J3, J5, J6; partners at +60, -60, 180 deg.
  G5  link turns: 120/240 deg = 2x/4x keep the families; 60/180/300 = 3x/6x/5x swap.
  G6  G = stabiliser of 0 in Aut(Fano+), |G| = 24, affine part {1, 2x, 4x}.
  G7  {P_g} = T_d, g -> P_g an isomorphism; 2x = 120 deg turn about (1,1,1).
  G8  classification of every g (class, axis, angle, normal, cycles).
  G9  48 face bijections carry G to the T_d face action, 0 to the O face action.
  G10 the Fano plane on the cube (axes, corners, T1 = Fano+ lines off 0).
  G11 Fano diagram layout (circle, vertices, midpoints, medians).
  G12 corner view along (1,1,1), Petrie hexagon = J5 u J6, QR-corner stabiliser = S3.
  G13 any two of J3, J5, J6 make a 6-cycle with the third joining opposite points.
  G14 Szilassi hexagon dual to v0; the dual skeleton is bipartite.
  G15 orbit of J5 under G; stabilisers of J5 and J6 (reported, no expected value).
  G16 generation-mismatch overlap matrix; (1/2)*overlap is not unistochastic.
  G17 1344 signed automorphisms; the 96 fixing e0 are Delta(96) on (z1, z2, z3).
  G18 su(3) = Der(O) fixing e0; commutants with J3, J5, J6; Delta(96) commutants.
  G19 Fock vacua of J3, J5, J6: overlaps, J6 vacuum in Furey's Fock space.
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
QR = (1, 2, 4)
QNR = (3, 5, 6)
LABELS = (1, 2, 3, 4, 5, 6)
RESULTS = {}           # claim id -> dict(holds, value, notes)


def report(cid, holds, value, notes=""):
    RESULTS[cid] = {"id": cid, "holds": bool(holds), "value": value, "notes": notes}
    print(f"{cid:4s} {'PASS' if holds else 'FAIL'}  {value}")


# ---------- combinatorics on Z7 ----------
def fano_plus():
    return [tuple(sorted(((i) % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)]


def fano_minus():
    return [tuple(sorted((i % 7, (i + 2) % 7, (i + 3) % 7))) for i in range(7)]


FP = fano_plus()
FM = fano_minus()
FPS = {frozenset(L) for L in FP}
FMS = {frozenset(L) for L in FM}


def is_fano_plane(lines):
    """Every pair of the 7 points lies in exactly one line, 7 lines of size 3."""
    if len({frozenset(L) for L in lines}) != 7:
        return False
    for a, b in itertools.combinations(range(7), 2):
        if sum(1 for L in lines if a in L and b in L) != 1:
            return False
    return True


def link_cycle(v, tris):
    """Return the link of v as a list of cycles (each a list of vertices)."""
    edges = [tuple(x for x in T if x != v) for T in tris if v in T]
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    if any(len(n) != 2 for n in adj.values()):
        return None
    seen, cycles = set(), []
    for start in sorted(adj):
        if start in seen:
            continue
        cyc, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nxt = [w for w in adj[cur] if w != prev]
            nxt = min(nxt) if prev is None else nxt[0]
            if nxt == start:
                break
            cyc.append(nxt)
            seen.add(nxt)
            prev, cur = cur, nxt
        cycles.append(cyc)
    return cycles


def is_orientable(tris):
    """Try to orient all triangles coherently (each edge used once each way)."""
    tris = [tuple(T) for T in tris]
    orient = {tris[0]: tris[0]}
    stack = [tris[0]]
    while stack:
        T = stack.pop()
        o = orient[T]
        dir_edges = {(o[i], o[(i + 1) % 3]) for i in range(3)}
        for U in tris:
            if U == T or len(set(U) & set(T)) != 2:
                continue
            a, b = [x for x in o if x in U]
            # edge a-b as directed in o
            e = (a, b) if (a, b) in dir_edges else (b, a)
            c = [x for x in U if x not in e][0]
            want = (e[1], e[0], c)       # U must use the edge reversed
            if U in orient:
                ou = orient[U]
                du = {(ou[i], ou[(i + 1) % 3]) for i in range(3)}
                if (e[1], e[0]) not in du:
                    return False
            else:
                orient[U] = want
                stack.append(U)
    return len(orient) == len(tris)


def same_cycle(c1, c2):
    """Equal as cyclic sequences up to rotation and reversal."""
    n = len(c1)
    if sorted(c1) != sorted(c2):
        return False
    for seq in (list(c2), list(reversed(c2))):
        for k in range(n):
            if seq[k:] + seq[:k] == list(c1):
                return True
    return False


def matching(c):
    return [tuple(sorted((r, (c * r) % 7))) for r in QR]


def matching_set(m):
    return frozenset(frozenset(p) for p in m)


J_PAIRS = {"J3": matching(3), "J5": matching(5), "J6": matching(6)}
J_SETS = {k: matching_set(v) for k, v in J_PAIRS.items()}


def J_matrix(c):
    """6x6 integer matrix of J_c on span(e1..e6); index = label - 1."""
    M = np.zeros((6, 6), dtype=np.int64)
    for r in QR:
        s = (c * r) % 7
        M[s - 1, r - 1] = 1       # e_r -> e_{cr}
        M[r - 1, s - 1] = -1      # e_{cr} -> -e_r
    return M


JM = {"J3": J_matrix(3), "J5": J_matrix(5), "J6": J_matrix(6)}


# ---------- octonions (basis index 0 = 1, index k+1 = e_k) ----------
def oct_table():
    """T[p][q] = (sign, r): basis_p * basis_q = sign * basis_r."""
    T = [[None] * 8 for _ in range(8)]
    for p in range(8):
        T[0][p] = (1, p)
        T[p][0] = (1, p)
    for a in range(7):
        T[a + 1][a + 1] = (-1, 0)
    for i in range(7):
        x, y, z = i % 7, (i + 1) % 7, (i + 3) % 7
        for (a, b, c) in ((x, y, z), (y, z, x), (z, x, y)):
            T[a + 1][b + 1] = (1, c + 1)
            T[b + 1][a + 1] = (-1, c + 1)
    return T


OT = oct_table()


def omul(x, y):
    out = [0] * 8
    for p in range(8):
        if x[p] == 0:
            continue
        for q in range(8):
            if y[q] == 0:
                continue
            s, r = OT[p][q]
            out[r] += s * x[p] * y[q]
    return out


def basis(p):
    v = [0] * 8
    v[p] = 1
    return v


# ---------- exact rational linear algebra ----------
def rref(rows, ncols):
    M = [[Fraction(x) for x in r] for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        k = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if k is None:
            continue
        M[r], M[k] = M[k], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def nullspace(rows, ncols):
    R, piv = rref(rows, ncols) if rows else ([], [])
    free = [c for c in range(ncols) if c not in piv]
    out = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, p in enumerate(piv):
            v[p] = -R[i][f]
        out.append(v)
    return out


# ---------- Gaussian-integer matrices as (re, im) pairs of int arrays ----------
def gm(A, B):
    return (A[0] @ B[0] - A[1] @ B[1], A[0] @ B[1] + A[1] @ B[0])


def gadd(A, B):
    return (A[0] + B[0], A[1] + B[1])


def gsub(A, B):
    return (A[0] - B[0], A[1] - B[1])


def gscale(A, k):
    return (A[0] * k, A[1] * k)


def gtimes_i(A):
    return (-A[1], A[0])


def gdag(A):
    return (A[0].T.copy(), -A[1].T.copy())


def gkron(A, B):
    return (np.kron(A[0], B[0]) - np.kron(A[1], B[1]),
            np.kron(A[0], B[1]) + np.kron(A[1], B[0]))


def gtrace(A):
    return (int(np.trace(A[0])), int(np.trace(A[1])))


def gzero(A):
    return not A[0].any() and not A[1].any()


def gid(n):
    return (np.eye(n, dtype=np.int64), np.zeros((n, n), dtype=np.int64))


# ---------- cube ----------
PHI = {1: "+x", 3: "-x", 2: "+y", 6: "-y", 4: "+z", 5: "-z"}
FACE_NORMAL = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0),
               "-y": (0, -1, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}
NORMAL_FACE = {v: k for k, v in FACE_NORMAL.items()}
FACES = ["+x", "-x", "+y", "-y", "+z", "-z"]


def signed_perms():
    out = []
    for P in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3), dtype=np.int64)
            for j in range(3):
                M[P[j], j] = s[P[j]]
            out.append(M)
    return out


def det3(M):
    return int(
        M[0, 0] * (M[1, 1] * M[2, 2] - M[1, 2] * M[2, 1])
        - M[0, 1] * (M[1, 0] * M[2, 2] - M[1, 2] * M[2, 0])
        + M[0, 2] * (M[1, 0] * M[2, 1] - M[1, 1] * M[2, 0]))


def mkey(M):
    return tuple(int(x) for x in np.asarray(M).ravel())


ALL_SP = signed_perms()
# T_d: D P with det D = +1  <=>  product of the nonzero entries = +1
TD = [M for M in ALL_SP if int(np.prod(M[M != 0])) == 1]
OCT = [M for M in ALL_SP if det3(M) == 1]
T1 = {(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)}


def face_action(M):
    return tuple(NORMAL_FACE[tuple(int(x) for x in M @ np.array(FACE_NORMAL[f]))] for f in FACES)


def perm_cycles(g):
    """g: dict on labels 1..6 -> cycle string, smallest element first."""
    seen, parts = set(), []
    for a in sorted(g):
        if a in seen or g[a] == a:
            seen.add(a)
            continue
        cyc, b = [a], g[a]
        seen.add(a)
        while b != a:
            cyc.append(b)
            seen.add(b)
            b = g[b]
        parts.append("(" + " ".join(map(str, cyc)) + ")")
    return "".join(parts) if parts else "()"


def P_of(g):
    """3x3 signed permutation matrix with P n(phi(a)) = n(phi(g(a))), or None."""
    M = np.zeros((3, 3), dtype=np.int64)
    for a in (1, 2, 4):                       # phi(a) = +x, +y, +z
        j = (1, 2, 4).index(a)
        M[:, j] = FACE_NORMAL[PHI[g[a]]]
    for a in LABELS:
        if tuple(int(x) for x in M @ np.array(FACE_NORMAL[PHI[a]])) != FACE_NORMAL[PHI[g[a]]]:
            return None
    return M


def classify(M):
    """Class in T_d plus geometric data (axis/angle/normal)."""
    d, t = det3(M), int(np.trace(M))
    I = np.eye(3, dtype=np.int64)
    order = next(k for k in range(1, 7) if (np.linalg.matrix_power(M, k) == I).all())
    anti = [int(M[2, 1] - M[1, 2]), int(M[0, 2] - M[2, 0]), int(M[1, 0] - M[0, 1])]

    def canon(v):
        g = math.gcd(*[abs(x) for x in v])
        v = [x // g for x in v]
        first = next(x for x in v if x != 0)
        return [-x for x in v] if first < 0 else v

    def eigvec(lam):
        rows = (M - lam * I).tolist()
        ns = nullspace(rows, 3)
        assert len(ns) == 1
        v = ns[0]
        den = math.lcm(*[x.denominator for x in v])
        return [int(x * den) for x in v]

    if order == 1:
        return dict(cls="E", axis=None, angle=None, normal=None, order=1)
    if d == 1 and order == 3:
        g = math.gcd(*[abs(x) for x in anti])
        return dict(cls="C3", axis=[x // g for x in anti], angle=120, normal=None, order=3)
    if d == 1 and order == 2:
        return dict(cls="C2", axis=canon(eigvec(1)), angle=180, normal=None, order=2)
    if d == -1 and order == 4:
        g = math.gcd(*[abs(x) for x in anti])
        return dict(cls="S4", axis=[x // g for x in anti], angle=90, normal=None, order=4)
    if d == -1 and order == 2 and t == 1:
        return dict(cls="sigma_d", axis=None, angle=None, normal=canon(eigvec(-1)), order=2)
    return dict(cls="other", axis=None, angle=None, normal=None, order=order)


# =====================================================================
def main():
    data = {}
    all_ok = True

    def claim(cid, ok, value, notes=""):
        nonlocal all_ok
        all_ok &= bool(ok)
        report(cid, ok, value, notes)

    tris = FP + FM
    data["phi"] = {str(k): PHI[k] for k in (1, 3, 2, 6, 4, 5)}
    data["fano_plus"] = sorted([list(L) for L in FP])
    data["fano_minus"] = sorted([list(L) for L in FM])

    # ---------------- G1 ----------------
    ok_planes = is_fano_plane(FP) and is_fano_plane(FM)
    disjoint = not (FPS & FMS)
    pair_once = all(sum(1 for L in FP if {a, b} <= set(L)) == 1 and
                    sum(1 for L in FM if {a, b} <= set(L)) == 1
                    for a, b in itertools.combinations(range(7), 2))
    edges = {frozenset(e) for T in tris for e in itertools.combinations(T, 2)}
    edge_deg = {e: sum(1 for T in tris if e <= set(T)) for e in edges}
    links = {v: link_cycle(v, tris) for v in range(7)}
    links_ok = all(L is not None and len(L) == 1 and len(L[0]) == 6 for L in links.values())
    V, E, F = 7, len(edges), len(tris)
    orient = is_orientable(tris)
    ok = (ok_planes and disjoint and pair_once and E == 21 and F == 14
          and all(d == 2 for d in edge_deg.values()) and links_ok and V - E + F == 0 and orient)
    claim("G1", ok, f"Fano planes={ok_planes}, share a line={not disjoint}, V,E,F={V},{E},{F}, "
          f"chi={V - E + F}, every edge in 2 triangles={all(d == 2 for d in edge_deg.values())}, "
          f"links are single 6-cycles={links_ok}, orientable={orient}",
          "orientable with chi=0, so the surface is a torus (not a Klein bottle)")

    # ---------------- G2 ----------------
    link0 = links[0][0]
    expect_link = [1, 3, 2, 6, 4, 5]
    lk_ok = same_cycle(expect_link, link0)
    alt = []
    for k in range(6):
        a, b = expect_link[k], expect_link[(k + 1) % 6]
        fam = "+" if frozenset((0, a, b)) in FPS else ("-" if frozenset((0, a, b)) in FMS else "?")
        alt.append(f"({a},{b}){fam}")
    alt_ok = [s[-1] for s in alt] == ["+", "-"] * 3
    claim("G2", lk_ok and alt_ok, f"link(0)={link0}; " + " ".join(alt))
    data["link_order"] = expect_link

    # ---------------- G3 ----------------
    rng = np.random.default_rng(20261019)
    alt_basis = all(omul(basis(p), omul(basis(p), basis(q))) == omul(omul(basis(p), basis(p)), basis(q))
                    and omul(omul(basis(q), basis(p)), basis(p)) == omul(basis(q), omul(basis(p), basis(p)))
                    for p in range(8) for q in range(8))
    n_rand, alt_rand, norm_rand, flex_rand = 300, True, True, True
    for _ in range(n_rand):
        x = [int(t) for t in rng.integers(-6, 7, size=8)]
        y = [int(t) for t in rng.integers(-6, 7, size=8)]
        xy = omul(x, y)
        alt_rand &= omul(x, xy) == omul(omul(x, x), y)
        alt_rand &= omul(omul(y, x), x) == omul(y, omul(x, x))
        flex_rand &= omul(omul(x, y), x) == omul(x, omul(y, x))
        norm_rand &= sum(t * t for t in xy) == sum(t * t for t in x) * sum(t * t for t in y)
    e = lambda k: basis(k + 1)
    nonassoc = omul(omul(e(1), e(2)), e(3)) != omul(e(1), omul(e(2), e(3)))
    L0 = np.zeros((6, 6), dtype=np.int64)
    leak = False
    for j in LABELS:
        v = omul(e(0), e(j))
        leak |= v[0] != 0 or v[1] != 0
        for i in LABELS:
            L0[i - 1, j - 1] = v[i + 1]
    lj3 = (not leak) and (L0 == JM["J3"]).all()
    claim("G3", alt_basis and alt_rand and norm_rand and lj3,
          f"alternative on basis={alt_basis}; on {n_rand} random integer pairs: alternative={alt_rand}, "
          f"flexible={flex_rand}, |xy|^2=|x|^2|y|^2 exactly={norm_rand}; non-associative={nonassoc}; "
          f"L_e0|span(e1..e6) == J3: {lj3}")

    # ---------------- G4 ----------------
    pts = list(LABELS)

    def all_matchings(p):
        if not p:
            return [[]]
        a, out = p[0], []
        for b in p[1:]:
            rest = [x for x in p if x not in (a, b)]
            for m in all_matchings(rest):
                out.append([(a, b)] + m)
        return out

    MATCH = [matching_set(m) for m in all_matchings(pts)]
    dbl = {a: (2 * a) % 7 for a in LABELS}
    inv = [m for m in MATCH if matching_set([(dbl[a], dbl[b]) for a, b in (tuple(p) for p in m)]) == m]
    inv_names = sorted(k for k, s in J_SETS.items() if s in inv)
    pos = {a: 60 * k for k, a in enumerate(expect_link)}

    def rel_angle(a, b):
        d = (pos[b] - pos[a]) % 360
        return d - 360 if d > 180 else d

    offs = {}
    for name, c in (("J3", 3), ("J5", 5), ("J6", 6)):
        offs[name] = sorted({rel_angle(r, (c * r) % 7) for r in QR})     # in (-180, 180]
    ok = (len(MATCH) == 15 and len(inv) == 3 and inv_names == ["J3", "J5", "J6"]
          and offs == {"J3": [60], "J5": [-60], "J6": [180]})
    claim("G4", ok, f"{len(MATCH)} matchings, {len(inv)} invariant under 2x: {inv_names}; "
          f"partner offsets of e_r (r in QR): {offs}")
    data["pairings"] = {"J3": [[1, 3], [2, 6], [4, 5]], "J5": [[1, 5], [2, 3], [4, 6]],
                        "J6": [[1, 6], [2, 5], [4, 3]]}
    assert all(matching_set(data["pairings"][k]) == J_SETS[k] for k in J_SETS)

    # ---------------- G5 ----------------
    turns = {}
    for k in range(1, 6):
        rot = {expect_link[i]: expect_link[(i + k) % 6] for i in range(6)}
        mult = [a for a in range(1, 7) if all((a * x) % 7 == rot[x] for x in LABELS)]
        turns[60 * k] = mult[0] if mult else None

    def fam_action(a):
        img = lambda L: frozenset((a * x) % 7 for x in L)
        if all(img(L) in FPS for L in FP) and all(img(L) in FMS for L in FM):
            return "keep"
        if all(img(L) in FMS for L in FP) and all(img(L) in FPS for L in FM):
            return "swap"
        return "neither"

    acts = {a: fam_action(a) for a in range(1, 7)}
    ok = (turns == {60: 3, 120: 2, 180: 6, 240: 4, 300: 5}
          and acts[2] == acts[4] == "keep" and acts[3] == acts[5] == acts[6] == "swap")
    claim("G5", ok, f"turn(deg)->x*a: {turns}; family action of x->ax: {acts}",
          "orientation: link (1,3,2,6,4,5) placed at 0,60,...,300 deg, turn = advance positions")

    # ---------------- G6 ----------------
    G = []
    for p in itertools.permutations(LABELS):
        g = {0: 0, **dict(zip(LABELS, p))}
        if all(frozenset(g[x] for x in L) in FPS for L in FP):
            G.append(g)
    mults_in = sorted(a for a in range(1, 7) if {0: 0, **{x: (a * x) % 7 for x in LABELS}} in G)
    affine = []
    for g in G:
        for a in range(1, 7):
            for b in range(7):
                if all(g[x] == (a * x + b) % 7 for x in range(7)):
                    affine.append((a, b))
    ok = len(G) == 24 and mults_in == [1, 2, 4] and sorted(affine) == [(1, 0), (2, 0), (4, 0)]
    claim("G6", ok, f"|G|={len(G)}; x->ax in G for a in {mults_in}; affine elements (a,b)={sorted(affine)}")

    # ---------------- G7 ----------------
    Pg = [P_of(g) for g in G]
    exists = all(P is not None for P in Pg)
    td_keys = {mkey(M) for M in TD}
    pg_keys = [mkey(P) for P in Pg]
    equal_td = exists and len(set(pg_keys)) == 24 and set(pg_keys) == td_keys
    compose = lambda g, h: {x: g[h[x]] for x in range(7)}
    hom = all((P_of(compose(g, h)) == P_of(g) @ P_of(h)).all() for g in G for h in G)
    g2 = {0: 0, **{x: (2 * x) % 7 for x in LABELS}}
    P2 = P_of(g2)
    c2 = classify(P2)
    turn_ok = (c2["cls"] == "C3" and c2["axis"] == [1, 1, 1]
               and [NORMAL_FACE[tuple(int(t) for t in P2 @ np.array(FACE_NORMAL[f]))] for f in ("+x", "+y", "+z")]
               == ["+y", "+z", "+x"])
    claim("G7", equal_td and hom and turn_ok,
          f"P_g exists for all={exists}; {{P_g}} == T_d (24 distinct)={equal_td}; homomorphism={hom}; "
          f"P(2x): +x->+y->+z, {c2['angle']} deg about {c2['axis']}={turn_ok}")

    # ---------------- G8 ----------------
    stab = []
    counts = {}
    for g, P in zip(G, Pg):
        c = classify(P)
        counts[c["cls"]] = counts.get(c["cls"], 0) + 1
        torus = None
        for a, name in ((1, "id"), (2, "x->2x"), (4, "x->4x")):
            if all(g[x] == (a * x) % 7 for x in LABELS):
                torus = name
        stab.append({
            "perm": [g[a] for a in LABELS],
            "cycles": perm_cycles({a: g[a] for a in LABELS}),
            "matrix": [[int(t) for t in row] for row in P],
            "det": det3(P),
            "class": c["cls"],
            "axis": c["axis"],
            "angle_deg": c["angle"],
            "normal": c["normal"],
            "torus": torus,
            "fixes_QR_corner": tuple(int(t) for t in P @ np.array([1, 1, 1])) == (1, 1, 1),
        })
    order_cls = {"E": 0, "C3": 1, "C2": 2, "S4": 3, "sigma_d": 4, "other": 5}
    stab.sort(key=lambda s: (order_cls[s["class"]], s["perm"]))
    rot90 = [M for M in OCT if classify(M)["order"] == 4]
    no90 = all(mkey(M) not in set(pg_keys) for M in rot90)
    noinv = mkey(-np.eye(3, dtype=np.int64)) not in set(pg_keys)
    ok = counts == {"E": 1, "C3": 8, "C2": 3, "S4": 6, "sigma_d": 6} and no90 and noinv and len(rot90) == 6
    claim("G8", ok, f"class sizes {counts}; 90-deg rotations ({len(rot90)}) absent={no90}; -I absent={noinv}",
          "per-element table written to geometry.json['stabilizer']")
    data["stabilizer"] = stab

    # ---------------- G9 ----------------
    td_faces = {face_action(M) for M in TD}
    o_faces = {face_action(M) for M in OCT}
    good_td, good_o = [], 0
    for img in itertools.permutations(FACES):
        psi = dict(zip(LABELS, img))
        psi_inv = {v: k for k, v in psi.items()}
        conj = {tuple(psi[g[psi_inv[f]]] for f in FACES) for g in G}
        if conj == td_faces:
            good_td.append(psi)
        if conj == o_faces:
            good_o += 1

    def opposite(f1, f2):
        return FACE_NORMAL[f1] == tuple(-t for t in FACE_NORMAL[f2])

    j3_opp = all(opposite(psi[a], psi[b]) for psi in good_td for a, b in J_PAIRS["J3"])
    j56_adj = all(not opposite(psi[a], psi[b]) and psi[a] != psi[b]
                  for psi in good_td for k in ("J5", "J6") for a, b in J_PAIRS[k])
    qr_corner, n_t1, n_t2 = True, 0, 0
    for psi in good_td:
        fs = [psi[r] for r in QR]
        axes = {f[1] for f in fs}
        qr_corner &= len(axes) == 3
        corner = [0, 0, 0]
        for f in fs:
            corner["xyz".index(f[1])] = 1 if f[0] == "+" else -1
        if tuple(corner) in T1:
            n_t1 += 1
        else:
            n_t2 += 1
    ok = len(good_td) == 48 and good_o == 0 and j3_opp and j56_adj and qr_corner and n_t1 == n_t2 == 24
    claim("G9", ok, f"bijections giving T_d action={len(good_td)}, O action={good_o}; J3 opposite={j3_opp}; "
          f"J5,J6 adjacent={j56_adj}; QR a corner={qr_corner}; QR on T1/T2={n_t1}/{n_t2}")

    # ---------------- G10 ----------------
    axis_of = lambda f: f[1]
    through0 = [L for L in FP if 0 in L]
    axes_ok = sorted(axis_of(PHI[a]) + axis_of(PHI[b]) for _, a, b in through0) == ["xx", "yy", "zz"]
    corners = []
    sgn = lambda s: "+" if s > 0 else "-"
    for s in itertools.product((1, -1), repeat=3):
        faces = sorted(a for a in LABELS if PHI[a] in {sgn(s[0]) + "x", sgn(s[1]) + "y", sgn(s[2]) + "z"})
        corners.append({"signs": list(s), "faces": faces, "tetra": "T1" if s in T1 else "T2",
                        "fano_plus_line": frozenset(faces) in FPS,
                        "fano_minus_line": frozenset(faces) in FMS})
    t1_lines = {frozenset(c["faces"]) for c in corners if c["tetra"] == "T1"}
    off0 = {frozenset(L) for L in FP if 0 not in L}
    t1_ok = t1_lines == off0 and all(c["fano_plus_line"] for c in corners if c["tetra"] == "T1")
    t2 = {tuple(c["signs"]): (c["faces"], c["fano_plus_line"], c["fano_minus_line"])
          for c in corners if c["tetra"] == "T2"}
    t2_ok = (t2[(-1, -1, -1)] == ([3, 5, 6], False, True)
             and all(not fp and not fm for k, (f, fp, fm) in t2.items() if k != (-1, -1, -1)))
    t1_named = {tuple(c["signs"]): c["faces"] for c in corners if c["tetra"] == "T1"}
    named_ok = t1_named == {(1, 1, 1): [1, 2, 4], (1, -1, -1): [1, 5, 6],
                            (-1, 1, -1): [2, 3, 5], (-1, -1, 1): [3, 4, 6]}
    fm0 = [tuple(x for x in L if x) for L in FM if 0 in L]
    fm0_ok = matching_set(fm0) == J_SETS["J5"] and all(not opposite(PHI[a], PHI[b]) for a, b in fm0)
    opp_counts = {}
    for L in FM:
        if 0 in L:
            continue
        opp_counts[L] = sum(1 for a, b in itertools.combinations(L, 2) if opposite(PHI[a], PHI[b]))
    opp_ok = all((v == 0) if L == (3, 5, 6) else (v == 1) for L, v in opp_counts.items())
    off0_list = sorted(tuple(sorted(L)) for L in off0)
    images = {tuple(off0_list.index(tuple(sorted(g[x] for x in L))) for L in off0_list) for g in G}
    s4_ok = len(images) == 24
    ok = axes_ok and t1_ok and named_ok and t2_ok and fm0_ok and opp_ok and s4_ok
    claim("G10", ok, f"Fano+ through 0 = axes {axes_ok}; T1 = Fano+ lines off 0 {t1_ok and named_ok}; "
          f"T2: {dict((str(k), v[0]) for k, v in t2.items())}, (-,-,-) Fano- only, others neither={t2_ok}; "
          f"Fano- through 0 = J5 adjacent={fm0_ok}; opposite pairs in other Fano- lines {opp_counts}; "
          f"G on 4 lines = S4 ({len(images)} perms)")
    data["corners"] = corners

    # ---------------- G11 ----------------
    diag = {"center": 0, "circle": [1, 2, 4], "vertices": [3, 5, 6],
            "midpoint_of": {"1": [5, 6], "2": [3, 5], "4": [3, 6]}}
    sides = [frozenset([m] + v) for m, v in ((1, [5, 6]), (2, [3, 5]), (4, [3, 6]))]
    opp_vertex = {1: 3, 2: 6, 4: 5}                     # vertex opposite the side with midpoint m
    medians = [frozenset((opp_vertex[m], 0, m)) for m in (1, 2, 4)]
    seven = sides + medians + [frozenset((1, 2, 4))]
    ok = (set(seven) == FPS and len(set(seven)) == 7
          and set(medians) == {frozenset((3, 0, 1)), frozenset((6, 0, 2)), frozenset((5, 0, 4))})
    claim("G11", ok, "sides {1,5,6},{2,3,5},{3,4,6}; medians {0,1,3},{0,2,6},{0,4,5}; circle {1,2,4}: "
          f"exactly the Fano+ lines={set(seven) == FPS}")
    data["fano_diagram"] = diag

    # ---------------- G12 ----------------
    n111 = np.array([1, 1, 1])

    def proj(v):
        v = [Fraction(int(t)) for t in v]
        s = sum(v) / 3
        return [t - s for t in v]

    dot = lambda a, b: sum(x * y for x, y in zip(a, b))
    pp = {f: proj(FACE_NORMAL[f]) for f in FACES}
    cos_ok = all(dot(pp[a], pp[b]) / dot(pp[a], pp[a]) == Fraction(-1, 2)
                 for a, b in (("+x", "+y"), ("+y", "+z"), ("+z", "+x")))
    neg_ok = all(pp["-" + ax] == [-t for t in pp["+" + ax]] for ax in "xyz")
    u, w = np.array([1, -1, 0]), np.array([1, 1, -2])      # u x w = 2(1,1,1): counterclockwise seen from (1,1,1)
    ang = {f: math.atan2(int(np.array(FACE_NORMAL[f]) @ w), int(np.array(FACE_NORMAL[f]) @ u)) for f in FACES}
    start = ang["+x"]
    view = sorted(FACES, key=lambda f: (ang[f] - start) % (2 * math.pi))
    view_labels = [next(a for a in LABELS if PHI[a] == f) for f in view]
    order_ok = view == ["+x", "-z", "+y", "-x", "+z", "-y"] and view_labels == [1, 5, 2, 3, 4, 6]
    # Petrie hexagon: cube edges = pairs of adjacent faces; edge {(i,s),(j,t)} touches (+,+,+) iff s=t=+
    cube_edges = [frozenset((a, b)) for a, b in itertools.combinations(LABELS, 2)
                  if not opposite(PHI[a], PHI[b])]
    petrie = [e for e in cube_edges if len({PHI[a][0] for a in e}) == 2]
    petrie_ok = len(cube_edges) == 12 and set(petrie) == (J_SETS["J5"] | J_SETS["J6"])

    def corner_pts(edge):
        a, b = sorted(edge)
        fa, fb = PHI[a], PHI[b]
        free = ({"x", "y", "z"} - {fa[1], fb[1]}).pop()
        out = []
        for s in (1, -1):
            c = {fa[1]: 1 if fa[0] == "+" else -1, fb[1]: 1 if fb[0] == "+" else -1, free: s}
            out.append((c["x"], c["y"], c["z"]))
        return out

    # walk the hexagon of corners
    adjc = {}
    for e_ in petrie:
        p, q = corner_pts(e_)
        adjc.setdefault(p, []).append((q, e_))
        adjc.setdefault(q, []).append((p, e_))
    cur = (1, 1, -1)
    prev_e, edge_seq = None, []
    for _ in range(6):
        nxt, e_ = [(q, ed) for q, ed in adjc[cur] if ed != prev_e][0]
        edge_seq.append(e_)
        prev_e, cur = e_, nxt
    closed = cur == (1, 1, -1)
    kinds = ["J5" if e_ in J_SETS["J5"] else "J6" for e_ in edge_seq]
    alt_ok = closed and all(kinds[k] != kinds[(k + 1) % 6] for k in range(6))
    face_seq = [list(edge_seq[k] & edge_seq[(k + 1) % 6])[0] for k in range(6)]
    face_hex_ok = same_cycle(view_labels, face_seq)
    opp_j3 = all(frozenset((view_labels[k], view_labels[k + 3])) in J_SETS["J3"] for k in range(3))
    fixers = [s for s in stab if s["fixes_QR_corner"]]
    fix_cls = sorted(s["class"] for s in fixers)
    weyl = {tuple(dict(zip(LABELS, s["perm"]))[r] for r in QR) for s in fixers}
    weyl_ok = (fix_cls == ["C3", "C3", "E", "sigma_d", "sigma_d", "sigma_d"]
               and weyl == set(itertools.permutations(QR)))
    ok = cos_ok and neg_ok and order_ok and petrie_ok and alt_ok and face_hex_ok and opp_j3 and weyl_ok
    claim("G12", ok, f"+x,+y,+z at 120 deg={cos_ok}, minus faces opposite={neg_ok}; order (ccw seen from (1,1,1)) "
          f"{view} = {view_labels}; Petrie edges = J5 u J6={petrie_ok}; around hexagon {kinds}; "
          f"face hexagon {face_seq} same cycle={face_hex_ok}; opposite = J3={opp_j3}; "
          f"QR-corner stabiliser {fix_cls} acting as S3 on {{1,2,4}}={weyl_ok}",
          "'opposite points' = opposite face labels in the face hexagon; the Petrie edges are its sides")
    data["corner_view_order"] = view_labels

    # ---------------- G13 ----------------
    def union_cycle(first, second):
        a, b = J_PAIRS[first], J_PAIRS[second]
        partner = lambda m, x: next(q for p in m for q in p if x in p and q != x)
        seq, cur, use_first = [1], 1, True
        for _ in range(5):
            cur = partner(a if use_first else b, cur)
            seq.append(cur)
            use_first = not use_first
        closes = partner(b, cur) == 1
        return seq if closes else None

    hexes = {"J6_opposite": union_cycle("J3", "J5"), "J3_opposite": union_cycle("J5", "J6"),
             "J5_opposite": union_cycle("J3", "J6")}
    opp_ok = all(h is not None and all(frozenset((h[k], h[k + 3])) in J_SETS[name.split("_")[0]] for k in range(3))
                 for name, h in hexes.items())
    ok = (opp_ok and same_cycle(hexes["J6_opposite"], expect_link)
          and same_cycle(hexes["J3_opposite"], [1, 5, 2, 3, 4, 6]))
    claim("G13", ok, f"single 6-cycles with the third pairing opposite={opp_ok}: {hexes}",
          "cycles start at 1 and step first along the lower-numbered J")
    data["hexagons"] = hexes

    # ---------------- G14 ----------------
    sz_corners = []
    for k in range(6):
        a, b = expect_link[k], expect_link[(k + 1) % 6]
        T = frozenset((0, a, b))
        sz_corners.append({"triangle": [0, a, b], "type": "up" if T in FPS else ("down" if T in FMS else "?")})
    types_ok = [c["type"] for c in sz_corners] == ["up", "down"] * 3
    up_pairs = matching_set([tuple(c["triangle"][1:]) for c in sz_corners if c["type"] == "up"])
    dn_pairs = matching_set([tuple(c["triangle"][1:]) for c in sz_corners if c["type"] == "down"])
    opp_edges = matching_set([(expect_link[k], expect_link[k + 3]) for k in range(3)])
    bip = all(sum(1 for T in FP if e_ <= set(T)) == 1 and sum(1 for T in FM if e_ <= set(T)) == 1 for e_ in edges)
    ok = (types_ok and up_pairs == J_SETS["J3"] and dn_pairs == J_SETS["J5"]
          and opp_edges == J_SETS["J6"] and bip)
    claim("G14", ok, f"corners {[(tuple(c['triangle']), c['type']) for c in sz_corners]}; up=J3 "
          f"{up_pairs == J_SETS['J3']}, down=J5 {dn_pairs == J_SETS['J5']}, opposite edges=J6 "
          f"{opp_edges == J_SETS['J6']}; every edge in one up + one down={bip}")
    data["szilassi"] = {"edge_order": expect_link, "corners": sz_corners}

    # ---------------- G15 ----------------
    act = lambda g, m: frozenset(frozenset(g[x] for x in p) for p in m)
    orbit5 = {act(g, J_SETS["J5"]) for g in G}
    j3_inv = all(act(g, J_SETS["J3"]) == J_SETS["J3"] for g in G)
    stab5 = [g for g in G if act(g, J_SETS["J5"]) == J_SETS["J5"]]
    stab6 = [g for g in G if act(g, J_SETS["J6"]) == J_SETS["J6"]]
    all_adj = [m for m in MATCH if all(not opposite(PHI[a], PHI[b]) for a, b in (tuple(p) for p in m))]
    stab5_names = sorted(perm_cycles({a: g[a] for a in LABELS}) for g in stab5)
    stab6_names = sorted(perm_cycles({a: g[a] for a in LABELS}) for g in stab6)
    claim("G15", j3_inv, f"J3 G-invariant={j3_inv}; |orbit(J5)|={len(orbit5)}, J6 in it={J_SETS['J6'] in orbit5}, "
          f"orbit = all {len(all_adj)} matchings into adjacent-face pairs={orbit5 == set(all_adj)}; "
          f"Stab(J5)={stab5_names}, Stab(J6)={stab6_names}",
          "no expected value beyond J3 invariance; stabilisers are {id, 2x, 4x} = C3 about (1,1,1)")
    data["orbits"] = {"J5_orbit_size": len(orbit5), "J6_in_J5_orbit": J_SETS["J6"] in orbit5,
                      "stab_J5_size": len(stab5), "stab_J6_size": len(stab6)}

    # ---------------- G16 ----------------
    rows = [(1, 3), (4, 5), (2, 6)]
    cols = [(2, 3), (4, 6), (1, 5)]
    ov = [[len(set(r) & set(c)) for c in cols] for r in rows]
    two_ones = all(sorted(r) == [0, 1, 1] for r in ov) and all(sorted(ov[i][j] for i in range(3)) == [0, 1, 1]
                                                               for j in range(3))
    B = [[Fraction(x, 2) for x in r] for r in ov]
    ds = all(sum(r) == 1 for r in B) and all(sum(B[i][j] for i in range(3)) == 1 for j in range(3))
    # unitary U with |U_ij|^2 = B_ij: rows i,k have <U_i,U_k> = sum over shared nonzero columns
    shared = [sum(1 for j in range(3) if B[i][j] and B[k][j]) for i, k in itertools.combinations(range(3), 2)]
    not_uni = all(s == 1 for s in shared)      # one term of modulus sqrt(1/2*1/2)=1/2, cannot vanish
    ok = two_ones and ds and not_uni
    claim("G16", ok, f"overlap {ov}; two 1s per row/col={two_ones}; B=overlap/2 doubly stochastic={ds}; "
          f"shared nonzero columns per row pair={shared} -> not unistochastic",
          "any two rows of U share exactly one nonzero column, so <U_i,U_k> is a single term of modulus 1/2 != 0")
    data["mismatch"] = {"rows": [list(r) for r in rows], "cols": [list(c) for c in cols], "overlap": ov}

    # ---------------- G17 ----------------
    imag = [[OT[a + 1][b + 1] for b in range(7)] for a in range(7)]
    collin = []
    for p in itertools.permutations(range(7)):
        if all(frozenset(p[x] for x in L) in FPS for L in FP):
            collin.append(p)
    autos = []
    per_coll = []
    for p in collin:
        cnt = 0
        for s in itertools.product((1, -1), repeat=7):
            good = True
            for a in range(7):
                for b in range(7):
                    if a == b:
                        continue
                    sg, c = imag[a][b]
                    sg2, c2_ = imag[p[a]][p[b]]
                    # phi(e_a)phi(e_b) = s_a s_b sg2 e_{c2}; phi(e_a e_b) = sg s_{c} e_{p[c]}
                    if c2_ - 1 != p[c - 1] or s[a] * s[b] * sg2 != sg * s[c - 1]:
                        good = False
                        break
                if not good:
                    break
            if good:
                autos.append((p, s))
                cnt += 1
        per_coll.append(cnt)
    fix0 = [(p, s) for p, s in autos if p[0] == 0]
    plus = [(p, s) for p, s in fix0 if s[0] == 1]
    minus = [(p, s) for p, s in fix0 if s[0] == -1]

    def six(p, s):
        M = np.zeros((6, 6), dtype=np.int64)
        for i in LABELS:
            M[p[i] - 1, i - 1] = s[i]
        return M

    def to3(M, anti=False):
        """3x3 Gaussian matrix A with M z_k = sum_j A_jk z_j (or conj(z_j) if anti); None if not."""
        A = [[None] * 3 for _ in range(3)]
        sgn_im = -1 if anti else 1
        for k, rk in enumerate(QR):
            for j, rj in enumerate(QR):
                re_, im_ = int(M[rj - 1, rk - 1]), int(M[rj - 1, (3 * rk) % 7 - 1])     # coeff of e_{r_j}
                re2, im2 = int(M[(3 * rj) % 7 - 1, rk - 1]), int(M[(3 * rj) % 7 - 1, (3 * rk) % 7 - 1])
                # target vector z_j = e_rj + i e_3rj (or conj): coeff of e_3rj must be (+-i)*coeff of e_rj
                if (re2, im2) != (-sgn_im * im_, sgn_im * re_):
                    return None
                A[j][k] = (re_, im_)
        return A

    def gmul_s(x, y):
        return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def gdet3(A):
        t = (0, 0)
        for perm in itertools.permutations(range(3)):
            sgn_ = 1 if sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j]) % 2 == 0 else -1
            pr = (1, 0)
            for i in range(3):
                pr = gmul_s(pr, A[i][perm[i]])
            t = (t[0] + sgn_ * pr[0], t[1] + sgn_ * pr[1])
        return t

    J3m = JM["J3"]
    lin = [to3(six(p, s)) for p, s in plus]
    lin_ok = all(A is not None for A in lin) and all((six(p, s) @ J3m == J3m @ six(p, s)).all() for p, s in plus)
    mono = all(sum(1 for x in row if x != (0, 0)) == 1 for A in lin for row in A) and all(
        x in {(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)} for A in lin for row in A for x in row)
    dets = {gdet3(A) for A in lin}
    lin_keys = {tuple(x for row in A for x in row) for A in lin}
    # Delta(96) = all det-1 monomial 3x3 matrices with entries in {+-1, +-i}
    mu4 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    d96 = set()
    for perm in itertools.permutations(range(3)):
        for ent in itertools.product(mu4, repeat=3):
            A = [[(0, 0)] * 3 for _ in range(3)]
            for k in range(3):
                A[perm[k]][k] = ent[k]
            if gdet3(A) == (1, 0):
                d96.add(tuple(x for row in A for x in row))
    is_d96 = lin_keys == d96 and len(d96) == 96
    I6 = np.eye(6, dtype=np.int64)

    def order6(M):
        P_, k = M.copy(), 1
        while not (P_ == I6).all():
            P_, k = P_ @ M, k + 1
        return k

    ocount = {}
    for p, s in plus:
        o = order6(six(p, s))
        ocount[o] = ocount.get(o, 0) + 1
    ocount = dict(sorted(ocount.items()))
    anti_ok = all((six(p, s) @ J3m == -J3m @ six(p, s)).all() and to3(six(p, s), anti=True) is not None
                  for p, s in minus)
    ok = (len(collin) == 168 and len(autos) == 1344 and set(per_coll) == {8} and len(fix0) == 192
          and len(plus) == 96 and len(minus) == 96 and lin_ok and mono and dets == {(1, 0)} and is_d96
          and ocount == {1: 1, 2: 15, 3: 32, 4: 24, 8: 24} and anti_ok)
    claim("G17", ok, f"collineations={len(collin)}, signed automorphisms={len(autos)} ({sorted(set(per_coll))} per "
          f"collineation); fixing e0 up to sign={len(fix0)} (+e0: {len(plus)}, -e0: {len(minus)}); "
          f"+e0 ones C-linear monomial in {{+-1,+-i}}={lin_ok and mono}, det={sorted(dets)}, "
          f"= all det-1 mu4-monomials (Delta(96))={is_d96}; orders {ocount}; -e0 ones antilinear={anti_ok}")

    # ---------------- G18 ----------------
    # derivations: unknown D (8x8), D[r][p] = coefficient of basis r in D(basis p)
    eqs = []
    for p in range(8):
        for q in range(8):
            sg, t = OT[p][q]
            for r in range(8):
                row = [0] * 64
                row[r * 8 + t] += sg                      # D(b_p b_q)_r
                for s_ in range(8):                       # - (D b_p) b_q - b_p (D b_q)
                    s1, t1 = OT[s_][q]
                    if t1 == r:
                        row[s_ * 8 + p] -= s1
                    s2, t2 = OT[p][s_]
                    if t2 == r:
                        row[s_ * 8 + q] -= s2
                if any(row):
                    eqs.append(row)
    der = nullspace(eqs, 64)
    fix_e0 = eqs + [[1 if k == r * 8 + 1 else 0 for k in range(64)] for r in range(8)]
    su3 = nullspace(fix_e0, 64)
    su3_6 = [[[v[(i + 1) * 8 + (j + 1)] for j in LABELS] for i in LABELS] for v in su3]
    closed_span = all(v[r * 8 + c] == 0 for v in su3 for r in (0, 1) for c in range(8))

    def mat_mul(A, Bm):
        return [[sum(A[i][k] * Bm[k][j] for k in range(6)) for j in range(6)] for i in range(6)]

    def commutant(Jm):
        Jl = [[int(x) for x in row] for row in Jm]
        coms = [[[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(mat_mul(Bk, Jl), mat_mul(Jl, Bk))]
                for Bk in su3_6]
        rows_ = [[coms[k][i][j] for k in range(8)] for i in range(6) for j in range(6)]
        ns = nullspace(rows_, 8)
        mats = [[[sum(t[k] * su3_6[k][i][j] for k in range(8)) for j in range(6)] for i in range(6)] for t in ns]
        return mats

    comm = {k: commutant(JM[k]) for k in ("J3", "J5", "J6")}
    dims = {k: len(v) for k, v in comm.items()}

    def common_kernel(mats):
        rows_ = [row for M_ in mats for row in M_]
        ns = nullspace(rows_, 6)
        out = []
        for v in ns:
            den = math.lcm(*[x.denominator for x in v])
            out.append([int(x * den) for x in v])
        return out

    kerJ6 = common_kernel(comm["J6"])
    kerJ5 = common_kernel(comm["J5"])
    v124 = [1, 1, 0, 1, 0, 0]
    j6_ann = all(sum(M_[i][j] * v124[j] for j in range(6)) == 0 for M_ in comm["J6"] for i in range(6))
    d96_comm = {k: sum(1 for p, s in plus if (six(p, s) @ JM[k] == JM[k] @ six(p, s)).all())
                for k in ("J3", "J5", "J6")}
    d96_comm_els = {k: sorted(perm_cycles({a: p[a] for a in LABELS}) + (" signs+" if all(x == 1 for x in s) else
                                                                         " signs" + str(s))
                              for p, s in plus if (six(p, s) @ JM[k] == JM[k] @ six(p, s)).all())
                    for k in ("J5", "J6")}
    j5_ann = all(sum(M_[i][j] * v124[j] for j in range(6)) == 0 for M_ in comm["J5"] for i in range(6))
    flat = lambda mats: [[x for row in M_ for x in row] for M_ in mats]
    span_rank = lambda mats: len(rref(flat(mats), 36)[1])
    same_sub = span_rank(comm["J5"]) == span_rank(comm["J6"]) == span_rank(comm["J5"] + comm["J6"]) == 3
    # the su(3) stabiliser of the J3-complex vector e1+e2+e4 (i.e. z-coordinates (1,1,1))
    stab_rows = [[sum(su3_6[k][i][j] * v124[j] for j in range(6)) for k in range(8)] for i in range(6)]
    stab_dim = len(nullspace(stab_rows, 8))
    ok = (len(der) == 14 and len(su3) == 8 and closed_span and dims == {"J3": 8, "J5": 3, "J6": 3}
          and j6_ann and d96_comm == {"J3": 96, "J5": 3, "J6": 3})
    claim("G18", ok, f"dim Der(O)={len(der)}, fixing e0={len(su3)}; commutant dims {dims}; J6 commutant kills "
          f"e1+e2+e4={j6_ann} (common kernel {kerJ6}); J5 commutant kills it too={j5_ann} (kernel {kerJ5}); "
          f"J5 and J6 commutants are the same subalgebra={same_sub} = stabiliser of e1+e2+e4 in su(3) "
          f"(dim {stab_dim}); Delta(96) commuting {d96_comm}: {d96_comm_els}",
          "the J5 and J6 commutants coincide: both are the su(2) fixing the colour vector r+g+b")

    # ---------------- G19 ----------------
    s0 = (np.eye(2, dtype=np.int64), np.zeros((2, 2), dtype=np.int64))
    sx = (np.array([[0, 1], [1, 0]]), np.zeros((2, 2), dtype=np.int64))
    sy = (np.zeros((2, 2), dtype=np.int64), np.array([[0, -1], [1, 0]]))
    sz = (np.array([[1, 0], [0, -1]]), np.zeros((2, 2), dtype=np.int64))
    k3 = lambda a, b, c: gkron(gkron(a, b), c)
    GAM = {1: k3(sx, s0, s0), 2: k3(sy, s0, s0), 3: k3(sz, sx, s0),
           4: k3(sz, sy, s0), 5: k3(sz, sz, sx), 6: k3(sz, sz, sy)}
    I8 = gid(8)
    cliff = all(gzero(gsub(gadd(gm(GAM[a], GAM[b]), gm(GAM[b], GAM[a])), gscale(I8, 2 if a == b else 0)))
                for a in LABELS for b in LABELS)
    herm = all(gzero(gsub(GAM[a], gdag(GAM[a]))) for a in LABELS)

    def gamma_vec(v):
        out = (np.zeros((8, 8), dtype=np.int64), np.zeros((8, 8), dtype=np.int64))
        for k in LABELS:
            if v[k - 1]:
                out = gadd(out, gscale(GAM[k], int(v[k - 1])))
        return out

    def ann2(name):
        """Return [2 a_J(e_r) for r in QR] (Gaussian-integer 8x8)."""
        out = []
        for r in QR:
            er = np.zeros(6, dtype=np.int64)
            er[r - 1] = 1
            out.append(gadd(gamma_vec(er), gtimes_i(gamma_vec(JM[name] @ er))))
        return out

    A = {k: ann2(k) for k in ("J3", "J5", "J6")}
    car = True
    for k, ops in A.items():
        for i in range(3):
            for j in range(3):
                car &= gzero(gadd(gm(ops[i], ops[j]), gm(ops[j], ops[i])))
                car &= gzero(gsub(gadd(gm(ops[i], gdag(ops[j])), gm(gdag(ops[j]), ops[i])),
                                  gscale(I8, 4 if i == j else 0)))
    # Q_J = prod_k (2a_k)(2a_k)^dag = 64 P_J, P_J the vacuum projector
    Q = {}
    for k, ops in A.items():
        q = I8
        for o in ops:
            q = gm(q, gm(o, gdag(o)))
        Q[k] = q
    vac_ok = all(gtrace(Q[k]) == (64, 0) and gzero(gsub(gm(Q[k], Q[k]), gscale(Q[k], 64)))
                 and all(gzero(gm(o, Q[k])) for o in A[k]) for k in Q)

    def overlap(a, b):
        t = gtrace(gm(Q[a], Q[b]))
        assert t[1] == 0
        return Fraction(t[0], 4096)

    ovl = {"J3_J5": overlap("J3", "J5"), "J3_J6": overlap("J3", "J6"), "J5_J6": overlap("J5", "J6")}
    # weights of the J6 vacuum on Furey (J3) number sectors
    ops3 = A["J3"]
    n4 = [gm(gdag(o), o) for o in ops3]          # 4 N_k
    e4 = [gm(o, gdag(o)) for o in ops3]          # 4 (1 - N_k)
    weights = {}
    for n in range(4):
        tot = (np.zeros((8, 8), dtype=np.int64), np.zeros((8, 8), dtype=np.int64))
        for S in itertools.combinations(range(3), n):
            pr = I8
            for k in range(3):
                pr = gm(pr, n4[k] if k in S else e4[k])
            tot = gadd(tot, pr)                   # 64 * projector onto N_J3 = n
        t = gtrace(gm(Q["J6"], tot))
        weights[n] = Fraction(t[0], 4096)
    # N=2 component of Omega_J6 in the basis (a2+a3+, a3+a1+, a1+a2+) Omega_J3
    col3 = next(j for j in range(8) if Q["J3"][0][j, j] != 0)
    col6 = next(j for j in range(8) if Q["J6"][0][j, j] != 0)
    om3 = (Q["J3"][0][:, [col3]], Q["J3"][1][:, [col3]])
    om6 = (Q["J6"][0][:, [col6]], Q["J6"][1][:, [col6]])
    cr = [gdag(o) for o in ops3]                  # 2 a_k^dag
    coeffs = []
    for (j, k) in ((1, 2), (2, 0), (0, 1)):
        st = gm(cr[j], gm(cr[k], om3))
        c = gm(gdag(st), om6)
        coeffs.append((int(c[0][0, 0]), int(c[1][0, 0])))
    equal = len(set(coeffs)) == 1 and coeffs[0] != (0, 0)
    N3 = gadd(gadd(n4[0], n4[1]), n4[2])                                   # 4 N_J3
    n6 = [gm(gdag(o), o) for o in A["J6"]]
    N6 = gadd(gadd(n6[0], n6[1]), n6[2])                                   # 4 N_J6
    commute = gzero(gsub(gm(N3, N6), gm(N6, N3)))
    q = Fraction(1, 4)
    ok = (cliff and herm and car and vac_ok and all(v == q for v in ovl.values())
          and weights == {0: q, 1: 0, 2: Fraction(3, 4), 3: 0} and equal and not commute)
    claim("G19", ok, f"Clifford={cliff and herm}, CAR={car}, unique vacua={vac_ok}; |<.|.>|^2 "
          f"{ {k: str(v) for k, v in ovl.items()} }; Omega_J6 weights on N_J3=0..3 "
          f"{ {n: str(w) for n, w in weights.items()} }; N=2 coefficients (unnormalised, cyclic basis) "
          f"{coeffs} equal={equal}; [N_J3,N_J6]=0? {commute}")

    data["invariants"] = {
        "signed_automorphisms": len(autos),
        "delta96_order_counts": {str(k): v for k, v in ocount.items()},
        "su3_commutant_dim": dims,
        "delta96_commuting": d96_comm,
        "vacuum_overlap": {k: str(v) for k, v in ovl.items()},
        "j6_vacuum_weights": {"N0": str(weights[0]), "N2": str(weights[2])},
    }

    keys = ["phi", "fano_plus", "fano_minus", "link_order", "pairings", "stabilizer", "corners",
            "fano_diagram", "corner_view_order", "hexagons", "szilassi", "mismatch", "orbits", "invariants"]
    out = {k: data[k] for k in keys}
    with open(os.path.join(HERE, "geometry.json"), "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"wrote {os.path.join(HERE, 'geometry.json')}")
    print("ALL PASS" if all_ok else "SOME CLAIMS FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
