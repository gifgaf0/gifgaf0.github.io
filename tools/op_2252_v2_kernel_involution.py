"""
OP-2.25.2-V2 — Kernel involution check across all 84 two-term sedenion ZDs.

CLAIM (from §2.25.2-V, observed for x = e_1 + e_10 only):
    The 4-dimensional right-kernel of L_x for any two-term ZD x = e_a ± e_b
    is spanned by four other two-term ZD cross-couplings y_i = e_{c_i} ± e_{d_i}.
    Moreover, the four kernel basis vectors are related to x by the involution
        (a, b) → (9 − b, 9 − a)
    on imaginary index pairs (where the pair (a, b) encodes the cross-edge
    between interior index a (∈ 1..7) and exterior index b−8 (∈ 1..7)).

CLARIFICATION OF THE INVOLUTION:
    The sample data in §2.25.2-V shows x = e_1 + e_10 has kernel basis
        k_0:  e_7 + e_12   (a',b') = (7, 12)
        k_1: -e_6 + e_13   (a',b') = (6, 13)
        k_2:  e_5 + e_14   (a',b') = (5, 14)
        k_3: -e_4 + e_15   (a',b') = (4, 15)
    For x with (a, b) = (1, 10): note a + (b−8) = 1 + 2 = 3.
    For k_0 with (a', b') = (7, 12): a' + (b'−8) = 7 + 4 = 11. Not the same.

    Re-reading the §2.25.2-V text: "a' + b' = 9 = 1+8" applies to *interior*
    pairs after subtracting 8 from any index ≥ 8. So translate:
        x = e_1 + e_10  → interior pair (1, 2)   since 10 = 2 + 8
        k_0: e_7 + e_12 → interior pair (7, 4)   since 12 = 4 + 8
        k_1: e_6 + e_13 → interior pair (6, 5)
        k_2: e_5 + e_14 → interior pair (5, 6)
        k_3: e_4 + e_15 → interior pair (4, 7)
    Pattern: each kernel-basis pair (i', j') satisfies i' + j' = 11.
    And x's interior pair (1, 2) has sum 3.
    Observation: 3 + 11 = 14 = 2·7. The pair sums (3, 11) are complementary mod 14.

    Equivalently, each kernel basis pair (i', j') satisfies i' = 8 − j_x and
    j' = 8 − i_x (where (i_x, j_x) is x's interior pair).  Wait — check:
        x interior = (1, 2). Predicted kernel pair set built from (8−2, 8−1) = (6, 7).
        But kernel pairs are (7, 4), (6, 5), (5, 6), (4, 7). Not just (6, 7).

    So the clean involution is different. The correct observation from the
    sample data: the four kernel pairs (i', j') for i_x = 1, j_x = 2 are
        {(4, 7), (5, 6), (6, 5), (7, 4)}
    These satisfy i' + j' = 11 AND {i', j'} ∩ {i_x, j_x, i_x+1, j_x+1, ...} = ∅.
    They are the four ordered pairs (i', j') with i' ≠ j', i'+j' = 11,
    and {i', j'} ⊆ {3,4,5,6,7} (i.e., disjoint from {1,2}, the i_x, j_x).

    Hmm — {4,7}, {5,6}, {6,5}, {7,4}. As *sets* there are only two: {4,7} and {5,6}.
    But we have FOUR signed kernel vectors. The signed ZDs are
        +e_4 + e_15  (sign +)
        -e_4 + e_15  ≡  e_15 - e_4  (sign −, but reads as ordered pair (4, 7) with sign)
        +e_5 + e_14
        -e_6 + e_13
        +e_7 + e_12
    So in fact: 2 unsigned index-set partners {(4,7), (5,6)} each appearing in
    BOTH orderings (4,7)/(7,4) and (5,6)/(6,5), with specific signs.

REFORMULATED CLAIM (what we will actually test):
    Let x = e_a + s·e_b be a two-term ZD with a ∈ {1..7}, b ∈ {8..15}, s ∈ {±1}.
    Let i_x = a, j_x = b − 8 (interior indices, both in {1..7}, i_x ≠ j_x).

    Then the 4-D right-kernel of L_x has a basis consisting of 4 vectors,
    each of which is itself a two-term cross-edge ZD e_{a'} + s'·e_{b'+8}
    with interior pair (a', b') satisfying:
        a' + b' = i_x + j_x + (7 or 14 ...)   ← to be determined empirically

    We will measure, for each of the 84 signed ZDs:
      (1) Whether each kernel basis vector is a two-term sedenion element
          (exactly 2 nonzero coefficients, both ±1 mod p);
      (2) Whether each such two-term element is itself a cross-edge
          (one index in {1..7}, one in {8..15});
      (3) The arithmetic relationship between (i_x, j_x) and the kernel pairs.

REPO-INTEGRATION NOTES (per CLAUDE_CODE_BRIEF_07_OP_2252_V2_INTEGRATION.md,
May 16 2026):
- ``sys.path.insert`` uses the script's own directory (repo's tools/ layout)
  instead of the original session path ``/home/claude/sqt``.
- ``main`` accepts ``p_run`` so Task 4 (verification at p=2731) re-uses this
  module unchanged. CLI: ``python3 op_2252_v2_kernel_involution.py [p]``.
- All other logic is byte-faithful to the session script. A/B test against
  the repo's pre-built sedenion_Fp table confirmed 256/256 basis products
  identical, so no adapter is needed.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sedenion_Fp import (mul_vec, basis_vec, DIM, add_vec, scale_vec, is_zero)
from collections import defaultdict


def lmm(x, p_val):
    M = [[0] * DIM for _ in range(DIM)]
    for j in range(DIM):
        col = mul_vec(x, basis_vec(j), p_val)
        for i in range(DIM):
            M[i][j] = col[i] % p_val
    return M


def rref_kernel(M, p_val):
    """Compute kernel of M over F_p via Gauss-Jordan, return basis vectors."""
    A = [row[:] for row in M]
    rows = len(A)
    cols = len(A[0])
    r = 0
    pivot_cols = []
    for c in range(cols):
        if r >= rows:
            break
        piv = None
        for i in range(r, rows):
            if A[i][c] % p_val != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], -1, p_val)
        A[r] = [(x * inv) % p_val for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] % p_val != 0:
                factor = A[i][c]
                A[i] = [(A[i][j] - factor * A[r][j]) % p_val for j in range(cols)]
        pivot_cols.append(c)
        r += 1
    free_cols = [c for c in range(cols) if c not in pivot_cols]
    kernel_basis = []
    for fc in free_cols:
        v = [0] * cols
        v[fc] = 1
        for i, pc in enumerate(pivot_cols):
            v[pc] = (-A[i][fc]) % p_val
        kernel_basis.append(v)
    return kernel_basis


def signed_repr(v, p_val):
    """Convert vector to (index, signed_coefficient) list with sign in {-1,0,+1,...}."""
    out = []
    for i, c in enumerate(v):
        c = c % p_val
        if c == 0:
            continue
        s = c if c <= p_val // 2 else c - p_val
        out.append((i, s))
    return out


def normalize_kernel_vec(v, p_val):
    """Normalize a kernel basis vector: scale so the leading nonzero coeff is ±1.
    Returns the normalized vector and its 'shape' classification."""
    nz = signed_repr(v, p_val)
    if not nz:
        return v, "zero"
    i0, c0 = nz[0]
    inv = pow(c0 % p_val, -1, p_val)
    scaled = [(x * inv) % p_val for x in v]
    nz_scaled = signed_repr(scaled, p_val)
    return scaled, nz_scaled


def classify_two_term(nz_signed):
    """Given a list of (index, signed_coeff) pairs, check if it represents
    a clean two-term sedenion element with coeffs in {±1}, one index in
    {1..7} (interior) and one in {8..15} (exterior cross-edge)."""
    if len(nz_signed) != 2:
        return None
    (i, c_i), (j, c_j) = nz_signed
    if abs(c_i) != 1 or abs(c_j) != 1:
        return None
    if i in range(1, 8) and j in range(8, 16):
        return (i, j - 8, c_i, c_j)
    if j in range(1, 8) and i in range(8, 16):
        return (j, i - 8, c_j, c_i)
    return None


def enumerate_two_term_ZDs(p_val):
    """Find all signed two-term ZDs x = e_a + s*e_b with a ∈ {1..7}, b ∈ {8..15}, s ∈ {±1}
    such that there exists a two-term annihilator y of the same form."""
    interior = list(range(1, 8))
    exterior = list(range(8, 16))
    zds = []
    for a in interior:
        for b in exterior:
            for sa in (1, -1):
                x = add_vec(basis_vec(a), scale_vec(basis_vec(b), sa % p_val, p_val), p_val)
                found = False
                for c in interior:
                    if found:
                        break
                    if c == a:
                        continue
                    for d in exterior:
                        if found:
                            break
                        if d == b:
                            continue
                        for sc in (1, -1):
                            y = add_vec(basis_vec(c), scale_vec(basis_vec(d), sc % p_val, p_val), p_val)
                            if is_zero(mul_vec(x, y, p_val), p_val):
                                found = True
                                break
                if found:
                    zds.append({
                        'a': a, 'b': b, 'sign': sa,
                        'vec': x[:],
                        'label': f"e_{a} {'+' if sa == 1 else '-'} e_{b}",
                        'interior_pair': (a, b - 8),
                    })
    return zds


def run(p_run=911):
    """Return (verdict_dict, pair_sum_data, zds) for the given prime.

    Repo-integration extension over the session script: returns the data
    rather than only printing, so the Fano-line audit script
    (``fano_line_identification.py``) can assert against it without re-deriving.
    """
    print("=" * 78)
    print(f"OP-2.25.2-V2 — Kernel-involution check across all 84 ZDs at p = {p_run}")
    print("=" * 78)

    zds = enumerate_two_term_ZDs(p_run)
    print(f"\nEnumerated {len(zds)} signed two-term cross-edge ZDs.")
    if len(zds) != 84:
        print(f"  WARNING: expected 84, got {len(zds)}. Aborting.")
        return None, None, zds

    all_kernels_two_term = True
    pair_sum_data = []   # (label, x_sum, k_sums, kernel_interior_pairs, (i_x, j_x))
    failures = []
    sample_outputs = []

    for k_idx, zd in enumerate(zds):
        x = zd['vec']
        i_x, j_x = zd['interior_pair']
        M = lmm(x, p_run)
        kernel = rref_kernel(M, p_run)

        if len(kernel) != 4:
            failures.append((zd['label'], f"kernel dim = {len(kernel)} ≠ 4"))
            continue

        kernel_classifications = []
        zd_is_clean = True
        kernel_interior_pairs = []

        for kv in kernel:
            kv_norm, nz_scaled = normalize_kernel_vec(kv, p_run)
            cls = classify_two_term(nz_scaled)
            if cls is None:
                zd_is_clean = False
                kernel_classifications.append(('NOT_CLEAN', nz_scaled))
            else:
                a_k, b_k, sa_k, sb_k = cls
                kernel_classifications.append(('OK', cls))
                kernel_interior_pairs.append((a_k, b_k))

        if not zd_is_clean:
            all_kernels_two_term = False
            failures.append((zd['label'], kernel_classifications))
            continue

        x_sum = i_x + j_x
        k_sums = tuple(sorted(a + b for (a, b) in kernel_interior_pairs))
        pair_sum_data.append((zd['label'], x_sum, k_sums, kernel_interior_pairs, (i_x, j_x)))

        if k_idx < 5 or k_idx in (10, 20, 40, 60, 83):
            sample_outputs.append((zd['label'], i_x, j_x, kernel_interior_pairs))

    print(f"\n{'=' * 78}")
    print("RESULTS")
    print(f"{'=' * 78}")
    print(f"\nTotal ZDs checked: {len(zds)}")
    print(f"All have kernel dim 4: {len(failures) == 0 or all('dim' not in str(f[1]) for f in failures)}")
    print(f"All kernel basis vectors normalize to clean 2-term cross-edges: {all_kernels_two_term}")
    print(f"Failures: {len(failures)}")
    if failures:
        print("\nFAILURES:")
        for label, info in failures[:5]:
            print(f"  {label}: {info}")

    print(f"\n{'=' * 78}")
    print("SAMPLE: x's interior pair → kernel basis interior pairs")
    print(f"{'=' * 78}")
    print(f"{'ZD label':<18}{'(i_x,j_x)':<12}{'i_x+j_x':<10}{'kernel pairs (i,j)':<40}")
    print("-" * 78)
    for label, i_x, j_x, kpairs in sample_outputs:
        kp_str = ", ".join(f"({a},{b})" for (a, b) in kpairs)
        print(f"{label:<18}{f'({i_x},{j_x})':<12}{i_x+j_x:<10}{kp_str:<40}")

    print(f"\n{'=' * 78}")
    print("PAIR-SUM RELATIONSHIP")
    print(f"{'=' * 78}")
    by_x_sum = defaultdict(list)
    for entry in pair_sum_data:
        label, x_sum, k_sums, kpairs, ix_jx = entry
        by_x_sum[x_sum].append((label, k_sums, kpairs))
    print(f"\nDistinct x interior-pair sums (i_x + j_x): {sorted(by_x_sum.keys())}")
    print(f"\nFor each x-sum value, the set of kernel-pair sums observed:")
    print(f"{'x_sum':<8}{'n_zds':<8}{'kernel pair-sums (as multiset)':<50}{'consistent?':<12}")
    print("-" * 78)
    for x_sum in sorted(by_x_sum.keys()):
        entries = by_x_sum[x_sum]
        k_sum_sets = set(e[1] for e in entries)
        consistent = (len(k_sum_sets) == 1)
        rep_sums = list(k_sum_sets)[0] if consistent else f"VARIES: {k_sum_sets}"
        print(f"{x_sum:<8}{len(entries):<8}{str(rep_sums):<50}{('YES' if consistent else 'NO'):<12}")

    print(f"\n{'=' * 78}")
    print("INVOLUTION TEST: does (x_sum) + (each kernel_pair_sum) = 14 always?")
    print(f"{'=' * 78}")
    all_complement_14 = True
    counterexamples = []
    for entry in pair_sum_data:
        label, x_sum, k_sums, kpairs, ix_jx = entry
        for ks in k_sums:
            if x_sum + ks != 14:
                all_complement_14 = False
                if len(counterexamples) < 5:
                    counterexamples.append((label, x_sum, ks, x_sum + ks))
    if all_complement_14:
        print("\n✓ For ALL 84 ZDs, every kernel basis vector's interior pair (i', j')")
        print("  satisfies (i' + j') + (i_x + j_x) = 14.")
    else:
        print("\n✗ The 'sum to 14' rule FAILS for some ZDs.")
        print("  Counterexamples:")
        for label, x_sum, ks, total in counterexamples:
            print(f"    {label}: x_sum={x_sum}, kernel_sum={ks}, total={total} (expected 14)")

    print(f"\n{'=' * 78}")
    print("DISJOINTNESS TEST: are kernel pairs always disjoint from x's interior pair?")
    print(f"{'=' * 78}")
    all_disjoint = True
    disj_counterex = []
    for zd in zds:
        x = zd['vec']
        i_x, j_x = zd['interior_pair']
        M = lmm(x, p_run)
        kernel = rref_kernel(M, p_run)
        if len(kernel) != 4:
            continue
        x_indices = {i_x, j_x}
        for kv in kernel:
            _, nz_scaled = normalize_kernel_vec(kv, p_run)
            cls = classify_two_term(nz_scaled)
            if cls is None:
                continue
            a_k, b_k, _, _ = cls
            if {a_k, b_k} & x_indices:
                all_disjoint = False
                if len(disj_counterex) < 5:
                    disj_counterex.append((zd['label'], (i_x, j_x), (a_k, b_k)))
    if all_disjoint:
        print("\n✓ For ALL 84 ZDs, every kernel basis vector's interior pair {i', j'}")
        print("  is disjoint from x's interior pair {i_x, j_x}.")
    else:
        print("\n✗ Disjointness FAILS for some ZDs.")
        for label, x_pair, k_pair in disj_counterex:
            print(f"  {label}: x_pair={x_pair}, k_pair={k_pair} (overlap)")

    print(f"\n{'=' * 78}")
    print("VERDICT (OP-2.25.2-V2)")
    print(f"{'=' * 78}")
    verdict = {
        'p': p_run,
        'n_zds': len(zds),
        'rank12_kernel4': len(failures) == 0,
        'kernels_clean_two_term': all_kernels_two_term,
        'complement_14': all_complement_14,
        'disjoint_from_x_pair': all_disjoint,
    }
    print(f"  (1) All 84 ZD elements have rank(L_x) = 12, kernel dim 4: "
          f"{'CONFIRMED' if verdict['rank12_kernel4'] else 'FAILED'}")
    print(f"  (2) Every kernel basis vec is a clean two-term cross-edge ZD: "
          f"{'CONFIRMED' if verdict['kernels_clean_two_term'] else 'FAILED'}")
    print(f"  (3) Kernel pair sums + x pair sum = 14 (complementary mod 14): "
          f"{'CONFIRMED' if verdict['complement_14'] else 'FAILED'}")
    print(f"  (4) Kernel pairs disjoint from x's interior pair: "
          f"{'CONFIRMED' if verdict['disjoint_from_x_pair'] else 'FAILED'}")

    return verdict, pair_sum_data, zds


def main():
    p_run = 911
    if len(sys.argv) > 1:
        p_run = int(sys.argv[1])
    run(p_run)


if __name__ == '__main__':
    main()
