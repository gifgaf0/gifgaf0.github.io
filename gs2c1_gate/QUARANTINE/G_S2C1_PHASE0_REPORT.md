# G-S2C1 (Gate G-S2-ON-CONE) — PHASE 0 REPORT (chat leg, September 2, 2026)

**Lock (byte-verified):** `G_S2_ON_CONE_EXECUTION_PREREGISTRATION.md` md5 2ea8ec13ffa3c32898cc24a3be605c64 (12,984 B) — cmp-identical to the approved staging memo; `t1_forbidden_G_S2_ON_CONE.txt` FROZEN 8cd89b9a82704accd89f7ff6f5e220b4 (144 B, 16 pattern lines); `G_S2_ON_CONE_LOCK_RECORD.md` f2f4d50029fb5be3122a885c48a7e04f (3,009 B; elections E-0..E-8 = §6 defaults, T3; M-naive expectation DISPERSIVE registered pre-data). **PHASE1_AUTHORIZED = False** in every instrument.

## Readiness: HARNESS READY / SUBSTRATE NOT READY

**(B) Instrument validated on an exactly-solvable p6m control** (NN central-force triangular lattice, closed-form dispersion; CONTROL-NOT-VERDICT):
- S2 projector (traceless-strain fraction o₂): T → 1, L → ½ exactly on both mirror lines at every ladder rung — PASS.
- **F-CTRL-L PASS** both directions: the longitudinal branch's known nonzero a₂ recovered to 7.7×10⁻⁹ (Γ–K, a₂ = −11/288) and 3.1×10⁻⁹ (Γ–M, a₂ = −1/32) against independent closed-form series coefficients; c_L = √(9/8) recovered to 10⁻⁶. The elected two-term basis {(ka)², (ka)⁴} on the elected window [10⁻³, 0.3] has a₂ bias ≤ 7.7×10⁻⁹ ≪ τ = 10⁻⁶ — E-4/E-5 adequate.
- **F-CTRL-INJ PASS:** injected a₂ = 10τ = 10⁻⁵ with noise 10⁻⁸ recovered at 1.0036×10⁻⁵ ± 5.3×10⁻⁷ (200 trials; CI95 contains the injection; mean error 3.6×10⁻⁸ < τ).
- Control-T diagnostic (not a verdict): the harmonic p6m lattice has direction-dependent a₂^T (−1/96 on Γ–K, −1/32 on Γ–M) with isotropic c_T — the prereg's F-ISO is on SPEEDS (θ_iso = 1%), and a₂ anisotropy is reported per direction, exactly as registered.

**(A) Substrate diagnostic — the load-bearing Phase-0 finding.** The instantiated crystal in reach (gz1 rebuild, branch claude/new-session-wrjklk @ ae9232e0, MANIFEST-verified: g = 22 soft-disk, n = 64, a* = 1.4576, μ = 55.946, ψ₀ md5 6e88cbd5…) is NOT stationary to the precision an acoustic ladder needs:
- ‖Lψ₀‖/‖ψ₀‖ = 1.27×10⁻¹ (= 2.27×10⁻³ × μ — identical to the rebuild's logged `residual_polished`; a 10⁻⁵ weight leakage into high-L eigenvectors, amplified by the L spectrum).
- Un-clipped product-form BdG, ω² = eig(L(L+2X)): the two translational Goldstone modes sit at **ω² ≈ −2.097** as k → 0 (basis-INDEPENDENT: identical at n_b = 24, 32, 40, 48, 64); the phase mode at −0.025. Ward residual on the translation mode ‖(L+2X)∂ₓψ₀‖/‖∂ₓψ₀‖ = 0.186. Offset ≈ 16.5 × residual.
- Refuted alternatives: aliasing (ψ₀ spectral weight beyond |m| ≥ 16 is 9×10⁻³¹; the grid-consistent X gives the identical Ward residual); kernel mismatch (grid kernel = analytic kernel to 0.0).
- The recovered `gz1_core.BdG.omegas` Hermitian form clips λ(L) ≥ 0 before L^{1/2}, which converts this offset into **spurious exact zero modes** (0, 0, ~10⁻⁵ from ka = 0.005 to 0.08) — the instrument's F-CTRL-L branch had zero extrapolated speed, which is how the finding surfaced (the harness halted on the resulting division by zero; the halt is the discovery path).
- **Phase-1 prerequisite (fixed here per E-5 "F-CONV thresholds fixed at Phase-0 close"):** re-crystallize at the elected gem8 kernel (E-3) to ‖Lψ₀‖/‖ψ₀‖ ≤ 10⁻¹⁰ and verify WARD-Γ: |ω²_Goldstone(k→0)| ≤ 10⁻⁸ (substrate units) in the un-clipped product form BEFORE any ladder point is computed; the acoustic ω² at the bottom rung (ka = 1.17×10⁻³, k = 8.0×10⁻⁴/a*) is O(10⁻⁶–10⁻⁵) for c = O(1–3), so 10⁻⁸ is a 1% floor. Speed convergence in n_b ≤ 10⁻⁶ relative; a₂ convergence in n_b ≤ 10⁻⁷ absolute. The Hermitian L^{1/2} form is admissible only once λ_min(L) ≥ −10⁻¹²; otherwise the product form is the form of record.

**(C)** F-CTRL-INJ as above — PASS.

## Honesty ledger (Phase 0)
- **H-S2C-1** the harness header cited a superseded lock-record hash (32a99a3d; the record was re-minted at f2f4d500 after the header was written) — corrected in the instrument (unlocked artifact), logged.
- **H-S2C-2** the first Phase-0 run halted (ZeroDivisionError) because the clipped Hermitian form returned zero acoustic speeds — a fail-closed halt that exposed the substrate finding; no number from that run is used.
- **H-S2C-3** the frozen T1 list carries bare numeric patterns (5e-16, 4.7e-23, 1.27e-22) that can collide with scientific-notation formatting of unrelated quantities (H-2 class). All Phase-0 scans returned zero hits; an amended list with contextual patterns is PROPOSED for the next lock cycle (the frozen list is not edited).
- **H-S2C-4** this turn's earlier in-context work (repo recovery of gz1/tsh4, lock minting, first harness) was recovered from the sandbox after a context reset; the filesystem was treated as the source of truth and every artifact re-verified by hash (prereg, T1, gz1 MANIFEST 17/17 present files OK) before use.
- **Retro Q-item (G-ζ1, §2.88.D.1 / V4.36 line):** G-ζ1's sanity gate (b) "three Goldstone zeros at Γ" passed on the clipped form — i.e., for the wrong reason; its verdict-bearing quantities (acoustic top 20.45, gaps 22.1/25.5/33) sit at ω ≈ 20–30 where a −2.1 offset in ω² is a ≲0.2% shift, so the quantitative impact is expected negligible, but the record should carry the annotation and a CC re-check if the author elects. NOT a G-S2C1 matter; filed for the author.

## What Phase 0 does NOT claim
No S2 ladder was computed, fitted, or sealed (the earlier harness's sealing path never executed; PHASE1_AUTHORIZED = False). No verdict arm is touched. Nothing about W_∪. The control-lattice numbers are instrument calibration only.

## Estate
lock/: prereg 2ea8ec13 (12,984 B); T1 8cd89b9a (144 B); lock record f2f4d500 (3,009 B). Phase 0: g_s2c1_phase0_close.py (the executed instrument), g_s2c1_phase0_harness.py (the Phase-1 instrument skeleton — BdG eigenvectors, polarisation fit, classifier, sealing path; halted at Phase 0 as above), checkpoint g_s2c1_phase0_checkpoint.json eae2bbd734f5129dd1e51efcbb55dd3d (4,555 B), run logs, this report. T1: zero hits on every artifact. gz1 substrate estate: MANIFEST.md5 verified for all 17 present files (15 cache files not fetched, not needed).

**Next authorization gate:** Phase 1 = (i) gem8 re-crystallization to the stationarity threshold + WARD-Γ verification, then (ii) the single-crystal ka-ladder fit. Not started.
