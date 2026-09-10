# G-S2C1-W — LOCK RECORD ADDENDUM 3 (fold execution record; V4.81 ACTIVE)

**Date:** September 9, 2026. **Authorization:** `FOLD_AUTHORIZATION_V4_81.md` **`03fcd0d2ac55c2e12d9d52ef3fc18d6d`** (585 B; the directive verbatim). **Amends:** Addendum 2 `7cdcf7e6a170dde885a0a0ce8ac3a8ad` §3, §6, §8.

## 1. Re-pin executed (directive item 1; Addendum 2 §3)
CC identity anchor `97f26c04…` → **`6dde4ae6ffb944d94b138985cd7cf6cd`** (the return manifest of the canonical CC emission under dispatch `7ca7e9e9…`). Comparator v1.1p `55e6977e801e73df2b3d0b15fe17d7bf` is thereby the comparator of record; its run 3 re-executed formally: **105 items; 19 misses (15 representational + 4 definitional, disposed Addendum 2 §4, H-W-6 reconciled `1f8451e8…`); zero deviation on every verdict-bearing quantity; C-W-7 independence witness PASS on all four arms; `cc_file_md5 == pin`.** Record `comparator_run3_v1_1p_OF_RECORD.json` **`0b39d0570a27df4df846c9d40fe06849`** — byte-identical to the preview record delivered with Addendum 2. Closure per Addendum 2 §6 is now unconditional: **Gate G-S2C1-W CLOSED two-leg, INERT, OOM-ROBUST; W_∪′ = W_∪ = (0, 2.1213132100130068 m] banked alongside the suspended W_∪; no reinstatement.**

## 2. Fold executed (directive item 2)
Hash gate: the staged candidate in the workspace re-hashed to **`b4e55aaea76a2152f7b1873309aec077`** (1,529,485 B) — equal to the authorized hash; proceeded. Promotion: `SQT_Master_Ledger_v4_81_CANONICAL.md` is a byte-identical copy of the candidate (same md5, same size). No re-stage: the authorization hash `03fcd0d2` is recorded HERE rather than in the ledger text, because embedding it would have changed the authorized hash; the V4.82 changelog line may cite it.

## 3. Reverse-splice verified (directive item 3) — twice
(i) The staging script's own inverse (`foldin_v4_81_gs2c1w.py` `8de856d7…`): BYTE-IDENTICAL to V4.80 `a28e9b40616ee9b5798e9a5be027c1d9`. (ii) **An independent inverse built from the candidate alone** — the seven additions located by their own markers in the V4.81 text and removed (changelog line, Part VI row, G-POLY1 row annotation, §2.91.O bracket, the V4.81 record span, the V4.81 As-of span, the title): md5 **`a28e9b40616ee9b5798e9a5be027c1d9` — BYTE-IDENTICAL to V4.80, PASS.** §2.52 Open 3 row byte-identical and unique: PASS. Delta +15,341 B, additions only.

## 4. State after V4.81
- Canonical: **V4.81 `b4e55aae…`** (September 9, 2026). V4.80 `a28e9b40` retired, reconstructible byte-exact from V4.81 by the inverse of §3.
- G-S2C1-W: CLOSED (Part VI row; §2.91.O bracket; G-POLY1 window-row annotation). W_∪ REMAINS SUSPENDED; W_∪′ BANKED ALONGSIDE (E-W-7(a)). No observable, no bridge, no channel-speed claim, no μ_n, no reinstatement; §2.52 Open 3 untouched.
- Open at V4.81: **P-5** (independence witness for every difference-forcing election) PROPOSED — your election; **D-S2C1-1** (single-crystal G-S2C1 S9 formal run-2) still OUTSTANDING as at V4.80; **Q-W-1** recorded for your answer (a sealed-file revision would be a new gate cycle, not an edit).
- Housekeeping owed by the author (the chat leg cannot push to the repository or write project knowledge): upload `SQT_Master_Ledger_v4_81_CANONICAL.md` to project knowledge in place of V4.80; commit the G-S2C1-W estate (memo, lock record, Addenda 1–3, T1 base + A1, pinned inputs, sealed file, instrument v6/v6.1, comparators v1.0/v1.1/v1.1p + schemas, chat checkpoints read #1 X-1 / read #2, dispatch, reconciliation, run records, fold script, authorization) alongside CC's `gs2c1w_gate/` on `claude/new-session-q8iuz5` or a chat branch; the X-1 checkpoint `3064fad78c492ee57689ba8232dc88c6` is retained in lineage.

## 5. Artifacts of this addendum
| artifact | md5 | bytes |
|---|---|---|
| `SQT_Master_Ledger_v4_81_CANONICAL.md` | `b4e55aaea76a2152f7b1873309aec077` | 1,529,485 |
| `FOLD_AUTHORIZATION_V4_81.md` | `03fcd0d2ac55c2e12d9d52ef3fc18d6d` | 585 |
| `comparator_run3_v1_1p_OF_RECORD.json` | `0b39d0570a27df4df846c9d40fe06849` | 1,870 |
| `g_s2c1w_compare_v1_1p.py` (comparator of record) | `55e6977e801e73df2b3d0b15fe17d7bf` | 7,614 |
| `foldin_v4_81_gs2c1w.py` | `8de856d7591e42d9977e53e1f84699c1` | 19,702 |
