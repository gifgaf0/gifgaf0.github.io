# GATE G-TSH2 — PRE-REGISTRATION INSTRUMENT
**STATUS: LOCKED (July 19, 2026). A-1 AUTHORIZED and A-2 ELECTED by the author, July 19, 2026. The md5 of this file is the lock; it is recorded in the execution report and the CC hand-off packet (the file itself cannot contain its own hash). Thresholds and all declarations below are immutable (T3). No gate quantity was computed before this lock.**
**Base:** SQT Master Ledger V4.68 CANONICAL · **Staging memo:** G_TSH2_STAGING_MEMO_v1.md, md5 09c9cc3805a33d0f51011deca2eeb3e9 · **Draft:** G_TSH2_PREREGISTRATION_DRAFT.md, md5 8f53c0e3fc7228b0e55806881ea0cb1e · **Elections (author, July 19):** E1(b as amended by A-1), E2(a), E3(staged θ), E4(a), E5(a), E6(G-TSH2). A0 confirmed author-side on Rakic–Ho–Lee arXiv:2403.13727 (no kernel-shape sweep of the modulus ratio).

---

## §A. Amendments (pre-lock; both resolved)

**A-1 — AUTHORIZED (author, July 19, 2026).** The E1(b)-elected Gaussian probe is analytically Q+ (Û(k) = πgR²·exp(−k²R²/4) > 0; the uniform state is the global GP minimizer at every g; first-passing g nonexistent). Substituted probe: the compact **parabolic cap** U(r) = g·(1−(r/R)²)·θ(R−r), Û(k) = 4πgR²·J₂(kR)/(kR)², negative lobes guaranteed, diagnostic g_c ≈ 105.5. The staging error is logged to the honesty ledger as **S-1** (Claude, staging memo v1).

**A-2 — ELECTED (author, July 19, 2026).** Arm-map symmetry tightened: KERNEL-CLASS-PINNED requires D_X > θ₂; D_X ∈ (θ₁, θ₂] routes to the dead zone. §9 below states the final semantics.

**Pre-lock feasibility diagnostic** (design-level; kernel transforms and spinodal thresholds only; no gate quantity): `gtsh2_feasibility_diag.py`, md5 49b157ba92676f26a5ab7c73bdb24374. Calibration: step g_c = 14.74 < 22 (canonical crystallization consistent); γ=6 g_c = 31.88 < 35 (the recorded G-TSH1 first-passing point sits just above its spinodal). γ=4: g_c = 80.93; γ=8: 22.75; γ=12: 17.78; cap: 105.46; Gaussian: no negative lobe (analytic).

## §1. Question, base, and consumed anchors

**Q:** Classification of the kernel-shape dependence of R_T ≡ c_T/c_L1 on the p6m GP supersolid at fixed lattice class, under the uniform per-kernel first-passing-g convention, into DERIVED-RATIO / KERNEL-CLASS-PINNED / KNOB (arms registered at V4.68 §2.91.I).

**Consumed read-only anchors (V4.68 §2.91.I; entered as-is, never re-measured, never re-tuned):**
- Step kernel (γ→∞ family anchor), canonical point g = 22: a* = 1.4575, μ = 55.854, c₂ = 1.765, c_T = 5.7749, c_L1 = 11.0453, R_T = 0.52284. Axis-(i) pool across g = 22→44: R_T ∈ {0.5228, 0.5286, 0.5348, 0.5436}.
- γ = 6 kernel at first-passing g = 35: R_T = 0.4988.

## §2. Kernel set (post-A-1)

| ID | U(r)/g (R = 1) | Family | Role | g-grid (step 5) | tier-2 at |
|---|---|---|---|---|---|
| K1 | θ(1−r) | γ-family (γ=∞) | anchor, read-only | — | — |
| K2 | 1/(1+r⁶) | γ-family | anchor, read-only | — | — |
| K3 | 1/(1+r⁴) | γ-family | new | 85…145 | g*, g*−5 |
| K4 | 1/(1+r⁸) | γ-family | new | 25…85 | g*, g*−5 |
| K5 | 1/(1+r¹²) | γ-family | new | 20…80 | g*, g*−5 |
| K6 | (1−r²)·θ(1−r) | compact cap [A-1] | cross-family probe | 110…170 | g*, g*−5 |

ρ₀ = 1 (cell mean density), m = 1, ħ = 1, substrate units throughout (T4). The declared import set of this gate is exactly {kernel form ∈ table, g per §3, ρ₀ = 1}; the kernel-set extension is the gate's one named new import. Anything consumed outside this set is an undeclared import and voids the affected result.

## §3. First-passing convention (E2(a), operationalized)

Per kernel, g scanned on its grid ascending. At each g: a\*-scan (§4) with tier-1 depth. **CERT(g)** = (i) cell-relaxed p6m state with E/N ≤ E_unif/N − 10⁻⁵·|E_unif/N| at the same mean density; (ii) density contrast (max−min)/mean ≥ 0.5; (iii) interior a\*-minimum (not at a bracket edge); (iv) no BdG instability on the measured k-set (F-NEG). **g\*** = smallest grid g passing CERT, then tier-2 confirmed: deep re-solve at g\* from 3 independent random-phase inits (all must re-certify, a\* agreeing to 0.5%) and deep re-solve at g\*−5 (must fail CERT). Tier-1 = 4,000 imaginary-time steps (dt = 2×10⁻³) from a triangular-seeded + 10% noise init per a-point; tier-2 = 20,000 steps + polish. If the lowest grid point passes, the grid is extended downward in steps of 5 (bounded g ≥ 5) until a fail brackets first passage; any extension is logged as a deviation. If no grid g passes: **FP-NONEXIST(p6m)** recorded; kernel excluded from pools with flag. If K6 flags out, D_X is unavailable and the reachable arms restrict to {KNOB, UNDERDETERMINED-2} with the restriction recorded.

## §4. Ground state numerics (chat leg)

Primitive rhombic cell a₁ = (a, 0), a₂ = (a/2, √3a/2); Fourier pseudospectral n = 32 (convergence at n = 40); one droplet site per cell. a\*-scan: 13 points over a_pred·[0.88, 1.12] (a_pred from the diagnostic roton k), parabolic refine ×2. Polish: gradient/imaginary-time to GP residual ‖(−½∇² + Φ − μ)ψ‖₂/‖ψ‖₂ ≤ 10⁻⁸ target; a floor above 10⁻⁶ triggers an honesty entry and a Ward re-check before any use. Φ = U ⋆ |ψ|² by FFT with Û from the analytic forms (K1, K6) or a precomputed radial table at 10⁻⁶ accuracy (K3–K5). Translation re-centering of the droplet to the origin (an exact symmetry operation) is permitted numerics.

## §5. BdG and the F9 Ward gate

Dense plane-wave build of L_k = −½(∇+ik)² − μ + Φ and the exchange operator X_k ([X_k f] = ψ·(U ⋆_k (ψf))); the Bogoliubov problem solved in the Hermitian-pencil form (L+2X_k)η = ω²·L_k⁻¹η (equivalent to the L^{1/2}(L+2X)L^{1/2} form); lowest bands retained; ω = √λ; any λ < −10⁻⁸·μ² at k ≠ 0 ⇒ **F-NEG** (state not ground; CERT fails at that g). **F9 (permanent, per kernel, pre-verdict):** r_W = ‖(L₀+2X₀)∂ψ₀‖₂/(‖∂ψ₀‖₂·μ) ≤ 5×10⁻³ for both ∂_x and ∂_y, checked after polish and before any speed is read. F9 fire ⇒ halt, honesty entry, cure by polish only (no parameter motion), recompute; a contaminated pass is voided (the H3 protocol).

## §6. Branch classifier

k along Γ→M lies in a p6m mirror line σ; modes classified by σ-parity on the grid: **odd ⇒ transverse (shear)**; even gapless pair sorted ascending ⇒ (c₂, c_L1). f_T = odd-projection fraction of the T-labelled mode ≥ 0.95 (**F-CLS**). Secondary witness (reported, non-falsifying): density weight w_ρ = |cell-mean of ψ₀(ũ+ṽ)|² — near-zero for T. The same classifier runs on Γ→K with its mirror.

## §7. Estimators (locked)

k-sets: f_j = j/40 of |Γ→M| and of |Γ→K|, j = 1…8. Speed: zero-intercept least squares of ω on k over j = 2…6 of the labelled branch. Exponent: log-log fit on W1 = {2…5} and W2 = {4…8}; **F-LIN**: p ∈ [0.90, 1.10] on both windows for the T and L1 branches. **F-ISO**: |c(ΓM) − c(ΓK)|/mean ≤ 2% per branch; fire ⇒ that kernel EXCLUDED with honesty entry; ≥2 exclusions ⇒ gate returns to author, no verdict. **F-CONV**: n = 40 recheck at j ∈ {3, 5}, both directions: the 4-point zero-intercept speed proxy per branch changes by |Δc|/c ≤ 10⁻³. R_T(kernel) = c_T/c_L1 at g\*, mean of the two directions.

## §8. W-μ static witness (E4(a); R2 report, non-falsifying)

Simple shear of the cell: a₂ → a₂ + ε·(a₂·ŷ)x̂, ε ∈ {±0.005, ±0.01}; fixed N; re-relax; μ_s = [E(+ε) + E(−ε) − 2E(0)]/(A_cell·ε²) per ε-pair, averaged. Report per kernel: (μ_s/ρ_tot) vs c_T² and their ratio; ratio outside [0.5, 2] flagged for the record (supersolid ρ_n/ρ_s partition is exactly the open Rakic–Ho–Lee territory; no theory relation is locked, nothing falsifies on this witness).

## §9. Pools, arms, verdict (quarantined in arm_mapper, run last; A-2 semantics FINAL)

Pools of R_T values: **P_W** (γ-family) = K1 anchors {0.5228, 0.5286, 0.5348, 0.5436} + K2 {0.4988} + K3 + K4 + K5 (one point each at g\*) — 8 points nominal. **P_X** = P_W + K6 — 9 points nominal. D = max-from-mean over the pool. θ₁ = 3%, θ₂ = 10% (E3, immutable, T3). Arm map:
- D_W ≤ θ₁ ∧ D_X ≤ θ₁ → **DERIVED-RATIO**
- D_W ≤ θ₁ ∧ D_X > θ₂ → **KERNEL-CLASS-PINNED**
- D_W > θ₂ → **KNOB**
- otherwise → **UNDERDETERMINED-2** (dead zone honored on both statistics; the honest exit is the verdict; no re-tuning, no threshold motion, no kernel added post hoc)

## §10. Controls and the T1 grep

**C-NEG:** step kernel at g = 8 (below spinodal 14.74), uniform state: exactly one gapless branch, zero odd-parity gapless modes — must pass. **C-POS:** classical nearest-neighbor central-spring triangular lattice, dynamical matrix in-file: analytic c_T/c_L = 1/√3 recovered to 10⁻⁶ and the polarization classifier labels T correctly — must pass. **T1 self-grep at every invocation**, both legs, all computation files: {299792458, 2.9979, GW170817, 1.6180, 0.6180, 137.03} — any hit halts the leg (self-trip logged, H1 protocol; the grep patterns are assembled from fragments in-source so the guard cannot self-trip). No physical-c statement, no observable, no KC anywhere in the gate.

## §11. Legs, D5, comparison, S9

Chat leg: this instrument, from scratch (`g_tsh2_chatleg.py`). CC leg: **full-from-scratch (E5(a))** — own cell size, truncation, schedules, classifier, reducer; the gz1/tsh1 lineage may not be imported. **D5 fix, first application: this locked file travels in-band to CC with its md5; CC verifies byte-identity before Phase 1.** Comparison (verdict-level, quarantined): **C1** per-kernel g\* exact grid match; **C2** a\*, μ per kernel ≤ 0.3%; **C3** c_T, c_L1 ≤ 0.5%; **C4** R_T ≤ 0.5%; **C5** D_W, D_X within 0.3 pp and arm verdict identity; **C6** falsifier/control state identity (F9, F-LIN, F-ISO, F-CONV, F-CLS, C-NEG, C-POS, FP flags). Any breach ⇒ **S9** counter-cross-check protocol before any fold.

## §12. Consequence routing (pre-declared)

- **DERIVED-RATIO** → the V4.68-deferred sub-classification (DERIVED-RATIO vs DERIVED-OF-LOCATED-IMPORT) activates as the next registered successor; R_T becomes a candidate class invariant of the p6m GP supersolid, substrate units only.
- **KERNEL-CLASS-PINNED** → any downstream use of R_T carries the kernel-class choice as a named import (M.REL ontology axis).
- **KNOB** → any downstream physical use of R_T requires a named kernel-selection import; no universality claim survives.
- **UNDERDETERMINED-2** → a kernel-set-extension successor is registered, unopened.
All arms: no KC evaluated; no observable; the transverse scale import (any physical c_T = c statement) stays named and unexercised (M.CW/T4); nothing prior modified; Paper IIA §3–§4, T1–T5, the §2.91.H retired estate, §2.90, μ_n, and the gauge-paper §7.4 firewall untouched. **§2.52 Open 3: frozen per standing instruction — not opened, not annotated.**

## §13. Order of operations (binding)

Locked → in-band transmission to CC with md5 → chat-leg execution Phases: P0 controls (C-NEG, C-POS) → P1 per-kernel g-scan/CERT/g\* → P2 per-kernel BdG speeds under F9/F-LIN/F-ISO/F-CONV/F-CLS → P3 results frozen to JSON → P4 arm_mapper (first appearance of θ in any executed path) → report → CC leg → C1–C6 → S9 if needed → author fold authorization → V4.69 candidate.
