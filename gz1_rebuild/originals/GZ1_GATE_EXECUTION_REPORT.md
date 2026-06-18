# GATE G-ζ1 EXECUTION REPORT
**Date:** 2026-06-10 · **Executor:** chat-side instance (independent sandbox) · **Ledger basis:** v4.35 CANONICAL, §2.88.D / Part VI gate row
**Status:** EXECUTED — verdict reached. **No canonical action taken.** §2.52 untouched per standing instruction.

---

## 0. Discipline attestation

- Pre-registration written before any computation: `GZ1_EXECUTION_PREREGISTRATION.md` (object, channel rule, layer definition, estimators, outcome mapping — all fixed in advance).
- Eddington guard: the target ζ = 1 − π/√12 = 0.0931004 appears in exactly one file, `comparison_step.py`, run last. No input, grid, frequency, or fit window was selected with reference to the target. The probe frequencies are the band-structure midgaps, fixed by Phase 3 before any decay was measured.
- Imports held to the I1–I3 ticket (V4.26 §3.4-SYM): scalar GP reduction, soft-core kernel U(r)=g·θ(R−r) with canonical g=22, R=1, ρ₀=1, one scale. No fresh tuning.
- Instrument is self-contained (`gz1_core.py` + per-phase scripts); imports no tool under test.

## 1. Object reproduction (R1)

Big-box quench at canonical parameters reproduces the V4.26 crystallized state: **ψ₆ = 0.834** (exact match to the registered R1 value), ψ₄ = 0.111, 234 peaks, density contrast 1.63. Object: p6m triangular crystal — CONFIRMED.

## 2. Primitive cell (R1)

Energy-minimizing lattice constant **a\* = 1.4576** (17-point scan + parabolic refine; big-box k_c gives 1.44, box-quantized). Cell-relaxed μ\* = 55.90; polished GP residual 5.0×10⁻³, μ = 55.857. Row spacing **d = √3·a\*/2 = 1.2623**.

## 3. Bogoliubov–Bloch bands (R1)

Plane-wave BdG on the cell (Hermitian form L^½(L+2X)L^½), n=32, cutoff-stable vs n=40 to ≤0.11%.

- **Sanity gates all PASS:** L(Γ) min eig ≈ 0 with eigenvector = ψ₀ (overlap 1.000000); **three Goldstone zeros at Γ** (superfluid phase + 2 lattice translations — textbook supersolid).
- **The quasi-static density channel is GAPLESS and propagating** (longitudinal acoustic band 0 → 20.4). This is the registered channel for the pairwise pulsation coupling.
- Normal-incidence (Γ→M_y) stop bands: **Gap A (20.405, 22.248)** Δ=1.84; **Gap A2 (25.225, 25.615)** Δ=0.39; **Gap B (29.838, 33.291)** Δ=3.45. Gaps A and B persist over the sampled 2D path.

## 4. Driven-strip decay measurement (R1)

16-row strip (8 rectangular cells, periodic), isotropic density source (registered), frequency-domain GMRES, per-row envelope ratios + windowed exponential fit, wrap-aware clean windows. η-independence verified at Gap A: κ = 0.8061 (η=0.02) vs 0.8087 (η=0.05) — 0.3% shift under 2.5× η ⇒ true evanescence.

| probe | ω | per-layer t | note |
|---|---|---|---|
| Gap A midgap | 21.33 | **0.36 ± 0.02** | κ=0.806, fit r²=0.997; smallest t in the landscape |
| Gap A2 midgap | 25.42 | **0.54 ± 0.03** | 2-row Bloch beat; per-period products |
| Gap B midgap | 31.56 | **0.75 ± 0.03** | κ=0.217, fit r²=0.996 |
| in-band 13.4 | 13.40 | ≈ 1.00 | per-period product 0.998 — Bloch transparency |
| in-band 20.0 | 20.00 | ≈ 0.98 | residual η absorption only |
| acoustic 5.0 | 5.00 | no decay regime | interference-dominated; channel gapless per §3 (R1) |

## 5. Comparison (run last)

PASS window [0.0881, 0.0981]. **No probe hits the window.** Closest approach: t = 0.36 at Gap A, **factor 3.9× above target**. Quasi-static density channel: t → 1 (factor 10.7×).

## 6. VERDICT (per pre-registered arms)

- **PRIMARY — DEGENERATE.** The registered channel rule identifies the pulsation coupling with the quasi-static density channel; that channel is gapless (3 Goldstone zeros, R1) and transparent (t→1). The per-layer-attenuation ontology is not realized by the MV-G1 crystal: a GP supersolid does not attenuate its own density channel.
- **ALTERNATIVE — INFORMATIVE-FAIL.** Even granting the most favorable reading (any finite-ω gap, no frequency-selection mechanism required), the minimum achievable t is 0.36, a factor 3.9 above ζ; no frequency anywhere in the computed band structure yields t in the window.

Both arms agree in consequence:

1. **Falsifier (1) fires → H′ (transmission inversion, R2) is RETIRED.** The interstitial-void-network reading of ζ as per-layer coherent retention is not produced by the crystallized state's Bogoliubov physics.
2. **§2.2 per-layer-attenuation ontology requires reconception** (DEGENERATE arm): within I1–I3, layers of the p6m crystal do not attenuate the long-wavelength density channel at all — the honesty clause (Bloch transparency; superfluids transparent to long-λ phonons) is what the computation found.
3. **Paper conditionality clause executes** (Paper IIA F3 hole-fill: the ζ-as-transmission paragraph reverts to its conditional/excised form).
4. **M.BRIDGE: no counterexample.** This was the program's registered best shot at deriving a dimensionless observable-bridge constant from the crystallized state with a fixed import ticket. It failed cleanly and informatively. The observable-bridge asymmetry pattern stands.

What the gate did establish (positive R1 content, independent of the verdict): the MV-G1 state is a genuine supersolid with the full textbook excitation structure — three Goldstone branches, cutoff-stable bands, real normal-incidence stop bands with η-independent evanescent decay. The instrument works; the hypothesis didn't.

## 7. Proposed ledger handling — DRAFTED, NOT EXECUTED (awaiting authorization)

Proposed v4.36 fold (append-only):
- **§2.88.D outcome row:** record verdict DEGENERATE (primary) / INFORMATIVE-FAIL (alternative), t-landscape table, η-independence check, provenance file list.
- **H′ retirement entry** under §3.A (hypothesis retirement, not a §3.x retraction — pre-registered null closure; no canonical claim was wrong).
- **§2.2 annotation:** per-layer-attenuation reading marked "not realized in MV-G1 BdG (G-ζ1); ontology reconception open."
- **Paper IIA F3:** conditionality clause execution noted; calculator untouched (downstream rule).
- **§2.52: no change** (standing instruction).

## 8. Provenance files

`GZ1_EXECUTION_PREREGISTRATION.md`, `gz1_core.py`, `phase1_object.py/json`, `phase2_cell.py/json`, `phase3a_bands.py` + `phase3a_line.json`, `phase3b_path.py/json`, `build_cache.py`, `solve_one.py`, `phase4_*.json`, `profile_*.npy`, `final_fits.py`, `phase4_fits.json`, `comparison_step.py`, `psi0_cell_n32.npy`, `psi0_polished_n32.npy`.
