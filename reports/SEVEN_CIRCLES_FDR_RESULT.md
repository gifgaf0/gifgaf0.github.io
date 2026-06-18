# Seven-Circles Look-Elsewhere Result

**Date:** 2026-06-03
**Status:** R1 (computational; reproducible from the dump + generator).
**Tool:** `tools/run_seven_circles_fdr.py` (uses `tools/fdr_lookelsewhere.py`).
**Inputs:** the canonical dump — `cross_ratios.txt` (11,495 CRs) and
`cross_ratios_by_chord.json` — generated verbatim from the locked sweep
(R=3, r=1, 40 chords d∈linspace(0.1,3.8,40), θ=0, all finite 4-subset
cross-ratios). N=11,495, 123 matches, cos 18° at 14/40 reproduced exactly.

## What was tested

Whether the seven-circles headline — *"cos 18° is the joint-highest-frequency
framework constant, ~10× null enrichment"* — survives a program-level
look-elsewhere control. Two questions at the granularity each is claimed:

- **Finding #1 (total):** are 123 matches over 11,495 CRs more than chance?
  Control = **placebo library** (real CR values fixed; the 23 framework
  constants replaced by random fake constants). Resampling the values against
  the *real* library is degenerate (recovers ~123 by construction) and is not
  used.
- **Finding #2 (per-constant, chord granularity):** is "cos 18° at 14/40 chord
  positions" special? Null = draw a random fake constant, count how many of the
  40 chords contain ≥1 CR within tolerance.

Each under two nulls: **log-uniform** over the value support [1, 1111], and
**empirical-density** (fake constants are randomly chosen actual CR values — the
strictest pipeline-geometry control). τ = 5×10⁻⁴, 20,000 draws, value+reciprocal
matching, full 23-entry library (15 reachable at this tolerance).

## Result

| Test | null | observed | mean(null) | enrichment | p-value | verdict |
|---|---|---:|---:|---:|---:|---|
| #1 total | log-uniform | 123 | 37.9 | 3.24× | 1.0e-02 | marginal |
| #1 total | empirical-density | 123 | **443.5** | **0.28×** | 1.0 | consistent w/ geometry |
| #2 cos 18° | log-uniform | 14/40 | 1.06 | 13.2× | 1.5e-02 | marginal |
| #2 cos 18° | empirical-density | 14/40 | 9.57 | **1.46×** | **0.35** | consistent w/ geometry |
| #2 √5/2 | empirical-density | 14/40 | 9.57 | 1.46× | 0.35 | consistent w/ geometry |
| #2 cos π/7 | empirical-density | 13/40 | 9.57 | 1.36× | 0.38 | consistent w/ geometry |

## Verdict

**The "~10× enrichment" headline does not survive a proper look-elsewhere
control.**

- The strictest honest null (empirical-density — fake constants drawn from where
  the pipeline actually puts CR mass) makes cos 18°'s 14/40 **consistent with
  chance (p ≈ 0.35, 1.46×)**. A random CR value already hits ≈9.6 of the 40
  chords, because CR values recur across chords as `d` varies — a geometric
  property of the sweep, not specialness of cos 18°.
- At the total level, a random 23-constant library drawn from the value
  distribution catches **~444 matches**; the framework library's **123 is
  0.28×** — *fewer* than random. The framework constants are not located where
  the CR density is highest.
- Even the favorable null (log-uniform over the full support) only reaches
  ~3× / 13× at **p ≈ 0.01–0.015 (marginal)**, not ~10×, and would fall further
  if the support were restricted to where framework constants actually live.

The original "~10× null enrichment" figure must have been computed against a
null far sparser than the pipeline's own value distribution (e.g. random
log-uniform sampling over a narrow range against the same library). Pinning the
null is exactly the gap this instrument was built to close.

## Honest scope

- This **does not** refute the *prior-address* arguments for cos 18° (the
  pentagon-deficit / bilateral-fold route, §2.45-NGA, and the µH proton-radius
  residual). It refutes only the **seven-circles cross-ratio enrichment** as
  independent evidence for cos 18° being distinguished. A genuine prior address,
  if derived, stands on its own; the cross-ratio probe simply does not add
  independent statistical weight.
- The empirical-density null is conservative by design; the log-uniform null is
  the other bracket. Both land at "marginal at best," neither at "~10×."
- Reproduce: `python3 tools/run_seven_circles_fdr.py cross_ratios.txt
  cross_ratios_by_chord.json`.

## Recommended ledger action

File as a negative result on the **seven-circles enrichment claim** (the §3.06
chord-CR closure is the precedent). Correct any citation of "~10× null
enrichment" to "consistent with pipeline geometry under an empirical-density
null; marginal (p≈0.01–0.015) under a log-uniform null." The cos 18° prior
address (§2.45-NGA) is unaffected and should be cited on its own basis.
