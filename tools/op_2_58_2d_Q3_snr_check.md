# OP-2.58.2d §3.1 SNR target check (Brief 09, Item 5 — Q3)

**Date:** May 27, 2026
**Brief:** CLAUDE_CODE_BRIEF_09 §3.5 (Item 5, conditional — FIRED).
**Status:** Pre-freeze. Toy scale q=911, k=7.
**Cross-ref:** §2.69.1 attribution-gap ledger entry (Brief-08 L1 finding).
**Recommendation:** downgrade the §3.1 SNR target to "reference value only,
not a validation gate," pending a written spec-scale re-derivation.

---

## 1. Measurement

SNR proxy ‖e‖ / ‖A·s‖ on the **generic** toy instances (sparse-uniform η=2
error — the toy analog of the spec noise; not the planted-ZD error):

| seed | ‖e‖ | ‖A·s‖ | SNR = ‖e‖/‖A·s‖ |
|---|---|---|---|
| 20260601 | 14.46 | 2792.7 | 0.005177 |
| 20260602 | 15.13 | 2919.1 | 0.005184 |
| 20260603 | 15.17 | 2760.9 | 0.005493 |
| **mean** | | | **0.005285** |

## 2. Comparison to the §3.1 target

The Rev 4 §3.1 secondary-run target is **SNR ≈ 0.0025 within 10% relative
error**, i.e. the band [0.00225, 0.00275]. The measured toy proxy ≈ **0.00529**
is roughly **2×** the target and lies well outside the ±10% band. The
measurement does **not** reproduce 0.0025 within 10%.

## 3. Why this is a Q3 (not a clean ratify or a clean refutation)

Two compounding issues mean the discrepancy cannot be resolved at toy scale:

1. **Definitional unattributability (L1 / §2.69.1).** The §3.1 SNR target
   inherits its 0.0025 value from the §2.66.2 reference, whose source numbers
   the Brief-08 L1 finding showed are unattributable (no source, no ledger, no
   audit log in the repo or its history). "SNR" is not pinned to a formula: the
   measured 0.00529 is an amplitude (norm) ratio; a power ratio (‖e‖²/‖A·s‖²)
   would give ≈ 2.8e-5, and other normalizations are possible. A factor-of-2
   gap is exactly what an amplitude-vs-power or per-coordinate-vs-aggregate
   definitional mismatch would produce. Without the source, the gap cannot be
   attributed to a real SNR difference vs a definitional one.

2. **Regime mismatch.** The toy parameters (q=911, k=7, η=2, h_s=14) are a
   different regime from spec (q=4,294,977,961, k=32, h_s=64). ‖A·s‖ scales with
   q and the secret/noise sparsity, so the toy SNR is not expected to equal a
   spec-derived SNR target. Comparing the toy proxy to a spec figure is
   apples-to-oranges.

The toy proxy lands in the **same order of magnitude** as the target (both
~10⁻³), which is reassuring, but "within 10%" is not satisfied and cannot be
made meaningful under the two issues above.

## 4. Recommendation (§3.5)

Per brief §3.5, the measurement differs materially, so file this as Q3 and
recommend: **the §3.1 "SNR ≈ 0.0025 within 10%" should be downgraded from a
validation gate to a reference value only**, OR re-derived in writing at spec
parameters with an explicit SNR definition before it is used as a gate. This
mirrors the L1 disposition of the §2.66.2 numbers: a figure whose provenance is
unattributable should not be load-bearing as a pass/fail gate.

Proposed §3.1 edit framing (applied by the session, not this brief):

> **§3.1 SNR note (Brief-09 Q3).** The SNR ≈ 0.0025 figure inherited from
> §2.66.2 is reference-only: its definition is unattributable (§2.69.1) and a
> toy-scale amplitude-ratio proxy ‖e‖/‖A·s‖ measures ≈ 0.0053 (same order,
> outside ±10%, plausibly an amplitude-vs-power definitional offset). The SNR is
> not a secondary-run pass/fail gate pending a written spec-scale re-derivation
> with an explicit definition.

## 5. Scope marker

This affects only §3.1's SNR target disposition. It does not alter §3.3.1
(handled in `op_2_58_2d_Q2_cutoff_repin.md`) or any other section.
