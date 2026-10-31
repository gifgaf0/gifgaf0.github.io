# Step 3 status: the first stable closure (E9), October 31, 2026

Label: Exploration. This note summarizes the E9 reports and adds nothing to them. Where it and a report differ, the report governs. Branch `claude/seed-step3-first-closure`.

## The question

Can a closed loop of the three-strand composite vortex (three U(1) phases, one gauge field, Route A of step 1) settle at a finite size instead of shrinking away? `PREREG.md` §0.

## What has been run

| Route | Configuration | Parameters | Result | Report |
|---|---|---|---|---|
| Control | Untwisted ring, N = 0 | κ = 2, η = 0.1 | Collapses, as required (P1 holds) | `REPORT_control.md` |
| Twist + gauge field (Hopfion) | N = 1, Hopf-linked start A and helix start B, 65³ | κ = 2, η = 0.1 | **COLLAPSE**, both starts. A unlinks by a point reconnection. B's strand 1 merges onto the core (the §10 mechanism). | `REPORT_N1.md`, `REPORT_N1_rerun.md` |
| Current + charge (vorton, option 4) | Straight-string feasibility scan, 12 σ-sector points | κ = 2, η = 0.1 + σ (A3) | Thin-ring equilibria at 6 of 12 points, all in the regime where the σ phase is metastable | `REPORT_phase0.md` |
| Current + charge (vorton, option 4) | Axisymmetric ring at b3_d1, n = 7 and n = 10 | as above | **STABLE (axisymmetric), string not required, metastable.** The same σ ring with no ψ vortex is cheaper by about 5 % (−298 at n = 7, −433 at n = 10). A charged σ lump of the same Q is cheaper still (by 1668 at n = 7). | `REPORT_phase1.md` |

## What this establishes

- **Twist route.** At κ = 2, η = 0.1 the twisted three-strand ring has no finite-size minimum. The twist has no protected place to live.
- **Vorton route.** The added core field σ can hold a ring open. The three-strand string contributes nothing to that and costs energy. So **option 4 is closed for the E9 string** (`PREREG_option4.md` §9.4). Any study of σ on its own is a different model and would need its own pre-registration.
- **The thirds played no stabilizing role in either route.** This is a negative result about Route A as a source of a stable closure, at the parameters tested.

## What is still open

- **The §6 trigger corner.** The static N = 1 runs at κ = 1 and at η = 0 (`PREREG.md` §6) have not been run. Until they are, the twist-route negative holds only at κ = 2, η = 0.1. Prompt issued October 31, 2026.
- **Limits of option 4 Phase 1.** One grid and one box, with no resolution check. The no-vortex control (C-d) was run from a single start. Pinching and phase slips (Phase 2) were not tested; they were not needed, since Phase 2 runs only on a "string-supported" result.
- **Untested alternatives.**
  - **Route B:** non-abelian U(3) vortices, where the thirds are exact by group structure. This was step 1's recommended target.
  - **A four-derivative stabilizer** (Skyrme/Faddeev type). This is excluded by A2 and would need a new pre-registration with an Eddington argument.

No particle identification is made or implied anywhere in E9.
