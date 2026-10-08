#!/usr/bin/env python3
"""
e_k8_1factorizations.py -- C2 batch, math_B leg, item (e): 1-factorizations of K8.

Self-contained.  Vertices 0..7.
  1. All perfect matchings of K8 (expect 105).
  2. All 1-factorizations on labelled vertices: unordered sets of 7 pairwise edge-disjoint perfect
     matchings covering the 28 edges (backtracking on the smallest uncovered edge, so each set is
     produced exactly once).  Expect 6240.
  3. Isomorphism classes under S8: union-find over the labelled set, generators = the 7 adjacent
     transpositions (i, i+1); canonical form of a factorization = sorted tuple of sorted matchings.
     Class sizes; |Aut| = 8!/class size.
  4. Cross-check |Aut| directly: for one representative per class, count the permutations in S8
     fixing it (all 40320).
  5. Invariant per class: number of factor pairs whose union is two 4-cycles (vs one 8-cycle).
  6. Supplementary (my own construction, not a ledger definition): the 1-factorization attached to a
     Fano plane on {0..6} with an added point 'inf'=7, F_z = {inf z} + {xy : {x,y,z} a line}, for the
     two cyclic Fano planes {QR + i} (QR = {1,2,4}) and {QNR + i} (QNR = {3,5,6}) mod 7.
"""
import itertools
import math
from collections import Counter

V = list(range(8))
EDGES = [(i, j) for i in V for j in V if i < j]


def perfect_matchings(vs):
    if not vs:
        yield ()
        return
    a = vs[0]
    for k in range(1, len(vs)):
        b = vs[k]
        rest = vs[1:k] + vs[k + 1:]
        for m in perfect_matchings(rest):
            yield ((a, b),) + m


PM = [tuple(sorted(m)) for m in perfect_matchings(V)]
PM_BY_EDGE = {e: [m for m in PM if e in m] for e in EDGES}


def one_factorizations():
    out = []

    def rec(uncovered, chosen):
        if not uncovered:
            out.append(tuple(sorted(chosen)))
            return
        e = min(uncovered)
        for m in PM_BY_EDGE[e]:
            if all(f in uncovered for f in m):
                rec(uncovered - set(m), chosen + [m])

    rec(set(EDGES), [])
    return out


def canon(fact):
    return tuple(sorted(tuple(sorted(tuple(sorted(e)) for e in m)) for m in fact))


def relabel(fact, perm):
    return canon([[(perm[a], perm[b]) for a, b in m] for m in fact])


class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def cycle_profile(fact):
    """number of factor pairs whose union is 2 x C4 (else it is a single C8)."""
    n44 = 0
    for m1, m2 in itertools.combinations(fact, 2):
        adj = {v: [] for v in V}
        for a, b in list(m1) + list(m2):
            adj[a].append(b)
            adj[b].append(a)
        # component sizes
        seen, comps = set(), []
        for v in V:
            if v in seen:
                continue
            stack, size = [v], 0
            seen.add(v)
            while stack:
                x = stack.pop()
                size += 1
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
            comps.append(size)
        if sorted(comps) == [4, 4]:
            n44 += 1
        else:
            assert sorted(comps) == [8]
    return n44


def main():
    print("=" * 78)
    print("ITEM (e) -- 1-factorizations of K8 (math_B leg)")
    print("=" * 78)
    print(f"perfect matchings of K8: {len(PM)}")
    F = one_factorizations()
    Fc = [canon(f) for f in F]
    assert len(set(Fc)) == len(Fc)
    print(f"labelled 1-factorizations of K8 (unordered factors): {len(F)}")
    for f in F:
        assert len(f) == 7 and len({e for m in f for e in m}) == 28
    index = {f: i for i, f in enumerate(Fc)}
    dsu = DSU(len(Fc))
    for i, f in enumerate(Fc):
        for k in range(7):
            perm = list(range(8))
            perm[k], perm[k + 1] = perm[k + 1], perm[k]
            g = relabel(f, perm)
            dsu.union(i, index[g])  # KeyError would mean the set is not S8-closed
    comps = Counter(dsu.find(i) for i in range(len(Fc)))
    print(f"isomorphism classes under S8: {len(comps)}")
    fact8 = math.factorial(8)
    rows = []
    for root, size in comps.items():
        rep = Fc[root]
        # direct stabilizer count over all of S8
        stab = sum(1 for perm in itertools.permutations(range(8)) if relabel(rep, perm) == rep)
        rows.append((size, fact8 // size, stab, cycle_profile(rep), rep))
    rows.sort(key=lambda r: r[0])
    print("class size | 8!/size | |Aut| by direct count | #factor pairs with union C4+C4 (of 21)")
    for size, aut, stab, n44, rep in rows:
        print(f"   {size:5d}   | {aut:6d}  | {stab:6d}                | {n44:2d}")
    print(f"sum of class sizes = {sum(r[0] for r in rows)}")
    print(f"orbit-stabilizer consistent for every class: {all(r[1] == r[2] for r in rows)}")
    print("representatives:")
    for size, aut, stab, n44, rep in rows:
        print(f"   |Aut|={aut}: {rep}")

    # supplementary: QR / QNR cyclic Fano planes -> 1-factorizations of K8 on {0..6} + {7 = inf}
    print("\nSupplementary (own construction, not a ledger definition): Fano-plane 1-factorizations")
    INF = 7
    for name, D in (("QR {1,2,4}", (1, 2, 4)), ("QNR {3,5,6}", (3, 5, 6))):
        lines = [tuple(sorted(((d + i) % 7) for d in D)) for i in range(7)]
        # check it is a Fano plane (every pair of points on exactly one line)
        pair_ok = all(sum(1 for L in lines if a in L and b in L) == 1 for a in range(7) for b in range(a + 1, 7))
        fact = []
        for z in range(7):
            m = [(z, INF)] + [tuple(sorted((x, y))) for L in lines if z in L for x, y in [tuple(v for v in L if v != z)]]
            fact.append(tuple(sorted(tuple(sorted(e)) for e in m)))
        fc = canon(fact)
        is_1f = len({e for m in fc for e in m}) == 28 and all(len(m) == 4 for m in fc)
        root = dsu.find(index[fc])
        print(f"   {name}: Fano plane: {pair_ok}; valid 1-factorization: {is_1f}; "
              f"class |Aut| = {fact8 // comps[root]}")
    neg = {i: (-i) % 7 for i in range(7)}
    neg[INF] = INF
    print("   x -> -x (fixing inf) maps the QR plane's lines onto the QNR plane's lines:",
          sorted(tuple(sorted(neg[v] for v in L)) for L in [tuple(sorted(((d + i) % 7) for d in (1, 2, 4))) for i in range(7)])
          == sorted(tuple(sorted(((d + i) % 7) for d in (3, 5, 6))) for i in range(7)))
    print("   x -> 3x (fixing inf) maps the QR plane's lines onto the QNR plane's lines:",
          sorted(tuple(sorted((3 * v) % 7 for v in L)) for L in [tuple(sorted(((d + i) % 7) for d in (1, 2, 4))) for i in range(7)])
          == sorted(tuple(sorted(((d + i) % 7) for d in (3, 5, 6))) for i in range(7)))

    # supplementary 2: all starters in Z_7 and the cyclic 1-factorizations they induce on Z_7 + {inf}
    print("\nSupplementary 2 (own construction): starters in Z_7 -> cyclic 1-factorizations of K8")
    nz = [1, 2, 3, 4, 5, 6]
    starters = set()
    for m in perfect_matchings(nz):
        diffs = sorted(d for a, b in m for d in ((a - b) % 7, (b - a) % 7))
        if diffs == nz:
            starters.add(tuple(sorted(tuple(sorted(e)) for e in m)))
    for S in sorted(starters):
        fact = []
        for k in range(7):
            mm = [(k, INF)] + [tuple(sorted(((a + k) % 7, (b + k) % 7))) for a, b in S]
            fact.append(tuple(sorted(tuple(sorted(e)) for e in mm)))
        fc = canon(fact)
        ok = len({e for m in fc for e in m}) == 28
        root = dsu.find(index[fc])
        times3 = tuple(sorted(tuple(sorted(((3 * a) % 7, (3 * b) % 7))) for a, b in S))
        print(f"   starter {S}: valid: {ok}; class |Aut| = {fact8 // comps[root]}; image under x->3x: {times3}")


if __name__ == "__main__":
    main()
