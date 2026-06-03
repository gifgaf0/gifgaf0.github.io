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
| `empirical` | (Monte Carlo from your actual values) | **most defensible** — folds in real pipeline geometry |

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

# EMPIRICAL null from the actual computed values (one float per line):
python3 tools/fdr_lookelsewhere.py --values cross_ratios.txt --tol 5e-4 \
    --reciprocal --observed 123
```

Analytic and Monte Carlo agree to within sampling error (validated in `--demo`:
E=51.8 vs MC mean=51.7). MC auto-caps trials by a compute budget
(`MC_MAX_DRAWS`) so large N stays responsive.

## Two findings that already matter

1. **The "~10× enrichment" headline is null-dependent.** Under a log-uniform
   null on [0.05, 25] with the partial 14-entry library, the seven-circles
   total (123 matches over 11,495 cross-ratios) is **~2.4×**, not ~10×. The
   enrichment number is a function of the assumed range, the library size, and
   the null — none of which the original report pins down. Report the null
   explicitly next to any enrichment claim.

2. **The empirical null is the one that decides it.** When the actual probe
   distribution already clusters near a target (because the pipeline *produces*
   those values), the empirical null absorbs the apparent signal: in a
   stress test where 200 of 4,200 values were seeded near cos 18°, the
   empirical-null enrichment was **0.95× (p ≈ 0.78)** — consistent with chance.
   This is exactly the pipeline-geometry-vs-special-constant distinction
   Perspective 5's placebo test targets. **Feed `--values` the real
   cross-ratios before citing significance.**

## Caveats / honest limits

- The default library is **partial (14 of the production 23)**; a smaller M
  *understates* the look-elsewhere effect. Paste the real `CURATED_CONSTANTS`.
- Analytic nulls assume disjoint match intervals (true at τ = 5e-4 here) and
  that target intervals lie inside the support (unreachable targets are
  reported and contribute 0).
- This bounds *accidental* matches under an explicit null. It does **not**
  adjudicate whether a matched constant has a genuine prior address — that
  remains the PAS's job. The tool tells you when a match is *not yet*
  surprising; it never certifies that one *is* meaningful.
