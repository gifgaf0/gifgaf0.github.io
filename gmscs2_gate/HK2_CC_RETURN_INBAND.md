# HK-2 — CC RETURN (single file, in-band, to the author) — September 27, 2026

**Dispatch:** `HK2_GMSCS2_ESTATE_LANDING_DISPATCH_INBAND.md` v2 (September 27, 2026, 19:50 UTC; delivered file md5
`d09e615796e079ff2c2641c164642ea5`, 649,371 B; P-4 single-file in-band; P-4.c lone delivery). **Activation flag
present verbatim:** `ACTIVATE: HK2-GMSCS2-ESTATE-LANDING`. **Executed by the CC session** from `main` = `14bcf93`
on the session's designated branch `claude/new-session-txamk5`. This return is committed on the same branch, after
the estate commit, so it rides the same PR (the dispatch's first option).

## 1. The PR (number / URL / merge state at the time of writing)

| PR | Branch | Estate commit | State at writing |
|---|---|---|---|
| **#30** https://github.com/gifgaf0/gifgaf0.github.io/pull/30 | `claude/new-session-txamk5` | `1b15a0d` | OPEN, mergeable, awaiting the author's merge |

Title and estate-commit first line: `G-MSCS2 fold-side estate -> gmscs2_gate/estate/ (successor PR, per precedent)`;
the commit body carries the tarball md5 `d86b9ffde9a6cf53fe11dd5009472b24` and the seventeen file md5s. The PR adds
exactly the seventeen tarball files plus `CC_LANDING_VERIFICATION.md` under `gmscs2_gate/estate/`, and this return
at `gmscs2_gate/HK2_CC_RETURN_INBAND.md`; nothing else is touched. No canonical ledger and no dispatch file was
committed. The merged number and date are left to the V4.86 housekeeping bracket, with PR #27 / #28 / #29.

**`main` at the time of writing** (`git ls-remote origin refs/heads/main`, 20:24 UTC):
`14bcf93119883b9da509071cf904e8fe8972b8e2` — unchanged from the state of record and from landing (20:14 UTC).
On `main`: `gmscs1_gate/estate/` present, `gmscs2_gate/` present (no `estate/` before PR #30),
`SQT_Master_Ledger_v4_79_CANONICAL.md` not at the root.

## 2. Dispatch §2 results

1. **Extraction:** twenty-one `OK` lines (seventeen `estate/`, three `tools/t1/`, the armored tarball
   base64-decoded); every md5 and byte count as inventoried (see D-HK2-3 for the extractor used).
2. **Manifest:** `tar -xzf` → `estate/` (17 files); `md5sum -c ESTATE_MANIFEST.md5` → **16/16 OK**; `diff -r` of
   the tarball's tree against the loose copies → no output. The landed files are byte-exact (manifest 16/16
   re-run on the committed tree).
3. **Comparator v1.1 selftest** (comparator `96d76bc176caa2ffc18c5ea3aa635604`, schema v1.1
   `d270899c95a2b69c3adf818a69667490`): **19 suites (S1–S19) all PASS, `SELFTEST PASS`** — in the extracted
   `estate/` and again in the landed `gmscs2_gate/estate/`.
4. **Reproductions from the checkpoints of record on `main`** (chat `1c5b6b59829d2a6b9ae2b1a7a016832d`, CC
   `9961745d1e1857cfab6445d4754b5060`):
   - v1.1 → 356 checks, 356 PASS, 0 MISS; output md5 **`91841a49770c89fb78eed404032df402`** =
     `cc/g_mscs2_twoleg_comparison_v1_1_SUPPLEMENTARY.json` (byte-exact).
   - v1.0 (comparator `80d3b907`, schema `66f586d7`) → 356 checks, 340 PASS, 16 MISS (all cubic quadform
     null-tolerance rows at 1e-10); output md5 **`a91d84a5b5cbe24221aa2e6301c67675`** =
     `cc/g_mscs2_twoleg_comparison_CHATSIDE_RUN.json` = `gmscs2_gate/g_mscs2_twoleg_comparison.json` (byte-exact).
5. **Determinism witness (optional; re-checked):** `CHATSIDE_RERUN` `68569dac` vs `9961745d`: 2,003 leaves each;
   only `utc` and `extras.elapsed_seconds` differ; canonical md5 `71217c56859c923ce0b4fd0ee8a187cb` both;
   instrument `e58ba9a6`.
6. **V4.85 reverse-splice: V4.85 NOT SUPPLIED.** Only the HK-2 dispatch was delivered; no
   `SQT_Master_Ledger_v4_85_CANONICAL.md` (`d9c237a7`) and no V4.84 (`f36bbdb0`), so neither the reconstruction to
   V4.84 nor `verify_v4_85_additive.py` was run. Landed on steps 1–3, stated in the landing note.

## 3. T1 state

Every committed file (the seventeen estate files, `CC_LANDING_VERIFICATION.md`, this return), the two commit
messages and the PR body scan CLEAN under the G-MSCS2 gate list `be921b8c29f7578e85ed92f1450c1956` (36
patterns; numeric formatting collisions exactly as the dispatch expects — closure memo 2, fold script 8, delta
file 8, re-run checkpoint 6, re-run log 2; logged, not hits) and under the base list
`05302210cc4ceb70553acbe8379e9fc3` (11 patterns; 0 collisions). The dispatch plaintext (minus the two list
embeds and the armor body) scans CLEAN under both. D-HK2-2 reproduced exactly (below). One further transport
coincidence in the compressed tarball binary: D-HK2-4.

## 4. D-HK2 items (anything that did not go as written)

- **D-HK2-1 (from the dispatch; recorded):** the directive names `gmscs2_chatleg_estate.tar.gz`; the fold-side
  estate `gmscs2_foldside_estate.tar.gz` (`d86b9ffd`) is what was landed.
- **D-HK2-2 (from the dispatch; reproduced):** armor-body substring coincidences at gate-list indices
  0, 5, 6, 9, 10, 22 and base-list indices 0, 5, 6, 9, 10 — exactly as listed.
- **D-HK2-3 (new; CC-side):** the dispatch's shared extractor was not executed — this session's execution policy
  declined to run code lifted from the uploaded dispatch. An independently written extractor (same header
  grammar; md5 and length asserted; the `END-EMBED` marker additionally asserted after each payload) gave the
  same twenty-one `OK` lines. The one dispatched program executed, `g_mscs2_compare_v1_1.py`, was reviewed
  first-hand beforehand (it is the v1.0 comparator on `main` plus the schema constant, docstring/usage/label,
  suite S15's probe value and the new suite S19); the T1 scans used the byte-identical copies on `main`.
- **D-HK2-4 (new; CC-side):** the header's "the decoded tarball and every file inside it are CLEAN" does not hold
  for the compressed `.tar.gz` binary itself (`d86b9ffd`, not committed): `t1_scan.py` reports `HIT hits=[9]` under
  both lists — one two-character alphabetic substring coincidence inside the deflate data, the D-HK2-2 transport
  class. The gunzipped tar stream (`d3ed7b60f50b6ca60b592eaeecb874c7`, 491,520 B) and all seventeen files in it
  are CLEAN; no committed file is affected. Found by the CC session's independent verification pass.
- **Observation (no action):** `g_mscs2_compare_v1_1.py`'s docstring still says it compares against
  `g_mscs2_schema_v1_0.json`; the code loads and asserts the v1.1 schema `d270899c`. Landed verbatim.
- **Branch:** the designated branch `claude/new-session-txamk5` was absent from `git ls-remote` at session start;
  this push created it on the remote, based on `14bcf93`. The container's local remote-tracking ref for `main`
  was stale (`d0a0e31`) until fetched; every repository-state statement here and in the landing note is taken
  from `git ls-remote` or a fresh fetch, not from that stale ref.

Process note: after the estate was staged, four independent read-only verifiers re-checked it before the push
(byte integrity against the dispatch inventory and a fresh armor decode; the landing note's claims against the
dispatch and the repository; fresh reproductions of steps 2–5; T1 on every file). Their only substantive finding
was D-HK2-4; the landing note was corrected before the push.

No embeds: no verification check failed.
