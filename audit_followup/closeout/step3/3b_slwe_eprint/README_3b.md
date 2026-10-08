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
