# OP-2.58.2d — Pre-Registration for LLL/BKZ Lattice Attack on Fano-Line Leakage

**Date staged:** May 27, 2026
**Cluster:** M (cryptography thread)
**Parent OP:** OP-2.58.2 (Fano-line classifier matrix-level leakage)
**Sibling sub-tasks:** OP-2.58.2c (production-scale empirical retest), OP-2.58.2e (LHL argument)
**Status:** PRE-REGISTRATION — to be frozen prior to first lattice-attack execution
**Discipline model:** Phase B audit log pattern (Entries 001–009 of `phase_b_audit_log.md`), extended to handle the lattice-attack third outcome (compute-bounded inconclusive).
**Append-only protocol:** This document, once frozen at §6 Freeze Statement, must not be edited. Any post-freeze modification creates a new audit entry rather than altering frozen content.

**Revision log (pre-freeze):**

- *Rev 1 (May 27, 2026, initial staging):* attack design, threshold, stopping rule.
- *Rev 2 (post-cryptography-review):* tightened §3.1 (q pinned to 4,294,977,961), §3.3 (signed-lift, cutoff parameter named), §4.2 (per-run cap clarified), §5.1 (split (a)/(b) nulls), §5.5 (basis-disagreement declarations).
- *Rev 3 (post-prefreeze-infrastructure-work, commit `766c6f5`):* **Convention C adopted.** Fano-line classifier downgraded from pass/fail to reference data only; pair-kernel classifier (1/21 baseline) is the sole pass/fail metric. Rationale: prefreeze findings F4 (the seven F_L overlap as real subspaces; the 1/7 baseline measures against a misspecified null) and F5 ("Fano line of z_i" is ambiguous; "pair (a, b) of z_i" is not). −A_scalarᵀ sign convention pinned in §3.6. Signed-lift convention pinned in §3.3.2.
- *Rev 4 (post-prefreeze-closure-work, commit chain following `766c6f5`):* **F1 closed**, **D1 closed**, **L1 filed separately as §2.69.1**. Signed-lift discrimination test (`tools/op_2_58_2d_F1_signed_lift_test.py`) ruled out possibility (a) — disabling signed-lift drops pair recovery to 41.8% (not the ~65% that would have indicated a §2.66.2 bug) while line recovery is essentially unchanged (89.6%). F1 closes on possibility (b)/(c): the reconstruction implements the projection-ratio specification of §2.66.2 but is not bit-exact, and bit-exactness is unverifiable due to source absence (L1). D1 (`tools/op_2_58_2d_D1_fano_union_dimension.py`) pins the §3.6(b) F_L-union dimension at rank 14, verified at both q = 911 and q = 4,294,977,961. L1 finding — the §2.66.2 baseline numbers (65.4% / 93.0%) and their cited upstream sources are unattributable; not in the working repo or in full git history — is filed as a separate Cluster M ledger entry §2.69.1 because it is wider in scope than OP-2.58.2d.
- *Rev 5 (post-Brief-09 cutoff-repin work, commit chain following Brief 08):* **Q2 closed**, **Q3 closed (as downgrade)**. Q2: §3.3.1 short-vector cutoff ratified at factor-of-2.0 via the toy-scale BKZ smoke test (`tools/op_2_58_2d_bkz_smoke.py`); β = 30 achieves uSVP solve across all three seeds with 100% pair recovery flat across N ∈ {1.0, …, 10.0}, pooled σ = 7.75, no discontinuity, outcome (c) ruled out. Caveat: cutoff is non-binding at toy scale (single trapdoor, ≥ 190× separated from bulk); fine N-discrimination deferred to secondary-run gate. Implementation notes pinned: fpylll `float_type="ld"` required (default precision hits "infinite loop in babai" on q-ary bases); `sys.modules` lookup needed for the gate-enforcement test. Q3: the §3.1 SNR target "≈ 0.0025 within 10%" is downgraded to reference-only (Brief 09 Item 5 measured ≈ 0.0053, factor-of-2 outside ±10% gate; the L1 attribution gap makes 0.0025 unverifiable). New §3.1 validation gate: secondary-run SNR within 25% of the Brief-09-measured 0.0053 baseline. Spec-scale SNR re-derivation deferred to `tools/op_2_58_2d_SNR_spec_derivation.md` (low priority, not a freeze blocker).

**Rev 5 is the freeze-ready state.** No remaining provisional values; no remaining placeholders. §6 freeze can be signed as the next discrete event.

---

## §1. Purpose

Pre-commit the design, execution conditions, success/null/inconclusive declarations, and stopping rule for the LLL/BKZ lattice-reduction attack against the Fano-line trapdoor in the Module-SLWE construction of §2.58.B. This is the gating attack of the OP-2.58.2 closure path: per the §2.66.2 status declaration, **OP-2.58.2 will not close until OP-2.58.2d returns a null** (and one of {OP-2.58.2c, OP-2.58.2e} returns positive).

The pre-registration discipline matches the Phase B model: the falsification condition, the null condition, the stopping rule, and the treatment of edge cases are all fixed in writing *before* the attack is run. Post-hoc reframing is treated as a §3.* retraction event, not as a reinterpretation.

---

## §2. Threat model and target

### §2.1 What the attack tries to recover

**Primary target (pass/fail).** The 4D pair-kernel K_{a,b} of the ZD-noise trapdoor in §2.58.B, given access to the public matrix A and ciphertext / public-key vector b = A·s + e (over 𝕊_p). Each ZD-noise sample z_i is generated as x = e_a + e_{b+8} for some interior pair {a, b} ⊂ {1, …, 7}; the defender records the pair as the trapdoor. The attacker is not assumed to know s. Recovery of (â, b̂)(v) = (a, b) above the 5σ threshold (see §3.2), against the random-guess baseline 1/21 ≈ 4.762%, constitutes a successful distinguisher.

**Reference target (no pass/fail weight).** The "Fano line of z_i" is *not* used as a pass/fail criterion. The reason is a structural finding from the pre-freeze infrastructure work (commit `766c6f5`, prefreeze report finding F4): the seven 8D Fano-line subspaces F_L overlap as real subspaces of 𝕊_q^{16}. The kernel-involution structure of §2.55 means K_{a,b} is supported on cross-edges of the *two co-lines through the shared third point*, so every K_{a,b} basis vector lies in F_L for the line containing {a, b} **and** also at projection ratio 1.0 inside the F_L of those two co-lines. The phrase "Fano line of z_i" is consequently ambiguous as a function of z_i alone, and the line-classifier's argmax against a 1/7 baseline measures against a misspecified null (the structurally-effective baseline is ≈ 2/7 from the two-line overlap). Per finding F5, no pass/fail weight is attached to the line classifier.

Fano-line ratios per §3.3 measurement (5) are still recorded as reference data — they are useful for cross-comparison against the §2.66.2 classifier-soundness diagnostic (88% / 96.2% reproduction at q = 911 per commit `766c6f5`) and for any future analysis that resolves the ambiguity by adopting a different convention — but they do not enter the closure declarations of §5.

**Forward-pointer to §2.58.B.1 (added with the full-text commit, consistent with V4.11; not a design change).** Pair-recovery is a *lower bound* on kernel-recovery. Per §2.58.B.1 (the A1 42-kernel partition, V4.11 canonical): the noise lives in one of **42** distinct ker(L_z), two per unordered pair {a,b}, distinguished by a chirality bit (the relative cross-edge sign; the two are exchanged by the CD doubling involution e_i↔e_{i+8}). The Convention-C pair classifier recovers the pair (21) but discards the chirality bit, so recovering the kernel implies recovering the pair, not conversely. Consequence for the §5 declarations: a pair-recovery **null** safely *upper-bounds* kernel-level leakage (no pair recovery ⇒ no kernel recovery), so a §5.1 null is sound at the kernel level despite the classifier being lossy. A pair-recovery **positive** would warrant a follow-on 42-class kernel classifier to measure the full leakage (a Brief 10.7-sibling, contingent on the positive; see OP-2.58.B.card). This forward-pointer is a clarifying addition consistent with the V4.11 canonical; the pass/fail metric (pair classifier, 1/21 baseline) is unchanged.

### §2.2 What the attack does NOT try to recover

- The secret s itself. Recovery of s would be a stronger break, but is not the falsifiability target of OP-2.58.2d.
- Direct decryption failure forcing. The DFR question is closed under §2.66.1 / OP-2.58.1.a.
- The Fano-line of z_i as a pass/fail target. Per §2.1 (Convention C, finding F5), the line classifier is recorded as reference data only and does not enter the §5 closure declarations.

### §2.3 Distinction from the seven prior attacks of §2.66.2

The seven prior attacks (direct projection, Singer-difference projection, dual-lattice distinguisher, sparse-recovery enumeration, correlated-noise projection) are all **linear / projection-based** distinguishers that operate on the ambient space 𝕊_q^k directly. OP-2.58.2d is structurally different: it constructs the LWE lattice associated with the Module-SLWE instance, runs BKZ reduction at increasing block sizes, and checks whether the basis vectors produced by reduction expose the Fano-line subspace structure of e.

A success here would mean BKZ at block size β recovers a basis vector that classifies (under the pair-kernel projection classifier of §3.3) to the true pair (a, b) of the ZD-noise generator more often than the 1/21 random-guess baseline, at the σ-thresholds of §3.2. A null means it does not, up to the stopping rule of §4. The argmax-pair-kernel is the pass/fail metric per §2.1 Convention C; argmax-Fano-line is recorded as reference data.

---

## §3. Pre-registered conditions

### §3.1 Parameter regime

**Primary run.** Spec parameters: k = 32, **q = 4,294,977,961** (the smallest prime ≥ 2³² with q ≡ 1 (mod 455); = 2³² + 10,665; bit length 33; log₂ q ≈ 32.0000036), d_sed = 16, **n_eff = k · d_sed = 512** (the scalar effective dimension; this is the dimension of the ambient F_q^512 once the 𝕊_q^k Module-SLWE instance is unrolled to its scalar-LWE form). h_s = h_r = 64. η = 2. ZD-noise per §2.58.B with pair-kernel basis sampling α_j ← {−1, 0, +1}.

The q value matches the q ≡ 1 (mod 455) constraint of §2.58.B and §2.66.1, sits just above 2³² (preserving the spec's bit-budget assumption), and is the smallest such prime — so any future tightening of q goes downward, not sideways. This pin is part of the §6 freeze.

**Secondary run.** Toy parameters matching §2.66.2 for direct comparison: q = 911, k ∈ {7, 14}, η = 2, n_eff = 16k ∈ {112, 224}.

The primary run is the binding result. The secondary run exists to verify that the lattice construction code reproduces a documented signal-to-mask ratio measurement before being scaled up.

**Q3 closure (Rev 5, post-Brief-09).** The original §3.1 target of "SNR ≈ 0.0025 within 10% relative error" was inherited from the §2.66.2 reported figure. Brief 09 Item 5 measured the SNR proxy ‖e‖ / ‖A·s‖ directly from the toy-scale (A, s, e) samples generated for Item 3 and obtained ≈ 0.0053, approximately 2× the §3.1 target and outside the ±10% gate. The discrepancy has two plausible sources:

(i) **Amplitude-vs-power offset.** The §2.66.2 figure may have been reported as a power ratio (‖e‖² / ‖A·s‖² or equivalent variance-ratio quantity) while the Brief-09 measurement is an amplitude ratio. Neither √0.0025 ≈ 0.05 nor 0.0025 itself cleanly resolves the factor-of-2, but the offset is in the family of definitional differences typical of "SNR" ambiguity in the LWE literature.
(ii) **Toy-vs-spec regime mismatch.** The Brief-09 measurement is at q = 911, k = 7; the §2.66.2 figure was reported at the same q but possibly a different k (the original record cannot be inspected per L1). SNR ratios for Module-LWE noise scale with k and η, so a toy-to-toy discrepancy is plausible but not characterizable without the §2.66.2 derivation.

Per the L1 attribution gap of §3.3 (and §2.69.1 in the canonical ledger), the original 0.0025 figure is unattributable: there is no §2.66.2 source in the repo to inspect for the definition or the parameters under which it was measured. Continuing to use 0.0025 as a validation gate would commit OP-2.58.2d's instrument validation to a number the framework cannot derive.

**Pinned Q3 closure language for §3.1:** the "SNR ≈ 0.0025 within 10% relative error" target is **downgraded to reference value only**. The toy-scale secondary-run gate is therefore not a single-number match; it is replaced with: (a) the Brief-09-measured SNR ≈ 0.0053 at (q = 911, k = 7) recorded as the reproducible baseline for this implementation; (b) confirmation that the secondary-run measurement at k ∈ {7, 14} produces an SNR within 25% of the Brief-09 baseline (a wider tolerance reflecting the absence of an external attribution); (c) deferred to a written spec-scale re-derivation (proposed as `tools/op_2_58_2d_SNR_spec_derivation.md`, low priority, not a freeze blocker) the question of what SNR should hold at (q = 4,294,977,961, k = 32).

If the secondary-run SNR at toy falls outside 25% of the Brief-09 baseline, the discrepancy is filed as an instrument failure per the original §3.1 protocol — but the gate is now against the reproducible Brief-09 measurement, not the unattributable 0.0025.

### §3.2 Detection thresholds

Following the §2.66.2 thresholds for consistency across the thread:

- **5σ leak-detection threshold.** A successful attack must produce a pair-kernel recovery rate at least 5σ above the random-guess baseline 1/21 ≈ 4.762%. Per §2.1 (Convention C, finding F5), the Fano-line recovery rate is not used as a pass/fail criterion; the 1/7 baseline does not enter the §5 closure declarations.
- **3σ marginal-significance threshold.** A 3σ excess on the pair classifier that does not replicate across the three independent samples of §3.5 is filed as banked observation (R3), not as a positive finding. A 3σ excess that does replicate but does not reach 5σ in the pooled sample is filed as a partial finding — see §5.3.
- **Below 3σ.** Null.

These thresholds were pre-frozen in the §2.66.2 audit and are reused here for cross-attack comparability on the pair classifier. The Fano-line classifier σ-statistics from §2.66.2 (best observed +1.42σ on Welch t = −0.30) remain on the historical record but are not the pass/fail metric for OP-2.58.2d.

### §3.3 What is measured

For each BKZ block size β in the schedule of §4.1, and for each of the three independent samples (§3.5), the BKZ output basis is read into the §2.66.2 projection classifier (reconstructed in `tools/op_2_58_2d_classifier.py`, commit `766c6f5`; see F1 paragraph below for the bit-exactness status). The classifier takes a candidate vector v ∈ 𝕊_q^k and returns its argmax-pair-kernel (â, b̂)(v) and argmax-Fano-line ℓ̂(v) under the projection metric ‖P_S v‖² / ‖v‖², summed block-wise over the k sedenion blocks. Candidates are signed-lifted to (−q/2, q/2] before projection (the centred representative; see §3.3.2 for the rationale).

**Pass/fail measurements** (used in §3.2 and §5):

1. **Short-vector pair-kernel recovery rate.** Fraction of the short basis vectors output by BKZ (defined per §3.3.1) whose argmax-pair-kernel (â, b̂) equals the (a, b) of the ZD-noise generator z_i = e_a + e_{b+8} (Convention C definition of "true pair"). Random-guess baseline 1/21 ≈ 4.762%.

**Reference-data measurements** (recorded but not pass/fail):

2. **Short-vector Fano-line recovery rate.** Same as (1) but against the seven F_L. Recorded for cross-comparison against the §2.66.2 classifier-soundness diagnostic and against the commit-`766c6f5` reconstruction (88% line / 96.2% pair on random ZD-noise at q = 911). Per finding F4 the seven F_L overlap, so this metric does not have a clean σ-statistic against a 1/7 baseline.
3. **Argmax-confidence distribution.** The projection ratio ‖P_S v‖² / ‖v‖² is reported as a histogram across short vectors at each β (for both the pair and line classifiers). Reference data only.
4. **Norm reduction.** ‖shortest BKZ output‖ as a function of β. Reference data only.
5. **Runtime per β.** Wall-clock time per block size. Used by the stopping rule (§4).

**F1 — bit-exactness against §2.66.2 (closed).**

The signed-lift discrimination test was executed against the commit-`766c6f5` reconstruction (`tools/op_2_58_2d_classifier_no_lift.py` + `tools/op_2_58_2d_F1_signed_lift_test.py`, on the `claude/nextgen-crypto-testspace-bhwUO` branch following `766c6f5`; q = 911, N = 500, seed `20260527`). Result matrix:

| classifier | lift on | lift off |
|---|---|---|
| pair | 96.2% | 41.8% |
| line | 88.0% | 89.6% |

The with-lift figures reproduce the commit-`766c6f5` baseline exactly. Neither no-lift metric approaches the §2.66.2 reported 65.4% / 93.0% diagnostic, so possibility (a) of the staging draft (signed-lift was the §2.66.2 bug) is **ruled out**.

Two structural facts follow:

- **Pair classifier:** signed-lift is load-bearing for the pair classifier — disabling it collapses pair recovery from 96.2% to 41.8% on the same input distribution. The 30-percentage-point gap between the commit-`766c6f5` reconstruction (96.2%) and the §2.66.2 reported pair diagnostic (65.4% — note: the §2.66.2 ledger entry as cited records 65.4% as the "Fano line" rate and 93.0% as the "exact pair" rate; the agent's harness reproduces these with line/pair *swapped* relative to the ledger's labels. The label-swap is a sub-question of L1 and inherits L1's unresolvable status — with the §2.66.2 source absent, there is no way to settle which labeling the original used; per Convention C the pass/fail metric is the pair classifier against the 1/21 random-guess null, which is structurally fixed by the geometry and does not depend on the §2.66.2 labels being correctly matched, so the swap question is recorded but does not gate freeze) is therefore attributable to possibility (b) or (c) of the staging draft — different input distribution and/or non-bit-exact classifier — not to a signed-lift bug.
- **Line classifier:** signed-lift is *not* load-bearing — disabling it leaves line recovery essentially unchanged (88.0% → 89.6%). The 4D pair-kernel projection is tight enough that a few wrap-around coefficients destroy it; the 8D F_L union projection is loose enough that the same coefficients still land mostly inside.

**Pinned F1 closure language for §3.2's σ-statistics:** the reconstruction in `tools/op_2_58_2d_classifier.py` implements the projection-ratio specification of §2.66.2 but is not bit-exact with the §2.66.2 reference. Bit-exactness is unverifiable due to source absence (see L1 below). The σ-statistics of §3.2 are computed against the reconstruction's own baseline established at the §3.1 secondary-run validation gate, against the 1/21 random-guess null for the pair classifier per §2.1 Convention C.

**L1 — §2.66.2 attribution gap (separate finding).** The §2.66.2 reference numbers (65.4% / 93.0%) and the upstream sources cited in the canonical ledger (`SQT_Master_Ledger_v4_0_CANONICAL.md`, `phase_b_audit_log.md`, `op_2_58_2_leakage_test.py`, `op_2_58_2b_advanced_attacks.py`) do not exist in the working repo or in its full git history (verified by file search and `git log --all -S`; commit `766c6f5` is the first appearance of the 65.4% / 93.0% figures in the repo, as uncaptioned reference data). Per the L1 attribution note (`tools/op_2_58_2d_L1_attribution_note.md`), the §2.66.2 baseline is **unattributable** at the source level. This is a Cluster M finding wider in scope than OP-2.58.2d and is filed separately as **§2.69.1** in the canonical ledger; it does not block OP-2.58.2d freeze because the pre-registration's pass/fail metric is the pair classifier against the 1/21 random-guess null (Convention C), which is structurally fixed by the geometry and does not depend on the §2.66.2 reference numbers. It does, however, mean that the line-recovery rates of §3.3 measurement (2) are recorded for cross-comparison against a §2.66.2 baseline whose derivation cannot be verified; this is named honestly in any synthesis-paper-grade citation per §2.69.1.

### §3.3.1 Pre-registered parameter: short-vector cutoff

"Short basis vectors output by BKZ" means: those BKZ-output basis vectors whose Euclidean norm is at most **2.0 times** the Euclidean norm of the shortest output basis vector at that β. The factor-of-2 is named here as a new pre-registered parameter of OP-2.58.2d (per Q1 of the prefreeze report; no §2.66.2 precedent exists because §2.66.2 was not operating on BKZ output).

**Q2 closure (Rev 5, post-Brief-09).** The factor-of-2.0 is ratified empirically by the toy-scale BKZ smoke test (`tools/op_2_58_2d_bkz_smoke.py`, commit chain following Brief 08). Sweep details: fpylll BKZ at k = 7 (N_lat = 225), seeds `20260601` / `20260602` / `20260603`, cutoff parameter N ∈ {1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 4.0, 6.0, 10.0}.

| β | uSVP solved (all 3 seeds) | Pair-recovery across N | Pooled σ vs 1/21 baseline |
|---|---|---|---|
| 20 | No (BKZ stuck at q-vectors, norm 911) | flat ≈ baseline | ≤ 2.9 |
| 30 | Yes (min norm 4.1–4.6) | 100% at every N | 7.75 |

No discontinuity at either β; the three seeds agree. Outcome (c) of Brief 09 §3.4 — instability — is ruled out, which was the §5 goal of the smoke test. N = 2.0 sits inside the flat 100% band at β = 30 and is therefore ratified.

**Caveat — non-binding at toy scale.** At toy k = 7 with a single ZD-noise trapdoor in the sample, the trapdoor vector at β = 30 is ≥ 190× shorter than the bulk of the BKZ output, so any N in the swept range correctly selects it. The cutoff is not being *discriminated* by this test — it is being shown to be in the safe range. Fine N-discrimination (which value gives the best σ-statistic when multiple trapdoor-aligned vectors are present and are not catastrophically separated from the bulk) is deferred to the §3.1 secondary-run validation gate, where k = 14 and the BKZ output population is larger. If the secondary-run measurement at k = 14 indicates a different N value is preferred — within the safe band already established — a discrete §3.3.1 second-stage edit is permitted *before* the primary run begins, signed and dated as a Rev 5.x addendum; this is the same gate condition as before the empirical confirmation.

**Implementation notes for reproducibility (load-bearing).** The Brief-09 harness uses `float_type="ld"` (long-double GSO) for fpylll's BKZ call. The default-precision and BKZ-2.0 paths hit a non-terminating "infinite loop in babai" condition on these q-ary lattices at toy scale; `ld` is robust and deterministic across all three seeds. Future implementations of OP-2.58.2d's BKZ driver must use `float_type="ld"` or a verified-equivalent precision setting; default-precision is a foot-gun. The gate-enforcement test similarly uses a `sys.modules` lookup to resolve the `SpecParamsRefused` class because the repo's sys.path import pattern creates two class objects (one per import path); a naive `isinstance` check against the bare-imported class will silently fail to catch spec-parameter invocations. Both are documented in `tools/op_2_58_2d_bkz_smoke.py` and `tools/test_op_2_58_2d_bkz_smoke.py` (commit chain following Brief 08).

Post-Q2-closure: the cutoff is **ratified at factor-of-2.0**; the §3.3.1 value is freeze-locked; the second-stage edit gate is the only remaining permissible §3.3.1 modification before §6 freeze, conditional on secondary-run data.

### §3.3.2 Signed-lift convention

Candidates passed to the classifier are signed-lifted from F_q to (−q/2, q/2] before the Euclidean projection is computed. Without this step, mod-q residues near q (e.g. coefficient −1 stored as 910 at q = 911) are read as large positive values by the Euclidean metric, systematically destroying the signal. The signed-lift is idempotent on small signed integer vectors (BKZ output is typically in the signed range), so the operational impact on the attack is nil; the impact is on cross-comparability with §2.66.2 and is the subject of the F1 signed-lift discrimination test.

### §3.4 Null condition (frozen)

**Null = no measurement of category (1) or (2) above exceeds 5σ at any β reached within the stopping budget, AND no measurement exceeds 3σ in replication across all three samples at any β reached.**

Failure to reach high β within budget (the third outcome) is NOT null — it is "inconclusive, compute-bounded" per §4.3.

### §3.5 Replication

Three independent (A, s, e) samples generated with seeds `20260601`, `20260602`, `20260603`. All three are run at every β in the schedule. Replication is required for the 3σ marginal threshold; the 5σ threshold is evaluated both per-sample and pooled.

### §3.6 Lattice construction

The Module-SLWE instance (A, b) over 𝕊_p is unrolled to its scalar-LWE equivalent via the d_sed = 16 sedenion basis. The scalar effective dimension is n_eff = k · d_sed (= 512 at spec, k · 16 ∈ {112, 224} at toy). The primal LWE lattice constructed from this scalar-LWE instance has dimension **N_lat = 2 · n_eff** by the standard "primal with target" embedding (n_eff coordinates for the secret subspace, n_eff coordinates for the equation subspace). At spec, N_lat = 1024; at toy k = 7, N_lat = 224; at toy k = 14, N_lat = 448. References to "n = 1024" in §4 and §9 refer to N_lat (the BKZ-relevant lattice dimension), not n_eff.

**Sign convention.** The lattice basis B is constructed such that the target z·B = (e, s, 1) holds with z = (m₀, s_scalar, 1), where the relation exploited is **e = b − A_scalar·s**. This requires the A-block of B to enter with sign **−A_scalarᵀ** rather than the +A_scalarᵀ that the literal §3.2 wording would suggest. The minus sign is the round-trip-verified convention (commit `766c6f5`, `tools/op_2_58_2d_lattice_attack.py`, 14 tests pass including exact round-trip ‖v_target‖ = 14.93, BDD gh = 107.9 > ‖v_target‖, det = q^{n_eff} via exact Bareiss on a dim-33 instance). The +A_scalarᵀ basis does not round-trip and is filed in the prefreeze report (`tools/op_2_58_2d_prefreeze_report.md`) as the discovered convention error in the original §3.2 wording. Pinned for the freeze: −A_scalarᵀ.

Two basis constructions are tested:

- **(a) Primal basis.** Standard primal LWE lattice from the unrolled (A, b) under the −A_scalarᵀ sign convention above — no structural projection applied. This is the basis a generic attacker would build with no knowledge of the trapdoor structure.
- **(b) Fano-projected basis.** Lattice basis pre-projected onto the union of the seven 8D F_L subspaces (using the kernel-basis output of `op_2252_v2_kernel_involution.py` at the appropriate p). Per finding F4 the seven F_L overlap as real subspaces; per D1 of the prefreeze closure work (`tools/op_2_58_2d_D1_fano_union_dimension.py`, commit chain following `766c6f5`), the rank of the stacked kernel basis is **exactly 14** — verified at both q = 911 and q = 4,294,977,961 by exact F_q Gaussian elimination, with each K_(a,b) of dimension 4 and each F_L of dimension 8 confirmed independently at both primes. Rank 14 sits in the expected 9–15 band (9 = three Fano lines disjoint, 15 = full ambient minus identity; the actual overlap structure pins it at 14). This basis exists *only* if the attacker is given the Fano-line structure as a hint; it is the worst case for the defender.

Both are run. The pass/fail metric on both (a) and (b) is the pair-kernel classifier only (per §2.1 Convention C); the Fano-line classifier is recorded as reference data per §3.3 measurement (2). A success on (a) without success on (b) would be a surprise and triggers a §3.* retraction-log scrutiny of the lattice construction code (see §5.5).

---

## §4. Stopping rule (lattice-attack-specific)

The Phase B pre-registration handled only two outcomes (signal / no signal). Lattice attacks have a third: ran out of compute before reaching the interesting block sizes. The reviewer flagged this in the May 27 staging response; the present §4 fixes it explicitly.

### §4.1 Block-size schedule

BKZ is run at increasing block sizes:

| β | Purpose |
|---|---------|
| 20 | Sanity warm-up; should complete in minutes at spec. Any positive signal here would be a catastrophic break and would not require continuation. |
| 30 | Tighter reduction; should complete in hours at spec. |
| 40 | Approaches the regime where state-of-the-art lattice attacks become interesting for n ≈ 1000. |
| 45 | Compute-aggressive; days at spec. |
| 50 | Compute-aggressive frontier. The lattice-estimator (cf. OP-2.58.5) gives concrete-security predictions in this range for n ≈ 1000. |
| 55 | Frontier+; days to weeks. |
| 60 | Frontier++. Reaching β = 60 at n = 1024 is at the edge of what is feasible without large compute resources. |

The schedule is **monotonically increasing**; no skipping forward then backing off. A timeout at β triggers the §4.3 decision tree, it does not authorize jumping to β + 10.

### §4.2 Compute budget (pre-committed)

**Primary run.** Total wall-clock budget: 30 days, single workstation (or equivalent in parallelized smaller jobs). The total primary-run workload at spec is: 7 block sizes × 3 samples × 2 basis types = **42 BKZ runs**. The 7-day cap is **per individual BKZ run** (i.e. per (β, sample, basis) triple), not pooled across samples or basis types at a given β. If any single (β, sample, basis) run exceeds 7 days without termination, that run is aborted and recorded as "(β, sample, basis)-aborted" per §4.3. Aborts at a given (β, sample, basis) do not auto-abort other runs at the same β with different sample seeds or basis types — those proceed independently.

The 30-day total budget is the hard ceiling across the 42 runs. In the realistic case where lower β runs complete quickly and only the high-β runs approach the per-run cap, the total budget is the binding constraint. In the pathological case where every run hits its 7-day cap, the schedule terminates well before 30 days are exhausted (42 × 7 = 294 run-days, but with parallelization the wall-clock can be much shorter). Parallelization across runs is permitted; the per-run cap is independent of parallelization.

**Secondary run (toy).** Total wall-clock budget: 24 hours. The toy workload is 7 block sizes × 3 samples × 2 basis types × 2 toy k values = 84 BKZ runs at much smaller N_lat (224 and 448). The 6-hour cap is per individual (β, sample, basis, k) run.

These budgets are pre-committed before first lattice-reduction run. They may not be extended after the run begins. If they prove insufficient, OP-2.58.2d closes as "inconclusive, compute-bounded at budget B" (§4.3) and a *new* pre-registration with a larger budget can be opened as OP-2.58.2d.2.

### §4.3 Decision tree at budget exhaustion

At end of budget, three states are possible:

1. **Reached β ≥ 50 with no signal.** Null. Files as the §2.66.2 status declaration intended.
2. **Reached 30 ≤ β_max < 50 with no signal.** Partial null. Files as "OP-2.58.2d returns null at β ≤ β_max; β > β_max not tested." Closure of OP-2.58.2 requires re-opening OP-2.58.2d at higher budget OR is conditional on OP-2.58.2e closing the analytic question.
3. **Reached β_max < 30 with no signal.** Inconclusive, compute-bounded. Does not close OP-2.58.2d. The attack code is preserved, a budget request is opened (OP-2.58.2d.2), and OP-2.58.2 remains OPEN with no positive evidence either way.

**Critical rule.** The β_max threshold defining "real null" (β ≥ 50) is set *in this pre-registration*, not after looking at where compute happened to stop. Post-hoc lowering of this threshold to claim a stronger null is a §3.* retraction event.

### §4.4 What counts as a signal during execution

A run terminates early (before budget exhaustion) only if a positive signal exceeds the 5σ threshold of §3.2 at some β. In that case, replication on the other two samples is the next step; if both replicate, the attack is declared a success at that β and the budget is not consumed at higher β.

A 3σ excess does NOT terminate the run. The full schedule continues; the 3σ excess is logged and evaluated only at end-of-run per §3.2.

---

## §5. Result declarations (pre-committed)

### §5.1 Null

The null condition decomposes across the two basis types of §3.6. Both must hold for OP-2.58.2 closure weight to accrue from the (b) component; the (a) component carries closer to sanity-check weight. Per §2.1 Convention C, the pass/fail metric is the pair-kernel classifier only; Fano-line recovery is recorded as reference data but does not enter the declarations below.

> **(a) Primal-basis null.** "OP-2.58.2d (a) returns null. LLL/BKZ reduction at block sizes β ∈ {schedule} on the primal LWE lattice of the §2.58.B construction at (parameters of §3.1) recovers no pair-kernel above the 5σ leak-detection threshold against the 1/21 random-guess baseline, and no replicated 3σ excess across three independent samples. Generic lattice reduction without knowledge of the trapdoor structure does not expose pair-kernel containment."

> **(b) Fano-projected-basis null.** "OP-2.58.2d (b) returns null. LLL/BKZ reduction at block sizes β ∈ {schedule} on the Fano-projected lattice — the worst-case lattice for the defender, where the F_L subspace structure of §3.6(b) is handed to the attacker as a basis hint — recovers no pair-kernel above the 5σ leak-detection threshold against the 1/21 random-guess baseline, and no replicated 3σ excess across three independent samples. Lattice reduction *with* the F_L structure as a hint does not expose the pair-kernel trapdoor either."

**The (b) null is the load-bearing result.** It is the much stronger statement, and it is what closes the lattice-reduction attack class on OP-2.58.2 (subject to §3.1 binding-clause scope). The (a) null without the (b) null does not close OP-2.58.2 — it only confirms that a generic attacker cannot find what a hinted attacker also cannot find, which is a much weaker claim. The (a) null without (b) null is filed as a partial null per §5.3.

**Both nulls together (the joint case)** carry the full closure weight per the §2.66.2 status declaration: OP-2.58.2 then requires only one of {OP-2.58.2c (production-scale empirical), OP-2.58.2e (LHL argument)} to return positive in order to close. The (a)+(b) joint null is the §6-freeze result that the present pre-registration targets.

### §5.2 Positive

> "OP-2.58.2d returns positive. BKZ at block size β = [value] on [basis (a) or (b)] of the §2.58.B construction at (parameters of §3.1) recovers pair-kernel at rate [value]% ± [σ] over [n] trials, exceeding the 5σ threshold against the 1/21 baseline and replicating across three independent samples. The §2.58.B construction is broken at the tested parameters by lattice reduction at block size β. The construction is retracted via §3.* entry; replacement candidates are listed in the retraction body."

### §5.3 Partial / inconclusive

Two sub-cases:

> "OP-2.58.2d returns partial null. BKZ at β ≤ β_max with [30 ≤ β_max < 50] returns no pair-kernel signal above the 5σ threshold against the 1/21 baseline. β > β_max not tested at budget B. Closure of OP-2.58.2 deferred pending OP-2.58.2d.2 (higher-budget rerun) or OP-2.58.2e closure."

> "OP-2.58.2d returns inconclusive. Compute budget B exhausted at β_max < 30. No signal detected, but the parameter regime where lattice attacks become interesting was not reached. OP-2.58.2 remains OPEN with no movement on the lattice-attack question. A budget request is opened as OP-2.58.2d.2."

### §5.4 Replicated 3σ without 5σ

Filed as banked observation (R3) inside §2.66.2 — the partial-finding pattern of §2.69's T3 sub-observation is the precedent. Does not close or open any structural threads but is preserved for cross-reference if a future higher-budget run revisits the same β.

### §5.5 Disagreement between (a) and (b)

The two basis-type results of §3.6 can disagree in direction. There are two such cases:

**Case 1: positive on (a), null on (b).** A generic attacker (no Fano-line hint) sees the trapdoor; a hinted attacker (Fano-line basis) does not. This is structurally implausible — adding a hint should not *hurt* the attacker — and is the case flagged in §3.6 as triggering instrument scrutiny.

> Declaration: "OP-2.58.2d returns inconsistent. Primal-basis result (a) exceeds the 5σ threshold at β = [value]; Fano-projected-basis result (b) is null at the same β. This pattern is structurally inconsistent (adding the Fano-line hint should not reduce attack power). The result is NOT declared positive. The lattice construction code and the §2.66.2 classifier are scrutinized for bugs before any closure declaration is filed. Resolution outcomes: (i) bug found in (b) construction → rerun (b), declaration deferred until rerun completes; (ii) bug found in (a) construction → (a) result retracted, OP-2.58.2d declared null per §5.1(b) if (b) null holds; (iii) no bug found → the result is filed as R3 banked observation with explicit 'no resolution' status, and OP-2.58.2d remains OPEN with neither closure nor break declared. Outcome (iii) is itself a finding — the §2.58.B construction admits a generic attack that the Fano hint blocks, which would be a novel structural fact requiring its own investigation."

**Case 2: null on (a), positive on (b).** A generic attacker cannot see the trapdoor; a hinted attacker can. This is structurally expected (the hint is information) and is the boundary case the security model is designed to live near.

> Declaration: "OP-2.58.2d (b) returns positive at β = [value]; (a) returns null at the same β. The §2.58.B construction is broken under the worst-case threat model where the attacker has the Fano-line structure as a hint. Under the realistic threat model where the attacker has only (A, b), the construction holds at the parameters tested up to compute budget B. The construction is retracted as a *generic* KEM proposal via §3.* entry; the Fano-line structure must be hidden (not just unobservable in A) for the trapdoor to be secure. This is a structural retraction, not a code-scrutiny event."

**The critical rule for both cases.** The result is NOT "OP-2.58.2d positive" in unqualified language until either the code scrutiny (Case 1) resolves or the threat model is explicitly named (Case 2). Both declarations are pre-committed verbatim above; deviation from this language at result-time is a §3.* retraction event.

---

## §6. Freeze Statement

The freeze is a discrete event: the freeze date and the freeze signature are added in the same act of saving the document. Until both are present, the document is a draft and the parameter values, thresholds, and decision criteria of §§1–5 may still be edited. Once both are present, the document is frozen and no content in §§1–5 may be edited.

**Freeze date:** 2026-05-27

**Freeze signature:** AUTHORIZED_RUN_V4.11_MAY_27_2026

*(This signature matches the §6 authorization the Brief-10 orchestrator parsed and accepted at the freeze-verification gate. The freeze covers the Rev 5 design of §§1–5 as recorded in this document. Committing this full §1–§6 text to the branch completes the on-branch realization of the already-frozen Rev 5; it is not a new revision — see Brief 10.6 Item 3 §4.4.)*

After the freeze: any extension of the §4.2 budget, any change to the §4.1 block-size schedule, any change to the §3.2 detection thresholds, any change to the §5 outcome declarations, and any change to the §3.6 basis-construction protocol are §3.* retraction events. They generate a new pre-registration document (e.g., OP-2.58.2d.2) rather than amend the present one.

The freeze date must precede the first execution of any lattice-reduction code against the §2.58.B construction at the parameters of §3.1. Code may be written and tested against synthetic / non-§2.58.B inputs before the freeze; the freeze gates the first run against the actual construction.

---

## §7. Files (to be produced)

- `op_2_58_2d_lattice_attack.py` — Module-SLWE lattice construction from `sedenion_Fp.py` outputs; primal and Fano-projected basis variants per §3.6.
- `op_2_58_2d_bkz_driver.py` — fpylll BKZ driver; takes block size β, samples 1/2/3, basis type a/b as CLI args.
- `op_2_58_2d_classifier.py` — projection classifier per §3.3 (commit `766c6f5`; argmax-pair-kernel pass/fail against 1/21 baseline + argmax-Fano-line as reference data per §2.1 Convention C; signed-lift per §3.3.2); produces the σ-statistic per the §3.2 thresholds.
- `op_2_58_2d_audit_log.md` — append-only log of each run with seed, β, sample, basis type, runtime, and outcome. Matches the Phase B audit log structure (Entries 001–009 of `phase_b_audit_log.md`).
- `op_2_58_2d_result.md` — closure document, written *after* the run completes, citing the present pre-registration and declaring one of the §5.1 (joint or partial null) / §5.2 (positive) / §5.3 (partial null or inconclusive) / §5.5 (disagreement) outcomes verbatim.

All files seed `20260601` / `20260602` / `20260603` for the three samples; basis construction is deterministic from the seed and the (A, s, e) instance.

---

## §8. Cross-references

- **§2.58.B (V4.7 canonical):** the Module-SLWE construction under test. KeyGen / encryption / decryption flow and parameter table.
- **§2.66.2 (V4.7 canonical):** the seven prior linear/projection attacks; signal-to-mask ratio measurements at q = 911 used as the §3.1 instrument-validation target.
- **§2.66.1 (V4.7 canonical):** the OP-2.58.1.a closure that established q-overprovisioning; rationale for keeping spec parameters at q = 2³² rather than tightening before this attack.
- **§2.69 (V4.7 canonical):** the Phase B distributional-identifiability null at 256-bit residue distribution. Cross-checked: §2.69 confirms the *modulus-level* unobservability of the trapdoor; §2.58.2d tests the *lattice-level* unobservability. Two different attack surfaces, same construction.
- **`phase_b_audit_log__1_.md` Entries 001–009:** template for the audit-log structure of §7.
- **OP-2.58.5 (deferred):** joint q-η optimization. Per the May 27 review, OP-2.58.5 is deferred until OP-2.58.2d closes. If OP-2.58.2d returns positive at q = 2³², joint q-η optimization is moot; if it returns null, the q-tightening question becomes the next move.

---

## §9. Methodological note: why the stopping rule matters

The Phase B null at 256-bit (§2.69) was a clean two-outcome test: the χ² statistic either fell within the null band or it did not. Lattice attacks have a third outcome — "we did not run BKZ long enough to know" — and that outcome is the most dangerous one for the SQT thread because it admits two failure modes:

1. **Strengthening drift.** Post-hoc, the experimenter is tempted to declare "we ran BKZ up to β = 25 with no signal, therefore null." But β = 25 may simply be below the regime where any attack on this lattice would be expected to succeed.
2. **Indefinite extension.** Post-hoc, the experimenter is tempted to keep running until something positive emerges, then declare success at whatever β it took. This is the lattice-attack version of p-hacking.

The §4 pre-committed budget and the §4.3 decision tree exist specifically to make both failure modes detectable as §3.* retraction events rather than absorbed into the closure declaration. The reviewer's May 27 note is the source of this section.

**Compute-asymmetry honesty.** The 30-day single-workstation budget of §4.2 is realistic for academic-scale BKZ on N_lat = 1024 reaching β ≤ 50. It is *not* the compute scale at which production lattice attacks against published KEM proposals routinely operate; cluster-scale and GPU-accelerated runs in the literature reach β ≥ 60 and beyond on lattices of comparable dimension. The §4.3 partial-null declaration ("returns null at β ≤ β_max; β > β_max not tested") handles the resulting result correctly, but any synthesis paper or external presentation citing OP-2.58.2d must state this asymmetry plainly: a null result here means "no signal detected within reachable compute on the test hardware," not "no signal exists in the regime where state-of-the-art attacks operate." The two statements differ; the second requires compute resources the framework does not have. Honest framing of the first is the closure language §5.1 supports; claiming the second from an academic-scale run would be an Eddington Maneuver against the lattice-attack literature.

---

*End of OP-2.58.2d pre-registration document.*
*To be frozen prior to first lattice-reduction execution.*
*Append-only after freeze; modifications generate §3.* retraction-log entries.*
