# G-CC-ε1-R2 — CC-Leg Report (independent second leg)

**Date:** 2026-07-15 · **Locked R2 pre-registration:** md5 `e356b14e87150ce535684c47c1e88652` ·
**Consumed declarations:** Branch C (V4.65) + VC-B (author-declared) + Amendment 2 (authorized) ·
**Chat leg:** `g_cc_e1_r2_chatleg.py` + `G_CC_E1_R2_EXECUTION_REPORT.md` (+ checkpoint `r2_checkpoint.json`) ·
**Script:** `g_cc_e1_r2_ccleg.py` (numpy + scipy + sympy).

> **Two-leg result: VERDICT-LEVEL AGREEMENT — ARM A (BOUND-DELIVERED, SURFACE class).** All report-§6
> comparison items match; **no S9 triggered.** Two CC contributions beyond confirmation: an
> **existence-boundary refinement** (report-§6-invited) and a **chat report-table typo caught** via
> direct profile cross-comparison.

## Independence (report §6, honored)
| Layer | Chat leg | CC leg (this) |
|---|---|---|
| Solver class | explicit forward-Euler **normalized gradient flow** | imaginary-time **split-step, implicit Crank–Nicolson** radial Laplacian (tridiagonal solve) |
| Grid | node-centered, DR=0.075, NR=640 | **cell-centered**, DR=0.06, NR=800 |
| Quadrature | trapezoid | **Simpson** |
| Measures | own | independent extractors |
| T-identities | derived | **re-derived** in sympy (two-fluid tensor identity + trace) |
| Existence probe | 3-seed adaptive | independent; **tests the chat's EMPTY points** |

## Results
### T-identities (independently re-derived)
The two-fluid momentum-flux identity Σρ_c u_c⊗u_c = J⊗J/ρ_tot + (ρ₁ρ₂/ρ_tot)Δu⊗Δu holds exactly; the
relative-flow stress (ρ₁ρ₂/ρ_tot)|Δu|² is winding-even and non-negative (the Amendment-2 correction,
re-verified); the R2 pointwise trace J_int+O_int=KE_int holds (single winding).

### D0 — existence & the three maps (cross-checked against the chat's own profiles)
All four admissible points localize (tail<1e-6, GP-residual<1e-5) with μ₁<η. **The CC solver's maps
agree with the CC measure-extractor applied to the chat's own checkpoint profiles to within 1.9%** at
every admissible point (apples-to-apples — same extractor, both solvers' converged states):

| (η,N₁) | CC solver (Â,Ĵ,Ô,T̂) | CC-on-chat-profile | max rel |
|---|---|---|---|
| (2.0,20) | 15.18, 4.67, 1.80, 8.07 | 15.17, 4.68, 1.82, 8.07 | 1.3% |
| (3.0,5) | 9.35, 0.60, **1.63**, 2.74 | 9.35, 0.61, **1.64**, 2.74 | 0.8% |
| (3.0,10) | 13.75, 4.41, 1.18, 7.50 | 13.73, 4.43, 1.20, 7.49 | 1.9% |
| (3.0,20) | 18.28, 7.37, 0.44, 11.24 | 18.26, 7.41, 0.45, 11.23 | 1.9% |

**Report-table typo caught:** the chat *report* table lists Ô=1.20 for **both** (3.0,5) and (3.0,10)
— a transcription duplication. The chat's own (3.0,5) *profile* gives Ô≈1.64 (matching the CC solver's
1.63), so the table's (3.0,5) Ô=1.20 is a **report typo, not a physics disagreement**. Recommend a
one-line correction to the chat report table.

### D0 — existence-boundary REFINEMENT (report-§6-invited)
The strongly-miscible probes (η ≤ 1.2) do **not** localize — the tube spreads to the boundary
(R_tube ≈ 18–22 ξ) — so the **qualitative domain structure (localized immiscible / empty miscible)
matches**. But the more-robust implicit-CN solver converges stable tubes at **lower loading and weaker
immiscibility** than the chat's explicit flow reached: **(2.0,10)** localizes robustly (tail 4×10⁻¹⁸,
res 2×10⁻¹¹), and **(3.0,3), (1.5,20)** localize — all points the chat classed EMPTY under its
*solver-level* caveat ("not a nonexistence theorem"). So the existence boundary is **tighter here**:
N₁_min(2.0) ∈ (5,10] and N₁_min(3.0) ∈ (2,3], versus the chat's (10,20] / (2,5]. This is a **wider
convergence basin of the second method — a boundary refinement, not a structural disagreement**; the
verdict is unchanged.

### D3′ — bounds
Over the four admissible points: **Â ∈ [9.35, 18.28] — all positive, no zero-crossing** (genuine
density deficit); **Ĵ ≥ 0.60, Ô ≥ 0.44** — flow channels bounded away from zero on the domain; T̂ ∈
[2.74, 11.24]; all measures finite (VC-B locality). Topological far-field floor OFF by VC-B (T5).

### D4′ — dimensional closure (KC3-blind, symbolic)
Per channel ℓ = γ·M·τ·ξ / 𝒫; **ρ_s and the knot length cancel exactly** ⇒ **SURFACE class (single
surviving import ξ), all three channels**; Mach saturates at **M → φ² ≈ 2.618** for ultrarelativistic
knots (c_s = φ⁻²c).

### Comparison (KC3 quarantined to the last step)
KC3 (Moore–Nelson, operationalized as loss-length ≥ propagation-length) maps to ξ·γ·M·τ̂ / 𝒫_i ≥ L_prop
per channel; **ξ is unpinned (M.CW)**, so the parameter-free joint-floor kill (Arm B) is unavailable
and no pass can be claimed — the comparison **delivers the constraint curve**. **ARM A — BOUND-DELIVERED
(SURFACE).**

## Two-leg comparison (report §6 items)
| Item | Verdict |
|---|---|
| **arm** | ARM A — BOUND-DELIVERED (SURFACE) — **MATCH** |
| **domain structure** | localized immiscible / empty miscible; N₁_min boundary — **QUALITATIVE MATCH**, boundary tightened (invited refinement) |
| **maps** | within **1.9%** vs the chat's own profiles at all 4 points — **MATCH** |
| **bounds** | Â>0 (no zero-crossing); Ĵ,Ô floors >0 — **MATCH** |
| **closure class** | SURFACE (single import ξ), all channels; M→φ² — **MATCH** |

**Verdict-level agreement ⇒ no S9 counter-cross-check.**

## Honesty / scope
- **Existence boundary is solver-sensitive**: my independent solver localizes states the chat's
  explicit flow classed EMPTY. Reported as a refinement (tighter N₁_min), verdict unchanged — the
  chat's own "solver-level, not a nonexistence theorem" caveat is exactly what a second method tests.
- **Chat report-table typo (Ô(3.0,5))** surfaced and diagnosed via profile cross-comparison — a report
  correction, not a physics disagreement.
- No KC claimed; no observable; no magnitudes beyond the delivered curve; **no fold**. Fluid branch,
  linear channel, **radial-sector** stability only (azimuthal/3D deferred per the R2 ceiling). §2.87.J
  and §2.52 Open 3 untouched. Fold eligibility (two-leg agreement — now achieved — **+ explicit author
  authorization**); the estate fold (VC-B + A2 + R2 + this set) targets §2.91.G as one unit.

## Consequence
The CC leg confirms the chat leg's routing: **II-B proceeds with the delivered constraint curve**, and
the single import that converts the inequality into a KC3 pass/fail is **ξ (the substrate scale) —
the named successor ξ-pinning gate/declaration.**
