# G_CI1_LOCK_RECORD_ADDENDUM_2.md — Addendum 2 to the G-CI1 lock record (append-only; base lock record `a6adbb6a` and Addendum 1 `e5029ae8` unmodified)

**Date:** August 19, 2026. **Scope:** Phase 2 (chat leg) closure; honesty items H-6…H-10; the I-3 route ruling; dispatch plan. Lock-record class (T1-exempt embed by the two-document convention).

## A2.1 — Author's authorizations of record for this addendum (VERBATIM)
> **Directive: Ratify H-4, Confirm F-IRR Verdict, and Authorize Phase 2**
> The Phase 1 checkpoint (`ci1_phase1.json`) and the F-IRR execution are confirmed.
> 1. I explicitly RATIFY the D-4 first-clause reading of record logged in H-4. Helicity content is the eigenphase multiset of the mode's polarization/orbital data. Derived strain/stress eigenphases are kinematic labels, not excitation content.
> 2. The F-IRR verdict (FIRES, K = ∅) is confirmed and now T3-immutable. CI-S is falsified-structural.
> 3. The activation of the CI-W/EM-IN operative branch and the PF-1 suspension of W_∪ from the Phase-3 intersection are acknowledged.
> I authorize the execution of Phase 2 (I-2 regime map + I-3 residual ledger) on the chat leg.
> 1. Execute the 2.1 containment check (s₁ and Q_T^a reproduction).
> 2. If containment passes, proceed with I-2 and I-3 on the 33-point grid.
> 3. Compute the ray bracket and validity indicators per §5.4.
> 4. Record all outputs in `ci1_phase2.json`.
> Report back with the Phase 2 containment status, the D₂ values, and the ray-bracket limits.

followed by two "Continue" authorizations (August 19) after the chat leg's interim reports, on which the production run, the T1-safe re-serialization, and this addendum proceed.

## A2.2 — Phase 2 (chat leg) closure
Instrument `g_ci1_phase2_regime_chatleg.py` md5 `6db6e872edefe318e92c5e9448ef02ee` (26,815 B); checkpoint `ci1_phase2.json` md5 `ee61b4b1cabda12ee77b27c05f425bc8` (57,470 B); T1 zero hits on both; inputs byte-asserted at invocation (`200e7a8b…` / `621120e5…`); nodes 20/40, mp precision 30 (+2 digits per decade below x = 1) ; 33-point grid.

**Containment (2.1) PASS ×4** — s₁ rel dev 3.26e-9 / 2.24e-9 / 1.55e-9 / 1.19e-9; Q_T^a rel dev 3.22e-8 / 3.04e-8 / 3.24e-8 / 2.74e-8 (hex:step / hex:gem8 / cubic:step / cubic:gem8), tolerance 1e-6. Controls: Ξ quadrature doubling 1e-11 (exact band-limit); isotropic-input null 3.7e-14; Voigt μ_V = JSON G_V; A(θ) anchor ≤ 9.0e-12 (cubic:step) and 4.8e-13 (cubic:gem8) — the anchor contraction identified as ⟨(δC_nnmm)²⟩ = (ν²/525)(3+cos²θ)², while the n⁴m⁴ contraction is (16ν²/525)P₄(cosθ) (both reproduced); delta-pairing fit returns canon's H-3 coefficients (2ν²/1575, ν²/180, −ν²/630) to 5e-12 with residual 1e-13 — an independent third reproduction; Φ_TM polynomials even, degree 4, odd/deg>4 content ~1e-14.

**D-2:** Re m̃_T(0) = Q_TT^a + Q_TL^a (V_L/V_T)³ (closed form); c_cone/V_T0 = 0.979885 / 0.971895 / 0.969449 / 0.958151; c_cone = 8.375838 / 9.960949 / 7.867852 / 9.459335 (substrate units), each between the banked Reuss and Hill speeds.
**I-2:** Q^(a)(x→0)/Q_T^a = 1 to 1e-10; Rayleigh exponent 4.00000 (PASS); stochastic asymptote Q^(a)x² → Φ_TT(1)/V_T⁴ (reproduced to 6 digits); Q^(d) = Q^(a)/8 tabulated with α_T·d and Im k/Re k.
**I-3 (route of record: direct PV):** D₂ = −4.5869158e-3 / −6.4834234e-3 / −7.1343678e-3 / −9.9284942e-3; Δ_ch/x² constant to 1e-10 across x ≤ 1e-2; large-x plateau Δ_ch → −8.8169e-3 / −1.21709e-2 / −1.40931e-2 / −1.89435e-2 (flat to 1e-7 over x = 1e5–1e8); per-point doubling worst 1.04e-8 / 1.08e-8 / 9.7e-9 / 1.01e-8 (the 1e-8 target missed by ≤ 8 % at one extreme-x point on three configs; floor 1e-6 nowhere approached; no VOID-NUM).
**Validity (§5.4):** ε_T = 0.09133 / 0.10912 / 0.13038 / 0.15743 (ε_T² ≤ 0.10 PASS ×4); x_S = 10 / 3.162 / 3.162 / 3.162 (hex:step limited by both rules at 31.6; the other three by ε_T·x ≤ 1 at x = 10); x_G = 10; a VOID gap x_S→x_G exists on three configs (hex:step has none).
**Ray bracket (2.4; E-11: ray attenuation VOID):** c_path (mean-arrival) = 8.403922 / 10.016926 / 7.829895 / 9.383016; Δ_geo^X (Voigt, Reuss, Hill, HS−, HS+): hex:step (−1.68 %, +1.40 %, −0.18 %, +0.16 %, −0.25 %); hex:gem8 (−2.26 %, +1.90 %, −0.25 %, +0.26 %, −0.36 %); cubic:step (−3.52 %, +4.83 %, +0.40 %, +0.92 %, −0.48 %); cubic:gem8 (−4.96 %, +7.77 %, +0.81 %, +1.86 %, −0.78 %). Fast/slow variants recorded.

## A2.3 — Honesty ledger continued
**H-6 (locked-text erratum, factor 8).** §4 2.2 defines Q_T(x) := α_T·d/x⁴ and annotates "(→ Q_T^a as x→0)"; with d = 2a (banked) the limit of that definition is Q_T^d = Q_T^a/8 (both banked). The mapper continuation's "Q_T := Q_T^a" for x < 1e-4 is the same slip. Resolution: the definition α_T·d = Q·x⁴ is authoritative; both normalizations are tabulated; the mapper consumes α_T·d; no edge moves. The two "Q_T^a" mentions are read as Q_T^d.
**H-7 (process).** A mid-debug Phase-2 draft and a containment prototype from an earlier, context-lost segment of this session were found in the workspace; inspected; their containment numbers agree with the sealed run to 1e-9; their residual route was broken (NaN / plateau artifacts); set aside unconsumed. Two numerical defects were found and fixed during this session's build before any output was consumed: (i) the pole-subtraction constant term needs its exact truncated-range PV correction (otherwise a spurious linear-in-x growth); (ii) the static subtraction's s-range must extend below the SAF scale s ~ 1 (otherwise a spurious upward drift at x ≥ 1e6). Both disclosed; both verified by cutoff/precision/panel-density insensitivity tests.
**H-8 (route inequivalence — ruling requested; author veto standing).** The subtracted Kramers–Kronig transform of α does not reproduce the direct on-shell real part: KK/direct = 0.9789 / 0.9844 / 0.9675 / 0.9706 in the Rayleigh regime (D₂ ratio), with the worst relative route deviation 0.18–0.37 near x ~ 10. Cause: the on-shell mass operator is not analytic in the upper half ω-plane (the SAF spectrum's poles move with k = ω/V). **Ruling of record (chat leg, pending the author's word, recorded with veto standing): the DIRECT principal-value route is the I-3 quantity of record for C-CI-3; KK is a diagnostic only; the CC dispatch says so.** The pre-registration's "either route" flexibility is thereby narrowed (a labeling-level amendment: both routes were meant to compute "the real part of the same second-order mass operator", and only the direct route does).
**H-9 (T1 hygiene, mechanical).** A machine-generated 16-digit float in the first production checkpoint contained, by digit coincidence, a six-digit string matching a T1 token. The serializer now writes floats at a fixed number of significant digits (11 here; every comparison tolerance is ≥ 1e-8) and rescans; the production run was repeated from scratch with the new serializer; the checkpoint is T1-clean by construction. No value changed beyond representation.
**H-10 (diagnostic field caveat).** The checkpoint field `exact_form_minus_second_order_rel_max` is computed in double precision and is dominated by cancellation at the smallest x (Δ ~ 1e-19); it is not a physics statement — the second-order consistent Δ_ch is the quantity of record; the exact-form difference is O(ε²) relative wherever the field is numerically meaningful.

## A2.4 — Dispatch
`G_CI1_CC_DISPATCH_INBAND.md` (P-4, one self-contained file) embeds byte-exact: the locked pre-registration, the frozen T1 list, the lock record + Addenda 1–2 (lock-record class, T1-exempt), the two byte-verified inputs (the pin record under E-10 exemption), and the sealed anchor file (T1-exempt; UNOPENED until Phase 3). No chat-leg instrument or checkpoint is embedded (blindness); commitment hashes only. CC executes Phases 0–3 from scratch; CC read #1 of the sealed file is the verdict read of record (E-9); A-DIFF last. Comparison by the chat leg afterwards (C-CI-1…4; S9 on any miss).

## A2.5 — What opens next
On the author's word: the dispatch goes to CC; after CC returns, the two-leg comparison; then the sealed-mapper chat-leg read (second, after CC's), and the fold-authorization staging toward §2.91.N + Part VI row + the §2.91.M W_∪ annotation (V4.77-class). Standing items untouched: §2.52 Open 3; §2.87.J; OP-2.58.2d; P-LEX-1.
