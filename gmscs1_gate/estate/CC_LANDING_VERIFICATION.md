# G-MSCS1 fold-side estate — CC landing verification (September 26, 2026)

Added at landing by the CC session (not part of the shipped tarball; `ESTATE_MANIFEST.md5` covers the
tarball's six files, all of which verified OK here — no self-entry, unlike the g2aa1 manifest, D-A1-2).
The estate was received from the author in the HK-1 dispatch (`HK1_GMSCS1_ESTATE_AND_V479_REMOVAL_DISPATCH_INBAND.md`,
P-4 single-file in-band, activation flag `ACTIVATE: HK1-GMSCS1-ESTATE-V479-REMOVAL` present verbatim in the
author's directive) as the base64-armored tarball `gmscs1_foldside_estate.tar.gz`
(md5 `027afc7494ec027331bb0727090e4b9e`, 37,577 B) together with the six loose `estate/` copies, the two T1
lists and the scanner; the loose copies are byte-identical to the tarball's tree (`diff -r` silent).
Per FOLD_LEDGER_2026-06-18 no canonical ledger is committed; the dispatch file itself is not committed either.

## What was received and its md5s

| File | md5 | Bytes |
|---|---|---|
| `ESTATE_MANIFEST.md5` | `108981889912ee63e018281f698eb426` | 392 |
| `FOLD_AUTHORIZATION_V4_83.md` | `76b4381485f24c0d8a3223a67416d7c0` | 1,467 |
| `G_MSCS1_TWOLEG_CLOSURE_MEMO.md` | `0825f1364d47f4a5cace1a05d702e19c` | 12,228 |
| `foldin_v4_83_gmscs1.py` | `9f798c35a14fc19d849efbdbc8bb6555` | 43,710 |
| `g_mscs1_compare_v1_1.py` | `54b329889418a10f4471b90704e0cbcd` | 19,261 |
| `g_mscs1_twoleg_comparison_CHATSIDE_RUN.json` | `d4a5b2713d32443cb7d6dec6c7a3c73f` | 69,284 |
| `twoleg_comparison_v1_1_candidate.json` | `948852fee4302da3ec2eb5e53b9c3758` | 68,084 |

All eleven embeds of the dispatch extracted with the shared extractor (`--decode-quarantined`, which here
only decodes the binary tarball): eleven `OK` lines, every md5 and byte count as inventoried.

## Checks run CC-side before this landing (dispatch §2)

1. **Estate manifest:** `tar -xzf` → `gmscs1_gate/estate/` (6 files); `md5sum -c ESTATE_MANIFEST.md5` → 6 × OK;
   `diff -r gmscs1_gate/estate ../estate` → no output.
2. **Comparator v1.1 selftest** (run inside the repository's `gmscs1_gate/`, against the frozen schema
   `g_mscs1_schema_v1_0.json` `76a42db3fd6ad82e485752bc2ddb24d5`): `ALL 17/17 SUITES GREEN (v1.1)
   (comparator 54b329889418a10f4471b90704e0cbcd, schema 76a42db3fd6ad82e485752bc2ddb24d5)`.
3. **Both comparison files reproduced byte-exactly from the checkpoints of record on `main`**
   (chat `c04c0b8e`, CC `249e11dd`, compare files `7b933c08` / `35d0f762`, comparator v1.0 `22432b29`,
   all md5-confirmed in `gmscs1_gate/`):
   - v1.1: 415 checks, 1 miss (`F-CTRL-ADMIX.r_xtal_h_projected`, chat 0.0 vs cc −1.967×10⁻³) →
     output md5 **`948852fee4302da3ec2eb5e53b9c3758`** = `twoleg_comparison_v1_1_candidate.json` (the
     supplementary run of record, FROZEN by the V4.83 S9 election (a)).
   - v1.0: 415 checks, 9 miss (the seven `halving_dev_kappa2` null rows plus the two ADMIX rows) →
     output md5 **`d4a5b2713d32443cb7d6dec6c7a3c73f`** = `g_mscs1_twoleg_comparison_CHATSIDE_RUN.json`
     = the CC run of record `gmscs1_gate/g_mscs1_twoleg_comparison.json` already on `main`.
4. **V4.83 fold verification: V4.83 NOT SUPPLIED.** The author's delivery for this session carried the HK-1
   dispatch and the G-MSCS2 dispatch only; no `SQT_Master_Ledger_v4_83_CANONICAL.md` (`40009ec0`) was
   provided alongside, so the reverse-splice to V4.82 (`d095a700`) was not run. Landing proceeds on steps
   1–3 as the dispatch instructs. (The V4.83 → V4.82 reconstruction remains verifiable from
   `foldin_v4_83_gmscs1.py`'s edit constants whenever the canonical is supplied; the V4.84 → V4.83
   reconstruction was verified at PR #26.)
5. **T1:** every estate file and this note scan CLEAN under the gate list `fef2827100d3f85e0a6341b44f0c00bf`
   (36 patterns; the two comparison JSONs log 6 numeric formatting collisions each under the contextual
   rule — 0 hits) and under the author's base list `05302210cc4ceb70553acbe8379e9fc3` (11 patterns; 0
   collisions, 0 hits). D-HK-1 (armor-body substring coincidences on the base64 transport) reproduced as
   recorded; the decoded tarball is CLEAN.

## Repository state at landing

`main` = `d0a0e31` (the PR #13 merge, September 22; PR #26 `e3df402` beneath it). `gmscs1_gate/estate/` is
absent from `main` at landing time. **`SQT_Master_Ledger_v4_79_CANONICAL.md` is still at the repository
root at landing** (md5 `6cfeca2248c3b89c4ff13ac5034f8a95`, 1,493,745 B, added by PR #13); its removal is
HK-1 Task B, an independent PR from the same `main`. Nothing else in the repository is touched by this PR.
