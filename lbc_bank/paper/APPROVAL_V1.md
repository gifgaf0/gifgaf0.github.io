# The author's approval of the paper draft (October 4, 2026)

**Plain-language summary.** The author approved the revised draft of the second-sound paper. This note records the approval word for word and pins exactly which text was approved, so the posted version can be checked against it. The posting version removes the cover note for the author and changes nothing else. Approving the paper folds nothing into the ledger: the one ledger figure the revision changes still waits for its own word (`../closure/NEXT_FOLD_NOTE.md`).

## The author's words (verbatim, October 4, 2026, 18:08 PDT)

> Approved draft

They answer the revision report sent after the second review. That report asked the author to confirm the wording of the acknowledgments, to decide on the title, and to remove the cover note before posting.

## What was approved

| Item | Value |
|---|---|
| Draft | `second_sound_light_cone_DRAFT.md`, md5 `a47080c26bb0a9c601912a5fa925a9f9` (53,859 B), commit `3664ed1` on `claude/lbc-bank-v489` (PR #35) |
| Title | Unchanged: "Second sound breaks the common light cone of a supersolid vacuum". The neutral alternative offered in the cover note was not taken |
| Acknowledgments | As worded: every check was made by AI agents, not by human referees |

## The posting version (v1)

| File | md5 | What it is |
|---|---|---|
| `submission/second_sound_light_cone_v1.md` | `0dc9b1ea59384bdca33e9980b6cbb8ef` | The approved draft with the cover note removed, and nothing else changed. The build asserts that the cover note plus v1 rebuilds the draft byte for byte |
| `submission/second_sound_light_cone_v1.tex` | `727a1ad4cd7283305729583a4744860e` | LaTeX from pandoc, with the two tables set as floats |
| `submission/second_sound_light_cone_v1.pdf` | `30ede2b2bf134caeb7f6f891d834ba5e` | 13 pages, A4, XeLaTeX. Byte-reproducible: the build fixes the dates |
| `submission/build_v1.py` | `3951a3fd47d5184d35a5a04d25d16c84` | Builds all three; with `--zip OUT` it also builds the supplementary zip |

**Checks.** Every PDF page was inspected as an image. Its extracted text was compared with the manuscript: every table entry, section heading and reference is present.

**Typesetting only.** The build changes no wording, number or symbol. It does six layout things:
- moves the title, author and abstract into the LaTeX title block;
- stacks the two formulas of Eq. (2);
- sets the references as a numbered list;
- makes the two tables floats;
- keeps units on the line of their numbers;
- sets the data-availability paragraph ragged right.

## Supplementary material

One zip holds `lbc_bank/` as committed together with this note, plus `lbc_bank/second_leg/` from `main`, with `SUPPLEMENT_MD5.txt` inside.
- It is not committed. `build_v1.py --zip OUT` rebuilds it byte for byte from the same commits (fixed timestamps, sorted entries).
- It holds no canonical ledger and none of Cox's text.

## What is left, and whose it is

- **Posting on Zenodo** (CC-BY-4.0) needs the author's account. Upload the PDF and the zip; the metadata can follow the venue note (`VENUE_AND_SUBMISSION.md`).
- **Merging PR #35** puts the paper's evidence on `main`, which is where its data statement points (`lbc_bank/` in the public repository).
- **Journal submission** follows the venue note: *Classical and Quantum Gravity*, with *Physical Review D* as the backup.
