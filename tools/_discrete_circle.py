"""(2,3,7) hyperbolic-triangle angle audit on F_3329's primitive 256-th roots.

The 256-th roots of unity in F_3329 are ζ^k, k = 0..255, with ζ = 17.
The *primitive* roots are those with gcd(k, 256) = 1, i.e. k odd; there
are φ(256) = 128 of them.

Treating the discrete log k as an angle (in units of 2π/256), the
hyperbolic (2,3,7) triangle has angles π/2 : π/3 : π/7 = 21 : 14 : 6
in units of π/42. We look for unordered triples {k₁, k₂, k₃} of
distinct primitive 256-th roots whose discrete logs are proportional
to (21, 14, 6) modulo 256, allowing arbitrary scalar `m ∈ Z/256` and
arbitrary permutation of the three coordinates.

For each candidate scalar `m` we form `(21m, 14m, 6m) mod 256`. The
triple is an admissible "primitive-root (2,3,7) triple" iff all three
coordinates are odd (so each lies in the primitive subset) and the
three coordinates are distinct. We count both
- the number of *ordered* triples (m, position permutation),
- the number of *unordered* admissible triples (i.e. distinct sets).

Comparison null: for unordered triples drawn uniformly at random from
the 128 primitive roots, the expected number that exactly match the
proportion (21:14:6) under the same definition is computed by the
same enumeration over Z/256 (without the parity restriction) divided
by the corresponding ratio of triple counts.
"""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path

MOD = 256
RATIO = (21, 14, 6)


def primitives() -> list[int]:
    return [k for k in range(MOD) if k % 2 == 1]


def enumerate_proportional_triples(modulus: int = MOD,
                                   ratio: tuple[int, int, int] = RATIO,
                                   restrict_odd: bool = True) -> list[tuple[int, int, int]]:
    """Return unordered (sorted) tuples (a, b, c) with all distinct,
    such that there exists m and a permutation π of (a,b,c) so
    (m·ratio[0], m·ratio[1], m·ratio[2]) mod modulus == π.

    If ``restrict_odd``, only triples with all three coords odd are
    returned (i.e., all three lie in the primitive 256-th-root index set).
    """
    found = set()
    for m in range(modulus):
        a, b, c = (m * ratio[0]) % modulus, (m * ratio[1]) % modulus, (m * ratio[2]) % modulus
        coords = (a, b, c)
        if restrict_odd and not all(x % 2 == 1 for x in coords):
            continue
        if len(set(coords)) < 3:
            continue
        found.add(tuple(sorted(coords)))
    return sorted(found)


def count_ordered_proportional_via_perms(modulus: int = MOD,
                                         ratio: tuple[int, int, int] = RATIO,
                                         restrict_odd: bool = True) -> int:
    """Each unordered triple in the result of `enumerate_proportional_triples`
    can correspond to multiple `(m, permutation)` pairs; we count the total."""
    n = 0
    for m in range(modulus):
        base = (
            (m * ratio[0]) % modulus,
            (m * ratio[1]) % modulus,
            (m * ratio[2]) % modulus,
        )
        if restrict_odd and not all(x % 2 == 1 for x in base):
            continue
        if len(set(base)) < 3:
            continue
        n += 1
    return n


def main() -> int:
    odd_indices = primitives()
    assert len(odd_indices) == 128

    triples_in_primitives = enumerate_proportional_triples(restrict_odd=True)
    triples_full_circle = enumerate_proportional_triples(restrict_odd=False)
    n_in_primitives_ordered = count_ordered_proportional_via_perms(restrict_odd=True)
    n_full_circle_ordered = count_ordered_proportional_via_perms(restrict_odd=False)

    # Total possible triple counts.
    from math import comb
    total_unordered_primitives = comb(128, 3)
    total_unordered_full = comb(256, 3)

    # Uniform-random null: probability a uniformly random unordered triple
    # of primitive 256-th roots is exactly (21:14:6)-proportional ≈
    # |triples_in_primitives| / C(128, 3).
    p_uniform_in_primitives = (
        len(triples_in_primitives) / total_unordered_primitives
    )
    p_uniform_full = len(triples_full_circle) / total_unordered_full

    payload = {
        "modulus": MOD,
        "ratio_237": RATIO,
        "primitives_count": len(odd_indices),
        "unordered_proportional_triples_in_primitives": len(triples_in_primitives),
        "unordered_proportional_triples_full_circle": len(triples_full_circle),
        "ordered_proportional_triples_in_primitives": n_in_primitives_ordered,
        "ordered_proportional_triples_full_circle": n_full_circle_ordered,
        "total_unordered_primitive_triples": total_unordered_primitives,
        "total_unordered_full_triples": total_unordered_full,
        "uniform_match_rate_primitives": p_uniform_in_primitives,
        "uniform_match_rate_full": p_uniform_full,
        "examples_in_primitives": triples_in_primitives[:8],
        "examples_full_circle": triples_full_circle[:8],
    }
    Path("tools/discrete_circle_audit.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    for k, v in payload.items():
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
