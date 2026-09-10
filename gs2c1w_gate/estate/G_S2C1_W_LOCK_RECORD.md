# G-S2C1-W — LOCK RECORD (staging memo lock; elections E-W-1..E-W-7; T1 freeze; pinned inputs)

**Date:** September 8, 2026. **Base:** `SQT_Master_Ledger_v4_80_CANONICAL.md` md5 `a28e9b40616ee9b5798e9a5be027c1d9` (1,514,144 B). **Gate:** G-S2C1-W, the W_∪′ re-derivation mini-gate (successor named at V4.80 PF-S2, §2.91.O). **Chat leg:** this instance. **Order of record:** register (memo) → lock (this record) → leg. No leg has run.

## 1. Author authorization (verbatim)

> **Directive: Lock G-S2C1-W Staging Memo and Proceed**
> The recovery of the Phase-3 machinery is confirmed. The staging memo (md5: 1ebb6a82fcb24e207b164a654eb94dd1) is approved.
> I explicitly AUTHORIZE the lock of the staging memo with the following elections:
> * E-W-1: (a) declared chain ξ = ℓ_P + G-C1 C-interval.
> * E-W-2: (a) Γ–K for the window, Γ–M for the FAIL-L robustness arm.
> * E-W-3: (a) each leg uses its own a₂; CI in comparator.
> * E-W-4: (i) author-supplied sealed file. Freeze T1 without D-W-2 merge.
> * E-W-5: (a) CC-BLIND-FIRST.
> * E-W-6: (a) Born a₂-only; dressed reported.
> * E-W-7: (a) W_∪′ banked alongside the suspended W_∪, no reinstatement.
> The defaults (D-W-1, D-W-4, D-W-5, D-W-6, D-W-7) are ratified.
> 1. Generate the lock record. 2. Freeze the T1 list and provide its hash. 3. Provide the `pinned_inputs_G_S2C1_W.json` so I can verify its contents before I provide the sealed anchor file.
> Do not write or execute the chat-side instrument until I provide the sealed anchors.

## 2. LOCKED — the staging memo

`staging_memo_G_S2C1_W.md` — md5 **`1ebb6a82fcb24e207b164a654eb94dd1`**, sha256 `b29db538886d21e6694c84d7f3a0272fae01294f992515f23656816f2bca9eff`, **32,219 B**, verified byte-identical at lock (September 8, 2026) to the approved draft delivered the same day. The file is never edited: its own header line ("Status: DRAFT — NOT LOCKED") stays as drafted and is superseded by this record — byte-identity is the ledger. Any change is a new draft with a new hash, staged under an addendum, never an edit under the old hash.

## 3. Elections — T3-immutable

| election | locked reading |
|---|---|
| E-W-1 | **(a)** declared chain: ξ = ℓ_P (G-SCALE1 reading (a)) + the G-C1 class-(b) interval C = ξ/a ∈ [0.0213, 0.0851] ⇒ a_phys = ℓ_P/C as an interval; window edge at a_phys.lo; FAIL-L only if it fires at a_phys.lo AND under the ×10 budget relaxation (EG-9); a_phys.hi serialized as the robustness arm |
| E-W-2 | **(a)** a₂^L = Γ–K for the window edge; Γ–M for the FAIL-L robustness arm — both serialized |
| E-W-3 | **(a)** each leg uses its own a₂ column; the comparator carries the 3.5% CI on every F_L-dependent quantity |
| E-W-4 | **(i)** the sealed anchor file `anchors_G_S2C1_W_SEALED.md` is AUTHOR-SUPPLIED; **T1 frozen WITHOUT the D-W-2 merge** (the G-S2C1 `8cd89b9a` and G-CI1 `653a0b74` lists are not part of this gate's T1 — D-W-2 disposed by election, disclosed permanently) |
| E-W-5 | **(a)** CC-BLIND-FIRST: the CC read is the verdict read of record for the CLASS; the chat read follows |
| E-W-6 | **(a)** edge of record = Born a₂-only; the a₄-dressed fixed-point edge REPORTED alongside; Δ₄ > 0.10 → DRESSING-SENSITIVE flag |
| E-W-7 | **(a)** W_∪′ is BANKED ALONGSIDE the suspended W_∪; NO reinstatement; INERT ≠ reinstatement; any PF-S2 reversal requires its own authorization |

**Defaults RATIFIED:** D-W-1 (a_phys interval ends), D-W-4 (silent sealed text ⇒ q = group for arrival-time-class rows, phase for coherence-class rows), D-W-5 (Δ₄ threshold 0.10), D-W-6 (band anchors evaluated at the upper band edge k₂; full sweep serialized), D-W-7 (contextual bare-numeric rule; formatting collisions logged, not fatal). Import delta under E-W-1(a): **zero** (every input previously declared).

## 4. FROZEN — the T1 forbidden-string list

`t1_forbidden_G_S2C1_W.txt` — md5 **`20ba1e7eab5a3bbffe510b4840edbc57`**, **1,560 B, 34 pattern lines** (pattern-lines-only convention, G-BKZ32 H-2; `#` lines are documentation, not patterns). Composition: **11** base patterns recovered byte-exact from `g_poly1_phase3_mapper_v5.py` `2c5ca7a4` (the seven FORBIDDEN, the two DECOYS retained as forbidden, the two `rb_mask` T1SUB tokens promoted to patterns); **21** identifier-class patterns for the S2-side dispersion / speed-offset anchor literature (names, symbols, units — **no numeric bounds**; the chat leg consulted no candidate anchor value in cutting them); **2** G-POLY1 sealed-reference strings (ledger-disclosed at V4.76; the G-POLY1 sealed file is not re-opened, so they may never appear in an instrument of this gate).

**T1 Addendum 1 (T1-A1) protocol:** at sealed delivery the author appends the anchor-specific identifiers and the bound / wavenumber / distance digit strings of the sealed file as `t1_forbidden_G_S2C1_W_A1.txt`, frozen with its own md5 declared in a lock-record addendum; every instrument scans base ∪ T1-A1. Justified scan exemptions (as at G-POLY1): the sealed file itself, the two list files.

**Scanner of record for this gate:** `t1_scan.py` md5 `ccd47ac5779c6592bb3c49d6890049e9` — implements the memo §6.4 D-W-7 rule (non-numeric patterns unconditional; a bare-numeric pattern is a HIT only when glued to a letter/underscore token; digit/sign/dot glue and exponent suffixes are LOGGED, not fatal); reports pattern indices, never echoes patterns. Independent CC re-implementation expected (disclosure-level rule only; no code transfer).

**Scan results at lock:** staging memo — 34 patterns, **0 hits, 0 logged**; `pinned_inputs_G_S2C1_W.json` — **0 hits, 1 logged** (H-W-1 below); this lock record — result appended at §9.

## 5. PINNED — the inputs file (author verification = pre-Phase-0 gate)

`pinned_inputs_G_S2C1_W.json` — md5 **`d1edc69b16dfd0b728a48cd8389b322b`**, **5,769 B**. Carries: provenance (ledger base, memo, T1, machinery commit `dd813646ed…`, the G-POLY1 blind-leg checkpoint `2064bd7b`); the arm map (by name, H-S2C-7 rule); a₂^L both legs both directions with the 3.5% CI and the a₄^L exclusion; the a₂^agg quartet (two-leg ≤ 3.4×10⁻¹³) and the a₄^agg diagnostic quartet; D(0); Q_T^a, the Q_T^d rule, s₁; the report-only tie-in; **the four G-POLY1 per-arm edges read programmatically from `2064bd7b`** (2.1213132100130068 / 1.8866794048346085 / 1.838266105289967 / 1.6447865351995365 m, all P-2, union upper 2.1213132100130068 m); the E-W-1(a) chain — ℓ_P = 1.616255×10⁻³⁵ m (CODATA 2018), C ∈ [0.0213, 0.0851], **a_phys ∈ [1.8992420681551118×10⁻³⁴, 7.588051643192489×10⁻³⁴] m**; the constants (KD_CLIP 0.3, N_MIN 10, Δ₄ threshold 0.10, fixed-point tol 10⁻¹⁵ / 200 iterations, c_q phase 1 / group 3, band rule k₂, OOM ×10 / ×0.1, comparator 10⁻⁶, pin 10⁻¹²); the locked elections; the ratified defaults; the exclusions. **It contains no anchor, no budget, no wavenumber, no comparison.**

**Verification gate:** the author's word on this file's contents is required before Phase 0. Any correction is a `v2` with a new md5 recorded in a lock-record addendum; the memo is untouched. The instrument's F-W-PIN gate asserts this file's md5 (or the v2 md5) before any sealed open.

## 6. Honesty ledger opened at lock

**H-W-0** (recovery, from the memo §1): 14 files, manifest 13/13, every ledger-cited hash matched; commit pinned; nothing modified or executed.

**H-W-1 (chat, self-caught at lock, pre-verdict, no artifact consumed):** on its first run the chat scanner counted digit-glue as identifier-glue for numeric patterns — stricter than the locked memo's D-W-7 text — and flagged the pinned-inputs file: the decimal rendering of the pinned chat a₂(Γ–M) = −1.9933×10⁻² (`-0.019933`) contains the digit run of one of the two mapper-v5 DECOY patterns retained in the frozen list. Disposition: (i) the T1 list is NOT re-cut (re-cutting a frozen list to dodge a collision is the reflex the discipline forbids); (ii) the scanner was corrected to the memo's rule — digit/sign/dot glue and exponent suffixes are formatting collisions, logged not fatal; (iii) the pinned value is a legitimate two-leg input, not a forbidden reference — the H-S2C-12 / H-CC-P2-2 numeric-collision class; (iv) the collision stands LOGGED on the JSON scan (1 logged, 0 hits). Both scanner versions' hashes are on the record (defective first cut superseded pre-use; `be054b9f` → `ccd47ac5`).

## 7. Pre-Phase-0 gates (all must be green before any read; each item halts the chain if missing)

1. Sealed anchor file `anchors_G_S2C1_W_SEALED.md` **author-supplied** (E-W-4(i)); md5 and census (row count + per-class census incl. the `disp` count) declared by lock-record addendum; field separator asserted absent from every anchor text (H-16 guard); constants bound by NAMED KEY only (G-CI1 S9 root cause (A)).
2. **T1-A1** appended by the author and frozen (md5 in the same addendum).
3. **Author verification word** on `pinned_inputs_G_S2C1_W.json` (or its v2).
4. Chat instrument (mapper v6 = v5 lineage + the `disp` kind + pinned-edge carry + F-W-PIN + comparison-last) written **only after items 1–3** per the directive; the nine v5 suites + C-SYN-D suite all green pre-read; T1 self-grep at every invocation.
5. Comparator + schema (C-W-1..6) FROZEN before either emission.
6. In-band CC dispatch `G_S2C1_W_CC_DISPATCH_INBAND.md` built: P-4 (activation flags embedded), P-4.b (sealed file and any quarantined embed base64-armored), **P-4.c (delivered ALONE; no loose file; the extractor is the only reader; any loose file at delivery is a logged deviation at the receiving leg)**; machinery referenced by commit SHA + `MANIFEST.md5` (verify-then-build), not re-embedded; every embed re-extraction-verified byte-exact before send.
7. **CC-BLIND-FIRST** read (E-W-5(a)); CC checkpoint hashed and returned to the chat workspace before the chat read (the re-lock-4 gate pattern).
8. Chat read; two-leg comparison C-W-1..6; S9 on any miss; fold only on separate authorization.

## 8. NOT authorized by this record

No instrument written; no execution; no read; no window; no comparison; no fold; no reinstatement; no §2.x / §3.x; no register change. The directive's standing instruction — **do not write or execute the chat-side instrument until the sealed anchors are provided** — is in force.

## 9. Delivery note and self-scan

Three lock artifacts (this record, the frozen T1 list, the pinned-inputs JSON) are delivered to the AUTHOR as separate hashed files alongside the already-delivered locked memo; this is a lock delivery to the author, not a leg dispatch — they will travel to the CC leg only inside the single in-band dispatch of gate 6 (P-4.c). Self-scan of this record against the frozen list: reported in the chat return with this record's md5 (the record cannot carry its own hash).
