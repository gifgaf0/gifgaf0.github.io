# V4.100 — staged, awaiting the author's fold word

**Plain-language summary.** This fold would correct one fact in the ledger and record where the SLWE note stands.
- **The fact.** The ledger says decryption at the spec's noise never fails "for any q > 1032". In fact it fails at q = 1033, and never fails from q = 1036 on, so the first safe prime is 1039.
- **The change.** The fold adds a short §2.100 and five pointers.
- **Checks.** It has been dry-run on V4.99 and passes its own reverse-splice check and the independent additivity check.
- **Status.** It was drafted on your "Yes" (October 10, 2026, 19:43 PDT) to drafting the ledger entry. It is not canonical until you give the fold word.

**What it adds** (dry run: +5,416 B):
- **§2.100, after §2.99.** It covers:
  - the threshold, under four decoding rules and both roundings of q/2;
  - the q = 911 tail versus the failure rate;
  - the note's deposit on October 9 and its revision on October 10;
  - the hybrid KEM's notice.
- **Five pointers.**
  - Four sit on V4.94's "q > 1032" brackets: OP-2.58.5, the closure of §2.66.1, the OP-2.58.1.b row, and the OP-2.58.1a harness-port row.
  - One sits on the "Phase C draft awaiting the author" row, recording the deposit and the revision.
- **Bookkeeping.** The record, the title and As-of bump, and the changelog line.

No verdict, register or row status changes.

**Dry run** (with placeholders for the fold word, its time, the date, the estate head and the ls-remote facts):
- `dryrun_fold_output.txt`: the reverse splice is byte-identical to V4.99 (`a86fa090…`). PASS.
- `dryrun_verify_output.txt`: five appends on the five expected lines and three insertion blocks at the declared places. §2.94's heading and C1 paragraph, §2.97, §2.99 and the §2.52 Open 3 row are unchanged. PASS.
- The dry-run ledger file was deleted after checking.

**Before folding.** Merge the pull request that carries this staging first. Item 4 of §2.100 records the hybrid-KEM notice, which that pull request adds.

**On the fold word:**
1. Run a live `git ls-remote`.
2. Run `python3 foldin_v4_100_slwe_threshold.py --word "<word>" --when "<time>" --date "<date>" --head <estate head> --ls-remote "<UTC>" --main <sha>`.
3. Run `python3 verify_v4_100_additive.py /home/claude/fold/SQT_Master_Ledger_v4_100_CANONICAL.md`.
4. Put V4.100 at the repository root in V4.99's place, so the root holds one canonical. V4.99 stays in the history.
5. Write `FOLD_AUTHORIZATION_V4_100.md`, quoting the word verbatim.
6. Commit, push and open a pull request. Merge it with a merge commit.

## Addendum, October 13, 2026: extended with the deposits
**Plain-language summary.** The author asked at 14:20 PDT to fold V4.100 with two new deposits recorded, the gauge paper v6.4 and *Fluid Lattice Topology* with its notice. The staging was extended accordingly, then dry-run and checked again.
- **What was added.**
  - §2.100 is retitled "The SLWE Decryption Threshold, and Three Zenodo Deposits".
  - It gains items 5 (the gauge paper, doi:10.5281/zenodo.23351330) and 6 (*Fluid Lattice Topology*, doi:10.5281/zenodo.23351706).
  - Item 3 now says the note's revision is not yet on Zenodo.
  - Two pointers are added, on the gauge paper's §2.93.B1 entry and on the "Phase B drafts awaiting the author" row. The Phase C row's pointer now names the FLT notice.
- **Where the facts come from.** The deposit facts were read from the Zenodo record pages and DataCite on October 13.
- **The new dry run** (placeholders as before): +8,980 B and seven pointers. The reverse splice is byte-identical to V4.99. The independent check, updated for the seven lines, the new heading and the deposit facts, passes (`dryrun_oct13_fold_output.txt`, `dryrun_oct13_verify_output.txt`). The October 10 dry-run files are kept as they were.
