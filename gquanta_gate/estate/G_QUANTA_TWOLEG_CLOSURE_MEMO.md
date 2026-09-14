# G-QUANTA — TWO-LEG CLOSURE MEMO

**Date:** September 10, 2026. **Base:** V4.81 `b4e55aaea76a2152f7b1873309aec077`. **Memo lock:** `0039d001769569297c2aa8ccbded5a3b` (4,863 B). **Elections (T3):** E-Q-1(b) standalone · E-Q-2(a) extended defects in scope. **Deviations:** D-Q-1 (D-T1, both legs), D-Q-2 (cosmetic), D-Q-3 (comparator post-emission), **D-Q-4 (return absent at first delivery — RESOLVED, below).**

## 1. Verification chain on the CC return (chat-side, bytes not prose)

1. **Retrieval.** GitHub REST API rate-limited (60/h, shared egress IP, 403). Pulled `gquanta_gate/G_QUANTA_CC_RETURN_INBAND.md` via raw.githubusercontent.com from **both** `claude/new-session-no3u27` and `refs/pull/14/head` — identical bytes; then a single-branch shallow clone for the commit audit — identical again. **md5 `83b37e740e5641c6fe37484783ad374b`, 65,139 B = declared.**
2. **Embeds.** Four sentinel blocks, re-extracted with the dispatch's own extractor rule, each byte-exact against its declared md5: instrument `4b1e700e3df9c1b5f51904fbf70ec219` (14,859 B) · checkpoint `ca0e69a75a521f3869726693b23e3dce` (3,335 B) · compare `e8890dc462e67aabd28e6425ae88f18d` (919 B) · two-leg comparison `525012b9107eb99ac402bc4df9e3044f` (37,514 B).
3. **Blindness ordering (git).** `7d41f24` (20:19) — pre-consultation checkpoint; message carries `ca0e69a7`; the checkpoint blob at that commit hashes `ca0e69a7`, byte-identical to the embedded one; `dispatch.md` at that commit = the staged dispatch `cd758b44`; **no chat-leg artifact in the tree.** `f59ed89` (20:19) — CC compare only. `948478e` (20:21) — first appearance of the decoded chat artifacts, the comparison, and the return. Order verified; H-CC-2 (truncated read at line 402 < first armor at 450) consistent with the tree.
4. **Comparator run of record (chat-side).** Frozen v1.0 `2be701be` + schema `05e53dbb` against chat `55861161` vs CC `ca0e69a7` (+ both compare files): **`C1-C6 ALL PASS` — 255 checks, 0 miss, S9 not triggered.**
5. **Comparator determinism.** The chat-side output is **byte-identical** to CC's own `g_quanta_twoleg_comparison.json` (`525012b9`, both).
6. **Independence witness.** Instrument md5s differ; checkpoints not byte-identical; CC instrument audited — dual-route (predicate + 16-entry literal lookup, per-row agreement asserted), no object→outcome mapping, the only object-name literal is the `Tower` token F-QUANTA-2 requires; timezone-aware `utc` (D-Q-2 does not recur).

## 2. Closed verdict (two-leg, identical on every verdict-bearing quantity)

| Object | Ledger ref | C1 | C2 | Verdict |
|---|---|---|---|---|
| L_B Borromean Baryon | §2.15/§2.51 | 1 | 1 | PASS |
| K₇ Vortex | §3.4 | 1 | 1 | PASS (independence witness, GP class) |
| Electron 2π Closure | §2.50.A | 1 | 1 | PASS |
| Clifford Unknot / Rule 17 | §2.41 | 0 | 1 | FAIL (charge only) |
| CD Tower Rungs 7/21/42/84/168 | §2.31/§2.75 | 0 | 0 | FAIL |
| Cluster M SLWE matrices | §2.58 | 0 | 0 | FAIL |

PC-1 met (3/3). PC-2 met (witness set {K₇ Vortex}). PC-3 met (6/6 concordant with H-Q-1..6). F-QUANTA-2 SILENT (real test: no tower rung carries continuous charge). F-QUANTA-1 SILENT **inert-by-inventory** (no `Single Exponent` row declared — reported as such, not as a pass). F-QUANTA-3 REGISTERED, NOT EXECUTED (no derived E_binding; scale separation, carried open).

## 3. Registers

- The **§2 discriminator** (continuous topological charge over a continuous configuration space ∧ Derrick-evading functional — competing dilation exponents or rigid constraint) as a general selection rule: **R3 → R2** — structural observation, machine-partitioned two-leg, concordant with every existing register, with a non-ropelength witness. Conditional on E-Q-2(a) (extended defects in scope) and on the §3 functional inventory as locked.
- The six per-object verdicts: R1-machine two-leg — but they are verdicts **on the encoded table**, i.e. on the framework's own declared config-space/invariant/functional entries; nothing here derives those entries.
- §2–§4 of the source memo (Derrick, Vakulenko–Kapitanskii, the residual-force hierarchy, scale-relative composites): R0 prior art, unchanged.
- §5 of the source memo (residual binding; the CM-1 constraint at §2.88.C): **untouched** — not in this gate.
- Non-claims: no observable, no bridge, no dimensionful constant (M.CW holds); no F-QUANTA-1 test performed; no claim that the tower rungs are physically empty — they are labels of sectors, not hosts of quanta, exactly as the memo stated; the Clifford-unknot verdict says only that the trivial knot carries no charge, not that Rule 17 is retired.

## 4. Fold plan (V4.82) — awaiting the author's word

- Prepend the V4.82 As-of summary + V4.82 fold-in record (September 10, 2026) above the V4.81 record.
- Insert **§2.91.P** (G-QUANTA) after §2.91.O, before `## J. Multi-Lens Reference…` (line ~1630 in V4.81): the discriminator, the locked inventory, the two-leg verdicts, PC-1/2/3, falsifier states, deviations D-Q-1..4, H-CC-1..4, CC-DD-1..8.
- One **Part V** row for the September 10 staging memo (stability and composite quanta; companion to the graded-base memo) with the discriminator's R2 promotion annotated in place, F-QUANTA-3 carried open, §5 residual-binding constraint stated.
- One **Part VI** row: G-QUANTA REGISTERED + LOCKED + EXECUTED, two-leg, C1–C6 ALL PASS, CLOSED.
- Title/As-of bump; one changelog line. Append-only; anchor-uniqueness asserted on every hunk; reverse-splice to byte identity against `b4e55aae`.
- Housekeeping named, not folded: standing-amendment P-5 (independence witness for every difference-forcing election) is again exercised here without a difference-forcing election — the C-Q-0 witness is the P-5 shape; the T1 list should travel in-band next gate (D-T1 twice in one gate is a pattern, not an exception).

## 5. Estate

| Artifact | md5 | Size |
|---|---|---|
| `staging_memo_G_QUANTA_v2.md` | `0039d001769569297c2aa8ccbded5a3b` | 4,863 B |
| `G_QUANTA_LOCK_RECORD.md` | `947768bd6d9652f5fdbeb43ceaf16502` | 5,312 B |
| `g_quanta_chatleg.py` | `79072196cdfc480f4073195d96100d2e` | 21,156 B |
| `g_quanta_chatleg_checkpoint.json` | `55861161748fca634534790f366380fd` | 4,605 B |
| `g_quanta_chatleg_compare.json` | `a5726e1efbc2feae46e43060df0250f5` | 1,333 B |
| `g_quanta_compare_v1_0.py` | `2be701be868259465525e29c79a4c621` | 11,960 B |
| `g_quanta_schema_v1_0.json` | `05e53dbb8e8e1f7669fa12b6fc55c260` | 1,615 B |
| `G_QUANTA_CC_DISPATCH_INBAND.md` | `cd758b4477b71c776e9379cc7e0908a8` | 68,964 B |
| `G_QUANTA_CHATLEG_EXECUTION_REPORT.md` | `4ecb40e37350da99eaa184c16000784f` | 4,803 B |
| `cc/G_QUANTA_CC_RETURN_INBAND.md` | `83b37e740e5641c6fe37484783ad374b` | 65,139 B |
| `cc/g_quanta_ccleg.py` | `4b1e700e3df9c1b5f51904fbf70ec219` | 14,859 B |
| `cc/g_quanta_ccleg_checkpoint.json` | `ca0e69a75a521f3869726693b23e3dce` | 3,335 B |
| `cc/g_quanta_ccleg_compare.json` | `e8890dc462e67aabd28e6425ae88f18d` | 919 B |
| `cc/g_quanta_twoleg_comparison.json` (CC) = `…_CHATSIDE_RUN.json` | `525012b9107eb99ac402bc4df9e3044f` | 37,514 B |

Repo: `gifgaf0/gifgaf0.github.io`, branch `claude/new-session-no3u27`, PR #14 (head = `948478e`). Chat-side estate not yet in the repo.
