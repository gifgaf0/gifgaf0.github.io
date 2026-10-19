# E7 reconciliation: original run vs independent cross-check

**Scope.** E7, scale and coupling audit (SEED.md §8).

**Inputs.**
- The original scripts and outputs in `experiments/E7_scale_audit/`.
- The cross-check in `experiments/E7_scale_audit/crosscheck/`: `CROSSCHECK.md` and `crosscheck.json`, with 2 major and 8 minor issues.

**Method.** For each issue I read both codes. Where the two disagreed numerically, I ran a decisive computation of my own:
- for the Demidov–Levkov figure, vector-path extraction from the PDF;
- for the hopfion, a symbolic identity plus a tail-correct re-optimisation.

Where the original was wrong, its scripts were fixed and rerun: `e7_hopfion.py`, the new `e7_dl_digitize.py`, `e7_audit.py`, `make_figures.py`, `collect_results.py`, `run_all.sh`. The cross-check folder was not modified.

**Outcome.**
- The cross-check was right on both major issues and on every minor point.
- All 10 issues are resolved, and none is left OPEN.
- No seed-claim verdict changed.
- Two CALIBRATED labels became CONSISTENT.

## Issues

| # | Severity | Issue | Who was right | Resolved |
|---|---|---|---|---|
| 1 | major | DL high-energy exponent F | cross-check | yes |
| 2 | major | Hopfion energy-rms radius | cross-check | yes |
| 3 | minor | Hopfion E_W labelled CALIBRATED | cross-check | yes |
| 4 | minor | Proton M·R labelled CALIBRATED | cross-check | yes |
| 5 | minor | QED illustration coupling identification | cross-check | yes |
| 6 | minor | E1e combination missing; P thresholds over-read | cross-check | yes |
| 7 | minor | Label, rounding and radius-definition inconsistencies | cross-check | yes |
| 8 | minor | LEP bound qualifier | cross-check | yes |
| 9 | minor | Unlisted deviation (own hedgehog) | cross-check | yes |
| 10 | minor | "Any soliton" wording | cross-check | yes |

### 1. Demidov–Levkov high-energy exponent (major)

**Issue.**
- `e7_audit.py` hard-coded `F2 = 3.93`, an eye reading of arXiv:1103.0013 Fig. 3b, stated as ±0.05.
- The cross-check's pixel digitisation gave 3.845 at the plateau and 4.48 at threshold.

**Diagnosis.** I settled this with a third method that depends on neither reading. The figure is gnuplot vector output, so `e7_dl_digitize.py` converts page 3 with `pdftocairo -svg` and parses the stroked paths:
- The y ticks of the upper panel lie at 58.63, 71.95 and 85.29 pt, i.e. 13.33 pt per 0.2 in F.
- The tick-label glyph sequences are [4, ., 4], [4, ., 2] and [4, ., 0]. They share digits with the "1.2", "10" and "11" labels, so the labels are decoded consistently.
- The x ticks are labelled 7 to 11. The curve's 18 vertices fall on round g²E values (6.26, 6.3, 6.4, 6.6, …, 11.5, 11.6, 11.7), which confirms the x calibration.
- The left axis edge (tick labelled 2g²M_S) reads g²E = 6.2324, against 6.2358 from our quadrature.

Results:
- F = 3.846 at g²E = 11.5;
- minimum F = 3.844 at g²E = 11.0;
- F = 4.480 at the first vertex, g²E = 6.26;
- reading uncertainty about ±0.002.

So the original's 3.93 was off by −0.085, outside its own ±0.05. Its threshold value of 4.45 was within tolerance but is now 4.48.

The same extraction on arXiv:1103.2133v2 Fig. 7b (δρ = 0 line) gives g²N_min = 3.977 (3.971–3.983 over g²E = 8.5–10.5) and 4.55 near threshold. The original 3.98 stands.

**Action.**
- New `e7_dl_digitize.py`, writing `dl_digitized.json`.
- `e7_audit.py` reads it, with the same vector readings typed in as a fallback, and records the version-1 eye readings for provenance.

Downstream values, before → after:

| Quantity | Version 1 | Version 2 |
|---|---|---|
| F, high-energy plateau | 3.93 | 3.844 (3.846 at g²E = 11.5) |
| F, threshold | 4.45 | 4.480 |
| κ = F/N_pair | 0.630–0.714 | 0.616–0.718 |
| g² for P = 0.1 / 1/e / 0.5 | 1.71 / 3.93 / 5.67 | 1.67 / 3.84 / 5.55 |
| M_S/m at P = 0.1 | 1.83 | 1.87 |
| QED fold-like suppression (g² = α) | 10⁻²³⁴ | 10⁻²²⁹ |

The pairs panel of `fig_vacuum_pairs.png` was regenerated. No conclusion changes.

**Resolved:** yes.

### 2. Hopfion energy-rms radius (major)

**Issue.** The original gave R̃_rms = 2.1441 (Ward units); the cross-check gave 2.0608.

**Diagnosis.**
- Version 1 used a 24-node not-a-knot cubic spline for f(t), t = r/(1+r), with f(1) = 0 but a free slope at t = 1. That means f ≈ a/r at large r.
- ∫r²ε d³r then grows linearly with the cutoff and is truncated only by the last Gauss node.
- The energy and the ring radius are insensitive to the tail, which is why they agreed.

A symbolic computation, now inside `e7_hopfion.py`, proves an exact identity. The angle-averaged densities of the hedgehog-Hopf ansatz are

- (16/3)(f′² + 2 sin²f/r²) and
- (16/3)(4 sin²f f′²/r² + 2 sin⁴f/r⁴).

So E_W[f] = (1/3π²) · E_ANW[F], with F(y) = f(y/√2). The minimiser is therefore f(r) = F_Skyrme(√2 r), and:
- R̃_rms = x_E/√2 = 2.06082;
- R̃_ring = x_½/√2 = 1.23930;
- E_W = a₁/(3π²) = 1.2314457.

Three independent numbers agree:

| Method | R̃_rms |
|---|---|
| Corrected optimiser (tail-correct spline f = (1 − t)²h) | 2.06080 |
| Exact Skyrme profile through the same 3D quadrature | 2.06083 |
| Identity | 2.06082 |

The cross-check was right.

**Action.** `e7_hopfion.py` version 2:
- profile f = (1 − t)²h(t), which builds in the correct C/r² tail;
- symbolic identity check;
- exact-profile check.

A first version-2 run kept the 600 × 64 3D quadrature inside the L-BFGS-B loop. Under shared CPU load it took more than 12 CPU-minutes, because the tail direction is nearly flat for the energy, and I stopped it. The optimiser now runs on the symbolically verified angle-integrated energy (120 iterations). The final profile is evaluated with the full 3D quadrature, and the 3D and radial energies agree to 4 × 10⁻¹⁶. All checks pass: |n| = 1 to 7 × 10⁻¹⁶, φ-independence 9 × 10⁻¹⁷.

New values:

| Quantity | Version 1 | Version 2 |
|---|---|---|
| c₀ʰ (rms / ring) | 589.7 / 340.8 | 566.7 / 340.8 |
| Electron g² = 1/κ₄ (LEP; rms / ring) | 2.07 × 10⁹ / 1.20 × 10⁹ | 1.99 × 10⁹ / 1.20 × 10⁹ |
| √κ₂ (rms) | 84.5 MeV | 82.9 MeV |

E_W and R̃_ring are unchanged.

**Resolved:** yes.

### 3. Hopfion E_W labelled CALIBRATED (minor)

**Diagnosis.** Confirmed by the identity in issue 2: E_W(ansatz) = a₁/(3π²) exactly, so it is not an independent calibration. The "≤ 5% above 1.204" tolerance was self-set. E8's preregistered 2% would not pass (2.3%).

**Action.** Relabelled CONSISTENT (variational upper bound, consistent with 1.204–1.22) in `results.json` and the report. The identity is stated.

**Resolved:** yes.

### 4. Proton M·R/ħc labelled CALIBRATED (minor)

**Diagnosis.**
- 2.8 is a PLAN expectation, not a literature value, and ±0.05 was set by the original agent.
- PLAN's 2.8 equals 939 MeV × 0.59 fm/ħc = 2.807, which is the same definition as our 2.826.
- The classical-mass value c₀/e² = 2.598 is outside the self-set band.

**Action.** Relabelled CONSISTENT and reported both values. Added the note that the data value (3.998) uses the charge radius while the model uses the isoscalar radius.

**Resolved:** yes.

### 5. QED illustration (minor)

**Diagnosis.** "10⁻²³⁴" assumed g² = α. With QED's loop-counting coupling g² = e² = 4πα it is about 10⁻¹⁸.

**Action.** Both are quoted, with F = 3.844: 10⁻²²⁸·⁸ for g² = α and 10⁻¹⁸·² for g² = 4πα. The conclusion is unchanged.

**Resolved:** yes.

### 6. E1e combination; P thresholds (minor)

**Diagnosis.** E1 finished after E7 version 1 ran, so the PLAN-specified combination can now be made.

**Action.** `e7_audit.py` reads `../E1_phi4/e1e_results.json` (sha256 prefix recorded) and uses the smallest producers reproduced at dx = 0.05. These are upper bounds.

| Quantity | N = E/m (preregistered) | N_lin |
|---|---|---|
| g²N_min | ≤ 2.48 | ≤ 3.38 |
| N_min/N_pair | ≤ 1.86 | ≤ 2.53 |
| g² needed for a classical pair from 2 quanta | ≥ 1.24 | ≥ 1.69 |

This reproduces the cross-check's 3.38 and 1.69 with N_lin. The P = 0.1–0.5 thresholds are now labelled "indicative (extrapolated leading exponent)" in the report, `results.json` and the figure.

Caveat: E1 is being reconciled separately, so these are its numbers as read now.

**Resolved:** yes.

### 7. Label, rounding and radius-definition inconsistencies (minor)

**Diagnosis.** Confirmed:
- (a) the E_rot ≤ 0.1 M floor appeared as 2.40 and 2.39 (the value is 2.3947);
- (b) λ_C/R and the vacuum ratios were QUANTIFIED in `results.json` but NO_TARGET in the summary;
- (c) "c₀ ≥ 52 with any pion mass" holds for the baryon rms radius only; with the half-baryon radius c₀ falls to 47.3;
- (d) the floor of 0.757 is for the baryon rms radius; it is 0.627 with the half-baryon radius.

**Action.** Harmonised: 2.39 everywhere, and QUANTIFIED for every gap number. The half-baryon values (47.3, 0.627, 1.98) are stated next to the baryon-rms ones, and there is a `results.json` row for c₀_half_min.

**Resolved:** yes.

### 8. LEP bound qualifier (minor)

**Diagnosis.** Confirmed: Schael et al. 2013 Eq. 3.9 converts a VV contact-interaction scale (positive interference, electromagnetic coupling strength) into r_e < 1.1 × 10⁻¹⁹ m. It is model dependent.

**Action.** Qualifier added in `e7_audit.py` (`LEP_bound_note`), the `results.json` note, the report Method and Findings, and the seed-claim evidence.

**Resolved:** yes.

### 9. Unlisted deviation (minor)

**Diagnosis.** Confirmed: PLAN says to use E2's profile; E7 solved its own. It agrees with E2 to ≤ 10⁻⁹, so the effect is nil.

**Action.** Listed as deviation 9 in the report.

**Resolved:** yes.

### 10. "Any soliton" wording (minor)

**Diagnosis.** Confirmed: M R = c₀/(g²ħ) is a theorem for one-scale families. With extra dimensionless parameters c₀ can move, and only the pion mass and the hopfion were tested.

**Action.** The seed-claim text now reads "theorem for one-scale families; the two-parameter families tested keep c₀ ≥ 47.3; not shown beyond those". The verdict stays CONFIRMED for the PLAN prediction as tested.

**Resolved:** yes.

## Final state

- **Headline changes.**
  - DL F = 4.48 → 3.84 (was 4.45 → 3.93).
  - Hopfion R̃_rms = 2.061 (was 2.144); c₀ʰ = 341–567; g² ≥ 1.2–2.0 × 10⁹.
  - Hopfion E_W and proton M·R are CONSISTENT, not CALIBRATED.
  - New: E1e g²N_min(φ⁴) ≤ 2.48–3.38.
  - QED illustration: 10⁻²²⁹ (g² = α) or 10⁻¹⁸ (g² = 4πα).
- **Unchanged.** Every Skyrme, electron, vacuum and Weinberg–Witten number. The cross-check reproduced these to ≤ 10⁻⁹.
- **Seed-claim verdicts (unchanged).**
  - CONFIRMED: proton classical; electron-like fold needs g² ≫ 1; few-quanta pair folding exponentially rare.
  - AMENDED: electron misses by ≥ 3.5 × 10⁶; "like QCD baryons"; "pairs form readily ⇒ strong coupling"; Weinberg–Witten.
  - QUANTIFIED: vacuum tension.
  - OPEN: §2 one cone (not tested in E7).
- **Consistency.** `results.json` (version 2) carries the headline, the seed_claims and a reconciliation block, and matches REPORT.md. The figures are regenerated: `fig_vacuum_pairs.png` 72 KB, `fig_scale.png` unchanged at 97 KB.
