"""
second_leg_checks.py -- independent recomputation of the decisive facts for the reversal-type
items (C2_PREREG 'M-rev': items a[§2.68.8.1], b, d, h) plus j, using DIFFERENT code paths:
  * products from tools/sedenion_Fp.py (MULT / mul_vec mod 911), not sedcore.SED;
  * ranks/kernels by a plain-Python Gauss-Jordan mod 911 (as the ledger's scripts do), not flint;
  * groups via sympy.combinatorics (GL(3,2) generated from two matrices; isomorphism tests).
"""
import sys, io, contextlib, json
from itertools import combinations, product, permutations
from collections import Counter
sys.path.insert(0, "/home/claude/gifgaf0.github.io/tools")
with contextlib.redirect_stdout(io.StringIO()):
    import sedenion_Fp as T
sys.path.pop(0)
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import DihedralGroup
from sympy.combinatorics.homomorphisms import is_isomorphic

p = 911
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
R = {}
def bv(i, c=1):
    v = [0] * 16; v[i] = c % p; return v
def add(*vs):
    return [sum(x) % p for x in zip(*vs)]
def mulv(x, y): return T.mul_vec(x, y, p)
def lmat(x):
    cols = [mulv(x, bv(j)) for j in range(16)]
    return [[cols[j][i] for j in range(16)] for i in range(16)]
def rref(M):
    A = [r[:] for r in M]; rows = len(A); cols = len(A[0]); r = 0; piv = []
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i][c] % p), None)
        if pr is None: continue
        A[r], A[pr] = A[pr], A[r]; inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] % p:
                f = A[i][c]; A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(cols)]
        piv.append(c); r += 1
        if r == rows: break
    return A, piv
def rank(M): return len(rref(M)[1])
def kernel(M):
    A, piv = rref(M); n = len(M[0]); out = []
    for fc in [c for c in range(n) if c not in piv]:
        v = [0] * n; v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-A[i][fc]) % p
        out.append(v)
    return out
def T_(M): return [list(r) for r in zip(*M)]
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(16)) % p for j in range(len(B[0]))] for i in range(16)]
def sign_of(i, j):
    (k, s), = T.MULT[i][j]; return k, s

# ---------------------------------------------------------------- (a) §2.68.8.1 and the n=6 count
say("== (a) second leg ==")
dich = all((sign_of(a, b + 8)[0] in (0, 8)) == (a == b) for a in range(1, 8) for b in range(1, 8))
say(f"  dichotomy e_a e_(b+8) in <e0,e8> iff a=b (tool table): {dich}")
x = add(bv(1), bv(2), bv(11), bv(12)); y = add(bv(3), bv(4, -1), bv(13), bv(14, -1))
e8terms = [(i, j, sign_of(i, j)[1] * (x[i] if x[i] < p // 2 else x[i] - p) * (y[j] if y[j] < p // 2 else y[j] - p))
           for i in range(16) for j in range(16) if x[i] and y[j] and i ^ j == 8]
say(f"  x=e1+e2+e11+e12, y=e3-e4+e13-e14: x*y == 0 mod 911: {all(v == 0 for v in mulv(x, y))}; e8 terms {e8terms}")
say(f"  rank L_(e_a +- e_(a+8)) mod 911: {set(rank(lmat(add(bv(a), bv(a+8, s)))) for a in range(1,8) for s in (1,-1))}")
cnt = Counter()
for n in (4, 5, 6):
    z = 0
    for S in combinations(range(1, 16), n):
        for sg in product((1, -1), repeat=n - 1):
            v = bv(S[0])
            for t, s in zip(S[1:], sg): v[t] = s % p
            if rank(lmat(v)) < 16: z += 1
    cnt[n] = z
    say(f"  clean n={n}: ZDs (tool table, plain Gauss-Jordan mod 911) = {z}")
R['a'] = dict(dichotomy=dich, counts={str(k): v for k, v in cnt.items()})

# ---------------------------------------------------------------- (d) 651 and the 42
say("== (d) second leg ==")
m2 = 0
for A2 in combinations(range(1, 8), 2):
    for B2 in combinations(range(1, 8), 2):
        for (u, w) in ((B2[0], B2[1]), (B2[1], B2[0])):
            if A2[0] != u and A2[1] != w: m2 += 1
say(f"  size-2 matchings of K77-M (choose 2 A-vertices, 2 B-vertices, a non-identity bijection): {m2}")
quads = []
cross = [(i, j) for i in range(1, 8) for j in range(9, 16)]
for L, Rr in combinations(cross, 2):
    if all(v == 0 for v in mulv(add(bv(L[0]), bv(L[1])), add(bv(Rr[0]), bv(Rr[1])))):
        quads.append((L, Rr))
lines7 = set(frozenset((i, j, i ^ j)) for i in range(1, 8) for j in range(1, 8) if i < j)
lc = set(frozenset(set(range(1, 8)) - set(l)) for l in lines7)
say(f"  ++ quadruples: {len(quads)}; all disjoint edge pairs with 4 labels = a Fano-line complement: "
    f"{all(frozenset({L[0], L[1]-8, Rr[0], Rr[1]-8}) in lc and L[0] != Rr[0] and L[1] != Rr[1] for L, Rr in quads)}")
R['d'] = dict(m2=m2, quads=len(quads))

# ---------------------------------------------------------------- (h) flag stabilizer and code spaces
say("== (h) second leg ==")
def mat_perm(M):
    img = []
    for v in range(1, 8):
        b = [(v >> 2) & 1, (v >> 1) & 1, v & 1]
        r = [sum(M[k][t] * b[t] for t in range(3)) % 2 for k in range(3)]
        img.append(r[0] * 4 + r[1] * 2 + r[2])
    return Permutation([0] + img)
Gs = PermutationGroup(mat_perm([[1, 1, 0], [0, 1, 0], [0, 0, 1]]), mat_perm([[0, 1, 0], [0, 0, 1], [1, 0, 0]]))
say(f"  sympy GL(3,2) order: {Gs.order()}")
els = list(Gs.elements)
flag = (1, frozenset((1, 2, 3)))
St = [g for g in els if g(1) == 1 and frozenset(g(i) for i in flag[1]) == flag[1]]
H = PermutationGroup(St)
hod = dict(sorted(Counter(g.order() for g in H.elements).items()))
say(f"  flag (1,{{1,2,3}}) stabilizer: order {H.order()}, abelian {H.is_abelian}, element orders {hod}; "
    f"sympy is_isomorphic(D4, H) = {is_isomorphic(DihedralGroup(4), H)} "
    f"(is_isomorphic(H, D4) = {is_isomorphic(H, DihedralGroup(4))}: sympy's test is not symmetric here)")
say(f"  classification: order 8, non-abelian, 5 involutions (Q8 has 1) -> D4: "
    f"{H.order() == 8 and not H.is_abelian and hod.get(2, 0) == 5}")
PW = PermutationGroup([g for g in els if all(g(i) == i for i in flag[1])])
say(f"  pointwise stabilizer of {{1,2,3}}: order {PW.order()}, abelian {PW.is_abelian}")
# code space C(m=1, flag line {1,2,3}) via tool table, then unsigned-lift stabilizer and orbit size
def cs_for(m, use_neg=False):
    ls = sorted([l for l in lines7 if m in l], key=lambda s: sorted(s))
    ks = []
    for l in ls:
        i, j = sorted(l - {m})
        k, s = sign_of(i, j); s = -s if use_neg else s
        ks.append(kernel(lmat(add(bv(i), bv(j + 8, s)))))
    out = []
    for (u, w) in ((0, 1), (0, 2), (1, 2)):
        Mx = T_(ks[u] + [[(-c) % p for c in v] for v in ks[w]])
        ker = kernel(Mx)
        vecs = [[sum(c[t] * ks[u][t][r] for t in range(len(ks[u]))) % p for r in range(16)] for c in ker]
        A, piv = rref(vecs); out.append(tuple(tuple(r) for r in A[:len(piv)]))
    return out
def canon(vecs):
    A, piv = rref([list(v) for v in vecs]); return tuple(tuple(r) for r in A[:len(piv)])
CSp = [c for m in range(1, 8) for c in cs_for(m)]
CSn = [c for m in range(1, 8) for c in cs_for(m, True)]
say(f"  canonical code spaces {len(set(CSp))}, negated-orientation spaces {len(set(CSn))}, common: {len(set(CSp) & set(CSn))}")
C0 = CSp[0]
def lift_apply(g, v):
    w = [0] * 16; w[0] = v[0]; w[8] = v[8]
    for i in range(1, 8):
        w[g(i)] = v[i]; w[g(i) + 8] = v[i + 8]
    return w
imgs = Counter(canon([lift_apply(g, v) for v in C0]) for g in els)
stab_u = imgs[C0]
say(f"  unsigned-lift orbit of C(m=1, first pair): {len(imgs)} spaces; stabilizer order {stab_u}; "
    f"orbit == canonical+negated: {set(imgs) == set(CSp) | set(CSn)}")
R['h'] = dict(flag_stab=H.order(), D4=bool(H.order() == 8 and not H.is_abelian and hod.get(2, 0) == 5),
              sympy_iso_D4_H=bool(is_isomorphic(DihedralGroup(4), H)), unsigned_orbit=len(imgs),
              unsigned_stab=stab_u, negated_common=len(set(CSp) & set(CSn)))

# ---------------------------------------------------------------- (b) signed automorphisms via the tool table
say("== (b) second leg ==")
def oct_sign(i, j): return sign_of(i, j)[1]
auts = []
for img in permutations(range(1, 8)):
    pi = (0,) + img
    if any(pi[i] ^ pi[j] != pi[i ^ j] for i in range(1, 8) for j in range(1, 8) if i != j): continue
    for sg in product((1, -1), repeat=7):
        e = (1,) + sg
        if all(oct_sign(i, j) * e[i ^ j] == e[i] * e[j] * oct_sign(pi[i], pi[j])
               for i in range(1, 8) for j in range(1, 8) if i != j):
            auts.append((pi, e))
say(f"  signed octonion automorphisms (tool table): {len(auts)}; per collineation: {set(Counter(a[0] for a in auts).values())}; "
    f"unsigned: {sum(1 for a in auts if all(s == 1 for s in a[1]))}")
def comp(g, h):
    (gp, ge), (hp, he) = g, h
    return (tuple(gp[hp[i]] for i in range(8)), tuple(he[i] * ge[hp[i]] for i in range(8)))
ID = (tuple(range(8)), (1,) * 8)
def order(g):
    k, c = 1, g
    while c != ID: c = comp(g, c); k += 1
    return k
od = Counter(order(g) for g in auts)
say(f"  element orders: {dict(sorted(od.items()))}; elements of order 8 exist -> not AGL(3,2)/its dual "
    f"(where (v,g)^4 = ((1+g)^3 v, 1) = 1), hence the extension 2^3.PSL(2,7) is NON-split: {od.get(8,0) > 0}")
# YB with a plain-Python implementation
def yb(v1, v2):
    A = lmat(v1); B = lmat(v2)
    ABA = mm(mm(A, B), A); BAB = mm(mm(B, A), B)
    D = [[(ABA[i][j] - BAB[i][j]) % p for j in range(16)] for i in range(16)]
    K = kernel(D)
    if not K: return False
    base = rank(K)
    for X in (A, B):
        if rank(K + [[sum(X[i][k] * v[k] for k in range(16)) % p for i in range(16)] for v in K]) != base: return False
    for v in K:
        ABv = [sum(A[i][k] * sum(B[k][l] * v[l] for l in range(16)) for k in range(16)) % p for i in range(16)]
        BAv = [sum(B[i][k] * sum(A[k][l] * v[l] for l in range(16)) for k in range(16)) % p for i in range(16)]
        if ABv != BAv: return True
    return False
roots = [(a, b) for a in range(1, 8) for b in range(9, 16) if b != a + 8]
Yplus = set(); YE = set()
for t1, t2 in combinations(roots, 2):
    anyyb = False
    for s1, s2, tt in product((1, -1), repeat=3):
        r = yb(add(bv(t1[0]), bv(t1[1], s1)), [(tt * c) % p for c in add(bv(t2[0]), bv(t2[1], s2))])
        if r:
            anyyb = True
            if (s1, s2, tt) == (1, 1, 1): Yplus.add(frozenset((t1, t2)))
    if anyyb: YE.add(frozenset((t1, t2)))
def act(g, pair):
    return frozenset(tuple(sorted((g(t[0]), g(t[1] - 8) + 8))) for t in pair)
pY = sum(all(act(g, q) in Yplus for q in Yplus) for g in els)
pYE = sum(all(act(g, q) in YE for q in YE) for g in els)
say(f"  Y (all-plus) = {len(Yplus)} pairs, preserved by {pY}/168 collineations; sign-blind Y^E = {len(YE)} pairs, preserved by {pYE}/168")
R['b'] = dict(auts=len(auts), order8=od.get(8, 0), Y=len(Yplus), YE=len(YE), presY=pY, presYE=pYE)

# ---------------------------------------------------------------- (j) TS_O1 sign
say("== (j) second leg ==")
F21 = [a for a in auts if all(s == 1 for s in a[1])]
def tw_img(a, t): return frozenset((a[0][t[0]], a[0][t[1] - 8] + 8))
orb = lambda t: frozenset(tw_img(a, t) for a in F21)
O1 = orb((1, 14)); O2 = orb((2, 13))
say(f"  TS_O1 size {len(O1)}: signs of e_a e_b = {dict(Counter(oct_sign(*sorted(t)) if False else sign_of(*sorted(t))[1] for t in O1))}; "
    f"TS_O2 size {len(O2)}: {dict(Counter(sign_of(*sorted(t))[1] for t in O2))}")
R['j'] = dict(O1=dict(Counter(sign_of(*sorted(t))[1] for t in O1)), O2=dict(Counter(sign_of(*sorted(t))[1] for t in O2)))
json.dump(R, open("second_leg_results.json", "w"), indent=1, default=str)
open("second_leg_output.txt", "w").write("\n".join(OUT) + "\n")
