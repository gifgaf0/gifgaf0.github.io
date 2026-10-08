# Phase B report: papers and calculators (October 7, 2026)

**Plain-language summary.** Phase B corrected the program's public work. Everything it produced is a draft for the author. Nothing has been published, deposited, deployed or sent.
- **Gauge paper.** It needs a correction. Its one addition to Furey's charge formula is inconsistent, and its Cabibbo value is ruled out by current data. A v6.4 is drafted.
- **PSL(2,7) note.** It is mathematically sound. A v3 cites the classical literature and fixes one count.
- **Paper VII and the three calculators.** They now say what the mass table is: a leading-order fit with named inputs, not "zero free parameters". The W-mass and weak-angle formulas are retired.
- **Alpha-decay paper.** Its data are right, but only one of its two breaks holds up. It now has a ledger entry.
- **The Flach question.** The η-invariant calculation once put to Flach no longer serves its purpose. A short note to him is drafted.
- **Second-sound paper.** It already had every fix the audit asked for, so it can be posted as approved.

The ledger is folded to V4.93 (+22 KB), and 34 dependent entries carry a pointer to the new section.

## What came out

| Part | Finding | Draft | What it needs from the author |
|---|---|---|---|
| **B0** second-sound paper | All eight requested fixes are already in v1, approved October 4 | None needed | Post v1 and submit |
| **B1** gauge paper v6.3 | • The hypercharge sign rule is inconsistent: verdict (N-I), two legs agreeing 32/32.<br>• sin θ_C = 3/13 is 7.6σ and 8.5σ from PDG 2024; the tan θ_C reading fits but was chosen after the data.<br>• The paper never says PSL(2,7) is the polyhedron's symmetry group; that claim was the ledger's own.<br>• Per the ledger, the paper is not under review at FFA | v6.4, 23 anchored edits | Approve v6.4 for Zenodo, decide the title, and decide whether to keep the post-hoc tan θ_C remark. Confirm the FFA question |
| **B2** PSL(2,7) note | • Sound.<br>• Prior art added.<br>• 146 circle-fixing elements, not 104.<br>• The Kawasaki sentence was wrong.<br>• The D₄ error was already fixed in v2.1 | v3 as Word tracked changes, plus clean .docx and PDFs | Confirm that v2.1 is the Zenodo v2 text. Approve v3 and decide the title |
| **B3** Paper VII and calculators | • Scoped wording replaces "Zero Free Parameters".<br>• m_W = m₀φ²⁷ (132σ off) and sin²θ_W = φ⁻³ (no scale or scheme) are retired.<br>• F₇* is not inside PSL(2,7).<br>• Quark rope lengths are per diameter, the others per radius | Public calculator v3.1, `SQTCalculator.jsx` v2.1, `sqt_v20_merged.jsx` v1.9.1, Paper VII | Approve and deploy. Paper VII §10 (gravitational waves) and the name "Theorem 1" need your review |
| **B4** alpha-decay paper | • The Q-values are right.<br>• 51 steps, not 74.<br>• One robust break, at Z = 88. The Z = 92 "break" changes sign at fixed neutron number.<br>• §4.5–§4.6 rest on retracted pieces.<br>• The abstract overstates the Curium test.<br>• ²⁰⁸Pb already has Q_α > 0 | Ledger entry §2.93.B4 and a list of five corrections | Give the deposit's DOI and date, and decide whether to correct it |
| **B5** η / Flach | The η calculation's purpose closed at V4.84. The space on record is S⁷/PSL(2,7) | `FLACH_NOTE_DRAFT.md` | Check which space your message named, then send or not |

## Blast radius

There are 34 brackets: B1 15, B2 3, B3 10, B4 4 and B5 2. There are also three new Part VI rows: the Phase B closure, the drafts awaiting you, and the alpha-decay correction.

The result files' tables listed 23 of the brackets. A sweep of the whole ledger at fold time found 11 more dependents:
- five places tied to "PSL(2,7) is K₇'s symmetry group", including one that credits the PSL(2,7) note with the claim (the note says no such thing);
- the W and Z rows;
- a second F₇* passage;
- the Flag 4 list item;
- the M.CW one-break record;
- §2.87's sentence tying the neutron moment to the Flach question.

The full list is in `fold_v4_93/FOLD_AUTHORIZATION_V4_93.md`.

## Decisions waiting on you

1. **Approvals.** Each of these is drafted and waits for you:
   - the gauge paper v6.4 and the PSL(2,7) note v3, for Zenodo;
   - the public calculator, deployed as `index.html`;
   - the two store calculators and the Paper VII draft;
   - the note to Flach;
   - posting the second-sound v1.
2. **Facts only you have:**
   - whether v2.1 is the text deposited as Zenodo v2;
   - the alpha-decay deposit's DOI and date, and whether it matches the May 28 store text;
   - which space your message to Flach named;
   - whether the gauge paper went to FFA (the ledger says it did not).
3. **Choices.**
   - B0 item 4: v1 renamed the chemical potential, while the brief asked to rename the shear modulus. Both remove the clash.
   - B3: the drafts retire the two electroweak formulas rather than scope them. Scoping would need a scale and scheme for φ⁻³ and a derivation of 27.
   - Conjecture 1: restate Z_f = 6 as |S₃|, or keep F₇* acting somewhere else (for example through AGL(1,7)).
   - The alpha-decay deposit: whether to correct it.
4. **The ledger.** The V4.93 file is attached. The project store still holds V4.91 and has 1,983 units free. Swapping in V4.93 needs your word and about 42 KB freed, or an instruction to keep the canonical ledger in the repository.

**Visibility.** The repository is public. The drafts on branch `claude/audit-followup-oct6` can be read by anyone, although none is published, deployed or deposited. If that matters, the repository can be made private or the drafts moved.

## Process notes

- **Blind leg held.** B1's second leg started only after the first leg was committed, which repairs Phase A's exposure pattern.
- **Fold-time corrections.** Four statements in the B4 file and one in the B5 file were tightened at the fold. Each file now ends with a note.
  - The paper and the ledger's slot framework count U from different origins, so "the paper's edges are the retracted 4-8-12 sequence" was withdrawn.
  - Capacity readings of the paper's edges depend on measuring U from mercury.
- **Proportionality.** Only B1 had a verdict decided by a new derivation, so only B1 was pre-registered and given a second leg. The rest are annotations, each computed once.

## Files

Everything is on branch `claude/audit-followup-oct6`:
- `audit_followup/phase_b/B0`–`B5`: results, check scripts and outputs, and the drafts;
- `audit_followup/fold_v4_93/`: the fold script, the independent check and the authorization record;
- `STATUS.md` at the repository root, updated.

The canonical `SQT_Master_Ledger_v4_93_CANONICAL.md` (md5 `0aa63a0bec9becbfb911dba3454255f2`) is delivered in the conversation.
