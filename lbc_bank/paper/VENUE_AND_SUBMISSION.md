# Venue recommendation and submission path

**Plain-language summary.** Post the paper on Zenodo first. The independent second computation has come back. It disagreed with the first on four numbers, all traced to defects in the first computation; after their correction the two agree on every cited number. An outside review then led to a revision on October 4: the vortex couplings are now derived, two claims are withdrawn, and a second, fresh review checked the result. Then submit it to *Classical and Quantum Gravity*, the journal where the closest prior work (the analogue-gravity "one metric needs fine tuning" papers) appeared. *Physical Review D* is the backup. What remains before posting is listed at the end.

## Recommendation

1. **Zenodo preprint (v1).** It is immediate and gets a DOI and a CC-BY-4.0 licence, matching the program's earlier Zenodo papers. Upload the PDF built from `second_sound_light_cone_DRAFT.md` and the supplementary scripts and data as a zip, with checksums. Post after the second leg returns. The cited numbers are now from two independent computations.
2. **arXiv**, if an endorser is available: primary **gr-qc**, cross-list **cond-mat.quant-gas**. A first-time submitter needs endorsement in gr-qc. An author of any of Refs. [1–8] or [38] would be the natural person to ask, since the paper extends their work.
3. **Journal: *Classical and Quantum Gravity*** (regular "Paper" format; the draft runs about 5,500 words plus two tables, and its abstract is just under IOP's 300-word guideline). Why it fits:
   - The paper is the mono-metricity / naturalness problem of Refs. [2] and [5], both published in CQG, applied to a concrete supersolid medium.
   - CQG's referee pool includes the analogue-gravity community, who will recognize the framing at once.
   - Negative results that close off a model class are within its scope.
   - **Backup: *Physical Review D*.** It suits the Lorentz-violation and vacuum-Cherenkov framing (Refs. [13–16] are the PRD/JHEP lineage).
   - **Second backup:** *Foundations of Physics* or *Universe*, for a foundations-of-medium-vacua audience.

## Before posting

- **Second leg: done** (PR #36; 108/112 on first comparison, four first-leg defects corrected, 112/112 after correction; see `../closure/LBC_2LEG_CLOSURE_MEMO.md`). The tables now carry the corrected values.
- **Cox's preprint body: read** (Ref. [28], v4, in full, October 4, 2026; `../lit/COX_V4_BODY_READ.md`). It never treats second sound, the Landau velocity or Cherenkov drag, so the novelty claim stands. Reading it did change the paper, however:
  - the proposal takes Green's route (one longitudinal sound at about 10²⁰ c), not MacCullagh's;
  - at its own superfluid fraction our hydrodynamics puts its omitted second sound above the light speed (checked twice; supplementary S6), so its matter (defects whose limiting speed is the light speed) escapes our drag argument.

  Secs. 1, 5, 9 and 10 now say this, and the paper no longer claims to refute the proposal.
- **Outside review: done** (October 4). Its points are implemented. The item that used to sit here, quantifying how a density-neutral vortex couples, is answered differently: Sec. 6 now derives the coupling (twice, the second time blind). A moving vortex reaches the density through its own flow, with a strength fixed by the circulation quantum, and it drives shear through the normal fraction. Two claims the derivation does not support are withdrawn: that a vortex still drives second sound through its circulation in Green's limit, and that vortex matter could outrun light.
- **Second review of the revision: done** (a fresh AI reviewer). It found no error in the new physics. Its fixes are applied:
  - Sec. 8 now separates the vortex's flow vertex, which radiates but does not bind;
  - the survival conditions are complete;
  - the Green's-limit decoupling is stated for constant ρ_n;
  - the Table 2 note gives the right cause.
- **Approved by the author** (October 4, 18:08 PDT: "Approved draft"; `APPROVAL_V1.md`). The title and the acknowledgments stay as worded. The posting version is built: `submission/second_sound_light_cone_v1.pdf`, the approved text with the cover note removed and nothing else changed.
- **Left for the author:** upload the PDF and the supplementary zip to Zenodo, merge PR #35, then submit to *Classical and Quantum Gravity*.
