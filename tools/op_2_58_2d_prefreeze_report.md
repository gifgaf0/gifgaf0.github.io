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

*End of OP-2.58.2d pre-freeze infrastructure correctness report.*
