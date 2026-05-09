"""
sedenion_audit.py
=================
Deep structural audit of the 84 zero-divisor pairs over F_p.

Questions:
1. Does the 84 = 21 × 4 factorization hold structurally?
2. Are the same 84 index quadruples (a,b,c,d) active across mod-455 primes?
3. Does a non-mod-455 prime give a different count?
4. What is the orbit structure under index permutations (proxy for Aut(S) action)?
5. What is the zero-divisor graph structure?
"""

import sys
sys.path.insert(0, '/home/claude')
from sedenion_Fp import mul_vec, add_vec, scale_vec, basis_vec, is_zero, DIM
from itertools import combinations, permutations
from collections import Counter, defaultdict

def find_canonical_zd_quadruples(p):
    """
    Return the set of canonical (a,b,c,d) quadruples (unordered pairs of
    unordered index pairs) such that (e_a+/-e_b)(e_c+/-e_d) = 0.
    One representative sign pattern per quadruple.
    """
    imag = list(range(1, 16))
    quadruples = set()

    for a, b in combinations(imag, 2):
        ea = basis_vec(a); eb = basis_vec(b)
        for sa in [1, p-1]:
            x = add_vec(scale_vec(ea, sa, p), eb, p)
            for c, d in combinations(imag, 2):
                if set([a,b]) & set([c,d]):
                    continue  # must be disjoint index sets
                ec = basis_vec(c); ed = basis_vec(d)
                for sc in [1, p-1]:
                    y = add_vec(scale_vec(ec, sc, p), ed, p)
                    if is_zero(mul_vec(x, y, p), p):
                        quad = tuple(sorted([tuple(sorted([a,b])),
                                            tuple(sorted([c,d]))]))
                        quadruples.add(quad)
    return quadruples


def analyze_quadruples(quads):
    """Analyze the structure of the 84 zero-divisor quadruples."""
    print(f"\nTotal quadruples: {len(quads)}")

    # Extract all index pairs involved
    all_pairs = set()
    for q in quads:
        all_pairs.add(q[0])
        all_pairs.add(q[1])
    print(f"Distinct index pairs (a,b) appearing: {len(all_pairs)}")
    # Expected: 21 pairs (C(7,2)=21 for octonion imaginary indices? or C(15,2)=105?)
    # Moreno: the 84 come from specific quadruples of imaginary unit indices

    # How many times does each pair appear?
    pair_count = Counter()
    for q in quads:
        pair_count[q[0]] += 1
        pair_count[q[1]] += 1
    freq = Counter(pair_count.values())
    print(f"Pair frequency distribution: {dict(sorted(freq.items()))}")
    # If 84 = 21 × 4: expect 21 pairs each appearing 4 times? Or 84 pairs each once?
    # Actually: 84 quadruples, each involving 2 pairs → 168 pair slots.
    # If 21 distinct pairs, 168/21 = 8 appearances each.

    # Index distribution: which imaginary unit indices appear?
    index_count = Counter()
    for q in quads:
        for pair in q:
            for idx in pair:
                index_count[idx] += 1
    print(f"Index participation counts:")
    for idx in range(1, 16):
        print(f"  e{idx:2d}: {index_count[idx]} appearances")

    # Check disjointness: all quadruples should have disjoint pairs
    non_disjoint = 0
    for q in quads:
        if set(q[0]) & set(q[1]):
            non_disjoint += 1
    print(f"Quadruples with overlapping indices: {non_disjoint} (should be 0)")

    return all_pairs, pair_count


def compare_across_primes(primes):
    """Check whether the same 84 quadruples appear across different primes."""
    print(f"\n=== Quadruple stability across primes ===")
    results = {}
    for p in primes:
        q = find_canonical_zd_quadruples(p)
        results[p] = q
        tag = "mod455" if p % 455 == 1 else "non-mod455"
        print(f"  p={p:6d} ({tag:12s}): {len(q)} quadruples")
    return results


def zero_divisor_graph(quads, n=15):
    """
    Build the zero-divisor graph: nodes = imaginary unit indices 1..n,
    edge between a and b if they appear together in some zero-divisor pair.
    """
    edges = set()
    for q in quads:
        for pair in q:
            a, b = pair
            edges.add((min(a,b), max(a,b)))
    print(f"\nZero-divisor graph: {n} nodes, {len(edges)} edges")
    # Degree sequence
    degree = Counter()
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    deg_seq = sorted(degree.values(), reverse=True)
    print(f"Degree sequence: {deg_seq}")
    deg_freq = Counter(deg_seq)
    print(f"Degree distribution: {dict(sorted(deg_freq.items()))}")
    return edges, degree


def check_21x4_factorization(quads, pair_count):
    """
    Verify whether the 84 = 21 × 4 factorization holds:
    Are there exactly 21 'active' pairs, each appearing in exactly 4 quadruples?
    """
    print(f"\n=== 21 × 4 factorization check ===")
    # Count pairs appearing exactly 4 times
    pairs_4 = [p for p, c in pair_count.items() if c == 4]
    pairs_other = [(p, c) for p, c in pair_count.items() if c != 4]
    print(f"Pairs appearing exactly 4 times: {len(pairs_4)}")
    print(f"Pairs with other counts: {pairs_other[:10]}")
    if len(pairs_4) == 21:
        print("✓ 84 = 21 × 4 structure CONFIRMED")
    else:
        print(f"✗ 21 × 4 not exact at this level; {len(pair_count)} distinct pairs total")


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

print("=== Deep Structural Audit of Sedenion Zero-Divisors over F_p ===\n")

# Primary: p=911 (smallest mod-455 prime)
p = 911
print(f"Primary field: F_{p}")
quads_911 = find_canonical_zd_quadruples(p)
all_pairs, pair_count = analyze_quadruples(quads_911)
check_21x4_factorization(quads_911, pair_count)
edges, degree = zero_divisor_graph(quads_911)

# Compare across primes: two mod-455, two non-mod-455
test_primes = [
    911,    # mod-455
    2731,   # mod-455
    907,    # NOT mod-455 (907 mod 455 = 452, prime)
    919,    # NOT mod-455 (919 mod 455 = 9, prime)
]
print(f"\nChecking: 907 prime={all(907%i!=0 for i in range(2,30))}, 907 mod 455={907%455}")
print(f"Checking: 919 prime={all(919%i!=0 for i in range(2,30))}, 919 mod 455={919%455}")

results = compare_across_primes(test_primes)

# Check if non-mod-455 primes give the same quadruples
print("\n=== Quadruple identity across primes ===")
q911 = results[911]
for p2 in test_primes[1:]:
    if p2 in results:
        same = q911 == results[p2]
        diff = q911.symmetric_difference(results[p2])
        print(f"  p={p2}: same quadruples as p=911? {same}  (diff size: {len(diff)})")

