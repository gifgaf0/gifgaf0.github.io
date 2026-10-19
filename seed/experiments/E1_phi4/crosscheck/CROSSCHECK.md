# E1 cross-check: φ⁴ in 1+1 D

**Verdict: CONFIRMED WITH CORRECTIONS.**

Two independent codes reproduce nearly every number in the report:

- E1a and E1b;
- the E1c map trend;
- every E1d statistic;
- E1e.

The exceptions:

- **One headline calibration does not stand: the DSV example point (ω, v) = (0.99, 0.43).** Its pair call depends on dx and dt, in the original code and in the independent codes.
- **Three seed-level verdicts claim more than the evidence supports.** Details under "Audit findings" below.

## What was recomputed, and how

| Part | Original | Cross-check |
|---|---|---|
| E1a | lattice Newton solve; lattice eigenproblem | scipy `solve_bvp` collocation, mass by quadrature; Chebyshev collocation of −∂² + 3φ_k² − 1; time-domain excitation in the FD6 code |
| E1b | 4th-order FD + leapfrog; x₀ = 12; box (40, 30); dt → 0 extrapolation | Fourier pseudo-spectral + RK4; x₀ = 15; periodic box ±260 with cubic sponge; dx 0.2; dt 0.04 (0.02 check); bisection to 10⁻⁵ |
| E1c | FD4 + leapfrog, dx 0.1, dt 0.04 | (1) FD6 + RK4, dx 0.08, dt 0.032: 6 ω × 26 v, plus 6 points at ω = 0.995. (2) Fourier code with exact linear Klein–Gordon propagation and 4th-order (Yoshida) splitting: dx 0.1 / 0.05, dt 0.02 / 0.01, at ω = 0.99 |
| E1d | FD4 + leapfrog, dx 0.1 | (1) FD6 + RK4 on all 1485 coarse points, two σ = 16 lines, 80 single-packet controls, a 100-point dx self-check. (2) Spectral code on a 90-point random sample (A ≥ 0.3, fixed seed), plus targeted runs: smallest producers in both φ_t forms (own one-way construction), self-folding thresholds |
| E1e | lattice-dispersion N_lin | own initial data, continuum dispersion; scaling N·λ/m² = Ẽ/(2√2) and floor 2/3 re-derived |

**Conventions and sources.**

- Conventions follow PLAN.md E1: V = ¼(φ² − 1)², m = √2, M_kink = 2√2/3.
- Initial data were built from PLAN.md and from DSV eqs. 11–13, read in arXiv:0803.0670v2. DSV Figs. 1–2 were rendered from that PDF.
- The original code was read only after the comparisons. For diagnosis it was then run unmodified, from a scratch copy, at other (dx, dt).

**Provenance of the two codes.**

- Code 1 comes from an earlier, interrupted attempt at this cross-check. It was reviewed, then reused.
- Code 2 is new in this pass. Self-tests: a static pair gives E = 2M_kink to 10⁻¹⁰; energy drift without the sponge is 5 × 10⁻⁸ over t = 100.

## Agreement table

| Quantity | Original | Cross-check | Agree |
|---|---|---|---|
| E1a M_kink | 0.9428090346 | 0.9428090416 (collocation, rel. err. 3e-15) | yes |
| E1a ω_s | 1.2247448677 | 1.2247448717 (Chebyshev); time domain 1.224731 | yes |
| E1b v_c | 0.26006 ± 0.00003 (dt → 0) | 0.260066; dt = 0.02 bracket [0.260060, 0.260066] | yes |
| E1b first window | [0.19256, 0.20343] | [0.192566, 0.203433] | yes |
| E1b windows 2 and 3 | [0.22414, 0.22896], [0.23723, 0.23974] | [0.224035, 0.228855], [0.237129, 0.239644] | yes (10⁻⁴, the original baseline dt bias) |
| E1b T₁₂, windows 1–3 | 17.80, 23.18, 28.52 | 17.80, 23.16, 28.52 | yes |
| E1c example (0.99, 0.43) | pair at T (forms at t = 1160) | no pair to 1.5T: FD6 (dx 0.08); spectral at (0.1, 0.02), (0.05, 0.02), (0.1, 0.01) | **no** |
| E1c (0.99, 0.41) | pair (forms at t = 670) | pair forming at t = 590 at all three spectral settings | yes |
| E1c ω = 0.99 column | producing v = 0.41, 0.43 | FD6: v = 0.40 (step 0.02); spectral: 0.41 yes; 0.42, 0.43, 0.44 no | **no** |
| E1c map, 160 common points | 21 producing | 21 producing (FD6), 14 in common, 91.2% call agreement | yes |
| E1c trend, Spearman(ω, median v) | −0.99 | −0.94 | yes |
| E1c pass-through | 0/10 at v = 0.90; 2/60 at v ≥ 0.85 | 0/18 at v ≥ 0.86 | yes |
| E1c ω > 0.99 | 0/72 | 0/6 | yes |
| E1d coarse grid | 564/1485 producing | 587/1485 producing; point agreement 83.2% (80.1% at E > 2M) | yes; the original's own dx-halving agreement is 79.7% |
| E1d fraction vs E/2M (1.5–2, 2–3, 3–4, 4–6, 6–8, 8–12, 12–24, 24–64, > 64) | .03, .08, .11, .18, .45, .53, .59–.60, .69–.70, .75 | .02, .07, .11, .23, .52, .56, .62–.64, .69–.70, .77 | yes |
| E1d 90-point random sample (spectral, one by one) | 28 producing | 28 producing; 73% point agreement; spectral vs FD6 84% | yes (counts) |
| E1d production below 2M | 0 of 19,526 | 0 (all runs) | yes |
| E1d producers with A ≤ 0.3 | 0 | 0 | yes |
| E1d lowest producer, baseline φ_t (0.8, 2, 0.5) | 1.858 × 2M, collision needed | FD6 1.858; spectral 1.8584, produces at dx 0.1 and 0.05; single packet makes no pair | yes |
| E1d raw 1.79 point (1.4, 1, 0.25) | not reproduced at dx 0.05 | no pair (FD6; spectral dx 0.1 and 0.05) | yes |
| E1d lowest producer, one-way φ_t (0.6, 4, 0.5) | 2.703, produces; (0.8, 2, 0.5) one-way: 2.90, no pair | 2.7030, produces at dx 0.1 and 0.05; (0.8, 2, 0.5) one-way: 2.902, no pair | yes |
| E1d self-folding onset, σ = 16 | min A 0.375 (σ-slice), 0.425 (k-slice) | k = 0.25: first at A = 0.425 (0.40 no); k = 1: first at 0.425 (0.45 and 0.5 no) | yes |
| E1d σ = 16, k = 1 line | 17 switches, onset A 0.375 | 17 switches, onset 0.375; 80% point agreement | yes |
| E1d σ = 16, k = 2 line | 17 switches, onset 0.375 | 9 switches, onset 0.375, same gap at A = 0.45–0.5 | qualitative only |
| E1d single-packet controls | 65% of producers self-fold | FD6 sample 71%; 87% call agreement | yes |
| E1d matched-energy speed ρ | −0.82, −0.87, −0.88 | −0.82, −0.93, −0.92 | yes (but confounded; see M3) |
| E1d matched-energy width ρ | −0.28, −0.28, −0.21 | −0.31, +0.12, +0.41 (all p > 0.2) | yes |
| E1e N·λ/m², Gaussian (0.8, 2, 0.5) | 1.2389 (N = E/m), 1.6879 (N_lin) | 1.2389, 1.6879 | yes |
| E1e N·λ/m², one-way (0.6, 4, 0.5) | 1.80, 1.96 | 1.802, 1.959 | yes |
| E1e N·λ/m², DSV (0.95, 0.62) | 4.7805, 3.9278 | 4.7805, 3.9278 | yes |

## The disagreement: the DSV example point

### Production calls by code and resolution

"Pair from t" is when the pair test starts passing continuously. ± is the pair's half-width at T where recorded. A dash means not run.

| Code | dx | dt | (0.99, 0.43) | (0.99, 0.41) |
|---|---|---|---|---|
| original (FD4 + leapfrog) | 0.1 | 0.04 | pair from t = 1160 (±22.5 at T) | pair from t = 670 |
|  | 0.1 | 0.02 | pair from 780 (±202 at T) | none |
|  | 0.1 | 0.01 | none | pair from 610 |
|  | 0.05 | 0.02 | none | none |
|  | 0.05 | 0.01 | none | none |
|  | 0.05 | 0.005 | none | – |
|  | 0.025 | 0.01 | none | – |
|  | 0.025 | 0.005 | pair from 840 | pair from 590 |
|  | 0.025 | 0.0025 | none | – |
|  | 0.0125 | 0.005 | pair from 840 | – |
| FD6 + RK4 | 0.08 | 0.032 | none (to 1.5T) | – (v = 0.40: pair) |
| spectral, 4th order | 0.1 | 0.02 | none | pair from 590 |
| spectral | 0.05 | 0.02 | none | pair from 590 |
| spectral | 0.1 | 0.01 | none | pair from 590 |

### ω = 0.99 column in the original code

v = 0.38–0.48 in steps of 0.01:

- (dx, dt) = (0.1, 0.04): producers at {0.39, 0.41, 0.43};
- (0.1, 0.02): {0.43};
- (0.05, 0.02): none.

### Diagnosis

**There is no bug.**

- The original's DSV initial data, time derivative, sponge and pair test match independent implementations.
- E/2M at the example is 11.198 in all codes, and map energies agree to 5 × 10⁻⁵.

**Why the call flips.**

- At (0.99, 0.43) the trains leave a central oscillation that lasts about 900 time units.
- Whether that oscillation ends in a pair depends on accumulated phase error. The leapfrog call flips with dt all the way down to 0.0025.
- In the original run that does produce, the pair forms the latest of all 80 producers (t = 1160 against a median of 120). It is ±22.5 wide at T, whereas DSV Fig. 1 shows the kinks at ±140 at T.

**A converged producer exists nearby.** At (0.99, 0.41):

- the spectral code at three (dx, dt) settings forms the pair at t = 590;
- the finest original setting also forms it at t = 590;
- the kinks are well separated at T, as in DSV's figure.

**Conclusion.** DSV's ω = 0.99 production near v ≈ 0.4 is reproduced, but at 0.41, not at the quoted 0.43. The E1 call at 0.43 is a property of the (0.1, 0.04) discretisation.

## Audit findings

### Major

**M1. E1c example row: CALIBRATED is not demonstrated.**

- The point was never resolution-checked.
- The original code produces at 4 of 10 settings; the independent codes produce at 0 of 4.
- "The pair is real: it is still separating at 1.5T" generalises from a single discretisation.
- The dx-check agreement of 74/78 is trivial in the ω = 0.99 column: its producing v values are not on the dx = 0.05 grid, which has no ω = 0.99 producer at all.
- **Fix:** relabel the row as a sensitive point. Report the converged producer at (0.99, 0.41). Resolution-check every map point that carries a verdict.

**M2. Seed §4 DSV claim marked CONFIRMED; "most easily at low speed" is contradicted by the E1c map.**

- At fixed ω there is no production below the velocity band (ω = 0.90: none for v < 0.73).
- The lowest-energy producers are at v = 0.62–0.73 (E/2M ≈ 7).
- **Fix:** AMENDED. Production occurs in an ω-dependent band that moves to lower v as the pulses weaken.

**M3. The E1d low-speed preference is an amplitude confound.**

- At matched energy, slow packets have larger A: mean A is 0.80–0.90 at v_g ≤ 0.47 against 0.36–0.42 at v_g ≥ 0.82 in the [2, 4) band. Production is controlled by A.
- At fixed A there is no significant negative speed trend.
  - Original data: one marginal case, A = 0.5, p = 0.045.
  - FD6 data: the only significant trend is positive (A = 1.2, ρ = +0.75).
  - Collision-needed production: no trend at any A.
- The one-way collision-needed speed test is NOT SUPPORTED in results.json, yet the seed-claim text says "low speed holds" in both φ_t forms. See `xc2_confound.py`.
- **Fix:** report the fixed-A test, and mark the speed prediction NOT SUPPORTED as a speed effect.

**M4. The §2 AMENDED rationale holds only for the scanned families.**

- The φ⁴ equation is time-reversal invariant.
- Reversing a slow (v ≪ v_c) kink–antikink capture, whose bion radiates its energy away, gives radiation-only initial data. In the limit these make a pair with E → 2M; the data are finely tuned.
- So the classical infimum is 2M. The onsets 1.86, 2.70 and 7.2 × 2M are family-specific upper bounds.
- **Fix:** mark the claim CONFIRMED (the floor holds) with a note on generic initial data, or restrict the amendment explicitly to the scanned families.

### Minor

1. CALIBRATED is used for the energy-conservation sanity check, which has no literature target.
2. Slice region, hole and switch counts are quoted as numbers but are not converged (9 vs 17 switches on the k = 2 line). Lead with the robust facts instead: onset A, non-monotonic lines, production fractions.
3. The self-folding mechanism is called "not analysed". A one-line estimate explains its threshold: a trough at φ = −1 − A is above the barrier V(0) = ¼ once A > √2 − 1 = 0.414. This local effect produces 65% of E1d's pairs, which limits what the fraction-vs-energy curves say about collisions.
4. The E1c table simplifies DSV Fig. 2: ω = 0.95 is given as 0.64–0.77, but the figure has gaps. The claim of reproduction "band by band" is loose at point level: at v step 0.02 the original hits 14 of DSV's 22 producing points, with 7 false positives.
5. The v_c offset of 2.6 × 10⁻⁴ is said to have no diagnosis. An independent code with different x₀, box and integrator lands within 10⁻⁵ of the original, so the offset lies in the [summary] target. CALIBRATED stands.

### Checked and found sound

- **Numbers.** Every number in REPORT.md checked against results.json and the detail files matched.
- **Figures.** All six figures referenced exist, each under 300 KB.
- **Literature.** The Manton et al. 2021 window (0.1920–0.2029) was confirmed by reading the paper.
- **E1e algebra.** The scaling algebra is correct.
- **Deviations.** The report discloses its deviations from the plan.

## Claim audit

| Claim | Verdict |
|---|---|
| E1a, E1b calibrations; Manton et al. citation | supported |
| E1c (0.99, 0.43) produces; "the pair is real" | unsupported (sensitive point) |
| E1c reproduces DSV Fig. 2 band by band | overstated |
| E1c dx check 74/78 | overstated (ω = 0.99 column agrees only trivially) |
| E1c trend, pass-through, ω > 0.99 null, hole | supported |
| E1d nothing below 2M; fraction-vs-energy table; A ≤ 0.3 passes through | supported |
| E1d lowest producers 1.86 / 2.70 × 2M | supported |
| E1d self-folding at A ≳ 0.4 | supported |
| E1d ragged boundary | supported (counts not converged) |
| E1d slower produces more | overstated (amplitude confound) |
| E1d no width preference | supported |
| E1e N_min·λ/m² values | supported |
| §2 AMENDED rationale | overstated |
| §4 small packet passes through: CONFIRMED | supported |
| §4 folding controlled by amplitude: AMENDED | supported |
| §4 DSV "most easily at low speed": CONFIRMED | overstated (should be AMENDED) |
| §4 / §7.1 ragged: CONFIRMED | supported |
| §8 QUANTIFIED / OPEN | supported |

## Files

All files are in `crosscheck/`.

**Pipeline**

- `crosscheck.json`
- `run_xc2_all.sh`

**Code 2 and its runs**

- `xc2_spec.py`: the spectral code.
- `xc2_dsv.jsonl`, `xc2_gauss_w0.jsonl`, `xc2_targets.jsonl`: its outputs.

**Comparison and audit**

- `xc2_compare.py`, `xc2_audit.py`, `xc2_audit_text.py`, `xc2_write_json.py`
- `xc2_confound.py` and `xc2_confound.json`: the amplitude-confound analysis.

**Original-code diagnosis**

- `xc2_diag_origcode_*.py`, with their outputs `xc2_origcode_*.json`.

**First-pass inputs**

- Code 1 sources: `xc_core.py`, `xc_e1a.py`, `xc_e1b.py`, `xc_e1c.py`, `xc_e1d.py`, `xc_e1e.py`.
- Their outputs: `xc_*.json` and `xc_*.jsonl`.
