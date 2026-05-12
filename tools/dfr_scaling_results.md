# Module-SLWE empirical DFR scaling

| k | q | failures | trials | DFR | log2(DFR) | notes |
|---|---|---|---|---|---|---|
| 4 | 911 | 5015 | 10000 | 5.015e-01 | -1.00 | completed in 32s |
| 8 | 911 | 4958 | 10000 | 4.958e-01 | -1.01 | completed in 107s |
| 12 | 911 | 4990 | 10000 | 4.990e-01 | -1.00 | completed in 227s |
| 16 | 911 | 4994 | 10000 | 4.994e-01 | -1.00 | completed in 387s |

**Linear fit:** log2(DFR) ≈ −0.000 · k + −1.001

## Reading the numbers

The empirical DFR sits at the noise-only ceiling (≈ 0.5) for every k
in the sweep. There is no usable slope to fit: the per-trial DFR is
already saturated at k=4. The cause is upstream of this script — see
`tools/QUESTIONS.md` §1 — the supplied `tools/sqt_slwe.py` self-
reports DFR ≈ 0.48 at (p=911, k=4) with the explicit verdict "noise
too large for this p", and our measurement at 10 000 trials matches.
Increasing k past 4 does not improve correctness because the noise
budget is already exceeded.

**Caveat on the q axis.** The brief specifies "q ≈ 2^24 for upper
sizes". The supplied source has `p = 911` as a module-level constant
(SPEC.md §2.6 toy parameters; the comment requires `p ≡ 1 mod 5,7,13`
for the PSL(2,7) symmetry the scheme is built on). The q axis cannot
vary without scheme-level edits. This sweep therefore varies k only;
the q column reads 911 throughout.

A meaningful DFR-scaling curve will need (a) §1's noise budget fixed
so DFR at k=4 is well below 0.5, and (b) the source parametrised in
p so q can sweep alongside k. Both are flagged in
`tools/QUESTIONS.md` for sign-off.

Slope is in bits of failure-rate reduction per unit increase in
module rank.
