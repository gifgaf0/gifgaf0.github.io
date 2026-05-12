"""Subgroup-chain × ZD labelling probe — chain enumeration.

Brief: CLAUDE_CODE_BRIEF_02_CHAIN_ZD (Section §1.2 of
SLWE_Prime_Master_v2.md is the reference). Open problem under
investigation: OP §2.24.2.

Setup (from the master doc §1.2):

- The 84 sedenion zero-divisor pairs over F_911 are enumerated by
  ``sedenion_audit.find_canonical_zd_quadruples``. Each "pair" is
  really an unordered pair of unordered index-pairs
  ``((a, b), (c, d))`` with ``a, b, c, d ∈ {1..7, 9..15}``,
  ``{a, b} ∩ {c, d} = ∅``, and ``a < b``, ``c < d``,
  ``(a, b) < (c, d)`` lex. There are exactly 84 such quadruples.
- The ZD graph on the 14 active indices is K_{7,7} minus the
  perfect matching ``{(i, i+8) : i = 1..7}``.

Subgroup chain (per the brief):

- PSL(2, 7) acts on the Fano plane PG(2, 2) — the 7 nonzero vectors
  of F_2³. We identify those 7 vectors with {e_1, ..., e_7} via the
  binary encoding ``(b₂, b₁, b₀) ↔ 4 b₂ + 2 b₁ + b₀``, and extend
  the action to {e_9, ..., e_15} by the index shift ``i ↦ i + 8``.
  This gives 168 permutations of the 14-element ground set.
- The stabilizer of any single Fano point in this action has index
  168 / 7 = 24, i.e. ``≅ S_4``. There are 7 such S_4 conjugates,
  one per Fano point.
- Inside each S_4, the index-2 subgroup of even permutations
  (induced action on the 6 non-fixed Fano points) is the unique A_4
  subgroup. There are therefore 7 chains
  ``A_4_i < S_4_i < PSL(2, 7)``.

Labelling (per the brief):

- For each chain ``A_4_i < S_4_i < PSL(2, 7)``, A_4_i acts on the
  84 ZD quadruples. Generically (and confirmed empirically here)
  |A_4_i| = 12 acts freely, partitioning the 84 quadruples into
  7 orbits of size 12. The orbit ID (0..6, in lex order of orbit
  representatives) is the "label" of each quadruple under that
  chain.

Outputs:

- ``tools/chain_zd_manifest.json`` — for each of the 7 chains, the
  84 ``[quad, label]`` assignments, plus the elements of A_4_i.
- Whether the full PSL(2, 7) action preserves the ZD-quadruple set
  (extends OP §2.24.1's Z_7 confirmation to all 168 elements).
- Whether Aut(MultTable) is *strictly* larger than PSL(2, 7), as a
  spot-check sampling outside the PSL(2, 7) image.
"""

from __future__ import annotations

import json
import sys
from itertools import product
from pathlib import Path

# Existing modules (we re-use, do not reimplement).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sedenion_Fp import mul_vec, basis_vec, DIM as SED_DIM  # noqa: E402
from sedenion_audit import find_canonical_zd_quadruples  # noqa: E402


FANO_POINTS = list(range(1, 8))   # 1..7 (octonion imaginaries)
SECOND_COPY = list(range(9, 16))  # 9..15 (sedenion-second-copy imaginaries)
GROUND_SET = FANO_POINTS + SECOND_COPY   # 14-element active basis
P_DEFAULT = 911


# ---------------------------------------------------------------------------
# GL(3, F_2) ≅ PSL(2, 7) action on the Fano plane
# ---------------------------------------------------------------------------


def _f2_vec(idx: int) -> tuple[int, int, int]:
    """1..7 → (b₂, b₁, b₀)."""
    return ((idx >> 2) & 1, (idx >> 1) & 1, idx & 1)


def _vec_to_idx(v: tuple[int, int, int]) -> int:
    """(b₂, b₁, b₀) → 1..7."""
    return 4 * v[0] + 2 * v[1] + v[2]


def _mat_vec_f2(M: list[list[int]], v: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((M[i][0] * v[0] + M[i][1] * v[1] + M[i][2] * v[2]) & 1
                 for i in range(3))


def _rank_mod2(M: list[list[int]]) -> int:
    A = [row[:] for row in M]
    rank = 0
    for c in range(3):
        piv = next((r for r in range(rank, 3) if A[r][c]), None)
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        for r in range(3):
            if r != rank and A[r][c]:
                A[r] = [(A[r][j] ^ A[rank][j]) for j in range(3)]
        rank += 1
    return rank


def build_psl_2_7_perms() -> list[dict[int, int]]:
    """Return 168 permutations of {1..7} from GL(3, F_2)."""
    perms: list[dict[int, int]] = []
    seen: set[tuple[int, ...]] = set()
    for entries in product((0, 1), repeat=9):
        M = [list(entries[3 * i:3 * i + 3]) for i in range(3)]
        if _rank_mod2(M) != 3:
            continue
        perm = {i: _vec_to_idx(_mat_vec_f2(M, _f2_vec(i))) for i in range(1, 8)}
        sig = tuple(perm[i] for i in range(1, 8))
        if sig in seen:
            continue
        seen.add(sig)
        perms.append(perm)
    assert len(perms) == 168, len(perms)
    return perms


def extend_to_ground_set(perm: dict[int, int]) -> dict[int, int]:
    """Extend a permutation of {1..7} to {1..7, 9..15} by ``i ↦ i+8``."""
    full = dict(perm)
    for i in range(1, 8):
        full[8 + i] = 8 + perm[i]
    return full


# ---------------------------------------------------------------------------
# Action on ZD quadruples; preservation check
# ---------------------------------------------------------------------------


def apply_perm_to_pair(perm: dict[int, int], pair: tuple[int, int]) -> tuple[int, int]:
    return tuple(sorted((perm[pair[0]], perm[pair[1]])))


def apply_perm_to_quad(perm: dict[int, int],
                       quad: tuple[tuple[int, int], tuple[int, int]]
                       ) -> tuple[tuple[int, int], tuple[int, int]]:
    p1 = apply_perm_to_pair(perm, quad[0])
    p2 = apply_perm_to_pair(perm, quad[1])
    return tuple(sorted((p1, p2)))


def preserves_quad_set(perm: dict[int, int],
                       quads: set[tuple]) -> bool:
    return all(apply_perm_to_quad(perm, q) in quads for q in quads)


# ---------------------------------------------------------------------------
# Subgroup chain: stabilizers and A_4 inside each S_4
# ---------------------------------------------------------------------------


def s4_stabilizer(perms_full: list[dict[int, int]],
                  fixed: int) -> list[dict[int, int]]:
    return [p for p in perms_full if p[fixed] == fixed]


def _compose(p1: dict[int, int], p2: dict[int, int]) -> dict[int, int]:
    return {k: p1[p2[k]] for k in p2}


def _inverse(p: dict[int, int]) -> dict[int, int]:
    return {v: k for k, v in p.items()}


def _perm_sig(p: dict[int, int]) -> tuple:
    return tuple(sorted(p.items()))


def _close_group(seed_perms: list[dict[int, int]]) -> list[dict[int, int]]:
    """Take a set of permutations and return the subgroup they generate."""
    table = {_perm_sig(p): p for p in seed_perms}
    changed = True
    while changed:
        changed = False
        items = list(table.values())
        for a in items:
            for b in items:
                c = _compose(a, b)
                sig = _perm_sig(c)
                if sig not in table:
                    table[sig] = c
                    changed = True
    return list(table.values())


def a4_within_s4(s4: list[dict[int, int]], fixed: int) -> list[dict[int, int]]:
    """A_4 = [S_4, S_4], the commutator subgroup.

    For an abstract S_4 sitting inside PSL(2, 7), the "sign" homomorphism
    that picks out A_4 is the abelianisation S_4 → Z/2. The commutator
    subgroup [S_4, S_4] is the kernel of this map. For S_4 it is A_4
    (the unique index-2 subgroup), exhibited as the subgroup generated
    by all commutators ``g h g⁻¹ h⁻¹``.
    """
    commutators: list[dict[int, int]] = []
    for g in s4:
        for h in s4:
            commutators.append(_compose(_compose(_compose(g, h), _inverse(g)),
                                         _inverse(h)))
    a4 = _close_group(commutators)
    assert len(a4) == 12, len(a4)
    return a4


# ---------------------------------------------------------------------------
# Orbit-based labelling
# ---------------------------------------------------------------------------


def orbits_of_group_on_quads(group: list[dict[int, int]],
                              quads: set[tuple]) -> list[list[tuple]]:
    seen: set[tuple] = set()
    orbits: list[list[tuple]] = []
    for q in sorted(quads):
        if q in seen:
            continue
        orbit = {q}
        frontier = [q]
        while frontier:
            cur = frontier.pop()
            for g in group:
                nq = apply_perm_to_quad(g, cur)
                if nq not in orbit:
                    orbit.add(nq)
                    frontier.append(nq)
        for x in orbit:
            seen.add(x)
        orbits.append(sorted(orbit))
    return orbits


def labelling_for_chain(a4: list[dict[int, int]], quads: set[tuple]
                        ) -> tuple[dict[tuple, int], list[list[tuple]]]:
    orbits = orbits_of_group_on_quads(a4, quads)
    # Sort orbits by their lex-smallest element so labels are deterministic.
    orbits.sort(key=lambda o: o[0])
    label_of: dict[tuple, int] = {}
    for label, orbit in enumerate(orbits):
        for q in orbit:
            label_of[q] = label
    return label_of, orbits


# ---------------------------------------------------------------------------
# Aut(MultTable) spot-check: search for a permutation outside PSL(2,7) that
# preserves the sedenion multiplication table up to sign
# ---------------------------------------------------------------------------


def _build_signed_mult_table(p: int) -> dict[tuple[int, int], tuple[int, int]]:
    """e_i · e_j = sign · e_k mapping for i, j ∈ 1..15. Returns
    ``(i, j) -> (k, sign)`` where ``sign ∈ {+1, -1}`` and ``k ∈ 0..15``.
    """
    table: dict[tuple[int, int], tuple[int, int]] = {}
    for i in range(1, 16):
        for j in range(1, 16):
            prod = mul_vec(basis_vec(i), basis_vec(j), p)
            nz = [(idx, v) for idx, v in enumerate(prod) if v != 0]
            if not nz:
                # i == j: e_i² = -1 = (0, -1)
                table[(i, j)] = (0, -1)
                continue
            assert len(nz) == 1, f"unexpected non-basis product at {i},{j}"
            idx, v = nz[0]
            sign = 1 if v == 1 else (-1 if v == p - 1 else None)
            assert sign is not None, f"unexpected coefficient at {i},{j}: {v}"
            table[(i, j)] = (idx, sign)
    return table


def preserves_signed_mult_table(perm_full: dict[int, int],
                                table: dict[tuple[int, int], tuple[int, int]]
                                ) -> bool:
    """Does ``perm`` (on {1..15} \\ {8}) preserve the signed mult table?

    We require ``perm(e_i) · perm(e_j) = ± perm(e_i · e_j)`` for every
    pair (i, j) in the perm's domain. The "sign" is allowed to vary
    per (i, j) — Aut up to overall sign, which is the natural notion
    on a Z₂-graded algebra.
    """
    def img(k):
        if k == 0:
            return 0   # e_0 fixed
        if k == 8:
            return 8   # e_8 fixed (we never permute it in this brief)
        return perm_full.get(k, k)
    for (i, j), (k, _sign) in table.items():
        if i == 8 or j == 8:
            continue
        ii, jj = img(i), img(j)
        kk_expected = img(k)
        # Compute the product perm(e_i) · perm(e_j) via the table.
        if ii == 0 or jj == 0:
            actual_k = jj if ii == 0 else ii
        elif (ii, jj) in table:
            actual_k, _ = table[(ii, jj)]
        else:
            return False
        if actual_k != kk_expected:
            return False
    return True


def search_aut_outside_psl(perms_full: list[dict[int, int]],
                            quads: set[tuple],
                            table: dict[tuple[int, int], tuple[int, int]],
                            n_samples: int = 5000) -> dict:
    """Random sample of ZD-graph-respecting permutations and test mult-table
    preservation. The ZD graph K_{7,7}-minus-matching has Aut = S_7 ≀ Z_2 of
    order 7!² · 2 ≈ 5·10⁷, so we can't enumerate; we sample randomly.

    A permutation that preserves K_{7,7}-minus-matching either (a) preserves
    both halves {1..7} and {9..15} (S_7 × S_7 minus the matching constraint),
    or (b) swaps them (involving the Z_2 factor). For each candidate we test
    mult-table preservation.
    """
    import random as _r
    psl_signatures = {tuple(sorted(p.items())) for p in perms_full}
    rng = _r.Random(0xc2a)
    n_psl_hits = 0
    n_extra_hits = 0
    extra_examples = []
    fano = FANO_POINTS[:]
    second = SECOND_COPY[:]
    for _ in range(n_samples):
        # Sample a random ZD-graph-respecting permutation.
        if rng.random() < 0.5:
            pi = list(fano)
            rng.shuffle(pi)
            pi2 = [8 + i for i in pi]   # synced shift (preserves matching)
            perm = {i: pi[idx] for idx, i in enumerate(fano)}
            perm.update({i: pi2[idx] for idx, i in enumerate(second)})
        else:
            # Swap halves: e_i ↔ e_{i+8}.
            pi = list(fano)
            rng.shuffle(pi)
            perm = {i: 8 + pi[idx] for idx, i in enumerate(fano)}
            perm.update({8 + i: pi[idx] for idx, i in enumerate(fano)})
        if not preserves_quad_set(perm, quads):
            continue
        if not preserves_signed_mult_table(perm, table):
            continue
        sig = tuple(sorted(perm.items()))
        if sig in psl_signatures:
            n_psl_hits += 1
        else:
            n_extra_hits += 1
            if len(extra_examples) < 3:
                extra_examples.append(perm)
    return {
        "samples": n_samples,
        "in_psl_count": n_psl_hits,
        "outside_psl_count": n_extra_hits,
        "extra_examples": extra_examples,
    }


# ---------------------------------------------------------------------------
# Main: build manifest
# ---------------------------------------------------------------------------


def quad_key(q: tuple[tuple[int, int], tuple[int, int]]) -> str:
    (a, b), (c, d) = q
    return f"{a},{b}|{c},{d}"


def perm_to_tuple(perm: dict[int, int]) -> list[list[int]]:
    return [[k, perm[k]] for k in sorted(perm.keys())]


def main() -> int:
    p = P_DEFAULT
    print(f"loading 84 ZD quadruples over F_{p} ...")
    quads_set = find_canonical_zd_quadruples(p)
    assert len(quads_set) == 84
    quads_sorted = sorted(quads_set)

    print("building PSL(2,7) ≅ GL(3, F_2) (168 elements) ...")
    perms_7 = build_psl_2_7_perms()
    perms_full = [extend_to_ground_set(p_) for p_ in perms_7]

    print("verifying full PSL(2,7) preserves the 84 ZD quadruples ...")
    n_preserving = sum(1 for p_ in perms_full
                       if preserves_quad_set(p_, quads_set))
    psl_preserves_zd = (n_preserving == 168)
    print(f"  preserving / total = {n_preserving} / 168")
    if not psl_preserves_zd:
        print("  ! full PSL(2,7) does NOT preserve all ZD quadruples")
        print("  ! OP §2.24.1 negative result — recorded in manifest")

    print("building 7 chains (S_4 point-stabilizers, A_4 subgroups) ...")
    chains = []
    for fp in FANO_POINTS:
        s4 = s4_stabilizer(perms_full, fp)
        assert len(s4) == 24, len(s4)
        a4 = a4_within_s4(s4, fp)
        label_of, orbits = labelling_for_chain(a4, quads_set)
        n_labels = len(set(label_of.values()))
        chains.append({
            "fixed_point": fp,
            "n_a4_orbits": len(orbits),
            "orbit_sizes": [len(o) for o in orbits],
            "labels": [{"quad": quad_key(q), "label": label_of[q]}
                       for q in quads_sorted],
        })
        print(f"  Fano point {fp}: A_4 has {len(orbits)} orbits "
              f"(sizes {sorted(set(len(o) for o in orbits))}); "
              f"labels used: 0..{n_labels - 1}")

    print("spot-checking whether Aut(MultTable) > PSL(2,7) ...")
    table = _build_signed_mult_table(p)
    aut_check = search_aut_outside_psl(perms_full, quads_set, table,
                                        n_samples=5000)
    print(f"  random samples: in-PSL hits = {aut_check['in_psl_count']}, "
          f"outside-PSL hits = {aut_check['outside_psl_count']}")

    manifest = {
        "prime": p,
        "ground_set": GROUND_SET,
        "num_quads": len(quads_sorted),
        "psl_preserves_zd_quads": psl_preserves_zd,
        "psl_preserving_count": n_preserving,
        "psl_order": 168,
        "chains": chains,
        "aut_table_spot_check": {
            "samples": aut_check["samples"],
            "in_psl_count": aut_check["in_psl_count"],
            "outside_psl_count": aut_check["outside_psl_count"],
            "aut_strictly_larger_than_psl": aut_check["outside_psl_count"] > 0,
            "extra_examples": [perm_to_tuple(e) for e in aut_check["extra_examples"]],
        },
    }
    out = Path("tools/chain_zd_manifest.json")
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {out}: {len(chains)} chains, {len(quads_sorted)} quads each")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
