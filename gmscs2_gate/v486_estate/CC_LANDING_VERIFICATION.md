# V4.86 fold estate — CC landing verification (September 27, 2026)

Added at landing by the CC session (not part of the delivered estate; `ESTATE_MANIFEST.md5` covers the nine
content files, all of which verified OK here — no self-entry, D-A1-2 hygiene). The estate was received from the
author in the HK-3 dispatch (`HK3_V486_ESTATE_LANDING_DISPATCH_INBAND.md`, September 27, 2026, 22:37 UTC;
delivered file md5 `56ab70e083c849494163119993b45450`, 88,825 B; P-4 single-file in-band, P-4.c lone delivery;
activation flag `ACTIVATE: HK3-V486-ESTATE-LANDING` present verbatim) as thirteen raw-text embeds: the ten
`estate/` files, the two T1 lists and the scanner. There is no binary and no armor in this dispatch. Per
FOLD_LEDGER_2026-06-18 no canonical ledger is committed; the dispatch file itself is not committed either.
Namespace: `gmscs2_gate/v486_estate/`, as the dispatch directs (the directive's directory name, under the gate
whose cycle V4.86 closes); `gmscs2_gate/estate/` is untouched.

## What was received and its md5s

| File | md5 | Bytes |
|---|---|---|
| `ESTATE_MANIFEST.md5` | `f98a6b92623e52f6a2de3a4b7155b15d` | 561 |
| `FOLD_AUTHORIZATION_V4_86.md` | `23038bd8275229856dbe8c24f6936d62` | 4,890 |
| `FOLD_AUTHORIZATION_V4_86_ADDENDUM.md` | `2797c643decfb17131a226b988fc30ee` | 4,575 |
| `V4_86_HOUSEKEEPING_STAGING_2.md` | `b8ec73b8a0c39af96b3ebc88880b6217` | 8,131 |
| `foldin_v4_86_hk_closeout.py` | `2b394f2040661f096f64997f79f9d641` | 22,225 |
| `V4_86_DELTA_ONLY.txt` | `c463083460f230803077578facefbc95` | 15,364 |
| `verify_v4_86_additive.py` | `82ad3a7de8950fe20b6c643fe44377e1` | 3,362 |
| `verify_v4_86_additive.log` | `28d701fcf7aef064a4c8f1898520f3e7` | 907 |
| `v486_facts.json` | `1b9f81a9a749e5f85f8566d62b59978c` | 3,914 |
| `v486_check_and_facts.py` | `e977a5b2c42974bf0010dded0a878798` | 6,914 |

Also received (not landed): `tools/t1/T1_forbidden_G_MSCS2.txt` `be921b8c29f7578e85ed92f1450c1956` (1,695 B),
`tools/t1/T1_base_author_20260919.txt` `05302210cc4ceb70553acbe8379e9fc3` (143 B), `tools/t1/t1_scan.py`
`6b86290090a8c84f1b1a0a99ec0bf697` (1,967 B) — all three byte-identical to `gmscs2_gate/tools/t1/` on `main`.

**Extraction:** thirteen `OK` lines (ten `estate/`, three `tools/t1/`), every md5 and byte count as inventoried.
Extracted with the CC session's own implementation of the header grammar (the D-HK2-3 practice, which the
dispatch accepts): exactly `bytes` payload bytes, md5 and length asserted, the matching `END-EMBED` marker
asserted after each payload (separating newlines allowed). The dispatch's extractor was not run.

## Checks run CC-side before this landing (dispatch §2)

1. **Manifest:** `md5sum -c ESTATE_MANIFEST.md5` → **9 × OK** (in the extracted `estate/` and again in the landed
   `gmscs2_gate/v486_estate/`, whose ten files are byte-identical to the extracted ones — `diff -r` silent before
   this note was added).
2. **Consistency with `main` and with the fold record** (fresh fetch of `main` = `d92642e`; checked with the
   CC session's own code — 34 assertions, 34 PASS; the checker is kept CC-side, outside the repository, under the
   dispatch's commit rule, and every assertion it makes is listed below):
   - `FOLD_AUTHORIZATION_V4_86.md` md5 **`23038bd8275229856dbe8c24f6936d62`** = `v486_facts.json` `auth_md5`
     (and 4,890 B = `auth_bytes`).
   - The erratum on `main`: `git show origin/main:gmscs2_gate/estate/ERRATUM_V4_85_H_MS2_8.md | md5sum` =
     **`196dbe30e9f5ab71169e7f90c61a62c8`** = `erratum_md5`.
   - The four merge commits the V4.86 brackets fill are two-parent merges on `main` with the recorded committer
     times (committer offset −07:00, converted to UTC):

     | sha | Subject | Committer time (UTC) | Occurrences in `V4_86_DELTA_ONLY.txt` |
     |---|---|---|---|
     | `6774013` | Merge pull request #27 | 2026-09-27T01:00:05Z | 7 |
     | `3a41828` | Merge pull request #28 | 2026-09-27T01:00:29Z | 6 |
     | `14bcf93` | Merge pull request #29 | 2026-09-27T01:01:08Z | 9 (on 6 lines) |
     | `d92642e` | Merge pull request #30 | 2026-09-27T20:26:20Z | 9 (on 6 lines) |

   - The facts file against `main`: `hk2_merge` `d92642e` (= `main`'s head), `hk2_pr` `#30`, `hk2_utc`
     `2026-09-27 20:26:20` (= `d92642e`'s committer time), `hk2_head` `304a099` (= `d92642e`'s second parent),
     `landing_md5` **`de17a1da21e067f7a4dbf50004cbbd24`** and `landing_bytes` 10,941 (= `main`'s
     `gmscs2_gate/estate/CC_LANDING_VERIFICATION.md`), `hk2_return` citing `5573a447` (= `main`'s
     `gmscs2_gate/HK2_CC_RETURN_INBAND.md`, `5573a44705d7c7d2f7c9af1dc7fb9531`, 7,131 B),
     `observation.main` = the full `d92642e5df4468f53865c1c7963317e07eaf4bbb`, `merge_files` = exactly the
     nineteen paths changed by `14bcf93..d92642e`, and `main`'s `gmscs2_gate/estate/ESTATE_MANIFEST.md5` =
     `23d2dbf5ae617981a274bdcad7abd86a`.
3. **The fold itself: V4.85 and V4.86 canonicals NOT SUPPLIED.** The author's delivery for this step carried the
   HK-3 dispatch only; neither `SQT_Master_Ledger_v4_85_CANONICAL.md` (`d9c237a7`) nor
   `SQT_Master_Ledger_v4_86_CANONICAL.md` (`d4c42a53`) accompanied it, so neither `verify_v4_86_additive.py` nor
   the reverse-splice to V4.85 was run. Landed on steps 1–2 (as PR #27 and PR #30 did).
4. **Syntax checks only** (`ast.parse`; nothing executed): `foldin_v4_86_hk_closeout.py`,
   `verify_v4_86_additive.py`, `v486_check_and_facts.py` — all three parse.
5. **T1:** every estate file and this note scan CLEAN under the G-MSCS2 gate list
   `be921b8c29f7578e85ed92f1450c1956` (36 patterns) and under the author's base list
   `05302210cc4ceb70553acbe8379e9fc3` (11 patterns), with **0 numeric collisions** throughout (the `main` copy of
   the scanner and lists was used). The dispatch plaintext minus the two list embeds also scans CLEAN under both,
   0 collisions.

## The three scripts: path caveat (dispatch §2.4)

They are landed as the record of what was run chat-side, **not** as runnable tools in this repository:

- `foldin_v4_86_hk_closeout.py` reads `/home/claude/v486/SQT_Master_Ledger_v4_85_CANONICAL.md` and
  `/home/claude/v486/v486_facts.json` and writes the V4.86 canonical under `/home/claude/v486/` (with
  `--dry-run`: stand-in facts, and it writes then removes `/home/claude/v486/_dryrun_v4_86.md`).
- `verify_v4_86_additive.py` reads both canonicals under `/home/claude/v486/` (paths `A` / `B` on its line 8) and
  writes `/home/claude/v486/V4_86_DELTA_ONLY.txt` — a path hardcoded separately on its line 49, before the
  `ADDITIVE DIFF VERIFIED` print. A step-3 run therefore needs line 49 adjusted as well as `A` / `B`: with only
  `A` / `B` changed it stops at that write (or, where `/home/claude/v486/` exists, writes there).
- `v486_check_and_facts.py`, from a chat-side clone (`/home/claude/ccrepo`), runs `git ls-remote origin` and
  `git fetch origin --prune --depth=300` against the remote, first rewriting that clone's `remote.origin.fetch`
  refspec; it reads a chat-side estate path (`/home/claude/hk2/estate`) and writes
  `/home/claude/v486/v486_facts.json` on success, or `/home/claude/v486/last_lsremote.json` on its halt paths
  (exits 3 and 4).

None of the paths is inside the repository. Re-running any of them needs its paths adjusted first; only the
dispatch's step 3 (with the canonicals held outside the repository) is a sanctioned execution.

## D-HK3 items

- **D-HK3-1 (from the dispatch; chat-side):** the chat session cannot push to this repository — its git proxy
  answers "not in this session's authorized repository set" (a dry-run push, nothing written; September 27,
  22:35:56 UTC) — so the PR is landed by CC, the HK-1 / HK-2 route.
- **D-HK3-2 (from the dispatch; a filename):** the directive's `V4_86_HOUSEKEEPING_STAGING_2.md` is the second
  (post-fold) version of the V4.86 staging note, `b8ec73b8`, chat-side name `V4_86_HOUSEKEEPING_STAGING.md`; it
  is landed under the directive's name. The superseded first version (`fde76975`) is not landed.
- **D-HK3-3 (from the dispatch; two files beyond the directive's list):** `v486_facts.json` (the fold script's
  input) and `v486_check_and_facts.py` (the pre-fold check that wrote it), plus the estate manifest.
- **D-HK3-4 (CC-side observation; no action, the file is landed verbatim):** `V4_86_HOUSEKEEPING_STAGING_2.md` is
  the post-fold version — the HK-2 section records the PR #30 merge and ends "SLOT CLOSED", and the V4.86-bracket
  and repository-state headings are post-fold ("EXECUTED …", "updated 20:49 UTC") — but two headings were not
  updated: the title still reads "…19:55 UTC; one slot still open" and the HK-2 heading still reads
  "(OPEN SLOT)". The md5 is of record, so the headings are left as delivered.
- **D-HK3-5 (CC-side observations on the landed records; for the author; nothing edited).** An independent
  cross-check of the repository facts the estate states (180 facts against git and the records on `main`) found
  these, each confirmed first-hand:
  1. The V4.86 record's H-MS2-8 text lists "the closure memo `e43a0732` §1.8" among the carriers of the wrong
     01:07 UTC fold-time observation. The memo's §1 item 8 is a *correct* observation made September 26,
     20:22–20:39 UTC ("both still unmerged" — the first merge, `6774013`, came at 01:00:05 UTC on September 27),
     and the memo contains no "01:07".
  2. The staging note and the V4.86 record say PR #29's three remaining `gmscs2_gate/` files (`extract.py`,
     `build_return.py`, `g_mscs2_cc_hypothesis_compare.py`) are "as listed in the return"; only
     `g_mscs2_cc_hypothesis_compare.py` is named in `gmscs2_gate/G_MSCS2_CC_RETURN_INBAND.md` (all three are on
     `main`; 34 − 3 = 31 holds).
  3. The §2.91.Q bracket calls `027afc74` "the delivered manifest"; `027afc74` is the gmscs1 tarball's md5 — the
     manifest on `main` is `108981889912ee63e018281f698eb426` (the 6/6 claim itself holds).
  4. The V4.83-record bracket quotes V4.85 as "not contained at the V4.85 fold time"; V4.85's text reads "not
     contained in main at the V4.85 fold time".
  5. `v486_facts.json` carries `cc_items` and `fold_utc` "20:49 UTC", which `v486_check_and_facts.py` does not
     write (it writes no `cc_items`, and its `fold_utc` would be the check time, 20:28); its docstring names only
     `auth_md5` / `auth_bytes` as filled in later. The facts file is therefore the check's output plus later
     runbook additions, not its untouched output.
  6. `FOLD_AUTHORIZATION_V4_86.md`'s "merged and its ref not retained" for `claude/new-session-txamk5` is wrong —
     the addendum already corrects it, and `git ls-remote` agrees with the addendum.

## Repository state at landing

`git ls-remote origin refs/heads/main` (queried September 27, 2026, 22:42 UTC; re-queried 22:43 UTC, unchanged) →
`d92642e5df4468f53865c1c7963317e07eaf4bbb` — the PR #30 merge (20:26:20 UTC), exactly the state of record in the
dispatch. `gmscs2_gate/v486_estate/` is absent from `main` before this PR. This PR branches from that `main` and
touches nothing outside `gmscs2_gate/v486_estate/` (the ten estate files plus this note) and the CC return
`gmscs2_gate/HK3_CC_RETURN_INBAND.md`; nothing in `gmscs2_gate/estate/` is changed.
