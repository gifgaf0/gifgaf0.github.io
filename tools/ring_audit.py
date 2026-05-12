"""Programmatic ring audit for ML-KEM's R_3329.

Wires the four lines of the analytical audit (commit 2017c4a,
documented in tools/BRIEF_03_RING_AUDIT_SUMMARY.md) into callable
functions that return structured dicts. Each function is *exact* —
it computes its result rather than reporting a cached number — so
the test suite can assert against the values directly.

Functions:
- factor_r3329()           : CRT decomposition of X^256+1 over F_3329.
- singer_orbit_audit()     : whether F_3329^* contains a Z_7 subgroup.
- zd_graph_audit()         : zero-divisor pair graph on the 128 CRT factors.
- discrete_circle_audit()  : (2,3,7)-proportional triples among primitive
                             256-th roots of unity.

No third-party dependencies. The factorisation is structural (we know
the roots are the 128 odd powers of zeta=17 in F_3329^*) so SageMath
or sympy are not needed; the result is verified by polynomial
multiplication mod 3329.
"""

from __future__ import annotations

import json
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Sequence

Q = 3329
ZETA = 17
DEG = 256
NUM_FACTORS = 128
NTT_FACTORS_JSON = Path(__file__).parent / "mlkem_ring_factors.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n ** 0.5) + 1
    return all(n % d != 0 for d in range(3, r + 1, 2))


def _factorise(n: int) -> dict[int, int]:
    """Trial-division factorisation; returns {prime: exponent}."""
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            out[d] = e
        d += 1
    if n > 1:
        out[n] = 1
    return out


def _multiplicative_order(g: int, mod: int) -> int:
    o = 1
    cur = g % mod
    while cur != 1:
        cur = (cur * g) % mod
        o += 1
    return o


def _poly_mul_mod(a: Sequence[int], b: Sequence[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if not ai:
            continue
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % Q
    return out


# ---------------------------------------------------------------------------
# Audit line 1: CRT decomposition of R_3329 = Z_3329[X] / (X^256 + 1)
# ---------------------------------------------------------------------------


def factor_r3329() -> dict:
    """Return the CRT decomposition of R_3329 with explicit verification.

    Each factor is a quadratic ``X^2 - r_j`` with ``r_j = zeta^(2j+1)``
    for j = 0..127, ``zeta = 17`` (canonical FIPS 203 generator of the
    order-256 subgroup of F_3329^*). The 128 factors are verified
    irreducible (each ``r_j`` is a quadratic non-residue mod 3329, so
    ``X^2 - r_j`` has no root in F_3329) and their product is
    confirmed to equal ``X^256 + 1`` exactly mod 3329.

    If ``tools/mlkem_ring_factors.json`` is present, the resulting roots
    are also cross-checked against the cached values.
    """
    assert _multiplicative_order(ZETA, Q) == 256, "zeta must have order 256"

    # 17 is a quadratic non-residue mod 3329 because 17^((q-1)/2) = -1.
    seventeen_qr = pow(ZETA, (Q - 1) // 2, Q)
    seventeen_is_nonresidue = (seventeen_qr == Q - 1)

    factors = []
    for j in range(NUM_FACTORS):
        k = 2 * j + 1
        r = pow(ZETA, k, Q)
        factors.append({
            "j": j,
            "k": k,
            "root": r,
            "neg_root": (-r) % Q,
            "factor_coeffs": [(-r) % Q, 0, 1],   # X^2 + 0*X + (-r)
        })

    # Verify: the 128 roots are distinct.
    roots = [f["root"] for f in factors]
    distinct = len(set(roots)) == NUM_FACTORS

    # Verify: each X^2 - r_j is irreducible iff r_j is a non-residue.
    # All 128 roots are odd powers of zeta=17; 17 is a non-residue, so every
    # odd power is also a non-residue.
    all_irreducible = all(
        pow(f["root"], (Q - 1) // 2, Q) == Q - 1 for f in factors
    )

    # Verify: product of factors equals X^256 + 1 mod 3329.
    product = [1]
    for f in factors:
        product = _poly_mul_mod(product, f["factor_coeffs"])
    expected = [0] * (DEG + 1)
    expected[0] = 1
    expected[DEG] = 1
    product_check = product == expected

    # Cross-check against the cached JSON, if available.
    json_match = None
    if NTT_FACTORS_JSON.exists():
        cached = json.loads(NTT_FACTORS_JSON.read_text())
        cached_roots = [f["root"] for f in cached["factors"]]
        json_match = cached_roots == roots

    return {
        "ring": "Z_3329[X] / (X^256 + 1)",
        "modulus": Q,
        "degree": DEG,
        "zeta": ZETA,
        "zeta_order": 256,
        "num_factors": NUM_FACTORS,
        "factor_form": "X^2 - root",
        "seventeen_is_quadratic_nonresidue": seventeen_is_nonresidue,
        "distinct_roots": distinct,
        "all_factors_irreducible": all_irreducible,
        "product_equals_X256_plus_1": product_check,
        "json_match": json_match,
        "first_three_roots": roots[:3],
        "last_three_roots": roots[-3:],
    }


# ---------------------------------------------------------------------------
# Audit line 2: Z_7 subgroup of F_3329^*
# ---------------------------------------------------------------------------


def singer_orbit_audit() -> dict:
    """Confirm F_3329^* has no Z_7 subgroup; report the natural cyclic action."""
    q_minus_1 = Q - 1
    q_minus_1_factorisation = _factorise(q_minus_1)

    has_z7 = (q_minus_1 % 7 == 0)
    q_mod_7 = Q % 7

    # The natural cyclic action on the 128 NTT factors comes from
    # multiplication by zeta^2 (rotation of factor index j -> j+1 mod 128).
    rotor = pow(ZETA, 2, Q)
    rotor_order = _multiplicative_order(rotor, Q)
    rotor_factorisation = _factorise(rotor_order)

    return {
        "q": Q,
        "q_minus_1": q_minus_1,
        "q_minus_1_factorisation": q_minus_1_factorisation,
        "q_mod_7": q_mod_7,
        "z_7_subgroup_exists_in_F_q_star": has_z7,
        "natural_cyclic_action": "multiplication by zeta^2",
        "natural_cyclic_order": rotor_order,
        "natural_cyclic_order_factorisation": rotor_factorisation,
        "candidate_primes_with_z7_subgroup": [
            p for p in (29, 43, 71, 113, 127, 197, 211, 239) if (p - 1) % 7 == 0
        ],
    }


# ---------------------------------------------------------------------------
# Audit line 3: ZD pair graph on the 128 CRT factors
# ---------------------------------------------------------------------------


def zd_graph_audit() -> dict:
    """Confirm that R_3329 is a product of 128 fields, so its ZD graph is K_128.

    Reasoning recapped programmatically:
    - Each factor X^2 - r_j is irreducible (factor_r3329 verifies).
    - Hence each quotient F_3329[X] / (X^2 - r_j) is the field F_{3329^2}.
    - A product of 128 fields has zero divisors only between different
      factors (orthogonal idempotents). Every pair {i, j} therefore
      supports zero divisors, so the ZD pair graph on factor indices
      is the complete graph K_128.
    - Aut(K_128) = Sym(128).
    """
    rf = factor_r3329()
    each_factor_is_field = rf["all_factors_irreducible"]
    n = NUM_FACTORS
    edge_count = comb(n, 2)
    is_complete = each_factor_is_field   # by the chain of implications above

    return {
        "num_vertices": n,
        "num_edges": edge_count,
        "each_factor_is_field": each_factor_is_field,
        "graph_is_K_n": is_complete,
        "graph_label": f"K_{n}",
        "automorphism_group": f"Sym({n})",
        "automorphism_group_order_log10": _stirling_log10_factorial(n),
    }


def _stirling_log10_factorial(n: int) -> float:
    """log10(n!) via Stirling, accurate to a couple of decimal places."""
    import math
    return (n * math.log10(n) - n * math.log10(math.e)
            + 0.5 * math.log10(2 * math.pi * n))


# ---------------------------------------------------------------------------
# Audit line 4: (2,3,7) angle triples among primitive 256-th roots
# ---------------------------------------------------------------------------


def discrete_circle_audit(modulus: int = 256,
                          ratio: tuple[int, int, int] = (21, 14, 6)) -> dict:
    """Enumerate (21:14:6)-proportional triples in Z/256.

    Two domains:
    - Restricted to primitive 256-th roots (k odd). Result is exactly 0.
    - Full circle (k arbitrary). Result is 248 unordered triples.

    The brief's parity argument is also computed: ratio components
    (14, 6) are even, so no scalar m makes (14m, 6m) odd mod 256 ⇒
    no triple of primitive roots can be proportional to (21, 14, 6).
    """
    primitive_indices = [k for k in range(modulus) if k % 2 == 1]
    n_primitive = len(primitive_indices)

    primitive_triples: set[tuple[int, int, int]] = set()
    full_triples: set[tuple[int, int, int]] = set()
    for m in range(modulus):
        coords = (
            (m * ratio[0]) % modulus,
            (m * ratio[1]) % modulus,
            (m * ratio[2]) % modulus,
        )
        if len(set(coords)) < 3:
            continue
        full_triples.add(tuple(sorted(coords)))
        if all(c % 2 == 1 for c in coords):
            primitive_triples.add(tuple(sorted(coords)))

    # Parity obstruction: 14·m and 6·m are even for every m, so a
    # triple with all-odd coords is impossible.
    parity_witness = all(
        (m * ratio[1]) % 2 == 0 and (m * ratio[2]) % 2 == 0
        for m in range(modulus)
    )

    return {
        "modulus": modulus,
        "ratio_237": ratio,
        "primitive_count": n_primitive,
        "triples_in_primitives": len(primitive_triples),
        "triples_full_circle": len(full_triples),
        "parity_obstruction": parity_witness,
        "total_unordered_primitive_triples": comb(n_primitive, 3),
        "total_unordered_full_triples": comb(modulus, 3),
        "first_full_triples": sorted(full_triples)[:5],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    import pprint
    print("=== factor_r3329 ===")
    pprint.pp(factor_r3329())
    print("\n=== singer_orbit_audit ===")
    pprint.pp(singer_orbit_audit())
    print("\n=== zd_graph_audit ===")
    pprint.pp(zd_graph_audit())
    print("\n=== discrete_circle_audit ===")
    pprint.pp(discrete_circle_audit())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
