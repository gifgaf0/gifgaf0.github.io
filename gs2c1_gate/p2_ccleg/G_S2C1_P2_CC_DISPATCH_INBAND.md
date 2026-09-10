# G-S2C1 (Gate G-S2-ON-CONE) — CC-LEG DISPATCH: PROBE P2 / PHASE 3 (AGGREGATE) — IN-BAND, P-4 + P-4.b
## The shear cone in the polycrystalline aggregate — leg 2 of 2

**Dispatch date:** September 3, 2026 (author directive; the author's act of placing this file in the CC repo constitutes the dispatch). **P-4:** one self-contained file; every artifact embedded byte-exact with md5 + byte count. **P-4.b:** all QUARANTINED embeds are base64-armored; the extractor writes them to `QUARANTINE/`; you do not decode them until your own checkpoint is hashed and committed. (Two non-quarantined banked inputs also travel base64 purely for byte-exactness — they lack a trailing newline; `quarantine=0` on their markers means you may open them at once.)
**Lock chain (raw):** prereg 2ea8ec13; Addendum P2 2feff442 (E-P2-1 (a), operational definition, F-AGG falsifiers — locked before the chat instrument existed); Addendum P2-A 71b4c701 (a₂^agg of record = the analytic D2; the pre-registered k³ term retired as refuted — H-S2C-10); T1 8cd89b9a. No new elections.

## 0. Embed manifest (verify all 19 before anything else)
| Embed | md5 | bytes | enc | quarantine |
|---|---|---|---|---|
| `activation_P2_G_S2C1.json` | ce053201caf19c1acf3e3c0907851732 | 4734 | raw | no |
| `G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2.md` | 2feff442dfd08a379443d893b8c7761b | 4556 | raw | no |
| `G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2A.md` | 71b4c7010e48601e07f6458c711dfb4a | 1549 | raw | no |
| `t1_forbidden_G_S2_ON_CONE.txt` | 8cd89b9a82704accd89f7ff6f5e220b4 | 144 | raw | no |
| `poly_vrh_results.json` | 200e7a8b775577564369c6924d38a84c | 2767 | b64 | no |
| `poly1_phase1full_cc.json` | ec87e42f0f617b00c4985ba2aceac339 | 8140 | b64 | no |
| `g_s2c1_p2_compare.py` | aa887e6c62b9898f92506549a11db9ae | 4204 | raw | no |
| `extract_embeds_v2.py` | d4ac62219a95bea1e29d226e371ee39a | 2102 | raw | no |
| `s2c1_p2_chat_cmp_checkpoint.json` | d9b8463851fb71285aa53506781bc75b | 4726 | b64 | **YES** |
| `g_s2c1_p2_aggregate.py` | 05a323cf73851a56f54539f37c00cb1f | 13391 | b64 | **YES** |
| `s2c1_p2_phase0_pin.json` | 0328b570af46a878970653ad8775f6d9 | 1147 | b64 | **YES** |
| `s2c1_p2_phase1_ladders.json` | 6da62fca644d5ea6b1d7abe7329b5e2c | 12854 | b64 | **YES** |
| `s2c1_p2_phase2_fits.json` | 0e8cc05e4868b8db086564e297cab6d5 | 11789 | b64 | **YES** |
| `s2c1_p2_structure_diag.json` | 60add009c282b9d603021ba0adbfa1e2 | 5027 | b64 | **YES** |
| `s2c1_phase3_checkpoint.json` | 48927b9aebce27615b8f18581fe98a4f | 6473 | b64 | **YES** |
| `s2c1_phase3_P2A_evaluation.json` | 56b17d9356a60c4fb2c7d69ad19a6198 | 2795 | b64 | **YES** |
| `G_S2C1_P2_AGGREGATE_REPORT.md` | b56fbe5636cca4cdcde02900ac73469b | 5493 | b64 | **YES** |
| `G_S2C1_PHASE3_REPORT.md` | 41c608891e53eda1d96d1ad4c1128171 | 4898 | b64 | **YES** |
| `G_S2C1_P2_AGGREGATE_STAGING.md` | cad1319a16a70cf4af4f26730c4887ef | 5495 | b64 | **YES** |

## 1. Verify-then-build
`python3 extract_embeds_v2.py G_S2C1_P2_CC_DISPATCH_INBAND.md .` → 19 `OK` lines; the 11 quarantined items land in `QUARANTINE/` unread. Write `cc_p2_phase0.json`. Read Addendum P2 and P2-A in full — they are the objects of record; this dispatch adds procedure only.

## 2. What you compute (the activation flags carry the exact statements)
Rebuild Ξ and Φ_TM yourself (flagged shared layer). Then, independently of the chat leg's method: the second-order real part Re Σ_T (the exact Hilbert partner of the banked Rayleigh attenuation), D(k) on the ladder, D(0) closed form, the Im-part tie-in (F-AGG-KK), your own derivation of the analytic D2 (write it before consulting the addendum's formula; confirm or dispute in writing), the structure check on R(k) = Δ − D2·k² against the even basis and the two rejected alternatives, a₄^agg, the L-channel control, F-CONV by doubling your own quadratures, F-AGG-DISP at τ_agg = 10⁻⁶, F-AGG-UNI, and the arm per substrate — decided before decoding. Per-phase JSONs (`cc_p2_phase1..4`), then `s2c1_p2_cc_cmp_checkpoint.json` in schema p2_cmp_v1 (keys in the flags). Hash, commit, record the commit. Only then decode and run `python3 g_s2c1_p2_compare.py QUARANTINE/s2c1_p2_chat_cmp_checkpoint.json s2c1_p2_cc_cmp_checkpoint.json`.

## 3. Comparison protocol (frozen; tolerances in the comparator header)
C1 pin 10⁻¹⁰; C2 KK booleans; C3 D0 10⁻⁸; C4 analytic a₂^agg (T and L) 10⁻⁶; C5 a₄^agg 5×10⁻², even-basis rms ≤ 10⁻⁷ both, small-k confirmation ≤ 10⁻³ both; C6 control booleans; C7 arm token. Any MISS ⇒ S9: fingerprint with mechanism, no re-tuning, arms untouched; the chat side re-runs the same frozen comparator on return.

## 4. Return manifest (one commit on `claude/<descriptor>`)
Your instrument(s) (md5 + bytes); phase JSONs; the checkpoint (md5, bytes, pre-decode commit hash); comparator output verbatim (md5); `G_S2C1_P2_CCLEG_REPORT.md` with your D2 derivation, the structure-check result, honesty ledger H-CC-P2-1..n, deviations, the T1 scan output, the quarantine-decode commit hash, and non-claims (no observable, no bridge, no window action; PF-S2 executes only at fold on author authorization).

## 5. Non-claims
Not a fold; not a window action; the 3-D kinematic point of E-P2-1 (a propagating plane wave's strain carries helicity 0/±1, never pure ±2) rides with the election as disclosed and is not re-adjudicated here.

---

# EMBEDS (byte-exact; extract with the script; QUARANTINED = base64-armored)

### EMBED — ACTIVATION FLAGS (P-4) — `activation_P2_G_S2C1.json` (md5 ce053201caf19c1acf3e3c0907851732, 4734 B, raw)

<<<EMBED-BEGIN name=activation_P2_G_S2C1.json md5=ce053201caf19c1acf3e3c0907851732 bytes=4734 enc=raw quarantine=0>>>
{
 "BLIND_UNTIL_CC_CHECKPOINT_HASHED": true,
 "BRANCH_NAMING": "claude/<descriptor>",
 "CHECKPOINT_SCHEMA": "p2_cmp_v1 \u2014 exactly the chat checkpoint's blocks/keys: per_substrate[name]{C1_pin{Q_T_a,V_T,V_L,pin_pass}, C2_KK{alpha_tie_max_rel,pass}, C3_D0{T,L}, C4_a2_agg{T_analytic,L_analytic,CI_quadrature_rel}, C5_a4_agg{T_even_basis,T_a6,even_basis_rms,smallk_confirmation_rel}, C6_controls{F_AGG_DISP_pass,F_AGG_L_pass,F_CONV_pass,structure_no_odd_or_log_term}, C7_arm, a2_over_QT, a2L_over_a2T}, F_AGG_UNI{a2_over_QT_spread_rel}, plus schema/gate/phase/leg/prereg_md5/addenda_md5/source_md5/election_E_P2_1/shared_layer_flagged",
 "COMPARATOR_FROZEN": "g_s2c1_p2_compare.py md5 aa887e6c62b9898f92506549a11db9ae (tolerances in its header, fixed before your run); run after hashing + committing your checkpoint; the chat side re-runs it on return",
 "DISCLOSURE": "Addendum P2-A's text (embedded raw, lock chain) necessarily reveals the chat leg's structure finding (analytic in k^2, a3 = 0) and the extraction rule; the quarantined artifacts carry the numbers. Your independence rests on your own real-part method and your own derivation of D2.",
 "ELECTION_E_P2_1": "(a) the aggregate S2 channel = the polarization-averaged transverse shear cone (full SO(3) grain average; projector 1/2(I - p p), scattered T+L summed)",
 "EXECUTE_CC_LEG": true,
 "LOCK": {
  "T1": "8cd89b9a82704accd89f7ff6f5e220b4",
  "addendum_P2": "2feff442dfd08a379443d893b8c7761b",
  "addendum_P2A": "71b4c7010e48601e07f6458c711dfb4a",
  "prereg": "2ea8ec13ffa3c32898cc24a3be605c64"
 },
 "NO_FOLD_NO_WINDOW_ACTION": true,
 "P4b_BASE64_ARMOR_QUARANTINE": true,
 "REQUESTED_VARIATION": "compute Re Sigma_T by a method DIFFERENT from the chat leg's Cauchy-weight PV quadrature + regular tail: e.g. (i) a numerical Kramers-Kronig/Hilbert transform of alpha_T(k) computed on a wide k-grid, or (ii) closed-form partial fractions of the mu-integral followed by an analytic PV in q, or (iii) epsilon-regularised complex integration with Richardson extrapolation in epsilon; derive the analytic D2 yourself (do not read it off the addendum's formula until your derivation is written) and confirm the formula or disagree with it in writing",
 "S9_ON_ANY_MISS": true,
 "SHARED_LAYER_FLAGGED": "the SO(3)-covariance Xi and the mode kernels Phi_TM(mu) are the banked G-POLY1 layer (the chat leg imported the recovered G-POLY1 instrument for them); rebuild them yourself (your own quadrature/rotation scheme); the INDEPENDENT content of this gate is everything below",
 "SUBSTRATE_OBJECTS_BANKED": "the four pinned polycrystal tensors in poly_vrh_results.json (md5 200e7a8b775577564369c6924d38a84c; vrh -> hex:step, hex:gem8, cubic:step, cubic:gem8; Voigt V_T = sqrt(mu_bar), V_L = sqrt(lambda_bar + 2 mu_bar)); exponential two-point spectrum eta(q) = a_g^3/(pi^2 (1+q^2 a_g^2)^2), a_g = 1; the banked Q_T^a quartet in poly1_phase1full_cc.json (your own G-POLY1 output) is the F-AGG-PIN reference",
 "T1_SCAN": "zero hits on every CC instrument and checkpoint (pattern lines only; the numeric patterns collide with scientific-notation floats \u2014 if a machine-epsilon value hits, classify and log as H-item, do NOT reformat to dodge)",
 "VERIFY_THEN_BUILD": true,
 "WHAT_TO_COMPUTE": [
  "F-AGG-PIN: reproduce the Q_T^a quartet digit-for-digit (rel <= 1e-10) before anything else",
  "D(k) = Delta c_T/c_T(k) for the T channel (and the L channel as control) on the ladder k a_g in {0.3/2^j, j=0..8} U {0.005,0.01,0.015,0.02,0.03}; D(0) closed form = -1/4 sum_M N_M int Phi_TM dmu; sign fixed by positive attenuation (k_eff^2 = k^2 - Pi)",
  "F-AGG-KK: your Im-part tie-in alpha_T(k) = sum_M k k_M^3 N_M/2 F_M(k_M,k) must reproduce the banked alpha_T_a grid values (poly1_phase1full_cc.json) to <= 1e-9 rel",
  "a2_agg of record = the analytic D2 (P2-A) for T and L, quadrature-converged to <= 1e-6 rel (F-CONV: doubling of your rotation quadrature, your mu nodes, your q-integration parameters)",
  "structure check: R(k) = Delta(k) - D2 k^2 fitted on {k^4, k^6, k^8} (rms <= 1e-7) AND tested against {k^3, k^4} and {k^4, k^4 ln k}: report which basis the data selects; a4_agg = the even-basis k^4 coefficient; small-k confirmation Delta/k^2 -> D2 at k <= 0.005 (<= 1e-3 incl. the a4 k^2 contribution)",
  "F-AGG-DISP at tau_agg = 1e-6 with CI = your F-CONV term; F-AGG-L (L channel nonzero, analytic-controlled); F-AGG-UNI reported (a2_agg/Q_T^a across the quartet; a2_L/a2_T)",
  "arm per substrate per Addendum P2 \u00a7Falsifiers with P2-A's extraction rule; decided BEFORE the quarantine is decoded"
 ],
 "dispatch": "CC LEG \u2014 Probe P2 (aggregate inheritance), Phase 3",
 "dispatch_date": "2026-09-03",
 "display": "Gate G-S2-ON-CONE",
 "gate": "G-S2C1"
}
<<<EMBED-END name=activation_P2_G_S2C1.json>>>

### EMBED — ADDENDUM P2 (locked 2feff442) — `G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2.md` (md5 2feff442dfd08a379443d893b8c7761b, 4556 B, raw)

<<<EMBED-BEGIN name=G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2.md md5=2feff442dfd08a379443d893b8c7761b bytes=4556 enc=raw quarantine=0>>>
# G-S2C1 — LOCK RECORD ADDENDUM P2 (Phase 3 / Probe P2, the aggregate) — LOCKED September 3, 2026

**Authorization (verbatim, author):** "Election E-P2-1: I elect (a) (aggregate averages over full SO(3); S2 channel = polarization-averaged transverse shear cone). Probe P2 Execution: You are authorized to lock the P2 Addendum incorporating E-P2-1 and the F-AGG falsifiers, and execute the Aggregate Probe (Phase 3) using the recovered G-POLY1 Rayleigh machinery. Compute a₂^agg and a₄^agg."

## Substrate objects (banked, G-POLY1)
The four pinned polycrystal tensors (`poly_vrh_results.json` md5 200e7a8b775577564369c6924d38a84c → `vrh` → hex:step, hex:gem8, cubic:step, cubic:gem8), the SO(3)-covariance Ξ and mode kernels Φ_TM(μ) exactly as in the recovered `poly1_fullprec_ccleg.py` (branch gvbkof @ 231b555a, manifest-verified), Voigt reference velocities V_T = √μ̄, V_L = √(λ̄+2μ̄), the exponential two-point spectrum η̃(q) = a_g³/(π²(1+q²a_g²)²), a_g ≡ 1. Pin check (Phase 0 of P2): the banked quartet Q_T^a {3.519074e-2, 5.002055e-2, 5.407763e-2, 7.549430e-2} must be reproduced digit-for-digit before anything else.

## Operational definition (E-P2-1 (a))
Channel: the polarization-averaged transverse wave (projector ½(I − p⊗p), scattered T+L summed). Quantity: the second-order (Born/SOA) fractional phase-velocity shift, the real-part partner of the banked attenuation, with the SAME kernels and the SAME mode normalization N_M = 1/(V_T²V_M²) that reproduces α_T:
  D(k) ≡ Δc_T/c_T(k) = (1/π) Σ_{M∈{T,L}} N_M · J_M(k),   J_M(k) = PV∫₀^∞ dq q⁴ F_M(q,k)/(k_M² − q²),
  F_M(q,k) = ∫₋₁¹ dμ Φ_TM(μ)/(1 + k² + q² − 2kqμ)²,   k_M = k V_T/V_M   (k in units 1/a_g).
Sign fixed by positive attenuation (k_eff² = k² − Π). Closed-form anchor: D(0) = −(1/4) Σ_M N_M ∫Φ_TM dμ (static second-order velocity renormalization below Voigt). Tie-in: Im-part reproduction α_T(k) = Σ_M k k_M³ N_M/2 · F_M(k_M, k) must equal the recovered `alpha_finite` on the G-POLY1 grid {0.02,0.03,0.05,0.08,0.12} to 10⁻⁹ relative (F-AGG-KK).
Dispersion: Δ(k) ≡ D(k) − D(0) on the E-4-style dyadic ladder k a_g ∈ {0.3/2^j, j = 0..8} ∪ {0.005,0.01,0.015,0.02,0.03}. Pre-registered analytic structure (derived pre-data from the pole region q ≈ k_M): Δ(k) = a₂^agg k² + a₃^agg k³ + a₄^agg k⁴ + …, with a₃ (non-analytic, the KK partner of the k⁴ attenuation) EXPECTED nonzero. Fit bases: (i) the elected P1 basis {k², k⁴} ("a₂^agg,2"); (ii) the 3-term basis {k², k³, k⁴} ("a₂^agg,3", with a₃ banked). RULE (pre-data): a₂^agg OF RECORD = the 3-term k² coefficient if the two bases disagree beyond max(CI) (2-term misspecified by the pre-registered k³ term), else the elected 2-term coefficient; both always reported with window-stability CIs (nested upper edges 0.3/0.15/0.075). Analytic control on a₂^agg: the small-k expansion coefficient computed independently from the closed-form derivative formula (D₂ from ∂F/∂k² and the pole-shift term) must agree with the fitted a₂^agg,3 within its CI (F-AGG-ANALYTIC).

## Falsifiers (P2), τ_agg = 10⁻⁶
- **F-AGG-DISP:** |a₂^agg| > max(τ_agg, CI) ⇒ **A3-agg** (the shear cone in the aggregate is dispersive at the grain scale). a₂^agg = 0 at τ_agg with a₃ or a₄ ≠ 0 ⇒ **A2-agg**; all zero ⇒ **A1-agg**.
- **F-AGG-KK:** α_T reproduction on the G-POLY1 grid ≤ 10⁻⁹ rel; **F-AGG-PIN:** Q_T quartet digit-for-digit; either failing ⇒ **A5-agg** halt.
- **F-AGG-L (positive control):** the L channel (Φ_LM, N_M = 1/(V_L²V_M²)) through the identical pipeline: D_L(0) and a₂^agg,L nonzero and analytic-controlled.
- **F-CONV:** Ξ quadrature doubling (nb 10→20, na 12→24): |Δa₂^agg|/|a₂^agg| ≤ 10⁻⁶; μ-nodes 64→128: ≤ 10⁻⁹; PV quad epsrel 10⁻¹⁰; tail split Q_max 50→100: ≤ 10⁻⁹.
- **F-AGG-UNI (report only):** the banked Q′_G near-universality tested on a₂^agg/Q_T^a across the quartet.

## Consequence (PF-S2, unchanged)
a₂^agg is the grain-scale dispersion coefficient; with P1's lattice-scale a₂ it feeds W_∪′ at fold, after the CC leg. No window action in P2.

## Registers and non-claims
R1-machine for every number; R2 for the aggregate reading (conditional on G-POLY1's E3 elections and the Born/SOA order). No observable, no bridge (M.BRIDGE), no channel-speed-equality claim, no μ_n. Two-leg: chat leg on the recovered framework machinery + the new PV step; CC leg from scratch in a later dispatch.
<<<EMBED-END name=G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2.md>>>

### EMBED — ADDENDUM P2-A (author-authorized) — `G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2A.md` (md5 71b4c7010e48601e07f6458c711dfb4a, 1549 B, raw)

<<<EMBED-BEGIN name=G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2A.md md5=71b4c7010e48601e07f6458c711dfb4a bytes=1549 enc=raw quarantine=0>>>
# G-S2C1 — LOCK RECORD ADDENDUM P2-A (September 3, 2026)

**Authorization (verbatim, author):** "I explicitly AUTHORIZE Amendment P2-A. The analytic D2 closed-form value (which correctly uses the pure even basis) is the a₂^agg of record. The mechanical arm is confirmed as A3-agg DISPERSIVE (grain-scale k²)."

**Operational form (both legs):**
- a₂^agg of record = the analytic second-order coefficient D2 = (1/π)Σ_M N_M[−∫₀^∞ q²F₂(q)dq − r_M²∫₀^∞ F₀(q)dq], F₂ = −2I₀/A³ + 12q²I₂/A⁴, A = 1+q², I₀ = ∫Φ_TM dμ, I₂ = ∫Φ_TM μ² dμ, r_M = V_inc/V_M — closed form on the same Ξ/Φ kernels; converged in quadrature to ≤ 10⁻⁶ relative (F-CONV).
- The ladder is confirmation, not extraction: Δ(k)/k² → D2 in the small-k limit (agreement ≤ 10⁻³ at k ≤ 0.005 including the a₄k² contribution), and the remainder R(k) = Δ − D2·k² is fitted on the pure even basis {k⁴, k⁶, k⁸} with rms ≤ 10⁻⁷ (structure check: no odd or logarithmic term at this order); a₃ ≡ 0 (the pre-registered k³ term is REFUTED and retired, H-S2C-10); a₄^agg = the even-basis k⁴ coefficient.
- F-AGG-DISP: |a₂^agg| > max(τ_agg = 10⁻⁶, CI) with CI the F-CONV quadrature term ⇒ A3-agg; the remaining arm logic of Addendum P2 unchanged. F-AGG-KK, F-AGG-PIN, F-AGG-L, F-AGG-UNI unchanged.
- Amends the extraction rule and the retired k³ pre-registration only. E-P2-1 (a), τ_agg, the substrate objects, and the sign/normalization convention of Addendum P2 (2feff442) unchanged.
<<<EMBED-END name=G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2A.md>>>

### EMBED — T1 LIST (frozen) — `t1_forbidden_G_S2_ON_CONE.txt` (md5 8cd89b9a82704accd89f7ff6f5e220b4, 144 B, raw)

<<<EMBED-BEGIN name=t1_forbidden_G_S2_ON_CONE.txt md5=8cd89b9a82704accd89f7ff6f5e220b4 bytes=144 enc=raw quarantine=0>>>
graviton
gravitational wave
GW170817
GW150914
GRB 170817
LIGO
Virgo
speed of gravity
c_g
4.7e-23
1.27e-22
5e-16
Weinberg
Witten
Hulse
PSR B1913
<<<EMBED-END name=t1_forbidden_G_S2_ON_CONE.txt>>>

### EMBED — BANKED SUBSTRATE TENSORS (G-POLY1 input, 200e7a8b; b64 for byte-exactness — NOT quarantined) — `poly_vrh_results.json` (md5 200e7a8b775577564369c6924d38a84c, 2767 B, b64)

<<<EMBED-BEGIN name=poly_vrh_results.json md5=200e7a8b775577564369c6924d38a84c bytes=2767 enc=b64 quarantine=0>>>
ewogImdlbThfZmNjX2lzbyI6IHsKICAiQSI6IDk0Ni4yMzk3ODY0NDUwNjQ0LAogICJsaW4iOiAt
MjE0LjQ1MzEwMzQzMDUyMTMsCiAgImJhc2VfcmVzIjogNC43MTAwNzQ0MTg1MjIwMjI1ZS0wOSwK
ICAic2Vjb25kcyI6IDM4LjAwMzI0MDEwODQ4OTk5CiB9LAogInZyaCI6IHsKICAiY29udHJvbHMi
OiB7CiAgICJjdWJpY19jbG9zZWRfZm9ybV9tYXhlcnIiOiA0LjQ0MDg5MjA5ODUwMDYyNmUtMTYs
CiAgICJpc29fbnVsbCI6ICJQQVNTIgogIH0sCiAgImhleDpzdGVwIjogewogICAibGFiZWwiOiAi
VFJVRS1PUFRJTVVNIChWNC43MiBSMSB0d28tbGVnKSIsCiAgICJDX292ZXJfcmhvIjogewogICAg
IkMxMSI6IDIzOC40MTgzLAogICAgIkMxMiI6IDEwOC41Mzg5LAogICAgIkMxMyI6IDU3LjQ3NTEs
CiAgICAiQzMzIjogMjg3LjY2ODgsCiAgICAiQzQ0IjogNjAuMDMwOCwKICAgICJDNjYiOiA2NC45
MjIzCiAgIH0sCiAgICJLX1ZSSCI6IDEzNC42MDksCiAgICJHX1YiOiA3My4wNjUsCiAgICJHX1Ii
OiA2OC42OTcsCiAgICJHX1ZSSCI6IDcwLjg4MSwKICAgIlZSX3NwcmVhZF9wY3QiOiA2LjE2LAog
ICAiQVUiOiAwLjMxNzksCiAgICJ2VF9WIjogOC41NDc4LAogICAidlRfUiI6IDguMjg4MywKICAg
InZUX1ZSSCI6IDguNDE5MSwKICAgInZUX2hhbGZ3aWR0aF9wY3QiOiAxLjU0LAogICAic2luZ2xl
X2NyeXN0YWxfaW5wdXQiOiB7CiAgICAibWVhbiI6IDguNDcyNzQyNjY0NzUzMjU5LAogICAgInN0
ZF9wY3QiOiA5LjE2NDI1OTAyNTQ1ODgzNSwKICAgICJtYXhkZXZfcGN0IjogMTkuMTA1MzgyNDEx
MjIzNDUyCiAgIH0KICB9LAogICJoZXg6Z2VtOCI6IHsKICAgImxhYmVsIjogIlRSVUUtT1BUSU1V
TSAoVjQuNzIgUjEgdHdvLWxlZykiLAogICAiQ19vdmVyX3JobyI6IHsKICAgICJDMTEiOiAzNzcu
NTQzOCwKICAgICJDMTIiOiAyMDAuMjA3NiwKICAgICJDMTMiOiAxMTEuMDAxOCwKICAgICJDMzMi
OiA0NjcuNzU1NCwKICAgICJDNDQiOiA4NC44MjQ1LAogICAgIkM2NiI6IDg4LjY4MzUKICAgfSwK
ICAgIktfVlJIIjogMjI5LjY5NiwKICAgIkdfViI6IDEwNS4wNDIsCiAgICJHX1IiOiA5Ni42MywK
ICAgIkdfVlJIIjogMTAwLjgzNiwKICAgIlZSX3NwcmVhZF9wY3QiOiA4LjM0LAogICAiQVUiOiAw
LjQzNTIsCiAgICJ2VF9WIjogMTAuMjQ5LAogICAidlRfUiI6IDkuODMwMSwKICAgInZUX1ZSSCI6
IDEwLjA0MTcsCiAgICJ2VF9oYWxmd2lkdGhfcGN0IjogMi4wOSwKICAgInNpbmdsZV9jcnlzdGFs
X2lucHV0IjogewogICAgIm1lYW4iOiAxMC4xMjAzMTU1NTE2ODcyMTUsCiAgICAic3RkX3BjdCI6
IDEwLjkwNjQxOTM1MDYyOTA3MiwKICAgICJtYXhkZXZfcGN0IjogMjIuNTkwMjgwNTIyMTcxNzgK
ICAgfQogIH0sCiAgImN1YmljOnN0ZXAiOiB7CiAgICJsYWJlbCI6ICJwb2xpc2hlZC1hdC1GUk9a
RU4gZ2VvbWV0cnkgKGxhYmVsbGVkKSIsCiAgICJDX292ZXJfcmhvIjogewogICAgIkM0NCI6IDg1
LjI5MzQsCiAgICAiQzEyIjogOTkuMzQ5LAogICAgIkMxMSI6IDE3Mi43OTk0CiAgIH0sCiAgICJL
X1ZSSCI6IDEyMy44MzIsCiAgICJHX1YiOiA2NS44NjYsCiAgICJHX1IiOiA1NS43ODQsCiAgICJH
X1ZSSCI6IDYwLjgyNSwKICAgIlZSX3NwcmVhZF9wY3QiOiAxNi41OCwKICAgIkFVIjogMC45MDM3
LAogICAidlRfViI6IDguMTE1OCwKICAgInZUX1IiOiA3LjQ2ODksCiAgICJ2VF9WUkgiOiA3Ljc5
OSwKICAgInZUX2hhbGZ3aWR0aF9wY3QiOiA0LjE1LAogICAic2luZ2xlX2NyeXN0YWxfaW5wdXQi
OiB7CiAgICAibWVhbiI6IDcuOTczNTk4MzY1MjY0NTEsCiAgICAic3RkX3BjdCI6IDEzLjExMzM3
MjI2NDQ0OTExNywKICAgICJtYXhkZXZfcGN0IjogMjMuOTk1ODY4Mjc3MjQ5MDM0CiAgIH0KICB9
LAogICJjdWJpYzpnZW04IjogewogICAibGFiZWwiOiAicG9saXNoZWQtYXQtRlJPWkVOIGdlb21l
dHJ5IChsYWJlbGxlZDsgaXNvIG1lYXN1cmVkIHRoaXMgc2Vzc2lvbikiLAogICAiQ19vdmVyX3Jo
byI6IHsKICAgICJDNDQiOiAxMzEuNTQzNiwKICAgICJDMTIiOiAxNzkuMzc1NiwKICAgICJDMTEi
OiAyNzIuMDc1MwogICB9LAogICAiS19WUkgiOiAyMTAuMjc2LAogICAiR19WIjogOTcuNDY2LAog
ICAiR19SIjogNzUuODA4LAogICAiR19WUkgiOiA4Ni42MzcsCiAgICJWUl9zcHJlYWRfcGN0Ijog
MjUuMCwKICAgIkFVIjogMS40Mjg1LAogICAidlRfViI6IDkuODcyNSwKICAgInZUX1IiOiA4Ljcw
NjgsCiAgICJ2VF9WUkgiOiA5LjMwNzksCiAgICJ2VF9oYWxmd2lkdGhfcGN0IjogNi4yNiwKICAg
InNpbmdsZV9jcnlzdGFsX2lucHV0IjogewogICAgIm1lYW4iOiA5LjYzNzA1NDY0Mzk4MDA3LAog
ICAgInN0ZF9wY3QiOiAxNS44MDgzMjA2OTY5MjgxMjQsCiAgICAibWF4ZGV2X3BjdCI6IDI5LjM1
MTY4NDE2ODA3MzM2NgogICB9CiAgfSwKICAibWl4dHVyZTpzdGVwIjogewogICAiZl9oY3AgLT4g
dlQiOiB7CiAgICAiMC4wIjogNy43OTksCiAgICAiMC4yNSI6IDcuOTQ5OSwKICAgICIwLjUiOiA4
LjEwMzIsCiAgICAiMC43NSI6IDguMjU5NCwKICAgICIxLjAiOiA4LjQxOTEKICAgfSwKICAgInBo
YXNlX3NwYW5fcGN0IjogNy42NQogIH0sCiAgIm1peHR1cmU6Z2VtOCI6IHsKICAgImZfaGNwIC0+
IHZUIjogewogICAgIjAuMCI6IDkuMzA3OSwKICAgICIwLjI1IjogOS40ODY0LAogICAgIjAuNSI6
IDkuNjY3OSwKICAgICIwLjc1IjogOS44NTI3LAogICAgIjEuMCI6IDEwLjA0MTcKICAgfSwKICAg
InBoYXNlX3NwYW5fcGN0IjogNy41OQogIH0KIH0KfQ==
<<<EMBED-END name=poly_vrh_results.json>>>

### EMBED — BANKED Q_T QUARTET + alpha grid (your G-POLY1 Phase-1 output; F-AGG-PIN / F-AGG-KK reference) — `poly1_phase1full_cc.json` (md5 ec87e42f0f617b00c4985ba2aceac339, 8140 B, b64)

<<<EMBED-BEGIN name=poly1_phase1full_cc.json md5=ec87e42f0f617b00c4985ba2aceac339 bytes=8140 enc=b64 quarantine=0>>>
ewogInBoYXNlMWEiOiB7CiAgInN0ZXBfaGV4IjogewogICAic3ltIjogImhleCIsCiAgICJLVl9w
aW5uZWQiOiAxMzQuNjA5Mjg4ODg4ODg4OSwKICAgIktSX3Bpbm5lZCI6IDEzNC42MTU5MjYwODk3
NDMxNywKICAgIkdWX3Bpbm5lZCI6IDczLjA2MjIxMzMzMzMzMzMzLAogICAiR1JfcGlubmVkIjog
NjguNjkzNTgwMjM5NTI2MjcsCiAgICJLVl9nZW4iOiAxMzQuNjA5Mjg4ODg4ODg4OSwKICAgIkdW
X2dlbiI6IDczLjA2NDUzMzMzMzMzMzM0LAogICAiS1JfZ2VuIjogMTM0LjYwODIzMzU5NTM5MDE3
LAogICAiR1JfZ2VuIjogNjguNjk2NTk3MDI5MzE1MTMsCiAgICJxdWFkX2RvdWJsaW5nX3JlbCI6
IDcuMDI3NzExNzQ1ODc3MjQxZS0xNCwKICAgIm1lYW5fdnNfdm9pZ3Rpc29fcmVsIjogMi4xNDI0
MTQ1Njc0ODQ5NTVlLTE1LAogICAiVl90b3QiOiA5MDU4LjU3MzM2NzA1MjY3NSwKICAgIlZfdG90
X2Nsb3NlZCI6IDkwNTguNTczMzY3MDUzMjM1LAogICAiVl90b3RfcmVsX3Jlc2lkIjogNi4xODM5
NDIyNDcxNjIxMjJlLTE0LAogICAiUGhpX0ciOiAxLjY5Njk2OTk3MDMxMzk1NywKICAgIlBoaV9m
dWxsIjogMC4wMzM1Njk0ODUwOTc2ODk1OTYsCiAgICJwaW5uZWRfNDZpX2NvbnRyYWN0aW9ucyI6
IHsKICAgICJkYzE1X3NxIjogMTE2LjM3MTQyMDQyNjA2MzI4LAogICAgImRjMjVfc3EiOiAxMDAu
MzcyMDYyNjgyNjk3OTIsCiAgICAiZGMzNV9zcSI6IDExNi4zNzE0MjA0MjYwNjMyNCwKICAgICJk
YzQ1X3NxIjogNzguNDczNjg0MTA2NzkzNDMsCiAgICAiZGM1NV9zcSI6IDEyOS4zODczMTQ0MDYy
NDkwNiwKICAgICJkYzU2X3NxIjogNzguNDczNjg0MTA2NzkzMzcsCiAgICAiZGMxNWRjMjUiOiAt
NDguNTc1NjI2NjU5MjA2MzksCiAgICAiZGMxNWRjMzUiOiAtNjkuMjk2NTk2NTUyNjY2MzMsCiAg
ICAiZGMyNWRjMzUiOiAtNDguNTc1NjI2NjU5MjA2MTE1CiAgIH0KICB9LAogICJnZW04X2hleCI6
IHsKICAgInN5bSI6ICJoZXgiLAogICAiS1ZfcGlubmVkIjogMjI5LjY5NjE1NTU1NTU1NTU4LAog
ICAiS1JfcGlubmVkIjogMjI5LjY4OTA4Nzc4NDE3MSwKICAgIkdWX3Bpbm5lZCI6IDEwNS4wNDQw
MDY2NjY2NjY2NiwKICAgIkdSX3Bpbm5lZCI6IDk2LjYzMzQ0MzUwNDY4NjExLAogICAiS1ZfZ2Vu
IjogMjI5LjY5NjE1NTU1NTU1NTUyLAogICAiR1ZfZ2VuIjogMTA1LjA0MTk1MzMzMzMzMzMyLAog
ICAiS1JfZ2VuIjogMjI5LjY5NTk0NTMwODcyNDM2LAogICAiR1JfZ2VuIjogOTYuNjMwNDAwNzgx
NTIxODEsCiAgICJxdWFkX2RvdWJsaW5nX3JlbCI6IDguNjkzMDQ2MjgyODE0OTc2ZS0xMywKICAg
Im1lYW5fdnNfdm9pZ3Rpc29fcmVsIjogMy43NzA3MTY5ODUyMzYyODZlLTE1LAogICAiVl90b3Qi
OiAyNjgyNi45ODU2NzA4NTU2ODQsCiAgICJWX3RvdF9jbG9zZWQiOiAyNjgyNi45ODU2NzA4NTg3
NiwKICAgIlZfdG90X3JlbF9yZXNpZCI6IDEuMTQ2ODYwMzg0NDM3Nzg2N2UtMTMsCiAgICJQaGlf
RyI6IDIuNDMxMjQ4MzI4NzI4MTA2NiwKICAgIlBoaV9mdWxsIjogMC4wMzg1NzExNjczMjU3NTky
MTUsCiAgICJwaW5uZWRfNDZpX2NvbnRyYWN0aW9ucyI6IHsKICAgICJkYzE1X3NxIjogMzMzLjY5
NTUyNTg5MDY2NzMsCiAgICAiZGMyNV9zcSI6IDMwMy45NTIxNzM0Mjg5NTQxLAogICAgImRjMzVf
c3EiOiAzMzMuNjk1NTI1ODkwNjY2NTQsCiAgICAiZGM0NV9zcSI6IDIzNi4yMTUxMDA1OTY5NTIz
LAogICAgImRjNTVfc3EiOiAzODMuMjM2MjI5MzcwMTE1MywKICAgICJkYzU2X3NxIjogMjM2LjIx
NTEwMDU5Njk1MTk3LAogICAgImRjMTVkYzI1IjogLTE1My42MDYzNTE1MzQwOTM3LAogICAgImRj
MTVkYzM1IjogLTE3OC40MjUxODg0MTU2MTc5NSwKICAgICJkYzI1ZGMzNSI6IC0xNTMuNjA2MzUx
NTM0MDk0MzYKICAgfQogIH0sCiAgInN0ZXBfY3ViaWMiOiB7CiAgICJzeW0iOiAiY3ViaWMiLAog
ICAiS1ZfcGlubmVkIjogMTIzLjgzMjQ2NjY2NjY2NjY2LAogICAiS1JfcGlubmVkIjogMTIzLjgz
MjQ2NjY2NjY2NjY2LAogICAiR1ZfcGlubmVkIjogNjUuODY2MTIsCiAgICJHUl9waW5uZWQiOiA1
NS43ODQxMjg3NDUxNTk2MSwKICAgIktWX2dlbiI6IDEyMy44MzI0NjY2NjY2NjY2OCwKICAgIkdW
X2dlbiI6IDY1Ljg2NjEyLAogICAiS1JfZ2VuIjogMTIzLjgzMjQ2NjY2NjY2NjcyLAogICAiR1Jf
Z2VuIjogNTUuNzg0MTI4NzQ1MTU5NjA2LAogICAicXVhZF9kb3VibGluZ19yZWwiOiAyLjI4MDM5
ODA5MjU4MDA3MTVlLTEzLAogICAibWVhbl92c192b2lndGlzb19yZWwiOiA2LjE3NTczNDM0MzQ1
NTA4OWUtMTUsCiAgICJWX3RvdCI6IDExMzIyLjU3NjI0NTk1MDYzLAogICAiVl90b3RfY2xvc2Vk
IjogMTEzMjIuNTc2MjQ1OTUxOTMyLAogICAiVl90b3RfcmVsX3Jlc2lkIjogMS4xNTAxOTEwNTM1
MTE2NjIyZS0xMywKICAgIlBoaV9HIjogMi42MDk4ODMzMjAxMDkzNDQzLAogICAiUGhpX2Z1bGwi
OiAwLjA1MDM3MjQzMzQ5OTg3MzMsCiAgICJwaW5uZWRfNDZpX2NvbnRyYWN0aW9ucyI6IHsKICAg
ICJkYzE1X3NxIjogMTc5LjcyMzQzMjQ3NTQyNzgsCiAgICAiZGMyNV9zcSI6IDg5Ljg2MTcxNjIz
NzcxNDEzLAogICAgImRjMzVfc3EiOiAxNzkuNzIzNDMyNDc1NDI5NDMsCiAgICAiZGM0NV9zcSI6
IDg5Ljg2MTcxNjIzNzcxMzk2LAogICAgImRjNTVfc3EiOiAxNjEuNzUxMDg5MjI3ODUxNDgsCiAg
ICAiZGM1Nl9zcSI6IDg5Ljg2MTcxNjIzNzcxNDMsCiAgICAiZGMxNWRjMjUiOiAtNDQuOTMwODU4
MTE4ODU3MDQ2LAogICAgImRjMTVkYzM1IjogLTEzNC43OTI1NzQzNTY1NzExLAogICAgImRjMjVk
YzM1IjogLTQ0LjkzMDg1ODExODg1Njg5CiAgIH0sCiAgICJudSI6IC05Ny4xMzY0MDAwMDAwMDAw
MiwKICAgImNsb3NlZF9iYXNpc19maXRfcmVzaWQiOiAyLjE4MTg1NjY4MzMyOTc4NTRlLTEyLAog
ICAiYWJjX21hY2hpbmUiOiBbCiAgICAxMS45ODE1NjIxNjUwMDMyMTMsCiAgICA1Mi40MTkzMzQ0
NzE5OTg0MywKICAgIC0xNC45NzY5NTI3MDYyODQ2NTgKICAgXSwKICAgImFfdnNfcGlubmVkX2Ns
ZWFuX3N0cmluZ19yZWwiOiAyLjExNjg2MjI0MTA1Mjc4NmUtMTIsCiAgICJiY19waW5uZWRfc3Ry
aW5ncyI6ICJjb3JydXB0ZWQgaW4gdHJhbnNwb3J0IC0tIG5vdCBjb25zdW1lZCAocGluIEUzKTsg
bWFjaGluZSB2YWx1ZXMgYWJvdmUiLAogICAiY3ViaWNfY29sbGFwc2VfcmVsIjogMS4yMTQ1ODM5
ODg5Mzk5MjEzZS0xMywKICAgIkFfYW5jaG9yX3JlbCI6IDIuMTY4NzA5NjU2MzAyNzgwOGUtMTIK
ICB9LAogICJnZW04X2N1YmljIjogewogICAic3ltIjogImN1YmljIiwKICAgIktWX3Bpbm5lZCI6
IDIxMC4yNzU1LAogICAiS1JfcGlubmVkIjogMjEwLjI3NTUsCiAgICJHVl9waW5uZWQiOiA5Ny40
NjYxMDAwMDAwMDAwMSwKICAgIkdSX3Bpbm5lZCI6IDc1LjgwNzg3MDQzNzg1NDgsCiAgICJLVl9n
ZW4iOiAyMTAuMjc1NTAwMDAwMDAwMDIsCiAgICJHVl9nZW4iOiA5Ny40NjYxMDAwMDAwMDAwNCwK
ICAgIktSX2dlbiI6IDIxMC4yNzU1MDAwMDAwMDAwNSwKICAgIkdSX2dlbiI6IDc1LjgwNzg3MDQz
Nzg1NDc5LAogICAicXVhZF9kb3VibGluZ19yZWwiOiA0LjE0NTU3Mjc3Mzk1MDMzNDVlLTEzLAog
ICAibWVhbl92c192b2lndGlzb19yZWwiOiA0LjkxNDY1Nzc5OTU2NTczMWUtMTUsCiAgICJWX3Rv
dCI6IDM0ODM4LjI4MDE4NzQ5NDk2NiwKICAgIlZfdG90X2Nsb3NlZCI6IDM0ODM4LjI4MDE4NzQ5
OTcxLAogICAiVl90b3RfcmVsX3Jlc2lkIjogMS4zNjIyNDM2NTEyMTUwNjdlLTEzLAogICAiUGhp
X0ciOiAzLjY2NzMyNjEwOTg5Nzg2NzMsCiAgICJQaGlfZnVsbCI6IDAuMDU5MjU1MzM3NjQzNTg0
NDUsCiAgICJwaW5uZWRfNDZpX2NvbnRyYWN0aW9ucyI6IHsKICAgICJkYzE1X3NxIjogNTUyLjk4
ODU3NDQwNDc1NjcsCiAgICAiZGMyNV9zcSI6IDI3Ni40OTQyODcyMDIzODAyLAogICAgImRjMzVf
c3EiOiA1NTIuOTg4NTc0NDA0NzY0MSwKICAgICJkYzQ1X3NxIjogMjc2LjQ5NDI4NzIwMjM3OTE2
LAogICAgImRjNTVfc3EiOiA0OTcuNjg5NzE2OTY0MzcyNTYsCiAgICAiZGM1Nl9zcSI6IDI3Ni40
OTQyODcyMDIzODAyNCwKICAgICJkYzE1ZGMyNSI6IC0xMzguMjQ3MTQzNjAxMTkwNTQsCiAgICAi
ZGMxNWRjMzUiOiAtNDE0Ljc0MTQzMDgwMzU3MDMsCiAgICAiZGMyNWRjMzUiOiAtMTM4LjI0NzE0
MzYwMTE5MDM0CiAgIH0sCiAgICJudSI6IC0xNzAuMzg3NDk5OTk5OTk5OTYsCiAgICJjbG9zZWRf
YmFzaXNfZml0X3Jlc2lkIjogMi4wNjI1NDM4NzkyNjcxNjhlLTEyLAogICAiYWJjX21hY2hpbmUi
OiBbCiAgICAzNi44NjU5MDQ5NjAyODQwMywKICAgIDE2MS4yODgzMzQyMDEzODA1NCwKICAgIC00
Ni4wODIzODEyMDAzOTUyMwogICBdLAogICAiYV92c19waW5uZWRfY2xlYW5fc3RyaW5nX3JlbCI6
IDkuMDY0OTcwOTk2MDY0NDAzZS0xMywKICAgImJjX3Bpbm5lZF9zdHJpbmdzIjogImNvcnJ1cHRl
ZCBpbiB0cmFuc3BvcnQgLS0gbm90IGNvbnN1bWVkIChwaW4gRTMpOyBtYWNoaW5lIHZhbHVlcyBh
Ym92ZSIsCiAgICJjdWJpY19jb2xsYXBzZV9yZWwiOiAxLjQ0MTA2OTQ4NTk2MzQ1MzJlLTEzLAog
ICAiQV9hbmNob3JfcmVsIjogMi40OTg2Njc5MzkyMjEzNzczZS0xMgogIH0KIH0sCiAicGhhc2Ux
YiI6IHsKICAic3RlcF9oZXgiOiB7CiAgICJtdV9iYXIiOiA3My4wNjQ1MzMzMzMzMzMzNCwKICAg
ImxhbV9iYXIiOiA4NS44OTk1OTk5OTk5OTk5OSwKICAgIlZUMCI6IDguNTQ3Nzc5NDM4NzM5MjQs
CiAgICJWTDAiOiAxNS4yMzI0ODcyMTIwOTU5NSwKICAgImludF9QaGlfVFQiOiAzNjIuMjg0NDgw
MzM3NDQzNzcsCiAgICJpbnRfUGhpX1RMIjogMjQxLjU3MTY5ODg0NTU1NDQ0LAogICAiUV9UX2Ei
OiAwLjAzNTE5MDczODg2NjA3MDAyLAogICAiUV9UX1RUX2EiOiAwLjAzMzkzMTc2OTIzNDg3MzI0
NiwKICAgIlFfVF9UTF9hIjogMC4wMDEyNTg5Njk2MzExOTY3NzQsCiAgICJRX0xfYSI6IDAuMDgz
NjMxOTQ5MTU3OTI1OTcsCiAgICJrVGFfZ3JpZCI6IFsKICAgIDAuMDIsCiAgICAwLjAzLAogICAg
MC4wNSwKICAgIDAuMDgsCiAgICAwLjEyCiAgIF0sCiAgICJhbHBoYV9UX2EiOiBbCiAgICA1LjYy
MTYzMzk1NDkwMzczNmUtMDksCiAgICAyLjg0MDM1MDIwODUyNzQ5M2UtMDgsCiAgICAyLjE3Nzkx
MDgwNTUwMjU3ODVlLTA3LAogICAgMS40MDU4NzExMjE5MzE0NzUzZS0wNiwKICAgIDYuOTA0NTE0
MzU4MTI1NTc3ZS0wNgogICBdLAogICAiZml0X2V4cG9uZW50IjogMy45OTA4NTc0MzkzMDE4NzI4
LAogICAiUV9leHRfcmljaGFyZHNvbiI6IDAuMDM1MTkwNTQwNDI2OTYzMzgsCiAgICJRX1RfZCI6
IDAuMDA0Mzk4ODQyMzU4MjU4NzUyNiwKICAgIlFwcmltZV9HIjogMC4wMDI1OTIxNzQ1NDM1NzQ4
MTcsCiAgICJzdGF0dXMiOiAiRlVMTCIKICB9LAogICJnZW04X2hleCI6IHsKICAgIm11X2JhciI6
IDEwNS4wNDE5NTMzMzMzMzMzMiwKICAgImxhbV9iYXIiOiAxNTkuNjY4MTg2NjY2NjY2NjYsCiAg
ICJWVDAiOiAxMC4yNDg5OTc2NzQ1Njk2MTIsCiAgICJWTDAiOiAxOS4yMjg5Mzg5NTQ5NTM2MywK
ICAgImludF9QaGlfVFQiOiAxMDczLjA2MTQ0MjIzNjMwNDksCiAgICJpbnRfUGhpX1RMIjogNzE1
LjM4OTI4MTk4OTI0NDIsCiAgICJRX1RfYSI6IDAuMDUwMDIwNTQ4NDc4NTMyMDksCiAgICJRX1Rf
VFRfYSI6IDAuMDQ4NjI2MDUyNjMzNDE0MzQsCiAgICJRX1RfVExfYSI6IDAuMDAxMzk0NDk1ODQ1
MTE3NzQ3NCwKICAgIlFfTF9hIjogMC4xMjUxMzI1MjU3MjM1NTEzOCwKICAgImtUYV9ncmlkIjog
WwogICAgMC4wMiwKICAgIDAuMDMsCiAgICAwLjA1LAogICAgMC4wOCwKICAgIDAuMTIKICAgXSwK
ICAgImFscGhhX1RfYSI6IFsKICAgIDcuOTkwNjMwNDc4OTA4Njk4ZS0wOSwKICAgIDQuMDM3Mjc1
NjQ4MzYxMTQ2ZS0wOCwKICAgIDMuMDk1NjM5MDE0ODg2NzdlLTA3LAogICAgMS45OTgyMDczMDAz
OTA0ZS0wNiwKICAgIDkuODEyOTA1NDU1OTU4NDU2ZS0wNgogICBdLAogICAiZml0X2V4cG9uZW50
IjogMy45OTA4MzYzNTQ3MzYyNjQsCiAgICJRX2V4dF9yaWNoYXJkc29uIjogMC4wNTAwMjAyNjU0
OTY1MDE2MywKICAgIlFfVF9kIjogMC4wMDYyNTI1Njg1NTk4MTY1MTEsCiAgICJRcHJpbWVfRyI6
IDAuMDAyNTcxNzUyMzMyMzAzOTE4LAogICAic3RhdHVzIjogIkZVTEwiCiAgfSwKICAic3RlcF9j
dWJpYyI6IHsKICAgIm11X2JhciI6IDY1Ljg2NjEyLAogICAibGFtX2JhciI6IDc5LjkyMTcyMDAw
MDAwMDAyLAogICAiVlQwIjogOC4xMTU3OTQ0Nzc0MzcxOSwKICAgIlZMMCI6IDE0LjU0ODMzMTg2
MzEzODEyNCwKICAgImludF9QaGlfVFQiOiA0NTIuOTAzMDQ5ODM4MDUxODYsCiAgICJpbnRfUGhp
X1RMIjogMzAxLjkzNTM2NjU1ODcwMTYsCiAgICJRX1RfYSI6IDAuMDU0MDc3NjI4MjQ2NTE4NjQs
CiAgICJRX1RfVFRfYSI6IDAuMDUyMTk3NjY2NDAyMTg5OTgsCiAgICJRX1RfVExfYSI6IDAuMDAx
ODc5OTYxODQ0MzI4NjYwNywKICAgIlFfTF9hIjogMC4xMjkyNTIzNzQ3ODQxNTM2NiwKICAgImtU
YV9ncmlkIjogWwogICAgMC4wMiwKICAgIDAuMDMsCiAgICAwLjA1LAogICAgMC4wOCwKICAgIDAu
MTIKICAgXSwKICAgImFscGhhX1RfYSI6IFsKICAgIDguNjM4NzY0MjcyOTQ2ODgyZS0wOSwKICAg
IDQuMzY0NzYzNjA1NDAyMzUxNGUtMDgsCiAgICAzLjM0Njc4ODkyNjg2ODkyNTZlLTA3LAogICAg
Mi4xNjAzOTQwNDQ2OTcxMDg2ZS0wNiwKICAgIDEuMDYxMDE2MDMzMDAyNDJlLTA1CiAgIF0sCiAg
ICJmaXRfZXhwb25lbnQiOiAzLjk5MDg1NTMzNjI2MDMxMSwKICAgIlFfZXh0X3JpY2hhcmRzb24i
OiAwLjA1NDA3NzMyMTcyMDk5OTU3LAogICAiUV9UX2QiOiAwLjAwNjc1OTcwMzUzMDgxNDgzLAog
ICAiUXByaW1lX0ciOiAwLjAwMjU5MDA0MDUxMjA1MzA5MjMsCiAgICJzdGF0dXMiOiAiRlVMTCIs
CiAgICJlcHNfTCI6IDAuMDQwMDU5NTM5MjA4NDY5MjUsCiAgICJlcHNfVCI6IDAuMDk2NTQ1Mzg3
NTUxODM3NTMKICB9LAogICJnZW04X2N1YmljIjogewogICAibXVfYmFyIjogOTcuNDY2MTAwMDAw
MDAwMDQsCiAgICJsYW1fYmFyIjogMTQ1LjI5ODA5OTk5OTk5OTk4LAogICAiVlQwIjogOS44NzI0
OTIwODY2MDEwMzMsCiAgICJWTDAiOiAxOC40NDUzMzI3NDMwMDAzMywKICAgImludF9QaGlfVFQi
OiAxMzkzLjUzMTIwNzUwMDA3MDIsCiAgICJpbnRfUGhpX1RMIjogOTI5LjAyMDgwNTAwMDA0NCwK
ICAgIlFfVF9hIjogMC4wNzU0OTQzMDIwNzEyMDc3OCwKICAgIlFfVF9UVF9hIjogMC4wNzMzNDY1
MjIxOTc5NzE2MSwKICAgIlFfVF9UTF9hIjogMC4wMDIxNDc3Nzk4NzMyMzYxNjU1LAogICAiUV9M
X2EiOiAwLjE4ODA2NzAwNjA3MjgyODksCiAgICJrVGFfZ3JpZCI6IFsKICAgIDAuMDIsCiAgICAw
LjAzLAogICAgMC4wNSwKICAgIDAuMDgsCiAgICAwLjEyCiAgIF0sCiAgICJhbHBoYV9UX2EiOiBb
CiAgICAxLjIwNTk5ODg1OTE2MjM5OGUtMDgsCiAgICA2LjA5MzMyNjE0MDc4ODM5ZS0wOCwKICAg
IDQuNjcyMTUyNDg0NzQ4NDk4ZS0wNywKICAgIDMuMDE1ODQ5NDI1MzA2NDAyM2UtMDYsCiAgICAx
LjQ4MTA2Nzc0NTQ4MTc2NTRlLTA1CiAgIF0sCiAgICJmaXRfZXhwb25lbnQiOiAzLjk5MDgzODUy
MzAxNDk2MywKICAgIlFfZXh0X3JpY2hhcmRzb24iOiAwLjA3NTQ5Mzg3MjczNDQwMjkzLAogICAi
UV9UX2QiOiAwLjAwOTQzNjc4Nzc1ODkwMDk3MiwKICAgIlFwcmltZV9HIjogMC4wMDI1NzMyMDY2
MDIzMzM5NzY3LAogICAic3RhdHVzIjogIkZVTEwiLAogICAiZXBzX0wiOiAwLjA0MzcxMzQ1MDI5
ODMyNDU2LAogICAiZXBzX1QiOiAwLjExNDQ0NDcxNzAwMTg2NTY1CiAgfQogfSwKICJfbWV0YSI6
IHsKICAiaW5zdHJ1bWVudCI6ICJwb2x5MV9mdWxscHJlY19jY2xlZy5weSIsCiAgImxlZyI6ICJj
YyIsCiAgImlucHV0X2ZpbGUiOiAicG9seV92cmhfcmVzdWx0cy5qc29uIiwKICAiaW5wdXRfbWQ1
IjogIjIwMGU3YThiNzc1NTc3NTY0MzY5YzY5MjRkMzhhODRjIiwKICAicGluX3JlY29yZF9tZDUi
OiAiNjIxMTIwZTUwZDM5NWJlZWEyZTkxNGQ1NGM5Mjk2MDAiLAogICJwcmVyZWdfbWQ1IjogImRh
YjQ2MmQyZTEzM2QwOTYyYzUxMmEzNGJiN2JjNjM1IiwKICAidGltZSI6ICIyMDI2LTA4LTA1IDA0
OjA2OjUxLjYyNTMxMCswMDowMCIsCiAgInBoYXNlIjogIjEtZnVsbCIKIH0KfQ==
<<<EMBED-END name=poly1_phase1full_cc.json>>>

### EMBED — FROZEN P2 COMPARATOR — `g_s2c1_p2_compare.py` (md5 aa887e6c62b9898f92506549a11db9ae, 4204 B, raw)

<<<EMBED-BEGIN name=g_s2c1_p2_compare.py md5=aa887e6c62b9898f92506549a11db9ae bytes=4204 enc=raw quarantine=0>>>
#!/usr/bin/env python3
# g_s2c1_p2_compare.py — Gate G-S2C1 Probe P2 (aggregate) two-leg comparator (FROZEN pre-return). Schema p2_cmp_v1.
# Usage: python3 g_s2c1_p2_compare.py s2c1_p2_chat_cmp_checkpoint.json s2c1_p2_cc_cmp_checkpoint.json
# Tolerances fixed BEFORE the CC leg runs (per substrate; all four substrates):
#   C1 pin        Q_T_a, V_T, V_L rel <= 1e-10 (both legs reproduce the bank) ; pin_pass identical True
#   C2 KK         alpha tie-in <= 1e-9 on both legs (boolean identical True) ; values reported
#   C3 D0         static shift, T and L, rel <= 1e-8
#   C4 a2_agg     analytic D2, T and L, rel <= 1e-6 (closed form on the same kernels; absorbs quadrature-scheme differences)
#   C5 a4_agg     even-basis k^4 coefficient rel <= 5e-2 (fit-dependent) ; even-basis rms <= 1e-7 on both legs ; small-k confirmation <= 1e-3 both
#   C6 controls   F_AGG_DISP, F_AGG_L, F_CONV, structure booleans identical True
#   C7 arm        base arm token identical ("A3-agg")
# Any MISS -> S9 (prereg §8). Provenance fields reported, never compared.
import json, sys, hashlib
def load(p): return json.load(open(p, encoding="utf-8"))
def rel(a, b): return abs(a - b) / max(abs(a), abs(b), 1e-300)
def main(cp, cc):
    A, B = load(cp), load(cc)
    for p in (cp, cc): print("checkpoint %s md5 %s" % (p, hashlib.md5(open(p, "rb").read()).hexdigest()))
    assert A["schema"] == B["schema"] == "p2_cmp_v1" and A["prereg_md5"] == B["prereg_md5"] == "2ea8ec13ffa3c32898cc24a3be605c64"
    assert A["addenda_md5"]["P2"] == B["addenda_md5"]["P2"] and A["addenda_md5"]["P2A"] == B["addenda_md5"]["P2A"], "addenda lock mismatch"
    miss = []
    def chk(tag, ok, desc):
        (None if ok else miss).append(tag + " " + desc) if not ok else None; print("  %s %s  %s" % (tag, "PASS" if ok else "MISS", desc))
    for n in ("step_hex", "gem8_hex", "step_cubic", "gem8_cubic"):
        a, b = A["per_substrate"][n], B["per_substrate"][n]
        for q in ("Q_T_a", "V_T", "V_L"): chk("C1", rel(a["C1_pin"][q], b["C1_pin"][q]) <= 1e-10, "%s %s %r vs %r" % (n, q, a["C1_pin"][q], b["C1_pin"][q]))
        chk("C1", a["C1_pin"]["pin_pass"] == b["C1_pin"]["pin_pass"] == True, "%s pin_pass" % n)
        chk("C2", a["C2_KK"]["pass"] == b["C2_KK"]["pass"] == True, "%s KK tie-in chat %.1e cc %.1e" % (n, a["C2_KK"]["alpha_tie_max_rel"], b["C2_KK"]["alpha_tie_max_rel"]))
        for ch in ("T", "L"): chk("C3", rel(a["C3_D0"][ch], b["C3_D0"][ch]) <= 1e-8, "%s D0_%s %+.6e vs %+.6e" % (n, ch, a["C3_D0"][ch], b["C3_D0"][ch]))
        for ch in ("T_analytic", "L_analytic"): chk("C4", rel(a["C4_a2_agg"][ch], b["C4_a2_agg"][ch]) <= 1e-6, "%s a2_agg %s %+.6e vs %+.6e (rel %.1e)" % (n, ch, a["C4_a2_agg"][ch], b["C4_a2_agg"][ch], rel(a["C4_a2_agg"][ch], b["C4_a2_agg"][ch])))
        chk("C5", rel(a["C5_a4_agg"]["T_even_basis"], b["C5_a4_agg"]["T_even_basis"]) <= 5e-2, "%s a4_agg %+.4e vs %+.4e" % (n, a["C5_a4_agg"]["T_even_basis"], b["C5_a4_agg"]["T_even_basis"]))
        chk("C5", a["C5_a4_agg"]["even_basis_rms"] <= 1e-7 and b["C5_a4_agg"]["even_basis_rms"] <= 1e-7, "%s even-basis rms %.1e / %.1e" % (n, a["C5_a4_agg"]["even_basis_rms"], b["C5_a4_agg"]["even_basis_rms"]))
        chk("C5", a["C5_a4_agg"]["smallk_confirmation_rel"] <= 1e-3 and b["C5_a4_agg"]["smallk_confirmation_rel"] <= 1e-3, "%s small-k confirmation %.1e / %.1e" % (n, a["C5_a4_agg"]["smallk_confirmation_rel"], b["C5_a4_agg"]["smallk_confirmation_rel"]))
        for k in ("F_AGG_DISP_pass", "F_AGG_L_pass", "F_CONV_pass", "structure_no_odd_or_log_term"): chk("C6", a["C6_controls"][k] == b["C6_controls"][k] == True, "%s %s" % (n, k))
        chk("C7", a["C7_arm"].split()[0] == b["C7_arm"].split()[0], "%s arm %s vs %s" % (n, a["C7_arm"], b["C7_arm"]))
    print("F-AGG-UNI (reported): chat spread %.2e  cc spread %.2e" % (A["F_AGG_UNI"]["a2_over_QT_spread_rel"], B["F_AGG_UNI"]["a2_over_QT_spread_rel"]))
    if miss: print("RESULT: S9 TRIGGERED — %d miss(es); counter-cross-check before any verdict." % len(miss)); return 2
    print("RESULT: C1–C7 ALL PASS — S9 NOT triggered; two-leg aggregate result stands; fold pending author authorization."); return 0
if __name__ == "__main__": sys.exit(main(sys.argv[1], sys.argv[2]))
<<<EMBED-END name=g_s2c1_p2_compare.py>>>

### EMBED — EXTRACTOR v2 (P-4.b) — `extract_embeds_v2.py` (md5 d4ac62219a95bea1e29d226e371ee39a, 2102 B, raw)

<<<EMBED-BEGIN name=extract_embeds_v2.py md5=d4ac62219a95bea1e29d226e371ee39a bytes=2102 enc=raw quarantine=0>>>
#!/usr/bin/env python3
# extract_embeds_v2.py — byte-exact extraction of every embed in a P-4 dispatch, with P-4.b base64 armor.
# Usage: python3 extract_embeds_v2.py <dispatch.md> [outdir] [--quarantine-dir DIR]
# Markers:  <<<EMBED-BEGIN name=NAME md5=HEX bytes=N enc=raw|b64 quarantine=0|1>>>  ...  <<<EMBED-END name=NAME>>>
# raw: payload is the file's UTF-8 text verbatim (file must end with a newline).  b64: payload is base64 (76-col lines).
# Every embed is verified against md5 + byte count; any mismatch aborts. quarantine=1 embeds are written to the
# quarantine dir (default ./QUARANTINE) and MUST NOT be opened before the CC checkpoint is hashed (procedural blindness).
import sys, os, re, base64, hashlib
BEGIN = "<<<EMBED-" + "BEGIN name=(\\S+) md5=([0-9a-f]{32}) bytes=(\\d+) enc=(raw|b64) quarantine=([01])>>>\n"
END = "<<<EMBED-" + "END name=%s>>>"
def main(path, outdir=".", qdir=None):
    qdir = qdir or os.path.join(outdir, "QUARANTINE"); os.makedirs(outdir, exist_ok=True); os.makedirs(qdir, exist_ok=True)
    text = open(path, "rb").read().decode("utf-8"); n = 0
    for m in re.finditer(BEGIN, text):
        name, md5, nbytes, enc, q = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5) == "1"
        j = text.find(END % name, m.end()); assert j > 0, "END marker missing: " + name
        seg = text[m.end():j]
        payload = seg.encode("utf-8") if enc == "raw" else base64.b64decode("".join(seg.split()))
        assert len(payload) == nbytes, "byte count mismatch %s: %d vs %d" % (name, len(payload), nbytes)
        assert hashlib.md5(payload).hexdigest() == md5, "md5 mismatch: " + name
        dest = os.path.join(qdir if q else outdir, name); open(dest, "wb").write(payload)
        print("OK  %s  %s  %d B  %s%s" % (md5, name, nbytes, enc, "  [QUARANTINE]" if q else "")); n += 1
    print("extracted %d embeds, all md5/byte-verified" % n)
if __name__ == "__main__":
    a = sys.argv[1:]; qd = None
    if "--quarantine-dir" in a: i = a.index("--quarantine-dir"); qd = a[i + 1]; a = a[:i] + a[i + 2:]
    main(a[0], a[1] if len(a) > 1 else ".", qd)
<<<EMBED-END name=extract_embeds_v2.py>>>

### EMBED — chat P2 comparison checkpoint (comparator input) — `s2c1_p2_chat_cmp_checkpoint.json` (md5 d9b8463851fb71285aa53506781bc75b, 4726 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_p2_chat_cmp_checkpoint.json md5=d9b8463851fb71285aa53506781bc75b bytes=4726 enc=b64 quarantine=1>>>
ewogIkZfQUdHX1VOSSI6IHsKICAiYTJfb3Zlcl9RVF9zcHJlYWRfcmVsIjogMC4wMTc2NzcyMDYx
MDg5MzUzOTMKIH0sCiAiYWRkZW5kYV9tZDUiOiB7CiAgIlAyIjogIjJmZWZmNDQyZGZkMDhhMzc5
NDQzZDg5M2I4Yzc3NjFiIiwKICAiUDJBIjogIjcxYjRjNzAxMGU0ODYwMWUwN2Y2NDU4YzcxMWRm
YjRhIgogfSwKICJlbGVjdGlvbl9FX1AyXzEiOiAiKGEpIiwKICJnYXRlIjogIkctUzJDMSIsCiAi
bGVnIjogImNoYXQiLAogInBlcl9zdWJzdHJhdGUiOiB7CiAgImdlbThfY3ViaWMiOiB7CiAgICJD
MV9waW4iOiB7CiAgICAiUV9UX2EiOiAwLjA3NTQ5NDMwMjA3MTIwNzc4LAogICAgIlZfTCI6IDE4
LjQ0NTMzMjc0MzAwMDMzLAogICAgIlZfVCI6IDkuODcyNDkyMDg2NjAxMDMzLAogICAgInBpbl9w
YXNzIjogdHJ1ZQogICB9LAogICAiQzJfS0siOiB7CiAgICAiYWxwaGFfdGllX21heF9yZWwiOiAy
LjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAicGFzcyI6IHRydWUKICAgfSwKICAgIkMzX0QwIjog
ewogICAgIkwiOiAtMC4wMTY2ODI5Nzc2ODc3NTg3NDcsCiAgICAiVCI6IC0wLjA0MzY3NzE0Mzky
Njk3OTc0NQogICB9LAogICAiQzRfYTJfYWdnIjogewogICAgIkNJX3F1YWRyYXR1cmVfcmVsIjog
MS4wMzY5NDgzMDQ5OTk4OTYyZS0xMywKICAgICJMX2FuYWx5dGljIjogLTAuMDUyMzYzMDIzNjg5
NzA3NzUsCiAgICAiVF9hbmFseXRpYyI6IC0wLjAzOTcxMzk3Njc5MTI4ODEzCiAgIH0sCiAgICJD
NV9hNF9hZ2ciOiB7CiAgICAiVF9hNiI6IC0wLjU0NjQ4MjUyNzU1ODM1NDksCiAgICAiVF9ldmVu
X2Jhc2lzIjogMC4xNDkyNTQyNTgxMDY4MTQxNCwKICAgICJldmVuX2Jhc2lzX3JtcyI6IDEuODQ2
NTI4MjYxNDY4NTMyNmUtMDgsCiAgICAic21hbGxrX2NvbmZpcm1hdGlvbl9yZWwiOiAwLjAwMDEx
NjEzMTY2OTgzNjU5NDQKICAgfSwKICAgIkM2X2NvbnRyb2xzIjogewogICAgIkZfQUdHX0RJU1Bf
cGFzcyI6IHRydWUsCiAgICAiRl9BR0dfTF9wYXNzIjogdHJ1ZSwKICAgICJGX0NPTlZfcGFzcyI6
IHRydWUsCiAgICAic3RydWN0dXJlX25vX29kZF9vcl9sb2dfdGVybSI6IHRydWUKICAgfSwKICAg
IkM3X2FybSI6ICJBMy1hZ2cgRElTUEVSU0lWRSAoZ3JhaW4tc2NhbGUga14yKSIsCiAgICJhMkxf
b3Zlcl9hMlQiOiAxLjMxODUwMzY1ODQxOTY4MiwKICAgImEyX292ZXJfUVQiOiAtMC41MjYwNTI2
Mzg0MzM5NDU2CiAgfSwKICAiZ2VtOF9oZXgiOiB7CiAgICJDMV9waW4iOiB7CiAgICAiUV9UX2Ei
OiAwLjA1MDAyMDU0ODQ3ODUzMjA5LAogICAgIlZfTCI6IDE5LjIyODkzODk1NDk1MzYzLAogICAg
IlZfVCI6IDEwLjI0ODk5NzY3NDU2OTYxMiwKICAgICJwaW5fcGFzcyI6IHRydWUKICAgfSwKICAg
IkMyX0tLIjogewogICAgImFscGhhX3RpZV9tYXhfcmVsIjogNi42NjEzMzgxNDc3NTA5MzllLTE2
LAogICAgInBhc3MiOiB0cnVlCiAgIH0sCiAgICJDM19EMCI6IHsKICAgICJMIjogLTAuMDEwOTUz
ODEzNjA5OTg2ODg1LAogICAgIlQiOiAtMC4wMjg5MTc4MDc2MDMwNzE3MzUKICAgfSwKICAgIkM0
X2EyX2FnZyI6IHsKICAgICJDSV9xdWFkcmF0dXJlX3JlbCI6IDUuOTYxODk3NjQyMjM3MDllLTE0
LAogICAgIkxfYW5hbHl0aWMiOiAtMC4wMzQ0MDY4MjczNTE4ODczNSwKICAgICJUX2FuYWx5dGlj
IjogLTAuMDI1OTMzNjkzNTg0Mjk0MjEKICAgfSwKICAgIkM1X2E0X2FnZyI6IHsKICAgICJUX2E2
IjogLTAuMzYxNTMwNDA3OTA1MDQyNzYsCiAgICAiVF9ldmVuX2Jhc2lzIjogMC4wOTg5NjQxOTUx
MjQ0NDgwNSwKICAgICJldmVuX2Jhc2lzX3JtcyI6IDEuMjEwODAyMTQ3ODQ5NzY0OWUtMDgsCiAg
ICAic21hbGxrX2NvbmZpcm1hdGlvbl9yZWwiOiAwLjAwMDExNzg3MzMzMTcyMzUyODEKICAgfSwK
ICAgIkM2X2NvbnRyb2xzIjogewogICAgIkZfQUdHX0RJU1BfcGFzcyI6IHRydWUsCiAgICAiRl9B
R0dfTF9wYXNzIjogdHJ1ZSwKICAgICJGX0NPTlZfcGFzcyI6IHRydWUsCiAgICAic3RydWN0dXJl
X25vX29kZF9vcl9sb2dfdGVybSI6IHRydWUKICAgfSwKICAgIkM3X2FybSI6ICJBMy1hZ2cgRElT
UEVSU0lWRSAoZ3JhaW4tc2NhbGUga14yKSIsCiAgICJhMkxfb3Zlcl9hMlQiOiAxLjMyNjcyMjk4
NDUyNDA2MjUsCiAgICJhMl9vdmVyX1FUIjogLTAuNTE4NDYwODAwMDczNDgzNQogIH0sCiAgInN0
ZXBfY3ViaWMiOiB7CiAgICJDMV9waW4iOiB7CiAgICAiUV9UX2EiOiAwLjA1NDA3NzYyODI0NjUx
ODY0LAogICAgIlZfTCI6IDE0LjU0ODMzMTg2MzEzODEyNCwKICAgICJWX1QiOiA4LjExNTc5NDQ3
NzQzNzE5LAogICAgInBpbl9wYXNzIjogdHJ1ZQogICB9LAogICAiQzJfS0siOiB7CiAgICAiYWxw
aGFfdGllX21heF9yZWwiOiAzLjMzMDY2OTA3Mzg3NTQ2OTZlLTE2LAogICAgInBhc3MiOiB0cnVl
CiAgIH0sCiAgICJDM19EMCI6IHsKICAgICJMIjogLTAuMDEzMDc1ODUxODIwNzExNjcsCiAgICAi
VCI6IC0wLjAzMTUxMzQyMjQzNDMzNjIzCiAgIH0sCiAgICJDNF9hMl9hZ2ciOiB7CiAgICAiQ0lf
cXVhZHJhdHVyZV9yZWwiOiAyLjAyNzI2NzI0Mjk2NTUzNThlLTEzLAogICAgIkxfYW5hbHl0aWMi
OiAtMC4wMzc2NzA1MjY4MTMxNjY2MSwKICAgICJUX2FuYWx5dGljIjogLTAuMDI4NTM3NDcxMTA3
OTQ0NDIzCiAgIH0sCiAgICJDNV9hNF9hZ2ciOiB7CiAgICAiVF9hNiI6IC0wLjM5MDQ4MzkzNTI3
NTExNDksCiAgICAiVF9ldmVuX2Jhc2lzIjogMC4xMDY4MTcyNTkyODI3MDA3NSwKICAgICJldmVu
X2Jhc2lzX3JtcyI6IDEuMzE3MDI2NDk2MzI4MjAxZS0wOCwKICAgICJzbWFsbGtfY29uZmlybWF0
aW9uX3JlbCI6IDAuMDAwMTE1MzE0MjQzNDk0NTM1MzQKICAgfSwKICAgIkM2X2NvbnRyb2xzIjog
ewogICAgIkZfQUdHX0RJU1BfcGFzcyI6IHRydWUsCiAgICAiRl9BR0dfTF9wYXNzIjogdHJ1ZSwK
ICAgICJGX0NPTlZfcGFzcyI6IHRydWUsCiAgICAic3RydWN0dXJlX25vX29kZF9vcl9sb2dfdGVy
bSI6IHRydWUKICAgfSwKICAgIkM3X2FybSI6ICJBMy1hZ2cgRElTUEVSU0lWRSAoZ3JhaW4tc2Nh
bGUga14yKSIsCiAgICJhMkxfb3Zlcl9hMlQiOiAxLjMyMDAzNzMxNzYyNjIxNjYsCiAgICJhMl9v
dmVyX1FUIjogLTAuNTI3NzEzMDY3OTIyNTMKICB9LAogICJzdGVwX2hleCI6IHsKICAgIkMxX3Bp
biI6IHsKICAgICJRX1RfYSI6IDAuMDM1MTkwNzM4ODY2MDcwMDMsCiAgICAiVl9MIjogMTUuMjMy
NDg3MjEyMDk1OTUsCiAgICAiVl9UIjogOC41NDc3Nzk0Mzg3MzkyNCwKICAgICJwaW5fcGFzcyI6
IHRydWUKICAgfSwKICAgIkMyX0tLIjogewogICAgImFscGhhX3RpZV9tYXhfcmVsIjogNS41NTEx
MTUxMjMxMjU3ODNlLTE2LAogICAgInBhc3MiOiB0cnVlCiAgIH0sCiAgICJDM19EMCI6IHsKICAg
ICJMIjogLTAuMDA4NjIwNzExMjc5ODA5ODY0LAogICAgIlQiOiAtMC4wMjA1MjgyNDQ1OTUzMjgz
NQogICB9LAogICAiQzRfYTJfYWdnIjogewogICAgIkNJX3F1YWRyYXR1cmVfcmVsIjogNS44ODQx
ODIwMzA1MTMzM2UtMTUsCiAgICAiTF9hbmFseXRpYyI6IC0wLjAyNDMyMjYxNDcwOTI0NDA1NSwK
ICAgICJUX2FuYWx5dGljIjogLTAuMDE4MzQ3NjYzMTYzOTQ3MDQ3CiAgIH0sCiAgICJDNV9hNF9h
Z2ciOiB7CiAgICAiVF9hNiI6IC0wLjI1MzYyOTc4NzM4OTI4MywKICAgICJUX2V2ZW5fYmFzaXMi
OiAwLjA2OTU0MDczNzY3MDMzNDEsCiAgICAiZXZlbl9iYXNpc19ybXMiOiA4LjQ4NzMzNTQ0MzEx
NzA1ZS0wOSwKICAgICJzbWFsbGtfY29uZmlybWF0aW9uX3JlbCI6IDAuMDAwMTE2NjM5MTc4NTEz
NDU1NzMKICAgfSwKICAgIkM2X2NvbnRyb2xzIjogewogICAgIkZfQUdHX0RJU1BfcGFzcyI6IHRy
dWUsCiAgICAiRl9BR0dfTF9wYXNzIjogdHJ1ZSwKICAgICJGX0NPTlZfcGFzcyI6IHRydWUsCiAg
ICAic3RydWN0dXJlX25vX29kZF9vcl9sb2dfdGVybSI6IHRydWUKICAgfSwKICAgIkM3X2FybSI6
ICJBMy1hZ2cgRElTUEVSU0lWRSAoZ3JhaW4tc2NhbGUga14yKSIsCiAgICJhMkxfb3Zlcl9hMlQi
OiAxLjMyNTY1MTkwOTU1OTY3MiwKICAgImEyX292ZXJfUVQiOiAtMC41MjEzNzc2MDU0NDgyNzI2
CiAgfQogfSwKICJwaGFzZSI6ICIzIC8gUDIgYWdncmVnYXRlIiwKICJwcmVyZWdfbWQ1IjogIjJl
YThlYzEzZmZhM2MzMjg5OGNjMjRhM2JlNjA1YzY0IiwKICJzY2hlbWEiOiAicDJfY21wX3YxIiwK
ICJzaGFyZWRfbGF5ZXJfZmxhZ2dlZCI6ICJYaS9QaGlfVE0ga2VybmVscyBhbmQgdGhlIHBpbm5l
ZCB0ZW5zb3JzIGFyZSB0aGUgYmFua2VkIEctUE9MWTEgbGF5ZXIgKGNoYXQgbGVnIHVzZWQgdGhl
IHJlY292ZXJlZCBDQy1hdXRob3JlZCBHLVBPTFkxIGluc3RydW1lbnQgZm9yIHRoZW0pOyB0aGUg
aW5kZXBlbmRlbnQgY29udGVudCBvZiB0aGlzIGdhdGUgaXMgdGhlIHJlYWwtcGFydCAoUFYpIGNv
bXB1dGF0aW9uLCB0aGUgYW5hbHl0aWMgRDIsIGFuZCB0aGUgZml0cyIsCiAic291cmNlX21kNSI6
IHsKICAiUDJBX2V2YWx1YXRpb24iOiAiNTZiMTdkOTM1NmE2MGM0ZmIyYzdkNjlhZDE5YTYxOTgi
LAogICJwaGFzZTBfcGluIjogIjAzMjhiNTcwYWY0NmE4Nzg5NzA2NTNhZDg3NzVmNmQ5IiwKICAi
cGhhc2UxX2xhZGRlcnMiOiAiNmRhNjJmY2E2NDRkNWVhNmIxZDdhYmU3MzI5YjVlMmMiLAogICJw
aGFzZTJfZml0cyI6ICIwZThjYzA1ZTQ4NjhiOGRiMDg2NTY0ZTI5N2NhYjZkNSIsCiAgInN0cnVj
dHVyZV9kaWFnIjogIjYwYWRkMDA5YzI4MmI5ZDYwMzAyMWJhMGFkYmZhMWUyIgogfQp9Cg==
<<<EMBED-END name=s2c1_p2_chat_cmp_checkpoint.json>>>

### EMBED — chat P2 instrument — `g_s2c1_p2_aggregate.py` (md5 05a323cf73851a56f54539f37c00cb1f, 13391 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=g_s2c1_p2_aggregate.py md5=05a323cf73851a56f54539f37c00cb1f bytes=13391 enc=b64 quarantine=1>>>
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX3MyYzFfcDJfYWdncmVnYXRlLnB5IOKAlCBHYXRl
IEctUzJDMSwgUEhBU0UgMyAvIFBST0JFIFAyIChhZ2dyZWdhdGUpLCBjaGF0IGxlZy4KTG9jazog
cHJlcmVnIDJlYThlYzEzOyBUMSA4Y2Q4OWI5YTsgcmVjb3JkIGYyZjRkNTAwOyBBLTEgOGJmNTFi
ZDA7IEEtMiBhOWJkYTA4NjsgQURERU5EVU0gUDIgMmZlZmY0NDJkZmQwOGEzNzk0NDNkODkzYjhj
Nzc2MWIKKGxvY2tlZCBiZWZvcmUgdGhpcyBmaWxlIHdhcyB3cml0dGVuKS4gRS1QMi0xIChhKTog
Y2hhbm5lbCA9IHBvbGFyaXphdGlvbi1hdmVyYWdlZCB0cmFuc3ZlcnNlIHNoZWFyIGNvbmUuCk1h
Y2hpbmVyeTogdGhlIHJlY292ZXJlZCBHLVBPTFkxIGluc3RydW1lbnQgcG9seTFfZnVsbHByZWNf
Y2NsZWcucHkgKGJyYW5jaCBndmJrb2YgQCAyMzFiNTU1YSwgbWFuaWZlc3QtdmVyaWZpZWQpIGlt
cG9ydGVkCmFzIGEgbW9kdWxlIGZvciDOniAoU08oMykgY292YXJpYW5jZSksIM6mX1RNKM68KSBr
ZXJuZWxzLCB0aGUgcGlubmVkIHRlbnNvcnMsIGFuZCBhbHBoYV9maW5pdGUgKHRoZSBJbS1wYXJ0
IHRpZS1pbikuCk5ldyBzdGVwOiB0aGUgcmVhbC1wYXJ0IHBhcnRuZXIgSl9NKGspID0gUFbiiKsg
cV40IEZfTShxLGspLyhrX01eMiAtIHFeMikgZHEgYnkgQ2F1Y2h5LXdlaWdodCBxdWFkcmF0dXJl
ICsgcmVndWxhciB0YWlsLgpBbGwgcXVhbnRpdGllcyBpbiBzdWJzdHJhdGUgdW5pdHMgd2l0aCBh
X2cgPSAxLiBUMSBzZWxmLXNjYW4gYXQgc3RhcnQuIFBlci1waGFzZSBKU09OIGNoZWNrcG9pbnRz
IChFOCkuCiIiIgppbXBvcnQgc3lzLCBvcywganNvbiwgbWF0aCwgaGFzaGxpYiwgdGltZQppbXBv
cnQgbnVtcHkgYXMgbnAKZnJvbSBzY2lweS5pbnRlZ3JhdGUgaW1wb3J0IHF1YWQKc3lzLnBhdGgu
aW5zZXJ0KDAsICIvaG9tZS9jbGF1ZGUvczJjL2dwb2x5MSIpCmltcG9ydCBwb2x5MV9mdWxscHJl
Y19jY2xlZyBhcyBQClQwID0gdGltZS50aW1lKCkKZGVmIGxvZyhzKTogcHJpbnQoIlslNi4xZnNd
ICVzIiAlICh0aW1lLnRpbWUoKSAtIFQwLCBzKSwgZmx1c2g9VHJ1ZSkKZGVmIG1kNWIoYik6IHJl
dHVybiBoYXNobGliLm1kNShiKS5oZXhkaWdlc3QoKQpkZWYgY2twdChuYW1lLCBvYmopOgogICAg
YiA9IChqc29uLmR1bXBzKG9iaiwgaW5kZW50PTEsIHNvcnRfa2V5cz1UcnVlLCBkZWZhdWx0PXN0
cikgKyAiXG4iKS5lbmNvZGUoKTsgb3BlbihuYW1lLCAid2IiKS53cml0ZShiKQogICAgbG9nKCJj
aGVja3BvaW50ICVzIG1kNSAlcyAoJWQgQikiICUgKG5hbWUsIG1kNWIoYiksIGxlbihiKSkpOyBy
ZXR1cm4gbWQ1YihiKQpwYXRzID0gW2wucnN0cmlwKCJcbiIpIGZvciBsIGluIG9wZW4oIi9ob21l
L2NsYXVkZS9zMmMvdDFfZm9yYmlkZGVuX0dfUzJfT05fQ09ORS50eHQiLCBlbmNvZGluZz0idXRm
LTgiKSBpZiBsLnN0cmlwKCldCnNyYyA9IG9wZW4ob3MucGF0aC5hYnNwYXRoKF9fZmlsZV9fKSwg
ZW5jb2Rpbmc9InV0Zi04IikucmVhZCgpLmxvd2VyKCkKYXNzZXJ0IG5vdCBbcCBmb3IgcCBpbiBw
YXRzIGlmIHAubG93ZXIoKSBpbiBzcmNdLCAiVDEgc2VsZi1zY2FuIGhpdCIKQURERU5EVU1fUDIg
PSAiMmZlZmY0NDJkZmQwOGEzNzk0NDNkODkzYjhjNzc2MWIiCmFzc2VydCBtZDViKG9wZW4oIi9o
b21lL2NsYXVkZS9zMmMvbG9jay9HX1MyX09OX0NPTkVfTE9DS19SRUNPUkRfQURERU5EVU1fUDIu
bWQiLCAicmIiKS5yZWFkKCkpID09IEFEREVORFVNX1AyLCAiUDIgYWRkZW5kdW0gbWQ1IG1pc21h
dGNoIOKAlCBoYWx0IgpUQVVfQUdHID0gMWUtNgpMQURERVIgPSBbMC4zIC8gMioqaiBmb3IgaiBp
biByYW5nZSg5KV0gKyBbMC4wMDUsIDAuMDEsIDAuMDE1LCAwLjAyLCAwLjAzXQpMQURERVIgPSBz
b3J0ZWQoc2V0KExBRERFUiksIHJldmVyc2U9VHJ1ZSkKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIHN1YnN0cmF0ZXMg
KGlkZW50aWNhbCBjb25zdHJ1Y3Rpb24gdG8gdGhlIHJlY292ZXJlZCBtYWluKCkpCnJhdyA9IG9w
ZW4oUC5JTlBVVCwgInJiIikucmVhZCgpOyBhc3NlcnQgbWQ1YihyYXcpID09IFAuSU5QVVRfTUQ1
LCAiaW5wdXQgbWQ1IG1pc21hdGNoIOKAlCBoYWx0Igp2ID0ganNvbi5sb2FkcyhyYXcpWyJ2cmgi
XQpjZmcgPSB7fQpjcyA9IHZbImhleDpzdGVwIl1bIkNfb3Zlcl9yaG8iXTsgICBjZmdbInN0ZXBf
aGV4Il0gICA9ICgiaGV4IiwgICBbY3Nba10gZm9yIGsgaW4gKCJDMTEiLCAiQzEyIiwgIkMxMyIs
ICJDMzMiLCAiQzQ0IiwgIkM2NiIpXSkKY3MgPSB2WyJoZXg6Z2VtOCJdWyJDX292ZXJfcmhvIl07
ICAgY2ZnWyJnZW04X2hleCJdICAgPSAoImhleCIsICAgW2NzW2tdIGZvciBrIGluICgiQzExIiwg
IkMxMiIsICJDMTMiLCAiQzMzIiwgIkM0NCIsICJDNjYiKV0pCmNzID0gdlsiY3ViaWM6c3RlcCJd
WyJDX292ZXJfcmhvIl07IGNmZ1sic3RlcF9jdWJpYyJdID0gKCJjdWJpYyIsIFtjc1siQzExIl0s
IGNzWyJDMTIiXSwgY3NbIkM0NCJdXSkKY3MgPSB2WyJjdWJpYzpnZW04Il1bIkNfb3Zlcl9yaG8i
XTsgY2ZnWyJnZW04X2N1YmljIl0gPSAoImN1YmljIiwgW2NzWyJDMTEiXSwgY3NbIkMxMiJdLCBj
c1siQzQ0Il1dKQpiYW5rZWQgPSBqc29uLmxvYWQob3BlbigiL2hvbWUvY2xhdWRlL3MyYy9ncG9s
eTEvcG9seTFfcGhhc2UxZnVsbF9jYy5qc29uIikpWyJwaGFzZTFiIl0KCiMgLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGtl
cm5lbHMKZGVmIGJ1aWxkKG5hbWUsIG5iPTEwLCBuYT0xMik6CiAgICBzeW0sIGNjID0gY2ZnW25h
bWVdCiAgICBNNiA9IFAudm9pZ3RfaGV4KCpjYykgaWYgc3ltID09ICJoZXgiIGVsc2UgUC52b2ln
dF9jdWJpYygqY2MpCiAgICBDNCA9IFAudGVuc29yX2Zyb21fdm9pZ3QoTTYpOyBLVmcsIEdWZywg
S1JnLCBHUmcgPSBQLmdlbl9jaGFpbihNNikKICAgIFhpLCBfID0gUC54aV9xdWFkcmF0dXJlKEM0
LCBuYj1uYiwgbmE9bmEpCiAgICBsYW0sIG11ID0gS1ZnIC0gMi4wICogR1ZnIC8gMy4wLCBHVmcK
ICAgIHJldHVybiBYaSwgbWF0aC5zcXJ0KG11KSwgbWF0aC5zcXJ0KGxhbSArIDIuMCAqIG11KQpk
ZWYgcGhpX3RhYmxlKFhpLCBpbmMsIG4pOgogICAgeGcsIHdnID0gbnAucG9seW5vbWlhbC5sZWdl
bmRyZS5sZWdnYXVzcyhuKQogICAgcmV0dXJuIHtNOiAoeGcsIHdnLCBucC5hcnJheShbUC5waGlf
cG0oWGksIGluYywgTSwgeCkgZm9yIHggaW4geGddKSkgZm9yIE0gaW4gKCJUIiwgIkwiKX0KZGVm
IEZfb2YodGFiLCBNLCBxLCBrKToKICAgIHhnLCB3ZywgcGggPSB0YWJbTV07IHJldHVybiBmbG9h
dChucC5zdW0od2cgKiBwaCAvICgxLjAgKyBrICogayArIHEgKiBxIC0gMi4wICogayAqIHEgKiB4
ZykgKiogMikpCmRlZiBKX00odGFiLCBNLCBrLCBrTSwgUW1heD01MC4wLCBlcHNyZWw9MWUtMTAp
OgogICAgIiIiUFbiiKtfMF7iiJ4gcV40IEZfTShxLGspLyhrTV4yIC0gcV4yKSBkcSA9IC1QVuKI
qyBbcV40IEYvKGtNK3EpXS8ocSAtIGtNKSBkcSAgKENhdWNoeSB3ZWlnaHQpICsgcmVndWxhciB0
YWlsLiIiIgogICAgZyA9IGxhbWJkYSBxOiAtcSAqKiA0ICogRl9vZih0YWIsIE0sIHEsIGspIC8g
KGtNICsgcSkKICAgIHB2LCBfID0gcXVhZChnLCAwLjAsIFFtYXgsIHdlaWdodD0iY2F1Y2h5Iiwg
d3Zhcj1rTSwgZXBzYWJzPTAuMCwgZXBzcmVsPWVwc3JlbCwgbGltaXQ9NDAwKQogICAgdGFpbCwg
XyA9IHF1YWQobGFtYmRhIHE6IHEgKiogNCAqIEZfb2YodGFiLCBNLCBxLCBrKSAvIChrTSAqIGtN
IC0gcSAqIHEpLCBRbWF4LCBucC5pbmYsIGVwc2Ficz0wLjAsIGVwc3JlbD1lcHNyZWwsIGxpbWl0
PTQwMCkKICAgIHJldHVybiBwdiArIHRhaWwKZGVmIERfb2YodGFiLCBWaW5jLCBWVCwgVkwsIGss
ICoqa3cpOgogICAgb3V0ID0gMC4wCiAgICBmb3IgTSwgVk0gaW4gKCgiVCIsIFZUKSwgKCJMIiwg
VkwpKToKICAgICAgICBvdXQgKz0gKDEuMCAvIChWaW5jICoqIDIgKiBWTSAqKiAyKSkgKiBKX00o
dGFiLCBNLCBrLCBrICogVmluYyAvIFZNLCAqKmt3KQogICAgcmV0dXJuIG91dCAvIG1hdGgucGkK
ZGVmIEQwX2Nsb3NlZCh0YWIsIFZpbmMsIFZULCBWTCk6CiAgICBvdXQgPSAwLjAKICAgIGZvciBN
LCBWTSBpbiAoKCJUIiwgVlQpLCAoIkwiLCBWTCkpOgogICAgICAgIHhnLCB3ZywgcGggPSB0YWJb
TV07IG91dCArPSAoMS4wIC8gKFZpbmMgKiogMiAqIFZNICoqIDIpKSAqIGZsb2F0KG5wLnN1bSh3
ZyAqIHBoKSkKICAgIHJldHVybiAtMC4yNSAqIG91dApkZWYgRDJfYW5hbHl0aWModGFiLCBWaW5j
LCBWVCwgVkwpOgogICAgIiIia14yIGNvZWZmaWNpZW50IG9mIEQgZnJvbSAoaSkg4oiCRi/iiIIo
a14yKSBhdCBmaXhlZCBwb2xlIGFuZCAoaWkpIHRoZSBwb2xlIHNoaWZ0IGtfTV4yID0ga14yIHJf
TV4yOgogICAgICAgRDIgPSAoMS/PgCkgzqNfTSBOX00gWyAt4oirIHFeMiBGMihxKSBkcSAtIHJf
TV4yIOKIqyBGMChxKSBkcSBdLCAgRjIgPSAtMiBJMC9BXjMgKyAxMiBxXjIgSTIvQV40LCBBID0g
MStxXjIuIiIiCiAgICBvdXQgPSAwLjAKICAgIGZvciBNLCBWTSBpbiAoKCJUIiwgVlQpLCAoIkwi
LCBWTCkpOgogICAgICAgIHhnLCB3ZywgcGggPSB0YWJbTV07IEkwID0gZmxvYXQobnAuc3VtKHdn
ICogcGgpKTsgSTIgPSBmbG9hdChucC5zdW0od2cgKiBwaCAqIHhnICoqIDIpKTsgck0yID0gKFZp
bmMgLyBWTSkgKiogMgogICAgICAgIHQxLCBfID0gcXVhZChsYW1iZGEgcTogLXEgKiBxICogKC0y
LjAgKiBJMCAvICgxICsgcSAqIHEpICoqIDMgKyAxMi4wICogcSAqIHEgKiBJMiAvICgxICsgcSAq
IHEpICoqIDQpLCAwLCBucC5pbmYsIGVwc3JlbD0xZS0xMikKICAgICAgICB0MiwgXyA9IHF1YWQo
bGFtYmRhIHE6IC1yTTIgKiBJMCAvICgxICsgcSAqIHEpICoqIDIsIDAsIG5wLmluZiwgZXBzcmVs
PTFlLTEyKQogICAgICAgIG91dCArPSAoMS4wIC8gKFZpbmMgKiogMiAqIFZNICoqIDIpKSAqICh0
MSArIHQyKQogICAgcmV0dXJuIG91dCAvIG1hdGgucGkKZGVmIGFscGhhX3RpZSh0YWIsIFZULCBW
TCwgayk6CiAgICBvdXQgPSAwLjAKICAgIGZvciBNLCBWTSBpbiAoKCJUIiwgVlQpLCAoIkwiLCBW
TCkpOgogICAgICAgIGtNID0gayAqIFZUIC8gVk07IG91dCArPSBrICoga00gKiogMyAvICgyLjAg
KiBWVCAqIFZUICogVk0gKiBWTSkgKiBGX29mKHRhYiwgTSwga00sIGspCiAgICByZXR1cm4gb3V0
CmRlZiBmaXRzKGtzLCBkbCk6CiAgICBrcyA9IG5wLmFycmF5KGtzKTsgZGwgPSBucC5hcnJheShk
bCk7IHJlcyA9IHt9CiAgICBmb3IgbGFiZWwsIGNvbHMgaW4gKCgiYmFzaXMyIiwgKDIsIDQpKSwg
KCJiYXNpczMiLCAoMiwgMywgNCkpKToKICAgICAgICBkZWYgZml0KHNlbCk6CiAgICAgICAgICAg
IFggPSBucC5zdGFjayhba3Nbc2VsXSAqKiBwIGZvciBwIGluIGNvbHNdLCBheGlzPTEpOyBjLCAq
XyA9IG5wLmxpbmFsZy5sc3RzcShYLCBkbFtzZWxdLCByY29uZD1Ob25lKQogICAgICAgICAgICBy
ID0gZGxbc2VsXSAtIFggQCBjOyByZXR1cm4gYywgZmxvYXQobnAuc3FydChucC5tZWFuKHIgKiBy
KSkpCiAgICAgICAgYywgcm1zID0gZml0KGtzID4gMCkKICAgICAgICBjaXMgPSBbZml0KGtzIDw9
IGUpWzBdIGZvciBlIGluICgwLjE1LCAwLjA3NSldCiAgICAgICAgcmVzW2xhYmVsXSA9IHsiY29l
ZiI6IHsiayVkIiAlIHA6IGZsb2F0KGNbaV0pIGZvciBpLCBwIGluIGVudW1lcmF0ZShjb2xzKX0s
ICJybXMiOiBybXMsCiAgICAgICAgICAgICAgICAgICAgICAiY2kiOiB7ImslZCIgJSBwOiBmbG9h
dChtYXgoYWJzKGNjW2ldIC0gY1tpXSkgZm9yIGNjIGluIGNpcykpIGZvciBpLCBwIGluIGVudW1l
cmF0ZShjb2xzKX19CiAgICByZXR1cm4gcmVzCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBQaGFzZSAwOiBwaW4gcmVw
cm9kdWN0aW9uIChGLUFHRy1QSU4pCmxvZygiUDIgcGhhc2UgMDogcGluIHJlcHJvZHVjdGlvbiBv
ZiB0aGUgUV9UIHF1YXJ0ZXQiKQpwaW4gPSB7fQpLRVIgPSB7fQpmb3IgbmFtZSBpbiBjZmc6CiAg
ICBYaSwgVlQsIFZMID0gYnVpbGQobmFtZSk7IHRhYiA9IHBoaV90YWJsZShYaSwgIlQiLCAyNCkg
ICAgICMgaW50X3BoaSB1c2VzIG49MjQgR0wgaW4gdGhlIHJlY292ZXJlZCBpbnN0cnVtZW50CiAg
ICBpVFQgPSBmbG9hdChucC5zdW0odGFiWyJUIl1bMV0gKiB0YWJbIlQiXVsyXSkpOyBpVEwgPSBm
bG9hdChucC5zdW0odGFiWyJMIl1bMV0gKiB0YWJbIkwiXVsyXSkpCiAgICBRVFQgPSBpVFQgLyAo
Mi4wICogVlQgKiogNCk7IFFUTCA9IFZUICogaVRMIC8gKDIuMCAqIFZMICoqIDUpOyBRVCA9IFFU
VCArIFFUTAogICAgYiA9IGJhbmtlZFtuYW1lXTsgcmVsID0gYWJzKFFUIC8gYlsiUV9UX2EiXSAt
IDEuMCkKICAgIHBpbltuYW1lXSA9IHsiUV9UX2EiOiBRVCwgImJhbmtlZCI6IGJbIlFfVF9hIl0s
ICJyZWwiOiByZWwsICJkaWdpdHM3X21hdGNoIjogKCIlLjZlIiAlIFFUKSA9PSAoIiUuNmUiICUg
YlsiUV9UX2EiXSksICJWVDAiOiBWVCwgIlZMMCI6IFZMLCAiVlQwX2JhbmtlZCI6IGJbIlZUMCJd
LCAiVkwwX2JhbmtlZCI6IGJbIlZMMCJdfQogICAgbG9nKCIgICUtMTFzIFFfVF9hICUuNmUgYmFu
a2VkICUuNmUgcmVsICUuMWUgOyBWX1QgJS42ZiAoYmFua2VkICUuNmYpIFZfTCAlLjZmIiAlIChu
YW1lLCBRVCwgYlsiUV9UX2EiXSwgcmVsLCBWVCwgYlsiVlQwIl0sIFZMKSkKICAgIEtFUltuYW1l
XSA9IChYaSwgVlQsIFZMKQpwaW5fb2sgPSBhbGwocFsiZGlnaXRzN19tYXRjaCJdIGFuZCBwWyJy
ZWwiXSA8IDFlLTEwIGZvciBwIGluIHBpbi52YWx1ZXMoKSkKY2twdCgiczJjMV9wMl9waGFzZTBf
cGluLmpzb24iLCB7InBpbiI6IHBpbiwgIkZfQUdHX1BJTl9wYXNzIjogYm9vbChwaW5fb2spLCAi
YWRkZW5kdW1fUDIiOiBBRERFTkRVTV9QMn0pCmlmIG5vdCBwaW5fb2s6IGxvZygiRi1BR0ctUElO
IEZBSUxFRCDigJQgQTUtYWdnIEhBTFQiKTsgc3lzLmV4aXQoMikKCiMgLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIFBoYXNl
IDE6IEQoaykgbGFkZGVycywgVCBjaGFubmVsIChFLVAyLTEgKGEpKSArIEwgY29udHJvbApsb2co
IlAyIHBoYXNlIDE6IGRpc3BlcnNpb24gbGFkZGVycyAoVCBjaGFubmVsIG9mIHJlY29yZDsgTCBj
aGFubmVsIGNvbnRyb2wpIikKcGgxID0ge30KZm9yIG5hbWUgaW4gY2ZnOgogICAgWGksIFZULCBW
TCA9IEtFUltuYW1lXTsgcmVjID0geyJWVCI6IFZULCAiVkwiOiBWTCwgImNoYW5uZWxzIjoge319
CiAgICBmb3IgaW5jLCBWaW5jIGluICgoIlQiLCBWVCksICgiTCIsIFZMKSk6CiAgICAgICAgdGFi
ID0gcGhpX3RhYmxlKFhpLCBpbmMsIDY0KQogICAgICAgIEQwID0gRDBfY2xvc2VkKHRhYiwgVmlu
YywgVlQsIFZMKTsgRGsgPSBbRF9vZih0YWIsIFZpbmMsIFZULCBWTCwgaykgZm9yIGsgaW4gTEFE
REVSXQogICAgICAgIER0aW55ID0gRF9vZih0YWIsIFZpbmMsIFZULCBWTCwgMWUtNCkKICAgICAg
ICByZWNbImNoYW5uZWxzIl1baW5jXSA9IHsiRDBfY2xvc2VkIjogRDAsICJEX2F0XzFlLTQiOiBE
dGlueSwgIkQwX2NvbnNpc3RlbmN5X3JlbCI6IGFicyhEdGlueSAvIEQwIC0gMS4wKSwgImxhZGRl
cl9rIjogTEFEREVSLCAiRCI6IERrLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJE
ZWx0YSI6IFtkIC0gRDAgZm9yIGQgaW4gRGtdLCAiRDJfYW5hbHl0aWMiOiBEMl9hbmFseXRpYyh0
YWIsIFZpbmMsIFZULCBWTCl9CiAgICAgICAgaWYgaW5jID09ICJUIjoKICAgICAgICAgICAgZ3Jp
ZCA9IGJhbmtlZFtuYW1lXVsia1RhX2dyaWQiXTsgYWwgPSBbYWxwaGFfdGllKHRhYiwgVlQsIFZM
LCBrKSBmb3IgayBpbiBncmlkXQogICAgICAgICAgICB0YWIyNCA9IHBoaV90YWJsZShYaSwgIlQi
LCAyNCk7IGFsMjQgPSBbYWxwaGFfdGllKHRhYjI0LCBWVCwgVkwsIGspIGZvciBrIGluIGdyaWRd
CiAgICAgICAgICAgIHJlY1siYWxwaGFfdGllX2luIl0gPSB7ImdyaWQiOiBncmlkLCAiYWxwaGFf
aGVyZV9uNjQiOiBhbCwgImFscGhhX2hlcmVfbjI0IjogYWwyNCwgImFscGhhX2JhbmtlZCI6IGJh
bmtlZFtuYW1lXVsiYWxwaGFfVF9hIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgIm1heF9yZWxfbjI0IjogbWF4KGFicyhhIC8gYiAtIDEuMCkgZm9yIGEsIGIgaW4gemlwKGFs
MjQsIGJhbmtlZFtuYW1lXVsiYWxwaGFfVF9hIl0pKSwKICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAibWF4X3JlbF9uNjQiOiBtYXgoYWJzKGEgLyBiIC0gMS4wKSBmb3IgYSwgYiBp
biB6aXAoYWwsIGJhbmtlZFtuYW1lXVsiYWxwaGFfVF9hIl0pKX0KICAgICAgICBsb2coIiAgJS0x
MXMgJXM6IEQwICUrLjZlIChrPTFlLTQ6ICUrLjZlKSA7IERlbHRhKDAuMykgJSsuNGUgRGVsdGEo
MC4wMzc1KSAlKy40ZSA7IEQyX2FuYWx5dGljICUrLjZlIiAlIChuYW1lLCBpbmMsIEQwLCBEdGlu
eSwgcmVjWyJjaGFubmVscyJdW2luY11bIkRlbHRhIl1bMF0sIHJlY1siY2hhbm5lbHMiXVtpbmNd
WyJEZWx0YSJdWzNdLCByZWNbImNoYW5uZWxzIl1baW5jXVsiRDJfYW5hbHl0aWMiXSkpCiAgICBs
b2coIiAgJS0xMXMgYWxwaGEgdGllLWluIHZzIGJhbmtlZDogbWF4IHJlbCAobj0yNCBub2RlcyBh
cyBiYW5rZWQpICUuMWUgOyAobj02NCkgJS4xZSIgJSAobmFtZSwgcmVjWyJhbHBoYV90aWVfaW4i
XVsibWF4X3JlbF9uMjQiXSwgcmVjWyJhbHBoYV90aWVfaW4iXVsibWF4X3JlbF9uNjQiXSkpCiAg
ICBwaDFbbmFtZV0gPSByZWMKY2twdCgiczJjMV9wMl9waGFzZTFfbGFkZGVycy5qc29uIiwgcGgx
KQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0gUGhhc2UgMjogZml0cywgYW5hbHl0aWMgY29udHJvbCwgRi1DT05WICjO
niBkb3VibGluZywgzrwgbm9kZXMsIFFtYXgpCmxvZygiUDIgcGhhc2UgMjogZml0cyArIGNvbnRy
b2xzICsgRi1DT05WIikKcGgyID0ge30KZm9yIG5hbWUgaW4gY2ZnOgogICAgWGksIFZULCBWTCA9
IEtFUltuYW1lXTsgciA9IHsiY2hhbm5lbHMiOiB7fX0KICAgIGZvciBpbmMgaW4gKCJUIiwgIkwi
KToKICAgICAgICBjaCA9IHBoMVtuYW1lXVsiY2hhbm5lbHMiXVtpbmNdOyBmID0gZml0cyhjaFsi
bGFkZGVyX2siXSwgY2hbIkRlbHRhIl0pCiAgICAgICAgYTJfMiwgYTJfMyA9IGZbImJhc2lzMiJd
WyJjb2VmIl1bImsyIl0sIGZbImJhc2lzMyJdWyJjb2VmIl1bImsyIl07IGNpID0gbWF4KGZbImJh
c2lzMiJdWyJjaSJdWyJrMiJdLCBmWyJiYXNpczMiXVsiY2kiXVsiazIiXSkKICAgICAgICBkaXNh
Z3JlZSA9IGFicyhhMl8yIC0gYTJfMykgPiBjaQogICAgICAgIGEyX3JlYyA9IGEyXzMgaWYgZGlz
YWdyZWUgZWxzZSBhMl8yCiAgICAgICAgYW4gPSBjaFsiRDJfYW5hbHl0aWMiXTsgYW5fb2sgPSBh
YnMoYTJfMyAtIGFuKSA8PSBtYXgoZlsiYmFzaXMzIl1bImNpIl1bImsyIl0sIDFlLTkgKiBhYnMo
YW4pKQogICAgICAgIHJbImNoYW5uZWxzIl1baW5jXSA9IHsiZml0cyI6IGYsICJhMl9iYXNpczIi
OiBhMl8yLCAiYTJfYmFzaXMzIjogYTJfMywgImEzX2Jhc2lzMyI6IGZbImJhc2lzMyJdWyJjb2Vm
Il1bImszIl0sICJhNF9iYXNpczMiOiBmWyJiYXNpczMiXVsiY29lZiJdWyJrNCJdLAogICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAiYmFzZXNfZGlzYWdyZWVfYmV5b25kX0NJIjogYm9vbChk
aXNhZ3JlZSksICJhMl9vZl9yZWNvcmQiOiBhMl9yZWMsICJiYXNpc19vZl9yZWNvcmQiOiAiYmFz
aXMzIiBpZiBkaXNhZ3JlZSBlbHNlICJiYXNpczIiLAogICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAiRDJfYW5hbHl0aWMiOiBhbiwgIkZfQUdHX0FOQUxZVElDX3JlbCI6IGFicyhhMl8zIC8g
YW4gLSAxLjApLCAiRl9BR0dfQU5BTFlUSUNfcGFzcyI6IGJvb2woYW5fb2spLCAiQ0lfYTIiOiBj
aX0KICAgICMgRi1DT05WIG9uIHRoZSBUIGNoYW5uZWw6IM6eIGRvdWJsaW5nLCDOvC1ub2RlIGRv
dWJsaW5nLCBRbWF4IGRvdWJsaW5nIOKAlCBvbiBEMl9hbmFseXRpYyBhbmQgb24gRGVsdGEoMC4z
KSwgRGVsdGEoMC4wMzc1KQogICAgWGkyLCBfLCBfID0gYnVpbGQobmFtZSwgbmI9MjAsIG5hPTI0
KTsgdGFiVCA9IHBoaV90YWJsZShYaSwgIlQiLCA2NCk7IHRhYlQyID0gcGhpX3RhYmxlKFhpMiwg
IlQiLCA2NCk7IHRhYlQxMjggPSBwaGlfdGFibGUoWGksICJUIiwgMTI4KQogICAgRDJhLCBEMmIs
IEQyYyA9IEQyX2FuYWx5dGljKHRhYlQsIFZULCBWVCwgVkwpLCBEMl9hbmFseXRpYyh0YWJUMiwg
VlQsIFZULCBWTCksIEQyX2FuYWx5dGljKHRhYlQxMjgsIFZULCBWVCwgVkwpCiAgICBkQSA9IERf
b2YodGFiVCwgVlQsIFZULCBWTCwgMC4zKTsgZEIgPSBEX29mKHRhYlQyLCBWVCwgVlQsIFZMLCAw
LjMpOyBkQyA9IERfb2YodGFiVDEyOCwgVlQsIFZULCBWTCwgMC4zKTsgZFEgPSBEX29mKHRhYlQs
IFZULCBWVCwgVkwsIDAuMywgUW1heD0xMDAuMCkKICAgIHJbIkZfQ09OViJdID0geyJEMl94aV9k
b3VibGluZ19yZWwiOiBhYnMoRDJiIC8gRDJhIC0gMS4wKSwgIkQyX211MTI4X3JlbCI6IGFicyhE
MmMgLyBEMmEgLSAxLjApLCAiRDAzX3hpX2RvdWJsaW5nX3JlbCI6IGFicyhkQiAvIGRBIC0gMS4w
KSwKICAgICAgICAgICAgICAgICAgICJEMDNfbXUxMjhfcmVsIjogYWJzKGRDIC8gZEEgLSAxLjAp
LCAiRDAzX1FtYXgxMDBfcmVsIjogYWJzKGRRIC8gZEEgLSAxLjApfQogICAgclsiRl9DT05WX3Bh
c3MiXSA9IGJvb2woclsiRl9DT05WIl1bIkQyX3hpX2RvdWJsaW5nX3JlbCJdIDw9IDFlLTYgYW5k
IHJbIkZfQ09OViJdWyJEMl9tdTEyOF9yZWwiXSA8PSAxZS05IGFuZCByWyJGX0NPTlYiXVsiRDAz
X1FtYXgxMDBfcmVsIl0gPD0gMWUtOSBhbmQgclsiRl9DT05WIl1bIkQwM194aV9kb3VibGluZ19y
ZWwiXSA8PSAxZS02KQogICAgdGllID0gcGgxW25hbWVdWyJhbHBoYV90aWVfaW4iXVsibWF4X3Jl
bF9uMjQiXTsgclsiRl9BR0dfS0tfcGFzcyJdID0gYm9vbCh0aWUgPD0gMWUtOSkKICAgIFQgPSBy
WyJjaGFubmVscyJdWyJUIl07IExjID0gclsiY2hhbm5lbHMiXVsiTCJdCiAgICByWyJGX0FHR19M
X3Bhc3MiXSA9IGJvb2woYWJzKExjWyJhMl9vZl9yZWNvcmQiXSkgPiBtYXgoVEFVX0FHRywgTGNb
IkNJX2EyIl0pIGFuZCBMY1siRl9BR0dfQU5BTFlUSUNfcGFzcyJdKQogICAgYTIgPSBUWyJhMl9v
Zl9yZWNvcmQiXTsgY2kgPSBUWyJDSV9hMiJdCiAgICBpZiBub3QgKHJbIkZfQ09OVl9wYXNzIl0g
YW5kIHJbIkZfQUdHX0tLX3Bhc3MiXSBhbmQgVFsiRl9BR0dfQU5BTFlUSUNfcGFzcyJdKTogYXJt
ID0gIkE1LWFnZyBJTlNUUlVNRU5ULUxJTUlURUQiCiAgICBlbGlmIGFicyhhMikgPiBtYXgoVEFV
X0FHRywgY2kpOiBhcm0gPSAiQTMtYWdnIERJU1BFUlNJVkUgKGdyYWluLXNjYWxlIGteMikiCiAg
ICBlbGlmIGFicyhUWyJhM19iYXNpczMiXSkgPiBUQVVfQUdHIG9yIGFicyhUWyJhNF9iYXNpczMi
XSkgPiBUQVVfQUdHOiBhcm0gPSAiQTItYWdnIFBST1RFQ1RFRCAoYTIgPSAwIGF0IHRhdV9hZ2c7
IGEzL2E0IG5vbnplcm8pIgogICAgZWxzZTogYXJtID0gIkExLWFnZyBPTi1DT05FLUVYQUNUIChh
Z2dyZWdhdGUsIEJvcm4gb3JkZXIpIgogICAgclsiYXJtX2NsYXNzIl0gPSBhcm07IHJbImEyX292
ZXJfUVQiXSA9IGEyIC8gYmFua2VkW25hbWVdWyJRX1RfYSJdCiAgICBsb2coIiAgJS0xMXMgVDog
YTIoYjIpICUrLjZlIGEyKGIzKSAlKy42ZSBhMyAlKy40ZSBhNCAlKy40ZSB8IGFuYWx5dGljIEQy
ICUrLjZlIChyZWwgJS4xZSkgfCBDSSAlLjFlIHwgcmVjICVzIC0+ICVzIiAlIChuYW1lLCBUWyJh
Ml9iYXNpczIiXSwgVFsiYTJfYmFzaXMzIl0sIFRbImEzX2Jhc2lzMyJdLCBUWyJhNF9iYXNpczMi
XSwgVFsiRDJfYW5hbHl0aWMiXSwgVFsiRl9BR0dfQU5BTFlUSUNfcmVsIl0sIGNpLCBUWyJiYXNp
c19vZl9yZWNvcmQiXSwgYXJtKSkKICAgIGxvZygiICAlLTExcyBMIGN0cmw6IGEyKGIzKSAlKy42
ZSBhbmFseXRpYyAlKy42ZSAocmVsICUuMWUpIDsgRi1DT05WICVzIDsgS0sgJXMgOyBhMi9RX1Qg
JSsuNGYiICUgKG5hbWUsIExjWyJhMl9iYXNpczMiXSwgTGNbIkQyX2FuYWx5dGljIl0sIExjWyJG
X0FHR19BTkFMWVRJQ19yZWwiXSwgclsiRl9DT05WIl0sIHJbIkZfQUdHX0tLX3Bhc3MiXSwgclsi
YTJfb3Zlcl9RVCJdKSkKICAgIHBoMltuYW1lXSA9IHIKdW5pID0ge246IHBoMltuXVsiYTJfb3Zl
cl9RVCJdIGZvciBuIGluIHBoMn0Kc3ByZWFkID0gKG1heCh1bmkudmFsdWVzKCkpIC0gbWluKHVu
aS52YWx1ZXMoKSkpIC8gYWJzKG5wLm1lYW4obGlzdCh1bmkudmFsdWVzKCkpKSkKc3VtbWFyeSA9
IHsiZ2F0ZSI6ICJHLVMyQzEiLCAicGhhc2UiOiAiMyAvIFAyIGFnZ3JlZ2F0ZSIsICJsZWciOiAi
Y2hhdCIsICJlbGVjdGlvbl9FX1AyXzEiOiAiKGEpIiwgImFkZGVuZHVtX1AyX21kNSI6IEFEREVO
RFVNX1AyLCAidGF1X2FnZyI6IFRBVV9BR0csCiAgICAgICAgICAgImEyX2FnZ19vZl9yZWNvcmRf
VCI6IHtuOiBwaDJbbl1bImNoYW5uZWxzIl1bIlQiXVsiYTJfb2ZfcmVjb3JkIl0gZm9yIG4gaW4g
cGgyfSwgImEzX2FnZ19UIjoge246IHBoMltuXVsiY2hhbm5lbHMiXVsiVCJdWyJhM19iYXNpczMi
XSBmb3IgbiBpbiBwaDJ9LAogICAgICAgICAgICJhNF9hZ2dfVCI6IHtuOiBwaDJbbl1bImNoYW5u
ZWxzIl1bIlQiXVsiYTRfYmFzaXMzIl0gZm9yIG4gaW4gcGgyfSwgIkQwX1QiOiB7bjogcGgxW25d
WyJjaGFubmVscyJdWyJUIl1bIkQwX2Nsb3NlZCJdIGZvciBuIGluIHBoMX0sCiAgICAgICAgICAg
ImFybV9jbGFzc19ieV9zdWJzdHJhdGUiOiB7bjogcGgyW25dWyJhcm1fY2xhc3MiXSBmb3IgbiBp
biBwaDJ9LCAiRl9BR0dfVU5JX2EyX292ZXJfUVQiOiB1bmksICJGX0FHR19VTklfc3ByZWFkX3Jl
bCI6IGZsb2F0KHNwcmVhZCksCiAgICAgICAgICAgInJlZ2lzdGVyZWRfZXhwZWN0YXRpb24iOiAi
RElTUEVSU0lWRSAoa14zIG5vbi1hbmFseXRpYyB0ZXJtIHByZS1yZWdpc3RlcmVkKSIsICJ2ZXJk
aWN0IjogImNoYXQtbGVnIFAyIGNsYXNzIG9ubHk7IHR3by1sZWcgKENDKSBwZW5kaW5nOyBubyB3
aW5kb3cgYWN0aW9uIn0KY2twdCgiczJjMV9wMl9waGFzZTJfZml0cy5qc29uIiwgeyJwZXJfc3Vi
c3RyYXRlIjogcGgyLCAic3VtbWFyeSI6IHN1bW1hcnl9KQpsb2coIkYtQUdHLVVOSTogYTJfYWdn
L1FfVCA9ICVzIDsgc3ByZWFkICUuMmUiICUgKHtuOiByb3VuZCh4LCA1KSBmb3IgbiwgeCBpbiB1
bmkuaXRlbXMoKX0sIHNwcmVhZCkpCmxvZygiUDIgQ09NUExFVEUgKGNoYXQgbGVnKS4iKQo=
<<<EMBED-END name=g_s2c1_p2_aggregate.py>>>

### EMBED — chat P2 phase-0 checkpoint — `s2c1_p2_phase0_pin.json` (md5 0328b570af46a878970653ad8775f6d9, 1147 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_p2_phase0_pin.json md5=0328b570af46a878970653ad8775f6d9 bytes=1147 enc=b64 quarantine=1>>>
ewogIkZfQUdHX1BJTl9wYXNzIjogdHJ1ZSwKICJhZGRlbmR1bV9QMiI6ICIyZmVmZjQ0MmRmZDA4
YTM3OTQ0M2Q4OTNiOGM3NzYxYiIsCiAicGluIjogewogICJnZW04X2N1YmljIjogewogICAiUV9U
X2EiOiAwLjA3NTQ5NDMwMjA3MTIwNzc4LAogICAiVkwwIjogMTguNDQ1MzMyNzQzMDAwMzMsCiAg
ICJWTDBfYmFua2VkIjogMTguNDQ1MzMyNzQzMDAwMzMsCiAgICJWVDAiOiA5Ljg3MjQ5MjA4NjYw
MTAzMywKICAgIlZUMF9iYW5rZWQiOiA5Ljg3MjQ5MjA4NjYwMTAzMywKICAgImJhbmtlZCI6IDAu
MDc1NDk0MzAyMDcxMjA3NzgsCiAgICJkaWdpdHM3X21hdGNoIjogdHJ1ZSwKICAgInJlbCI6IDAu
MAogIH0sCiAgImdlbThfaGV4IjogewogICAiUV9UX2EiOiAwLjA1MDAyMDU0ODQ3ODUzMjA5LAog
ICAiVkwwIjogMTkuMjI4OTM4OTU0OTUzNjMsCiAgICJWTDBfYmFua2VkIjogMTkuMjI4OTM4OTU0
OTUzNjMsCiAgICJWVDAiOiAxMC4yNDg5OTc2NzQ1Njk2MTIsCiAgICJWVDBfYmFua2VkIjogMTAu
MjQ4OTk3Njc0NTY5NjEyLAogICAiYmFua2VkIjogMC4wNTAwMjA1NDg0Nzg1MzIwOSwKICAgImRp
Z2l0czdfbWF0Y2giOiB0cnVlLAogICAicmVsIjogMC4wCiAgfSwKICAic3RlcF9jdWJpYyI6IHsK
ICAgIlFfVF9hIjogMC4wNTQwNzc2MjgyNDY1MTg2NCwKICAgIlZMMCI6IDE0LjU0ODMzMTg2MzEz
ODEyNCwKICAgIlZMMF9iYW5rZWQiOiAxNC41NDgzMzE4NjMxMzgxMjQsCiAgICJWVDAiOiA4LjEx
NTc5NDQ3NzQzNzE5LAogICAiVlQwX2JhbmtlZCI6IDguMTE1Nzk0NDc3NDM3MTksCiAgICJiYW5r
ZWQiOiAwLjA1NDA3NzYyODI0NjUxODY0LAogICAiZGlnaXRzN19tYXRjaCI6IHRydWUsCiAgICJy
ZWwiOiAwLjAKICB9LAogICJzdGVwX2hleCI6IHsKICAgIlFfVF9hIjogMC4wMzUxOTA3Mzg4NjYw
NzAwMywKICAgIlZMMCI6IDE1LjIzMjQ4NzIxMjA5NTk1LAogICAiVkwwX2JhbmtlZCI6IDE1LjIz
MjQ4NzIxMjA5NTk1LAogICAiVlQwIjogOC41NDc3Nzk0Mzg3MzkyNCwKICAgIlZUMF9iYW5rZWQi
OiA4LjU0Nzc3OTQzODczOTI0LAogICAiYmFua2VkIjogMC4wMzUxOTA3Mzg4NjYwNzAwMiwKICAg
ImRpZ2l0czdfbWF0Y2giOiB0cnVlLAogICAicmVsIjogMi4yMjA0NDYwNDkyNTAzMTNlLTE2CiAg
fQogfQp9Cg==
<<<EMBED-END name=s2c1_p2_phase0_pin.json>>>

### EMBED — chat P2 phase-1 checkpoint — `s2c1_p2_phase1_ladders.json` (md5 6da62fca644d5ea6b1d7abe7329b5e2c, 12854 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_p2_phase1_ladders.json md5=6da62fca644d5ea6b1d7abe7329b5e2c bytes=12854 enc=b64 quarantine=1>>>
ewogImdlbThfY3ViaWMiOiB7CiAgIlZMIjogMTguNDQ1MzMyNzQzMDAwMzMsCiAgIlZUIjogOS44
NzI0OTIwODY2MDEwMzMsCiAgImFscGhhX3RpZV9pbiI6IHsKICAgImFscGhhX2JhbmtlZCI6IFsK
ICAgIDEuMjA1OTk4ODU5MTYyMzk4ZS0wOCwKICAgIDYuMDkzMzI2MTQwNzg4MzllLTA4LAogICAg
NC42NzIxNTI0ODQ3NDg0OThlLTA3LAogICAgMy4wMTU4NDk0MjUzMDY0MDIzZS0wNiwKICAgIDEu
NDgxMDY3NzQ1NDgxNzY1NGUtMDUKICAgXSwKICAgImFscGhhX2hlcmVfbjI0IjogWwogICAgMS4y
MDU5OTg4NTkxNjIzOTc3ZS0wOCwKICAgIDYuMDkzMzI2MTQwNzg4Mzg5ZS0wOCwKICAgIDQuNjcy
MTUyNDg0NzQ4NDk4ZS0wNywKICAgIDMuMDE1ODQ5NDI1MzA2NDAyOGUtMDYsCiAgICAxLjQ4MTA2
Nzc0NTQ4MTc2NTdlLTA1CiAgIF0sCiAgICJhbHBoYV9oZXJlX242NCI6IFsKICAgIDEuMjA1OTk4
ODU5MTYyMzk3MmUtMDgsCiAgICA2LjA5MzMyNjE0MDc4ODM4N2UtMDgsCiAgICA0LjY3MjE1MjQ4
NDc0ODQ5NzNlLTA3LAogICAgMy4wMTU4NDk0MjUzMDY0MDJlLTA2LAogICAgMS40ODEwNjc3NDU0
ODE3NjU0ZS0wNQogICBdLAogICAiZ3JpZCI6IFsKICAgIDAuMDIsCiAgICAwLjAzLAogICAgMC4w
NSwKICAgIDAuMDgsCiAgICAwLjEyCiAgIF0sCiAgICJtYXhfcmVsX24yNCI6IDIuMjIwNDQ2MDQ5
MjUwMzEzZS0xNiwKICAgIm1heF9yZWxfbjY0IjogNi42NjEzMzgxNDc3NTA5MzllLTE2CiAgfSwK
ICAiY2hhbm5lbHMiOiB7CiAgICJMIjogewogICAgIkQiOiBbCiAgICAgLTAuMDE4NzgyNDg1ODYx
MDQ0MDg1LAogICAgIC0wLjAxNzYxODgxMzE0OTQxNjI1LAogICAgIC0wLjAxNjk2MDMwODY4MjYw
OTM3MiwKICAgICAtMC4wMTY3NTU0OTk2MTMwMjM5OCwKICAgICAtMC4wMTY3Mjk2NDYzNTI3ODA1
NzMsCiAgICAgLTAuMDE2NzAzODMyMDM2MjY0NzEyLAogICAgIC0wLjAxNjcwMTMxNjM0NjcxNzkz
NiwKICAgICAtMC4wMTY2OTQ3MzA1NzY3MTE4OSwKICAgICAtMC4wMTY2ODgyMDgyOTY5NDUwMywK
ICAgICAtMC4wMTY2ODc1NzU1MDgzNDAzMiwKICAgICAtMC4wMTY2ODQyODY0MDczMDE4MDYsCiAg
ICAgLTAuMDE2Njg0MTI3OTY3NDMxOTQ3LAogICAgIC0wLjAxNjY4MzI2NTMwOTI0NTg5NSwKICAg
ICAtMC4wMTY2ODMwNDk1ODE5ODQ3NgogICAgXSwKICAgICJEMF9jbG9zZWQiOiAtMC4wMTY2ODI5
Nzc2ODc3NTg3NDcsCiAgICAiRDBfY29uc2lzdGVuY3lfcmVsIjogMy4xMzkxOTE1NTExNDkxNjc1
ZS0wOCwKICAgICJEMl9hbmFseXRpYyI6IC0wLjA1MjM2MzAyMzY4OTcwNzc1LAogICAgIkRfYXRf
MWUtNCI6IC0wLjAxNjY4Mjk3ODIxMTQ2OTM3NCwKICAgICJEZWx0YSI6IFsKICAgICAtMC4wMDIw
OTk1MDgxNzMyODUzMzc0LAogICAgIC0wLjAwMDkzNTgzNTQ2MTY1NzUwMzMsCiAgICAgLTAuMDAw
Mjc3MzMwOTk0ODUwNjI0NzMsCiAgICAgLTcuMjUyMTkyNTI2NTIzMTQ5ZS0wNSwKICAgICAtNC42
NjY4NjY1MDIxODI1NTFlLTA1LAogICAgIC0yLjA4NTQzNDg1MDU5NjQzNzZlLTA1LAogICAgIC0x
LjgzMzg2NTg5NTkxODg5ODZlLTA1LAogICAgIC0xLjE3NTI4ODg5NTMxNDQwMjVlLTA1LAogICAg
IC01LjIzMDYwOTE4NjI4MzE4MDVlLTA2LAogICAgIC00LjU5NzgyMDU4MTU3MzQ1ODVlLTA2LAog
ICAgIC0xLjMwODcxOTU0MzA1OTAyODJlLTA2LAogICAgIC0xLjE1MDI3OTY3MzE5OTYzOWUtMDYs
CiAgICAgLTIuODc2MjE0ODcxNDgwNTk4ZS0wNywKICAgICAtNy4xODk0MjI2MDEzNDc0NzNlLTA4
CiAgICBdLAogICAgImxhZGRlcl9rIjogWwogICAgIDAuMywKICAgICAwLjE1LAogICAgIDAuMDc1
LAogICAgIDAuMDM3NSwKICAgICAwLjAzLAogICAgIDAuMDIsCiAgICAgMC4wMTg3NSwKICAgICAw
LjAxNSwKICAgICAwLjAxLAogICAgIDAuMDA5Mzc1LAogICAgIDAuMDA1LAogICAgIDAuMDA0Njg3
NSwKICAgICAwLjAwMjM0Mzc1LAogICAgIDAuMDAxMTcxODc1CiAgICBdCiAgIH0sCiAgICJUIjog
ewogICAgIkQiOiBbCiAgICAgLTAuMDQ2MzU2NTQwNDAzNzU4NTM1LAogICAgIC0wLjA0NDUwMTAw
Nzc2MTAwNTgyLAogICAgIC0wLjA0Mzg5NTg5MjI3NDM3NDk2LAogICAgIC0wLjA0MzczMjY5NjY4
MDA5MDk2LAogICAgIC0wLjA0MzcxMjc2NTQyMDA2MjUsCiAgICAgLTAuMDQzNjkzMDA1NTUxODU1
MzUsCiAgICAgLTAuMDQzNjkxMDg3MzU1MzMyOTIsCiAgICAgLTAuMDQzNjg2MDcxOTgzNTI4OTA0
LAogICAgIC0wLjA0MzY4MTExMzgyNTAwMTMyLAogICAgIC0wLjA0MzY4MDYzMzI1NDcxNjQ3NCwK
ICAgICAtMC4wNDM2NzgxMzY2ODI2NDI4NCwKICAgICAtMC4wNDM2NzgwMTY0NzYxMTQ0NCwKICAg
ICAtMC4wNDM2NzczNjIwNzc4NDIxNSwKICAgICAtMC4wNDM2NzcxOTg0NjA3OTEyMgogICAgXSwK
ICAgICJEMF9jbG9zZWQiOiAtMC4wNDM2NzcxNDM5MjY5Nzk3NDUsCiAgICAiRDBfY29uc2lzdGVu
Y3lfcmVsIjogOS4wOTQwMjU3NTQ2NjM0NDhlLTA5LAogICAgIkQyX2FuYWx5dGljIjogLTAuMDM5
NzEzOTc2NzkxMjg4MTMsCiAgICAiRF9hdF8xZS00IjogLTAuMDQzNjc3MTQ0MzI0MTgwODE1LAog
ICAgIkRlbHRhIjogWwogICAgIC0wLjAwMjY3OTM5NjQ3Njc3ODc5MDYsCiAgICAgLTAuMDAwODIz
ODYzODM0MDI2MDc4NCwKICAgICAtMC4wMDAyMTg3NDgzNDczOTUyMTQ1NCwKICAgICAtNS41NTUy
NzUzMTExMjEyNjZlLTA1LAogICAgIC0zLjU2MjE0OTMwODI3NTQ3NWUtMDUsCiAgICAgLTEuNTg2
MTYyNDg3NTYwODU1ZS0wNSwKICAgICAtMS4zOTQzNDI4MzUzMTc0NzQ3ZS0wNSwKICAgICAtOC45
MjgwNTY1NDkxNTk1MTNlLTA2LAogICAgIC0zLjk2OTg5ODAyMTU3MzI3MDRlLTA2LAogICAgIC0z
LjQ4OTMyNzczNjcyODk5NzdlLTA2LAogICAgIC05LjkyNzU1NjYzMDkyODcwMmUtMDcsCiAgICAg
LTguNzI1NDkxMzQ2OTUwMzMxZS0wNywKICAgICAtMi4xODE1MDg2MjQwMjE3Nzc0ZS0wNywKICAg
ICAtNS40NTMzODExNDczNTIyNzY0ZS0wOAogICAgXSwKICAgICJsYWRkZXJfayI6IFsKICAgICAw
LjMsCiAgICAgMC4xNSwKICAgICAwLjA3NSwKICAgICAwLjAzNzUsCiAgICAgMC4wMywKICAgICAw
LjAyLAogICAgIDAuMDE4NzUsCiAgICAgMC4wMTUsCiAgICAgMC4wMSwKICAgICAwLjAwOTM3NSwK
ICAgICAwLjAwNSwKICAgICAwLjAwNDY4NzUsCiAgICAgMC4wMDIzNDM3NSwKICAgICAwLjAwMTE3
MTg3NQogICAgXQogICB9CiAgfQogfSwKICJnZW04X2hleCI6IHsKICAiVkwiOiAxOS4yMjg5Mzg5
NTQ5NTM2MywKICAiVlQiOiAxMC4yNDg5OTc2NzQ1Njk2MTIsCiAgImFscGhhX3RpZV9pbiI6IHsK
ICAgImFscGhhX2JhbmtlZCI6IFsKICAgIDcuOTkwNjMwNDc4OTA4Njk4ZS0wOSwKICAgIDQuMDM3
Mjc1NjQ4MzYxMTQ2ZS0wOCwKICAgIDMuMDk1NjM5MDE0ODg2NzdlLTA3LAogICAgMS45OTgyMDcz
MDAzOTA0ZS0wNiwKICAgIDkuODEyOTA1NDU1OTU4NDU2ZS0wNgogICBdLAogICAiYWxwaGFfaGVy
ZV9uMjQiOiBbCiAgICA3Ljk5MDYzMDQ3ODkwODY5NGUtMDksCiAgICA0LjAzNzI3NTY0ODM2MTE0
NGUtMDgsCiAgICAzLjA5NTYzOTAxNDg4Njc3ZS0wNywKICAgIDEuOTk4MjA3MzAwMzkwMzk4OGUt
MDYsCiAgICA5LjgxMjkwNTQ1NTk1ODQ1M2UtMDYKICAgXSwKICAgImFscGhhX2hlcmVfbjY0Ijog
WwogICAgNy45OTA2MzA0Nzg5MDg2OTNlLTA5LAogICAgNC4wMzcyNzU2NDgzNjExNDI1ZS0wOCwK
ICAgIDMuMDk1NjM5MDE0ODg2NzY5NmUtMDcsCiAgICAxLjk5ODIwNzMwMDM5MDM5ODhlLTA2LAog
ICAgOS44MTI5MDU0NTU5NTg0NTFlLTA2CiAgIF0sCiAgICJncmlkIjogWwogICAgMC4wMiwKICAg
IDAuMDMsCiAgICAwLjA1LAogICAgMC4wOCwKICAgIDAuMTIKICAgXSwKICAgIm1heF9yZWxfbjI0
IjogNi42NjEzMzgxNDc3NTA5MzllLTE2LAogICAibWF4X3JlbF9uNjQiOiA3Ljc3MTU2MTE3MjM3
NjA5NmUtMTYKICB9LAogICJjaGFubmVscyI6IHsKICAgIkwiOiB7CiAgICAiRCI6IFsKICAgICAt
MC4wMTIzMDQ2ODg2NTczMjMwMzIsCiAgICAgLTAuMDExNTY1ODc1NzE4NTg5Njc5LAogICAgIC0w
LjAxMTEzNTgzODAwMDc3MzkzNywKICAgICAtMC4wMTEwMDE0NTMyMTk5ODkwMjEsCiAgICAgLTAu
MDEwOTg0NDczMzEwODg4NTUzLAogICAgIC0wLjAxMDk2NzUxNTU1NDAwMDI1MywKICAgICAtMC4w
MTA5NjU4NjI3ODQ2MTYyNjIsCiAgICAgLTAuMDEwOTYxNTM1ODg0Mzk4MDEzLAogICAgIC0wLjAx
MDk1NzI1MDQ4MzkxOTIwMiwKICAgICAtMC4wMTA5NTY4MzQ3MDUwMzY4MTYsCiAgICAgLTAuMDEw
OTU0NjczNTQyNDY5NzI1LAogICAgIC0wLjAxMDk1NDU2OTQzNTM2NzY3LAogICAgIC0wLjAxMDk1
NDAwMjYwMDgzMjIyNywKICAgICAtMC4wMTA5NTM4NjA4NTAzOTU4NwogICAgXSwKICAgICJEMF9j
bG9zZWQiOiAtMC4wMTA5NTM4MTM2MDk5ODY4ODUsCiAgICAiRDBfY29uc2lzdGVuY3lfcmVsIjog
My4xNDE1Njc0NzI4MzA3ODZlLTA4LAogICAgIkQyX2FuYWx5dGljIjogLTAuMDM0NDA2ODI3MzUx
ODg3MzUsCiAgICAiRF9hdF8xZS00IjogLTAuMDEwOTUzODEzOTU0MTA4MzMsCiAgICAiRGVsdGEi
OiBbCiAgICAgLTAuMDAxMzUwODc1MDQ3MzM2MTQ2OCwKICAgICAtMC4wMDA2MTIwNjIxMDg2MDI3
OTM0LAogICAgIC0wLjAwMDE4MjAyNDM5MDc4NzA1MTQsCiAgICAgLTQuNzYzOTYxMDAwMjEzNTk3
ZS0wNSwKICAgICAtMy4wNjU5NzAwOTAxNjY3MTU2ZS0wNSwKICAgICAtMS4zNzAxOTQ0MDEzMzY3
MTJlLTA1LAogICAgIC0xLjIwNDkxNzQ2MjkzNzcwMTllLTA1LAogICAgIC03LjcyMjI3NDQxMTEy
NzQzOWUtMDYsCiAgICAgLTMuNDM2ODczOTMyMzE2MTYxOGUtMDYsCiAgICAgLTMuMDIxMDk1MDQ5
OTMwMzUzZS0wNiwKICAgICAtOC41OTkzMjQ4MjgzOTgzMTRlLTA3LAogICAgIC03LjU1ODI1Mzgw
Nzg0NDA1NmUtMDcsCiAgICAgLTEuODg5OTA4NDUzNDE0NjM1ZS0wNywKICAgICAtNC43MjQwNDA4
OTgzOTM0ZS0wOAogICAgXSwKICAgICJsYWRkZXJfayI6IFsKICAgICAwLjMsCiAgICAgMC4xNSwK
ICAgICAwLjA3NSwKICAgICAwLjAzNzUsCiAgICAgMC4wMywKICAgICAwLjAyLAogICAgIDAuMDE4
NzUsCiAgICAgMC4wMTUsCiAgICAgMC4wMSwKICAgICAwLjAwOTM3NSwKICAgICAwLjAwNSwKICAg
ICAwLjAwNDY4NzUsCiAgICAgMC4wMDIzNDM3NSwKICAgICAwLjAwMTE3MTg3NQogICAgXQogICB9
LAogICAiVCI6IHsKICAgICJEIjogWwogICAgIC0wLjAzMDY1ODIyNzYzMzQ1NzE3LAogICAgIC0w
LjAyOTQ1NTA5MjM3NTAwODYxNywKICAgICAtMC4wMjkwNjA2MDYxODQ0MjQ1NSwKICAgICAtMC4w
Mjg5NTQwODEyNDgwODM3NSwKICAgICAtMC4wMjg5NDEwNjc2NDQxMDU5MywKICAgICAtMC4wMjg5
MjgxNjUxOTA2MjMxOSwKICAgICAtMC4wMjg5MjY5MTI2NDAzMDYxOTMsCiAgICAgLTAuMDI4OTIz
NjM3NjUyOTc1MjU2LAogICAgIC0wLjAyODkyMDM5OTk3ODEyNzYyLAogICAgIC0wLjAyODkyMDA4
NjE2MzQ5ODA2MywKICAgICAtMC4wMjg5MTg0NTU4ODMyNDg4NSwKICAgICAtMC4wMjg5MTgzNzcz
ODcxODY1NDUsCiAgICAgLTAuMDI4OTE3OTUwMDU4MTAzMzY0LAogICAgIC0wLjAyODkxNzg0MzIx
NDI0MTgzOAogICAgXSwKICAgICJEMF9jbG9zZWQiOiAtMC4wMjg5MTc4MDc2MDMwNzE3MzUsCiAg
ICAiRDBfY29uc2lzdGVuY3lfcmVsIjogOC45Njk0NzQyNzQ0MjI4NWUtMDksCiAgICAiRDJfYW5h
bHl0aWMiOiAtMC4wMjU5MzM2OTM1ODQyOTQyMSwKICAgICJEX2F0XzFlLTQiOiAtMC4wMjg5MTc4
MDc4NjI0NDkyNywKICAgICJEZWx0YSI6IFsKICAgICAtMC4wMDE3NDA0MjAwMzAzODU0MzMyLAog
ICAgIC0wLjAwMDUzNzI4NDc3MTkzNjg4MTUsCiAgICAgLTAuMDAwMTQyNzk4NTgxMzUyODE2MTIs
CiAgICAgLTMuNjI3MzY0NTAxMjAxNTg4ZS0wNSwKICAgICAtMi4zMjYwMDQxMDM0MTk0MDQ2ZS0w
NSwKICAgICAtMS4wMzU3NTg3NTUxNDU0NDM5ZS0wNSwKICAgICAtOS4xMDUwMzcyMzQ0NTc0MDhl
LTA2LAogICAgIC01LjgzMDA0OTkwMzUyMDYyM2UtMDYsCiAgICAgLTIuNTkyMzc1MDU1ODg0ODMy
NGUtMDYsCiAgICAgLTIuMjc4NTYwNDI2MzI4MjYzM2UtMDYsCiAgICAgLTYuNDgyODAxNzcxMTY1
NDQ3ZS0wNywKICAgICAtNS42OTc4NDExNDgxMDE1MTJlLTA3LAogICAgIC0xLjQyNDU1MDMxNjI4
NTQ2NjdlLTA3LAogICAgIC0zLjU2MTExNzAxMDMwMzM3MmUtMDgKICAgIF0sCiAgICAibGFkZGVy
X2siOiBbCiAgICAgMC4zLAogICAgIDAuMTUsCiAgICAgMC4wNzUsCiAgICAgMC4wMzc1LAogICAg
IDAuMDMsCiAgICAgMC4wMiwKICAgICAwLjAxODc1LAogICAgIDAuMDE1LAogICAgIDAuMDEsCiAg
ICAgMC4wMDkzNzUsCiAgICAgMC4wMDUsCiAgICAgMC4wMDQ2ODc1LAogICAgIDAuMDAyMzQzNzUs
CiAgICAgMC4wMDExNzE4NzUKICAgIF0KICAgfQogIH0KIH0sCiAic3RlcF9jdWJpYyI6IHsKICAi
VkwiOiAxNC41NDgzMzE4NjMxMzgxMjQsCiAgIlZUIjogOC4xMTU3OTQ0Nzc0MzcxOSwKICAiYWxw
aGFfdGllX2luIjogewogICAiYWxwaGFfYmFua2VkIjogWwogICAgOC42Mzg3NjQyNzI5NDY4ODJl
LTA5LAogICAgNC4zNjQ3NjM2MDU0MDIzNTE0ZS0wOCwKICAgIDMuMzQ2Nzg4OTI2ODY4OTI1NmUt
MDcsCiAgICAyLjE2MDM5NDA0NDY5NzEwODZlLTA2LAogICAgMS4wNjEwMTYwMzMwMDI0MmUtMDUK
ICAgXSwKICAgImFscGhhX2hlcmVfbjI0IjogWwogICAgOC42Mzg3NjQyNzI5NDY4OGUtMDksCiAg
ICA0LjM2NDc2MzYwNTQwMjM1MmUtMDgsCiAgICAzLjM0Njc4ODkyNjg2ODkyNWUtMDcsCiAgICAy
LjE2MDM5NDA0NDY5NzEwODZlLTA2LAogICAgMS4wNjEwMTYwMzMwMDI0MTk3ZS0wNQogICBdLAog
ICAiYWxwaGFfaGVyZV9uNjQiOiBbCiAgICA4LjYzODc2NDI3Mjk0Njg3OWUtMDksCiAgICA0LjM2
NDc2MzYwNTQwMjM1MWUtMDgsCiAgICAzLjM0Njc4ODkyNjg2ODkyNDZlLTA3LAogICAgMi4xNjAz
OTQwNDQ2OTcxMDg2ZS0wNiwKICAgIDEuMDYxMDE2MDMzMDAyNDE5MmUtMDUKICAgXSwKICAgImdy
aWQiOiBbCiAgICAwLjAyLAogICAgMC4wMywKICAgIDAuMDUsCiAgICAwLjA4LAogICAgMC4xMgog
ICBdLAogICAibWF4X3JlbF9uMjQiOiAzLjMzMDY2OTA3Mzg3NTQ2OTZlLTE2LAogICAibWF4X3Jl
bF9uNjQiOiA3Ljc3MTU2MTE3MjM3NjA5NmUtMTYKICB9LAogICJjaGFubmVscyI6IHsKICAgIkwi
OiB7CiAgICAiRCI6IFsKICAgICAtMC4wMTQ2ODYyNjAwMjYxMzc4OTIsCiAgICAgLTAuMDEzNzYx
MTk4OTIxMzE3NTg5LAogICAgIC0wLjAxMzI3NjMwMzQwMDcxMTQ5LAogICAgIC0wLjAxMzEyODA4
NjkyMjQ0NDIxMiwKICAgICAtMC4wMTMxMDk0NTEzNTgxMTc2MTEsCiAgICAgLTAuMDEzMDkwODU5
NzU2NDMyMTk2LAogICAgIC0wLjAxMzA4OTA0ODc4NjM5MTU1LAogICAgIC0wLjAxMzA4NDMwODU5
MTM0NTk0NiwKICAgICAtMC4wMTMwNzk2MTUwOTcyMTkyMzQsCiAgICAgLTAuMDEzMDc5MTU5Nzg5
NTcyMTQyLAogICAgIC0wLjAxMzA3Njc5MzM0NzczMDMxOCwKICAgICAtMC4wMTMwNzY2NzkzNTk4
MjIxNDksCiAgICAgLTAuMDEzMDc2MDU4NzM5NjkyNjc4LAogICAgIC0wLjAxMzA3NTkwMzU1MjI4
ODMzMwogICAgXSwKICAgICJEMF9jbG9zZWQiOiAtMC4wMTMwNzU4NTE4MjA3MTE2NywKICAgICJE
MF9jb25zaXN0ZW5jeV9yZWwiOiAyLjg4MTM3MTA5NzI3NDE1NDZlLTA4LAogICAgIkQyX2FuYWx5
dGljIjogLTAuMDM3NjcwNTI2ODEzMTY2NjEsCiAgICAiRF9hdF8xZS00IjogLTAuMDEzMDc1ODUy
MTk3NDc1NDg1LAogICAgIkRlbHRhIjogWwogICAgIC0wLjAwMTYxMDQwODIwNTQyNjIyMTgsCiAg
ICAgLTAuMDAwNjg1MzQ3MTAwNjA1OTE4OCwKICAgICAtMC4wMDAyMDA0NTE1Nzk5OTk4MTk4LAog
ICAgIC01LjIyMzUxMDE3MzI1NDE5NjRlLTA1LAogICAgIC0zLjM1OTk1Mzc0MDU5NDE0MDRlLTA1
LAogICAgIC0xLjUwMDc5MzU3MjA1MjYyNzhlLTA1LAogICAgIC0xLjMxOTY5NjU2Nzk4Nzk4NTJl
LTA1LAogICAgIC04LjQ1Njc3MDYzNDI3NTU3OWUtMDYsCiAgICAgLTMuNzYzMjc2NTA3NTYzNzUx
ZS0wNiwKICAgICAtMy4zMDc5Njg4NjA0NzIwMjE0ZS0wNiwKICAgICAtOS40MTUyNzAxODY0ODMw
MjdlLTA3LAogICAgIC04LjI3NTM5MTEwNDc4NjAwNmUtMDcsCiAgICAgLTIuMDY5MTg5ODEwMDg0
NjkyOGUtMDcsCiAgICAgLTUuMTczMTU3NjY2MzAwODMxNmUtMDgKICAgIF0sCiAgICAibGFkZGVy
X2siOiBbCiAgICAgMC4zLAogICAgIDAuMTUsCiAgICAgMC4wNzUsCiAgICAgMC4wMzc1LAogICAg
IDAuMDMsCiAgICAgMC4wMiwKICAgICAwLjAxODc1LAogICAgIDAuMDE1LAogICAgIDAuMDEsCiAg
ICAgMC4wMDkzNzUsCiAgICAgMC4wMDUsCiAgICAgMC4wMDQ2ODc1LAogICAgIDAuMDAyMzQzNzUs
CiAgICAgMC4wMDExNzE4NzUKICAgIF0KICAgfSwKICAgIlQiOiB7CiAgICAiRCI6IFsKICAgICAt
MC4wMzM0NDEwNjIwNjcwNjU5LAogICAgIC0wLjAzMjEwNTYyNjI2ODAxNjcsCiAgICAgLTAuMDMx
NjcwNjIyOTM0MjQ4MjYsCiAgICAgLTAuMDMxNTUzMzQyMTEyMDc2OTEsCiAgICAgLTAuMDMxNTM5
MDE5NTAxMzE5OTMsCiAgICAgLTAuMDMxNTI0ODIwMjcxMzI4NzEsCiAgICAgLTAuMDMxNTIzNDQx
ODg3Mzg0MTMsCiAgICAgLTAuMDMxNTE5ODM3OTM0NzMyMTUsCiAgICAgLTAuMDMxNTE2Mjc1MTA4
MjAwNzUsCiAgICAgLTAuMDMxNTE1OTI5NzgxNDEwMzg2LAogICAgIC0wLjAzMTUxNDEzNTgwNDAx
NTk1LAogICAgIC0wLjAzMTUxNDA0OTQyNjU0NjkxLAogICAgIC0wLjAzMTUxMzU3OTE5MjEwNjg2
NSwKICAgICAtMC4wMzE1MTM0NjE2MjA5OTk2MgogICAgXSwKICAgICJEMF9jbG9zZWQiOiAtMC4w
MzE1MTM0MjI0MzQzMzYyMywKICAgICJEMF9jb25zaXN0ZW5jeV9yZWwiOiA5LjA1NzA1MTc3NTIy
OTc1MmUtMDksCiAgICAiRDJfYW5hbHl0aWMiOiAtMC4wMjg1Mzc0NzExMDc5NDQ0MjMsCiAgICAi
RF9hdF8xZS00IjogLTAuMDMxNTEzNDIyNzE5NzU0OTMsCiAgICAiRGVsdGEiOiBbCiAgICAgLTAu
MDAxOTI3NjM5NjMyNzI5NjY5LAogICAgIC0wLjAwMDU5MjIwMzgzMzY4MDQ2NDQsCiAgICAgLTAu
MDAwMTU3MjAwNDk5OTEyMDI0NjcsCiAgICAgLTMuOTkxOTY3Nzc0MDY3NTQ1ZS0wNSwKICAgICAt
Mi41NTk3MDY2OTgzNjk4NTdlLTA1LAogICAgIC0xLjEzOTc4MzY5OTI0Nzg1OTRlLTA1LAogICAg
IC0xLjAwMTk0NTMwNDc4OTc4MDhlLTA1LAogICAgIC02LjQxNTUwMDM5NTkxNDg3NWUtMDYsCiAg
ICAgLTIuODUyNjczODY0NTE3Mzc0NGUtMDYsCiAgICAgLTIuNTA3MzQ3MDc0MTUyOTU0N2UtMDYs
CiAgICAgLTcuMTMzNjk2Nzk3MTY4MDIxZS0wNywKICAgICAtNi4yNjk5MjIxMDY3ODMwMWUtMDcs
CiAgICAgLTEuNTY3NTc3NzA2MzIxMjEwNGUtMDcsCiAgICAgLTMuOTE4NjY2MzM4NjQyNTczNWUt
MDgKICAgIF0sCiAgICAibGFkZGVyX2siOiBbCiAgICAgMC4zLAogICAgIDAuMTUsCiAgICAgMC4w
NzUsCiAgICAgMC4wMzc1LAogICAgIDAuMDMsCiAgICAgMC4wMiwKICAgICAwLjAxODc1LAogICAg
IDAuMDE1LAogICAgIDAuMDEsCiAgICAgMC4wMDkzNzUsCiAgICAgMC4wMDUsCiAgICAgMC4wMDQ2
ODc1LAogICAgIDAuMDAyMzQzNzUsCiAgICAgMC4wMDExNzE4NzUKICAgIF0KICAgfQogIH0KIH0s
CiAic3RlcF9oZXgiOiB7CiAgIlZMIjogMTUuMjMyNDg3MjEyMDk1OTUsCiAgIlZUIjogOC41NDc3
Nzk0Mzg3MzkyNCwKICAiYWxwaGFfdGllX2luIjogewogICAiYWxwaGFfYmFua2VkIjogWwogICAg
NS42MjE2MzM5NTQ5MDM3MzZlLTA5LAogICAgMi44NDAzNTAyMDg1Mjc0OTNlLTA4LAogICAgMi4x
Nzc5MTA4MDU1MDI1Nzg1ZS0wNywKICAgIDEuNDA1ODcxMTIxOTMxNDc1M2UtMDYsCiAgICA2Ljkw
NDUxNDM1ODEyNTU3N2UtMDYKICAgXSwKICAgImFscGhhX2hlcmVfbjI0IjogWwogICAgNS42MjE2
MzM5NTQ5MDM3MzJlLTA5LAogICAgMi44NDAzNTAyMDg1Mjc0OTJlLTA4LAogICAgMi4xNzc5MTA4
MDU1MDI1NzgyZS0wNywKICAgIDEuNDA1ODcxMTIxOTMxNDc0OGUtMDYsCiAgICA2LjkwNDUxNDM1
ODEyNTU3NGUtMDYKICAgXSwKICAgImFscGhhX2hlcmVfbjY0IjogWwogICAgNS42MjE2MzM5NTQ5
MDM3MzFlLTA5LAogICAgMi44NDAzNTAyMDg1Mjc0OTE0ZS0wOCwKICAgIDIuMTc3OTEwODA1NTAy
NTc4ZS0wNywKICAgIDEuNDA1ODcxMTIxOTMxNDc0NGUtMDYsCiAgICA2LjkwNDUxNDM1ODEyNTU3
M2UtMDYKICAgXSwKICAgImdyaWQiOiBbCiAgICAwLjAyLAogICAgMC4wMywKICAgIDAuMDUsCiAg
ICAwLjA4LAogICAgMC4xMgogICBdLAogICAibWF4X3JlbF9uMjQiOiA1LjU1MTExNTEyMzEyNTc4
M2UtMTYsCiAgICJtYXhfcmVsX242NCI6IDguODgxNzg0MTk3MDAxMjUyZS0xNgogIH0sCiAgImNo
YW5uZWxzIjogewogICAiTCI6IHsKICAgICJEIjogWwogICAgIC0wLjAwOTY1NTc2Mzk4NDE0NDk2
NSwKICAgICAtMC4wMDkwNjMxMDY4NTQzNTA1OCwKICAgICAtMC4wMDg3NTAxMzkyMTM2MDMwNjMs
CiAgICAgLTAuMDA4NjU0NDM4MTU5NzE1NDUxLAogICAgIC0wLjAwODY0MjQwNTU2NjUwNjk1NSwK
ICAgICAtMC4wMDg2MzA0MDE0NDUwMTM1MywKICAgICAtMC4wMDg2MjkyMzIxNTMyNTkyNTEsCiAg
ICAgLTAuMDA4NjI2MTcxNTQ5MTY1NDE1LAogICAgIC0wLjAwODYyMzE0MTEwNTUyMjIyNCwKICAg
ICAtMC4wMDg2MjI4NDcxMjc4NzQxMjIsCiAgICAgLTAuMDA4NjIxMzE5MTkyODUzMTEzLAogICAg
IC0wLjAwODYyMTI0NTU5NDU5MjE0MiwKICAgICAtMC4wMDg2MjA4NDQ4ODA1Njc1ODgsCiAgICAg
LTAuMDA4NjIwNzQ0NjgxMTc0MDg0CiAgICBdLAogICAgIkQwX2Nsb3NlZCI6IC0wLjAwODYyMDcx
MTI3OTgwOTg2NCwKICAgICJEMF9jb25zaXN0ZW5jeV9yZWwiOiAyLjgyMTg1OTIzNTE2OTE5OTZl
LTA4LAogICAgIkQyX2FuYWx5dGljIjogLTAuMDI0MzIyNjE0NzA5MjQ0MDU1LAogICAgIkRfYXRf
MWUtNCI6IC0wLjAwODYyMDcxMTUyMzA3NDIwMiwKICAgICJEZWx0YSI6IFsKICAgICAtMC4wMDEw
MzUwNTI3MDQzMzUxMDA1LAogICAgIC0wLjAwMDQ0MjM5NTU3NDU0MDcxNTMsCiAgICAgLTAuMDAw
MTI5NDI3OTMzNzkzMTk4NjgsCiAgICAgLTMuMzcyNjg3OTkwNTU4NzE3NmUtMDUsCiAgICAgLTIu
MTY5NDI4NjY5NzA5MDZlLTA1LAogICAgIC05LjY5MDE2NTIwMzY2NjQxOGUtMDYsCiAgICAgLTgu
NTIwODczNDQ5Mzg3MTc4ZS0wNiwKICAgICAtNS40NjAyNjkzNTU1NTA1NTFlLTA2LAogICAgIC0y
LjQyOTgyNTcxMjM1OTU3MDdlLTA2LAogICAgIC0yLjEzNTg0ODA2NDI1ODAzOWUtMDYsCiAgICAg
LTYuMDc5MTMwNDMyNDgzMzcxZS0wNywKICAgICAtNS4zNDMxNDc4MjI3ODMxOTVlLTA3LAogICAg
IC0xLjMzNjAwNzU3NzI0MjAwNDRlLTA3LAogICAgIC0zLjM0MDEzNjQyMTk2MTUxNWUtMDgKICAg
IF0sCiAgICAibGFkZGVyX2siOiBbCiAgICAgMC4zLAogICAgIDAuMTUsCiAgICAgMC4wNzUsCiAg
ICAgMC4wMzc1LAogICAgIDAuMDMsCiAgICAgMC4wMiwKICAgICAwLjAxODc1LAogICAgIDAuMDE1
LAogICAgIDAuMDEsCiAgICAgMC4wMDkzNzUsCiAgICAgMC4wMDUsCiAgICAgMC4wMDQ2ODc1LAog
ICAgIDAuMDAyMzQzNzUsCiAgICAgMC4wMDExNzE4NzUKICAgIF0KICAgfSwKICAgIlQiOiB7CiAg
ICAiRCI6IFsKICAgICAtMC4wMjE3NjIxOTI0NjUwMDQ3NiwKICAgICAtMC4wMjA5MDg1ODIxOTY3
NjYzMzgsCiAgICAgLTAuMDIwNjI5Mjg2OTY3MTQ5OTUsCiAgICAgLTAuMDIwNTUzOTA4NTQzNTkw
MDg1LAogICAgIC0wLjAyMDU0NDcwMTA3ODY4MjE0LAogICAgIC0wLjAyMDUzNTU3MjQ5NTEwNDE0
NCwKICAgICAtMC4wMjA1MzQ2ODYzMTg5MzIxNTUsCiAgICAgLTAuMDIwNTMyMzY5Mjg0MjU5MzM3
LAogICAgIC0wLjAyMDUzMDA3ODY2Mjk3MDczOCwKICAgICAtMC4wMjA1Mjk4NTY2NDMxNzU5NDYs
CiAgICAgLTAuMDIwNTI4NzAzMjQzMjI3Mjg4LAogICAgIC0wLjAyMDUyODY0NzcwODQ4MTc0NiwK
ICAgICAtMC4wMjA1MjgzNDUzNzk5NDMwMzIsCiAgICAgLTAuMDIwNTI4MjY5Nzg5Njc1NTMKICAg
IF0sCiAgICAiRDBfY2xvc2VkIjogLTAuMDIwNTI4MjQ0NTk1MzI4MzUsCiAgICAiRDBfY29uc2lz
dGVuY3lfcmVsIjogOC45MzkxNjAwNzg4MjQ2N2UtMDksCiAgICAiRDJfYW5hbHl0aWMiOiAtMC4w
MTgzNDc2NjMxNjM5NDcwNDcsCiAgICAiRF9hdF8xZS00IjogLTAuMDIwNTI4MjQ0Nzc4ODMzNjEz
LAogICAgIkRlbHRhIjogWwogICAgIC0wLjAwMTIzMzk0Nzg2OTY3NjQwOTksCiAgICAgLTAuMDAw
MzgwMzM3NjAxNDM3OTg3NjQsCiAgICAgLTAuMDAwMTAxMDQyMzcxODIxNjAwMzksCiAgICAgLTIu
NTY2Mzk0ODI2MTczNTE4ZS0wNSwKICAgICAtMS42NDU2NDgzMzUzNzg5MDQ4ZS0wNSwKICAgICAt
Ny4zMjc4OTk3NzU3OTM0ODRlLTA2LAogICAgIC02LjQ0MTcyMzYwMzgwNDczOWUtMDYsCiAgICAg
LTQuMTI0Njg4OTMwOTg2MzU5ZS0wNiwKICAgICAtMS44MzQwNjc2NDIzODczODhlLTA2LAogICAg
IC0xLjYxMjA0Nzg0NzU5NTQ3MTRlLTA2LAogICAgIC00LjU4NjQ3ODk4OTM3NjgwNzZlLTA3LAog
ICAgIC00LjAzMTEzMTUzMzk1ODg5OGUtMDcsCiAgICAgLTEuMDA3ODQ2MTQ2ODE2NTkzM2UtMDcs
CiAgICAgLTIuNTE5NDM0NzE4MTQyODY1NmUtMDgKICAgIF0sCiAgICAibGFkZGVyX2siOiBbCiAg
ICAgMC4zLAogICAgIDAuMTUsCiAgICAgMC4wNzUsCiAgICAgMC4wMzc1LAogICAgIDAuMDMsCiAg
ICAgMC4wMiwKICAgICAwLjAxODc1LAogICAgIDAuMDE1LAogICAgIDAuMDEsCiAgICAgMC4wMDkz
NzUsCiAgICAgMC4wMDUsCiAgICAgMC4wMDQ2ODc1LAogICAgIDAuMDAyMzQzNzUsCiAgICAgMC4w
MDExNzE4NzUKICAgIF0KICAgfQogIH0KIH0KfQo=
<<<EMBED-END name=s2c1_p2_phase1_ladders.json>>>

### EMBED — chat P2 phase-2 checkpoint — `s2c1_p2_phase2_fits.json` (md5 0e8cc05e4868b8db086564e297cab6d5, 11789 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_p2_phase2_fits.json md5=0e8cc05e4868b8db086564e297cab6d5 bytes=11789 enc=b64 quarantine=1>>>
ewogInBlcl9zdWJzdHJhdGUiOiB7CiAgImdlbThfY3ViaWMiOiB7CiAgICJGX0FHR19LS19wYXNz
IjogdHJ1ZSwKICAgIkZfQUdHX0xfcGFzcyI6IGZhbHNlLAogICAiRl9DT05WIjogewogICAgIkQw
M19RbWF4MTAwX3JlbCI6IDAuMCwKICAgICJEMDNfbXUxMjhfcmVsIjogMS43NzYzNTY4Mzk0MDAy
NTA1ZS0xNSwKICAgICJEMDNfeGlfZG91YmxpbmdfcmVsIjogOS40MzY4OTU3MDkzMTM4M2UtMTQs
CiAgICAiRDJfbXUxMjhfcmVsIjogMS4wMjE0MDUxODI2NTUxNDRlLTE0LAogICAgIkQyX3hpX2Rv
dWJsaW5nX3JlbCI6IDEuMDM2OTQ4MzA0OTk5ODk2MmUtMTMKICAgfSwKICAgIkZfQ09OVl9wYXNz
IjogdHJ1ZSwKICAgImEyX292ZXJfUVQiOiAtMC41MzM2ODY2ODQwMjI2ODQ5LAogICAiYXJtX2Ns
YXNzIjogIkE1LWFnZyBJTlNUUlVNRU5ULUxJTUlURUQiLAogICAiY2hhbm5lbHMiOiB7CiAgICAi
TCI6IHsKICAgICAiQ0lfYTIiOiAwLjAwNDMxNDkwOTU1MDMzODEyMSwKICAgICAiRDJfYW5hbHl0
aWMiOiAtMC4wNTIzNjMwMjM2ODk3MDc3NSwKICAgICAiRl9BR0dfQU5BTFlUSUNfcGFzcyI6IGZh
bHNlLAogICAgICJGX0FHR19BTkFMWVRJQ19yZWwiOiAwLjA2MDE2NjIyMDAwNzY2MjI1LAogICAg
ICJhMl9iYXNpczIiOiAtMC4wNDgwMjAxMjkyMDU3MzUxLAogICAgICJhMl9iYXNpczMiOiAtMC4w
NTU1MTM1MDg4OTMyODkxMywKICAgICAiYTJfb2ZfcmVjb3JkIjogLTAuMDU1NTEzNTA4ODkzMjg5
MTMsCiAgICAgImEzX2Jhc2lzMyI6IDAuMDc4MjMyMjkxNDE3MjA1MywKICAgICAiYTRfYmFzaXMz
IjogMC4wOTY4NDQ2Mzc2OTI4Nzc4NSwKICAgICAiYmFzZXNfZGlzYWdyZWVfYmV5b25kX0NJIjog
dHJ1ZSwKICAgICAiYmFzaXNfb2ZfcmVjb3JkIjogImJhc2lzMyIsCiAgICAgImZpdHMiOiB7CiAg
ICAgICJiYXNpczIiOiB7CiAgICAgICAiY2kiOiB7CiAgICAgICAgImsyIjogMC4wMDQzMTQ5MDk1
NTAzMzgxMjEsCiAgICAgICAgIms0IjogMC4yNjQ1OTQ3MTgzNjcwODkwMwogICAgICAgfSwKICAg
ICAgICJjb2VmIjogewogICAgICAgICJrMiI6IC0wLjA0ODAyMDEyOTIwNTczNTEsCiAgICAgICAg
Ims0IjogMC4yNzQzOTQ1ODUwNTE1NDYzNQogICAgICAgfSwKICAgICAgICJybXMiOiA0Ljg5ODQ5
MjU2NzcxNzg4NWUtMDYKICAgICAgfSwKICAgICAgImJhc2lzMyI6IHsKICAgICAgICJjaSI6IHsK
ICAgICAgICAiazIiOiAwLjAwMzEyMDAwNjE3MjExMzA0MDcsCiAgICAgICAgImszIjogMC4wNzU2
MTU4ODEyNzc3NDM5MiwKICAgICAgICAiazQiOiAwLjQxNzY0MTk3ODQyNDgxMTIKICAgICAgIH0s
CiAgICAgICAiY29lZiI6IHsKICAgICAgICAiazIiOiAtMC4wNTU1MTM1MDg4OTMyODkxMywKICAg
ICAgICAiazMiOiAwLjA3ODIzMjI5MTQxNzIwNTMsCiAgICAgICAgIms0IjogMC4wOTY4NDQ2Mzc2
OTI4Nzc4NQogICAgICAgfSwKICAgICAgICJybXMiOiA2LjE1MDc1OTkwNzk1MjA2MWUtMDcKICAg
ICAgfQogICAgIH0KICAgIH0sCiAgICAiVCI6IHsKICAgICAiQ0lfYTIiOiAwLjAwMDc1MjEzNzQ1
Nzg0NjE2MzcsCiAgICAgIkQyX2FuYWx5dGljIjogLTAuMDM5NzEzOTc2NzkxMjg4MTMsCiAgICAg
IkZfQUdHX0FOQUxZVElDX3Bhc3MiOiBmYWxzZSwKICAgICAiRl9BR0dfQU5BTFlUSUNfcmVsIjog
MC4wMTQ1MTE5NDI0MDA3OTQ0NTMsCiAgICAgImEyX2Jhc2lzMiI6IC0wLjAzODk1ODI1NzA4NzQx
NTYyLAogICAgICJhMl9iYXNpczMiOiAtMC4wNDAyOTAzMDM3MzQ5ODk3OSwKICAgICAiYTJfb2Zf
cmVjb3JkIjogLTAuMDQwMjkwMzAzNzM0OTg5NzksCiAgICAgImEzX2Jhc2lzMyI6IDAuMDEzOTA2
ODE3MTk4NTc1NTc1LAogICAgICJhNF9iYXNpczMiOiAwLjA3MDUyNDQzMDQwNTc3NTM3LAogICAg
ICJiYXNlc19kaXNhZ3JlZV9iZXlvbmRfQ0kiOiB0cnVlLAogICAgICJiYXNpc19vZl9yZWNvcmQi
OiAiYmFzaXMzIiwKICAgICAiZml0cyI6IHsKICAgICAgImJhc2lzMiI6IHsKICAgICAgICJjaSI6
IHsKICAgICAgICAiazIiOiAwLjAwMDc1MjEzNzQ1Nzg0NjE2MzcsCiAgICAgICAgIms0IjogMC4w
NDQwMTI4NzY2NjkwNzUyNDYKICAgICAgIH0sCiAgICAgICAiY29lZiI6IHsKICAgICAgICAiazIi
OiAtMC4wMzg5NTgyNTcwODc0MTU2MiwKICAgICAgICAiazQiOiAwLjEwMjA4NjI2NTI1NDMyODYy
CiAgICAgICB9LAogICAgICAgInJtcyI6IDguNzE1NzYyMDIwNjU0OTU0ZS0wNwogICAgICB9LAog
ICAgICAiYmFzaXMzIjogewogICAgICAgImNpIjogewogICAgICAgICJrMiI6IDAuMDAwNTcyNDA4
Mjk1MzY2MDg5MiwKICAgICAgICAiazMiOiAwLjAxMzU3MTEzMzIyNTkwOTkxNywKICAgICAgICAi
azQiOiAwLjA3MjQzMTAzMDI5OTU3NDI4CiAgICAgICB9LAogICAgICAgImNvZWYiOiB7CiAgICAg
ICAgImsyIjogLTAuMDQwMjkwMzAzNzM0OTg5NzksCiAgICAgICAgImszIjogMC4wMTM5MDY4MTcx
OTg1NzU1NzUsCiAgICAgICAgIms0IjogMC4wNzA1MjQ0MzA0MDU3NzUzNwogICAgICAgfSwKICAg
ICAgICJybXMiOiAxLjE1NTcyNjM3NzE1NDAxMjllLTA3CiAgICAgIH0KICAgICB9CiAgICB9CiAg
IH0KICB9LAogICJnZW04X2hleCI6IHsKICAgIkZfQUdHX0tLX3Bhc3MiOiB0cnVlLAogICAiRl9B
R0dfTF9wYXNzIjogZmFsc2UsCiAgICJGX0NPTlYiOiB7CiAgICAiRDAzX1FtYXgxMDBfcmVsIjog
MC4wLAogICAgIkQwM19tdTEyOF9yZWwiOiAxLjk5ODQwMTQ0NDMyNTI4MThlLTE1LAogICAgIkQw
M194aV9kb3VibGluZ19yZWwiOiA1LjgwNjQ2NjQxODc4OTU2OWUtMTQsCiAgICAiRDJfbXUxMjhf
cmVsIjogMS4wNDM2MDk2NDMxNDc2NDcxZS0xNCwKICAgICJEMl94aV9kb3VibGluZ19yZWwiOiA1
Ljk2MTg5NzY0MjIzNzA5ZS0xNAogICB9LAogICAiRl9DT05WX3Bhc3MiOiB0cnVlLAogICAiYTJf
b3Zlcl9RVCI6IC0wLjUyNjA5NTAxNzU0NzA1MDUsCiAgICJhcm1fY2xhc3MiOiAiQTUtYWdnIElO
U1RSVU1FTlQtTElNSVRFRCIsCiAgICJjaGFubmVscyI6IHsKICAgICJMIjogewogICAgICJDSV9h
MiI6IDAuMDAyODkzNTE2NTExODY5NTA0LAogICAgICJEMl9hbmFseXRpYyI6IC0wLjAzNDQwNjgy
NzM1MTg4NzM1LAogICAgICJGX0FHR19BTkFMWVRJQ19wYXNzIjogZmFsc2UsCiAgICAgIkZfQUdH
X0FOQUxZVElDX3JlbCI6IDAuMDYxNDE5OTc0MTk0NjcwNiwKICAgICAiYTJfYmFzaXMyIjogLTAu
MDMxNDk0NTc1ODg4OTkwMTEsCiAgICAgImEyX2Jhc2lzMyI6IC0wLjAzNjUyMDA5Mzc5OTk2MDc1
NCwKICAgICAiYTJfb2ZfcmVjb3JkIjogLTAuMDM2NTIwMDkzNzk5OTYwNzU0LAogICAgICJhM19i
YXNpczMiOiAwLjA1MjQ2NzM1MDkzMTk3NjI4NCwKICAgICAiYTRfYmFzaXMzIjogMC4wNjQxMTM0
MzM5NDU1NDkzLAogICAgICJiYXNlc19kaXNhZ3JlZV9iZXlvbmRfQ0kiOiB0cnVlLAogICAgICJi
YXNpc19vZl9yZWNvcmQiOiAiYmFzaXMzIiwKICAgICAiZml0cyI6IHsKICAgICAgImJhc2lzMiI6
IHsKICAgICAgICJjaSI6IHsKICAgICAgICAiazIiOiAwLjAwMjg5MzUxNjUxMTg2OTUwNCwKICAg
ICAgICAiazQiOiAwLjE3NzM4NzM2ODcxODY1MDEzCiAgICAgICB9LAogICAgICAgImNvZWYiOiB7
CiAgICAgICAgImsyIjogLTAuMDMxNDk0NTc1ODg4OTkwMTEsCiAgICAgICAgIms0IjogMC4xODMx
ODkyNjg1ODE5NDE0NgogICAgICAgfSwKICAgICAgICJybXMiOiAzLjI4NTI0NTI4MTU5NTMyM2Ut
MDYKICAgICAgfSwKICAgICAgImJhc2lzMyI6IHsKICAgICAgICJjaSI6IHsKICAgICAgICAiazIi
OiAwLjAwMjA5Mjg2MTE4MzUyMzQ1NSwKICAgICAgICAiazMiOiAwLjA1MDcxNTcyNzQwMjU0MjY1
NCwKICAgICAgICAiazQiOiAwLjI4MDA1OTI0NDc1NDE0NDcKICAgICAgIH0sCiAgICAgICAiY29l
ZiI6IHsKICAgICAgICAiazIiOiAtMC4wMzY1MjAwOTM3OTk5NjA3NTQsCiAgICAgICAgImszIjog
MC4wNTI0NjczNTA5MzE5NzYyODQsCiAgICAgICAgIms0IjogMC4wNjQxMTM0MzM5NDU1NDkzCiAg
ICAgICB9LAogICAgICAgInJtcyI6IDQuMTI2NDM2NjMwODIwNjk1N2UtMDcKICAgICAgfQogICAg
IH0KICAgIH0sCiAgICAiVCI6IHsKICAgICAiQ0lfYTIiOiAwLjAwMDQ5ODIyMTk0Njc4ODg5MDQs
CiAgICAgIkQyX2FuYWx5dGljIjogLTAuMDI1OTMzNjkzNTg0Mjk0MjEsCiAgICAgIkZfQUdHX0FO
QUxZVElDX3Bhc3MiOiBmYWxzZSwKICAgICAiRl9BR0dfQU5BTFlUSUNfcmVsIjogMC4wMTQ3MjQ3
NzI3NzQ0OTkwMTgsCiAgICAgImEyX2Jhc2lzMiI6IC0wLjAyNTQzMzEwMzMzMDEwNDg2MiwKICAg
ICAiYTJfYmFzaXMzIjogLTAuMDI2MzE1NTYxMzI5NTI2NDI4LAogICAgICJhMl9vZl9yZWNvcmQi
OiAtMC4wMjYzMTU1NjEzMjk1MjY0MjgsCiAgICAgImEzX2Jhc2lzMyI6IDAuMDA5MjEzMDI3MjY1
NzY4NTksCiAgICAgImE0X2Jhc2lzMyI6IDAuMDQ2ODE4NDUzODYwNzQxMiwKICAgICAiYmFzZXNf
ZGlzYWdyZWVfYmV5b25kX0NJIjogdHJ1ZSwKICAgICAiYmFzaXNfb2ZfcmVjb3JkIjogImJhc2lz
MyIsCiAgICAgImZpdHMiOiB7CiAgICAgICJiYXNpczIiOiB7CiAgICAgICAiY2kiOiB7CiAgICAg
ICAgImsyIjogMC4wMDA0OTgyMjE5NDY3ODg4OTA0LAogICAgICAgICJrNCI6IDAuMDI5MTQ2Mzcz
MDg4NzU1NDgKICAgICAgIH0sCiAgICAgICAiY29lZiI6IHsKICAgICAgICAiazIiOiAtMC4wMjU0
MzMxMDMzMzAxMDQ4NjIsCiAgICAgICAgIms0IjogMC4wNjc3Mjc2MjY3NDA4NzI5OQogICAgICAg
fSwKICAgICAgICJybXMiOiA1Ljc3NDA3MzY2ODYwODgyM2UtMDcKICAgICAgfSwKICAgICAgImJh
c2lzMyI6IHsKICAgICAgICJjaSI6IHsKICAgICAgICAiazIiOiAwLjAwMDM3OTI3Njk3MzMzNzUz
MzQsCiAgICAgICAgImszIjogMC4wMDg5OTEwOTU5Mzg4ODQ2NTMsCiAgICAgICAgIms0IjogMC4w
NDc5NzcxNTg1NTQ0MzEyOQogICAgICAgfSwKICAgICAgICJjb2VmIjogewogICAgICAgICJrMiI6
IC0wLjAyNjMxNTU2MTMyOTUyNjQyOCwKICAgICAgICAiazMiOiAwLjAwOTIxMzAyNzI2NTc2ODU5
LAogICAgICAgICJrNCI6IDAuMDQ2ODE4NDUzODYwNzQxMgogICAgICAgfSwKICAgICAgICJybXMi
OiA3LjY1ODg0MDkwODU5MTkzOGUtMDgKICAgICAgfQogICAgIH0KICAgIH0KICAgfQogIH0sCiAg
InN0ZXBfY3ViaWMiOiB7CiAgICJGX0FHR19LS19wYXNzIjogdHJ1ZSwKICAgIkZfQUdHX0xfcGFz
cyI6IGZhbHNlLAogICAiRl9DT05WIjogewogICAgIkQwM19RbWF4MTAwX3JlbCI6IDIuMjIwNDQ2
MDQ5MjUwMzEzZS0xNiwKICAgICJEMDNfbXUxMjhfcmVsIjogMS41NTQzMTIyMzQ0NzUyMTkyZS0x
NSwKICAgICJEMDNfeGlfZG91YmxpbmdfcmVsIjogMS44OTQwNDA0ODAwMTA1MTdlLTEzLAogICAg
IkQyX211MTI4X3JlbCI6IDEuMDIxNDA1MTgyNjU1MTQ0ZS0xNCwKICAgICJEMl94aV9kb3VibGlu
Z19yZWwiOiAyLjAyNzI2NzI0Mjk2NTUzNThlLTEzCiAgIH0sCiAgICJGX0NPTlZfcGFzcyI6IHRy
dWUsCiAgICJhMl9vdmVyX1FUIjogLTAuNTM1MzMwOTY3NjE1NzMzLAogICAiYXJtX2NsYXNzIjog
IkE1LWFnZyBJTlNUUlVNRU5ULUxJTUlURUQiLAogICAiY2hhbm5lbHMiOiB7CiAgICAiTCI6IHsK
ICAgICAiQ0lfYTIiOiAwLjAwMjc4NDkxMzM2MDg3MDg4MTgsCiAgICAgIkQyX2FuYWx5dGljIjog
LTAuMDM3NjcwNTI2ODEzMTY2NjEsCiAgICAgIkZfQUdHX0FOQUxZVElDX3Bhc3MiOiBmYWxzZSwK
ICAgICAiRl9BR0dfQU5BTFlUSUNfcmVsIjogMC4wNTQyNDk5NDY5NDM5MjAzOCwKICAgICAiYTJf
YmFzaXMyIjogLTAuMDM0ODY4MDY4NDQyNDcyMzA0LAogICAgICJhMl9iYXNpczMiOiAtMC4wMzk3
MTQxNTA4OTQxMzA0MywKICAgICAiYTJfb2ZfcmVjb3JkIjogLTAuMDM5NzE0MTUwODk0MTMwNDMs
CiAgICAgImEzX2Jhc2lzMyI6IDAuMDUwNTk0MDExMDMzNDQ3OTUsCiAgICAgImE0X2Jhc2lzMyI6
IDAuMDczODA2Mjc4MzM1MjY5MiwKICAgICAiYmFzZXNfZGlzYWdyZWVfYmV5b25kX0NJIjogdHJ1
ZSwKICAgICAiYmFzaXNfb2ZfcmVjb3JkIjogImJhc2lzMyIsCiAgICAgImZpdHMiOiB7CiAgICAg
ICJiYXNpczIiOiB7CiAgICAgICAiY2kiOiB7CiAgICAgICAgImsyIjogMC4wMDI3ODQ5MTMzNjA4
NzA4ODE4LAogICAgICAgICJrNCI6IDAuMTY5OTgwMjM0MTc2NTI4NTgKICAgICAgIH0sCiAgICAg
ICAiY29lZiI6IHsKICAgICAgICAiazIiOiAtMC4wMzQ4NjgwNjg0NDI0NzIzMDQsCiAgICAgICAg
Ims0IjogMC4xODg2MzA1MjU4Nzk2NDA2MwogICAgICAgfSwKICAgICAgICJybXMiOiAzLjE2ODIy
NDg5MTMxODk5OGUtMDYKICAgICAgfSwKICAgICAgImJhc2lzMyI6IHsKICAgICAgICJjaSI6IHsK
ICAgICAgICAiazIiOiAwLjAwMjAyNDUwNjUyNTczNjkwMDgsCiAgICAgICAgImszIjogMC4wNDg5
NTMyNjg2MjQ1NTQxNjYsCiAgICAgICAgIms0IjogMC4yNjk0Mzg5MjUwODI3NTA2NAogICAgICAg
fSwKICAgICAgICJjb2VmIjogewogICAgICAgICJrMiI6IC0wLjAzOTcxNDE1MDg5NDEzMDQzLAog
ICAgICAgICJrMyI6IDAuMDUwNTk0MDExMDMzNDQ3OTUsCiAgICAgICAgIms0IjogMC4wNzM4MDYy
NzgzMzUyNjkyCiAgICAgICB9LAogICAgICAgInJtcyI6IDQuMDAxMjQzNjU0Nzk3NTUwM2UtMDcK
ICAgICAgfQogICAgIH0KICAgIH0sCiAgICAiVCI6IHsKICAgICAiQ0lfYTIiOiAwLjAwMDUzNzU5
NDA3MTY0Mjg5NTQsCiAgICAgIkQyX2FuYWx5dGljIjogLTAuMDI4NTM3NDcxMTA3OTQ0NDIzLAog
ICAgICJGX0FHR19BTkFMWVRJQ19wYXNzIjogZmFsc2UsCiAgICAgIkZfQUdHX0FOQUxZVElDX3Jl
bCI6IDAuMDE0NDM1Njg1MTQwNzc2NzU1LAogICAgICJhMl9iYXNpczIiOiAtMC4wMjc5OTczMTc3
MTY1MjkxOTgsCiAgICAgImEyX2Jhc2lzMyI6IC0wLjAyODk0OTQyOTA1NTU3MjcyLAogICAgICJh
Ml9vZl9yZWNvcmQiOiAtMC4wMjg5NDk0MjkwNTU1NzI3MiwKICAgICAiYTNfYmFzaXMzIjogMC4w
MDk5NDAyMjEyMTQzODY2MTksCiAgICAgImE0X2Jhc2lzMyI6IDAuMDUwNTQ2MTQ2ODU4NTI2NDgs
CiAgICAgImJhc2VzX2Rpc2FncmVlX2JleW9uZF9DSSI6IHRydWUsCiAgICAgImJhc2lzX29mX3Jl
Y29yZCI6ICJiYXNpczMiLAogICAgICJmaXRzIjogewogICAgICAiYmFzaXMyIjogewogICAgICAg
ImNpIjogewogICAgICAgICJrMiI6IDAuMDAwNTM3NTk0MDcxNjQyODk1NCwKICAgICAgICAiazQi
OiAwLjAzMTQ1NjQ1MjEzMjY0OTk3CiAgICAgICB9LAogICAgICAgImNvZWYiOiB7CiAgICAgICAg
ImsyIjogLTAuMDI3OTk3MzE3NzE2NTI5MTk4LAogICAgICAgICJrNCI6IDAuMDczMTA1NzAyNzgz
Mjc3NTUKICAgICAgIH0sCiAgICAgICAicm1zIjogNi4yMjk4MDEzMjA1ODQ2MjNlLTA3CiAgICAg
IH0sCiAgICAgICJiYXNpczMiOiB7CiAgICAgICAiY2kiOiB7CiAgICAgICAgImsyIjogMC4wMDA0
MDkxNTgyNzM1NjQ1MTgsCiAgICAgICAgImszIjogMC4wMDk3MDAzOTI3MDE0NjU3NywKICAgICAg
ICAiazQiOiAwLjA1MTc3MDAxMzQ1MjMwODM5NgogICAgICAgfSwKICAgICAgICJjb2VmIjogewog
ICAgICAgICJrMiI6IC0wLjAyODk0OTQyOTA1NTU3MjcyLAogICAgICAgICJrMyI6IDAuMDA5OTQw
MjIxMjE0Mzg2NjE5LAogICAgICAgICJrNCI6IDAuMDUwNTQ2MTQ2ODU4NTI2NDgKICAgICAgIH0s
CiAgICAgICAicm1zIjogOC4yNjEzOTU5MTYxMzgwMzNlLTA4CiAgICAgIH0KICAgICB9CiAgICB9
CiAgIH0KICB9LAogICJzdGVwX2hleCI6IHsKICAgIkZfQUdHX0tLX3Bhc3MiOiB0cnVlLAogICAi
Rl9BR0dfTF9wYXNzIjogZmFsc2UsCiAgICJGX0NPTlYiOiB7CiAgICAiRDAzX1FtYXgxMDBfcmVs
IjogMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgICJEMDNfbXUxMjhfcmVsIjogMS41NTQzMTIy
MzQ0NzUyMTkyZS0xNSwKICAgICJEMDNfeGlfZG91YmxpbmdfcmVsIjogMi42NjQ1MzUyNTkxMDAz
NzU3ZS0xNSwKICAgICJEMl9tdTEyOF9yZWwiOiAxLjA2NTgxNDEwMzY0MDE1MDNlLTE0LAogICAg
IkQyX3hpX2RvdWJsaW5nX3JlbCI6IDUuODg0MTgyMDMwNTEzMzNlLTE1CiAgIH0sCiAgICJGX0NP
TlZfcGFzcyI6IHRydWUsCiAgICJhMl9vdmVyX1FUIjogLTAuNTI4OTkxODQ5NTgxNTIwNiwKICAg
ImFybV9jbGFzcyI6ICJBNS1hZ2cgSU5TVFJVTUVOVC1MSU1JVEVEIiwKICAgImNoYW5uZWxzIjog
ewogICAgIkwiOiB7CiAgICAgIkNJX2EyIjogMC4wMDE3ODgwMDE4MzIwNTcxNTMyLAogICAgICJE
Ml9hbmFseXRpYyI6IC0wLjAyNDMyMjYxNDcwOTI0NDA1NSwKICAgICAiRl9BR0dfQU5BTFlUSUNf
cGFzcyI6IGZhbHNlLAogICAgICJGX0FHR19BTkFMWVRJQ19yZWwiOiAwLjA1NDAyMjIzODgwNTgz
NDAxLAogICAgICJhMl9iYXNpczIiOiAtMC4wMjI1MjM0NDM0MjM3OTM3ODIsCiAgICAgImEyX2Jh
c2lzMyI6IC0wLjAyNTYzNjU3NjgwOTQ0OTEyNywKICAgICAiYTJfb2ZfcmVjb3JkIjogLTAuMDI1
NjM2NTc2ODA5NDQ5MTI3LAogICAgICJhM19iYXNpczMiOiAwLjAzMjUwMTY5NzI4NTEwMjcxNSwK
ICAgICAiYTRfYmFzaXMzIjogMC4wNDg3Mjc4NzgwODcyODU2NCwKICAgICAiYmFzZXNfZGlzYWdy
ZWVfYmV5b25kX0NJIjogdHJ1ZSwKICAgICAiYmFzaXNfb2ZfcmVjb3JkIjogImJhc2lzMyIsCiAg
ICAgImZpdHMiOiB7CiAgICAgICJiYXNpczIiOiB7CiAgICAgICAiY2kiOiB7CiAgICAgICAgImsy
IjogMC4wMDE3ODgwMDE4MzIwNTcxNTMyLAogICAgICAgICJrNCI6IDAuMTA4OTg2MTg4MTQ5ODQy
OTMKICAgICAgIH0sCiAgICAgICAiY29lZiI6IHsKICAgICAgICAiazIiOiAtMC4wMjI1MjM0NDM0
MjM3OTM3ODIsCiAgICAgICAgIms0IjogMC4xMjI0OTEyMTIwOTU1MjY3MQogICAgICAgfSwKICAg
ICAgICJybXMiOiAyLjAzNTMyODgyODI1MTUwNjNlLTA2CiAgICAgIH0sCiAgICAgICJiYXNpczMi
OiB7CiAgICAgICAiY2kiOiB7CiAgICAgICAgImsyIjogMC4wMDEzMDE3ODk5Mjg3MzY3Nzk2LAog
ICAgICAgICJrMyI6IDAuMDMxNDU3MTAwNjAzMTczMjksCiAgICAgICAgIms0IjogMC4xNzI5NjY4
NzE2OTg2MzA4CiAgICAgICB9LAogICAgICAgImNvZWYiOiB7CiAgICAgICAgImsyIjogLTAuMDI1
NjM2NTc2ODA5NDQ5MTI3LAogICAgICAgICJrMyI6IDAuMDMyNTAxNjk3Mjg1MTAyNzE1LAogICAg
ICAgICJrNCI6IDAuMDQ4NzI3ODc4MDg3Mjg1NjQKICAgICAgIH0sCiAgICAgICAicm1zIjogMi41
NzQ3Mjc1NDk4OTAyOTE1ZS0wNwogICAgICB9CiAgICAgfQogICAgfSwKICAgICJUIjogewogICAg
ICJDSV9hMiI6IDAuMDAwMzQ5NTgzNTUwMTkxNTczNCwKICAgICAiRDJfYW5hbHl0aWMiOiAtMC4w
MTgzNDc2NjMxNjM5NDcwNDcsCiAgICAgIkZfQUdHX0FOQUxZVElDX3Bhc3MiOiBmYWxzZSwKICAg
ICAiRl9BR0dfQU5BTFlUSUNfcmVsIjogMC4wMTQ2MDQwODc0Mjg1MzczNiwKICAgICAiYTJfYmFz
aXMyIjogLTAuMDE3OTk2NDE4MjM0OTEzMjI0LAogICAgICJhMl9iYXNpczMiOiAtMC4wMTg2MTU2
MTQwNDA5MDI2ODMsCiAgICAgImEyX29mX3JlY29yZCI6IC0wLjAxODYxNTYxNDA0MDkwMjY4MywK
ICAgICAiYTNfYmFzaXMzIjogMC4wMDY0NjQ1MjA1MTc4ODI2ODI2LAogICAgICJhNF9iYXNpczMi
OiAwLjAzMjk1MjU3Mzc2MjA1MDM2NiwKICAgICAiYmFzZXNfZGlzYWdyZWVfYmV5b25kX0NJIjog
dHJ1ZSwKICAgICAiYmFzaXNfb2ZfcmVjb3JkIjogImJhc2lzMyIsCiAgICAgImZpdHMiOiB7CiAg
ICAgICJiYXNpczIiOiB7CiAgICAgICAiY2kiOiB7CiAgICAgICAgImsyIjogMC4wMDAzNDk1ODM1
NTAxOTE1NzM0LAogICAgICAgICJrNCI6IDAuMDIwNDUwMjMzMzQyNDYxNzgKICAgICAgIH0sCiAg
ICAgICAiY29lZiI6IHsKICAgICAgICAiazIiOiAtMC4wMTc5OTY0MTgyMzQ5MTMyMjQsCiAgICAg
ICAgIms0IjogMC4wNDc2MjM5NDg2NzQ1OTI4OTUKICAgICAgIH0sCiAgICAgICAicm1zIjogNC4w
NTE1MDY3MDA4MzQ0ODhlLTA3CiAgICAgIH0sCiAgICAgICJiYXNpczMiOiB7CiAgICAgICAiY2ki
OiB7CiAgICAgICAgImsyIjogMC4wMDAyNjYxMzM0NDUxNzMzNjUyLAogICAgICAgICJrMyI6IDAu
MDA2MzA4ODM0OTUzNzAyNTUzLAogICAgICAgICJrNCI6IDAuMDMzNjYzNjEyNTY4OTE2ODI2CiAg
ICAgICB9LAogICAgICAgImNvZWYiOiB7CiAgICAgICAgImsyIjogLTAuMDE4NjE1NjE0MDQwOTAy
NjgzLAogICAgICAgICJrMyI6IDAuMDA2NDY0NTIwNTE3ODgyNjgyNiwKICAgICAgICAiazQiOiAw
LjAzMjk1MjU3Mzc2MjA1MDM2NgogICAgICAgfSwKICAgICAgICJybXMiOiA1LjM3NDE4ODMyMDQ5
NTI2N2UtMDgKICAgICAgfQogICAgIH0KICAgIH0KICAgfQogIH0KIH0sCiAic3VtbWFyeSI6IHsK
ICAiRDBfVCI6IHsKICAgImdlbThfY3ViaWMiOiAtMC4wNDM2NzcxNDM5MjY5Nzk3NDUsCiAgICJn
ZW04X2hleCI6IC0wLjAyODkxNzgwNzYwMzA3MTczNSwKICAgInN0ZXBfY3ViaWMiOiAtMC4wMzE1
MTM0MjI0MzQzMzYyMywKICAgInN0ZXBfaGV4IjogLTAuMDIwNTI4MjQ0NTk1MzI4MzUKICB9LAog
ICJGX0FHR19VTklfYTJfb3Zlcl9RVCI6IHsKICAgImdlbThfY3ViaWMiOiAtMC41MzM2ODY2ODQw
MjI2ODQ5LAogICAiZ2VtOF9oZXgiOiAtMC41MjYwOTUwMTc1NDcwNTA1LAogICAic3RlcF9jdWJp
YyI6IC0wLjUzNTMzMDk2NzYxNTczMywKICAgInN0ZXBfaGV4IjogLTAuNTI4OTkxODQ5NTgxNTIw
NgogIH0sCiAgIkZfQUdHX1VOSV9zcHJlYWRfcmVsIjogMC4wMTczOTI2NDcwODg4NDI1NTYsCiAg
ImEyX2FnZ19vZl9yZWNvcmRfVCI6IHsKICAgImdlbThfY3ViaWMiOiAtMC4wNDAyOTAzMDM3MzQ5
ODk3OSwKICAgImdlbThfaGV4IjogLTAuMDI2MzE1NTYxMzI5NTI2NDI4LAogICAic3RlcF9jdWJp
YyI6IC0wLjAyODk0OTQyOTA1NTU3MjcyLAogICAic3RlcF9oZXgiOiAtMC4wMTg2MTU2MTQwNDA5
MDI2ODMKICB9LAogICJhM19hZ2dfVCI6IHsKICAgImdlbThfY3ViaWMiOiAwLjAxMzkwNjgxNzE5
ODU3NTU3NSwKICAgImdlbThfaGV4IjogMC4wMDkyMTMwMjcyNjU3Njg1OSwKICAgInN0ZXBfY3Vi
aWMiOiAwLjAwOTk0MDIyMTIxNDM4NjYxOSwKICAgInN0ZXBfaGV4IjogMC4wMDY0NjQ1MjA1MTc4
ODI2ODI2CiAgfSwKICAiYTRfYWdnX1QiOiB7CiAgICJnZW04X2N1YmljIjogMC4wNzA1MjQ0MzA0
MDU3NzUzNywKICAgImdlbThfaGV4IjogMC4wNDY4MTg0NTM4NjA3NDEyLAogICAic3RlcF9jdWJp
YyI6IDAuMDUwNTQ2MTQ2ODU4NTI2NDgsCiAgICJzdGVwX2hleCI6IDAuMDMyOTUyNTczNzYyMDUw
MzY2CiAgfSwKICAiYWRkZW5kdW1fUDJfbWQ1IjogIjJmZWZmNDQyZGZkMDhhMzc5NDQzZDg5M2I4
Yzc3NjFiIiwKICAiYXJtX2NsYXNzX2J5X3N1YnN0cmF0ZSI6IHsKICAgImdlbThfY3ViaWMiOiAi
QTUtYWdnIElOU1RSVU1FTlQtTElNSVRFRCIsCiAgICJnZW04X2hleCI6ICJBNS1hZ2cgSU5TVFJV
TUVOVC1MSU1JVEVEIiwKICAgInN0ZXBfY3ViaWMiOiAiQTUtYWdnIElOU1RSVU1FTlQtTElNSVRF
RCIsCiAgICJzdGVwX2hleCI6ICJBNS1hZ2cgSU5TVFJVTUVOVC1MSU1JVEVEIgogIH0sCiAgImVs
ZWN0aW9uX0VfUDJfMSI6ICIoYSkiLAogICJnYXRlIjogIkctUzJDMSIsCiAgImxlZyI6ICJjaGF0
IiwKICAicGhhc2UiOiAiMyAvIFAyIGFnZ3JlZ2F0ZSIsCiAgInJlZ2lzdGVyZWRfZXhwZWN0YXRp
b24iOiAiRElTUEVSU0lWRSAoa14zIG5vbi1hbmFseXRpYyB0ZXJtIHByZS1yZWdpc3RlcmVkKSIs
CiAgInRhdV9hZ2ciOiAxZS0wNiwKICAidmVyZGljdCI6ICJjaGF0LWxlZyBQMiBjbGFzcyBvbmx5
OyB0d28tbGVnIChDQykgcGVuZGluZzsgbm8gd2luZG93IGFjdGlvbiIKIH0KfQo=
<<<EMBED-END name=s2c1_p2_phase2_fits.json>>>

### EMBED — chat structure diagnostic — `s2c1_p2_structure_diag.json` (md5 60add009c282b9d603021ba0adbfa1e2, 5027 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_p2_structure_diag.json md5=60add009c282b9d603021ba0adbfa1e2 bytes=5027 enc=b64 quarantine=1>>>
ewogIkZfQUdHX1VOSV9hbmFseXRpYyI6IHsKICAiYTJfb3Zlcl9RVCI6IHsKICAgImdlbThfY3Vi
aWMiOiAtMC41MjYwNTI2Mzg0MzM5NDU2LAogICAiZ2VtOF9oZXgiOiAtMC41MTg0NjA4MDAwNzM0
ODM1LAogICAic3RlcF9jdWJpYyI6IC0wLjUyNzcxMzA2NzkyMjUzLAogICAic3RlcF9oZXgiOiAt
MC41MjEzNzc2MDU0NDgyNzI2CiAgfSwKICAic3ByZWFkX3JlbCI6IDAuMDE3Njc3MjA2MTA4OTM1
MzkzCiB9LAogInBlcl9zdWJzdHJhdGUiOiB7CiAgImdlbThfY3ViaWMiOiB7CiAgICJMIjogewog
ICAgIkQwIjogLTAuMDE2NjgyOTc3Njg3NzU4NzQ3LAogICAgIlJfb3Zlcl9rNF9hdF9rIjogewog
ICAgICIwLjAwMTkiOiAwLjU3MDMyOTE0NzkwNDg2MDYsCiAgICAgIjAuMDAzNiI6IDAuNTY5NzM4
MjI2NjI2MzU5NSwKICAgICAiMC4wMDY3IjogMC41Njk1ODM0NTgyNDU0OTUsCiAgICAgIjAuMDEy
NiI6IDAuNTY5MDM0MjIwNDA3NjQKICAgIH0sCiAgICAiYTJfYWdnX2FuYWx5dGljIjogLTAuMDUy
MzYzMDIzNjg5NzA3NzUsCiAgICAiZXZlbl9iYXNpc19maXQiOiB7CiAgICAgImE0IjogMC41NTQz
NzgyMjUwODcyOTkxLAogICAgICJhNiI6IC0zLjcwMjIwMDgwNzA1MDYyNiwKICAgICAiYTgiOiAx
Mi41MjMxNTM5NDAyMjQ0NzcsCiAgICAgInJtcyI6IDMuMzk0MDE3NDM4MjQyMjI0ZS0wNwogICAg
fSwKICAgICJzbWFsbGtfY29uZmlybWF0aW9uX3JlbCI6IDAuMDAwNDUzNDI5NTIzNjI4NzAxMTUs
CiAgICAic3B1cmlvdXNfYTNfaWZfazNfYmFzaXMiOiAwLjA1OTM5MTQ2ODIxMTE4NzQ4CiAgIH0s
CiAgICJUIjogewogICAgIkQwIjogLTAuMDQzNjc3MTQzOTI2OTc5NzQ1LAogICAgIlJfb3Zlcl9r
NF9hdF9rIjogewogICAgICIwLjAwMTkiOiAwLjIyMzg5NDYzOTY0ODc3NTY1LAogICAgICIwLjAw
MzYiOiAwLjE1MDEzMDMyOTUzNTA3MDE2LAogICAgICIwLjAwNjciOiAwLjE0OTk5ODYxOTY4MDA0
MDEsCiAgICAgIjAuMDEyNiI6IDAuMTQ5OTMwMjY0ODQxNDI5NDMKICAgIH0sCiAgICAiYTJfYWdn
X2FuYWx5dGljIjogLTAuMDM5NzEzOTc2NzkxMjg4MTMsCiAgICAiZXZlbl9iYXNpc19maXQiOiB7
CiAgICAgImE0IjogMC4xNDkyNTQyNTgxMDY4MTQxNCwKICAgICAiYTYiOiAtMC41NDY0ODI1Mjc1
NTgzNTQ5LAogICAgICJhOCI6IDEuMjg0NzEwNTc5NzU3NDkzOCwKICAgICAicm1zIjogMS44NDY1
MjgyNjE0Njg1MzI2ZS0wOAogICAgfSwKICAgICJzbWFsbGtfY29uZmlybWF0aW9uX3JlbCI6IDAu
MDAwMTE2MTMxNjY5ODM2NTk0NCwKICAgICJzcHVyaW91c19hM19pZl9rM19iYXNpcyI6IDAuMDEw
OTgxNjc1NDEwNTgyNjUzCiAgIH0sCiAgICJhMl9vdmVyX1FUIjogLTAuNTI2MDUyNjM4NDMzOTQ1
NiwKICAgInJhdGlvX2EyX0xfb3Zlcl9UIjogMS4zMTg1MDM2NTg0MTk2ODIKICB9LAogICJnZW04
X2hleCI6IHsKICAgIkwiOiB7CiAgICAiRDAiOiAtMC4wMTA5NTM4MTM2MDk5ODY4ODUsCiAgICAi
Ul9vdmVyX2s0X2F0X2siOiB7CiAgICAgIjAuMDAxOSI6IDAuMzgxNTQ3MjA0ODM1MDIwNCwKICAg
ICAiMC4wMDM2IjogMC4zODExNjEzOTE1OTQxNTE2LAogICAgICIwLjAwNjciOiAwLjM4MTA1Nzc4
ODg4MzczNzY1LAogICAgICIwLjAxMjYiOiAwLjM4MDY5MDE2MDk5ODgzMjM1CiAgICB9LAogICAg
ImEyX2FnZ19hbmFseXRpYyI6IC0wLjAzNDQwNjgyNzM1MTg4NzM1LAogICAgImV2ZW5fYmFzaXNf
Zml0IjogewogICAgICJhNCI6IDAuMzcwOTE4NDM4NDQyMTM4MzQsCiAgICAgImE2IjogLTIuNDgx
MTA5NTc5MjE1MDEyLAogICAgICJhOCI6IDguMzgzNzEwNDI3MTE4NDUsCiAgICAgInJtcyI6IDIu
MjY0Njc2MTQ5OTAyMjg0NGUtMDcKICAgIH0sCiAgICAic21hbGxrX2NvbmZpcm1hdGlvbl9yZWwi
OiAwLjAwMDIxMzI0MjIwNzY2OTYwNjEsCiAgICAic3B1cmlvdXNfYTNfaWZfazNfYmFzaXMiOiAw
LjAzOTgzNzU2NjMxNjQ0OTg4CiAgIH0sCiAgICJUIjogewogICAgIkQwIjogLTAuMDI4OTE3ODA3
NjAzMDcxNzM1LAogICAgIlJfb3Zlcl9rNF9hdF9rIjogewogICAgICIwLjAwMTkiOiAwLjE0Nzkz
NzYyMTgwNjEyNzc3LAogICAgICIwLjAwMzYiOiAwLjA5OTUzOTA1NzM1ODQ4NjE5LAogICAgICIw
LjAwNjciOiAwLjA5OTQ1MTk3NzE4NTg3MjIsCiAgICAgIjAuMDEyNiI6IDAuMDk5NDA2NzkzMTg2
MjcyODIKICAgIH0sCiAgICAiYTJfYWdnX2FuYWx5dGljIjogLTAuMDI1OTMzNjkzNTg0Mjk0MjEs
CiAgICAiZXZlbl9iYXNpc19maXQiOiB7CiAgICAgImE0IjogMC4wOTg5NjQxOTUxMjQ0NDgwNSwK
ICAgICAiYTYiOiAtMC4zNjE1MzA0MDc5MDUwNDI3NiwKICAgICAiYTgiOiAwLjg0NjgxNDM4ODE3
MzA2MzQsCiAgICAgInJtcyI6IDEuMjEwODAyMTQ3ODQ5NzY0OWUtMDgKICAgIH0sCiAgICAic21h
bGxrX2NvbmZpcm1hdGlvbl9yZWwiOiAwLjAwMDExNzg3MzMzMTcyMzUyODEsCiAgICAic3B1cmlv
dXNfYTNfaWZfazNfYmFzaXMiOiAwLjAwNzI3NzIwMTk2MzA4MDYzCiAgIH0sCiAgICJhMl9vdmVy
X1FUIjogLTAuNTE4NDYwODAwMDczNDgzNSwKICAgInJhdGlvX2EyX0xfb3Zlcl9UIjogMS4zMjY3
MjI5ODQ1MjQwNjI1CiAgfSwKICAic3RlcF9jdWJpYyI6IHsKICAgIkwiOiB7CiAgICAiRDAiOiAt
MC4wMTMwNzU4NTE4MjA3MTE2NywKICAgICJSX292ZXJfazRfYXRfayI6IHsKICAgICAiMC4wMDE5
IjogMC4zNzgzNjk4ODc5NjU4MjE0LAogICAgICIwLjAwMzYiOiAwLjM3Nzg3OTkyMDg4MzUwMDEs
CiAgICAgIjAuMDA2NyI6IDAuMzc3NzgzMTcxNDg0NzgyNCwKICAgICAiMC4wMTI2IjogMC4zNzc0
Mzk3Nzg3NzU5MTU4NAogICAgfSwKICAgICJhMl9hZ2dfYW5hbHl0aWMiOiAtMC4wMzc2NzA1MjY4
MTMxNjY2MSwKICAgICJldmVuX2Jhc2lzX2ZpdCI6IHsKICAgICAiYTQiOiAwLjM2ODgyMTQ2NDQ4
MTI2MSwKICAgICAiYTYiOiAtMi4zNTc2MjUyMTY3NTY0NjkzLAogICAgICJhOCI6IDcuNzkxNzYz
MDgxMjA5NjcxLAogICAgICJybXMiOiAyLjAxODQ0MjAzMjE2NTc4OTVlLTA3CiAgICB9LAogICAg
InNtYWxsa19jb25maXJtYXRpb25fcmVsIjogMC4wMDAxOTMwOTExNzAwNTg3MjM0NSwKICAgICJz
cHVyaW91c19hM19pZl9rM19iYXNpcyI6IDAuMDM4NTQwNjA4MzMzNTc0OQogICB9LAogICAiVCI6
IHsKICAgICJEMCI6IC0wLjAzMTUxMzQyMjQzNDMzNjIzLAogICAgIlJfb3Zlcl9rNF9hdF9rIjog
ewogICAgICIwLjAwMTkiOiAwLjE2NTQ1MDgyNzk5OTI5NzE0LAogICAgICIwLjAwMzYiOiAwLjEw
NzQ0MzQ1ODk0MjY2MjUxLAogICAgICIwLjAwNjciOiAwLjEwNzQwNDMzOTYzNjk5NzIzLAogICAg
ICIwLjAxMjYiOiAwLjEwNzI5OTI3MjAyOTk1MDYxCiAgICB9LAogICAgImEyX2FnZ19hbmFseXRp
YyI6IC0wLjAyODUzNzQ3MTEwNzk0NDQyMywKICAgICJldmVuX2Jhc2lzX2ZpdCI6IHsKICAgICAi
YTQiOiAwLjEwNjgxNzI1OTI4MjcwMDc1LAogICAgICJhNiI6IC0wLjM5MDQ4MzkzNTI3NTExNDks
CiAgICAgImE4IjogMC45MTcxOTY5NTkyODc2Njc1LAogICAgICJybXMiOiAxLjMxNzAyNjQ5NjMy
ODIwMWUtMDgKICAgIH0sCiAgICAic21hbGxrX2NvbmZpcm1hdGlvbl9yZWwiOiAwLjAwMDExNTMx
NDI0MzQ5NDUzNTM0LAogICAgInNwdXJpb3VzX2EzX2lmX2szX2Jhc2lzIjogMC4wMDc4NDk5MjI3
MDMxNDk5NTQKICAgfSwKICAgImEyX292ZXJfUVQiOiAtMC41Mjc3MTMwNjc5MjI1MywKICAgInJh
dGlvX2EyX0xfb3Zlcl9UIjogMS4zMjAwMzczMTc2MjYyMTY2CiAgfSwKICAic3RlcF9oZXgiOiB7
CiAgICJMIjogewogICAgIkQwIjogLTAuMDA4NjIwNzExMjc5ODA5ODY0LAogICAgIlJfb3Zlcl9r
NF9hdF9rIjogewogICAgICIwLjAwMTkiOiAwLjI0NDA2ODUxNDE0NTg5NzcyLAogICAgICIwLjAw
MzYiOiAwLjI0Mzc0Mjg3MDk4NTU4Mjc4LAogICAgICIwLjAwNjciOiAwLjI0MzY4MTMxNTUzODk2
Mjc3LAogICAgICIwLjAxMjYiOiAwLjI0MzQ2Mjg4ODgyOTA4MjIKICAgIH0sCiAgICAiYTJfYWdn
X2FuYWx5dGljIjogLTAuMDI0MzIyNjE0NzA5MjQ0MDU1LAogICAgImV2ZW5fYmFzaXNfZml0Ijog
ewogICAgICJhNCI6IDAuMjM4MDg0MzczODIxNTc4NjUsCiAgICAgImE2IjogLTEuNTA3Nzg1OTY2
NjU0MzUzMiwKICAgICAiYTgiOiA0Ljk0ODc4NTk1NjIxNTU0NywKICAgICAicm1zIjogMS4yNjM5
ODM2NjM2OTE0NzhlLTA3CiAgICB9LAogICAgInNtYWxsa19jb25maXJtYXRpb25fcmVsIjogMC4w
MDAxOTI5MDAwMDY5ODkxMjczNSwKICAgICJzcHVyaW91c19hM19pZl9rM19iYXNpcyI6IDAuMDI0
NzgyODQxODE5MzU4NDYzCiAgIH0sCiAgICJUIjogewogICAgIkQwIjogLTAuMDIwNTI4MjQ0NTk1
MzI4MzUsCiAgICAiUl9vdmVyX2s0X2F0X2siOiB7CiAgICAgIjAuMDAxOSI6IDAuMTA4MTgxMDIw
Nzk0OTc4OTYsCiAgICAgIjAuMDAzNiI6IDAuMDY5OTQ0NTY0MDk1OTMyMzYsCiAgICAgIjAuMDA2
NyI6IDAuMDY5OTE5NDcyNzMyODA4MDcsCiAgICAgIjAuMDEyNiI6IDAuMDY5ODUwOTQzOTk4MTk5
NzQKICAgIH0sCiAgICAiYTJfYWdnX2FuYWx5dGljIjogLTAuMDE4MzQ3NjYzMTYzOTQ3MDQ3LAog
ICAgImV2ZW5fYmFzaXNfZml0IjogewogICAgICJhNCI6IDAuMDY5NTQwNzM3NjcwMzM0MSwKICAg
ICAiYTYiOiAtMC4yNTM2Mjk3ODczODkyODMsCiAgICAgImE4IjogMC41OTM3OTU4NDUwMTQ1NzE1
LAogICAgICJybXMiOiA4LjQ4NzMzNTQ0MzExNzA1ZS0wOQogICAgfSwKICAgICJzbWFsbGtfY29u
ZmlybWF0aW9uX3JlbCI6IDAuMDAwMTE2NjM5MTc4NTEzNDU1NzMsCiAgICAic3B1cmlvdXNfYTNf
aWZfazNfYmFzaXMiOiAwLjAwNTEwNjM5Mzk1MDM4MDQyNwogICB9LAogICAiYTJfb3Zlcl9RVCI6
IC0wLjUyMTM3NzYwNTQ0ODI3MjYsCiAgICJyYXRpb19hMl9MX292ZXJfVCI6IDEuMzI1NjUxOTA5
NTU5NjcyCiAgfQogfSwKICJwdXJwb3NlIjogIlAyIHN0cnVjdHVyZSBkaWFnbm9zdGljICsgUFJP
UE9TRUQgYW1lbmRtZW50IFAyLUEgcXVhbnRpdGllcyAoTk9UIG9mIHJlY29yZCB1bnRpbCBhdXRo
b3JpemVkKSIKfQo=
<<<EMBED-END name=s2c1_p2_structure_diag.json>>>

### EMBED — chat Phase-3 consolidated checkpoint — `s2c1_phase3_checkpoint.json` (md5 48927b9aebce27615b8f18581fe98a4f, 6473 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_phase3_checkpoint.json md5=48927b9aebce27615b8f18581fe98a4f bytes=6473 enc=b64 quarantine=1>>>
ewogImNvbnRyb2xzIjogewogICJGX0FHR19LS19tYXhfcmVsIjogNi42NjEzMzgxNDc3NTA5Mzll
LTE2LAogICJGX0FHR19LS19wYXNzIjogdHJ1ZSwKICAiRl9BR0dfTF9wYXNzIjogZmFsc2UsCiAg
IkZfQUdHX1BJTl9wYXNzIjogdHJ1ZSwKICAiRl9DT05WX3Bhc3MiOiB0cnVlLAogICJGX0NPTlZf
d29yc3QiOiB7CiAgICJEMDNfUW1heDEwMF9yZWwiOiAyLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAg
ICJEMDNfbXUxMjhfcmVsIjogMS45OTg0MDE0NDQzMjUyODE4ZS0xNSwKICAgIkQwM194aV9kb3Vi
bGluZ19yZWwiOiAxLjg5NDA0MDQ4MDAxMDUxN2UtMTMsCiAgICJEMl9tdTEyOF9yZWwiOiAxLjA2
NTgxNDEwMzY0MDE1MDNlLTE0LAogICAiRDJfeGlfZG91YmxpbmdfcmVsIjogMi4wMjcyNjcyNDI5
NjU1MzU4ZS0xMwogIH0KIH0sCiAiZWxlY3Rpb25fRV9QMl8xIjogIihhKSBwb2xhcml6YXRpb24t
YXZlcmFnZWQgdHJhbnN2ZXJzZSBzaGVhciBjb25lIChhdXRob3ItY29uZmlybWVkKSIsCiAiZ2F0
ZSI6ICJHLVMyQzEiLAogImxlZyI6ICJjaGF0IiwKICJwZXJfc3Vic3RyYXRlIjogewogICJnZW04
X2N1YmljIjogewogICAiRDBfc3RhdGljX3NoaWZ0IjogLTAuMDQzNjc3MTQzOTI2OTc5NzQ1LAog
ICAiRl9BR0dfRElTUCI6IHsKICAgICJsb2NrZWRfcnVsZSI6IHsKICAgICAiRl9BR0dfQU5BTFlU
SUNfcGFzcyI6IGZhbHNlLAogICAgICJhMl9vZl9yZWNvcmQiOiAtMC4wNDAyOTAzMDM3MzQ5ODk3
OSwKICAgICAiYXJtIjogIkE1LWFnZyBJTlNUUlVNRU5ULUxJTUlURUQiCiAgICB9LAogICAgInBy
b3Bvc2VkX1AyQSI6IHsKICAgICAiQ0kiOiA4LjA1MTA4NDQyMzY4NzE5N2UtMTUsCiAgICAgImEy
X29mX3JlY29yZCI6IC0wLjAzOTcxMzk3Njc5MTI4ODEzLAogICAgICJhcm0iOiAiQTMtYWdnIERJ
U1BFUlNJVkUgKGdyYWluLXNjYWxlIGteMikiLAogICAgICJleGNlZWRzX3RhdV9hZ2ciOiB0cnVl
CiAgICB9CiAgIH0sCiAgICJhMl9MX292ZXJfYTJfVCI6IDEuMzE4NTAzNjU4NDE5NjgyLAogICAi
YTJfYWdnX2FuYWx5dGljX0QyIjogLTAuMDM5NzEzOTc2NzkxMjg4MTMsCiAgICJhMl9hZ2dfbG9j
a2VkX3J1bGVfYmFzaXMzX2ZpdCI6IC0wLjA0MDI5MDMwMzczNDk4OTc5LAogICAiYTJfb3Zlcl9R
X1QiOiAtMC41MjYwNTI2Mzg0MzM5NDU2LAogICAiYTNfYWdnIjogMC4wLAogICAiYTNfbm90ZSI6
ICJwcmUtcmVnaXN0ZXJlZCBrXjMgdGVybSBSRUZVVEVEIGJ5IHRoZSBtYWNoaW5lIChSL2teNCBm
bGF0IG92ZXIgZm91ciBkZWNhZGVzOyBldmVuIGJhc2lzIHJtcyAxLjhlLTA4KSIsCiAgICJhNF9h
Z2dfZXZlbl9iYXNpcyI6IDAuMTQ5MjU0MjU4MTA2ODE0MTQsCiAgICJhNl9hZ2dfZXZlbl9iYXNp
cyI6IC0wLjU0NjQ4MjUyNzU1ODM1NDksCiAgICJmaXRfdnNfYW5hbHl0aWNfcmVsIjogMC4wMTQ1
MTE5NDI0MDA3OTQ0NTMKICB9LAogICJnZW04X2hleCI6IHsKICAgIkQwX3N0YXRpY19zaGlmdCI6
IC0wLjAyODkxNzgwNzYwMzA3MTczNSwKICAgIkZfQUdHX0RJU1AiOiB7CiAgICAibG9ja2VkX3J1
bGUiOiB7CiAgICAgIkZfQUdHX0FOQUxZVElDX3Bhc3MiOiBmYWxzZSwKICAgICAiYTJfb2ZfcmVj
b3JkIjogLTAuMDI2MzE1NTYxMzI5NTI2NDI4LAogICAgICJhcm0iOiAiQTUtYWdnIElOU1RSVU1F
TlQtTElNSVRFRCIKICAgIH0sCiAgICAicHJvcG9zZWRfUDJBIjogewogICAgICJDSSI6IDUuMjU3
NDUyNzQ5MjU0NTEzZS0xNSwKICAgICAiYTJfb2ZfcmVjb3JkIjogLTAuMDI1OTMzNjkzNTg0Mjk0
MjEsCiAgICAgImFybSI6ICJBMy1hZ2cgRElTUEVSU0lWRSAoZ3JhaW4tc2NhbGUga14yKSIsCiAg
ICAgImV4Y2VlZHNfdGF1X2FnZyI6IHRydWUKICAgIH0KICAgfSwKICAgImEyX0xfb3Zlcl9hMl9U
IjogMS4zMjY3MjI5ODQ1MjQwNjI1LAogICAiYTJfYWdnX2FuYWx5dGljX0QyIjogLTAuMDI1OTMz
NjkzNTg0Mjk0MjEsCiAgICJhMl9hZ2dfbG9ja2VkX3J1bGVfYmFzaXMzX2ZpdCI6IC0wLjAyNjMx
NTU2MTMyOTUyNjQyOCwKICAgImEyX292ZXJfUV9UIjogLTAuNTE4NDYwODAwMDczNDgzNSwKICAg
ImEzX2FnZyI6IDAuMCwKICAgImEzX25vdGUiOiAicHJlLXJlZ2lzdGVyZWQga14zIHRlcm0gUkVG
VVRFRCBieSB0aGUgbWFjaGluZSAoUi9rXjQgZmxhdCBvdmVyIGZvdXIgZGVjYWRlczsgZXZlbiBi
YXNpcyBybXMgMS4yZS0wOCkiLAogICAiYTRfYWdnX2V2ZW5fYmFzaXMiOiAwLjA5ODk2NDE5NTEy
NDQ0ODA1LAogICAiYTZfYWdnX2V2ZW5fYmFzaXMiOiAtMC4zNjE1MzA0MDc5MDUwNDI3NiwKICAg
ImZpdF92c19hbmFseXRpY19yZWwiOiAwLjAxNDcyNDc3Mjc3NDQ5OTAxOAogIH0sCiAgInN0ZXBf
Y3ViaWMiOiB7CiAgICJEMF9zdGF0aWNfc2hpZnQiOiAtMC4wMzE1MTM0MjI0MzQzMzYyMywKICAg
IkZfQUdHX0RJU1AiOiB7CiAgICAibG9ja2VkX3J1bGUiOiB7CiAgICAgIkZfQUdHX0FOQUxZVElD
X3Bhc3MiOiBmYWxzZSwKICAgICAiYTJfb2ZfcmVjb3JkIjogLTAuMDI4OTQ5NDI5MDU1NTcyNzIs
CiAgICAgImFybSI6ICJBNS1hZ2cgSU5TVFJVTUVOVC1MSU1JVEVEIgogICAgfSwKICAgICJwcm9w
b3NlZF9QMkEiOiB7CiAgICAgIkNJIjogNS43ODUzMDgwMzc0MjExMTI0ZS0xNSwKICAgICAiYTJf
b2ZfcmVjb3JkIjogLTAuMDI4NTM3NDcxMTA3OTQ0NDIzLAogICAgICJhcm0iOiAiQTMtYWdnIERJ
U1BFUlNJVkUgKGdyYWluLXNjYWxlIGteMikiLAogICAgICJleGNlZWRzX3RhdV9hZ2ciOiB0cnVl
CiAgICB9CiAgIH0sCiAgICJhMl9MX292ZXJfYTJfVCI6IDEuMzIwMDM3MzE3NjI2MjE2NiwKICAg
ImEyX2FnZ19hbmFseXRpY19EMiI6IC0wLjAyODUzNzQ3MTEwNzk0NDQyMywKICAgImEyX2FnZ19s
b2NrZWRfcnVsZV9iYXNpczNfZml0IjogLTAuMDI4OTQ5NDI5MDU1NTcyNzIsCiAgICJhMl9vdmVy
X1FfVCI6IC0wLjUyNzcxMzA2NzkyMjUzLAogICAiYTNfYWdnIjogMC4wLAogICAiYTNfbm90ZSI6
ICJwcmUtcmVnaXN0ZXJlZCBrXjMgdGVybSBSRUZVVEVEIGJ5IHRoZSBtYWNoaW5lIChSL2teNCBm
bGF0IG92ZXIgZm91ciBkZWNhZGVzOyBldmVuIGJhc2lzIHJtcyAxLjNlLTA4KSIsCiAgICJhNF9h
Z2dfZXZlbl9iYXNpcyI6IDAuMTA2ODE3MjU5MjgyNzAwNzUsCiAgICJhNl9hZ2dfZXZlbl9iYXNp
cyI6IC0wLjM5MDQ4MzkzNTI3NTExNDksCiAgICJmaXRfdnNfYW5hbHl0aWNfcmVsIjogMC4wMTQ0
MzU2ODUxNDA3NzY3NTUKICB9LAogICJzdGVwX2hleCI6IHsKICAgIkQwX3N0YXRpY19zaGlmdCI6
IC0wLjAyMDUyODI0NDU5NTMyODM1LAogICAiRl9BR0dfRElTUCI6IHsKICAgICJsb2NrZWRfcnVs
ZSI6IHsKICAgICAiRl9BR0dfQU5BTFlUSUNfcGFzcyI6IGZhbHNlLAogICAgICJhMl9vZl9yZWNv
cmQiOiAtMC4wMTg2MTU2MTQwNDA5MDI2ODMsCiAgICAgImFybSI6ICJBNS1hZ2cgSU5TVFJVTUVO
VC1MSU1JVEVEIgogICAgfSwKICAgICJwcm9wb3NlZF9QMkEiOiB7CiAgICAgIkNJIjogMy43MTk1
NjE2NTE3MjM1MjVlLTE1LAogICAgICJhMl9vZl9yZWNvcmQiOiAtMC4wMTgzNDc2NjMxNjM5NDcw
NDcsCiAgICAgImFybSI6ICJBMy1hZ2cgRElTUEVSU0lWRSAoZ3JhaW4tc2NhbGUga14yKSIsCiAg
ICAgImV4Y2VlZHNfdGF1X2FnZyI6IHRydWUKICAgIH0KICAgfSwKICAgImEyX0xfb3Zlcl9hMl9U
IjogMS4zMjU2NTE5MDk1NTk2NzIsCiAgICJhMl9hZ2dfYW5hbHl0aWNfRDIiOiAtMC4wMTgzNDc2
NjMxNjM5NDcwNDcsCiAgICJhMl9hZ2dfbG9ja2VkX3J1bGVfYmFzaXMzX2ZpdCI6IC0wLjAxODYx
NTYxNDA0MDkwMjY4MywKICAgImEyX292ZXJfUV9UIjogLTAuNTIxMzc3NjA1NDQ4MjcyNiwKICAg
ImEzX2FnZyI6IDAuMCwKICAgImEzX25vdGUiOiAicHJlLXJlZ2lzdGVyZWQga14zIHRlcm0gUkVG
VVRFRCBieSB0aGUgbWFjaGluZSAoUi9rXjQgZmxhdCBvdmVyIGZvdXIgZGVjYWRlczsgZXZlbiBi
YXNpcyBybXMgOC41ZS0wOSkiLAogICAiYTRfYWdnX2V2ZW5fYmFzaXMiOiAwLjA2OTU0MDczNzY3
MDMzNDEsCiAgICJhNl9hZ2dfZXZlbl9iYXNpcyI6IC0wLjI1MzYyOTc4NzM4OTI4MywKICAgImZp
dF92c19hbmFseXRpY19yZWwiOiAwLjAxNDYwNDA4NzQyODUzNzM2CiAgfQogfSwKICJwaGFzZSI6
ICIzIC8gUHJvYmUgUDIgKGFnZ3JlZ2F0ZSBpbmhlcml0YW5jZSkiLAogInByb3ZlbmFuY2UiOiB7
CiAgImFkZGVuZHVtX1AyX21kNSI6ICIyZmVmZjQ0MmRmZDA4YTM3OTQ0M2Q4OTNiOGM3NzYxYiIs
CiAgImNoZWNrcG9pbnRzIjogewogICAicGhhc2UwX3BpbiI6ICIwMzI4YjU3MGFmNDZhODc4OTcw
NjUzYWQ4Nzc1ZjZkOSIsCiAgICJwaGFzZTFfbGFkZGVycyI6ICI2ZGE2MmZjYTY0NGQ1ZWE2YjFk
N2FiZTczMjliNWUyYyIsCiAgICJwaGFzZTJfZml0cyI6ICIwZThjYzA1ZTQ4NjhiOGRiMDg2NTY0
ZTI5N2NhYjZkNSIsCiAgICJzdHJ1Y3R1cmVfZGlhZyI6ICI2MGFkZDAwOWMyODJiOWQ2MDMwMjFi
YTBhZGJmYTFlMiIKICB9LAogICJpbnN0cnVtZW50X21kNSI6ICIwNWEzMjNjZjczODUxYTU2ZjU0
NTM5ZjM3YzAwY2IxZiIsCiAgInJlY292ZXJlZF9tYWNoaW5lcnkiOiAicG9seTFfZnVsbHByZWNf
Y2NsZWcucHkgYTU4NDgyZWYgKGJyYW5jaCBndmJrb2YgQCAyMzFiNTU1YSwgMjAvMjAgbWFuaWZl
c3QgT0spOyBpbnB1dCBwb2x5X3ZyaF9yZXN1bHRzLmpzb24gMjAwZTdhOGIiLAogICJyZXByb2R1
Y3Rpb24iOiAicmUtZXhlY3V0ZWQgU2VwdCAzIChwMl9yZXByby8pOiBhbGwgdGhyZWUgY2hlY2tw
b2ludHMgYnl0ZS1pZGVudGljYWwiCiB9LAogInN1bW1hcnkiOiB7CiAgIkZfQUdHX1VOSSI6IHsK
ICAgImEyTF9vdmVyX2EyVCI6IHsKICAgICJnZW04X2N1YmljIjogMS4zMTg1MDM2NTg0MTk2ODIs
CiAgICAiZ2VtOF9oZXgiOiAxLjMyNjcyMjk4NDUyNDA2MjUsCiAgICAic3RlcF9jdWJpYyI6IDEu
MzIwMDM3MzE3NjI2MjE2NiwKICAgICJzdGVwX2hleCI6IDEuMzI1NjUxOTA5NTU5NjcyCiAgIH0s
CiAgICJhMl9vdmVyX1FUX3NwcmVhZF9yZWwiOiAwLjAxNzY3NzIwNjEwODkzNTM5MwogIH0sCiAg
ImEyX2FnZ19hbmFseXRpY19ieV9zdWJzdHJhdGUiOiB7CiAgICJnZW04X2N1YmljIjogLTAuMDM5
NzEzOTc2NzkxMjg4MTMsCiAgICJnZW04X2hleCI6IC0wLjAyNTkzMzY5MzU4NDI5NDIxLAogICAi
c3RlcF9jdWJpYyI6IC0wLjAyODUzNzQ3MTEwNzk0NDQyMywKICAgInN0ZXBfaGV4IjogLTAuMDE4
MzQ3NjYzMTYzOTQ3MDQ3CiAgfSwKICAiYTRfYWdnX2J5X3N1YnN0cmF0ZSI6IHsKICAgImdlbThf
Y3ViaWMiOiAwLjE0OTI1NDI1ODEwNjgxNDE0LAogICAiZ2VtOF9oZXgiOiAwLjA5ODk2NDE5NTEy
NDQ0ODA1LAogICAic3RlcF9jdWJpYyI6IDAuMTA2ODE3MjU5MjgyNzAwNzUsCiAgICJzdGVwX2hl
eCI6IDAuMDY5NTQwNzM3NjcwMzM0MQogIH0sCiAgImFybV91bmRlcl9wcm9wb3NlZF9QMkEiOiB7
CiAgICJnZW04X2N1YmljIjogIkEzLWFnZyIsCiAgICJnZW04X2hleCI6ICJBMy1hZ2ciLAogICAi
c3RlcF9jdWJpYyI6ICJBMy1hZ2ciLAogICAic3RlcF9oZXgiOiAiQTMtYWdnIgogIH0sCiAgImhv
bmVzdHkiOiB7CiAgICJILVMyQy0xMCI6ICJwcmUtcmVnaXN0ZXJlZCBub24tYW5hbHl0aWMga14z
IHRlcm0gcmVmdXRlZCAoZGVyaXZhdGlvbiBlcnJvciwgY29ycmVjdGVkOiBhbmFseXRpYyBpbiBr
X01eMiBmb3IgZXZlbiBGMCkiLAogICAiSC1TMkMtMTEiOiAid2luZG93LXN0YWJpbGl0eSBDSSB1
bmRlci1lc3RpbWF0ZWQgZml0LWJhc2lzIGJpYXMiLAogICAiSC1TMkMtMTIiOiAiVDEgbnVtZXJp
Yy1wYXR0ZXJuIGNvbGxpc2lvbjogb25lIGJhcmUgbnVtZXJpYyBwYXR0ZXJuIG9mIHRoZSBmcm96
ZW4gbGlzdCBtYXRjaGVkIGluc2lkZSBhIG1hY2hpbmUtZXBzaWxvbiBGLUNPTlYgZmxvYXQgaW4g
dGhlIHBoYXNlLTIgY2hlY2twb2ludDsgY2xhc3NpZmllZCBhcyBmb3JtYXR0aW5nIGNvbGxpc2lv
biwgbG9nZ2VkLCBub3QgcmVmb3JtYXR0ZWQ7IGNvbnRleHR1YWwtcGF0dGVybiBhbWVuZG1lbnQg
cHJvcG9zZWQgZm9yIHRoZSBuZXh0IGxvY2sgY3ljbGUiCiAgfSwKICAibWVjaGFuaWNhbF9hcm1f
bG9ja2VkX3J1bGUiOiB7CiAgICJnZW04X2N1YmljIjogIkE1LWFnZyBJTlNUUlVNRU5ULUxJTUlU
RUQiLAogICAiZ2VtOF9oZXgiOiAiQTUtYWdnIElOU1RSVU1FTlQtTElNSVRFRCIsCiAgICJzdGVw
X2N1YmljIjogIkE1LWFnZyBJTlNUUlVNRU5ULUxJTUlURUQiLAogICAic3RlcF9oZXgiOiAiQTUt
YWdnIElOU1RSVU1FTlQtTElNSVRFRCIKICB9LAogICJzdGF0dXMiOiAiUDIgY2hhdCBsZWcgQ09N
UExFVEUgYW5kIHJlcHJvZHVjZWQ7IEYtQUdHLURJU1AgZXZhbHVhdGVkIHVuZGVyIGJvdGggdGhl
IGxvY2tlZCBydWxlIChBNS1hZ2cpIGFuZCB0aGUgcHJvcG9zZWQgUDItQSAoQTMtYWdnKTsgUDIt
QSBhd2FpdHMgYXV0aG9yIGRlY2lzaW9uOyBQMiBDQyBsZWcgKHR3by1sZWcpIG5vdCB5ZXQgZGlz
cGF0Y2hlZDsgbm8gd2luZG93IGFjdGlvbiIKIH0KfQo=
<<<EMBED-END name=s2c1_phase3_checkpoint.json>>>

### EMBED — chat P2-A evaluation — `s2c1_phase3_P2A_evaluation.json` (md5 56b17d9356a60c4fb2c7d69ad19a6198, 2795 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_phase3_P2A_evaluation.json md5=56b17d9356a60c4fb2c7d69ad19a6198 bytes=2795 enc=b64 quarantine=1>>>
ewogImFkZGVuZHVtX1AyQV9tZDUiOiAiNzFiNGM3MDEwZTQ4NjAxZTA3ZjY0NThjNzExZGZiNGEi
LAogImFkZGVuZHVtX1AyX21kNSI6ICIyZmVmZjQ0MmRmZDA4YTM3OTQ0M2Q4OTNiOGM3NzYxYiIs
CiAiZ2F0ZSI6ICJHLVMyQzEiLAogImxlZyI6ICJjaGF0IiwKICJtZWNoYW5pY2FsX2FybV9QMkFf
YWxsIjogewogICJnZW04X2N1YmljIjogIkEzLWFnZyBESVNQRVJTSVZFIChncmFpbi1zY2FsZSBr
XjIpIiwKICAiZ2VtOF9oZXgiOiAiQTMtYWdnIERJU1BFUlNJVkUgKGdyYWluLXNjYWxlIGteMiki
LAogICJzdGVwX2N1YmljIjogIkEzLWFnZyBESVNQRVJTSVZFIChncmFpbi1zY2FsZSBrXjIpIiwK
ICAic3RlcF9oZXgiOiAiQTMtYWdnIERJU1BFUlNJVkUgKGdyYWluLXNjYWxlIGteMikiCiB9LAog
InBlcl9zdWJzdHJhdGUiOiB7CiAgImdlbThfY3ViaWMiOiB7CiAgICJDSV9xdWFkcmF0dXJlIjog
NC4xMTgxMzQwOTE4NTMxNDQ1ZS0xNSwKICAgIkZfQUdHX0RJU1BfcGFzcyI6IHRydWUsCiAgICJG
X0FHR19LS19wYXNzIjogdHJ1ZSwKICAgIkZfQUdHX0xfcGFzcyI6IHRydWUsCiAgICJGX0FHR19Q
SU5fcGFzcyI6IHRydWUsCiAgICJGX0NPTlZfcGFzcyI6IHRydWUsCiAgICJhMl9MIjogLTAuMDUy
MzYzMDIzNjg5NzA3NzUsCiAgICJhMl9hZ2dfb2ZfcmVjb3JkIjogLTAuMDM5NzEzOTc2NzkxMjg4
MTMsCiAgICJhMyI6IDAuMCwKICAgImE0X2FnZyI6IDAuMTQ5MjU0MjU4MTA2ODE0MTQsCiAgICJh
NiI6IC0wLjU0NjQ4MjUyNzU1ODM1NDksCiAgICJldmVuX2Jhc2lzX3JtcyI6IDEuODQ2NTI4MjYx
NDY4NTMyNmUtMDgsCiAgICJtZWNoYW5pY2FsX2FybV9QMkEiOiAiQTMtYWdnIERJU1BFUlNJVkUg
KGdyYWluLXNjYWxlIGteMikiLAogICAic21hbGxrX2NvbmZpcm1hdGlvbl9yZWwiOiAwLjAwMDEx
NjEzMTY2OTgzNjU5NDQKICB9LAogICJnZW04X2hleCI6IHsKICAgIkNJX3F1YWRyYXR1cmUiOiAx
LjU0NjE0MDI2NjM0NzAyODJlLTE1LAogICAiRl9BR0dfRElTUF9wYXNzIjogdHJ1ZSwKICAgIkZf
QUdHX0tLX3Bhc3MiOiB0cnVlLAogICAiRl9BR0dfTF9wYXNzIjogdHJ1ZSwKICAgIkZfQUdHX1BJ
Tl9wYXNzIjogdHJ1ZSwKICAgIkZfQ09OVl9wYXNzIjogdHJ1ZSwKICAgImEyX0wiOiAtMC4wMzQ0
MDY4MjczNTE4ODczNSwKICAgImEyX2FnZ19vZl9yZWNvcmQiOiAtMC4wMjU5MzM2OTM1ODQyOTQy
MSwKICAgImEzIjogMC4wLAogICAiYTRfYWdnIjogMC4wOTg5NjQxOTUxMjQ0NDgwNSwKICAgImE2
IjogLTAuMzYxNTMwNDA3OTA1MDQyNzYsCiAgICJldmVuX2Jhc2lzX3JtcyI6IDEuMjEwODAyMTQ3
ODQ5NzY0OWUtMDgsCiAgICJtZWNoYW5pY2FsX2FybV9QMkEiOiAiQTMtYWdnIERJU1BFUlNJVkUg
KGdyYWluLXNjYWxlIGteMikiLAogICAic21hbGxrX2NvbmZpcm1hdGlvbl9yZWwiOiAwLjAwMDEx
Nzg3MzMzMTcyMzUyODEKICB9LAogICJzdGVwX2N1YmljIjogewogICAiQ0lfcXVhZHJhdHVyZSI6
IDUuNzg1MzA4MDM3NDIxMTEyNGUtMTUsCiAgICJGX0FHR19ESVNQX3Bhc3MiOiB0cnVlLAogICAi
Rl9BR0dfS0tfcGFzcyI6IHRydWUsCiAgICJGX0FHR19MX3Bhc3MiOiB0cnVlLAogICAiRl9BR0df
UElOX3Bhc3MiOiB0cnVlLAogICAiRl9DT05WX3Bhc3MiOiB0cnVlLAogICAiYTJfTCI6IC0wLjAz
NzY3MDUyNjgxMzE2NjYxLAogICAiYTJfYWdnX29mX3JlY29yZCI6IC0wLjAyODUzNzQ3MTEwNzk0
NDQyMywKICAgImEzIjogMC4wLAogICAiYTRfYWdnIjogMC4xMDY4MTcyNTkyODI3MDA3NSwKICAg
ImE2IjogLTAuMzkwNDgzOTM1Mjc1MTE0OSwKICAgImV2ZW5fYmFzaXNfcm1zIjogMS4zMTcwMjY0
OTYzMjgyMDFlLTA4LAogICAibWVjaGFuaWNhbF9hcm1fUDJBIjogIkEzLWFnZyBESVNQRVJTSVZF
IChncmFpbi1zY2FsZSBrXjIpIiwKICAgInNtYWxsa19jb25maXJtYXRpb25fcmVsIjogMC4wMDAx
MTUzMTQyNDM0OTQ1MzUzNAogIH0sCiAgInN0ZXBfaGV4IjogewogICAiQ0lfcXVhZHJhdHVyZSI6
IDEuMDc5NjA5ODk4OTEyMDg1NWUtMTYsCiAgICJGX0FHR19ESVNQX3Bhc3MiOiB0cnVlLAogICAi
Rl9BR0dfS0tfcGFzcyI6IHRydWUsCiAgICJGX0FHR19MX3Bhc3MiOiB0cnVlLAogICAiRl9BR0df
UElOX3Bhc3MiOiB0cnVlLAogICAiRl9DT05WX3Bhc3MiOiB0cnVlLAogICAiYTJfTCI6IC0wLjAy
NDMyMjYxNDcwOTI0NDA1NSwKICAgImEyX2FnZ19vZl9yZWNvcmQiOiAtMC4wMTgzNDc2NjMxNjM5
NDcwNDcsCiAgICJhMyI6IDAuMCwKICAgImE0X2FnZyI6IDAuMDY5NTQwNzM3NjcwMzM0MSwKICAg
ImE2IjogLTAuMjUzNjI5Nzg3Mzg5MjgzLAogICAiZXZlbl9iYXNpc19ybXMiOiA4LjQ4NzMzNTQ0
MzExNzA1ZS0wOSwKICAgIm1lY2hhbmljYWxfYXJtX1AyQSI6ICJBMy1hZ2cgRElTUEVSU0lWRSAo
Z3JhaW4tc2NhbGUga14yKSIsCiAgICJzbWFsbGtfY29uZmlybWF0aW9uX3JlbCI6IDAuMDAwMTE2
NjM5MTc4NTEzNDU1NzMKICB9CiB9LAogInBoYXNlIjogIjMgLyBQMiBcdTIwMTQgUDItQSBldmFs
dWF0aW9uIiwKICJzb3VyY2VfbWQ1IjogewogICJwaGFzZTJfZml0cyI6ICIwZThjYzA1ZTQ4Njhi
OGRiMDg2NTY0ZTI5N2NhYjZkNSIsCiAgInBoYXNlM19jaGVja3BvaW50IjogIjQ4OTI3YjlhZWJj
ZTI3NjE1YjhmMTg1ODFmZTk4YTRmIiwKICAic3RydWN0dXJlX2RpYWciOiAiNjBhZGQwMDljMjgy
YjlkNjAzMDIxYmEwYWRiZmExZTIiCiB9LAogInN0YXR1cyI6ICJjaGF0IGxlZyBQMiBtZWNoYW5p
Y2FsIGFybSB1bmRlciBQMi1BOyBQMiBDQyBsZWcgcGVuZGluZzsgbm8gd2luZG93IGFjdGlvbiIK
fQo=
<<<EMBED-END name=s2c1_phase3_P2A_evaluation.json>>>

### EMBED — chat P2 report — `G_S2C1_P2_AGGREGATE_REPORT.md` (md5 b56fbe5636cca4cdcde02900ac73469b, 5493 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=G_S2C1_P2_AGGREGATE_REPORT.md md5=b56fbe5636cca4cdcde02900ac73469b bytes=5493 enc=b64 quarantine=1>>>
IyBHLVMyQzEg4oCUIFBIQVNFIDMgLyBQUk9CRSBQMiAoQUdHUkVHQVRFKSDigJQgUkVQT1JUIChj
aGF0IGxlZywgU2VwdGVtYmVyIDMsIDIwMjYpCgoqKkxvY2s6KiogQWRkZW5kdW0gUDIgKioyZmVm
ZjQ0MioqIChFLVAyLTEgKGEpIHZlcmJhdGltOyBvcGVyYXRpb25hbCBkZWZpbml0aW9uOyBmYWxz
aWZpZXJzOyBmaXQtYmFzaXMgcnVsZSDigJQgbG9ja2VkIEJFRk9SRSB0aGUgaW5zdHJ1bWVudCB3
YXMgd3JpdHRlbikuIE1hY2hpbmVyeTogdGhlIHJlY292ZXJlZCBHLVBPTFkxIGluc3RydW1lbnQg
KGd2YmtvZiBAIDIzMWI1NTVhLCBtYW5pZmVzdC12ZXJpZmllZCkgaW1wb3J0ZWQgYXMgYSBtb2R1
bGU7IGlucHV0IGBwb2x5X3ZyaF9yZXN1bHRzLmpzb25gIG1kNSAyMDBlN2E4YiB2ZXJpZmllZCBh
dCBydW4uIEluc3RydW1lbnQgYGdfczJjMV9wMl9hZ2dyZWdhdGUucHlgOyBjaGVja3BvaW50cyBw
Ml9waGFzZTBfcGluICoqMDMyOGI1NzAqKiwgcDJfcGhhc2UxX2xhZGRlcnMgKio2ZGE2MmZjYSoq
LCBwMl9waGFzZTJfZml0cyAqKjBlOGNjMDVlKio7IHN0cnVjdHVyZSBkaWFnbm9zdGljICoqNjBh
ZGQwMDkqKi4gVDEgemVybyBoaXRzIHRocm91Z2hvdXQuCgojIyBDb250cm9scyDigJQgYWxsIGV4
YWN0Ci0gKipGLUFHRy1QSU4gUEFTUzoqKiB0aGUgYmFua2VkIFFfVF5hIHF1YXJ0ZXQgcmVwcm9k
dWNlZCBkaWdpdC1mb3ItZGlnaXQgKHJlbGF0aXZlIDAgdG8gMi4yw5cxMOKBu8K54oG2KTsgVl9U
LCBWX0wgdG8gdGhlIHByaW50ZWQgZGlnaXRzLgotICoqRi1BR0ctS0sgUEFTUzoqKiB0aGUgSW0t
cGFydCB0aWUtaW4gzrFfVChrKSA9IM6jX00gayBrX03CsyBOX00vMiDCtyBGX00oa19NLGspIHJl
cHJvZHVjZXMgdGhlIHJlY292ZXJlZCBgYWxwaGFfZmluaXRlYCBvbiB0aGUgRy1QT0xZMSBncmlk
IHRvIOKJpCA2LjfDlzEw4oG7wrnigbYg4oCUIHNhbWUga2VybmVscywgc2FtZSBtb2RlIG5vcm1h
bGl6YXRpb247IHRoZSByZWFsIHBhcnQgY29tcHV0ZWQgaGVyZSBpcyBpdHMgZXhhY3QgSGlsYmVy
dCBwYXJ0bmVyLgotICoqRi1DT05WIFBBU1M6Kiogzp4gcXVhZHJhdHVyZSBkb3VibGluZyDiiaQg
MsOXMTDigbvCucKzIG9uIEQyIGFuZCBvbiBEKDAuMyk7IM68LW5vZGVzIDY04oaSMTI4IOKJpCAy
w5cxMOKBu8K54oG0OyBRX21heCA1MOKGkjEwMCDiiaQgMTDigbvCucKyOyBEKDApIGNsb3NlZCBm
b3JtIHZzIEQoMTDigbvigbQpOiBpZGVudGljYWwgdG8gNyBkaWdpdHMuCgojIyBSZXN1bHQg4oCU
IHRoZSBzaGVhciBjb25lIGluIHRoZSBhZ2dyZWdhdGUgaXMgZGlzcGVyc2l2ZSBhdCBSYXlsZWln
aCBvcmRlciAoRS1QMi0xIChhKSkKRChrKSA9IM6UY19UL2NfVChrKSA9ICgxL8+AKc6jX00gTl9N
wrdQVuKIq3HigbRGX00vKGtfTcKy4oiSccKyKWRxLiBTdGF0aWMgc2Vjb25kLW9yZGVyIHJlbm9y
bWFsaXphdGlvbiBEKDApID0g4oiSMi4wNSAvIOKIkjIuODkgLyDiiJIzLjE1IC8g4oiSNC4zNyDD
lzEw4oG7wrIgKHN0ZXBfaGV4IC8gZ2VtOF9oZXggLyBzdGVwX2N1YmljIC8gZ2VtOF9jdWJpYykg
4oCUIHRoZSBCb3JuIHZlbG9jaXR5IHNoaWZ0IGJlbG93IFZvaWd0LCBhcyBpdCBtdXN0IGJlLgpE
aXNwZXJzaW9uIGNvZWZmaWNpZW50cyAoayBpbiB1bml0cyAxL2FfZyksICoqZXhhY3QgYW5hbHl0
aWMga8KyIGNvZWZmaWNpZW50LCBxdWFkcmF0dXJlLWNvbnZlcmdlZCB0byAxMOKBu8K5wrMgYW5k
IGNvbmZpcm1lZCBieSB0aGUgc21hbGwtayBsaW1pdCBvZiB0aGUgbGFkZGVyOioqCnwgc3Vic3Ry
YXRlIHwgYeKCgl5hZ2cgKFQpIHwgYeKChF5hZ2cgKGV2ZW4tYmFzaXMpIHwgYeKChiB8IGHigoJe
YWdnLEwgKGNvbnRyb2wpIHwgYeKCgi9RX1ReYSB8CnwtLS18LS0tfC0tLXwtLS18LS0tfC0tLXwK
fCBzdGVwX2hleCB8IOKIkjEuODM0NzY2w5cxMOKBu8KyIHwgKzYuOTU0w5cxMOKBu8KyIHwg4oiS
MC4yNTQgfCDiiJIyLjQzMjI2McOXMTDigbvCsiB8IOKIkjAuNTIxNCB8CnwgZ2VtOF9oZXggfCDi
iJIyLjU5MzM2OcOXMTDigbvCsiB8ICs5Ljg5NsOXMTDigbvCsiB8IOKIkjAuMzYyIHwg4oiSMy40
NDA2ODPDlzEw4oG7wrIgfCDiiJIwLjUxODUgfAp8IHN0ZXBfY3ViaWMgfCDiiJIyLjg1Mzc0N8OX
MTDigbvCsiB8ICsxLjA2OMOXMTDigbvCuSB8IOKIkjAuMzkwIHwg4oiSMy43NjcwNTPDlzEw4oG7
wrIgfCDiiJIwLjUyNzcgfAp8IGdlbThfY3ViaWMgfCDiiJIzLjk3MTM5OMOXMTDigbvCsiB8ICsx
LjQ5M8OXMTDigbvCuSB8IOKIkjAuNTQ2IHwg4oiSNS4yMzYzMDLDlzEw4oG7wrIgfCDiiJIwLjUy
NjEgfApUd28gbmV3IFIyLWNsYXNzIG5lYXItdW5pdmVyc2FsaXRpZXMgYWNyb3NzIHRoZSBxdWFy
dGV0IChyZXBvcnQtb25seSwgRi1BR0ctVU5JKTogYeKCgl5hZ2cvUV9UXmEgPSDiiJIwLjUyIMKx
IDAuOSUgYW5kIGHigoJeYWdnLEwvYeKCgl5hZ2csVCA9IDEuMzIzIMKxIDAuMyUuIEYtQUdHLUwg
UEFTUyAoTCBjaGFubmVsIG5vbnplcm8sIGFuYWx5dGljLWNvbnRyb2xsZWQpLgoKIyMgVGhlIGxv
Y2tlZCBydWxlJ3MgdmVyZGljdCwgYW5kIHdoeSBpdCBpcyBBNS1hZ2cKVGhlIFAyIGFkZGVuZHVt
IHByZS1yZWdpc3RlcmVkIGEgbm9uLWFuYWx5dGljICoqa8KzIHRlcm0qKiBhbmQgbWFkZSB0aGUg
My10ZXJtIGJhc2lzIHtrwrIsa8KzLGvigbR9IHRoZSBiYXNpcyBvZiByZWNvcmQgd2hlbiB0aGUg
YmFzZXMgZGlzYWdyZWUsIHdpdGggdGhlIGZpdHRlZCBrwrIgY29lZmZpY2llbnQgcmVxdWlyZWQg
dG8gbWF0Y2ggdGhlIGluZGVwZW5kZW50IGFuYWx5dGljIEQyIHdpdGhpbiBDSSAoRi1BR0ctQU5B
TFlUSUMpLiBUaGUgYmFzZXMgZGlzYWdyZWVkIChieSBjb25zdHJ1Y3Rpb24gb2YgdGhlIGFsaWFz
aW5nKTsgdGhlIDMtdGVybSBh4oKCIG1pc3NlcyB0aGUgYW5hbHl0aWMgRDIgYnkgMS41JSAoVCkg
YW5kIDXigJM2JSAoTCksIG91dHNpZGUgQ0kg4oeSICoqbWVjaGFuaWNhbCBhcm0gQTUtYWdnIElO
U1RSVU1FTlQtTElNSVRFRCBmb3IgYWxsIGZvdXIgc3Vic3RyYXRlcy4qKgpNYWNoaW5lIGRpYWdu
b3NpczogUihrKSA9IM6UKGspIOKIkiBEMsK3a8KyIHNpdHMgYXQgKiorMC4wNjk1wrdr4oG0IG92
ZXIgZm91ciBkZWNhZGVzKiogKFIva+KBtCBmbGF0IGZyb20gayA9IDAuMDAzNiB0byAwLjAyNDsg
Ui9rwrMg4oaSIDA7IFIvKGvigbQgbG4gaykgbm90IGNvbnN0YW50KTsgYSBwdXJlIGV2ZW4gYmFz
aXMge2vigbQsa+KBtixr4oG4fSBmaXRzIFIgdG8gcm1zIDguNcOXMTDigbvigbkgKHRoZSBxdWFk
IGZsb29yKS4gKipUaGUgYWdncmVnYXRlIGRpc3BlcnNpb24gaXMgYW5hbHl0aWMgaW4ga8KyIOKA
lCBubyBrwrMsIG5vIGvigbQgbG9nIGsgYXQgdGhpcyBvcmRlci4qKiBUaGUgcHJlLXJlZ2lzdGVy
ZWQga8KzIHRlcm0gd2FzIGEgZGVyaXZhdGlvbiBlcnJvciAoY29ycmVjdGVkOiBmb3IgRuKCgCBl
dmVuIGluIHEgdGhlIHBvbGUtcmVnaW9uIGV4cGFuc2lvbiBpcyBhbmFseXRpYyBpbiBrX03Csiks
IHJlZnV0ZWQgYnkgdGhlIG1hY2hpbmUg4oCUICoqSC1TMkMtMTAqKi4gVGhlICJh4oKDIiBvZiB0
aGUgMy10ZXJtIGZpdCAoKzXDlzEw4oG7wrMpIGlzIGFsaWFzaW5nIG9mIGHigoY7IHRoZSBlbGVj
dGVkIDItdGVybSBiYXNpcyBpcyBiaWFzZWQgMS45JSB0aGUgb3RoZXIgd2F5IGJ5IHRoZSBzYW1l
IGvigbYgdGVybSBvdmVyIHRoZSB3aW5kb3cgKGHigoZr4oG2L2HigoJrwrIg4omIIDExJSBhdCBr
ID0gMC4zKS4gVGhlIHdpbmRvdy1zdGFiaWxpdHkgQ0kgdW5kZXItZXN0aW1hdGVkIHRoaXMgYmFz
aXMgYmlhcyDigJQgKipILVMyQy0xMSoqLgoKIyMgUHJvcG9zZWQgQW1lbmRtZW50IFAyLUEgKGF1
dGhvcidzIGNhbGw7IE5PVCBhcHBsaWVkKQph4oKCXmFnZyBvZiByZWNvcmQgPSB0aGUgYW5hbHl0
aWMgc2Vjb25kLW9yZGVyIGNvZWZmaWNpZW50IEQyIChjbG9zZWQgZm9ybSBvbiB0aGUgc2FtZSDO
ni/OpiBrZXJuZWxzOyBSMS1tYWNoaW5lKSwgd2l0aCB0aGUgbGFkZGVyIGFzIGNvbmZpcm1hdGlv
biAozpQva8KyIOKGkiBEMiBpbiB0aGUgc21hbGwtayBsaW1pdDsgZXZlbi1iYXNpcyByZW1haW5k
ZXIgcm1zIOKJpCAxMOKBu+KBuCk7IGHigoMg4omhIDAgKHJlZnV0ZWQpOyBh4oKEXmFnZyA9IHRo
ZSBldmVuLWJhc2lzIGvigbQgY29lZmZpY2llbnQuIFVuZGVyIFAyLUE6ICoqQTMtYWdnIERJU1BF
UlNJVkUgKGdyYWluIHNjYWxlKSoqIGZvciBhbGwgZm91ciBzdWJzdHJhdGVzLCB8YeKCgl5hZ2d8
ID0gMS444oCTNC4ww5cxMOKBu8KyIOKJqyDPhF9hZ2cuIFRoZSBsb2NrZWQgcnVsZSBpcyBub3Qg
ZWRpdGVkOyBQMi1BIGlzIGEgcHJvcG9zYWwgaW4gdGhlIGhvbmVzdHkgcmVjb3JkLgoKIyMgQ29u
c2VxdWVuY2UgYW5kIG5vbi1jbGFpbXMKUEYtUzIgaW5wdXQgbm93IGNvbXBsZXRlIGluIGtpbmQ6
IGxhdHRpY2Utc2NhbGUgYeKCgiAoUDE6IOKIkjEuMjgv4oiSMS45OcOXMTDigbvCsiBhdCBhKikg
YW5kIGdyYWluLXNjYWxlIGHigoJeYWdnIChQMjog4oiSMS444oCm4oiSNC4ww5cxMOKBu8KyIGF0
IGFfZyksIGJvdGggbmVnYXRpdmUgKG5vcm1hbCBkaXNwZXJzaW9uKSwgYm90aCBPKDEw4oG7wrIp
LiBXX+KIquKAsiBpcyBhIGZvbGQgYWN0aW9uIGFmdGVyIHRoZSBDQyBsZWcgYW5kIHRoZSBhdXRo
b3IncyB3b3JkOyBub3RoaW5nIGhlcmUgdG91Y2hlcyBXX+KIqi4gTm8gb2JzZXJ2YWJsZSwgbm8g
YnJpZGdlLCBubyDOvF9uLiBSMS1tYWNoaW5lIGZvciBldmVyeSBudW1iZXI7IFIyIGZvciB0aGUg
YWdncmVnYXRlIHJlYWRpbmcgY29uZGl0aW9uYWwgb24gRy1QT0xZMSdzIEUzIGVsZWN0aW9ucyBh
bmQgQm9ybi9TT0Egb3JkZXIuIFRoZSAzLUQga2luZW1hdGljIHBvaW50IChhIHByb3BhZ2F0aW5n
IHBsYW5lIHdhdmUncyBzdHJhaW4gY2FycmllcyBoZWxpY2l0eSAwL8KxMSwgbmV2ZXIgcHVyZSDC
sTIpIHN0YW5kcyBhcyBkaXNjbG9zZWQgaW4gdGhlIHN0YWdpbmcgbm90ZSBhbmQgbm93IHJpZGVz
IHdpdGggRS1QMi0xIChhKS4KCiMjIFQxIHNjYW4gcmVjb3JkCkFsbCBQMiBhcnRpZmFjdHMgc2Nh
bm5lZCBhZ2FpbnN0IHRoZSBmcm96ZW4gbGlzdCA4Y2Q4OWI5YTogb25lIGhpdCwgYHMyYzFfcDJf
cGhhc2UyX2ZpdHMuanNvbmAgbGluZSAyODkg4oCUIHRoZSBiYXJlIG51bWVyaWMgcGF0dGVybiBg
NWUtMTZgIG1hdGNoZWQgaW5zaWRlIHRoZSBGLUNPTlYgdmFsdWUgYEQwM19RbWF4MTAwX3JlbCA9
IDEuMTEwMjIzMDI0NjI1MTU2NWUtMTZgIChtYWNoaW5lIGVwc2lsb24pLiBDbGFzc2lmaWVkIGFz
IHRoZSBudW1lcmljLWZvcm1hdHRpbmcgY29sbGlzaW9uIHByZWRpY3RlZCBhdCBQaGFzZSAwIChI
LVMyQy0zKTsgbG9nZ2VkIGFzICoqSC1TMkMtMTIqKjsgdGhlIGNoZWNrcG9pbnQgaXMgbm90IHJl
Zm9ybWF0dGVkIGFuZCB0aGUgZnJvemVuIGxpc3QgaXMgbm90IGVkaXRlZC4gVGhlIGNvbnRleHR1
YWwtcGF0dGVybiBhbWVuZG1lbnQgb2YgdGhlIFQxIGxpc3QgcmVtYWlucyBQUk9QT1NFRCBmb3Ig
dGhlIG5leHQgbG9jayBjeWNsZS4K
<<<EMBED-END name=G_S2C1_P2_AGGREGATE_REPORT.md>>>

### EMBED — chat Phase-3 report — `G_S2C1_PHASE3_REPORT.md` (md5 41c608891e53eda1d96d1ad4c1128171, 4898 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=G_S2C1_PHASE3_REPORT.md md5=41c608891e53eda1d96d1ad4c1128171 bytes=4898 enc=b64 quarantine=1>>>
IyBHLVMyQzEgKEdhdGUgRy1TMi1PTi1DT05FKSDigJQgUEhBU0UgMyBSRVBPUlQ6IFByb2JlIFAy
LCBBZ2dyZWdhdGUgSW5oZXJpdGFuY2UgKGNoYXQgbGVnLCBTZXB0ZW1iZXIgMywgMjAyNikKCioq
QXV0aG9yaXphdGlvbiBjaGFpbjoqKiBFLVAyLTEgKGEpIGVsZWN0ZWQgYW5kIGNvbmZpcm1lZDsg
QWRkZW5kdW0gUDIgKioyZmVmZjQ0MioqIGxvY2tlZCBiZWZvcmUgdGhlIGluc3RydW1lbnQgZXhp
c3RlZDsgUDIgZXhlY3V0ZWQgdW5kZXIgaXQgKGNoZWNrcG9pbnRzIDAzMjhiNTcwIC8gNmRhNjJm
Y2EgLyAwZThjYzA1ZTsgc3RydWN0dXJlIGRpYWdub3N0aWMgNjBhZGQwMDk7IGluc3RydW1lbnQg
MDVhMzIzY2YpOyAqKnJlLWV4ZWN1dGVkIHRvZGF5OiBhbGwgdGhyZWUgY2hlY2twb2ludHMgYnl0
ZS1pZGVudGljYWwqKiDigJQgdGhlIFAyIHJlc3VsdCBpcyBhIGRldGVybWluaXN0aWMgZnVuY3Rp
b24gb2YgdGhlIGxvY2tlZCBpbnN0cnVtZW50LiBDb25zb2xpZGF0ZWQgUGhhc2UtMyBjaGVja3Bv
aW50OiBgczJjMV9waGFzZTNfY2hlY2twb2ludC5qc29uYCAoaGFzaCBpbiB0aGUgbWFuaWZlc3Qg
YmVsb3cpLiBNYWNoaW5lcnk6IHRoZSByZWNvdmVyZWQgRy1QT0xZMSBpbnN0cnVtZW50IChndmJr
b2YgQCAyMzFiNTU1YSwgbWFuaWZlc3QtdmVyaWZpZWQpLCBpbnB1dCAyMDBlN2E4YiB2ZXJpZmll
ZCBhdCBldmVyeSBydW4uCgojIyBXaGF0IHdhcyBjb21wdXRlZApSZSDOo19UIGF0IHNlY29uZCAo
Qm9ybi9TT0EpIG9yZGVyIOKAlCB0aGUgS3JhbWVyc+KAk0tyb25pZyBwYXJ0bmVyIG9mIHRoZSBi
YW5rZWQgUmF5bGVpZ2ggYXR0ZW51YXRpb24g4oCUIG9uIHRoZSBpZGVudGljYWwgzp4vzqZfVE0g
a2VybmVscyBhbmQgbW9kZSBub3JtYWxpemF0aW9uOiBEKGspID0gzpRjX1QvY19UKGspID0gKDEv
z4ApzqNfTSBOX03Ct1BW4oirceKBtEZfTShxLGspLyhrX03CsuKIknHCsilkcSwgYnkgQ2F1Y2h5
LXdlaWdodCBxdWFkcmF0dXJlIHBsdXMgcmVndWxhciB0YWlsLCBmb3IgdGhlIHBvbGFyaXphdGlv
bi1hdmVyYWdlZCBzaGVhciBjb25lIChFLVAyLTEgKGEpKSBhbmQgdGhlIEwgY2hhbm5lbCBhcyBw
b3NpdGl2ZSBjb250cm9sLCBvbiB0aGUgZm91ciBiYW5rZWQgcG9seWNyeXN0YWwgdGVuc29ycy4K
CiMjIENvbnRyb2xzIChhbGwgZXhhY3QpCkYtQUdHLVBJTjogUV9UIHF1YXJ0ZXQgcmVwcm9kdWNl
ZCB0byDiiaQgMsOXMTDigbvCueKBti4gRi1BR0ctS0s6IHRoZSBJbS1wYXJ0IHRpZS1pbiByZXBy
b2R1Y2VzIHRoZSByZWNvdmVyZWQgYGFscGhhX2Zpbml0ZWAgdG8g4omkIDfDlzEw4oG7wrnigbYg
KHRoZSByZWFsIHBhcnQgaXMgaXRzIGV4YWN0IEhpbGJlcnQgcGFydG5lciBieSBjb25zdHJ1Y3Rp
b24pLiBGLUNPTlY6IM6eLXF1YWRyYXR1cmUgZG91Ymxpbmcg4omkIDLDlzEw4oG7wrnCsywgzrwt
bm9kZXMgZG91Ymxpbmcg4omkIDLDlzEw4oG7wrnigbQsIFFfbWF4IGRvdWJsaW5nIOKJpCAxMOKB
u8K54oG1IOKAlCBjb252ZXJnZWQuIEYtQUdHLUw6IEwgY2hhbm5lbCBub256ZXJvIGFuZCBhbmFs
eXRpYy1jb250cm9sbGVkLgoKIyMgUmVzdWx0Cnwgc3Vic3RyYXRlIHwgRCgwKSAoc3RhdGljIEJv
cm4gc2hpZnQpIHwgKiph4oKCXmFnZyoqIChhbmFseXRpYyBrwrIgY29lZmZpY2llbnQpIHwgYeKC
hF5hZ2cgfCBh4oKCXmFnZy9RX1ReYSB8IGHigoIsTC9h4oKCLFQgfAp8LS0tfC0tLXwtLS18LS0t
fC0tLXwtLS18Cnwgc3RlcF9oZXggfCDiiJIyLjA1M8OXMTDigbvCsiB8ICoq4oiSMS44MzQ3NjbD
lzEw4oG7wrIqKiB8ICs2Ljk1NMOXMTDigbvCsiB8IOKIkjAuNTIxNCB8IDEuMzI1NyB8CnwgZ2Vt
OF9oZXggfCDiiJIyLjg5MsOXMTDigbvCsiB8ICoq4oiSMi41OTMzNjnDlzEw4oG7wrIqKiB8ICs5
Ljg5NsOXMTDigbvCsiB8IOKIkjAuNTE4NSB8IDEuMzI2NyB8Cnwgc3RlcF9jdWJpYyB8IOKIkjMu
MTUxw5cxMOKBu8KyIHwgKiriiJIyLjg1Mzc0N8OXMTDigbvCsioqIHwgKzEuMDY4w5cxMOKBu8K5
IHwg4oiSMC41Mjc3IHwgMS4zMjAwIHwKfCBnZW04X2N1YmljIHwg4oiSNC4zNjjDlzEw4oG7wrIg
fCAqKuKIkjMuOTcxMzk4w5cxMOKBu8KyKiogfCArMS40OTPDlzEw4oG7wrkgfCDiiJIwLjUyNjEg
fCAxLjMxODUgfAph4oKCXmFnZyBpcyBuZWdhdGl2ZSAobm9ybWFsIGRpc3BlcnNpb24pIGFuZCBP
KDEw4oG7wrIpIGZvciBldmVyeSBzdWJzdHJhdGU7IGl0IGV4Y2VlZHMgz4RfYWdnID0gMTDigbvi
gbYgYnkgZm91ciBvcmRlcnMgYW5kIGl0cyBjb252ZXJnZWQgdW5jZXJ0YWludHkgKOKJsjEw4oG7
wrnCsyByZWxhdGl2ZSkgYnkgdGhpcnRlZW4uIFR3byByZXBvcnQtb25seSBuZWFyLXVuaXZlcnNh
bGl0aWVzOiBh4oKCXmFnZy9RX1ReYSA9IOKIkjAuNTIgwrEgMC45JSwgYeKCgixML2HigoIsVCA9
IDEuMzIzIMKxIDAuMyUgKEYtQUdHLVVOSSkuCgojIyBTdHJ1Y3R1cmUgZmluZGluZyAodGhlIG1h
Y2hpbmUgYWdhaW5zdCBteSBwcmUtcmVnaXN0cmF0aW9uKQpUaGUgYWRkZW5kdW0gcHJlLXJlZ2lz
dGVyZWQgYSBub24tYW5hbHl0aWMga8KzIHRlcm0gYW5kIG1hZGUgdGhlIDMtdGVybSBiYXNpcyB7
a8KyLGvCsyxr4oG0fSB0aGUgYmFzaXMgb2YgcmVjb3JkIG9uIGRpc2FncmVlbWVudCwgcmVxdWly
aW5nIGl0cyBrwrIgY29lZmZpY2llbnQgdG8gbWF0Y2ggdGhlIGluZGVwZW5kZW50IGFuYWx5dGlj
IEQyIHdpdGhpbiBDSS4gVGhlIG1hY2hpbmUgcmVmdXRlcyB0aGUga8KzIHRlcm06IFIoaykgPSDO
lChrKSDiiJIgRDLCt2vCsiA9ICswLjA2OTXCt2vigbQgZmxhdCBvdmVyIGZvdXIgZGVjYWRlcyBv
ZiBrIChSL2vCsyDihpIgMDsgUi8oa+KBtCBsbiBrKSBub3QgY29uc3RhbnQpOyBhIHB1cmUgZXZl
biBiYXNpcyB7a+KBtCxr4oG2LGvigbh9IGZpdHMgUiB0byBybXMgOC41w5cxMOKBu+KBuSAodGhl
IHF1YWRyYXR1cmUgZmxvb3IpLiBUaGUgYWdncmVnYXRlIGRpc3BlcnNpb24gaXMgYW5hbHl0aWMg
aW4ga8KyOyB0aGUgZml0dGVkICJh4oKDIiBpcyBhbGlhc2luZyBvZiBh4oKGOyBib3RoIGZpdCBi
YXNlcyBhcmUgYmlhc2VkIDEuNeKAkzEuOSUgYnkgdGhlIGvigbYgdGVybSBvdmVyIHRoZSB3aW5k
b3c7IHRoZSBhbmFseXRpYyBjb250cm9sIGNhdWdodCBpdCAoSC1TMkMtMTAsIEgtUzJDLTExKS4K
CiMjIEYtQUdHLURJU1Ag4oCUIGV2YWx1YXRlZCB1bmRlciBib3RoIHJ1bGVzLCBub3QgY2hvc2Vu
Ci0gKipMb2NrZWQgcnVsZSAoQWRkZW5kdW0gUDIgYXMgd3JpdHRlbik6KiogdGhlIDMtdGVybSBm
aXR0ZWQgYeKCgiBtaXNzZXMgdGhlIGFuYWx5dGljIEQyIGJ5IDEuNOKAkzEuNSUgKFQpIGFuZCA1
4oCTNiUgKEwpLCBvdXRzaWRlIENJIOKHkiBGLUFHRy1BTkFMWVRJQyBmYWlscyDih5IgKiptZWNo
YW5pY2FsIGFybSBBNS1hZ2cgSU5TVFJVTUVOVC1MSU1JVEVELCBhbGwgZm91ciBzdWJzdHJhdGVz
LioqIFRoZSBydWxlIGlzIG5vdCBlZGl0ZWQuCi0gKipQcm9wb3NlZCBQMi1BIChhdXRob3IncyBk
ZWNpc2lvbiBwZW5kaW5nKToqKiBh4oKCXmFnZyBvZiByZWNvcmQgPSB0aGUgYW5hbHl0aWMgRDIg
KGNsb3NlZCBmb3JtIG9uIHRoZSBzYW1lIGtlcm5lbHMsIFIxLW1hY2hpbmUpLCB0aGUgbGFkZGVy
IGFzIGNvbmZpcm1hdGlvbiAozpQva8KyIOKGkiBEMiBpbiB0aGUgc21hbGwtayBsaW1pdCksIGHi
goMg4omhIDAsIGHigoReYWdnIGZyb20gdGhlIGV2ZW4gYmFzaXMg4oeSICoqQTMtYWdnIERJU1BF
UlNJVkUgKGdyYWluLXNjYWxlIGvCsiksIGFsbCBmb3VyIHN1YnN0cmF0ZXMuKiogVGhlIHBoeXNp
Y3MgZG9lcyBub3QgZGVwZW5kIG9uIHRoZSBkZWNpc2lvbjsgdGhlIHJlY29yZCdzIGFybSBsYWJl
bCBkb2VzLgoKIyMgQ29uc2VxdWVuY2UgKFBGLVMyKSBhbmQgc3RhdHVzCkJvdGggZGlzcGVyc2lv
biBzY2FsZXMgdGhlIHdpbmRvdyByZS1kZXJpdmF0aW9uIG5lZWRzIGFyZSBpbiBoYW5kIGFuZCBj
b25jb3JkYW50IGluIHNpZ24gYW5kIG1hZ25pdHVkZTogbGF0dGljZS1zY2FsZSBh4oKCID0g4oiS
MS4yOOKApuKIkjEuMzLDlzEw4oG7wrIgKM6T4oCTSykgLyDiiJIxLjk54oCm4oiSMi4wNsOXMTDi
gbvCsiAozpPigJNNKSBhdCBhKiAodHdvLWxlZywgQTMgYm90aCBsZWdzKSwgZ3JhaW4tc2NhbGUg
YeKCgl5hZ2cgPSDiiJIxLjjigKbiiJI0LjDDlzEw4oG7wrIgYXQgYV9nIChjaGF0IGxlZykuIFRo
ZSBTMiBjaGFubmVsIGRvZXMgbm90IHJpZGUgdGhlIGNvbmUgZXhhY3RseSBhdCBlaXRoZXIgc2Nh
bGU6IFdf4oiqIHN0YXlzIHN1c3BlbmRlZCwgYW5kIFdf4oiq4oCyIGlzIGEgZm9sZCBhY3Rpb24g
ZnJvbSB0aGUgYeKCgiBzY2FsZXMgb24geW91ciB3b3JkLiBTdGlsbCBvcGVuIGJlZm9yZSB0aGUg
Zm9sZCBwYWNrZXQ6ICgxKSB0aGUgY2hhdC1zaWRlIHJ1bi0yIG9uIHRoZSBzaW5nbGUtY3J5c3Rh
bCBTOSDigJQgdGhlIGF1dGhvciByZXBvcnRzIHJ1bi0yIEFMTCBQQVNTOyB0aGUgY2hhdCBzaWRl
IGhhcyBub3QgeWV0IHJlY2VpdmVkIENDJ3MgdjEuMSBjaGVja3BvaW50LCBjb21wYXJhdG9yIG91
dHB1dCwgYW5kIGNvbW1pdCB0byByZS1ydW4gdGhlIGZyb3plbiB2MS4xIChjYzkwMDVkMikgaXRz
ZWxmLCB3aGljaCB0aGUgcHJvdG9jb2wgcmVxdWlyZXM7ICgyKSBQMi1BOyAoMykgdGhlIFAyIEND
IGxlZyAodHdvLWxlZyBvbiB0aGUgYWdncmVnYXRlKSDigJQgYSBzZXBhcmF0ZSBkaXNwYXRjaC4g
SG9uZXN0eTogSC1TMkMtMTAsIC0xMSwgLTEyIGZpbGVkOyBUMSB6ZXJvIGhpdHMgb24gdGhpcyBy
ZXBvcnQgYW5kIHRoZSBQaGFzZS0zIGNoZWNrcG9pbnQgKG9uZSBILTItY2xhc3Mgc2VsZi1jYXRj
aCBpbiB0aGUgY2hlY2twb2ludCdzIG93biBob25lc3R5IHRleHQsIHJlcGhyYXNlZCkuIE5vIG9i
c2VydmFibGUsIG5vIGJyaWRnZSwgbm8gzrxfbiwgbm8gd2luZG93IGFjdGlvbiBoZXJlLgo=
<<<EMBED-END name=G_S2C1_PHASE3_REPORT.md>>>

### EMBED — chat P2 staging note — `G_S2C1_P2_AGGREGATE_STAGING.md` (md5 cad1319a16a70cf4af4f26730c4887ef, 5495 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=G_S2C1_P2_AGGREGATE_STAGING.md md5=cad1319a16a70cf4af4f26730c4887ef bytes=5495 enc=b64 quarantine=1>>>
IyBHLVMyQzEg4oCUIFBIQVNFIDMgLyBQUk9CRSBQMiAoQUdHUkVHQVRFKSDigJQgU1RBR0lORyBO
T1RFIChTZXB0ZW1iZXIgMywgMjAyNjsgTk9UIEFVVEhPUklaRUQsIE5PVCBFWEVDVVRFRCkKCioq
T2JqZWN0OioqIHByZXJlZyDCpzMgUHJvYmUgUDIg4oCUIGluIHRoZSBiYW5rZWQgUmF5bGVpZ2gg
bWFjaGluZXJ5LCB0aGUgc2NhdHRlcmluZy1pbmR1Y2VkIGZyYWN0aW9uYWwgcGhhc2UtdmVsb2Np
dHkgZGlzcGVyc2lvbiDOlGPigoIoz4kpL2PigoIgb2YgdGhlIFMyIGNoYW5uZWwgYW5kIGl0cyBh
dHRlbnVhdGlvbiBleHBvbmVudCBhY3Jvc3MgdGhlIFJheWxlaWdoIHdpbmRvdzsgd2hldGhlciB0
aGUgcXVhZHJ1cG9sZSBjb21iaW5hdGlvbiBpbmhlcml0cyB0aGUgdHJhbnN2ZXJzZSBRX1QtY2xh
c3MgY29lZmZpY2llbnRzIG9yIGNhbmNlbHMgYXQgbGVhZGluZyBvcmRlci4KCiMjIFJlY292ZXJl
ZCBpbnN0cnVtZW50IChpdGVtIDQgb2YgdGhlIGRpcmVjdGl2ZSkg4oCUIFJFQURZCkctUE9MWTEg
ZXN0YXRlIHJlY292ZXJlZCBmcm9tIHRoZSBDQyByZXBvLCBicmFuY2ggYGNsYXVkZS9uZXctc2Vz
c2lvbi1ndmJrb2ZgIEAgKioyMzFiNTU1YSoqLCBkaXJlY3RvcnkgYGdwb2x5MV9nYXRlL2A6IDIx
IGZpbGVzLCAqKjIwLzIwIE1BTklGRVNULm1kNSBlbnRyaWVzIHZlcmlmaWVkKiouIExvYWQtYmVh
cmluZyBwaWVjZXM6IGBwb2x5MV9mdWxscHJlY19jY2xlZy5weWAgKFNPKDMpIGNvdmFyaWFuY2Ug
zp4gb2YgdGhlIHJvdGF0ZWQgZWxhc3RpYyB0ZW5zb3IgYnkgR2F1c3PigJNMZWdlbmRyZS91bmlm
b3JtLUV1bGVyIHF1YWRyYXR1cmU7IG1vZGUtcHJvamVjdGVkIGtlcm5lbHMgzqZfVE0ozrwpOyBS
YXlsZWlnaCBhc3NlbWJseSBRX1QgPSBRX1RUICsgUV9UTDsgZmluaXRlLWthIEJvcm4gYXR0ZW51
YXRpb24gd2l0aCB0aGUgZXhwb25lbnRpYWwgdHdvLXBvaW50IHNwZWN0cnVtIM63KHEpIOKInSBh
wrMvKDErccKyYcKyKcKyOyB0aGUgcGlubmVkIGhleC9jdWJpYyBWb2lndCB0ZW5zb3JzKSwgYHBv
bHkxX3BoYXNlMWZ1bGxfY2MuanNvbmAgKHRoZSBiYW5rZWQgcXVhcnRldCDigJQgcmVwcm9kdWNl
ZCBoZXJlIGZyb20gdGhlIHJlY292ZXJlZCBjaGVja3BvaW50OiBzdGVwX2hleCBRX1ReYSAzLjUx
OTA3NGUtMiAoVl9UMCA4LjU0Nzc3OSwgVl9MMCAxNS4yMzI0ODcpLCBnZW04X2hleCA1LjAwMjA1
NWUtMiAoMTAuMjQ4OTk4LCAxOS4yMjg5MzkpLCBzdGVwX2N1YmljIDUuNDA3NzYzZS0yLCBnZW04
X2N1YmljIDcuNTQ5NDMwZS0yOyBmaXQgZXhwb25lbnRzIDMuOTkwOOKAkzMuOTkwOSksIHRoZSBw
cmVyZWcgKGRhYjQ2MmQyKSwgcGluIHJlY29yZCwgQ0MgcmVwb3J0LCBjb21wYXJhdG9yLiBMYXRl
ciBwaGFzZXMgbGl2ZSBvbiBicmFuY2hlcyA0Z3dobWUgKHBoYXNlMikgYW5kIGUxdTkxcCAocGhh
c2UzKSDigJQgbm90IG5lZWRlZCBmb3IgUDIuIE5PVEU6IHRoZSByZWNvdmVyZWQgUGhhc2UtMSBp
bnN0cnVtZW50IGlzIHRoZSBDQyBsZWcnczsgdGhlIGNoYXQtc2lkZSBQaGFzZS0xIGluc3RydW1l
bnQgd2FzIG5vdCBjb21taXR0ZWQuIEZvciBHLVMyQzEncyBQMiBpdCBzZXJ2ZXMgYXMgYSBmcmFt
ZXdvcmsgdG9vbCBmb3IgdGhlIGNoYXQgbGVnOyB0aGUgRy1TMkMxIENDIGxlZyBidWlsZHMgaXRz
IG93biAoRS02KS4KCiMjIFdoYXQgUDIgY29tcHV0ZXMgKG9wZXJhdGlvbmFsIGRlZmluaXRpb24s
IGZvciB0aGUgYXV0aG9yJ3MgZWxlY3Rpb24pClRoZSByZWNvdmVyZWQgbWFjaGluZXJ5IGNvbXB1
dGVzIEltIM6jX1QgKGF0dGVudWF0aW9uLCDPieKBtCkuIFAyIG5lZWRzICoqUmUgzqNfVCBhdCB0
aGUgc2FtZSBzZWNvbmQgKEJvcm4vU09BKSBvcmRlcioqIOKAlCB0aGUgU3Rhbmtl4oCTS2luby9X
ZWF2ZXIgcmVhbCBwYXJ0IOKAlCBmcm9tIHRoZSBpZGVudGljYWwgzp4gYW5kIM6mX1RNIGtlcm5l
bHM6IHRoZSBwcmluY2lwYWwtdmFsdWUgYW5ndWxhciBpbnRlZ3JhbCBvZiDOpl9UTSjOvCnCt863
KHEpLyhrX03CsiDiiJIgfGsg4oiSIHF8wrIpIG92ZXIgc2NhdHRlcmVkIHdhdmV2ZWN0b3JzLCBi
b3RoIE0g4oiIIHtULCBMfSwgZ2l2aW5nIM6UY19UL2NfVChrIGFfZykgPSDiiJJSZSDOo19ULygy
IGvCsiBWX1TCsikgd2l0aCBhX2cgdGhlIGdyYWluIGNvcnJlbGF0aW9uIGxlbmd0aC4gSW4gdGhl
IFJheWxlaWdoIHdpbmRvdyAoayBhX2cg4omqIDEpIHRoaXMgaXMgYSBUYXlsb3Igc2VyaWVzIGlu
IChrIGFfZynCsjogKipQMiBkZWxpdmVycyBh4oKCXmFnZyAoYW5kIGHigoReYWdnKSBmb3IgdGhl
IFQgY2hhbm5lbCBwZXIgc3Vic3RyYXRlIG9mIHRoZSBxdWFydGV0KiosIHRoZSBhZ2dyZWdhdGUt
c2NhbGUgYW5hbG9ndWUgb2YgUGhhc2UgMSdzIGxhdHRpY2Utc2NhbGUgYeKCgi4gQm91bmRlZCwg
Y2xvc2VkLWZvcm0tY2hlY2thYmxlICh0aGUgzrwtaW50ZWdyYWxzIGFyZSBwb2x5bm9taWFsIMOX
IHJhdGlvbmFsKSwgcmV1c2luZyB0aGUgYmFua2VkIM6eIChubyBuZXcgdGVuc29yIGlucHV0cyku
CgojIyBFbGVjdGlvbiByZXF1aXJlZCBCRUZPUkUgZXhlY3V0aW9uIOKAlCBFLVAyLTEgKGNoYW5u
ZWwgaW4gdGhlIGFnZ3JlZ2F0ZSkKVGhlIGFnZ3JlZ2F0ZSBhdmVyYWdlcyBvdmVyIGZ1bGwgU08o
MykgKHBpbm5lZCBFMy1lbGVjdGlvbnMgb2YgRy1QT0xZMSksIHNvIG5vIGxheWVyIHBsYW5lIHN1
cnZpdmVzOyBpbiAzLUQgZWxhc3RpY2l0eSB0aGUgc3RyYWluIG9mIGEgcHJvcGFnYXRpbmcgcGxh
bmUgd2F2ZSBpcyBr4oqXZSArIGXiipdrIChoZWxpY2l0eSAwIGZvciBMLCDCsTEgZm9yIFQgYWJv
dXQgayksIGFuZCBhIHB1cmUgaGVsaWNpdHktwrEyIChUVCkgc3RyYWluIGlzIG5vdCBhIHByb3Bh
Z2F0aW5nIGFjb3VzdGljIG1vZGUuIFRoZXJlZm9yZSBpbiB0aGUgYWdncmVnYXRlIHRoZSAiUzIv
cXVhZHJ1cG9sZSBjaGFubmVsIiBjYW4gb25seSBiZSB0aGUgKipwb2xhcml6YXRpb24tYXZlcmFn
ZWQgdHJhbnN2ZXJzZSAoc2hlYXIpIHdhdmUg4oCUIHRoZSBzaGVhciBjb25lIGl0c2VsZioqIOKA
lCBleGFjdGx5IHRoZSBjaGFubmVsIHdob3NlIFFfVCBxdWFydGV0IGlzIGJhbmtlZC4gUHJvcG9z
ZWQgZGVmYXVsdCAqKkUtUDItMSAoYSk6KiogUDIncyBjaGFubmVsID0gdGhlIGJhbmtlZCBUIGNo
YW5uZWwgKHByb2plY3RvciDCvShJIOKIkiBw4oqXcCksIFRUICsgVEwgZGVjb21wb3NlZCk7IHRo
ZSBjYW5jZWxsYXRpb24gcXVlc3Rpb24gYmVjb21lcyB3aGV0aGVyIHRoZSBkaXNwZXJzaW9uIGNv
ZWZmaWNpZW50IGHigoJeYWdnIHZhbmlzaGVzIGF0IFJheWxlaWdoIG9yZGVyIHdoaWxlIFFfVCAo
YXR0ZW51YXRpb24pIGRvZXMgbm90LiBBbHRlcm5hdGl2ZSAoYik6IGEgbGF5ZXItYW5pc290cm9w
aWMgKHRyYW5zdmVyc2VseSBpc290cm9waWMsIGhleC1heGlzLXRleHR1cmVkKSBhZ2dyZWdhdGUg
d2hlcmUgYW4gaW4tbGF5ZXIgReKCgiBzaGVhciBjYW4gYmUgc2luZ2xlZCBvdXQg4oCUIGEgZGlm
ZmVyZW50IHN1YnN0cmF0ZSBvYmplY3QgdGhhbiBHLVBPTFkxIGJhbmtlZDsgd291bGQgcmVxdWly
ZSBpdHMgb3duIEhhc2hpbuKAk1NodHJpa21hbi9SYXlsZWlnaCBjeWNsZS4gU3RydWN0dXJhbCBu
b3RlIGZvciB0aGUgcmVjb3JkOiB0aGlzIDMtRCBraW5lbWF0aWMgcG9pbnQgYXBwbGllcyB0byB0
aGUgZnJhbWV3b3JrJ3Mgb3duIHJlYWRpbmcgb2YgdGhlIEdXLXNpZGUgY2FycmllcjsgaXQgaXMg
ZGlzY2xvc2VkIGhlcmUsIG5vdCBkZWNpZGVkLgoKIyMgRmFsc2lmaWVycyAocHJvcG9zZWQgZm9y
IHRoZSBQMiBhZGRlbmR1bSBsb2NrKQotICoqRi1BR0ctRElTUDoqKiB8YeKCgl5hZ2d8ID4gz4Rf
YWdnIChwcm9wb3NlZCAxMOKBu+KBtiwgc2FtZSBhcyDPhCkgd2l0aCB0d28tbGVnIENJIOKHkiB0
aGUgc2hlYXIgY29uZSBpbiB0aGUgYWdncmVnYXRlIGlzIGRpc3BlcnNpdmUgYXQgUmF5bGVpZ2gg
b3JkZXIg4oeSIEEzLWNsYXNzIGZvciBQMi4gYeKCgl5hZ2cgPSAwIGF0IFJheWxlaWdoIG9yZGVy
IHdpdGggYeKChF5hZ2cg4omgIDAg4oeSIEEyLWNsYXNzLiBTaWduIGFuZCBtYWduaXR1ZGUgcmVs
YXRpdmUgdG8gdGhlIGJhbmtlZCBRX1QgcmVwb3J0ZWQgKHJhdGlvIGHigoJeYWdnL1FfVF5hIHBl
ciBzdWJzdHJhdGUpLgotICoqRi1BR0ctS0sgKGNvbnNpc3RlbmN5KToqKiB0aGUgcmVhbCBwYXJ0
J3Mgay1kZXBlbmRlbmNlIG11c3QgYmUgdGhlIEtyYW1lcnPigJNLcm9uaWcgcGFydG5lciBvZiB0
aGUgYmFua2VkIM+J4oG0IGF0dGVudWF0aW9uIHdpdGggdGhlIGV4cG9uZW50aWFsIHNwZWN0cnVt
IOKAlCB0aGUgYW5hbHl0aWMgcmVsYXRpb24gYmV0d2VlbiB0aGUgbGVhZGluZyBkaXNwZXJzaW9u
IGNvZWZmaWNpZW50IGFuZCBRX1QgYXQgZml4ZWQgzrcocSkgaXMgYSBjbG9zZWQtZm9ybSBjaGVj
ayAocG9zaXRpdmUgY29udHJvbCBvbiB0aGUgaW5zdHJ1bWVudCkuCi0gKipGLUFHRy1MIChwb3Np
dGl2ZSBjb250cm9sKToqKiB0aGUgTCBjaGFubmVsJ3MgYeKCgl5hZ2cgY29tcHV0ZWQgYnkgdGhl
IGlkZW50aWNhbCBwaXBlbGluZTsgbXVzdCBiZSBub256ZXJvIGFuZCByZXByb2R1Y2UgdGhlIHNh
bWUgY2xvc2VkLWZvcm0gcmVsYXRpb24uCi0gKipGLUFHRy1VTkk6KiogdGhlIFHigLJfRyBuZWFy
LXVuaXZlcnNhbGl0eSAoMC43OSUgYWNyb3NzIHRoZSBxdWFydGV0LCBiYW5rZWQgUjIpIHRlc3Rl
ZCBvbiB0aGUgZGlzcGVyc2lvbiBjb2VmZmljaWVudDsgcmVwb3J0ZWQsIG5vbi12ZXJkaWN0Lgot
ICoqRi1DT05WOioqIHF1YWRyYXR1cmUgZG91YmxpbmcgKG5iIDEw4oaSMjAsIG5hIDEy4oaSMjQp
IOKJpCAxMOKBu+KBuSBhcyBpbiBQaGFzZSAxOyBQViBpbnRlZ3JhbCBieSB0d28gbWV0aG9kcy4K
CiMjIFBGLVMyIGNvbnNlcXVlbmNlICh1bmNoYW5nZWQgZnJvbSB0aGUgbG9jaykKUDEgY2hhdC1s
ZWcgQTMgKHR3by1sZWcgcGVuZGluZykgYWxyZWFkeSByb3V0ZXMgV1/iiKog4oaSIHN1c3BlbmRl
ZDsgV1/iiKrigLIgaXMgcmUtZGVyaXZlZCBmcm9tIHRoZSBtZWFzdXJlZCBkaXNwZXJzaW9uIHNj
YWxlcyDigJQgUDEncyBh4oKCIChsYXR0aWNlIHNjYWxlIGEqKSBBTkQgUDIncyBh4oKCXmFnZyAo
Z3JhaW4gc2NhbGUgYV9nLCB0aGUgc2NhbGUgdGhhdCBwcm9kdWNlZCB0aGUgbWFjcm9zY29waWMg
KDAsIDIuMTIgbV0gd2luZG93IGluIEctUE9MWTEgUGhhc2UgMykuIEJvdGggYXJlIG5lZWRlZCBi
ZWZvcmUgYW55IHdpbmRvdyBhY3Rpb24uCgojIyBTdGF0dXMKSW5zdHJ1bWVudCByZWNvdmVyZWQg
YW5kIHZlcmlmaWVkOyBpbnB1dHMgaW4gaGFuZDsgRS1QMi0xIGFuZCB0aGUgUDIgZmFsc2lmaWVy
IGFkZGVuZHVtIG5lZWQgYXV0aG9yIGVsZWN0aW9uL2xvY2s7ICoqbm90aGluZyBjb21wdXRlZCoq
LiBUd28tbGVnOiBjaGF0IGxlZyBvbiB0aGUgcmVjb3ZlcmVkIG1hY2hpbmVyeSArIHRoZSBuZXcg
UmUgzqNfVCBzdGVwOyBDQyBsZWcgZnJvbSBzY3JhdGNoIChpdHMgb3duIM6eIHF1YWRyYXR1cmUs
IGl0cyBvd24gUFYgaW50ZWdyYWwpLgo=
<<<EMBED-END name=G_S2C1_P2_AGGREGATE_STAGING.md>>>
