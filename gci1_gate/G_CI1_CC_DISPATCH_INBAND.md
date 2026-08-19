# G_CI1_CC_DISPATCH_INBAND.md — Gate G-CI1 (Q3(1) Carrier-Identity Claim) — BLIND CC LEG DISPATCH (P-4: one self-contained file)

Minted 2026-08-19T16:32:18.417743+00:00 by the chat leg. Base canonical `SQT_Master_Ledger_v4_76_CANONICAL.md` md5 `f539d10cb4f73c81e7d9fdbe7fa63714` (1,432,221 B).
This file embeds, byte-exact, everything the CC leg needs: the LOCKED pre-registration, the FROZEN T1 list, the lock record and its addenda, the two byte-verified inputs, and the SEALED anchor file. **Extract each embed to a file with exactly the bytes between its fence lines and assert the stated md5 before use.** Nothing else is required or permitted as input.

## 0. Standing rules for the CC leg (read first)
1. **Full-from-scratch (E-9).** Build your own instruments from the pre-registration. No chat-leg instrument or checkpoint is embedded here, by design (blindness). Commitment hashes of the chat leg's sealed artifacts are listed in §6 so that ordering can be audited afterwards.
2. **T1 self-grep at every invocation** (case-sensitive extended regex against the frozen list) on every instrument and checkpoint you write. Exactly four embed classes are T1-exempt: the sealed anchor file, the lock record (+ Addenda 1–3, lock-record class), the pin record (election E-10 — its single hit is the SI velocity-unit token in the aluminium benchmark control line, not consumed), and the frozen T1 list itself (self-referential: the pattern list matches its own lines by construction). Your own files must be T1-clean; a hit is a halt.
3. **T4.** No SI value, no anchor value, no observational dialect token outside the sealed file and the Phase-3 mapper. Substrate units (rho = 1) throughout Phases 1–2.
4. **Sealed file UNOPENED until Phase 3.1.** Do not read the sealed embed (even by eye) before your Phase-2 checkpoint is written and hashed. At Phase-3 open: assert md5 `dd8fe2d364624750201ad9c9ffef575c` and census = 12 rows; parse by structured fields; never echo a row (M-1); form every comparison dimensionless before any print (M-2). **CC read #1 is the verdict read of record (E-9, CC-blind-first).** A-DIFF runs LAST of all arms.
5. **Checkpoints.** One JSON per phase: `ci1_phase0_cc.json`, `ci1_phase1_cc.json`, `ci1_phase2_cc.json`, `ci1_phase3_cc.json`; md5 and byte count reported for each; doubling gates recorded at every comparison-grid point.
6. **Halts (§5.5).** Any hash mismatch; containment miss (s1 or Q_T^a > 1e-6 relative vs the banked digits); an UNDERDETERMINED cone-degeneracy call that would decide K; an arm whose curve lookups cannot all be resolved; a T1 hit. Halt = write what you have, mark HALT, report; do not improvise.

## 1. Elections and rulings in force (T3-immutable; details in the embedded lock record + addenda)
E-0..E-9 as in the lock record §4; E-10 (pin-record embed exemption); E-11 (ray-regime attenuation VOID by default — no prior-art form pinned; a VOID only widens a window); E-12 (direct-PV I-3 route of record; KK diagnostic only).
**Phase 1 verdict of record (author-ratified, T3-immutable): F-IRR FIRES, K = ∅; CI-S FALSIFIED-STRUCTURAL; CI-W/EM-IN is the operative branch; W_∪ doubly conditional and SUSPENDED from the Phase-3 intersection (PF-1).** The CC leg still executes Phase 1 from scratch (R-a machine check + R-b inventory) as the independent second leg of the R1 table; the ratified reading of D-4 (H-4): a branch's helicity content is the eigenphase multiset of its mode's polarization/orbital data; derived strain/stress eigenphases are kinematic labels, recorded, not excitation content.
**H-6 (locked-text erratum, factor 8):** §4 2.2 defines Q_T(x) := alpha_T d / x^4 and says "-> Q_T^a"; with d = 2a (banked) the x->0 limit of that definition is Q_T^d = Q_T^a/8 (both banked). Read the two "Q_T^a" mentions as Q_T^d; tabulate both normalizations (Q^(a) -> Q_T^a; Q^(d) := alpha_T d/x^4 = Q^(a)/8) and alpha_T d itself; the mapper consumes alpha_T d. Containment's Q_T^a target is unaffected.
**H-8 / E-12 (route ruling for I-3, RATIFIED by the author, T3-immutable — Addendum 3):** the comparison quantity for C-CI-3 is the real part of the second-order mass operator obtained by DIRECT principal-value quadrature over the intermediate wavevector, on shell, with the k->0 static value subtracted (Delta_ch := -[Re mt_T(x) - Re mt_T(0)]/2 in the consistent second-order form; c_cone/V_T0 = 1/(1+Re mt_T(0)/2)). The subtracted Kramers–Kronig transform of alpha is NOT equivalent (the on-shell mass operator is not analytic in the upper half omega-plane: the SAF spectrum's poles move with k = omega/V); compute it only as a diagnostic if you wish, reported separately. Document your quadrature (the static subtraction must cover the SAF scale s ~ 1; the pole at s = k_M is removable after subtraction; the PV identity over a truncated range needs its exact correction term).

## 2. What to execute (pre-registration §4; thresholds §5)
**Phase 0 (CC):** assert the embed hashes (prereg 6c480340..., T1 653a0b74..., lock record a6adbb6a..., sealed dd8fe2d3..., inputs 200e7a8b... / 621120e5...); record D-1..D-9 as frozen (the embedded §2); sealed census asserted structurally (row-id regex count only, no field read); T1 zero hits. (The A0 literature pass was done by the chat leg and recorded NOT TRIGGERED; you need not repeat it.)
**Phase 1 (CC):** I-1 R-a: R_theta about k-hat, theta in {0.1, 2pi/7, 2pi/5}, tau_h = 1e-12, on (i) the aggregate transverse polarization subspace, (ii) each single-crystal qT eigenvector of the four E-7 tensors at >= 26 directions including axial/basal/oblique, (iii) the derived plane-wave strain sym(k (x) u) and stress C:eps. Record eigenphase multisets; the +-2 exclusion test; the derived-field labels. R-b: the inventory table over the banked branches (superfluid phase/Josephson complex; transverse acoustic pair; longitudinal; internal 7-sector (G-INT1); optical/intra-cell; orientational/bond/texture content) x columns (source record; gapless D-5; mode-variable rank + orbital content; helicity content; speed vs c_ch, D-5 class). Inventory only (E-4); a branch absent from the records is ABSENT. Form K and render F-IRR; compare to the verdict of record.
**Phase 2 (CC):** 2.1 containment (s1 and Q_T^a from the tensors, <= 1e-6 relative vs the banked digits: s1 = 1.51508022e-1 / 1.81569447e-1 / 2.33348904e-1 / 2.84231508e-1 and Q_T^a = 3.519074e-2 / 5.002055e-2 / 5.407763e-2 / 7.549430e-2 for hex:step / hex:gem8 / cubic:step / cubic:gem8); the A(theta)-anchor gate on the cubic tensors (the pin's (69) is the contraction <(delta C_nnmm)^2> = (nu^2/525)(3+cos^2 theta)^2; the n^4 m^4 contraction is (16 nu^2/525) P4(cos theta)); isotropic-input null. 2.2 I-2: Q^(a)(x), Q^(d)(x), alpha_T d, Im k/Re k on x = 10^n, n = -8..8 step 0.5 (33 points); Rayleigh exponent 4.00 +- 0.02 on [1e-4, 1e-3]. 2.3 I-3: Delta_ch(x) per H-8 (direct route), the scaled residual (Delta/x^2 for x <= 1e-2, Delta for x >= 1e-2), D2, the large-x plateau, per-point doubling gate (<= 1e-8; floor 1e-6 = VOID-NUM, H-logged), c_cone/V_T0, eps_T, x_S (Q^(d) x^3 <= 0.10 and eps_T x <= 1), x_G = 10. 2.4 ray bracket: c_path = 2/<1/v_qT1 + 1/v_qT2> over uniform S^2 (mean-arrival; fast/slow variants reported) vs the banked chain {Voigt, Reuss, Hill, HS-, HS+} (Voigt/Reuss/Hill from the input JSON; the banked HS shear bands: hex:step mu in [70.40652703751678, 70.97358894133485], hex:gem8 [99.81834260491628, 101.05874270193425], cubic:step [60.196099, 61.904685], cubic:gem8 [84.855805, 89.432106]); Delta_geo^X, min/max. Ray-regime attenuation: VOID (E-11).
**Phase 3 (CC, blind-first):** open the sealed embed only now; parse VLD and CONV first, then the ten arm rows in the stated read order; evaluate every arm per the pre-registration §4 Phase 3 and §5.4 (both-model overlap rule, gap rule, N-rules, OOM band, both-readings rules R1–R4 of the CONV row), A-DIFF last; under the ratified verdict (K = ∅) the POL arm is VOID-NO-CANDIDATE and the mapping is the CI-W/EM-IN face; write `ci1_phase3_cc.json` with the window(s) and the verdict class; **do not disclose any anchor value in your report text — report by row id, verdict class, and dimensionless ratios only** (M-1/M-2); the sanctioned post-verdict disclosure happens through the checkpoint carrier at fold.

## 3. Two-leg comparison protocol (chat leg performs the comparison after your return; pre-registration §8)
C-CI-1: R-a eigenphase multisets identical; R-b table identical in every cell (R1-machine two-leg); F-IRR verdict identical. C-CI-2: containment values, Q^(d)(x) and Q^(a)(x) on the 33-point grid, eps_T, x_S — <= 1e-6 relative. C-CI-3: the scaled residual on the grid (direct route), D2, plateau, Delta_geo^X — <= 1e-6 relative (points that either leg marks VOID-NUM are compared as VOID). C-CI-4: Phase-3 windows and verdict class identical (interval-set equality 1e-6). Any miss -> S9 escalation (both legs re-derive from the pre-registration text; no leg copies the other).

## 4. Report-back format
For each phase: checkpoint md5 + bytes; T1 hits (must be 0); the headline numbers (containment devs; D2 x4; c_cone/V_T0 x4; x_S x4; Delta_geo min/max x4; F-IRR); the Phase-3 verdict class and windows by row id (no anchor values in prose). H-items: number every self-catch; never silently correct.

## 5. Reserved successor / standing items (do not touch)
§2.52 Open 3 frozen; §2.87.J reserved; OP-2.58.2d and P-LEX-1 standing. Fold target after comparison: §2.91.N + Part VI row + W_∪ conditionality annotation on §2.91.M (V4.77-class), author-authorized only.

## 6. Chat-leg commitments (hashes only; contents withheld for blindness)
- `ci1_phase0.json`: md5 `b049856819f5e133e888771cf4ab69ec` (3,257 B)
- `ci1_resupply_verify.json`: md5 `d99d21b2bc15d9f0075ee9d00e6c69d8` (1,835 B)
- `ci1_phase1.json`: md5 `9d8e40b827f68d354335c2a147420636` (218,006 B)
- `ci1_phase2.json`: md5 `ee61b4b1cabda12ee77b27c05f425bc8` (57,470 B)
- `g_ci1_phase0_chatleg.py`: md5 `b8e6abcc45569daa43757a90e415b7ae` (5,875 B)
- `g_ci1_phase1_irrep_chatleg.py`: md5 `b5715bf62189c9f2105e451e396c21ce` (23,236 B)
- `g_ci1_phase2_regime_chatleg.py`: md5 `6db6e872edefe318e92c5e9448ef02ee` (26,815 B)

---
# EMBEDS (byte-exact; fences are `<<<EMBED name md5 bytes>>>` ... `<<<END name>>>`; the content is every byte between the two fence lines, excluding the single newline after the opening fence and the single newline before the closing fence)

## PREREG (LOCKED byte-identical; md5 6c480340...)
<<<EMBED G_CI1_EXECUTION_PREREGISTRATION.md 6c480340658a54e9da5d3553a8890c46 36793 SCANNED>>>
# G-CI1 — Execution Pre-Registration (DRAFT FOR LOCK)

**Gate:** G-CI1 (election E-0) — the Q3(1) Carrier-Identity Claim. **Drafted:** August 17, 2026, **before any computation.** **Status: DRAFT — NOT LOCKED. Phase 0 NOT opened. No instrument written. No sealed anchor file drafted (a lock-time artifact). Nothing evaluated.** Lock occurs only on the author's explicit freeze word, byte-identical to the reviewed text, md5-recorded, against whatever SQT canonical is current at that moment.

**Base:** `SQT_Master_Ledger_v4_76_CANONICAL.md` md5 `f539d10cb4f73c81e7d9fdbe7fa63714` (1,432,221 B). **Staging memo:** `staging_memo_Q3_1_carrier_identity.md` md5 `ca6d891f51c425bd46ffbb1dee4e45f8` (30,363 B) — APPROVED by the author August 17, 2026 (the B-3 burden ratified; the CI-S/CI-W differentiation ratified). This pre-registration is downstream of that memo and does not restate its LSF sweep; where the two differ, this document is the more precise and the memo is not amended.

**Two-document convention.** This pre-registration is written T1-clean by design (no observational-dialect tokens; see §10) so that it can travel as a scanned in-band embed. The author's election text is therefore reproduced **verbatim in the LOCK RECORD** (`G_CI1_LOCK_RECORD.md`, a T1-exempt embed, the G-POLY1 lock-record pattern) and only paraphrased here (§0). Where this document uses abstract labels (S2, TR-1…TR-4), the lock record and the sealed file carry the dialect names.

---

## §0 — Elections of record (paraphrased; verbatim text in the lock record)

- **E-0** Gate name **G-CI1** adopted.
- **E-1** **(a)** Channel referent = the **aggregate isotropized transverse acoustic channel** (V4.73/G-POLY1 lineage); the single-crystal branch-named reading is a subordinate arm carrying the V4.72 splitting burden.
- **E-2** Claim forms **CI-S** (primary) and **CI-W** (pre-registered retreat) adopted, definitions **T3-immutable** at lock (§2).
- **E-3** Scope = **radiative sectors only**; matter-sector species universality → named successor gate (§9.4).
- **E-4** Phase-1 **R-b policy: inventory only** of banked degrees of freedom; no new model construction (R-c excluded, own staging required).
- **E-5** Sealed-anchor roster: **A-EM-TRANS** (four rungs, ordered by decreasing carrier wavelength **TR-1, TR-2, TR-3, TR-4** — the author's four named bands, TR-4 the shortest-wavelength ground-based very-high-energy rung), **A-ACHROM**, **A-BIR-EM**, **A-POL**, **A-DIFF**. Row-level content is drafted into the sealed file at lock (§7).
- **E-6** Gauge-paper firewall maintained (no EM-mechanism content consumed or emitted; §7.4 precedent).
- **E-7** Kernels **{step, gem8}**, **hex primary + cubic labelled** (KNOB named throughout).
- **E-8** Thresholds, tolerances, OOM bands, N-style voiding rules, validity indicators, halts — **§5 of this document** (author to confirm or amend at lock; PF-4).
- **E-9** Leg architecture: **CC full-from-scratch; CC-blind-first for the Phase-3 read** (E3-5(a) precedent).

---

## §1 — Question, object, register targets

**Question.** Is the Q3(1) claim — *EM and the spin-2 radiative sector share the one transverse channel* — well-posed and surviving on the banked domain-scale window, in its strong form (carrier co-residency, CI-S), or only in its weak form (cone identity, CI-W), or in neither?

**Object.** The E-1(a) channel of the polycrystalline aggregate built from the four G-TSH4-lineage elastic tensors (hex:step, hex:gem8 primary; cubic:step, cubic:gem8 labelled), with the banked G-POLY1 estate: the Rayleigh quartet Q_T^a, the birefringence quartet s₁ and the path-random law δ_RMS(L) = s₁·√(d/L), the sealed-anchor window architecture, and W_∪ = (0, 2.1213132100130068] in SI length units (CONSERVATIVE, spin-2-side-anchor-governed, import-conditional). Nothing new is imported (§3).

**Register targets.** Phase-1 R-a result: theorem-class (R1) with machine confirmation. F-IRR inventory verdict: R1-machine two-leg on the table; R2 on the reading. Phase-2 numerics: R1-machine two-leg. Phase-3 windows and verdict classes: R1-machine two-leg, **conditional on the named imports (§3.3) and revocable with them**. The CI-S/CI-W physical reading: R2 at most. **The polycrystal postulate remains R3 under every outcome; nothing is promoted by this gate.**

---

## §2 — Definitions (frozen at lock; T3-immutable per E-2)

**D-1 Channel (E-1(a)).** The long-wavelength transverse acoustic sector of the statistically isotropic, untextured polycrystalline aggregate of the substrate (V4.73/G-POLY1): the two degenerate transverse displacement polarizations propagating at the aggregate speed c_ch. Single-crystal transverse branches (qT₁, qT₂ per direction, both structures, both kernels) are the subordinate branch-named reading.

**D-2 Cone speed.** c_cone := c_ch(k→0⁺), the effective-medium limit of the channel phase speed computed by the Phase-2 instrument (its own k→0⁺ limit — no external aggregate convention enters the definition). This is the ANNEX-CDEF-1 referent under E-1(a).

**D-3 In-channel.** A radiative sector is *in-channel* iff its quanta are excitations of the D-1 channel (their propagation is the channel's propagation: same dispersion, same grain scattering, same regime map).

**D-4 Helicity content.** For a mode of wavevector k in the aggregate, the multiset of eigenphases e^{iλθ} of the rotation R_θ about k̂ acting on the mode's polarization/orbital data, λ ∈ ℤ; for single-crystal branches the same kinematic label applied to the branch's polarization vector and its derived strain/stress fields (SO(2)_k̂ is then not a symmetry; the label is still well-defined).

**D-5 Gapless / degenerate with the cone.** *Gapless*: banked as a zero mode (Goldstone) at Γ in the cited records, or (if a leg recomputes) ω(q_min)/ω_ref ≤ 1e-3 with a fitted small-q exponent ≥ 0.9. *Degenerate with the cone*: |v_branch/c_ch − 1| ≤ θ₁ = 3% (DEGENERATE); ≥ θ₂ = 10% (NOT); (3%, 10%) UNDERDETERMINED (§5.5 halt rule).

**D-6 CI-S (strong form — carrier co-residency).** EM and the spin-2 radiative sector (S2) are both in-channel (D-3) excitations of the D-1 channel. This is Q3(1) as written and the form under adjudication. **Well-posedness requirement (B-3):** the channel hosts a gapless helicity-±2 excitation degenerate with the cone (F-IRR).

**D-7 CI-W (weak form — cone identity).** EM and S2 share the propagation cone (one speed c_cone, one transverse plane) **without** carrier co-residency in the D-1 channel. Sub-branches, fixed by Phase 1 and by the standing declarations, not elected inside the gate:
- **CI-W/EM-IN:** EM in-channel, S2 not in-channel (S2 on the cone by assumption). *The pre-registered computable retreat.*
- **CI-W/EM-OUT:** neither sector in-channel. No banked falsifier surface reaches it → **UNADJUDICATED-DEGENERATE**; an author declaration item (M.ONT-adjacent), recorded not decided.
- **CI-W/S2-IN-only:** S2 in-channel, EM out — reachable only if F-IRR passes, F-POL passes on K, and the EM-face arms return an empty window while the S2 face does not (EM-in-channel falsified, S2-in-channel not); Phase 3 then reports the S2 face (W_∪ inherited) as the surviving reading, explicitly weaker.

**D-8 CI-V (vector-carrier reading) — NAMED, NOT ADOPTED.** "The S2 sector is the helicity-±1 transverse acoustic wave itself." This is vocabulary substitution (spin-2 → spin-1) foreclosed by E-2; it is not CI-S and is not adjudicated. Its would-be first surface is A-POL. Recorded so that no post-verdict slide into it can occur silently (PF-3).

**D-9 Regime variable.** x := k·d, with k the carrier wavevector magnitude in the aggregate (k = ω/c_cone) and d the domain scale (M.CW; never derived).

---

## §3 — Inherited estate, byte provenance, imports

**3.1 Consumed (banked; zero new physics imports).** (i) The four full-precision tensors of `poly_vrh_results.json` md5 `200e7a8b775577564369c6924d38a84c` (2,767 B) — **required by re-supply, byte-verified (X-1 style) before Phase 2 opens (PF-6)**; fallback: the ledger-transcribed full-precision block (hex (C11, C12, C13, C33, C44, C66): hex:step 238.4183, 108.5389, 57.4751, 287.6688, 60.0308, 64.9223; hex:gem8 377.5438, 200.2076, 111.0018, 467.7554, 84.8245, 88.6835; cubic (C11, C12, C44): cubic:step 172.7994, 99.349, 85.2934; cubic:gem8 272.0753, 179.3756, 131.5436) admitted only if the §5.2 containment reproduction passes. (ii) Q_T^a = {3.519074e-2, 5.002055e-2, 5.407763e-2, 7.549430e-2}, Q_T^d = Q_T^a/8. (iii) s₁ = {1.51508022e-1, 1.81569447e-1, 2.33348904e-1, 2.84231508e-1}; the law δ_RMS(L) = s₁·√(d/L). (iv) The SAF pinned in G-POLY1: η(r) = exp(−r/a), d = 2a, η̃(0) = a³/π², spectrum ratio η̃(q)/η̃(0) = (1 + q²a²)⁻² (the banked finite-ka dressing). (v) The Rayleigh assembly and Born-validity statements of the FROZEN pin record 621120e5 (10,759 B) — **required by re-supply (PF-7)**; fallback: verbatim re-retrieval and re-pin at Phase-2 open under the transcription rule (no reconstruction from memory). (vi) The G-POLY1 Phase-0b VRH/HS chain (§C conventions) for the aggregate-speed conventions used in the ray-regime bracket. (vii) The G-ζ1 / G-TSH1 / G-TSH4 (Route D) / G-INT1 mode records for the R-b inventory. (viii) W_∪ and its four per-config edges as inputs (not re-run).

**3.2 ANNEX-CDEF-1 clause discharged here.** The A-DIFF comparison is the "own pre-registration" the clause requires; it runs last of all (§4, Phase 3), CC-blind-first.

**3.3 Imports named (both pre-existing; neither exercised outside the sealed mapper).** (a) The A-SHEAR-lineage transverse-scale import (channel speed ↔ SI), exercised only inside `anchors_G_CI1_SEALED.md`'s CONV row and the Phase-3 mapper, exactly as G-POLY1. (b) The M.CW domain scale d as the free axis. **Not licensed:** ξ = ℓ_P for the transverse sector (ANNEX-SC-1 substitution clause standing) — therefore **no SI-valued substrate floor exists in this gate**; F-VLD's floor is stated in substrate units (d ≥ N_cell·a) and left unexercised; every window is reported unbounded below in SI, the P-2 pattern.

**3.4 Consistency flag (recorded, not adjudicated).** The ANNEX-CDEF-1 c-referent is single-valued only under E-1(a) (or a named branch). Under CI-W/EM-IN it survives as c_cone with EM in-channel; under CI-W/EM-OUT the referent has no carrier on the books — flagged for the author.

---

## §4 — Phases and instruments (execution order fixed)

**Phase 0 — Definitions, checklist, final A0 pass (chat leg; CC repeats optionally).**
0.1 Assert base canonical md5, memo md5, this pre-registration's lock md5, T1 list md5 (§10) — checkpoint `ci1_phase0.json`.
0.2 Freeze D-1…D-9 verbatim (this text).
0.3 Final A0 collision pass: one targeted retrieval on the exact CI-S phrasing (co-resident EM + helicity-±2 excitations of one elastic transverse channel of a discrete/aggregate medium). Query strings and result summary recorded (paraphrase only). **A0 TRIGGERED** iff a located source asserts CI-S as defined → **HALT, return to author before Phase 1.**
0.4 Assert the sealed file's md5 and census against the lock record (`anchors_G_CI1_SEALED.md` is drafted and sealed at lock, §13.3); **UNOPENED until Phase 3.**
0.5 T1 self-grep zero hits on every Phase-0 file.

**Phase 1 — I-1 irrep/helicity audit (both legs; anchor-free).**
1.1 **R-a machine check.** Construct R_θ about k̂ for θ ∈ {0.1, 2π/7, 2π/5}; act on (i) the aggregate transverse polarization subspace, (ii) each single-crystal qT eigenvector (E-7 tensors, ≥ 26 directions incl. the E4 axial/basal/oblique set), (iii) the derived plane-wave strain ε_ij = i(k_iu_j + k_ju_i)/2 and stress σ = C:ε. Record helicity content (D-4). Exact arithmetic permitted (then τ_h trivially met).
1.2 **R-b inventory (E-4).** A table over the banked branches: {superfluid phase / Josephson complex; transverse acoustic pair; longitudinal acoustic; the internal 7-component sector (G-INT1: two-body gapless, three-body-gapped on Fano lines); optical/intra-cell branches on the books; orientational/bond content of the droplet lattice} × columns {source record; gapless (D-5); mode-variable tensor rank + intra-cell orbital content; helicity content; long-wavelength speed vs c_ch (D-5 class)}. No branch is constructed; a branch absent from the records is listed ABSENT, not modelled.
1.3 **F-IRR decision (§6).** Candidate set K := {branches with gapless ∧ (±2 ∈ helicity content) ∧ DEGENERATE-with-cone}. K = ∅ → F-IRR FIRES → CI-S FALSIFIED-STRUCTURAL → CI-W arm. K ≠ ∅ → CI-S well-posed; K carried to F-POL. Any UNDERDETERMINED degeneracy call that would decide K → halt (§5.5).
1.4 Checkpoint `ci1_phase1.json` (table, eigenphases, verdict); T1 zero hits.

**Phase 2 — I-2 regime map + I-3 residual ledger (both legs; substrate units; T1-clean; zero anchors).**
2.1 **Containment (opens the phase).** From the tensors reproduce s₁ (both legs' own eigen-quadrature) and Q_T^a (the SO(3)-quadrature covariance Ξ + transverse projector + Rayleigh assembly, the G-POLY1 Phase-1 construction) — thresholds §5.2. Fail → **HALT (X-1 unresolved).**
2.2 **I-2 attenuation curve.** For each config and P = T: the second-order (Born) attenuation with the SAF spectrum evaluated at the physical momentum transfer of every scattering channel — Q_P(x) := Σ_M (V_P0/V_M0)³/(2V_P0²V_M0²) ∫ Φ_PM(n̂,n̂')·η̃(q_PM)/η̃(0) dμ with q_PM = |k_P n̂ − k_M n̂'|, k_M = k_P V_P0/V_M0, and α_P(x)·d = Q_P(x)·x⁴, α the amplitude attenuation coefficient (Im k) in the banked convention, ℓ_att := 1/α; grid §5.2. The well-conditioned comparison quantity is Q_T(x) := α_T·d/x⁴ (→ Q_T^a as x→0). Controls: x→0 recovers Q_T^a (containment) and the fitted exponent 4 (§5.2).
2.3 **I-3 residual curve.** Δ_ch(x) := [c_ph(x) − c_cone]/c_cone from the real part of the same second-order mass operator (direct principal-value quadrature over the intermediate wavevector, or a subtracted Kramers–Kronig transform of the leg's own α — each leg documents its route; the two legs need not use the same route). Report the small-x coefficient D₂ (Δ_ch → D₂·x², sign as computed) and the large-x plateau; the well-conditioned comparison quantities are Δ_ch/x² for x ≤ 1e-2 and Δ_ch for x ≥ 1e-2. **Mapper continuations (fixed here):** for x < 1e-4 the mapper uses the certified Rayleigh tails Δ_ch := D₂·x² and Q_T := Q_T^a; for x ≥ 1e-4 the tabulated curves, log-log interpolated.
2.4 **Ray-regime bracket.** c_path := 2/⟨1/v_qT1 + 1/v_qT2⟩_{S², uniform} (mean-arrival convention, primary; fast/slow variants reported); Δ_geo^X := (c_path − c_agg^X)/c_agg^X for X ∈ {Voigt, Reuss, Hill, HS−, HS+} (banked chain); report min/max over X.
2.5 **Validity indicators** (§5.4) computed per config: ε_T, x_S, coherence, phase criterion.
2.6 Checkpoint `ci1_phase2.json`; T1 zero hits; per-leg doubling gates recorded.

**Phase 3 — I-4 sealed-anchor W_Q3 mapper (runs LAST; CC-blind-first per E-9; A-DIFF last of all).**
3.1 Open sealed file; assert md5 + census; parse rows structurally (never echo). Read order fixed: A-EM-TRANS (TR-1→TR-4) → A-ACHROM → A-BIR-EM → A-POL → A-DIFF.
3.2 Convert each row's reference quantities to k_r (aggregate wavevector) and D_r (path length) using the CONV row only.
3.3 Evaluate each arm's criterion (§7 patterns) on a log-d grid, apply validity/N-rules (VOID never counts as FAIL, and is reported distinctly from PASS), form the interval windows, apply the OOM bands, intersect over arms, unite over configs (CONSERVATIVE, the W_∪ convention), report per-arm/per-config edges with regime placement x_r at each edge, and the verdict class (§6).
3.4 CC read #1 = the blind verdict read of record; CC checkpoint hashed and returned before the chat read; chat masking discipline §8.4; chat read after.
3.5 Checkpoints `ci1_phase3_cc_read1.json`, `ci1_phase3_chat_read<n>.json`.

**D-1 — Danielewski differentiation memo (documentary; single-leg + CC audit; verdict-independent).** `G_CI1_D1_DANIELEWSKI_DIFFERENTIATION.md`: attribution block (the transverse-elastic-EM lineage: MacCullagh 1839 → Kelvin → Kleinert world-crystal → the Planck–Kleinert program 2007–2026, all citations of the memo's Register A verified at lock); the memo §3 differentiation table with source pointers (paraphrase; any direct quotation ≤ 15 words and at most one per source); a one-paragraph differentiation statement whose load-bearing axis is the opposite gravity routing; a "what is not claimed" line. Acceptance: citation existence + claim-consistency audited by the CC leg (categorical PASS/FAIL per row; a FAIL row is repaired before fold, H-logged). Discharge of Burden B-1 completes on acceptance regardless of the gate verdict.

---

## §5 — E-8: thresholds, tolerances, OOM bands, N-rules, validity, halts

**5.1 Structural.**
| Item | Value |
|---|---|
| Helicity eigenphase tolerance τ_h | 1e-12 rad (per eigenphase, each θ) |
| ±2 exclusion | no eigenphase within τ_h of ±2θ, any θ in the set |
| Gapless (recompute route) | ω(q_min)/ω_ref ≤ 1e-3 AND small-q exponent ≥ 0.9 |
| Cone degeneracy θ₁ / θ₂ | 3% / 10% (standing thresholds; dead zone UNDERDETERMINED) |
| A0 trigger | as §4 Phase 0.3 (categorical) |

**5.2 Phase-2 containment and controls.**
| Item | Value |
|---|---|
| s₁ reproduction (per config) | ≤ 1e-6 relative vs the banked digits |
| Q_T^a reproduction (per config) | ≤ 1e-6 relative vs the banked digits |
| Rayleigh exponent control | fitted d ln α/d ln x on x ∈ [1e-4, 1e-3] within 4.00 ± 0.02 |
| Per-leg quadrature doubling gate | ≤ 1e-8 relative on Q_T(x) and on the scaled residual (Δ_ch/x² for x ≤ 1e-2, Δ_ch for x ≥ 1e-2) at every comparison-grid point (attained value recorded; a point not reaching ≤ 1e-6 is VOID-NUM and H-logged) |
| Comparison grid | x = 10^n, n = −8, −7.5, …, +8 (33 points) |
| ε_T (fluctuation strength) | RMS relative deviation of the two transverse eigen-speeds from their pooled sphere mean (uniform S², both polarizations pooled) |

**5.3 Two-leg comparison (E-9; S9 on any miss).**
| Criterion | Content | Tolerance |
|---|---|---|
| C-CI-1 | Phase-1 helicity contents (multisets), inventory row-set, F-IRR verdict | categorical identity; eigenphase deviations both ≤ τ_h |
| C-CI-2 | Containment values; Q_T(x) on the comparison grid; ε_T; x_S | ≤ 1e-6 relative (categorical for x_S regime labels) |
| C-CI-3 | The scaled residual on the grid (Δ_ch/x² for x ≤ 1e-2, Δ_ch for x ≥ 1e-2); D₂; large-x plateau; Δ_geo^X min/max | ≤ 1e-6 relative |
| C-CI-4 | Every per-arm/per-config edge of record; interval counts; verdict class; OOM lines | edges ≤ 1e-6 relative; counts and classes identical |
| C-CI-5 | Sealed md5 + census; every checkpoint md5; T1 list md5 | identity |
| C-CI-6 | Deviation-table containment: every extraction/route divergence pre-registered on BOTH legs before the chat read (E3-7(a) pattern) | any out-of-table item → S9 |

**5.4 Regime, validity, and voiding rules (per config, per arm; VOID ≠ FAIL).**
| Rule | Value / definition |
|---|---|
| Weak-fluctuation validity (second-order theory) | ε_T² ≤ 0.10 (global per config; else all second-order arms VOID for that config, reported) |
| Coherent-wave validity | Im k/Re k = Q_T(x)·x³ ≤ 0.10 at the evaluated x (else VOID-INCOHERENT at that x) |
| Phase-perturbation validity | ε_T·x ≤ 1 (else VOID-PHASE at that x) |
| x_S | the largest x on the grid satisfying both preceding rules (second-order curve trusted for x ≤ x_S) |
| Ray-regime domain | x ≥ x_G = 10 — F-DIFF uses the Δ_geo bracket; P-ACHROM-DISP: identical path averages ⇒ zero difference (PASS-RAY, nondispersive rays), reported |
| Overlap x_G ≤ x ≤ x_S | where both models are available, an exclusion is asserted only if BOTH exclude (else VOID-DISAGREE, reported); where only the second-order model is available (ray attenuation unpinned), the second-order curve governs up to x_S |
| Gap x_S < x < x_G | VOID unless the bridge rule holds: BOTH boundary points excluded AND the leg's own \|Δ_ch\| (resp. α·d) is unimodal/monotone across the gap — then excluded; else VOID |
| Birefringence-walk arm live iff | N_λ := d/λ_r ≥ 10 AND N_dom := D_r/d ≥ 10 (else VOID-N) |
| Ray-bracket exclusion | asserted from min_X \|Δ_geo^X\| only (conservative); all X reported |
| Attenuation in ray regime | Born curve not used above x_S; the ray-regime attenuation is VOID unless a verbatim prior-art form is pinned at Phase-2 open (PF-7); a VOID here can only widen a window |
| OOM robustness | every sealed threshold (τ_r, Δτ_r, β_r, κ_r, band edges) recomputed at ×10 and ×0.1; a class is OOM-robust iff identical under both |
| Substrate floor | d ≥ N_cell·a with N_cell = 10 in substrate units; **not converted to SI** (§3.3) |
| Window arithmetic | sorted disjoint half-open intervals in d > 0; per arm PASS-set with VOID treated as non-excluding but flagged; ∩ over arms; ∪ over configs; PRESERVING test = interval-set equality with W_∪ at ≤ 1e-6 relative on endpoints |

**5.5 Halts / return-to-author (any leg).** A0 TRIGGERED; §5.2 containment fail; sealed md5 or census mismatch at open; any T1 hit in an instrument or checkpoint; any UNDERDETERMINED cone-degeneracy call that decides K on any config; F-CI-*-MACRO firing (instrument-defect review mandatory before acceptance, §6); any S9.

---

## §6 — Arms, surfaces per branch, verdict matrix

**Arms.** F-IRR (Phase 1; anchor-free). F-POL (A-POL; categorical). F-EM-TRANS (TR-1…TR-4; P-TRANS). F-ACHROM (two sub-rows: chromatic dimming P-ACHROM-DIM; chromatic dispersion P-ACHROM-DISP). F-BIR-EM (two sub-rows; P-BIR). F-DIFF (A-DIFF; P-DIFF; last). F-VLD (validity edges §5.4; the substrate floor unexercised).

**Surface matrix.**
| Branch | F-IRR | F-POL | F-EM-TRANS | F-ACHROM | F-BIR-EM | F-DIFF | W_∪ role |
|---|---|---|---|---|---|---|---|
| CI-S (K ≠ ∅) | PASS by definition | on K | yes | yes | yes | Δ_S := [c_ph(x_EM) − c_ph(x_S2)]/c_ph(x_S2) | intersected |
| CI-W/EM-IN | FIRED | VOID-NO-CANDIDATE | yes | yes | yes | Δ_W := Δ_ch(x_EM) (S2 = cone by assumption) | **SUSPENDED** — reported alongside, not intersected (PF-1) |
| CI-W/S2-IN-only | PASS | PASS on K | returned ∅ | returned ∅ | returned ∅ | Δ_S evaluated, reported | intersected (spin-2 face only) |
| CI-W/EM-OUT | — | — | — | — | — | — | UNADJUDICATED-DEGENERATE |

**Verdict classes.**
- **P-CI-S-PRESERVING** — CI-S live and W_Q3 = W_∪ (no EM arm governs).
- **P-CI-S-TIGHTENING** — CI-S live and ∅ ≠ W_Q3 ⊊ W_∪ (a union of intervals is admissible; banked with per-arm/per-config edges and OOM lines).
- **F-CI-S-MACRO** — CI-S live and W_Q3 = ∅. *Structural note pre-declared:* every roster arm vanishes as d → 0⁺ (Rayleigh) or is VOID there (N-rules), so this class can fire only through an instrument defect or a floor-binding arm not in the roster; on firing, review before acceptance (§5.5).
- **F-CI-S-STRUCT** — F-IRR fires (K = ∅) or F-POL fires on K; CI-W arm activates.
- **P-CI-W/EM-IN-WINDOWED** — under CI-W/EM-IN, W^EM := W_EM ∩ W_DIFF ∩ W_VLD ≠ ∅, banked with edges; reported explicitly as the weaker form (cone identity is then an assumption; the radiative component of B-2 is *transferred to that assumption, not discharged*).
- **F-CI-W/EM-IN-MACRO** — W^EM = ∅ (same structural note as MACRO).
- **CI-W/S2-IN-only WINDOWED / MACRO** — the spin-2 face only, W_∪-conditioned.
- **CI-W/EM-OUT: UNADJUDICATED-DEGENERATE.**

**Priors, stated so they cannot be adjusted afterwards (the G-C1 pattern).** R-a: the transverse displacement channel and its strain/stress fields carry helicity {±1} (and 0) only — theorem-shaped; the machine check confirms rather than decides. R-b: the banked gapless set is Goldstone-counted (three lattice translations + U(1) phase in 3D; the internal sector spatially unlocked on the books) — no gapless helicity-±2 branch is expected; **F-IRR is expected to fire and CI-W/EM-IN is the expected operative branch.** F-DIFF is ceiling-shaped (Δ_ch vanishes as x → 0 and plateaus at large x while its reference sits at the cone), whereas the EM-internal arms are interval-shaped (they vanish at both regime ends), so a WINDOWED (tightening-type) outcome is the expected class of the operative branch. No number is anticipated; every edge comes from execution.

---

## §7 — Sealed anchor file `anchors_G_CI1_SEALED.md` (drafted at lock; md5-asserted at every open; UNOPENED before Phase 3)

**Census (fixed here, asserted at every open): 12 rows** — 4 × A-EM-TRANS (TR-1…TR-4) + 2 × A-ACHROM (ACH-DIM, ACH-DISP) + 2 × A-BIR-EM (BIR-1 long-wavelength polarimetry, BIR-2 short-wavelength polarimetry) + 1 × A-POL + 1 × A-DIFF + 1 × VLD (validity edge parameters, mirrors G-POLY1 A-4) + 1 × CONV.

**Row schema (structured fields; parsed, never echoed):** `id | class | pattern | dialect_ref (memo Register letter+item) | anchor_text (verbatim quantity string, sealed) | params (k-reference(s) — the A-DIFF row carries both k_EM and k_S2; D_r; threshold(s); sign convention) | Caveat | Binding | frozen-ASCII flag`. Frozen-ASCII semantics inherited (E3-6(a)); superscript-detached readings are read conservatively (a corrected reading may only tighten). Loud-flagged fallbacks and the terminal masked-diagnostic rule inherited from P3-A2.

**Patterns (this gate's own family; the criterion is the PASS condition).**
- **P-TRANS:** α_T(x_r; d)·D_r ≤ τ_r. TR rows carry the arrival budget τ_r = 1 (CONSERVATIVE, Caveat: tighter residual budgets exist and would only tighten).
- **P-ACHROM-DIM:** |α_T(x₁;d) − α_T(x₂;d)|·D_r ≤ Δτ_r (two reference wavevectors within one observed band).
- **P-ACHROM-DISP:** |Δ_ch(x₁;d) − Δ_ch(x₂;d)| ≤ β_r (EM-internal; the memo Register F(iii) vacuum-dispersion class).
- **P-BIR:** the polarization-walk phase Φ_RMS := s₁·k_r·√(d·D_r) ≤ κ_r (radians; the depolarization budget implied by the sealed polarization-degree observation), live only under the N-rules; Binding: a random-axis walk is a depolarization observable and is compared to the sealed budget at order-of-magnitude level only (R2, the DLM-comparison precedent); Caveat: the coherent-birefringence coefficient bounds of the memo's Register F(iii) are a different dialect (fixed axis) and are NOT used as κ_r.
- **P-POL:** categorical — K's helicity content ⊇ {±2} and tensor-dominant → PASS; {±1}-only → FAIL; mixed → INDETERMINATE (Binding: the papers' own extreme-hypothesis caveat).
- **P-DIFF:** B_lo ≤ Δ ≤ B_hi with Δ per §6 (Δ_S or Δ_W); the row's Binding clause states the observational sign convention and its mapping onto Δ.
- **VLD row:** the numeric N-rule and validity thresholds of §5.4 restated for the mapper (no physics; guards against silent drift).
- **CONV row:** the SI conversion constants (channel-speed↔SI via the transverse-scale import; energy↔wavevector; distance units) — the only place they exist; T1-exempt embed.

**Post-verdict disclosure:** rows disclosed via the sanctioned checkpoint carriers verbatim (anchor_texts, Caveat/Binding), the G-POLY1 pattern.

---

## §8 — Two-leg architecture, dispatch, checkpoints, masking

**8.1 Legs.** Chat leg: from-scratch instruments `g_ci1_phase1_irrep_chatleg.py`, `g_ci1_phase2_regime_chatleg.py`, `g_ci1_phase3_mapper_chatleg.py`, T1 self-grep at every invocation. CC leg (E-9): full-from-scratch — own SO(3) quadrature/covariance, own eigen stack, own Born angular integrals, own mass-operator real-part route, own mapper — verify-then-build against the in-band dispatch hashes; **CC read #1 of Phase 3 is the blind verdict read of record.**

**8.2 Dispatch (P-4).** One self-contained file `G_CI1_CC_DISPATCH_INBAND.md` embedding byte-exact: this pre-registration (locked), the lock record, the T1 list, the sealed file (T1-scan-exempt embed), the input tensors, the chat Phase-1/2 checkpoints (consult-after-hashing), activation flags, and the blindness clause. Every embed re-extraction-verified byte-exact; sizes byte-labelled.

**8.3 Checkpoints (E8 J-discipline).** `ci1_phase0.json`, `ci1_phase1.json`, `ci1_phase2.json`, `ci1_phase3_cc_read1.json`, `ci1_phase3_chat_read<n>.json`, CC twins `ci1_phase<k>_cc.json`; each carries the md5s of its inputs, instrument, T1 list, and (Phase 3) the sealed file, plus byte-labelled sizes.

**8.4 Chat-leg blindness protections (H-16 lessons carried forward wholesale).** M-1 sealed rows parsed by structured fields, never echoed or interpolated into strings; M-2 the first-DIMENSIONLESS rule — every comparison is formed as a dimensionless ratio before any print; M-3 structured exceptions with raise-time masking; M-4 self-scan of every emitted string against T1 + the sealed rows' own token set before emission (adversarial synthetics exercised pre-read); M-5 catch-all masked abort; the terminal masked-diagnostic rule. Nine-suite pre-read gates on the chat mapper (schema, symbolic criterion, fallback, adversarial, forced-failure masking, identifier/sign guard, positivity, masked abort, census) all green before the chat read.

**8.5 Expectation pins.** Before the chat read, each leg pins its expected extraction/route divergences (the E3-7(a) pattern) into its checkpoint; C-CI-6 compares.

**8.6 Honesty ledger.** G-CI1.H-1 … sequential, both legs, never silently corrected; S9 counter-cross-check on any out-of-table miss; S9-lite for classification-only divergences.

---

## §9 — Blast radius (pre-declared), consequence routing, successors

**9.1 On P-CI-S-PRESERVING / -TIGHTENING.** CI-S survives; the ANNEX-CDEF-1 restatement stands single-channel; the radiative component of B-2 is discharged on W_Q3 with the computed residual; the polycrystal postulate remains R3 (a non-kill with a window is not a confirmation).

**9.2 On F-CI-S-STRUCT (expected).** CI-S retires as written; **the S2 sector is UNLOCATED in the banked substrate** — a named M.ONT gap. **PF-1 (sharpened blast radius, requires the author's acknowledgment):** the four G-POLY1 sealed anchors were evaluated under the reading "S2 propagates as the aggregate transverse acoustic wave"; F-IRR negates that reading, so **W_∪ becomes doubly conditional** — on the transverse-scale import (as banked) **and** on S2-in-channel — its numbers untouched, its status annotated at fold; under CI-W/EM-IN it is SUSPENDED from the intersection (reported alongside). The transverse estate (G-TSH1–4), G-POLY1's numerics and P-2 as a conditional statement, K-bookkeeping, Paper IIA §3–§4, the §2.91.F theorems T1–T5, §2.90, μ_n, and the gauge-paper §7.4 firewall are untouched. The ANNEX-CDEF-1 structural-pass restatement reverts to an explicit two-sector assumption (CI-W/EM-IN if WINDOWED; otherwise the pre-V4.71 named-assumption status).

**9.3 On CI-W/EM-IN-WINDOWED (expected class).** Banked as an EM-face window on d with per-arm edges; the c-referent stands as c_cone with EM in-channel; cone identity remains an assumption; the R-c composite/tensorial-variable route is the only in-framework path back to CI-S.

**9.4 Successors registered-unopened at fold.** **G-CI2** — matter-sector species universality (all knot species on one cone; Register-D mechanism set: Chadha–Nielsen / Sundrum / BPS / Hořava; requires knot-dispersion machinery). **R-c** — composite or tensorial ±2 carrier constructions (R3; own staging + author word). **CI-W/EM-OUT declaration item** (M.ONT-adjacent) if the author elects to revisit EM-in-channel. **c-referent repair** (the §3.4 flag) if EM-OUT is ever declared.

**9.5 Fold target.** §2.91.N candidate + one Part VI row + the W_∪ conditionality annotation on §2.91.M (additive) + G-CI2/R-c registration lines; V4.77-class; anchor-unique edits with reverse-splice byte verification; byte-labelled sizes; the fold script re-anchors to the canonical current at authorization.

---

## §10 — Eddington guard, T1 forbidden-string list, T4

**T4.** All Phase-0/1/2 files in substrate units and dimensionless x; no SI value anywhere outside the sealed mapper. The Phase-2 residual and attenuation curves are computed once, on the fixed grid, before any anchor is opened; nothing is re-tuned after a read (T3).

**T1 list `t1_forbidden_G_CI1.txt` (a separate file — draft `t1_forbidden_G_CI1_DRAFT.txt` accompanies this pre-registration; frozen at lock, md5 in the lock record; one regex per line; applied to every instrument and checkpoint of every phase, both legs; the sealed embed and the lock record are the two exempt embeds).** Contents by class: the inherited G-POLY1 class (distance units, frequency units, the spin-2-side event/catalogue/detector tokens, the linearized-gravity dialect acronym, the physical channel-speed value in every common spelling, SI speed and length words) plus the EM extension (band names other than "optical", source-class names, instrument/observatory names, EM energy and wavelength unit strings, the named photon-sector authors and source identifiers, the standard-candle and burst dialect tokens, the physical constants that would convert energy or wavelength to SI, and the ξ = ℓ_P value in every spelling). "optical" is deliberately absent — it is legitimate phonon vocabulary in Phase 1. Zero hits required at every invocation; a hit is a §5.5 halt. **This pre-registration is itself scanned against the draft list before presentation and must return zero hits (recorded in the Phase-0 checkpoint at lock).**

**Eddington disposition.** No sealed number is known to any instrument before Phase 3; the CC blind read precedes the chat read; the branch (CI-S vs CI-W) is fixed by Phase 1 before any anchor opens; D-6…D-8 foreclose vocabulary substitution; the ray-bracket exclusion uses the minimum over aggregate conventions; VOID never counts as PASS in the ledger; the priors of §6 are stated now.

---

## §11 — Non-claims and freeze

No Maxwell/gauge derivation (E-6). No construction of a ±2 carrier beyond inventory (E-4). No matter-sector universality discharge (E-3). No d derived; no SI floor; no magnitudes; no KC; no observable claimed — windows are import-conditional and revocable with the imports, exactly as W_∪. The polycrystal postulate stays R3 under every outcome. The longitudinal estate stays retired. **§2.52 Open 3 untouched, not advanced, not annotated. The G-2a-L1/§2.87.J fold remains RETARGETED pending its CC comparison; §2.87.J stays reserved.**

---

## §12 — Pre-lock flags (author's word required; each resolves by a one-line election in the lock record)

- **PF-1** Sharpened blast radius: W_∪ becomes doubly conditional on F-IRR firing; SUSPENDED under CI-W/EM-IN (§9.2). *Acknowledge / amend.*
- **PF-2** CI-W sub-branching: EM-IN is the pre-registered computable retreat; EM-OUT UNADJUDICATED-DEGENERATE (author declaration item, not decided in-gate); S2-IN-only as defined. *Confirm.*
- **PF-3** CI-V (vector-carrier reading) named-not-adopted; foreclosed by E-2; A-POL its would-be surface. *Confirm naming.*
- **PF-4** E-8 numbers as in §5 (τ_h 1e-12; θ₁/θ₂ 3%/10%; containment 1e-6; doubling 1e-8; comparison 1e-6; grid 10^{−8..8} half-decade; ε_T² ≤ 0.10; Im k/Re k ≤ 0.10; ε_T·x ≤ 1; x_G = 10; N_λ, N_dom, N_cell = 10; OOM ×10^{±1}; exponent 4.00 ± 0.02). *Confirm / amend.*
- **PF-5** Sealed census 12 rows as in §7 (ACHROM and BIR two sub-rows each; VLD and CONV rows). *Confirm.*
- **PF-6** Re-supply `poly_vrh_results.json` (200e7a8b) before Phase 2; fallback = ledger block + containment. *Confirm.*
- **PF-7** Re-supply pin record 621120e5 (Rayleigh assembly + Born validity); fallback = re-retrieval/re-pin at Phase-2 open; ray-regime attenuation VOID unless a verbatim prior-art form is pinned. *Confirm.*

---

## §13 — Lock procedure (on the author's freeze word)

1. Re-anchor: assert the current canonical md5 (V4.76 f539d10c or later); record it in the lock record.
2. Freeze this file byte-identical; md5 + byte size recorded; the lock record `G_CI1_LOCK_RECORD.md` carries the author's election text E-0…E-9 verbatim, the PF-1…PF-7 resolutions, the T1 list md5, and this file's md5.
3. Draft, hash, and seal `anchors_G_CI1_SEALED.md` (census 12); record its md5 in the lock record; UNOPENED thereafter until Phase 3.
4. Then, and only then, Phase 0 opens (§4).

*Pre-registration draft only. Not locked. Not executed. Written before any computation.*

<<<END G_CI1_EXECUTION_PREREGISTRATION.md>>>

## T1 FROZEN LIST (78 case-sensitive regex lines; self-referential embed — matches its own patterns by construction, hence exempt from the scan)
<<<EMBED t1_forbidden_G_CI1.txt 653a0b7447e68aa8a094e62337a24da3 1127 EXEMPT>>>
# G-CI1 T1 forbidden-string list — DRAFT (frozen at lock; md5 recorded in the lock record)
# One Python regex per line; lines beginning with '#' are comments. Case-sensitive.
# Applied by self-grep to every instrument file and checkpoint of every phase, both legs.
# Exempt embeds: anchors_G_CI1_SEALED.md and G_CI1_LOCK_RECORD.md only.
# --- inherited class (G-POLY1 lineage) ---
\bMpc\b
\bGpc\b
\bkpc\b
\bpc\b
\bHz\b
\b[kMGT]Hz\b
GW1
170817
170814
GWTC
LIGO
Virgo
KAGRA
\bLVK\b
\bSME\b
299792458
2\.99792458
2\.998e8
\b3e8\b
\bm/s\b
\bkm/s\b
\bmeters?\b
\bmetres?\b
# --- EM extension (band / source-class / instrument / unit / constant tokens) ---
\bradio\b
X-ray
x-ray
gamma-ray
γ-ray
\bVHE\b
\b[kMGT]eV\b
\beV\b
H\.E\.S\.S
\bHESS\b
\bMAGIC\b
VERITAS
\bFermi\b
\bLAT\b
\bCTA\b
LHAASO
\bHAWC\b
\bEBL\b
blazar
quasar
\bQSO\b
\bAGN\b
\bGRB\b
\bFRB\b
pulsar
magnetar
supernova
\bSNe?\b
\bIa\b
Kostel
Mewes
Aharonian
\b1ES\b
\bMk[nr]\b
\bPKS\b
Chandra
\bXMM\b
NuSTAR
\bSwift\b
INTEGRAL
\bnm\b
\bÅ\b
Angstrom
micron
\bμm\b
redshift
\bz\s*=\s*\d
6\.626
6\.62607
4\.1357
1\.054571
1\.602176
1\.616255
1\.616e-35
Planck length

<<<END t1_forbidden_G_CI1.txt>>>

## LOCK RECORD (T1-exempt embed)
<<<EMBED G_CI1_LOCK_RECORD.md a6adbb6ab69bcc6184b8fc2f6bcb9f5b 9851 EXEMPT>>>
# G_CI1_LOCK_RECORD.md — Lock record for Gate G-CI1 (the Q3(1) Carrier-Identity Claim)

**Lock executed:** August 17, 2026 (Pacific), 2026-08-18T00:21Z (container UTC). **Lock authority:** the author's explicit freeze word of August 17, 2026 (reproduced verbatim in §3). **This file is a T1-scan-EXEMPT embed** (one of exactly two: this lock record and `anchors_G_CI1_SEALED.md`), because it carries the author's election text verbatim, which contains observational-dialect tokens by design (the two-document convention of the pre-registration header).

## §1 — Lock chain (byte-anchored)

| Artifact | md5 | bytes | status |
|---|---|---|---|
| Base canonical `SQT_Master_Ledger_v4_76_CANONICAL.md` | `f539d10cb4f73c81e7d9fdbe7fa63714` | 1,432,221 | re-anchored at lock (§13.1 of the pre-registration): V4.76 is the current canonical; no later canonical exists |
| Staging memo `staging_memo_Q3_1_carrier_identity.md` | `ca6d891f51c425bd46ffbb1dee4e45f8` | 30,363 | APPROVED (author, August 17, 2026); not amended |
| Pre-registration `G_CI1_EXECUTION_PREREGISTRATION.md` | `6c480340658a54e9da5d3553a8890c46` | 36,793 | **LOCKED byte-identical to the reviewed draft** (the author's confirmed md5); its header text reads "DRAFT — NOT LOCKED" by construction of byte-identity; this record is the lock (the G-POLY1 / G-2a-S8 precedent) |
| T1 forbidden-string list `t1_forbidden_G_CI1.txt` | `653a0b7447e68aa8a094e62337a24da3` | 1,127 | **FROZEN byte-identical** to the reviewed draft `t1_forbidden_G_CI1_DRAFT.txt` (same md5); 78 case-sensitive regex lines; header text says DRAFT by construction of byte-identity |
| Sealed anchor file `anchors_G_CI1_SEALED.md` | `dd8fe2d364624750201ad9c9ffef575c` | 17,652 | **SEALED at lock** (second and final seal; the first seal 6cdf147d / 17,694 B superseded before any instrument touched it — G-CI1.H-3 below); census = 12 rows (4 TR + ACH-DIM + ACH-DISP + BIR-1 + BIR-2 + POL + DIFF + VLD + CONV); pipe-safe (10 separators per row, no pipe outside table rows), superscript-free (E3-6(a) semantics never engage); UNOPENED by any instrument before Phase 3; md5 + census asserted at every open |

**T1 self-scan of the pre-registration against the frozen list (case-sensitive, the declared discipline): 0 hits** — recorded also in `ci1_phase0.json`. Transparency note: a case-insensitive scan returns exactly one collision, the satellite token `INTEGRAL` against the ordinary mathematical word "integral" (pre-registration line 207); this is precisely why the list is declared case-sensitive; no change was made.

## §2 — Author's election directive (VERBATIM; the E-0…E-9 text of record)

> **Directive: Authorize Staging Memo and Elections for G-CI1**
> The staging memo is approved. The B-3 (helicity/irrep) burden discovery is a critical and correct structural catch. The CI-S vs CI-W differentiation is ratified.
> I authorize the following elections:
> * E-0: Gate name G-CI1 is adopted.
> * E-1: (a) Aggregate isotropized transverse acoustic channel as referent.
> * E-2: CI-S and CI-W definitions adopted and T3-immutable.
> * E-3: Scope restricted to radiative sectors; matter-sector routed to named successor.
> * E-4: Phase-1 R-b policy adopted (inventory only, no new model construction).
> * E-6: Gauge-paper firewall maintained.
> * E-7: Kernels {step, gem8}, hex primary + cubic labelled.
> * E-9: CC full-from-scratch; CC-blind-first for Phase-3 read.
> **For E-5 (Sealed-anchor roster):**
> Proceed with A-EM-TRANS, A-ACHROM, A-BIR-EM, A-POL, and A-DIFF. For the A-EM-TRANS ladder, include Radio, Optical, X-ray, and VHE γ-ray (e.g., H.E.S.S.) rungs to ensure maximum regime coverage.
> Draft the pre-registration (`G_CI1_EXECUTION_PREREGISTRATION.md`), including the exact thresholds and tolerances for E-8. Do not lock or execute Phase 0 until I explicitly authorize the freeze.

**Election E-8** is carried by the locked pre-registration §5 and confirmed by PF-4 below. **Dialect-label dictionary for the sealed roster** (the pre-registration uses abstract labels): TR-1 = the author's "Radio" rung (realized at seal as a low-frequency radio-galaxy detection at 150 MHz, redshift-anchored — the longest-wavelength band of the roster, chosen for maximum regime coverage at the long-wavelength end; the CMB monopole spectrum is carried by the ACH-DIM row instead); TR-2 = "Optical"; TR-3 = "X-ray"; TR-4 = "VHE γ-ray (e.g., H.E.S.S.)" (realized as the H.E.S.S. 1ES 1101-232 spectrum, per the author's example).

## §3 — Author's freeze directive and pre-lock-flag resolutions (VERBATIM)

> **Directive: Freeze G-CI1 Pre-registration and Authorize PF Resolutions**
> The T1 draft list md5 (`653a0b7447e68aa8a094e62337a24da3`) and the G_CI1_EXECUTION_PREREGISTRATION.md draft md5 (`6c480340658a54e9da5d3553a8890c46`) are confirmed.
> I explicitly AUTHORIZE the lock and FREEZE the pre-registration byte-identical to the reviewed text against V4.76.
> **Pre-lock Flag Resolutions (to be written verbatim into the lock record):**
> * PF-1 (Blast Radius): Acknowledged and amended as written. If F-IRR fires, W_∪ becomes doubly conditional; under CI-W/EM-IN it is SUSPENDED from the intersection.
> * PF-2 (CI-W Branching): Confirmed as written (EM-IN operative; EM-OUT author-declared; S2-IN defined).
> * PF-3 (CI-V Naming): Confirmed. CI-V is named-not-adopted and foreclosed by E-2.
> * PF-4 (E-8 Numbers): Confirmed as written (τ_h 1e-12, θ₁/θ₂ 3%/10%, containment 1e-6, Born exponent 4.00 ± 0.02, x_grid half-decade, etc.).
> * PF-5 (Census 12): Confirmed.
> * PF-6 (JSON Re-supply): Confirmed. I will re-supply `poly_vrh_results.json` `200e7a8b` before Phase 2.
> * PF-7 (Pin Record Re-supply): Confirmed. I will re-supply `621120e5` before Phase 2; fallback to verbatim re-retrieval.
> Execute the lock sequence:
> 1. Re-anchor to V4.76.
> 2. Mint `G_CI1_LOCK_RECORD.md`.
> 3. Draft, hash, and seal `anchors_G_CI1_SEALED.md` (census 12, T4-quarantined).
> 4. Open Phase 0.
> Report back with the lock hashes and the Phase 0 readiness status.

**Reading of PF-1 "acknowledged and amended as written":** the author's restatement is identical in content to the pre-registration §9.2 / §12 PF-1 text (doubly conditional on F-IRR firing; SUSPENDED from the intersection under CI-W/EM-IN); no textual amendment to the pre-registration was required or made (byte-identity preserved); the resolution is recorded here as ACKNOWLEDGED. PF-2, PF-3, PF-4, PF-5: CONFIRMED as written. PF-6, PF-7: CONFIRMED with the author's re-supply commitments before Phase 2; the pre-registered fallbacks stand.

## §4 — Elections in force (T3-immutable from this lock)

E-0 G-CI1; E-1(a) aggregate isotropized transverse acoustic channel; E-2 CI-S/CI-W definitions D-6/D-7 T3-immutable (D-8 CI-V named-not-adopted, PF-3); E-3 radiative sectors only, matter-sector successor G-CI2 named; E-4 R-b inventory only; E-5 roster A-EM-TRANS (TR-1…TR-4) + A-ACHROM (2) + A-BIR-EM (2) + A-POL + A-DIFF, sealed as census 12 with VLD + CONV; E-6 gauge-paper firewall; E-7 kernels {step, gem8}, hex primary + cubic labelled; E-8 §5 numbers as locked (PF-4); E-9 CC full-from-scratch, CC-blind-first Phase-3 read (CC read #1 = the blind read of record).

## §5 — Sealing statement and honesty ledger opening

**Sealed-file provenance.** Every quantity in `anchors_G_CI1_SEALED.md` was retrieved from its named published source at seal time and transcribed; four in-row items that were not verbatim-retrieved from the anchor source (a nominal last-scattering redshift, a representative optical filter wavelength, two instrument band brackets) are marked [RECALLED-FLAG] inside the sealed params and each carries a pre-declared conservative two-reading rule (exclusion asserted only where both readings exclude). No sealed quantity was evaluated against any curve at seal time; the Phase-1/2 instruments are pre-registered in closed form and consume no anchor.

**G-CI1.H-1 (process disclosure, chat leg, at lock).** The chat leg drafted the sealed file at lock, as the procedure requires (§13.3); the chat leg's Phase-3 blindness is therefore procedural — enforced by T1 (tokens), T4 (no SI outside the sealed file and mapper), the M-1…M-5 masking discipline, the pre-registered closed-form Phase-1/2 instruments, and the E-9 CC-blind-first architecture in which CC read #1 is the verdict read of record — not an information barrier. This is the same disclosure class as G-POLY1.H-8; recorded at lock, before any computation.

**G-CI1.H-3 (re-seal disclosure, at lock, before Phase 1).** The first sealed file (md5 6cdf147d8b96f89dc3c6c45b321aa66c, 17,694 B) realized TR-1 as the CMB monopole (microwave/mm-wave). On seal review — before Phase 1 opened and before any instrument had opened the file — TR-1 was re-realized as a 150 MHz radio-galaxy detection (a longer wavelength by two decades, redshift-anchored) to honor the author's E-5 wording "Radio" and the maximum-regime-coverage instruction; the CMB monopole spectrum remains the ACH-DIM row. The file was re-sealed (md5 dd8fe2d364624750201ad9c9ffef575c, 17,652 B; census 12 unchanged; structural checks re-run) and Phase 0 was re-run against the final seal. The superseded seal is not consumed anywhere.

**G-CI1.H-2 (hygiene note, at lock).** The frozen T1 list and the locked pre-registration carry the word "DRAFT" in their headers by construction of byte-identity with the author-confirmed hashes; the lock status is established by this record, not by the files' header strings.

## §6 — What opens now

Phase 0 (definitions, checklist, final A0 pass, sealed md5/census assert, T1 zero hits) opens on this lock and closes to `ci1_phase0.json`. Phase 1 opens only after Phase 0 closes with A0 NOT TRIGGERED. Nothing else changes: §2.52 Open 3 untouched; §2.87.J reserved; OP-2.58.2d and P-LEX-1 standing.

<<<END G_CI1_LOCK_RECORD.md>>>

## LOCK RECORD ADDENDUM 1 (lock-record class, T1-exempt embed)
<<<EMBED G_CI1_LOCK_RECORD_ADDENDUM_1.md e5029ae86cd43dcb343ebb4e872f856b 5203 EXEMPT>>>
# G_CI1_LOCK_RECORD_ADDENDUM_1.md — Addendum 1 to the G-CI1 lock record (append-only; the lock record `a6adbb6ab69bcc6184b8fc2f6bcb9f5b` is unmodified)

**Date:** August 18–19, 2026. **Base lock:** pre-registration `6c480340` LOCKED; T1 list `653a0b74` FROZEN; sealed file `dd8fe2d3` SEALED (census 12, UNOPENED); lock record `a6adbb6a`; Phase 0 CLOSED (`ci1_phase0.json` `b0498568`, A0 NOT TRIGGERED). This addendum is a T1-scan-EXEMPT embed of the lock-record class (it carries the author's directive text verbatim).

## A1.1 — PF-6 / PF-7 discharge (X-1 byte provenance)
`poly_vrh_results.json` md5 `200e7a8b775577564369c6924d38a84c` (2,767 B) — PASS. `G_POLY1_PIN_RECORD.md` md5 `621120e50d395beea2e914d54c929600` (10,759 B) — PASS. Verification checkpoint `ci1_resupply_verify.json` md5 `d99d21b2bc15d9f0075ee9d00e6c69d8` (1,835 B). Neither fallback invoked. Author acknowledgment: "The PF-6 and PF-7 re-supply verifications are confirmed. The byte-exact provenance is acknowledged."

## A1.2 — Author's directive (VERBATIM)

> **Directive: Acknowledge Resupply and Authorize Phase 1 (I-1 Irrep/Helicity Audit)**
> The PF-6 and PF-7 re-supply verifications are confirmed. The byte-exact provenance is acknowledged.
> For the Phase 2 items:
> 1. I authorize a specific T1-exemption line for the `G_POLY1_PIN_RECORD.md` embed in the CC dispatch due to the legacy Aluminum benchmark token.
> 2. I elect to leave the ray-regime attenuation VOID by default. We will not pin a new prior-art form; widening the window is the conservative and honest path.
> I authorize the execution of Phase 1 (I-1 irrep/helicity audit) on the chat leg.
> 1. Execute the R-a machine check to verify the helicity content of the transverse displacement channel and its derived strain/stress fields.
> 2. Execute the R-b inventory across the banked G-TSH4 and G-INT1 sectors for any ±2 content degenerate with the acoustic cone.
> 3. Form the candidate set K and render the F-IRR decision.
> 4. Record all findings and the F-IRR verdict in `ci1_phase1.json`.
> Report back with the Phase 1 checkpoint and the F-IRR verdict.

## A1.3 — Elections recorded (T3-immutable from this addendum)
- **E-10 (dispatch embed exemption):** the CC dispatch `G_CI1_CC_DISPATCH_INBAND.md` carries the frozen `G_POLY1_PIN_RECORD.md` byte-exact as a **third declared T1-scan-exempt embed** (justification: frozen upstream input, byte-exact by requirement; its single hit is the SI velocity-unit token of the He-2 aluminium benchmark control line, source-marked "SI units in this control only", not consumed by G-CI1). All other dispatch content remains T1-scanned.
- **E-11 (ray-regime attenuation):** VOID by default (§5.4); no new prior-art form is pinned; a VOID can only widen a window.

## A1.4 — Phase 1 (chat leg) closure
Instrument `g_ci1_phase1_irrep_chatleg.py` md5 `b5715bf62189c9f2105e451e396c21ce` (23,236 B); checkpoint `ci1_phase1.json` md5 `9d8e40b827f68d354335c2a147420636` (218,006 B); T1 zero hits on both; inputs: `poly_vrh_results.json` (byte-verified) as the E-7 tensors; 35 directions (13 lattice incl. axial/basal/oblique, 2 hex in-plane, 20 Fibonacci); θ ∈ {0.1, 2π/7, 2π/5}; τ_h = 1e-12. **F-IRR: FIRES (K = ∅) — CI-S FALSIFIED-STRUCTURAL; the CI-W arm activates; CI-W/EM-IN operative (PF-2); W_∪ doubly conditional and SUSPENDED from the Phase-3 intersection (PF-1, fold-time annotation).**

## A1.5 — Honesty ledger continued
**G-CI1.H-4 (interpretive item, author veto standing; the G-TSH3 D-3 pattern).** The R-a machine check confirms the pre-registered priors for the D-1 channel and for the strain of every plane wave (the ±2 strain component vanishes identically; machine max 4.6e-16) and for the isotropic aggregate stress (5e-16), but the derived STRESS of single-crystal qT branches carries anisotropy-induced ±2 kinematic components at generic directions (nonzero on 58/70 hex and 49/70 cubic branch-directions; max fraction 0.27–0.47 of the stress norm; zero at the axial and pure-mode directions). The F-IRR verdict of record is rendered under the D-4 first-clause reading (a branch's helicity content = the eigenphase multiset of its mode's polarization/orbital data; derived-field eigenphases are kinematic labels), consistent with D-6's "excitation". Under the alternative reading (derived-stress labels counted as branch content) the transverse pair — DEGENERATE by definition as the channel — would make K non-empty; that reading would also make every anisotropic elastic medium trivially "host ±2", emptying the B-3 burden. **Ratification of the reading of record is requested from the author; the verdict is T3-immutable only after ratification.**
**G-CI1.H-5 (process).** Two chat-side serializer defects (numpy scalar types) fired at first execution and were fixed before any output was consumed; no numerical content affected; recorded.

## A1.6 — What opens next
Phase 2 (I-2 regime map + I-3 residual ledger; containment 2.1 opens the phase) is branch-independent and opens on the author's word; the E-11 VOID election and the E-10 exemption apply at Phase-2 open. Phase 3 (sealed mapper, CC-blind-first) is steered by the ratified F-IRR verdict.

<<<END G_CI1_LOCK_RECORD_ADDENDUM_1.md>>>

## LOCK RECORD ADDENDUM 2 (lock-record class, T1-exempt embed)
<<<EMBED G_CI1_LOCK_RECORD_ADDENDUM_2.md 92672d5a72cf2efce8865d2a4ca3fb6c 8443 EXEMPT>>>
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

<<<END G_CI1_LOCK_RECORD_ADDENDUM_2.md>>>

## LOCK RECORD ADDENDUM 3 (lock-record class, T1-exempt embed; H-8 RATIFIED / E-12; release authorization)
<<<EMBED G_CI1_LOCK_RECORD_ADDENDUM_3.md 4c0b52c6ab10b5f075ad49abad137020 4286 EXEMPT>>>
# G_CI1_LOCK_RECORD_ADDENDUM_3.md — Addendum 3 to the G-CI1 lock record (append-only; base `a6adbb6a`, Addendum 1 `e5029ae8`, Addendum 2 `92672d5a` unmodified)

**Date:** August 19, 2026. **Scope:** the author's ratification of H-8, acknowledgment of H-9, confirmations of record, and the release authorization for the blind CC dispatch. Lock-record class (T1-exempt embed by the two-document convention).

## A3.1 — Author's directive (VERBATIM)
> **Directive: Ratify H-8, Acknowledge H-9, and Authorize CC Dispatch**
> The Phase 2 checkpoint (`ci1_phase2.json`) and the successful containment checks are confirmed.
> 1. I explicitly RATIFY the H-8 route ruling: the DIRECT principal-value quadrature is the I-3 quantity of record for C-CI-3. The Kramers-Kronig transform is diagnostic only.
> 2. I ACKNOWLEDGE the H-9 T1-hygiene re-serialization and the 11-digit float constraint.
> 3. The ray-bracket limits and x_S validities are confirmed as recorded.
> I authorize the P-4 CC dispatch.
> 1. Release `G_CI1_CC_DISPATCH_INBAND.md` to the blind CC leg.
> 2. CC must execute Phases 0–3 from scratch. CC Read #1 is the verdict read of record.
> 3. A-DIFF runs last.
> 4. Report back when the CC checkpoint is returned, placed in the workspace, and hashed. Do not run Chat Read #2 until I authorize it.

## A3.2 — Elections / rulings now T3-immutable
- **E-12 (H-8 ratified):** the I-3 quantity of record for C-CI-3 is the real part of the second-order mass operator by DIRECT principal-value quadrature over the intermediate wavevector, on shell, static value subtracted (Δ_ch := −[Re m̃_T(x) − Re m̃_T(0)]/2; c_cone/V_T0 = 1/(1 + Re m̃_T(0)/2)). The Kramers–Kronig transform of α is diagnostic only and is never compared at the 1e-6 tolerance.
- **H-9 acknowledged:** checkpoint floats serialized at a fixed 11 significant digits (all comparison tolerances ≥ 1e-8 relative) with an automatic T1 rescan; the Phase-2 production run was repeated from scratch under this rule.
- **Confirmed as recorded:** the ray-bracket limits Δ_geo^X (Addendum 2 §A2.2) and the validity edges x_S = 10 / 3.162 / 3.162 / 3.162 (hex:step / hex:gem8 / cubic:step / cubic:gem8), x_G = 10.

## A3.3 — Dispatch release
The released dispatch is `G_CI1_CC_DISPATCH_INBAND.md` rebuilt to embed this Addendum 3 (so the CC leg sees the H-8 ruling as ratified, not pending); the pre-release build `c80a03a1558e6943b38b869120201ad5` (104,549 B) is superseded by the released build whose md5 and byte count are recorded in `G_CI1_CC_DISPATCH_MANIFEST.json` and in the chat report of release. Every embed extracts back byte-exact (verified); the non-exempt body is T1-clean; the four declared T1-exempt embeds are the sealed file, the lock-record class (record + Addenda 1–3), the pin record (E-10), and the frozen T1 list itself (self-referential).

## A3.4 — Protocol in force until the CC return
- CC executes Phases 0–3 from scratch; CC Read #1 of the sealed file is the verdict read of record (E-9); A-DIFF runs last; CC reports checkpoints (`ci1_phase0_cc.json`, `ci1_phase1_cc.json`, `ci1_phase2_cc.json`, `ci1_phase3_cc.json`) with md5 + bytes and zero T1 hits.
- **Chat Read #2 is EMBARGOED** until the author's explicit authorization: the chat leg does not open the sealed file, does not run any Phase-3 mapper, and does not pre-compute any arm, before that word. The chat leg's pre-return work is limited to receiving and byte-hashing the returned CC artifacts and preparing the C-CI-1…3 comparison of Phases 1–2 (anchor-free).
- On return: X-1 byte-hash of each CC artifact into the workspace; C-CI-1 (Phase 1 R-a multisets, R-b table, F-IRR), C-CI-2 (containment values, Q^(d)/Q^(a) on the 33-point grid, ε_T, x_S; ≤ 1e-6 relative), C-CI-3 (direct-route scaled residual, D₂, plateau, Δ_geo^X; ≤ 1e-6 relative; VOID-NUM points compared as VOID); C-CI-4 waits for Chat Read #2 (interval-set equality 1e-6). Any miss → S9 (both legs re-derive from the pre-registration text; no leg copies the other).

## A3.5 — Standing
§2.52 Open 3 frozen; §2.87.J reserved; OP-2.58.2d and P-LEX-1 standing. Fold target (author-authorized only, after the comparison and Chat Read #2): §2.91.N + Part VI row + the W_∪ conditionality annotation on §2.91.M (V4.77-class).

<<<END G_CI1_LOCK_RECORD_ADDENDUM_3.md>>>

## INPUT: poly_vrh_results.json (PF-6, byte-verified)
<<<EMBED poly_vrh_results.json 200e7a8b775577564369c6924d38a84c 2767 SCANNED>>>
{
 "gem8_fcc_iso": {
  "A": 946.2397864450644,
  "lin": -214.4531034305213,
  "base_res": 4.7100744185220225e-09,
  "seconds": 38.00324010848999
 },
 "vrh": {
  "controls": {
   "cubic_closed_form_maxerr": 4.440892098500626e-16,
   "iso_null": "PASS"
  },
  "hex:step": {
   "label": "TRUE-OPTIMUM (V4.72 R1 two-leg)",
   "C_over_rho": {
    "C11": 238.4183,
    "C12": 108.5389,
    "C13": 57.4751,
    "C33": 287.6688,
    "C44": 60.0308,
    "C66": 64.9223
   },
   "K_VRH": 134.609,
   "G_V": 73.065,
   "G_R": 68.697,
   "G_VRH": 70.881,
   "VR_spread_pct": 6.16,
   "AU": 0.3179,
   "vT_V": 8.5478,
   "vT_R": 8.2883,
   "vT_VRH": 8.4191,
   "vT_halfwidth_pct": 1.54,
   "single_crystal_input": {
    "mean": 8.472742664753259,
    "std_pct": 9.164259025458835,
    "maxdev_pct": 19.105382411223452
   }
  },
  "hex:gem8": {
   "label": "TRUE-OPTIMUM (V4.72 R1 two-leg)",
   "C_over_rho": {
    "C11": 377.5438,
    "C12": 200.2076,
    "C13": 111.0018,
    "C33": 467.7554,
    "C44": 84.8245,
    "C66": 88.6835
   },
   "K_VRH": 229.696,
   "G_V": 105.042,
   "G_R": 96.63,
   "G_VRH": 100.836,
   "VR_spread_pct": 8.34,
   "AU": 0.4352,
   "vT_V": 10.249,
   "vT_R": 9.8301,
   "vT_VRH": 10.0417,
   "vT_halfwidth_pct": 2.09,
   "single_crystal_input": {
    "mean": 10.120315551687215,
    "std_pct": 10.906419350629072,
    "maxdev_pct": 22.59028052217178
   }
  },
  "cubic:step": {
   "label": "polished-at-FROZEN geometry (labelled)",
   "C_over_rho": {
    "C44": 85.2934,
    "C12": 99.349,
    "C11": 172.7994
   },
   "K_VRH": 123.832,
   "G_V": 65.866,
   "G_R": 55.784,
   "G_VRH": 60.825,
   "VR_spread_pct": 16.58,
   "AU": 0.9037,
   "vT_V": 8.1158,
   "vT_R": 7.4689,
   "vT_VRH": 7.799,
   "vT_halfwidth_pct": 4.15,
   "single_crystal_input": {
    "mean": 7.97359836526451,
    "std_pct": 13.113372264449117,
    "maxdev_pct": 23.995868277249034
   }
  },
  "cubic:gem8": {
   "label": "polished-at-FROZEN geometry (labelled; iso measured this session)",
   "C_over_rho": {
    "C44": 131.5436,
    "C12": 179.3756,
    "C11": 272.0753
   },
   "K_VRH": 210.276,
   "G_V": 97.466,
   "G_R": 75.808,
   "G_VRH": 86.637,
   "VR_spread_pct": 25.0,
   "AU": 1.4285,
   "vT_V": 9.8725,
   "vT_R": 8.7068,
   "vT_VRH": 9.3079,
   "vT_halfwidth_pct": 6.26,
   "single_crystal_input": {
    "mean": 9.63705464398007,
    "std_pct": 15.808320696928124,
    "maxdev_pct": 29.351684168073366
   }
  },
  "mixture:step": {
   "f_hcp -> vT": {
    "0.0": 7.799,
    "0.25": 7.9499,
    "0.5": 8.1032,
    "0.75": 8.2594,
    "1.0": 8.4191
   },
   "phase_span_pct": 7.65
  },
  "mixture:gem8": {
   "f_hcp -> vT": {
    "0.0": 9.3079,
    "0.25": 9.4864,
    "0.5": 9.6679,
    "0.75": 9.8527,
    "1.0": 10.0417
   },
   "phase_span_pct": 7.59
  }
 }
}
<<<END poly_vrh_results.json>>>

## INPUT: G_POLY1_PIN_RECORD.md (PF-7, byte-verified; E-10 T1-exempt embed — one SI-control token in the He-2 benchmark line)
<<<EMBED G_POLY1_PIN_RECORD.md 621120e50d395beea2e914d54c929600 10759 EXEMPT>>>
# G-POLY1 PIN RECORD — E3-PIN-COMPLETE + HS-PIN

**Locked under:** exec prereg `dab462d2e133d0962c512a34bb7bc635`; staging memo `68623d68…`; base V4.73 `e48f5c52…`. Supplements E3-PIN v1 (He, arXiv:1706.09137). Transcription-before-evaluation: nothing below was consumed before being written here.

## E3-PIN-COMPLETE — source: Roy & Kube, J. Mech. Phys. Solids 203 (2025) 106237 (open access, NSF-PAR 10623592). FOSA sector ≡ Weaver JMPS 38, 55 (1990) ≡ Stanke–Kino JASA 75, 665 (1984) (equivalence per the source §1, §4.1, Fig. 1).

Transcribed, with source equation numbers:
- **(12)** ⟨δC(x₁)δC(x₂)⟩ = Ξ·η(x₁,x₂); **(13)/(A.1)** Ξ = ⟨C⊗C⟩ − ⟨C⟩⊗⟨C⟩, orientation average over SO(3), untextured.
- **(14)** C_ijkl = c₁₂δ_ij δ_kl + c₄₄(δ_ik δ_jl + δ_il δ_jk) + ν Σₙ a_in a_jn a_kn a_ln, **ν ≡ c₁₁ − c₁₂ − 2c₄₄**.
- **(15)** ⟨aaaa⟩ = (1/5)(δδ+δδ+δδ); reference medium c⁰₁₂ = c₁₂+ν/5, c⁰₄₄ = c₄₄+ν/5, c⁰₁₁ = c⁰₁₂+2c⁰₄₄; ρV²_L0 = c₁₂+2c₄₄+3ν/5, ρV²_T0 = c₄₄+ν/5 (= G_Voigt).
- **(17)–(18)** η(r) = e^(−r/a); η̃(q) = a³/(π²(1+q²a²)²) [(2π)⁻³ FT convention; He Eq. (71)'s 8πa³ form is the same object × (2π)³ — convention reconciled here, no conflict].
- **(A.3)–(A.4)** Ξ = a·T_A + b·T_B + c·T_C with **a = 2ν²/1575, b = −ν²/630, c = ν²/180**; T_A = the 9 latin-latin × greek-greek delta pairings; T_B = the 24 latin↔greek perfect matchings; T_C = the 72 mixed pairings (one LL + one GG + two LG). [(A.5)–(A.7) descriptive forms.]
- **(3), (30), (61)–(63)** FOSA self-energy; vertex ∇_j(δc_ijkl ∇_l u_k); slot roles pol/outer-grad/propagator/inner-grad (assignment immaterial under the full elasticity symmetry of δC — noted, and moot for cubic where δC is totally symmetric).
- **(41), (45)–(48)** dyadic propagator split; Im g₀M(s) = −π δ(s−k_M0)/(2ρV²_M0 k_M0).
- **(49)–(58)** dispersion k² = k²₀[1−m̃]⁻¹; α = Im k; m̃ scaled per (51)–(52).
- **(69) A-scalar anchor (clean):** A(θ) = (ν²/525)(3+cos²θ)² — **mandatory machine-reproduction falsifier** for the contraction machinery. Independently hand-verified at θ=0: A(0) = ν²·Var(Σnᵢ⁴) with Var = 41/105 − 9/25 = 16/525 ⇒ 16ν²/525 ✓. The retrieved B/C digit strings were corrupted in transport and are **NOT consumed**; every contraction is machine-computed from the pinned Ξ, with the A-anchor as the gate.
- **(81)–(82)** ε_L = √(4ν²/525)/c⁰₁₁, ε_T = √(3ν²/700)/c⁰₄₄ — recomputed as controls (Born validity: ε² ≪ 1).

**Convention resolutions (E2-witness class, logged pre-evaluation):** (i) overall self-energy sign fixed by Im k_M ≥ 0 (physical attenuation); (ii) the scattering theory's reference medium is the **Voigt** average ⟨C⟩ (source-pinned) — role-distinct from the E4 **Hill** verdict speeds; no collision: Q_T is a property of the pinned scattering theory, verdict propagation speeds remain Hill.

**Hexagonal arm (declared generalization route):** Ξ_hex = ⟨C⊗C⟩ − ⟨C⟩⊗⟨C⟩ by exact-degree SO(3) quadrature (zyz Euler: Gauss–Legendre in cosβ, n=10; uniform α,γ grids, n=12; integrand band-limit 8 — quadrature exact with margin), **validated to machine precision against the pinned cubic closed form before any hexagonal use**; the pinned machinery (12)–(13), (61)–(63), (41)–(58) is symmetry-agnostic and applied unchanged. The paywalled hexagonal closed forms (JASA 143, 219 (2018) line) are not consumed. Falsifiers: cubic closed-form reproduction; isotropic-input null Ξ ≡ 0.

**Rayleigh assembly (machine, from pinned pieces only):** α_P·a = Q_P·(k_P0 a)⁴ with
Q_P = Σ_{M∈{L,T}} (V_P0/V_M0)³ / (2 V²_P0 V²_M0) · ∫₋₁¹ Φ_PM(μ) dμ, ρ = 1,
Φ_PM(μ) = Ξ contracted with [ext-pol_P ⊗ p̂p̂ ⊗ dyad_M(ŝ) ⊗ ŝŝ] on both vertices (P-pol: p̂p̂ for L, (δ−p̂p̂)/2 for T; M-dyad: ŝŝ for L, δ−ŝŝ for T), μ = p̂·ŝ.
Cross-checked in-instrument against the finite-η̃ evaluation: exponent-4 fit and prefactor→Q_P agreement are falsifiers.

## HS-PIN — source: Zemlyakov & Chugunov, arXiv:2507.12266 (open access)

**CUBIC — COMPLETE.** Eqs. (9)–(10), verbatim:
μ_HS⁽¹⁾ = (c₁₁−c₁₂)/2 + 3·[ 10/(2c₄₄−c₁₁+c₁₂) + 24(K+c₁₁−c₁₂) / (5(c₁₁−c₁₂)(3K+2c₁₁−2c₁₂)) ]⁻¹
μ_HS⁽²⁾ = c₄₄ + [ 5/(c₁₁−c₁₂−2c₄₄) + 9(K+2c₄₄) / (5c₄₄(3K+4c₄₄)) ]⁻¹
with K = (c₁₁+2c₁₂)/3 (exact for cubic). Role: c₄₄ > (c₁₁−c₁₂)/2 ⇒ (1) = lower, (2) = upper — the case for both cubic configs here (Zener > 1). K≫c limit forms Eqs. (11)–(12); **implementation control** = the source's Table I bcc Coulomb-crystal row (c₄₄ = 0.1828, c₁₁−c₁₂ = 0.0490 → VR 0.0510/0.1195, HS 0.0712/0.1028), hand-verified against (11)–(12) to 4 digits pre-coding. Source Eqs. (4)–(8) independently re-confirm the Phase-0a cubic VRH transcription.

**HEXAGONAL — PENDING.** Named transcription sources: Berryman, JMPS 53, 2141 (2005); Peselnick–Meister (1965); Watt–Peselnick, JAP 51, 1525 (1980); Kube–Argüelles, Comput. Geosci. 95, 118 (2016) (iterative any-symmetry scheme). Obligation: transcribe-and-execute before Phase 3 (E4 band completeness). VR bounds stand in for hexagonal configs until pinned. No from-memory hexagonal HS coefficients are used anywhere.

---
# SUPPLEMENT (Aug 4, 2026 session) — cross-source redundancy + hexagonal HS upgrade

## S1. E3 cross-source: He, arXiv:1710.03828 (He-2; fetched in full this session)
Same FOSA/SK-Weaver operator class, stated for **arbitrary crystal symmetry** ("we neglect the unique symmetry of different types of crystals, and treat them as generally anisotropic materials" — Appendix). Serves as an independent redundancy pin for the CC leg; the chat-leg instrument consumes the Roy–Kube assembly above.
- Covariance = SO(3) Haar average, normalized measure (8π²)⁻¹ sinθ dφ∧dθ∧dψ — Eqs. (28)–(29), (33); Euler convention Q = R(ψ)R(θ)R(φ), ranges [0,2π)×[0,π]×[0,2π) — (A2), (A7)–(A8).
- SAF P(r) = e^(−r/a), P̃(k) = 8πa³/(1+k²a²)² — (30)–(31) ["a … generally considered as the average radius of the grains"]; dimensionless ᾱ = α·d, K̄₀ = k₀·d with **d = 2a** — (51)–(52). [Same object as Roy–Kube (17)–(18) × (2π)³ — reconciliation already logged above.]
- Transverse dispersion **M₁₁M₈₈ − M₁₈² = 0** — Eq. (50); M₁₁ = μ(k²−k_T²) − K₄₄k², M₁₈ = −K₄₄ik — (46a);
  **M₈₈ = K₄₄ − [⟨Ξ₁₅²⟩+⟨Ξ₂₅²⟩]Σ₄₄ − 2⟨Ξ₁₅Ξ₂₅⟩Σ₄₅ − 2[⟨Ξ₁₅Ξ₃₅⟩+⟨Ξ₂₅Ξ₃₅⟩]Σ₆₆-class per (46i) verbatim: … − ⟨Ξ₃₅²⟩Σ₆₆ − [⟨Ξ₄₅²⟩+⟨Ξ₅₅²⟩]Σ₇₇ − ⟨Ξ₅₆²⟩Σ₉₉** — (46i); pinned transverse Voigt-pair set **{15,25,35,45,55,56}**; M₂₂=M₁₁, M₂₇=M₁₈ — (46j); Σ₅₅=Σ₄₄, Σ₅₆=Σ₄₆, Σ₈₈=Σ₇₇ — (48e).
- K₁₁ = 3(λ+6μ)(λ+2μ)/(3λ+8μ), K₁₂ = 3(λ+μ)(λ+2μ)/(3λ+8μ), K₄₄ = 15(λ+2μ)μ/[2(3λ+8μ)] — (47); singularity constants S₁₁₁₁ = (2λ+7μ)/[15μ(λ+2μ)], S₁₂₂₁ = −(λ+μ)/[15μ(λ+2μ)], S₂₂₃₃ = (3λ+8μ)/[30μ(λ+2μ)] — (14)–(17); Σ-kernels (48a)–(48d) as Σ_ab = S-const − (8π³)⁻¹∫ s_i s_j G̃_ij(s)P̃(k−s)d³s.
- Ξ = Π[I+SΠ]⁻¹ — (25) (Born limit Ξ→δc, the E3-elected weak-fluctuation class); Voigt reference λ̄,μ̄ — (54); ε = |c₁₁−c₁₂−2c₄₄|/c₁₁⁰ — (53).
- **Benchmark hook (Tables 1–2):** Al C₁₁=103.4, C₁₂=57.1, C₄₄=28.6 GPa, ρ=2700 → λ̄=54.92, μ̄=26.42 GPa, V̄_T=3128.13, V̄_L=6317.52 m/s. Instrument must reproduce from (54) (SI units in this control only).

## S2. HS-PIN hexagonal — UPGRADE (Berryman SEP-125 appendix, node10 + node11, fetched verbatim this session)
Lineage: Peselnick–Meister JAP 36, 2879 (1965); Watt–Peselnick JAP 51, 1525 (1980); product formulas Berryman 2004b; journal statement Berryman JMPS 53, 2141 (2005).
**Machinery (node10):** (22) K_V = [2(C₁₁+C₁₂)+4C₁₃+C₃₃]/9; (23) G_V = (1/5)(G_eff^v + 2C₄₄ + 2C₆₆); (24) **G_eff^v = (C₁₁+C₃₃−2C₁₃−C₆₆)/3**; (25) 1/(K_R−C₁₃) = 1/(C₁₁−C₆₆−C₁₃) + 1/(C₃₃−C₁₃); (26) G_R = [(1/5)(1/G_eff^r + 2/C₄₄ + 2/C₆₆)]⁻¹; product formulas **3K_R G_eff^v = 3K_V G_eff^r = ω₊ω₋/2 = C₃₃(C₁₁−C₆₆)−C₁₃²** ⇒ G_eff^r = K_R G_eff^v/K_V.
**PMW/HS bounds (node11):** (27) **K_HS^± = K_V(G_eff^r + ζ±)/(G_eff^v + ζ±)**; (28) ζ± = (G±/6)(9K±+8G±)/(K±+2G±); (29) K± = K_V(G_eff^r−G±)/(G_eff^v−G±); (30) 0 ≤ G₋ ≤ min(C₄₄, G_eff^r, C₆₆); (31) max(C₄₄, G_eff^v, C₆₆) ≤ G₊ ≤ ∞; (33) α± = −1/(K±+4G±/3), β± = 2α±/15 − 1/(5G±).
**(32) shear bounds: 1/(G_hex^± + ζ±) = (1/5)[⟨FIRST TERM ELIDED in source rendering⟩ + 2/(C₄₄+ζ±) + 2/(C₆₆+ζ±)] — NOT reconstructed.** α±, β± enter within the elided fragment. Watt–Peselnick note (verbatim): a later condition permits C₄₄ to be replaced in some circumstances by G_eff^r.
**Consistency identity (derived-class, labeled):** at ζ = 0 with first term 1/G_eff^r, (32) reproduces (26) exactly; and 3K_V G_eff^r = C₃₃(C₁₁−C₆₆)−C₁₃² = ½[(C₁₁+C₁₂)C₃₃−2C₁₃²] — identical to the independently pinned arXiv:1606.03700 G_R. Two pinned hex-Reuss statements = one formula.
**Status upgrade:** hex **K_HS^± COMPLETE** ((27)–(31), evaluable now for step:AB); hex **G_HS^± PENDING-verbatim** (one elided term; completion source: Berryman JMPS 53, 2141 (2005) or PRB 85, 094204 appendix — OSTI purl/1082188 returned 502 this session; obligation before Phase 3; V/R shear bracket stands in, disclosed).

## S3. Consolidated status
- **E3-PIN-COMPLETE: COMPLETE** — primary Roy–Kube assembly (above) + He-2 redundancy (S1); both arms covered; A(θ)-anchor is the hard machine gate; corrupted B/C digit strings remain un-consumed.
- **HS-PIN:** cubic COMPLETE (Eqs. (9)–(10) + role rule + Table-I control); hex K COMPLETE (S2); hex G PENDING-verbatim (S2).
- **Input map for Phase 0b/1 this leg:** step:AB hex → 1a+1b full, K_HS^± now, G_HS pending; gem8:FCC cubic → 1a+1b full, μ_HS full; step:FCC cubic → 1a full (K-free), 1b T→T partial + full-Q_T BLOCKED on K (c₁₁,c₁₂ input-gap; the K-free simplified HS forms (11)–(12) are out of regime and are not used); gem8:AB hex → INPUT-GAP.

<<<END G_POLY1_PIN_RECORD.md>>>

## SEALED ANCHOR FILE — UNOPENED UNTIL PHASE 3 (T1-exempt embed; md5-assert + census-assert at open)
<<<EMBED anchors_G_CI1_SEALED.md dd8fe2d364624750201ad9c9ffef575c 17652 EXEMPT>>>
# anchors_G_CI1_SEALED.md — G-CI1 sealed anchor file (SEALED AT LOCK, August 17, 2026)

STATUS: SEALED. CENSUS = 12 rows (4 x A-EM-TRANS + 2 x A-ACHROM + 2 x A-BIR-EM + 1 x A-POL + 1 x A-DIFF + 1 x VLD + 1 x CONV). T1-SCAN-EXEMPT EMBED (one of the two exempt embeds; the other is G_CI1_LOCK_RECORD.md). UNOPENED by any instrument before Phase 3 (pre-registration §4, Phase 3.1); md5-asserted at every open; census asserted at every open. Rows are parsed by structured fields and NEVER echoed (M-1); every comparison is formed dimensionless before any print (M-2). H-16 lesson applied: the pipe character is the field separator ONLY — no absolute-value bars anywhere in this file; abs() is spelled out. All numerics in params are plain ASCII e-notation; no superscript glyphs appear in any field (E3-6(a) frozen-ASCII semantics therefore never engage; ascii_flag = CLEAN on every row).

Row schema (9 fields, in order): id / class / pattern / dialect_ref / anchor_text / params / Caveat / Binding / ascii_flag
Read order (Phase 3.1): TR-1, TR-2, TR-3, TR-4, ACH-DIM, ACH-DISP, BIR-1, BIR-2, POL, DIFF; VLD and CONV are parsed first (mapper configuration), never evaluated as arms. Post-verdict disclosure via the sanctioned checkpoint carriers verbatim (anchor_text, Caveat, Binding).

Provenance discipline: every anchor_text quantity was retrieved from the named source at seal time (August 17, 2026) and transcribed; quantities NOT retrieved from a source are marked [RECALLED-FLAG] inside params and carry a conservative two-reading rule. Nothing in this file was evaluated against any curve at seal time.

| id | class | pattern | dialect_ref | anchor_text | params | Caveat | Binding | ascii_flag |
|---|---|---|---|---|---|---|---|---|
| TR-1 | A-EM-TRANS | P-TRANS | memo Register F(i), longest-wavelength rung (author band 1: the low-frequency radio rung, chosen for maximum regime coverage at the long-wavelength end); source: Saxena et al. 2018 MNRAS 480, 2733 (arXiv:1806.01191) | TGSS J1530+1049, the most distant radio galaxy to date at a redshift of z = 5.72, selected from the TGSS ADR1 survey at 150 MHz; flux density of 170 mJy at a frequency of 150 MHz and 7.5 mJy at 1.4 GHz; compact morphology in VLA imaging at 1.4 GHz (deconvolved angular size 0.6 arcsec); Lyman-alpha redshift from GMOS spectroscopy (Saxena et al. 2018) | nu_ref = 1.5e8 Hz (primary; the survey selection frequency, a secure detection at 170 mJy); k_ref = 2*pi*nu_ref/c; secondary detected frequency nu_sec = 1.4e9 Hz reported alongside (informational, non-verdict); z_src = 5.72; D_ref = D_lt(5.72) per CONV rule R1; tau_r = 1.0 (arrival budget) | The intrinsic luminosity is not independently known, so tau_r = 1 is the CONSERVATIVE arrival budget of the P-TRANS pattern (the A-1 twin), read with the x10^(+/-1) OOM band; tighter residual budgets exist and would only tighten. Ionospheric and interstellar plasma effects at 150 MHz are modeled non-substrate propagation effects. | P-TRANS: alpha_T(x_ref; d) * D_ref <= tau_r. CONV rules R1 (D_lt) and R2 (k-dressing both-readings intersection: k_obs and (1+z_src)*k_obs; exclusion asserted only where both readings exclude; both reported). | CLEAN |
| TR-2 | A-EM-TRANS | P-TRANS | memo Register F(i), rung 2 (author band 2); source: Fan et al. 2003 AJ 125, 1649 (astro-ph/0301135) | quasar SDSS J114816.64+525150.3 at z=6.43 (redshift determined from the position of the Lyman break, accurate to 0.05), discovered in 1300 deg^2 of SDSS imaging data (Fan et al. 2003) | lambda_ref = 9.0e-7 m [RECALLED-FLAG: representative observed-frame wavelength of the detection band; the Lyman break sits at (1+z)*1.216e-7 m = 9.03e-7 m; the survey filter's effective wavelength (about 8.9e-7 m) was not retrieved from the anchor source]; k_ref = 2*pi/lambda_ref; two-reading bracket for the flag: lambda in [8.5e-7, 1.0e-6] m, exclusion asserted only if excluded at both edges; z_src = 6.43; D_ref = D_lt(6.43) per CONV R1; tau_r = 1.0 | Broadband detection (i-dropout selection); the representative wavelength is flagged and bracketed; tighter budgets only tighten. | P-TRANS as TR-1; CONV R1, R2, R3 (bracket both-readings). | CLEAN |
| TR-3 | A-EM-TRANS | P-TRANS | memo Register F(i), rung 3 (author band 3); source: Banados et al. 2018 ApJL 856, L25 (arXiv:1803.08105) | quasar ULAS J1342+0928 at z = 7.54: 45 ks Chandra observation, 14.0 (+4.8, -3.7) counts detected in the observed-frame energy range 0.5-7.0 keV (6 sigma detection); hardness ratio HR = -0.51 (+0.26, -0.28) between the 0.5-2.0 keV and 2.0-7.0 keV ranges | E_ref = 2.0e3 eV (observed-frame boundary between the two counted sub-bands; representative); E bracket for R3: [5.0e2, 7.0e3] eV (the detection band edges), exclusion asserted only if excluded at both edges, representative reported; k = E/(hbar*c); z_src = 7.54; D_ref = D_lt(7.54) per CONV R1; tau_r = 1.0 | 14 counts total; band-integrated detection; the sub-band counts are few; tighter budgets only tighten. | P-TRANS as TR-1; CONV R1, R2, R3. | CLEAN |
| TR-4 | A-EM-TRANS | P-TRANS | memo Register F(i), shortest-wavelength ground-based very-high-energy rung (author band 4); sources: Aharonian et al. (H.E.S.S. Collaboration) 2006 Nature 440, 1018 (astro-ph/0508073) and the collaboration's auxiliary data table for its Figure 2 | 1ES 1101-232, z = 0.186; spectrum data points from 0.165 to 3.292 TeV; highest bin: energy interval 2.615-3.292 TeV, mean energy 2.916 TeV, flux 4.73e-14 +/- 3.03e-14 per TeV cm^2 s; bin 1.650-2.077 TeV: mean 1.840 TeV, 1.17e-13 +/- 0.56e-13; bin 0.657-0.827 TeV: mean 0.733 TeV, 1.17e-12 +/- 0.37e-12 (auxiliary table); companion A&A paper: power law of index 2.94 +/- 0.20 over 200 GeV to 4 TeV | E_ref = 2.916e12 eV (highest measured bin, source-reported); conservative alternative reading E_alt = 7.33e11 eV (highest bin at or above 3 sigma); exclusion asserted only if excluded under BOTH E readings (R3), both reported; k = E/(hbar*c); z_src = 0.186; D_ref = D_lt(0.186) per CONV R1; tau_r = 1.0 | EBL pair-production is a modeled non-substrate opacity already acting on these photons; tau_r = 1 is the residual-additional-opacity budget (the A-1 twin, memo Register F(i)); the highest bin is a 1.6 sigma point, hence the E_alt reading. | P-TRANS as TR-1; CONV R1, R2, R3. | CLEAN |
| ACH-DIM | A-ACHROM | P-ACHROM-DIM | memo Register F(ii) chromatic-dimming class; sources: Fixsen et al. 1996 ApJ 473, 576; Mather et al. 1994 | FIRAS: rms deviations from a blackbody spectrum less than 50 parts per million of the peak of the cosmic microwave background; abs(y) < 15e-6 and abs(mu) < 9e-5 (95% CL) (Fixsen et al. 1996); wavelength range 0.5 to 5 mm | lambda_1 = 5.0e-3 m; lambda_2 = 5.0e-4 m (band edges); k_i = 2*pi/lambda_i; Delta_tau_r = 5.0e-5; z_src = 1090 [RECALLED-FLAG: nominal last-scattering redshift, not verbatim-retrieved; D_lt insensitive below 1e-4 relative]; D_ref = D_lt(1090) per CONV R1 | The 50 ppm figure is a model-fit residual (blackbody plus dipole plus Galactic terms), read at order-of-magnitude level (R2, the DLM-comparison precedent) with the x10^(+/-1) OOM band; a frequency-dependent attenuation across the band would appear as a distortion at the level of its differential optical depth. | P-ACHROM-DIM: abs(alpha_T(x_1;d) - alpha_T(x_2;d)) * D_ref <= Delta_tau_r; CONV R1, R2. | CLEAN |
| ACH-DISP | A-ACHROM | P-ACHROM-DISP | memo Register F(iii) vacuum-dispersion class (frequency-dependent speed within one observed band); source: Schaefer 1999 PRL 82, 4964 (astro-ph/9810479) | Delta c/c < 6.3 x 10^-21 based on the simultaneous arrival of a flare in GRB 930229 with a rise time of 220 +/- 30 microseconds for photons of 30 keV and 200 keV (Schaefer 1999); secondary, same source: Crab pulsar optical pulses at 0.35 and 0.55 microns, phase difference less than 10 microseconds at 2 kpc, Delta c/c less than 5 x 10^-17 | primary: E_1 = 3.0e4 eV, E_2 = 2.0e5 eV, k_i = E_i/(hbar*c), beta_r = 6.3e-21, z_src unknown (no redshift for this burst; observed-frame k only; R2 not applicable, flagged); secondary reading (informational, reported alongside, non-verdict): lambda_1 = 3.5e-7 m, lambda_2 = 5.5e-7 m, beta_sec = 5.0e-17 | A path-integrated two-energy simultaneity bound; the criterion is a speed-ratio comparison at the two k for the same d, no distance enters; the secondary reading is a distinct regime pin, reported not intersected. | P-ACHROM-DISP: abs(Delta_ch(x_1;d) - Delta_ch(x_2;d)) <= beta_r; ray regime x >= x_G: identical path averages imply zero difference, PASS-RAY (nondispersive rays), reported (§5.4). | CLEAN |
| BIR-1 | A-BIR-EM | P-BIR | memo Register F(iii) polarization-walk twin of the banked s_1 law, long-wavelength polarimetry; sources: Michilli et al. 2018 Nature 553, 182 (arXiv:1801.03965); Gajjar et al. 2018 ApJ 863, 2 | FRB 121102, localized to a dwarf galaxy at redshift z = 0.193: bursts show ~100% linearly polarized emission at 4.1-4.9 GHz (Arecibo) with RM_src = +1.46 x 10^5 rad m^-2; nearly 100% linear polarization at 4-8 GHz (GBT) | nu_ref = 4.5e9 Hz; k_ref = 2*pi*nu_ref/c; P_obs = 1.0 (nearly 100%); kappa_r = 1.0 rad (order-of-magnitude depolarization budget: a random-axis walk phase of order 1 rad would depolarize an ensemble; near-total observed polarization bounds Phi_RMS at that order); z_src = 0.193; D_ref = D_lt(0.193) per CONV R1; N-rules: N_lambda = d/lambda_ref >= 10 and N_dom = D_ref/d >= 10, else VOID-N | Depolarization dialect (random-axis walk), not fixed-axis coherent birefringence: the coherent-birefringence coefficient bounds of Register F(iii) are a different dialect and are NOT used as kappa_r. The observed polarization is after Faraday-rotation correction (a plasma effect, not a vacuum property). kappa_r read at OOM level with the x10^(+/-1) band; the comparison is R2 (DLM precedent). | P-BIR: Phi_RMS := s_1 * k_ref * sqrt(d * D_ref) <= kappa_r, live only under the N-rules; CONV R1, R2. | CLEAN |
| BIR-2 | A-BIR-EM | P-BIR | memo Register F(iii) polarization-walk twin, short-wavelength polarimetry; source: Gotz et al. 2014 MNRAS 444, 2776 (arXiv:1408.4121) | GRB 140206A: using INTEGRAL/IBIS as a Compton polarimeter, the linear polarization level of the second peak of the burst is constrained as being larger than 28% at 90% c.l.; TNG afterglow spectroscopy gives z = 2.739 (Gotz et al. 2014) | E bracket = [2.0e5, 8.0e5] eV [RECALLED-FLAG: the IBIS Compton-mode band was not verbatim-retrieved from the anchor source; R3 applies — exclusion asserted only if excluded at both edges]; k = E/(hbar*c); P_obs >= 0.28; kappa_r = 1.0 rad (OOM depolarization budget as BIR-1); z_src = 2.739; D_ref = D_lt(2.739) per CONV R1; N-rules as BIR-1 | Prompt-emission polarization lower limit; band flagged and bracketed; OOM level; R2 comparison. | P-BIR as BIR-1; CONV R1, R2, R3. | CLEAN |
| POL | A-POL | P-POL | memo Register E, LVK polarization program; sources: Abbott et al. 2017 PRL 119, 141101 (GW170814); the GWTC-1 tests-of-GR summary (arXiv:1905.05565 sec. 8); Takeda et al. 2021 PRD 103, 064037 (arXiv:2010.14538) | purely tensor polarizations preferred over purely vector or purely scalar polarizations: for GW170817 Bayes factors greater than 10^20 in favor of purely tensor polarizations; GW170814 and GW170818 give Bayes factors of a few tens and hundreds versus purely vector or scalar (GWTC-1 summary); Takeda et al. find logarithms of the Bayes factors of 2.775 and 3.636 for GW170814 and 21.078 and 44.544 for GW170817 in favor of pure tensor against pure vector and pure scalar respectively | categorical; evaluated on the Phase-1 candidate set K only: PASS iff K's helicity content contains {+2, -2} and is tensor-dominant; FAIL iff K's content is {+1, -1}-only; INDETERMINATE iff mixed; under CI-W/EM-IN (K empty) the arm is VOID-NO-CANDIDATE | The LVK tests are extreme-hypothesis tests (pure tensor vs pure vector vs pure scalar) and, per the papers' own caveat, do not preclude mixed-content scenarios; no viable theory predicts purely scalar or purely vector radiation, so the test is a null test. | P-POL categorical; mixed content maps to INDETERMINATE, not FAIL (the papers' own extreme-hypothesis caveat, Binding). | CLEAN |
| DIFF | A-DIFF | P-DIFF | memo Register E, the GW170817/GRB 170817A speed band; the ANNEX-CDEF-1 own-pre-registration clause discharged here (§3.2); source: Abbott et al. 2017 ApJL 848, L13 (arXiv:1710.05834) | observed time delay of (+1.74 +/- 0.05) s between GRB 170817A and GW170817; the difference between the speed of gravity and the speed of light constrained to be between -3 x 10^-15 and +7 x 10^-16 times the speed of light; luminosity distance 40 (+8, -14) Mpc | Delta_obs := (v_GW - c_EM)/c_EM in [B_lo_obs, B_hi_obs] = [-3.0e-15, +7.0e-16]; sign mapping onto the gate's Delta (Delta_S under CI-S, Delta_W under CI-W/EM-IN; both EM relative to the S2 reference, §6): Delta = -Delta_obs/(1 + Delta_obs) = -Delta_obs to better than 1e-14 relative, hence [B_lo, B_hi] = [-7.0e-16, +3.0e-15]; k_S2 = 2*pi*f_ref/c with f_ref = 1.0e2 Hz (inherited from the G-POLY1 A-1 reference frequency, lineage convention); k_EM: E bracket [1.0e4, 1.0e6] eV [RECALLED-FLAG: gamma-ray-monitor band edges not verbatim-retrieved; R3 applies, representative 1.0e5 eV reported]; distance informational only (the criterion is a speed-ratio comparison) | The source bound already folds an assumed emission-delay window; frozen as stated; f_ref = 1.0e2 Hz is a lineage convention (the signal spans a broader band); the sign convention of the observation is stated explicitly above so that no sign slip can occur at read. | P-DIFF: B_lo <= Delta <= B_hi; runs LAST of all arms; CC read #1 is the blind read of record (E-9). | CLEAN |
| VLD | VLD | validity-edge parameters (mirrors G-POLY1 A-4) | pre-registration §5 restated for the mapper (no physics; guards against silent drift) | eps_T^2 <= 0.10 (weak-fluctuation validity, per config; else all second-order arms VOID); Q_T(x)*x^3 <= 0.10 (coherent-wave validity, else VOID-INCOHERENT at that x); eps_T*x <= 1 (phase-perturbation validity, else VOID-PHASE); x_S = largest grid x satisfying both; x_G = 10 (ray-regime domain); overlap rule: exclusion only if BOTH models exclude; gap rule: VOID unless both boundary points excluded AND the leg's own abs(Delta_ch) (resp. alpha*d) is unimodal or monotone across the gap; N_lambda = N_dom = N_cell = 10; OOM band x10^(+1) and x10^(-1) on every sealed threshold; grid x = 10^n, n = -8, -7.5, ..., +8 (33 points); comparison edges 1e-6 relative; doubling gate 1e-8 (floor 1e-6, VOID-NUM); containment 1e-6; Rayleigh exponent control 4.00 +/- 0.02 on x in [1e-4, 1e-3]; substrate floor d >= N_cell*a in substrate units, NOT converted to SI, unexercised | thresholds: eps_T2_max = 1.0e-1; imk_rek_max = 1.0e-1; epsx_max = 1.0; x_G = 1.0e1; N_lambda = 10; N_dom = 10; N_cell = 10; OOM_factor = 1.0e1; grid_n_min = -8; grid_n_max = 8; grid_step = 0.5; tol_edge = 1.0e-6; tol_doubling = 1.0e-8; floor_doubling = 1.0e-6; tol_contain = 1.0e-6; exponent_target = 4.00; exponent_tol = 0.02; interval_equality_tol = 1.0e-6 | VOID never counts as FAIL and is reported distinctly from PASS; a VOID can only widen a window. | Every arm and config applies these rules identically; the mapper asserts this row's values against the locked pre-registration §5 at open (any mismatch is a §5.5 halt). | CLEAN |
| CONV | CONV | conversion constants and conventions | the only place SI values exist in this gate (T4); the transverse-scale import (A-SHEAR lineage, ANNEX-CDEF-1, election E-1(a)) is exercised here and in the Phase-3 mapper only | exact SI defining constants (2019 SI): c = 299792458 m/s; h = 6.62607015e-34 J s; e = 1.602176634e-19 C; k_B = 1.380649e-23 J/K; derived: hbar = h/(2*pi); 1 eV = 1.602176634e-19 J; k(E) = E/(hbar*c) for photon energy E; k(lambda) = 2*pi/lambda; k(nu) = 2*pi*nu/c; length units: 1 au = 149597870700 m (IAU 2012 exact), 1 pc = 648000/pi au = 3.0856775814913673e16 m, 1 Mpc = 1e6 pc; 1 Gyr = 3.15576e16 s (Julian); cosmology for redshift-to-distance (Planck 2018 VI abstract): H0 = 67.4 km/s/Mpc, Omega_m = 0.315, spatially flat, radiation neglected (effect on lookback time below 1e-3 relative for the roster's redshifts, in the conservative direction for the highest); Wien frequency-law constant x_pk = 2.821439372122079 | channel-speed import: c_ch = c = 299792458 m/s under E-1(a) (the aggregate isotropized transverse channel; A-SHEAR lineage; ANNEX-CDEF-1 reading (a)); the domain scale d in metres is the free axis and x = k*d is dimensionless; RULE R1 (distance): for redshift-anchored rows D_ref = D_lt(z) = c * Integral_0^z dz' / ((1+z') * H(z')), H(z) = H0 * sqrt(Omega_m*(1+z)^3 + 1 - Omega_m), the light-travel distance (smaller than the comoving distance: conservative, fewer exclusions); RULE R2 (k-dressing): for redshift-anchored rows every criterion is evaluated at k_obs and at (1+z)*k_obs, and an exclusion is asserted only where BOTH readings exclude (both reported); RULE R3 (brackets): where a row carries a bracket [RECALLED-FLAG] an exclusion is asserted only where both bracket edges exclude (representative reported); RULE R4: every sealed threshold recomputed at x10 and x0.1 (OOM robustness, §5.4) | The import is named, exercised only here and in the sealed mapper, and revocable with the A-SHEAR lineage exactly as W_union; no d is derived; every window is import-conditional. | Phase 3.2: convert each row's reference quantities to k_r and D_r using this row only; the Phase-3 mapper parses this row before any arm row; T4 holds outside this file and the mapper. | CLEAN |

END OF SEALED FILE. Census check string: ROWS=12.

<<<END anchors_G_CI1_SEALED.md>>>
