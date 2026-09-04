# CC-leg derivation of the analytic second-order coefficient D2 (written before any numeric run; own derivation)

**Disclosure up front:** Addendum P2-A travels raw in the dispatch, so its D2 formula was *visible* before this
derivation was written down. What follows is nevertheless derived from the Addendum-P2 operational definition
alone (the D(k) integral), every step shown; §5 then compares the result against P2-A's stated form. The
derivation was drafted from the P2 definition and my own SOA re-derivation of that definition, not by
manipulating P2-A's expression backwards.

## 1. Setup (Addendum P2 operational definition, re-derived)

For a statistically isotropic, exponentially correlated (a_g = 1) polycrystal, second-order (Born/SOA)
self-energy of the incident mode I with density-normalized moduli c = C/ρ, δc(x) = c(g(x)) − ⟨c⟩:

  Σ_I(k, ω) = k² Σ_M ∫ d³q q² η̃(|k − q|) Φ_IM(k̂·q̂) / (ω² − V_M² q²),   η̃(q) = 1/(π²(1+q²)²),

where Φ_IM(μ) is the SO(3)-averaged squared matrix element ⟨(û_i p̂_j δc_ijkl ŝ_l û'_k)²⟩ with the incident
polarization averaged (T: ½(I − p̂p̂); L: p̂p̂) and the scattered mode's polarizations summed (T: I − ŝŝ; L: ŝŝ).
η̃ carries the 1/(2π)³-convention Fourier transform of e^{−r}: 8π/(1+q²)² / (2π)³ = 1/(π²(1+q²)²). On shell
(ω = V_I k), with d³q = 2π q² dq dμ, the π² cancels and

  Δc_I/c_I(k) ≡ D(k) = Re Σ_I/(2V_I²k²) = (1/π) Σ_M N_M J_M(k),   J_M(k) = PV∫₀^∞ dq q⁴ F_M(q,k)/(k_M² − q²),
  F_M(q,k) = ∫₋₁¹ dμ Φ_IM(μ)/(1 + k² + q² − 2kqμ)²,   k_M = k V_I/V_M,   N_M = 1/(V_I² V_M²),

and the imaginary part gives α_I(k) = Σ_M k k_M³ (N_M/2) F_M(k_M, k) — exactly the banked Addendum-P2 forms
(this fixes every constant: the same derivation yields both the banked α and this D, so the KK tie-in F-AGG-KK
validates the normalization chain end to end). Sign: k_eff² = k² − Π, positive attenuation.

## 2. Evenness of Φ_IM (the structural input)

In the squared matrix element each of ŝ and û' appears an even number of times (ŝ_l ŝ_q from the two copies,
plus the scattered projector, itself even in ŝ). Sending ŝ → −ŝ maps μ → −μ and leaves the contraction
invariant, so Φ_IM(−μ) = Φ_IM(μ): the kernels are **even polynomials in μ of degree ≤ 4** (a rank-8 isotropic
covariance contracted with four fixed unit vectors). Write I₀ = ∫Φ dμ, I₂ = ∫Φ μ² dμ; all odd moments vanish.
(The instrument verifies the evenness numerically; this is also the pre-data root of a₃ ≡ 0 — see §4.)

## 3. Small-k expansion of J_M

With A₀ = 1 + q², ε = k² − 2kqμ (|ε|/A₀ ≤ 2k/√(1+k²) uniformly in q, so the expansion is uniform):

  1/(A₀ + ε)² = 1/A₀² − 2ε/A₀³ + 3ε²/A₀⁴ − O(ε³)
  ⇒ F_M(q,k) = I₀/A₀² + k² F₂(q) + O(k⁴),   **F₂(q) = −2I₀/A₀³ + 12 q² I₂/A₀⁴**

(the O(ε) μ-odd piece 4kqμ/A₀³ and the O(ε³) μ-odd pieces integrate to zero against even Φ; the ε² term keeps
only its (2kqμ)² part at O(k²), giving 3·4k²q²μ²/A₀⁴ → 12q²I₂/A₀⁴; the −2ε/A₀³ term keeps −2k²I₀/A₀³).

For the PV denominator use the exact identity 1/(k_M² − q²) = −1/q² − k_M²/q⁴ + k_M⁴/(q⁴(k_M² − q²)):

  J_M(k) = −∫₀^∞ q² F_M(q,k) dq − k_M² ∫₀^∞ F_M(q,k) dq + k_M⁴ PV∫₀^∞ F_M(q,k)/(k_M² − q²) dq.

Third term: scaling q = kx gives k_M⁴ (1/k) PV∫ F_M(kx,k)/(r_M² − x²)k... = k³ r_M⁴ PV∫₀^∞ F_M(kx,k) dx/(r_M² − x²),
and since F_M(kx,k) → I₀·(1+O(k²x²…))⁻²-type with PV∫₀^∞ dx/(r² − x²) = 0 exactly, the bracket is O(k), so the
whole term is **O(k⁴): no k³ term arises** (the pole region kills it through the vanishing of the PV integral,
and every other candidate odd term already vanished by evenness of Φ).

With ∫₀^∞ dq/A₀² = π/4, ∫ q²/A₀² dq = π/4, ∫ q²/A₀³ dq = π/16, ∫ q⁴/A₀⁴ dq = π/32:

  J_M(k) = −(π/4) I₀ + k² [ −∫₀^∞ q² F₂(q) dq − r_M² (π/4) I₀ ] + O(k⁴),   r_M = V_I/V_M,

  −∫ q²F₂ dq = 2I₀(π/16) − 12I₂(π/32) = (π/8) I₀ − (3π/8) I₂.

## 4. Result

  D(0) = −(1/4) Σ_M N_M I₀^{M}   (matches the P2 anchor), and **D(k) = D(0) + D2 k² + O(k⁴)** with

  **D2 = (1/π) Σ_M N_M [ −∫₀^∞ q² F₂(q) dq − r_M² ∫₀^∞ F₀(q) dq ]**,  F₀ = I₀/A₀²,
  **   = Σ_M N_M [ (1 − 2 r_M²) I₀^{M}/8 − (3/8) I₂^{M} ]**   (fully closed form; no quadrature needed beyond
        the exact polynomial moments I₀, I₂ of the kernels).

All corrections are even in k (Φ even ⇒ F_M is a function of k², q² only ⇒ J_M analytic in k² at this order);
the pre-registered k³ term is derived to be exactly zero, and the ladder remainder R(k) = Δ − D2k² should fit
the pure even basis {k⁴, k⁶, k⁸} — which the instrument tests against {k³, k⁴} and {k⁴, k⁴ ln k}.

## 5. Comparison with Addendum P2-A (written after §1–4)

P2-A states D2 = (1/π)Σ_M N_M[−∫₀^∞ q²F₂(q)dq − r_M²∫₀^∞ F₀(q)dq] with F₂ = −2I₀/A³ + 12q²I₂/A⁴, A = 1+q²,
r_M = V_inc/V_M. This is **identical, term for term**, to the §3–4 result (same F₂, same pole/static split,
same r_M² piece), before closed-form evaluation of the q-integrals. CC leg: **CONFIRMS the P2-A formula**, and
additionally reduces it to the elementary closed form D2 = Σ_M N_M[(1−2r_M²)I₀/8 − 3I₂/8].
