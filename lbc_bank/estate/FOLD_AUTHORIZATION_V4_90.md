# FOLD AUTHORIZATION — V4.90 (banking annotation: the paper-cited LBC numbers closed two-leg)

**Plain-language summary.** The author approved folding the staged V4.90 record into the ledger. It records three things:
- the outcome of the second, independent computation;
- the three first-computation defects that computation exposed;
- the corrected values at §2.91.V.

Nothing earlier in the ledger was changed, and the checks confirm it. The project's stored copy of the ledger has not been replaced yet; that swap waits for the author's word, as at every fold.

**Recorded:** October 4, 2026, 21:21 UTC.

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_89_CANONICAL.md`, md5 `db01bd273629ce7a385ff3c7fb6efdfc` (1,773,873 B). The project-store copy was read back at fold time and is byte-identical |
| Result | `SQT_Master_Ledger_v4_90_CANONICAL.md`, md5 `ef69a5738e313c9d99ca2cdd641241f6` (1,777,039 B; +3,166 B, +3,073 characters) |
| Kind | Banking annotation, no gate: register upgrade of the paper-cited numbers only |
| Edits | E1 title; E2 As-of prepend; E3 the V4.90 fold-in record (before the V4.89 record); E4 one bracket at the end of §2.91.V; E5 one changelog line |
| Not touched | No Part VI row; no retraction; the §2.52 Open 3 row untouched |

## The author's words (verbatim, October 4, 2026, 14:16 PDT)

> Go ahead and fold v 4.90

These words answer the staging note `../closure/V4_90_STAGING.md`, which closed with "It needs your word to fold" and "No fold is authorized by this note".

## Differences from the staging note

- **Format.** The staged record and bracket were written as bulleted blockquotes for reading. In the ledger they are rendered as single paragraphs, the form of every earlier record. The content is the same, compressed to keep the additions short (+3.2 kB).
- **One clause added to the §2.91.V bracket.** The 3D ratio c₂/c_T ≈ 0.06 (was 0.062, a value also quoted in the §2.91.I annotation). The staging note listed the corrected 3D shear speeds (7.75–8.04) and c₂ = 0.471 but not the ratio they imply (0.059–0.061).
- **Provenance added to the record.** The fold-time repository state, and a note that the estate branch also holds the Cox v4 body read. That read changes no ledger line.

## Repository state at fold (live `git ls-remote`, 2026-10-04 21:20:40 UTC)

| Ref | Value |
|---|---|
| `refs/heads/main` | `a9b5cabfd4b641f2d48ff7a03ce7b3d9316d35e4` (PR #36, the second leg, merged 18:09:13 UTC) |
| `refs/heads/claude/lbc-bank-v489` | `2ec5baf62b662b21be123edcb5cae3b228b18e95` (PR #35, open, mergeable) |

No canonical ledger is on `main`.

## Project store

The store is not changed by this fold.
- **Room:** project stats at fold time were 1,996,147 of 2,000,000 used, so 3,853 free. V4.90 is 3,166 B (3,073 characters) larger than V4.89, so the swap fits either way the units are counted.
- **The swap** (delete V4.89, write V4.90) waits for the author's word, per the standing practice that the author authorizes each store swap.

## Verification

- **Fold script:** `foldin_v4_90_lbc_closure.py`, md5 `964e49c5dd161ed5e0a2eeb4a688ba0c`.
  - Anchors are read from the file and asserted unique.
  - Every fragment lands exactly once.
  - The §2.52 Open 3 Part VI row is byte-identical and unique.
  - The reverse splice reconstructs V4.89 byte-identically, which is asserted before the output is accepted.
- **Independent check:** `verify_v4_90_additive.py`, md5 `f6617f30a20006162d403021c323988c`, shares no code with the fold script. Its line-level diff shows exactly five change sites:
  - the declared title rewrite;
  - the declared As-of rewrite, with the old line's text after its version label kept verbatim at the end of the new line;
  - two pure insertions: the record (2 lines, 1,792 B) and the changelog line (208 B);
  - one in-line append at §2.91.V (590 characters added, none removed).

  4,634 of the 4,637 V4.89 lines are carried unchanged, and the check reports PASS.
