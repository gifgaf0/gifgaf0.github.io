# CC-side verification of the V4.82 fold (Gate G-QUANTA)

**Date:** September 14, 2026. **Leg:** cc. **Gate:** G-QUANTA (§2.91.P).
**Subject:** `SQT_Master_Ledger_v4_82_CANONICAL.md` md5 `d095a7003bb0d4c177e7451e1d14c4c6`, 1,552,643 B, as delivered chat-side.

## Why this record exists

The canonical ledger is not kept in this repository (`FOLD_LEDGER_2026-06-18.md`; restated in
`estate/ESTATE_NOTE.md`), so the folded V4.82 cannot be audited from the tree. This is the CC leg's
independent check that the delivered V4.82 is the V4.81 base plus exactly the seven edits the fold
script declares — performed **without ever holding V4.81**, whose bytes this leg has never received.

## Method

`verify_v482_reverse_splice.py` (beside this file) parses `estate/foldin_v4_82_gquanta.py` with `ast`
and evaluates only its edit-literal assignments. **The fold script is never executed** — it would
halt here anyway, since its `SRC` is the chat-side path `/mnt/project/SQT_Master_Ledger_v4_81_CANONICAL.md`.
The seven edits are then reversed against the delivered V4.82 by an independent reimplementation
(this file's own `str.replace` sequence, not the script's `reverse-splice` block), and the result is
hashed against the locked V4.81 md5. The three file-derived anchors (`ROW_VRH`, `ROW_S2C1W`,
`LINE_CH81`) are not needed in reverse: each inserted fragment is removed with its own leading
newline, which is anchor-independent.

## Result — PASS

```
extracted 13 edit literals from foldin_v4_82_gquanta.py (script not executed)
delivered V4.82: 1,552,643 B  md5 d095a7003bb0d4c177e7451e1d14c4c6
  OK   T_NEW present exactly once (count=1)
  OK   A_SUM present exactly once (count=1)
  OK   RECORD present exactly once (count=1)
  OK   SEC_P present exactly once (count=1)
  OK   ROW_V present exactly once (count=1)
  OK   ROW_VI present exactly once (count=1)
  OK   CH_NEW present exactly once (count=1)
  OK   T_OLD absent (count=0)
  OK   A_OLD absent (count=0)
  OK   §2.52 Open 3 row unique (count=1)

reverse-splice result: 1,529,485 B  md5 b4e55aaea76a2152f7b1873309aec077
locked V4.81:          1,529,485 B  md5 b4e55aaea76a2152f7b1873309aec077
REVERSE-SPLICE: BYTE-IDENTICAL TO V4.81 — PASS
delta V4.81 -> V4.82: +23,158 B
```

What this establishes, independently of the chat leg's own run:

1. The delivered V4.82 reconstructs the locked V4.81 (`b4e55aaea76a2152f7b1873309aec077`, 1,529,485 B)
   **byte-identically** once the seven edits are removed — so the fold's base really was the locked
   V4.81 and the fold is purely additive.
2. Each of the seven inserted fragments (E1 title, E2 As-of, E3 fold-in record, E4 §2.91.P,
   E5 Part V row, E6 Part VI row, E7 changelog) occurs **exactly once**; the two superseded
   fragments (V4.81 title, V4.81 As-of opener) are **absent**.
3. The `§2.52 Open 3` row is present and unique — the frozen-row guard holds in the delivered bytes,
   not only inside the fold script's own assertions.

## Reproducing

```
python3 gquanta_gate/verify_v482_reverse_splice.py \
    gquanta_gate/estate/foldin_v4_82_gquanta.py \
    /path/to/SQT_Master_Ledger_v4_82_CANONICAL.md
```
Exit 0 on PASS, 1 on any mismatch. The V4.82 ledger must be supplied out-of-band, by repo policy.

## Delivery chain checked

`estate/MANIFEST.md5` verifies in place (5/5 OK). The fold script arrived by two independent routes —
the tarball and a separate upload — and both copies hash `ff6fa734de9c6dbf35a2e0d84f5a2e56`. The
authorization is `7cc57e8cb4b72320aeac50b699625476` / 1,044 B, matching the `AUTH_MD5` / `AUTH_BYTES`
constants the fold script embeds in its own fold-in record. The dispatch re-delivered with the estate
hashes `cd758b4477b71c776e9379cc7e0908a8`, identical to `gquanta_gate/dispatch.md` already on `main`.

## D-T1 — still open, and not closable from this repository

The G-QUANTA T1 list (13 pattern lines, md5 prefix `04438b74`, cited as held in the G-2a-L1 estate)
was never supplied to either leg. The reason is narrower than "unavailable", and the chat leg's
sharpening of it is recorded here because it makes the remedy concrete:

**There is no G-2a-L1 gate directory in this repository at all.** Every occurrence of `04438b74` on
`main` — eleven of them — sits inside G-QUANTA's own paperwork (`G_QUANTA_LOCK_RECORD.md`,
`dispatch.md`, `g_quanta_ccleg.py`, its checkpoint, `return_header.md`, and the CC return), each one
citing a list nobody in this tree holds. The chat leg reports the list is cited by md5 in the V4.79
fold-in record; that record is in the canonical ledger, which this repository does not keep, so the
CC leg states it as the chat leg's finding rather than confirming it.

Every T1 list in the tree was hashed. None is `04438b74`:

| Path on `main` | md5 | Lines |
|---|---|---|
| `gci1_gate/embeds/t1_forbidden_G_CI1.txt` | `653a0b7447e68aa8a094e62337a24da3` | 84 |
| `gs2c1w_gate/estate/t1_forbidden_G_S2C1_W.txt` | `20ba1e7eab5a3bbffe510b4840edbc57` | 47 |
| `gs2c1_gate/t1_forbidden_G_S2_ON_CONE.txt` | `8cd89b9a82704accd89f7ff6f5e220b4` | 16 |
| `gs2c1_gate/p2_ccleg/t1_forbidden_G_S2_ON_CONE.txt` | `8cd89b9a82704accd89f7ff6f5e220b4` | 16 |

**Count correction (CC):** four lists, not five. A fifth 14-line candidate, `gpoly1_gate/t1_grep_log.txt`
(`079fa5ab43f6c95127e6b26be6991dd6`), is a scan **log**, not a forbidden-string list — a header, a
parenthetical note, a date, nine per-artifact hit lines, and an adjudications line. It cites no list
md5 at all, which corroborates rather than weakens the finding: G-POLY1 appears to have run without a
list too. The two archived tarballs on `main` were also opened and contain no T1 entries. The
conclusion is unchanged; only the tally is.

So `D-Q-1 / D-T1` was unavoidable on both legs rather than an oversight. The next-gate fix is
therefore specific, not aspirational: surface the 13-line list from the G-2a-L1 estate, **commit it
once to a shared location in this repository**, and embed it in the dispatch — rather than each gate
citing an md5 for a file no leg can reach.
