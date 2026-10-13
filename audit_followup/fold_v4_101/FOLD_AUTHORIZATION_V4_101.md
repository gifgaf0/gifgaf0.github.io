# FOLD AUTHORIZATION — V4.101 (the SLWE note's revision deposited, and the gauge record's description)

**Plain-language summary.** This fold records two things you did on Zenodo after V4.100.
- **The revised SLWE note.** You deposited it as version 2 (doi:10.5281/zenodo.23352161). The notice on *Fluid Lattice Topology* now cites a note that contains the figures it quotes.
- **The gauge record.** You replaced its description with the v6.4 abstract.

The fold adds a short §2.101 and four pointers to it. Nothing already in the ledger was changed or removed, and the independent check confirms that. One fix is still to make on Zenodo: the note's description (see below).

**Recorded:** October 13, 2026, 15:01 PDT (22:01 UTC).

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_100_CANONICAL.md`, md5 `35a20a1f2db1ad66663b4cd60b7c8234` (1,923,114 B), at the repository root on `main` (`c3e5072`, the merge of PR #43) |
| Result | `SQT_Master_Ledger_v4_101_CANONICAL.md`, md5 `4a67c76037b63adc6037aec0d7f2ac4d` (1,926,632 B; +3,518 B) |
| Kind | Estate facts only, read from DataCite at fold time. The note's file could not be read, because Zenodo rate-limited the record page; §2.101 says so. Nothing is computed, so there is no leg |
| Edits | Title; As-of prepend; the V4.101 fold-in record (before the V4.100 record); §2.101 (after §2.100, before Cluster J); four in-line "[→ V4.101 (§2.101): …]" pointers; one changelog line |
| Checks | Reverse splice byte-identical to V4.100 (`fold_v4_101_output.txt`). The independent check passes too (`verify_v4_101_additive.py`, `verify_v4_101_output.txt`): four appends on the four typed hosts, each stating its fact; three insertions at the declared places; §2.100's heading, header and registers line, §2.99 and the V4.100 record unchanged. The check was also run against V4.100 itself and against a copy with one silent edit, and it failed on both, as it should. A dry run passed first, and its file was deleted |
| Estate | Head at fold `6235c51` (the staging, on `claude/ledger-v4-100-fold`; not in PR #43, which had been merged at 14:41 PDT). Live `git ls-remote` 2026-10-13 22:00:52 UTC: main = `c3e5072`. The fold is committed on `claude/ledger-v4-101-fold` |

## The author's words (verbatim)

Tuesday, October 13, 2026, 15:00 PDT, the fold word:

> Fold

It answers the staging's request ("Say 'fold' and I'll fold it"). The facts it folds were given at 14:53 PDT:

> https://doi.org/10.5281/zenodo.23352161.
>
> Gauge group abstract edited.

## The four pointers (V4.100 line numbers)

| Line | Entry | What the pointer says |
|---|---|---|
| 1912 | §2.100, item 3 (the note) | Deposited as version 2 on October 13, 2026 (doi:10.5281/zenodo.23352161) |
| 1914 | §2.100, item 5 (the gauge paper) | The author replaced the description with the v6.4 abstract on October 13 |
| 1915 | §2.100, item 6 (*Fluid Lattice Topology*) | The revision is on Zenodo since October 13 (doi:10.5281/zenodo.23352161) |
| 4655 | "Phase C draft awaiting the author" row | The revision was deposited as version 2 on October 13, 2026 |

## The facts, as read at fold time

- **The note's version 2.** DataCite gives 10.5281/zenodo.23352161 as a version of 10.5281/zenodo.23270248, registered 2026-10-13 21:52:56 UTC, with the note's title.
- **Its description.** Read again at 22:00 UTC, the description still runs words together at the draft's wrap points, and the four changes are unnumbered.
- **The gauge record.** DataCite last updated it at 21:39:31 UTC. Its description now says the rank-4 problem is "addressed by showing" and no longer lists hypercharge assignments.

## Still to do on Zenodo (not blocking)

- **The note's description.** Replace it with `../closeout/step3/3b_slwe_eprint/ZENODO_V2_DESCRIPTION_UNWRAPPED.txt`, the same 455 words with one line per paragraph or item. That is a metadata edit.
- **The note's file.** Glance at it: its md5 should begin `31284174`.

## Where the ledger lives

- **V4.101 at the root.** V4.101 takes V4.100's place at the repository root.
- **V4.100 stays in the history.** It remains in `main`'s history, at `c3e5072`.
- **To rerun the scripts.** The fold script and the check read V4.100 from the root, so restore it there first: `git show c3e5072:SQT_Master_Ledger_v4_100_CANONICAL.md > SQT_Master_Ledger_v4_100_CANONICAL.md`.
- **Merging.** Merge with a merge commit.
