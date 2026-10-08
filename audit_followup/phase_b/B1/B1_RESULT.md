# B1 — Gauge paper v6.3: result and correction draft

**Plain-language summary.** The published gauge-group paper needs a correction, and a draft (v6.4) is ready for the author's approval.
- **The hypercharge sign is wrong.** The paper's one addition to Furey's charge formula, an alternating sign, is not a relabelling of anything Furey does, and it is not consistent: charges must add up over the three modes, and these do not. The paper's labels also put the one-mode and two-mode states in the same color representation, which is impossible because those two sectors are always conjugate. With either color convention, one quark sector gets a charge no real quark of that color has. The correct charges are Furey's own (N/3). What the paper adds is only the matching of the three modes with the polyhedron's three Hamiltonian cycles.
- **The Cabibbo match fails as stated.** The paper states sin θ_C = 3/13. The 2024 data put 3/13 between 7.6σ and 8.5σ too high. Read as tan θ_C it agrees within 0.8σ, but switching readings after seeing the data is exactly the move the ledger forbids, so that agreement can be kept only as a labelled post-hoc observation. Renormalization-group running cannot close the 2.6 % gap, because the Cabibbo angle runs by about one part in 10⁴.
- **The paper never calls PSL(2,7) the polyhedron's symmetry group.** That claim lives in the ledger, which wrongly attributes it to the paper in three places and builds on it in five entries. The correct statement: the polyhedron's faces form two Fano planes; the face set's symmetry group has order 42; PSL(2,7) is the symmetry group of each Fano plane on its own.
- **The FFA question.** Per the ledger, the gauge paper is not under review at *Finite Fields and Their Applications*. "v5" is its Zenodo version number. The only FFA submission on record is the PSL(2,7) spectral-rigidity paper, which was declined.

## Answers to the brief

| Brief item | Answer |
|---|---|
| Any claim that PSL(2,7) is the Császár polyhedron's automorphism or symmetry group | **None in the paper.**<br>• v6.3 never mentions PSL(2,7).<br>• The v5 manuscript in the store (`Gifford_Csaszar_Gauge_Group_v5_2026.docx`, headed "v4 (Revised)" with the v5 note) does not either.<br>• Earlier versions are not in the store.<br>• §8 says "trivial symmetry group (C₁)".<br>• The misattribution is in the ledger (table below). |
| Is 3/13 stated as tan θ_C? | **No.** It is stated as sin θ_C:<br>• §6.1: "\|V_us\| = 3/13";<br>• §9 claim (5), §10 (ix) and §12: "sin(θ_C) = 3/13". |
| The J = L_e₀ sign dressing against Furey (PLB 742, 2015) | **Closed: verdict (N-I), not a reparametrization, and inconsistent.** Two legs agree 32/32. |
| Draft the correction | `v6_4_draft/` (23 anchored hunks, reverse-splice verified). |
| Is v5 still under review at FFA? | **Not per the ledger** (details below). |

## Verdicts (pre-registration `B1_PREREG.md`, md5 `5374289db16dcdd73f90875cc89b7ee3`, locked at c2148ae)

**DR-B1-1, the Furey item: (N-I).** Not a reparametrization, and inconsistent. Leg 1 is `b1_checks.py`; leg 2 is `leg2/` (octonion construction); the comparison is `b1_compare_output.txt`.
- **C1. Sector colors.** With the modes in 3, the sectors are N = 0, 1, 2, 3 → 1, 3, 3̄, 1; with the modes in 3̄, they are 1, 3̄, 3, 1. Either way the N = 1 and N = 2 sectors are conjugate. Leg 1 used Jordan–Wigner matrices; leg 2 used Furey's ladder operators as left multiplications on ℂ⊗𝕆 and the cubic Casimir.
- **C2. Additivity.** The paper's Y = (0, 1/3, −2/3, 1) is not affine in N: the second differences are −4/3 and 8/3, where any a + bN gives 0.
- **C3. Furey's options.** None of the 8 options (N/3, −N/3, (3−N)/3, −(3−N)/3, each with 3 or 3̄ modes) reproduces the paper's Y or its table. Four of them satisfy the Standard Model color–charge correlation. No induced action makes both quark sectors 3̄.
- **C4. The paper's Y with the induced colors.** With 3 modes the pairs include (3, +1/3), which fails; with 3̄ modes they include (3, −2/3), which fails. One quark sector violates the correlation either way.
- **Consequence.** Claim (b) of §5 is withdrawn as incorrect, §9 claim (3) is withdrawn, and the novelty of §5 is confined to (a). This also corrects v6.3's statement that its spectrum {0, +1/3, −2/3, +1} "is the one anticipated by the number-operator construction": Furey's spectrum is {0, 1/3, 2/3, 1}.

**DR-B1-2, the Cabibbo observable: sin θ_C reading excluded; tan θ_C reading post hoc; (ix) closed negative.**

| Reading | Data (PDG 2024) | Value | Pull of 3/13 = 0.230769 |
|---|---|---|---|
| sin θ_C = \|V_us\| | Eq. 12.8 | 0.22431 ± 0.00085 | **+7.60σ** |
| sin θ_C = λ | global fit, Eq. 12.26 | 0.22501 ± 0.00068 | **+8.47σ** |
| tan θ_C = \|V_us/V_ud\| | Eqs. 12.8 / 12.7 | 0.230376 ± 0.000876 | +0.45σ |
| tan θ_C | K_μ2/π_μ2 \|V_us\| = 0.2250(4) / \|V_ud\| | 0.231084 ± 0.000418 | −0.75σ |
| tan θ_C | λ/√(1−λ²), global fit | 0.230932 ± 0.000735 | −0.22σ |

- The relative deviations of the sin reading are +2.88 % (direct) and +2.56 % (fit). The paper's "2.6 %" used the 2022 fit value.
- Both legs agree to 0.01σ.
- **Running.** Grossman, Ismail, Ruderman & Tsai (JHEP 06 (2022) 065) find "λ, ρ, and η only change by O(10⁻⁴) from the weak scale to the Planck scale".
- **Consequence.** Claim (5) leaves the verified list, the tan reading becomes Conjecture 3 (labelled post hoc), and Open Problem (ix) is restated.
- **Eddington flag.** Switching to tan θ_C closes the residual with the factor 1/|V_ud| without deriving that the construction yields tan θ_C. That is the Eddington Maneuver as the ledger defines it, which is why the reading cannot be presented as a result.

**DR-B1-3, symmetry statements.**
- **T1.** There is no PSL(2,7) claim in v6.3 or v5.
- **C6** (both legs):
  - the Császár face set has automorphism group AGL(1,7), of order 42;
  - all 42 automorphisms preserve the orientation of the torus (0 reverse it);
  - the 21 elements of F₂₁ keep each face Fano plane; |Stab_{S₇}(Fano⁺)| = 168, and its intersection with Aut(faces) has 21 elements;
  - 42 = 2·3·7 is squarefree, so every Sylow subgroup is cyclic and the Schur multiplier of AGL(1,7) is trivial.
- **Consequences.**
  - §3's "the 7 lines of the Fano plane and their complements" is false, since a complement of a line has four points; the draft corrects it.
  - §8's chirality now has a proof that holds for every realization in ℝ³.
- **Information.** Of the 30 Fano planes on seven labelled points, 8 share no line with Fano⁺, and Fano⁻ is one of them.

## Is v5 under review at *Finite Fields and Their Applications*?

**Not according to the ledger.**
- **"v5" is the gauge paper's Zenodo version number.** Record 21316171, published July 12, 2026; its content is manuscript v6.3.
- **No journal submission of the gauge paper is recorded.** Its Framework Index row ends: "Remaining: journal venue selection".
- **The only FFA submission on record is FFA-26-260,** the PSL(2,7) spectral-rigidity paper (Paper I).
  - It was transferred from *J. Algebra* (JALGEBRA-D-26-00651) and originally sent to *JCTA*.
  - FFA rejected it with no referee comments and no onward referral (V4.45 record, June 18, 2026).
- **Three status lines are stale on that history:**
  - the ledger's §1.1 "Paper status: Submitted to Journal of Algebra";
  - the Framework Index rows "Submitted to Journal of Algebra";
  - the project description's "submitted to JCT-A".
  The §1.1 line is item B2.
- I cannot see the journal's system. If the gauge paper was sent to FFA without a ledger record, the ledger is missing an entry; the author should confirm.

## Blast radius

**In the ledger.** Ten brackets for the Phase B fold, using V4.92 line numbers.

| Entry (line) | What it says | Bracket |
|---|---|---|
| §2.D-FC, Status (L532) | "Register 1 (direct consequence of SL(2,7) representation theory)"; L539: "The K₇ (Császár polyhedron) symmetry group is PSL(2,7)"; L534 credits Paper I | **The premise is restated.**<br>• PSL(2,7) ≅ GL(3,2) is the automorphism group of one face Fano plane, i.e. the octonion triple system.<br>• It is not the automorphism group of K₇ (that is S₇), nor of the Császár face set (AGL(1,7), order 42, trivial Schur multiplier, so no spin cover).<br>• The SL(2,7) mathematics stands as R1.<br>• Its reading as the polyhedron's spin structure loses its premise. |
| §2.74 cross-references (L2193) | "Gauge Group paper v5 (Császár automorphism group / PSL(2,7))" | **Misattributed:** the paper (v5, v6.3) makes no such claim. |
| §2.74 Part VII (L2260) | "Császár automorphism group / PSL(2,7): Gauge Group paper (v5)" | Same. |
| §2.75 cross-references (L2269) | "Gauge Group paper v5 (PSL(2,7) as Császár automorphism group)" | Same. |
| OP-2.75-CR (L2351) | "the spin representation of K₇'s symmetry group (PSL(2,7) …)" | The premise is restated as for §2.D-FC. |
| §2.77 (L2507) | "not a contingent feature of the K₇ symmetry group" | Same. |
| §2.E-WD (L2773) | "the K₇ symmetry group's spin double cover SL(2,7)" | Same. |
| §2.E-QQ (L3050) | "the discrete K₇ symmetry group at the top" | Same. |
| Part V, the V4.59 gauge-paper row (L4359) | "(b) sign dressing provisional — reparametrization an open audit item" | **Closed in the negative.**<br>• The dressing is inconsistent; two legs agree 32/32; claim (b) is withdrawn.<br>• sin θ_C = 3/13 is excluded by PDG 2024 at 7.6σ and 8.5σ.<br>• The tan θ_C agreement is post hoc.<br>• v6.4 is drafted and awaits the author. |
| Part V, the V4.61 v6.3 row (L4360) | v6.3 published | v6.4 correction drafted, not published. |

The V4.6 fold record (L20) repeats "K₇'s symmetry group PSL(2,7)". It is a historical log and is not touched, as in Phase A.

*Fold-time addition (V4.93).* A sweep of the whole ledger at fold time found five more dependents, and the fold brackets them too: §2.D-FC's Paper I cross-reference (L534) and its premise sentence (L539); §2.74 Part II, item 2 (L2219); the V4.7 §2.E-QQ entry (L2920); and §2.86's cross-references (L3207). Paper I (v2.1) calls PSL(2,7) the automorphism group of the Fano plane, not of K₇. The §2.D-FC wording was also tightened: "no spin cover" became "no genuinely projective (spin) representations". A ℤ₂ central extension of AGL(1,7) exists through its abelianization, but with a trivial Schur multiplier every projective representation is linear. See `fold_v4_93/FOLD_AUTHORIZATION_V4_93.md`.

**Outside the ledger.**
- **Paper II-A v2.2, §1.1** (`Gifford_Paper_IIA_Bjerknes_Gravity_v2_2_2026.md`) says the gauge paper "established … 16 sub-1% numerical predictions for particle properties" and "golden ratio as flux eigenvalue". Both were already inaccurate before B1:
  - v6.3 lists five claims, not sixteen predictions;
  - v6.3 says φ has no prior address in the Császár geometry.
  B1 weakens the description further. If II-A is or will be on Zenodo, its next version should describe the gauge paper as v6.4 does. The ledger leaves II-A's Zenodo sign-off open (V4.39-era record); its status was not confirmed here.
- **The Framework Index** (project store) gauge-paper row. It needs updating at the next index regeneration; the store is full.
- **`STATUS.md`.** Updated at the end of Phase B.

## Process notes

- **Blindness held this time.** The first leg was committed (86664a3) before the second leg started, and the second leg read nothing outside `leg2/`. That repairs the Phase A exposure pattern (H-A1-1, H-A2-1, H-A3-1).
- **Byte-exact source.** The v6.3 source was transcribed from the project store and matched the ledger anchor md5 `8c01f4c9d849bbab1eaff826fd353c3f` on the first attempt. The edit script therefore runs on the canonical bytes.
- **What the correction does not decide.** These are listed in `v6_4_draft/V64_CHANGE_LOG.md`, "Left for the author":
  - the title;
  - whether to keep the post-hoc observation;
  - §8's coordinate-level C₁ claim;
  - the labelling;
  - Zenodo metadata.

## Files

| File | md5 |
|---|---|
| `B1_PREREG.md` | `5374289db16dcdd73f90875cc89b7ee3` |
| `b1_checks.py` / `b1_output.txt` / `b1_results.json` | `5eec9a62…` / `9b87c0a5…` / `726c27fc…` |
| `leg2/` (`leg2_b1.py`, `leg2_output.txt`, `leg2_results.json`, `LEG2_REPORT.md`, `MANIFEST.md5`) | `e6de2b52…`, `cf1d0983…`, `44470d71…`, `95ba95cb…`, `6b236e3a…` |
| `b1_compare.py` / `b1_compare_output.txt` | `c14542d9…` / `b5b7cd5d…` (32/32 PASS) |
| `v6_4_draft/source/Gifford_Csaszar_Gauge_Group_v6_3_2026.md` | `8c01f4c9d849bbab1eaff826fd353c3f` |
| `v6_4_draft/edit_v6_4_correction.py` | `dcbf9608f8a877970e0464ae2283b2af` |
| `v6_4_draft/Gifford_Csaszar_Gauge_Group_v6_4_2026_DRAFT.md` | `afbbf56dc1f0b5573d8beb1431555567` |
| `v6_4_draft/V64_CHANGE_LOG.md` | the change log, with items left for the author |

Sources (read October 7, 2026):
- Furey, [arXiv:1603.04078](https://arxiv.org/abs/1603.04078), via [ar5iv](https://ar5iv.arxiv.org/html/1603.04078);
- [PDG 2024 CKM review](https://ccwww.kek.jp/pdg/2024/reviews/rpp2024-rev-ckm-matrix.pdf);
- Grossman et al., [arXiv:2201.10561](https://ar5iv.labs.arxiv.org/html/2201.10561), JHEP 06 (2022) 065.
