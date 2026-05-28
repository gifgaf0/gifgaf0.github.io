# OP-2.58.2d — Pre-Freeze Infrastructure Correctness Report

**Date:** May 27, 2026
**Brief:** CLAUDE_CODE_BRIEF_07_OP_2_58_2D_PREFREEZE_CORRECTNESS.md (items 2, 3)
**Status:** Pre-freeze. No code was executed against the §2.58.B construction
at the spec parameters of §3.1. Synthetic / toy-scale (q=911, k∈{1,7}) only.
**Feeds:** §3.3 footnote (classifier candidate-cutoff) and §3.6 (lattice
construction conventions). Findings below may revise the pre-registration
pre-freeze — which is drafting, not a §3.* retraction.

---

## 0. Headline

Item 3 (primal lattice construction) is **complete and round-trips**, after a
**convention fix**: the brief's literal §3.2 basis does not round-trip; the
correct sign was pinned and tested.

Item 2 (classifier) is **partially blocked**: the bit-exactness requirement of
§2.3 **cannot be verified** because the §2.66.2 classifier source is absent
from the repo. A faithful reconstruction from the §3.3 spec was built and it
reproduces §2.66.2-*class* recovery behaviour, but "identical to §2.66.2" is
**unverified**. Three substantive findings (below) warrant pre-freeze revision
of §3.3.

Per brief §6, these blockers are returned rather than papered over. **The
freeze should wait on findings F1, F4, F5 below.**

---

## 1. Item 3 — Primal LWE lattice construction

**Files:** `op_2_58_2d_lattice_attack.py`, `test_op_2_58_2d_lattice_construction.py`
(14 tests, all passing).

### F-LAT-1 — §3.2 convention does not round-trip; pinned the fix

The basis literally written in brief §3.2 has `+A_scalarᵀ` in the middle block
with last row `[b_scalarᵀ | 0 | 1]` and target `(e, s, 1)`. Working through
`z·B = (e, s, 1)` with `b = A·s + e`:

> first block of `z·B` = `q·z₁ + s·A_scalarᵀ + b_scalar`. With `s·A_scalarᵀ =
> A_scalar·s` this is `q·z₁ + A_scalar·s + b_scalar`, which can equal `e_scalar`
> only if `A_scalar·s + b_scalar ≡ e_scalar`, i.e. `2·A_scalar·s + e ≡ e` — false.

The standard primal-with-target embedding requires the **negative**:
`-A_scalarᵀ` (equivalently the relation `e = b − A·s`). With that sign,
`z = (m₀, s_scalar, 1)` where `m₀ = (e + A_scalar·s − b)/q` is an exact integer
vector, and `z·B = (e, s, 1)` exactly. **Pinned convention:**

```
B = [ q·I_{n_eff}     0          0  ]   (n_eff rows)
    [ -A_scalarᵀ   I_{n_eff}     0  ]   (n_eff rows)
    [  b_scalarᵀ      0          1  ]   (1 row)
```

target `v_target = (e_scalar, s_scalar, 1)`, row convention `z·B`, dimension
`(2·n_eff + 1)`, `N_lat = 2·n_eff`.

**Recommended §3.6 action (pre-freeze):** §3.6 says "standard primal with
target embedding," which is a *class* of conventions. Pin the specific member
above (sign `-A_scalarᵀ`, b in the last row, target `(e, s, 1)`, row
convention). This report is the pinning artifact item 3 was for.

### Round-trip and convention results (toy q=911, k=7, η=2, h_s=14, seed 20260527)

- **Round-trip:** `v_target = z·B` exactly, `z = (m₀, s_scalar, 1)`. ✓
- **Norm:** `‖v_target‖ = 14.93`, matches `√(‖e‖²+‖s‖²+1)` independently. ✓
- **BDD / uSVP:** `gh(B) = 107.9` (dim 225, det `q^{112}`); `‖v_target‖ < gh`. ✓
  The instance is in the unique-decoding regime.
- **det B = q^{n_eff}:** confirmed structurally (block lower-triangular with
  diagonal blocks `q·I, I, [1]`) and by exact Bareiss determinant on a tiny
  k=1 instance (dim 33). ✓
- **Sedenion unrolling:** `A₁₁·s₁` via sedenion product == 16×16 left-mult
  block applied to `s₁`. ✓
- **Scalar-LWE:** `A_scalar·s_scalar + e_scalar ≡ b_scalar (mod q)`, and the
  sedenion-form `b` reshapes to the same `b_scalar`. ✓
- **h_s at toy scale:** §3.1 of the pre-registration defines `h_s = h_r = 64`
  only at spec. Per brief §3.2 we use `h_s_toy = round(64·7/32) = 14`,
  documented in the instance generator.

### F-LAT-2 (minor) — §3.3 test-2 N_lat typo

Brief §3.3 test 2 parenthetically says "for N_lat = 112 at toy k = 7." That
conflicts with brief §3.2 and pre-reg §3.6, both of which give
`N_lat = 2·n_eff = 224` at toy k=7 (n_eff = 16·7 = 112). The tests use the
correct `N_lat = 224`. Recommend correcting the parenthetical pre-freeze.

### Out of scope (as specified)

The Fano-projected basis (b) of §3.6 is a `NotImplementedError` stub
(post-freeze; depends on §2.58.B Fano-line data). No BKZ. No spec parameters.

---

## 2. Item 2 — Classifier port and fixture validation

**Files:** `op_2_58_2d_classifier.py`, `test_op_2_58_2d_classifier.py` (9 tests,
all passing), `fixtures/op_2_58_2d_classifier_fixtures.json`.

### F1 (BLOCKER) — §2.66.2 classifier source absent; bit-exactness unverifiable

The §2.66.2 classifier source files named in the brief
(`op_2_58_2_leakage_test.py`, `op_2_58_2b_advanced_attacks.py`) are **not
present** anywhere in the repo (verified by file search and content grep). The
pre-registration §3.3 commits the classifier as *identical* to the §2.66.2 one,
and §2.3 makes bit-exactness the core requirement of item 2. **With no oracle,
this cannot be checked.**

- **Path A (existing fixtures):** impossible — no §2.66.2 fixtures exist.
- **Path B (regenerate):** forced, and **circular** — the regenerated fixtures
  use the classifier-under-test as their own oracle. The fixtures JSON header
  names this circularity explicitly (brief §6 requirement) and the
  `independent_checks` list provides the non-circular mitigation: clean
  `K_{a,b}` basis vectors whose in-subspace closure ratio is analytically 1.0
  (a value known without reference to the classifier).

**Reconstruction fidelity (diagnostic, not proof):** the reconstructed
classifier reproduces §2.66.2-*class* behaviour. On 500 random ZD-noise vectors
`z = Σ αⱼ kⱼ`, `αⱼ ∈ {−1,0,+1}`, sampled from the pair-kernels:

| quantity | this reconstruction | §2.66.2 (reported) | chance |
|---|---|---|---|
| pair recovery | 96.2% | (one of 65.4% / 93.0%) | 4.76% |
| Fano-line recovery | 88.0% | (one of 65.4% / 93.0%) | 14.29% |

Same order, same phenomenon (strong recovery far above chance), but **not
proven identical**.

**Recommended §3.3 action (pre-freeze):** either (i) obtain the §2.66.2
classifier source and run the bit-exactness comparison before freeze, or
(ii) re-scope the §3.3 "identical to §2.66.2" commitment to "reconstructed from
the §3.3 spec; cross-attack comparability rests on shared subspace definitions
and the σ-statistic, not on a byte-level identity that cannot be checked." The
cross-attack comparability argument of §3.3 currently rests on an unverifiable
identity.

### F2 — pinned subspace definitions (resolved, documented)

- `K_{a,b}` (4D, "16→4"): the real span of the four clean ±1 two-term
  cross-edge kernel vectors of `L_x` for `x = e_a + e_{b+8}` (a<b), from
  `op_2252_v2_kernel_involution.py`. Verified 4-dimensional for all 21 pairs.
- `F_L` (8D, "16→8"): the real span of the kernels of the three pairs on line
  `L = {a,b,c}` — `span(K_{a,b} ∪ K_{a,c} ∪ K_{b,c})`. **Verified exactly
  8-dimensional for all seven lines**, matching the pre-reg "16→8 drop" and
  §3.6(b)'s "using the kernel-basis output of op_2252." This is the natural
  reading; absent the §2.66.2 source it cannot be confirmed as *the* intended
  `F_L`, but it is dimensionally exact and analytically clean.

### F4 (FINDING for §3.3) — the seven F_L subspaces overlap

The seven `F_L` are **not pairwise disjoint**. A clean `K_{1,2}` basis vector
projects with ratio 1.0 onto **two** lines' subspaces, not one. This is a
direct consequence of the kernel-involution structure (OP-2.25.2-V2): a pair's
kernel is supported on the cross-edges of the *other two pairs through the
shared third point*, which lie on *other* Fano lines. Consequence:

- **§2.5 test 3's strict "‖P_{F_L'} b‖²/‖b‖² < 1 for all L' ≠ L" is FALSE by
  construction.** The test was adjusted to assert the two properties that DO
  hold: (i) in-subspace closure `‖P_{F_L} b‖²/‖b‖² = 1`, and (ii) a near-uniform
  argmax distribution on random vectors (each line ≈ 1/7, within ±3.5% at
  N=1000). The overlap itself is asserted as a regression check
  (`test_fano_subspaces_overlap_finding`).

**Recommended §3.3 action (pre-freeze):** §3.3 must not assume the `F_L` are
disjoint. State that the argmax classifier operates over overlapping subspaces
and that the σ-statistic is the meaningful output, not per-vector subspace
membership.

### F5 (FINDING for §3.3) — "Fano-line class of a ZD-noise vector" is ambiguous

Because the `F_L` overlap, a single clean `K_{a,b}` basis vector is recovered
to its containing line in only some cases — on the 21 single basis vectors the
argmax-line lands on the *containing* line only part of the time, and every
clean basis vector sits at ratio 1.0 in exactly two lines. The ambiguity has a
structural source: the "Fano line of `z_i ∈ K_{a,b}`" could mean (i) the line
*containing* the pair `{a,b}`, or (ii) the lines *supporting* the kernel (the
two partner pairs' lines through the third point). These differ under the
involution. Generic random noise resolves the ambiguity statistically
(88% land on the containing line), but the *definition* is not pinned by the
available documents.

**Recommended §3.3 action (pre-freeze):** define `ℓ(z_i)` precisely — almost
certainly "the line containing the pair from which `z_i` was sampled" — and
note that single-vector recovery is inherently ≤ 2-way ambiguous while
distributional recovery is not. This matters for the 5σ accounting: the
baseline and the ceiling both depend on which definition is used.

### Q1 (brief §2.6) — candidate-cutoff factor-of-2 precedent

**No precedent can be found.** The §2.66.2 source is absent, and a repo-wide
search for the "twice the shortest output norm" cutoff returns nothing.
**Treat the factor-of-2 as a NEW pre-registered parameter introduced by
OP-2.58.2d** and name it as such in a pre-freeze revision to §3.3 measurement
(1) — e.g. "candidate-cutoff factor c = 2, pre-registered here (no §2.66.2
precedent located)."

### Q2 (brief §2.6) — is the factor-of-2 doing meaningful work?

**Partial answer; full answer deferred to the BKZ smoke test (item 4).** The
cutoff is defined against "the shortest output norm at that β" — i.e. against
BKZ output. No BKZ runs exist yet, so the cutoff cannot be exercised on real
reduced bases. On the synthetic fixtures (uniform `𝕊_911^7`), vector norms are
tightly concentrated, so a factor-of-2 cutoff is a **near-no-op** (admits
>95% of candidates). That is expected, not degenerate: the cutoff is meant to
exploit the short-vs-bulk norm separation that BKZ *produces*, which the
ambient random distribution does not have. **Recommended §3.3 note:** state
that the cutoff is calibrated against BKZ output norm structure, not the
ambient candidate distribution, and report the actual passing-count
distribution once the item-4 BKZ smoke test produces reduced bases. If at that
point the cutoff is degenerate (too few candidates for σ-statistics, or a
no-op on reduced bases too), the proposed alternative is "top-k shortest
vectors for fixed k."

---

## 3. Fixture sourcing summary (brief §5)

- **Path used: B (regenerated), forced** by the absence of the §2.66.2 source.
- **Circularity:** named explicitly in the fixtures JSON header; mitigated by
  the `independent_checks` (analytic closure = 1.0, non-circular).
- Header records seed (20260527), p (911), k (7), N (500), source classifier
  file, subspace source, repo commit at generation, and the candidate input
  convention (mod-p residues, signed-lifted to `(-p/2, p/2]` before
  projection — see F-CLS-bug below).

### F-CLS-bug (resolved during item 2) — input convention

The classifier must signed-lift its mod-q candidate input to `(-q/2, q/2]`
before the Euclidean projection; a raw residue 910 would otherwise be read as
+910 instead of −1. This is idempotent on already-small signed vectors (BKZ
short vectors), so the real-attack use is unaffected. Fixed and documented; the
fixtures record the convention.

---

## 4. Spec-parameter discipline confirmation (brief §6)

**No code was executed against the §2.58.B construction at the spec parameters
of §3.1 (k = 32, q = 4,294,977,961).** All work is toy-scale (q = 911,
k ∈ {1, 7}). The lattice instance generator refuses `q ≥ SPEC_Q` or `k ≥ SPEC_K`
unless `allow_spec_params=True` (never set by default); this gate is enforced
and tested (`test_spec_params_refused_by_default`). The classifier is
scale-agnostic but was exercised only at p = 911.

---

## 5. Freeze recommendation

The freeze should **wait** on the following pre-freeze revisions:

1. **F1 (load-bearing):** resolve the §2.66.2 bit-exactness question — obtain
   the source and compare, or re-scope the §3.3 "identical to §2.66.2"
   commitment. The cross-attack comparability argument currently rests on an
   unverifiable identity.
2. **F4 / F5:** revise §3.3 to (a) acknowledge the `F_L` overlap and (b) pin the
   definition of `ℓ(z_i)`.
3. **Q1:** name the factor-of-2 candidate cutoff as a new pre-registered
   parameter in §3.3.
4. **F-LAT-1:** pin the specific primal embedding convention (sign `-A_scalarᵀ`)
   in §3.6.

Items that are clean and need no revision: the lattice round-trip, BDD, det,
unrolling, and scalar-LWE properties (item 3); the `K_{a,b}` (4D) and `F_L`
(8D) dimensional structure (item 2). Q2 and the BKZ-driven cutoff calibration
are correctly deferred to the item-4 smoke test.

---

## 6. Brief-08 pre-freeze item closure (L1, F1, D1)

The three remaining Rev 3 pre-freeze items are now resolved. Each is a discrete
signed pre-freeze edit (Brief 08, §5 sequencing L1 → F1 → D1); the result files
carry the patch strings.

### L1 — §2.66.2 pair-vs-line attribution → UNATTRIBUTABLE (unlocatable)
See `op_2_58_2d_L1_attribution_note.md`. The §2.66.2 source, the SQT master
ledger (`SQT_Master_Ledger_v4_0_CANONICAL.md`), and the Phase-B audit log
(`phase_b_audit_log.md`) are **all absent from the repo and its full git
history** — none has ever existed on any branch. The 65.4%/93.0% numbers
survive only as uncaptioned reference data in §2 of this report. No evidence-
based §3.3 attribution is possible; the attribution-dependent sentence is
instead replaced by the F1 (b/c) framing.

**Retraction-grade flag (Brief 08 §7):** the total absence of the §2.66.2
attribution weakens the SQT thread's reliance on §2.66.2 as a load-bearing
reference below what the Rev 3 pre-registration assumes. There is no ledger
file in this repo to record this into; it is surfaced here for freeze
consideration.

### F1 — signed-lift discrimination → (b/c) closure selected
See `op_2_58_2d_F1_result.md`. 4-number matrix (q=911, N=500, seed 20260527):
pair 96.2% (lift on) / 41.8% (lift off); line 88.0% (lift on) / 89.6% (lift
off). The with-lift figures reproduce the §2 baseline exactly. Neither metric
approaches §2.66.2's 65.4% under disabled lift, so possibility (a) (signed-lift
= the §2.66.2 bug) is **ruled out**; this converges with L1's unattributable
resolution on the **(b/c)** §3.3 closure paragraph. Disable-path instrumentation
confirmed (910 → +910, not −1). No SNR consequence (outcome is (b/c), not (a)).

### D1 — §3.6(b) F_L union dimension → rank 14 at both q
See `op_2_58_2d_D1_result.md`. Exact F_q-rank of the 16×56 stacked kernel basis
is **14** at q = 911 and **14** at q = 4,294,977,961 (ranks agree). Each K_{a,b}
is 4D and each F_L is 8D at both primes (sanity confirmed). Rank 14 is in the
expected 9–15 band given F4 (partial F_L overlap; not the 8 or 16 edge cases).

### Freeze readiness

OP-2.58.2d pre-registration Rev 3 is now ready for §3.3.1 second-stage cutoff
repin (pending item-4 smoke test) and §6 freeze. No remaining pre-freeze
placeholders or deferred sub-tasks. The §2.66.2 retraction-grade weakness (L1)
should be visible to the freeze signer but does not itself block the freeze:
the F1 (b/c) closure was chosen precisely so that the §3.3 commitment no longer
depends on the unverifiable §2.66.2 identity.

---

## 7. Brief-09 closure (Q2 cutoff repin, Q3 SNR)

The final pre-freeze dependency — the §3.3.1 short-vector cutoff repin — is
resolved by the toy-scale BKZ smoke test (`op_2_58_2d_bkz_smoke.py`,
`op_2_58_2d_bkz_smoke_results.md`). One conditional item (Item 5 / Q3) fired.

### Q2 — §3.3.1 cutoff → RATIFY factor-of-2.0 (outcome a)
See `op_2_58_2d_Q2_cutoff_repin.md`. At β=30 (where fplll BKZ solves the toy
uSVP on all three seeds, min norm 4.1–4.6), pair-recovery is **100%**, flat
across every swept cutoff N ∈ {1.0…10.0}, with pooled σ = 7.75 vs the 1/21
baseline and zero variance across seeds. At β=20 BKZ does not reduce the lattice
(stuck at q-vectors, norm 911) and there is no signal at any N. No discontinuity
at either β → the §3.4(c) instability outcome is **ruled out** (the §5 goal).
The cutoff is non-binding at toy scale (single trapdoor vector, ≫10× separated
from the bulk), so 2.0 is ratified as safe but fine N-discrimination is deferred
to the secondary-run gate (consistent with the Brief-07 Q2 prediction). The
§3.3.1 patch is a value-unchanged addendum. Item 2 lattice→classifier sanity
passed (planted e → true pair, ratio 1.0).

### Q3 — §3.1 SNR target → downgrade to reference-only (Item 5 fired)
See `op_2_58_2d_Q3_snr_check.md`. The toy-scale SNR proxy ‖e‖/‖A·s‖ ≈ 0.0053
(three seeds) is ~2× the §3.1 target of 0.0025 and outside ±10%. Combined with
the L1/§2.69.1 finding that the §2.66.2 SNR figure's definition is
unattributable (amplitude-vs-power offset would explain the factor of 2) and the
toy-vs-spec regime mismatch, the recommendation is to **downgrade the §3.1
"SNR ≈ 0.0025 within 10%" from a validation gate to a reference value**, pending
a written spec-scale re-derivation with an explicit definition.

### Freeze readiness
The §3.3.1 cutoff repin (Q2) and the §3.1 SNR disposition (Q3) are the last
pre-freeze items. With the Q2 addendum and the Q3 SNR downgrade applied to the
pre-registration (by the session, append-only), OP-2.58.2d has no remaining
provisional values or open pre-freeze dependencies and is ready for the §6
freeze. The spec-parameter gate remains enforced and tested (new
`test_op_2_58_2d_bkz_smoke.py` adds two gate assertions); the full suite is
303 tests passing.

---

## 9. Brief-10.5 closure (L2 — §2.58.B construction implemented)

The Brief-10 primary run halted because the §2.58.B construction was not present
as executable code (L2 finding, §2.69.2). Brief 10.5 implements it:
`tools/op_2_58_2d_construction.py` (`gen_zd_noise_sample`, `gen_public_matrix`,
`gen_spec_instance`), built from canonical §2.58.B prose on top of the existing
sedenion / kernel-involution / lattice modules (all consumed unchanged). See
`op_2_58_2d_L2_construction_note.md`.

**Implemented:** §2.58.B KeyGen steps 1–5 at toy scale, spec-gate enforced. 12
toy tests pass (secret non-ZD, z ∈ 84-ZD set, ℓ/pair label consistency, kernel
containment L_z·e=0, α range/distribution, 4D kernel basis, b round-trip, spec
gate, matrix-structure halt).

**Halted (surfaced for session resolution):**
- **§2.3 public-matrix structure.** Only `"uniform"` is implemented; the
  PSL(2,7)-equivariant and Singer-cycle readings raise `NotImplementedError`
  (runtime message cites §2.3 and §2.69.2). The choice materially changes the
  attack surface and is a session-level structural decision; (b)/(c) need a
  follow-on Brief 10.6.

**§2.4 σ finding:** the cross-check (σ ∈ {1,2,4}) gives **95.857% pair-recovery
at every σ, spread 0.000%** — σ is non-load-bearing at toy scale (the projection
ratio is scale-invariant). Cross-check **PASS** (within ±3% of the Brief-08
96.2% baseline; the small gap is the canonical-allowed all-zero-α coordinate).

**Path to Brief 10 re-attempt:** the construction now exists and is toy-verified.
The primary run remains blocked on (1) committing the frozen Rev 5
pre-registration with a signed §6 (orchestrator freeze check), and (2) resolving
the §2.3 matrix-structure gap (+ Brief 10.6 if (b)/(c)). Lattice basis (b)
remains a stub. Full suite: 322 passing (OP-2.58.2d suite: 53 tests).

---

## §10. Brief 10.6 closure (pre-schedule)

Brief 10.6 closed the three pre-schedule questions left open by Brief 10's
proof-of-life run.

### §10.1 Item 1 — basis-(b) design ratification

**Ratified reading: (I) F_L-restriction.** Three candidate readings of §3.6(b)
("lattice basis pre-projected onto the union of the seven 8D F_L subspaces")
were considered: (I) restriction — replace e-side q·I_n rows with q·F_L per
block; (II) augmentation — enrich basis (a) with 14·k unscaled F_L basis
vectors as auxiliary short rows; (III) quotient — project to F_L⊥ (rejected
on prose grounds, "onto" not "out of").

Toy comparison at k=7 q=911 β=30 across seeds 20260601/02/03 under the §3.3.1
N=2.0×min_norm cutoff and 1/21≈0.0476 baseline:

| basis              | tot_short | tot_hits | pooled rate |
|--------------------|-----------|----------|-------------|
| (a) primal         | 675       | 24       | 0.0356 (below baseline) |
| (b)-I restriction  | 633       | 34       | **0.0537 (RATIFIED)**   |
| (b)-II augmentation| 294       | 0        | 0.0000 (degenerate)     |

Reading (II) is INVERSE to Brief 10.6's predicted outcome — under the frozen
§3.3.1 cutoff, the unscaled F_L hint vectors (norm ≈ 1.0 after LLL) hijack
the short-set selection and the trapdoor signal is not captured. Reading (I)
is the worst-case-for-defender and is the ratified basis (b).

Code: `tools/op_2_58_2d_lattice_attack.build_fano_projected_lattice`. Rejected
(II) retained as `_build_fano_augmentation_lattice` for the audit record.
Full ratification record: `tools/op_2_58_2d_basis_b_ratification.md`.
Reproducer: `tools/op_2_58_2d_basis_b_compare.py`.

### §10.2 Item 2 — σ resolution

**Pinned: σ = 2.** Sub-case 1 (cite §2.66.1 / DFR analysis) did not close —
§2.66.1 is not present on-branch (only §2.66.2 line classifier is referenced;
the L1 attribution gap of §3.3 applies). Sub-case 2 (derive from η=2 and
kernel-vector structure) closed cleanly.

Empirical finding at q=911 over 50 seeds × k=7 × DIM=16 = 5600 coords/σ:
every nonzero `e_d` is **exactly ±σ** — the rref_kernel basis vectors have
disjoint support per coordinate, so no superposition occurs and the η bound
on `|e_d|` translates directly to a bound on σ. With η=2: σ ≤ 2; σ ∈ {1, 2}
feasible, σ = 4 violates η.

Pin σ = 2 (worst-case-for-defender within η: the largest noise the
construction permits, max BDD radius for the attacker). Matches the
proof-of-life setting. The σ ∈ {1, 2, 4} cross-check (Brief 10.5 §2.4)
spanned the η bound to characterise classifier σ-invariance; the schedule
stays within η.

**Classifier-vs-lattice-attack sensitivity (Brief 10.6 §3.4)**: σ is
non-load-bearing for the §3.3 classifier (exact direction-only invariance,
95.857% pair-recovery across σ ∈ {1,2,4} with 0.000% spread — Brief 10.5
finding); σ IS load-bearing for the lattice attack (scales ‖e‖, hence
‖v_target‖, hence BDD radius). At spec k=32 σ=2, ‖v_target‖ ≈ 27 ≪ gh ≈ 5×10⁵
→ uSVP regime → BKZ-recoverable in principle at sufficient β.

Sub-case 3 (sweep over σ) ruled out; schedule remains 42 runs, not 126.
No production-code change required — `_run_one`'s `job.get("sigma", 2)`
default already conforms. Full record: `tools/op_2_58_2d_sigma_resolution.md`.

### §10.3 Item 3 — Full pre-reg text committed

`OP_2_58_2d_staging_PREREGISTRATION.md` now contains the full Rev 5 binding
text (§§1–6) supplied by the session principal, replacing the §6-only stub.
The §2.1 forward-pointer to §2.58.B.1 is included (the clarifying
V4.11-consistent addition: pair-recovery is a lower bound on kernel-recovery;
pair-null safely upper-bounds kernel leakage). Per Brief 10.6 §4.4: **this is
not a Rev 6** — committing the full text completes the on-branch realization
of the already-frozen Rev 5; the §6 freeze signature
`AUTHORIZED_RUN_V4.11_MAY_27_2026` covers it.

Audit Entry 002 (the orchestrator's freeze-verification entry) records the
SHA-256 of the committed text:
`ecbb7dfc19d3491d37d6a6b961387b0e3e70637c0dd47a958d19d4fa5ffdd12e`. The
orchestrator's `verify_freeze()` recomputes the hash at run time so the
binding result is provably tied to the exact frozen text in the repo at that
run.

Regex update: the freeze-verification regex was tightened to require a
literal colon between "Freeze date/signature" and its value, so §6's intro
paragraph mention ("the freeze date and the freeze signature are added in the
same act…") doesn't false-match. The regex also tolerates the markdown `**`
bolding around the field label.

### §10.4 Out-of-session prerequisite (the only remaining work)

After Brief 10.6: OP-2.58.2d is fully prepared. The construction (Brief 10.5),
the trapdoor geometry (§2.58.B.1), the proof-of-life pipeline (Brief 10),
basis (a) and basis (b) (both ratified, Brief 10.6 Item 1), σ pinning
(Brief 10.6 Item 2), and the full binding pre-reg text on branch (Brief 10.6
Item 3) are all in place. The orchestrator's construction-availability check
now returns `basis_b_ready=True`, `construction_ready=True`, no blockers.

The only remaining prerequisite for an OP-2.58.2d result is the 30-day
wall-clock compute of the 42-run schedule (§4.2), which the proof-of-life
confirmed is realistic but out-of-session. When that compute completes,
closure follows the Brief-10 §3.4 / pre-reg §5 structure: the verbatim
§5.1/§5.2/§5.3/§5.5 outcome declaration, the per-(β, sample, basis) table,
the §4.3 decision-tree resolution, and the ledger entry.

Suite: 325 passing post-Brief-10.6; ruff clean on touched files.

---

## §11. Brief 10.7 closure (σ noise-model reconciliation, §2.69.3)

Brief 10.6 Item 2 pinned σ=2 via the η=2 boundary derivation because
§2.66.1 was reported as "not citable, branch-absent." Session review found
§2.66.1 IS in canonical V4.9 (line 2162) — branch-absent but fully
recoverable. The third branch-absence finding in the OP-2.58.2d arc (filed
as §2.69.3 in canonical V4.12) and the mildest of the three (§2.69.1:
§2.66.2 scripts source-absent; §2.69.2: §2.58.B construction source-absent;
§2.69.3: §2.66.1 branch-sync gap, recoverable).

### §11.1 §2.66.1 recovery (Item 1)

`tools/op_2_58_2d_dfr_reference.md` recovers the load-bearing facts of
§2.66.1 to the branch: Var(N)=(η/2)·(h_s+h_r+1), η=2 by ML-KEM convention
(not DFR optimisation), DFR slack to η=512 (no DFR-constrained σ-band),
and the load-bearing scope distinction — §2.66.1 analyses **unconfined**
CBD(η); §2.58.B deploys **confined** kernel-restricted noise. §2.66.1 is
the cross-check anchor, not the calibration target.

### §11.2 The noise-model reconciliation (Item 2)

`tools/op_2_58_2d_sigma_calibration.py` (branch-adapted, N=50,000, p=911;
kernel structure is q-independent per A1/D1):

| metric | confined σ=2 | CBD(η=2) | role |
|---|---|---|---|
| per-coordinate variance | 1.332 | 1.000 | easy scalar — necessary, not sufficient |
| per-block Euclidean norm | 4.514 ± 0.965 | 3.953 ± 0.614 | **BDD-radius metric the attack sees** |
| occupied dimensions | 5.33 ± 1.89 | 10.0 ± 1.93 | **fingerprint: distinct distributions** |

**Mean-norm ratio 1.142** — confined σ=2 is 1.14× larger than CBD(η=2),
the conservative direction (larger noise → harder attack → conservative
null). **Occupancy means non-overlapping** (5.33 vs 10.0) — the confined
sampler is genuinely a different distribution, not a CBD reparameterisation;
this is the load-bearing fingerprint preventing the cross-check from being
misread as a calibration.

`test_op_2_58_2d_sigma_calibration.py` locks both claims (norm ratio in
the 1.05–1.25 band; occupancy means non-overlapping) plus the 1/√k
aggregate-averaging assumption.

### §11.3 Dissolution of the σ-band concern

The Brief 10.6 worry — "σ=2 might be the weak-null corner of a DFR-
constrained band" — is **dissolved** by §2.66.1: there is no
DFR-constrained band. η=2 is fixed by ML-KEM convention; DFR slack is many
orders of magnitude in either direction (log₂ DFR ≈ −10¹⁴ at η=512). σ=2
is fully determined by the §2.58.B sampler definition realising the η=2
convention — it is not a sweep target, not a band corner, not a
calibration. The sub-case 2 derivation (σ ≤ η = 2) agreed on the value
but missed the framing; §2.69.3 supplies the correct anchor.

### §11.4 Two-level conservatism statement

Per-block:
- Mean norm ratio 1.14 (confined > CBD in mean).
- P(confined per-block norm > CBD per-block norm) = 0.71 — the distributions
  overlap; the conservative direction is a 71% statement at the
  per-block level. Range of per-block ratios: [0, 3.27] (lower tail driven
  by the ~1.2% all-zero-α blocks and single-active-α blocks).

Aggregate (k=32 — the operative BDD radius):
- Per-block draws are independent by construction (per §2.58.B KeyGen each
  z_i and its α are drawn independently; the shared public matrix A enters
  the signal A·s, not the noise offset e).
- 1/√k averaging collapses the per-block spread; aggregate ratio converges
  to 1.14.
- Verified empirically by `aggregate_independence()`: aggregate norm mean
  26.11 matches the √(32·E‖e‖²) = 26.12 independent-draw prediction to
  0.05%; per-block→aggregate CV ratio is 6.78 ≈ √32; P(confined aggregate
  < CBD aggregate) = 0.001 (vs 0.29 per-block).
- **The attack sees the aggregate, not per-block.** A pair-recovery null
  at σ=2 is conservative at the aggregate BDD radius.

### §11.5 Methodological note (carried to closure & any synthesis)

The σ pin went **variance-match → norm-check → sampler-definition with
cross-check → cross-check defended across draws**, and σ=2 survived all
four while each metric reframed the prior justification. The convenient
metric (per-coordinate variance, scalar, attack doesn't see) was never
allowed to stand as the justification once the load-bearing metric
(aggregate BDD norm with its spread) was an hour of compute away. When a
reviewer asks "why that noise level, and does it match what the
construction deploys?", the answer is measured at every level —
per-coordinate, per-block, aggregate, across-draws — not assumed.

The Brief 10.6 sigma_resolution.md remains on-branch as the contemporaneous
record of the sub-case 2 derivation; it is **not retracted**. It pins the
same value (σ=2). §11 here updates the JUSTIFICATION (norm cross-check,
not η-boundary alone) and the FRAMING (cross-check, not calibration). Both
documents are valid; this one is the operative anchor.

### §11.6 Code touch (Item 3)

- `op_2_58_2d_construction.gen_spec_instance` docstring reframed: σ=2 is
  the confined-sampler value cross-checked against CBD(η=2) by aggregate
  BDD norm. Cites §2.69.3 + `op_2_58_2d_sigma_calibration.py` +
  `op_2_58_2d_dfr_reference.md`.
- `op_2_58_2d_primary_run._run_one` σ default comment reframed (BDD-norm
  cross-check, not per-coord variance).
- `op_2_58_2d_primary_run.main` Audit Entry 002 now prints the σ pin with
  the norm ratio (1.14), occupancy (5.33 vs 10.0), and aggregate
  inversion probability (≈0.001) alongside the prereg SHA-256.

### §11.7 Out-of-session prerequisite (the only remaining work)

After Brief 10.7: every pre-schedule parameter is pinned with an on-branch
derivation. Construction (Brief 10.5), trapdoor geometry (§2.58.B.1),
pipeline (Brief 10 proof-of-life), basis (a)/(b) ratified (Brief 10.6
Item 1), σ=2 pinned with norm/occupancy reconciliation (Brief 10.7), full
binding text + SHA-256 + σ pin in Audit Entry 002 (Brief 10.6 Item 3 +
Brief 10.7 Item 3), §2.66.1 recovered to branch (Brief 10.7 Item 1).

The only remaining step toward an OP-2.58.2d result is the 30-day
wall-clock compute of the 42-run schedule (pre-reg §4.2), out-of-session
by necessity. Per the §2.1 §2.58.B.1 forward-pointer, a pair-recovery null
at σ=2 safely upper-bounds kernel-level leakage at the operational noise
level (conservative in the aggregate BDD radius via §2.69.3 / §11.4).

Suite: 327 passing post-Brief-10.7 (325 prior + 2 reconciliation tests);
ruff clean on touched files.

---

*End of OP-2.58.2d pre-freeze infrastructure correctness report.*
