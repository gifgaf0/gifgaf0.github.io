# op_2_58_2d_dfr_reference.md — §2.66.1 load-bearing facts (Brief 10.7 Item 1)

**Status**: Branch-recovered reference for §2.66.1 (DFR closure). The full
canonical entry lives in `SQT_Master_Ledger_v4_9_CANONICAL.md` §2.66.1 (line
2162). This file is the on-branch recovery per Brief 10.7 §3.1 / §2.69.3
(branch-sync gap), so the OP-2.58.2d closure can cite §2.66.1's load-bearing
facts without round-tripping through the canonical ledger.

**Branch-absence context**: Brief 10.6 Item 2 reported "§2.66.1 not citable
from on-branch state" and fell through to sub-case 2 (derive σ from η=2
boundary). Session review found §2.66.1 IS in canonical V4.9; only branch-
absent. This is the third branch-absence finding in the OP-2.58.2d arc and
the mildest — fully recoverable — filed as §2.69.3 (V4.12).

---

## §1. Load-bearing facts from §2.66.1

§2.66.1 closes OP-2.58.1.a (DFR analysis). The facts the OP-2.58.2d schedule
needs:

1. **Noise distribution.** Centred binomial distribution CBD(η) per coordinate
   of e (and of r at the decryption side). The two CBD draws contribute
   independently to the decryption-failure sum.

2. **Variance formula.** Per §2.66.1 derivation:

   Var(N) = (η/2) · (h_s + h_r + 1)

   where N is the per-coordinate decryption-failure sum, η is the CBD width,
   h_s = h_r = 64 (sparse-secret weights, OP-2.58.2d pre-reg §3.1).

3. **DFR slack (η-sweep).** §2.66.1 evaluates DFR for η ∈ {2, 4, 8, …, 512} at
   the spec parameters (q = 4,294,977,961, k = 32, n_eff = 512). The headline:
   DFR ≤ 2⁻¹²⁸ for **all η up to η = 512** (log₂ DFR ≈ −10¹⁴ at η = 512,
   asymptotic to the absolute floor at η near 1024). **No DFR-constrained
   σ-band exists** — DFR is satisfied with massive slack across the full
   η-range OP-2.58.B could plausibly use.

4. **η = 2 by ML-KEM convention.** The pinned η = 2 in OP-2.58.2d pre-reg §3.1
   is selected by ML-KEM convention (matching the Kyber/ML-KEM standard
   parameter), **not** by DFR optimisation. The DFR slack at η = 2 is
   enormous; ML-KEM's η = 2 choice was a security-noise-budget compromise
   in the original lattice-LWE setting.

5. **Distribution scope (load-bearing for OP-2.58.2d Brief 10.7).** §2.66.1
   analyses **unconfined** CBD(η) noise: "independent of the sedenion
   non-associative structure," i.e., the analysis treats each of the
   n_eff = 512 coordinates as an independent CBD(η = 2) draw. This is the
   correctness-analysis proxy. §2.58.B as deployed uses **confined**
   kernel-restricted noise (e_i = σ · Σ_j α_j · k_j⁽ⁱ⁾ with α_j ∈ {−1, 0, +1}
   and k_j⁽ⁱ⁾ the 4D kernel basis of L_{z_i}). These are **distinct
   distributions** — see §2.69.3 / `op_2_58_2d_sigma_calibration.py` for the
   occupancy fingerprint (confined: 5.3 ± 1.9 occupied dims/block; CBD(η=2):
   10.0 ± 1.9 occupied dims/block; non-overlapping means).

   §2.66.1 is therefore the **cross-check anchor**, not the calibration
   target. σ for the §2.58.B sampler is pinned at σ = 2 by the sampler's own
   definition (the ternary α with ±1 kernel basis); §2.66.1's CBD(η = 2) is
   the comparison reference in the BDD-norm metric.

## §2. Why the branch-sync gap mattered (and didn't)

Brief 10.6 Item 2 sub-case 1 said "check §2.66.1 first". When §2.66.1 isn't
on-branch, the question reframes to "what bounds σ?" — and without §2.66.1,
the answer leans on the η = 2 boundary alone (the sub-case 2 derivation:
σ ≤ η = 2). That derivation **agrees with σ = 2** as the pinned value but
**misses the load-bearing fact** that §2.66.1 establishes no DFR-constrained
σ-band exists at all. The earlier worry ("σ = 2 might be the weak-null
corner of a DFR-constrained band") is dissolved by §2.66.1: there is no
band; the slack is many orders of magnitude on either side of η = 2.

The recovery here ensures any closure document citing σ = 2 can cite the
correct anchor: §2.66.1 fixes η = 2 by convention with no DFR constraint
on σ; §2.69.3 cross-checks the deployed (confined) noise against §2.66.1's
(unconfined CBD) reference in the BDD-norm metric.

## §3. Cross-references

- **Canonical**: `SQT_Master_Ledger_v4_9_CANONICAL.md` §2.66.1 (full entry).
- **V4.12 annotation**: §2.66.1 carries a §2.69.3 forward-pointer per the
  Cluster-M-append patch (May 27, 2026) — additive only, DFR closure body
  unchanged.
- **§2.69.3** (V4.12) — branch-sync gap + noise-model reconciliation.
- **§2.58.B.1** (V4.11) — confirms the kernel-basis vectors are clean ±1
  two-term; the input to the reconciliation script.
- **OP-2.58.2d Rev 5 pre-reg §3.1** — names η = 2; σ = 2 realises it as the
  confined sampler value (per §2.69.3, not per η-boundary alone).
- **Brief 10.6 Item 2** (`op_2_58_2d_sigma_resolution.md`) — the earlier
  derivation; sub-case 1 reported as "not citable" is now reframed as
  "branch-absent, recoverable" by this reference and `op_2_58_2d_sigma_calibration.py`.
- **Brief 10.7** — this brief, which recovers §2.66.1 and commits the
  reconciliation.
- **`op_2_58_2d_sigma_calibration.py`** — the on-branch reconciliation
  computing the BDD-norm cross-check (1.14× conservative) and occupancy
  fingerprint (5.3 vs 10.0).
