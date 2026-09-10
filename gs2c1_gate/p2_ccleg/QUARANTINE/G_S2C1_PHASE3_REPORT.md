# G-S2C1 (Gate G-S2-ON-CONE) — PHASE 3 REPORT: Probe P2, Aggregate Inheritance (chat leg, September 3, 2026)

**Authorization chain:** E-P2-1 (a) elected and confirmed; Addendum P2 **2feff442** locked before the instrument existed; P2 executed under it (checkpoints 0328b570 / 6da62fca / 0e8cc05e; structure diagnostic 60add009; instrument 05a323cf); **re-executed today: all three checkpoints byte-identical** — the P2 result is a deterministic function of the locked instrument. Consolidated Phase-3 checkpoint: `s2c1_phase3_checkpoint.json` (hash in the manifest below). Machinery: the recovered G-POLY1 instrument (gvbkof @ 231b555a, manifest-verified), input 200e7a8b verified at every run.

## What was computed
Re Σ_T at second (Born/SOA) order — the Kramers–Kronig partner of the banked Rayleigh attenuation — on the identical Ξ/Φ_TM kernels and mode normalization: D(k) = Δc_T/c_T(k) = (1/π)Σ_M N_M·PV∫q⁴F_M(q,k)/(k_M²−q²)dq, by Cauchy-weight quadrature plus regular tail, for the polarization-averaged shear cone (E-P2-1 (a)) and the L channel as positive control, on the four banked polycrystal tensors.

## Controls (all exact)
F-AGG-PIN: Q_T quartet reproduced to ≤ 2×10⁻¹⁶. F-AGG-KK: the Im-part tie-in reproduces the recovered `alpha_finite` to ≤ 7×10⁻¹⁶ (the real part is its exact Hilbert partner by construction). F-CONV: Ξ-quadrature doubling ≤ 2×10⁻¹³, μ-nodes doubling ≤ 2×10⁻¹⁴, Q_max doubling ≤ 10⁻¹⁵ — converged. F-AGG-L: L channel nonzero and analytic-controlled.

## Result
| substrate | D(0) (static Born shift) | **a₂^agg** (analytic k² coefficient) | a₄^agg | a₂^agg/Q_T^a | a₂,L/a₂,T |
|---|---|---|---|---|---|
| step_hex | −2.053×10⁻² | **−1.834766×10⁻²** | +6.954×10⁻² | −0.5214 | 1.3257 |
| gem8_hex | −2.892×10⁻² | **−2.593369×10⁻²** | +9.896×10⁻² | −0.5185 | 1.3267 |
| step_cubic | −3.151×10⁻² | **−2.853747×10⁻²** | +1.068×10⁻¹ | −0.5277 | 1.3200 |
| gem8_cubic | −4.368×10⁻² | **−3.971398×10⁻²** | +1.493×10⁻¹ | −0.5261 | 1.3185 |
a₂^agg is negative (normal dispersion) and O(10⁻²) for every substrate; it exceeds τ_agg = 10⁻⁶ by four orders and its converged uncertainty (≲10⁻¹³ relative) by thirteen. Two report-only near-universalities: a₂^agg/Q_T^a = −0.52 ± 0.9%, a₂,L/a₂,T = 1.323 ± 0.3% (F-AGG-UNI).

## Structure finding (the machine against my pre-registration)
The addendum pre-registered a non-analytic k³ term and made the 3-term basis {k²,k³,k⁴} the basis of record on disagreement, requiring its k² coefficient to match the independent analytic D2 within CI. The machine refutes the k³ term: R(k) = Δ(k) − D2·k² = +0.0695·k⁴ flat over four decades of k (R/k³ → 0; R/(k⁴ ln k) not constant); a pure even basis {k⁴,k⁶,k⁸} fits R to rms 8.5×10⁻⁹ (the quadrature floor). The aggregate dispersion is analytic in k²; the fitted "a₃" is aliasing of a₆; both fit bases are biased 1.5–1.9% by the k⁶ term over the window; the analytic control caught it (H-S2C-10, H-S2C-11).

## F-AGG-DISP — evaluated under both rules, not chosen
- **Locked rule (Addendum P2 as written):** the 3-term fitted a₂ misses the analytic D2 by 1.4–1.5% (T) and 5–6% (L), outside CI ⇒ F-AGG-ANALYTIC fails ⇒ **mechanical arm A5-agg INSTRUMENT-LIMITED, all four substrates.** The rule is not edited.
- **Proposed P2-A (author's decision pending):** a₂^agg of record = the analytic D2 (closed form on the same kernels, R1-machine), the ladder as confirmation (Δ/k² → D2 in the small-k limit), a₃ ≡ 0, a₄^agg from the even basis ⇒ **A3-agg DISPERSIVE (grain-scale k²), all four substrates.** The physics does not depend on the decision; the record's arm label does.

## Consequence (PF-S2) and status
Both dispersion scales the window re-derivation needs are in hand and concordant in sign and magnitude: lattice-scale a₂ = −1.28…−1.32×10⁻² (Γ–K) / −1.99…−2.06×10⁻² (Γ–M) at a* (two-leg, A3 both legs), grain-scale a₂^agg = −1.8…−4.0×10⁻² at a_g (chat leg). The S2 channel does not ride the cone exactly at either scale: W_∪ stays suspended, and W_∪′ is a fold action from the a₂ scales on your word. Still open before the fold packet: (1) the chat-side run-2 on the single-crystal S9 — the author reports run-2 ALL PASS; the chat side has not yet received CC's v1.1 checkpoint, comparator output, and commit to re-run the frozen v1.1 (cc9005d2) itself, which the protocol requires; (2) P2-A; (3) the P2 CC leg (two-leg on the aggregate) — a separate dispatch. Honesty: H-S2C-10, -11, -12 filed; T1 zero hits on this report and the Phase-3 checkpoint (one H-2-class self-catch in the checkpoint's own honesty text, rephrased). No observable, no bridge, no μ_n, no window action here.
