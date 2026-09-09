# G-S2C1-W — CLOSURE LOG (chat leg; two-leg comparison OUTSTANDING)

**Date:** September 8, 2026. **Base:** V4.80 `a28e9b40616ee9b5798e9a5be027c1d9`. **Gate:** G-S2C1-W, the W_∪′ re-derivation mini-gate (§2.91.O PF-S2 successor). **Status: CHAT LEG READ COMPLETE (post-exposure re-run); CC LEG EXECUTED EXTERNALLY (hash declared, file absent); TWO-LEG COMPARISON OUTSTANDING; NOT FOLD-READY.**

## 1. Lock chain of record
| artifact | md5 | bytes |
|---|---|---|
| staging memo (LOCKED) | `1ebb6a82fcb24e207b164a654eb94dd1` | 32,219 |
| lock record | `5f963ed8d7eff9f803da5c1eea2f841a` | 10,875 |
| lock record Addendum 1 | `125809174278cc7738692fd783d4ecd7` | 7,207 |
| T1 base (FROZEN) | `20ba1e7eab5a3bbffe510b4840edbc57` | 1,560 (34 patterns) |
| T1-A1 (FROZEN, author) | `735eae308aa7baec19f23da5602a2d82` | 39 (4 patterns; union 37) |
| pinned inputs (AUTHOR-VERIFIED) | `d1edc69b16dfd0b728a48cd8389b322b` | 5,769 |
| sealed anchor file (author-supplied) | `8c7d59f64057e372d7b1ff760667a7c2` | 154 (1 row, {disp: 1}, 8 fields) |
| comparator v1.0 (FROZEN pre-chat-emission) | `007688e5d8ea45d6848fd8e99c57a7d8` | 4,665 |
| schema v1.0 (FROZEN) | `dd014b8cc4c48e5dbf356e96baded753` | 1,382 |
| chat instrument v6 (read #1, X-1) | `044fc22e31ca900ee0ad89a3db119cc8` | 25,819 |
| chat instrument v6.1 (read #2, of record) | `e034d4281c4a2906377e1587672cc128` | 26,458 |
| chat checkpoint read #1 (X-1, masked) | `3064fad78c492ee57689ba8232dc88c6` | 1,603 |
| **chat checkpoint read #2 (of record)** | **`af7516c519048ad631f1a867f5f0822d`** | 18,857 |
| CC checkpoint (DECLARED by author; file ABSENT) | `97f26c04f982b1cc1694f4a47bdce882` | not declared |
| in-band CC dispatch (P-4/P-4.b/P-4.c; 13 embeds; re-extraction ALL OK) | `7ca7e9e9937d2f3c12f0521bce859e37` | 115,183 |
| T1 scanner of record | `ccd47ac5779c6592bb3c49d6890049e9` | 2,138 |
| G-POLY1 Phase-3 machinery | commit `dd813646ed…`, `MANIFEST.md5` 13/13 OK | — |

## 2. Read ledger
- **CC read #1 (external, E-W-5(a) CC-BLIND-FIRST):** executed before this package existed (D-W-9); checkpoint md5 declared `97f26c04f982b1cc1694f4a47bdce882`; **the verdict read of record for the CLASS** — its contents are not yet in the chat workspace (D-W-10).
- **Chat read #1 (v6 `044fc22e`): X-1, MASKED ABORT — H-W-4.** The masking self-scan (the instrument's own falsifier) fired on the multi-token T1-A1 patterns, which a token-level mask (the v5 lineage) cannot cover; the read aborted fail-closed before any anchor text reached the checkpoint or the transcript (checkpoint `3064fad78c492ee57689ba8232dc88c6` carries only the masked defect label `MASKING SELF-SCAN FAILED`). Contained; nothing consumed. Repair v6.1: two-pass masker (full-pattern pass longest-first, then token pass) + suite S13b asserting every multi-token pattern masks whole. All suites green before read #2.
- **Chat read #2 (v6.1 `e034d4281c4a2906377e1587672cc128`): the post-exposure re-run of record (H-W-2).** T1 self-grep 37 patterns PASS; F-W-PIN PASS (worst rel dev 0.0; G-POLY1 edges pinned byte-exact from `2064bd7b`); sealed md5 + census asserted at open; single read; per-arm records, union, and the pre-comparison record (md5 `7aa034398c7ab32c78b69a53a7f83980`) serialized BEFORE the comparison step; checkpoint T1 scan 0 hits / 17 logged numeric collisions (the parsed budget/wavenumber and their derived fields as JSON numbers — the H-S2C-12 class, expected and disclosed in Addendum 1 §3).

## 3. Chat-leg results (read #2; E-W-1(a) a_phys.lo, E-W-2(a) Γ–K, E-W-3(a) chat a₂ column, group quantity c_q = 3)
| arm | F_L (floor) | d_disp Born [m] | k·d | dressed [m] | Δ₄ | pinned G-POLY1 edge [m] | **W′ upper [m]** (governing) | class / OOM |
|---|---|---|---|---|---|---|---|---|
| `hex:step` | 1.02e-81 | 2.2242e+05 | 0.191 | 2.4338e+05 | 0.138 **DS** | 2.121313210013007 | **2.121313210013007** (GPOLY1-pinned) | P-2' / robust |
| `hex:gem8` | 1.02e-81 | 1.8709e+05 | 0.160 | 1.9834e+05 | 0.098 | 1.886679404834608 | **1.886679404834608** (GPOLY1-pinned) | P-2' / robust |
| `cubic:step` | 1.02e-81 | 1.7835e+05 | 0.153 | 1.8766e+05 | 0.087 | 1.838266105289967 | **1.838266105289967** (GPOLY1-pinned) | P-2' / robust |
| `cubic:gem8` | 1.02e-81 | 1.5118e+05 | 0.130 | 1.5657e+05 | 0.063 | 1.644786535199537 | **1.644786535199537** (GPOLY1-pinned) | P-2' / robust |

- **Lattice floor:** F_L ≈ 10⁻⁸¹ on every arm; robustness arms (hex:step) (Γ–K, a_phys.hi) 1.62e-80, (Γ–M, lo) 1.58e-81, (Γ–M, hi) 2.53e-80 — all with fail_L False. **FAIL-L did not fire on any configuration.** The registered M-naive expectation (memo §3.8) — VOID-TRIVIAL floor under the declared chain — is realized.
- **Grain-scale `disp` edges:** all inside the Born envelope (k·d 0.13–0.19 ≤ 0.3), all five orders of magnitude ABOVE the pinned G-POLY1 edges, hence **non-governing on every arm**. hex:step carries a DRESSING-SENSITIVE flag (Δ₄ = 0.138 > 0.10); its a₄-dressed edge is reported (the dressing widens, as a₄ > 0), the Born value stands as the edge of record (E-W-6(a)); both non-governing.
- **OOM:** budget ×10 → the `disp` edges leave the envelope (k·d 0.603 > 0.3, VOIDED — a VOID can only widen); budget ×0.1 → edges ~7×10⁴ m, still non-governing. Governing edge unchanged under both → **OOM-ROBUST** on every arm.
- **Union / intersection:** W_∪′ = (0, **2.121313210013007 m**] (arm `hex:step`); strict intersection upper 1.644786535199537 m (`cubic:gem8`), non-verdict.
- **Comparison (LAST, quarantined; the pinned W_∪ edge read here only):** W′_up / W_up = 1 → **class INERT, OOM-ROBUST**; F-W-MONO not triggered; per-arm classes all P-2′; **reinstatement: NONE (E-W-7(a): banked alongside the suspended W_union)**.

## 4. Chat-leg verdict statement (single-leg, post-exposure — NOT the read of record for the class)
**INERT, OOM-ROBUST: with the S2 channel's measured O(k²) dispersion at both scales made into constraint curves, the single sealed dispersion budget is non-binding on the domain scale by five orders of magnitude, and W_∪′ = W_∪ = (0, 2.1213132100130068 m] — unchanged, still SUSPENDED, banked alongside per E-W-7(a). The lattice-scale floor under the declared chain (ξ = ℓ_P, C-interval) is trivially satisfied (~10⁻⁸¹ of the budget). Nothing reinstated; nothing promoted.**

## 5. Two-leg status — OUTSTANDING (D-W-10)
Frozen comparator run 1 (`comparator_run1` record): `status OUTSTANDING — CC checkpoint file ABSENT; a hash cannot be compared to values; C-W-1..6 not executed` (exit 3). The declared CC md5 `97f26c04f982b1cc1694f4a47bdce882` is recorded as the identity anchor. Repository recovery attempted: branch listing obtained once (one branch not on the ledger, `claude/new-session-17ziy6` @ 4183f55, is a candidate for the external CC leg); tree listings for that branch and the two G-S2C1 CC branches were blocked by the shared unauthenticated API quota; raw-path probes for conventional names missed. **To close:** return the CC checkpoint FILE (with its name, byte size, branch, commit) to the chat workspace; hash it against the declared md5; then (a) if it conforms to schema v1.0 → run the frozen comparator `007688e5` as-is; (b) if it does not (expected in part, since CC ran before the schema existed — D-W-9) → representational S9, resolved by CC re-emission under the dispatch `7ca7e9e9937d2f3c12f0521bce859e37` (path-(a) pattern), the frozen comparator never edited. Chat-side C-W-3 expectation for the CC file: `sealed_md5 = 8c7d59f6…`, census 1/{disp: 1}; a differing sealed md5 means a differing serialization, resolved by byte comparison.

## 6. Honesty ledger and deviations (complete; nothing silent)
- **H-W-0** recovery: 14 files, manifest 13/13, ledger hashes matched, commit pinned, nothing modified.
- **H-W-1** (lock): first scanner cut over-counted digit-glue; corrected to D-W-7; the pinned a₂(Γ–M, chat) decimal rendering collides with a retained mapper-v5 decoy — logged, list not re-cut.
- **H-W-2** (delivery): chat blindness on the `disp` set burned — the sealed row arrived in the clear in the directive body; the chat read is a post-exposure re-run; the CC read is the read of record for the class.
- **H-W-3** (instrument development, pre-read, self-caught on first run): suites S6/S7 synthetics mis-sized (a floor below its budget; a dressed root sought beyond the a₄ turnover) — the tests, not the code; corrected before any read; the no-root branch itself is exercised by S7 as designed.
- **H-W-4** (chat read #1): token-level masker vs multi-token T1-A1 patterns — the masking self-scan fired, masked abort, read #1 spent as X-1, contained; v6.1 two-pass masker + S13b.
- **D-W-0..D-W-6** as in the memo §9 (blindness on the G-POLY1 set ledger-burned; lost chat estate pinned from V4.80 + `2064bd7b`; D-W-2 disposed by E-W-4 — frozen without merge; lattice CI; new kind suites; inherited imports; environment).
- **D-W-8** P-4.b not performed on the author→chat delivery. **D-W-9** CC executed before dispatch/comparator existed; comparator frozen pre-chat-emission only; dispatch built after the fact as the canonical package (v6.1 of record embedded). **D-W-10** CC checkpoint absent; comparison OUTSTANDING.
- **Q-W-1** (R-B observation, post-read, not acted on): the sealed row's stated wavenumber corresponds to a wavelength of ~7.3×10⁶ m (radiation at ~41 cycles per second), whereas a binary system with an orbital period of several hours radiates at a wavenumber of order 10⁻¹² /m — some six orders lower; and the caveat binds an orbital-decay agreement to a carrier group-speed offset, which is a dialect reading rather than a direct dispersion measurement. Under the sealed-text-dispositive rule the instrument reads what is sealed; the verdict would be INERT at the lower wavenumber a fortiori (the `disp` edge scales as 1/k and would move UP by six orders). Recorded for the author; any revision is a new sealed md5 + a new addendum, never an instrument-side correction.
- **T1-A1 note:** one A1 line duplicates a base pattern (harmless).

## 7. Registers and what is NOT claimed
Every chat number R1-machine **single-leg** (two-leg pending §5). The INERT reading R2, conditional on the E-W elections, S-W-1 additivity, E-P2-1 (a), G-POLY1's E3 elections, and the Born/SOA order (memo §9 D-W-5). The polycrystal postulate remains **R3**. W_∪′ is banked ALONGSIDE the suspended W_∪ (E-W-7(a)); **no reinstatement; no observable; no bridge (M.BRIDGE intact); no channel-speed-equality statement; no μ_n; no d derived; the §2.52 Open 3 row untouched.** Not fold-ready: fold requires the CC checkpoint file in the workspace and C-W-1..6 passing (or an S9 cycle closed), then the author's separate fold authorization.

## 8. Delivery note (P-4.c)
Four files are delivered to the AUTHOR: this closure log, Addendum 1, the chat checkpoint of record, and the in-band dispatch. The dispatch is self-contained (13 embeds, including the instrument v6.1, comparator, schema, sealed file and T1-A1 armored, the extractor, and the machinery manifest) and must be forwarded to the CC leg **ALONE** — any file accompanying it at that delivery is a logged deviation at the receiving leg.
