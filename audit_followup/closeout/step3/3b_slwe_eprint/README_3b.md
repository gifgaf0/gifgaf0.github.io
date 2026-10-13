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

## Addendum, October 10, 2026: the note revised after an independent audit
**Plain-language summary.** An independent audit of the deposited note (your cryptography agent's, revision 2) found four wrong statements and one overstatement. The mathematics stands, and so does the main result. The revised note corrects them and adds the estimates the first version left out. You said "Yes" to making the changes (16:01 PDT). A second, separate check of the revision against its sources found more to fix; those fixes are in. Nothing is deposited.

**Corrections to this README's October 9 addendum** (append-only, so they are stated here):
- Item 1 there says the working specification "switched to a uniform matrix". The title paragraph says the title "holds for version 1's parameters, which is where the working specification made the matrix uniform". Both are wrong about where:
  - the specification never used version 1's parameters: it targets q ≈ 3329, with toy runs at q = 911;
  - its uniform matrix comes from Brief 06, which was tested at p = 8191 and put into the key generation of the hybrid-KEM wrapper;
  - that wrapper's target is k = 32 with q ≈ 2³² (`hybrid_kem/SPEC.md`), so the pairing of a uniform matrix with q ≈ 2³² comes from the hybrid-KEM design;
  - the C1 audit was the first to estimate that pairing.
- Item 4 there gives 2⁻³⁵³·⁵ as the failure probability at q = 911. That figure is the tail P(|N| > 227). The failure rate is 2⁻³⁵³·⁹; with the decoder of `tools/sqt_slwe.py` and its encoding m⌊q/2⌋ it is 2⁻³⁵¹·⁴.
- The October 9 edits called q = 4 294 977 961 and weight 64 "version 1's parameters". Version 1 gives only q ≈ 2³² with q ≡ 1 (mod 455), and sparse ternary secrets. The exact prime was fixed by the C1 pre-registration; weight 64 is version 2's, and the ledger's.

**Where the four errors came from.**
- Error 2's sentence ("kept version 1's parameters") was written in the October 9 edits.
- Errors 1 and 3 became errors in those edits. The edits tied sentences of the Phase C draft to *Fluid Lattice Topology*, but in the draft "reported earlier" and "the proposed parameters" had referred to the project's own documents.
- Error 4 ("q > 1032") was in the Phase C draft. I passed over it in two reviews and edited that sentence on October 9 without catching it.

**What the revision changes.** `build_v2.py` makes 23 edits to the first version's source; reversing them gives the first version byte for byte. In the note, "version 1" and "version 2" mean the proposing paper's versions. The note's own versions are "the first version of this note" and "this revision", and its date line reads "October 2026 (revised)".
1. **Abstract.**
   - The ledger's 2^(−6.4×10¹⁵) is out; Section 5 attributes it to the ledger.
   - It adds version 2's figures: 2⁴⁰ after the rank collapse, and 2¹⁶⁷ with a uniform matrix against about 2²⁷² for Category 5.
   - "Sixteen-dimensional" becomes "16-dimensional", which also removes the first version's 5.8 pt overrun in the first line.
2. **Section 2.**
   - It says what version 1 specifies (n = 512, q ≈ 2³² with q ≡ 1 (mod 455), sparse ternary secrets), and that the prime, weight 64 and CBD(2) are the note's instantiation.
   - A footnote says that ⌊q/2⌉ stands for either rounding of q/2, since Section 5 now shows the choice matters at the boundary.
3. **Section 3.** Version 2 after the collapse: 2^40.4.
4. **Section 4.** It is retitled "A uniform matrix does not restore the claimed security".
   - The uniform matrix is credited to Brief 06, with the hybrid-KEM wrapper's target (k = 32, q ≈ 2³²) and [6]'s statement that its security table applies with this matrix.
   - Table 2 gains a "claimed" column, [6]'s q = 3329 row (2^112.2) and version 2's parameters (2^167.2).
   - [6]'s rows carry its own labels "L5" and "L3", since its scale is not NIST's: it rates Kyber-1024 "L3".
   - With weight-64 secrets both of [6]'s rows fall below 2^128. A dense secret lifts q = 911 only to 2^149.
   - 3329 is not ≡ 1 (mod 455); 2731, the nearest such prime below it, gives 2^114.
   - Version 2 with a uniform matrix:
     - every lattice attack in the estimator's default set is printed: 2^167 MITM hybrid, 2^181 hybrid, 2^239 dual hybrid, 2^249 BDD, 2^254 uSVP at β = 800, 2^268 dual;
     - all are below 2^272, and the primal hybrid attacks put the parameters below Category 3.
     - "Category 1" and "Category 3", as first drafted, were loose: NIST's call also defines Categories 2 and 4 (2^146 and 2^210 gates).
5. **Section 5.**
   - At q = 1033 the worst case |N| = 258 fails under every decoder and rounding tried. The first prime with no failures is 1039.
   - The failure rate at q = 911 is given next to the tail.
   - The 2^(−6.4×10¹⁵) is attributed to the ledger.
6. **Conclusion.** It covers both parameter sets, "under every lattice attack in the estimator's default set".
7. **Section 7.** It cites commit `d96d1f7451ffca96468ce1918f595370154558af`, which adds `v2_runs/` (with checksums), lists the three new scripts, and keeps each centred display with its sentence.
8. **"Changes in this revision".** A new paragraph lists the four errors and the Table 1 wording. The acknowledgement adds that a separate Claude agent audited the first version.
9. **References.**
   - [6] is now cited as v2.0 with notes to v2.4.
   - New entries: Brief 06 (as a project brief, without a byline, since the file has none), the hybrid-KEM specification, the ledger's section 2.66.1, and NIST's 2016 call.

| File | md5 | |
|---|---|---|
| `slwe_negative_result_v2.pdf` | `50599a25b50cce62ecef8ad60d632f65` | 6 pages; rebuilds byte-identical with `SOURCE_DATE_EPOCH`. No overfull boxes, and no new bitmap fonts |
| `slwe_negative_result_v2.tex` | `a12cef5cc2c741d9a0d08ba6408ffe83` | |
| `build_v2.py` | | Builds both from the first version's source (md5 `b470bae5…`) and checks the reverse |
| `v2_runs/` | | The new runs, in commit `d96d1f7`; its README gives the figures and checksums |
| `ZENODO_V2_DRAFT.md` | | Settings and description for the new Zenodo version |
| `FLT_V3_NOTICE_DRAFT.md` | | Updated: a uniform matrix restores neither version's claim. It cites the note's all-versions DOI |

**Keep the cited commit reachable.** Merge with a merge commit, not a squash or rebase, so `d96d1f7` stays in `main`'s history. Deposit after the merge: until then the commit is not on GitHub.

**The title question of October 9 is settled.** With a uniform matrix, version 2's parameters reach about 2^167, below Category 5 under every lattice attack in the estimator's default set, so the title holds for both parameter sets. It is unchanged.

**Also in commit `d96d1f7`** (append-only addenda):
- `tools/SLWE_Prime_Master_v2.md` ([6]), v2.4. My October 8 note there called the C1 instantiation "the spec". The addendum states [6]'s own target and gives the estimator's figures for its own rows: at q = 911, 2^122.2 by BKW and 2^127.4 otherwise; at q = 3329, 2^112.2.
- `audit_followup/phase_c/C1/C1_RESULT.md`, on its "q > 1032" threshold and its tail-versus-rate wording.

**Not changed: the ledger.** Its V4.94 brackets and §2.66.1 still say "q > 1032". Correcting that needs a fold, which is your call.

## Addendum, October 10, 2026 (evening): the yardstick for "Category 5"
**Plain-language summary.** The revised note had argued that version 2 fails Category 5 because every lattice attack in the estimator comes in below 2^272. That test is too strict: by it, standardized ML-KEM would fail its own categories too. The note now measures version 2 against ML-KEM under the same estimator. The conclusion stands: version 2 falls between ML-KEM-512 and ML-KEM-768, about 95 bits below ML-KEM-1024. You said "Yes" to this change (19:15 PDT).
- **The new runs.** The estimator's own Kyber512/768/1024 sets are ML-KEM's lattice problems, with compression ignored. They give 2^139.7, 2^196.4 and 2^262.3, below the AES-based thresholds of 2^143, 2^207 and 2^272. The cases are in `v2_runs/v2_estimator_run.py`; the earlier cases were not rerun and are unchanged.
- **Superseded wording.** The note's Section 4, abstract, conclusion and "Changes" paragraph are reworded to this comparison, and FIPS 203 is cited. So are `ZENODO_V2_DRAFT.md`, the notice and `STATUS.md`. This supersedes the earlier addendum's item 4 wording ("all are below 2^272 … below Category 3"); its other items stand.
- **The cited commit.** Section 7 now cites `4eb30148edfe6e4949e16b6ecfc6d04f4512b6e1`, which adds these runs on top of `d96d1f7`. Keep both by merging with a merge commit.

| File | md5 | |
|---|---|---|
| `slwe_negative_result_v2.pdf` | `312841740b484f731d452c11e445a260` | 6 pages; rebuilds byte-identical. This supersedes the md5s in the addendum above |
| `slwe_negative_result_v2.tex` | `da095ae29e3076a977ffb47ab72e3473` | |

## Addendum, October 13, 2026: the notice is deposited; the revised note is not yet
**Plain-language summary.** *Fluid Lattice Topology* now carries the notice on Zenodo. The revised note, whose figures the notice quotes, is still to be deposited.
- ***Fluid Lattice Topology*.** Deposited by the author on October 13 as doi:10.5281/zenodo.23351706 (Zenodo v4), from `flt_v3/`. The PDF on Zenodo has md5 `6bd55206…`, which is the file built there.
- **The note.** At the fold of V4.100, DataCite lists one version under the note's all-versions DOI (10.5281/zenodo.23270248). The revision (`slwe_negative_result_v2.pdf`, md5 `31284174…`) waits for the author, with its deposit text in `ZENODO_V2_DRAFT.md`.
- **The ledger.** V4.100 records the threshold correction and the deposits (§2.100).

## Addendum, October 13, 2026 (afternoon): the revised note is deposited
- **The deposit.** The author deposited the revision as version 2 of the note: doi:10.5281/zenodo.23352161 (DataCite: a version of 10.5281/zenodo.23270248, registered 21:52 UTC).
- **What it completes.** The figures that the notice on *Fluid Lattice Topology* quotes are now on Zenodo.
- **The description.** It was pasted from the wrapped draft, so words run together at the wrap points. `ZENODO_V2_DESCRIPTION_UNWRAPPED.txt` is the paste-ready text.
- **The gauge record.** Its description was updated to the v6.4 abstract by 21:39 UTC (DataCite).
- **The ledger.** V4.100 says the revision was not yet deposited. A V4.101 entry recording both is staged in `audit_followup/fold_v4_101/`.
