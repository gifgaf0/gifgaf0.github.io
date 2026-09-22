# G-2a-A1 fold-side estate — CC landing verification (September 21, 2026)

Added at landing by the CC session (not part of the shipped tarball; `ESTATE_MANIFEST.md5` covers the
tarball's thirteen files, all of which verified OK here — the manifest's one self-entry is its own
placeholder hash). The estate was received from the author as `g2aa1_foldside_estate.tar.gz`
(md5 `96fb09ae48a85d58ccc1cc5ab603a064`) together with the loose closure memo, fold authorization,
fold script and the V4.84 canonical ledger; the loose copies are byte-identical to the tarball's.
Per FOLD_LEDGER_2026-06-18 the canonical ledger is **not** committed; it was held only to verify the fold.

## Checks run CC-side before this landing

1. **Estate manifest:** all thirteen files match `ESTATE_MANIFEST.md5`; the closure memo is
   `ccf5db3b0a06a394633d30e2a4531fb3` (23,349 B) as the authorization cites; the authorization is
   `c0b7bc461ffbe3e4d75b9c4ae9689fd1` (2,918 B) as the fold-in record cites; schema v1.1 r2
   `88a92fe2`, comparator v1.1 `7ce866cc`, supplementary run `5c8f6a35`, chat-side two-leg run
   `5942248e` (byte-identical to the CC run of record) — all as the closure memo states.
2. **V4.84 fold verification (without holding V4.83):** the received
   `SQT_Master_Ledger_v4_84_CANONICAL.md` (md5 `f36bbdb04104008783f2763f70fb916f`, 1,637,662 B)
   was reverse-spliced using the fold script's own reverse block (edit constants taken from
   `foldin_v4_84_g2aa1.py`; the two file-read anchors re-identified uniquely in V4.84): the
   reconstruction is **byte-identical to V4.83** — md5 `40009ec0197876b130766f1ae7494360`,
   1,589,553 B. All fourteen edit fragments (E1–E13, E8 as a/b) present exactly once; the
   §2.52 Open 3 row byte-identical pre/post.
3. **Comparator v1.1 selftest:** 22/22 suites PASS here (the 15 of v1.0 plus S16–S22).
4. **Supplementary run reproduced:** v1.1 on the two checkpoints of record (chat `8f657a23`,
   CC `bbf94221`) gives 436 / 436 / 0, output **byte-identical** to
   `cc/g_2a_a1_twoleg_comparison_v1_1_SUPPLEMENTARY.json` (`5c8f6a35`).
5. **Determinism witness re-verified:** the chat-side re-execution checkpoint (`9cc07211`) equals
   the CC checkpoint of record (`bbf94221`) in every leaf except `extras.elapsed_seconds`
   (3.88 → 2.57), confirmed by direct leaf diff; the timing-stripped canonical md5
   `42a65c26ae895022b1a349b520437b0a` reproduces on both (canonical form: `json.dumps` with
   `sort_keys=True`, separators `(",", ":")`, ASCII).
6. **T1:** every estate file and this note scan CLEAN against the gate list `2026b782` (24 patterns).

## Repository state at landing

`main` = `022fa3c` (PR #25, the G-2a-A1 CC leg `claude/new-session-j6430a`, merged — the fold-time
observation "not contained in main" is superseded). `gmscs1_gate/estate/` is still absent from
`main` at landing time; the E10/E11 housekeeping brackets' "recorded as observed" note therefore
still stands for that item. This estate lands by the successor PR from `claude/new-session-j6430a`
(restarted from the merged `main`), per the precedent.
