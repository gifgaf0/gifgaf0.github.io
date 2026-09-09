# G-S2C1-W estate — provenance note (committed by the CC leg, September 9, 2026)

Committed under the Addendum 3 §4 housekeeping request (the chat leg holds no push
credentials), by the CC session that produced the checkpoint of record `6dde4ae6…`
(commit `4184c2ab`). Gate G-S2C1-W is **CLOSED two-leg, INERT, OOM-ROBUST**
(Addendum 3 §1); **V4.81 ACTIVE** `b4e55aaea76a2152f7b1873309aec077`
(fold record: `G_S2C1_W_LOCK_RECORD_ADDENDUM_3.md` in this directory).

Every file here was hash-verified before commit against its frozen declaration
(`ESTATE_MANIFEST.md5`; check with `md5sum -c ESTATE_MANIFEST.md5`).

## Quarantined artifacts travel INSIDE the dispatch (P-4.b honored post-closure)

`G_S2C1_W_CC_DISPATCH_INBAND.md` (md5 `7ca7e9e9…`, 115,183 B) is the canonical
package of record and carries, base64-armored, the three quarantined embeds that
are deliberately NOT committed as loose clear-text files:

| embed | md5 | bytes |
|---|---|---|
| `t1_forbidden_G_S2C1_W_A1.txt` (T1-A1) | `735eae308aa7baec19f23da5602a2d82` | 39 |
| `anchors_G_S2C1_W_SEALED.md` (sealed anchor file) | `8c7d59f64057e372d7b1ff760667a7c2` | 154 |
| `g_s2c1w_mapper_v6.py` (chat instrument v6.1, read of record) | `e034d4281c4a2906377e1587672cc128` | 26,458 |

All three (and every plain embed) are byte-recoverable with the committed
extractor: `python3 extract_embeds_G_S2C1_W.py` run beside the dispatch.
This mirrors the G-POLY1 Phase-3 pattern (extractor-as-only-reader) while
still placing the full frozen chain in-repo.

## Second delivery (September 9, 2026): three items supplied and verified

Added in the follow-up commit, each hash-verified against its declaration before
commit: `G_S2C1_W_LOCK_RECORD_ADDENDUM_2.md` (`7cdcf7e6…`, 7,558 B),
`H_W_6_reconciliation.json` (`1f8451e8…`, 1,550 B — the memo-letter per-arm
oom_robust recomputation, false on all four arms = the CC return),
`foldin_v4_81_gs2c1w.py` (`8de856d7…`, 19,702 B — not executable here: the V4.80
canonical is not in the repository; its reverse-splice was byte-verified twice
chat-side per Addendum 3 §3). The same delivery re-supplied Addendum 3, comparator
v1.1p, and the run-3 record — all byte-identical to the files already here — plus
the run-3 PREVIEW (`comparator_run3_v1_1p.json`), which the CC leg hashed to the
same `0b39d057…`: an independent confirmation of Addendum 3 §1's
"byte-identical to the preview" claim (one copy committed). The CC leg also
re-verified Addendum 2 §1's declaration of its own return manifest
(`c827f1d6…`, 327 B) against the committed `../RETURN_MANIFEST.md5`: exact.

## Estate items NOT in this commit (not present in the CC session; author to supply)

| artifact | declared md5 | bytes |
|---|---|---|
| `SQT_Master_Ledger_v4_81_CANONICAL.md` | `b4e55aaea76a2152f7b1873309aec077` | 1,529,485 |
| chat instrument v6 (pre-X-1) | `044fc22e…` (prefix as cited in the fold record) | — |
| comparator v1.1 | `f27a008f…` | — |
| `g_s2c1w_schema_v1_1.json` | `6c020e94…` (v1.1p in this directory needs it to run) | — |
| chat checkpoint read #1 (X-1, retained in lineage) | `3064fad78c492ee57689ba8232dc88c6` | — |
| chat checkpoint read #2 of record | `af7516c519048ad631f1a867f5f0822d` | 18,857 |
| comparator run records 1–2 (incl. the superseded text `722f0f1d…`) | — | — |
| closure log + closure-log Addendum 1 | `376bfad8…` / `510b9fe7…` | — |

The CC return of record (instrument, scanner, checkpoint `6dde4ae6…`, pre-read
suite results, CC report, return manifest) lives one directory up in
`gs2c1w_gate/` (commits `4184c2ab`, `208902e0`).
