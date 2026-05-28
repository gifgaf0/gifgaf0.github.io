# OP-2.58.2d Item L2 — §2.58.B construction implementation record

**Date:** May 27, 2026
**Brief:** CLAUDE_CODE_BRIEF_10_5_OP_2_58_2D_CONSTRUCTION.md
**Ledger anchor:** §2.69.2 (V4.10) — the L2 finding (Brief-10 halt: §2.58.B not
present as executable code).
**Status:** Pre-freeze / toy scale. Spec-parameter gate enforced. No §2.58.B
spec-parameter execution.

---

## 1. Implementation chain

`tools/op_2_58_2d_construction.py` implements §2.58.B KeyGen from canonical
prose (V4.9 §2.58.B). Public API:

| Function | §2.58.B step | Notes |
|---|---|---|
| `gen_zd_noise_sample(p, k, sigma, rng, *, trapdoor_cardinality="pair_21")` | steps 1, 2, 4 | secret, ZD trapdoor + ℓ/pair labels, kernel-basis noise; §2.3-bis kwarg per A1 (§2.58.B.1) |
| `gen_public_matrix(p, k, rng, structure)` | step 3 | `"uniform"` only; non-uniform readings halt (see §2 below) |
| `gen_spec_instance(..., allow_spec_params=False)` | composes + step 5 | computes b = A·s + e; spec-gate enforced |

**Dependencies (consumed unchanged):** `sedenion_Fp.py` (`mul_vec`, `add_vec`,
`basis_vec`, `DIM`); `op_2252_v2_kernel_involution.py` (`enumerate_two_term_ZDs`,
`lmm`, `rref_kernel`); the spec gate `_check_not_spec` from
`op_2_58_2d_lattice_attack.py`. No existing module was modified.

**Trapdoor sampling convention.** z_i is sampled over the 21 canonical
Convention-C cross-edge pairs (a<b in 1..7, z = e_a + e_{b+8}). These are the
subset of the 84 two-term ZDs over which Convention C's (a,b) label and the §3.3
classifier's K_{a,b} subspaces are defined; each is a member of the 84-ZD set
(verified by `test_z_is_zd`). This is forced by the (a,b)-pair label convention
(`test_pair_label_consistency` requires a<b), not an independent structural
choice, so it is not a §2.3-style halt.

## 2. §2.3 specification-gap status (public-matrix structure)

**Implemented:** `"uniform"` only (reading (a) — A unconstrained in 𝕊_p^{k×k};
PSL(2,7)/Singer treated as latent structure of 𝕊_p, not a constraint on A).

**Halted (NotImplementedError, runtime message cites §2.3 and §2.69.2):**
- `"psl27_equivariant"` (reading (b))
- `"singer_cycle"` (reading (c))

These remain **permanently unimplemented within this brief's scope** (not
placeholders). Implementing (b)/(c) requires choosing the PSL(2,7)/Singer action
on 𝕊_p^k, building generators, and sampling from the constrained subspace —
progressively more work that may surface further §2.58.B ambiguities. Per Brief
10.5 §2.3, the choice is a session-level structural decision (it materially
changes the attack surface the §2.66.2 attacks probe); if the session pins (b)
or (c), a follow-on **Brief 10.6** implements it. Surfaced for session
resolution.

**§2.3 / §2.3-bis are independent and both resolved at the implementation-default
level** (uniform-A; pair_21 trapdoor cardinality), with the structural questions
filed as **OP-2.58.2.M** (matrix structure, deferred) and **OP-2.58.B.card**
(trapdoor cardinality, open).

## 2.3-bis. Trapdoor cardinality — corrected by §2.58.B.1

The §2.58.B prose "z_i ← ZD uniformly" was initially read as a 21/42/84
ambiguity (pairs / signed-pairs / full-ZD-set). The **A1 computation
(§2.58.B.1)** corrected this: the 84 two-term ZDs partition into **42 distinct
noise subspaces** (2 per unordered pair, exchanged by the CD doubling involution
e_i ↔ e_{i+8}); empirically verified at p = 911 (the verification is locked in
`test_42_kernel_partition`) and field-independent at q = 4,294,977,961 per A1.
The three *geometrically meaningful* trapdoor objects are:

| Reading | Object | Cardinality | Status |
|---|---|---|---|
| `fano_line_7` | Fano line ℓ(z_i) | 7 | halts (needs §2.66.2 line classifier) |
| `pair_21` | unordered pair {a,b} | 21 | **implemented** (the §3.3 Convention-C target) |
| `kernel_42` | noise subspace ker(L_z) | 42 | halts (needs 42-class chirality classifier) |

84 is a 2-to-1 redundant labelling of the 42 kernels, not a fourth object. The
construction's `trapdoor_cardinality` parameter (default `"pair_21"`) controls
only which object is recorded/scored; the noise geometry is identical regardless.
`kernel_42` and `fano_line_7` raise `NotImplementedError` whose runtime message
cites `OP-2.58.B.card` and `§2.58.B.1`.

**Pair-recovery is a lower bound on kernel-recovery** (kernel ⇒ pair, not
conversely), so the Convention-C classifier's results upper-bound kernel leakage
safely: a pair-recovery null implies kernel-recovery null. Which object is the
*operative* trapdoor is the open structural problem **OP-2.58.B.card**.

Implementation note: the `pair_21` default samples uniformly over the 21
canonical Convention-C cross-edge reps (a<b, z=e_a+e_{b+8}). Each such ZD is one
of two sharing its kernel, so this samples 21 specific kernels (one chirality
per pair) out of 42 — a chirality-discarding projection. Brief-10.5 behavior is
preserved exactly.

## 3. §2.4 σ-stability finding

The cross-check (`op_2_58_2d_construction_classifier_cross_check.py`, 100 samples,
k=7, q=911) measured pair-recovery at σ ∈ {1, 2, 4}:

| σ | pair-recovery | in ±3% band of 96.2%? |
|---|---|---|
| 1 | 95.857% (671/700) | yes |
| 2 | 95.857% (671/700) | yes |
| 4 | 95.857% (671/700) | yes |

**Spread across σ: 0.000%.** σ is **non-load-bearing at toy scale.** This is
exact, not approximate: the §3.3 projection metric ‖P_S v‖²/‖v‖² is invariant
under scaling v by σ, so σ cannot change the argmax pair. The §2.4 prediction
("σ affects magnitude, not direction; projection classifiers are
magnitude-insensitive") is confirmed with evidence. No σ halt-and-surface.

## 4. Item 3 cross-check result

**PASS.** Recovery is within ±3% of the Brief-08 with-lift baseline (96.2%) at
all three σ values. The small gap below 96.2% (95.857%) is attributable to the
canonical-allowed all-zero α coordinate (α_j ← {−1,0,+1} with no nonzero
constraint; ≈1.2% of coordinates yield e_i = 0, which the classifier resolves to
its tie-break pair). This is a faithful consequence of the §2.58.B step-4
distribution, not a construction/classifier discrepancy. Working hypothesis: the
construction's noise sampler matches what the classifier was built to detect
(neither outcome (a) sampler-mismatch, (b) bug, nor (c) σ-load-bearing applies).

## 5. Ledger cross-reference

This implementation closes the L2 finding recorded at **§2.69.2**. Any reference
to §2.58.B as an executable artifact cites §2.69.2; the §2.66.2 baseline numbers
(96.2% etc.) remain cited via **§2.69.1** (the L1 attribution gap).

## 6. Test count delta

Brief 10.5 adds `tools/test_op_2_58_2d_construction.py`: 10 named tests, with the
matrix-structure test parametrized over the two halted structures → 12
collected. The revised §2.3-bis patch (this version) adds the trapdoor-cardinality
halt test (parametrized × 2) and the A1 42-kernel partition lock → +3, so the
construction file collects **15** tests. Suite progression: post-Brief-09 303 →
post-Brief-10 310 (+7) → post-Brief-10.5 322 (+12) → post §2.3-bis revised
**325 passing** (+3). The OP-2.58.2d-specific suite is 56 tests (14 + 9 + 11 +
7 + 15).

## 7. Honest framing note (Brief 10.5 §3.4 point 7)

`gen_spec_instance` may be the first executable realization of §2.58.B in the
working repo. Whether any prior Cluster M work — notably the now-unattributable
§2.66.2 scripts cited in §2.69.1 — implemented §2.58.B in the form §2.69.2 names
is **unverifiable**, because the L1 attribution gap (§2.69.1) prevents that
question from being settled. Brief 10.5 implements §2.58.B-from-prose and makes
**no claim of priority**: whether or not it is the first such implementation is a
question §2.69.1 closes off, not one this brief resolves.

## 8. Path to Brief 10 re-attempt

The §2.58.B construction now exists and is toy-verified. Brief 10 (spec-parameter
primary run) remains blocked on **two** further session-side actions, unchanged
by this brief:
1. Commit the frozen Rev 5 `OP_2_58_2d_staging_PREREGISTRATION.md` with a signed
   §6 (the orchestrator's freeze check still halts without it).
2. Resolve the §2.3 matrix-structure gap (and, if (b)/(c), deliver Brief 10.6) —
   the primary run's basis and attack surface depend on it.
Basis (b) of the lattice (`build_fano_projected_lattice`) also remains a stub;
its implementation depends on the §2.58.B Fano-line subspace data now available
via this construction, but wiring it into the lattice module is out of Brief
10.5's scope.
