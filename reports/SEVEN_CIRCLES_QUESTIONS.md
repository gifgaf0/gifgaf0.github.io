# Seven Circles Probe — Blocker

**Date:** 2026-05-14
**Brief:** CLAUDE_CODE_BRIEF_07_SEVEN_CIRCLES.md
**Status:** Blocked at Step 0. No code written. No 27/40 reproduction attempted.

## What the brief requires

Step 0 of Brief 07 names four files that must be read **before any code is
written**, and explicitly forbids guessing the circle definition:

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

Searched the full tree of `/home/user/gifgaf0.github.io`:

| Required artefact | Found? |
|---|:---:|
| `scratch_seven_circles_experiment.md` | no |
| `seven_circles_tight.py` (source of `CURATED_CONSTANTS`) | no |
| `three_perspectives.py` (source of `chord_intersections`, `cr_from_center`) | no |
| `phi_trig_inventory.md` | no |
| Any definition of `CURATED_CONSTANTS` | no |
| Any other "seven circles" / cross-ratio / tube/spine module | no |

Tooling that does exist in `tools/`: `chain_enumerate`, `chain_zd_labelling`,
`clifford_check`, `dfr_scaling`, `gs_profile`, `lattice_estimate`,
`discrete_circle_audit.{md,json,_*.py}`. None of these define the
seven-circles construction, the 40 chord positions, or `CURATED_CONSTANTS`.
The `_discrete_circle.py` / `discrete_circle_audit.*` files are a separate
discrete-circle audit and do not match the brief's setup.

## Ambiguities that cannot be resolved without the source

1. **What are the 7 natural torus circles?** Brief 07 lists three competing
   readings (spine + 6 tube cross-sections at Z₇ angles; 7 tube
   cross-sections; the 7 circles from `seven_circles_tight.py`) and asks
   the agent to pick the one that matches the scratch file. Without the
   scratch file or `seven_circles_tight.py`, there is no principled choice.

2. **What are the 40 chord positions?** Three candidate readings noted in
   the brief (all C(7,2)=21 pairs × 2 intersections — which is 42, not 40;
   a specific grid; a filtered subset). 40 ≠ 21·2; some filtering is
   required and only the scratch file specifies it.

3. **Which centre defines CR_tube?** Brief 07 points at
   `cr_from_center(..., tube_centre)` from `three_perspectives.py`, but
   "tube_centre" depends on which circle is being treated as the tube
   under reading (1) above.

4. **What tolerance counts as a cos18° hit?** The default in the brief
   is `tol = 5e-4`, but the scratch file may have used a different
   value (e.g. an exact-match within float epsilon, or a wider window).
   The 27/40 figure is tolerance-sensitive; guessing changes the count.

5. **Definition of `CURATED_CONSTANTS`.** The framework constant table
   that determines what counts as a "match" lives in
   `seven_circles_tight.py`. The brief assumes its keys are known. They
   are not present in this repo.

Any of these choices would silently change the 27/40 count. The brief
states "the principle (cos18° is the dominant value) matters more than
the exact 27/40 fraction" but also requires `cos18_hits == 27` in the
Definition of Done. Both cannot be satisfied without the source.

## What this blocker does NOT affect

- Brief 08 (`rho_derivation.py`) is self-contained — all constants and
  formulas are stated inside the brief — and is being executed
  independently of this blocker.
- The void correction `ζ(1−cos18°)` in
  `borromean_circumscription_derivation.md §5` is identified from the
  "5 is always a void connection" principle and the numerical match to
  the muonic-H residual. It does not itself depend on the 27/40 result;
  the 27/40 result is the *prior geometric address* cited in §X.1 of
  the paper, not a step in the formula.

## To unblock

Either upload the four files named in Step 0 of Brief 07, or supply
the exact construction in-line (the 7 circles' centres & radii, the
40-position enumeration rule, the `CURATED_CONSTANTS` table, the
tolerance, and which centre defines CR_tube). With those in hand the
brief is straight enumeration — a few hours of work — and the
DoD-required `cos18_hits == 27` becomes a verifiable claim rather than
a guess.
