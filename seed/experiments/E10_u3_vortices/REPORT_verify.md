# E10 / Route B, Amendment A: verification of the λ = 1 WINDOW (V1a, V1b, V1c, V2) and robustness (V3a, V3b): report

*November 4, 2026. **Label: Exploration, post-hoc verification.** Run under `PREREG_B2B3.md` §6 (Amendment A, committed at d0a8a78 before any verification run). Scope: exactly §A.3 (V1a, V1b, V1c, V2) and §A.5 (V3a, V3b). No B4 was run and no loop was built. `PREREG_B2B3.md`, `REPORT_B2B3.md`, `prior_address_routeB.md`, `NOTE_route_B.md`, `README.md`, the existing scripts and all E9 files are unmodified.*

**Units.** Model units only (PREREG §1): energies per unit length in v², lengths in 1/(gv). q is the SU(3)_{C+F} charge per unit length under G = diag(0, 1, 0). It is not electric charge. No particle identification is made.

## Summary

| | Result |
|---|---|
| **A.4 verdict** | **CONFIRMED.** All three conditions hold. |
| A.4 (1), V1b (r_max 40, dr 0.05) | **Holds.** All 14 central sign changes persist with central differences at both bracketing points. All have d²E/dR² > 0 by direct solve (f″(1) = 6.92–7.14), leak ≤ 5 × 10⁻¹¹, ω/m = 0.968–0.984 at the bracketing points. |
| A.4 (2), V1c (r_max 60, dr 0.05) | **Holds.** Selected sign change: #66, (0.25, 24.8)–(0.30, 24.8), the most negative V1b bracket 𝒯 (−0.1654). It persists. 𝒯 changes by 5.8 × 10⁻⁶ and 2.3 × 10⁻⁵, against \|𝒯\| = 0.491 and 0.165. |
| A.4 (3), V2 (2D, half-width 30, h = 0.125) | **Holds.** ℰ agrees with V1b to −3.9 × 10⁻⁶ and −4.0 × 10⁻⁶ (tolerance 10⁻³). The 2D 𝒯 (envelope value; deviation 5) is +0.489 / −0.168, the same signs as V1b (+0.491 / −0.165). |
| A-P1 (CONFIRMED, ~40 %) | **Holds.** |
| A-P2 (r_q, I_q change < 5 % from r_max 20 → 40 at the 14 central sign changes, ~70 %) | **Holds.** Over their 27 bracketing points: r_q +3.2 to +4.4 × 10⁻⁴ (V1a), +3.9 to +4.9 × 10⁻⁴ (V1b); I_q +3 to +7 × 10⁻⁶ (V1a), −3 to +3 × 10⁻⁶ (V1b). |
| A-P3 (V3a: BPS-only, ~50 %) | **Fails.** V3a is **one-sided**: 76 stable sign changes at λ = 0.9, none at λ = 1.1. |
| A.6 consequence | **CONFIRMED:** a B4 pre-registration is written before any loop code. It fixes in advance the selection rule among confirmed sign changes, n from A.1 and the passenger control. The V3 classification (one-sided) goes into B4's caveats. *Not done here (out of scope).* |
| n, R_eq, Q (A.1) of the 14 confirmed (V1b) | **n = 3 for all 14.** R_eq = n/k* = 10.00–10.44, R_eq/r_q = 3.01–3.06, Q = 2πR_eq q* = 1478–1627, d²E/dR² = 2πf″(1)/R_eq = +4.16 to +4.49. |
| V3 | **Descriptive only. V3 does not feed A.4 or any selection.** λ = 0.9: 95 sign changes, 76 stable (all with one-sided k differences). λ = 1.1: none (min 𝒯/ℰ = +0.11). λ = 0.8, q = 30–60: 259 sign changes, 227 stable, 122 of them central. |

**Read before the summary.**
- **Box and resolution are not the issue.** Going from r_max 20 to 40 to 60, and from dr 0.1 to 0.05, ℰ moves by ≤ 1.4 × 10⁻⁶ (relative) and 𝒯 by ≤ 10⁻⁴ at every central bracketing point. Moving the edge to 40 cuts the original edge-band charge fraction from ~4.5 × 10⁻⁵ to ~10⁻¹¹. The charge is not delocalising: r_q grows by < 0.08 % and I_q by < 10⁻⁵.
- **The window is still at threshold.** ω*/m = 0.981–0.982 for the 14 confirmed sign changes. R_eq/r_q is only 3.01–3.06 at n = 3, which sits on the A.1 boundary by construction.
- **2D agreement is much closer here than at the §2.4 point of REPORT_B2B3** (4 × 10⁻⁶ against 3 × 10⁻⁴). Only one 2D spacing was run, so there is no Richardson extrapolation at the window. This is recorded, not explained (§4).
- **The edge sign changes are less clean than the central ones.** At the one-sided-k bracket points of #17, #59 and #109 (k = 0.45), the finite-difference 𝒯 and the envelope value T − (k² + ω²)I disagree by ~0.14. The envelope is negative at both bracketing points of #17. At the central points the two agree to ≤ 0.0026. Edge sign changes do not enter A.4.
- **This is a straight-string result only.** No loop exists or was computed.

## 1. Commands run

```
cd seed/experiments/E10_u3_vortices
pip install scipy                                       # deviation 1
python3 verify_orig.py > log_verify_orig.txt            # regenerate the original lam=1 solutions (465 points)
nice -n 19 python3 verify_v3.py run > log_verify_v3_run.txt     # V3a/V3b scans (low priority, in parallel)
./verify_chain.sh                                       # V1a, V1b solve + analyse, then V1c and V2
#   python3 verify_v1.py solve V1a / analyse V1a        -> verify_V1a.json, log_verify_V1a.txt
#   python3 verify_v1.py solve V1b / analyse V1b        -> verify_V1b.json (incl. V1c selection), log_verify_V1b.txt
#   python3 verify_v1.py solve V1c / analyse V1c        -> verify_V1c.json, log_verify_V1c.txt
#   python3 verify_v2.py solve / analyse                -> verify_V2.json, log_verify_V2.txt
V2_FINALIZE=1 python3 verify_v2.py solve; python3 verify_v2.py analyse   # V2 stopped by hand (deviation 6)
python3 verify_v3.py analyse > log_verify_V3.txt        # V3 sign changes and R-ray direct solves -> verify_V3.json
python3 verify_tables.py > log_verify_tables.txt        # read-only tables and the A.4 rule -> verify_results.json
```

After the container restart, V2 was resumed from its checkpoints and V3 from its per-point files (deviation 7).

## 2. Instrument, software, checks

- **Software:** Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (the same versions as `b3_results.json` meta). 4 cores, single-threaded BLAS.
- **Instrument (unchanged).** The radial functional is `u3radial.Radial`. Per-point solves use `b3_scan.solve_point` (L-BFGS-B, gtol 10⁻⁹, ftol 10⁻¹², maxcor 20, maxiter 20 000). Also unchanged:
  - the window test `b3_scan.in_window` (ω < m_bulk and leak < 1 %);
  - the 𝒯 stencil `b3_scan.tcal`;
  - the R-ray direct solve of `b3_scan.analyse`: f(u) = u·ℰ(k*/u, q*/u) at u = 0.97, 1, 1.03, warm-started from the nearest solved grid point of the same run.
  - The 2D instrument is `u3lattice.Lattice2D` (`make_fg`, `OPTS2D`).
- **No existing script was modified or copied.** The new drivers only import the existing modules, so no diff is needed:
  - `verify_common.py`: point-set selection, padding, per-point storage;
  - `verify_orig.py`, `verify_v1.py`, `verify_v2.py`, `verify_v3.py`, `verify_tables.py`, `verify_chain.sh`.
- **Leak band** = r > r_max − 4 for the radial runs (`Radial.observables` uses the grid's own r_max), and box-edge distance < 4 in 2D.
- **Regenerating the originals (check).** The B3 per-point fields were not kept (REPORT_B2B3 §6 dev. 7). I replayed the recorded warm-start chain at dr 0.1, r_max 20: row k = 0 from the abelian-Higgs initial up to q = 29.2, then each needed (k, q) from (k − 0.05, q). `verify_orig.py` asserts that `warm_from` in `b3_results.json` is that chain for every needed point. **All 465 regenerated ℰ are bit-identical to `b3_results.json`.** The λ = 0.8 q = 30 starting points for V3b were handled as follows: k ≤ 0.10 from `b3_raw_run1_lam0.8.npz`; k = 0.15–0.25 regenerated, also bit-identical.
- **Warm starts.** Every V1 point starts from its original solution, padded as follows:
  - linear interpolation in r for r ≤ 20;
  - vacuum (h = 1, a = 0) beyond 20;
  - α kept;
  - h(r_max) = 1 is the Dirichlet edge of the new grid.
  - V2: the same padding to r = 45 (> 30√2), mapped onto the lattice by `from_radial` with V = rot12(α).
  - Check: at (0, 5.0) the padded V1a start has the original energy to 10⁻¹⁵.
- **Convergence.** Every V1 solve converged (0 failures). All ended on `RELATIVE REDUCTION OF F <= FACTR*EPSMCH`, at max|∇| ≤ 6.2 × 10⁻⁴ (V1a), 1.8 × 10⁻³ (V1b), 9.8 × 10⁻⁴ (V1c). The original scan stopped the same way, at a median max|∇| of 3 × 10⁻⁴ (max 7.7 × 10⁻⁴) for in-window points with q > 20. V1b's largest value is about 2.4 × the original's largest (deviation 9). V3: 0 non-converged solves.

## 3. Point set S (selected programmatically from `b3_results.json`, `lambdas[1].summary.sign_changes`)

The 14 sign changes with empty flags (central in both directions at both bracketing points); the lowest-ω* stable one; the three with the largest k*. Union of bracketing points and their in-window 𝒯-stencil neighbours: **75 grid points**.

| # | role | bracket (k, q) | k* | q* | ω*/m | flags (original) | f″(1) direct (original) |
|---|---|---|---|---|---|---|---|
| 2 | central | (0.25, 23.7)–(0.30, 23.7) | 0.2982 | 23.700 | 0.9818 | central | 7.111 |
| 11 | central | (0.25, 24.1)–(0.30, 24.1) | 0.2941 | 24.100 | 0.9814 | central | 7.037 |
| 34 | central | (0.25, 24.0)–(0.30, 24.0) | 0.2951 | 24.000 | 0.9815 | central | 7.055 |
| 48 | central | (0.25, 23.8)–(0.30, 23.8) | 0.2971 | 23.800 | 0.9817 | central | 7.092 |
| 60 | central | (0.25, 23.9)–(0.30, 23.9) | 0.2961 | 23.900 | 0.9816 | central | 7.073 |
| 61 | central | (0.25, 24.4)–(0.30, 24.4) | 0.2912 | 24.400 | 0.9812 | central | 6.984 |
| 63 | central | (0.25, 24.3)–(0.30, 24.3) | 0.2921 | 24.300 | 0.9812 | central | 7.001 |
| 66 | central | (0.25, 24.8)–(0.30, 24.8) | 0.2874 | 24.800 | 0.9808 | central | 6.916 |
| 70 | central | (0.25, 24.5)–(0.30, 24.5) | 0.2902 | 24.500 | 0.9811 | central | 6.966 |
| 73 | central | (0.25, 24.6)–(0.30, 24.6) | 0.2893 | 24.600 | 0.9810 | central | 6.949 |
| 85 | central | (0.30, 23.5)–(0.30, 23.6) | 0.3000 | 23.526 | 0.9820 | central | 7.144 |
| 93 | central | (0.25, 24.2)–(0.30, 24.2) | 0.2931 | 24.200 | 0.9813 | central | 7.019 |
| 103 | central | (0.25, 24.7)–(0.30, 24.7) | 0.2883 | 24.700 | 0.9809 | central | 6.933 |
| 107 | central | (0.25, 23.6)–(0.30, 23.6) | 0.2992 | 23.600 | 0.9819 | central | 7.130 |
| 20 | edge: lowest ω* stable | (0.25, 29.1)–(0.30, 29.1) | 0.2576 | 29.100 | 0.9779 | one-sided k | 6.448 |
| 17 | edge: largest k* | (0.45, 14.8)–(0.45, 14.9) | 0.4500 | 14.884 | 0.9988 | one-sided k | 9.574 |
| 59 | edge: largest k* | (0.40, 14.9)–(0.45, 14.9) | 0.4494 | 14.900 | 0.9988 | one-sided k | 9.564 |
| 109 | edge: largest k* | (0.40, 15.0)–(0.45, 15.0) | 0.4466 | 15.000 | 0.9985 | one-sided k, one-sided q | 9.524 |

## 4. V1a / V1b / V1c / V2 against the originals

### 4.1 𝒯 at the bracketing points, d²E/dR² and A.1 quantities

𝒯 is from finite differences (`b3_scan.tcal`), given as "first point / second point". f″(1) = R_eq·(d²E/dR²)/2π, by direct solve. The A.1 columns are from V1b. r_q at the sign change is linearly interpolated between the bracketing points.

| # | 𝒯 orig (r_max 20, dr 0.1) | 𝒯 V1a (40, 0.1) | 𝒯 V1b (40, 0.05) | 𝒯 V1c (60, 0.05) | f″ V1a | f″ V1b | f″ V1c | k* | q* | ω*/m | n | R_eq | R_eq/r_q | Q |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | +0.60399 / −0.02296 | +0.60405 / −0.02290 | +0.60396 / −0.02300 | — | 7.111 | 7.110 | — | 0.2982 | 23.700 | 0.9818 | 3 | 10.06 | 3.02 | 1498 |
| 11 | +0.56236 / −0.07527 | +0.56243 / −0.07521 | +0.56234 / −0.07530 | — | 7.037 | 7.036 | — | 0.2941 | 24.100 | 0.9814 | 3 | 10.20 | 3.04 | 1545 |
| 34 | +0.57271 / −0.06225 | +0.57278 / −0.06219 | +0.57269 / −0.06226 | — | 7.055 | 7.054 | — | 0.2951 | 24.000 | 0.9815 | 3 | 10.17 | 3.03 | 1533 |
| 48 | +0.59352 / −0.03610 | +0.59359 / −0.03604 | +0.59349 / −0.03615 | — | 7.092 | 7.091 | — | 0.2971 | 23.800 | 0.9817 | 3 | 10.10 | 3.03 | 1510 |
| 60 | +0.58310 / −0.04919 | +0.58316 / −0.04913 | +0.58307 / −0.04922 | — | 7.073 | 7.073 | — | 0.2961 | 23.900 | 0.9816 | 3 | 10.13 | 3.03 | 1521 |
| 61 | +0.53154 / −0.11410 | +0.53162 / −0.11404 | +0.53153 / −0.11412 | — | 6.984 | 6.983 | — | 0.2912 | 24.400 | 0.9812 | 3 | 10.30 | 3.05 | 1580 |
| 63 | +0.54178 / −0.10120 | +0.54185 / −0.10113 | +0.54176 / −0.10123 | — | 7.001 | 7.000 | — | 0.2921 | 24.300 | 0.9812 | 3 | 10.27 | 3.04 | 1568 |
| **66** | +0.49097 / −0.16536 | +0.49105 / −0.16529 | +0.49099 / −0.16538 | **+0.49098 / −0.16535** | 6.916 | 6.915 | 6.916 | 0.2874 | 24.800 | 0.9808 | 3 | 10.44 | 3.06 | 1627 |
| 70 | +0.52135 / −0.12697 | +0.52142 / −0.12691 | +0.52134 / −0.12699 | — | 6.966 | 6.966 | — | 0.2902 | 24.500 | 0.9811 | 3 | 10.34 | 3.05 | 1591 |
| 73 | +0.51119 / −0.13981 | +0.51126 / −0.13974 | +0.51117 / −0.13982 | — | 6.949 | 6.949 | — | 0.2893 | 24.600 | 0.9810 | 3 | 10.37 | 3.05 | 1603 |
| 85 | +0.00343 / −0.00978 | +0.00349 / −0.00973 | +0.00339 / −0.00982 | — | 7.144 | 7.143 | — | 0.3000 | 23.526 | 0.9820 | 3 | 10.00 | 3.01 | 1478 |
| 93 | +0.55205 / −0.08825 | +0.55212 / −0.08819 | +0.55203 / −0.08828 | — | 7.019 | 7.018 | — | 0.2931 | 24.200 | 0.9813 | 3 | 10.24 | 3.04 | 1556 |
| 103 | +0.50106 / −0.15261 | +0.50113 / −0.15253 | +0.50106 / −0.15261 | — | 6.933 | 6.932 | — | 0.2883 | 24.700 | 0.9809 | 3 | 10.40 | 3.06 | 1615 |
| 107 | +0.61449 / −0.00978 | +0.61455 / −0.00973 | +0.61446 / −0.00982 | — | 7.130 | 7.129 | — | 0.2992 | 23.600 | 0.9819 | 3 | 10.03 | 3.02 | 1487 |
| 20 (edge) | +0.08691 / −0.48385 | +0.08705 / −0.48373 | +0.08702 / −0.48375 | — | 6.448 | 6.448 | — | 0.2576 | 29.100 | 0.9779 | 3 | 11.64 | 3.16 | 2129 |
| 17 (edge) | +0.02430 / −0.00466 | +0.02431 / −0.00466 | +0.02392 / −0.00504 | — | 9.574 | 9.573 | — | 0.4500 | 14.883 | 0.9989 | 4 | 8.89 | 3.53 | 831 |
| 59 (edge) | +0.40707 / −0.00466 | +0.40707 / −0.00466 | +0.40670 / −0.00504 | — | 9.564 | 9.562 | — | 0.4494 | 14.900 | 0.9988 | 4 | 8.90 | 3.53 | 833 |
| 109 (edge) | +0.38115 / −0.02764 | +0.38115 / −0.02764 | +0.38079 / −0.02802 | — | 9.524 | 9.522 | — | 0.4466 | 15.000 | 0.9985 | 4 | 8.96 | 3.54 | 844 |

- **All 18 sign changes persist in V1a and V1b.** All direct-solve f″(1) values are positive and unchanged from the originals to ≤ 2 × 10⁻³.
- The 14 central sign changes keep central differences in both directions at both bracketing points: every stencil neighbour stays in the window. The 4 edge ones keep their original one-sided stencils.
- For the edge sign changes #17, #59 and #109, the u = 0.97 ray point (k*/0.97 ≈ 0.46) lies outside the window, in V1a and V1b, and at the same (k, q) in the original. `b3_scan.analyse` does not test the ray points against the window, and neither does this run (deviation 10).

### 4.2 Per-point observables at the bracketing points of sign change #66 (and the edge ones, V1b)

The full per-point tables for all bracketing points of all 18 sign changes, in all three runs, are in `log_verify_tables.txt`. All 75 points of every run are in `verify_results.json`. Columns: relative changes are against the original (dr 0.1, r_max 20). α = π/4 to 10⁻¹⁰ everywhere.

| run | (k, q) | ℰ | ℰ/ℰ_orig − 1 | T | I_q | I_q/I_orig − 1 | ω/m | leak | r_q | 𝒯 (FD) | 𝒯 (envelope) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| orig | (0.25, 24.8) | 26.159077 | — | 13.32407 | 12.774367 | — | 0.97069 | 4.5 × 10⁻⁵ | 3.42537 | +0.49097 | — |
| V1a | (0.25, 24.8) | 26.159059 | −7.1 × 10⁻⁷ | 13.32411 | 12.774423 | +4.4 × 10⁻⁶ | 0.97069 | 3.3 × 10⁻¹¹ | 3.42686 | +0.49105 | +0.48915 |
| V1b | (0.25, 24.8) | 26.159063 | −5.3 × 10⁻⁷ | 13.32407 | 12.774375 | +6.4 × 10⁻⁷ | 0.97069 | 3.4 × 10⁻¹¹ | 3.42706 | +0.49099 | +0.48907 |
| V1c | (0.25, 24.8) | 26.159063 | −5.2 × 10⁻⁷ | 13.32408 | 12.774387 | +1.6 × 10⁻⁶ | 0.97069 | 3.5 × 10⁻¹⁴ | 3.42709 | +0.49098 | +0.48910 |
| **V2 (2D)** | (0.25, 24.8) | **26.158960** | −4.5 × 10⁻⁶ (**−3.9 × 10⁻⁶ vs V1b**) | 13.32384 | 12.774235 | −1.0 × 10⁻⁵ | 0.97070 | 1.7 × 10⁻⁸ | 3.42716 | — | **+0.48872** |
| orig | (0.30, 24.8) | 26.507946 | — | 13.17002 | 12.599146 | — | 0.98419 | 4.3 × 10⁻⁵ | 3.40197 | −0.16536 | — |
| V1a | (0.30, 24.8) | 26.507929 | −6.5 × 10⁻⁷ | 13.17004 | 12.599189 | +3.5 × 10⁻⁶ | 0.98419 | 3.8 × 10⁻¹¹ | 3.40333 | −0.16529 | −0.16785 |
| V1b | (0.30, 24.8) | 26.507932 | −5.2 × 10⁻⁷ | 13.17001 | 12.599144 | −1.5 × 10⁻⁷ | 0.98419 | 3.1 × 10⁻¹¹ | 3.40354 | −0.16538 | −0.16792 |
| V1c | (0.30, 24.8) | 26.507932 | −5.1 × 10⁻⁷ | 13.17001 | 12.599145 | −8.7 × 10⁻⁸ | 0.98419 | 3.1 × 10⁻¹³ | 3.40360 | −0.16535 | −0.16792 |
| **V2 (2D)** | (0.30, 24.8) | **26.507825** | −4.6 × 10⁻⁶ (**−4.0 × 10⁻⁶ vs V1b**) | 13.16978 | 12.599006 | −1.1 × 10⁻⁵ | 0.98420 | 1.6 × 10⁻⁸ | 3.40367 | — | **−0.16827** |

V2 details:
- lattice L = 480, h = 0.125, half-width 30, α fixed at V1b's value (π/4);
- about 220 L-BFGS-B iterations at each point, interrupted once by the container restart;
- final max|∇| = 3.5 × 10⁻⁶ and 3.3 × 10⁻⁶ (the original 2D comparison ended at 2.0 × 10⁻⁶);
- ℰ moved by ≤ 1.4 × 10⁻⁸ relative over the last ~100 iterations;
- the 90° symmetry holds to max|det H − rot90| = 1.0–1.3 × 10⁻¹⁴, so the 2D minimum stayed equivariant;
- the 2D leak (edge distance < 4) is 1.6–1.7 × 10⁻⁸.

The 2D–radial gap here (4 × 10⁻⁶) is about 80 × smaller than at the B3 §2.4 validation point (k, q) = (0.2, 3.0), where the gap at h = 0.125 was 3.1 × 10⁻⁴. At that point the 2D values sat below the radial ones and moved by +2.7 × 10⁻⁴ under Richardson extrapolation. This is consistent with a fatter, smoother core (core radius 2.84–2.86 at these two points, against 1.47 for the static string) making the O(h²) error smaller. A single 2D spacing does not establish this, so it is recorded, not explained.

**Edge points, FD against envelope 𝒯 (V1b).** At the central bracketing points, FD 𝒯 and the envelope value T − (k² + ω²)I_q agree to ≤ 0.0026. At the edge brackets with one-sided k differences they do not:
- (0.30, 29.1): −0.484 (FD) against −0.688 (envelope);
- (0.45, 14.8): +0.024 against −0.116;
- (0.45, 14.9): −0.005 against −0.146;
- (0.45, 15.0): −0.028 against −0.175.

The envelope 𝒯 is negative at both bracketing points of #17, so by the envelope there is no sign change there. The original report found the same FD/envelope mismatch pattern, which the one-sided stencil explains. It does not affect A.4, which uses central sign changes only.

### 4.3 Box and resolution trends (A.4 descriptive item)

Bracketing points of the 14 central sign changes (27 distinct points), relative to the original (r_max 20, dr 0.1):

| run | ΔI_q/I_q | Δr_q/r_q | Δℰ/ℰ |
|---|---|---|---|
| V1a (r_max 40, dr 0.1) | +3.1 to +6.8 × 10⁻⁶ | +3.2 to +4.4 × 10⁻⁴ | −7.1 to −5.0 × 10⁻⁷ |
| V1b (r_max 40, dr 0.05) | −3.2 to +2.9 × 10⁻⁶ | +3.9 to +4.9 × 10⁻⁴ | −5.8 to −5.2 × 10⁻⁷ |
| V1b vs V1a (dr 0.1 → 0.05) | −6.8 to −2.8 × 10⁻⁶ | +5.5 to +8.0 × 10⁻⁵ | — |

The V1c bracket and its stencil, r_max 20 / 40 / 40 / 60 (orig dr 0.1 / V1a dr 0.1 / V1b dr 0.05 / V1c dr 0.05):

| (k, q) | r_q | I_q | leak |
|---|---|---|---|
| (0.20, 24.8) | 3.44501 / 3.44658 / 3.44678 / 3.44678 | 12.923343 / 12.923410 / 12.923368 / 12.923365 | 4.7e-5 / 4.7e-11 / 1.8e-11 / 7.5e-12 |
| (0.25, 24.7) | 3.41882 / 3.42024 / 3.42049 / 3.42048 | 12.724930 / 12.724993 / 12.724922 / 12.724921 | 4.5e-5 / 2.2e-11 / 9.3e-12 / 6.8e-13 |
| (0.25, 24.8) | 3.42537 / 3.42686 / 3.42706 / 3.42709 | 12.774367 / 12.774423 / 12.774375 / 12.774387 | 4.5e-5 / 3.3e-11 / 3.4e-11 / 3.5e-14 |
| (0.25, 24.9) | 3.43192 / 3.43341 / 3.43362 / 3.43366 | 12.823825 / 12.823867 / 12.823835 / 12.823831 | 4.6e-5 / 4.0e-11 / 3.3e-11 / 2.2e-12 |
| (0.30, 24.7) | 3.39539 / 3.39674 / 3.39697 / 3.39696 | 12.550399 / 12.550443 / 12.550391 / 12.550379 | 4.2e-5 / 3.2e-11 / 2.8e-11 / 5.3e-13 |
| (0.30, 24.8) | 3.40197 / 3.40333 / 3.40354 / 3.40360 | 12.599146 / 12.599189 / 12.599144 / 12.599145 | 4.3e-5 / 3.8e-11 / 3.1e-11 / 3.1e-13 |
| (0.30, 24.9) | 3.40850 / 3.40991 / 3.41014 / 3.41014 | 12.647895 / 12.647943 / 12.647902 / 12.647893 | 4.3e-5 / 2.3e-11 / 5.3e-11 / 1.5e-13 |
| (0.35, 24.8) | 3.37503 / 3.37632 / 3.37654 / 3.37657 | 12.401117 / 12.401162 / 12.401107 / 12.401116 | 4.0e-5 / 3.7e-11 / 1.4e-11 / 1.7e-13 |

- **r_q grows by ~0.04 % from r_max 20 → 40 and by ≤ 0.002 % from 40 → 60. I_q changes by ≤ 10⁻⁵.**
- The small r_q step at 20 → 40 is the part of the charge tail that the r = 20 Dirichlet edge cut off. Beyond that, r_q converges with the box.
- **The charge is not delocalising into the bulk at these (k, q).**

## 5. A.4 verdict (applied literally)

| condition | test | result |
|---|---|---|
| (1) V1b | ≥ 1 central sign change of S persists (opposite 𝒯 signs at its bracketing points, central differences), with d²E/dR² > 0 by direct solve, leak < 1 % and ω < m_bulk at both bracketing points | **14 of 14** central sign changes pass. f″(1) = +6.92 to +7.14; leak ≤ 4.8 × 10⁻¹¹; ω/m = 0.9686–0.9842 at the bracketing points |
| (2) V1c | the selected sign change (#66) persists and \|𝒯(V1c) − 𝒯(V1b)\| < \|𝒯(V1b)\| at each bracketing point, no sign flip | **passes:** changes 5.8 × 10⁻⁶ and 2.3 × 10⁻⁵ against 0.491 and 0.165 |
| (3) V2 | ℰ within 10⁻³ of V1b at both bracketing points, and 𝒯 the same sign (as V1b) at both | **passes:** ℰ −3.9 × 10⁻⁶ and −4.0 × 10⁻⁶; 𝒯 (envelope) +0.489 and −0.168 against V1b +0.491 and −0.165 |

**The λ = 1 WINDOW is CONFIRMED** (PREREG_B2B3 §6 A.4).

**Confirmed sign changes and their A.1 quantities (V1b):** the 14 central ones in §4.1.
- All have **n = 3**: 3·r_q·k* = 2.94–2.99, so n = 3 is the smallest integer with R_eq/r_q ≥ 3.
- R_eq = 10.00–10.44; R_eq/r_q = 3.01–3.06.
- Q = 1478–1627; d²E/dR² = +4.16 to +4.49 (model units).
- #66, the V1c/V2 sign change: n = 3, R_eq = 10.44, Q = 1627.

**V3 does not feed A.4** or any later selection (A.5).

**Predictions (A.6):** A-P1 (CONFIRMED) **holds**. A-P2 **holds**: ≤ 4.4 × 10⁻⁴ in r_q and ≤ 6.8 × 10⁻⁶ in I_q from r_max 20 to 40. A-P3 (BPS-only) **fails**: one-sided, §6.

**Consequence (A.6, literal):** "A B4 pre-registration is written before any loop code. It fixes in advance: a selection rule among confirmed sign changes, n from A.1, and the passenger control (the cheapest charged bulk lump at the same Q, no string). The V3 classification is carried into B4's caveats." Nothing of B4 was written or run here.

## 6. V3: robustness (post-hoc, descriptive only; does not feed A.4)

Grid of V1a (dr 0.1, r_max 40). Scan rules, 𝒯 stencil and sign-change analysis are as in B3 (`b3_scan.analyse` unchanged). "Stable" means the B3 rule: Clough–Tocher f″(1) > 0. The direct-solve f″(1) is given as a cross-check.

| set | solves / in window | rows: how they ended | sign changes | stable (interp.) | direct f″ > 0 | stable sign changes: k*, q*, ω*/m | stencils | min 𝒯/ℰ (k, q) |
|---|---|---|---|---|---|---|---|---|
| V3a λ = 0.9 (m = 0.9) | 1674 / 1669 | k = 0.20, 0.25: cap q = 40 (in window, ω/m = 0.974, 0.988). k = 0.30–0.50 closed by ω ≥ m at q = 29.4, 19.0, 14.9, 12.5, 10.9 | 95 (rows k = 0.20: 57, 0.25: 37, 0.30: 1) | **76** | 95 / 95 | 0.217–0.300, 25.7–38.7, 0.979–0.996 | all one-sided k (k = 0.20 is the first scanned row) | −0.0144 (0.30, 29.3) |
| V3a λ = 1.1 (m = 1.0) | 864 / 857 | all rows closed by ω ≥ m: q = 15.2, 14.1, 13.0, 12.0, 11.2, 10.4, 9.8 for k = 0.20 … 0.50 | **0** | 0 | — | — | — | +0.110 (0.50, 9.7) |
| V3b λ = 0.8 (m = 0.8), q = 30–60 | 1806 / 1806 | every row k = 0 … 0.25 reached the cap q = 60 in window (ω/m = 0.949 … 0.999) | 259 (rows k = 0.15: 139, 0.20: 119, 0.25: 1) | **227** (122 central) | 259 / 259 | 0.176–0.242, 35.7–58.2, 0.975–0.994; central: 0.176–0.200, 46.1–58.2, 0.975–0.981 | 139 central, 119 one-sided k, 1 one-sided q | −0.038 (0.25, 60.0) |

Notes:
- The "unstable" sign changes (19 at λ = 0.9, 32 at λ = 0.8) are all points where the interpolant is undefined (the ray leaves the window hull) or disagrees with the direct solve. Every direct f″(1) is positive.
- At λ = 0.8 the original B3 NONE was truncated at q = 30. With q extended to 60 it has sign changes, so that NONE was an artifact of the q cap. Again, descriptive only.

**Classification (A.5): one-sided.** There are stable sign changes at λ = 0.9 and none at λ = 1.1. This is not "BPS-only" (A-P3 fails), and the window is not confined to λ = 1. Off BPS on the λ < 1 side (M_s = λ < M_V), the window band continues to lower k* and higher q* (λ = 0.9: k* down to 0.22, q* up to 39; λ = 0.8: k* 0.18–0.24 at q* 36–58). On the λ > 1 side (m_bulk = M_V = 1 < M_s), the rows close by ω ≥ m at q ≤ 15, with 𝒯/ℰ ≥ +0.11.

## 7. Deviations, collected

1. **SciPy installed with pip** (not in the fresh container); same version as B3 (1.18.1).
2. **The original solutions were regenerated, not loaded.** The B3 per-point fields had not been kept. They were rebuilt by replaying the recorded warm-start chain at the original grid. 465/465 λ = 1 points and 6/6 λ = 0.8 starting points reproduce the recorded ℰ bit for bit (§2).
3. **Padding needs interpolation for dr = 0.05.** "Padded with vacuum" is read as: linear interpolation of h and a in r inside r ≤ 20, vacuum (h = 1, a = 0) beyond, α kept. For V2, the padded profile (to r = 45) is mapped onto the lattice by `from_radial`.
4. **V1c selection (ambiguity, literal reading):** "the central sign change whose bracket has the most negative 𝒯". Read as: among the central sign changes of S that persist in V1b with central differences, the one with the most negative 𝒯 at a bracketing point. That is #66 (−0.1654). The first runner-up, #103, has −0.1526.
5. **V2 𝒯 is the envelope value**, T − (k² + ω²)I_q, which is exact at the minimiser. It is not the finite-difference stencil. The stencil would need 6 more L = 480 solves (each ~ 12–24 h on this machine). At the central radial points the two agree to ≤ 0.0026, about 1/60 of the smaller \|𝒯\| at the V2 points. `verify_v2.py stencil` would compute them.
6. **V2 stopped by hand.** After ~220 L-BFGS-B iterations per point, ℰ had moved by ≤ 1.4 × 10⁻⁸ relative over the last ~100 iterations, with max|∇| ≈ 3.4 × 10⁻⁶. Converging to ftol 10⁻¹⁵ would have taken days. The solves were stopped and evaluated at the last checkpoint (`V2_FINALIZE`: one further L-BFGS-B iteration). The 2D–V1b difference (4 × 10⁻⁶) is 250 × below the 10⁻³ test and 300 × above the late drift.
7. **One container restart.** V2 resumed from its 5-iteration checkpoints (L-BFGS-B memory reset once). V3 resumed from its per-point files. Running jobs were otherwise unaffected. Per-point observables were committed throughout (`verify_points/`); field files live outside the repository (`/tmp/claude-0/verify_fields`, ~0.6 GB).
8. **V3 was run at low priority (nice 19)**, concurrently with V1/V2, with 2–4 workers. Its analysis was restarted once with more workers (cached ray solves reused). This has no effect on results: the solves are deterministic and per point.
9. **Stopping criterion.** All radial solves stop on L-BFGS-B's ftol (10⁻¹²) test, as in B3. The largest max|∇| at stop is 1.8 × 10⁻³ (V1b, at 4× the unknowns), against 7.7 × 10⁻⁴ in the original window points. The energies agree across runs to ≤ 1.4 × 10⁻⁶ and 𝒯 to ≤ 10⁻⁴, so this does not affect any sign. It was not tightened, because the instrument is fixed.
10. **Ray points outside the window.** For #17, #59 and #109, the u = 0.97 ray point (k ≈ 0.46, q ≈ 15.3, beyond the k = 0.45 row's window edge at q = 15.0) is outside the window. The original rays are at the same (k, q), and its `analyse` does not check the window on the ray. The values are reported as computed. These sign changes are edge ones and do not enter A.4.
11. **n from A.1:** r_q "at the sign change" is read as the linear interpolation of the bracketing points' charge rms radius at t = 𝒯_a/(𝒯_a − 𝒯_b), the same t as for k*, q* and ω*.
12. **A.4 (3) reading (ambiguity, literal reading flagged):** "𝒯 has the same sign at both" is read as "the same sign as V1b at each of the two bracketing points". The alternative reading (the same sign at the two points as each other) would contradict a sign change, so it cannot be intended. **Flag for the author.**
13. **A.4 (2) reading:** "its 𝒯 values change by less than \|𝒯\| itself" is read per bracketing point, against the V1b \|𝒯\|.
14. **A-P2 reading:** "at the 14 central points" is read as the 27 distinct bracketing grid points of the 14 central sign changes, original (r_max 20) against V1a (r_max 40, the same dr). V1b is also reported.
15. **V3 first rows.**
    - V3a starts at k = 0.20 from the abelian-Higgs initial (α₀ = π/4 − 0.05), as B3's first point, because no λ = 0.9 or 1.1 originals exist.
    - V3b starts each row at q = 30 from the padded original λ = 0.8 solution, and then follows the B3 warm-start rule.
    - Because k = 0.20 is V3a's first row, its 𝒯 uses forward k differences. The V3 tables include these as computed.
16. **Stencil neighbours** are taken as the in-window neighbours the original `tcal` used. Every neighbour of every central bracket point stayed in the window in V1a, V1b and V1c, so the stencils are unchanged.

No parameter outside Amendment A was used. The V2 envelope 𝒯 (5) and the V2 stop (6) are method choices, not parameters, and are flagged.

## 8. What is and is not established

**Established:**
- The 14 central λ = 1 sign changes of 𝒯 on the straight fixed-charge string are **not artifacts** of the r_max = 20 box, the dr = 0.1 resolution or the radial reduction, at the level A.4 tests.
  - Doubling and tripling the box and halving dr change ℰ by ≤ 1.4 × 10⁻⁶ and 𝒯 by ≤ 10⁻⁴.
  - d²E/dR² stays positive.
  - The full 2D functional agrees with the radial one to 4 × 10⁻⁶ at the bracket of the deepest sign change.
- **The A.4 confirmation rule is met: CONFIRMED.** A.6 says a B4 pre-registration is now to be written.
- The charge does not delocalise with the box (r_q and I_q converge; A-P2 holds).
- Descriptively, the window is not a λ = 1 fine-tuning: it is present at λ = 0.9 and at λ = 0.8 for q > 30, and absent at λ = 1.1 (one-sided).

**Not established:**
- **No loop exists or was computed.** A confirmed straight-string window is not a vorton.
- **The thin-ring proxy is marginal by construction.** With n = 3, R_eq/r_q = 3.01–3.06 is right at A.1's threshold. ω*/m is 0.981–0.982, still at the leak threshold in frequency, though not in the spatial leak, which is ≤ 10⁻¹⁰.
- The 2D check is at one point pair and one spacing, with 𝒯 from the envelope identity, not the 2D stencil. Its 80 × closer agreement than at the B3 §2.4 point is not explained.
- The edge sign changes, especially #17, rest on one-sided k differences that disagree with the envelope 𝒯. Only the central ones are clean.
- **Classical only.** The CP² worldsheet gap (B1 §2) is outside this test.
- The B4 pre-registration (selection rule, n, passenger control) is the author's to write; it was not started.

## 9. Files

- **Code (new):** `verify_common.py`, `verify_orig.py`, `verify_v1.py`, `verify_v2.py`, `verify_v3.py`, `verify_tables.py`, `verify_chain.sh`. Existing code is imported, unchanged.
- **Results:**
  - `verify_results.json`: point set, V1a/V1b/V1c/V2 per-point and per-sign-change results, trends, A.4 evaluation, V3 summaries;
  - `verify_V1a.json`, `verify_V1b.json` (includes the V1c selection), `verify_V1c.json`, `verify_V2.json`, `verify_V3.json` (includes every V3 point's observables);
  - `verify_points/<run>/<i>_<j>.json`: every solved point's observables, written as it was solved.
- **Logs:** `log_verify_orig.txt`, `log_verify_V1a.txt`, `log_verify_V1b.txt`, `log_verify_V1c.txt`, `log_verify_V2.txt`, `log_verify_v3_run.txt`, `log_verify_V3.txt`, `log_verify_tables.txt`.
- Field files are not committed. They are reproducible: the scripts are deterministic, and the regenerated originals are bit-identical to B3.
