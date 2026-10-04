# Venue recommendation and submission path

**Plain-language summary.** Post the paper on Zenodo first. The independent second computation has come back. It disagreed with the first on four numbers, all traced to defects in the first computation; after their correction the two agree on every cited number. Then submit it to *Classical and Quantum Gravity*, the journal where the closest prior work (the analogue-gravity "one metric needs fine tuning" papers) appeared. *Physical Review D* is the backup. Three things to do before posting are listed at the end.

## Recommendation

1. **Zenodo preprint (v1).** It is immediate and gets a DOI and a CC-BY-4.0 licence, matching the program's earlier Zenodo papers. Upload the PDF built from `second_sound_light_cone_DRAFT.md` and the supplementary scripts and data as a zip, with checksums. Post after the second leg returns. The cited numbers are now from two independent computations.
2. **arXiv**, if an endorser is available: primary **gr-qc**, cross-list **cond-mat.quant-gas**. A first-time submitter needs endorsement in gr-qc. An author of any of Refs. [1–8] or [38] would be the natural person to ask, since the paper extends their work.
3. **Journal: *Classical and Quantum Gravity*** (regular "Paper" format; the draft runs about 4,300 words plus two tables). Why it fits:
   - The paper is the mono-metricity / naturalness problem of Refs. [2] and [5], both published in CQG, applied to a concrete supersolid medium.
   - CQG's referee pool includes the analogue-gravity community, who will recognize the framing at once.
   - Negative results that close off a model class are within its scope.
   - **Backup: *Physical Review D*.** It suits the Lorentz-violation and vacuum-Cherenkov framing (Refs. [13–16] are the PRD/JHEP lineage).
   - **Second backup:** *Foundations of Physics* or *Universe*, for a foundations-of-medium-vacua audience.

## Before posting

- **Second leg: done** (PR #36; 108/112 on first comparison, four first-leg defects corrected, 112/112 after correction; see `../closure/LBC_2LEG_CLOSURE_MEMO.md`). The tables now carry the corrected values.
- **Read the body of Cox's preprint** (Ref. [28], Zenodo v4, 6.7 MB PDF; our literature sweep could not parse it) for any treatment of second sound, longitudinal sound or Cherenkov drag. The paper quotes only its record's no-drag sentence. If the body treats second sound, revise the framing in Secs. 1 and 9.
- **Optional and cheap:** add the current-vertex (circulation) weights to Sec. 6. The phase-mode projection uses the same BdG eigenvectors as the density weights. This would turn the qualitative "a density-neutral vortex still couples" into a number.
- Remove the cover note at the top of the draft, and choose how to word the AI-assistance acknowledgment.
