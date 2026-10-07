# FOLD AUTHORIZATION — V4.93 (the October 2026 audit follow-up, Phase B)

**Plain-language summary.** This fold records Phase B in one new ledger section, §2.93, and adds a short pointer to every entry the Phase B findings touch. Phase B was about the program's public work: the papers and the calculators. In order:
- the second-sound paper already had every fix the brief asked for;
- the gauge paper needs a correction: its hypercharge sign rule is inconsistent and its Cabibbo value is ruled out by data;
- the PSL(2,7) note gets a version 3 that cites the classical literature and fixes one miscount;
- Paper VII and the calculators drop "Zero Free Parameters" and retire the W-mass and weak-angle formulas;
- the alpha-decay paper gets its first ledger entry;
- the η computation once asked of Flach has lost its purpose, and a short note to him is drafted.

All of these are drafts. Nothing has been published, deposited, deployed or sent.

Nothing already in the ledger was changed or removed, and the checks confirm it. The project's stored copy of the ledger has not been replaced; the swap waits for the author's word and for room in the store (see below).

**Recorded:** October 7, 2026, 19:10 UTC.

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_92_CANONICAL.md`, md5 `a98cf1b6f12578537e11270d2cdf0fda` (1,800,402 B), the output of the Phase A fold |
| Result | `SQT_Master_Ledger_v4_93_CANONICAL.md`, md5 `0aa63a0bec9becbfb911dba3454255f2` (1,822,335 B; +21,933 B, +21,217 characters) |
| Kind | Audit fold: six Phase B parts (B1 pre-registered and two-leg; B0 and B2–B5 annotations) plus their blast radius |
| Edits | E1 title; E2 As-of prepend; E3 the V4.93 fold-in record (before the V4.92 record); E5 §2.93 (after §2.92, before Cluster J); E6 34 in-line "[→ V4.93 …]" brackets; E7 three Part VI rows after the G-RCX1 row; E8 one changelog line. No Preamble rule (no E4) |
| Not touched | Every existing sentence (brackets are appended only); the fold-in records and the As-of history (historical logs); the §1.1 heading line (its "SUBMISSION READY" is covered by the Paper status bracket); no §3.x; the §2.52 Open 3 row |

## The author's words (verbatim, brief of October 6, 2026)

> Keep the discipline proportionate. Pre-register the decision rule for anything that can kill or downgrade. Use a blind second leg only where a new number or derivation decides a verdict. Everything else is an annotation.

> Work out the blast radius every time. For each kill or downgrade, list every entry that depends on it and annotate those entries in the same fold. V4.67 retired the gravity bridge but missed that the drag constrains matter itself. Don't repeat that.

> Prior Address, Eddington and M.CW apply. Every deliverable opens with a plain-language summary. The project store is full, so write to the repo. One short fold per phase.

> Draft, don't publish or send. Zenodo versions, journal notes and the note to Flach come back to me for approval.

> B4. Alpha-decay paper. – Add a ledger entry.

**How "drafts only" was read.** The brief's Phase B heading is "PHASE B: PUBLIC WORK (drafts only)", and its deliverables line says "Phase B: drafts only." That rule is applied to the public work: no paper, note or calculator leaves the repository. The ledger fold is internal and follows "One short fold per phase", B4's "Add a ledger entry" and the blast-radius rule. As at V4.92, the canonical file is delivered in the conversation, and the store copy is not replaced without the author's word.

## What was folded, and from where

| Part | Result file | Finding | Draft (not published) |
|---|---|---|---|
| B0 second-sound paper | `phase_b/B0/B0_RESULT.md` | All eight items already in the approved v1 | None needed |
| B1 gauge paper | `phase_b/B1/B1_RESULT.md` (pre-registration `B1_PREREG.md` 5374289d, lock c2148ae; two legs, 32/32) | Sign dressing (N-I); sin θ_C = 3/13 excluded; the PSL(2,7)-symmetry claim is the ledger's | v6.4 (`v6_4_draft/`) |
| B2 PSL(2,7) note | `phase_b/B2/B2_RESULT.md` | Prior art; 146 not 104; Kawasaki statement corrected; D₄ already fixed in v2.1 | v3 as tracked changes (`v3_draft/`) |
| B3 Paper VII and calculators | `phase_b/B3/B3_RESULT.md` | Scoped wording; m_W = m₀φ²⁷ and sin²θ_W = φ⁻³ retired; F₇* ⊄ PSL(2,7); L per diameter vs per radius | site v3.1, `SQTCalculator.jsx` v2.1, `sqt_v20_merged.jsx` v1.9.1, Paper VII |
| B4 alpha-decay paper | `phase_b/B4/B4_RESULT.md` | 51 steps, not 74; one robust break at Z = 88; §4.5–§4.6 unsupported; ²⁰⁸Pb has Q_α > 0 | Ledger entry §2.93.B4; corrections listed for the author |
| B5 η / Flach | `phase_b/B5/B5_RESULT.md` | Purpose closed at V4.84; the space on record is S⁷/PSL(2,7) | `FLACH_NOTE_DRAFT.md` |

## Where the brackets go (V4.92 line numbers)

The result files' tables gave 23 brackets. A sweep of the whole V4.92 ledger at fold time, for every term each finding touches, found 11 more dependents (marked +). Total: 34.

| Part | Lines | Entries |
|---|---|---|
| B1 (15) | 532, 534+, 539+, 2193, 2219+, 2260, 2269, 2351, 2507, 2773, 2920+, 3050, 3207+, 4359, 4360 | §2.D-FC status, its Paper I cross-reference and its premise sentence; §2.74 cross-references, Part II item 2 and audit trail; §2.75 cross-references; OP-2.75-CR; §2.77; §2.E-WD; the V4.7 §2.E-QQ entry; the V4.9 §2.E-QQ sections; §2.86 cross-references; the Part V V4.59 and V4.61 gauge-paper rows |
| B2 (3) | 315, 349, 1069 | §1.1 Theorem 2.1; §1.1 Paper status; §2.87 step (i) |
| B3 (10) | 385, 395+, 396+, 655, 1008+, 1682, 3880, 3884, 3913+, 4477 | §2.1 headline and its W and Z rows; §2.15 support list (Z_f = 6, with open verification (2)); §2.83 Part II's chain reading (F₇* on Fano triangles); §2.92.C(6); §2.64.A verify-then-widen list, Flag 4 and the Flag 4 list item; the Part VI string-update row |
| B4 (4) | 227+, 500, 527, 1431 | M.CW instances (the one-break record); §2.17 Lemma θ (incidental arithmetic); §2.21; §2.45-NGA |
| B5 (2) | 1065+, 4553 | §2.87's unification sentence; the Part VI η-defect row |

**Changes from the result files' proposed texts.**
- **B1, §2.D-FC.** "trivial Schur multiplier, so no spin cover" became "no genuinely projective (spin) representations". A ℤ₂ central extension of AGL(1,7) exists (through its abelianization ℤ₆), but with a trivial multiplier every projective representation is linear.
- **B4.** Four refinements; details are in the note at the end of `B4_RESULT.md`.
  - *§2.45-NGA* is restated in terms of Z. The paper counts U = Z − 80, while the ledger's slot framework uses its own U (§2.45-NGA puts U = 8 at Rn; §3.A.4 puts ²⁴⁰Pu, Z = 94, at U = 16). The result file's sentence that the paper's regime edges "are the retracted 4-8-12 sequence" is replaced by a narrower one: capacity readings of the edges (8 = dim 𝕆, 12 = |A₄|) depend on measuring U from Hg, Z = 80; from ²⁰⁸Pb the edges sit at ΔU = 6 and 10, as the paper's §4.5 notes.
  - *The ferromagnetism item* the ledger marks "refuted, R3" is the conjecture's Gate-1 spin-flip reading, not Lemma θ, so §2.93.B4 cites only §3.01 and §3.02.
  - *The Curium sentence.* §4.6 says the prediction is "not confirmed", but the abstract says its Cm→Cf half is "confirmed" at t = +0.4. This is added to the corrections list and to the Part VI row.
  - *§2.21.* The bracket drops the decay-chain sentence, which concerns the paper, not §2.21.
- **B5.** "No longer needed for μ_n" became "no longer needed for that purpose". §2.91.R (V4.84) still lists "the FR/η parity of Gate 2b" among what a derived μ_n would rest on; what closed is an FR sign from the internal geometry.

## Repository state at fold (live `git ls-remote`, 2026-10-07 19:05:01 UTC)

| Ref | Value |
|---|---|
| `refs/heads/main` | `3587eb3098e4f7652685e4f16de5cd7583a9fa4a` (PR #37 merged) |
| `refs/heads/claude/audit-followup-oct6` | `d21dcc4bd5c915b34e2e13f7727ae6a029bcf3d1` (the estate through B5) |

No canonical ledger is committed to the repository; the V4.93 file is delivered in the conversation. The repository is public, so the Phase B drafts on this branch are publicly visible, although none is published, deployed or deposited.

## Project store

The store is not changed by this fold.
- **Room:** at the V4.92 fold the store held 1,998,017 of 2,000,000, leaving 1,983 free. V4.92 was not swapped in.
- **The problem:** V4.93 is 44,033 B larger than V4.91, the copy in the store (re-read at fold time: 1,998,017 of 2,000,000 used), so a delete-and-write swap does not fit.
- **What the swap needs:** the author's word, plus about 42 KB freed in the store, or an instruction to keep the canonical in the repository instead.

## Verification

- **Fold script:** `foldin_v4_93_phase_b.py`, md5 `2814bfd5bf494be1d9f45d4695704491`; log `fold_v4_93_output.txt`.
  - Every anchor is read from the file and asserted unique, and each bracketed line is found by a unique prefix.
  - Every fragment lands exactly once.
  - The §2.52 Open 3 row is byte-identical and unique.
  - The reverse splice reconstructs V4.92 byte-identically, and this is asserted before the output is accepted.
- **Independent check:** `verify_v4_93_additive.py`, md5 `4c260ea7a5704843c6de9015243b1028`; log `verify_v4_93_output.txt` (md5 `dbcc1f330edd5ef3fd20e8d778073a8c`). It shares no code with the fold script.
  - Every V4.92 line survives unchanged (4,635 lines) or as an in-line append whose added text matches `[→ V4.93 (§2.93.Bx) …]` (34 lines).
  - The 34 appends sit on exactly the 34 line numbers in the table above, which the check carries as its own list (B1 15, B2 3, B3 10, B4 4, B5 2).
  - The only rewrites are the declared title and As-of lines. The old As-of text after its version label is kept verbatim at the end of the new line.
  - Everything else is a pure insertion, 24 lines (13,187 B), in four blocks at the declared places:
    - the record, before the V4.92 record;
    - §2.93, between §2.92's last paragraph and Cluster J;
    - three Part VI rows, between the G-RCX1 and G-C1 rows;
    - the changelog line, after the V4.92 line.
  - Result: PASS.
