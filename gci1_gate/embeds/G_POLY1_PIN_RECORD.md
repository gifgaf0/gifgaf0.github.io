# G-POLY1 PIN RECORD — E3-PIN-COMPLETE + HS-PIN

**Locked under:** exec prereg `dab462d2e133d0962c512a34bb7bc635`; staging memo `68623d68…`; base V4.73 `e48f5c52…`. Supplements E3-PIN v1 (He, arXiv:1706.09137). Transcription-before-evaluation: nothing below was consumed before being written here.

## E3-PIN-COMPLETE — source: Roy & Kube, J. Mech. Phys. Solids 203 (2025) 106237 (open access, NSF-PAR 10623592). FOSA sector ≡ Weaver JMPS 38, 55 (1990) ≡ Stanke–Kino JASA 75, 665 (1984) (equivalence per the source §1, §4.1, Fig. 1).

Transcribed, with source equation numbers:
- **(12)** ⟨δC(x₁)δC(x₂)⟩ = Ξ·η(x₁,x₂); **(13)/(A.1)** Ξ = ⟨C⊗C⟩ − ⟨C⟩⊗⟨C⟩, orientation average over SO(3), untextured.
- **(14)** C_ijkl = c₁₂δ_ij δ_kl + c₄₄(δ_ik δ_jl + δ_il δ_jk) + ν Σₙ a_in a_jn a_kn a_ln, **ν ≡ c₁₁ − c₁₂ − 2c₄₄**.
- **(15)** ⟨aaaa⟩ = (1/5)(δδ+δδ+δδ); reference medium c⁰₁₂ = c₁₂+ν/5, c⁰₄₄ = c₄₄+ν/5, c⁰₁₁ = c⁰₁₂+2c⁰₄₄; ρV²_L0 = c₁₂+2c₄₄+3ν/5, ρV²_T0 = c₄₄+ν/5 (= G_Voigt).
- **(17)–(18)** η(r) = e^(−r/a); η̃(q) = a³/(π²(1+q²a²)²) [(2π)⁻³ FT convention; He Eq. (71)'s 8πa³ form is the same object × (2π)³ — convention reconciled here, no conflict].
- **(A.3)–(A.4)** Ξ = a·T_A + b·T_B + c·T_C with **a = 2ν²/1575, b = −ν²/630, c = ν²/180**; T_A = the 9 latin-latin × greek-greek delta pairings; T_B = the 24 latin↔greek perfect matchings; T_C = the 72 mixed pairings (one LL + one GG + two LG). [(A.5)–(A.7) descriptive forms.]
- **(3), (30), (61)–(63)** FOSA self-energy; vertex ∇_j(δc_ijkl ∇_l u_k); slot roles pol/outer-grad/propagator/inner-grad (assignment immaterial under the full elasticity symmetry of δC — noted, and moot for cubic where δC is totally symmetric).
- **(41), (45)–(48)** dyadic propagator split; Im g₀M(s) = −π δ(s−k_M0)/(2ρV²_M0 k_M0).
- **(49)–(58)** dispersion k² = k²₀[1−m̃]⁻¹; α = Im k; m̃ scaled per (51)–(52).
- **(69) A-scalar anchor (clean):** A(θ) = (ν²/525)(3+cos²θ)² — **mandatory machine-reproduction falsifier** for the contraction machinery. Independently hand-verified at θ=0: A(0) = ν²·Var(Σnᵢ⁴) with Var = 41/105 − 9/25 = 16/525 ⇒ 16ν²/525 ✓. The retrieved B/C digit strings were corrupted in transport and are **NOT consumed**; every contraction is machine-computed from the pinned Ξ, with the A-anchor as the gate.
- **(81)–(82)** ε_L = √(4ν²/525)/c⁰₁₁, ε_T = √(3ν²/700)/c⁰₄₄ — recomputed as controls (Born validity: ε² ≪ 1).

**Convention resolutions (E2-witness class, logged pre-evaluation):** (i) overall self-energy sign fixed by Im k_M ≥ 0 (physical attenuation); (ii) the scattering theory's reference medium is the **Voigt** average ⟨C⟩ (source-pinned) — role-distinct from the E4 **Hill** verdict speeds; no collision: Q_T is a property of the pinned scattering theory, verdict propagation speeds remain Hill.

**Hexagonal arm (declared generalization route):** Ξ_hex = ⟨C⊗C⟩ − ⟨C⟩⊗⟨C⟩ by exact-degree SO(3) quadrature (zyz Euler: Gauss–Legendre in cosβ, n=10; uniform α,γ grids, n=12; integrand band-limit 8 — quadrature exact with margin), **validated to machine precision against the pinned cubic closed form before any hexagonal use**; the pinned machinery (12)–(13), (61)–(63), (41)–(58) is symmetry-agnostic and applied unchanged. The paywalled hexagonal closed forms (JASA 143, 219 (2018) line) are not consumed. Falsifiers: cubic closed-form reproduction; isotropic-input null Ξ ≡ 0.

**Rayleigh assembly (machine, from pinned pieces only):** α_P·a = Q_P·(k_P0 a)⁴ with
Q_P = Σ_{M∈{L,T}} (V_P0/V_M0)³ / (2 V²_P0 V²_M0) · ∫₋₁¹ Φ_PM(μ) dμ, ρ = 1,
Φ_PM(μ) = Ξ contracted with [ext-pol_P ⊗ p̂p̂ ⊗ dyad_M(ŝ) ⊗ ŝŝ] on both vertices (P-pol: p̂p̂ for L, (δ−p̂p̂)/2 for T; M-dyad: ŝŝ for L, δ−ŝŝ for T), μ = p̂·ŝ.
Cross-checked in-instrument against the finite-η̃ evaluation: exponent-4 fit and prefactor→Q_P agreement are falsifiers.

## HS-PIN — source: Zemlyakov & Chugunov, arXiv:2507.12266 (open access)

**CUBIC — COMPLETE.** Eqs. (9)–(10), verbatim:
μ_HS⁽¹⁾ = (c₁₁−c₁₂)/2 + 3·[ 10/(2c₄₄−c₁₁+c₁₂) + 24(K+c₁₁−c₁₂) / (5(c₁₁−c₁₂)(3K+2c₁₁−2c₁₂)) ]⁻¹
μ_HS⁽²⁾ = c₄₄ + [ 5/(c₁₁−c₁₂−2c₄₄) + 9(K+2c₄₄) / (5c₄₄(3K+4c₄₄)) ]⁻¹
with K = (c₁₁+2c₁₂)/3 (exact for cubic). Role: c₄₄ > (c₁₁−c₁₂)/2 ⇒ (1) = lower, (2) = upper — the case for both cubic configs here (Zener > 1). K≫c limit forms Eqs. (11)–(12); **implementation control** = the source's Table I bcc Coulomb-crystal row (c₄₄ = 0.1828, c₁₁−c₁₂ = 0.0490 → VR 0.0510/0.1195, HS 0.0712/0.1028), hand-verified against (11)–(12) to 4 digits pre-coding. Source Eqs. (4)–(8) independently re-confirm the Phase-0a cubic VRH transcription.

**HEXAGONAL — PENDING.** Named transcription sources: Berryman, JMPS 53, 2141 (2005); Peselnick–Meister (1965); Watt–Peselnick, JAP 51, 1525 (1980); Kube–Argüelles, Comput. Geosci. 95, 118 (2016) (iterative any-symmetry scheme). Obligation: transcribe-and-execute before Phase 3 (E4 band completeness). VR bounds stand in for hexagonal configs until pinned. No from-memory hexagonal HS coefficients are used anywhere.

---
# SUPPLEMENT (Aug 4, 2026 session) — cross-source redundancy + hexagonal HS upgrade

## S1. E3 cross-source: He, arXiv:1710.03828 (He-2; fetched in full this session)
Same FOSA/SK-Weaver operator class, stated for **arbitrary crystal symmetry** ("we neglect the unique symmetry of different types of crystals, and treat them as generally anisotropic materials" — Appendix). Serves as an independent redundancy pin for the CC leg; the chat-leg instrument consumes the Roy–Kube assembly above.
- Covariance = SO(3) Haar average, normalized measure (8π²)⁻¹ sinθ dφ∧dθ∧dψ — Eqs. (28)–(29), (33); Euler convention Q = R(ψ)R(θ)R(φ), ranges [0,2π)×[0,π]×[0,2π) — (A2), (A7)–(A8).
- SAF P(r) = e^(−r/a), P̃(k) = 8πa³/(1+k²a²)² — (30)–(31) ["a … generally considered as the average radius of the grains"]; dimensionless ᾱ = α·d, K̄₀ = k₀·d with **d = 2a** — (51)–(52). [Same object as Roy–Kube (17)–(18) × (2π)³ — reconciliation already logged above.]
- Transverse dispersion **M₁₁M₈₈ − M₁₈² = 0** — Eq. (50); M₁₁ = μ(k²−k_T²) − K₄₄k², M₁₈ = −K₄₄ik — (46a);
  **M₈₈ = K₄₄ − [⟨Ξ₁₅²⟩+⟨Ξ₂₅²⟩]Σ₄₄ − 2⟨Ξ₁₅Ξ₂₅⟩Σ₄₅ − 2[⟨Ξ₁₅Ξ₃₅⟩+⟨Ξ₂₅Ξ₃₅⟩]Σ₆₆-class per (46i) verbatim: … − ⟨Ξ₃₅²⟩Σ₆₆ − [⟨Ξ₄₅²⟩+⟨Ξ₅₅²⟩]Σ₇₇ − ⟨Ξ₅₆²⟩Σ₉₉** — (46i); pinned transverse Voigt-pair set **{15,25,35,45,55,56}**; M₂₂=M₁₁, M₂₇=M₁₈ — (46j); Σ₅₅=Σ₄₄, Σ₅₆=Σ₄₆, Σ₈₈=Σ₇₇ — (48e).
- K₁₁ = 3(λ+6μ)(λ+2μ)/(3λ+8μ), K₁₂ = 3(λ+μ)(λ+2μ)/(3λ+8μ), K₄₄ = 15(λ+2μ)μ/[2(3λ+8μ)] — (47); singularity constants S₁₁₁₁ = (2λ+7μ)/[15μ(λ+2μ)], S₁₂₂₁ = −(λ+μ)/[15μ(λ+2μ)], S₂₂₃₃ = (3λ+8μ)/[30μ(λ+2μ)] — (14)–(17); Σ-kernels (48a)–(48d) as Σ_ab = S-const − (8π³)⁻¹∫ s_i s_j G̃_ij(s)P̃(k−s)d³s.
- Ξ = Π[I+SΠ]⁻¹ — (25) (Born limit Ξ→δc, the E3-elected weak-fluctuation class); Voigt reference λ̄,μ̄ — (54); ε = |c₁₁−c₁₂−2c₄₄|/c₁₁⁰ — (53).
- **Benchmark hook (Tables 1–2):** Al C₁₁=103.4, C₁₂=57.1, C₄₄=28.6 GPa, ρ=2700 → λ̄=54.92, μ̄=26.42 GPa, V̄_T=3128.13, V̄_L=6317.52 m/s. Instrument must reproduce from (54) (SI units in this control only).

## S2. HS-PIN hexagonal — UPGRADE (Berryman SEP-125 appendix, node10 + node11, fetched verbatim this session)
Lineage: Peselnick–Meister JAP 36, 2879 (1965); Watt–Peselnick JAP 51, 1525 (1980); product formulas Berryman 2004b; journal statement Berryman JMPS 53, 2141 (2005).
**Machinery (node10):** (22) K_V = [2(C₁₁+C₁₂)+4C₁₃+C₃₃]/9; (23) G_V = (1/5)(G_eff^v + 2C₄₄ + 2C₆₆); (24) **G_eff^v = (C₁₁+C₃₃−2C₁₃−C₆₆)/3**; (25) 1/(K_R−C₁₃) = 1/(C₁₁−C₆₆−C₁₃) + 1/(C₃₃−C₁₃); (26) G_R = [(1/5)(1/G_eff^r + 2/C₄₄ + 2/C₆₆)]⁻¹; product formulas **3K_R G_eff^v = 3K_V G_eff^r = ω₊ω₋/2 = C₃₃(C₁₁−C₆₆)−C₁₃²** ⇒ G_eff^r = K_R G_eff^v/K_V.
**PMW/HS bounds (node11):** (27) **K_HS^± = K_V(G_eff^r + ζ±)/(G_eff^v + ζ±)**; (28) ζ± = (G±/6)(9K±+8G±)/(K±+2G±); (29) K± = K_V(G_eff^r−G±)/(G_eff^v−G±); (30) 0 ≤ G₋ ≤ min(C₄₄, G_eff^r, C₆₆); (31) max(C₄₄, G_eff^v, C₆₆) ≤ G₊ ≤ ∞; (33) α± = −1/(K±+4G±/3), β± = 2α±/15 − 1/(5G±).
**(32) shear bounds: 1/(G_hex^± + ζ±) = (1/5)[⟨FIRST TERM ELIDED in source rendering⟩ + 2/(C₄₄+ζ±) + 2/(C₆₆+ζ±)] — NOT reconstructed.** α±, β± enter within the elided fragment. Watt–Peselnick note (verbatim): a later condition permits C₄₄ to be replaced in some circumstances by G_eff^r.
**Consistency identity (derived-class, labeled):** at ζ = 0 with first term 1/G_eff^r, (32) reproduces (26) exactly; and 3K_V G_eff^r = C₃₃(C₁₁−C₆₆)−C₁₃² = ½[(C₁₁+C₁₂)C₃₃−2C₁₃²] — identical to the independently pinned arXiv:1606.03700 G_R. Two pinned hex-Reuss statements = one formula.
**Status upgrade:** hex **K_HS^± COMPLETE** ((27)–(31), evaluable now for step:AB); hex **G_HS^± PENDING-verbatim** (one elided term; completion source: Berryman JMPS 53, 2141 (2005) or PRB 85, 094204 appendix — OSTI purl/1082188 returned 502 this session; obligation before Phase 3; V/R shear bracket stands in, disclosed).

## S3. Consolidated status
- **E3-PIN-COMPLETE: COMPLETE** — primary Roy–Kube assembly (above) + He-2 redundancy (S1); both arms covered; A(θ)-anchor is the hard machine gate; corrupted B/C digit strings remain un-consumed.
- **HS-PIN:** cubic COMPLETE (Eqs. (9)–(10) + role rule + Table-I control); hex K COMPLETE (S2); hex G PENDING-verbatim (S2).
- **Input map for Phase 0b/1 this leg:** step:AB hex → 1a+1b full, K_HS^± now, G_HS pending; gem8:FCC cubic → 1a+1b full, μ_HS full; step:FCC cubic → 1a full (K-free), 1b T→T partial + full-Q_T BLOCKED on K (c₁₁,c₁₂ input-gap; the K-free simplified HS forms (11)–(12) are out of regime and are not used); gem8:AB hex → INPUT-GAP.
