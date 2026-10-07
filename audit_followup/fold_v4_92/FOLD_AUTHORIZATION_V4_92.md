# FOLD AUTHORIZATION — V4.92 (the October 2026 audit follow-up, Phase A)

**Plain-language summary.** This fold records the four Phase A results of the October 6 audit follow-up in one new ledger section, §2.92, and adds a short pointer to every entry those results affect. In order:
- the gravitational-wave reading of the transverse line fails the polarization test;
- the vacuum's hidden internal waves are soft and slow;
- the proton ropelength check fails;
- the two static gravity entries are downgraded.

It also adds one standing rule to the Preamble: any gravity mechanism must make everything fall alike, to MICROSCOPE's precision (KC-EP).

Nothing already in the ledger was changed or removed, and the checks confirm it. The project's stored copy of the ledger has not been replaced. The swap waits for the author's word, and this time it also needs room in the store (see below).

**Recorded:** October 7, 2026, 16:45 UTC.

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_91_CANONICAL.md`, md5 `ce9ca6873adb5686227f5d103b41e3cc` (1,778,302 B). The project-store copy was read back at fold time and is byte-identical |
| Result | `SQT_Master_Ledger_v4_92_CANONICAL.md`, md5 `a98cf1b6f12578537e11270d2cdf0fda` (1,800,402 B; +22,100 B, +21,375 characters) |
| Kind | Audit fold: four pre-registered parts (A1–A3 two-leg; A4 dispositions) plus their blast radius |
| Edits | E1 title; E2 As-of prepend; E3 the V4.92 fold-in record (before the V4.91 record); E4 the Preamble KC-EP rule (before the M.ONT flag); E5 §2.92 (after §2.91.V, before Cluster J); E6 44 in-line "[→ V4.92 …]" brackets; E7 three Part VI rows after the G-VS1 row (the Phase A closure, G-OBD1, G-RCX1); E8 one changelog line |
| Not touched | Every existing sentence (brackets are appended only); the fold-in records and the As-of history (historical logs); no §3.x; the §2.52 Open 3 row |

## The author's words (verbatim, brief of October 6, 2026)

> Work out the blast radius every time. For each kill or downgrade, list every entry that depends on it and annotate those entries in the same fold. V4.67 retired the gravity bridge but missed that the drag constrains matter itself. Don't repeat that.

> Prior Address, Eddington and M.CW apply. Every deliverable opens with a plain-language summary. The project store is full, so write to the repo. One short fold per phase.

> Equivalence principle. Any surviving mechanism must couple universally to mass-energy, including binding energy and electrons (ε_e), at MICROSCOPE's ~10^-15 level. Make this a standing kill condition.

> Deliverables […] Phase A: the polarization gate (prereg, derivation, second-leg check, verdict, blast radius), the internal-mode results, the matter and gravity dispositions, one fold, and a plain-language status.

## What was folded, and from where

| Part | Pre-registration (md5, lock commit) | Result file | Verdict |
|---|---|---|---|
| A1 polarization gate | `A1_PREREG.md` d5f6aa3b…, 44e12de (+ Addendum 1) | `A1_polarization/A1_VERDICT.md` | FALSIFIED: S2 pure vector; GW170817 pass withdrawn |
| A2 internal modes | `A2_PREREG.md` fd2e9597…, eefeef2 | `A2_internal_modes/A2_RESULT.md` | two DOWNGRADES; G-OBD1 registered |
| A3 matter sector | `A3_PREREG.md` e2f1090c…, 53667db | `A3_matter/A3_RESULT.md` | §2.15 → Conjecture; linking unprotected; §2.1 a fit; G-RCX1 registered |
| A4 gravity entries | `A4_PREREG.md` 7b876a27…, 08d6295 | `A4_gravity/A4_RESULT.md` | §2.89 and §2.90 DOWNGRADED; KC-EP declared |

**Where the brackets go.** The 44 brackets follow the blast-radius tables in the four result files:
- A1 block: 24 brackets (the three M.ONT/M.REL annexes, §2.88.E, §2.91.A/B/D/H/I/M/N/O/Q/S/T, the Part V polycrystal row, and eight Part VI rows). The VC-B annex bracket also carries the A2 and A3 points, and the §2.91.D bracket carries A4's KC-EP.
- A2: 4 (§2.91.U, §2.88.D.2, §2.91.P, the Part VI G-VS1 row).
- A3: 9 (§2.15, §§2.4–2.6, §2.82, §2.14, §2.1, the M.ONT declaration, and the Part V/VI rows for G-Φ1, the M.ONT gate and G-κ1).
- A4: 7 (four on §2.90, two on §2.89, one on §2.88).

## Repository state at fold (live `git ls-remote`, 2026-10-07 16:41:35 UTC)

| Ref | Value |
|---|---|
| `refs/heads/main` | `3587eb3098e4f7652685e4f16de5cd7583a9fa4a` (PR #37 merged) |
| `refs/heads/claude/audit-followup-oct6` | `3297421aa8ae8203f3efd248e0e15256da42e201` (the Phase A estate, through A4) |

No canonical ledger is committed to the repository; the V4.92 file is delivered in the conversation.

## Project store

The store is not changed by this fold.
- **Room:** at fold time the store held 1,998,017 of 2,000,000, leaving 1,983 free.
- **The problem:** V4.92 is 22,100 B larger than V4.91, so a delete-and-write swap does not fit.
- **What the swap needs:** the author's word, plus about 20 KB freed in the store, or an instruction to keep the canonical in the repository instead.

## Verification

- **Fold script:** `foldin_v4_92_phase_a.py`, md5 `bb50700aeefe20e8eabc0b0aebb60f28`.
  - Every anchor is read from the file and asserted unique, and each bracketed line is found by a unique prefix.
  - Every fragment lands exactly once.
  - The §2.52 Open 3 row is byte-identical and unique.
  - The reverse splice reconstructs V4.91 byte-identically, and this is asserted before the output is accepted.
- **Independent check:** `verify_v4_92_additive.py`, md5 `f6670077ed75938cf1c76e183649b863`, shares no code with the fold script.
  - Every V4.91 line survives unchanged (4,597 lines) or as an in-line append, the added text matching `[→ V4.92 …]` (44 lines).
  - The only rewrites are the declared title and As-of lines; the old As-of text after its version label is kept verbatim at the end.
  - Everything else is a pure insertion: 28 lines, 11,990 B, comprising the two new headings and their text, the record, three Part VI rows and the changelog line.
  - Result: PASS.
