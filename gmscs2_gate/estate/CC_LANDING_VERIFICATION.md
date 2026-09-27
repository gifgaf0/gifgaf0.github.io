# G-MSCS2 fold-side estate — CC landing verification (September 27, 2026)

Added at landing by the CC session (not part of the shipped tarball; `ESTATE_MANIFEST.md5` covers the
tarball's sixteen content files, all of which verified OK here — no self-entry, D-A1-2 hygiene).
The estate was received from the author in the HK-2 dispatch (`HK2_GMSCS2_ESTATE_LANDING_DISPATCH_INBAND.md`,
v2 of September 27, 2026, 19:50 UTC; delivered file md5 `d09e615796e079ff2c2641c164642ea5`, 649,371 B;
P-4 single-file in-band, P-4.c lone delivery; activation flag `ACTIVATE: HK2-GMSCS2-ESTATE-LANDING` present
verbatim) as the base64-armored tarball `gmscs2_foldside_estate.tar.gz`
(md5 `d86b9ffde9a6cf53fe11dd5009472b24`, 117,969 B) together with the seventeen loose `estate/` copies, the two
T1 lists and the scanner; the loose copies are byte-identical to the tarball's tree (`diff -r` silent).
Per FOLD_LEDGER_2026-06-18 no canonical ledger is committed; the dispatch file itself is not committed either.

## What was received and its md5s

| File | md5 | Bytes |
|---|---|---|
| `ESTATE_MANIFEST.md5` | `23d2dbf5ae617981a274bdcad7abd86a` | 1,112 |
| `FOLD_AUTHORIZATION_V4_85.md` | `7eb8d34407130010d624ded26c25b2fe` | 3,979 |
| `G_MSCS2_TWOLEG_CLOSURE_MEMO.md` | `e43a07329c931004ed8139b37cb14c98` | 26,906 |
| `G_MSCS2_CHATLEG_EXECUTION_REPORT.md` | `ae032ab9d585b842cfd57410e7380d08` | 16,045 |
| `G_MSCS2_PHASE0_EXECUTION_REPORT.md` | `b6a966920a34552e0f0e2dd91f2e969f` | 8,207 |
| `V4_85_HOUSEKEEPING_STAGING.md` | `7be337ff28a8db088f872f4d67507c30` | 7,450 |
| `ERRATUM_V4_85_H_MS2_8.md` | `196dbe30e9f5ab71169e7f90c61a62c8` | 5,320 |
| `foldin_v4_85_gmscs2.py` | `e1f55056a1c3aae72366591c9f7e0e14` | 88,027 |
| `V4_85_DELTA_ONLY.txt` | `a6393324a2f27e98a1ca3cba41183f1d` | 78,767 |
| `verify_v4_85_additive.py` | `cd5d62164b62dbeaef33320e07a2c261` | 3,366 |
| `g_mscs2_compare_v1_1.py` | `96d76bc176caa2ffc18c5ea3aa635604` | 18,133 |
| `g_mscs2_schema_v1_1_CANDIDATE.json` | `d270899c95a2b69c3adf818a69667490` | 6,820 |
| `cc/g_mscs2_twoleg_comparison_CHATSIDE_RUN.json` | `a91d84a5b5cbe24221aa2e6301c67675` | 65,679 |
| `cc/g_mscs2_twoleg_comparison_v1_1_SUPPLEMENTARY.json` | `91841a49770c89fb78eed404032df402` | 62,595 |
| `cc/determinism/README.md` | `4b1aa5f1eb23c37f7faf906329348df5` | 757 |
| `cc/determinism/g_mscs2_ccleg_checkpoint_CHATSIDE_RERUN.json` | `68569dac878b732385f177400ae306da` | 68,540 |
| `cc/determinism/run_ccleg_chatside.log` | `ebe479646620fa84e593df9919cc9418` | 7,046 |

Also received (not landed): `gmscs2_foldside_estate.tar.gz` `d86b9ffde9a6cf53fe11dd5009472b24` (117,969 B);
`tools/t1/T1_forbidden_G_MSCS2.txt` `be921b8c29f7578e85ed92f1450c1956` (1,695 B),
`tools/t1/T1_base_author_20260919.txt` `05302210cc4ceb70553acbe8379e9fc3` (143 B) and `tools/t1/t1_scan.py`
`6b86290090a8c84f1b1a0a99ec0bf697` (1,967 B) — the three T1 files byte-identical to `gmscs2_gate/tools/t1/` on `main`.

All twenty-one embeds of the dispatch extracted (seventeen `estate/`, three `tools/t1/`, the armored tarball
base64-decoded): twenty-one `OK` lines, every md5 and byte count as inventoried. The extraction was done with an
independently written CC-side extractor rather than the dispatch's shared one — see D-HK2-3.

## Checks run CC-side before this landing (dispatch §2)

1. **Estate manifest:** `tar -xzf gmscs2_foldside_estate.tar.gz` → `estate/` (17 files); `md5sum -c
   ESTATE_MANIFEST.md5` → 16 × OK; `diff -r` of the tarball's tree against the loose copies → no output. The
   seventeen files landed in `gmscs2_gate/estate/` are byte-exact copies of the tarball's tree (`diff -r`
   reports only this note as extra; manifest 16 × OK re-run in place).
2. **Comparator v1.1 selftest** (run inside `estate/`, against the frozen v1.1 schema
   `g_mscs2_schema_v1_1_CANDIDATE.json` `d270899c95a2b69c3adf818a69667490`, asserted by the comparator at load):
   19 suites (S1–S19), all `[PASS]`; `SELFTEST PASS` (comparator `96d76bc176caa2ffc18c5ea3aa635604`).
3. **Both comparison files reproduced byte-exactly from the checkpoints of record on `main`**
   (`gmscs2_gate/g_mscs2_chatleg_checkpoint.json` `1c5b6b59829d2a6b9ae2b1a7a016832d`,
   `gmscs2_gate/g_mscs2_ccleg_checkpoint.json` `9961745d1e1857cfab6445d4754b5060`, both md5-confirmed):
   - v1.1 (inside `estate/`): 356 checks, 356 PASS, 0 MISS → output md5 **`91841a49770c89fb78eed404032df402`**
     = `cc/g_mscs2_twoleg_comparison_v1_1_SUPPLEMENTARY.json` (byte-exact; the supplementary run of record,
     FROZEN by the V4.85 S9 election (a)).
   - v1.0 (inside `gmscs2_gate/`, comparator `80d3b9078788fb17f57945da7d9c2c96`, frozen schema
     `66f586d7b6c5e8228394222ddfda73f2`): 356 checks, 340 PASS, 16 MISS (the cubic quadform null rows at the
     v1.0 1e-10 tolerance) → output md5 **`a91d84a5b5cbe24221aa2e6301c67675`** =
     `cc/g_mscs2_twoleg_comparison_CHATSIDE_RUN.json` = `gmscs2_gate/g_mscs2_twoleg_comparison.json` on `main`
     (byte-exact, both).
   Both outputs were written outside the repository; the working tree was unchanged by the runs.
4. **Determinism witness (optional; re-checked):** `cc/determinism/g_mscs2_ccleg_checkpoint_CHATSIDE_RERUN.json`
   (`68569dac`) against the CC checkpoint of record `9961745d`: 2,003 leaves each, identical key sets; the only
   differing leaves are `utc` and `extras.elapsed_seconds`; canonical form (drop those two keys,
   `json.dumps(sort_keys=True, separators=(',', ':'))`, md5) **`71217c56859c923ce0b4fd0ee8a187cb`** for both;
   `instrument_md5` `e58ba9a6d52daa23f8264255b6dbbb75`.
5. **V4.85 fold verification: V4.85 NOT SUPPLIED.** The author's delivery for this session carried the HK-2
   dispatch only; no `SQT_Master_Ledger_v4_85_CANONICAL.md` (`d9c237a7`) and no V4.84 (`f36bbdb0`) accompanied
   it, so neither the reverse-splice to V4.84 nor `verify_v4_85_additive.py` was run. Landing proceeds on steps
   1–3 as the dispatch instructs (as PR #27 did for V4.83). The V4.85 → V4.84 reconstruction remains verifiable
   from `foldin_v4_85_gmscs2.py`'s edit literals whenever the canonical is supplied.
6. **T1:** every estate file and this note scan CLEAN under the G-MSCS2 gate list
   `be921b8c29f7578e85ed92f1450c1956` (36 patterns; numeric formatting collisions under the contextual rule,
   logged, not hits: the closure memo 2, the fold script 8, the delta file 8, the re-run checkpoint 6, the
   re-run log 2 — exactly the dispatch's expected counts) and under the author's base list
   `05302210cc4ceb70553acbe8379e9fc3` (11 patterns; 0 collisions, 0 hits). The dispatch plaintext (minus the two
   list embeds and the armor body) also scans CLEAN under both lists (its 26 gate-list collisions are the
   2 + 8 + 8 + 6 + 2 of the embedded estate files). The gunzipped tar stream of the tarball (md5
   `d3ed7b60f50b6ca60b592eaeecb874c7`, 491,520 B) scans CLEAN under both lists (26 / 0 collisions); the
   compressed `.tar.gz` binary itself does not — see D-HK2-4.

## D-HK2 items

- **D-HK2-1 (tarball name; recorded, not silently corrected — from the dispatch):** the author's directive names
  `gmscs2_chatleg_estate.tar.gz` (`c1b76d09…`), the pre-dispatch chat-leg estate, whose files are already on
  `main` under `gmscs2_gate/` (commit `d7fd5c7`, PR #29). The fold-side estate landed here is
  `gmscs2_foldside_estate.tar.gz` (`d86b9ffde9a6cf53fe11dd5009472b24`, 117,969 B), built after the V4.85 fold,
  per the PR #26 (g2aa1) and PR #27 (gmscs1) precedent.
- **D-HK2-2 (armor-transport collisions; the D-A1-1 / D-HK-1 class):** reproduced as recorded. Short alphabetic
  patterns occur as substring coincidences inside the tarball's base64 armor body — gate-list indices
  0, 5, 6, 9, 10, 22 and base-list indices 0, 5, 6, 9, 10 — exactly as the dispatch lists them. They are
  transport collisions, not text; the gunzipped tar stream and every file inside it scan CLEAN (for the
  compressed binary, see D-HK2-4).
- **D-HK2-3 (extractor; CC-side):** the dispatch's shared extractor was not executed — this session's execution
  policy declined to run code lifted from the uploaded dispatch file. The embeds were extracted with an
  independently written extractor applying the same header grammar (`name`, `md5`, `bytes`,
  `encoding=raw|base64`, `armor_bytes`): exactly `bytes` raw bytes, or `armor_bytes` of armor base64-decoded;
  md5 and length asserted; and, in addition, the matching `END-EMBED` marker asserted right after each payload
  (separating newlines allowed). The result is the dispatch's expected twenty-one `OK` lines. The one
  dispatched program executed, `g_mscs2_compare_v1_1.py`, was reviewed first-hand beforehand: it differs from
  the v1.0 comparator on `main` (`80d3b907`) only in its docstring and usage lines, the schema default and md5
  constant, the output label, suite S15's probe value, and the added suite S19. The dispatched T1 lists and
  `t1_scan.py` are byte-identical to `gmscs2_gate/tools/t1/` on `main`, and the scans were run with the `main`
  copy.
- **D-HK2-4 (the compressed tarball binary; CC-side):** the dispatch header states that "the decoded tarball and
  every file inside it are CLEAN". For the base64-decoded `.tar.gz` binary itself (`d86b9ffd`, not committed),
  `t1_scan.py` reports `HIT hits=[9]` under both the gate list and the base list: one two-character alphabetic
  pattern occurring once as a substring coincidence inside the deflate-compressed data — a transport collision of
  the D-HK2-2 class, not text. The gunzipped tar stream (`d3ed7b60`) and all seventeen files inside it scan
  CLEAN under both lists, so every committed file is unaffected; the dispatch's sentence holds for the tar stream
  and its files, not for the compressed binary. Recorded, not resolved.
- **Observation (no action; the file is landed verbatim):** `g_mscs2_compare_v1_1.py`'s module docstring still
  reads "Compares the chat-leg and CC-leg checkpoints against g_mscs2_schema_v1_0.json" (carried over from
  v1.0), while its code loads and asserts `g_mscs2_schema_v1_1_CANDIDATE.json` (`d270899c`). Behaviour is as
  the code says; the stale line is the author's to amend upstream if wanted.

## Repository state at landing

`git ls-remote origin refs/heads/main` (queried September 27, 2026, 20:14 UTC) →
`14bcf93119883b9da509071cf904e8fe8972b8e2` — the PR #29 merge (01:01:08 UTC), above PR #28 `3a41828` (01:00:29 UTC) and PR #27 `6774013`
(01:00:05 UTC), exactly the state of record in the dispatch. On `main`: `gmscs1_gate/estate/` is present
(PR #27), `gmscs2_gate/` is present (PR #29; no `estate/` beneath it before this PR), and
`SQT_Master_Ledger_v4_79_CANONICAL.md` is **not** at the repository root (PR #28); the only root file matching
"ledger" is `FOLD_LEDGER_2026-06-18.md`. This PR branches from that `main` and touches nothing outside
`gmscs2_gate/estate/` (the seventeen tarball files plus this note) and the CC return
`gmscs2_gate/HK2_CC_RETURN_INBAND.md`.
