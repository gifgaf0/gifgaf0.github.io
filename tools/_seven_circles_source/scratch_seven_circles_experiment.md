# Scratch Note — Seven-Circles Cross-Ratio Experiment

**Date:** May 13, 2026
**Status:** SCRATCH NOTE / Register 2 structural observation
**NOT a ledger entry. NOT a closure of OP-CIRCLES.**
**Append-only discipline preserved. No prior ledger content modified.**

---

## Motivation

Session originated from the pulsation amplitude question (May 13,
84-gap decomposition entry). The chain:

1. Pulsation 0.0948 needs a scale-invariant address, not a numerical
   match to integer combinations like π/33 (Eddington-flagged).
2. Scalar-in-front-of-sine-wave framing: amplitude is a prefactor,
   not part of the sine itself; dimension changes the prefactor,
   not the function.
3. The May 12 OP-CIRCLES entry already named seven natural torus
   circles and conjectured a chord-through-three-circles construction
   giving projectively invariant trig content (CONJ-FANO-CIRCLES).
4. Rather than name three circles in advance and risk Eddington
   maneuver, **enumerate all cross-ratios from all chord-circle
   intersections and look at the full distribution**. Experimentation,
   not selection.

---

## Procedure (fixed before computation)

- Seven natural torus circles (canonical R=3, r=1; reparam tested
  at R/r = 1.5, 2, 2.5, 3, 3.5, 4, 5, 7, 10):
  ① outer equator (R+r), ② inner equator / hole (R−r),
  ③ spine (R), ④ tube cross-section (r),
  ⑤ geometric mean √(R²−r²), ⑥ heptagon inradius (R−r)cos(π/7),
  ⑦ wing-tip circle.

- A chord at perpendicular distance d from origin, angle θ.
  Compute all line-circle intersections (typically 12 points,
  two per circle when chord passes inside).

- Compute all 4-point cross-ratios CR(t₁,t₂;t₃,t₄) =
  (t₁−t₃)(t₂−t₄)/((t₁−t₄)(t₂−t₃)) using chord parameter t.

- Match each value (and its reciprocal) against a curated library
  of **23 framework-specific constants** (5-fold trig, 7-fold trig,
  packing constants, the 84-decomposition values). No generic
  rationals (no 1/2, π/3, √2, etc. — these match by accident
  at high N and dilute the signal).

- Tolerance: 0.05% relative error (10× stricter than v1 of this
  experiment).

- Run null model: same number of random log-uniform values in
  the same range, same tolerance, same library. Report enrichment.

- Sweep d from 0.1 to 3.8 (chord positions) and R/r from 1.5 to 10
  (torus shapes). Check stability of (a) match rate, (b) which
  constants appear, (c) which 4-circle quadruples produce them.

---

## Results

### R1 — Primary chord enrichment

Primary chord (d=1.5, R=3, r=1, 495 cross-ratios):
- 10 matches at 0.05% tolerance (2.02%)
- Null expectation: 1 match (0.20%)
- **Enrichment ~10×**

This is meaningful at the single-chord level. The earlier v1
experiment at 0.5% tolerance gave 2× enrichment, dominated by
generic rationals (π/3, 1/2, √2). Tightening the tolerance and
restricting the library to framework-specific values raised the
enrichment to 10×.

### R2 — Three constants account for 64% of all matches across sweep

Full chord sweep (40 chord positions at d ∈ [0.1, 3.8], R=3, r=1):

| Constant | Hits / 40 | Register | Status |
|---|---|---|---|
| **cos(18°) = √(2+φ)/2** | 27 | 5-fold | **previously UNMAPPED** |
| **cos(π/7)** | 26 | 7-fold | Klein triangle |
| **√5/2** | 26 | 5-fold | governs t parameter (mapped) |
| sin(36°) = √(3−φ)/2 | 7 | 5-fold | **previously UNMAPPED** |
| φ/2 | 7 | 5-fold | governs K(0) (mapped) |
| cos(2π/7) | 7 | 7-fold | — |
| void (0.71284) | 6 | framework | 84-decomp |
| arctan(1/√2) | 6 | Prop P.α | — |
| gap (0.28716) | 3 | framework | 84-decomp |
| pulsation (0.0948) | 2 | framework | open — borderline noise |
| φ⁻¹, ε₃/ε₂, 8/21, φ⁻² | 1–2 each | various | scattered |

Top three constants (cos(18°), cos(π/7), √5/2) account for
79 of 123 total matches (64%).

### R3 — Reparameterization shifts pairings but not registers

When R/r varies from 1.5 to 10, **zero specific quadruple-to-constant
correspondences persist** at 0.05% tolerance. The quadruples that
produce matches at R/r=3 do not produce matches at R/r=5.

However, the **register identity is stable**: 5-fold and 7-fold trig
values dominate the matches across all R/r values. The specific
combinatorial address shifts with metric reparameterization, but
the algebraic register of the matched values does not.

### R4 — Pulsation 0.0948 does NOT have a clean cross-ratio address

The pulsation matched only 2 cross-ratios out of 19,800 computed
across the sweep. Compare to cos(18°) at 27 matches, void at 6.
At 0.05% tolerance, this is at or below the noise floor.

**The seven-circle structure does not give the pulsation amplitude
a clean geometric address.** The gap (0.28716) and void (0.71284) —
the φ-related components of the 84-decomposition — match more
strongly than the pulsation residual.

This is consistent with the structural reading from session
discussion: the pulsation is determined by subtraction
(void − φ⁻¹), not as a primary geometric object.

### R5 — Fano-line filter is not selective

80% of all 4-subsets of {1..7} contain a Fano line by chance.
Matches in Fano-line-containing quadruples: 62/123 = 50.4%.
**Below the null expectation.** The Fano incidence structure
does not select for framework-constant cross-ratios at this
level of analysis.

---

## What this DOES say

1. **Seven-circle torus structure is loaded with 5-fold and 7-fold
   trig content.** Three constants in particular (cos(18°), cos(π/7),
   √5/2) appear as cross-ratios with high frequency across all
   chord positions and torus shapes.

2. **The two previously unmapped 5-fold values (cos(18°), sin(36°))
   now have candidate geometric addresses.** From `phi_trig_inventory.md`:
   > "Unmapped values that could carry physical content:
   >  √(2+φ)/2 (≈ 0.951) — cos(18°)... appears nowhere explicit
   >  in current locked parameters. √(3−φ)/2 (≈ 0.588) — sin(36°)...
   >  also unmapped."

   Both appeared, cos(18°) very frequently. This is a partial
   confirmation of option (a) of the 5-Fold Completeness Conjecture:
   *unmapped values correspond to physical parameters not yet
   derived in the framework*.

3. **The gap/void components of the 84-decomposition appear in the
   torus circle geometry.** This supports the structural reading
   that the φ-tower scale gap (which sets void) lives in the
   geometric relationships between torus circles, while the
   pulsation residual does not.

4. **Convergence with §2.45 and §2.46.** Three independent results
   point to the 5-fold register as the framework's primary
   geometric carrier:
   - §2.45: pentagon seam transfer (5 as crystallographic forbidden
     direction in p6m)
   - §2.46: 5 as the only subtractor in the four-prime ladder
   - This experiment: 5-fold trig dominates the cross-ratio matches
   None of these is a derivation. The convergence is suggestive,
   not conclusive.

---

## What this does NOT say

1. **OP-CIRCLES is not closed.** No combinatorial-to-metric
   correspondence has been established. The seven circles do
   not have unique Fano-line assignments. The specific quadruple
   that produces cos(18°) at R/r=3 produces a different value
   at R/r=5.

2. **The 5-fold dominance may be partially an artifact** of the
   constant library containing 5 explicit 5-fold values versus 3
   explicit 7-fold values. Per-constant hit rate is what matters,
   and cos(π/7) (one of three 7-fold values) hits at the same rate
   as cos(18°) and √5/2 (two of five 5-fold values). The dominance
   is concentrated in **three specific values** of mixed register,
   not in a register broadly.

3. **The pulsation amplitude is not derived.** Open 3 of the
   May 13 84-gap entry remains open. The torus geometry encodes
   the gap/void but not the pulsation residual cleanly.

4. **The cross-ratio addresses are not unique.** Multiple quadruples
   produce the same constant; the same quadruple produces different
   constants at different R/r. This is the metric-vs-combinatorial
   problem from the May 12 entry, restated quantitatively rather
   than resolved.

---

## What this could become

If pushed further with discipline, candidate next steps:

1. **Vary chord angle θ, not just distance d.** Current experiment
   uses only horizontal chords. The 5-fold dominance might shift
   to 7-fold at specific angles, suggesting an angular signature
   of which register the geometry exposes.

2. **Restrict to chords passing through the heptagon inradius
   (circle ⑥) tangentially.** This selects a chord with 7-fold
   relationship to the configuration; check if the match
   distribution shifts to 7-fold.

3. **Cross-check against the Császár 3D embedding directly.**
   The 2D silhouette is one specific projection of the 4D Császár
   structure. Multiple silhouettes (top-down, side, oblique) might
   produce different match distributions. The "perspective"
   distinction from §2.34 (L/O/E observers) maps directly onto
   this.

4. **Sweep the constant library systematically.** Add and remove
   constants one at a time, measure how the enrichment changes.
   The library's effect on the result must be quantified before
   any claim of structural significance.

---

## Falsification

This is a scratch note, not a conjecture. Nothing is being claimed
strongly enough to require falsification. But for future reference:

If a tighter version of the experiment (0.01% tolerance, library
reduced to 10 framework-specific values, chord angle swept) gives
match rate at or below null expectation, the appearance of cos(18°),
cos(π/7), and √5/2 was noise inflated by library size, and the
seven-circle structure has no scale-invariant framework content.

---

## Audit Status

- All numerical results computed from explicit formulas; code at
  `/home/claude/circles_experiment/seven_circles_tight.py`.
- No fitted parameters. R=3, r=1 chosen as canonical; varied
  systematically over 8 R/r values for reparameterization check.
- Null model uses log-uniform random sampling over [0.01, 100],
  same library, same tolerance.
- Register-tagged throughout: Register 1 (computed numerical
  facts), Register 2 (structural observations from those facts),
  Register 3 (suggested interpretations, explicitly labeled).

---

*Filed May 13, 2026 as scratch note. To be reconsidered if
the angular sweep or perspective variation produces sharper
results, OR if the §3.4 Bjerknes Lagrangian derivation
independently identifies any of the same cross-ratios.*

*This note does not modify any prior ledger content.*
*OP-CIRCLES remains open. The pulsation amplitude question
remains open. The 5-Fold Completeness Conjecture remains at
Tier 4 (unaudited).*
