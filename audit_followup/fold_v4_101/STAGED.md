# V4.101 — staged, awaiting the author's fold word

**Plain-language summary.** This fold would record two things you did on Zenodo after V4.100 was folded.
- **The revised SLWE note.** You deposited it as version 2, doi:10.5281/zenodo.23352161. With it on Zenodo, the notice on *Fluid Lattice Topology* now cites a note that contains the figures it quotes.
- **The gauge record's description.** You replaced it with the v6.4 abstract.

V4.100 says the first of these was not yet done, so the fold adds a short §2.101 and four pointers to it. Nothing is computed, and no verdict, register or row status changes. It is not canonical until you give the fold word.

**What it adds** (dry run: +3,358 B):
- **§2.101, after §2.100.** It covers the note's version 2 (DOI, registration, file) and the gauge description.
- **Four pointers.** On §2.100's items 3 (the note), 5 (the gauge paper) and 6 (*Fluid Lattice Topology*), and on the "Phase C draft awaiting the author" row.
- **Bookkeeping.** The record, the title and As-of bump, and the changelog line.

**Facts and their sources.**
- **The deposit.** DataCite, read on October 13: 10.5281/zenodo.23352161 is a version of 10.5281/zenodo.23270248, registered 21:52:56 UTC.
- **The gauge description.** It was updated at 21:39:31 UTC; it now says "addressed by showing" and no longer lists hypercharge assignments.
- **The file.** The note's file could not be read at staging, because Zenodo rate-limited the request. The fold script takes what is read at fold time as `--file-check`. The file should be `slwe_negative_result_v2.pdf`, md5 `312841740b484f731d452c11e445a260`.

**The description's spacing.** As DataCite harvested the note's description, words run together at the draft's wrap points, 24 joins in all. `../closeout/step3/3b_slwe_eprint/ZENODO_V2_DESCRIPTION_UNWRAPPED.txt` is the paste-ready text. §2.101 mentions it either way.

**Dry run** (placeholders for the word, time, head, ls-remote and file check):
- `dryrun_fold_output.txt`: the reverse splice is byte-identical to V4.100 (`35a20a1f…`).
- `dryrun_verify_output.txt`: the independent check finds four appends on the four typed hosts, each stating its fact. It finds three insertions at the declared places, and §2.100's heading, header and registers line, §2.99 and the V4.100 record unchanged. PASS.
- The check also fails as it should on V4.100 itself and on a copy with one silent edit.
- The dry-run ledger file was deleted.

**On the fold word:**
1. Read the note's record for its file, if Zenodo allows.
2. Run a live `git ls-remote`.
3. Run `python3 foldin_v4_101_deposit_followup.py --word "<word>" --when "<time>" --date "<date>" --head <estate head> --ls-remote "<UTC>" --main <sha> --file-check "<what was read>"`.
4. Run `python3 verify_v4_101_additive.py /home/claude/fold/SQT_Master_Ledger_v4_101_CANONICAL.md`.
5. Put V4.101 at the root in V4.100's place.
6. Write `FOLD_AUTHORIZATION_V4_101.md`.
7. Commit and push. If PR #43 is still open, the fold joins it; otherwise it goes on a new branch with its own pull request.

**Folded** on October 13, 2026, at 15:01 PDT, on the author's word of 15:00 PDT ("Fold"). The result is V4.101, md5 `4a67c760…` (1,926,632 B). The reverse splice is exact and the independent check passes. PR #43 had already been merged at 14:41 PDT, so the fold goes on `claude/ledger-v4-101-fold` with its own pull request. See `FOLD_AUTHORIZATION_V4_101.md`.
