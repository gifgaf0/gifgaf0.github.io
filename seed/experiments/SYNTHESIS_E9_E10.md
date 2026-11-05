# Closed loops of fractional-flux strings: what the pre-registered tests of E9 and E10 found

*Synthesis of experiments E9 and E10. Matthew Gifford, November 4, 2026. Label: Exploration. This note summarizes the reports listed in §7 and adds no new computation. Where it and a report differ, the report governs. Branch `claude/seed-step3-first-closure`, head at writing: 79596b5.*

## 1. The question

Can a closed loop of string carrying exactly one third of a magnetic flux quantum settle at a finite size, instead of shrinking away or dissolving?

Without some stabilizer, a closed loop of string in a field theory shrinks: its energy is mostly tension, which falls with length. The question is whether any of the natural stabilizers holds a loop open, in two models where thirds of flux arise:

- **Route A (E9).** Three complex scalars with one U(1) gauge field and a Josephson coupling η. A vortex in one component carries 1/3 of a flux quantum when the three densities are equal. Step 2 confirmed this: the fraction is 1/3, and an isolated third is confined (logarithmically at η = 0, linearly at η > 0). The free object is the composite of all three.
- **Route B (E10).** U(3) gauge theory with three flavours in the colour-flavour-locked vacuum (the single-coupling model of Auzzi, Eto and Vinci, with one parameter λ; BPS at λ = 1). Here the elementary string carries exactly 1/3 of the U(1) flux by group structure. It is a free, finite-tension string with its own internal orientation in CP².

All tests were pre-registered before any code for that test ran. Amendments written after seeing results are labelled post-hoc in their documents.

## 2. Stabilizers tried, and results

| # | Model | Stabilizer | Configuration | Result |
|---|---|---|---|---|
| 1 | A | Topological twist (Hopf charge 1) and the gauge field | Composite ring with strand 1 linked once; 4 cells of (κ, η), 2 starts each | **COLLAPSE** in all 8 runs. The twist is lost by merging onto the core or by a point reconnection; no pause at any radius. |
| 2 | A + core field σ | Charge and current on a core condensate (vorton) | Straight-string scan, then an axisymmetric ring | Ring **STABLE (axisymmetric)**, but **the string is not required**: the same σ ring without the vortex is about 5 % cheaper, and a charged σ lump is cheaper still. |
| 3 | A, strands locked to space | Chiral (Lifshitz) term γψ*·(D×ψ) | 1D vacuum calculation, then twisted rings at γ = ±0.1, ±0.2, ±0.3 | 1D: the uniform vacuum is stable only for \|γ\| < 0.3535 (η = 0.1); the soft mode is the relative phases, not the director. Ring: **COLLAPSE** in all 12 runs. ±γ behave alike, so the chiral gain is not tied to the twist's handedness. |
| 4 | B | Charge and twist on the string's own orientation moduli (intrinsic vorton) | Calibration, straight-string scan, verification, axisymmetric ring at n = 3 and 5 | The straight-string window is **confirmed** at λ = 1 (box, resolution and full 2D checks). Ring **METASTABLE** at both n: it stops within 2 % of the predicted radius from both starts. But **the string is not required**: a vortex-free charged lump is 9–10 % cheaper. |
| 5 | B | — (diagnostic) | Where vortex-free charged lumps bind, λ ∈ {0.8, …, 1.2} | **TRACKS.** Lumps bind exactly where the straight-string window exists (λ ≤ 1) and nowhere else on the grid. |

**In one sentence.** No loop was held open by topology alone. Every loop held open by charge was beaten by a charged lump that needs no string, and in Route B the conditions for the two coincide.

## 3. Three results worth keeping, independent of any wider picture

### 3.1 A no-go for relative-phase vortons in Route A

In a model where all components condense in the vacuum, every finite-energy stationary configuration has equal frequencies in all components. A common frequency is a gauge shift. So no relative phase can rotate in a localized way, and a vorton needs a field that vanishes in the vacuum.

Sketch: finite energy requires ω_k + eA₀(∞) = 0 for every condensed component. At η = 0 the relative charges are carried by massless modes; at η > 0 they are not conserved.

Source: `E9_three_strand_closure/PREREG_option4.md` §0.2.

### 3.2 An identity for thin charged rings (derived, checked against data)

For a straight string of tension T, write ℰ(k, q) = T + k²J + ω²I, where:
- k is the twist per unit length,
- q = 2ωI is the charge per unit length,
- J and I are the twist and charge inertias.

The thin-ring equilibrium function is 𝒯 = ℰ − k∂_kℰ − q∂_qℰ = T − k²J − ω²I. Therefore:

  **ℰ = 2T − 𝒯**, and at equilibrium (𝒯 = 0): **ℰ = 2T, ℰ/q = T/(ωI)**.

**Check.** At E10's selected bracket, E − 2T = −0.489 and +0.168, against 𝒯 = +0.491 and −0.165. The difference is finite-difference error.

**Consequence.** Charge stays bound only if ω < m (the lightest charged bulk mass). So a thin charged ring can have energy below the cost of dispersing its charge (m per unit charge) only if

  **T/I < m².**

At E10's selected point T/I ≈ 1.04 m², so the ring could not beat dispersal whatever the loop dynamics did. B4 confirmed this: E = 1.066 m·Q. This inequality screens any proposed charge-supported closure in this class of models before a loop is built.

Source: `E10_u3_vortices/STATUS_routeB.md`.

### 3.3 In Route B, the string's charge window and the bulk Q-ball switch on together

| | λ = 0.8 | 0.9 | 1.0 | 1.1 | 1.2 |
|---|---|---|---|---|---|
| Straight-string window (string holds charge) | yes | yes | yes | no | no |
| Vortex-free charged lump binds (E < m·Q) | yes | yes | yes | no | no |

Both switch off between λ = 1.0 and 1.1. That is where the lightest bulk mode changes from the scalar (mass λ) to the vector (mass 1), and where the attraction between parallel strings ends.

**Reading (plausible, not proven).** The same scalar-mediated attraction lets an unhiggsed orientation region grow, both in a string core and in a free lump. So whenever a string can hold charge, the charge can also bind without the string. Both bound objects have the same partly unhiggsed interior.

**Limits.** The λ grid has a spacing of 0.1. The charge grid goes up to Q = 2710.9. Each lump was started from one orientation.

Sources: `REPORT_verify.md` (V3), `REPORT_QB.md`.

## 4. What was not tested

- **A four-derivative (Skyrme/Faddeev-type) stiffness.** It was excluded by the step-3 assumption A2. The version supplied by the gauge field comes paired with a supercurrent that screens it.
- **The chiral helical regime**, where the vacuum itself is twisted (\|γ\| > 0.3535), and closures as defects in it.
- **Route A with an SU(3)-invariant potential** (the semilocal model). There twisted current-carrying strings exist without an added field (Forgács, Reuillon and Volkov 2006).
- **Braided or linked elementary strings in Route B.** These are unprotected: non-abelian strings reconnect at BPS (Eto et al., PRL 98, 091602, 2007).
- **Non-axisymmetric stability (3D) of the Route B ring.** It is not triggered by the "string not required" verdict.
- **Quantum effects.** All results are classical. The CP² moduli acquire a quantum gap.

## 5. Forecasts against outcomes

| Test | Forecast (prior) | Outcome |
|---|---|---|
| Route A twisted ring | COLLAPSE (about 60 %) | COLLAPSE, all cells |
| Vorton straight-string window, from a frozen-profile estimate | none expected | 6 of 12 points had windows. The profile fattened by 10–100 ×. |
| Chiral term: soft mode and screening | director soft; screening possible | relative phases soft; the gauge field enhances the effect |
| Chiral ring | CHIRAL-STABLE about 10 % | COLLAPSE |
| Route B straight-string window | about 10 % | WINDOW, confirmed |
| Route B ring | METASTABLE about 35 % (n = 5) | METASTABLE |
| Route B vortex-free lump | disperses (75 %) | binds |
| Lumps vs window | BROADER 55 % (thin-wall estimate) | TRACKS |

**The recurring lesson.** Estimates that freeze the string's cross-section, or treat a lump as thin-walled, were wrong in sign or direction four times. The core deforms strongly under charge and twist, and in both models that deformation decided the outcome. Straight-string calculations that let the profile relax were the reliable guide: B4's ring stopped within 2 % of their prediction.

## 6. What this means for the closure question

- **Topology without stiffness does not hold a loop.** In Route A, a protected twist (Hopf charge) collapsed in every cell. Neither the gauge field, nor a chiral term in its stable-vacuum regime, supplied a stiffness that stops shrinkage.
- **Charge can hold a loop, but in both models the charge prefers to bind without the loop.** The string ends up a passenger. In Route B the two abilities appear to share a cause. A charge-supported closure would need a model where charge can bind to a string but not to itself, with T/I < m² on the string.
- **Open directions that remain consistent with these results:**
  - a stiffness that the gauge field cannot screen, derived from a model of the medium rather than added by hand (`E9_three_strand_closure/NOTE_chiral_term.md` §6);
  - protected closures (braids or links) in a setting where strings cannot pass through each other.

No particle identification is made or implied anywhere in E9 or E10.

## 7. Sources (all in `seed/experiments/`)

- **Route A:** `E9_three_strand_closure/`
  - `STATUS_step3.md`, `PREREG.md`
  - `REPORT_control.md`, `REPORT_N1.md`, `REPORT_N1_rerun.md`, `REPORT_N1_cells.md`
  - `PREREG_option4.md`, `REPORT_phase0.md`, `REPORT_phase1.md`
  - `NOTE_chiral_term.md`, `PREREG_chiral1d.md`, `REPORT_chiral1d.md`, `PREREG_chiral_loop.md`, `REPORT_chiral_loop.md`
- **Route B:** `E10_u3_vortices/`
  - `STATUS_routeB.md`, `NOTE_route_B.md`, `prior_address_routeB.md`
  - `PREREG_B2B3.md` (with Amendment A), `REPORT_B2B3.md`, `REPORT_verify.md`
  - `PREREG_B4.md`, `REPORT_B4.md`
  - `PREREG_QB.md`, `REPORT_QB.md`
- **Steps 1–2:** `E9_three_strand_closure/prior/`

## Addendum (November 4, 2026): E11 and closure

The first open direction of §6, a stiffness derived from a model of the medium, was tried once as `E11_medium_stiffness/` under a fixed stopping rule. It failed criterion D2 as pre-registered. The derived stiffness is a Faddeev term (the Seed's Model C, `E8_hopfions`) and does not see the thirds. **The step-3 closure line has ended:** see `CLOSURE_step3.md`. The second direction of §6 (protected braids or links) and the items of §4 remain untested and would be new programmes.
