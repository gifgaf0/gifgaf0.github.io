# HK-5 — CC landing verification (G-VS1 fold-side estate) — October 2, 2026

**Dispatch:** `dispatch_HK5.md`, delivered md5 `021b134d2749831bd1af243c620dd092` (414,479 B; P-4 single file, P-4.c lone delivery; saved outside the repository, not committed). **Activation flag received, verbatim, in the author's directive:** `ACTIVATE: HK5-GVS1-ESTATE-LANDING` (the dispatch arrived once without a directive; per its own clause the CC leg did not proceed until the flag was supplied). **Executed by the CC session** on its branch `claude/new-session-tf548k` from `c21a25f2a37fcb3e3064219d48db093d3556af41` (confirmed by `git rev-parse HEAD` and `origin/claude/new-session-tf548k` after a fetch, working tree clean; `origin/main` = `7460a78`, as the dispatch records).

## 1. Extraction and manifest (dispatch §2.1)

- The dispatch's extractor (saved outside the repository), run from the repository root: **23 `OK` lines**, every md5 and byte count asserted, every END-EMBED marker where expected, every file under `g_vs1_gate/estate/`.
- `md5sum -c ESTATE_MANIFEST.md5` in `g_vs1_gate/estate/`: **22/22 OK** (manifest `28fb85d22d70105e91d4b744ccb14bba`, 1,370 B, self-excluded).

## 2. T1 (dispatch §2.2)

Lists from the branch: gate list `324f577d20e2bfba3b594d96c4ca3ba7` (31 patterns), base `05302210cc4ceb70553acbe8379e9fc3` (11), scanner `6b86290090a8c84f1b1a0a99ec0bf697`. Every one of the twenty-three estate files under both lists: **CLEAN, hits = [], 0 collisions** (46 clean lines). This note, the return, the estate commit message and the PR body scanned under both lists before use: CLEAN. One CC-side item on commit messages is recorded under D-HK5-CC-1 below.

## 3. Landing checks (dispatch §2.3)

`python3 g_vs1_gate/estate/hk5_landing_checks.py` from the repository root on the branch, with the estate in the tree (read-only, as its code confirms: file reads, read-only git queries, the comparator and the scanner): **122 PASS, 0 FAIL, `HK-5 LANDING CHECKS: ALL PASS`.** Independently of the script, CC confirmed: `cmp` byte-identity of the estate's `g_vs1_twoleg_comparison.json` and `g_vs1_twoleg_comparison_preread.json` with CC's `g_vs1_twoleg_comparison_cc.json` / `_preread_cc.json` (D-HK5-1 holds); `ast.parse` on the five estate scripts (the four chat-side scripts and the checks script) all OK. The S9 reproduction inside the checks (comparator v1.1 on the projected checkpoints → 445/445, and on the projected pre-read pair → 71/71) ran here and passed.

## 4. The fold (dispatch §2.4) — not run, by design

V4.87 (`dc243cb4fd98f8c79e2a139f138eb6b0`, 1,757,725 B) and V4.88 (`66b0a634e3b087c85d4209f3e6bb6a28`, 1,768,607 B) are not in the repository and were not supplied. `foldin_v4_88_g_vs1.py` and `verify_v4_88_additive.py` were syntax-checked only. The reverse-splice (asserted in-script, chat-side) and the additive verification (log `88aed80860171b1ab815659277b757d3`) were **not reproduced by CC**; the V4.88 identity above is the chat side's statement, carried here as cited. Both scripts carry absolute chat-side paths (D-HK5-2).

## 5. Commits

- `26d75e2` — the estate (23 files), first line `G-VS1 fold estate -> g_vs1_gate/estate/ (V4.88; successor PR, per precedent)`; body: the twenty-two manifest entries, the manifest md5, the V4.88 identity and base, "canonical not committed".
- (this commit) — this landing note, `g_vs1_gate/estate/CC_LANDING_VERIFICATION.md` (not in the manifest; the HK-4 shape).
- (next) — the return `g_vs1_gate/HK5_CC_RETURN_INBAND.md`, committed after the PR is opened so that it cites the PR number (the D-HK4-9 practice).

Nothing under `g_vs1_gate/` outside `estate/` was added, edited or removed; no canonical ledger and no dispatch file committed.

## 6. D-HK5 items as observed, and CC-side items

- **D-HK5-1** confirmed first-hand (`cmp`, both files). **D-HK5-2** confirmed by reading lines 10–13 and 7–8 of the two scripts. **D-HK5-3**: the two fills are present in the delta and are checked by the landing script (PASS). **D-HK5-4**: not observable from here; the lock record is on the branch (`82b2ff9`) and the closure memo in this estate, as stated. **D-HK5-5**: the discarded first-run md5 `2e7aecaa` is not in the repository, as intended. **D-HK5-6**: this PR moves the branch head from `c21a25f` by fast-forward; no history rewritten.
- **D-HK5-CC-1 (commit-message trailer vs T1; self-caught before the estate commit).** The CC harness appends a `Claude-Session:` link to every commit message; the link's random path contains the two-letter base pattern at index 9 as a substring, so the scanner (non-numeric patterns are substring hits) reports every such message as a hit. The dispatch requires commit messages CLEAN, so the HK-5 commit messages (the estate commit, this note, the return) carry the `Co-Authored-By` line only, no session link. The five earlier G-VS1 commit messages (`82b2ff9`, `c44d731`, `f9b88d9`, `d3577eb`, `c21a25f`) do carry the link and scan as index-9 hits for that reason alone — the D-VS-3 / D-A1-1 class (a transport token, not text); they are history and are not rewritten.
- **D-HK5-CC-2 (order of the return).** The return is committed after the PR is opened so it can cite the PR number; dispatch §4 asks for the number and URL.
