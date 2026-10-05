# FOLD AUTHORIZATION — V4.91 (one figure at §2.91.V: the radiation ratio)

**Plain-language summary.** The author approved folding the one ledger figure that the paper's October 4 revision changed. The ledger's §2.91.V said fast matter radiates about 9×10¹⁰ times more power into second sound than into first sound. That figure used speeds the second computation later corrected; with the corrected speeds it is about 10¹¹. The old figure stays in place, as append-only discipline requires, with a bracket after it giving the corrected one. Nothing else in the ledger changed, and the checks confirm it. The project's stored copy of the ledger has not been replaced; that swap waits for the author's word, as at every fold.

**Recorded:** October 5, 2026, 03:22 UTC (October 4, 20:22 PDT).

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_90_CANONICAL.md`, md5 `ef69a5738e313c9d99ca2cdd641241f6` (1,777,039 B). The project-store copy was read back at fold time and is byte-identical |
| Result | `SQT_Master_Ledger_v4_91_CANONICAL.md`, md5 `ce9ca6873adb5686227f5d103b41e3cc` (1,778,302 B; +1,263 B, +1,199 characters) |
| Kind | Banking annotation, no gate: one figure |
| Edits | E1 title; E2 As-of prepend; E3 the V4.91 fold-in record (before the V4.90 record); E4 one bracket at the end of §2.91.V; E5 one changelog line |
| Not touched | Erratum (3)'s old text (kept verbatim); no Part VI row; no retraction; the §2.52 Open 3 row |

## The author's words (verbatim, October 4, 2026, 20:21 PDT)

> Go ahead a fold the updated figure

These words answer the staging note `../closure/NEXT_FOLD_NOTE.md` and the report that followed the paper's approval, which said the figure "is still waiting for your separate go-ahead to fold".

## The figure

- **Old (V4.89, §2.91.V erratum (3)):** "the 3D quadrupole slow/fast ratio is ≈ 9×10¹⁰". It used the first computation's c₁/c₂ = 33.6.
- **New:** about 10¹¹, between 1.10 × 10¹¹ and 1.79 × 10¹¹, from V4.90's two-leg c₁ = 16.1–17.0 and c₂ = 0.471 (c₁/c₂ = 34.3–36.1).
- **Sources:** `../paper/revision_numbers_check.py`, item R1. The paper's second reviewer recomputed it independently and got 1.10–1.79 × 10¹¹.

## Differences from the staging note

- **The bracket is shorter.** The staged bracket also said that the paper now derives the vortex couplings. In the ledger that sentence moved to the fold-in record, so the §2.91.V bracket carries only the figure (100 characters).
- **Provenance added to the record:** the fold-time repository state, and the paper's approval the same day (`../paper/APPROVAL_V1.md`).

## Repository state at fold (live `git ls-remote`, 2026-10-05 03:22:08 UTC)

| Ref | Value |
|---|---|
| `refs/heads/main` | `6cd2c66b42eb4f16cb3c50ef434466699a9b920b` (PR #35 merged at `3664ed1`, 2026-10-05 00:07:59 UTC) |
| `refs/heads/claude/lbc-bank-v489` | `15237eae0f0fc802acdb7e2f3e34dc7a396c70ea` (the approval record and the v1 build, made after the merge, so not yet on `main`) |

No canonical ledger is on `main`.

## Project store

The store is not changed by this fold.
- **Room:** project stats at fold time were 1,997,468 of 2,000,000 used, so 2,532 free. V4.91 is 1,263 B (1,199 characters) larger than V4.90, so the swap fits either way the units are counted.
- **The swap** (delete V4.90, write V4.91) waits for the author's word.

## Verification

- **Fold script:** `foldin_v4_91_radiation_ratio.py`, md5 `769808e91e246e800edb675624f6d051`.
  - Anchors are read from the file and asserted unique, including erratum (3)'s old text.
  - Every fragment lands exactly once.
  - The §2.52 Open 3 Part VI row is byte-identical and unique.
  - The reverse splice reconstructs V4.90 byte-identically, which is asserted before the output is accepted.
- **Independent check:** `verify_v4_91_additive.py`, md5 `4d8df9ddb52f23c9cc3f2a9cfbf8e824`, shares no code with the fold script. Its line-level diff shows exactly five change sites:
  - the declared title rewrite;
  - the declared As-of rewrite, with the old line's text after its version label kept verbatim at the end of the new line;
  - two pure insertions: the record (2 lines, 755 B) and the changelog line (208 B);
  - one in-line append at §2.91.V (100 characters added, none removed; the old 9×10¹⁰ text is still there).

  4,637 of the 4,640 V4.90 lines are carried unchanged, and the check reports PASS.
