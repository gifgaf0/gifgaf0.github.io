# G-TSH3 chat-leg — honesty/deviation ledger + instrument lock
(running; folds into G_TSH3_CHATLEG_REPORT.md and CC handoff)

Staging memo lock: md5 `dab46b332b83997d34f9e4ca64c07a4d` (author word "Lock", July 21).
Leg md5 history: ee6ad7d3 (lock-time) -> f1f80021 (H-2) -> e91d40bd (H-3) -> **0be61011 (D-2, current)**.

## Honesty entries
- **H-0** — unexplained pre-existing leg file found on disk; removed; leg rewritten from scratch.
- **H-1** — C-POS control fired on finite-q fit; cured with exact q->0 acoustic matrix in-file.
- **H-2** — tabulated-Hankel defect: adaptive quadrature oscillation-unsafe at high k -> garbage table -> spurious short-wavelength attraction -> solver collapse (seed-independent e=3053.417 at gamma8). Caught at P0b' pre-use; no recorded quantity affected; analytic kernels untouched. Fix: Bessel-zero-subdivided 12-pt Gauss-Legendre `hankel_table()`, validated vs analytic step to 8.9e-16; tables renamed `*_v2`; stale npz purged.
- **H-3** — forward-Euler polish spectrally unstable (dt*lam_max ~ 16); diverged to seed-independent attractor whenever L-BFGS exited unconverged. Fix: Sobolev-preconditioned exact-gradient descent, P=(G^2/2+max(|mu|,1))^-1, no Trotter splitting (Ward-safe). Loop inert at-target, so prior step records stand.

## Declared deviations
- **D-1** — speed-fit spacing halved dq 0.04 -> 0.02·(2π/a), anchor-calibrated pre-verdict.
- **D-2** (author-ratified with instrument lock) — random-init amplitude 0.4 -> 3.0; tier-2 rule at fixed (g*, a*): three random-init deep solves, accept iff >=2/3 crystallize (e < e_unif, contrast > 5) and crystallized subset machine-identical (rel spread <= 1e-8); uniform landings logged, never silently dropped. Basin-diagnostic only; accepted states remain unconstrained stationary points at res <= 1e-12. Motivating control: gamma8@20 hex-triad e=34.782937 < e_unif=34.894320, mu rel 1.7e-5 vs frozen anchor.

## AUTH-INST-1 — instrument convention LOCKED (author word "Lock", July 21)
Uniform instrument for every kernel and every point in G-TSH3:
- Δq = 0.02·(2π/a*), forced-origin ω-vs-q fit, j = 2..6, exponent windows W1=j2-4, W2=j4-6, both directions Γ→K and Γ→M averaged; classifier σ-parity via MIR_K/MIR_M.
- **Eddington guard:** no per-kernel or per-point Δq tuning toward anchors. The Δq sweep (dq_sweep.{py,log,json}) is diagnostic-only and closed.

### ANCHOR-SYS (cross-era systematic, quantified)
Static chain reproduces both eras to <=1.3e-4 (a*, mu; Ward/res ~1e-12; n32->40 RT agreement 2.4e-6). Speeds under THIS instrument deviate from frozen-anchor speeds in kernel-dependent directions:
- step@22: cT +0.29%, cL1 +1.07%, RT −0.77% (my RT 0.51880 vs frozen 0.52284)
- gamma8@20: cT −0.29%, cL1 −0.77%, RT +0.49% (my RT 0.48026 vs frozen 0.47791)
No fit convention (origin / free-intercept / ω²-origin / ω²-free) reconciles both; no single Δq reconciles both (sweep: step improves toward dq≈0.03–0.05, gamma8 optimal near dq≈0.015). Attribution: per-era window conventions in the archived TSH1/TSH2 legs (files not on disk). Assigned systematic for cross-era comparison only: ±1% speeds, ±0.8% R_T. Internal comparability of all NEW G-TSH3 points is unaffected (one instrument).
- **BOUNDARY rule:** if D_ext lands within 1% of θ₂=10% (i.e., in [9%, 11%]), flag BOUNDARY and return to author before any verdict.
- **Pre-registered CC cross-check:** CC's from-scratch leg at the same locked convention should land near MY values (step RT ≈ 0.5188, gamma8 RT ≈ 0.4803), NOT the frozen anchors. Two-leg speed comparison is my-leg vs CC-leg; frozen anchors enter D_ext via their recorded R_T values as frozen data, not as re-measurements.

- **H-5** (self-caught pre-use, P2 audit) — leg F-CONV gate was 1e-4; locked memo §6 specifies ≤5e-6. Corrected before any P2 invocation; no recorded quantity affected. Leg md5 after fix recorded in report.
- **D-3** (declared, author-visible) — memo §6 tier-2 machine-identity "≤1e-15 rel" is unattainable at the locked deep-residual target 1e-12 (μ error is linear in solver residual; e quadratic). Operational gate: ≤1e-8 rel on translation-invariant (e, μ) [H-4 comparator]. Observed spreads: gem8 3.8e-14, gem4 4.5e-14, gem3 3.1e-12, cap_p2 4.1e-12 — residual-limited, ≥4 decades inside the gate. Accept/reject outcome is invariant for any threshold in [1e-11, 1e-8]; a literal 1e-15 would fail ALL kernels including the frozen-anchor reproductions, i.e. it gates solver precision, not physics. Flagged to author with veto standing.
