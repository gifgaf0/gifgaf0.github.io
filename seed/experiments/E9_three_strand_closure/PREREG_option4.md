# E9 option 4 pre-registration: a charged, current-carrying closure (vorton)

*Draft for the author, October 30, 2026. Label: Exploration. Written after the N = 1 rerun (`REPORT_N1_rerun.md`, both starts COLLAPSE) and before any option 4 loop is computed. Follows `PREREG.md` §6 (fallback), §9 (Amendment A) and §10 (Amendment B).*

## 0. Two things to settle before the test

### 0.1 The §6 trigger is not yet met

§6 opens option 4 "if COLLAPSE at both κ values and both η values". Only κ = 2, η = 0.1 has been run. The static N = 1 runs at κ = 1 and at η = 0 are still owed under `PREREG.md`. This pre-registration is written now at the author's request. It does not waive those runs. Whether to run or waive them is the author's call, and the decision should be recorded in the README.

### 0.2 Option 4 as worded in §6 is empty in the E9 model

§6 describes "a loop whose relative phase rotates in time at frequency ω, stabilized by the conserved charge". In the E9 model that object does not exist. The argument is short.

1. Take any stationary configuration ψ_k = f_k(x) e^{−iω_k t} with static A₀, A. Each component contributes (ω_k + eA₀)²|f_k|² to the energy density.
2. All three strands are condensed in the vacuum (|f_k|² → 1 + η far away). Finite energy then needs ω_k + eA₀(∞) = 0 for every k. Since A₀(∞) is one number, ω₁ = ω₂ = ω₃.
3. A common frequency is a gauge shift. So **every finite-energy stationary configuration of E9 is gauge-equivalent to a static one.** No relative phase can rotate without the rotation filling all of space.
4. Charge points the same way:
   - At η = 0 the relative U(1)s are spontaneously broken in the vacuum. Their charge cannot be localized, and it would radiate as the massless relative-phase mode.
   - At η > 0 the Josephson term breaks them explicitly. There is no conserved relative charge at all.

**Consequence.** A vorton needs a field that is zero in the vacuum and condensed only in the string core. This is Witten's σ: its charge and current are confined to the loop. E9 has no such field, so option 4 must add one. That is a change of model. It is declared as A3 below, not derived.

This connects to the rerun. Under the §10 rule, start B collapsed because "the twist has no protected place to live where all three amplitudes vanish". The σ field is a field whose natural home is exactly where all three amplitudes vanish. That is the motivation for A3. It is not a derivation of A3.

## 1. Model (declared inputs)

### 1.1 Energy

The E9 energy (`gl3.py`, unchanged) plus a neutral complex scalar σ:

E = Σ_k [ |Dψ_k|² + ½(|ψ_k|² − 1)² ] + ½(∇×A)² − η Σ_{i<j} Re(ψ_i ψ_j*)
  + |∂_tσ|² + |∇σ|² − μ²|σ|² + ½λ|σ|⁴ + β|σ|² Σ_k|ψ_k|²

- **ψ sector, unchanged:** κ = 2 (e = 1/√12), η = 0.1, ξ = 1/√2 in `gl3.py` coordinate units. The ψ_k are static, so their kinetic term plays no role.
- **A3 (declared, not derived).** A neutral core field σ exists. It has a global U(1)_σ, does not couple to A, and couples to the strands only through β|σ|²Σ|ψ_k|². A1 (interchangeable strands) is untouched, because σ couples to all three equally.
- **A4 (declared).** σ is relativistic: σ = s(x) e^{−iωt}, with Noether charge Q = 2ω∫|s|². The non-relativistic (Gross–Pitaevskii) version is out of scope and would need its own label.
- **Conserved labels:**
  - Q, the U(1)_σ charge.
  - n, the winding of σ's phase once around the loop (the current). n is protected only while |σ| ≠ 0 along the core; a phase slip can change it.

### 1.2 Method: minimum energy at fixed charge

With I = ∫|s|² and Q = 2ωI, the energy at fixed Q is

E_Q[ψ, A, s] = E_static[ψ, A, s] + Q²/(4I).

A local minimum of E_Q at fixed Q (and fixed n) is a stationary solution with ω = Q/(2I). It is stable against every perturbation that preserves Q and n. This is an unconstrained minimization, so it reuses the L-BFGS machinery of `gl3.py`. The extra term's gradient is −(Q²/4I²)·∂I.

### 1.3 Disclosure: what was computed before writing this

Script: `option4_design.py`. It treats a straight composite string only, all three strands winding once, radial ansatz, dr = 0.04. No loop was computed.

**Bare composite string (σ = 0):**
- Tension per coordinate length: T₀ = 27.80.
- Core radius where f² = ½(1 + η): 1.17.

**Bound-state eigenvalue.** ε₀(β) is the lowest m = 0 eigenvalue of −∇² + 3βf² on the bare string. σ condenses in the core when μ² > ε₀.

| β | 0.5 | 1 | 2 | 3 | 5 | 8 |
|---|---|---|---|---|---|---|
| ε₀ | 1.272 | 2.047 | 3.163 | 4.025 | 5.397 | 7.014 |

**Five trial points at k = ω = 0.**

| β | λ | μ² | m²_vac = 3β(1+η) − μ² | T | σ(0) | I_c = ∫\|s\|² d²x |
|---|---|---|---|---|---|---|
| 0.5 | 1 | 1.45 | 0.20 | 27.32 | 0.76 | 6.31 |
| 0.5 | 1 | 1.55 | 0.10 | 26.33 | 0.95 | 14.71 |
| 1 | 2 | 2.30 | 1.00 | 27.57 | 0.63 | 1.99 |
| 1 | 2 | 2.50 | 0.80 | 26.92 | 0.85 | 4.76 |
| 1 | 2 | 2.65 | 0.65 | 25.95 | 0.98 | 8.64 |

**What the trial points show.** A crude thin-ring balance (σ profile frozen) says a ring holds only if

k² + ω² ≈ T/I_c, with k = n/R.

Two conditions bound k and ω:
- σ must stay localized: ω < m_vac.
- The core condensate must survive the current: roughly k² − ω² < μ² − ε₀.

Together these give k² + ω² ≲ (μ² − ε₀) + 2m²_vac. At the point (β, λ, μ²) = (1, 2, 2.5) that limit is 2.05, but T/I_c = 5.66. **On this estimate the first-guess parameters cannot hold a thin ring.** The obstacle is the composite's large tension, which grows with three strands at κ = 2, compared with what a core condensate can carry.

This is why §2 is a parameter scan with a fixed selection rule, and not a single point. The estimate is crude, and Phase 0 replaces it with the exact straight-string calculation.

## 2. Phase 0: straight-string feasibility (1D, radial)

### 2.1 Grid, fixed now

- β ∈ {1, 2, 3, 5}.
- μ² = ε₀(β) + δ, with δ ∈ {0.25, 0.5, 1.0}.
- λ = μ⁴/(1.6 D), where D = 1.815 is the depth of the ψ vacuum below the all-zero state. This puts the σ-only vacuum at 80 % of D.

That is 12 points, and all of them have m²_vac > 0.

### 2.2 Checks at each point

- **C3, vacuum.** The homogeneous minimum of the full potential over (ρ_ψ, |σ|²) must be the ψ vacuum with σ = 0. A point that fails is dropped and recorded.
- **Existence window.** Minimize the line energy at fixed winding density k and charge per length q:

  ℰ(k, q) = T_static(k) + q²/(4I).

  T_static includes k²|s|². Take k from 0 in steps of 0.05, and q from 0 upward. A (k, q) is inside the window if σ stays condensed (σ(0) > 0.05) and ω = q/(2I) < m_vac.
- **Thin-ring equilibrium.** A ring of fixed (n, Q) has E(R) = 2πR ℰ(n/R, Q/2πR). So dE/dR = 0 is

  𝒯(k, q) ≡ ℰ − k ∂_kℰ − q ∂_qℰ = 0.

  Derivatives are central differences on the grid. Stability in R needs d²E/dR² > 0 there.

### 2.3 Per-point verdict and selection rule

- **Verdict per point:**
  - WINDOW if 𝒯 changes sign inside the existence window at a point with d²E/dR² > 0.
  - NONE otherwise.
- **Selection rule, fixed now.** Among WINDOW points, take the one whose equilibrium has the smallest ω*/m_vac (furthest from leaking); ties go to the smaller β.
- **If every point is NONE.** Phase 1 still runs once, at the point with the smallest min(𝒯/ℰ) over its window. It is labelled a *thick-vorton probe*, because thin-ring failure does not exclude a fat loop.

## 3. Phase 1: the loop, axisymmetric (2D in ρ, z)

### 3.1 Why 2D is valid here

Unlike Amendment A's twisted ring, this configuration is axisymmetric:
- The ψ_k wind around the ring core and do not depend on φ.
- σ ∝ e^{inφ} and vanishes on the axis.
- σ is neutral, so A_φ has no source and A = (A_ρ, A_z) is consistent.

### 3.2 Setup

- **Grid.** h = 0.25, ρ ∈ [0, 24], z ∈ [−24, 24]. Energy as in §1 with |∂_φσ|² → n²|s|²/ρ², integrated with weight 2πρ.
- **Gradient check** against finite differences before any run. Expect ≲ 10⁻⁶.
- **Labels from Phase 0.** Take k*, q* from the selected point. Set n = max(1, round(8k*)), R_eq = n/k*, Q = 2πR_eq q*.
- **Starts:**
  - The composite ring of the N = 0 control (`starts.py`, circle in the z = 0 plane) at R₀ = R_eq.
  - The same at R₀ = 1.5 R_eq.
  - In both, σ = σ(0)·exp(−d²/2)·e^{inφ}, where d is the distance to the ring core.
- **Controls.** All run at the selected point's (β, λ, μ²):
  - C-a: n = 0, Q = 0.
  - C-b: n only, Q = 0.
  - C-c: Q only, n = 0.

### 3.3 Recorded quantities

- E above the vacuum.
- Composite ring radius (`core_radius`) and the σ-weighted radius.
- I and ω = Q/2I.
- The fraction of I within 4 units of any box edge (leak).
- Iteration count.

## 4. Phase 2: 3D stability (only if Phase 1 is STABLE)

- **Grid.** 65³, h = 0.5. The Phase 1 solution is interpolated onto it.
- **Perturbations added:** m = 2 and m = 3 ring-shape deformations of amplitude 0.05 R, plus field noise 10⁻³.
- **Minimization.** E_Q at fixed Q in 3D. n is not imposed. It is measured as the phase winding of σ along the detected composite line, so a phase slip shows up as a change in n.
- **Box check.** 81³.

## 5. Predictions and outcome map (written now)

| | Prediction | Outcome |
|---|---|---|
| P0 | At least one of the 12 points is WINDOW. | descriptive. NONE everywhere is itself a result: no thin-ring vorton on the E9 host string over this grid. |
| P1 (control C-a) | n = 0, Q = 0: the ring collapses, as in the N = 0 control. | instrument check. It must hold. |
| P2 | Both starts stop at the same R_f (within 10 %), with R_f > 2ξ (1.41 coordinate units), ω < m_vac, leak fraction < 1 %, and E < m_vac·Q (cheaper than free σ quanta). | **STABLE (axisymmetric)** |
| | The ring shrinks to core scale and vanishes. | **COLLAPSE** |
| | σ spreads to the box: leak > 1 %, or ω ≥ m_vac. | **LEAK** (the charge is not localized) |
| | The ring grows to the box. | **EXPANDS** (inconclusive) |
| | Any other end state, or E ≥ m_vac·Q at a finite R_f. | **MARGINAL** |
| P3 | Phase 1 R_f within 25 % of the Phase 0 thin-ring R_eq. | descriptive. Tests the thin-ring picture. |
| P4 | If Phase 2 runs, the m = 2, 3 deformations decay, n is unchanged, and R_f moves < 5 % at 81³. | **STABLE (3D)**. A pinching or phase-slip decay is recorded as UNSTABLE (3D), with its mode. |
| P5 | Controls C-b (current only) and C-c (charge only). No verdict. | descriptive. Prior art suggests both fail alone; recorded either way. |

**My prior, stated honestly.**
- P0: about 50 %. The §1.3 estimate is unfavourable at small β, and better at large β where ε₀/β falls.
- STABLE (axisymmetric), given WINDOW: about 40 %.
- STABLE (3D), given that: about 50 %. Vortons in related models are reported to be unstable to pinching over much of their range.
- Overall: about 10 %.

**What a STABLE result would and would not mean.** A charged, current-carrying loop held open by a core condensate is a known mechanism (Witten; Davis and Shellard; Battye and Sutcliffe; Garaud, Radu and Volkov). A STABLE result would show that the E9 three-strand string can host one, at σ parameters that were *chosen* by the §2 rule. It says nothing about the thirds. The strands enter only as a host string with a large tension.

## 6. Eddington guard

- No particle mass, no PDG number. The outputs are E/T₀, R_f/ξ, ω/m_vac, n and Q.
- The ψ sector (κ, η, e, h of `PREREG.md`) is not re-tuned.
- The σ parameters are new inputs, chosen by the §2 rule, which is fixed here. No point outside the §2 grid is to be tried after seeing Phase 1. A wider scan is a new pre-registration.
- "Closure" describes the configuration. No identification with any particle is made. n and Q are not to be read as spin or electric charge: σ is neutral under A by A3.

## 7. Prior art to verify before interpreting (all [memory] until checked)

- Witten, Nucl. Phys. B 249, 557 (1985): superconducting strings, bosonic core condensate.
- Davis, Shellard, Phys. Lett. B 209, 485 (1988) and Nucl. Phys. B 323, 209 (1989): vortons.
- Carter (1989–90): elastic string models and the vorton equilibrium condition. §2's 𝒯 = 0 should be checked against Carter's form.
- Lemperiere, Shellard, Nucl. Phys. B 649, 511 (2003): vorton stability and instabilities.
- Battye, Sutcliffe, Nucl. Phys. B 814, 180 (2009): vorton construction and dynamics in a global U(1)×U(1) model.
- Radu, Volkov, Phys. Rep. 468, 101 (2008): stationary ring solitons (knots and vortons).
- Garaud, Radu, Volkov, PRL 111, 171602 (2013): stable cosmic vortons in a gauged model.

## 8. Cost and run plan

- **Phase 0:** about 12 × 150 one-dimensional minimizations, of seconds each. Under an hour.
- **Phase 1:** about 5 axisymmetric runs of ~2×10⁵ unknowns, minutes each.
- **Phase 2:** 3D at 65³ is ~3×10⁶ unknowns at about 0.6 s per iteration, so about an hour per run, plus the 81³ check.

**Order:**
1. Phase 0 (new script `option4_phase0.py`, reusing `option4_design.py`).
2. Report.
3. Phase 1 (`axial_vorton.py`, gradient-checked).
4. Report.
5. Phase 2 only if the Phase 1 verdict is STABLE.

Each report applies §5 as written and records deviations, as in `REPORT_N1_rerun.md`.

## 9. Amendment A (October 31, 2026, after Phase 0, before any Phase 1 run)

**Label: post-hoc.** This amendment is written after reading `REPORT_phase0.md` (commit 025f69c). The selection rule below was chosen knowing the Phase 0 results. It is recorded as such, and a Phase 1 result obtained under it carries that label. §1–§8 are unchanged. Where they conflict with this section, this section governs Phase 1 and Phase 2.

### 9.1 What Phase 0 showed that the pre-registration did not anticipate

- **C3 gap (author's).** C3 tested only the global minimum. At 11 of 12 points the σ phase (ψ = 0, |σ|² = S = μ²/λ) is also a *local* minimum, because βS > 1 + η. Large charge can then be stored in a widening σ-phase tube. The only non-metastable point, b1_d1, is the only point with no equilibrium. **Recorded finding: on this grid, thin-ring equilibria occur only where the σ phase is metastable.** This is descriptive and is not a new verdict.
- **What the equilibria are.** Every equilibrium sits at q* ≳ 35, where σ fills a tube of radius about 3–5 and pushes the ψ core out to a similar radius. What holds the ring open looks like the pressure of a charged σ domain, not a current in a thin core. The ψ string may therefore be a passenger. §3 had no control for that. C-d below adds one.
- **The §2.3 selection rule is ill-posed in this regime.** Along every 𝒯 = 0 contour ω*/m_vac falls monotonically as q* rises, so "smallest ω*/m_vac" always picks the q cap. Raising the cap would only move the selection to the new cap. The rule is replaced, not re-run.

### 9.2 Replacement selection rule

Among the Phase 0 sign changes with d²E/dR² > 0 (interpolant and direct solve agreeing in sign) and R_eq/r_σ ≥ 3 under the §3.2 n rule, take the smallest ω*/m_vac. The threshold 3 is the author's item 3. It was set during the Phase 0 run, before any result was seen.

Applied to `phase0_results.json`, this selects **b3_d1**:

| | value |
|---|---|
| β, δ, μ², λ, m_vac | 3, 1, 5.0250, 8.6951, 2.2079 |
| k*, q* | 0.8144, 53.50 (between grid points (0.80, 53.5) and (0.85, 53.5); no one-sided flags) |
| ω*/m_vac | 0.646 |
| r_σ*, r_ψ* | 2.80, 3.39 |
| d²E/dR² | +47.3 (interpolant), +47.4 (direct) |

The runner-up is b2_d1 at ω*/m_vac = 0.765.

**Caveat, stated now.** The selected point sits at R_eq/r_σ = 3.07, just above the threshold. Along the contour, ω*/m_vac falls while R_eq/r_σ falls, so the threshold, like the cap before it, sets the location. To make the result independent of that, Phase 1 runs the selected (k*, q*) at two values of n. Because 𝒯 = 0 depends only on (k, q), a larger n at the same (k*, q*) gives the same thin-ring equilibrium at a larger radius.

| run | n | R_eq = n/k* | Q = 2πR_eq q* | R_eq/r_σ | R_eq/r_ψ |
|---|---|---|---|---|---|
| **primary** | 7 | 8.595 | 2889.3 | 3.07 | 2.54 |
| **thin check** | 10 | 12.279 | 4127.6 | 4.39 | 3.62 |

### 9.3 Phase 1 changes

**Grid.** ρ ∈ [0, 32], z ∈ [−32, 32], h = 0.25. The 1.5 R_eq start at n = 10 reaches ρ ≈ 22 with the ψ core included, too close to the §3.2 box.

**Starts.** Profiles come from the straight-string solution, not the §3.2 Gaussian. Regenerate the straight-string solution at the selected point and (k*, q*) with `option4_phase0.py`'s functional; it is deterministic. With d the distance from the circle ρ = R₀, z = 0:
- ψ_k = f(d) e^{iχ}, where χ is the angle around the ring core.
- A is the matching a(d) profile, oriented around the core.
- σ = s(d) e^{inφ}.

Two starts for each n: R₀ = R_eq and R₀ = 1.5 R_eq.

**Controls.** All at the b3_d1 potential, all at n = 7 unless stated.
- **C-a.** n = 0, Q = 0, σ start as above. Must collapse (P1).
- **C-b.** n = 7, Q = 0. Descriptive.
- **C-c.** n = 0, Q = 2889.3. Descriptive.
- **C-d, passenger control (new).** n = 7, Q = 2889.3, the same σ start at R₀ = R_eq, and ψ_k = f(d) with **no winding** (χ = 0, A = 0). The σ tube is unchanged, but no vortex threads it. Also run at n = 10, Q = 4127.6.
- **C-e, lump comparison (new).** n = 0, Q = 2889.3, no ψ winding, σ started as a ball of radius 4 at the origin. It relaxes to the lowest-energy charged σ lump the 2D code can reach. The energy E_lump is recorded. Repeat at Q = 4127.6.

**Recorded quantities** (in addition to §3.3):
- E − E_lump at the same Q.
- For C-d, E_C-d − E_main at the same (n, Q).
- r_σ and r_ψ of the final state.

### 9.4 Verdicts, revised

P2's STABLE/COLLAPSE/LEAK/EXPANDS/MARGINAL arms stand as written, applied to each main run (n = 7, n = 10). The main verdict is then qualified by C-d:

| main run | C-d at the same n | verdict |
|---|---|---|
| STABLE | COLLAPSE, LEAK, or relaxes to something with no σ ring | **STABLE, string-supported** |
| STABLE | STABLE | **STABLE, string not required.** The E9 string is a passenger. E_C-d − E_main is reported. |
| not STABLE | any | the main verdict as is |

**C-e qualifier.** If E_lump < E at a STABLE main run, the ring is recorded as **metastable**: it is held only by its winding n against decay into a charged lump. Phase 2's phase-slip monitor tests that channel.

**Thin-ring check (P3, revised).** P3 is applied to both n. If n = 7 and n = 10 disagree (one STABLE, one not), the result is recorded as **n-dependent**, and the n = 10 verdict is the one carried forward.

Phase 2 runs only on a **STABLE, string-supported** result. A "string not required" result closes option 4 as far as the E9 string is concerned. Any study of σ alone would be a new pre-registration.

### 9.5 Ambiguities from `REPORT_phase0.md` §7, settled

- **(a)** The k stop rule stands as run, and is recorded as a limit of Phase 0. No re-run.
- **(b)** The localization test stays ω < m_vac (the stricter, pre-registered form). Report ω² < m²_vac + k² alongside as descriptive.
- **(c)** b1_d0.25 stays NONE (truncated), per the literal rule.
- **(d)** Superseded by the two-n design in §9.2.
- **(e)** Recorded in §9.1.
- **(f)** Superseded by §9.2.

### 9.6 Prior, revised

- STABLE (axisymmetric) at n = 10: about 35 %.
- C-d STABLE, given a STABLE main run: about 50 %. In a metastable σ phase a charged, wound σ ring may not need a vortex at all.
- **STABLE, string-supported: about 15 %.** Then STABLE (3D) given that: about 50 %. **Overall about 7 %.**

### 9.7 Eddington guard, restated

Unchanged from §6. In addition:
- No point other than b3_d1 is run in Phase 1. Running b2_d1 or b5_d1 would be a new amendment.
- No n other than 7 and 10 is run.
