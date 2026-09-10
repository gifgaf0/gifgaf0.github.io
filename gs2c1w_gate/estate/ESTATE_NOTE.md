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

## Third delivery (September 9, 2026): chat checkpoint + closure log; CC BACKSTOP RUN

Added, hash-verified against their declarations: **`g_s2c1w_phase3_chat.json`**
(`af7516c519048ad631f1a867f5f0822d`, 18,857 B — the chat read #2 of record) and
**`G_S2C1_W_CLOSURE_LOG.md`** (`376bfad8fef81932cf75f11a8dc3efd9`, 11,254 B).
The same delivery re-supplied the lock record, Addendum 1, pinned inputs, and the
T1 base list — all byte-identical to the files already here.

**Independent CC-side backstop of comparator run 3 (this session, September 9):**
with the chat checkpoint in hand, the CC leg re-executed `g_s2c1w_compare_v1_1p.py`
(the committed `55e6977e…` copy) on chat `af7516c5…` vs CC `6dde4ae6…` (the
committed checkpoint, pin-checked by the comparator itself). Output:
**byte-identical to `comparator_run3_v1_1p_OF_RECORD.json` (`0b39d057…`)**, exit 1
with the 19 disposed misses — the run-3 record is independently reproduced.
Caveat (disclosed): `g_s2c1w_schema_v1_1.json` (`6c020e94…`) is not yet in the
estate; the backstop ran with the frozen v1.0 schema (`dd014b8c…`, in this
directory) standing in, since the comparator consumes only fields both schemas
carry (tolerances, lock_keys, arms, disp_keys, F_L_dependent_fields) — the
byte-identical output certifies those consumed fields are effectively identical.
A second cross-check: the CC scanner's T1 scan of the chat checkpoint reports
0 hits / 17 logged, matching the checkpoint's own `t1_checkpoint_scan` exactly.

## Estate items NOT in this commit (not present in the CC session; author to supply)

| artifact | declared md5 | bytes |
|---|---|---|
| `SQT_Master_Ledger_v4_81_CANONICAL.md` | `b4e55aaea76a2152f7b1873309aec077` | 1,529,485 |
| chat instrument v6 (read #1, X-1) | `044fc22e31ca900ee0ad89a3db119cc8` | 25,819 |
| comparator v1.1 | `f27a008f…` | — |
| `g_s2c1w_schema_v1_1.json` | `6c020e94…` (see backstop caveat above) | — |
| chat checkpoint read #1 (X-1, retained in lineage) | `3064fad78c492ee57689ba8232dc88c6` | 1,603 |
| comparator run records 1–2 (incl. the superseded text `722f0f1d…`) | — | — |
| closure-log Addendum 1 | `510b9fe7…` | — |

The CC return of record (instrument, scanner, checkpoint `6dde4ae6…`, pre-read
suite results, CC report, return manifest) lives one directory up in
`gs2c1w_gate/` (commits `4184c2ab`, `208902e0`).
