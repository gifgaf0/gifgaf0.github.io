# FOLD AUTHORIZATION — V4.94 (the October 2026 audit follow-up, Phase C)

**Plain-language summary.** This fold records Phase C in one new ledger section, §2.94, and adds a short pointer to every entry the Phase C findings touch.

C1 is the crypto negative result. The program's lattice cryptosystem fails at its own parameters, for two separate reasons:
- its structured public matrix collapses to rank 76 at every size;
- even a random matrix gives about 2^51 security, not the 2^128 target.

On the other hand, decryption never fails, and the old failure-rate figure is replaced.

C2 is the annotation batch, and every item was verified before folding:
- the cosmological-redshift gate of the ζ-tax picture fails against supernova time dilation;
- the electron's 2π closure and what rests on it become conditional on a vacuum choice that has not been made;
- "the factor of 4 is the spin-3/2 quartet" is downgraded, because that quartet is the Δ;
- the polycrystal window is only 5–20 lattice cells wide, and ξ = ℓ_P is not licensed on the transverse line;
- the frozen §2.52 Open 3 row receives the G-ζ1 result, as the brief directs, and nothing else;
- fourteen math corrections are folded.

Nothing in the ledger was changed or removed, and the checks confirm it. The ePrint note is a draft. The project's stored copy of the ledger has not been replaced: the swap waits for the author's word and for room in the store (see below).

**Recorded:** October 7, 2026, 21:40 UTC.

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_93_CANONICAL.md`, md5 `0aa63a0bec9becbfb911dba3454255f2` (1,822,335 B), the output of the Phase B fold |
| Result | `SQT_Master_Ledger_v4_94_CANONICAL.md`, md5 `708df4cf8f4703088c89b4fad96584bd` (1,862,277 B; +39,942 B, +38,282 characters) |
| Kind | Audit fold: C1 (pre-registered; two legs on the rank) and C2 (pre-registered; second legs on P1, P3, P4 and the math reversals), plus their blast radius |
| Edits | E1 title; E2 As-of prepend; E3 the V4.94 fold-in record (before the V4.93 record); E5 §2.94 (after §2.93, before Cluster J); E6 113 in-line "[→ V4.94 …]" brackets (34 C1, 79 C2); E7 three Part VI rows after the Phase B rows; E8 one changelog line. No Preamble rule (no E4) |
| Not touched | Every existing sentence (brackets are appended only); the fold-in records and the As-of history (historical logs); no §3.x. The §2.52 Open 3 row receives exactly one append, the G-ζ1 result, as the brief authorizes |

## The author's words (verbatim, brief of October 6, 2026)

> Keep the discipline proportionate. Pre-register the decision rule for anything that can kill or downgrade. Use a blind second leg only where a new number or derivation decides a verdict. Everything else is an annotation.

> Work out the blast radius every time. For each kill or downgrade, list every entry that depends on it and annotate those entries in the same fold. V4.67 retired the gravity bridge but missed that the drag constrains matter itself. Don't repeat that.

> Prior Address, Eddington and M.CW apply. Every deliverable opens with a plain-language summary. The project store is full, so write to the repo. One short fold per phase.

> Draft, don't publish or send. Zenodo versions, journal notes and the note to Flach come back to me for approval.

> C1. Crypto negative result. – Confirm by direct computation that the Singer-orbit public matrix has rank ≤ 112 at several module ranks: k = 8, 16, 32, 64. – Run the lattice estimator on the spec parameters with a uniform matrix. – State correctness as a worst-case noise bound (DFR = 0), replacing the 2^(-6.4×10^15) figure. – Annotate the dependent rows (OP-2.58.2c/2e/5, §2.58.B, §2.66.1, §2.66.2) and carry the §3.05 correction into §§2.59–2.61. – Draft a short standalone note. IACR ePrint is the natural venue.

> C2. Annotation batch, one fold. Verify each item first.

> §2.52 Open 3. Add the G-ζ1 result, and leave the freeze in place.

> Phase C: the crypto note draft and one annotation fold.

**The §2.52 Open 3 row.** Every fold since V4.36 has left this row untouched under a standing instruction. The brief's C2 item is the first instruction to change it, and only by adding the G-ζ1 result: "Add the G-ζ1 result, and leave the freeze in place." The fold adds that one bracket and nothing else. The row stays Open. The fold script and the independent check each assert that the V4.94 row equals the V4.93 row plus exactly that append.

## What was folded, and from where

| Part | Result file | Finding | Draft (not submitted) |
|---|---|---|---|
| C1 crypto negative result | `phase_c/C1/C1_RESULT.md` (pre-registration `C1_PREREG.md` 778e3d4a, lock ce82bdc; leg 1 committed 782594c before the blind leg 2) | Rank 76 at k = 8, 16, 32, 64 at both primes, via a fixed 256 × 112 factor of rank 76. Uniform-matrix spec at 2^51.0 (lattice estimator; core-SVP β = 72). DFR = 0 by a worst-case bound. Sum-to-14 holds for 6 of 21 pairs | `phase_c/C1/eprint_draft/` (4 pp., LaTeX + PDF) |
| C2 annotation batch | `phase_c/C2/C2_RESULT.md` (pre-registration `C2_PREREG.md` e538b2e5, lock d6fee69; blind math legs `math_A/`, `math_B/`; this session's `c2_checks*.py`, `c2_quotes_check.py`) | P1 FAILED as framed. P2 annotated. P3 CONDITIONAL. P4 DOWNGRADED. P5 G-ζ1 appended. Fourteen math items | — |

## Where the brackets go (V4.93 line numbers)

The result files' tables gave the core targets. A sweep of the whole V4.93 ledger at fold time found the rest of the dependents, using:
- for C1: "SLWE", "DFR", "Singer", "OP-2.58", "§2.58", "§2.66", "§2.69.5", "sum-14", "§3.05";
- for C2: each item's terms ("ζ-tax", "W^EM_∪", "ξ = ℓ_P", "§2.50", "OP-2.14", "first-stable", "factor of 4", "spin-3/2", "quartet", "μ_n", and the math items' sections).

Lines that only say "no μ_n", or that cite an entry without depending on the corrected claim, are not bracketed. C2_RESULT.md lists the ones checked and left alone.

| Part | Lines | Entries |
|---|---|---|
| C1 (34) | 3233, 3241, 3290, 3292, 3332, 3335, 3347, 3359, 3374, 3445, 3453, 3474, 3490, 3525, 3539, 3541, 3543, 3817, 4421, 4444, 4445, 4446, 4447, 4448, 4449, 4452, 4453, 4454, 4458, 4459, 4539, 4540, 4608, 4611 | the Cluster M head; §2.58.B status; OP-2.58.1.a and OP-2.58.5 items; §2.59 (a) and its comparison; §2.60 Result I; §2.61 Result I; RD-03; §2.66 production scaling and the q-binding item; §2.66.1 figure and closure; §2.66.2's "DOES establish", OP-2.58.2c/2e items and closure conditions; §2.69.5's security reading; the Part VI rows G-BKZ32, OP-2.58.1.a/1.b/2/2c/2d/2e/5, OP-2.59, RD-01–04, the §2.66.2 recovery and hygiene rows, the §3.1 fix and harness-port rows; the closed list's OQ-01 and OP-2.58.1.a |
| C2 P1 (3) | 4364, 4378, 4599 | the banked ζ-tax row; G-FOLD1's "flagged, not adjudicated"; ζ-tax gate 3 |
| C2 P2 (5) | 293, 1632, 1658, 4420, 4424 | ANNEX-CDEF-1; §2.91.H (G-SCALE1); §2.91.N (G-CI1, the window); the G-CI1 and G-S2C1-W rows |
| C2 P3 (12) | 279, 283, 424, 1373, 1379, 1662, 1672, 4255, 4376, 4382, 4425, 4610 | M.REL worked example and rationale; §2.14; §2.50; §2.50.A; §2.91.P (G-QUANTA); §2.91.U (G-VS1's "not re-read"); §4.10; the electron Cl(2) and stability-memo rows; the G-QUANTA row; OP-2.14 in the closed list |
| C2 P4 (18) | 1045, 1053, 1057, 1067, 1080, 1084, 1096, 1100, 1118, 1134, 1154, 1666, 4438, 4563, 4565, 4574, 4578, 4579 | §2.85 Parts B, D, E; §2.87 (reduction, unification, net); §2.87.A (assignment, four-4, Gate 2a sharpened); §2.87.B net; §2.87.C; §2.91.R; the Part VI rows G-2a-S1/S2, the μ_n gate, σ₄\|₂O, Gate 2a, the factor-assignment question, the locking derivation |
| C2 P5 (1) | 4393 | the §2.52 Open 3 row (the single authorized append) |
| C2 math (40) | 408, 484, 496, 1353, 1740, 1760, 1782, 1792, 1950, 1972, 2003, 2036, 2060, 2068, 2149, 2194, 2353, 2371, 2440, 2442, 2461, 2494, 2531, 2771, 2772, 2853, 2857, 2869, 3189, 3215, 3219, 3402, 3412, 4468, 4469, 4478, 4531, 4533, 4543, 4587 | (a) OP-2.81.1/2 and §2.68.8.1; (b) signed lifts; (c) §2.77 and §2.E-WD; (d) the size-2 matchings; (e) K₈; (f) arctan(1/√2); (g) log(4π)/log 7; (h) §2.62.B/C; (i) §2.84A; (j) OP-2.74.1c.i/iii; (k) de Marrais in §2.55, §2.68.4 and §2.41.B; (l) α⁻¹. Lines 496 and 1760 each carry a combined bracket, (a)+(d) and (b)+(k); line 1782 carries the K₈ correction with a pointer to (h) |

**Changes from the result files' proposed texts.**
- **C1.** One bracket was added at §2.59's "Negative result" (L3335). With Fano points as F₂³'s nonzero vectors, the co-line partners of a⊕b are its Hamming syndrome class. So on the actual kernels, §2.59's two structures are one partition. This identity follows from the XOR construction already used in `c1_checks.py`.
- **(b).** The bracket sits at §2.75 Part VI's "do not lift to algebra automorphisms" (L2353), the statement the signed lifts contradict. It does not sit at Part I (L2301). Part I is true as written for 𝒴 as defined, and the pre-registered M-rev rule annotates only what the computation contradicts.
- **(d) and (h).** The size-2-matching and stabilizer brackets keep the subagents' wording, shortened. "D₄ \ V₄ swaps" is written as "the elements of D₄ outside V₄ swap".
- **(c).** At L2869 and L2531, the bracket keeps what stands — no four order-4 images anticommute pairwise — next to the correction that the generated algebra is M₄(ℂ).
- **(i), (j), (a).** The corrected forms are folded, not the leads' wording: a ↦ 3a in §2.84A's labels; TS_O1 is the + class; OP-2.81.1 is only partly answered.

## Repository state at fold (live `git ls-remote`, 2026-10-07 21:35:09 UTC)

| Ref | Value |
|---|---|
| `refs/heads/main` | `3587eb3098e4f7652685e4f16de5cd7583a9fa4a` (PR #37 merged) |
| `refs/heads/claude/audit-followup-oct6` | `53923faa30f9f0468166254ece70f934d153a98a` (the estate through C2's verification) |

No canonical ledger is committed to the repository; the V4.94 file is delivered in the conversation. The repository is public, so the Phase C drafts on this branch are publicly visible, although none is published or submitted.

## Project store

The store is not changed by this fold.
- **Room:** re-read at fold time, the store holds 1,998,017 of 2,000,000, leaving 1,983 free. It still holds V4.91; V4.92 and V4.93 were not swapped in.
- **The problem:** V4.94 is 83,975 B larger than V4.91, so a delete-and-write swap does not fit.
- **What the swap needs:** the author's word, plus about 82 KB freed in the store, or an instruction to keep the canonical in the repository instead.

## Verification

- **Fold script:** `foldin_v4_94_phase_c.py`, md5 `bc3b9b8a56f2d1fde171db32394dce28`; log `fold_v4_94_output.txt` (md5 `548fdea5c51d961a4b0f6bfd29b6f941`).
  - Every anchor is read from the file and asserted unique. Each bracketed line is found by a unique prefix.
  - Every fragment lands exactly once.
  - The §2.52 Open 3 row equals the V4.93 row plus exactly the one authorized append.
  - The reverse splice reconstructs V4.93 byte-identically, and this is asserted before the output is accepted.
- **Independent check:** `verify_v4_94_additive.py`, md5 `15f9cf0469285fc171d34c9dc0a8c036`; log `verify_v4_94_output.txt` (md5 `132196039492cc9ec79323eb91edbd4a`). It shares no code with the fold script.
  - **Survival.** Every V4.93 line survives, either unchanged (4,580 lines) or as an in-line append whose added text matches `[→ V4.94 (§2.94.C1|C2): …]` (113 lines).
  - **Placement.** The 113 appends sit on exactly the 113 line numbers in the table above, which the check carries as its own list (C1 34, C2 79).
  - **Part labels.** Each append carries its line's part label.
  - **Aim.** Each host line contains a keyword typed in the check from a reading of that line, a guard against a mis-aimed anchor.
  - **Rewrites.** The only rewrites are the declared title and As-of lines. The old As-of text after its version label is kept verbatim at the end of the new line.
  - **Insertions.** Everything else is a pure insertion, 16 lines (11,833 B), in four blocks at the declared places:
    - the record, before the V4.93 record;
    - §2.94, between §2.93's last paragraph and Cluster J;
    - three Part VI rows, between the Alpha-decay row and the G-C1 row;
    - the changelog line, after the V4.93 line.
  - **§2.52 Open 3.** The row is the V4.93 row plus exactly one append, the G-ζ1 result, ending "The row stays Open and frozen."
  - Result: PASS.
- **Honesty item H-1 (the checker, not the fold).** The first run of the independent check failed one assertion. It expected the string "[→ V4.94 (§2.94.C" to occur 113 times in V4.94, but it occurs 115 times. The two extra are §2.94's own preamble sentence naming the two pointer forms. The check was corrected to count occurrences inside inserted text separately, and it requires exactly those two. The fold was not changed between the two runs. The §2.94 wording was then tightened once (the Registers line), and both scripts were re-run; the hashes above are from that final run.
