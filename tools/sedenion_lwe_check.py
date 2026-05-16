"""
sedenion_lwe_check.py
=====================
Left-multiplication injectivity audit over F_p.

For each canonical zero-divisor element s in the sedenion algebra S
over F_p, compute rank(L_s) where L_s : S → S is the linear map
x ↦ s · x (sedenion product). If rank(L_s) < 16 then ker(L_s) is
non-trivial: an LWE scheme that uses s as a secret cannot recover
the random coordinate that lives in ker(L_s). Such s is therefore
unusable as an LWE secret.

Inputs (only):
- ``sedenion_Fp.py``     — multiplication table over F_p
- ``sedenion_audit.py``  — canonical ZD quadruple enumeration

This script does **not** assume any result from
``tools/SLWE_Prime_Master_v2.md``. The manifest's claim
"rank(L_s) = 12 for ALL 42 ZD elements (ker dim=4)" is what we are
verifying or refuting; the rank is recomputed from the
multiplication table directly.
"""

import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sedenion_Fp import mul_vec, basis_vec, DIM
from sedenion_audit import find_canonical_zd_quadruples


# ─────────────────────────────────────────────────────────────────
# Linear-algebra helpers (Gaussian elimination over F_p)
# ─────────────────────────────────────────────────────────────────


def left_mult_matrix(s, p):
    """Return the 16×16 matrix of x ↦ s · x in the basis (e_0..e_15)."""
    M = [[0] * DIM for _ in range(DIM)]
    for j in range(DIM):
        col = mul_vec(s, basis_vec(j), p)
        for i in range(DIM):
            M[i][j] = col[i] % p
    return M


def rank_Fp(M, p):
    """Row-reduce a copy of M over F_p and return its rank."""
    A = [row[:] for row in M]
    n_rows = len(A)
    n_cols = len(A[0])
    rank = 0
    for col in range(n_cols):
        pivot = next((r for r in range(rank, n_rows) if A[r][col] % p != 0),
                     None)
        if pivot is None:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        inv = pow(A[rank][col] % p, p - 2, p)
        A[rank] = [(x * inv) % p for x in A[rank]]
        for r in range(n_rows):
            if r != rank and A[r][col] % p != 0:
                f = A[r][col]
                A[r] = [(A[r][c] - f * A[rank][c]) % p for c in range(n_cols)]
        rank += 1
    return rank


def two_term(a, b, sa, sb, p):
    """Sedenion vector sa·e_a + sb·e_b mod p."""
    v = [0] * DIM
    v[a] = sa % p
    v[b] = sb % p
    return v


# ─────────────────────────────────────────────────────────────────
# Main audit
# ─────────────────────────────────────────────────────────────────


def main():
    p = 911
    print(f"Field: F_{p}")
    print("Building canonical ZD quadruple set (this calls sedenion_audit.find_canonical_zd_quadruples)…")
    quads = find_canonical_zd_quadruples(p)
    print(f"Canonical ZD quadruples found: {len(quads)}")

    # Distinct index pairs (a,b) appearing in at least one quadruple.
    pairs = set()
    pair_freq = Counter()
    for q in quads:
        for pair in q:
            pairs.add(pair)
            pair_freq[pair] += 1
    pairs = sorted(pairs)
    print(f"Distinct (a,b) index pairs participating: {len(pairs)}")
    appearance_dist = Counter(pair_freq.values())
    print(f"Per-pair appearance count distribution: {dict(sorted(appearance_dist.items()))}")
    print(f"Total pair-slots (sanity: 2*{len(quads)} = {2*len(quads)}): {sum(pair_freq.values())}")

    # Per-pair rank of L_s with the canonical sign choice s = +e_a + e_b.
    print("\n── rank(L_s) for s = +e_a + e_b, one row per distinct pair ──")
    print(f"  {'pair':<14}{'rank':>6}{'ker_dim':>10}")
    per_pair = []
    for (a, b) in pairs:
        s = two_term(a, b, 1, 1, p)
        M = left_mult_matrix(s, p)
        r = rank_Fp(M, p)
        per_pair.append(((a, b), r, DIM - r))
        print(f"  (e{a:2d},e{b:2d})       {r:>4} {DIM - r:>10}")

    rank_dist_canon = Counter(r for (_, r, _) in per_pair)
    print(f"\nRank distribution over {len(pairs)} canonical (+,+) pairs:")
    for r, ct in sorted(rank_dist_canon.items()):
        print(f"  rank={r}: {ct} pairs   (ker_dim={DIM - r})")

    # Sweep all four sign patterns (±,±) per pair — total 4·|pairs| elements.
    print(f"\n── Full sign sweep: 4 sign patterns × {len(pairs)} pairs ──")
    all_elements = []
    for (a, b) in pairs:
        for sa in (1, -1):
            for sb in (1, -1):
                s = two_term(a, b, sa, sb, p)
                M = left_mult_matrix(s, p)
                r = rank_Fp(M, p)
                all_elements.append((((a, b), (sa, sb)), r))
    rank_dist_full = Counter(r for (_, r) in all_elements)
    print(f"Total ZD-shape elements probed: {len(all_elements)}")
    print(f"Rank distribution (over all signs): {dict(sorted(rank_dist_full.items()))}")

    # Controls: ZD-style two-term element on a NON-ZD pair, and a basis unit.
    print("\n── Controls (sanity) ──")
    # Pick a basis pair that does NOT appear in the ZD set.
    all_two_index_pairs = {(i, j) for i in range(1, DIM) for j in range(i + 1, DIM)}
    nonzd_pairs = sorted(all_two_index_pairs - set(pairs))
    print(f"Non-ZD basis pairs available: {len(nonzd_pairs)}")
    sample_nonzd = nonzd_pairs[:5]
    for (a, b) in sample_nonzd:
        s = two_term(a, b, 1, 1, p)
        r = rank_Fp(left_mult_matrix(s, p), p)
        print(f"  control non-ZD s = e_{a}+e_{b}: rank(L_s) = {r}   (expect 16)")

    # Basis units e_1..e_15 should all be units (rank 16) since e_i^2 = -1.
    nonunit_basis = []
    for i in range(1, DIM):
        r = rank_Fp(left_mult_matrix(basis_vec(i), p), p)
        if r != DIM:
            nonunit_basis.append((i, r))
    if not nonunit_basis:
        print(f"  control basis units e_1..e_15: all rank {DIM} ✓")
    else:
        print(f"  control basis units (non-full rank): {nonunit_basis}")

    # ─────────────────────────────────────────────────────────────
    # Verdict against the manifest claim
    # ─────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("VERDICT vs SLWE_Prime_Master_v2.md §6 claim")
    print('  "rank(L_s) = 12 for ALL 42 ZD elements (ker dim=4)."')
    print("=" * 60)
    n_pairs = len(pairs)
    canon_uniform_12 = all(r == 12 for (_, r, _) in per_pair)
    full_uniform_12 = all(r == 12 for (_, r) in all_elements)
    print(f"Distinct index pairs:       {n_pairs}      (manifest: 42 — {'MATCH' if n_pairs == 42 else 'MISMATCH'})")
    print(f"All (+,+) ranks == 12:      {canon_uniform_12}")
    print(f"All sign-sweep ranks == 12: {full_uniform_12}")
    print(f"Canonical rank distribution: {dict(sorted(rank_dist_canon.items()))}")
    print(f"Sign-sweep rank distribution: {dict(sorted(rank_dist_full.items()))}")
    if n_pairs == 42 and full_uniform_12:
        print("\nVERIFIED — manifest claim holds as stated.")
    else:
        print("\nNOT verified as stated. See actual distribution above.")


if __name__ == "__main__":
    main()
