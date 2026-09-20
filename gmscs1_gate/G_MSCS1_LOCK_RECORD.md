# LOCK RECORD — Gate G-MSCS1 (Multi-Species Channel Speed: the Q3(1) carrier-identity residue and the emergent species-universality obligation)

**LOCKED:** September 19, 2026 (chat leg). **Base:** `SQT_Master_Ledger_v4_82_CANONICAL.md` md5 `d095a7003bb0d4c177e7451e1d14c4c6` (1,552,643 B).
**Author authorization (verbatim, September 19, 2026):** "I explicitly AUTHORIZE Amendment A-1 and the lock of `staging_memo_G_MSCS1_v2.md` (`3f30262eaec461fb5fd3202835f7de37`)." Supersedes the draft lock record (8be7cb63, LOCK HELD) — every hash below is now final.

## 1. Artifact of record

| Artifact | md5 | Size |
|---|---|---|
| `staging_memo_G_MSCS1_v2.md` | `3f30262eaec461fb5fd3202835f7de37` | 34,837 B |

Lineage: v1 `staging_memo_G_MSCS1_draft.md` `53300f21cbe233a640a49e76685cdf57` (21,025 B), superseded by Amendment A-1 (memo §A). T1 scan of v2 under the gate list: CLEAN.

## 2. Elections (author, September 19, 2026 — T3-immutable)

E-MS-1 (a) · E-MS-2 (a) · E-MS-2b (a) primary + (b) second arm · E-MS-2c ⟨001⟩ primary, ⟨111⟩ reported · E-MS-3 (a), the second-order Born at t = 0 only (narrowing clarification, memo §8) · E-MS-4 (a) · E-MS-5 (a) · E-MS-6 (a). Amendment A-1 (A-1.1–A-1.4; re-class to a delivery gate) AUTHORIZED.

## 3. Frozen pre-emission artifacts

| Artifact | md5 | Size | State |
|---|---|---|---|
| `g_mscs1_schema_v1_0.json` | `76a42db3fd6ad82e485752bc2ddb24d5` | 3,906 B | FROZEN — carries every lock constant and tolerance (memo_lock_md5 = v2) |
| `g_mscs1_compare_v1_0.py` | `22432b292ae0a9d5c91a6cb7aa67502f` | 18,541 B | FROZEN — 17/17 adversarial suites; no gate numbers in the file |
| `tools/t1/T1_base_author_20260919.txt` | `05302210cc4ceb70553acbe8379e9fc3` | 143 B | base stratum (11 patterns; H-MS-0) |
| `tools/t1/T1_forbidden_G_MSCS1.txt` | `fef2827100d3f85e0a6341b44f0c00bf` | 1,433 B | gate list (36 patterns) |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 B | contextual numeric rule |

Both legs' checkpoints must carry `memo_md5` = v2, `T1.list_md5` = fef28271, `T1.state` = CLEAN; LIST_ABSENT is rejected by the comparator (D-T1 RETIRED).

## 4. Honesty items carried into execution

- **H-MS-0** — authorizing-directive T1-hash discrepancy (G-BKZ32 H-1 class): the supplied base list hashes to no variant of `04438b74` (11 vs 13 patterns; 143/55 B vs 117 B); pinned under its own hash with authority from the author's supply.
- **H-MS-1** — the v1 draft's kill set was symmetry-forced; caught at instrument design, pre-lock; Amendment A-1 authorized.

## 5. Addendum A-2 — operationalizations (chat, pre-execution; each locked here before the computation it governs)

- **A-2.1 Pin sources (banked, md5-verified at every open).** X-3 `gs2c1_gate/p2_ccleg/cc_p2_phase1.json` `aaae206733b0f0a378a5c6b600274d3f` (11,454 B): the full-precision a₂^agg = D2 quartet, D(0), I₀, I₂, V_T, V_L of the G-S2C1 P2 CC leg — the PIN-A2AGG reference (the ledger quotes the quartet to 7 digits; the pin is at 1×10⁻⁸ and needs the banked full precision). X-4 `gpoly1_gate/poly1_phase1full_cc.json` `ec87e42f0f617b00c4985ba2aceac339` (8,140 B): the general Voigt/Reuss moduli (`*_gen`) and the banked I₀ (`int_Phi_TT/TL`) — the PIN-VRH0 and kernel-moment references. X-5 `gpoly1_gate/chatleg_phase0bfull.json` `df413a7cfa30e599b779af8fee5d07d1` (1,920 B): the cubic Hashin–Shtrikman bands of record (A-2.3).
- **A-2.2 Kernel construction (PIN-A2AGG).** Φ_TM(μ) as in Addendum P2 of G-S2C1 (2feff442): δc = c(g) − c̄ with c̄ the SO(3) Voigt mean; incident T projector ½(I − p̂p̂), scattered projectors I − ŝŝ (T) and ŝŝ (L); N_M = 1/(V_T²V_M²), V_T = √μ̄, V_L = √(λ̄ + 2μ̄); D2 = Σ_M N_M[(1 − 2r_M²)I₀/8 − 3I₂/8] (P2-A). This leg's own quadrature: ZYZ product grid (16, 10, 16) (exact at band-limit 8; CC's was (12, 8, 12)); μ-moments by 8-point Gauss–Legendre (exact for the degree-4 even kernels). Helicity resolution (F-CTRL-POL): incident projectors ê_±ê_±^† with ê_± = (x̂ ± iŷ)/√2 in place of ½(I − p̂p̂).
- **A-2.3 Hashin–Shtrikman at texture t.** Walpole-form bounds with an isotropic reference C₀ = 3K₀J + 2G₀K: C_HS = [⟨(C_g + C*)⁻¹⟩_ODF]⁻¹ − C*, C* = 3K*J + 2G*K, K* = 4G₀/3, G* = G₀(9K₀ + 8G₀)/(6(K₀ + 2G₀)); the reference pair optimized at t = 0 (upper: the minimal feasible majorant C₀ ⪰ C_g giving the smallest bound; lower: the maximal minorant giving the largest) and reused at every t (the bounds stay rigorous for any ODF; slightly less tight off t = 0). Cubic at t = 0 must reproduce the X-5 bands to ≤ 1×10⁻⁶ relative (PIN-HS0); hex bands are reported as computed (the banked hex G_HS confirmation checkpoint is not among the fetched pin sources — stated, not hidden). `vT_HS_lo/hi` = the bound speeds at t = 0; the "HS scheme" for r_agg_E2_HS = the mean tensor ½(C_HS⁺ + C_HS⁻) at each t. VRH primary: `r_agg_*_VRH` uses the Hill tensor ½(C_V + C_R) at each t.
- **A-2.4 Fit and halving.** r_agg(t) fitted on the memo basis {t, t², t³} over the nine grid points |t| ≤ 0.25 (κ₂ of record, S_t of record); `halving_dev_kappa2` = the relative change of κ₂ when the window halves to |t| ≤ 0.1 (seven points). A 4-term {t, t², t³, t⁴} fit is reported alongside as a check (extra key, not compared).
- **A-2.5 Quadrature and doubling.** Sphere grid GL(cos θ) 64 × uniform φ 128; `quadrature.doubling_residual` = max over the eight configuration keys of |r_xtal_E2(64×128) − r_xtal_E2(128×256)|. Hex branches labelled by eigenvector character (qSH ≡ e ∥ ẑ × k̂, exactly decoupled), cubic by admixture (qL) then speed (qT1 fast, qT2 slow). Aggregate descriptor weight per mode: w_EM · ⟨f_E₂(n̂)⟩_ODF with f_E₂ the m = ±2 fraction of the transverse-projected strain about n̂, ⟨·⟩_ODF over the n̂-sphere with weight 1 + t·P₂(n̂·ẑ) (GL 12 × 24, exact for the degree-6 integrand); f_E₂(n̂) = 1 − 2|S_⊥n̂|²/|S_⊥|² + ½(n̂·S_⊥·n̂)²/|S_⊥|².
- **A-2.6 F-CTRL-ISO tensor.** Isotropic K = 134.609, G = 70.881 (the hex:step Hill pair) run through the cubic path with C11 − C12 = 2C44. **F-CTRL-TEX tensor.** Synthetic hex C11 = 300, C12 = 100, C13 = 50, C33 = 200, C44 = 40, C66 = 100 at t = 1.

## 6. Pinned execution constants (memo §4; schema)

τ_agg = 1×10⁻⁶. Two-leg: Phase-1 means/r/λ ≤ 1×10⁻⁸; pins ≤ 1×10⁻⁸; Born (t = 0) ≤ 1×10⁻⁶ rel; r_agg(t), S_t ≤ 1×10⁻⁶; κ₂ ≤ 1×10⁻⁴ rel (floor 1×10⁻⁶). t-grid {−0.5, −0.25, −0.1, −0.05, −0.02, 0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0}. X-1 `200e7a8b775577564369c6924d38a84c` (2,767 B).

## 7. Execution order

1. Chat leg `g_mscs1_chatleg.py`: selftest → phase0 (halt on any control failure → INDETERMINATE) → phase1 → phase2 → checkpoint → compare (last, separate artifact).
2. P-4 single-file in-band dispatch (memo, this record, schema, comparator, T1 list + scanner, pin sources in the clear; chat instrument/checkpoint/compare base64-armored); delivered alone (P-4.c).
3. CC leg blind from scratch; pre-consultation checkpoint committed before the armor is opened; comparator both sides; S9 on any MISS.
4. Fold at V4.83, carrying the §10 housekeeping bracket.
