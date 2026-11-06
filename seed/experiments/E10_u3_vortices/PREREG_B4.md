# E10 / Route B, B4: the axisymmetric charged, twisted loop

*November 4, 2026. Label: Exploration. Written after `REPORT_verify.md` (A.4: CONFIRMED, head 6f5e71b) and before any loop code. Follows `PREREG_B2B3.md` §3, §4 and §6.*

## 0. The question

The straight elementary U(3) string, carrying charge and twist, has a verified thin-ring equilibrium at λ = 1. Does a closed loop of it actually stop at a finite radius? And if it does, is the result an absolute minimum, or only a local one above the cost of breaking up into free bulk quanta?

## 1. Selection (fixed by verification status, not by value)

**Selected point: sign change #66 at λ = 1.** It is the only sign change carried through every Amendment A check: V1b, V1c (r_max = 60) and V2 (2D lattice). Values from `verify_results.json`, V1b:

| quantity | value |
|---|---|
| bracket | (k, q) = (0.25, 24.8) – (0.30, 24.8) |
| k*, q* | 0.287402, 24.80 |
| ω*/m_bulk | 0.98079 |
| r_q* (charge rms radius) | 3.4095 |
| ℰ* | 26.415 |
| d²E/dR² | +4.16 (direct) |

**Two values of n,** as in E9 option 4 Amendment A, so that a result cannot hinge on how thin the ring is. Since 𝒯 = 0 depends only on (k, q), a larger n gives the same equilibrium at a larger radius.

| run | n | R_eq = n/k* | Q = 2πR_eq q* | R_eq/r_q |
|---|---|---|---|---|
| primary (A.1 rule) | 3 | 10.438 | 1626.5 | 3.06 |
| thin check | 5 | 17.397 | 2710.9 | 5.10 |

Compute Q from the exact JSON values; the numbers above are rounded.

**Not selectable** (A.7): the λ = 0.8 and 0.9 sign changes, which are descriptive (V3). The same applies to any other λ = 1 sign change.

## 2. The thin-ring energy budget (computed now)

- **Thin-ring energy:** E_thin = 2πR_eq ℰ* = 1732.4 (n = 3) and 2887.4 (n = 5).
- **Cost of dispersing the charge into free bulk quanta:** m_bulk·Q, with m_bulk = 1 at λ = 1. That is 1626.5 and 2710.9.
- **Ratio:** E_thin/(m_bulk Q) = ℰ*/(m_bulk q*) = **1.065** at both n.

**Consequence, before any run.**
- ω* < m_bulk, so emitting one charge quantum costs more than it releases. That makes the ring **locally** stable against charge loss.
- But its total energy is about 6.5 % above the fully dispersed state. **Even a perfect thin ring here is at best metastable,** not absolutely stable.

The verdicts below separate these two cases.

## 3. Model and instrument

**Model.** PREREG_B2B3 §1 at λ = 1, with G = diag(0, 1, 0). Rescaled units.

**Axisymmetric ansatz.**
- Let (ρ, φ, z) be cylindrical coordinates, χ the angle around the ring core in the (ρ, z) half-plane, and U(β) = exp(iβG).
- Fields: H(ρ, φ, z, t) = U(nφ − ωt) H(ρ, z) U(nφ − ωt)†, with W_ρ and W_z rotated the same way.
- Dressings W_φ and W_t are solved for; W_t comes from the Gauss law (inner linear solve, as in B3).
- **The elementary winding is around the ring core.** The first entry's phase winds once in χ, at the orientation set by the start.
- **Functional:** E_Q = E_static + E_twist(n, W_φ) + Q²/(4I(H)), with I(H) from the inner W_t solve, exactly as B3's ℰ. The integration weight is 2πρ.
- **Gradient:** analytic, checked against 5-point finite differences.

**Grid.**
- Box ρ ∈ [0, 40], z ∈ [−20, 20], with a Dirichlet vacuum edge (H = 1).
- Primary spacing h = 0.25.
- **Final-state check at h = 0.125:** re-relax every non-collapsing end state. It must move R_f by < 5 % and E by < 1e-3 relative.
- **Regression before any loop run:** a straight segment far from the axis (large R) must reproduce B3's ℰ at (k*, q*) to < 2e-3 relative, at h = 0.25.

**Starts.**
- Take the converged straight-string solution at (k*, q*): re-solve it on the radial grid at the interpolated k*, warm-started from V1b.
- Map it onto a ring of radius R₀ in the z = 0 plane, by distance d from the core circle and angle χ.
- Each n gets two starts: R₀ = R_eq and R₀ = 1.5 R_eq.

## 4. Runs

| run | n | Q | R₀ | purpose |
|---|---|---|---|---|
| M3a, M3b | 3 | 1626.5 | 10.44, 15.66 | main |
| M5a, M5b | 5 | 2710.9 | 17.40, 26.10 | main (thin check) |
| C-a | 0 | 0 | 10.44 | instrument control: must collapse |
| C-b | 3 | 0 | 10.44 | twist only: descriptive (B3 P4 says the twist switches itself off) |
| C-c | 0 | 1626.5 | 10.44 | charge only: descriptive (B3 P1 says no equilibrium) |
| C-d | — | 1626.5 | — | **no vortex.** The same SU(3)_{C+F} charge, seeded as a rotating deformation of H inside a ball of radius 4 at the origin. Gives E_disp: the box's dispersed-charge energy, or a bound bulk lump if one exists. |
| C-d5 | — | 2710.9 | — | the same at n = 5's Q |

**Recorded every 50 iterations and at the end, per run:**
- E above vacuum;
- R_f, the ψ-core position: the zero of the first-entry winding in (ρ, z), at plaquette resolution;
- the charge-weighted radius and r_q;
- I, and ω = Q/(2I) with ω/m_bulk;
- the leak fraction: charge density within 4 units of the box edge, excluding the axis;
- the twist retention τ = ⟨4 sin²α cos²α⟩, charge-weighted (1 = fully twisted, 0 = unwound);
- iterations and stop message.

Final fields are saved.

## 5. Verdicts (fixed now)

**Per main run.** These apply to a pair of starts at the same n:

| verdict | conditions |
|---|---|
| **STABLE (absolute)** | Both starts reach the same R_f within 10 %. R_f/r_q ≥ 2. τ ≥ 0.5. ω < m_bulk. Leak < 1 %. The h = 0.125 check passes. **And E < min(m_bulk·Q, E_disp).** |
| **METASTABLE** | Every STABLE condition except the last: E ≥ min(m_bulk·Q, E_disp). |
| **COLLAPSE** | The ring shrinks to core scale (R_f/r_q < 1) or the core vanishes. The mechanism is named: plain shrinkage; unwinding first (τ < 0.1, then shrinkage); or charge loss first. |
| **LEAK** | Leak > 1 % or ω ≥ m_bulk at the end state. The charge is not held. |
| **EXPANDS** | The ring reaches the box edge. Inconclusive. |
| **MARGINAL** | Any other end state, including two starts ending at different R_f. |

**Passenger qualifier (C-d).** If C-d ends in a localized bulk lump (leak < 1 %, finite charge radius) with E_lump < E_main at the same Q, the main verdict carries **"string not required"**. The charged bulk lump is then the cheaper object, and the string is not what holds the charge.

**n-dependence.** If n = 3 and n = 5 disagree, record "n-dependent". The n = 5 verdict carries forward, as the better thin-ring case.

**Phase 3 (3D).** Pinching, and non-axisymmetric unwinding of the twist (π₁(CP²) = 0), gets its own pre-registration. It is written only after a **STABLE** or **METASTABLE** result without the "string not required" qualifier.

## 6. Predictions (written now)

| ID | Prediction | Prior |
|---|---|---|
| P1 | C-a collapses. | must hold |
| P2 | C-b: τ → 0 (the twist switches off), then collapse. C-c: collapse. | 85 % |
| P3 | C-d: the charge disperses to box modes. E_disp ≥ m_bulk·Q, with the excess set by the box (lowest mode ω ≈ √(1 + (π/L)²)). There is no bound bulk lump. | 75 % |
| P4 | Main runs that do not collapse stop within 15 % of R_eq. Curvature corrections are of order r_q/R. | 70 % (given no collapse) |
| P5 | Verdicts. From §2, absolute STABLE is very unlikely. | n = 5: METASTABLE about 35 %, COLLAPSE about 55 %, STABLE (absolute) < 5 %, other about 5 %. n = 3: METASTABLE about 25 %, COLLAPSE about 65 %. |

**My overall prior that B4 gives a METASTABLE or STABLE ring at n = 5: about 40 %.**

## 7. What each outcome would mean

- **METASTABLE at n = 5.** The first finite-size closure in this programme. It is a classical, axisymmetric, charged and twisted loop of an elementary 1/3-flux string. It is locally stable, and sits about 6.5 % above dispersal.
  - It needs no added field: the orientation moduli are part of the U(3) model.
  - It holds only on the type-I/BPS side, by V3, and only classically. The CP² moduli acquire a quantum gap (B1 §2).
  - Not established until Phase 3: non-axisymmetric stability.
- **COLLAPSE at both n.** The thin-ring window does not survive closing the string. Route B's intrinsic vorton closes at the loop level, with its mechanism recorded.
- **"String not required".** The charge binds into a bulk lump on its own, as in E9 option 4. Route B's string is a passenger.

## 8. Eddington guard

- Fixed: λ = 1, #66, n ∈ {3, 5}, Q by formula, the grid rule, the starts and the verdict rules. None is to be retuned after seeing results.
- Any other n, Q, λ or sign change is a new pre-registration.
- Model units only. No particle identification. The SU(3)_{C+F} charge is not electric charge, and n is not spin.
