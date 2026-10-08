# FOLD AUTHORIZATION — V4.97 (closing the substrate program)

**Plain-language summary.** This fold adds the author's closing entry, §2.97, to the ledger. The entry closes the supersolid-vacuum program, says what carries forward and sets the conditions for any successor. The fold then marks every affected open item in the task list (Part VI) with a short pointer.
- §2.97 is folded as approved, apart from four mechanical changes:
  - the date is entered;
  - the review note is removed;
  - the bracketed alternative in C(f) is left out (the F7 default);
  - the "move" of the successor-intake rows is done by reference, because the ledger never moves or deletes rows.
- 43 task rows got a pointer: 27 close with the program, 14 keep their mathematics open while the physical reading closes, and 2 go to the successor intake. Two rows are left to the author.
- Three factual points in the approved text are reported below and were not changed.

Nothing already in the ledger was changed or removed, and the independent check confirms that.

**Recorded:** October 8, 2026, 07:45 PDT (14:45 UTC).

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_96_CANONICAL.md`, md5 `120b076a613b7ef4074193c03df2cf0d` (1,877,637 B), the output of the V4.96 fold |
| Result | `SQT_Master_Ledger_v4_97_CANONICAL.md`, md5 `a5a07bcd4f8ca13c87f65974d5580f24` (1,903,201 B; +25,564 B, +25,072 characters) |
| Kind | A decision record. Nothing is newly derived, so there is no pre-registration and no second leg (the proportionality rule, as §2.97 states) |
| Source text | `audit_followup/inputs/CLOSING_ENTRY_V4_97_DRAFT.md`, md5 `10270b68a446f6025331f132f8d48038`. Byte-identical to the attachment the author sent with the brief |
| Edits | **E1** title; **E2** As-of prepend; **E2b** a V4.97 note at the head of the Status line; **E3** the V4.97 fold-in record (before the V4.96 record); **E4** pointers on the Preamble's KC-EP header (standing) and M.ONT header (closed) and on §2.91.D's kill set (standing); **E5** §2.97, after §2.96 and before Cluster J; **E6** 43 Part VI row pointers (`closeout/CO1_CLASSIFICATION.md`); **E7** 11 banner lines; **E8** two Part VI rows after the lattice-spacing-bound row; **E9** the Successor intake block before "Closed / dropped"; **E10** one changelog line |
| Not touched | Every existing sentence (pointers are appended only); the fold-in records and the As-of history; §2.92.A; the frozen §2.52 Open 3 row and §2.52's body; the rows already closed (G-POLY1, §3.4-G2-CHIRAL, G-QUANTA, ζ-tax gate 3, the polycrystal floor, the factor-assignment question); no §3.x |
| Checks | Reverse splice byte-identical to V4.96 (`fold_v4_97_output.txt`). The independent check (`verify_v4_97_additive.py`, `verify_v4_97_output.txt`) also passes: 46 appends on exactly the typed lines, each saying what its rule says; 16 insertion blocks, all at declared places; §2.97 equal to the approved draft plus its two fill-ins. A dry run passed the same checks first (`dryrun_*_output.txt`), and its file was deleted |
| Estate | Branch `claude/audit-followup-oct6`, head at fold `87566bb`; live `git ls-remote` 2026-10-08 14:42:35 UTC: main = `3587eb3`, remote branch = `f1974c5` |

## The author's words (verbatim)

From the close-out brief, received Wednesday, October 7, 2026, 22:19 PDT (`inputs/BRIEF_2026-10-07_close_out.md`):

> Base: V4.95 plus the staged V4.96. Attached: CLOSING_ENTRY_V4_97_DRAFT.md, my approved text for §2.97. Fold it as written, apart from the fill-ins below and mechanical fixes (anchors, pointer format, date). If you find a factual error in it, report it; don't change it silently.

> 1b. V4.97: fold §2.97 from the attachment, after §2.96. The sweep:
>     - Classify every Part VI row that is Open, Registered, Standing or Partially executed by §2.97.C rules (a)–(h).
>     - One [→ V4.97 (§2.97)] pointer on each row closed by (a), moved by (e), or split by (b) (rows that join math to a physical mapping). No pointer on pure-math, crypto or author-action rows, or on rows already closed or retracted.
>     - One banner line at the head of each Part II cluster whose subject is substrate physics (list which), and at the heads of Parts IV and V.
>     - Part VI: add the rows "Substrate program — CLOSED (V4.97)" and "Successor program — NOT OPENED (conditions §2.97.D)", and move the C(e) rows into a "Successor intake (not opened)" block, text unchanged.
>     - One pointer each on the Preamble's M.ONT header (closed) and KC-EP header (standing), and on §2.91.D's kill set (standing).
>     - Update the Status and As-of lines and STATUS.md.

The author's facts, Thursday, October 8, 2026, 07:09 PDT, taken as the go-ahead:

> F1. Gauge group paper isn't under review
>
> F3. https://doi.org/10.5281/zenodo.20448930. 5/29/26
>
> F5. Hollister CA

## Fill-ins and mechanical fixes

1. **Review note removed.** The HTML comment at the head of the draft says "remove this note before folding".
2. **Date.** "October [DATE], 2026" became "October 8, 2026".
3. **C(f).** The bracket "[AUTHOR: or keep it as a frozen historical row, outside the closure.]" is left out, which is the F7 default. C(f) now reads as drafted otherwise. The §2.52 Open 3 row is not touched. It is listed as closed with the program in the new "Substrate program — CLOSED" row.
4. **C(e) by reference.** The brief asks for the C(e) rows to be moved. Moving them would delete them from where they stand, which append-only forbids. So the intake block lists each item by reference with its current status of record, and the two open rows (G-RCX1, §3.4-G2-knot) carry a pointer to it. The rows' texts are unchanged.

## Factual points in the approved text (reported, not changed)

These are recorded in the V4.97 fold-in record as fold notes. §2.97 itself is folded as approved.

1. **C(e)'s list.**
   - §3.4-G2-CHIRAL is not "Faddeev–Hopf soliton work". It recomputes Milnor's μ̄ on idealized curves, and its row records ✓ CLOSED (V4.32, §3.09).
   - The Faddeev–Hopf rows are §3.4-G2-orient (closed, R1, V4.27) and §3.4-G2-knot (open).
   - G-QUANTA's row is CLOSED (V4.82).
   - §2.84 Part C is a Part II section, not a row.
   - The intake lists all five items as the text names them, each with its status of record.
2. **C(a)'s examples.**
   - G-POLY1's row records CLOSED: GATE COMPLETE (V4.76). It therefore gets no pointer, since the brief allows none on rows already closed.
   - G-ζ1 (executed V4.36), G-κ1 (V4.52), G-IIB-L1 (V4.64), G-CC-ε1 (V4.66) and the M.ONT gate (declared V4.51) had also run. They carry pointers because their rows' status still reads Open or Registered.
3. **B.2's register.** The text gives "(§2.93.B4, R2)" for the alpha-decay data and the Z = 88 observation. §2.93.B4 records the data at R1 and the Z = 88 break at R2.

The draft's other figures were checked against the sections it cites, and all of them match:
- 20.81 (§2.92.A);
- 0.79 and −39.2 orders (§2.91.V);
- 58.006, 758.7 MeV, 60.194 and 80.95 (§2.92.C);
- dof −1 (§2.92.C);
- I4, I6 and the immiscibility import;
- b = 1.003 ± 0.005 ± 0.010 (§2.94.C2 P1);
- 2.08×10⁻³⁵ m, 1.28 ℓ_P, 4.15×10⁻³⁷ m and 0.026 ℓ_P (§2.95, §2.96);
- the 10⁻²³ tuning (the second-sound paper);
- the Part V items named in C(g).

The B.3 quotations appear only in the approved draft and are taken as the author's own words.

## The sweep

- **Classification.** See `audit_followup/closeout/CO1_CLASSIFICATION.md`.
  - 163 Part VI table rows: 94 in scope, 69 out of scope.
  - Every row appears exactly once, and each lead status was machine-checked.
  - Two rows are left to the author under C(h): OP-C7-1 and OP-2.77-FB.
- **Pointers.**
  - On Part VI rows: 27 under (a), 14 under (b) split, 2 under (e).
  - On the Preamble and §2.91.D: KC-EP header (standing), M.ONT header (closed), §2.91.D kill set (standing).
- **Banners: 11.**
  - Part II clusters A (mass table), B (K₇ ε-per-edge), D (magnetism, heavy elements), E (Cayley–Dickson tower and hexagonal vacuum), F (Borromean confinement), H (angle as stored energy), I (scale ladders and the substrate sections §2.88–§2.96), N (continuum-limit fidelity) and O (conjectural re-readings).
  - Parts IV and V.
- **Part II clusters with no banner.**
  - **C** (Clifford tower): mathematics; its physics entry, §2.52, is handled by C(f).
  - **G** (the APS boundary term and the η offset): mathematics; the α⁻¹ application in §2.25.3–6 and the Gate 2a section §2.87.J filed there are physics.
  - **J** (the multi-lens reference): mathematics and method, with the short physics observations §§2.32–2.36 and §2.44.
  - **K** (the five-fold inventory): mathematics, with the physics-labelled angle band of §2.57.
  - **L**: mathematics.
  - **M**: crypto.

  C, G, J and K are mixed. A later fold can add banners there if the author wants them.
- **Part IV.** The banner names the sections C(a) lists: §4.7, §4.10, §4.11–§4.13 and §4.15. §4.14 (the Doc-3 intake audit) is not named in C(a). It is left for the author.

## Waiting for the author's word (not done)

- **The canonical ledger in the repository** ("lives in the repository from now on"). The repository is public and serves `main` as a website. Committing the ledger reverses the June 18 policy, and it cannot be undone once pushed. Until the author confirms, the ledger stays out of the repository, as before. It is reproducible exactly from the fold scripts and the base md5.
- **Deleting V4.95 from the project store**, to make room for STATUS.md and the phase reports.

## Addendum, October 8, 2026: fold note (3) withdrawn at V4.98

Fact 3 above is withdrawn, and §2.97.B.2's "(§2.93.B4, R2)" was correct as you wrote it.
- §2.93.B4 labels its arithmetic "Data (R1)".
- Its own disposition reads "The data and the Z = 88 observation are banked (R2)".
- §2.93's register line gives "R1 for the arithmetic, R2 for the dispositions".

B.2 quotes that disposition. The V4.97 record keeps its text and carries a [→ V4.98 (§2.98)] pointer that withdraws the note (`../fold_v4_98/FOLD_AUTHORIZATION_V4_98.md`).

## Addendum, October 8, 2026: the store copy is V4.96
"Deleting V4.95 from the project store" above should name V4.96. The store's copy has been V4.96 since October 7, 20:13 PDT, byte-identical to this fold's base (md5 `120b076a…`). See `../closeout/CLOSEOUT_FACTS.md` (addendum) and `../CLOSEOUT_REPORT.md`, section 4.
