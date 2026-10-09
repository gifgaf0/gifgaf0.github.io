# SLWE negative-result note for IACR ePrint, final form (Step 3b)

**Plain-language summary.** The four-page note from Phase C is now in final form. Three things changed:
- the byline and contact follow F5;
- the red "DRAFT" date line is gone;
- the acknowledgement is one sentence on AI assistance, below, for you to approve.

The text is otherwise unchanged. **Nothing is submitted.** ePrint posting is public and permanent, so submitting is your step.

| File | md5 | What it is |
|---|---|---|
| `slwe_negative_result_final.pdf` | `336db1d0412634a97905dc680d3fb957` | 4 pages (pdflatex) |
| `slwe_negative_result_final.tex` | `b8446d46f0ff052c56dfdf4d8c029cad` | Source |
| `build_final.py` | | Builds both from the Phase C draft (md5 `70ea6610…`). It checks that only the three edits were made and that reversing them gives back the draft byte for byte |

**The three edits.**
1. **Byline:** "Matthew Gifford, Independent researcher, Hollister, California, USA". The email placeholder is removed because this repository is public. ePrint's submission form asks for an email separately; enter it there, or add it to the PDF yourself.
2. **Date:** "October 2026".
3. **Acknowledgement, for your approval:**
   > AI agents (Anthropic's Claude) drafted this note and wrote and ran all of its computations, including both independent rank implementations; the author directed the work, reviewed the text, and takes responsibility for it.

   It replaces the draft's "The computations and both rank implementations were carried out by AI agents, not by human referees." The disclosure is kept, and the sentence now also covers the drafting.

**Optional, not changed.** Section 7 points to the branch `claude/audit-followup-oct6`. Branches can be deleted after a merge. For a permanent ePrint, a commit hash or a tagged release would hold.

## Addendum, October 8, 2026: the commit hash applied and the text finalized
You directed: "Use the latest commit hash from the claude/audit-followup-oct6 branch as the reference" and "Apply the ePrint commit hash and finalize the text."
- **Section 7 now cites the repository at a fixed commit:** `b09929ada97cc3c5bfc0f5f327518cd82e342fea`.
  - It was the branch head when the note was finalized, and it holds `audit_followup/phase_c/C1/` exactly as the note describes.
  - The commits after it touch only this note and the reports.
  - The hash is set on its own centred line. A 40-character hash cannot break across lines, and inline it ran 31 pt into the margin.
  - `build_final.py` now makes four edits. Reversing them still gives the Phase C draft byte for byte.
- **The text is final.** The acknowledgement sentence stays as drafted above; no other wording changed.

| File | md5 | |
|---|---|---|
| `slwe_negative_result_final.pdf` | `7d31a4a0353faa6c7b36a339dd8fa3ca` | 4 pages; rebuilds byte-identical with `SOURCE_DATE_EPOCH` |
| `slwe_negative_result_final.tex` | `5acb853b207e64e00850865e13d59002` | |

**Keep the cited commit reachable.** Merge the pull request with a merge commit, not a squash or rebase, so this commit stays in `main`'s history. Nothing is submitted.

## Addendum, October 9, 2026: the note now cites the paper it refutes
**Plain-language summary.** The note used to say SLWE "was never published as secure". That was wrong: *Fluid Lattice Topology* (Zenodo, doi:10.5281/zenodo.20078312) proposed it, and both of its versions claimed NIST Category 5. You approved four edits ("Yes", 13:06 PDT), made as edits 5–23 in `build_final.py`:
1. **Cite the paper and say what each version claimed.**
   - Version 1 claimed Category 5 at n = 512, q ≈ 2³².
   - Version 2 claimed Category 5 at k = 64, q = 911 from a primal estimate, with the dual and hybrid attacks left to check.
   - The introduction also cites the project's working specification (`tools/SLWE_Prime_Master_v2.md`, v2.1). On May 10, 2026, before version 2, it recorded that the Singer matrix has rank 76 at k = 32, and it switched to a uniform matrix. Section 4's "a later revision" now names that document.
2. **Credit version 2's own correction.** Version 2 had already found version 1's modulus far too large. Section 4 confirms that with the standard estimator.
3. **The rank collapse breaks version 2 too.** Table 1 already has k = 64 over F₉₁₁: rank 76, not 1024. Version 2's own rank test used k = 4, where the matrix has 64 columns, below the cap of 76.
4. **Each number is labelled with its parameter set.**
   - The 2³⁹ and 2⁵¹ estimates and "decryption never fails" are for version 1's parameters.
   - At version 2's q = 911, decryption can fail with probability 2⁻³⁵³·⁵, which is consistent with version 2's bound of 2⁻²⁹⁵.
   - The note says it did not estimate version 2's parameters: with the Singer matrix they fall to the rank collapse, and with a uniform matrix the scheme is generic Module-LWE with sparse secrets.

| File | md5 | |
|---|---|---|
| `slwe_negative_result_final.pdf` | `bb5d256ad7dd58f72dd4468aa41ada55` | 5 pages; it rebuilds byte-identical with `SOURCE_DATE_EPOCH`. The only LaTeX warnings are the two from the Phase C draft: the abstract's first line runs 5.8 pt over, and the MATZOV reference is loose |
| `slwe_negative_result_final.tex` | `b470bae54a389b5aa2f9a8b52c5bd279` | Reversing all 23 edits gives back the Phase C draft byte for byte |
| `FLT_V3_NOTICE_DRAFT.md` | | The notice for a version 3 of *Fluid Lattice Topology*, or for its Zenodo description |

**For you to decide: the title.** "…and why a uniform matrix does not repair it" holds for version 1's parameters, which is where the working specification made the matrix uniform. For version 2's parameters with a uniform matrix, the note makes no claim. A narrower title would be "…and why a uniform matrix does not repair its original parameters". The title is unchanged.

The cited commit `b09929a` is still the right reference: the scripts in `audit_followup/phase_c/C1/` are unchanged. Nothing is submitted or deposited.

## Addendum, October 9, 2026: deposited on Zenodo
You deposited the note as Zenodo record **10.5281/zenodo.23270249**: version v1, a preprint under CC BY 4.0, published October 9, 2026.
- Its one file, `slwe_negative_result_final-1.pdf`, has md5 `bb5d256ad7dd58f72dd4468aa41ada55`. That is byte for byte the PDF in this folder.
- The title stays as it was.
- The record lists no related identifiers yet. `FLT_V3_NOTICE_DRAFT.md` now cites this DOI and suggests the identifiers for both records.
