# Phase C report: the crypto negative result and the annotation batch (October 7, 2026)

**Plain-language summary.** Phase C banked one negative result and cleaned up the ledger. Everything it produced is either a ledger annotation or a draft for the author. Nothing has been published, submitted or sent.
- **The lattice cryptosystem fails at its own parameters.** Its structured public matrix collapses to rank 76 at every size from k = 7 up, so an attacker faces a 76-dimensional problem, not a 512-dimensional one. Even a fully random matrix gives about 2^51 security with the specified parameters, not 2^128. Decryption never fails, which the old failure-rate figure (2^(−6.4×10¹⁵)) obscured. A four-page note for the IACR ePrint archive is drafted.
- **The ζ-tax redshift fails.** It is "tired light": it reddens light without stretching time. Supernova light curves are stretched exactly as expansion predicts (DES 2024).
- **The electron's 2π closure becomes conditional.** The vacuum of record protects no phase winding. A protected 2π winding needs a vacuum choice (I6) that has been registered but not made. The mass exponent 2π/Φ and two "stable quantum" verdicts rest on it, so they are conditional too.
- **"The factor of 4 is the spin-3/2 quartet" is downgraded.** The 4 in the quark-model neutron moment is a spin-½ coupling weight. The spin-3/2 quartet is the Δ, and its neutral member has zero moment.
- **The polycrystal window is only 5–20 lattice cells wide,** and ξ = ℓ_P was never licensed on the light side.
- **§2.52 Open 3 gets the G-ζ1 result, and the freeze stays.**
- **Fourteen math corrections**, all checked exactly.

The ledger is folded to V4.94 (+40 KB). There are 113 pointers on dependent entries, and an independent check confirms the fold is purely additive.

## What came out

| Part | Finding | Legs | Draft or ledger change | What it needs from you |
|---|---|---|---|---|
| **C1** rank | 76 at k = 8, 16, 32, 64, at both primes, for every seed. Cause: a fixed 256 × 112 factor of rank 76. At p = 911 the rank falls short of full from k = 5 | Pre-registered; two legs, the second blind, run after the first was committed | 34 ledger pointers, including the "k ≤ 7, no collapse" correction to §2.69.5 | — |
| **C1** uniform-matrix spec | 2^51.0 by the lattice estimator (bdd; usvp β = 72). An independent core-SVP estimate also gives β = 72 | Estimator plus cross-check | OP-2.58.5 criterion (iii) FAILS | — |
| **C1** correctness | The noise is at most 258, against q/4 ≈ 1.07 × 10⁹, so DFR = 0. The old figure was a Gaussian tail outside the noise's range | Arithmetic | Replaces 2^(−6.4×10¹⁵) everywhere it appears | — |
| **C1** §3.05 carry-over | The sum-to-14 rule holds for 6 of 21 pairs. On the actual kernels, §2.59's two structures are one partition | Exact | §§2.59–2.61 and OQ-01 annotated | — |
| **C1** note | — | — | `phase_c/C1/eprint_draft/` (4 pp.) | Title, byline, contact; whether and when to submit |
| **C2 P1** ζ-tax gate 3 | **CLOSED — FAILED as framed.** A per-vertex amplitude penalty is tired light (b = 0); DES measures b = 1.003 ± 0.011. Added to expansion, its share is −0.003 ± 0.011 | Pre-registered; a second reading of the sources | Gate row, banked row and G-FOLD1's open flag annotated | Whether to open a frame/metric recast as a new entry |
| **C2 P2** polycrystal | The window edge is 4.96–19.82 cells, and a 20-cell floor empties it. ξ = ℓ_P is not licensed on the light side; one gate elected it | One leg (annotation) | 5 pointers; Part VI row for the floor | Choose the floor N (or none) |
| **C2 P3** 2π closure | **CONDITIONAL on I6.** π₁ = 0 at the vacuum of record. The winding is π on the polar strata, where protection is accidental, and 2π only where ψ₀ carries weight | Pre-registered; a second reading | 12 pointers: §2.50/.A, §2.14, OP-2.14, G-QUANTA, M.REL and others | — (G-OBD1 is the registered route to make I6 a computation) |
| **C2 P4** μ_n | **DOWNGRADED.** Two exact legs: μ_p = (4μ_u − μ_d)/3 from spin-½ weights 4/3 and −1/3; μ(Δ⁰) = 0 at μ_u = −2μ_d | Pre-registered; two legs | 18 pointers across §2.85, §2.87, §2.87.A–C, §2.91.R and Part VI | — |
| **C2 P5** §2.52 Open 3 | The G-ζ1 result is added (DEGENERATE; closest t = 0.36, 3.87× ζ). The freeze stays | — | One authorized append, asserted by both scripts | — |
| **C2 math** | The full table is in `phase_c/C2/C2_RESULT.md`. Highlights: Moreno closes OP-2.81.2; every Fano symmetry lifts with signs (1344); §2.77's involution is outer, and the order-4 images generate M₄(ℂ); 651 matchings, not 42; K₈ has six 1-factorizations; D₄, not V₄ × ℤ₂; the α⁻¹ entries name two starting values | Two blind subagent legs plus this session's checks; every reversal computed twice | 40 pointers | — |

**Leads corrected before folding.** Three of the findings file's leads were wrong in detail. The corrected forms are what was folded:
- **OP-2.81.1.** Moreno settles the count and the rank, not the kernel split. The split has a third class the ledger never mentions (1,344 kernels with no clean two-term vector).
- **§2.84A.** In that entry's own labels the swap is a ↦ 3a. The lead's 7⊕a ≡ −a holds only in Cayley–Dickson labels.
- **OP-2.74.1c.i.** TS_O1 is the class with e_a·e_b = **+**e_{a⊕b}, not −.

## Blast radius

The fold adds 113 pointers: 34 for C1 and 79 for C2.
- C2 by item: P1 3, P2 5, P3 12, P4 18, P5 1, math 40.
- Three new Part VI rows: the Phase C closure, the draft awaiting you, and the polycrystal-floor election.
- Every line is listed in `fold_v4_94/FOLD_AUTHORIZATION_V4_94.md`.

**What the fold-time sweep added** beyond the result files:
- **Crypto.** The §3.1 fix row (the DFR = 0 bound assumes it), the harness-port row, the §2.66.2 recovery and citation-hygiene rows, the OP-2.59 and RD rows, and §2.59's own comparison line.
- **2π.** The M.REL worked example, whose "π₁(S¹) = ℤ" assumes a vacuum with protected windings, plus G-VS1's own "not re-read" note.
- **μ_n.** Fifteen passages and rows in the μ_n / Gate 2a thread that carry the factor-of-4 reading, beyond the three the pre-registration named.

**Checked and deliberately left alone:**
- mentions that only say "no μ_n";
- §2.1's numbers (fitted, so unchanged);
- §2.75 Part I, which is true as written for 𝒴 as defined;
- G-MSCS-A, which reads the window edge but depends on no verdict here.

## Decisions waiting on you

1. **The ePrint note.** Title, byline and contact (left as a placeholder because the repository is public); whether and when to submit, since ePrint posting is permanent; and the AI-computation acknowledgement.
2. **Two crypto-project files** do not describe the spec and are flagged for correction:
   - `tools/lattice_estimate_results.md` claims "> 512 bits" from a failed estimator run with different noise and dimension;
   - `tools/SLWE_Prime_Master_v2.md` §4.4 lists β values that do not match core-SVP.
3. **The polycrystal floor.** Choose a minimum number of lattice cells per grain, or none. Under the declared chain, 20 cells closes the light-side window.
4. **The ζ-tax picture.** Gate 3 closed as framed. A frame or metric recast would time-dilate, but it would be a new entry with a new mechanism; gates 1, 2 and 4 are untouched.
5. **Found, not annotated** (outside this brief):
   - L2427's claim that the sum-15 twosets are all χ = −1 is false;
   - the findings file's §2.53 imaginaries column;
   - the other Part II §M–O findings: G-C1 vs §2.64.A, the verify-then-widen couplings, C.COSM.4, the §2.69 canary, the §4.7 blocker, and the cosmogony entries.
   These are for a later batch if you want them.
6. **The ledger.** The V4.94 file is attached. The project store still holds V4.91 and has 1,983 units free. Swapping in V4.94 needs your word and about 82 KB freed, or an instruction to keep the canonical ledger in the repository.

**Visibility.** The repository is public. The ePrint draft and the result files on branch `claude/audit-followup-oct6` can be read by anyone, although nothing is submitted.

## Process notes

- **Blind legs.**
  - **C1's rank.** The second leg built the algebra from the pre-registration text alone, after leg 1 was committed.
  - **C2's math.** Two subagents worked blind to each other and to this session. Their reports are saved verbatim (`math_A/REPORT.md`, `math_B/REPORT.md`), because the harness does not let subagents write report files.
  - **This session's own checks.** These were written without reading either subagent's code:
    - P4 (the quark moments);
    - the e₈-cancelling zero product;
    - the 651 matchings;
    - D₄;
    - the SL(2,7) conjugacy;
    - the signed lifts and the annihilation graph;
    - the generation of SL(2,7) by its order-4 elements, which gives M₄(ℂ) by Burnside.
- **Second readings.** P1 and P3 rest on quotations. `c2_quotes_check.py` re-reads them, and the P2 and P5 facts, verbatim from the V4.93 file (27 of 27 quotations found). DES was read from a second copy of the abstract.
- **H-1.** The independent fold check first failed its own count of "[→ V4.94" strings: §2.94's preamble names the pointer form twice. The check was corrected, not the fold, and both scripts were then re-run on the final text.
- **Proportionality.** Second legs were used only where a verdict could kill, downgrade, close or reverse. P2 and P5 and the factual math slips are one-leg annotations.

## Files

Everything is on branch `claude/audit-followup-oct6`:
- `audit_followup/phase_c/C1/`: the pre-registration, both rank legs, the comparison, the estimator run, the core-SVP cross-check, the correctness checks, `C1_RESULT.md` and the ePrint draft;
- `audit_followup/phase_c/C2/`: the pre-registration, `C2_RESULT.md`, `math_A/` and `math_B/` with their reports, and this session's checks;
- `audit_followup/fold_v4_94/`: the fold script, the independent check and the authorization record;
- `STATUS.md` at the repository root, updated.

The canonical `SQT_Master_Ledger_v4_94_CANONICAL.md` (md5 `708df4cf8f4703088c89b4fad96584bd`) is delivered in the conversation.
