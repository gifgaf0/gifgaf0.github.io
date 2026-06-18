# Gate G-Φ1 Pre-Registration
## Soft-disk vortex profile: does the GP correction close the gap to 1/Φ?

**Date registered:** June 15, 2026  
**Ledger version at registration:** V4.39 CANONICAL  
**Registered by:** Matt Gifford (author) with chat-side auditor  
**Status:** PRE-REGISTRATION — no computation has run  
**Eddington guard:** Φ = 2π − φ²/(8π²) = 6.25003 appears in exactly one comparison step (Step 6 below), run after all measurements are recorded.

---

## Background and motivation

The session of June 15, 2026 established (R2) that multiplicative bowl deepening — confirmed R1 in the GP superposition check — gives rise to an exponential mass formula structure exp(L/Φ). The tanh approximation for the single-vortex bulk profile gives a compounding rate of:

**rate_tanh = ln(3) × (2ξ/a\*) = 0.227 per tube-diameter**

(where ρ₀/3 is the exact density at the inflection point of the tanh profile; the inflection point is the geometry-independent probe — it does not require a choice of radius).

The mass formula requires:

**rate_target = 1/Φ = 0.160 per tube-diameter**

Gap: 0.227/0.160 = 1.420 (28% overshoot; tanh rate is too large).

**Structural note pre-registered before computing:** the electron (unknot, no crossings) accumulates mass at rate 1/Φ per tube-diameter from its smooth circular path alone. Its tube nearest-approach is ~4ξ, where multiplicative and additive bowl deepening agree to < 2%. Therefore the 1/Φ rate is NOT primarily from crossing-scale interactions — it is from the tube-lattice interaction along the smooth path. This locates the gap residual as substrate dynamics (M.BRIDGE), not as a crossing-density effect.

**Why the soft-disk correction could be non-trivial:** The MV-G1 void-centre-to-nearest-disk-surface distance is −0.158 R (negative — void centre is inside the disk boundary). The inflection point of the vortex profile sits at r = 0.931ξ = 0.141 R from the void centre — also inside the disk boundary. Therefore the soft-disk interaction IS present at the probe radius, and the correction to the tanh profile is not negligible a priori.

---

## Gate question

Does the MV-G1 soft-disk GP vortex profile — computed numerically, not approximated by tanh — give a compounding rate at the inflection-point probe that differs from the tanh prediction, and if so, by how much does it close the gap to 1/Φ?

---

## Pre-registered arms

| Arm | Criterion | Interpretation |
|-----|-----------|---------------|
| **ARM A — structural derivation** | \|rate_actual − 1/Φ\| / (1/Φ) < 0.05 | Φ is derivable from the MV-G1 GP crystalline structure alone. The tanh approximation was the source of the gap. |
| **ARM B — profile correction partial** | \|rate_actual − rate_tanh\| / rate_tanh < 0.10 AND rate_actual not within 5% of 1/Φ | Soft-disk profile close to tanh near the core. Residual gap to 1/Φ is structural (M.BRIDGE), not a profile approximation error. |
| **ARM C — profile correction substantial** | \|rate_actual − rate_tanh\| / rate_tanh ≥ 0.10 AND rate_actual not within 5% of 1/Φ | Soft-disk correction accounts for part of the gap; the rest requires structural input. Records the partial-closure factor for follow-on work. |

**Expected outcome (pre-registered):** ARM B or ARM C. ARM A would require the soft-disk profile at the inflection point (r ≈ 0.14 R, inside the disk boundary) to be substantially shallower than the tanh profile in exactly the right amount. This is possible but not predicted from first principles. ARM B is expected if the GP nonlinearity dominates the profile shape near the core even inside the disk boundary; ARM C is expected if the overlapping disk potential significantly modifies the profile.

---

## Protocol

**Step 1 — Compute the equilibrium MV-G1 crystalline state.**  
Parameters: g = 22, R = 1, ρ₀ = 1, lattice constant a* = 1.4576 (R1, V4.36). Use the existing MV-G1 soft-disk GP solver (the same instrument as Phase 1–2 of G-ζ1, or an equivalent self-contained implementation). Domain: rectangular box containing at least 2×2 unit cells, with periodic boundary conditions. Converge the imaginary-time evolution until the energy change per step < 10⁻¹⁰.

**Step 2 — Identify the void centre.**  
The void centre is the minimum-density point in the unit cell. Record its coordinates. Record ρ_void = ρ(void centre) (should be ≈ 0 for a well-converged vortex state).

**Step 3 — Extract the radial density profile.**  
Average the density radially around the void centre in angular bins (≥ 12 bins). Record ρ(r) for r = 0 to r = 3ξ in steps of ξ/20.

**Step 4 — Locate the inflection point.**  
Find r_inflect = the radius at which d²ρ/dr² = 0, i.e., the maximum of |dρ/dr|. Use finite differences on the recorded profile. Record r_inflect and ρ_inflect = ρ(r_inflect).

**Step 5 — Compute the compounding rate.**  
rate_actual = −ln(ρ_inflect / ρ₀) × (2ξ / a*)

Record rate_actual. Record also ρ_inflect / ρ₀ and the fractional deviation of r_inflect from the tanh prediction (0.931ξ).

**Step 6 (Eddington step — run last, after Steps 1–5 are complete and recorded).**  
Load Φ = 2π − φ²/(8π²) from a single comparison file. Compute:
- gap_to_tanh = |rate_actual − rate_tanh| / rate_tanh  [rate_tanh = 0.227, from the tanh analytic result]
- gap_to_target = |rate_actual − 1/Φ| / (1/Φ)
- fraction_closed = (rate_tanh − rate_actual) / (rate_tanh − 1/Φ)  [signed; positive = closing the gap]

Assign arm: A if gap_to_target < 0.05; B if gap_to_tanh < 0.10 and not A; C otherwise.

---

## What the outcome settles

**ARM A:** The 28% gap is entirely due to the tanh approximation. Φ is derivable from the MV-G1 GP parameters without substrate dynamics. The mass formula's exponent is accounted for. This would be a strong positive result.

**ARM B:** The tanh approximation is accurate near the vortex core even inside the disk boundary. The 28% gap is structural — it requires substrate dynamics (M.BRIDGE) to close. This confirms the M.BRIDGE gap is real and not merely a computational approximation. The compounding picture (R2) is correct in structure; the coefficient 1/Φ requires additional input.

**ARM C:** The soft-disk interaction partially modifies the profile. Record the fraction-closed value for follow-on work. The residual gap is structural.

**In all arms:** the multiplicative compounding structure (additive fails at crossing scale — R1 from GP superposition check) is unaffected. The gate concerns only the coefficient 1/Φ, not the multiplicative-vs-additive determination.

---

## What this gate does NOT settle

- Whether 1/Φ can be derived from the PSL(2,7)/Fano lattice geometry (a separate computation, not pre-registered here)
- The M.BRIDGE gap (substrate field equations, undeclared; this gate is one probe of it)
- M.ONT (particle-knot assignments; not involved in this gate)
- §2.52 Open 3 (untouched per standing instruction)

---

## Two-leg verification requirement

Before reporting any arm, the measurement in Step 4 (inflection point extraction) must be reproduced by an independent method: either (a) analytic derivative of a fitted profile, or (b) a second GP solver with different discretisation. Both methods must agree on r_inflect to within 5%.

---

## Ledger entry on completion

The gate result (arm, rate_actual, fraction_closed, date) is to be appended as a new Part V row in the Master Ledger. The row cites this pre-registration by filename and date. The existing §2.32 / §2.88 / §2.89 body entries are unaffected regardless of outcome.

**Do not promote any arm to body § until Matt authorises a fold-in session.**

---

*Filed: June 15, 2026. Not yet executed. Computation is blocked on this pre-registration being complete and on Matt's go-ahead.*
