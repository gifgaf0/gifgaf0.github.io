# G-S2C1 (Gate G-S2-ON-CONE) — CC-LEG REPORT: PROBE P2 / PHASE 3 (AGGREGATE) — leg 2 of 2
**Date:** September 4, 2026. **Dispatch:** `G_S2C1_P2_CC_DISPATCH_INBAND.md` md5 2bd1ff8f9017eb2dff62b960f084c15b (143506 B); all 19 embeds extracted and md5/byte-verified; 11 quarantined artifacts written to `QUARANTINE/` and left unread until the checkpoint commit.
**Lock chain honored:** prereg 2ea8ec13; Addendum P2 2feff442; Addendum P2-A 71b4c701; T1 8cd89b9a. No new elections.

## 1. Verdict

**Comparator (frozen, `g_s2c1_p2_compare.py` aa887e6c): C1–C7 ALL PASS on all four substrates — S9 NOT triggered. The two-leg aggregate result stands; fold pending author authorization.** Verbatim output: `comparator_output.txt` (md5 3a71728f3de851912c01d2ef141c7e34, 4305 B).

Headline (this leg, computed blind to method — see honesty ledger for the delivery-blindness caveat):

| substrate | a₂^agg of record (analytic D2, T) | a₂^agg,L | a₄^agg (even basis) | a₆ | arm |
|---|---|---|---|---|---|
| step_hex | −1.834766316394585e-02 | −2.432261470924973e-02 | +6.986e-02 | −2.695e-01 | A3-agg DISPERSIVE (grain-scale k²) |
| gem8_hex | −2.593369358429419e-02 | −3.440682735189905e-02 | +9.942e-02 | −3.842e-01 | A3-agg DISPERSIVE (grain-scale k²) |
| step_cubic | −2.853747110794621e-02 | −3.767052681317584e-02 | +1.073e-01 | −4.152e-01 | A3-agg DISPERSIVE (grain-scale k²) |
| gem8_cubic | −3.971397679128610e-02 | −5.236302368972408e-02 | +1.500e-01 | −5.811e-01 | A3-agg DISPERSIVE (grain-scale k²) |

C4 agreement chat↔cc on a₂^agg: ≤ 3.4e-13 relative (tolerance 1e-6). Arms identical; F-AGG-UNI spread identical to 3 digits (1.77e-2 both legs); a₂L/a₂T ≈ 1.326–1.320 across the quartet (reported).

## 2. Independence content of this leg (the flagged shared layer, rebuilt)

- **SO(3)/kernel layer (own scheme):** ZYZ-Euler product quadrature — uniform 12-point grids in α, γ × 8-node Gauss–Legendre in cos β — which is *exact* for the l ≤ 8 band limit of δc⊗δc; doubling (24, 16, 24) shifts D2 by ≤ 8e-15 (F-CONV Ξ term). Kernels Φ_IM(μ) extracted as polynomials on 9 Chebyshev nodes: all odd-degree and degree>4 coefficients at machine zero (≤ 3e-14 relative) — Φ_IM is an even quartic, verified not assumed; all μ-integrals (I₀, I₂, F_M) then closed-form. Reciprocity control Φ_LT = 2Φ_TL to 6e-15. Mean isotropy: quadrature mean vs closed-form Voigt at ≤ 2e-15.
- **Re Σ_T method (REQUESTED_VARIATION, differs from the chat leg's Cauchy-weight PV quadrature + regular tail):** variation (ii)-type — the μ-integral in closed form as a uniformly convergent geometric series in (B/A)² = (2kq/(1+k²+q²))² ≤ 0.083 on the ladder, then PV in q by exact pole extraction: on [0, 2k_M] the pole part integrates to g(k_M)·ln3/(2k_M) in closed form and the analytic remainder (g(q)−g(k_M))/(k_M²−q²) is quadratured in mpmath (dps 30); tail [2k_M, ∞) regular. Cross-checks: settings/split variation ≤ 1.3e-16; **variation (iii) as an independent method control** — ε-regularized weight (k_M²−q²)/((k_M²−q²)²+ε²) at ε₀, ε₀/2, ε₀/4 with quadratic Richardson to ε→0 — reproduces D(k) to ≤ 4.9e-8 on every substrate.
- **Own D2 derivation:** `CC_D2_DERIVATION.md` (md5 3697624eefb36aa48b2a209271501a40), written before the numeric run. From the P2 operational definition, using the evenness of Φ (derived structurally, verified numerically) and the exact split 1/(k_M²−q²) = −1/q² − k_M²/q⁴ + k_M⁴/(q⁴(k_M²−q²)): D(k) = D(0) + D2·k² + O(k⁴) with **D2 = Σ_M N_M[(1−2r_M²)I₀^M/8 − (3/8)I₂^M]** and *no k³ term* (the pole piece dies through PV∫₀^∞dx/(r²−x²) = 0; every other odd candidate dies by evenness of Φ). **Verdict on the P2-A formula: CONFIRMED, term for term** — the addendum's D2 = (1/π)Σ_M N_M[−∫q²F₂dq − r_M²∫F₀dq] with F₂ = −2I₀/A³ + 12q²I₂/A⁴ is identical to my §3 expression before closed-form evaluation of the q-integrals; this leg additionally reduces it to the elementary closed form above. a₃ ≡ 0 (H-S2C-10 retirement) is *derived*, independently, on this leg.

## 3. Results against the falsifiers (all decided before quarantine decode)

- **F-AGG-PIN:** Q_T^a quartet reproduced at 1.3e-15…6.1e-14 relative (gate 1e-10); V_T, V_L at ≤ 9e-16; Q_L^a (control) at ≤ 3e-13; int Φ_TT/int Φ_TL at ≤ 6.1e-14. PASS.
- **F-AGG-KK:** α_T(k) = Σ_M k k_M³ N_M/2 · F_M(k_M,k) in this leg's closed form reproduces the banked `alpha_T_a` grid at 2.1e-15…6.2e-14 max relative (gate 1e-9). PASS.
- **D(0) anchor:** closed form −(1/4)Σ N_M I₀ vs the mpmath ladder's D0: agreement ≤ 6e-16. C3 chat↔cc ≤ 1e-8: PASS.
- **Structure check:** R(k) = Δ(k) − D2·k² on the 14-point ladder — even basis {k⁴,k⁶,k⁸} rms 1.3e-11…2.9e-11; rejected {k³,k⁴} rms 1.8e-7…3.9e-7 (worse by ~1.3e4×); rejected {k⁴, k⁴ln k} rms 7.2e-8…1.5e-7 (worse by ~5e3×). **The data select the pure even basis**; no odd or logarithmic term at this order. Small-k confirmation Δ/k² → D2 (incl. a₄k²) at ≤ 3.6e-8 (gate 1e-3). PASS.
- **F-AGG-DISP:** |a₂^agg| = 1.8e-2…4.0e-2 ≫ max(τ_agg = 1e-6, CI ≈ 2e-16 abs) ⇒ **A3-agg DISPERSIVE (grain-scale k²)**, all four substrates.
- **F-AGG-L (positive control):** D0_L and a₂L nonzero (−8.6e-3…−1.7e-2; −2.4e-2…−5.2e-2), analytic value confirmed by a 3-point L-ladder at the expected O(k²) truncation level. PASS.
- **F-CONV:** Ξ-doubling on D2 ≤ 8e-15 (gate 1e-6); on Q_T ≤ 2e-13; PV settings variation ≤ 1.3e-16 (gate 1e-9); ε-Richardson method agreement ≤ 4.9e-8 (gate 1e-6). PASS. CI of record = max(Ξ-doubling, PV variation) per substrate ≈ 2e-15 relative.
- **F-AGG-UNI (report only):** a₂/Q_T^a = {−0.5214 (step_hex), −0.5185 (gem8_hex), −0.5277 (step_cubic), −0.5261 (gem8_cubic)}; spread 1.768e-2 — near-universal at the ~2% level, matching the chat leg.

## 4. Return manifest (md5, bytes)

Instruments: `g_s2c1_p2_cc_instrument.py` c1e5915595646ca27fd73c61ec0ef123 (13137 B); `g_s2c1_p2_cc_stage3.py` b3206361c3d5f79e44f9bff0fedf0d36 (6940 B); `cc_p2_pv_xcheck.py` aa30f229892b3495ac529ad6fb6728b3 (3564 B).
Phase JSONs: `cc_p2_phase0.json` e26dce3cd5e967aeee71c0aba599e21c (2432 B); `cc_p2_phase1.json` aaae206733b0f0a378a5c6b600274d3f (11454 B); `cc_p2_phase2.json` b1b6f35e0420cbacb8fc99b0aa1f8fba (6551 B); `cc_p2_phase3.json` a8e9f4f93beaefd972d82ab1caf22e7e (6386 B); `cc_p2_phase4.json` e6066bc5fc977029800d96fbd2a9c341 (1982 B); `cc_p2_pv_xcheck.json` 69d7c4e5edac2fe2a9bdbcb2e6a0b220 (440 B).
Checkpoint: `s2c1_p2_cc_cmp_checkpoint.json` **md5 50a9e800af7f1fe44a691ba977c62422** (5351 B), schema p2_cmp_v1. **Pre-decode commit: 3253240183d94d72f6e48ad179775c1655a0dffa** (branch `claude/new-session-3xgb2b`) — checkpoint hashed and committed with `QUARANTINE/` unread; the quarantine was decoded and the comparator run only after that commit. The quarantine-decode commit is the return commit carrying this report (HEAD of the same branch).
Comparator output: `comparator_output.txt` 3a71728f3de851912c01d2ef141c7e34 (4305 B). D2 derivation: `CC_D2_DERIVATION.md` 3697624eefb36aa48b2a209271501a40 (5532 B). T1 scan: `cc_p2_t1_scan.json` f430397693138ece8b5ee15b4aea8602 (1040 B).

## 5. Honesty ledger

- **H-CC-P2-1 (blindness breach at delivery, disclosed pre-computation in `cc_p2_phase0.json`):** the session upload that delivered the dispatch also carried `s2c1_phase3_P2A_evaluation.json` — a QUARANTINED chat-leg artifact — as a loose file, and it was read by this leg before extraction. Numerical blindness to the chat leg's headline P2-A numbers was therefore not intact for this leg. Mitigation, applied and auditable: no value from that file was consumed or tuned to; every number came from the banked inputs via this leg's own instrument, own kernels, own PV method, and own D2 derivation; the arm was still decided before the `QUARANTINE/` copies were opened; the frozen comparator (tolerances fixed pre-run) adjudicated. Methodological independence intact; delivery blindness was not. The two-leg claim should be read with this caveat.
- **H-CC-P2-2 (T1 numeric collisions):** the T1 scan over all CC instruments and outputs returns 3 hits, all of the numeric pattern `5e-16` occurring inside machine-epsilon floats (`…7.390347823399325e-16`, `…3.984522480373865e-16`, `…2.2551405187698315e-16`). Classified as scientific-notation collisions per the activation flags; not reformatted to dodge. Zero non-numeric hits.
- **H-CC-P2-3 (two commits, not one):** the dispatch asks for one return commit but also for a pre-decode checkpoint commit hash; this leg made the pre-decode commit (3253240…) and this return commit. Recorded as a protocol note, not a deviation of substance.
- **H-CC-P2-4 (observation, banked substrate):** the banked "hex" tensors carry C66 ≠ (C11−C12)/2 (e.g. step: 64.9223 vs 64.9397), i.e. they are 6-constant tetragonal-form objects labeled hex. Consumed exactly as banked (pin E3); the general Voigt formulas reproduce the banked μ̄, V_T, V_L to machine precision, so this is a property of the locked substrate, not an error in either leg.
- **H-CC-P2-5 (instrument edit before first successful stage-3 run):** `g_s2c1_p2_cc_stage3.py` was patched (a numpy-repr string issue) after stage 1–2 had run and before its first successful run; no numeric logic changed. The committed file is the file that ran.

## 6. Deviations

None of substance. The L-channel ladder was run at 3 control points only (the L requirement in P2/P2-A is the analytic value plus control, and C5 compares the T channel only); the F-CONV μ-node doubling of the chat spec is subsumed on this leg by closed-form μ-integrals (the kernel-degree and doubling controls stand in for it, both at machine zero).

## 7. Non-claims

R1-machine for every number; R2 for the aggregate reading (conditional on G-POLY1's E3 elections and Born/SOA order). No observable, no bridge (M.BRIDGE), no channel-speed-equality claim, no μ_n, no window action; not a fold — PF-S2 executes only at fold on author authorization. The 3-D kinematic point of E-P2-1 rides with the election as disclosed and is not re-adjudicated here.
