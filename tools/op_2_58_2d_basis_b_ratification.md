# op_2_58_2d_basis_b_ratification.md — Brief 10.6 Item 1

**Decision**: §3.6(b) Fano-projected basis is realised as **reading (I)
F_L-restriction**. Rejected: reading (II) augmentation, reading (III)
quotient. Empirically established by toy-scale comparison at k=7, q=911,
β=30 across 3 seeds (§3 below).

**Anchor**: Brief 10.6 §2. Frozen pre-reg §3.6(b). D1 (Brief 08) rank-14 F_L
union. §2.58.B.1 / OP-2.58.B.card chirality framing.

---

## §1. Candidate readings

§3.6(b) reads: "lattice basis pre-projected onto the union of the seven 8D
F_L subspaces, using the kernel-basis output of
`op_2252_v2_kernel_involution.py`." D1 (Brief 08) pinned the F_L union
F_q-rank at 14 (at q=911 and q=SPEC_Q). Three geometrically distinct
realisations were considered (Brief 10.6 §2.2):

- **(I) Restriction**: replace the e-side q·I_n rows of basis (a) with q·F_L
  per block. The attacker works inside the 14-dim-per-block sublattice where
  the noise lives. Ambient e-side rank: 14k vs 16k. Discards the F_L⊥
  direction.

- **(II) Augmentation**: keep basis (a) intact and prepend 14·k extra rows
  (v at block-i e-position, 0, 0), with v an UNSCALED F_L basis vector. The
  lattice is enriched on the e-side: Z·F_L per block (free) plus qZ on the
  full 16-dim ambient. The attacker "has the full problem plus the F_L hint."

- **(III) Quotient**: project to the 2-dim-per-block F_L⊥ complement, on the
  theory that if the noise lives in F_L, the signal lives in F_L⊥. Rejected
  on prose grounds: §3.6(b) reads "onto" the F_L, not "out of" it. Not
  toy-tested.

## §2. Criterion: worst-case-for-defender

§3.6(b) names basis (b) as "the basis built when the attacker is given the
Fano-line structure as a hint." Ratification picks whichever of (I)/(II)
maximises attacker power under the frozen §3.3.1 cutoff convention
(N=2.0×min_norm, baseline 1/21≈0.0476 chance pair-recovery).

## §3. Toy-scale evidence

Comparison harness: `gen_spec_instance(q=911, k=7, σ=2, rng=seed)` with
trapdoor `pair_21`; build each basis; LLL + BKZ-β=30 (fpylll, `float_type="ld"`,
`max_loops=8`); classify e-slice of each short row (N=2.0×min_norm) with
`FanoLineClassifier(911)`; score pair-recovery rate against the block-0
true pair from `inst["pair"][0]`. Three seeds: 20260601, 20260602, 20260603.

### §3.1 Per-seed table

| seed     | basis              | rows × cols | n_short | hits | rate   | min_norm |
|----------|--------------------|-------------|---------|------|--------|----------|
| 20260601 | (a) primal         | 225 × 225   | 225     | 17   | 0.076  | 911.00   |
| 20260601 | (b)-I restriction  | 211 × 225   | 211     | 10   | 0.047  | 1288.35  |
| 20260601 | (b)-II augmentation| 323 × 225   | 98      | 0    | 0.000  | 1.00     |
| 20260602 | (a) primal         | 225 × 225   | 225     | 4    | 0.018  | 911.00   |
| 20260602 | (b)-I restriction  | 211 × 225   | 211     | 3    | 0.014  | 1288.35  |
| 20260602 | (b)-II augmentation| 323 × 225   | 98      | 0    | 0.000  | 1.00     |
| 20260603 | (a) primal         | 225 × 225   | 225     | 3    | 0.013  | 911.00   |
| 20260603 | (b)-I restriction  | 211 × 225   | 211     | 21   | 0.100  | 1288.35  |
| 20260603 | (b)-II augmentation| 323 × 225   | 98      | 0    | 0.000  | 1.00     |

### §3.2 Pooled

| basis              | total short | total hits | pooled rate |
|--------------------|-------------|------------|-------------|
| (a) primal         | 675         | 24         | **0.0356**  (below baseline) |
| (b)-I restriction  | 633         | 34         | **0.0537**  (above baseline — RATIFIED) |
| (b)-II augmentation| 294         | 0          | **0.0000**  (degenerate)       |

### §3.3 Decision

Reading (I) F_L-restriction is the ratified basis (b). It is the only reading
that exceeds the 1/21 baseline at this β/dim and across all three seeds it
matches or beats basis (a). It is therefore the worst-case-for-defender among
the candidates, satisfying §3.6(b)'s "given the Fano-line structure as a hint."

## §4. Why (II) failed — inversion of Brief 10.6's prediction

Brief 10.6 §2.3 hypothesised (II) would be the more-literal "hint" reading
and therefore the worst-case-for-defender. The toy result inverts this
prediction. Mechanism:

The unscaled F_L basis vectors (v with ±1 entries from `rref_kernel`) have
norm ≈ √2 ≈ 1.41 per row. After LLL, BKZ finds these vectors as the
shortest rows of the augmented lattice (min_norm = 1.00 — 14·7 = 98 rows of
norm 1.0 survive the reduction at β=30). The §3.3.1 cutoff
N=2.0×min_norm = 2.00 therefore captures the unscaled F_L hint vectors, not
the trapdoor target. The F_L hints span the noise subspace BUT have NO
correlation with which specific kernel K_{a,b} ⊂ F_L is the trapdoor — every
pair's K_{a,b} sits inside the same F_L, and an arbitrary F_L vector
projects roughly uniformly across the 21 K_{a,b}'s. So `classify(...)["pair"]`
returns the argmax-projection pair from an essentially random F_L direction,
which has chance ≈ 1/21 of matching the true pair — except that the
classifier's argmax is dominated by a few F_L "axes" and 0/294 of the
shortest 98 vectors land on the true pair across all three seeds.

The hint is **too short**: it overwhelms the trapdoor signal under the
fixed cutoff metric. (II) would only become competitive if the cutoff
convention were changed to an absolute norm scaled to the target estimate
(e.g., N = c×sqrt(2·n_eff·σ²)), but that would require re-opening §3.3.1
post-freeze. Within the frozen cutoff convention, (II) is degenerate.

The ratification answer is therefore (I), as an empirical finding —
opposite to the brief's predicted outcome.

## §5. §2.58.B.1 consistency (per Brief 10.6 §2.4)

Reading (I) restricts to the 14-dim F_L union per block. The 42-kernel
chirality structure of §2.58.B.1 lives *inside* this union: each Fano line's
F_L contains the two K_{a,b} kernels per Convention-C pair, exchanged by
the CD doubling involution e_i ↔ e_{i+8}. The F_L restriction does NOT
distinguish these two kernels (it preserves the full F_L, not a single
K_{a,b}), so basis (b) remains a 21-class (pair_21) object scored by the
Convention-C classifier.

**Forward-pointer recommended for pre-reg §2.1**: "Pair-recovery is a lower
bound on kernel-recovery (§2.58.B.1: noise lives in one of 42 ker(L_z), 2
per pair; the pair classifier discards the chirality bit). A pair-recovery
null safely upper-bounds kernel leakage; a pair-recovery positive would
warrant a 42-class follow-on classifier." This is a clarifying addition
consistent with V4.11, not a design change.

## §6. Caveats and out-of-scope

- The toy comparison is at β=30 dim 225. The spec schedule β up to 60 dim
  1025 may shift the relative ranking of (a) vs (b)-I; the ratification
  picks the basis structure, not a β-specific prediction. The schedule
  itself produces the verdict.
- (II)'s degeneracy is a property of the §3.3.1 cutoff convention, not an
  absolute statement about reading (II). Documented as a known limitation.
- (III) was rejected on prose grounds without toy verification. If a future
  brief argues for "out of" rather than "onto" reading, the toy harness here
  is sufficient to test (III) by replacing the F_L basis with its orthogonal
  complement.
- The 95.857% σ-stability of the §3.3 classifier (Brief 10.5 §2.4) is a
  classifier property; it does NOT carry over to lattice-attack BDD radius
  (§3.3 of `op_2_58_2d_sigma_resolution.md`).

## §7. Code location

- Ratified builder: `op_2_58_2d_lattice_attack.build_fano_projected_lattice`.
- Rejected (II) retained as `_build_fano_augmentation_lattice` for audit.
- F_L union basis (D1 re-derived): `_fano_union_basis`.
- Toy comparison harness: ad-hoc; see this document §3 for the published
  numbers. Reproduce with the script committed at
  `tools/op_2_58_2d_basis_b_compare.py` (Brief 10.6 deliverable).
