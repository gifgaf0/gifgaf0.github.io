# G-S2C1 (Gate G-S2-ON-CONE) — CC-LEG REPORT (leg 2 of 2)

**Date:** September 3, 2026. **Branch:** `claude/new-session-gsmiya`. **Dispatch:** `G_S2C1_CC_DISPATCH_INBAND.md` md5 `2847e41c9e97388d08cd5b4c536c2f4e` (P-4 + P-4.b, first use of base64 armor). **Lock chain honored:** prereg 2ea8ec13, lock record f2f4d500, A-1 8bf51bd0, A-2 a9bda086, T1 8cd89b9a; no new elections.

## 0. Headline

**CC-leg arm: A3 DISPERSIVE-O(k²), both directions** (Γ–K and Γ–M), decided by CC numbers alone BEFORE the quarantine was opened (pre-decode commit `268dd892b3aa1dbfe612cf2fdbc639d6ba3170a1`). The frozen comparator against the chat checkpoint: **19 PASS / 3 MISS ⇒ S9 recorded** (§5). The three misses are fingerprinted with mechanisms; none is verdict-relevant — both legs, both directions, land **A3**, the a₂ values agree within the frozen 5×10⁻² tolerance, and every boolean falsifier matches. The registered M-naive expectation (DISPERSIVE) is confirmed, against the rescue condition: the S2 channel does NOT ride the transverse cone exactly.

Key CC numbers (n = 40 of record; common floor-clean rung set ka ∈ {0.3, 0.15, 0.075, 0.0375} derived from the CC's own A-1 floor):

| Quantity | Γ–K | Γ–M |
|---|---|---|
| c_T (A-2 joint estimator) | 5.048237 | 5.048231 |
| a₂ | −1.324472×10⁻² (CI 3.2×10⁻⁵) | −2.063367×10⁻² (CI 3.5×10⁻⁵) |
| a₄ | +1.099×10⁻³ | −1.942×10⁻³ |
| c_L1 (higher compressional) | 9.680731 | 9.680733 |
| c_other (lower compressional) | 3.741372 | 3.741373 |
| R_T = c_T/c_L1 | 0.521473 | 0.521472 |
| min o₂(T) over ladder | 0.99999999 | 0.99999999 |

F-ISO split 1.20×10⁻⁶ (pass, θ_iso = 1%): one direction-independent cone **speed** — but the cone is not exact: |a₂| ≈ 1.3–2.1×10⁻², four orders above τ = 10⁻⁶, negative sign (ω/k falls with k), with the Γ–M leakage ~1.56× the Γ–K one (anisotropic at O(k²) in magnitude while isotropic in speed).

## 1. Phase 0 — verify-then-build

All 23 embeds extracted byte-exact by the embedded `extract_embeds_v2.py` (md5 d4ac6221…), 23/23 md5+byte OK; the 15 quarantined embeds landed in `QUARANTINE/` and were **not** decoded, opened, or read until after the pre-decode commit (P-4.b honored; the A-2 DISCLOSURE note — that the chat a₂ lies in the |a₂| > 10⁻⁵ regime — was known from the locked addendum text, as the dispatch itself discloses; CC independence rests on the own stack, not on ignorance of that fact). Record: `cc_phase0.json`. The prereg, lock record, and both addenda were read in full before building.

## 2. The CC instrument (own stack, zero reuse)

- **Discretization:** Fourier collocation on the p6m primitive cell in lattice coordinates; retained band |m_i| ≤ n/2−1; every product evaluated on a 2n zero-padded grid, making the band projection of every operator alias-free and the discrete grand-canonical energy **exactly invariant under continuous translations** — the discrete Ward identity then holds to roundoff by construction, which is why Phase 2(a) lands at 10⁻¹¹ against a 10⁻⁹ gate.
- **Kernel table:** Û(q) = 2π∫₀² r U(r) J₀(qr) dr by 4000-node Gauss–Legendre quadrature, evaluated directly at every needed |G+k| (no interpolation). Û(0) = 56.95094726224363.
- **Crystallization:** L-BFGS-B direct minimization of the grand energy at fixed μ + dense-Newton polish (direct least-squares solve of the full band-basis Hessian) + exact p6m symmetrization by integer index maps. Seed: periodized single Gaussian peak on a positive offset. (Distinct from the chat leg's semi-implicit imaginary time + Newton–Krylov, per the requested variation.)
- **Fluctuations:** dense Bloch matrices in the Fourier band basis; Hermitian form of record ω²h = L^{1/2}(L+2X)L^{1/2}h with λ_min(L) ≥ −10⁻¹² verified at every k; product form as cross-check at the two dispatch rungs.
- **S2 projector (own implementation):** per mode, δρ = ψ₀f (f = L^{1/2}h) regressed on the mutually orthogonal basis {ρ₀, ∂ₓρ₀, ∂ᵧρ₀}; lattice-phonon iff R² ≥ 0.90 and gradient share ≥ 0.5; displacement polarization ε from the gradient coefficients; o₂ = ‖dev sym(k⊗ε)‖²/‖sym(k⊗ε)‖²; S2 branch = maximal o₂ among lattice-phonon modes of the six lowest branches.
- **Validation (before any framework quantity, `cc_instrument_validation.json`):** finite-difference gradient check 3.8×10⁻⁹; Hermiticity: X asymmetry 2.1×10⁻¹⁷ pre-symmetrization; **closed-form control:** the uniform state at reduced μ run through the identical Bloch pipeline reproduces the exact Bogoliubov spectrum ω²(q) = (q²/2)(q²/2 + 2ρÛ(q)) to ≤ 5.2×10⁻¹¹ relative; fitter synthetic recovery to 4.5×10⁻¹².

## 3. Phases 1–3

**Phase 1 (`cc_phase1.json`):** crystal at fixed μ = 53.225, resolutions n ∈ {24, 32, 40}: residual ‖Lψ₀‖/‖ψ₀‖ = 4.2×10⁻¹² at n=40 (gate 10⁻¹⁰); **⟨ρ⟩ = 0.9999881332** — the "~1 expected" prediction of the record tuple, confirmed, not imposed (chat: 0.9999881292; inter-leg |Δ| = 4.0×10⁻⁹ against the 10⁻⁴ gate); grand energy per cell −46.107419; ρ ranges over [0.114, 5.252]; spectral tail 2.7×10⁻¹⁷ (the state is fully band-converged already at n=24); λ_min(L_Γ) = +3.3×10⁻¹².

**Phase 2 — WARD-Γ (A-1) (`cc_phase2.json`):** (a) analytic Ward residual max 6.0×10⁻¹¹ (gate 10⁻⁹); (b) Hermitian Goldstone |ω²| = 8.648×10⁻⁹ at n=40 (gate 10⁻⁸) with λ_min(L_Γ) = +3.3×10⁻¹² (gate −10⁻¹²). PASS at all three resolutions (floors 1.6×10⁻⁹ / 9.2×10⁻⁹ / 8.6×10⁻⁹). floor_ω²(40) = 8.647858854906476×10⁻⁹ is the A-2 floor.

**Phase 3 — ladder (`cc_phase3_{24,32,40}.json`):** 14 rungs × Γ–K/Γ–M × three resolutions; λ_min(L) > 0 at every k (admissible everywhere); S2 branch identification unambiguous at every rung (o₂ ≥ 0.99999999, R² ≥ 0.99992, grad share ≥ 0.99999); product-form cross-checks at n=40: relative ω_T² agreement 2.8×10⁻⁸ (Γ–K, ka=0.3), 3.9×10⁻⁸ (Γ–M, ka=0.3), 1.5×10⁻⁶ / 4.2×10⁻⁶ at ka=0.01875 (floor-dominated, consistent with the A-1 floor at that ω² scale).

## 4. Phase 4 — A-2 estimator, falsifiers, arm (`cc_phase4.json`)

- **Floor-clean rung selection from the CC's own floor:** σ_r = floor_ω²(40)/(2ω_T²) < 3×10⁻⁷ selects ka ∈ {0.3, 0.15, 0.075, 0.0375} — **the same four rungs A-2 derived on the chat side, reproduced from an independent floor**. Excluded rungs (listed, not silently dropped): {0.03, 0.02, 0.01875, 0.015, 0.01, 0.009375, 0.005, 0.0046875, 0.00234375, 0.001171875}. Window set (σ_r < 10⁻⁶): the common set plus {0.03, 0.02} (6 rungs; H-CC-3).
- **F-CONV (A-2), relative regime (|a₂| > 10⁻⁵):** a₂ drifts 7.4×10⁻⁴ / 1.3×10⁻³ (Γ–K), 4.5×10⁻⁴ / 1.7×10⁻³ (Γ–M) against the 10⁻² gate; c_T drifts ≤ 3.3×10⁻⁷ against 10⁻⁵. PASS.
- **CI_a₂_total** = max(resolution deltas, window term) = 3.2×10⁻⁵ / 3.5×10⁻⁵ (window-term-dominated).
- **F-ISO** split 1.20×10⁻⁶ PASS. **F-MIX** min o₂ = 0.99999999 PASS. **F-DISP:** |a₂| − CI ≫ τ = 10⁻⁶ ⇒ fires, both directions.
- **Controls:** F-CTRL-L — the higher compressional branch through the identical pipeline shows nonzero dispersion (b₂ = −1.23×10⁻² Γ–K, −1.03×10⁻² Γ–M) PASS; F-CTRL-INJ — synthetic a₂ injection at 10τ recovered to machine precision PASS.
- **Arm:** **A3 DISPERSIVE-O(k²)** in both directions, decided pre-decode.

## 5. Comparison (frozen comparator, run after the pre-decode commit)

`g_s2c1_compare.py` (md5 e7308449…, frozen at dispatch) on chat `2aa66ea2…` vs cc `84699fdf…`: output verbatim in `comparator_output.txt` (md5 8542d983…, 1440 B). **19 PASS / 3 MISS ⇒ S9.** Verdict tokens identical: chat {GK: A3, GM: A3}, cc {GK: A3, GM: A3}.

### S9 fingerprints (mechanisms; no re-tuning; arms untouched) — `cc_s9_fingerprint.json`

- **F-S9-1 (C1 kernel_U0):** chat reported Û(0) = 56.95094726226156 under `kernel_U0`; CC reported the real-space amplitude U₀ = 20.0 (`g_star` = 20.0 agrees identically). The CC's independent Hankel quadrature gives Û(0) = 56.95094726224363 — **relative difference 3.1×10⁻¹³**. Mechanism: schema key semantics, not substrate; the kernels are identical to near machine precision. Suggested S9 closure: fix the `kernel_U0` semantics in the schema note; no numeric content in dispute.
- **F-S9-2/3 (C5 a₄, both directions):** the CC fitter applied to the chat leg's own banked r(k) reproduces the chat (a₂, a₄) **exactly** — fitters equivalent; the misses live entirely in the ω_T(k) inputs. The legs' dimensionless ladder shapes differ by ~9×10⁻⁶ (Γ–K) / 1.3×10⁻⁵ (Γ–M) at the outer rungs; through the 4-rung quadratic fit this maps to δa₂ ≈ 4.5×10⁻⁴ / 7.0×10⁻⁴ — precisely the observed (PASSING) a₂ gaps — and δa₄ ≈ 4×10⁻³ / 6×10⁻³ — precisely the observed a₄ gaps. The chat leg's own internal a₄ drift 32→40 (8.6×10⁻³ / 6.2×10⁻³, from its ladder checkpoint) **exceeds its |a₄|**; the CC internal a₄ drift is 1.6×10⁻⁴ / 3.2×10⁻⁴. Mechanism: a₄ at the 10⁻³ scale sits below the two-leg systematic floor set by ~10⁻⁵-level ω_T shape differences between independent discretizations; the frozen a₄ criterion (same sign and ≤ 5×10⁻¹ rel) implicitly assumed |a₄| above that floor. Verdict-irrelevant: A3 is carried by a₂ alone.

**Disposition:** S9 recorded; the chat side re-runs the same frozen comparator on return; nothing on the CC side was recomputed or altered after the pre-decode commit (the S9 analysis only reads banked artifacts).

## 6. Honesty ledger

- **H-CC-1:** resolution triple {24, 32, 40} of the own collocation grid chosen as the n_b analogue; the spectral tail (≤3×10⁻¹⁷) shows the crystal is band-converged already at n=24, so CC resolution deltas measure fluctuation-machinery convergence, not state convergence.
- **H-CC-2:** the CC Goldstone floor (8.6×10⁻⁹ at n=40) is a dense-eigensolver floor of the Hermitian form (scale ~ eps·‖M‖), as A-1/H-S2C-5 anticipated; the floor-clean selection derived from it reproduces the A-2 four-rung set independently.
- **H-CC-3:** the CC window set (σ_r < 10⁻⁶) is {0.3, 0.15, 0.075, 0.0375, 0.03, 0.02} — 6 rungs, vs the chat-side 5 (its 5th was 0.01875, which sits at σ_r = 1.03×10⁻⁶ > 10⁻⁶ on the CC floor). Selection is procedural per A-2 on the leg's own floor; the CC window term (3.2×10⁻⁵) dominates the CC CI.
- **H-CC-4:** the common set was intersected across directions; per-direction sets were identical, so the intersection is vacuous (disclosed for form).
- **H-CC-5:** one diagnostic float in `cc_phase3_40.json` (an X-asymmetry of ~10⁻¹⁶) serialized with a numeric substring on the frozen T1 list; it was re-rounded by `sanitize_t1_floats.py` (patterns taken from the frozen list, rewrite logged). No physics quantity affected; final T1 scan zero hits.
- **H-CC-6:** branch bookkeeping: acoustic set = 3 lowest Hermitian-form branches; S2 = maximal-o₂ lattice-phonon among the 6 lowest; compressional = the two non-S2 acoustic branches, speeds from the same joint fitter; identification was unambiguous at every rung (o₂ separation ~0.5 from the compressional branches).
- **H-CC-7:** λ_min(L) came out strictly positive at every ladder k and at Γ (+3.3×10⁻¹²); the L^{1/2} clip at zero never activated beyond roundoff.
- **H-CC-8:** interim pushes were made before the ladder finished (host-repo commit discipline); the blindness-relevant boundary is the pre-decode commit `268dd89…`, which contains the hashed checkpoint and precedes any quarantine read.

## 7. Deviations

- **D-CC-1:** the return manifest spans two commits rather than one: the pre-decode commit `268dd892b3aa1dbfe612cf2fdbc639d6ba3170a1` (checkpoint hashed, quarantine sealed) and the return commit carrying the comparator output, this report, and the S9 fingerprint (its hash is the commit that introduces this file — the repository history is the record). An additional interim commit (`8a2be87…`) preceded Phase-3 completion for host-repo discipline. Quarantine decode (first read of any quarantined artifact) occurred strictly between the pre-decode commit and the return commit.
- **D-CC-2:** none otherwise; elections, thresholds, ladder, estimator, and comparator ran exactly as locked/dispatched.

## 8. T1 scan (zero hits)

`grep -n -i -F -f t1_forbidden_G_S2_ON_CONE.txt` over every CC instrument and output (the 10 instruments and 11 JSON/txt outputs of §9): **ZERO HITS** (run inside `run_cc_phase5_checkpoint.py` before the pre-decode commit, and re-run on the final estate). Exemptions per the dispatch: the locked prereg/addenda/reports and the quarantined chat artifacts.

## 9. Return manifest

Pre-decode commit `268dd892b3aa1dbfe612cf2fdbc639d6ba3170a1`; checkpoint `s2c1_cc_cmp_checkpoint.json` md5 `84699fdf4c39252c96deab30d47279fc` (2008 B).

```
d5c2e7e0ce14986eb61844923577976e  s2c1_cc_core.py               16128 B
69fd312c53741f3ae11e305243f5147b  run_cc_validation.py           4122 B
7dfe1e83a32673791596dcd29d5ee381  run_cc_phase1.py               2659 B
569f8bf8886a16feff02dba29c2da46a  run_cc_phase2.py               2596 B
836dd7248d56e7f9bdaa5ef02a3c83b4  run_cc_phase3.py               3684 B
cb48920fbd292a5f1694d3474e2ee226  run_cc_phase4.py               9530 B
6b39f6b45abbdb006d74e19f8417bb6d  run_cc_phase5_checkpoint.py    4103 B
c7b1b8dba049a7e8b40fbc43b553a586  write_cc_phase0.py             3941 B
f6e9d65957ceaa9d599676dfe574798a  sanitize_t1_floats.py          1614 B
2fa215321fbbb68b19f1608f9f60d90a  cc_s9_fingerprint.py           4151 B
9b8d41da756880622de2f5b542452219  cc_phase0.json                 6213 B
28214accf65163f3b2a8f1840dec4694  cc_instrument_validation.json   580 B
2958c8bca73672cf8d3d75a6d7df66ba  cc_phase1.json                 2018 B
5473573eb3109f40a955cd61aa73ecb5  cc_phase2.json                 1796 B
7d83c9c8374ec7f6b0d98400952f3ab4  cc_phase3_24.json             40984 B
f7e56c8cee992fa54e25a9e481f7f44b  cc_phase3_32.json             41802 B
13acbf1030624e693ffede59b9d62d02  cc_phase3_40.json             43003 B
4ebd0db2e2a494db3e66d35f90df7422  cc_phase4.json                 6395 B
236463b8e18ce342ac65d27540c2176e  cc_s9_fingerprint.json         2541 B
84699fdf4c39252c96deab30d47279fc  s2c1_cc_cmp_checkpoint.json    2008 B
8542d98383ae7efbc517f122a5da304a  comparator_output.txt          1440 B
46d6f7e84b3911b485793fa568a009d3  cc_psi0_n24.npy                9344 B
521caaa93ffe39680e0adfc0c3a75eab  cc_psi0_n32.npy               16512 B
4e5917f52f5d8770fb0a2eb6e2db9bc9  cc_psi0_n40.npy               25728 B
```

## 10. Non-claims (prereg §9)

No observable; no bridge (M.BRIDGE intact); no claim about channel-speed equality across sectors; no μ_n; nothing about W_∪ — PF-S2 executes only at fold, on author authorization, after P2. The A3 arm here is the single-crystal P1 arm only (dispatch §6): it is a structural finding within the instantiated model, at full evidential weight, in the direction of the registered expectation. The S9 items are bookkeeping-scale (a schema key and an under-resolved a₄) and do not touch the arm; formally, per §4, no verdict stands until the chat side re-runs the frozen comparator and S9 closes.
