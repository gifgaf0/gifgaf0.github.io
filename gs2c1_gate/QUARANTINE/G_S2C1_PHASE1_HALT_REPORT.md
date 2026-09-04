# G-S2C1 — PHASE 1 HALT REPORT (chat leg, September 2, 2026)

**Status: HALTED at directive item 2 (WARD-Γ). The ladder (item 3) was NOT run.** Lock unchanged (prereg 2ea8ec13; T1 8cd89b9a; record f2f4d500).

## Item 1 — re-crystallization: PASS, and the E-3 record point is CONFIRMED
GEM-8 kernel U(r) = 20·exp(−r⁸) in 2-D (Ũ(0) = 56.950947), hexagonal cell a* = 1.46059, n = 64, fixed μ = 53.225. Fixed-μ semi-implicit imaginary time converges in 2,000 steps to ‖Lψ₀‖/‖ψ₀‖ = **1.96×10⁻¹²** (threshold 10⁻¹⁰; 5×10⁴ margin; Newton–Krylov confirms it is at the double-precision fixed point). The resulting mean density is **⟨ρ⟩ = 0.999988** — i.e. the record's (g* = 20, a* = 1.46059, μ = 53.225, ρ₀ = 1) tuple closes on this instrument to 1.2×10⁻⁵ — an independent confirmation of the G-TSH3 first-passing point. ψ₀ spectral tail beyond |m| ≥ 24: 2×10⁻³². λ_min(L) at Γ = **+1.6×10⁻¹⁴**: the Hermitian L^{1/2} BdG form is admissible on this state (the Phase-0 defect was the old state, not the form). ψ₀ md5 in the checkpoint; `psi0_gem8_n64.npy` banked.

## Item 2 — WARD-Γ: FAIL as literally specified; the Ward identity itself holds
Literal criterion (product-form eig, n_b = 32): Goldstone |ω²| = {8.9×10⁻⁹, 4.4×10⁻⁹, **3.5×10⁻⁸**} — third mode exceeds 10⁻⁸ → halt.
Diagnosis (chat-side, all numbers in the checkpoint):
- Analytic translation modes ∂ₓψ₀, ∂ᵧψ₀ under (L+2X): residual **6.6×10⁻¹² / 1.1×10⁻¹¹** (n_b = 32; 2–3×10⁻¹² at n_b = 24) — the Ward identity holds at the stationarity level.
- Dense-eig Goldstone values vs basis: product form 2.1×10⁻⁹ (24) → 3.5×10⁻⁸ (32) → 3.6×10⁻⁸ (40); Hermitian eigh 6.5×10⁻¹⁰ → 3.1×10⁻⁹ → 1.8×10⁻⁸; kinetic cutoff 4,955 → 8,952 → 14,134. The values track (cutoff)²·ε_machine: **a double-precision solver floor, not a property of the substrate.** No state, however stationary, passes the literal criterion by dense eig at n_b ≥ 32 (product) or 40 (Hermitian).
- The Phase-0 threshold was derived in the regime where the offset was governed by stationarity (offset ≈ 16.5 × residual at residual 0.127); at machine-level stationarity the offset is governed by roundoff amplified by the kinetic cutoff — a different regime the threshold statement did not anticipate. **H-S2C-5** (H-2 class: a gate stated on a quantity that hits a numerical floor).

## What the ladder needs (for the author's decision)
The physically relevant requirement is Goldstone offset ≪ ω_T² at the bottom rung (ka = 1.17×10⁻³): with c_T ~ 2–3 that is ω_T² ~ 3–6×10⁻⁶, so the Hermitian floor at n_b = 32 (3×10⁻⁹) is ~10⁻³ of it and enters r(k) at the bottom rung at ~5×10⁻⁴, weighted (ka)² ~ 10⁻⁶ in the a₂ fit — negligible; at the top rung (ω_T² ~ 0.5) the floor is ~10⁻⁸ relative → a₂ precision ~10⁻⁷ < τ. F-CONV (n_b 24/32/40) measures this directly.

**Proposed Amendment A-1 (requires authorization; not applied):** WARD-Γ is satisfied by (a) the analytic-mode Ward residual ‖(L+2X)∂ψ₀‖/‖∂ψ₀‖ ≤ 10⁻⁹ on both legs AND (b) the Hermitian-form Goldstone |ω²| ≤ 10⁻⁸ at the n_b of record with λ_min(L) ≥ −10⁻¹² verified at every k; the dense-eig floor is carried as an explicit uncertainty term in F-CONV. Under A-1 the present state PASSES ((a) 1.1×10⁻¹¹; (b) 3.1×10⁻⁹ at n_b = 32; the ladder would run at n_b ∈ {24, 32, 40} with product-form cross-checks at two rungs). Alternative without amendment: run the ladder at n_b = 24 where the literal product-form criterion holds (2.1×10⁻⁹) — NOT recommended chat-side, since selecting the basis to satisfy a floor-limited gate is Eddington-shaped; the amendment is the honest route.

## Estate
`g_s2c1_phase1.py` (halted at item 2 by design), `g_s2c1_phase1_run.log`, `g_s2c1_phase1_checkpoint.json` (steps 1–2 + diagnosis), `psi0_gem8_n64.npy`. T1: zero hits. PHASE1 ladder: not executed; arms untouched; nothing about W_∪.
