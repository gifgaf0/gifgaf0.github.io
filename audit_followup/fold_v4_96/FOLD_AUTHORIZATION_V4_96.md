# FOLD AUTHORIZATION — V4.96 (the polycrystal floor elected, N = 50)

**Plain-language summary.** This fold records the author's choice of 50 lattice cells as the minimum grain size, with its consequences, in a short new §2.96 and ten pointers.
- **The consequences.** At that floor the photon data require a lattice spacing of at most 0.026 Planck lengths. The ledger's declared lattice leaves no light window on any photon arm.
- **The author's two sentences.** §2.96 also says which verdicts rest on which data. The first sentence gained one qualifier. The second was scoped, because the TeV arms already exclude a Planck-length lattice at N = 50 without any PeV photon. Details below.

Nothing in the ledger was changed or removed, and the independent check confirms that.

**Recorded:** October 7, 2026, 20:15 PDT (October 8, 03:15 UTC).

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_95_CANONICAL.md`, md5 `3b6c11c33fdc88566f8cc1774d2d6a7b` (1,871,378 B), the output of the V4.95 fold |
| Result | `SQT_Master_Ledger_v4_96_CANONICAL.md`, md5 `120b076a613b7ef4074193c03df2cf0d` (1,877,637 B; +6,259 B, +5,972 characters) |
| Kind | Records an author election and its consequences. These are arithmetic on the §2.95 two-leg numbers, so there is no new derivation and no second leg |
| Edits | E1 title; E2 As-of prepend; E3 the V4.96 fold-in record (before the V4.95 record); E5 §2.96 (after §2.95, before Cluster J); E6 ten in-line "[→ V4.96 (§2.96): …]" pointers; E8 one changelog line. No Preamble rule and no new Part VI row: the election is recorded on the floor row itself |
| Not touched | Every existing sentence (pointers are appended only); the fold-in records and the As-of history; §2.92.A (the A1 verdict); the frozen §2.52 Open 3 row; no §3.x |

## The author's words (verbatim)

The election, Wednesday, October 7, 2026, 19:16 PDT:

> I select N = 50

The fold word, the same day, 20:05 PDT:

> Fold it as V4.96 now. In §2.96, add two sentences if they aren't already there:
> (1) With the PeV bound, the no-window verdict holds for every N ≥ 2; N = 50 sets only the quoted spacing (0.026 ℓ_P, or 0.055 at 10× the loss).
> (2) Without the PeV data, the declared-chain verdict needs N ≥ 20, and a Planck-length lattice would fit the original window up to N ≈ 230, so the Planck-lattice verdict depends on the PeV data.

## How the two sentences were folded

Neither sentence was already in the staged §2.96. Both now sit in a paragraph headed "What rests on which data". Every number is from the two-leg record (`ls_leg1.json`, agreeing with `leg2/ls_leg2.json`).

The quantity used below, N_P, is the largest number of cells a grain can hold if the lattice spacing is ℓ_P: N_P = d_max/ℓ_P.

**(1) Folded with one qualifier.**
- With the PeV arms, N_P = 1.28, so the no-window verdict holds for every N ≥ 2, as the author wrote. N = 50 sets only the quoted spacing, 0.0257 ℓ_P (0.0553 at τ × 10).
- At 10× the loss, however, N_P = 2.77. A Planck-length lattice then still fits N = 2 cells, so the verdict holds from N ≥ 3. The folded sentence adds "(for a Planck-length lattice at 10× the loss, every N ≥ 3)".
- The declared-chain verdict holds for every N ≥ 1 under both readings (N_D = 0.11, and 0.24 at 10×), so N ≥ 2 covers it.

**(2) Its facts were folded; its conclusion was scoped.**
- **The facts hold.** On W^EM_∪'s original anchor alone:
  - N_D = 19.82, so the declared-chain verdict needs N ≥ 20;
  - N_P = 232.9, so a Planck-length lattice fits up to N ≈ 233. This is the author's "≈ 230", given to the precision the ledger already quotes.
- **The conclusion does not hold as worded.** The conclusion "the Planck-lattice verdict depends on the PeV data" holds only for 2 ≤ N ≤ 6. The bound also has two TeV arms, which carry no PeV photons:

  | TeV arm | N_P | At 10× the loss | Declared chain, N_D |
  |---|---|---|---|
  | Mrk 501 (16 TeV) | 6.49 | 13.99 | 0.55 |
  | GRB 221009A (7.7 TeV) | 10.77 | 23.19 | 0.92 |

  So without any PeV photon, a Planck-length lattice is already excluded for N ≥ 7 (N ≥ 14 at 10× the loss), and at the elected N = 50 in particular. The PeV arms extend this to N ≥ 2 (N ≥ 3 at 10×). The TeV arms also leave the declared chain no window for any N ≥ 2 (for any N ≥ 1 at the threshold).
- **The folded wording.** The author's two facts are kept, and a sentence follows that states what the TeV arms already close and where the PeV data matter.

If the author wants different wording, a later fold can add it; this fold changes nothing already written.

## Where the pointers go (V4.95 line numbers)

| Line | Entry |
|---|---|
| 297 | ANNEX-CDEF-1 (the transverse scale import) |
| 1660 | §2.91.M, G-POLY1 (the polycrystal postulate's promotion gate) |
| 1662 | §2.91.N, G-CI1 (W^EM_∪) |
| 1692 | §2.92.E (the one transverse light carrier) |
| 1730 | §2.95, "The bound" |
| 4407 | Part V: the polycrystalline-vacuum (VRH) exploration row, where the postulate is banked R3 |
| 4446 | Part VI: G-CI1 row |
| 4450 | Part VI: G-S2C1-W row |
| 4465 | Part VI: the polycrystal-floor row (**ELECTED — N = 50**) |
| 4466 | Part VI: the lattice-spacing-bound row |

## Repository state at fold (live `git ls-remote`, 2026-10-08 03:08:33 UTC)

| Ref | Value |
|---|---|
| `refs/heads/main` | `3587eb3098e4f7652685e4f16de5cd7583a9fa4a` |
| `refs/heads/claude/audit-followup-oct6` | `48c57b83f686014c4eb11c523aeeadb188233b6b` (the estate through the staged fold with the author's paragraph) |

No canonical ledger is committed to the repository; the V4.96 file is delivered in the conversation. The repository is public.

## Project store

The store is not changed by this fold.
- **What it holds.** The author's upload of V4.95 (2026-10-08 02:17:54 UTC) is byte-identical to the canonical (md5 3b6c11c3…).
- **Room.** Re-read at fold time, it holds 1,994,291 of 2,000,000, so 5,709 are free.
- **The swap.** V4.96 is 6,259 B larger than V4.95, so a delete-and-write swap does not fit by about 550 B. It needs the author's word plus about 0.6 KB freed.

## Verification

- **Fold script:** `foldin_v4_96_floor_election.py`, md5 `99652ea4bb82bdd3ac4a02d29ad5198c`, run with the fold word, its time, the estate head and the live ls-remote facts. Log: `fold_v4_96_output.txt` (md5 `2c1cea0008123a05f23191d3b4f919ff`).
  - Every anchor is read from the file and asserted unique, and every fragment lands exactly once.
  - The reverse splice reconstructs V4.95 byte-identically.
- **Independent check:** `verify_v4_96_additive.py`, md5 `9d6c7da73a3cd9418575d2fa7bf48018`. Log: `verify_v4_96_output.txt` (md5 `60e32847af370a53628d68c0cd00e0e9`).
  - **Survival.** Every V4.95 line survives: 4,715 unchanged, 10 as in-line appends on exactly the ten lines above (each containing its typed keyword), and the title and As-of rewrites.
  - **Insertions.** Fifteen lines (4,191 B) are inserted in three blocks: the record, §2.96 (six paragraphs, including "What rests on which data") and the changelog line.
  - **Fixed rows.** §2.92.A and §2.52 Open 3 are unchanged.
  - Result: PASS.
- **Staging history.** The fold was staged and dry-run after the election (commit `6da1d8d`). At the fold word, the author's paragraph was added to the script, and the check's paragraph count for §2.96 was raised from 4 to 6 to match. Both changes were committed (`48c57b8`) and dry-run again before the canonical run.
