"""Compute the CRT decomposition of R = Z_3329[X] / (X^256 + 1).

q-1 = 3328 = 2^8 * 13. Hence F_q contains a primitive 256-th root of
unity but no 512-th root, so X^256 + 1 splits as

    X^256 + 1 = prod_{j=0}^{127} (X^2 - zeta^{2j+1})

where zeta is any element of order 256. ML-KEM canonically takes
zeta = 17 (FIPS 203 §4.3 / Annex A.1). The 128 quadratic factors are
indexed by the 128 *primitive* 256-th roots of unity, equivalently by
the odd residues 1, 3, 5, ..., 255 mod 256.

We don't depend on sympy here: the structure is fixed and a direct
computation suffices. The script also performs an independent
verification that the polynomial product of the 128 factors equals
X^256 + 1 modulo 3329.

Output: tools/mlkem_ring_factors.json containing for each factor j:

    {
      "j":      <integer 0..127>,
      "k":      <odd integer 1..255 = 2j+1>,
      "root":   <int = zeta^k mod q>,
      "neg_root": <int = -root mod q (the trailing coefficient of the factor)>,
      "factor_coeffs": [neg_root, 0, 1]    # X^2 + 0*X + (-root)
    }

plus a top-level metadata block.
"""

from __future__ import annotations

import json
from pathlib import Path

Q = 3329
ZETA = 17     # generator of the order-256 subgroup of F_q^*
DEG = 256     # ring degree
NUM_FACTORS = 128


def order_of(g: int) -> int:
    """Multiplicative order of g modulo Q."""
    o = 1
    cur = g % Q
    while cur != 1:
        cur = (cur * g) % Q
        o += 1
    return o


def poly_mul_mod(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if not ai:
            continue
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % Q
    return out


def main() -> int:
    assert order_of(ZETA) == 256, f"zeta has order {order_of(ZETA)}"

    # Build the 128 roots r_j = zeta^(2j+1) for j = 0..127.
    factors = []
    for j in range(NUM_FACTORS):
        k = 2 * j + 1
        r = pow(ZETA, k, Q)
        neg_r = (-r) % Q
        factors.append({
            "j": j,
            "k": k,
            "root": r,
            "neg_root": neg_r,
            "factor_coeffs": [neg_r, 0, 1],   # X^2 + 0*X + (-r)
        })

    # Distinct-roots check: the 128 roots must all differ.
    roots = sorted(f["root"] for f in factors)
    assert len(set(roots)) == NUM_FACTORS, "duplicate roots — zeta order or k parity wrong"

    # Independent verification: prod_j (X^2 - r_j) mod q == X^256 + 1.
    # We multiply iteratively to keep this O(N * deg) memory bounded.
    product = [1]
    for f in factors:
        product = poly_mul_mod(product, f["factor_coeffs"])
    expected = [0] * (DEG + 1)
    expected[0] = 1
    expected[DEG] = 1
    if product != expected:
        # Shouldn't happen with correct zeta — surface the diff helpfully.
        diff_idx = [i for i, (a, b) in enumerate(zip(product, expected)) if a != b]
        raise SystemExit(f"factor product != X^256+1; diff at indices {diff_idx[:20]}...")

    out_path = Path("tools/mlkem_ring_factors.json")
    payload = {
        "ring": "Z_3329[X] / (X^256 + 1)",
        "modulus": Q,
        "degree": DEG,
        "zeta": ZETA,
        "zeta_order": 256,
        "num_factors": NUM_FACTORS,
        "factor_form": "X^2 - root",
        "verified": "product of factor_coeffs equals X^256 + 1 over F_3329",
        "factors": factors,
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} : {NUM_FACTORS} quadratic factors, product check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
