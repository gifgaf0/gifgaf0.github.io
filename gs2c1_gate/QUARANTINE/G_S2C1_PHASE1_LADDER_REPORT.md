# G-S2C1 (Gate G-S2-ON-CONE) — PHASE 1 LADDER REPORT (chat leg, September 3, 2026)

**Lock:** prereg 2ea8ec13; T1 8cd89b9a; lock record f2f4d500; **Addendum A-1 8bf51bd0** (author-authorized, verbatim). Substrate: banked gem8 state (array md5 b27fa004; residual re-verified 1.96×10⁻¹²). Instrument: `g_s2c1_phase1_ladder.py` (derived verbatim from the halted c987a1a6; staged execution; Hermitian form of record, product-form cross-checks at ka = 0.3 and 0.01875). Checkpoint **5ee152fc** (43,647 B); stage files nb24 e4975050 / nb32 3bfdb48e / nb40GK 2b037836 / nb40GM 67946d95; diagnostic analysis bdfd3d01.

## WARD-Γ under A-1: PASS at n_b = 24, 32, 40
(a) analytic-mode Ward residual 2.3×10⁻¹² … 2.3×10⁻¹¹ (≤ 10⁻⁹); (b) Hermitian Goldstone |ω²| 1.2×10⁻⁹ / 3.0×10⁻⁹ / 8.1×10⁻⁹ (≤ 10⁻⁸) with λ_min(L) = +1.6×10⁻¹⁴ at Γ and no λ_min < −10⁻¹² at any ladder or speed-set k (tracked at every solve). Product-form cross-checks: 2.1×10⁻⁹ / 3.5×10⁻⁸ / 3.6×10⁻⁸ (the H-S2C-5 floor, as diagnosed).

## Channel identification and speeds
The S2/quadrupole branch identifies unambiguously: o₂ = 0.99999999 at every rung, both directions (**F-MIX PASS**, θ_id = 0.90). Three gapless branches, k→0: T = 5.04813–5.04820, and the two compressional branches 9.68059 and 3.74136 (substrate units). **F-ISO PASS:** c_T(Γ–K)/c_T(Γ–M) − 1 = 1.3×10⁻⁵ (θ_iso = 1%). Framework-label R_T = c_T/c_L1 = 5.0482/9.6806 = **0.52147** vs the G-TSH3 gem8 record 0.51767 (0.73%; the record is at the first-passing convention, this is the k→0 extrapolation) — the substrate is the framework's.

## F-DISP (E-4 window, E-5 thresholds)
Elected estimator (speed from the small-k set, then r = a₂(ka)² + a₄(ka)⁴), n_b = 40: **a₂ = −1.282×10⁻² (Γ–K; CI 6.8×10⁻³), −1.939×10⁻² (Γ–M; CI 4.4×10⁻³)**; a₄ unresolved (CI ~1). Sign stable at every n_b and in the A-1 floor-weighted fit (−1.284×10⁻² / −1.955×10⁻²). |a₂| exceeds τ = 10⁻⁶ by 10⁴ and its own inflated CI by 1.9× / 4.4×.

**F-CONV at the Phase-0-fixed thresholds: FAIL** (c_T rel 32→40 = 1.2×10⁻⁵ vs 10⁻⁶; a₂ abs 32→40 = 9×10⁻⁴ vs 10⁻⁷). Mechanism, machine-verified: the 32→40 change in r_T is a uniform ≈1.2×10⁻⁵ offset across all rungs from 0.3 to 0.019 — a shift of the speed extrapolated from the small-k set, where the A-1 dense floor is ≈1.5×10⁻⁵ in r — while the T-branch ω at ka ≥ 0.0375 agree across n_b to ~10⁻⁶. DIAGNOSTIC (not the elected estimator): the c-free joint fit on floor-clean rungs (σ_r < 3×10⁻⁷) converges across n_b to ≤ 3×10⁻³ relative — **a₂ = −1.279×10⁻² (Γ–K), −1.993×10⁻² (Γ–M); a₄ = −3.0×10⁻³, −8.3×10⁻³; c_T = 5.04820 / 5.04817** — and the all-rung joint fit at n_b = 40 collapses (−4.8×10⁻³), which is the floor doing exactly what A-1 says it does.

## Arm
- **Mechanical arm at the elected thresholds: A5 INSTRUMENT-LIMITED** (F-CONV clause). The instrument cannot certify a₂ to 10⁻⁷ absolute — a precision designed for the near-cone regime.
- **Substantive chat-leg indication: A3 DISPERSIVE-O(k²)** — the S2 channel of the gem8 p6m supersolid inherits O(k²) dispersion at the 1–2% level, direction-dependent at O(k²) with an isotropic speed, the same pattern as the harmonic p6m control (−1/96 vs −1/32). The registered M-naive expectation (DISPERSIVE) is realized. The verdict is two-leg; nothing here touches W_∪.

**Proposed Amendment A-2 (author's call; not applied):** F-CONV on a₂ regime-appropriate — absolute 10⁻⁷ when |a₂| ≤ 10τ, relative 10⁻² when |a₂| > 10τ; speed reference and convergence assessed on the c-free joint estimator over floor-clean rungs (σ_r < 10⁻⁶), the dense floor carried as the A-1 term. Under A-2 the present ladder is A3 with F-CONV PASS (≤ 3×10⁻³). Under PF-S2, A3 ⇒ W_∪ stays suspended and W_∪′ is re-derived from the a₂ scale — after the CC leg and the aggregate probe.

## Honesty ledger
- **H-S2C-6** the first ladder run was terminated by the sandbox tool time limit at n_b = 40 Γ–M before writing its checkpoint (log preserved: g_s2c1_phase1_ladder_run1_killed.log); a background relaunch did not survive the tool call; the instrument was restructured into stage files (the E8 lesson, again) and re-run whole — every number above is from the staged run.
- **H-S2C-7** the classifier's "L1"/"PH" labels are swapped relative to the G-TSH3 convention (its "L1" is the 3.741 branch); the framework-label R_T is reported alongside; the T channel is unaffected.
- **H-S2C-8** the elected speed-set estimator is floor-sensitive at small ka in a way the Phase-0 control (analytic, floorless) could not reveal; disclosed with the mechanism; A-2 proposed rather than silently switching estimators.

## Readiness for Phase 2/3
- **CC leg (two-leg):** ready to dispatch under P-4 + P-4.b (base64 armor) with the A-1 wording; A-2 should be decided before dispatch so both legs run the same F-CONV clause.
- **Aggregate probe (P2):** inputs in hand (c_T, c_L1, the T-branch a₂/a₄, the banked G-POLY1 Q_T quartet); the Rayleigh grain-scattering instrument needs recovery from the CC repo (not in project knowledge).
