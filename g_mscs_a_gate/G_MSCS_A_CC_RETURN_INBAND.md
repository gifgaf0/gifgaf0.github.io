# G-MSCS-A — CC LEG RETURN (P-4 single-file in-band, mirrored) — September 30, 2026

**Gate:** G-MSCS-A (the sealed-anchor mini-gate on the texture constraint surface r_agg = κ₂₂t₂² + κ₄₄t₄²). **Leg:** CC, built blind from scratch (CC-BLIND-FIRST, E-SA-8(a)); the read of record for the class. **Base:** V4.86 `d4c42a53cbd6d325ebc740879288e844` (not held; not needed). **Lock chain honoured (every one md5 + byte guarded by the instrument at every invocation):** memo v2 `6ea16b952db835bb351d3dc1b474c6ed` (121,950 B) · lock record `8116cc622279b5d4e73214178ae97cd8` (Addendum A-2.1–A-2.6) · pinned inputs `2d44ec01a66889f330d940dee3313bdc` (96,761 B) · schema v1.0 `5323e11fc27d688f61aaf57302c875c0` · comparator v1.0 `c5b4a7aab2fc8651be6d26d1f3d25642` · gate T1 list `e274e58ea50b9ed347969e507d2a4f36` · base list `05302210cc4ceb70553acbe8379e9fc3` · T1-A1 `3b753b3a371a162fc2ab21b9eed51bd5` · scanner `6b86290090a8c84f1b1a0a99ec0bf697`.

**Dispatch consumed:** the delivered file (md5 `a934bc9463f9abf31cded093d750ed63`, 666,726 B), saved as `g_mscs_a_gate/dispatch.md`. **Activation flag received, verbatim, in the author's directive:** `ACTIVATE: G-MSCS-A-CC-LEG-1` — delivered in a second directive after the dispatch (D-CC-1, §8); nothing sealed was opened and nothing was committed before it arrived.

## 1. Branch and commits (pre-read first, pre-consultation second)

Branch `claude/new-session-7flqwf`, started from `main` = **`e1fa071`** (the state the dispatch §6 records, unchanged at start; `git fetch origin main` confirmed it). Directory `g_mscs_a_gate/`. The chat-side fold estate lands later in `g_mscs_a_gate/estate/` by a successor PR; no canonical ledger is committed.

| Commit | Content |
|---|---|
| **`1752296`** — **pre-read checkpoint** | `dispatch.md` (quarantine still armored), `extract.py`, the twenty plain embeds at their paths (`tools/t1/`, `inputs/`, `sealed/` — the sealed armor unopened), the instrument `g_mscs_a_ccleg.py` (md5 **`a5263388f2db2ce676060551e5636d81`**, 67,228 B), `g_mscs_a_ccleg_prereadcheckpoint.json` (md5 **`c9f8e4af305f579b1b19953725042d87`**, 17,030 B; `phase3` = null; quoted in the commit message), `run_preread.log`. Committed before the flag arrived, on the session's stop-hook instruction to commit untracked work; Phase 3 was held. |
| **`21b7d79`** — **pre-consultation checkpoint** | `g_mscs_a_ccleg_checkpoint.json` (md5 **`d0e129fc8c324f0779803a6e33068777`**, 138,012 B; md5 and gate class quoted in the commit message), `run_read.log`. No quarantined embed was decoded before this commit. |
| (this commit) — return | `G_MSCS_A_CC_RETURN_INBAND.md` (this file, with the three embeds), its plaintext and `build_return.py`. |
| (next commit) — quarantine opened | the three decoded embeds and `g_mscs_a_preread_twoleg_comparison.json`: the frozen comparator run on the chat pre-read checkpoint against the CC pre-read checkpoint. |

**Dispatch §2 results:** the extractor (the dispatch's, saved as `extract.py`) printed twenty `OK` lines and three `SKIP` lines, every md5 and byte count as inventoried. `t1_scan.py` on the memo and the lock record under the gate list: CLEAN (3 / 0 collisions). `g_mscs_a_compare_v1_0.py selftest`: SELFTEST PASS (22/22; the schema md5 asserted). `sa_verify_pinned_inputs.py inputs pinned_inputs_G_MSCS_A.json sa_build_pinned_inputs.py`: RESULT PASS (335 values through the pointer map; 1,105 derived leaves, 0 mismatches).

## 2. Instrument and execution summary

**`g_mscs_a_ccleg.py`** (md5 `a5263388…`), standard library only (the container has no numpy; none was needed). Written from the memo (§1, §3, §4, §5, §6), the lock record's Addendum A-2, the schema and the pinned file; the chat mapper, its pre-read checkpoint and the freeze report stayed armored until after the return was committed (§1). Two modes: `preread` (Phases 0 and 2, checkpoint with `phase3` = null) and `read` (Phases 0 and 2 recomputed from scratch, then Phase 3). Run time: **2.1 s** for the full read (pre-read 1.9 s).

- **Guards and T1.** Nine locked artifacts md5 + byte guarded at every invocation; the frozen scanner is imported (after its guard) so the hit rule is the scanner's own; this file, the memo, the pinned file, the lock record, the schema and the comparator are scanned under the gate list ∪ A1 at every invocation, halt on any hit, no override; the emitted checkpoint is scanned before it is written (fixed point on the collision count), re-scanned after, and deleted on a hit. A key-name guard refuses any checkpoint carrying `lo`, `hi`, `k_em_max`, `k_t_max`, `cl`, `src` or `note`.
- **Binder (A-2.1, F-CTRL-SA-PIN).** Own RFC 6901 resolver. The seven pinned sources are read from `inputs/` at their md5s and byte counts; every `raw` value is re-read through the `provenance` pointer template (`{K}` substituted; scopes `all` / `cubic` / `dqf` = the keys the quadform-basis diagnostic banks) and compared to the pinned value by its JSON serialization (bit-exact for floats); every `raw` leaf is checked to be covered by a pointer (the only uncovered field is the `branch` label, checked against `structure`). 335 values, 0 mismatches.
- **Derivations (F-CTRL-SA-PIN-DERIVED).** Own code for `families` (Richardson even / odd parts of the banked 12-point grids at the (0.05, 0.1) pair, fit resolution, two-leg relatives, the three-term reconstruction and the truncation ratio at D on the primary arm), `reach` (the second-order box over the mapped families, the hull with every banked grid value inside D and the CC 5 × 5 grid on the primary arm, zero-snap, ×(1 + μ)), `unions`, `synthetic` (the pinned band rules), `nulls` (N-1 … N-4; the mixed and even Richardson parts of the 5 × 5 grid at the (0.125, 0.25) pair under the row-major layout), `hex_quadform` and `zero_ctrl`. All 1,105 leaves of the pinned `derived` (minus `summary`) reproduced with **worst scaled deviation 0.0** — every leaf bit-identical.
- **Masked parser (A-2.3, memo §4.1–§4.4).** Own implementation: BOM, UTF-8, control characters and Unicode separators, final LF, blank lines, the ` | ` separator with the bar-anywhere-else guard, first-`=` split, canonical key order, `SA-n` ids, the token sets from the pinned `tokens`, the ASCII number regex with finiteness, lo ≤ hi, `cl` in (0, 1) or `hard`, printable ASCII outside `src` / `note`. A failure raises a reason code that names the row and the key, never a value. Row md5 over the row bytes without the LF; census {rows, per_class, fields_per_row}. Armor: marker lines (lines starting with `=====`) stripped, whitespace ignored, base64 validated; a one-member zip also accepted. The md5 and byte count of the unarmored file are asserted against the author's stated `cfd62dcf…` / 177 B before parsing; an open outside Phase 3 is counted and halts.
- **Class logic (A-2.4).** Per row the regime clause x = max(k_em_max, k_t_max) × d_EM against KD_CLIP; the combined interval as the intersection of the non-VOID rows; for I ∋ 0 the per-cell binding end by sign(κ), t\* = √(b/κ) (0 at b = 0), BINDING iff t\* < D, the same with κ_bi, T on the primary arm only, ν with the b = 0 infinity, σ\* by the family rms (closed forms recomputed and asserted against `constants.rms`); the fcc t₂ family NULL-INERT; for I ∌ 0 the exclusion classes against R^w and R^h with the SIGN / MAGNITUDE sub-reason and the per-family requirements; the two-parameter region on the hex keys enumerated node by node from the area-grid generator; the gate class in precedence; the σ-union and strict intersection; OOM ×10 / ×0.1 through the same mapper with the MONO check (a violation on the actual rows halts as an instrument defect). Every count is computed from the pinned generators; no point count is typed in the instrument.
- **Pre-read validation (no sealed open).** Beyond Phase 2, the instrument's Phase 3 path was exercised on synthetic armored files (in-zero, excluding-zero, two rows, void, void plus silent, inconsistent, malformed, wrong md5) with the armor path, md5, byte count and output name monkey-patched in a scratch directory; every case behaved as specified and every written synthetic checkpoint self-compared clean through the frozen comparator (2,225 / 1,099 / 2,976 checks). The pre-read checkpoint self-compares 706/706. The scratch files were deleted; the real armor was not touched.

## 3. Phase 0 (12 items; all PASS; recomputed identically on the pre-read and the read runs)

| Item | `odf_reading` | CC float(s) | Rule |
|---|---|---|---|
| F-CTRL-SA-PIN | none | raw_mismatches 0; worst two-leg κ rel 1.109×10⁻⁹ (S2-h κ₂); κ₃ rel 1.777×10⁻⁸ (fcc; the floor clause, CC-DD-1); b₁ rel 6.477×10⁻¹³; S abs 2.750×10⁻¹⁵ | 0; ≤ 1×10⁻⁴; ≤ 1×10⁻⁴; ≤ 1×10⁻⁴; ≤ 1×10⁻⁶ |
| F-CTRL-SA-PIN-DERIVED | none | leaf_mismatches 0; worst_scaled_dev 0.0 (1,105 leaves) | 0; ≤ 1 |
| F-CTRL-SA-ZERO | uniform | worst_abs_r0 3.331×10⁻¹⁶ | ≤ 1×10⁻¹² |
| F-CTRL-SA-RECON | hexP4/cubK4/hexP2 | worst_abs_E2_Hill 6.846×10⁻¹⁰; worst_rel_robust 7.269×10⁻⁴ (S2-h) | ≤ 1×10⁻⁸; ≤ 1×10⁻³ |
| F-CTRL-SA-S | hexP2/hexP4/cubK4 | worst_abs_bi 2.173×10⁻¹²; worst_abs_fit 4.267×10⁻¹¹ | ≤ 1×10⁻⁶ each |
| F-CTRL-SA-K24 | hexP2P4/cubP2K4-i | worst_abs_bi 9.423×10⁻¹¹ (the fcc 5 × 5 estimate); worst_abs_fit7 3.478×10⁻⁷ | ≤ 1×10⁻⁶ each |
| F-CTRL-SA-L2NULL | cubP2-ii/cubP2-i/cubP2K4-i | worst_abs_kappa2 1.221×10⁻¹³; worst_abs_kappa22 7.964×10⁻⁹; worst_abs_t2_alone_t1 3.331×10⁻¹⁶; the cubP2-ii identity as a string | ≤ 1×10⁻⁶; ≤ 1×10⁻⁶; ≤ 1×10⁻¹² |
| F-CTRL-SA-SIGN | none | binding_end_mismatches 0 (36 mapped cells; t\* also checked against the expected end) | 0 |
| F-CTRL-SA-GRID | none | count_mismatches 0 (formula vs enumeration; the eight counts written) | 0 |
| F-CTRL-SA-MONO | none | worst_scaling_rel 2.809×10⁻¹⁶; monotonicity_violations 0 | ≤ 1×10⁻¹⁴; 0 |
| F-CTRL-SA-MASK | none | sealed_opens_before_phase3 0 | 0 |
| F-CTRL-SA-T1 | none | hits 0; collisions 16 (memo 3, pinned file 13, others 0) | 0 |

## 4. Phase 2 (14 suites; all PASS on both runs)

| Suite | Result |
|---|---|
| C-SYN-1 | t\* = t_syn on the reference cell to 1×10⁻¹² relative; BINDING at 0.01 and 0.1, INERT-IN-D at 0.5; every other cell's t\* = √(b/\|κ\|) recomputed; gate WINDOW-DELIVERED / WINDOW-DELIVERED / INERT-IN-D |
| C-SYN-2 | binding ends by sign(κ) on all 36 cells; t\* = 0.05·√(\|κ_ref\|/\|κ\|) on κ > 0 cells, 0.1·√(…) on κ < 0 cells |
| C-SYN-3 | (i) EXCLUDED on every cell, MAGNITUDE where R^w[1] > 0 and SIGN where R^w[1] = 0, gate KILL-IN-D; (ii) the mirror, KILL-IN-D; (iii) TUNED on ≥ 1 cell, gate TUNED; (iv) `robustness_only_positive`: no primary-arm primary-key cell TUNED, ≥ 1 robustness cell TUNED, gate TUNED |
| C-SYN-4 | [−1, +1]: INERT-IN-D on every mapped cell; gate INERT-IN-D |
| C-SYN-5 | the fcc t₂ family NULL-INERT with window [−D, +D] under C-SYN-1 |
| C-SYN-6 | fifteen malformed files (CRLF, BOM, trailing blank line, form feed and U+2028 in `src`, Unicode minus, superscript form, bar in `src`, lo > hi, `reading=ceiling`, wrong `delta_def`, missing key, wrong id, duplicate key, percent-form `cl`) each abort with a reason code; the valid file parses (census 1 row, 11 fields, row md5 as computed independently); a fixed-string search finds no synthetic value in the reason codes, the instrument's stdout or either checkpoint |
| C-SYN-7 | OOM on the C-SYN-1 intervals: worst scaling rel 2.809×10⁻¹⁶, violations 0 |
| C-SYN-8 | rows [−b(0.1), +b(0.1)] and [−b(0.05), +b(0.2)]: the mapped interval is [−b(0.05), +b(0.1)] (t₄ binds at t\* = 0.1 on hi, t₂ at 0.05·√(\|κ_ref\|/\|κ₂\|) on lo) |
| C-SYN-9 | two disjoint rows: ANCHOR-INCONSISTENT, `combined` null, per-row mappings serialized |
| C-SYN-10 | k = 1×10³³: VOID-REGIME; alone → gate VOID; with a silent row the silent row alone is mapped (combined identical to the silent row alone) |
| C-SYN-11 | [0, 0]: t\* = 0, ν = ∞ (`nu` null, `nu_is_inf` true), NULL-FLOOR set, BINDING on every mapped cell; gate WINDOW-DELIVERED |
| C-SYN-12 | t_syn = 1×10⁻⁹: the flag on each cell equals (\|S_bi\|·t\*/b > 0.1) recomputed; set on 16 cells, clear on 20 |
| C-SYN-13 | `margin_positive` and `margin_negative`: no cell TUNED, ≥ 1 cell MARGIN, gate MARGIN-ONLY (both) |
| C-SYN-14 | the fcc ⟨001⟩ Hill reach rebuilt with +5×10⁻¹³ at t = 0.02: hull[1] = 0, widened[1] = 0 (also with the perturbation at t = 0); a positive interval classes EXCLUDED-IN-D / SIGN |

## 5. Phase 3 — the read of record (no value of the sealed file appears here or in any artifact)

**Sealed identity (C-SA-3):** md5 `cfd62dcf060427ac3402604e6c3284ff`, 177 B, census {rows 1, per_class {spd: 1}, fields_per_row [11]}, row md5 `59b357fda68557002f11a40100c3ca9c` — identical to the chat leg's census-mode confirmation. `t1_a1_md5` `3b753b3a371a162fc2ab21b9eed51bd5`. Row SA-1: not VOID-REGIME; contains 0. Combined interval = the row (one row); `n_void_rows` 0; `combined_empty` false; `contains_zero` true.

**Gate class: `WINDOW-DELIVERED`.** OOM ×10 `WINDOW-DELIVERED`, ×0.1 `WINDOW-DELIVERED`; **OOM-ROBUST** true (every mapped cell BINDING under both scalings; MONO on the actual rows: worst scaling rel 2.809×10⁻¹⁶, 0 violations). `sigma_union_hi` (CONSERVATIVE, the max σ₄\* over the four primary keys) = **1.235493174523598×10⁻⁶** (cubic_step\|001); `sigma_strict_hi` (serialized, non-verdict) = 6.582437027892329×10⁻⁷ (hex_gem8\|a).

**Per-cell classes and edges (the 36 mapped cells; the fcc t₂ family NULL-INERT on all 12 cubic cells with window [−0.25, +0.25]).** Every mapped cell is **BINDING** on both κ of record and κ_bi; no RESOLUTION-SENSITIVE, TRUNCATION-SENSITIVE or NULL-FLOOR-SENSITIVE flag fires anywhere; binding ends exactly as ST-4 pre-registered (S2-E₂ hex t₂ and fcc ⟨001⟩ t₄ on lo, S2-E₂ hex t₄ and fcc ⟨111⟩ t₄ on hi, every S2-h family on lo). Full precision in the embedded checkpoint; four significant digits here.

| key | arm | fam | t\* | t\*_bi | σ\* | T (primary arm) | ν | end |
|---|---|---|---|---|---|---|---|---|
| hex_step\|a | E2_Hill | t4 | 2.089×10⁻⁶ | 2.089×10⁻⁶ | 6.963×10⁻⁷ | 2.884×10⁻⁹ | 4.197×10⁻⁵ | hi |
| hex_step\|a | E2_Hill | t2 | 1.444×10⁻⁶ | 1.444×10⁻⁶ | 6.456×10⁻⁷ | 7.391×10⁻¹⁰ | 4.452×10⁻⁶ | lo |
| hex_step\|a | E2_HSmean | t4 | 2.092×10⁻⁶ | 2.092×10⁻⁶ | 6.974×10⁻⁷ | — | 8.849×10⁻⁶ | hi |
| hex_step\|a | E2_HSmean | t2 | 1.449×10⁻⁶ | 1.449×10⁻⁶ | 6.482×10⁻⁷ | — | 3.397×10⁻⁶ | lo |
| hex_step\|a | h_Hill | t4 | 1.999×10⁻⁵ | 1.999×10⁻⁵ | 6.663×10⁻⁶ | — | 4.315×10⁻⁵ | lo |
| hex_step\|a | h_Hill | t2 | 3.866×10⁻⁵ | 3.866×10⁻⁵ | 1.729×10⁻⁵ | — | 7.153×10⁻⁶ | lo |
| hex_step\|b | E2_Hill | t4 | 2.089×10⁻⁶ | 2.089×10⁻⁶ | 6.963×10⁻⁷ | 2.886×10⁻⁹ | 2.651×10⁻⁵ | hi |
| hex_step\|b | E2_Hill | t2 | 1.444×10⁻⁶ | 1.444×10⁻⁶ | 6.458×10⁻⁷ | 7.397×10⁻¹⁰ | 5.166×10⁻⁶ | lo |
| hex_step\|b | E2_HSmean | t4 | 2.092×10⁻⁶ | 2.092×10⁻⁶ | 6.974×10⁻⁷ | — | 1.106×10⁻⁵ | hi |
| hex_step\|b | E2_HSmean | t2 | 1.450×10⁻⁶ | 1.450×10⁻⁶ | 6.483×10⁻⁷ | — | 3.934×10⁻⁶ | lo |
| hex_step\|b | h_Hill | t4 | 1.999×10⁻⁵ | 1.999×10⁻⁵ | 6.663×10⁻⁶ | — | 3.329×10⁻⁵ | lo |
| hex_step\|b | h_Hill | t2 | 3.868×10⁻⁵ | 3.868×10⁻⁵ | 1.730×10⁻⁵ | — | 0 (S_bi = 0) | lo |
| hex_gem8\|a | E2_Hill | t4 | 1.975×10⁻⁶ | 1.975×10⁻⁶ | 6.582×10⁻⁷ | 2.413×10⁻⁹ | 2.819×10⁻⁵ | hi |
| hex_gem8\|a | E2_Hill | t2 | 1.258×10⁻⁶ | 1.258×10⁻⁶ | 5.626×10⁻⁷ | 8.233×10⁻¹⁰ | 1.094×10⁻⁵ | lo |
| hex_gem8\|a | E2_HSmean | t4 | 1.978×10⁻⁶ | 1.978×10⁻⁶ | 6.593×10⁻⁷ | — | 3.137×10⁻⁶ | hi |
| hex_gem8\|a | E2_HSmean | t2 | 1.261×10⁻⁶ | 1.261×10⁻⁶ | 5.641×10⁻⁷ | — | 9.259×10⁻⁶ | lo |
| hex_gem8\|a | h_Hill | t4 | 1.967×10⁻⁵ | 1.967×10⁻⁵ | 6.556×10⁻⁶ | — | 3.882×10⁻⁵ | lo |
| hex_gem8\|a | h_Hill | t2 | 3.039×10⁻⁵ | 3.039×10⁻⁵ | 1.359×10⁻⁵ | — | 1.312×10⁻⁵ | lo |
| hex_gem8\|b | E2_Hill | t4 | 1.975×10⁻⁶ | 1.975×10⁻⁶ | 6.583×10⁻⁷ | 2.412×10⁻⁹ | 3.654×10⁻⁵ | hi |
| hex_gem8\|b | E2_Hill | t2 | 1.258×10⁻⁶ | 1.258×10⁻⁶ | 5.625×10⁻⁷ | 8.229×10⁻¹⁰ | 1.078×10⁻⁵ | lo |
| hex_gem8\|b | E2_HSmean | t4 | 1.978×10⁻⁶ | 1.978×10⁻⁶ | 6.593×10⁻⁷ | — | 1.464×10⁻⁵ | hi |
| hex_gem8\|b | E2_HSmean | t2 | 1.261×10⁻⁶ | 1.261×10⁻⁶ | 5.641×10⁻⁷ | — | 9.335×10⁻⁶ | lo |
| hex_gem8\|b | h_Hill | t4 | 1.967×10⁻⁵ | 1.967×10⁻⁵ | 6.557×10⁻⁶ | — | 4.125×10⁻⁵ | lo |
| hex_gem8\|b | h_Hill | t2 | 3.038×10⁻⁵ | 3.038×10⁻⁵ | 1.359×10⁻⁵ | — | 9.368×10⁻⁶ | lo |
| cubic_step\|001 | E2_Hill | t4 | 2.831×10⁻⁶ | 2.831×10⁻⁶ | 1.235×10⁻⁶ | 1.991×10⁻⁸ | 9.396×10⁻⁴ | lo |
| cubic_step\|001 | E2_HSmean | t4 | 2.776×10⁻⁶ | 2.776×10⁻⁶ | 1.212×10⁻⁶ | — | 9.692×10⁻⁵ | lo |
| cubic_step\|001 | h_Hill | t4 | 8.882×10⁻⁶ | 8.884×10⁻⁶ | 3.876×10⁻⁶ | — | 1.766×10⁻³ | lo |
| cubic_step\|111 | E2_Hill | t4 | 1.675×10⁻⁶ | 1.675×10⁻⁶ | 7.309×10⁻⁷ | 1.178×10⁻⁸ | 1.591×10⁻³ | hi |
| cubic_step\|111 | E2_HSmean | t4 | 1.642×10⁻⁶ | 1.642×10⁻⁶ | 7.168×10⁻⁷ | — | 1.537×10⁻⁴ | hi |
| cubic_step\|111 | h_Hill | t4 | 8.882×10⁻⁶ | 8.884×10⁻⁶ | 3.876×10⁻⁶ | — | 1.766×10⁻³ | lo |
| cubic_gem8\|001 | E2_Hill | t4 | 2.584×10⁻⁶ | 2.584×10⁻⁶ | 1.128×10⁻⁶ | 2.183×10⁻⁸ | 1.872×10⁻³ | lo |
| cubic_gem8\|001 | E2_HSmean | t4 | 2.509×10⁻⁶ | 2.509×10⁻⁶ | 1.095×10⁻⁶ | — | 2.095×10⁻⁴ | lo |
| cubic_gem8\|001 | h_Hill | t4 | 8.133×10⁻⁶ | 8.136×10⁻⁶ | 3.549×10⁻⁶ | — | 3.285×10⁻³ | lo |
| cubic_gem8\|111 | E2_Hill | t4 | 1.529×10⁻⁶ | 1.529×10⁻⁶ | 6.672×10⁻⁷ | 1.292×10⁻⁸ | 3.168×10⁻³ | hi |
| cubic_gem8\|111 | E2_HSmean | t4 | 1.484×10⁻⁶ | 1.484×10⁻⁶ | 6.477×10⁻⁷ | — | 3.688×10⁻⁴ | hi |
| cubic_gem8\|111 | h_Hill | t4 | 8.133×10⁻⁶ | 8.136×10⁻⁶ | 3.549×10⁻⁶ | — | 3.285×10⁻³ | lo |

Windows are [−t\*, +t\*] on every mapped cell. The largest ν (3.285×10⁻³, cubic_gem8 S2-h) sits a factor of about 30 below the 0.10 flag threshold; the largest T (2.183×10⁻⁸) a factor of about 5×10⁶ below it.

**Two-parameter region (hex keys, every arm; reported, no class):** on every one of the 12 hex cells exactly **1 admissible node of the 40,401** (the origin), `area_fraction` 2.475×10⁻⁵, `compact` true; `definiteness` indefinite on the S2-E₂ arms with `null_ray_slope` 2.9956 / 2.9948 / 3.2497 / 3.2501 (Hill; step a / b, gem8 a / b) and 2.9887 / 2.9878 / 3.2460 / 3.2465 (HS-mean) — ST-2's slopes; negative-definite on S2-h, slope null. At this budget the null rays do not reach a second grid node, so the region is compact on the pinned grid even on the indefinite arms.

**Reading, in one sentence (R2, under E-MS-1(a), I-SA-1, E-SA-4(a), the no-Born aggregate and D):** the sealed anchor contains δ = 0 and binds every configuration, arm and mapped family far inside D, delivering the constraint curve on the texture import as a σ-window of 1.2355×10⁻⁶ (CONSERVATIVE) across the four primary configurations; no kill-surface item fires, no texture is confirmed or required, and the class is robust to an order of magnitude either way. Per ST-1 no window here is sightline-independent.

## 6. CC-DD (readings that A-2 left to this leg)

- **CC-DD-1** `derived.families.twoleg_kappa3_rel` and `twoleg_rel` are computed on every mapped family and null on the unmapped fcc t₂ family — the pinned layout carries the hex κ₃ relatives although every hex κ₃ is below the κ floor. The F-CTRL-SA-PIN float `worst_twoleg_kappa3_rel` applies A-2.2's floor clause literally (only the fcc κ₃ are counted): 1.777×10⁻⁸; over every mapped cell it would read 2.079×10⁻⁷ (the memo §5 figure). Both are four orders under 1×10⁻⁴.
- **CC-DD-2** `hex_quadform.kappa22_fit7_vs_kappa2_rel` is normalized by |κ₂₂ fit7| (the pinned value; normalizing by |κ₂| differs at 5×10⁻⁶ relative, above the PIN-DERIVED tolerance).
- **CC-DD-3** Checkpoint layout beyond the schema's field lists: `phase3.rows[j]` carries `id`, `row_md5`, `void_regime`, `contains_zero` and the same three blocks as `combined` (`families`, `exclusion`, `two_param`), a block null where it does not apply (void row; I ∌ 0 → `families` and `two_param` null; I ∋ 0 → `exclusion` null; VOID and ANCHOR-INCONSISTENT → `combined` null). `exclusion` is serialized per key × arm × mapped family with the five schema fields, `class` and `subreason` repeated per family and `t_in` / `t_out` / `can_supply_alone` null on a family of the other sign. `nulls` is the pinned `derived.nulls` layout (N-3 with `pure_l2_change_t1`). Everything beyond the schema sits under a top-level `extras` block (the OOM per-cell classes and combined blocks, unions, synthetic intervals, per-file T1 counts, elapsed time), which the comparator does not read.
- **CC-DD-4** `reach.grid_exceeds_box` is computed on the unsnapped grid extrema (matches the pinned value on all 24 cells).
- **CC-DD-5** The NULL-INERT record carries `class` and the window only; every other field, the flags included, is null (not false).
- **CC-DD-6** `nu` is serialized null when infinite (b = 0), with `nu_is_inf` true — JSON has no infinity and the comparator compares null only to null.
- **CC-DD-7** OOM monotonicity for an interval excluding 0 (beyond A-2.2's BINDING / INERT wording): t_in and t_out must scale by √10 / √0.1 (memo §3.8) and the exclusion class may only move TUNED → MARGIN → EXCLUDED under ×10 and back under ×0.1. Not exercised by the actual row (I ∋ 0); exercised by the synthetic dry runs.
- **CC-DD-8** C-SYN-14: the literal perturbation (+5×10⁻¹³ at t = 0.02) leaves the fcc ⟨001⟩ Hill hull upper end set by the 5 × 5 grid's noise value, which snaps to 0 either way; the suite also perturbs t = 0 as an extra check.
- **CC-DD-9** Armor: marker lines are the lines starting with `=====`; whitespace ignored; base64 validated; a one-member zip also accepted.
- **CC-DD-10** F-CTRL-SA-GRID `count_mismatches` compares the counts by formula with the counts by explicit enumeration of the generators (the t-grid predicates, the axis product, the area node list).
- **CC-DD-11** The T1 scan calls the frozen scanner's own `scan_text` (imported after its md5 guard) so the hit rule is the scanner's, not a re-implementation; the contextual numeric rule is therefore exactly the gate's.
- **CC-DD-12** The two-parameter `null_ray_slope` and `definiteness` use the arm's κ of record (κ₂ and κ₄₄), as A-2.4 words it; `sigma_star` is t\*·rms on the unclipped t\* (serialized for INERT-IN-D cells too; the gate σ-union reads it only where every primary key is BINDING).

## 7. H-CC (self-caught bugs; observations)

- **H-CC-1 (bug, caught by a synthetic Phase 3 dry run before any real open):** the VOID and ANCHOR-INCONSISTENT early returns of the row mapper lacked the two σ fields the gate block reads (a KeyError after the sealed line). Fixed; every synthetic Phase 3 path then ran and self-compared clean.
- **H-CC-2 (bug):** the C-SYN-6 leak guard searched for a four-digit fragment of the synthetic `cl`, which matched a synthetic row md5 by chance and refused that checkpoint; the guard now searches only the full value strings and their long digit runs. On the real read no synthetic value appears anywhere (checked at write time and over the whole stdout).
- **H-CC-3 (observation, no verdict effect):** memo §5 quotes the PIN κ₃ agreement as "≤ 2.1×10⁻⁷", a figure that counts the hex κ₃ coefficients, while A-2.2's floor clause excludes them (CC-DD-1). The lock record is binding; the memo figure is the mapped-cell reading.
- **H-CC-4 (observation):** the pre-read checkpoint carries `activation_flag` null (written before the flag arrived); the read checkpoint carries it verbatim. Both checkpoints are otherwise identical in Phases 0 and 2 (same instrument, same floats).
- **H-CC-5 (observation, for the S9 if it comes):** the layout choices of CC-DD-3 are the likeliest source of a representational miss against the chat mapper (a "key sets differ" row from C-SA-1/2); the classes, flags and edges themselves have no free parameter. The path-(a) mini-dispatch pattern applies.

## 8. Deviations

- **D-CC-1 (the activation flag):** the directive that delivered the dispatch carried only the file; the flag `ACTIVATE: G-MSCS-A-CC-LEG-1` arrived in a second directive. Before it: the blind build, Phases 0 and 2, the synthetic dry runs, and — on the session's stop-hook instruction to commit untracked work — the pre-read commit `1752296` (the sealed armor unopened, the quarantine still armored). After it: Phase 3, the pre-consultation commit `21b7d79`, this return. The interlock was honoured for everything it guards.
- **D-CC-2:** standard library only (no numpy in the container; none needed). Python 3.11.15.
- **D-CC-3:** the Phase 3 code path was rehearsed on synthetic armored files in the session scratchpad (never in the repository; deleted afterwards) — recorded so that the "one-shot read" is known to have run on tested code, not as a sealed open (the MASK counter stayed 0; the real armor's md5 and byte count were asserted only at the real read).

## 9. T1 state

Under the gate list `e274e58e` (36 patterns) ∪ A1 `3b753b3a` (68 patterns), at both runs: **0 hits** on the instrument, the memo (3 collisions), the pinned file (13), the lock record, the schema, the comparator, the pre-read checkpoint (1 collision post-write), the read checkpoint (1 post-write), `run_preread.log`, `run_read.log`, `extract.py`, both commit messages and this return (scanned before commit under the gate list, A1 and the base list). The three list embeds and the sealed armor are scan-exempt for cause (the G-POLY1 class).

## 10. Embeds (the dispatch's sentinel format, byte-exact)

1. `g_mscs_a_ccleg.py` — the instrument (md5 `a5263388f2db2ce676060551e5636d81`, 67,228 B).
2. `g_mscs_a_ccleg_prereadcheckpoint.json` — the pre-read checkpoint (md5 `c9f8e4af305f579b1b19953725042d87`, 17,030 B).
3. `g_mscs_a_ccleg_checkpoint.json` — the pre-consultation checkpoint, the read of record (md5 `d0e129fc8c324f0779803a6e33068777`, 138,012 B).

=====BEGIN-EMBED name=g_mscs_a_ccleg.py md5=a5263388f2db2ce676060551e5636d81 bytes=67228 encoding=raw=====
#!/usr/bin/env python3
"""g_mscs_a_ccleg.py -- Gate G-MSCS-A, the CC-leg instrument (built blind: from the locked memo sections 1, 3-6, the
lock record's Addendum A-2, the frozen schema and the pinned-inputs file only; its own parser, binder and class logic;
the chat mapper stayed quarantined while this was written).

Standard library only. Every invocation: md5 + byte guards on the memo, the pinned file, the lock record, the gate T1
list, the base list, T1-A1, the scanner, the schema and the comparator; a T1 scan of this file, the memo, the pinned
file, the lock record, the schema and the comparator under the gate list plus A1 (halt on any hit, no override); then
Phase 0 (twelve controls, halt-on-fail) and Phase 2 (fourteen synthetic suites) from scratch. `preread` stops there and
writes g_mscs_a_ccleg_prereadcheckpoint.json (phase3 = null). `read` goes on to Phase 3: the armored sealed file is
decoded only then, parsed masked, mapped, OOM-scaled, and g_mscs_a_ccleg_checkpoint.json is written and T1-scanned
after writing (deleted on a hit). No value of the sealed file (lo, hi, k_em_max, k_t_max, cl, src, note) is ever printed,
logged or serialized -- only its md5, byte count, census, row md5s and the derived classes, flags and edges.

Usage:  python3 g_mscs_a_ccleg.py preread [--inputs DIR] [--flag TEXT]
        python3 g_mscs_a_ccleg.py read    [--inputs DIR] [--flag TEXT]
Exit: 0 on a completed run; 1 on a halt (INDETERMINATE), a T1 hit or a masked abort; 2 on usage.
No point count is typed anywhere in this file: every count is computed from the pinned generators.
"""
import base64, hashlib, importlib.util, io, json, math, os, re, sys, tempfile, time, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE, LEG, INSTRUMENT = 'G-MSCS-A', 'cc', os.path.basename(os.path.abspath(__file__))
LEDGER_BASE_MD5 = 'd4c42a53cbd6d325ebc740879288e844'
MEMO, PINNED, LOCK = 'staging_memo_G_MSCS_A_v2.md', 'pinned_inputs_G_MSCS_A.json', 'G_MSCS_A_LOCK_RECORD.md'
SCHEMA, COMPARATOR = 'g_mscs_a_schema_v1_0.json', 'g_mscs_a_compare_v1_0.py'
T1_LIST, T1_BASE, T1_A1, SCANNER = ('tools/t1/T1_forbidden_G_MSCS_A.txt', 'tools/t1/T1_base_author_20260919.txt',
                                    'tools/t1/t1_forbidden_G_MSCS_A_A1.txt', 'tools/t1/t1_scan.py')
GUARDS = {  # locked artifact -> (md5, bytes), from the lock record section 1 and the dispatch inventory
    MEMO: ('6ea16b952db835bb351d3dc1b474c6ed', 121950),
    PINNED: ('2d44ec01a66889f330d940dee3313bdc', 96761),
    LOCK: ('8116cc622279b5d4e73214178ae97cd8', 17923),
    T1_LIST: ('e274e58ea50b9ed347969e507d2a4f36', 1482),
    T1_BASE: ('05302210cc4ceb70553acbe8379e9fc3', 143),
    T1_A1: ('3b753b3a371a162fc2ab21b9eed51bd5', 1030),
    SCANNER: ('6b86290090a8c84f1b1a0a99ec0bf697', 1967),
    SCHEMA: ('5323e11fc27d688f61aaf57302c875c0', 9436),
    COMPARATOR: ('c5b4a7aab2fc8651be6d26d1f3d25642', 16850),
}
T1_SCANNED = [MEMO, PINNED, LOCK, SCHEMA, COMPARATOR]          # plus this file itself
SEALED_ARMOR = 'sealed/anchors_G_MSCS_A_SEALED.md.b64'
SEALED_MD5, SEALED_BYTES = 'cfd62dcf060427ac3402604e6c3284ff', 177   # the author's stated md5 and byte count (unarmored)
PREREAD_CK, READ_CK = 'g_mscs_a_ccleg_prereadcheckpoint.json', 'g_mscs_a_ccleg_checkpoint.json'
ELECTIONS = {'E-SA-0': 'a', 'E-SA-1': 'a', 'E-SA-2': 'a', 'E-SA-3': 'a', 'E-SA-4': 'a', 'E-SA-5': 'a', 'E-SA-6': 'a',
             'E-SA-7': '05302210+MSCS1stratum', 'E-SA-8': 'a', 'E-SA-9': 'a', 'E-SA-10': 'a', 'E-SA-11': 'a'}
FORBIDDEN_KEYS = {'lo', 'hi', 'k_em_max', 'k_t_max', 'src', 'note', 'cl'}
CLASS_PRECEDENCE = ['INDETERMINATE', 'VOID', 'ANCHOR-INCONSISTENT', 'KILL-IN-D', 'TUNED', 'MARGIN-ONLY',
                    'WINDOW-DELIVERED', 'INERT-IN-D']
PHASE0_ITEMS = ['F-CTRL-SA-PIN', 'F-CTRL-SA-PIN-DERIVED', 'F-CTRL-SA-ZERO', 'F-CTRL-SA-RECON', 'F-CTRL-SA-S',
                'F-CTRL-SA-K24', 'F-CTRL-SA-L2NULL', 'F-CTRL-SA-SIGN', 'F-CTRL-SA-GRID', 'F-CTRL-SA-MONO',
                'F-CTRL-SA-MASK', 'F-CTRL-SA-T1']
PHASE0_ODF = {'F-CTRL-SA-PIN': 'none', 'F-CTRL-SA-PIN-DERIVED': 'none', 'F-CTRL-SA-ZERO': 'uniform',
              'F-CTRL-SA-RECON': 'hexP4/cubK4/hexP2', 'F-CTRL-SA-S': 'hexP2/hexP4/cubK4',
              'F-CTRL-SA-K24': 'hexP2P4/cubP2K4-i', 'F-CTRL-SA-L2NULL': 'cubP2-ii/cubP2-i/cubP2K4-i',
              'F-CTRL-SA-SIGN': 'none', 'F-CTRL-SA-GRID': 'none', 'F-CTRL-SA-MONO': 'none', 'F-CTRL-SA-MASK': 'none',
              'F-CTRL-SA-T1': 'none'}
CUBP2_II_IDENTITY = ('cubP2-ii: the octahedrally symmetrized l=2 perturbation is identically zero (the octahedral group '
                     'has no l=2 invariant; for <001>, sum_i P2(e_i . z) = 0), so r_agg is unchanged by t2 at every '
                     'order -- asserted symbolically, no number')
# A-2.2 SIGN and A-2.5 C-SYN-2 / C-SYN-8 name two extra synthetic strengths beside constants.synthetic_t
SYN_T_ASYM_LO, SYN_T_ASYM_HI, SYN_T_OUTER = 0.1, 0.05, 0.2
# --------------------------------------------------------------------------------------------- run-time state
STATE = {'sealed_opens_before_phase3': 0, 'phase3_active': False, 'log': [], 'synthetic_secrets': []}


class Halt(Exception):
    pass


class MaskedAbort(Exception):
    """a sealed-file format failure: carries a reason code only, never a value"""


def log(msg=''):
    STATE['log'].append(msg)
    print(msg)
    sys.stdout.flush()


def md5b(b):
    return hashlib.md5(b).hexdigest()


def read(rel):
    return open(os.path.join(HERE, rel), 'rb').read()


def guard_all():
    seen = {}
    for rel, (want, nbytes) in GUARDS.items():
        b = read(rel)
        h = md5b(b)
        if h != want or len(b) != nbytes:
            raise Halt('GUARD %s: md5 %s bytes %d (expected %s, %d)' % (rel, h, len(b), want, nbytes))
        seen[rel] = h
    return seen


def load_scanner():
    spec = importlib.util.spec_from_file_location('t1_scan_frozen', os.path.join(HERE, SCANNER))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def t1_scan(scanner, pats, rels):
    """scan the named files under the pattern list with the frozen scanner's rule; hits by index only"""
    out, total_hits, total_coll = {}, 0, 0
    for rel in rels:
        text = read(rel).decode('utf-8', 'replace')
        hits, coll = scanner.scan_text(text, pats)
        out[rel] = {'hits': len(hits), 'hit_indices': sorted({i for i, _ in hits}), 'collisions': len(coll)}
        total_hits += len(hits)
        total_coll += len(coll)
    return out, total_hits, total_coll


def t1_scan_text(scanner, pats, text):
    hits, coll = scanner.scan_text(text, pats)
    return len(hits), len(coll)


# --------------------------------------------------------------------------------------------- pointers, leaves
def jptr(doc, ptr):
    """RFC 6901"""
    if ptr == '':
        return doc
    if not ptr.startswith('/'):
        raise Halt('pointer must start with /')
    cur = doc
    for tok in ptr[1:].split('/'):
        tok = tok.replace('~1', '/').replace('~0', '~')
        cur = cur[int(tok)] if isinstance(cur, list) else cur[tok]
    return cur


def leaves(node, path=''):
    if isinstance(node, dict):
        for k in sorted(node):
            yield from leaves(node[k], path + '/' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, '%s/%d' % (path, i))
    else:
        yield path, node


def walk_keys(node):
    if isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_keys(v)


def isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def rel_dev(a, b):
    m = max(abs(a), abs(b))
    return 0.0 if m == 0 else abs(a - b) / m


# --------------------------------------------------------------------------------------------- the pinned inputs
class Pinned:
    def __init__(self, P, S):
        self.P = P
        self.S = S
        st, c, g = P['structure'], P['constants'], P['grids']
        self.keys, self.hex, self.cubic = list(st['keys']), list(st['hex_keys']), list(st['cubic_keys'])
        self.arms = list(st['arms'])
        self.primary_arm, self.primary_keys = st['primary']['arm'], list(st['primary']['keys'])
        self.robust_arms = list(st['robustness']['arms'])
        self.mapped = {'hex': list(st['mapped_families']['hex']), 'cubic': list(st['mapped_families']['cubic'])}
        self.null_fams = {'cubic': list(st['null_families']['cubic'])}
        self.D, self.KD, self.mu = c['D'], c['KD_CLIP'], c['mu']
        self.floor, self.tau, self.snap = c['kappa_floor'], c['tau_agg'], c['zero_snap']
        self.trunc_thr, self.nf_thr = c['trunc_threshold'], c['nullfloor_threshold']
        self.pin_rel, self.pin_abs = c['pin_derived_tol_rel'], c['pin_derived_tol_abs']
        self.twoleg_rel, self.zero_tol = c['pin_twoleg_tol_rel'], c['zero_ctrl_tol_abs']
        self.recon_abs, self.recon_rel = c['recon_tol_abs_E2_Hill'], c['recon_tol_rel_robust']
        self.l2_t1_abs, self.mono_rel = c['l2null_t1_tol_abs'], c['mono_tol_rel']
        self.syn_t, self.syn_tight = list(c['synthetic_t']), c['synthetic_t_tight']
        self.band = list(c['synthetic_band_fractions'])
        self.k_silent, self.k_void = c['synthetic_k']['silent'], c['synthetic_k']['void']
        self.oom = list(c['oom_factors'])
        self.t_grid, self.axis = list(g['t_grid']), list(g['t2t4_axis'])
        self.rp1, self.rp2 = list(g['richardson_pairs']['one_param']), list(g['richardson_pairs']['two_param'])
        self.area_lo, self.area_hi, self.area_n = g['area_grid']['lo'], g['area_grid']['hi'], g['area_grid']['nodes_per_axis']
        self.d_EM = P['raw']['regime']['d_EM']
        self.raw = P['raw']['keys']
        # rms per family from the closed forms; asserted against constants.rms
        self.rms = {'hexP2': math.sqrt(1.0 / 5.0), 'hexP4': 1.0 / 3.0, 'cubK4': math.sqrt(4.0 / 21.0)}
        for k, v in self.rms.items():
            if c['rms'][k] != v:
                raise Halt('rms closed form %s differs from constants.rms' % k)
        # constants cross-checked against the frozen schema's tolerances
        T = S['tolerances']
        for a, b in (('D', 'D'), ('KD_CLIP', 'KD_CLIP'), ('kappa_floor', 'kappa_floor'), ('mu', 'mu'),
                     ('tau_agg', 'tau_agg'), ('trunc_threshold', 'trunc_threshold'),
                     ('nullfloor_threshold', 'nullfloor_threshold'), ('pin_derived_tol_rel', 'pin_derived_rel'),
                     ('pin_derived_tol_abs', 'pin_derived_abs'), ('pin_twoleg_tol_rel', 'pin_twoleg_rel'),
                     ('zero_ctrl_tol_abs', 'zero_ctrl_abs'), ('recon_tol_abs_E2_Hill', 'recon_abs_E2_Hill'),
                     ('recon_tol_rel_robust', 'recon_rel_robust'), ('l2null_t1_tol_abs', 'l2null_t1_abs'),
                     ('mono_tol_rel', 'mono_rel'), ('edge_twoleg_tol_rel', 'edge_twoleg_rel')):
            if c[a] != T[b]:
                raise Halt('constant %s differs between the pinned file and the schema' % a)
        if P['_meta']['gate'] != GATE or S['gate'] != GATE:
            raise Halt('gate label')
        if S['keys'] != self.keys or S['arms'] != self.arms or S['primary']['keys'] != self.primary_keys:
            raise Halt('structure differs between the pinned file and the schema')
        if S['elections'] != ELECTIONS or P['_meta']['elections_applied']['E-SA-7'] != 'base 05302210 + the G-MSCS1 stratum':
            raise Halt('elections')
        self.i0 = self.t_grid.index(0.0)
        self.n_axis = len(self.axis)

    def branch(self, K):
        return 'hex' if K in self.hex else 'cubic'

    def fam_list(self, K):
        """every family in the pinned layout for this key: mapped ones first, then the null family"""
        return self.mapped[self.branch(K)] + self.null_fams.get(self.branch(K), [])

    def is_mapped(self, K, F):
        return F in self.mapped[self.branch(K)]

    def odf(self, K, F):
        if F == 't2':
            return 'hexP2' if K in self.hex else 'cubP2-i'
        return 'hexP4' if K in self.hex else 'cubK4'

    def rms_of(self, K, F):
        return self.rms['hexP2'] if F == 't2' else (self.rms['hexP4'] if K in self.hex else self.rms['cubK4'])

    def cells(self):
        for K in self.keys:
            for A in self.arms:
                for F in self.mapped[self.branch(K)]:
                    yield K, A, F

    def idx5(self, i, j):
        return self.n_axis * i + j


# --------------------------------------------------------------------------------------------- the derivations
def rich_even(pin, r, h1, h2):
    tg = pin.t_grid

    def E(h):
        return (r[tg.index(h)] + r[tg.index(-h)] - 2.0 * r[pin.i0]) / (2.0 * h * h)
    return (4.0 * E(h1) - E(h2)) / 3.0


def rich_odd(pin, r, h1, h2):
    tg = pin.t_grid

    def O(h):
        return (r[tg.index(h)] - r[tg.index(-h)]) / (2.0 * h)
    return (4.0 * O(h1) - O(h2)) / 3.0


def grid5(pin, R, t2, t4):
    return R[pin.idx5(pin.axis.index(t2), pin.axis.index(t4))]


def rich_mixed(pin, R, h1, h2):
    def M(h):
        return (grid5(pin, R, h, h) - grid5(pin, R, h, -h) - grid5(pin, R, -h, h) + grid5(pin, R, -h, -h)) / (4.0 * h * h)
    return (4.0 * M(h1) - M(h2)) / 3.0


def rich_even_5x5(pin, R, along, h1, h2):
    """even part along one axis of the 5x5 grid, the other coordinate at 0"""
    def val(h):
        return grid5(pin, R, h, 0.0) if along == 't2' else grid5(pin, R, 0.0, h)

    def E(h):
        return (val(h) + val(-h) - 2.0 * val(0.0)) / (2.0 * h * h)
    return (4.0 * E(h1) - E(h2)) / 3.0


def derive_families(pin):
    out = {}
    h1, h2 = pin.rp1
    for K in pin.keys:
        out[K] = {}
        for A in pin.arms:
            out[K][A] = {}
            for F in pin.fam_list(K):
                d = pin.raw[K]['arms'][A][F]
                grid, kappa = d['grid'], d['kappa']
                mapped = pin.is_mapped(K, F)
                kbi = rich_even(pin, grid, h1, h2)
                rec = {'kappa': kappa, 'kappa_bi': kbi, 'S_bi': rich_odd(pin, grid, h1, h2), 'S_fit': d.get('S'),
                       'mapped': mapped, 'odf_reading': pin.odf(K, F), 'r0': grid[pin.i0],
                       'fit_res_rel': (abs(kappa - kbi) / abs(kbi)) if mapped else None}
                # the two-leg relatives are serialized on the mapped families and null on the null family (the pinned layout)
                if 'kappa_cc' in d:
                    rec['twoleg_rel'] = rel_dev(kappa, d['kappa_cc']) if mapped else None
                if 'kappa3_cc' in d:
                    rec['twoleg_kappa3_rel'] = rel_dev(d['kappa3'], d['kappa3_cc']) if mapped else None
                if 'S_cc' in d:
                    rec['twoleg_S_abs'] = abs(d['S'] - d['S_cc'])
                if A == pin.primary_arm and mapped:
                    S, k3 = d['S'], d['kappa3']
                    worst = 0.0
                    for t, r in zip(pin.t_grid, grid):
                        if abs(t) <= pin.D:
                            worst = max(worst, abs(r - (S * t + kappa * t * t + k3 * t * t * t)))
                    rec['recon_max_abs'] = worst
                    rec['trunc_T_at_D'] = abs(k3) * pin.D / abs(kappa)
                out[K][A][F] = rec
    return out


def snap0(pin, x):
    return 0.0 if abs(x) <= pin.snap else x


def build_reach(pin, fam, grids_override=None):
    """R^h and R^w per key and arm; grids_override lets a suite substitute one one-parameter grid"""
    out = {}
    D2 = pin.D * pin.D
    for K in pin.keys:
        out[K] = {}
        for A in pin.arms:
            lo_box = hi_box = 0.0
            vals = []
            for F in pin.mapped[pin.branch(K)]:
                kap = fam[K][A][F]['kappa']
                lo_box += min(0.0, kap * D2)
                hi_box += max(0.0, kap * D2)
                grid = pin.raw[K]['arms'][A][F]['grid']
                if grids_override and (K, A, F) in grids_override:
                    grid = grids_override[(K, A, F)]
                vals += [r for t, r in zip(pin.t_grid, grid) if abs(t) <= pin.D]
            if A == pin.primary_arm:
                vals += list(pin.raw[K]['quadform']['grid5x5_cc'])
            gmin, gmax = min(vals), max(vals)
            hull = [snap0(pin, min(lo_box, gmin)), snap0(pin, max(hi_box, gmax))]
            out[K][A] = {'box': [lo_box, hi_box], 'grid_min': gmin, 'grid_max': gmax,
                         'grid_exceeds_box': bool(gmin < lo_box or gmax > hi_box), 'hull': hull,
                         'widened': [(1.0 + pin.mu) * hull[0], (1.0 + pin.mu) * hull[1]]}
    return out


def build_unions(pin, reach):
    def union(cells, which):
        return [min(reach[K][A][which][0] for K, A in cells), max(reach[K][A][which][1] for K, A in cells)]
    all_cells = [(K, A) for K in pin.keys for A in pin.arms]
    prim = [(K, pin.primary_arm) for K in pin.primary_keys]
    return {'hull_all': union(all_cells, 'hull'), 'hull_primary': union(prim, 'hull'),
            'widened_all': union(all_cells, 'widened'), 'widened_primary': union(prim, 'widened')}


def build_synthetic(pin, U):
    f1, f2 = pin.band
    w, h = U['widened_all'][0], U['hull_all'][0]
    neg = [w + f1 * (h - w), w + f2 * (h - w)]
    h, w = U['hull_all'][1], U['widened_all'][1]
    pos = [h + f1 * (w - h), h + f2 * (w - h)]
    p, q = U['widened_primary'][1], U['hull_all'][1]
    rob = [p + f1 * (q - p), p + f2 * (q - p)]
    return {'margin_negative': neg, 'margin_positive': pos, 'robustness_only_positive': rob}


def build_nulls(pin, fam):
    h1, h2 = pin.rp2
    N1, N2, N3, N4 = {}, {}, {}, {}
    for K, A, F in pin.cells():
        N1['%s/%s/%s' % (K, A, F)] = {'bi': fam[K][A][F]['S_bi'], 'fit': fam[K][A][F]['S_fit'], 'odf_reading': pin.odf(K, F)}
    for K in pin.keys:
        q = pin.raw[K]['quadform']
        N2[K] = {'fit7': q['kappa24_fit7'], 'bi_chat': pin.raw[K]['kappa24_bi_chat'], 'bi_cc': pin.raw[K]['kappa24_bi_cc'],
                 'bi_5x5': rich_mixed(pin, q['grid5x5_cc'], h1, h2),
                 'odf_reading': 'hexP2P4' if K in pin.hex else 'cubP2K4-i'}
    for K in pin.cubic:
        q = pin.raw[K]['quadform']
        f = fam[K][pin.primary_arm]['t2']
        N3[K] = {'fit': f['kappa'], 'bi': f['kappa_bi'], 'odf_reading': 'cubP2-i', 'pure_l2_change_t1': pin.raw[K]['pure_l2_change_t1']}
        N4[K] = {'fit7': q['kappa22_fit7'], 'bi_5x5': rich_even_5x5(pin, q['grid5x5_cc'], 't2', h1, h2),
                 'k12_chat_t2sq': (q['basis_k12_chat'][0] if 'basis_k12_chat' in q else None), 'odf_reading': 'cubP2K4-i'}
    return {'N-1': N1, 'N-2': N2, 'N-3': N3, 'N-4': N4}


def build_hex_quadform(pin, fam):
    h1, h2 = pin.rp2
    out = {}
    for K in pin.hex:
        q = pin.raw[K]['quadform']
        R = q['grid5x5_cc']
        k22, k44, k24 = (rich_even_5x5(pin, R, 't2', h1, h2), rich_even_5x5(pin, R, 't4', h1, h2), rich_mixed(pin, R, h1, h2))
        k2 = fam[K][pin.primary_arm]['t2']['kappa']
        slopes = {}
        for A in [a for a in pin.arms if a != 'h_Hill']:
            slopes[A + '_fit'] = math.sqrt(-fam[K][A]['t2']['kappa'] / fam[K][A]['t4']['kappa'])
            slopes[A + '_bi'] = math.sqrt(-fam[K][A]['t2']['kappa_bi'] / fam[K][A]['t4']['kappa_bi'])
        slopes[pin.primary_arm + '_bi5x5'] = math.sqrt(-k22 / k44)
        hk2, hk4 = fam[K]['h_Hill']['t2']['kappa'], fam[K]['h_Hill']['t4']['kappa']
        form = 'negative-definite' if (hk2 < 0 and hk4 < 0) else ('positive-definite' if (hk2 > 0 and hk4 > 0) else 'indefinite')
        out[K] = {'k22_bi_5x5': k22, 'k24_bi_5x5': k24, 'k44_bi_5x5': k44,
                  'kappa22_fit7_vs_kappa2_rel': abs(q['kappa22_fit7'] - k2) / abs(q['kappa22_fit7']),
                  'null_ray_slope': slopes, 'h_Hill_form': form}
    return out


def build_zero_ctrl(pin):
    return {K: {'%s/%s' % (A, F): {'odf_reading': 'uniform', 'r0': pin.raw[K]['arms'][A][F]['grid'][pin.i0]}
                for A in pin.arms for F in pin.fam_list(K)} for K in pin.keys}


def rederive(pin):
    fam = derive_families(pin)
    reach = build_reach(pin, fam)
    unions = build_unions(pin, reach)
    return {'families': fam, 'reach': reach, 'unions': unions, 'synthetic': build_synthetic(pin, unions),
            'nulls': build_nulls(pin, fam), 'hex_quadform': build_hex_quadform(pin, fam), 'zero_ctrl': build_zero_ctrl(pin)}


def compare_leaves(mine, pinned, rel, absf):
    a, b = dict(leaves(mine)), dict(leaves(pinned))
    mism, worst, missing, extra = 0, 0.0, sorted(set(b) - set(a)), sorted(set(a) - set(b))
    for p in sorted(set(a) & set(b)):
        x, y = a[p], b[p]
        if isnum(x) and isnum(y):
            sc = abs(x - y) / (rel * abs(y) + absf)
            worst = max(worst, sc)
            if sc > 1.0:
                mism += 1
        elif x != y or type(x) != type(y):
            mism += 1
    return mism + len(missing) + len(extra), worst, missing, extra, len(a)


# --------------------------------------------------------------------------------------------- the mapping
class Mapper:
    def __init__(self, pin, fam, reach):
        self.pin, self.fam, self.reach = pin, fam, reach

    def family_record(self, K, A, F, lo, hi):
        pin, f = self.pin, self.fam[K][A][F]
        if not pin.is_mapped(K, F):
            return {'class': 'NULL-INERT', 't_star': None, 't_star_bi': None, 'class_bi': None, 'resolution_sensitive': None,
                    'sigma_star': None, 'window_lo': -pin.D, 'window_hi': pin.D, 'trunc_T': None, 'truncation_sensitive': None,
                    'nu': None, 'nu_is_inf': None, 'nullfloor_sensitive': None, 'binding_end': None}

        def edge(kappa):
            b = hi if kappa > 0 else lo
            if b == 0:
                return b, 0.0
            q = b / kappa
            if q < 0:
                raise Halt('instrument defect: b/kappa < 0 on an interval containing 0')
            return b, math.sqrt(q)
        b, ts = edge(f['kappa'])
        cls = 'BINDING' if ts < pin.D else 'INERT-IN-D'
        bbi, tsbi = edge(f['kappa_bi'])
        clsbi = 'BINDING' if tsbi < pin.D else 'INERT-IN-D'
        rec = {'class': cls, 't_star': ts, 't_star_bi': tsbi, 'class_bi': clsbi, 'resolution_sensitive': cls != clsbi,
               'sigma_star': ts * pin.rms_of(K, F),
               'window_lo': -ts if cls == 'BINDING' else -pin.D, 'window_hi': ts if cls == 'BINDING' else pin.D,
               'binding_end': 'hi' if f['kappa'] > 0 else 'lo'}
        if A == pin.primary_arm:
            T = abs(pin.raw[K]['arms'][A][F]['kappa3']) * ts / abs(f['kappa'])
            rec['trunc_T'], rec['truncation_sensitive'] = T, bool(T > pin.trunc_thr)
        else:
            rec['trunc_T'], rec['truncation_sensitive'] = None, False
        if b == 0:
            rec['nu'], rec['nu_is_inf'], rec['nullfloor_sensitive'] = None, True, True
        else:
            nu = abs(f['S_bi']) * ts / abs(b)
            rec['nu'], rec['nu_is_inf'], rec['nullfloor_sensitive'] = nu, False, bool(nu > pin.nf_thr)
        return rec

    def exclusion_record(self, K, A, lo, hi):
        pin = self.pin
        Rw, Rh = self.reach[K][A]['widened'], self.reach[K][A]['hull']
        if hi < Rw[0] or lo > Rw[1]:
            cls = 'EXCLUDED-IN-D'
            sub = 'SIGN' if ((hi < 0 and Rw[0] >= 0) or (lo > 0 and Rw[1] <= 0)) else 'MAGNITUDE'
        elif not (hi < Rh[0] or lo > Rh[1]):
            cls, sub = 'TUNED-ADMISSIBLE', None
        else:
            cls, sub = 'MARGIN', None
        sgn = 1 if lo > 0 else -1
        out = {}
        for F in pin.mapped[pin.branch(K)]:
            kap = self.fam[K][A][F]['kappa']
            rec = {'class': cls, 'subreason': sub, 't_in': None, 't_out': None, 'can_supply_alone': None}
            if (kap > 0) == (sgn > 0):
                t_in = math.sqrt(min(abs(lo), abs(hi)) / abs(kap))
                rec['t_in'], rec['t_out'], rec['can_supply_alone'] = t_in, math.sqrt(max(abs(lo), abs(hi)) / abs(kap)), bool(t_in <= pin.D)
            out[F] = rec
        return out

    def two_param(self, K, A, lo, hi):
        pin = self.pin
        k2, k44 = self.fam[K][A]['t2']['kappa'], self.fam[K][A]['t4']['kappa']
        n, a_lo, a_hi = pin.area_n, pin.area_lo, pin.area_hi
        nodes = [a_lo + i * (a_hi - a_lo) / (n - 1) for i in range(n)]
        last = n - 1
        adm, total, boundary = 0, 0, False
        sq4 = [k44 * t4 * t4 for t4 in nodes]
        for i, t2 in enumerate(nodes):
            s2 = k2 * t2 * t2
            for j in range(n):
                total += 1
                v = s2 + sq4[j]
                if lo <= v <= hi:
                    adm += 1
                    if i == 0 or i == last or j == 0 or j == last:
                        boundary = True
        prod = k2 * k44
        return {'area_fraction': adm / total, 'admissible_nodes': adm, 'total_nodes': total,
                'null_ray_slope': (math.sqrt(-k2 / k44) if prod < 0 else None),
                'definiteness': ('indefinite' if prod < 0 else ('negative-definite' if k2 < 0 else 'positive-definite')),
                'compact': not boundary}

    def map_interval(self, lo, hi):
        pin = self.pin
        if lo <= 0 <= hi:
            fam = {K: {A: {F: self.family_record(K, A, F, lo, hi) for F in pin.fam_list(K)} for A in pin.arms} for K in pin.keys}
            tp = {K: {A: self.two_param(K, A, lo, hi) for A in pin.arms} for K in pin.hex}
            return {'contains_zero': True, 'families': fam, 'exclusion': None, 'two_param': tp}
        exc = {K: {A: self.exclusion_record(K, A, lo, hi) for A in pin.arms} for K in pin.keys}
        return {'contains_zero': False, 'families': None, 'exclusion': exc, 'two_param': None}

    def gate_class(self, m):
        pin = self.pin
        if m['contains_zero']:
            fam = m['families']
            ok = all(fam[K][pin.primary_arm]['t4']['class'] == 'BINDING' for K in pin.primary_keys)
            return 'WINDOW-DELIVERED' if ok else 'INERT-IN-D'
        classes = [m['exclusion'][K][A][pin.mapped[pin.branch(K)][0]]['class'] for K in pin.keys for A in pin.arms]
        if all(c == 'EXCLUDED-IN-D' for c in classes):
            return 'KILL-IN-D'
        if any(c == 'TUNED-ADMISSIBLE' for c in classes):
            return 'TUNED'
        return 'MARGIN-ONLY'

    def map_rows(self, rows, scale=1.0):
        """rows: list of dicts with lo, hi, k_em_max, k_t_max (floats) and id, row_md5; never serialized as such"""
        pin = self.pin
        out_rows, ints = [], []
        for r in rows:
            x = max(r['k_em_max'], r['k_t_max']) * pin.d_EM
            void = bool(x > pin.KD)
            rec = {'id': r['id'], 'row_md5': r.get('row_md5'), 'void_regime': void,
                   'contains_zero': None, 'families': None, 'exclusion': None, 'two_param': None}
            if not void:
                lo, hi = r['lo'] * scale, r['hi'] * scale
                ints.append((lo, hi))
                rec.update(self.map_interval(lo, hi))
            out_rows.append(rec)
        n_void = sum(1 for r in out_rows if r['void_regime'])
        res = {'n_void_rows': n_void, 'rows': out_rows, 'combined': None, 'combined_empty': False, 'contains_zero': None,
               'sigma_union_hi': None, 'sigma_strict_hi': None}
        if not ints:
            res['gate_class'] = 'VOID'
            return res
        lo, hi = max(a for a, _ in ints), min(b for _, b in ints)
        if lo > hi:
            res['combined_empty'] = True
            res['gate_class'] = 'ANCHOR-INCONSISTENT'
            return res
        m = self.map_interval(lo, hi)
        res['contains_zero'] = m['contains_zero']
        res['combined'] = {'families': m['families'], 'exclusion': m['exclusion'], 'two_param': m['two_param']}
        res['gate_class'] = self.gate_class(m)
        sig = None
        if m['contains_zero']:
            recs = [m['families'][K][pin.primary_arm]['t4'] for K in pin.primary_keys]
            if all(r['class'] == 'BINDING' for r in recs):
                sig = (max(r['sigma_star'] for r in recs), min(r['sigma_star'] for r in recs))
        res['sigma_union_hi'], res['sigma_strict_hi'] = (sig if sig else (None, None))
        return res

    def map_with_oom(self, rows):
        base = self.map_rows(rows)
        up = self.map_rows(rows, scale=self.pin.oom[2])
        down = self.map_rows(rows, scale=self.pin.oom[0])
        if self.pin.oom[1] != 1.0:
            raise Halt('oom factors')
        worst, viol, notes = mono_check(self.pin, base, up, down)
        return base, up, down, worst, viol, notes


def mono_check(pin, base, up, down):
    """A-2.2 MONO / memo 3.8: exact sqrt(10) / sqrt(0.1) scaling of unclipped raw edges; monotone clipped windows and classes"""
    worst, viol, notes = 0.0, 0, []
    if base['combined'] is None or up['combined'] is None or down['combined'] is None:
        return worst, viol, ['no combined interval on some scaling; nothing to check']
    su, sd = math.sqrt(pin.oom[2]), math.sqrt(pin.oom[0])
    if base['contains_zero']:
        rank = {'BINDING': 0, 'INERT-IN-D': 1}
        for K, A, F in pin.cells():
            b, u, d = (x['combined']['families'][K][A][F] for x in (base, up, down))
            if b['t_star'] > 0:
                worst = max(worst, abs(u['t_star'] / b['t_star'] - su) / su, abs(d['t_star'] / b['t_star'] - sd) / sd)
            if b['t_star_bi'] > 0:
                worst = max(worst, abs(u['t_star_bi'] / b['t_star_bi'] - su) / su, abs(d['t_star_bi'] / b['t_star_bi'] - sd) / sd)
            if rank[u['class']] < rank[b['class']] or u['window_hi'] < b['window_hi']:
                viol += 1
                notes.append('x10 narrowed %s/%s/%s' % (K, A, F))
            if rank[d['class']] > rank[b['class']] or d['window_hi'] > b['window_hi']:
                viol += 1
                notes.append('x0.1 widened %s/%s/%s' % (K, A, F))
    else:
        rank = {'TUNED-ADMISSIBLE': 0, 'MARGIN': 1, 'EXCLUDED-IN-D': 2}
        for K, A, F in pin.cells():
            b, u, d = (x['combined']['exclusion'][K][A][F] for x in (base, up, down))
            for key in ('t_in', 't_out'):
                if b[key] is not None and b[key] > 0:
                    worst = max(worst, abs(u[key] / b[key] - su) / su, abs(d[key] / b[key] - sd) / sd)
            if rank[u['class']] < rank[b['class']]:
                viol += 1
                notes.append('x10 moved %s/%s toward admissible' % (K, A))
            if rank[d['class']] > rank[b['class']]:
                viol += 1
                notes.append('x0.1 moved %s/%s toward excluded' % (K, A))
    return worst, viol, notes


# --------------------------------------------------------------------------------------------- the masked parser
REQUIRED = ['id', 'class', 'delta_def', 'lo', 'hi', 'cl', 'reading', 'geom', 'k_em_max', 'k_t_max', 'src']
OPTIONAL = ['q', 'note']
CANON = REQUIRED + OPTIONAL
FREE_TEXT = {'src', 'note'}
NUM_RE = re.compile(r'^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$')
BAD_UNICODE = {'\u0085', ' ', ' ', '﻿'}
SEP = ' | '


def is_bad_char(c):
    o = ord(c)
    return (o < 32 and c != '\n') or (127 <= o < 160) or c in BAD_UNICODE


def plain_number(s):
    if not NUM_RE.match(s):
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def parse_masked(raw, tokens):
    """A-2.3 / memo 4.1-4.4. Returns (rows, census, row_md5s); raises MaskedAbort(reason) -- the reason never carries a value."""
    if raw.startswith(b'\xef\xbb\xbf'):
        raise MaskedAbort('BOM')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise MaskedAbort('NOT_UTF8')
    if any(is_bad_char(c) for c in text):
        raise MaskedAbort('CONTROL_OR_SEPARATOR_CHAR')
    if not text.endswith('\n'):
        raise MaskedAbort('NO_FINAL_LF')
    if text.endswith('\n\n'):
        raise MaskedAbort('BLANK_LINE_AT_END')
    row_bytes = raw[:-1].split(b'\n')
    rows, md5s, fields_per_row, per_class = [], [], [], {}
    for n, rb in enumerate(row_bytes, 1):
        line = rb.decode('utf-8')
        tag = 'row %d' % n
        if line.strip() == '':
            raise MaskedAbort(tag + ' BLANK_LINE')
        if line.startswith('|') or line.endswith('|'):
            raise MaskedAbort(tag + ' LEADING_OR_TRAILING_BAR')
        fields = line.split(SEP)
        if any('|' in f for f in fields):
            raise MaskedAbort(tag + ' SEPARATOR_COLLISION')
        keys, vals = [], {}
        for f in fields:
            if '=' not in f:
                raise MaskedAbort(tag + ' FIELD_WITHOUT_EQUALS')
            k, v = f.split('=', 1)
            if k not in CANON:
                raise MaskedAbort(tag + ' UNKNOWN_KEY')
            if k in vals:
                raise MaskedAbort(tag + ' DUPLICATE_KEY ' + k)
            keys.append(k)
            vals[k] = v
        missing = [k for k in REQUIRED if k not in vals]
        if missing:
            raise MaskedAbort(tag + ' MISSING_KEY ' + ','.join(missing))
        if keys != [k for k in CANON if k in vals]:
            raise MaskedAbort(tag + ' KEY_ORDER')
        for k, v in vals.items():
            if v == '' or v != v.strip():
                raise MaskedAbort(tag + ' EMPTY_OR_PADDED ' + k)
            if k not in FREE_TEXT and not all(32 <= ord(c) < 127 for c in v):
                raise MaskedAbort(tag + ' NON_ASCII ' + k)
        if vals['id'] != 'SA-%d' % n:
            raise MaskedAbort(tag + ' ID_SEQUENCE')
        if vals['class'] not in tokens['class']:
            raise MaskedAbort(tag + ' CLASS_NOT_READ_BY_THIS_GATE')
        if vals['delta_def'] != tokens['delta_def']:
            raise MaskedAbort(tag + ' WRONG_DELTA_DEF')
        lo, hi = plain_number(vals['lo']), plain_number(vals['hi'])
        if lo is None or hi is None:
            raise MaskedAbort(tag + ' NOT_A_PLAIN_NUMBER lo/hi')
        if not lo <= hi:
            raise MaskedAbort(tag + ' ORDER')
        cl = vals['cl']
        if cl != 'hard':
            c = plain_number(cl)
            if c is None or not (0.0 < c < 1.0):
                raise MaskedAbort(tag + ' CL_NOT_IN_OPEN_UNIT_INTERVAL_OR_hard')
        if vals['reading'] not in tokens['reading_conformant']:
            raise MaskedAbort(tag + (' READING_NOT_MAPPED' if vals['reading'] in tokens['reading_frozen_list'] else ' UNKNOWN_READING'))
        if vals['geom'] not in tokens['geom']:
            raise MaskedAbort(tag + ' UNKNOWN_GEOM')
        kem, kt = plain_number(vals['k_em_max']), plain_number(vals['k_t_max'])
        if kem is None or kt is None or kem <= 0 or kt <= 0:
            raise MaskedAbort(tag + ' K_NOT_A_POSITIVE_PLAIN_NUMBER')
        if 'q' in vals and vals['q'] not in tokens['q']:
            raise MaskedAbort(tag + ' UNKNOWN_Q')
        rows.append({'id': vals['id'], 'lo': lo, 'hi': hi, 'k_em_max': kem, 'k_t_max': kt, 'row_md5': md5b(rb)})
        md5s.append(md5b(rb))
        fields_per_row.append(len(fields))
        per_class[vals['class']] = per_class.get(vals['class'], 0) + 1
    if not rows:
        raise MaskedAbort('NO_ROWS')
    return rows, {'rows': len(rows), 'per_class': per_class, 'fields_per_row': fields_per_row}, md5s


def unarmor(raw):
    """base64 text (marker lines stripped, whitespace ignored) or a zip with exactly one member"""
    if raw[:2] == b'PK':
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names = z.namelist()
            if len(names) != 1:
                raise MaskedAbort('ZIP_MEMBER_COUNT')
            return z.read(names[0])
    body = ''.join(l for l in raw.decode('ascii', 'replace').splitlines() if not l.startswith('====='))
    return base64.b64decode(re.sub(r'\s+', '', body), validate=True)


def open_sealed(rel):
    if not STATE['phase3_active']:
        STATE['sealed_opens_before_phase3'] += 1
        raise Halt('MASK: sealed open attempted outside Phase 3')
    data = unarmor(read(rel))
    h = md5b(data)
    if h != SEALED_MD5 or len(data) != SEALED_BYTES:
        raise Halt('SEALED identity: md5 %s bytes %d (stated %s, %d)' % (h, len(data), SEALED_MD5, SEALED_BYTES))
    return data, h, len(data)


# --------------------------------------------------------------------------------------------- Phase 0
def phase0(pin, scanner, pats, sources, t1_result, derived_mine):
    P, R, res = pin.P, {}, {}

    def item(name, passed, floats, detail):
        e = {'passed': bool(passed), 'odf_reading': PHASE0_ODF[name], 'detail': detail}
        e.update(floats)
        R[name] = e
        log('  %-24s %s  %s' % (name, 'PASS' if passed else 'FAIL', ' '.join('%s=%s' % (k, repr(v)) for k, v in floats.items())))
        if not passed:
            raise Halt('Phase 0 %s failed -> INDETERMINATE' % name)

    # PIN: identity, re-read through provenance, two-leg agreement
    prov, dqf_keys = P['provenance'], set(sources['DQF'].keys())
    n_checked, mism, covered = 0, 0, set()
    for field, spec in prov.items():
        src = sources[spec['src']]
        if field.startswith('keys/<K>/'):
            sub = field[len('keys/<K>/'):]
            for K in pin.keys:
                if spec['scope'] == 'cubic' and K not in pin.cubic:
                    continue
                if spec['scope'] == 'dqf' and K not in dqf_keys:
                    continue
                want = jptr(pin.raw[K], '/' + sub)
                got = jptr(src, spec['pointer'].replace('{K}', K))
                n_checked += 1
                covered.add('/keys/%s/%s' % (K, sub))
                if json.dumps(want, sort_keys=True) != json.dumps(got, sort_keys=True):
                    mism += 1
        else:
            want = jptr(P, '/' + field) if field.startswith('raw/') else jptr(P['grids'], '/' + field[len('grids/'):])
            got = jptr(src, spec['pointer'])
            n_checked += 1
            covered.add('/' + field[len('raw/'):] if field.startswith('raw/') else '/grids/' + field[len('grids/'):])
            if json.dumps(want, sort_keys=True) != json.dumps(got, sort_keys=True):
                mism += 1
    raw_leaf_paths = {p for p, _ in leaves(P['raw'])}
    uncovered = []
    for p in sorted(raw_leaf_paths):
        base = re.sub(r'/\d+$', '', p)
        while base and base not in covered and re.search(r'/\d+$', base):
            base = re.sub(r'/\d+$', '', base)
        if p in covered or base in covered:
            continue
        if p.endswith('/branch') and jptr(P['raw'], p) == pin.branch(p.split('/')[2]):
            continue
        uncovered.append(p)
    wk = wk3 = wb1 = wS = 0.0
    for K in pin.keys:
        for A in pin.arms:
            for F in pin.fam_list(K):
                d = pin.raw[K]['arms'][A][F]
                if 'kappa_cc' in d and max(abs(d['kappa']), abs(d['kappa_cc'])) > pin.floor:
                    wk = max(wk, rel_dev(d['kappa'], d['kappa_cc']))
                if 'kappa3_cc' in d and max(abs(d['kappa3']), abs(d['kappa3_cc'])) > pin.floor:
                    wk3 = max(wk3, rel_dev(d['kappa3'], d['kappa3_cc']))
                if 'S_cc' in d:
                    wS = max(wS, abs(d['S'] - d['S_cc']))
        q = pin.raw[K]['quadform']
        if max(abs(q['kappa22_fit7']), abs(q['kappa22_fit7_cc'])) > pin.floor:
            wk = max(wk, rel_dev(q['kappa22_fit7'], q['kappa22_fit7_cc']))
        wb1 = max(wb1, rel_dev(pin.raw[K]['b1_Hill'], pin.raw[K]['b1_Hill_cc']))
    ok = (mism == 0 and not uncovered and wk <= pin.twoleg_rel and wk3 <= pin.twoleg_rel and wb1 <= pin.twoleg_rel and wS <= pin.tau)
    item('F-CTRL-SA-PIN', ok, {'raw_mismatches': mism, 'worst_twoleg_kappa_rel': wk, 'worst_twoleg_kappa3_rel': wk3,
                               'worst_twoleg_b1_rel': wb1, 'worst_twoleg_S_abs': wS},
         'pinned md5 guarded; %d values re-read through provenance pointers from the seven sources at their md5s; raw leaves not covered by a pointer: %d' % (n_checked, len(uncovered)))
    res['pin'] = {'values_checked': n_checked, 'raw_leaves': len(raw_leaf_paths), 'uncovered': uncovered}

    # PIN-DERIVED
    pinned_derived = {k: v for k, v in P['derived'].items() if k != 'summary'}
    mism, worst, missing, extra, nleaves = compare_leaves(derived_mine, pinned_derived, pin.pin_rel, pin.pin_abs)
    item('F-CTRL-SA-PIN-DERIVED', mism == 0 and worst <= 1.0, {'leaf_mismatches': mism, 'worst_scaled_dev': worst},
         '%d leaves re-derived with this instrument; missing %d, extra %d' % (nleaves, len(missing), len(extra)))
    res['derived_leaves'] = nleaves

    # ZERO
    w = max(abs(pin.raw[K]['arms'][A][F]['grid'][pin.i0]) for K in pin.keys for A in pin.arms for F in pin.fam_list(K))
    item('F-CTRL-SA-ZERO', w <= pin.zero_tol, {'worst_abs_r0': w}, 'the banked grid value at t = 0 on every key, arm and family')

    # RECON
    fam = derived_mine['families']
    wE = max(fam[K][pin.primary_arm][F]['recon_max_abs'] for K in pin.keys for F in pin.mapped[pin.branch(K)])
    wR = max(fam[K][A][F]['fit_res_rel'] for K, A, F in pin.cells() if A in pin.robust_arms)
    item('F-CTRL-SA-RECON', wE <= pin.recon_abs and wR <= pin.recon_rel, {'worst_abs_E2_Hill': wE, 'worst_rel_robust': wR},
         'three-term reconstruction on the primary arm inside D; fit vs basis-independent kappa on the robustness arms')

    # S (N-1)
    wb = max(abs(fam[K][A][F]['S_bi']) for K, A, F in pin.cells())
    wf = max(abs(fam[K][A][F]['S_fit']) for K, A, F in pin.cells() if fam[K][A][F]['S_fit'] is not None)
    item('F-CTRL-SA-S', wb <= pin.tau and wf <= pin.tau, {'worst_abs_bi': wb, 'worst_abs_fit': wf}, 'first-order slope null on every mapped cell')

    # K24 (N-2)
    N2 = derived_mine['nulls']['N-2']
    wb = max(max(abs(N2[K]['bi_chat']), abs(N2[K]['bi_cc']), abs(N2[K]['bi_5x5'])) for K in pin.keys)
    wf = max(abs(N2[K]['fit7']) for K in pin.keys)
    item('F-CTRL-SA-K24', wb <= pin.floor and wf <= pin.floor, {'worst_abs_bi': wb, 'worst_abs_fit7': wf}, 'kappa24 on all eight keys: chat diagnostic, CC checkpoint, own 5x5 mixed Richardson, fit7')

    # L2NULL (N-3, N-4)
    N3, N4 = derived_mine['nulls']['N-3'], derived_mine['nulls']['N-4']
    w2 = max(max(abs(N3[K]['fit']), abs(N3[K]['bi'])) for K in pin.cubic)
    w22 = max(max(abs(N4[K]['fit7']), abs(N4[K]['bi_5x5']), abs(N4[K]['k12_chat_t2sq'] or 0.0)) for K in pin.cubic)
    wt1 = max(abs(pin.raw[K]['pure_l2_change_t1']) for K in pin.cubic)
    item('F-CTRL-SA-L2NULL', w2 <= pin.floor and w22 <= pin.floor and wt1 <= pin.l2_t1_abs,
         {'worst_abs_kappa2': w2, 'worst_abs_kappa22': w22, 'worst_abs_t2_alone_t1': wt1}, CUBP2_II_IDENTITY)

    # SIGN
    mapper = Mapper(pin, fam, derived_mine['reach'])
    kref = abs(fam['hex_step|a'][pin.primary_arm]['t4']['kappa'])
    m = mapper.map_interval(-kref * SYN_T_ASYM_LO ** 2, kref * SYN_T_ASYM_HI ** 2)
    bad = 0
    for K, A, F in pin.cells():
        r, kap = m['families'][K][A][F], fam[K][A][F]['kappa']
        want_end = 'hi' if kap > 0 else 'lo'
        want_t = (SYN_T_ASYM_HI if kap > 0 else SYN_T_ASYM_LO) * math.sqrt(kref / abs(kap))
        if r['binding_end'] != want_end or abs(r['t_star'] - want_t) > 1e-12 * want_t:
            bad += 1
    item('F-CTRL-SA-SIGN', bad == 0, {'binding_end_mismatches': bad}, 'asymmetric synthetic interval: hi binds where kappa > 0, lo where kappa < 0, on every mapped cell')

    # GRID
    counts = grid_counts(pin)
    enum = {'n_t_grid': len(list(pin.t_grid)), 'n_fit_window_inclusive': len([t for t in pin.t_grid if abs(t) <= pin.D]),
            'n_fit_window_strict': len([t for t in pin.t_grid if abs(t) < pin.D]),
            'n_window_0p1_inclusive': len([t for t in pin.t_grid if abs(t) <= 0.1]),
            'n_window_0p1_strict': len([t for t in pin.t_grid if abs(t) < 0.1]),
            'n_t2t4_axis': len(pin.axis), 'n_t2t4_grid': len([(a, b) for a in pin.axis for b in pin.axis]),
            'n_area_grid': len([(i, j) for i in range(pin.area_n) for j in range(pin.area_n)])}
    cm = sum(1 for k in counts if counts[k] != enum[k])
    item('F-CTRL-SA-GRID', cm == 0, {'count_mismatches': cm}, 'every count computed from the generators (formula vs enumeration)')

    # MONO on the C-SYN-1 intervals
    worst, viol = 0.0, 0
    for t in pin.syn_t:
        b = kref * t * t
        rows = [{'id': 'SA-1', 'lo': -b, 'hi': b, 'k_em_max': pin.k_silent, 'k_t_max': pin.k_silent}]
        _, _, _, w, v, _ = mapper.map_with_oom(rows)
        worst, viol = max(worst, w), viol + v
    item('F-CTRL-SA-MONO', worst <= pin.mono_rel and viol == 0, {'worst_scaling_rel': worst, 'monotonicity_violations': viol},
         'C-SYN-1 intervals scaled x10 and x0.1: exact sqrt scaling of raw edges, monotone windows and classes')

    # MASK
    item('F-CTRL-SA-MASK', STATE['sealed_opens_before_phase3'] == 0, {'sealed_opens_before_phase3': STATE['sealed_opens_before_phase3']},
         'the sealed file is opened only in Phase 3; md5, bytes and census asserted at every open; masked parser')

    # T1
    per_file, hits, coll = t1_result
    item('F-CTRL-SA-T1', hits == 0, {'hits': hits, 'collisions': coll}, 'instrument, memo, pinned file, lock record, schema, comparator under gate list + A1')
    return R, res, mapper


def grid_counts(pin):
    tg = pin.t_grid
    return {'n_t_grid': len(tg), 'n_fit_window_inclusive': sum(abs(t) <= pin.D for t in tg), 'n_fit_window_strict': sum(abs(t) < pin.D for t in tg),
            'n_window_0p1_inclusive': sum(abs(t) <= 0.1 for t in tg), 'n_window_0p1_strict': sum(abs(t) < 0.1 for t in tg),
            'n_t2t4_axis': len(pin.axis), 'n_t2t4_grid': len(pin.axis) ** 2, 'n_area_grid': pin.area_n ** 2}


# --------------------------------------------------------------------------------------------- Phase 2
def synthetic_rows(pin, intervals, k=None):
    k = pin.k_silent if k is None else k
    return [{'id': 'SA-%d' % (i + 1), 'lo': lo, 'hi': hi, 'k_em_max': k, 'k_t_max': k} for i, (lo, hi) in enumerate(intervals)]


def phase2(pin, mapper, derived_mine, tokens, scanner, pats):
    fam, U, SYN = derived_mine['families'], derived_mine['unions'], derived_mine['synthetic']
    kref = abs(fam['hex_step|a'][pin.primary_arm]['t4']['kappa'])
    res = {}

    def suite(name, passed, detail):
        res[name] = {'passed': bool(passed), 'detail': detail}
        log('  %-9s %s  %s' % (name, 'PASS' if passed else 'FAIL', detail))

    def budget(t):
        return kref * t * t

    def fam_of(m, K, A, F):
        return m['combined']['families'][K][A][F]

    def exc_of(m, K, A):
        return m['combined']['exclusion'][K][A][pin.mapped[pin.branch(K)][0]]

    # C-SYN-1
    ok, notes = True, []
    for t in pin.syn_t:
        m = mapper.map_rows(synthetic_rows(pin, [(-budget(t), budget(t))]))
        r = fam_of(m, 'hex_step|a', pin.primary_arm, 't4')
        ok &= abs(r['t_star'] - t) <= 1e-12 * t and r['class'] == ('BINDING' if t < pin.D else 'INERT-IN-D')
        for K, A, F in pin.cells():
            want = math.sqrt(budget(t) / abs(fam[K][A][F]['kappa']))
            ok &= abs(fam_of(m, K, A, F)['t_star'] - want) <= 1e-12 * want
        notes.append('%s:%s' % (t, m['gate_class']))
    suite('C-SYN-1', ok, 'symmetric budgets on the reference cell and every cell; gate ' + ', '.join(notes))
    # C-SYN-2
    m = mapper.map_rows(synthetic_rows(pin, [(-budget(SYN_T_ASYM_LO), budget(SYN_T_ASYM_HI))]))
    ok = True
    for K, A, F in pin.cells():
        kap, r = fam[K][A][F]['kappa'], fam_of(m, K, A, F)
        want = (SYN_T_ASYM_HI if kap > 0 else SYN_T_ASYM_LO) * math.sqrt(kref / abs(kap))
        ok &= r['binding_end'] == ('hi' if kap > 0 else 'lo') and abs(r['t_star'] - want) <= 1e-12 * want
    suite('C-SYN-2', ok, 'asymmetric interval: binding ends by sign(kappa), t* by the binding end on every cell')
    # C-SYN-3
    Up, Um, Hp = U['widened_all'][1], U['widened_all'][0], U['hull_all'][1]
    m1 = mapper.map_rows(synthetic_rows(pin, [(10 * Up, 20 * Up)]))
    ok1 = m1['gate_class'] == 'KILL-IN-D'
    for K in pin.keys:
        for A in pin.arms:
            e, Rw = exc_of(m1, K, A), derived_mine['reach'][K][A]['widened']
            ok1 &= e['class'] == 'EXCLUDED-IN-D' and e['subreason'] == ('MAGNITUDE' if Rw[1] > 0 else 'SIGN')
    m2 = mapper.map_rows(synthetic_rows(pin, [(20 * Um, 10 * Um)]))
    ok2 = m2['gate_class'] == 'KILL-IN-D'
    for K in pin.keys:
        for A in pin.arms:
            e, Rw = exc_of(m2, K, A), derived_mine['reach'][K][A]['widened']
            ok2 &= e['class'] == 'EXCLUDED-IN-D' and e['subreason'] == ('MAGNITUDE' if Rw[0] < 0 else 'SIGN')
    m3 = mapper.map_rows(synthetic_rows(pin, [(0.25 * Hp, 0.5 * Hp)]))
    ok3 = m3['gate_class'] == 'TUNED' and any(exc_of(m3, K, A)['class'] == 'TUNED-ADMISSIBLE' for K in pin.keys for A in pin.arms)
    m4 = mapper.map_rows(synthetic_rows(pin, [tuple(SYN['robustness_only_positive'])]))
    prim_tuned = any(exc_of(m4, K, pin.primary_arm)['class'] == 'TUNED-ADMISSIBLE' for K in pin.primary_keys)
    rob_tuned = any(exc_of(m4, K, A)['class'] == 'TUNED-ADMISSIBLE' for K in pin.keys for A in pin.arms if not (A == pin.primary_arm and K in pin.primary_keys))
    ok4 = m4['gate_class'] == 'TUNED' and not prim_tuned and rob_tuned
    suite('C-SYN-3', ok1 and ok2 and ok3 and ok4, 'excluding-zero intervals: (i) %s (ii) %s (iii) %s (iv) %s' % (m1['gate_class'], m2['gate_class'], m3['gate_class'], m4['gate_class']))
    # C-SYN-4
    m = mapper.map_rows(synthetic_rows(pin, [(-1.0, 1.0)]))
    suite('C-SYN-4', m['gate_class'] == 'INERT-IN-D' and all(fam_of(m, K, A, F)['class'] == 'INERT-IN-D' for K, A, F in pin.cells()), 'wide interval: INERT-IN-D everywhere; gate ' + m['gate_class'])
    # C-SYN-5
    ok = True
    for t in pin.syn_t:
        m = mapper.map_rows(synthetic_rows(pin, [(-budget(t), budget(t))]))
        for K in pin.cubic:
            for A in pin.arms:
                for F in pin.null_fams['cubic']:
                    r = fam_of(m, K, A, F)
                    ok &= r['class'] == 'NULL-INERT' and r['window_lo'] == -pin.D and r['window_hi'] == pin.D and r['t_star'] is None
    suite('C-SYN-5', ok, 'the fcc t2 family is NULL-INERT with window D under C-SYN-1')
    # C-SYN-6
    ok, codes = csyn6(tokens)
    suite('C-SYN-6', ok, 'fifteen malformed files abort masked with reason codes; the valid file parses; no synthetic value in any output: ' + '; '.join(codes))
    # C-SYN-7
    worst, viol = 0.0, 0
    for t in pin.syn_t:
        _, _, _, w, v, _ = mapper.map_with_oom(synthetic_rows(pin, [(-budget(t), budget(t))]))
        worst, viol = max(worst, w), viol + v
    suite('C-SYN-7', worst <= pin.mono_rel and viol == 0, 'OOM on the C-SYN-1 intervals: worst scaling rel %r, violations %d' % (worst, viol))
    # C-SYN-8
    m = mapper.map_rows(synthetic_rows(pin, [(-budget(SYN_T_ASYM_LO), budget(SYN_T_ASYM_LO)), (-budget(SYN_T_ASYM_HI), budget(SYN_T_OUTER))]))
    r = fam_of(m, 'hex_step|a', pin.primary_arm, 't4')
    r2 = fam_of(m, 'hex_step|a', pin.primary_arm, 't2')
    ok = (abs(r['t_star'] - SYN_T_ASYM_LO) <= 1e-12 * SYN_T_ASYM_LO and r['binding_end'] == 'hi'
          and abs(r2['t_star'] - SYN_T_ASYM_HI * math.sqrt(kref / abs(fam['hex_step|a'][pin.primary_arm]['t2']['kappa']))) <= 1e-12 and r2['binding_end'] == 'lo'
          and m['combined_empty'] is False and m['n_void_rows'] == 0 and len(m['rows']) == 2)
    suite('C-SYN-8', ok, 'two consistent rows: the intersection is mapped (upper end from row 1, lower end from row 2)')
    # C-SYN-9
    m = mapper.map_rows(synthetic_rows(pin, [(budget(SYN_T_ASYM_LO), budget(SYN_T_OUTER)), (-budget(SYN_T_OUTER), -budget(SYN_T_ASYM_LO))]))
    suite('C-SYN-9', m['gate_class'] == 'ANCHOR-INCONSISTENT' and m['combined_empty'] and m['combined'] is None, 'two disjoint rows: ' + m['gate_class'])
    # C-SYN-10
    t = pin.syn_t[1]
    ma = mapper.map_rows(synthetic_rows(pin, [(-budget(t), budget(t))], k=pin.k_void))
    rows = synthetic_rows(pin, [(-budget(t), budget(t))], k=pin.k_void) + synthetic_rows(pin, [(-budget(t), budget(t))])
    rows[1]['id'] = 'SA-2'
    mb = mapper.map_rows(rows)
    mc = mapper.map_rows(synthetic_rows(pin, [(-budget(t), budget(t))]))
    ok = (ma['gate_class'] == 'VOID' and ma['rows'][0]['void_regime'] and ma['n_void_rows'] == 1 and ma['combined'] is None
          and mb['rows'][0]['void_regime'] and not mb['rows'][1]['void_regime'] and mb['n_void_rows'] == 1
          and json.dumps(mb['combined'], sort_keys=True) == json.dumps(mc['combined'], sort_keys=True) and mb['gate_class'] == mc['gate_class'])
    suite('C-SYN-10', ok, 'regime clause: a void-k row is VOID-REGIME; alone -> gate %s; with a silent row the silent row alone is mapped' % ma['gate_class'])
    # C-SYN-11
    m = mapper.map_rows(synthetic_rows(pin, [(0.0, 0.0)]))
    ok = m['gate_class'] == 'WINDOW-DELIVERED'
    for K, A, F in pin.cells():
        r = fam_of(m, K, A, F)
        ok &= r['t_star'] == 0.0 and r['nu'] is None and r['nu_is_inf'] is True and r['nullfloor_sensitive'] is True and r['class'] == 'BINDING'
    suite('C-SYN-11', ok, 'the point interval: t* = 0, nu infinite, NULL-FLOOR set, BINDING on every mapped cell; gate ' + m['gate_class'])
    # C-SYN-12
    b = budget(pin.syn_tight)
    m = mapper.map_rows(synthetic_rows(pin, [(-b, b)]))
    ok, nset, nclear = True, 0, 0
    for K, A, F in pin.cells():
        r, f = fam_of(m, K, A, F), fam[K][A][F]
        ts = math.sqrt(b / abs(f['kappa']))
        want = abs(f['S_bi']) * ts / b > pin.nf_thr
        ok &= r['nullfloor_sensitive'] == want
        nset += want
        nclear += not want
    suite('C-SYN-12', ok and nset >= 1 and nclear >= 1, 'tight budget: the null-floor flag recomputed per cell; set on %d cells, clear on %d' % (nset, nclear))
    # C-SYN-13
    ok, notes = True, []
    for name in ('margin_positive', 'margin_negative'):
        m = mapper.map_rows(synthetic_rows(pin, [tuple(SYN[name])]))
        cl = [exc_of(m, K, A)['class'] for K in pin.keys for A in pin.arms]
        ok &= m['gate_class'] == 'MARGIN-ONLY' and 'TUNED-ADMISSIBLE' not in cl and 'MARGIN' in cl
        notes.append('%s:%s' % (name, m['gate_class']))
    suite('C-SYN-13', ok, 'the pinned MARGIN-band intervals: ' + ', '.join(notes))
    # C-SYN-14
    K0, A0 = 'cubic_step|001', pin.primary_arm
    grid = list(pin.raw[K0]['arms'][A0]['t4']['grid'])
    grid[pin.t_grid.index(0.02)] += 5e-13
    reach2 = build_reach(pin, fam, {(K0, A0, 't4'): grid})
    grid0 = list(pin.raw[K0]['arms'][A0]['t4']['grid'])
    grid0[pin.i0] += 5e-13
    reach3 = build_reach(pin, fam, {(K0, A0, 't4'): grid0})
    m2 = Mapper(pin, fam, reach2)
    mm = m2.map_rows(synthetic_rows(pin, [(0.25 * Hp, 0.5 * Hp)]))
    e = mm['combined']['exclusion'][K0][A0]['t4']
    ok = (reach2[K0][A0]['hull'][1] == 0.0 and reach2[K0][A0]['widened'][1] == 0.0 and reach3[K0][A0]['hull'][1] == 0.0
          and e['class'] == 'EXCLUDED-IN-D' and e['subreason'] == 'SIGN')
    suite('C-SYN-14', ok, 'grid noise at zero: the rebuilt hull upper end snaps to 0 (perturbation at t = 0.02, and at t = 0 as an extra check); a positive interval classes SIGN')
    return res


def csyn6(tokens):
    """memo 4.7: fifteen malformed synthetic files and one valid one, parsed masked; no synthetic value may leak"""
    lo, hi, cl, kem, kt, src = '-0.0031415926', '0.0027182818', '0.8642', '1234.5678', '8765.4321', 'SYNTHETIC-SOURCE-QZX'
    # the leak search uses the full value strings and their long digit runs only (a short fragment could match an md5 by chance)
    secrets = [lo, hi, cl, kem, kt, src, '3141592', '2718281', '1234.5678', '8765.4321', 'SYNTHETIC-SOURCE']
    STATE['synthetic_secrets'] = secrets

    def row(**over):
        f = {'id': 'SA-1', 'class': 'spd', 'delta_def': 'tensor_over_EM_minus_1', 'lo': lo, 'hi': hi, 'cl': cl, 'reading': 'bound',
             'geom': 'single', 'k_em_max': kem, 'k_t_max': kt, 'src': src}
        f.update(over)
        return ' | '.join('%s=%s' % (k, f[k]) for k in REQUIRED if k in f)
    valid = (row() + '\n').encode('utf-8')
    cases = {
        'CRLF': (row() + '\r\n').encode('utf-8'),
        'BOM': b'\xef\xbb\xbf' + valid,
        'trailing blank line': valid + b'\n',
        'form feed in src': (row(src='SYN\x0cTHETIC') + '\n').encode('utf-8'),
        'U+2028 in src': (row(src='SYN THETIC') + '\n').encode('utf-8'),
        'Unicode minus': (row(lo='−0.0031415926') + '\n').encode('utf-8'),
        'superscript form': (row(hi='2.7×10⁻³') + '\n').encode('utf-8'),
        'bar in src': (row(src='SYN|THETIC') + '\n').encode('utf-8'),
        'lo > hi': (row(lo=hi, hi=lo) + '\n').encode('utf-8'),
        'reading=ceiling': (row(reading='ceiling') + '\n').encode('utf-8'),
        'wrong delta_def': (row(delta_def='EM_over_tensor_minus_1') + '\n').encode('utf-8'),
        'missing key': ((' | '.join(f for f in row().split(' | ') if not f.startswith('geom='))) + '\n').encode('utf-8'),
        'wrong id': (row(id='SA-2') + '\n').encode('utf-8'),
        'duplicate key': (row() + ' | cl=' + cl + '\n').encode('utf-8'),
        'percent-form cl': (row(cl='86.42%') + '\n').encode('utf-8'),
    }
    tmp = tempfile.mkdtemp(prefix='g_mscs_a_csyn6_')
    ok, codes, texts = True, [], []
    for name, data in cases.items():
        path = os.path.join(tmp, re.sub(r'\W+', '_', name) + '.md')
        open(path, 'wb').write(data)
        try:
            parse_masked(open(path, 'rb').read(), tokens)
            ok = False
            codes.append('%s -> NO ABORT' % name)
        except MaskedAbort as e:
            codes.append('%s -> %s' % (name, e))
        os.remove(path)
    path = os.path.join(tmp, 'valid.md')
    open(path, 'wb').write(valid)
    try:
        rows, census, md5s = parse_masked(open(path, 'rb').read(), tokens)
        ok &= census['rows'] == 1 and census['per_class'] == {'spd': 1} and census['fields_per_row'] == [len(REQUIRED)] and md5s[0] == md5b(valid[:-1])
        codes.append('valid -> parsed, census %d row' % census['rows'])
    except MaskedAbort as e:
        ok = False
        codes.append('valid -> %s' % e)
    os.remove(path)
    os.rmdir(tmp)
    leak = [s for s in secrets if any(s in c for c in codes)]
    if leak:
        ok = False
        codes.append('LEAK in reason codes')
    return ok, codes


# --------------------------------------------------------------------------------------------- checkpoint
def secrets_absent(text):
    return [s for s in STATE['synthetic_secrets'] if s in text]


def write_checkpoint(ck, rel, scanner, pats):
    bad = sorted({k for k in walk_keys(ck) if k in FORBIDDEN_KEYS})
    if bad:
        raise Halt('checkpoint carries a forbidden key: ' + ', '.join(bad))
    coll = 0
    for _ in range(8):
        ck['T1_post_write'] = {'hits': 0, 'collisions': coll}
        text = json.dumps(ck, sort_keys=True, indent=1, allow_nan=False) + '\n'
        h, c = t1_scan_text(scanner, pats, text)
        if h:
            raise Halt('T1 post-write: %d hit(s) in the checkpoint; not written' % h)
        if c == coll:
            break
        coll = c
    else:
        raise Halt('T1 post-write collision count did not reach a fixed point')
    if secrets_absent(text):
        raise Halt('a synthetic value of C-SYN-6 appears in the checkpoint; not written')
    path = os.path.join(HERE, rel)
    open(path, 'wb').write(text.encode('ascii'))
    h2, c2 = t1_scan_text(scanner, pats, open(path, 'rb').read().decode('utf-8'))
    if h2:
        os.remove(path)
        raise Halt('T1 post-write re-scan hit; checkpoint deleted')
    return md5b(text.encode('ascii')), len(text), c2


def identity_block(pin, guards, instrument_md5, flag):
    P, S = pin.P, pin.S
    return {'gate': GATE, 'leg': LEG, 'instrument': INSTRUMENT, 'instrument_md5': instrument_md5,
            'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'activation_flag': flag,
            'memo_lock_md5': guards[MEMO], 'memo_lock_bytes': GUARDS[MEMO][1], 'lock_record_md5': guards[LOCK],
            'pinned_inputs_md5': guards[PINNED], 'pinned_inputs_bytes': GUARDS[PINNED][1],
            'builder_md5': P['_meta']['builder_md5'], 'verifier_md5': S['verifier_md5'],
            't1_list_md5': guards[T1_LIST], 't1_base_md5': guards[T1_BASE], 't1_a1_md5': guards[T1_A1], 'scanner_md5': guards[SCANNER],
            'schema_md5': guards[SCHEMA], 'comparator_md5': guards[COMPARATOR], 'ledger_base_md5': LEDGER_BASE_MD5,
            'elections': dict(ELECTIONS)}


def grids_block(pin):
    g = {'t_grid': list(pin.t_grid), 't2t4_axis': list(pin.axis), 'D': pin.D, 'area_lo': pin.area_lo, 'area_hi': pin.area_hi,
         'area_nodes_per_axis': pin.area_n, 'richardson_pairs': {'one_param': list(pin.rp1), 'two_param': list(pin.rp2)},
         'oom_factors': list(pin.oom)}
    g.update(grid_counts(pin))
    return g


# --------------------------------------------------------------------------------------------- main
def main(argv):
    if len(argv) < 2 or argv[1] not in ('preread', 'read'):
        print(__doc__)
        return 2
    mode = argv[1]
    inputs = argv[argv.index('--inputs') + 1] if '--inputs' in argv else 'inputs'
    flag = argv[argv.index('--flag') + 1] if '--flag' in argv else None
    t0 = time.time()
    try:
        log('%s %s leg, mode %s' % (GATE, LEG, mode))
        guards = guard_all()
        instrument_md5 = md5b(open(os.path.abspath(__file__), 'rb').read())
        log('guards: %d locked artifacts at their md5 and byte counts; instrument md5 %s' % (len(guards), instrument_md5))
        scanner = load_scanner()
        pats = scanner.load(os.path.join(HERE, T1_LIST)) + scanner.load(os.path.join(HERE, T1_A1))
        per_file, hits, coll = t1_scan(scanner, pats, T1_SCANNED + [INSTRUMENT])
        for rel, r in per_file.items():
            log('  T1 %-32s %s hits=%d collisions=%d' % (rel, 'HIT' if r['hits'] else 'CLEAN', r['hits'], r['collisions']))
        if hits:
            raise Halt('T1: %d hit(s) under the gate list + A1; halting (no override)' % hits)
        S = json.loads(read(SCHEMA).decode('ascii'))
        P = json.loads(read(PINNED).decode('ascii'))
        pin = Pinned(P, S)
        sources = {}
        for alias, spec in P['sources'].items():
            b = open(os.path.join(inputs, spec['path']), 'rb').read()
            if md5b(b) != spec['md5'] or len(b) != spec['bytes']:
                raise Halt('source %s (%s): md5 %s bytes %d differ from the pinned record' % (alias, spec['path'], md5b(b), len(b)))
            sources[alias] = json.loads(b.decode('utf-8'))
        log('sources: %d files at their md5s under %s' % (len(sources), inputs))
        derived_mine = rederive(pin)
        log('Phase 0')
        R0, extra0, mapper = phase0(pin, scanner, pats, sources, (per_file, hits, coll), derived_mine)
        log('Phase 2')
        R2 = phase2(pin, mapper, derived_mine, P['tokens'], scanner, pats)
        if not all(v['passed'] for v in R2.values()):
            raise Halt('Phase 2: a suite failed; no sealed open')
        ck = identity_block(pin, guards, instrument_md5, flag)
        ck.update({'phase0': R0, 'nulls': derived_mine['nulls'], 'grids': grids_block(pin), 'phase2': R2, 'phase3': None,
                   'extras': {'t1_scan': per_file, 'pin': extra0['pin'], 'derived_leaves_rederived': extra0['derived_leaves'],
                              'unions_rederived': derived_mine['unions'], 'synthetic_rederived': derived_mine['synthetic'],
                              'method': 'pure Python; own RFC 6901 binder over the seven pinned sources; own masked parser; '
                                        'Richardson even/odd/mixed parts as pinned; hull-and-widen reach; area grid enumerated from the pinned generator'}})
        if mode == 'preread':
            ck['extras']['elapsed_seconds'] = round(time.time() - t0, 3)
            h, n, c = write_checkpoint(ck, PREREAD_CK, scanner, pats)
            log('pre-read checkpoint written: %s md5 %s %d B; post-write T1 hits 0 collisions %d' % (PREREAD_CK, h, n, c))
            return 0
        # -------------------------------------------------------------------------------- Phase 3
        log('Phase 3')
        STATE['phase3_active'] = True
        data, smd5, sbytes = open_sealed(SEALED_ARMOR)
        try:
            rows, census, row_md5s = parse_masked(data, P['tokens'])
        except MaskedAbort as e:
            log('masked abort: %s (the read is not spent; no value emitted)' % e)
            return 1
        log('sealed: md5 %s bytes %d census %s row md5s %s' % (smd5, sbytes, json.dumps(census, sort_keys=True), row_md5s))
        base, up, down, worst, viol, notes = mapper.map_with_oom(rows)
        if viol or worst > pin.mono_rel:
            raise Halt('MONO on the actual rows: instrument defect (S9): violations %d worst %r %s' % (viol, worst, notes))
        gate = {'gate_class': base['gate_class'], 'sigma_union_hi': base['sigma_union_hi'], 'sigma_strict_hi': base['sigma_strict_hi'],
                'oom_class_x10': up['gate_class'], 'oom_class_x0p1': down['gate_class'],
                'oom_robust': bool(base['gate_class'] == up['gate_class'] == down['gate_class']),
                'contains_zero': base['contains_zero'], 'combined_empty': base['combined_empty'], 'n_void_rows': base['n_void_rows']}
        if gate['gate_class'] not in CLASS_PRECEDENCE:
            raise Halt('gate class outside the precedence list')
        ck['phase3'] = {'sealed_md5': smd5, 'sealed_bytes': sbytes, 'census': census, 'row_md5s': row_md5s, 't1_a1_md5': guards[T1_A1],
                        'n_void_rows': base['n_void_rows'], 'combined_empty': base['combined_empty'], 'contains_zero': base['contains_zero'],
                        'rows': base['rows'], 'combined': base['combined'], 'gate': gate}

        def cell_classes(m):
            if m['combined'] is None:
                return None
            if m['contains_zero']:
                return {'%s/%s/%s' % (K, A, F): m['combined']['families'][K][A][F]['class'] for K in pin.keys for A in pin.arms for F in pin.fam_list(K)}
            return {'%s/%s' % (K, A): m['combined']['exclusion'][K][A][pin.mapped[pin.branch(K)][0]]['class'] for K in pin.keys for A in pin.arms}
        ck['extras']['oom'] = {'x10': {'gate_class': up['gate_class'], 'cells': cell_classes(up), 'combined': up['combined']},
                               'x0p1': {'gate_class': down['gate_class'], 'cells': cell_classes(down), 'combined': down['combined']},
                               'mono_worst_scaling_rel': worst, 'mono_violations': viol}
        ck['extras']['elapsed_seconds'] = round(time.time() - t0, 3)
        h, n, c = write_checkpoint(ck, READ_CK, scanner, pats)
        log('gate class %s (x10 %s, x0.1 %s, OOM-robust %s); sigma_union_hi %r sigma_strict_hi %r' % (
            gate['gate_class'], gate['oom_class_x10'], gate['oom_class_x0p1'], gate['oom_robust'], gate['sigma_union_hi'], gate['sigma_strict_hi']))
        log('checkpoint written: %s md5 %s %d B; post-write T1 hits 0 collisions %d' % (READ_CK, h, n, c))
        return 0
    except Halt as e:
        log('HALT: %s' % e)
        return 1
    finally:
        leak = secrets_absent('\n'.join(STATE['log']))
        if leak:
            print('WARNING: a C-SYN-6 synthetic value reached stdout')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
=====END-EMBED name=g_mscs_a_ccleg.py=====

=====BEGIN-EMBED name=g_mscs_a_ccleg_prereadcheckpoint.json md5=c9f8e4af305f579b1b19953725042d87 bytes=17030 encoding=raw=====
{
 "T1_post_write": {
  "collisions": 1,
  "hits": 0
 },
 "activation_flag": null,
 "builder_md5": "8189100ede80eac360b25a146e580abf",
 "comparator_md5": "c5b4a7aab2fc8651be6d26d1f3d25642",
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
 "extras": {
  "derived_leaves_rederived": 1042,
  "elapsed_seconds": 1.864,
  "method": "pure Python; own RFC 6901 binder over the seven pinned sources; own masked parser; Richardson even/odd/mixed parts as pinned; hull-and-widen reach; area grid enumerated from the pinned generator",
  "pin": {
   "raw_leaves": 1119,
   "uncovered": [],
   "values_checked": 335
  },
  "synthetic_rederived": {
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
  "t1_scan": {
   "G_MSCS_A_LOCK_RECORD.md": {
    "collisions": 0,
    "hit_indices": [],
    "hits": 0
   },
   "g_mscs_a_ccleg.py": {
    "collisions": 0,
    "hit_indices": [],
    "hits": 0
   },
   "g_mscs_a_compare_v1_0.py": {
    "collisions": 0,
    "hit_indices": [],
    "hits": 0
   },
   "g_mscs_a_schema_v1_0.json": {
    "collisions": 0,
    "hit_indices": [],
    "hits": 0
   },
   "pinned_inputs_G_MSCS_A.json": {
    "collisions": 13,
    "hit_indices": [],
    "hits": 0
   },
   "staging_memo_G_MSCS_A_v2.md": {
    "collisions": 3,
    "hit_indices": [],
    "hits": 0
   }
  },
  "unions_rederived": {
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
  }
 },
 "gate": "G-MSCS-A",
 "grids": {
  "D": 0.25,
  "area_hi": 0.25,
  "area_lo": -0.25,
  "area_nodes_per_axis": 201,
  "n_area_grid": 40401,
  "n_fit_window_inclusive": 9,
  "n_fit_window_strict": 7,
  "n_t2t4_axis": 5,
  "n_t2t4_grid": 25,
  "n_t_grid": 12,
  "n_window_0p1_inclusive": 7,
  "n_window_0p1_strict": 5,
  "oom_factors": [
   0.1,
   1.0,
   10.0
  ],
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
 "instrument": "g_mscs_a_ccleg.py",
 "instrument_md5": "a5263388f2db2ce676060551e5636d81",
 "ledger_base_md5": "d4c42a53cbd6d325ebc740879288e844",
 "leg": "cc",
 "lock_record_md5": "8116cc622279b5d4e73214178ae97cd8",
 "memo_lock_bytes": 121950,
 "memo_lock_md5": "6ea16b952db835bb351d3dc1b474c6ed",
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
 "phase0": {
  "F-CTRL-SA-GRID": {
   "count_mismatches": 0,
   "detail": "every count computed from the generators (formula vs enumeration)",
   "odf_reading": "none",
   "passed": true
  },
  "F-CTRL-SA-K24": {
   "detail": "kappa24 on all eight keys: chat diagnostic, CC checkpoint, own 5x5 mixed Richardson, fit7",
   "odf_reading": "hexP2P4/cubP2K4-i",
   "passed": true,
   "worst_abs_bi": 9.423484215176359e-11,
   "worst_abs_fit7": 3.4778572462814414e-07
  },
  "F-CTRL-SA-L2NULL": {
   "detail": "cubP2-ii: the octahedrally symmetrized l=2 perturbation is identically zero (the octahedral group has no l=2 invariant; for <001>, sum_i P2(e_i . z) = 0), so r_agg is unchanged by t2 at every order -- asserted symbolically, no number",
   "odf_reading": "cubP2-ii/cubP2-i/cubP2K4-i",
   "passed": true,
   "worst_abs_kappa2": 1.221245327087672e-13,
   "worst_abs_kappa22": 7.963757933367799e-09,
   "worst_abs_t2_alone_t1": 3.3306690738754696e-16
  },
  "F-CTRL-SA-MASK": {
   "detail": "the sealed file is opened only in Phase 3; md5, bytes and census asserted at every open; masked parser",
   "odf_reading": "none",
   "passed": true,
   "sealed_opens_before_phase3": 0
  },
  "F-CTRL-SA-MONO": {
   "detail": "C-SYN-1 intervals scaled x10 and x0.1: exact sqrt scaling of raw edges, monotone windows and classes",
   "monotonicity_violations": 0,
   "odf_reading": "none",
   "passed": true,
   "worst_scaling_rel": 2.808666774861361e-16
  },
  "F-CTRL-SA-PIN": {
   "detail": "pinned md5 guarded; 335 values re-read through provenance pointers from the seven sources at their md5s; raw leaves not covered by a pointer: 0",
   "odf_reading": "none",
   "passed": true,
   "raw_mismatches": 0,
   "worst_twoleg_S_abs": 2.7504827357592218e-15,
   "worst_twoleg_b1_rel": 6.476723471215587e-13,
   "worst_twoleg_kappa3_rel": 1.7771343065301202e-08,
   "worst_twoleg_kappa_rel": 1.10862881023457e-09
  },
  "F-CTRL-SA-PIN-DERIVED": {
   "detail": "1042 leaves re-derived with this instrument; missing 0, extra 0",
   "leaf_mismatches": 0,
   "odf_reading": "none",
   "passed": true,
   "worst_scaled_dev": 0.0
  },
  "F-CTRL-SA-RECON": {
   "detail": "three-term reconstruction on the primary arm inside D; fit vs basis-independent kappa on the robustness arms",
   "odf_reading": "hexP4/cubK4/hexP2",
   "passed": true,
   "worst_abs_E2_Hill": 6.845659647617054e-10,
   "worst_rel_robust": 0.0007269110377504565
  },
  "F-CTRL-SA-S": {
   "detail": "first-order slope null on every mapped cell",
   "odf_reading": "hexP2/hexP4/cubK4",
   "passed": true,
   "worst_abs_bi": 2.173076533532973e-12,
   "worst_abs_fit": 4.267168229021896e-11
  },
  "F-CTRL-SA-SIGN": {
   "binding_end_mismatches": 0,
   "detail": "asymmetric synthetic interval: hi binds where kappa > 0, lo where kappa < 0, on every mapped cell",
   "odf_reading": "none",
   "passed": true
  },
  "F-CTRL-SA-T1": {
   "collisions": 16,
   "detail": "instrument, memo, pinned file, lock record, schema, comparator under gate list + A1",
   "hits": 0,
   "odf_reading": "none",
   "passed": true
  },
  "F-CTRL-SA-ZERO": {
   "detail": "the banked grid value at t = 0 on every key, arm and family",
   "odf_reading": "uniform",
   "passed": true,
   "worst_abs_r0": 3.3306690738754696e-16
  }
 },
 "phase2": {
  "C-SYN-1": {
   "detail": "symmetric budgets on the reference cell and every cell; gate 0.01:WINDOW-DELIVERED, 0.1:WINDOW-DELIVERED, 0.5:INERT-IN-D",
   "passed": true
  },
  "C-SYN-10": {
   "detail": "regime clause: a void-k row is VOID-REGIME; alone -> gate VOID; with a silent row the silent row alone is mapped",
   "passed": true
  },
  "C-SYN-11": {
   "detail": "the point interval: t* = 0, nu infinite, NULL-FLOOR set, BINDING on every mapped cell; gate WINDOW-DELIVERED",
   "passed": true
  },
  "C-SYN-12": {
   "detail": "tight budget: the null-floor flag recomputed per cell; set on 16 cells, clear on 20",
   "passed": true
  },
  "C-SYN-13": {
   "detail": "the pinned MARGIN-band intervals: margin_positive:MARGIN-ONLY, margin_negative:MARGIN-ONLY",
   "passed": true
  },
  "C-SYN-14": {
   "detail": "grid noise at zero: the rebuilt hull upper end snaps to 0 (perturbation at t = 0.02, and at t = 0 as an extra check); a positive interval classes SIGN",
   "passed": true
  },
  "C-SYN-2": {
   "detail": "asymmetric interval: binding ends by sign(kappa), t* by the binding end on every cell",
   "passed": true
  },
  "C-SYN-3": {
   "detail": "excluding-zero intervals: (i) KILL-IN-D (ii) KILL-IN-D (iii) TUNED (iv) TUNED",
   "passed": true
  },
  "C-SYN-4": {
   "detail": "wide interval: INERT-IN-D everywhere; gate INERT-IN-D",
   "passed": true
  },
  "C-SYN-5": {
   "detail": "the fcc t2 family is NULL-INERT with window D under C-SYN-1",
   "passed": true
  },
  "C-SYN-6": {
   "detail": "fifteen malformed files abort masked with reason codes; the valid file parses; no synthetic value in any output: CRLF -> CONTROL_OR_SEPARATOR_CHAR; BOM -> BOM; trailing blank line -> BLANK_LINE_AT_END; form feed in src -> CONTROL_OR_SEPARATOR_CHAR; U+2028 in src -> CONTROL_OR_SEPARATOR_CHAR; Unicode minus -> row 1 NON_ASCII lo; superscript form -> row 1 NON_ASCII hi; bar in src -> row 1 SEPARATOR_COLLISION; lo > hi -> row 1 ORDER; reading=ceiling -> row 1 READING_NOT_MAPPED; wrong delta_def -> row 1 WRONG_DELTA_DEF; missing key -> row 1 MISSING_KEY geom; wrong id -> row 1 ID_SEQUENCE; duplicate key -> row 1 DUPLICATE_KEY cl; percent-form cl -> row 1 CL_NOT_IN_OPEN_UNIT_INTERVAL_OR_hard; valid -> parsed, census 1 row",
   "passed": true
  },
  "C-SYN-7": {
   "detail": "OOM on the C-SYN-1 intervals: worst scaling rel 2.808666774861361e-16, violations 0",
   "passed": true
  },
  "C-SYN-8": {
   "detail": "two consistent rows: the intersection is mapped (upper end from row 1, lower end from row 2)",
   "passed": true
  },
  "C-SYN-9": {
   "detail": "two disjoint rows: ANCHOR-INCONSISTENT",
   "passed": true
  }
 },
 "phase3": null,
 "pinned_inputs_bytes": 96761,
 "pinned_inputs_md5": "2d44ec01a66889f330d940dee3313bdc",
 "scanner_md5": "6b86290090a8c84f1b1a0a99ec0bf697",
 "schema_md5": "5323e11fc27d688f61aaf57302c875c0",
 "t1_a1_md5": "3b753b3a371a162fc2ab21b9eed51bd5",
 "t1_base_md5": "05302210cc4ceb70553acbe8379e9fc3",
 "t1_list_md5": "e274e58ea50b9ed347969e507d2a4f36",
 "utc": "2026-09-30T04:56:38Z",
 "verifier_md5": "cf004d517d2efe91a02c92a58e3df6bf"
}
=====END-EMBED name=g_mscs_a_ccleg_prereadcheckpoint.json=====

=====BEGIN-EMBED name=g_mscs_a_ccleg_checkpoint.json md5=d0e129fc8c324f0779803a6e33068777 bytes=138012 encoding=raw=====
{
 "T1_post_write": {
  "collisions": 1,
  "hits": 0
 },
 "activation_flag": "ACTIVATE: G-MSCS-A-CC-LEG-1",
 "builder_md5": "8189100ede80eac360b25a146e580abf",
 "comparator_md5": "c5b4a7aab2fc8651be6d26d1f3d25642",
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
 "extras": {
  "derived_leaves_rederived": 1042,
  "elapsed_seconds": 2.132,
  "method": "pure Python; own RFC 6901 binder over the seven pinned sources; own masked parser; Richardson even/odd/mixed parts as pinned; hull-and-widen reach; area grid enumerated from the pinned generator",
  "oom": {
   "mono_violations": 0,
   "mono_worst_scaling_rel": 2.808666774861361e-16,
   "x0p1": {
    "cells": {
     "cubic_gem8|001/E2_HSmean/t2": "NULL-INERT",
     "cubic_gem8|001/E2_HSmean/t4": "BINDING",
     "cubic_gem8|001/E2_Hill/t2": "NULL-INERT",
     "cubic_gem8|001/E2_Hill/t4": "BINDING",
     "cubic_gem8|001/h_Hill/t2": "NULL-INERT",
     "cubic_gem8|001/h_Hill/t4": "BINDING",
     "cubic_gem8|111/E2_HSmean/t2": "NULL-INERT",
     "cubic_gem8|111/E2_HSmean/t4": "BINDING",
     "cubic_gem8|111/E2_Hill/t2": "NULL-INERT",
     "cubic_gem8|111/E2_Hill/t4": "BINDING",
     "cubic_gem8|111/h_Hill/t2": "NULL-INERT",
     "cubic_gem8|111/h_Hill/t4": "BINDING",
     "cubic_step|001/E2_HSmean/t2": "NULL-INERT",
     "cubic_step|001/E2_HSmean/t4": "BINDING",
     "cubic_step|001/E2_Hill/t2": "NULL-INERT",
     "cubic_step|001/E2_Hill/t4": "BINDING",
     "cubic_step|001/h_Hill/t2": "NULL-INERT",
     "cubic_step|001/h_Hill/t4": "BINDING",
     "cubic_step|111/E2_HSmean/t2": "NULL-INERT",
     "cubic_step|111/E2_HSmean/t4": "BINDING",
     "cubic_step|111/E2_Hill/t2": "NULL-INERT",
     "cubic_step|111/E2_Hill/t4": "BINDING",
     "cubic_step|111/h_Hill/t2": "NULL-INERT",
     "cubic_step|111/h_Hill/t4": "BINDING",
     "hex_gem8|a/E2_HSmean/t2": "BINDING",
     "hex_gem8|a/E2_HSmean/t4": "BINDING",
     "hex_gem8|a/E2_Hill/t2": "BINDING",
     "hex_gem8|a/E2_Hill/t4": "BINDING",
     "hex_gem8|a/h_Hill/t2": "BINDING",
     "hex_gem8|a/h_Hill/t4": "BINDING",
     "hex_gem8|b/E2_HSmean/t2": "BINDING",
     "hex_gem8|b/E2_HSmean/t4": "BINDING",
     "hex_gem8|b/E2_Hill/t2": "BINDING",
     "hex_gem8|b/E2_Hill/t4": "BINDING",
     "hex_gem8|b/h_Hill/t2": "BINDING",
     "hex_gem8|b/h_Hill/t4": "BINDING",
     "hex_step|a/E2_HSmean/t2": "BINDING",
     "hex_step|a/E2_HSmean/t4": "BINDING",
     "hex_step|a/E2_Hill/t2": "BINDING",
     "hex_step|a/E2_Hill/t4": "BINDING",
     "hex_step|a/h_Hill/t2": "BINDING",
     "hex_step|a/h_Hill/t4": "BINDING",
     "hex_step|b/E2_HSmean/t2": "BINDING",
     "hex_step|b/E2_HSmean/t4": "BINDING",
     "hex_step|b/E2_Hill/t2": "BINDING",
     "hex_step|b/E2_Hill/t4": "BINDING",
     "hex_step|b/h_Hill/t2": "BINDING",
     "hex_step|b/h_Hill/t4": "BINDING"
    },
    "combined": {
     "exclusion": null,
     "families": {
      "cubic_gem8|001": {
       "E2_HSmean": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0006625024960880849,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 3.4621946275957827e-07,
         "t_star": 7.932884475813561e-07,
         "t_star_bi": 7.932974548368443e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 7.932884475813561e-07,
         "window_lo": -7.932884475813561e-07
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.005919121523213176,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 3.5663489736720796e-07,
         "t_star": 8.171532063240189e-07,
         "t_star_bi": 8.172275410799875e-07,
         "trunc_T": 6.903953730828331e-09,
         "truncation_sensitive": false,
         "window_hi": 8.171532063240189e-07,
         "window_lo": -8.171532063240189e-07
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.010388366023361581,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.1224186552516745e-06,
         "t_star": 2.571784224560671e-06,
         "t_star_bi": 2.5727187839259167e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 2.571784224560671e-06,
         "window_lo": -2.571784224560671e-06
        }
       }
      },
      "cubic_gem8|111": {
       "E2_HSmean": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0011661487336917852,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0482619641579742e-07,
         "t_star": 4.6931577469264213e-07,
         "t_star_bi": 4.6932110353097547e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 4.6931577469264213e-07,
         "window_lo": -4.6931577469264213e-07
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.010018772462098058,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.1098805062532822e-07,
         "t_star": 4.834343563608708e-07,
         "t_star_bi": 4.834783334254348e-07,
         "trunc_T": 4.084434079896353e-09,
         "truncation_sensitive": false,
         "window_hi": 4.834343563608708e-07,
         "window_lo": -4.834343563608708e-07
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.010388366023361581,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.1224186552516745e-06,
         "t_star": 2.571784224560671e-06,
         "t_star_bi": 2.5727187839259167e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 2.571784224560671e-06,
         "window_lo": -2.571784224560671e-06
        }
       }
      },
      "cubic_step|001": {
       "E2_HSmean": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0003064730193049063,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 3.831408331952647e-07,
         "t_star": 8.778859349728748e-07,
         "t_star_bi": 8.77892126431401e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 8.778859349728748e-07,
         "window_lo": -8.778859349728748e-07
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0029711235995085994,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 3.906972465086486e-07,
         "t_star": 8.951998529683519e-07,
         "t_star_bi": 8.952548562964382e-07,
         "trunc_T": 6.296753597110758e-09,
         "truncation_sensitive": false,
         "window_hi": 8.951998529683519e-07,
         "window_lo": -8.951998529683519e-07
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.005585213402618946,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.225821860387256e-06,
         "t_star": 2.8087107318780953e-06,
         "t_star_bi": 2.8094333365739677e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 2.8087107318780953e-06,
         "window_lo": -2.8087107318780953e-06
        }
       }
      },
      "cubic_step|111": {
       "E2_HSmean": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00048600005079557927,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.2666917373407562e-07,
         "t_star": 5.193643231747489e-07,
         "t_star_bi": 5.193679861145341e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 5.193643231747489e-07,
         "window_lo": -5.193643231747489e-07
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00503144855532146,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.311396081387769e-07,
         "t_star": 5.296073751991881e-07,
         "t_star_bi": 5.296399155716738e-07,
         "trunc_T": 3.725209748318907e-09,
         "truncation_sensitive": false,
         "window_hi": 5.296073751991881e-07,
         "window_lo": -5.296073751991881e-07
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.005585213402618946,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.225821860387256e-06,
         "t_star": 2.8087107318780953e-06,
         "t_star_bi": 2.8094333365739677e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 2.8087107318780953e-06,
         "window_lo": -2.8087107318780953e-06
        }
       }
      },
      "hex_gem8|a": {
       "E2_HSmean": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.9278910324750513e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.7839604471924586e-07,
         "t_star": 3.989056829093261e-07,
         "t_star_bi": 3.989051242997132e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 3.989056829093261e-07,
         "window_lo": -3.989056829093261e-07
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 9.92016542966505e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0849011555163492e-07,
         "t_star": 6.254703466549048e-07,
         "t_star_bi": 6.254707108144702e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.254703466549048e-07,
         "window_lo": -6.254703466549048e-07
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 3.459700950843784e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.7790850957431113e-07,
         "t_star": 3.978155211838319e-07,
         "t_star_bi": 3.97817292877753e-07,
         "trunc_T": 2.603427610015837e-10,
         "truncation_sensitive": false,
         "window_hi": 3.978155211838319e-07,
         "window_lo": -3.978155211838319e-07
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 8.913795514324561e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0815493562769057e-07,
         "t_star": 6.244648068830717e-07,
         "t_star_bi": 6.24468896040789e-07,
         "trunc_T": 7.629296456680734e-10,
         "truncation_sensitive": false,
         "window_hi": 6.244648068830717e-07,
         "window_lo": -6.244648068830717e-07
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 4.1485375442967636e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 4.297088101323804e-06,
         "t_star": 9.60858109986553e-06,
         "t_star_bi": 9.608714946224392e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 9.60858109986553e-06,
         "window_lo": -9.60858109986553e-06
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00012276478701108923,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0733129338900986e-06,
         "t_star": 6.219938801670296e-06,
         "t_star_bi": 6.22010803788012e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.219938801670296e-06,
         "window_lo": -6.219938801670296e-06
        }
       }
      },
      "hex_gem8|b": {
       "E2_HSmean": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.9521079430529517e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.783726483193466e-07,
         "t_star": 3.988533669687226e-07,
         "t_star_bi": 3.988528081395981e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 3.988533669687226e-07,
         "window_lo": -3.988533669687226e-07
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 4.6294863191777856e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0849352861965886e-07,
         "t_star": 6.254805858589766e-07,
         "t_star_bi": 6.254809498919889e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.254805858589766e-07,
         "window_lo": -6.254805858589766e-07
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 3.410187376739944e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.7788556820018462e-07,
         "t_star": 3.977642227117877e-07,
         "t_star_bi": 3.977659952805345e-07,
         "trunc_T": 2.602368130105003e-10,
         "truncation_sensitive": false,
         "window_hi": 3.977642227117877e-07,
         "window_lo": -3.977642227117877e-07
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00011555106217809555,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0815828822701443e-07,
         "t_star": 6.244748646810433e-07,
         "t_star_bi": 6.244789530887736e-07,
         "trunc_T": 7.627073233098915e-10,
         "truncation_sensitive": false,
         "window_hi": 6.244748646810433e-07,
         "window_lo": -6.244748646810433e-07
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.9625397113506577e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 4.29607099137462e-06,
         "t_star": 9.606306772878565e-06,
         "t_star_bi": 9.606440709180047e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 9.606306772878565e-06,
         "window_lo": -9.606306772878565e-06
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00013044413939585083,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0734170973264194e-06,
         "t_star": 6.220251291979258e-06,
         "t_star_bi": 6.220420522548329e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.220251291979258e-06,
         "window_lo": -6.220251291979258e-06
        }
       }
      },
      "hex_step|a": {
       "E2_HSmean": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.0742114025396826e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0496675926282541e-07,
         "t_star": 4.5831960683951234e-07,
         "t_star_bi": 4.5831924015710697e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 4.5831960683951234e-07,
         "window_lo": -4.5831960683951234e-07
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.798434535398441e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.2055300278972003e-07,
         "t_star": 6.616590083691602e-07,
         "t_star_bi": 6.61659407091156e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.616590083691602e-07,
         "window_lo": -6.616590083691602e-07
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.4078885887952783e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.041623037907976e-07,
         "t_star": 4.565207897191864e-07,
         "t_star_bi": 4.5652195190319044e-07,
         "trunc_T": 2.337158160535306e-10,
         "truncation_sensitive": false,
         "window_hi": 4.565207897191864e-07,
         "window_lo": -4.565207897191864e-07
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00013271320343501784,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.202005228820862e-07,
         "t_star": 6.606015686462587e-07,
         "t_star_bi": 6.606054870267185e-07,
         "trunc_T": 9.12138022298914e-10,
         "truncation_sensitive": false,
         "window_hi": 6.606015686462587e-07,
         "window_lo": -6.606015686462587e-07
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.2619902399545996e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 5.466970684763733e-06,
         "t_star": 1.222451808213028e-05,
         "t_star_bi": 1.2224615642171955e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 1.222451808213028e-05,
         "window_lo": -1.222451808213028e-05
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00013646201949597277,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.1070981719507025e-06,
         "t_star": 6.321294515852108e-06,
         "t_star_bi": 6.321460127307353e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.321294515852108e-06,
         "window_lo": -6.321294515852108e-06
        }
       }
      },
      "hex_step|b": {
       "E2_HSmean": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.2441571135683647e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0502169687206209e-07,
         "t_star": 4.5844245106828686e-07,
         "t_star_bi": 4.58442084668771e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 4.5844245106828686e-07,
         "window_lo": -4.5844245106828686e-07
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 3.497938848948003e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.205464253536181e-07,
         "t_star": 6.616392760608543e-07,
         "t_star_bi": 6.616396750256083e-07,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.616392760608543e-07,
         "window_lo": -6.616392760608543e-07
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.633581526365727e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.042161540798295e-07,
         "t_star": 4.566412026260698e-07,
         "t_star_bi": 4.56642363622766e-07,
         "trunc_T": 2.3391341878200897e-10,
         "truncation_sensitive": false,
         "window_hi": 4.566412026260698e-07,
         "window_lo": -4.566412026260698e-07
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 8.381643066791726e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.2019412678874173e-07,
         "t_star": 6.605823803662252e-07,
         "t_star_bi": 6.605862998003097e-07,
         "trunc_T": 9.124761581940579e-10,
         "truncation_sensitive": false,
         "window_hi": 6.605823803662252e-07,
         "window_lo": -6.605823803662252e-07
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 5.469841904220187e-06,
         "t_star": 1.2230938324013232e-05,
         "t_star_bi": 1.2231036301263607e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 1.2230938324013232e-05,
         "window_lo": -1.2230938324013232e-05
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00010526173852715158,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.1069187840322237e-06,
         "t_star": 6.320756352096672e-06,
         "t_star_bi": 6.320922033406374e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.320756352096672e-06,
         "window_lo": -6.320756352096672e-06
        }
       }
      }
     },
     "two_param": {
      "hex_gem8|a": {
       "E2_HSmean": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 3.2459969594961784,
        "total_nodes": 40401
       },
       "E2_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 3.249659452469566,
        "total_nodes": 40401
       },
       "h_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "negative-definite",
        "null_ray_slope": null,
        "total_nodes": 40401
       }
      },
      "hex_gem8|b": {
       "E2_HSmean": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 3.2464758687049406,
        "total_nodes": 40401
       },
       "E2_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 3.2501308980491763,
        "total_nodes": 40401
       },
       "h_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "negative-definite",
        "null_ray_slope": null,
        "total_nodes": 40401
       }
      },
      "hex_step|a": {
       "E2_HSmean": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 2.988666120042645,
        "total_nodes": 40401
       },
       "E2_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 2.995647084883406,
        "total_nodes": 40401
       },
       "h_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "negative-definite",
        "null_ray_slope": null,
        "total_nodes": 40401
       }
      },
      "hex_step|b": {
       "E2_HSmean": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 2.987776171603675,
        "total_nodes": 40401
       },
       "E2_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 2.9947701642622118,
        "total_nodes": 40401
       },
       "h_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "negative-definite",
        "null_ray_slope": null,
        "total_nodes": 40401
       }
      }
     }
    },
    "gate_class": "WINDOW-DELIVERED"
   },
   "x10": {
    "cells": {
     "cubic_gem8|001/E2_HSmean/t2": "NULL-INERT",
     "cubic_gem8|001/E2_HSmean/t4": "BINDING",
     "cubic_gem8|001/E2_Hill/t2": "NULL-INERT",
     "cubic_gem8|001/E2_Hill/t4": "BINDING",
     "cubic_gem8|001/h_Hill/t2": "NULL-INERT",
     "cubic_gem8|001/h_Hill/t4": "BINDING",
     "cubic_gem8|111/E2_HSmean/t2": "NULL-INERT",
     "cubic_gem8|111/E2_HSmean/t4": "BINDING",
     "cubic_gem8|111/E2_Hill/t2": "NULL-INERT",
     "cubic_gem8|111/E2_Hill/t4": "BINDING",
     "cubic_gem8|111/h_Hill/t2": "NULL-INERT",
     "cubic_gem8|111/h_Hill/t4": "BINDING",
     "cubic_step|001/E2_HSmean/t2": "NULL-INERT",
     "cubic_step|001/E2_HSmean/t4": "BINDING",
     "cubic_step|001/E2_Hill/t2": "NULL-INERT",
     "cubic_step|001/E2_Hill/t4": "BINDING",
     "cubic_step|001/h_Hill/t2": "NULL-INERT",
     "cubic_step|001/h_Hill/t4": "BINDING",
     "cubic_step|111/E2_HSmean/t2": "NULL-INERT",
     "cubic_step|111/E2_HSmean/t4": "BINDING",
     "cubic_step|111/E2_Hill/t2": "NULL-INERT",
     "cubic_step|111/E2_Hill/t4": "BINDING",
     "cubic_step|111/h_Hill/t2": "NULL-INERT",
     "cubic_step|111/h_Hill/t4": "BINDING",
     "hex_gem8|a/E2_HSmean/t2": "BINDING",
     "hex_gem8|a/E2_HSmean/t4": "BINDING",
     "hex_gem8|a/E2_Hill/t2": "BINDING",
     "hex_gem8|a/E2_Hill/t4": "BINDING",
     "hex_gem8|a/h_Hill/t2": "BINDING",
     "hex_gem8|a/h_Hill/t4": "BINDING",
     "hex_gem8|b/E2_HSmean/t2": "BINDING",
     "hex_gem8|b/E2_HSmean/t4": "BINDING",
     "hex_gem8|b/E2_Hill/t2": "BINDING",
     "hex_gem8|b/E2_Hill/t4": "BINDING",
     "hex_gem8|b/h_Hill/t2": "BINDING",
     "hex_gem8|b/h_Hill/t4": "BINDING",
     "hex_step|a/E2_HSmean/t2": "BINDING",
     "hex_step|a/E2_HSmean/t4": "BINDING",
     "hex_step|a/E2_Hill/t2": "BINDING",
     "hex_step|a/E2_Hill/t4": "BINDING",
     "hex_step|a/h_Hill/t2": "BINDING",
     "hex_step|a/h_Hill/t4": "BINDING",
     "hex_step|b/E2_HSmean/t2": "BINDING",
     "hex_step|b/E2_HSmean/t4": "BINDING",
     "hex_step|b/E2_Hill/t2": "BINDING",
     "hex_step|b/E2_Hill/t4": "BINDING",
     "hex_step|b/h_Hill/t2": "BINDING",
     "hex_step|b/h_Hill/t4": "BINDING"
    },
    "combined": {
     "exclusion": null,
     "families": {
      "cubic_gem8|001": {
       "E2_HSmean": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 6.62502496088085e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 3.462194627595783e-06,
         "t_star": 7.932884475813561e-06,
         "t_star_bi": 7.932974548368443e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 7.932884475813561e-06,
         "window_lo": -7.932884475813561e-06
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0005919121523213178,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 3.5663489736720793e-06,
         "t_star": 8.171532063240188e-06,
         "t_star_bi": 8.172275410799874e-06,
         "trunc_T": 6.903953730828332e-08,
         "truncation_sensitive": false,
         "window_hi": 8.171532063240188e-06,
         "window_lo": -8.171532063240188e-06
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.001038836602336158,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.1224186552516744e-05,
         "t_star": 2.5717842245606708e-05,
         "t_star_bi": 2.5727187839259168e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 2.5717842245606708e-05,
         "window_lo": -2.5717842245606708e-05
        }
       }
      },
      "cubic_gem8|111": {
       "E2_HSmean": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00011661487336917854,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.048261964157974e-06,
         "t_star": 4.693157746926421e-06,
         "t_star_bi": 4.6932110353097546e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 4.693157746926421e-06,
         "window_lo": -4.693157746926421e-06
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.001001877246209806,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.1098805062532825e-06,
         "t_star": 4.834343563608708e-06,
         "t_star_bi": 4.834783334254348e-06,
         "trunc_T": 4.084434079896353e-08,
         "truncation_sensitive": false,
         "window_hi": 4.834343563608708e-06,
         "window_lo": -4.834343563608708e-06
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.001038836602336158,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.1224186552516744e-05,
         "t_star": 2.5717842245606708e-05,
         "t_star_bi": 2.5727187839259168e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 2.5717842245606708e-05,
         "window_lo": -2.5717842245606708e-05
        }
       }
      },
      "cubic_step|001": {
       "E2_HSmean": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 3.0647301930490626e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 3.831408331952646e-06,
         "t_star": 8.778859349728748e-06,
         "t_star_bi": 8.77892126431401e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 8.778859349728748e-06,
         "window_lo": -8.778859349728748e-06
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.00029711235995085995,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 3.906972465086486e-06,
         "t_star": 8.951998529683518e-06,
         "t_star_bi": 8.952548562964383e-06,
         "trunc_T": 6.296753597110758e-08,
         "truncation_sensitive": false,
         "window_hi": 8.951998529683518e-06,
         "window_lo": -8.951998529683518e-06
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0005585213402618946,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.2258218603872558e-05,
         "t_star": 2.8087107318780948e-05,
         "t_star_bi": 2.8094333365739675e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 2.8087107318780948e-05,
         "window_lo": -2.8087107318780948e-05
        }
       }
      },
      "cubic_step|111": {
       "E2_HSmean": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 4.8600005079557925e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.266691737340756e-06,
         "t_star": 5.193643231747488e-06,
         "t_star_bi": 5.193679861145341e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 5.193643231747488e-06,
         "window_lo": -5.193643231747488e-06
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.000503144855532146,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.311396081387769e-06,
         "t_star": 5.296073751991881e-06,
         "t_star_bi": 5.2963991557167375e-06,
         "trunc_T": 3.725209748318907e-08,
         "truncation_sensitive": false,
         "window_hi": 5.296073751991881e-06,
         "window_lo": -5.296073751991881e-06
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": null,
         "class": "NULL-INERT",
         "class_bi": null,
         "nu": null,
         "nu_is_inf": null,
         "nullfloor_sensitive": null,
         "resolution_sensitive": null,
         "sigma_star": null,
         "t_star": null,
         "t_star_bi": null,
         "trunc_T": null,
         "truncation_sensitive": null,
         "window_hi": 0.25,
         "window_lo": -0.25
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0005585213402618946,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.2258218603872558e-05,
         "t_star": 2.8087107318780948e-05,
         "t_star_bi": 2.8094333365739675e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 2.8087107318780948e-05,
         "window_lo": -2.8087107318780948e-05
        }
       }
      },
      "hex_gem8|a": {
       "E2_HSmean": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.9278910324750513e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.7839604471924581e-06,
         "t_star": 3.9890568290932605e-06,
         "t_star_bi": 3.989051242997132e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 3.9890568290932605e-06,
         "window_lo": -3.9890568290932605e-06
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 9.92016542966505e-07,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.084901155516349e-06,
         "t_star": 6.254703466549048e-06,
         "t_star_bi": 6.254707108144702e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.254703466549048e-06,
         "window_lo": -6.254703466549048e-06
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 3.4597009508437845e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.7790850957431116e-06,
         "t_star": 3.978155211838319e-06,
         "t_star_bi": 3.97817292877753e-06,
         "trunc_T": 2.603427610015837e-09,
         "truncation_sensitive": false,
         "window_hi": 3.978155211838319e-06,
         "window_lo": -3.978155211838319e-06
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 8.91379551432456e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0815493562769054e-06,
         "t_star": 6.244648068830717e-06,
         "t_star_bi": 6.24468896040789e-06,
         "trunc_T": 7.629296456680734e-09,
         "truncation_sensitive": false,
         "window_hi": 6.244648068830717e-06,
         "window_lo": -6.244648068830717e-06
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 4.148537544296764e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 4.2970881013238034e-05,
         "t_star": 9.608581099865529e-05,
         "t_star_bi": 9.608714946224391e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 9.608581099865529e-05,
         "window_lo": -9.608581099865529e-05
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.2276478701108921e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0733129338900985e-05,
         "t_star": 6.219938801670296e-05,
         "t_star_bi": 6.22010803788012e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.219938801670296e-05,
         "window_lo": -6.219938801670296e-05
        }
       }
      },
      "hex_gem8|b": {
       "E2_HSmean": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.952107943052951e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.783726483193466e-06,
         "t_star": 3.988533669687226e-06,
         "t_star_bi": 3.988528081395981e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 3.988533669687226e-06,
         "window_lo": -3.988533669687226e-06
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 4.629486319177786e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0849352861965883e-06,
         "t_star": 6.254805858589766e-06,
         "t_star_bi": 6.254809498919889e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.254805858589766e-06,
         "window_lo": -6.254805858589766e-06
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 3.410187376739944e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 1.778855682001846e-06,
         "t_star": 3.977642227117877e-06,
         "t_star_bi": 3.977659952805344e-06,
         "trunc_T": 2.602368130105003e-09,
         "truncation_sensitive": false,
         "window_hi": 3.977642227117877e-06,
         "window_lo": -3.977642227117877e-06
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.1555106217809554e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0815828822701443e-06,
         "t_star": 6.244748646810433e-06,
         "t_star_bi": 6.244789530887736e-06,
         "trunc_T": 7.627073233098914e-09,
         "truncation_sensitive": false,
         "window_hi": 6.244748646810433e-06,
         "window_lo": -6.244748646810433e-06
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.9625397113506574e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 4.2960709913746206e-05,
         "t_star": 9.606306772878564e-05,
         "t_star_bi": 9.606440709180046e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 9.606306772878564e-05,
         "window_lo": -9.606306772878564e-05
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.3044413939585084e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0734170973264194e-05,
         "t_star": 6.220251291979259e-05,
         "t_star_bi": 6.220420522548328e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.220251291979259e-05,
         "window_lo": -6.220251291979259e-05
        }
       }
      },
      "hex_step|a": {
       "E2_HSmean": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.0742114025396827e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.0496675926282543e-06,
         "t_star": 4.583196068395123e-06,
         "t_star_bi": 4.58319240157107e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 4.583196068395123e-06,
         "window_lo": -4.583196068395123e-06
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.798434535398441e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.2055300278972002e-06,
         "t_star": 6.6165900836916016e-06,
         "t_star_bi": 6.616594070911559e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.6165900836916016e-06,
         "window_lo": -6.6165900836916016e-06
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.4078885887952784e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.041623037907976e-06,
         "t_star": 4.565207897191864e-06,
         "t_star_bi": 4.5652195190319045e-06,
         "trunc_T": 2.337158160535306e-09,
         "truncation_sensitive": false,
         "window_hi": 4.565207897191864e-06,
         "window_lo": -4.565207897191864e-06
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.3271320343501783e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.202005228820862e-06,
         "t_star": 6.606015686462586e-06,
         "t_star_bi": 6.606054870267185e-06,
         "trunc_T": 9.121380222989139e-09,
         "truncation_sensitive": false,
         "window_hi": 6.606015686462586e-06,
         "window_lo": -6.606015686462586e-06
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 2.2619902399545997e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 5.466970684763733e-05,
         "t_star": 0.0001222451808213028,
         "t_star_bi": 0.00012224615642171955,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 0.0001222451808213028,
         "window_lo": -0.0001222451808213028
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.3646201949597276e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.1070981719507024e-05,
         "t_star": 6.321294515852107e-05,
         "t_star_bi": 6.321460127307352e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.321294515852107e-05,
         "window_lo": -6.321294515852107e-05
        }
       }
      },
      "hex_step|b": {
       "E2_HSmean": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.2441571135683647e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.050216968720621e-06,
         "t_star": 4.5844245106828685e-06,
         "t_star_bi": 4.58442084668771e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 4.5844245106828685e-06,
         "window_lo": -4.5844245106828685e-06
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 3.497938848948003e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.205464253536181e-06,
         "t_star": 6.616392760608543e-06,
         "t_star_bi": 6.616396750256084e-06,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.616392760608543e-06,
         "window_lo": -6.616392760608543e-06
        }
       },
       "E2_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.633581526365727e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.042161540798295e-06,
         "t_star": 4.566412026260698e-06,
         "t_star_bi": 4.566423636227659e-06,
         "trunc_T": 2.3391341878200902e-09,
         "truncation_sensitive": false,
         "window_hi": 4.566412026260698e-06,
         "window_lo": -4.566412026260698e-06
        },
        "t4": {
         "binding_end": "hi",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 8.381643066791728e-06,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.2019412678874173e-06,
         "t_star": 6.605823803662252e-06,
         "t_star_bi": 6.605862998003097e-06,
         "trunc_T": 9.12476158194058e-09,
         "truncation_sensitive": false,
         "window_hi": 6.605823803662252e-06,
         "window_lo": -6.605823803662252e-06
        }
       },
       "h_Hill": {
        "t2": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 0.0,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 5.4698419042201875e-05,
         "t_star": 0.00012230938324013233,
         "t_star_bi": 0.00012231036301263605,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 0.00012230938324013233,
         "window_lo": -0.00012230938324013233
        },
        "t4": {
         "binding_end": "lo",
         "class": "BINDING",
         "class_bi": "BINDING",
         "nu": 1.0526173852715156e-05,
         "nu_is_inf": false,
         "nullfloor_sensitive": false,
         "resolution_sensitive": false,
         "sigma_star": 2.1069187840322236e-05,
         "t_star": 6.320756352096671e-05,
         "t_star_bi": 6.320922033406374e-05,
         "trunc_T": null,
         "truncation_sensitive": false,
         "window_hi": 6.320756352096671e-05,
         "window_lo": -6.320756352096671e-05
        }
       }
      }
     },
     "two_param": {
      "hex_gem8|a": {
       "E2_HSmean": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 3.2459969594961784,
        "total_nodes": 40401
       },
       "E2_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 3.249659452469566,
        "total_nodes": 40401
       },
       "h_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "negative-definite",
        "null_ray_slope": null,
        "total_nodes": 40401
       }
      },
      "hex_gem8|b": {
       "E2_HSmean": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 3.2464758687049406,
        "total_nodes": 40401
       },
       "E2_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 3.2501308980491763,
        "total_nodes": 40401
       },
       "h_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "negative-definite",
        "null_ray_slope": null,
        "total_nodes": 40401
       }
      },
      "hex_step|a": {
       "E2_HSmean": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 2.988666120042645,
        "total_nodes": 40401
       },
       "E2_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 2.995647084883406,
        "total_nodes": 40401
       },
       "h_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "negative-definite",
        "null_ray_slope": null,
        "total_nodes": 40401
       }
      },
      "hex_step|b": {
       "E2_HSmean": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 2.987776171603675,
        "total_nodes": 40401
       },
       "E2_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "indefinite",
        "null_ray_slope": 2.9947701642622118,
        "total_nodes": 40401
       },
       "h_Hill": {
        "admissible_nodes": 1,
        "area_fraction": 2.475186257765897e-05,
        "compact": true,
        "definiteness": "negative-definite",
        "null_ray_slope": null,
        "total_nodes": 40401
       }
      }
     }
    },
    "gate_class": "WINDOW-DELIVERED"
   }
  },
  "pin": {
   "raw_leaves": 1119,
   "uncovered": [],
   "values_checked": 335
  },
  "synthetic_rederived": {
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
  "t1_scan": {
   "G_MSCS_A_LOCK_RECORD.md": {
    "collisions": 0,
    "hit_indices": [],
    "hits": 0
   },
   "g_mscs_a_ccleg.py": {
    "collisions": 0,
    "hit_indices": [],
    "hits": 0
   },
   "g_mscs_a_compare_v1_0.py": {
    "collisions": 0,
    "hit_indices": [],
    "hits": 0
   },
   "g_mscs_a_schema_v1_0.json": {
    "collisions": 0,
    "hit_indices": [],
    "hits": 0
   },
   "pinned_inputs_G_MSCS_A.json": {
    "collisions": 13,
    "hit_indices": [],
    "hits": 0
   },
   "staging_memo_G_MSCS_A_v2.md": {
    "collisions": 3,
    "hit_indices": [],
    "hits": 0
   }
  },
  "unions_rederived": {
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
  }
 },
 "gate": "G-MSCS-A",
 "grids": {
  "D": 0.25,
  "area_hi": 0.25,
  "area_lo": -0.25,
  "area_nodes_per_axis": 201,
  "n_area_grid": 40401,
  "n_fit_window_inclusive": 9,
  "n_fit_window_strict": 7,
  "n_t2t4_axis": 5,
  "n_t2t4_grid": 25,
  "n_t_grid": 12,
  "n_window_0p1_inclusive": 7,
  "n_window_0p1_strict": 5,
  "oom_factors": [
   0.1,
   1.0,
   10.0
  ],
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
 "instrument": "g_mscs_a_ccleg.py",
 "instrument_md5": "a5263388f2db2ce676060551e5636d81",
 "ledger_base_md5": "d4c42a53cbd6d325ebc740879288e844",
 "leg": "cc",
 "lock_record_md5": "8116cc622279b5d4e73214178ae97cd8",
 "memo_lock_bytes": 121950,
 "memo_lock_md5": "6ea16b952db835bb351d3dc1b474c6ed",
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
 "phase0": {
  "F-CTRL-SA-GRID": {
   "count_mismatches": 0,
   "detail": "every count computed from the generators (formula vs enumeration)",
   "odf_reading": "none",
   "passed": true
  },
  "F-CTRL-SA-K24": {
   "detail": "kappa24 on all eight keys: chat diagnostic, CC checkpoint, own 5x5 mixed Richardson, fit7",
   "odf_reading": "hexP2P4/cubP2K4-i",
   "passed": true,
   "worst_abs_bi": 9.423484215176359e-11,
   "worst_abs_fit7": 3.4778572462814414e-07
  },
  "F-CTRL-SA-L2NULL": {
   "detail": "cubP2-ii: the octahedrally symmetrized l=2 perturbation is identically zero (the octahedral group has no l=2 invariant; for <001>, sum_i P2(e_i . z) = 0), so r_agg is unchanged by t2 at every order -- asserted symbolically, no number",
   "odf_reading": "cubP2-ii/cubP2-i/cubP2K4-i",
   "passed": true,
   "worst_abs_kappa2": 1.221245327087672e-13,
   "worst_abs_kappa22": 7.963757933367799e-09,
   "worst_abs_t2_alone_t1": 3.3306690738754696e-16
  },
  "F-CTRL-SA-MASK": {
   "detail": "the sealed file is opened only in Phase 3; md5, bytes and census asserted at every open; masked parser",
   "odf_reading": "none",
   "passed": true,
   "sealed_opens_before_phase3": 0
  },
  "F-CTRL-SA-MONO": {
   "detail": "C-SYN-1 intervals scaled x10 and x0.1: exact sqrt scaling of raw edges, monotone windows and classes",
   "monotonicity_violations": 0,
   "odf_reading": "none",
   "passed": true,
   "worst_scaling_rel": 2.808666774861361e-16
  },
  "F-CTRL-SA-PIN": {
   "detail": "pinned md5 guarded; 335 values re-read through provenance pointers from the seven sources at their md5s; raw leaves not covered by a pointer: 0",
   "odf_reading": "none",
   "passed": true,
   "raw_mismatches": 0,
   "worst_twoleg_S_abs": 2.7504827357592218e-15,
   "worst_twoleg_b1_rel": 6.476723471215587e-13,
   "worst_twoleg_kappa3_rel": 1.7771343065301202e-08,
   "worst_twoleg_kappa_rel": 1.10862881023457e-09
  },
  "F-CTRL-SA-PIN-DERIVED": {
   "detail": "1042 leaves re-derived with this instrument; missing 0, extra 0",
   "leaf_mismatches": 0,
   "odf_reading": "none",
   "passed": true,
   "worst_scaled_dev": 0.0
  },
  "F-CTRL-SA-RECON": {
   "detail": "three-term reconstruction on the primary arm inside D; fit vs basis-independent kappa on the robustness arms",
   "odf_reading": "hexP4/cubK4/hexP2",
   "passed": true,
   "worst_abs_E2_Hill": 6.845659647617054e-10,
   "worst_rel_robust": 0.0007269110377504565
  },
  "F-CTRL-SA-S": {
   "detail": "first-order slope null on every mapped cell",
   "odf_reading": "hexP2/hexP4/cubK4",
   "passed": true,
   "worst_abs_bi": 2.173076533532973e-12,
   "worst_abs_fit": 4.267168229021896e-11
  },
  "F-CTRL-SA-SIGN": {
   "binding_end_mismatches": 0,
   "detail": "asymmetric synthetic interval: hi binds where kappa > 0, lo where kappa < 0, on every mapped cell",
   "odf_reading": "none",
   "passed": true
  },
  "F-CTRL-SA-T1": {
   "collisions": 16,
   "detail": "instrument, memo, pinned file, lock record, schema, comparator under gate list + A1",
   "hits": 0,
   "odf_reading": "none",
   "passed": true
  },
  "F-CTRL-SA-ZERO": {
   "detail": "the banked grid value at t = 0 on every key, arm and family",
   "odf_reading": "uniform",
   "passed": true,
   "worst_abs_r0": 3.3306690738754696e-16
  }
 },
 "phase2": {
  "C-SYN-1": {
   "detail": "symmetric budgets on the reference cell and every cell; gate 0.01:WINDOW-DELIVERED, 0.1:WINDOW-DELIVERED, 0.5:INERT-IN-D",
   "passed": true
  },
  "C-SYN-10": {
   "detail": "regime clause: a void-k row is VOID-REGIME; alone -> gate VOID; with a silent row the silent row alone is mapped",
   "passed": true
  },
  "C-SYN-11": {
   "detail": "the point interval: t* = 0, nu infinite, NULL-FLOOR set, BINDING on every mapped cell; gate WINDOW-DELIVERED",
   "passed": true
  },
  "C-SYN-12": {
   "detail": "tight budget: the null-floor flag recomputed per cell; set on 16 cells, clear on 20",
   "passed": true
  },
  "C-SYN-13": {
   "detail": "the pinned MARGIN-band intervals: margin_positive:MARGIN-ONLY, margin_negative:MARGIN-ONLY",
   "passed": true
  },
  "C-SYN-14": {
   "detail": "grid noise at zero: the rebuilt hull upper end snaps to 0 (perturbation at t = 0.02, and at t = 0 as an extra check); a positive interval classes SIGN",
   "passed": true
  },
  "C-SYN-2": {
   "detail": "asymmetric interval: binding ends by sign(kappa), t* by the binding end on every cell",
   "passed": true
  },
  "C-SYN-3": {
   "detail": "excluding-zero intervals: (i) KILL-IN-D (ii) KILL-IN-D (iii) TUNED (iv) TUNED",
   "passed": true
  },
  "C-SYN-4": {
   "detail": "wide interval: INERT-IN-D everywhere; gate INERT-IN-D",
   "passed": true
  },
  "C-SYN-5": {
   "detail": "the fcc t2 family is NULL-INERT with window D under C-SYN-1",
   "passed": true
  },
  "C-SYN-6": {
   "detail": "fifteen malformed files abort masked with reason codes; the valid file parses; no synthetic value in any output: CRLF -> CONTROL_OR_SEPARATOR_CHAR; BOM -> BOM; trailing blank line -> BLANK_LINE_AT_END; form feed in src -> CONTROL_OR_SEPARATOR_CHAR; U+2028 in src -> CONTROL_OR_SEPARATOR_CHAR; Unicode minus -> row 1 NON_ASCII lo; superscript form -> row 1 NON_ASCII hi; bar in src -> row 1 SEPARATOR_COLLISION; lo > hi -> row 1 ORDER; reading=ceiling -> row 1 READING_NOT_MAPPED; wrong delta_def -> row 1 WRONG_DELTA_DEF; missing key -> row 1 MISSING_KEY geom; wrong id -> row 1 ID_SEQUENCE; duplicate key -> row 1 DUPLICATE_KEY cl; percent-form cl -> row 1 CL_NOT_IN_OPEN_UNIT_INTERVAL_OR_hard; valid -> parsed, census 1 row",
   "passed": true
  },
  "C-SYN-7": {
   "detail": "OOM on the C-SYN-1 intervals: worst scaling rel 2.808666774861361e-16, violations 0",
   "passed": true
  },
  "C-SYN-8": {
   "detail": "two consistent rows: the intersection is mapped (upper end from row 1, lower end from row 2)",
   "passed": true
  },
  "C-SYN-9": {
   "detail": "two disjoint rows: ANCHOR-INCONSISTENT",
   "passed": true
  }
 },
 "phase3": {
  "census": {
   "fields_per_row": [
    11
   ],
   "per_class": {
    "spd": 1
   },
   "rows": 1
  },
  "combined": {
   "exclusion": null,
   "families": {
    "cubic_gem8|001": {
     "E2_HSmean": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.000209501684318514,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 1.0948420726001125e-06,
       "t_star": 2.5085983358561767e-06,
       "t_star_bi": 2.5086268192989865e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 2.5085983358561767e-06,
       "window_lo": -2.5085983358561767e-06
      }
     },
     "E2_Hill": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.0018717905760678862,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 1.1277785687807645e-06,
       "t_star": 2.5840653292934074e-06,
       "t_star_bi": 2.584300396431581e-06,
       "trunc_T": 2.1832218649834568e-08,
       "truncation_sensitive": false,
       "window_hi": 2.5840653292934074e-06,
       "window_lo": -2.5840653292934074e-06
      }
     },
     "h_Hill": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.003285089780132855,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 3.5493994388586036e-06,
       "t_star": 8.132695800101668e-06,
       "t_star_bi": 8.135651136304486e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 8.132695800101668e-06,
       "window_lo": -8.132695800101668e-06
      }
     }
    },
    "cubic_gem8|111": {
     "E2_HSmean": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.0003687686088987177,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.477173051429366e-07,
       "t_star": 1.4841067898751585e-06,
       "t_star_bi": 1.4841236411415748e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.4841067898751585e-06,
       "window_lo": -1.4841067898751585e-06
      }
     },
     "E2_Hill": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.003168214033920284,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.672027990549506e-07,
       "t_star": 1.528753665277861e-06,
       "t_star_bi": 1.5288927329666916e-06,
       "trunc_T": 1.2916114645286625e-08,
       "truncation_sensitive": false,
       "window_hi": 1.528753665277861e-06,
       "window_lo": -1.528753665277861e-06
      }
     },
     "h_Hill": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.003285089780132855,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 3.5493994388586036e-06,
       "t_star": 8.132695800101668e-06,
       "t_star_bi": 8.135651136304486e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 8.132695800101668e-06,
       "window_lo": -8.132695800101668e-06
      }
     }
    },
    "cubic_step|001": {
     "E2_HSmean": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 9.691527823922576e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 1.2115976975116847e-06,
       "t_star": 2.7761190803407526e-06,
       "t_star_bi": 2.776138659451734e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 2.7761190803407526e-06,
       "window_lo": -2.7761190803407526e-06
      }
     },
     "E2_Hill": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.0009395517784325108,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 1.235493174523598e-06,
       "t_star": 2.830870496427837e-06,
       "t_star_bi": 2.8310444322234794e-06,
       "trunc_T": 1.9912083231728236e-08,
       "truncation_sensitive": false,
       "window_hi": 2.830870496427837e-06,
       "window_lo": -2.830870496427837e-06
      }
     },
     "h_Hill": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.0017661995570374912,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 3.876389084448661e-06,
       "t_star": 8.881923201293279e-06,
       "t_star_bi": 8.88420827798017e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 8.881923201293279e-06,
       "window_lo": -8.881923201293279e-06
      }
     }
    },
    "cubic_step|111": {
     "E2_HSmean": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.0001536867103471558,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 7.167908643480925e-07,
       "t_star": 1.6423741966639787e-06,
       "t_star_bi": 1.6423857798966321e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.6423741966639787e-06,
       "window_lo": -1.6423741966639787e-06
      }
     },
     "E2_Hill": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.0015910837364779516,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 7.309276191973275e-07,
       "t_star": 1.6747655712528054e-06,
       "t_star_bi": 1.6748684729457705e-06,
       "trunc_T": 1.1780147566550347e-08,
       "truncation_sensitive": false,
       "window_hi": 1.6747655712528054e-06,
       "window_lo": -1.6747655712528054e-06
      }
     },
     "h_Hill": {
      "t2": {
       "binding_end": null,
       "class": "NULL-INERT",
       "class_bi": null,
       "nu": null,
       "nu_is_inf": null,
       "nullfloor_sensitive": null,
       "resolution_sensitive": null,
       "sigma_star": null,
       "t_star": null,
       "t_star_bi": null,
       "trunc_T": null,
       "truncation_sensitive": null,
       "window_hi": 0.25,
       "window_lo": -0.25
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.0017661995570374912,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 3.876389084448661e-06,
       "t_star": 8.881923201293279e-06,
       "t_star_bi": 8.88420827798017e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 8.881923201293279e-06,
       "window_lo": -8.881923201293279e-06
      }
     }
    },
    "hex_gem8|a": {
     "E2_HSmean": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 9.258804403403184e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 5.641378268780703e-07,
       "t_star": 1.261450529578373e-06,
       "t_star_bi": 1.2614487630996736e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.261450529578373e-06,
       "window_lo": -1.261450529578373e-06
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 3.1370317523404443e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.593036347748591e-07,
       "t_star": 1.9779109043245774e-06,
       "t_star_bi": 1.977912055898236e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.9779109043245774e-06,
       "window_lo": -1.9779109043245774e-06
      }
     },
     "E2_Hill": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 1.0940535027716599e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 5.625961053806963e-07,
       "t_star": 1.2580031355078722e-06,
       "t_star_bi": 1.2580087380959796e-06,
       "trunc_T": 8.232760971018636e-10,
       "truncation_sensitive": false,
       "window_hi": 1.2580031355078722e-06,
       "window_lo": -1.2580031355078722e-06
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 2.818789642225767e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.582437027892329e-07,
       "t_star": 1.974731108367699e-06,
       "t_star_bi": 1.9747440394197973e-06,
       "trunc_T": 2.4125953747763257e-09,
       "truncation_sensitive": false,
       "window_hi": 1.974731108367699e-06,
       "window_lo": -1.974731108367699e-06
      }
     },
     "h_Hill": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 1.3118827598699444e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 1.3588585706591621e-05,
       "t_star": 3.0385001358020878e-05,
       "t_star_bi": 3.0385424617371403e-05,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 3.0385001358020878e-05,
       "window_lo": -3.0385001358020878e-05
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 3.8821634342049665e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.556391173378819e-06,
       "t_star": 1.966917352013646e-05,
       "t_star_bi": 1.9669708692022073e-05,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.966917352013646e-05,
       "window_lo": -1.966917352013646e-05
      }
     }
    },
    "hex_gem8|b": {
     "E2_HSmean": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 9.335384998721974e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 5.640638409653405e-07,
       "t_star": 1.261285092048132e-06,
       "t_star_bi": 1.2612833248752757e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.261285092048132e-06,
       "window_lo": -1.261285092048132e-06
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 1.4639721165191051e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.593144278436239e-07,
       "t_star": 1.9779432835308717e-06,
       "t_star_bi": 1.977944434704334e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.9779432835308717e-06,
       "window_lo": -1.9779432835308717e-06
      }
     },
     "E2_Hill": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 1.0783959358452934e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 5.625235583858025e-07,
       "t_star": 1.2578409154957262e-06,
       "t_star_bi": 1.2578465208502752e-06,
       "trunc_T": 8.229410601365208e-10,
       "truncation_sensitive": false,
       "window_hi": 1.2578409154957262e-06,
       "window_lo": -1.2578409154957262e-06
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 3.654045425345189e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.582543046391783e-07,
       "t_star": 1.974762913917535e-06,
       "t_star_bi": 1.9747758425979663e-06,
       "trunc_T": 2.4118923297496913e-09,
       "truncation_sensitive": false,
       "window_hi": 1.974762913917535e-06,
       "window_lo": -1.974762913917535e-06
      }
     },
     "h_Hill": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 9.368373146565864e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 1.3585369322521385e-05,
       "t_star": 3.0377809304598083e-05,
       "t_star_bi": 3.0378232848372144e-05,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 3.0377809304598083e-05,
       "window_lo": -3.0377809304598083e-05
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 4.12500587911389e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.5567205670865016e-06,
       "t_star": 1.9670161701259506e-05,
       "t_star_bi": 1.9670696855307497e-05,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.9670161701259506e-05,
       "window_lo": -1.9670161701259506e-05
      }
     }
    },
    "hex_step|a": {
     "E2_HSmean": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 3.396954720549381e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.48161803893943e-07,
       "t_star": 1.4493338539257445e-06,
       "t_star_bi": 1.4493326943741656e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.4493338539257445e-06,
       "window_lo": -1.4493338539257445e-06
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 8.849427014734168e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.974498336049859e-07,
       "t_star": 2.0923495008149578e-06,
       "t_star_bi": 2.092350761684618e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 2.0923495008149578e-06,
       "window_lo": -2.0923495008149578e-06
      }
     },
     "E2_Hill": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 4.4521346323532944e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.456178923261492e-07,
       "t_star": 1.4436454947314095e-06,
       "t_star_bi": 1.4436491698799224e-06,
       "trunc_T": 7.390743039341021e-10,
       "truncation_sensitive": false,
       "window_hi": 1.4436454947314095e-06,
       "window_lo": -1.4436454947314095e-06
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 4.196759984319384e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.963351942674173e-07,
       "t_star": 2.089005582802252e-06,
       "t_star_bi": 2.089017973809244e-06,
       "trunc_T": 2.8844336909060227e-09,
       "truncation_sensitive": false,
       "window_hi": 2.089005582802252e-06,
       "window_lo": -2.089005582802252e-06
      }
     },
     "h_Hill": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 7.153041203327343e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 1.728807926522378e-05,
       "t_star": 3.865732043744499e-05,
       "t_star_bi": 3.86576289493853e-05,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 3.865732043744499e-05,
       "window_lo": -3.865732043744499e-05
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 4.3153079571357646e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.663229476941336e-06,
       "t_star": 1.998968843082401e-05,
       "t_star_bi": 1.99902121402292e-05,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.998968843082401e-05,
       "window_lo": -1.998968843082401e-05
      }
     }
    },
    "hex_step|b": {
     "E2_HSmean": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 3.934370245976813e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.483355318683353e-07,
       "t_star": 1.449722321486079e-06,
       "t_star_bi": 1.4497211628290752e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.449722321486079e-06,
       "window_lo": -1.449722321486079e-06
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 1.1061453878663364e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.974290339257395e-07,
       "t_star": 2.0922871017772188e-06,
       "t_star_bi": 2.0922883634145478e-06,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 2.0922871017772188e-06,
       "window_lo": -2.0922871017772188e-06
      }
     },
     "E2_Hill": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 5.165838366890101e-06,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.457881818921485e-07,
       "t_star": 1.444026273776843e-06,
       "t_star_bi": 1.4440299451707584e-06,
       "trunc_T": 7.396991786279577e-10,
       "truncation_sensitive": false,
       "window_hi": 1.444026273776843e-06,
       "window_lo": -1.444026273776843e-06
      },
      "t4": {
       "binding_end": "hi",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 2.650508262562066e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.963149680443216e-07,
       "t_star": 2.088944904132965e-06,
       "t_star_bi": 2.088957298471811e-06,
       "trunc_T": 2.8855029704933374e-09,
       "truncation_sensitive": false,
       "window_hi": 2.088944904132965e-06,
       "window_lo": -2.088944904132965e-06
      }
     },
     "h_Hill": {
      "t2": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 0.0,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 1.7297158858368365e-05,
       "t_star": 3.8677623024924324e-05,
       "t_star_bi": 3.8677932856194386e-05,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 3.8677623024924324e-05,
       "window_lo": -3.8677623024924324e-05
      },
      "t4": {
       "binding_end": "lo",
       "class": "BINDING",
       "class_bi": "BINDING",
       "nu": 3.3286684421489656e-05,
       "nu_is_inf": false,
       "nullfloor_sensitive": false,
       "resolution_sensitive": false,
       "sigma_star": 6.6626622025342276e-06,
       "t_star": 1.9987986607602684e-05,
       "t_star_bi": 1.998851053790706e-05,
       "trunc_T": null,
       "truncation_sensitive": false,
       "window_hi": 1.9987986607602684e-05,
       "window_lo": -1.9987986607602684e-05
      }
     }
    }
   },
   "two_param": {
    "hex_gem8|a": {
     "E2_HSmean": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "indefinite",
      "null_ray_slope": 3.2459969594961784,
      "total_nodes": 40401
     },
     "E2_Hill": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "indefinite",
      "null_ray_slope": 3.249659452469566,
      "total_nodes": 40401
     },
     "h_Hill": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "negative-definite",
      "null_ray_slope": null,
      "total_nodes": 40401
     }
    },
    "hex_gem8|b": {
     "E2_HSmean": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "indefinite",
      "null_ray_slope": 3.2464758687049406,
      "total_nodes": 40401
     },
     "E2_Hill": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "indefinite",
      "null_ray_slope": 3.2501308980491763,
      "total_nodes": 40401
     },
     "h_Hill": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "negative-definite",
      "null_ray_slope": null,
      "total_nodes": 40401
     }
    },
    "hex_step|a": {
     "E2_HSmean": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "indefinite",
      "null_ray_slope": 2.988666120042645,
      "total_nodes": 40401
     },
     "E2_Hill": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "indefinite",
      "null_ray_slope": 2.995647084883406,
      "total_nodes": 40401
     },
     "h_Hill": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "negative-definite",
      "null_ray_slope": null,
      "total_nodes": 40401
     }
    },
    "hex_step|b": {
     "E2_HSmean": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "indefinite",
      "null_ray_slope": 2.987776171603675,
      "total_nodes": 40401
     },
     "E2_Hill": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "indefinite",
      "null_ray_slope": 2.9947701642622118,
      "total_nodes": 40401
     },
     "h_Hill": {
      "admissible_nodes": 1,
      "area_fraction": 2.475186257765897e-05,
      "compact": true,
      "definiteness": "negative-definite",
      "null_ray_slope": null,
      "total_nodes": 40401
     }
    }
   }
  },
  "combined_empty": false,
  "contains_zero": true,
  "gate": {
   "combined_empty": false,
   "contains_zero": true,
   "gate_class": "WINDOW-DELIVERED",
   "n_void_rows": 0,
   "oom_class_x0p1": "WINDOW-DELIVERED",
   "oom_class_x10": "WINDOW-DELIVERED",
   "oom_robust": true,
   "sigma_strict_hi": 6.582437027892329e-07,
   "sigma_union_hi": 1.235493174523598e-06
  },
  "n_void_rows": 0,
  "row_md5s": [
   "59b357fda68557002f11a40100c3ca9c"
  ],
  "rows": [
   {
    "contains_zero": true,
    "exclusion": null,
    "families": {
     "cubic_gem8|001": {
      "E2_HSmean": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.000209501684318514,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 1.0948420726001125e-06,
        "t_star": 2.5085983358561767e-06,
        "t_star_bi": 2.5086268192989865e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 2.5085983358561767e-06,
        "window_lo": -2.5085983358561767e-06
       }
      },
      "E2_Hill": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.0018717905760678862,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 1.1277785687807645e-06,
        "t_star": 2.5840653292934074e-06,
        "t_star_bi": 2.584300396431581e-06,
        "trunc_T": 2.1832218649834568e-08,
        "truncation_sensitive": false,
        "window_hi": 2.5840653292934074e-06,
        "window_lo": -2.5840653292934074e-06
       }
      },
      "h_Hill": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.003285089780132855,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 3.5493994388586036e-06,
        "t_star": 8.132695800101668e-06,
        "t_star_bi": 8.135651136304486e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 8.132695800101668e-06,
        "window_lo": -8.132695800101668e-06
       }
      }
     },
     "cubic_gem8|111": {
      "E2_HSmean": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.0003687686088987177,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.477173051429366e-07,
        "t_star": 1.4841067898751585e-06,
        "t_star_bi": 1.4841236411415748e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.4841067898751585e-06,
        "window_lo": -1.4841067898751585e-06
       }
      },
      "E2_Hill": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.003168214033920284,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.672027990549506e-07,
        "t_star": 1.528753665277861e-06,
        "t_star_bi": 1.5288927329666916e-06,
        "trunc_T": 1.2916114645286625e-08,
        "truncation_sensitive": false,
        "window_hi": 1.528753665277861e-06,
        "window_lo": -1.528753665277861e-06
       }
      },
      "h_Hill": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.003285089780132855,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 3.5493994388586036e-06,
        "t_star": 8.132695800101668e-06,
        "t_star_bi": 8.135651136304486e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 8.132695800101668e-06,
        "window_lo": -8.132695800101668e-06
       }
      }
     },
     "cubic_step|001": {
      "E2_HSmean": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 9.691527823922576e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 1.2115976975116847e-06,
        "t_star": 2.7761190803407526e-06,
        "t_star_bi": 2.776138659451734e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 2.7761190803407526e-06,
        "window_lo": -2.7761190803407526e-06
       }
      },
      "E2_Hill": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.0009395517784325108,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 1.235493174523598e-06,
        "t_star": 2.830870496427837e-06,
        "t_star_bi": 2.8310444322234794e-06,
        "trunc_T": 1.9912083231728236e-08,
        "truncation_sensitive": false,
        "window_hi": 2.830870496427837e-06,
        "window_lo": -2.830870496427837e-06
       }
      },
      "h_Hill": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.0017661995570374912,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 3.876389084448661e-06,
        "t_star": 8.881923201293279e-06,
        "t_star_bi": 8.88420827798017e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 8.881923201293279e-06,
        "window_lo": -8.881923201293279e-06
       }
      }
     },
     "cubic_step|111": {
      "E2_HSmean": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.0001536867103471558,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 7.167908643480925e-07,
        "t_star": 1.6423741966639787e-06,
        "t_star_bi": 1.6423857798966321e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.6423741966639787e-06,
        "window_lo": -1.6423741966639787e-06
       }
      },
      "E2_Hill": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.0015910837364779516,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 7.309276191973275e-07,
        "t_star": 1.6747655712528054e-06,
        "t_star_bi": 1.6748684729457705e-06,
        "trunc_T": 1.1780147566550347e-08,
        "truncation_sensitive": false,
        "window_hi": 1.6747655712528054e-06,
        "window_lo": -1.6747655712528054e-06
       }
      },
      "h_Hill": {
       "t2": {
        "binding_end": null,
        "class": "NULL-INERT",
        "class_bi": null,
        "nu": null,
        "nu_is_inf": null,
        "nullfloor_sensitive": null,
        "resolution_sensitive": null,
        "sigma_star": null,
        "t_star": null,
        "t_star_bi": null,
        "trunc_T": null,
        "truncation_sensitive": null,
        "window_hi": 0.25,
        "window_lo": -0.25
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.0017661995570374912,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 3.876389084448661e-06,
        "t_star": 8.881923201293279e-06,
        "t_star_bi": 8.88420827798017e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 8.881923201293279e-06,
        "window_lo": -8.881923201293279e-06
       }
      }
     },
     "hex_gem8|a": {
      "E2_HSmean": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 9.258804403403184e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 5.641378268780703e-07,
        "t_star": 1.261450529578373e-06,
        "t_star_bi": 1.2614487630996736e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.261450529578373e-06,
        "window_lo": -1.261450529578373e-06
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 3.1370317523404443e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.593036347748591e-07,
        "t_star": 1.9779109043245774e-06,
        "t_star_bi": 1.977912055898236e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.9779109043245774e-06,
        "window_lo": -1.9779109043245774e-06
       }
      },
      "E2_Hill": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 1.0940535027716599e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 5.625961053806963e-07,
        "t_star": 1.2580031355078722e-06,
        "t_star_bi": 1.2580087380959796e-06,
        "trunc_T": 8.232760971018636e-10,
        "truncation_sensitive": false,
        "window_hi": 1.2580031355078722e-06,
        "window_lo": -1.2580031355078722e-06
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 2.818789642225767e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.582437027892329e-07,
        "t_star": 1.974731108367699e-06,
        "t_star_bi": 1.9747440394197973e-06,
        "trunc_T": 2.4125953747763257e-09,
        "truncation_sensitive": false,
        "window_hi": 1.974731108367699e-06,
        "window_lo": -1.974731108367699e-06
       }
      },
      "h_Hill": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 1.3118827598699444e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 1.3588585706591621e-05,
        "t_star": 3.0385001358020878e-05,
        "t_star_bi": 3.0385424617371403e-05,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 3.0385001358020878e-05,
        "window_lo": -3.0385001358020878e-05
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 3.8821634342049665e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.556391173378819e-06,
        "t_star": 1.966917352013646e-05,
        "t_star_bi": 1.9669708692022073e-05,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.966917352013646e-05,
        "window_lo": -1.966917352013646e-05
       }
      }
     },
     "hex_gem8|b": {
      "E2_HSmean": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 9.335384998721974e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 5.640638409653405e-07,
        "t_star": 1.261285092048132e-06,
        "t_star_bi": 1.2612833248752757e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.261285092048132e-06,
        "window_lo": -1.261285092048132e-06
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 1.4639721165191051e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.593144278436239e-07,
        "t_star": 1.9779432835308717e-06,
        "t_star_bi": 1.977944434704334e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.9779432835308717e-06,
        "window_lo": -1.9779432835308717e-06
       }
      },
      "E2_Hill": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 1.0783959358452934e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 5.625235583858025e-07,
        "t_star": 1.2578409154957262e-06,
        "t_star_bi": 1.2578465208502752e-06,
        "trunc_T": 8.229410601365208e-10,
        "truncation_sensitive": false,
        "window_hi": 1.2578409154957262e-06,
        "window_lo": -1.2578409154957262e-06
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 3.654045425345189e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.582543046391783e-07,
        "t_star": 1.974762913917535e-06,
        "t_star_bi": 1.9747758425979663e-06,
        "trunc_T": 2.4118923297496913e-09,
        "truncation_sensitive": false,
        "window_hi": 1.974762913917535e-06,
        "window_lo": -1.974762913917535e-06
       }
      },
      "h_Hill": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 9.368373146565864e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 1.3585369322521385e-05,
        "t_star": 3.0377809304598083e-05,
        "t_star_bi": 3.0378232848372144e-05,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 3.0377809304598083e-05,
        "window_lo": -3.0377809304598083e-05
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 4.12500587911389e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.5567205670865016e-06,
        "t_star": 1.9670161701259506e-05,
        "t_star_bi": 1.9670696855307497e-05,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.9670161701259506e-05,
        "window_lo": -1.9670161701259506e-05
       }
      }
     },
     "hex_step|a": {
      "E2_HSmean": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 3.396954720549381e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.48161803893943e-07,
        "t_star": 1.4493338539257445e-06,
        "t_star_bi": 1.4493326943741656e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.4493338539257445e-06,
        "window_lo": -1.4493338539257445e-06
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 8.849427014734168e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.974498336049859e-07,
        "t_star": 2.0923495008149578e-06,
        "t_star_bi": 2.092350761684618e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 2.0923495008149578e-06,
        "window_lo": -2.0923495008149578e-06
       }
      },
      "E2_Hill": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 4.4521346323532944e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.456178923261492e-07,
        "t_star": 1.4436454947314095e-06,
        "t_star_bi": 1.4436491698799224e-06,
        "trunc_T": 7.390743039341021e-10,
        "truncation_sensitive": false,
        "window_hi": 1.4436454947314095e-06,
        "window_lo": -1.4436454947314095e-06
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 4.196759984319384e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.963351942674173e-07,
        "t_star": 2.089005582802252e-06,
        "t_star_bi": 2.089017973809244e-06,
        "trunc_T": 2.8844336909060227e-09,
        "truncation_sensitive": false,
        "window_hi": 2.089005582802252e-06,
        "window_lo": -2.089005582802252e-06
       }
      },
      "h_Hill": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 7.153041203327343e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 1.728807926522378e-05,
        "t_star": 3.865732043744499e-05,
        "t_star_bi": 3.86576289493853e-05,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 3.865732043744499e-05,
        "window_lo": -3.865732043744499e-05
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 4.3153079571357646e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.663229476941336e-06,
        "t_star": 1.998968843082401e-05,
        "t_star_bi": 1.99902121402292e-05,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.998968843082401e-05,
        "window_lo": -1.998968843082401e-05
       }
      }
     },
     "hex_step|b": {
      "E2_HSmean": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 3.934370245976813e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.483355318683353e-07,
        "t_star": 1.449722321486079e-06,
        "t_star_bi": 1.4497211628290752e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.449722321486079e-06,
        "window_lo": -1.449722321486079e-06
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 1.1061453878663364e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.974290339257395e-07,
        "t_star": 2.0922871017772188e-06,
        "t_star_bi": 2.0922883634145478e-06,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 2.0922871017772188e-06,
        "window_lo": -2.0922871017772188e-06
       }
      },
      "E2_Hill": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 5.165838366890101e-06,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.457881818921485e-07,
        "t_star": 1.444026273776843e-06,
        "t_star_bi": 1.4440299451707584e-06,
        "trunc_T": 7.396991786279577e-10,
        "truncation_sensitive": false,
        "window_hi": 1.444026273776843e-06,
        "window_lo": -1.444026273776843e-06
       },
       "t4": {
        "binding_end": "hi",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 2.650508262562066e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.963149680443216e-07,
        "t_star": 2.088944904132965e-06,
        "t_star_bi": 2.088957298471811e-06,
        "trunc_T": 2.8855029704933374e-09,
        "truncation_sensitive": false,
        "window_hi": 2.088944904132965e-06,
        "window_lo": -2.088944904132965e-06
       }
      },
      "h_Hill": {
       "t2": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 0.0,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 1.7297158858368365e-05,
        "t_star": 3.8677623024924324e-05,
        "t_star_bi": 3.8677932856194386e-05,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 3.8677623024924324e-05,
        "window_lo": -3.8677623024924324e-05
       },
       "t4": {
        "binding_end": "lo",
        "class": "BINDING",
        "class_bi": "BINDING",
        "nu": 3.3286684421489656e-05,
        "nu_is_inf": false,
        "nullfloor_sensitive": false,
        "resolution_sensitive": false,
        "sigma_star": 6.6626622025342276e-06,
        "t_star": 1.9987986607602684e-05,
        "t_star_bi": 1.998851053790706e-05,
        "trunc_T": null,
        "truncation_sensitive": false,
        "window_hi": 1.9987986607602684e-05,
        "window_lo": -1.9987986607602684e-05
       }
      }
     }
    },
    "id": "SA-1",
    "row_md5": "59b357fda68557002f11a40100c3ca9c",
    "two_param": {
     "hex_gem8|a": {
      "E2_HSmean": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "indefinite",
       "null_ray_slope": 3.2459969594961784,
       "total_nodes": 40401
      },
      "E2_Hill": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "indefinite",
       "null_ray_slope": 3.249659452469566,
       "total_nodes": 40401
      },
      "h_Hill": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "negative-definite",
       "null_ray_slope": null,
       "total_nodes": 40401
      }
     },
     "hex_gem8|b": {
      "E2_HSmean": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "indefinite",
       "null_ray_slope": 3.2464758687049406,
       "total_nodes": 40401
      },
      "E2_Hill": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "indefinite",
       "null_ray_slope": 3.2501308980491763,
       "total_nodes": 40401
      },
      "h_Hill": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "negative-definite",
       "null_ray_slope": null,
       "total_nodes": 40401
      }
     },
     "hex_step|a": {
      "E2_HSmean": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "indefinite",
       "null_ray_slope": 2.988666120042645,
       "total_nodes": 40401
      },
      "E2_Hill": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "indefinite",
       "null_ray_slope": 2.995647084883406,
       "total_nodes": 40401
      },
      "h_Hill": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "negative-definite",
       "null_ray_slope": null,
       "total_nodes": 40401
      }
     },
     "hex_step|b": {
      "E2_HSmean": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "indefinite",
       "null_ray_slope": 2.987776171603675,
       "total_nodes": 40401
      },
      "E2_Hill": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "indefinite",
       "null_ray_slope": 2.9947701642622118,
       "total_nodes": 40401
      },
      "h_Hill": {
       "admissible_nodes": 1,
       "area_fraction": 2.475186257765897e-05,
       "compact": true,
       "definiteness": "negative-definite",
       "null_ray_slope": null,
       "total_nodes": 40401
      }
     }
    },
    "void_regime": false
   }
  ],
  "sealed_bytes": 177,
  "sealed_md5": "cfd62dcf060427ac3402604e6c3284ff",
  "t1_a1_md5": "3b753b3a371a162fc2ab21b9eed51bd5"
 },
 "pinned_inputs_bytes": 96761,
 "pinned_inputs_md5": "2d44ec01a66889f330d940dee3313bdc",
 "scanner_md5": "6b86290090a8c84f1b1a0a99ec0bf697",
 "schema_md5": "5323e11fc27d688f61aaf57302c875c0",
 "t1_a1_md5": "3b753b3a371a162fc2ab21b9eed51bd5",
 "t1_base_md5": "05302210cc4ceb70553acbe8379e9fc3",
 "t1_list_md5": "e274e58ea50b9ed347969e507d2a4f36",
 "utc": "2026-09-30T05:28:13Z",
 "verifier_md5": "cf004d517d2efe91a02c92a58e3df6bf"
}
=====END-EMBED name=g_mscs_a_ccleg_checkpoint.json=====

