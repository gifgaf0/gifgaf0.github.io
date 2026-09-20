# G-MSCS1 — CHAT-LEG EXECUTION REPORT

**Date:** September 19, 2026. **Base:** V4.82 `d095a7003bb0d4c177e7451e1d14c4c6`. **Memo lock:** v2 `3f30262eaec461fb5fd3202835f7de37` (34,837 B). **Lock record:** `G_MSCS1_LOCK_RECORD.md` `3dbe953badb6c030ef1d449adbac2044` (7,289 B; Addendum A-2 operationalizations locked pre-execution). **Comparator v1.0** `22432b29` + **schema v1.0** `76a42db3` FROZEN before this emission. **Instrument:** `g_mscs1_chatleg.py` `db5f51dd9ef7f54dd0826991d594681b` (34,606 B; 7/7 suites; md5-guards the memo, X-1, X-3..X-5; T1 halt-without-list; run time 8 m 45 s single core). **Checkpoint:** `g_mscs1_chatleg_checkpoint.json` `c04c0b8ea34cfe60f231aa06828e6ce4` (33,289 B). **Compare (last):** `g_mscs1_chatleg_compare.json` `7b933c08b92d57b9523f2cee4ff076ba` (3,277 B). **T1:** gate list `fef28271` CLEAN on instrument, memo, checkpoint (4 numeric formatting collisions logged, 0 hits), compare (1 collision, 0 hits). **Verdict class: IDENTITY-DELIVERED.**

## 1. Phase 0 — controls and pins (all PASS)

| Control | Result |
|---|---|
| F-CTRL-ISO | r_xtal_E2 2.2×10⁻¹⁶, r_xtal_h 0, λ_max 5.9×10⁻³¹, max_t |r_agg| 4.4×10⁻¹⁶ — texture on an isotropic grain does nothing |
| F-CTRL-SO3 | ODF-averaged E₂ fraction at t = 0 = 0.4 for every mode (max dev 5.0×10⁻¹⁶); r_agg(0) = 0 exactly — the SO(3) identity, honoured |
| F-CTRL-TEX | synthetic hex at t = 1: r_agg = 2.50×10⁻³ ≫ τ_agg — the instrument sees a split when there is one |
| PIN-A2AGG | worst relative residual **6.3×10⁻¹⁴** against the banked a₂^agg = D2 quartet, D(0), I₀, I₂, V_T, V_L (X-3/X-4) — the from-scratch Born kernels (SO(3) grid (16,10,16), 8-point μ-GL) reproduce the G-S2C1 P2 machinery to machine precision |
| F-CTRL-POL | helicity +1 vs −1 self-energies: 0; helicity vs polarization-average: 4.8×10⁻¹⁶ — the order-consistent stand-in for F-MS-2 (an algebraic identity for a real symmetric scattering kernel, as expected) |
| F-CTRL-ADMIX | 0 — **see H-MS-3: as coded, tautological** |
| PIN-VRH0 | worst 1.4×10⁻¹⁴ against the banked general Voigt/Reuss moduli (X-4 `*_gen`) |
| PIN-HS0 | worst 1.6×10⁻¹² against the banked cubic Hashin–Shtrikman bands (X-5): step [60.196098808, 61.904684503], gem8 [84.855804968, 89.432106200]; the Walpole machinery with optimized isotropic references reproduces the classical bounds |

Hex HS bands (computed, A-2.3; no banked reference among the pin sources): step G_HS [70.40653, 70.97359] (VR bracket [68.69, 73.06]); gem8 [99.81834, 101.05874] (VR [96.63, 105.04]).

## 2. Phase 1 — single crystal (quadrature 64×128; doubling residual 1.8×10⁻¹⁵ ≤ 1×10⁻¹⁰)

| Key | r_xtal(S2-E₂) | r_xtal(S2-h) | ⟨λ_L⟩ (qT) | max λ_L @ branch | Cov_EM(λ,v) | E₂ share qSH/qSV(qT1/qT2)/qL |
|---|---|---|---|---|---|---|
| hex_step\|a | −2.7967×10⁻² | −1.1129×10⁻³ | 4.81×10⁻³ | 3.35×10⁻² @ qSV | +3.64×10⁻² | 0.833 / 0.165 / 0.002 |
| hex_step\|b | −2.7947×10⁻² | −1.1128×10⁻³ | 4.81×10⁻³ | 3.35×10⁻² @ qSV | +3.64×10⁻² | 0.833 / 0.165 / 0.002 |
| hex_gem8\|a | −3.9339×10⁻² | −1.3149×10⁻³ | 4.95×10⁻³ | 3.51×10⁻² @ qSV | +5.13×10⁻² | 0.833 / 0.165 / 0.002 |
| hex_gem8\|b | −3.9352×10⁻² | −1.3149×10⁻³ | 4.95×10⁻³ | 3.51×10⁻² @ qSV | +5.13×10⁻² | 0.833 / 0.165 / 0.002 |
| cubic_step\|001 | −1.7297×10⁻² | −1.5164×10⁻³ | 8.39×10⁻³ | 3.87×10⁻² @ qT2 | +4.90×10⁻² | 0.449 / 0.543 / 0.009 |
| cubic_step\|111 | **+1.1531×10⁻²** | −1.5164×10⁻³ | 8.39×10⁻³ | 3.87×10⁻² @ qT2 | +4.90×10⁻² | 0.533 / 0.459 / 0.008 |
| cubic_gem8\|001 | −2.0842×10⁻² | −1.8451×10⁻³ | 9.31×10⁻³ | 4.33×10⁻² @ qT2 | +7.22×10⁻² | 0.449 / 0.542 / 0.010 |
| cubic_gem8\|111 | **+1.3895×10⁻²** | −1.8451×10⁻³ | 9.31×10⁻³ | 4.33×10⁻² @ qT2 | +7.22×10⁻² | 0.533 / 0.458 / 0.009 |

Readings (R2): the E₂ descriptor is direction-selective as designed — on hex it sits 83% on the qSH branch (its in-plane-polarized basal support), and its sphere-weighted speed is 2.8–3.9% below the EM species' (negative, order 10⁻², H-MS-1 concordant); the hex (a)/(b) arms agree to 2×10⁻⁵ in r (the tetragonal-form/C66 disposition is immaterial here). The admixture-controlled descriptor S2-h splits at 10⁻³, with the sign of −Cov_EM(λ_L, v) and within 25% of the first-order value −Cov/(3⟨v⟩) (hex: −1.43×10⁻³ vs −1.11×10⁻³) — the split is admixture-sourced (H-MS-2 concordant). Cubic: the sign of r_xtal(S2-E₂) flips with the elected axis (⟨001⟩ negative, ⟨111⟩ positive) — the descriptor's axis is a genuine choice on a cubic lattice, recorded, not resolved.

## 3. Phase 2 — aggregate

| Key | v_T(Hill, t=0) | HS band | S_t(E₂) | κ₂(E₂) Hill | κ₂(E₂) HS-mean | κ₂(h) | halving dev | r_agg(t=1) |
|---|---|---|---|---|---|---|---|---|
| hex_step\|a | 8.41906 | [8.39086, 8.42458] | +1.6×10⁻¹³ | **−1.43946×10⁻³** | −1.42819×10⁻³ | −2.0×10⁻⁶ | 4.3×10⁻⁶ | −1.440×10⁻³ |
| hex_step\|b | 8.41928 | [8.39108, 8.42480] | +1.6×10⁻¹³ | −1.43870×10⁻³ | −1.42742×10⁻³ | −2.0×10⁻⁶ | 4.3×10⁻⁶ | −1.440×10⁻³ |
| hex_gem8\|a | 10.04172 | [9.99091, 10.05280] | +4.9×10⁻¹³ | **−1.89565×10⁻³** | −1.88530×10⁻³ | −3.2×10⁻⁶ | 7.5×10⁻⁶ | −1.897×10⁻³ |
| hex_gem8\|b | 10.04155 | [9.99074, 10.05263] | +4.9×10⁻¹³ | −1.89614×10⁻³ | −1.88580×10⁻³ | −3.3×10⁻⁶ | 7.5×10⁻⁶ | −1.898×10⁻³ |
| cubic_step\|001 | 7.79905 | [7.75861, 7.86795] | +3.9×10⁻¹⁶ | +3.1×10⁻¹⁵ | −4.6×10⁻¹⁶ | −3.5×10⁻¹⁷ | 4.8 (0/0) | −1.1×10⁻¹⁶ |
| cubic_step\|111 | 7.79905 | [7.75861, 7.86795] | +4.1×10⁻¹⁶ | −1.7×10⁻¹⁶ | +3.7×10⁻¹⁵ | +1.7×10⁻¹⁵ | 37 (0/0) | −2.2×10⁻¹⁶ |
| cubic_gem8\|001 | 9.30790 | [9.21172, 9.45685] | +2.3×10⁻¹⁶ | −1.5×10⁻¹⁶ | −2.9×10⁻¹⁶ | +1.5×10⁻¹⁵ | 37 (0/0) | −2.2×10⁻¹⁶ |
| cubic_gem8\|111 | 9.30790 | [9.21172, 9.45685] | −1.2×10⁻¹⁵ | +1.3×10⁻¹⁶ | −4.2×10⁻¹⁶ | 0 | 37 (0/0) | +2.2×10⁻¹⁶ |

λ_L in the aggregate: 10⁻³⁰ at t = 0 (isotropy), 1.0–1.5×10⁻⁵ at t = 1 on hex (O(t²), H-MS-4 concordant), 10⁻³⁰ at every t on cubic.

**Findings.**
- **First-order protection CONFIRMED on every key and both arms: |S_t| ≤ 4.9×10⁻¹³** (F-MS-3 SILENT by thirteen orders). The species split under texture is second order, r_agg(t) ≈ κ₂ t², with the cubic fit residual 3–7×10⁻¹¹ on the memo basis and the 4-term and half-window fits agreeing to ≤ 7.5×10⁻⁶.
- **The delivered constraint curve (hex stacking branch): κ₂(S2-E₂) = −1.439×10⁻³ (step) / −1.896×10⁻³ (gem8)** under Hill; the HS-mean scheme agrees to 0.8% — the split is not an averaging-scheme artifact. Sign matches r_xtal(S2-E₂) (H-MS-3 concordant on hex). At full l = 2 texture (t = 1) the species split is 1.4–1.9×10⁻³; at t = −0.5, 3.6–4.7×10⁻⁴. κ₂(S2-h) = −2 to −3×10⁻⁶ — the admixture-controlled split is three orders smaller, O(t³)-class.
- **Cubic l = 2 texture NULL (a structural finding, R1-machine with R2 reading):** on both cubic configurations and both descriptor axes, the textured aggregate tensor is *identical* to the untextured one (max |⟨C⟩_{t=1} − ⟨C⟩_{t=0}| ≈ 10⁻¹², post-hoc diagnostic) and every species quantity is zero to rounding. Reason: the l = 2 harmonic summed over the octahedral orbit of a cubic grain's axis vanishes (Σ over the three orthonormal ⟨001⟩ directions of P₂(n̂·ẑ) = 0; likewise for ⟨111⟩), so a cubic crystal carries no l = 2 texture coefficient — the first texture a cubic aggregate can feel is l = 4. The species-universality identity is therefore **exact to all orders in an l = 2 fiber texture on the fcc stacking branch**, and the hex branch's κ₂ is the only texture constraint curve this family delivers. E-MS-5's registered l = 4 successor arm is where the cubic branch's first constraint curve would come from. H-MS-3 and H-MS-5 are NOT concordant because of this (their cubic clauses presupposed a non-zero cubic κ₂) — a prediction refuted by symmetry, recorded as such.

## 4. Hypotheses (compare step, run last): 3/5 concordant

H-MS-1 OK · H-MS-2 OK · H-MS-3 MISS (cubic clause; see the cubic null) · H-MS-4 OK · H-MS-5 MISS (moot: cubic κ₂ ≡ 0). The two misses are the same finding.

## 5. Honesty items (chat)

- **H-MS-2 — halving criterion undefined at κ₂ = 0.** A-2.4 defined `halving_dev_kappa2` as a relative change of κ₂; on the cubic keys κ₂ ≈ 10⁻¹⁵ and the ratio is 0/0 (values 4.8 and 37). The frozen comparator's per-leg check `halving_dev ≤ 1×10⁻⁴` will therefore MISS on the four cubic keys on **both** legs (the chat-vs-chat sanity run shows exactly these 8 items plus the 2 expected INDEPENDENCE items, 405/415 PASS). Pre-classified definitional (the G-S2C1-W H-W-6 class): the fix is a floored denominator max(|κ₂|, κ₂_abs_floor = 10⁻⁶), already the semantics of the frozen two-leg κ₂ tolerance. The checkpoint of record is left as computed; comparator v1.1 with the floored rule is proposed for the author's election at the S9 step, to be frozen before any re-emission (the G-2a-L1 precedent). Nothing verdict-bearing depends on it.
- **H-MS-3 — F-CTRL-ADMIX as coded is a tautology.** The control was implemented as "projected speeds over projected speeds − 1" and returns 0 identically; it tests nothing. The substantive admixture check is H-MS-2 (sign and magnitude of r_xtal(S2-h) against −Cov_EM(λ_L, v)/(3⟨v⟩), concordant on all eight keys); F-CTRL-ADMIX's `passed = True` is disclosed as vacuous, not as evidence. The CC leg is asked to implement the control as the memo states it (eigenvectors replaced by their transverse projections on the quasi-transverse branches, then r_xtal(S2-h) recomputed) and to report the number.
- **H-MS-4 — pre-lock catch during instrument build (no artifact consumed it):** the first S4 self-test assumed the banked hex tensors are transversely isotropic; they are tetragonal-form (C66 free), so the qSH branch decouples exactly only on the symmetrized arm (b). Labels on arm (a) are by maximum overlap with ẑ × k̂; the species means are label-free, and the (a)/(b) arms agree to 2×10⁻⁵.
- T1: 4 + 1 numeric formatting collisions logged on the checkpoint/compare (bare numeric base patterns inside longer float literals — the contextual rule working; none a forbidden reference).

## 6. Registers (chat-side; nothing folded)

Every number R1-machine (single-leg until CC). Readings R2 conditional on E-MS-1(a), the untextured import, K = ∅, the kernel election, and A-2.3 (HS operationalization): (i) species universality is an identity on the untextured aggregate (control-verified); (ii) it is protected to first order in an l = 2 fiber texture on every configuration, and to all orders on the cubic branch; (iii) the hex branch's second-order split is κ₂ t² with κ₂ = −1.44×10⁻³ / −1.90×10⁻³ — the delivered constraint curve on the texture import; (iv) the admixture maps λ_L (⟨λ_L⟩ 5–9×10⁻³, max 3.4–4.3% on the qSV/qT2 branch) are the single-crystal differentiator from the isotropic-continuum lane (Danielewski, §3.2). No observable, no bridge, no SI value, no evaluation against any bound; no kill claimed or possible here.

## 7. Estate

| Artifact | md5 | Size |
|---|---|---|
| `staging_memo_G_MSCS1_v2.md` | `3f30262eaec461fb5fd3202835f7de37` | 34,837 B |
| `G_MSCS1_LOCK_RECORD.md` | `3dbe953badb6c030ef1d449adbac2044` | 7,289 B |
| `g_mscs1_schema_v1_0.json` | `76a42db3fd6ad82e485752bc2ddb24d5` | 3,906 B |
| `g_mscs1_compare_v1_0.py` | `22432b292ae0a9d5c91a6cb7aa67502f` | 18,541 B |
| `tools/t1/T1_forbidden_G_MSCS1.txt` / `t1_scan.py` / `T1_base_author_20260919.txt` | `fef28271…` / `6b862900…` / `05302210…` | 1,433 / 1,967 / 143 B |
| `g_mscs1_chatleg.py` | `db5f51dd9ef7f54dd0826991d594681b` | 34,606 B |
| `g_mscs1_chatleg_checkpoint.json` | `c04c0b8ea34cfe60f231aa06828e6ce4` | 33,289 B |
| `g_mscs1_chatleg_compare.json` | `7b933c08b92d57b9523f2cee4ff076ba` | 3,277 B |
| `run_chatleg.log` | `79737687c857153c07f3f9e2baf3c26b` | — |
| pin sources X-1 / X-3 / X-4 / X-5 | `200e7a8b…` / `aaae2067…` / `ec87e42f…` / `df413a7c…` | 2,767 / 11,454 / 8,140 / 1,920 B |
