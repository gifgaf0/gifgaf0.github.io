# Alpha-decay paper, version 2: corrected draft (Step 2c)

**Plain-language summary.** This is a corrected version of the deposited alpha-decay paper (Zenodo, May 29, 2026, doi:10.5281/zenodo.20448930, the author's F3). It makes the five corrections the ledger lists (§2.93.B4), and the data and Table 1 are unchanged.
- The paper now claims **one** robust break, at radium (Z = 88), instead of two.
- The step count is fixed: 51, not 74.
- The two sections that leaned on the now-closed framework are removed, with the citations that did not support them.

A one-paragraph version note for Zenodo is below. Nothing is deposited.

## Files

| File | What it is |
|---|---|
| `alpha_decay_isotone_steps_v2_DRAFT.md` | Text of record for version 2 (md5 `819a3d84b783241b24e834e0a7fd558e`) |
| `alpha_decay_isotone_steps_v2_DRAFT.pdf` | Typeset copy, 6 pages. Figure 1 is not in the project store, so the PDF has a placeholder where it goes. The figure itself is unchanged; only its caption changed |
| `v1_to_v2.diff` | Line diff from the store copy to version 2 |
| `build_v2.py` | Builds both files from the store copy (md5 `770ac497…`). Every replacement is anchored and must match exactly once, and the result is checked (no "74 steps", no Z = 92 claim, no citation of the gauge paper, references renumbered) |
| `check_fixed_n.py` / `.json` / `_output.txt` | An independent re-computation of every fixed-N number the new Section 3.3 quotes, from the store's AME2020 table. It shares no code with Phase B's `b4_checks.py` and agrees with it to 10⁻⁴ MeV (PASS) |

## The five corrections (B4's list) and how each is made

| # | Correction | In version 2 |
|---|---|---|
| 1 | 74 → 51 steps (N > 128) | Abstract, Introduction, Section 2 ("51 … (74 over all N)") and the Conclusions |
| 2 | One robust break at Z = 88. Without a pre-registered N-controlled test, no Z = 92 claim. Remove "it is not driven by a correlation between N and Z" | New abstract. Section 3.3 is now "Boundaries at Fixed Neutron Number", with Table 2 (the equal-N comparisons on record in §2.93.B4, re-computed). Section 4.2 is now "Z = 92: Not Supported at Fixed N". Sections 3.1–3.2, 4.3–4.4, the N-correlation limitation, the Conclusions and the figure caption are adjusted to match. The quoted sentence is gone |
| 3 | Section 4.5: the decay-chain "terminus", "No parameter is adjusted", ref. [11]; or drop Sections 4.5–4.6 | **Sections 4.5–4.6 are dropped.** They were the paper's only tie to the SQT framework, which V4.97 closed. Ref. [11] did not contain J(θ) or Lemma θ, and the Curium prediction they motivated failed. The "Note on version 2" records all of this, so the failed prediction stays on record. Limitations becomes Section 4.5 |
| 4 | Ref. [9] "[Citation pending]": complete it or remove the sentence | The sentence and ref. [9] are removed (a citation cannot be completed without checking it). Akrawy (2020) becomes [9] |
| 5 | The abstract's "Cm→Cf half … confirmed" (t = +0.4) | Removed with Sections 4.5–4.6. The version note says why |

Two further changes follow from these:
- **The title.** It is now "Isotone Steps of α-Decay Q-Values in the Deformed Actinide Region: A Robust Break at Radium (Z = 88)", because a paper that claims one break cannot be titled "Three-Regime Structure". The old title can be restored in one line of `build_v2.py`.
- **The byline** follows F5: "Matthew Gifford (independent researcher, Hollister, CA)". The version line cites version 1's DOI and date. The store copy's "Draft notes for revision" block is removed, since every note in it is now resolved.

**If you would rather keep Sections 4.5–4.6** (correction 3's first option), they need these changes:
- remove "the terminus toward which all actinide chains converge" (only the 4n series ends at ²⁰⁸Pb);
- replace "No parameter is adjusted" with a statement that the U↔θ map is read from the data;
- replace ref. [11], which does not contain the material;
- make the abstract's Curium sentence match §4.6 ("not confirmed");
- check §4.6's σ values: they are population SDs (0.072, 0.079), while Table 1 uses sample SDs (0.078, 0.086).

## Zenodo version note (proposed text)

> Version 2 (October 2026) corrects version 1 (May 29, 2026). The data, the AME2020 Q-values and the regime table are unchanged. The step count for N > 128 is corrected from 74 to 51; 74 counts all N. The paper now claims one robust break, at Z = 88 (Ra). Compared at fixed neutron number, the step across Z = 88 rises at every shared N. The apparent break at Z = 92 changes sign at fixed N and reflects the groups' different neutron coverage, so it is no longer claimed. Sections 4.5–4.6 are removed: a structural account drawn from a separate framework, and the Curium prediction it motivated, which the data did not confirm. The reference cited for that account did not contain it. An incomplete citation and the sentence relying on it are removed, and the abstract no longer says half of the Curium prediction was confirmed. The title is changed to match.

## Facts used and one still open

- **Used:** the DOI 10.5281/zenodo.20448930 and the deposit date May 29, 2026 (the author's F3); Hollister, CA (F5).
- **Not answered (F3's second part): is the deposit the same text as the May 28 store copy?** Version 2 is built on the store copy. If the deposited version 1 differs, the same five corrections apply, but the anchors in `build_v2.py` may need to move.

## Addendum, October 8, 2026: F3 answered
You confirmed that the deposited version 1 is exactly the May 28 store copy (the directive of 08:43 PDT). So `v1_to_v2.diff` is the diff from the deposited text, and the anchors in `build_v2.py` stand as they are. Nothing is deposited.
