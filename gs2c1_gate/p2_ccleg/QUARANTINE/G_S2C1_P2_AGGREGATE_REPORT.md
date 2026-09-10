# G-S2C1 — PHASE 3 / PROBE P2 (AGGREGATE) — REPORT (chat leg, September 3, 2026)

**Lock:** Addendum P2 **2feff442** (E-P2-1 (a) verbatim; operational definition; falsifiers; fit-basis rule — locked BEFORE the instrument was written). Machinery: the recovered G-POLY1 instrument (gvbkof @ 231b555a, manifest-verified) imported as a module; input `poly_vrh_results.json` md5 200e7a8b verified at run. Instrument `g_s2c1_p2_aggregate.py`; checkpoints p2_phase0_pin **0328b570**, p2_phase1_ladders **6da62fca**, p2_phase2_fits **0e8cc05e**; structure diagnostic **60add009**. T1 zero hits throughout.

## Controls — all exact
- **F-AGG-PIN PASS:** the banked Q_T^a quartet reproduced digit-for-digit (relative 0 to 2.2×10⁻¹⁶); V_T, V_L to the printed digits.
- **F-AGG-KK PASS:** the Im-part tie-in α_T(k) = Σ_M k k_M³ N_M/2 · F_M(k_M,k) reproduces the recovered `alpha_finite` on the G-POLY1 grid to ≤ 6.7×10⁻¹⁶ — same kernels, same mode normalization; the real part computed here is its exact Hilbert partner.
- **F-CONV PASS:** Ξ quadrature doubling ≤ 2×10⁻¹³ on D2 and on D(0.3); μ-nodes 64→128 ≤ 2×10⁻¹⁴; Q_max 50→100 ≤ 10⁻¹²; D(0) closed form vs D(10⁻⁴): identical to 7 digits.

## Result — the shear cone in the aggregate is dispersive at Rayleigh order (E-P2-1 (a))
D(k) = Δc_T/c_T(k) = (1/π)Σ_M N_M·PV∫q⁴F_M/(k_M²−q²)dq. Static second-order renormalization D(0) = −2.05 / −2.89 / −3.15 / −4.37 ×10⁻² (step_hex / gem8_hex / step_cubic / gem8_cubic) — the Born velocity shift below Voigt, as it must be.
Dispersion coefficients (k in units 1/a_g), **exact analytic k² coefficient, quadrature-converged to 10⁻¹³ and confirmed by the small-k limit of the ladder:**
| substrate | a₂^agg (T) | a₄^agg (even-basis) | a₆ | a₂^agg,L (control) | a₂/Q_T^a |
|---|---|---|---|---|---|
| step_hex | −1.834766×10⁻² | +6.954×10⁻² | −0.254 | −2.432261×10⁻² | −0.5214 |
| gem8_hex | −2.593369×10⁻² | +9.896×10⁻² | −0.362 | −3.440683×10⁻² | −0.5185 |
| step_cubic | −2.853747×10⁻² | +1.068×10⁻¹ | −0.390 | −3.767053×10⁻² | −0.5277 |
| gem8_cubic | −3.971398×10⁻² | +1.493×10⁻¹ | −0.546 | −5.236302×10⁻² | −0.5261 |
Two new R2-class near-universalities across the quartet (report-only, F-AGG-UNI): a₂^agg/Q_T^a = −0.52 ± 0.9% and a₂^agg,L/a₂^agg,T = 1.323 ± 0.3%. F-AGG-L PASS (L channel nonzero, analytic-controlled).

## The locked rule's verdict, and why it is A5-agg
The P2 addendum pre-registered a non-analytic **k³ term** and made the 3-term basis {k²,k³,k⁴} the basis of record when the bases disagree, with the fitted k² coefficient required to match the independent analytic D2 within CI (F-AGG-ANALYTIC). The bases disagreed (by construction of the aliasing); the 3-term a₂ misses the analytic D2 by 1.5% (T) and 5–6% (L), outside CI ⇒ **mechanical arm A5-agg INSTRUMENT-LIMITED for all four substrates.**
Machine diagnosis: R(k) = Δ(k) − D2·k² sits at **+0.0695·k⁴ over four decades** (R/k⁴ flat from k = 0.0036 to 0.024; R/k³ → 0; R/(k⁴ ln k) not constant); a pure even basis {k⁴,k⁶,k⁸} fits R to rms 8.5×10⁻⁹ (the quad floor). **The aggregate dispersion is analytic in k² — no k³, no k⁴ log k at this order.** The pre-registered k³ term was a derivation error (corrected: for F₀ even in q the pole-region expansion is analytic in k_M²), refuted by the machine — **H-S2C-10**. The "a₃" of the 3-term fit (+5×10⁻³) is aliasing of a₆; the elected 2-term basis is biased 1.9% the other way by the same k⁶ term over the window (a₆k⁶/a₂k² ≈ 11% at k = 0.3). The window-stability CI under-estimated this basis bias — **H-S2C-11**.

## Proposed Amendment P2-A (author's call; NOT applied)
a₂^agg of record = the analytic second-order coefficient D2 (closed form on the same Ξ/Φ kernels; R1-machine), with the ladder as confirmation (Δ/k² → D2 in the small-k limit; even-basis remainder rms ≤ 10⁻⁸); a₃ ≡ 0 (refuted); a₄^agg = the even-basis k⁴ coefficient. Under P2-A: **A3-agg DISPERSIVE (grain scale)** for all four substrates, |a₂^agg| = 1.8–4.0×10⁻² ≫ τ_agg. The locked rule is not edited; P2-A is a proposal in the honesty record.

## Consequence and non-claims
PF-S2 input now complete in kind: lattice-scale a₂ (P1: −1.28/−1.99×10⁻² at a*) and grain-scale a₂^agg (P2: −1.8…−4.0×10⁻² at a_g), both negative (normal dispersion), both O(10⁻²). W_∪′ is a fold action after the CC leg and the author's word; nothing here touches W_∪. No observable, no bridge, no μ_n. R1-machine for every number; R2 for the aggregate reading conditional on G-POLY1's E3 elections and Born/SOA order. The 3-D kinematic point (a propagating plane wave's strain carries helicity 0/±1, never pure ±2) stands as disclosed in the staging note and now rides with E-P2-1 (a).

## T1 scan record
All P2 artifacts scanned against the frozen list 8cd89b9a: one hit, `s2c1_p2_phase2_fits.json` line 289 — the bare numeric pattern `5e-16` matched inside the F-CONV value `D03_Qmax100_rel = 1.1102230246251565e-16` (machine epsilon). Classified as the numeric-formatting collision predicted at Phase 0 (H-S2C-3); logged as **H-S2C-12**; the checkpoint is not reformatted and the frozen list is not edited. The contextual-pattern amendment of the T1 list remains PROPOSED for the next lock cycle.
