# E2 reconciliation

**Inputs**

- The original run: `REPORT.md`, `results.json` and the scripts in `seed/experiments/E2_skyrme_su3/`.
- The independent cross-check: `crosscheck/crosscheck.json` and the `xc_*.py` scripts. Its verdict was "confirmed_with_corrections": all numbers agree, all its own checks pass, and it raised 8 issues, all minor.

**Method**

- Read both codes for every issue.
- Re-read the cited literature myself: converted the arXiv PDFs with pdftotext into scratch, outside the repo.
- Queried PDG 2026 with the `pdg` package.
- Fixed the original scripts, reran the full pipeline, and checked that it reproduces itself.

## Issues

| # | issue (from the cross-check) | which side is right | diagnosis | action | resolved |
|---|---|---|---|---|---|
| 1 | Verdict vocabulary: N_c parity, Derrick, virial and von Laue labelled CALIBRATED; identities treated as calibrations | cross-check | PLAN §1 reserves CALIBRATED for literature targets. N_c parity (SEED §2) and Derrick (SEED §4) are seed claims; virial and von Laue are internal checks with preregistered tolerances. The ordering and E(10)−E(8), E(10̄)−E(8) are exact literature targets in PLAN ([read: DPP]), so CALIBRATED is formally right for them, but they are algebraic consequences of the rotor formula | `collect_results.py`: N_c parity → CONFIRMED (given the imported WZ rule); Derrick → CONFIRMED; virial and von Laue → PASS (defined as an internal check, which is not a PLAN word). Ordering and level differences stay CALIBRATED, with the note "tests the irrep/Casimir code; the order depends only on I₁/I₂, so the two sets are one test". "e is the only pure number" stays CONFIRMED, flagged as true by construction. No numbers changed | yes |
| 2 | The corrected 30% reading ("most static properties within about 30%") is not shown by E2 | cross-check | The only non-fit nucleon static observable E2 computes is g_A (−52%). F_pi is an output only if the masses are taken as inputs. Radii and moments are E5's test | AMENDED kept on the g_A evidence alone. The "most static properties" clause is withdrawn, and E2 makes no claim about radii or moments. F_pi (−30.5%) is kept as context only | yes |
| 3 | Target provenance: "36.5 F_pi/e = 1.2315 × 3π²" is not in the cited [read] texts; ANW numbers readable in Acus et al. | cross-check | Verified by converting the PDFs: see "Literature checked" below. 36.5 and 50.9 are ANW's own values; 1.2315 × 3π² is the standard E/(12π²) and was not read here | Source strings in `results.json` and the report corrected. M_cl is checked against all three versions and passes each: −0.004% vs 36.463, −0.11% vs 36.5, +0.053% vs 36.44. Λ is +0.16% vs 50.90. ANW F_pi, e and g_A upgraded to [read: Acus Table 1]. PLAN.md is outside this directory and was not edited; its overstated [read] label is flagged for the series summary | yes |
| 4 | The I₂ calibration target is a variational (arctan-ansatz) value | cross-check | A weak calibration: it only excludes formula slips above 1.5%. The density is independently verified on both sides: SU(3) matrices 5e-15, finite differences 7e-11 | Stated in the calibration table and in `results.json`. Verdict unchanged: CALIBRATED, +0.33% vs the recomputed 40.5435 | yes |
| 5 | `collect_results.py` hard-codes CALIBRATED; the multiplet ordering is printed but not asserted | cross-check | Correct: a regression would not have flipped those verdicts | `su3_rotor.py` gets a new check: the lowest six Y_R = 1 levels equal 8(½), 10(3/2), 10̄(½), 27(3/2), 35(5/2), 27(½) at both parameter sets (PASS). `collect_results.py` now derives every exact or qualitative verdict from asserted checks via `from_check(...)` | yes |
| 6 | PDG 2026 g_A quoted as 1.2754 | cross-check | pdg 2026.0, S017AV: λ = g_A/g_V = −1.275335 ± 0.001263, displayed as −1.2753 ± 0.0013. 1.2754 is the 2024 value | `su3_rotor.py` reads g_A/g_V from the pdg package (with a fallback table holding the same value) into `rotor.json`; `collect_results.py` uses it. All text quotes 1.2753(13). −52% unchanged | yes |
| 7 | (1,3) written "24" at N_c = 4 and 7 | cross-check | `irrep_name()` had no (3,1) or (1,3) entry and printed "24(1,3)"; the report dropped the bar | Added (3,1) → 24 and (1,3) → 24bar. Table and notes corrected; the N_c = 7 lowest state is 24̄(½) | yes |
| 8a | Pressure node 2.1522 is a grid-interval midpoint | cross-check | Correct: the midpoint of a 0.001-wide interval | `derrick_virial.py` uses brentq: x = 2.1523728647, agreeing with the cross-check (2.1523728647) to 1e-13. p(0) now from the exact −a²/8 + a⁴/2 = 0.381628, with a = −F′(0). The cross-check's 0.3816277 was evaluated at x = 1e-3 | yes |
| 8b | Asymptotic residuals "6e-7, 2e-9, 5e-10" are relative; x = 40 value called solver noise | partly cross-check | They are relative (now stated). But the x = 40 value was not solver noise: it was the 4.5e-10 error of C (8d) | After the C fix: 6.0e-7, 1.4e-9 and 4.3e-12 at x = 10, 20, 40, matching the cross-check's remainder estimate (~5e-12). Noted that C is now taken at x = 100 with the same series, so the x = 40 value is a consistency check | yes |
| 8c | "E₂ = E₄ to 6e-13" vs "4e-13" in different places | neither is wrong | Two genuine numbers: −4.4e-13 (reference solution, `skyrme_hedgehog.py`) and +5.6e-13 (independent quadrature, `derrick_virial.py`) | Both quoted wherever the virial result appears | yes |
| 8d | The report's "−2C = −17.2771564357" does not match the `results.json` C; the original C is good only to 4.5e-10 | cross-check | Root cause: `solve_mapped` took C = 2L²F_tt(t = 1), a second spectral derivative at the end point. Its error is ~5e-10 and noisy in N: −4.5e-10 at N = 160, +7.5e-10 at N = 200. D = bulk + C inherited it (2.3e-10). `verify_densities.py`'s own N = 120 solve printed a third value | `skyrme_hedgehog.py` now sets C from the interpolated F(100) and the asymptotic series (`C_from_FX`, remainder ~1e-13), keeping the old estimate as a diagnostic. New check: D/(−2C) − 1 = −1.1e-12 (< 1e-11). See "Number changes" below | yes |

## Literature checked

All PDFs were converted fresh with pdftotext.

- **Schechter–Weigel, hep-ph/9907554 §2:**
  - "E = 23.2πf_π/e", which is 36.44 F_π/e.
  - "α² = 53.3/(e³f_π)", which gives Λ = 3 × 53.3/π = 50.90.
  - Neither "36.5" nor "1.2315" appears.
- **Praszalowicz, hep-ph/0308114 v1 and v3:** only the arctan formulas, eqs. 25–28, with x₀ = √(15/4). No 36.5, 1.2315 or 50.9.
- **Acus et al., hep-ph/9605435 Table 1, ANW column:** f_π = 64.5 MeV, e = 5.45, r₀ = 0.59 fm, μ_p = 1.87, μ_n = −1.31, g_A = 0.61.

## Number changes

| quantity | before | after | relative change | after vs cross-check |
|---|---|---|---|---|
| C | 8.63857821430118 | 8.63857821821941 | +4.5e-10 | 6.6e-13 |
| D | −17.277156440338604 | −17.277156436420377 | −2.3e-10 | 1.6e-13 |
| g_A (ANW fit) | 0.6104737139051 | 0.6104737137667 | −2.3e-10 | 6.0e-13 |
| pressure node x | 2.1522138 (midpoint) | 2.1523729 (root) | — | 1.3e-13 |
| p(0) | 0.381595 (at x = 0.01) | 0.381628 (exact) | — | — |

- The refit g_A values (0.65707, 0.45995) changed in the 10th digit.
- Λ, J₂, M, I₁/I₂ and every MeV number changed by ≤ 1e-14 relative.
- The N = 40 and N = 80 convergence rows of D, Λ and J₂ changed, because they also used the end-point C. The report table is updated.

## Files changed

All in `seed/experiments/E2_skyrme_su3/`.

- **Scripts:** `skyrme_hedgehog.py`, `su3_rotor.py`, `derrick_virial.py`, `collect_results.py`, `run_all.sh` (runtime comment only).
- **Regenerated by the rerun:** `results.json`, `profile.json` (only the C, Λ and J₂ header fields), `out/hedgehog.json`, `out/verify.json`, `out/rotor.json`, `out/derrick.json`, `out/run_all.log`.
- **Unchanged:** the figures are byte-identical to the committed ones, and `crosscheck/` was not touched.
- **Backup:** the originals are in the scratchpad at `e2rec/orig/`.

## Final consistency

- `run_all.sh` passes end to end (`all checks pass: True`, exit 0).
- A second full rerun gives a byte-identical `results.json`.
- The report's headline numbers, the `results.json` headline and seed claims, and the verdicts agree with each other.
- Verdicts:
  - **CALIBRATED:** M_cl, Λ, ANW F_π, ANW e, g_A, I₂ (flagged weak), lowest multiplets, E(10)−E(8), E(10̄)−E(8).
  - **PASS:** virial, von Laue.
  - **CONFIRMED:** Derrick, N_c parity (given the imported WZ rule).
  - **NO_TARGET, agrees:** the four expectations.
  - **Seed claims:** §2 CONFIRMED (given the WZ rule), §4 CONFIRMED, §6B octet/decuplet CONFIRMED, §6B degeneracy CONFIRMED, §6B "e only pure number" CONFIRMED (by construction), §6B 30% AMENDED (g_A −52%; other static properties left to E5).
- **Open items:** none.
- **Downstream:** E3's `make_results.py` compares against E2's `profile.json`. The stored C moved by 4.5e-10, which does not affect it.
