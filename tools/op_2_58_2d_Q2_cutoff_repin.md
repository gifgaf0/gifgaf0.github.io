# OP-2.58.2d §3.3.1 cutoff repin recommendation (Brief 09, Item 4)

**Date:** May 27, 2026
**Brief:** CLAUDE_CODE_BRIEF_09 §3.4 (Item 4)
**Status:** Pre-freeze. Toy scale only.
**Decision: OUTCOME (a) — RATIFY factor-of-2.0.**
**Inputs:** `op_2_58_2d_bkz_smoke.py`, `op_2_58_2d_bkz_smoke_results.md`.

---

## 1. Summary table

| β | uSVP solved (3 seeds) | recovery at N = 2.0 (pooled) | σ at N=2.0 | recovery across N ∈ {1.0…10.0} | discontinuity? |
|---|---|---|---|---|---|
| 20 | No (all stuck at q-vectors) | 0.068 (≈ baseline) | 2.50 | flat ≈ baseline, never 5σ | none |
| 30 | Yes (all; min norm 4.1–4.6) | **1.000** | **7.75** | **flat at 1.000** | none |

Baseline = 1/21 ≈ 4.762%. §3.2 threshold = 5σ.

## 2. Rationale

At β = 30 — the block size at which BKZ actually reduces the toy lattice — the
pair-recovery rate at N = 2.0 is **100%**, identical across all three seeds
(zero sample variance), and **flat across the entire swept neighborhood**
N ∈ {1.0, 1.25, …, 10.0}. Pooled σ = 7.75, comfortably above the §3.2 5σ
threshold. There is no discontinuity and no sample disagreement at any N. This
is the §3.4(a) condition for ratification: high, stable, monotone recovery in a
neighborhood of N = 2.0.

The flatness has a specific cause worth recording (it qualifies the ratify but
does not weaken it): at toy scale the leakage instance produces a **single**
near-trapdoor vector, separated from the bulk of the BKZ output (≈ 889) by more
than 190×. Every cutoff from N = 1.0 to N ≈ 190 therefore selects exactly that
one vector, so the recovery rate is insensitive to N within the swept range.
factor-of-2.0 is safely inside this flat high-recovery band; so would be 1.5 or
3.0. The toy data ratifies 2.0 as a **safe** value but cannot finely discriminate
it from neighbors, because the graded short-vs-bulk norm distribution that the
cutoff is designed to filter does not exist at β ≤ 30 on a toy instance (Brief-07
Q2: the cutoff is calibrated against BKZ output norm *structure*, which only
emerges at higher β or on genuinely §2.58.B-structured multi-vector leakage).

The §5 purpose of the smoke test — **rule out instability (c)** — is achieved:
the cutoff is a well-defined scalar, the recovery-vs-N curve is flat/monotone at
both β tested, and the three seeds agree. No §3.3.1 re-specification is needed.

## 3. Proposed §3.3.1 patch (verbatim addendum; the value is unchanged)

The factor-of-2.0 value **stays**. Append the following empirical-confirmation
sentence to §3.3.1 (this is the §3.4(a) no-op-plus-addendum form):

> **§3.3.1 addendum (Brief-09 smoke test, toy scale q=911, k=7).** The
> factor-of-2.0 short-vector cutoff is empirically ratified: at β=30, where BKZ
> solves the toy uSVP, pair-recovery is 100% (pooled σ = 7.75 vs the 1/21
> baseline) and flat across all swept cutoffs N ∈ [1.0, 10.0], with no
> discontinuity and zero variance across three seeds (20260601/602/603). The
> cutoff is non-binding at toy scale (the toy leakage instance yields a single
> trapdoor vector separated from the bulk by ≫10×, so any N in the swept range
> is equivalent), and at β=20 BKZ does not reduce the toy lattice enough to
> surface signal at any N. The fine signal-vs-dilution calibration that would
> discriminate among candidate N values requires higher β or §2.58.B-structured
> multi-vector leakage and is deferred to the §3.1 secondary-run validation
> gate; factor-of-2.0 is retained as a standard-practice value confirmed safe by
> this smoke test.

## 4. Scope marker

This recommendation changes **only** §3.3.1 (an addendum; the factor value is
unchanged). The SNR target of §3.1 is handled separately in
`op_2_58_2d_Q3_snr_check.md` (Item 5 fired). No other §3.x section is touched.
The pre-registration edit itself is applied by the session, not by this brief
(brief §4.2, append-only discipline).
