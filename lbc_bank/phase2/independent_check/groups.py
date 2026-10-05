"""Independent check of Claim 2: subgroups of PSL(2,7) and SL(2,7), built from scratch over F_7."""
import itertools
from collections import Counter

p = 7

def mul(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return ((a*e + b*g) % p, (a*f + b*h) % p, (c*e + d*g) % p, (c*f + d*h) % p)

I = (1, 0, 0, 1)
negI = (p-1, 0, 0, p-1)

SL = [m for m in itertools.product(range(p), repeat=4) if (m[0]*m[3] - m[1]*m[2]) % p == 1]
print("|SL(2,7)| =", len(SL))

def neg(A):
    return tuple((-x) % p for x in A)

# PSL elements: canonical representative of {A, -A}
def canon(A):
    return min(A, neg(A))

PSL = sorted({canon(A) for A in SL})
print("|PSL(2,7)| =", len(PSL))

def pmul(A, B):
    return canon(mul(A, B))

def order(A, mulf, e):
    k, X = 1, A
    while X != e:
        X = mulf(X, A)
        k += 1
    return k

def inv(A, mulf, e):
    o = order(A, mulf, e)
    X = e
    for _ in range(o - 1):
        X = mulf(X, A)
    return X

ePSL = canon(I)
print("PSL element-order stats:", sorted(Counter(order(A, pmul, ePSL) for A in PSL).items()))
print("SL  element-order stats:", sorted(Counter(order(A, mul, I) for A in SL).items()))

def gen_subgroup(gens, mulf, e):
    S = {e}
    frontier = [e]
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                y = mulf(x, g)
                if y not in S:
                    S.add(y)
                    new.append(y)
        frontier = new
    return frozenset(S)

# ---------------- Q8 test ----------------
def is_Q8(H, mulf, e):
    if len(H) != 8:
        return False
    oc = Counter(order(x, mulf, e) for x in H)
    return oc == Counter({1: 1, 2: 1, 4: 6})

def all_subgroups_order(n, G, mulf, e, max_gens=2):
    subs = set()
    for gs in itertools.combinations(G, max_gens):
        H = gen_subgroup(gs, mulf, e)
        if len(H) == n:
            subs.add(H)
    for g in G:
        H = gen_subgroup([g], mulf, e)
        if len(H) == n:
            subs.add(H)
    return subs

# Every group of order 8 is 2-generated, so 2-generated subgroups cover all order-8 subgroups.
subs8 = all_subgroups_order(8, PSL, pmul, ePSL)
print("PSL: # subgroups of order 8 =", len(subs8))
types8 = Counter(tuple(sorted(Counter(order(x, pmul, ePSL) for x in H).items())) for H in subs8)
print("PSL: order-8 subgroup element-order types:", types8)
print("PSL: any Q8?", any(is_Q8(H, pmul, ePSL) for H in subs8))

# Square-root test: Q8 needs 6 order-4 elements squaring to one involution
invols = [A for A in PSL if order(A, pmul, ePSL) == 2]
max_roots = max(sum(1 for x in PSL if order(x, pmul, ePSL) == 4 and pmul(x, x) == u) for u in invols)
print("PSL: max # order-4 square roots of any involution =", max_roots, "(Q8 would need 6)")

# SL(2,7) contains Q8
i_ = (0, p-1, 1, 0)
j_ = (3, 2, 2, 4)
Q = gen_subgroup([i_, j_], mul, I)
print("SL: <i,j> order", len(Q), "is Q8:", is_Q8(Q, mul, I),
      "i^2=-I:", mul(i_, i_) == negI, "j^2=-I:", mul(j_, j_) == negI,
      "ij = -ji:", mul(i_, j_) == neg(mul(j_, i_)))
subs8SL = all_subgroups_order(8, SL, mul, I)
print("SL: # subgroups of order 8 =", len(subs8SL), " # that are Q8:", sum(is_Q8(H, mul, I) for H in subs8SL))

# ---------------- A4 and S4 ----------------
def sylow3_action_faithful(H, mulf, e):
    """Return (#Sylow-3 subgroups, kernel size) of conjugation action of H on its Sylow 3-subgroups."""
    syl = list({gen_subgroup([x], mulf, e) for x in H if order(x, mulf, e) == 3})
    def conj(g, S):
        gi = inv(g, mulf, e)
        return frozenset(mulf(mulf(g, s), gi) for s in S)
    kernel = [g for g in H if all(conj(g, S) == S for S in syl)]
    return len(syl), len(kernel)

subs12 = all_subgroups_order(12, PSL, pmul, ePSL)
subs24 = all_subgroups_order(24, PSL, pmul, ePSL)
print("PSL: # subgroups of order 12 =", len(subs12), " order 24 =", len(subs24))
for name, subs in [("12", subs12), ("24", subs24)]:
    stats = Counter()
    for H in subs:
        nsyl, ker = sylow3_action_faithful(H, pmul, ePSL)
        oc = tuple(sorted(Counter(order(x, pmul, ePSL) for x in H).items()))
        stats[(nsyl, ker, oc)] += 1
    print(" order", name, "-> (#Syl3, kernel size, element-order stats): count", dict(stats))
# A group of order 24 acting faithfully on 4 objects is S4; order 12 acting faithfully on 4 objects is A4 (unique index-2 subgroup of S4).
