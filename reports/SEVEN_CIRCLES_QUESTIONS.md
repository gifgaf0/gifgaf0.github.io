# Seven Circles Probe — Blocker (v2, with v5 spec-level information)

**Date:** 2026-05-14 (v2)
**Brief:** CLAUDE_CODE_BRIEF_07_SEVEN_CIRCLES.md
**Status:** Still blocked. v5 of `borromean_circumscription_derivation.md`
            supplies useful spec-level information that was previously
            only in the missing scratch file, but does not close the
            implementation gap. No code written. No probe attempted.

## What the brief requires

Step 0 of Brief 07 names four files that must be read **before any code
is written**, and explicitly forbids guessing the circle definition:

> ```
> read scratch_seven_circles_experiment.md
> read seven_circles_tight.py            # contains CURATED_CONSTANTS
> read three_perspectives.py             # contains chord_intersections, cr_from_center
> ```
> Document your answers before proceeding. … If you hit a blocker (scratch
> file missing, ambiguous circle definition, CURATED_CONSTANTS undefined),
> write the blocker in `reports/SEVEN_CIRCLES_QUESTIONS.md` and stop. Do
> not guess the circle definition.

## What is in this repository

Re-searched the full tree of `/home/user/gifgaf0.github.io`:

| Required artefact | Found? |
|---|:---:|
| `scratch_seven_circles_experiment.md` | no |
| `seven_circles_tight.py` (source of `CURATED_CONSTANTS`) | no |
| `three_perspectives.py` (source of `chord_intersections`, `cr_from_center`) | no |
| `phi_trig_inventory.md` | no |
| Any definition of `CURATED_CONSTANTS` | no |
| Any other "seven circles" / cross-ratio / tube/spine module | no |

The only candidate in `tools/` is `_discrete_circle.py` /
`discrete_circle_audit.{md,json}`, which is a separate discrete-circle
audit and does not match the brief's setup.

## What v5 of `borromean_circumscription_derivation.md` adds

§5.2 and §6.4 of the v5 spec supply specification that was previously
only in the missing scratch file. The following are now known:

- **The seven natural torus circles at R=3, r=1, by label:**
  1. outer equator
  2. hole equator
  3. spine
  4. tube cross-section
  5. geometric mean
  6. heptagon inradius
  7. wing-tip
- **Chord-position count:** 40 horizontal chord positions.
- **Match tolerance:** 0.05%.
- **Library size:** 23 framework constants (the `CURATED_CONSTANTS` table).
- **Expected primary result:** cos 18° = √(2 + φ)/2 at **14/40** chord
  positions (35%), joint-highest frequency, ~10× null expectation.
  (The earlier 27/40 figure was the unaudited v1 scratch result and is
  **not** the citable count — see paper §X.1 footnote.)
- **Dominant circle combinations:** (1, 2, 5, 7), (1, 3, 5, 6),
  (2, 3, 5, 6) — exclusively the hole-boundary geometry
  (circles 2, 5, 6: hole equator, geometric mean, heptagon inradius).
  cos 18° concentrates at the void/hole boundary, **not** the tube.
- **Gate non-identity (verified numerically here, ascending order
  d, a, c, b):** cross-ratio of the pure radii
  `{R−r, R, √(R²−r²), (R−r)·cos(π/7)}` evaluates to **1.034239**,
  not cos 18° = 0.951057. The near-cos18° signal must therefore come
  from chord-height + 4-point selection geometry within the full
  sweep — it is **not** a four-radii projective identity. (v5 §6.4
  explicitly states this and §7 records it as the open gate.)

## What is still missing

Even with the above, five items remain ambiguous and cannot be
resolved without the source code or an explicit construction:

1. **Definition of "wing-tip".** Six of the seven labels parse
   algebraically without ambiguity (R+r=4, R−r=2, R=3, r=1,
   √(R²−r²)=√8≈2.828, (R−r)·cos(π/7)≈1.802). "wing-tip" is not a
   standard term in this context. Candidates include (a) R+r·cos(π/7),
   (b) R·cos(π/7), (c) (R+r)·cos(π/7), among others. The dominant
   4-tuple (1, 2, 5, 7) names circle 7 explicitly, so the choice
   propagates into the headline result.

2. **The 23 `CURATED_CONSTANTS`.** The framework-constant library that
   determines what counts as a "match" at 0.05% tolerance lives in
   `seven_circles_tight.py`. Without the list, "joint-highest frequency"
   cannot be tested — different libraries give different rankings.

3. **40-chord enumeration rule.** Brief 07 says "40 chord positions"
   but does not state the rule. Candidates: uniform y grid between
   y_min and y_max of the union, adaptive spacing per circle,
   a specific filter that lands at exactly 40, only chords where all
   seven circles are cut. The exact rule changes which configurations
   are in scope.

4. **4-from-7 selection rule and side choice.** Cross-ratio is a
   function of four points. Each chord meets each of the seven circles
   in at most two points → up to 14 points per chord. The probe must
   pick four of them. The dominant-tuples list (1, 2, 5, 7),
   (1, 3, 5, 6), (2, 3, 5, 6) suggests every 4-subset of circles is
   enumerated; the side choice (left only / right only / a specific
   pairing) is unstated.

5. **Cross-ratio formula.** Brief 07 mentions `cr_from_center` from
   `three_perspectives.py`. Angular (from a designated centre),
   Euclidean (signed projective on the line), or unsigned modulus —
   each gives a different value for the same four points. The brief
   names CR_tube and CR_line, implying at least two different
   formulations relative to two different centres.

Any of these choices silently changes the 14/40 count. The brief
explicitly forbids guessing the circle definition; the same principle
applies to the selection and CR-formula choices.

## Editorial guidance for the eventual report (from v5 instructions)

When the source materials arrive and the probe is run, the report
must follow the editorial discipline applied in `paper/X1_cos18_address.md`:

- Structure: geometric fact → computation → result.
- Single citation footnote at the first cos 18° appearance.
- No rung structure, face inheritance, H²→ℝ³ discussion, Clifford
  tower context, or PSL(2,5)/PSL(2,7) interface.
- Any unexpected residual flagged at full numerical precision and
  labelled "residual consistent with deeper geometric structure; see
  companion framework documentation". No naming of the broader
  framework.
- Bilateral symmetry of the 36° → 18°/side fold is stated as
  geometric fact; its derivation from the substrate action is the
  open gate and the prior address is Register 2 until that closes.
- **Target count is 14/40 (tight, 0.05% tolerance).** If the probe
  returns 14/40, the brief's DoD is met. If it does not, document
  the discrepancy at full precision per the brief's epistemic
  discipline section — do not adjust tolerance to force agreement.

## What this blocker does NOT affect

- Brief 08 (`tools/rho_derivation.py`, commit `4d6b612`) is complete
  and follows the v5 framing: it computes the void correction
  ζ·(1 − cos 18°), reports the post-correction residual at full
  precision (−0.0019% in ρ; −0.000076 absolute), and matches the
  identity cos(π/10) = √(2+φ)/2 to 1e-12. 13/13 tests passing.
- Paper section §X.1 (`paper/X1_cos18_address.md`) is drafted to the
  v5 editorial constraints and pointers at the probe report; it does
  not depend on the probe being unblocked. When the probe lands and
  the citable count is confirmed, only the footnote pointer needs
  updating.

## To unblock

Either upload the four files named in Step 0 of Brief 07, or supply
the exact construction in-line:

- the wing-tip circle definition (closed-form expression for its
  radius)
- the 23-entry `CURATED_CONSTANTS` table
- the 40-chord enumeration rule (concrete and reproducible)
- the 4-from-7 selection rule and side choice for points on each
  chord
- the cross-ratio formula (including which centre defines `CR_tube`
  and which defines `CR_line`)

With those, the brief reduces to straight enumeration over a known
configuration space and the target 14/40 becomes a verifiable claim
rather than an unconstrained probe.
