# Step 3 status: the first stable closure (E9), October 31, 2026

Label: Exploration. This note summarizes the E9 reports and adds nothing to them. Where it and a report differ, the report governs. Branch `claude/seed-step3-first-closure`.

## The question

Can a closed loop of the three-strand composite vortex (three U(1) phases, one gauge field, Route A of step 1) settle at a finite size instead of shrinking away? `PREREG.md` §0.

## What has been run

| Route | Configuration | Parameters | Result | Report |
|---|---|---|---|---|
| Control | Untwisted ring, N = 0 | κ = 2, η = 0.1 | Collapses, as required (P1 holds) | `REPORT_control.md` |
| Twist + gauge field (Hopfion) | N = 1, Hopf-linked start A and helix start B, 65³ | κ = 2, η = 0.1 | **COLLAPSE**, both starts. A unlinks by a point reconnection. B's strand 1 merges onto the core (the §10 mechanism). | `REPORT_N1.md`, `REPORT_N1_rerun.md` |
| Twist + gauge field, §6 corner cells | N = 1, starts A and B, 65³ | κ = 1, η = 0.1; κ = 2, η = 0; κ = 1, η = 0 | **COLLAPSE** in all six runs; N = 0 controls collapse (P1 holds in each cell). Mechanisms: B merges onto the core in every cell, even at η = 0. A merges at κ = 1, η = 0.1. At η = 0, A undergoes a point reconnection and the two loops then separate. | `REPORT_N1_cells.md` |
| Current + charge (vorton, option 4) | Straight-string feasibility scan, 12 σ-sector points | κ = 2, η = 0.1 + σ (A3) | Thin-ring equilibria at 6 of 12 points, all in the regime where the σ phase is metastable | `REPORT_phase0.md` |
| Current + charge (vorton, option 4) | Axisymmetric ring at b3_d1, n = 7 and n = 10 | as above | **STABLE (axisymmetric), string not required, metastable.** The same σ ring with no ψ vortex is cheaper by about 5 % (−298 at n = 7, −433 at n = 10). A charged σ lump of the same Q is cheaper still (by 1668 at n = 7). | `REPORT_phase1.md` |
| Chiral stiffness term (option 2, medium-stiffness version) | Derivation note; 1D vacuum and texture calculations | locked model (A5, A6), κ = 2, η ∈ {0, 0.1}, three directions | Term γψ*·(D×ψ) requires strands locked to space; locked symmetry D₃ × U(1); thirds survive. Uniform vacuum stable for |γ| < 0.3535 at η = 0.1 (A free); unstable for any γ ≠ 0 at η = 0. Soft mode is the relative phases (120° offset + current), not the director; no screening. | `NOTE_chiral_term.md` (+ Addendum A), `REPORT_chiral1d.md` |
| Chiral stiffness term, loop | N = 1, starts A and B, 65³, γ ∈ {±0.1, ±0.2, ±0.3} | locked model, κ = 2, η = 0.1 | **COLLAPSE** in all 12 runs; every (start, \|γ\|) cell COLLAPSE. ±γ lose strand 1 at the same iteration; the texture takes whichever handedness γ favours, so the chiral gain is not tied to the sign of N. Delay vs γ = 0: at most 6 iterations. Open boundaries create a surface twist (≈ 1570γ² below the plain vacuum) that invalidates the virial residual; it does not affect the verdicts. | `PREREG_chiral_loop.md`, `REPORT_chiral_loop.md` |

## What this establishes

- **Twist route.** In all four (κ, η) cells of `PREREG.md` (κ ∈ {1, 2}, η ∈ {0, 0.1}), and from both starts, the twisted three-strand ring has no finite-size minimum. No run pauses at any radius while linked. **The §6 condition is met.** Option 4 was opened early; this makes its opening valid after the fact.
- **Vorton route.** The added core field σ can hold a ring open. The three-strand string contributes nothing to that and costs energy. So **option 4 is closed for the E9 string** (`PREREG_option4.md` §9.4). Any study of σ on its own is a different model and would need its own pre-registration.
- **Chiral route.** Below the vacuum threshold (|γ| ≤ 0.3 < 0.3535) the chiral term does not hold the twisted ring open, and does not distinguish the twist's handedness. The trend (delays of 0, 2, 6 iterations) suggests, without proving, that a chirality strong enough to matter would twist the uniform vacuum first.
- **The thirds played no stabilizing role in any route.** Three stabilizer families (twist + gauge field, vorton, chiral term) are negative for the Route A string at the parameters tested.

## What is still open

- **η = 0 relaxation tail.** Once the lines vanish, the η = 0 runs take 220–300 extra iterations to reach the vacuum (about 80 at η = 0.1). This is undiagnosed. It is consistent with the relative phases being a massless, flat direction at η = 0, which L-BFGS relaxes slowly. It does not affect any verdict.
- **Limits of option 4 Phase 1.** One grid and one box, with no resolution check. The no-vortex control (C-d) was run from a single start. Pinching and phase slips (Phase 2) were not tested; they were not needed, since Phase 2 runs only on a "string-supported" result.
- **Untested alternatives.**
  - **Route B:** non-abelian U(3) vortices, where the thirds are exact by group structure. This was step 1's recommended target.
  - **A four-derivative stabilizer** (Skyrme/Faddeev type). This is excluded by A2 and would need a new pre-registration with an Eddington argument.
- **Chiral route, not tested.** The helical regime (|γ| > 0.3535, where the vacuum itself is twisted) and closures as defects in it. Any future chiral run needs periodic boundaries, or a subtracted surface layer, because of the open-boundary surface twist. A unit model that would fix γ does not exist.
- **Next: Route B** (non-abelian U(3) vortices), opened November 1, 2026, as `E10_u3_vortices` (`NOTE_route_B.md`). Also recorded there: Route A with an SU(3)-invariant potential (the semilocal model) has twisted current-carrying strings without an added field (Forgács, Reuillon and Volkov 2006). E9 never tested that, because its per-component potential breaks SU(3).

No particle identification is made or implied anywhere in E9.
