# V4.96 — staged, awaiting the author's fold word

**Update: FOLDED** on the author's word "Fold it as V4.96 now." (October 7, 2026, 20:05 PDT). The result is md5 `120b076a613b7ef4074193c03df2cf0d`; see `FOLD_AUTHORIZATION_V4_96.md`. The text below is the staging note, kept as it was.

**Plain-language summary.** This fold would record the author's polycrystal-floor election (N = 50, "I select N = 50", October 7, 2026, 19:16 PDT) and its consequences in the ledger: a short §2.96 and ten pointers. It has been dry-run on V4.95 and passes its own reverse-splice check and the independent additivity check. It is not canonical until the author gives the fold word.

**What it adds** (dry run: +5,064 B):
- a short §2.96, after §2.95;
- ten pointers:
  - the floor row (ELECTED);
  - the lattice-spacing-bound row and §2.95;
  - §2.91.N and the G-CI1 row;
  - the G-S2C1-W row;
  - ANNEX-CDEF-1;
  - §2.92.E;
  - §2.91.M (G-POLY1) and the Part V VRH row (the polycrystal postulate);
- the record and the changelog line.

No new Part VI row: the election is recorded on the floor row itself.

**Dry run** (placeholders for the fold word, its time, the estate head and the ls-remote facts):
- `dryrun_fold_output.txt`: reverse splice byte-identical to V4.95 (3b6c11c3…), PASS.
- `dryrun_verify_output.txt`: 10 appends on the 10 expected lines, three insertion blocks at the declared places, §2.92.A and §2.52 Open 3 unchanged, PASS.
- The dry-run ledger file was deleted after checking.

**On the fold word:**
1. Run a live `git ls-remote`.
2. Run `python3 foldin_v4_96_floor_election.py --word "<word>" --when "<time>" --date "<date>" --head <estate head> --ls-remote "<UTC>" --main <sha>`.
3. Run `python3 verify_v4_96_additive.py /home/claude/fold/SQT_Master_Ledger_v4_96_CANONICAL.md`.
4. Write `FOLD_AUTHORIZATION_V4_96.md` quoting the election and the word verbatim.
5. Commit and push.
