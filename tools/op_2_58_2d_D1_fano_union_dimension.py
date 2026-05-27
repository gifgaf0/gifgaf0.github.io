"""op_2_58_2d_D1_fano_union_dimension.py — Item D1 of Brief 08 (OP-2.58.2d).

Computes the EXACT F_q-dimension of the union of the seven 8D F_L subspaces,
i.e. the rank over F_q of the stacked kernel basis

    M_union = [ basis(F_{L_1}) | ... | basis(F_{L_7}) ]   (16 × 56 over F_q)

at the toy prime q = 911 and the spec prime q = 4,294,977,961.

This pins the §3.6(b) "exact dimension is fixed by the rank of the stacked
kernel basis at q" deferral to actual integers. It operates on the kernel
basis only — it does NOT execute the §2.58.B attack at spec parameters
(brief §7 discipline: D1's rank computation may use both q values).

Rank is computed by exact Gaussian elimination over F_q (modular inverses),
never floating-point SVD.

Each F_L basis is built from the kernel-involution module:
  - For a pair (a, b) (a<b in 1..7), x = e_a + e_{b+8}; the right-kernel of
    L_x (4-dimensional, per OP-2.25.2-V2) is a basis of K_{a,b}.
  - F_L (line L = {a,b,c}) is the span of K_{a,b}, K_{a,c}, K_{b,c}: 12
    generating kernel vectors whose F_q-rank is 8 (the "16→8" drop).
We extract an 8-vector F_q basis per line and stack the seven of them into the
16×56 M_union. As a cross-check the script also stacks all 7×12 = 84 raw
generators and confirms the union rank is identical (rank is basis-independent).
"""

from __future__ import annotations

import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sedenion_Fp import DIM, add_vec, basis_vec, mul_vec  # noqa: E402
from op_2252_v2_kernel_involution import lmm, rref_kernel  # noqa: E402

TOY_Q = 911
SPEC_Q = 4_294_977_961


def _kernel_vectors_modp(a: int, b: int, q: int) -> list[list[int]]:
    """Raw F_q kernel basis of K_{a,b}: the right-kernel of L_x for the
    cross-edge ZD x = e_a + e_{b+8}. Returns 4 length-16 vectors mod q."""
    x = add_vec(basis_vec(a), basis_vec(b + 8), q)
    ker = rref_kernel(lmm(x, q), q)
    return [[c % q for c in v] for v in ker]


def fano_lines(q: int) -> list[tuple[int, int, int]]:
    """The 7 Fano lines {a,b,c} ⊂ {1..7} read from e_a·e_b = ±e_c."""
    lines = set()
    for a, b in combinations(range(1, 8), 2):
        prod = mul_vec(basis_vec(a), basis_vec(b), q)
        nz = [i for i, v in enumerate(prod) if v % q != 0]
        assert len(nz) == 1, f"e_{a}·e_{b} not single-term: {nz}"
        lines.add(frozenset({a, b, nz[0]}))
    assert len(lines) == 7
    return sorted((tuple(sorted(L)) for L in lines))


def rank_modp(columns: list[list[int]], q: int) -> int:
    """Exact rank over F_q of the matrix whose COLUMNS are `columns`
    (each a length-DIM vector). Gaussian elimination with modular inverses."""
    # Work on the rows of the transpose: each input column becomes a row.
    rows = [[c % q for c in col] for col in columns]
    n_cols = DIM
    r = 0
    n_rows = len(rows)
    for c in range(n_cols):
        piv = None
        for i in range(r, n_rows):
            if rows[i][c] % q != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], -1, q)
        rows[r] = [(x * inv) % q for x in rows[r]]
        for i in range(n_rows):
            if i != r and rows[i][c] % q != 0:
                f = rows[i][c]
                rows[i] = [(rows[i][j] - f * rows[r][j]) % q for j in range(n_cols)]
        r += 1
        if r == n_rows:
            break
    return r


def _basis_of_columns(columns: list[list[int]], q: int) -> list[list[int]]:
    """Return a maximal F_q-independent subset of `columns` (preserving order)."""
    chosen: list[list[int]] = []
    cur_rank = 0
    for col in columns:
        trial = chosen + [col]
        if rank_modp(trial, q) > cur_rank:
            chosen.append(col)
            cur_rank += 1
    return chosen


def compute(q: int) -> dict:
    lines = fano_lines(q)
    pairs = list(combinations(range(1, 8), 2))

    # Sanity: each K_{a,b} is 4-dimensional over F_q.
    pair_dims = {}
    for (a, b) in pairs:
        kv = _kernel_vectors_modp(a, b, q)
        pair_dims[(a, b)] = rank_modp(kv, q)

    # Build each F_L (12 generators) and its dimension; extract an 8-vector basis.
    fano_dims = {}
    union_56_cols: list[list[int]] = []
    union_all_gens: list[list[int]] = []
    for (a, b, c) in lines:
        gens: list[list[int]] = []
        for (i, j) in [(a, b), (a, c), (b, c)]:
            gens.extend(_kernel_vectors_modp(i, j, q))
        fano_dims[(a, b, c)] = rank_modp(gens, q)
        basis = _basis_of_columns(gens, q)
        union_56_cols.extend(basis)
        union_all_gens.extend(gens)

    rank_union_56 = rank_modp(union_56_cols, q)
    rank_union_all = rank_modp(union_all_gens, q)

    return {
        "q": q,
        "pair_dims": pair_dims,
        "fano_dims": fano_dims,
        "n_union_cols": len(union_56_cols),
        "n_all_gens": len(union_all_gens),
        "rank_union_56": rank_union_56,
        "rank_union_all_generators": rank_union_all,
    }


def _report(res: dict) -> None:
    q = res["q"]
    print("=" * 70)
    print(f"D1 — F_L union dimension at q = {q}")
    print("=" * 70)
    pd = set(res["pair_dims"].values())
    fd = set(res["fano_dims"].values())
    print(f"  K_(a,b) dims (all 21 pairs): {sorted(pd)}  "
          f"(expected {{4}}: {'OK' if pd == {4} else 'MISMATCH'})")
    print(f"  F_L dims (all 7 lines):      {sorted(fd)}  "
          f"(expected {{8}}: {'OK' if fd == {8} else 'MISMATCH'})")
    print(f"  M_union shape: 16 × {res['n_union_cols']} "
          f"(8 basis vectors × 7 lines)")
    print(f"  rank(M_union) over F_{q}            = {res['rank_union_56']}")
    print(f"  rank(all {res['n_all_gens']} raw generators)  = "
          f"{res['rank_union_all_generators']} (cross-check, must match)")
    assert res["rank_union_56"] == res["rank_union_all_generators"], \
        "basis-extracted union rank disagrees with raw-generator union rank"


def main() -> None:
    toy = compute(TOY_Q)
    _report(toy)
    print()
    spec = compute(SPEC_Q)
    _report(spec)
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  rank_911  = {toy['rank_union_56']}")
    print(f"  rank_spec = {spec['rank_union_56']}  (q = {SPEC_Q})")
    if toy["rank_union_56"] != spec["rank_union_56"]:
        print("  WARNING: toy and spec ranks DIFFER — flag for §3.6(b) patch.")


if __name__ == "__main__":
    main()
