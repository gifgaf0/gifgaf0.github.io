# E10 / Route B, QB: where do bulk charged lumps (Q-balls) bind? Report

*November 5, 2026. **Label: Exploration.** Run under `PREREG_QB.md`, committed at ed1254b before any QB run (head at start: ed1254b). Scope: exactly PREREG_QB §1–§3. B4's axisymmetric instrument with n = 0 and no vortex, unchanged and imported. No grid refinement. No existing file was edited; README.md and the STATUS files are untouched. New files: `qb_run.py`, `qb_analyse.py`, `qb_chain.sh`, `qb_autocommit.sh`, `qb_resume.sh`, `qb_fields/.gitignore`, `qb_results.json`, `qb_hist/`, `qb_fields/`, `log_qb_*.txt`, and this report.*

**Units.** Model units only (PREREG_B2B3 §1): energies in v²/(gv), lengths in 1/(gv). Q is the SU(3)_{C+F} Noether charge under G = diag(0, 1, 0). It is not electric charge, and no particle identification is made. m_bulk = min(1, λ).

## Summary

| | Result |
|---|---|
| **Regression (QB-P1)** | **Passes.** λ = 1, Q = 1626.5329, S1 (B4's C-d start): E = 1589.911045, which is 2.8 × 10⁻⁸ relative from 1589.9110 (2.4 × 10⁻⁹ from B4's unrounded 1589.9110486). |
| **Verdict grid** | **BOUND** at λ = 0.8 and 0.9 for Q ∈ {1626.5, 2710.9}, and at λ = 1.0 for Q ∈ {800, 1626.5, 2710.9}. **DISPERSED** everywhere else, including every Q at λ = 1.1 and 1.2. No MARGINAL point. |
| **Starts** | S1 and S2 reach the same end state at all 25 points: \|ΔE\|/E ≤ 1.5 × 10⁻¹⁰, and the verdicts are identical. |
| **Q_min(λ) brackets** | (800, 1626.53] at λ = 0.8 and 0.9; (400, 800] at λ = 1.0; > 2710.9 (no BOUND point on the grid) at λ = 1.1 and 1.2. |
| **Box check** (6 runs, ρ ∈ [0, 60], z ∈ [−30, 30]) | **All pass:** every verdict is unchanged, and \|ΔE/E\| ≤ 1.0 × 10⁻⁴. |
| **Resolution check** (3 runs, h = 0.125) | **All pass:** every verdict is unchanged, and \|ΔE/E\| ≤ 1.2 × 10⁻⁵. |
| **Classification** | B = {0.8, 0.9, 1.0} = W, so **TRACKS**. |
| **Predictions** | QB-P1 holds. QB-P2 (BROADER, 55 %) fails. QB-P2′ (TRACKS, 30 %) holds. QB-P3 (70 %) fails as stated: E/(m_bulk Q) does fall with Q at every λ in B, but Q_min does not rise with λ inside the window (it falls from 0.9 to 1.0). QB-P4 (45 %) fails: λ = 1.2 at Q = 2710.9 is DISPERSED with E/(m_bulk Q) = 1.0100. |
| **§6 consequence** | **TRACKS branch:** on this grid, the lump binds where the straight-string window exists and nowhere else. |

**What changed against the preregistered expectation.** The thin-wall estimate (PREREG_QB §5) predicted lumps up to λ ≈ √2. At λ = 1.1 and 1.2 the charge instead spreads over the box at every Q up to 2710.9: about 25 % of it sits in the edge band, the 3D rms radius is about 29, and |det H| stays ≥ 0.99 (no unhiggsed core forms). At λ ≤ 1, every BOUND lump has the unhiggsed-orientation core B4 found: |det H| < 0.7 out to r ≈ 5.5–10, with τ = 1.000. There is also a sign difference in the spread-out states. At λ > 1, E/(m_bulk Q) rises with Q (1.0036 → 1.0098 at λ = 1.1), as a net repulsion would. At λ ≤ 1 it falls with Q. This is descriptive only; no fit was made.

## 1. Commands run

```
pip install scipy==1.18.1 numba==0.68.1          # not present in the container; the same versions as B4 (deviation 1)
python3 qb_run.py L1.0_Q1626.5329_S1 > log_qb_L1.0_Q1626.5329_S1.txt   # regression, alone, before any other run
python3 qb_analyse.py regression                  # QB-P1 gate (exit 1 on failure)
./qb_chain.sh >> log_qb_chain.txt                 # re-checks the gate; 49 grid runs, 4 at a time; then the
                                                  # box/resolution runs listed by `qb_analyse.py checklist`;
                                                  # then qb_analyse.py > log_qb_analyse.txt (-> qb_results.json)
./qb_autocommit.sh                                # WIP commits every 20 min (container restarts); none occurred
```

`qb_resume.sh` relaunches the chain after a container restart. Every run resumes from its checkpoint or is skipped if it is done. It was not needed: every run reports 0 restarts.

**Software:** Python 3.13.18, numpy 2.5.3, scipy 1.18.1, numba 0.68.1, the same as B4. One thread per process, four processes on four cores.

**Wall time:** 39,800 s of CPU over the 50 grid runs (535–1,199 s each), plus 10,100 s for the 9 check runs.

### 1.1 Instrument (unchanged from B4)

- `qb_run.py` builds `b4_axi.Axi(lam, h = 0.25, rho_max = 40, zhalf = 20, n = 0, Q)` with Dirichlet H = 1 on the outer column and on the rows z = ±20.
- Minimiser and settings, all imported unchanged:
  - `b4_lbfgs.lbfgs` with `b4_run.OPTS` (m = 20, gtol = 10⁻⁶, ftol = 10⁻¹⁴ on 5 consecutive iterations, maxiter 20,000);
  - CG tolerances `b4_run.CG_TOL_RUN` = 10⁻⁸ during the run and `CG_TOL_OBS` = 10⁻¹² for observables;
  - observables and checkpoints every 50 iterations (`b4_run.EVERY`).
- Fixed charge Q, with E = E_static + Q²/(4I) and ω = Q/(2I), exactly as in B4. With n = 0 there is no twist.
- **Starts:**
  - S1 = `b4_axi.ball_start(A)`, radius 4: B4's C-d start, H = 1 − (1 − r²/R²)² m m†, m = (1, 1, 0)/√2, W = 0.
  - S2 = `b4_axi.ball_start(A, R=8)`.
- **Per-run observables:**
  - E and E/(m_bulk Q);
  - ω/m_bulk, from `Axi.observables`, which already divides by min(1, λ);
  - leak: the charge fraction with ρ > ρ_max − 4 or |z| > z_half − 4, so the axis is excluded;
  - 3D charge rms radius √⟨ρ² + z²⟩ about the origin, weighted by the Gauss-law charge density at the solved X (as B4's `b4_tables.py`);
  - r_q: B4's rms distance from the charge-weighted circle (R_q, z_q);
  - radius of the |det H| < 0.7 region: the largest √(ρ² + z²) of any site with |det H| < 0.7 (deviation 4), with its largest ρ and |z| also recorded;
  - iterations and stop message, plus τ, I, |det H| at the origin, the charge fractions within r < 5, 10 and 15, and max|∇|.
- **Saved:**
  - final fields: `qb_fields/<tag>.npz` (the packed L-BFGS vector; `Axi.unpack` gives H, W_ρ, W_z, W̃_φ);
  - histories: `qb_hist/<tag>.json`;
  - logs: `log_qb_<tag>.txt`;
  - collected results: `qb_results.json`.
- **File sizes:** 80 MB of fields in total. The largest single file is 4.4 MB (an h = 0.125 field). **No file exceeds 20 MB.**

### 1.2 Regression (QB-P1)

| | value |
|---|---|
| run | λ = 1, Q = 1626.5329, S1 (= B4 C-d) |
| E | **1589.9110448** |
| target (PREREG_QB §1) | 1589.9110 → rel. dev. **2.8 × 10⁻⁸** (< 10⁻⁶: **passes**) |
| B4 C-d, unrounded (Q = 1626.532904) | 1589.9110486 → rel. dev. 2.4 × 10⁻⁹ |
| other quantities | ω/m = 0.95531, leak 1.58 × 10⁻⁴, 3D rms 7.351, r_q = 4.974 (B4: 0.95531, 1.6 × 10⁻⁴, 7.35, 4.974) |
| iterations / stop | 1720 / ftol (B4: 1607 / line search failed after memory reset; the path differs because Q differs in the 8th digit) |

**A second cross-check, not part of the gate.** λ = 1 at Q = 2710.9 gives E = 2621.4703. B4's C-d5 gave 2621.4591 at Q = 2710.8882. The ratio ΔE/ΔQ = 0.95 matches ω = 0.948, as dE/dQ = ω requires.

## 2. All 50 runs

λ, Q; start; final E; E/(m_bulk Q); ω/m_bulk; leak; 3D charge rms radius; r_q; radius of the |det H| < 0.7 region (0 = no such site); L-BFGS iterations; stop ("ls" = line search failed after memory reset); per-run verdict.

| λ | Q | start | E | E/(m Q) | ω/m | leak | 3D rms | r_q | \|det H\|<0.7 radius | iters | stop | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.8 | 200 | S1 | 161.1437 | 1.00715 | 1.00664 | 0.0141 | 19.376 | 10.527 | 0 | 2007 | ftol | DISPERSED |
| 0.8 | 200 | S2 | 161.1437 | 1.00715 | 1.00664 | 0.0141 | 19.376 | 10.527 | 0 | 1873 | ftol | DISPERSED |
| 0.8 | 400 | S1 | 322.1138 | 1.00661 | 1.00544 | 0.0127 | 18.542 | 10.367 | 0 | 1919 | ls | DISPERSED |
| 0.8 | 400 | S2 | 322.1138 | 1.00661 | 1.00544 | 0.0127 | 18.542 | 10.367 | 0 | 1917 | ls | DISPERSED |
| 0.8 | 800 | S1 | 643.1064 | 1.00485 | 0.99655 | 0.0054 | 12.286 | 8.224 | 0 | 3379 | ls | DISPERSED |
| 0.8 | 800 | S2 | 643.1064 | 1.00485 | 0.99655 | 0.0054 | 12.286 | 8.224 | 0 | 3357 | ls | DISPERSED |
| 0.8 | 1626.53 | S1 | 1290.5918 | 0.99183 | 0.97014 | 0.0012 | 8.945 | 6.123 | 8.163 | 1685 | ls | BOUND |
| 0.8 | 1626.53 | S2 | 1290.5918 | 0.99183 | 0.97014 | 0.0012 | 8.945 | 6.123 | 8.163 | 1650 | ls | BOUND |
| 0.8 | 2710.9 | S1 | 2127.2198 | 0.98086 | 0.96004 | 0.0014 | 9.632 | 6.474 | 10.174 | 2052 | ftol | BOUND |
| 0.8 | 2710.9 | S2 | 2127.2198 | 0.98086 | 0.96004 | 0.0014 | 9.632 | 6.474 | 10.174 | 1687 | ls | BOUND |
| 0.9 | 200 | S1 | 181.0070 | 1.00559 | 1.00513 | 0.0139 | 19.270 | 10.508 | 0 | 1911 | ftol | DISPERSED |
| 0.9 | 200 | S2 | 181.0070 | 1.00559 | 1.00513 | 0.0139 | 19.269 | 10.508 | 0 | 1883 | ls | DISPERSED |
| 0.9 | 400 | S1 | 361.8309 | 1.00509 | 1.00396 | 0.0122 | 18.198 | 10.295 | 0 | 2405 | ftol | DISPERSED |
| 0.9 | 400 | S2 | 361.8309 | 1.00509 | 1.00396 | 0.0122 | 18.197 | 10.295 | 0 | 2018 | ls | DISPERSED |
| 0.9 | 800 | S1 | 720.4495 | 1.00062 | 0.98077 | 9.2e-04 | 7.988 | 5.603 | 5.535 | 1686 | ls | DISPERSED |
| 0.9 | 800 | S2 | 720.4495 | 1.00062 | 0.98077 | 9.2e-04 | 7.988 | 5.603 | 5.535 | 1786 | ftol | DISPERSED |
| 0.9 | 1626.53 | S1 | 1441.5806 | 0.98477 | 0.96229 | 4.7e-04 | 8.009 | 5.460 | 8.083 | 1927 | ftol | BOUND |
| 0.9 | 1626.53 | S2 | 1441.5806 | 0.98477 | 0.96229 | 4.7e-04 | 8.009 | 5.460 | 8.083 | 1482 | ls | BOUND |
| 0.9 | 2710.9 | S1 | 2376.0082 | 0.97385 | 0.95374 | 6.3e-04 | 8.900 | 5.970 | 9.888 | 2001 | ftol | BOUND |
| 0.9 | 2710.9 | S2 | 2376.0082 | 0.97385 | 0.95374 | 6.3e-04 | 8.900 | 5.970 | 9.888 | 1992 | ftol | BOUND |
| 1.0 | 200 | S1 | 200.8973 | 1.00449 | 1.00405 | 0.0137 | 19.157 | 10.487 | 0 | 1976 | ftol | DISPERSED |
| 1.0 | 200 | S2 | 200.8973 | 1.00449 | 1.00405 | 0.0137 | 19.158 | 10.487 | 0 | 1950 | ls | DISPERSED |
| 1.0 | 400 | S1 | 401.6014 | 1.00400 | 1.00290 | 0.0117 | 17.782 | 10.204 | 0 | 2515 | ftol | DISPERSED |
| 1.0 | 400 | S2 | 401.6014 | 1.00400 | 1.00290 | 0.0117 | 17.783 | 10.204 | 0 | 2402 | ftol | DISPERSED |
| 1.0 | 800 | S1 | 795.5614 | 0.99445 | 0.96989 | 2.1e-04 | 6.646 | 4.624 | 5.870 | 1466 | ls | BOUND |
| 1.0 | 800 | S2 | 795.5614 | 0.99445 | 0.96989 | 2.1e-04 | 6.646 | 4.624 | 5.870 | 1526 | ftol | BOUND |
| 1.0 | 1626.53 | S1 | 1589.9110 | 0.97748 | 0.95531 | 1.6e-04 | 7.351 | 4.974 | 7.926 | 1720 | ftol | BOUND |
| 1.0 | 1626.53 | S2 | 1589.9110 | 0.97748 | 0.95531 | 1.6e-04 | 7.351 | 4.974 | 7.926 | 1450 | ls | BOUND |
| 1.0 | 2710.9 | S1 | 2621.4703 | 0.96701 | 0.94815 | 2.5e-04 | 8.347 | 5.571 | 9.605 | 1822 | ftol | BOUND |
| 1.0 | 2710.9 | S2 | 2621.4703 | 0.96701 | 0.94815 | 2.5e-04 | 8.347 | 5.571 | 9.605 | 1649 | ls | BOUND |
| 1.1 | 200 | S1 | 200.7245 | 1.00362 | 1.00420 | 0.2018 | 29.217 | 12.033 | 0 | 2409 | ls | DISPERSED |
| 1.1 | 200 | S2 | 200.7245 | 1.00362 | 1.00420 | 0.2018 | 29.216 | 12.034 | 0 | 2103 | ls | DISPERSED |
| 1.1 | 400 | S1 | 401.6775 | 1.00419 | 1.00533 | 0.2020 | 29.227 | 12.107 | 0 | 2254 | ftol | DISPERSED |
| 1.1 | 400 | S2 | 401.6775 | 1.00419 | 1.00533 | 0.2020 | 29.227 | 12.107 | 0 | 2060 | ls | DISPERSED |
| 1.1 | 800 | S1 | 804.2484 | 1.00531 | 1.00748 | 0.2063 | 29.233 | 12.318 | 0 | 3002 | ftol | DISPERSED |
| 1.1 | 800 | S2 | 804.2484 | 1.00531 | 1.00748 | 0.2064 | 29.233 | 12.318 | 0 | 2963 | ls | DISPERSED |
| 1.1 | 1626.53 | S1 | 1638.4822 | 1.00735 | 1.01114 | 0.2400 | 29.160 | 13.116 | 0 | 2218 | ls | DISPERSED |
| 1.1 | 1626.53 | S2 | 1638.4822 | 1.00735 | 1.01114 | 0.2400 | 29.160 | 13.116 | 0 | 1993 | ls | DISPERSED |
| 1.1 | 2710.9 | S1 | 2737.4905 | 1.00981 | 1.01585 | 0.2590 | 29.274 | 13.503 | 0 | 2147 | ftol | DISPERSED |
| 1.1 | 2710.9 | S2 | 2737.4905 | 1.00981 | 1.01585 | 0.2590 | 29.274 | 13.503 | 0 | 2136 | ls | DISPERSED |
| 1.2 | 200 | S1 | 200.7289 | 1.00364 | 1.00424 | 0.2021 | 29.225 | 12.036 | 0 | 2156 | ls | DISPERSED |
| 1.2 | 200 | S2 | 200.7289 | 1.00364 | 1.00424 | 0.2021 | 29.224 | 12.036 | 0 | 1939 | ftol | DISPERSED |
| 1.2 | 400 | S1 | 401.6948 | 1.00424 | 1.00541 | 0.2025 | 29.242 | 12.111 | 0 | 2097 | ls | DISPERSED |
| 1.2 | 400 | S2 | 401.6948 | 1.00424 | 1.00541 | 0.2025 | 29.242 | 12.111 | 0 | 1892 | ftol | DISPERSED |
| 1.2 | 800 | S1 | 804.3138 | 1.00539 | 1.00761 | 0.2091 | 29.239 | 12.370 | 0 | 3186 | ls | DISPERSED |
| 1.2 | 800 | S2 | 804.3138 | 1.00539 | 1.00761 | 0.2091 | 29.238 | 12.370 | 0 | 2976 | ls | DISPERSED |
| 1.2 | 1626.53 | S1 | 1638.7126 | 1.00749 | 1.01140 | 0.2424 | 29.183 | 13.151 | 0 | 2008 | ftol | DISPERSED |
| 1.2 | 1626.53 | S2 | 1638.7126 | 1.00749 | 1.01140 | 0.2424 | 29.183 | 13.151 | 0 | 1811 | ftol | DISPERSED |
| 1.2 | 2710.9 | S1 | 2738.0884 | 1.01003 | 1.01627 | 0.2615 | 29.304 | 13.534 | 0 | 2146 | ls | DISPERSED |
| 1.2 | 2710.9 | S2 | 2738.0884 | 1.01003 | 1.01627 | 0.2615 | 29.304 | 13.534 | 0 | 1824 | ls | DISPERSED |

- **Stop rule.** 28 of 50 runs stopped on "line search failed (after memory reset)" and 22 on ftol. max|∇| ≤ 1.6 × 10⁻⁴ in every run (B4: 3.6 × 10⁻⁵ to 2.0 × 10⁻⁴). S1 and S2 agree to ≤ 1.5 × 10⁻¹⁰ in E at every point, so both stop types reach the same state.
- **Restarts and τ.** No run restarted. τ = 1.000 in every run.
- **BOUND lumps** (S1 values; S2 is identical):

| λ | Q | \|det H\| at origin | min \|det H\| | \|det H\|<0.7: max ρ / max \|z\| | charge within r < 5 / 10 / 15 | I |
|---|---|---|---|---|---|---|
| 0.8 | 1626.53 | 0.127 | 0.127 | 8.12 / 8.00 | 0.167 / 0.730 / 0.959 | 1047.9 |
| 0.8 | 2710.9 | 0.015 | 0.015 | 10.12 / 10.00 | 0.108 / 0.643 / 0.952 | 1764.8 |
| 0.9 | 1626.53 | 0.021 | 0.000 | 7.88 / 8.00 | 0.202 / 0.825 / 0.984 | 939.0 |
| 0.9 | 2710.9 | 0.072 | 0.001 | 9.88 / 9.75 | 0.123 / 0.728 / 0.978 | 1579.1 |
| 1.0 | 800 | 0.038 | 0.038 | 5.62 / 5.75 | 0.381 / 0.918 / 0.993 | 412.4 |
| 1.0 | 1626.53 | 0.154 | 0.000 | 7.88 / 7.75 | 0.231 / 0.891 / 0.994 | 851.3 |
| 1.0 | 2710.9 | 0.145 | 0.000 | 9.38 / 9.50 | 0.134 / 0.800 / 0.990 | 1429.6 |

  The unhiggsed region is close to spherical: its largest ρ and largest |z| agree to within 0.25. It grows with Q, roughly like Q^{1/3}, as a thin-wall lump would (descriptive).

- **λ ≥ 1.1, all Q.**
  - Min |det H| ≥ 0.99.
  - 8–11 % of the charge lies within r < 15, and 20–26 % sits in the edge band.
  - I ≈ Q/(2ω) with ω slightly above m_bulk: the charge occupies the box's lowest charged mode.
  - Path, as an example: λ = 1.2, Q = 2710.9, S2 is still compact at iteration 300 (r_q = 4.6, E/(mQ) = 1.14), then spreads (leak 0.27 by iteration 600).
  - In all 20 λ ≥ 1.1 runs, the minimum E/(m_bulk Q) over the recorded history equals the end value, which is above 1. No recorded state was below m_bulk Q.

## 3. Verdict grid and Q_min brackets

Verdict of the lower-E start (PREREG_QB §3). In brackets: which start had the lower E, and the S1/S2 verdicts (B = BOUND, D = DISPERSED). The number is E/(m_bulk Q) of the lower-E start.

| λ \ Q | 200 | 400 | 800 | 1626.53 | 2710.9 | Q_min bracket |
|---|---|---|---|---|---|---|
| 0.8 | **DISPERSED** (S2; D/D) 1.0071 | **DISPERSED** (S2; D/D) 1.0066 | **DISPERSED** (S2; D/D) 1.0049 | **BOUND** (S2; B/B) 0.9918 | **BOUND** (S1; B/B) 0.9809 | (800, 1626.53] |
| 0.9 | **DISPERSED** (S1; D/D) 1.0056 | **DISPERSED** (S1; D/D) 1.0051 | **DISPERSED** (S2; D/D) 1.0006 | **BOUND** (S1; B/B) 0.9848 | **BOUND** (S1; B/B) 0.9738 | (800, 1626.53] |
| 1.0 | **DISPERSED** (S2; D/D) 1.0045 | **DISPERSED** (S1; D/D) 1.0040 | **BOUND** (S2; B/B) 0.9945 | **BOUND** (S1; B/B) 0.9775 | **BOUND** (S2; B/B) 0.9670 | (400, 800] |
| 1.1 | **DISPERSED** (S2; D/D) 1.0036 | **DISPERSED** (S2; D/D) 1.0042 | **DISPERSED** (S1; D/D) 1.0053 | **DISPERSED** (S2; D/D) 1.0073 | **DISPERSED** (S2; D/D) 1.0098 | > 2710.9 (no BOUND point) |
| 1.2 | **DISPERSED** (S2; D/D) 1.0036 | **DISPERSED** (S2; D/D) 1.0042 | **DISPERSED** (S1; D/D) 1.0054 | **DISPERSED** (S2; D/D) 1.0075 | **DISPERSED** (S2; D/D) 1.0100 | > 2710.9 (no BOUND point) |

- **Which start is lower.** The lower-E start is decided by differences of 10⁻¹¹ to 10⁻¹⁰ relative, at the level of the stopping noise. It never affects a verdict.
- **No MARGINAL point.** Every point satisfies all four BOUND conditions or meets a DISPERSED condition.
- **Q_min brackets:** (800, 1626.53] at λ = 0.8 and 0.9; (400, 800] at λ = 1.0; above 2710.9 at λ = 1.1 and 1.2. These are reported as brackets only; there is no refinement (PREREG_QB §3, §7).
- **Two DISPERSED points worth flagging** (deviation 7):
  - **λ = 0.9, Q = 800** is DISPERSED only through the clause E/(m_bulk Q) ≥ 1, at 1.00062. It is otherwise lump-like: leak 9 × 10⁻⁴, 3D rms 7.99, ω/m = 0.981, and |det H| < 0.7 out to r = 5.5. It is a compact charged object 0.06 % above m_bulk Q in this box.
  - **λ = 0.8, Q = 800** is partly localized (leak 0.54 %, rms 12.3, ω/m = 0.997, no |det H| < 0.7 site) at E/(mQ) = 1.0049.
  - Both are DISPERSED under the literal rule, and the brackets use the literal verdicts.

## 4. Box and resolution checks (PREREG_QB §3)

**Box check.** For each λ, the largest-Q and the smallest-Q BOUND point (lower-E start) were re-relaxed in ρ ∈ [0, 60], z ∈ [−30, 30] at h = 0.25.
- **Start:** the h = 0.25 end state, embedded on the same lattice sites with vacuum padding (H = 1, W = 0) outside the old box (deviation 5).
- **Leak band:** within 4 of the new edges (ρ > 56 or |z| > 26).

| point | E (B4 box) | E (large box) | \|ΔE/E\| | verdict | E/(mQ) | leak | 3D rms | iters | stop | passes |
|---|---|---|---|---|---|---|---|---|---|---|
| λ 0.8, Q 1626.53 (S2) | 1290.5918 | 1290.4602 | 1.02e-04 | BOUND → BOUND | 0.99183 → 0.99173 | 1.2e-03 → 1.6e-05 | 8.945 → 9.035 | 1372 | ls | **yes** |
| λ 0.8, Q 2710.9 (S1) | 2127.2198 | 2127.0015 | 1.03e-04 | BOUND → BOUND | 0.98086 → 0.98076 | 1.4e-03 → 1.1e-05 | 9.632 → 9.687 | 1656 | ftol | **yes** |
| λ 0.9, Q 1626.53 (S1) | 1441.5806 | 1441.5471 | 2.32e-05 | BOUND → BOUND | 0.98477 → 0.98474 | 4.7e-04 → 2.2e-06 | 8.009 → 8.030 | 1436 | ftol | **yes** |
| λ 0.9, Q 2710.9 (S1) | 2376.0082 | 2375.9414 | 2.81e-05 | BOUND → BOUND | 0.97385 → 0.97382 | 6.3e-04 → 1.8e-06 | 8.900 → 8.917 | 1205 | ls | **yes** |
| λ 1.0, Q 800 (S2) | 795.5614 | 795.5549 | 8.14e-06 | BOUND → BOUND | 0.99445 → 0.99444 | 2.1e-04 → 1.0e-06 | 6.646 → 6.660 | 895 | ls | **yes** |
| λ 1.0, Q 2710.9 (S2) | 2621.4703 | 2621.4513 | 7.25e-06 | BOUND → BOUND | 0.96701 → 0.96700 | 2.5e-04 → 2.8e-07 | 8.347 → 8.351 | 1096 | ls | **yes** |

- E falls slightly in the larger box, at most by 1.0 × 10⁻⁴ (λ = 0.8, the softest and widest lumps). The threshold shift the MARGINAL band allows for (0.005) is about 50 times larger.
- The tightest BOUND margin on the grid is λ = 1.0, Q = 800: E/(mQ) = 0.99445 against 0.995. That point is in both checks, and both move E/(mQ) by ≤ 2 × 10⁻⁵.

**Resolution check.** For each λ with a BOUND point, one BOUND point was re-relaxed at h = 0.125, in the B4 box, starting from `b4_run.refine` of the h = 0.25 end state.
- **Reading:** the smallest-Q BOUND point, the one nearest the binding threshold (deviation 6).

| point | E (h = 0.25) | E (h = 0.125) | \|ΔE/E\| | verdict | E/(mQ) | leak | iters | stop | passes |
|---|---|---|---|---|---|---|---|---|---|
| λ 0.8, Q 1626.53 (S2) | 1290.5918 | 1290.5989 | 5.45e-06 | BOUND → BOUND | 0.99183 → 0.99183 | 1.2e-03 → 1.3e-03 | 726 | ls | **yes** |
| λ 0.9, Q 1626.53 (S1) | 1441.5806 | 1441.5906 | 6.96e-06 | BOUND → BOUND | 0.98477 → 0.98477 | 4.7e-04 → 4.9e-04 | 880 | ftol | **yes** |
| λ 1.0, Q 800 (S2) | 795.5614 | 795.5706 | 1.16e-05 | BOUND → BOUND | 0.99445 → 0.99446 | 2.1e-04 → 2.2e-04 | 729 | ls | **yes** |

All nine checks pass. The DISPERSED points were not box-checked; PREREG_QB §3 does not ask for it.

## 5. Classification, predictions, consequence

**Classification (PREREG_QB §4).** B = {0.8, 0.9, 1.0} and W = {0.8, 0.9, 1.0}, so B = W: **TRACKS.**

| ID | Prediction | Prior | Outcome |
|---|---|---|---|
| QB-P1 | Regression reproduces B4's C-d | must hold | **Holds.** 2.8 × 10⁻⁸ relative. |
| QB-P2 | BROADER: lumps bind at λ = 1.1 and 1.2 at the larger Q | 55 % | **Fails.** No BOUND point at λ = 1.1 or 1.2. |
| QB-P2′ | TRACKS | 30 % | **Holds.** |
| QB-P3 | At each λ with a BOUND point, E/(m_bulk Q) falls with Q, and Q_min(λ) rises with λ | 70 % | **Fails as stated.** The first half holds at every λ in B: 0.9918 → 0.9809 (λ = 0.8), 0.9848 → 0.9738 (0.9), 0.9945 → 0.9775 → 0.9670 (1.0). The second half fails: the smallest BOUND Q is 1626.53, 1626.53 and 800 at λ = 0.8, 0.9 and 1.0, so it falls from 0.9 to 1.0 inside the window. It then jumps to "none ≤ 2710.9" at 1.1 and 1.2. Reading used: the smallest BOUND Q must be non-decreasing in λ and larger at 1.2 than at 0.8, with no BOUND point counted as +∞. |
| QB-P4 | λ = 1.2, Q = 2710.9: BOUND with 0.95 < E/(m_bulk Q) < 0.995 | 45 % | **Fails.** DISPERSED: E/(mQ) = 1.0100, leak 0.26, ω/m = 1.016. |

**The thin-wall estimate (§5) is not borne out on this grid.** It predicted binding at large Q for every λ < √2. At λ = 1.1 and 1.2, no compact charged state with E < m_bulk Q appears up to Q = 2710.9, from either start. Inside the window, Q_min falls with λ (0.8, 0.9 → 1.0), and E/(mQ) at fixed Q falls as λ rises toward 1. Then binding stops between λ = 1.0 and 1.1 at every Q tested.

**§6 consequence (TRACKS branch, as preregistered).** On the λ × Q grid of PREREG_QB, the window and the lump coincide. That is what a shared mechanism would produce: the attraction that lets a charged string hold its charge also lets the charge bind without the string. It is a structural reason why charge-supported closures are passengers in this class of models. The qualifications are in §7.

## 6. Deviations and readings, collected

1. **Software installs.** `pip install scipy==1.18.1 numba==0.68.1`; neither was in the container. These are the same versions B4 used, and numba is for speed only.
2. **Literal Q values.** The grid uses Q = 1626.5329 and 2710.9 as written in PREREG_QB. B4's unrounded values were 1626.532904 and 2710.8882. The regression ran at the literal value: 1626.5329 differs from B4's Q by 2 × 10⁻⁹ relative.
3. **Leak definition.** Leak is the charge-density fraction in the band within 4 of the Dirichlet edges, axis excluded: `Axi.observables` unchanged, i.e. ρ > ρ_max − 4 or |z| > z_half − 4. In the large box it is relative to the new edges.
4. **Radius of the |det H| < 0.7 region.** Taken as the largest 3D distance √(ρ² + z²) from the origin of any site with |det H| < 0.7, or 0 if there is none. B4 quoted "ρ ≤ 7.9" for C-d without a script. The max ρ and max |z| are recorded too (§2): 7.88 and 7.75 for this run, matching B4.
5. **Box-check start.** The h = 0.25 end state is copied onto the same sites of the larger lattice, and the new region is vacuum (H = 1, W = 0, W̃_φ = 0). The PREREG says "re-relax"; this is the literal reading of re-relaxing the same state.
6. **Resolution-check point.** "One BOUND point" per λ: the smallest-Q BOUND point (lower-E start) was taken, as the most threshold-sensitive. **Flag for the author.** The other choices were not run, but every point's box check moved E by ≤ 10⁻⁴.
7. **Literal verdicts for compact-but-above-threshold states.** λ = 0.9, Q = 800 is localized (leak < 0.1 %, rms 8, |det H| < 0.7 to r = 5.5) but has E/(mQ) = 1.0006, so it is DISPERSED. λ = 0.8, Q = 800 is partly localized at 1.0049, also DISPERSED. Under a reading that asked only for localization, the brackets at λ = 0.9 (and possibly 0.8) would move down to (400, 800]. **Flag for the author.** Only the literal verdict is used.
8. **Stop rule.** 28 of 50 grid runs and 6 of 9 check runs ended on "line search failed (after memory reset)", as several B4 runs did. That is the B4 stopping rule unchanged. max|∇| ≤ 1.6 × 10⁻⁴ on the grid and ≤ 1.9 × 10⁻⁴ in the checks, and S1/S2 agree to ≤ 1.5 × 10⁻¹⁰.
9. **Lower-E start.** The lower-E start is decided by differences of 10⁻¹¹ to 10⁻¹⁰ relative, i.e. by stopping noise. It never changes a verdict.
10. **QB-P3 reading.** "Rises with λ" was taken as: the smallest BOUND Q is non-decreasing in λ, and larger at 1.2 than at 0.8 (no BOUND point = +∞). "Falls with Q" was taken as strictly decreasing over the BOUND Q values. **Flag for the author:** other readings of "rises" (for example, comparing only λ > 1 with λ ≤ 1) would make the second half hold.
11. **Auxiliary files.**
    - `qb_fields/.gitignore` (new) keeps the float64 run checkpoints out of git; float32 copies were committed periodically by `qb_autocommit.sh` and deleted when each run finished.
    - The WIP commits ("E10 QB: WIP run state") come from that script and from manual commits during the run.
12. **No container restart.** Every run reports 0 restarts, and `qb_resume.sh` was never used.

## 7. What is and isn't established

**Established (Exploration, this instrument: axisymmetric, n = 0, h = 0.25, box 40 × 40 with the 60 × 60 and h = 0.125 checks):**
- In the U(3) single-coupling model (PREREG_B2B3 §1, G = diag(0, 1, 0)), a localized charged lump with E < 0.995 m_bulk Q, ω < m_bulk and leak < 1 % exists at λ = 0.8, 0.9 and 1.0, for Q ≥ 1626.5 (λ = 0.8, 0.9) and Q ≥ 800 (λ = 1.0) on the grid.
- Every such lump has an unhiggsed core (|det H| → 0, H ≈ 1 − mm†) of radius about 5.5–10 that grows with Q. E/(m_bulk Q) falls with Q at each λ.
- At λ = 1.1 and 1.2, no such state was found at any Q ≤ 2710.9. Both starts relax to the same box-filling state with E > m_bulk Q.
- So the set of λ with a bound lump equals the set with a straight-string window, on this grid: **TRACKS**.
- B4's C-d is reproduced to 2.8 × 10⁻⁸.
- Every BOUND verdict survives a 1.5× larger box (ΔE ≤ 1.0 × 10⁻⁴) and, where checked, h → h/2 (ΔE ≤ 1.2 × 10⁻⁵).

**Not established:**
- **Binding at λ = 1.1 or 1.2 for Q > 2710.9.** The thin-wall estimate still allows lumps at large enough Q, and the grid stops at 2710.9. Checking would need a new pre-registration (PREREG_QB §7).
- **That the lump is absent at λ = 1.1 and 1.2.** The DISPERSED verdict there comes from two ball starts in one box, and those points were not box-checked; §3 does not ask for it. A lump reachable only from other starts, or only in a larger box, is not excluded.
- **Q_min beyond its brackets.** Nothing finer than the brackets, nor the λ position of the binding edge between 1.0 and 1.1, nor whether it coincides with the window's edge (V3) more finely than the grid spacing 0.1.
- **The shared mechanism itself.** TRACKS is a coincidence of two sets on a 5-point λ grid. That the same attraction drives both is the preregistered interpretation of TRACKS, not something QB measures.
- **Stability.** Dynamic or 3D (non-axisymmetric) stability of the lumps, or of anything else, is not tested; the instrument is static and axisymmetric.
- **The status of λ = 0.9, Q = 800** (localized, E/(mQ) = 1.0006): whether it is a metastable lump or a box artefact (§3, deviation 7).
- **Any physical identification.** The charge is the SU(3)_{C+F} Noether charge, not electric charge, and all quantities are in model units.
