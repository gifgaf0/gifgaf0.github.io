"""
item_j_ts_sign.py -- C2 math_A item (j): OP-2.74.1c.i (L2440; Part VI L4531) and OP-2.74.1c.iii (L2442).

Ledger definitions (§2.75 Part I lift; §2.76 Part II; op_274_1c_l15_orbit_membership.py):
  F21     = the 21 elements of PSL(2,7) whose naive lift (i -> g(i), i+8 -> g(i)+8, 8 fixed)
            preserves Y  (= the 21 unsigned octonion automorphisms, item b).
  twosets = the 49 octad-straddle {a, b+8}, a,b in 1..7;  F21-orbits TS_O1 (contains {1,14}),
            TS_O2 (contains {2,13}), TS_IDOUB (the 7 {a, a+8}).
  sum-15 twosets: {a, 15-a}, a = 1..6.
Lead: "TS_O1 is exactly the twosets with e_a e_b = -e_{a XOR b}" (a in 1..7, b in 9..15).
"""
import json
from itertools import product, combinations
from collections import Counter
import numpy as np
import flint
from sedcore import *

OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = {}
plus = {i: 1 for i in PTS}
G = gl32_perms()
F21 = [g for g in G if octonion_signed_auto(perm_dict(g), plus)]
assert len(F21) == 21
def lift15(g):
    L = {i: g[i - 1] for i in PTS}; L.update({i + 8: g[i - 1] + 8 for i in PTS}); L[8] = 8
    return L
TW = [frozenset((a, b + 8)) for a in PTS for b in PTS]
def orbit(t):
    return frozenset(frozenset(lift15(g)[i] for i in t) for g in F21)
TS = {}
for t in TW:
    o = orbit(t)
    TS[o] = None
orbs = list(TS)
TS_O1 = next(o for o in orbs if frozenset((1, 14)) in o)
TS_O2 = next(o for o in orbs if frozenset((2, 13)) in o)
TS_ID = next(o for o in orbs if frozenset((1, 9)) in o)
say(f"F21 orbits on the 49 twosets: sizes {sorted(len(o) for o in orbs)}; TS_O1 {len(TS_O1)}, TS_O2 {len(TS_O2)}, TS_IDOUB {len(TS_ID)}")

def sigma(t):
    a, b = sorted(t)
    return SED[a][b]                      # e_a e_b = sigma e_{a^b}
s1 = Counter(sigma(t) for t in TS_O1); s2 = Counter(sigma(t) for t in TS_O2)
say(f"sigma (e_a e_b = sigma e_(a^b)) on TS_O1: {dict(s1)};  on TS_O2: {dict(s2)}")
say(f"lead's sign:     TS_O1 == {{sigma = -1}}: {set(TS_O1) == set(t for t in TW if t not in TS_ID and sigma(t) == -1)};  "
    f"TS_O2 == {{sigma = +1}}: {set(TS_O2) == set(t for t in TW if t not in TS_ID and sigma(t) == +1)}")
say(f"reversed sign:   TS_O1 == {{sigma = +1}}: {set(TS_O1) == set(t for t in TW if t not in TS_ID and sigma(t) == +1)};  "
    f"TS_O2 == {{sigma = -1}}: {set(TS_O2) == set(t for t in TW if t not in TS_ID and sigma(t) == -1)}")
RES['TS_O1_is_sigma_plus'] = set(TS_O1) == set(t for t in TW if t not in TS_ID and sigma(t) == +1)
say("  (a <= 7 < b. Equivalently e_b e_a = -e_(a^b) on TS_O1, since e_a, e_b anticommute: the lead's")
say("   'e_a e_b = -e_(a^b)' holds for TS_O1 only if the product is read in the order (copy-B unit)(copy-A unit).)")
RES['TS_O1_sigma'] = dict(s1); RES['TS_O2_sigma'] = dict(s2)
say("sum-15 twosets:")
for a in range(1, 7):
    t = frozenset((a, 15 - a))
    lab = 'TS_O1' if t in TS_O1 else 'TS_O2' if t in TS_O2 else '?'
    say(f"   ({a},{15-a}): e{a} e{15-a} = {sigma(t):+d} e{a ^ (15 - a)}   -> {lab};  chi7(b-8-a) = {chi7(15-a-8-a):+d}")
# F21-invariance of sigma (it must be: unsigned automorphisms preserve every structure constant)
inv = all(sigma(t) == sigma(frozenset(lift15(g)[i] for i in t)) for g in F21 for t in TW if t not in TS_ID)
say(f"sigma is F21-invariant: {inv}")
RES['sigma_F21_invariant'] = inv

# OP-2.74.1c.iii: the three L1.5 operator pairs, with all sign variants
P = 911
def nm(M): return flint.nmod_mat([[int(v) % P for v in row] for row in M.tolist()], P)
def yb(v1, v2):
    A = Lmat(v1); B = Lmat(v2)
    D = A @ B @ A - B @ A @ B
    K, nul = nm(D).nullspace()
    if nul == 0: return False
    Km = flint.nmod_mat([[int(K[r, c]) for c in range(nul)] for r in range(16)], P)
    base = Km.rank()
    for X in (nm(A) * Km, nm(B) * Km):
        S = flint.nmod_mat([[int(Km[r, c]) for c in range(nul)] + [int(X[r, c]) for c in range(nul)] for r in range(16)], P)
        if S.rank() != base: return False
    C = (nm(A) * nm(B) - nm(B) * nm(A)) * Km
    return any(int(C[r, c]) for r in range(16) for c in range(nul))
def v(a, b, s=1):
    x = basis(a); x[b] += s; return x
T = {'T_A': (1, 14), 'T_B': (2, 13), 'T_C': (4, 11)}
say("\nOP-2.74.1c.iii: L1.5 operator pairs (both all-plus, and with the relative sign of the 2nd flipped)")
for (n1, n2) in (('T_A', 'T_B'), ('T_A', 'T_C'), ('T_B', 'T_C')):
    t1, t2 = T[n1], T[n2]
    res = {(s1_, s2_, tt): yb(v(*t1, s1_), [tt * c for c in v(*t2, s2_)])
           for s1_, s2_, tt in product((1, -1), repeat=3)}
    co = any(all(c == 0 for c in mul(v(*t1, a_), v(*t2, b_))) for a_, b_ in product((1, -1), repeat=2))
    say(f"   ({n1},{n2}): sigma product {sigma(frozenset(t1))*sigma(frozenset(t2)):+d}; co-assessors {co}; "
        f"strut constants {t1[0]^(t1[1]-8)},{t2[0]^(t2[1]-8)}; YB(all-plus) {res[(1,1,1)]}; "
        f"YB sign variants (s1,s2,t): {[k for k, val in res.items() if val]}")
    RES[f'{n1}{n2}'] = [list(k) for k, val in res.items() if val]
# an explicit automorphism carrying the YB pair (e1+e14, e4+e11) onto a YB variant of (T_A, T_B)
target = {frozenset((1, 14)), frozenset((2, 13))}
found = None
for g in G:
    pi = perm_dict(g)
    for sg in product((1, -1), repeat=7):
        eps = dict(zip(PTS, sg))
        if not octonion_signed_auto(pi, eps): continue
        for e8s in (1, -1):
            M = sed_lift_matrix(pi, eps, e8s)
            u = (M @ np.array(v(1, 14))).tolist(); w = (M @ np.array(v(4, 11))).tolist()
            su = frozenset(i for i in range(16) if u[i]); sw = frozenset(i for i in range(16) if w[i])
            if {su, sw} == target:
                found = (g, sg, e8s, u, w); break
        if found: break
    if found: break
if found:
    g, sg, e8s, u, w = found
    fmt = lambda x: " ".join(f"{'+' if x[i] > 0 else '-'}e{i}" for i in range(16) if x[i])
    say(f"   automorphism (perm {g}, signs {sg}, e8 -> {e8s:+d}e8) maps (e1+e14, e4+e11) to ({fmt(u)}, {fmt(w)});"
        f" YB of the image: {yb(u, w)}")
RES['automorphism_TATC_to_TATB'] = str(found[:3]) if found else None

json.dump(RES, open("item_j_results.json", "w"), indent=1)
open("item_j_output.txt", "w").write("\n".join(OUT) + "\n")
