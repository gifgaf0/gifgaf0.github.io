CLOSE-OUT BRIEF: fold V4.96, close the substrate program (V4.97), clear Phases A–C
Base: V4.95 plus the staged V4.96. Attached: CLOSING_ENTRY_V4_97_DRAFT.md, my
approved text for §2.97. Fold it as written, apart from the fill-ins below and
mechanical fixes (anchors, pointer format, date). If you find a factual error in
it, report it; don't change it silently.

MY FACTS AND ELECTIONS (blank = use the default and flag it in the report)
F1. Is the gauge paper under review at any journal? ______
    Default: no. §2.93.B1(4) records "v5" as its Zenodo version number, and
    FFA-26-260 as the PSL(2,7) note, declined.
F2. PSL(2,7) note: is v2.1 the Zenodo v2 text (10.5281/zenodo.20532770)? ______
    Is any journal submission still open? ______   Default: yes; none.
F3. Alpha-decay deposit: DOI ______  date ______
    Same text as the May 28 store copy? ______   No default: leave placeholders.
F4. Is the old public calculator live? ______
    Default: check the repository's Pages setup and report.
F5. Byline for every new output: ______   Default: Matthew Gifford, matching the
    Zenodo records. Contact for the ePrint: ______
F6. Titles. Gauge paper: ______   Default: "Gauge Group and Generation Structure
    from the Császár Polyhedron". PSL(2,7) note: ______   Default: propose two.
F7. §2.52 Open 3 at closure: ______   Default: §2.97.C(f) as drafted (text
    untouched, listed as closed with the program).

HOW TO WORK
- Nothing here should need a new derivation. If one turns out to be needed,
  stop and report.
- One short fold per step, with the usual reverse-splice and additivity checks.
  Prior Address, Eddington and M.CW apply. Every deliverable opens with a
  plain-language summary.
- Draft, don't publish or send. Deposits, deployments, journal letters and the
  ePrint come back to me. I'll send the Flach note myself.
- The canonical ledger lives in the repository from now on. The project store
  keeps STATUS.md and the phase reports.
- The repository is public. Keep letters (to editors, to Flach) in the project
  store, not on the branch, and move FLACH_NOTE_DRAFT.md there.
- Don't open a successor program.

STEP 1. TWO FOLDS
1a. V4.96, as staged. Make sure §2.96 says:
    (1) with the PeV bound, the no-window verdict holds for every N ≥ 2, and
        N = 50 sets only the quoted spacing (0.026 ℓ_P; 0.055 at 10× the loss);
    (2) without the PeV data, the declared-chain verdict needs N ≥ 20, and a
        Planck-length lattice would fit the original window up to N ≈ 230, so
        the Planck-lattice verdict depends on the PeV data.
1b. V4.97: fold §2.97 from the attachment, after §2.96. The sweep:
    - Classify every Part VI row that is Open, Registered, Standing or
      Partially executed by §2.97.C rules (a)–(h).
    - One [→ V4.97 (§2.97)] pointer on each row closed by (a), moved by (e), or
      split by (b) (rows that join math to a physical mapping). No pointer on
      pure-math, crypto or author-action rows, or on rows already closed or
      retracted.
    - One banner line at the head of each Part II cluster whose subject is
      substrate physics (list which), and at the heads of Parts IV and V.
    - Part VI: add the rows "Substrate program — CLOSED (V4.97)" and
      "Successor program — NOT OPENED (conditions §2.97.D)", and move the C(e)
      rows into a "Successor intake (not opened)" block, text unchanged.
    - One pointer each on the Preamble's M.ONT header (closed) and KC-EP header
      (standing), and on §2.91.D's kill set (standing).
    - Update the Status and As-of lines and STATUS.md.
    Report the classification table (row → rule) and every row you could not
    classify. Count check: every Open/Registered/Standing/Partially executed
    Part VI row appears in the table exactly once.

STEP 2. PUBLIC CORRECTIONS (drafts only)
2a. Gauge paper, from v6.4:
    - Aut(ℍ) = SO(3), not SU(2): the unit quaternions act by conjugation, with
      kernel ±1. Fix §3, §4 and Open Problem (xi).
    - §7.4 is backwards. A torus embedded in ℝ³ inherits the spin structure
      induced from ℝ³, which is even (Arf 0): antiperiodic around two of the
      three nonzero classes of H₁(T²; ℤ₂) and periodic around one. The
      all-periodic structure is the odd one, and no embedding induces it.
    - Uniqueness of the 7-vertex torus triangulation is classical; cite a
      standard source. Bokowski & Eggert (1991) classify its realizations in
      ℝ³, as their title says.
    - Title per F6. A one-paragraph Zenodo version note in plain terms: the
      withdrawn hypercharge sign rule, sin θ_C = 3/13 excluded, tan θ_C
      labelled post hoc, and the three fixes above.
    - If F1 is yes: a short letter to the editor with the corrections, plus a
      withdrawal alternative. Project store only.
2b. PSL(2,7) note v3: "establishes" → "records" in the abstract; title per F6;
    a Zenodo version note. If F2 names an open submission, draft a withdrawal
    letter (project store).
2c. Alpha-decay deposit: a corrected version with the five §2.93.B4
    corrections and a version note, using F3.
2d. Public calculator: if it is live, prepare v3.1 with a one-line banner
    ("Archived, V4.97: a fitted mass table with named inputs; the program it
    belonged to is closed"). As an alternative, prepare a stub index.html that
    points to the archive. Deploy nothing.
2e. Crypto repository files: correct tools/lattice_estimate_results.md and
    tools/SLWE_Prime_Master_v2.md §4.4 to the §2.94.C1 figures. Commit on the
    working branch; I'll merge.

STEP 3. NEW OUTPUTS (package only)
3a. Second-sound v1: byline per F5, cover note removed, nothing else changed.
    Export the PDF and source for my last read.
3b. SLWE ePrint: byline and contact per F5, and a one-sentence AI-assistance
    acknowledgement for me to approve. Export the final PDF. Don't submit.

STEP 4. ARCHIVE, THEN THE LAST BATCH
4a. Paper VII and the two store calculators: apply the B3 drafts, remove Paper
    VII §10 (gravitational waves), rename "Theorem 1" so that its name says it
    is a fit, and add an "Archived at V4.97" header. No deployment or deposit.
4b. One fold (V4.98) for the remaining mathematics:
    - §2.76's claim that the sum-15 (a + b = 15) twosets are all χ = −1 (the
      Phase C report's "L2427");
    - the §2.53 imaginaries column from the findings file;
    - every item on Phase C's "found, not annotated" list that is mathematics
      or crypto.
    Physics items on that list are covered by §2.97 and get no separate note.

REPORT
One report at the end:
- what folded (V4.96–V4.98);
- the classification table and the unclassified rows;
- every draft awaiting me, with its path;
- any fact you needed and didn't have.
