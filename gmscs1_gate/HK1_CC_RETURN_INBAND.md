# HK-1 — CC RETURN (single file, in-band, to the author) — September 26, 2026

**Dispatch:** `HK1_GMSCS1_ESTATE_AND_V479_REMOVAL_DISPATCH_INBAND.md` (P-4 single-file in-band; P-4.c lone delivery). **Activation flag received verbatim in the author's directive:** `ACTIVATE: HK1-GMSCS1-ESTATE-V479-REMOVAL`. **Executed by the CC session** on `main` = `d0a0e31` (the PR #13 merge), both tasks as separate PRs from that `main`, in the order Task A then Task B. Delivered in the same session as the G-MSCS2 CC leg (processed after HK-1, as directed); this return is committed on the G-MSCS2 working branch beside the gate directory, not in either HK-1 PR (the dispatch's commit rule for the two PRs).

## 1. The two PRs (numbers / URLs / merge state at the time of writing)

| Task | PR | Branch | Head | State at writing |
|---|---|---|---|---|
| A — `gmscs1_gate/estate/` landing | **#27** https://github.com/gifgaf0/gifgaf0.github.io/pull/27 | `claude/hk1-gmscs2-dispatch-e6vcfh-task-a` | `e3380c1` | OPEN, awaiting the author's merge |
| B — remove `SQT_Master_Ledger_v4_79_CANONICAL.md` | **#28** https://github.com/gifgaf0/gifgaf0.github.io/pull/28 | `claude/hk1-gmscs2-dispatch-e6vcfh-task-b` | `9f530f0` | OPEN, awaiting the author's merge |

`main` before either merge: `d0a0e31`. Neither PR was merged by the author before this return was written, so the "main head after each merge" field is left to the V4.85 housekeeping bracket (either merge order works; both branch from `d0a0e31` and touch disjoint paths).

Commit messages are as the dispatch prescribes (first lines: `G-MSCS1 fold-side estate -> gmscs1_gate/estate/ (successor PR, per precedent)` and `Remove SQT_Master_Ledger_v4_79_CANONICAL.md from the repository root (FOLD_LEDGER_2026-06-18; author election 2026-09-23)`); bodies carry the tarball md5 and the six file md5s (A) and the file's md5/size, its PR #13 entry, the policy sentence and "history retains the blob; nothing else changed" (B). PR #27 adds exactly the six tarball files plus `CC_LANDING_VERIFICATION.md` under `gmscs1_gate/estate/`; PR #28 is exactly one deletion (`git ls-tree` on `main` showed only `FOLD_LEDGER_2026-06-18.md` and the V4.79 file matching "ledger"; `git status` showed one `D`).

## 2. Dispatch §2 results

1. **Extraction:** eleven `OK` lines (seven `estate/`, three `tools/t1/`, the armored tarball decoded with `--decode-quarantined`); every md5 and byte count as inventoried; tarball `027afc7494ec027331bb0727090e4b9e` (37,577 B).
2. **Manifest:** `tar -xzf` → `gmscs1_gate/estate/` (6 files); `md5sum -c ESTATE_MANIFEST.md5` → **6/6 OK**; `diff -r gmscs1_gate/estate ../estate` → no output (loose copies byte-identical).
3. **Comparator v1.1 selftest** (in the repository's `gmscs1_gate/`, schema `76a42db3fd6ad82e485752bc2ddb24d5`): **`ALL 17/17 SUITES GREEN (v1.1)  (comparator 54b329889418a10f4471b90704e0cbcd, schema 76a42db3fd6ad82e485752bc2ddb24d5)`**.
4. **Reproductions from the checkpoints of record on `main`** (inputs md5-confirmed: chat `c04c0b8e`, CC `249e11dd`, compare files `7b933c08` / `35d0f762`, comparator v1.0 `22432b29`):
   - v1.1 → 415 checks, 1 miss (`F-CTRL-ADMIX.r_xtal_h_projected`, chat 0.0 vs cc −1.967×10⁻³); output md5 **`948852fee4302da3ec2eb5e53b9c3758`** = `twoleg_comparison_v1_1_candidate.json` (byte-exact).
   - v1.0 → 415 checks, 9 miss (the seven `halving_dev_kappa2` null rows + the two ADMIX rows); output md5 **`d4a5b2713d32443cb7d6dec6c7a3c73f`** = `g_mscs1_twoleg_comparison_CHATSIDE_RUN.json` = `gmscs1_gate/g_mscs1_twoleg_comparison.json` on `main` (byte-exact).
5. **V4.83 reverse-splice: V4.83 NOT SUPPLIED.** The delivery for this session carried the HK-1 dispatch and the G-MSCS2 dispatch only; no `SQT_Master_Ledger_v4_83_CANONICAL.md` (`40009ec0`) accompanied them, so the reconstruction to V4.82 (`d095a700`) was not run; landed on steps 1–3 as instructed, stated in the landing note.
6. **T1 state:** every estate file, the landing note and this return scan CLEAN under the gate list `fef2827100d3f85e0a6341b44f0c00bf` (36 patterns; the two comparison JSONs log 6 numeric formatting collisions each — 0 hits) and under the base list `05302210cc4ceb70553acbe8379e9fc3` (11 patterns; 0 collisions). D-HK-1 reproduced: the base64 armor body carries substring coincidences (gate indices 9, 10, 22; base indices 9, 10); the decoded tarball is CLEAN.

## 3. Deviations / D-HK items

- **D-HK-2 (branch naming):** this session's designated working branch is `claude/hk1-gmscs2-dispatch-e6vcfh` (the G-MSCS2 leg lives there). The two HK-1 PRs require two branches from `main`; they were created as `…-task-a` and `…-task-b` suffixes of the designated name rather than `claude/new-session-*` names. Content and process are as the dispatch prescribes.
- **D-HK-3 (V4.83 absent):** as §2 item 5; not a failure, a recorded "not supplied".
- Nothing else deviated from the dispatch as written. No canonical ledger and no dispatch file was committed; nothing outside `gmscs1_gate/estate/` (A) and the one deletion (B) is touched by the two PRs.

No embeds: no check failed.
