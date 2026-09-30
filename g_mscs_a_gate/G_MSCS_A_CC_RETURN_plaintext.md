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

