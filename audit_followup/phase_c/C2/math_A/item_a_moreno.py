"""
item_a_moreno.py -- C2 math_A item (a): OP-2.81.1 / OP-2.81.2, Moreno's criterion,
and the §2.68.8.1 doubling-axis argument (OP-2.67.1b(ii)).

Ledger definitions used (SQT_Master_Ledger_v4_93, §2.81 L2754-2763, op_2252_v3_v4.py):
  clean element  = sum_{i in S} eps_i e_i, S subset {1..15}, eps_i in {+1,-1},
                   counted modulo global sign (lead coefficient +1);  n = |S|.
  zero divisor   = rank(L_x) < 16 (left multiplication), L_x column j = x e_j.
Here ranks are EXACT over Z (flint fmpz_mat.rank), and additionally mod 911 / mod 103.

Moreno's criterion (sedenions A_4, arXiv:q-alg/9710013 Cor. 1.9, the norm argument
after Thm 2.7, Thm 2.9 with n=3): x = (a,b), a,b octonions, is a zero divisor iff
Re a = Re b = 0, |a| = |b| != 0, <a,b> = 0.  For a clean x:
  a-part support A = S cap {1..7},  b-part support B' = {j-8 : j in S, j>=9},
  Re b = eps_8 (if 8 in S), |a|^2 = |A|, |b|^2 = |B'| (+1 if 8 in S),
  <a,b> = sum_{i in A cap B'} eps_i eps_{i+8}.
"""
import sys, json, time
from itertools import combinations, product
from collections import Counter, defaultdict
from math import comb
import numpy as np
import flint
from sedcore import *

OUT = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)

RES = {}

# ======================================================================= A0
say("=" * 78)
say("A0. Table check")
say("=" * 78)
say("mismatches vs tools/sedenion_Fp.py MULT:", xcheck_tool_table())

def moreno_predict(S, eps):
    """S tuple of indices, eps tuple of signs (same length). Moreno criterion."""
    d = dict(zip(S, eps))
    if 8 in d:
        return False
    A = [i for i in S if 1 <= i <= 7]
    Bp = [j - 8 for j in S if 9 <= j <= 15]
    if len(A) == 0 or len(A) != len(Bp):
        return False
    dot = sum(d[i] * d[i + 8] for i in set(A) & set(Bp))
    return dot == 0

def predicted_count(n):
    if n % 2:
        return 0
    k = n // 2
    tot = 0
    for m in range(0, k + 1):
        if m % 2:
            continue
        tot += comb(7, k) * comb(k, m) * comb(7 - k, k - m) * 2 ** (2 * k - m) * comb(m, m // 2)
    return tot // 2

# ======================================================================= A1
say()
say("=" * 78)
say("A1. Exhaustive census of ALL clean elements, n = 1..15 (exact rank over Z)")
say("=" * 78)
t0 = time.time()
census = {}
mismatch_examples = []
zd_store = {}           # n -> list of (S, eps) for n<=6 (for later use)
p911_disagree = Counter()
for n in range(1, 16):
    total = 0
    zd = 0
    pred = 0
    agree = 0
    rank_dist = Counter()
    rank911_dist = Counter()
    rank103_dist = Counter()
    sign_list = [(1,) + s for s in product((1, -1), repeat=n - 1)]
    for S in combinations(range(1, 16), n):
        LB = LBASIS[list(S)]                       # (n,16,16)
        for eps in sign_list:
            M = np.tensordot(np.array(eps, dtype=np.int64), LB, axes=(0, 0))
            Ml = M.tolist()
            r = flint.fmpz_mat(Ml).rank()
            total += 1
            rank_dist[r] += 1
            is_zd = r < 16
            pr = moreno_predict(S, eps)
            zd += is_zd
            pred += pr
            if is_zd == pr:
                agree += 1
            elif len(mismatch_examples) < 10:
                mismatch_examples.append((S, eps, r, pr))
            if n <= 6 and is_zd:
                zd_store.setdefault(n, []).append((S, eps))
            if n <= 5:
                r9 = flint.nmod_mat(Ml, 911).rank()
                r3 = flint.nmod_mat(Ml, 103).rank()
                rank911_dist[r9] += 1
                rank103_dist[r3] += 1
                if r9 != r:
                    p911_disagree[n] += 1
    census[n] = dict(total=total, zd=zd, moreno_pred=pred, agree=agree,
                     formula=predicted_count(n),
                     rank_dist=dict(sorted(rank_dist.items())),
                     rank911=dict(sorted(rank911_dist.items())) if n <= 5 else None,
                     rank103=dict(sorted(rank103_dist.items())) if n <= 5 else None)
    say(f"  n={n:2d}: clean={total:8d}  ZD(exact)={zd:6d}  Moreno-pred={pred:6d}  "
        f"formula={predicted_count(n):6d}  agree={agree==total}  ranks={dict(sorted(rank_dist.items()))}"
        f"   [{time.time()-t0:.0f}s]")
    if n <= 5:
        say(f"         mod 911 ranks {dict(sorted(rank911_dist.items()))}; mod 103 ranks {dict(sorted(rank103_dist.items()))}")
tot_all = sum(c['total'] for c in census.values())
zd_all = sum(c['zd'] for c in census.values())
say(f"  TOTAL clean elements = {tot_all}  (expected (3^15-1)/2 = {(3**15-1)//2})")
say(f"  TOTAL clean ZDs      = {zd_all}")
say(f"  Moreno criterion == exact rank test on every element: {all(c['agree']==c['total'] for c in census.values())}")
say(f"  mismatch examples: {mismatch_examples}")
say(f"  ZDs at odd n: {sum(census[n]['zd'] for n in range(1,16,2))}")
say(f"  rank of every ZD (all n): {sorted(set(r for c in census.values() for r in c['rank_dist'] if r < 16))}")
say(f"  ledger table check (n=2..5 at p=911: 84, 0, 1764, 0): "
    f"{[census[n]['zd'] for n in (2,3,4,5)]}; mod-911 rank disagreements with exact: {dict(p911_disagree)}")
RES['A1_census'] = {str(k): v for k, v in census.items()}
RES['A1_total'] = tot_all
RES['A1_total_zd'] = zd_all

# ======================================================================= A2
say()
say("=" * 78)
say("A2. n = 4 kernel structure (OP-2.81.1): clean-vs-mixed split by Moreno type")
say("=" * 78)

def rref_kernel_mod(M, p):
    """Kernel basis exactly as op_2252_v3_v4.py does it (Gauss-Jordan over F_p)."""
    n = 16
    A = [[v % p for v in row] for row in M]
    piv_cols, r = [], 0
    for c in range(n):
        piv = next((i for i in range(r, n) if A[i][c] % p), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(v * inv) % p for v in A[r]]
        for i in range(n):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(n)]
        piv_cols.append(c); r += 1
        if r == n:
            break
    free = [c for c in range(n) if c not in piv_cols]
    ker = []
    for fc in free:
        v = [0] * n; v[fc] = 1
        for ri, pc in enumerate(piv_cols):
            v[pc] = (-A[ri][fc]) % p
        ker.append(v)
    return ker

def signed_terms(v, p):
    nz = [(i, v[i] % p) for i in range(16) if v[i] % p]
    if not nz:
        return None
    inv = pow(nz[0][1], p - 2, p)
    terms = []
    for i, c in nz:
        cc = (c * inv) % p
        if cc == 1: terms.append((i, 1))
        elif cc == p - 1: terms.append((i, -1))
        else: return None
    return terms

# all clean 2-term and 4-term vectors (mod sign) for the intrinsic test
clean2 = []
for S in combinations(range(1, 16), 2):
    for s in (1, -1):
        v = [0] * 16; v[S[0]] = 1; v[S[1]] = s; clean2.append(v)
clean4 = []
for S in combinations(range(1, 16), 4):
    for s in product((1, -1), repeat=3):
        v = [0] * 16; v[S[0]] = 1
        for t, ss in zip(S[1:], s): v[t] = ss
        clean4.append(v)
C2 = np.array(clean2, dtype=np.int64)      # (210,16)
C4 = np.array(clean4, dtype=np.int64)      # (10920,16)

def moreno_type(S, eps):
    A = set(i for i in S if i <= 7); Bp = set(j - 8 for j in S if j >= 9)
    return len(A & Bp)                       # overlap m

tab = Counter()
examples = {}
for (S, eps) in zd_store[4]:
    x = [0] * 16
    for i, e in zip(S, eps): x[i] = e
    M = Lmat(x)
    m = moreno_type(S, eps)
    ker = rref_kernel_mod(M.tolist(), 911)
    cl = [signed_terms(v, 911) for v in ker]
    rref_clean = all(c is not None for c in cl)
    rref_shape = tuple(sorted(len(c) if c else -1 for c in cl))
    # intrinsic: clean 2-/4-term vectors in ker (exact: M v = 0)
    in2 = C2[(C2 @ M.T == 0).all(axis=1)]
    in4 = C4[(C4 @ M.T == 0).all(axis=1)]
    span2 = flint.fmpz_mat(in2.tolist()).rank() if len(in2) else 0
    span24 = flint.fmpz_mat(np.vstack([in2, in4]).tolist()).rank() if len(in2) + len(in4) else 0
    key = (m, rref_clean, rref_shape, len(in2), span2, span24)
    tab[key] += 1
    examples.setdefault(key, (S, eps))
say("  key = (overlap m=|A cap B'|, RREF-basis-clean?, RREF basis term-counts, "
    "#clean 2-term in ker, rank of their span, rank of span of clean 2+4-term in ker)")
for key, cnt in sorted(tab.items(), key=lambda kv: (kv[0][0], -kv[1])):
    say(f"   {cnt:5d}  {key}   e.g. S={examples[key][0]} eps={examples[key][1]}")
RES['A2_n4_kernel_table'] = [[list(map(str, k)), v] for k, v in tab.items()]
# ledger examples
for S in [(1, 2, 9, 10), (1, 2, 12, 15)]:
    hits = [(S2, e2) for (S2, e2) in zd_store[4] if S2 == S]
    say(f"  ledger example support {S}: {len(hits)} ZD sign patterns; Moreno overlap m = "
        f"{moreno_type(S, (1,1,1,1))}")

# ======================================================================= A3
say()
say("=" * 78)
say("A3. §2.68.8.1 doubling-axis argument")
say("=" * 78)
# (a) the dichotomy as stated
dich = []
for a in PTS:
    for b in PTS:
        k, s = mul_basis(a, b + 8)
        dich.append((a, b, k, s))
on_axis = [(a, b) for (a, b, k, s) in dich if k in (0, 8)]
say(f"  (a) e_a e_(b+8) lands on <e0,e8> exactly for a=b: {sorted(on_axis) == [(a,a) for a in PTS]}; "
    f"value for a=b: {set((k,s) for (a,b,k,s) in dich if a==b)} (= -e8);  "
    f"a!=b lands in 9..15: {all(9<=k<=15 for (a,b,k,s) in dich if a!=b)}")
# (b) which products appear in (e_a+e_b)(e_c+e_d)
say("  (b) (e_a+e_b)(e_c+e_d) = e_a e_c + e_a e_d + e_b e_c + e_b e_d : the product e_a e_b of the")
say("      two components of ONE factor is not a term; for x = e_a + e_(a+8) the internal product")
say("      e_a e_(a+8) = -e8 never enters x*y unless y itself contains e_a or e_(a+8).")
# (c) ZD-participating basis elements whose product lands on e8
pairs_to_e8 = [(i, i ^ 8, SED[i][i ^ 8]) for i in range(1, 16) if i != 8]
assessors = [(a, b + 8) for a in PTS for b in PTS if a != b]
part = sorted(set(i for t in assessors for i in t))
say(f"  (c) indices used by the 42 assessors: {part} (all of 1..15 except 8)")
say(f"      every i in that set has e_i e_(i^8) = +-e8: {[(i,j,s) for (i,j,s) in pairs_to_e8]}")
say(f"      e.g. e1 (in ZD e1+e10) times e9 (in ZD e9+e2): e1 e9 = {SED[1][9]:+d} e8;"
    f"  e10 e2 = {SED[10][2]:+d} e8")
# (d) genuine zero products whose e8 component receives cancelling terms
found = []
n_found = Counter()
for n in (2, 4):
    for (S, eps) in zd_store[n]:
        x = [0] * 16
        for i, e in zip(S, eps): x[i] = e
        M = Lmat(x)
        for C in (C2, C4):
            ker_vecs = C[(C @ M.T == 0).all(axis=1)]
            for y in ker_vecs:
                ys = [j for j in range(16) if y[j]]
                contrib = [(i, j, SED[i][j] * x[i] * int(y[j])) for i in S for j in ys if i ^ j == 8]
                if len(contrib) >= 2:
                    n_found[(n, len(ys))] += 1
                    if len(found) < 50:
                        found.append((tuple(S), tuple(eps), tuple(int(t) for t in y), contrib))
say(f"  (d) clean ZD pairs (x, y) with x y = 0 whose e8-component receives >= 2 nonzero terms "
    f"(which therefore cancel): {sum(n_found.values())} found, by (n_x, n_y): {dict(n_found)}"
    f" (search over clean n=2,4 ZDs x and clean 2/4-term y in ker L_x)")
for f in found[:3]:
    S, eps, y, contrib = f
    xs = " ".join(f"{'+' if e>0 else '-'}e{i}" for i, e in zip(S, eps))
    ysr = " ".join(f"{'+' if y[j]>0 else '-'}e{j}" for j in range(16) if y[j])
    prod = mul([dict(zip(S, eps)).get(i, 0) for i in range(16)], list(y))
    say(f"      x = {xs} ;  y = {ysr} ;  e8-terms {contrib} ;  x*y == 0: {all(v==0 for v in prod)}")
n2_e8 = sum(v for (nx, ny), v in n_found.items() if nx == 2)
say(f"      of these, with x two-term: {n2_e8}")
# (e) identity-edge elements are not ZDs; Moreno reason
idr = {}
for a in PTS:
    for s in (1, -1):
        x = [0] * 16; x[a] = 1; x[a + 8] = s
        idr[(a, s)] = exact_rank(Lmat(x))
say(f"  (e) rank L_x for x = e_a +- e_(a+8), a=1..7: {set(idr.values())} (16 = not a ZD); "
    f"Moreno: (a-part, b-part) = (e_a, +-e_a) not orthogonal")
# (f) 'unique 2D subspace with no Moreno-form ZDs' : test a few other 2D subspaces
def plane_has_clean_zd(i, j):
    zds = []
    for s in (1, -1):
        x = [0] * 16; x[i] = 1; x[j] = s
        if exact_rank(Lmat(x)) < 16:
            zds.append(s)
    return zds
others = [(1, 2), (1, 9), (3, 11), (0, 1), (9, 10)]
say(f"  (f) 2D coordinate planes span(e_i,e_j) and whether e_i +- e_j is a ZD: "
    f"{[(p, plane_has_clean_zd(*p)) for p in others]}")
say("      span(e_i,e_j) with i,j <= 7 lies in the octonions (division algebra): no ZD at all;")
say("      so <e0,e8> is not 'the unique 2-dimensional subspace containing no Moreno-form ZDs'.")
RES['A3'] = dict(dichotomy_ok=sorted(on_axis) == [(a, a) for a in PTS],
                 e8_cancel_pairs_found=sum(n_found.values()),
                 e8_cancel_by_nx_ny={str(k): v for k, v in n_found.items()},
                 e8_cancel_with_two_term_x=n2_e8,
                 identity_edge_ranks=sorted(set(idr.values())))

# ======================================================================= A4
say()
say("=" * 78)
say("A4. Moreno criterion on NON-clean integer sedenions (random sanity, exact)")
say("=" * 78)
rng = np.random.default_rng(20261007)
ok_suff = 0; ok_nec = 0; NS = 300
for t in range(NS):
    # sufficiency: x = (u, e_k u) with u pure, u_k = 0  -> ZD expected
    k = int(rng.integers(1, 8))
    u = [0] + [int(v) for v in rng.integers(-3, 4, size=7)]
    u[k] = 0
    if all(v == 0 for v in u):
        u[1 if k != 1 else 2] = 1
    b = mul(basis(k)[:8] + [0] * 8, u + [0] * 8)[:8]       # e_k u in octonions
    x = u + b
    if exact_rank(Lmat(x)) < 16:
        ok_suff += 1
    # necessity: random integer x -> if singular, criterion must hold
    y = [int(v) for v in rng.integers(-2, 3, size=16)]
    sing = exact_rank(Lmat(y)) < 16
    a_, b_ = y[:8], y[8:]
    crit = (a_[0] == 0 and b_[0] == 0 and sum(v*v for v in a_) == sum(v*v for v in b_) != 0
            and sum(p*q for p, q in zip(a_[1:], b_[1:])) == 0)
    if sing == crit:
        ok_nec += 1
say(f"  sufficiency: {ok_suff}/{NS} constructed (u, e_k u) are ZDs")
say(f"  random integer elements: criterion == singularity in {ok_nec}/{NS}")
RES['A4'] = dict(suff=ok_suff, nec=ok_nec, N=NS)

json.dump(RES, open("item_a_results.json", "w"), indent=1, default=str)
open("item_a_output.txt", "w").write("\n".join(OUT) + "\n")
say("wrote item_a_output.txt, item_a_results.json")
