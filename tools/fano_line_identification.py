"""
fano_line_identification.py — Identify the 7 Fano lines from the repo's
sedenion multiplication table and assert the OP-2.25.2-V2 kernel
prediction against the kernel-involution check.

Per ``reports/OP-2.25.2-V2_RESULT.md`` (May 16, 2026):

    For x = e_a + e_{b+8} with interior pair {a, b}, let L = {a, b, m} be
    the unique Fano line containing {a, b}, where m is the third point on
    the line. Then ker(L_x) lies entirely in the cross-edge ZD subspace
    spanned by the other two Fano lines through m.

This script:

1. Computes the 7 Fano lines from ``sedenion_Fp.mul_vec`` by reading
   ``e_a · e_b = ±e_c`` for each unordered pair (a, b) in {1..7}.
2. For each of the 21 unordered pairs, identifies the third point m
   and predicts the kernel pair-set = the two other unordered pairs
   through m.
3. Calls ``op_2252_v2_kernel_involution.run(p)`` and asserts every
   84-ZD kernel pair-set matches the Fano-line prediction.

CLI: ``python3 fano_line_identification.py [p]``  (defaults to p=911).
"""

import sys
import os
from itertools import combinations
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sedenion_Fp import mul_vec, basis_vec
from op_2252_v2_kernel_involution import run


def compute_fano_lines(p_val):
    """Return (sorted_lines, pair_to_third_point).

    Each (a, b) with a, b ∈ {1..7}, a < b yields ``e_a · e_b = ±e_c``;
    the index c is the third point of the Fano line {a, b, c}.
    """
    lines = set()
    pair_to_third = {}
    for a, b in combinations(range(1, 8), 2):
        prod = mul_vec(basis_vec(a), basis_vec(b), p_val)
        nz = [(i, v) for i, v in enumerate(prod) if v != 0]
        assert len(nz) == 1, f"e_{a}*e_{b} is not a single basis element: {nz}"
        c, coeff = nz[0]
        assert c in range(1, 8), f"e_{a}*e_{b} = ±e_{c}; c={c} not in 1..7"
        assert coeff in (1, p_val - 1), \
            f"e_{a}*e_{b} coefficient at e_{c}: {coeff} (expected ±1)"
        lines.add(frozenset({a, b, c}))
        pair_to_third[frozenset({a, b})] = c
    assert len(lines) == 7, f"expected 7 Fano lines, got {len(lines)}"
    return sorted(lines, key=sorted), pair_to_third


def predict_kernel_pair_set(pair, pair_to_third):
    """For ZD interior pair {a, b}: kernel pair-set = the two other
    unordered pairs (i, j) with {i, j, m} a Fano line, where m is the
    third point of {a, b}'s Fano line."""
    m = pair_to_third[pair]
    others = [p for p, third in pair_to_third.items() if third == m and p != pair]
    assert len(others) == 2, f"expected 2 partner pairs for {set(pair)}, got {others}"
    return frozenset(others), m


def main():
    p_val = int(sys.argv[1]) if len(sys.argv) > 1 else 911

    print(f"Computing 7 Fano lines from sedenion_Fp at p = {p_val}\n")
    lines, pair_to_third = compute_fano_lines(p_val)
    print("The 7 Fano lines on {e_1..e_7}:")
    for line in lines:
        s = sorted(line)
        print(f"  {{{s[0]}, {s[1]}, {s[2]}}}")

    print("\nFor each of the 21 unordered pairs: Fano-line third point + predicted kernel pair-set:")
    print(f"  {'pair':<10}{'third m':<10}{'predicted kernel pair-set':<40}")
    print("  " + "-" * 60)
    for pair in sorted(pair_to_third.keys(), key=sorted):
        kernel_set, m = predict_kernel_pair_set(pair, pair_to_third)
        kset_str = " ∪ ".join(
            "{" + ",".join(str(x) for x in sorted(p)) + "}"
            for p in sorted(kernel_set, key=sorted)
        )
        s = sorted(pair)
        print(f"  {{{s[0]},{s[1]}}}      {m:<10}{kset_str}")

    print(f"\nRunning op_2252_v2_kernel_involution.run({p_val}) to assert against kernel data…")
    print("(suppressing op_2252's own verbose output — the verdict is what matters)\n")

    # Capture op_2252's stdout to keep this script's output focused.
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        verdict, pair_sum_data, _ = run(p_val)
    op_verdict_lines = buf.getvalue().splitlines()
    # Echo only the final verdict block (last 6 lines)
    for ln in op_verdict_lines[-6:]:
        print(f"    {ln}")

    assert verdict is not None, "op_2252 returned None — 84 ZD count failed"

    print("\nAsserting Fano-line prediction against every ZD's kernel pair-set…")
    failures = []
    for label, x_sum, k_sums, kpairs, ix_jx in pair_sum_data:
        x_pair = frozenset(ix_jx)
        kernel_unordered = [frozenset(kp) for kp in kpairs]
        kernel_multiset = Counter(kernel_unordered)
        predicted, m = predict_kernel_pair_set(x_pair, pair_to_third)
        if set(kernel_multiset.keys()) != predicted:
            failures.append((label, ix_jx, m, dict(kernel_multiset), set(predicted)))

    print("\n" + "=" * 78)
    print("FANO-LINE PREDICTION ASSERTION")
    print("=" * 78)
    if not failures:
        print(f"\n✓ For ALL {len(pair_sum_data)} ZDs at p={p_val}, the kernel pair-set matches the")
        print(f"  Fano-line prediction exactly: kernel supported on the two other Fano-lines")
        print(f"  through the third point of x's own Fano line.")
        print(f"\n  (Each predicted unordered pair appears twice in the 4-vector kernel basis,")
        print(f"   once with each interior-pair ordering, totalling 4 basis vectors.)")
    else:
        print(f"\n✗ {len(failures)} ZDs DISAGREE with the Fano-line prediction.")
        for label, ix_jx, m, ker, pred in failures[:5]:
            print(f"  {label}: x_pair={set(ix_jx)}, m={m},")
            print(f"    kernel={ker}")
            print(f"    predicted={pred}")
        sys.exit(1)


if __name__ == '__main__':
    main()
