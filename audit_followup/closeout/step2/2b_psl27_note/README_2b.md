# PSL(2,7) note, version 3: close-out draft (Step 2b)

**Plain-language summary.** The Phase B draft of the PSL(2,7) note (v3) gets three more changes:
- the abstract now says the note *records* its results, since they are classical, rather than *establishes* them;
- the title drops "rigidity" and "crystallization";
- the running head matches the new title.

The brief asked for two title proposals, so the draft is built twice, once with each title. Every change is a tracked change against the author's v2.1 file, so each one can be accepted or rejected in Word. Nothing is deposited. No withdrawal letter is drafted, because no journal submission is open (F2 default).

## The two title proposals

| | Title | Running head |
|---|---|---|
| **A** (recommended) | **The Seven-Point Coset Geometry of PSL(2,7): Spectral Gap, Cheeger Constant and a Smith Obstruction** | The Seven-Point Coset Geometry of PSL(2,7) |
| **B** | **PSL(2,7) on Seven Points: A Spectral Record of the Gelfand Pair (PSL(2,7), S₄)** | PSL(2,7) on Seven Points |

A lists what the note contains: the gap λ₁ = 2/3, the Cheeger constant h = 8/21 and the orbifold result. B names the classical structure that the new prior-art paragraph explains. Both drop "spectral rigidity", which names Schur's lemma, and "crystallization", which no theorem in the note supports.

## Files

| File | What it is |
|---|---|
| `PSL27_v3_CLOSEOUT_DRAFT_titleA_tracked.docx` / `.pdf` | v2.1 → v3 with title A. Every change is tracked, author "Claude (audit draft)" |
| `PSL27_v3_CLOSEOUT_DRAFT_titleA_clean.docx` / `.pdf` | The same, all changes accepted (12 pages) |
| `PSL27_v3_CLOSEOUT_DRAFT_titleB_*` | The same pair with title B |
| `make_v3_closeout.py` | Edits E11–E14, applied after Phase B's `make_v3_tracked.py` (E1–E10) |
| `build_v3_closeout.sh` | Rebuilds both drafts from the v2.1 source. It checks the source md5 (`9e809324…`) and validates the result against v2.1 with the tracked-changes author check (`build_log_A.txt`, `build_log_B.txt`: "All validations PASSED!") |
| `MANIFEST.txt` | md5 and size of each draft |

## The close-out edits (E11–E14)

| Edit | Where | Change |
|---|---|---|
| E11 | Abstract | "and establish four main results" → "and **record** four main results" |
| E12 | Abstract | "we establish via Smith's theorem" → "we **record** via Smith's theorem". The brief says "establishes" → "records"; the abstract has the verb twice, in the form "establish", so both are changed |
| E13 | Title (two lines) | Proposal A or B |
| E14 | Running head | Shortened to match |

The Phase B edits E1–E10 are unchanged (`phase_b/B2/B2_RESULT.md`): the prior-art paragraph and abstract sentence, the 146-element count in Open Problem 4.4, the index-theory sentence, and the reference fixes. The verb also appears twice in the Introduction ("to establish this characterization"; "We also establish, as an independent result"). It is left unchanged there, because the brief named only the abstract. The other two uses, in Sections 4.1 and 4.2, are about other things ("no established map"; "stability established in Lemma 2.9").

## Zenodo version note (proposed text)

> Version 3 (October 2026) adds no new result and changes no theorem. It now says plainly that its main spectral statements are classical. The group acts 2-transitively on the seven cosets of S₄, so (PSL(2,7), S₄) is a Gelfand pair, and the distance-transitive actions of the groups between PSL₂(q) and PΓL₂(q) are classified (Faradžev and Ivanov, 1990). The note records the case q = 7 in spectral language, and its abstract says so. One count in Open Problem 4.4 is corrected: 146 group elements fix a circle on the 7-sphere, not 104, because the 42 elements of order 4 were left out. The same problem's description of the index theory it needs is corrected, since Kawasaki's theorem is not limited to isolated singularities. The title drops "spectral rigidity" and "crystallization": the first is a name for Schur's lemma, and no theorem in the note stands behind the second. Smaller fixes correct a reference year, an appendix label and a superscript, and six classical references are added.

**Assumption carried from Phase B (F2 default).** The v2.1 file is the text deposited as Zenodo v2 (10.5281/zenodo.20532770). The Zenodo record could not be fetched from here.

## Addendum, October 8, 2026: title A chosen
You chose title A ("For the PSL(2,7) note, we will proceed with Title Option A"; the directive of 08:43 PDT). The files to deposit are `PSL27_v3_CLOSEOUT_DRAFT_titleA_clean.docx` and `.pdf`; the tracked pair is there for your review. The title B files stay as drafted. Your confirmation of F2 also settles the assumption above: v2.1 is the Zenodo v2 text, and no submission is open. Nothing is deposited.
