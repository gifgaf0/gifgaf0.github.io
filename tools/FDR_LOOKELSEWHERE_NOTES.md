# FDR / Look-Elsewhere Calculator — Notes

**Tool:** `tools/fdr_lookelsewhere.py` (stdlib only, no deps).
**Perspective-1 instrument** for `reports/SQT_v4.24_FIVE_PERSPECTIVES.md`.

## What it answers

The Prior Address Standard audits each constant's lineage individually. It does
not bound the *program-wide* rate at which a random probe value lands within
tolerance of **some** entry of a small constant library. This tool computes that
expected spurious-hit count, so every hit table can carry its own null
expectation, a Poisson p-value, and an enrichment factor.

For N probes, M-target library, relative tolerance τ:

- **E[total spurious hits]** = N · Σ p_c
- **E[distinct constants hit]** = Σ (1 − (1 − p_c)^N)
- **p-value** for observed K = P(Poisson(E) ≥ K)
- **enrichment** = observed / E

with per-target probability p_c under one of three nulls:

| Null | p_c | When to use |
|---|---|---|
| `log` (default) | ln((1+τ)/(1−τ)) / ln(b/a) | values span scales; scale-agnostic |
| `uniform` | 2τc / (b−a) | values roughly linear on [a,b] |
| `empirical` (`--values`) | (Monte Carlo from your actual values) | total-count question; folds in real pipeline geometry |
| `placebo` (`--placebo`) | (random fake constants from `--values` support) | **single-constant question** — is *this* constant special vs random constants in the same distribution? |

The library is the full production 23-entry `CURATED_CONSTANTS` from
`seven_circles_tight.py` (supplied 2026-06-03).

## Usage

```bash
# Worked seven-circles example (analytic + Monte Carlo, partial library):
python3 tools/fdr_lookelsewhere.py --demo

# Total-match level: N cross-ratios, observed total matches:
python3 tools/fdr_lookelsewhere.py --n 11495 --tol 5e-4 --range 0.05 25 \
    --null log --reciprocal --observed 123 --mc 20000

# Single constant at a chord-position count:
python3 tools/fdr_lookelsewhere.py --n 40 --tol 5e-4 --range 0.05 25 \
    --null log --reciprocal --only "cos(18deg)" --observed 14

# EMPIRICAL null (total-count question) from the actual values, one float/line:
python3 tools/fdr_lookelsewhere.py --values cross_ratios.txt --tol 5e-4 \
    --reciprocal --observed 123

# PLACEBO test (single-constant question): is cos(18deg) special vs random
# constants drawn from the SAME value distribution?
python3 tools/fdr_lookelsewhere.py --values cross_ratios.txt --tol 5e-4 \
    --reciprocal --only "cos(18deg)" --observed 14 --placebo 20000
```

Analytic and Monte Carlo agree to within sampling error (validated in `--demo`:
E=51.8 vs MC mean=51.7). MC auto-caps trials by a compute budget
(`MC_MAX_DRAWS`) so large N stays responsive.

## Two findings that already matter

1. **The "~10× enrichment" headline is null-dependent — and ~1.7× under the
   full library.** Under a log-uniform null on [0.05, 25] with the production
   23-entry library, the seven-circles total (123 matches over 11,495
   cross-ratios) is **~1.71×** (E[total] ≈ 72; Poisson p ≈ 3.3e-8 — still
   formally above chance, but not ~10×). With the partial 14-entry library it
   was 2.4×; adding the real library entries *lowered* the enrichment, as a
   look-elsewhere correction must. Always report the null and the library size
   next to an enrichment claim.

   **Provenance caveat (open).** The 11,495 denominator is not reproducible
   from the canonical sweep (40 chords × C(12,4) = 19,800; the report's 11,495
   is a different/filtered config). This is the same class of issue as the
   §2.66.2 attribution gap. Lock a stated sweep and regenerate, rather than
   reverse-engineer 11,495 (see "what to hand the generator", below).

2. **The placebo test is what decides single-constant specialness.** The
   total-count empirical null answers "are 123 matches more than chance?"; the
   *placebo* null answers "is cos 18° special *vs other constants in the same
   distribution*?" — the one that controls for pipeline geometry. Validation:
   on synthetic values with a deliberately-seeded cos 18° cluster, the placebo
   test correctly returns SIGNAL (p ≈ 2.5e-4); on a broad distribution with no
   seeded cluster it returns ~chance. **Feed `--values` the real cross-ratios
   and run `--placebo` before citing that cos 18° is special.**

## What to hand the seven-circles generator

To make both findings airtight, regenerate the cross-ratio dump from a **locked,
stated** sweep (there is no saved file; CRs are computed on the fly in
`seven_circles_tight.py`):

- **Config to lock** (the canonical one in `seven_circles_report.md`): R=3, r=1,
  7 natural circles, 40 chord positions d ∈ linspace(0.1, 3.8, 40), θ=0, all
  4-subsets of intersection points with exactly 4 valid intersections.
- **Emit:** (a) `cross_ratios.txt` — one CR value per line (for `--values`), and
  (b) a one-line manifest: the exact intersection/4-subset rule, the total count
  (this *replaces* the unreproducible 11,495), and per-constant chord-position
  hit counts (for the 14/40-style placebo at chord granularity).
- Then: `--values cross_ratios.txt --observed <total>` for finding #1, and
  `--placebo 20000 --only "cos(18deg)" --observed <hits>` for finding #2.

## Caveats / honest limits

- Analytic nulls assume disjoint match intervals (true at τ = 5e-4 here) and
  that target intervals lie inside the support (unreachable targets are
  reported and contribute 0).
- This bounds *accidental* matches under an explicit null. It does **not**
  adjudicate whether a matched constant has a genuine prior address — that
  remains the PAS's job. The tool tells you when a match is *not yet*
  surprising; it never certifies that one *is* meaningful.
