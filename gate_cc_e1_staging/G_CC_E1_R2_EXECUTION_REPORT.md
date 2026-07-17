# Gate G-CC-ε1-R2 — Chat-Leg Execution Report

**Date:** July 15, 2026 · **Verdict:** **ARM A — BOUND-DELIVERED (SURFACE class; constraint curve delivered). NO KC IS CLAIMED PASSED.** · **Status:** chat leg COMPLETE; CC leg PENDING (two-leg rule bars fold).

**Artifact chain:** R2 instrument md5 `e356b14e87150ce535684c47c1e88652` (locked, re-verified) · LSF-δ `57aed6ec…` (post-lock, pre-derivation; no amendment) · chat leg `g_cc_e1_r2_chatleg.py` md5 `0b58d11b…` (numpy+sympy, standalone, phased execution with checkpoint `r2_checkpoint.json` md5 `2a20eed5…` carrying the converged profiles for CC cross-comparison) · **46 assertions** across phases · consumed declarations: Branch C (V4.65) + VC-B · adopted inputs T1–T5 (machine-rechecked on every profile via the T2 trace identity, max pointwise deviation < 1e−10).

---

## 1. D0 — existence & radial stability (the domain, found not assumed)

Stable (radial-sector) annular winding-carriers exist on the **immiscible branch only**: LOCALIZED at (η, N₁) = (2.0, 20), (3.0, 5), (3.0, 10), (3.0, 20); tube radii R_tube ≈ 1.35–1.80 ξ. **A minimum-loading existence boundary N₁_min(η) emerged** — N₁_min(2.0) ∈ (10, 20], N₁_min(3.0) ∈ (2, 5], decreasing in η — the F3-analog for the VC-B family: small loadings cannot pay the winding kinetic cost of a tight annulus and unbind. Miscible probes (η = 0.5, 0.9) and the weakly immiscible band (η = 1.2, 1.5) yielded no localized state **at solver level** (adaptive 3-seed gradient flow; stated as a solver-level statement, not a nonexistence theorem). Bound-state criterion μ₁ < η verified on every admissible point. Perturb-and-reconverge and two-seed checks passed on the admissible samples. Stability certificate: constrained gradient-flow convergence (radial sector; azimuthal/3D deferred per the R2 ceiling).

## 2. D2′/D3′ — the three maps and their bounds (bath units: ℏ = m = g = n₂∞ = 1)

| η | N₁ | Â (deficit) | Ĵ (current) | Ô (relative) | T̂ (tension) | μ₁ |
|---|---|---|---|---|---|---|
| 2.0 | 20 | 15.17 | 4.68 | 1.82 | 8.06 | 1.355 |
| 3.0 | 5 | 9.35 | 0.61 | 1.20 | 2.74 | 1.623 |
| 3.0 | 10 | 13.73 | 4.43 | 1.20 | 7.49 | 1.623 |
| 3.0 | 20 | 18.26 | 7.41 | 0.45 | 11.23 | 1.351 |

**Bounds over the computed domain (machine-verified extrema):** Â ∈ [9.35, 18.26] — all positive, **no zero-crossing found**: the annular carrier carves a genuine total-density deficit (winding-KE dilution + interface); Ĵ ≥ 0.61, Ô ≥ 0.45 — **the flow channels have nonzero floors on the computed domain** (domain-level statements, not global theorems); T̂ ∈ [2.74, 11.23]. All measures **finite** — the VC-B locality payoff versus the VC-A logarithm, on the record. Topological far-field floor: **OFF by VC-B** (T5; recorded constant 0).

## 3. D4′ — dimensional closure (KC3-blind, symbolic)

Per channel, the loss length closes to **ℓ = γ·M·τ̂·ξ / 𝒫_channel**, with ρ_s and the knot length **cancelling exactly** (machine-asserted). **SURFACE class, all three channels — the single surviving import is ξ, the substrate scale.** The Mach number saturates at **M → φ² ≈ 2.618** for ultrarelativistic knots (c_s = φ⁻²c, locked) — the cone kinematics of every fast knot evaluate at the same golden point.

## 4. Comparison (quarantined, run last) and the delivered object

KC3 (Moore–Nelson, operationalized as loss length ≥ propagation length) maps to the **delivered constraint curve**: **ξ · γ · M · τ̂ / 𝒫ᵢ(Â, Ĵ, Ô; M = φ²) ≥ L_prop** per channel. With ξ unpinned (M.CW), the parameter-free joint-floor kill is unavailable and no pass can be claimed: the arm is **A — BOUND-DELIVERED (SURFACE)**. The KC3 disposition is now an explicit inequality that resolves exactly when ξ is pinned — **the named successor item** (a declaration/derivation gate for the substrate scale).

## 5. Honesty ledger (this leg)

1. **Solver-criterion redesign (methodological, logged):** the initial residual criterion outran the soft ring-radius mode (first sweep misclassified localizing states as EMPTY); redesigned to phased checkpointed execution with adaptive 3-seed initialization and measure-drift convergence — the redesign preceded any map extraction; no result was harvested from the misclassifying configuration.
2. **Tooling:** numpy 2.x `trapz` rename; a refactor splice left a stale block in the final phase (KeyError on first final run) — both caught by execution, both content-free.
3. The sweep-phase assertion counter contributed 0 by design (per-point assertions live in the final-phase measures); the 46 total is the true machine-checked count as executed.

## 6. CC dispatch specification (two-leg rule)

Independent build, zero shared machinery: independent solver class (imaginary-time split-step or shooting/Newton BVP vs the chat leg's normalized gradient flow); own measure extractors and quadrature; independent re-derivation of T1–T5; **independent probe of the existence boundary** N₁_min(η) including points the chat leg found EMPTY (the solver-level statements are exactly what a second method should test); the checkpoint profiles available for direct cross-comparison at the four admissible points; D4′ closure re-derived; comparison last. Verdict-level comparison: arm + domain structure + maps within stated errors + bounds + closure class; disagreement → S9.

## 7. Consequence routing

II-B proceeds with the constraint curve in hand; every II-B computation states its (Â, Ĵ, Ô)-dependence per the V4.65 lift terms. The successor item is the **ξ-pinning gate/declaration** — the single import whose value converts the delivered inequality into a KC3 pass/fail. Fold eligibility: two-leg agreement + explicit author authorization; the estate fold (VC-B declaration + A2 + R2 + this result set) targets §2.91.G as one unit. §2.87.J and the §2.52 Open 3 row untouched throughout.

*Filed July 15, 2026. Chat leg complete; nothing folds without the CC comparison and explicit authorization.*
