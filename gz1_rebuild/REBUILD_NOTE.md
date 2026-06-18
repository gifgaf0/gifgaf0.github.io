# GZ1 REBUILD NOTE

**Date:** 2026-06-13. **Class:** REPRODUCTION (rebuild against a known R1 record;
not a new gate, not load-bearing). Discharges the optional-hygiene CC-reproduction
registered in ledger v4.36. **Master Ledger untouched.**

## What these files are
Reconstructions of the Gate G-ζ1 instrument, lost to a sandbox reset. They were
rebuilt **only** from the three surviving documents (the binding protocol):
- `originals/GZ1_EXECUTION_PREREGISTRATION.md` (date 2026-06-09)
- `originals/GZ1_GATE_EXECUTION_REPORT.md` (date 2026-06-10)
- `originals/phase4_fits.json` (the original fit outputs)

The reconstruction was written against the pre-registered protocol + R1 targets,
**not** against the lost source code. Per the brief, the comparison target
ζ = 1 − π/√12 appears in exactly one file, `comparison_step.py`, which runs last
(Eddington isolation preserved). Self-contained: numpy + scipy only; no framework
tool imported.

## Original md5s (for contrast; the originals are lost, so byte-identity is NOT
expected — these record what was)
- `gz1_core.py` : 13d01cf8
- `comparison_step.py` : 726488a5
- `phase4_fits.json` : 8d87ca96

Rebuilt-file md5s are in `MANIFEST.md5`. A reproduction is judged by **R1-record
agreement** (targets reproduced within tolerance), not byte-identity — the lost
sources cannot be byte-matched and no attempt was made to.

## Underspecified choices made (HARD RULE 4 log — standard choices, none resolved
by reference to any target value)
1. **Quench internals (Phase 1):** dtau = 2e-3, steps = 4000, seed-noise
   amplitude 1%, renorm-each-step — taken from `tools/mv_g1_minimiser.py`
   defaults, which the pre-registration explicitly cites as the canonical I1–I3
   instantiation. Two kernels run: the V4.26 grid-FFT disk kernel (headline,
   canonical-object replication) and the binding continuum Bessel kernel Ũ(q);
   both logged in `phase1.json`.
2. **Cell scan window (Phase 2):** 17 points over a ∈ [0.9, 1.1]·a_kc, centred on
   the **target-independent** big-box k_c estimate from Phase 1 (a_kc = 1.4406);
   parabolic refine on the best 3; cell grid n = 64; scan 2500 / polish 12000
   imaginary-time steps. The scan objective is the energy density at fixed mean
   density ρ₀=1 (the −μ∫ρ term is constant across the scan).
3. **BdG basis (Phase 3):** plane-wave cutoff n_b = 32 (cutoff check vs 40);
   ψ₀ coefficients read from the polished n=64 cell FFT with anti-alias
   truncation |Δm| < n/2 (logged). Normal-incidence line 61 points; Γ–M–K–Γ
   path 16/10/16 points/segment. Gap detection: lower-envelope coverage with a
   0.15 minimum-width cut.
4. **Strip (Phase 4):** 16 rows, Lx = a*, Ly = 16·d_row, periodic both ways;
   grid **Nx = 24, Ny = 192** (a reconstruction choice — the report does not
   pin the strip grid; the pre-registration says "~36 rows" while the report §4
   says "16-row strip", and the **report (the execution record) was followed**:
   16 rows). Isotropic Gaussian source σ = 0.5, ψ₀-masked, on the row-0 site.
   GMRES rtol = 3e-4, restart = 200, maxiter = 250, damping η = 0.02 (and 0.05
   for the independence check).
5. **Fit conventions:** decoded from the field structure of the original
   `phase4_fits.json` — `rows_rel` = per-row envelope / row-0; `wrap_min_row` =
   argmin over rows 1..N−1; `clean_ratios` = consecutive ratios over rows
   1..max(wrap_min_row−2, 2); `t_ratio_median/spread` = median / population-σ
   of those; `kappa_fit` = −slope of ln(rows_rel) vs y over rows
   1..max(wrap_min_row−1, 6); `t_fit` = exp(−κ·d_row); `fit_r2` = linear-fit r².
   These were inferred to match the original schema; they were **not** tuned to
   any κ/t value.

## Known reconstruction deviations from the R1 record (logged, not hidden)
- **Phase 3b 2D-path persistence:** the report states gaps A and B persist over
  the Γ–M–K–Γ path (A2 normal-incidence only). The rebuild finds **all three**
  gaps filled somewhere on the K-direction of the path. A secondary 2D-path
  characterisation difference (does not enter the verdict, which rests on the
  normal-incidence gaps + the gapless density channel + the strip decay).
- **Gap A decay constant:** κ(Gap A) = 0.573 (rebuilt) vs 0.806 (original);
  t = 0.485 vs 0.362. The largest quantitative deviation, concentrated at Gap A
  because its midgap (ω≈21.3) sits just above the gapless acoustic top (20.45),
  where the coarser strip grid gives wrap_min_row = 8 (vs 6) and a flatter fit
  window. **Gaps A2 and B reproduce κ/t to within a few %** (κ 0.448 vs 0.470;
  0.210 vs 0.217). The η-independence of κ(Gap A) is reproduced (0.1% shift),
  confirming the decay is a genuine evanescent stop-band decay in the rebuild too.
