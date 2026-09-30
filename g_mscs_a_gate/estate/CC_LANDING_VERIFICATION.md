# CC LANDING VERIFICATION — G-MSCS-A fold-side estate (HK-4) — September 30, 2026

**Executed by the CC session** on branch `claude/new-session-7flqwf`, from `13070d8` (confirmed by `git rev-parse HEAD` before extraction), under the verbatim activation flag `ACTIVATE: HK4-GMSCSA-ESTATE-LANDING`. Dispatch: `HK4_GMSCSA_ESTATE_LANDING_DISPATCH_INBAND.md`, delivered file md5 `01807b47f0a2ef6c374dab65dcc7391c` (697,380 B), saved outside the repository and not committed. Estate commit `37fb329`: exactly the fifteen files of dispatch §1 under `g_mscs_a_gate/estate/`; this note follows it as its own commit; the HK-4 return follows on the same branch. No canonical ledger, no dispatch file, and nothing under `g_mscs_a_gate/` outside `estate/` was added, edited or removed.

**Verdict line: HK-4 LANDING CHECKS: ALL PASS (121 PASS, 0 FAIL); extraction 15/15; manifest 14/14; T1 0 hits under the gate list, A1 and the base list.**

## 1. Extraction and manifest (dispatch §2.1)

- Extractor: the CC session's own (the D-HK2-3 practice) — the dispatch's regex, plus an assertion that the `END-EMBED` marker for the same name follows each payload immediately and that every name lies under `g_mscs_a_gate/estate/`. **Fifteen `OK` lines**, each md5 and byte count as inventoried in §1 of the dispatch; all `encoding=raw`; nothing quarantined; nothing decoded.
- `md5sum -c ESTATE_MANIFEST.md5` in the extracted directory: **14/14 OK** (the manifest is self-excluded; its own md5 `deba2ca6b3fb3c313fbf157f011964b5`, 826 B, as inventoried).
- The landed directory holds fifteen files and nothing else.

## 2. T1 (dispatch §2.2; lists from `main`, `g_mscs_a_gate/tools/t1/`)

Gate list `e274e58ea50b9ed347969e507d2a4f36` (36 patterns), A1 `3b753b3a371a162fc2ab21b9eed51bd5` (68), base `05302210cc4ceb70553acbe8379e9fc3` (11), scanner `6b86290090a8c84f1b1a0a99ec0bf697`. Every one of the fifteen estate files: **CLEAN, hits = [] under all three lists.** Formatting collisions exactly as the dispatch expects and nowhere else: `foldin_v4_87_g_mscs_a.py` 1 under the gate list and 1 under A1; `g_mscs_a_chatleg_checkpoint.json` 1 under the gate list; 0 under the base list on every file. This note, the return, the estate commit message, the further commit messages and the PR body were scanned CLEAN under the three lists before use.

## 3. Landing checks (dispatch §2.3)

`python3 g_mscs_a_gate/estate/hk4_landing_checks.py` from the repository root on the branch at `13070d8` + the extracted estate: **121 PASS lines, 0 FAIL, final line `HK-4 LANDING CHECKS: ALL PASS`.** Sections (a)–(g) all passed as the dispatch lists them: the manifest and every estate file at its md5 / byte count; the G-MSCS-A files on `main` and on the branch at the md5s the V4.87 record cites (the CC instrument `a5263388`, pre-read checkpoint `c9f8e4af`, checkpoint of record `d0e129fc`, return `1f4c66b9`, addendum `f364a802`, the decoded quarantine, the lock chain, the pinned sources); the nine cited commits with their subjects and `6755cf7` as the two-parent merge of PR #32 with second parent `1752296`; the delta's citation counts and the three honesty brackets word-for-word against the erratum; the four chat-side scripts parse; the T1 sweep.

- **2.3(c), the sealed-identity assertion, was run, not skipped:** the script decoded the armor on `main` into memory, asserted md5 `cfd62dcf…` / 177 B, and printed nothing but the PASS line. The CC session's policy did not object (it holds the same identity from its own Phase 3 read of record); no value of the sealed file was printed, logged, quoted or diffed anywhere in this landing.
- **Syntax checks (2.3(f)), redone by hand:** `ast.parse` OK on `foldin_v4_87_g_mscs_a.py`, `verify_v4_87_additive.py`, `s9_projection_v1_0.py`, `hk4_landing_checks.py` and, additionally, `sa_t1a1_build.py`. None of the fold-side scripts was executed.

**Beyond the dispatch (CC-side, read-only, in the session scratchpad; nothing committed from it):**
- The frozen comparator `c5b4a7aa` re-run on the landed chat checkpoint `4a933fdb` against the CC checkpoint of record `d0e129fc`: **1,477 checks, 1,428 pass, 49 misses — the rows byte-identical to the landed `g_mscs_a_twoleg_comparison.json`.** The 49 are exactly the 1 + 48 the CC return addendum 1 (`13070d8`) predicted before the chat read landed: the `rows[0]` key set and the four flags of the twelve NULL-INERT records.
- `s9_projection_v1_0.py` re-run on both checkpoints: the chat projection drops 3 row keys and nulls 96 NULL-INERT flags; **the CC projection changes nothing — the projected CC file is byte-identical to the checkpoint of record (md5 `d0e129fc…`), so the CC checkpoint already is the A-2.4 literal reading.** The comparator on the two projections: **2,225 checks, 2,225 pass, 0 misses — rows byte-identical to the landed `g_mscs_a_twoleg_comparison_s9.json`.**
- Gate blocks of the two checkpoints equal field for field (WINDOW-DELIVERED; ×10 and ×0.1 WINDOW-DELIVERED; OOM-robust; `sigma_union_hi` 1.235493174523598×10⁻⁶; `sigma_strict_hi` 6.582437027892329×10⁻⁷); every mapped cell's t\* agrees at 1×10⁻¹⁰ relative; the sealed identity (md5, bytes, row md5) identical.

## 4. The fold (dispatch §2.4) — NOT REPRODUCED HERE, by design

V4.86 (`d4c42a53cbd6d325ebc740879288e844`, 1,730,321 B) and V4.87 (`dc243cb4fd98f8c79e2a139f138eb6b0`, 1,757,725 B) are not in the repository and were not supplied. `foldin_v4_87_g_mscs_a.py` and `verify_v4_87_additive.py` were syntax-checked only. The reverse-splice (asserted in-script, chat-side) and the additive verification (`verify_v4_87_additive.log` `7e6a2d1c`: ADDITIVE DIFF VERIFIED, 7 changed lines, 6 added lines) are the chat side's results and were not reproduced by CC. What CC verified instead is what the landing checks cover: the delta's citations and bracket texts against the erratum, the authorization's citations, and the verifier log's verdict line.

## 5. D-HK4 items, as observed by CC

- **D-HK4-1 (name collision):** confirmed. `g_mscs_a_gate/run_read.log` is `5e2de03a6f887d3e4e14c3ab88309f1b` (the CC read, `620c421`); `g_mscs_a_gate/estate/run_read.log` is `fd109fa8937b81526541ddd3f5f07f90` (the chat read). Different directories, different files; both retained.
- **D-HK4-2 (absolute paths):** confirmed. `foldin_v4_87_g_mscs_a.py` lines 23–25 set `SRC`, `OUT`, `DELTA` under `/home/claude/v487/`; it writes `OUT` (line 159) and `DELTA` (line 189). `verify_v4_87_additive.py` lines 7–8 open `A` and `B` under the same directory and write nothing (it prints; no `open(..., 'w')` in the file). A future run must edit those lines. Same class as D-HK3-6.
- **D-HK4-3 (erratum revised before the fold):** confirmed on the landed text: the H-SA-4 κ₂₄ bracket names the cell as `cubic:step ⟨111⟩` with the one-sentence note on the bare-bar table split; md5 `13dc2e69` (5,499 B). No landed record cites the earlier working md5.
- **D-HK4-4 (branch reuse):** this PR moves `refs/heads/claude/new-session-7flqwf` from `13070d8` to the return commit — fast-forward, the D-HK3-7 situation. PR #32 (`6755cf7`) merged `1752296` only; `21b7d79`, `48fa2a3`, `620c421`, `13070d8` reach `main` with this PR.
- **D-HK4-5 (project store swap):** not observable from the repository; recorded as the chat side stated it.
- **D-HK4-6 (the sealed-identity assertion):** run as shipped; see §3.
- **D-HK4-7 (one file, two places; the A1 builder):** confirmed: `G_MSCS_A_TWOLEG_CLOSURE_MEMO.md` lands once, in `estate/`; `sa_t1a1_build.py` `dc7a747e` (4,367 B, the md5 the lock record §1 cites) was not on `main` before and lands here.

## 6. CC-side observations (nothing edited; for the author)

- **O-HK4-1:** the dispatch §2.3(b) cites the CC return addendum at md5 `f364a802` and the plaintext at `8a2844c6`, `build_return.py` at `49876268`; the landing checks confirmed all three against the branch, so the record's citations are the committed bytes.
- **O-HK4-2:** the `s9_projection_v1_0.py` result on the CC checkpoint (0 changes, md5 unchanged) is a fact the closure memo can state if it does not already: the S9 projection is a projection of the chat checkpoint only.
- **O-HK4-3:** the HK-4 dispatch's own extractor (§2.1) is single-purpose (`encoding=raw` only); the G-MSCS-A extractor committed as `g_mscs_a_gate/extract.py` would also have worked on it. The CC session used its own.

*Landing note written after the estate commit `37fb329`; scanned CLEAN under the gate list, A1 and the base list before commit.*
