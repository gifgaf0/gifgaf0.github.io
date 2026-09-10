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
