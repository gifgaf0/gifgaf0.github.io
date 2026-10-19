# E5 — Add light: independent cross-check (second pass)

*Second, independent computation and audit of `seed/experiments/E5_add_light/` (PLAN.md §4 E5). The code is in `crosscheck/`.*

**How this pass was done.**
- I read PLAN.md, SEED.md, REPORT.md and results.json first, and opened the original scripts only after my numbers were compared.
- The directory already held a first cross-check pass (shooting solver, Noether currents, π⁰, charges, linearisation). I reviewed that code line by line and reran it: it reproduces its earlier output bit for bit.
- I then added new checks and compared everything against the **current** results.json, which the original has revised since the first pass.
- Reproduce with `crosscheck/run_crosscheck.sh`: 4 min 19 s wall (3 min 20 s CPU) on one shared core, with thread variables set to 1.

## Verdict: **confirmed with corrections**

- **Numbers:** 100 of 100 compared rows agree, most to 1e-9 relative or better. All 14 calibration rows pass in my numbers. There is no numeric disagreement and no blocking issue.
- **Physics verdicts:** the seed verdicts as worded in results.json are supported.
- **Major issue:** REPORT.md and the structured summary were not updated after the original's own reconciliation pass. They contradict results.json on verdict wording and on the check count, and they keep text errors that results.json lists as fixed.
- **Minor issues:** ten more, listed below.

## Methods: original vs cross-check

| Piece | Original | Cross-check |
|---|---|---|
| Hedgehog profile | `solve_bvp` collocation | (a) Two-sided shooting (DOP853), with sympy-generated series at both ends. (b) **New:** finite-element minimisation of the energy functional on a compactified mesh, using damped Newton with the exact tridiagonal Hessian. N = 4000, 8000 and 16000, with Richardson extrapolation at the observed order. |
| EM and axial currents | Closed forms derived in sympy | Noether currents from numerically differentiating the matrix Lagrangian (a 5-point stencil, exact for a quartic), plus the matrix baryon current, on a 3D grid. |
| Isoscalar μ | ⟨r²⟩J/(6λ) | μ/J from the rotating baryon current, with the Noether angular momentum J_z. |
| Isovector μ, g_A | λ/6; (π/3e²)\|D\| | ½∫x×V₃, with ⟨R₃₃⟩ = 1/3 from explicit S³ wavefunctions and the operator sign tied to classical charges. g_A from the axial sphere integral × 3/2, and separately from the surface term 2πC/3e² on the FE profile. |
| π⁰ → γγ | sympy | Plane-wave amplitude and polarisation sum from Bernstein–Holstein eq. 67, plus the textbook A = N_cα/(3πf). **New:** the same WZ coefficient (−N_c/48π²), integrated over the hedgehog, gives charge **0.16666667 per unit N_c** (isovector part 1e-19), i.e. B/2 at N_c = 3. |
| Charges | Branching rule and weight peeling | Gelfand–Tsetlin patterns. **New:** anomaly-consistent charges for N_c = 1…9. |
| One cone, vacuum | sympy | Own sympy linearisation and Euler–Lagrange equations; T_μν with a general metric. |
| PDG inputs | `pdg` package | **New:** independent `pdg` query; data-side radii, tally and Γ_PDG recomputed. |

## Agreement (ANW parameters F_π = 129 MeV, e = 5.45, unless stated)

| Quantity | Original | Cross-check | Target (tol) | Agree |
|---|---|---|---|---|
| r_{I=0} | 0.5939287 fm | 0.5939287 (Noether), 0.5939287 (FE) | 0.59 (±0.01) | yes |
| r_M^{I=0}, ANW def.; Sachs | 0.9223268; 0.7144313 fm | 0.9223268; 0.7144313 fm | 0.92 (±0.01) | yes |
| μ_p / μ_n / ratio | 1.877637 / −1.323047 / −1.419176 | identical (both methods) | 1.87 / −1.31 / −1.43 (±0.02) | yes |
| g_A | 0.609127 | 0.609127 (sphere × 3/2), 0.609127 (2πC/3e², FE) | 0.61 (±0.01) | yes |
| g_πNN (Goldberger–Treiman) | 8.867756 | 8.867756 | 8.9 (±0.05, post hoc) | yes |
| Γ(π⁰→γγ), N_c = 3, f = 92.21 MeV | 7.761089 eV | 7.761089 eV (two derivations) | PrimEx-II 7.802 ± 0.117 | yes (−0.350σ; +0.332σ vs PDG 7.7202 ± 0.1232) |
| Γ, N_c = 1 | 0.862343 eV | 0.862343 eV | excluded | yes (−59.3σ) |
| Γ at f = 64.5 MeV; at the SU(3)-refit f | 15.862 eV; 20.3985 eV (f = 56.8774) | 15.862 eV; 20.3988 eV (f = 56.8770) | ≈ 15.9, ≈ 20 | yes |
| f needed for PrimEx-II | 91.968 MeV | 91.968 MeV | — | yes |
| isovector ⟨r²⟩(R), R = 2…200 (x units) | 0.5517 … 290.828; slope 1.463846 | identical (shooting and FE) | diverges | yes (0.411 fm × R) |
| enclosed Q_p, Q_n (24 entries); charge outside R (6 entries) | e.g. 0.76354, 0.18480 at 1 fm | identical to < 1e-10 | — | yes |
| neutron Q_n maximum | +0.20571 at 0.7255 fm | +0.20571 at 0.7255 fm | — | yes |
| own SU(2) refit | 129.263 MeV, 5.4440 | 129.2627, 5.44399 | — | yes |
| massive refit; r_p, ⟨r²⟩_n, r_{I=1} | 108.2598 MeV, 4.84205; 0.88013, −0.30787, 1.04044 | identical | none | yes |
| massive μ_p, μ_n, g_A | 1.97199, −1.24097, 0.64914 | identical | none | yes |
| M/(3π²), Λ, C, F′(0), ⟨x²⟩_B, ⟨x⁴⟩_B | 1.2314457, 50.978739, 8.638578, −1.0037641, 4.477836, 48.35455 | identical from shooting **and** FE minimisation | E2 | yes |
| Ĩ₂ (SU(3)); D = −2C | 40.678582; G = 2πC/3 | 40.678582; G₃₃ = 18.0925958 (2πC/3 to 1.3e-9) | — | yes |
| charges of 8, 10, 10̄, 27; SU(2); N_c table | integers; {0,1} with consistent charges | identical | exact | yes |
| one cone; taut vacuum | ω² = k² + m², ω = \|k\|; T = V₀g | identical (Maxwell rank 3 off the cone, 1 on it) | by construction | yes |
| PDG r_E^{I=0}, r_M^{I=0}; within 30% / 33% | 0.76902, 0.82174 fm; 3/7, 6/7 | identical | — | yes |

**My convergence checks.**
- **Shooting** (X = 25/40/80, x_m = 2.5/1.5/1.0, two x₀, two rtol): F′(0) agrees to 1e-9 and C to 7e-8 for X ≥ 40.
- **Grids:** X = 400 with 8×10 angles and X = 200 with 6×8 angles agree to ≤ 3e-8.
- **Virial and baryon number:** virial 1e-13; B = 1 − 1e-12.
- **FE:** Richardson spreads are 2e-13 in M, 1.7e-6 in Λ, 1e-9 in ⟨x²⟩ and 9e-8 in C. Λ and F′(0) converge at first order on this mesh and the others at second order; each is extrapolated at its own order.
- **Axial sphere integral:** converges with the cutoff (18.09257 at R = 50, 18.0925958 at R = 200).

## Issues

**Major**

1. **REPORT.md and the summary are out of date relative to the original's own results.json.**
   - results.json carries a `reconciliation` block listing 8 changes made after the first cross-check pass, and its seed verdicts are generated by `make_results.py`. The REPORT was not updated to match.
   - The REPORT (string-checked in `cc_audit.py`) still has:
     - 38/38, four times (log and results.json: 39/39, all computed; 10d now computed, 9g added);
     - CALIBRATED for the internal checks (results.json: CHECK PASSED);
     - QUANTIFIED for the f_π tension (results.json: no SEED verdict);
     - "3 of 7 within 30%" for SEED 6B (results.json: 6 of 7 within 33%, amendment carried by g_A and the radii);
     - a plain CONFIRMED for Commitment 4 (results.json: "in the preregistered operational sense only");
     - the π⁰-coupling typo and the X = 25 convergence overstatement, both of which results.json lists as corrected.
   - Two deliverables of one experiment therefore disagree on seed-verdict wording. **Fix:** regenerate the REPORT and summary from results.json, applying every item in `reconciliation.changes`.

**Minor**

2. **π⁰ coupling typo (Method).** "(N_c e²/48π²f) ε ∂_μA_ν A_α ∂_βπ⁰" is a factor 2 too small. With ∂_μA_ν the coefficient is 24π²; 48π² goes with F_μν. The amplitude N_c e²/(12π²f) and all numbers are correct.
3. **Convergence wording.** The REPORT claims "X = 25…400 agree to 5×10⁻⁸ in Λ". X = 25 is off by 7.2e-7 (C by 1.2e-6); the 5e-8 figure holds for X = 100–400.
4. **Check count and runtime.** The REPORT says 38/38 and 150–170 s (2 min 59 s in total); the log shows 39 checks in 302.6 s.
5. **Verdict vocabulary.** CALIBRATED is used for checks with no literature target. QUANTIFIED is used for a paraphrased SEED 6B claim, although PLAN reserves it for §8 gaps; SEED 6B only says that F sets the units and e is the only pure number.
6. **The f_π "tension" is not independent.** Γ ∝ 1/f², so the 2.03× excess is (92/64.5)²: ANW's f_π is 30% low (38% low for the SU(3) refit). That 30% miss belongs in the 6B tally; the width only squares it.
7. **SEED 6B framing.** "3 of 7 within 30%" counts μ_p (−33%), μ_n (−31%) and g_πNN (−32%) as misses of "roughly 30%". AMENDED is earned by g_A (−52%) and by r_p and ⟨r²⟩_n, which are infinite with massless pions. My recomputed tally is 3/7 within 30% and 6/7 within 33%.
8. **Commitment 4.** The preregistered prediction holds: the slope is 0.411 fm × R, and the radius becomes finite with m_π. But the test cannot distinguish "dressing" from any extended charge distribution, and "not slowed" holds by construction. The verdict needs the qualifier that results.json already has.
9. **Neutron peak in the summary.** "+0.185 at 1 fm" is a table grid point. The maximum is +0.2057 at 0.7255 fm.
10. **g_πNN tolerance.** It passes only under the post hoc ±0.05 and fails ±0.02 (|Δ| = 0.032). This is disclosed, and acceptable because g_A passes its preregistered tolerance.
11. **Unverified attribution.** "ANW's own table (via Rakhimov) already excepted g_A" was not read in any source.

## Claim audit

| Claim (original verdict) | Cross-check |
|---|---|
| §7.4 integer charges from a gauged U(1) (CONFIRMED) | **Supported.** The charge matrix is an input. Integrality follows from the WZ constraint, which selects triality-zero irreps. The new check ties the B/2 charge and π⁰→γγ to one WZ coefficient. |
| §7.4/§2 one cone (CONFIRMED, by construction) | **Supported**, correctly labelled. |
| Commitment 1, taut vacuum (CONFIRMED, by construction) | **Supported.** V₀ is an arbitrary added constant. |
| Commitment 4, dressed not slowed (REPORT: CONFIRMED) | **Overstated** in the REPORT. The qualified verdict in results.json is supported. |
| §6B within roughly 30% (AMENDED) | **Supported.** The framing is overstated (issue 7) and f_π is missing from the tally. |
| §6B one parameter set, anomaly included (REPORT: QUANTIFIED) | Numbers supported; verdict **overstated or wrong word** (issues 5 and 6). The PLAN prediction is confirmed. |
| WZ gives π⁰→γγ; N_c = 1 excluded (CONFIRMED with caveat) | **Supported.** Bär–Wiese hep-ph/0105258, read this pass, states the caveat exactly. Anomaly-consistent nucleon charges {0,1} for N_c = 1…9 reproduce. |

## Step 4: reading the original code

There was no numeric disagreement to diagnose. In the code I verified that:
- the reconciliation recorded in results.json is real: 10d is now a computed expansion of the gauged WZ term, 9g was added, and 5c and 7b test the exact value and sign;
- results.json is generated by `make_results.py`, with the qualified verdicts.

The stale text sits only in REPORT.md and the summary.

**Other checks:**
- **Citations**, all read in the arXiv mirror:
  - Bernstein–Holstein eqs. 67–71 and the 8.10 eV higher-order value. Their eq. 69 second line is a factor 2 off for F̃ = ½εF, as the original notes.
  - hep-ph/0605305 eq. 24: ρ_M ∝ r²F′sin²F, which is the ANW magnetic-radius definition.
  - Ma–Harada eqs. 4.116 and 4.121, with twice our normalisation.
  - Bär–Wiese abstract and §1.
- **Figures:** `fig_charge_densities.png` (88 KB) and `fig_vs_pdg.png` (46 KB) exist and show the stated content.
- **Massive variant:** its outputs (μ_p 1.97, μ_n −1.24, g_A 0.65, r_{I=0} 0.68 fm, r_{I=1} 1.04 fm) match AN84's published values as I remember them. I did not read AN84, so this is not a sourced check.

## Files (`seed/experiments/E5_add_light/crosscheck/`)

- **Code, pass 1, reviewed and rerun:** `cc_lib.py`, `cc_profile.py`, `cc_hedgehog.py`, `cc_pi0.py`, `cc_charges.py`, `cc_linear.py`, `cc_extra.py`.
- **Code, new in this pass:** `cc_new.py` (FE solver, WZ charge, N_c charges, PDG, textbook width), `cc_compare.py` (rewritten, 100 rows), `cc_audit.py` (text audit, issues, claim audit), and `run_crosscheck.sh`.
- **Outputs:** `cc_*_log.txt` and `cc_*.json`, `crosscheck_numbers.json`, `crosscheck.json`, `full_run.log`.
- **First-pass records:** `prev_attempt/` (`crosscheck_pass1.json`, `crosscheck_numbers_pass1.json`, and its compare and run scripts).
