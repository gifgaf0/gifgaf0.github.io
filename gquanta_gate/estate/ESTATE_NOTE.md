# G-QUANTA — chat-side estate (for `gquanta_gate/estate/`)

**Gate:** G-QUANTA (§2.91.P). **Fold:** V4.82, September 14, 2026. **Base:** V4.81 `b4e55aaea76a2152f7b1873309aec077`.
**Layout precedent:** `gs2c1w_gate/estate/` (G-S2C1-W, the immediately prior gate) — chat-side estate as a subdirectory of the gate directory, carrying the fold script and the fold authorization.

## Files

| File | md5 | Size | What it is |
|---|---|---|---|
| `foldin_v4_82_gquanta.py` | `ff6fa734de9c6dbf35a2e0d84f5a2e56` | 29,119 B | The V4.82 fold: seven additive edits on V4.81, unique-anchor asserts, §2.52 Open 3 guard, byte-identical reverse-splice. Reads `/mnt/project/SQT_Master_Ledger_v4_81_CANONICAL.md`. |
| `FOLD_AUTHORIZATION_V4_82.md` | `7cc57e8cb4b72320aeac50b699625476` | 1,044 B | The author's fold directive, verbatim. |
| `G_QUANTA_TWOLEG_CLOSURE_MEMO.md` | `ccd53cb95981ea76f0471aea817779ed` | 7,259 B | The chat-side verification chain on the CC return, the closed verdict, registers, fold plan. |
| `G_QUANTA_CHATLEG_EXECUTION_REPORT.md` | `4ecb40e37350da99eaa184c16000784f` | 4,803 B | Chat-leg execution log, verdicts, PC states, deviations. |

## Already on `main` in `gquanta_gate/` — do not re-add

Verified byte-identical against the chat-side originals: `staging_memo_G_QUANTA_v2.md` `0039d001`, `G_QUANTA_LOCK_RECORD.md` `947768bd`, `g_quanta_chatleg.py` `79072196`, `g_quanta_chatleg_checkpoint.json` `55861161`, `g_quanta_chatleg_compare.json` `a5726e1e`, `g_quanta_compare_v1_0.py` `2be701be`, `g_quanta_schema_v1_0.json` `05e53dbb`, and the dispatch as `dispatch.md` `cd758b44`. The armor round-trip is therefore confirmed at rest, not only in transit.

## Deliberately NOT included

`SQT_Master_Ledger_v4_82_CANONICAL.md` (`d095a7003bb0d4c177e7451e1d14c4c6`, 1,552,643 B). `FOLD_LEDGER_2026-06-18.md` states the canonical ledger is not kept in this repository; V4.82 follows that policy. The fold script plus the V4.81 base md5 reproduce it exactly.

## Open

`D-T1` on both legs: no T1 forbidden-string list was supplied, so both checkpoints record `LIST_ABSENT`. The list (13 pattern lines, md5 prefix `04438b74`) should travel in-band in the next dispatch.
