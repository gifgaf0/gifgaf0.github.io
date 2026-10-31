# E9 option 4, Phase 1 (axisymmetric loop at b3_d1): report

October 31, 2026. **Label: Exploration, post-hoc selection** (`PREREG_option4.md` §9, Amendment A, commit da06bb3).

**Rules followed.**
- The model is §1.1–§1.2. The setup is §3 as amended by §9.3, and the verdict rules are §5 as amended by §9.4.
- The ψ sector is unchanged: κ = 2 (e = 1/√12), η = 0.1.
- The σ sector is at b3_d1 only:
  - β = 3
  - μ² = 5.02498614657458 (= ε₀(3) + 1)
  - λ = 8.695070858562827
  - m_vac = 2.2079433537628224
  - These are the exact values in `phase0_results.json`.
- Only n = 7 and n = 10 were run (§9.7). There is no Phase 2 and no 3D.
- `PREREG_option4.md`, `PREREG.md`, `gl3.py`, `option4_design.py` and `option4_phase0.py` are unmodified.

**Units.** Model units only (`gl3.py` coordinates, ξ = 1/√2, so 2ξ = 1.41).
- E is the energy above the true vacuum (|ψ_k|² = 1 + η, σ = 0) on the same grid.
- n and Q are the σ winding and the U(1)_σ charge. They are not spin or electric charge (§6).
- No particle identification is made.

## Summary

| | Result |
|---|---|
| P1 (C-a: n = 0, Q = 0 collapses) | **Holds.** The ring collapses to the vacuum: E = 4 × 10⁻⁹, I = 2 × 10⁻¹¹, no winding left. The instrument check passes. |
| Main, n = 7 (Q = 2889.19) | Both starts (R₀ = 8.595 and 12.892) stop at the same state: R_f = 8.25 (ψ winding zero), E = 5462.021, ω/m_vac = 0.650, leak 3 × 10⁻¹⁵, E/(m_vac Q) = 0.856. **STABLE (axisymmetric).** |
| Main, n = 10 (Q = 4127.42) | Both starts (R₀ = 12.278 and 18.418) stop at the same state: R_f = 12.00, E = 7804.510, ω/m_vac = 0.648, leak 6 × 10⁻¹⁵, E/(m_vac Q) = 0.856. **STABLE (axisymmetric).** |
| C-d (no ψ winding) | **STABLE** at both n (single-run P2 arms). It is a σ ring with no vortex, at **lower** energy than the main ring: E_C-d − E_main = −297.99 (n = 7) and −432.54 (n = 10). |
| **§9.4 verdict** | **STABLE, string not required**, at n = 7 and at n = 10. Not n-dependent. |
| C-e qualifier | **Metastable** at both n: E − E_lump = +1667.71 (n = 7) and +2605.98 (n = 10). |
| P3 (R_f vs thin-ring R_eq, 25 %) | **Holds** at both n: R_f/R_eq − 1 = −4.0 % (n = 7) and −2.3 % (n = 10). |
| P5 (descriptive) | C-b (n = 7, Q = 0) collapses to the vacuum. C-c (n = 0, Q = 2889.19) collapses onto the axis and ends in the same charged lump as C-e (E equal to 3 × 10⁻⁸). |
| Phase 2 | **Does not run.** §9.4 runs Phase 2 only on STABLE, string-supported. A "string not required" result closes option 4 as far as the E9 string is concerned. |

**Read this before the summary.** The fixed-(n, Q) σ condensate holds a ring open at the Phase 0 thin-ring radius. This is the §9.1 suspicion: the ring is held by the pressure of a charged σ domain. The E9 three-strand vortex threading the tube is not needed, and it costs energy:
- The same n and Q with the vortex removed relaxes to a slightly larger ring.
- That ring is lower in energy by about 5 %.

Both rings are also above a charged σ lump at the same Q. They are held against it only by n.

## 1. Commands run

```
cd seed/experiments/E9_three_strand_closure
git checkout claude/seed-step3-first-closure          # at da06bb3 (Amendment A)
pip install scipy                                     # not present in the container (deviation 1)
python3 axial_vorton.py gradcheck                     # > log_phase1_gradcheck.txt, phase1_gradcheck.json
python3 axial_vorton.py profiles                      # > log_phase1_profiles.txt, phase1_profiles.json
nohup python3 axial_vorton.py run > log_phase1.txt 2>&1 &   # all 11 runs, 4 in parallel; 157 s wall
python3 phase1_verdicts.py                            # > log_phase1_verdicts.txt; adds 'verdicts' to phase1_results.json
```

Before the official commands, two diagnostics were run with inline `python3 -c` calls. Neither wrote any output file:
- An ε sweep of the gradient check (deviation 2).
- A one-off evaluation of the 11 start states and of the A orientation (§3).

## 2. Software, hardware, minimizer

- Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (installed with pip). Linux container, 4 cores (Intel Xeon 2.1 GHz), 15 GB RAM. `OMP_NUM_THREADS=1`, with one worker per run and 4 in parallel.
- **Grid.**
  - Sites: ρ_i = (i + ½)h for i = 0…127, so ρ ∈ [0.125, 31.875]. z_j = −32 + jh for j = 0…256. h = 0.25.
  - That is 128 × 257 sites and 328 575 real unknowns: 3 complex ψ, complex σ, A_ρ and A_z.
  - Weights: 2πρh² on sites and z-links. 2πρ_{i+½}h² on ρ-links and plaquettes, with ρ_{i+½} = (i + 1)h.
- **Lattice.** As in `gl3.py`:
  - Non-compact links.
  - Covariant difference (e^{−iehA}ψ(x + μ) − ψ(x))/h.
  - Open boundaries. The face at ρ = 0 has zero weight, so no axis condition is imposed or needed.
  - σ is neutral (plain differences) with the e^{inφ} factor removed. n enters as n²|σ|²/ρ².
- **Minimizer.**
  - L-BFGS-B with `gl3.minimize`'s options: gtol = 10⁻⁵, ftol = 10⁻¹³, maxfun = 2·maxiter.
  - maxiter = 50 000, chosen before any run (deviation 3).
  - No run came near maxiter: the largest was 1272 iterations. Stop messages are in the table in §4.
- **Run time.** 35–77 s per run, 157 s in total.

## 3. Checks

**Gradient check** (`phase1_gradcheck.json`). The random state is gl3-style: normal × 0.5 on every unknown, at n = 7 and Q = 2889. The error is |fd − g|/(|fd| + 10⁻⁸) over 40 random coordinates. For the term-only checks the coordinates are drawn among those where that term's gradient is non-zero.

| grid | stencil | full functional | n²\|σ\|²/ρ² only | Q²/(4I) only |
|---|---|---|---|---|
| 8 × 9 (703 unknowns) | gl3 definition: central, ε = 10⁻⁶ | 3.4 × 10⁻⁵ | 4.2 × 10⁻⁸ | 1.1 × 10⁻⁷ |
| 8 × 9 | 5-point, ε = 10⁻³ | **7.2 × 10⁻⁹** | **9.3 × 10⁻¹¹** | **1.4 × 10⁻¹⁰** |
| 128 × 257 (full) | gl3 definition: central, ε = 10⁻⁶ | 4.6 × 10⁻⁴ | 3.2 × 10⁻⁴ | 1.1 × 10⁻⁴ |
| 128 × 257 | 5-point, ε = 10⁻³ | **4.8 × 10⁻⁷** | **2.9 × 10⁻⁷** | **1.3 × 10⁻⁷** |

**The gl3-definition check does not reach the expected ≲ 10⁻⁶.**
- **Why.** The error is floating-point cancellation, not a gradient error. On a random state E is large: Q²/(4I) is about 10⁶ on the small grid, and the n²/ρ² weight is about 3000 at ρ = h/2.
- **Diagnostic ε sweep** (not saved). The error falls as ε grows, which is the signature of roundoff, not of truncation:
  - Small grid, full functional: 3.4 × 10⁻⁵ at ε = 10⁻⁶, 4.7 × 10⁻⁷ at 10⁻⁵, 2.7 × 10⁻⁷ at 10⁻⁴.
  - Full grid: 4.6 × 10⁻⁴, 3.1 × 10⁻⁵, 5.0 × 10⁻⁶, 5.5 × 10⁻⁷ at ε = 10⁻⁶ … 10⁻³.
  - Every term checked alone behaves the same way.
- **What I added.** A five-point stencil (truncation O(ε⁴)) at ε = 10⁻³. It gives 7 × 10⁻⁹ on the small grid and 5 × 10⁻⁷ on the full grid, with the n²/ρ² and Q²/(4I) terms at ≤ 3 × 10⁻⁷. I take the gradient as correct.
- The stencil is my addition (deviation 2).

**Straight-string profile** (`phase1_profiles.json`, `log_phase1_profiles.txt`).
- **Solve.** `option4_phase0.solve_line` at b3_d1 with k* = 0.8144323693283151 and q* = 53.5. These are the exact values of the sign change selected by the §9.2 rule, which `axial_vorton.selected()` re-applies to `phase0_results.json` and which returns b3_d1. Warm start: Phase 0's first-solve start, the bare string plus 0.6 e^{−r²/2}.
- **Result.** Converged (FACTR) in 6069 iterations, max|∇| = 2.4 × 10⁻⁵:
  - ℰ = 101.206, I = 18.746, σ(0) = 0.855
  - ω = 1.42694 (ω/m_vac = 0.6463)
  - r_σ = 2.7986, r_ψ = 3.379
  - 𝒯_virial = −0.006
- **Agreement with Phase 0.** Its interpolated values were ω*/m_vac = 0.6463 and r_σ* = 2.7986. The neighbouring Phase 0 grid solves (0.80, 53.5) and (0.85, 53.5) bracket ℰ, I and r_ψ.

**Starts.** The A orientation was checked on the n = 7, R₀ = R_eq start:

| A in the start | E |
|---|---|
| +A (as built) | 5488.9 |
| −A | 15609.5 |
| A = 0 | 8019.5 |

So A = a(d)/(e d) χ̂, with χ = atan2(z, ρ − R₀), is the orientation consistent with ψ = f e^{iχ}. The start energy 5488.9 is close to the thin-ring value 2πR_eq ℰ = 5465.5. Every wound start has exactly one winding zero per strand at the intended core.

## 4. All 11 runs (final states)

Column meanings:
- **ψ zeros.** Gauge-invariant plaquette winding of each strand, given as the plaquette centre (resolution ±h/2).
- **R_σ.** ∫ρ|σ|²/∫|σ|² with the 3D measure.
- **r_σ, r_ψ.** Equivalent-area radii in the (ρ, z) plane of the regions |σ|² > ½ max|σ|² and mean_k|ψ_k|² < ½(1 + η).
- **ω²<m²+k².** k = n/R_f; for n = 0, k = 0.
- **leak.** The fraction of I with ρ > 28 or |z| > 28.
- **stop.** FACTR is `CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH`. PGTOL is `CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL`.

| run | n | Q | start R₀ | E | E/(m_vac Q) | ψ zeros (ρ, z) | R_σ | r_σ | r_ψ | I | ω/m_vac | ω²<m²+k² | leak | it | stop | final max\|∇\| |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| main_n7_R1.0 | 7 | 2889.19 | 8.595 | 5462.021 | 0.856 | 3 × (8.25, +0.125) | 9.057 | 2.77 | 3.36 | 1007.33 | 0.6495 | yes | 3 × 10⁻¹⁵ | 689 | FACTR | 1.4 × 10⁻⁵ |
| main_n7_R1.5 | 7 | 2889.19 | 12.892 | 5462.021 | 0.856 | 3 × (8.25, −0.125) | 9.057 | 2.77 | 3.36 | 1007.33 | 0.6495 | yes | 6 × 10⁻¹⁵ | 883 | FACTR | 1.8 × 10⁻⁵ |
| main_n10_R1.0 | 10 | 4127.42 | 12.278 | 7804.510 | 0.856 | 3 × (12.00, −0.125) | 12.620 | 2.79 | 3.36 | 1443.16 | 0.6477 | yes | 6 × 10⁻¹⁵ | 606 | FACTR | 1.3 × 10⁻⁴ |
| main_n10_R1.5 | 10 | 4127.42 | 18.418 | 7804.510 | 0.856 | 3 × (12.00, −0.125) | 12.620 | 2.79 | 3.36 | 1443.16 | 0.6477 | yes | 4 × 10⁻¹⁵ | 854 | FACTR | 2.4 × 10⁻⁵ |
| C-a (Ca_n0_Q0) | 0 | 0 | 8.595 | 4 × 10⁻⁹ | — | none | — | — | 0 | 2 × 10⁻¹¹ | — | — | n/a | 1007 | PGTOL | 8.9 × 10⁻⁶ |
| C-b (Cb_n7_Q0) | 7 | 0 | 8.595 | 4 × 10⁻⁹ | — | none | — | — | 0 | 9 × 10⁻¹² | — | — | n/a | 1014 | PGTOL | 9.1 × 10⁻⁶ |
| C-c (Cc_n0_Q7) | 0 | 2889.19 | 8.595 | 3794.311 | 0.595 | none | 4.465 | 5.24* | 5.65* | 1249.90 | 0.5235 | yes | 1 × 10⁻¹⁴ | 1272 | FACTR | 1.2 × 10⁻⁴ |
| C-d (Cd_n7) | 7 | 2889.19 | 8.595 | 5164.034 | 0.810 | none | 10.742 | 2.46 | 2.98 | 977.23 | 0.6695 | yes | 2 × 10⁻¹⁵ | 590 | FACTR | 1.6 × 10⁻⁵ |
| C-d (Cd_n10) | 10 | 4127.42 | 12.278 | 7371.974 | 0.809 | none | 15.066 | 2.44 | 2.95 | 1397.75 | 0.6687 | yes | 4 × 10⁻¹⁵ | 575 | FACTR | 2.5 × 10⁻⁵ |
| C-e (Ce_Q7) | 0 | 2889.19 | ball | 3794.311 | 0.595 | none | 4.465 | 5.24* | 5.65* | 1249.90 | 0.5235 | yes | 5 × 10⁻¹⁵ | 901 | FACTR | 1.4 × 10⁻⁴ |
| C-e (Ce_Q10) | 0 | 4127.42 | ball | 5198.531 | 0.570 | none | 5.088 | 6.00* | 6.41* | 1850.14 | 0.5052 | yes | 1 × 10⁻¹⁴ | 984 | FACTR | 1.4 × 10⁻⁴ |

Notes on the table:
- m_vac Q = 6379.2 (n = 7) and 9113.1 (n = 10).
- ω = Q/(2I) = 1.4341 (main n = 7), 1.4300 (main n = 10), 1.4783 and 1.4765 (C-d), 1.1558 (C-c and C-e at Q₇) and 1.1154 (C-e at Q₁₀).
- **\*** For the lumps on the axis (C-c, C-e), the area-equivalent radius is measured on a half-disk in the (ρ, z) plane. It is a factor √2 below the lump's 3D half-radius. These entries are descriptive only.
- **leak n/a.** With I ≈ 10⁻¹¹ the leak fraction is a ratio of roundoff-level numbers (4.6 × 10⁻² and 9.4 × 10⁻² as computed). σ is gone.
- **The two starts at each n reach the same state:**
  - E agrees to 9 × 10⁻¹⁰ (n = 7) and 5 × 10⁻⁹ (n = 10).
  - R_σ agrees to 10⁻⁵ and I to 5 × 10⁻⁴.
  - The ψ zeros sit at the same ρ in mirror plaquettes z = ±0.125. The core is on z = 0, between plaquette rows.
- **C-c and C-e at Q = 2889.19 reach the same lump.** E agrees to 3 × 10⁻⁸.
- Per-strand zeros coincide in every wound run: the three strands stay merged.
- The thin-ring estimate 2πR_eq ℰ(k*, q*) is 5465.5 (n = 7) and 7807.9 (n = 10). The ring energies are 5462.0 and 7804.5.

**Histories** (every 50 iterations in `phase1_results.json`; console copy in `log_phase1.txt`):
- **Main runs.**
  - The 1.5 R_eq starts contract monotonically. At n = 7, R_core goes 13.0 → 12.25 → 10.75 → 9.25 → 8.5 → 8.25 at iterations 0, 50, 100, 150, 200 and 250, then holds at 8.25. E falls monotonically from 5924.7 to 5462.02.
  - The R_eq starts move inward slightly, to 8.25 and 12.00.
  - The winding zeros are present, one per strand, at every recorded iteration.
- **C-d.** The σ ring drifts outward: R_σ goes 8.90 → 9.29 → 10.16 → 10.49 → 10.74 (n = 7). No ψ zero appears at any recorded iteration. The ψ depletion inside the σ tube reaches mean|ψ|² = 0.034 at the minimum, so it never reaches zero.
- **C-c.** The wound ring contracts to the axis: R_core goes 8.5 → 8.0 → 5.0 → 3.25 → 2.0 over iterations 0–200. Zeros then appear and disappear near the axis inside the σ lump, where ψ ≈ 0 and the phase is ill-defined (iterations 200–650). From iteration 650 to the end there are none.
- **C-a and C-b.** σ decays (I → 0 by iteration ~300) and the ring shrinks to the vacuum.

Final fields are saved as `phase1_<run>.npz` (compressed, 0.6–1.8 MB each; none exceeds 20 MB). Each holds ψ, σ, A_ρ, A_z, ρ, z, n, Q, β, μ², λ and h.

## 5. Verdicts (§5 P1–P2, as amended by §9.4)

Applied by `phase1_verdicts.py` (`log_phase1_verdicts.txt`). The definitions used are listed in §8.

**P1.** C-a ends in the vacuum: E = 4.3 × 10⁻⁹, I = 2.0 × 10⁻¹¹, no winding. **Holds.** The instrument check passes, so the run continues.

**P2, per main run:**

| n | start R₀ = R_eq | start R₀ = 1.5 R_eq | same R_f within 10 % | R_f > 1.41 | ω < m_vac | leak < 1 % | E < m_vac Q | main verdict |
|---|---|---|---|---|---|---|---|---|
| 7 | R_f = 8.25 | R_f = 8.25 | yes (0 %) | yes | yes (0.650) | yes | yes (0.856) | **STABLE (axisymmetric)** |
| 10 | R_f = 12.00 | R_f = 12.00 | yes (0 %) | yes | yes (0.648) | yes | yes (0.856) | **STABLE (axisymmetric)** |

**C-d qualifier (§9.4).** C-d ends as a σ ring at both n:
- σ is maximal off the axis: |σ|max = 0.857 at (ρ, z) = (10.625, 0) for n = 7 and (14.875, 0) for n = 10.
- R_σ = 10.74 and 15.07. No ψ winding anywhere.
- ω/m_vac = 0.670 and 0.669, leak ~10⁻¹⁵, E/(m_vac Q) = 0.810 and 0.809.

These pass every single-run P2 condition, so C-d is **STABLE** at both n.

| n | main | C-d | E_C-d − E_main | **verdict** |
|---|---|---|---|---|
| 7 | STABLE | STABLE | −297.99 | **STABLE, string not required** |
| 10 | STABLE | STABLE | −432.54 | **STABLE, string not required** |

**C-e qualifier.** E_lump < E at both n, so the ring is **metastable**: it is held only by n against decay into a charged lump.

| n | E (main) | E_lump | E − E_lump | E_C-d − E_lump |
|---|---|---|---|---|
| 7 | 5462.02 | 3794.31 | +1667.71 | +1369.72 |
| 10 | 7804.51 | 5198.53 | +2605.98 | +2173.44 |

**n-dependence (§9.4).** Same verdict at n = 7 and n = 10. The result carried forward (n = 10) is **STABLE, string not required; metastable**.

**Phase 2.** §9.4 runs Phase 2 only on STABLE, string-supported. **It does not run.** Per §9.4, this result closes option 4 as far as the E9 string is concerned. Any study of σ alone would need a new pre-registration.

## 6. P3 (thin-ring check)

| n | R_eq = n/k* | R_f (ψ zero) | R_f/R_eq − 1 | R_σ | R_σ/R_eq − 1 | within 25 % |
|---|---|---|---|---|---|---|
| 7 | 8.595 | 8.25 | −4.0 % | 9.057 | +5.4 % | **yes** |
| 10 | 12.278 | 12.00 | −2.3 % | 12.620 | +2.8 % | **yes** |

- P3 holds at both n. The thin-ring picture of Phase 0 locates the axisymmetric ring well. The agreement improves at the thinner n = 10 ring, as expected.
- The σ tube sits slightly outside the ψ zero: R_σ − R_f = 0.81 (n = 7) and 0.62 (n = 10).
- The final ω/m_vac (0.650, 0.648) matches the straight-string ω*/m_vac = 0.646. r_σ (2.77, 2.79) matches r_σ* = 2.80, and r_ψ (3.36) matches 3.38.
- P3 is descriptive and tests the thin-ring proxy only. The C-d result shows the same proxy says nothing about whether the vortex is needed.

## 7. P5 (descriptive)

- **C-b** (n = 7, Q = 0). The current alone does not hold the ring. σ decays to zero, the ring collapses, and the end state is the vacuum (E = 4 × 10⁻⁹).
- **C-c** (n = 0, Q = 2889.19). The charge alone does not hold a ring. The wound ring contracts through the axis, the ψ winding annihilates there, and σ collects into a charged lump on the axis: E = 3794.31, ω/m_vac = 0.523, R_σ = 4.47. This is the same state C-e reaches from the ball start.

Both fail alone, as the prior art suggested (§5 P5). Charge plus current together hold the ring: the main runs, and C-d without the vortex.

## 8. Deviations and readings, collected

**Deviations.**
1. **SciPy installed with pip.** It was not present in the container.
2. **Gradient check.**
   - The gl3-definition check (central difference, ε = 10⁻⁶) gives 3.4 × 10⁻⁵ (small grid) and 4.6 × 10⁻⁴ (full grid), above the expected ≲ 10⁻⁶. The ε sweep in §3 shows this is roundoff.
   - I added a five-point stencil at ε = 10⁻³, reported alongside: 7 × 10⁻⁹ and 5 × 10⁻⁷.
   - The check also ran on a small 8 × 9 grid as well as on the full grid.
3. **maxiter = 50 000.** Neither `gl3.py` (default 3000) nor the pre-registration fixes it for Phase 1.
   - I first wrote 30 000 into the script and raised it to 50 000 before launching any run. No run had been made with either value.
   - The other options are gl3's: gtol = 10⁻⁵, ftol = 10⁻¹³, maxfun = 2·maxiter.
   - No run came near maxiter (largest 1272).
4. **Minimized function is E − E_vac.** This is a constant shift and leaves the gradient and minimizer path unchanged. It does change the scale of the FACTR test, which is relative to |f|: about 5 × 10³ here instead of about 6 × 10⁴ for the total. The stop is therefore about 12× stricter than on the total energy.
5. **9 of 11 runs stopped on FACTR, not PGTOL.**
   - Their final max|∇| is 1.4 × 10⁻⁵ to 1.4 × 10⁻⁴, above gtol = 10⁻⁵.
   - Per the instructions, these were recorded and not extended.
   - Evidence that the end states are stationary: the pairs of independent starts agree in E to ≤ 5 × 10⁻⁹ (main runs) and 3 × 10⁻⁸ (C-c vs C-e), and the recorded histories are flat over the last 300+ iterations.
6. **Straight-string warm start.** The profile was regenerated from Phase 0's first-solve warm start (bare string + 0.6 e^{−r²/2}), directly at (k*, q*), not by Phase 0's chain of neighbour warm starts. It reproduces Phase 0's interpolated ω* and r_σ* (§3).
7. **Start construction details I had to decide.**
   - f, a and s are linearly interpolated from the dr = 0.04 radial grid. Beyond d = 24 (the radial box) they are set to the vacuum: f = √(1 + η), a = 1, s = 0.
   - A is evaluated at link midpoints.
   - χ = atan2(z, ρ − R₀), counter-clockwise in (ρ, z), as in `gl3.ring_phase`.
   - The σ start is real.
8. **Q values.** Computed as 2π(n/k*)q* from the exact JSON values: Q₇ = 2889.1937 and Q₁₀ = 4127.4196.
   - The task and the §9.2 table give 4127.6 for n = 10, which is what the rounded k* = 0.8144 gives. The exact value was used, as the task instructs.
   - The start radii are R_eq = 8.5949 and 12.2785, and 1.5 R_eq = 12.8924 and 18.4177.
9. **Q²/(4I) uses site values of |σ|².** Phase 0 used midpoint values on its radial grid. This difference is inherent to the 2D lattice.
10. **Extra files.**
    - `phase1_verdicts.py`: read-only; it applies §5/§9.4 and adds a `verdicts` block to `phase1_results.json`.
    - `phase1_gradcheck.json`.
    - `log_phase1_gradcheck.txt`, `log_phase1_profiles.txt` and `log_phase1_verdicts.txt`.
11. **Runs executed 4 in parallel.** This does not affect the deterministic L-BFGS-B paths.
12. **Branch.** The work was committed to `claude/seed-step3-first-closure`, as the task specifies.

**Ambiguities, flagged for the author.** Each was resolved by the most literal reading I could find.
- **(a) R_f.**
  - For main runs I took R_f as the ρ of the ψ winding zero (the composite core), at plaquette resolution ±h/2.
  - The σ-weighted radius is reported alongside. Using it instead changes no verdict: it gives 9.06 vs 9.06 and 12.62 vs 12.62, and P3 = +5.4 % and +2.8 %.
- **(b) "Within 10 %"** was read as |R₁ − R₂|/mean ≤ 0.10. It is moot here (0 %).
- **(c) C-d is a single run.** §9.4's table needs a C-d verdict, but §9.3 gives one start.
  - I applied the P2 arms without the two-start test, with R_f = the σ-weighted radius, since there is no ψ zero by construction.
  - Every margin is wide: R_σ = 10.7 and 15.1, ω/m_vac = 0.67, leak ~10⁻¹⁵, E/(m_vac Q) = 0.81.
- **(d) Control starts C-a, C-b and C-c.** §9.3 says "σ start as above". I used the n = 7 wound start at R₀ = R_eq(n = 7) = 8.595 (ψ wound, A, σ = s(d)), with only n and Q changed.
- **(e) C-e start.**
  - "No ψ winding" was read as ψ_k = √(1 + η) everywhere (the vacuum), A = 0.
  - The ball was read as a sharp step: σ = √(μ²/λ) for √(ρ² + z²) < 4, else 0.
- **(f) Leak band.** "Within 4 units of any box edge" was taken as ρ > 28 or |z| > 28. The axis ρ = 0 is a symmetry axis, not a box edge, and is excluded. Counting it would make every on-axis lump "leak".
- **(g) r_σ and r_ψ in 2D.** These are equivalent-area radii in the (ρ, z) plane. For the tubes they match Phase 0's radial definition; for the on-axis lumps they are √2 low (§4).
- **(h) FACTR stop with max|∇| > gtol** is taken as the end state (deviation 5).

No parameter, point or n outside §9 was used. The ψ sector was not touched. No term was added to the energy beyond §1.1–§1.2. `PREREG_option4.md`, `PREREG.md`, `gl3.py`, `option4_design.py` and `option4_phase0.py` are unmodified.

## 9. What is and is not established

**Established** (axisymmetric, b3_d1, h = 0.25, one 32 × 64 box):
- At fixed (n, Q) = (7, 2889.19) and (10, 4127.42) there is a stationary charged, current-carrying ring threaded by the merged three-strand vortex.
  - It is reached from two starts at each n.
  - Its radius is within 4 % of the Phase 0 thin-ring R_eq.
  - ω/m_vac = 0.65, σ is localized (leak ~10⁻¹⁵), and E = 0.856 m_vac Q.
- **The vortex is not what holds the ring.** With the vortex removed (C-d), the same n and Q give a σ ring that is stationary, localized and **lower** in energy by 298 (n = 7) and 433 (n = 10). The σ-phase domain, which is metastable at this point (§9.1), carries the ring by itself. The E9 string is a passenger that costs energy. By §9.4, this closes option 4 as far as the E9 string is concerned.
- Both rings are metastable against a charged σ lump at the same Q. That lump is lower by 1668 / 2606 (wound) and 1370 / 2173 (unwound).
- Charge alone (C-c) and current alone (C-b) each fail to hold a ring.

**Not established:**
- **Anything about 3D stability.** An axisymmetric STABLE says nothing about:
  - pinching or other non-axisymmetric deformations (m = 2, 3);
  - phase slips that change n;
  - whether n protects the ring against the lump in 3D.

  These are Phase 2 questions, and Phase 2 does not run under §9.4.
- **Grid and box independence.** There was one grid (h = 0.25) and one box. The pre-registration did not ask for a Phase 1 resolution or box check, and none was run. All states sit well inside the box (leak ~10⁻¹⁵, R + r_ψ ≲ 19 < 28), but resolution effects at the 1 % level are not bounded.
- **That these are the lowest states.** L-BFGS finds local minima. For example, whether the wound ring can reach the lower unwound ring was not tested. In the axisymmetric reduction the ψ zero can only leave through the axis or to infinity.
- **Dynamics.** Minimizer iterations are not a time evolution.
- **Robustness of the selection.** The point (b3_d1) and the two n values were selected post hoc (§9). No other point or n was run (§9.7).
- **No statement about the thirds, and no particle identification.** n and Q are σ labels in model units.

## 10. Files committed

- **Code:**
  - `axial_vorton.py`: the instrument, gradient check, profile generation and runs.
  - `phase1_verdicts.py`: verdict application, read-only on the run data.
- **Data:**
  - `phase1_profiles.json`: the straight-string f, a, s on the radial grid, plus the solve record and the selection.
  - `phase1_results.json`: per-run spec, stop message, iterations, final observables, history every 50 iterations, and the `verdicts` block.
  - `phase1_gradcheck.json`.
- **Logs:** `log_phase1.txt`, `log_phase1_gradcheck.txt`, `log_phase1_profiles.txt` and `log_phase1_verdicts.txt`.
- **Final fields:** `phase1_main_n7_R1.0.npz`, `phase1_main_n7_R1.5.npz`, `phase1_main_n10_R1.0.npz`, `phase1_main_n10_R1.5.npz`, `phase1_Ca_n0_Q0.npz`, `phase1_Cb_n7_Q0.npz`, `phase1_Cc_n0_Q7.npz`, `phase1_Cd_n7.npz`, `phase1_Cd_n10.npz`, `phase1_Ce_Q7.npz` and `phase1_Ce_Q10.npz`. They total about 15 MB, and none exceeds 20 MB.
