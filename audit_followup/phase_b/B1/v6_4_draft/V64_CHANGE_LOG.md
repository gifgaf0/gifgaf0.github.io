# V6.4 change log (DRAFT): gauge paper correction, v6.3 → v6.4

**Plain-language summary.** This draft corrects the published gauge-group paper in four places and adds no new claim.
- **The hypercharge sign is withdrawn.** The alternating sign the paper put in front of Furey's charge formula is not a relabelling of Furey's choices. It is inconsistent: charges must add up over the three modes, and they do not. It also puts two sectors in the same color representation, which the mathematics forbids. The correct charges are Furey's own, N/3, and the paper's contribution here shrinks to matching the three modes with the polyhedron's three Hamiltonian cycles.
- **The Cabibbo match is downgraded.** As stated (sin θ_C = 3/13), it is 7.6σ–8.5σ away from the 2024 data. Read as tan θ_C, it agrees within 0.8σ, but that reading was found after looking at the data. So it is kept only as a labelled post-hoc observation, not a result.
- **The face description is fixed.** The 14 faces are the lines of two Fano planes, not "lines and their complements". The face set's symmetry group (order 42) is stated, along with where PSL(2,7) actually acts.
- **The chirality statement gets its proof.** All 42 symmetries of the triangulation preserve its orientation, so no version of the polyhedron can have a mirror symmetry.

**Status: DRAFT.** Nothing is published. Any Zenodo version comes back to the author for approval (brief of October 6, 2026: "Draft, don't publish or send").

| Item | Value |
|---|---|
| Source | v6.3, md5 `8c01f4c9d849bbab1eaff826fd353c3f` (the ledger anchor; the copy in `source/` was transcribed from the project store and verified byte-exact by this md5) |
| Result | `Gifford_Csaszar_Gauge_Group_v6_4_2026_DRAFT.md`, md5 `afbbf56dc1f0b5573d8beb1431555567` (42,923 → 50,350 B; 267 → 277 lines) |
| Script | `edit_v6_4_correction.py`, md5 `dcbf9608f8a877970e0464ae2283b2af`; usage `python3 edit_v6_4_correction.py [SRC_v6_3.md] [OUT_DIR]` |
| Authority | `../B1_PREREG.md` (md5 `5374289db16dcdd73f90875cc89b7ee3`, locked at commit c2148ae); two-leg checks 32/32 PASS (`../b1_compare_output.txt`); `../B1_RESULT.md` |

## Hunks

| Hunk | Tags | Description |
|---|---|---|
| G1 | T8 | version line v6.3 → v6.4 |
| G2 | T8 | v6.4 revision note (correction declaration) |
| G3 | COR | Abstract, first sentence: hypercharge and Cabibbo claims scoped |
| G4 | COR | Abstract, stages (iii) and (iv) |
| G5 | COR | Section 1: outline sentence |
| G6 | FACT | Section 3: the faces are two line-disjoint Fano planes; Aut(face set) = AGL(1,7); PSL(2,7) per plane |
| G7 | COR | Section 3: the Fano± bipartition is no longer said to provide hypercharge |
| G8 | COR | Section 5, first paragraph: Furey 2015's operator is a charge |
| G9 | WD/COR | Section 5: sign dressing withdrawn; Furey's Q = N/3 restored; audit item closed negative; novelty confined to (a) |
| G10 | COR | Section 6.1: the displayed equation states the number 3/13, not \|V_us\| = 3/13 |
| G11 | COR | Section 6.1: physical-interpretation sentence scoped |
| G12 | COR/DATA | Section 6.1: comparison updated to PDG 2024; sin reading excluded; tan reading post hoc |
| G13 | FACT | Section 8: chirality given its combinatorial basis |
| G14 | WD | Section 9: verified claim (3) withdrawn |
| G15 | WD | Section 9: verified claim (5) withdrawn from the verified list |
| G16 | COR | Section 9: Conjecture 3 (post-hoc observation) added |
| G17 | COR | Open Problem (ix) restated; RG running closed negative |
| G18 | COR | Section 11: mixing-angle wording scoped |
| G19 | COR | Section 11: "Cabibbo 3/13 result" → "the 3/13 ratio" |
| G20 | COR | Section 12: hypercharge sentence corrected |
| G21 | COR | Section 12: Cabibbo sentence corrected |
| G22 | COR | Section 12: claim and conjecture counts |
| G23 | REF | References: Grossman et al. (2022) at 17 and PDG (2024) at 24, inserted alphabetically; list renumbered to 25 |

Tags: **WD** withdrawal, **COR** correction, **FACT** factual repair, **DATA** data update, **REF** reference, **T8** bookkeeping.

## Verification

- **Reverse splice.** Removing every hunk from the draft reconstructs v6.3 byte-exactly, so everything not listed is untouched.
- **Structural checks.** These are EOF-anchored and asserted in the script:
  - references are numbered 1–25 in sequence to the end of the file;
  - the body contains no bracket-number citation, so renumbering is safe;
  - Grossman et al. (2022) is cited twice in the body and listed once;
  - PDG 2024 is cited in the body and listed once;
  - every paragraph containing the dressing formula, or "sin(θ_C) = 3/13", is a withdrawal;
  - the v6.2 disambiguation labels survive;
  - Section 9 lists claims (1)–(5), with (3) and (5) marked withdrawn, plus Conjecture 3.
- **Sources.**
  - The numbers come from PDG 2024 (Navas et al., Phys. Rev. D 110, 030001), CKM review Eqs. 12.7, 12.8, 12.26 and 12.27.
  - Furey's definitions come from arXiv:1603.04078 (= Phys. Lett. B 742, 195).
  - The running statement comes from Grossman, Ismail, Ruderman & Tsai, JHEP 06 (2022) 065 (arXiv:2201.10561): "λ, ρ, and η only change by O(10⁻⁴) from the weak scale to the Planck scale".
  - All three were read on October 7, 2026.

## Left for the author (not changed in the draft)

1. **The title and the Section 5 heading still say "Hypercharge".** After the correction, the section carries Furey's charge on the cycle modes. Retitling is an editorial call.
2. **Whether to keep the post-hoc tan θ_C observation at all.** Dropping it is the conservative option. Keeping it, as drafted, is honest only with the post-hoc label.
3. **Section 8, "trivial symmetry group (C₁) … no rotational axes".** This depends on the coordinates; the draft does not verify it. The combinatorics allow order-2 rotations: an element x ↦ −x + c of AGL(1,7) preserves orientation. What the draft adds holds for every realization: no mirror, inversion or rotoreflection symmetry.
4. **Labelling.** Section 3 says {e₁, …, e₇}, while Sections 6 and 6.3 use e₀. The draft bridges this with "e₇ ≡ e₀" and does not relabel.
5. **Not re-checked:** the |V_cb| note's PDG comparison (still PDG 2022); verified claims (1), (2) and (4); the abstract's "No free parameters are introduced". These are outside B1's scope.
6. **Zenodo metadata.** The record's description and keywords probably repeat the hypercharge and Cabibbo claims. If v6.4 is approved, they need the same scoping. The record metadata was not available here.
