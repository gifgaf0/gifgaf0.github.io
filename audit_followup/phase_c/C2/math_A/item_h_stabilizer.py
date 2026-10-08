"""
item_h_stabilizer.py -- C2 math_A item (h): §2.62.C "V4 Klein Four-Group as Code-Space
Stabilizer" (L3408-3412; also §2.41 L1740, §2.29 Thm 4 L484, §2.42 L1782).

Objects (pinned from §2.62.A-C and tqc_stabilizer_group.py):
  * Fano flags (m, L), m in L, in the XOR Fano plane; PSL(2,7) = GL(3,2) acting on them.
  * code space C(m, L): for the three lines L_k through m, pair (i_k, j_k) = sorted(L_k - {m}),
    s_k = sign of e_{i_k} e_{j_k} on e_m, x_k = e_{i_k} + s_k e_{j_k + 8};
    C = ker L_{x_j} cap ker L_{x_k}  (computed here exactly over Q); its flag is (m, {m} u interior).
  * group actions on the sedenions: (U) the unsigned lift used by tqc_stabilizer_group.py
    (e_i -> e_g(i), e_{i+8} -> e_{g(i)+8}); (S) the signed CD lifts (genuine automorphisms).
"""
import json
from itertools import combinations, product
from collections import Counter
import numpy as np
import flint
from sedcore import *

OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = {}

G = gl32_perms()                     # tuples, g[i-1] = g(i)
def comp(p, q): return tuple(p[q[i - 1] - 1] for i in PTS)
def order(p):
    k, cur = 1, p
    while cur != tuple(PTS):
        cur = comp(p, cur); k += 1
    return k
def iso_type(H):
    od = Counter(order(h) for h in H)
    ab = all(comp(a, b) == comp(b, a) for a in H for b in H)
    n = len(H)
    t = {(8, False, (1, 5, 2)): "D4 (dihedral, order 8)",
         (8, False, (1, 1, 6)): "Q8",
         (8, True, (1, 7, 0)): "C2^3 = V4 x C2",
         (4, True, (1, 3, 0)): "V4 = C2 x C2",
         (4, True, (1, 1, 2)): "C4"}
    key = (n, ab, (od.get(1, 0), od.get(2, 0), od.get(4, 0)))
    return t.get(key, f"order {n}, abelian={ab}, orders={dict(od)}"), dict(sorted(od.items())), ab

# ------------------------------------------------------------- H1 abstract flags
say("=" * 78); say("H1. PSL(2,7) = GL(3,2) on the 21 Fano flags"); say("=" * 78)
flags = [(m, L) for L in LINES for m in sorted(L)]
assert len(flags) == 21
def act_flag(g, f):
    m, L = f
    return (g[m - 1], frozenset(g[x - 1] for x in L))
orb = set(act_flag(g, flags[0]) for g in G)
say(f"  orbit of a flag: {len(orb)} (transitive: {len(orb) == 21})")
stab_types = Counter(); pw_types = Counter(); contain = True
for f in flags:
    St = [g for g in G if act_flag(g, f) == f]
    PW = [g for g in G if all(g[x - 1] == x for x in f[1])]
    stab_types[(len(St),) + (iso_type(St)[0],)] += 1
    pw_types[(len(PW),) + (iso_type(PW)[0],)] += 1
    contain &= set(PW) <= set(St)
say(f"  flag stabilizers: {dict(stab_types)}")
say(f"  pointwise stabilizers of the flag's line: {dict(pw_types)};  contained in the flag stabilizer (index 2): {contain}")
f0 = flags[0]
St0 = [g for g in G if act_flag(g, f0) == f0]
t0 = iso_type(St0)
say(f"  example flag {f0[0]} in {sorted(f0[1])}: |Stab| = {len(St0)}, element orders {t0[1]}, abelian {t0[2]} -> {t0[0]}")
say(f"  V4 x C2 would be abelian with element orders {{1:1, 2:7}}; the flag stabilizer is not.")
RES['flag_stabilizer'] = dict(order=len(St0), type=t0[0], orders=t0[1])

# ------------------------------------------------------------- H2 code spaces (exact)
say(); say("=" * 78); say("H2. The 21 code spaces C(m,L) rebuilt exactly over Q"); say("=" * 78)
def kernel_basis(x):
    M = flint.fmpz_mat(Lmat(x).tolist())
    X, nul = M.nullspace()
    return [[int(X[r, c]) for r in range(16)] for c in range(nul)]
def span_canon(vecs):
    """canonical RREF (over Q) of the row space, as a hashable tuple"""
    R, rk = flint.fmpq_mat(len(vecs), 16, [v for vec in vecs for v in vec]).rref()
    return tuple(tuple(str(R[i, j]) for j in range(16)) for i in range(rk))
def intersect(B1, B2):
    M = flint.fmpz_mat(16, len(B1) + len(B2), [ (B1 + [[-c for c in v] for v in B2])[c][r]
                                                for r in range(16) for c in range(len(B1) + len(B2))])
    X, nul = M.nullspace()
    out = []
    for c in range(nul):
        coeff = [int(X[r, c]) for r in range(len(B1) + len(B2))]
        v = [sum(coeff[t] * B1[t][r] for t in range(len(B1))) for r in range(16)]
        if any(v): out.append(v)
    if not out: return []
    R, rk = flint.fmpq_mat(len(out), 16, [v for vec in out for v in vec]).rref()
    return out if rk else []
def lines_through(m): return [L for L in LINES if m in L]
CS = []
for m in PTS:
    lines = lines_through(m)
    pairs = [tuple(sorted(L - {m})) for L in lines]
    ks = []
    for (i, j) in pairs:
        s = SED[i][j] if (i ^ j) == m else None
        x = basis(i); x[j + 8] += s
        ks.append(kernel_basis(x))
    for (u, w) in ((0, 1), (0, 2), (1, 2)):
        I = intersect(ks[u], ks[w])
        R, rk = flint.fmpq_mat(len(I), 16, [v for vec in I for v in vec]).rref()
        interior = sorted(set(idx for v in I for idx in range(1, 8) if v[idx]))
        L = frozenset([m] + interior)
        CS.append(dict(m=m, L=L, basis=I, dim=rk, key=span_canon(I), isline=L in LINES))
say(f"  code spaces: {len(CS)}; dims {Counter(c['dim'] for c in CS)}; flag = (m, m u interior) is a line: "
    f"{all(c['isline'] for c in CS)}; distinct flags: {len(set((c['m'], c['L']) for c in CS))}; "
    f"distinct subspaces: {len(set(c['key'] for c in CS))}")
CSKEYS = {c['key']: (c['m'], c['L']) for c in CS}

def image_key(P, C):
    return span_canon([(P @ np.array(v)).tolist() for v in C['basis']])

# ------------------------------------------------------------- H3 unsigned lift (the ledger's computation)
say(); say("=" * 78); say("H3. Unsigned lift (tqc_stabilizer_group.py): stabilizers and orbits"); say("=" * 78)
plus = {i: 1 for i in PTS}
UL = [(g, sed_lift_matrix(perm_dict(g), plus, 1)) for g in G]
res_u = Counter(); orbit_sizes = Counter(); in_cs = Counter(); pw_eq = True
for C in CS:
    imgs = {}
    for g, P in UL:
        imgs.setdefault(image_key(P, C), []).append(g)
    St = imgs[C['key']]
    tname = iso_type(St)[0]
    res_u[(len(St), tname)] += 1
    orbit_sizes[len(imgs)] += 1
    in_cs[sum(1 for k in imgs if k in CSKEYS)] += 1
    PW = [g for g in G if all(g[x - 1] == x for x in C['L'])]
    pw_eq &= (set(St) == set(PW))
say(f"  stabilizer (unsigned lift) of each code space: {dict(res_u)}")
say(f"  equals the pointwise stabilizer of L (ledger's claim): {pw_eq}")
say(f"  orbit of a code space under the 168 unsigned lifts: sizes {dict(orbit_sizes)}; "
    f"how many images are code spaces: {dict(in_cs)}")
say("  -> under the unsigned lift GL(3,2) does NOT act on the set of 21 code spaces (orbit 42, half")
say("     of the images are not code spaces), so 168/|Stab| = 21 cannot hold for it.")
RES['unsigned'] = dict(stab=str(dict(res_u)), pw_equal=pw_eq, orbit=str(dict(orbit_sizes)),
                       images_that_are_codespaces=str(dict(in_cs)))

# ------------------------------------------------------------- H4 signed lifts (genuine automorphisms)
say(); say("=" * 78); say("H4. Signed CD lifts (sedenion automorphisms): action on the 21 code spaces"); say("=" * 78)
SL = []
for g in G:
    pi = perm_dict(g)
    for sg in product((1, -1), repeat=7):
        eps = dict(zip(PTS, sg))
        if octonion_signed_auto(pi, eps):
            for e8s in (1, -1):
                SL.append((g, sg, e8s, sed_lift_matrix(pi, eps, e8s)))
say(f"  signed lifts: {len(SL)}")
perm_ok = True
stab_imgs = []
for ci, C in enumerate(CS):
    St = []
    for (g, sg, e8s, P) in SL:
        k = image_key(P, C)
        if k not in CSKEYS:
            perm_ok = False
        if k == C['key']:
            St.append((g, sg, e8s))
        # flag equivariance: image code space has flag g(flag)
        if k in CSKEYS and CSKEYS[k] != act_flag(g, (C['m'], C['L'])):
            perm_ok = False
    imgG = sorted(set(s[0] for s in St))
    flagSt = [g for g in G if act_flag(g, (C['m'], C['L'])) == (C['m'], C['L'])]
    stab_imgs.append((len(St), len(imgG), iso_type(imgG)[0], set(imgG) == set(flagSt)))
    if ci == 0:
        orbitC = set(image_key(P, C) for (_, _, _, P) in SL)
        say(f"  orbit of C(m={C['m']}, L={sorted(C['L'])}) under the signed lifts: {len(orbitC)} code spaces")
say(f"  every signed lift maps code spaces to code spaces, equivariantly with the flag action: {perm_ok}")
say(f"  per code space: (|Stab| in the {len(SL)}-group, |image in PSL(2,7)|, type of image, image == flag stabilizer): "
    f"{dict(Counter(stab_imgs))}")
RES['signed'] = dict(n_lifts=len(SL), equivariant=perm_ok, stab=str(dict(Counter(stab_imgs))))

# ------------------------------------------------------------- H5 the 'negated orientation' family (§2.62.B Sign Duality)
say(); say("=" * 78); say("H5. §2.62.B 'Sign Duality': does the negated CD orientation give the same 21 spaces?"); say("=" * 78)
CSN = []
for m in PTS:
    lines = lines_through(m)
    pairs = [tuple(sorted(L - {m})) for L in lines]
    ks = []
    for (i, j) in pairs:
        s = -SED[i][j]
        x = basis(i); x[j + 8] += s
        ks.append(kernel_basis(x))
    for (u, w) in ((0, 1), (0, 2), (1, 2)):
        I = intersect(ks[u], ks[w])
        interior = sorted(set(idx for v in I for idx in range(1, 8) if v[idx]))
        CSN.append(dict(m=m, L=frozenset([m] + interior), basis=I, key=span_canon(I) if I else None,
                        dim=len(I)))
keysN = set(c['key'] for c in CSN if c['key'])
say(f"  negated-orientation intersections: dims {Counter(c['dim'] for c in CSN)}; "
    f"identical to the canonical 21: {keysN == set(CSKEYS)}; overlap with canonical: {len(keysN & set(CSKEYS))}")
# the other mixed sign triplets (should be trivial per §2.62.A)
mixed_dims = Counter()
for m in PTS:
    lines = lines_through(m)
    pairs = [tuple(sorted(L - {m})) for L in lines]
    base = [SED[i][j] for (i, j) in pairs]
    for flip in product((1, -1), repeat=3):
        if flip in ((1, 1, 1), (-1, -1, -1)):
            continue
        ks = []
        for (i, j), b, f in zip(pairs, base, flip):
            x = basis(i); x[j + 8] += b * f
            ks.append(kernel_basis(x))
        for (u, w) in ((0, 1), (0, 2), (1, 2)):
            mixed_dims[len(intersect(ks[u], ks[w]))] += 1
say(f"  the 6 mixed sign triplets per point: pairwise intersection dims {dict(mixed_dims)}")
FAM = dict(CSKEYS)
FAMN = {c['key']: (c['m'], c['L']) for c in CSN if c['key']}
ALL42 = set(FAM) | set(FAMN)
# unsigned-lift orbit == both families?
C0 = CS[0]
orbU = set(image_key(P, C0) for (g, P) in UL)
say(f"  unsigned-lift orbit of C0 (42 spaces) == canonical 21 + negated 21: {orbU == ALL42}")
orbS = set(image_key(P, C0) for (_, _, _, P) in SL)
say(f"  signed-lift orbit of C0 (42 spaces) == canonical 21 + negated 21: {orbS == ALL42}")
# subgroup of signed lifts preserving the canonical family; its action
pres = []
for (g, sg, e8s, P) in SL:
    if all(image_key(P, C) in FAM for C in CS):
        pres.append((g, sg, e8s, P))
say(f"  signed lifts preserving the canonical 21-family: {len(pres)} (index {len(SL)//max(1,len(pres))}); "
    f"e8-sign of those: {dict(Counter(e for (_,_,e,_) in pres))}")
eqv = all(FAM[image_key(P, C)] == act_flag(g, (C['m'], C['L'])) for (g, sg, e8s, P) in pres for C in CS)
say(f"  on the canonical family these act through the flag action (equivariant): {eqv}")
kern = [(g, sg, e8s) for (g, sg, e8s, P) in pres if g == tuple(PTS)]
say(f"  of these, lifts of the identity collineation (they fix every code space): {len(kern)}")
st_pres = Counter()
for C in CS:
    St = [g for (g, sg, e8s, P) in pres if image_key(P, C) == C['key']]
    imgG = sorted(set(St))
    st_pres[(len(St), len(imgG), iso_type(imgG)[0])] += 1
say(f"  within that subgroup: (|Stab C|, |image in PSL(2,7)|, type): {dict(st_pres)}  -> "
    f"{len(pres)}/{len(CS)} = {len(pres)//21} per code space, image order 8 = flag stabilizer")
# H6: the 42 = (flag, sign-family) picture under the unsigned lift
say(); say("=" * 78); say("H6. Unsigned lift on the 42 spaces = 21 flags x {canonical, negated}"); say("=" * 78)
LAB = {}
for k, f in FAM.items(): LAB[k] = (f, '+')
for k, f in FAMN.items(): LAB[k] = (f, '-')
eq42 = True; pairstab_ok = True; swapcoset_ok = True
for C in CS:
    f = (C['m'], C['L'])
    Cneg = [c for c in CSN if (c['m'], c['L']) == f][0]
    pair = {C['key'], Cneg['key']}
    Spair = []
    for g, P in UL:
        k = image_key(P, C)
        if k not in LAB or LAB[k][0] != act_flag(g, f):
            eq42 = False
        if k in pair:
            Spair.append(g)
    flagSt = [g for g in G if act_flag(g, f) == f]
    pairstab_ok &= (set(Spair) == set(flagSt))
    PW = [g for g in G if all(g[x - 1] == x for x in C['L'])]
    swap = [g for g in flagSt if image_key(UL[G.index(g)][1], C) == Cneg['key']]
    swapcoset_ok &= (set(swap) == set(flagSt) - set(PW))
say(f"  every unsigned-lift image of a code space is a (flag, sign) space with flag = g(flag): {eq42}")
say(f"  the set of g mapping C+(f) into {{C+(f), C-(f)}} == flag stabilizer D4 (for all 21 f): {pairstab_ok}")
say(f"  D4 \\ V4 (the non-pointwise coset) swaps C+(f) <-> C-(f): {swapcoset_ok}")
say("  -> V4 = stabilizer of the single subspace under the unsigned lift (orbit 42 = 168/4);")
say("     D4 = flag stabilizer = stabilizer of the pair {C+(f), C-(f)} (orbit 21 = 168/8).")
e8p = [(g, sg, e8s, P) for (g, sg, e8s, P) in SL if e8s == 1]
orb1344 = set(image_key(P, C0) for (_, _, _, P) in e8p)
say(f"  orbit of C0 under the 1344 lifts with e8 -> +e8: {len(orb1344)} spaces")
RES['H6'] = dict(eq42=eq42, pair_stab_is_D4=pairstab_ok, D4_minus_V4_swaps=swapcoset_ok, orbit_1344=len(orb1344))
RES['negated_family_identical'] = (keysN == set(CSKEYS))
RES['negated_overlap'] = len(keysN & set(CSKEYS))
RES['family_preserving_lifts'] = len(pres)
RES['family_stab'] = str(dict(st_pres))

json.dump(RES, open("item_h_results.json", "w"), indent=1)
open("item_h_output.txt", "w").write("\n".join(OUT) + "\n")
