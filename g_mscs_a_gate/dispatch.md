# G-MSCS-A — CC LEG DISPATCH (P-4 single-file in-band; P-4.b armor; P-4.c lone delivery; CC-BLIND-FIRST)

**Gate:** G-MSCS-A (the sealed-anchor mini-gate on the texture constraint surface r_agg = κ₂₂t₂² + κ₄₄t₄² — the registered successor of G-MSCS1 / G-MSCS2; G-MSCS1 kill-surface item (iii)). **Date:** September 29, 2026 (September 30, UTC).
**Base ledger:** `SQT_Master_Ledger_v4_86_CANONICAL.md` md5 `d4c42a53cbd6d325ebc740879288e844` (deliberately not in the repository; not needed for this leg — everything this leg consumes is pinned).
**Lock chain (all FROZEN):** memo v2 `6ea16b952db835bb351d3dc1b474c6ed` (121,950 B) · lock record `8116cc622279b5d4e73214178ae97cd8` (Addendum A-2.1–A-2.6, binding) · pinned inputs `2d44ec01a66889f330d940dee3313bdc` (96,761 B; the author's word "Pinned inputs verified", lock record §3) · schema v1.0 `5323e11fc27d688f61aaf57302c875c0` · comparator v1.0 `c5b4a7aab2fc8651be6d26d1f3d25642` (asserts the schema md5; 22 selftest suites) · gate T1 list `e274e58ea50b9ed347969e507d2a4f36` (36 patterns = base `05302210cc4ceb70553acbe8379e9fc3` 11 + the G-MSCS1 stratum 25) · **T1-A1 `3b753b3a371a162fc2ab21b9eed51bd5` (1,030 B, 68 pattern lines; author-supplied; FROZEN after the chat-side pre-freeze collision scan: 0 hits over every locked artifact and the chat mapper)** · scanner `6b86290090a8c84f1b1a0a99ec0bf697` · chat mapper `0d0e5ecf610b34f21e8c22dd3938ce40` (frozen; quarantined here).
**Elections (T3):** E-SA-0 … E-SA-11 all (a); E-SA-7 base `05302210` + the G-MSCS1 stratum. Schema codes: `a` ×11, `05302210+MSCS1stratum`.
**Sealed anchor (the author's delivery of September 29, 21:31 PDT):** `anchors_G_MSCS_A_SEALED.md`, unarmored md5 `cfd62dcf060427ac3402604e6c3284ff`, 177 B, census 1 row, class `spd`, 11 fields — confirmed by the chat leg in `census` mode only (md5, bytes, census, row md5 `59b357fda68557002f11a40100c3ca9c`; nothing else read). The armor is carried here byte-exact (P-4.b).
**Chat-leg state at dispatch (E-SA-8(a), CC-BLIND-FIRST):** Phases 0 and 2 EXECUTED on the frozen mapper (pre-read checkpoint `ccbb32077996833cdac2339938193ec1`, `phase3` = null; 12/12 controls, 14/14 suites); **Phase 3 NOT executed — the chat read runs only after your pre-consultation checkpoint is committed.** Your read is the read of record for the class.

**T1-scan exemptions (the G-POLY1 justified-exemption class):** the three list embeds necessarily contain every pattern; the sealed embed is armor; the dispatch **plaintext** (minus those embeds and minus base64 armor *bodies*, which are transport encoding, not text) scans CLEAN against the gate list ∪ A1; every plain payload scans CLEAN on its own before embedding (the pinned file logs formatting collisions, not hits — memo §13).

**ACTIVATION FLAG — must be present verbatim in the author's directive to you:** `ACTIVATE: G-MSCS-A-CC-LEG-1`. Without it, do not proceed.

## 0. Blindness clause (read first)

Three embeds are **QUARANTINED** (base64): the chat mapper, its pre-read checkpoint and its freeze report. **Do not decode any of them until step 5.** Build your instrument from the memo (§1, §3, §4, §5, §6), the lock record (Addendum A-2 — the binding operationalizations), the schema and the pinned file ONLY. The sealed file is **QUARANTINED-UNTIL-YOUR-PHASE-3**: decode its armor only inside your Phase 3, after your Phase 0 and Phase 2 are green and committed; never print, log or write any of its values (lo, hi, k_em_max, k_t_max, cl, src, note) — only its md5, byte count, census and row md5s. The comparator refuses a checkpoint carrying any such field.

## 1. Embed inventory (20 plain/raw, 3 quarantined)

| Embed | md5 | Size | Handling |
|---|---|---|---|
| `staging_memo_G_MSCS_A_v2.md` | `6ea16b952db835bb351d3dc1b474c6ed` | 121,950 B | plain |
| `G_MSCS_A_LOCK_RECORD.md` | `8116cc622279b5d4e73214178ae97cd8` | 17,923 B | plain |
| `g_mscs_a_schema_v1_0.json` | `5323e11fc27d688f61aaf57302c875c0` | 9,436 B | plain |
| `g_mscs_a_compare_v1_0.py` | `c5b4a7aab2fc8651be6d26d1f3d25642` | 16,850 B | plain |
| `pinned_inputs_G_MSCS_A.json` | `2d44ec01a66889f330d940dee3313bdc` | 96,761 B | plain |
| `sa_build_pinned_inputs.py` | `8189100ede80eac360b25a146e580abf` | 41,342 B | plain |
| `sa_verify_pinned_inputs.py` | `cf004d517d2efe91a02c92a58e3df6bf` | 28,804 B | plain |
| `sa_anchor_validate.py` | `3a11c8f1421d26b882097dbd4e0759d7` | 7,604 B | plain |
| `tools/t1/T1_forbidden_G_MSCS_A.txt` | `e274e58ea50b9ed347969e507d2a4f36` | 1,482 B | T1 list (scan-exempt) |
| `tools/t1/T1_base_author_20260919.txt` | `05302210cc4ceb70553acbe8379e9fc3` | 143 B | T1 list (scan-exempt) |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 B | plain |
| `tools/t1/t1_forbidden_G_MSCS_A_A1.txt` | `3b753b3a371a162fc2ab21b9eed51bd5` | 1,030 B | T1 list (scan-exempt) |
| `inputs/gmscs2_gate/g_mscs2_chatleg_checkpoint.json` | `1c5b6b59829d2a6b9ae2b1a7a016832d` | 31,575 B | plain (a pinned source, byte-exact from main e1fa071) |
| `inputs/gmscs2_gate/g_mscs2_ccleg_checkpoint.json` | `9961745d1e1857cfab6445d4754b5060` | 68,540 B | plain (a pinned source, byte-exact from main e1fa071) |
| `inputs/gmscs1_gate/g_mscs1_chatleg_checkpoint.json` | `c04c0b8ea34cfe60f231aa06828e6ce4` | 33,289 B | plain (a pinned source, byte-exact from main e1fa071) |
| `inputs/gmscs1_gate/g_mscs1_ccleg_checkpoint.json` | `249e11dd53c4cb82f302b15d3c94c337` | 24,415 B | plain (a pinned source, byte-exact from main e1fa071) |
| `inputs/gmscs2_gate/diag_kappa24.json` | `b7952dfcaddcd1d98e424aee8ce5231f` | 1,917 B | plain (a pinned source, byte-exact from main e1fa071) |
| `inputs/gmscs2_gate/diag_quadform_basis.json` | `d84aa1fdce7dea1b1a5d24dfb8f13c18` | 1,119 B | plain (a pinned source, byte-exact from main e1fa071) |
| `inputs/gci1_gate/ci1_phase3_cc_r2.json` | `845ae6beb1b90fe34c540f843ffdb9f5` | 45,760 B | plain (a pinned source, byte-exact from main e1fa071) |
| `sealed/anchors_G_MSCS_A_SEALED.md.b64` | `904a8dffbe8ef50e0555bf278c7581b0` | 409 B | the author's armored sealed file (P-4.b) -- QUARANTINED UNTIL YOUR PHASE 3; the armor itself is carried raw |
| `g_mscs_a_chatleg.py` | `0d0e5ecf610b34f21e8c22dd3938ce40` | 51,490 B | QUARANTINED (base64) |
| `g_mscs_a_chatleg_prereadcheckpoint.json` | `ccbb32077996833cdac2339938193ec1` | 13,842 B | QUARANTINED (base64) |
| `G_MSCS_A_MAPPER_FREEZE_AND_PREREAD_REPORT.md` | `1bf60dd342adbe3f09043365cd25e021` | 5,773 B | QUARANTINED (base64) |


## 2. Verify-then-build

Save this file as `dispatch.md` in a fresh `g_mscs_a_gate/` directory (branch from the current `main` = `e1fa071`, or later; say which), then run the extractor below **without** `--decode-quarantined` (it recreates `tools/t1/`, `inputs/` and `sealed/`):

```python
import base64, hashlib, os, re, sys
src = open(sys.argv[1], 'rb').read()
pat = re.compile(rb'=====BEGIN-EMBED name=(\S+) md5=([0-9a-f]{32}) bytes=(\d+) encoding=(raw|base64)(?: armor_bytes=(\d+))?[^\n]*\n')
pos = 0
while True:
    m = pat.search(src, pos)
    if not m: break
    name, want, n, enc, armor = m.group(1).decode(), m.group(2).decode(), int(m.group(3)), m.group(4).decode(), m.group(5)
    start = m.end()
    if enc == 'raw':
        payload = src[start:start + n]
    else:
        if '--decode-quarantined' not in sys.argv:
            print(f'SKIP {name} (quarantined; not decoded)'); pos = start + int(armor); continue
        payload = base64.decodebytes(src[start:start + int(armor)])
    got = hashlib.md5(payload).hexdigest()
    assert got == want and len(payload) == n, f'{name}: md5 {got} != {want} or length {len(payload)} != {n}'
    os.makedirs(os.path.dirname(name) or '.', exist_ok=True)
    open(name, 'wb').write(payload); print(f'OK   {name}  {got}  {n:,} B')
    pos = start + (n if enc == 'raw' else int(armor))   # step over the body: the sealed armor's own header line sits inside a raw body
```

Expected: **twenty `OK` lines and three `SKIP` lines.** (`sealed/anchors_G_MSCS_A_SEALED.md.b64` extracts as a raw file — it is the author's armor, not the anchor; do not decode it before your Phase 3.) Any assertion failure → HALT, report the md5 seen, do not build. Then: `python3 tools/t1/t1_scan.py tools/t1/T1_forbidden_G_MSCS_A.txt staging_memo_G_MSCS_A_v2.md G_MSCS_A_LOCK_RECORD.md` → CLEAN; `python3 g_mscs_a_compare_v1_0.py selftest` → SELFTEST PASS (22/22; this also proves the schema md5 you hold is the frozen one); `python3 sa_verify_pinned_inputs.py inputs pinned_inputs_G_MSCS_A.json sa_build_pinned_inputs.py` → RESULT: PASS (the `inputs/` tree carries the seven pinned sources at their repository paths, so it serves as the repo root).

## 3. Build (blind)

Instrument `g_mscs_a_ccleg.py`, written from the words of A-2 and memo §3–§6, with **its own parser, binder and class logic** (the parse is the independence surface — C-SA-8 requires your instrument md5 to differ from the chat mapper's, and the chat mapper stays quarantined until step 5). It must: md5-guard the memo (md5 + bytes), the pinned file (md5 + bytes), the lock record, the T1 list, A1, the scanner, the schema and the comparator; T1-scan itself, the memo, the pinned file, the lock record, the schema and the comparator at every invocation under the gate list ∪ A1 and halt on any hit, no override; read every banked value from the pinned file by name (A-2.1) and re-read every `raw` value from `inputs/` through the `provenance` pointers (F-CTRL-SA-PIN); re-derive `derived` with your own code (F-CTRL-SA-PIN-DERIVED, the tolerance of A-2.2); implement the twelve Phase-0 controls (A-2.2), the fourteen Phase-2 suites (A-2.5) and the masked grammar (A-2.3); and map per A-2.4 (per row, the regime clause, the intersection, the one-parameter windows with the basis-independent class and the three flags, the exclusion classes with sub-reasons and requirements, the two-parameter region on the 201 × 201 area grid, the gate class in precedence, the σ-union, OOM ×10 / ×0.1 with the monotonicity check). Checkpoint keys per the schema (`phase0`, `nulls`, `grids` with the counts computed at run time, `phase2`, `phase3`, `T1_post_write`; identity fields as the schema's C-SA-0 list; `instrument_md5` yours; `t1_a1_md5` = `3b753b3a…`). Floats at full precision; sorted keys; no anchor value anywhere.

## 4. Run (blind; CC-BLIND-FIRST)

1. Phase 0 (12 items; halt-on-fail → INDETERMINATE; `sealed_opens_before_phase3` must be 0) → Phase 2 (14 suites; all green before any sealed open) → write and **commit** `g_mscs_a_ccleg_prereadcheckpoint.json` (`phase3` = null), quoting its md5 in the commit message.
2. Phase 3: decode `sealed/anchors_G_MSCS_A_SEALED.md.b64` (strip the `=====` marker lines; base64), assert md5 `cfd62dcf…` and 177 B, parse masked, map, OOM, write `g_mscs_a_ccleg_checkpoint.json`, T1-scan it post-write (delete on a hit), and **commit it as the pre-consultation checkpoint**, quoting its md5 and the gate class in the commit message. Only then:
3. Return (§5). The chat leg runs its own read after your pre-consultation commit; the two-leg comparison (`g_mscs_a_compare_v1_0.py compare CHAT.json CC.json`) is run by both legs afterwards; S9 on misses; the comparator's C-SA-3 requires identical sealed md5, bytes, census and row md5s, C-SA-1 every edge at 1×10⁻¹⁰ relative, C-SA-2 every class and flag identical.

## 5. Return (single file, in-band, mirrored)

`G_MSCS_A_CC_RETURN_INBAND.md`: branch + commits (pre-read first, pre-consultation second); the activation flag line you received, verbatim; instrument summary (parser, binder and class logic in your own words; run time); the Phase-0 table with observed floats; the Phase-2 table; **the gate class and the serialized classes, flags and edges — never a value of the sealed file**; CC-DD items (every reading you had to take that A-2 left to you, if any); H-CC items (disagreements with memo / lock record / schema / pinned file; self-caught bugs); deviations; T1 state (hits 0; collision counts). Embeds (the sentinel format of this dispatch, byte-exact): your instrument, your pre-read checkpoint, your checkpoint. Only after committing the return, decode the quarantine (`--decode-quarantined`) and add, as a separate commit, your run of the comparator on the chat pre-read checkpoint against your pre-read checkpoint (expected: a PASS on everything but the pre-read `phase3` absence, which the comparator treats as a pre-read pair). Scan the return before committing. Per the gate convention the chat-side fold estate lands later in `g_mscs_a_gate/estate/` by a successor PR; do not commit any canonical ledger.

## 6. Disclosures (chat leg)

- **D-SA-1 (pre-freeze collision, resolved before A1 arrived):** a synthetic A1 built during the chat mapper's end-to-end test produced one-significant-digit renderings that coincide with tolerance literals in the locked artifacts; the author's A1 as delivered carries no such pattern — 0 hits over every locked artifact, the mapper, the reports and the erratum (68 patterns, 3 formatting collisions in the memo, none elsewhere).
- **D-SA-2 (delivery mode, recorded):** the armored sealed file and A1 arrived base64-armored inline in the author's directive rather than as attachments. The chat leg wrote the armor to files byte-exact and opened the sealed armor only through the mapper's `census` mode (md5, bytes, census, row md5), never decoding it otherwise; the chat mapper was frozen before delivery, so the exposure could tune nothing, and the read of record is yours (CC-BLIND-FIRST). Recorded so it is a decision, not an oversight; the fold's H-register will carry it if the author so elects.
- **Repository state at dispatch (recorded as observed):** `git ls-remote origin refs/heads/main` at 2026-09-30 02:05:51 UTC → `e1fa071758a0912472bbb6eba7f77fab35669807`; the seven pinned sources at their md5s of record; embedded here byte-exact so this leg is self-contained.

## 7. Embeds

=====BEGIN-EMBED name=staging_memo_G_MSCS_A_v2.md md5=6ea16b952db835bb351d3dc1b474c6ed bytes=121950 encoding=raw=====
# STAGING MEMO — Gate G-MSCS-A (the sealed-anchor mini-gate on the texture constraint surface r_agg = κ₂₂t₂² + κ₄₄t₄² — the registered successor of G-MSCS1 / G-MSCS2) — v2 DRAFT

**Date:** September 29, 2026 (v2; draft v1 of the same date, md5 `a7d6bdbc656e9d924e6bea84b3cef3c3`, 67,501 B, superseded — §C records every change). **Base:** `SQT_Master_Ledger_v4_86_CANONICAL.md` md5 `d4c42a53cbd6d325ebc740879288e844` (1,730,321 B) — the project-store copy byte-verified September 29, 2026 (md5 over all 1,730,321 bytes; H-SA-1 discharged). **Status: DRAFT — NOT LOCKED. Elections applied (§10). The pinned-inputs file has been generated for the author's pre-lock verification (§9): `pinned_inputs_G_MSCS_A.json`, md5 `2d44ec01a66889f330d940dee3313bdc` (96,761 B). No sealed file exists. No T1 list is frozen for this gate. No schema, comparator or mapper exists. Nothing has been mapped against any anchor.** Author authorization is required, separately, for: the pinned-inputs verification; the lock, which also freezes the T1 gate list, the schema and the comparator (§5 step 3); the sealed-anchor supply and the T1-A1 freeze (§5 steps 5–6); and each execution step (the G-S2C1-W order, amended in §5 so that the pinned inputs are verified before lock). **Lineage:** G-MSCS1 E-MS-6(a) ("any comparison is a separate pre-registered mini-gate with sealed anchors") → the V4.83 fold-in record, "a sealed-anchor mini-gate on κ₂t² (only on the author's word)" (§2.91.Q lists "a sealed-anchor mini-gate on κ₂t²") → the §2.91.Q V4.85 bracket, "the sealed-anchor mini-gate now has a curve on both stacking branches and is re-registered as κ₂₂t₂² + κ₄₄t₄²" → the author's word, directive of September 27, 2026, 20:31 PDT: "The author has elected to proceed with the sealed-anchor mini-gate on the texture constraint surface (r_agg = κ₂₂t₂² + κ₄₄t₄²)." → **the author's elections and v2 directive of September 29, 2026: E-SA-0 … E-SA-11 all (a), E-SA-7 "The base 05302210 + the G-MSCS1 stratum"; "Please proceed with generating staging memo v2. Ensure the LSF-δ sweep is fully executed and documented. Include the H-MS2-9 honesty item as a planned bracket for the eventual fold. Once v2 is ready, provide it alongside the necessary commands for generating the pinned inputs file so that I may review and verify it prior to the final lock"**

**Gate ID (elected, E-SA-0(a)): G-MSCS-A.** Everything G-MSCS1 and G-MSCS2 settled is consumed as banked: no fit is re-run, no coefficient re-selected, no aggregate recomputed. (The basis-independent estimators used below are fixed linear combinations of banked grid values, not fits.) The gate adds one thing — the sealed anchor — and a mapper that turns it into a statement about the texture import. It is the first gate of the multi-species family that sits on the kill surface (G-MSCS1 §5 item (iii)).

## A. The binding process rules from the G-MSCS2 lock — where each is implemented

The directive of September 27 makes the five process notes of the G-MSCS2 closure (memo `e43a0732` §5; §2.91.S) binding on this draft. Each is implemented as a mechanism:

| # | Rule | Implemented at | Mechanism |
|---|---|---|---|
| 1 | Any "r_agg unchanged" control states which ODF reading it assumes | §5 (every control); §6.2 (every null key) | every control and every null key carries an `odf_reading` field from a closed token set that names each ODF once, with `none` where no ODF is involved (§6.2); the comparator rejects a record without it |
| 2 | Schema null tolerances at the fit's resolution, or a basis that resolves the null | §6.2; S-SA-4 | every null is compared at the resolution of that quantity in this family (τ_agg = 1×10⁻⁶ for first-order slopes; the κ floor 1×10⁻⁶ for coefficients — the G-MSCS2 v1.1 delta), never below what the 3-term fit resolves; every coefficient carries its computed fit resolution (fit vs basis-independent) |
| 3 | Every inherited definition gets a one-line re-derivation in the new context before lock | §2 (D-1 … D-24) | a table: inherited definition → one-line re-derivation here → carry status; re-deriving D-1 produced S-SA-1, the most consequential finding of this draft |
| 4 | Point counts are computed from the pinned grid, never typed | §6.3; §15 | the schema holds grid *generators*; the comparator recomputes every count from them; the counts quoted here are printed by the builder and the verifier from the pinned generators and written into no file — which re-exhibits the H-CC-1 slip: the lock-record "7" and "5" are the *strict*-window counts; the inclusive windows both legs used hold 9 and 7 points |
| 5 | A claimed null carries a basis-independent estimator as a schema key | §6.2 N-1 … N-4 | four nulls are consumed (the first-order slope on every arm; κ₂₄ on every key; the fcc κ₂; the fcc quadratic-form κ₂₂); each has a fit key and a basis-independent key (Richardson extrapolation of the odd, even or mixed parts of the banked grids), both compared at the rule-2 tolerance |

## B. Pre-draft catches (chat-self-caught while re-deriving the inherited definitions, plus the independent audit of §15 and, in v2, the LSF-δ read of §14; nothing computed against any anchor)

- **S-SA-1 — the sightline (rule 3 on D-1; the load-bearing catch).** The inherited r_agg is a ratio of two *k̂-sphere* means (G-MSCS1 §2.5). A sealed speed anchor is, in its likely form, one source seen along one sightline. For any fiber texture the aggregate is transversely isotropic about the fiber axis ẑ (for every grain tensor, tetragonal-form hex included, and every averaging scheme), so along ẑ the two transverse modes are degenerate and pure, the ODF-averaged E₂ weight is equal on them, λ_L = 0, and **the per-direction species split vanishes identically at every texture strength**. A single-sightline anchor at unknown angle ψ to an unknown fiber axis is therefore, at its most conservative reading, **INERT for every texture** — no model-independent texture bound follows from one sightline. A binding window needs an identification; v1 offered three readings (E-SA-3), and **E-SA-3(a) is elected: the inherited sphere-weighted reading with the identification declared (I-SA-1)**. (LSF-δ, L-SA-2: in the effective-field-theory dialect one sightline likewise constrains only a fixed projection of the direction-dependent coefficients, and single-event readings there are one-coefficient-at-a-time or isotropic-only by assumption; I-SA-1 is this gate's analogue of that assumption — an identification, stated, not derived.) *Pre-draft check (disclosed; the G-MSCS1 F-CTRL-TEX synthetic transversely-isotropic tensor, not a banked tensor; §15):* κ(ψ = 0) = −4×10⁻¹⁴ (P₂ family) and 0 (P₄); for P₂, κ(ψ) = κ(90°)·sin⁴ψ to four digits and its maximum is at 90°, 1.61× the sphere-weighted κ; for P₄, κ(ψ) is non-monotone with its maximum 1.66× the sphere-weighted κ at ψ = 40.9° (1° scan with golden-section refinement); the sphere-weighted κ exceeds the uniform-sphere (population) mean of κ(ψ) by 1.17× (P₂) and 1.40× (P₄), so sphere-weighted windows come out 7–16% tighter than a population reading. The readings differ by O(1) factors in κ and by their square roots in a window edge; the conservative reading differs from all of them categorically.
- **S-SA-2 — the hex null rays (S2-E₂ arms).** On hex, for the S2-E₂ descriptor, κ₂₂ < 0 < κ₄₄ (both legs), so the two-parameter form is indefinite: r = 0 at second order along |t₄/t₂| = √(−κ₂₂/κ₄₄) = **2.9957 / 2.9948 / 3.2497 / 3.2501** (hex_step|a, |b, hex_gem8|a, |b; Hill, basis-independent) and 2.9887 / 2.9878 / 3.2460 / 3.2465 (HS-mean). For any interval containing δ = 0 the admissible (t₂, t₄) region reaches the domain boundary along those rays: **the general weak texture on the hex branch cannot be bounded at second order by the S2-E₂ split**; third order governs there (the registered successor "the third-order cross terms", unopened). Under S2-h every hex coefficient is negative, so its (diagonal) form is negative-definite — no null rays, a compact region. The gate bounds the one-parameter families and reports the two-parameter region without assigning it a class.
- **S-SA-3 — two normalizations of t₄.** Hex t₄ multiplies P₄ (⟨P₄²⟩ = 1/9) and cubic t₄ multiplies K̃₄ (⟨K̃₄²⟩ = 4/21); t₂ multiplies P₂ (⟨P₂²⟩ = 1/5). A window "|t₄| ≤ x" means different textures on the two branches. A cross-branch statement needs a common measure; the gate uses the RMS deviation of the ODF from uniform, σ = |t|·rms (rms = 1/3, √(4/21) = 0.436436, √(1/5) = 0.447214; the closed forms verified in exact rational arithmetic by the builder) — E-SA-5(a), elected.
- **S-SA-4 — the fit-basis resolution of the coefficients of record (rule 2).** The κ of record is the 3-term {t, t², t³} fit over the nine inclusive points |t| ≤ 0.25. The basis-independent Richardson value of the even part of the banked grid differs from it, on the S2-E₂ Hill arm, by **1.18–1.31×10⁻⁵ (hex κ₄₄), 5.08–8.92×10⁻⁶ (hex κ₂) and 1.22–1.82×10⁻⁴ relative (fcc κ₄₄)**, and by ≤ 2.3×10⁻⁵ (HS-mean) and ≤ 7.3×10⁻⁴ (S2-h) on the robustness arms — the quartic content aliasing into t², the mechanism of the eight κ₂₂ misses of G-MSCS2 run 1. On fcc that is at or above the 1×10⁻⁴ two-leg κ tolerance; the legs agreed because they shared the basis. It moves a window edge by at most 0.91×10⁻⁴ relative on the Hill arm and 3.7×10⁻⁴ on S2-h (E-v2-6). Disposition: the κ of record stays the edge of record (E-SA-6(a)); the basis-independent edge is serialized beside it; a class that differs between the two is flagged RESOLUTION-SENSITIVE, never silently resolved.
- **S-SA-5 — the binding end is set by sign(κ).** For an interval [lo, hi] ∋ 0, a key with κ < 0 is bounded by lo and a key with κ > 0 by hi. For S2-E₂ on fcc κ₄₄(⟨001⟩) < 0 < κ₄₄(⟨111⟩): **the descriptor-axis choice decides which end of the anchor binds**, and the primary ⟨001⟩ axis binds on the opposite end from the hex t₄ family. Under S2-h every key binds on lo. The anchor's sign convention is therefore load-bearing: a fixed `delta_def` token (§4) and an asymmetric-interval control (F-CTRL-SA-SIGN).
- **S-SA-6 — the first-order polarization split dominates.** The textured aggregate also splits its two transverse polarizations at *first* order: b₁ (A-2.7) is the qSH/qSV split per unit t₄ for propagation perpendicular to the fiber (ψ = 90°), banked. |b₁/κ₄₄| = 101.2 (hex; fcc ⟨001⟩) and 151.86 / 151.85 (fcc ⟨111⟩, step / gem8) per unit t₄ (computed), so at the domain edge |t₄| = 0.25 the ψ = 90° polarization split exceeds the sphere-weighted species split by a factor of at least 404.9, and more at smaller non-zero |t₄|. The two are different directional measures (κ(90°) is not the sphere-weighted κ — S-SA-1), so this is a statement of dominance, not a crossover. An anchor on polarization-dependent propagation would constrain texture at first order; that is outside the registered scope of this gate (E-SA-1(a)) and is named so that no window from this gate is read as the tightest texture constraint the substrate admits. The polarization split also vanishes along the fiber axis (the S-SA-1 symmetry). (LSF-δ, L-SA-2: at the lowest order of the effective-field-theory dialect the tensor-sector shift is nondispersive and nonbirefringent, so a dispersion-free first-order polarization split has no counterpart there — a translation question for the E-SA-1(b) successor, not for this gate.)
- **S-SA-7 — the aggregate regime.** The banked r_agg is the leading-order, long-wavelength aggregate (no Born; E-MS2-3(a)). It describes a messenger only while k·d ≪ 1 across that messenger's band. d is an import (M.CW). The operative on-ledger scale is the floor-adjoining (near) component of the EM-side window of record, W^EM_∪ = (0, 3.7641664288e-33] SI length units (G-CI1, V4.77; beyond 1.0813e+25 the ledger records a far component VOID, every arm undecidable). At that d the clause fires only for k > 7.96×10³¹ m⁻¹ (v1: "8.0×10³¹"; E-v2-6) — it is effectively vacuous, stated so it is a decision rather than an oversight. The W_∪′ edge banked alongside (2.1213132100130068 m, W_∪ still suspended) would instead VOID every EM band with k > 0.1415 m⁻¹ (v1: "0.14"; E-v2-6) — E-SA-4(a) elected: the W^EM_∪ edge, in v2 read by key from the G-CI1 CC r2 checkpoint (§9).
- **S-SA-8 — "r_agg unchanged by t₂ on fcc" has two readings (rule 1).** Under reading (ii) (the O_h-symmetrized l = 2 term, identically zero because the octahedral group has no l = 2 invariant) r_agg is unchanged at every order. Under reading (i) (the inherited single descriptor-axis P₂, the one both G-MSCS2 legs took) r_agg is unchanged by t₂ alone (≤ 3.4×10⁻¹⁶ at t₂ = 1) and at second order jointly, but changes at third order with t₄: the t₂t₄² coefficient is −5.90×10⁻⁵ (step) / −8.51×10⁻⁵ (gem8) on both axes (the banked CC fit; H-MS2-9), the A-3.1 mixed change −9.08×10⁻⁷ / −1.30×10⁻⁶ at (0.25, 0.25). The mapper treats the fcc t₂ direction as unconstrained at second order under both readings; the reach test of the kill (§3.6) includes the reading-(i) third-order content, the wider of the two.
- **S-SA-9 — the second-order box understates the banked reach (audit finding E1).** Inside D the banked grids reach beyond the second-order box range: by up to 7.5% (1.0745×) on fcc under reading (i) (the CC 5 × 5 corner of cubic_gem8|111: +2.011×10⁻⁵ against +1.872×10⁻⁵) and by 5.0% on the negative side (cubic_gem8|001); by ≤ 1.0% on the robustness arms (their one-parameter grids) and by ≤ 0.06% on hex. A kill test on the box alone could declare a kill that a banked texture inside D reproduces. Disposition: the reach is the hull of the box and every banked grid value inside D (endpoints within 1×10⁻¹² of zero set to 0 — grid noise never crosses zero), and the kill test uses that hull widened by μ = 0.10 (the D-W-5 threshold) on every arm, covering extrema between grid points and, on the arms without a banked two-parameter grid, unbanked third-order content (E-SA-11). An interval that meets only the widening band is backed by no banked texture: it is classed MARGIN, neither a kill nor a required texture.
- **S-SA-10 — T1-A1 must not collide with locked artifacts.** Scanner `6b862900` counts a bare-numeric pattern as a hit when a whole numeric token equals it, and F-CTRL-SA-T1 has no override. An A1 pattern that is too short (a bare "9", say) would match an unrelated token in the locked memo or mapper and block the gate permanently. Disposition: A1 renderings shorter than four characters are dropped by the builder; the locked artifacts are scanned under A1 before it is frozen (§4.6); and no checkpoint, log or report carries an anchor value verbatim (§4.8). (v2 audit: renderings that carry the Unicode minus sign U+2212 are plain-substring patterns under `6b862900`, because the character is outside the scanner's numeric set; the contextual numeric rule therefore does not shield them, and the pre-freeze scan covers them like any other A1 pattern.)
- **S-SA-11 — three speed statements share the dialect, and only one of them is δ (LSF-δ, L-SA-1).**
  1. *Counterpart timing* compares the tensor messenger with the co-travelling EM signal along one sightline. That is δ as defined; it is conformant `spd` content.
  2. *Detector-network and catalog statements* compare the tensor messenger with the conventional constant, as realized along the network's baselines. That is a different ratio. In the substrate, each descriptor-weighted speed changes with direction at *first* order in t₄ (b₁ ≠ 0 on every key) and, on hex, in t₂ by the first-order affinity; on fcc the t₂ direction is null, since a cubic grain tensor has no l = 2 content. Transverse isotropy pins the qSV speed at ψ = 90° to the on-axis shear speed, so the banked b₁ ≠ 0 is a first-order change of qSH there; each descriptor inherits it at half weight, because the zeroth-order descriptor weights of the two transverse modes are equal (the SO(3) identity). The effective tensor is affine in t at first order (Man–Huang; carried from G-MSCS1 §12). First-order protection — F-MS-3 for the sphere-weighted r_agg, and per sightline by the same identity — concerns only the ratio of the two descriptors.
  3. *Cherenkov statements* are one-sided and compare the tensor speed with the limiting speed of high-energy matter.

  Disposition: only statement 1 is entered as an `spd` row (§4.3, custody rule). Statements 2 and 3 are not mapped by this gate. A gate on statement 2 would be a first-order directional gate — named here, not registered.
- **S-SA-12 — the anchor's sign structure must survive transcription (LSF-δ, L-SA-1).** The primary counterpart-timing interval is two-sided and asymmetric, each end set by a stated emission-delay assumption. Secondary restatements symmetrize it into a magnitude bound. The binding end is set by sign(κ) (S-SA-5), so a symmetrized row changes the budget on every key that binds at the narrower end — silently, since the validator cannot see it. Disposition: the conformant entry is the primary statement's own two ends (§4.3, custody rule). A source that states only a magnitude is still entered lo = −B, hi = +B, as v1 specified.

## C. v1 → v2 (every change; append-only)

1. **Elections applied (§10).** E-SA-0 … E-SA-11 all (a); E-SA-7 as elected. Every "recommended" of v1 now reads "elected". §10 keeps each election's v1 option text verbatim, as the record of what was offered and declined; only E-SA-4's two k thresholds are restated (E-v2-6). Two v1 quantities now serve a declined option only and are kept for information: the primary-arm union (E-SA-9(b)) and the W_∪′ regime edge (E-SA-4(c), carried by no instrument).
2. **LSF-δ executed (§14).** Six clusters, L-SA-1 … L-SA-6 (v1 planned five; L-SA-6, the long-wavelength regime, was added at execution), each source with its transcription ceiling. Verdict: **novel-in-assembly; A0 not triggered**, with one residual risk recorded (the Rodgers preprint at AB, to be read before lock). Two catches, S-SA-11 and S-SA-12, both custody rules for the author's file (§4.3); citation and rounding items H-SA-3 and H-SA-4 (§12); prior art now attributed for ST-1 (L-SA-3), for I-SA-1 (L-SA-2), and for D-13 and D-9 (L-SA-6).
3. **Pinned inputs generated before lock (§3.1, §9; the order the author set on September 29).** `sa_build_pinned_inputs.py` (md5 `8189100ede80eac360b25a146e580abf`) builds `pinned_inputs_G_MSCS_A.json` (md5 `2d44ec01a66889f330d940dee3313bdc`, 96,761 B) from **seven** sources: the six of v1 plus the G-CI1 CC r2 checkpoint, from which the W^EM_∪ edge is now read by key instead of being typed from the ledger (the builder asserts it equals the V4.77 literal).
   - The builder produces identical bytes under Python 3.10, 3.11, 3.12 and 3.13.
   - The independent verifier, `sa_verify_pinned_inputs.py` (md5 `cf004d517d2efe91a02c92a58e3df6bf`), shares no code with the builder and trusts nothing in the file: it holds its own pointer map, constants, tokens and structure.
   - On the file it passes: 335 values checked against their sources, and all 1,105 derived leaves re-derived. It fails on each of 37 tampered copies (§15 item 4).
4. **New control and preflight (§5).** A new control, F-CTRL-SA-PIN-DERIVED. A build-time preflight of every Phase-0 criterion that depends on pinned values only; all pass. The CC counterparts of κ₃, S and b₁ are now pinned too, so F-CTRL-SA-PIN covers every coefficient the mapper uses.
5. **Corrections.**
   - **E-v2-1:** eight "≤" statements in v1 rounded the observed maximum *down*:

     | quantity (where) | observed maximum | v1 bound |
     |---|---|---|
     | N-1, HS-mean (D-7, §6.2) | 2.5054×10⁻¹³ | ≤ 2.5×10⁻¹³ |
     | N-1, S2-h (D-7, §6.2) | 1.2118×10⁻¹² | ≤ 1.2×10⁻¹² |
     | N-2, fcc, chat diagnostic and CC checkpoint | 2.2204×10⁻¹² | ≤ 2.2×10⁻¹² |
     | N-3 fit | 3.1417×10⁻¹⁵ | ≤ 3.1×10⁻¹⁵ |
     | N-3, basis-independent | 1.2212×10⁻¹³ | ≤ 1.2×10⁻¹³ |
     | the t₂-alone change | 3.33×10⁻¹⁶ (three significant digits) | ≤ 3.3×10⁻¹⁶ |
     | the truncation maximum (D-12, §3.3) | 2.1122×10⁻³ | ≤ 2.1×10⁻³ |
     | the S2-E₂ Hill fit-resolution maximum (§6.4) | 1.8194×10⁻⁴ | ≤ 1.8×10⁻⁴ |

     Each bound now states the maximum rounded up. No verdict moves. The nearest to a threshold is the truncation maximum, against the 0.10 flag threshold (a factor of about 47). Every other bound that is tested sits at least three orders of magnitude below its tolerance.
   - **E-v2-2:** v1's F-CTRL-SA-PIN "observed ≤ 2.1×10⁻¹¹" covered only the S2-E₂ coefficients. Over every coefficient the control compares, the maximum is 1.11×10⁻⁹ (S2-h κ₂). It is now restated per arm (§0, §5).
   - **E-v2-3:** H-SA-2's origin. v1 traced "−1.0×10⁻⁴" to the closure memo. It first appears in the CC in-band return prose (`gmscs2_gate/G_MSCS2_CC_RETURN_INBAND.md`, md5 `290b34315f16debd2fdc05f8d2109bee`, line 79), which the closure memo then carried. The item is now H-MS2-9 (§12).
   - **E-v2-4:** N-2 on fcc now also carries this gate's own mixed difference on the CC 5 × 5 grid. That estimate is ≤ 9.5×10⁻¹¹: the O(h⁴) remainder at the coarser (0.125, 0.25) pair, which is sixth-order odd–odd content of the reading-(i) grid, since the pair cancels the quartic term exactly. v1 used this estimator on hex only.
   - **E-v2-5:** S-SA-9 now also states the negative-side excess (5.0%, cubic_gem8|001) and the robustness-arm excess (≤ 1.0%). v1 stated the positive side only.
   - **E-v2-6 (found by the independent audit of v2):**
     - *Rounded values.* Further rounded values are restated, conservatively for the statement they sit in:
       - the regime thresholds, "fires only for k > 7.96×10³¹ m⁻¹" (the threshold is 7.9699×10³¹; v1 printed 8.0) and "would VOID every band with k > 0.1415 m⁻¹" (the threshold is 0.14142; v1 printed 0.14);
       - the quadratic-form agreement, "to within 5.3×10⁻⁶ / 6.1×10⁻⁶";
       - the κ₂₄ fit7 ranges, 1.2–1.9×10⁻⁸ and 1.9–3.5×10⁻⁷;
       - the (a)/(b) coefficient agreement in D-11, 1.1×10⁻³ relative.
     - *Fit resolution per arm.* It is now stated for each arm: on S2-E₂ Hill 1.18–1.31×10⁻⁵ (hex κ₄₄), 5.08–8.92×10⁻⁶ (hex κ₂) and 1.22–1.82×10⁻⁴ (fcc); ≤ 2.3×10⁻⁵ on HS-mean and ≤ 7.3×10⁻⁴ on S2-h, both tested by F-CTRL-SA-RECON (S-SA-4, §6.4). v1 stated the Hill figures as if they held for every arm.
     - *ST-5.* It was false for intervals excluding 0 (a class there turns on the reach, not on D) and is corrected.
     - *§3.6 wording.* It now restricts the t₂ family to hex keys, as the builder and verifier always did.
     - *F-CTRL-SA-RECON.* Its detection-power note is corrected for κ₂: an (a)↔(b) swap there *is* caught by the Hill RECON.
6. **H-SA-2 → H-MS2-9** (the author's numbering, directive of September 29), with a planned bracket for the eventual fold (§12). **H-SA-3** and **H-SA-4** added (§12); H-SA-4 covers three round-downs in the banked record (the κ₂₄ estimator, and the S₄ and b₁ two-leg bounds). **Q-SA-2** and **Q-SA-3** added (§10).
7. **§12 repository observation refreshed.** `git ls-remote` on September 30, 00:01:06 UTC: `main` = `e1fa071…`, unchanged since v1.
8. **ST-1 wording (§8).** The vanishing is claimed on the fiber axis only; shear-speed degeneracies on off-axis cones (L-SA-3) are neither claimed nor needed.
9. **Audit.** v2 was audited by a separate agent before delivery; the findings and their dispositions are in §15 item 6. Besides E-v2-6, the audit produced these changes:
   - the verifier rewritten (item 3);
   - the synthetic generators pinned (§5 Phase 2), because one suite could not be built from v1's budgets (C-SYN-12) and one only by coincidence (C-SYN-13); C-SYN-3's robustness-only interval is pinned too, for definiteness;
   - the PIN-DERIVED scope named (§5);
   - S-SA-11 item 2 made precise;
   - S-SA-10 notes the Unicode-minus renderings;
   - §4.6 item 5 moved to the lock;
   - the pre-lock Rodgers read (§15 item 8).
10. **Structural changes the list above does not already name.**
    - The lock becomes one event that also composes and freezes the T1 gate list and freezes the schema and the comparator (§5 step 3, §15 item 8). v1's order ran lock → T1 list → pinned inputs → schema and comparator.
    - The builder and verifier md5s join the lock record and §6.1.
    - §11 gains a register sentence for the LSF findings and S-SA-11.

## 0. What the ledger has settled (consumed as banked; not re-litigated)

- **G-MSCS1 (§2.91.Q, V4.83):** under E-MS-1(a) EM and S2 are two descriptors of the one transverse phonon; species-speed equality is an SO(3) identity on the untextured aggregate; first-order protection holds in an l = 2 fiber texture; the delivered curve r_agg ≈ κ₂t² on the hex branch; the fcc branch is blind to l = 2 by symmetry. **Kill surface (§5), unchanged since:** (i) E-MS-1(b); (ii) the value of the texture import; (iii) "a sealed-anchor comparison of κ₂t² against the 2017 multi-messenger tensor-speed bound" (E-MS-6(b), declined there). **This gate is item (iii), extended to κ₂₂t₂² + κ₄₄t₄², and what it delivers is a statement about item (ii).**
- **G-MSCS2 (§2.91.S, V4.85):** first-order protection in every l = 4 family; κ₄₄ on all eight keys (fcc ⟨111⟩ = −(2/3)·⟨001⟩ exactly; the hex l = 4 response of the opposite sign to l = 2); the (t₂, t₄) form diagonal (κ₂₄ = 0, basis-independent, both legs); the second-order surface r_agg = κ₂₂t₂² + κ₄₄t₄² + O(t³) closed on every configuration; b₁ the first-order polarization split; exhaustion — (t₂, t₄) is the general axisymmetric weak texture for every observable of the family.
- **ANNEX-CDEF-1 (V4.71):** c is defined as the transverse-channel speed; only dimensionless ratios carry physics. The anchor quantity is a ratio; no SI speed enters any instrument.
- **G-CI1 (§2.91.N, V4.77):** CI-W/EM-IN operative; W^EM_∪ banked. **G-S2C1-W (V4.81):** the `disp` speed-offset anchor kind, the author-supplied sealed file, the T1-A1 protocol, CC-BLIND-FIRST, and the H-W-2 lesson (a sealed row delivered in the clear burns the chat leg's blindness).

**Banked coefficients (S2-E₂ descriptor, Hill; chat checkpoints of record; from the pinned-inputs file — `raw` and `derived.families` — reproduced by the independent verifier; not typed):**

| key | κ₄₄ of record | κ₄₄ basis-indep. | fit res. | κ₂ of record (G-MSCS1) | κ₂ basis-indep. |
|---|---|---|---|---|---|
| hex_step\|a | +1.604053×10⁻⁴ | +1.604034×10⁻⁴ | 1.19×10⁻⁵ | −1.439462×10⁻³ | −1.439454×10⁻³ |
| hex_step\|b | +1.604147×10⁻⁴ | +1.604128×10⁻⁴ | 1.19×10⁻⁵ | −1.438703×10⁻³ | −1.438695×10⁻³ |
| hex_gem8\|a | +1.795073×10⁻⁴ | +1.795049×10⁻⁴ | 1.31×10⁻⁵ | −1.895648×10⁻³ | −1.895632×10⁻³ |
| hex_gem8\|b | +1.795015×10⁻⁴ | +1.794992×10⁻⁴ | 1.31×10⁻⁵ | −1.896137×10⁻³ | −1.896121×10⁻³ |
| cubic_step\|001 | −3.743529×10⁻⁴ | −3.743069×10⁻⁴ | 1.2×10⁻⁴ | null (fit 3.1×10⁻¹⁵) | null (−2.6×10⁻¹⁴) |
| cubic_step\|111 | +2.495686×10⁻⁴ | +2.495380×10⁻⁴ | 1.2×10⁻⁴ | null (≈ −2×10⁻¹⁶) | null (−2.8×10⁻¹⁴) |
| cubic_gem8\|001 | −4.492771×10⁻⁴ | −4.491954×10⁻⁴ | 1.8×10⁻⁴ | null (−1.5×10⁻¹⁶) | null (−1.2×10⁻¹³) |
| cubic_gem8\|111 | +2.995181×10⁻⁴ | +2.994636×10⁻⁴ | 1.8×10⁻⁴ | null (1.3×10⁻¹⁶) | null (−1.2×10⁻¹³) |

κ₂ fit resolution: 5.1×10⁻⁶ (step) / 8.9×10⁻⁶ (gem8). Two-leg agreement of the banked coefficients (chat vs CC checkpoints, relative): S2-E₂ κ₄₄ ≤ 2.1×10⁻¹¹ and κ₂ ≤ 2.7×10⁻¹²; HS-mean κ₄₄ ≤ 1.7×10⁻¹¹; S2-h κ₄₄ ≤ 3.3×10⁻¹⁰ and κ₂ ≤ 1.2×10⁻⁹; the hex quadratic-form κ₂₂ ≤ 1.2×10⁻¹² (E-v2-2). Hex quadratic form (7-term fit): κ₂₂ = −1.439469 / −1.438710 / −1.895660 / −1.896149 ×10⁻³ (= κ₂ to within 5.3×10⁻⁶ (step) / 6.1×10⁻⁶ (gem8)); its basis-independent values from the CC 5 × 5 grid reproduce the κ₂ and κ₄₄ basis-independent columns to all printed digits. HS-mean against Hill (κ_HS/κ_Hill − 1): hex κ₄₄ −0.32%; hex κ₂ −0.78% (step) / −0.55% (gem8); fcc κ₄₄ +3.98% (step) / +6.11% (gem8).

**Reachable δ inside D used by the kill test (§3.6): the hull of the second-order box and every banked grid value inside D, widened ×1.10 (`derived.reach` of the pinned-inputs file):**

| key | S2-E₂ Hill | S2-E₂ HS-mean | S2-h Hill |
|---|---|---|---|
| hex_step\|a | [−9.898×10⁻⁵, +1.103×10⁻⁵] | [−9.820×10⁻⁵, +1.100×10⁻⁵] | [−6.542×10⁻⁷, 0] |
| hex_step\|b | [−9.892×10⁻⁵, +1.103×10⁻⁵] | [−9.815×10⁻⁵, +1.100×10⁻⁵] | [−6.541×10⁻⁷, 0] |
| hex_gem8\|a | [−1.303×10⁻⁴, +1.234×10⁻⁵] | [−1.296×10⁻⁴, +1.231×10⁻⁵] | [−7.565×10⁻⁷, 0] |
| hex_gem8\|b | [−1.304×10⁻⁴, +1.234×10⁻⁵] | [−1.297×10⁻⁴, +1.231×10⁻⁵] | [−7.566×10⁻⁷, 0] |
| cubic_step\|001 | [−2.681×10⁻⁵, 0] | [−2.681×10⁻⁵, 0] | [−2.637×10⁻⁶, 0] |
| cubic_step\|111 | [0, +1.822×10⁻⁵] | [0, +1.787×10⁻⁵] | [−2.637×10⁻⁶, 0] |
| cubic_gem8\|001 | [−3.244×10⁻⁵, 0] | [−3.284×10⁻⁵, 0] | [−3.149×10⁻⁶, 0] |
| cubic_gem8\|111 | [0, +2.213×10⁻⁵] | [0, +2.189×10⁻⁵] | [−3.149×10⁻⁶, 0] |

(Endpoints within 1×10⁻¹² of zero are set to 0 before widening, so grid noise never crosses zero.) S2-h reaches no positive δ on any key. The unwidened hull unions are [−1.1853×10⁻⁴, +2.0115×10⁻⁵] over every key and arm and [−1.1850×10⁻⁴, +1.1223×10⁻⁵] over the primary arm; the bands between these and the widened unions of §7 are the MARGIN bands.

## 1. Object

**Question (one sentence):** given an author-supplied sealed anchor bounding the fractional difference δ between the limiting propagation speeds of the tensor messenger and the electromagnetic messenger, which strengths of the weak axisymmetric fiber texture — t₂ and t₄, the only texture coefficients the descriptor pair sees — are admissible on each instantiated configuration under the banked second-order surface r_agg = κ₂₂t₂² + κ₄₄t₄², and, if the anchor excludes δ = 0, can any texture inside the validated domain reproduce it?

**Per-key classes.** For an interval containing 0, per family: BINDING (a proper window |t| ≤ t\* < D) · INERT-IN-D (the anchor does not bite inside D) · NULL-INERT (the fcc t₂ family). For an interval excluding 0, per key and arm on the key's whole texture domain: EXCLUDED-IN-D (sub-reason SIGN or MAGNITUDE) · TUNED-ADMISSIBLE · MARGIN (meets only the widening band). Flags: RESOLUTION-SENSITIVE, TRUNCATION-SENSITIVE, NULL-FLOOR-SENSITIVE, VOID-REGIME (per row), OOM-ROBUST.

**Gate classes (pre-registered; one assigned by the machine, last; precedence left to right):**
- **INDETERMINATE** — a Phase-0 control or pin fails; no verdict.
- **VOID** — every row VOID-REGIME; nothing mapped. (A non-conformant file never reaches the mapper: it aborts masked before any mapping, the read not spent — §3.2.)
- **ANCHOR-INCONSISTENT** — the rows' intervals do not intersect; no joint mapping; per-row results serialized.
- **KILL-IN-D** — the combined interval I excludes δ = 0 and I misses the widened reach R^w on every elected (key, arm) (E-SA-9, E-SA-11): kill surface item (iii) fires within the validated domain; routing pre-declared (§7).
- **TUNED** — I excludes δ = 0 and meets the unwidened reach (a banked texture inside D) on at least one elected (key, arm): a texture of stated non-zero strength would be required. Never a confirmation of texture; never a promotion.
- **MARGIN-ONLY** — I excludes δ = 0, misses every unwidened reach, and meets some widened reach only inside the margin: unresolved at this gate's resolution (the third-order successor's territory); neither a kill nor a required texture. KILL-IN-D, TUNED and MARGIN-ONLY together exhaust the intervals excluding 0.
- **WINDOW-DELIVERED** — I contains δ = 0 and every primary key is BINDING on t₄: the constraint curve on the texture import is delivered, per key and as the σ-union.
- **INERT-IN-D** — I contains δ = 0 and at least one primary key is INERT-IN-D on t₄ (the conservative union reaches D).

**Not predicted.** Which of the last six classes the sealed anchor produces is not predicted and not consulted by any instrument; it depends on a budget this memo has not seen (D-SA-0 states what the chat leg nonetheless knows). The only pre-registered content is structural (§8).

## 2. Inherited definitions, each re-derived in the new context (rule 3)

| # | Inherited definition (source) | One-line re-derivation here | Carry status |
|---|---|---|---|
| D-1 | r_agg = ⟨v⟩_S2/⟨v⟩_EM − 1, ⟨v⟩_X = Σ_b∫dΩ w_X v / Σ_b∫dΩ w_X (G-MSCS1 §2.5) | a ratio of two descriptor-weighted k̂-sphere means; a one-sightline anchor measures its restriction Δ(k̂) = v_S2(k̂)/v_EM(k̂) − 1, which depends on ψ = ∠(k̂, ẑ) and vanishes at ψ = 0 (S-SA-1) | **CARRIES ONLY UNDER I-SA-1** (E-SA-3(a), elected) |
| D-2 | species ↔ carriers: EM = CI-W/EM-IN helicity-±1 content; S2 = the E₂ content of the transverse phonon (E-MS-1(a)) | the anchor's tensor messenger is read as the S2 descriptor, its EM messenger as the EM descriptor, so δ ≡ v_tensor/v_EM − 1 ↔ r_agg with the same sign | CARRIES (R2 identification, inherited) |
| D-3 | t₂: w = 1 + t₂P₂(n̂·ẑ), positivity [−1, 2] (G-MSCS1 A-1.4) | the P₂ coefficient of the fiber marginal of the grain descriptor axis; on fcc its octahedral orbit average is zero (D-8) | CARRIES; the mapped domain is D₂, not the positivity range (D-12) |
| D-4 | t₄: hex 1 + t₄P₄ (positivity [−1, 7/3]); cubic 1 + t₄K̃₄ (positivity [−1, 3/2]) (G-MSCS2 §2.5) | the l = 4 fiber coefficient in two normalizations (S-SA-3) | CARRIES per branch; cross-branch only through σ (E-SA-5) |
| D-5 | κ of record = the 3-term fit over the inclusive window \|t\| ≤ 0.25 (G-MSCS1 A-2.4; G-MSCS2 A-2.3 + H-CC-1) | a basis-dependent estimate of ½r″(0); the basis-independent value differs by the fit resolution of S-SA-4 | CARRIES with its resolution serialized (E-SA-6) |
| D-6 | quadratic form κ₂₂t₂² + κ₂₄t₂t₄ + κ₄₄t₄² on the 5 × 5 grid; κ₂₄ = 0 (A-3.2) | S2-E₂: indefinite on hex (null rays, S-SA-2), degenerate on fcc (κ₂₂ = 0); S2-h hex: negative-definite under the diagonal form | CARRIES; the diagonal form is licensed by the N-2 null on every key |
| D-7 | first-order protection S = 0 (F-MS-3 / F-MS2-3) | the odd part of r in t vanishes, so the mapping carries no linear term; basis-independent odd-part estimates ≤ 2.2×10⁻¹² (S2-E₂ Hill), ≤ 2.6×10⁻¹³ (HS-mean), ≤ 1.3×10⁻¹² (S2-h) | CARRIES (null N-1 on every arm) |
| D-8 | the cubic l = 2 null (F-CTRL-L2NULL; A-3.3) | reading (ii): no l = 2 term at any order (the octahedral group has no l = 2 invariant); reading (i): null to second order, t₂t₄² at third (S-SA-8) | CARRIES at second order under both readings, each stated (rule 1) |
| D-9 | Hill primary, HS-mean reported (A-2.4) | two aggregate schemes; HS-mean/Hill − 1 = −0.32% (hex κ₄₄), −0.78% / −0.55% (hex κ₂), +3.98% / +6.11% (fcc κ₄₄) | CARRIES (robustness arm) |
| D-10 | cubic descriptor axis ⟨001⟩ primary, ⟨111⟩ reported (E-MS-2c) | for S2-E₂ the two axes give the fcc split opposite signs, so they bind on opposite ends of a two-sided anchor (S-SA-5) | CARRIES; a kill must hold on both (E-SA-9) |
| D-11 | hex arms (a) tetragonal-form / (b) symmetrized (E-MS-2b) | two tensor forms of the same stacking; coefficients within 1.1×10⁻³ relative (S2-h κ₂ the largest; ≤ 6.0×10⁻⁵ for κ₄₄ on the S2-E₂ arms) | CARRIES (robustness arm) |
| D-12 | positivity ranges as the texture domain | positivity bounds the ODF; the second-order surface is validated only on the fit window (primary-arm truncation at its edge ≤ 2.2×10⁻³, computed — E-v2-1) | **NEW: D := the fit window, \|t\| ≤ 0.25 per family** (E-SA-10(a), elected) |
| D-13 | leading-order long-wavelength aggregate; no Born (E-MS2-3(a)) | valid for a messenger only if k·d ≪ 1 on its band; d is an import | CARRIES UNDER E-SA-4 |
| D-14 | τ_agg = 1×10⁻⁶ on r; κ floor 1×10⁻⁶ (G-MSCS1/2 tolerances; the v1.1 delta) | the resolutions at which r and κ are resolved two-leg in this family | CARRIES as the null tolerances (rule 2) |
| D-15 | the 12-point t-grid and its fit windows (G-MSCS1 lock record §6; A-2.4) | counts computed: 12 points; \|t\| ≤ 0.25 holds 9 inclusive / 7 strict; \|t\| ≤ 0.1 holds 7 inclusive / 5 strict; the inclusive counts are the ones both legs used | CARRIES (rule 4) |
| D-16 | the T1 base `05302210` + the G-MSCS1 stratum (E-MS2-7) | the stratum already covers the digit strings and identifiers of the registered anchor dialect | CARRIES; an author-supplied A1 is added (E-SA-7) |
| D-17 | "a sealed-anchor comparison of κ₂t² against the 2017 multi-messenger tensor-speed bound" (G-MSCS1 §5 (iii)) | a two-sided interval on δ at a stated confidence, from one sightline, over two bands | **NEW: the `spd` row of §4** |
| D-18 | S2-h: w_S2h = (1 − λ_L)/(1 + λ_L/3) (G-MSCS1 §2.3′) | the admixture-controlled descriptor; every S2-h coefficient is negative, so it binds on lo everywhere and reaches no positive δ | CARRIES (robustness arm) |
| D-19 | b₁ = d/dt₄[(v_qSH − v_qSV)/v_T] at t₄ = 0, propagation ⊥ fiber, Hill (G-MSCS2 A-2.7) | the ψ = 90° first-order polarization split per unit t₄; a different observable from the species split (S-SA-6) | CARRIES as a reported quantity; not mapped (E-SA-1) |
| D-20 | W^EM_∪ = (0, 3.7641664288e-33] SI length units (G-CI1; in v2 read by key from the CC r2 checkpoint `845ae6be`, §9) | the floor-adjoining component of record; a far component beyond 1.0813e+25 is VOID | CARRIES UNDER E-SA-4 (the regime scale) |
| D-21 | KD_CLIP = 0.3 and the E-11 rule "a VOID can only widen a window" (G-POLY1 / G-S2C1-W) | the long-wavelength envelope, applied here to the messenger bands | CARRIES (E-SA-4(a)) |
| D-22 | 0.10 — the ratified D-W-5 default threshold for the Δ₄ dressing diagnostic (G-S2C1-W) | reused as the truncation-flag threshold and as the reach margin μ | CARRIES (E-SA-11) |
| D-23 | the frozen P3-A1 reading-token list {bound, ceiling, margin, criterion} (G-POLY1) | only `bound` is a conformant reading for this gate | CARRIES (§4.3) |
| D-24 | the ODF-averaged per-grain E₂ weight: the S² average of frac_E2(n̂) with the fiber marginal (G-MSCS2 A-2.5) | invariant under rotations about the fiber axis — the source of ST-1 | CARRIES |

## 3. The mapper (the whole computation; nothing else is computed)

**3.1 Inputs.** The mapper reads `pinned_inputs_G_MSCS_A.json` (md5 `2d44ec01…`, 96,761 B), generated **before lock** by `sa_build_pinned_inputs.py` (md5 `8189100e…`) and verified by the author before lock (§9; the order the author set on September 29).
- **Sources.** Seven banked sources, all on `main`, each guarded by its full md5 and byte count: G-MSCS2 chat `1c5b6b59` / CC `9961745d`; G-MSCS1 chat `c04c0b8e` / CC `249e11dd`; `diag_kappa24.json` `b7952dfc`; `diag_quadform_basis.json` `d84aa1fd`; and the G-CI1 CC r2 checkpoint `845ae6be` for the regime scale. Every value is read by NAMED KEY, through one RFC 6901 pointer per field recorded in the file's `provenance` block.
- **`raw`, per key, arm and family:** the κ of record and its CC counterpart; the banked 12-point grid; the banked first-order slope S, where banked, with its CC counterpart; the cubic coefficient, on the S2-E₂ Hill arm, with its CC counterpart.
- **`raw`, per key:** the quadratic form, the CC 5 × 5 grid and the discarded cubic terms, the κ₂₄ diagnostics, and b₁ with its CC counterpart; on fcc, also the l = 2 identity change and the A-3.1 mixed change.
- **`raw`, global:** the W^EM_∪ edge.
- **The rest of the file:** `constants`, `grids` (generators only), `tokens`, `structure`, and `derived` — reference values that are a pure function of the rest: the basis-independent κ, the fit resolutions, the reachable sets and their unions, the pinned synthetic intervals of Phase 2, the null estimators, the null-ray slopes and the derived constants. No point count is written (rule 4).

The cubic coefficients (κ₃, κ₄₄₄), the quadratic form and the 5 × 5 grid are banked for the S2-E₂ Hill arm only. So the truncation flag and F-CTRL-SA-RECON are defined on that arm, and the robustness arms rest on their banked grids. **The sealed file is the only other input.**

**3.2 Rows.** The sealed file must conform to §4 in full; a non-conformant file aborts masked before any mapping, emitting a reason code only. **New rule of this gate:** such an abort does not spend the read — the F-W-CENSUS precedent covered only aborts before parsing, and this extends it to a grammar failure found by parsing, because nothing is mapped and no value is emitted; the author re-issues the file under §4.8's before-read revision rule. For each row: I_j = [lo_j, hi_j]; the regime clause (E-SA-4(a)): x = max(k_em_max, k_t_max) × d_EM, d_EM the W^EM_∪ upper edge; x > KD_CLIP → the row is VOID-REGIME (a VOID can only widen). **The combined interval I = ∩_j I_j over non-VOID rows is mapped** (the mapping is monotone in I, so mapping the intersection equals intersecting the mapped sets); if the intersection is empty the gate is ANCHOR-INCONSISTENT. Per-row mappings are serialized for the record.

**3.3 One-parameter windows (I ∋ 0).** For each key K and family F (t₄ on every key; t₂ on hex keys; t₂ on cubic keys is the null family) with coefficient κ of record and D_F = 0.25:
- null family: NULL-INERT (window = D).
- binding end b = hi if κ > 0, lo if κ < 0 (S-SA-5); t\* = √(b/κ) (b/κ ≥ 0 by construction; t\* = 0 if b = 0); t\* < D_F → BINDING, window [−t\*, t\*]; else INERT-IN-D.
- the same with the basis-independent κ; a class difference → RESOLUTION-SENSITIVE (class of record from κ of record).
- truncation (S2-E₂ Hill arm): T = |κ₃|·t\*/|κ| with κ₃ the cubic coefficient of the same fit; T > 0.10 → TRUNCATION-SENSITIVE. Inside D, T ≤ 2.2×10⁻³ on every key (maximum 2.11×10⁻³, cubic_gem8; computed): expected never to fire.
- null floor: ν = |S_bi|·t\*/|b| with S_bi the basis-independent first-order estimate; ν > 0.10 → NULL-FLOOR-SENSITIVE (a very tight budget brings the edge to where the banked numerical floor of the first-order null can no longer confirm it independently; the edge of record rests on the algebraic S = 0 of first-order protection). At b = 0 (t\* = 0) ν is defined as +∞: the flag is set, and the window {0} rests entirely on the algebraic null.
- σ-edge: σ\* = t\*·rms_F (rms 1/3 hex P₄, √(4/21) cubic K̃₄, √(1/5) P₂).

**3.4 The two-parameter region (reported, no class).** Hex keys, diagonal form (licensed by N-2): A₂₄ = {(t₂, t₄) ∈ D × D : κ₂₂t₂² + κ₄₄t₄² ∈ I}. Serialized per arm: the axis windows, the null-ray slope (S2-E₂) or definiteness (S2-h), the admissible area fraction on the pinned area grid (generator: 201 × 201 uniform nodes on D × D; the count is computed), and a compactness flag. Cubic keys: the strip {|t₄| ≤ t₄\*} × D₂. The banked third-order cross terms are serialized and not mapped: hex t₂²t₄ = −7.28×10⁻⁶ / −9.83×10⁻⁶ and t₂t₄² = −3.94×10⁻⁶ / −3.58×10⁻⁶ (step / gem8); fcc reading (i) t₂t₄² = −5.90×10⁻⁵ / −8.51×10⁻⁵.

**3.5 Intervals excluding 0.** Per key and arm on the key's whole texture domain D × D (on fcc the t₂ direction enters only through the reading-(i) third-order content of the 5 × 5 grid): EXCLUDED-IN-D iff I ∩ R^w_{K,arm} = ∅ — sub-reason SIGN if R^w lies wholly on the other side of 0 from I, else MAGNITUDE; TUNED-ADMISSIBLE iff I ∩ R^h_{K,arm} ≠ ∅; otherwise MARGIN. The one-parameter requirements are serialized for information: for each family with κ of δ's sign, the annulus [t_in, min(t_out, D_F)] with t_in = √(min(|lo|, |hi|)/|κ|), t_out = √(max(|lo|, |hi|)/|κ|); a family whose t_in > D_F cannot supply δ alone.

**3.6 The reachable sets R^h and R^w.** For each key and arm, R^h is the hull of (i) the second-order box range [Σ_F min(0, κ_F D_F²), Σ_F max(0, κ_F D_F²)] over the mapped families F of §3.3 (t₄ on every key; t₂ on hex keys only — the fcc t₂ null family is excluded) and (ii) every banked grid value inside D of those families for that key and arm (the one-parameter grids; the CC 5 × 5 (t₂, t₄) grid on the S2-E₂ Hill arm only, reading (i) on fcc — the wider reading), with any endpoint within 1×10⁻¹² of zero set to 0; R^w = (1 + μ)·R^h, μ = 0.10, on every arm (E-SA-11). The values are the §0 reach table (R^w) and its footnote (the R^h unions) — `derived.reach` and `derived.unions` of the pinned file. Diagonality is banked two-leg for S2-E₂ Hill; for HS-mean and S2-h it is taken from the same harmonic-orthogonality reading (§2.91.S, R2) and flagged `diag_assumed`; μ covers their unbanked cross terms (the banked S2-E₂ excess over the box is ≤ 7.5%).

**3.7 Gate level (E-SA-5(a)).** Primary arm: S2-E₂, Hill, hex (a), cubic ⟨001⟩, the four configurations. The t₄ gate window in σ: [0, max_K σ₄\*_K] — the widest (CONSERVATIVE, the W_∪ lineage) — with any INERT-IN-D primary key making the gate INERT-IN-D (no gate-level exclusion is claimed beyond a key's validated domain); the strict intersection serialized, non-verdict. The gate-level t₂ window is INERT for any I ∋ 0 by the fcc null (ST-3); hex t₂ windows are delivered per branch. Robustness arms (HS-mean, S2-h, hex (b), cubic ⟨111⟩) are serialized for every quantity.

**3.8 OOM robustness.** Every row's lo and hi scaled ×10 and ×0.1. The *unclipped* raw edges of non-null families (t\*, t_in, t_out) must scale by exactly √10 / √0.1; clipped windows (INERT-IN-D, NULL-INERT, a TUNED outer edge at D) and the classes are checked for monotonicity only (×10 never narrows, ×0.1 never widens). The gate class is OOM-ROBUST iff identical under both scalings.

## 4. The sealed anchor file — exact format and parameters (the author's deliverable)

**4.1 Name and encoding.** `anchors_G_MSCS_A_SEALED.md` (the name follows E-SA-0). UTF-8; LF line endings only; **no control character anywhere except the row-ending LF** (no C0 control such as CR, TAB, form feed or NUL; no DEL; no C1 control such as NEL), no U+FEFF anywhere (a BOM included), and no Unicode line or paragraph separator; **one anchor row per line and nothing else** — no header, no comment, no blank line, no BEGIN/END marker inside the file (markers belong to the armor); the file ends with exactly one LF after the last row.

**4.2 Row grammar.** `key=value | key=value | … | key=value` — the separator is exactly space-bar-space; no leading or trailing bar; no bar anywhere else in the row (the H-16 guard); the first `=` in a field separates key from value; values carry no leading or trailing space. Keys appear in the canonical order below: the eleven required keys, then optional keys in their order. Row ids are SA-1, SA-2, … in file order.

**4.3 Required keys (every row).**

| key | value | meaning |
|---|---|---|
| `id` | `SA-n` | row n in file order |
| `class` | `spd` | a species-speed interval (the only class this gate reads) |
| `delta_def` | `tensor_over_EM_minus_1` | δ ≡ v_tensor/v_EM − 1; δ > 0 means the tensor messenger is faster. A source quoting (v_EM − v_tensor)/v_EM is entered negated with its ends swapped |
| `lo` | number | lower end of the admissible interval of δ (dimensionless; may be negative) |
| `hi` | number | upper end; lo ≤ hi. A source quoting \|δ\| ≤ B is entered lo = −B, hi = +B |
| `cl` | number in (0, 1), or `hard` | the interval's confidence level (two-sided 90% → 0.9); `hard` for a deterministic bound; serialized, not used |
| `reading` | `bound` | the only conformant token of the frozen P3-A1 list {bound, ceiling, margin, criterion} |
| `geom` | `single` or `population` | one source along one sightline, or a statement averaged over many sightlines (serialized; informs E-SA-3) |
| `k_em_max` | positive number | the largest angular wavenumber k = 2π/λ of the EM band the anchor's timing uses, in m⁻¹ (for the regime clause) |
| `k_t_max` | positive number | the same for the tensor messenger's band, in m⁻¹ |
| `src` | free text | the source; never parsed, never echoed; hashed into the row md5 and masked in every output |

**Optional keys:** `q` = `phase` or `group` (serialized; the leading-order surface is non-dispersive, so it is not used); `note` = free text (never echoed).

**What the LSF-δ read of the dialect fixes for the entry (L-SA-1).** These are custody rules for the author's file: the validator cannot see them, and no value is quoted.
1. `delta_def` — the primary counterpart-timing statement defines the fractional difference as (tensor speed − EM speed)/EM speed, positive when the tensor messenger is faster. That is δ as defined here, so it is entered unchanged (no negation, no swap).
2. `lo`, `hi` — enter the primary statement's own two ends. Its interval is two-sided and asymmetric, each end set by a stated emission-delay assumption. A secondary restatement as a symmetric magnitude bound drops the sign structure that S-SA-5 makes load-bearing (S-SA-12).
3. `cl` — the primary statement frames its interval as conservative and states no separate confidence level for it. The entry is the author's (`hard` is admissible); it is serialized and never used.
4. `geom` — one source, one sightline: `single`.
5. `q` — the same source's coefficient subsection speaks of relative group velocity. The leading-order surface is nondispersive, so `q` is serialized and never used.
6. `k_em_max`, `k_t_max` — the photon side is stated as energies, and the tensor side is dated by its signal peak with no band stated. The author supplies both (the conversion is done outside the gate). Under E-SA-4(a) the clause fires only above 7.96×10³¹ m⁻¹.
7. **Only counterpart-timing statements are `spd` rows.** Detector-network and catalog intervals, and one-sided Cherenkov bounds, are different ratios and are not entered (S-SA-11).

**4.4 Numbers.** ASCII decimal or e-notation only, matching `[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?` and finite: `-2.5e-3`, `0.0004`, `1e2`. **Not accepted:** the Unicode minus sign, superscript digits, the multiplication sign or a caret power form, percent signs, thousands separators, a unit inside a value. Every field except `src` and `note` is printable ASCII (this stops the E3-6 superscript class and the H-19 lexer class at the door). The conversion of a frequency or photon energy into k is the author's, done outside the gate — no conversion constant enters any instrument.

**4.5 Template (placeholders, not values):**
`id=SA-1 | class=spd | delta_def=tensor_over_EM_minus_1 | lo=<number> | hi=<number> | cl=<number or hard> | reading=bound | geom=<single or population> | k_em_max=<number> | k_t_max=<number> | src=<free text>`

**4.6 Delivered with the file (author).**
1. **The file, so that its content never appears in the clear in the conversation:** zipped or base64-armored as an attachment, or committed armored to the repository on a branch named in the directive. Never pasted into a directive, and never as a plain `.md` or `.txt` attachment — those are displayed to the chat leg (the H-W-2 exposure). The chat mapper is frozen before delivery, so an exposure could not tune anything; what it would cost is the chat read's blind status, already carried by CC-BLIND-FIRST.
2. The md5 and byte count of the unarmored file, stated in the directive.
3. The intended census (N rows, all `spd`).
4. **T1-A1** `t1_forbidden_G_MSCS_A_A1.txt`: the numeric part built by `sa_t1a1_build.py` on the author's side (it refuses a file that fails the validator; it writes every plausible rendering of every number in lo, hi, k_em_max and k_t_max — signed and unsigned, integer form, padded, unpadded and three-digit exponents, upper- and lower-case e, up to two extra trailing zeros, the caret forms, the house superscript form with ASCII and Unicode minus — prints only the count and the md5, and drops renderings shorter than four characters), then every catalog, event, collaboration or instrument identifier in `src`, appended by hand (four characters or more each); UTF-8, LF, no BOM, no TAB, no padded line; its md5 and byte count stated; delivered the same way as the sealed file.
5. *(Moved in v2.)* The author's word that the pinned-inputs file is verified is given **before lock** and recorded in the lock record (§5 step 2); nothing is needed here at sealed delivery.

**Pre-freeze collision scan (S-SA-10).** Before T1-A1 is frozen, the chat leg scans every locked artifact (memo, lock record, pinned inputs, mapper, schema, comparator) under A1. A hit means a pattern is too generic for this gate; the author resolves it before the freeze (logged as a D-item). After the freeze F-CTRL-SA-T1 has no override.

**4.7 Validator.** `sa_anchor_validate.py` checks 4.1–4.4 and T1-A1's form and is blind by construction: it prints md5, byte count, census, key order and a reason code per key — never a value. Run by the author before sealing; run by the chat leg only to confirm the census at dispatch build (census printed, nothing else read). Tested on two valid and fifteen malformed synthetic files (CRLF, BOM, trailing blank line, form feed and U+2028 inside `src`, Unicode minus, superscript form, a bar inside `src`, lo > hi, `reading=ceiling`, wrong `delta_def`, missing key, wrong id, duplicate key, percent-form `cl`) and a malformed T1-A1 (BOM, TAB, padded line): every malformed file failed with its reason code, and a fixed-string search found no synthetic value in any output. The builder refused a malformed file without printing anything from it; its renderings were each caught by scanner `6b862900` across fifteen rendering forms (integer, three-digit exponent and extra-zero forms included), and unrelated numbers scanned clean.

**4.8 Custody.** The chat leg verifies md5, byte count and census, and carries the armored file into the dispatch (P-4.b); it does not decode it for any other purpose before its own read. The sealed md5, census and per-row md5s are asserted at every open. **No checkpoint, log or report carries lo, hi, k_em_max, k_t_max or src verbatim** — only the file and row md5s and derived quantities (windows, classes); two legs that parsed the same bytes identically agree on both. A revision of the sealed file before the CC read is a new md5 and a lock-record addendum (the read not spent); after any read it is a new gate cycle (this reconciles the two G-S2C1-W statements of Q-W-1).

## 5. Execution leg

**Phase 0 — pins and controls (halt-on-fail; INDETERMINATE on any failure; every record carries its `odf_reading` token, §6.2).**
- **F-CTRL-SA-PIN** [`none` — identity of inputs] — the pinned-inputs md5 equals the lock-record md5; every pinned value re-read from its source by named key at run time equals the pinned value bit-for-bit (this, not RECON, is what guards a key or arm swap); the chat and CC banked coefficients agree: κ and κ₃ ≤ 1×10⁻⁴ relative (the banked κ tolerance, applied to κ₃ as well); b₁ ≤ 1×10⁻⁴ relative (this gate's choice; G-MSCS2's comparator banked b₁ at 1×10⁻⁶ absolute, which the observed agreement also meets); S ≤ τ_agg absolute. Observed: κ ≤ 2.1×10⁻¹¹ on S2-E₂ κ₄₄ and ≤ 1.2×10⁻⁹ over every κ compared (S2-h κ₂ the largest; E-v2-2); κ₃ ≤ 2.1×10⁻⁷; b₁ ≤ 6.5×10⁻¹³; S ≤ 2.8×10⁻¹⁵ (the CC counterparts of κ₃, S and b₁ are pinned in v2).
- **F-CTRL-SA-PIN-DERIVED** [`none` — identity of derivation; new in v2] — each leg re-derives, from the pinned file's `raw`, `constants` and `grids` and with its own code, the blocks of `derived` that this memo defines: `families`, `reach`, `unions`, `synthetic`, `nulls`, `hex_quadform` and `zero_ctrl` (§3.3–§3.6, §5, §6.2). It must match every value within |Δ| ≤ 1×10⁻¹²·|x| + 1×10⁻¹⁶. `derived.summary` holds the maxima this memo quotes; the independent verifier reproduces it, and the legs are not required to. A miss halts the run (INDETERMINATE), and the S9 decides whether the leg or the builder is at fault.
- **F-CTRL-SA-ZERO** [`uniform`: the untextured SO(3)-uniform ODF, t₂ = t₄ = 0] — the banked r_agg at t = 0 is ≤ 1×10⁻¹² in absolute value on every key, arm and family (observed ≤ 3.4×10⁻¹⁶): the identity point of the surface.
- **F-CTRL-SA-RECON** [`hexP4` / `cubK4` for t₄; `hexP2` for t₂] — on the S2-E₂ Hill arm, the 3-term form S·t + κt² + κ₃t³ reproduces the banked grid inside D to ≤ 1×10⁻⁸ absolute (observed maxima 6.85×10⁻¹⁰ for t₄, 1.41×10⁻¹⁰ for t₂). On the robustness arms, whose cubic coefficients are not banked: the pinned κ must agree with the basis-independent κ of the same arm's banked grid to ≤ 1×10⁻³ relative (the largest fit resolution on any arm is 7.3×10⁻⁴, on S2-h; 2.3×10⁻⁵ on HS-mean). Detection power, stated honestly: on the Hill arm a mis-read coefficient is caught when it is off by more than about 1.6×10⁻⁷ absolute (about 0.1% relative); on the robustness arms when it is off by more than about 0.1% relative; an arm (a)↔(b) swap is below both for κ₄₄ (≤ 6.0×10⁻⁵ relative) and is guarded there by F-CTRL-SA-PIN, while for κ₂ (≤ 5.3×10⁻⁴ relative) the Hill RECON also catches it (residuals of 3.0–4.8×10⁻⁸ at t = 0.25; E-v2-6).
- **F-CTRL-SA-S** (null N-1) [`hexP2`, `hexP4`, `cubK4` per family] — the basis-independent first-order slope ≤ τ_agg on every key, arm and family.
- **F-CTRL-SA-K24** (null N-2) [`hexP2P4` on hex; `cubP2K4-i` on fcc] — κ₂₄ basis-independent ≤ the κ floor on all eight keys (every key from the chat diagnostic, the CC checkpoint and this gate's own mixed difference on the CC 5 × 5 grid — E-v2-4); failure halts (INDETERMINATE), with no fallback.
- **F-CTRL-SA-L2NULL** (nulls N-3, N-4) — [`cubP2-ii`] the octahedrally symmetrized l = 2 perturbation is identically zero (the octahedral group has no l = 2 invariant; for ⟨001⟩ this is Σᵢ P₂(êᵢ·ẑ) = 0), so r_agg is unchanged by t₂ at every order — an identity, asserted symbolically; [`cubP2-i`, `cubP2K4-i`] the fcc κ₂ and the quadratic-form κ₂₂ are ≤ the κ floor (fit and basis-independent), r_agg unchanged by t₂ alone (≤ 1×10⁻¹² at t₂ = 1, banked), and the third-order t₂t₄² term serialized, not asserted null.
- **F-CTRL-SA-SIGN** [`none`] — asymmetric synthetic intervals: the binding end must be hi for κ > 0 and lo for κ < 0 on every key, arm and family.
- **F-CTRL-SA-GRID** [`none`] (rule 4) — every point count in the checkpoint recomputed from the generators.
- **F-CTRL-SA-MONO** [`none`] — §3.8: exact √10 scaling of the unclipped raw edges of non-null families (relative 1×10⁻¹⁴); monotonicity of clipped windows and classes; a violation halts the run as an instrument defect (S9 class), never a finding.
- **F-CTRL-SA-MASK** [`none`] — the sealed file is opened only in Phase 3; md5, byte count and census asserted at every open; a parse defect aborts masked (reason code only); no sealed value reaches stdout, a log or any artifact; `src` never echoed.
- **F-CTRL-SA-T1** [`none`] — T1 self-scan of the instrument, this memo, the pinned inputs and the checkpoint under base ∪ G-MSCS1 stratum ∪ A1; halt on any hit, no override.

**Preflight (build time; not a gate result).** The builder evaluates every Phase-0 criterion that depends on pinned values only, and refuses to write the file on any failure. All pass:

| criterion | observed | limit |
|---|---|---|
| two-leg κ; quadratic-form κ₂₂ | ≤ 1.2×10⁻⁹; ≤ 1.2×10⁻¹² (relative) | 1×10⁻⁴ |
| two-leg cubic coefficient κ₃; b₁ | ≤ 2.1×10⁻⁷; ≤ 6.5×10⁻¹³ (relative) | 1×10⁻⁴ |
| two-leg first-order slope S | ≤ 2.8×10⁻¹⁵ (absolute) | τ_agg = 1×10⁻⁶ |
| r(0) | ≤ 3.4×10⁻¹⁶ | 1×10⁻¹² |
| RECON, S2-E₂ Hill | 6.85×10⁻¹⁰ (t₄); 1.41×10⁻¹⁰ (t₂) | 1×10⁻⁸ |
| robustness arms, κ of record vs basis-independent | ≤ 7.3×10⁻⁴ (the tightest margin, a factor of about 1.4, on S2-h) | 1×10⁻³ |
| N-1 | ≤ 2.2×10⁻¹² (bi); ≤ 4.3×10⁻¹¹ (fit) | 1×10⁻⁶ |
| N-2 | ≤ 3.5×10⁻⁷ (the fcc fit7); every basis-independent estimator ≤ 9.5×10⁻¹¹ | 1×10⁻⁶ |
| N-3 | ≤ 1.3×10⁻¹³ | 1×10⁻⁶ |
| N-4 | ≤ 8.0×10⁻⁹ (fit7); ≤ 1.1×10⁻¹⁴ (bi, k12) | 1×10⁻⁶ |
| t₂ alone at t₂ = 1 | ≤ 3.4×10⁻¹⁶ | 1×10⁻¹² |

The legs repeat all of them at Phase 0 with their own code.

**Phase 2 — pre-read suites (synthetic anchors only; all green before any sealed open).** The synthetic generators are pinned (`constants.synthetic_t`, `synthetic_t_tight`, `synthetic_band_fractions`, `synthetic_k`; `derived.synthetic`). Budgets are b = |κ|·t_syn² with t_syn ∈ {0.01, 0.1, 0.5}, so every expected edge is exact by construction and no synthetic value resembles an observation; every suite uses k_em_max = k_t_max = `synthetic_k.silent` (1 m⁻¹) except C-SYN-10: C-SYN-1 symmetric interval ∋ 0; C-SYN-2 asymmetric interval ∋ 0 (binding end); C-SYN-3 intervals excluding 0 on either side (SIGN, MAGNITUDE, TUNED-ADMISSIBLE, including the pinned interval `derived.synthetic.robustness_only_positive`, the middle half of the band between the primary union and the all-arm hull, reachable only on a robustness arm); C-SYN-4 a wide interval (INERT-IN-D everywhere); C-SYN-5 the fcc t₂ null; C-SYN-6 the malformed-file set of §4.7 (masked abort, reason code, no value); C-SYN-7 OOM (exact scaling unclipped, monotone clipped); C-SYN-8 two consistent rows (intersection); C-SYN-9 two disjoint rows (ANCHOR-INCONSISTENT); C-SYN-10 the regime clause at k = `synthetic_k.void` (1×10³³ m⁻¹; VOID-REGIME); C-SYN-11 lo = hi = 0 (t\* = 0, NULL-FLOOR-SENSITIVE by definition); C-SYN-12 a very tight budget, t_syn = `synthetic_t_tight` = 1×10⁻⁹ (NULL-FLOOR-SENSITIVE wherever the pinned S_bi makes ν > 0.1. At this budget the flag fires on some mapped cells and not on others: most non-firing cells have 0 < ν < 0.1, and one has S_bi exactly 0. Both branches of the flag are therefore exercised, and the expected flags follow from the pinned S_bi); C-SYN-13 the pinned MARGIN-band intervals `derived.synthetic.margin_positive` and `margin_negative`, the middle half of each band (MARGIN, gate MARGIN-ONLY); C-SYN-14 grid noise at zero (a zero-snapped endpoint never turns SIGN into MAGNITUDE).

**Phase 3 — the read (CC-BLIND-FIRST, E-SA-8(a)).** CC decodes the armored sealed file from the dispatch and maps it with its own parser, binder and class logic on the same pinned inputs; it commits a pre-consultation checkpoint before opening any chat artifact — the CC read is the read of record for the class. The chat leg then reads with its frozen mapper. The comparison runs last, with the comparator frozen before either read.

**Order of operations (binding once locked; amended in v2 at the author's direction).**
1. memo v1 → the author's elections → **v2** (elections applied; LSF-δ executed; the pinned-inputs file generated and its md5 stated).
2. **The author regenerates and verifies the pinned-inputs file (§9)**; and the Rodgers preprint is read in full (L-SA-5; §15 item 8).
3. **Lock — one event, on the author's word "Lock"** (the G-MSCS2 pattern):
   - the memo md5;
   - the T1 gate list composed and frozen;
   - schema v1.0 + comparator v1.0 written, self-tested and frozen;
   - the lock record with Addendum A-2, citing the md5s of the memo, the pinned inputs, the builder, the verifier, the T1 list, the schema and the comparator, and recording the author's verification of the pinned inputs.
4. The chat mapper written, the pre-read suites green, the mapper md5 frozen.
5. **The author supplies the sealed file + T1-A1** (§4.6).
6. The chat leg confirms md5, bytes and census; the A1 pre-freeze collision scan; A1 frozen.
7. The dispatch built (P-4; P-4.b with the sealed file armored; P-4.c, delivered alone).
8. CC blind read → chat read → two-leg comparison → S9 on misses.
9. Fold authorization → V4.87, which also carries H-MS2-9 unless an earlier fold does.

This improves on the G-S2C1-W order, where the sealed row arrived in the clear before the chat instrument existed (H-W-2; Addendum 1 items 3–6). It also improves on v1's order, where the pinned inputs were verified only after lock.

## 6. Schema and comparator (rules 1, 2, 4, 5 encoded)

**6.1 Identity and custody keys.** memo md5; lock-record md5; pinned-inputs md5, builder md5 and verifier md5; T1 list md5 + A1 md5 + scanner md5; sealed md5, bytes, census {rows, per_class, fields_per_row}; per-row md5; elections; each leg's mapper md5. No anchor value (§4.8).

**6.2 Nulls — each with a fit key and a basis-independent key, both compared at the resolution of the quantity, each carrying its `odf_reading` token (rules 1, 2, 5).** The closed token set names each ODF once: `none` (no ODF involved); `uniform`; `hexP2` (1 + t₂P₂(ĉ·ẑ)); `hexP4` (1 + t₄P₄(ĉ·ẑ)); `hexP2P4` (both); `cubK4` (1 + t₄K̃₄); `cubP2-i` (the inherited single descriptor-axis P₂ on a cubic grain — G-MSCS1's cubic l = 2 family); `cubP2-ii` (the octahedrally symmetrized P₂, identically zero); `cubP2K4-i`; `cubP2K4-ii`.
- **N-1 first-order slope** (every key × arm × family): `fit` = the banked S where banked (S2-E₂ Hill and S2-h), tolerance τ_agg = 1×10⁻⁶; `bi` = the Richardson odd part [4·O(0.05) − O(0.1)]/3, O(h) = [r(h) − r(−h)]/(2h) on the banked grid, tolerance τ_agg. Observed `bi` ≤ 2.2×10⁻¹² (S2-E₂ Hill), ≤ 2.6×10⁻¹³ (HS-mean), ≤ 1.3×10⁻¹² (S2-h); `fit` ≤ 4.3×10⁻¹¹.
- **N-2 κ₂₄** (all eight keys): `fit7` (tolerance the κ floor 1×10⁻⁶ — at the 7-term fit's resolution, where its aliased values 1.2–1.9×10⁻⁸ on hex and 1.9–3.5×10⁻⁷ on fcc pass); `bi` = the Richardson mixed second difference — the chat diagnostic, the CC in-checkpoint value, and this gate's own from the CC 5 × 5 grid on every key; tolerance the κ floor. Observed ≤ 1.4×10⁻¹² (hex, all three), ≤ 2.3×10⁻¹² (fcc, chat and CC), ≤ 9.5×10⁻¹¹ (fcc, the 5 × 5 estimate — the O(h⁴) remainder at the coarser (0.125, 0.25) pair: sixth-order odd–odd content of the reading-(i) grid; the pair cancels the quartic term exactly).
- **N-3 κ₂ on fcc** [`cubP2-i`; the `cubP2-ii` identity clause of F-CTRL-SA-L2NULL]: `fit` (G-MSCS1 fit, ≤ 3.2×10⁻¹⁵) and `bi` (Richardson even part of the G-MSCS1 grid, ≤ 1.3×10⁻¹³); tolerance the κ floor.
- **N-4 κ₂₂ of the fcc quadratic form** [`cubP2K4-i`]: `fit7` (4.5×10⁻⁹ / −3.0×10⁻⁹ / 8.0×10⁻⁹ / −5.3×10⁻⁹ — the t₄⁴ aliasing of the G-MSCS2 S9) and `bi` (the Richardson even part along t₂ of the CC 5 × 5 grid: 0 / 0 / −8.9×10⁻¹⁵ / 1.1×10⁻¹⁴; the chat quartic-inclusive refit −9.1×10⁻¹⁵ where banked); tolerance the κ floor — the G-MSCS2 v1.1 delta, adopted from the start.

**6.3 Grids (rule 4).** The schema carries generators, never counts: the 12-point t-grid as its explicit list; the 5-point (t₂, t₄) axis; the fit-window predicate |t| ≤ 0.25 (inclusive); the Richardson step pairs (0.05, 0.1) and (0.125, 0.25); the area grid as (−0.25, 0.25, 201) per axis; the OOM factors {0.1, 1, 10}. The comparator recomputes every count from them at comparison time and rejects a checkpoint whose count fields differ; no count literal appears in any instrument.

**6.4 Coefficients and edges.** Per key × arm × family: κ of record, κ basis-independent, the fit resolution |κ_fit − κ_bi|/|κ_bi| (serialized; observed ≤ 1.9×10⁻⁴ on S2-E₂ Hill, ≤ 2.3×10⁻⁵ on HS-mean and ≤ 7.3×10⁻⁴ on S2-h — the two robustness arms tested by F-CTRL-SA-RECON; E-v2-6); for the combined interval: t\*, σ\*, the basis-independent t\*, class, flags, OOM classes; per row the same, for the record; the reachable set R^w and its box and hull; the two-parameter record of §3.4; gate class, σ-union, intersection. Two-leg tolerance on every edge 1×10⁻¹⁰ relative (identical inputs; any larger difference is a parsing or binding difference — the historical failure point: G-CI1 S9 (A), G-POLY1 H-16, H-19); classes, flags, census and per-row md5s identical.

**6.5 Comparator checks.** C-SA-1 edges; C-SA-2 per-key and gate classes, flags, OOM classes; C-SA-3 sealed md5, bytes, census, per-row md5s; C-SA-4 pinned-inputs md5; C-SA-5 the nulls of §6.2 at their tolerances, with their tokens; C-SA-6 T1 zero hits on both legs; C-SA-7 grids recomputed; C-SA-8 the two mapper md5s differ (independent implementations; the parse is the independence surface). S9 on any miss; representational misses resolved by the path-(a) mini-dispatch pattern.

## 7. Falsifiers, the kill surface, and the blast radius

- **F-SA-1 (kill surface item (iii)) — KILL-IN-D** as defined in §1. From the §0 reach table, the union of reachable δ inside D is **[−1.3038×10⁻⁴, +2.2126×10⁻⁵]** over every key and arm (E-SA-9(a), elected) and **[−1.3035×10⁻⁴, +1.2345×10⁻⁵]** over the primary arm alone (E-SA-9(b), declined; serialized for information). KILL-IN-D fires iff the combined interval lies wholly outside the all-arm union (ST-6); an interval outside the unwidened unions (footnote to the §0 reach table) but not outside these is MARGIN-ONLY.
- **F-SA-2 (instrument integrity, not physics)** — F-CTRL-SA-MONO; halt, S9.
- **F-SA-3 (two-leg)** — any C-SA miss; S9 before any class is reported.
- **Not falsifiers:** a BINDING window of any size (the delivered curve); INERT-IN-D; TUNED (a required-texture statement, never a confirmation — systematics and other physics lie outside the gate); ANCHOR-INCONSISTENT (a statement about the rows, routed to the author); MARGIN-ONLY (routed to the registered third-order successor).
- **Blast radius of KILL-IN-D (pre-declared, the §2.2 / G-SCALE1 pattern).** It is a kill of the conjunction "the single-species identity (E-MS-1(a)) + a weak axisymmetric texture inside D + I-SA-1 + the leading-order aggregate in its regime". Routing: (a) E-MS-1(a) — the S2 = E₂-content identification is the first address; (b) D — a texture beyond |t| = 0.25 is outside the validated surface, not excluded; (c) I-SA-1 — a sightline-resolved reading could differ (along the fiber axis the split is zero; off it κ(ψ) is not the sphere-weighted κ); (d) E-SA-4 and the no-Born order. Nothing in §2.91.Q or §2.91.S is touched; the polycrystal postulate stays R3; a successor is named, not executed. Any verdict-aware change to D, μ, the arm set, or the comparison reading after the read is Eddington-foreclosed by this clause.

## 8. Pre-registered structural statements (derived from banked signs and values; no anchor) and hypotheses

- **ST-1** — the per-direction species split vanishes along the fiber axis for every fiber texture, every grain tensor and every averaging scheme (S-SA-1); a single-sightline anchor at unknown orientation is conservatively INERT. The claim is on the axis only: shear-speed degeneracies on off-axis cones (L-SA-3, Vavryčuk) are neither claimed nor needed. The symmetry is textbook (L-SA-3); the statement about the species split is this gate's.
- **ST-2** — for S2-E₂ on hex and any interval containing 0, the two-parameter admissible region reaches the boundary of D along |t₄/t₂| = 2.9957 / 2.9948 / 3.2497 / 3.2501 (Hill) and 2.9887 / 2.9878 / 3.2460 / 3.2465 (HS-mean); for S2-h the hex region is compact.
- **ST-3** — the fcc branch is t₂-blind at second order under both readings; for any interval containing 0 the gate-level t₂ window is INERT under E-SA-5(a).
- **ST-4** — for an interval containing 0: S2-E₂ hex t₂ and fcc ⟨001⟩ t₄ bind on lo, S2-E₂ hex t₄ and fcc ⟨111⟩ t₄ bind on hi; every S2-h family binds on lo.
- **ST-5** — every unclipped edge scales as √(budget/|κ|). For an interval containing 0, a class can change under ×10 / ×0.1 only if an edge lies within a factor √10 of D. For an interval excluding 0, a class can change only if an end of the interval lies within a factor 10 of an end of some reachable set R^h or R^w, because the classes there are set by the interval against the reach, not by D. (Corrected in v2; v1 stated the D condition for every interval — E-v2-6.)
- **ST-6** — the kill thresholds of F-SA-1: a positive δ is reachable inside D only through S2-E₂ hex t₄ and fcc ⟨111⟩; a negative δ through S2-E₂ hex t₂ (with t₄), fcc ⟨001⟩, and every S2-h arm; S2-h reaches no positive δ. The MARGIN bands are (+2.0115×10⁻⁵, +2.2126×10⁻⁵] and [−1.3038×10⁻⁴, −1.1853×10⁻⁴) over every arm, (+1.1223×10⁻⁵, +1.2345×10⁻⁵] and [−1.3035×10⁻⁴, −1.1850×10⁻⁴) over the primary arm (for information; E-SA-9(b) declined).
- **HYP-SA-1** — the chat and CC legs return identical classes and edges on the first run (the mapping has no free parameter; any miss is a parsing or binding miss).
- **Not predicted:** the gate class (§1).

## 9. Pinned inputs and imports

- **The pinned-inputs file (generated before lock; verified by the author before the lock record is written).** `pinned_inputs_G_MSCS_A.json`, md5 `2d44ec01a66889f330d940dee3313bdc`, 96,761 B. It was built by `sa_build_pinned_inputs.py` (md5 `8189100ede80eac360b25a146e580abf`) from a clone of `main` at `e1fa071`, and checked independently by `sa_verify_pinned_inputs.py` (md5 `cf004d517d2efe91a02c92a58e3df6bf`), which shares no code with the builder and trusts nothing in the file: it holds its own pointer map, constants, tokens and structure, and re-derives every leaf of `derived` (1,105 leaves).
  - **Deterministic by construction:** standard library only; values are either copied or derived with +, −, ×, ÷ and √ only; keys sorted; ASCII; a trailing LF. The builder gives identical bytes under Python 3.10, 3.11, 3.12 and 3.13.
  - **Self-identifying:** the builder embeds its own md5, so the file names its generator.
  - **Refuses on any failure:** a source md5 or byte count, a missing key, a non-finite value, a structural assertion (grid identity, the Richardson steps present, the floor-adjoining W^EM_∪ component, the diagnostic basis order) or a preflight control (§5).
  - **Checks itself after writing:** it re-derives `derived` from the written file (bit-identical), re-reads all 335 copied values from their sources by pointer (bit-identical), and confirms that the round trip is byte-stable.
- **Sources (seven, on `main`; the full md5 and byte count of each are asserted):**

| alias | path | md5 | bytes |
|---|---|---|---|
| G2chat | `gmscs2_gate/g_mscs2_chatleg_checkpoint.json` | `1c5b6b59829d2a6b9ae2b1a7a016832d` | 31,575 |
| G2cc | `gmscs2_gate/g_mscs2_ccleg_checkpoint.json` | `9961745d1e1857cfab6445d4754b5060` | 68,540 |
| G1chat | `gmscs1_gate/g_mscs1_chatleg_checkpoint.json` | `c04c0b8ea34cfe60f231aa06828e6ce4` | 33,289 |
| G1cc | `gmscs1_gate/g_mscs1_ccleg_checkpoint.json` | `249e11dd53c4cb82f302b15d3c94c337` | 24,415 |
| DK24 | `gmscs2_gate/diag_kappa24.json` | `b7952dfcaddcd1d98e424aee8ce5231f` | 1,917 |
| DQF | `gmscs2_gate/diag_quadform_basis.json` | `d84aa1fdce7dea1b1a5d24dfb8f13c18` | 1,119 |
| CI1 | `gci1_gate/ci1_phase3_cc_r2.json` | `845ae6beb1b90fe34c540f843ffdb9f5` | 45,760 |

- **The regime scale, read by key (new in v2).** `d_EM` = `/per_oom/x1/W_EM_union/0/1` of the G-CI1 CC r2 checkpoint (the V4.77 record names it: "ci1_phase3_cc_r2 845ae6be (45,760 B)"). The builder asserts that the near component is a single floor-adjoining interval and that the value equals the ledger literal 3.7641664288e-33.
- **What the author checks (the commands are in the delivery note; nothing here needs the sealed file):**
  1. the seven source md5s;
  2. that the builder regenerates the file with md5 `2d44ec01…`;
  3. that the independent verifier, run with the builder as its third argument, prints PASS. The verifier re-derives every leaf to within 1×10⁻¹² relative; any change below that tolerance is caught by the whole-file md5 of step 2;
  4. by reading, that the §0 tables match what the builder prints from `derived.families`, `derived.reach` and `derived.unions`.

  The author's word "pinned inputs verified" is then recorded in the lock record. The lock record also cites the md5s of the file, the builder and the verifier.
- **File layout.** `sources` · `provenance` (one RFC 6901 pointer template per field, with its scope) · `structure` (the keys, the arms, the primary set, the mapped and null families) · `tokens` (the `odf_reading` set of rule 1, the conformant anchor tokens) · `constants` (D, μ, KD_CLIP, the tolerances, the OOM factors, the synthetic generators — the budgets, the tight budget, the band fractions and the two k values — and the rms closed forms) · `grids` (generators only) · `raw` (copied values) · `derived` (reference values, a pure function of the rest — including `synthetic`, the pinned synthetic intervals of Phase 2; F-CTRL-SA-PIN-DERIVED) · `rms_exact_check` (⟨P₂²⟩ = 1/5, ⟨P₄²⟩ = 1/9, ⟨K̃₄²⟩ = 4/21 and ⟨K̃₄⟩ = 0, verified in exact rational arithmetic) · `_meta`. No point count is written anywhere in the file (rule 4); the builder and the verifier print the counts, which they compute from the generators.
- **Imports, named:**
  - E-MS-1(a) (inherited);
  - **I-SA-1** — the sealed δ is compared with the sphere-weighted descriptor split (E-SA-3(a), elected);
  - the regime (E-SA-4(a), elected);
  - `diag_assumed` for the robustness arms' diagonality (§3.6);
  - the untextured-ODF reference and the M.ONT polycrystal ontology (inherited — this gate is a constraint *on* the texture import, not a claim about its value);
  - K = ∅;
  - the V4.70 KNOB caveat (kernel-labelled throughout);
  - the tetragonal-form hex tensors (E-MS-2b).

  **Import delta of this gate under the elections: I-SA-1, plus the `diag_assumed` reading on the robustness arms of the kill test.**

## 10. Elections (ELECTED by the author, directive of September 29, 2026; T3-immutable at lock)

Each election keeps its v1 option text verbatim, as the record of what was offered and declined. The one correction is in E-SA-4, whose two k thresholds are restated (E-v2-6).

- **E-SA-0 (gate ID): ELECTED (a).** Options: (a) G-MSCS-A · (b) G-MSCS3 · (c) other. *v1 recommendation: (a) — a mini-gate on the family's banked surface, the G-S2C1-W naming pattern.*
- **E-SA-1 (anchor classes): ELECTED (a).** Options: (a) `spd` rows only · (b) also a first-order polarization-split class (needs its own identification and the S-SA-1 symmetry again). *v1 recommendation: (a); (b) registered as a successor (S-SA-6).*
- **E-SA-2 (families): ELECTED (a).** Options: (a) t₄ on every key, t₂ on hex keys, the hex two-parameter region reported · (b) t₄ only. *v1 recommendation: (a).*
- **E-SA-3 (the comparison reading of a one-sightline anchor — S-SA-1): ELECTED (a).** Options:
  - (a) **sphere-weighted** — the banked surface as registered, I-SA-1 declared, no new computation;
  - (b) **directional arm added** — a new two-leg computation of κ(ψ) per key on a pinned ψ-grid with the G-MSCS2 machinery: per-ψ windows, the uniform-mean (population) reading, and the conservative INERT stated;
  - (c) (a) primary + (b) as a second arm.

  *v1 recommendation: (a) — it keeps the gate the mini-gate the author elected; ST-1 goes into the verdict record so no window is read as sightline-independent; (b) registered as the successor "the directional arm".* (Prior art for (b): L-SA-2.)
- **E-SA-4 (regime): ELECTED (a).** Options:
  - (a) evaluated at the W^EM_∪ near-component edge with KD_CLIP = 0.3 — effectively vacuous at that d (fires only for k > 7.96×10³¹ m⁻¹; v1 printed "8.0×10³¹");
  - (b) declared, not evaluated;
  - (c) evaluated at the W_∪′ edge banked alongside (2.1213132100130068 m) — would VOID every EM band with k > 0.1415 m⁻¹ (v1 printed "0.14").

  *v1 recommendation: (a) — the operative ledger scale; the dependence becomes explicit and checkable.*
- **E-SA-5 (gate-level summary): ELECTED (a).** Options: (a) the σ-union across the four configurations (CONSERVATIVE), per-branch windows serialized · (b) per-branch windows only. *v1 recommendation: (a).*
- **E-SA-6 (coefficient of record): ELECTED (a).** Options: (a) the banked fit values of record; basis-independent edges serialized; RESOLUTION-SENSITIVE flag · (b) the basis-independent values of record. *v1 recommendation: (a) — consume as banked.*
- **E-SA-7 (T1): ELECTED — "The base 05302210 + the G-MSCS1 stratum."** As registered in v1: the base `05302210` (11 patterns) + the G-MSCS1 stratum (25) — together the 36 pattern lines of `be921b8c`, composed as `tools/t1/T1_forbidden_G_MSCS_A.txt` at lock — + the author's T1-A1 at sealed delivery; no chat-side stratum (the chat leg composes no anchor-digit pattern).
- **E-SA-8 (leg order): ELECTED (a).** Options: (a) CC-BLIND-FIRST · (b) chat-first. *v1 recommendation: (a).*
- **E-SA-9 (a kill must be election-robust): ELECTED (a).** Options: (a) KILL-IN-D requires exclusion on the primary arm and every robustness arm (HS-mean, S2-h, hex (b), cubic ⟨111⟩) · (b) primary arm only. *v1 recommendation: (a) — the G-SCALE1 pattern.* The primary-only union of (b) is serialized for information.
- **E-SA-10 (domain): ELECTED (a).** Options: (a) D = the fit window |t| ≤ 0.25 per family · (b) extended to |t| ≤ 0.5 using the banked grid points there as a check. *v1 recommendation: (a).*
- **E-SA-11 (reach of the kill test — S-SA-9): ELECTED (a).** Options: (a) the hull of the second-order box and the banked grid values inside D, widened by μ = 0.10 · (b) the hull without widening · (c) the second-order box alone. *v1 recommendation: (a); (c) is shown to understate the banked reach by up to 7.5% and is not recommended.*
- **Q-SA-1 (for the author, not an election):** unchanged from v1. Standing amendment P-5 (an independence witness for every difference-forcing election) remains proposed. This gate forces no leg difference (shared pinned inputs), so P-5 is not needed here, and its absence is a decision, not an oversight.
- **Q-SA-2 (for the author, not an election; new in v2):** do H-SA-3 (the Man–Huang citation) and H-SA-4 (three round-downs: the κ₂₄ estimator bound and the S₄ and b₁ two-leg bounds) ride the next fold's bracket with H-MS2-9, and under which numbers? Or do they stay recorded here only? (§12.)
- **Q-SA-3 (for the author, not an election; new in v2):** should H-MS2-9 also get an estate erratum file, `gmscs2_gate/estate/H_MS2_9_ERRATUM.md`, through the next housekeeping PR? (§12.)

## 11. Registers and non-claims

- Every edge, class and flag R1-machine two-leg **on the pinned coefficients and the sealed text** (arithmetic and parsing). The reading "the texture import is bounded by the anchor" R2, conditional on E-MS-1(a), I-SA-1, the regime (E-SA-4), the leading-order aggregate (no Born; kernel-labelled) and D. A KILL-IN-D would be R2 in the same conditions plus `diag_assumed`, routed per §7. The polycrystal postulate remains R3. ST-1 … ST-6 are R1 structural consequences of banked values (ST-1 a symmetry identity). The LSF-δ findings are R1 bibliographic at their stated ceilings; S-SA-11's first-order statement is R2 (structural: the banked b₁ and the Man–Huang first-order affinity), not a computed result.
- No confirmation of any texture; no d, no f, no SI value in any instrument except the W^EM_∪ edge and the sealed k fields inside the quarantined mapper; no claim about the tensor messenger beyond E-MS-1(a); no helicity-±2 field (K = ∅); no reinstatement of W_∪; no evaluation of any bound outside the sealed rows; no retraction; §2.52 Open 3 untouched.

## 12. Housekeeping (carried by the next fold, not by this memo)

- **PR #31 (post-V4.86).** `git ls-remote origin refs/heads/main` returned the same result at 2026-09-29 19:11:26 UTC (v1) and at 2026-09-30 00:01:06 UTC (v2): `e1fa071758a0912472bbb6eba7f77fab35669807` = "Merge pull request #31 from gifgaf0/claude/new-session-txamk5", committed 2026-09-27 18:57:46 −07:00 (2026-09-28 01:57:46 UTC), parents `d92642e` + `c351d2a`. PR #31 landed the V4.86 fold estate at `gmscs2_gate/v486_estate/` (11 files, commit `734bd3b`) and `gmscs2_gate/HK3_CC_RETURN_INBAND.md` (commit `c351d2a`): 12 files, nothing outside `gmscs2_gate/`. Recorded as observed (the V4.86 `ls-remote` rule). The next fold's bracket carries it, together with the `FOLD_AUTHORIZATION_V4_86_ADDENDUM.md` correction (CC's branch ref retained).
- **H-MS2-9 — PLANNED BRACKET for the eventual fold** (the author's numbering, directive of September 29; v1's H-SA-2; origin corrected in v2, E-v2-3).
  - *Item — proposed record text:*

    **H-MS2-9 (two-leg record; honesty; a third-order coefficient misquoted — non-verdict-bearing).** V4.85 states, in its record and in §2.91.S, that the fcc reading-(i) t₂t₄² coefficient is "−5.9×10⁻⁵ / −1.0×10⁻⁴" (step / gem8). The banked CC fit (`g_mscs2_ccleg_checkpoint.json` `9961745d`, `/phase2/<key>/quadform/x_cubic_terms_discarded`, the t₂t₄² entry) gives **−5.90×10⁻⁵ (step) and −8.51×10⁻⁵ (gem8), identical on the ⟨001⟩ and ⟨111⟩ descriptor axes.** Two further banked values agree with the pair: the chat quadform-basis diagnostic (`d84aa1fd`, cubic_step|001) reproduces the step value to within 4.0×10⁻¹⁰ relative, and the CC A-3.1 mixed changes at (0.25, 0.25) are consistent with the banked pair — −9.08×10⁻⁷ with the step value to within 1.6%, and −1.30×10⁻⁶ with −8.51×10⁻⁵ (gem8) to within 2.0%, the quartic correction — while "−1.0×10⁻⁴" misses the gem8 change by about 20%.

    The figure "−1.0×10⁻⁴" first appears in the CC in-band return prose (`G_MSCS2_CC_RETURN_INBAND.md` `290b3431`, line 79: "fit coefficient −5.9e-5 / −1.0e-4"), where the prose disagrees with the same leg's checkpoint. The chat closure memo (`e43a0732`, lines 45 and 56) carried it, and V4.85 took it from there. The search was scoped to the repository history available to this session, a shallow clone of 15 commits: within it the CC return (commit `3849c3d`, September 26, 20:20 UTC) precedes the estate commit that carries the closure memo (`1b15a0d`, September 27, 20:23 UTC). No comparator read the prose; the C-checks compare checkpoints.

    **The step value stands; the gem8 value of record is −8.51×10⁻⁵.** The item is non-verdict-bearing: it concerns a discarded third-order term, and no class, coefficient of record, tolerance, control, falsifier or H-item of G-MSCS2 rests on it. Found September 29, 2026, by the G-MSCS-A pre-draft audit.
  - *Anchors (V4.86, md5 `d4c42a53…`), four occurrences:*
    - line 41 (the V4.85 fold-in record): "(fit coefficient −5.9×10⁻⁵ / −1.0×10⁻⁴)" and "cubic under the inherited weight t₂t₄² ≈ −5.9×10⁻⁵ / −1.0×10⁻⁴, no t₂² term of any kind";
    - line 1646 (§2.91.S): "(coefficient −5.9×10⁻⁵ / −1.0×10⁻⁴)" and the same second phrase.

    Each occurrence keeps its text (append-only).
  - *Bracket text, appended after each occurrence:* **[H-MS2-9 (V4.8x): for the gem8 value read −8.51×10⁻⁵ — the banked CC fit, both descriptor axes; the step value −5.9×10⁻⁵ stands; non-verdict-bearing.]** Here "V4.8x" is the fold that carries it.
  - *Estate (Q-SA-3):* if the author so elects, `gmscs2_gate/estate/H_MS2_9_ERRATUM.md` goes in via the next housekeeping PR, carrying the item text, the four anchors, and the checkpoint pointers and values. The closure memo `e43a0732` and the CC return `290b3431` are not edited; the erratum points at them.
  - *Status:* planned, not applied. It rides the next fold whether or not G-MSCS-A has closed by then.
- **H-SA-3 (citation precision; recorded, not resolved; found by L-SA-3).** The representation theorem for material tensors of weakly-textured polycrystals is Man & Huang, J. Elasticity 106(1), 1–42 (online November 2010 — OpenAlex gives the 24th, Springer the 25th; issue January 2012), DOI 10.1007/s10659-010-9284-3. The record was verified this session via OpenAlex, and again by the independent audit.
  - The G-MSCS2 v2 memo cites it as "J. Elasticity 105, 1 (2011)". That conflates it with a different paper, Man & Huang, J. Elasticity 105, 29–48 (2011), the first-order Voigt–Reuss–Hill formula.
  - V4.85 carries "Man–Huang (2011)" at V4.86 lines 41 and 1646, and "Man–Huang 2011" at line 3.
  - The G-MSCS1 memo's "(2012)" is the issue year.

  Attribution only; non-verdict-bearing. *Related, not an error:* the banked record cites Thompson–Smith–Lee as "1984". The NTRS record retrieved this session gives the publication date as 1986 (a NASA Lewis conference, *Analytical Ultrasonics in Materials Research and Testing*); the meeting year is not on that record. Disposition: Q-SA-2.
- **H-SA-4 (siblings of H-MS2-9: three round-downs in the banked record; recorded, not resolved; found by the independent audit of v2).**
  - *The κ₂₄ estimator.* V4.85 gives the basis-independent κ₂₄ estimator as "≤ 2.2×10⁻¹²" on both legs, at V4.86 lines 3, 41, 1646 and 4366, as does the CC return (`290b3431`, line 79: "≤ 2.2e-12"). The CC checkpoint holds 2.2204×10⁻¹² (cubic_step|111) — the same round-down E-v2-1 corrected in this memo. *Proposed bracket:* **[for "≤ 2.2×10⁻¹²" read "≤ 2.3×10⁻¹²" — the CC checkpoint maximum 2.2204×10⁻¹², cubic_step|111; non-verdict-bearing (the tolerance is 1×10⁻⁶).]**
  - *The S₄ and b₁ two-leg bounds.* V4.86 line 3 bounds the two-leg deviations of S₄ and b₁ at two significant digits, each rounded down from its banked maximum. The maxima, from the chat and CC checkpoints now both pinned, are 2.3429×10⁻¹⁵ (S₄, hex_step|a) and 1.5328×10⁻¹⁴ (b₁, cubic_gem8|111). *Proposed bracket, line 3 only:* **[H-SA-4: the two-leg bounds read S₄ ≤ 2.4×10⁻¹⁵ and b₁ ≤ 1.6×10⁻¹⁴ — the banked maxima 2.3429×10⁻¹⁵ and 1.5328×10⁻¹⁴; non-verdict-bearing.]** Lines 41 and 1646 give the same figures as worst-case values, which are correct at two digits.

  Disposition: Q-SA-2.
- **The project store** stood at 1,900,823 of 2,000,000 B at the start of this session and at 1,929,233 B before v2's writes. With about 70 KB free, v2 replaces the v1 draft at the same store path. v1 stays retrievable from its delivery in this conversation, where its md5 is `a7d6bdbc…`. The builder and the verifier are stored alongside it (`claude/sa_build_pinned_inputs.py`, `claude/sa_verify_pinned_inputs.py`). The pinned-inputs file is not stored, because it regenerates from the builder.

## 13. T1

**The gate list.** It is composed at lock as `tools/t1/T1_forbidden_G_MSCS_A.txt`: the pattern lines of `be921b8c` verbatim, under a header naming this gate. Per E-SA-7 as elected, that is the base `05302210` (11 patterns) plus the G-MSCS1 observational stratum (25).

**The scanner.** `t1_scan.py` `6b862900`: pattern lines only; case-sensitive substring; the contextual numeric rule; hits reported by index only.

**T1-A1.** The author's list is appended at sealed delivery, after the pre-freeze collision scan (§4.6); the effective list is the union.

**Exemptions.** The sealed file and the list files are exempt from scanning, for cause; the instruments halt without them.

**Scan results.** **This v2 scans CLEAN (0 hits) under the 36 patterns of `be921b8c`** (the list the gate list will copy), under the base alone, and, as a courtesy, under the G-2a-L1 list `04438b74`; the scan record, collision counts included, is in §15. Five other artifacts also scan CLEAN under all three lists: the builder, the verifier, the pinned-inputs file and the two author-side tools. In the pinned file the scanner logs 13 / 0 / 2 formatting collisions (under `be921b8c` / `05302210` / `04438b74`): digit runs inside longer numeric tokens — banked values and values derived from them — which are not hits under the contextual numeric rule and are not reworded, because the file's values are fixed by the sources and the derivation. One collision in a draft of this memo was reworded before delivery; its location is not recorded, so as not to point at a pattern. S-SA-10's pre-freeze A1 scan covers the pinned file with the other locked artifacts.

## 14. LSF-δ (executed September 29, 2026; six clusters; per-source transcription ceilings stated)

**Ceilings** (as in G-MSCS2 §12):
- **FT** — the full text, or a full-text excerpt, was read this session;
- **AB** — the abstract or publisher description;
- **LS** — listing only (title and venue confirmed; text not retrieved this session);
- **SEC** — a secondary exposition;
- **NF** — not fetched; a standard reference.

**Execution.** Three sub-agents ran the searches in parallel (clusters 1 + 2, 3 + 6, 4 + 5). They worked under the ceiling discipline and the T1 hygiene rules: no bound digit, and no event, collaboration or instrument identifier, in a report's main text; where a citation needed such an identifier, it went on a separate line that is not transcribed here. The chat leg re-verified three records directly — the Man–Huang record (OpenAlex), the Thompson–Smith–Lee record (NTRS) and the Rodgers preprint record (Zenodo) — and transcribes the rest at the ceilings the agents stated. Three FT-ceiling entries (Cornish–Blas–Nardini, Anber–Donoghue, Moore–Nelson) quote sentences that also stand in their abstracts. The independent audit of v2 re-fetched the sources and confirmed 21 of the quotes verbatim, one of them apart from inner quotation marks (§15 item 6); the Thompson–Smith–Lee entry was corrected by it (the NTRS abstract text and ceiling).

**Access notes.** Refused this session, with the affected sources cited at LS or AB:
- the Springer article pages (rate-limited);
- ADS, IOPscience and Google Books (robots);
- the AIP / JASA / JAP article pages, ScienceDirect, SciELO, De Gruyter, ResearchGate, PNAS and the Royal Society pages (403);
- Crossref, for three records (rate-limited);
- one Zenodo API request (the fetch permission was not answered).

**The 2017 multi-messenger papers are cited by neutral handle only.** Their titles, author collaborations and archive numbers carry T1 identifiers, and no file of this gate writes them (D-SA-0).

| Cluster | Sources (ceiling) | What was found | Bearing on this gate |
|---|---|---|---|
| **L-SA-1** the multi-messenger speed-difference dialect | the joint timing paper of the 2017 multi-messenger event (FT; paraphrased where its wording carries a T1 string: the speed difference is defined as the tensor speed minus the EM speed, the EM speed being called "the speed of light", and the fraction is taken relative to the EM speed; the positive end assumes that the tensor signal's peak and "the first photons were emitted simultaneously"; its coefficient subsection fits "with all other coefficients, including the EM sector ones, set to zero"); the overview paper of the same event (AB; it reports the lag only); the collaboration's tests-of-GR paper for that event, Phys. Rev. Lett. 123, 011102 (2019) (FT excerpts; defers the speed result to the joint paper; its propagation test covers frequency-dependent dispersion only); the first-catalog tests-of-GR paper, Phys. Rev. D 100, 104036 (2019) (FT excerpts: a frequency-independent speed change "gives no observable dephasing" and "can be constrained by comparison with the arrival time of the photons"); Cornish–Blas–Nardini, PRL 119, 161102 (2017) (FT: "upper and lower bounds on the speed of gravitational wave propagation"); Liu et al., PRD 102, 024028 (2020) (AB); Ray et al., Phys. Rev. D 110, 122001 (2024), arXiv:2307.13099 (FT excerpts: "which arrive from a multitude of sky directions, allows for a complete exploration of the isotropy of vg"); Moore–Nelson, JHEP 09 (2001) 023 (FT: "the case c_g < c is very tightly constrained by the observation of the highest energy cosmic rays"); Kimura–Yamamoto, JCAP 07 (2012) 050 (AB); Kostelecký–Tasson, PLB 749, 551 (2015) (FT: "Any single coefficient constraint is normally one-sided because Čerenkov radiation is possible only for superluminal particles"); Ezquiaga–Zumalacárregui, Front. Astron. Space Sci. 5, 44 (2018) (FT, partial: "Note that the speed can depend on the propagation direction. It may also depend on the frequency"); de Rham–Melville, PRL 121, 221101 (2018) (AB); Creminelli–Vernizzi, PRL 119, 251302 (2017) (AB) | *Sign:* the primary statement defines the fractional difference as (tensor − EM)/EM, positive when the tensor messenger is faster — δ as defined here. *Shape:* the interval is two-sided and asymmetric; the positive end assumes simultaneous emission, the negative end an assumed intrinsic EM emission lag, and both use the lower end of the distance credible interval. It is framed as conservative, with no separate confidence level of its own. *Sightline and bands:* the speed subsection carries no sightline caveat; the coefficient subsection uses the counterpart's sky position, fits one coefficient at a time, and speaks of relative group velocity. The photon side is stated as energies; the tensor side is dated by its signal peak, with no band stated. *Other statements in the dialect:* network-timing and catalog intervals are measured against the conventional constant, not a co-travelling signal; Cherenkov bounds are one-sided and measured against the limiting speed of matter; secondary restatements symmetrize the interval, dropping its sign structure; and the bound applies only in the event's band (de Rham–Melville) | Fixes the §4.3 entry: `delta_def` unchanged (no negation); the primary statement's own two ends (S-SA-12); `cl` is the author's entry (`hard` admissible); `geom=single`; `q` serialized (group, per the source); the k fields supplied by the author. S-SA-11: only counterpart timing is δ. Prior art; no collision |
| **L-SA-2** direction-dependent and birefringent constraints, effective-field-theory dialect | Kostelecký–Mewes, PLB 757, 510 (2016) (FT: "multiple astrophysical sources at different sky locations permits extraction of independent constraints on different coefficients"; "under the assumption that the other components vanish"); Mewes, PRD 99, 104062 (2019) (FT: "a given point source with fixed observed v̂ can at most measure the four linear combinations of spherical coefficients"; at the lowest order "the phase and group velocities acquire the same frequency- and polarization-independent shift"); Shao, PRD 101, 104019 (2020) (FT; a global fit over the first transient catalog); O'Neal-Ault et al., Universe 7, 380 (2021) (FT: "the two modes generally travel at different speeds in the vacuum"); the 2023 global fit over the third transient catalog, PRD 107, 064031 (2023) (FT: "The strength of the LI violation can change with source location."; its first author's name is a T1 pattern and is withheld); Kostelecký–Russell, *Data Tables for Lorentz and CPT Violation*, Rev. Mod. Phys. 83, 11 (2011), arXiv:0801.0287, 2026 edition (AB); the joint timing paper's coefficient subsection (FT, above) | One sightline constrains only a fixed small set of linear combinations of the direction-dependent coefficients. Single-event results are either one-coefficient-at-a-time ("maximal reach") or isotropic-only, with the anisotropic part set to zero by assumption; separating the coefficients needs many sightlines. At the lowest order the tensor-sector shift is nondispersive and nonbirefringent; tensor birefringence enters only at higher order, and dispersively. No analysis that relates a single-sightline bound to a sphere-averaged quantity was located | Prior art for S-SA-1's logic in that dialect. I-SA-1 is this gate's analogue of the isotropic-only assumption: declared, not derived. The successor to the declined E-SA-3(b) finds its machinery here. S-SA-6's first-order, dispersion-free polarization split has no lowest-order tensor-sector counterpart in this dialect — a translation question for the E-SA-1(b) successor. No collision |
| **L-SA-3** fiber texture → transverse isotropy; the along-axis shear degeneracy | Turner, JASA 106, 541 (1999) (AB: "equiaxed cubic polycrystalline metals with a single aligned axis. The Green's dyadics in this case are those for a transversely isotropic medium."); Maurel–Lund–Montagnat, Proc. R. Soc. A 471, 20140988 (2015) (FT: "the structure is invariant by rotation along the vertical axis e3, thus it is isotropic in the transverse plane"); Evans et al., J. Mater. Sci. 56, 10053 (2021) (FT: "If a manufacturing or forming process produces texture with axial anisotropy, as is the case for extrusion, the material will have transversely isotropic symmetry"); Martinschitz et al., J. Appl. Cryst. 42, 416 (2009) (FT: "elastic behaviour is in-plane isotropic (i.e. independent of the angle ϕ) but dependent on the tilt angle ψ"); Le Bourdais–Leymarie–Gardahaut, Mater. Charact. 233, 116105 (2026) (FT excerpt); Thomsen, Geophysics 51, 1954 (1986) (FT, scanned copy: velocities as functions of the angle between the wavefront normal and "the unique (vertical) axis"); Thomsen–Anderson, GSA Spec. Pap. 514 (2015) (FT: "These two modes have the same velocity VS0 at vertical propagation; at other angles of propagation, their velocities differ"); Chevrot–van der Hilst, GJI 152, 497 (2003) (FT: "In transversely isotropic media the direction of the symmetry axis always corresponds to a kiss singularity"); Vavryčuk, GJI 145, 265 (2001) (FT: the S-wave slowness surfaces "can intersect along a line"); Crampin, Wave Motion 3, 343 (1981) (AB); Cholach–Schmitt, CSEG Recorder 28(7) (2003) (FT: for hexagonal crystals with the symmetry axis along Z, "only three non-zero coefficients (C011≡1, C211 and C411) contribute to the elasticity"); Li–Thompson, J. Appl. Phys. 67, 2663 (1990) (AB); Thompson–Smith–Lee, NASA NTRS 19860013503 (AB — the NTRS abstract, publication 1986: a procedure for determining the ODF expansion coefficients "W sub 400, W sub 420 and W sub 440"); Lobos Fernández–Böhlke, J. Elasticity 134, 1 (2019) (AB); Man–Huang, J. Elasticity 106, 1 (2012; online 2010) (LS; record verified) and J. Elasticity 105, 29 (2011) (AB: "Our formula is correct to first order in the texture coefficients"); Sayers, J. Phys. D 15, 2157 (1982) and Sayers–Allen, J. Phys. D 17, 1399 (1984) (LS); Roe 1965; Bunge 1968, 1982 (LS) | Transverse isotropy of a fiber-textured aggregate is in print for cubic grains, for hexagonal grains, and for axial textures in general; the theorem-form "any crystal symmetry" statement was not retrieved (Man–Huang at LS). The degeneracy of the two shear modes along the TI axis (a "kiss singularity"), and their splitting away from it, are textbook seismology. The velocities depend only on the angle to the axis. The l = 2 and l = 4 ODF coefficients control the elastic constants of hexagonal and cubic aggregates. Caveat (Vavryčuk): shear-speed degeneracies can also occur on a cone off the axis. A per-grain descriptor weighting of one shear mode (the E₂ content) was not located | ST-1's symmetry is textbook and now attributed (Thomsen–Anderson; Chevrot–van der Hilst; Turner; Evans et al.). ST-1 claims the vanishing of the species split on the axis only (§8). H-SA-3 (the Man–Huang citation). No collision |
| **L-SA-6** the long-wavelength regime | Stanke–Kino, JASA 75, 665 (1984) (AB: "valid in the Rayleigh, stochastic, and geometric regions"); Hirsekorn, JASA 72, 1021 (1982) (AB); Sha, Acoustics 2(1), 5 (2020) (FT: "The quasi-static velocities from the SOA model obey the Hashin–Shtrikman bounds and agree reasonably with self-consistent velocity"); Huang–Sha–Huthwaite–Rokhlin–Lowe, JASA 148, 3645 (2020) (FT, accepted manuscript: "In the low-frequency Rayleigh regime, the phase velocity is independent of frequency, i.e. nondispersive"; "the velocity extends asymptotically to the quasi-static velocity limit, which is significantly below the Voigt average"); Huang–Rokhlin–Lowe, Phil. Trans. R. Soc. A 380, 20210382 (2022) (FT); Roy–Kube, J. Mech. Phys. Solids (2025), arXiv:2505.06453 (volume and article number not confirmed) (FT: "the elastodynamic scattering theories recover the effective static properties in the long wavelength limit"; "the Rayleigh regime, for p₀ℓ < 1/2"); Li–Rokhlin, Wave Motion 58, 145 (2015) (AB); Weaver, JMPS 38, 55 (1990) (LS); Papadakis 1965, 1968 (LS; the regimes via SEC) | The k → 0 limit of the scattering theories is the quasi-static effective medium: inside the Hashin–Shtrikman bounds, near the self-consistent value, and below Voigt. It is nondispersive in the Rayleigh regime, whose boundary is stated as p₀ℓ < 1/2 (ℓ a correlation length). An explicit statement that the dispersive corrections are of higher order in k·d was not located | D-13 (the leading-order aggregate is the k → 0 limit) and D-9 (Hill primary, HS-mean reported) are grounded. KD_CLIP = 0.3 (D-21, banked) is of the same order as the literature's Rayleigh boundary, up to the correlation-length convention, which this gate does not fix; it is not re-derived. Under E-SA-4(a) the clause is effectively vacuous. No collision |
| **L-SA-4** emergent species universality; bounds turned into constraints on the medium | Chadha–Nielsen, NPB 217, 125 (1983) (AB: "this model simulates Lorentz invariance better and better as the energy scale is progressively lowered"); Collins–Perez–Sudarsky–Urrutia–Vucetich, PRL 93, 191301 (2004) (AB: "unless the bare parameters of the theory are unnaturally strongly fine-tuned"); Iengo–Russo–Serone, JHEP 11 (2009) 020 (AB); Anber–Donoghue, PRD 83, 105027 (2011) (FT: "The largest velocity difference should be in system with the weakest interaction"); Bednik–Pujolàs–Sibiryakov, JHEP 11 (2013) 064 (AB); Liberati–Visser–Weinfurtner, PRL 96, 151301 (2006) (FT: "They both 'experience' the same space-time if the sound speeds are equal") and CQG 23, 3129 (2006) (FT); Barceló–Liberati–Visser, Living Rev. Relativ. 8, 12 (2005) and 14, 3 (2011) (FT, partial: "in superfluids there will be multiple acoustic metrics"); Oost–Mukohyama–Wang, PRD 97, 124023 (2018) (FT); Gümrükçüoğlu–Saravani–Sotiriou, PRD 97, 024032 (2018) (FT); Baker et al., PRL 119, 251301 (2017) (FT); Creminelli–Vernizzi, PRL 119, 251302 (2017) (FT); Sakstein–Jain, PRL 119, 251303 (2017) (FT: "none other than the fractional difference between the speed of gravitons and photons"); Ezquiaga–Zumalacárregui, PRL 119, 251304 (2017) (FT: on perturbed backgrounds the tensor speed "depends on the direction and can not be compensated"); Liang–Xu–Lu–Shao, PRD 106, 124019 (2022) (FT: the tensor propagation speed "depends on the angle β between k̂ and b̂"); Araújo Filho, arXiv:2603.08310 (2026; journal reference not confirmed) (FT: "For a generic spacelike orientation, the same argument constrains the projected combination") | Emergent convergence of species speeds is infrared-attractive but generally logarithmic; residual differences vanish only with fine-tuning or strong coupling; gravity versus light is named the most stringent test. One effective metric for all excitations needs coinciding mode speeds; generic media are multi-metric. After the 2017 event, the bound fixes the coupling that sets the tensor speed (Einstein-aether, Hořava, scalar-tensor). Of these, only Ezquiaga–Zumalacárregui treats direction. Spacelike background-vector models project the bound onto the event's direction, and propagation orthogonal to the background sees nothing. No work that maps the bound onto an orientation distribution was located | E-MS-1(a)'s identity form is the framework's answer to the naturalness obligation (G-MSCS1 §12): one phonon, two descriptors, so equality is an identity on the untextured aggregate rather than a tuned coincidence. The texture breaks it only at second order in the sphere-weighted reading. The background-vector projection is the nearest prior art to ST-1's logic: a null direction set by a background orientation (orthogonal to the vector there; along the fiber axis here). No collision |
| **L-SA-5** collision check | 15 queries: the vacuum as a polycrystal; orientation texture; crystalline or elastic spacetime and the tensor speed; the world crystal; solid and elastic dark energy; nematic spacetime; Lorentz-violation domains; the direction-averaged tensor speed. Adjacent lanes read: Kleinert, Braz. J. Phys. 35, 359 (2005) and Kleinert–Zaanen, PLA 324, 361 (2004) (FT; gravity from the defects or nematic order of a Planck-scale crystal — no species speeds, texture or bound); Danielewski 2007 (LS), a 2010 talk abstract (AB: "The transverse wave is the electromagnetic wave and its velocity equals the velocity of light"), and Danielewski–Sapa–Roth, Symmetry 15, 1672 (2023) (AB); Tartaglia–Radicella, CQG 27, 035001 (2010) (AB) and AIP Conf. Proc. 1241, 1128 (2010) (AB); Tenev–Horstemeyer, IJMPD 27, 1850083 (2018) (FT; isotropic elastic spacetime); Bernadotte–Klinkhamer, PRD 75, 024028 (2007) (FT: photon bounds mapped onto a vacuum of defects with a "homogeneous and isotropic (randomly oriented) distribution"); Battye–Moss, PRD 80, 023531 (2009) (FT; dark energy that "could represent a cubic or hexagonal crystalline lattice") and Battye–Pace–Trinh, PRD 98, 023504 (2018) (FT; the tensor-speed bound applied to isotropic elastic dark energy); Schreck–da Silva Magalhães, arXiv:2604.17646 (2026) (FT; single-crystal point groups mapped to photon-sector coefficients); Rodgers, *Gravitational Wave Propagation Speed and Lorentz-Violation Bounds*, Zenodo, DOI 10.5281/zenodo.22727182 (September 12, 2026) (AB — record verified; description only: the two speeds are equal "as a forced consequence of both phenomena propagating across the identical underlying lattice substrate"; per the independent audit's reading of the same description, it also applies a sixfold rotational-symmetry suppression argument to tensor-wave dispersion — a lattice-symmetry argument adjacent to this gate's hex branch) | No work was located that maps a multi-messenger speed bound onto an orientation-texture coefficient of a polycrystalline vacuum. The nearest method precedent is Bernadotte–Klinkhamer: bounds mapped onto the parameters of an orientation-distributed defect vacuum, but photon-only, with no grains and no species comparison. The nearest object is Danielewski: light as the transverse wave of a cubic Planck crystal, with no texture and no bound. The Rodgers preprint sits in the untextured-identity lane (E-MS-1(a)'s neighbour); its description names no texture, and its full text was not read | **Novel-in-assembly; A0 not triggered.** Honest ceiling: every ingredient is textbook or elementary — the TI of a fiber aggregate, the along-axis degeneracy, the projection of a one-sightline bound, and the sphere-weighted second-order split banked at G-MSCS1/2. The novelty is the assembly. Residual risk recorded: the Rodgers preprint at AB, to be read in full before lock (§15 item 8) |

## 15. Disclosures and the pre-lock state

1. **D-SA-0 (blindness, stated plainly).** The chat leg is not informationally blind to the public multi-messenger speed bounds. They are in the literature, and their digit strings are in the G-MSCS1 stratum this gate carries (composed chat-side at G-MSCS1). Blindness is procedural:
   - the sealed file is author-supplied and never in the clear;
   - T1-A1 is author-supplied;
   - the CC read is the read of record;
   - every coefficient, domain, margin, rule and tolerance is pinned before any anchor exists (in v2, in a file the author verifies before lock), so the mapping has nothing left to tune.

   The LSF-δ read (§14) re-read the dialect's primary sources for their conventions only: sign, sidedness, confidence semantics, sightline and bands. It read no value. This memo names no anchor source by identifier and quotes no bound.
2. **Pre-draft sanity check (not a gate result).** `sa_predraft_directional_check.py` (v2, md5 `444ddf23…`) produced the S-SA-1 numbers on the G-MSCS1 F-CTRL-TEX synthetic tensor (C11, C12, C13, C33, C44, C66 = 300, 100, 50, 200, 40, 100): no banked tensor, no ledger value, no anchor. It reproduced the SO(3)-identity control (E₂ weight 2/5 at t = 0) to 5.6×10⁻¹⁶. Unchanged from v1. E-SA-3(b) was declined, so no leg re-derives it.
3. **Numbers.** The v1 preview scripts (`sa_pinned_preview.py` `0b87d4a2…`, `sa_pinned_preview_ext.py` `5c2e5730…`, `sa_reach_v3.py` `5e582eb2…`) are superseded by the builder. Every number in §0, §B, §2, §3, §5, §6, §7 and §8 that is not quoted from the ledger or a lock record is output by the builder and re-derived by the verifier from the pinned file. That includes the derived constants 404.9, 7.97×10³¹ m⁻¹, 1.0745 and 3.33×10⁻¹⁶. The exceptions: the S-SA-1 numbers (the pre-draft script, item 2); 0.1414 m⁻¹, the W_∪′ figure of the declined E-SA-4(c), from the v1 preview (`sa_reach_v3.py`) and carried by no instrument; the bibliographic content of §14; and a few figures hand-computed from builder output, each with its arithmetic stated where it is used — the (a)/(b) agreement figures of D-11 and F-CTRL-SA-RECON, the S-SA-4 edge shifts (half the fit resolution), the H-MS2-9 A-3.1 percentages, and the conservative regime thresholds 7.96×10³¹ and 0.1415 m⁻¹. The §12 repository facts are from `git ls-remote` and `git log`, quoted.
4. **Tools:**
   - `sa_build_pinned_inputs.py` (`8189100e…`) — new;
   - `sa_verify_pinned_inputs.py` (`cf004d51…`) — new; rewritten after the v2 audit;
   - `sa_anchor_validate.py` (v2, `3a11c8f1…`) — author-side, unchanged since v1;
   - `sa_t1a1_build.py` (v2, `dc7a747e…`) — author-side, unchanged since v1.

   The builder's determinism was tested under four Python versions (identical md5). The verifier was tested on 37 tampered copies. Nineteen are from the independent audit's first pass: derived fields the first verifier did not re-derive, constants, tokens, structure, a dropped arm, and a redirected pointer with a consistent raw value — all nineteen had passed the first verifier. Four are from its second pass: a free-text `_meta` field rewritten (two cases), a derived 0.0 written as the integer 0, and a wrong embedded builder md5 with no builder argument given. Fourteen more: a raw value scaled by 1 + 10⁻¹⁵, a derived edge scaled by 1.0001, an unprovenanced raw value, μ changed, the last digit of d_EM changed, a count field written, a grid value moved by 10⁻¹⁸, a synthetic interval, a synthetic constant, a CC value, a derived leaf deleted, a derived leaf added, an election in `_meta`, and the embedded builder md5. Each copy failed with its own reason. One further probe, a derived value moved 5×10⁻¹³ relative, passes the verifier by design (below its tolerance) and is caught by the whole-file md5.
5. **H-SA-1 — DISCHARGED** (v1): the V4.86 canonical in the project store is byte-identical to the record.
6. **Independent audits.** v1 was audited in two passes by an agent that had not seen the drafting (18 errors and 9 suggestions in the first pass, then 9 issues introduced by the rewrite; every item corrected in v1; v1 §15 item 6). The v2 audit: an agent that had not seen the drafting audited v2 before delivery (September 29). It reported 4 errors, 7 minor issues and 6 suggestions, and every item is dispositioned in this file (§C items 3–5 and 9–10; E-v2-6).
   - **The four errors:**
     1. the verifier's coverage was overstated, and it trusted the file under test. It is rewritten: it now holds its own pointer map, constants, tokens and structure and re-derives every leaf; 19 of the auditor's tampered copies had passed the first verifier, and all 37 fail the new one.
     2. the fit resolution was stated for all arms but held for S2-E₂ Hill only (S-SA-4, §6.4).
     3. C-SYN-12 could not be built from the pinned budgets, and C-SYN-13 only by coincidence. The synthetic generators are now pinned, and C-SYN-3's robustness-only interval with them, for definiteness.
     4. ST-5 was false for intervals excluding 0 (corrected).
   - **Minor issues:** the §3.6 t₂ scope; S-SA-11 item 2; seven more rounded values; RECON detection power for κ₂; the fcc 5 × 5 residual attribution; the completeness of the change record (the declined options are restored verbatim); and wording.
   - **Suggestions adopted:** H-SA-4; the scope of the origin search; the Rodgers note and its pre-lock read; the CC counterparts of κ₃, S and b₁ pinned; the U+2212 note in S-SA-10; v1's retrievability.
   - **What the auditor confirmed:**
     - byte-identical regeneration of the pinned file under Python 3.10–3.13 from `e1fa071`;
     - every κ-table, reach, union, MARGIN-band, null-ray, two-leg, preflight and count value;
     - the H-MS2-9 anchors, values and origin within the available history;
     - the H-SA-3 citations;
     - 21 LSF quotes, verbatim;
     - that nothing in the memo evaluates or reveals a bound value;
     - T1 CLEAN on every artifact.
   - **A focused second pass** on the corrected file (September 29):
     - It found every first-pass item fixed.
     - The pinned file regenerates byte-identically under Python 3.10–3.13.
     - The rewritten verifier failed all 33 tampered copies. Of seven further probes, three classes are now closed as well (free-text metadata, integer-typed values, the builder md5 when none is supplied); the fourth, sub-tolerance values, is left to the whole-file md5 by design.
     - The pinned synthetic intervals give their stated classes, and ST-5 held on 200,000 random intervals.
     - T1 is CLEAN.
     - It found no errors and no rounding regressions. It raised eight minor wording and consistency items and one suggestion (two further round-downs in the banked record, now part of H-SA-4), all dispositioned in this file.
7. **LSF-δ execution (disclosed).** Three sub-agents ran the searches, with the instructions summarized in §14. The chat leg verified three records directly. One fetch permission (the Zenodo file listing) was not answered, so the Rodgers preprint stays at AB, and that is recorded as the residual collision risk.
8. **Pre-lock conditions, remaining — in this order:**
   1. the author regenerates and verifies the pinned inputs (§9) and gives the word "pinned inputs verified";
   2. the Rodgers preprint (L-SA-5) read in full, by the author or the CC leg (the chat leg's fetches were blocked); if it maps a speed bound onto a lattice orientation texture, A0 is re-examined before lock;
   3. the T1 gate list `tools/t1/T1_forbidden_G_MSCS_A.txt` composed;
   4. schema v1.0 + comparator v1.0 written and self-tested;
   5. the lock record with Addendum A-2. The operationalizations — the synthetic generators, the Richardson step pairs, the area-grid generator, the `odf_reading` token set, μ — are now carried by the pinned file's `constants`, `grids` and `tokens`; the reason-code list belongs to schema v1.0. The record cites the md5s of this memo, the pinned file, the builder, the verifier, the T1 list, the schema and the comparator;
   6. **the author's word "Lock"**, at which items 3–5 freeze (§5, step 3).

   The chat mapper, the pre-read suites and the sealed delivery then follow the §5 order.
9. **T1 scan of this file:** CLEAN — 0 hits and 0 formatting collisions under `be921b8c` (36 patterns), under the base `05302210` alone, and under the courtesy list `04438b74`; scanner `t1_scan.py` `6b862900`. The scan ran on this file as delivered (the placeholders filled), September 29, 2026.

*v2 DRAFT, September 29, 2026. Base V4.86 (d4c42a53). Elections applied. Not locked.*

=====END-EMBED name=staging_memo_G_MSCS_A_v2.md=====

=====BEGIN-EMBED name=G_MSCS_A_LOCK_RECORD.md md5=8116cc622279b5d4e73214178ae97cd8 bytes=17923 encoding=raw=====
# G-MSCS-A — LOCK RECORD (September 29, 2026)

**Gate:** G-MSCS-A (the sealed-anchor mini-gate on the texture constraint surface r_agg = κ₂₂t₂² + κ₄₄t₄² — the registered successor of G-MSCS1 / G-MSCS2; G-MSCS1 kill-surface item (iii)). **Base:** V4.86 `d4c42a53cbd6d325ebc740879288e844` (1,730,321 B). **Authorization:** the author's directive of September 29, 2026, 19:00 PDT — pre-lock conditions item 4: "All conditions have been met. 'Lock.'" — after "Pinned inputs verified." (item 1), the Rodgers read (item 2), and the Q-SA-2 / Q-SA-3 answers (item 3), each recorded verbatim in §3 below.

## 1. Locked artifacts (frozen at these hashes; never edited after this record)

| Artifact | md5 | Bytes | Role |
|---|---|---|---|
| `staging_memo_G_MSCS_A_v2.md` | **`6ea16b952db835bb351d3dc1b474c6ed`** | 121,950 | the locked memo (v2; draft v1 `a7d6bdbc` superseded; the file's own status line reads "DRAFT — NOT LOCKED" and is superseded by this record, the G-MSCS2 pattern) |
| `pinned_inputs_G_MSCS_A.json` | **`2d44ec01a66889f330d940dee3313bdc`** | 96,761 | the pinned inputs of record — generated before lock, verified by the author (§3) |
| `sa_build_pinned_inputs.py` | `8189100ede80eac360b25a146e580abf` | 41,342 | the builder (memo §9); its md5 is embedded in the pinned file |
| `sa_verify_pinned_inputs.py` | `cf004d517d2efe91a02c92a58e3df6bf` | 28,804 | the independent verifier (memo §9) |
| `tools/t1/T1_forbidden_G_MSCS_A.txt` | **`e274e58ea50b9ed347969e507d2a4f36`** | 1,482 | gate T1 list: the 36 pattern lines of `be921b8c` verbatim (base `05302210` 11 + the G-MSCS1 stratum 25), header naming this gate |
| `tools/t1/T1_base_author_20260919.txt` | `05302210cc4ceb70553acbe8379e9fc3` | 143 | base stratum |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 | scanner (contextual numeric rule) |
| `g_mscs_a_schema_v1_0.json` | **`5323e11fc27d688f61aaf57302c875c0`** | 9,436 | checkpoint schema v1.0 — FROZEN pre-emission |
| `g_mscs_a_compare_v1_0.py` | **`c5b4a7aab2fc8651be6d26d1f3d25642`** | 16,850 | comparator v1.0 — FROZEN pre-emission; asserts the schema md5; 22/22 adversarial suites |
| `sa_anchor_validate.py` | `3a11c8f1421d26b882097dbd4e0759d7` | 7,604 | author-side validator (memo §4.7) |
| `sa_t1a1_build.py` | `dc7a747e91ce57cd8305296e579b09f3` | 4,367 | author-side T1-A1 builder (memo §4.6) |

Elections (T3-immutable): E-SA-0 (a) · E-SA-1 (a) · E-SA-2 (a) · E-SA-3 (a) · E-SA-4 (a) · E-SA-5 (a) · E-SA-6 (a) · E-SA-7 base `05302210` + the G-MSCS1 stratum · E-SA-8 (a) · E-SA-9 (a) · E-SA-10 (a) · E-SA-11 (a). Schema `elections` codes: `a` ×11 and `05302210+MSCS1stratum`.

**Not locked by this record:** the chat mapper (written after lock; its md5 is frozen when the pre-read suites are green and is recorded in the chat-leg checkpoint `instrument_md5` and the execution report — memo §5 step 4); the author's sealed file and T1-A1 (memo §5 step 5); the CC mapper.

**Repository state at lock (recorded as observed, the V4.86 `ls-remote` rule):** `git ls-remote origin refs/heads/main` at 2026-09-30 02:05:51 UTC → `e1fa071758a0912472bbb6eba7f77fab35669807` (PR #31 merge), unchanged since the v1 and v2 observations. The seven pinned sources are at their md5s of record on that commit. Not load-bearing for the gate beyond the source guards.

## 2. Addendum A-2 — operationalizations (binding for both legs; CC re-derives from these words, the memo and the pinned file, not from chat code)

**A-2.1 Inputs.** The pinned file `2d44ec01` is the only banked input; the sealed file is the only other input. Every value the mapper uses is read from the pinned file by name: `raw.keys[K].arms[ARM][FAM].{kappa, kappa_cc, grid, S, S_cc, kappa3, kappa3_cc}`, `raw.keys[K].quadform.*`, `raw.keys[K].{kappa24_bi_chat, kappa24_bi_cc, b1_Hill, b1_Hill_cc, pure_l2_change_t1, A31_mixed_change_cc}`, `raw.regime.d_EM`, `constants.*`, `grids.*`, `structure.*`, `tokens.*`, `derived.*`. Keys in the order `hex_step|a`, `hex_step|b`, `hex_gem8|a`, `hex_gem8|b`, `cubic_step|001`, `cubic_step|111`, `cubic_gem8|001`, `cubic_gem8|111`; arms `E2_Hill` (primary), `E2_HSmean`, `h_Hill`; primary keys `hex_step|a`, `hex_gem8|a`, `cubic_step|001`, `cubic_gem8|001`. Mapped families: t₄ on every key, t₂ on hex keys; the cubic t₂ family is the null family (NULL-INERT).

**A-2.2 Phase 0 (each control halts the run on failure; the checkpoint records `passed` and the floats the schema names, with the `odf_reading` token).**
- PIN: the pinned file's md5 equals `2d44ec01…`; every `raw` value is re-read from its source through the pointer in `provenance` (the seven sources at their md5s of record, from a clone of `main` supplied to the mapper) and must equal the pinned value bit for bit (`raw_mismatches` = 0); two-leg agreement of the banked coefficients: κ and κ₃ ≤ 1×10⁻⁴ relative (|a − b|/max(|a|, |b|), a coefficient counted only where max(|a|, |b|) > the κ floor), b₁ ≤ 1×10⁻⁴ relative, S ≤ τ_agg absolute.
- PIN-DERIVED: re-derive `derived.families`, `derived.reach`, `derived.unions`, `derived.synthetic`, `derived.nulls`, `derived.hex_quadform` and `derived.zero_ctrl` from `raw`, `constants` and `grids` with the leg's own code (the formulas of memo §3.3–§3.6 and §6.2; the Richardson forms in `grids.richardson_formulas`; the 5 × 5 layout in `grids.grid5x5_layout`); every leaf must match within |Δ| ≤ 1×10⁻¹²·|x| + 1×10⁻¹⁶ (`worst_scaled_dev` = max |Δ|/(1×10⁻¹²·|x| + 1×10⁻¹⁶) ≤ 1; non-numeric leaves exact; the leaf sets identical, `leaf_mismatches` = 0). `derived.summary` is not required of the legs.
- ZERO: |r(0)| ≤ 1×10⁻¹² on every key, arm and family (the grid value at t = 0).
- RECON: on `E2_Hill`, max over the nine inclusive points |t| ≤ D of |grid − (S·t + κt² + κ₃t³)| ≤ 1×10⁻⁸ per mapped family; on `E2_HSmean` and `h_Hill`, |κ − κ_bi|/|κ_bi| ≤ 1×10⁻³ per mapped family.
- S (N-1): |S_bi| ≤ τ_agg on every key × arm × mapped family, and |S| ≤ τ_agg where S is banked (`E2_Hill`, `h_Hill`).
- K24 (N-2): |κ₂₄| ≤ the κ floor for each of `bi_chat`, `bi_cc`, the leg's own 5 × 5 mixed Richardson estimate, and `fit7`, on all eight keys.
- L2NULL (N-3, N-4): on the cubic keys |κ₂| (fit) and |κ₂_bi| ≤ the κ floor; |κ₂₂ fit7|, |κ₂₂ bi_5x5| and, where banked, |k12[0]| ≤ the κ floor; |pure_l2_change_t1| ≤ 1×10⁻¹²; the `cubP2-ii` identity is asserted symbolically (a string in the record, no number).
- SIGN: with the asymmetric synthetic interval [−|κ_ref|·0.1², +|κ_ref|·0.05²] (κ_ref = `hex_step|a` `E2_Hill` t₄ κ), the binding end must be `hi` where κ > 0 and `lo` where κ < 0 on every key × arm × mapped family (`binding_end_mismatches` = 0).
- GRID: the counts `n_t_grid`, `n_fit_window_inclusive` (|t| ≤ D), `n_fit_window_strict` (|t| < D), `n_window_0p1_inclusive`, `n_window_0p1_strict`, `n_t2t4_axis`, `n_t2t4_grid`, `n_area_grid` are computed from the generators at run time and written; the comparator recomputes and rejects any difference.
- MONO: for the synthetic intervals of C-SYN-1 (t_syn ∈ {0.01, 0.1, 0.5}) scaled ×10 and ×0.1: every unclipped t\* (BINDING) scales by exactly √10 / √0.1 (relative deviation ≤ 1×10⁻¹⁴); windows and classes monotone — under ×10 no window narrows and no class moves from INERT-IN-D to BINDING; under ×0.1 no window widens and no class moves from BINDING to INERT-IN-D (`monotonicity_violations` = 0).
- MASK: the sealed file is opened only in Phase 3; the checkpoint records `sealed_opens_before_phase3` = 0.
- T1: the instrument, the memo, the pinned file (and, when present, the lock record, schema and comparator) scanned under the gate list ∪ A1 (A1 required in Phase 3, optional before); `hits` = 0; collisions logged.

**A-2.3 The sealed file (memo §4).** Delivered armored: either a base64 text file (BEGIN/END marker lines permitted and stripped; whitespace ignored) or a zip archive containing exactly one member. The mapper decodes it, asserts the author's stated md5 and byte count of the unarmored file, and parses with its own masked parser implementing §4.1–§4.4 exactly: UTF-8 without BOM; LF only; no control character except LF; no U+FEFF, U+0085, U+2028, U+2029; one row per line; the separator ` | `; no bar elsewhere; the first `=` splits key and value; keys in the canonical order (eleven required, then `q`, `note`); `id` = `SA-n` in file order; `class` = `spd`; `delta_def` = `tensor_over_EM_minus_1`; `lo`, `hi` plain ASCII numbers with lo ≤ hi; `cl` in (0, 1) or `hard`; `reading` = `bound` (`ceiling`, `margin`, `criterion` → READING_NOT_MAPPED); `geom` ∈ {`single`, `population`}; `k_em_max`, `k_t_max` positive plain numbers; `q` ∈ {`phase`, `group`}; every field but `src` and `note` printable ASCII. A non-conformant file aborts with a reason code and nothing else (the read not spent). Census = {rows, per_class, fields_per_row}; row md5 = md5 of the row's bytes (without the LF); sealed md5 = md5 of the whole unarmored file.

**A-2.4 The mapping (memo §3).**
- Per row j: I_j = [lo_j, hi_j]; x_j = max(k_em_max, k_t_max) × d_EM; x_j > KD_CLIP (0.3) → VOID-REGIME. Combined I = ∩ over non-VOID rows. All rows VOID → gate VOID. I = ∅ → ANCHOR-INCONSISTENT. Per-row mappings are serialized with the same structure as the combined one.
- I ∋ 0 (lo ≤ 0 ≤ hi): per key, arm, mapped family with κ (of record) and D = 0.25: binding end b = hi if κ > 0 else lo; t\* = √(b/κ) (t\* = 0 if b = 0); BINDING iff t\* < D, window [−t\*, +t\*]; else INERT-IN-D, window [−D, +D]. The same with κ_bi → `class_bi`, `t_star_bi`; `resolution_sensitive` = (class ≠ class_bi). On `E2_Hill`: T = |κ₃|·t\*/|κ|, `truncation_sensitive` = (T > 0.10); on the robustness arms T is null and the flag false. ν = |S_bi|·t\*/|b| with `nu_is_inf` = true and the flag set when b = 0; `nullfloor_sensitive` = (ν > 0.10). σ\* = t\*·rms with rms = 1/3 (hex t₄), √(4/21) (cubic t₄), √(1/5) (t₂). The cubic t₂ family: class NULL-INERT, window [−D, +D], the other fields null.
- I ∌ 0: per key and arm with R^h = `derived.reach[K][ARM].hull` and R^w = `.widened`: EXCLUDED-IN-D iff I ∩ R^w = ∅ (closed intervals), sub-reason SIGN if R^w lies wholly on the other side of 0 from I (hi < 0 and R^w[0] ≥ 0, or lo > 0 and R^w[1] ≤ 0), else MAGNITUDE; TUNED-ADMISSIBLE iff I ∩ R^h ≠ ∅; otherwise MARGIN. Requirements per family with sign(κ) = sign(δ): t_in = √(min(|lo|, |hi|)/|κ|), t_out = √(max(|lo|, |hi|)/|κ|), `can_supply_alone` = (t_in ≤ D); families with the other sign: null.
- Two-parameter region (hex keys, every arm, I ∋ 0 only): A₂₄ = {(t₂, t₄) on the 201 × 201 area grid of D × D: κ₂t₂² + κ₄₄t₄² ∈ I} with κ₂ = the arm's t₂ κ of record and κ₄₄ = the arm's t₄ κ of record; `area_fraction` = admissible nodes / total nodes (both counts computed); `null_ray_slope` = √(−κ₂/κ₄₄) where κ₂κ₄₄ < 0 else null; `definiteness` ∈ {indefinite, negative-definite, positive-definite}; `compact` = no admissible node lies on the boundary of the area grid.
- Gate class, in precedence: INDETERMINATE (any Phase-0 failure) > VOID > ANCHOR-INCONSISTENT > KILL-IN-D (I ∌ 0 and EXCLUDED-IN-D on all 24 (key, arm) cells — E-SA-9(a)) > TUNED (I ∌ 0 and TUNED-ADMISSIBLE on ≥ 1 cell) > MARGIN-ONLY (I ∌ 0, otherwise) > WINDOW-DELIVERED (I ∋ 0 and the four primary keys BINDING on t₄ on `E2_Hill`) > INERT-IN-D.
- Gate-level windows (I ∋ 0): `sigma_union_hi` = max over the primary keys of σ₄\* (the CONSERVATIVE union); `sigma_strict_hi` = min (serialized, non-verdict); both null unless every primary key is BINDING on t₄.
- OOM: the whole mapping repeated with every row's lo and hi scaled ×10 and ×0.1; `oom_robust` = (the three gate classes identical); the monotonicity check of A-2.2 MONO applied to the actual rows halts as an instrument defect (S9), never a finding.

**A-2.5 Phase 2 suites (all must pass before any sealed open; k_em_max = k_t_max = `synthetic_k.silent` unless stated).** Budgets b(t) = |κ_ref|·t² with κ_ref = `hex_step|a` `E2_Hill` t₄ κ and t ∈ `synthetic_t` = {0.01, 0.1, 0.5}. C-SYN-1 [−b(t), +b(t)]: on the reference cell t\* = t to 1×10⁻¹² relative, BINDING for t < D and INERT-IN-D for t = 0.5; every other cell's t\* equals √(b/|κ_cell|) recomputed. C-SYN-2 [−b(0.1), +b(0.05)]: binding ends by sign(κ); t\* = 0.05·√(|κ_ref|/|κ|) on κ > 0 cells and 0.1·√(|κ_ref|/|κ|) on κ < 0 cells. C-SYN-3: (i) [10·U⁺, 20·U⁺] with U⁺ = `unions.widened_all[1]` → EXCLUDED on every cell (MAGNITUDE where R^w[1] > 0, SIGN where R^w[1] = 0), gate KILL-IN-D; (ii) [20·U⁻, 10·U⁻] with U⁻ = `unions.widened_all[0]` → the mirror, gate KILL-IN-D; (iii) [0.25·H⁺, 0.5·H⁺] with H⁺ = `unions.hull_all[1]` → TUNED on ≥ 1 cell, gate TUNED; (iv) `derived.synthetic.robustness_only_positive` → no primary-arm primary-key cell TUNED, ≥ 1 robustness cell TUNED, gate TUNED. C-SYN-4 [−1, +1] → INERT-IN-D on every mapped cell, gate INERT-IN-D. C-SYN-5 the cubic t₂ family is NULL-INERT under C-SYN-1. C-SYN-6 the fifteen malformed files of memo §4.7 and one valid file, generated with distinctive synthetic values → every malformed file aborts with a reason code; the mapper's stdout, the reason codes and the checkpoint contain none of the synthetic values (fixed-string search). C-SYN-7 the MONO check on the C-SYN-1 intervals. C-SYN-8 rows [−b(0.1), +b(0.1)] and [−b(0.05), +b(0.2)] → I = [−b(0.05), +b(0.1)]. C-SYN-9 rows [b(0.1), b(0.2)] and [−b(0.2), −b(0.1)] → ANCHOR-INCONSISTENT. C-SYN-10 a row with k = `synthetic_k.void` (1×10³³ m⁻¹) → VOID-REGIME; alone → gate VOID; with a silent C-SYN-1 row → the silent row alone is mapped. C-SYN-11 [0, 0] → t\* = 0, ν = ∞, NULL-FLOOR on every mapped cell, BINDING, gate WINDOW-DELIVERED. C-SYN-12 t = `synthetic_t_tight` = 1×10⁻⁹ → the flag on each cell equals (|S_bi|·t\*/b > 0.1) recomputed, with ≥ 1 cell set and ≥ 1 cell clear. C-SYN-13 `derived.synthetic.margin_positive` and `margin_negative` → no cell TUNED, ≥ 1 cell MARGIN, gate MARGIN-ONLY. C-SYN-14 the reach of `cubic_step|001` `E2_Hill` rebuilt from a copy of its grid with +5×10⁻¹³ added at t = 0.02 → hull[1] snapped to 0; a positive interval classes SIGN.

**A-2.6 Checkpoint discipline.** One checkpoint per leg per run; a Phase 0 + 2 run (before any sealed file) writes `g_mscs_a_<leg>_prereadcheckpoint.json` with `phase3` = null; the read writes `g_mscs_a_<leg>_checkpoint.json`, recomputing Phases 0 and 2 from scratch. Floats at full double precision; sorted keys; the checkpoint is T1-scanned after writing (`T1_post_write`) under the gate list ∪ A1 and deleted on a hit. No field of any checkpoint carries lo, hi, k_em_max, k_t_max, cl, src or note; the comparator refuses a checkpoint that does.

## 3. The author's pre-lock words (verbatim, directive of September 29, 2026, 19:00 PDT)

1. *Pinned inputs:* "I have independently verified the pinned_inputs_G_MSCS_A.json output against the stated values in the staging memo. The counts, grids, robust null thresholds, and synthetic generators align correctly with the definitions we established. 'Pinned inputs verified.'"
2. *Rodgers preprint (memo §15 item 8.2; L-SA-5 residual risk):* "The Rodgers preprint explores dispersion effects modeled on a static crystalline medium but explicitly models gravitational wave propagation through a scalar deformation potential, lacking any directional tensor component coupling to a physical orientation distribution function (ODF). It derives an effectively isotropic wave equation where the lattice spacing dictates a high-frequency cutoff, but no orientation-texture coefficients are derived, bounded, or bounded against multi-messenger signals. Therefore, A0 is NOT triggered." — The L-SA-5 verdict (novel-in-assembly; A0 not triggered) stands with the residual risk discharged by the author's full read; the ceiling for that source is now FT (author).
3. *Q-SA-2:* "Yes. H-SA-3 (the Man–Huang citation) and H-SA-4 (the three round-downs) must join the H-MS2-9 bracket for the next fold. Do not leave them as 'recorded here only.'" *Q-SA-3:* "Yes. Include an estate erratum file (H_MS2_9_ERRATUM.md) detailing H-MS2-9, H-SA-3, and H-SA-4." — Both carried: `estate/H_MS2_9_ERRATUM.md` is drafted alongside this record for the next housekeeping PR, and the next fold's bracket carries H-MS2-9, H-SA-3 and H-SA-4 (memo §12).
4. *Lock:* "All conditions have been met. 'Lock.' Proceed to freeze the T1 list, the schema v1.0, and the comparator v1.0, and write the lock record. Once those are established, build the chat mapper, ensure the pre-read suites are green, freeze the mapper MD5, and report back. I will prepare the sealed anchor delivery while you execute these steps."

## 4. Order of operations (binding; memo §5)

This record (memo md5; T1 list frozen; schema + comparator frozen) → the chat mapper written → Phase 0 + Phase 2 green (pre-read checkpoint) → mapper md5 frozen, reported → **the author supplies the sealed file + T1-A1 (memo §4.6)** → the chat leg confirms md5, bytes and census; the A1 pre-freeze collision scan over every locked artifact and the mapper; A1 frozen → dispatch (P-4; P-4.b with the sealed file armored; P-4.c delivered alone) → CC blind read from scratch (CC-BLIND-FIRST; its own parser, binder and class logic) → chat read → two-leg comparison with the frozen comparator → S9 on misses → fold authorization → V4.87, which carries H-MS2-9, H-SA-3 and H-SA-4 unless an earlier fold does.

*Lock record written September 29, 2026 (September 30, 02:06 UTC). Base V4.86 (d4c42a53).*

=====END-EMBED name=G_MSCS_A_LOCK_RECORD.md=====

=====BEGIN-EMBED name=g_mscs_a_schema_v1_0.json md5=5323e11fc27d688f61aaf57302c875c0 bytes=9436 encoding=raw=====
{
 "anchor_tokens": {
  "class": [
   "spd"
  ],
  "delta_def": "tensor_over_EM_minus_1",
  "geom": [
   "single",
   "population"
  ],
  "q": [
   "phase",
   "group"
  ],
  "reading_conformant": [
   "bound"
  ],
  "reading_frozen_list": [
   "bound",
   "ceiling",
   "margin",
   "criterion"
  ]
 },
 "arms": [
  "E2_Hill",
  "E2_HSmean",
  "h_Hill"
 ],
 "builder_md5": "8189100ede80eac360b25a146e580abf",
 "comparison_rules": {
  "C-SA-0": "provenance: memo_lock_md5, pinned_inputs_md5, t1_list_md5, schema_md5, elections, ledger_base_md5 equal this schema on both legs; phase0 passed on both legs with float rules re-evaluated; phase2 suites all passed on both legs",
  "C-SA-1": "every numeric field of phase3 (edges, windows, sigma, t_in/t_out, area fractions, nu) compared across legs at |a-b| <= edge_twoleg_rel*max(|a|,|b|) + edge_twoleg_abs_floor; null compares only to null",
  "C-SA-2": "every class, sub-reason, flag and OOM class of phase3 identical across legs (strings/bools exact)",
  "C-SA-3": "sealed_md5, sealed_bytes, census and row_md5s identical",
  "C-SA-4": "pinned_inputs_md5 on both legs equals this schema's",
  "C-SA-5": "every null of nulls within its tolerance on each leg, tokens present and identical, values across legs at pin_derived_rel",
  "C-SA-6": "F-CTRL-SA-T1 hits == 0 on both legs; T1_post_write hits == 0 on both legs",
  "C-SA-7": "grid counts recomputed from the generators equal the checkpoint counts on both legs",
  "C-SA-8": "instrument_md5 differs between legs (independence witness)",
  "free_text": "never compared"
 },
 "cubic_keys": [
  "cubic_step|001",
  "cubic_step|111",
  "cubic_gem8|001",
  "cubic_gem8|111"
 ],
 "elections": {
  "E-SA-0": "a",
  "E-SA-1": "a",
  "E-SA-10": "a",
  "E-SA-11": "a",
  "E-SA-2": "a",
  "E-SA-3": "a",
  "E-SA-4": "a",
  "E-SA-5": "a",
  "E-SA-6": "a",
  "E-SA-7": "05302210+MSCS1stratum",
  "E-SA-8": "a",
  "E-SA-9": "a"
 },
 "families": {
  "cubic": [
   "t4"
  ],
  "hex": [
   "t4",
   "t2"
  ],
  "null": {
   "cubic": [
    "t2"
   ]
  }
 },
 "frozen": "2026-09-29",
 "gate": "G-MSCS-A",
 "grids": {
  "count_fields": [
   "n_t_grid",
   "n_fit_window_inclusive",
   "n_fit_window_strict",
   "n_window_0p1_inclusive",
   "n_window_0p1_strict",
   "n_t2t4_axis",
   "n_t2t4_grid",
   "n_area_grid"
  ],
  "rule": "generators only; the comparator recomputes every count from t_grid, t2t4_axis, D and area_grid and rejects a checkpoint whose count fields differ"
 },
 "hex_keys": [
  "hex_step|a",
  "hex_step|b",
  "hex_gem8|a",
  "hex_gem8|b"
 ],
 "keys": [
  "hex_step|a",
  "hex_step|b",
  "hex_gem8|a",
  "hex_gem8|b",
  "cubic_step|001",
  "cubic_step|111",
  "cubic_gem8|001",
  "cubic_gem8|111"
 ],
 "ledger_base_md5": "d4c42a53cbd6d325ebc740879288e844",
 "leg_domain": [
  "chat",
  "cc"
 ],
 "memo_lock_bytes": 121950,
 "memo_lock_md5": "6ea16b952db835bb351d3dc1b474c6ed",
 "nulls": {
  "N-1": {
   "keys": [
    "fit",
    "bi"
   ],
   "odf_reading": "per family (hexP2/hexP4/cubK4)",
   "scope": "every key x arm x mapped family",
   "tolerance": 1e-06
  },
  "N-2": {
   "keys": [
    "fit7",
    "bi_chat",
    "bi_cc",
    "bi_5x5"
   ],
   "odf_reading": "hexP2P4 (hex) / cubP2K4-i (cubic)",
   "scope": "every key",
   "tolerance": 1e-06
  },
  "N-3": {
   "keys": [
    "fit",
    "bi"
   ],
   "odf_reading": "cubP2-i",
   "scope": "cubic keys",
   "tolerance": 1e-06
  },
  "N-4": {
   "keys": [
    "fit7",
    "bi_5x5",
    "k12_chat_t2sq"
   ],
   "odf_reading": "cubP2K4-i",
   "scope": "cubic keys",
   "tolerance": 1e-06
  },
  "rule": "every null record carries its odf_reading token; a record without a token is rejected; every value is compared to its tolerance on each leg and across legs at pin_derived_rel"
 },
 "odf_reading_tokens": [
  "none",
  "uniform",
  "hexP2",
  "hexP4",
  "hexP2P4",
  "cubK4",
  "cubP2-i",
  "cubP2-ii",
  "cubP2K4-i",
  "cubP2K4-ii"
 ],
 "optional_row_keys": [
  "q",
  "note"
 ],
 "phase0": {
  "float_rules": {
   "F-CTRL-SA-GRID": {
    "count_mismatches": {
     "rule": "eq",
     "threshold": 0
    }
   },
   "F-CTRL-SA-K24": {
    "worst_abs_bi": {
     "rule": "le",
     "threshold": 1e-06
    },
    "worst_abs_fit7": {
     "rule": "le",
     "threshold": 1e-06
    }
   },
   "F-CTRL-SA-L2NULL": {
    "worst_abs_kappa2": {
     "rule": "le",
     "threshold": 1e-06
    },
    "worst_abs_kappa22": {
     "rule": "le",
     "threshold": 1e-06
    },
    "worst_abs_t2_alone_t1": {
     "rule": "le",
     "threshold": 1e-12
    }
   },
   "F-CTRL-SA-MASK": {
    "sealed_opens_before_phase3": {
     "rule": "eq",
     "threshold": 0
    }
   },
   "F-CTRL-SA-MONO": {
    "monotonicity_violations": {
     "rule": "eq",
     "threshold": 0
    },
    "worst_scaling_rel": {
     "rule": "le",
     "threshold": 1e-14
    }
   },
   "F-CTRL-SA-PIN": {
    "raw_mismatches": {
     "rule": "eq",
     "threshold": 0
    },
    "worst_twoleg_S_abs": {
     "rule": "le",
     "threshold": 1e-06
    },
    "worst_twoleg_b1_rel": {
     "rule": "le",
     "threshold": 0.0001
    },
    "worst_twoleg_kappa3_rel": {
     "rule": "le",
     "threshold": 0.0001
    },
    "worst_twoleg_kappa_rel": {
     "rule": "le",
     "threshold": 0.0001
    }
   },
   "F-CTRL-SA-PIN-DERIVED": {
    "leaf_mismatches": {
     "rule": "eq",
     "threshold": 0
    },
    "worst_scaled_dev": {
     "rule": "le",
     "threshold": 1.0
    }
   },
   "F-CTRL-SA-RECON": {
    "worst_abs_E2_Hill": {
     "rule": "le",
     "threshold": 1e-08
    },
    "worst_rel_robust": {
     "rule": "le",
     "threshold": 0.001
    }
   },
   "F-CTRL-SA-S": {
    "worst_abs_bi": {
     "rule": "le",
     "threshold": 1e-06
    },
    "worst_abs_fit": {
     "rule": "le",
     "threshold": 1e-06
    }
   },
   "F-CTRL-SA-SIGN": {
    "binding_end_mismatches": {
     "rule": "eq",
     "threshold": 0
    }
   },
   "F-CTRL-SA-T1": {
    "hits": {
     "rule": "eq",
     "threshold": 0
    }
   },
   "F-CTRL-SA-ZERO": {
    "worst_abs_r0": {
     "rule": "le",
     "threshold": 1e-12
    }
   }
  },
  "items": [
   "F-CTRL-SA-PIN",
   "F-CTRL-SA-PIN-DERIVED",
   "F-CTRL-SA-ZERO",
   "F-CTRL-SA-RECON",
   "F-CTRL-SA-S",
   "F-CTRL-SA-K24",
   "F-CTRL-SA-L2NULL",
   "F-CTRL-SA-SIGN",
   "F-CTRL-SA-GRID",
   "F-CTRL-SA-MONO",
   "F-CTRL-SA-MASK",
   "F-CTRL-SA-T1"
  ],
  "note": "the comparator re-evaluates every float rule from the reported float on each leg, independently of the leg's own passed flag, and also requires passed == true on both legs",
  "odf_reading": {
   "F-CTRL-SA-GRID": "none",
   "F-CTRL-SA-K24": "hexP2P4/cubP2K4-i",
   "F-CTRL-SA-L2NULL": "cubP2-ii/cubP2-i/cubP2K4-i",
   "F-CTRL-SA-MASK": "none",
   "F-CTRL-SA-MONO": "none",
   "F-CTRL-SA-PIN": "none",
   "F-CTRL-SA-PIN-DERIVED": "none",
   "F-CTRL-SA-RECON": "hexP4/cubK4/hexP2",
   "F-CTRL-SA-S": "hexP2/hexP4/cubK4",
   "F-CTRL-SA-SIGN": "none",
   "F-CTRL-SA-T1": "none",
   "F-CTRL-SA-ZERO": "uniform"
  }
 },
 "phase2": {
  "rule": "every suite passed on both legs; suite details are free text except the boolean",
  "suites": [
   "C-SYN-1",
   "C-SYN-2",
   "C-SYN-3",
   "C-SYN-4",
   "C-SYN-5",
   "C-SYN-6",
   "C-SYN-7",
   "C-SYN-8",
   "C-SYN-9",
   "C-SYN-10",
   "C-SYN-11",
   "C-SYN-12",
   "C-SYN-13",
   "C-SYN-14"
  ]
 },
 "phase3": {
  "class_precedence": [
   "INDETERMINATE",
   "VOID",
   "ANCHOR-INCONSISTENT",
   "KILL-IN-D",
   "TUNED",
   "MARGIN-ONLY",
   "WINDOW-DELIVERED",
   "INERT-IN-D"
  ],
  "gate_fields": [
   "gate_class",
   "sigma_union_hi",
   "sigma_strict_hi",
   "oom_class_x10",
   "oom_class_x0p1",
   "oom_robust",
   "contains_zero",
   "combined_empty",
   "n_void_rows"
  ],
  "identity": [
   "sealed_md5",
   "sealed_bytes",
   "census",
   "row_md5s",
   "t1_a1_md5"
  ],
  "never_serialized": [
   "lo",
   "hi",
   "k_em_max",
   "k_t_max",
   "src",
   "note",
   "cl"
  ],
  "per_exclusion_fields": [
   "class",
   "subreason",
   "t_in",
   "t_out",
   "can_supply_alone"
  ],
  "per_family_fields": [
   "class",
   "t_star",
   "t_star_bi",
   "class_bi",
   "resolution_sensitive",
   "sigma_star",
   "window_lo",
   "window_hi",
   "trunc_T",
   "truncation_sensitive",
   "nu",
   "nu_is_inf",
   "nullfloor_sensitive",
   "binding_end"
  ],
  "per_two_param_fields": [
   "area_fraction",
   "admissible_nodes",
   "total_nodes",
   "null_ray_slope",
   "definiteness",
   "compact"
  ]
 },
 "pinned_inputs_bytes": 96761,
 "pinned_inputs_md5": "2d44ec01a66889f330d940dee3313bdc",
 "primary": {
  "arm": "E2_Hill",
  "keys": [
   "hex_step|a",
   "hex_gem8|a",
   "cubic_step|001",
   "cubic_gem8|001"
  ]
 },
 "required_row_keys": [
  "id",
  "class",
  "delta_def",
  "lo",
  "hi",
  "cl",
  "reading",
  "geom",
  "k_em_max",
  "k_t_max",
  "src"
 ],
 "scanner_md5": "6b86290090a8c84f1b1a0a99ec0bf697",
 "schema_version": "1.0",
 "t1_base_md5": "05302210cc4ceb70553acbe8379e9fc3",
 "t1_list_md5": "e274e58ea50b9ed347969e507d2a4f36",
 "tolerances": {
  "D": 0.25,
  "KD_CLIP": 0.3,
  "edge_twoleg_abs_floor": 1e-18,
  "edge_twoleg_rel": 1e-10,
  "kappa_floor": 1e-06,
  "l2null_t1_abs": 1e-12,
  "mono_rel": 1e-14,
  "mu": 0.1,
  "nullfloor_threshold": 0.1,
  "pin_derived_abs": 1e-16,
  "pin_derived_rel": 1e-12,
  "pin_twoleg_rel": 0.0001,
  "recon_abs_E2_Hill": 1e-08,
  "recon_rel_robust": 0.001,
  "tau_agg": 1e-06,
  "trunc_threshold": 0.1,
  "zero_ctrl_abs": 1e-12
 },
 "verifier_md5": "cf004d517d2efe91a02c92a58e3df6bf"
}

=====END-EMBED name=g_mscs_a_schema_v1_0.json=====

=====BEGIN-EMBED name=g_mscs_a_compare_v1_0.py md5=c5b4a7aab2fc8651be6d26d1f3d25642 bytes=16850 encoding=raw=====
#!/usr/bin/env python3
"""g_mscs_a_compare_v1_0.py -- two-leg comparator for Gate G-MSCS-A, FROZEN v1.0 (September 29, 2026).

Compares the chat-leg and CC-leg checkpoints against g_mscs_a_schema_v1_0.json (md5 asserted at load).
Checks (memo section 6.5):
  C-SA-0 provenance (memo, pinned inputs, T1 list, schema, elections, ledger base equal the schema on both legs);
         phase 0 passed on both legs with every float rule re-evaluated from the reported float; phase 2 all passed.
  C-SA-1 every numeric field of phase3 across legs at |a-b| <= rel*max(|a|,|b|) + floor (null only equals null).
  C-SA-2 every class, sub-reason, flag and OOM class identical (strings / bools / ints exact); the tree shapes identical.
  C-SA-3 sealed_md5, sealed_bytes, census, row_md5s identical.
  C-SA-4 pinned_inputs_md5 on both legs equals the schema's.
  C-SA-5 every null within its tolerance on each leg, its odf_reading token present, values across legs at pin_derived_rel.
  C-SA-6 T1 hits == 0 on both legs (F-CTRL-SA-T1 and the post-write scan).
  C-SA-7 grid counts recomputed here from the generators equal the checkpoint counts on both legs.
  C-SA-8 instrument_md5 differs between legs.
Never compared: free text (utc, detail strings). Never present: any anchor value (the checkpoint layout has no field for one;
the comparator additionally refuses a checkpoint carrying a key named lo, hi, k_em_max, k_t_max, src, note or cl).

Usage:  compare : python3 g_mscs_a_compare_v1_0.py compare CHAT.json CC.json [--schema S.json] [--out OUT.json]
        selftest: python3 g_mscs_a_compare_v1_0.py selftest [--schema S.json]
Exit: 0 all PASS, 1 any MISS, 2 usage/fatal."""
import copy, hashlib, json, math, sys

SCHEMA_DEFAULT = 'g_mscs_a_schema_v1_0.json'
SCHEMA_MD5 = '5323e11fc27d688f61aaf57302c875c0'
FORBIDDEN_KEYS = {'lo', 'hi', 'k_em_max', 'k_t_max', 'src', 'note', 'cl'}
FREE_TEXT = {'utc', 'detail', 'note_free_text'}


def load_schema(path):
    raw = open(path, 'rb').read()
    h = hashlib.md5(raw).hexdigest()
    if h != SCHEMA_MD5:
        raise SystemExit('FATAL: schema md5 %s != frozen %s' % (h, SCHEMA_MD5))
    return json.loads(raw.decode('ascii')), h


def isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


class Rec:
    def __init__(self):
        self.rows = []

    def add(self, check, name, ok, note=''):
        self.rows.append({'check': check, 'name': name, 'pass': bool(ok), 'note': note})

    def summary(self):
        n = len(self.rows)
        p = sum(r['pass'] for r in self.rows)
        return {'checks': n, 'pass': p, 'miss': n - p}


def rule_ok(v, rule):
    if rule['rule'] == 'eq':
        return isnum(v) and v == rule['threshold']
    if not isnum(v):
        return False
    return v <= rule['threshold'] if rule['rule'] == 'le' else v >= rule['threshold']


def walk_keys(node, path=''):
    if isinstance(node, dict):
        for k, v in node.items():
            yield path + '/' + k, k
            yield from walk_keys(v, path + '/' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_keys(v, '%s[%d]' % (path, i))


def compare_tree(a, b, rel, floor, rec, check, path):
    """generic two-leg comparison: numbers at tolerance, everything else exact, shapes identical"""
    if isinstance(a, dict) and isinstance(b, dict):
        if sorted(a) != sorted(b):
            rec.add(check, path, False, 'key sets differ')
            return
        for k in a:
            if k in FREE_TEXT:
                continue
            compare_tree(a[k], b[k], rel, floor, rec, check, path + '/' + k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            rec.add(check, path, False, 'lengths differ')
            return
        for i in range(len(a)):
            compare_tree(a[i], b[i], rel, floor, rec, check, '%s[%d]' % (path, i))
    elif isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str) or a is None or b is None:
        rec.add(check + '/exact', path, a == b and type(a) == type(b))
    elif isnum(a) and isnum(b):
        rec.add(check + '/num', path, abs(a - b) <= rel * max(abs(a), abs(b)) + floor)
    else:
        rec.add(check, path, False, 'type mismatch or non-finite')


def recount(g):
    D = g['D']
    tg = g['t_grid']
    return {'n_t_grid': len(tg), 'n_fit_window_inclusive': sum(abs(t) <= D for t in tg), 'n_fit_window_strict': sum(abs(t) < D for t in tg),
            'n_window_0p1_inclusive': sum(abs(t) <= 0.1 for t in tg), 'n_window_0p1_strict': sum(abs(t) < 0.1 for t in tg),
            'n_t2t4_axis': len(g['t2t4_axis']), 'n_t2t4_grid': len(g['t2t4_axis']) ** 2, 'n_area_grid': g['area_nodes_per_axis'] ** 2}


def compare(chat, cc, S, schema_md5):
    rec = Rec()
    T = S['tolerances']
    legs = {'chat': chat, 'cc': cc}
    # refusal: any forbidden key anywhere
    for leg, ck in legs.items():
        bad = sorted({k for _, k in walk_keys(ck) if k in FORBIDDEN_KEYS})
        rec.add('C-SA-refuse', leg + ' no anchor-value field', not bad, ', '.join(bad))
    # C-SA-0 provenance and phase 0 / phase 2
    for leg, ck in legs.items():
        for field, want in (('memo_lock_md5', S['memo_lock_md5']), ('pinned_inputs_md5', S['pinned_inputs_md5']), ('t1_list_md5', S['t1_list_md5']),
                            ('schema_md5', schema_md5), ('ledger_base_md5', S['ledger_base_md5']), ('gate', S['gate']), ('scanner_md5', S['scanner_md5'])):
            rec.add('C-SA-0', '%s %s' % (leg, field), ck.get(field) == want)
        rec.add('C-SA-0', leg + ' elections', ck.get('elections') == S['elections'])
        rec.add('C-SA-0', leg + ' leg label', ck.get('leg') == leg)
        P0 = ck.get('phase0') or {}
        for item in S['phase0']['items']:
            e = P0.get(item)
            rec.add('C-SA-0/phase0', '%s %s passed' % (leg, item), isinstance(e, dict) and e.get('passed') is True)
            rec.add('C-SA-0/phase0', '%s %s odf_reading' % (leg, item), isinstance(e, dict) and e.get('odf_reading') == S['phase0']['odf_reading'][item])
            for fname, rule in S['phase0']['float_rules'][item].items():
                rec.add('C-SA-0/phase0/float', '%s %s.%s' % (leg, item, fname), isinstance(e, dict) and rule_ok(e.get(fname), rule))
        P2 = ck.get('phase2') or {}
        for suite in S['phase2']['suites']:
            rec.add('C-SA-0/phase2', '%s %s' % (leg, suite), isinstance(P2.get(suite), dict) and P2[suite].get('passed') is True)
    # C-SA-4
    for leg, ck in legs.items():
        rec.add('C-SA-4', leg + ' pinned md5', ck.get('pinned_inputs_md5') == S['pinned_inputs_md5'])
    # C-SA-8
    rec.add('C-SA-8', 'instrument md5 differs', chat.get('instrument_md5') != cc.get('instrument_md5') and bool(chat.get('instrument_md5')))
    # C-SA-6
    for leg, ck in legs.items():
        rec.add('C-SA-6', leg + ' F-CTRL-SA-T1 hits', (ck.get('phase0') or {}).get('F-CTRL-SA-T1', {}).get('hits') == 0)
        rec.add('C-SA-6', leg + ' post-write hits', (ck.get('T1_post_write') or {}).get('hits') == 0)
    # C-SA-7
    for leg, ck in legs.items():
        g = ck.get('grids') or {}
        try:
            want = recount(g)
            for k, v in want.items():
                rec.add('C-SA-7', '%s %s' % (leg, k), g.get(k) == v)
        except Exception as e:
            rec.add('C-SA-7', leg + ' generators', False, str(e))
    # C-SA-5 nulls
    for leg, ck in legs.items():
        N = ck.get('nulls') or {}
        for nid, spec in S['nulls'].items():
            if nid == 'rule':
                continue
            block = N.get(nid) or {}
            rec.add('C-SA-5', '%s %s present' % (leg, nid), bool(block))
            for cell, rec_ in block.items():
                rec.add('C-SA-5/token', '%s %s %s' % (leg, nid, cell), rec_.get('odf_reading') in S['odf_reading_tokens'])
                for k in spec['keys']:
                    v = rec_.get(k)
                    if v is None:
                        rec.add('C-SA-5/null-value', '%s %s %s %s' % (leg, nid, cell, k), k == 'k12_chat_t2sq' or k == 'fit', 'absent')
                    else:
                        rec.add('C-SA-5/tol', '%s %s %s %s' % (leg, nid, cell, k), isnum(v) and abs(v) <= spec['tolerance'])
    compare_tree(chat.get('nulls'), cc.get('nulls'), T['pin_derived_rel'], T['pin_derived_abs'], rec, 'C-SA-5/twoleg', 'nulls')
    # C-SA-1/2/3: phase 3
    p3c, p3cc = chat.get('phase3'), cc.get('phase3')
    if p3c is None and p3cc is None:
        rec.add('C-SA-3', 'phase3 absent on both legs (pre-read run)', True)
    else:
        for k in S['phase3']['identity']:
            rec.add('C-SA-3', k, (p3c or {}).get(k) == (p3cc or {}).get(k) and (p3c or {}).get(k) is not None)
        compare_tree(p3c, p3cc, T['edge_twoleg_rel'], T['edge_twoleg_abs_floor'], rec, 'C-SA-1/2', 'phase3')
        for leg, p3 in (('chat', p3c), ('cc', p3cc)):
            rec.add('C-SA-2', leg + ' gate class in precedence list', isinstance(p3, dict) and (p3.get('gate') or {}).get('gate_class') in S['phase3']['class_precedence'])
    return rec


# ------------------------------------------------------------------------------------------------ self-test
def synthetic_checkpoint(S, leg, schema_md5):
    keys, arms = S['keys'], S['arms']
    ck = {'gate': S['gate'], 'leg': leg, 'utc': '2026-09-29T00:00:00Z', 'instrument_md5': ('a' if leg == 'chat' else 'b') * 32,
          'memo_lock_md5': S['memo_lock_md5'], 'memo_lock_bytes': S['memo_lock_bytes'], 'pinned_inputs_md5': S['pinned_inputs_md5'],
          't1_list_md5': S['t1_list_md5'], 't1_a1_md5': 'c' * 32, 'scanner_md5': S['scanner_md5'], 'schema_md5': schema_md5,
          'ledger_base_md5': S['ledger_base_md5'], 'elections': dict(S['elections']), 'lock_record_md5': 'd' * 32,
          'phase0': {}, 'nulls': {}, 'phase2': {s: {'passed': True, 'detail': 'synthetic'} for s in S['phase2']['suites']},
          'grids': {'t_grid': [-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0], 't2t4_axis': [-0.25, -0.125, 0.0, 0.125, 0.25],
                    'D': 0.25, 'area_nodes_per_axis': 201},
          'T1_post_write': {'hits': 0, 'collisions': 0}}
    ck['grids'].update(recount(ck['grids']))
    for item in S['phase0']['items']:
        e = {'passed': True, 'odf_reading': S['phase0']['odf_reading'][item]}
        for f, rule in S['phase0']['float_rules'][item].items():
            e[f] = rule['threshold'] if rule['rule'] == 'eq' else (0.5 * rule['threshold'] if rule['rule'] == 'le' else rule['threshold'])
        ck['phase0'][item] = e
    ck['nulls'] = {'N-1': {'%s/E2_Hill/t4' % k: {'odf_reading': 'hexP4' if 'hex' in k else 'cubK4', 'fit': 1e-11, 'bi': 2e-12} for k in keys},
                   'N-2': {k: {'odf_reading': 'hexP2P4' if 'hex' in k else 'cubP2K4-i', 'fit7': 1e-8, 'bi_chat': 1e-12, 'bi_cc': 1e-12, 'bi_5x5': 1e-12} for k in keys},
                   'N-3': {k: {'odf_reading': 'cubP2-i', 'fit': 1e-15, 'bi': 1e-13} for k in S['cubic_keys']},
                   'N-4': {k: {'odf_reading': 'cubP2K4-i', 'fit7': 1e-9, 'bi_5x5': 1e-14, 'k12_chat_t2sq': None} for k in S['cubic_keys']}}
    fam = {k: {a: {f: {'class': 'BINDING', 't_star': 0.1234, 't_star_bi': 0.1234, 'class_bi': 'BINDING', 'resolution_sensitive': False,
                       'sigma_star': 0.04, 'window_lo': -0.1234, 'window_hi': 0.1234, 'trunc_T': 1e-4, 'truncation_sensitive': False,
                       'nu': 1e-9, 'nu_is_inf': False, 'nullfloor_sensitive': False, 'binding_end': 'hi'} for f in ('t4', 't2')} for a in arms} for k in keys}
    ck['phase3'] = {'sealed_md5': 'e' * 32, 'sealed_bytes': 321, 'census': {'rows': 1, 'per_class': {'spd': 1}, 'fields_per_row': [11]},
                    'row_md5s': ['f' * 32], 't1_a1_md5': 'c' * 32, 'n_void_rows': 0, 'combined_empty': False, 'contains_zero': True,
                    'rows': [{'id': 'SA-1', 'row_md5': 'f' * 32, 'void_regime': False, 'contains_zero': True}],
                    'combined': {'families': fam, 'exclusion': None, 'two_param': {}},
                    'gate': {'gate_class': 'WINDOW-DELIVERED', 'sigma_union_hi': 0.05, 'sigma_strict_hi': 0.04, 'oom_class_x10': 'INERT-IN-D',
                             'oom_class_x0p1': 'WINDOW-DELIVERED', 'oom_robust': False, 'contains_zero': True, 'combined_empty': False, 'n_void_rows': 0}}
    return ck


def selftest(S, schema_md5):
    base_c, base_cc = synthetic_checkpoint(S, 'chat', schema_md5), synthetic_checkpoint(S, 'cc', schema_md5)
    ok0 = compare(base_c, base_cc, S, schema_md5).summary()['miss'] == 0
    suites = {}
    def mut(name, f, expect_miss=True):
        c, d = copy.deepcopy(base_c), copy.deepcopy(base_cc)
        f(c, d)
        miss = compare(c, d, S, schema_md5).summary()['miss']
        suites[name] = (miss > 0) == expect_miss
    mut('A1 edge differs beyond tolerance', lambda c, d: d['phase3']['combined']['families']['hex_step|a']['E2_Hill']['t4'].__setitem__('t_star', 0.1234 * (1 + 1e-9)))
    mut('A2 edge differs within tolerance', lambda c, d: d['phase3']['combined']['families']['hex_step|a']['E2_Hill']['t4'].__setitem__('t_star', 0.1234 * (1 + 1e-11)), expect_miss=False)
    mut('A3 class differs', lambda c, d: d['phase3']['combined']['families']['hex_step|a']['E2_Hill']['t4'].__setitem__('class', 'INERT-IN-D'))
    mut('A4 gate class differs', lambda c, d: d['phase3']['gate'].__setitem__('gate_class', 'INERT-IN-D'))
    mut('A5 sealed md5 differs', lambda c, d: d['phase3'].__setitem__('sealed_md5', '0' * 32))
    mut('A6 row md5 differs', lambda c, d: d['phase3'].__setitem__('row_md5s', ['0' * 32]))
    mut('A7 pinned md5 wrong on one leg', lambda c, d: c.__setitem__('pinned_inputs_md5', '0' * 32))
    mut('A8 same instrument md5', lambda c, d: d.__setitem__('instrument_md5', c['instrument_md5']))
    mut('A9 phase0 passed but float violates rule', lambda c, d: c['phase0']['F-CTRL-SA-ZERO'].__setitem__('worst_abs_r0', 1e-11))
    mut('A10 phase0 passed false', lambda c, d: d['phase0']['F-CTRL-SA-S'].__setitem__('passed', False))
    mut('A11 null exceeds tolerance', lambda c, d: c['nulls']['N-2']['hex_step|a'].__setitem__('bi_cc', 2e-6))
    mut('A12 null token missing', lambda c, d: c['nulls']['N-1']['hex_step|a/E2_Hill/t4'].pop('odf_reading'))
    mut('A13 count field typed wrong', lambda c, d: d['grids'].__setitem__('n_fit_window_inclusive', 7))
    mut('A14 T1 hit on one leg', lambda c, d: c['phase0']['F-CTRL-SA-T1'].__setitem__('hits', 1))
    mut('A15 anchor value field present', lambda c, d: d['phase3']['rows'][0].__setitem__('lo', -1.0))
    mut('A16 phase2 suite failed', lambda c, d: d['phase2']['C-SYN-9'].__setitem__('passed', False))
    mut('A17 flag differs', lambda c, d: d['phase3']['combined']['families']['cubic_gem8|111']['h_Hill']['t4'].__setitem__('nullfloor_sensitive', True))
    mut('A18 elections differ', lambda c, d: c['elections'].__setitem__('E-SA-9', 'b'))
    mut('A19 census differs', lambda c, d: d['phase3']['census'].__setitem__('rows', 2))
    mut('A20 gate class not in precedence list', lambda c, d: [x['phase3']['gate'].__setitem__('gate_class', 'KILLED') for x in (c, d)])
    mut('A21 utc differs (free text)', lambda c, d: d.__setitem__('utc', 'other'), expect_miss=False)
    mut('A22 null differs across legs', lambda c, d: d['nulls']['N-3']['cubic_step|001'].__setitem__('bi', 1.1e-13))
    return ok0, suites


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    args = sys.argv[1:]
    schema = args[args.index('--schema') + 1] if '--schema' in args else SCHEMA_DEFAULT
    S, smd5 = load_schema(schema)
    if args[0] == 'selftest':
        ok0, suites = selftest(S, smd5)
        print('baseline synthetic pair: %s' % ('PASS' if ok0 else 'FAIL'))
        for k, v in suites.items():
            print('  %-42s %s' % (k, 'ok' if v else 'FAILED'))
        good = ok0 and all(suites.values())
        print('SELFTEST: %s (%d/%d)' % ('PASS' if good else 'FAIL', sum(suites.values()), len(suites)))
        return 0 if good else 1
    if args[0] == 'compare' and len(args) >= 3:
        chat, cc = json.load(open(args[1])), json.load(open(args[2]))
        rec = compare(chat, cc, S, smd5)
        s = rec.summary()
        out = {'schema_md5': smd5, 'summary': s, 'misses': [r for r in rec.rows if not r['pass']]}
        if '--out' in args:
            json.dump({'rows': rec.rows, **out}, open(args[args.index('--out') + 1], 'w'), indent=1, sort_keys=True)
        print('checks %d  pass %d  miss %d' % (s['checks'], s['pass'], s['miss']))
        for r in out['misses'][:40]:
            print('  MISS %s %s %s' % (r['check'], r['name'], r['note']))
        print('RESULT: ' + ('PASS' if s['miss'] == 0 else 'MISS'))
        return 0 if s['miss'] == 0 else 1
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())

=====END-EMBED name=g_mscs_a_compare_v1_0.py=====

=====BEGIN-EMBED name=pinned_inputs_G_MSCS_A.json md5=2d44ec01a66889f330d940dee3313bdc bytes=96761 encoding=raw=====
{
 "_meta": {
  "base_ledger_md5": "d4c42a53cbd6d325ebc740879288e844",
  "builder": "sa_build_pinned_inputs.py",
  "builder_md5": "8189100ede80eac360b25a146e580abf",
  "contents": "banked values by named key + fixed constants, grid generators and tokens + a derived reference section; no anchor value; no observational number; no point count",
  "cubic_term_order": [
   "t2^3",
   "t2^2*t4",
   "t2*t4^2",
   "t4^3"
  ],
  "dqf_basis_note": "index order of the chat quadform-basis diagnostic; asserted by this builder: k7[0..2] equal the fit7 kappa22, kappa24, kappa44 of the same key bit for bit and k7[3..6] equal the CC named cubic terms to 1e-4 relative; k12[3..6] equal k7[3..6] to 1e-8 relative (the shared order); the k12 quartic indices 7..11 follow the monomial order and are not independently confirmed (no instrument reads them)",
  "dqf_basis_order": [
   "t2^2",
   "t2*t4",
   "t4^2",
   "t2^3",
   "t2^2*t4",
   "t2*t4^2",
   "t4^3",
   "t2^4",
   "t2^3*t4",
   "t2^2*t4^2",
   "t2*t4^3",
   "t4^4"
  ],
  "elections_applied": {
   "E-SA-0": "a",
   "E-SA-1": "a",
   "E-SA-10": "a",
   "E-SA-11": "a",
   "E-SA-2": "a",
   "E-SA-3": "a",
   "E-SA-4": "a",
   "E-SA-5": "a",
   "E-SA-6": "a",
   "E-SA-7": "base 05302210 + the G-MSCS1 stratum",
   "E-SA-8": "a",
   "E-SA-9": "a"
  },
  "file_schema": "g_mscs_a_pinned_inputs/1",
  "gate": "G-MSCS-A"
 },
 "constants": {
  "D": 0.25,
  "KD_CLIP": 0.3,
  "edge_twoleg_tol_rel": 1e-10,
  "fam_rms": {
   "t2": "hexP2",
   "t4_cubic": "cubK4",
   "t4_hex": "hexP4"
  },
  "kappa_floor": 1e-06,
  "l2null_t1_tol_abs": 1e-12,
  "mono_tol_rel": 1e-14,
  "mu": 0.1,
  "nullfloor_threshold": 0.1,
  "oom_factors": [
   0.1,
   1.0,
   10.0
  ],
  "pin_derived_tol_abs": 1e-16,
  "pin_derived_tol_rel": 1e-12,
  "pin_twoleg_tol_rel": 0.0001,
  "recon_tol_abs_E2_Hill": 1e-08,
  "recon_tol_rel_robust": 0.001,
  "rms": {
   "cubK4": 0.4364357804719847,
   "hexP2": 0.4472135954999579,
   "hexP4": 0.3333333333333333
  },
  "rms_closed_form": {
   "cubK4": "sqrt(4/21)",
   "hexP2": "sqrt(1/5)",
   "hexP4": "1/3"
  },
  "synthetic_band_fractions": [
   0.25,
   0.75
  ],
  "synthetic_k": {
   "silent": 1.0,
   "void": 1e+33
  },
  "synthetic_rules": {
   "margin_negative": "[w + f1*(h - w), w + f2*(h - w)], w = unions.widened_all[0], h = unions.hull_all[0]",
   "margin_positive": "[h + f1*(w - h), h + f2*(w - h)], h = unions.hull_all[1], w = unions.widened_all[1]",
   "robustness_only_positive": "[p + f1*(q - p), p + f2*(q - p)], p = unions.widened_primary[1], q = unions.hull_all[1]"
  },
  "synthetic_t": [
   0.01,
   0.1,
   0.5
  ],
  "synthetic_t_tight": 1e-09,
  "tau_agg": 1e-06,
  "trunc_threshold": 0.1,
  "zero_ctrl_tol_abs": 1e-12,
  "zero_snap": 1e-12
 },
 "derived": {
  "families": {
   "cubic_gem8|001": {
    "E2_HSmean": {
     "t2": {
      "S_bi": -3.7007434154171886e-16,
      "S_fit": null,
      "fit_res_rel": null,
      "kappa": -2.9328086757977686e-16,
      "kappa_bi": 3.700743415417188e-15,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 0.0
     },
     "t4": {
      "S_bi": -2.5054032922374364e-13,
      "S_fit": null,
      "fit_res_rel": 2.270878052334917e-05,
      "kappa": -0.0004767151950423074,
      "kappa_bi": -0.0004767043696674021,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 0.0,
      "twoleg_rel": 1.4395298748822331e-12
     }
    },
    "E2_Hill": {
     "t2": {
      "S_bi": 0.0,
      "S_fit": 2.2690471976516216e-16,
      "fit_res_rel": null,
      "kappa": -1.4940723442743361e-16,
      "kappa_bi": -1.1842378929335001e-13,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 0.0,
      "twoleg_S_abs": 1.1819852171697378e-15,
      "twoleg_kappa3_rel": null,
      "twoleg_rel": null
     },
     "t4": {
      "S_bi": -2.173076533532973e-12,
      "S_fit": -4.267168229021896e-11,
      "fit_res_rel": 0.00018194418484485464,
      "kappa": -0.0004492770934296169,
      "kappa_bi": -0.00044919536494510587,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 0.0,
      "recon_max_abs": 6.845659647617054e-10,
      "trunc_T_at_D": 0.0021121968553136795,
      "twoleg_S_abs": 1.361085304723368e-15,
      "twoleg_kappa3_rel": 7.612414992334093e-09,
      "twoleg_rel": 4.4523814756654665e-12
     }
    },
    "h_Hill": {
     "t2": {
      "S_bi": -3.7007434154171886e-16,
      "S_fit": 1.0207029061365447e-15,
      "fit_res_rel": null,
      "kappa": 1.4525703347111552e-15,
      "kappa_bi": 3.700743415417188e-15,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 0.0,
      "twoleg_S_abs": 1.0207029061365447e-15,
      "twoleg_rel": null
     },
     "t4": {
      "S_bi": -1.2118084313783584e-12,
      "S_fit": -2.385281734789809e-11,
      "fit_res_rel": 0.0007269110377504565,
      "kappa": -4.535782266248913e-05,
      "kappa_bi": -4.53248755101961e-05,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 0.0,
      "twoleg_S_abs": 4.564511416063326e-16,
      "twoleg_rel": 5.971839055927073e-11
     }
    }
   },
   "cubic_gem8|111": {
    "E2_HSmean": {
     "t2": {
      "S_bi": -3.7007434154171886e-16,
      "S_fit": null,
      "fit_res_rel": null,
      "kappa": -4.1502009563175863e-16,
      "kappa_bi": -1.1472304587793283e-13,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 0.0
     },
     "t4": {
      "S_bi": 1.7393494052460787e-13,
      "S_fit": null,
      "fit_res_rel": 2.270909640721569e-05,
      "kappa": 0.00031781013002497063,
      "kappa_bi": 0.00031780291300798064,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 0.0,
      "twoleg_rel": 1.7062505733408149e-12
     }
    },
    "E2_Hill": {
     "t2": {
      "S_bi": 3.7007434154171886e-16,
      "S_fit": -1.1819852171697386e-15,
      "fit_res_rel": null,
      "kappa": 1.272728293270753e-16,
      "kappa_bi": -1.221245327087672e-13,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 0.0,
      "twoleg_S_abs": 1.4745123456668797e-15,
      "twoleg_kappa3_rel": null,
      "twoleg_rel": null
     },
     "t4": {
      "S_bi": 1.4506914188435378e-12,
      "S_fit": 2.8447697640179876e-11,
      "fit_res_rel": 0.00018194430841970036,
      "kappa": 0.00029951806228887087,
      "kappa_bi": 0.0002994635765955303,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 0.0,
      "recon_max_abs": 4.5637747349637264e-10,
      "trunc_T_at_D": 0.0021121968402507537,
      "twoleg_S_abs": 6.625652507059083e-16,
      "twoleg_kappa3_rel": 1.3117634020690619e-09,
      "twoleg_rel": 1.828082677099285e-11
     }
    },
    "h_Hill": {
     "t2": {
      "S_bi": 0.0,
      "S_fit": 0.0,
      "fit_res_rel": null,
      "kappa": 0.0,
      "kappa_bi": 0.0,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 0.0,
      "twoleg_S_abs": 0.0,
      "twoleg_rel": null
     },
     "t4": {
      "S_bi": -1.2118084313783584e-12,
      "S_fit": -2.385281734789809e-11,
      "fit_res_rel": 0.0007269110377504565,
      "kappa": -4.535782266248913e-05,
      "kappa_bi": -4.53248755101961e-05,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 0.0,
      "twoleg_S_abs": 4.564511416063326e-16,
      "twoleg_rel": 5.971839055927073e-11
     }
    }
   },
   "cubic_step|001": {
    "E2_HSmean": {
     "t2": {
      "S_bi": 0.0,
      "S_fit": null,
      "fit_res_rel": null,
      "kappa": -4.606723061512521e-16,
      "kappa_bi": -7.031412489292657e-14,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": -1.1102230246251565e-16
     },
     "t4": {
      "S_bi": -1.0473103865630644e-13,
      "S_fit": null,
      "fit_res_rel": 1.4105432409214183e-05,
      "kappa": -0.00038926474535513255,
      "kappa_bi": -0.0003892592546850259,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": -1.1102230246251565e-16,
      "twoleg_rel": 1.4214556682320975e-12
     }
    },
    "E2_Hill": {
     "t2": {
      "S_bi": 1.4802973661668755e-15,
      "S_fit": 3.872699649800502e-16,
      "fit_res_rel": null,
      "kappa": 3.141702123932416e-15,
      "kappa_bi": -2.5905203907920314e-14,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 0.0,
      "twoleg_S_abs": 3.1717500348738004e-16,
      "twoleg_kappa3_rel": null,
      "twoleg_rel": null
     },
     "t4": {
      "S_bi": -9.956850159179946e-13,
      "S_fit": -1.9549678946260598e-11,
      "fit_res_rel": 0.00012288880002660066,
      "kappa": -0.0003743529418175674,
      "kappa_bi": -0.00037430694368641615,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 0.0,
      "recon_max_abs": 3.851696308700505e-10,
      "trunc_T_at_D": 0.0017584770529819804,
      "twoleg_S_abs": 8.826357293288202e-16,
      "twoleg_kappa3_rel": 1.0764307189694584e-08,
      "twoleg_rel": 6.403794803716564e-12
     }
    },
    "h_Hill": {
     "t2": {
      "S_bi": 1.4802973661668755e-15,
      "S_fit": 2.7381760509747877e-16,
      "fit_res_rel": null,
      "kappa": -3.458500796931401e-17,
      "kappa_bi": -1.4062824978585312e-13,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 2.220446049250313e-16,
      "twoleg_S_abs": 2.7381760509747754e-16,
      "twoleg_rel": null
     },
     "t4": {
      "S_bi": -5.965598385652507e-13,
      "S_fit": -1.1694898610377518e-11,
      "fit_res_rel": 0.000514611662150869,
      "kappa": -3.8028327673460484e-05,
      "kappa_bi": -3.800876791822578e-05,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 2.220446049250313e-16,
      "twoleg_S_abs": 2.597167705599043e-16,
      "twoleg_rel": 5.212980910713622e-11
     }
    }
   },
   "cubic_step|111": {
    "E2_HSmean": {
     "t2": {
      "S_bi": -1.1102230246251565e-15,
      "S_fit": null,
      "fit_res_rel": null,
      "kappa": 3.6895286501663385e-15,
      "kappa_bi": 2.2204460492503128e-14,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": -1.1102230246251565e-16
     },
     "t4": {
      "S_bi": 6.550315845288424e-14,
      "S_fit": null,
      "fit_res_rel": 1.410552299687539e-05,
      "kappa": 0.00025950983023805826,
      "kappa_bi": 0.00025950616976781277,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": -1.1102230246251565e-16,
      "twoleg_rel": 8.571975116921406e-12
     }
    },
    "E2_Hill": {
     "t2": {
      "S_bi": 1.2952601953960159e-15,
      "S_fit": 4.1100077415202465e-16,
      "fit_res_rel": null,
      "kappa": -1.6739143857147652e-16,
      "kappa_bi": -2.775557561562891e-14,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 0.0,
      "twoleg_S_abs": 3.4090581265934943e-16,
      "twoleg_kappa3_rel": null,
      "twoleg_rel": null
     },
     "t4": {
      "S_bi": 6.650235917504688e-13,
      "S_fit": 1.3035416405833344e-11,
      "fit_res_rel": 0.00012288866692412693,
      "kappa": 0.00024956862787724117,
      "kappa_bi": 0.00024953796248968385,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 0.0,
      "recon_max_abs": 2.567795518451871e-10,
      "trunc_T_at_D": 0.001758477092071195,
      "twoleg_S_abs": 6.625512989752494e-16,
      "twoleg_kappa3_rel": 1.8907606678227007e-09,
      "twoleg_rel": 1.0210853855651288e-11
     }
    },
    "h_Hill": {
     "t2": {
      "S_bi": 0.0,
      "S_fit": -2.925271284971396e-16,
      "fit_res_rel": null,
      "kappa": 1.7403176010158433e-15,
      "kappa_bi": -1.1102230246251564e-13,
      "mapped": false,
      "odf_reading": "cubP2-i",
      "r0": 2.220446049250313e-16,
      "twoleg_S_abs": 2.9252712849714613e-16,
      "twoleg_rel": null
     },
     "t4": {
      "S_bi": -5.965598385652507e-13,
      "S_fit": -1.1694898610377518e-11,
      "fit_res_rel": 0.000514611662150869,
      "kappa": -3.8028327673460484e-05,
      "kappa_bi": -3.800876791822578e-05,
      "mapped": true,
      "odf_reading": "cubK4",
      "r0": 2.220446049250313e-16,
      "twoleg_S_abs": 2.597167705599043e-16,
      "twoleg_rel": 5.212980910713622e-11
     }
    }
   },
   "hex_gem8|a": {
    "E2_HSmean": {
     "t2": {
      "S_bi": 2.2019423321732272e-14,
      "S_fit": null,
      "fit_res_rel": 2.8007082661424708e-06,
      "kappa": -0.0018853014774839155,
      "kappa_bi": -0.001885306757678136,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": -2.220446049250313e-16
     },
     "t4": {
      "S_bi": -1.1102230246251565e-15,
      "S_fit": null,
      "fit_res_rel": 1.164434647898957e-06,
      "kappa": 0.0001789305885725744,
      "kappa_bi": 0.00017893038021984012,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": -2.220446049250313e-16,
      "twoleg_rel": 7.2212244388584446e-12
     }
    },
    "E2_Hill": {
     "t2": {
      "S_bi": 2.609024107869118e-14,
      "S_fit": 4.894642365145396e-13,
      "fit_res_rel": 8.907132939307482e-06,
      "kappa": -0.0018956484826701352,
      "kappa_bi": -0.0018956315980274876,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": -2.220446049250313e-16,
      "recon_max_abs": 1.4122192364086558e-10,
      "trunc_T_at_D": 0.00016360771962016938,
      "twoleg_S_abs": 6.855092691746027e-16,
      "twoleg_kappa3_rel": 3.1353981528597408e-09,
      "twoleg_rel": 1.9467783127707382e-12
     },
     "t4": {
      "S_bi": -9.992007221626409e-15,
      "S_fit": -2.652046374551464e-13,
      "fit_res_rel": 1.3096562242390882e-05,
      "kappa": 0.00017950729579484115,
      "kappa_bi": 0.0001795049448971575,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": -2.220446049250313e-16,
      "recon_max_abs": 1.9667368706327432e-11,
      "trunc_T_at_D": 0.0003054334036357186,
      "twoleg_S_abs": 2.269053282616184e-16,
      "twoleg_kappa3_rel": 1.691794132927529e-08,
      "twoleg_rel": 1.5474771506222774e-11
     }
    },
    "h_Hill": {
     "t2": {
      "S_bi": 1.2952601953960159e-15,
      "S_fit": 1.9849252759426836e-14,
      "fit_res_rel": 2.785994928976321e-05,
      "kappa": -3.2493966959289463e-06,
      "kappa_bi": -3.2493061704238113e-06,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0,
      "twoleg_S_abs": 9.791794049478322e-16,
      "twoleg_rel": 1.10862881023457e-09
     },
     "t4": {
      "S_bi": 5.921189464667502e-15,
      "S_fit": 8.394408199844183e-14,
      "fit_res_rel": 5.4418063445612275e-05,
      "kappa": -7.754414849489288e-06,
      "kappa_bi": -7.753992892212123e-06,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "twoleg_S_abs": 4.6912895559969835e-17,
      "twoleg_rel": 8.616837524721172e-11
     }
    }
   },
   "hex_gem8|b": {
    "E2_HSmean": {
     "t2": {
      "S_bi": 2.220446049250313e-14,
      "S_fit": null,
      "fit_res_rel": 2.8021763349109695e-06,
      "kappa": -0.0018857960842583088,
      "kappa_bi": -0.0018858013686062762,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": -3.3306690738754696e-16
     },
     "t4": {
      "S_bi": -5.1810407815840636e-15,
      "S_fit": null,
      "fit_res_rel": 1.1640109268010643e-06,
      "kappa": 0.00017892473038334653,
      "kappa_bi": 0.00017892452211324772,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": -3.3306690738754696e-16,
      "twoleg_rel": 1.6684801315550194e-11
     }
    },
    "E2_Hill": {
     "t2": {
      "S_bi": 2.572016673714946e-14,
      "S_fit": 4.895751529361098e-13,
      "fit_res_rel": 8.912680402499193e-06,
      "kappa": -0.0018961374665242264,
      "kappa_bi": -0.001896120567007608,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0,
      "recon_max_abs": 1.413470088315518e-10,
      "trunc_T_at_D": 0.00016356222992877292,
      "twoleg_S_abs": 7.168010053241271e-16,
      "twoleg_kappa3_rel": 1.7771343065301202e-08,
      "twoleg_rel": 1.6781043526542566e-12
     },
     "t4": {
      "S_bi": -1.295260195396016e-14,
      "S_fit": -2.664544112656851e-13,
      "fit_res_rel": 1.30939493159543e-05,
      "kappa": 0.00017950151354905876,
      "kappa_bi": 0.00017949916319611362,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "recon_max_abs": 1.966286384926537e-11,
      "trunc_T_at_D": 0.0003053394805968098,
      "twoleg_S_abs": 1.9546929055950477e-15,
      "twoleg_kappa3_rel": 2.0791999660278074e-07,
      "twoleg_rel": 2.087011183018691e-11
     }
    },
    "h_Hill": {
     "t2": {
      "S_bi": -9.251858538542972e-16,
      "S_fit": 1.861754403597132e-14,
      "fit_res_rel": 2.7885271281613077e-05,
      "kappa": -3.2509354903061167e-06,
      "kappa_bi": -3.2508448396158696e-06,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0,
      "twoleg_S_abs": 6.147236945680442e-16,
      "twoleg_rel": 8.681022375965836e-11
     },
     "t4": {
      "S_bi": 6.29126380620922e-15,
      "S_fit": 8.256781483484296e-14,
      "fit_res_rel": 5.441351585427506e-05,
      "kappa": -7.753635743144201e-06,
      "kappa_bi": -7.753213863518717e-06,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "twoleg_S_abs": 1.5027163065405909e-15,
      "twoleg_rel": 2.6763085149308272e-11
     }
    }
   },
   "hex_step|a": {
    "E2_HSmean": {
     "t2": {
      "S_bi": 7.031412489292658e-15,
      "S_fit": null,
      "fit_res_rel": 1.6001159592085983e-06,
      "kappa": -0.0014281847168633966,
      "kappa_bi": -0.0014281870021282115,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0
     },
     "t4": {
      "S_bi": 2.960594732333751e-15,
      "S_fit": null,
      "fit_res_rel": 1.205219337873632e-06,
      "kappa": 0.000159893047684377,
      "kappa_bi": 0.00015989285497841618,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "twoleg_rel": 1.2614823757652081e-11
     }
    },
    "E2_Hill": {
     "t2": {
      "S_bi": 9.25185853854297e-15,
      "S_fit": 1.6266231256261696e-13,
      "fit_res_rel": 5.091489849044244e-06,
      "kappa": -0.0014394617694966992,
      "kappa_bi": -0.001439454440529027,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0,
      "recon_max_abs": 6.12984387455027e-11,
      "trunc_T_at_D": 0.00012798749877157464,
      "twoleg_S_abs": 1.3371021615797176e-15,
      "twoleg_kappa3_rel": 4.7984978456336064e-08,
      "twoleg_rel": 2.6982626041257274e-12
     },
     "t4": {
      "S_bi": -1.4062824978585317e-14,
      "S_fit": -2.2136167800606602e-13,
      "fit_res_rel": 1.1863102562183057e-05,
      "kappa": 0.00016040534614367987,
      "kappa_bi": 0.00016040344326118114,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "recon_max_abs": 1.5919020684798283e-11,
      "trunc_T_at_D": 0.00034519219511093416,
      "twoleg_S_abs": 2.3428706317273546e-15,
      "twoleg_kappa3_rel": 2.025157866131e-07,
      "twoleg_rel": 1.2574365880403542e-11
     }
    },
    "h_Hill": {
     "t2": {
      "S_bi": 5.551115123125783e-16,
      "S_fit": 4.563941055176853e-15,
      "fit_res_rel": 1.5961435913877652e-05,
      "kappa": -2.0075101981637655e-06,
      "kappa_bi": -2.007478155929831e-06,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0,
      "twoleg_S_abs": 6.625535099698291e-16,
      "twoleg_rel": 9.358147555522567e-10
     },
     "t4": {
      "S_bi": 6.47630097698008e-15,
      "S_fit": 7.665423084547844e-14,
      "fit_res_rel": 5.239864216275228e-05,
      "kappa": -7.507739661972004e-06,
      "kappa_bi": -7.507346287220308e-06,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "twoleg_S_abs": 6.132571428069822e-16,
      "twoleg_rel": 1.687854029730019e-10
     }
    }
   },
   "hex_step|b": {
    "E2_HSmean": {
     "t2": {
      "S_bi": 8.141635513917814e-15,
      "S_fit": null,
      "fit_res_rel": 1.5984530602652609e-06,
      "kappa": -0.0014274194267221226,
      "kappa_bi": -0.0014274217083887206,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0
     },
     "t4": {
      "S_bi": 3.700743415417189e-15,
      "S_fit": null,
      "fit_res_rel": 1.2059890902507512e-06,
      "kappa": 0.00015990258492339606,
      "kappa_bi": 0.0001599023920828557,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "twoleg_rel": 8.7900999041608e-12
     }
    },
    "E2_Hill": {
     "t2": {
      "S_bi": 1.0732155904709847e-14,
      "S_fit": 1.6125034658616313e-13,
      "fit_res_rel": 5.084947067267994e-06,
      "kappa": -0.001438702718749083,
      "kappa_bi": -0.0014386954030591126,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0,
      "recon_max_abs": 6.118720107813709e-11,
      "trunc_T_at_D": 0.0001280619321235199,
      "twoleg_S_abs": 2.7504827357592218e-15,
      "twoleg_kappa3_rel": 6.93762517037559e-08,
      "twoleg_rel": 1.1465226024259965e-12
     },
     "t4": {
      "S_bi": -8.881784197001252e-15,
      "S_fit": -2.1990268388075987e-13,
      "fit_res_rel": 1.1866637163185323e-05,
      "kappa": 0.00016041466503408588,
      "kappa_bi": 0.00016041276147404912,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "recon_max_abs": 1.5924992858305423e-11,
      "trunc_T_at_D": 0.0003453301909476391,
      "twoleg_S_abs": 2.0582629676446206e-16,
      "twoleg_kappa3_rel": 4.867051527463476e-08,
      "twoleg_rel": 1.2780791006448472e-11
     }
    },
    "h_Hill": {
     "t2": {
      "S_bi": 0.0,
      "S_fit": 6.550087858874976e-15,
      "fit_res_rel": 1.602127984081706e-05,
      "kappa": -2.0054031941127916e-06,
      "kappa_bi": -2.0053710655017665e-06,
      "mapped": true,
      "odf_reading": "hexP2",
      "r0": 0.0,
      "twoleg_S_abs": 1.5870476470231372e-15,
      "twoleg_rel": 1.897048358696962e-10
     },
     "t4": {
      "S_bi": 4.9960036108132044e-15,
      "S_fit": 7.485871681214715e-14,
      "fit_res_rel": 5.2425207337068515e-05,
      "kappa": -7.509018168894417e-06,
      "kappa_bi": -7.508624527696736e-06,
      "mapped": true,
      "odf_reading": "hexP4",
      "r0": 0.0,
      "twoleg_S_abs": 1.3742446786218513e-15,
      "twoleg_rel": 3.2074778101782324e-10
     }
    }
   }
  },
  "hex_quadform": {
   "hex_gem8|a": {
    "h_Hill_form": "negative-definite",
    "k22_bi_5x5": -0.001895631597937708,
    "k24_bi_5x5": 1.3922196728799463e-12,
    "k44_bi_5x5": 0.00017950494490529914,
    "kappa22_fit7_vs_kappa2_rel": 6.026543396456391e-06,
    "null_ray_slope": {
     "E2_HSmean_bi": 3.2460033949287443,
     "E2_HSmean_fit": 3.2459969594961784,
     "E2_Hill_bi": 3.249666259511073,
     "E2_Hill_bi5x5": 3.2496662593604224,
     "E2_Hill_fit": 3.249659452469566
    }
   },
   "hex_gem8|b": {
    "h_Hill_form": "negative-definite",
    "k22_bi_5x5": -0.0018961205667779406,
    "k24_bi_5x5": 1.3871866618349789e-12,
    "k44_bi_5x5": 0.00017949916319714987,
    "kappa22_fit7_vs_kappa2_rel": 6.026145660631879e-06,
    "null_ray_slope": {
     "E2_HSmean_bi": 3.246482306782216,
     "E2_HSmean_fit": 3.2464758687049406,
     "E2_Hill_bi": 3.2501376928171584,
     "E2_Hill_bi5x5": 3.2501376926109407,
     "E2_Hill_fit": 3.2501308980491763
    }
   },
   "hex_step|a": {
    "h_Hill_form": "negative-definite",
    "k22_bi_5x5": -0.0014394544404684833,
    "k24_bi_5x5": 6.988483865673819e-13,
    "k44_bi_5x5": 0.00016040344325614816,
    "kappa22_fit7_vs_kappa2_rel": 5.2328358657189794e-06,
    "null_ray_slope": {
     "E2_HSmean_bi": 2.9886703121516915,
     "E2_HSmean_fit": 2.988666120042645,
     "E2_Hill_bi": 2.9956572274955366,
     "E2_Hill_bi5x5": 2.9956572274795352,
     "E2_Hill_fit": 2.995647084883406
    }
   },
   "hex_step|b": {
    "h_Hill_form": "negative-definite",
    "k22_bi_5x5": -0.001438695402984358,
    "k24_bi_5x5": 6.846375318521799e-13,
    "k44_bi_5x5": 0.0001604127614758255,
    "kappa22_fit7_vs_kappa2_rel": 5.233252862381621e-06,
    "null_ray_slope": {
     "E2_HSmean_bi": 2.98778036113015,
     "E2_HSmean_fit": 2.987776171603675,
     "E2_Hill_bi": 2.99478031899494,
     "E2_Hill_bi5x5": 2.994780318900554,
     "E2_Hill_fit": 2.9947701642622118
    }
   }
  },
  "nulls": {
   "N-1": {
    "cubic_gem8|001/E2_HSmean/t4": {
     "bi": -2.5054032922374364e-13,
     "fit": null,
     "odf_reading": "cubK4"
    },
    "cubic_gem8|001/E2_Hill/t4": {
     "bi": -2.173076533532973e-12,
     "fit": -4.267168229021896e-11,
     "odf_reading": "cubK4"
    },
    "cubic_gem8|001/h_Hill/t4": {
     "bi": -1.2118084313783584e-12,
     "fit": -2.385281734789809e-11,
     "odf_reading": "cubK4"
    },
    "cubic_gem8|111/E2_HSmean/t4": {
     "bi": 1.7393494052460787e-13,
     "fit": null,
     "odf_reading": "cubK4"
    },
    "cubic_gem8|111/E2_Hill/t4": {
     "bi": 1.4506914188435378e-12,
     "fit": 2.8447697640179876e-11,
     "odf_reading": "cubK4"
    },
    "cubic_gem8|111/h_Hill/t4": {
     "bi": -1.2118084313783584e-12,
     "fit": -2.385281734789809e-11,
     "odf_reading": "cubK4"
    },
    "cubic_step|001/E2_HSmean/t4": {
     "bi": -1.0473103865630644e-13,
     "fit": null,
     "odf_reading": "cubK4"
    },
    "cubic_step|001/E2_Hill/t4": {
     "bi": -9.956850159179946e-13,
     "fit": -1.9549678946260598e-11,
     "odf_reading": "cubK4"
    },
    "cubic_step|001/h_Hill/t4": {
     "bi": -5.965598385652507e-13,
     "fit": -1.1694898610377518e-11,
     "odf_reading": "cubK4"
    },
    "cubic_step|111/E2_HSmean/t4": {
     "bi": 6.550315845288424e-14,
     "fit": null,
     "odf_reading": "cubK4"
    },
    "cubic_step|111/E2_Hill/t4": {
     "bi": 6.650235917504688e-13,
     "fit": 1.3035416405833344e-11,
     "odf_reading": "cubK4"
    },
    "cubic_step|111/h_Hill/t4": {
     "bi": -5.965598385652507e-13,
     "fit": -1.1694898610377518e-11,
     "odf_reading": "cubK4"
    },
    "hex_gem8|a/E2_HSmean/t2": {
     "bi": 2.2019423321732272e-14,
     "fit": null,
     "odf_reading": "hexP2"
    },
    "hex_gem8|a/E2_HSmean/t4": {
     "bi": -1.1102230246251565e-15,
     "fit": null,
     "odf_reading": "hexP4"
    },
    "hex_gem8|a/E2_Hill/t2": {
     "bi": 2.609024107869118e-14,
     "fit": 4.894642365145396e-13,
     "odf_reading": "hexP2"
    },
    "hex_gem8|a/E2_Hill/t4": {
     "bi": -9.992007221626409e-15,
     "fit": -2.652046374551464e-13,
     "odf_reading": "hexP4"
    },
    "hex_gem8|a/h_Hill/t2": {
     "bi": 1.2952601953960159e-15,
     "fit": 1.9849252759426836e-14,
     "odf_reading": "hexP2"
    },
    "hex_gem8|a/h_Hill/t4": {
     "bi": 5.921189464667502e-15,
     "fit": 8.394408199844183e-14,
     "odf_reading": "hexP4"
    },
    "hex_gem8|b/E2_HSmean/t2": {
     "bi": 2.220446049250313e-14,
     "fit": null,
     "odf_reading": "hexP2"
    },
    "hex_gem8|b/E2_HSmean/t4": {
     "bi": -5.1810407815840636e-15,
     "fit": null,
     "odf_reading": "hexP4"
    },
    "hex_gem8|b/E2_Hill/t2": {
     "bi": 2.572016673714946e-14,
     "fit": 4.895751529361098e-13,
     "odf_reading": "hexP2"
    },
    "hex_gem8|b/E2_Hill/t4": {
     "bi": -1.295260195396016e-14,
     "fit": -2.664544112656851e-13,
     "odf_reading": "hexP4"
    },
    "hex_gem8|b/h_Hill/t2": {
     "bi": -9.251858538542972e-16,
     "fit": 1.861754403597132e-14,
     "odf_reading": "hexP2"
    },
    "hex_gem8|b/h_Hill/t4": {
     "bi": 6.29126380620922e-15,
     "fit": 8.256781483484296e-14,
     "odf_reading": "hexP4"
    },
    "hex_step|a/E2_HSmean/t2": {
     "bi": 7.031412489292658e-15,
     "fit": null,
     "odf_reading": "hexP2"
    },
    "hex_step|a/E2_HSmean/t4": {
     "bi": 2.960594732333751e-15,
     "fit": null,
     "odf_reading": "hexP4"
    },
    "hex_step|a/E2_Hill/t2": {
     "bi": 9.25185853854297e-15,
     "fit": 1.6266231256261696e-13,
     "odf_reading": "hexP2"
    },
    "hex_step|a/E2_Hill/t4": {
     "bi": -1.4062824978585317e-14,
     "fit": -2.2136167800606602e-13,
     "odf_reading": "hexP4"
    },
    "hex_step|a/h_Hill/t2": {
     "bi": 5.551115123125783e-16,
     "fit": 4.563941055176853e-15,
     "odf_reading": "hexP2"
    },
    "hex_step|a/h_Hill/t4": {
     "bi": 6.47630097698008e-15,
     "fit": 7.665423084547844e-14,
     "odf_reading": "hexP4"
    },
    "hex_step|b/E2_HSmean/t2": {
     "bi": 8.141635513917814e-15,
     "fit": null,
     "odf_reading": "hexP2"
    },
    "hex_step|b/E2_HSmean/t4": {
     "bi": 3.700743415417189e-15,
     "fit": null,
     "odf_reading": "hexP4"
    },
    "hex_step|b/E2_Hill/t2": {
     "bi": 1.0732155904709847e-14,
     "fit": 1.6125034658616313e-13,
     "odf_reading": "hexP2"
    },
    "hex_step|b/E2_Hill/t4": {
     "bi": -8.881784197001252e-15,
     "fit": -2.1990268388075987e-13,
     "odf_reading": "hexP4"
    },
    "hex_step|b/h_Hill/t2": {
     "bi": 0.0,
     "fit": 6.550087858874976e-15,
     "odf_reading": "hexP2"
    },
    "hex_step|b/h_Hill/t4": {
     "bi": 4.9960036108132044e-15,
     "fit": 7.485871681214715e-14,
     "odf_reading": "hexP4"
    }
   },
   "N-2": {
    "cubic_gem8|001": {
     "bi_5x5": -9.422566430809336e-11,
     "bi_cc": 1.2027416100105863e-12,
     "bi_chat": -5.782411586589357e-13,
     "fit7": 3.4778572462814414e-07,
     "odf_reading": "cubP2K4-i"
    },
    "cubic_gem8|111": {
     "bi_5x5": -9.423484215176359e-11,
     "bi_cc": -3.7007434154171886e-13,
     "bi_chat": -1.8503717077085943e-13,
     "fit7": 3.477857238465428e-07,
     "odf_reading": "cubP2K4-i"
    },
    "cubic_step|001": {
     "bi_5x5": -3.529946705308854e-11,
     "bi_cc": -7.632783294297951e-13,
     "bi_chat": -6.707597440443654e-13,
     "fit7": 1.974043374986076e-07,
     "odf_reading": "cubP2K4-i"
    },
    "cubic_step|111": {
     "bi_5x5": -3.529236162573094e-11,
     "bi_cc": -2.220446049250313e-12,
     "bi_chat": 7.401486830834377e-13,
     "fit7": 1.9740433870651724e-07,
     "odf_reading": "cubP2K4-i"
    },
    "hex_gem8|a": {
     "bi_5x5": 1.3922196728799463e-12,
     "bi_cc": 1.3646491344350882e-12,
     "bi_chat": -5.319818659662209e-13,
     "fit7": -1.837213417851943e-08,
     "odf_reading": "hexP2P4"
    },
    "hex_gem8|b": {
     "bi_5x5": 1.3871866618349789e-12,
     "bi_cc": 9.483155002006545e-13,
     "bi_chat": 6.938893903907228e-13,
     "fit7": -1.8376074990497388e-08,
     "odf_reading": "hexP2P4"
    },
    "hex_step|a": {
     "bi_5x5": 6.988483865673819e-13,
     "bi_cc": 3.006854025026466e-13,
     "bi_chat": 9.483155002006545e-13,
     "fit7": -1.2488790730491887e-08,
     "odf_reading": "hexP2P4"
    },
    "hex_step|b": {
     "bi_5x5": 6.846375318521799e-13,
     "bi_cc": 1.8503717077085943e-13,
     "bi_chat": 2.544261098099317e-13,
     "fit7": -1.2484615083901236e-08,
     "odf_reading": "hexP2P4"
    }
   },
   "N-3": {
    "cubic_gem8|001": {
     "bi": -1.1842378929335001e-13,
     "fit": -1.4940723442743361e-16,
     "odf_reading": "cubP2-i",
     "pure_l2_change_t1": 2.220446049250313e-16
    },
    "cubic_gem8|111": {
     "bi": -1.221245327087672e-13,
     "fit": 1.272728293270753e-16,
     "odf_reading": "cubP2-i",
     "pure_l2_change_t1": 2.220446049250313e-16
    },
    "cubic_step|001": {
     "bi": -2.5905203907920314e-14,
     "fit": 3.141702123932416e-15,
     "odf_reading": "cubP2-i",
     "pure_l2_change_t1": 1.1102230246251565e-16
    },
    "cubic_step|111": {
     "bi": -2.775557561562891e-14,
     "fit": -1.6739143857147652e-16,
     "odf_reading": "cubP2-i",
     "pure_l2_change_t1": 3.3306690738754696e-16
    }
   },
   "N-4": {
    "cubic_gem8|001": {
     "bi_5x5": -8.881784197001252e-15,
     "fit7": 7.963757933367799e-09,
     "k12_chat_t2sq": null,
     "odf_reading": "cubP2K4-i"
    },
    "cubic_gem8|111": {
     "bi_5x5": 1.0658141036401503e-14,
     "fit7": -5.3091738364530734e-09,
     "k12_chat_t2sq": null,
     "odf_reading": "cubP2K4-i"
    },
    "cubic_step|001": {
     "bi_5x5": 0.0,
     "fit7": 4.48191107636109e-09,
     "k12_chat_t2sq": -9.053974820150282e-15,
     "odf_reading": "cubP2K4-i"
    },
    "cubic_step|111": {
     "bi_5x5": 0.0,
     "fit7": -2.98793883027198e-09,
     "k12_chat_t2sq": null,
     "odf_reading": "cubP2K4-i"
    }
   }
  },
  "reach": {
   "cubic_gem8|001": {
    "E2_HSmean": {
     "box": [
      -2.9794699690144212e-05,
      0.0
     ],
     "grid_exceeds_box": true,
     "grid_max": 0.0,
     "grid_min": -2.9853890737618904e-05,
     "hull": [
      -2.9853890737618904e-05,
      0.0
     ],
     "widened": [
      -3.28392798113808e-05,
      0.0
     ]
    },
    "E2_Hill": {
     "box": [
      -2.8079818339351056e-05,
      0.0
     ],
     "grid_exceeds_box": true,
     "grid_max": 2.220446049250313e-16,
     "grid_min": -2.9494540072172448e-05,
     "hull": [
      -2.9494540072172448e-05,
      0.0
     ],
     "widened": [
      -3.2443994079389694e-05,
      0.0
     ]
    },
    "h_Hill": {
     "box": [
      -2.8348639164055705e-06,
      0.0
     ],
     "grid_exceeds_box": true,
     "grid_max": 0.0,
     "grid_min": -2.86299115281885e-06,
     "hull": [
      -2.86299115281885e-06,
      0.0
     ],
     "widened": [
      -3.1492902681007354e-06,
      0.0
     ]
    }
   },
   "cubic_gem8|111": {
    "E2_HSmean": {
     "box": [
      0.0,
      1.9863133126560664e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.9902593825005255e-05,
     "grid_min": 0.0,
     "hull": [
      0.0,
      1.9902593825005255e-05
     ],
     "widened": [
      0.0,
      2.1892853207505782e-05
     ]
    },
    "E2_Hill": {
     "box": [
      0.0,
      1.871987889305443e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 2.011479498964519e-05,
     "grid_min": 0.0,
     "hull": [
      0.0,
      2.011479498964519e-05
     ],
     "widened": [
      0.0,
      2.2126274488609713e-05
     ]
    },
    "h_Hill": {
     "box": [
      -2.8348639164055705e-06,
      0.0
     ],
     "grid_exceeds_box": true,
     "grid_max": 0.0,
     "grid_min": -2.86299115281885e-06,
     "hull": [
      -2.86299115281885e-06,
      0.0
     ],
     "widened": [
      -3.1492902681007354e-06,
      0.0
     ]
    }
   },
   "cubic_step|001": {
    "E2_HSmean": {
     "box": [
      -2.4329046584695784e-05,
      0.0
     ],
     "grid_exceeds_box": true,
     "grid_max": -1.1102230246251565e-16,
     "grid_min": -2.4368267510732622e-05,
     "hull": [
      -2.4368267510732622e-05,
      0.0
     ],
     "widened": [
      -2.6805094261805885e-05,
      0.0
     ]
    },
    "E2_Hill": {
     "box": [
      -2.3397058863597962e-05,
      0.0
     ],
     "grid_exceeds_box": true,
     "grid_max": 2.220446049250313e-16,
     "grid_min": -2.437491187379237e-05,
     "hull": [
      -2.437491187379237e-05,
      0.0
     ],
     "widened": [
      -2.681240306117161e-05,
      0.0
     ]
    },
    "h_Hill": {
     "box": [
      -2.3767704795912803e-06,
      0.0
     ],
     "grid_exceeds_box": true,
     "grid_max": 2.220446049250313e-16,
     "grid_min": -2.397505487583551e-06,
     "hull": [
      -2.397505487583551e-06,
      0.0
     ],
     "widened": [
      -2.6372560363419064e-06,
      0.0
     ]
    }
   },
   "cubic_step|111": {
    "E2_HSmean": {
     "box": [
      0.0,
      1.621936438987864e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.6245511674117807e-05,
     "grid_min": -1.1102230246251565e-16,
     "hull": [
      0.0,
      1.6245511674117807e-05
     ],
     "widened": [
      0.0,
      1.787006284152959e-05
     ]
    },
    "E2_Hill": {
     "box": [
      0.0,
      1.5598039242327573e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.656215744905154e-05,
     "grid_min": 0.0,
     "hull": [
      0.0,
      1.656215744905154e-05
     ],
     "widened": [
      0.0,
      1.8218373193956695e-05
     ]
    },
    "h_Hill": {
     "box": [
      -2.3767704795912803e-06,
      0.0
     ],
     "grid_exceeds_box": true,
     "grid_max": 2.220446049250313e-16,
     "grid_min": -2.397505487583551e-06,
     "hull": [
      -2.397505487583551e-06,
      0.0
     ],
     "widened": [
      -2.6372560363419064e-06,
      0.0
     ]
    }
   },
   "hex_gem8|a": {
    "E2_HSmean": {
     "box": [
      -0.00011783134234274472,
      1.11831617857859e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.118972928826345e-05,
     "grid_min": -0.00011785019986731982,
     "hull": [
      -0.00011785019986731982,
      1.118972928826345e-05
     ],
     "widened": [
      -0.0001296352198540518,
      1.2308702217089796e-05
     ]
    },
    "E2_Hill": {
     "box": [
      -0.00011847803016688345,
      1.1219205987177572e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.1222636018715093e-05,
     "grid_min": -0.00011849743822156533,
     "hull": [
      -0.00011849743822156533,
      1.1222636018715093e-05
     ],
     "widened": [
      -0.00013034718204372187,
      1.2344899620586603e-05
     ]
    },
    "h_Hill": {
     "box": [
      -6.877382215886397e-07,
      0.0
     ],
     "grid_exceeds_box": false,
     "grid_max": 0.0,
     "grid_min": -4.860845420617821e-07,
     "hull": [
      -6.877382215886397e-07,
      0.0
     ],
     "widened": [
      -7.565120437475037e-07,
      0.0
     ]
    }
   },
   "hex_gem8|b": {
    "E2_HSmean": {
     "box": [
      -0.0001178622552661443,
      1.1182795648959158e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.1189362505659162e-05,
     "grid_min": -0.0001178811207174224,
     "hull": [
      -0.0001178811207174224,
      1.1189362505659162e-05
     ],
     "widened": [
      -0.00012966923278916466,
      1.230829875622508e-05
     ]
    },
    "E2_Hill": {
     "box": [
      -0.00011850859165776415,
      1.1218844596816173e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.1222273463173948e-05,
     "grid_min": -0.00011852799934330971,
     "hull": [
      -0.00011852799934330971,
      1.1222273463173948e-05
     ],
     "widened": [
      -0.0001303807992776407,
      1.2344500809491344e-05
     ]
    },
    "h_Hill": {
     "box": [
      -6.877857020906448e-07,
      0.0
     ],
     "grid_exceeds_box": false,
     "grid_max": 0.0,
     "grid_min": -4.860355559133112e-07,
     "hull": [
      -6.877857020906448e-07,
      0.0
     ],
     "widened": [
      -7.565642722997094e-07,
      0.0
     ]
    }
   },
   "hex_step|a": {
    "E2_HSmean": {
     "box": [
      -8.926154480396229e-05,
      9.993315480273562e-06
     ],
     "grid_exceeds_box": true,
     "grid_max": 9.998838376379382e-06,
     "grid_min": -8.927425424842816e-05,
     "hull": [
      -8.927425424842816e-05,
      9.998838376379382e-06
     ],
     "widened": [
      -9.820167967327098e-05,
      1.0998722214017322e-05
     ]
    },
    "E2_Hill": {
     "box": [
      -8.99663605935437e-05,
      1.0025334133979992e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.0028797479577634e-05,
     "grid_min": -8.997788565145992e-05,
     "hull": [
      -8.997788565145992e-05,
      1.0028797479577634e-05
     ],
     "widened": [
      -9.897567421660592e-05,
      1.1031677227535398e-05
     ]
    },
    "h_Hill": {
     "box": [
      -5.947031162584856e-07,
      0.0
     ],
     "grid_exceeds_box": false,
     "grid_max": 0.0,
     "grid_min": -4.7064235364491225e-07,
     "hull": [
      -5.947031162584856e-07,
      0.0
     ],
     "widened": [
      -6.541734278843342e-07,
      0.0
     ]
    }
   },
   "hex_step|b": {
    "E2_HSmean": {
     "box": [
      -8.921371417013266e-05,
      9.993911557712254e-06
     ],
     "grid_exceeds_box": true,
     "grid_max": 9.999435379270949e-06,
     "grid_min": -8.922641129294195e-05,
     "hull": [
      -8.922641129294195e-05,
      9.999435379270949e-06
     ],
     "widened": [
      -9.814905242223616e-05,
      1.0999378917198045e-05
     ]
    },
    "E2_Hill": {
     "box": [
      -8.991891992181769e-05,
      1.0025916564630367e-05
     ],
     "grid_exceeds_box": true,
     "grid_max": 1.0029381496190481e-05,
     "grid_min": -8.993044558192054e-05,
     "hull": [
      -8.993044558192054e-05,
      1.0029381496190481e-05
     ],
     "widened": [
      -9.89234901401126e-05,
      1.103231964580953e-05
     ]
    },
    "h_Hill": {
     "box": [
      -5.946513351879505e-07,
      0.0
     ],
     "grid_exceeds_box": false,
     "grid_max": 0.0,
     "grid_min": -4.70722723466821e-07,
     "hull": [
      -5.946513351879505e-07,
      0.0
     ],
     "widened": [
      -6.541164687067457e-07,
      0.0
     ]
    }
   }
  },
  "summary": {
   "b1_dominance_at_D_min": 404.9282983075056,
   "b1_over_kappa44": {
    "cubic_gem8|001": 101.2320745768764,
    "cubic_gem8|111": 151.84811186406765,
    "cubic_step|001": 101.23789387624376,
    "cubic_step|111": 151.85684081505752,
    "hex_gem8|a": 101.2487120966351,
    "hex_gem8|b": 101.24871233675518,
    "hex_step|a": 101.24883302011449,
    "hex_step|b": 101.24883266612132
   },
   "b1_twoleg_rel_max": 6.476723471215587e-13,
   "fit_res_max_by_arm": {
    "E2_HSmean": 2.270909640721569e-05,
    "E2_Hill": 0.00018194430841970036,
    "h_Hill": 0.0007269110377504565
   },
   "grid_excess_over_box_max": {
    "negative_side": 1.0503821540340523,
    "positive_side": 1.0745152308174553
   },
   "grid_excess_over_box_max_by_arm": {
    "E2_HSmean": 1.0019866301148546,
    "E2_Hill": 1.0745152308174553,
    "h_Hill": 1.0099219000427164
   },
   "hs_over_hill_minus_1": {
    "cubic_gem8|001": {
     "t4": 0.06107166827322108
    },
    "cubic_gem8|111": {
     "t4": 0.061071668253709355
    },
    "cubic_step|001": {
     "t4": 0.03983354175117482
    },
    "cubic_step|111": {
     "t4": 0.039833541761134406
    },
    "hex_gem8|a": {
     "t2": -0.005458293180835572,
     "t4": -0.0032127230245051486
    },
    "hex_gem8|b": {
     "t2": -0.005453920113120403,
     "t4": -0.0032132495949934725
    },
    "hex_step|a": {
     "t2": -0.007834214754620095,
     "t4": -0.0031937742202432506
    },
    "hex_step|b": {
     "t2": -0.00784268485762718,
     "t4": -0.003192227534689618
    }
   },
   "k_fire_WEM": 7.969892024557444e+31,
   "null_max_abs": {
    "N-1_bi_by_arm": {
     "E2_HSmean": 2.5054032922374364e-13,
     "E2_Hill": 2.173076533532973e-12,
     "h_Hill": 1.2118084313783584e-12
    },
    "N-1_fit_by_arm": {
     "E2_Hill": 4.267168229021896e-11,
     "h_Hill": 2.385281734789809e-11
    },
    "N-2_by_estimator_cubic": {
     "bi_5x5": 9.423484215176359e-11,
     "bi_cc": 2.220446049250313e-12,
     "bi_chat": 7.401486830834377e-13,
     "fit7": 3.4778572462814414e-07
    },
    "N-2_by_estimator_hex": {
     "bi_5x5": 1.3922196728799463e-12,
     "bi_cc": 1.3646491344350882e-12,
     "bi_chat": 9.483155002006545e-13,
     "fit7": 1.8376074990497388e-08
    },
    "N-3_bi": 1.221245327087672e-13,
    "N-3_fit": 3.141702123932416e-15,
    "N-4_bi_5x5": 1.0658141036401503e-14,
    "N-4_fit7": 7.963757933367799e-09,
    "N-4_k12_chat": 9.053974820150282e-15
   },
   "pure_l2_change_t1_max": 3.3306690738754696e-16,
   "quadform_kappa22_twoleg_rel_max": 1.1439264470668777e-12,
   "recon_max_abs_E2_Hill": {
    "t2": 1.413470088315518e-10,
    "t4": 6.845659647617054e-10
   },
   "trunc_T_at_D_max": 0.0021121968553136795,
   "twoleg_S_abs_max": 2.7504827357592218e-15,
   "twoleg_kappa3_rel_max": 2.0791999660278074e-07,
   "twoleg_rel_max": 1.10862881023457e-09,
   "twoleg_rel_max_by_arm_family": {
    "E2_HSmean/t4": 1.6684801315550194e-11,
    "E2_Hill/t2": 2.6982626041257274e-12,
    "E2_Hill/t4": 2.087011183018691e-11,
    "h_Hill/t2": 1.10862881023457e-09,
    "h_Hill/t4": 3.2074778101782324e-10
   },
   "zero_ctrl_max_abs": 3.3306690738754696e-16
  },
  "synthetic": {
   "margin_negative": [
    -0.00012741759929405796,
    -0.00012149119932689245
   ],
   "margin_positive": [
    2.061766486438632e-05,
    2.1623404613868583e-05
   ],
   "robustness_only_positive": [
    1.428737346285125e-05,
    1.8172321147380544e-05
   ]
  },
  "unions": {
   "hull_all": [
    -0.00011852799934330971,
    2.011479498964519e-05
   ],
   "hull_primary": [
    -0.00011849743822156533,
    1.1222636018715093e-05
   ],
   "widened_all": [
    -0.0001303807992776407,
    2.2126274488609713e-05
   ],
   "widened_primary": [
    -0.00013034718204372187,
    1.2344899620586603e-05
   ]
  },
  "zero_ctrl": {
   "cubic_gem8|001": {
    "E2_HSmean/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_HSmean/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    }
   },
   "cubic_gem8|111": {
    "E2_HSmean/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_HSmean/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    }
   },
   "cubic_step|001": {
    "E2_HSmean/t2": {
     "odf_reading": "uniform",
     "r0": -1.1102230246251565e-16
    },
    "E2_HSmean/t4": {
     "odf_reading": "uniform",
     "r0": -1.1102230246251565e-16
    },
    "E2_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 2.220446049250313e-16
    },
    "h_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 2.220446049250313e-16
    }
   },
   "cubic_step|111": {
    "E2_HSmean/t2": {
     "odf_reading": "uniform",
     "r0": -1.1102230246251565e-16
    },
    "E2_HSmean/t4": {
     "odf_reading": "uniform",
     "r0": -1.1102230246251565e-16
    },
    "E2_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 2.220446049250313e-16
    },
    "h_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 2.220446049250313e-16
    }
   },
   "hex_gem8|a": {
    "E2_HSmean/t2": {
     "odf_reading": "uniform",
     "r0": -2.220446049250313e-16
    },
    "E2_HSmean/t4": {
     "odf_reading": "uniform",
     "r0": -2.220446049250313e-16
    },
    "E2_Hill/t2": {
     "odf_reading": "uniform",
     "r0": -2.220446049250313e-16
    },
    "E2_Hill/t4": {
     "odf_reading": "uniform",
     "r0": -2.220446049250313e-16
    },
    "h_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    }
   },
   "hex_gem8|b": {
    "E2_HSmean/t2": {
     "odf_reading": "uniform",
     "r0": -3.3306690738754696e-16
    },
    "E2_HSmean/t4": {
     "odf_reading": "uniform",
     "r0": -3.3306690738754696e-16
    },
    "E2_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    }
   },
   "hex_step|a": {
    "E2_HSmean/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_HSmean/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    }
   },
   "hex_step|b": {
    "E2_HSmean/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_HSmean/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "E2_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t2": {
     "odf_reading": "uniform",
     "r0": 0.0
    },
    "h_Hill/t4": {
     "odf_reading": "uniform",
     "r0": 0.0
    }
   }
  }
 },
 "grids": {
  "area_grid": {
   "hi": 0.25,
   "lo": -0.25,
   "node": "lo + i*(hi - lo)/(nodes_per_axis - 1)",
   "nodes_per_axis": 201
  },
  "fit_window": "abs(t) <= D, inclusive (the window both banked legs used; H-CC-1)",
  "grid5x5_layout": "row-major, t2 outer, t4 inner: index = 5*i + j for (t2_axis[i], t4_axis[j])",
  "richardson_formulas": {
   "even": "[4*E(h1) - E(h2)]/3, E(h) = [r(h) + r(-h) - 2*r(0)]/(2h^2)",
   "mixed": "[4*M(h1) - M(h2)]/3, M(h) = [R(h,h) - R(h,-h) - R(-h,h) + R(-h,-h)]/(4h^2)",
   "odd": "[4*O(h1) - O(h2)]/3, O(h) = [r(h) - r(-h)]/(2h)"
  },
  "richardson_pairs": {
   "one_param": [
    0.05,
    0.1
   ],
   "two_param": [
    0.125,
    0.25
   ]
  },
  "t2t4_axis": [
   -0.25,
   -0.125,
   0.0,
   0.125,
   0.25
  ],
  "t_grid": [
   -0.5,
   -0.25,
   -0.1,
   -0.05,
   -0.02,
   0.0,
   0.02,
   0.05,
   0.1,
   0.25,
   0.5,
   1.0
  ]
 },
 "provenance": {
  "grids/t2t4_axis": {
   "pointer": "/t2t4_grid",
   "scope": "global",
   "src": "G2chat"
  },
  "grids/t_grid": {
   "pointer": "/t4_grid",
   "scope": "global",
   "src": "G2chat"
  },
  "keys/<K>/A31_mixed_change_cc": {
   "pointer": "/extras/A3_diagnostics/A-3.1_mixed_r_agg_change_A29/{K}",
   "scope": "cubic",
   "src": "G2cc"
  },
  "keys/<K>/arms/E2_HSmean/t2/grid": {
   "pointer": "/phase2/{K}/r_agg_E2_HS",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/E2_HSmean/t2/kappa": {
   "pointer": "/phase2/{K}/kappa2_E2_HS",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/E2_HSmean/t4/grid": {
   "pointer": "/phase2/{K}/r_agg_E2_HS",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/E2_HSmean/t4/kappa": {
   "pointer": "/phase2/{K}/kappa44_E2_HS",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/E2_HSmean/t4/kappa_cc": {
   "pointer": "/phase2/{K}/kappa44_E2_HS",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/arms/E2_Hill/t2/S": {
   "pointer": "/phase2/{K}/S_t_E2",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/E2_Hill/t2/S_cc": {
   "pointer": "/phase2/{K}/S_t_E2",
   "scope": "all",
   "src": "G1cc"
  },
  "keys/<K>/arms/E2_Hill/t2/grid": {
   "pointer": "/phase2/{K}/r_agg_E2_VRH",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/E2_Hill/t2/kappa": {
   "pointer": "/phase2/{K}/kappa2_E2",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/E2_Hill/t2/kappa3": {
   "pointer": "/phase2/{K}/kappa3_E2",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/E2_Hill/t2/kappa3_cc": {
   "pointer": "/phase2/{K}/kappa3_E2",
   "scope": "all",
   "src": "G1cc"
  },
  "keys/<K>/arms/E2_Hill/t2/kappa_cc": {
   "pointer": "/phase2/{K}/kappa2_E2",
   "scope": "all",
   "src": "G1cc"
  },
  "keys/<K>/arms/E2_Hill/t4/S": {
   "pointer": "/phase2/{K}/S4_E2",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/E2_Hill/t4/S_cc": {
   "pointer": "/phase2/{K}/S4_E2",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/arms/E2_Hill/t4/grid": {
   "pointer": "/phase2/{K}/r_agg_E2_VRH",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/E2_Hill/t4/kappa": {
   "pointer": "/phase2/{K}/kappa44_E2",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/E2_Hill/t4/kappa3": {
   "pointer": "/phase2/{K}/kappa444_E2",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/E2_Hill/t4/kappa3_cc": {
   "pointer": "/phase2/{K}/kappa444_E2",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/arms/E2_Hill/t4/kappa_cc": {
   "pointer": "/phase2/{K}/kappa44_E2",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/arms/h_Hill/t2/S": {
   "pointer": "/phase2/{K}/S_t_h",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/h_Hill/t2/S_cc": {
   "pointer": "/phase2/{K}/S_t_h",
   "scope": "all",
   "src": "G1cc"
  },
  "keys/<K>/arms/h_Hill/t2/grid": {
   "pointer": "/phase2/{K}/r_agg_h_VRH",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/h_Hill/t2/kappa": {
   "pointer": "/phase2/{K}/kappa2_h",
   "scope": "all",
   "src": "G1chat"
  },
  "keys/<K>/arms/h_Hill/t2/kappa_cc": {
   "pointer": "/phase2/{K}/kappa2_h",
   "scope": "all",
   "src": "G1cc"
  },
  "keys/<K>/arms/h_Hill/t4/S": {
   "pointer": "/phase2/{K}/S4_h",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/h_Hill/t4/S_cc": {
   "pointer": "/phase2/{K}/S4_h",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/arms/h_Hill/t4/grid": {
   "pointer": "/phase2/{K}/r_agg_h_VRH",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/h_Hill/t4/kappa": {
   "pointer": "/phase2/{K}/kappa44_h",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/arms/h_Hill/t4/kappa_cc": {
   "pointer": "/phase2/{K}/kappa44_h",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/b1_Hill": {
   "pointer": "/phase2/{K}/biref_b1_VRH",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/b1_Hill_cc": {
   "pointer": "/phase2/{K}/biref_b1_VRH",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/kappa24_bi_cc": {
   "pointer": "/phase2/{K}/kappa24_richardson",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/kappa24_bi_chat": {
   "pointer": "/{K}/kappa24_richardson",
   "scope": "all",
   "src": "DK24"
  },
  "keys/<K>/pure_l2_change_t1": {
   "pointer": "/{K}/pure_l2_r_agg_change_t1",
   "scope": "cubic",
   "src": "DK24"
  },
  "keys/<K>/quadform/basis_k12_chat": {
   "pointer": "/{K}/k12",
   "scope": "dqf",
   "src": "DQF"
  },
  "keys/<K>/quadform/basis_k7_chat": {
   "pointer": "/{K}/k7",
   "scope": "dqf",
   "src": "DQF"
  },
  "keys/<K>/quadform/cubic_terms_cc": {
   "pointer": "/phase2/{K}/quadform/x_cubic_terms_discarded",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/quadform/grid5x5_cc": {
   "pointer": "/phase2/{K}/quadform/x_grid_r_agg_E2_VRH",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/quadform/kappa22_fit7": {
   "pointer": "/phase2/{K}/quadform/kappa22",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/quadform/kappa22_fit7_cc": {
   "pointer": "/phase2/{K}/quadform/kappa22",
   "scope": "all",
   "src": "G2cc"
  },
  "keys/<K>/quadform/kappa24_fit7": {
   "pointer": "/phase2/{K}/quadform/kappa24",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/quadform/kappa44_fit7": {
   "pointer": "/phase2/{K}/quadform/kappa44",
   "scope": "all",
   "src": "G2chat"
  },
  "keys/<K>/quadform/reading_cc": {
   "pointer": "/phase2/{K}/quadform/x_reading",
   "scope": "all",
   "src": "G2cc"
  },
  "raw/regime/d_EM": {
   "pointer": "/per_oom/x1/W_EM_union/0/1",
   "scope": "global",
   "src": "CI1"
  }
 },
 "raw": {
  "keys": {
   "cubic_gem8|001": {
    "A31_mixed_change_cc": -1.3041577882066946e-06,
    "arms": {
     "E2_HSmean": {
      "t2": {
       "grid": [
        0.0,
        0.0,
        -2.220446049250313e-16,
        0.0,
        0.0,
        0.0,
        -3.3306690738754696e-16,
        0.0,
        0.0,
        0.0,
        0.0,
        -3.3306690738754696e-16
       ],
       "kappa": -2.9328086757977686e-16
      },
      "t4": {
       "grid": [
        -0.00011966081632819314,
        -2.9853890737618904e-05,
        -4.770848111346204e-06,
        -1.1922353594373547e-06,
        -1.907120693589448e-07,
        0.0,
        -1.9065148326724568e-07,
        -1.1912887032394792e-06,
        -4.763274711439003e-06,
        -2.9735539746722495e-05,
        -0.00011871353319847788,
        -0.000473085445427901
       ],
       "kappa": -0.0004767151950423074,
       "kappa_cc": -0.00047671519504299364
      }
     },
     "E2_Hill": {
      "t2": {
       "S": 2.2690471976516216e-16,
       "S_cc": -9.550804974045757e-16,
       "grid": [
        -2.220446049250313e-16,
        0.0,
        0.0,
        -2.220446049250313e-16,
        -2.220446049250313e-16,
        0.0,
        0.0,
        -2.220446049250313e-16,
        0.0,
        0.0,
        0.0,
        -2.220446049250313e-16
       ],
       "kappa": -1.4940723442743361e-16,
       "kappa3": -3.710299357793312e-15,
       "kappa3_cc": 1.5179666171081885e-14,
       "kappa_cc": -2.9881446885486723e-16
      },
      "t4": {
       "S": -4.267168229021896e-11,
       "S_cc": -4.267032120491424e-11,
       "grid": [
        -0.00011285904498181676,
        -2.813923524602746e-05,
        -4.495877947818805e-06,
        -1.1234705115104049e-06,
        -1.7970867816075042e-07,
        0.0,
        -1.796480421090152e-07,
        -1.1225230265310415e-06,
        -4.488296764137978e-06,
        -2.8020636270609245e-05,
        -0.00011190615454603758,
        -0.0004466673069934979
       ],
       "kappa": -0.0004492770934296169,
       "kappa3": 3.7958466556260277e-06,
       "kappa3_cc": 3.7958466267304677e-06,
       "kappa_cc": -0.00044927709343161725
      }
     },
     "h_Hill": {
      "t2": {
       "S": 1.0207029061365447e-15,
       "S_cc": 0.0,
       "grid": [
        0.0,
        2.220446049250313e-16,
        -2.220446049250313e-16,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2.220446049250313e-16,
        2.220446049250313e-16
       ],
       "kappa": 1.4525703347111552e-15,
       "kappa_cc": 0.0
      },
      "t4": {
       "S": -2.385281734789809e-11,
       "S_cc": -2.3853273799039695e-11,
       "grid": [
        -1.1590815615636352e-05,
        -2.86299115281885e-06,
        -4.5509719270864224e-07,
        -1.1353983042639015e-07,
        -1.8144388991281346e-08,
        0.0,
        -1.8115683841912755e-08,
        -1.1309128233882859e-07,
        -4.515080809230909e-07,
        -2.806831356338968e-06,
        -1.1139242344304634e-05,
        -4.4028971179166376e-05
       ],
       "kappa": -4.535782266248913e-05,
       "kappa_cc": -4.5357822665197825e-05
      }
     }
    },
    "b1_Hill": -0.04548125222774924,
    "b1_Hill_cc": -0.045481252227733915,
    "branch": "cubic",
    "kappa24_bi_cc": 1.2027416100105863e-12,
    "kappa24_bi_chat": -5.782411586589357e-13,
    "pure_l2_change_t1": 2.220446049250313e-16,
    "quadform": {
     "cubic_terms_cc": [
      7.94404069994542e-09,
      -3.7210027738773715e-10,
      -8.510772973814659e-05,
      3.7952989894238772e-06
     ],
     "grid5x5_cc": [
      -2.6783930420104518e-05,
      -6.690981583457045e-06,
      0.0,
      -6.682561632942452e-06,
      -2.671647848284664e-05,
      -2.7461582832954967e-05,
      -6.858695032030404e-06,
      2.220446049250313e-16,
      -6.8470805999476525e-06,
      -2.7368557376838965e-05,
      -2.813923524602746e-05,
      -7.026408480825808e-06,
      2.220446049250313e-16,
      -7.0115995675079645e-06,
      -2.802063627083129e-05,
      -2.8816887658988932e-05,
      -7.194121929177122e-06,
      0.0,
      -7.176118534180098e-06,
      -2.867271516504566e-05,
      -2.9494540072172448e-05,
      -7.3618353776394585e-06,
      2.220446049250313e-16,
      -7.340637501407343e-06,
      -2.9324794059037984e-05
     ],
     "kappa22_fit7": 7.963757933367799e-09,
     "kappa22_fit7_cc": 7.963760249103659e-09,
     "kappa24_fit7": 3.4778572462814414e-07,
     "kappa44_fit7": -0.00044927996760422685,
     "reading_cc": "(i) inherited descriptor-axis P2 (A-3.3)"
    }
   },
   "cubic_gem8|111": {
    "A31_mixed_change_cc": -1.30415778798465e-06,
    "arms": {
     "E2_HSmean": {
      "t2": {
       "grid": [
        -2.220446049250313e-16,
        0.0,
        -2.220446049250313e-16,
        -2.220446049250313e-16,
        0.0,
        0.0,
        0.0,
        -2.220446049250313e-16,
        0.0,
        0.0,
        0.0,
        -3.3306690738754696e-16
       ],
       "kappa": -4.1502009563175863e-16
      },
      "t4": {
       "grid": [
        7.977387755220278e-05,
        1.9902593825005255e-05,
        3.180565407712166e-06,
        7.948235725141473e-07,
        1.2714137898051092e-07,
        0.0,
        1.2710098884483045e-07,
        7.941924689003343e-07,
        3.1755164744406983e-06,
        1.982369316411159e-05,
        7.9142355466022e-05,
        0.00031539029695215604
       ],
       "kappa": 0.00031781013002497063,
       "kappa_cc": 0.00031781013002442837
      }
     },
     "E2_Hill": {
      "t2": {
       "S": -1.1819852171697386e-15,
       "S_cc": 2.925271284971411e-16,
       "grid": [
        -2.220446049250313e-16,
        0.0,
        2.220446049250313e-16,
        -2.220446049250313e-16,
        0.0,
        0.0,
        -2.220446049250313e-16,
        -2.220446049250313e-16,
        0.0,
        0.0,
        -2.220446049250313e-16,
        2.220446049250313e-16
       ],
       "kappa": 1.272728293270753e-16,
       "kappa3": 1.888996552887521e-14,
       "kappa3_cc": -1.1860380658980084e-14,
       "kappa_cc": -2.2936777285248548e-15
      },
      "t4": {
       "S": 2.8447697640179876e-11,
       "S_cc": 2.844703507492917e-11,
       "grid": [
        7.523936332098913e-05,
        1.8759490163944292e-05,
        2.997251965064507e-06,
        7.489803408589069e-07,
        1.1980578551451515e-07,
        0.0,
        1.1976536118396552e-07,
        7.483486843540277e-07,
        2.992197842610622e-06,
        1.8680424180850252e-05,
        7.460410303061771e-05,
        0.0002977782046622579
       ],
       "kappa": 0.00029951806228887087,
       "kappa3": -2.530564419058326e-06,
       "kappa3_cc": -2.5305644157388242e-06,
       "kappa_cc": 0.00029951806228339543
      }
     },
     "h_Hill": {
      "t2": {
       "S": 0.0,
       "S_cc": 0.0,
       "grid": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        4.440892098500626e-16
       ],
       "kappa": 0.0,
       "kappa_cc": 0.0
      },
      "t4": {
       "S": -2.385281734789809e-11,
       "S_cc": -2.3853273799039695e-11,
       "grid": [
        -1.1590815615636352e-05,
        -2.86299115281885e-06,
        -4.5509719270864224e-07,
        -1.1353983042639015e-07,
        -1.8144388991281346e-08,
        0.0,
        -1.8115683841912755e-08,
        -1.1309128233882859e-07,
        -4.515080809230909e-07,
        -2.806831356338968e-06,
        -1.1139242344304634e-05,
        -4.4028971179166376e-05
       ],
       "kappa": -4.535782266248913e-05,
       "kappa_cc": -4.5357822665197825e-05
      }
     }
    },
    "b1_Hill": -0.04548125222774924,
    "b1_Hill_cc": -0.045481252227733915,
    "branch": "cubic",
    "kappa24_bi_cc": -3.7007434154171886e-13,
    "kappa24_bi_chat": -1.8503717077085943e-13,
    "pure_l2_change_t1": 2.220446049250313e-16,
    "quadform": {
     "cubic_terms_cc": [
      7.944032815079988e-09,
      2.4807098986342795e-10,
      -8.510772972257114e-05,
      -2.530199325182433e-06
     ],
     "grid5x5_cc": [
      2.011479498964519e-05,
      5.019699217623241e-06,
      0.0,
      5.003437645978437e-06,
      1.9984581968612858e-05,
      1.943714257679474e-05,
      4.85198576893886e-06,
      4.440892098500626e-16,
      4.8389186786401694e-06,
      1.9332503074620533e-05,
      1.8759490163722248e-05,
      4.684272320254479e-06,
      2.220446049250313e-16,
      4.674399711523947e-06,
      1.8680424180406163e-05,
      1.8081837751315888e-05,
      4.5165588722362315e-06,
      2.220446049250313e-16,
      4.509880744407724e-06,
      1.8028345286635883e-05,
      1.7404185337799305e-05,
      4.34884542355185e-06,
      0.0,
      4.345361777291501e-06,
      1.7376266392421513e-05
     ],
     "kappa22_fit7": -5.3091738364530734e-09,
     "kappa22_fit7_cc": -5.309171208626909e-09,
     "kappa24_fit7": 3.477857238465428e-07,
     "kappa44_fit7": 0.0002995199784038129,
     "reading_cc": "(i) inherited descriptor-axis P2 (A-3.3)"
    }
   },
   "cubic_step|001": {
    "A31_mixed_change_cc": -9.076177710509725e-07,
    "arms": {
     "E2_HSmean": {
      "t2": {
       "grid": [
        2.220446049250313e-16,
        0.0,
        2.220446049250313e-16,
        -2.220446049250313e-16,
        0.0,
        -1.1102230246251565e-16,
        -2.220446049250313e-16,
        -2.220446049250313e-16,
        2.220446049250313e-16,
        -1.1102230246251565e-16,
        -2.220446049250313e-16,
        0.0
       ],
       "kappa": -4.606723061512521e-16
      },
      "t4": {
       "grid": [
        -9.763423144693029e-05,
        -2.4368267510732622e-05,
        -3.895110956775305e-06,
        -9.734623724888536e-07,
        -1.5572379152839488e-07,
        -1.1102230246251565e-16,
        -1.5568364131191004e-07,
        -9.72835024426466e-07,
        -3.890092109437582e-06,
        -2.428984143432178e-05,
        -9.700663450318281e-05,
        -0.00038683591265264994
       ],
       "kappa": -0.00038926474535513255,
       "kappa_cc": -0.0003892647453545792
      }
     },
     "E2_Hill": {
      "t2": {
       "S": 3.872699649800502e-16,
       "S_cc": 7.009496149267015e-17,
       "grid": [
        -2.220446049250313e-16,
        2.220446049250313e-16,
        -1.1102230246251565e-16,
        -1.1102230246251565e-16,
        -1.1102230246251565e-16,
        0.0,
        0.0,
        0.0,
        -1.1102230246251565e-16,
        2.220446049250313e-16,
        0.0,
        -1.1102230246251565e-16
       ],
       "kappa": 3.141702123932416e-15,
       "kappa3": -6.308626889222545e-15,
       "kappa3_cc": -1.317121335111205e-15,
       "kappa_cc": -2.1857725036605986e-16
      },
      "t4": {
       "S": -1.9549678946260598e-11,
       "S_cc": -1.9550561581989927e-11,
       "grid": [
        -9.39538922326566e-05,
        -2.3438263274333515e-05,
        -3.74577545780852e-06,
        -9.361008704855678e-07,
        -1.497439410247381e-07,
        0.0,
        -1.497018550233875e-07,
        -9.354432559671721e-07,
        -3.7405139442503454e-06,
        -2.3355986619622016e-05,
        -9.329380310130198e-05,
        -0.0003723937335883276
       ],
       "kappa": -0.0003743529418175674,
       "kappa3": 2.633164231609963e-06,
       "kappa3_cc": 2.633164259954152e-06,
       "kappa_cc": -0.0003743529418199647
      }
     },
     "h_Hill": {
      "t2": {
       "S": 2.7381760509747877e-16,
       "S_cc": 1.2375133173866637e-30,
       "grid": [
        0.0,
        0.0,
        0.0,
        -1.1102230246251565e-16,
        0.0,
        2.220446049250313e-16,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
       ],
       "kappa": -3.458500796931401e-17,
       "kappa_cc": -3.5691728224331273e-16
      },
      "t4": {
       "S": -1.1694898610377518e-11,
       "S_cc": -1.1695158327148078e-11,
       "grid": [
        -9.68846050775074e-06,
        -2.397505487583551e-06,
        -3.8144366332204527e-07,
        -9.518939547703553e-08,
        -1.5214148607611833e-08,
        2.220446049250313e-16,
        -1.5192968327859546e-08,
        -9.485844321144299e-08,
        -3.787956872614018e-07,
        -2.3560916755371863e-06,
        -9.356026678397633e-06,
        -3.698437991406234e-05
       ],
       "kappa": -3.8028327673460484e-05,
       "kappa_cc": -3.8028327671478075e-05
      }
     }
    },
    "b1_Hill": -0.03789870339598654,
    "b1_Hill_cc": -0.0378987033959945,
    "branch": "cubic",
    "kappa24_bi_cc": -7.632783294297951e-13,
    "kappa24_bi_chat": -6.707597440443654e-13,
    "pure_l2_change_t1": 1.1102230246251565e-16,
    "quadform": {
     "basis_k12_chat": [
      -9.053974820150282e-15,
      -3.529544061534051e-11,
      -0.0003743069390912568,
      3.641060270537046e-09,
      -1.704889076336002e-10,
      -5.901878168607192e-05,
      2.6329133346838128e-06,
      1.540337215208414e-13,
      1.894830996557711e-14,
      -4.412479086589967e-15,
      3.716510718732071e-06,
      -7.529609598691114e-07
     ],
     "basis_k7_chat": [
      4.48191107636109e-09,
      1.974043374986076e-07,
      -0.00037435455939106166,
      3.6410602705142863e-09,
      -1.7048890759809645e-10,
      -5.90187816860719e-05,
      2.632913334683767e-06
     ],
     "cubic_terms_cc": [
      3.641053119147632e-09,
      -1.7049900348209627e-10,
      -5.901878166287058e-05,
      2.6329133467859226e-06
     ],
     "grid5x5_cc": [
      -2.250161467498568e-05,
      -5.62161334682898e-06,
      2.220446049250313e-16,
      -5.614963276112661e-06,
      -2.2448368848349e-05,
      -2.296993897477062e-05,
      -5.737740866873509e-06,
      2.220446049250313e-16,
      -5.7292771964423395e-06,
      -2.2902177733929996e-05,
      -2.3438263274666582e-05,
      -5.8538683869180375e-06,
      2.220446049250313e-16,
      -5.84359111688304e-06,
      -2.3355986619510993e-05,
      -2.3906587574007432e-05,
      -5.969995906629499e-06,
      2.220446049250313e-16,
      -5.957905037323741e-06,
      -2.3809795504758924e-05,
      -2.437491187379237e-05,
      -6.086123426451984e-06,
      2.220446049250313e-16,
      -6.072218957542397e-06,
      -2.4263604390561966e-05
     ],
     "kappa22_fit7": 4.48191107636109e-09,
     "kappa22_fit7_cc": 4.48191140345094e-09,
     "kappa24_fit7": 1.974043374986076e-07,
     "kappa44_fit7": -0.00037435455939106166,
     "reading_cc": "(i) inherited descriptor-axis P2 (A-3.3)"
    }
   },
   "cubic_step|111": {
    "A31_mixed_change_cc": -9.076177709399502e-07,
    "arms": {
     "E2_HSmean": {
      "t2": {
       "grid": [
        -1.1102230246251565e-16,
        2.220446049250313e-16,
        2.220446049250313e-16,
        0.0,
        -1.1102230246251565e-16,
        -1.1102230246251565e-16,
        -1.1102230246251565e-16,
        -1.1102230246251565e-16,
        0.0,
        2.220446049250313e-16,
        -1.1102230246251565e-16,
        0.0
       ],
       "kappa": 3.6895286501663385e-15
      },
      "t4": {
       "grid": [
        6.508948763128686e-05,
        1.6245511674117807e-05,
        2.5967406376281588e-06,
        6.489749149185542e-07,
        1.0381586101892992e-07,
        -1.1102230246251565e-16,
        1.0378909398589542e-07,
        6.48556682580903e-07,
        2.5933947396250545e-06,
        1.619322762280717e-05,
        6.467108966878854e-05,
        0.000257890608435174
       ],
       "kappa": 0.00025950983023805826,
       "kappa_cc": 0.00025950983023583375
      }
     },
     "E2_Hill": {
      "t2": {
       "S": 4.1100077415202465e-16,
       "S_cc": 7.00949614926752e-17,
       "grid": [
        -1.1102230246251565e-16,
        0.0,
        -1.1102230246251565e-16,
        -1.1102230246251565e-16,
        2.220446049250313e-16,
        0.0,
        -1.1102230246251565e-16,
        0.0,
        0.0,
        0.0,
        -3.3306690738754696e-16,
        -2.220446049250313e-16
       ],
       "kappa": -1.6739143857147652e-16,
       "kappa3": -6.477861259177068e-15,
       "kappa3_cc": -1.3171213351113003e-15,
       "kappa_cc": -1.9478276488317234e-15
      },
      "t4": {
       "S": 1.3035416405833344e-11,
       "S_cc": 1.3036078957132319e-11,
       "grid": [
        6.263592815525243e-05,
        1.5625508849481662e-05,
        2.4971836385390134e-06,
        6.240672469903785e-07,
        9.982929394247719e-08,
        0.0,
        9.980123660824347e-08,
        6.236288374594778e-07,
        2.493675963277653e-06,
        1.5570657746266647e-05,
        6.21958687341273e-05,
        0.0002482624890589591
       ],
       "kappa": 0.00024956862787724117,
       "kappa3": -1.7554428600870769e-06,
       "kappa3_cc": -1.7554428634061992e-06,
       "kappa_cc": 0.00024956862787469286
      }
     },
     "h_Hill": {
      "t2": {
       "S": -2.925271284971396e-16,
       "S_cc": 6.568330085717285e-30,
       "grid": [
        -1.1102230246251565e-16,
        0.0,
        0.0,
        0.0,
        2.220446049250313e-16,
        2.220446049250313e-16,
        0.0,
        0.0,
        0.0,
        2.220446049250313e-16,
        0.0,
        -1.1102230246251565e-16
       ],
       "kappa": 1.7403176010158433e-15,
       "kappa_cc": -2.0861676807089763e-15
      },
      "t4": {
       "S": -1.1694898610377518e-11,
       "S_cc": -1.1695158327148078e-11,
       "grid": [
        -9.68846050775074e-06,
        -2.397505487583551e-06,
        -3.8144366332204527e-07,
        -9.518939547703553e-08,
        -1.5214148607611833e-08,
        2.220446049250313e-16,
        -1.5192968327859546e-08,
        -9.485844321144299e-08,
        -3.787956872614018e-07,
        -2.3560916755371863e-06,
        -9.356026678397633e-06,
        -3.698437991406234e-05
       ],
       "kappa": -3.8028327673460484e-05,
       "kappa_cc": -3.8028327671478075e-05
      }
     }
    },
    "b1_Hill": -0.03789870339598654,
    "b1_Hill_cc": -0.0378987033959945,
    "branch": "cubic",
    "kappa24_bi_cc": -2.220446049250313e-12,
    "kappa24_bi_chat": 7.401486830834377e-13,
    "pure_l2_change_t1": 3.3306690738754696e-16,
    "quadform": {
     "cubic_terms_cc": [
      3.641059720302595e-09,
      1.1367343055093113e-10,
      -5.9018781674654424e-05,
      -1.7552755590229606e-06
     ],
     "grid5x5_cc": [
      1.656215744905154e-05,
      4.134833963886919e-06,
      2.220446049250313e-16,
      4.124355251766687e-06,
      1.647827551787273e-05,
      1.6093833149044556e-05,
      4.018706444064435e-06,
      2.220446049250313e-16,
      4.010041331437009e-06,
      1.60244666316256e-05,
      1.5625508849259617e-05,
      3.902578924019906e-06,
      2.220446049250313e-16,
      3.89572741110733e-06,
      1.5570657746266647e-05,
      1.5157184549918767e-05,
      3.7864514044194664e-06,
      2.220446049250313e-16,
      3.7814134909996966e-06,
      1.511684886068565e-05,
      1.4688860249911784e-05,
      3.670323884596982e-06,
      2.220446049250313e-16,
      3.6670995706700182e-06,
      1.4663039975326697e-05
     ],
     "kappa22_fit7": -2.98793883027198e-09,
     "kappa22_fit7_cc": -2.987937980693619e-09,
     "kappa24_fit7": 1.9740433870651724e-07,
     "kappa44_fit7": 0.00024956970625745204,
     "reading_cc": "(i) inherited descriptor-axis P2 (A-3.3)"
    }
   },
   "hex_gem8|a": {
    "arms": {
     "E2_HSmean": {
      "t2": {
       "grid": [
        -0.00047147218794019174,
        -0.00011785019986731982,
        -1.885426634828935e-05,
        -4.71341728180974e-06,
        -7.541323487902929e-07,
        -2.220446049250313e-16,
        -7.54113030021486e-07,
        -4.713115426713266e-06,
        -1.8851851520729213e-05,
        -0.00011781246964737146,
        -0.0004711703880158069,
        -0.0018840138120467254
       ],
       "kappa": -0.0018853014774839155
      },
      "t4": {
       "grid": [
        4.468026881743192e-05,
        1.1176594882256197e-05,
        1.7888838452773115e-06,
        4.472734345117857e-07,
        7.156879000547178e-08,
        -2.220446049250313e-16,
        7.157551462633194e-08,
        4.473785086833715e-07,
        1.7897244393161316e-06,
        1.118972928826345e-05,
        4.478534775564924e-05,
        0.00017935416817671523
       ],
       "kappa": 0.0001789305885725744,
       "kappa_cc": 0.0001789305885712823
      }
     },
     "E2_Hill": {
      "t2": {
       "S": 4.894642365145396e-13,
       "S_cc": 4.88778727245365e-13,
       "grid": [
        -0.00047377007967119855,
        -0.0001184586706243218,
        -1.8955103105455784e-05,
        -4.7389256596641616e-06,
        -7.582427594687857e-07,
        -2.220446049250313e-16,
        -7.582626075919308e-07,
        -4.7392357853670575e-06,
        -1.8957584126733096e-05,
        -0.00011849743822145431,
        -0.00047408026726247776,
        -0.0018971495594123367
       ],
       "kappa": -0.0018956484826701352,
       "kappa3": -1.24057090180438e-06,
       "kappa3_cc": -1.2405708979146963e-06,
       "kappa_cc": -0.0018956484826738256
      },
      "t4": {
       "S": -2.652046374551464e-13,
       "S_cc": -2.6497773212688476e-13,
       "grid": [
        4.48512154973546e-05,
        1.1215782710127797e-05,
        1.7948340194084977e-06,
        4.4873519322585764e-07,
        7.180022998376501e-08,
        -2.220446049250313e-16,
        7.180373828852282e-08,
        4.4879001181996614e-07,
        1.79527257415657e-06,
        1.1222636018715093e-05,
        4.490606733864588e-05,
        0.00017976326080337834
       ],
       "kappa": 0.00017950729579484115,
       "kappa3": 2.1931009732824822e-07,
       "kappa3_cc": 2.1931009361797286e-07,
       "kappa_cc": 0.00017950729579206332
      }
     },
     "h_Hill": {
      "t2": {
       "S": 1.9849252759426836e-14,
       "S_cc": 1.8870073354479004e-14,
       "grid": [
        -8.038770585860888e-07,
        -2.0201977346534505e-07,
        -3.242488200161375e-08,
        -8.11473377382299e-09,
        -1.299176211055908e-09,
        0.0,
        -1.3002692256236514e-09,
        -8.131815554257571e-09,
        -3.256153702224651e-08,
        -2.041550737352793e-07,
        -8.209613446830133e-07,
        -3.3191570847357355e-06
       ],
       "kappa": -3.2493966959289463e-06,
       "kappa_cc": -3.249396699531321e-06
      },
      "t4": {
       "S": 8.394408199844183e-14,
       "S_cc": 8.39909948940018e-14,
       "grid": [
        -1.9274619713627317e-06,
        -4.832185266367972e-07,
        -7.744891550309774e-08,
        -1.937356264303247e-08,
        -3.1008647871644257e-09,
        0.0,
        -3.102331946891468e-09,
        -1.9396488082357166e-08,
        -7.763232257040897e-08,
        -4.860845420617821e-07,
        -1.9503980948076816e-06,
        -7.852781449102508e-06
       ],
       "kappa": -7.754414849489288e-06,
       "kappa_cc": -7.754414848821103e-06
      }
     }
    },
    "b1_Hill": 0.01817488251117739,
    "b1_Hill_cc": 0.018174882511168545,
    "branch": "hex",
    "kappa24_bi_cc": 1.3646491344350882e-12,
    "kappa24_bi_chat": -5.319818659662209e-13,
    "quadform": {
     "cubic_terms_cc": [
      -1.2406272604391896e-06,
      -9.829662260388087e-06,
      -3.579747184617073e-06,
      2.192759781806895e-07
     ],
     "grid5x5_cc": [
      -0.00010703681490453754,
      -0.00011556458006634074,
      -0.00011845867062465487,
      -0.00011571629866791167,
      -0.00010733444339172671,
      -1.8335614543230072e-05,
      -2.678657164734144e-05,
      -2.9616888306382982e-05,
      -2.6823938995890195e-05,
      -1.840486895210436e-05,
      1.1215782709905753e-05,
      2.8043458761839446e-06,
      0.0,
      2.8052024405589293e-06,
      1.1222636018493048e-05,
      -1.8395703234586058e-05,
      -2.6805229290549626e-05,
      -2.9621734073170813e-05,
      -2.684293430765816e-05,
      -1.8466325168220443e-05,
      -0.00010718475434112751,
      -0.0001156303094735911,
      -0.00011849743822156533,
      -0.00011578403746348442,
      -0.00010748778656943792
     ],
     "kappa22_fit7": -0.0018956599069468293,
     "kappa22_fit7_cc": -0.0018956599069480582,
     "kappa24_fit7": -1.837213417851943e-08,
     "kappa44_fit7": 0.00017949842202586976,
     "reading_cc": "hex two-parameter family"
    }
   },
   "hex_gem8|b": {
    "arms": {
     "E2_HSmean": {
      "t2": {
       "grid": [
        -0.0004715958998675607,
        -0.0001178811207174224,
        -1.885921295863291e-05,
        -4.714653872306407e-06,
        -7.543301969725746e-07,
        -3.3306690738754696e-16,
        -7.543108705432289e-07,
        -4.714351890200419e-06,
        -1.8856797115107682e-05,
        -0.00011784337463216499,
        -0.00047129397306711063,
        -0.0018845078483341604
       ],
       "kappa": -0.0018857960842583088
      },
      "t4": {
       "grid": [
        4.467880939684754e-05,
        1.117622939106333e-05,
        1.7888253052156244e-06,
        4.4725879444484917e-07,
        7.156644721284522e-08,
        -3.3306690738754696e-16,
        7.157317138961616e-08,
        4.473638579582939e-07,
        1.7896658164318069e-06,
        1.1189362505659162e-05,
        4.4783877998222366e-05,
        0.00017934826780519053
       ],
       "kappa": 0.00017892473038334653,
       "kappa_cc": 0.0001789247303803612
      }
     },
     "E2_Hill": {
      "t2": {
       "S": 4.895751529361098e-13,
       "S_cc": 4.90291953941434e-13,
       "grid": [
        -0.0004738923403120321,
        -0.00011848923252755217,
        -1.895999284384775e-05,
        -4.740148086490592e-06,
        -7.584383474590339e-07,
        0.0,
        -7.584581946940006e-07,
        -4.740458205976239e-06,
        -1.8962473815165026e-05,
        -0.00011852799934297664,
        -0.0004742025216768475,
        -0.0018976387487924518
       ],
       "kappa": -0.0018961374665242264,
       "kappa3": -1.240545889104786e-06,
       "kappa3_cc": -1.240545911150953e-06,
       "kappa_cc": -0.0018961374665274083
      },
      "t4": {
       "S": -2.664544112656851e-13,
       "S_cc": -2.6449971836009003e-13,
       "grid": [
        4.484977886543007e-05,
        1.121542248339047e-05,
        1.7947762760428532e-06,
        4.4872074855817345e-07,
        7.179791761124932e-08,
        0.0,
        7.180142480578411e-08,
        4.4877554827849053e-07,
        1.795214681576951e-06,
        1.1222273463173948e-05,
        4.490461206385632e-05,
        0.0001797573959907428
       ],
       "kappa": 0.00017950151354905876,
       "kappa3": 2.1923559565364329e-07,
       "kappa3_cc": 2.1923555007017898e-07,
       "kappa_cc": 0.00017950151355280498
      }
     },
     "h_Hill": {
      "t2": {
       "S": 1.861754403597132e-14,
       "S_cc": 1.9232267730539364e-14,
       "grid": [
        -8.04256157782568e-07,
        -2.021152383235858e-07,
        -3.2440223618479536e-08,
        -8.118574701398984e-09,
        -1.2997911635892478e-09,
        0.0,
        -1.3008849553131085e-09,
        -8.13566802815302e-09,
        -3.2576969677400314e-08,
        -2.0425195845774624e-07,
        -8.213518059019265e-07,
        -3.320743002910298e-06
       ],
       "kappa": -3.2509354903061167e-06,
       "kappa_cc": -3.250935490588331e-06
      },
      "t4": {
       "S": 8.256781483484296e-14,
       "S_cc": 8.407053114138355e-14,
       "grid": [
        -1.92726942582766e-06,
        -4.831701241325703e-07,
        -7.744114405294766e-08,
        -1.9371617421271026e-08,
        -3.1005531475614134e-09,
        0.0,
        -3.102020196266153e-09,
        -1.9394538197659017e-08,
        -7.762451403880988e-08,
        -4.860355559133112e-07,
        -1.9502008778982116e-06,
        -7.851981527973173e-06
       ],
       "kappa": -7.753635743144201e-06,
       "kappa_cc": -7.753635743351712e-06
      }
     }
    },
    "b1_Hill": 0.018174297109340813,
    "b1_Hill_cc": 0.018174297109331976,
    "branch": "hex",
    "kappa24_bi_cc": 9.483155002006545e-13,
    "kappa24_bi_chat": 6.938893903907228e-13,
    "quadform": {
     "cubic_terms_cc": [
      -1.2406023432182818e-06,
      -9.831922716422042e-06,
      -3.577712618127711e-06,
      2.1920153310548912e-07
     ],
     "grid5x5_cc": [
      -0.00010706773413393655,
      -0.0001155952227629431,
      -0.0001184892325272191,
      -0.00011574697652394494,
      -0.000107365435008,
      -1.834362212749241e-05,
      -2.679430169083563e-05,
      -2.962452855348463e-05,
      -2.6831678121230773e-05,
      -1.8412896608754892e-05,
      1.1215422483834558e-05,
      2.804255680111112e-06,
      -3.3306690738754696e-16,
      2.8051119533856195e-06,
      1.1222273463173948e-05,
      -1.840367901628781e-05,
      -2.6812951251953265e-05,
      -2.9629374222905902e-05,
      -2.6850665423627795e-05,
      -1.847432084567391e-05,
      -0.00010721560863369284,
      -0.00011566093504566943,
      -0.00011852799934330971,
      -0.00011581469909605069,
      -0.00010751871440861649
     ],
     "kappa22_fit7": -0.0018961488929936498,
     "kappa22_fit7_cc": -0.0018961488929958188,
     "kappa24_fit7": -1.8376074990497388e-08,
     "kappa44_fit7": 0.00017949263950353062,
     "reading_cc": "hex two-parameter family"
    }
   },
   "hex_step|a": {
    "arms": {
     "E2_HSmean": {
      "t2": {
       "grid": [
        -0.0003571461079143745,
        -8.927425424842816e-05,
        -1.4282679909993767e-05,
        -3.5705689754861325e-06,
        -5.71281304040383e-07,
        0.0,
        -5.712682860092855e-07,
        -3.570365567528988e-06,
        -1.4281052650555459e-05,
        -8.924882879379759e-05,
        -0.0003569427177455564,
        -0.001427336256063394
       ],
       "kappa": -0.0014281847168633966
      },
      "t4": {
       "grid": [
        3.992922854578751e-05,
        9.987793137877787e-06,
        1.5985754207026304e-06,
        3.9968797649336807e-07,
        6.395431473293911e-08,
        0.0,
        6.395996976493734e-08,
        3.9977633781163036e-07,
        1.5992823094723718e-06,
        9.998838376379382e-06,
        4.0017593226249204e-05,
        0.00016024951313786673
       ],
       "kappa": 0.000159893047684377,
       "kappa_cc": 0.000159893047686394
      }
     },
     "E2_Hill": {
      "t2": {
       "S": 1.6266231256261696e-13,
       "S_cc": 1.6132521040103724e-13,
       "grid": [
        -0.00035977898386985174,
        -8.995485659324398e-05,
        -1.4393819487867887e-05,
        -3.5985447373043655e-06,
        -5.757759000690754e-07,
        0.0,
        -5.757876907486192e-07,
        -3.5987289647154697e-06,
        -1.4395293312707835e-05,
        -8.997788565123788e-05,
        -0.0003599632319449819,
        -0.001440311666697669
       ],
       "kappa": -0.0014394617694966992,
       "kappa3": -7.369324458207498e-07,
       "kappa3_cc": -7.369324104590622e-07,
       "kappa_cc": -0.0014394617695005832
      },
      "t4": {
       "S": -2.2136167800606602e-13,
       "S_cc": -2.1901880737433866e-13,
       "grid": [
        4.0075112154536185e-05,
        1.0021876255539297e-05,
        1.6038160919329414e-06,
        4.009811214178427e-07,
        6.415961073535925e-08,
        0.0,
        6.416315367907544e-08,
        4.0103648424327787e-07,
        1.6042590029741177e-06,
        1.0028797479577634e-05,
        4.013050311080235e-05,
        0.00016065650935481735
       ],
       "kappa": 0.00016040534614367987,
       "kappa3": 2.214826941714643e-07,
       "kappa3_cc": 2.2148264931772227e-07,
       "kappa_cc": 0.00016040534614166288
      }
     },
     "h_Hill": {
      "t2": {
       "S": 4.563941055176853e-15,
       "S_cc": 3.901387545207024e-15,
       "grid": [
        -4.97443568558964e-07,
        -1.249121053259472e-07,
        -2.0039163883822653e-08,
        -5.014240023193395e-09,
        -8.027059017479132e-10,
        0.0,
        -8.03276667404873e-10,
        -5.023157112482579e-09,
        -2.0110500931203035e-08,
        -1.260267620262212e-07,
        -5.063613528477617e-07,
        -2.043685221497782e-06
       ],
       "kappa": -2.0075101981637655e-06,
       "kappa_cc": -2.0075102000424232e-06
      },
      "t4": {
       "S": 7.665423084547844e-14,
       "S_cc": 7.604097370267146e-14,
       "grid": [
        -1.8659710554480569e-06,
        -4.678262344182116e-07,
        -7.498399878791417e-08,
        -1.875714272792095e-08,
        -3.0022188068912214e-09,
        0.0,
        -3.0036605425109997e-09,
        -1.8779669153090595e-08,
        -7.516421407505192e-08,
        -4.7064235364491225e-07,
        -1.8885071644270113e-06,
        -7.604051808440815e-06
       ],
       "kappa": -7.507739661972004e-06,
       "kappa_cc": -7.507739663239201e-06
      }
     }
    },
    "b1_Hill": 0.01624085410723511,
    "b1_Hill_cc": 0.01624085410722665,
    "branch": "hex",
    "kappa24_bi_cc": 3.006854025026466e-13,
    "kappa24_bi_chat": 9.483155002006545e-13,
    "quadform": {
     "basis_k12_chat": [
      -0.001439454440047776,
      1.6668029803601492e-12,
      0.0001604034438794772,
      -7.36951568936323e-07,
      -7.276386967011858e-06,
      -3.936928935774002e-06,
      2.214379693918294e-07,
      -1.199644627757171e-07,
      -1.268159318600241e-07,
      -3.6031722935636756e-07,
      -1.0829856288863797e-07,
      3.11374900994371e-08
     ],
     "basis_k7_chat": [
      -0.0014394693020032903,
      -1.2488790730491887e-08,
      0.00016039903763945317,
      -7.369515689363175e-07,
      -7.276386967011854e-06,
      -3.936928935774004e-06,
      2.214379693918309e-07
     ],
     "cubic_terms_cc": [
      -7.369515817719742e-07,
      -7.276386960723754e-06,
      -3.936928925279228e-06,
      2.2143796444095318e-07
     ],
     "grid5x5_cc": [
      -7.976009400101347e-05,
      -8.737740784903192e-05,
      -8.995485659313296e-05,
      -8.748962981364183e-05,
      -7.997872808929163e-05,
      -1.2409636205301666e-05,
      -1.9962433144171676e-05,
      -2.2490065633484768e-05,
      -1.9989874392223328e-05,
      -1.2459014352539377e-05,
      1.0021876255539297e-05,
      2.505878869740741e-06,
      2.220446049250313e-16,
      2.5067439404224956e-06,
      1.0028797479355589e-05,
      -1.2473478692598405e-05,
      -1.998057378083118e-05,
      -2.2492944204866028e-05,
      -2.0008244574820644e-05,
      -1.252395037854015e-05,
      -7.990431874749238e-05,
      -8.743059230065242e-05,
      -8.997788565145992e-05,
      -8.754401630450825e-05,
      -8.012662609491183e-05
     ],
     "kappa22_fit7": -0.0014394693020032903,
     "kappa22_fit7_cc": -0.0014394693020041397,
     "kappa24_fit7": -1.2488790730491887e-08,
     "kappa44_fit7": 0.00016039903763945317,
     "reading_cc": "hex two-parameter family"
    }
   },
   "hex_step|b": {
    "arms": {
     "E2_HSmean": {
      "t2": {
       "grid": [
        -0.0003569546896101672,
        -8.922641129294195e-05,
        -1.4275026188892426e-05,
        -3.5686556428826677e-06,
        -5.70975180358424e-07,
        0.0,
        -5.709621745397797e-07,
        -3.5684524321011324e-06,
        -1.4273400507525125e-05,
        -8.92010104921459e-05,
        -0.00035675149663971784,
        -0.0014265718105259673
       ],
       "kappa": -0.0014274194267221226
      },
      "t4": {
       "grid": [
        3.9931605506859924e-05,
        9.988388290027572e-06,
        1.5986707333492944e-06,
        3.9971181187148375e-07,
        6.395812945925172e-08,
        0.0,
        6.396378560147298e-08,
        3.9980018806673456e-07,
        1.599377740690855e-06,
        9.999435379270949e-06,
        4.001998499925108e-05,
        0.00016025911078099142
       ],
       "kappa": 0.00015990258492339606,
       "kappa_cc": 0.0001599025849219905
      }
     },
     "E2_Hill": {
      "t2": {
       "S": 1.6125034658616313e-13,
       "S_cc": 1.6400082932192235e-13,
       "grid": [
        -0.000359589205973343,
        -8.990741528092094e-05,
        -1.4386229051588373e-05,
        -3.5966471373383158e-06,
        -5.754722848250182e-07,
        0.0,
        -5.754840760596736e-07,
        -3.596831374630405e-06,
        -1.4387702956364379e-05,
        -8.993044558192054e-05,
        -0.00035977346397653154,
        -0.0014395524516434
       ],
       "kappa": -0.001438702718749083,
       "kappa3": -7.369721996574744e-07,
       "kappa3_cc": -7.369722507858468e-07,
       "kappa_cc": -0.0014387027187507326
      },
      "t4": {
       "S": -2.1990268388075987e-13,
       "S_cc": -2.2010851017752434e-13,
       "grid": [
        4.007742972289563e-05,
        1.0022457102243365e-05,
        1.6039091734754152e-06,
        4.010044041269367e-07,
        6.416333730996371e-08,
        0.0,
        6.416688203003673e-08,
        4.0105979270954606e-07,
        1.6043522874653604e-06,
        1.0029381496190481e-05,
        4.0132846051976756e-05,
        0.0001606659405379851
       ],
       "kappa": 0.00016041466503408588,
       "kappa3": 2.2158410762808975e-07,
       "kappa3_cc": 2.2158411841270297e-07,
       "kappa_cc": 0.00016041466503203565
      }
     },
     "h_Hill": {
      "t2": {
       "S": 6.550087858874976e-15,
       "S_cc": 8.137135505898113e-15,
       "grid": [
        -4.969233557972075e-07,
        -1.2478124211678931e-07,
        -2.0018147695033406e-08,
        -5.0089790093466036e-09,
        -8.018634645168277e-10,
        0.0,
        -8.024334530176702e-10,
        -5.017882886981795e-09,
        -2.0089378716114936e-08,
        -1.2589424946973793e-07,
        -5.058279419767331e-07,
        -2.041524180040888e-06
       ],
       "kappa": -2.0054031941127916e-06,
       "kappa_cc": -2.0054031944932263e-06
      },
      "t4": {
       "S": 7.485871681214715e-14,
       "S_cc": 7.34844721335253e-14,
       "grid": [
        -1.8662871319463648e-06,
        -4.679056785361624e-07,
        -7.499675247490956e-08,
        -1.8760334619116747e-08,
        -3.0027293984602466e-09,
        0.0,
        -3.004171911236142e-09,
        -1.878286859380296e-08,
        -7.517702727000142e-08,
        -4.70722723466821e-07,
        -1.8888306501096963e-06,
        -7.605363090079642e-06
       ],
       "kappa": -7.509018168894417e-06,
       "kappa_cc": -7.509018171302918e-06
      }
     }
    },
    "b1_Hill": 0.016241797577228063,
    "b1_Hill_cc": 0.016241797577238582,
    "branch": "hex",
    "kappa24_bi_cc": 1.8503717077085943e-13,
    "kappa24_bi_chat": 2.544261098099317e-13,
    "quadform": {
     "cubic_terms_cc": [
      -7.369912610454396e-07,
      -7.272454059151412e-06,
      -3.939847498398738e-06,
      2.215393441283962e-07
     ],
     "grid5x5_cc": [
      -7.971208679635744e-05,
      -8.732984004833355e-05,
      -8.990741528103197e-05,
      -8.7442000696214e-05,
      -7.993059542565906e-05,
      -1.2397187749924043e-05,
      -1.99504295744779e-05,
      -2.247820554202029e-05,
      -1.9977855104102993e-05,
      -1.2446531859500176e-05,
      1.002245710202132e-05,
      2.506024271653473e-06,
      2.220446049250313e-16,
      2.5068897382407584e-06,
      1.0029381496190481e-05,
      -1.2461075853509307e-05,
      -1.9968581805862584e-05,
      -2.2481084268943796e-05,
      -1.999623680537521e-05,
      -1.2511513793445062e-05,
      -7.985640459950982e-05,
      -8.738304907141003e-05,
      -8.993044558192054e-05,
      -8.749641069916159e-05,
      -8.007858526049016e-05
     ],
     "kappa22_fit7": -0.001438710247883606,
     "kappa22_fit7_cc": -0.0014387102478831734,
     "kappa24_fit7": -1.2484615083901236e-08,
     "kappa44_fit7": 0.00016040835823465525,
     "reading_cc": "hex two-parameter family"
    }
   }
  },
  "regime": {
   "d_EM": 3.7641664288e-33
  }
 },
 "rms_exact_check": {
  "K4_mean": "0",
  "K4_sq": "4/21",
  "P2_sq": "1/5",
  "P4_sq": "1/9"
 },
 "sources": {
  "CI1": {
   "bytes": 45760,
   "md5": "845ae6beb1b90fe34c540f843ffdb9f5",
   "path": "gci1_gate/ci1_phase3_cc_r2.json"
  },
  "DK24": {
   "bytes": 1917,
   "md5": "b7952dfcaddcd1d98e424aee8ce5231f",
   "path": "gmscs2_gate/diag_kappa24.json"
  },
  "DQF": {
   "bytes": 1119,
   "md5": "d84aa1fdce7dea1b1a5d24dfb8f13c18",
   "path": "gmscs2_gate/diag_quadform_basis.json"
  },
  "G1cc": {
   "bytes": 24415,
   "md5": "249e11dd53c4cb82f302b15d3c94c337",
   "path": "gmscs1_gate/g_mscs1_ccleg_checkpoint.json"
  },
  "G1chat": {
   "bytes": 33289,
   "md5": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "path": "gmscs1_gate/g_mscs1_chatleg_checkpoint.json"
  },
  "G2cc": {
   "bytes": 68540,
   "md5": "9961745d1e1857cfab6445d4754b5060",
   "path": "gmscs2_gate/g_mscs2_ccleg_checkpoint.json"
  },
  "G2chat": {
   "bytes": 31575,
   "md5": "1c5b6b59829d2a6b9ae2b1a7a016832d",
   "path": "gmscs2_gate/g_mscs2_chatleg_checkpoint.json"
  }
 },
 "structure": {
  "arms": [
   "E2_Hill",
   "E2_HSmean",
   "h_Hill"
  ],
  "cubic_keys": [
   "cubic_step|001",
   "cubic_step|111",
   "cubic_gem8|001",
   "cubic_gem8|111"
  ],
  "hex_keys": [
   "hex_step|a",
   "hex_step|b",
   "hex_gem8|a",
   "hex_gem8|b"
  ],
  "keys": [
   "hex_step|a",
   "hex_step|b",
   "hex_gem8|a",
   "hex_gem8|b",
   "cubic_step|001",
   "cubic_step|111",
   "cubic_gem8|001",
   "cubic_gem8|111"
  ],
  "kill_test_set": "every key x every arm (E-SA-9(a)); the primary-only union is serialized for information",
  "mapped_families": {
   "cubic": [
    "t4"
   ],
   "hex": [
    "t4",
    "t2"
   ]
  },
  "null_families": {
   "cubic": [
    "t2"
   ]
  },
  "primary": {
   "arm": "E2_Hill",
   "keys": [
    "hex_step|a",
    "hex_gem8|a",
    "cubic_step|001",
    "cubic_gem8|001"
   ]
  },
  "robustness": {
   "arms": [
    "E2_HSmean",
    "h_Hill"
   ],
   "keys": [
    "hex_step|b",
    "hex_gem8|b",
    "cubic_step|111",
    "cubic_gem8|111"
   ]
  }
 },
 "tokens": {
  "class": [
   "spd"
  ],
  "delta_def": "tensor_over_EM_minus_1",
  "geom": [
   "single",
   "population"
  ],
  "odf_reading": [
   "none",
   "uniform",
   "hexP2",
   "hexP4",
   "hexP2P4",
   "cubK4",
   "cubP2-i",
   "cubP2-ii",
   "cubP2K4-i",
   "cubP2K4-ii"
  ],
  "q": [
   "phase",
   "group"
  ],
  "reading_conformant": [
   "bound"
  ],
  "reading_frozen_list": [
   "bound",
   "ceiling",
   "margin",
   "criterion"
  ]
 }
}

=====END-EMBED name=pinned_inputs_G_MSCS_A.json=====

=====BEGIN-EMBED name=sa_build_pinned_inputs.py md5=8189100ede80eac360b25a146e580abf bytes=41342 encoding=raw=====
#!/usr/bin/env python3
"""sa_build_pinned_inputs.py -- G-MSCS-A (staging memo v2, sections 3.1 and 9): builds the pinned-inputs file of record,
pinned_inputs_G_MSCS_A.json, from the seven banked sources on `main`, BY NAMED KEY (RFC 6901 JSON pointers, recorded in
the file's `provenance` block), with full-md5 and byte-count guards on every source.

Deterministic by construction: standard library only; every value is either copied from a source (JSON float parse,
exact round trip) or derived with +, -, *, / and sqrt (IEEE-754 correctly rounded); no transcendental function, no
numpy, no clock, no path, no host name in the output; sorted keys; a trailing LF. The same sources give the same bytes
on any platform with IEEE-754 doubles and Python >= 3.6.

No anchor value, no observational number is read or written. The only SI value is the W^EM_U near-component edge (the
ledger's regime scale of record, V4.77), read by key from the G-CI1 CC r2 checkpoint and cross-checked against the
ledger literal.

Usage:  python3 sa_build_pinned_inputs.py REPO_DIR [OUT_FILE]
        REPO_DIR  a clone of gifgaf0/gifgaf0.github.io at a commit whose seven source files carry the md5s below
                  (any commit at or after e1fa071 in which they are unchanged); the repository is only read.
        OUT_FILE  default ./pinned_inputs_G_MSCS_A.json (an existing file is overwritten)
Exit:   0 built and self-verified; 1 a guard failed (no output file is left behind); 2 usage error.

The file has two parts: `raw` (copied values; each field's source and pointer template in `provenance`) and `derived`
(reference values; a pure function of `raw`, `constants` and `grids`). Before exiting, the builder re-reads the written
file, re-derives `derived` from the file alone and requires bit identity, and re-reads every `raw` value from its
source by pointer and requires bit identity. The legs repeat both checks with their own code (F-CTRL-SA-PIN and
F-CTRL-SA-PIN-DERIVED). Point counts are printed from the generators and never written (rule 4)."""
import hashlib, json, math, os, sys
from fractions import Fraction

GATE = 'G-MSCS-A'
FILE_SCHEMA = 'g_mscs_a_pinned_inputs/1'
OUT_DEFAULT = 'pinned_inputs_G_MSCS_A.json'

SOURCES = {  # alias: (repository path, md5 of record, bytes of record)
    'G2chat': ('gmscs2_gate/g_mscs2_chatleg_checkpoint.json', '1c5b6b59829d2a6b9ae2b1a7a016832d', 31575),
    'G2cc':   ('gmscs2_gate/g_mscs2_ccleg_checkpoint.json',   '9961745d1e1857cfab6445d4754b5060', 68540),
    'G1chat': ('gmscs1_gate/g_mscs1_chatleg_checkpoint.json', 'c04c0b8ea34cfe60f231aa06828e6ce4', 33289),
    'G1cc':   ('gmscs1_gate/g_mscs1_ccleg_checkpoint.json',   '249e11dd53c4cb82f302b15d3c94c337', 24415),
    'DK24':   ('gmscs2_gate/diag_kappa24.json',               'b7952dfcaddcd1d98e424aee8ce5231f', 1917),
    'DQF':    ('gmscs2_gate/diag_quadform_basis.json',        'd84aa1fdce7dea1b1a5d24dfb8f13c18', 1119),
    'CI1':    ('gci1_gate/ci1_phase3_cc_r2.json',             '845ae6beb1b90fe34c540f843ffdb9f5', 45760),
}
KEYS = ['hex_step|a', 'hex_step|b', 'hex_gem8|a', 'hex_gem8|b',
        'cubic_step|001', 'cubic_step|111', 'cubic_gem8|001', 'cubic_gem8|111']
HEX = KEYS[:4]
CUBIC = KEYS[4:]
ARMS = ['E2_Hill', 'E2_HSmean', 'h_Hill']
PRIMARY = {'arm': 'E2_Hill', 'keys': ['hex_step|a', 'hex_gem8|a', 'cubic_step|001', 'cubic_gem8|001']}
LEDGER_WEM_EDGE = 3.7641664288e-33   # the V4.77 ledger literal; a cross-check only -- the pinned value is read by key

# raw fields: (destination path under keys/<K>/, source alias, JSON pointer template, scope)
# scope: 'all' = every key; 'cubic' = cubic keys only; 'dqf' = the keys the chat quadform-basis diagnostic banks
FIELDS = [
    ('arms/E2_Hill/t4/kappa',      'G2chat', '/phase2/{K}/kappa44_E2', 'all'),
    ('arms/E2_Hill/t4/kappa_cc',   'G2cc',   '/phase2/{K}/kappa44_E2', 'all'),
    ('arms/E2_Hill/t4/S',          'G2chat', '/phase2/{K}/S4_E2', 'all'),
    ('arms/E2_Hill/t4/kappa3',     'G2chat', '/phase2/{K}/kappa444_E2', 'all'),
    ('arms/E2_Hill/t4/grid',       'G2chat', '/phase2/{K}/r_agg_E2_VRH', 'all'),
    ('arms/E2_HSmean/t4/kappa',    'G2chat', '/phase2/{K}/kappa44_E2_HS', 'all'),
    ('arms/E2_HSmean/t4/kappa_cc', 'G2cc',   '/phase2/{K}/kappa44_E2_HS', 'all'),
    ('arms/E2_HSmean/t4/grid',     'G2chat', '/phase2/{K}/r_agg_E2_HS', 'all'),
    ('arms/h_Hill/t4/kappa',       'G2chat', '/phase2/{K}/kappa44_h', 'all'),
    ('arms/h_Hill/t4/kappa_cc',    'G2cc',   '/phase2/{K}/kappa44_h', 'all'),
    ('arms/h_Hill/t4/S',           'G2chat', '/phase2/{K}/S4_h', 'all'),
    ('arms/h_Hill/t4/grid',        'G2chat', '/phase2/{K}/r_agg_h_VRH', 'all'),
    # the l = 2 family (G-MSCS1): mapped on hex keys; the null family on cubic keys (null N-3)
    ('arms/E2_Hill/t2/kappa',      'G1chat', '/phase2/{K}/kappa2_E2', 'all'),
    ('arms/E2_Hill/t2/kappa_cc',   'G1cc',   '/phase2/{K}/kappa2_E2', 'all'),
    ('arms/E2_Hill/t2/S',          'G1chat', '/phase2/{K}/S_t_E2', 'all'),
    ('arms/E2_Hill/t2/kappa3',     'G1chat', '/phase2/{K}/kappa3_E2', 'all'),
    ('arms/E2_Hill/t2/grid',       'G1chat', '/phase2/{K}/r_agg_E2_VRH', 'all'),
    ('arms/E2_HSmean/t2/kappa',    'G1chat', '/phase2/{K}/kappa2_E2_HS', 'all'),
    ('arms/E2_HSmean/t2/grid',     'G1chat', '/phase2/{K}/r_agg_E2_HS', 'all'),
    ('arms/h_Hill/t2/kappa',       'G1chat', '/phase2/{K}/kappa2_h', 'all'),
    ('arms/h_Hill/t2/kappa_cc',    'G1cc',   '/phase2/{K}/kappa2_h', 'all'),
    ('arms/h_Hill/t2/S',           'G1chat', '/phase2/{K}/S_t_h', 'all'),
    ('arms/h_Hill/t2/grid',        'G1chat', '/phase2/{K}/r_agg_h_VRH', 'all'),
    # the CC counterparts of every other coefficient the mapper uses (F-CTRL-SA-PIN covers each; v2 audit 13(c))
    ('arms/E2_Hill/t4/S_cc',       'G2cc',   '/phase2/{K}/S4_E2', 'all'),
    ('arms/E2_Hill/t4/kappa3_cc',  'G2cc',   '/phase2/{K}/kappa444_E2', 'all'),
    ('arms/h_Hill/t4/S_cc',        'G2cc',   '/phase2/{K}/S4_h', 'all'),
    ('arms/E2_Hill/t2/S_cc',       'G1cc',   '/phase2/{K}/S_t_E2', 'all'),
    ('arms/E2_Hill/t2/kappa3_cc',  'G1cc',   '/phase2/{K}/kappa3_E2', 'all'),
    ('arms/h_Hill/t2/S_cc',        'G1cc',   '/phase2/{K}/S_t_h', 'all'),
    # the (t2, t4) quadratic form, S2-E2 Hill arm (reading (i) on cubic keys: A-3.3)
    ('quadform/kappa22_fit7',      'G2chat', '/phase2/{K}/quadform/kappa22', 'all'),
    ('quadform/kappa22_fit7_cc',   'G2cc',   '/phase2/{K}/quadform/kappa22', 'all'),
    ('quadform/kappa24_fit7',      'G2chat', '/phase2/{K}/quadform/kappa24', 'all'),
    ('quadform/kappa44_fit7',      'G2chat', '/phase2/{K}/quadform/kappa44', 'all'),
    ('quadform/grid5x5_cc',        'G2cc',   '/phase2/{K}/quadform/x_grid_r_agg_E2_VRH', 'all'),
    ('quadform/cubic_terms_cc',    'G2cc',   '/phase2/{K}/quadform/x_cubic_terms_discarded', 'all'),
    ('quadform/reading_cc',        'G2cc',   '/phase2/{K}/quadform/x_reading', 'all'),
    ('quadform/basis_k7_chat',     'DQF',    '/{K}/k7', 'dqf'),
    ('quadform/basis_k12_chat',    'DQF',    '/{K}/k12', 'dqf'),
    ('kappa24_bi_chat',            'DK24',   '/{K}/kappa24_richardson', 'all'),
    ('kappa24_bi_cc',              'G2cc',   '/phase2/{K}/kappa24_richardson', 'all'),
    ('b1_Hill',                    'G2chat', '/phase2/{K}/biref_b1_VRH', 'all'),
    ('b1_Hill_cc',                 'G2cc',   '/phase2/{K}/biref_b1_VRH', 'all'),
    ('pure_l2_change_t1',          'DK24',   '/{K}/pure_l2_r_agg_change_t1', 'cubic'),
    ('A31_mixed_change_cc',        'G2cc',   '/extras/A3_diagnostics/A-3.1_mixed_r_agg_change_A29/{K}', 'cubic'),
]
GLOBAL_FIELDS = [  # (destination, alias, pointer)
    ('grids/t_grid',     'G2chat', '/t4_grid'),
    ('grids/t2t4_axis',  'G2chat', '/t2t4_grid'),
    ('regime/d_EM',      'CI1',    '/per_oom/x1/W_EM_union/0/1'),
]
CUBIC_TERM_ORDER = ['t2^3', 't2^2*t4', 't2*t4^2', 't4^3']            # the CC checkpoint's discarded-term order (A-2.9)
DQF_BASIS = ['t2^2', 't2*t4', 't4^2', 't2^3', 't2^2*t4', 't2*t4^2', 't4^3', 't2^4', 't2^3*t4', 't2^2*t4^2', 't2*t4^3', 't4^4']

CONSTANTS = {
    'D': 0.25,                        # E-SA-10(a): the fit window |t| <= 0.25 per family (D-12)
    'mu': 0.10,                       # E-SA-11(a): reach widening (D-22)
    'KD_CLIP': 0.3,                   # E-SA-4(a): long-wavelength envelope (D-21)
    'tau_agg': 1e-6,                  # rule 2: first-order slope tolerance (D-14)
    'kappa_floor': 1e-6,              # rule 2: coefficient-null tolerance (D-14)
    'zero_snap': 1e-12,               # S-SA-9: hull endpoints within this of zero are set to 0
    'trunc_threshold': 0.10,          # TRUNCATION-SENSITIVE (D-22)
    'nullfloor_threshold': 0.10,      # NULL-FLOOR-SENSITIVE (section 3.3)
    'recon_tol_abs_E2_Hill': 1e-8,    # F-CTRL-SA-RECON, S2-E2 Hill arm
    'recon_tol_rel_robust': 1e-3,     # F-CTRL-SA-RECON, robustness arms (kappa of record vs basis-independent)
    'pin_twoleg_tol_rel': 1e-4,       # F-CTRL-SA-PIN, chat vs CC banked coefficients
    'zero_ctrl_tol_abs': 1e-12,       # F-CTRL-SA-ZERO
    'l2null_t1_tol_abs': 1e-12,       # F-CTRL-SA-L2NULL (r_agg unchanged by t2 alone at t2 = 1)
    'edge_twoleg_tol_rel': 1e-10,     # section 6.4
    'mono_tol_rel': 1e-14,            # F-CTRL-SA-MONO
    'pin_derived_tol_rel': 1e-12,     # F-CTRL-SA-PIN-DERIVED: |leg - pinned| <= tol_rel*|pinned| + tol_abs
    'pin_derived_tol_abs': 1e-16,
    'oom_factors': [0.1, 1.0, 10.0],  # section 3.8
    'synthetic_t': [0.01, 0.1, 0.5],  # Phase 2 synthetic budgets b = |kappa| * t_syn^2 (C-SYN-1..5, 7..11, 14)
    'synthetic_t_tight': 1e-9,        # C-SYN-12: a budget tight enough that the NULL-FLOOR flag is exercised
    'synthetic_band_fractions': [0.25, 0.75],   # C-SYN-3 (robustness-only) and C-SYN-13 (MARGIN) interval rule
    'synthetic_k': {'silent': 1.0, 'void': 1e33},   # m^-1: every suite uses 'silent' for k_em_max and k_t_max; C-SYN-10 uses 'void'
    'synthetic_rules': {
        'margin_positive': '[h + f1*(w - h), h + f2*(w - h)], h = unions.hull_all[1], w = unions.widened_all[1]',
        'margin_negative': '[w + f1*(h - w), w + f2*(h - w)], w = unions.widened_all[0], h = unions.hull_all[0]',
        'robustness_only_positive': '[p + f1*(q - p), p + f2*(q - p)], p = unions.widened_primary[1], q = unions.hull_all[1]'},
    'rms': {'hexP2': math.sqrt(1 / 5), 'hexP4': 1 / 3, 'cubK4': math.sqrt(4 / 21)},
    'rms_closed_form': {'hexP2': 'sqrt(1/5)', 'hexP4': '1/3', 'cubK4': 'sqrt(4/21)'},
    'fam_rms': {'t2': 'hexP2', 't4_hex': 'hexP4', 't4_cubic': 'cubK4'},
}
GRIDS_FIXED = {
    'fit_window': 'abs(t) <= D, inclusive (the window both banked legs used; H-CC-1)',
    'richardson_pairs': {'one_param': [0.05, 0.1], 'two_param': [0.125, 0.25]},
    'richardson_formulas': {
        'odd':   '[4*O(h1) - O(h2)]/3, O(h) = [r(h) - r(-h)]/(2h)',
        'even':  '[4*E(h1) - E(h2)]/3, E(h) = [r(h) + r(-h) - 2*r(0)]/(2h^2)',
        'mixed': '[4*M(h1) - M(h2)]/3, M(h) = [R(h,h) - R(h,-h) - R(-h,h) + R(-h,-h)]/(4h^2)'},
    'grid5x5_layout': 'row-major, t2 outer, t4 inner: index = 5*i + j for (t2_axis[i], t4_axis[j])',
    'area_grid': {'lo': -0.25, 'hi': 0.25, 'nodes_per_axis': 201, 'node': 'lo + i*(hi - lo)/(nodes_per_axis - 1)'},
}
TOKENS = {
    'odf_reading': ['none', 'uniform', 'hexP2', 'hexP4', 'hexP2P4', 'cubK4', 'cubP2-i', 'cubP2-ii', 'cubP2K4-i', 'cubP2K4-ii'],
    'delta_def': 'tensor_over_EM_minus_1',
    'class': ['spd'],
    'reading_conformant': ['bound'],
    'reading_frozen_list': ['bound', 'ceiling', 'margin', 'criterion'],
    'geom': ['single', 'population'],
    'q': ['phase', 'group'],
}
STRUCTURE = {
    'keys': KEYS, 'hex_keys': HEX, 'cubic_keys': CUBIC, 'arms': ARMS, 'primary': PRIMARY,
    'robustness': {'arms': ['E2_HSmean', 'h_Hill'], 'keys': ['hex_step|b', 'hex_gem8|b', 'cubic_step|111', 'cubic_gem8|111']},
    'mapped_families': {'hex': ['t4', 't2'], 'cubic': ['t4']},
    'null_families': {'cubic': ['t2']},
    'kill_test_set': 'every key x every arm (E-SA-9(a)); the primary-only union is serialized for information',
}
ELECTIONS = {'E-SA-0': 'a', 'E-SA-1': 'a', 'E-SA-2': 'a', 'E-SA-3': 'a', 'E-SA-4': 'a', 'E-SA-5': 'a',
             'E-SA-6': 'a', 'E-SA-7': 'base 05302210 + the G-MSCS1 stratum', 'E-SA-8': 'a', 'E-SA-9': 'a',
             'E-SA-10': 'a', 'E-SA-11': 'a'}


class GuardError(Exception):
    pass


def guard(cond, msg):
    if not cond:
        raise GuardError(msg)


def ptr_get(doc, pointer):
    """RFC 6901 dereference (the '~1' and '~0' escapes honoured)."""
    guard(pointer.startswith('/'), 'bad pointer ' + pointer)
    cur = doc
    for tok in pointer[1:].split('/'):
        tok = tok.replace('~1', '/').replace('~0', '~')
        if isinstance(cur, list):
            guard(tok.isdigit() and int(tok) < len(cur), 'pointer index out of range: ' + pointer)
            cur = cur[int(tok)]
        else:
            guard(isinstance(cur, dict) and tok in cur, 'pointer key missing: ' + pointer)
            cur = cur[tok]
    return cur


def is_float_leaf(v):
    if isinstance(v, bool):
        return False
    if isinstance(v, float):
        return math.isfinite(v)
    if isinstance(v, list):
        return len(v) > 0 and all(is_float_leaf(x) for x in v)
    return False


def set_path(d, path, value):
    parts = path.split('/')
    for p in parts[:-1]:
        d = d.setdefault(p, {})
    guard(parts[-1] not in d, 'duplicate destination ' + path)
    d[parts[-1]] = value


def load_sources(repo):
    docs, meta = {}, {}
    for alias, (path, md5, nbytes) in SOURCES.items():
        full = os.path.join(repo, path)
        guard(os.path.isfile(full), 'source missing: ' + path)
        b = open(full, 'rb').read()
        h = hashlib.md5(b).hexdigest()
        guard(h == md5 and len(b) == nbytes, 'source md5/bytes mismatch: %s (got %s, %d B)' % (path, h, len(b)))
        docs[alias] = json.loads(b.decode('utf-8'))
        meta[alias] = {'path': path, 'md5': md5, 'bytes': nbytes}
    return docs, meta


def scope_keys(scope, docs):
    if scope == 'all':
        return KEYS
    if scope == 'cubic':
        return CUBIC
    if scope == 'dqf':
        return [k for k in KEYS if k in docs['DQF']]
    raise GuardError('unknown scope ' + scope)


def build_raw(docs):
    guard(list(docs['G2chat']['phase2'].keys()) == KEYS, 'G-MSCS2 chat key set/order differs from the pinned key list')
    for alias in ('G2cc', 'G1chat', 'G1cc', 'DK24'):
        src = docs[alias]['phase2'] if 'phase2' in docs[alias] else docs[alias]
        guard(sorted(src.keys()) == sorted(KEYS), 'key set differs in ' + alias)
    raw = {'keys': {}}
    for k in KEYS:
        raw['keys'][k] = {'branch': 'hex' if k in HEX else 'cubic'}
    for dest, alias, ptmpl, scope in FIELDS:
        for k in scope_keys(scope, docs):
            v = ptr_get(docs[alias], ptmpl.format(K=k))
            if dest == 'quadform/reading_cc':
                guard(isinstance(v, str), 'reading is not a string')
            else:
                guard(is_float_leaf(v), 'non-float or non-finite value at %s:%s' % (alias, ptmpl.format(K=k)))
            set_path(raw['keys'][k], dest, v)
    glob = {}
    for dest, alias, p in GLOBAL_FIELDS:
        v = ptr_get(docs[alias], p)
        guard(is_float_leaf(v), 'non-float global at ' + p)
        set_path(glob, dest, v)
    # structural assertions on the global values
    guard(ptr_get(docs['G1chat'], '/t_grid') == glob['grids']['t_grid'], 'the G-MSCS1 t grid differs from the G-MSCS2 t4 grid')
    wem = ptr_get(docs['CI1'], '/per_oom/x1/W_EM_union')
    guard(len(wem) == 1 and wem[0][0] == 0.0, 'W^EM_U near component is not a single floor-adjoining interval')
    guard(glob['regime']['d_EM'] == LEDGER_WEM_EDGE, 'W^EM_U edge differs from the V4.77 ledger literal')
    for arr in (glob['grids']['t_grid'],):
        for h in GRIDS_FIXED['richardson_pairs']['one_param'] + [0.0]:
            guard(h in arr and -h in arr, 'one-parameter Richardson step missing from the t grid')
    for h in GRIDS_FIXED['richardson_pairs']['two_param'] + [0.0]:
        guard(h in glob['grids']['t2t4_axis'] and -h in glob['grids']['t2t4_axis'], 'two-parameter step missing')
    for k in KEYS:
        q = raw['keys'][k]['quadform']
        guard(len(q['grid5x5_cc']) == len(glob['grids']['t2t4_axis']) ** 2, '5x5 grid length')
        guard(len(q['cubic_terms_cc']) == len(CUBIC_TERM_ORDER), 'cubic-term list length')
        for arm in ARMS:
            for fam in ('t4', 't2'):
                guard(len(raw['keys'][k]['arms'][arm][fam]['grid']) == len(glob['grids']['t_grid']), 'grid length')
    for k in raw['keys']:
        q = raw['keys'][k]['quadform']
        if 'basis_k12_chat' in q:
            guard(len(q['basis_k12_chat']) == len(DQF_BASIS) and len(q['basis_k7_chat']) == 7, 'k7/k12 length')
            guard([q['basis_k7_chat'][i] for i in range(3)] == [q['kappa22_fit7'], q['kappa24_fit7'], q['kappa44_fit7']],
                  'the diagnostic k7[0..2] do not reproduce the fit7 kappa22, kappa24, kappa44 (basis order unconfirmed)')
            for i, c in zip(range(3, 7), q['cubic_terms_cc']):
                a = q['basis_k7_chat'][i]
                guard(abs(a - c) <= 1e-4 * max(abs(a), abs(c)) + 1e-12,
                      'the diagnostic k7[3..6] do not match the CC named cubic terms (basis order unconfirmed)')
                b = q['basis_k12_chat'][i]
                guard(abs(a - b) <= 1e-8 * max(abs(a), abs(b)) + 1e-15,
                      'the diagnostic k12[3..6] do not match k7[3..6] (shared order unconfirmed)')
    return raw, glob


# ---------------------------------------------------------------- derived: a pure function of (raw, constants, grids)
def derive(raw, constants, grids):
    D, MU, SNAP = constants['D'], constants['mu'], constants['zero_snap']
    tg, ax = grids['t_grid'], grids['t2t4_axis']
    h1, h2 = grids['richardson_pairs']['one_param']
    g1, g2 = grids['richardson_pairs']['two_param']
    ind = [i for i, t in enumerate(tg) if abs(t) <= D]

    def at(arr, t):
        return arr[tg.index(t)]

    def rich_odd(arr):
        O = lambda h: (at(arr, h) - at(arr, -h)) / (2 * h)
        return (4 * O(h1) - O(h2)) / 3

    def rich_even(arr):
        E = lambda h: (at(arr, h) + at(arr, -h) - 2 * at(arr, 0.0)) / (2 * h * h)
        return (4 * E(h1) - E(h2)) / 3

    def grid5(arr):
        n = len(ax)
        return {(ax[i], ax[j]): arr[n * i + j] for i in range(n) for j in range(n)}

    def e22(R, h):
        return (R[(h, 0.0)] + R[(-h, 0.0)] - 2 * R[(0.0, 0.0)]) / (2 * h * h)

    def e44(R, h):
        return (R[(0.0, h)] + R[(0.0, -h)] - 2 * R[(0.0, 0.0)]) / (2 * h * h)

    def m24(R, h):
        return (R[(h, h)] - R[(h, -h)] - R[(-h, h)] + R[(-h, -h)]) / (4 * h * h)

    def rich2(f, R):
        return (4 * f(R, g1) - f(R, g2)) / 3

    def rel(a, b):
        return abs(a - b) / max(abs(a), abs(b))

    def snap(x):
        return 0.0 if abs(x) < SNAP else x

    def tok(k, fam):
        if fam == 't2':
            return 'hexP2' if k in HEX else 'cubP2-i'
        return 'hexP4' if k in HEX else 'cubK4'

    out = {'families': {}, 'reach': {}, 'unions': {}, 'nulls': {'N-1': {}, 'N-2': {}, 'N-3': {}, 'N-4': {}},
           'hex_quadform': {}, 'zero_ctrl': {}, 'summary': {}}
    for k in KEYS:
        rk = raw['keys'][k]
        out['families'][k], out['reach'][k], out['zero_ctrl'][k] = {}, {}, {}
        mapped = ['t4', 't2'] if k in HEX else ['t4']
        for arm in ARMS:
            out['families'][k][arm] = {}
            for fam in ('t4', 't2'):
                f = rk['arms'][arm][fam]
                kb = rich_even(f['grid'])
                e = {'odf_reading': tok(k, fam), 'kappa': f['kappa'], 'kappa_bi': kb,
                     'fit_res_rel': (abs(f['kappa'] - kb) / abs(kb)) if abs(kb) > constants['kappa_floor'] else None,
                     'S_bi': rich_odd(f['grid']), 'S_fit': f.get('S'), 'r0': at(f['grid'], 0.0),
                     'mapped': fam in mapped}
                if 'kappa3' in f and fam in mapped:
                    e['recon_max_abs'] = max(abs(f['grid'][i] - (f['S'] * tg[i] + f['kappa'] * tg[i] * tg[i]
                                                                  + f['kappa3'] * tg[i] * tg[i] * tg[i])) for i in ind)
                    e['trunc_T_at_D'] = abs(f['kappa3']) * D / abs(f['kappa'])
                if 'kappa_cc' in f:
                    e['twoleg_rel'] = rel(f['kappa'], f['kappa_cc']) if (abs(f['kappa']) > constants['kappa_floor'] or abs(f['kappa_cc']) > constants['kappa_floor']) else None
                if 'kappa3_cc' in f:
                    e['twoleg_kappa3_rel'] = rel(f['kappa3'], f['kappa3_cc']) if fam in mapped else None
                if 'S_cc' in f:
                    e['twoleg_S_abs'] = abs(f['S'] - f['S_cc'])
                out['families'][k][arm][fam] = e
                out['zero_ctrl'][k]['%s/%s' % (arm, fam)] = {'odf_reading': 'uniform', 'r0': e['r0']}
                if fam in mapped:
                    out['nulls']['N-1']['%s/%s/%s' % (k, arm, fam)] = {'odf_reading': tok(k, fam), 'fit': f.get('S'),
                                                                       'bi': e['S_bi']}
            # reach: hull of the second-order box and every banked grid value inside D, then widened by (1 + mu)
            ks = [rk['arms'][arm][fam]['kappa'] for fam in mapped]
            box_lo, box_hi = 0.0, 0.0
            for x in ks:
                box_lo += min(0.0, x * D * D)
                box_hi += max(0.0, x * D * D)
            vals = [rk['arms'][arm][fam]['grid'][i] for fam in mapped for i in ind]
            if arm == 'E2_Hill':
                vals = vals + list(rk['quadform']['grid5x5_cc'])
            hull = [snap(min(box_lo, min(vals))), snap(max(box_hi, max(vals)))]
            out['reach'][k][arm] = {'box': [box_lo, box_hi], 'grid_min': min(vals), 'grid_max': max(vals), 'hull': hull,
                                    'widened': [hull[0] * (1 + MU), hull[1] * (1 + MU)],
                                    'grid_exceeds_box': (min(vals) < box_lo) or (max(vals) > box_hi)}
        # nulls N-2 (kappa24, every key), N-3 and N-4 (cubic)
        R = grid5(rk['quadform']['grid5x5_cc'])
        out['nulls']['N-2'][k] = {'odf_reading': 'hexP2P4' if k in HEX else 'cubP2K4-i',
                                  'fit7': rk['quadform']['kappa24_fit7'], 'bi_chat': rk['kappa24_bi_chat'],
                                  'bi_cc': rk['kappa24_bi_cc'], 'bi_5x5': rich2(m24, R)}
        if k in CUBIC:
            f2 = rk['arms']['E2_Hill']['t2']
            out['nulls']['N-3'][k] = {'odf_reading': 'cubP2-i', 'fit': f2['kappa'], 'bi': rich_even(f2['grid']),
                                      'pure_l2_change_t1': rk['pure_l2_change_t1']}
            q = rk['quadform']
            out['nulls']['N-4'][k] = {'odf_reading': 'cubP2K4-i', 'fit7': q['kappa22_fit7'], 'bi_5x5': rich2(e22, R),
                                      'k12_chat_t2sq': q['basis_k12_chat'][0] if 'basis_k12_chat' in q else None}
        else:
            a = rk['arms']
            hq = {'k22_bi_5x5': rich2(e22, R), 'k44_bi_5x5': rich2(e44, R), 'k24_bi_5x5': rich2(m24, R)}
            hq['null_ray_slope'] = {
                'E2_Hill_bi5x5': math.sqrt(-hq['k22_bi_5x5'] / hq['k44_bi_5x5']),
                'E2_Hill_bi': math.sqrt(-rich_even(a['E2_Hill']['t2']['grid']) / rich_even(a['E2_Hill']['t4']['grid'])),
                'E2_Hill_fit': math.sqrt(-a['E2_Hill']['t2']['kappa'] / a['E2_Hill']['t4']['kappa']),
                'E2_HSmean_bi': math.sqrt(-rich_even(a['E2_HSmean']['t2']['grid']) / rich_even(a['E2_HSmean']['t4']['grid'])),
                'E2_HSmean_fit': math.sqrt(-a['E2_HSmean']['t2']['kappa'] / a['E2_HSmean']['t4']['kappa'])}
            hq['h_Hill_form'] = ('negative-definite' if (a['h_Hill']['t2']['kappa'] < 0 and a['h_Hill']['t4']['kappa'] < 0)
                                 else 'not negative-definite')
            hq['kappa22_fit7_vs_kappa2_rel'] = rel(rk['quadform']['kappa22_fit7'], a['E2_Hill']['t2']['kappa'])
            out['hex_quadform'][k] = hq
    # unions
    def union(sel, which):
        items = [out['reach'][k][arm][which] for k in KEYS for arm in ARMS if sel(k, arm)]
        return [min(x[0] for x in items), max(x[1] for x in items)]
    prim = lambda k, arm: arm == PRIMARY['arm'] and k in PRIMARY['keys']
    every = lambda k, arm: True
    out['unions'] = {'widened_all': union(every, 'widened'), 'widened_primary': union(prim, 'widened'),
                     'hull_all': union(every, 'hull'), 'hull_primary': union(prim, 'hull')}
    f1, f2 = constants['synthetic_band_fractions']
    u = out['unions']
    def band(lo_end, hi_end):
        return [lo_end + f1 * (hi_end - lo_end), lo_end + f2 * (hi_end - lo_end)]
    out['synthetic'] = {'margin_positive': band(u['hull_all'][1], u['widened_all'][1]),
                        'margin_negative': band(u['widened_all'][0], u['hull_all'][0]),
                        'robustness_only_positive': band(u['widened_primary'][1], u['hull_all'][1])}
    # summary constants quoted by the memo (nothing hand-computed)
    b1r = {k: abs(raw['keys'][k]['b1_Hill'] / raw['keys'][k]['arms']['E2_Hill']['t4']['kappa']) for k in KEYS}
    fams = [(k, arm, fam) for k in KEYS for arm in ARMS for fam in ('t4', 't2')]
    s = out['summary']
    s['b1_over_kappa44'] = b1r
    s['b1_dominance_at_D_min'] = min(b1r.values()) / D
    s['k_fire_WEM'] = constants['KD_CLIP'] / raw['regime']['d_EM']
    s['trunc_T_at_D_max'] = max(out['families'][k]['E2_Hill'][f]['trunc_T_at_D'] for k in KEYS for f in ('t4', 't2')
                                if 'trunc_T_at_D' in out['families'][k]['E2_Hill'][f])
    s['recon_max_abs_E2_Hill'] = {f: max(out['families'][k]['E2_Hill'][f]['recon_max_abs'] for k in KEYS
                                         if 'recon_max_abs' in out['families'][k]['E2_Hill'][f]) for f in ('t4', 't2')}
    s['zero_ctrl_max_abs'] = max(abs(out['families'][k][arm][fam]['r0']) for k, arm, fam in fams)
    s['pure_l2_change_t1_max'] = max(abs(raw['keys'][k]['pure_l2_change_t1']) for k in CUBIC)
    s['twoleg_rel_max'] = max(out['families'][k][arm][fam]['twoleg_rel'] for k, arm, fam in fams
                              if out['families'][k][arm][fam].get('twoleg_rel') is not None)
    s['twoleg_rel_max_by_arm_family'] = {'%s/%s' % (arm, fam): max(out['families'][k][arm][fam]['twoleg_rel'] for k in KEYS
                                                                    if out['families'][k][arm][fam].get('twoleg_rel') is not None)
                                         for arm in ARMS for fam in ('t4', 't2')
                                         if any(out['families'][k][arm][fam].get('twoleg_rel') is not None for k in KEYS)}
    s['twoleg_kappa3_rel_max'] = max(out['families'][k][arm][fam]['twoleg_kappa3_rel'] for k, arm, fam in fams
                                     if out['families'][k][arm][fam].get('twoleg_kappa3_rel') is not None)
    s['twoleg_S_abs_max'] = max(out['families'][k][arm][fam]['twoleg_S_abs'] for k, arm, fam in fams
                                if out['families'][k][arm][fam].get('twoleg_S_abs') is not None)
    s['b1_twoleg_rel_max'] = max(rel(raw['keys'][k]['b1_Hill'], raw['keys'][k]['b1_Hill_cc']) for k in KEYS)
    s['quadform_kappa22_twoleg_rel_max'] = max(rel(raw['keys'][k]['quadform']['kappa22_fit7'], raw['keys'][k]['quadform']['kappa22_fit7_cc']) for k in HEX)
    s['fit_res_max_by_arm'] = {arm: max(out['families'][k][arm][fam]['fit_res_rel'] for k in KEYS for fam in ('t4', 't2')
                                        if out['families'][k][arm][fam]['mapped'] and out['families'][k][arm][fam]['fit_res_rel'] is not None)
                               for arm in ARMS}
    s['hs_over_hill_minus_1'] = {k: {f: raw['keys'][k]['arms']['E2_HSmean'][f]['kappa'] / raw['keys'][k]['arms']['E2_Hill'][f]['kappa'] - 1
                                     for f in (['t4', 't2'] if k in HEX else ['t4'])} for k in KEYS}
    pos = [out['reach'][k][arm]['hull'][1] / out['reach'][k][arm]['box'][1] for k in KEYS for arm in ARMS if out['reach'][k][arm]['box'][1] > 0]
    neg = [out['reach'][k][arm]['hull'][0] / out['reach'][k][arm]['box'][0] for k in KEYS for arm in ARMS if out['reach'][k][arm]['box'][0] < 0]
    s['grid_excess_over_box_max'] = {'positive_side': max(pos), 'negative_side': max(neg)}
    s['grid_excess_over_box_max_by_arm'] = {arm: max([out['reach'][k][arm]['hull'][1] / out['reach'][k][arm]['box'][1] for k in KEYS if out['reach'][k][arm]['box'][1] > 0]
                                                     + [out['reach'][k][arm]['hull'][0] / out['reach'][k][arm]['box'][0] for k in KEYS if out['reach'][k][arm]['box'][0] < 0])
                                            for arm in ARMS}
    n2 = out['nulls']['N-2']
    s['null_max_abs'] = {
        'N-1_bi_by_arm': {arm: max(abs(v['bi']) for kk, v in out['nulls']['N-1'].items() if kk.split('/')[1] == arm) for arm in ARMS},
        'N-1_fit_by_arm': {arm: max(abs(v['fit']) for kk, v in out['nulls']['N-1'].items() if kk.split('/')[1] == arm)
                           for arm in ARMS if all(v['fit'] is not None for kk, v in out['nulls']['N-1'].items() if kk.split('/')[1] == arm)},
        'N-2_by_estimator_hex': {e: max(abs(n2[k][e]) for k in HEX) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')},
        'N-2_by_estimator_cubic': {e: max(abs(n2[k][e]) for k in CUBIC) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')},
        'N-3_fit': max(abs(v['fit']) for v in out['nulls']['N-3'].values()),
        'N-3_bi': max(abs(v['bi']) for v in out['nulls']['N-3'].values()),
        'N-4_fit7': max(abs(v['fit7']) for v in out['nulls']['N-4'].values()),
        'N-4_bi_5x5': max(abs(v['bi_5x5']) for v in out['nulls']['N-4'].values()),
        'N-4_k12_chat': max(abs(v['k12_chat_t2sq']) for v in out['nulls']['N-4'].values() if v['k12_chat_t2sq'] is not None)}
    return out


def preflight(dv, constants):
    """The Phase-0 criteria that depend on pinned values only, evaluated at build time (the legs repeat them at Phase 0
    with their own code). A failure means the banked record itself cannot pass a control: nothing is written."""
    s, n = dv['summary'], dv['nulls']
    tau, kf = constants['tau_agg'], constants['kappa_floor']
    robust_res = max(dv['families'][k][arm][f]['fit_res_rel'] for k in KEYS for arm in ('E2_HSmean', 'h_Hill') for f in ('t4', 't2')
                     if dv['families'][k][arm][f]['mapped'])
    checks = [
        ('F-CTRL-SA-PIN two-leg kappa (rel)', s['twoleg_rel_max'], constants['pin_twoleg_tol_rel']),
        ('F-CTRL-SA-PIN two-leg quadform kappa22 (rel)', s['quadform_kappa22_twoleg_rel_max'], constants['pin_twoleg_tol_rel']),
        ('F-CTRL-SA-PIN two-leg cubic coefficient kappa3 (rel)', s['twoleg_kappa3_rel_max'], constants['pin_twoleg_tol_rel']),
        ('F-CTRL-SA-PIN two-leg b1 (rel)', s['b1_twoleg_rel_max'], constants['pin_twoleg_tol_rel']),
        ('F-CTRL-SA-PIN two-leg first-order slope S (abs)', s['twoleg_S_abs_max'], constants['tau_agg']),
        ('F-CTRL-SA-ZERO r(0) (abs)', s['zero_ctrl_max_abs'], constants['zero_ctrl_tol_abs']),
        ('F-CTRL-SA-RECON S2-E2 Hill t4 (abs)', s['recon_max_abs_E2_Hill']['t4'], constants['recon_tol_abs_E2_Hill']),
        ('F-CTRL-SA-RECON S2-E2 Hill t2 (abs)', s['recon_max_abs_E2_Hill']['t2'], constants['recon_tol_abs_E2_Hill']),
        ('F-CTRL-SA-RECON robustness arms kappa vs bi (rel)', robust_res, constants['recon_tol_rel_robust']),
        ('F-CTRL-SA-S N-1 bi (abs)', max(abs(v['bi']) for v in n['N-1'].values()), tau),
        ('F-CTRL-SA-S N-1 fit where banked (abs)', max(abs(v['fit']) for v in n['N-1'].values() if v['fit'] is not None), tau),
        ('F-CTRL-SA-K24 N-2 every estimator (abs)', max(max(abs(v[e]) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')) for v in n['N-2'].values()), kf),
        ('F-CTRL-SA-L2NULL N-3 fit and bi (abs)', max(max(abs(v['fit']), abs(v['bi'])) for v in n['N-3'].values()), kf),
        ('F-CTRL-SA-L2NULL N-4 fit7, bi, k12 (abs)', max(max(abs(v['fit7']), abs(v['bi_5x5']), abs(v['k12_chat_t2sq'] or 0.0)) for v in n['N-4'].values()), kf),
        ('F-CTRL-SA-L2NULL t2 alone at t2 = 1 (abs)', s['pure_l2_change_t1_max'], constants['l2null_t1_tol_abs']),
    ]
    for name, val, tol in checks:
        guard(val <= tol, 'preflight failed: %s = %.3e > %.1e' % (name, val, tol))
    return checks


def exact_rms_checks():
    """<P2^2> = 1/5, <P4^2> = 1/9 (Legendre orthogonality over mu in [-1, 1]) and <K4~^2> = 4/21, <K4~> = 0 over the
    unit sphere, K4~ = (5/2)(x^4 + y^4 + z^4 - 3/5), from the exact sphere moments
    <x^2a y^2b z^2c> = (2a-1)!!(2b-1)!!(2c-1)!!/(2s+1)!!, s = a + b + c.  Exact rational arithmetic."""
    def dfact(n):
        r = 1
        while n > 1:
            r *= n
            n -= 2
        return r

    def mom(a, b, c):
        return Fraction(dfact(2 * a - 1) * dfact(2 * b - 1) * dfact(2 * c - 1), dfact(2 * (a + b + c) + 1))

    def leg_sq(coeffs):  # <p(mu)^2> over mu uniform in [-1, 1]; p given by {power: coefficient}
        tot = Fraction(0)
        for i, ci in coeffs.items():
            for j, cj in coeffs.items():
                n = i + j
                tot += ci * cj * (Fraction(1, n + 1) if n % 2 == 0 else 0)
        return tot
    P2 = {2: Fraction(3, 2), 0: Fraction(-1, 2)}
    P4 = {4: Fraction(35, 8), 2: Fraction(-30, 8), 0: Fraction(3, 8)}
    S1 = 3 * mom(2, 0, 0)
    S2 = 3 * mom(4, 0, 0) + 6 * mom(2, 2, 0)
    K4_mean = Fraction(5, 2) * (S1 - Fraction(3, 5))
    K4_sq = Fraction(25, 4) * (S2 - 2 * Fraction(3, 5) * S1 + Fraction(9, 25))
    res = {'P2_sq': leg_sq(P2), 'P4_sq': leg_sq(P4), 'K4_sq': K4_sq, 'K4_mean': K4_mean}
    guard(res == {'P2_sq': Fraction(1, 5), 'P4_sq': Fraction(1, 9), 'K4_sq': Fraction(4, 21), 'K4_mean': Fraction(0)},
          'rms closed forms failed the exact check')
    return {k: str(v) for k, v in res.items()}


def assemble(raw, glob, meta, builder_md5):
    grids = dict(GRIDS_FIXED)
    grids.update(glob['grids'])
    constants = dict(CONSTANTS)
    raw_all = {'keys': raw['keys'], 'regime': glob['regime']}
    prov = {'keys/<K>/' + dest: {'src': alias, 'pointer': ptmpl, 'scope': scope} for dest, alias, ptmpl, scope in FIELDS}
    for dest, alias, p in GLOBAL_FIELDS:
        prov[dest if not dest.startswith('regime/') else 'raw/' + dest] = {'src': alias, 'pointer': p, 'scope': 'global'}
    doc = {
        '_meta': {'gate': GATE, 'file_schema': FILE_SCHEMA, 'builder': 'sa_build_pinned_inputs.py',
                  'builder_md5': builder_md5, 'base_ledger_md5': 'd4c42a53cbd6d325ebc740879288e844',
                  'contents': 'banked values by named key + fixed constants, grid generators and tokens + a derived '
                              'reference section; no anchor value; no observational number; no point count',
                  'elections_applied': ELECTIONS,
                  'cubic_term_order': CUBIC_TERM_ORDER, 'dqf_basis_order': DQF_BASIS,
                  'dqf_basis_note': 'index order of the chat quadform-basis diagnostic; asserted by this builder: k7[0..2] '
                                    'equal the fit7 kappa22, kappa24, kappa44 of the same key bit for bit and k7[3..6] '
                                    'equal the CC named cubic terms to 1e-4 relative; k12[3..6] equal k7[3..6] to 1e-8 '
                                    'relative (the shared order); the k12 quartic indices 7..11 follow the monomial order '
                                    'and are not independently confirmed (no instrument reads them)'},
        'sources': meta,
        'provenance': prov,
        'structure': STRUCTURE,
        'tokens': TOKENS,
        'constants': constants,
        'grids': grids,
        'raw': raw_all,
        'rms_exact_check': exact_rms_checks(),
    }
    doc['derived'] = derive(raw_all_for_derive(raw_all), constants, grids)
    return doc


def raw_all_for_derive(raw_all):
    return {'keys': raw_all['keys'], 'regime': raw_all['regime']}


def serialize(doc):
    return (json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')


def verify_written(path, docs):
    b = open(path, 'rb').read()
    d = json.loads(b.decode('ascii'))
    # (1) derived is a pure function of the file's own raw / constants / grids
    guard(serialize_part(derive(raw_all_for_derive(d['raw']), d['constants'], d['grids'])) == serialize_part(d['derived']),
          'derived section does not re-derive bit-identically from the written file')
    # (2) every raw value equals its source by pointer, bit for bit
    n = 0
    for dest, alias, ptmpl, scope in FIELDS:
        for k in scope_keys(scope, docs):
            v_src = ptr_get(docs[alias], ptmpl.format(K=k))
            cur = d['raw']['keys'][k]
            for p in dest.split('/'):
                cur = cur[p]
            guard(json.dumps(cur) == json.dumps(v_src) and cur == v_src, 'raw value differs from source: %s %s' % (k, dest))
            n += 1
    for dest, alias, p in GLOBAL_FIELDS:
        cur = d['grids'][dest.split('/')[1]] if dest.startswith('grids/') else d['raw']['regime'][dest.split('/')[1]]
        guard(cur == ptr_get(docs[alias], p), 'global value differs from source: ' + dest)
        n += 1
    # (3) the round trip is byte-stable
    guard(serialize(d) == b, 'serialization is not byte-stable')
    return b, n


def serialize_part(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=True, allow_nan=False)


def counts(doc):
    g, D = doc['grids'], doc['constants']['D']
    tg = g['t_grid']
    return {'t_grid': len(tg),
            'fit_window_0.25_inclusive': len([t for t in tg if abs(t) <= D]),
            'fit_window_0.25_strict': len([t for t in tg if abs(t) < D]),
            'window_0.1_inclusive': len([t for t in tg if abs(t) <= 0.1]),
            'window_0.1_strict': len([t for t in tg if abs(t) < 0.1]),
            't2t4_axis': len(g['t2t4_axis']), 't2t4_grid': len(g['t2t4_axis']) ** 2,
            'area_grid': g['area_grid']['nodes_per_axis'] ** 2,
            'raw_keys': len(doc['raw']['keys'])}


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        return 2
    repo = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) == 3 else OUT_DEFAULT
    guard(sys.float_info.mant_dig == 53, 'IEEE-754 double precision required')
    builder_md5 = hashlib.md5(open(os.path.abspath(__file__), 'rb').read()).hexdigest()
    docs, meta = load_sources(repo)
    raw, glob = build_raw(docs)
    doc = assemble(raw, glob, meta, builder_md5)
    pre = preflight(doc['derived'], doc['constants'])
    data = serialize(doc)
    with open(out, 'wb') as fh:
        fh.write(data)
    try:
        b, n = verify_written(out, docs)
    except Exception:
        os.remove(out)
        raise
    dv, c = doc['derived'], counts(doc)
    print('G-MSCS-A pinned inputs -- builder md5 %s' % builder_md5)
    print('sources (7, full md5 + bytes verified):')
    for a, m in meta.items():
        print('  %-7s %s  %s  %6d B' % (a, m['md5'], m['path'], m['bytes']))
    print('counts from the generators (printed, never written): %s' % ', '.join('%s %d' % kv for kv in c.items()))
    print('self-verification: derived re-derived bit-identically from the written file; %d raw values equal their sources by pointer; byte-stable round trip' % n)
    print('rms exact: %s' % doc['rms_exact_check'])
    print('preflight on banked values (the legs repeat these at Phase 0):')
    for name, val, tol in pre:
        print('  PASS %-52s %.2e <= %.0e' % (name, val, tol))
    print('\nS2-E2 Hill coefficients (memo section 0 table):')
    print('  %-15s %15s %15s %9s %15s %15s' % ('key', 'k44 record', 'k44 bi', 'res', 'k2 record', 'k2 bi'))
    for k in KEYS:
        f4, f2 = dv['families'][k]['E2_Hill']['t4'], dv['families'][k]['E2_Hill']['t2']
        print('  %-15s %+15.6e %+15.6e %9.2e %+15.6e %+15.6e' % (k, f4['kappa'], f4['kappa_bi'], f4['fit_res_rel'], f2['kappa'], f2['kappa_bi']))
    print('\nreach R^w = (1 + mu) * hull (memo section 0 table):')
    for k in KEYS:
        print('  %-15s ' % k + '  '.join('%s [%+.3e, %+.3e]' % (arm, *dv['reach'][k][arm]['widened']) for arm in ARMS))
    u = dv['unions']
    print('\nunions: widened all [%+.4e, %+.4e]  widened primary [%+.4e, %+.4e]' % (*u['widened_all'], *u['widened_primary']))
    print('        hull all    [%+.4e, %+.4e]  hull primary    [%+.4e, %+.4e]' % (*u['hull_all'], *u['hull_primary']))
    print('synthetic intervals: ' + '  '.join('%s [%+.4e, %+.4e]' % (k, *v) for k, v in sorted(dv['synthetic'].items())))
    print('\nhex null-ray slopes |t4/t2|:')
    for k in HEX:
        print('  %-12s ' % k + '  '.join('%s %.4f' % kv for kv in sorted(dv['hex_quadform'][k]['null_ray_slope'].items())) + '  S2-h: ' + dv['hex_quadform'][k]['h_Hill_form'])
    s = dv['summary']
    print('\nsummary:')
    for key in sorted(s):
        v = s[key]
        if isinstance(v, dict):
            print('  %s: %s' % (key, {kk: (('%.4g' % vv) if isinstance(vv, float) else {a: '%.4g' % b for a, b in vv.items()}) for kk, vv in v.items()}))
        else:
            print('  %s: %.6g' % (key, v))
    print('\nwrote %s  md5 %s  %d B' % (out, hashlib.md5(b).hexdigest(), len(b)))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except GuardError as e:
        print('GUARD FAILED: %s' % e)
        sys.exit(1)

=====END-EMBED name=sa_build_pinned_inputs.py=====

=====BEGIN-EMBED name=sa_verify_pinned_inputs.py md5=cf004d517d2efe91a02c92a58e3df6bf bytes=28804 encoding=raw=====
#!/usr/bin/env python3
"""sa_verify_pinned_inputs.py -- G-MSCS-A (staging memo v2, section 9): an independent check of the pinned-inputs file,
written separately from the builder (no shared code) for the author's pre-lock verification. Revised after the v2 audit:
it trusts nothing in the file under test -- the keys, arms, pointers, constants, tokens and structure it expects are
written into this script -- and it re-derives EVERY leaf of the file's `derived` block with its own code.

Checks:
 (1) the seven sources on disk carry the md5s and byte counts of record (written here), and the file's `sources` block
     says the same;
 (2) the file's `provenance` block equals the pointer map written here, field for field (a redirected pointer fails);
     every `raw` value equals its source value through that pointer, bit for bit; the `raw` block holds exactly the
     expected leaves (none missing, none extra); the number of comparisons equals the expected number;
 (3) `constants`, `tokens`, `structure`, `grids`, `_meta` (the embedded builder md5 included: it must name the builder
     of record, written here) and `rms_exact_check` equal the values written here (the rms closed forms re-verified in
     exact rational arithmetic);
 (4) a full re-derivation of `derived` from the file's own `raw` block with this script's code: every leaf of the
     file's `derived` block is compared (floats within |d| <= 1e-12*|x| + 1e-16 -- a few leaves differ from the
     builder's in the last bits because the arithmetic is ordered differently; types, strings, booleans and nulls
     exactly), the two leaf sets are identical, and the count is reported. Tampering below that tolerance is caught
     by the whole-file md5, which the author compares with the md5 of record;
 (5) no point count is written in the file (rule 4).

Usage:  python3 sa_verify_pinned_inputs.py REPO_DIR PINNED_FILE [BUILDER_FILE]
        (with BUILDER_FILE, the md5 embedded in the file must equal that file's md5)
Exit:   0 all checks pass; 1 any check fails; 2 usage.  Prints no value that the memo does not already print."""
import hashlib, json, math, os, sys
from fractions import Fraction

SOURCES = {
    'G2chat': ('gmscs2_gate/g_mscs2_chatleg_checkpoint.json', '1c5b6b59829d2a6b9ae2b1a7a016832d', 31575),
    'G2cc':   ('gmscs2_gate/g_mscs2_ccleg_checkpoint.json',   '9961745d1e1857cfab6445d4754b5060', 68540),
    'G1chat': ('gmscs1_gate/g_mscs1_chatleg_checkpoint.json', 'c04c0b8ea34cfe60f231aa06828e6ce4', 33289),
    'G1cc':   ('gmscs1_gate/g_mscs1_ccleg_checkpoint.json',   '249e11dd53c4cb82f302b15d3c94c337', 24415),
    'DK24':   ('gmscs2_gate/diag_kappa24.json',               'b7952dfcaddcd1d98e424aee8ce5231f', 1917),
    'DQF':    ('gmscs2_gate/diag_quadform_basis.json',        'd84aa1fdce7dea1b1a5d24dfb8f13c18', 1119),
    'CI1':    ('gci1_gate/ci1_phase3_cc_r2.json',             '845ae6beb1b90fe34c540f843ffdb9f5', 45760),
}
HEXK = ['hex_step|a', 'hex_step|b', 'hex_gem8|a', 'hex_gem8|b']
CUBK = ['cubic_step|001', 'cubic_step|111', 'cubic_gem8|001', 'cubic_gem8|111']
ALLK = HEXK + CUBK
ARMS = ['E2_Hill', 'E2_HSmean', 'h_Hill']
PRIM = ['hex_step|a', 'hex_gem8|a', 'cubic_step|001', 'cubic_gem8|001']
TOL_REL, TOL_ABS = 1e-12, 1e-16

# -------------------------------------------------------------------- the expected pointer map, generated from a table
KAPPA_NAME = {('E2_Hill', 't4'): 'kappa44_E2', ('E2_HSmean', 't4'): 'kappa44_E2_HS', ('h_Hill', 't4'): 'kappa44_h',
              ('E2_Hill', 't2'): 'kappa2_E2', ('E2_HSmean', 't2'): 'kappa2_E2_HS', ('h_Hill', 't2'): 'kappa2_h'}
GRID_NAME = {'E2_Hill': 'r_agg_E2_VRH', 'E2_HSmean': 'r_agg_E2_HS', 'h_Hill': 'r_agg_h_VRH'}
S_NAME = {('E2_Hill', 't4'): 'S4_E2', ('h_Hill', 't4'): 'S4_h', ('E2_Hill', 't2'): 'S_t_E2', ('h_Hill', 't2'): 'S_t_h'}
K3_NAME = {'t4': 'kappa444_E2', 't2': 'kappa3_E2'}
HAS_KAPPA_CC = {('E2_Hill', 't4'), ('E2_HSmean', 't4'), ('h_Hill', 't4'), ('E2_Hill', 't2'), ('h_Hill', 't2')}

def expected_provenance():
    P = {}
    def put(dest, src, ptr, scope='all'):
        P['keys/<K>/' + dest] = {'src': src, 'pointer': ptr, 'scope': scope}
    for arm in ARMS:
        for fam in ('t4', 't2'):
            g = 'G2' if fam == 't4' else 'G1'
            base = 'arms/%s/%s/' % (arm, fam)
            put(base + 'kappa', g + 'chat', '/phase2/{K}/' + KAPPA_NAME[(arm, fam)])
            put(base + 'grid', g + 'chat', '/phase2/{K}/' + GRID_NAME[arm])
            if (arm, fam) in HAS_KAPPA_CC:
                put(base + 'kappa_cc', g + 'cc', '/phase2/{K}/' + KAPPA_NAME[(arm, fam)])
            if (arm, fam) in S_NAME:
                put(base + 'S', g + 'chat', '/phase2/{K}/' + S_NAME[(arm, fam)])
                put(base + 'S_cc', g + 'cc', '/phase2/{K}/' + S_NAME[(arm, fam)])
            if arm == 'E2_Hill':
                put(base + 'kappa3', g + 'chat', '/phase2/{K}/' + K3_NAME[fam])
                put(base + 'kappa3_cc', g + 'cc', '/phase2/{K}/' + K3_NAME[fam])
    for q, leg in (('kappa22', 'chat'), ('kappa24', 'chat'), ('kappa44', 'chat')):
        put('quadform/%s_fit7' % q, 'G2' + leg, '/phase2/{K}/quadform/' + q)
    put('quadform/kappa22_fit7_cc', 'G2cc', '/phase2/{K}/quadform/kappa22')
    put('quadform/grid5x5_cc', 'G2cc', '/phase2/{K}/quadform/x_grid_r_agg_E2_VRH')
    put('quadform/cubic_terms_cc', 'G2cc', '/phase2/{K}/quadform/x_cubic_terms_discarded')
    put('quadform/reading_cc', 'G2cc', '/phase2/{K}/quadform/x_reading')
    put('quadform/basis_k7_chat', 'DQF', '/{K}/k7', 'dqf')
    put('quadform/basis_k12_chat', 'DQF', '/{K}/k12', 'dqf')
    put('kappa24_bi_chat', 'DK24', '/{K}/kappa24_richardson')
    put('kappa24_bi_cc', 'G2cc', '/phase2/{K}/kappa24_richardson')
    put('b1_Hill', 'G2chat', '/phase2/{K}/biref_b1_VRH')
    put('b1_Hill_cc', 'G2cc', '/phase2/{K}/biref_b1_VRH')
    put('pure_l2_change_t1', 'DK24', '/{K}/pure_l2_r_agg_change_t1', 'cubic')
    put('A31_mixed_change_cc', 'G2cc', '/extras/A3_diagnostics/A-3.1_mixed_r_agg_change_A29/{K}', 'cubic')
    P['grids/t_grid'] = {'src': 'G2chat', 'pointer': '/t4_grid', 'scope': 'global'}
    P['grids/t2t4_axis'] = {'src': 'G2chat', 'pointer': '/t2t4_grid', 'scope': 'global'}
    P['raw/regime/d_EM'] = {'src': 'CI1', 'pointer': '/per_oom/x1/W_EM_union/0/1', 'scope': 'global'}
    return P

EXPECTED_CONSTANTS = {
    'D': 0.25, 'mu': 0.10, 'KD_CLIP': 0.3, 'tau_agg': 1e-6, 'kappa_floor': 1e-6, 'zero_snap': 1e-12,
    'trunc_threshold': 0.10, 'nullfloor_threshold': 0.10, 'recon_tol_abs_E2_Hill': 1e-8, 'recon_tol_rel_robust': 1e-3,
    'pin_twoleg_tol_rel': 1e-4, 'zero_ctrl_tol_abs': 1e-12, 'l2null_t1_tol_abs': 1e-12, 'edge_twoleg_tol_rel': 1e-10,
    'mono_tol_rel': 1e-14, 'pin_derived_tol_rel': 1e-12, 'pin_derived_tol_abs': 1e-16, 'oom_factors': [0.1, 1.0, 10.0],
    'synthetic_t': [0.01, 0.1, 0.5], 'synthetic_t_tight': 1e-9, 'synthetic_band_fractions': [0.25, 0.75],
    'synthetic_k': {'silent': 1.0, 'void': 1e33},
    'synthetic_rules': {
        'margin_positive': '[h + f1*(w - h), h + f2*(w - h)], h = unions.hull_all[1], w = unions.widened_all[1]',
        'margin_negative': '[w + f1*(h - w), w + f2*(h - w)], w = unions.widened_all[0], h = unions.hull_all[0]',
        'robustness_only_positive': '[p + f1*(q - p), p + f2*(q - p)], p = unions.widened_primary[1], q = unions.hull_all[1]'},
    'rms': {'hexP2': math.sqrt(0.2), 'hexP4': 1.0 / 3.0, 'cubK4': math.sqrt(4.0 / 21.0)},
    'rms_closed_form': {'hexP2': 'sqrt(1/5)', 'hexP4': '1/3', 'cubK4': 'sqrt(4/21)'},
    'fam_rms': {'t2': 'hexP2', 't4_hex': 'hexP4', 't4_cubic': 'cubK4'},
}
EXPECTED_TOKENS = {
    'odf_reading': ['none', 'uniform', 'hexP2', 'hexP4', 'hexP2P4', 'cubK4', 'cubP2-i', 'cubP2-ii', 'cubP2K4-i', 'cubP2K4-ii'],
    'delta_def': 'tensor_over_EM_minus_1', 'class': ['spd'], 'reading_conformant': ['bound'],
    'reading_frozen_list': ['bound', 'ceiling', 'margin', 'criterion'], 'geom': ['single', 'population'], 'q': ['phase', 'group'],
}
EXPECTED_STRUCTURE = {
    'keys': ALLK, 'hex_keys': HEXK, 'cubic_keys': CUBK, 'arms': ARMS, 'primary': {'arm': 'E2_Hill', 'keys': PRIM},
    'robustness': {'arms': ['E2_HSmean', 'h_Hill'], 'keys': ['hex_step|b', 'hex_gem8|b', 'cubic_step|111', 'cubic_gem8|111']},
    'mapped_families': {'hex': ['t4', 't2'], 'cubic': ['t4']}, 'null_families': {'cubic': ['t2']},
    'kill_test_set': 'every key x every arm (E-SA-9(a)); the primary-only union is serialized for information',
}
EXPECTED_GRIDS_FIXED = {
    'fit_window': 'abs(t) <= D, inclusive (the window both banked legs used; H-CC-1)',
    'richardson_pairs': {'one_param': [0.05, 0.1], 'two_param': [0.125, 0.25]},
    'richardson_formulas': {
        'odd':   '[4*O(h1) - O(h2)]/3, O(h) = [r(h) - r(-h)]/(2h)',
        'even':  '[4*E(h1) - E(h2)]/3, E(h) = [r(h) + r(-h) - 2*r(0)]/(2h^2)',
        'mixed': '[4*M(h1) - M(h2)]/3, M(h) = [R(h,h) - R(h,-h) - R(-h,h) + R(-h,-h)]/(4h^2)'},
    'grid5x5_layout': 'row-major, t2 outer, t4 inner: index = 5*i + j for (t2_axis[i], t4_axis[j])',
    'area_grid': {'lo': -0.25, 'hi': 0.25, 'nodes_per_axis': 201, 'node': 'lo + i*(hi - lo)/(nodes_per_axis - 1)'},
}
EXPECTED_META = {
    'gate': 'G-MSCS-A', 'file_schema': 'g_mscs_a_pinned_inputs/1', 'builder': 'sa_build_pinned_inputs.py',
    'base_ledger_md5': 'd4c42a53cbd6d325ebc740879288e844',
    'elections_applied': {'E-SA-0': 'a', 'E-SA-1': 'a', 'E-SA-2': 'a', 'E-SA-3': 'a', 'E-SA-4': 'a', 'E-SA-5': 'a',
                          'E-SA-6': 'a', 'E-SA-7': 'base 05302210 + the G-MSCS1 stratum', 'E-SA-8': 'a', 'E-SA-9': 'a',
                          'E-SA-10': 'a', 'E-SA-11': 'a'},
    'cubic_term_order': ['t2^3', 't2^2*t4', 't2*t4^2', 't4^3'],
    'dqf_basis_order': ['t2^2', 't2*t4', 't4^2', 't2^3', 't2^2*t4', 't2*t4^2', 't4^3', 't2^4', 't2^3*t4', 't2^2*t4^2', 't2*t4^3', 't4^4'],
    'contents': 'banked values by named key + fixed constants, grid generators and tokens + a derived reference section; no anchor value; no observational number; no point count',
    'dqf_basis_note': 'index order of the chat quadform-basis diagnostic; asserted by this builder: k7[0..2] equal the fit7 kappa22, kappa24, kappa44 of the same key bit for bit and k7[3..6] equal the CC named cubic terms to 1e-4 relative; k12[3..6] equal k7[3..6] to 1e-8 relative (the shared order); the k12 quartic indices 7..11 follow the monomial order and are not independently confirmed (no instrument reads them)',
}
EXPECTED_BUILDER_MD5 = '8189100ede80eac360b25a146e580abf'   # the builder of record (staging memo v2); the file must name it

fails = []
def check(ok, what):
    if not ok:
        fails.append(what)
    return ok

def get(doc, pointer):
    node = doc
    for part in pointer.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node

def flat(node, prefix=''):
    """leaf paths of a JSON tree; lists of numbers are expanded element by element"""
    out = {}
    if isinstance(node, dict):
        for k, v in node.items():
            out.update(flat(v, (prefix + '/' + k) if prefix else k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.update(flat(v, '%s[%d]' % (prefix, i)))
    else:
        out[prefix] = node
    return out

def same(a, b):
    if type(a) != type(b):
        return False
    if isinstance(a, float):
        return abs(a - b) <= TOL_REL * abs(b) + TOL_ABS
    return a == b

# ------------------------------------------------------------------------------- the independent re-derivation
def rederive(raw, C, G):
    D, MU, SNAP, KF = C['D'], C['mu'], C['zero_snap'], C['kappa_floor']
    T, AX = G['t_grid'], G['t2t4_axis']
    a1, a2 = G['richardson_pairs']['one_param']
    b1, b2 = G['richardson_pairs']['two_param']
    inside = [i for i in range(len(T)) if -D <= T[i] <= D]

    def val(g, t):
        return dict(zip(T, g))[t]
    def even(g):
        e = lambda h: (val(g, h) + val(g, -h) - 2.0 * val(g, 0.0)) / (2.0 * h * h)
        return (4.0 * e(a1) - e(a2)) / 3.0
    def odd(g):
        o = lambda h: (val(g, h) - val(g, -h)) / (2.0 * h)
        return (4.0 * o(a1) - o(a2)) / 3.0
    def grid5(v):
        n = len(AX)
        return {(AX[i], AX[j]): v[i * n + j] for i in range(n) for j in range(n)}
    def rich5(R, kind):
        def f(h):
            if kind == '22':
                return (R[(h, 0.0)] + R[(-h, 0.0)] - 2.0 * R[(0.0, 0.0)]) / (2.0 * h * h)
            if kind == '44':
                return (R[(0.0, h)] + R[(0.0, -h)] - 2.0 * R[(0.0, 0.0)]) / (2.0 * h * h)
            return (R[(h, h)] - R[(h, -h)] - R[(-h, h)] + R[(-h, -h)]) / (4.0 * h * h)
        return (4.0 * f(b1) - f(b2)) / 3.0
    def relative(x, y):
        return abs(x - y) / max(abs(x), abs(y))
    def token(k, fam):
        if k in HEXK:
            return 'hexP2' if fam == 't2' else 'hexP4'
        return 'cubP2-i' if fam == 't2' else 'cubK4'

    fam_out, reach, zero, n1, n2, n3, n4, hq = {}, {}, {}, {}, {}, {}, {}, {}
    for k in ALLK:
        rk = raw['keys'][k]
        mapped = ('t4', 't2') if k in HEXK else ('t4',)
        fam_out[k], reach[k], zero[k] = {}, {}, {}
        for arm in ARMS:
            fam_out[k][arm] = {}
            for fam in ('t4', 't2'):
                f = rk['arms'][arm][fam]
                kb = even(f['grid'])
                e = {'odf_reading': token(k, fam), 'kappa': f['kappa'], 'kappa_bi': kb,
                     'fit_res_rel': (abs(f['kappa'] - kb) / abs(kb)) if abs(kb) > KF else None,
                     'S_bi': odd(f['grid']), 'S_fit': f['S'] if 'S' in f else None,
                     'r0': val(f['grid'], 0.0), 'mapped': fam in mapped}
                if fam in mapped and 'kappa3' in f:
                    e['recon_max_abs'] = max(abs(f['grid'][i] - (f['S'] * T[i] + f['kappa'] * T[i] ** 2 + f['kappa3'] * T[i] ** 3)) for i in inside)
                    e['trunc_T_at_D'] = abs(f['kappa3']) * D / abs(f['kappa'])
                if 'kappa_cc' in f:
                    e['twoleg_rel'] = relative(f['kappa'], f['kappa_cc']) if max(abs(f['kappa']), abs(f['kappa_cc'])) > KF else None
                if 'kappa3_cc' in f:
                    e['twoleg_kappa3_rel'] = relative(f['kappa3'], f['kappa3_cc']) if fam in mapped else None
                if 'S_cc' in f:
                    e['twoleg_S_abs'] = abs(f['S'] - f['S_cc'])
                fam_out[k][arm][fam] = e
                zero[k][arm + '/' + fam] = {'odf_reading': 'uniform', 'r0': e['r0']}
                if fam in mapped:
                    n1['%s/%s/%s' % (k, arm, fam)] = {'odf_reading': token(k, fam), 'fit': e['S_fit'], 'bi': e['S_bi']}
            lo = sum(min(0.0, rk['arms'][arm][fm]['kappa'] * D * D) for fm in mapped)
            hi = sum(max(0.0, rk['arms'][arm][fm]['kappa'] * D * D) for fm in mapped)
            pts = [rk['arms'][arm][fm]['grid'][i] for fm in mapped for i in inside]
            if arm == 'E2_Hill':
                pts = pts + rk['quadform']['grid5x5_cc']
            hull = [min(lo, min(pts)), max(hi, max(pts))]
            hull = [0.0 if abs(x) < SNAP else x for x in hull]
            reach[k][arm] = {'box': [lo, hi], 'grid_min': min(pts), 'grid_max': max(pts), 'hull': hull,
                             'widened': [x * (1.0 + MU) for x in hull], 'grid_exceeds_box': min(pts) < lo or max(pts) > hi}
        R = grid5(rk['quadform']['grid5x5_cc'])
        n2[k] = {'odf_reading': 'hexP2P4' if k in HEXK else 'cubP2K4-i', 'fit7': rk['quadform']['kappa24_fit7'],
                 'bi_chat': rk['kappa24_bi_chat'], 'bi_cc': rk['kappa24_bi_cc'], 'bi_5x5': rich5(R, '24')}
        if k in CUBK:
            n3[k] = {'odf_reading': 'cubP2-i', 'fit': rk['arms']['E2_Hill']['t2']['kappa'],
                     'bi': even(rk['arms']['E2_Hill']['t2']['grid']), 'pure_l2_change_t1': rk['pure_l2_change_t1']}
            k12 = rk['quadform'].get('basis_k12_chat')
            n4[k] = {'odf_reading': 'cubP2K4-i', 'fit7': rk['quadform']['kappa22_fit7'], 'bi_5x5': rich5(R, '22'),
                     'k12_chat_t2sq': k12[0] if k12 is not None else None}
        else:
            A = rk['arms']
            q22, q44, q24 = rich5(R, '22'), rich5(R, '44'), rich5(R, '24')
            hq[k] = {'k22_bi_5x5': q22, 'k44_bi_5x5': q44, 'k24_bi_5x5': q24,
                     'null_ray_slope': {'E2_Hill_bi5x5': math.sqrt(-q22 / q44),
                                        'E2_Hill_bi': math.sqrt(-even(A['E2_Hill']['t2']['grid']) / even(A['E2_Hill']['t4']['grid'])),
                                        'E2_Hill_fit': math.sqrt(-A['E2_Hill']['t2']['kappa'] / A['E2_Hill']['t4']['kappa']),
                                        'E2_HSmean_bi': math.sqrt(-even(A['E2_HSmean']['t2']['grid']) / even(A['E2_HSmean']['t4']['grid'])),
                                        'E2_HSmean_fit': math.sqrt(-A['E2_HSmean']['t2']['kappa'] / A['E2_HSmean']['t4']['kappa'])},
                     'h_Hill_form': 'negative-definite' if (A['h_Hill']['t2']['kappa'] < 0 and A['h_Hill']['t4']['kappa'] < 0) else 'not negative-definite',
                     'kappa22_fit7_vs_kappa2_rel': relative(rk['quadform']['kappa22_fit7'], A['E2_Hill']['t2']['kappa'])}
    cells = [(k, arm) for k in ALLK for arm in ARMS]
    un = {'hull_all': [min(reach[k][a]['hull'][0] for k, a in cells), max(reach[k][a]['hull'][1] for k, a in cells)],
          'widened_all': [min(reach[k][a]['widened'][0] for k, a in cells), max(reach[k][a]['widened'][1] for k, a in cells)],
          'hull_primary': [min(reach[k]['E2_Hill']['hull'][0] for k in PRIM), max(reach[k]['E2_Hill']['hull'][1] for k in PRIM)],
          'widened_primary': [min(reach[k]['E2_Hill']['widened'][0] for k in PRIM), max(reach[k]['E2_Hill']['widened'][1] for k in PRIM)]}
    f1, f2 = C['synthetic_band_fractions']
    iv = lambda a, b: [a + f1 * (b - a), a + f2 * (b - a)]
    syn = {'margin_positive': iv(un['hull_all'][1], un['widened_all'][1]),
           'margin_negative': iv(un['widened_all'][0], un['hull_all'][0]),
           'robustness_only_positive': iv(un['widened_primary'][1], un['hull_all'][1])}
    # summary
    trip = [(k, arm, fam) for k in ALLK for arm in ARMS for fam in ('t4', 't2')]
    FF = lambda k, arm, fam: fam_out[k][arm][fam]
    b1r = {k: abs(raw['keys'][k]['b1_Hill'] / raw['keys'][k]['arms']['E2_Hill']['t4']['kappa']) for k in ALLK}
    def mx(values):
        values = list(values)
        return max(values)
    ratio_pos = lambda k, a: reach[k][a]['hull'][1] / reach[k][a]['box'][1]
    ratio_neg = lambda k, a: reach[k][a]['hull'][0] / reach[k][a]['box'][0]
    n1_arm = lambda arm: [v for kk, v in n1.items() if kk.split('/')[1] == arm]
    summary = {
        'b1_over_kappa44': b1r,
        'b1_dominance_at_D_min': min(b1r.values()) / D,
        'k_fire_WEM': C['KD_CLIP'] / raw['regime']['d_EM'],
        'trunc_T_at_D_max': mx(FF(k, 'E2_Hill', fam)['trunc_T_at_D'] for k in ALLK for fam in ('t4', 't2') if 'trunc_T_at_D' in FF(k, 'E2_Hill', fam)),
        'recon_max_abs_E2_Hill': {fam: mx(FF(k, 'E2_Hill', fam)['recon_max_abs'] for k in ALLK if 'recon_max_abs' in FF(k, 'E2_Hill', fam)) for fam in ('t4', 't2')},
        'zero_ctrl_max_abs': mx(abs(FF(*t)['r0']) for t in trip),
        'pure_l2_change_t1_max': mx(abs(raw['keys'][k]['pure_l2_change_t1']) for k in CUBK),
        'twoleg_rel_max': mx(FF(*t)['twoleg_rel'] for t in trip if FF(*t).get('twoleg_rel') is not None),
        'twoleg_rel_max_by_arm_family': {'%s/%s' % (arm, fam): mx(FF(k, arm, fam)['twoleg_rel'] for k in ALLK if FF(k, arm, fam).get('twoleg_rel') is not None)
                                         for arm in ARMS for fam in ('t4', 't2') if any(FF(k, arm, fam).get('twoleg_rel') is not None for k in ALLK)},
        'twoleg_kappa3_rel_max': mx(FF(*t)['twoleg_kappa3_rel'] for t in trip if FF(*t).get('twoleg_kappa3_rel') is not None),
        'twoleg_S_abs_max': mx(FF(*t)['twoleg_S_abs'] for t in trip if FF(*t).get('twoleg_S_abs') is not None),
        'b1_twoleg_rel_max': mx(relative(raw['keys'][k]['b1_Hill'], raw['keys'][k]['b1_Hill_cc']) for k in ALLK),
        'quadform_kappa22_twoleg_rel_max': mx(relative(raw['keys'][k]['quadform']['kappa22_fit7'], raw['keys'][k]['quadform']['kappa22_fit7_cc']) for k in HEXK),
        'fit_res_max_by_arm': {arm: mx(FF(k, arm, fam)['fit_res_rel'] for k in ALLK for fam in ('t4', 't2')
                                       if FF(k, arm, fam)['mapped'] and FF(k, arm, fam)['fit_res_rel'] is not None) for arm in ARMS},
        'hs_over_hill_minus_1': {k: {fam: raw['keys'][k]['arms']['E2_HSmean'][fam]['kappa'] / raw['keys'][k]['arms']['E2_Hill'][fam]['kappa'] - 1
                                     for fam in (('t4', 't2') if k in HEXK else ('t4',))} for k in ALLK},
        'grid_excess_over_box_max': {'positive_side': mx(ratio_pos(k, a) for k, a in cells if reach[k][a]['box'][1] > 0),
                                     'negative_side': mx(ratio_neg(k, a) for k, a in cells if reach[k][a]['box'][0] < 0)},
        'grid_excess_over_box_max_by_arm': {arm: mx([ratio_pos(k, arm) for k in ALLK if reach[k][arm]['box'][1] > 0]
                                                    + [ratio_neg(k, arm) for k in ALLK if reach[k][arm]['box'][0] < 0]) for arm in ARMS},
        'null_max_abs': {
            'N-1_bi_by_arm': {arm: mx(abs(v['bi']) for v in n1_arm(arm)) for arm in ARMS},
            'N-1_fit_by_arm': {arm: mx(abs(v['fit']) for v in n1_arm(arm)) for arm in ARMS if all(v['fit'] is not None for v in n1_arm(arm))},
            'N-2_by_estimator_hex': {e: mx(abs(n2[k][e]) for k in HEXK) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')},
            'N-2_by_estimator_cubic': {e: mx(abs(n2[k][e]) for k in CUBK) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')},
            'N-3_fit': mx(abs(v['fit']) for v in n3.values()), 'N-3_bi': mx(abs(v['bi']) for v in n3.values()),
            'N-4_fit7': mx(abs(v['fit7']) for v in n4.values()), 'N-4_bi_5x5': mx(abs(v['bi_5x5']) for v in n4.values()),
            'N-4_k12_chat': mx(abs(v['k12_chat_t2sq']) for v in n4.values() if v['k12_chat_t2sq'] is not None)},
    }
    return {'families': fam_out, 'reach': reach, 'unions': un, 'synthetic': syn, 'zero_ctrl': zero,
            'nulls': {'N-1': n1, 'N-2': n2, 'N-3': n3, 'N-4': n4}, 'hex_quadform': hq, 'summary': summary}

def rms_exact():
    def dfac(n):
        return 1 if n <= 1 else n * dfac(n - 2)
    def sph(a, b, c):   # <x^a y^b z^c> on the unit sphere, a, b, c even
        return Fraction(dfac(a - 1) * dfac(b - 1) * dfac(c - 1), dfac(a + b + c + 1))
    mu = lambda n: Fraction(1, n + 1) if n % 2 == 0 else Fraction(0)
    p2 = {0: Fraction(-1, 2), 2: Fraction(3, 2)}
    p4 = {0: Fraction(3, 8), 2: Fraction(-15, 4), 4: Fraction(35, 8)}
    sq = lambda p: sum(p[i] * p[j] * mu(i + j) for i in p for j in p)
    s1 = sph(4, 0, 0) + sph(0, 4, 0) + sph(0, 0, 4)
    s2 = sph(8, 0, 0) + sph(0, 8, 0) + sph(0, 0, 8) + 2 * (sph(4, 4, 0) + sph(4, 0, 4) + sph(0, 4, 4))
    k4m = Fraction(5, 2) * (s1 - Fraction(3, 5))
    k4s = Fraction(25, 4) * (s2 - Fraction(6, 5) * s1 + Fraction(9, 25))
    return {'P2_sq': str(sq(p2)), 'P4_sq': str(sq(p4)), 'K4_sq': str(k4s), 'K4_mean': str(k4m)}

def main():
    if len(sys.argv) not in (3, 4):
        print(__doc__); return 2
    repo, path = sys.argv[1], sys.argv[2]
    blob = open(path, 'rb').read()
    print('pinned file: md5 %s  %d B' % (hashlib.md5(blob).hexdigest(), len(blob)))
    F = json.loads(blob.decode('ascii'))
    check(sorted(F) == sorted(['_meta', 'sources', 'provenance', 'structure', 'tokens', 'constants', 'grids', 'raw', 'rms_exact_check', 'derived']), 'top-level blocks')
    # (1) sources
    src = {}
    for alias, (rel_path, md5, n) in SOURCES.items():
        b = open(os.path.join(repo, rel_path), 'rb').read()
        check(hashlib.md5(b).hexdigest() == md5 and len(b) == n, 'source md5/bytes: ' + rel_path)
        src[alias] = json.loads(b.decode('utf-8'))
    check(F['sources'] == {a: {'path': p, 'md5': m, 'bytes': n} for a, (p, m, n) in SOURCES.items()}, 'the sources block')
    # (2) provenance and raw
    EP = expected_provenance()
    check(F['provenance'] == EP, 'the provenance block differs from the expected pointer map')
    n_cmp, covered = 0, set()
    for dest, spec in EP.items():
        if dest.startswith('keys/<K>/'):
            sub = dest[len('keys/<K>/'):]
            ks = ALLK if spec['scope'] == 'all' else CUBK if spec['scope'] == 'cubic' else [k for k in ALLK if k in src['DQF']]
            for k in ks:
                want = get(src[spec['src']], spec['pointer'].replace('{K}', k))
                try:
                    have = get(F['raw']['keys'][k], '/' + sub)
                except (KeyError, IndexError, TypeError):
                    check(False, 'raw value missing: %s %s' % (k, sub)); continue
                check(json.dumps(have) == json.dumps(want), 'raw != source: %s %s' % (k, sub))
                covered.add('keys/%s/%s' % (k, sub)); n_cmp += 1
        else:
            want = get(src[spec['src']], spec['pointer'])
            have = get(F, '/' + dest)
            check(json.dumps(have) == json.dumps(want), 'global != source: ' + dest)
            n_cmp += 1
    expect_cmp = sum(len(ALLK) if s['scope'] == 'all' else len(CUBK) if s['scope'] == 'cubic' else (sum(1 for k in ALLK if k in src['DQF']) if s['scope'] == 'dqf' else 1)
                     for s in EP.values())
    check(n_cmp == expect_cmp, 'comparison count')
    check(sorted(F['raw']) == ['keys', 'regime'] and sorted(F['raw']['regime']) == ['d_EM'] and sorted(F['raw']['keys']) == sorted(ALLK), 'raw block shape')
    raw_leaves = set()
    for k in ALLK:
        check(F['raw']['keys'][k].get('branch') == ('hex' if k in HEXK else 'cubic'), 'branch of ' + k)
        for p in flat({kk: vv for kk, vv in F['raw']['keys'][k].items() if kk != 'branch'}):
            raw_leaves.add('keys/%s/%s' % (k, p.split('[')[0]))
    check(raw_leaves == covered, 'raw leaves without a pointer, or pointers without a raw leaf')
    print('provenance: %d values equal their sources through the pointer map written here (expected %d); %d raw fields, all covered' % (n_cmp, expect_cmp, len(covered)))
    # (3) constants, tokens, structure, grids, meta, rms
    check(F['constants'] == EXPECTED_CONSTANTS, 'constants')
    check(F['tokens'] == EXPECTED_TOKENS, 'tokens')
    check(F['structure'] == EXPECTED_STRUCTURE, 'structure')
    g_fixed = {k: v for k, v in F['grids'].items() if k not in ('t_grid', 't2t4_axis')}
    check(g_fixed == EXPECTED_GRIDS_FIXED and sorted(F['grids']) == sorted(list(EXPECTED_GRIDS_FIXED) + ['t_grid', 't2t4_axis']), 'grids')
    m = F['_meta']
    check(all(m.get(k) == v for k, v in EXPECTED_META.items()), '_meta')
    check(sorted(m) == sorted(list(EXPECTED_META) + ['builder_md5']), '_meta fields')
    check(m.get('builder_md5') == EXPECTED_BUILDER_MD5, 'the embedded builder md5 is not the builder of record')
    check(isinstance(m.get('builder_md5'), str) and len(m['builder_md5']) == 32 and all(c in '0123456789abcdef' for c in m['builder_md5']), 'builder md5 field')
    if len(sys.argv) == 4:
        check(hashlib.md5(open(sys.argv[3], 'rb').read()).hexdigest() == m['builder_md5'], 'the embedded builder md5 differs from the builder file')
    check(F['rms_exact_check'] == rms_exact() == {'P2_sq': '1/5', 'P4_sq': '1/9', 'K4_sq': '4/21', 'K4_mean': '0'}, 'rms exact check')
    # (4) full re-derivation
    mine = flat(rederive(F['raw'], F['constants'], F['grids']))
    theirs = flat(F['derived'])
    check(set(mine) == set(theirs), 'derived leaf sets differ (%d here, %d in the file)' % (len(mine), len(theirs)))
    bad = [p for p in theirs if p in mine and not same(mine[p], theirs[p])]
    for p in bad[:10]:
        check(False, 'derived mismatch: ' + p)
    n_num = sum(1 for v in theirs.values() if isinstance(v, float))
    print('re-derivation: all %d derived leaves compared (%d numeric within %.0e rel + %.0e abs; the rest exact); %d mismatches'
          % (len(theirs), n_num, TOL_REL, TOL_ABS, len(bad)))
    # (5) rule 4
    words = [p for p in flat(F) if any(w in p.split('/')[-1].split('[')[0].lower() for w in ('count', 'n_points', 'npts', 'num_points'))]
    check(not words, 'a count-like field is written')
    T = F['grids']['t_grid']
    print('counts computed here: t grid %d; |t| <= D: %d inclusive / %d strict; |t| <= 0.1: %d / %d; 5x5 %d; area %d' % (
        len(T), sum(abs(t) <= 0.25 for t in T), sum(abs(t) < 0.25 for t in T), sum(abs(t) <= 0.1 for t in T),
        sum(abs(t) < 0.1 for t in T), len(F['grids']['t2t4_axis']) ** 2, F['grids']['area_grid']['nodes_per_axis'] ** 2))
    if fails:
        print('RESULT: FAIL (%d)' % len(fails))
        for f in fails[:20]:
            print('  ' + f)
        return 1
    print('RESULT: PASS')
    return 0

if __name__ == '__main__':
    sys.exit(main())

=====END-EMBED name=sa_verify_pinned_inputs.py=====

=====BEGIN-EMBED name=sa_anchor_validate.py md5=3a11c8f1421d26b882097dbd4e0759d7 bytes=7604 encoding=raw=====
#!/usr/bin/env python3
"""sa_anchor_validate.py -- G-MSCS-A sealed-anchor file validator (staging memo v1, section 4; v2 after the independent
audit: control characters, Unicode separators, and T1-A1 BOM/whitespace now rejected). BLIND BY CONSTRUCTION:
it reports md5, byte count, census, key order and a format verdict per key, and NEVER prints, logs or returns a field
value (not even inside an error message). Intended to be run by the author before sealing, and by either leg only to
confirm the census; the mapper's own masked parse is the read of record.

Usage:  python3 sa_anchor_validate.py ANCHOR_FILE [T1_A1_FILE]
Exit:   0 = every check passed; 1 = at least one check failed; 2 = usage error.

Format (memo section 4.2): UTF-8 without BOM; LF line endings only; no CR, no TAB; exactly one row per line; no blank,
comment or marker lines; the file ends with exactly one LF. A row is  key=value | key=value | ...  with the separator
' | ' (space, bar, space); no leading or trailing bar; no bar anywhere else. Keys in the canonical order below; required
keys exactly once; optional keys at most once, after the required ones, in canonical order."""
import hashlib, math, re, sys

REQUIRED = ['id', 'class', 'delta_def', 'lo', 'hi', 'cl', 'reading', 'geom', 'k_em_max', 'k_t_max', 'src']
OPTIONAL = ['q', 'note']
CANON = REQUIRED + OPTIONAL
FREE_TEXT = {'src', 'note'}                      # the only fields that may hold non-ASCII text; never parsed as numbers
NUM = re.compile(r'^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$')   # ASCII decimal or e-notation only
SEP = ' | '

BAD_UNICODE = {'\u0085', '\u2028', '\u2029', '\ufeff'}
def bad_char(c):
    o = ord(c)
    return (o < 32 and c != '\n') or 127 <= o < 160 or c in BAD_UNICODE

def num_ok(s):
    if not NUM.match(s):
        return False
    try:
        return math.isfinite(float(s))
    except ValueError:
        return False

def check_value(key, val):
    """Return a reason code ('OK' or a failure code). Never echoes the value."""
    if val == '' or val != val.strip():
        return 'EMPTY_OR_PADDED'
    if key not in FREE_TEXT and not all(32 <= ord(c) < 127 for c in val):
        return 'NON_ASCII'            # catches the Unicode minus, superscripts, the multiplication sign, NBSP
    if key == 'class':
        return 'OK' if val == 'spd' else 'CLASS_NOT_READ_BY_THIS_GATE'
    if key == 'delta_def':
        return 'OK' if val == 'tensor_over_EM_minus_1' else 'WRONG_DELTA_DEF'
    if key in ('lo', 'hi'):
        return 'OK' if num_ok(val) else 'NOT_A_PLAIN_NUMBER'
    if key == 'cl':
        if val == 'hard':
            return 'OK'
        return 'OK' if (num_ok(val) and 0.0 < float(val) < 1.0) else 'CL_NOT_IN_(0,1)_OR_hard'
    if key == 'reading':
        return 'OK' if val == 'bound' else ('READING_NOT_MAPPED' if val in ('ceiling', 'margin', 'criterion') else 'UNKNOWN_READING')
    if key == 'geom':
        return 'OK' if val in ('single', 'population') else 'UNKNOWN_GEOM'
    if key in ('k_em_max', 'k_t_max'):
        return 'OK' if (num_ok(val) and float(val) > 0.0) else 'NOT_A_POSITIVE_PLAIN_NUMBER'
    if key == 'q':
        return 'OK' if val in ('phase', 'group') else 'UNKNOWN_Q'
    return 'OK'                        # src, note: free text (bar, CR, LF, TAB already excluded at file level)

def validate(path):
    raw = open(path, 'rb').read()
    ok = True
    print('file: md5 %s  bytes %d' % (hashlib.md5(raw).hexdigest(), len(raw)))
    def fail(msg):
        nonlocal ok
        ok = False
        print('  FAIL ' + msg)
    if raw.startswith(b'\xef\xbb\xbf'):
        fail('BOM present')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        fail('not UTF-8'); return False
    if '\r' in text: fail('CR present (LF line endings only)')
    if '\t' in text: fail('TAB present')
    if any(bad_char(c) for c in text): fail('control character or Unicode line/paragraph separator present (other than the row-ending LF)')
    if not text.endswith('\n'): fail('file does not end with LF')
    if text.endswith('\n\n'): fail('blank line(s) at end of file')
    lines = text[:-1].split('\n') if text.endswith('\n') else text.split('\n')
    if lines == ['']:
        fail('no rows'); return False
    census = {}
    for n, line in enumerate(lines, 1):
        tag = 'row %d' % n
        if line.strip() == '':
            fail(tag + ': blank line'); continue
        if line.startswith('|') or line.rstrip().endswith('|'):
            fail(tag + ': leading or trailing bar')
        fields = line.split(SEP)
        if any('|' in f for f in fields):
            fail(tag + ': SEPARATOR_COLLISION (a bar not in the form " | ")')
        keys, vals = [], {}
        for f in fields:
            if '=' not in f:
                fail(tag + ': field without key=value'); continue
            k, v = f.split('=', 1)
            if k in vals:
                fail(tag + ': duplicate key ' + (k if k in CANON else '<unknown>'))
            if k not in CANON:
                fail(tag + ': unknown key (name withheld)'); continue
            keys.append(k); vals[k] = v
        missing = [k for k in REQUIRED if k not in vals]
        if missing: fail(tag + ': missing required key(s) ' + ','.join(missing))
        order = [k for k in CANON if k in keys]
        if keys != order: fail(tag + ': keys not in canonical order')
        if vals.get('id') != 'SA-%d' % n: fail(tag + ': id is not SA-%d (rows numbered in file order)' % n)
        cls = vals.get('class', '?'); census[cls if cls == 'spd' else 'other'] = census.get(cls if cls == 'spd' else 'other', 0) + 1
        verdicts = {k: check_value(k, vals[k]) for k in keys}
        bad = {k: c for k, c in verdicts.items() if c != 'OK'}
        for k, c in bad.items(): fail('%s: key %s -> %s' % (tag, k, c))
        if 'lo' in vals and 'hi' in vals and verdicts.get('lo') == 'OK' and verdicts.get('hi') == 'OK':
            if not float(vals['lo']) <= float(vals['hi']): fail(tag + ': ORDER (lo must not exceed hi)')
        print('  %s: fields %d  keys-in-order %s  per-key %s' % (tag, len(fields), 'yes' if keys == order else 'NO',
              'all OK' if not bad else '%d failing' % len(bad)))
    print('census: rows %d  per-class %s' % (len(lines), census))
    return ok

def validate_t1a1(path):
    raw = open(path, 'rb').read(); ok = True
    print('T1-A1: md5 %s  bytes %d' % (hashlib.md5(raw).hexdigest(), len(raw)))
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        print('  FAIL not UTF-8'); return False
    if raw.startswith(b'\xef\xbb\xbf'): print('  FAIL BOM present'); ok = False
    if '\r' in text: print('  FAIL CR present'); ok = False
    if any(bad_char(c) for c in text): print('  FAIL control character (TAB included) or Unicode separator present'); ok = False
    if not text.endswith('\n'): print('  FAIL does not end with LF'); ok = False
    pats = [l for l in text.split('\n') if l.strip() and not l.startswith('#')]
    padded = sum(1 for p in pats if p != p.strip())
    if padded: print('  FAIL %d pattern line(s) with leading or trailing whitespace (the scanner would never match them)' % padded); ok = False
    print('  pattern lines %d (values withheld)' % len(pats))
    if not pats: print('  FAIL no pattern lines'); ok = False
    return ok

if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        print(__doc__); sys.exit(2)
    good = validate(sys.argv[1])
    if len(sys.argv) == 3:
        good = validate_t1a1(sys.argv[2]) and good
    print('RESULT: ' + ('PASS' if good else 'FAIL'))
    sys.exit(0 if good else 1)

=====END-EMBED name=sa_anchor_validate.py=====

=====BEGIN-EMBED name=tools/t1/T1_forbidden_G_MSCS_A.txt md5=e274e58ea50b9ed347969e507d2a4f36 bytes=1482 encoding=raw=====
# T1 forbidden-string list — Gate G-MSCS-A (gate-specific), composed at lock, September 29, 2026 (E-SA-7 as elected: "The base 05302210 + the G-MSCS1 stratum").
# Composition: the 36 pattern lines of the G-MSCS2 gate list T1_forbidden_G_MSCS2.txt (md5 be921b8c29f7578e85ed92f1450c1956, 1,695 B) copied VERBATIM and in the same order — stratum 1 the author's base list (T1_base_author_20260919.txt, md5 05302210cc4ceb70553acbe8379e9fc3, 143 B, 11 pattern lines); stratum 2 the G-MSCS1 observational stratum (25 pattern lines). No chat-side stratum (the chat leg composes no anchor-digit pattern). The author's T1-A1 (t1_forbidden_G_MSCS_A_A1.txt) is appended at sealed delivery after the pre-freeze collision scan (memo section 4.6); the effective list is the union.
# Scanner: t1_scan.py (md5 6b86290090a8c84f1b1a0a99ec0bf697): pattern lines only ('#' lines ignored); case-sensitive substring; bare numeric patterns under the contextual numeric rule — a hit counts only when the maximal numeric token containing the match equals the pattern; embedded matches are logged as formatting collisions. Hits are reported by pattern index only.
# Exempt from scanning, for cause: the sealed anchor file and the list files themselves.
Mpc
Gpc
LIGO
170817
299792458
SME
GW1
3.19
0.019
Hz
GW
2.99792458
3e-15
7e-16
3×10⁻¹⁵
7×10⁻¹⁶
3×10^-15
7×10^-16
3 × 10^-15
7 × 10^-16
m/s
km/s
LVC
Virgo
KAGRA
Fermi
GRB
GWTC
Haegel
2210.04481
ApJL 848
848, L13
k_(I)
k_(V)
k_(E)
k_(B)

=====END-EMBED name=tools/t1/T1_forbidden_G_MSCS_A.txt=====

=====BEGIN-EMBED name=tools/t1/T1_base_author_20260919.txt md5=05302210cc4ceb70553acbe8379e9fc3 bytes=143 encoding=raw=====
# T1 forbidden-string list, base stratum
# Recovered from G-2a-L1 dispatch (0c5588ee)
#
Mpc
Gpc
LIGO
170817
299792458
SME
GW1
3.19
0.019
Hz
GW

=====END-EMBED name=tools/t1/T1_base_author_20260919.txt=====

=====BEGIN-EMBED name=tools/t1/t1_scan.py md5=6b86290090a8c84f1b1a0a99ec0bf697 bytes=1967 encoding=raw=====
#!/usr/bin/env python3
"""t1_scan.py — T1 forbidden-string scanner, G-MSCS1 (frozen with the gate list).
Rules: pattern lines only ('#' comment lines and blank lines ignored); case-sensitive substring;
bare numeric patterns (regex ^[0-9.e+\-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+$) under the contextual numeric rule:
a match counts only if the maximal token of numeric characters containing it equals the pattern;
otherwise it is logged as a formatting COLLISION (not a hit). Hits are reported by pattern INDEX only.
Usage: t1_scan.py LIST FILE [FILE...]   -> exit 0 clean, 1 hit, 2 usage.
"""
import re, sys
NUMCHARS = set("0123456789.eE+-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
def load(list_path):
    pats = [l.rstrip("\n") for l in open(list_path, encoding="utf-8")]
    return [p for p in pats if p.strip() and not p.startswith("#")]
def is_numeric(p): return all(c in NUMCHARS for c in p)
def scan_text(text, pats):
    hits, collisions = [], []
    for i, p in enumerate(pats):
        start = 0
        while True:
            j = text.find(p, start)
            if j < 0: break
            if is_numeric(p):
                a = j
                while a > 0 and text[a-1] in NUMCHARS and text[a-1] != " ": a -= 1
                b = j + len(p)
                while b < len(text) and text[b] in NUMCHARS and text[b] != " ": b += 1
                tok = text[a:b]
                (hits if tok == p else collisions).append((i, j))
            else:
                hits.append((i, j))
            start = j + 1
    return hits, collisions
def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(2)
    pats = load(sys.argv[1]); rc = 0
    for f in sys.argv[2:]:
        text = open(f, "rb").read().decode("utf-8", "replace")
        hits, coll = scan_text(text, pats)
        print(f"{f}: {'HIT' if hits else 'CLEAN'}  hits={[i for i,_ in hits]}  numeric_collisions={len(coll)}")
        if hits: rc = 1
    sys.exit(rc)
if __name__ == "__main__": main()

=====END-EMBED name=tools/t1/t1_scan.py=====

=====BEGIN-EMBED name=tools/t1/t1_forbidden_G_MSCS_A_A1.txt md5=3b753b3a371a162fc2ab21b9eed51bd5 bytes=1030 encoding=raw=====
# T1-A1 for G-MSCS-A -- numeric renderings written by sa_t1a1_build.py (values not printed by the tool)
-3*10^-15
-3.0*10^-15
-3.00*10^-15
-3.00x10^-15
-3.00×10^-15
-3.00×10⁻¹⁵
-3.0x10^-15
-3.0×10^-15
-3.0×10⁻¹⁵
-3x10^-15
-3×10^-15
-3×10⁻¹⁵
2*10^-5
2.0*10^-5
2.00*10^-5
2.00x10^-5
2.00×10^-5
2.00×10⁻⁵
2.0x10^-5
2.0×10^-5
2.0×10⁻⁵
2x10^-5
2×10^-5
2×10⁻⁵
3*10^-15
3.0*10^-15
3.00*10^-15
3.00x10^-15
3.00×10^-15
3.00×10⁻¹⁵
3.0x10^-15
3.0×10^-15
3.0×10⁻¹⁵
3x10^-15
3×10^-15
3×10⁻¹⁵
5*10^12
5.0*10^12
5.00*10^12
5.00x10^12
5.00×10^12
5.00×10¹²
5.0x10^12
5.0×10^12
5.0×10¹²
5x10^12
5×10^12
5×10¹²
7*10^-16
7.0*10^-16
7.00*10^-16
7.00x10^-16
7.00×10^-16
7.00×10⁻¹⁶
7.0x10^-16
7.0×10^-16
7.0×10⁻¹⁶
7x10^-16
7×10^-16
7×10⁻¹⁶
−3.00e-15
−3.00×10⁻¹⁵
−3.0e-15
−3.0×10⁻¹⁵
−3e-15
−3×10⁻¹⁵
# --- identifiers from src: the author appends each catalog / event / collaboration / instrument identifier below ---
GW170817
ApJL

=====END-EMBED name=tools/t1/t1_forbidden_G_MSCS_A_A1.txt=====

=====BEGIN-EMBED name=inputs/gmscs2_gate/g_mscs2_chatleg_checkpoint.json md5=1c5b6b59829d2a6b9ae2b1a7a016832d bytes=31575 encoding=raw=====
{
 "gate": "G-MSCS2",
 "leg": "chat",
 "instrument": "g_mscs2_chatleg.py",
 "instrument_md5": "f277580ddf0b4da9734d11edb009c54b",
 "memo_lock_md5": "efdcabdcd937cda4acb64f941dc4bb2b",
 "memo_lock_bytes": 46053,
 "ledger_base_md5": "f36bbdb04104008783f2763f70fb916f",
 "t1_list_md5": "be921b8c29f7578e85ed92f1450c1956",
 "x1_md5": "200e7a8b775577564369c6924d38a84c",
 "x6_chat_md5": "c04c0b8ea34cfe60f231aa06828e6ce4",
 "x6_cc_md5": "249e11dd53c4cb82f302b15d3c94c337",
 "utc": "2026-09-26T16:02:10.372438+00:00",
 "elections": {
  "E-MS2-1": "a+b",
  "E-MS2-2": "a",
  "E-MS2-2b": "a+b",
  "E-MS2-2c": "001+111",
  "E-MS2-3": "a",
  "E-MS2-4": "a",
  "E-MS2-5": "a",
  "E-MS2-6": "a",
  "E-MS2-7": "05302210+MSCS1stratum",
  "E-MS2-8": "a"
 },
 "t1_scan": {
  "instrument": "CLEAN",
  "memo": "CLEAN"
 },
 "quadrature": {
  "n_theta": 64,
  "n_phi": 128,
  "so3_grid": [
   16,
   10,
   16
  ],
  "n_grid": [
   12,
   24
  ]
 },
 "t4_grid": [
  -0.5,
  -0.25,
  -0.1,
  -0.05,
  -0.02,
  0.0,
  0.02,
  0.05,
  0.1,
  0.25,
  0.5,
  1.0
 ],
 "t2t4_grid": [
  -0.25,
  -0.125,
  0.0,
  0.125,
  0.25
 ],
 "phase0": {
  "PIN-XTAL": {
   "worst_rel": 0.0,
   "passed": true
  },
  "PIN-VRH0": {
   "worst_rel": 0.0,
   "passed": true
  },
  "PIN-HS0": {
   "worst_rel": 0.0,
   "passed": true
  },
  "PIN-K2": {
   "worst_rel_hex_kappa2": 1.3929675245859295e-12,
   "worst_abs_cubic_kappa2": 2.1553376966476035e-15,
   "kappa2_E2_recomputed": {
    "hex_step|a": -0.0014394617694987043,
    "hex_step|b": -0.0014387027187499476,
    "hex_gem8|a": -0.0018956484826701352,
    "hex_gem8|b": -0.0018961374665243645,
    "cubic_step|001": -4.551387048761626e-16,
    "cubic_step|111": -1.6739143857147652e-16,
    "cubic_gem8|001": -2.1553376966476035e-15,
    "cubic_gem8|111": -1.6019775691385888e-15
   },
   "passed": true
  },
  "F-CTRL-ISO": {
   "worst_abs": 4.440892098500626e-16,
   "passed": true
  },
  "F-CTRL-SO3": {
   "dev_from_0p4": 4.996003610813204e-16,
   "r_agg_0_abs": 0.0,
   "passed": true
  },
  "F-CTRL-POS": {
   "min_odf_weight": 0.39502706178551494,
   "passed": true
  },
  "F-CTRL-L2NULL": {
   "worst_abs": 5.849908933676171e-14,
   "passed": true
  },
  "F-CTRL-L4EXHAUST": {
   "worst_rel_tensor": 4.325772878954588e-14,
   "worst_abs_r_agg": 4.440892098500626e-16,
   "passed": true
  },
  "F-CTRL-C4": {
   "worst_rel_closed_form": 2.5186926550099605e-14,
   "worst_rel_affine": 4.0740437216673334e-14,
   "h0_effect_rel": 2.3021584638627248e-14,
   "passed": true
  },
  "F-CTRL-MARG": {
   "worst_abs": 8.326672684688674e-16,
   "passed": true
  },
  "F-CTRL-TEX4": {
   "r_agg_t1_abs": 0.0004118326557733809,
   "passed": true
  },
  "F-CTRL-QUAD": {
   "doubling_residual": 2.2603428860704315e-14,
   "k_sphere_doubling": 2.220446049250313e-16,
   "so3_doubling": 2.2603428860704315e-14,
   "passed": true
  }
 },
 "phase0_witness": {
  "single_crystal": {
   "hex_step|a": {
    "v_EM": 8.498926630589143,
    "v_S2E2": 8.261235391127114,
    "v_S2h": 8.489468358289109,
    "r_xtal_E2": -0.02796720689487253,
    "r_xtal_h": -0.001112878450555299,
    "lambda_mean": 0.004808575724022838,
    "lambda_max": 0.03353758299774612,
    "lambda_max_branch": "qSV"
   },
   "hex_step|b": {
    "v_EM": 8.49913805976472,
    "v_S2E2": 8.261611551328288,
    "v_S2h": 8.489680210591468,
    "r_xtal_E2": -0.027947129081346778,
    "r_xtal_h": -0.0011128009813166084,
    "lambda_mean": 0.004808600428348514,
    "lambda_max": 0.033534547685208825,
    "lambda_max_branch": "qSV"
   },
   "hex_gem8|a": {
    "v_EM": 10.167571147427779,
    "v_S2E2": 9.767584615679638,
    "v_S2h": 10.154202161568202,
    "r_xtal_E2": -0.039339437703303504,
    "r_xtal_h": -0.0013148652382883874,
    "lambda_mean": 0.0049537696180639535,
    "lambda_max": 0.03513301845903744,
    "lambda_max_branch": "qSV"
   },
   "hex_gem8|b": {
    "v_EM": 10.167412388965342,
    "v_S2E2": 9.767300819096656,
    "v_S2h": 10.154042977980577,
    "r_xtal_E2": -0.03935234989611769,
    "r_xtal_h": -0.0013149275816995987,
    "lambda_mean": 0.004953789932329422,
    "lambda_max": 0.035133018459037525,
    "lambda_max_branch": "qSV"
   },
   "cubic_step|001": {
    "v_EM": 8.028124827494889,
    "v_S2E2": 7.889264216956222,
    "v_S2h": 8.015951162831872,
    "r_xtal_E2": -0.0172967677412158,
    "r_xtal_h": -0.001516377102324551,
    "lambda_mean": 0.0083923190288783,
    "lambda_max": 0.03870069334173741,
    "lambda_max_branch": "qT2"
   },
   "cubic_step|111": {
    "v_EM": 8.028124827494889,
    "v_S2E2": 8.120698567854001,
    "v_S2h": 8.015951162831872,
    "r_xtal_E2": 0.01153117849414409,
    "r_xtal_h": -0.001516377102324551,
    "lambda_mean": 0.0083923190288783,
    "lambda_max": 0.03870069334173741,
    "lambda_max_branch": "qT2"
   },
   "cubic_gem8|001": {
    "v_EM": 9.72117101507821,
    "v_S2E2": 9.5185580718033,
    "v_S2h": 9.703234472528251,
    "r_xtal_E2": -0.020842442022740326,
    "r_xtal_h": -0.0018451010194284745,
    "lambda_mean": 0.0093105038596528,
    "lambda_max": 0.043292701954120015,
    "lambda_max_branch": "qT2"
   },
   "cubic_gem8|111": {
    "v_EM": 9.72117101507821,
    "v_S2E2": 9.856246310594818,
    "v_S2h": 9.703234472528251,
    "r_xtal_E2": 0.01389496134849355,
    "r_xtal_h": -0.0018451010194284745,
    "lambda_mean": 0.0093105038596528,
    "lambda_max": 0.043292701954120015,
    "lambda_max_branch": "qT2"
   }
  },
  "vT_t0": {
   "hex_step|a": {
    "V": 8.547779438739228,
    "R": 8.288341029983927,
    "H": 8.419059637591603,
    "HSlo": 8.390859731728247,
    "HShi": 8.424582419403457
   },
   "hex_step|b": {
    "V": 8.547982997955295,
    "R": 8.288576029181627,
    "H": 8.419278648579612,
    "HSlo": 8.391084746837947,
    "HShi": 8.424803257723832
   },
   "hex_gem8|a": {
    "V": 10.248997674569596,
    "R": 9.830076336505329,
    "H": 10.041721817369147,
    "HSlo": 9.990913001571156,
    "HShi": 10.052797754949037
   },
   "hex_gem8|b": {
    "V": 10.248847414872234,
    "R": 9.82989031256601,
    "H": 10.041554085160632,
    "HSlo": 9.99073982971986,
    "HShi": 10.052629959294945
   },
   "cubic_step|001": {
    "V": 8.115794477437195,
    "R": 7.468877341686607,
    "H": 7.799046375844923,
    "HSlo": 7.758614490211087,
    "HShi": 7.867953005904775
   },
   "cubic_step|111": {
    "V": 8.115794477437195,
    "R": 7.468877341686607,
    "H": 7.799046375844923,
    "HSlo": 7.758614490211087,
    "HShi": 7.867953005904775
   },
   "cubic_gem8|001": {
    "V": 9.87249208660102,
    "R": 8.706771527831352,
    "H": 9.307899076533179,
    "HSlo": 9.211721064370861,
    "HShi": 9.456854984588738
   },
   "cubic_gem8|111": {
    "V": 9.87249208660102,
    "R": 8.706771527831352,
    "H": 9.307899076533179,
    "HSlo": 9.211721064370861,
    "HShi": 9.456854984588738
   }
  },
  "hs_ref": {
   "hex_step": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   },
   "hex_gem8": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   },
   "cubic_step": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   },
   "cubic_gem8": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   }
  }
 },
 "phase2": {
  "hex_step|a": {
   "r_agg_E2_VRH": [
    4.0075112154536185e-05,
    1.0021876255539297e-05,
    1.6038160919329414e-06,
    4.009811214178427e-07,
    6.415961073535925e-08,
    0.0,
    6.416315367907544e-08,
    4.0103648424327787e-07,
    1.6042590029741177e-06,
    1.0028797479577634e-05,
    4.013050311080235e-05,
    0.00016065650935481735
   ],
   "r_agg_h_VRH": [
    -1.8659710554480569e-06,
    -4.678262344182116e-07,
    -7.498399878791417e-08,
    -1.875714272792095e-08,
    -3.0022188068912214e-09,
    0.0,
    -3.0036605425109997e-09,
    -1.8779669153090595e-08,
    -7.516421407505192e-08,
    -4.7064235364491225e-07,
    -1.8885071644270113e-06,
    -7.604051808440815e-06
   ],
   "r_agg_E2_HS": [
    3.992922854578751e-05,
    9.987793137877787e-06,
    1.5985754207026304e-06,
    3.9968797649336807e-07,
    6.395431473293911e-08,
    0.0,
    6.395996976493734e-08,
    3.9977633781163036e-07,
    1.5992823094723718e-06,
    9.998838376379382e-06,
    4.0017593226249204e-05,
    0.00016024951313786673
   ],
   "r_agg_E2_V": [
    4.5906615393498384e-05,
    1.1471262962414741e-05,
    1.8349039123677358e-06,
    4.586852686561116e-07,
    7.338576546445097e-08,
    0.0,
    7.33806317931851e-08,
    4.58605053044181e-07,
    1.834262182365265e-06,
    1.146123554107703e-05,
    4.582638479200263e-05,
    0.0001831689574216533
   ],
   "r_agg_E2_R": [
    3.3875297374086344e-05,
    8.480578136849104e-06,
    1.3580482476349687e-06,
    3.396095238361596e-07,
    5.434692451622425e-08,
    -2.220446049250313e-16,
    5.4359510670565214e-08,
    3.3980618208140356e-07,
    1.3596215249211951e-06,
    8.505161953609175e-06,
    3.4072006643626196e-05,
    0.0001367168344819092
   ],
   "lambda_mean_t4": [
    9.380371358233803e-06,
    2.3485575382655725e-06,
    3.76118153700876e-07,
    9.405930416680826e-08,
    1.50523726728794e-08,
    1.8167378864124917e-30,
    1.505624900178596e-08,
    9.411987210373284e-08,
    3.766027057532789e-07,
    2.356129599974271e-06,
    9.440974601830511e-06,
    3.790633597378362e-05
   ],
   "S4_E2": -2.2136167800606602e-13,
   "S4_h": 7.665423084547844e-14,
   "kappa44_E2": 0.00016040534614367987,
   "kappa44_h": -7.507739661972004e-06,
   "kappa444_E2": 2.214826941714643e-07,
   "kappa44_E2_HS": 0.000159893047684377,
   "halving_dev_kappa44": 1.6055695365075912e-09,
   "kappa44_E2_window0p1": 0.00016040374057414337,
   "fit_residual": 7.917855904914435e-12,
   "biref_b1_VRH": 0.01624085410723511,
   "vT_VRH": 8.419059637591603,
   "vT_HS_lo": 8.390859731728247,
   "vT_HS_hi": 8.424582419403457,
   "quadform": {
    "kappa22": -0.0014394693020032903,
    "kappa24": -1.2488790730491887e-08,
    "kappa44": 0.00016039903763945317,
    "residual": 3.3538422169011824e-10
   },
   "hs_ref": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   }
  },
  "hex_step|b": {
   "r_agg_E2_VRH": [
    4.007742972289563e-05,
    1.0022457102243365e-05,
    1.6039091734754152e-06,
    4.010044041269367e-07,
    6.416333730996371e-08,
    0.0,
    6.416688203003673e-08,
    4.0105979270954606e-07,
    1.6043522874653604e-06,
    1.0029381496190481e-05,
    4.0132846051976756e-05,
    0.0001606659405379851
   ],
   "r_agg_h_VRH": [
    -1.8662871319463648e-06,
    -4.679056785361624e-07,
    -7.499675247490956e-08,
    -1.8760334619116747e-08,
    -3.0027293984602466e-09,
    0.0,
    -3.004171911236142e-09,
    -1.878286859380296e-08,
    -7.517702727000142e-08,
    -4.70722723466821e-07,
    -1.8888306501096963e-06,
    -7.605363090079642e-06
   ],
   "r_agg_E2_HS": [
    3.9931605506859924e-05,
    9.988388290027572e-06,
    1.5986707333492944e-06,
    3.9971181187148375e-07,
    6.395812945925172e-08,
    0.0,
    6.396378560147298e-08,
    3.9980018806673456e-07,
    1.599377740690855e-06,
    9.999435379270949e-06,
    4.001998499925108e-05,
    0.00016025911078099142
   ],
   "r_agg_E2_V": [
    4.5906764786884935e-05,
    1.1471300246368443e-05,
    1.834909872044932e-06,
    4.586867581313214e-07,
    7.338600394035666e-08,
    0.0,
    7.338087026909079e-08,
    4.586065414091678e-07,
    1.8342681347149892e-06,
    1.1461272707791181e-05,
    4.58265332441421e-05,
    0.00018316954966857146
   ],
   "r_agg_E2_R": [
    3.387997594805903e-05,
    8.481750945144029e-06,
    1.358236212167796e-06,
    3.396565417812525e-07,
    5.435444982992976e-08,
    -2.220446049250313e-16,
    5.43670393149398e-08,
    3.3985325398333543e-07,
    1.3598099228850913e-06,
    8.506341536929085e-06,
    3.407673944177958e-05,
    0.0001367358889383663
   ],
   "lambda_mean_t4": [
    9.382285878067786e-06,
    2.3490375675855626e-06,
    3.761951017486418e-07,
    9.407855350433293e-08,
    1.50554537652803e-08,
    2.8493087979525507e-30,
    1.5059331708544535e-08,
    9.41391466685843e-08,
    3.766798556224593e-07,
    2.356612783412843e-06,
    9.442914373552677e-06,
    3.7914157412036276e-05
   ],
   "S4_E2": -2.1990268388075987e-13,
   "S4_h": 7.485871681214715e-14,
   "kappa44_E2": 0.00016041466503408588,
   "kappa44_h": -7.509018168894417e-06,
   "kappa444_E2": 2.2158410762808975e-07,
   "kappa44_E2_HS": 0.00015990258492339606,
   "halving_dev_kappa44": 1.6061616350891272e-09,
   "kappa44_E2_window0p1": 0.0001604130588724508,
   "fit_residual": 7.920774530058612e-12,
   "biref_b1_VRH": 0.016241797577228063,
   "vT_VRH": 8.419278648579612,
   "vT_HS_lo": 8.391084746837947,
   "vT_HS_hi": 8.424803257723832,
   "quadform": {
    "kappa22": -0.001438710247883606,
    "kappa24": -1.2484615083901236e-08,
    "kappa44": 0.00016040835823465525,
    "residual": 3.352089161397567e-10
   },
   "hs_ref": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   }
  },
  "hex_gem8|a": {
   "r_agg_E2_VRH": [
    4.48512154973546e-05,
    1.1215782710127797e-05,
    1.7948340194084977e-06,
    4.4873519322585764e-07,
    7.180022998376501e-08,
    -2.220446049250313e-16,
    7.180373828852282e-08,
    4.4879001181996614e-07,
    1.79527257415657e-06,
    1.1222636018715093e-05,
    4.490606733864588e-05,
    0.00017976326080337834
   ],
   "r_agg_h_VRH": [
    -1.9274619713627317e-06,
    -4.832185266367972e-07,
    -7.744891550309774e-08,
    -1.937356264303247e-08,
    -3.1008647871644257e-09,
    0.0,
    -3.102331946891468e-09,
    -1.9396488082357166e-08,
    -7.763232257040897e-08,
    -4.860845420617821e-07,
    -1.9503980948076816e-06,
    -7.852781449102508e-06
   ],
   "r_agg_E2_HS": [
    4.468026881743192e-05,
    1.1176594882256197e-05,
    1.7888838452773115e-06,
    4.472734345117857e-07,
    7.156879000547178e-08,
    -2.220446049250313e-16,
    7.157551462633194e-08,
    4.473785086833715e-07,
    1.7897244393161316e-06,
    1.118972928826345e-05,
    4.478534775564924e-05,
    0.00017935416817671523
   ],
   "r_agg_E2_V": [
    5.303875172746331e-05,
    1.3252550826958753e-05,
    2.119752434470712e-06,
    5.298846901258258e-07,
    8.477646917803838e-08,
    0.0,
    8.476974855398112e-08,
    5.297796816794431e-07,
    2.118912363124892e-06,
    1.3239424036859404e-05,
    5.2933718038605804e-05,
    0.00021156107694930704
   ],
   "r_agg_E2_R": [
    3.595565596703487e-05,
    9.00219195942853e-06,
    1.4416580706999582e-06,
    3.6052483665116597e-07,
    5.769461730587011e-08,
    2.220446049250313e-16,
    5.770887079314946e-08,
    3.6074754627968275e-07,
    1.4434397612728134e-06,
    9.030032598777993e-06,
    3.617843036884949e-05,
    0.00014520159111719444
   ],
   "lambda_mean_t4": [
    8.586544971336659e-06,
    2.149767718561195e-06,
    3.4427901847744266e-07,
    8.609675774057867e-08,
    1.3778098793752491e-08,
    2.8730624380705302e-30,
    1.3781618408431266e-08,
    8.615175202016012e-08,
    3.447189812864189e-07,
    2.156643075108242e-06,
    8.64157462489947e-06,
    3.469662301937302e-05
   ],
   "S4_E2": -2.652046374551464e-13,
   "S4_h": 8.394408199844183e-14,
   "kappa44_E2": 0.00017950729579484115,
   "kappa44_h": -7.754414849489288e-06,
   "kappa444_E2": 2.1931009732824822e-07,
   "kappa44_E2_HS": 0.0001789305885725744,
   "halving_dev_kappa44": 1.9836269332293953e-09,
   "kappa44_E2_window0p1": 0.00017950531216790792,
   "fit_residual": 9.782244930805078e-12,
   "biref_b1_VRH": 0.01817488251117739,
   "vT_VRH": 10.041721817369147,
   "vT_HS_lo": 9.990913001571156,
   "vT_HS_hi": 10.052797754949037,
   "quadform": {
    "kappa22": -0.0018956599069468293,
    "kappa24": -1.837213417851943e-08,
    "kappa44": 0.00017949842202586976,
    "residual": 5.234501973994977e-10
   },
   "hs_ref": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   }
  },
  "hex_gem8|b": {
   "r_agg_E2_VRH": [
    4.484977886543007e-05,
    1.121542248339047e-05,
    1.7947762760428532e-06,
    4.4872074855817345e-07,
    7.179791761124932e-08,
    0.0,
    7.180142480578411e-08,
    4.4877554827849053e-07,
    1.795214681576951e-06,
    1.1222273463173948e-05,
    4.490461206385632e-05,
    0.0001797573959907428
   ],
   "r_agg_h_VRH": [
    -1.92726942582766e-06,
    -4.831701241325703e-07,
    -7.744114405294766e-08,
    -1.9371617421271026e-08,
    -3.1005531475614134e-09,
    0.0,
    -3.102020196266153e-09,
    -1.9394538197659017e-08,
    -7.762451403880988e-08,
    -4.860355559133112e-07,
    -1.9502008778982116e-06,
    -7.851981527973173e-06
   ],
   "r_agg_E2_HS": [
    4.467880939684754e-05,
    1.117622939106333e-05,
    1.7888253052156244e-06,
    4.4725879444484917e-07,
    7.156644721284522e-08,
    -3.3306690738754696e-16,
    7.157317138961616e-08,
    4.473638579582939e-07,
    1.7896658164318069e-06,
    1.1189362505659162e-05,
    4.4783877998222366e-05,
    0.00017934826780519053
   ],
   "r_agg_E2_V": [
    5.303886886287579e-05,
    1.3252580101541511e-05,
    2.1197571176134744e-06,
    5.298858605229384e-07,
    8.477665636164033e-08,
    -2.220446049250313e-16,
    8.476993573758307e-08,
    5.297808522986003e-07,
    2.118917045379476e-06,
    1.3239453297675396e-05,
    5.293383506255189e-05,
    0.00021156154497359303
   ],
   "r_agg_E2_R": [
    3.5952455723853305e-05,
    9.001389598140008e-06,
    1.4415294635750087e-06,
    3.604926657185814e-07,
    5.7689468313526504e-08,
    -2.220446049250313e-16,
    5.770371891422599e-08,
    3.607153351570247e-07,
    1.4433108375122572e-06,
    9.029225293666343e-06,
    3.6175190557319326e-05,
    0.00014518854130995962
   ],
   "lambda_mean_t4": [
    8.585494956969248e-06,
    2.1495044120961677e-06,
    3.442368068742277e-07,
    8.60861977268715e-08,
    1.3776408500080999e-08,
    1.2842490776280975e-31,
    1.3779927181871647e-08,
    8.614117743311946e-08,
    3.446766530827854e-07,
    2.1563779463223537e-06,
    8.640510019776536e-06,
    3.4692328181093574e-05
   ],
   "S4_E2": -2.664544112656851e-13,
   "S4_h": 8.256781483484296e-14,
   "kappa44_E2": 0.00017950151354905876,
   "kappa44_h": -7.753635743144201e-06,
   "kappa444_E2": 2.1923559565364329e-07,
   "kappa44_E2_HS": 0.00017892473038334653,
   "halving_dev_kappa44": 1.9831700693261328e-09,
   "kappa44_E2_window0p1": 0.00017949953037898944,
   "fit_residual": 9.779989255161774e-12,
   "biref_b1_VRH": 0.018174297109340813,
   "vT_VRH": 10.041554085160632,
   "vT_HS_lo": 9.99073982971986,
   "vT_HS_hi": 10.052629959294945,
   "quadform": {
    "kappa22": -0.0018961488929936498,
    "kappa24": -1.8376074990497388e-08,
    "kappa44": 0.00017949263950353062,
    "residual": 5.235878076926172e-10
   },
   "hs_ref": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   }
  },
  "cubic_step|001": {
   "r_agg_E2_VRH": [
    -9.39538922326566e-05,
    -2.3438263274333515e-05,
    -3.74577545780852e-06,
    -9.361008704855678e-07,
    -1.497439410247381e-07,
    0.0,
    -1.497018550233875e-07,
    -9.354432559671721e-07,
    -3.7405139442503454e-06,
    -2.3355986619622016e-05,
    -9.329380310130198e-05,
    -0.0003723937335883276
   ],
   "r_agg_h_VRH": [
    -9.68846050775074e-06,
    -2.397505487583551e-06,
    -3.8144366332204527e-07,
    -9.518939547703553e-08,
    -1.5214148607611833e-08,
    2.220446049250313e-16,
    -1.5192968327859546e-08,
    -9.485844321144299e-08,
    -3.787956872614018e-07,
    -2.3560916755371863e-06,
    -9.356026678397633e-06,
    -3.698437991406234e-05
   ],
   "r_agg_E2_HS": [
    -9.763423144693029e-05,
    -2.4368267510732622e-05,
    -3.895110956775305e-06,
    -9.734623724888536e-07,
    -1.5572379152839488e-07,
    -1.1102230246251565e-16,
    -1.5568364131191004e-07,
    -9.72835024426466e-07,
    -3.890092109437582e-06,
    -2.428984143432178e-05,
    -9.700663450318281e-05,
    -0.00038683591265264994
   ],
   "r_agg_E2_V": [
    -8.656972747833613e-05,
    -2.165779263818557e-05,
    -3.4668497381762364e-06,
    -8.668513868936856e-07,
    -1.3870976867114138e-07,
    -2.220446049250313e-16,
    -1.3872807247405916e-07,
    -8.671373886715017e-07,
    -3.4691377971407533e-06,
    -2.1693548558410214e-05,
    -8.685591781631974e-05,
    -0.0003481608292099647
   ],
   "r_agg_E2_R": [
    -0.00010266089551069779,
    -2.5539698595644644e-05,
    -4.075082313370615e-06,
    -1.0178631776325275e-06,
    -1.62772200718031e-07,
    0.0,
    -1.626590514502979e-07,
    -1.0160951826598819e-06,
    -4.060937358718597e-06,
    -2.5318574635946334e-05,
    -0.00010088878284708613,
    -0.00040089811455568114
   ],
   "lambda_mean_t4": [
    4.609149288923567e-05,
    1.1441973694575324e-05,
    1.8238333906427962e-06,
    4.5542048818170287e-07,
    7.28169924946495e-08,
    4.258392291069694e-32,
    7.275150651909723e-08,
    4.5439722332712426e-07,
    1.8156459438817009e-06,
    1.131389946897127e-05,
    4.506273110522298e-05,
    0.00017918241978267293
   ],
   "S4_E2": -1.9549678946260598e-11,
   "S4_h": -1.1694898610377518e-11,
   "kappa44_E2": -0.0003743529418175674,
   "kappa44_h": -3.8028327673460484e-05,
   "kappa444_E2": 2.633164231609963e-06,
   "kappa44_E2_HS": -0.00038926474535513255,
   "halving_dev_kappa44": 3.8814126843849956e-08,
   "kappa44_E2_window0p1": -0.00037431412769072355,
   "fit_residual": 1.9141190676384054e-10,
   "biref_b1_VRH": -0.03789870339598654,
   "vT_VRH": 7.799046375844923,
   "vT_HS_lo": 7.758614490211087,
   "vT_HS_hi": 7.867953005904775,
   "quadform": {
    "kappa22": 4.48191107636109e-09,
    "kappa24": 1.974043374986076e-07,
    "kappa44": -0.00037435455939106166,
    "residual": 2.199041542390919e-09
   },
   "hs_ref": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   }
  },
  "cubic_step|111": {
   "r_agg_E2_VRH": [
    6.263592815525243e-05,
    1.5625508849481662e-05,
    2.4971836385390134e-06,
    6.240672469903785e-07,
    9.982929394247719e-08,
    0.0,
    9.980123660824347e-08,
    6.236288374594778e-07,
    2.493675963277653e-06,
    1.5570657746266647e-05,
    6.21958687341273e-05,
    0.0002482624890589591
   ],
   "r_agg_h_VRH": [
    -9.68846050775074e-06,
    -2.397505487583551e-06,
    -3.8144366332204527e-07,
    -9.518939547703553e-08,
    -1.5214148607611833e-08,
    2.220446049250313e-16,
    -1.5192968327859546e-08,
    -9.485844321144299e-08,
    -3.787956872614018e-07,
    -2.3560916755371863e-06,
    -9.356026678397633e-06,
    -3.698437991406234e-05
   ],
   "r_agg_E2_HS": [
    6.508948763128686e-05,
    1.6245511674117807e-05,
    2.5967406376281588e-06,
    6.489749149185542e-07,
    1.0381586101892992e-07,
    -1.1102230246251565e-16,
    1.0378909398589542e-07,
    6.48556682580903e-07,
    2.5933947396250545e-06,
    1.619322762280717e-05,
    6.467108966878854e-05,
    0.000257890608435174
   ],
   "r_agg_E2_V": [
    5.7713151652150074e-05,
    1.4438528425309016e-05,
    2.3112331588581725e-06,
    5.779009244477606e-07,
    9.247317889204965e-08,
    -2.220446049250313e-16,
    9.24853815753579e-08,
    5.780915923736529e-07,
    2.3127585315751986e-06,
    1.4462365705680824e-05,
    5.790394521065778e-05,
    0.00023210721947308777
   ],
   "r_agg_E2_R": [
    6.844059700705785e-05,
    1.7026465730429763e-05,
    2.7167215423951063e-06,
    6.785754516069886e-07,
    1.0851480047868733e-07,
    0.0,
    1.0843936770754681e-07,
    6.773967884399212e-07,
    2.7072915724790647e-06,
    1.687904975722354e-05,
    6.725918856465007e-05,
    0.0002672654097037874
   ],
   "lambda_mean_t4": [
    4.609149288923567e-05,
    1.1441973694575324e-05,
    1.8238333906427962e-06,
    4.5542048818170287e-07,
    7.28169924946495e-08,
    4.258392291069694e-32,
    7.275150651909723e-08,
    4.5439722332712426e-07,
    1.8156459438817009e-06,
    1.131389946897127e-05,
    4.506273110522298e-05,
    0.00017918241978267293
   ],
   "S4_E2": 1.3035416405833344e-11,
   "S4_h": -1.1694898610377518e-11,
   "kappa44_E2": 0.00024956862787724117,
   "kappa44_h": -3.8028327673460484e-05,
   "kappa444_E2": -1.7554428600870769e-06,
   "kappa44_E2_HS": 0.00025950983023805826,
   "halving_dev_kappa44": 2.58760610979741e-08,
   "kappa44_E2_window0p1": 0.0002495427518161432,
   "fit_residual": 1.276078223066598e-10,
   "biref_b1_VRH": -0.03789870339598654,
   "vT_VRH": 7.799046375844923,
   "vT_HS_lo": 7.758614490211087,
   "vT_HS_hi": 7.867953005904775,
   "quadform": {
    "kappa22": -2.98793883027198e-09,
    "kappa24": 1.9740433870651724e-07,
    "kappa44": 0.00024956970625745204,
    "residual": 2.1873014049153484e-09
   },
   "hs_ref": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   }
  },
  "cubic_gem8|001": {
   "r_agg_E2_VRH": [
    -0.00011285904498181676,
    -2.813923524602746e-05,
    -4.495877947818805e-06,
    -1.1234705115104049e-06,
    -1.7970867816075042e-07,
    0.0,
    -1.796480421090152e-07,
    -1.1225230265310415e-06,
    -4.488296764137978e-06,
    -2.8020636270609245e-05,
    -0.00011190615454603758,
    -0.0004466673069934979
   ],
   "r_agg_h_VRH": [
    -1.1590815615636352e-05,
    -2.86299115281885e-06,
    -4.5509719270864224e-07,
    -1.1353983042639015e-07,
    -1.8144388991281346e-08,
    0.0,
    -1.8115683841912755e-08,
    -1.1309128233882859e-07,
    -4.515080809230909e-07,
    -2.806831356338968e-06,
    -1.1139242344304634e-05,
    -4.4028971179166376e-05
   ],
   "r_agg_E2_HS": [
    -0.00011966081632819314,
    -2.9853890737618904e-05,
    -4.770848111346204e-06,
    -1.1922353594373547e-06,
    -1.907120693589448e-07,
    0.0,
    -1.9065148326724568e-07,
    -1.1912887032394792e-06,
    -4.763274711439003e-06,
    -2.9735539746722495e-05,
    -0.00011871353319847788,
    -0.000473085445427901
   ],
   "r_agg_E2_V": [
    -0.00010259742095253266,
    -2.5669950862616808e-05,
    -4.109380245087557e-06,
    -1.027536250419736e-06,
    -1.644244953524776e-07,
    -2.220446049250313e-16,
    -1.6444982064989233e-07,
    -1.0279319617723104e-06,
    -4.112546025059061e-06,
    -2.571942578966091e-05,
    -0.00010299349550790815,
    -0.0004130383775181601
   ],
   "r_agg_E2_R": [
    -0.0001260264360279928,
    -3.1312188380594463e-05,
    -4.992733691588924e-06,
    -1.246807165178332e-06,
    -1.9935923534220024e-07,
    -2.220446049250313e-16,
    -1.9918857729894768e-07,
    -1.2441405581320453e-06,
    -4.971398591790965e-06,
    -3.097858158196409e-05,
    -0.00012335053834788834,
    -0.0004896609150398801
   ],
   "lambda_mean_t4": [
    4.90403290776372e-05,
    1.215369995936284e-05,
    1.93574973745955e-06,
    4.832554553191739e-07,
    7.725747039759944e-08,
    1.490703376101465e-30,
    7.717532305173628e-08,
    4.819718164432341e-07,
    1.9254781517274743e-06,
    1.1992935409001277e-05,
    4.7746428880325785e-05,
    0.00018989709593312986
   ],
   "S4_E2": -4.267168229021896e-11,
   "S4_h": -2.385281734789809e-11,
   "kappa44_E2": -0.0004492770934296169,
   "kappa44_h": -4.535782266248913e-05,
   "kappa444_E2": 3.7958466556260277e-06,
   "kappa44_E2_HS": -0.0004767151950423074,
   "halving_dev_kappa44": 6.896612588907494e-08,
   "kappa44_E2_window0p1": -0.0004492081273037278,
   "fit_residual": 3.4010683936684335e-10,
   "biref_b1_VRH": -0.04548125222774924,
   "vT_VRH": 9.307899076533179,
   "vT_HS_lo": 9.211721064370861,
   "vT_HS_hi": 9.456854984588738,
   "quadform": {
    "kappa22": 7.963757933367799e-09,
    "kappa24": 3.4778572462814414e-07,
    "kappa44": -0.00044927996760422685,
    "residual": 3.8754519610994595e-09
   },
   "hs_ref": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   }
  },
  "cubic_gem8|111": {
   "r_agg_E2_VRH": [
    7.523936332098913e-05,
    1.8759490163944292e-05,
    2.997251965064507e-06,
    7.489803408589069e-07,
    1.1980578551451515e-07,
    0.0,
    1.1976536118396552e-07,
    7.483486843540277e-07,
    2.992197842610622e-06,
    1.8680424180850252e-05,
    7.460410303061771e-05,
    0.0002977782046622579
   ],
   "r_agg_h_VRH": [
    -1.1590815615636352e-05,
    -2.86299115281885e-06,
    -4.5509719270864224e-07,
    -1.1353983042639015e-07,
    -1.8144388991281346e-08,
    0.0,
    -1.8115683841912755e-08,
    -1.1309128233882859e-07,
    -4.515080809230909e-07,
    -2.806831356338968e-06,
    -1.1139242344304634e-05,
    -4.4028971179166376e-05
   ],
   "r_agg_E2_HS": [
    7.977387755220278e-05,
    1.9902593825005255e-05,
    3.180565407712166e-06,
    7.948235725141473e-07,
    1.2714137898051092e-07,
    0.0,
    1.2710098884483045e-07,
    7.941924689003343e-07,
    3.1755164744406983e-06,
    1.982369316411159e-05,
    7.9142355466022e-05,
    0.00031539029695215604
   ],
   "r_agg_E2_V": [
    6.839828063509579e-05,
    1.711330057552196e-05,
    2.7395868300583714e-06,
    6.850241669464907e-07,
    1.0961633001294047e-07,
    -2.220446049250313e-16,
    1.0963321339652055e-07,
    6.852879745888885e-07,
    2.7416973500393738e-06,
    1.714628385962591e-05,
    6.866233033830937e-05,
    0.000275358918345292
   ],
   "r_agg_E2_R": [
    8.401762401866186e-05,
    2.0874792253877672e-05,
    3.3284891276519346e-06,
    8.3120477656351e-07,
    1.3290615674677042e-07,
    -2.220446049250313e-16,
    1.3279238464392051e-07,
    8.294270388287117e-07,
    3.314265728082688e-06,
    2.065238772153144e-05,
    8.223369223170351e-05,
    0.00032644061002673475
   ],
   "lambda_mean_t4": [
    4.90403290776372e-05,
    1.215369995936284e-05,
    1.93574973745955e-06,
    4.832554553191739e-07,
    7.725747039759944e-08,
    1.490703376101465e-30,
    7.717532305173628e-08,
    4.819718164432341e-07,
    1.9254781517274743e-06,
    1.1992935409001277e-05,
    4.7746428880325785e-05,
    0.00018989709593312986
   ],
   "S4_E2": 2.8447697640179876e-11,
   "S4_h": -2.385281734789809e-11,
   "kappa44_E2": 0.00029951806228887087,
   "kappa44_h": -4.535782266248913e-05,
   "kappa444_E2": -2.530564419058326e-06,
   "kappa44_E2_HS": 0.00031781013002497063,
   "halving_dev_kappa44": 4.597743564728951e-08,
   "kappa44_E2_window0p1": 0.0002994720848532236,
   "fit_residual": 2.2673798427315232e-10,
   "biref_b1_VRH": -0.04548125222774924,
   "vT_VRH": 9.307899076533179,
   "vT_HS_lo": 9.211721064370861,
   "vT_HS_hi": 9.456854984588738,
   "quadform": {
    "kappa22": -5.3091738364530734e-09,
    "kappa24": 3.477857238465428e-07,
    "kappa44": 0.0002995199784038129,
    "residual": 3.8544177871454794e-09
   },
   "hs_ref": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   }
  }
 },
 "phase3": {
  "verdict_class": "IDENTITY-DELIVERED-L4",
  "F-MS2-3": "SILENT",
  "F-MS2-4": "SILENT",
  "F-MS2-2": "REGISTERED_NOT_EXECUTED",
  "worst_S4": 4.267168229021896e-11
 },
 "T1_post_write": {
  "list_md5": "be921b8c29f7578e85ed92f1450c1956",
  "scanner_md5": "6b86290090a8c84f1b1a0a99ec0bf697",
  "checkpoint": "CLEAN"
 }
}
=====END-EMBED name=inputs/gmscs2_gate/g_mscs2_chatleg_checkpoint.json=====

=====BEGIN-EMBED name=inputs/gmscs2_gate/g_mscs2_ccleg_checkpoint.json md5=9961745d1e1857cfab6445d4754b5060 bytes=68540 encoding=raw=====
{
 "gate": "G-MSCS2",
 "leg": "cc",
 "instrument": "g_mscs2_ccleg.py",
 "instrument_md5": "e58ba9a6d52daa23f8264255b6dbbb75",
 "memo_lock_md5": "efdcabdcd937cda4acb64f941dc4bb2b",
 "memo_lock_bytes": 46053,
 "ledger_base_md5": "f36bbdb04104008783f2763f70fb916f",
 "t1_list_md5": "be921b8c29f7578e85ed92f1450c1956",
 "schema_md5": "66f586d7b6c5e8228394222ddfda73f2",
 "x1_md5": "200e7a8b775577564369c6924d38a84c",
 "x6_chat_md5": "c04c0b8ea34cfe60f231aa06828e6ce4",
 "x6_cc_md5": "249e11dd53c4cb82f302b15d3c94c337",
 "activation_flag": "ACTIVATE: G-MSCS2-CC-LEG-1 WITH-A3",
 "addendum_A3_in_force": true,
 "utc": "2026-09-26 20:16:01 UTC",
 "elections": {
  "E-MS2-1": "a+b",
  "E-MS2-2": "a",
  "E-MS2-2b": "a+b",
  "E-MS2-2c": "001+111",
  "E-MS2-3": "a",
  "E-MS2-4": "a",
  "E-MS2-5": "a",
  "E-MS2-6": "a",
  "E-MS2-7": "05302210+MSCS1stratum",
  "E-MS2-8": "a"
 },
 "t1_scan": {
  "instrument": "CLEAN",
  "numeric_collisions_instrument": 0,
  "memo": "CLEAN",
  "numeric_collisions_memo": 0,
  "checkpoint_numeric_collisions": 6
 },
 "phase0": {
  "PIN-XTAL": {
   "worst_rel": 3.9907334492519883e-13,
   "worst_rel_vs_cc": 1.5980224727224674e-14,
   "by_key": {
    "hex_step|a": 1.8037809691863846e-16,
    "hex_step|b": 3.9907334492519883e-13,
    "hex_gem8|a": 5.925104822972279e-16,
    "hex_gem8|b": 8.463710763570074e-15,
    "cubic_step|001": 6.418673368548789e-15,
    "cubic_step|111": 1.0757782310463976e-15,
    "cubic_gem8|001": 1.203427902250091e-13,
    "cubic_gem8|111": 1.203427902250091e-13
   },
   "passed": true
  },
  "PIN-VRH0": {
   "worst_rel": 3.740581037287146e-15,
   "worst_rel_vs_cc": 3.985903300406611e-15,
   "passed": true
  },
  "PIN-HS0": {
   "worst_rel": 1.4642081959835474e-12,
   "worst_rel_vs_cc": 4.631715998568954e-13,
   "G_HS": {
    "hex_step|a": [
     70.40652703755305,
     70.97358894131216
    ],
    "hex_step|b": [
     70.4103032286342,
     70.97730993134306
    ],
    "hex_gem8|a": [
     99.81834260496913,
     101.05874270188924
    ],
    "hex_gem8|b": [
     99.81488234518243,
     101.05536909849494
    ],
    "cubic_step|001": [
     60.19609880774969,
     61.9046845031052
    ],
    "cubic_step|111": [
     60.19609880774969,
     61.9046845031052
    ],
    "cubic_gem8|001": [
     84.85580496802234,
     89.43210619949916
    ],
    "cubic_gem8|111": [
     84.85580496802234,
     89.43210619949916
    ]
   },
   "passed": true
  },
  "PIN-K2": {
   "worst_rel_hex_kappa2": 1.9101739846654823e-12,
   "worst_abs_cubic_kappa2": 3.1015835146880138e-15,
   "by_key": {
    "hex_step|a": {
     "kappa2_E2": -0.0014394617694985317,
     "x6_chat": -0.0014394617694966992,
     "x6_cc": -0.0014394617695005832,
     "dev": 1.2730581323988415e-12
    },
    "hex_step|b": {
     "kappa2_E2": -0.0014387027187495968,
     "x6_chat": -0.001438702718749083,
     "x6_cc": -0.0014387027187507326,
     "dev": 3.570542980347443e-13
    },
    "hex_gem8|a": {
     "kappa2_E2": -0.0018956484826737562,
     "x6_chat": -0.0018956484826701352,
     "x6_cc": -0.0018956484826738256,
     "dev": 1.9101739846654823e-12
    },
    "hex_gem8|b": {
     "kappa2_E2": -0.001896137466524572,
     "x6_chat": -0.0018961374665242264,
     "x6_cc": -0.0018961374665274083,
     "dev": 1.8228828800159285e-13
    },
    "cubic_step|001": {
     "kappa2_E2": 3.1015835146880138e-15,
     "x6_chat": 3.141702123932416e-15,
     "x6_cc": -2.1857725036605986e-16,
     "dev": 3.1015835146880138e-15
    },
    "cubic_step|111": {
     "kappa2_E2": 2.87608926272809e-15,
     "x6_chat": -1.6739143857147652e-16,
     "x6_cc": -1.9478276488317234e-15,
     "dev": 2.87608926272809e-15
    },
    "cubic_gem8|001": {
     "kappa2_E2": 1.1537558658562911e-15,
     "x6_chat": -1.4940723442743361e-16,
     "x6_cc": -2.9881446885486723e-16,
     "dev": 1.1537558658562911e-15
    },
    "cubic_gem8|111": {
     "kappa2_E2": -4.371545007321201e-16,
     "x6_chat": 1.272728293270753e-16,
     "x6_cc": -2.2936777285248548e-15,
     "dev": 4.371545007321201e-16
    }
   },
   "passed": true
  },
  "F-CTRL-ISO": {
   "passed": true,
   "worst_abs": 4.440892098500626e-16,
   "x_detail": {
    "cubic": {
     "r_xtal_worst": 2.220446049250313e-16,
     "r_agg_worst": 2.220446049250313e-16
    },
    "hex": {
     "r_xtal_worst": 2.220446049250313e-16,
     "r_agg_worst": 4.440892098500626e-16
    }
   }
  },
  "F-CTRL-SO3": {
   "passed": true,
   "dev_from_0p4": 7.771561172376096e-16,
   "r_agg_0_abs": 3.3306690738754696e-16,
   "x_mean_F0_t0": 0.39999999999999997
  },
  "F-CTRL-POS": {
   "passed": true,
   "min_odf_weight": 0.33498992971329056,
   "x_n_odfs_checked": 520
  },
  "F-CTRL-L2NULL": {
   "passed": true,
   "worst_abs": 7.987802509504381e-15,
   "mixed_r_agg_change_A29": {
    "cubic_step|001": -9.076177710509725e-07,
    "cubic_step|111": -9.076177709399502e-07,
    "cubic_gem8|001": -1.3041577882066946e-06,
    "cubic_gem8|111": -1.30415778798465e-06
   },
   "x_scope": "A-3.1: pure l = 2 (tensors + r_agg) and mixed-term tensor clauses; mixed r_agg reported",
   "x_literal_A29_worst_abs": 1.3041577882066946e-06,
   "x_literal_A29_would_pass": false,
   "x_detail": {
    "cubic_step|001": {
     "pure_l2_t1": {
      "V": 1.3428385384522914e-15,
      "Sbar": 5.322352074662751e-16,
      "HS_lo": 1.9496117725117262e-15,
      "HS_hi": 7.987802509504381e-15,
      "r_agg_E2": 3.3306690738754696e-16,
      "r_agg_h": 3.3306690738754696e-16
     },
     "mixed_tensor_clauses": {
      "V": 1.7514315387333965e-15,
      "Sbar": 5.782386151353505e-16,
      "HS_lo": 1.9564636944716545e-15,
      "HS_hi": 2.7640142460363863e-15
     },
     "mixed_r_agg_change_A29": -9.076177710509725e-07,
     "x_mixed_r_agg_h_change": 0.0
    },
    "cubic_step|111": {
     "pure_l2_t1": {
      "V": 8.057031230713749e-16,
      "Sbar": 7.741603017691276e-16,
      "HS_lo": 1.8103537887608885e-15,
      "HS_hi": 6.0597122485895305e-15,
      "r_agg_E2": 2.220446049250313e-16,
      "r_agg_h": 2.220446049250313e-16
     },
     "mixed_tensor_clauses": {
      "V": 3.2334120715078092e-15,
      "Sbar": 1.349223435315818e-15,
      "HS_lo": 2.5154533214635556e-15,
      "HS_hi": 2.211211396829109e-15
     },
     "mixed_r_agg_change_A29": -9.076177709399502e-07,
     "x_mixed_r_agg_h_change": 1.1102230246251565e-16
    },
    "cubic_gem8|001": {
     "pure_l2_t1": {
      "V": 1.0024401505828492e-15,
      "Sbar": 1.31505692512355e-15,
      "HS_lo": 2.4606279633542988e-15,
      "HS_hi": 4.485119197650071e-15,
      "r_agg_E2": 2.220446049250313e-16,
      "r_agg_h": 0.0
     },
     "mixed_tensor_clauses": {
      "V": 1.1737120487694359e-15,
      "Sbar": 1.0467655379750148e-15,
      "HS_lo": 8.821789730108347e-16,
      "HS_hi": 2.251149896189947e-15
     },
     "mixed_r_agg_change_A29": -1.3041577882066946e-06,
     "x_mixed_r_agg_h_change": -2.220446049250313e-16
    },
    "cubic_gem8|111": {
     "pure_l2_t1": {
      "V": 1.169513509013324e-15,
      "Sbar": 1.972585387685325e-15,
      "HS_lo": 2.6363871035938917e-15,
      "HS_hi": 3.4500916905000543e-15,
      "r_agg_E2": 0.0,
      "r_agg_h": 0.0
     },
     "mixed_tensor_clauses": {
      "V": 8.383657491210257e-16,
      "Sbar": 1.570148306962522e-15,
      "HS_lo": 4.05802327584984e-15,
      "HS_hi": 3.1169767793399268e-15
     },
     "mixed_r_agg_change_A29": -1.30415778798465e-06,
     "x_mixed_r_agg_h_change": -2.220446049250313e-16
    }
   }
  },
  "F-CTRL-L4EXHAUST": {
   "passed": true,
   "worst_rel_tensor": 6.420725383328799e-15,
   "worst_abs_r_agg": 5.551115123125783e-16,
   "x_t6": 0.3,
   "x_K6_normalization": "max|K6| = 1 on the sphere (raw scale 0.04617033598890424)",
   "x_detail": {
    "hex_step|a t4=0.25": {
     "tensor_rel": 6.420725383328799e-15,
     "r_agg_abs": 0.0
    },
    "hex_step|a t2=t4=0.25": {
     "tensor_rel": 3.954172686838796e-15,
     "r_agg_abs": 0.0
    },
    "hex_step|b t4=0.25": {
     "tensor_rel": 3.457237682791583e-15,
     "r_agg_abs": 2.220446049250313e-16
    },
    "hex_step|b t2=t4=0.25": {
     "tensor_rel": 2.9547193290865556e-15,
     "r_agg_abs": 5.551115123125783e-16
    },
    "hex_gem8|a t4=0.25": {
     "tensor_rel": 3.4172542639648757e-15,
     "r_agg_abs": 2.220446049250313e-16
    },
    "hex_gem8|a t2=t4=0.25": {
     "tensor_rel": 2.785667179874864e-15,
     "r_agg_abs": 2.220446049250313e-16
    },
    "hex_gem8|b t4=0.25": {
     "tensor_rel": 3.417297115191496e-15,
     "r_agg_abs": 2.220446049250313e-16
    },
    "hex_gem8|b t2=t4=0.25": {
     "tensor_rel": 3.110962356424953e-15,
     "r_agg_abs": 2.220446049250313e-16
    },
    "cubic_step|001 t4=0.25": {
     "tensor_rel": 3.0404156706400247e-15,
     "r_agg_abs": 1.1102230246251565e-16,
     "x_direct_E2_weight_change": 3.885780586188048e-16
    },
    "cubic_step|111 t4=0.25": {
     "tensor_rel": 3.0404156706400247e-15,
     "r_agg_abs": 2.220446049250313e-16,
     "x_direct_E2_weight_change": 3.3306690738754696e-16
    },
    "cubic_gem8|001 t4=0.25": {
     "tensor_rel": 2.251149896189947e-15,
     "r_agg_abs": 0.0,
     "x_direct_E2_weight_change": 3.885780586188048e-16
    },
    "cubic_gem8|111 t4=0.25": {
     "tensor_rel": 2.251149896189947e-15,
     "r_agg_abs": 2.220446049250313e-16,
     "x_direct_E2_weight_change": 3.3306690738754696e-16
    }
   }
  },
  "F-CTRL-C4": {
   "passed": true,
   "worst_rel_closed_form": 1.7155661439689658e-15,
   "worst_rel_affine": 3.5337177708315534e-15,
   "h0_effect_rel": 2.9771733495537138e-15,
   "x_detail": {
    "cubic_step|001": {
     "H": -97.13640000000002,
     "H_S": 0.0077525114483620264,
     "closed_form_rel": 1.3910967984279206e-15,
     "affine_rel": 3.5337177708315534e-15,
     "x_voigt_dC_t0p3": [
      [
       -0.8325977142859813,
       -0.2775325714285799,
       1.1101302857144049,
       0.0,
       0.0,
       0.0
      ],
      [
       -0.2775325714285799,
       -0.8325977142859813,
       1.1101302857144049,
       0.0,
       0.0,
       0.0
      ],
      [
       1.1101302857144049,
       1.1101302857144049,
       -2.2202605714288666,
       0.0,
       0.0,
       0.0
      ],
      [
       0.0,
       0.0,
       0.0,
       1.1101302857142057,
       0.0,
       0.0
      ],
      [
       0.0,
       0.0,
       0.0,
       0.0,
       1.1101302857142057,
       0.0
      ],
      [
       0.0,
       0.0,
       0.0,
       0.0,
       0.0,
       -0.2775325714286509
      ]
     ]
    },
    "cubic_gem8|001": {
     "H": -170.38749999999996,
     "H_S": 0.006986500320404432,
     "closed_form_rel": 1.7155661439689658e-15,
     "affine_rel": 2.817545679910539e-15,
     "x_voigt_dC_t0p3": [
      [
       -1.460464285714579,
       -0.4868214285713748,
       1.9472857142857265,
       0.0,
       0.0,
       0.0
      ],
      [
       -0.4868214285713748,
       -1.460464285714579,
       1.9472857142857265,
       0.0,
       0.0,
       0.0
      ],
      [
       1.9472857142857265,
       1.9472857142857265,
       -3.894571428571112,
       0.0,
       0.0,
       0.0
      ],
      [
       0.0,
       0.0,
       0.0,
       1.9472857142857403,
       0.0,
       0.0
      ],
      [
       0.0,
       0.0,
       0.0,
       0.0,
       1.9472857142857403,
       0.0
      ],
      [
       0.0,
       0.0,
       0.0,
       0.0,
       0.0,
       -0.4868214285714173
      ]
     ]
    }
   }
  },
  "F-CTRL-MARG": {
   "passed": true,
   "worst_abs": 1.659783421814609e-14,
   "x_c_coefficients": {
    "001": 1.0,
    "111": -0.6666666666666661
   },
   "x_detail": {
    "cubic_step|001 t4=0.5": 1.0547118733938987e-14,
    "cubic_step|001 t4=-0.5": 1.4377388168895777e-14,
    "cubic_step|111 t4=0.5": 7.271960811294775e-15,
    "cubic_step|111 t4=-0.5": 9.547918011776346e-15,
    "cubic_gem8|001 t4=0.5": 1.0158540675320182e-14,
    "cubic_gem8|001 t4=-0.5": 1.659783421814609e-14,
    "cubic_gem8|111 t4=0.5": 6.8833827526759706e-15,
    "cubic_gem8|111 t4=-0.5": 1.1324274851176597e-14
   }
  },
  "F-CTRL-TEX4": {
   "passed": true,
   "r_agg_t1_abs": 0.0004118326557733809,
   "x_r_agg_t1": 0.0004118326557733809,
   "x_H": 120.0
  },
  "F-CTRL-QUAD": {
   "passed": true,
   "doubling_residual": 2.220446049250313e-16,
   "x_k_rule": "GL(cos theta) 64 x uniform phi 128; doubling 128 x 256 at t4 = 0.25 on Hill/E2 per key",
   "x_fiber_rule": "fiber-axis route: analytic SO(2) coset average x GL(cos theta) 16 x uniform phi 32 on a generically rotated node set (exact to degree 31)"
  }
 },
 "phase1": {
  "hex_step|a": {
   "v_EM": 8.498926630589143,
   "v_S2E2": 8.261235391127114,
   "v_S2h": 8.489468358289109,
   "lambda_mean": 0.004808575724022839,
   "lambda_max": 0.03353758299774612,
   "r_xtal_E2": -0.02796720689487253,
   "r_xtal_h": -0.001112878450555299
  },
  "hex_step|b": {
   "v_EM": 8.499138059764721,
   "v_S2E2": 8.26161155132829,
   "v_S2h": 8.489680210591466,
   "lambda_mean": 0.0048086004283485135,
   "lambda_max": 0.033534547685208825,
   "r_xtal_E2": -0.027947129081346778,
   "r_xtal_h": -0.0011128009813170525
  },
  "hex_gem8|a": {
   "v_EM": 10.167571147427779,
   "v_S2E2": 9.767584615679638,
   "v_S2h": 10.154202161568202,
   "lambda_mean": 0.0049537696180639535,
   "lambda_max": 0.03513301845903746,
   "r_xtal_E2": -0.039339437703303504,
   "r_xtal_h": -0.0013148652382883874
  },
  "hex_gem8|b": {
   "v_EM": 10.167412388965342,
   "v_S2E2": 9.767300819096652,
   "v_S2h": 10.154042977980577,
   "lambda_mean": 0.004953789932329423,
   "lambda_max": 0.035133018459037504,
   "r_xtal_E2": -0.03935234989611802,
   "r_xtal_h": -0.0013149275816995987
  },
  "cubic_step|001": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 7.889264216956223,
   "v_S2h": 8.015951162831872,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173745,
   "r_xtal_E2": -0.01729676774121569,
   "r_xtal_h": -0.001516377102324551
  },
  "cubic_step|111": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 8.120698567854001,
   "v_S2h": 8.015951162831872,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173745,
   "r_xtal_E2": 0.01153117849414409,
   "r_xtal_h": -0.001516377102324551
  },
  "cubic_gem8|001": {
   "v_EM": 9.721171015078212,
   "v_S2E2": 9.5185580718033,
   "v_S2h": 9.703234472528251,
   "lambda_mean": 0.0093105038596528,
   "lambda_max": 0.043292701954120015,
   "r_xtal_E2": -0.020842442022740437,
   "r_xtal_h": -0.0018451010194286965
  },
  "cubic_gem8|111": {
   "v_EM": 9.721171015078212,
   "v_S2E2": 9.85624631059482,
   "v_S2h": 9.703234472528251,
   "lambda_mean": 0.0093105038596528,
   "lambda_max": 0.043292701954120015,
   "r_xtal_E2": 0.01389496134849355,
   "r_xtal_h": -0.0018451010194286965
  }
 },
 "phase2": {
  "hex_step|a": {
   "vT_V": 8.54777943873924,
   "vT_R": 8.28834102998393,
   "vT_VRH": 8.419059637591612,
   "vT_HS_lo": 8.390859731729106,
   "vT_HS_hi": 8.424582419402885,
   "x_KV_GV_KR_GR": [
    134.6092888888889,
    73.06453333333334,
    134.60823359538978,
    68.6965970293151
   ],
   "kappa2_E2": -0.0014394617694985317,
   "x_l2_family": {
    "S2_E2": 1.6132797019583628e-13,
    "kappa3_E2": -7.369324352731974e-07,
    "fit_residual": 6.12980248496293e-11,
    "r_agg_E2_VRH_l2": [
     -0.00035977898387029583,
     -8.995485659313296e-05,
     -1.4393819488089932e-05,
     -3.5985447373043655e-06,
     -5.757759000690754e-07,
     2.220446049250313e-16,
     -5.757876907486192e-07,
     -3.5987289647154697e-06,
     -1.4395293313262947e-05,
     -8.997788565145992e-05,
     -0.00035996323194520397,
     -0.001440311666697891
    ],
    "n_fit_points": 9
   },
   "r_agg_E2_VRH": [
    4.007511215431414e-05,
    1.0021876255539297e-05,
    1.6038160917108968e-06,
    4.009811211957981e-07,
    6.415961051331465e-08,
    2.220446049250313e-16,
    6.416315367907544e-08,
    4.010364844653225e-07,
    1.6042590029741177e-06,
    1.0028797479355589e-05,
    4.013050311080235e-05,
    0.00016065650935481735
   ],
   "r_agg_h_VRH": [
    -1.8659710554480569e-06,
    -4.678262346402562e-07,
    -7.498399856586957e-08,
    -1.875714272792095e-08,
    -3.0022190289358264e-09,
    2.220446049250313e-16,
    -3.0036607645556046e-09,
    -1.87796693751352e-08,
    -7.516421385300731e-08,
    -4.7064235364491225e-07,
    -1.8885071644270113e-06,
    -7.604051808884904e-06
   ],
   "r_agg_E2_HS": [
    3.9929228545565465e-05,
    9.987793138321877e-06,
    1.5985754207026304e-06,
    3.9968797649336807e-07,
    6.395431473293911e-08,
    2.220446049250313e-16,
    6.395996998698195e-08,
    3.9977633781163036e-07,
    1.5992823096944164e-06,
    9.998838376157337e-06,
    4.001759322602716e-05,
    0.00016024951313764468
   ],
   "r_agg_E2_V": [
    4.5906615393498384e-05,
    1.1471262962192696e-05,
    1.8349039123677358e-06,
    4.586852682120224e-07,
    7.338576568649557e-08,
    2.220446049250313e-16,
    7.33806317931851e-08,
    4.5860505282213637e-07,
    1.834262182365265e-06,
    1.146123554107703e-05,
    4.582638479200263e-05,
    0.0001831689574216533
   ],
   "r_agg_E2_R": [
    3.3875297373642255e-05,
    8.480578136849104e-06,
    1.3580482476349687e-06,
    3.396095238361596e-07,
    5.434692451622425e-08,
    -2.220446049250313e-16,
    5.4359510670565214e-08,
    3.3980618208140356e-07,
    1.3596215251432398e-06,
    8.50516195338713e-06,
    3.4072006643626196e-05,
    0.0001367168344819092
   ],
   "lambda_mean_t4": [
    9.380371358234877e-06,
    2.348557538265015e-06,
    3.76118153700588e-07,
    9.405930416692327e-08,
    1.5052372673057354e-08,
    3.1742861445148563e-32,
    1.5056249001901823e-08,
    9.411987210408266e-08,
    3.76602705753589e-07,
    2.3561295999753513e-06,
    9.440974601825143e-06,
    3.790633597379144e-05
   ],
   "x_vqSH_t4": [
    8.40539067675697,
    8.412224084972753,
    8.416325157518935,
    8.417692354242819,
    8.418512713843494,
    8.419059637591612,
    8.419606575233734,
    8.420427007777953,
    8.421794465014582,
    8.42589736115591,
    8.432737282295363,
    8.446423824260233
   ],
   "x_vqSV_t4": [
    8.473824460683653,
    8.44642382426023,
    8.430001048422602,
    8.424529641490455,
    8.421247471660271,
    8.419059637591616,
    8.416872025827097,
    8.413591023096172,
    8.40812378441001,
    8.391730187797545,
    8.3644337843702,
    8.30993346171258
   ],
   "x_r_agg_h_HS": [
    -1.8473497336302103e-06,
    -4.633610806159538e-07,
    -7.428707060608275e-08,
    -1.8584336070048835e-08,
    -2.9747054819395657e-09,
    0.0,
    -2.976326296533216e-09,
    -1.860966414302112e-08,
    -7.448969630008406e-08,
    -4.665272389514641e-07,
    -1.8726825539161496e-06,
    -7.545286253130001e-06
   ],
   "S4_E2": -2.1901880737433866e-13,
   "S4_h": 7.604097370267146e-14,
   "kappa44_E2": 0.00016040534614166288,
   "kappa444_E2": 2.2148264931772227e-07,
   "kappa44_h": -7.507739663239201e-06,
   "kappa44_E2_HS": 0.000159893047686394,
   "halving_dev_kappa44": 1.605578370315842e-09,
   "fit_residual_E2": 1.5919189948239166e-11,
   "x_fit_windows": {
    "n_points_0p25_inclusive": 9,
    "n_points_0p1_inclusive": 7,
    "kappa44_E2_strict_window_0p25": 0.00016040374056329256,
    "n_strict_0p25": 7,
    "kappa44_E2_strict_window_0p1": 0.00016040351948750056,
    "n_strict_0p1": 5,
    "halving_dev_strict": 2.2107579200451866e-10
   },
   "biref_b1_VRH": 0.01624085410722665,
   "x_biref_polarization_overlap_min": 1.0,
   "quadform": {
    "kappa22": -0.0014394693020041397,
    "kappa24": -1.2488792577836864e-08,
    "kappa44": 0.00016039903763748667,
    "residual": 6.910614703230103e-10,
    "x_cubic_terms_discarded": [
     -7.369515817719742e-07,
     -7.276386960723754e-06,
     -3.936928925279228e-06,
     2.2143796444095318e-07
    ],
    "x_grid_r_agg_E2_VRH": [
     -7.976009400101347e-05,
     -8.737740784903192e-05,
     -8.995485659313296e-05,
     -8.748962981364183e-05,
     -7.997872808929163e-05,
     -1.2409636205301666e-05,
     -1.9962433144171676e-05,
     -2.2490065633484768e-05,
     -1.9989874392223328e-05,
     -1.2459014352539377e-05,
     1.0021876255539297e-05,
     2.505878869740741e-06,
     2.220446049250313e-16,
     2.5067439404224956e-06,
     1.0028797479355589e-05,
     -1.2473478692598405e-05,
     -1.998057378083118e-05,
     -2.2492944204866028e-05,
     -2.0008244574820644e-05,
     -1.252395037854015e-05,
     -7.990431874749238e-05,
     -8.743059230065242e-05,
     -8.997788565145992e-05,
     -8.754401630450825e-05,
     -8.012662609491183e-05
    ],
    "x_reading": "hex two-parameter family"
   },
   "x_min_odf_weight_5x5": 0.5012432944308812,
   "kappa24_richardson": 3.006854025026466e-13,
   "x_kappa24_richardson_D": {
    "D_0p02": -9.416079027602109e-11,
    "D_0p01": -2.3314683517128287e-11
   }
  },
  "hex_step|b": {
   "vT_V": 8.547982997955327,
   "vT_R": 8.288576029181625,
   "vT_VRH": 8.419278648579626,
   "vT_HS_lo": 8.391084746839004,
   "vT_HS_hi": 8.424803257723177,
   "x_KV_GV_KR_GR": [
    134.60928888888893,
    73.06801333333333,
    134.60823359538995,
    68.70049259152424
   ],
   "kappa2_E2": -0.0014387027187495968,
   "x_l2_family": {
    "S2_E2": 1.6260684338530435e-13,
    "kappa3_E2": -7.369722178139577e-07,
    "fit_residual": 6.118731076551562e-11,
    "r_agg_E2_VRH_l2": [
     -0.000359589205973343,
     -8.990741528103197e-05,
     -1.4386229051588373e-05,
     -3.5966471373383158e-06,
     -5.754722847139959e-07,
     2.220446049250313e-16,
     -5.754840760596736e-07,
     -3.59683137440836e-06,
     -1.4387702956142334e-05,
     -8.993044558192054e-05,
     -0.0003597734639763095,
     -0.001439552451643178
    ],
    "n_fit_points": 9
   },
   "r_agg_E2_VRH": [
    4.0077429722673585e-05,
    1.002245710202132e-05,
    1.6039091732533706e-06,
    4.010044043489813e-07,
    6.41633368658745e-08,
    2.220446049250313e-16,
    6.416688158594752e-08,
    4.0105979248750145e-07,
    1.6043522874653604e-06,
    1.0029381496190481e-05,
    4.013284605175471e-05,
    0.00016066594053820715
   ],
   "r_agg_h_VRH": [
    -1.8662871319463648e-06,
    -4.679056788692293e-07,
    -7.499675225286495e-08,
    -1.8760334619116747e-08,
    -3.002729731527154e-09,
    0.0,
    -3.0041720222584445e-09,
    -1.8782868815847564e-08,
    -7.517702727000142e-08,
    -4.70722723466821e-07,
    -1.8888306498876517e-06,
    -7.605363089635553e-06
   ],
   "r_agg_E2_HS": [
    3.9931605506859924e-05,
    9.988388289805528e-06,
    1.5986707333492944e-06,
    3.9971181187148375e-07,
    6.395812945925172e-08,
    0.0,
    6.396378515738377e-08,
    3.9980018828877917e-07,
    1.5993777409128995e-06,
    9.999435379270949e-06,
    4.001998499880699e-05,
    0.00016025911078099142
   ],
   "r_agg_E2_V": [
    4.5906764787329024e-05,
    1.1471300246590488e-05,
    1.834909872044932e-06,
    4.586867579092768e-07,
    7.338600416240126e-08,
    0.0,
    7.338086982500158e-08,
    4.586065411871232e-07,
    1.8342681347149892e-06,
    1.1461272707569137e-05,
    4.582653324369801e-05,
    0.00018316954966857146
   ],
   "r_agg_E2_R": [
    3.387997594828107e-05,
    8.48175094469994e-06,
    1.3582362119457514e-06,
    3.396565415592079e-07,
    5.435444960788516e-08,
    0.0,
    5.436703953698441e-08,
    3.3985325398333543e-07,
    1.3598099231071359e-06,
    8.50634153670704e-06,
    3.4076739442001625e-05,
    0.00013673588893814426
   ],
   "lambda_mean_t4": [
    9.382285878068264e-06,
    2.349037567583009e-06,
    3.761951017469074e-07,
    9.407855350473187e-08,
    1.5055453765106412e-08,
    2.1832584308612035e-32,
    1.5059331708440377e-08,
    9.413914666881178e-08,
    3.766798556212922e-07,
    2.3566127834136175e-06,
    9.442914373552608e-06,
    3.79141574120327e-05
   ],
   "x_vqSH_t4": [
    8.405608540880545,
    8.412442521740191,
    8.416543938628882,
    8.417911250260097,
    8.418731678835607,
    8.41927864857963,
    8.419825632227806,
    8.42064613380016,
    8.42201370613454,
    8.426116947951204,
    8.43295744649473,
    8.446645148098783
   ],
   "x_vqSV_t4": [
    8.474048123412766,
    8.446645148098783,
    8.430220981468079,
    8.42474911299687,
    8.4214666667335,
    8.419278648579626,
    8.417090852892375,
    8.413809574581274,
    8.408341877402567,
    8.391946911323686,
    8.3646482451878,
    8.310143468908551
   ],
   "x_r_agg_h_HS": [
    -1.8476708764092464e-06,
    -4.63441771403339e-07,
    -7.430002091357579e-08,
    -1.8587576922080018e-08,
    -2.975224289158973e-09,
    0.0,
    -2.976845991931043e-09,
    -1.8612911878435057e-08,
    -7.450270145259452e-08,
    -4.6660878161297603e-07,
    -1.8730105157960253e-06,
    -7.5466131491674915e-06
   ],
   "S4_E2": -2.2010851017752434e-13,
   "S4_h": 7.34844721335253e-14,
   "kappa44_E2": 0.00016041466503203565,
   "kappa444_E2": 2.2158411841270297e-07,
   "kappa44_h": -7.509018171302918e-06,
   "kappa44_E2_HS": 0.0001599025849219905,
   "halving_dev_kappa44": 1.606171687621935e-09,
   "fit_residual_E2": 1.5924962558031076e-11,
   "x_fit_windows": {
    "n_points_0p25_inclusive": 9,
    "n_points_0p1_inclusive": 7,
    "kappa44_E2_strict_window_0p25": 0.00016041305886034803,
    "n_strict_0p25": 7,
    "kappa44_E2_strict_window_0p1": 0.00016041283771231938,
    "n_strict_0p1": 5,
    "halving_dev_strict": 2.2114802865477387e-10
   },
   "biref_b1_VRH": 0.016241797577238582,
   "x_biref_polarization_overlap_min": 1.0,
   "quadform": {
    "kappa22": -0.0014387102478831734,
    "kappa24": -1.2484618920946934e-08,
    "kappa44": 0.00016040835823498604,
    "residual": 6.907207573508519e-10,
    "x_cubic_terms_discarded": [
     -7.369912610454396e-07,
     -7.272454059151412e-06,
     -3.939847498398738e-06,
     2.215393441283962e-07
    ],
    "x_grid_r_agg_E2_VRH": [
     -7.971208679635744e-05,
     -8.732984004833355e-05,
     -8.990741528103197e-05,
     -8.7442000696214e-05,
     -7.993059542565906e-05,
     -1.2397187749924043e-05,
     -1.99504295744779e-05,
     -2.247820554202029e-05,
     -1.9977855104102993e-05,
     -1.2446531859500176e-05,
     1.002245710202132e-05,
     2.506024271653473e-06,
     2.220446049250313e-16,
     2.5068897382407584e-06,
     1.0029381496190481e-05,
     -1.2461075853509307e-05,
     -1.9968581805862584e-05,
     -2.2481084268943796e-05,
     -1.999623680537521e-05,
     -1.2511513793445062e-05,
     -7.985640459950982e-05,
     -8.738304907141003e-05,
     -8.993044558192054e-05,
     -8.749641069916159e-05,
     -8.007858526049016e-05
    ],
    "x_reading": "hex two-parameter family"
   },
   "x_min_odf_weight_5x5": 0.5012432944308812,
   "kappa24_richardson": 1.8503717077085943e-13,
   "x_kappa24_richardson_D": {
    "D_0p02": -9.381384558082573e-11,
    "D_0p01": -2.3314683517128287e-11
   }
  },
  "hex_gem8|a": {
   "vT_V": 10.248997674569605,
   "vT_R": 9.830076336505323,
   "vT_VRH": 10.041721817369147,
   "vT_HS_lo": 9.990913001571435,
   "vT_HS_hi": 10.052797754948084,
   "x_KV_GV_KR_GR": [
    229.6961555555555,
    105.04195333333318,
    229.6959453087235,
    96.6304007815219
   ],
   "kappa2_E2": -0.0018956484826737562,
   "x_l2_family": {
    "S2_E2": 4.876221669425802e-13,
    "kappa3_E2": -1.2405708651167132e-06,
    "fit_residual": 1.412218853278713e-10,
    "r_agg_E2_VRH_l2": [
     -0.0004737700796713096,
     -0.00011845867062465487,
     -1.8955103105455784e-05,
     -4.738925659331095e-06,
     -7.582427593577634e-07,
     0.0,
     -7.582626074809085e-07,
     -4.7392357853670575e-06,
     -1.895758412695514e-05,
     -0.00011849743822156533,
     -0.00047408026726247776,
     -0.0018971495594125587
    ],
    "n_fit_points": 9
   },
   "r_agg_E2_VRH": [
    4.485121549713256e-05,
    1.1215782709905753e-05,
    1.7948340196305423e-06,
    4.4873519344790225e-07,
    7.18002297617204e-08,
    0.0,
    7.180373828852282e-08,
    4.4879001204201074e-07,
    1.7952725743786146e-06,
    1.1222636018493048e-05,
    4.490606733908997e-05,
    0.0001797632608036004
   ],
   "r_agg_h_VRH": [
    -1.9274619713627317e-06,
    -4.832185266367972e-07,
    -7.744891528105313e-08,
    -1.937356253201017e-08,
    -3.1008645651198208e-09,
    -2.220446049250313e-16,
    -3.102331946891468e-09,
    -1.939648786031256e-08,
    -7.763232234836437e-08,
    -4.860845420617821e-07,
    -1.9503980948076816e-06,
    -7.852781449102508e-06
   ],
   "r_agg_E2_HS": [
    4.468026881720988e-05,
    1.1176594882256197e-05,
    1.788883845499356e-06,
    4.472734349558749e-07,
    7.156879022751639e-08,
    0.0,
    7.157551484837654e-08,
    4.473785086833715e-07,
    1.7897244393161316e-06,
    1.1189729288041406e-05,
    4.4785347755871285e-05,
    0.00017935416817671523
   ],
   "r_agg_E2_V": [
    5.303875172679717e-05,
    1.3252550827180798e-05,
    2.119752434470712e-06,
    5.298846896817366e-07,
    8.477646873394917e-08,
    -2.220446049250313e-16,
    8.476974855398112e-08,
    5.297796819014877e-07,
    2.118912363568981e-06,
    1.3239424036859404e-05,
    5.2933718038605804e-05,
    0.000211561076949085
   ],
   "r_agg_E2_R": [
    3.595565596681283e-05,
    9.002191959206485e-06,
    1.4416580709220028e-06,
    3.6052483665116597e-07,
    5.769461730587011e-08,
    -2.220446049250313e-16,
    5.770887079314946e-08,
    3.6074754605763815e-07,
    1.4434397612728134e-06,
    9.030032598555948e-06,
    3.6178430369071535e-05,
    0.00014520159111741648
   ],
   "lambda_mean_t4": [
    8.586544971337518e-06,
    2.1497677185609786e-06,
    3.442790184765544e-07,
    8.609675774035136e-08,
    1.377809879374235e-08,
    1.1304160191794135e-31,
    1.378161840846958e-08,
    8.615175202017991e-08,
    3.447189812868586e-07,
    2.1566430751075244e-06,
    8.641574624897541e-06,
    3.469662301936794e-05
   ],
   "x_vqSH_t4": [
    10.023475003193818,
    10.032597444270642,
    10.038071833759119,
    10.039896786291415,
    10.040991795492339,
    10.041721817369147,
    10.0424518518639,
    10.04354692730903,
    10.045372116427943,
    10.050848162030675,
    10.059976517914187,
    10.078239422579216
   ],
   "x_vqSV_t4": [
    10.114791124935708,
    10.078239422579216,
    10.05632493167103,
    10.049022733471405,
    10.044642031258608,
    10.041721817369151,
    10.03880180536684,
    10.034422163064969,
    10.027123750307732,
    10.005235759520405,
    9.96877872937166,
    9.89594181624304
   ],
   "x_r_agg_h_HS": [
    -1.904816657849473e-06,
    -4.77818533073382e-07,
    -7.660939072007267e-08,
    -1.916569458693118e-08,
    -3.06779790459899e-09,
    0.0,
    -3.069520637666301e-09,
    -1.9192605837936583e-08,
    -7.682468428082956e-08,
    -4.81182647171785e-07,
    -1.9317340119728854e-06,
    -7.785211407873582e-06
   ],
   "S4_E2": -2.6497773212688476e-13,
   "S4_h": 8.39909948940018e-14,
   "kappa44_E2": 0.00017950729579206332,
   "kappa444_E2": 2.1931009361797286e-07,
   "kappa44_h": -7.754414848821103e-06,
   "kappa44_E2_HS": 0.0001789305885712823,
   "halving_dev_kappa44": 1.98359848907698e-09,
   "fit_residual_E2": 1.9667137863803042e-11,
   "x_fit_windows": {
    "n_points_0p25_inclusive": 9,
    "n_points_0p1_inclusive": 7,
    "kappa44_E2_strict_window_0p25": 0.00017950531219357424,
    "n_strict_0p25": 7,
    "kappa44_E2_strict_window_0p1": 0.00017950503907526356,
    "n_strict_0p1": 5,
    "halving_dev_strict": 2.7311831068228473e-10
   },
   "biref_b1_VRH": 0.018174882511168545,
   "x_biref_polarization_overlap_min": 1.0,
   "quadform": {
    "kappa22": -0.0018956599069480582,
    "kappa24": -1.837213389418741e-08,
    "kappa44": 0.0001794984220250463,
    "residual": 1.0648670178059136e-09,
    "x_cubic_terms_discarded": [
     -1.2406272604391896e-06,
     -9.829662260388087e-06,
     -3.579747184617073e-06,
     2.192759781806895e-07
    ],
    "x_grid_r_agg_E2_VRH": [
     -0.00010703681490453754,
     -0.00011556458006634074,
     -0.00011845867062465487,
     -0.00011571629866791167,
     -0.00010733444339172671,
     -1.8335614543230072e-05,
     -2.678657164734144e-05,
     -2.9616888306382982e-05,
     -2.6823938995890195e-05,
     -1.840486895210436e-05,
     1.1215782709905753e-05,
     2.8043458761839446e-06,
     0.0,
     2.8052024405589293e-06,
     1.1222636018493048e-05,
     -1.8395703234586058e-05,
     -2.6805229290549626e-05,
     -2.9621734073170813e-05,
     -2.684293430765816e-05,
     -1.8466325168220443e-05,
     -0.00010718475434112751,
     -0.0001156303094735911,
     -0.00011849743822156533,
     -0.00011578403746348442,
     -0.00010748778656943792
    ],
    "x_reading": "hex two-parameter family"
   },
   "x_min_odf_weight_5x5": 0.5012432944308812,
   "kappa24_richardson": 1.3646491344350882e-12,
   "x_kappa24_richardson_D": {
    "D_0p02": -1.384309333829492e-10,
    "D_0p01": -3.3584246494910985e-11
   }
  },
  "hex_gem8|b": {
   "vT_V": 10.248847414872237,
   "vT_R": 9.829890312566,
   "vT_VRH": 10.041554085160628,
   "vT_HS_lo": 9.990739829721441,
   "vT_HS_hi": 10.052629959293983,
   "x_KV_GV_KR_GR": [
    229.6961555555557,
    105.03887333333333,
    229.69594530872402,
    96.6267435570789
   ],
   "kappa2_E2": -0.001896137466524572,
   "x_l2_family": {
    "S2_E2": 4.875886535531316e-13,
    "kappa3_E2": -1.240545878339092e-06,
    "fit_residual": 1.4134697812830154e-10,
    "r_agg_E2_VRH_l2": [
     -0.0004738923403125872,
     -0.0001184892325272191,
     -1.895999284384775e-05,
     -4.740148086490592e-06,
     -7.58438347125967e-07,
     -3.3306690738754696e-16,
     -7.584581950270675e-07,
     -4.740458206198284e-06,
     -1.896247381538707e-05,
     -0.00011852799934330971,
     -0.0004742025216768475,
     -0.0018976387487925628
    ],
    "n_fit_points": 9
   },
   "r_agg_E2_VRH": [
    4.484977886520802e-05,
    1.1215422483834558e-05,
    1.7947762760428532e-06,
    4.4872074833612885e-07,
    7.179791783329392e-08,
    -3.3306690738754696e-16,
    7.180142480578411e-08,
    4.4877554850053514e-07,
    1.7952146817989956e-06,
    1.1222273463173948e-05,
    4.4904612064078364e-05,
    0.00017975739599096485
   ],
   "r_agg_h_VRH": [
    -1.927269426160727e-06,
    -4.831701241325703e-07,
    -7.744114427499227e-08,
    -1.9371617421271026e-08,
    -3.1005531475614134e-09,
    0.0,
    -3.102020196266153e-09,
    -1.9394537975614412e-08,
    -7.762451403880988e-08,
    -4.860355559133112e-07,
    -1.9502008777871893e-06,
    -7.851981527973173e-06
   ],
   "r_agg_E2_HS": [
    4.4678809397069585e-05,
    1.1176229391285375e-05,
    1.788825305437669e-06,
    4.4725879400075996e-07,
    7.156644721284522e-08,
    0.0,
    7.157317116757156e-08,
    4.473638581803385e-07,
    1.7896658166538515e-06,
    1.1189362504993028e-05,
    4.478387799844441e-05,
    0.00017934826780541258
   ],
   "r_agg_E2_V": [
    5.303886886309783e-05,
    1.3252580101541511e-05,
    2.119757117835519e-06,
    5.298858605229384e-07,
    8.477665636164033e-08,
    0.0,
    8.476993551553846e-08,
    5.297808525206449e-07,
    2.1189170456015205e-06,
    1.3239453297675396e-05,
    5.293383506255189e-05,
    0.00021156154497381507
   ],
   "r_agg_E2_R": [
    3.595245572363126e-05,
    9.001389598140008e-06,
    1.441529463352964e-06,
    3.604926654965368e-07,
    5.7689468313526504e-08,
    0.0,
    5.770371869218138e-08,
    3.607153353790693e-07,
    1.4433108375122572e-06,
    9.029225293444298e-06,
    3.617519055709728e-05,
    0.00014518854131018166
   ],
   "lambda_mean_t4": [
    8.585494956968122e-06,
    2.149504412095888e-06,
    3.442368068741232e-07,
    8.608619772748549e-08,
    1.3776408499920126e-08,
    1.4601244111111373e-32,
    1.377992718187533e-08,
    8.614117743261891e-08,
    3.4467665308283026e-07,
    2.156377946320049e-06,
    8.640510019776651e-06,
    3.469232818107467e-05
   ],
   "x_vqSH_t4": [
    10.023308160928295,
    10.032430157717402,
    10.037904279977404,
    10.039729143323793,
    10.040824098986775,
    10.04155408516063,
    10.042284083943612,
    10.043379105804545,
    10.045204205572364,
    10.050679982790257,
    10.059807890256161,
    10.078069893892161
   ],
   "x_vqSV_t4": [
    10.114619777154987,
    10.078069893892167,
    10.056156483546925,
    10.04885464374793,
    10.044474156150082,
    10.041554085160628,
    10.038634215917357,
    10.034254787490369,
    10.02695673049066,
    10.00506980176343,
    9.968614524611981,
    9.89578105533233
   ],
   "x_r_agg_h_HS": [
    -1.9046226722441162e-06,
    -4.777697857338836e-07,
    -7.660156642330662e-08,
    -1.916373604249344e-08,
    -3.0674842665945334e-09,
    0.0,
    -3.069206444550332e-09,
    -1.9190643740785163e-08,
    -7.681682567817205e-08,
    -4.811333683685248e-07,
    -1.9315357753235673e-06,
    -7.784409007616233e-06
   ],
   "S4_E2": -2.6449971836009003e-13,
   "S4_h": 8.407053114138355e-14,
   "kappa44_E2": 0.00017950151355280498,
   "kappa444_E2": 2.1923555007017898e-07,
   "kappa44_h": -7.753635743351712e-06,
   "kappa44_E2_HS": 0.0001789247303803612,
   "halving_dev_kappa44": 1.983162964739032e-09,
   "fit_residual_E2": 1.9662829153101785e-11,
   "x_fit_windows": {
    "n_points_0p25_inclusive": 9,
    "n_points_0p1_inclusive": 7,
    "kappa44_E2_strict_window_0p25": 0.00017949953038984024,
    "n_strict_0p25": 7,
    "kappa44_E2_strict_window_0p1": 0.00017949925734378234,
    "n_strict_0p1": 5,
    "halving_dev_strict": 2.730460579045222e-10
   },
   "biref_b1_VRH": 0.018174297109331976,
   "x_biref_polarization_overlap_min": 1.0,
   "quadform": {
    "kappa22": -0.0018961488929958188,
    "kappa24": -1.8376076624769533e-08,
    "kappa44": 0.0001794926395035944,
    "residual": 1.065120803066407e-09,
    "x_cubic_terms_discarded": [
     -1.2406023432182818e-06,
     -9.831922716422042e-06,
     -3.577712618127711e-06,
     2.1920153310548912e-07
    ],
    "x_grid_r_agg_E2_VRH": [
     -0.00010706773413393655,
     -0.0001155952227629431,
     -0.0001184892325272191,
     -0.00011574697652394494,
     -0.000107365435008,
     -1.834362212749241e-05,
     -2.679430169083563e-05,
     -2.962452855348463e-05,
     -2.6831678121230773e-05,
     -1.8412896608754892e-05,
     1.1215422483834558e-05,
     2.804255680111112e-06,
     -3.3306690738754696e-16,
     2.8051119533856195e-06,
     1.1222273463173948e-05,
     -1.840367901628781e-05,
     -2.6812951251953265e-05,
     -2.9629374222905902e-05,
     -2.6850665423627795e-05,
     -1.847432084567391e-05,
     -0.00010721560863369284,
     -0.00011566093504566943,
     -0.00011852799934330971,
     -0.00011581469909605069,
     -0.00010751871440861649
    ],
    "x_reading": "hex two-parameter family"
   },
   "x_min_odf_weight_5x5": 0.5012432944308812,
   "kappa24_richardson": 9.483155002006545e-13,
   "x_kappa24_richardson_D": {
    "D_0p02": -1.3829215550487106e-10,
    "D_0p01": -3.3861802251067274e-11
   }
  },
  "cubic_step|001": {
   "vT_V": 8.115794477437197,
   "vT_R": 7.468877341686608,
   "vT_VRH": 7.7990463758449255,
   "vT_HS_lo": 7.758614490213423,
   "vT_HS_hi": 7.867953005903455,
   "x_KV_GV_KR_GR": [
    123.8324666666667,
    65.86612000000011,
    123.8324666666664,
    55.78412874515961
   ],
   "kappa2_E2": 3.1015835146880138e-15,
   "x_l2_family": {
    "S2_E2": 7.281757776394048e-16,
    "kappa3_E2": -1.146936681328841e-14,
    "fit_residual": 2.377569989491883e-16,
    "r_agg_E2_VRH_l2": [
     -2.220446049250313e-16,
     2.220446049250313e-16,
     -2.220446049250313e-16,
     -1.1102230246251565e-16,
     0.0,
     2.220446049250313e-16,
     -2.220446049250313e-16,
     -1.1102230246251565e-16,
     0.0,
     2.220446049250313e-16,
     0.0,
     -1.1102230246251565e-16
    ],
    "n_fit_points": 9
   },
   "r_agg_E2_VRH": [
    -9.395389223276762e-05,
    -2.3438263274666582e-05,
    -3.7457754580305647e-06,
    -9.361008703745455e-07,
    -1.497439411357604e-07,
    2.220446049250313e-16,
    -1.497018551344098e-07,
    -9.354432559671721e-07,
    -3.7405139445834124e-06,
    -2.3355986619510993e-05,
    -9.329380310130198e-05,
    -0.00037239373358843864
   ],
   "r_agg_h_VRH": [
    -9.68846050775074e-06,
    -2.3975054874725288e-06,
    -3.8144366354408987e-07,
    -9.518939558805783e-08,
    -1.5214148385567228e-08,
    2.220446049250313e-16,
    -1.5192968327859546e-08,
    -9.485844332246529e-08,
    -3.787956874834464e-07,
    -2.3560916753151417e-06,
    -9.35602667828661e-06,
    -3.6984379914395404e-05
   ],
   "r_agg_E2_HS": [
    -9.763423144681926e-05,
    -2.4368267510732622e-05,
    -3.8951109565532605e-06,
    -9.734623725998759e-07,
    -1.5572379152839488e-07,
    0.0,
    -1.5568364131191004e-07,
    -9.728350243154438e-07,
    -3.890092109215537e-06,
    -2.428984143432178e-05,
    -9.700663450318281e-05,
    -0.00038683591265264994
   ],
   "r_agg_E2_V": [
    -8.656972747855818e-05,
    -2.165779263818557e-05,
    -3.466849738398281e-06,
    -8.668513871157302e-07,
    -1.3870976844909677e-07,
    0.0,
    -1.3872807258508146e-07,
    -8.671373886715017e-07,
    -3.469137797362798e-06,
    -2.169354855874328e-05,
    -8.685591781654178e-05,
    -0.0003481608292099647
   ],
   "r_agg_E2_R": [
    -0.00010266089551080881,
    -2.5539698595755667e-05,
    -4.075082313259593e-06,
    -1.0178631777435498e-06,
    -1.62772200718031e-07,
    0.0,
    -1.626590508951864e-07,
    -1.0160951828819265e-06,
    -4.060937358607575e-06,
    -2.531857463616838e-05,
    -0.00010088878284675307,
    -0.00040089811455579216
   ],
   "lambda_mean_t4": [
    4.609149288923272e-05,
    1.1441973694570702e-05,
    1.8238333906431066e-06,
    4.5542048818039484e-07,
    7.281699249507607e-08,
    2.886965639435218e-32,
    7.27515065186239e-08,
    4.543972233271462e-07,
    1.8156459438818421e-06,
    1.1313899468969845e-05,
    4.506273110522628e-05,
    0.00017918241978269667
   ],
   "x_vqSH_t4": [
    7.8286697387363295,
    7.813841440805378,
    7.804960450386541,
    7.802002757566123,
    7.8002287714909055,
    7.799046375844921,
    7.7978641892518405,
    7.796091300705217,
    7.793137527641544,
    7.7842839760350415,
    7.769553681221708,
    7.740187203363332
   ],
   "x_vqSV_t4": [
    7.681815675870555,
    7.740187203363333,
    7.775441982083123,
    7.787233869781483,
    7.794318880905729,
    7.799046375844923,
    7.803777215636821,
    7.810879787457552,
    7.822734394943356,
    7.858428344081813,
    7.918370223605677,
    8.040093037992495
   ],
   "x_r_agg_h_HS": [
    -1.0507363846112838e-05,
    -2.6022092733946067e-06,
    -4.141111604738512e-07,
    -1.033459262611558e-07,
    -1.6518079348770698e-08,
    0.0,
    -1.649527459068878e-08,
    -1.0298959707277788e-07,
    -4.1126040262184915e-07,
    -2.557652528878407e-06,
    -1.0150519568208338e-05,
    -4.003006102926143e-05
   ],
   "S4_E2": -1.9550561581989927e-11,
   "S4_h": -1.1695158327148078e-11,
   "kappa44_E2": -0.0003743529418199647,
   "kappa444_E2": 2.633164259954152e-06,
   "kappa44_h": -3.8028327671478075e-05,
   "kappa44_E2_HS": -0.0003892647453545792,
   "halving_dev_kappa44": 3.881410404427089e-08,
   "fit_residual_E2": 3.8516937287863786e-10,
   "x_fit_windows": {
    "n_points_0p25_inclusive": 9,
    "n_points_0p1_inclusive": 7,
    "kappa44_E2_strict_window_0p25": -0.0003743141277159204,
    "n_strict_0p25": 7,
    "kappa44_E2_strict_window_0p1": -0.00037430878583169736,
    "n_strict_0p1": 5,
    "halving_dev_strict": 5.3418842230505345e-09
   },
   "biref_b1_VRH": -0.0378987033959945,
   "x_biref_polarization_overlap_min": 1.0,
   "quadform": {
    "kappa22": 4.48191140345094e-09,
    "kappa24": 1.974043382091395e-07,
    "kappa44": -0.00037435455939083614,
    "residual": 4.681631408729078e-09,
    "x_cubic_terms_discarded": [
     3.641053119147632e-09,
     -1.7049900348209627e-10,
     -5.901878166287058e-05,
     2.6329133467859226e-06
    ],
    "x_grid_r_agg_E2_VRH": [
     -2.250161467498568e-05,
     -5.62161334682898e-06,
     2.220446049250313e-16,
     -5.614963276112661e-06,
     -2.2448368848349e-05,
     -2.296993897477062e-05,
     -5.737740866873509e-06,
     2.220446049250313e-16,
     -5.7292771964423395e-06,
     -2.2902177733929996e-05,
     -2.3438263274666582e-05,
     -5.8538683869180375e-06,
     2.220446049250313e-16,
     -5.84359111688304e-06,
     -2.3355986619510993e-05,
     -2.3906587574007432e-05,
     -5.969995906629499e-06,
     2.220446049250313e-16,
     -5.957905037323741e-06,
     -2.3809795504758924e-05,
     -2.437491187379237e-05,
     -6.086123426451984e-06,
     2.220446049250313e-16,
     -6.072218957542397e-06,
     -2.4263604390561966e-05
    ],
    "x_reading": "(i) inherited descriptor-axis P2 (A-3.3)"
   },
   "x_min_odf_weight_5x5": 0.5012432318877168,
   "kappa24_richardson": -7.632783294297951e-13,
   "x_kappa24_richardson_D": {
    "D_0p02": 1.4855477958874985e-09,
    "D_0p01": 3.708144902248023e-10
   },
   "x_quadform_reading_ii_Oh_symmetrized": {
    "kappa22": 4.481910076277481e-09,
    "kappa24": 0.0,
    "kappa44": -0.0003743545593927722,
    "residual": 5.640124744696825e-10,
    "x_cubic_terms_discarded": [
     5.874795163635559e-20,
     -1.7048980812178564e-10,
     2.3092588281654192e-20,
     2.6329133467859e-06
    ]
   }
  },
  "cubic_step|111": {
   "vT_V": 8.115794477437197,
   "vT_R": 7.468877341686608,
   "vT_VRH": 7.7990463758449255,
   "vT_HS_lo": 7.758614490213423,
   "vT_HS_hi": 7.867953005903455,
   "x_KV_GV_KR_GR": [
    123.8324666666667,
    65.86612000000011,
    123.8324666666664,
    55.78412874515961
   ],
   "kappa2_E2": 2.87608926272809e-15,
   "x_l2_family": {
    "S2_E2": 6.653947455025535e-17,
    "kappa3_E2": -1.1119718263637282e-15,
    "fit_residual": 2.56347473180974e-16,
    "r_agg_E2_VRH_l2": [
     -1.1102230246251565e-16,
     2.220446049250313e-16,
     -2.220446049250313e-16,
     0.0,
     -1.1102230246251565e-16,
     2.220446049250313e-16,
     2.220446049250313e-16,
     -1.1102230246251565e-16,
     -2.220446049250313e-16,
     2.220446049250313e-16,
     -1.1102230246251565e-16,
     0.0
    ],
    "n_fit_points": 9
   },
   "r_agg_E2_VRH": [
    6.263592815503038e-05,
    1.5625508849259617e-05,
    2.497183638094924e-06,
    6.240672469903785e-07,
    9.98292941645218e-08,
    2.220446049250313e-16,
    9.980123660824347e-08,
    6.236288374594778e-07,
    2.4936759630556082e-06,
    1.5570657746266647e-05,
    6.219586873434935e-05,
    0.00024826248905873705
   ],
   "r_agg_h_VRH": [
    -9.68846050775074e-06,
    -2.3975054874725288e-06,
    -3.8144366354408987e-07,
    -9.518939558805783e-08,
    -1.5214148385567228e-08,
    2.220446049250313e-16,
    -1.5192968327859546e-08,
    -9.485844332246529e-08,
    -3.787956874834464e-07,
    -2.3560916753151417e-06,
    -9.35602667828661e-06,
    -3.6984379914395404e-05
   ],
   "r_agg_E2_HS": [
    6.508948763128686e-05,
    1.6245511674117807e-05,
    2.5967406376281588e-06,
    6.489749151405988e-07,
    1.0381586079688532e-07,
    0.0,
    1.0378909398589542e-07,
    6.48556682580903e-07,
    2.5933947391809653e-06,
    1.6193227622585127e-05,
    6.467108966901058e-05,
    0.000257890608435396
   ],
   "r_agg_E2_V": [
    5.7713151652150074e-05,
    1.4438528425086972e-05,
    2.3112331584140833e-06,
    5.779009244477606e-07,
    9.247317867000504e-08,
    0.0,
    9.24853813533133e-08,
    5.780915923736529e-07,
    2.3127585311311094e-06,
    1.4462365705680824e-05,
    5.790394521065778e-05,
    0.00023210721947308777
   ],
   "r_agg_E2_R": [
    6.844059700750194e-05,
    1.7026465730429763e-05,
    2.7167215417289725e-06,
    6.785754516069886e-07,
    1.0851480047868733e-07,
    0.0,
    1.0843936770754681e-07,
    6.773967882178766e-07,
    2.7072915724790647e-06,
    1.687904975722354e-05,
    6.725918856487212e-05,
    0.0002672654097037874
   ],
   "lambda_mean_t4": [
    4.609149288923272e-05,
    1.1441973694570702e-05,
    1.8238333906431066e-06,
    4.5542048818039484e-07,
    7.281699249507607e-08,
    2.886965639435218e-32,
    7.27515065186239e-08,
    4.543972233271462e-07,
    1.8156459438818421e-06,
    1.1313899468969845e-05,
    4.506273110522628e-05,
    0.00017918241978269667
   ],
   "x_vqSH_t4": [
    7.8286697387363295,
    7.813841440805378,
    7.804960450386541,
    7.802002757566123,
    7.8002287714909055,
    7.799046375844921,
    7.7978641892518405,
    7.796091300705217,
    7.793137527641544,
    7.7842839760350415,
    7.769553681221708,
    7.740187203363332
   ],
   "x_vqSV_t4": [
    7.681815675870555,
    7.740187203363333,
    7.775441982083123,
    7.787233869781483,
    7.794318880905729,
    7.799046375844923,
    7.803777215636821,
    7.810879787457552,
    7.822734394943356,
    7.858428344081813,
    7.918370223605677,
    8.040093037992495
   ],
   "x_r_agg_h_HS": [
    -1.0507363846112838e-05,
    -2.6022092733946067e-06,
    -4.141111604738512e-07,
    -1.033459262611558e-07,
    -1.6518079348770698e-08,
    0.0,
    -1.649527459068878e-08,
    -1.0298959707277788e-07,
    -4.1126040262184915e-07,
    -2.557652528878407e-06,
    -1.0150519568208338e-05,
    -4.003006102926143e-05
   ],
   "S4_E2": 1.3036078957132319e-11,
   "S4_h": -1.1695158327148078e-11,
   "kappa44_E2": 0.00024956862787469286,
   "kappa444_E2": -1.7554428634061992e-06,
   "kappa44_h": -3.8028327671478075e-05,
   "kappa44_E2_HS": 0.00025950983023583375,
   "halving_dev_kappa44": 2.5876089432676306e-08,
   "fit_residual_E2": 2.567799075151687e-10,
   "x_fit_windows": {
    "n_points_0p25_inclusive": 9,
    "n_points_0p1_inclusive": 7,
    "kappa44_E2_strict_window_0p25": 0.0002495427517852602,
    "n_strict_0p25": 7,
    "kappa44_E2_strict_window_0p1": 0.000249539190595456,
    "n_strict_0p1": 5,
    "halving_dev_strict": 3.5611898042010176e-09
   },
   "biref_b1_VRH": -0.0378987033959945,
   "x_biref_polarization_overlap_min": 1.0,
   "quadform": {
    "kappa22": -2.987937980693619e-09,
    "kappa24": 1.9740433813807004e-07,
    "kappa44": 0.00024956970625728664,
    "residual": 4.587444687234791e-09,
    "x_cubic_terms_discarded": [
     3.641059720302595e-09,
     1.1367343055093113e-10,
     -5.9018781674654424e-05,
     -1.7552755590229606e-06
    ],
    "x_grid_r_agg_E2_VRH": [
     1.656215744905154e-05,
     4.134833963886919e-06,
     2.220446049250313e-16,
     4.124355251766687e-06,
     1.647827551787273e-05,
     1.6093833149044556e-05,
     4.018706444064435e-06,
     2.220446049250313e-16,
     4.010041331437009e-06,
     1.60244666316256e-05,
     1.5625508849259617e-05,
     3.902578924019906e-06,
     2.220446049250313e-16,
     3.89572741110733e-06,
     1.5570657746266647e-05,
     1.5157184549918767e-05,
     3.7864514044194664e-06,
     2.220446049250313e-16,
     3.7814134909996966e-06,
     1.511684886068565e-05,
     1.4688860249911784e-05,
     3.670323884596982e-06,
     2.220446049250313e-16,
     3.6670995706700182e-06,
     1.4663039975326697e-05
    ],
    "x_reading": "(i) inherited descriptor-axis P2 (A-3.3)"
   },
   "x_min_odf_weight_5x5": 0.592308427039737,
   "kappa24_richardson": -2.220446049250313e-12,
   "x_kappa24_richardson_D": {
    "D_0p02": 1.4854784069484595e-09,
    "D_0p01": 3.6970426720017713e-10
   },
   "x_quadform_reading_ii_Oh_symmetrized": {
    "kappa22": -2.987940326556023e-09,
    "kappa24": 0.0,
    "kappa44": 0.00024956970625615875,
    "residual": 3.7600879804673443e-10,
    "x_cubic_terms_discarded": [
     -1.278985071649335e-19,
     1.13668932575448e-10,
     1.3937789601430342e-19,
     -1.75527555352198e-06
    ]
   }
  },
  "cubic_gem8|001": {
   "vT_V": 9.872492086601033,
   "vT_R": 8.70677152783136,
   "vT_VRH": 9.307899076533191,
   "vT_HS_lo": 9.21172106438435,
   "vT_HS_hi": 9.456854984586533,
   "x_KV_GV_KR_GR": [
    210.2755,
    97.46610000000004,
    210.2755000000005,
    75.80787043785483
   ],
   "kappa2_E2": 1.1537558658562911e-15,
   "x_l2_family": {
    "S2_E2": -6.562240873197596e-17,
    "kappa3_E2": 8.150081301186718e-15,
    "fit_residual": 2.3517000401158335e-16,
    "r_agg_E2_VRH_l2": [
     -2.220446049250313e-16,
     0.0,
     -2.220446049250313e-16,
     0.0,
     -2.220446049250313e-16,
     2.220446049250313e-16,
     -2.220446049250313e-16,
     0.0,
     -2.220446049250313e-16,
     2.220446049250313e-16,
     2.220446049250313e-16,
     0.0
    ],
    "n_fit_points": 9
   },
   "r_agg_E2_VRH": [
    -0.0001128590449820388,
    -2.813923524602746e-05,
    -4.4958779480408495e-06,
    -1.1234705115104049e-06,
    -1.7970867827177273e-07,
    2.220446049250313e-16,
    -1.796480418869706e-07,
    -1.1225230265310415e-06,
    -4.488296764137978e-06,
    -2.802063627083129e-05,
    -0.00011190615454581554,
    -0.0004466673069931648
   ],
   "r_agg_h_VRH": [
    -1.1590815615636352e-05,
    -2.8629911530408947e-06,
    -4.5509719315273145e-07,
    -1.1353983020434555e-07,
    -1.814438921332595e-08,
    0.0,
    -1.8115683841912755e-08,
    -1.130912825608732e-07,
    -4.515080812561578e-07,
    -2.806831356338968e-06,
    -1.1139242344526679e-05,
    -4.402897117872229e-05
   ],
   "r_agg_E2_HS": [
    -0.00011966081632830416,
    -2.9853890737618904e-05,
    -4.770848111679271e-06,
    -1.1922353594373547e-06,
    -1.907120691369002e-07,
    0.0,
    -1.9065148337826798e-07,
    -1.1912887032394792e-06,
    -4.7632747116610474e-06,
    -2.9735539746722495e-05,
    -0.0001187135331985889,
    -0.00047308544542767894
   ],
   "r_agg_E2_V": [
    -0.0001025974209527547,
    -2.5669950862838853e-05,
    -4.109380245309602e-06,
    -1.027536250752803e-06,
    -1.64424495130433e-07,
    0.0,
    -1.6444982087193694e-07,
    -1.027931961994355e-06,
    -4.112546025059061e-06,
    -2.571942578966091e-05,
    -0.00010299349550801917,
    -0.00041303837751849315
   ],
   "r_agg_E2_R": [
    -0.00012602643602821484,
    -3.131218838081651e-05,
    -4.9927336920330134e-06,
    -1.246807165178332e-06,
    -1.9935923512015563e-07,
    0.0,
    -1.991885777430369e-07,
    -1.2441405583540899e-06,
    -4.97139859201301e-06,
    -3.097858158174205e-05,
    -0.0001233505383476663,
    -0.0004896609150401021
   ],
   "lambda_mean_t4": [
    4.904032907764078e-05,
    1.2153699959364867e-05,
    1.93574973746057e-06,
    4.832554553198263e-07,
    7.725747039747598e-08,
    1.7881190712790638e-32,
    7.71753230516142e-08,
    4.819718164432939e-07,
    1.9254781517300095e-06,
    1.1992935409003581e-05,
    4.7746428880319185e-05,
    0.0001898970959331191
   ],
   "x_vqSH_t4": [
    9.350344912225461,
    9.329093655815193,
    9.316370184203885,
    9.312133516080836,
    9.3095925855339,
    9.307899076533191,
    9.306205922579213,
    9.303666856029864,
    9.299436845071506,
    9.286759974945172,
    9.265675171442178,
    9.22366383642728
   ],
   "x_vqSV_t4": [
    9.140242928223895,
    9.223663836427281,
    9.274102651758323,
    9.290983413949936,
    9.3011285849161,
    9.307899076533193,
    9.314675248914305,
    9.324850244459974,
    9.341837530802305,
    9.393022356361138,
    9.479112467990138,
    9.654537112754017
   ],
   "x_r_agg_h_HS": [
    -1.3122808741106162e-05,
    -3.2443178208385604e-06,
    -5.158176553665683e-07,
    -1.2869057297582032e-07,
    -2.0565501634983718e-08,
    0.0,
    -2.0532573419274058e-08,
    -1.281760627636075e-07,
    -5.117012934485743e-07,
    -3.1799690708433914e-06,
    -1.2607143399345766e-05,
    -4.9646877244069465e-05
   ],
   "S4_E2": -4.267032120491424e-11,
   "S4_h": -2.3853273799039695e-11,
   "kappa44_E2": -0.00044927709343161725,
   "kappa444_E2": 3.7958466267304677e-06,
   "kappa44_h": -4.5357822665197825e-05,
   "kappa44_E2_HS": -0.00047671519504299364,
   "halving_dev_kappa44": 6.896611766469673e-08,
   "fit_residual_E2": 6.845658699329788e-10,
   "x_fit_windows": {
    "n_points_0p25_inclusive": 9,
    "n_points_0p1_inclusive": 7,
    "kappa44_E2_strict_window_0p25": -0.00044920812731395255,
    "n_strict_0p25": 7,
    "kappa44_E2_strict_window_0p1": -0.00044919863753253587,
    "n_strict_0p1": 5,
    "halving_dev_strict": 9.489781416683208e-09
   },
   "biref_b1_VRH": -0.045481252227733915,
   "x_biref_polarization_overlap_min": 1.0,
   "quadform": {
    "kappa22": 7.963760249103659e-09,
    "kappa24": 3.477857238464886e-07,
    "kappa44": -0.0004492799676061741,
    "residual": 8.27241502064556e-09,
    "x_cubic_terms_discarded": [
     7.94404069994542e-09,
     -3.7210027738773715e-10,
     -8.510772973814659e-05,
     3.7952989894238772e-06
    ],
    "x_grid_r_agg_E2_VRH": [
     -2.6783930420104518e-05,
     -6.690981583457045e-06,
     0.0,
     -6.682561632942452e-06,
     -2.671647848284664e-05,
     -2.7461582832954967e-05,
     -6.858695032030404e-06,
     2.220446049250313e-16,
     -6.8470805999476525e-06,
     -2.7368557376838965e-05,
     -2.813923524602746e-05,
     -7.026408480825808e-06,
     2.220446049250313e-16,
     -7.0115995675079645e-06,
     -2.802063627083129e-05,
     -2.8816887658988932e-05,
     -7.194121929177122e-06,
     0.0,
     -7.176118534180098e-06,
     -2.867271516504566e-05,
     -2.9494540072172448e-05,
     -7.3618353776394585e-06,
     2.220446049250313e-16,
     -7.340637501407343e-06,
     -2.9324794059037984e-05
    ],
    "x_reading": "(i) inherited descriptor-axis P2 (A-3.3)"
   },
   "x_min_odf_weight_5x5": 0.5012432318877168,
   "kappa24_richardson": 1.2027416100105863e-12,
   "x_kappa24_richardson_D": {
    "D_0p02": 2.6165181132853377e-09,
    "D_0p01": 6.550315845288424e-10
   },
   "x_quadform_reading_ii_Oh_symmetrized": {
    "kappa22": 7.963758508465077e-09,
    "kappa24": 0.0,
    "kappa44": -0.0004492799676052757,
    "residual": 1.0037063528647863e-09,
    "x_cubic_terms_discarded": [
     1.0832008566002682e-20,
     -3.7210446234290756e-10,
     -9.542907645354657e-21,
     3.7952989932745593e-06
    ]
   }
  },
  "cubic_gem8|111": {
   "vT_V": 9.872492086601033,
   "vT_R": 8.70677152783136,
   "vT_VRH": 9.307899076533191,
   "vT_HS_lo": 9.21172106438435,
   "vT_HS_hi": 9.456854984586533,
   "x_KV_GV_KR_GR": [
    210.2755,
    97.46610000000004,
    210.2755000000005,
    75.80787043785483
   ],
   "kappa2_E2": -4.371545007321201e-16,
   "x_l2_family": {
    "S2_E2": -9.55080497404575e-16,
    "kappa3_E2": 1.5179666171081875e-14,
    "fit_residual": 2.6680828527204455e-16,
    "r_agg_E2_VRH_l2": [
     0.0,
     0.0,
     0.0,
     -2.220446049250313e-16,
     -2.220446049250313e-16,
     2.220446049250313e-16,
     -2.220446049250313e-16,
     -2.220446049250313e-16,
     -2.220446049250313e-16,
     0.0,
     2.220446049250313e-16,
     2.220446049250313e-16
    ],
    "n_fit_points": 9
   },
   "r_agg_E2_VRH": [
    7.523936332098913e-05,
    1.8759490163722248e-05,
    2.997251965064507e-06,
    7.489803408589069e-07,
    1.1980578529247055e-07,
    2.220446049250313e-16,
    1.1976536118396552e-07,
    7.483486843540277e-07,
    2.9921978423885776e-06,
    1.8680424180406163e-05,
    7.460410303061771e-05,
    0.00029777820466247995
   ],
   "r_agg_h_VRH": [
    -1.1590815615636352e-05,
    -2.8629911530408947e-06,
    -4.5509719315273145e-07,
    -1.1353983020434555e-07,
    -1.814438921332595e-08,
    0.0,
    -1.8115683841912755e-08,
    -1.130912825608732e-07,
    -4.515080812561578e-07,
    -2.806831356338968e-06,
    -1.1139242344526679e-05,
    -4.402897117872229e-05
   ],
   "r_agg_E2_HS": [
    7.977387755198073e-05,
    1.990259382478321e-05,
    3.1805654074901213e-06,
    7.948235725141473e-07,
    1.2714137920255553e-07,
    0.0,
    1.2710098884483045e-07,
    7.941924689003343e-07,
    3.1755164742186537e-06,
    1.9823693164333633e-05,
    7.914235546579995e-05,
    0.0003153902969514899
   ],
   "r_agg_E2_V": [
    6.83982806346517e-05,
    1.7113300575299917e-05,
    2.7395868300583714e-06,
    6.850241667244461e-07,
    1.0961633023498507e-07,
    0.0,
    1.0963321339652055e-07,
    6.852879745888885e-07,
    2.741697349817329e-06,
    1.714628385962591e-05,
    6.866233033830937e-05,
    0.000275358918345292
   ],
   "r_agg_E2_R": [
    8.401762401821777e-05,
    2.0874792253877672e-05,
    3.32848912742989e-06,
    8.312047763414654e-07,
    1.3290615674677042e-07,
    0.0,
    1.3279238464392051e-07,
    8.294270390507563e-07,
    3.3142657278606436e-06,
    2.065238772153144e-05,
    8.223369223170351e-05,
    0.0003264406100265127
   ],
   "lambda_mean_t4": [
    4.904032907764078e-05,
    1.2153699959364867e-05,
    1.93574973746057e-06,
    4.832554553198263e-07,
    7.725747039747598e-08,
    1.7881190712790638e-32,
    7.71753230516142e-08,
    4.819718164432939e-07,
    1.9254781517300095e-06,
    1.1992935409003581e-05,
    4.7746428880319185e-05,
    0.0001898970959331191
   ],
   "x_vqSH_t4": [
    9.350344912225461,
    9.329093655815193,
    9.316370184203885,
    9.312133516080836,
    9.3095925855339,
    9.307899076533191,
    9.306205922579213,
    9.303666856029864,
    9.299436845071506,
    9.286759974945172,
    9.265675171442178,
    9.22366383642728
   ],
   "x_vqSV_t4": [
    9.140242928223895,
    9.223663836427281,
    9.274102651758323,
    9.290983413949936,
    9.3011285849161,
    9.307899076533193,
    9.314675248914305,
    9.324850244459974,
    9.341837530802305,
    9.393022356361138,
    9.479112467990138,
    9.654537112754017
   ],
   "x_r_agg_h_HS": [
    -1.3122808741106162e-05,
    -3.2443178208385604e-06,
    -5.158176553665683e-07,
    -1.2869057297582032e-07,
    -2.0565501634983718e-08,
    0.0,
    -2.0532573419274058e-08,
    -1.281760627636075e-07,
    -5.117012934485743e-07,
    -3.1799690708433914e-06,
    -1.2607143399345766e-05,
    -4.9646877244069465e-05
   ],
   "S4_E2": 2.844703507492917e-11,
   "S4_h": -2.3853273799039695e-11,
   "kappa44_E2": 0.00029951806228339543,
   "kappa444_E2": -2.5305644157388242e-06,
   "kappa44_h": -4.5357822665197825e-05,
   "kappa44_E2_HS": 0.00031781013002442837,
   "halving_dev_kappa44": 4.597744102265546e-08,
   "fit_residual_E2": 4.5637748167913443e-10,
   "x_fit_windows": {
    "n_points_0p25_inclusive": 9,
    "n_points_0p1_inclusive": 7,
    "kappa44_E2_strict_window_0p25": 0.0002994720848423728,
    "n_strict_0p25": 7,
    "kappa44_E2_strict_window_0p1": 0.00029946575831691963,
    "n_strict_0p1": 5,
    "halving_dev_strict": 6.326525453146346e-09
   },
   "biref_b1_VRH": -0.045481252227733915,
   "x_biref_polarization_overlap_min": 1.0,
   "quadform": {
    "kappa22": -5.309171208626909e-09,
    "kappa24": 3.47785722141147e-07,
    "kappa44": 0.0002995199784012639,
    "residual": 8.104726731325246e-09,
    "x_cubic_terms_discarded": [
     7.944032815079988e-09,
     2.4807098986342795e-10,
     -8.510772972257114e-05,
     -2.530199325182433e-06
    ],
    "x_grid_r_agg_E2_VRH": [
     2.011479498964519e-05,
     5.019699217623241e-06,
     0.0,
     5.003437645978437e-06,
     1.9984581968612858e-05,
     1.943714257679474e-05,
     4.85198576893886e-06,
     4.440892098500626e-16,
     4.8389186786401694e-06,
     1.9332503074620533e-05,
     1.8759490163722248e-05,
     4.684272320254479e-06,
     2.220446049250313e-16,
     4.674399711523947e-06,
     1.8680424180406163e-05,
     1.8081837751315888e-05,
     4.5165588722362315e-06,
     2.220446049250313e-16,
     4.509880744407724e-06,
     1.8028345286635883e-05,
     1.7404185337799305e-05,
     4.34884542355185e-06,
     0.0,
     4.345361777291501e-06,
     1.7376266392421513e-05
    ],
    "x_reading": "(i) inherited descriptor-axis P2 (A-3.3)"
   },
   "x_min_odf_weight_5x5": 0.592308427039737,
   "kappa24_richardson": -3.7007434154171886e-13,
   "x_kappa24_richardson_D": {
    "D_0p02": 2.616795669041494e-09,
    "D_0p01": 6.539213615042172e-10
   },
   "x_quadform_reading_ii_Oh_symmetrized": {
    "kappa22": -5.309171561986808e-09,
    "kappa24": 0.0,
    "kappa44": 0.0002995199783988804,
    "residual": 6.691377850242178e-10,
    "x_cubic_terms_discarded": [
     -1.0564719868000641e-19,
     2.480726617119792e-10,
     1.1060923802608755e-19,
     -2.53019932518239e-06
    ]
   }
  }
 },
 "phase3": {
  "verdict_class": "IDENTITY-DELIVERED-L4",
  "F-MS2-3": "SILENT",
  "F-MS2-4": "SILENT",
  "F-MS2-2": "REGISTERED_NOT_EXECUTED",
  "worst_S4": 4.267032120491424e-11
 },
 "extras": {
  "method": {
   "so3_route": "fiber-axis: analytic SO(2) coset average (TI projector for tensors; closed-form psi moments for the E2 weight) x S^2 rule GL(cos theta) 16 x uniform phi 32 over the crystal-frame fiber axis, node set rotated by a fixed generic rotation",
   "so3_exact_degree": 31,
   "n_fiber_nodes": 512,
   "k_rule": "GL(cos theta) 64 x uniform phi 128 (pinned)",
   "n_rule": "GL 12 x 24 (pinned)",
   "fracE2": "(1 - (k.n)^2)(1 - (ehat_perp.n)^2)",
   "hs_optimizer": "boundary-K0 bisection + 600-point coarse scan + 9 nested 21-point refinements over G0",
   "fit_windows": "|t4| <= 0.25 (9 points) and |t4| <= 0.1 (7 points), inclusive (G-MSCS1 convention); strict-window fits in phase2[key].x_fit_windows",
   "cubic_two_parameter_reading": "(i) inherited descriptor-axis P2 (A-3.3); reading (ii) in phase2[key].x_quadform_reading_ii_Oh_symmetrized"
  },
  "selftests": {
   "mandel_rotation_dev": 2.6645352591003757e-15,
   "ti_projector_vs_psi_average_dev": 6.661338147750939e-16,
   "fiber_rule_iso_dev": 1.3322676295501878e-15,
   "K4_mean": 4.0766001685454967e-17,
   "K4_sq_mean_minus_4_21": -5.551115123125783e-17,
   "P4_sq_mean_minus_1_9": -2.7755575615628914e-17,
   "K6_mean": 1.5612511283791264e-15,
   "K6_K4_overlap": 1.1319070680748666e-16,
   "P2_mean": 3.2959746043559335e-17,
   "K4_range": [
    -0.6650100702867094,
    0.9961753204696011
   ],
   "fracE2_closed_form_dev": 6.800116025829084e-16,
   "psi_moment_closed_form_dev": 2.220446049250313e-16,
   "T4_voigt_table_dev": 1.3877787807814457e-17
  },
  "hs_references": {
   "hex_step": {
    "lo_K0_G0_GHS": [
     134.60708943792756,
     60.030800002397555,
     70.40652703755302
    ],
    "hi_K0_G0_GHS": [
     135.3665900803748,
     115.55987439270903,
     70.9735889413121
    ]
   },
   "hex_step|b": {
    "lo_K0_G0_GHS": [
     134.60708943792758,
     60.030800002600856,
     70.41030322863422
    ],
    "hi_K0_G0_GHS": [
     135.3665893814545,
     115.55987454112007,
     70.97730993134309
    ]
   },
   "hex_gem8": {
    "lo_K0_G0_GHS": [
     229.69575433713962,
     84.82450000252788,
     99.8183426049691
    ],
    "hi_K0_G0_GHS": [
     230.13605574483987,
     178.2943403296807,
     101.05874270188906
    ]
   },
   "hex_gem8|b": {
    "lo_K0_G0_GHS": [
     229.69575433713962,
     84.8245000038631,
     99.81488234518235
    ],
    "hi_K0_G0_GHS": [
     230.13605492810942,
     178.29434048781673,
     101.05536909849488
    ]
   },
   "cubic_step": {
    "lo_K0_G0_GHS": [
     123.83246666828633,
     36.72520000144275,
     60.19609880774969
    ],
    "hi_K0_G0_GHS": [
     123.83246666504702,
     85.29339999837849,
     61.904684503105194
    ]
   },
   "cubic_gem8": {
    "lo_K0_G0_GHS": [
     210.27550000263054,
     46.34985000384669,
     84.85580496802234
    ],
    "hi_K0_G0_GHS": [
     210.27549999736948,
     131.5435999975429,
     89.4321061994992
    ]
   }
  },
  "A3_diagnostics": {
   "A-3.1_mixed_r_agg_change_A29": {
    "cubic_step|001": -9.076177710509725e-07,
    "cubic_step|111": -9.076177709399502e-07,
    "cubic_gem8|001": -1.3041577882066946e-06,
    "cubic_gem8|111": -1.30415778798465e-06
   },
   "A-3.2_kappa24_richardson": {
    "hex_step|a": 3.006854025026466e-13,
    "hex_step|b": 1.8503717077085943e-13,
    "hex_gem8|a": 1.3646491344350882e-12,
    "hex_gem8|b": 9.483155002006545e-13,
    "cubic_step|001": -7.632783294297951e-13,
    "cubic_step|111": -2.220446049250313e-12,
    "cubic_gem8|001": 1.2027416100105863e-12,
    "cubic_gem8|111": -3.7007434154171886e-13
   },
   "A-3.3_reading": "(i) inherited descriptor-axis P2"
  },
  "biref_voigt_identity_cubic": {
   "cubic_step|001": {
    "vqSH2_minus_vqSV2_voigt": -0.23127714285708123,
    "H_t4_over_21": -0.23127714285714293,
    "rel_residual": 2.667822848004258e-13
   },
   "cubic_step|111": {
    "vqSH2_minus_vqSV2_voigt": -0.23127714285708123,
    "H_t4_over_21": -0.23127714285714293,
    "rel_residual": 2.667822848004258e-13
   },
   "cubic_gem8|001": {
    "vqSH2_minus_vqSV2_voigt": -0.4056845238094411,
    "H_t4_over_21": -0.40568452380952374,
    "rel_residual": 2.0374478032135002e-13
   },
   "cubic_gem8|111": {
    "vqSH2_minus_vqSV2_voigt": -0.4056845238094411,
    "H_t4_over_21": -0.40568452380952374,
    "rel_residual": 2.0374478032135002e-13
   }
  },
  "so3_control_mean_F0_by_key": [
   0.39999999999999997,
   0.39999999999999997,
   0.39999999999999997,
   0.39999999999999997,
   0.39999999999999997,
   0.39999999999999997,
   0.39999999999999997,
   0.39999999999999997
  ],
  "elapsed_seconds": 170.003
 }
}
=====END-EMBED name=inputs/gmscs2_gate/g_mscs2_ccleg_checkpoint.json=====

=====BEGIN-EMBED name=inputs/gmscs1_gate/g_mscs1_chatleg_checkpoint.json md5=c04c0b8ea34cfe60f231aa06828e6ce4 bytes=33289 encoding=raw=====
{
 "gate": "G-MSCS1",
 "leg": "chat",
 "instrument": "g_mscs1_chatleg.py",
 "instrument_md5": "db5f51dd9ef7f54dd0826991d594681b",
 "memo_md5": "3f30262eaec461fb5fd3202835f7de37",
 "memo_bytes": 34837,
 "ledger_base_md5": "d095a7003bb0d4c177e7451e1d14c4c6",
 "utc": "2026-09-19T22:54:03.606899+00:00",
 "elections": {
  "E-MS-1": "(a) two descriptors of the one transverse field; S2-E2 primary, S2-h second arm",
  "E-MS-2": "(a) all four configurations",
  "E-MS-2b": "(a+b) banked tetragonal-form primary; symmetrized C66 second arm",
  "E-MS-2c": "(001+111) <001> primary, <111> reported",
  "E-MS-3": "(a) VRH/HS leading order; Born at t = 0 only; texture sweep",
  "E-MS-4": "(a) table + lambda_L",
  "E-MS-5": "(a) fiber ODF 1 + t P2, t in [-1, 2]",
  "E-MS-6": "(a) no observational contact"
 },
 "T1": {
  "list_md5": "fef2827100d3f85e0a6341b44f0c00bf",
  "state": "CLEAN",
  "numeric_collisions": 0,
  "files": [
   "g_mscs1_chatleg.py",
   "staging_memo_G_MSCS1_v2.md"
  ]
 },
 "inputs": {
  "X1_md5": "200e7a8b775577564369c6924d38a84c",
  "X1_bytes": 2767,
  "X3_md5": "aaae206733b0f0a378a5c6b600274d3f",
  "X4_md5": "ec87e42f0f617b00c4985ba2aceac339",
  "X5_md5": "df413a7cfa30e599b779af8fee5d07d1"
 },
 "quadrature": {
  "n_theta": 64,
  "n_phi": 128,
  "doubling_residual": 1.7763568394002505e-15,
  "so3_grid": [
   16,
   10,
   16
  ],
  "n_grid": [
   12,
   24
  ]
 },
 "t_grid": [
  -0.5,
  -0.25,
  -0.1,
  -0.05,
  -0.02,
  0.0,
  0.02,
  0.05,
  0.1,
  0.25,
  0.5,
  1.0
 ],
 "controls": {
  "F-CTRL-ISO": {
   "r_xtal_E2": 2.220446049250313e-16,
   "r_xtal_h": 0.0,
   "lambda_max": 5.8657280953489826e-31,
   "r_agg_max": 4.440892098500626e-16,
   "passed": true
  },
  "F-CTRL-SO3": {
   "w_S2_mean_t0": 0.39999999999999997,
   "dev_from_0p4": 4.996003610813204e-16,
   "r_agg_0_E2": 0.0,
   "passed": true
  },
  "F-CTRL-TEX": {
   "r_agg_t1": 0.0025019145217410887,
   "passed": true
  },
  "PIN-A2AGG": {
   "worst_rel_residual": 6.275451101635372e-14,
   "passed": true
  },
  "F-CTRL-POL": {
   "split_plus_minus": 0.0,
   "split_plus_avg": 4.799045625554363e-16,
   "passed": true
  },
  "F-CTRL-ADMIX": {
   "r_xtal_h_projected": 0.0,
   "passed": true
  },
  "PIN-VRH0": {
   "worst_rel_residual": 1.3982193552955251e-14,
   "passed": true
  },
  "PIN-HS0": {
   "worst_rel_residual": 1.601689060021389e-12,
   "passed": true
  }
 },
 "pins_vrh0": {
  "hex_step": {
   "GV": 73.06453333333313,
   "GR": 68.69659702931501,
   "KV": 134.60928888888833,
   "KR": 134.60823359538983,
   "worst_rel": 4.222845193672222e-15,
   "G_HS": [
    70.40652703753862,
    70.97358894132181
   ],
   "hs_ref": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   }
  },
  "hex_gem8": {
   "GV": 105.041953333333,
   "GR": 96.63040078152201,
   "KV": 229.69615555555526,
   "KR": 229.69594530872757,
   "worst_rel": 1.3982193552955251e-14,
   "G_HS": [
    99.81834260496358,
    101.05874270190839
   ],
   "hs_ref": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   }
  },
  "cubic_step": {
   "GV": 65.86612000000007,
   "GR": 55.78412874515959,
   "KV": 123.83246666666679,
   "KR": 123.83246666666577,
   "worst_rel": 7.688833886201092e-15,
   "G_HS": [
    60.196098807713454,
    61.904684503125985
   ],
   "hs_ref": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   },
   "hs_band_rel": 8.404305891603147e-13
  },
  "cubic_gem8": {
   "GV": 97.46609999999977,
   "GR": 75.80787043785469,
   "KV": 210.27549999999948,
   "KR": 210.27549999999925,
   "worst_rel": 3.784596227574358e-15,
   "G_HS": [
    84.85580496777382,
    89.43210619954085
   ],
   "hs_ref": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   },
   "hs_band_rel": 1.601689060021389e-12
  }
 },
 "born_t0": {
  "hex_step": {
   "D0_plus": -0.02052824459532726,
   "D0_minus": -0.02052824459532726,
   "D0_avg": -0.02052824459532726,
   "D2_avg": -0.018347663163946017,
   "D2_plus": -0.01834766316394601,
   "D2_minus": -0.01834766316394601,
   "a2agg_residual_rel": 9.076548452285695e-15,
   "I0_TT": 362.2844803374222,
   "I0_TL": 241.57169884554065,
   "I2_TT": 123.43047361632915,
   "I2_TL": 83.80274060401825,
   "V_T": 8.547779438739228,
   "V_L": 15.232487212095924
  },
  "hex_gem8": {
   "D0_plus": -0.02891780760307181,
   "D0_minus": -0.02891780760307181,
   "D0_avg": -0.028917807603071825,
   "D2_avg": -0.025933693584294384,
   "D2_plus": -0.025933693584294374,
   "D2_minus": -0.025933693584294374,
   "a2agg_residual_rel": 7.357979369086492e-15,
   "I0_TT": 1073.0614422363028,
   "I0_TL": 715.3892819892385,
   "I2_TT": 364.295965349171,
   "I2_TL": 247.56667439133207,
   "V_T": 10.248997674569596,
   "V_L": 19.228938954953616
  },
  "cubic_step": {
   "D0_plus": -0.03151342243433812,
   "D0_minus": -0.03151342243433812,
   "D0_avg": -0.03151342243433812,
   "D2_avg": -0.028537471107946306,
   "D2_plus": -0.028537471107946306,
   "D2_minus": -0.028537471107946306,
   "a2agg_residual_rel": 3.2825286917824895e-15,
   "I0_TT": 452.9030498380803,
   "I0_TL": 301.93536655872015,
   "I2_TT": 157.12962953566074,
   "I2_TL": 108.86105052797411,
   "V_T": 8.115794477437195,
   "V_L": 14.54833186313813
  },
  "cubic_gem8": {
   "D0_plus": -0.04367714392697779,
   "D0_minus": -0.04367714392697779,
   "D0_avg": -0.043677143926977795,
   "D2_avg": -0.039713976791286285,
   "D2_plus": -0.03971397679128628,
   "D2_minus": -0.03971397679128628,
   "a2agg_residual_rel": 4.542764439072047e-15,
   "I0_TT": 1393.5312074999997,
   "I0_TL": 929.0208049999997,
   "I2_TT": 483.47001076530677,
   "I2_TL": 334.95307935374194,
   "V_T": 9.87249208660102,
   "V_L": 18.445332743000304
  }
 },
 "phase1": {
  "hex_step|a": {
   "v_EM": 8.498926630589143,
   "v_S2E2": 8.261235391127114,
   "v_S2h": 8.489468358289109,
   "r_xtal_E2": -0.02796720689487253,
   "r_xtal_h": -0.001112878450555299,
   "lambda_mean": 0.004808575724022838,
   "lambda_max": 0.03353758299774612,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.036444417932560425,
   "share_EM": {
    "qSH": 0.49999999946246804,
    "qSV": 0.4951914248135092,
    "qL": 0.004808575724022834
   },
   "share_S2E2": {
    "qSH": 0.83333320610945,
    "qSV": 0.16464005343946514,
    "qL": 0.0020267404510848717
   },
   "doubling_r_xtal_E2": 7.771561172376096e-16
  },
  "hex_step|b": {
   "v_EM": 8.49913805976472,
   "v_S2E2": 8.261611551328288,
   "v_S2h": 8.489680210591468,
   "r_xtal_E2": -0.027947129081346778,
   "r_xtal_h": -0.0011128009813166084,
   "lambda_mean": 0.004808600428348514,
   "lambda_max": 0.033534547685208825,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.03644303566084012,
   "share_EM": {
    "qSH": 0.5,
    "qSV": 0.49519139957165154,
    "qL": 0.004808600428348502
   },
   "share_S2E2": {
    "qSH": 0.8333333333333336,
    "qSV": 0.16464001815350915,
    "qL": 0.002026648513157485
   },
   "doubling_r_xtal_E2": 6.661338147750939e-16
  },
  "hex_gem8|a": {
   "v_EM": 10.167571147427779,
   "v_S2E2": 9.767584615679638,
   "v_S2h": 10.154202161568202,
   "r_xtal_E2": -0.039339437703303504,
   "r_xtal_h": -0.0013148652382883874,
   "lambda_mean": 0.0049537696180639535,
   "lambda_max": 0.03513301845903744,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.05132899179683144,
   "share_EM": {
    "qSH": 0.49999999908685466,
    "qSV": 0.49504623129508146,
    "qL": 0.004953769618063935
   },
   "share_S2E2": {
    "qSH": 0.8333322334753969,
    "qSV": 0.16452961765676766,
    "qL": 0.002138148867835594
   },
   "doubling_r_xtal_E2": 6.661338147750939e-16
  },
  "hex_gem8|b": {
   "v_EM": 10.167412388965342,
   "v_S2E2": 9.767300819096656,
   "v_S2h": 10.154042977980577,
   "r_xtal_E2": -0.03935234989611769,
   "r_xtal_h": -0.0013149275816995987,
   "lambda_mean": 0.004953789932329422,
   "lambda_max": 0.035133018459037525,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.05133043709649301,
   "share_EM": {
    "qSH": 0.5,
    "qSV": 0.4950462100676707,
    "qL": 0.004953789932329417
   },
   "share_S2E2": {
    "qSH": 0.8333333333333337,
    "qSV": 0.16452845141380396,
    "qL": 0.002138215252862705
   },
   "doubling_r_xtal_E2": 4.440892098500626e-16
  },
  "cubic_step|001": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 7.889264216956222,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": -0.0172967677412158,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173741,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779367,
   "share_EM": {
    "qT1": 0.4992967361164542,
    "qT2": 0.49231094485466753,
    "qL": 0.008392319028878298
   },
   "share_S2E2": {
    "qT1": 0.4488023208911163,
    "qT2": 0.5426280022478344,
    "qL": 0.008569676861049398
   },
   "doubling_r_xtal_E2": 1.1102230246251565e-15
  },
  "cubic_step|111": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 8.120698567854001,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": 0.01153117849414409,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173741,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779367,
   "share_EM": {
    "qT1": 0.4992967361164542,
    "qT2": 0.49231094485466753,
    "qL": 0.008392319028878298
   },
   "share_S2E2": {
    "qT1": 0.5330407329981224,
    "qT2": 0.45868518652777995,
    "qL": 0.00827408047409754
   },
   "doubling_r_xtal_E2": 2.220446049250313e-16
  },
  "cubic_gem8|001": {
   "v_EM": 9.72117101507821,
   "v_S2E2": 9.5185580718033,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": -0.020842442022740326,
   "r_xtal_h": -0.0018451010194284745,
   "lambda_mean": 0.0093105038596528,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386433,
   "share_EM": {
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184,
    "qL": 0.009310503859652788
   },
   "share_S2E2": {
    "qT1": 0.44874904568984914,
    "qT2": 0.5417581722353867,
    "qL": 0.009492782074764219
   },
   "doubling_r_xtal_E2": 1.7763568394002505e-15
  },
  "cubic_gem8|111": {
   "v_EM": 9.72117101507821,
   "v_S2E2": 9.856246310594818,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": 0.01389496134849355,
   "r_xtal_h": -0.0018451010194284745,
   "lambda_mean": 0.0093105038596528,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386433,
   "share_EM": {
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184,
    "qL": 0.009310503859652788
   },
   "share_S2E2": {
    "qT1": 0.5329595958441811,
    "qT2": 0.4578514191062405,
    "qL": 0.009188985049578388
   },
   "doubling_r_xtal_E2": 2.220446049250313e-16
  }
 },
 "phase2": {
  "hex_step|a": {
   "vT_VRH": 8.419059637591603,
   "vT_V": 8.547779438739228,
   "vT_R": 8.288341029983927,
   "vT_HS_lo": 8.390859731728247,
   "vT_HS_hi": 8.424582419403457,
   "r_agg_E2_VRH": [
    -0.00035977898386985174,
    -8.995485659324398e-05,
    -1.4393819487867887e-05,
    -3.5985447373043655e-06,
    -5.757759000690754e-07,
    0.0,
    -5.757876907486192e-07,
    -3.5987289647154697e-06,
    -1.4395293312707835e-05,
    -8.997788565123788e-05,
    -0.0003599632319449819,
    -0.001440311666697669
   ],
   "r_agg_h_VRH": [
    -4.97443568558964e-07,
    -1.249121053259472e-07,
    -2.0039163883822653e-08,
    -5.014240023193395e-09,
    -8.027059017479132e-10,
    0.0,
    -8.03276667404873e-10,
    -5.023157112482579e-09,
    -2.0110500931203035e-08,
    -1.260267620262212e-07,
    -5.063613528477617e-07,
    -2.043685221497782e-06
   ],
   "r_agg_E2_HS": [
    -0.0003571461079143745,
    -8.927425424842816e-05,
    -1.4282679909993767e-05,
    -3.5705689754861325e-06,
    -5.71281304040383e-07,
    0.0,
    -5.712682860092855e-07,
    -3.570365567528988e-06,
    -1.4281052650555459e-05,
    -8.924882879379759e-05,
    -0.0003569427177455564,
    -0.001427336256063394
   ],
   "r_agg_E2_V": [
    -0.00044489345330223085,
    -0.00011129506285811885,
    -1.7814259669179933e-05,
    -4.4541593531288726e-06,
    -7.127228306424982e-07,
    0.0,
    -7.12799589352997e-07,
    -4.455358709520851e-06,
    -1.782385456405855e-05,
    -0.00011144498796067381,
    -0.0004460929933972624,
    -0.0017869833104871002
   ],
   "r_agg_E2_R": [
    -0.0002692160058006543,
    -6.725248904060344e-05,
    -1.0755531967165943e-05,
    -2.6884807549087952e-06,
    -4.301184323152185e-07,
    -2.220446049250313e-16,
    -4.300672613588574e-07,
    -2.687681208590753e-06,
    -1.0749135596066495e-05,
    -6.715254554567895e-05,
    -0.00026841645213737664,
    -0.0010721651905468699
   ],
   "S_t_E2": 1.6266231256261696e-13,
   "S_t_h": 4.563941055176853e-15,
   "kappa2_E2": -0.0014394617694966992,
   "kappa2_h": -2.0075101981637655e-06,
   "kappa3_E2": -7.369324458207498e-07,
   "kappa2_E2_HS": -0.0014281847168633966,
   "kappa2_E2_4term": -0.0014394544404300721,
   "S_t_E2_4term": 1.6265790021720394e-13,
   "kappa4_E2_4term": -1.1996041223777304e-07,
   "fit_residual": 3.04965357812358e-11,
   "fit_residual_4term": 3.3973616694016385e-15,
   "halving_dev_kappa2": 4.296077191089223e-06,
   "kappa2_E2_window0p1": -0.0014394555854578238,
   "lambda_mean_t": [
    2.5111906360924555e-06,
    6.283852379843875e-07,
    1.0059951851654784e-07,
    2.5154764402907355e-08,
    4.025233601588008e-09,
    1.8167378864124917e-30,
    4.025864750027318e-09,
    2.5164626100033596e-08,
    1.0067841215238367e-07,
    6.296179578773908e-07,
    2.521052590656771e-06,
    1.0105781771545095e-05
   ],
   "hs_ref": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   }
  },
  "hex_step|b": {
   "vT_VRH": 8.419278648579612,
   "vT_V": 8.547982997955295,
   "vT_R": 8.288576029181627,
   "vT_HS_lo": 8.391084746837947,
   "vT_HS_hi": 8.424803257723832,
   "r_agg_E2_VRH": [
    -0.000359589205973343,
    -8.990741528092094e-05,
    -1.4386229051588373e-05,
    -3.5966471373383158e-06,
    -5.754722848250182e-07,
    0.0,
    -5.754840760596736e-07,
    -3.596831374630405e-06,
    -1.4387702956364379e-05,
    -8.993044558192054e-05,
    -0.00035977346397653154,
    -0.0014395524516434
   ],
   "r_agg_h_VRH": [
    -4.969233557972075e-07,
    -1.2478124211678931e-07,
    -2.0018147695033406e-08,
    -5.0089790093466036e-09,
    -8.018634645168277e-10,
    0.0,
    -8.024334530176702e-10,
    -5.017882886981795e-09,
    -2.0089378716114936e-08,
    -1.2589424946973793e-07,
    -5.058279419767331e-07,
    -2.041524180040888e-06
   ],
   "r_agg_E2_HS": [
    -0.0003569546896101672,
    -8.922641129294195e-05,
    -1.4275026188892426e-05,
    -3.5686556428826677e-06,
    -5.70975180358424e-07,
    0.0,
    -5.709621745397797e-07,
    -3.5684524321011324e-06,
    -1.4273400507525125e-05,
    -8.92010104921459e-05,
    -0.00035675149663971784,
    -0.0014265718105259673
   ],
   "r_agg_E2_V": [
    -0.0004447026316007907,
    -0.00011124729747324924,
    -1.7806611237514147e-05,
    -4.452246738839705e-06,
    -7.124167632488465e-07,
    0.0,
    -7.124934562341423e-07,
    -4.4534450686084526e-06,
    -1.7816197920628163e-05,
    -0.0001113970942586695,
    -0.00044590114491716015,
    -0.0017862135883479624
   ],
   "r_agg_E2_R": [
    -0.0002690281488036961,
    -6.720559786976832e-05,
    -1.0748036230245894e-05,
    -2.686607384894124e-06,
    -4.298187469276016e-07,
    -2.220446049250313e-16,
    -4.297676474696033e-07,
    -2.6858089564596455e-06,
    -1.0741648802214954e-05,
    -6.710579410051931e-05,
    -0.000268229712959811,
    -0.0010714202639685588
   ],
   "S_t_E2": 1.6125034658616313e-13,
   "S_t_h": 6.550087858874976e-15,
   "kappa2_E2": -0.001438702718749083,
   "kappa2_h": -2.0054031941127916e-06,
   "kappa3_E2": -7.369721996574744e-07,
   "kappa2_E2_HS": -0.0014274194267221226,
   "kappa2_E2_4term": -0.0014386954029739513,
   "S_t_E2_4term": 1.6124593656681758e-13,
   "kappa4_E2_4term": -1.1974286021456171e-07,
   "fit_residual": 3.04412293281627e-11,
   "fit_residual_4term": 3.330880835213012e-15,
   "halving_dev_kappa2": 4.290548556187453e-06,
   "kappa2_E2_window0p1": -0.0014386965459252104,
   "lambda_mean_t": [
    2.5086422130892723e-06,
    6.277474540246005e-07,
    1.0049740414358128e-07,
    2.512922990624887e-08,
    4.021147509275336e-09,
    2.8493087979525507e-30,
    4.0217778869806965e-09,
    2.5139079553542238e-08,
    1.005762013941085e-07,
    6.289786678735804e-07,
    2.5184921186771055e-06,
    1.0095510979328715e-05
   ],
   "hs_ref": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   }
  },
  "hex_gem8|a": {
   "vT_VRH": 10.041721817369147,
   "vT_V": 10.248997674569596,
   "vT_R": 9.830076336505329,
   "vT_HS_lo": 9.990913001571156,
   "vT_HS_hi": 10.052797754949037,
   "r_agg_E2_VRH": [
    -0.00047377007967119855,
    -0.0001184586706243218,
    -1.8955103105455784e-05,
    -4.7389256596641616e-06,
    -7.582427594687857e-07,
    -2.220446049250313e-16,
    -7.582626075919308e-07,
    -4.7392357853670575e-06,
    -1.8957584126733096e-05,
    -0.00011849743822145431,
    -0.00047408026726247776,
    -0.0018971495594123367
   ],
   "r_agg_h_VRH": [
    -8.038770585860888e-07,
    -2.0201977346534505e-07,
    -3.242488200161375e-08,
    -8.11473377382299e-09,
    -1.299176211055908e-09,
    0.0,
    -1.3002692256236514e-09,
    -8.131815554257571e-09,
    -3.256153702224651e-08,
    -2.041550737352793e-07,
    -8.209613446830133e-07,
    -3.3191570847357355e-06
   ],
   "r_agg_E2_HS": [
    -0.00047147218794019174,
    -0.00011785019986731982,
    -1.885426634828935e-05,
    -4.71341728180974e-06,
    -7.541323487902929e-07,
    -2.220446049250313e-16,
    -7.54113030021486e-07,
    -4.713115426713266e-06,
    -1.8851851520729213e-05,
    -0.00011781246964737146,
    -0.0004711703880158069,
    -0.0018840138120467254
   ],
   "r_agg_E2_V": [
    -0.0005816603154129574,
    -0.00014553490980062644,
    -2.3297462136029345e-05,
    -5.8253708745681365e-06,
    -9.321564546915795e-07,
    0.0,
    -9.322866439953614e-07,
    -5.8274050896978125e-06,
    -2.331373598807307e-05,
    -0.00014578920292729336,
    -0.0005836950659862117,
    -0.002339328010586894
   ],
   "r_agg_E2_R": [
    -0.00035643481654545894,
    -8.901723504473047e-05,
    -1.4234158591031054e-05,
    -3.557830641987003e-06,
    -5.691851292510819e-07,
    2.220446049250313e-16,
    -5.690951039305503e-07,
    -3.5564239939667175e-06,
    -1.4222905402316854e-05,
    -8.88414034126983e-05,
    -0.0003550281474846706,
    -0.00141752637341086
   ],
   "S_t_E2": 4.894642365145396e-13,
   "S_t_h": 1.9849252759426836e-14,
   "kappa2_E2": -0.0018956484826701352,
   "kappa2_h": -3.2493966959289463e-06,
   "kappa3_E2": -1.24057090180438e-06,
   "kappa2_E2_HS": -0.0018853014774839155,
   "kappa2_E2_4term": -0.001895631597971673,
   "S_t_E2_4term": 4.894584258277063e-13,
   "kappa4_E2_4term": -2.763647120625483e-07,
   "fit_residual": 7.025789764898445e-11,
   "fit_residual_4term": 1.0214700603304965e-14,
   "halving_dev_kappa2": 7.51551994532953e-06,
   "kappa2_E2_window0p1": -0.0018956342358861544,
   "lambda_mean_t": [
    3.6006634946247986e-06,
    9.011863601809301e-07,
    1.4429157576509233e-07,
    3.608153193406747e-08,
    5.773880433588238e-09,
    2.8730624380705302e-30,
    5.775001291440091e-09,
    3.6099045346764643e-08,
    1.444316833663885e-07,
    9.033755744645923e-07,
    3.618178152703809e-06,
    1.4512512141033628e-05
   ],
   "hs_ref": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   }
  },
  "hex_gem8|b": {
   "vT_VRH": 10.041554085160632,
   "vT_V": 10.248847414872234,
   "vT_R": 9.82989031256601,
   "vT_HS_lo": 9.99073982971986,
   "vT_HS_hi": 10.052629959294945,
   "r_agg_E2_VRH": [
    -0.0004738923403120321,
    -0.00011848923252755217,
    -1.895999284384775e-05,
    -4.740148086490592e-06,
    -7.584383474590339e-07,
    0.0,
    -7.584581946940006e-07,
    -4.740458205976239e-06,
    -1.8962473815165026e-05,
    -0.00011852799934297664,
    -0.0004742025216768475,
    -0.0018976387487924518
   ],
   "r_agg_h_VRH": [
    -8.04256157782568e-07,
    -2.021152383235858e-07,
    -3.2440223618479536e-08,
    -8.118574701398984e-09,
    -1.2997911635892478e-09,
    0.0,
    -1.3008849553131085e-09,
    -8.13566802815302e-09,
    -3.2576969677400314e-08,
    -2.0425195845774624e-07,
    -8.213518059019265e-07,
    -3.320743002910298e-06
   ],
   "r_agg_E2_HS": [
    -0.0004715958998675607,
    -0.0001178811207174224,
    -1.885921295863291e-05,
    -4.714653872306407e-06,
    -7.543301969725746e-07,
    -3.3306690738754696e-16,
    -7.543108705432289e-07,
    -4.714351890200419e-06,
    -1.8856797115107682e-05,
    -0.00011784337463216499,
    -0.00047129397306711063,
    -0.0018845078483341604
   ],
   "r_agg_E2_V": [
    -0.0005817817193016772,
    -0.00014556530971254755,
    -2.3302331052743597e-05,
    -5.826588524215914e-06,
    -9.323513193715272e-07,
    -2.220446049250313e-16,
    -9.324815636313488e-07,
    -5.828623595549587e-06,
    -2.3318611752976004e-05,
    -0.00014581970985627635,
    -0.0005838173263492674,
    -0.0023398190658678875
   ],
   "r_agg_E2_R": [
    -0.0003565570229338011,
    -8.904772300111219e-05,
    -1.423903074149191e-05,
    -3.5590481938241325e-06,
    -5.693798912353998e-07,
    -2.220446049250313e-16,
    -5.692898042974903e-07,
    -3.557640585682975e-06,
    -1.422776987347607e-05,
    -8.887177138017233e-05,
    -0.0003551493939385475,
    -0.0014180096723556135
   ],
   "S_t_E2": 4.895751529361098e-13,
   "S_t_h": 1.861754403597132e-14,
   "kappa2_E2": -0.0018961374665242264,
   "kappa2_h": -3.2509354903061167e-06,
   "kappa3_E2": -1.240545889104786e-06,
   "kappa2_E2_HS": -0.0018857960842583088,
   "kappa2_E2_4term": -0.001896120566862326,
   "S_t_E2_4term": 4.895693407496872e-13,
   "kappa4_E2_4term": -2.766096300511605e-07,
   "fit_residual": 7.032016110210891e-11,
   "fit_residual_4term": 1.0163106401516192e-14,
   "halving_dev_kappa2": 7.520240357827345e-06,
   "kappa2_E2_window0p1": -0.0018961232071147266,
   "lambda_mean_t": [
    3.6022883240770764e-06,
    9.015930248247842e-07,
    1.4435669065055046e-07,
    3.609781489575608e-08,
    5.7764861216668656e-09,
    1.2842490776280975e-31,
    5.777607540357807e-09,
    3.611533707604357e-08,
    1.4449686840147292e-07,
    9.037833352239438e-07,
    3.6198117522104935e-06,
    1.4519069924274029e-05
   ],
   "hs_ref": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   }
  },
  "cubic_step|001": {
   "vT_VRH": 7.799046375844923,
   "vT_V": 8.115794477437195,
   "vT_R": 7.468877341686607,
   "vT_HS_lo": 7.758614490211087,
   "vT_HS_hi": 7.867953005904775,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    -1.1102230246251565e-16,
    2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "r_agg_E2_HS": [
    2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    -2.220446049250313e-16,
    0.0
   ],
   "r_agg_E2_V": [
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    2.220446049250313e-16,
    0.0
   ],
   "r_agg_E2_R": [
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0
   ],
   "S_t_E2": 3.872699649800502e-16,
   "S_t_h": 2.7381760509747877e-16,
   "kappa2_E2": 3.141702123932416e-15,
   "kappa2_h": -3.458500796931401e-17,
   "kappa3_E2": -6.308626889222545e-15,
   "kappa2_E2_HS": -4.606723061512521e-16,
   "kappa2_E2_4term": -1.4860741481801268e-14,
   "S_t_E2_4term": 3.872699649800578e-16,
   "kappa4_E2_4term": 2.946596976449254e-13,
   "fit_residual": 8.549374687587548e-17,
   "fit_residual_4term": 4.1204862127242437e-17,
   "halving_dev_kappa2": 4.802491637841732,
   "kappa2_E2_window0p1": -1.194629605484262e-14,
   "lambda_mean_t": [
    2.8112615174278626e-30,
    1.9079063183926423e-31,
    2.534920485447341e-30,
    1.979885257559672e-30,
    2.173629477557336e-30,
    4.258392291069694e-32,
    7.083137335193975e-31,
    2.8979386817414475e-31,
    2.106564088504244e-31,
    4.975216689832133e-31,
    2.6091436397777845e-30,
    3.806067177046203e-30
   ],
   "hs_ref": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   }
  },
  "cubic_step|111": {
   "vT_VRH": 7.799046375844923,
   "vT_V": 8.115794477437195,
   "vT_R": 7.468877341686607,
   "vT_HS_lo": 7.758614490211087,
   "vT_HS_hi": 7.867953005904775,
   "r_agg_E2_VRH": [
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16,
    -2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    2.220446049250313e-16,
    2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16
   ],
   "r_agg_E2_HS": [
    -1.1102230246251565e-16,
    2.220446049250313e-16,
    2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0
   ],
   "r_agg_E2_V": [
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    2.220446049250313e-16
   ],
   "r_agg_E2_R": [
    0.0,
    -1.1102230246251565e-16,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    2.220446049250313e-16
   ],
   "S_t_E2": 4.1100077415202465e-16,
   "S_t_h": -2.925271284971396e-16,
   "kappa2_E2": -1.6739143857147652e-16,
   "kappa2_h": 1.7403176010158433e-15,
   "kappa3_E2": -6.477861259177068e-15,
   "kappa2_E2_HS": 3.6895286501663385e-15,
   "kappa2_E2_4term": -7.551062690715626e-15,
   "S_t_E2_4term": 4.1100077415202347e-16,
   "kappa4_E2_4term": 1.208541677071763e-13,
   "fit_residual": 9.58829698458047e-17,
   "fit_residual_4term": 9.082728246688532e-17,
   "halving_dev_kappa2": 36.70942580584538,
   "kappa2_E2_window0p1": -6.312235033344818e-15,
   "lambda_mean_t": [
    4.465944891615489e-31,
    5.476038365628235e-32,
    6.051257726818309e-32,
    1.948365321836496e-30,
    2.828315617598195e-30,
    4.258392291069694e-32,
    2.0671675410653463e-31,
    1.4414436418839758e-31,
    6.97654761692104e-31,
    8.05882784895705e-32,
    8.826351831704817e-31,
    5.277432358348646e-32
   ],
   "hs_ref": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   }
  },
  "cubic_gem8|001": {
   "vT_VRH": 9.307899076533179,
   "vT_V": 9.87249208660102,
   "vT_R": 8.706771527831352,
   "vT_HS_lo": 9.211721064370861,
   "vT_HS_hi": 9.456854984588738,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    2.220446049250313e-16,
    2.220446049250313e-16
   ],
   "r_agg_E2_HS": [
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16
   ],
   "r_agg_E2_V": [
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16
   ],
   "r_agg_E2_R": [
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -4.440892098500626e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    -4.440892098500626e-16
   ],
   "S_t_E2": 2.2690471976516216e-16,
   "S_t_h": 1.0207029061365447e-15,
   "kappa2_E2": -1.4940723442743361e-16,
   "kappa2_h": 1.4525703347111552e-15,
   "kappa3_E2": -3.710299357793312e-15,
   "kappa2_E2_HS": -2.9328086757977686e-16,
   "kappa2_E2_4term": -7.548769884661831e-15,
   "S_t_E2_4term": 2.2690471976516093e-16,
   "kappa4_E2_4term": 1.2111100076374125e-13,
   "fit_residual": 1.2768503165890454e-16,
   "fit_residual_4term": 1.239173204933564e-16,
   "halving_dev_kappa2": 36.70942580584519,
   "kappa2_E2_window0p1": -5.634061021497827e-15,
   "lambda_mean_t": [
    1.3321601247899372e-30,
    3.2963158788329955e-31,
    5.115608018065614e-31,
    2.5296306525163064e-31,
    6.091189661068836e-32,
    1.490703376101465e-30,
    4.970531018467675e-31,
    1.6321728720822753e-31,
    2.0328800328242484e-30,
    9.252456281403098e-32,
    1.2157397395047422e-30,
    4.788242399022421e-30
   ],
   "hs_ref": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   }
  },
  "cubic_gem8|111": {
   "vT_VRH": 9.307899076533179,
   "vT_V": 9.87249208660102,
   "vT_R": 8.706771527831352,
   "vT_HS_lo": 9.211721064370861,
   "vT_HS_hi": 9.456854984588738,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    4.440892098500626e-16
   ],
   "r_agg_E2_HS": [
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16
   ],
   "r_agg_E2_V": [
    0.0,
    2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    -3.3306690738754696e-16
   ],
   "r_agg_E2_R": [
    0.0,
    2.220446049250313e-16,
    0.0,
    -4.440892098500626e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    0.0,
    -4.440892098500626e-16,
    0.0
   ],
   "S_t_E2": -1.1819852171697386e-15,
   "S_t_h": 0.0,
   "kappa2_E2": 1.272728293270753e-16,
   "kappa2_h": 0.0,
   "kappa3_E2": 1.888996552887521e-14,
   "kappa2_E2_HS": -4.1502009563175863e-16,
   "kappa2_E2_4term": 4.644932862254055e-15,
   "S_t_E2_4term": -1.181985217169738e-15,
   "kappa4_E2_4term": -7.39439805238916e-14,
   "fit_residual": 1.3736358346507315e-16,
   "fit_residual_4term": 1.3607124301964625e-16,
   "halving_dev_kappa2": 36.70942580584462,
   "kappa2_E2_window0p1": 4.799385314609271e-15,
   "lambda_mean_t": [
    6.654563919555887e-32,
    1.284474620620143e-31,
    8.203146796165973e-32,
    2.191414433855259e-31,
    3.5992660205608407e-31,
    1.490703376101465e-30,
    3.737141516433966e-32,
    2.779423581315274e-32,
    4.91382581689863e-32,
    1.018907926091293e-30,
    1.3956842828973518e-31,
    4.844546844365318e-31
   ],
   "hs_ref": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   }
  }
 },
 "falsifiers": {
  "F-MS-3": {
   "state": "SILENT",
   "worst_S_t": 4.895751529361098e-13
  },
  "F-MS-2": {
   "state": "REGISTERED_NOT_EXECUTED"
  },
  "F-MS-1": {
   "state": "RETIRED_TO_CONTROL"
  }
 },
 "verdict_class": "IDENTITY-DELIVERED",
 "T1_post_write": {
  "list_md5": "fef2827100d3f85e0a6341b44f0c00bf",
  "state": "CLEAN",
  "numeric_collisions": 4,
  "files": [
   "g_mscs1_chatleg_checkpoint.json"
  ]
 }
}
=====END-EMBED name=inputs/gmscs1_gate/g_mscs1_chatleg_checkpoint.json=====

=====BEGIN-EMBED name=inputs/gmscs1_gate/g_mscs1_ccleg_checkpoint.json md5=249e11dd53c4cb82f302b15d3c94c337 bytes=24415 encoding=raw=====
{
 "gate": "G-MSCS1",
 "leg": "cc",
 "instrument": "g_mscs1_ccleg.py",
 "instrument_md5": "195a2b1baf1589675d4bf18983673a23",
 "memo_md5": "3f30262eaec461fb5fd3202835f7de37",
 "memo_bytes": 34837,
 "ledger_base_md5": "d095a7003bb0d4c177e7451e1d14c4c6",
 "utc": "2026-09-20 02:00:35 UTC",
 "elections": {
  "E-MS-1": "(a) two descriptors of the one transverse field; S2-E2 primary, S2-h second arm",
  "E-MS-2": "(a) all four configurations",
  "E-MS-2b": "(a+b) banked tetragonal-form primary + hexagonal-symmetrized C66 second arm",
  "E-MS-2c": "(001+111) cubic axis 001 primary, 111 reported",
  "E-MS-3": "(a) VRH/HS leading order; polarization-resolved Born at t = 0 only",
  "E-MS-4": "(a) verbatim differentiation table + lambda_L computation",
  "E-MS-5": "(a) fiber ODF 1 + t P2(cos theta), t in [-1, 2]",
  "E-MS-6": "(a) no observational contact in this gate"
 },
 "T1": {
  "list_md5": "fef2827100d3f85e0a6341b44f0c00bf",
  "state": "CLEAN",
  "numeric_collisions": 5,
  "x_collisions_instrument_plus_memo": 0
 },
 "inputs": {
  "X1_md5": "200e7a8b775577564369c6924d38a84c",
  "X1_bytes": 2767,
  "X3_md5": "aaae206733b0f0a378a5c6b600274d3f",
  "X4_md5": "ec87e42f0f617b00c4985ba2aceac339",
  "X5_md5": "df413a7cfa30e599b779af8fee5d07d1"
 },
 "quadrature": {
  "n_theta": 64,
  "n_phi": 128,
  "doubling_residual": 1.1102230246251565e-15
 },
 "t_grid": [
  -0.5,
  -0.25,
  -0.1,
  -0.05,
  -0.02,
  0.0,
  0.02,
  0.05,
  0.1,
  0.25,
  0.5,
  1.0
 ],
 "controls": {
  "F-CTRL-ISO": {
   "passed": true,
   "r_xtal_E2": 2.220446049250313e-16,
   "r_xtal_h": 0.0,
   "lambda_max": 5.8657280953489826e-31,
   "r_agg_max": 2.220446049250313e-16
  },
  "F-CTRL-SO3": {
   "passed": true,
   "w_S2_mean_t0": 0.39999999999999997,
   "dev_from_0p4": 1.0547118733938987e-15,
   "r_agg_0_E2": 4.440892098500626e-16
  },
  "F-CTRL-TEX": {
   "passed": true,
   "r_agg_t1": 0.002501914521741977
  },
  "F-CTRL-POL": {
   "passed": true,
   "split_plus_minus": 0.0,
   "split_plus_avg": 2.0816681711721685e-17
  },
  "PIN-A2AGG": {
   "passed": true,
   "worst_rel_residual": 4.376704922376667e-15
  },
  "F-CTRL-ADMIX": {
   "passed": true,
   "r_xtal_h_projected": -0.001967367205683912,
   "x_r_by_key": {
    "hex_step|a": -0.0009717819955337159,
    "hex_step|b": -0.0009717429602675853,
    "hex_gem8|a": -0.0011309526900499245,
    "hex_gem8|b": -0.0011309883383803232,
    "cubic_step|001": -0.0016115554323222758,
    "cubic_step|111": -0.0016115554323222758,
    "cubic_gem8|001": -0.001967367205683912,
    "cubic_gem8|111": -0.001967367205683912
   },
   "x_r_complete_projection_worst": 0.0,
   "x_identity_check_2p6": {
    "hex_step|a": {
     "r_xtal_h": -0.001112878450555299,
     "identity_pred": -0.0014293733595875718,
     "rel_resid": 0.2843930609621828
    },
    "hex_step|b": {
     "r_xtal_h": -0.0011128009813170525,
     "identity_pred": -0.0014292835894878586,
     "rel_resid": 0.2844018054299647
    },
    "hex_gem8|a": {
     "r_xtal_h": -0.0013148652382883874,
     "identity_pred": -0.0016827680558306841,
     "rel_resid": 0.27980268002309533
    },
    "hex_gem8|b": {
     "r_xtal_h": -0.0013149275816995987,
     "identity_pred": -0.0016828417147120545,
     "rel_resid": 0.27979801939884136
    },
    "cubic_step|001": {
     "r_xtal_h": -0.001516377102324551,
     "identity_pred": -0.0020353270533740894,
     "rel_resid": 0.3422301419970053
    },
    "cubic_step|111": {
     "r_xtal_h": -0.001516377102324551,
     "identity_pred": -0.0020353270533740894,
     "rel_resid": 0.3422301419970053
    },
    "cubic_gem8|001": {
     "r_xtal_h": -0.0018451010194286965,
     "identity_pred": -0.0024760981546310635,
     "rel_resid": 0.3419851425792092
    },
    "cubic_gem8|111": {
     "r_xtal_h": -0.0018451010194286965,
     "identity_pred": -0.0024760981546310635,
     "rel_resid": 0.3419851425792092
    }
   },
   "x_note": "substantive implementation per dispatch step 3.3: r_xtal_h_projected is the literal memo-section-4 number (quasi-transverse eigenvectors projected, quasi-longitudinal branch untouched) and is NOT zero within tau_agg; the pass flag follows the complete zero-admixture reading, under which the split vanishes exactly; see H-CC items in the CC report"
  }
 },
 "phase1": {
  "hex_step|a": {
   "v_EM": 8.498926630589143,
   "v_S2E2": 8.261235391127112,
   "v_S2h": 8.489468358289109,
   "r_xtal_E2": -0.027967206894872754,
   "r_xtal_h": -0.001112878450555299,
   "lambda_mean": 0.004808575724022839,
   "lambda_max": 0.03353758299774612,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.03644441793256045,
   "share_EM": {
    "qL": 0.004808575724022839,
    "qSV": 0.4951914248135092,
    "qSH": 0.499999999462468
   },
   "share_S2E2": {
    "qL": 0.0020267404510848678,
    "qSV": 0.1646400534394651,
    "qSH": 0.8333332061094499
   }
  },
  "hex_step|b": {
   "v_EM": 8.499138059764721,
   "v_S2E2": 8.26161155132829,
   "v_S2h": 8.489680210591466,
   "r_xtal_E2": -0.027947129081346778,
   "r_xtal_h": -0.0011128009813170525,
   "lambda_mean": 0.0048086004283485135,
   "lambda_max": 0.033534547685208825,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.03644303566084019,
   "share_EM": {
    "qL": 0.0048086004283485135,
    "qSV": 0.49519139957165154,
    "qSH": 0.5
   },
   "share_S2E2": {
    "qL": 0.002026648513157482,
    "qSV": 0.16464001815350915,
    "qSH": 0.8333333333333335
   }
  },
  "hex_gem8|a": {
   "v_EM": 10.167571147427779,
   "v_S2E2": 9.767584615679638,
   "v_S2h": 10.154202161568202,
   "r_xtal_E2": -0.039339437703303504,
   "r_xtal_h": -0.0013148652382883874,
   "lambda_mean": 0.0049537696180639535,
   "lambda_max": 0.03513301845903746,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.051328991796831605,
   "share_EM": {
    "qL": 0.004953769618063954,
    "qSV": 0.49504623129508146,
    "qSH": 0.49999999908685466
   },
   "share_S2E2": {
    "qL": 0.0021381488678355936,
    "qSV": 0.16452961765676763,
    "qSH": 0.8333322334753966
   }
  },
  "hex_gem8|b": {
   "v_EM": 10.167412388965342,
   "v_S2E2": 9.767300819096654,
   "v_S2h": 10.154042977980577,
   "r_xtal_E2": -0.03935234989611791,
   "r_xtal_h": -0.0013149275816995987,
   "lambda_mean": 0.004953789932329422,
   "lambda_max": 0.035133018459037504,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.05133043709649307,
   "share_EM": {
    "qL": 0.004953789932329422,
    "qSV": 0.4950462100676707,
    "qSH": 0.5
   },
   "share_S2E2": {
    "qL": 0.0021382152528626997,
    "qSV": 0.1645284514138039,
    "qSH": 0.8333333333333336
   }
  },
  "cubic_step|001": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 7.889264216956221,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": -0.017296767741215913,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173745,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779363,
   "share_EM": {
    "qL": 0.0083923190288783,
    "qT1": 0.4992967361164543,
    "qT2": 0.49231094485466753
   },
   "share_S2E2": {
    "qL": 0.008569676861049402,
    "qT1": 0.44880232089111627,
    "qT2": 0.5426280022478344
   }
  },
  "cubic_step|111": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 8.120698567854001,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": 0.01153117849414409,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173745,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779363,
   "share_EM": {
    "qL": 0.0083923190288783,
    "qT1": 0.4992967361164543,
    "qT2": 0.49231094485466753
   },
   "share_S2E2": {
    "qL": 0.008274080474097544,
    "qT1": 0.5330407329981224,
    "qT2": 0.45868518652777995
   }
  },
  "cubic_gem8|001": {
   "v_EM": 9.721171015078212,
   "v_S2E2": 9.518558071803296,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": -0.02084244202274077,
   "r_xtal_h": -0.0018451010194286965,
   "lambda_mean": 0.009310503859652798,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386443,
   "share_EM": {
    "qL": 0.009310503859652798,
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184
   },
   "share_S2E2": {
    "qL": 0.009492782074764233,
    "qT1": 0.44874904568984897,
    "qT2": 0.5417581722353866
   }
  },
  "cubic_gem8|111": {
   "v_EM": 9.721171015078212,
   "v_S2E2": 9.856246310594821,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": 0.013894961348493773,
   "r_xtal_h": -0.0018451010194286965,
   "lambda_mean": 0.009310503859652798,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386443,
   "share_EM": {
    "qL": 0.009310503859652798,
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184
   },
   "share_S2E2": {
    "qL": 0.009188985049578397,
    "qT1": 0.5329595958441811,
    "qT2": 0.4578514191062405
   }
  }
 },
 "phase2": {
  "hex_step|a": {
   "vT_VRH": 8.419059637591616,
   "vT_HS_lo": 8.390859731729313,
   "vT_HS_hi": 8.424582419402883,
   "r_agg_E2_VRH": [
    -0.0003597789838700738,
    -8.995485659368807e-05,
    -1.4393819487867887e-05,
    -3.5985447373043655e-06,
    -5.7577590029112e-07,
    -2.220446049250313e-16,
    -5.757876907486192e-07,
    -3.5987289647154697e-06,
    -1.4395293313040902e-05,
    -8.997788565123788e-05,
    -0.00035996323194520397,
    -0.001440311666698113
   ],
   "r_agg_h_VRH": [
    -4.97443568558964e-07,
    -1.249121053259472e-07,
    -2.0039163883822653e-08,
    -5.01423980114879e-09,
    -8.027061237925182e-10,
    0.0,
    -8.03276667404873e-10,
    -5.023156890437974e-09,
    -2.011050115324764e-08,
    -1.260267622482658e-07,
    -5.063613532918509e-07,
    -2.043685221497782e-06
   ],
   "r_agg_E2_HS": [
    -0.0003571461079148186,
    -8.927425424842816e-05,
    -1.4282679909993767e-05,
    -3.5705689754861325e-06,
    -5.71281304040383e-07,
    2.220446049250313e-16,
    -5.712682857872409e-07,
    -3.570365567528988e-06,
    -1.4281052650777504e-05,
    -8.924882879401963e-05,
    -0.0003569427177455564,
    -0.0014273362560642822
   ],
   "S_t_E2": 1.6132521040103724e-13,
   "S_t_h": 3.901387545207024e-15,
   "kappa2_E2": -0.0014394617695005832,
   "kappa2_h": -2.0075102000424232e-06,
   "kappa3_E2": -7.369324104590622e-07,
   "fit_residual": 6.129824287082772e-11,
   "halving_dev_kappa2": 4.296068727221966e-06,
   "lambda_mean_t": [
    2.5111906360905225e-06,
    6.283852379770122e-07,
    1.0059951851451649e-07,
    2.51547644056437e-08,
    4.025233596548142e-09,
    0.0,
    4.025864754976195e-09,
    2.516462609932631e-08,
    1.0067841215180097e-07,
    6.296179578773481e-07,
    2.521052590653425e-06,
    1.0105781771537547e-05
   ],
   "x_kappa_4term_fit_E2": [
    1.613207980641205e-13,
    -0.0014394544404483034,
    -7.369324103762292e-07,
    -1.199601774147876e-07
   ]
  },
  "hex_step|b": {
   "vT_VRH": 8.4192786485796,
   "vT_HS_lo": 8.391084746839036,
   "vT_HS_hi": 8.42480325772318,
   "r_agg_E2_VRH": [
    -0.000359589205973343,
    -8.990741528092094e-05,
    -1.4386229051810417e-05,
    -3.5966471373383158e-06,
    -5.754722848250182e-07,
    0.0,
    -5.75484075837629e-07,
    -3.59683137440836e-06,
    -1.4387702956142334e-05,
    -8.993044558214258e-05,
    -0.00035977346397664256,
    -0.001439552451643511
   ],
   "r_agg_h_VRH": [
    -4.969233557972075e-07,
    -1.247812418947447e-07,
    -2.001814791707801e-08,
    -5.0089792313912085e-09,
    -8.018635755391301e-10,
    0.0,
    -8.024333419953678e-10,
    -5.017882998004097e-09,
    -2.0089378716114936e-08,
    -1.2589424969178253e-07,
    -5.058279419767331e-07,
    -2.04152418015191e-06
   ],
   "r_agg_E2_HS": [
    -0.0003569546896107223,
    -8.922641129327502e-05,
    -1.4275026188892426e-05,
    -3.5686556428826677e-06,
    -5.709751801363794e-07,
    -2.220446049250313e-16,
    -5.709621745397797e-07,
    -3.5684524321011324e-06,
    -1.4273400507525125e-05,
    -8.920101049236795e-05,
    -0.0003567514966401619,
    -0.0014265718105257452
   ],
   "S_t_E2": 1.6400082932192235e-13,
   "S_t_h": 8.137135505898113e-15,
   "kappa2_E2": -0.0014387027187507326,
   "kappa2_h": -2.0054031944932263e-06,
   "kappa3_E2": -7.369722507858468e-07,
   "fit_residual": 6.118721569792576e-11,
   "halving_dev_kappa2": 4.290551805693156e-06,
   "lambda_mean_t": [
    2.508642213075073e-06,
    6.277474540209645e-07,
    1.0049740414635627e-07,
    2.512922990500282e-08,
    4.021147506729069e-09,
    0.0,
    4.0217778891485955e-09,
    2.51390795521338e-08,
    1.0057620139494587e-07,
    6.289786678683045e-07,
    2.5184921186663207e-06,
    1.009551097933715e-05
   ],
   "x_kappa_4term_fit_E2": [
    1.6399641930257683e-13,
    -0.0014386954029695716,
    -7.369722507030138e-07,
    -1.197429589050166e-07
   ]
  },
  "hex_gem8|a": {
   "vT_VRH": 10.041721817369156,
   "vT_HS_lo": 9.990913001573082,
   "vT_HS_hi": 10.05279775494808,
   "r_agg_E2_VRH": [
    -0.0004737700796713096,
    -0.00011845867062443283,
    -1.8955103105566806e-05,
    -4.738925659331095e-06,
    -7.582427593577634e-07,
    -2.220446049250313e-16,
    -7.582626074809085e-07,
    -4.739235785145013e-06,
    -1.895758412695514e-05,
    -0.00011849743822178738,
    -0.00047408026726236674,
    -0.0018971495594128918
   ],
   "r_agg_h_VRH": [
    -8.038770585860888e-07,
    -2.0201977357636736e-07,
    -3.242488200161375e-08,
    -8.11473377382299e-09,
    -1.299175989011303e-09,
    0.0,
    -1.3002695586905588e-09,
    -8.131815554257571e-09,
    -3.2561537133268814e-08,
    -2.041550740683462e-07,
    -8.209613451271025e-07,
    -3.3191570850688024e-06
   ],
   "r_agg_E2_HS": [
    -0.00047147218794074686,
    -0.00011785019986754186,
    -1.8854266348178328e-05,
    -4.713417281476673e-06,
    -7.541323485682483e-07,
    -2.220446049250313e-16,
    -7.541130296884191e-07,
    -4.713115426491221e-06,
    -1.8851851520507168e-05,
    -0.00011781246964759351,
    -0.00047117038801591793,
    -0.0018840138120480576
   ],
   "S_t_E2": 4.88778727245365e-13,
   "S_t_h": 1.8870073354479004e-14,
   "kappa2_E2": -0.0018956484826738256,
   "kappa2_h": -3.249396699531321e-06,
   "kappa3_E2": -1.2405708979146963e-06,
   "fit_residual": 1.4122180315889916e-10,
   "halving_dev_kappa2": 7.515517296534205e-06,
   "lambda_mean_t": [
    3.6006634946301176e-06,
    9.011863601856414e-07,
    1.4429157576291246e-07,
    3.608153193548488e-08,
    5.7738804321405966e-09,
    0.0,
    5.775001286170658e-09,
    3.609904534358997e-08,
    1.4443168336644392e-07,
    9.033755744628227e-07,
    3.6181781526989147e-06,
    1.4512512141049044e-05
   ],
   "x_kappa_4term_fit_E2": [
    4.887729165585316e-13,
    -0.0018956315979800395,
    -1.2405708978056256e-06,
    -2.7636463552777845e-07
   ]
  },
  "hex_gem8|b": {
   "vT_VRH": 10.041554085160612,
   "vT_HS_lo": 9.990739829721814,
   "vT_HS_hi": 10.05262995929398,
   "r_agg_E2_VRH": [
    -0.0004738923403124762,
    -0.00011848923252755217,
    -1.8959992844180817e-05,
    -4.740148086490592e-06,
    -7.58438347125967e-07,
    4.440892098500626e-16,
    -7.584581950270675e-07,
    -4.740458205643172e-06,
    -1.896247381538707e-05,
    -0.00011852799934330971,
    -0.00047420252167706956,
    -0.0018976387487922297
   ],
   "r_agg_h_VRH": [
    -8.04256157782568e-07,
    -2.021152383235858e-07,
    -3.244022384052414e-08,
    -8.118574701398984e-09,
    -1.2997910525669454e-09,
    2.220446049250313e-16,
    -1.3008851773577135e-09,
    -8.13566802815302e-09,
    -3.2576969677400314e-08,
    -2.0425195845774624e-07,
    -8.213518062349934e-07,
    -3.3207430030213203e-06
   ],
   "r_agg_E2_HS": [
    -0.00047159589986833783,
    -0.00011788112071775547,
    -1.8859212958410865e-05,
    -4.714653872306407e-06,
    -7.543301973056415e-07,
    0.0,
    -7.543108700991397e-07,
    -4.714351890200419e-06,
    -1.8856797115107682e-05,
    -0.00011784337463249805,
    -0.00047129397306722165,
    -0.0018845078483346045
   ],
   "S_t_E2": 4.90291953941434e-13,
   "S_t_h": 1.9232267730539364e-14,
   "kappa2_E2": -0.0018961374665274083,
   "kappa2_h": -3.250935490588331e-06,
   "kappa3_E2": -1.240545911150953e-06,
   "fit_residual": 1.4134676897214994e-10,
   "halving_dev_kappa2": 7.520230342822992e-06,
   "lambda_mean_t": [
    3.6022883240769405e-06,
    9.015930248276157e-07,
    1.4435669065512994e-07,
    3.609781489279239e-08,
    5.776486127644972e-09,
    0.0,
    5.7776075427095745e-09,
    3.6115337074777367e-08,
    1.4449686839815845e-07,
    9.03783335221914e-07,
    3.6198117522199667e-06,
    1.4519069924266563e-05
   ],
   "x_kappa_4term_fit_E2": [
    4.902861417464788e-13,
    -0.001896120566887107,
    -1.2405459110416654e-06,
    -2.7660927652668255e-07
   ]
  },
  "cubic_step|001": {
   "vT_VRH": 7.7990463758448945,
   "vT_HS_lo": 7.758614490217017,
   "vT_HS_hi": 7.867953005902295,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16,
    2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    2.220446049250313e-16
   ],
   "r_agg_E2_HS": [
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0
   ],
   "S_t_E2": 7.009496149267015e-17,
   "S_t_h": 1.2375133173866637e-30,
   "kappa2_E2": -2.1857725036605986e-16,
   "kappa2_h": -3.5691728224331273e-16,
   "kappa3_E2": -1.317121335111205e-15,
   "fit_residual": 2.1815805389137155e-16,
   "halving_dev_kappa2": 36.70942580584521,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    7.009496149266831e-17,
    -1.0159890418394039e-14,
    -1.3171213351111684e-15,
    1.62717039777404e-13
   ]
  },
  "cubic_step|111": {
   "vT_VRH": 7.7990463758448945,
   "vT_HS_lo": 7.758614490217017,
   "vT_HS_hi": 7.867953005902295,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    4.440892098500626e-16,
    6.661338147750939e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16
   ],
   "r_agg_E2_HS": [
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0
   ],
   "S_t_E2": 7.00949614926752e-17,
   "S_t_h": 6.568330085717285e-30,
   "kappa2_E2": -1.9478276488317234e-15,
   "kappa2_h": -2.0861676807089763e-15,
   "kappa3_E2": -1.3171213351113003e-15,
   "fit_residual": 2.1383492789520715e-16,
   "halving_dev_kappa2": 3.2315974980991067,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    7.009496149266832e-17,
    -9.84213081218537e-15,
    -1.3171213351111702e-15,
    1.2921206888215457e-13
   ]
  },
  "cubic_gem8|001": {
   "vT_VRH": 9.307899076533193,
   "vT_HS_lo": 9.211721064384875,
   "vT_HS_hi": 9.456854984584107,
   "r_agg_E2_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    0.0
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "r_agg_E2_HS": [
    2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16,
    -5.551115123125783e-16
   ],
   "S_t_E2": -9.550804974045757e-16,
   "S_t_h": 0.0,
   "kappa2_E2": -2.9881446885486723e-16,
   "kappa2_h": 0.0,
   "kappa3_E2": 1.5179666171081885e-14,
   "fit_residual": 2.409052517562122e-16,
   "halving_dev_kappa2": 36.70942580584519,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    -9.550804974045788e-16,
    -1.3348319157336616e-14,
    1.517966617108195e-14,
    2.1359117629450065e-13
   ]
  },
  "cubic_gem8|111": {
   "vT_VRH": 9.307899076533193,
   "vT_HS_lo": 9.211721064384875,
   "vT_HS_hi": 9.456854984584107,
   "r_agg_E2_VRH": [
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "r_agg_E2_HS": [
    4.440892098500626e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -5.551115123125783e-16,
    -3.3306690738754696e-16
   ],
   "S_t_E2": 2.925271284971411e-16,
   "S_t_h": 0.0,
   "kappa2_E2": -2.2936777285248548e-15,
   "kappa2_h": 0.0,
   "kappa3_E2": -1.1860380658980084e-14,
   "fit_residual": 2.220446049250313e-16,
   "halving_dev_kappa2": 8.27952094619114,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    2.9252712849713164e-16,
    -2.4646954092833455e-14,
    -1.1860380658979912e-14,
    3.658730891834499e-13
   ]
  }
 },
 "born_t0": {
  "hex_step": {
   "D0_plus": -0.020528244595327125,
   "D0_minus": -0.020528244595327125,
   "D0_avg": -0.02052824459532713,
   "D2_avg": -0.018347663163945885,
   "a2agg_residual_rel": 1.8909475942262037e-15
  },
  "hex_gem8": {
   "D0_plus": -0.028917807603071596,
   "D0_minus": -0.028917807603071596,
   "D0_avg": -0.028917807603071617,
   "D2_avg": -0.025933693584294176,
   "a2agg_residual_rel": 6.689072153715041e-16
  },
  "cubic_step": {
   "D0_plus": -0.03151342243433817,
   "D0_minus": -0.03151342243433817,
   "D0_avg": -0.031513422434338176,
   "D2_avg": -0.028537471107946338,
   "a2agg_residual_rel": 4.376704922376667e-15
  },
  "cubic_gem8": {
   "D0_plus": -0.04367714392697755,
   "D0_minus": -0.04367714392697755,
   "D0_avg": -0.043677143926977566,
   "D2_avg": -0.03971397679128604,
   "a2agg_residual_rel": 1.5724953827557158e-15
  }
 },
 "falsifiers": {
  "F-MS-3": {
   "state": "SILENT",
   "worst_S_t": 4.90291953941434e-13
  },
  "F-MS-2": {
   "state": "REGISTERED_NOT_EXECUTED"
  },
  "F-MS-1": {
   "state": "RETIRED_TO_CONTROL"
  }
 },
 "x_pins": {
  "PIN-VRH0_worst_rel": 9.898898090587927e-16,
  "PIN-HS0_worst_rel": 4.644295379818518e-12,
  "hs_references": {
   "hex_step": {
    "lo_K0_G0": [
     134.60708943792756,
     60.030800002639964
    ],
    "hi_K0_G0": [
     135.3665929776937,
     115.55987377748554
    ]
   },
   "hex_step|b": {
    "lo_K0_G0": [
     134.60708943792758,
     60.03080000263914
    ],
    "hi_K0_G0": [
     135.36658842797797,
     115.55987474358491
    ]
   },
   "hex_gem8": {
    "lo_K0_G0": [
     229.69575433713962,
     84.82450000424566
    ],
    "hi_K0_G0": [
     230.1360532921952,
     178.29434080456548
    ]
   },
   "hex_gem8|b": {
    "lo_K0_G0": [
     229.69575433713962,
     84.82450000424924
    ],
    "hi_K0_G0": [
     230.13605425859672,
     178.29434061744877
    ]
   },
   "cubic_step": {
    "lo_K0_G0": [
     123.83246666828633,
     36.725200002429304
    ],
    "hi_K0_G0": [
     123.832466665047,
     85.29339999757266
    ]
   },
   "cubic_gem8": {
    "lo_K0_G0": [
     210.27550000263054,
     46.34985000394528
    ],
    "hi_K0_G0": [
     210.27549999736948,
     131.5435999960556
    ]
   }
  }
 },
 "x_so3_grid": [
  20,
  12,
  20
 ],
 "x_runtime_s": 33.46,
 "verdict_class": "IDENTITY-DELIVERED"
}
=====END-EMBED name=inputs/gmscs1_gate/g_mscs1_ccleg_checkpoint.json=====

=====BEGIN-EMBED name=inputs/gmscs2_gate/diag_kappa24.json md5=b7952dfcaddcd1d98e424aee8ce5231f bytes=1917 encoding=raw=====
{
 "hex_step|a": {
  "kappa24_richardson": 9.483155002006545e-13,
  "D_h0p02": -9.38832345198648e-11,
  "D_h0p01": -2.275957200481571e-11
 },
 "hex_step|b": {
  "kappa24_richardson": 2.544261098099317e-13,
  "D_h0p02": -9.402201239794294e-11,
  "D_h0p01": -2.3314683517128287e-11
 },
 "hex_gem8|a": {
  "kappa24_richardson": -5.319818659662209e-13,
  "D_h0p02": -1.3829215550487106e-10,
  "D_h0p01": -3.497202527569243e-11
 },
 "hex_gem8|b": {
  "kappa24_richardson": 6.938893903907228e-13,
  "D_h0p02": -1.3863910020006642e-10,
  "D_h0p01": -3.4139358007223564e-11
 },
 "cubic_step|001": {
  "kappa24_richardson": -6.707597440443654e-13,
  "D_h0p02": 1.4852702401313422e-09,
  "D_h0p01": 3.708144902248023e-10,
  "pure_l2_r_agg_change_t1": 1.1102230246251565e-16,
  "mixed_r_agg_change_A29": 9.076177711619948e-07,
  "r_agg_0_0p25": -2.3355986619622016e-05,
  "r_agg_0p25_0p25": -2.426360439078401e-05
 },
 "cubic_step|111": {
  "kappa24_richardson": 7.401486830834377e-13,
  "D_h0p02": 1.4854784069484595e-09,
  "D_h0p01": 3.7192471324942744e-10,
  "pure_l2_r_agg_change_t1": 3.3306690738754696e-16,
  "mixed_r_agg_change_A29": 9.076177711619948e-07,
  "r_agg_0_0p25": 1.5570657746266647e-05,
  "r_agg_0p25_0p25": 1.4663039975104653e-05
 },
 "cubic_gem8|001": {
  "kappa24_richardson": -5.782411586589357e-13,
  "D_h0p02": 2.6163099464682205e-09,
  "D_h0p01": 6.536438057480609e-10,
  "pure_l2_r_agg_change_t1": 2.220446049250313e-16,
  "mixed_r_agg_change_A29": 1.3041577882066946e-06,
  "r_agg_0_0p25": -2.8020636270609245e-05,
  "r_agg_0p25_0p25": -2.932479405881594e-05
 },
 "cubic_gem8|111": {
  "kappa24_richardson": -1.8503717077085943e-13,
  "D_h0p02": 2.6162405575291814e-09,
  "D_h0p01": 6.539213615042172e-10,
  "pure_l2_r_agg_change_t1": 2.220446049250313e-16,
  "mixed_r_agg_change_A29": 1.3041577884287392e-06,
  "r_agg_0_0p25": 1.8680424180850252e-05,
  "r_agg_0p25_0p25": 1.7376266392421513e-05
 }
}
=====END-EMBED name=inputs/gmscs2_gate/diag_kappa24.json=====

=====BEGIN-EMBED name=inputs/gmscs2_gate/diag_quadform_basis.json md5=d84aa1fdce7dea1b1a5d24dfb8f13c18 bytes=1119 encoding=raw=====
{
 "cubic_step|001": {
  "k7": [
   4.48191107636109e-09,
   1.974043374986076e-07,
   -0.00037435455939106166,
   3.6410602705142863e-09,
   -1.7048890759809645e-10,
   -5.90187816860719e-05,
   2.632913334683767e-06
  ],
  "k12": [
   -9.053974820150282e-15,
   -3.529544061534051e-11,
   -0.0003743069390912568,
   3.641060270537046e-09,
   -1.704889076336002e-10,
   -5.901878168607192e-05,
   2.6329133346838128e-06,
   1.540337215208414e-13,
   1.894830996557711e-14,
   -4.412479086589967e-15,
   3.716510718732071e-06,
   -7.529609598691114e-07
  ]
 },
 "hex_step|a": {
  "k7": [
   -0.0014394693020032903,
   -1.2488790730491887e-08,
   0.00016039903763945317,
   -7.369515689363175e-07,
   -7.276386967011854e-06,
   -3.936928935774004e-06,
   2.214379693918309e-07
  ],
  "k12": [
   -0.001439454440047776,
   1.6668029803601492e-12,
   0.0001604034438794772,
   -7.36951568936323e-07,
   -7.276386967011858e-06,
   -3.936928935774002e-06,
   2.214379693918294e-07,
   -1.199644627757171e-07,
   -1.268159318600241e-07,
   -3.6031722935636756e-07,
   -1.0829856288863797e-07,
   3.11374900994371e-08
  ]
 }
}
=====END-EMBED name=inputs/gmscs2_gate/diag_quadform_basis.json=====

=====BEGIN-EMBED name=inputs/gci1_gate/ci1_phase3_cc_r2.json md5=845ae6beb1b90fe34c540f843ffdb9f5 bytes=45760 encoding=raw=====
{"gate":"G-CI1","leg":"CC","phase":3,"read":"CC r2 (S9 re-derivation, mini-dispatch path (a); the r1 blind read #1 stays the verdict read of record for the CLASS, E-9)","inputs":{"sealed_md5":"dd8fe2d364624750201ad9c9ffef575c","sealed_census":12,"ci1_phase2_cc.json":"f79113b7664addc9b1d96893aa883cbf","ci1_phase3_cc.json_r1":"e97d9a1cbf94e5e8cd390b99dab87cf0","t1_list":"653a0b7447e68aa8a094e62337a24da3","minidispatch":"4c21c43d7a2b36aa54985b2d7043b1d3","addendum4":"b3f8cbd58cd2202f971abc823eef76ac","dispatch_r1":"420082d54f11817c9d64a8198f1042ae"},"operative_branch":"CI-W/EM-IN (F-IRR FIRED, K empty; PF-2)","arm_semantics":{"readings_rules":"R2 dressing (both-k) and R3 brackets (both-edge) combined conservatively: EXCL only if every reading EXCLs; VOID never excludes","distance":"light-travel integral of the CONV row by log-substitution Simpson (u = ln(1+z')), n = 2^14, per-call doubling gate 1e-10 asserted at every bound z including the largest sealed z","energy_conversion":"k(E) = E/(hbar*c) with the reduced action constant DERIVED as h/(2*pi) from the sealed CONV anchor-slot (field-5) text, bound by named-key regex (S9-R1)","ray_attenuation":"VOID (E-11)","diff_rule":"SIGNED band criterion (negative edge binds); upper edge validity-capped at the strongest (tightest) reading validity limit \u2014 EXCL only while every bracket reading is wave-valid and excluding, VOID beyond (S9-R1, E-11; no ray-regime grant)","window_of_record":"the d->0+ connected component of the pass set; far non-excluded components disclosed alongside (H-CC-12)"},"per_oom":{"x1":{"verdict":"P-CI-W/EM-IN-WINDOWED","W_EM_union":[[0.0000000000e+00,3.7641664288e-33]],"W_EM_union_far":[[1.0812672472e+25,"inf"]],"configs":{"hex:step":{"W_EM_cfg":[[0.0000000000e+00,3.7641664288e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[2.6780311672e-09,4.7334773405e-01]],"pass_intervals":2,"voids":[[4.7334773405e-01,"inf","VOID-RAY-ATT"]],"xr_edges":[8.4191074357e-09,1.4880952381e+00]},"TR-2":{"excl":[[1.0599674567e-17,1.8207496854e-07]],"pass_intervals":2,"voids":[[1.8207496854e-07,"inf","VOID-RAY-ATT"]],"xr_edges":[7.3999688331e-11,1.2711230746e+00]},"TR-3":{"excl":[[3.5430384229e-21,3.3008862573e-11]],"pass_intervals":2,"voids":[[3.3008862573e-11,"inf","VOID-RAY-ATT"]],"xr_edges":[3.5910329288e-11,3.3456005353e-01]},"TR-4":{"excl":[[3.7641664288e-33,5.7057700047e-19]],"pass_intervals":2,"voids":[[5.7057700047e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[5.5624979822e-14,8.4317032040e+00]},"ACH-DIM":{"excl":[[1.5172429595e-15,7.2939937256e-07]],"pass_intervals":2,"voids":[[7.2939937256e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,7.9577471546e-04,"VOID-RAY-ATT"],[7.9577471546e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[1.9066237341e-12,9.1659028414e-04]},"ACH-DISP":{"excl":[[1.1695208816e-21,9.8663490230e-12]],"pass_intervals":2,"voids":[[9.8663490230e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[1.7780450684e-10,1.5000000000e+00]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[7.7085927896e-18,1.9732698046e-12]],"pass_intervals":2,"voids":[[1.9732698046e-12,"inf","VOID-VALIDITY"]],"xr_edges":[3.9065072458e-06,1.0000000000e+00]}}},"hex:gem8":{"W_EM_cfg":[[0.0000000000e+00,3.3478202275e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[2.3818200074e-09,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[7.4878884087e-09,4.7057703277e-01]},"TR-2":{"excl":[[9.4272677869e-18,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[6.5814744939e-11,4.0196441022e-01]},"TR-3":{"excl":[[3.1511507058e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[3.1938366446e-11,1.0579717833e-01]},"TR-4":{"excl":[[3.3478202275e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[4.9472422679e-14,2.6663386680e+00]},"ACH-DIM":{"excl":[[1.3494240400e-15,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[1.6957362603e-12,2.8985129791e-04]},"ACH-DISP":{"excl":[[9.8370794267e-22,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[1.4955500870e-10,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[6.4838551182e-18,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[3.2858431742e-06,3.1622776602e-01]}}},"cubic:step":{"W_EM_cfg":[[0.0000000000e+00,3.2619132000e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[2.3207011113e-09,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[7.2957448074e-09,4.7057703277e-01]},"TR-2":{"excl":[[9.1853585751e-18,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[6.4125900045e-11,4.0196441022e-01]},"TR-3":{"excl":[[3.0702903335e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[3.1118809261e-11,1.0579717833e-01]},"TR-4":{"excl":[[3.2619132000e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[4.8202931343e-14,2.6663386680e+00]},"ACH-DIM":{"excl":[[1.3147970290e-15,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[1.6522226749e-12,2.8985129791e-04]},"ACH-DISP":{"excl":[[9.3775766632e-22,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[1.4256909990e-10,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[6.1809858197e-18,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[3.1323571695e-06,3.1622776602e-01]}}},"cubic:gem8":{"W_EM_cfg":[[0.0000000000e+00,2.9185931177e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[2.0764446741e-09,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[6.5278593505e-09,4.7057703277e-01]},"TR-2":{"excl":[[8.2185891153e-18,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[5.7376575972e-11,4.0196441022e-01]},"TR-3":{"excl":[[2.7471387762e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[2.7843519116e-11,1.0579717833e-01]},"TR-4":{"excl":[[2.9185931177e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[4.3129517876e-14,2.6663386680e+00]},"ACH-DIM":{"excl":[[1.1764131430e-15,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[1.4783243551e-12,2.8985129791e-04]},"ACH-DISP":{"excl":[[7.9492590205e-22,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[1.2085411233e-10,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[5.2395473850e-18,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[2.6552615222e-06,3.1622776602e-01]}}}}},"x10":{"verdict":"P-CI-W/EM-IN-WINDOWED","W_EM_union":[[0.0000000000e+00,8.1096507332e-33]],"W_EM_union_far":[[1.0812672472e+25,"inf"]],"configs":{"hex:step":{"W_EM_cfg":[[0.0000000000e+00,8.1096507332e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[5.7696432477e-09,4.7334773405e-01]],"pass_intervals":2,"voids":[[4.7334773405e-01,"inf","VOID-RAY-ATT"]],"xr_edges":[1.8138417119e-08,1.4880952381e+00]},"TR-2":{"excl":[[2.2836306589e-17,1.8207496854e-07]],"pass_intervals":2,"voids":[[1.8207496854e-07,"inf","VOID-RAY-ATT"]],"xr_edges":[1.5942749559e-10,1.2711230746e+00]},"TR-3":{"excl":[[7.6332448864e-21,3.3008862573e-11]],"pass_intervals":2,"voids":[[3.3008862573e-11,"inf","VOID-RAY-ATT"]],"xr_edges":[7.7366459149e-11,3.3456005353e-01]},"TR-4":{"excl":[[8.1096507332e-33,5.7057700047e-19]],"pass_intervals":2,"voids":[[5.7057700047e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[1.1984038616e-13,8.4317032040e+00]},"ACH-DIM":{"excl":[[3.2688008651e-15,7.2939937256e-07]],"pass_intervals":2,"voids":[[7.2939937256e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,7.9577471546e-04,"VOID-RAY-ATT"],[7.9577471546e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[4.1076963135e-12,9.1659028414e-04]},"ACH-DISP":{"excl":[[3.6983497570e-21,9.8663490230e-12]],"pass_intervals":2,"voids":[[9.8663490230e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[5.6226721987e-10,1.5000000000e+00]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[2.4376710770e-17,1.9732698046e-12]],"pass_intervals":2,"voids":[[1.9732698046e-12,"inf","VOID-VALIDITY"]],"xr_edges":[1.2353460593e-05,1.0000000000e+00]}}},"hex:gem8":{"W_EM_cfg":[[0.0000000000e+00,7.2126600340e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[5.1314756495e-09,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[1.6132166543e-08,4.7057703277e-01]},"TR-2":{"excl":[[2.0310432752e-17,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[1.4179356961e-10,4.0196441022e-01]},"TR-3":{"excl":[[6.7889483941e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[6.8809124614e-11,1.0579717833e-01]},"TR-4":{"excl":[[7.2126600340e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[1.0658510362e-13,2.6663386680e+00]},"ACH-DIM":{"excl":[[2.9072459634e-15,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[3.6533530243e-12,2.8985129791e-04]},"ACH-DISP":{"excl":[[3.1107576512e-21,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[4.7293446299e-10,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[2.0503750192e-17,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[1.0390748464e-05,3.1622776602e-01]}}},"cubic:step":{"W_EM_cfg":[[0.0000000000e+00,7.0275789540e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[4.9997989794e-09,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[1.5718205703e-08,4.7057703277e-01]},"TR-2":{"excl":[[1.9789255155e-17,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[1.3815506359e-10,4.0196441022e-01]},"TR-3":{"excl":[[6.6147400029e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[6.7043442184e-11,1.0579717833e-01]},"TR-4":{"excl":[[7.0275789540e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[1.0385006745e-13,2.6663386680e+00]},"ACH-DIM":{"excl":[[2.8326443296e-15,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[3.5596058464e-12,2.8985129791e-04]},"ACH-DISP":{"excl":[[2.9654501189e-21,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[4.5084307964e-10,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[1.9545993376e-17,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[9.9053831007e-06,3.1622776602e-01]}}},"cubic:gem8":{"W_EM_cfg":[[0.0000000000e+00,6.2879182588e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[4.4735644379e-09,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[1.4063846636e-08,4.7057703277e-01]},"TR-2":{"excl":[[1.7706413493e-17,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[1.2361408567e-10,4.0196441022e-01]},"TR-3":{"excl":[[5.9185310779e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[5.9987043476e-11,1.0579717833e-01]},"TR-4":{"excl":[[6.2879182588e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[9.2919729477e-14,2.6663386680e+00]},"ACH-DIM":{"excl":[[2.5345052852e-15,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[3.1849532737e-12,2.8985129791e-04]},"ACH-DISP":{"excl":[[2.5137764216e-21,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[3.8217425955e-10,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[1.6568903645e-17,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[8.3966741934e-06,3.1622776602e-01]}}}}},"x0.1":{"verdict":"P-CI-W/EM-IN-WINDOWED","W_EM_union":[[0.0000000000e+00,1.7471712864e-33]],"W_EM_union_far":[[1.0812672472e+25,"inf"]],"configs":{"hex:step":{"W_EM_cfg":[[0.0000000000e+00,1.7471712864e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[1.2430319562e-09,4.7334773405e-01]],"pass_intervals":2,"voids":[[4.7334773405e-01,"inf","VOID-RAY-ATT"]],"xr_edges":[3.9078035063e-09,1.4880952381e+00]},"TR-2":{"excl":[[4.9199331108e-18,1.8207496854e-07]],"pass_intervals":2,"voids":[[1.8207496854e-07,"inf","VOID-RAY-ATT"]],"xr_edges":[3.4347612705e-11,1.2711230746e+00]},"TR-3":{"excl":[[1.6445327581e-21,3.3008862573e-11]],"pass_intervals":2,"voids":[[3.3008862573e-11,"inf","VOID-RAY-ATT"]],"xr_edges":[1.6668098344e-11,3.3456005353e-01]},"TR-4":{"excl":[[1.7471712864e-33,5.7057700047e-19]],"pass_intervals":2,"voids":[[5.7057700047e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[2.5818828521e-14,8.4317032040e+00]},"ACH-DIM":{"excl":[[7.0424179786e-16,7.2939937256e-07]],"pass_intervals":2,"voids":[[7.2939937256e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,7.9577471546e-04,"VOID-RAY-ATT"],[7.9577471546e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[8.8497634340e-13,9.1659028414e-04]},"ACH-DISP":{"excl":[[3.6983497570e-22,9.8663490230e-12]],"pass_intervals":2,"voids":[[9.8663490230e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[5.6226721987e-11,1.5000000000e+00]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[2.4376710770e-18,1.9732698046e-12]],"pass_intervals":2,"voids":[[1.9732698046e-12,"inf","VOID-VALIDITY"]],"xr_edges":[1.2353460593e-06,1.0000000000e+00]}}},"hex:gem8":{"W_EM_cfg":[[0.0000000000e+00,1.5539204985e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[1.1055429150e-09,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[3.4755699225e-09,4.7057703277e-01]},"TR-2":{"excl":[[4.3757500891e-18,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[3.0548498520e-11,4.0196441022e-01]},"TR-3":{"excl":[[1.4626345929e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[1.4824476506e-11,1.0579717833e-01]},"TR-4":{"excl":[[1.5539204985e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[2.2963064468e-14,2.6663386680e+00]},"ACH-DIM":{"excl":[[6.2634715560e-16,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[7.8709104906e-13,2.8985129791e-04]},"ACH-DISP":{"excl":[[3.1107576512e-22,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[4.7293446299e-11,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[2.0503750192e-18,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[1.0390748464e-06,3.1622776602e-01]}}},"cubic:step":{"W_EM_cfg":[[0.0000000000e+00,1.5140459885e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[1.0771740365e-09,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[3.3863847631e-09,4.7057703277e-01]},"TR-2":{"excl":[[4.2634657795e-18,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[2.9764606159e-11,4.0196441022e-01]},"TR-3":{"excl":[[1.4251025328e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[1.4444071758e-11,1.0579717833e-01]},"TR-4":{"excl":[[1.5140459885e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[2.2373818787e-14,2.6663386680e+00]},"ACH-DIM":{"excl":[[6.1027472082e-16,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[7.6689383184e-13,2.8985129791e-04]},"ACH-DISP":{"excl":[[2.9654501189e-22,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[4.5084307964e-11,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[1.9545993376e-18,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[9.9053831007e-07,3.1622776602e-01]}}},"cubic:gem8":{"W_EM_cfg":[[0.0000000000e+00,1.3546909225e-33]],"W_EM_cfg_far":[[1.0812672472e+25,"inf"]],"arms":{"TR-1":{"excl":[[9.6380024131e-10,1.4968569649e-01]],"pass_intervals":2,"voids":[[1.4968569649e-01,4.7334773405e-01,"VOID-GAP"],[4.7334773405e-01,1.0058878804e+00,"VOID-RAY-ATT"],[1.0058878804e+00,3.1808967728e+00,"VOID-GAP"],[3.1808967728e+00,"inf","VOID-RAY-ATT"]],"xr_edges":[3.0299639069e-09,4.7057703277e-01]},"TR-2":{"excl":[[3.8147311466e-18,5.7577160551e-08]],"pass_intervals":2,"voids":[[5.7577160551e-08,1.8207496854e-07,"VOID-GAP"],[1.8207496854e-07,4.2779830289e-07,"VOID-RAY-ATT"],[4.2779830289e-07,1.3528170163e-06,"VOID-GAP"],[1.3528170163e-06,"inf","VOID-RAY-ATT"]],"xr_edges":[2.6631847434e-11,4.0196441022e-01]},"TR-3":{"excl":[[1.2751088668e-21,1.0438318870e-11]],"pass_intervals":2,"voids":[[1.0438318870e-11,3.3008862573e-11,"VOID-GAP"],[3.3008862573e-11,8.9143243152e-11,"VOID-RAY-ATT"],[8.9143243152e-11,4.6212407602e-10,"VOID-GAP"],[4.6212407602e-10,1.2480054041e-09,"VOID-RAY-ATT"],[1.2480054041e-09,3.9465396092e-09,"VOID-GAP"],[3.9465396092e-09,"inf","VOID-RAY-ATT"]],"xr_edges":[1.2923816742e-11,1.0579717833e-01]},"TR-4":{"excl":[[1.3546909225e-33,1.8043229020e-19]],"pass_intervals":2,"voids":[[1.8043229020e-19,6.7670432256e-19,"VOID-GAP"],[6.7670432256e-19,"inf","VOID-RAY-ATT"]],"xr_edges":[2.0018948857e-14,2.6663386680e+00]},"ACH-DIM":{"excl":[[5.4604261084e-16,2.3065633412e-07]],"pass_intervals":2,"voids":[[2.3065633412e-07,7.2939937256e-06,"VOID-GAP"],[7.2939937256e-06,2.5164606052e-04,"VOID-RAY-ATT"],[2.5164606052e-04,7.9577471546e-03,"VOID-GAP"],[7.9577471546e-03,"inf","VOID-RAY-ATT"]],"xr_edges":[6.8617738191e-13,2.8985129791e-04]},"ACH-DISP":{"excl":[[2.5137764216e-22,3.1200135103e-12]],"pass_intervals":2,"voids":[[3.1200135103e-12,6.5775660153e-11,"VOID-GAP"]],"xr_edges":[3.8217425955e-11,4.7434164903e-01]},"BIR-1":{"excl":[[6.6620546222e-01,2.3119153034e+24]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.6620546222e-01,"VOID-N"],[2.3119153034e+24,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,2.1804372809e+26]},"BIR-2":{"excl":[[6.1992099217e-11,1.0812672472e+25]],"pass_intervals":2,"voids":[[0.0000000000e+00,6.1992099217e-11,"VOID-N"],[1.0812672472e+25,"inf","VOID-N"]],"xr_edges":[6.2831853072e+01,1.0959142482e+37]},"POL":{"state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"},"DIFF":{"excl":[[1.6568903645e-18,6.2400270206e-13]],"pass_intervals":2,"voids":[[6.2400270206e-13,"inf","VOID-VALIDITY"]],"xr_edges":[8.3966741934e-07,3.1622776602e-01]}}}}}},"verdict_class":"P-CI-W/EM-IN-WINDOWED","oom_robust":true,"W_union_gpoly1":"SUSPENDED (PF-1); reported alongside: (0, 2.1213132100130068]","s9_rederivation":{"scope":{"rederived":["TR-3","TR-4","ACH-DISP","BIR-2","DIFF","ACH-DIM"],"carried":["TR-1","TR-2","BIR-1","POL"],"not_rerun":"phases 0-2, F-IRR, verdict-class machinery; windows and OOM bands recomputed from the corrected arm set"},"kE_binding":{"statement":"k(E) = E/(hbar*c); hbar derived as h/(2*pi) from the sealed CONV anchor-slot (field-5) text; h bound by named-key regex and role-asserted; definition markers for k(E), k(lambda), k(nu) asserted present in field 5","source":"sealed CONV row, field 5 (anchor_text slot); channel-speed import and RULES R1-R4 taken from field 6 (params) per the confirmed field map","h_role_matched":"EK_H_JS","hbar_derivation_marker_found":true,"kE_definition_marker_found":true},"diff_rule":{"band_edge":"the sealed sign map fixes the in-model differential negative; the criterion is signed and the NEGATIVE band edge binds","upper_edge":"validity-capped at the strongest-reading validity limit; VOID beyond (E-11, no ray-regime grant; a VOID can only widen a window); no unbounded exclusion"},"D_lt_largest_z":{"z_note":"largest sealed z (the CMB-epoch row)","old_linear_ladder_n4096":1.3053923867e+26,"old_linear_doubling_reldev_4096_vs_8192":1.5182188875e-04,"old_ladder_passes_1e-10_gate_at_largest_z":false,"new_log_ladder_2p14":1.3051793345e+26,"new_log_doubling_reldev_2p14_vs_2p15":7.6344482810e-15,"new_ladder_passes_1e-10_gate_at_largest_z":true,"new_over_old_minus_1":-1.6320931755e-04,"per_z_gate_evidence":{"0.186":{"new":2.2386445023e+25,"new_doubling_reldev":5.7556712889e-15,"old_4096":2.2386445023e+25,"old_doubling_reldev":3.8371141926e-15},"0.193":{"new":2.3119153034e+25,"new_doubling_reldev":1.6719775853e-14,"old_4096":2.3119153034e+25,"old_doubling_reldev":4.4586068942e-15},"2.739":{"new":1.0812672472e+26,"new_doubling_reldev":9.3742993185e-15,"old_4096":1.0812672472e+26,"old_doubling_reldev":4.7665928738e-16},"5.72":{"new":1.2117499834e+26,"new_doubling_reldev":1.6162616991e-14,"old_4096":1.2117499834e+26,"old_doubling_reldev":1.4829909976e-13},"6.43":{"new":1.2247981823e+26,"new_doubling_reldev":1.2904558382e-14,"old_4096":1.2247981823e+26,"old_doubling_reldev":2.3200151700e-13},"7.54":{"new":1.2399377404e+26,"new_doubling_reldev":2.6325314881e-15,"old_4096":1.2399377404e+26,"old_doubling_reldev":4.2605443821e-13},"1090":{"new":1.3051793345e+26,"new_doubling_reldev":7.6344482810e-15,"old_4096":1.3053923867e+26,"old_doubling_reldev":1.5182188875e-04}}},"per_arm_old_new_x1":{"hex:step":{"TR-3":{"old_excl_r1":[[4.1078604976e-20,2.0740080032e-10]],"new_excl_r2":[[3.5430384229e-21,3.3008862573e-11]],"old_over_new_edge_ratios":[[1.1594174286e+01,6.2831853071e+00]]},"TR-4":{"old_excl_r1":[[4.3642401616e-32,3.5850410260e-18]],"new_excl_r2":[[3.7641664288e-33,5.7057700047e-19]],"old_over_new_edge_ratios":[[1.1594174286e+01,6.2831853072e+00]]},"ACH-DISP":{"old_excl_r1":[[7.3483164197e-21,6.1992099217e-11]],"new_excl_r2":[[1.1695208816e-21,9.8663490230e-12]],"old_over_new_edge_ratios":[[6.2831853072e+00,6.2831853072e+00]]},"BIR-2":{"old_excl_r1":[[3.8950784696e-10,1.0812672472e+25]],"new_excl_r2":[[6.1992099217e-11,1.0812672472e+25]],"old_over_new_edge_ratios":[[6.2831853072e+00,1.0000000000e+00]]},"DIFF":{"old_excl_r1":[[1.0026897610e-16,"inf"]],"new_excl_r2":[[7.7085927896e-18,1.9732698046e-12]],"old_over_new_edge_ratios":[[1.3007429350e+01,"inf-vs-finite"]]},"ACH-DIM":{"old_excl_r1":[[1.5171604123e-15,7.2939937256e-07]],"new_excl_r2":[[1.5172429595e-15,7.2939937256e-07]],"old_over_new_edge_ratios":[[9.9994559396e-01,1.0000000000e+00]]},"TR-1":{"old_excl_r1":[[2.6780311672e-09,4.7334773405e-01]],"new_excl_r2":[[2.6780311672e-09,4.7334773405e-01]],"old_over_new_edge_ratios":[[9.9999999999e-01,1.0000000000e+00]],"carried_identity_worst_reldev":1.3634421827e-11},"TR-2":{"old_excl_r1":[[1.0599674567e-17,1.8207496854e-07]],"new_excl_r2":[[1.0599674567e-17,1.8207496854e-07]],"old_over_new_edge_ratios":[[1.0000000000e+00,9.9999999998e-01]],"carried_identity_worst_reldev":3.7492538867e-11},"BIR-1":{"old_excl_r1":[[6.6620546222e-01,2.3119153034e+24]],"new_excl_r2":[[6.6620546222e-01,2.3119153034e+24]],"old_over_new_edge_ratios":[[1.0000000000e+00,1.0000000000e+00]],"carried_identity_worst_reldev":1.6794666516e-11},"POL":{"old_state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)","new_state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)","identical":true}},"hex:gem8":{"TR-3":{"old_excl_r1":[[3.6534990484e-20,6.5585891757e-11]],"new_excl_r2":[[3.1511507058e-21,1.0438318870e-11]],"old_over_new_edge_ratios":[[1.1594174286e+01,6.2831853072e+00]]},"TR-4":{"old_excl_r1":[[3.8815211194e-32,1.1336895147e-18]],"new_excl_r2":[[3.3478202275e-33,1.8043229020e-19]],"old_over_new_edge_ratios":[[1.1594174286e+01,6.2831853070e+00]]},"ACH-DISP":{"old_excl_r1":[[6.1808192920e-21,1.9603623046e-11]],"new_excl_r2":[[9.8370794267e-22,3.1200135103e-12]],"old_over_new_edge_ratios":[[6.2831853072e+00,6.2831853071e+00]]},"BIR-2":{"old_excl_r1":[[3.8950784696e-10,1.0812672472e+25]],"new_excl_r2":[[6.1992099217e-11,1.0812672472e+25]],"old_over_new_edge_ratios":[[6.2831853072e+00,1.0000000000e+00]]},"DIFF":{"old_excl_r1":[[8.4338287368e-17,"inf"]],"new_excl_r2":[[6.4838551182e-18,6.2400270206e-13]],"old_over_new_edge_ratios":[[1.3007429350e+01,"inf-vs-finite"]]},"ACH-DIM":{"old_excl_r1":[[1.3493506232e-15,2.3065633412e-07]],"new_excl_r2":[[1.3494240400e-15,2.3065633412e-07]],"old_over_new_edge_ratios":[[9.9994559395e-01,1.0000000000e+00]]},"TR-1":{"old_excl_r1":[[2.3818200074e-09,1.4968569649e-01]],"new_excl_r2":[[2.3818200074e-09,1.4968569649e-01]],"old_over_new_edge_ratios":[[9.9999999998e-01,1.0000000000e+00]],"carried_identity_worst_reldev":2.0367823099e-11},"TR-2":{"old_excl_r1":[[9.4272677869e-18,5.7577160551e-08]],"new_excl_r2":[[9.4272677869e-18,5.7577160551e-08]],"old_over_new_edge_ratios":[[1.0000000000e+00,1.0000000000e+00]],"carried_identity_worst_reldev":3.5355310696e-12},"BIR-1":{"old_excl_r1":[[6.6620546222e-01,2.3119153034e+24]],"new_excl_r2":[[6.6620546222e-01,2.3119153034e+24]],"old_over_new_edge_ratios":[[1.0000000000e+00,1.0000000000e+00]],"carried_identity_worst_reldev":1.6794666516e-11},"POL":{"old_state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)","new_state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)","identical":true}},"cubic:step":{"TR-3":{"old_excl_r1":[[3.5597481234e-20,6.5585891757e-11]],"new_excl_r2":[[3.0702903335e-21,1.0438318870e-11]],"old_over_new_edge_ratios":[[1.1594174286e+01,6.2831853072e+00]]},"TR-4":{"old_excl_r1":[[3.7819190146e-32,1.1336895147e-18]],"new_excl_r2":[[3.2619132000e-33,1.8043229020e-19]],"old_over_new_edge_ratios":[[1.1594174286e+01,6.2831853070e+00]]},"ACH-DISP":{"old_excl_r1":[[5.8921051907e-21,1.9603623046e-11]],"new_excl_r2":[[9.3775766632e-22,3.1200135103e-12]],"old_over_new_edge_ratios":[[6.2831853071e+00,6.2831853071e+00]]},"BIR-2":{"old_excl_r1":[[3.8950784696e-10,1.0812672472e+25]],"new_excl_r2":[[6.1992099217e-11,1.0812672472e+25]],"old_over_new_edge_ratios":[[6.2831853072e+00,1.0000000000e+00]]},"DIFF":{"old_excl_r1":[[8.0398736366e-17,"inf"]],"new_excl_r2":[[6.1809858197e-18,6.2400270206e-13]],"old_over_new_edge_ratios":[[1.3007429350e+01,"inf-vs-finite"]]},"ACH-DIM":{"old_excl_r1":[[1.3147254961e-15,2.3065633412e-07]],"new_excl_r2":[[1.3147970290e-15,2.3065633412e-07]],"old_over_new_edge_ratios":[[9.9994559397e-01,1.0000000000e+00]]},"TR-1":{"old_excl_r1":[[2.3207011113e-09,1.4968569649e-01]],"new_excl_r2":[[2.3207011113e-09,1.4968569649e-01]],"old_over_new_edge_ratios":[[9.9999999999e-01,1.0000000000e+00]],"carried_identity_worst_reldev":1.3714930998e-11},"TR-2":{"old_excl_r1":[[9.1853585751e-18,5.7577160551e-08]],"new_excl_r2":[[9.1853585751e-18,5.7577160551e-08]],"old_over_new_edge_ratios":[[1.0000000000e+00,1.0000000000e+00]],"carried_identity_worst_reldev":4.4469317850e-12},"BIR-1":{"old_excl_r1":[[6.6620546222e-01,2.3119153034e+24]],"new_excl_r2":[[6.6620546222e-01,2.3119153034e+24]],"old_over_new_edge_ratios":[[1.0000000000e+00,1.0000000000e+00]],"carried_identity_worst_reldev":1.6794666516e-11},"POL":{"old_state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)","new_state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)","identical":true}},"cubic:gem8":{"TR-3":{"old_excl_r1":[[3.1850805759e-20,6.5585891757e-11]],"new_excl_r2":[[2.7471387762e-21,1.0438318870e-11]],"old_over_new_edge_ratios":[[1.1594174286e+01,6.2831853072e+00]]},"TR-4":{"old_excl_r1":[[3.3838677276e-32,1.1336895147e-18]],"new_excl_r2":[[2.9185931177e-33,1.8043229020e-19]],"old_over_new_edge_ratios":[[1.1594174286e+01,6.2831853070e+00]]},"ACH-DISP":{"old_excl_r1":[[4.9946667481e-21,1.9603623046e-11]],"new_excl_r2":[[7.9492590205e-22,3.1200135103e-12]],"old_over_new_edge_ratios":[[6.2831853072e+00,6.2831853071e+00]]},"BIR-2":{"old_excl_r1":[[3.8950784696e-10,1.0812672472e+25]],"new_excl_r2":[[6.1992099217e-11,1.0812672472e+25]],"old_over_new_edge_ratios":[[6.2831853072e+00,1.0000000000e+00]]},"DIFF":{"old_excl_r1":[[6.8153042438e-17,"inf"]],"new_excl_r2":[[5.2395473850e-18,6.2400270206e-13]],"old_over_new_edge_ratios":[[1.3007429350e+01,"inf-vs-finite"]]},"ACH-DIM":{"old_excl_r1":[[1.1763491390e-15,2.3065633412e-07]],"new_excl_r2":[[1.1764131430e-15,2.3065633412e-07]],"old_over_new_edge_ratios":[[9.9994559392e-01,1.0000000000e+00]]},"TR-1":{"old_excl_r1":[[2.0764446741e-09,1.4968569649e-01]],"new_excl_r2":[[2.0764446741e-09,1.4968569649e-01]],"old_over_new_edge_ratios":[[9.9999999998e-01,1.0000000000e+00]],"carried_identity_worst_reldev":2.2602172159e-11},"TR-2":{"old_excl_r1":[[8.2185891153e-18,5.7577160551e-08]],"new_excl_r2":[[8.2185891153e-18,5.7577160551e-08]],"old_over_new_edge_ratios":[[1.0000000000e+00,1.0000000000e+00]],"carried_identity_worst_reldev":3.5355310696e-12},"BIR-1":{"old_excl_r1":[[6.6620546222e-01,2.3119153034e+24]],"new_excl_r2":[[6.6620546222e-01,2.3119153034e+24]],"old_over_new_edge_ratios":[[1.0000000000e+00,1.0000000000e+00]],"carried_identity_worst_reldev":1.6794666516e-11},"POL":{"old_state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)","new_state":"VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)","identical":true}}},"carried_arm_identity_worst_reldev":3.7492538867e-11},"expectation_pins":["PIN-CC-P3-1..5: unchanged from r1 (named-key binders with loud masked halts; doubling-gated D_lt; 24/decade + 64-step bisection; own-curve lookups; conservative reading combiner).","PIN-CC-S9-1: with the corrected k(E), the r1-over-r2 edge ratios must reproduce the S9 fingerprints \u2014 (2*pi)^(4/3) on TR-3/TR-4 Rayleigh onsets, 2*pi on their validity cutoffs, 2*pi on both ACH-DISP edges, 2*pi on the BIR-2 live edge with its upper (N-rule, k-independent) edge unchanged, 2*pi*sqrt(30/7) on the DIFF onset with the upper edge finite (validity-capped).","PIN-CC-S9-2: the ACH-DIM D-independent validity edge must not move; the onset moves only through D_lt at the largest sealed z.","PIN-CC-S9-3: carried arms TR-1, TR-2, BIR-1, POL re-emitted from unchanged machinery; identity to r1 evidenced (worst relative edge deviation reported; expected at the D_lt-quadrature noise floor, orders below the 1e-6 comparison tolerance).","PIN-CC-S9-4: derive, never transcribe \u2014 every edge below comes from this leg's own Phase-2 curves and quadratures; the disclosed expected edges are compared only AFTER computation, by the chat leg's frozen run-3 comparator."],"honesty":["G-CI1.H-CC-8 (root-cause acknowledgment, S9 primary): CONFIRMED in this leg's own r1 source. The r1 CONV binder did read the sealed row's 5th (anchor-slot) field, but bound its constants by MAGNITUDE WINDOW, not named key: the reduced-action-constant role was filled by the only J*s-magnitude numeral present, which is the action quantum h itself \u2014 the sealed text defines the reduced constant ONLY symbolically (h/(2*pi)) and pins k(E) = E/(hbar*c). Every energy-anchored k was therefore a factor 2*pi low, while the frequency/wavelength arms used the sealed 2*pi-carrying forms \u2014 the internal inconsistency named in the mini-dispatch, reproduced here as the r1-over-r2 edge ratios (2*pi)^(4/3) on Rayleigh onsets and 2*pi on validity/live edges. The r1 pin PIN-CC-P3-1 promised named-key binding; the CONV constants path fell short of that pin. Fixed by the r2 named-key binder with derivation-marker asserts.","G-CI1.H-CC-9 (S9 secondary, DIFF band edge): the r1 DIFF criterion tested the band against abs(Delta_ch) under a both-signs rule, letting the positive band edge govern; the sealed sign map fixes the in-model differential NEGATIVE, so the negative band edge binds. r2 evaluates the signed value (onset ratio r1/r2 = 2*pi*sqrt(30/7), the k factor combined with the band-edge factor sqrt(30/7)).","G-CI1.H-CC-10 (S9 secondary, DIFF upper edge): the r1 read granted the ray-regime geometric bracket and extended the DIFF exclusion unbounded; election E-11 grants no ray regime to this arm \u2014 r2 caps the exclusion at the strongest-reading validity limit and returns VOID beyond (a VOID can only widen a window).","G-CI1.H-CC-11 (S9 tertiary, ACH-DIM onset): the r1 D_lt ladder was fixed-step linear-z Simpson n=4096 with its doubling gate asserted at z <= 6 only; at the largest sealed z its own 4096-vs-8192 doubling deviation is 1.518e-04 (gate 1e-10: FAILS), and its value there sits 1.632e-04 relative ABOVE the gate-passing log-substitution ladder \u2014 the D^(-1/3) signature the chat leg attributed. r2 uses u = ln(1+z') Simpson n = 2^14 with the 1e-10 doubling gate asserted per call at every bound z including the largest (deviation 7.634e-15).","G-CI1.H-CC-13 (self-catch, r2 instrument, numbered per the standing rule): the FIRST r2 evaluation run implemented the DIFF validity cap with a special combiner that kept excluding while ANY bracket reading remained wave-valid (mixed EXCL/VOID treated as EXCL), putting the upper edge at the loosest reading's validity limit \u2014 a factor k_hi/k_lo high against the embedded S9 record. Caught on first read of that run's output against the record; resolved by the sealed R3 rule itself, which is dispositive without the record: exclusion is asserted only where BOTH bracket edges exclude, and a reading beyond wave validity is VOID, not excluding \u2014 so the standard conservative combiner already caps the exclusion at the tightest reading validity limit. The special combiner was removed (the DIFF arm now uses the same combiner as every other arm); the defective run's checkpoint was superseded in place before any return, and no other arm changed between the runs.","G-CI1.H-CC-12 (window-of-record disclosure): with the DIFF exclusion validity-capped (E-11), the region beyond the largest arm exclusion edge is no longer excluded by any arm \u2014 every arm is VOID there by its own N-rule, ray rule, or validity cap. The checkpoint's W_EM keys carry the d->0+ connected component (the window of record, G-POLY1 WINDOWED-class lineage) and the far non-excluded components are serialized alongside under *_far keys. Nothing is silently dropped; VOID never excludes and never counts as FAIL."]}
=====END-EMBED name=inputs/gci1_gate/ci1_phase3_cc_r2.json=====

=====BEGIN-EMBED name=sealed/anchors_G_MSCS_A_SEALED.md.b64 md5=904a8dffbe8ef50e0555bf278c7581b0 bytes=409 encoding=raw QUARANTINED-UNTIL-PHASE-3=====
=====BEGIN-EMBED name=anchors_G_MSCS_A_SEALED.md md5=cfd62dcf060427ac3402604e6c3284ff bytes=177 encoding=base64=====
aWQ9U0EtMSB8IGNsYXNzPXNwZCB8IGRlbHRhX2RlZj10ZW5zb3Jfb3Zlcl9FTV9taW51c18xIHwg
bG89LTNlLTE1IHwgaGk9N2UtMTYgfCBjbD1oYXJkIHwgcmVhZGluZz1ib3VuZCB8IGdlb209c2lu
Z2xlIHwga19lbV9tYXg9NWUxMiB8IGtfdF9tYXg9MmUtNSB8IHNyYz1HVzE3MDgxN19BcEpMXzg0
OF9MMTMK
=====END-EMBED name=anchors_G_MSCS_A_SEALED.md=====

=====END-EMBED name=sealed/anchors_G_MSCS_A_SEALED.md.b64=====

=====BEGIN-EMBED name=g_mscs_a_chatleg.py md5=0d0e5ecf610b34f21e8c22dd3938ce40 bytes=51490 encoding=base64 armor_bytes=69560 QUARANTINED=====
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX21zY3NfYV9jaGF0bGVnLnB5IC0tIEdhdGUgRy1N
U0NTLUEsIGNoYXQtbGVnIG1hcHBlciAobWVtbyA2ZWExNmI5NSBzZWN0aW9ucyAzLTY7IGxvY2sg
cmVjb3JkIEFkZGVuZHVtIEEtMikuCgpUaGUgd2hvbGUgY29tcHV0YXRpb24gb2YgdGhlIGdhdGU6
IFBoYXNlIDAgKHBpbnMgYW5kIGNvbnRyb2xzOyBoYWx0LW9uLWZhaWwpLCBQaGFzZSAyICh0aGUg
Zm91cnRlZW4gc3ludGhldGljCnByZS1yZWFkIHN1aXRlczsgYWxsIG11c3QgcGFzcyBiZWZvcmUg
YW55IHNlYWxlZCBvcGVuKSBhbmQgUGhhc2UgMyAodGhlIG1hc2tlZCByZWFkIG9mIHRoZSBhdXRo
b3IncyBzZWFsZWQgYW5jaG9yIGZpbGUKYW5kIGl0cyBtYXBwaW5nIG9udG8gdGhlIGJhbmtlZCB0
ZXh0dXJlIHN1cmZhY2UpLiBFdmVyeSBiYW5rZWQgdmFsdWUgaXMgcmVhZCBmcm9tIHRoZSBwaW5u
ZWQtaW5wdXRzIGZpbGUgb2YgcmVjb3JkIGJ5Cm5hbWU7IHRoZSBzZWFsZWQgZmlsZSBpcyB0aGUg
b25seSBvdGhlciBpbnB1dC4gTm8gYW5jaG9yIHZhbHVlIChsbywgaGksIGtfZW1fbWF4LCBrX3Rf
bWF4LCBjbCwgc3JjLCBub3RlKSBpcyBldmVyCnByaW50ZWQsIGxvZ2dlZCBvciB3cml0dGVuIC0t
IG9ubHkgdGhlIGZpbGUgYW5kIHJvdyBtZDVzIGFuZCB0aGUgZGVyaXZlZCBxdWFudGl0aWVzICh3
aW5kb3dzLCBjbGFzc2VzLCBmbGFncykuCgpVc2FnZToKICBwcmVyZWFkIDogcHl0aG9uMyBnX21z
Y3NfYV9jaGF0bGVnLnB5IHByZXJlYWQgLS1yZXBvIFJFUE8gWy0tYTEgQTFfTElTVF0gWy0tb3V0
IERJUl0KICAgICAgICAgICAgUGhhc2UgMCArIFBoYXNlIDI7IHdyaXRlcyBnX21zY3NfYV9jaGF0
bGVnX3ByZXJlYWRjaGVja3BvaW50Lmpzb24gKHBoYXNlMyA9IG51bGwpLgogIHJlYWQgICAgOiBw
eXRob24zIGdfbXNjc19hX2NoYXRsZWcucHkgcmVhZCAtLXJlcG8gUkVQTyAtLXNlYWxlZCBBUk1P
UkVEIC0tbWQ1IE1ENSAtLWJ5dGVzIE4gLS1hMSBBMV9MSVNUIFstLW91dCBESVJdCiAgICAgICAg
ICAgIFBoYXNlcyAwICsgMiByZWNvbXB1dGVkIGZyb20gc2NyYXRjaCwgdGhlbiB0aGUgcmVhZDsg
d3JpdGVzIGdfbXNjc19hX2NoYXRsZWdfY2hlY2twb2ludC5qc29uLgogIGNlbnN1cyAgOiBweXRo
b24zIGdfbXNjc19hX2NoYXRsZWcucHkgY2Vuc3VzIC0tc2VhbGVkIEFSTU9SRUQgLS1tZDUgTUQ1
IC0tYnl0ZXMgTgogICAgICAgICAgICBEZWNvZGVzIGFuZCB2YWxpZGF0ZXMgb25seTsgcHJpbnRz
IG1kNSwgYnl0ZXMgYW5kIGNlbnN1cyAoZGlzcGF0Y2ggYnVpbGQsIG1lbW8gNC43KTsgbm8gbWFw
cGluZy4KRXhpdDogMCBkb25lOyAxIGhhbHRlZCAoUGhhc2UgMCBmYWlsdXJlID0gSU5ERVRFUk1J
TkFURSwgYSBQaGFzZSAyIGZhaWx1cmUsIGEgbWFza2VkIGFib3J0LCBhIFQxIGhpdCk7IDIgdXNh
Z2UuCkZpbGVzIGV4cGVjdGVkIGJlc2lkZSB0aGlzIHNjcmlwdDogc3RhZ2luZ19tZW1vX0dfTVND
U19BX3YyLm1kLCBwaW5uZWRfaW5wdXRzX0dfTVNDU19BLmpzb24sIEdfTVNDU19BX0xPQ0tfUkVD
T1JELm1kLApnX21zY3NfYV9zY2hlbWFfdjFfMC5qc29uLCBnX21zY3NfYV9jb21wYXJlX3YxXzAu
cHksIHRvb2xzL3QxL3tUMV9mb3JiaWRkZW5fR19NU0NTX0EudHh0LCBUMV9iYXNlX2F1dGhvcl8y
MDI2MDkxOS50eHQsIHQxX3NjYW4ucHl9LiIiIgppbXBvcnQgYmFzZTY0LCBkYXRldGltZSwgaGFz
aGxpYiwgaW1wb3J0bGliLnV0aWwsIGlvLCBqc29uLCBtYXRoLCBvcywgcmUsIHN5cywgdGVtcGZp
bGUsIHppcGZpbGUKCkdBVEUsIExFRyA9ICdHLU1TQ1MtQScsICdjaGF0JwpIRVJFID0gb3MucGF0
aC5kaXJuYW1lKG9zLnBhdGguYWJzcGF0aChfX2ZpbGVfXykpCkxFREdFUl9NRDUgPSAnZDRjNDJh
NTNjYmQ2ZDMyNWViYzc0MDg3OTI4OGU4NDQnCk1FTU9fTUQ1LCBNRU1PX0JZVEVTID0gJzZlYTE2
Yjk1MmRiODM1YmIzNTFkM2RjMWI0NzRjNmVkJywgMTIxOTUwClBJTl9NRDUsIFBJTl9CWVRFUyA9
ICcyZDQ0ZWMwMWE2Njg4OWYzMzBkOTQwZGVlMzMxM2JkYycsIDk2NzYxClQxX01ENSwgQkFTRV9N
RDUsIFNDQU5ORVJfTUQ1ID0gJ2UyNzRlNThlYTUwYjllZDM0Nzk2OWU1MDdkMmE0ZjM2JywgJzA1
MzAyMjEwY2M0Y2ViNzA1NTNhY2JlODM3OWU5ZmMzJywgJzZiODYyOTAwOTBhOGM4NGYxYjFhMGE5
OWVjMGJmNjk3JwpTQ0hFTUFfTUQ1LCBDT01QQVJBVE9SX01ENSA9ICc1MzIzZTExZmMyN2Q2ODhm
NjFhYWY1NzMwMmM4NzVjMCcsICdjNWI0YTdhYWIyZmM4NjUxYmU2ZDI2ZDFmM2QyNTY0MicKTE9D
S19NRDUgPSAnODExNmNjNjIyMjc5YjVkNGU3MzIxNDE3OGFlOTdjZDgnICAgIyBmaWxsZWQgYXQg
ZnJlZXplICh0aGUgbG9jayByZWNvcmQgaXMgd3JpdHRlbiBiZWZvcmUgdGhpcyBpbnN0cnVtZW50
KQpCVUlMREVSX01ENSwgVkVSSUZJRVJfTUQ1ID0gJzgxODkxMDBlZGU4MGVhYzM2MGIyNWExNDZl
NTgwYWJmJywgJ2NmMDA0ZDUxN2QyZWZlOTFhMDJjOTJhNThlM2RmNmJmJwpFTEVDVElPTlMgPSB7
J0UtU0EtMCc6ICdhJywgJ0UtU0EtMSc6ICdhJywgJ0UtU0EtMic6ICdhJywgJ0UtU0EtMyc6ICdh
JywgJ0UtU0EtNCc6ICdhJywgJ0UtU0EtNSc6ICdhJywgJ0UtU0EtNic6ICdhJywKICAgICAgICAg
ICAgICdFLVNBLTcnOiAnMDUzMDIyMTArTVNDUzFzdHJhdHVtJywgJ0UtU0EtOCc6ICdhJywgJ0Ut
U0EtOSc6ICdhJywgJ0UtU0EtMTAnOiAnYScsICdFLVNBLTExJzogJ2EnfQpGSUxFUyA9IHsnbWVt
byc6ICdzdGFnaW5nX21lbW9fR19NU0NTX0FfdjIubWQnLCAncGluJzogJ3Bpbm5lZF9pbnB1dHNf
R19NU0NTX0EuanNvbicsICdsb2NrJzogJ0dfTVNDU19BX0xPQ0tfUkVDT1JELm1kJywKICAgICAg
ICAgJ3NjaGVtYSc6ICdnX21zY3NfYV9zY2hlbWFfdjFfMC5qc29uJywgJ2NvbXBhcmF0b3InOiAn
Z19tc2NzX2FfY29tcGFyZV92MV8wLnB5JywKICAgICAgICAgJ3QxJzogJ3Rvb2xzL3QxL1QxX2Zv
cmJpZGRlbl9HX01TQ1NfQS50eHQnLCAnYmFzZSc6ICd0b29scy90MS9UMV9iYXNlX2F1dGhvcl8y
MDI2MDkxOS50eHQnLCAnc2Nhbm5lcic6ICd0b29scy90MS90MV9zY2FuLnB5J30KUkVRVUlSRUQg
PSBbJ2lkJywgJ2NsYXNzJywgJ2RlbHRhX2RlZicsICdsbycsICdoaScsICdjbCcsICdyZWFkaW5n
JywgJ2dlb20nLCAna19lbV9tYXgnLCAna190X21heCcsICdzcmMnXQpPUFRJT05BTCA9IFsncScs
ICdub3RlJ10KQ0FOT04gPSBSRVFVSVJFRCArIE9QVElPTkFMCk5VTSA9IHJlLmNvbXBpbGUocide
WystXT8oPzpcZCtcLj9cZCp8XC5cZCspKD86W2VFXVsrLV0/XGQrKT8kJykKU0VQID0gJyB8ICcK
QkFEX1VOSUNPREUgPSB7J1x1MDA4NScsICfigKgnLCAn4oCpJywgJ++7vyd9CkxPRyA9IFtdClNF
QUxFRF9PUEVOUyA9IDAKCgpkZWYgc2F5KHMpOgogICAgTE9HLmFwcGVuZChzKQogICAgcHJpbnQo
cykKCgpkZWYgbWQ1YihiKToKICAgIHJldHVybiBoYXNobGliLm1kNShiKS5oZXhkaWdlc3QoKQoK
CmRlZiBtZDVmKHApOgogICAgcmV0dXJuIG1kNWIob3BlbihwLCAncmInKS5yZWFkKCkpCgoKY2xh
c3MgSGFsdChFeGNlcHRpb24pOgogICAgcGFzcwoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tIGd1YXJkcyBhbmQgVDEKZGVmIGd1YXJkcygpOgogICAgcGF0aHMgPSB7azogb3Mu
cGF0aC5qb2luKEhFUkUsIHYpIGZvciBrLCB2IGluIEZJTEVTLml0ZW1zKCl9CiAgICB3YW50ID0g
eydtZW1vJzogTUVNT19NRDUsICdwaW4nOiBQSU5fTUQ1LCAndDEnOiBUMV9NRDUsICdiYXNlJzog
QkFTRV9NRDUsICdzY2FubmVyJzogU0NBTk5FUl9NRDUsICdzY2hlbWEnOiBTQ0hFTUFfTUQ1LAog
ICAgICAgICAgICAnY29tcGFyYXRvcic6IENPTVBBUkFUT1JfTUQ1LCAnbG9jayc6IExPQ0tfTUQ1
fQogICAgZm9yIGssIG0gaW4gd2FudC5pdGVtcygpOgogICAgICAgIGggPSBtZDVmKHBhdGhzW2td
KQogICAgICAgIGlmIGggIT0gbToKICAgICAgICAgICAgcmFpc2UgSGFsdCgnZ3VhcmQ6ICVzIG1k
NSAlcyAhPSAlcycgJSAoRklMRVNba10sIGgsIG0pKQogICAgaWYgb3MucGF0aC5nZXRzaXplKHBh
dGhzWydtZW1vJ10pICE9IE1FTU9fQllURVMgb3Igb3MucGF0aC5nZXRzaXplKHBhdGhzWydwaW4n
XSkgIT0gUElOX0JZVEVTOgogICAgICAgIHJhaXNlIEhhbHQoJ2d1YXJkOiBieXRlIGNvdW50JykK
ICAgIHJldHVybiBwYXRocwoKCmRlZiBsb2FkX3NjYW5uZXIocGF0aHMpOgogICAgc3BlYyA9IGlt
cG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCd0MV9zY2FuJywgcGF0aHNbJ3Nj
YW5uZXInXSkKICAgIG0gPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMpCiAg
ICBzcGVjLmxvYWRlci5leGVjX21vZHVsZShtKQogICAgcmV0dXJuIG0KCgpkZWYgdDFfc2Nhbihw
YXRocywgdGFyZ2V0cywgYTEpOgogICAgbSA9IGxvYWRfc2Nhbm5lcihwYXRocykKICAgIHBhdHMg
PSBtLmxvYWQocGF0aHNbJ3QxJ10pCiAgICBpZiBhMToKICAgICAgICBwYXRzID0gcGF0cyArIG0u
bG9hZChhMSkKICAgIGhpdHMsIGNvbGwgPSAwLCAwCiAgICBwZXIgPSB7fQogICAgZm9yIHQgaW4g
dGFyZ2V0czoKICAgICAgICB0ZXh0ID0gb3Blbih0LCBlbmNvZGluZz0ndXRmLTgnKS5yZWFkKCkK
ICAgICAgICBoLCBjID0gbS5zY2FuX3RleHQodGV4dCwgcGF0cykKICAgICAgICBoaXRzICs9IGxl
bihoKTsgY29sbCArPSBsZW4oYykKICAgICAgICBwZXJbb3MucGF0aC5iYXNlbmFtZSh0KV0gPSB7
J2hpdHNfYnlfaW5kZXgnOiBzb3J0ZWQoe2kgZm9yIGksIF8gaW4gaH0pLCAnY29sbGlzaW9ucyc6
IGxlbihjKX0KICAgIHJldHVybiB7J2hpdHMnOiBoaXRzLCAnY29sbGlzaW9ucyc6IGNvbGwsICdw
YXR0ZXJucyc6IGxlbihwYXRzKSwgJ2ExX2luY2x1ZGVkJzogYm9vbChhMSksICdwZXJfZmlsZSc6
IHBlcn0KCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBwaW5uZWQgaW5wdXRz
LCBvd24gcmUtZGVyaXZhdGlvbgpkZWYgcHRyKGRvYywgcG9pbnRlcik6CiAgICBub2RlID0gZG9j
CiAgICBmb3IgcGFydCBpbiBwb2ludGVyLmxzdHJpcCgnLycpLnNwbGl0KCcvJyk6CiAgICAgICAg
cGFydCA9IHBhcnQucmVwbGFjZSgnfjEnLCAnLycpLnJlcGxhY2UoJ34wJywgJ34nKQogICAgICAg
IG5vZGUgPSBub2RlW2ludChwYXJ0KV0gaWYgaXNpbnN0YW5jZShub2RlLCBsaXN0KSBlbHNlIG5v
ZGVbcGFydF0KICAgIHJldHVybiBub2RlCgoKZGVmIGZsYXQobm9kZSwgcHJlZml4PScnKToKICAg
IG91dCA9IHt9CiAgICBpZiBpc2luc3RhbmNlKG5vZGUsIGRpY3QpOgogICAgICAgIGZvciBrLCB2
IGluIG5vZGUuaXRlbXMoKToKICAgICAgICAgICAgb3V0LnVwZGF0ZShmbGF0KHYsIChwcmVmaXgg
KyAnLycgKyBrKSBpZiBwcmVmaXggZWxzZSBrKSkKICAgIGVsaWYgaXNpbnN0YW5jZShub2RlLCBs
aXN0KToKICAgICAgICBmb3IgaSwgdiBpbiBlbnVtZXJhdGUobm9kZSk6CiAgICAgICAgICAgIG91
dC51cGRhdGUoZmxhdCh2LCAnJXNbJWRdJyAlIChwcmVmaXgsIGkpKSkKICAgIGVsc2U6CiAgICAg
ICAgb3V0W3ByZWZpeF0gPSBub2RlCiAgICByZXR1cm4gb3V0CgoKZGVmIHJlZGVyaXZlKFApOgog
ICAgIiIidGhlIGNoYXQgbGVnJ3Mgb3duIHJlLWRlcml2YXRpb24gb2YgZGVyaXZlZC57ZmFtaWxp
ZXMscmVhY2gsdW5pb25zLHN5bnRoZXRpYyxudWxscyxoZXhfcXVhZGZvcm0semVyb19jdHJsfSIi
IgogICAgcmF3LCBDLCBHID0gUFsncmF3J10sIFBbJ2NvbnN0YW50cyddLCBQWydncmlkcyddCiAg
ICBLRVlTLCBIRVgsIENVQiwgQVJNUywgUFJJTSA9IFBbJ3N0cnVjdHVyZSddWydrZXlzJ10sIFBb
J3N0cnVjdHVyZSddWydoZXhfa2V5cyddLCBQWydzdHJ1Y3R1cmUnXVsnY3ViaWNfa2V5cyddLCBQ
WydzdHJ1Y3R1cmUnXVsnYXJtcyddLCBQWydzdHJ1Y3R1cmUnXVsncHJpbWFyeSddWydrZXlzJ10K
ICAgIEQsIE1VLCBTTkFQLCBLRiA9IENbJ0QnXSwgQ1snbXUnXSwgQ1snemVyb19zbmFwJ10sIENb
J2thcHBhX2Zsb29yJ10KICAgIFQsIEFYID0gR1sndF9ncmlkJ10sIEdbJ3QydDRfYXhpcyddCiAg
ICAoaDEsIGgyKSwgKGcxLCBnMikgPSBHWydyaWNoYXJkc29uX3BhaXJzJ11bJ29uZV9wYXJhbSdd
LCBHWydyaWNoYXJkc29uX3BhaXJzJ11bJ3R3b19wYXJhbSddCiAgICBpbnNpZGUgPSBbaSBmb3Ig
aSwgdCBpbiBlbnVtZXJhdGUoVCkgaWYgLUQgPD0gdCA8PSBEXQogICAgdmFsID0gbGFtYmRhIGcs
IHQ6IGdbVC5pbmRleCh0KV0KICAgIGV2ZW4gPSBsYW1iZGEgZzogKDQgKiAoKHZhbChnLCBoMSkg
KyB2YWwoZywgLWgxKSAtIDIgKiB2YWwoZywgMC4wKSkgLyAoMiAqIGgxICogaDEpKSAtICgodmFs
KGcsIGgyKSArIHZhbChnLCAtaDIpIC0gMiAqIHZhbChnLCAwLjApKSAvICgyICogaDIgKiBoMikp
KSAvIDMKICAgIG9kZCA9IGxhbWJkYSBnOiAoNCAqICgodmFsKGcsIGgxKSAtIHZhbChnLCAtaDEp
KSAvICgyICogaDEpKSAtICgodmFsKGcsIGgyKSAtIHZhbChnLCAtaDIpKSAvICgyICogaDIpKSkg
LyAzCiAgICBkZWYgZ3JpZDUodik6CiAgICAgICAgbiA9IGxlbihBWCkKICAgICAgICByZXR1cm4g
eyhBWFtpXSwgQVhbal0pOiB2W24gKiBpICsgal0gZm9yIGkgaW4gcmFuZ2UobikgZm9yIGogaW4g
cmFuZ2Uobil9CiAgICBkZWYgcmljaDUoUiwga2luZCk6CiAgICAgICAgZGVmIGYoaCk6CiAgICAg
ICAgICAgIGlmIGtpbmQgPT0gJzIyJzogcmV0dXJuIChSWyhoLCAwLjApXSArIFJbKC1oLCAwLjAp
XSAtIDIgKiBSWygwLjAsIDAuMCldKSAvICgyICogaCAqIGgpCiAgICAgICAgICAgIGlmIGtpbmQg
PT0gJzQ0JzogcmV0dXJuIChSWygwLjAsIGgpXSArIFJbKDAuMCwgLWgpXSAtIDIgKiBSWygwLjAs
IDAuMCldKSAvICgyICogaCAqIGgpCiAgICAgICAgICAgIHJldHVybiAoUlsoaCwgaCldIC0gUlso
aCwgLWgpXSAtIFJbKC1oLCBoKV0gKyBSWygtaCwgLWgpXSkgLyAoNCAqIGggKiBoKQogICAgICAg
IHJldHVybiAoNCAqIGYoZzEpIC0gZihnMikpIC8gMwogICAgcmVsID0gbGFtYmRhIHgsIHk6IGFi
cyh4IC0geSkgLyBtYXgoYWJzKHgpLCBhYnMoeSkpCiAgICB0b2sgPSBsYW1iZGEgaywgZjogKCdo
ZXhQMicgaWYgayBpbiBIRVggZWxzZSAnY3ViUDItaScpIGlmIGYgPT0gJ3QyJyBlbHNlICgnaGV4
UDQnIGlmIGsgaW4gSEVYIGVsc2UgJ2N1Yks0JykKICAgIGZhbSwgcmVhY2gsIHplcm8sIG4xLCBu
MiwgbjMsIG40LCBocSA9IHt9LCB7fSwge30sIHt9LCB7fSwge30sIHt9LCB7fQogICAgZm9yIGsg
aW4gS0VZUzoKICAgICAgICByayA9IHJhd1sna2V5cyddW2tdCiAgICAgICAgbWFwcGVkID0gKCd0
NCcsICd0MicpIGlmIGsgaW4gSEVYIGVsc2UgKCd0NCcsKQogICAgICAgIGZhbVtrXSwgcmVhY2hb
a10sIHplcm9ba10gPSB7fSwge30sIHt9CiAgICAgICAgZm9yIGFybSBpbiBBUk1TOgogICAgICAg
ICAgICBmYW1ba11bYXJtXSA9IHt9CiAgICAgICAgICAgIGZvciBmIGluICgndDQnLCAndDInKToK
ICAgICAgICAgICAgICAgIGQgPSBya1snYXJtcyddW2FybV1bZl0KICAgICAgICAgICAgICAgIGti
ID0gZXZlbihkWydncmlkJ10pCiAgICAgICAgICAgICAgICBlID0geydvZGZfcmVhZGluZyc6IHRv
ayhrLCBmKSwgJ2thcHBhJzogZFsna2FwcGEnXSwgJ2thcHBhX2JpJzoga2IsICdmaXRfcmVzX3Jl
bCc6IChhYnMoZFsna2FwcGEnXSAtIGtiKSAvIGFicyhrYikpIGlmIGFicyhrYikgPiBLRiBlbHNl
IE5vbmUsCiAgICAgICAgICAgICAgICAgICAgICdTX2JpJzogb2RkKGRbJ2dyaWQnXSksICdTX2Zp
dCc6IGQuZ2V0KCdTJyksICdyMCc6IHZhbChkWydncmlkJ10sIDAuMCksICdtYXBwZWQnOiBmIGlu
IG1hcHBlZH0KICAgICAgICAgICAgICAgIGlmIGYgaW4gbWFwcGVkIGFuZCAna2FwcGEzJyBpbiBk
OgogICAgICAgICAgICAgICAgICAgIGVbJ3JlY29uX21heF9hYnMnXSA9IG1heChhYnMoZFsnZ3Jp
ZCddW2ldIC0gKGRbJ1MnXSAqIFRbaV0gKyBkWydrYXBwYSddICogVFtpXSAqKiAyICsgZFsna2Fw
cGEzJ10gKiBUW2ldICoqIDMpKSBmb3IgaSBpbiBpbnNpZGUpCiAgICAgICAgICAgICAgICAgICAg
ZVsndHJ1bmNfVF9hdF9EJ10gPSBhYnMoZFsna2FwcGEzJ10pICogRCAvIGFicyhkWydrYXBwYSdd
KQogICAgICAgICAgICAgICAgaWYgJ2thcHBhX2NjJyBpbiBkOgogICAgICAgICAgICAgICAgICAg
IGVbJ3R3b2xlZ19yZWwnXSA9IHJlbChkWydrYXBwYSddLCBkWydrYXBwYV9jYyddKSBpZiBtYXgo
YWJzKGRbJ2thcHBhJ10pLCBhYnMoZFsna2FwcGFfY2MnXSkpID4gS0YgZWxzZSBOb25lCiAgICAg
ICAgICAgICAgICBpZiAna2FwcGEzX2NjJyBpbiBkOgogICAgICAgICAgICAgICAgICAgIGVbJ3R3
b2xlZ19rYXBwYTNfcmVsJ10gPSByZWwoZFsna2FwcGEzJ10sIGRbJ2thcHBhM19jYyddKSBpZiBm
IGluIG1hcHBlZCBlbHNlIE5vbmUKICAgICAgICAgICAgICAgIGlmICdTX2NjJyBpbiBkOgogICAg
ICAgICAgICAgICAgICAgIGVbJ3R3b2xlZ19TX2FicyddID0gYWJzKGRbJ1MnXSAtIGRbJ1NfY2Mn
XSkKICAgICAgICAgICAgICAgIGZhbVtrXVthcm1dW2ZdID0gZQogICAgICAgICAgICAgICAgemVy
b1trXVthcm0gKyAnLycgKyBmXSA9IHsnb2RmX3JlYWRpbmcnOiAndW5pZm9ybScsICdyMCc6IGVb
J3IwJ119CiAgICAgICAgICAgICAgICBpZiBmIGluIG1hcHBlZDoKICAgICAgICAgICAgICAgICAg
ICBuMVsnJXMvJXMvJXMnICUgKGssIGFybSwgZildID0geydvZGZfcmVhZGluZyc6IHRvayhrLCBm
KSwgJ2ZpdCc6IGVbJ1NfZml0J10sICdiaSc6IGVbJ1NfYmknXX0KICAgICAgICAgICAgbG8gPSBz
dW0obWluKDAuMCwgcmtbJ2FybXMnXVthcm1dW2ZtXVsna2FwcGEnXSAqIEQgKiBEKSBmb3IgZm0g
aW4gbWFwcGVkKQogICAgICAgICAgICBoaSA9IHN1bShtYXgoMC4wLCBya1snYXJtcyddW2FybV1b
Zm1dWydrYXBwYSddICogRCAqIEQpIGZvciBmbSBpbiBtYXBwZWQpCiAgICAgICAgICAgIHB0cyA9
IFtya1snYXJtcyddW2FybV1bZm1dWydncmlkJ11baV0gZm9yIGZtIGluIG1hcHBlZCBmb3IgaSBp
biBpbnNpZGVdCiAgICAgICAgICAgIGlmIGFybSA9PSAnRTJfSGlsbCc6CiAgICAgICAgICAgICAg
ICBwdHMgPSBwdHMgKyBya1sncXVhZGZvcm0nXVsnZ3JpZDV4NV9jYyddCiAgICAgICAgICAgIGh1
bGwgPSBbMC4wIGlmIGFicyh4KSA8IFNOQVAgZWxzZSB4IGZvciB4IGluIChtaW4obG8sIG1pbihw
dHMpKSwgbWF4KGhpLCBtYXgocHRzKSkpXQogICAgICAgICAgICByZWFjaFtrXVthcm1dID0geydi
b3gnOiBbbG8sIGhpXSwgJ2dyaWRfbWluJzogbWluKHB0cyksICdncmlkX21heCc6IG1heChwdHMp
LCAnaHVsbCc6IGh1bGwsICd3aWRlbmVkJzogW3ggKiAoMSArIE1VKSBmb3IgeCBpbiBodWxsXSwK
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnZ3JpZF9leGNlZWRzX2JveCc6IG1pbihwdHMp
IDwgbG8gb3IgbWF4KHB0cykgPiBoaX0KICAgICAgICBSID0gZ3JpZDUocmtbJ3F1YWRmb3JtJ11b
J2dyaWQ1eDVfY2MnXSkKICAgICAgICBuMltrXSA9IHsnb2RmX3JlYWRpbmcnOiAnaGV4UDJQNCcg
aWYgayBpbiBIRVggZWxzZSAnY3ViUDJLNC1pJywgJ2ZpdDcnOiBya1sncXVhZGZvcm0nXVsna2Fw
cGEyNF9maXQ3J10sICdiaV9jaGF0JzogcmtbJ2thcHBhMjRfYmlfY2hhdCddLAogICAgICAgICAg
ICAgICAgICdiaV9jYyc6IHJrWydrYXBwYTI0X2JpX2NjJ10sICdiaV81eDUnOiByaWNoNShSLCAn
MjQnKX0KICAgICAgICBpZiBrIGluIENVQjoKICAgICAgICAgICAgbjNba10gPSB7J29kZl9yZWFk
aW5nJzogJ2N1YlAyLWknLCAnZml0JzogcmtbJ2FybXMnXVsnRTJfSGlsbCddWyd0MiddWydrYXBw
YSddLCAnYmknOiBldmVuKHJrWydhcm1zJ11bJ0UyX0hpbGwnXVsndDInXVsnZ3JpZCddKSwgJ3B1
cmVfbDJfY2hhbmdlX3QxJzogcmtbJ3B1cmVfbDJfY2hhbmdlX3QxJ119CiAgICAgICAgICAgIGsx
MiA9IHJrWydxdWFkZm9ybSddLmdldCgnYmFzaXNfazEyX2NoYXQnKQogICAgICAgICAgICBuNFtr
XSA9IHsnb2RmX3JlYWRpbmcnOiAnY3ViUDJLNC1pJywgJ2ZpdDcnOiBya1sncXVhZGZvcm0nXVsn
a2FwcGEyMl9maXQ3J10sICdiaV81eDUnOiByaWNoNShSLCAnMjInKSwgJ2sxMl9jaGF0X3Qyc3En
OiBrMTJbMF0gaWYgazEyIGlzIG5vdCBOb25lIGVsc2UgTm9uZX0KICAgICAgICBlbHNlOgogICAg
ICAgICAgICBBID0gcmtbJ2FybXMnXQogICAgICAgICAgICBxMjIsIHE0NCwgcTI0ID0gcmljaDUo
UiwgJzIyJyksIHJpY2g1KFIsICc0NCcpLCByaWNoNShSLCAnMjQnKQogICAgICAgICAgICBocVtr
XSA9IHsnazIyX2JpXzV4NSc6IHEyMiwgJ2s0NF9iaV81eDUnOiBxNDQsICdrMjRfYmlfNXg1Jzog
cTI0LAogICAgICAgICAgICAgICAgICAgICAnbnVsbF9yYXlfc2xvcGUnOiB7J0UyX0hpbGxfYmk1
eDUnOiBtYXRoLnNxcnQoLXEyMiAvIHE0NCksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAnRTJfSGlsbF9iaSc6IG1hdGguc3FydCgtZXZlbihBWydFMl9IaWxsJ11bJ3Qy
J11bJ2dyaWQnXSkgLyBldmVuKEFbJ0UyX0hpbGwnXVsndDQnXVsnZ3JpZCddKSksCiAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnRTJfSGlsbF9maXQnOiBtYXRoLnNxcnQo
LUFbJ0UyX0hpbGwnXVsndDInXVsna2FwcGEnXSAvIEFbJ0UyX0hpbGwnXVsndDQnXVsna2FwcGEn
XSksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnRTJfSFNtZWFuX2Jp
JzogbWF0aC5zcXJ0KC1ldmVuKEFbJ0UyX0hTbWVhbiddWyd0MiddWydncmlkJ10pIC8gZXZlbihB
WydFMl9IU21lYW4nXVsndDQnXVsnZ3JpZCddKSksCiAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAnRTJfSFNtZWFuX2ZpdCc6IG1hdGguc3FydCgtQVsnRTJfSFNtZWFuJ11b
J3QyJ11bJ2thcHBhJ10gLyBBWydFMl9IU21lYW4nXVsndDQnXVsna2FwcGEnXSl9LAogICAgICAg
ICAgICAgICAgICAgICAnaF9IaWxsX2Zvcm0nOiAnbmVnYXRpdmUtZGVmaW5pdGUnIGlmIChBWydo
X0hpbGwnXVsndDInXVsna2FwcGEnXSA8IDAgYW5kIEFbJ2hfSGlsbCddWyd0NCddWydrYXBwYSdd
IDwgMCkgZWxzZSAnbm90IG5lZ2F0aXZlLWRlZmluaXRlJywKICAgICAgICAgICAgICAgICAgICAg
J2thcHBhMjJfZml0N192c19rYXBwYTJfcmVsJzogcmVsKHJrWydxdWFkZm9ybSddWydrYXBwYTIy
X2ZpdDcnXSwgQVsnRTJfSGlsbCddWyd0MiddWydrYXBwYSddKX0KICAgIGNlbGxzID0gWyhrLCBh
KSBmb3IgayBpbiBLRVlTIGZvciBhIGluIEFSTVNdCiAgICB1biA9IHsnaHVsbF9hbGwnOiBbbWlu
KHJlYWNoW2tdW2FdWydodWxsJ11bMF0gZm9yIGssIGEgaW4gY2VsbHMpLCBtYXgocmVhY2hba11b
YV1bJ2h1bGwnXVsxXSBmb3IgaywgYSBpbiBjZWxscyldLAogICAgICAgICAgJ3dpZGVuZWRfYWxs
JzogW21pbihyZWFjaFtrXVthXVsnd2lkZW5lZCddWzBdIGZvciBrLCBhIGluIGNlbGxzKSwgbWF4
KHJlYWNoW2tdW2FdWyd3aWRlbmVkJ11bMV0gZm9yIGssIGEgaW4gY2VsbHMpXSwKICAgICAgICAg
ICdodWxsX3ByaW1hcnknOiBbbWluKHJlYWNoW2tdWydFMl9IaWxsJ11bJ2h1bGwnXVswXSBmb3Ig
ayBpbiBQUklNKSwgbWF4KHJlYWNoW2tdWydFMl9IaWxsJ11bJ2h1bGwnXVsxXSBmb3IgayBpbiBQ
UklNKV0sCiAgICAgICAgICAnd2lkZW5lZF9wcmltYXJ5JzogW21pbihyZWFjaFtrXVsnRTJfSGls
bCddWyd3aWRlbmVkJ11bMF0gZm9yIGsgaW4gUFJJTSksIG1heChyZWFjaFtrXVsnRTJfSGlsbCdd
Wyd3aWRlbmVkJ11bMV0gZm9yIGsgaW4gUFJJTSldfQogICAgZjEsIGYyID0gQ1snc3ludGhldGlj
X2JhbmRfZnJhY3Rpb25zJ10KICAgIGl2ID0gbGFtYmRhIGEsIGI6IFthICsgZjEgKiAoYiAtIGEp
LCBhICsgZjIgKiAoYiAtIGEpXQogICAgc3luID0geydtYXJnaW5fcG9zaXRpdmUnOiBpdih1blsn
aHVsbF9hbGwnXVsxXSwgdW5bJ3dpZGVuZWRfYWxsJ11bMV0pLCAnbWFyZ2luX25lZ2F0aXZlJzog
aXYodW5bJ3dpZGVuZWRfYWxsJ11bMF0sIHVuWydodWxsX2FsbCddWzBdKSwKICAgICAgICAgICAn
cm9idXN0bmVzc19vbmx5X3Bvc2l0aXZlJzogaXYodW5bJ3dpZGVuZWRfcHJpbWFyeSddWzFdLCB1
blsnaHVsbF9hbGwnXVsxXSl9CiAgICByZXR1cm4geydmYW1pbGllcyc6IGZhbSwgJ3JlYWNoJzog
cmVhY2gsICd1bmlvbnMnOiB1biwgJ3N5bnRoZXRpYyc6IHN5biwgJ3plcm9fY3RybCc6IHplcm8s
CiAgICAgICAgICAgICdudWxscyc6IHsnTi0xJzogbjEsICdOLTInOiBuMiwgJ04tMyc6IG4zLCAn
Ti00JzogbjR9LCAnaGV4X3F1YWRmb3JtJzogaHF9CgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0gdGhlIG1hcHBpbmcgKEEtMi40KQpSTVMgPSB7KCdoZXgnLCAndDQnKTogMS4w
IC8gMy4wLCAoJ2N1YmljJywgJ3Q0Jyk6IG1hdGguc3FydCg0LjAgLyAyMS4wKSwgKCdoZXgnLCAn
dDInKTogbWF0aC5zcXJ0KDEuMCAvIDUuMCksICgnY3ViaWMnLCAndDInKTogbWF0aC5zcXJ0KDEu
MCAvIDUuMCl9CgoKY2xhc3MgTWFwcGVyOgogICAgZGVmIF9faW5pdF9fKHNlbGYsIFAsIERWKToK
ICAgICAgICBzZWxmLlAsIHNlbGYuRFYgPSBQLCBEVgogICAgICAgIFMgPSBQWydzdHJ1Y3R1cmUn
XQogICAgICAgIHNlbGYuS0VZUywgc2VsZi5IRVgsIHNlbGYuQVJNUywgc2VsZi5QUklNID0gU1sn
a2V5cyddLCBTWydoZXhfa2V5cyddLCBTWydhcm1zJ10sIFNbJ3ByaW1hcnknXVsna2V5cyddCiAg
ICAgICAgc2VsZi5ELCBzZWxmLktELCBzZWxmLmRFTSA9IFBbJ2NvbnN0YW50cyddWydEJ10sIFBb
J2NvbnN0YW50cyddWydLRF9DTElQJ10sIFBbJ3JhdyddWydyZWdpbWUnXVsnZF9FTSddCiAgICAg
ICAgc2VsZi5UUiwgc2VsZi5ORiA9IFBbJ2NvbnN0YW50cyddWyd0cnVuY190aHJlc2hvbGQnXSwg
UFsnY29uc3RhbnRzJ11bJ251bGxmbG9vcl90aHJlc2hvbGQnXQogICAgICAgIHNlbGYuTk9ERVMg
PSBQWydncmlkcyddWydhcmVhX2dyaWQnXVsnbm9kZXNfcGVyX2F4aXMnXQogICAgICAgIHNlbGYu
cmVhY2ggPSBEVlsncmVhY2gnXQoKICAgIGRlZiBtYXBwZWQoc2VsZiwgayk6CiAgICAgICAgcmV0
dXJuICgndDQnLCAndDInKSBpZiBrIGluIHNlbGYuSEVYIGVsc2UgKCd0NCcsKQoKICAgIGRlZiBm
YW1fd2luZG93KHNlbGYsIGssIGFybSwgZiwgbG8sIGhpKToKICAgICAgICBkID0gc2VsZi5QWydy
YXcnXVsna2V5cyddW2tdWydhcm1zJ11bYXJtXVtmXQogICAgICAgIGUgPSBzZWxmLkRWWydmYW1p
bGllcyddW2tdW2FybV1bZl0KICAgICAgICBEID0gc2VsZi5ECiAgICAgICAgaWYgZiA9PSAndDIn
IGFuZCBrIG5vdCBpbiBzZWxmLkhFWDoKICAgICAgICAgICAgcmV0dXJuIHsnY2xhc3MnOiAnTlVM
TC1JTkVSVCcsICdiaW5kaW5nX2VuZCc6IE5vbmUsICd0X3N0YXInOiBOb25lLCAndF9zdGFyX2Jp
JzogTm9uZSwgJ2NsYXNzX2JpJzogTm9uZSwgJ3Jlc29sdXRpb25fc2Vuc2l0aXZlJzogRmFsc2Us
CiAgICAgICAgICAgICAgICAgICAgJ3NpZ21hX3N0YXInOiBOb25lLCAnd2luZG93X2xvJzogLUQs
ICd3aW5kb3dfaGknOiBELCAndHJ1bmNfVCc6IE5vbmUsICd0cnVuY2F0aW9uX3NlbnNpdGl2ZSc6
IEZhbHNlLCAnbnUnOiBOb25lLCAnbnVfaXNfaW5mJzogRmFsc2UsICdudWxsZmxvb3Jfc2Vuc2l0
aXZlJzogRmFsc2V9CiAgICAgICAgZGVmIGVkZ2Uoa2FwcGEpOgogICAgICAgICAgICBiID0gaGkg
aWYga2FwcGEgPiAwIGVsc2UgbG8KICAgICAgICAgICAgdHMgPSBtYXRoLnNxcnQoYiAvIGthcHBh
KSBpZiBiICE9IDAgZWxzZSAwLjAKICAgICAgICAgICAgcmV0dXJuIGIsIHRzLCAoJ0JJTkRJTkcn
IGlmIHRzIDwgRCBlbHNlICdJTkVSVC1JTi1EJykKICAgICAgICBiLCB0cywgY2xzID0gZWRnZShk
WydrYXBwYSddKQogICAgICAgIF8sIHRzX2JpLCBjbHNfYmkgPSBlZGdlKGVbJ2thcHBhX2JpJ10p
CiAgICAgICAgdyA9IG1pbih0cywgRCkKICAgICAgICBvdXQgPSB7J2NsYXNzJzogY2xzLCAnYmlu
ZGluZ19lbmQnOiAnaGknIGlmIGRbJ2thcHBhJ10gPiAwIGVsc2UgJ2xvJywgJ3Rfc3Rhcic6IHRz
LCAndF9zdGFyX2JpJzogdHNfYmksICdjbGFzc19iaSc6IGNsc19iaSwKICAgICAgICAgICAgICAg
J3Jlc29sdXRpb25fc2Vuc2l0aXZlJzogY2xzICE9IGNsc19iaSwgJ3NpZ21hX3N0YXInOiB0cyAq
IFJNU1soJ2hleCcgaWYgayBpbiBzZWxmLkhFWCBlbHNlICdjdWJpYycsIGYpXSwgJ3dpbmRvd19s
byc6IC13LCAnd2luZG93X2hpJzogd30KICAgICAgICBpZiBhcm0gPT0gJ0UyX0hpbGwnOgogICAg
ICAgICAgICBUID0gYWJzKGRbJ2thcHBhMyddKSAqIHRzIC8gYWJzKGRbJ2thcHBhJ10pCiAgICAg
ICAgICAgIG91dFsndHJ1bmNfVCddLCBvdXRbJ3RydW5jYXRpb25fc2Vuc2l0aXZlJ10gPSBULCBU
ID4gc2VsZi5UUgogICAgICAgIGVsc2U6CiAgICAgICAgICAgIG91dFsndHJ1bmNfVCddLCBvdXRb
J3RydW5jYXRpb25fc2Vuc2l0aXZlJ10gPSBOb25lLCBGYWxzZQogICAgICAgIGlmIGIgPT0gMDoK
ICAgICAgICAgICAgb3V0WydudSddLCBvdXRbJ251X2lzX2luZiddLCBvdXRbJ251bGxmbG9vcl9z
ZW5zaXRpdmUnXSA9IE5vbmUsIFRydWUsIFRydWUKICAgICAgICBlbHNlOgogICAgICAgICAgICBu
dSA9IGFicyhlWydTX2JpJ10pICogdHMgLyBhYnMoYikKICAgICAgICAgICAgb3V0WydudSddLCBv
dXRbJ251X2lzX2luZiddLCBvdXRbJ251bGxmbG9vcl9zZW5zaXRpdmUnXSA9IG51LCBGYWxzZSwg
bnUgPiBzZWxmLk5GCiAgICAgICAgcmV0dXJuIG91dAoKICAgIGRlZiBleGNsdXNpb24oc2VsZiwg
aywgYXJtLCBsbywgaGkpOgogICAgICAgIHJ3LCByaCA9IHNlbGYucmVhY2hba11bYXJtXVsnd2lk
ZW5lZCddLCBzZWxmLnJlYWNoW2tdW2FybV1bJ2h1bGwnXQogICAgICAgIGludGVyID0gbGFtYmRh
IFI6IG1heChsbywgUlswXSkgPD0gbWluKGhpLCBSWzFdKQogICAgICAgIGlmIG5vdCBpbnRlcihy
dyk6CiAgICAgICAgICAgIGNscyA9ICdFWENMVURFRC1JTi1EJwogICAgICAgICAgICBzdWIgPSAn
U0lHTicgaWYgKChoaSA8IDAgYW5kIHJ3WzBdID49IDApIG9yIChsbyA+IDAgYW5kIHJ3WzFdIDw9
IDApKSBlbHNlICdNQUdOSVRVREUnCiAgICAgICAgZWxpZiBpbnRlcihyaCk6CiAgICAgICAgICAg
IGNscywgc3ViID0gJ1RVTkVELUFETUlTU0lCTEUnLCBOb25lCiAgICAgICAgZWxzZToKICAgICAg
ICAgICAgY2xzLCBzdWIgPSAnTUFSR0lOJywgTm9uZQogICAgICAgIHJlcSA9IHt9CiAgICAgICAg
Zm9yIGYgaW4gc2VsZi5tYXBwZWQoayk6CiAgICAgICAgICAgIGthcHBhID0gc2VsZi5QWydyYXcn
XVsna2V5cyddW2tdWydhcm1zJ11bYXJtXVtmXVsna2FwcGEnXQogICAgICAgICAgICBpZiAoa2Fw
cGEgPiAwKSA9PSAobG8gPiAwKToKICAgICAgICAgICAgICAgIHRfaW4sIHRfb3V0ID0gbWF0aC5z
cXJ0KG1pbihhYnMobG8pLCBhYnMoaGkpKSAvIGFicyhrYXBwYSkpLCBtYXRoLnNxcnQobWF4KGFi
cyhsbyksIGFicyhoaSkpIC8gYWJzKGthcHBhKSkKICAgICAgICAgICAgICAgIHJlcVtmXSA9IHsn
dF9pbic6IHRfaW4sICd0X291dCc6IHRfb3V0LCAnY2FuX3N1cHBseV9hbG9uZSc6IHRfaW4gPD0g
c2VsZi5EfQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmVxW2ZdID0geyd0X2lu
JzogTm9uZSwgJ3Rfb3V0JzogTm9uZSwgJ2Nhbl9zdXBwbHlfYWxvbmUnOiBGYWxzZX0KICAgICAg
ICByZXR1cm4geydjbGFzcyc6IGNscywgJ3N1YnJlYXNvbic6IHN1YiwgJ3JlcXVpcmVtZW50cyc6
IHJlcX0KCiAgICBkZWYgdHdvX3BhcmFtKHNlbGYsIGssIGFybSwgbG8sIGhpKToKICAgICAgICBh
ID0gc2VsZi5QWydyYXcnXVsna2V5cyddW2tdWydhcm1zJ11bYXJtXQogICAgICAgIGsyLCBrNCA9
IGFbJ3QyJ11bJ2thcHBhJ10sIGFbJ3Q0J11bJ2thcHBhJ10KICAgICAgICBuLCBEID0gc2VsZi5O
T0RFUywgc2VsZi5ECiAgICAgICAgbm9kZSA9IFstRCArIGkgKiAoMiAqIEQpIC8gKG4gLSAxKSBm
b3IgaSBpbiByYW5nZShuKV0KICAgICAgICBzcSA9IFt4ICogeCBmb3IgeCBpbiBub2RlXQogICAg
ICAgIGFkbSwgYm91bmRhcnkgPSAwLCBGYWxzZQogICAgICAgIGZvciBpIGluIHJhbmdlKG4pOgog
ICAgICAgICAgICBiYXNlID0gazIgKiBzcVtpXQogICAgICAgICAgICBmb3IgaiBpbiByYW5nZShu
KToKICAgICAgICAgICAgICAgIHYgPSBiYXNlICsgazQgKiBzcVtqXQogICAgICAgICAgICAgICAg
aWYgbG8gPD0gdiA8PSBoaToKICAgICAgICAgICAgICAgICAgICBhZG0gKz0gMQogICAgICAgICAg
ICAgICAgICAgIGlmIGkgaW4gKDAsIG4gLSAxKSBvciBqIGluICgwLCBuIC0gMSk6CiAgICAgICAg
ICAgICAgICAgICAgICAgIGJvdW5kYXJ5ID0gVHJ1ZQogICAgICAgIGRlZmluID0gJ2luZGVmaW5p
dGUnIGlmIGsyICogazQgPCAwIGVsc2UgKCduZWdhdGl2ZS1kZWZpbml0ZScgaWYgazIgPCAwIGVs
c2UgJ3Bvc2l0aXZlLWRlZmluaXRlJykKICAgICAgICByZXR1cm4geydhZG1pc3NpYmxlX25vZGVz
JzogYWRtLCAndG90YWxfbm9kZXMnOiBuICogbiwgJ2FyZWFfZnJhY3Rpb24nOiBhZG0gLyAobiAq
IG4pLCAnbnVsbF9yYXlfc2xvcGUnOiBtYXRoLnNxcnQoLWsyIC8gazQpIGlmIGsyICogazQgPCAw
IGVsc2UgTm9uZSwKICAgICAgICAgICAgICAgICdkZWZpbml0ZW5lc3MnOiBkZWZpbiwgJ2NvbXBh
Y3QnOiBub3QgYm91bmRhcnl9CgogICAgZGVmIG1hcF9pbnRlcnZhbChzZWxmLCBsbywgaGksIHdp
dGhfdHdvX3BhcmFtPVRydWUpOgogICAgICAgICIiImxvIDw9IGhpOyByZXR1cm5zIHRoZSBwZXIt
Y2VsbCByZWNvcmQgYW5kIHRoZSBnYXRlLWxldmVsIGZpZWxkcyBmb3IgdGhpcyBpbnRlcnZhbCAo
bm8gdmFsdWUgc2VyaWFsaXplZCkiIiIKICAgICAgICBjb250YWluczAgPSBsbyA8PSAwLjAgPD0g
aGkKICAgICAgICByZXMgPSB7J2NvbnRhaW5zX3plcm8nOiBjb250YWluczAsICdmYW1pbGllcyc6
IE5vbmUsICdleGNsdXNpb24nOiBOb25lLCAndHdvX3BhcmFtJzogTm9uZX0KICAgICAgICBpZiBj
b250YWluczA6CiAgICAgICAgICAgIHJlc1snZmFtaWxpZXMnXSA9IHtrOiB7YXJtOiB7Zjogc2Vs
Zi5mYW1fd2luZG93KGssIGFybSwgZiwgbG8sIGhpKSBmb3IgZiBpbiAoJ3Q0JywgJ3QyJyl9IGZv
ciBhcm0gaW4gc2VsZi5BUk1TfSBmb3IgayBpbiBzZWxmLktFWVN9CiAgICAgICAgICAgIGlmIHdp
dGhfdHdvX3BhcmFtOgogICAgICAgICAgICAgICAgcmVzWyd0d29fcGFyYW0nXSA9IHtrOiB7YXJt
OiBzZWxmLnR3b19wYXJhbShrLCBhcm0sIGxvLCBoaSkgZm9yIGFybSBpbiBzZWxmLkFSTVN9IGZv
ciBrIGluIHNlbGYuSEVYfQogICAgICAgICAgICBwcmltID0gW3Jlc1snZmFtaWxpZXMnXVtrXVsn
RTJfSGlsbCddWyd0NCddIGZvciBrIGluIHNlbGYuUFJJTV0KICAgICAgICAgICAgYWxsYiA9IGFs
bChwWydjbGFzcyddID09ICdCSU5ESU5HJyBmb3IgcCBpbiBwcmltKQogICAgICAgICAgICByZXNb
J2dhdGVfY2xhc3MnXSA9ICdXSU5ET1ctREVMSVZFUkVEJyBpZiBhbGxiIGVsc2UgJ0lORVJULUlO
LUQnCiAgICAgICAgICAgIHJlc1snc2lnbWFfdW5pb25faGknXSA9IG1heChwWydzaWdtYV9zdGFy
J10gZm9yIHAgaW4gcHJpbSkgaWYgYWxsYiBlbHNlIE5vbmUKICAgICAgICAgICAgcmVzWydzaWdt
YV9zdHJpY3RfaGknXSA9IG1pbihwWydzaWdtYV9zdGFyJ10gZm9yIHAgaW4gcHJpbSkgaWYgYWxs
YiBlbHNlIE5vbmUKICAgICAgICBlbHNlOgogICAgICAgICAgICByZXNbJ2V4Y2x1c2lvbiddID0g
e2s6IHthcm06IHNlbGYuZXhjbHVzaW9uKGssIGFybSwgbG8sIGhpKSBmb3IgYXJtIGluIHNlbGYu
QVJNU30gZm9yIGsgaW4gc2VsZi5LRVlTfQogICAgICAgICAgICBjbHMgPSBbcmVzWydleGNsdXNp
b24nXVtrXVthcm1dWydjbGFzcyddIGZvciBrIGluIHNlbGYuS0VZUyBmb3IgYXJtIGluIHNlbGYu
QVJNU10KICAgICAgICAgICAgaWYgYWxsKGMgPT0gJ0VYQ0xVREVELUlOLUQnIGZvciBjIGluIGNs
cyk6CiAgICAgICAgICAgICAgICByZXNbJ2dhdGVfY2xhc3MnXSA9ICdLSUxMLUlOLUQnCiAgICAg
ICAgICAgIGVsaWYgYW55KGMgPT0gJ1RVTkVELUFETUlTU0lCTEUnIGZvciBjIGluIGNscyk6CiAg
ICAgICAgICAgICAgICByZXNbJ2dhdGVfY2xhc3MnXSA9ICdUVU5FRCcKICAgICAgICAgICAgZWxz
ZToKICAgICAgICAgICAgICAgIHJlc1snZ2F0ZV9jbGFzcyddID0gJ01BUkdJTi1PTkxZJwogICAg
ICAgICAgICByZXNbJ3NpZ21hX3VuaW9uX2hpJ10gPSByZXNbJ3NpZ21hX3N0cmljdF9oaSddID0g
Tm9uZQogICAgICAgIHJldHVybiByZXMKCiAgICBkZWYgbWFwX3Jvd3Moc2VsZiwgcm93cywgd2l0
aF90d29fcGFyYW09VHJ1ZSk6CiAgICAgICAgIiIicm93czogbGlzdCBvZiBkaWN0cyB7bG8sIGhp
LCBrZW0sIGt0fTsgcmV0dXJucyB0aGUgcGhhc2UtMyBtYXBwaW5nIGJsb2NrIChyb3cgbWQ1cyBh
ZGRlZCBieSB0aGUgY2FsbGVyKSIiIgogICAgICAgIG91dCA9IHsncm93cyc6IFtdLCAnbl92b2lk
X3Jvd3MnOiAwfQogICAgICAgIGxpdmUgPSBbXQogICAgICAgIGZvciByIGluIHJvd3M6CiAgICAg
ICAgICAgIHggPSBtYXgoclsna2VtJ10sIHJbJ2t0J10pICogc2VsZi5kRU0KICAgICAgICAgICAg
dm9pZCA9IHggPiBzZWxmLktECiAgICAgICAgICAgIHJlYyA9IHsndm9pZF9yZWdpbWUnOiB2b2lk
LCAnY29udGFpbnNfemVybyc6IE5vbmUsICdnYXRlX2NsYXNzX3Jvdyc6IE5vbmUsICdmYW1pbGll
cyc6IE5vbmUsICdleGNsdXNpb24nOiBOb25lLCAndHdvX3BhcmFtJzogTm9uZX0KICAgICAgICAg
ICAgaWYgdm9pZDoKICAgICAgICAgICAgICAgIG91dFsnbl92b2lkX3Jvd3MnXSArPSAxCiAgICAg
ICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBsaXZlLmFwcGVuZChyKQogICAgICAgICAgICAg
ICAgbSA9IHNlbGYubWFwX2ludGVydmFsKHJbJ2xvJ10sIHJbJ2hpJ10sIHdpdGhfdHdvX3BhcmFt
KQogICAgICAgICAgICAgICAgcmVjLnVwZGF0ZSh7J2NvbnRhaW5zX3plcm8nOiBtWydjb250YWlu
c196ZXJvJ10sICdnYXRlX2NsYXNzX3Jvdyc6IG1bJ2dhdGVfY2xhc3MnXSwgJ2ZhbWlsaWVzJzog
bVsnZmFtaWxpZXMnXSwgJ2V4Y2x1c2lvbic6IG1bJ2V4Y2x1c2lvbiddLCAndHdvX3BhcmFtJzog
bVsndHdvX3BhcmFtJ119KQogICAgICAgICAgICBvdXRbJ3Jvd3MnXS5hcHBlbmQocmVjKQogICAg
ICAgIGlmIG5vdCBsaXZlOgogICAgICAgICAgICBvdXQudXBkYXRlKHsnY29tYmluZWRfZW1wdHkn
OiBOb25lLCAnY29udGFpbnNfemVybyc6IE5vbmUsICdjb21iaW5lZCc6IE5vbmUsICdnYXRlJzog
eydnYXRlX2NsYXNzJzogJ1ZPSUQnLCAnc2lnbWFfdW5pb25faGknOiBOb25lLCAnc2lnbWFfc3Ry
aWN0X2hpJzogTm9uZX19KQogICAgICAgICAgICByZXR1cm4gb3V0CiAgICAgICAgTE8sIEhJID0g
bWF4KHJbJ2xvJ10gZm9yIHIgaW4gbGl2ZSksIG1pbihyWydoaSddIGZvciByIGluIGxpdmUpCiAg
ICAgICAgaWYgTE8gPiBISToKICAgICAgICAgICAgb3V0LnVwZGF0ZSh7J2NvbWJpbmVkX2VtcHR5
JzogVHJ1ZSwgJ2NvbnRhaW5zX3plcm8nOiBOb25lLCAnY29tYmluZWQnOiBOb25lLCAnZ2F0ZSc6
IHsnZ2F0ZV9jbGFzcyc6ICdBTkNIT1ItSU5DT05TSVNURU5UJywgJ3NpZ21hX3VuaW9uX2hpJzog
Tm9uZSwgJ3NpZ21hX3N0cmljdF9oaSc6IE5vbmV9fSkKICAgICAgICAgICAgcmV0dXJuIG91dAog
ICAgICAgIG0gPSBzZWxmLm1hcF9pbnRlcnZhbChMTywgSEksIHdpdGhfdHdvX3BhcmFtKQogICAg
ICAgIG91dC51cGRhdGUoeydjb21iaW5lZF9lbXB0eSc6IEZhbHNlLCAnY29udGFpbnNfemVybyc6
IG1bJ2NvbnRhaW5zX3plcm8nXSwKICAgICAgICAgICAgICAgICAgICAnY29tYmluZWQnOiB7J2Zh
bWlsaWVzJzogbVsnZmFtaWxpZXMnXSwgJ2V4Y2x1c2lvbic6IG1bJ2V4Y2x1c2lvbiddLCAndHdv
X3BhcmFtJzogbVsndHdvX3BhcmFtJ119LAogICAgICAgICAgICAgICAgICAgICdnYXRlJzogeydn
YXRlX2NsYXNzJzogbVsnZ2F0ZV9jbGFzcyddLCAnc2lnbWFfdW5pb25faGknOiBtWydzaWdtYV91
bmlvbl9oaSddLCAnc2lnbWFfc3RyaWN0X2hpJzogbVsnc2lnbWFfc3RyaWN0X2hpJ119fSkKICAg
ICAgICByZXR1cm4gb3V0CgogICAgZGVmIGZ1bGwoc2VsZiwgcm93cyk6CiAgICAgICAgIiIidGhl
IG1hcHBpbmcgd2l0aCBPT00gcm9idXN0bmVzcyBhbmQgdGhlIG1vbm90b25pY2l0eSBjaGVjayAo
aGFsdHMgYXMgYW4gaW5zdHJ1bWVudCBkZWZlY3QpIiIiCiAgICAgICAgYmFzZSA9IHNlbGYubWFw
X3Jvd3Mocm93cykKICAgICAgICBzY2FsZWQgPSB7fQogICAgICAgIGZvciB0YWcsIGZjdCBpbiAo
KCd4MTAnLCAxMC4wKSwgKCd4MHAxJywgMC4xKSk6CiAgICAgICAgICAgIHNjYWxlZFt0YWddID0g
c2VsZi5tYXBfcm93cyhbeydsbyc6IHJbJ2xvJ10gKiBmY3QsICdoaSc6IHJbJ2hpJ10gKiBmY3Qs
ICdrZW0nOiByWydrZW0nXSwgJ2t0Jzogclsna3QnXX0gZm9yIHIgaW4gcm93c10sIHdpdGhfdHdv
X3BhcmFtPUZhbHNlKQogICAgICAgICAgICB3b3JzdCwgdmlvbCA9IHNlbGYubW9ub19jaGVjayhi
YXNlLCBzY2FsZWRbdGFnXSwgZmN0KQogICAgICAgICAgICBpZiB3b3JzdCA+IHNlbGYuUFsnY29u
c3RhbnRzJ11bJ21vbm9fdG9sX3JlbCddIG9yIHZpb2w6CiAgICAgICAgICAgICAgICByYWlzZSBI
YWx0KCdGLUNUUkwtU0EtTU9OTyBvbiB0aGUgYWN0dWFsIHJvd3M6IHNjYWxpbmcgZGV2ICUuM2Us
ICVkIG1vbm90b25pY2l0eSB2aW9sYXRpb25zIC0tIGluc3RydW1lbnQgZGVmZWN0IChTOSknICUg
KHdvcnN0LCB2aW9sKSkKICAgICAgICBnID0gYmFzZVsnZ2F0ZSddCiAgICAgICAgZ1snb29tX2Ns
YXNzX3gxMCddLCBnWydvb21fY2xhc3NfeDBwMSddID0gc2NhbGVkWyd4MTAnXVsnZ2F0ZSddWydn
YXRlX2NsYXNzJ10sIHNjYWxlZFsneDBwMSddWydnYXRlJ11bJ2dhdGVfY2xhc3MnXQogICAgICAg
IGdbJ29vbV9yb2J1c3QnXSA9IGdbJ2dhdGVfY2xhc3MnXSA9PSBnWydvb21fY2xhc3NfeDEwJ10g
PT0gZ1snb29tX2NsYXNzX3gwcDEnXQogICAgICAgIGdbJ2NvbnRhaW5zX3plcm8nXSwgZ1snY29t
YmluZWRfZW1wdHknXSwgZ1snbl92b2lkX3Jvd3MnXSA9IGJhc2VbJ2NvbnRhaW5zX3plcm8nXSwg
YmFzZVsnY29tYmluZWRfZW1wdHknXSwgYmFzZVsnbl92b2lkX3Jvd3MnXQogICAgICAgIHJldHVy
biBiYXNlCgogICAgZGVmIG1vbm9fY2hlY2soc2VsZiwgYmFzZSwgc2MsIGZjdCk6CiAgICAgICAg
IiIiZXhhY3Qgc3FydChmY3QpIHNjYWxpbmcgb2YgdW5jbGlwcGVkIGVkZ2VzOyBtb25vdG9uZSB3
aW5kb3dzIGFuZCBjbGFzc2VzOyByZXR1cm5zICh3b3JzdCByZWxhdGl2ZSBkZXZpYXRpb24sIHZp
b2xhdGlvbnMpIiIiCiAgICAgICAgd29yc3QsIHZpb2wgPSAwLjAsIDAKICAgICAgICByb290ID0g
bWF0aC5zcXJ0KGZjdCkKICAgICAgICBwYWlycyA9IFsoYi5nZXQoJ2NvbWJpbmVkJyksIHMuZ2V0
KCdjb21iaW5lZCcpKSBmb3IgYiwgcyBpbiAoKGJhc2UsIHNjKSwpIGlmIGIuZ2V0KCdjb21iaW5l
ZCcpIGFuZCBzLmdldCgnY29tYmluZWQnKV0KICAgICAgICBwYWlycyArPSBbKGIsIHMpIGZvciBi
LCBzIGluIHppcChiYXNlWydyb3dzJ10sIHNjWydyb3dzJ10pIGlmIGIuZ2V0KCdmYW1pbGllcycp
IGlzIG5vdCBOb25lIG9yIGIuZ2V0KCdleGNsdXNpb24nKSBpcyBub3QgTm9uZV0KICAgICAgICBP
UkRFUl9XID0geydCSU5ESU5HJzogMCwgJ0lORVJULUlOLUQnOiAxfQogICAgICAgIE9SREVSX1gg
PSB7J1RVTkVELUFETUlTU0lCTEUnOiAwLCAnTUFSR0lOJzogMSwgJ0VYQ0xVREVELUlOLUQnOiAy
fQogICAgICAgIGZvciBiLCBzIGluIHBhaXJzOgogICAgICAgICAgICBpZiBiLmdldCgnZmFtaWxp
ZXMnKToKICAgICAgICAgICAgICAgIGZvciBrIGluIHNlbGYuS0VZUzoKICAgICAgICAgICAgICAg
ICAgICBmb3IgYXJtIGluIHNlbGYuQVJNUzoKICAgICAgICAgICAgICAgICAgICAgICAgZm9yIGYg
aW4gc2VsZi5tYXBwZWQoayk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB4LCB5ID0gYlsn
ZmFtaWxpZXMnXVtrXVthcm1dW2ZdLCBzWydmYW1pbGllcyddW2tdW2FybV1bZl0KICAgICAgICAg
ICAgICAgICAgICAgICAgICAgIGlmIHhbJ2NsYXNzJ10gPT0gJ0JJTkRJTkcnIGFuZCB5WydjbGFz
cyddID09ICdCSU5ESU5HJyBhbmQgeFsndF9zdGFyJ10gPiAwOgogICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgIHdvcnN0ID0gbWF4KHdvcnN0LCBhYnMoeVsndF9zdGFyJ10gLSB4Wyd0X3N0
YXInXSAqIHJvb3QpIC8gKHhbJ3Rfc3RhciddICogcm9vdCkpCiAgICAgICAgICAgICAgICAgICAg
ICAgICAgICBpZiBmY3QgPiAxIGFuZCAoeVsnd2luZG93X2hpJ10gPCB4Wyd3aW5kb3dfaGknXSBv
ciBPUkRFUl9XW3lbJ2NsYXNzJ11dIDwgT1JERVJfV1t4WydjbGFzcyddXSk6CiAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgdmlvbCArPSAxCiAgICAgICAgICAgICAgICAgICAgICAgICAg
ICBpZiBmY3QgPCAxIGFuZCAoeVsnd2luZG93X2hpJ10gPiB4Wyd3aW5kb3dfaGknXSBvciBPUkRF
Ul9XW3lbJ2NsYXNzJ11dID4gT1JERVJfV1t4WydjbGFzcyddXSk6CiAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgdmlvbCArPSAxCiAgICAgICAgICAgIGlmIGIuZ2V0KCdleGNsdXNpb24n
KToKICAgICAgICAgICAgICAgIGZvciBrIGluIHNlbGYuS0VZUzoKICAgICAgICAgICAgICAgICAg
ICBmb3IgYXJtIGluIHNlbGYuQVJNUzoKICAgICAgICAgICAgICAgICAgICAgICAgeCwgeSA9IGJb
J2V4Y2x1c2lvbiddW2tdW2FybV0sIHNbJ2V4Y2x1c2lvbiddW2tdW2FybV0KICAgICAgICAgICAg
ICAgICAgICAgICAgaWYgZmN0ID4gMSBhbmQgT1JERVJfWFt5WydjbGFzcyddXSA8IE9SREVSX1hb
eFsnY2xhc3MnXV06CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB2aW9sICs9IDEKICAgICAg
ICAgICAgICAgICAgICAgICAgaWYgZmN0IDwgMSBhbmQgT1JERVJfWFt5WydjbGFzcyddXSA+IE9S
REVSX1hbeFsnY2xhc3MnXV06CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB2aW9sICs9IDEK
ICAgICAgICAgICAgICAgICAgICAgICAgZm9yIGYsIHJxIGluIHhbJ3JlcXVpcmVtZW50cyddLml0
ZW1zKCk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiBycVsndF9pbiddIGlzIG5vdCBO
b25lOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZvciBrZXkgaW4gKCd0X2luJywg
J3Rfb3V0Jyk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHdvcnN0ID0gbWF4
KHdvcnN0LCBhYnMoeVsncmVxdWlyZW1lbnRzJ11bZl1ba2V5XSAtIHJxW2tleV0gKiByb290KSAv
IChycVtrZXldICogcm9vdCkpCiAgICAgICAgcmV0dXJuIHdvcnN0LCB2aW9sCgoKIyAtLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gdGhlIHNlYWxlZCBmaWxlIChBLTIuMyksIG1hc2tl
ZApjbGFzcyBNYXNrZWRBYm9ydChFeGNlcHRpb24pOgogICAgcGFzcwoKCmRlZiBkZWNvZGVfYXJt
b3IocGF0aCk6CiAgICAiIiJiYXNlNjQgdGV4dCAobWFya2VyIGxpbmVzIHN0cmlwcGVkKSBvciBh
IHppcCB3aXRoIGV4YWN0bHkgb25lIG1lbWJlcjsgcmV0dXJucyB0aGUgcmF3IGJ5dGVzIiIiCiAg
ICBnbG9iYWwgU0VBTEVEX09QRU5TCiAgICBTRUFMRURfT1BFTlMgKz0gMQogICAgYiA9IG9wZW4o
cGF0aCwgJ3JiJykucmVhZCgpCiAgICBpZiBiWzoyXSA9PSBiJ1BLJzoKICAgICAgICB6ID0gemlw
ZmlsZS5aaXBGaWxlKGlvLkJ5dGVzSU8oYikpCiAgICAgICAgbmFtZXMgPSBbbiBmb3IgbiBpbiB6
Lm5hbWVsaXN0KCkgaWYgbm90IG4uZW5kc3dpdGgoJy8nKV0KICAgICAgICBpZiBsZW4obmFtZXMp
ICE9IDE6CiAgICAgICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KCdBUk1PUl9aSVBfTk9UX09ORV9N
RU1CRVInKQogICAgICAgIHJldHVybiB6LnJlYWQobmFtZXNbMF0pCiAgICBsaW5lcyA9IFtsLnN0
cmlwKCkgZm9yIGwgaW4gYi5kZWNvZGUoJ2FzY2lpJywgZXJyb3JzPSdyZXBsYWNlJykuc3BsaXRs
aW5lcygpXQogICAgYm9keSA9ICcnLmpvaW4obCBmb3IgbCBpbiBsaW5lcyBpZiBsIGFuZCBub3Qg
bC5zdGFydHN3aXRoKCctLS0tLScpIGFuZCBub3QgbC5zdGFydHN3aXRoKCc9PT09PScpKQogICAg
dHJ5OgogICAgICAgIHJldHVybiBiYXNlNjQuYjY0ZGVjb2RlKGJvZHksIHZhbGlkYXRlPVRydWUp
CiAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KCdBUk1PUl9C
QVNFNjRfSU5WQUxJRCcpCgoKZGVmIGNoZWNrX3ZhbHVlKGtleSwgdmFsKToKICAgIGlmIHZhbCA9
PSAnJyBvciB2YWwgIT0gdmFsLnN0cmlwKCk6CiAgICAgICAgcmV0dXJuICdFTVBUWV9PUl9QQURE
RUQnCiAgICBpZiBrZXkgbm90IGluICgnc3JjJywgJ25vdGUnKSBhbmQgbm90IGFsbCgzMiA8PSBv
cmQoYykgPCAxMjcgZm9yIGMgaW4gdmFsKToKICAgICAgICByZXR1cm4gJ05PTl9BU0NJSScKICAg
IGlmIGtleSA9PSAnY2xhc3MnOgogICAgICAgIHJldHVybiAnT0snIGlmIHZhbCA9PSAnc3BkJyBl
bHNlICdDTEFTU19OT1RfUkVBRF9CWV9USElTX0dBVEUnCiAgICBpZiBrZXkgPT0gJ2RlbHRhX2Rl
Zic6CiAgICAgICAgcmV0dXJuICdPSycgaWYgdmFsID09ICd0ZW5zb3Jfb3Zlcl9FTV9taW51c18x
JyBlbHNlICdXUk9OR19ERUxUQV9ERUYnCiAgICBpZiBrZXkgaW4gKCdsbycsICdoaScpOgogICAg
ICAgIHJldHVybiAnT0snIGlmIChOVU0ubWF0Y2godmFsKSBhbmQgbWF0aC5pc2Zpbml0ZShmbG9h
dCh2YWwpKSkgZWxzZSAnTk9UX0FfUExBSU5fTlVNQkVSJwogICAgaWYga2V5ID09ICdjbCc6CiAg
ICAgICAgaWYgdmFsID09ICdoYXJkJzoKICAgICAgICAgICAgcmV0dXJuICdPSycKICAgICAgICBy
ZXR1cm4gJ09LJyBpZiAoTlVNLm1hdGNoKHZhbCkgYW5kIDAuMCA8IGZsb2F0KHZhbCkgPCAxLjAp
IGVsc2UgJ0NMX05PVF9JTl8oMCwxKV9PUl9oYXJkJwogICAgaWYga2V5ID09ICdyZWFkaW5nJzoK
ICAgICAgICByZXR1cm4gJ09LJyBpZiB2YWwgPT0gJ2JvdW5kJyBlbHNlICgnUkVBRElOR19OT1Rf
TUFQUEVEJyBpZiB2YWwgaW4gKCdjZWlsaW5nJywgJ21hcmdpbicsICdjcml0ZXJpb24nKSBlbHNl
ICdVTktOT1dOX1JFQURJTkcnKQogICAgaWYga2V5ID09ICdnZW9tJzoKICAgICAgICByZXR1cm4g
J09LJyBpZiB2YWwgaW4gKCdzaW5nbGUnLCAncG9wdWxhdGlvbicpIGVsc2UgJ1VOS05PV05fR0VP
TScKICAgIGlmIGtleSBpbiAoJ2tfZW1fbWF4JywgJ2tfdF9tYXgnKToKICAgICAgICByZXR1cm4g
J09LJyBpZiAoTlVNLm1hdGNoKHZhbCkgYW5kIG1hdGguaXNmaW5pdGUoZmxvYXQodmFsKSkgYW5k
IGZsb2F0KHZhbCkgPiAwLjApIGVsc2UgJ05PVF9BX1BPU0lUSVZFX1BMQUlOX05VTUJFUicKICAg
IGlmIGtleSA9PSAncSc6CiAgICAgICAgcmV0dXJuICdPSycgaWYgdmFsIGluICgncGhhc2UnLCAn
Z3JvdXAnKSBlbHNlICdVTktOT1dOX1EnCiAgICByZXR1cm4gJ09LJwoKCmRlZiBwYXJzZV9zZWFs
ZWQocmF3KToKICAgICIiIm1hc2tlZCBwYXJzZTogcmV0dXJucyAocm93cyBhcyBmbG9hdHMsIGNl
bnN1cywgcm93IG1kNXMpOyByYWlzZXMgTWFza2VkQWJvcnQocmVhc29uKSAtLSBubyB2YWx1ZSBp
biBhbnkgbWVzc2FnZSIiIgogICAgaWYgcmF3LnN0YXJ0c3dpdGgoYidceGVmXHhiYlx4YmYnKToK
ICAgICAgICByYWlzZSBNYXNrZWRBYm9ydCgnQk9NX1BSRVNFTlQnKQogICAgdHJ5OgogICAgICAg
IHRleHQgPSByYXcuZGVjb2RlKCd1dGYtOCcpCiAgICBleGNlcHQgVW5pY29kZURlY29kZUVycm9y
OgogICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KCdOT1RfVVRGOCcpCiAgICBpZiAnXHInIGluIHRl
eHQ6CiAgICAgICAgcmFpc2UgTWFza2VkQWJvcnQoJ0NSX1BSRVNFTlQnKQogICAgaWYgJ1x0JyBp
biB0ZXh0OgogICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KCdUQUJfUFJFU0VOVCcpCiAgICBpZiBh
bnkoKChvcmQoYykgPCAzMiBhbmQgYyAhPSAnXG4nKSBvciAxMjcgPD0gb3JkKGMpIDwgMTYwIG9y
IGMgaW4gQkFEX1VOSUNPREUpIGZvciBjIGluIHRleHQpOgogICAgICAgIHJhaXNlIE1hc2tlZEFi
b3J0KCdDT05UUk9MX09SX1NFUEFSQVRPUl9DSEFSJykKICAgIGlmIG5vdCB0ZXh0LmVuZHN3aXRo
KCdcbicpOgogICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KCdOT19UUkFJTElOR19MRicpCiAgICBp
ZiB0ZXh0LmVuZHN3aXRoKCdcblxuJyk6CiAgICAgICAgcmFpc2UgTWFza2VkQWJvcnQoJ0JMQU5L
X0xJTkVfQVRfRU5EJykKICAgIGxpbmVzID0gdGV4dFs6LTFdLnNwbGl0KCdcbicpCiAgICByb3dz
LCBjZW5zdXMsIG1kNXMsIGZpZWxkc19wZXJfcm93ID0gW10sIHt9LCBbXSwgW10KICAgIGZvciBu
LCBsaW5lIGluIGVudW1lcmF0ZShsaW5lcywgMSk6CiAgICAgICAgdGFnID0gJ3JvdyAlZDogJyAl
IG4KICAgICAgICBpZiBsaW5lLnN0cmlwKCkgPT0gJyc6CiAgICAgICAgICAgIHJhaXNlIE1hc2tl
ZEFib3J0KHRhZyArICdCTEFOS19MSU5FJykKICAgICAgICBpZiBsaW5lLnN0YXJ0c3dpdGgoJ3wn
KSBvciBsaW5lLnJzdHJpcCgpLmVuZHN3aXRoKCd8Jyk6CiAgICAgICAgICAgIHJhaXNlIE1hc2tl
ZEFib3J0KHRhZyArICdMRUFESU5HX09SX1RSQUlMSU5HX0JBUicpCiAgICAgICAgZmllbGRzID0g
bGluZS5zcGxpdChTRVApCiAgICAgICAgaWYgYW55KCd8JyBpbiBmIGZvciBmIGluIGZpZWxkcyk6
CiAgICAgICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KHRhZyArICdTRVBBUkFUT1JfQ09MTElTSU9O
JykKICAgICAgICBrZXlzLCB2YWxzID0gW10sIHt9CiAgICAgICAgZm9yIGYgaW4gZmllbGRzOgog
ICAgICAgICAgICBpZiAnPScgbm90IGluIGY6CiAgICAgICAgICAgICAgICByYWlzZSBNYXNrZWRB
Ym9ydCh0YWcgKyAnRklFTERfV0lUSE9VVF9FUVVBTFMnKQogICAgICAgICAgICBrLCB2ID0gZi5z
cGxpdCgnPScsIDEpCiAgICAgICAgICAgIGlmIGsgbm90IGluIENBTk9OOgogICAgICAgICAgICAg
ICAgcmFpc2UgTWFza2VkQWJvcnQodGFnICsgJ1VOS05PV05fS0VZJykKICAgICAgICAgICAgaWYg
ayBpbiB2YWxzOgogICAgICAgICAgICAgICAgcmFpc2UgTWFza2VkQWJvcnQodGFnICsgJ0RVUExJ
Q0FURV9LRVlfJyArIGspCiAgICAgICAgICAgIGtleXMuYXBwZW5kKGspOyB2YWxzW2tdID0gdgog
ICAgICAgIG1pc3NpbmcgPSBbayBmb3IgayBpbiBSRVFVSVJFRCBpZiBrIG5vdCBpbiB2YWxzXQog
ICAgICAgIGlmIG1pc3Npbmc6CiAgICAgICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KHRhZyArICdN
SVNTSU5HX1JFUVVJUkVEXycgKyAnLCcuam9pbihtaXNzaW5nKSkKICAgICAgICBpZiBrZXlzICE9
IFtrIGZvciBrIGluIENBTk9OIGlmIGsgaW4ga2V5c106CiAgICAgICAgICAgIHJhaXNlIE1hc2tl
ZEFib3J0KHRhZyArICdLRVlfT1JERVInKQogICAgICAgIGlmIHZhbHNbJ2lkJ10gIT0gJ1NBLSVk
JyAlIG46CiAgICAgICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KHRhZyArICdJRF9TRVFVRU5DRScp
CiAgICAgICAgZm9yIGsgaW4ga2V5czoKICAgICAgICAgICAgYyA9IGNoZWNrX3ZhbHVlKGssIHZh
bHNba10pCiAgICAgICAgICAgIGlmIGMgIT0gJ09LJzoKICAgICAgICAgICAgICAgIHJhaXNlIE1h
c2tlZEFib3J0KHRhZyArICdrZXkgJXMgLT4gJXMnICUgKGssIGMpKQogICAgICAgIGxvLCBoaSA9
IGZsb2F0KHZhbHNbJ2xvJ10pLCBmbG9hdCh2YWxzWydoaSddKQogICAgICAgIGlmIG5vdCBsbyA8
PSBoaToKICAgICAgICAgICAgcmFpc2UgTWFza2VkQWJvcnQodGFnICsgJ09SREVSJykKICAgICAg
ICByb3dzLmFwcGVuZCh7J2xvJzogbG8sICdoaSc6IGhpLCAna2VtJzogZmxvYXQodmFsc1sna19l
bV9tYXgnXSksICdrdCc6IGZsb2F0KHZhbHNbJ2tfdF9tYXgnXSksICdnZW9tJzogdmFsc1snZ2Vv
bSddLCAncSc6IHZhbHMuZ2V0KCdxJyl9KQogICAgICAgIGNlbnN1c1t2YWxzWydjbGFzcyddXSA9
IGNlbnN1cy5nZXQodmFsc1snY2xhc3MnXSwgMCkgKyAxCiAgICAgICAgbWQ1cy5hcHBlbmQobWQ1
YihsaW5lLmVuY29kZSgndXRmLTgnKSkpCiAgICAgICAgZmllbGRzX3Blcl9yb3cuYXBwZW5kKGxl
bihmaWVsZHMpKQogICAgaWYgbm90IHJvd3M6CiAgICAgICAgcmFpc2UgTWFza2VkQWJvcnQoJ05P
X1JPV1MnKQogICAgcmV0dXJuIHJvd3MsIHsncm93cyc6IGxlbihyb3dzKSwgJ3Blcl9jbGFzcyc6
IGNlbnN1cywgJ2ZpZWxkc19wZXJfcm93JzogZmllbGRzX3Blcl9yb3d9LCBtZDVzCgoKZGVmIG9w
ZW5fc2VhbGVkKHBhdGgsIG1kNV9zdGF0ZWQsIGJ5dGVzX3N0YXRlZCk6CiAgICByYXcgPSBkZWNv
ZGVfYXJtb3IocGF0aCkKICAgIGlmIG1kNWIocmF3KSAhPSBtZDVfc3RhdGVkIG9yIGxlbihyYXcp
ICE9IGludChieXRlc19zdGF0ZWQpOgogICAgICAgIHJhaXNlIE1hc2tlZEFib3J0KCdTRUFMRURf
TUQ1X09SX0JZVEVTX01JU01BVENIJykKICAgIHJvd3MsIGNlbnN1cywgbWQ1cyA9IHBhcnNlX3Nl
YWxlZChyYXcpCiAgICByZXR1cm4gcm93cywgY2Vuc3VzLCBtZDVzLCBtZDViKHJhdyksIGxlbihy
YXcpCgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gUGhhc2UgMApkZWYgcGhh
c2UwKFAsIERWLCBNLCBwYXRocywgcmVwbywgYTEpOgogICAgQyA9IFBbJ2NvbnN0YW50cyddCiAg
ICBvdXQgPSB7fQogICAgS0VZUywgQVJNUywgSEVYID0gUFsnc3RydWN0dXJlJ11bJ2tleXMnXSwg
UFsnc3RydWN0dXJlJ11bJ2FybXMnXSwgUFsnc3RydWN0dXJlJ11bJ2hleF9rZXlzJ10KICAgICMg
UElOCiAgICBkb2NzID0ge30KICAgIGZvciBhbGlhcywgcyBpbiBQWydzb3VyY2VzJ10uaXRlbXMo
KToKICAgICAgICBiID0gb3Blbihvcy5wYXRoLmpvaW4ocmVwbywgc1sncGF0aCddKSwgJ3JiJyku
cmVhZCgpCiAgICAgICAgaWYgbWQ1YihiKSAhPSBzWydtZDUnXSBvciBsZW4oYikgIT0gc1snYnl0
ZXMnXToKICAgICAgICAgICAgcmFpc2UgSGFsdCgnRi1DVFJMLVNBLVBJTjogc291cmNlICVzIG1k
NS9ieXRlcycgJSBzWydwYXRoJ10pCiAgICAgICAgZG9jc1thbGlhc10gPSBqc29uLmxvYWRzKGIu
ZGVjb2RlKCd1dGYtOCcpKQogICAgbWlzbSA9IDAKICAgIGZvciBkZXN0LCBzcGVjIGluIFBbJ3By
b3ZlbmFuY2UnXS5pdGVtcygpOgogICAgICAgIGlmIGRlc3Quc3RhcnRzd2l0aCgna2V5cy88Sz4v
Jyk6CiAgICAgICAgICAgIHN1YiA9IGRlc3RbbGVuKCdrZXlzLzxLPi8nKTpdCiAgICAgICAgICAg
IGtzID0gS0VZUyBpZiBzcGVjWydzY29wZSddID09ICdhbGwnIGVsc2UgUFsnc3RydWN0dXJlJ11b
J2N1YmljX2tleXMnXSBpZiBzcGVjWydzY29wZSddID09ICdjdWJpYycgZWxzZSBbayBmb3IgayBp
biBLRVlTIGlmIGsgaW4gZG9jc1snRFFGJ11dCiAgICAgICAgICAgIGZvciBrIGluIGtzOgogICAg
ICAgICAgICAgICAgaGF2ZSA9IHB0cihQWydyYXcnXVsna2V5cyddW2tdLCAnLycgKyBzdWIpCiAg
ICAgICAgICAgICAgICBpZiBqc29uLmR1bXBzKGhhdmUpICE9IGpzb24uZHVtcHMocHRyKGRvY3Nb
c3BlY1snc3JjJ11dLCBzcGVjWydwb2ludGVyJ10ucmVwbGFjZSgne0t9JywgaykpKToKICAgICAg
ICAgICAgICAgICAgICBtaXNtICs9IDEKICAgICAgICBlbHNlOgogICAgICAgICAgICBpZiBqc29u
LmR1bXBzKHB0cihQLCAnLycgKyBkZXN0KSkgIT0ganNvbi5kdW1wcyhwdHIoZG9jc1tzcGVjWydz
cmMnXV0sIHNwZWNbJ3BvaW50ZXInXSkpOgogICAgICAgICAgICAgICAgbWlzbSArPSAxCiAgICBy
ZWwgPSBsYW1iZGEgeCwgeTogYWJzKHggLSB5KSAvIG1heChhYnMoeCksIGFicyh5KSkKICAgIHdr
ID0gd2szID0gd3MgPSB3YiA9IDAuMAogICAgZm9yIGsgaW4gS0VZUzoKICAgICAgICByayA9IFBb
J3JhdyddWydrZXlzJ11ba10KICAgICAgICB3YiA9IG1heCh3YiwgcmVsKHJrWydiMV9IaWxsJ10s
IHJrWydiMV9IaWxsX2NjJ10pKQogICAgICAgIGZvciBhcm0gaW4gQVJNUzoKICAgICAgICAgICAg
Zm9yIGYgaW4gTS5tYXBwZWQoayk6CiAgICAgICAgICAgICAgICBkID0gcmtbJ2FybXMnXVthcm1d
W2ZdCiAgICAgICAgICAgICAgICBpZiAna2FwcGFfY2MnIGluIGQgYW5kIG1heChhYnMoZFsna2Fw
cGEnXSksIGFicyhkWydrYXBwYV9jYyddKSkgPiBDWydrYXBwYV9mbG9vciddOgogICAgICAgICAg
ICAgICAgICAgIHdrID0gbWF4KHdrLCByZWwoZFsna2FwcGEnXSwgZFsna2FwcGFfY2MnXSkpCiAg
ICAgICAgICAgICAgICBpZiAna2FwcGEzX2NjJyBpbiBkOgogICAgICAgICAgICAgICAgICAgIHdr
MyA9IG1heCh3azMsIHJlbChkWydrYXBwYTMnXSwgZFsna2FwcGEzX2NjJ10pKQogICAgICAgICAg
ICAgICAgaWYgJ1NfY2MnIGluIGQ6CiAgICAgICAgICAgICAgICAgICAgd3MgPSBtYXgod3MsIGFi
cyhkWydTJ10gLSBkWydTX2NjJ10pKQogICAgZSA9IHsnb2RmX3JlYWRpbmcnOiAnbm9uZScsICdy
YXdfbWlzbWF0Y2hlcyc6IG1pc20sICd3b3JzdF90d29sZWdfa2FwcGFfcmVsJzogd2ssICd3b3Jz
dF90d29sZWdfa2FwcGEzX3JlbCc6IHdrMywgJ3dvcnN0X3R3b2xlZ19iMV9yZWwnOiB3YiwgJ3dv
cnN0X3R3b2xlZ19TX2Ficyc6IHdzfQogICAgZVsncGFzc2VkJ10gPSBtaXNtID09IDAgYW5kIHdr
IDw9IENbJ3Bpbl90d29sZWdfdG9sX3JlbCddIGFuZCB3azMgPD0gQ1sncGluX3R3b2xlZ190b2xf
cmVsJ10gYW5kIHdiIDw9IENbJ3Bpbl90d29sZWdfdG9sX3JlbCddIGFuZCB3cyA8PSBDWyd0YXVf
YWdnJ10KICAgIG91dFsnRi1DVFJMLVNBLVBJTiddID0gZQogICAgIyBQSU4tREVSSVZFRAogICAg
bWluZSwgdGhlaXJzID0gZmxhdChEViksIGZsYXQoe2s6IFBbJ2Rlcml2ZWQnXVtrXSBmb3IgayBp
biBEVn0pCiAgICB3b3JzdCwgbG0gPSAwLjAsIDAKICAgIGlmIHNldChtaW5lKSAhPSBzZXQodGhl
aXJzKToKICAgICAgICBsbSArPSBsZW4oc2V0KG1pbmUpIF4gc2V0KHRoZWlycykpCiAgICBmb3Ig
cCBpbiBtaW5lOgogICAgICAgIGlmIHAgbm90IGluIHRoZWlyczoKICAgICAgICAgICAgY29udGlu
dWUKICAgICAgICBhLCBiID0gbWluZVtwXSwgdGhlaXJzW3BdCiAgICAgICAgaWYgaXNpbnN0YW5j
ZShhLCBmbG9hdCkgYW5kIGlzaW5zdGFuY2UoYiwgZmxvYXQpOgogICAgICAgICAgICB3b3JzdCA9
IG1heCh3b3JzdCwgYWJzKGEgLSBiKSAvIChDWydwaW5fZGVyaXZlZF90b2xfcmVsJ10gKiBhYnMo
YikgKyBDWydwaW5fZGVyaXZlZF90b2xfYWJzJ10pKQogICAgICAgIGVsaWYgYSAhPSBiIG9yIHR5
cGUoYSkgIT0gdHlwZShiKToKICAgICAgICAgICAgbG0gKz0gMQogICAgb3V0WydGLUNUUkwtU0Et
UElOLURFUklWRUQnXSA9IHsnb2RmX3JlYWRpbmcnOiAnbm9uZScsICd3b3JzdF9zY2FsZWRfZGV2
Jzogd29yc3QsICdsZWFmX21pc21hdGNoZXMnOiBsbSwgJ2xlYXZlc19jb21wYXJlZCc6IGxlbiht
aW5lKSwgJ3Bhc3NlZCc6IHdvcnN0IDw9IDEuMCBhbmQgbG0gPT0gMH0KICAgICMgWkVSTwogICAg
d3ogPSBtYXgoYWJzKERWWydmYW1pbGllcyddW2tdW2FdW2ZdWydyMCddKSBmb3IgayBpbiBLRVlT
IGZvciBhIGluIEFSTVMgZm9yIGYgaW4gKCd0NCcsICd0MicpKQogICAgb3V0WydGLUNUUkwtU0Et
WkVSTyddID0geydvZGZfcmVhZGluZyc6ICd1bmlmb3JtJywgJ3dvcnN0X2Fic19yMCc6IHd6LCAn
cGFzc2VkJzogd3ogPD0gQ1snemVyb19jdHJsX3RvbF9hYnMnXX0KICAgICMgUkVDT04KICAgIHdy
ID0gbWF4KERWWydmYW1pbGllcyddW2tdWydFMl9IaWxsJ11bZl1bJ3JlY29uX21heF9hYnMnXSBm
b3IgayBpbiBLRVlTIGZvciBmIGluIE0ubWFwcGVkKGspKQogICAgd3JyID0gbWF4KERWWydmYW1p
bGllcyddW2tdW2FdW2ZdWydmaXRfcmVzX3JlbCddIGZvciBrIGluIEtFWVMgZm9yIGEgaW4gKCdF
Ml9IU21lYW4nLCAnaF9IaWxsJykgZm9yIGYgaW4gTS5tYXBwZWQoaykpCiAgICBvdXRbJ0YtQ1RS
TC1TQS1SRUNPTiddID0geydvZGZfcmVhZGluZyc6ICdoZXhQNC9jdWJLNC9oZXhQMicsICd3b3Jz
dF9hYnNfRTJfSGlsbCc6IHdyLCAnd29yc3RfcmVsX3JvYnVzdCc6IHdyciwKICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgJ3Bhc3NlZCc6IHdyIDw9IENbJ3JlY29uX3RvbF9hYnNfRTJfSGls
bCddIGFuZCB3cnIgPD0gQ1sncmVjb25fdG9sX3JlbF9yb2J1c3QnXX0KICAgICMgUyAoTi0xKQog
ICAgbjEgPSBEVlsnbnVsbHMnXVsnTi0xJ10KICAgIHdiXyA9IG1heChhYnModlsnYmknXSkgZm9y
IHYgaW4gbjEudmFsdWVzKCkpCiAgICB3Zl8gPSBtYXgoYWJzKHZbJ2ZpdCddKSBmb3IgdiBpbiBu
MS52YWx1ZXMoKSBpZiB2WydmaXQnXSBpcyBub3QgTm9uZSkKICAgIG91dFsnRi1DVFJMLVNBLVMn
XSA9IHsnb2RmX3JlYWRpbmcnOiAnaGV4UDIvaGV4UDQvY3ViSzQnLCAnd29yc3RfYWJzX2JpJzog
d2JfLCAnd29yc3RfYWJzX2ZpdCc6IHdmXywgJ3Bhc3NlZCc6IHdiXyA8PSBDWyd0YXVfYWdnJ10g
YW5kIHdmXyA8PSBDWyd0YXVfYWdnJ119CiAgICAjIEsyNCAoTi0yKQogICAgbjIgPSBEVlsnbnVs
bHMnXVsnTi0yJ10KICAgIHdiaSA9IG1heChtYXgoYWJzKHZbJ2JpX2NoYXQnXSksIGFicyh2Wydi
aV9jYyddKSwgYWJzKHZbJ2JpXzV4NSddKSkgZm9yIHYgaW4gbjIudmFsdWVzKCkpCiAgICB3NyA9
IG1heChhYnModlsnZml0NyddKSBmb3IgdiBpbiBuMi52YWx1ZXMoKSkKICAgIG91dFsnRi1DVFJM
LVNBLUsyNCddID0geydvZGZfcmVhZGluZyc6ICdoZXhQMlA0L2N1YlAySzQtaScsICd3b3JzdF9h
YnNfYmknOiB3YmksICd3b3JzdF9hYnNfZml0Nyc6IHc3LCAncGFzc2VkJzogd2JpIDw9IENbJ2th
cHBhX2Zsb29yJ10gYW5kIHc3IDw9IENbJ2thcHBhX2Zsb29yJ119CiAgICAjIEwyTlVMTCAoTi0z
LCBOLTQpCiAgICBuMywgbjQgPSBEVlsnbnVsbHMnXVsnTi0zJ10sIERWWydudWxscyddWydOLTQn
XQogICAgdzIgPSBtYXgobWF4KGFicyh2WydmaXQnXSksIGFicyh2WydiaSddKSkgZm9yIHYgaW4g
bjMudmFsdWVzKCkpCiAgICB3MjIgPSBtYXgobWF4KGFicyh2WydmaXQ3J10pLCBhYnModlsnYmlf
NXg1J10pLCBhYnModlsnazEyX2NoYXRfdDJzcSddIG9yIDAuMCkpIGZvciB2IGluIG40LnZhbHVl
cygpKQogICAgd3QxID0gbWF4KGFicyh2WydwdXJlX2wyX2NoYW5nZV90MSddKSBmb3IgdiBpbiBu
My52YWx1ZXMoKSkKICAgIG91dFsnRi1DVFJMLVNBLUwyTlVMTCddID0geydvZGZfcmVhZGluZyc6
ICdjdWJQMi1paS9jdWJQMi1pL2N1YlAySzQtaScsICdpZGVudGl0eV9jdWJQMl9paSc6ICd0aGUg
b2N0YWhlZHJhbGx5IHN5bW1ldHJpemVkIGwgPSAyIHBlcnR1cmJhdGlvbiB2YW5pc2hlcyBpZGVu
dGljYWxseSAobm8gbCA9IDIgaW52YXJpYW50IG9mIHRoZSBvY3RhaGVkcmFsIGdyb3VwKTsgYXNz
ZXJ0ZWQgc3ltYm9saWNhbGx5JywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICd3b3Jz
dF9hYnNfa2FwcGEyJzogdzIsICd3b3JzdF9hYnNfa2FwcGEyMic6IHcyMiwgJ3dvcnN0X2Fic190
Ml9hbG9uZV90MSc6IHd0MSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdwYXNzZWQn
OiB3MiA8PSBDWydrYXBwYV9mbG9vciddIGFuZCB3MjIgPD0gQ1sna2FwcGFfZmxvb3InXSBhbmQg
d3QxIDw9IENbJ2wybnVsbF90MV90b2xfYWJzJ119CiAgICAjIFNJR04KICAgIGtyZWYgPSBhYnMo
UFsncmF3J11bJ2tleXMnXVsnaGV4X3N0ZXB8YSddWydhcm1zJ11bJ0UyX0hpbGwnXVsndDQnXVsn
a2FwcGEnXSkKICAgIG0gPSBNLm1hcF9pbnRlcnZhbCgta3JlZiAqIDAuMSAqKiAyLCBrcmVmICog
MC4wNSAqKiAyLCB3aXRoX3R3b19wYXJhbT1GYWxzZSkKICAgIGJtID0gMAogICAgZm9yIGsgaW4g
S0VZUzoKICAgICAgICBmb3IgYSBpbiBBUk1TOgogICAgICAgICAgICBmb3IgZiBpbiBNLm1hcHBl
ZChrKToKICAgICAgICAgICAgICAgIGthcHBhID0gUFsncmF3J11bJ2tleXMnXVtrXVsnYXJtcydd
W2FdW2ZdWydrYXBwYSddCiAgICAgICAgICAgICAgICBpZiBtWydmYW1pbGllcyddW2tdW2FdW2Zd
WydiaW5kaW5nX2VuZCddICE9ICgnaGknIGlmIGthcHBhID4gMCBlbHNlICdsbycpOgogICAgICAg
ICAgICAgICAgICAgIGJtICs9IDEKICAgIG91dFsnRi1DVFJMLVNBLVNJR04nXSA9IHsnb2RmX3Jl
YWRpbmcnOiAnbm9uZScsICdiaW5kaW5nX2VuZF9taXNtYXRjaGVzJzogYm0sICdwYXNzZWQnOiBi
bSA9PSAwfQogICAgIyBHUklECiAgICBnID0gZ3JpZF9jb3VudHMoUCkKICAgIG91dFsnRi1DVFJM
LVNBLUdSSUQnXSA9IHsnb2RmX3JlYWRpbmcnOiAnbm9uZScsICdjb3VudF9taXNtYXRjaGVzJzog
MCwgJ3Bhc3NlZCc6IFRydWUsICdjb3VudHMnOiBnfQogICAgIyBNT05PIG9uIHRoZSBDLVNZTi0x
IGludGVydmFscwogICAgd29yc3RfcywgdmlvbCA9IDAuMCwgMAogICAgZm9yIHQgaW4gQ1snc3lu
dGhldGljX3QnXToKICAgICAgICBiID0ga3JlZiAqIHQgKiB0CiAgICAgICAgcm93cyA9IFt7J2xv
JzogLWIsICdoaSc6IGIsICdrZW0nOiBDWydzeW50aGV0aWNfayddWydzaWxlbnQnXSwgJ2t0Jzog
Q1snc3ludGhldGljX2snXVsnc2lsZW50J119XQogICAgICAgIGJhc2UgPSBNLm1hcF9yb3dzKHJv
d3MsIHdpdGhfdHdvX3BhcmFtPUZhbHNlKQogICAgICAgIGZvciBmY3QgaW4gKDEwLjAsIDAuMSk6
CiAgICAgICAgICAgIHNjID0gTS5tYXBfcm93cyhbeydsbyc6IC1iICogZmN0LCAnaGknOiBiICog
ZmN0LCAna2VtJzogcm93c1swXVsna2VtJ10sICdrdCc6IHJvd3NbMF1bJ2t0J119XSwgd2l0aF90
d29fcGFyYW09RmFsc2UpCiAgICAgICAgICAgIHcsIHYgPSBNLm1vbm9fY2hlY2soYmFzZSwgc2Ms
IGZjdCkKICAgICAgICAgICAgd29yc3RfcywgdmlvbCA9IG1heCh3b3JzdF9zLCB3KSwgdmlvbCAr
IHYKICAgIG91dFsnRi1DVFJMLVNBLU1PTk8nXSA9IHsnb2RmX3JlYWRpbmcnOiAnbm9uZScsICd3
b3JzdF9zY2FsaW5nX3JlbCc6IHdvcnN0X3MsICdtb25vdG9uaWNpdHlfdmlvbGF0aW9ucyc6IHZp
b2wsICdwYXNzZWQnOiB3b3JzdF9zIDw9IENbJ21vbm9fdG9sX3JlbCddIGFuZCB2aW9sID09IDB9
CiAgICAjIE1BU0sKICAgIG91dFsnRi1DVFJMLVNBLU1BU0snXSA9IHsnb2RmX3JlYWRpbmcnOiAn
bm9uZScsICdzZWFsZWRfb3BlbnNfYmVmb3JlX3BoYXNlMyc6IFNFQUxFRF9PUEVOUywgJ3Bhc3Nl
ZCc6IFNFQUxFRF9PUEVOUyA9PSAwfQogICAgIyBUMQogICAgdGFyZ2V0cyA9IFtvcy5wYXRoLmFi
c3BhdGgoX19maWxlX18pLCBwYXRoc1snbWVtbyddLCBwYXRoc1sncGluJ10sIHBhdGhzWydsb2Nr
J10sIHBhdGhzWydzY2hlbWEnXSwgcGF0aHNbJ2NvbXBhcmF0b3InXV0KICAgIHNjID0gdDFfc2Nh
bihwYXRocywgdGFyZ2V0cywgYTEpCiAgICBvdXRbJ0YtQ1RSTC1TQS1UMSddID0geydvZGZfcmVh
ZGluZyc6ICdub25lJywgJ2hpdHMnOiBzY1snaGl0cyddLCAnY29sbGlzaW9ucyc6IHNjWydjb2xs
aXNpb25zJ10sICdwYXR0ZXJucyc6IHNjWydwYXR0ZXJucyddLCAnYTFfaW5jbHVkZWQnOiBzY1sn
YTFfaW5jbHVkZWQnXSwgJ3Blcl9maWxlJzogc2NbJ3Blcl9maWxlJ10sICdwYXNzZWQnOiBzY1sn
aGl0cyddID09IDB9CiAgICByZXR1cm4gb3V0CgoKZGVmIGdyaWRfY291bnRzKFApOgogICAgRywg
RCA9IFBbJ2dyaWRzJ10sIFBbJ2NvbnN0YW50cyddWydEJ10KICAgIHRnID0gR1sndF9ncmlkJ10K
ICAgIHJldHVybiB7J3RfZ3JpZCc6IHRnLCAndDJ0NF9heGlzJzogR1sndDJ0NF9heGlzJ10sICdE
JzogRCwgJ2FyZWFfbm9kZXNfcGVyX2F4aXMnOiBHWydhcmVhX2dyaWQnXVsnbm9kZXNfcGVyX2F4
aXMnXSwKICAgICAgICAgICAgJ25fdF9ncmlkJzogbGVuKHRnKSwgJ25fZml0X3dpbmRvd19pbmNs
dXNpdmUnOiBzdW0oYWJzKHQpIDw9IEQgZm9yIHQgaW4gdGcpLCAnbl9maXRfd2luZG93X3N0cmlj
dCc6IHN1bShhYnModCkgPCBEIGZvciB0IGluIHRnKSwKICAgICAgICAgICAgJ25fd2luZG93XzBw
MV9pbmNsdXNpdmUnOiBzdW0oYWJzKHQpIDw9IDAuMSBmb3IgdCBpbiB0ZyksICduX3dpbmRvd18w
cDFfc3RyaWN0Jzogc3VtKGFicyh0KSA8IDAuMSBmb3IgdCBpbiB0ZyksCiAgICAgICAgICAgICdu
X3QydDRfYXhpcyc6IGxlbihHWyd0MnQ0X2F4aXMnXSksICduX3QydDRfZ3JpZCc6IGxlbihHWyd0
MnQ0X2F4aXMnXSkgKiogMiwgJ25fYXJlYV9ncmlkJzogR1snYXJlYV9ncmlkJ11bJ25vZGVzX3Bl
cl9heGlzJ10gKiogMn0KCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBQaGFz
ZSAyIChBLTIuNSkKZGVmIHBoYXNlMihQLCBEViwgTSk6CiAgICBDID0gUFsnY29uc3RhbnRzJ10K
ICAgIEtFWVMsIEFSTVMsIEhFWCwgUFJJTSA9IFBbJ3N0cnVjdHVyZSddWydrZXlzJ10sIFBbJ3N0
cnVjdHVyZSddWydhcm1zJ10sIFBbJ3N0cnVjdHVyZSddWydoZXhfa2V5cyddLCBQWydzdHJ1Y3R1
cmUnXVsncHJpbWFyeSddWydrZXlzJ10KICAgIGtzID0gQ1snc3ludGhldGljX2snXVsnc2lsZW50
J10KICAgIGtyZWYgPSBhYnMoUFsncmF3J11bJ2tleXMnXVsnaGV4X3N0ZXB8YSddWydhcm1zJ11b
J0UyX0hpbGwnXVsndDQnXVsna2FwcGEnXSkKICAgIGIgPSBsYW1iZGEgdDoga3JlZiAqIHQgKiB0
CiAgICByb3cgPSBsYW1iZGEgbG8sIGhpLCBrPWtzOiB7J2xvJzogbG8sICdoaSc6IGhpLCAna2Vt
JzogaywgJ2t0Jzoga30KICAgIFIgPSB7fQogICAgZGVmIHN1aXRlKG5hbWUsIGNvbmQsIGRldGFp
bCk6CiAgICAgICAgUltuYW1lXSA9IHsncGFzc2VkJzogYm9vbChjb25kKSwgJ2RldGFpbCc6IGRl
dGFpbH0KICAgICAgICBpZiBub3QgY29uZDoKICAgICAgICAgICAgc2F5KCcgICVzIEZBSUxFRDog
JXMnICUgKG5hbWUsIGRldGFpbCkpCiAgICAjIEMtU1lOLTEKICAgIG9rLCBkZXQgPSBUcnVlLCBb
XQogICAgZm9yIHQgaW4gQ1snc3ludGhldGljX3QnXToKICAgICAgICBtID0gTS5tYXBfaW50ZXJ2
YWwoLWIodCksIGIodCksIHdpdGhfdHdvX3BhcmFtPUZhbHNlKQogICAgICAgIHJlZiA9IG1bJ2Zh
bWlsaWVzJ11bJ2hleF9zdGVwfGEnXVsnRTJfSGlsbCddWyd0NCddCiAgICAgICAgb2sgJj0gYWJz
KHJlZlsndF9zdGFyJ10gLSB0KSA8PSAxZS0xMiAqIHQgYW5kIHJlZlsnY2xhc3MnXSA9PSAoJ0JJ
TkRJTkcnIGlmIHQgPCBDWydEJ10gZWxzZSAnSU5FUlQtSU4tRCcpCiAgICAgICAgZm9yIGsgaW4g
S0VZUzoKICAgICAgICAgICAgZm9yIGEgaW4gQVJNUzoKICAgICAgICAgICAgICAgIGZvciBmIGlu
IE0ubWFwcGVkKGspOgogICAgICAgICAgICAgICAgICAgIGthcHBhID0gUFsncmF3J11bJ2tleXMn
XVtrXVsnYXJtcyddW2FdW2ZdWydrYXBwYSddCiAgICAgICAgICAgICAgICAgICAgb2sgJj0gYWJz
KG1bJ2ZhbWlsaWVzJ11ba11bYV1bZl1bJ3Rfc3RhciddIC0gbWF0aC5zcXJ0KGIodCkgLyBhYnMo
a2FwcGEpKSkgPD0gMWUtMTIgKiBtWydmYW1pbGllcyddW2tdW2FdW2ZdWyd0X3N0YXInXQogICAg
ICAgIGRldC5hcHBlbmQoJ3Q9JWcgcmVmIGNsYXNzICVzJyAlICh0LCByZWZbJ2NsYXNzJ10pKQog
ICAgc3VpdGUoJ0MtU1lOLTEnLCBvaywgJzsgJy5qb2luKGRldCkpCiAgICAjIEMtU1lOLTIKICAg
IG0gPSBNLm1hcF9pbnRlcnZhbCgtYigwLjEpLCBiKDAuMDUpLCB3aXRoX3R3b19wYXJhbT1GYWxz
ZSkKICAgIG9rID0gVHJ1ZQogICAgZm9yIGsgaW4gS0VZUzoKICAgICAgICBmb3IgYSBpbiBBUk1T
OgogICAgICAgICAgICBmb3IgZiBpbiBNLm1hcHBlZChrKToKICAgICAgICAgICAgICAgIGthcHBh
ID0gUFsncmF3J11bJ2tleXMnXVtrXVsnYXJtcyddW2FdW2ZdWydrYXBwYSddCiAgICAgICAgICAg
ICAgICBlID0gbVsnZmFtaWxpZXMnXVtrXVthXVtmXQogICAgICAgICAgICAgICAgd2FudCA9ICgw
LjA1IGlmIGthcHBhID4gMCBlbHNlIDAuMSkgKiBtYXRoLnNxcnQoa3JlZiAvIGFicyhrYXBwYSkp
CiAgICAgICAgICAgICAgICBvayAmPSBlWydiaW5kaW5nX2VuZCddID09ICgnaGknIGlmIGthcHBh
ID4gMCBlbHNlICdsbycpIGFuZCBhYnMoZVsndF9zdGFyJ10gLSB3YW50KSA8PSAxZS0xMiAqIHdh
bnQKICAgIHN1aXRlKCdDLVNZTi0yJywgb2ssICdiaW5kaW5nIGVuZHMgYnkgc2lnbihrYXBwYSk7
IGVkZ2VzIGV4YWN0JykKICAgICMgQy1TWU4tMwogICAgVSA9IERWWyd1bmlvbnMnXQogICAgbTEg
PSBNLm1hcF9yb3dzKFtyb3coMTAgKiBVWyd3aWRlbmVkX2FsbCddWzFdLCAyMCAqIFVbJ3dpZGVu
ZWRfYWxsJ11bMV0pXSwgd2l0aF90d29fcGFyYW09RmFsc2UpCiAgICBtMiA9IE0ubWFwX3Jvd3Mo
W3JvdygyMCAqIFVbJ3dpZGVuZWRfYWxsJ11bMF0sIDEwICogVVsnd2lkZW5lZF9hbGwnXVswXSld
LCB3aXRoX3R3b19wYXJhbT1GYWxzZSkKICAgIG0zID0gTS5tYXBfcm93cyhbcm93KDAuMjUgKiBV
WydodWxsX2FsbCddWzFdLCAwLjUgKiBVWydodWxsX2FsbCddWzFdKV0sIHdpdGhfdHdvX3BhcmFt
PUZhbHNlKQogICAgbTQgPSBNLm1hcF9yb3dzKFtyb3coKkRWWydzeW50aGV0aWMnXVsncm9idXN0
bmVzc19vbmx5X3Bvc2l0aXZlJ10pXSwgd2l0aF90d29fcGFyYW09RmFsc2UpCiAgICBvayA9IG0x
WydnYXRlJ11bJ2dhdGVfY2xhc3MnXSA9PSAnS0lMTC1JTi1EJyBhbmQgbTJbJ2dhdGUnXVsnZ2F0
ZV9jbGFzcyddID09ICdLSUxMLUlOLUQnIGFuZCBtM1snZ2F0ZSddWydnYXRlX2NsYXNzJ10gPT0g
J1RVTkVEJyBhbmQgbTRbJ2dhdGUnXVsnZ2F0ZV9jbGFzcyddID09ICdUVU5FRCcKICAgIGZvciBr
IGluIEtFWVM6CiAgICAgICAgZm9yIGEgaW4gQVJNUzoKICAgICAgICAgICAgcncgPSBEVlsncmVh
Y2gnXVtrXVthXVsnd2lkZW5lZCddCiAgICAgICAgICAgIG9rICY9IG0xWydjb21iaW5lZCddWydl
eGNsdXNpb24nXVtrXVthXVsnc3VicmVhc29uJ10gPT0gKCdTSUdOJyBpZiByd1sxXSA8PSAwIGVs
c2UgJ01BR05JVFVERScpCiAgICAgICAgICAgIG9rICY9IG0yWydjb21iaW5lZCddWydleGNsdXNp
b24nXVtrXVthXVsnc3VicmVhc29uJ10gPT0gKCdTSUdOJyBpZiByd1swXSA+PSAwIGVsc2UgJ01B
R05JVFVERScpCiAgICBvayAmPSBhbGwobTRbJ2NvbWJpbmVkJ11bJ2V4Y2x1c2lvbiddW2tdWydF
Ml9IaWxsJ11bJ2NsYXNzJ10gIT0gJ1RVTkVELUFETUlTU0lCTEUnIGZvciBrIGluIFBSSU0pCiAg
ICBvayAmPSBhbnkobTRbJ2NvbWJpbmVkJ11bJ2V4Y2x1c2lvbiddW2tdW2FdWydjbGFzcyddID09
ICdUVU5FRC1BRE1JU1NJQkxFJyBmb3IgayBpbiBLRVlTIGZvciBhIGluIEFSTVMpCiAgICBzdWl0
ZSgnQy1TWU4tMycsIG9rLCAnS0lMTC9LSUxML1RVTkVEL1RVTkVEKHJvYnVzdG5lc3Mgb25seSk6
ICVzICVzICVzICVzJyAlIChtMVsnZ2F0ZSddWydnYXRlX2NsYXNzJ10sIG0yWydnYXRlJ11bJ2dh
dGVfY2xhc3MnXSwgbTNbJ2dhdGUnXVsnZ2F0ZV9jbGFzcyddLCBtNFsnZ2F0ZSddWydnYXRlX2Ns
YXNzJ10pKQogICAgIyBDLVNZTi00CiAgICBtID0gTS5tYXBfcm93cyhbcm93KC0xLjAsIDEuMCld
LCB3aXRoX3R3b19wYXJhbT1GYWxzZSkKICAgIG9rID0gbVsnZ2F0ZSddWydnYXRlX2NsYXNzJ10g
PT0gJ0lORVJULUlOLUQnIGFuZCBhbGwobVsnY29tYmluZWQnXVsnZmFtaWxpZXMnXVtrXVthXVtm
XVsnY2xhc3MnXSA9PSAnSU5FUlQtSU4tRCcgZm9yIGsgaW4gS0VZUyBmb3IgYSBpbiBBUk1TIGZv
ciBmIGluIE0ubWFwcGVkKGspKQogICAgc3VpdGUoJ0MtU1lOLTQnLCBvaywgbVsnZ2F0ZSddWydn
YXRlX2NsYXNzJ10pCiAgICAjIEMtU1lOLTUKICAgIG0gPSBNLm1hcF9pbnRlcnZhbCgtYigwLjEp
LCBiKDAuMSksIHdpdGhfdHdvX3BhcmFtPUZhbHNlKQogICAgb2sgPSBhbGwobVsnZmFtaWxpZXMn
XVtrXVthXVsndDInXVsnY2xhc3MnXSA9PSAnTlVMTC1JTkVSVCcgZm9yIGsgaW4gUFsnc3RydWN0
dXJlJ11bJ2N1YmljX2tleXMnXSBmb3IgYSBpbiBBUk1TKQogICAgc3VpdGUoJ0MtU1lOLTUnLCBv
aywgJ2N1YmljIHQyIE5VTEwtSU5FUlQnKQogICAgIyBDLVNZTi02IG1hc2tlZCBhYm9ydCBzZXQK
ICAgIG9rLCBkZXQgPSBjc3luNigpCiAgICBzdWl0ZSgnQy1TWU4tNicsIG9rLCBkZXQpCiAgICAj
IEMtU1lOLTcgKE1PTk8gb24gQy1TWU4tMSBpbnRlcnZhbHMpCiAgICB3b3JzdCwgdmlvbCA9IDAu
MCwgMAogICAgZm9yIHQgaW4gQ1snc3ludGhldGljX3QnXToKICAgICAgICBiYXNlID0gTS5tYXBf
cm93cyhbcm93KC1iKHQpLCBiKHQpKV0sIHdpdGhfdHdvX3BhcmFtPUZhbHNlKQogICAgICAgIGZv
ciBmY3QgaW4gKDEwLjAsIDAuMSk6CiAgICAgICAgICAgIHcsIHYgPSBNLm1vbm9fY2hlY2soYmFz
ZSwgTS5tYXBfcm93cyhbcm93KC1iKHQpICogZmN0LCBiKHQpICogZmN0KV0sIHdpdGhfdHdvX3Bh
cmFtPUZhbHNlKSwgZmN0KQogICAgICAgICAgICB3b3JzdCwgdmlvbCA9IG1heCh3b3JzdCwgdyks
IHZpb2wgKyB2CiAgICBzdWl0ZSgnQy1TWU4tNycsIHdvcnN0IDw9IENbJ21vbm9fdG9sX3JlbCdd
IGFuZCB2aW9sID09IDAsICd3b3JzdCBzY2FsaW5nIGRldiAlLjJlLCB2aW9sYXRpb25zICVkJyAl
ICh3b3JzdCwgdmlvbCkpCiAgICAjIEMtU1lOLTggaW50ZXJzZWN0aW9uCiAgICBtID0gTS5tYXBf
cm93cyhbcm93KC1iKDAuMSksIGIoMC4xKSksIHJvdygtYigwLjA1KSwgYigwLjIpKV0sIHdpdGhf
dHdvX3BhcmFtPUZhbHNlKQogICAgcmVmID0gbVsnY29tYmluZWQnXVsnZmFtaWxpZXMnXVsnaGV4
X3N0ZXB8YSddWydFMl9IaWxsJ11bJ3Q0J10KICAgIG9rID0gbVsnY29tYmluZWRfZW1wdHknXSBp
cyBGYWxzZSBhbmQgYWJzKHJlZlsndF9zdGFyJ10gLSAwLjEpIDw9IDFlLTEyIGFuZCByZWZbJ2Jp
bmRpbmdfZW5kJ10gPT0gJ2hpJwogICAgbmVnID0gbVsnY29tYmluZWQnXVsnZmFtaWxpZXMnXVsn
Y3ViaWNfc3RlcHwwMDEnXVsnRTJfSGlsbCddWyd0NCddCiAgICBrYyA9IGFicyhQWydyYXcnXVsn
a2V5cyddWydjdWJpY19zdGVwfDAwMSddWydhcm1zJ11bJ0UyX0hpbGwnXVsndDQnXVsna2FwcGEn
XSkKICAgIG9rICY9IGFicyhuZWdbJ3Rfc3RhciddIC0gbWF0aC5zcXJ0KGIoMC4wNSkgLyBrYykp
IDw9IDFlLTEyICogbmVnWyd0X3N0YXInXQogICAgc3VpdGUoJ0MtU1lOLTgnLCBvaywgJ0kgPSBb
bWF4IGxvLCBtaW4gaGldJykKICAgICMgQy1TWU4tOQogICAgbSA9IE0ubWFwX3Jvd3MoW3Jvdyhi
KDAuMSksIGIoMC4yKSksIHJvdygtYigwLjIpLCAtYigwLjEpKV0sIHdpdGhfdHdvX3BhcmFtPUZh
bHNlKQogICAgc3VpdGUoJ0MtU1lOLTknLCBtWydnYXRlJ11bJ2dhdGVfY2xhc3MnXSA9PSAnQU5D
SE9SLUlOQ09OU0lTVEVOVCcgYW5kIG1bJ2NvbWJpbmVkX2VtcHR5J10gaXMgVHJ1ZSwgbVsnZ2F0
ZSddWydnYXRlX2NsYXNzJ10pCiAgICAjIEMtU1lOLTEwIHJlZ2ltZQogICAga3YgPSBDWydzeW50
aGV0aWNfayddWyd2b2lkJ10KICAgIG0xID0gTS5tYXBfcm93cyhbcm93KC1iKDAuMSksIGIoMC4x
KSwga3YpXSwgd2l0aF90d29fcGFyYW09RmFsc2UpCiAgICBtMiA9IE0ubWFwX3Jvd3MoW3Jvdygt
YigwLjEpLCBiKDAuMSksIGt2KSwgcm93KC1iKDAuMDUpLCBiKDAuMDUpKV0sIHdpdGhfdHdvX3Bh
cmFtPUZhbHNlKQogICAgb2sgPSBtMVsnZ2F0ZSddWydnYXRlX2NsYXNzJ10gPT0gJ1ZPSUQnIGFu
ZCBtMVsnbl92b2lkX3Jvd3MnXSA9PSAxIGFuZCBtMVsncm93cyddWzBdWyd2b2lkX3JlZ2ltZSdd
IGlzIFRydWUKICAgIG9rICY9IG0yWyduX3ZvaWRfcm93cyddID09IDEgYW5kIGFicyhtMlsnY29t
YmluZWQnXVsnZmFtaWxpZXMnXVsnaGV4X3N0ZXB8YSddWydFMl9IaWxsJ11bJ3Q0J11bJ3Rfc3Rh
ciddIC0gMC4wNSkgPD0gMWUtMTIKICAgIHN1aXRlKCdDLVNZTi0xMCcsIG9rLCAnJXM7IG1peGVk
IG5fdm9pZCAlZCcgJSAobTFbJ2dhdGUnXVsnZ2F0ZV9jbGFzcyddLCBtMlsnbl92b2lkX3Jvd3Mn
XSkpCiAgICAjIEMtU1lOLTExCiAgICBtID0gTS5tYXBfcm93cyhbcm93KDAuMCwgMC4wKV0sIHdp
dGhfdHdvX3BhcmFtPUZhbHNlKQogICAgZmFtID0gbVsnY29tYmluZWQnXVsnZmFtaWxpZXMnXQog
ICAgb2sgPSBtWydnYXRlJ11bJ2dhdGVfY2xhc3MnXSA9PSAnV0lORE9XLURFTElWRVJFRCcgYW5k
IGFsbChmYW1ba11bYV1bZl1bJ3Rfc3RhciddID09IDAuMCBhbmQgZmFtW2tdW2FdW2ZdWydudV9p
c19pbmYnXSBhbmQgZmFtW2tdW2FdW2ZdWydudWxsZmxvb3Jfc2Vuc2l0aXZlJ10gYW5kIGZhbVtr
XVthXVtmXVsnY2xhc3MnXSA9PSAnQklORElORycgZm9yIGsgaW4gS0VZUyBmb3IgYSBpbiBBUk1T
IGZvciBmIGluIE0ubWFwcGVkKGspKQogICAgc3VpdGUoJ0MtU1lOLTExJywgb2ssIG1bJ2dhdGUn
XVsnZ2F0ZV9jbGFzcyddKQogICAgIyBDLVNZTi0xMgogICAgdCA9IENbJ3N5bnRoZXRpY190X3Rp
Z2h0J10KICAgIG0gPSBNLm1hcF9pbnRlcnZhbCgtYih0KSwgYih0KSwgd2l0aF90d29fcGFyYW09
RmFsc2UpCiAgICBvaywgZmlyZWQsIGNsZWFyID0gVHJ1ZSwgMCwgMAogICAgZm9yIGsgaW4gS0VZ
UzoKICAgICAgICBmb3IgYSBpbiBBUk1TOgogICAgICAgICAgICBmb3IgZiBpbiBNLm1hcHBlZChr
KToKICAgICAgICAgICAgICAgIGUgPSBtWydmYW1pbGllcyddW2tdW2FdW2ZdCiAgICAgICAgICAg
ICAgICB3YW50ID0gYWJzKERWWydmYW1pbGllcyddW2tdW2FdW2ZdWydTX2JpJ10pICogZVsndF9z
dGFyJ10gLyBiKHQpID4gQ1snbnVsbGZsb29yX3RocmVzaG9sZCddCiAgICAgICAgICAgICAgICBv
ayAmPSBlWydudWxsZmxvb3Jfc2Vuc2l0aXZlJ10gPT0gd2FudAogICAgICAgICAgICAgICAgZmly
ZWQgKz0gd2FudDsgY2xlYXIgKz0gKG5vdCB3YW50KQogICAgc3VpdGUoJ0MtU1lOLTEyJywgb2sg
YW5kIGZpcmVkID49IDEgYW5kIGNsZWFyID49IDEsICdmbGFnIGZpcmVzIG9uICVkIGNlbGxzLCBj
bGVhciBvbiAlZCcgJSAoZmlyZWQsIGNsZWFyKSkKICAgICMgQy1TWU4tMTMKICAgIG9rLCBkZXQg
PSBUcnVlLCBbXQogICAgZm9yIG5hbWUgaW4gKCdtYXJnaW5fcG9zaXRpdmUnLCAnbWFyZ2luX25l
Z2F0aXZlJyk6CiAgICAgICAgbSA9IE0ubWFwX3Jvd3MoW3JvdygqRFZbJ3N5bnRoZXRpYyddW25h
bWVdKV0sIHdpdGhfdHdvX3BhcmFtPUZhbHNlKQogICAgICAgIGNscyA9IFttWydjb21iaW5lZCdd
WydleGNsdXNpb24nXVtrXVthXVsnY2xhc3MnXSBmb3IgayBpbiBLRVlTIGZvciBhIGluIEFSTVNd
CiAgICAgICAgb2sgJj0gbVsnZ2F0ZSddWydnYXRlX2NsYXNzJ10gPT0gJ01BUkdJTi1PTkxZJyBh
bmQgJ1RVTkVELUFETUlTU0lCTEUnIG5vdCBpbiBjbHMgYW5kICdNQVJHSU4nIGluIGNscwogICAg
ICAgIGRldC5hcHBlbmQoJyVzICVzJyAlIChuYW1lLCBtWydnYXRlJ11bJ2dhdGVfY2xhc3MnXSkp
CiAgICBzdWl0ZSgnQy1TWU4tMTMnLCBvaywgJzsgJy5qb2luKGRldCkpCiAgICAjIEMtU1lOLTE0
IGdyaWQgbm9pc2UgYXQgemVybwogICAgUGMgPSBqc29uLmxvYWRzKGpzb24uZHVtcHMoUCkpCiAg
ICBnID0gUGNbJ3JhdyddWydrZXlzJ11bJ2N1YmljX3N0ZXB8MDAxJ11bJ2FybXMnXVsnRTJfSGls
bCddWyd0NCddWydncmlkJ10KICAgIGdbUGNbJ2dyaWRzJ11bJ3RfZ3JpZCddLmluZGV4KDAuMDIp
XSArPSA1ZS0xMwogICAgRFZjID0gcmVkZXJpdmUoUGMpCiAgICBodWxsID0gRFZjWydyZWFjaCdd
WydjdWJpY19zdGVwfDAwMSddWydFMl9IaWxsJ11bJ2h1bGwnXQogICAgTWMgPSBNYXBwZXIoUGMs
IERWYykKICAgIGV4ID0gTWMuZXhjbHVzaW9uKCdjdWJpY19zdGVwfDAwMScsICdFMl9IaWxsJywg
MWUtNiwgMmUtNikKICAgIHN1aXRlKCdDLVNZTi0xNCcsIGh1bGxbMV0gPT0gMC4wIGFuZCBleFsn
Y2xhc3MnXSA9PSAnRVhDTFVERUQtSU4tRCcgYW5kIGV4WydzdWJyZWFzb24nXSA9PSAnU0lHTics
ICdzbmFwcGVkIGh1bGwgaGkgPT0gMDsgU0lHTicpCiAgICByZXR1cm4gUgoKCmRlZiBjc3luNigp
OgogICAgIiIidGhlIGZpZnRlZW4gbWFsZm9ybWVkIGZpbGVzIG9mIG1lbW8gNC43IGFuZCBvbmUg
dmFsaWQgZmlsZSwgd2l0aCBkaXN0aW5jdGl2ZSBzeW50aGV0aWMgdmFsdWVzOyBldmVyeSBtYWxm
b3JtZWQgZmlsZSBtdXN0CiAgICBhYm9ydCB3aXRoIGEgcmVhc29uIGNvZGU7IG5vIHN5bnRoZXRp
YyB2YWx1ZSBtYXkgYXBwZWFyIGluIGFueSByZWFzb24gY29kZSBvciBpbiB0aGUgbG9nIiIiCiAg
ICBWID0gWyctMC4wMDAxMjM0NTY3ODknLCAnMC4wMDA5ODc2NTQzMjEnLCAnMTIzNDU2Ljc4OScs
ICc5ODc2NS40MzIxJ10gICAjIHN5bnRoZXRpYyB2YWx1ZXMgKG5ldmVyIGFuY2hvcnMpCiAgICBn
b29kID0gJ2lkPVNBLTEgfCBjbGFzcz1zcGQgfCBkZWx0YV9kZWY9dGVuc29yX292ZXJfRU1fbWlu
dXNfMSB8IGxvPSVzIHwgaGk9JXMgfCBjbD0wLjkgfCByZWFkaW5nPWJvdW5kIHwgZ2VvbT1zaW5n
bGUgfCBrX2VtX21heD0lcyB8IGtfdF9tYXg9JXMgfCBzcmM9c3ludGhldGljIHNvdXJjZVxuJyAl
IHR1cGxlKFYpCiAgICBiYWQgPSB7CiAgICAgICAgJ2NybGYnOiBnb29kLnJlcGxhY2UoJ1xuJywg
J1xyXG4nKSwgJ2JvbSc6ICfvu78nICsgZ29vZCwgJ3RyYWlsaW5nX2JsYW5rJzogZ29vZCArICdc
bicsCiAgICAgICAgJ2Zvcm1mZWVkX2luX3NyYyc6IGdvb2QucmVwbGFjZSgnc3ludGhldGljIHNv
dXJjZScsICdzeW50aGV0aWNceDBjc291cmNlJyksICd1MjAyOF9pbl9zcmMnOiBnb29kLnJlcGxh
Y2UoJ3N5bnRoZXRpYyBzb3VyY2UnLCAnc3ludGhldGlj4oCoc291cmNlJyksCiAgICAgICAgJ3Vu
aWNvZGVfbWludXMnOiBnb29kLnJlcGxhY2UoJ2xvPS0wLjAwMDEyMzQ1Njc4OScsICdsbz3iiJIw
LjAwMDEyMzQ1Njc4OScpLCAnc3VwZXJzY3JpcHQnOiBnb29kLnJlcGxhY2UoJ2hpPTAuMDAwOTg3
NjU0MzIxJywgJ2hpPTkuODc2NTQzMjHDlzEw4oG74oG0JyksCiAgICAgICAgJ2Jhcl9pbl9zcmMn
OiBnb29kLnJlcGxhY2UoJ3N5bnRoZXRpYyBzb3VyY2UnLCAnc3ludGhldGljIHwgc291cmNlJyks
ICdsb19ndF9oaSc6IGdvb2QucmVwbGFjZSgnbG89LTAuMDAwMTIzNDU2Nzg5JywgJ2xvPTAuNScp
LAogICAgICAgICdyZWFkaW5nX2NlaWxpbmcnOiBnb29kLnJlcGxhY2UoJ3JlYWRpbmc9Ym91bmQn
LCAncmVhZGluZz1jZWlsaW5nJyksICd3cm9uZ19kZWx0YV9kZWYnOiBnb29kLnJlcGxhY2UoJ3Rl
bnNvcl9vdmVyX0VNX21pbnVzXzEnLCAnRU1fb3Zlcl90ZW5zb3JfbWludXNfMScpLAogICAgICAg
ICdtaXNzaW5nX2tleSc6IGdvb2QucmVwbGFjZSgnIHwgZ2VvbT1zaW5nbGUnLCAnJyksICd3cm9u
Z19pZCc6IGdvb2QucmVwbGFjZSgnaWQ9U0EtMScsICdpZD1TQS0yJyksCiAgICAgICAgJ2R1cGxp
Y2F0ZV9rZXknOiBnb29kLnJlcGxhY2UoJyB8IHNyYz0nLCAnIHwgY2w9MC44IHwgc3JjPScpLCAn
cGVyY2VudF9jbCc6IGdvb2QucmVwbGFjZSgnY2w9MC45JywgJ2NsPTkwJScpLAogICAgfQogICAg
b2ssIGNvZGVzID0gVHJ1ZSwge30KICAgIGZvciBuYW1lLCB0ZXh0IGluIGJhZC5pdGVtcygpOgog
ICAgICAgIHRyeToKICAgICAgICAgICAgcGFyc2Vfc2VhbGVkKHRleHQuZW5jb2RlKCd1dGYtOCcp
KQogICAgICAgICAgICBvayA9IEZhbHNlOyBjb2Rlc1tuYW1lXSA9ICdBQ0NFUFRFRCcKICAgICAg
ICBleGNlcHQgTWFza2VkQWJvcnQgYXMgZToKICAgICAgICAgICAgY29kZXNbbmFtZV0gPSBzdHIo
ZSkKICAgIHRyeToKICAgICAgICByb3dzLCBjZW5zdXMsIG1kNXMgPSBwYXJzZV9zZWFsZWQoZ29v
ZC5lbmNvZGUoJ3V0Zi04JykpCiAgICAgICAgb2sgJj0gY2Vuc3VzID09IHsncm93cyc6IDEsICdw
ZXJfY2xhc3MnOiB7J3NwZCc6IDF9LCAnZmllbGRzX3Blcl9yb3cnOiBbMTFdfQogICAgZXhjZXB0
IE1hc2tlZEFib3J0IGFzIGU6CiAgICAgICAgb2sgPSBGYWxzZTsgY29kZXNbJ3ZhbGlkJ10gPSBz
dHIoZSkKICAgIGxlYWsgPSBhbnkodiBpbiBjIGZvciB2IGluIFYgZm9yIGMgaW4gY29kZXMudmFs
dWVzKCkpIG9yIGFueSh2IGluIGwgZm9yIHYgaW4gViBmb3IgbCBpbiBMT0cpCiAgICByZXR1cm4g
b2sgYW5kIG5vdCBsZWFrIGFuZCBsZW4oYmFkKSA9PSAxNSwgJzE1IG1hbGZvcm1lZCBmaWxlcyBh
Ym9ydGVkOiAlczsgdmFsaWQgZmlsZSBjZW5zdXMgY29uZmlybWVkOyBsZWFrICVzJyAlICgnLCAn
LmpvaW4oc29ydGVkKGNvZGVzKSksICdOT05FJyBpZiBub3QgbGVhayBlbHNlICdERVRFQ1RFRCcp
CgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gY2hlY2twb2ludApkZWYgd3Jp
dGVfY2hlY2twb2ludChjaywgcGF0aCwgcGF0aHMsIGExKToKICAgIGRhdGEgPSAoanNvbi5kdW1w
cyhjaywgaW5kZW50PTEsIHNvcnRfa2V5cz1UcnVlLCBlbnN1cmVfYXNjaWk9VHJ1ZSwgYWxsb3df
bmFuPUZhbHNlKSArICdcbicpLmVuY29kZSgnYXNjaWknKQogICAgb3BlbihwYXRoLCAnd2InKS53
cml0ZShkYXRhKQogICAgc2MgPSB0MV9zY2FuKHBhdGhzLCBbcGF0aF0sIGExKQogICAgaWYgc2Nb
J2hpdHMnXToKICAgICAgICBvcy5yZW1vdmUocGF0aCkKICAgICAgICByYWlzZSBIYWx0KCdUMSBw
b3N0LXdyaXRlOiAlZCBoaXQocykgaW4gdGhlIGNoZWNrcG9pbnQgYnkgaW5kZXggJXMgLS0gY2hl
Y2twb2ludCBkZWxldGVkJyAlIChzY1snaGl0cyddLCBzY1sncGVyX2ZpbGUnXSkpCiAgICBja1sn
VDFfcG9zdF93cml0ZSddID0geydoaXRzJzogc2NbJ2hpdHMnXSwgJ2NvbGxpc2lvbnMnOiBzY1sn
Y29sbGlzaW9ucyddLCAncGF0dGVybnMnOiBzY1sncGF0dGVybnMnXSwgJ2ExX2luY2x1ZGVkJzog
c2NbJ2ExX2luY2x1ZGVkJ119CiAgICBkYXRhID0gKGpzb24uZHVtcHMoY2ssIGluZGVudD0xLCBz
b3J0X2tleXM9VHJ1ZSwgZW5zdXJlX2FzY2lpPVRydWUsIGFsbG93X25hbj1GYWxzZSkgKyAnXG4n
KS5lbmNvZGUoJ2FzY2lpJykKICAgIG9wZW4ocGF0aCwgJ3diJykud3JpdGUoZGF0YSkKICAgIHNj
MiA9IHQxX3NjYW4ocGF0aHMsIFtwYXRoXSwgYTEpCiAgICBpZiBzYzJbJ2hpdHMnXToKICAgICAg
ICBvcy5yZW1vdmUocGF0aCkKICAgICAgICByYWlzZSBIYWx0KCdUMSBwb3N0LXdyaXRlIChzZWNv
bmQgc2Nhbik6IGhpdHMnKQogICAgcmV0dXJuIG1kNWIoZGF0YSksIGxlbihkYXRhKQoKCmRlZiBt
YWluKCk6CiAgICBhcmdzID0gc3lzLmFyZ3ZbMTpdCiAgICBpZiBub3QgYXJncyBvciBhcmdzWzBd
IG5vdCBpbiAoJ3ByZXJlYWQnLCAncmVhZCcsICdjZW5zdXMnKToKICAgICAgICBwcmludChfX2Rv
Y19fKTsgcmV0dXJuIDIKICAgIG1vZGUgPSBhcmdzWzBdCiAgICBvcHQgPSBsYW1iZGEgbiwgZD1O
b25lOiBhcmdzW2FyZ3MuaW5kZXgobikgKyAxXSBpZiBuIGluIGFyZ3MgZWxzZSBkCiAgICBvdXRk
aXIgPSBvcHQoJy0tb3V0JywgSEVSRSkKICAgIHRyeToKICAgICAgICBpZiBtb2RlID09ICdjZW5z
dXMnOgogICAgICAgICAgICByb3dzLCBjZW5zdXMsIG1kNXMsIHNtZDUsIHNieXRlcyA9IG9wZW5f
c2VhbGVkKG9wdCgnLS1zZWFsZWQnKSwgb3B0KCctLW1kNScpLCBvcHQoJy0tYnl0ZXMnKSkKICAg
ICAgICAgICAgc2F5KCdzZWFsZWQ6IG1kNSAlcyAgYnl0ZXMgJWQgIGNlbnN1cyAlcyAgcm93IG1k
NXMgJXMnICUgKHNtZDUsIHNieXRlcywganNvbi5kdW1wcyhjZW5zdXMsIHNvcnRfa2V5cz1UcnVl
KSwgbWQ1cykpCiAgICAgICAgICAgIHJldHVybiAwCiAgICAgICAgcmVwbywgYTEgPSBvcHQoJy0t
cmVwbycpLCBvcHQoJy0tYTEnKQogICAgICAgIGlmIG5vdCByZXBvOgogICAgICAgICAgICByYWlz
ZSBIYWx0KCctLXJlcG8gcmVxdWlyZWQnKQogICAgICAgIGlmIG1vZGUgPT0gJ3JlYWQnIGFuZCBu
b3QgYTE6CiAgICAgICAgICAgIHJhaXNlIEhhbHQoJy0tYTEgcmVxdWlyZWQgZm9yIHRoZSByZWFk
IChGLUNUUkwtU0EtVDEgdW5kZXIgYmFzZSDiiKogc3RyYXR1bSDiiKogQTEpJykKICAgICAgICBw
YXRocyA9IGd1YXJkcygpCiAgICAgICAgUCA9IGpzb24ubG9hZHMob3BlbihwYXRoc1sncGluJ10s
ICdyYicpLnJlYWQoKS5kZWNvZGUoJ2FzY2lpJykpCiAgICAgICAgRFYgPSByZWRlcml2ZShQKQog
ICAgICAgIE0gPSBNYXBwZXIoUCwgRFYpCiAgICAgICAgaW5zdF9tZDUgPSBtZDVmKG9zLnBhdGgu
YWJzcGF0aChfX2ZpbGVfXykpCiAgICAgICAgc2F5KCclcyAlcyBsZWcgLS0gaW5zdHJ1bWVudCBt
ZDUgJXM7IHBpbm5lZCAlczsgbWVtbyAlczsgbG9jayByZWNvcmQgJXMnICUgKEdBVEUsIExFRywg
aW5zdF9tZDUsIFBJTl9NRDUsIE1FTU9fTUQ1LCBMT0NLX01ENSkpCiAgICAgICAgY2sgPSB7J2dh
dGUnOiBHQVRFLCAnbGVnJzogTEVHLCAndXRjJzogZGF0ZXRpbWUuZGF0ZXRpbWUudXRjbm93KCku
c3RyZnRpbWUoJyVZLSVtLSVkVCVIOiVNOiVTWicpLCAnaW5zdHJ1bWVudF9tZDUnOiBpbnN0X21k
NSwKICAgICAgICAgICAgICAnbWVtb19sb2NrX21kNSc6IE1FTU9fTUQ1LCAnbWVtb19sb2NrX2J5
dGVzJzogTUVNT19CWVRFUywgJ2xvY2tfcmVjb3JkX21kNSc6IExPQ0tfTUQ1LCAncGlubmVkX2lu
cHV0c19tZDUnOiBQSU5fTUQ1LAogICAgICAgICAgICAgICdidWlsZGVyX21kNSc6IEJVSUxERVJf
TUQ1LCAndmVyaWZpZXJfbWQ1JzogVkVSSUZJRVJfTUQ1LCAndDFfbGlzdF9tZDUnOiBUMV9NRDUs
ICd0MV9hMV9tZDUnOiBtZDVmKGExKSBpZiBhMSBlbHNlIE5vbmUsCiAgICAgICAgICAgICAgJ3Nj
YW5uZXJfbWQ1JzogU0NBTk5FUl9NRDUsICdzY2hlbWFfbWQ1JzogU0NIRU1BX01ENSwgJ2NvbXBh
cmF0b3JfbWQ1JzogQ09NUEFSQVRPUl9NRDUsICdsZWRnZXJfYmFzZV9tZDUnOiBMRURHRVJfTUQ1
LCAnZWxlY3Rpb25zJzogRUxFQ1RJT05TLAogICAgICAgICAgICAgICdncmlkcyc6IGdyaWRfY291
bnRzKFApLCAncGhhc2UwJzogTm9uZSwgJ251bGxzJzogTm9uZSwgJ3BoYXNlMic6IE5vbmUsICdw
aGFzZTMnOiBOb25lfQogICAgICAgICMgUGhhc2UgMAogICAgICAgIFAwID0gcGhhc2UwKFAsIERW
LCBNLCBwYXRocywgcmVwbywgYTEpCiAgICAgICAgY2tbJ3BoYXNlMCddID0gUDAKICAgICAgICBj
a1snbnVsbHMnXSA9IERWWydudWxscyddCiAgICAgICAgZm9yIGl0ZW0sIGUgaW4gUDAuaXRlbXMo
KToKICAgICAgICAgICAgc2F5KCcgIFBoYXNlIDAgJS0yMnMgJXMnICUgKGl0ZW0sICdQQVNTJyBp
ZiBlWydwYXNzZWQnXSBlbHNlICdGQUlMJykpCiAgICAgICAgaWYgbm90IGFsbChlWydwYXNzZWQn
XSBmb3IgZSBpbiBQMC52YWx1ZXMoKSk6CiAgICAgICAgICAgIGNrWyd2ZXJkaWN0J10gPSAnSU5E
RVRFUk1JTkFURScKICAgICAgICAgICAgd3JpdGVfY2hlY2twb2ludChjaywgb3MucGF0aC5qb2lu
KG91dGRpciwgJ2dfbXNjc19hX2NoYXRsZWdfcHJlcmVhZGNoZWNrcG9pbnQuanNvbicpLCBwYXRo
cywgYTEpCiAgICAgICAgICAgIHJhaXNlIEhhbHQoJ1BoYXNlIDAgZmFpbHVyZSAtPiBJTkRFVEVS
TUlOQVRFJykKICAgICAgICAjIFBoYXNlIDIKICAgICAgICBQMiA9IHBoYXNlMihQLCBEViwgTSkK
ICAgICAgICBja1sncGhhc2UyJ10gPSBQMgogICAgICAgIGZvciBzLCBlIGluIFAyLml0ZW1zKCk6
CiAgICAgICAgICAgIHNheSgnICBQaGFzZSAyICUtOXMgJXMnICUgKHMsICdQQVNTJyBpZiBlWydw
YXNzZWQnXSBlbHNlICdGQUlMJykpCiAgICAgICAgaWYgbm90IGFsbChlWydwYXNzZWQnXSBmb3Ig
ZSBpbiBQMi52YWx1ZXMoKSk6CiAgICAgICAgICAgIHdyaXRlX2NoZWNrcG9pbnQoY2ssIG9zLnBh
dGguam9pbihvdXRkaXIsICdnX21zY3NfYV9jaGF0bGVnX3ByZXJlYWRjaGVja3BvaW50Lmpzb24n
KSwgcGF0aHMsIGExKQogICAgICAgICAgICByYWlzZSBIYWx0KCdQaGFzZSAyIGZhaWx1cmUgLS0g
bm8gc2VhbGVkIG9wZW4nKQogICAgICAgIGlmIG1vZGUgPT0gJ3ByZXJlYWQnOgogICAgICAgICAg
ICBoLCBuID0gd3JpdGVfY2hlY2twb2ludChjaywgb3MucGF0aC5qb2luKG91dGRpciwgJ2dfbXNj
c19hX2NoYXRsZWdfcHJlcmVhZGNoZWNrcG9pbnQuanNvbicpLCBwYXRocywgYTEpCiAgICAgICAg
ICAgIHNheSgncHJlLXJlYWQgY2hlY2twb2ludCB3cml0dGVuOiBtZDUgJXMgICVkIEIgIChwaGFz
ZTMgPSBudWxsKScgJSAoaCwgbikpCiAgICAgICAgICAgIHJldHVybiAwCiAgICAgICAgIyBQaGFz
ZSAzCiAgICAgICAgdHJ5OgogICAgICAgICAgICByb3dzLCBjZW5zdXMsIG1kNXMsIHNtZDUsIHNi
eXRlcyA9IG9wZW5fc2VhbGVkKG9wdCgnLS1zZWFsZWQnKSwgb3B0KCctLW1kNScpLCBvcHQoJy0t
Ynl0ZXMnKSkKICAgICAgICBleGNlcHQgTWFza2VkQWJvcnQgYXMgZToKICAgICAgICAgICAgc2F5
KCdNQVNLRUQgQUJPUlQgKHRoZSByZWFkIG5vdCBzcGVudCk6ICVzJyAlIGUpCiAgICAgICAgICAg
IHJldHVybiAxCiAgICAgICAgc2F5KCdzZWFsZWQ6IG1kNSAlcyAgYnl0ZXMgJWQgIGNlbnN1cyAl
cycgJSAoc21kNSwgc2J5dGVzLCBqc29uLmR1bXBzKGNlbnN1cywgc29ydF9rZXlzPVRydWUpKSkK
ICAgICAgICBwMyA9IE0uZnVsbChbeydsbyc6IHJbJ2xvJ10sICdoaSc6IHJbJ2hpJ10sICdrZW0n
OiByWydrZW0nXSwgJ2t0Jzogclsna3QnXX0gZm9yIHIgaW4gcm93c10pCiAgICAgICAgZm9yIGks
IHIgaW4gZW51bWVyYXRlKHAzWydyb3dzJ10pOgogICAgICAgICAgICByWydpZCddID0gJ1NBLSVk
JyAlIChpICsgMSk7IHJbJ3Jvd19tZDUnXSA9IG1kNXNbaV07IHJbJ2dlb20nXSA9IHJvd3NbaV1b
J2dlb20nXTsgclsncSddID0gcm93c1tpXVsncSddCiAgICAgICAgcDMudXBkYXRlKHsnc2VhbGVk
X21kNSc6IHNtZDUsICdzZWFsZWRfYnl0ZXMnOiBzYnl0ZXMsICdjZW5zdXMnOiBjZW5zdXMsICdy
b3dfbWQ1cyc6IG1kNXMsICd0MV9hMV9tZDUnOiBtZDVmKGExKX0pCiAgICAgICAgY2tbJ3BoYXNl
MyddID0gcDMKICAgICAgICBja1sndmVyZGljdCddID0gcDNbJ2dhdGUnXVsnZ2F0ZV9jbGFzcydd
CiAgICAgICAgaCwgbiA9IHdyaXRlX2NoZWNrcG9pbnQoY2ssIG9zLnBhdGguam9pbihvdXRkaXIs
ICdnX21zY3NfYV9jaGF0bGVnX2NoZWNrcG9pbnQuanNvbicpLCBwYXRocywgYTEpCiAgICAgICAg
c2F5KCdnYXRlIGNsYXNzOiAlcyAgKE9PTSB4MTAgJXMsIHgwLjEgJXM7IHJvYnVzdCAlcyknICUg
KHAzWydnYXRlJ11bJ2dhdGVfY2xhc3MnXSwgcDNbJ2dhdGUnXVsnb29tX2NsYXNzX3gxMCddLCBw
M1snZ2F0ZSddWydvb21fY2xhc3NfeDBwMSddLCBwM1snZ2F0ZSddWydvb21fcm9idXN0J10pKQog
ICAgICAgIHNheSgnY2hlY2twb2ludCB3cml0dGVuOiBtZDUgJXMgICVkIEInICUgKGgsIG4pKQog
ICAgICAgIHJldHVybiAwCiAgICBleGNlcHQgSGFsdCBhcyBlOgogICAgICAgIHNheSgnSEFMVDog
JXMnICUgZSkKICAgICAgICByZXR1cm4gMQoKCmlmIF9fbmFtZV9fID09ICdfX21haW5fXyc6CiAg
ICBzeXMuZXhpdChtYWluKCkpCg==
=====END-EMBED name=g_mscs_a_chatleg.py=====

=====BEGIN-EMBED name=g_mscs_a_chatleg_prereadcheckpoint.json md5=ccbb32077996833cdac2339938193ec1 bytes=13842 encoding=base64 armor_bytes=18699 QUARANTINED=====
ewogIlQxX3Bvc3Rfd3JpdGUiOiB7CiAgImExX2luY2x1ZGVkIjogZmFsc2UsCiAgImNvbGxpc2lv
bnMiOiAxLAogICJoaXRzIjogMCwKICAicGF0dGVybnMiOiAzNgogfSwKICJidWlsZGVyX21kNSI6
ICI4MTg5MTAwZWRlODBlYWMzNjBiMjVhMTQ2ZTU4MGFiZiIsCiAiY29tcGFyYXRvcl9tZDUiOiAi
YzViNGE3YWFiMmZjODY1MWJlNmQyNmQxZjNkMjU2NDIiLAogImVsZWN0aW9ucyI6IHsKICAiRS1T
QS0wIjogImEiLAogICJFLVNBLTEiOiAiYSIsCiAgIkUtU0EtMTAiOiAiYSIsCiAgIkUtU0EtMTEi
OiAiYSIsCiAgIkUtU0EtMiI6ICJhIiwKICAiRS1TQS0zIjogImEiLAogICJFLVNBLTQiOiAiYSIs
CiAgIkUtU0EtNSI6ICJhIiwKICAiRS1TQS02IjogImEiLAogICJFLVNBLTciOiAiMDUzMDIyMTAr
TVNDUzFzdHJhdHVtIiwKICAiRS1TQS04IjogImEiLAogICJFLVNBLTkiOiAiYSIKIH0sCiAiZ2F0
ZSI6ICJHLU1TQ1MtQSIsCiAiZ3JpZHMiOiB7CiAgIkQiOiAwLjI1LAogICJhcmVhX25vZGVzX3Bl
cl9heGlzIjogMjAxLAogICJuX2FyZWFfZ3JpZCI6IDQwNDAxLAogICJuX2ZpdF93aW5kb3dfaW5j
bHVzaXZlIjogOSwKICAibl9maXRfd2luZG93X3N0cmljdCI6IDcsCiAgIm5fdDJ0NF9heGlzIjog
NSwKICAibl90MnQ0X2dyaWQiOiAyNSwKICAibl90X2dyaWQiOiAxMiwKICAibl93aW5kb3dfMHAx
X2luY2x1c2l2ZSI6IDcsCiAgIm5fd2luZG93XzBwMV9zdHJpY3QiOiA1LAogICJ0MnQ0X2F4aXMi
OiBbCiAgIC0wLjI1LAogICAtMC4xMjUsCiAgIDAuMCwKICAgMC4xMjUsCiAgIDAuMjUKICBdLAog
ICJ0X2dyaWQiOiBbCiAgIC0wLjUsCiAgIC0wLjI1LAogICAtMC4xLAogICAtMC4wNSwKICAgLTAu
MDIsCiAgIDAuMCwKICAgMC4wMiwKICAgMC4wNSwKICAgMC4xLAogICAwLjI1LAogICAwLjUsCiAg
IDEuMAogIF0KIH0sCiAiaW5zdHJ1bWVudF9tZDUiOiAiMGQwZTVlY2Y2MTBiMzRmMjFlOGMyMmRk
MzkzOGNlNDAiLAogImxlZGdlcl9iYXNlX21kNSI6ICJkNGM0MmE1M2NiZDZkMzI1ZWJjNzQwODc5
Mjg4ZTg0NCIsCiAibGVnIjogImNoYXQiLAogImxvY2tfcmVjb3JkX21kNSI6ICI4MTE2Y2M2MjIy
NzliNWQ0ZTczMjE0MTc4YWU5N2NkOCIsCiAibWVtb19sb2NrX2J5dGVzIjogMTIxOTUwLAogIm1l
bW9fbG9ja19tZDUiOiAiNmVhMTZiOTUyZGI4MzViYjM1MWQzZGMxYjQ3NGM2ZWQiLAogIm51bGxz
IjogewogICJOLTEiOiB7CiAgICJjdWJpY19nZW04fDAwMS9FMl9IU21lYW4vdDQiOiB7CiAgICAi
YmkiOiAtMi41MDU0MDMyOTIyMzc0MzY0ZS0xMywKICAgICJmaXQiOiBudWxsLAogICAgIm9kZl9y
ZWFkaW5nIjogImN1Yks0IgogICB9LAogICAiY3ViaWNfZ2VtOHwwMDEvRTJfSGlsbC90NCI6IHsK
ICAgICJiaSI6IC0yLjE3MzA3NjUzMzUzMjk3M2UtMTIsCiAgICAiZml0IjogLTQuMjY3MTY4MjI5
MDIxODk2ZS0xMSwKICAgICJvZGZfcmVhZGluZyI6ICJjdWJLNCIKICAgfSwKICAgImN1YmljX2dl
bTh8MDAxL2hfSGlsbC90NCI6IHsKICAgICJiaSI6IC0xLjIxMTgwODQzMTM3ODM1ODRlLTEyLAog
ICAgImZpdCI6IC0yLjM4NTI4MTczNDc4OTgwOWUtMTEsCiAgICAib2RmX3JlYWRpbmciOiAiY3Vi
SzQiCiAgIH0sCiAgICJjdWJpY19nZW04fDExMS9FMl9IU21lYW4vdDQiOiB7CiAgICAiYmkiOiAx
LjczOTM0OTQwNTI0NjA3ODdlLTEzLAogICAgImZpdCI6IG51bGwsCiAgICAib2RmX3JlYWRpbmci
OiAiY3ViSzQiCiAgIH0sCiAgICJjdWJpY19nZW04fDExMS9FMl9IaWxsL3Q0IjogewogICAgImJp
IjogMS40NTA2OTE0MTg4NDM1Mzc4ZS0xMiwKICAgICJmaXQiOiAyLjg0NDc2OTc2NDAxNzk4NzZl
LTExLAogICAgIm9kZl9yZWFkaW5nIjogImN1Yks0IgogICB9LAogICAiY3ViaWNfZ2VtOHwxMTEv
aF9IaWxsL3Q0IjogewogICAgImJpIjogLTEuMjExODA4NDMxMzc4MzU4NGUtMTIsCiAgICAiZml0
IjogLTIuMzg1MjgxNzM0Nzg5ODA5ZS0xMSwKICAgICJvZGZfcmVhZGluZyI6ICJjdWJLNCIKICAg
fSwKICAgImN1YmljX3N0ZXB8MDAxL0UyX0hTbWVhbi90NCI6IHsKICAgICJiaSI6IC0xLjA0NzMx
MDM4NjU2MzA2NDRlLTEzLAogICAgImZpdCI6IG51bGwsCiAgICAib2RmX3JlYWRpbmciOiAiY3Vi
SzQiCiAgIH0sCiAgICJjdWJpY19zdGVwfDAwMS9FMl9IaWxsL3Q0IjogewogICAgImJpIjogLTku
OTU2ODUwMTU5MTc5OTQ2ZS0xMywKICAgICJmaXQiOiAtMS45NTQ5Njc4OTQ2MjYwNTk4ZS0xMSwK
ICAgICJvZGZfcmVhZGluZyI6ICJjdWJLNCIKICAgfSwKICAgImN1YmljX3N0ZXB8MDAxL2hfSGls
bC90NCI6IHsKICAgICJiaSI6IC01Ljk2NTU5ODM4NTY1MjUwN2UtMTMsCiAgICAiZml0IjogLTEu
MTY5NDg5ODYxMDM3NzUxOGUtMTEsCiAgICAib2RmX3JlYWRpbmciOiAiY3ViSzQiCiAgIH0sCiAg
ICJjdWJpY19zdGVwfDExMS9FMl9IU21lYW4vdDQiOiB7CiAgICAiYmkiOiA2LjU1MDMxNTg0NTI4
ODQyNGUtMTQsCiAgICAiZml0IjogbnVsbCwKICAgICJvZGZfcmVhZGluZyI6ICJjdWJLNCIKICAg
fSwKICAgImN1YmljX3N0ZXB8MTExL0UyX0hpbGwvdDQiOiB7CiAgICAiYmkiOiA2LjY1MDIzNTkx
NzUwNDY4OGUtMTMsCiAgICAiZml0IjogMS4zMDM1NDE2NDA1ODMzMzQ0ZS0xMSwKICAgICJvZGZf
cmVhZGluZyI6ICJjdWJLNCIKICAgfSwKICAgImN1YmljX3N0ZXB8MTExL2hfSGlsbC90NCI6IHsK
ICAgICJiaSI6IC01Ljk2NTU5ODM4NTY1MjUwN2UtMTMsCiAgICAiZml0IjogLTEuMTY5NDg5ODYx
MDM3NzUxOGUtMTEsCiAgICAib2RmX3JlYWRpbmciOiAiY3ViSzQiCiAgIH0sCiAgICJoZXhfZ2Vt
OHxhL0UyX0hTbWVhbi90MiI6IHsKICAgICJiaSI6IDIuMjAxOTQyMzMyMTczMjI3MmUtMTQsCiAg
ICAiZml0IjogbnVsbCwKICAgICJvZGZfcmVhZGluZyI6ICJoZXhQMiIKICAgfSwKICAgImhleF9n
ZW04fGEvRTJfSFNtZWFuL3Q0IjogewogICAgImJpIjogLTEuMTEwMjIzMDI0NjI1MTU2NWUtMTUs
CiAgICAiZml0IjogbnVsbCwKICAgICJvZGZfcmVhZGluZyI6ICJoZXhQNCIKICAgfSwKICAgImhl
eF9nZW04fGEvRTJfSGlsbC90MiI6IHsKICAgICJiaSI6IDIuNjA5MDI0MTA3ODY5MTE4ZS0xNCwK
ICAgICJmaXQiOiA0Ljg5NDY0MjM2NTE0NTM5NmUtMTMsCiAgICAib2RmX3JlYWRpbmciOiAiaGV4
UDIiCiAgIH0sCiAgICJoZXhfZ2VtOHxhL0UyX0hpbGwvdDQiOiB7CiAgICAiYmkiOiAtOS45OTIw
MDcyMjE2MjY0MDllLTE1LAogICAgImZpdCI6IC0yLjY1MjA0NjM3NDU1MTQ2NGUtMTMsCiAgICAi
b2RmX3JlYWRpbmciOiAiaGV4UDQiCiAgIH0sCiAgICJoZXhfZ2VtOHxhL2hfSGlsbC90MiI6IHsK
ICAgICJiaSI6IDEuMjk1MjYwMTk1Mzk2MDE1OWUtMTUsCiAgICAiZml0IjogMS45ODQ5MjUyNzU5
NDI2ODM2ZS0xNCwKICAgICJvZGZfcmVhZGluZyI6ICJoZXhQMiIKICAgfSwKICAgImhleF9nZW04
fGEvaF9IaWxsL3Q0IjogewogICAgImJpIjogNS45MjExODk0NjQ2Njc1MDJlLTE1LAogICAgImZp
dCI6IDguMzk0NDA4MTk5ODQ0MTgzZS0xNCwKICAgICJvZGZfcmVhZGluZyI6ICJoZXhQNCIKICAg
fSwKICAgImhleF9nZW04fGIvRTJfSFNtZWFuL3QyIjogewogICAgImJpIjogMi4yMjA0NDYwNDky
NTAzMTNlLTE0LAogICAgImZpdCI6IG51bGwsCiAgICAib2RmX3JlYWRpbmciOiAiaGV4UDIiCiAg
IH0sCiAgICJoZXhfZ2VtOHxiL0UyX0hTbWVhbi90NCI6IHsKICAgICJiaSI6IC01LjE4MTA0MDc4
MTU4NDA2MzZlLTE1LAogICAgImZpdCI6IG51bGwsCiAgICAib2RmX3JlYWRpbmciOiAiaGV4UDQi
CiAgIH0sCiAgICJoZXhfZ2VtOHxiL0UyX0hpbGwvdDIiOiB7CiAgICAiYmkiOiAyLjU3MjAxNjY3
MzcxNDk0NmUtMTQsCiAgICAiZml0IjogNC44OTU3NTE1MjkzNjEwOThlLTEzLAogICAgIm9kZl9y
ZWFkaW5nIjogImhleFAyIgogICB9LAogICAiaGV4X2dlbTh8Yi9FMl9IaWxsL3Q0IjogewogICAg
ImJpIjogLTEuMjk1MjYwMTk1Mzk2MDE2ZS0xNCwKICAgICJmaXQiOiAtMi42NjQ1NDQxMTI2NTY4
NTFlLTEzLAogICAgIm9kZl9yZWFkaW5nIjogImhleFA0IgogICB9LAogICAiaGV4X2dlbTh8Yi9o
X0hpbGwvdDIiOiB7CiAgICAiYmkiOiAtOS4yNTE4NTg1Mzg1NDI5NzJlLTE2LAogICAgImZpdCI6
IDEuODYxNzU0NDAzNTk3MTMyZS0xNCwKICAgICJvZGZfcmVhZGluZyI6ICJoZXhQMiIKICAgfSwK
ICAgImhleF9nZW04fGIvaF9IaWxsL3Q0IjogewogICAgImJpIjogNi4yOTEyNjM4MDYyMDkyMmUt
MTUsCiAgICAiZml0IjogOC4yNTY3ODE0ODM0ODQyOTZlLTE0LAogICAgIm9kZl9yZWFkaW5nIjog
ImhleFA0IgogICB9LAogICAiaGV4X3N0ZXB8YS9FMl9IU21lYW4vdDIiOiB7CiAgICAiYmkiOiA3
LjAzMTQxMjQ4OTI5MjY1OGUtMTUsCiAgICAiZml0IjogbnVsbCwKICAgICJvZGZfcmVhZGluZyI6
ICJoZXhQMiIKICAgfSwKICAgImhleF9zdGVwfGEvRTJfSFNtZWFuL3Q0IjogewogICAgImJpIjog
Mi45NjA1OTQ3MzIzMzM3NTFlLTE1LAogICAgImZpdCI6IG51bGwsCiAgICAib2RmX3JlYWRpbmci
OiAiaGV4UDQiCiAgIH0sCiAgICJoZXhfc3RlcHxhL0UyX0hpbGwvdDIiOiB7CiAgICAiYmkiOiA5
LjI1MTg1ODUzODU0Mjk3ZS0xNSwKICAgICJmaXQiOiAxLjYyNjYyMzEyNTYyNjE2OTZlLTEzLAog
ICAgIm9kZl9yZWFkaW5nIjogImhleFAyIgogICB9LAogICAiaGV4X3N0ZXB8YS9FMl9IaWxsL3Q0
IjogewogICAgImJpIjogLTEuNDA2MjgyNDk3ODU4NTMxN2UtMTQsCiAgICAiZml0IjogLTIuMjEz
NjE2NzgwMDYwNjYwMmUtMTMsCiAgICAib2RmX3JlYWRpbmciOiAiaGV4UDQiCiAgIH0sCiAgICJo
ZXhfc3RlcHxhL2hfSGlsbC90MiI6IHsKICAgICJiaSI6IDUuNTUxMTE1MTIzMTI1NzgzZS0xNiwK
ICAgICJmaXQiOiA0LjU2Mzk0MTA1NTE3Njg1M2UtMTUsCiAgICAib2RmX3JlYWRpbmciOiAiaGV4
UDIiCiAgIH0sCiAgICJoZXhfc3RlcHxhL2hfSGlsbC90NCI6IHsKICAgICJiaSI6IDYuNDc2MzAw
OTc2OTgwMDhlLTE1LAogICAgImZpdCI6IDcuNjY1NDIzMDg0NTQ3ODQ0ZS0xNCwKICAgICJvZGZf
cmVhZGluZyI6ICJoZXhQNCIKICAgfSwKICAgImhleF9zdGVwfGIvRTJfSFNtZWFuL3QyIjogewog
ICAgImJpIjogOC4xNDE2MzU1MTM5MTc4MTRlLTE1LAogICAgImZpdCI6IG51bGwsCiAgICAib2Rm
X3JlYWRpbmciOiAiaGV4UDIiCiAgIH0sCiAgICJoZXhfc3RlcHxiL0UyX0hTbWVhbi90NCI6IHsK
ICAgICJiaSI6IDMuNzAwNzQzNDE1NDE3MTg5ZS0xNSwKICAgICJmaXQiOiBudWxsLAogICAgIm9k
Zl9yZWFkaW5nIjogImhleFA0IgogICB9LAogICAiaGV4X3N0ZXB8Yi9FMl9IaWxsL3QyIjogewog
ICAgImJpIjogMS4wNzMyMTU1OTA0NzA5ODQ3ZS0xNCwKICAgICJmaXQiOiAxLjYxMjUwMzQ2NTg2
MTYzMTNlLTEzLAogICAgIm9kZl9yZWFkaW5nIjogImhleFAyIgogICB9LAogICAiaGV4X3N0ZXB8
Yi9FMl9IaWxsL3Q0IjogewogICAgImJpIjogLTguODgxNzg0MTk3MDAxMjUyZS0xNSwKICAgICJm
aXQiOiAtMi4xOTkwMjY4Mzg4MDc1OTg3ZS0xMywKICAgICJvZGZfcmVhZGluZyI6ICJoZXhQNCIK
ICAgfSwKICAgImhleF9zdGVwfGIvaF9IaWxsL3QyIjogewogICAgImJpIjogMC4wLAogICAgImZp
dCI6IDYuNTUwMDg3ODU4ODc0OTc2ZS0xNSwKICAgICJvZGZfcmVhZGluZyI6ICJoZXhQMiIKICAg
fSwKICAgImhleF9zdGVwfGIvaF9IaWxsL3Q0IjogewogICAgImJpIjogNC45OTYwMDM2MTA4MTMy
MDQ0ZS0xNSwKICAgICJmaXQiOiA3LjQ4NTg3MTY4MTIxNDcxNWUtMTQsCiAgICAib2RmX3JlYWRp
bmciOiAiaGV4UDQiCiAgIH0KICB9LAogICJOLTIiOiB7CiAgICJjdWJpY19nZW04fDAwMSI6IHsK
ICAgICJiaV81eDUiOiAtOS40MjI1NjY0MzA4MDkzMzZlLTExLAogICAgImJpX2NjIjogMS4yMDI3
NDE2MTAwMTA1ODYzZS0xMiwKICAgICJiaV9jaGF0IjogLTUuNzgyNDExNTg2NTg5MzU3ZS0xMywK
ICAgICJmaXQ3IjogMy40Nzc4NTcyNDYyODE0NDE0ZS0wNywKICAgICJvZGZfcmVhZGluZyI6ICJj
dWJQMks0LWkiCiAgIH0sCiAgICJjdWJpY19nZW04fDExMSI6IHsKICAgICJiaV81eDUiOiAtOS40
MjM0ODQyMTUxNzYzNTllLTExLAogICAgImJpX2NjIjogLTMuNzAwNzQzNDE1NDE3MTg4NmUtMTMs
CiAgICAiYmlfY2hhdCI6IC0xLjg1MDM3MTcwNzcwODU5NDNlLTEzLAogICAgImZpdDciOiAzLjQ3
Nzg1NzIzODQ2NTQyOGUtMDcsCiAgICAib2RmX3JlYWRpbmciOiAiY3ViUDJLNC1pIgogICB9LAog
ICAiY3ViaWNfc3RlcHwwMDEiOiB7CiAgICAiYmlfNXg1IjogLTMuNTI5OTQ2NzA1MzA4ODU0ZS0x
MSwKICAgICJiaV9jYyI6IC03LjYzMjc4MzI5NDI5Nzk1MWUtMTMsCiAgICAiYmlfY2hhdCI6IC02
LjcwNzU5NzQ0MDQ0MzY1NGUtMTMsCiAgICAiZml0NyI6IDEuOTc0MDQzMzc0OTg2MDc2ZS0wNywK
ICAgICJvZGZfcmVhZGluZyI6ICJjdWJQMks0LWkiCiAgIH0sCiAgICJjdWJpY19zdGVwfDExMSI6
IHsKICAgICJiaV81eDUiOiAtMy41MjkyMzYxNjI1NzMwOTRlLTExLAogICAgImJpX2NjIjogLTIu
MjIwNDQ2MDQ5MjUwMzEzZS0xMiwKICAgICJiaV9jaGF0IjogNy40MDE0ODY4MzA4MzQzNzdlLTEz
LAogICAgImZpdDciOiAxLjk3NDA0MzM4NzA2NTE3MjRlLTA3LAogICAgIm9kZl9yZWFkaW5nIjog
ImN1YlAySzQtaSIKICAgfSwKICAgImhleF9nZW04fGEiOiB7CiAgICAiYmlfNXg1IjogMS4zOTIy
MTk2NzI4Nzk5NDYzZS0xMiwKICAgICJiaV9jYyI6IDEuMzY0NjQ5MTM0NDM1MDg4MmUtMTIsCiAg
ICAiYmlfY2hhdCI6IC01LjMxOTgxODY1OTY2MjIwOWUtMTMsCiAgICAiZml0NyI6IC0xLjgzNzIx
MzQxNzg1MTk0M2UtMDgsCiAgICAib2RmX3JlYWRpbmciOiAiaGV4UDJQNCIKICAgfSwKICAgImhl
eF9nZW04fGIiOiB7CiAgICAiYmlfNXg1IjogMS4zODcxODY2NjE4MzQ5Nzg5ZS0xMiwKICAgICJi
aV9jYyI6IDkuNDgzMTU1MDAyMDA2NTQ1ZS0xMywKICAgICJiaV9jaGF0IjogNi45Mzg4OTM5MDM5
MDcyMjhlLTEzLAogICAgImZpdDciOiAtMS44Mzc2MDc0OTkwNDk3Mzg4ZS0wOCwKICAgICJvZGZf
cmVhZGluZyI6ICJoZXhQMlA0IgogICB9LAogICAiaGV4X3N0ZXB8YSI6IHsKICAgICJiaV81eDUi
OiA2Ljk4ODQ4Mzg2NTY3MzgxOWUtMTMsCiAgICAiYmlfY2MiOiAzLjAwNjg1NDAyNTAyNjQ2NmUt
MTMsCiAgICAiYmlfY2hhdCI6IDkuNDgzMTU1MDAyMDA2NTQ1ZS0xMywKICAgICJmaXQ3IjogLTEu
MjQ4ODc5MDczMDQ5MTg4N2UtMDgsCiAgICAib2RmX3JlYWRpbmciOiAiaGV4UDJQNCIKICAgfSwK
ICAgImhleF9zdGVwfGIiOiB7CiAgICAiYmlfNXg1IjogNi44NDYzNzUzMTg1MjE3OTllLTEzLAog
ICAgImJpX2NjIjogMS44NTAzNzE3MDc3MDg1OTQzZS0xMywKICAgICJiaV9jaGF0IjogMi41NDQy
NjEwOTgwOTkzMTdlLTEzLAogICAgImZpdDciOiAtMS4yNDg0NjE1MDgzOTAxMjM2ZS0wOCwKICAg
ICJvZGZfcmVhZGluZyI6ICJoZXhQMlA0IgogICB9CiAgfSwKICAiTi0zIjogewogICAiY3ViaWNf
Z2VtOHwwMDEiOiB7CiAgICAiYmkiOiAtMS4xODQyMzc4OTI5MzM1MDAxZS0xMywKICAgICJmaXQi
OiAtMS40OTQwNzIzNDQyNzQzMzYxZS0xNiwKICAgICJvZGZfcmVhZGluZyI6ICJjdWJQMi1pIiwK
ICAgICJwdXJlX2wyX2NoYW5nZV90MSI6IDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNgogICB9LAogICAi
Y3ViaWNfZ2VtOHwxMTEiOiB7CiAgICAiYmkiOiAtMS4yMjEyNDUzMjcwODc2NzJlLTEzLAogICAg
ImZpdCI6IDEuMjcyNzI4MjkzMjcwNzUzZS0xNiwKICAgICJvZGZfcmVhZGluZyI6ICJjdWJQMi1p
IiwKICAgICJwdXJlX2wyX2NoYW5nZV90MSI6IDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNgogICB9LAog
ICAiY3ViaWNfc3RlcHwwMDEiOiB7CiAgICAiYmkiOiAtMi41OTA1MjAzOTA3OTIwMzE0ZS0xNCwK
ICAgICJmaXQiOiAzLjE0MTcwMjEyMzkzMjQxNmUtMTUsCiAgICAib2RmX3JlYWRpbmciOiAiY3Vi
UDItaSIsCiAgICAicHVyZV9sMl9jaGFuZ2VfdDEiOiAxLjExMDIyMzAyNDYyNTE1NjVlLTE2CiAg
IH0sCiAgICJjdWJpY19zdGVwfDExMSI6IHsKICAgICJiaSI6IC0yLjc3NTU1NzU2MTU2Mjg5MWUt
MTQsCiAgICAiZml0IjogLTEuNjczOTE0Mzg1NzE0NzY1MmUtMTYsCiAgICAib2RmX3JlYWRpbmci
OiAiY3ViUDItaSIsCiAgICAicHVyZV9sMl9jaGFuZ2VfdDEiOiAzLjMzMDY2OTA3Mzg3NTQ2OTZl
LTE2CiAgIH0KICB9LAogICJOLTQiOiB7CiAgICJjdWJpY19nZW04fDAwMSI6IHsKICAgICJiaV81
eDUiOiAtOC44ODE3ODQxOTcwMDEyNTJlLTE1LAogICAgImZpdDciOiA3Ljk2Mzc1NzkzMzM2Nzc5
OWUtMDksCiAgICAiazEyX2NoYXRfdDJzcSI6IG51bGwsCiAgICAib2RmX3JlYWRpbmciOiAiY3Vi
UDJLNC1pIgogICB9LAogICAiY3ViaWNfZ2VtOHwxMTEiOiB7CiAgICAiYmlfNXg1IjogMS4wNjU4
MTQxMDM2NDAxNTAzZS0xNCwKICAgICJmaXQ3IjogLTUuMzA5MTczODM2NDUzMDczNGUtMDksCiAg
ICAiazEyX2NoYXRfdDJzcSI6IG51bGwsCiAgICAib2RmX3JlYWRpbmciOiAiY3ViUDJLNC1pIgog
ICB9LAogICAiY3ViaWNfc3RlcHwwMDEiOiB7CiAgICAiYmlfNXg1IjogMC4wLAogICAgImZpdDci
OiA0LjQ4MTkxMTA3NjM2MTA5ZS0wOSwKICAgICJrMTJfY2hhdF90MnNxIjogLTkuMDUzOTc0ODIw
MTUwMjgyZS0xNSwKICAgICJvZGZfcmVhZGluZyI6ICJjdWJQMks0LWkiCiAgIH0sCiAgICJjdWJp
Y19zdGVwfDExMSI6IHsKICAgICJiaV81eDUiOiAwLjAsCiAgICAiZml0NyI6IC0yLjk4NzkzODgz
MDI3MTk4ZS0wOSwKICAgICJrMTJfY2hhdF90MnNxIjogbnVsbCwKICAgICJvZGZfcmVhZGluZyI6
ICJjdWJQMks0LWkiCiAgIH0KICB9CiB9LAogInBoYXNlMCI6IHsKICAiRi1DVFJMLVNBLUdSSUQi
OiB7CiAgICJjb3VudF9taXNtYXRjaGVzIjogMCwKICAgImNvdW50cyI6IHsKICAgICJEIjogMC4y
NSwKICAgICJhcmVhX25vZGVzX3Blcl9heGlzIjogMjAxLAogICAgIm5fYXJlYV9ncmlkIjogNDA0
MDEsCiAgICAibl9maXRfd2luZG93X2luY2x1c2l2ZSI6IDksCiAgICAibl9maXRfd2luZG93X3N0
cmljdCI6IDcsCiAgICAibl90MnQ0X2F4aXMiOiA1LAogICAgIm5fdDJ0NF9ncmlkIjogMjUsCiAg
ICAibl90X2dyaWQiOiAxMiwKICAgICJuX3dpbmRvd18wcDFfaW5jbHVzaXZlIjogNywKICAgICJu
X3dpbmRvd18wcDFfc3RyaWN0IjogNSwKICAgICJ0MnQ0X2F4aXMiOiBbCiAgICAgLTAuMjUsCiAg
ICAgLTAuMTI1LAogICAgIDAuMCwKICAgICAwLjEyNSwKICAgICAwLjI1CiAgICBdLAogICAgInRf
Z3JpZCI6IFsKICAgICAtMC41LAogICAgIC0wLjI1LAogICAgIC0wLjEsCiAgICAgLTAuMDUsCiAg
ICAgLTAuMDIsCiAgICAgMC4wLAogICAgIDAuMDIsCiAgICAgMC4wNSwKICAgICAwLjEsCiAgICAg
MC4yNSwKICAgICAwLjUsCiAgICAgMS4wCiAgICBdCiAgIH0sCiAgICJvZGZfcmVhZGluZyI6ICJu
b25lIiwKICAgInBhc3NlZCI6IHRydWUKICB9LAogICJGLUNUUkwtU0EtSzI0IjogewogICAib2Rm
X3JlYWRpbmciOiAiaGV4UDJQNC9jdWJQMks0LWkiLAogICAicGFzc2VkIjogdHJ1ZSwKICAgIndv
cnN0X2Fic19iaSI6IDkuNDIzNDg0MjE1MTc2MzU5ZS0xMSwKICAgIndvcnN0X2Fic19maXQ3Ijog
My40Nzc4NTcyNDYyODE0NDE0ZS0wNwogIH0sCiAgIkYtQ1RSTC1TQS1MMk5VTEwiOiB7CiAgICJp
ZGVudGl0eV9jdWJQMl9paSI6ICJ0aGUgb2N0YWhlZHJhbGx5IHN5bW1ldHJpemVkIGwgPSAyIHBl
cnR1cmJhdGlvbiB2YW5pc2hlcyBpZGVudGljYWxseSAobm8gbCA9IDIgaW52YXJpYW50IG9mIHRo
ZSBvY3RhaGVkcmFsIGdyb3VwKTsgYXNzZXJ0ZWQgc3ltYm9saWNhbGx5IiwKICAgIm9kZl9yZWFk
aW5nIjogImN1YlAyLWlpL2N1YlAyLWkvY3ViUDJLNC1pIiwKICAgInBhc3NlZCI6IHRydWUsCiAg
ICJ3b3JzdF9hYnNfa2FwcGEyIjogMS4yMjEyNDUzMjcwODc2NzJlLTEzLAogICAid29yc3RfYWJz
X2thcHBhMjIiOiA3Ljk2Mzc1NzkzMzM2Nzc5OWUtMDksCiAgICJ3b3JzdF9hYnNfdDJfYWxvbmVf
dDEiOiAzLjMzMDY2OTA3Mzg3NTQ2OTZlLTE2CiAgfSwKICAiRi1DVFJMLVNBLU1BU0siOiB7CiAg
ICJvZGZfcmVhZGluZyI6ICJub25lIiwKICAgInBhc3NlZCI6IHRydWUsCiAgICJzZWFsZWRfb3Bl
bnNfYmVmb3JlX3BoYXNlMyI6IDAKICB9LAogICJGLUNUUkwtU0EtTU9OTyI6IHsKICAgIm1vbm90
b25pY2l0eV92aW9sYXRpb25zIjogMCwKICAgIm9kZl9yZWFkaW5nIjogIm5vbmUiLAogICAicGFz
c2VkIjogdHJ1ZSwKICAgIndvcnN0X3NjYWxpbmdfcmVsIjogMi4xOTQzMzQ2NTU5ODkyMzU4ZS0x
NgogIH0sCiAgIkYtQ1RSTC1TQS1QSU4iOiB7CiAgICJvZGZfcmVhZGluZyI6ICJub25lIiwKICAg
InBhc3NlZCI6IHRydWUsCiAgICJyYXdfbWlzbWF0Y2hlcyI6IDAsCiAgICJ3b3JzdF90d29sZWdf
U19hYnMiOiAyLjc1MDQ4MjczNTc1OTIyMThlLTE1LAogICAid29yc3RfdHdvbGVnX2IxX3JlbCI6
IDYuNDc2NzIzNDcxMjE1NTg3ZS0xMywKICAgIndvcnN0X3R3b2xlZ19rYXBwYTNfcmVsIjogMi4w
NzkxOTk5NjYwMjc4MDc0ZS0wNywKICAgIndvcnN0X3R3b2xlZ19rYXBwYV9yZWwiOiAxLjEwODYy
ODgxMDIzNDU3ZS0wOQogIH0sCiAgIkYtQ1RSTC1TQS1QSU4tREVSSVZFRCI6IHsKICAgImxlYWZf
bWlzbWF0Y2hlcyI6IDAsCiAgICJsZWF2ZXNfY29tcGFyZWQiOiAxMDQyLAogICAib2RmX3JlYWRp
bmciOiAibm9uZSIsCiAgICJwYXNzZWQiOiB0cnVlLAogICAid29yc3Rfc2NhbGVkX2RldiI6IDMu
Mzg4MTI5NzEyMTQ2NTg1ZS0wNQogIH0sCiAgIkYtQ1RSTC1TQS1SRUNPTiI6IHsKICAgIm9kZl9y
ZWFkaW5nIjogImhleFA0L2N1Yks0L2hleFAyIiwKICAgInBhc3NlZCI6IHRydWUsCiAgICJ3b3Jz
dF9hYnNfRTJfSGlsbCI6IDYuODQ1NjU5NjQ3NjE3MDU0ZS0xMCwKICAgIndvcnN0X3JlbF9yb2J1
c3QiOiAwLjAwMDcyNjkxMTAzNzc1MDQ1NjUKICB9LAogICJGLUNUUkwtU0EtUyI6IHsKICAgIm9k
Zl9yZWFkaW5nIjogImhleFAyL2hleFA0L2N1Yks0IiwKICAgInBhc3NlZCI6IHRydWUsCiAgICJ3
b3JzdF9hYnNfYmkiOiAyLjE3MzA3NjUzMzUzMjk3M2UtMTIsCiAgICJ3b3JzdF9hYnNfZml0Ijog
NC4yNjcxNjgyMjkwMjE4OTZlLTExCiAgfSwKICAiRi1DVFJMLVNBLVNJR04iOiB7CiAgICJiaW5k
aW5nX2VuZF9taXNtYXRjaGVzIjogMCwKICAgIm9kZl9yZWFkaW5nIjogIm5vbmUiLAogICAicGFz
c2VkIjogdHJ1ZQogIH0sCiAgIkYtQ1RSTC1TQS1UMSI6IHsKICAgImExX2luY2x1ZGVkIjogZmFs
c2UsCiAgICJjb2xsaXNpb25zIjogMTMsCiAgICJoaXRzIjogMCwKICAgIm9kZl9yZWFkaW5nIjog
Im5vbmUiLAogICAicGFzc2VkIjogdHJ1ZSwKICAgInBhdHRlcm5zIjogMzYsCiAgICJwZXJfZmls
ZSI6IHsKICAgICJHX01TQ1NfQV9MT0NLX1JFQ09SRC5tZCI6IHsKICAgICAiY29sbGlzaW9ucyI6
IDAsCiAgICAgImhpdHNfYnlfaW5kZXgiOiBbXQogICAgfSwKICAgICJnX21zY3NfYV9jaGF0bGVn
LnB5IjogewogICAgICJjb2xsaXNpb25zIjogMCwKICAgICAiaGl0c19ieV9pbmRleCI6IFtdCiAg
ICB9LAogICAgImdfbXNjc19hX2NvbXBhcmVfdjFfMC5weSI6IHsKICAgICAiY29sbGlzaW9ucyI6
IDAsCiAgICAgImhpdHNfYnlfaW5kZXgiOiBbXQogICAgfSwKICAgICJnX21zY3NfYV9zY2hlbWFf
djFfMC5qc29uIjogewogICAgICJjb2xsaXNpb25zIjogMCwKICAgICAiaGl0c19ieV9pbmRleCI6
IFtdCiAgICB9LAogICAgInBpbm5lZF9pbnB1dHNfR19NU0NTX0EuanNvbiI6IHsKICAgICAiY29s
bGlzaW9ucyI6IDEzLAogICAgICJoaXRzX2J5X2luZGV4IjogW10KICAgIH0sCiAgICAic3RhZ2lu
Z19tZW1vX0dfTVNDU19BX3YyLm1kIjogewogICAgICJjb2xsaXNpb25zIjogMCwKICAgICAiaGl0
c19ieV9pbmRleCI6IFtdCiAgICB9CiAgIH0KICB9LAogICJGLUNUUkwtU0EtWkVSTyI6IHsKICAg
Im9kZl9yZWFkaW5nIjogInVuaWZvcm0iLAogICAicGFzc2VkIjogdHJ1ZSwKICAgIndvcnN0X2Fi
c19yMCI6IDMuMzMwNjY5MDczODc1NDY5NmUtMTYKICB9CiB9LAogInBoYXNlMiI6IHsKICAiQy1T
WU4tMSI6IHsKICAgImRldGFpbCI6ICJ0PTAuMDEgcmVmIGNsYXNzIEJJTkRJTkc7IHQ9MC4xIHJl
ZiBjbGFzcyBCSU5ESU5HOyB0PTAuNSByZWYgY2xhc3MgSU5FUlQtSU4tRCIsCiAgICJwYXNzZWQi
OiB0cnVlCiAgfSwKICAiQy1TWU4tMTAiOiB7CiAgICJkZXRhaWwiOiAiVk9JRDsgbWl4ZWQgbl92
b2lkIDEiLAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkMtU1lOLTExIjogewogICAiZGV0YWls
IjogIldJTkRPVy1ERUxJVkVSRUQiLAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkMtU1lOLTEy
IjogewogICAiZGV0YWlsIjogImZsYWcgZmlyZXMgb24gMTYgY2VsbHMsIGNsZWFyIG9uIDIwIiwK
ICAgInBhc3NlZCI6IHRydWUKICB9LAogICJDLVNZTi0xMyI6IHsKICAgImRldGFpbCI6ICJtYXJn
aW5fcG9zaXRpdmUgTUFSR0lOLU9OTFk7IG1hcmdpbl9uZWdhdGl2ZSBNQVJHSU4tT05MWSIsCiAg
ICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiQy1TWU4tMTQiOiB7CiAgICJkZXRhaWwiOiAic25hcHBl
ZCBodWxsIGhpID09IDA7IFNJR04iLAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkMtU1lOLTIi
OiB7CiAgICJkZXRhaWwiOiAiYmluZGluZyBlbmRzIGJ5IHNpZ24oa2FwcGEpOyBlZGdlcyBleGFj
dCIsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiQy1TWU4tMyI6IHsKICAgImRldGFpbCI6ICJL
SUxML0tJTEwvVFVORUQvVFVORUQocm9idXN0bmVzcyBvbmx5KTogS0lMTC1JTi1EIEtJTEwtSU4t
RCBUVU5FRCBUVU5FRCIsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiQy1TWU4tNCI6IHsKICAg
ImRldGFpbCI6ICJJTkVSVC1JTi1EIiwKICAgInBhc3NlZCI6IHRydWUKICB9LAogICJDLVNZTi01
IjogewogICAiZGV0YWlsIjogImN1YmljIHQyIE5VTEwtSU5FUlQiLAogICAicGFzc2VkIjogdHJ1
ZQogIH0sCiAgIkMtU1lOLTYiOiB7CiAgICJkZXRhaWwiOiAiMTUgbWFsZm9ybWVkIGZpbGVzIGFi
b3J0ZWQ6IGJhcl9pbl9zcmMsIGJvbSwgY3JsZiwgZHVwbGljYXRlX2tleSwgZm9ybWZlZWRfaW5f
c3JjLCBsb19ndF9oaSwgbWlzc2luZ19rZXksIHBlcmNlbnRfY2wsIHJlYWRpbmdfY2VpbGluZywg
c3VwZXJzY3JpcHQsIHRyYWlsaW5nX2JsYW5rLCB1MjAyOF9pbl9zcmMsIHVuaWNvZGVfbWludXMs
IHdyb25nX2RlbHRhX2RlZiwgd3JvbmdfaWQ7IHZhbGlkIGZpbGUgY2Vuc3VzIGNvbmZpcm1lZDsg
bGVhayBOT05FIiwKICAgInBhc3NlZCI6IHRydWUKICB9LAogICJDLVNZTi03IjogewogICAiZGV0
YWlsIjogIndvcnN0IHNjYWxpbmcgZGV2IDIuMTllLTE2LCB2aW9sYXRpb25zIDAiLAogICAicGFz
c2VkIjogdHJ1ZQogIH0sCiAgIkMtU1lOLTgiOiB7CiAgICJkZXRhaWwiOiAiSSA9IFttYXggbG8s
IG1pbiBoaV0iLAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkMtU1lOLTkiOiB7CiAgICJkZXRh
aWwiOiAiQU5DSE9SLUlOQ09OU0lTVEVOVCIsCiAgICJwYXNzZWQiOiB0cnVlCiAgfQogfSwKICJw
aGFzZTMiOiBudWxsLAogInBpbm5lZF9pbnB1dHNfbWQ1IjogIjJkNDRlYzAxYTY2ODg5ZjMzMGQ5
NDBkZWUzMzEzYmRjIiwKICJzY2FubmVyX21kNSI6ICI2Yjg2MjkwMDkwYThjODRmMWIxYTBhOTll
YzBiZjY5NyIsCiAic2NoZW1hX21kNSI6ICI1MzIzZTExZmMyN2Q2ODhmNjFhYWY1NzMwMmM4NzVj
MCIsCiAidDFfYTFfbWQ1IjogbnVsbCwKICJ0MV9saXN0X21kNSI6ICJlMjc0ZTU4ZWE1MGI5ZWQz
NDc5NjllNTA3ZDJhNGYzNiIsCiAidXRjIjogIjIwMjYtMDktMzBUMDI6MTU6NDhaIiwKICJ2ZXJp
Zmllcl9tZDUiOiAiY2YwMDRkNTE3ZDJlZmU5MWEwMmM5MmE1OGUzZGY2YmYiCn0K
=====END-EMBED name=g_mscs_a_chatleg_prereadcheckpoint.json=====

=====BEGIN-EMBED name=G_MSCS_A_MAPPER_FREEZE_AND_PREREAD_REPORT.md md5=1bf60dd342adbe3f09043365cd25e021 bytes=5773 encoding=base64 armor_bytes=7802 QUARANTINED=====
IyBHLU1TQ1MtQSDigJQgY2hhdCBtYXBwZXIgZnJlZXplIGFuZCBwcmUtcmVhZCByZXBvcnQgKFNl
cHRlbWJlciAyOSwgMjAyNjsgMDI6MTYgVVRDIFNlcHRlbWJlciAzMCkKCioqTG9jayByZWNvcmQ6
KiogYEdfTVNDU19BX0xPQ0tfUkVDT1JELm1kYCBtZDUgYDgxMTZjYzYyMjI3OWI1ZDRlNzMyMTQx
NzhhZTk3Y2Q4YCAoMTcsOTIzIEIpLiBMb2NrZWQgYXJ0aWZhY3RzIGFzIGl0cyDCpzEuICoqQ2hh
dCBtYXBwZXIgRlJPWkVOOioqIGBnX21zY3NfYV9jaGF0bGVnLnB5YCBtZDUgKipgMGQwZTVlY2Y2
MTBiMzRmMjFlOGMyMmRkMzkzOGNlNDBgKiogKDUxLDQ5MCBCKS4gSXQgZW1iZWRzIGFuZCBhc3Nl
cnRzLCBhdCBldmVyeSBpbnZvY2F0aW9uLCB0aGUgbWQ1cyBvZiB0aGUgbWVtbyAoYDZlYTE2Yjk1
YCksIHRoZSBwaW5uZWQgZmlsZSAoYDJkNDRlYzAxYCksIHRoZSBsb2NrIHJlY29yZCAoYDgxMTZj
YzYyYCksIHRoZSBUMSBnYXRlIGxpc3QgKGBlMjc0ZTU4ZWApLCB0aGUgYmFzZSBsaXN0IChgMDUz
MDIyMTBgKSwgdGhlIHNjYW5uZXIgKGA2Yjg2MjkwMGApLCB0aGUgc2NoZW1hIChgNTMyM2UxMWZg
KSBhbmQgdGhlIGNvbXBhcmF0b3IgKGBjNWI0YTdhYWApLgoKIyMgUHJlLXJlYWQgcnVuIChQaGFz
ZSAwICsgUGhhc2UgMiksIHRoZSBmcm96ZW4gaW5zdHJ1bWVudCwgYG1haW5gID0gYGUxZmEwNzFg
CgpDaGVja3BvaW50IGBnX21zY3NfYV9jaGF0bGVnX3ByZXJlYWRjaGVja3BvaW50Lmpzb25gIG1k
NSBgY2NiYjMyMDc3OTk2ODMzY2RhYzIzMzk5MzgxOTNlYzFgICgxMyw4NDIgQjsgYHBoYXNlM2Ag
PSBudWxsOyBwb3N0LXdyaXRlIFQxIHNjYW4gMCBoaXRzLCAxIGNvbGxpc2lvbikuCgp8IENvbnRy
b2wgfCBSZXN1bHQgfCBPYnNlcnZlZCAobGltaXQpIHwKfC0tLXwtLS18LS0tfAp8IEYtQ1RSTC1T
QS1QSU4gfCBQQVNTIHwgMzM1IHJhdyB2YWx1ZXMgZXF1YWwgdGhlaXIgc291cmNlcyBieSBwb2lu
dGVyOyB0d28tbGVnIM66IOKJpCAxLjExw5cxMOKBu+KBuSwgzrrigoMg4omkIDIuMDjDlzEw4oG7
4oG3LCBi4oKBIOKJpCA2LjQ4w5cxMOKBu8K5wrMgcmVsYXRpdmUgKDHDlzEw4oG74oG0KTsgUyDi
iaQgMi43NsOXMTDigbvCueKBtSBhYnNvbHV0ZSAoMcOXMTDigbvigbYpIHwKfCBGLUNUUkwtU0Et
UElOLURFUklWRUQgfCBQQVNTIHwgMSwwNDIgbGVhdmVzIHJlLWRlcml2ZWQgd2l0aCB0aGUgbWFw
cGVyJ3Mgb3duIGNvZGU7IHdvcnN0IHNjYWxlZCBkZXZpYXRpb24gMy40w5cxMOKBu+KBtSBvZiB0
aGUgdG9sZXJhbmNlOyAwIG1pc21hdGNoZXMgfAp8IEYtQ1RSTC1TQS1aRVJPIHwgUEFTUyB8IOKJ
pCAzLjM0w5cxMOKBu8K54oG2ICgxw5cxMOKBu8K5wrIpIHwKfCBGLUNUUkwtU0EtUkVDT04gfCBQ
QVNTIHwgNi44NcOXMTDigbvCueKBsCBhYnNvbHV0ZSBvbiBTMi1F4oKCIEhpbGwgKDHDlzEw4oG7
4oG4KTsgNy4yN8OXMTDigbvigbQgcmVsYXRpdmUgb24gdGhlIHJvYnVzdG5lc3MgYXJtcyAoMcOX
MTDigbvCsykgfAp8IEYtQ1RSTC1TQS1TIHwgUEFTUyB8IGJpIOKJpCAyLjE4w5cxMOKBu8K5wrIs
IGZpdCDiiaQgNC4yN8OXMTDigbvCucK5ICgxw5cxMOKBu+KBtikgfAp8IEYtQ1RSTC1TQS1LMjQg
fCBQQVNTIHwgZXZlcnkgYmFzaXMtaW5kZXBlbmRlbnQgZXN0aW1hdG9yIOKJpCA5LjQzw5cxMOKB
u8K5wrk7IGZpdDcg4omkIDMuNDjDlzEw4oG74oG3ICgxw5cxMOKBu+KBtikgfAp8IEYtQ1RSTC1T
QS1MMk5VTEwgfCBQQVNTIHwgzrrigoIg4omkIDEuMjPDlzEw4oG7wrnCsywgzrrigoLigoIg4omk
IDcuOTfDlzEw4oG74oG5ICgxw5cxMOKBu+KBtik7IHTigoIgYWxvbmUgYXQgdOKCgiA9IDEg4omk
IDMuMzTDlzEw4oG7wrnigbYgKDHDlzEw4oG7wrnCsikgfAp8IEYtQ1RSTC1TQS1TSUdOIHwgUEFT
UyB8IDAgYmluZGluZy1lbmQgbWlzbWF0Y2hlcyBvdmVyIDM2IGNlbGxzIHwKfCBGLUNUUkwtU0Et
R1JJRCB8IFBBU1MgfCBjb3VudHMgZnJvbSB0aGUgZ2VuZXJhdG9yczogMTI7IDkgLyA3OyA3IC8g
NTsgNTsgMjU7IDQwLDQwMSB8CnwgRi1DVFJMLVNBLU1PTk8gfCBQQVNTIHwgd29yc3Qg4oiaMTAg
c2NhbGluZyBkZXZpYXRpb24gMi4yw5cxMOKBu8K54oG2ICgxw5cxMOKBu8K54oG0KTsgMCBtb25v
dG9uaWNpdHkgdmlvbGF0aW9ucyB8CnwgRi1DVFJMLVNBLU1BU0sgfCBQQVNTIHwgMCBzZWFsZWQg
b3BlbnMgYmVmb3JlIFBoYXNlIDMgfAp8IEYtQ1RSTC1TQS1UMSB8IFBBU1MgfCAwIGhpdHMgdW5k
ZXIgdGhlIDM2IHBhdHRlcm5zIG92ZXIgdGhlIGluc3RydW1lbnQsIG1lbW8sIHBpbm5lZCBmaWxl
LCBsb2NrIHJlY29yZCwgc2NoZW1hIGFuZCBjb21wYXJhdG9yOyAxMyBjb2xsaXNpb25zLCBhbGwg
aW4gdGhlIHBpbm5lZCBmaWxlIHwKClBoYXNlIDI6ICoqQy1TWU4tMSDigKYgQy1TWU4tMTQgYWxs
IFBBU1MqKiAoZm91cnRlZW4gb2YgZm91cnRlZW4pLiBBbW9uZyB0aGUgZGV0YWlsczogQy1TWU4t
MyBnaXZlcyBLSUxMLUlOLUQgLyBLSUxMLUlOLUQgLyBUVU5FRCAvIFRVTkVEKHJvYnVzdG5lc3Mg
b25seSk7IEMtU1lOLTYgYWJvcnRlZCBhbGwgZmlmdGVlbiBtYWxmb3JtZWQgZmlsZXMgd2l0aCBy
ZWFzb24gY29kZXMgYW5kIGxlYWtlZCBub25lIG9mIHRoZSBmb3VyIHN5bnRoZXRpYyB2YWx1ZXM7
IEMtU1lOLTEyIGZpcmVzIHRoZSBOVUxMLUZMT09SIGZsYWcgb24gMTYgb2YgMzYgY2VsbHMgYXQg
dF9zeW4gPSAxMOKBu+KBuSBhbmQgbm90IG9uIHRoZSBvdGhlciAyMDsgQy1TWU4tMTMgZ2l2ZXMg
TUFSR0lOLU9OTFkgb24gYm90aCBwaW5uZWQgYmFuZCBpbnRlcnZhbHM7IEMtU1lOLTE0IHNuYXBz
IHRoZSBub2lzeSBodWxsIGVuZCB0byAwIGFuZCBjbGFzc2VzIFNJR04uCgoqKkNvbXBhcmF0b3Iq
KiBgYzViNGE3YWFgOiAyMi8yMiBhZHZlcnNhcmlhbCBzZWxmLXRlc3Qgc3VpdGVzOyBvbiB0aGUg
cHJlLXJlYWQgY2hlY2twb2ludCBhZ2FpbnN0IGEgcHNldWRvLUNDIGNvcHkgKGxlZyBsYWJlbCBh
bmQgaW5zdHJ1bWVudCBtZDUgY2hhbmdlZCkgMCBtaXNzZXMuCgojIyBTeW50aGV0aWMgZW5kLXRv
LWVuZCByZWFkIChkaXNjbG9zZWQ7IG5vdCBhIGdhdGUgcmVzdWx0OyBkZWxldGVkIGFmdGVyIHRo
ZSB0ZXN0KQoKVGhlIGZ1bGwgYHJlYWRgIHBhdGggd2FzIGV4ZXJjaXNlZCB3aXRoIHN5bnRoZXRp
YyBzZWFsZWQgZmlsZXMgd2hvc2UgdmFsdWVzIHJlc2VtYmxlIG5vIG9ic2VydmF0aW9uIChidWRn
ZXRzIG9mIG9yZGVyIDEw4oG74oG2IOKApiAxMOKBu+KBtCksIGJhc2U2NC1hcm1vcmVkLCB3aXRo
IGEgc3ludGhldGljIFQxLUExIGJ1aWx0IGJ5IGBzYV90MWExX2J1aWxkLnB5YDogZXZlcnkgZ2F0
ZSBjbGFzcyB3YXMgcHJvZHVjZWQgYnkgY29uc3RydWN0aW9uIChXSU5ET1ctREVMSVZFUkVELCBJ
TkVSVC1JTi1ELCBUVU5FRCwgTUFSR0lOLU9OTFksIEtJTEwtSU4tRCwgVk9JRCksIE9PTSByb2J1
c3RuZXNzIGFuZCB0aGUgcm93LWxldmVsIE1PTk8gY2hlY2sgcmFuLCB0aGUgdHdvLXBhcmFtZXRl
ciByZWdpb24gd2FzIGNvbXB1dGVkICh0aGUgaGV4IFMyLUXigoIgcmVnaW9uIG5vbi1jb21wYWN0
IGFsb25nIHRoZSBudWxsIHJheXMsIGFzIFNULTIgcHJlZGljdHMpLCB0aGUgY2hlY2twb2ludCBj
YXJyaWVkIG5vbmUgb2YgdGhlIHN5bnRoZXRpYyB2YWx1ZXMgb3IgdGhlIHN5bnRoZXRpYyBgc3Jj
YCB0ZXh0IChmaXhlZC1zdHJpbmcgc2VhcmNoKSwgdGhlIG1hc2tlZCBhYm9ydHMgZmlyZWQgb24g
YSBDUkxGIGZpbGUgYW5kIG9uIGEgd3Jvbmcgc3RhdGVkIG1kNSwgYW5kIGBjZW5zdXNgIG1vZGUg
cHJpbnRlZCBtZDUsIGJ5dGVzIGFuZCBjZW5zdXMgb25seS4KCiMjIEQtU0EtMSAoYSBwcmUtZnJl
ZXplIGNvbGxpc2lvbiwgZm91bmQgYnkgdGhlIHN5bnRoZXRpYyBydW47IGZvciB0aGUgYXV0aG9y
IGJlZm9yZSBUMS1BMSBpcyBmcm96ZW4pCgpgc2FfdDFhMV9idWlsZC5weWAgd3JpdGVzLCBmb3Ig
ZXZlcnkgYW5jaG9yIG51bWJlciwgcmVuZGVyaW5ncyBhdCBwcmVjaXNpb25zIHAg4oiIIHtu4oiS
MiwgbuKIkjEsIG4sIG4rMX0gc2lnbmlmaWNhbnQgZGlnaXRzLiBXaGVuIGEgbnVtYmVyIGhhcyBv
bmUgb3IgdHdvIHNpZ25pZmljYW50IGRpZ2l0cywgdGhhdCBzZXQgaW5jbHVkZXMgYSAqKm9uZS1z
aWduaWZpY2FudC1kaWdpdCoqIHJlbmRlcmluZyDigJQgZm9yIGEgc3ludGhldGljIHZhbHVlIGl0
IHByb2R1Y2VkIHRoZSBob3VzZSBmb3JtcyBgMcOXMTDigbvCs2AgYW5kIGAxw5cxMOKBu+KBtGAg
YW5kIHRoZSBlLWZvcm0gYDFlLTRgIOKAlCB3aGljaCBhcmUgYWxzbyB0aGUgdG9sZXJhbmNlIGxp
dGVyYWxzIG9mIHRoZSBsb2NrZWQgbWVtbywgdGhlIGxvY2sgcmVjb3JkIGFuZCB0aGUgcGlubmVk
IGZpbGUgKHRoZSDOuiBmbG9vciwgz4RfYWdnLCB0aGUgdHdvLWxlZyDOuiB0b2xlcmFuY2UsIHRo
ZSBSRUNPTiB0b2xlcmFuY2UpLiBVbmRlciB0aGUgdW5pb24gbGlzdCB0aGUgUGhhc2UtMCBUMSBz
Y2FuIHRoZW4gaGFsdHMgb24gdGhlIGxvY2tlZCBhcnRpZmFjdHMgdGhlbXNlbHZlcywgZXhhY3Rs
eSB0aGUgUy1TQS0xMCBoYXphcmQuIFRoaXMgaXMgd2hhdCB0aGUgcHJlLWZyZWV6ZSBjb2xsaXNp
b24gc2NhbiAobWVtbyDCpzQuNikgZXhpc3RzIGZvciwgYW5kIHRoZSBtZW1vIGFscmVhZHkgc2V0
cyB0aGUgZGlzcG9zaXRpb246IGEgY29sbGlkaW5nIHBhdHRlcm4gaXMgdG9vIGdlbmVyaWMgZm9y
IHRoaXMgZ2F0ZSBhbmQgaXMgcmVtb3ZlZCBmcm9tIEExIGJlZm9yZSB0aGUgZnJlZXplLCBsb2dn
ZWQgYXMgYSBELWl0ZW0uICoqUmVjb21tZW5kYXRpb246KiogYWZ0ZXIgYnVpbGRpbmcgQTEsIGRl
bGV0ZSBmcm9tIGl0IGV2ZXJ5IHJlbmRlcmluZyB3aXRoIGZld2VyIHRoYW4gdHdvIHNpZ25pZmlj
YW50IGRpZ2l0cyAob3IsIGVxdWl2YWxlbnRseSwgcnVuIGB0MV9zY2FuLnB5YCB3aXRoIEExIGFs
b25lIG92ZXIgdGhlIGxvY2tlZCBhcnRpZmFjdHMgYW5kIHRoZSBtYXBwZXIsIGFuZCBkZWxldGUg
ZWFjaCBoaXQncyBwYXR0ZXJuIGxpbmUpOyB0aGUgY2hhdCBsZWcgcmVwZWF0cyB0aGF0IHNjYW4g
b24gcmVjZWlwdCBhbmQgcmVwb3J0cyBhbnkgaGl0IGJ5IGluZGV4IGJlZm9yZSB0aGUgQTEgZnJl
ZXplLiBObyBsb2NrZWQgYXJ0aWZhY3QgY2hhbmdlcy4KCiMjIFdoYXQgcmVtYWlucyAobG9jayBy
ZWNvcmQgwqc0KQoKMS4gKipUaGUgYXV0aG9yIHN1cHBsaWVzIHRoZSBzZWFsZWQgZmlsZSArIFQx
LUExKiogKG1lbW8gwqc0LjYpOiBhcm1vcmVkICh6aXAgb3IgYmFzZTY0IHdpdGggbWFya2Vycyks
IHRoZSB1bmFybW9yZWQgbWQ1IGFuZCBieXRlIGNvdW50LCB0aGUgY2Vuc3VzLCBhbmQgQTEgYWZ0
ZXIgdGhlIGNvbGxpc2lvbiByZXNvbHV0aW9uIGFib3ZlLgoyLiBUaGUgY2hhdCBsZWcgY29uZmly
bXMgbWQ1LCBieXRlcyBhbmQgY2Vuc3VzIChgY2Vuc3VzYCBtb2RlOyBub3RoaW5nIGVsc2UgcmVh
ZCksIHJ1bnMgdGhlIEExIHByZS1mcmVlemUgY29sbGlzaW9uIHNjYW4sIGZyZWV6ZXMgQTEuCjMu
IERpc3BhdGNoIChQLTQ7IHRoZSBzZWFsZWQgZmlsZSBhcm1vcmVkIGluIFAtNC5iOyBQLTQuYyBk
ZWxpdmVyZWQgYWxvbmUpIOKGkiBDQyBibGluZCByZWFkIGZyb20gc2NyYXRjaCDihpIgY2hhdCBy
ZWFkIOKGkiB0d28tbGVnIGNvbXBhcmlzb24g4oaSIFM5IG9uIG1pc3NlcyDihpIgZm9sZCBhdXRo
b3JpemF0aW9uIOKGkiBWNC44NyB3aXRoIEgtTVMyLTksIEgtU0EtMyBhbmQgSC1TQS00LgoKKkNo
YXQgbGVnLCBTZXB0ZW1iZXIgMjksIDIwMjYuIE5vdGhpbmcgaGFzIGJlZW4gbWFwcGVkIGFnYWlu
c3QgYW55IGFuY2hvci4qCg==
=====END-EMBED name=G_MSCS_A_MAPPER_FREEZE_AND_PREREAD_REPORT.md=====

