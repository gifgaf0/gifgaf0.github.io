# ERRATUM — FOLD_AUTHORIZATION_V4_71.md (size line)
**Filed:** July 28, 2026, chat leg, in response to a CC-leg audit observation. The original memo (md5 `a016995ce30ba708c69c62a994afe4b8`) is left untouched — it is referenced by md5 in the record; this erratum travels beside it.

## The observation (CC leg, credited)
The memo's size line reads "1,295,979 → 1,308,549 bytes (+12,570)" while the actual V4.71 file — same binding md5 `9517f4fb7aa2de65b0b4a69985962d8f` — is **1,347,411 bytes**.

## Root cause (fully reconciled; no integrity issue)
The fold script's log line reports `len(str)` — **Unicode character counts** — and the memo transcribed those figures with the label "bytes." The ledger is UTF-8 with heavy multi-byte content (§, Λ, ξ, →, ≤, subscripts), so characters ≠ bytes:

| quantity | characters (as the script prints) | bytes (filesystem) |
|---|---|---|
| V4.70 | 1,295,979 | **1,334,614** |
| V4.71 | 1,308,549 | **1,347,411** |
| fold insertion | +12,570 | **+12,797** |

Both columns are internally exact; only the label was wrong.

## Live re-verification performed at this filing (July 28, 2026)
The seven splice pairs were harvested from `foldin_v4_71_annex_cdef1.py` (md5 `03b170bd42d300f81a35209a4f0be006`) and applied in reverse to the canonical V4.71:
- per-splice insertions: E1-title +0 B, E2-header +2,905 B, E3-record +5,750 B, E4-annex +2,595 B, E5-q34 +206 B, E6-row +116 B, E7-changelog +1,225 B — total **+12,797 B**;
- reconstructed base: **1,334,614 B, md5 `969124145cd3070b266d3c5ecf44434e`** — the sealed V4.70 digest, byte-exact.

**The chain V4.70 → V4.71 is intact.** The script's "reverse-splice byte-identity" claim was always sound (string identity ⇒ byte identity for identical content); only the memo's unit label erred.

## Standing correction going forward
All future fold memos report **bytes** (from `wc -c` / `len(bytes)`), with character counts given only if explicitly labelled. H-protocol: this erratum stands as the correction record; nothing was silently edited.
