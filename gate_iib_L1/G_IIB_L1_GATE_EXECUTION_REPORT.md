# Gate G-IIB-L1 — Chat-Leg Execution Report

**Date:** July 14, 2026 · **Executor:** chat-side instance · **Status:** chat leg COMPLETE; CC leg PENDING (two-leg rule bars fold until verdict-level comparison).

**Artifact set:** locked prereg `G_IIB_L1_EXECUTION_PREREGISTRATION.md` md5 `acf71fb87763295577d44f672064adfd` (lock authorization "Lock", July 14) · `G_IIB_L1_LSF_DELTA.md` (filed pre-derivation) · `g_iib_l1_chatleg.py` (standalone, sympy 1.14 + Fraction, imports no tool under test) · this report. Sequence honored: lock → LSF-Δ → derivations → quarantined comparison step run last.

---

## 1. Verdict (per the locked arms, precedence applied)

**ARM D — DEGENERATE (UNDERDETERMINED).** No KC is claimed passed. The missing declaration is named: **the M.ONT knot-core ↔ longitudinal-channel coupling class.** The gate stops here per the locked stopping rule (§7): no exploratory continuation inside this gate; re-registration only after the named declaration is made.

| Decision point | Token | Content |
|---|---|---|
| D1 monopole slaving | **PASS** | Steady-state knot sources have time support {ω₀} only; amplitude and phase determined (no free phase); self-frequency content transient in **both** damping regimes (Hurwitz via Vieta); steady-state emission = elastic scattering of the drive (exact energy balance, phasor identity + exact-rational trig spot check). CM-1 re-verified exactly over common periods, 28 rational pairs incl. the 1836 and 1836.15 ratios. |
| D2 dipole reduction | **STRUCTURAL-PASS** | Theorem, both directions: orbital-dipole coefficient A = d(ρ₁m₂ − ρ₂m₁)/(m₁+m₂) = 0 ⟺ ρᵢ = λmᵢ. Sidebands ω₀ ± Ω carry (D₀ω₀/2)·A. Universality itself = the §2.88.A equivalence — **named condition**, not proven here; its registered discharge path is the §2.88.C follow-on on the MV-G1 state. CM-motion term carries no Ω content (verified); its O(V) piece is the D4b(ii) Doppler channel — the two audits cohere. |
| D3 quadrupole onset | **PASS** | 2Ω quadrupole content generic, coefficient B = ρ₁r₁² + ρ₂r₂² > 0; under universality B = λμd² > 0 (does not cancel). Leading orbital emission = quadrupole given D1 + D2's condition. Acoustic twin: co-rotating vortex pair = rotating quadrupole sound (LSF-Δ C2). |
| D4a subsonic motion | **PASS (exact)** | Any static-profile source in uniform subsonic motion radiates **exactly nothing** (Lagrange identity ⇒ empty on-shell intersection; elliptic co-moving operator; 704-combination exact Fraction sweep, zero exceptions). Wake opens exactly at v = c_s (Mach witness). Stronger than linear order. |
| D4b coupling-class dichotomy | **UNDERDETERMINED** | Dichotomy proved: **[static-core-direct]** ⇒ order-one wake sourcing above c_s = φ⁻²c (Gravejat CMP 243 (2003) no-supersonic-traveling-waves + Landau/impurity-drag anchors); **[drive-mediated, uniform drive]** ⇒ zero independent sourcing exactly (every coupling ∝ D₀; D₀→0 decouples), with an O(v) intra-mechanism **Doppler friction toward the substrate rest frame** recorded per the locked "executed and recorded" clause (net radiated momentum ∝ n·(v/c)·P_scat for any positive Doppler exponent n; magnitude ∝ D₀²ρ² — M.CW-walled; prior-art twin: sub-critical Doppler drag, LSF-Δ C1). **The declared corpus does not fix which class the physical knot occupies** — §2.91 silent, §2.88.C explicitly M.ONT-gates "which object pulsates," §3.4 forces a core deficit on any single-component knot, M.ONT row open. |

**Precedence (locked §3):** no unconditional SOURCING; UNDERDETERMINED present ⇒ ARM D. FAIL-dominance not triggered — the class-conditional sourcing lives inside the undetermined classification, exactly the structure the locked arms anticipate.

## 2. Banked findings (verdict-independent; R1 unless noted)

- **T1** — steady-state source support {ω₀}, no free phase, elastic-scattering energy balance.
- **T2** — dipole ≡ 0 ⟺ ρᵢ = λmᵢ (both directions); non-universal response ⇒ the KC1(b) channel. The condition is §2.88.A.
- **T3** — quadrupole onset generic and universality-proof (B = λμd²); supplies Carlip's quadrupole-only premise.
- **T4** — exact subsonic silence for any static profile; wake threshold exactly c_s.
- **T5** — the coupling-class dichotomy (R1) + corpus classification (R2). **Banked constraint on M.ONT:** the single-component-filament-in-longitudinal-ψ branch is structurally **KC3-dead** for v > c_s unless a separate kinematic closure is derived. The KC set has become a constraint *on* M.ONT.

**Contingent ladder (recorded, not claimed):** IF M.ONT ⇒ drive-mediated-only: D1+D3+D4 carry KC1(a), KC2's premises, and KC3 at the independent-sourcing level; KC1(b) conditional on §2.88.A ⇒ Arm-B-equivalent contingent verdict, Doppler-friction magnitude gate outstanding. IF M.ONT admits any static-core-direct longitudinal coupling ⇒ KC3 fires structurally ⇒ Arm-C path, §2.91.D blast radius.

## 3. Eddington / quarantine attestation

The four KC thresholds (1.3×10⁻⁴; α₀² < 2×10⁻⁵; 2×10¹⁰c; 2×10⁻¹⁵c/2×10⁻¹⁹c) appear in exactly one function, `comparison_step()`, executed last; the derivation phase is threshold-blind and proves vanishing/order structure only. No numeric target existed or was introduced. No constant selected post hoc. No observable, no magnitudes for ρ_s, Z₀, ω₀, D₀.

## 4. Honesty ledger

1. **Self-caught bug (falsifier fired as designed, first run):** original D1.4 asserted Re(root) = −γ/2 — false in the overdamped regime. Corrected to the Hurwitz-stability theorem (Vieta exact + sign lemma, proved and grid-falsified over 81 exact pairs). The fix **strengthens** the claim (transient decay in both regimes); no check weakened.
2. **Execution-level interpretation (stated in the LSF-Δ):** locked §5's "appended to this prereg" executed as a companion artifact citing the lock MD5, preserving the §8 freeze — BD-IIB-1 precedent. Not an amendment.

## 5. Scope confirmations

Linear order only; fluid branch only; no effective metric; no §3.x; no register change to anything prior; no Pin/spin content; §2.87.J untouched (reserved for G-2a-L1); **the §2.52 Open 3 row untouched per standing instruction.** Assertions passed: **843.**

## 6. CC-leg dispatch specification (two-leg rule)

Independent build, zero shared machinery, same five decision points, verdict-level comparison; disagreement → S9. Required independent constructions: (i) CM-1 averages by a different method (e.g., complex-exponential orthogonality over exact periods); (ii) Hurwitz stability via Routh–Hurwitz or explicit-discriminant case split; (iii) the dipole ⟺ universality theorem from the N-body deviation decomposition rather than the 2-body witness; (iv) the on-shell intersection theorem via a different inequality route (e.g., Cauchy–Schwarz over an independent parameterization) with its own exact grid; (v) the Doppler O(v) asymmetry with an independently derived kernel exponent (Liénard–Wiechert construction), coefficient cross-checked. Comparison items: the five tokens + the arm + the named missing declaration + the banked constraint. **Fold eligibility:** only after two-leg verdict agreement and explicit author fold authorization; target placement §2.91.F or as assigned at fold.

## 7. Consequence routing

The mandatory-first computation of the II-B phase has executed and **routes the program to M.ONT**: the II-B phase is now formally blocked on the M.ONT knot-core ↔ longitudinal-channel coupling-class declaration — which this gate has converted from an open ontology question into a declaration with pre-computed, KC-anchored stakes on each branch.

*Filed July 14, 2026. Chat leg complete. Nothing folds without the CC comparison and explicit authorization.*
