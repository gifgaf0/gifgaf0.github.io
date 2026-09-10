# G-S2C1 — LOCK RECORD ADDENDUM P2 (Phase 3 / Probe P2, the aggregate) — LOCKED September 3, 2026

**Authorization (verbatim, author):** "Election E-P2-1: I elect (a) (aggregate averages over full SO(3); S2 channel = polarization-averaged transverse shear cone). Probe P2 Execution: You are authorized to lock the P2 Addendum incorporating E-P2-1 and the F-AGG falsifiers, and execute the Aggregate Probe (Phase 3) using the recovered G-POLY1 Rayleigh machinery. Compute a₂^agg and a₄^agg."

## Substrate objects (banked, G-POLY1)
The four pinned polycrystal tensors (`poly_vrh_results.json` md5 200e7a8b775577564369c6924d38a84c → `vrh` → hex:step, hex:gem8, cubic:step, cubic:gem8), the SO(3)-covariance Ξ and mode kernels Φ_TM(μ) exactly as in the recovered `poly1_fullprec_ccleg.py` (branch gvbkof @ 231b555a, manifest-verified), Voigt reference velocities V_T = √μ̄, V_L = √(λ̄+2μ̄), the exponential two-point spectrum η̃(q) = a_g³/(π²(1+q²a_g²)²), a_g ≡ 1. Pin check (Phase 0 of P2): the banked quartet Q_T^a {3.519074e-2, 5.002055e-2, 5.407763e-2, 7.549430e-2} must be reproduced digit-for-digit before anything else.

## Operational definition (E-P2-1 (a))
Channel: the polarization-averaged transverse wave (projector ½(I − p⊗p), scattered T+L summed). Quantity: the second-order (Born/SOA) fractional phase-velocity shift, the real-part partner of the banked attenuation, with the SAME kernels and the SAME mode normalization N_M = 1/(V_T²V_M²) that reproduces α_T:
  D(k) ≡ Δc_T/c_T(k) = (1/π) Σ_{M∈{T,L}} N_M · J_M(k),   J_M(k) = PV∫₀^∞ dq q⁴ F_M(q,k)/(k_M² − q²),
  F_M(q,k) = ∫₋₁¹ dμ Φ_TM(μ)/(1 + k² + q² − 2kqμ)²,   k_M = k V_T/V_M   (k in units 1/a_g).
Sign fixed by positive attenuation (k_eff² = k² − Π). Closed-form anchor: D(0) = −(1/4) Σ_M N_M ∫Φ_TM dμ (static second-order velocity renormalization below Voigt). Tie-in: Im-part reproduction α_T(k) = Σ_M k k_M³ N_M/2 · F_M(k_M, k) must equal the recovered `alpha_finite` on the G-POLY1 grid {0.02,0.03,0.05,0.08,0.12} to 10⁻⁹ relative (F-AGG-KK).
Dispersion: Δ(k) ≡ D(k) − D(0) on the E-4-style dyadic ladder k a_g ∈ {0.3/2^j, j = 0..8} ∪ {0.005,0.01,0.015,0.02,0.03}. Pre-registered analytic structure (derived pre-data from the pole region q ≈ k_M): Δ(k) = a₂^agg k² + a₃^agg k³ + a₄^agg k⁴ + …, with a₃ (non-analytic, the KK partner of the k⁴ attenuation) EXPECTED nonzero. Fit bases: (i) the elected P1 basis {k², k⁴} ("a₂^agg,2"); (ii) the 3-term basis {k², k³, k⁴} ("a₂^agg,3", with a₃ banked). RULE (pre-data): a₂^agg OF RECORD = the 3-term k² coefficient if the two bases disagree beyond max(CI) (2-term misspecified by the pre-registered k³ term), else the elected 2-term coefficient; both always reported with window-stability CIs (nested upper edges 0.3/0.15/0.075). Analytic control on a₂^agg: the small-k expansion coefficient computed independently from the closed-form derivative formula (D₂ from ∂F/∂k² and the pole-shift term) must agree with the fitted a₂^agg,3 within its CI (F-AGG-ANALYTIC).

## Falsifiers (P2), τ_agg = 10⁻⁶
- **F-AGG-DISP:** |a₂^agg| > max(τ_agg, CI) ⇒ **A3-agg** (the shear cone in the aggregate is dispersive at the grain scale). a₂^agg = 0 at τ_agg with a₃ or a₄ ≠ 0 ⇒ **A2-agg**; all zero ⇒ **A1-agg**.
- **F-AGG-KK:** α_T reproduction on the G-POLY1 grid ≤ 10⁻⁹ rel; **F-AGG-PIN:** Q_T quartet digit-for-digit; either failing ⇒ **A5-agg** halt.
- **F-AGG-L (positive control):** the L channel (Φ_LM, N_M = 1/(V_L²V_M²)) through the identical pipeline: D_L(0) and a₂^agg,L nonzero and analytic-controlled.
- **F-CONV:** Ξ quadrature doubling (nb 10→20, na 12→24): |Δa₂^agg|/|a₂^agg| ≤ 10⁻⁶; μ-nodes 64→128: ≤ 10⁻⁹; PV quad epsrel 10⁻¹⁰; tail split Q_max 50→100: ≤ 10⁻⁹.
- **F-AGG-UNI (report only):** the banked Q′_G near-universality tested on a₂^agg/Q_T^a across the quartet.

## Consequence (PF-S2, unchanged)
a₂^agg is the grain-scale dispersion coefficient; with P1's lattice-scale a₂ it feeds W_∪′ at fold, after the CC leg. No window action in P2.

## Registers and non-claims
R1-machine for every number; R2 for the aggregate reading (conditional on G-POLY1's E3 elections and the Born/SOA order). No observable, no bridge (M.BRIDGE), no channel-speed-equality claim, no μ_n. Two-leg: chat leg on the recovered framework machinery + the new PV step; CC leg from scratch in a later dispatch.
