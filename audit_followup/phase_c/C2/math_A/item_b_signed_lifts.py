"""
item_b_signed_lifts.py -- C2 math_A item (b): signed vs unsigned Fano lifts, and whether
"PSL(2,7) does not act on Y" (§2.75) / the O_POS-O_NEG chirality survive signed lifts.

Definitions pinned from the ledger / its provenance scripts:
  * octonion automorphism by a (signed) permutation: e0 -> e0, e_i -> eps_i e_pi(i).
  * CD lift to the sedenions (the ledger's §2.75 Part I lift, with signs added):
        e_{i+8} -> e8s * eps_i e_{pi(i)+8},  e8 -> e8s * e8   (e8s = +1 or -1).
  * Y (§2.74/§2.75, sedenion_yb_pair_search.py): the 42 'ZD roots' are e_a + e_b
    (a<b, both coefficients +1) having a two-term annihilator; an unordered pair of roots
    is YB iff, with A = L_{x1}, B = L_{x2} over F_911 and K = ker(ABA - BAB):
      dim K > 0, K invariant under A and B, and [A,B]|_K != 0.
  * O_POS / O_NEG (§2.75 Part V; op_274_1c_l15_orbit_membership.py): the two F21-orbits
    on Y labelled by the chi7((y-8-x) mod 7) multiset counts.
"""
import json
from itertools import permutations, product, combinations
from collections import Counter, defaultdict
import numpy as np
import flint
from sedcore import *

P = 911
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)
RES = {}

# ledger data: the 42 YB pairs exactly as listed in oq274_psl27_orbit_decomp.py
YB_PAIRS_RAW = [
    ((1,10),(4,15)), ((1,10),(6,13)), ((1,11),(6,12)), ((1,11),(7,13)),
    ((1,12),(3,14)), ((1,12),(7,10)), ((1,13),(2,14)), ((1,13),(3,15)),
    ((1,14),(4,11)), ((1,14),(5,10)), ((1,15),(2,12)), ((1,15),(5,11)),
    ((2,9),(5,14)),  ((2,9),(7,12)),  ((2,11),(4,13)), ((2,11),(7,14)),
    ((2,12),(5,11)), ((2,13),(3,12)), ((2,13),(6,9)),  ((2,14),(3,15)),
    ((2,15),(4,9)),  ((2,15),(6,11)), ((3,9),(4,14)),  ((3,9),(5,15)),
    ((3,10),(5,12)), ((3,10),(6,15)), ((3,12),(6,9)),  ((3,13),(4,10)),
    ((3,13),(7,9)),  ((3,14),(7,10)), ((4,9),(6,11)),  ((4,10),(7,9)),
    ((4,11),(5,10)), ((4,13),(7,14)), ((4,14),(5,15)), ((4,15),(6,13)),
    ((5,9),(6,10)),  ((5,9),(7,11)),  ((5,12),(6,15)), ((5,14),(7,12)),
    ((6,10),(7,11)), ((6,12),(7,13)),
]
def canon_unsigned(pair):
    return frozenset(frozenset(t) for t in pair)
LEDGER_Y = set(canon_unsigned(p) for p in YB_PAIRS_RAW)
assert len(LEDGER_Y) == 42

# ===================================================================== B1
say("=" * 78)
say("B1. Pure (unsigned) permutations of e1..e7 that are octonion automorphisms")
say("=" * 78)
plus = {i: 1 for i in PTS}
pure_auts = []
for img in permutations(PTS):
    pi = dict(zip(PTS, img))
    if octonion_signed_auto(pi, plus):
        pure_auts.append(pi)
def perm_order(pi):
    k, cur = 1, dict(pi)
    while any(cur[i] != i for i in PTS):
        cur = {i: pi[cur[i]] for i in PTS}; k += 1
    return k
say(f"  count = {len(pure_auts)} (out of 5040); all collineations: {all(is_collineation(p) for p in pure_auts)}")
say(f"  element orders: {dict(sorted(Counter(perm_order(p) for p in pure_auts).items()))}")
F21_pure = [tuple(p[i] for i in PTS) for p in pure_auts]
RES['B1_pure_automorphisms'] = len(pure_auts)

# ===================================================================== B2
say()
say("=" * 78)
say("B2. Signed permutations e_i -> eps_i e_pi(i) that are octonion automorphisms")
say("=" * 78)
signed_auts = []
coll = [perm_dict(t) for t in gl32_perms()]
n_perm_tested = 0
for img in permutations(PTS):
    pi = dict(zip(PTS, img))
    n_perm_tested += 1
    if not is_collineation(pi):
        continue        # a non-collineation can never satisfy pi(i^j) = pi(i)^pi(j)
    for sg in product((1, -1), repeat=7):
        eps = dict(zip(PTS, sg))
        if octonion_signed_auto(pi, eps):
            signed_auts.append((tuple(img), sg))
# completeness: non-collineations fail the index condition for every sign choice
noncoll_fail = all(not octonion_signed_auto(dict(zip(PTS, img)), plus) for img in permutations(PTS)
                   if not is_collineation(dict(zip(PTS, img))))
by_perm = Counter(s[0] for s in signed_auts)
say(f"  signed automorphisms found = {len(signed_auts)}  (5040 x 128 = 645,120 candidates; "
    f"non-collineations excluded by the index law, verified: {noncoll_fail})")
say(f"  distinct underlying permutations = {len(by_perm)}; lifts per permutation = {sorted(set(by_perm.values()))}")
say(f"  underlying permutations == the 168 XOR-Fano collineations: {set(by_perm) == set(gl32_perms())}")
kernel = [sg for (img, sg) in signed_auts if img == tuple(PTS)]
say(f"  kernel (pi = id) sign vectors: {len(kernel)} ->")
for sg in kernel:
    flipped = sorted(i for i, s in zip(PTS, sg) if s < 0)
    fixedline = sorted(set(PTS) - set(flipped))
    say(f"     flip {flipped}  (complement {fixedline} is {'a line' if frozenset(fixedline) in LINES else 'not a line' if flipped else 'all'})")

# group law: compose signed maps, check closure and order
def compose(g, h):           # (g o h)(e_i) = g(h(e_i))
    (gi, gs), (hi, hs) = g, h
    img = tuple(gi[hi[i - 1] - 1] for i in PTS)
    sg = tuple(hs[i - 1] * gs[hi[i - 1] - 1] for i in PTS)
    return (img, sg)
SA = set(signed_auts)
closed = all(compose(g, h) in SA for g in signed_auts[::7] for h in signed_auts)
say(f"  closure under composition (sampled 1/7 x all): {closed};  |group| = {len(SA)}")
RES['B2_signed_automorphisms'] = len(SA)
RES['B2_lifts_per_collineation'] = sorted(set(by_perm.values()))

# split / non-split test: does some lift pair of (a, b) satisfy the PSL(2,7) presentation?
def pow_(g, k):
    r = (tuple(PTS), (1,) * 7)
    for _ in range(k):
        r = compose(g, r)
    return r
ID = (tuple(PTS), (1,) * 7)
def inv(g):
    for h in SA:
        if compose(g, h) == ID:
            return h
def unsigned_order(img):
    return perm_order(dict(zip(PTS, img)))
def order_signed(g):
    k, cur = 1, g
    while cur != ID:
        cur = compose(g, cur); k += 1
    return k
# pick generators of GL(3,2): x of order 2, y of order 3 with xy of order 7 and [x,y] of order 4
cols = gl32_perms()
def comp_u(p, q):
    return tuple(p[q[i - 1] - 1] for i in PTS)
def inv_u(p):
    r = [0] * 7
    for i in PTS: r[p[i - 1] - 1] = i
    return tuple(r)
gens = None
for x in cols:
    if unsigned_order(x) != 2: continue
    for y in cols:
        if unsigned_order(y) != 3: continue
        if unsigned_order(comp_u(x, y)) == 7:
            c = comp_u(comp_u(inv_u(x), inv_u(y)), comp_u(x, y))
            if unsigned_order(c) == 4:
                gens = (x, y); break
    if gens: break
lx = [g for g in signed_auts if g[0] == gens[0]]
ly = [g for g in signed_auts if g[0] == gens[1]]
sat = 0
order_hist = Counter()
for X in lx:
    for Y in ly:
        c = compose(compose(inv(X), inv(Y)), compose(X, Y))
        rel = (order_signed(X) == 2 or X == ID) and pow_(Y, 3) == ID and pow_(compose(X, Y), 7) == ID and pow_(c, 4) == ID
        sat += rel
    order_hist[order_signed(X)] += 1
say(f"  generators of PSL(2,7): x={gens[0]} (order 2), y={gens[1]} (order 3), xy order 7, [x,y] order 4")
say(f"  orders of the 8 lifts of x: {dict(order_hist)};  lifts of y of order 3: "
    f"{sum(1 for Y in ly if pow_(Y,3)==ID)}/8")
say(f"  lift pairs (X,Y) satisfying X^2=Y^3=(XY)^7=[X,Y]^4=1: {sat}/64  -> "
    f"{'SPLIT (a complement PSL(2,7) exists)' if sat else 'NON-SPLIT: no subgroup of the 1344-group maps isomorphically onto PSL(2,7)'}")
RES['B2_split'] = bool(sat)
inv_order_classes = Counter(order_signed(g) for g in SA)
say(f"  element-order distribution of the 1344-group: {dict(sorted(inv_order_classes.items()))}")

# orientation reversal pattern of unsigned collineations (§2.86 C 'orientation-reversers')
OT = oriented_triples()
def reversed_lines(pi):
    rev = 0
    for L in LINES:
        i, j = sorted(L)[:2]
        k = i ^ j
        # orientation of (i,j,k) in table vs image
        s0 = OCT[i][j]
        s1 = OCT[pi[i]][pi[j]]
        rev += (s0 != s1)
    return rev
rev_hist = Counter()
for t in cols:
    rev_hist[reversed_lines(perm_dict(t))] += 1
say(f"  unsigned collineations by # of the 7 lines whose orientation they reverse: {dict(sorted(rev_hist.items()))}")
say(f"   (7 reversed = anti-automorphism; 0 = automorphism)")
RES['B2_reversal_hist'] = dict(rev_hist)
# conjugacy-type split of the 147 non-preserving collineations
F21set = set(F21_pure)
ord147 = Counter(unsigned_order(t) for t in cols if t not in F21set)
say(f"  element orders of the 147 collineations outside F21: {dict(sorted(ord147.items()))}")
RES['B2_orders_outside_F21'] = dict(ord147)

# ===================================================================== B3
say()
say("=" * 78)
say("B3. CD lifts to the sedenions are sedenion automorphisms")
say("=" * 78)
LIFTS = []
for (img, sg) in signed_auts:
    pi = dict(zip(PTS, img)); eps = dict(zip(PTS, sg))
    for e8s in (1, -1):
        LIFTS.append(((img, sg, e8s), sed_lift_matrix(pi, eps, e8s)))
SEDA = np.array(SED, dtype=np.int64)
IJ = np.arange(16)[:, None] ^ np.arange(16)[None, :]
def fast_signed_perm_auto(M):
    """Exact test for a signed permutation matrix M (M e_i = c_i e_p(i))."""
    p = np.argmax(np.abs(M), axis=0); c = M[p, np.arange(16)]
    if not (np.abs(M).sum(axis=0) == 1).all():
        return False
    if not (p[IJ] == (p[:, None] ^ p[None, :])).all():
        return False
    lhs = SEDA * c[IJ]
    rhs = c[:, None] * c[None, :] * SEDA[p[:, None], p[None, :]]
    return bool((lhs == rhs).all())
ok_fast = sum(fast_signed_perm_auto(M) for (_, M) in LIFTS)
say(f"  all {len(LIFTS)} lifts (1344 octonion automorphisms x e8 -> +-e8) checked on all 256 basis "
    f"products: {ok_fast} are sedenion automorphisms")
agree = all(fast_signed_perm_auto(M) == is_sed_automorphism(M) for (_, M) in LIFTS[::97])
say(f"  fast test agrees with the slow generic test on a 1/97 sample: {agree}")
RES['B3_signed_sed_auts'] = ok_fast
# unsigned lifts: which are sedenion automorphisms
uns_ok = sum(is_sed_automorphism(sed_lift_matrix(perm_dict(t), plus, 1)) for t in cols)
say(f"  unsigned CD lifts (the §2.75 Part I lift) that are sedenion automorphisms: {uns_ok}/168")
RES['B3_unsigned_sed_auts'] = uns_ok

# ===================================================================== B4
say()
say("=" * 78)
say("B4. The YB family: reproduction, sign-resolution, and the group actions")
say("=" * 78)

def zd_roots():
    roots = []
    for a, b in combinations(range(1, 16), 2):
        x = basis(a); x[b] += 1
        M = Lmat(x)
        if exact_rank(M) < 16:
            # the script requires a two-term annihilator; check one exists
            found = False
            for c, d in combinations(range(1, 16), 2):
                if (c, d) == (a, b): continue
                for sc, sd in product((1, -1), repeat=2):
                    y = basis(c, sc); y[d] += sd
                    if all(v == 0 for v in mul(x, y)):
                        found = True; break
                if found: break
            if found:
                roots.append((a, b))
    return roots
ROOTS = zd_roots()
say(f"  ZD roots (e_a + e_b with a two-term annihilator): {len(ROOTS)}; all assessors "
    f"(a<=7, b>=9, b != a+8): {ROOTS == [(a,b) for a in PTS for b in range(9,16) if b != a+8]}")

def nm(M):
    return flint.nmod_mat([[int(v) % P for v in row] for row in M.tolist()], P)

def yb(v1, v2):
    A = Lmat(v1); B = Lmat(v2)
    D = A @ B @ A - B @ A @ B
    Dn = nm(D)
    K, nullity = Dn.nullspace()
    if nullity == 0:
        return False
    Kcols = [[int(K[r, c]) for r in range(16)] for c in range(nullity)]
    Kmat = flint.nmod_mat([[Kcols[c][r] for c in range(nullity)] for r in range(16)], P)
    base = Kmat.rank()
    An, Bn = nm(A), nm(B)
    AK, BK = An * Kmat, Bn * Kmat
    def stacked(X):
        return flint.nmod_mat([[int(Kmat[r, c]) for c in range(nullity)] + [int(X[r, c]) for c in range(nullity)]
                               for r in range(16)], P)
    if stacked(AK).rank() != base or stacked(BK).rank() != base:
        return False
    C = (An * Bn - Bn * An) * Kmat
    return any(int(C[r, c]) != 0 for r in range(16) for c in range(nullity))

def vec(a, b, s=1):
    v = basis(a); v[b] += s; return v

# (+,+,+) slice: the ledger's Y
Y_mine = set()
for T1, T2 in combinations(ROOTS, 2):
    if yb(vec(*T1), vec(*T2)):
        Y_mine.add(canon_unsigned((T1, T2)))
say(f"  reproduced Y (all-plus representatives): {len(Y_mine)} pairs; equal to the ledger's 42: {Y_mine == LEDGER_Y}")
RES['B4_Y_reproduced'] = (Y_mine == LEDGER_Y)

# sign-resolved family: elements e_a + s e_b, pairs (u1, t*u2)
def canon_signed(v1, v2):
    k1 = tuple(i for i in range(16) if v1[i]); k2 = tuple(i for i in range(16) if v2[i])
    w1, w2 = (v1, v2) if k1 <= k2 else (v2, v1)
    lead = next(w1[i] for i in range(16) if w1[i])
    if lead < 0:
        w1 = [-c for c in w1]; w2 = [-c for c in w2]
    return (tuple(w1), tuple(w2))

Ysgn = set()
profile = {}
for T1, T2 in combinations(ROOTS, 2):
    prof = []
    for s1, s2, t in product((1, -1), repeat=3):
        u1 = vec(T1[0], T1[1], s1); u2 = [t * c for c in vec(T2[0], T2[1], s2)]
        if yb(u1, u2):
            Ysgn.add(canon_signed(u1, u2)); prof.append((s1, s2, t))
    profile[canon_unsigned((T1, T2))] = tuple(prof)
Yexists = set(k for k, v in profile.items() if v)
say(f"  sign-resolved YB family Y^sgn: {len(Ysgn)} signed pairs (of 861 x 8 = 6888 tested)")
say(f"  its unsigned projection Y^E (twoset pairs with >=1 YB sign variant): {len(Yexists)}")
say(f"  Y (all-plus) subset of Y^E: {LEDGER_Y <= Yexists};  #YB sign variants per pair in Y^E: "
    f"{dict(Counter(len(v) for k, v in profile.items() if v))}")
RES['B4_Ysgn'] = len(Ysgn); RES['B4_YE'] = len(Yexists)

# action of the signed lifts on Y^sgn
def act(M, key):
    v1 = (M @ np.array(key[0])).tolist(); v2 = (M @ np.array(key[1])).tolist()
    return canon_signed(v1, v2)
inv_all = all(act(M, key) in Ysgn for (_, M) in LIFTS for key in Ysgn)
say(f"  Y^sgn invariant under all {len(LIFTS)} signed CD lifts (2 x 1344): {inv_all}")
# naive unsigned action on twoset pairs
def lift15(t):
    L = {i: t[i - 1] for i in PTS}
    L.update({i + 8: t[i - 1] + 8 for i in PTS}); L[8] = 8
    return L
def act_unsigned(L, pair):
    return frozenset(frozenset(L[i] for i in ts) for ts in pair)
pres_Y = [t for t in cols if all(act_unsigned(lift15(t), p) in LEDGER_Y for p in LEDGER_Y)]
pres_YE = [t for t in cols if all(act_unsigned(lift15(t), p) in Yexists for p in Yexists)]
say(f"  naive (unsigned) lift: elements preserving Y = {len(pres_Y)} (ledger: 21); "
    f"preserving Y^E = {len(pres_YE)}")
say(f"  the 21 Y-preservers == the 21 pure automorphisms (F21): {set(pres_Y) == F21set}")
# the signed lift acts on unsigned twosets exactly as the naive lift does
same_on_twosets = True
for (k, M) in LIFTS[::5]:
    img = k[0]
    for (a, b) in ROOTS:
        w = (M @ np.array(vec(a, b))).tolist()
        supp = frozenset(i for i in range(16) if w[i])
        if supp != frozenset((img[a - 1], img[b - 9] + 8)):
            same_on_twosets = False
say(f"  signed lifts induce on unsigned twosets the same permutation as the naive lift: {same_on_twosets}")
say("   => as a set of unsigned twoset-pairs, Y is preserved by exactly the same 21 collineations")
say("      whether or not signs are used.")
RES['B4_naive_preservers_Y'] = len(pres_Y); RES['B4_naive_preservers_YE'] = len(pres_YE)

# which signed lifts preserve the all-plus slice Y (as signed pairs)?
plus_slice = set(k for k in Ysgn if all(c >= 0 for c in k[0]) and all(c >= 0 for c in k[1]))
say(f"  all-plus members of Y^sgn: {len(plus_slice)} (should be the 42 of Y)")
slice_pres = [k for (k, M) in LIFTS if all(act(M, key) in plus_slice for key in plus_slice)]
say(f"  signed lifts mapping the all-plus slice onto itself: {len(slice_pres)}; their underlying "
    f"permutations: {len(set(k[0] for k in slice_pres))} distinct, all in F21: "
    f"{set(k[0] for k in slice_pres) <= F21set}")

# orbits of the signed group on Y^sgn
def orbits(elements, maps, actf):
    left = set(elements); orbs = []
    while left:
        s = next(iter(left)); orb = {s}; fr = [s]
        while fr:
            nf = []
            for x in fr:
                for M in maps:
                    y = actf(M, x)
                    if y not in orb:
                        orb.add(y); nf.append(y)
            fr = nf
        orbs.append(orb); left -= orb
    return orbs
gen_maps = [M for (k, M) in LIFTS if k[0] in (gens[0], gens[1]) or (k[0] == tuple(PTS))]
O_sgn = orbits(Ysgn, gen_maps, act)
say(f"  orbits of the signed-lift group on Y^sgn: sizes {sorted(len(o) for o in O_sgn)}")

# F21 orbits on Y and the chirality labels
F21_lifts = [lift15(t) for t in F21_pure]
O_F21 = orbits(LEDGER_Y, F21_lifts, act_unsigned)
def chir_dist(orb):
    dist = Counter()
    for raw in YB_PAIRS_RAW:
        if canon_unsigned(raw) in orb:
            (x1, y1), (x2, y2) = raw
            dist[tuple(sorted([chi7(y1 - 8 - x1), chi7(y2 - 8 - x2)]))] += 1
    return dist
labels = {}
for o in O_F21:
    d = chir_dist(o)
    lab = "O_NEG" if d.get((-1, -1), 0) > d.get((1, 1), 0) else "O_POS"
    labels[lab] = o
    say(f"  F21-orbit size {len(o)}: chirality multiset counts {dict(d)} -> {lab}")
# where do O_POS and O_NEG (as all-plus signed pairs) sit among the signed-group orbits?
def plus_key(pair):
    (a, b), (c, d) = [tuple(sorted(t)) for t in pair]
    return canon_signed(vec(a, b), vec(c, d))
for lab in ("O_POS", "O_NEG"):
    idx = Counter()
    for pr in labels[lab]:
        k = plus_key(tuple(pr))
        for n_, o in enumerate(O_sgn):
            if k in o:
                idx[n_] += 1
    say(f"  {lab} members lie in signed-group orbit(s) {dict(idx)}")
cross = []
for (k, M) in LIFTS:
    for pr in list(labels["O_POS"])[:1]:
        img = act(M, plus_key(tuple(pr)))
        if img in plus_slice:
            un = canon_unsigned(tuple(tuple(i for i in range(16) if v[i]) for v in img))
            if un in labels["O_NEG"]:
                cross.append((k, un))
say(f"  signed lifts carrying an O_POS all-plus pair to an O_NEG all-plus pair: {len(cross)} "
    f"(e.g. underlying perm {cross[0][0][0] if cross else None}, signs {cross[0][0][1] if cross else None}, e8 {cross[0][0][2] if cross else None})")
RES['B4_signed_orbits_on_Ysgn'] = sorted(len(o) for o in O_sgn)
RES['B4_OPOS_to_ONEG_maps'] = len(cross)
for n_, o in enumerate(O_sgn):
    npl = len(o & plus_slice)
    say(f"   signed orbit #{n_}: size {len(o)}, all-plus members {npl}")
# sigma(T): e_a e_b = sigma e_(a^b) for an assessor twoset T=(a,b)
def sigma(T):
    a, b = T
    return SED[a][b]
# naive PSL(2,7) orbits on Y^E and how Y sits in it
O_YE = orbits(Yexists, [lift15(t) for t in (gens[0], gens[1])], act_unsigned)
say(f"  naive-lift PSL(2,7) orbits on Y^E: sizes {sorted(len(o) for o in O_YE)}; "
    f"Y meets them as {[len(o & LEDGER_Y) for o in O_YE]}")
prof_hist = Counter()
for k, v in profile.items():
    if not v: continue
    T1, T2 = [tuple(sorted(t)) for t in k]
    prof_hist[(k in LEDGER_Y, sigma(T1) * sigma(T2), v)] += 1
say("  sign profiles over Y^E: (in Y?, sigma(T1)*sigma(T2), YB sign variants (s1,s2,t)) -> count")
for key, cnt in sorted(prof_hist.items(), key=lambda kv: str(kv[0])):
    say(f"     {key} : {cnt}")
RES['B4_profiles'] = {str(k): v for k, v in prof_hist.items()}
with open("item_b_YE_pairs.txt", "w") as fh:
    fh.write("# the 126 sign-blind YB twoset pairs Y^E; columns: T1 T2 inY sigma1*sigma2 YB-sign-variants(s1,s2,t)\n")
    for k in sorted(Yexists, key=lambda s: sorted(sorted(t) for t in s)):
        T1, T2 = sorted(tuple(sorted(t)) for t in k)
        fh.write(f"{T1} {T2} {k in LEDGER_Y} {sigma(T1)*sigma(T2):+d} {profile[k]}\n")

# ===================================================================== B5
say()
say("=" * 78)
say("B5. G-2a.3 (§2.41.B L1760): the annihilation graph on the 84 two-term ZDs")
say("=" * 78)
ZD84 = []
for (a, b) in ROOTS:
    for s in (1, -1):
        ZD84.append(tuple(vec(a, b, s)))
def zkey(v):
    lead = next(c for c in v if c)
    return tuple(v) if lead > 0 else tuple(-c for c in v)
E = set()
for u, w in combinations(ZD84, 2):
    if all(c == 0 for c in mul(list(u), list(w))):
        E.add(frozenset((u, w)))
deg = Counter()
for e in E:
    for u in e: deg[u] += 1
say(f"  edges = {len(E)}; degrees = {sorted(set(deg.values()))}")
# components
adj = defaultdict(set)
for e in E:
    u, w = tuple(e); adj[u].add(w); adj[w].add(u)
comps = []; seen = set()
for v in ZD84:
    if v in seen: continue
    st = [v]; comp = set([v]); seen.add(v)
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y); comp.add(y); st.append(y)
    comps.append(comp)
miss = []
for c in comps:
    used = set()
    for v in c:
        for i in range(16):
            if v[i]: used.add(i if i < 8 else i - 8)
    miss.append(sorted(set(PTS) - used))
say(f"  components: {len(comps)} of sizes {sorted(len(c) for c in comps)}; missing octonion index per component: {miss}")
# assessor-level graph inside each component: octahedron check
for c in comps[:1]:
    ass = sorted(set(tuple(i for i in range(16) if v[i]) for v in c))
    aedges = set()
    for e in E:
        u, w = tuple(e)
        if u in c:
            aedges.add(frozenset((tuple(i for i in range(16) if u[i]), tuple(i for i in range(16) if w[i]))))
    adeg = Counter()
    for e in aedges:
        for t in e: adeg[t] += 1
    say(f"  component 1: {len(ass)} assessors, {len(aedges)} assessor-edges, degrees {sorted(set(adeg.values()))} "
        f"(octahedron K_2,2,2: 6 vertices, 12 edges, 4-regular)")
def act_vec(M, v):
    return zkey((M @ np.array(v)).tolist())
Ekeys = set(frozenset(zkey(list(x)) for x in e) for e in E)
def preserves_graph(M):
    for e in Ekeys:
        u, w = tuple(e)
        if frozenset((act_vec(M, u), act_vec(M, w))) not in Ekeys:
            return False
    return True
uns_pres = sum(preserves_graph(sed_lift_matrix(perm_dict(t), plus, 1)) for t in cols)
sgn_pres = sum(preserves_graph(M) for (_, M) in LIFTS)
say(f"  unsigned naive lifts preserving the annihilation graph: {uns_pres}/168 (ledger: 21)")
say(f"  signed CD lifts preserving the annihilation graph: {sgn_pres}/{len(LIFTS)}")
RES['B5'] = dict(edges=len(E), comps=sorted(len(c) for c in comps), unsigned_preservers=uns_pres,
                 signed_preservers=sgn_pres, n_lifts=len(LIFTS))
# the signed-lift group acting on the 168 annihilating unordered pairs
def act_ann(M, e):
    u, w = tuple(e)
    return frozenset((zkey((M @ np.array(u)).tolist()), zkey((M @ np.array(w)).tolist())))
O_ann = orbits(Ekeys, gen_maps, act_ann)
say(f"  signed-lift group on the {len(Ekeys)} annihilating pairs: orbit sizes {sorted(len(o) for o in O_ann)}")
RES['B5_ann_orbits'] = sorted(len(o) for o in O_ann)
gen_maps_1344 = [M for (k, M) in LIFTS if k[2] == 1 and (k[0] in (gens[0], gens[1]) or k[0] == tuple(PTS))]
O_ann1344 = orbits(Ekeys, gen_maps_1344, act_ann)
e0 = next(iter(Ekeys))
stab1344 = sum(1 for (k, M) in LIFTS if k[2] == 1 and act_ann(M, e0) == e0)
kern_moves = [sum(1 for e in Ekeys if act_ann(M, e) != e) for (k, M) in LIFTS if k[2] == 1 and k[0] == tuple(PTS)]
say(f"  1344 lifts with e8 -> +e8: orbit sizes on the 168 pairs {sorted(len(o) for o in O_ann1344)}; "
    f"stabilizer of one pair: {stab1344}; annihilating pairs moved by each of the 8 kernel (pi=id) lifts: {kern_moves}")
say("   -> the action on the pairs is by the non-split 2^3.PSL(2,7), whose 2^3 acts non-trivially;")
say("      it does not factor through an action of PSL(2,7) itself.")
RES['B5_1344_orbits'] = sorted(len(o) for o in O_ann1344); RES['B5_1344_stab'] = stab1344
RES['B5_kernel_moves'] = kern_moves
# box-kite membership of the Y pairs, and of the three PSL(2,7)-orbits on Y^E
def strut(T):
    a, b = T
    return a ^ (b - 8)
def coassessor(T1, T2):
    u = vec(*T1); w1 = vec(*T2); w2 = vec(T2[0], T2[1], -1)
    return any(all(c == 0 for c in mul(u, w)) for w in (w1, w2))
for n_, o in enumerate(O_YE):
    kinds = Counter()
    for k in o:
        T1, T2 = sorted(tuple(sorted(t)) for t in k)
        same = strut(T1) == strut(T2)
        kinds[('same box-kite' if same else 'different box-kites',
               'co-assessors' if coassessor(T1, T2) else 'not co-assessors')] += 1
    say(f"  PSL(2,7)-orbit on Y^E of size {len(o)} (meets Y in {len(o & LEDGER_Y)}): {dict(kinds)}")
yk = Counter()
for k in LEDGER_Y:
    T1, T2 = sorted(tuple(sorted(t)) for t in k)
    yk[(strut(T1) == strut(T2), coassessor(T1, T2), sigma(T1) == sigma(T2))] += 1
say(f"  Y pairs by (same box-kite, co-assessors, equal sigma): {dict(yk)}")

json.dump(RES, open("item_b_results.json", "w"), indent=1, default=str)
open("item_b_output.txt", "w").write("\n".join(OUT) + "\n")
say("wrote item_b_output.txt, item_b_results.json")
