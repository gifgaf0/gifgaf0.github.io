# OP-2.25.2-V2 — Result: Kernel Structure is the Fano Plane Co-Line Structure

**Date:** May 16, 2026
**Status:** Closed. R2 result, fully empirical over 84 ZDs in F_{911} and
extended to F_{2731} by the repo-integration brief (this commit).
**Supersedes:** The naive "complement to 14" / "(a,b) → (9−b, 9−a)" conjecture
from §2.25.2-V, which was extrapolated from a single sample point and is
falsified at scale.

---

## Claim verified

For every two-term sedenion cross-edge zero-divisor x = e_a ± e_{b+8}
(a, b ∈ {1..7}, a ≠ b, signs in {±1}) over F_{911} and F_{2731}:

1. **rank(L_x) = 12** (kernel dimension 4) — 84/84 confirmed.
2. **Every kernel basis vector is itself a clean two-term cross-edge ZD** —
   84/84 confirmed, with coefficients in {±1} after normalization.
3. **The kernel pair-set depends only on the unordered {a, b}** — sign of x
   does not affect which pairs appear in the kernel. 21/21 unordered pairs
   confirmed consistent across their 4 signed representatives.
4. **Kernel pairs are disjoint from the x pair** — 84/84 confirmed.

## The actual structure

For each unordered x-pair {i_x, j_x} ⊂ {1..7}, the kernel basis lives on
exactly **two** unordered interior pairs {a', b'}, {a'', b''}. The triple
of pairs

    { {i_x, j_x}, {a', b'}, {a'', b''} }

is always a **partition of {1..7} \ {m}** for a unique missing element m.

The seven partitions (indexed by missing element):

| Missing m | Triple of pairs                |
|-----------|--------------------------------|
| 1         | {2,3}, {4,5}, {6,7}            |
| 2         | {1,3}, {4,6}, {5,7}            |
| 3         | {1,2}, {4,7}, {5,6}            |
| 4         | {1,5}, {2,6}, {3,7}            |
| 5         | {1,4}, {2,7}, {3,6}            |
| 6         | {1,7}, {2,4}, {3,5}            |
| 7         | {1,6}, {2,5}, {3,4}            |

## Identification with the Fano plane

The 7 Fano lines on the octonion imaginaries {e_1..e_7} (recovered
empirically from the Cayley-Dickson multiplication: e_a · e_b = ±e_c
defines line {a, b, c}):

    {1,2,3}, {1,4,5}, {1,6,7}, {2,4,6}, {2,5,7}, {3,4,7}, {3,5,6}

**Theorem (verified):** A pair {i, j} appears in the partition labeled "missing m"
*if and only if* {i, j, m} is a Fano line.

Equivalently: the three pairs in "partition missing m" are exactly the three
Fano lines through the point m, with the point m itself deleted from each line.

## What this says about the boundary decomposition

For x = e_a + e_{b+8} with interior pair {a, b}, let L = {a, b, m} be the
unique Fano line containing {a, b}, where m is the third point on the line.

**Then ker(L_x) lies entirely in the cross-edge ZD subspace spanned by
the other two Fano lines through m.**

The kernel structure is therefore Fano-line-aligned at every level:

- x sits on a Fano line (because (a, b) determines a Fano line uniquely)
- The kernel of L_x is supported on the two **other** Fano lines through the
  third point of x's own line
- The 4-dimensional kernel is exactly the 4 signed two-term ZDs you can build
  from those two other lines (2 pairs × 2 signs = 4)

## Framework reading

The §2.25.2 framework picture had K_{7,7}-minus-identity-matching as the
abstract boundary skin. The 21 cross-edges in the interior factor (= 21
unordered pairs (a,b)) are now identified with the 21 = C(7,2) edges of the
**Johnson graph J(7,2)** — and the kernel-involution puts a graded structure
on them via the Fano plane:

- Each of the 21 cross-edges sits on exactly **one** Fano line.
- The 7 Fano lines partition the 21 cross-edges into **7 groups of 3**.
- Within each group of 3, the three cross-edges share the same "missing third
  point" m, and their corresponding L_x kernels live on the cross-edges of the
  other two Fano lines through m.

This is a clean **Fano-plane refinement** of §2.25.2's bare cross-edge count.
The R2 statement promotes from "84 stress channels" to "84 stress channels
organized as 21 cross-edges × 4 signs, with the 21 cross-edges Fano-line-graded
into 7 groups of 3."

## Implications for OP-C7-4 (SLWE-with-native-ZD-noise)

This result sharpens the construction problem stated in §2.54:

A SLWE variant where the per-coordinate noise is drawn from ker(L_x) for a
random ZD x **does not produce a generic 4-D noise space per coordinate**.
The noise space is selected by x's Fano-line and is supported on the 4
cross-edges of the **other two Fano lines through the third point**.

This is a 7-state classifier on the noise channel: knowing which Fano line
the ZD x sits on tells you which 8 of the 21 cross-edges (= 4 × 2 from the
other two lines) carry the kernel mass.

For the cryptographic construction this is **double-edged**:

- *Possibly useful:* The structure may allow algebraic shielding — an
  attacker who tries to project the noise to a smaller subspace must guess
  the correct Fano-line class to align with the actual support.
- *Possibly fatal:* If the Fano-line class leaks (e.g., via the public matrix
  A's structure), the noise space drops from 4 dimensions to a known 4D
  subspace, and standard LWE distinguishers may apply.

Activating OP-C7-4 step 4 (cryptanalysis) requires settling which side of
this edge the construction lands on. The empirical structure here is the
necessary input for that analysis; it does not by itself decide the
question.

## G_2 orbit structure (Task 6 note, repo-integration brief)

The G_2 = Aut(O) action on octonion imaginaries permutes Fano lines.
Per the kernel identification, ker(L_x) is determined by the Fano line
containing x's interior pair. Therefore G_2 acts compatibly: g · L_x =
L_{g·x} and g maps ker(L_x) bijectively to ker(L_{g·x}). The 84 → 84 ZD
map under G_2 is by definition transitive on lines and 3-cycles within
a line, so the action covers all 84 elements in a small number of orbits.
Detailed orbit count is OP-2.25.2-V1's natural setting.

## Status flags

- **(1)-(4) above:** R2, computationally verified over all 84 elements at
  p = 911 and p = 2731 (commit 167556e cross-checks rank=12 / ker-dim=4
  at the 168-sign-variant level using an independent enumerator).
- **Fano-line identification:** R2, structurally clean and matches the
  Cayley-Dickson construction of octonions. Verified by
  ``tools/fano_line_identification.py`` at both primes; the 21 → kernel
  pair-set mapping is identical across p=911 and p=2731, supporting the
  T2 prediction that the structure holds for all mod-455 primes.
- **R1 promotion path:** Prove the rank-12 + Fano-line-aligned-kernel
  structure symbolically (over Q, not just over F_p), via the Moreno
  characterization of sedenion ZDs and the action of the octonion
  automorphism group G_2 on the imaginaries. This is OP-2.25.2-V1
  from §2.25.2-V, with the kernel structure now made specific.
- **OP-2.25.2-V3 (new, opened by this brief):** Verify that the
  Fano-line structure of L_x kernels lifts to the 3-term and higher-term
  ZDs (the remainder of the 168 = 84 × 2 sedenion ZDs beyond the
  two-term cross-edge ones).

## Reproducibility

Scripts at ``tools/`` (repo paths; updated from the session's
``/home/claude/sqt/`` paths during integration):

- ``tools/sedenion_Fp.py`` — Cayley-Dickson sedenion arithmetic mod p.
  Pre-builds the 16×16 multiplication table at module load. Verified
  byte-identical to the session's straight-CD build on all 256 basis-pair
  products at p=911 (A/B test recorded in the integration commit).
- ``tools/op_2252_v2_kernel_involution.py`` — the universal 84-element
  check. CLI: ``python3 tools/op_2252_v2_kernel_involution.py [p]``.
  Repo-integration tweaks: ``sys.path`` uses the script's own directory;
  ``main`` accepts a prime so Task 4 (verification at p=2731) re-uses the
  module unchanged.
- ``tools/fano_line_identification.py`` — Fano-line extraction + per-pair
  kernel-pair-set prediction + assertion against the kernel-involution
  output. CLI: ``python3 tools/fano_line_identification.py [p]``.
- ``tools/sedenion_lwe_check.py`` (commit ``167556e``) — independent
  rank-12 universality check at the 168-sign-variant level. Complements
  item (1) of this verdict; uses ``find_canonical_zd_quadruples`` from
  ``sedenion_audit.py`` rather than the cross-edge enumerator used by
  ``op_2252_v2_kernel_involution.py``.

The session writeup additionally referenced ``zd_rank_check.py`` as a
"recovered from project" probe; that file is not present in the repo's
history (verified by ``git log --all -- tools/zd_rank_check.py`` returning
empty). ``tools/sedenion_lwe_check.py`` from commit ``167556e`` is the
nearest functional substitute and is what backs the rank-12 universality
claim in this repo.

---

*End of OP-2.25.2-V2 result.*
