# G-IIB-L1 — CC-Leg Report (independent second leg)

**Date:** 2026-07-14 · **Locked pre-registration:** `G_IIB_L1_EXECUTION_PREREGISTRATION.md`
(md5 `acf71fb87763295577d44f672064adfd`) · **Chat leg:** `g_iib_l1_chatleg.py` +
`G_IIB_L1_GATE_EXECUTION_REPORT.md` · **LSF-Δ:** `G_IIB_L1_LSF_DELTA.md` (chat, pre-derivation) ·
**Script:** `g_iib_l1_ccleg.py` (sympy 1.14 + `fractions`, imports no tool under test).

> **Two-leg result: VERDICT-LEVEL AGREEMENT.** The CC leg independently reproduces the chat leg's
> five tokens, the arm (**ARM D — DEGENERATE/UNDERDETERMINED**), the named missing declaration, and
> the banked constraint — using the report §6-mandated *different methods* for each decision point.
> No S9 counter-cross-check triggered.

## Independence (report §6 (i)–(v), honored)
| Point | Chat method | CC method (this leg) |
|---|---|---|
| (i) CM-1 averages | direct trig integration over common periods | **complex-exponential orthogonality** — ⟨e^{iΩt}⟩ over the exact common period T, Ω=w₁±w₂ |
| (ii) Hurwitz stability | Vieta + sign lemma | **Routh–Hurwitz first column** (regime-agnostic) **+ explicit discriminant case split** |
| (iii) dipole ⟺ universality | 2-body witness | **N-body deviation decomposition** (N=2,3,4; ρ_i=λm_i+δ_i, CM-projected internal dipole) |
| (iv) subsonic silence | Lagrange identity | **Cauchy–Schwarz** (as an explicit sum-of-squares) + **own exact Fraction grid** (fifths) |
| (v) Doppler O(v) | generic Doppler exponent n | **Liénard–Wiechert retardation kernel** — fixes n_LW = 3 (dipole power/solid-angle) |

All five constructions are distinct from the chat leg's. Notably, the **Routh–Hurwitz route for D1.4
sidesteps the chat's self-caught bug entirely** (for a degree-2 polynomial, all-coefficients-positive
⟹ stable, with no root computation), and the **Liénard–Wiechert construction fixes the chat's generic
Doppler exponent to n_LW = 3** while reproducing the same (n/3)(v/c) net-momentum structure.

## Decision points (tokens match)
- **D1 — PASS.** CM-1 zero-average verified over 28 rational pairs (incl. the 1836 and 1836.15
  proton/electron ratios) via complex-exponential orthogonality; equal-frequency kernel = cos(p)/2;
  monopole radiated power P_rad = ρA²ω²/(8πc) > 0 (Parseval, cross-checked vs the trig integral) ⇒
  γ_rad>0; **Hurwitz stability in both damping regimes** (Routh–Hurwitz + discriminant case split) ⇒
  self-frequency content transient; unique steady response at ω₀ (no free phase); exact
  elastic-scattering energy balance ⟨P_in⟩=⟨P_rad⟩.
- **D2 — STRUCTURAL-PASS.** N-body decomposition (N=2,3,4): the CM-projected internal dipole
  Σδ_ix_i vanishes for all internal motions **iff δ_i/m_i is constant**, i.e. ρ_i = λm_i (both
  directions). The universality condition is the §2.88.A equivalence — the **named hinge**, not proven
  here.
- **D3 — PASS.** Quadrupole carries 2Ω with B = ρ₁r₁²+ρ₂r₂² > 0; under universality B = λμd² > 0
  (no cancellation) ⇒ leading orbital emission at quadrupole (the GR-template premise for KC2).
- **D4a — PASS (exact).** Subsonic silence via Cauchy–Schwarz ⇒ empty on-shell intersection ⇒
  elliptic co-moving operator ⇒ radiated power = 0 exactly; own exact fifths-grid sweep (all subsonic
  (v,k) strictly positive); Mach witness ⇒ wake opens exactly at v = c_s.
- **D4b — UNDERDETERMINED.** Dichotomy proved: **[static-core-direct]** ⇒ order-one wake sourcing
  above c_s (Gravejat CMP 243 (2003) / Landau-drag anchors); **[drive-mediated, uniform drive]** ⇒
  zero independent sourcing exactly (all coupling ∝ D₀; D₀→0 decouples), with an O(v) Liénard–Wiechert
  **Doppler friction toward the substrate rest frame** recorded (n_LW=3; magnitude ∝ D₀²ρ² —
  M.CW-walled). The declared corpus does not fix which class the physical knot occupies ⇒ M.ONT-gated.

## Comparison (report §6 comparison items)
| Item | Chat | CC | |
|---|---|---|---|
| D1 | PASS | PASS | ✔ |
| D2 | STRUCTURAL-PASS | STRUCTURAL-PASS | ✔ |
| D3 | PASS | PASS | ✔ |
| D4a | PASS | PASS | ✔ |
| D4b | UNDERDETERMINED | UNDERDETERMINED | ✔ |
| **arm** | **ARM D** | **ARM D** | ✔ |
| missing declaration | M.ONT knot-core↔longitudinal-channel coupling class | (same) | ✔ |
| banked constraint | single-component-filament-in-longitudinal-ψ is KC3-dead for v>c_s unless a separate kinematic closure is derived | (same) | ✔ |

**Verdict-level agreement on every comparison item ⇒ no disagreement, no S9.**

## Eddington / quarantine (held)
The four KC thresholds (1.3×10⁻⁴; α₀²<2×10⁻⁵; 2×10¹⁰c; 2×10⁻¹⁵c/2×10⁻¹⁹c) appear in exactly one
function, `comparison_step()`, executed **last**; the derivation phase is threshold-blind (proves
vanishing/order/sign structure only). No numeric target existed or was introduced; no observable, no
magnitudes for ρ_s, Z₀, ω₀, D₀. **1148 assertions passed.** Linear order, fluid branch; no effective
metric; no §3.x; no register change; no Pin/spin content; §2.87.J untouched; **§2.52 Open 3 untouched.**

## Honesty notes
- The chat leg self-caught a D1.4 bug (Re(root)=−γ/2 is false overdamped) and fixed it to Hurwitz.
  My independent method (**Routh–Hurwitz**, regime-agnostic) never encounters that root form — it
  confirms stability from the coefficient signs alone. I *did* hit a related sympy pitfall (the
  underdamped `sqrt(4ω_i²−γ²)` sign is unknown to sympy) and fixed it by representing that discriminant
  as a positive real symbol — a tooling detail, not a claim change.
- **This leg proves nothing physical beyond the locked derivation structure.** It takes no position on
  the fluid/solid branch, the KCs, or the M.ONT declaration; it does not fold. Fold eligibility (per
  report §6) is two-leg verdict agreement (now achieved) **+ explicit author authorization**, target
  §2.91.F or as assigned — not granted here.

## Consequence
The CC leg confirms the chat leg's routing: **the II-B phase is formally blocked on the M.ONT
knot-core↔longitudinal-channel coupling-class declaration**, now a declaration with pre-computed,
KC-anchored stakes on each branch (drive-mediated ⇒ Arm-B-equivalent contingent verdict with a Doppler
magnitude gate outstanding; any static-core-direct coupling ⇒ Arm-C / §2.91.D blast radius).
