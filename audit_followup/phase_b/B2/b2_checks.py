#!/usr/bin/env python3
"""B2 checks for the PSL(2,7) Zenodo note (v2 -> v3 draft). Explicit computation, no character-table lookup.

(1) PSL(2,7) as 2x2 matrices over F_7 modulo ±I; conjugacy classes, orders, sizes.
(2) rho_8 built explicitly as Ind_B^G(chi), B = upper-triangular Borel (order 21), chi of order 3;
    its character per class; eigenvalue-1 multiplicity per class = dimension of the fixed subspace in R^8
    (rho_8 is real, so the complex fixed dimension equals the real one); fixed set on S^7 = unit sphere of that subspace.
(3) all subgroups (every subgroup of PSL(2,7) is 2-generated) and the maximal ones; D4 maximal or not.
(4) n_1(H; rho_6) for every maximal subgroup H, with chi_6 = (permutation character on the cosets of an S4) - 1.
(5) the decomposition of L^2(G/D4) by multiplicities <Ind 1, rho>, for rho_1, rho_6, rho_7, rho_8.
"""
import itertools, json
import numpy as np

p = 7
def mul(a, b):
    return ((a[0]*b[0] + a[1]*b[2]) % p, (a[0]*b[1] + a[1]*b[3]) % p,
            (a[2]*b[0] + a[3]*b[2]) % p, (a[2]*b[1] + a[3]*b[3]) % p)
def neg(a):
    return tuple((-x) % p for x in a)
def canon(a):
    return min(a, neg(a))
SL = [m for m in itertools.product(range(p), repeat=4) if (m[0]*m[3] - m[1]*m[2]) % p == 1]
G = sorted(set(canon(m) for m in SL))
assert len(SL) == 336 and len(G) == 168
idx = {g: i for i, g in enumerate(G)}
I = canon((1, 0, 0, 1))
def gm(a, b):
    return canon(mul(a, b))
def inv(a):
    return canon((a[3], (-a[1]) % p, (-a[2]) % p, a[0]))
def order(a):
    k, x = 1, a
    while x != I:
        x, k = gm(x, a), k + 1
    return k
# conjugacy classes
seen, classes = set(), []
for g in G:
    if g in seen:
        continue
    cl = sorted(set(gm(gm(h, g), inv(h)) for h in G))
    seen |= set(cl)
    classes.append(cl)
# label classes; split the two order-7 classes as 7A (contains [[1,1],[0,1]]) and 7B
u = canon((1, 1, 0, 1))
def label(cl):
    o = order(cl[0])
    if o == 7:
        return "7A" if u in cl else "7B"
    return {1: "1A", 2: "2A", 3: "3A", 4: "4A"}[o]
classes.sort(key=lambda c: (order(c[0]), label(c)))
cls_of = {g: label(c) for c in classes for g in c}
print("(1) classes:", [(label(c), order(c[0]), len(c)) for c in classes])

# ---------------------------------------------------------------- (2) rho_8 = Ind_B^G chi
B = [g for g in G if g[2] == 0]                     # upper triangular mod ±I
assert len(B) == 21
w = np.exp(2j * np.pi / 3)
def chi(b):
    # b = [[a, x],[0, a^-1]] mod ±1; a^2 is well defined; chi(b) = w^(log_3 of a^2 in the order-3 group <2>)
    a2 = (b[0] * b[0]) % p                          # in {1, 2, 4}
    return {1: 1, 2: w, 4: w * w}[a2]
# left coset representatives of B
reps, covered = [], set()
for g in G:
    if g in covered:
        continue
    reps.append(g)
    covered |= set(gm(g, b) for b in B)
assert len(reps) == 8
Bset = set(B)
def rho8(g):
    M = np.zeros((8, 8), dtype=complex)
    for j, r in enumerate(reps):
        gr = gm(g, r)
        for i, s in enumerate(reps):
            b = gm(inv(s), gr)
            if b in Bset:
                M[i, j] = chi(b)
                break
    return M
mats = {g: rho8(g) for g in G}
for a, b in [(G[5], G[17]), (G[40], G[101]), (G[77], G[150])]:
    assert np.allclose(mats[gm(a, b)], mats[a] @ mats[b])
assert all(np.allclose(m @ m.conj().T, np.eye(8)) for m in mats.values())
char8, fixdim = {}, {}
for c in classes:
    vals = [np.trace(mats[g]) for g in c]
    assert np.allclose(vals, vals[0])
    lab = label(c)
    assert abs(vals[0].imag) < 1e-9
    char8[lab] = round(float(vals[0].real), 9)
    fd = []
    for g in c:
        ev = np.linalg.eigvals(mats[g])
        fd.append(int(np.sum(np.abs(ev - 1) < 1e-8)))
    assert len(set(fd)) == 1
    fixdim[lab] = fd[0]
# irreducibility: sum |chi|^2 / |G| = 1
norm = sum(len(c) * abs(np.trace(mats[c[0]])) ** 2 for c in classes) / 168
print("(2) rho_8 character by class:", char8, "| <chi,chi> =", round(norm, 9))
print("(2) fixed-subspace dimension by class:", fixdim)
sphere = {lab: f"S^{d-1}" for lab, d in fixdim.items()}
print("(2) fixed set on S^7 by class:", sphere)
circle = sum(len(c) for c in classes if fixdim[label(c)] == 2)
three_sphere = sum(len(c) for c in classes if fixdim[label(c)] == 4)
print(f"(2) elements fixing a circle: {circle} = " + " + ".join(f"{label(c)}:{len(c)}" for c in classes if fixdim[label(c)] == 2)
      + f"; elements fixing an S^3: {three_sphere}; without 4A: {circle - sum(len(c) for c in classes if label(c) == '4A')}")
# nesting: Fix(g) for g in 4A lies inside Fix(g^2), g^2 in 2A
g4 = [c for c in classes if label(c) == "4A"][0][0]
def fixspace(M):
    ev, V = np.linalg.eig(M)
    return V[:, np.abs(ev - 1) < 1e-8]
F4, F2 = fixspace(mats[g4]), fixspace(mats[gm(g4, g4)])
proj = F2 @ np.linalg.pinv(F2)
print("(2) Fix(4A element) inside Fix(its square, 2A):", bool(np.allclose(proj @ F4, F4)), "| square in", cls_of[gm(g4, g4)])

# ---------------------------------------------------------------- (3) subgroups
def closure(gens):
    S = {I}
    frontier = [I]
    while frontier:
        new = []
        for x in frontier:
            for gg in gens:
                y = gm(x, gg)
                if y not in S:
                    S.add(y); new.append(y)
        frontier = new
    return frozenset(S)
subs = set()
for a in G:
    subs.add(closure([a]))
for a, b in itertools.combinations(G, 2):
    subs.add(closure([a, b]))
subs = sorted(subs, key=len)
proper = [S for S in subs if len(S) < 168]
maximal = [S for S in proper if not any(S < T for T in proper)]
def iso_type(S):
    n = len(S)
    ords = sorted(order(x) for x in S)
    o = {k: ords.count(k) for k in set(ords)}
    if n == 24: return "S4"
    if n == 21: return "7:3"
    if n == 8: return "D4" if o.get(4, 0) == 2 else "?"
    return f"order {n}"
print(f"(3) number of subgroups: {len(subs)}")
mt = {}
for S in maximal:
    mt[iso_type(S)] = mt.get(iso_type(S), 0) + 1
print("(3) maximal subgroups by type (count of subgroups):", mt)
# conjugacy classes of maximal subgroups
def conj_set(S, h):
    return frozenset(gm(gm(h, x), inv(h)) for x in S)
mclasses = []
for S in maximal:
    if not any(S in cc for cc in mclasses):
        mclasses.append(set(conj_set(S, h) for h in G))
print("(3) conjugacy classes of maximal subgroups:", [(iso_type(next(iter(cc))), len(cc)) for cc in mclasses])
d4s = [S for S in subs if len(S) == 8]
print(f"(3) subgroups of order 8: {len(d4s)}; all D4: {all(iso_type(S)=='D4' for S in d4s)}; "
      f"each inside an S4: {all(any(S < T for T in maximal if len(T)==24) for S in d4s)}; any maximal: {any(S in maximal for S in d4s)}")

# ---------------------------------------------------------------- (4) n_1(H; rho_6)
S4 = [S for S in maximal if len(S) == 24][0]
cos, cov = [], set()
for g in G:
    if g in cov:
        continue
    cs = frozenset(gm(g, h) for h in S4)
    cos.append(cs); cov |= cs
assert len(cos) == 7
def perm_char(g):
    return sum(1 for cs in cos if frozenset(gm(g, x) for x in cs) == cs)
chi6 = {label(c): perm_char(c[0]) - 1 for c in classes}
assert all(perm_char(x) - 1 == chi6[label(c)] for c in classes for x in c)
norm6 = sum(len(c) * chi6[label(c)] ** 2 for c in classes) / 168
print("(4) chi_6 by class:", chi6, "| <chi6,chi6> =", norm6)
n1 = []
for cc in mclasses:
    for S in sorted(cc, key=lambda s: sorted(s))[:1]:
        val = sum(chi6[cls_of[x]] for x in S) / len(S)
        n1.append((iso_type(S), len(cc), val))
# all members of each class give the same value; check every maximal subgroup
all_n1 = {}
for S in maximal:
    all_n1.setdefault(iso_type(S), set()).add(sum(chi6[cls_of[x]] for x in S) / len(S))
print("(4) n_1(H; rho_6) per maximal class (type, class size, value):", n1, "| all values by type:", all_n1)
D4 = d4s[0]
print("(4) n_1(D4; rho_6) =", sum(chi6[cls_of[x]] for x in D4) / 8, "(D4 not maximal; for the record)")
# outer automorphism exchanges the two S4 classes: conjugation by diag(3,1) in PGL(2,7)
def outer(a):
    # conjugation by t = [[3,0],[0,1]] : t a t^-1 = [[a0, 3 a1],[a2/3, a3]]
    i3 = pow(3, -1, p)
    return canon((a[0], (3 * a[1]) % p, (a[2] * i3) % p, a[3]))
s4cls = [cc for cc in mclasses if len(next(iter(cc))) == 24]
img = frozenset(outer(x) for x in next(iter(s4cls[0])))
print("(4) outer automorphism maps S4 class 1 to class 2:", img in s4cls[1], "| fixes chi_6 (7A<->7B swap leaves chi_6):",
      chi6["7A"] == chi6["7B"])

# ---------------------------------------------------------------- (5) L^2(G/D4)
chars = {"rho1": {l: 1 for l in chi6}, "rho6": chi6, "rho7": None, "rho8": dict(char8)}
# rho7 = permutation character on P^1(F_7) (cosets of B) minus 1
def perm_B(g):
    return sum(1 for r in reps if gm(inv(r), gm(g, r)) in Bset)
chars["rho7"] = {label(c): perm_B(c[0]) - 1 for c in classes}
mult = {name: round(float(sum(ch[cls_of[x]] for x in D4) / 8), 9) for name, ch in chars.items()}
print("(5) multiplicities in L^2(G/D4):", mult, "| dimension check:", 1 * mult["rho1"] + 6 * mult["rho6"] + 7 * mult["rho7"] + 8 * mult["rho8"])

out = {"classes": [(label(c), order(c[0]), len(c)) for c in classes], "rho8_char": {k: str(v) for k, v in char8.items()},
       "rho8_fixdim": fixdim, "elements_fixing_circle": circle, "elements_fixing_S3": three_sphere,
       "without_4A": circle - 42, "n_subgroups": len(subs), "maximal_types": mt,
       "maximal_classes": [(iso_type(next(iter(cc))), len(cc)) for cc in mclasses],
       "D4_maximal": any(S in maximal for S in d4s), "chi6": chi6, "n1": {k: sorted(v) for k, v in all_n1.items()},
       "L2_G_D4": mult}
json.dump(out, open("b2_results.json", "w"), indent=1, sort_keys=True)
print("wrote b2_results.json")
