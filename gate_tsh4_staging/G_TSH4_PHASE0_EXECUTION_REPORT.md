# G-TSH4 — PHASE 0 EXECUTION REPORT (chat leg)
**Gate:** G-TSH4, the 3D-stack shear gate. Registered address §2.91.I Q3 item (3) (§2.88.B caveat).
**Base canonical:** V4.71, md5 `9517f4fb7aa2de65b0b4a69985962d8f` (authorized this directive, P-a).
**Pre-registration:** `G_TSH4_EXECUTION_PREREGISTRATION.md`, md5 `e66b964d4467fcb9a5f328ef0db80a35`.
**Source memo:** `staging_memo_G_TSH4_3D_stack_gate.md`, LOCKED md5 `bfee456f0d936584401fcabd2b75dc13` (re-verified intact).
**Instrument:** `gtsh4_phase0_core.py` md5 `2ea84f6163cb8421fe78483fe8f0a6e0`; driver `gtsh4_phase0_run.py` md5 `82d34a744466456ec5ef5eaf2bda316d`; scheduler `gtsh4_phase0_resume.py` (scheduling only, physics-identical).
**STATUS: HALTED TO AUTHOR under election E5(b).**

---

## §0. State reconciliation (reported first, per H-protocol)

On resuming this directive the chat leg found **the pre-registration already minted and sealed** with exactly the elections given (P-a, step+gem8, S+D, {AA,AB,ABC,FCC,BCC}, high-symmetry sampling, halt-to-author, full-from-scratch, θ₁=3%/θ₂=10%/δ_E=1e-4), the Phase 0 instrument already built, and an execution log showing three step-kernel structures completed. A results JSON containing all ten items was subsequently found on disk.

**No second pre-registration was minted.** Re-minting would have created two competing sealed artifacts and broken the Eddington chain. The existing artifact was adopted as *the* pre-registration and the instrument was left byte-frozen.

**Provenance closed by independent recompute.** The two decisive step-kernel entries were recomputed from scratch with the frozen instrument: AB → 70.202166036 (stored 70.202166036, Δ = 0.000e+00) and FCC → 70.209965147 (stored 70.209965147, Δ = 0.000e+00); Λ_c re-derived to 21.713735 at k\* = 5.4486. The three values in the interrupted log also match the JSON exactly. The stored results are reproducible.

## §1. Coupling (pre-declared, kernel-adaptive)

Λ = 2.0 × Λ_c, Λ_c = min over k with Û̃(k) < 0 of [−k²/(4Û̃(k))] — the roton-instability threshold of the uniform state, so both kernels sit at the same relative distance above their own crystallization threshold.

| kernel | Λ_c | k\* | Λ = 2Λ_c |
|---|---|---|---|
| step | 21.713735 | 5.4486 | 43.427469 |
| gem8 | 33.783379 | 5.5655 | 67.566757 |

All ten relaxed states are strongly modulated droplet crystals (peak/void contrast 1.2×10⁴ – 8.5×10⁴), i.e. the same strongly-modulated regime as the 2D MV-G1 anchor, not a weak density wave.

## §2. Results — energy per particle at each structure's own optimum

**step kernel (Λ = 43.4275)**

| structure | e | rel. to min | geometry | c/a | peaks |
|---|---|---|---|---|---|
| **AB (hcp)** | **70.202166036** | 0 | a=1.40014, c=2.28435 | 1.63152 | 4/4 |
| FCC | 70.209965147 | 1.1110e-4 | L=1.97963 | — | 4/4 |
| ABC | 70.209965196 | 1.1110e-4 | a=1.39984, c=3.42881 | 2.44943 | 6/6 |
| BCC | 71.094373039 | 1.2709e-2 | L=1.57397 | — | 2/2 |
| AA | 71.601317575 | 1.9930e-2 | a=1.29532, c=1.36091 | 1.05064 | 2/2 |

**gem8 kernel (Λ = 67.5668)**

| structure | e | rel. to min | geometry | c/a | peaks |
|---|---|---|---|---|---|
| **AB (hcp)** | **102.489254245** | 0 | a=1.38974, c=2.26802 | 1.63197 | 4/4 |
| FCC | 102.498561765 | 9.0815e-5 | L=1.96503 | — | 4/4 |
| ABC | 102.498561853 | 9.0815e-5 | a=1.38947, c=3.40361 | 2.44957 | 6/6 |
| BCC | 103.371632925 | 8.6095e-3 | L=1.55704 | — | 2/2 |
| AA | 104.327213294 | 1.7933e-2 | a=1.28300, c=1.34293 | 1.04671 | 2/2 |

## §3. Q-A decision, applied exactly as locked

| kernel | argmin | (e₂−e₁)/|e₁| | δ_E | arm |
|---|---|---|---|---|
| step | AB | **1.1110e-4** | 1e-4 | STACK-SELECTED (margin +11.1% over δ_E) |
| gem8 | AB | **9.0815e-5** | 1e-4 | **DEGENERATE-STRUCTURE → halt (E5b)** |

**The two kernels straddle the pre-declared margin.** Per E5(b) the gate **halts to author**. Thresholds are T3-immutable and are not re-tuned; the straddle is reported as data.

## §4. Findings

**F-1 — The substrate selects a close-packed stack of triangular layers, in both kernels.** AB (hcp) and ABC/FCC lie within ~1e-4 of each other and 0.86–2.0% below both AA (simple hexagonal) and BCC. The registered question behind §2.88.B — *does the 2D p6m layer structure survive dimensional promotion?* — answers **yes** on the structural side: the 3D ground state is a stack of p6m layers in every case that survives. What is *not* resolved is the **stacking sequence**, hcp vs fcc, which is near-degenerate.

**F-2 — Instrument validation via the recorded containment.** ABC with free c/a relaxed to c/a = 2.449433 (step) and 2.449566 (gem8) against √6 = 2.449490 — i.e. onto the fcc geometry — and its energy agreed with the independently seeded cubic FCC run to **6.9e-10 and 8.6e-10 relative**. Two different cell geometries, two different grids, one energy. This is the strongest available check that the energy functional, cell construction and relaxation are correct.

**F-3 — ARM-LABEL DEFECT (verdict-assembly integrity; author decision required).** The locked decision rule maps argmin ∈ {AA, AB, ABC} → STACK-SELECTED and argmin ∈ {FCC, BCC} → NON-STACK-SELECTED. **FCC is itself an ABC stack of triangular layers** — F-2 demonstrates this numerically, not just in principle. The labels therefore do not carve the structure space: the same physical structure receives opposite labels depending on which seed reached it. The pre-registration anticipated the containment but declared the FCC run non-verdict-bearing, which does not repair the map. *The chat leg has not re-labelled anything.* The honest re-carving appears to be {AA, BCC} = non-close-packed vs {AB, ABC≡FCC} = close-packed p6m stacks, with stacking sequence as a sub-question — **but that is an author call, filed here at the catch, pre-verdict.**

**F-4 — Verdict fragility w.r.t. δ_E.** Both gaps sit within 11% of the margin (1.111e-4 and 9.08e-5). Any Q-A statement of the form "hcp beats fcc" is not robust. The defensible physical statement is: **hcp and fcc are near-degenerate at the 1e-4 level, hcp marginally lower in both kernels.**

**F-5 — Mild tension with the LSF anchor, reported not smoothed.** Ancilotto–Rossi–Toigo (PRA 88, 033618) report FCC for the 3D soft-core GP supersolid. Here fcc is second by ~1e-4 in both kernels, below the resolving power the pre-declared margin claims. This is consistent within the near-degeneracy and is **not** presented as a contradiction of the prior art; different kernel, different coupling convention, and a splitting at the 1e-4 level.

## §5. Falsifiers and audit

- **F-CONV: PASS, but non-discriminating.** All ten values lie between 0.00e+00 and 5.55e-16 — machine-epsilon (≈1 ulp), roughly ten orders below the 5e-6 gate. The spectral (plane-wave) discretization is converged to double precision by dx = 0.05, so the test cannot discriminate at this resolution. *Recorded as an instrument observation, not a falsifier firing.*
- **H-protocol note (self-caught, chat leg, on resume):** the driver's inline comment asserts that continuation-seeding across different grids "is not possible" and re-seeds the finer run instead. That assertion is **wrong** — spectral interpolation would carry the coarse solution onto the fine grid. Because F-CONV saturates at ulp level, the departure is immaterial to every number reported here. Logged rather than silently corrected; the instrument was **not** modified mid-execution, to preserve uniformity across structures.
- **Two prior self-caught bugs, already logged in-code by the executing leg and surfaced here:** (i) the T1 self-grep initially fired on its own forbidden-literal list, repaired by excising the delimited guard block — explicitly *not* by fragment assembly, which T1 forbids; (ii) the split-step applied the half-kinetic factor twice, doubling the effective kinetic operator (Λ_eff = Λ/2), which at Λ = 2Λ_c sits exactly at threshold and melted every seeded crystal — caught by the modulation-contrast sanity check.
- **Symmetry verification:** every relaxed state retained its seeded droplet count (2/2, 4/4, 6/6 as appropriate). No structure relaxed into a different one.
- **T1 self-grep:** PASS on all computation files, every invocation.
- **F9 / F-LIN / F-ISO / F-NEG:** Phase 1–2 falsifiers, not exercised in Phase 0. F-ISO remains re-scoped as locked.

## §6. What is not claimed

No shear speed, no ratio, no anisotropy statistic, no observable, no magnitude. Q-B, Q-C and Q-D are untouched. R_T's KNOB status is untouched. No comparison to any measured quantity was performed or licensed. The CC leg has not run; no two-leg comparison exists, so nothing here is fold-eligible.

## §7. Author decisions required to resume

1. **F-3, the arm-label defect.** Re-carve the Q-A arms (recommended: close-packed p6m stack {AB, ABC≡FCC} vs non-close-packed {AA, BCC}, stacking sequence demoted to a sub-question), or rule otherwise. Amendment class: filed at the catch, pre-verdict.
2. **The E5(b) halt.** Options: (a) accept the near-degeneracy as the finding and carry **both** hcp and fcc into Q-C — if the A_3D verdicts agree, the degeneracy is immaterial to the gate's actual stake, which is the §2.88.B isotropy question; (b) increase precision (finer optimizer tolerance / denser geometry search) to sharpen the 1e-4 splitting — legitimate, since it changes precision and not the T3-immutable δ_E; (c) add Λ values to test whether the ordering is coupling-dependent — an amendment, logged as post-hoc and non-substitutive for the pre-declared run.
   *Chat-leg recommendation: (a).* The gate's registered stake is isotropy, not stacking sequence, and hcp and fcc have different symmetry classes (hexagonal vs cubic) — so running Q-C on both is not redundant, it is the sharpest available test of whether the §2.88.B caveat's answer is structure-robust.
3. **CC leg dispatch.** The pre-registration is self-contained and ready to travel in-band for the full-from-scratch second leg.
