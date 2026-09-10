# G_CI1_LOCK_RECORD_ADDENDUM_3.md — Addendum 3 to the G-CI1 lock record (append-only; base `a6adbb6a`, Addendum 1 `e5029ae8`, Addendum 2 `92672d5a` unmodified)

**Date:** August 19, 2026. **Scope:** the author's ratification of H-8, acknowledgment of H-9, confirmations of record, and the release authorization for the blind CC dispatch. Lock-record class (T1-exempt embed by the two-document convention).

## A3.1 — Author's directive (VERBATIM)
> **Directive: Ratify H-8, Acknowledge H-9, and Authorize CC Dispatch**
> The Phase 2 checkpoint (`ci1_phase2.json`) and the successful containment checks are confirmed.
> 1. I explicitly RATIFY the H-8 route ruling: the DIRECT principal-value quadrature is the I-3 quantity of record for C-CI-3. The Kramers-Kronig transform is diagnostic only.
> 2. I ACKNOWLEDGE the H-9 T1-hygiene re-serialization and the 11-digit float constraint.
> 3. The ray-bracket limits and x_S validities are confirmed as recorded.
> I authorize the P-4 CC dispatch.
> 1. Release `G_CI1_CC_DISPATCH_INBAND.md` to the blind CC leg.
> 2. CC must execute Phases 0–3 from scratch. CC Read #1 is the verdict read of record.
> 3. A-DIFF runs last.
> 4. Report back when the CC checkpoint is returned, placed in the workspace, and hashed. Do not run Chat Read #2 until I authorize it.

## A3.2 — Elections / rulings now T3-immutable
- **E-12 (H-8 ratified):** the I-3 quantity of record for C-CI-3 is the real part of the second-order mass operator by DIRECT principal-value quadrature over the intermediate wavevector, on shell, static value subtracted (Δ_ch := −[Re m̃_T(x) − Re m̃_T(0)]/2; c_cone/V_T0 = 1/(1 + Re m̃_T(0)/2)). The Kramers–Kronig transform of α is diagnostic only and is never compared at the 1e-6 tolerance.
- **H-9 acknowledged:** checkpoint floats serialized at a fixed 11 significant digits (all comparison tolerances ≥ 1e-8 relative) with an automatic T1 rescan; the Phase-2 production run was repeated from scratch under this rule.
- **Confirmed as recorded:** the ray-bracket limits Δ_geo^X (Addendum 2 §A2.2) and the validity edges x_S = 10 / 3.162 / 3.162 / 3.162 (hex:step / hex:gem8 / cubic:step / cubic:gem8), x_G = 10.

## A3.3 — Dispatch release
The released dispatch is `G_CI1_CC_DISPATCH_INBAND.md` rebuilt to embed this Addendum 3 (so the CC leg sees the H-8 ruling as ratified, not pending); the pre-release build `c80a03a1558e6943b38b869120201ad5` (104,549 B) is superseded by the released build whose md5 and byte count are recorded in `G_CI1_CC_DISPATCH_MANIFEST.json` and in the chat report of release. Every embed extracts back byte-exact (verified); the non-exempt body is T1-clean; the four declared T1-exempt embeds are the sealed file, the lock-record class (record + Addenda 1–3), the pin record (E-10), and the frozen T1 list itself (self-referential).

## A3.4 — Protocol in force until the CC return
- CC executes Phases 0–3 from scratch; CC Read #1 of the sealed file is the verdict read of record (E-9); A-DIFF runs last; CC reports checkpoints (`ci1_phase0_cc.json`, `ci1_phase1_cc.json`, `ci1_phase2_cc.json`, `ci1_phase3_cc.json`) with md5 + bytes and zero T1 hits.
- **Chat Read #2 is EMBARGOED** until the author's explicit authorization: the chat leg does not open the sealed file, does not run any Phase-3 mapper, and does not pre-compute any arm, before that word. The chat leg's pre-return work is limited to receiving and byte-hashing the returned CC artifacts and preparing the C-CI-1…3 comparison of Phases 1–2 (anchor-free).
- On return: X-1 byte-hash of each CC artifact into the workspace; C-CI-1 (Phase 1 R-a multisets, R-b table, F-IRR), C-CI-2 (containment values, Q^(d)/Q^(a) on the 33-point grid, ε_T, x_S; ≤ 1e-6 relative), C-CI-3 (direct-route scaled residual, D₂, plateau, Δ_geo^X; ≤ 1e-6 relative; VOID-NUM points compared as VOID); C-CI-4 waits for Chat Read #2 (interval-set equality 1e-6). Any miss → S9 (both legs re-derive from the pre-registration text; no leg copies the other).

## A3.5 — Standing
§2.52 Open 3 frozen; §2.87.J reserved; OP-2.58.2d and P-LEX-1 standing. Fold target (author-authorized only, after the comparison and Chat Read #2): §2.91.N + Part VI row + the W_∪ conditionality annotation on §2.91.M (V4.77-class).
