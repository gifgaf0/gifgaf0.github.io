# G-TSH4 — TWO-LEG STATUS MEMO (after the exposed leg's self-halt)
**Filed:** July 28, 2026, chat leg. Base canonical V4.71 `9517f4fb7aa2de65b0b4a69985962d8f`.

## Roles as they now stand
| role | instance | status |
|---|---|---|
| Executor 1 | chat leg | complete; everything single-leg provisional (reports `615702e3` Phase 0, `3491541b` Phase 1–2; verdict `c72b6724`) |
| **Auditor (exposed-side record)** | current CC instance | **self-halted from the blind leg by correctly invoking the dispatch's quarantine rule** — the protocol operating as designed, credited |
| Executor 2 (blind) | fresh CC instance | pending dispatch |

## Exposed-side deliveries entering the comparison record as audit annexes (not the blind leg)
1. Phase-0 independent recompute on the locked model (retroactively confirmed: §B functional, Λ=2Λ_c, both analytic kernels, all five cells) — Q-A ordering confirmed; F-3 found independently, matching the authorized A-1.1 re-carve.
2. Phase-1/2 internal-consistency audit: 21/21.
3. Ledger chain verification (V4.71 authentic; size audit that produced the chars-vs-bytes erratum `a5d88fd7`).
4. In-band dispatch verification: prereg block `e66b964d` ✓, Part A `2c676701` ✓, byte-exact.
5. Offer on the table: convention-robust FCC Zener corroboration, labelled non-leg (author election D-3, pending).

## Contamination hazard — flagged before it bites
The exposed-side record (including chat-leg numbers) is **committed to the repo** (fe5f4c3..74fb9d1). A fresh instance launched inside that checkout can self-contaminate by listing or reading files. **Launch the blind instance in a clean working directory containing exactly one file: `G_TSH4_CC_DISPATCH_INBAND.md` (`96eb8e8fe3f0311b62f82075e2fa2a82`).** The dispatch's HALT-on-exposure rule remains the backstop, not the plan.

## Dispatch message template (paste as the fresh instance's first message)
> You are the blind second leg for gate G-TSH4. The only artifact you may use is the attached `G_TSH4_CC_DISPATCH_INBAND.md` (md5 `96eb8e8fe3f0311b62f82075e2fa2a82`). Run its verify-then-build step first; then execute the blind-leg scope exactly as written, with your own independent solver and your own quarantined θ mapper run last. Do not read, request, or search for any other SQT material for this task. If any chat-leg energies, constants, slopes, or verdicts appear in your context, HALT and report the exposure. Freeze your numbers when done and report them for C1–C6.
> **A-2 status: [ACTIVE / not active — author strikes one].**

## The one election still open — A-2 (residual validity gate ≤1e-6, both legs)
Chat-leg recommendation: **ACTIVE.** Rationale: the gate is generic instrument hygiene (a residual bound; no magnitudes, no directions leak). Without it, a split-step-class solver on the blind leg can pass its own convergence practice while sitting a few percent off the true GP minimum — precisely the artifact class the chat leg caught, and precisely the scale where θ₁ = 3% lives — burning the blind leg's budget on a foreseeable C1/C3 divergence and an S9 cycle. The independence-purist counterargument (let the blind leg discover the bias itself) is on record; the author's word decides.

## Then
Blind leg freezes → C1–C6 (verdict-level divergence → S9; gate fragility → S9-lite) → fold candidate **V4.72**. §2.87.J remains reserved; §2.52 Open 3 frozen; open queue otherwise unchanged (OP-2.58.2d BKZ, P-LEX-1 evaluation, G-2a-L1 comparison, Framework Index cosmetic sweep, E2 witness successor).
