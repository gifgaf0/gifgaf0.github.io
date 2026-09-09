# G-S2C1-W — CC LEG REPORT (execution under the in-band dispatch of record)

**Date:** September 9, 2026. **Gate:** G-S2C1-W (the W_∪′ re-derivation mini-gate; §2.91.O PF-S2 successor). **Leg:** CC (this session; branch `claude/new-session-q8iuz5`). **Dispatch of record:** `G_S2C1_W_CC_DISPATCH_INBAND.md` — md5 **`7ca7e9e9937d2f3c12f0521bce859e37`**, **115,183 B**, delivered **ALONE** (P-4.c verified at delivery: the upload directory contained the dispatch and nothing else — **no loose-file deviation to log**). **Base:** V4.80 `a28e9b40616ee9b5798e9a5be027c1d9`. **Memo LOCKED** `1ebb6a82`; lock record `5f963ed8`; Addendum 1 `12580917`.

**Verdict of this leg: INERT** — no `disp` edge governs on any arm at the sealed budget; W_∪′ = W_∪ = (0, 2.1213132100130068 m] on the governing arm (`hex:step`). Gate class OOM-ROBUST (×10 / ×0.1). **Reinstatement NONE** (E-W-7(a)); INERT ≠ reinstatement.

**Checkpoint of record (this leg, this dispatch):** `g_s2c1w_phase3_cc.json` (schema v1.0) — md5 **`6dde4ae6ffb944d94b138985cd7cf6cd`**, **5,488 B** — committed at **`4184c2ab0b4177024725437f269f32b718076ad3`** on `claude/new-session-q8iuz5` before any quarantined chat material could have been consulted (§6 blindness note).

---

## 1. Verify-then-build (dispatch §3 steps 1–2)

**Step 1 — embeds.** Embed #13 (`extract_embeds_G_S2C1_W.py`) was cut by hand from its markers and verified against its declared hash (`a5a006c6…`, 2,775 B) before first execution; it then extracted and verified **all 13 embeds byte-exact** against the §1 table (13/13 OK, armored embeds decoded to bytes for hash verification only — see §6). Dispatch own hash recorded above.

**Step 2 — machinery in-repo.** `origin/claude/new-session-e1u91p` fetched; commit **`dd813646ed112f630816ee260ae0bdd096e2b417`** present with the ledger's commit message; `gpoly1_gate/phase3/` extracted **at that SHA** (git archive, not branch head): **14 files; `MANIFEST.md5` 13/13 OK; the in-repo manifest is byte-identical to embed #11** (`3b178fb2…`). Nothing in that directory was modified or executed; `att_edge`/`bir_edge` were not reused (the G-POLY1 kinds enter as pinned numbers only) — the machinery served as the lineage reference for the envelope, dressing, masking, and single-read patterns, per the dispatch.

## 2. T1 (dispatch §3 step 3)

Independent scanner **`t1_scan_cc.py`** written from the disclosed rule only (lock record §4 / memo §6.4 D-W-7): non-numeric patterns unconditional; bare-numeric patterns hit only under letter/underscore glue (exponent continuations excluded); digit/sign/dot glue and standalone numeric occurrences logged, not fatal; patterns reported by index only. Effective list = base `20ba1e7e` ∪ A1 `735eae30` = **37 distinct patterns** (both list md5s asserted in-instrument before every scan). Results:

| artifact | hits | logged |
|---|---|---|
| `g_s2c1w_mapper_cc.py` (self-grep, every invocation) | **0** | 1 |
| `t1_scan_cc.py` | **0** | 0 |
| `g_s2c1w_phase3_cc.json` (checkpoint) | **0** | 6 |
| `g_s2c1w_cc_preread_results.json` | **0** | 0 |
| this report | result in the return note (a file cannot carry its own scan) | |

The logged numeric collisions are the expected class (pinned-input decimal renderings and the sealed budget/wavenumber appearing as parsed numbers in the checkpoint — the Addendum 1 §3 expectation; H-W-1 / H-S2C-12 lineage).

## 3. F-W-PIN (dispatch §3 step 4)

`pinned_inputs_G_S2C1_W.json` md5 asserted (`d1edc69b…`, AUTHOR-VERIFIED). **46 values** cross-asserted against the memo §2 pins hard-coded in this instrument (E-W-3(a): the CC a₂ column is the window column of this leg): **max rel dev 0.000e+00** (tol 10⁻¹²), including the a_phys = ℓ_P/C chain identity at both interval ends. The four G-POLY1 edges were pinned **programmatically from the in-repo blind-leg checkpoint** `poly1_phase3_cc.json` (md5 asserted `2064bd7b…`): per-arm `W[1]` byte-values and per-arm class `P-2` all exact; union upper exact. Report-only tie-in reproduced: mean a₂^agg/Q_T^a and spread serialized in the checkpoint's `pinned_gate.tie_in_report_only` (consistent with the memo's −0.52 ± 0.9%).

## 4. Instrument design register (CC-DD)

- **CC-DD-1** — `g_s2c1w_mapper_cc.py` built from scratch; no code transfer from the chat lineage (embed #8 never opened, §6). Own lexer, own Born edge, own fixed-point dressing (with turnover guard and bisection fallback), own union/intersection, own comparison-last gate; stages halt-the-chain in dispatch order (T1 self-grep → F-W-PIN → suites → read → serialize+hash → comparison → checkpoint).
- **CC-DD-2** — NAMED-KEY binder: f4 must read literally `B = <value>`, f5 `k = <value> /m` (band form `[k₁, k₂]` supported under D-W-6, evaluated at k₂ with the sweep serialized); strict positivity; frozen q tokens {phase, group}; constants never bound by magnitude window (G-CI1 S9 root-cause (A) rule).
- **CC-DD-3 (lexer normalization, disclosed)** — the author-supplied sealed serialization wraps token fields in markdown inline-code (one symmetric backtick pair). Invocation 1 aborted masked **[CENSUS]** pre-parse (read NOT spent) because the raw f0 token compared unequal to the declared class. Diagnosis used **structure-only probes** (byte/newline/bar counts, field lengths, char-class shape, and two booleans: "wrapped in one backtick pair" / "core equals the declared class") — no sealed value entered the session. The unwrap (strip one symmetric backtick pair per field before token interpretation) was added as formatting-handling, with pre-read suite #12 asserting a wrapped synthetic row lexes identically to its plain form. The declared census of record ({`disp`: 1}, machine-confirmed at Addendum 1) already reads through this formatting, so the normalization converges with the serialization of record rather than editing it.
- **CC-DD-4** — masked X-1 aborts carry a defect CLASS only (FIELD-COUNT, NAMED-KEY, NEGATIVITY, UNIT, Q-TOKEN, KIND, CENSUS, …); census and md5/bytes asserted pre-parse, so pre-parse defects do not spend the read.
- **CC-DD-5** — comparison-last guard: the comparison function refuses to run without `pre_comparison_md5` (hash of the serialized sealed/anchors/per-arm/robustness/union block); F-W-MONO is a trapped S9 halt, never a finding.
- **CC-DD-6** — EG-9 as coded: `fail_L` requires the floor to consume the budget at a_phys.lo **and** under the ×10 relaxation; the base-only firing is serialized as `oom_fragile`. The robustness arm (Γ–M column, a_phys.hi — the maximal floor) is serialized per anchor in `robustness_arm`, non-verdict.
- **CC-DD-7** — checkpoint T1 scan is taken over the pre-scan serialization; the scan block is appended after (the hash reported is of the final file).

## 5. Pre-read suites and the read (dispatch §3 steps 5–6)

**24/24 suites green** before any sealed open (serialized in `g_s2c1w_cc_preread_results.json`): Born edge vs hand value; envelope VOID with ceiling 0.3/k; FAIL-L election-robust vs OOM-FRAGILE; Δ₄ both sides of 0.10; dressed fixed point (residual ≤ 10⁻¹²); no-root-beyond-turnover; phase/group edge ratio √3 at zero floor; seven malformed-row masked aborts with masked messages verified; census mismatch (read not spent); comparison-last guard; F-W-MONO trap; masking self-scan (sentinel fields absent from serialized output); band rule; inline-code unwrap.

**The read:** invocation 1 — masked CENSUS abort, pre-parse, **read not spent** (§4 CC-DD-3). Invocation 2 — the **single spent read of this leg**: md5 `8c7d59f6…` + 154 B asserted at open; census confirmed **1 row / {disp: 1} / 8 pipe-delimited fields** (7 content + trailing empty; no leading bar; separator guard implicit in the exact field count); one `disp` anchor lexed, **q = group** (explicit in the sealed text — the D-W-4 silent-text default was implemented but not needed). Identifier fields (f1/f2/f6) were consumed for structure only and appear nowhere outside the sealed file; the row is carried as `row_md5` `45dc769be248e68d8cf2e00684350c83`.

## 6. Blindness and quarantine handling

- **Embed #8 (chat instrument, quarantined):** never decoded into this session, never opened, never consulted — before **or after** the checkpoint commit. The CC-BLIND-FIRST obligation (decode only after the CC checkpoint is hashed and committed) is satisfied trivially: nothing in §3 required consulting it, so the armor was never lifted.
- **Embeds #5 / #7:** read programmatically only — #5 by the scanner at T1 setup, #7 by the mapper at read time; neither's content was displayed or quoted. Note (mechanical): the extractor of record decodes every armored embed to bytes in order to verify the declared (md5, size) — that is its documented convention (its docstring; the G-POLY1 precedent) and the only reading of those bytes outside the designated instruments was the hash.

## 7. Results of record

Sealed anchor (masked): class `disp`, q = group (c_q = 3), budget and wavenumber as parsed numbers in the checkpoint only. Lattice floor at the window reading (CC Γ–K, a_phys.lo): **F_L ≈ 1.1×10⁻⁸¹** — many orders below the budget, exactly the memo §3.8 pre-registered expectation (VOID-TRIVIAL floor); robustness reading (Γ–M, a_phys.hi): ≈ 2.6×10⁻⁸⁰, floor nowhere near consuming any budget → **no FAIL-L, on any arm, under any reading**.

| arm | kd at Born edge | Born edge (m) | Δ₄ | dressed | disp governs? | arm class | W′_A upper (m) |
|---|---|---|---|---|---|---|---|
| hex:step | 0.1906 | 2.224×10⁵ | 0.138 → **DRESSING-SENSITIVE** | 2.434×10⁵ (converged) | no | P-2′ | 2.1213132100130068 (pinned) |
| hex:gem8 | 0.1603 | 1.871×10⁵ | 0.098 | 1.983×10⁵ | no | P-2′ | 1.8866794048346085 (pinned) |
| cubic:step | 0.1528 | 1.783×10⁵ | 0.087 | 1.877×10⁵ | no | P-2′ | 1.838266105289967 (pinned) |
| cubic:gem8 | 0.1296 | 1.512×10⁵ | 0.063 | 1.566×10⁵ | no | P-2′ | 1.6447865351995365 (pinned) |

Every `disp` edge is inside the Born envelope (kd ≤ 0.3, no VOID) and lies ~10⁵ m above the pinned G-POLY1 edge — the pinned edge governs every arm. The record edge is Born a₂-only throughout (E-W-6(a)); the hex:step Δ₄ flag is report-only and on a non-governing edge. **W_∪′ = (0, 2.1213132100130068] (governing arm hex:step); ∩ = (0, 1.6447865351995365]; class INERT; F-W-MONO clean (equality, not excess).**

**OOM nuance (disclosed, rule-faithful):** the per-arm `oom_robust` flags are **False** — under the ×10 budget relaxation, kd crosses the 0.3 envelope on every arm and the arm class label flips P-2′ → VOID-DISP (all `disp` edges VOIDED). The window itself is invariant (the pinned edge governs in both labelings; a VOID can only widen), so the **gate-level** comparison class is INERT under base, ×10, and ×0.1 alike: `comparison.oom_robust = true`. The flip is a label move with zero window consequence, reported as the frozen §3.5 rule requires.

## 8. Honesty items (H-CC)

- **H-CC-1 (self-caught, post-read, verdict-inert):** one pre-read synthetic — the B′ constant of the no-root-beyond-turnover suite — turns out to equal the sealed budget numerically. It was chosen blind (before any sealed open, in a suite that exercises the dressed-root solver on synthetic coefficients only) and touches no verdict path. Consequently the checkpoint's `read.synthetics_disjoint_from_sealed = true` flag is accurate for its implemented check (anchor values vs the enumerated synthetic set) but that set omitted this one constant — a blind spot in the flag, not in the verdict. Per the H-W-1 discipline the suite was **not** re-cut post-read; the collision stands disclosed here.
- **H-CC-2 (invocation-1 abort and amendment):** the masked CENSUS abort and the CC-DD-3 unwrap amendment occurred between invocation 1 (read not spent) and invocation 2 (the single spent read). The amendment was made on structure-only evidence, enumerated in §4; no anchor value was seen before the spent read.

## 9. Deviations and standing items

- **D-W-9 / D-W-10 (carried from Addendum 1):** the externally executed CC checkpoint (declared md5 `97f26c04f982b1cc1694f4a47bdce882`; file absent) is **not** this file. This run is the canonical CC emission **under the dispatch of record** (the dispatch's own D-W-9 clause: representational resolution by re-emission under this dispatch). The frozen comparator `g_s2c1w_compare_v1_0.py` hard-pins the declared md5 and will exit 3 (OUTSTANDING) against this checkpoint; per the dispatch that pin is not editable after the fact — disposition (adopting this dispatch-canonical emission as the CC side of C-W-1..6, the path-(a) mini-dispatch pattern) is the author's, at fold level.
- **P-4.c:** clean — no loose file accompanied the dispatch.
- **Q-W-1** stands as recorded (the instrument read the sealed text as dispositive; nothing was re-derived from any named source).
- **Not done, per dispatch §4:** no fold; no register change; no reinstatement of W_∪; no reading of the four G-POLY1 sealed anchors (pinned only); no re-fit of any pinned coefficient; no per-arm tuning.

## 10. Return (dispatch §0 RETURN)

- **Checkpoint:** `gs2c1w_gate/g_s2c1w_phase3_cc.json` — md5 `6dde4ae6ffb944d94b138985cd7cf6cd`, 5,488 B (schema v1.0; T1: 0 hits, 6 logged).
- **CC report:** this file (md5 in the return manifest and the chat-side return note).
- **Return manifest:** `gs2c1w_gate/RETURN_MANIFEST.md5` (md5 + bytes for every returned artifact).
- **Branch:** `claude/new-session-q8iuz5`. **Commits:** checkpoint of record at `4184c2ab0b4177024725437f269f32b718076ad3`; this report and the manifest in the follow-up commit on the same branch (sha in the session return note — a commit cannot carry its own sha).
