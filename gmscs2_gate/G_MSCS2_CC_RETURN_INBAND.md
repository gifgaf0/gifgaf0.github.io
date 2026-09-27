# G-MSCS2 — CC LEG RETURN (P-4 single-file in-band, mirrored) — September 26, 2026

**Gate:** G-MSCS2 (the l = 4 / cubic-effective texture family). **Leg:** CC, built blind from scratch. **Base:** V4.84 `f36bbdb04104008783f2763f70fb916f` (not held; not needed). **Lock chain honoured:** memo v2 `efdcabdcd937cda4acb64f941dc4bb2b` (46,053 B) · lock record `49232d4c42061c4536867eba14aae501` (A-2.1–A-2.10) **+ Addendum A-3 (§0b of the dispatch) in force** · schema v1.0 `66f586d7b6c5e8228394222ddfda73f2` · comparator v1.0 `80d3b9078788fb17f57945da7d9c2c96` · T1 gate list `be921b8c29f7578e85ed92f1450c1956` (36 patterns; scanner `6b86290090a8c84f1b1a0a99ec0bf697`) · X-1 `200e7a8b775577564369c6924d38a84c` · X-6 chat `c04c0b8ea34cfe60f231aa06828e6ce4` / cc `249e11dd53c4cb82f302b15d3c94c337`. All md5 + byte guarded by the instrument at every invocation.

**Activation flag received, verbatim, in the author's directive:** `ACTIVATE: G-MSCS2-CC-LEG-1 WITH-A3`

## 1. Branch and commits (pre-consultation first)

Branch `claude/hk1-gmscs2-dispatch-e6vcfh`, started from `main` = **`d0a0e31`** (the PR #13 merge; the state the dispatch §5 records, unchanged at start). Directory `gmscs2_gate/`.

| Commit | Content |
|---|---|
| **`ead55bb`** — **pre-consultation checkpoint** | `dispatch.md` (quarantine still armored), the ten plaintext embeds, the instrument `g_mscs2_ccleg.py` (md5 **`e58ba9a6d52daa23f8264255b6dbbb75`**), its checkpoint `g_mscs2_ccleg_checkpoint.json` (md5 **`9961745d1e1857cfab6445d4754b5060`**, quoted in the commit message), `run_ccleg.log`. No quarantined embed was decoded before this commit. |
| `d7fd5c7` — armor opened | The twelve decoded embeds (all md5/bytes as inventoried), `g_mscs2_twoleg_comparison.json` (`a91d84a5b5cbe24221aa2e6301c67675`), the chat-vs-chat re-run `g_mscs2_chatleg_selfcompare_CCRERUN.json` (byte-identical to the quarantined `0a10623660c8fbaed4c37ec388978593`), the CC-vs-CC sanity `g_mscs2_ccleg_selfcompare.json` (`7951e0f0e41607a7372d8269a51f83ef`), the hypothesis compare `g_mscs2_cc_hypothesis_compare.py` → `g_mscs2_ccleg_compare.json` (`daedd0dee64536be10ea1bd79c7a9c41`, written last). |
| (this commit) — return | `G_MSCS2_CC_RETURN_INBAND.md` (this file, with the six embeds), and the HK-1 return `gmscs1_gate/HK1_CC_RETURN_INBAND.md`. |

The HK-1 housekeeping preceded this leg in the same session, as directed: **PR #27** (`gmscs1_gate/estate/`, branch `…-task-a`, head `e3380c1`) and **PR #28** (V4.79 canonical removal, branch `…-task-b`, head `9f530f0`), both from `d0a0e31`, both OPEN at the time of writing (the author merges). Nothing in this leg depends on them; the dispatch §5 / memo §10 observation ("no PR #27 in `main`'s history") is now superseded by these two PRs, which is the fact the V4.85 bracket carries.

## 2. Instrument and execution summary

**`g_mscs2_ccleg.py`** (md5 `e58ba9a6`), numpy only; built from the memo (§0–§2, §4–§9), the lock record (A-2, A-3) and the schema; the G-MSCS1 instruments on `main` read for the inherited descriptor definitions, not copied. Guards: md5 + bytes on the memo, lock record, schema, T1 list, scanner, X-1, both X-6 files; T1 self-scan of the instrument and the memo at every invocation, halt on any hit, no override; the emitted checkpoint T1-scanned before it is written (fixed point on the collision count). Runtime **170 s** (single process, 8192-direction k̂ rule).

**Method variations executed (lock record §3; dispatch §0):**
1. **SO(3) averages by the fiber-axis route, not an Euler product grid.** Every ODF of this gate is a function of the fiber axis in the crystal frame, n = g⁻¹ẑ (the K̃₄, P₄, P₆, K₆ families and the inherited l = 2 family alike: P₂((g·n_c)·ẑ) = P₂(n_c·n)). Writing g = R_z(ψ)·g₀(n), the ψ-average — the SO(2) coset average about the sample fiber axis — is done **analytically**: for rank-4 tensors it is the orthogonal projection onto the five-dimensional transversely-isotropic subspace (Mandel inner product; a 36 × 36 projector built from an orthonormalized TI basis; selftested against a 12-point uniform ψ average, 6.7e-16); for the per-grain E₂ weight it is the closed-form circular moment of the degree-4 polynomial, which leaves f̄ = a₀ + a₂x² + a₄x⁴ with x = n_c·n per mode (selftested against brute force, 2.2e-16, and against the sphere identity a₀ + a₂/3 + a₄/5 = 2/5). What remains is an S² integral over n, done with **GL(cos θ) 16 × uniform φ 32 on a generically rotated node set** (512 nodes; exact for polynomial degree ≤ 31 in n; the gate needs ≥ 12). The uniform average of the fiber table reproduces the closed-form isotropic projection to 1.3e-15; ⟨K̃₄⟩ = 4e-17, ⟨K̃₄²⟩ − 4/21 = −5.6e-17, ⟨P₄²⟩ − 1/9 = −2.8e-17, ⟨K₆⟩ = 1.6e-15, ⟨K₆K̃₄⟩ = 1.1e-16. (The chat leg's grid is the ZYZ (16, 10, 16) product; no scipy was available here, so the Lebedev option was not taken.)
2. **Factorized E₂ fraction:** frac_E₂(n̂) = (1 − (k̂·n̂)²)(1 − (ê⊥·n̂)²), derived from the memo 2.2 m = ±2 projection formula and selftested against it (6.8e-16). The marginal moments F₀, F₂, F₄, F₆ per mode use the pinned GL 12 × 24 n̂-rule; the SO(3)-direct average (F-CTRL-MARG) uses the fiber route above — two constructions, compared to 1.7e-14 on every mode.
3. **Own HS reference optimizer** (boundary-K₀ bisection on the feasibility eigenvalue, a 600-point coarse scan and nine nested 21-point refinements over G₀): reproduces the X-6 `hs_ref` / `G_HS` to 1.5e-12 relative (PIN-HS0).
4. Own branch labelling (qL by maximal admixture; the birefringence pair by polarization overlap along k̂ = x̂, overlaps 1.000), own least-squares fits (numpy lstsq on [t, t², t³] and on the 7-column (t₂, t₄) basis), own checkpoint layout (`extras` for everything beyond the schema).

**Environment note:** the container had neither numpy nor scipy; numpy 2.4.6 was installed with pip for this session (D-CC-1, §8).

## 3. Phase 0 (13 items; all PASS; chat values from the decoded checkpoint for comparison)

| Item | CC float(s) | Chat float(s) | Rule |
|---|---|---|---|
| PIN-XTAL | worst_rel 4.0e-13 (vs the CC X-6 1.6e-14) | 0 | ≤ 1e-8 |
| PIN-VRH0 | 3.7e-15 | 0 | ≤ 1e-8 |
| PIN-HS0 | 1.5e-12 | 0 | ≤ 1e-6 |
| PIN-K2 | hex rel 1.9e-12; cubic abs 3.1e-15 | 1.4e-12; 2.2e-15 | ≤ 1e-4; ≤ 1e-12 |
| F-CTRL-ISO | 4.4e-16 (both paths) | 4.4e-16 | ≤ 1e-10 |
| F-CTRL-SO3 | dev 7.8e-16; r_agg(0) 3.3e-16 | 5.0e-16; 0 | ≤ 1e-10; ≤ 1e-6 |
| F-CTRL-POS | min 0.335 (512 fiber nodes, 337 ODFs) | 0.395 | ≥ 0 |
| F-CTRL-L2NULL (A-3.1 scope) | 8.0e-15 | 5.9e-14 | ≤ 1e-12 |
| F-CTRL-L4EXHAUST | tensor 6.4e-15; r_agg 5.6e-16 | 4.3e-14; 4.4e-16 | ≤ 1e-12 |
| F-CTRL-C4 | closed form 1.7e-15; affine 3.5e-15; H = 0 effect 3.0e-15 | 2.5e-14; 4.1e-14; 2.3e-14 | ≤ 1e-12 |
| F-CTRL-MARG | 1.7e-14 (8 mode sets: 4 cubic keys × t₄ = ±0.5) | 8.3e-16 | ≤ 1e-12 |
| F-CTRL-TEX4 | 4.118e-4 | 4.118e-4 | > 1e-6 |
| F-CTRL-QUAD | 2.2e-16 | 2.3e-14 | ≤ 1e-10 |

Marginal coefficients derived, not assumed: c_⟨001⟩ = K̃₄(ẑ) = 1, c_⟨111⟩ = K̃₄((1,1,1)/√3) = −2/3 (to 5e-16), and c₂ = 1 on every key. The A-2.2 Voigt table of (H/3)𝒯⁴(ẑ) reproduced from the traceless projection of ẑ⊗ẑ⊗ẑ⊗ẑ (1.4e-17). H = −97.1364 (cubic:step) / −170.3875 (cubic:gem8); H_S = +7.75e-3 / +6.99e-3. The Voigt birefringence identity v²_qSH − v²_qSV = Ht₄/21 holds to 2.7e-13 (in-instrument, extras).

## 4. Phase 2 coefficients per key (Hill unless stated; substrate ratios; the chat leg agrees on every one, §6)

| Key | κ₄₄(S2-E₂) | HS-mean | κ₄₄(S2-h) | κ₄₄₄ | S₄(E₂) | halving dev | b₁ | v_T(0) | κ₂(E₂), l = 2 pin |
|---|---|---|---|---|---|---|---|---|---|
| hex_step\|a | **+1.604053e-4** | +1.598930e-4 | −7.508e-6 | +2.215e-7 | −2.2e-13 | 1.6e-9 | +1.624085e-2 | 8.4190596 | −1.439462e-3 |
| hex_step\|b | +1.604147e-4 | +1.599026e-4 | −7.509e-6 | +2.216e-7 | −2.2e-13 | 1.6e-9 | +1.624180e-2 | 8.4192786 | −1.438703e-3 |
| hex_gem8\|a | **+1.795073e-4** | +1.789306e-4 | −7.754e-6 | +2.193e-7 | −2.7e-13 | 2.0e-9 | +1.817488e-2 | 10.0417218 | −1.895648e-3 |
| hex_gem8\|b | +1.795015e-4 | +1.789247e-4 | −7.754e-6 | +2.192e-7 | −2.6e-13 | 2.0e-9 | +1.817430e-2 | 10.0415541 | −1.896137e-3 |
| cubic_step\|001 | **−3.743529e-4** | −3.892647e-4 | −3.803e-5 | +2.633e-6 | −2.0e-11 | 3.9e-8 | −3.789870e-2 | 7.7990464 | +3.1e-15 |
| cubic_step\|111 | **+2.495686e-4** | +2.595098e-4 | −3.803e-5 | −1.755e-6 | +1.3e-11 | 2.6e-8 | −3.789870e-2 | 7.7990464 | +2.9e-15 |
| cubic_gem8\|001 | **−4.492771e-4** | −4.767152e-4 | −4.536e-5 | +3.796e-6 | −4.3e-11 | 6.9e-8 | −4.548125e-2 | 9.3078991 | +1.2e-15 |
| cubic_gem8\|111 | **+2.995181e-4** | +3.178101e-4 | −4.536e-5 | −2.531e-6 | +2.8e-11 | 4.6e-8 | −4.548125e-2 | 9.3078991 | −4.4e-16 |

Every halving deviation ≤ max(1e-4·|κ₄₄|, 1e-6) (per-leg rule) on both legs; fit residuals 8e-12 (hex) to 3e-10 (cubic). κ₄₄(⟨111⟩)/κ₄₄(⟨001⟩) = −0.66667 on both fcc configurations (= c_⟨111⟩/c_⟨001⟩). The r_agg arrays (VRH, HS, V, R; both arms), λ̄_L(t₄), v_qSH/v_qSV(t₄) along x̂, and the strict-window fits are in the checkpoint.

**Second arm — the (t₂, t₄) quadratic form (5 × 5 grid, 7-term fit; A-3.2 Richardson beside it):**

| Key | κ₂₂ | κ₂₄ (7-term fit) | κ₄₄ | residual | κ₂₄ Richardson (A-3.2) |
|---|---|---|---|---|---|
| hex_step\|a | −1.439469e-3 | −1.2489e-8 | +1.603990e-4 | 6.9e-10 | +3.0e-13 |
| hex_step\|b | −1.438710e-3 | −1.2485e-8 | +1.604084e-4 | 6.9e-10 | +1.9e-13 |
| hex_gem8\|a | −1.895660e-3 | −1.8372e-8 | +1.794984e-4 | 1.1e-9 | +1.4e-12 |
| hex_gem8\|b | −1.896149e-3 | −1.8376e-8 | +1.794926e-4 | 1.1e-9 | +9.5e-13 |
| cubic_step\|001 (reading (i)) | +4.482e-9 | +1.9740e-7 | −3.743546e-4 | 4.7e-9 | −7.6e-13 |
| cubic_step\|111 (reading (i)) | −2.988e-9 | +1.9740e-7 | +2.495697e-4 | 4.6e-9 | −2.2e-12 |
| cubic_gem8\|001 (reading (i)) | +7.964e-9 | +3.4779e-7 | −4.492800e-4 | 8.3e-9 | +1.2e-12 |
| cubic_gem8\|111 (reading (i)) | −5.309e-9 | +3.4779e-7 | +2.995200e-4 | 8.1e-9 | −3.7e-13 |

Hex κ₂₂ reproduces the l = 2 pin to 5e-6 relative; the 7-term κ₄₄ matches the one-parameter κ₄₄ to 4e-5 relative. **The basis-independent cross coefficient is null on every key** (|κ₂₄_Richardson| ≤ 2.2e-12, the estimator's own noise): the quadratic form is diagonal in l. Under reading (ii) (extras `x_quadform_reading_ii_Oh_symmetrized`) the cubic form gives κ₂₄ = 0 exactly and the same κ₂₂ ≈ +4.5e-9 / −3.0e-9 / +8.0e-9 / −5.3e-9 — i.e. the cubic κ₂₂ values are not the l = 2 weight at all but the t₄⁴ content of r(t₄) aliasing into the t₂² column of a basis without a constant term (the chat's 12-term refit, `diag_quadform_basis.json`, shows the same). The cubic κ₂₄ ≈ 2e-7 / 3.5e-7 under reading (i) is the third-order t₂t₄² coupling (fit coefficient −5.9e-5 / −1.0e-4, in the discarded terms) plus higher odd terms aliasing into t₂t₄.

## 5. Verdict class (assembled last, by the schema rule): **IDENTITY-DELIVERED-L4**

All 13 Phase-0 items pass; **F-MS2-3 SILENT** (worst |S₄| = 4.267e-11 over the eight keys and both arms; first-order protection holds in the l = 4 families); **F-MS2-4 SILENT** (|κ₄₄(S2-E₂)| = 3.74e-4 and 4.49e-4 on the primary cubic keys, far above the 1e-6 floor: the fcc branch, blind at l = 2, has a non-zero second-order texture split at l = 4); F-MS2-2 REGISTERED_NOT_EXECUTED. The chat leg reports the identical class and states.

## 6. Two-leg comparison (comparator v1.0 frozen; chat `1c5b6b59` vs CC `9961745d`)

**356 checks, 340 PASS, 16 MISS** (`g_mscs2_twoleg_comparison.json` `a91d84a5`). Independence witness: instrument md5s differ (`f277580d` vs `e58ba9a6`). Every C0 provenance row, every C1 Phase-0 row (both `passed` flags and every float re-evaluated per leg), every C2 cross-leg row and every C3 verdict row PASSES. Cross-leg agreement, worst over the eight keys: r_agg arrays (VRH, HS, V, R, h) ≤ 6.7e-16 absolute; λ̄_L(t₄) 2.4e-17; S₄ 2.3e-15; b₁ 1.5e-14; κ₄₄(E₂) 2.1e-11 relative; κ₄₄(HS) 1.7e-11; κ₄₄(h) 3.2e-10; κ₄₄₄ 2.1e-7; v_T(VRH) 1.7e-15; v_T(HS) 1.5e-12; quadform κ₄₄ 1.2e-11, κ₂₂ 5.0e-7, κ₂₄ 3.1e-7 (relative, on the null-level values); halving deviations 2.8e-14. Two constructions of the SO(3) average — an Euler product grid and the analytic-coset fiber route — witness the exhaustion, affinity, cubic-null and marginal identities at machine precision.

**The 16 misses, classified — all DEFINITIONAL, none representational, none substantive:**

| Rows | Miss | Class | Ground |
|---|---|---|---|
| 8 | `phase2[cubic_*].quadform.kappa22` cubic null ≤ 1e-10, chat and cc columns (values +4.5e-9 / −3.0e-9 / +8.0e-9 / −5.3e-9, identical on both legs to 5e-7 relative) | **definitional** (A-3.2, pre-classified: fit-basis resolution) | Not an l = 2 effect: the identical values appear under reading (ii) where no l = 2 term exists; it is the t₄⁴ content of r(t₄) aliasing into the t₂² column of the constant-free 7-term basis. The true κ₂₂ on cubic is zero (the chat's 12-term refit: −9e-15). |
| 8 | `phase2[cubic_*].quadform.kappa24` cubic null ≤ 1e-10, chat and cc columns (values +1.974e-7 / +3.478e-7, identical on both legs to 3e-7 relative) | **definitional** (A-3.2, pre-classified) | Under reading (i) (both legs, CC-DD-1) the single-axis l = 2 weight couples to the l = 4 speed perturbation at third order (t₂t₄²), and the higher odd terms alias into t₂t₄; the basis-independent estimator gives κ₂₄ ≤ 2.2e-12 on every key, both legs. The true κ₂₄ is zero (diagonality). |

The chat-vs-chat re-run reproduces the quarantined self-compare **byte-for-byte** (356 / 338 / 18: the two structural self-comparison rows + the same sixteen); the CC-vs-CC sanity has the same structure (338 / 18). Neither checkpoint was edited.

**Hypothesis compare (last; `g_mscs2_ccleg_compare.json`, 25 clauses, 20 met):** HYP-MS2-2 (sign flip ⟨001⟩ < 0 < ⟨111⟩) met on all four cubic keys and sharpened to the exact ratio −2/3; HYP-MS2-3 (S₄ = 0) met everywhere; HYP-MS2-5 met (|b₁| ≈ 4e-2 per unit t₄, ≈ 400× the descriptor split at t₄ = 0.25); HYP-MS2-1's existence clause met, its magnitude clause NOT met (|κ₄₄| = 2.5–4.5e-4 on fcc, below the M-naive 1e-3–1e-2 and below the hex κ₂); HYP-MS2-4's dominance clause met (|κ₄₄|/|κ₂₂| = 0.11 / 0.095 on hex) and its pin clause met, its cross-term clause NOT met (κ₂₄ is null). Same concordance pattern as the chat leg (3/5 hypotheses).

## 7. CC-DD items (design decisions where the lock record left a choice)

- **CC-DD-1 (A-3.3 — the cubic two-parameter reading): reading (i), the inherited descriptor-axis P₂.** The lock record A-2.2 defines "the l = 2 family" as exactly G-MSCS1's w = 1 + t·P₂((g·axis_c)·ẑ) and A-2.3 says "on cubic keys the same fit is run"; reading (i) is also the only one under which the comparison tests anything (under (ii) κ₂₂ = κ₂₄ = 0 by construction). Reading (ii) is computed and reported beside it in extras. The chat leg took reading (i) as well (its report §2), so the quadform rows compare like for like.
- **CC-DD-2 (fit windows):** inclusive |t₄| ≤ 0.25 (9 grid points) and |t₄| ≤ 0.1 (7 points), the G-MSCS1 convention the pin PIN-K2 rides on; the lock record's counts "7" and "5" do not match the pinned grid (H-CC-1). Strict-window (7 / 5 point) fits are reported in `phase2[key].x_fit_windows` (κ₄₄ differs by ≤ 1.5e-4 relative). The chat leg's "win0.1" values match mine to 1e-11, so both legs took the inclusive windows.
- **CC-DD-3 (K₆ amplitude):** K₆ normalized to max|K₆| = 1 on the sphere (raw scale 4.617e-2), t₆ = 0.3, evaluated at base t₄ = 0.25 on every key and additionally at (t₂, t₄) = (0.25, 0.25) on the hex keys; on the cubic keys the SO(3)-direct E₂ weight change under the K₆ term is also reported (≤ 3.9e-16).
- **CC-DD-4 (F-CTRL-L2NULL `worst_abs`):** the worst of the relative tensor changes (⟨C⟩_V, ⟨S⟩_R, C_HS lo and hi; relative to the largest entry) and the absolute r_agg changes, over all four cubic keys; the mixed-term r_agg change reported separately as `mixed_r_agg_change_A29` (A-3.1).
- **CC-DD-5 (F-CTRL-POS "SO(3) grid"):** the 512 fiber nodes (every ODF depends on n only); 337 ODFs checked (both grids, the Richardson stencil, t₂ = 1, the t₆ cases, the C4 and birefringence points).
- **CC-DD-6 (F-CTRL-SO3):** the worst over all eight keys of the per-mode deviation of F₀ from 2/5 (modes with w_EM > 1e-6), not only hex_step|a; r_agg(0) likewise.
- **CC-DD-7 (F-CTRL-MARG):** on the Hill-tensor modes of all four cubic keys at t₄ = +0.5 and −0.5, every mode with transverse content.
- **CC-DD-8 (checkpoint extras):** the A-3 diagnostics sit both under their named keys (`phase0["F-CTRL-L2NULL"].mixed_r_agg_change_A29`, `phase2[key].kappa24_richardson`) and mirrored under `extras.A3_diagnostics`.

## 8. H-CC items (disagreements with the memo / lock record / schema; self-caught bugs) and deviations

- **H-CC-1 (lock record A-2.3 point counts):** "the 7 grid points with |t₄| ≤ 0.25" and "the 5 points with |t₄| ≤ 0.1" — the pinned 12-point grid has 9 and 7 such points (inclusive). Resolved per CC-DD-2; recorded for the process note. No effect on the comparison (both legs agree to 2e-11).
- **H-CC-2 (self-caught, pre-commit):** the first blind run's extras-only Voigt-birefringence identity check used H = C₁₁ − C₁₂ − C₄₄ (one C₄₄ instead of two) and reported a spurious residual of order 1; caught in the pre-commit inspection of the checkpoint (the F-CTRL-C4 block, which uses the correct H, had passed), fixed, and the instrument re-run in full before the pre-consultation commit. No verdict-bearing quantity changed between the two runs.
- **H-CC-3 (representational; not compared):** my `mixed_r_agg_change_A29` is the signed difference r(0.25, 0.25) − r(0, 0.25) = −9.076e-7 (cubic:step) / −1.304e-6 (cubic:gem8), negative on all four keys; the chat's diagnostic carries the same magnitudes with the opposite sign convention. Magnitudes agree to 1e-16. Under LITERAL-A29 this quantity would have failed the control (1.3e-6 > 1e-12) and sent the leg to INDETERMINATE — recorded in the checkpoint as `x_literal_A29_would_pass: false`; under A-3.1 it is the diagnostic, as the addendum foresaw.
- **H-CC-4 (memo §2.5 / HYP-MS2-4 expectation):** the memo describes the hex cross-coefficient κ₂₄ as the term that "completes the quadratic form"; the machine finds it null on every key by a basis-independent estimator (both legs). The quadratic form of the general weak fiber texture is diagonal, r_agg = κ₂₂t₂² + κ₄₄t₄² + O(t³); cross-coupling begins at third order. A finding, not a falsifier (the memo §5 lists κ₂₄ ≠ 0 among the non-falsifiers, and its absence is likewise none).
- **D-CC-1 (environment):** the session container lacked numpy and scipy; numpy was installed with pip. The instrument depends on numpy only.
- **D-CC-2 (branch):** this leg runs on the session's designated branch `claude/hk1-gmscs2-dispatch-e6vcfh` rather than a `claude/new-session-*` name; the two HK-1 PR branches carry `-task-a` / `-task-b` suffixes of it.
- Nothing else deviated from the dispatch as written; no canonical ledger is committed; the chat-side fold estate is expected in `gmscs2_gate/estate/` by a successor PR.

## 9. T1 state

Gate list `be921b8c` (36 patterns). Instrument CLEAN (0 collisions); memo CLEAN; checkpoint CLEAN (6 numeric formatting collisions under the contextual rule, 0 hits; the count is recorded in the checkpoint's `t1_scan`); run log CLEAN (2 collisions); the hypothesis-compare script and output CLEAN; the two-leg comparison and the two self-compares CLEAN (collisions only); this return scanned CLEAN before commit (the embedded checkpoint's collisions are logged, not hits). D-MS2-1 reproduced on the dispatch's armor bodies (pattern index [9] on the Phase-0 report's armor); every decoded payload CLEAN.

## 10. A-3 diagnostics (in force)

- **A-3.1 `mixed_r_agg_change_A29`** (S2-E₂, Hill; r(0.25, 0.25) − r(0, 0.25)): cubic_step|001 −9.076178e-7; cubic_step|111 −9.076178e-7; cubic_gem8|001 −1.304158e-6; cubic_gem8|111 −1.304158e-6 (identical for the two descriptor axes, as the F₂ moment of the E₂ fraction does not depend on n_c). The S2-h arm: 0.0 exactly (no descriptor axis).
- **A-3.2 `kappa24_richardson`** (h = 0.02, D(0.02) and D(0.01) in extras): +3.0e-13 / +1.9e-13 / +1.4e-12 / +9.5e-13 (hex) and −7.6e-13 / −2.2e-12 / +1.2e-12 / −3.7e-13 (cubic) — null on every key; the chat leg's diagnostic values are of the same size.
- **A-3.3:** reading (i), CC-DD-1.

## 11. Registers and non-claims (as locked)

Every check and coefficient R1-machine, now two-leg; the verdict class and the constraint-surface reading R2, conditional on E-MS-1(a), the untextured import, K = ∅, the kernel election and A-2.4; the diagonality reading (harmonic orthogonality of the l = 2 weight perturbation and the l = 4 speed perturbation over the fiber direction) R2, now witnessed two-leg by two independent quadratures; the polycrystal postulate R3. No observable, no bridge, no SI value, no value of t₂ or t₄, no evaluation against any bound; no kill claimed or possible here; §2.52 Open 3 untouched.

## 12. Embeds (sentinel format of the dispatch, byte-exact; all `encoding=raw`)

=====BEGIN-EMBED name=g_mscs2_ccleg.py md5=e58ba9a6d52daa23f8264255b6dbbb75 bytes=57297 encoding=raw=====
#!/usr/bin/env python3
"""g_mscs2_ccleg.py -- Gate G-MSCS2, CC leg instrument (blind build).

Built from staging_memo_G_MSCS2_v2.md (efdcabdc), G_MSCS2_LOCK_RECORD.md Addendum A-2
(49232d4c) with Addendum A-3 in force (activation flag "ACTIVATE: G-MSCS2-CC-LEG-1 WITH-A3"),
and g_mscs2_schema_v1_0.json (66f586d7) ONLY, before any quarantined chat artifact was
decoded. The G-MSCS1 instruments on main were read for the inherited descriptor definitions
(memo 2.2-2.4), not copied.

Method variation (lock record section 3; dispatch section 0):
  * SO(3) averages by the FIBER-AXIS ROUTE, not a ZYZ Euler product grid. Every ODF of this
    gate is a function of the fiber axis expressed in the crystal frame, n = g^-1 z. Writing
    g = R_z(psi) g0(n) with g0(n) n = z, the psi-average (the SO(2) coset average about the
    sample fiber axis) is done ANALYTICALLY: for rank-4 tensors it is the orthogonal
    projection onto the five-dimensional transversely-isotropic subspace (Mandel inner
    product); for the per-grain E2 weight it is the closed-form circular moment of a degree-4
    polynomial in the descriptor axis, which leaves a polynomial a0 + a2 x^2 + a4 x^4 in
    x = n_c . n (n_c the descriptor axis in the crystal frame). What remains is an S^2
    integral over n, done with Gauss-Legendre(cos theta) 16 x uniform phi 32 on a generically
    rotated node set (exact for polynomial degree <= 31 in n; the gate needs >= 12). A
    12-point uniform psi average is kept only as a selftest of the analytic projection.
  * The E2 fraction about an axis n is evaluated in the factorized closed form
    frac_E2 = (1 - (k.n)^2) (1 - (e_perp_hat . n)^2), derived from the m = +-2 projection
    formula of memo 2.2 (selftested against that formula).
  * Own HS reference optimizer (boundary-K0 bisection + nested grid refinement over G0),
    own branch labelling, own fits, own checkpoint layout.

Halt discipline: md5 + byte guards on the memo, the lock record, the schema, the T1 list, the
scanner, X-1 and both X-6 files before any computation; T1 self-scan (this file + the memo) at
every invocation with the frozen scanner rule; any hit halts (no override flag exists); any
Phase-0 pin/control failure -> INDETERMINATE by the schema rule (Phase 2 still computed and
written so the failure can be diagnosed, but the verdict says INDETERMINATE).

Addendum A-3 (in force):
  A-3.1 F-CTRL-L2NULL: the pure l = 2 clause covers the three tensors and r_agg; the mixed
        (t2, t4) clause covers the three tensors only; the mixed r_agg change is the reported
        diagnostic mixed_r_agg_change_A29 per cubic key.
  A-3.2 kappa24_richardson per key (h = 0.02, Richardson-extrapolated central cross
        difference) alongside the 7-term quadform.
  A-3.3 CC-DD reading for the cubic (t2, t4) form: (i) the INHERITED DESCRIPTOR-AXIS P2
        (the l = 2 family exactly as A-2.2 defines it, w = 1 + t2 P2(n_c . n)); the
        O_h-symmetrized reading (ii) is reported in extras for the record.
"""
import hashlib
import importlib.util
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ACTIVATION_FLAG = "ACTIVATE: G-MSCS2-CC-LEG-1 WITH-A3"
A3_IN_FORCE = True

GUARDS = {
    "staging_memo_G_MSCS2_v2.md": ("efdcabdcd937cda4acb64f941dc4bb2b", 46053),
    "G_MSCS2_LOCK_RECORD.md": ("49232d4c42061c4536867eba14aae501", 11804),
    "g_mscs2_schema_v1_0.json": ("66f586d7b6c5e8228394222ddfda73f2", 5800),
    "tools/t1/T1_forbidden_G_MSCS2.txt": ("be921b8c29f7578e85ed92f1450c1956", 1695),
    "tools/t1/t1_scan.py": ("6b86290090a8c84f1b1a0a99ec0bf697", 1967),
    "inputs/poly_vrh_results.json": ("200e7a8b775577564369c6924d38a84c", 2767),
    "inputs/g_mscs1_chatleg_checkpoint.json": ("c04c0b8ea34cfe60f231aa06828e6ce4", 33289),
    "inputs/g_mscs1_ccleg_checkpoint.json": ("249e11dd53c4cb82f302b15d3c94c337", 24415),
}
MEMO = "staging_memo_G_MSCS2_v2.md"
T1_LIST = "tools/t1/T1_forbidden_G_MSCS2.txt"
T1_SCANNER = "tools/t1/t1_scan.py"

KEYS = ["hex_step|a", "hex_step|b", "hex_gem8|a", "hex_gem8|b",
        "cubic_step|001", "cubic_step|111", "cubic_gem8|001", "cubic_gem8|111"]
X6_CFG = {"hex_step": "step_hex", "hex_gem8": "gem8_hex",
          "cubic_step": "step_cubic", "cubic_gem8": "gem8_cubic"}
T4_GRID = np.array([-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0])
T2T4_GRID = np.array([-0.25, -0.125, 0.0, 0.125, 0.25])
ZHAT = np.array([0.0, 0.0, 1.0])
XHAT = np.array([1.0, 0.0, 0.0])
YHAT = np.array([0.0, 1.0, 0.0])
N111 = np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0)
SQ2 = math.sqrt(2.0)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_file(p):
    return md5_bytes(open(p, "rb").read())


def halt(msg):
    print("HALT: " + msg)
    sys.exit(1)


# ---------------------------------------------------------------- guards + T1
def guard_files():
    for rel, (want, nbytes) in GUARDS.items():
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            halt(f"guarded file missing: {rel}")
        b = open(p, "rb").read()
        got = md5_bytes(b)
        if got != want or len(b) != nbytes:
            halt(f"guard mismatch on {rel}: md5 {got} bytes {len(b)}")


def t1_load():
    """Load the frozen scanner module (md5-guarded above) and the gate list."""
    spec = importlib.util.spec_from_file_location("t1_scan", os.path.join(HERE, T1_SCANNER))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pats = mod.load(os.path.join(HERE, T1_LIST))
    if len(pats) != 36:
        halt(f"T1 gate list has {len(pats)} patterns, expected 36")
    return mod, pats


def t1_selfscan(mod, pats):
    out = {}
    for label, f in (("instrument", os.path.abspath(__file__)), ("memo", os.path.join(HERE, MEMO))):
        text = open(f, "rb").read().decode("utf-8", "replace")
        hits, coll = mod.scan_text(text, pats)
        if hits:
            halt(f"T1 HIT in {label}: pattern indices {[i for i, _ in hits]}")
        out[label] = "CLEAN"
        out[f"numeric_collisions_{label}"] = len(coll)
    return out


# ---------------------------------------------------------------- Mandel algebra
PAIRS = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
MF = np.array([1.0, 1.0, 1.0, SQ2, SQ2, SQ2])
MFF = np.outer(MF, MF)
_m6 = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
J6 = np.outer(_m6, _m6) / 3.0
KD6 = np.eye(6) - J6
# Mandel basis tensors E_B (symmetric 3x3 with unit Mandel component B)
EB = np.zeros((6, 3, 3))
for _b, (_i, _j) in enumerate(PAIRS):
    EB[_b, _i, _j] = EB[_b, _j, _i] = 1.0 / MF[_b]


def voigt_to_mandel(Cv):
    return np.asarray(Cv, dtype=float) * MFF


def mandel_to_voigt(M):
    return M / MFF


def sym2_to_mandel(S):
    """symmetric 3x3 (..., 3, 3) -> Mandel vector (..., 6)."""
    return np.stack([S[..., i, j] * MF[b] for b, (i, j) in enumerate(PAIRS)], axis=-1)


def mandel_to_full(M):
    Cv = mandel_to_voigt(M)
    C = np.zeros((3, 3, 3, 3))
    for a, (i, j) in enumerate(PAIRS):
        for b, (k, l) in enumerate(PAIRS):
            C[i, j, k, l] = C[j, i, k, l] = C[i, j, l, k] = C[j, i, l, k] = Cv[a, b]
    return C


def full_to_mandel(C):
    M = np.zeros((6, 6))
    for a, (i, j) in enumerate(PAIRS):
        for b, (k, l) in enumerate(PAIRS):
            M[a, b] = MF[a] * MF[b] * C[i, j, k, l]
    return M


def iso_KG(M):
    """Bulk and shear modulus of the isotropic (uniform-SO(3)) projection of M."""
    K = float(M[:3, :3].sum()) / 9.0
    G = (float(np.trace(M)) - 3.0 * K) / 10.0
    return K, G


def iso_M(K, G):
    return 3.0 * K * J6 + 2.0 * G * KD6


def iso_project(M):
    return iso_M(*iso_KG(M))


def hex_voigt(C11, C12, C13, C33, C44, C66):
    Cv = np.zeros((6, 6))
    Cv[0, 0] = Cv[1, 1] = C11
    Cv[2, 2] = C33
    Cv[0, 1] = Cv[1, 0] = C12
    Cv[0, 2] = Cv[2, 0] = Cv[1, 2] = Cv[2, 1] = C13
    Cv[3, 3] = Cv[4, 4] = C44
    Cv[5, 5] = C66
    return Cv


def cubic_voigt(C11, C12, C44):
    Cv = np.zeros((6, 6))
    for i in range(3):
        Cv[i, i] = C11
        for j in range(3):
            if i != j:
                Cv[i, j] = C12
    Cv[3, 3] = Cv[4, 4] = Cv[5, 5] = C44
    return Cv


def mandel_rotation(g):
    """6x6 orthogonal Mandel rotation matrices for a batch of 3x3 rotations g (..., 3, 3):
    column B = Mandel vector of g E_B g^T."""
    rotE = np.einsum("...ik,bkl,...jl->...bij", g, EB, g)
    Q = sym2_to_mandel(rotE)           # (..., 6 [B], 6 [A])
    return np.swapaxes(Q, -1, -2)      # (..., A, B)


def rotate_mandel(M, g):
    Q = mandel_rotation(g)
    return np.einsum("...ab,bc,...dc->...ad", Q, M, Q)


def rot_z(psi):
    c, s = math.cos(psi), math.sin(psi)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def rot_axis_angle(axis, ang):
    a = np.asarray(axis, dtype=float)
    a = a / np.linalg.norm(a)
    Kx = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * Kx + (1.0 - math.cos(ang)) * (Kx @ Kx)


def g0_to_z(n):
    """A rotation taking the unit vector n to z (any representative of the coset)."""
    nz = float(np.clip(n[2], -1.0, 1.0))
    axis = np.cross(n, ZHAT)
    s = np.linalg.norm(axis)
    if s < 1e-14:
        return np.eye(3) if nz > 0 else rot_axis_angle(XHAT, math.pi)
    return rot_axis_angle(axis / s, math.acos(nz))


# ---------------------------------------------------------------- TI projector (analytic SO(2) average)
def ti_projector():
    """Orthogonal projector (36x36, Mandel-flattened) onto the transversely-isotropic
    (about z) subspace = the SO(2)_z-fixed subspace of elasticity tensors."""
    basis = []
    for p in range(5):
        c = np.zeros(5)
        c[p] = 1.0
        C11, C12, C13, C33, C44 = c
        basis.append(voigt_to_mandel(hex_voigt(C11, C12, C13, C33, C44, 0.5 * (C11 - C12))).ravel())
    B = np.array(basis).T                       # (36, 5)
    Qb, _ = np.linalg.qr(B)
    return Qb @ Qb.T


TI_P = ti_projector()


def ti_average(Mrot):
    """Analytic SO(2)_z coset average of a batch of Mandel tensors (..., 6, 6)."""
    shp = Mrot.shape
    flat = Mrot.reshape(-1, 36) @ TI_P.T
    return flat.reshape(shp)


# ---------------------------------------------------------------- S^2 rules
def sphere_gl_uniform(n_theta, n_phi, rotation=None):
    """GL(cos theta) x uniform phi rule; weights sum to 1; optional rigid rotation of nodes."""
    x, w = np.polynomial.legendre.leggauss(n_theta)
    phi = 2.0 * np.pi * np.arange(n_phi) / n_phi
    ct = np.repeat(x, n_phi)
    st = np.sqrt(1.0 - ct * ct)
    ph = np.tile(phi, n_theta)
    pts = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=1)
    wts = np.repeat(w, n_phi) / (2.0 * n_phi)
    if rotation is not None:
        pts = pts @ rotation.T
    return pts, wts


# the fiber-axis (n) rule: generic rotation so that no node sits on a crystal symmetry axis
GEN_ROT = rot_axis_angle([0.3, -0.7, 0.55], 1.234567) @ rot_axis_angle([1.0, 0.2, -0.1], 0.789)
NFIB, WFIB = sphere_gl_uniform(16, 32, GEN_ROT)          # 512 nodes, exact to degree 31


# ---------------------------------------------------------------- ODF weight functions on n
def P2(x):
    return 1.5 * x * x - 0.5


def P4(x):
    return (35.0 * x ** 4 - 30.0 * x * x + 3.0) / 8.0


def P6(x):
    return (231.0 * x ** 6 - 315.0 * x ** 4 + 105.0 * x * x - 5.0) / 16.0


def K4_cubic(n):
    return 2.5 * (np.sum(n ** 4, axis=-1) - 0.6)


def K6_cubic_raw(n):
    return np.sum(n ** 6, axis=-1) - (15.0 / 11.0) * np.sum(n ** 4, axis=-1) + 30.0 / 77.0


_fine, _ = sphere_gl_uniform(200, 400)
K6_SCALE = float(np.max(np.abs(K6_cubic_raw(_fine))))
del _fine


def K6_cubic(n):
    return K6_cubic_raw(n) / K6_SCALE


class Config:
    """One configuration/arm key: symmetry, crystal tensor, descriptor axis, ODF family."""

    def __init__(self, key, sym, M, n_c):
        self.key, self.sym, self.M, self.n_c = key, sym, M, n_c
        self.x = NFIB @ n_c                       # n_c . n at the fiber nodes
        if sym == "hex":
            self.f2 = P2(NFIB[:, 2])
            self.f4 = P4(NFIB[:, 2])
            self.f6 = P6(NFIB[:, 2])
            self.c4 = 1.0
            self.c6 = 1.0
        else:
            self.f2 = P2(self.x)                  # inherited descriptor-axis l = 2 family (reading (i))
            self.f4 = K4_cubic(NFIB)
            self.f6 = K6_cubic(NFIB)
            self.c4 = float(K4_cubic(n_c[None, :])[0])
            self.c6 = float(K6_cubic(n_c[None, :])[0])
        self.c2 = 1.0                             # P2(n_c . n_c) = 1 on every key

    def odf(self, t2=0.0, t4=0.0, t6=0.0):
        return 1.0 + t2 * self.f2 + t4 * self.f4 + t6 * self.f6


# ---------------------------------------------------------------- fiber tables + ODF averages
G0_TAB = np.array([g0_to_z(n) for n in NFIB])           # (512, 3, 3)
Q0_TAB = mandel_rotation(G0_TAB)                        # (512, 6, 6)


def fiber_table(M):
    """T(n) = analytic psi-average of (R_z(psi) g0(n)) . M, for every fiber node n."""
    Mrot = np.einsum("nab,bc,ndc->nad", Q0_TAB, M, Q0_TAB)
    return ti_average(Mrot)


def odf_average(table, wvals):
    return np.einsum("n,nab->ab", WFIB * wvals, table)


# ---------------------------------------------------------------- k-sphere modes
def christoffel_modes(M, K):
    """Christoffel eigenmodes on directions K (Nk,3). Returns flattened per-mode arrays
    (Nk*3): v, lam, wEM, ehat (unit transverse polarization), plus per-direction (Nk,3) v."""
    C = mandel_to_full(M)
    G = np.einsum("ijkl,nj,nl->nik", C, K, K, optimize=True)
    G = 0.5 * (G + np.swapaxes(G, 1, 2))
    ev, evec = np.linalg.eigh(G)
    v = np.sqrt(np.maximum(ev, 0.0))                        # (Nk, 3) ascending
    E = np.swapaxes(evec, 1, 2)                              # (Nk, branch, comp)
    ke = np.einsum("ni,nbi->nb", K, E)
    lam = ke * ke
    eperp = E - ke[:, :, None] * K[:, None, :]
    wEM = np.einsum("nbi,nbi->nb", eperp, eperp)
    nrm = np.sqrt(np.maximum(wEM, 0.0))
    ehat = np.zeros_like(eperp)
    ok = nrm > 1e-13
    ehat[ok] = eperp[ok] / nrm[ok][:, None]
    return {"v": v, "lam": lam, "wEM": wEM, "ehat": ehat, "K": K, "E": E}


def frac_E2_fixed_axis(modes, axis):
    A = modes["K"] @ axis            # (Nk,)
    B = modes["ehat"] @ axis         # (Nk, 3)
    return (1.0 - A[:, None] ** 2) * (1.0 - B ** 2)


NHAT, WNHAT = sphere_gl_uniform(12, 24)                  # pinned descriptor-axis rule (A-2.5)
PL_NHAT = {0: np.ones(len(NHAT)), 2: P2(NHAT[:, 2]), 4: P4(NHAT[:, 2]), 6: P6(NHAT[:, 2])}


def e2_marginal_moments(modes):
    """F_l per mode (Nk, 3) for l = 0, 2, 4, 6: the P_l-weighted S^2 average over the
    descriptor axis of frac_E2, with the pinned GL 12 x 24 rule."""
    A = modes["K"] @ NHAT.T                                          # (Nk, Nn)
    B = np.einsum("nbi,mi->nbm", modes["ehat"], NHAT, optimize=True)  # (Nk, 3, Nn)
    frac = (1.0 - A[:, None, :] ** 2) * (1.0 - B ** 2)
    out = {}
    for l, pl in PL_NHAT.items():
        out[l] = frac @ (WNHAT * pl)
    return out


def e2_psi_coefficients(modes):
    """Closed-form SO(2) (psi) average of frac_E2 about a descriptor axis rotating on the cone
    of fixed z-component x: fbar = a0 + a2 x^2 + a4 x^4, per mode (Nk, 3)."""
    kz = modes["K"][:, 2][:, None] * np.ones_like(modes["lam"])
    ez = modes["ehat"][:, :, 2]
    kz2, ez2 = kz * kz, ez * ez
    A = (1.0 - kz2) * (1.0 - ez2) + 2.0 * kz2 * ez2
    B = kz2 + ez2 - 6.0 * kz2 * ez2
    a0 = 0.5 * kz2 + 0.5 * ez2 + A / 8.0
    a2 = 1.0 - 1.5 * (kz2 + ez2) - A / 4.0 + B / 2.0
    a4 = A / 8.0 - B / 2.0 + kz2 * ez2
    valid = modes["wEM"] > 1e-13
    a0[~valid] = a2[~valid] = a4[~valid] = 0.0
    return a0, a2, a4


def e2_direct_average(modes, cfg, wvals):
    """SO(3)-direct ODF average of the per-grain E2 weight (descriptor axis carried along),
    by the fiber-axis route: sum_n w(n) [a0 + a2 (n_c.n)^2 + a4 (n_c.n)^4]."""
    a0, a2, a4 = e2_psi_coefficients(modes)
    W0 = float(np.sum(WFIB * wvals))
    W2 = float(np.sum(WFIB * wvals * cfg.x ** 2))
    W4 = float(np.sum(WFIB * wvals * cfg.x ** 4))
    return a0 * W0 + a2 * W2 + a4 * W4


def descriptor_speeds(modes, wq, fbar):
    """<v>_EM, <v>_S2E2, <v>_S2h and the QT lambda statistics for one aggregate."""
    v, lam, wEM = modes["v"], modes["lam"], modes["wEM"]
    W = wq[:, None]
    wS2 = fbar * wEM
    wh = (1.0 - lam) / (1.0 + lam / 3.0)
    vEM = float(np.sum(W * wEM * v)) / float(np.sum(W * wEM))
    vS2 = float(np.sum(W * wS2 * v)) / float(np.sum(W * wS2))
    vh = float(np.sum(W * wh * v)) / float(np.sum(W * wh))
    qL = np.argmax(lam, axis=1)
    idx = np.arange(lam.shape[0])
    lam_qt = lam.copy()
    lam_qt[idx, qL] = np.nan
    lam_mean = float(np.nansum(W * lam_qt) / 2.0)
    lam_max = float(np.nanmax(lam_qt))
    return {"v_EM": vEM, "v_S2E2": vS2, "v_S2h": vh,
            "r_E2": vS2 / vEM - 1.0, "r_h": vh / vEM - 1.0,
            "lambda_mean": lam_mean, "lambda_max": lam_max}


# ---------------------------------------------------------------- HS bounds (Walpole form)
def cstar_iso(K0, G0):
    Ks = 4.0 * G0 / 3.0
    Gs = G0 * (9.0 * K0 + 8.0 * G0) / (6.0 * (K0 + 2.0 * G0))
    return iso_M(Ks, Gs)


def hs_from_P(P, Cs):
    return np.linalg.inv(P) - Cs


def G_hs_t0(M, K0, G0):
    Cs = cstar_iso(K0, G0)
    T = np.linalg.inv(M + Cs)
    return iso_KG(hs_from_P(iso_project(T), Cs))[1]


def hs_reference(M, side):
    """Isotropic reference (K0, G0) at t = 0: side 'hi' = minimal feasible majorant
    (C0 >= C_g) minimizing G_HS; side 'lo' = maximal feasible minorant maximizing G_HS."""
    K_g, G_g = iso_KG(M)
    scale = float(np.linalg.norm(M))
    sgn = 1.0 if side == "hi" else -1.0

    def feasible(K0, G0):
        return float(np.linalg.eigvalsh(sgn * (iso_M(K0, G0) - M))[0]) >= -1e-11 * scale

    def K0_boundary(G0):
        lo, hi = 1e-6 * K_g, 200.0 * K_g
        if side == "hi":
            if not feasible(hi, G0):
                return None
            if feasible(lo, G0):
                return lo
            for _ in range(200):          # smallest feasible K0
                mid = 0.5 * (lo + hi)
                if feasible(mid, G0):
                    hi = mid
                else:
                    lo = mid
            return hi
        if not feasible(lo, G0):
            return None
        if feasible(hi, G0):
            return hi
        for _ in range(200):              # largest feasible K0
            mid = 0.5 * (lo + hi)
            if feasible(mid, G0):
                lo = mid
            else:
                hi = mid
        return lo

    def objective(G0):
        K0 = K0_boundary(G0)
        if K0 is None:
            return math.inf, None
        g = G_hs_t0(M, K0, G0)
        return (g if side == "hi" else -g), K0

    grid = np.linspace(0.01 * G_g, 10.0 * G_g, 600)
    vals = np.array([objective(G0)[0] for G0 in grid])
    i = int(np.argmin(vals))
    centre, half = grid[i], grid[1] - grid[0]
    for _ in range(9):                    # nested refinement, 21 points per level
        g_grid = np.linspace(centre - half, centre + half, 21)
        v_grid = np.array([objective(G0)[0] for G0 in g_grid])
        centre = g_grid[int(np.argmin(v_grid))]
        half = g_grid[1] - g_grid[0]
    G0 = float(centre)
    _, K0 = objective(G0)
    return float(K0), G0, G_hs_t0(M, K0, G0)


# ---------------------------------------------------------------- fits
def fit_cubic_through_origin(t, r, window, inclusive=True):
    sel = (np.abs(t) <= window + 1e-12) if inclusive else (np.abs(t) < window - 1e-12)
    tt, rr = t[sel], r[sel]
    A = np.stack([tt, tt ** 2, tt ** 3], axis=1)
    c, *_ = np.linalg.lstsq(A, rr, rcond=None)
    return [float(x) for x in c], float(np.max(np.abs(A @ c - rr))), int(sel.sum())


def fit_quadform(t2, t4, r):
    A = np.stack([t2 ** 2, t2 * t4, t4 ** 2, t2 ** 3, t2 ** 2 * t4, t2 * t4 ** 2, t4 ** 3], axis=1)
    c, *_ = np.linalg.lstsq(A, r, rcond=None)
    return {"kappa22": float(c[0]), "kappa24": float(c[1]), "kappa44": float(c[2]),
            "residual": float(np.max(np.abs(A @ c - r))),
            "x_cubic_terms_discarded": [float(x) for x in c[3:]]}


# ---------------------------------------------------------------- selftests of the machinery
def selftests():
    rng = np.random.default_rng(2026)
    rep = {}
    # 1. Mandel rotation: orthogonality + agreement with the full-tensor rotation
    g = rot_axis_angle(rng.normal(size=3), 1.1)
    Q = mandel_rotation(g)
    A = rng.normal(size=(6, 6))
    M = A + A.T
    C4 = mandel_to_full(M)
    C4r = np.einsum("ia,jb,kc,ld,abcd->ijkl", g, g, g, g, C4)
    rep["mandel_rotation_dev"] = float(max(np.max(np.abs(Q @ Q.T - np.eye(6))),
                                           np.max(np.abs(rotate_mandel(M, g) - full_to_mandel(C4r)))))
    # 2. TI projector == 12-point uniform psi average, on random M
    psis = 2.0 * np.pi * np.arange(12) / 12.0
    avg = np.mean([rotate_mandel(M, rot_z(p)) for p in psis], axis=0)
    rep["ti_projector_vs_psi_average_dev"] = float(np.max(np.abs(ti_average(M[None])[0] - avg)))
    # 3. fiber rule: uniform average == closed-form isotropic projection
    tab = fiber_table(M)
    rep["fiber_rule_iso_dev"] = float(np.max(np.abs(odf_average(tab, np.ones(len(WFIB))) - iso_project(M))))
    # 4. harmonic normalizations on the fiber rule
    k4, p4, k6, p2 = K4_cubic(NFIB), P4(NFIB[:, 2]), K6_cubic(NFIB), P2(NFIB[:, 2])
    rep["K4_mean"] = float(np.sum(WFIB * k4))
    rep["K4_sq_mean_minus_4_21"] = float(np.sum(WFIB * k4 * k4) - 4.0 / 21.0)
    rep["P4_sq_mean_minus_1_9"] = float(np.sum(WFIB * p4 * p4) - 1.0 / 9.0)
    rep["K6_mean"] = float(np.sum(WFIB * k6))
    rep["K6_K4_overlap"] = float(np.sum(WFIB * k6 * k4))
    rep["P2_mean"] = float(np.sum(WFIB * p2))
    rep["K4_range"] = [float(k4.min()), float(k4.max())]
    # 5. frac_E2 closed form vs the m = +-2 projection formula of memo 2.2
    worst = 0.0
    for _ in range(200):
        k = rng.normal(size=3)
        k /= np.linalg.norm(k)
        e = rng.normal(size=3)
        e -= (e @ k) * k
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)
        S = 0.5 * (np.outer(k, e) + np.outer(e, k))
        s2 = float(np.sum(S * S))
        ref = 1.0 - 2.0 * float((S @ n) @ (S @ n)) / s2 + 0.5 * float(n @ S @ n) ** 2 / s2
        eh = e / np.linalg.norm(e)
        mine = (1.0 - float(k @ n) ** 2) * (1.0 - float(eh @ n) ** 2)
        worst = max(worst, abs(ref - mine))
    rep["fracE2_closed_form_dev"] = worst
    # 6. analytic psi moments of frac_E2 vs brute force (12-point psi) on random modes/cones
    worst = 0.0
    for _ in range(50):
        k = rng.normal(size=3)
        k /= np.linalg.norm(k)
        e = rng.normal(size=3)
        e -= (e @ k) * k
        eh = e / np.linalg.norm(e)
        x = rng.uniform(-1, 1)
        rho = math.sqrt(1 - x * x)
        m = {"K": k[None, :], "ehat": eh[None, None, :], "lam": np.zeros((1, 1)), "wEM": np.ones((1, 1))}
        a0, a2, a4 = e2_psi_coefficients(m)
        ana = float(a0[0, 0] + a2[0, 0] * x * x + a4[0, 0] * x ** 4)
        brute = np.mean([(1 - (k @ np.array([rho * math.cos(p), rho * math.sin(p), x])) ** 2)
                         * (1 - (eh @ np.array([rho * math.cos(p), rho * math.sin(p), x])) ** 2)
                         for p in psis])
        worst = max(worst, abs(ana - brute))
        worst = max(worst, abs(float(a0[0, 0] + a2[0, 0] / 3.0 + a4[0, 0] / 5.0) - 0.4))
    rep["psi_moment_closed_form_dev"] = worst
    # 7. the l = 4 harmonic tensor of z: Voigt entries of (1/3) T4(z) against the A-2.2 table
    T4 = harmonic_l4_tensor(ZHAT)
    Tv = mandel_to_voigt(full_to_mandel(T4)) / 3.0
    table = {(0, 0): 3, (1, 1): 3, (2, 2): 8, (0, 1): 1, (0, 2): -4, (1, 2): -4, (3, 3): -4, (4, 4): -4, (5, 5): 1}
    dev = 0.0
    for (a, b), val in table.items():
        dev = max(dev, abs(Tv[a, b] - val / 105.0), abs(Tv[b, a] - val / 105.0))
    for a in range(6):
        for b in range(6):
            if (a, b) not in table and (b, a) not in table:
                dev = max(dev, abs(Tv[a, b]))
    rep["T4_voigt_table_dev"] = float(dev)
    return rep


def harmonic_l4_tensor(n):
    """The l = 4 (traceless, fully symmetric) part of n x n x n x n."""
    d = np.eye(3)
    nn = np.outer(n, n)
    T = np.einsum("i,j,k,l->ijkl", n, n, n, n)
    T -= (np.einsum("ij,kl->ijkl", d, nn) + np.einsum("ik,jl->ijkl", d, nn) + np.einsum("il,jk->ijkl", d, nn)
          + np.einsum("jk,il->ijkl", d, nn) + np.einsum("jl,ik->ijkl", d, nn) + np.einsum("kl,ij->ijkl", d, nn)) / 7.0
    T += (np.einsum("ij,kl->ijkl", d, d) + np.einsum("ik,jl->ijkl", d, d) + np.einsum("il,jk->ijkl", d, d)) / 35.0
    return T


# ---------------------------------------------------------------- aggregate machinery per key
class Aggregate:
    """Textured Voigt / Reuss / Hill / HS tensors of one configuration via the fiber tables."""

    def __init__(self, cfg, hs_lo, hs_hi):
        self.cfg = cfg
        self.tabC = fiber_table(cfg.M)
        self.tabS = fiber_table(np.linalg.inv(cfg.M))
        self.hs = {}
        for side, (K0, G0, _) in (("lo", hs_lo), ("hi", hs_hi)):
            Cs = cstar_iso(K0, G0)
            self.hs[side] = (fiber_table(np.linalg.inv(cfg.M + Cs)), Cs)

    def tensors(self, wvals):
        V = odf_average(self.tabC, wvals)
        Sbar = odf_average(self.tabS, wvals)
        R = np.linalg.inv(Sbar)
        hs = {side: hs_from_P(odf_average(tab, wvals), Cs) for side, (tab, Cs) in self.hs.items()}
        return {"V": V, "Sbar": Sbar, "R": R, "Hill": 0.5 * (V + R),
                "HS_lo": hs["lo"], "HS_hi": hs["hi"], "HS": 0.5 * (hs["lo"] + hs["hi"])}


def r_on_tensor(M_agg, cfg, kq, wq, t2, t4, t6=0.0, want_modes=False):
    """Descriptor speeds on one aggregate tensor with the E2 weight marginal
    F0 + c2 t2 F2 + c4 t4 F4 + c6 t6 F6 (A-2.5)."""
    modes = christoffel_modes(M_agg, kq)
    F = e2_marginal_moments(modes)
    fbar = F[0] + cfg.c2 * t2 * F[2] + cfg.c4 * t4 * F[4] + cfg.c6 * t6 * F[6]
    out = descriptor_speeds(modes, wq, fbar)
    if want_modes:
        out["_modes"], out["_F"], out["_fbar"] = modes, F, fbar
    return out


def transverse_pair_along_x(M_agg):
    """qSH (e || y) and qSV (e || z) speeds for propagation along x (k perpendicular to the
    fiber axis), labelled by polarization."""
    modes = christoffel_modes(M_agg, XHAT[None, :])
    E, v = modes["E"][0], modes["v"][0]
    bSH = int(np.argmax(np.abs(E @ YHAT)))
    bSV = int(np.argmax(np.abs(E @ ZHAT)))
    if bSH == bSV:
        halt("transverse labelling along x degenerate")
    return float(v[bSH]), float(v[bSV]), float(abs(E[bSH] @ YHAT)), float(abs(E[bSV] @ ZHAT))


def rel_dev(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def tensor_rel_change(A, B):
    return float(np.max(np.abs(A - B)) / np.max(np.abs(B)))


# ---------------------------------------------------------------- main
def main():
    t_start = time.time()
    guard_files()
    t1mod, t1pats = t1_load()
    t1_state = t1_selfscan(t1mod, t1pats)
    schema = json.load(open(os.path.join(HERE, "g_mscs2_schema_v1_0.json"), encoding="utf-8"))
    tau = schema["tolerances"]["tau_agg"]
    kfloor = schema["tolerances"]["kappa_floor"]
    assert list(T4_GRID) == schema["t4_grid"] and list(T2T4_GRID) == schema["t2t4_grid"]
    assert KEYS == schema["keys"]
    print(f"activation: {ACTIVATION_FLAG}   (Addendum A-3 in force: {A3_IN_FORCE})")
    print(f"T1: instrument {t1_state['instrument']} memo {t1_state['memo']}")

    X1 = json.load(open(os.path.join(HERE, "inputs/poly_vrh_results.json"), encoding="utf-8"))
    X6c = json.load(open(os.path.join(HERE, "inputs/g_mscs1_chatleg_checkpoint.json"), encoding="utf-8"))
    X6cc = json.load(open(os.path.join(HERE, "inputs/g_mscs1_ccleg_checkpoint.json"), encoding="utf-8"))
    vrh = X1["vrh"]

    def hexM(tag, arm):
        c = vrh[tag]["C_over_rho"]
        C66 = c["C66"] if arm == "a" else 0.5 * (c["C11"] - c["C12"])
        return voigt_to_mandel(hex_voigt(c["C11"], c["C12"], c["C13"], c["C33"], c["C44"], C66))

    def cubM(tag):
        c = vrh[tag]["C_over_rho"]
        return voigt_to_mandel(cubic_voigt(c["C11"], c["C12"], c["C44"]))

    CFG = {
        "hex_step|a": Config("hex_step|a", "hex", hexM("hex:step", "a"), ZHAT),
        "hex_step|b": Config("hex_step|b", "hex", hexM("hex:step", "b"), ZHAT),
        "hex_gem8|a": Config("hex_gem8|a", "hex", hexM("hex:gem8", "a"), ZHAT),
        "hex_gem8|b": Config("hex_gem8|b", "hex", hexM("hex:gem8", "b"), ZHAT),
        "cubic_step|001": Config("cubic_step|001", "cubic", cubM("cubic:step"), ZHAT),
        "cubic_step|111": Config("cubic_step|111", "cubic", cubM("cubic:step"), N111),
        "cubic_gem8|001": Config("cubic_gem8|001", "cubic", cubM("cubic:gem8"), ZHAT),
        "cubic_gem8|111": Config("cubic_gem8|111", "cubic", cubM("cubic:gem8"), N111),
    }

    print("== selftests ==")
    st = selftests()
    for k, v in st.items():
        print(f"   {k}: {v}")
    for k in ("mandel_rotation_dev", "ti_projector_vs_psi_average_dev", "fracE2_closed_form_dev",
              "psi_moment_closed_form_dev", "T4_voigt_table_dev", "K4_mean", "K4_sq_mean_minus_4_21",
              "P4_sq_mean_minus_1_9", "K6_mean", "K6_K4_overlap", "P2_mean"):
        if abs(st[k]) > 1e-12:
            halt(f"selftest {k} = {st[k]}")
    if st["fiber_rule_iso_dev"] > 1e-12 * 10:
        halt("fiber rule iso dev")
    print(f"   marginal coefficients c4: 001 -> {CFG['cubic_step|001'].c4}, 111 -> {CFG['cubic_step|111'].c4}"
          f"   (c6: {CFG['cubic_step|001'].c6}, {CFG['cubic_step|111'].c6}; K6 scale {K6_SCALE})")
    if abs(CFG["cubic_step|001"].c4 - 1.0) > 1e-14 or abs(CFG["cubic_step|111"].c4 + 2.0 / 3.0) > 1e-14:
        halt("marginal c coefficients differ from A-2.5")

    kq, wq = sphere_gl_uniform(64, 128)
    kq2, wq2 = sphere_gl_uniform(128, 256)

    # ================================================================ Phase 1 (PIN-XTAL inputs)
    print("== Phase 1 (single crystal; PIN-XTAL inputs) ==")
    phase1 = {}
    for key, cfg in CFG.items():
        modes = christoffel_modes(cfg.M, kq)
        fr = frac_E2_fixed_axis(modes, cfg.n_c)
        d = descriptor_speeds(modes, wq, fr)
        phase1[key] = {k: d[k] for k in ("v_EM", "v_S2E2", "v_S2h", "r_E2", "r_h", "lambda_mean", "lambda_max")}
        phase1[key]["r_xtal_E2"] = phase1[key].pop("r_E2")
        phase1[key]["r_xtal_h"] = phase1[key].pop("r_h")
        print(f"   {key}: r_E2 {phase1[key]['r_xtal_E2']:+.6e} r_h {phase1[key]['r_xtal_h']:+.6e} "
              f"lam_mean {phase1[key]['lambda_mean']:.4e} lam_max {phase1[key]['lambda_max']:.4e}")

    def pin_worst(fields, mine, theirs):
        w = 0.0
        for f in fields:
            if f in theirs and theirs[f] is not None:
                w = max(w, rel_dev(mine[f], theirs[f]))
        return w

    pin_xtal = {"worst_rel": 0.0, "worst_rel_vs_cc": 0.0, "by_key": {}}
    for key in KEYS:
        a = pin_worst(("r_xtal_E2", "r_xtal_h", "lambda_mean", "lambda_max"), phase1[key], X6c["phase1"][key])
        b = pin_worst(("r_xtal_E2", "r_xtal_h", "lambda_mean", "lambda_max"), phase1[key], X6cc["phase1"][key])
        pin_xtal["by_key"][key] = a
        pin_xtal["worst_rel"] = max(pin_xtal["worst_rel"], a)
        pin_xtal["worst_rel_vs_cc"] = max(pin_xtal["worst_rel_vs_cc"], b)
    pin_xtal["passed"] = bool(pin_xtal["worst_rel"] <= 1e-8)
    print(f"   PIN-XTAL worst rel {pin_xtal['worst_rel']:.3e} (vs cc {pin_xtal['worst_rel_vs_cc']:.3e})")

    # ================================================================ HS references + t = 0 pins
    print("== HS references (optimized at t = 0, reused at every texture) ==")
    hs_ref = {}
    for key, cfg in CFG.items():
        base = key.split("|")[0]
        cache = base if cfg.sym == "cubic" or key.endswith("|a") else key
        if cache not in hs_ref:
            lo = hs_reference(cfg.M, "lo")
            hi = hs_reference(cfg.M, "hi")
            hs_ref[cache] = {"lo": lo, "hi": hi}
            print(f"   {cache}: lo (K0,G0)=({lo[0]:.6f},{lo[1]:.6f}) G_HS {lo[2]:.10f} | "
                  f"hi ({hi[0]:.6f},{hi[1]:.6f}) G_HS {hi[2]:.10f}")

    AGG = {}
    for key, cfg in CFG.items():
        base = key.split("|")[0]
        cache = base if cfg.sym == "cubic" or key.endswith("|a") else key
        AGG[key] = Aggregate(cfg, hs_ref[cache]["lo"], hs_ref[cache]["hi"])

    phase2 = {k: {} for k in KEYS}
    pin_vrh0 = {"worst_rel": 0.0, "worst_rel_vs_cc": 0.0}
    pin_hs0 = {"worst_rel": 0.0, "worst_rel_vs_cc": 0.0, "G_HS": {}}
    for key, cfg in CFG.items():
        T0 = AGG[key].tensors(cfg.odf())
        KV, GV = iso_KG(T0["V"])
        KR, GR = iso_KG(T0["R"])
        G_lo, G_hi = iso_KG(T0["HS_lo"])[1], iso_KG(T0["HS_hi"])[1]
        p = phase2[key]
        p["vT_V"], p["vT_R"], p["vT_VRH"] = math.sqrt(GV), math.sqrt(GR), math.sqrt(0.5 * (GV + GR))
        p["vT_HS_lo"], p["vT_HS_hi"] = math.sqrt(G_lo), math.sqrt(G_hi)
        p["x_KV_GV_KR_GR"] = [KV, GV, KR, GR]
        for src, acc in ((X6c, "worst_rel"), (X6cc, "worst_rel_vs_cc")):
            pin_vrh0[acc] = max(pin_vrh0[acc], pin_worst(("vT_VRH", "vT_V", "vT_R"), p, src["phase2"][key]))
            pin_hs0[acc] = max(pin_hs0[acc], pin_worst(("vT_HS_lo", "vT_HS_hi"), p, src["phase2"][key]))
        cfgx = X6_CFG[key.split("|")[0]]
        if cfgx in X6c.get("pins_vrh0", {}):
            ghs = X6c["pins_vrh0"][cfgx]["G_HS"]
            pin_hs0["worst_rel"] = max(pin_hs0["worst_rel"], rel_dev(G_lo, ghs[0]), rel_dev(G_hi, ghs[1]))
        pin_hs0["G_HS"][key] = [G_lo, G_hi]
    pin_vrh0["passed"] = bool(pin_vrh0["worst_rel"] <= 1e-8)
    pin_hs0["passed"] = bool(pin_hs0["worst_rel"] <= 1e-6)
    print(f"   PIN-VRH0 worst rel {pin_vrh0['worst_rel']:.3e} (vs cc {pin_vrh0['worst_rel_vs_cc']:.3e})")
    print(f"   PIN-HS0 worst rel {pin_hs0['worst_rel']:.3e} (vs cc {pin_hs0['worst_rel_vs_cc']:.3e})")

    # ================================================================ PIN-K2 (l = 2 family, t4 = 0)
    print("== PIN-K2 (the inherited l = 2 family, G-MSCS1 grid and window) ==")
    pin_k2 = {"worst_rel_hex_kappa2": 0.0, "worst_abs_cubic_kappa2": 0.0, "by_key": {}}
    so3_dev_all, so3_mean_t0 = 0.0, []
    for key, cfg in CFG.items():
        r2 = []
        for t in T4_GRID:
            T = AGG[key].tensors(cfg.odf(t2=t))
            d = r_on_tensor(T["Hill"], cfg, kq, wq, t2=t, t4=0.0, want_modes=(t == 0.0))
            r2.append(d["r_E2"])
            if t == 0.0:
                F0 = d["_F"][0]
                valid = d["_modes"]["wEM"] > 1e-6
                so3_dev_all = max(so3_dev_all, float(np.max(np.abs(F0[valid] - 0.4))))
                so3_mean_t0.append(float(np.mean(F0[valid])))
        (S2, k2, k3), resid, npts = fit_cubic_through_origin(T4_GRID, np.array(r2), 0.25)
        phase2[key]["kappa2_E2"] = k2
        phase2[key]["x_l2_family"] = {"S2_E2": S2, "kappa3_E2": k3, "fit_residual": resid, "r_agg_E2_VRH_l2": r2, "n_fit_points": npts}
        ref = X6c["phase2"][key]["kappa2_E2"]
        if cfg.sym == "hex":
            dev = rel_dev(k2, ref)
            pin_k2["worst_rel_hex_kappa2"] = max(pin_k2["worst_rel_hex_kappa2"], dev)
        else:
            dev = abs(k2)
            pin_k2["worst_abs_cubic_kappa2"] = max(pin_k2["worst_abs_cubic_kappa2"], dev)
        pin_k2["by_key"][key] = {"kappa2_E2": k2, "x6_chat": ref, "x6_cc": X6cc["phase2"][key]["kappa2_E2"], "dev": dev}
        print(f"   {key}: kappa2_E2 {k2:+.9e}  (X-6 chat {ref:+.9e})  dev {dev:.3e}")
    pin_k2["passed"] = bool(pin_k2["worst_rel_hex_kappa2"] <= 1e-4 and pin_k2["worst_abs_cubic_kappa2"] <= 1e-12)

    # ================================================================ Phase 2 (l = 4 families)
    print("== Phase 2 (l = 4 families; VRH and HS at every t4) ==")
    doubling = 0.0
    biref_identity = {}
    for key, cfg in CFG.items():
        p = phase2[key]
        arrays = {k: [] for k in ("r_agg_E2_VRH", "r_agg_h_VRH", "r_agg_E2_HS", "r_agg_E2_V", "r_agg_E2_R", "lambda_mean_t4",
                                  "x_vqSH_t4", "x_vqSV_t4", "x_r_agg_h_HS")}
        for t in T4_GRID:
            T = AGG[key].tensors(cfg.odf(t4=t))
            dH = r_on_tensor(T["Hill"], cfg, kq, wq, 0.0, t)
            dHS = r_on_tensor(T["HS"], cfg, kq, wq, 0.0, t)
            dV = r_on_tensor(T["V"], cfg, kq, wq, 0.0, t)
            dR = r_on_tensor(T["R"], cfg, kq, wq, 0.0, t)
            arrays["r_agg_E2_VRH"].append(dH["r_E2"])
            arrays["r_agg_h_VRH"].append(dH["r_h"])
            arrays["lambda_mean_t4"].append(dH["lambda_mean"])
            arrays["r_agg_E2_HS"].append(dHS["r_E2"])
            arrays["x_r_agg_h_HS"].append(dHS["r_h"])
            arrays["r_agg_E2_V"].append(dV["r_E2"])
            arrays["r_agg_E2_R"].append(dR["r_E2"])
            vsh, vsv, _, _ = transverse_pair_along_x(T["Hill"])
            arrays["x_vqSH_t4"].append(vsh)
            arrays["x_vqSV_t4"].append(vsv)
            if t == 0.25:
                d2 = r_on_tensor(T["Hill"], cfg, kq2, wq2, 0.0, t)
                doubling = max(doubling, abs(d2["r_E2"] - dH["r_E2"]))
        p.update(arrays)
        rE = np.array(arrays["r_agg_E2_VRH"])
        (S4, k44, k444), resid, n9 = fit_cubic_through_origin(T4_GRID, rE, 0.25)
        (_, k44h, _), _, n7 = fit_cubic_through_origin(T4_GRID, rE, 0.1)
        (S4h, k44_h, _), _, _ = fit_cubic_through_origin(T4_GRID, np.array(arrays["r_agg_h_VRH"]), 0.25)
        (_, k44_HS, _), _, _ = fit_cubic_through_origin(T4_GRID, np.array(arrays["r_agg_E2_HS"]), 0.25)
        (_, k44_s7, _), _, ns7 = fit_cubic_through_origin(T4_GRID, rE, 0.25, inclusive=False)
        (_, k44_s5, _), _, ns5 = fit_cubic_through_origin(T4_GRID, rE, 0.1, inclusive=False)
        p.update({"S4_E2": S4, "S4_h": S4h, "kappa44_E2": k44, "kappa444_E2": k444, "kappa44_h": k44_h,
                  "kappa44_E2_HS": k44_HS, "halving_dev_kappa44": abs(k44 - k44h), "fit_residual_E2": resid,
                  "x_fit_windows": {"n_points_0p25_inclusive": n9, "n_points_0p1_inclusive": n7,
                                    "kappa44_E2_strict_window_0p25": k44_s7, "n_strict_0p25": ns7,
                                    "kappa44_E2_strict_window_0p1": k44_s5, "n_strict_0p1": ns5,
                                    "halving_dev_strict": abs(k44_s7 - k44_s5)}})
        # birefringence (A-2.7): symmetric difference at +-0.05 on Hill, k = x, labelled by polarization
        dv = {}
        for t in (0.05, -0.05):
            T = AGG[key].tensors(cfg.odf(t4=t))
            vsh, vsv, aY, aZ = transverse_pair_along_x(T["Hill"])
            dv[t] = vsh - vsv
        p["biref_b1_VRH"] = (dv[0.05] - dv[-0.05]) / (0.1 * p["vT_VRH"])
        p["x_biref_polarization_overlap_min"] = min(aY, aZ)
        print(f"   {key}: S4 {S4:+.3e} kappa44_E2 {k44:+.9e} (HS {k44_HS:+.6e}, h {k44_h:+.3e}) "
              f"kappa444 {k444:+.3e} halving {abs(k44 - k44h):.3e} b1 {p['biref_b1_VRH']:+.6e}")

    # Voigt birefringence identity on the cubic keys (in-instrument check, extras)
    for key, cfg in CFG.items():
        if cfg.sym != "cubic":
            continue
        Cv = mandel_to_voigt(cfg.M)
        H = Cv[0, 0] - Cv[0, 1] - 2.0 * Cv[3, 3]
        T = AGG[key].tensors(cfg.odf(t4=0.05))
        vsh, vsv, _, _ = transverse_pair_along_x(T["V"])
        biref_identity[key] = {"vqSH2_minus_vqSV2_voigt": vsh ** 2 - vsv ** 2, "H_t4_over_21": H * 0.05 / 21.0,
                               "rel_residual": rel_dev(vsh ** 2 - vsv ** 2, H * 0.05 / 21.0)}

    # ================================================================ Phase 2 second arm: quadratic form
    print("== Phase 2 second arm: the (t2, t4) quadratic form on the 5 x 5 grid; A-3.2 Richardson ==")
    for key, cfg in CFG.items():
        t2s, t4s, rs = [], [], []
        pos_min = math.inf
        for t2 in T2T4_GRID:
            for t4 in T2T4_GRID:
                w = cfg.odf(t2=t2, t4=t4)
                pos_min = min(pos_min, float(w.min()))
                T = AGG[key].tensors(w)
                d = r_on_tensor(T["Hill"], cfg, kq, wq, t2, t4)
                t2s.append(t2)
                t4s.append(t4)
                rs.append(d["r_E2"])
        qf = fit_quadform(np.array(t2s), np.array(t4s), np.array(rs))
        qf["x_grid_r_agg_E2_VRH"] = rs
        qf["x_reading"] = "(i) inherited descriptor-axis P2 (A-3.3)" if cfg.sym == "cubic" else "hex two-parameter family"
        phase2[key]["quadform"] = qf
        phase2[key]["x_min_odf_weight_5x5"] = pos_min

        def r_mixed(t2, t4):
            T = AGG[key].tensors(cfg.odf(t2=t2, t4=t4))
            return r_on_tensor(T["Hill"], cfg, kq, wq, t2, t4)["r_E2"]

        def D(h):
            return (r_mixed(h, h) - r_mixed(h, -h) - r_mixed(-h, h) + r_mixed(-h, -h)) / (4.0 * h * h)

        Dh, Dh2 = D(0.02), D(0.01)
        phase2[key]["kappa24_richardson"] = (4.0 * Dh2 - Dh) / 3.0
        phase2[key]["x_kappa24_richardson_D"] = {"D_0p02": Dh, "D_0p01": Dh2}
        if cfg.sym == "cubic":
            # reading (ii): the O_h-symmetrized l = 2 term vanishes identically on cubic; the form
            # reduces to kappa44 t4^2 -- the same 7-term fit on r(t4) alone, for the record
            rs_ii = []
            for t2 in T2T4_GRID:
                for t4 in T2T4_GRID:
                    T = AGG[key].tensors(cfg.odf(t4=t4))
                    rs_ii.append(r_on_tensor(T["Hill"], cfg, kq, wq, 0.0, t4)["r_E2"])
            phase2[key]["x_quadform_reading_ii_Oh_symmetrized"] = fit_quadform(np.array(t2s), np.array(t4s), np.array(rs_ii))
        print(f"   {key}: kappa22 {qf['kappa22']:+.6e} kappa24 {qf['kappa24']:+.6e} kappa44 {qf['kappa44']:+.6e} "
              f"resid {qf['residual']:.2e} | kappa24_richardson {phase2[key]['kappa24_richardson']:+.6e}")

    # ================================================================ Phase 0 controls
    print("== Phase 0 controls ==")
    # F-CTRL-SO3 (hex_step|a at t = 0 is the stated control; evaluated on every key)
    i0 = int(np.where(T4_GRID == 0.0)[0][0])
    r0 = max(abs(phase2[k]["r_agg_E2_VRH"][i0]) for k in KEYS)
    ctrl_so3 = {"passed": bool(so3_dev_all <= 1e-10 and r0 <= 1e-6), "dev_from_0p4": so3_dev_all,
                "r_agg_0_abs": r0, "x_mean_F0_t0": float(np.mean(so3_mean_t0))}

    # F-CTRL-QUAD
    ctrl_quad = {"passed": bool(doubling <= 1e-10), "doubling_residual": doubling,
                 "x_k_rule": "GL(cos theta) 64 x uniform phi 128; doubling 128 x 256 at t4 = 0.25 on Hill/E2 per key",
                 "x_fiber_rule": "fiber-axis route: analytic SO(2) coset average x GL(cos theta) 16 x uniform phi 32 on a generically rotated node set (exact to degree 31)"}

    # F-CTRL-ISO: isotropic tensor through both paths
    K_iso, G_iso = 134.609, 70.881
    C11i, C12i = K_iso + 4.0 * G_iso / 3.0, K_iso - 2.0 * G_iso / 3.0
    iso_worst = 0.0
    iso_detail = {}
    for path in ("cubic", "hex"):
        if path == "cubic":
            cfg_i = Config("iso|cubic", "cubic", voigt_to_mandel(cubic_voigt(C11i, C12i, G_iso)), ZHAT)
        else:
            cfg_i = Config("iso|hex", "hex", voigt_to_mandel(hex_voigt(C11i, C12i, C12i, C11i, G_iso, G_iso)), ZHAT)
        lo, hi = hs_reference(cfg_i.M, "lo"), hs_reference(cfg_i.M, "hi")
        agg_i = Aggregate(cfg_i, lo, hi)
        m = christoffel_modes(cfg_i.M, kq)
        d = descriptor_speeds(m, wq, frac_E2_fixed_axis(m, ZHAT))
        w_x = max(abs(d["r_E2"]), abs(d["r_h"]))
        w_a = 0.0
        for t in T4_GRID:
            T = agg_i.tensors(cfg_i.odf(t4=t))
            for tens in ("Hill", "HS"):
                dd = r_on_tensor(T[tens], cfg_i, kq, wq, 0.0, t)
                w_a = max(w_a, abs(dd["r_E2"]), abs(dd["r_h"]))
        iso_detail[path] = {"r_xtal_worst": w_x, "r_agg_worst": w_a}
        iso_worst = max(iso_worst, w_x, w_a)
    ctrl_iso = {"passed": bool(iso_worst <= 1e-10), "worst_abs": iso_worst, "x_detail": iso_detail}

    # F-CTRL-POS: every ODF used, on the fiber nodes
    pos_min = math.inf
    used = []
    for key, cfg in CFG.items():
        for t in T4_GRID:
            used.append(cfg.odf(t4=t))
            used.append(cfg.odf(t2=t))
        for t2 in T2T4_GRID:
            for t4 in T2T4_GRID:
                used.append(cfg.odf(t2=t2, t4=t4))
        for h in (0.02, 0.01):
            for s1 in (1, -1):
                for s2 in (1, -1):
                    used.append(cfg.odf(t2=s1 * h, t4=s2 * h))
        used.append(cfg.odf(t2=1.0))
        used.append(cfg.odf(t4=0.25, t6=0.3))
        used.append(cfg.odf(t2=0.25, t4=0.25, t6=0.3))
        for t in (0.05, -0.05, 0.3, 0.6, 1.0):
            used.append(cfg.odf(t4=t))
    pos_min = float(min(w.min() for w in used))
    ctrl_pos = {"passed": bool(pos_min >= 0.0), "min_odf_weight": pos_min, "x_n_odfs_checked": len(used)}

    # F-CTRL-L2NULL (A-3.1 scope)
    l2_worst = 0.0
    l2_detail, mixed_diag = {}, {}
    for key, cfg in CFG.items():
        if cfg.sym != "cubic":
            continue
        T0 = AGG[key].tensors(cfg.odf())
        T1 = AGG[key].tensors(cfg.odf(t2=1.0))
        d0 = r_on_tensor(T0["Hill"], cfg, kq, wq, 0.0, 0.0)
        d1 = r_on_tensor(T1["Hill"], cfg, kq, wq, 1.0, 0.0)
        pure = {"V": tensor_rel_change(T1["V"], T0["V"]), "Sbar": tensor_rel_change(T1["Sbar"], T0["Sbar"]),
                "HS_lo": tensor_rel_change(T1["HS_lo"], T0["HS_lo"]), "HS_hi": tensor_rel_change(T1["HS_hi"], T0["HS_hi"]),
                "r_agg_E2": abs(d1["r_E2"] - d0["r_E2"]), "r_agg_h": abs(d1["r_h"] - d0["r_h"])}
        Ta = AGG[key].tensors(cfg.odf(t2=0.0, t4=0.25))
        Tb = AGG[key].tensors(cfg.odf(t2=0.25, t4=0.25))
        da = r_on_tensor(Ta["Hill"], cfg, kq, wq, 0.0, 0.25)
        db = r_on_tensor(Tb["Hill"], cfg, kq, wq, 0.25, 0.25)
        mixed_t = {"V": tensor_rel_change(Tb["V"], Ta["V"]), "Sbar": tensor_rel_change(Tb["Sbar"], Ta["Sbar"]),
                   "HS_lo": tensor_rel_change(Tb["HS_lo"], Ta["HS_lo"]), "HS_hi": tensor_rel_change(Tb["HS_hi"], Ta["HS_hi"])}
        mixed_r = db["r_E2"] - da["r_E2"]
        l2_detail[key] = {"pure_l2_t1": pure, "mixed_tensor_clauses": mixed_t, "mixed_r_agg_change_A29": mixed_r,
                          "x_mixed_r_agg_h_change": db["r_h"] - da["r_h"]}
        mixed_diag[key] = mixed_r
        l2_worst = max(l2_worst, *pure.values(), *mixed_t.values())
    literal_worst = max(l2_worst, max(abs(v) for v in mixed_diag.values()))
    ctrl_l2 = {"passed": bool(l2_worst <= 1e-12), "worst_abs": l2_worst, "mixed_r_agg_change_A29": mixed_diag,
               "x_scope": "A-3.1: pure l = 2 (tensors + r_agg) and mixed-term tensor clauses; mixed r_agg reported",
               "x_literal_A29_worst_abs": literal_worst, "x_literal_A29_would_pass": bool(literal_worst <= 1e-12),
               "x_detail": l2_detail}

    # F-CTRL-L4EXHAUST
    ex_t, ex_r = 0.0, 0.0
    ex_detail = {}
    for key, cfg in CFG.items():
        cases = [((0.0, 0.25), "t4=0.25")]
        if cfg.sym == "hex":
            cases.append(((0.25, 0.25), "t2=t4=0.25"))
        for (t2, t4), label in cases:
            Ta = AGG[key].tensors(cfg.odf(t2=t2, t4=t4))
            Tb = AGG[key].tensors(cfg.odf(t2=t2, t4=t4, t6=0.3))
            da = r_on_tensor(Ta["Hill"], cfg, kq, wq, t2, t4, 0.0)
            db = r_on_tensor(Tb["Hill"], cfg, kq, wq, t2, t4, 0.3)
            ha = r_on_tensor(Ta["HS"], cfg, kq, wq, t2, t4, 0.0)
            hb = r_on_tensor(Tb["HS"], cfg, kq, wq, t2, t4, 0.3)
            tens = max(tensor_rel_change(Tb["V"], Ta["V"]), tensor_rel_change(Tb["Sbar"], Ta["Sbar"]),
                       tensor_rel_change(Tb["HS_lo"], Ta["HS_lo"]), tensor_rel_change(Tb["HS_hi"], Ta["HS_hi"]))
            rr = max(abs(db["r_E2"] - da["r_E2"]), abs(db["r_h"] - da["r_h"]), abs(hb["r_E2"] - ha["r_E2"]))
            entry = {"tensor_rel": tens, "r_agg_abs": rr}
            if cfg.sym == "cubic":
                m = christoffel_modes(Ta["Hill"], kq)
                wa = e2_direct_average(m, cfg, cfg.odf(t2=t2, t4=t4))
                wb = e2_direct_average(m, cfg, cfg.odf(t2=t2, t4=t4, t6=0.3))
                entry["x_direct_E2_weight_change"] = float(np.max(np.abs(wb - wa)))
            ex_detail[f"{key} {label}"] = entry
            ex_t, ex_r = max(ex_t, tens), max(ex_r, rr)
    ctrl_ex = {"passed": bool(ex_t <= 1e-12 and ex_r <= 1e-12), "worst_rel_tensor": ex_t, "worst_abs_r_agg": ex_r,
               "x_t6": 0.3, "x_K6_normalization": f"max|K6| = 1 on the sphere (raw scale {K6_SCALE})", "x_detail": ex_detail}

    # F-CTRL-C4: exact closed forms and affinity on both cubic configurations; H = 0 tensor
    c4_cf, c4_aff = 0.0, 0.0
    c4_detail = {}
    T4z = harmonic_l4_tensor(ZHAT)
    for key in ("cubic_step|001", "cubic_gem8|001"):
        cfg = CFG[key]
        Cv = mandel_to_voigt(cfg.M)
        H = Cv[0, 0] - Cv[0, 1] - 2.0 * Cv[3, 3]
        Sfull = mandel_to_full(np.linalg.inv(cfg.M))
        HS_ = Sfull[0, 0, 0, 0] - Sfull[0, 0, 1, 1] - 2.0 * Sfull[0, 1, 0, 1]
        T = {t: AGG[key].tensors(cfg.odf(t4=t)) for t in (0.0, 0.3, 0.6)}
        Cmax = float(np.max(np.abs(mandel_to_voigt(T[0.0]["V"]))))
        Smax = float(np.max(np.abs(mandel_to_full(T[0.0]["Sbar"]))))
        dev_cf, dev_af = 0.0, 0.0
        for t in (0.3, 0.6):
            dCv = mandel_to_voigt(T[t]["V"] - T[0.0]["V"])
            pred = mandel_to_voigt(full_to_mandel(t * (H / 3.0) * T4z))
            dev_cf = max(dev_cf, float(np.max(np.abs(dCv - pred))) / Cmax)
            dS = mandel_to_full(T[t]["Sbar"] - T[0.0]["Sbar"])
            dev_cf = max(dev_cf, float(np.max(np.abs(dS - t * (HS_ / 3.0) * T4z))) / Smax)
        dev_af = max(float(np.max(np.abs((T[0.6]["V"] - T[0.0]["V"]) - 2.0 * (T[0.3]["V"] - T[0.0]["V"])))) / Cmax,
                     float(np.max(np.abs((T[0.6]["Sbar"] - T[0.0]["Sbar"]) - 2.0 * (T[0.3]["Sbar"] - T[0.0]["Sbar"])))) / Smax)
        c4_detail[key] = {"H": H, "H_S": HS_, "closed_form_rel": dev_cf, "affine_rel": dev_af,
                          "x_voigt_dC_t0p3": [[float(x) for x in row] for row in mandel_to_voigt(T[0.3]["V"] - T[0.0]["V"])]}
        c4_cf, c4_aff = max(c4_cf, dev_cf), max(c4_aff, dev_af)
    cfg_h0 = Config("h0|cubic", "cubic", voigt_to_mandel(cubic_voigt(C11i, C12i, G_iso)), ZHAT)
    tab0 = fiber_table(cfg_h0.M)
    V0, V3 = odf_average(tab0, cfg_h0.odf()), odf_average(tab0, cfg_h0.odf(t4=0.3))
    h0_eff = float(np.max(np.abs(V3 - V0)) / np.max(np.abs(V0)))
    ctrl_c4 = {"passed": bool(c4_cf <= 1e-12 and c4_aff <= 1e-12 and h0_eff <= 1e-12),
               "worst_rel_closed_form": c4_cf, "worst_rel_affine": c4_aff, "h0_effect_rel": h0_eff, "x_detail": c4_detail}

    # F-CTRL-MARG: SO(3)-direct vs marginal E2 weight average on the cubic keys, every mode
    marg_worst = 0.0
    marg_detail = {}
    for key, cfg in CFG.items():
        if cfg.sym != "cubic":
            continue
        for t4 in (0.5, -0.5):
            T = AGG[key].tensors(cfg.odf(t4=t4))
            d = r_on_tensor(T["Hill"], cfg, kq, wq, 0.0, t4, want_modes=True)
            direct = e2_direct_average(d["_modes"], cfg, cfg.odf(t4=t4))
            valid = d["_modes"]["wEM"] > 1e-13
            dev = float(np.max(np.abs(direct[valid] - d["_fbar"][valid])))
            marg_detail[f"{key} t4={t4}"] = dev
            marg_worst = max(marg_worst, dev)
    ctrl_marg = {"passed": bool(marg_worst <= 1e-12), "worst_abs": marg_worst,
                 "x_c_coefficients": {"001": CFG["cubic_step|001"].c4, "111": CFG["cubic_step|111"].c4}, "x_detail": marg_detail}

    # F-CTRL-TEX4
    cfg_t = Config("tex4|cubic", "cubic", voigt_to_mandel(cubic_voigt(300.0, 100.0, 40.0)), ZHAT)
    lo, hi = hs_reference(cfg_t.M, "lo"), hs_reference(cfg_t.M, "hi")
    agg_t = Aggregate(cfg_t, lo, hi)
    Tt = agg_t.tensors(cfg_t.odf(t4=1.0))
    dt = r_on_tensor(Tt["Hill"], cfg_t, kq, wq, 0.0, 1.0)
    ctrl_tex = {"passed": bool(abs(dt["r_E2"]) > 1e-6), "r_agg_t1_abs": abs(dt["r_E2"]), "x_r_agg_t1": dt["r_E2"], "x_H": 120.0}

    phase0 = {
        "PIN-XTAL": pin_xtal, "PIN-VRH0": pin_vrh0, "PIN-HS0": pin_hs0, "PIN-K2": pin_k2,
        "F-CTRL-ISO": ctrl_iso, "F-CTRL-SO3": ctrl_so3, "F-CTRL-POS": ctrl_pos, "F-CTRL-L2NULL": ctrl_l2,
        "F-CTRL-L4EXHAUST": ctrl_ex, "F-CTRL-C4": ctrl_c4, "F-CTRL-MARG": ctrl_marg, "F-CTRL-TEX4": ctrl_tex,
        "F-CTRL-QUAD": ctrl_quad,
    }
    assert list(phase0) == schema["phase0"]["items"]
    for name, c in phase0.items():
        floats = {k: c[k] for k in schema["phase0"]["float_rules"].get(name, {})}
        print(f"   {name}: {'PASS' if c['passed'] else 'FAIL'}  {floats}")

    # ================================================================ Phase 3 (verdict last, schema rule)
    worst_S4 = max(max(abs(phase2[k]["S4_E2"]), abs(phase2[k]["S4_h"])) for k in KEYS)
    all0 = all(c["passed"] for c in phase0.values())
    fm3 = "FIRES" if worst_S4 > tau else "SILENT"
    null_cubic = all(abs(phase2[k]["kappa44_E2"]) <= kfloor for k in schema["primary_cubic_keys"])
    fm4 = "FIRES" if null_cubic else "SILENT"
    if not all0:
        verdict = "INDETERMINATE"
    elif fm3 == "FIRES":
        verdict = "PROTECTION-BREACH"
    elif null_cubic:
        verdict = "L4-NULL"
    else:
        verdict = "IDENTITY-DELIVERED-L4"
    phase3 = {"verdict_class": verdict, "F-MS2-3": fm3, "F-MS2-4": fm4, "F-MS2-2": "REGISTERED_NOT_EXECUTED", "worst_S4": worst_S4}
    print(f"== verdict: {verdict}  (worst |S4| {worst_S4:.3e}; F-MS2-3 {fm3}; F-MS2-4 {fm4}) ==")

    checkpoint = {
        "gate": "G-MSCS2", "leg": "cc", "instrument": "g_mscs2_ccleg.py",
        "instrument_md5": md5_file(os.path.abspath(__file__)),
        "memo_lock_md5": GUARDS[MEMO][0], "memo_lock_bytes": GUARDS[MEMO][1],
        "ledger_base_md5": schema["ledger_base_md5"],
        "t1_list_md5": GUARDS[T1_LIST][0], "schema_md5": GUARDS["g_mscs2_schema_v1_0.json"][0],
        "x1_md5": GUARDS["inputs/poly_vrh_results.json"][0],
        "x6_chat_md5": GUARDS["inputs/g_mscs1_chatleg_checkpoint.json"][0],
        "x6_cc_md5": GUARDS["inputs/g_mscs1_ccleg_checkpoint.json"][0],
        "activation_flag": ACTIVATION_FLAG, "addendum_A3_in_force": A3_IN_FORCE,
        "utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "elections": dict(schema["elections"]),
        "t1_scan": t1_state,
        "phase0": phase0, "phase1": phase1, "phase2": phase2, "phase3": phase3,
        "extras": {
            "method": {
                "so3_route": "fiber-axis: analytic SO(2) coset average (TI projector for tensors; closed-form psi moments for the E2 weight) x S^2 rule GL(cos theta) 16 x uniform phi 32 over the crystal-frame fiber axis, node set rotated by a fixed generic rotation",
                "so3_exact_degree": 31, "n_fiber_nodes": int(len(WFIB)),
                "k_rule": "GL(cos theta) 64 x uniform phi 128 (pinned)", "n_rule": "GL 12 x 24 (pinned)",
                "fracE2": "(1 - (k.n)^2)(1 - (ehat_perp.n)^2)",
                "hs_optimizer": "boundary-K0 bisection + 600-point coarse scan + 9 nested 21-point refinements over G0",
                "fit_windows": "|t4| <= 0.25 (9 points) and |t4| <= 0.1 (7 points), inclusive (G-MSCS1 convention); strict-window fits in phase2[key].x_fit_windows",
                "cubic_two_parameter_reading": "(i) inherited descriptor-axis P2 (A-3.3); reading (ii) in phase2[key].x_quadform_reading_ii_Oh_symmetrized",
            },
            "selftests": st,
            "hs_references": {k: {"lo_K0_G0_GHS": list(v["lo"]), "hi_K0_G0_GHS": list(v["hi"])} for k, v in hs_ref.items()},
            "A3_diagnostics": {
                "A-3.1_mixed_r_agg_change_A29": mixed_diag,
                "A-3.2_kappa24_richardson": {k: phase2[k]["kappa24_richardson"] for k in KEYS},
                "A-3.3_reading": "(i) inherited descriptor-axis P2",
            },
            "biref_voigt_identity_cubic": biref_identity,
            "so3_control_mean_F0_by_key": so3_mean_t0,
            "elapsed_seconds": 0.0,
        },
    }
    checkpoint["extras"]["elapsed_seconds"] = round(time.time() - t_start, 3)

    def to_py(o):
        if isinstance(o, dict):
            return {str(k): to_py(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [to_py(v) for v in o]
        if isinstance(o, np.ndarray):
            return to_py(o.tolist())
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o

    checkpoint = to_py(checkpoint)
    out_path = os.path.join(HERE, "g_mscs2_ccleg_checkpoint.json")
    blob = json.dumps(checkpoint, indent=1, ensure_ascii=False)
    hits, coll = t1mod.scan_text(blob, t1pats)
    if hits:
        halt(f"T1 HIT in the emitted checkpoint: {[i for i, _ in hits]}")
    checkpoint["t1_scan"]["checkpoint_numeric_collisions"] = len(coll)
    blob = json.dumps(checkpoint, indent=1, ensure_ascii=False)
    hits, coll2 = t1mod.scan_text(blob, t1pats)
    if hits or len(coll2) != len(coll):
        halt("T1 fixed point on the emitted checkpoint failed")
    open(out_path, "w", encoding="utf-8").write(blob)
    print(f"checkpoint -> {out_path}  md5 {md5_file(out_path)}  runtime {checkpoint['extras']['elapsed_seconds']} s")


if __name__ == "__main__":
    main()
=====END-EMBED name=g_mscs2_ccleg.py=====

=====BEGIN-EMBED name=g_mscs2_ccleg_checkpoint.json md5=9961745d1e1857cfab6445d4754b5060 bytes=68540 encoding=raw=====
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
=====END-EMBED name=g_mscs2_ccleg_checkpoint.json=====

=====BEGIN-EMBED name=g_mscs2_twoleg_comparison.json md5=a91d84a5b5cbe24221aa2e6301c67675 bytes=65679 encoding=raw=====
{
 "cc_ckpt_md5": "9961745d1e1857cfab6445d4754b5060",
 "chat_ckpt_md5": "1c5b6b59829d2a6b9ae2b1a7a016832d",
 "comparator": "g_mscs2_compare_v1_0",
 "misses": [
  {
   "cc": null,
   "chat": 4.48191107636109e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 4.48191140345094e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.974043374986076e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.974043382091395e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": -2.98793883027198e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -2.987937980693619e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.9740433870651724e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.9740433813807004e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 7.963757933367799e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 7.963760249103659e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.4778572462814414e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.477857238464886e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": -5.3091738364530734e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -5.309171208626909e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.477857238465428e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.47785722141147e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  }
 ],
 "rows": [
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key gate present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key gate present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key leg present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key leg present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key instrument_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key instrument_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key memo_lock_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key memo_lock_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key ledger_base_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key ledger_base_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_list_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_list_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x1_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x1_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_chat_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_chat_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_cc_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_cc_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key elections present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key elections present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_scan present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_scan present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase0 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase0 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase2 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase2 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase3 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase3 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "efdcabdcd937cda4acb64f941dc4bb2b",
   "chat": "efdcabdcd937cda4acb64f941dc4bb2b",
   "check": "C0",
   "name": "memo_lock_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "efdcabdcd937cda4acb64f941dc4bb2b",
   "chat": "efdcabdcd937cda4acb64f941dc4bb2b",
   "check": "C0",
   "name": "memo_lock_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "f36bbdb04104008783f2763f70fb916f",
   "chat": "f36bbdb04104008783f2763f70fb916f",
   "check": "C0",
   "name": "ledger_base_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "f36bbdb04104008783f2763f70fb916f",
   "chat": "f36bbdb04104008783f2763f70fb916f",
   "check": "C0",
   "name": "ledger_base_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "be921b8c29f7578e85ed92f1450c1956",
   "chat": "be921b8c29f7578e85ed92f1450c1956",
   "check": "C0",
   "name": "t1_list_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "be921b8c29f7578e85ed92f1450c1956",
   "chat": "be921b8c29f7578e85ed92f1450c1956",
   "check": "C0",
   "name": "t1_list_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "200e7a8b775577564369c6924d38a84c",
   "chat": "200e7a8b775577564369c6924d38a84c",
   "check": "C0",
   "name": "x1_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "200e7a8b775577564369c6924d38a84c",
   "chat": "200e7a8b775577564369c6924d38a84c",
   "check": "C0",
   "name": "x1_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "chat": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "check": "C0",
   "name": "x6_chat_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "chat": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "check": "C0",
   "name": "x6_chat_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "249e11dd53c4cb82f302b15d3c94c337",
   "chat": "249e11dd53c4cb82f302b15d3c94c337",
   "check": "C0",
   "name": "x6_cc_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "249e11dd53c4cb82f302b15d3c94c337",
   "chat": "249e11dd53c4cb82f302b15d3c94c337",
   "check": "C0",
   "name": "x6_cc_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "G-MSCS2",
   "chat": "G-MSCS2",
   "check": "C0",
   "name": "gate label",
   "note": "",
   "pass": true
  },
  {
   "cc": "cc",
   "chat": "chat",
   "check": "C0",
   "name": "leg labels chat/cc",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "CLEAN",
   "check": "C0",
   "name": "t1_scan.instrument CLEAN (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "CLEAN",
   "chat": null,
   "check": "C0",
   "name": "t1_scan.instrument CLEAN (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "CLEAN",
   "check": "C0",
   "name": "t1_scan.memo CLEAN (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "CLEAN",
   "chat": null,
   "check": "C0",
   "name": "t1_scan.memo CLEAN (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": {
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
   "chat": {
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
   "check": "C0",
   "name": "elections == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": {
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
   "chat": {
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
   "check": "C0",
   "name": "elections == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "e58ba9a6d52daa23f8264255b6dbbb75",
   "chat": "f277580ddf0b4da9734d11edb009c54b",
   "check": "C0",
   "name": "independence witness: instrument_md5 differ",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-XTAL.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0,
   "check": "C1",
   "name": "phase0.PIN-XTAL.worst_rel (chat) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.9907334492519883e-13,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-XTAL.worst_rel (cc) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-VRH0.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0,
   "check": "C1",
   "name": "phase0.PIN-VRH0.worst_rel (chat) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.740581037287146e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-VRH0.worst_rel (cc) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-HS0.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0,
   "check": "C1",
   "name": "phase0.PIN-HS0.worst_rel (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.4642081959835474e-12,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-HS0.worst_rel (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-K2.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.1553376966476035e-15,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_abs_cubic_kappa2 (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.1015835146880138e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_abs_cubic_kappa2 (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.3929675245859295e-12,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_rel_hex_kappa2 (chat) le 0.0001",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.9101739846654823e-12,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_rel_hex_kappa2 (cc) le 0.0001",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.440892098500626e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.worst_abs (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.440892098500626e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.worst_abs (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.996003610813204e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.dev_from_0p4 (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.771561172376096e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.dev_from_0p4 (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.r_agg_0_abs (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.3306690738754696e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.r_agg_0_abs (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.39502706178551494,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.min_odf_weight (chat) ge 0.0",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.33498992971329056,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.min_odf_weight (cc) ge 0.0",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 5.849908933676171e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.worst_abs (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.987802509504381e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.worst_abs (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.440892098500626e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_abs_r_agg (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 5.551115123125783e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_abs_r_agg (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.325772878954588e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_rel_tensor (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 6.420725383328799e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_rel_tensor (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.3021584638627248e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.h0_effect_rel (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.9771733495537138e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.h0_effect_rel (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.0740437216673334e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_affine (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.5337177708315534e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_affine (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.5186926550099605e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_closed_form (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.7155661439689658e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_closed_form (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 8.326672684688674e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.worst_abs (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.659783421814609e-14,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.worst_abs (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0004118326557733809,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.r_agg_t1_abs (chat) gt 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0004118326557733809,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.r_agg_t1_abs (cc) gt 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.2603428860704315e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.doubling_residual (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.220446049250313e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.doubling_residual (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 7.820e-18",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 2.220e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": -2.1901880737433866e-13,
   "chat": -2.2136167800606602e-13,
   "check": "C2",
   "name": "phase2[hex_step|a].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.604097370267146e-14,
   "chat": 7.665423084547844e-14,
   "check": "C2",
   "name": "phase2[hex_step|a].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.01624085410722665,
   "chat": 0.01624085410723511,
   "check": "C2",
   "name": "phase2[hex_step|a].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.2148264931772227e-07,
   "chat": 2.214826941714643e-07,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016040534614166288,
   "chat": 0.00016040534614367987,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.000159893047686394,
   "chat": 0.000159893047684377,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.507739663239201e-06,
   "chat": -7.507739661972004e-06,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.424582419402885,
   "chat": 8.424582419403457,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.390859731729106,
   "chat": 8.390859731728247,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.419059637591612,
   "chat": 8.419059637591603,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.6055695365075912e-09,
   "check": "C2",
   "name": "phase2[hex_step|a].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.605578370315842e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0014394693020041397,
   "chat": -0.0014394693020032903,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.2488792577836864e-08,
   "chat": -1.2488790730491887e-08,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016039903763748667,
   "chat": 0.00016039903763945317,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 3.578e-18",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": -2.2010851017752434e-13,
   "chat": -2.1990268388075987e-13,
   "check": "C2",
   "name": "phase2[hex_step|b].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.34844721335253e-14,
   "chat": 7.485871681214715e-14,
   "check": "C2",
   "name": "phase2[hex_step|b].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.016241797577238582,
   "chat": 0.016241797577228063,
   "check": "C2",
   "name": "phase2[hex_step|b].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.2158411841270297e-07,
   "chat": 2.2158410762808975e-07,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016041466503203565,
   "chat": 0.00016041466503408588,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001599025849219905,
   "chat": 0.00015990258492339606,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.509018171302918e-06,
   "chat": -7.509018168894417e-06,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.424803257723177,
   "chat": 8.424803257723832,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.391084746839004,
   "chat": 8.391084746837947,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.419278648579626,
   "chat": 8.419278648579612,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.6061616350891272e-09,
   "check": "C2",
   "name": "phase2[hex_step|b].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.606171687621935e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0014387102478831734,
   "chat": -0.001438710247883606,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.2484618920946934e-08,
   "chat": -1.2484615083901236e-08,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016040835823498604,
   "chat": 0.00016040835823465525,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 5.075e-18",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 6.661e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 2.220e-16",
   "pass": true
  },
  {
   "cc": -2.6497773212688476e-13,
   "chat": -2.652046374551464e-13,
   "check": "C2",
   "name": "phase2[hex_gem8|a].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.39909948940018e-14,
   "chat": 8.394408199844183e-14,
   "check": "C2",
   "name": "phase2[hex_gem8|a].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.018174882511168545,
   "chat": 0.01817488251117739,
   "check": "C2",
   "name": "phase2[hex_gem8|a].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.1931009361797286e-07,
   "chat": 2.1931009732824822e-07,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017950729579206332,
   "chat": 0.00017950729579484115,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001789305885712823,
   "chat": 0.0001789305885725744,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.754414848821103e-06,
   "chat": -7.754414849489288e-06,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.052797754948084,
   "chat": 10.052797754949037,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.990913001571435,
   "chat": 9.990913001571156,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.041721817369147,
   "chat": 10.041721817369147,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.9836269332293953e-09,
   "check": "C2",
   "name": "phase2[hex_gem8|a].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.98359848907698e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0018956599069480582,
   "chat": -0.0018956599069468293,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.837213389418741e-08,
   "chat": -1.837213417851943e-08,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001794984220250463,
   "chat": 0.00017949842202586976,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 1.891e-17",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 6.661e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 2.220e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 2.220e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 3.331e-16",
   "pass": true
  },
  {
   "cc": -2.6449971836009003e-13,
   "chat": -2.664544112656851e-13,
   "check": "C2",
   "name": "phase2[hex_gem8|b].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.407053114138355e-14,
   "chat": 8.256781483484296e-14,
   "check": "C2",
   "name": "phase2[hex_gem8|b].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.018174297109331976,
   "chat": 0.018174297109340813,
   "check": "C2",
   "name": "phase2[hex_gem8|b].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.1923555007017898e-07,
   "chat": 2.1923559565364329e-07,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017950151355280498,
   "chat": 0.00017950151354905876,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001789247303803612,
   "chat": 0.00017892473038334653,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.753635743351712e-06,
   "chat": -7.753635743144201e-06,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.052629959293983,
   "chat": 10.052629959294945,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.990739829721441,
   "chat": 9.99073982971986,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.041554085160628,
   "chat": 10.041554085160632,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.9831700693261328e-09,
   "check": "C2",
   "name": "phase2[hex_gem8|b].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.983162964739032e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0018961488929958188,
   "chat": -0.0018961488929936498,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.8376076624769533e-08,
   "chat": -1.8376074990497388e-08,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001794926395035944,
   "chat": 0.00017949263950353062,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 2.374e-17",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 2.220e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 5.551e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 3.331e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 3.331e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 3.331e-16",
   "pass": true
  },
  {
   "cc": -1.9550561581989927e-11,
   "chat": -1.9549678946260598e-11,
   "check": "C2",
   "name": "phase2[cubic_step|001].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.1695158327148078e-11,
   "chat": -1.1694898610377518e-11,
   "check": "C2",
   "name": "phase2[cubic_step|001].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0378987033959945,
   "chat": -0.03789870339598654,
   "check": "C2",
   "name": "phase2[cubic_step|001].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.633164259954152e-06,
   "chat": 2.633164231609963e-06,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0003743529418199647,
   "chat": -0.0003743529418175674,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0003892647453545792,
   "chat": -0.00038926474535513255,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -3.8028327671478075e-05,
   "chat": -3.8028327673460484e-05,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.867953005903455,
   "chat": 7.867953005904775,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.758614490213423,
   "chat": 7.758614490211087,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.7990463758449255,
   "chat": 7.799046375844923,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 3.8814126843849956e-08,
   "check": "C2",
   "name": "phase2[cubic_step|001].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.881410404427089e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.48191140345094e-09,
   "chat": 4.48191107636109e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.974043382091395e-07,
   "chat": 1.974043374986076e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00037435455939083614,
   "chat": -0.00037435455939106166,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.48191107636109e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 4.48191140345094e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.974043374986076e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.974043382091395e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 2.374e-17",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 6.661e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 3.331e-16",
   "pass": true
  },
  {
   "cc": 1.3036078957132319e-11,
   "chat": 1.3035416405833344e-11,
   "check": "C2",
   "name": "phase2[cubic_step|111].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.1695158327148078e-11,
   "chat": -1.1694898610377518e-11,
   "check": "C2",
   "name": "phase2[cubic_step|111].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0378987033959945,
   "chat": -0.03789870339598654,
   "check": "C2",
   "name": "phase2[cubic_step|111].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.7554428634061992e-06,
   "chat": -1.7554428600870769e-06,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00024956862787469286,
   "chat": 0.00024956862787724117,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00025950983023583375,
   "chat": 0.00025950983023805826,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -3.8028327671478075e-05,
   "chat": -3.8028327673460484e-05,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.867953005903455,
   "chat": 7.867953005904775,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.758614490213423,
   "chat": 7.758614490211087,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.7990463758449255,
   "chat": 7.799046375844923,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.58760610979741e-08,
   "check": "C2",
   "name": "phase2[cubic_step|111].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.5876089432676306e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.987937980693619e-09,
   "chat": -2.98793883027198e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.9740433813807004e-07,
   "chat": 1.9740433870651724e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00024956970625728664,
   "chat": 0.00024956970625745204,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": -2.98793883027198e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -2.987937980693619e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.9740433870651724e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.9740433813807004e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 1.076e-17",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 3.331e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 3.331e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 3.331e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": -4.267032120491424e-11,
   "chat": -4.267168229021896e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.3853273799039695e-11,
   "chat": -2.385281734789809e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.045481252227733915,
   "chat": -0.04548125222774924,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.7958466267304677e-06,
   "chat": 3.7958466556260277e-06,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00044927709343161725,
   "chat": -0.0004492770934296169,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00047671519504299364,
   "chat": -0.0004767151950423074,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -4.5357822665197825e-05,
   "chat": -4.535782266248913e-05,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.456854984586533,
   "chat": 9.456854984588738,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.21172106438435,
   "chat": 9.211721064370861,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.307899076533191,
   "chat": 9.307899076533179,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 6.896612588907494e-08,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 6.896611766469673e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.963760249103659e-09,
   "chat": 7.963757933367799e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.477857238464886e-07,
   "chat": 3.4778572462814414e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0004492799676061741,
   "chat": -0.00044927996760422685,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 7.963757933367799e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 7.963760249103659e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.4778572462814414e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.477857238464886e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 1.076e-17",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 6.661e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 4.441e-16",
   "pass": true
  },
  {
   "cc": 2.844703507492917e-11,
   "chat": 2.8447697640179876e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.3853273799039695e-11,
   "chat": -2.385281734789809e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.045481252227733915,
   "chat": -0.04548125222774924,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.5305644157388242e-06,
   "chat": -2.530564419058326e-06,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00029951806228339543,
   "chat": 0.00029951806228887087,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00031781013002442837,
   "chat": 0.00031781013002497063,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -4.5357822665197825e-05,
   "chat": -4.535782266248913e-05,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.456854984586533,
   "chat": 9.456854984588738,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.21172106438435,
   "chat": 9.211721064370861,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.307899076533191,
   "chat": 9.307899076533179,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.597743564728951e-08,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.597744102265546e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -5.309171208626909e-09,
   "chat": -5.3091738364530734e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.47785722141147e-07,
   "chat": 3.477857238465428e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0002995199784012639,
   "chat": 0.0002995199784038129,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": -5.3091738364530734e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -5.309171208626909e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.477857238465428e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.47785722141147e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": "REGISTERED_NOT_EXECUTED",
   "chat": "REGISTERED_NOT_EXECUTED",
   "check": "C3",
   "name": "phase3.F-MS2-2 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "REGISTERED_NOT_EXECUTED",
   "chat": "REGISTERED_NOT_EXECUTED",
   "check": "C3",
   "name": "phase3.F-MS2-2 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-3 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-3 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-4 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-4 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class equal",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class in domain (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.267168229021896e-11,
   "check": "C3",
   "name": "phase3.worst_S4 (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": null,
   "check": "C3",
   "name": "phase3.verdict_class in domain (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.267032120491424e-11,
   "chat": null,
   "check": "C3",
   "name": "phase3.worst_S4 (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "verdict recomputed == reported (chat)",
   "note": "reported IDENTITY-DELIVERED-L4",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C3",
   "name": "worst_S4 consistent with phase2 (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "SILENT",
   "check": "C3",
   "name": "F-MS2-3 state consistent (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": null,
   "check": "C3",
   "name": "verdict recomputed == reported (cc)",
   "note": "reported IDENTITY-DELIVERED-L4",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C3",
   "name": "worst_S4 consistent with phase2 (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": null,
   "check": "C3",
   "name": "F-MS2-3 state consistent (cc)",
   "note": "",
   "pass": true
  }
 ],
 "schema_md5": "66f586d7b6c5e8228394222ddfda73f2",
 "summary": {
  "checks": 356,
  "miss": 16,
  "pass": 340
 }
}
=====END-EMBED name=g_mscs2_twoleg_comparison.json=====

=====BEGIN-EMBED name=g_mscs2_chatleg_selfcompare_CCRERUN.json md5=0a10623660c8fbaed4c37ec388978593 bytes=65952 encoding=raw=====
{
 "cc_ckpt_md5": "1c5b6b59829d2a6b9ae2b1a7a016832d",
 "chat_ckpt_md5": "1c5b6b59829d2a6b9ae2b1a7a016832d",
 "comparator": "g_mscs2_compare_v1_0",
 "misses": [
  {
   "cc": "chat",
   "chat": "chat",
   "check": "C0",
   "name": "leg labels chat/cc",
   "note": "",
   "pass": false
  },
  {
   "cc": "f277580ddf0b4da9734d11edb009c54b",
   "chat": "f277580ddf0b4da9734d11edb009c54b",
   "check": "C0",
   "name": "independence witness: instrument_md5 differ",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 4.48191107636109e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 4.48191107636109e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.974043374986076e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.974043374986076e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": -2.98793883027198e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -2.98793883027198e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.9740433870651724e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.9740433870651724e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 7.963757933367799e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 7.963757933367799e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.4778572462814414e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.4778572462814414e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": -5.3091738364530734e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -5.3091738364530734e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.477857238465428e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.477857238465428e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  }
 ],
 "rows": [
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key gate present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key gate present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key leg present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key leg present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key instrument_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key instrument_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key memo_lock_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key memo_lock_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key ledger_base_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key ledger_base_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_list_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_list_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x1_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x1_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_chat_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_chat_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_cc_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_cc_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key elections present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key elections present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_scan present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_scan present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase0 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase0 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase2 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase2 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase3 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase3 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "efdcabdcd937cda4acb64f941dc4bb2b",
   "chat": "efdcabdcd937cda4acb64f941dc4bb2b",
   "check": "C0",
   "name": "memo_lock_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "efdcabdcd937cda4acb64f941dc4bb2b",
   "chat": "efdcabdcd937cda4acb64f941dc4bb2b",
   "check": "C0",
   "name": "memo_lock_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "f36bbdb04104008783f2763f70fb916f",
   "chat": "f36bbdb04104008783f2763f70fb916f",
   "check": "C0",
   "name": "ledger_base_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "f36bbdb04104008783f2763f70fb916f",
   "chat": "f36bbdb04104008783f2763f70fb916f",
   "check": "C0",
   "name": "ledger_base_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "be921b8c29f7578e85ed92f1450c1956",
   "chat": "be921b8c29f7578e85ed92f1450c1956",
   "check": "C0",
   "name": "t1_list_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "be921b8c29f7578e85ed92f1450c1956",
   "chat": "be921b8c29f7578e85ed92f1450c1956",
   "check": "C0",
   "name": "t1_list_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "200e7a8b775577564369c6924d38a84c",
   "chat": "200e7a8b775577564369c6924d38a84c",
   "check": "C0",
   "name": "x1_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "200e7a8b775577564369c6924d38a84c",
   "chat": "200e7a8b775577564369c6924d38a84c",
   "check": "C0",
   "name": "x1_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "chat": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "check": "C0",
   "name": "x6_chat_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "chat": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "check": "C0",
   "name": "x6_chat_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "249e11dd53c4cb82f302b15d3c94c337",
   "chat": "249e11dd53c4cb82f302b15d3c94c337",
   "check": "C0",
   "name": "x6_cc_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "249e11dd53c4cb82f302b15d3c94c337",
   "chat": "249e11dd53c4cb82f302b15d3c94c337",
   "check": "C0",
   "name": "x6_cc_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "G-MSCS2",
   "chat": "G-MSCS2",
   "check": "C0",
   "name": "gate label",
   "note": "",
   "pass": true
  },
  {
   "cc": "chat",
   "chat": "chat",
   "check": "C0",
   "name": "leg labels chat/cc",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": "CLEAN",
   "check": "C0",
   "name": "t1_scan.instrument CLEAN (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "CLEAN",
   "chat": null,
   "check": "C0",
   "name": "t1_scan.instrument CLEAN (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "CLEAN",
   "check": "C0",
   "name": "t1_scan.memo CLEAN (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "CLEAN",
   "chat": null,
   "check": "C0",
   "name": "t1_scan.memo CLEAN (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": {
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
   "chat": {
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
   "check": "C0",
   "name": "elections == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": {
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
   "chat": {
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
   "check": "C0",
   "name": "elections == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "f277580ddf0b4da9734d11edb009c54b",
   "chat": "f277580ddf0b4da9734d11edb009c54b",
   "check": "C0",
   "name": "independence witness: instrument_md5 differ",
   "note": "",
   "pass": false
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-XTAL.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0,
   "check": "C1",
   "name": "phase0.PIN-XTAL.worst_rel (chat) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-XTAL.worst_rel (cc) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-VRH0.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0,
   "check": "C1",
   "name": "phase0.PIN-VRH0.worst_rel (chat) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-VRH0.worst_rel (cc) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-HS0.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0,
   "check": "C1",
   "name": "phase0.PIN-HS0.worst_rel (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-HS0.worst_rel (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-K2.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.1553376966476035e-15,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_abs_cubic_kappa2 (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.1553376966476035e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_abs_cubic_kappa2 (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.3929675245859295e-12,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_rel_hex_kappa2 (chat) le 0.0001",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.3929675245859295e-12,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_rel_hex_kappa2 (cc) le 0.0001",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.440892098500626e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.worst_abs (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.440892098500626e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.worst_abs (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.996003610813204e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.dev_from_0p4 (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.996003610813204e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.dev_from_0p4 (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.r_agg_0_abs (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.r_agg_0_abs (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.39502706178551494,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.min_odf_weight (chat) ge 0.0",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.39502706178551494,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.min_odf_weight (cc) ge 0.0",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 5.849908933676171e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.worst_abs (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 5.849908933676171e-14,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.worst_abs (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.440892098500626e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_abs_r_agg (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.440892098500626e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_abs_r_agg (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.325772878954588e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_rel_tensor (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.325772878954588e-14,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_rel_tensor (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.3021584638627248e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.h0_effect_rel (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.3021584638627248e-14,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.h0_effect_rel (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.0740437216673334e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_affine (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.0740437216673334e-14,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_affine (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.5186926550099605e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_closed_form (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.5186926550099605e-14,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_closed_form (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 8.326672684688674e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.worst_abs (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.326672684688674e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.worst_abs (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0004118326557733809,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.r_agg_t1_abs (chat) gt 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0004118326557733809,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.r_agg_t1_abs (cc) gt 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.2603428860704315e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.doubling_residual (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.2603428860704315e-14,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.doubling_residual (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -2.2136167800606602e-13,
   "chat": -2.2136167800606602e-13,
   "check": "C2",
   "name": "phase2[hex_step|a].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.665423084547844e-14,
   "chat": 7.665423084547844e-14,
   "check": "C2",
   "name": "phase2[hex_step|a].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.01624085410723511,
   "chat": 0.01624085410723511,
   "check": "C2",
   "name": "phase2[hex_step|a].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.214826941714643e-07,
   "chat": 2.214826941714643e-07,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016040534614367987,
   "chat": 0.00016040534614367987,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.000159893047684377,
   "chat": 0.000159893047684377,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.507739661972004e-06,
   "chat": -7.507739661972004e-06,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.424582419403457,
   "chat": 8.424582419403457,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.390859731728247,
   "chat": 8.390859731728247,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.419059637591603,
   "chat": 8.419059637591603,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.6055695365075912e-09,
   "check": "C2",
   "name": "phase2[hex_step|a].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.6055695365075912e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0014394693020032903,
   "chat": -0.0014394693020032903,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.2488790730491887e-08,
   "chat": -1.2488790730491887e-08,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016039903763945317,
   "chat": 0.00016039903763945317,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -2.1990268388075987e-13,
   "chat": -2.1990268388075987e-13,
   "check": "C2",
   "name": "phase2[hex_step|b].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.485871681214715e-14,
   "chat": 7.485871681214715e-14,
   "check": "C2",
   "name": "phase2[hex_step|b].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.016241797577228063,
   "chat": 0.016241797577228063,
   "check": "C2",
   "name": "phase2[hex_step|b].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.2158410762808975e-07,
   "chat": 2.2158410762808975e-07,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016041466503408588,
   "chat": 0.00016041466503408588,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00015990258492339606,
   "chat": 0.00015990258492339606,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.509018168894417e-06,
   "chat": -7.509018168894417e-06,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.424803257723832,
   "chat": 8.424803257723832,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.391084746837947,
   "chat": 8.391084746837947,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.419278648579612,
   "chat": 8.419278648579612,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.6061616350891272e-09,
   "check": "C2",
   "name": "phase2[hex_step|b].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.6061616350891272e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.001438710247883606,
   "chat": -0.001438710247883606,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.2484615083901236e-08,
   "chat": -1.2484615083901236e-08,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016040835823465525,
   "chat": 0.00016040835823465525,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -2.652046374551464e-13,
   "chat": -2.652046374551464e-13,
   "check": "C2",
   "name": "phase2[hex_gem8|a].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.394408199844183e-14,
   "chat": 8.394408199844183e-14,
   "check": "C2",
   "name": "phase2[hex_gem8|a].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.01817488251117739,
   "chat": 0.01817488251117739,
   "check": "C2",
   "name": "phase2[hex_gem8|a].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.1931009732824822e-07,
   "chat": 2.1931009732824822e-07,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017950729579484115,
   "chat": 0.00017950729579484115,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001789305885725744,
   "chat": 0.0001789305885725744,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.754414849489288e-06,
   "chat": -7.754414849489288e-06,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.052797754949037,
   "chat": 10.052797754949037,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.990913001571156,
   "chat": 9.990913001571156,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.041721817369147,
   "chat": 10.041721817369147,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.9836269332293953e-09,
   "check": "C2",
   "name": "phase2[hex_gem8|a].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.9836269332293953e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0018956599069468293,
   "chat": -0.0018956599069468293,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.837213417851943e-08,
   "chat": -1.837213417851943e-08,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017949842202586976,
   "chat": 0.00017949842202586976,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -2.664544112656851e-13,
   "chat": -2.664544112656851e-13,
   "check": "C2",
   "name": "phase2[hex_gem8|b].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.256781483484296e-14,
   "chat": 8.256781483484296e-14,
   "check": "C2",
   "name": "phase2[hex_gem8|b].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.018174297109340813,
   "chat": 0.018174297109340813,
   "check": "C2",
   "name": "phase2[hex_gem8|b].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.1923559565364329e-07,
   "chat": 2.1923559565364329e-07,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017950151354905876,
   "chat": 0.00017950151354905876,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017892473038334653,
   "chat": 0.00017892473038334653,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.753635743144201e-06,
   "chat": -7.753635743144201e-06,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.052629959294945,
   "chat": 10.052629959294945,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.99073982971986,
   "chat": 9.99073982971986,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.041554085160632,
   "chat": 10.041554085160632,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.9831700693261328e-09,
   "check": "C2",
   "name": "phase2[hex_gem8|b].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.9831700693261328e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0018961488929936498,
   "chat": -0.0018961488929936498,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.8376074990497388e-08,
   "chat": -1.8376074990497388e-08,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017949263950353062,
   "chat": 0.00017949263950353062,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -1.9549678946260598e-11,
   "chat": -1.9549678946260598e-11,
   "check": "C2",
   "name": "phase2[cubic_step|001].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.1694898610377518e-11,
   "chat": -1.1694898610377518e-11,
   "check": "C2",
   "name": "phase2[cubic_step|001].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.03789870339598654,
   "chat": -0.03789870339598654,
   "check": "C2",
   "name": "phase2[cubic_step|001].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.633164231609963e-06,
   "chat": 2.633164231609963e-06,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0003743529418175674,
   "chat": -0.0003743529418175674,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00038926474535513255,
   "chat": -0.00038926474535513255,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -3.8028327673460484e-05,
   "chat": -3.8028327673460484e-05,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.867953005904775,
   "chat": 7.867953005904775,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.758614490211087,
   "chat": 7.758614490211087,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.799046375844923,
   "chat": 7.799046375844923,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 3.8814126843849956e-08,
   "check": "C2",
   "name": "phase2[cubic_step|001].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.8814126843849956e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.48191107636109e-09,
   "chat": 4.48191107636109e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.974043374986076e-07,
   "chat": 1.974043374986076e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00037435455939106166,
   "chat": -0.00037435455939106166,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.48191107636109e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 4.48191107636109e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.974043374986076e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.974043374986076e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 1.3035416405833344e-11,
   "chat": 1.3035416405833344e-11,
   "check": "C2",
   "name": "phase2[cubic_step|111].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.1694898610377518e-11,
   "chat": -1.1694898610377518e-11,
   "check": "C2",
   "name": "phase2[cubic_step|111].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.03789870339598654,
   "chat": -0.03789870339598654,
   "check": "C2",
   "name": "phase2[cubic_step|111].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.7554428600870769e-06,
   "chat": -1.7554428600870769e-06,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00024956862787724117,
   "chat": 0.00024956862787724117,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00025950983023805826,
   "chat": 0.00025950983023805826,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -3.8028327673460484e-05,
   "chat": -3.8028327673460484e-05,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.867953005904775,
   "chat": 7.867953005904775,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.758614490211087,
   "chat": 7.758614490211087,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.799046375844923,
   "chat": 7.799046375844923,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.58760610979741e-08,
   "check": "C2",
   "name": "phase2[cubic_step|111].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.58760610979741e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.98793883027198e-09,
   "chat": -2.98793883027198e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.9740433870651724e-07,
   "chat": 1.9740433870651724e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00024956970625745204,
   "chat": 0.00024956970625745204,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": -2.98793883027198e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -2.98793883027198e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.9740433870651724e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.9740433870651724e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -4.267168229021896e-11,
   "chat": -4.267168229021896e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.385281734789809e-11,
   "chat": -2.385281734789809e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.04548125222774924,
   "chat": -0.04548125222774924,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.7958466556260277e-06,
   "chat": 3.7958466556260277e-06,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0004492770934296169,
   "chat": -0.0004492770934296169,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0004767151950423074,
   "chat": -0.0004767151950423074,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -4.535782266248913e-05,
   "chat": -4.535782266248913e-05,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.456854984588738,
   "chat": 9.456854984588738,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.211721064370861,
   "chat": 9.211721064370861,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.307899076533179,
   "chat": 9.307899076533179,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 6.896612588907494e-08,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 6.896612588907494e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.963757933367799e-09,
   "chat": 7.963757933367799e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.4778572462814414e-07,
   "chat": 3.4778572462814414e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00044927996760422685,
   "chat": -0.00044927996760422685,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 7.963757933367799e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 7.963757933367799e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.4778572462814414e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.4778572462814414e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 2.8447697640179876e-11,
   "chat": 2.8447697640179876e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.385281734789809e-11,
   "chat": -2.385281734789809e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.04548125222774924,
   "chat": -0.04548125222774924,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.530564419058326e-06,
   "chat": -2.530564419058326e-06,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00029951806228887087,
   "chat": 0.00029951806228887087,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00031781013002497063,
   "chat": 0.00031781013002497063,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -4.535782266248913e-05,
   "chat": -4.535782266248913e-05,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.456854984588738,
   "chat": 9.456854984588738,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.211721064370861,
   "chat": 9.211721064370861,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.307899076533179,
   "chat": 9.307899076533179,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.597743564728951e-08,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.597743564728951e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -5.3091738364530734e-09,
   "chat": -5.3091738364530734e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.477857238465428e-07,
   "chat": 3.477857238465428e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0002995199784038129,
   "chat": 0.0002995199784038129,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": -5.3091738364530734e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -5.3091738364530734e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.477857238465428e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.477857238465428e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": "REGISTERED_NOT_EXECUTED",
   "chat": "REGISTERED_NOT_EXECUTED",
   "check": "C3",
   "name": "phase3.F-MS2-2 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "REGISTERED_NOT_EXECUTED",
   "chat": "REGISTERED_NOT_EXECUTED",
   "check": "C3",
   "name": "phase3.F-MS2-2 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-3 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-3 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-4 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-4 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class equal",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class in domain (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.267168229021896e-11,
   "check": "C3",
   "name": "phase3.worst_S4 (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": null,
   "check": "C3",
   "name": "phase3.verdict_class in domain (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.267168229021896e-11,
   "chat": null,
   "check": "C3",
   "name": "phase3.worst_S4 (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "verdict recomputed == reported (chat)",
   "note": "reported IDENTITY-DELIVERED-L4",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C3",
   "name": "worst_S4 consistent with phase2 (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "SILENT",
   "check": "C3",
   "name": "F-MS2-3 state consistent (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": null,
   "check": "C3",
   "name": "verdict recomputed == reported (cc)",
   "note": "reported IDENTITY-DELIVERED-L4",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C3",
   "name": "worst_S4 consistent with phase2 (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": null,
   "check": "C3",
   "name": "F-MS2-3 state consistent (cc)",
   "note": "",
   "pass": true
  }
 ],
 "schema_md5": "66f586d7b6c5e8228394222ddfda73f2",
 "summary": {
  "checks": 356,
  "miss": 18,
  "pass": 338
 }
}
=====END-EMBED name=g_mscs2_chatleg_selfcompare_CCRERUN.json=====

=====BEGIN-EMBED name=g_mscs2_ccleg_selfcompare.json md5=7951e0f0e41607a7372d8269a51f83ef bytes=66080 encoding=raw=====
{
 "cc_ckpt_md5": "9961745d1e1857cfab6445d4754b5060",
 "chat_ckpt_md5": "9961745d1e1857cfab6445d4754b5060",
 "comparator": "g_mscs2_compare_v1_0",
 "misses": [
  {
   "cc": "cc",
   "chat": "cc",
   "check": "C0",
   "name": "leg labels chat/cc",
   "note": "",
   "pass": false
  },
  {
   "cc": "e58ba9a6d52daa23f8264255b6dbbb75",
   "chat": "e58ba9a6d52daa23f8264255b6dbbb75",
   "check": "C0",
   "name": "independence witness: instrument_md5 differ",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 4.48191140345094e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 4.48191140345094e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.974043382091395e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.974043382091395e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": -2.987937980693619e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -2.987937980693619e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.9740433813807004e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.9740433813807004e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 7.963760249103659e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 7.963760249103659e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.477857238464886e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.477857238464886e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": -5.309171208626909e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -5.309171208626909e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.47785722141147e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.47785722141147e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  }
 ],
 "rows": [
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key gate present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key gate present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key leg present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key leg present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key instrument_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key instrument_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key memo_lock_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key memo_lock_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key ledger_base_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key ledger_base_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_list_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_list_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x1_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x1_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_chat_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_chat_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_cc_md5 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key x6_cc_md5 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key elections present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key elections present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_scan present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key t1_scan present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase0 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase0 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase2 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase2 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase3 present (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C0",
   "name": "required key phase3 present (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "efdcabdcd937cda4acb64f941dc4bb2b",
   "chat": "efdcabdcd937cda4acb64f941dc4bb2b",
   "check": "C0",
   "name": "memo_lock_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "efdcabdcd937cda4acb64f941dc4bb2b",
   "chat": "efdcabdcd937cda4acb64f941dc4bb2b",
   "check": "C0",
   "name": "memo_lock_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "f36bbdb04104008783f2763f70fb916f",
   "chat": "f36bbdb04104008783f2763f70fb916f",
   "check": "C0",
   "name": "ledger_base_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "f36bbdb04104008783f2763f70fb916f",
   "chat": "f36bbdb04104008783f2763f70fb916f",
   "check": "C0",
   "name": "ledger_base_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "be921b8c29f7578e85ed92f1450c1956",
   "chat": "be921b8c29f7578e85ed92f1450c1956",
   "check": "C0",
   "name": "t1_list_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "be921b8c29f7578e85ed92f1450c1956",
   "chat": "be921b8c29f7578e85ed92f1450c1956",
   "check": "C0",
   "name": "t1_list_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "200e7a8b775577564369c6924d38a84c",
   "chat": "200e7a8b775577564369c6924d38a84c",
   "check": "C0",
   "name": "x1_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "200e7a8b775577564369c6924d38a84c",
   "chat": "200e7a8b775577564369c6924d38a84c",
   "check": "C0",
   "name": "x1_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "chat": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "check": "C0",
   "name": "x6_chat_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "chat": "c04c0b8ea34cfe60f231aa06828e6ce4",
   "check": "C0",
   "name": "x6_chat_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "249e11dd53c4cb82f302b15d3c94c337",
   "chat": "249e11dd53c4cb82f302b15d3c94c337",
   "check": "C0",
   "name": "x6_cc_md5 == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "249e11dd53c4cb82f302b15d3c94c337",
   "chat": "249e11dd53c4cb82f302b15d3c94c337",
   "check": "C0",
   "name": "x6_cc_md5 == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "G-MSCS2",
   "chat": "G-MSCS2",
   "check": "C0",
   "name": "gate label",
   "note": "",
   "pass": true
  },
  {
   "cc": "cc",
   "chat": "cc",
   "check": "C0",
   "name": "leg labels chat/cc",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": "CLEAN",
   "check": "C0",
   "name": "t1_scan.instrument CLEAN (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "CLEAN",
   "chat": null,
   "check": "C0",
   "name": "t1_scan.instrument CLEAN (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "CLEAN",
   "check": "C0",
   "name": "t1_scan.memo CLEAN (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "CLEAN",
   "chat": null,
   "check": "C0",
   "name": "t1_scan.memo CLEAN (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": {
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
   "chat": {
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
   "check": "C0",
   "name": "elections == schema (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": {
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
   "chat": {
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
   "check": "C0",
   "name": "elections == schema (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "e58ba9a6d52daa23f8264255b6dbbb75",
   "chat": "e58ba9a6d52daa23f8264255b6dbbb75",
   "check": "C0",
   "name": "independence witness: instrument_md5 differ",
   "note": "",
   "pass": false
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-XTAL.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 3.9907334492519883e-13,
   "check": "C1",
   "name": "phase0.PIN-XTAL.worst_rel (chat) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.9907334492519883e-13,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-XTAL.worst_rel (cc) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-VRH0.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 3.740581037287146e-15,
   "check": "C1",
   "name": "phase0.PIN-VRH0.worst_rel (chat) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.740581037287146e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-VRH0.worst_rel (cc) le 1e-08",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-HS0.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.4642081959835474e-12,
   "check": "C1",
   "name": "phase0.PIN-HS0.worst_rel (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.4642081959835474e-12,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-HS0.worst_rel (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.PIN-K2.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 3.1015835146880138e-15,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_abs_cubic_kappa2 (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.1015835146880138e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_abs_cubic_kappa2 (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.9101739846654823e-12,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_rel_hex_kappa2 (chat) le 0.0001",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.9101739846654823e-12,
   "chat": null,
   "check": "C1",
   "name": "phase0.PIN-K2.worst_rel_hex_kappa2 (cc) le 0.0001",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.440892098500626e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.worst_abs (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.440892098500626e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-ISO.worst_abs (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 7.771561172376096e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.dev_from_0p4 (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.771561172376096e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.dev_from_0p4 (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 3.3306690738754696e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.r_agg_0_abs (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.3306690738754696e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-SO3.r_agg_0_abs (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.33498992971329056,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.min_odf_weight (chat) ge 0.0",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.33498992971329056,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-POS.min_odf_weight (cc) ge 0.0",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 7.987802509504381e-15,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.worst_abs (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.987802509504381e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L2NULL.worst_abs (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 5.551115123125783e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_abs_r_agg (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 5.551115123125783e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_abs_r_agg (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 6.420725383328799e-15,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_rel_tensor (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 6.420725383328799e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-L4EXHAUST.worst_rel_tensor (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.9771733495537138e-15,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.h0_effect_rel (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.9771733495537138e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.h0_effect_rel (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 3.5337177708315534e-15,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_affine (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.5337177708315534e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_affine (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.7155661439689658e-15,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_closed_form (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.7155661439689658e-15,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-C4.worst_rel_closed_form (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.659783421814609e-14,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.worst_abs (chat) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.659783421814609e-14,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-MARG.worst_abs (cc) le 1e-12",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 0.0004118326557733809,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.r_agg_t1_abs (chat) gt 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0004118326557733809,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-TEX4.r_agg_t1_abs (cc) gt 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": true,
   "chat": true,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.passed true both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.220446049250313e-16,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.doubling_residual (chat) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.220446049250313e-16,
   "chat": null,
   "check": "C1",
   "name": "phase0.F-CTRL-QUAD.doubling_residual (cc) le 1e-10",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -2.1901880737433866e-13,
   "chat": -2.1901880737433866e-13,
   "check": "C2",
   "name": "phase2[hex_step|a].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.604097370267146e-14,
   "chat": 7.604097370267146e-14,
   "check": "C2",
   "name": "phase2[hex_step|a].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.01624085410722665,
   "chat": 0.01624085410722665,
   "check": "C2",
   "name": "phase2[hex_step|a].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.2148264931772227e-07,
   "chat": 2.2148264931772227e-07,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016040534614166288,
   "chat": 0.00016040534614166288,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.000159893047686394,
   "chat": 0.000159893047686394,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.507739663239201e-06,
   "chat": -7.507739663239201e-06,
   "check": "C2",
   "name": "phase2[hex_step|a].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.424582419402885,
   "chat": 8.424582419402885,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.390859731729106,
   "chat": 8.390859731729106,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.419059637591612,
   "chat": 8.419059637591612,
   "check": "C2",
   "name": "phase2[hex_step|a].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.605578370315842e-09,
   "check": "C2",
   "name": "phase2[hex_step|a].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.605578370315842e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|a].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0014394693020041397,
   "chat": -0.0014394693020041397,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.2488792577836864e-08,
   "chat": -1.2488792577836864e-08,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016039903763748667,
   "chat": 0.00016039903763748667,
   "check": "C2",
   "name": "phase2[hex_step|a].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -2.2010851017752434e-13,
   "chat": -2.2010851017752434e-13,
   "check": "C2",
   "name": "phase2[hex_step|b].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.34844721335253e-14,
   "chat": 7.34844721335253e-14,
   "check": "C2",
   "name": "phase2[hex_step|b].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.016241797577238582,
   "chat": 0.016241797577238582,
   "check": "C2",
   "name": "phase2[hex_step|b].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.2158411841270297e-07,
   "chat": 2.2158411841270297e-07,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016041466503203565,
   "chat": 0.00016041466503203565,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001599025849219905,
   "chat": 0.0001599025849219905,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.509018171302918e-06,
   "chat": -7.509018171302918e-06,
   "check": "C2",
   "name": "phase2[hex_step|b].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.424803257723177,
   "chat": 8.424803257723177,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.391084746839004,
   "chat": 8.391084746839004,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.419278648579626,
   "chat": 8.419278648579626,
   "check": "C2",
   "name": "phase2[hex_step|b].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.606171687621935e-09,
   "check": "C2",
   "name": "phase2[hex_step|b].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.606171687621935e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_step|b].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0014387102478831734,
   "chat": -0.0014387102478831734,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.2484618920946934e-08,
   "chat": -1.2484618920946934e-08,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00016040835823498604,
   "chat": 0.00016040835823498604,
   "check": "C2",
   "name": "phase2[hex_step|b].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -2.6497773212688476e-13,
   "chat": -2.6497773212688476e-13,
   "check": "C2",
   "name": "phase2[hex_gem8|a].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.39909948940018e-14,
   "chat": 8.39909948940018e-14,
   "check": "C2",
   "name": "phase2[hex_gem8|a].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.018174882511168545,
   "chat": 0.018174882511168545,
   "check": "C2",
   "name": "phase2[hex_gem8|a].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.1931009361797286e-07,
   "chat": 2.1931009361797286e-07,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017950729579206332,
   "chat": 0.00017950729579206332,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001789305885712823,
   "chat": 0.0001789305885712823,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.754414848821103e-06,
   "chat": -7.754414848821103e-06,
   "check": "C2",
   "name": "phase2[hex_gem8|a].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.052797754948084,
   "chat": 10.052797754948084,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.990913001571435,
   "chat": 9.990913001571435,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.041721817369147,
   "chat": 10.041721817369147,
   "check": "C2",
   "name": "phase2[hex_gem8|a].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.98359848907698e-09,
   "check": "C2",
   "name": "phase2[hex_gem8|a].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.98359848907698e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|a].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0018956599069480582,
   "chat": -0.0018956599069480582,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.837213389418741e-08,
   "chat": -1.837213389418741e-08,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001794984220250463,
   "chat": 0.0001794984220250463,
   "check": "C2",
   "name": "phase2[hex_gem8|a].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -2.6449971836009003e-13,
   "chat": -2.6449971836009003e-13,
   "check": "C2",
   "name": "phase2[hex_gem8|b].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 8.407053114138355e-14,
   "chat": 8.407053114138355e-14,
   "check": "C2",
   "name": "phase2[hex_gem8|b].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.018174297109331976,
   "chat": 0.018174297109331976,
   "check": "C2",
   "name": "phase2[hex_gem8|b].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.1923555007017898e-07,
   "chat": 2.1923555007017898e-07,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00017950151355280498,
   "chat": 0.00017950151355280498,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001789247303803612,
   "chat": 0.0001789247303803612,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -7.753635743351712e-06,
   "chat": -7.753635743351712e-06,
   "check": "C2",
   "name": "phase2[hex_gem8|b].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.052629959293983,
   "chat": 10.052629959293983,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.990739829721441,
   "chat": 9.990739829721441,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 10.041554085160628,
   "chat": 10.041554085160628,
   "check": "C2",
   "name": "phase2[hex_gem8|b].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 1.983162964739032e-09,
   "check": "C2",
   "name": "phase2[hex_gem8|b].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.983162964739032e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[hex_gem8|b].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0018961488929958188,
   "chat": -0.0018961488929958188,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.8376076624769533e-08,
   "chat": -1.8376076624769533e-08,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0001794926395035944,
   "chat": 0.0001794926395035944,
   "check": "C2",
   "name": "phase2[hex_gem8|b].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -1.9550561581989927e-11,
   "chat": -1.9550561581989927e-11,
   "check": "C2",
   "name": "phase2[cubic_step|001].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.1695158327148078e-11,
   "chat": -1.1695158327148078e-11,
   "check": "C2",
   "name": "phase2[cubic_step|001].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0378987033959945,
   "chat": -0.0378987033959945,
   "check": "C2",
   "name": "phase2[cubic_step|001].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.633164259954152e-06,
   "chat": 2.633164259954152e-06,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0003743529418199647,
   "chat": -0.0003743529418199647,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0003892647453545792,
   "chat": -0.0003892647453545792,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -3.8028327671478075e-05,
   "chat": -3.8028327671478075e-05,
   "check": "C2",
   "name": "phase2[cubic_step|001].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.867953005903455,
   "chat": 7.867953005903455,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.758614490213423,
   "chat": 7.758614490213423,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.7990463758449255,
   "chat": 7.7990463758449255,
   "check": "C2",
   "name": "phase2[cubic_step|001].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 3.881410404427089e-08,
   "check": "C2",
   "name": "phase2[cubic_step|001].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.881410404427089e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.48191140345094e-09,
   "chat": 4.48191140345094e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.974043382091395e-07,
   "chat": 1.974043382091395e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00037435455939083614,
   "chat": -0.00037435455939083614,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.48191140345094e-09,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 4.48191140345094e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.974043382091395e-07,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.974043382091395e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 1.3036078957132319e-11,
   "chat": 1.3036078957132319e-11,
   "check": "C2",
   "name": "phase2[cubic_step|111].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.1695158327148078e-11,
   "chat": -1.1695158327148078e-11,
   "check": "C2",
   "name": "phase2[cubic_step|111].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0378987033959945,
   "chat": -0.0378987033959945,
   "check": "C2",
   "name": "phase2[cubic_step|111].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -1.7554428634061992e-06,
   "chat": -1.7554428634061992e-06,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00024956862787469286,
   "chat": 0.00024956862787469286,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00025950983023583375,
   "chat": 0.00025950983023583375,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -3.8028327671478075e-05,
   "chat": -3.8028327671478075e-05,
   "check": "C2",
   "name": "phase2[cubic_step|111].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.867953005903455,
   "chat": 7.867953005903455,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.758614490213423,
   "chat": 7.758614490213423,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.7990463758449255,
   "chat": 7.7990463758449255,
   "check": "C2",
   "name": "phase2[cubic_step|111].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 2.5876089432676306e-08,
   "check": "C2",
   "name": "phase2[cubic_step|111].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 2.5876089432676306e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.987937980693619e-09,
   "chat": -2.987937980693619e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 1.9740433813807004e-07,
   "chat": 1.9740433813807004e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00024956970625728664,
   "chat": 0.00024956970625728664,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": -2.987937980693619e-09,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -2.987937980693619e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 1.9740433813807004e-07,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 1.9740433813807004e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_step|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": -4.267032120491424e-11,
   "chat": -4.267032120491424e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.3853273799039695e-11,
   "chat": -2.3853273799039695e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.045481252227733915,
   "chat": -0.045481252227733915,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.7958466267304677e-06,
   "chat": 3.7958466267304677e-06,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00044927709343161725,
   "chat": -0.00044927709343161725,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.00047671519504299364,
   "chat": -0.00047671519504299364,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -4.5357822665197825e-05,
   "chat": -4.5357822665197825e-05,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.456854984586533,
   "chat": 9.456854984586533,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.21172106438435,
   "chat": 9.21172106438435,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.307899076533191,
   "chat": 9.307899076533191,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 6.896611766469673e-08,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 6.896611766469673e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 7.963760249103659e-09,
   "chat": 7.963760249103659e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.477857238464886e-07,
   "chat": 3.477857238464886e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.0004492799676061741,
   "chat": -0.0004492799676061741,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 7.963760249103659e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 7.963760249103659e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.477857238464886e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.477857238464886e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|001].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111] present both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].lambda_mean_t4 length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].lambda_mean_t4 elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_HS length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_HS elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_R length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_R elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_V length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_V elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_E2_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 12,
   "chat": 12,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_h_VRH length 12 both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].r_agg_h_VRH elementwise <= 1e-06",
   "note": "worst 0.000e+00",
   "pass": true
  },
  {
   "cc": 2.844703507492917e-11,
   "chat": 2.844703507492917e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].S4_E2 abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.3853273799039695e-11,
   "chat": -2.3853273799039695e-11,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].S4_h abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -0.045481252227733915,
   "chat": -0.045481252227733915,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].biref_b1_VRH abs <= 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": -2.5305644157388242e-06,
   "chat": -2.5305644157388242e-06,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa444_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00029951806228339543,
   "chat": 0.00029951806228339543,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_E2 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.00031781013002442837,
   "chat": 0.00031781013002442837,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_E2_HS rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": -4.5357822665197825e-05,
   "chat": -4.5357822665197825e-05,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].kappa44_h rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.456854984586533,
   "chat": 9.456854984586533,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_HS_hi rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.21172106438435,
   "chat": 9.21172106438435,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_HS_lo rel <= 1e-06 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": 9.307899076533191,
   "chat": 9.307899076533191,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].vT_VRH rel <= 1e-08 (floor 0.0)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.597744102265546e-08,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].halving_dev_kappa44 (chat) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.597744102265546e-08,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].halving_dev_kappa44 (cc) <= max(rel*|kappa44|, floor)",
   "note": "",
   "pass": true
  },
  {
   "cc": -5.309171208626909e-09,
   "chat": -5.309171208626909e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 3.47785722141147e-07,
   "chat": 3.47785722141147e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": 0.0002995199784012639,
   "chat": 0.0002995199784012639,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa44 rel <= 0.0001 (floor 1e-06)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": -5.309171208626909e-09,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": -5.309171208626909e-09,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa22 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": null,
   "chat": 3.47785722141147e-07,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (chat) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": 3.47785722141147e-07,
   "chat": null,
   "check": "C2",
   "name": "phase2[cubic_gem8|111].quadform.kappa24 (cc) cubic null abs <= 1e-10",
   "note": "",
   "pass": false
  },
  {
   "cc": "REGISTERED_NOT_EXECUTED",
   "chat": "REGISTERED_NOT_EXECUTED",
   "check": "C3",
   "name": "phase3.F-MS2-2 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "REGISTERED_NOT_EXECUTED",
   "chat": "REGISTERED_NOT_EXECUTED",
   "check": "C3",
   "name": "phase3.F-MS2-2 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-3 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-3 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-4 typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": "SILENT",
   "check": "C3",
   "name": "phase3.F-MS2-4 equal",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class typed str both legs",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class equal",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "phase3.verdict_class in domain (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": 4.267032120491424e-11,
   "check": "C3",
   "name": "phase3.worst_S4 (chat) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": null,
   "check": "C3",
   "name": "phase3.verdict_class in domain (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": 4.267032120491424e-11,
   "chat": null,
   "check": "C3",
   "name": "phase3.worst_S4 (cc) le 1e-06",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "IDENTITY-DELIVERED-L4",
   "check": "C3",
   "name": "verdict recomputed == reported (chat)",
   "note": "reported IDENTITY-DELIVERED-L4",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C3",
   "name": "worst_S4 consistent with phase2 (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": null,
   "chat": "SILENT",
   "check": "C3",
   "name": "F-MS2-3 state consistent (chat)",
   "note": "",
   "pass": true
  },
  {
   "cc": "IDENTITY-DELIVERED-L4",
   "chat": null,
   "check": "C3",
   "name": "verdict recomputed == reported (cc)",
   "note": "reported IDENTITY-DELIVERED-L4",
   "pass": true
  },
  {
   "cc": null,
   "chat": null,
   "check": "C3",
   "name": "worst_S4 consistent with phase2 (cc)",
   "note": "",
   "pass": true
  },
  {
   "cc": "SILENT",
   "chat": null,
   "check": "C3",
   "name": "F-MS2-3 state consistent (cc)",
   "note": "",
   "pass": true
  }
 ],
 "schema_md5": "66f586d7b6c5e8228394222ddfda73f2",
 "summary": {
  "checks": 356,
  "miss": 18,
  "pass": 338
 }
}
=====END-EMBED name=g_mscs2_ccleg_selfcompare.json=====

=====BEGIN-EMBED name=g_mscs2_ccleg_compare.json md5=daedd0dee64536be10ea1bd79c7a9c41 bytes=6426 encoding=raw=====
{
 "artifact": "G-MSCS2 CC-leg hypothesis compare (memo section 6; not verdicts)",
 "checkpoint_md5": "9961745d1e1857cfab6445d4754b5060",
 "leg": "cc",
 "summary": {
  "clauses": 25,
  "met": 20,
  "not_met": 5
 },
 "rows": [
  {
   "hypothesis": "HYP-MS2-1",
   "clause": "kappa44_E2 non-zero on both primary fcc keys (above the 1e-6 floor)",
   "met": true,
   "detail": {
    "cubic_step|001": -0.0003743529418199647,
    "cubic_gem8|001": -0.00044927709343161725
   }
  },
  {
   "hypothesis": "HYP-MS2-1",
   "clause": "|kappa44_E2| of order 1e-3 .. 1e-2 on the primary fcc keys",
   "met": false,
   "detail": {
    "cubic_step|001": 0.0003743529418199647,
    "cubic_gem8|001": 0.00044927709343161725
   }
  },
  {
   "hypothesis": "HYP-MS2-1",
   "clause": "kappa44_h smaller than kappa44_E2 in magnitude (ratio reported with <lambda_L> for scale)",
   "met": true,
   "detail": {
    "kappa44_h/kappa44_E2": {
     "cubic_step|001": 0.10158415608168724,
     "cubic_step|111": -0.1523762341257568,
     "cubic_gem8|001": 0.10095734531834431,
     "cubic_gem8|111": -0.15143601797971554
    },
    "lambda_mean": {
     "cubic_step|001": 0.0083923190288783,
     "cubic_step|111": 0.0083923190288783,
     "cubic_gem8|001": 0.0093105038596528,
     "cubic_gem8|111": 0.0093105038596528
    }
   }
  },
  {
   "hypothesis": "HYP-MS2-2",
   "clause": "cubic_step|001: sign kappa44_E2 == sign r_xtal_E2 and < 0",
   "met": true,
   "detail": {
    "kappa44_E2": -0.0003743529418199647,
    "r_xtal_E2": -0.01729676774121569
   }
  },
  {
   "hypothesis": "HYP-MS2-2",
   "clause": "cubic_step|111: sign kappa44_E2 == sign r_xtal_E2 and > 0",
   "met": true,
   "detail": {
    "kappa44_E2": 0.00024956862787469286,
    "r_xtal_E2": 0.01153117849414409
   }
  },
  {
   "hypothesis": "HYP-MS2-2",
   "clause": "cubic_gem8|001: sign kappa44_E2 == sign r_xtal_E2 and < 0",
   "met": true,
   "detail": {
    "kappa44_E2": -0.00044927709343161725,
    "r_xtal_E2": -0.020842442022740437
   }
  },
  {
   "hypothesis": "HYP-MS2-2",
   "clause": "cubic_gem8|111: sign kappa44_E2 == sign r_xtal_E2 and > 0",
   "met": true,
   "detail": {
    "kappa44_E2": 0.00029951806228339543,
    "r_xtal_E2": 0.01389496134849355
   }
  },
  {
   "hypothesis": "HYP-MS2-3",
   "clause": "|S4_E2|, |S4_h| <= 1e-6 on every key",
   "met": true,
   "detail": {
    "worst_S4": 4.267032120491424e-11
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_step|a: |kappa44| < |kappa22|",
   "met": true,
   "detail": {
    "kappa22": -0.0014394693020041397,
    "kappa44": 0.00016039903763748667
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_step|a: kappa24 non-zero (above the 1e-6 floor) with |kappa44| < |kappa24| < |kappa22|",
   "met": false,
   "detail": {
    "kappa24_fit": -1.2488792577836864e-08,
    "kappa24_richardson": 3.006854025026466e-13
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_step|a: kappa22 reproduces kappa2_E2 (l = 2 family) to 1e-4 relative",
   "met": true,
   "detail": {
    "kappa22": -0.0014394693020041397,
    "kappa2_E2": -0.0014394617694985317
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_step|b: |kappa44| < |kappa22|",
   "met": true,
   "detail": {
    "kappa22": -0.0014387102478831734,
    "kappa44": 0.00016040835823498604
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_step|b: kappa24 non-zero (above the 1e-6 floor) with |kappa44| < |kappa24| < |kappa22|",
   "met": false,
   "detail": {
    "kappa24_fit": -1.2484618920946934e-08,
    "kappa24_richardson": 1.8503717077085943e-13
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_step|b: kappa22 reproduces kappa2_E2 (l = 2 family) to 1e-4 relative",
   "met": true,
   "detail": {
    "kappa22": -0.0014387102478831734,
    "kappa2_E2": -0.0014387027187495968
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_gem8|a: |kappa44| < |kappa22|",
   "met": true,
   "detail": {
    "kappa22": -0.0018956599069480582,
    "kappa44": 0.0001794984220250463
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_gem8|a: kappa24 non-zero (above the 1e-6 floor) with |kappa44| < |kappa24| < |kappa22|",
   "met": false,
   "detail": {
    "kappa24_fit": -1.837213389418741e-08,
    "kappa24_richardson": 1.3646491344350882e-12
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_gem8|a: kappa22 reproduces kappa2_E2 (l = 2 family) to 1e-4 relative",
   "met": true,
   "detail": {
    "kappa22": -0.0018956599069480582,
    "kappa2_E2": -0.0018956484826737562
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_gem8|b: |kappa44| < |kappa22|",
   "met": true,
   "detail": {
    "kappa22": -0.0018961488929958188,
    "kappa44": 0.0001794926395035944
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_gem8|b: kappa24 non-zero (above the 1e-6 floor) with |kappa44| < |kappa24| < |kappa22|",
   "met": false,
   "detail": {
    "kappa24_fit": -1.8376076624769533e-08,
    "kappa24_richardson": 9.483155002006545e-13
   }
  },
  {
   "hypothesis": "HYP-MS2-4",
   "clause": "hex_gem8|b: kappa22 reproduces kappa2_E2 (l = 2 family) to 1e-4 relative",
   "met": true,
   "detail": {
    "kappa22": -0.0018961488929958188,
    "kappa2_E2": -0.001896137466524572
   }
  },
  {
   "hypothesis": "HYP-MS2-5",
   "clause": "cubic_step|001: |b1| of order 1e-1 (0.03 .. 0.3)",
   "met": true,
   "detail": {
    "biref_b1_VRH": -0.0378987033959945
   }
  },
  {
   "hypothesis": "HYP-MS2-5",
   "clause": "cubic_step|001: |b1| * 0.25 exceeds the descriptor split |kappa44| * 0.25^2 by >= two orders",
   "met": true,
   "detail": {
    "biref_at_0p25": 0.009474675848998625,
    "descriptor_split_at_0p25": 2.3397058863747792e-05,
    "ratio": 404.9515755024668
   }
  },
  {
   "hypothesis": "HYP-MS2-5",
   "clause": "cubic_gem8|001: |b1| of order 1e-1 (0.03 .. 0.3)",
   "met": true,
   "detail": {
    "biref_b1_VRH": -0.045481252227733915
   }
  },
  {
   "hypothesis": "HYP-MS2-5",
   "clause": "cubic_gem8|001: |b1| * 0.25 exceeds the descriptor split |kappa44| * 0.25^2 by >= two orders",
   "met": true,
   "detail": {
    "biref_at_0p25": 0.011370313056933479,
    "descriptor_split_at_0p25": 2.8079818339476078e-05,
    "ratio": 404.9282983055662
   }
  },
  {
   "hypothesis": "Expected class",
   "clause": "IDENTITY-DELIVERED-L4",
   "met": true,
   "detail": {
    "verdict_class": "IDENTITY-DELIVERED-L4"
   }
  }
 ]
}
=====END-EMBED name=g_mscs2_ccleg_compare.json=====

