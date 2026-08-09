# G-POLY1 PHASE 3 — CC LEG EXECUTION REPORT (E3-5(a) CC-BLIND-FIRST, read cc-1)

**Date:** August 9, 2026. **Base:** V4.75 CANONICAL md5 `0e923ab786c1e1a96eb0a3bcad3e616f` (1,416,574 B).
**Dispatch:** `G_POLY1_PHASE3_CC_DISPATCH_INBAND.md` (in-band, P-4 self-contained).
**Chain honored:** memo `e16a7890` (LOCKED) + P3-A1 `ba75b113` (`7f4b53ad`) + P3-A2 `ac87bc92` (`b1150c94`) + P3-A3 `257b81bf` (`6a7069b0`). Elections E3-1(a)/E3-2(a)/E3-3(a)/E3-4(a)/**E3-5(a)** in force, T3-immutable.
**Leg role:** CC is the BLIND LEG OF RECORD. This read (cc-1) ran FIRST; chat read #4 is gated on the checkpoint hashed below.

## 1. Verify-then-build

All **15 embeds** re-extracted from the dispatch under the declared extraction convention and md5-verified against the declared identities: **15/15 PASS** (extractor: `extract_embeds.py`; sealed anchor file `anchors_G_POLY1_SEALED.md` verified byte-intact at `a1d19dd98151cd7299af41fb14584c6f`, 2,470 B, by hash only).

**Transport note (recorded for the ledger):** the dispatch is in-band, so the sealed span is necessarily present in the document the CC orchestrator ingested. The binding discipline observed: the sealed embed was extracted and hash-verified as bytes only; the only *reading* of it (parse + evaluation) was the mapper's single md5-asserted open, after all pre-read gates passed. No anchor-derived number in this report or the checkpoint was produced outside the mapper. The dispatch carries no chat-side anchor-derived Phase-3 content (blindness clause verified: the only chat Phase-3 artifacts embedded are the reference instrument and records; no chat Phase-3 checkpoint or window values are present).

## 2. Instrument and pre-read gates

**Instrument:** `g_poly1_phase3_mapper_cc.py` — independent implementation (zero-shared-machinery; the chat v4 was consulted as reference only; its synthetic documents were transcribed as shared test-vector DATA per dispatch §2(a)). T1 wall: forbidden strings assembled at runtime; case-insensitive source self-grep PASS on every invocation. Structured exceptions with raise-time masking and pre-emission self-scan per P3-A3 §2; first-DIMENSIONLESS rule for CEIL primary / CEIL-FB / DLM-FB per P3-A3 §3.

**Independent design register (CC-DD-1..8, echoed in the checkpoint):** sign-guarded numeric lexer (identifier-embedded digit runs are not quantities); inverse-marked known units are DIMENSIONED, unknown unit tokens pass the dimensionless validator, bare percent is dimensionless; comparison-operator variants normalized row-wide, multiplication marks only inside criterion matching; CEIL primary = 80-char keyword-adjacent window, CEIL-FB = leading-keyword clause; DLM primary adjacency tokens = the frozen P3-A1 §2(b) list {ceiling, bound, margin, criterion}; VLD f_max+margin route = min(margin·λ_min, 0.3/k_max), tighter governs; superscript exponents NOT folded into numeric values; P1–P6 first-match-in-order with all additional matches recorded.

**Pre-read gates (all PASS before the read):** memo §7 C-SYN-ATT (closed form ≤1e-12; dressed root self-consistent ≤1e-12 at kd≈0.035; Born agreement ≤1e-6 at kd≈1e-3), C-SYN-BIR (per arm, ≤1e-12), C-MONO, C-UNIT; C-SYN-X four-class round-trip; symbolic ATT-REF variants P3/P4/P6 (+P5) with operator normalization; fallback-engaging synthetics (CEIL-FB/DLM-FB/VLD-default, loud flags); adversarial synthetics — shared set (abs-bars, dimensioned decoys) plus CC additions (identifier-digit guard, inverse units, percent, pipes) — and the forced-failure masking-path test end-to-end.

**CC-H-note (pre-read self-catch, zero sealed contact):** one stage-0 gate failure during instrument buildout — the dressed ATT root-finder initially capped far-out-of-envelope edges at the bracket instead of returning the Born closed form (the convention the shared C-SYN-X vector pins: a Born edge past kd=1 is returned as Born and voided by the envelope a fortiori). Caught by C-SYN-X in a NO-READ invocation; fixed; all gates re-run PASS. Consistent with the H-14 precedent (pre-read catches; no exposure; no re-lock required).

**Read accounting:** stage-0 invocations (no read): 2 (one failing gates, one passing). Stage-1 single read: **1** (the only opening of the sealed embed). Sealed md5 asserted at open: `a1d19dd98151cd7299af41fb14584c6f` (2,470 B) — identity confirmed.

## 3. Single-read result (cc-1)

**No X-1. No fallbacks engaged. Census: 4 rows → 1:ATT-REF, 2:CEIL, 3:DLM, 4:VLD.**
Refs: D_ref = 1.234271033e+24 m; k(f_ref) = 2.095845022e-06 /m. Inheritance: rows 2 and 3 inherit D_ref (reported); row 2 carries its own frequency (span `100 Hz`).

Per-row engaged readings (spans verbatim, post-normalization):

| row | class | engaged | span | reading | flags |
|---|---|---|---|---|---|
| A-1 | ATT-REF | **P5**, B = 1.0 | `ℓ_att(f_ref) >= D_ref` | expr ≥ D_ref/n ⇒ B = n (n absent ⇒ 1) | no other pattern matched |
| A-2 | CEIL | primary, B = 90.0 | `90%` | first-dimensionless in ceiling-window | OOM; inherits D_ref; own f (`100 Hz`); Caveat clause echoed in checkpoint |
| A-3 | DLM | primary, B = 3.19 | `3.19` | first quantity adjacent to frozen token `bound`, dimensionless-validated | OOM; inherits D_ref; Binding clause echoed |
| A-4 | VLD | f_max+margin route | margin span `10` | d_cap = min(margin·λ_min, 0.3/k_max) = 1.4314e4 m | governing clip: kd-envelope |

**Extraction readings flagged for author adjudication (C-P3-4 material, spans echoed loudly):**
- **A-2:** the mechanical first-dimensionless rule lands on the `90%` band-level token — the row's per-length ceiling value is DIMENSIONED (inverse length) and is skipped by the frozen rule; no pre-registered semantics convert a per-length bound times an inherited path into a dimensionless depth. Non-verdict-bearing here (CEIL is OOM-flagged, non-governing; its BIR channel is regime-voided), but the reading deserves an author ruling before any fold-level citation of the A-2 edge.
- **A-3:** B = 3.19 is the mantissa of a superscript-exponent quantity whose unit token is detached by the superscript run (CC-DD-7 declared). Regime-voided either way (see §4).
- **A-4:** margin read as 10 from a superscript-exponent token (`10` + superscript). Non-governing either way: the kd-envelope is tighter than the margin route under both readings.

## 4. Verdict (per-arm, gate, W_∪, OOM robustness)

Governing edge in every arm: **A-1** (ATT-REF, B = 1, at f_ref over D_ref; kd at edge ≈ 4e-6, deep inside the E3-3(a) envelope — no clipping engaged). Voided rows (reported, per arm): A-2-bir and A-3, both by the lock-record BIR-regime rule N_edge = (s₁/B)² ≥ 10 (N ≈ 3e-6…8e-3 ≪ 10). A-2-att (≈7.4–9.5 m) and the A-4 cap (1.43e4 m) are valid but not governing.

| arm | class | W_arm | governing | OOM ×10 relax |
|---|---|---|---|---|
| hex:step | **P-2** | (0, 2.121313e+00] m | A1 | class P-2, edge unchanged — **survives** |
| hex:gem8 | **P-2** | (0, 1.886679e+00] m | A1 | class P-2, edge unchanged — **survives** |
| cubic:step | **P-2** | (0, 1.838266e+00] m | A1 | class P-2, edge unchanged — **survives** |
| cubic:gem8 | **P-2** | (0, 1.644787e+00] m | A1 | class P-2, edge unchanged — **survives** |

**GATE VERDICT CLASS: P-2 (PASS-UNBOUNDED-BELOW; no lower-edge rows in the sealed set).**
**W_∪ = (0, 2.121313e+00] m.**
**OOM-robustness line:** every arm's class survives the uniform ×10 relaxation of all OOM rows (the governing A-1 edge is not OOM-flagged; relaxed CEIL/DLM rows remain non-governing/voided). Informational: a uniform ×(1/10) tightening also leaves A-1 governing in every arm.

**Checkpoint (sanctioned carrier, written + hashed BEFORE any other action):**
`poly1_phase3_cc.json` — md5 `2064bd7b4ed4f7b2b4e09bafdc0cf85a` (11,808 B).
Mapper source md5 at run: recorded inside the checkpoint (`mapper_source_md5`).

## 5. Advance notice for the C-P3 comparison (S9-relevant, pre-chat-read-4)

Predicted cross-leg divergences, from the CC design register vs the reference v4 source (the author may prefer to adjudicate these BEFORE spending chat read #4; the chat leg's blindness is already burned per H-16, and this leg's blind read is complete, so disclosure here costs nothing):

1. **C-P3-4 (DLM span):** v4's DLM primary uses invented adjacency tokens (`coefficients`, `set`) not on the frozen P3-A1 §2(b) list; on the sealed A-3 it will read B = 10 (bare mantissa near `coefficients`) where CC reads B = 3.19 (adjacent to the frozen token `bound`). Same OOM decade; both regime-voided; C-P3-1/2 unaffected, C-P3-4 will flag span/value.
2. **C-P3-1 (VLD cap):** v4 computes d_cap = 0.3/(k_max·margin) ≈ 1.431e3 m; CC computes min(margin·λ_min, 0.3/k_max) = 1.431e4 m. Neither governs; C-P3-1 will flag the non-governing edge.
3. **Defect warning (v4, CEIL stated-path):** v4's path regex has no identifier guard and its unit capture admits hyphens; on the sealed A-2 it will bind the catalog token's `-3` with the adjacent scale word as a stated path, giving a **negative** path length, hence a negative cube-root argument (complex in py3) and an uncaught TypeError at the envelope comparison — i.e., chat read #4 as-written likely **crashes mid-run rather than aborting X-1 cleanly**. This is exactly the H-17 class (values-blind synthetics missed an identifier-embedded digit decoy). Recommend a v4 patch + re-lock cycle before read #4; the CC instrument's CC-DD-1 guard covers the case (adversarial synthetic included).

## 6. Standing G_HS confirmation (dispatch §2(g))

**Instrument:** `g_poly1_hexghs_ccleg.py` — independent implementation from PIN Addenda 1+2 (both branches; tetragonal-primary; admissible-δ-family singular uppers with K⁺>0 guard; grid + golden-section refinement; cross-route asserts (2), (36)/(6), (37)+(39)/(43) vs (11)/(13) at ≤1e-9; tetragonal product identity asserted exact).

**Controls (5/5 PASS):** Co [76.5699, 76.8821] vs table [76.6, 77.0] (singular); Mg [17.2972, 17.3028] vs [17.3, 17.3] (singular); Graphite B [14.8469, 148.9163] vs [14.8, 148.9] (non-singular); TiO2 [110.0267, 116.9735] vs [110.0, 117.0] (non-singular); Sn [17.7020, 18.9348] vs [17.7, 19.0] (singular).

**Framework tensors (tetragonal-primary):**
- hex:step: μ_HS = [70.406527, 70.973589], v_T = [8.3909, 8.4246], half-width 0.20% (VR 1.54%, tightening ×7.7); hex(measured, guarded) [70.4039, 70.7578] with excluded K⁺<0 sliver 4.93e-05; hex(exact projection) [70.4103, 70.9773].
- hex:gem8: μ_HS = [99.818343, 101.058743], v_T = [9.9909, 10.0528], half-width 0.31% (VR 2.09%, tightening ×6.8); no sliver.

**CC checkpoint hashed BEFORE consulting the chat checkpoint:** `poly1_hexghs_cc.json` — md5 `96951e65df37700e30a8783aeb5dedfb` (3,785 B). T1 scan of checkpoint: 0 hits.

**Deviations vs the embedded chat checkpoint (`d74916a2`):** all δ-free quantities (lower bounds, non-singular uppers, VR moduli, K_PM, projections) agree to ≤4e-16 rel. Singular-case uppers agree to ≤4.0e-7 (controls) and ≤3.3e-8 (tensors); the residual is entirely the chat leg's 241-point grid quantization of δ* vs CC's golden-section refinement — the **mechanism check** (CC family evaluated at the chat δ*) reproduces the chat μ⁺ to 0.0e+00 rel on both tensors. CC refined uppers are marginally lower (validity direction preserved: still upper bounds, tighter). **No substantive deviation; the hex G_HS completion is CONFIRMED, tetragonal-primary, both branches.**

## 7. H-ledger parity

H-12 (read #1 exposure, X-1, zero values), H-13 (authorized R-B inspection, self-catches), H-14 (v2 defects, pre-read catches), H-15 (read #2 exposure, X-1), H-16 (chat quarantine breach; containment `d6e73451` → `b99fa804`; chat blindness burned), H-17 (CEIL-FB first-quantity deviation) — all stand as banked. CC leg adds: the §2 pre-read self-catch note (no sealed contact, no exposure, no re-lock triggered) and the §5 item-3 defect warning on the reference v4 (pre-read-4, values-derived, disclosed under the sanctioned-carrier rule). H-10/H-11 (G_HS) acknowledged as banked; CC G_HS run adds none.

## 8. Deliverables in this directory

| file | role |
|---|---|
| `extract_embeds.py` | verify-then-build extractor (15/15 PASS) |
| `g_poly1_phase3_mapper_cc.py` | CC Phase-3 mapper (independent; T1-clean source) |
| `poly1_phase3_cc.json` | **CC Phase-3 checkpoint** — md5 `2064bd7b4ed4f7b2b4e09bafdc0cf85a` — the gate for chat read #4 |
| `g_poly1_hexghs_ccleg.py` | CC G_HS instrument (independent; both branches) |
| `poly1_hexghs_cc.json` | CC G_HS checkpoint — md5 `96951e65df37700e30a8783aeb5dedfb` |
| `compare_ghs.py` | G_HS cross-leg comparison (run post-hash) |
| `MANIFEST.md5` | md5 manifest of this directory |

The sealed anchor file is **not** committed (θ discipline: its contents live only in the mapper run and the sanctioned carriers). Reproduction requires re-extracting the embeds from the dispatch (`extract_embeds.py` against the dispatch file) into `embeds/` beside the instruments.

**CC leg status: COMPLETE. Awaiting chat read #4 (gated on checkpoint `2064bd7b`) and the C-P3 comparison (C-P3-1/2/3 expected clean on classes, census, and the governing A-1 edge; C-P3-4 and the non-governing edges expected to flag per §5 — S9 adjudication material prepared above).**
