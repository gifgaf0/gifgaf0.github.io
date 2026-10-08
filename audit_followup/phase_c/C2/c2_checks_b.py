#!/usr/bin/env python3
"""C2 second computation for M-rev items (b) and (c), written in this session without reading the math_A / math_B code.

(b) Signed vs unsigned Fano lifts. For each of the 168 collineations π of PG(2,2) (permutations of {1..7} with
    π(i⊕j) = π(i)⊕π(j), the octonion table being e_i·e_j = ±e_{i⊕j}), count the sign vectors ε ∈ {±1}^7 for which
    e_i ↦ ε_i·e_{π(i)} is an octonion automorphism; count those that work with ε = (+…+); and, unsigned, count how many of
    the 7 line orientations each π reverses (an anti-automorphism would reverse all 7).
    A Cayley–Dickson extension (a, b) ↦ (φa, φb) of an octonion automorphism φ is a sedenion automorphism (φ commutes with
    conjugation), so every signed lift also preserves every zero product, hence the annihilation graph of §2.41.B. This
    is checked directly on the 84 two-term cross-copy zero divisors.
(c) The 42 order-4 elements of SL(2,7) generate the whole group, so by Burnside's theorem their images under the
    irreducible 4-dimensional representation σ₄ generate all of M₄(ℂ).
Sedenion table: tools/sedenion_Fp.py (MULT), imported unchanged.
"""
import contextlib, io, itertools, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
with contextlib.redirect_stdout(io.StringIO()):
    from sedenion_Fp import MULT                     # noqa: E402

out = {}


def prod_basis(a, c):
    """e_a · e_c as (index, sign) from the program's table (single term for basis elements)."""
    terms = MULT[a][c]
    assert len(terms) == 1
    return terms[0]


# octonion structure constants s(i, j), e_i e_j = s(i, j) e_{i xor j}, i, j in 1..7, i != j
s = {}
for i in range(1, 8):
    for j in range(1, 8):
        if i != j:
            k, sg = prod_basis(i, j)
            assert k == i ^ j
            s[(i, j)] = sg

# collineations of PG(2,2) on F_2^3 \ {0} = {1..7}
coll = [p for p in itertools.permutations(range(1, 8))
        if all(p[(i ^ j) - 1] == p[i - 1] ^ p[j - 1] for i in range(1, 8) for j in range(1, 8) if i != j)]
assert len(coll) == 168
lines = sorted({tuple(sorted((i, j, i ^ j))) for i in range(1, 8) for j in range(1, 8) if i != j})
assert len(lines) == 7

per_pi, unsigned_ok, reversed_counts = [], 0, {}
for p in coll:
    P = lambda i: p[i - 1]                            # noqa: E731
    n_eps = 0
    for eps in itertools.product((1, -1), repeat=7):
        E = lambda i: eps[i - 1]                      # noqa: E731
        if all(E(i) * E(j) * s[(P(i), P(j))] == s[(i, j)] * E(i ^ j) for (i, j) in s):
            n_eps += 1
    per_pi.append(n_eps)
    if all(s[(P(i), P(j))] == s[(i, j)] for (i, j) in s):
        unsigned_ok += 1
    rev = sum(1 for (a, b, c) in lines if s[(P(a), P(b))] != s[(a, b)])
    reversed_counts[rev] = reversed_counts.get(rev, 0) + 1
out["b"] = {"collineations": len(coll), "sign_vectors_per_collineation": sorted(set(per_pi)),
            "signed_automorphisms_total": sum(per_pi), "unsigned_automorphisms": unsigned_ok,
            "line_orientations_reversed_unsigned_histogram": dict(sorted(reversed_counts.items()))}

# signed lifts preserve the annihilation graph on the 84 two-term cross-copy zero divisors e_a ± e_{b+8}
def smul(x, y):
    r = [0] * 16
    for a in range(16):
        if x[a]:
            for c in range(16):
                if y[c]:
                    for (k, sg) in MULT[a][c]:
                        r[k] += sg * x[a] * y[c]
    return r


zds = []
for a in range(1, 8):
    for b in range(1, 8):
        if a != b:
            for sg in (1, -1):
                v = [0] * 16
                v[a], v[b + 8] = 1, sg
                zds.append(tuple(v))
# keep those with a nonzero annihilator among the candidates (the two-term cross-copy zero divisors)
ann = {(x, y) for x in zds for y in zds if x < y and not any(smul(list(x), list(y)))}
zd_set = sorted({x for e in ann for x in e})
out["b"]["two_term_cross_copy_zds_in_annihilating_pairs"] = len(zd_set)
out["b"]["annihilating_unordered_pairs"] = len(ann)


def lift(p, eps, e8):
    """Signed CD lift: e_i -> eps_i e_p(i), e_{i+8} -> e8*eps_i e_{p(i)+8}; returns a function on vectors."""
    def f(v):
        w = [0] * 16
        w[0] = v[0]
        w[8] = e8 * v[8]
        for i in range(1, 8):
            w[p[i - 1]] += eps[i - 1] * v[i]
            w[p[i - 1] + 8] += e8 * eps[i - 1] * v[i + 8]
        return tuple(w)
    return f


def canon(v):
    """Representative of ±v (zero divisors are counted up to sign)."""
    nz = next(x for x in v if x)
    return tuple(-x for x in v) if nz < 0 else v


ann_c = {frozenset((canon(x), canon(y))) for (x, y) in ann}
preserve, tested = 0, 0
for p in coll:
    for eps in itertools.product((1, -1), repeat=7):
        P = lambda i: p[i - 1]                        # noqa: E731
        E = lambda i: eps[i - 1]                      # noqa: E731
        if not all(E(i) * E(j) * s[(P(i), P(j))] == s[(i, j)] * E(i ^ j) for (i, j) in s):
            continue
        for e8 in (1, -1):
            f = lift(p, eps, e8)
            tested += 1
            img = {frozenset((canon(f(x)), canon(f(y)))) for (x, y) in ann}
            preserve += img == ann_c
out["b"]["signed_CD_lifts_tested"] = tested
out["b"]["signed_CD_lifts_preserving_annihilation_graph"] = preserve
unsigned_preserve = 0
for p in coll:
    f = lift(p, (1,) * 7, 1)
    img = {frozenset((canon(f(x)), canon(f(y)))) for (x, y) in ann}
    unsigned_preserve += img == ann_c
out["b"]["unsigned_lifts_preserving_annihilation_graph"] = unsigned_preserve

# ---------------------------------------------------------------- (c) order-4 elements generate SL(2,7)
P7 = 7
def mul(A, B):
    return ((A[0]*B[0] + A[1]*B[2]) % P7, (A[0]*B[1] + A[1]*B[3]) % P7,
            (A[2]*B[0] + A[3]*B[2]) % P7, (A[2]*B[1] + A[3]*B[3]) % P7)
G = [(a, b, c, d) for a in range(P7) for b in range(P7) for c in range(P7) for d in range(P7) if (a*d - b*c) % P7 == 1]
I = (1, 0, 0, 1)
def order(g):
    k, h = 1, g
    while h != I:
        h, k = mul(h, g), k + 1
    return k
gens = [g for g in G if order(g) == 4]
H, frontier = {I}, [I]
while frontier:
    nxt = []
    for h in frontier:
        for g in gens:
            x = mul(h, g)
            if x not in H:
                H.add(x); nxt.append(x)
    frontier = nxt
out["c"] = {"order_4_elements": len(gens), "subgroup_they_generate": len(H), "|SL(2,7)|": len(G),
            "consequence": "by Burnside, the images of the order-4 elements under an irreducible 4-dim representation "
                           "generate the full matrix algebra M4(C) (dimension 16)" if len(H) == len(G) else "not all"}

json.dump(out, open(os.path.join(HERE, "c2_checks_b.json"), "w"), indent=1)
for k, v in out.items():
    print(k, v)
