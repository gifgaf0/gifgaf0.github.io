# FOLD AUTHORIZATION — V4.95 (the lattice-spacing bound)

**Plain-language summary.** This fold records one bound in one new ledger section, §2.95, and adds a short pointer to each entry the bound touches.
- **The bound.** All photon data together require the grains of a polycrystalline vacuum to be no larger than 2.08 × 10⁻³⁵ m, which is 1.28 Planck lengths. A grain of N lattice cells therefore needs a lattice spacing no larger than 2.08 × 10⁻³⁵ m / N, which is below the Planck length for any N ≥ 2.
- **Texture.** Any coherent grain alignment must be below about 10⁻³⁵.
- **Dispersion.** It does not bind.

It is a bound, not a verdict: nothing already decided is changed, and no scale is pinned. Nothing in the ledger was changed or removed, and the independent check confirms that. The project's stored copy of the ledger is not replaced (see below).

**Recorded:** October 7, 2026, 18:45 PDT (October 8, 01:45 UTC).

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_94_CANONICAL.md`, md5 `708df4cf8f4703088c89b4fad96584bd` (1,862,277 B), the output of the Phase C fold |
| Result | `SQT_Master_Ledger_v4_95_CANONICAL.md`, md5 `3b6c11c33fdc88566f8cc1774d2d6a7b` (1,871,378 B; +9,101 B, +8,506 characters) |
| Kind | One short fold recording a bound. Pre-registered; one leg, then a blind second leg because the pre-registered trigger fired |
| Edits | E1 title; E2 As-of prepend; E3 the V4.95 fold-in record (before the V4.94 record); E5 §2.95 (after §2.94, before Cluster J); E6 nine in-line "[→ V4.95 (§2.95): …]" pointers; E7 one Part VI row after the polycrystal-floor row; E8 one changelog line. No Preamble rule (no E4) |
| Not touched | Every existing sentence (pointers are appended only); the fold-in records and the As-of history (historical logs); §2.92.A (the A1 verdict); no §3.x |

## The author's words (verbatim, brief of October 7, 2026)

The full brief is saved as `audit_followup/inputs/BRIEF_2026-10-07_lattice_bound.txt` (md5 e6bdcf4edf0565f69dcca645c35275c1).

> Base: V4.94. This computes a bound. It is not a verdict on anything already decided.

> - State the result as a bound ("the data require a ≤ …"), not a prediction. Don't re-pin ξ or any other scale after seeing numbers.
> - One short fold recording the bound is authorized. Put a plain-language summary first. Write to the repo.

> - List what the result touches: the light-only transverse carrier, the polycrystal-floor row, and the ANNEX-SC-1 / G-S2C1-W chain.
> - Say in one sentence what it does not touch: the A1 polarization verdict, the A2 internal-mode friction, the second-sound drag and KC-EP.

> - One leg is enough. If the window comes out empty for every N ≥ 20 on every arm, run a blind second leg on the decisive arm before folding.

The standing rules of the October 6 brief also apply: "Draft, don't publish or send" and "Every deliverable opens with a plain-language summary."

## What was folded, and from where

| Step | File | Commit |
|---|---|---|
| Prior Address | `lattice_bound/LS_PRIOR_ADDRESS.md` (md5 1423d421…) | `65404f5` |
| Pre-registration | `lattice_bound/LS_PREREG.md` (md5 ea6651ce…), locked before any computation | `65404f5` |
| Leg 1 | `ls_leg1.py`, `.json`, `_output.txt` | `a9e6091` |
| The comparison, run last | `ls_compare.py`, `.json`, `_output.txt`: the trigger fires | `ebf150c` |
| The comparator, frozen before leg 2 | `ls_twoleg_compare.py` | `824f7fd` |
| Leg 2 (blind) and the comparison | `leg2/` and `ls_twoleg_compare.*`: 185/185, worst 4.8 × 10⁻¹⁵ | `4a4b7b0` |
| Result report | `lattice_bound/LS_RESULT.md` (md5 16cb33e3…) | `1322b2b` |

## Where the pointers go (V4.94 line numbers)

These are the entries the brief names, plus the two texture entries that the pre-registration (§10) named before any computation.

| Line | Entry | Why |
|---|---|---|
| 295 | ANNEX-CDEF-1 (the M.REL scale-axis annex: the transverse scale import, the ANNEX-SC-1 substitution clause) | the ANNEX-SC-1 / G-S2C1-W chain |
| 1634 | §2.91.H, G-SCALE1 (ANNEX-SC-1's declaration) | the ANNEX-SC-1 / G-S2C1-W chain |
| 1660 | §2.91.N, G-CI1 (W^EM_∪ of record) | the light window itself |
| 1670 | §2.91.S, G-MSCS2 (b₁ banked) | the texture bound uses b₁ |
| 1672 | §2.91.T, G-MSCS-A (the first-order polarization-split successor E-SA-1(b), unopened) | the texture bound is that observable's bound |
| 1690 | §2.92.E (the one transverse light carrier) | the light-only transverse carrier |
| 4432 | Part VI, G-CI1 row | the light window itself |
| 4436 | Part VI, G-S2C1-W row | the ANNEX-SC-1 / G-S2C1-W chain |
| 4451 | Part VI, polycrystal-floor row | the polycrystal-floor row |

**Two entries are deliberately left without pointers.**
- **§2.92.A.** It states the light-only carrier inside the A1 verdict paragraph. The brief says the bound does not touch the A1 verdict. §2.92.E carries the same carrier as a standing declaration, so the pointer goes there, and the independent check asserts that §2.92.A is unchanged.
- **The polycrystal postulate's own rows** (§2.91.M / G-POLY1 and the Part V VRH row). §2.95 says the postulate stays R3. Nothing in those rows is contradicted, because the bound uses their machinery and does not adjudicate the postulate.

## Repository state at fold (live `git ls-remote`, 2026-10-08 01:36:53 UTC)

| Ref | Value |
|---|---|
| `refs/heads/main` | `3587eb3098e4f7652685e4f16de5cd7583a9fa4a` |
| `refs/heads/claude/audit-followup-oct6` | `1322b2b9b0db7bcd99b37411872817682901a628` (the estate through the result report) |

No canonical ledger is committed to the repository; the V4.95 file is delivered in the conversation. The repository is public, so the result files on this branch can be read by anyone.

## Project store

The store is not changed by this fold.
- **Room:** re-read at fold time, it holds 1,998,017 of 2,000,000, so 1,983 are free. It still holds V4.91.
- **The problem:** V4.95 is 93,076 B larger than V4.91, so a delete-and-write swap does not fit.
- **What the swap needs:** the author's word, plus about 91 KB freed, or an instruction to keep the canonical in the repository.

## Verification

- **Fold script:** `foldin_v4_95_lattice_bound.py`, md5 `0086ea6646d981095c9176334b5fadbf`; log `fold_v4_95_output.txt` (md5 `3d27f83c6e6f891743529b97e52f76f9`).
  - Every anchor is read from the file and asserted unique, and every fragment lands exactly once.
  - The nine pointers are the only occurrences of "[→ V4.95 (§2.95): ".
  - The reverse splice reconstructs V4.94 byte-identically, and this is asserted before the output is accepted.
- **Independent check:** `verify_v4_95_additive.py`, md5 `9a3694d2257a3e9cb36c84075178fa97`; log `verify_v4_95_output.txt` (md5 `6298a7961ae691f16287f93af7bbce5e`). It shares no code with the fold script.
  - **Survival.** Every V4.94 line survives: 4,700 unchanged, 9 as in-line appends whose added text matches `[→ V4.95 (§2.95): …]`, plus the title and As-of rewrites.
  - **Placement.** The appends sit on exactly the nine line numbers above, which the check carries as its own list.
  - **Aim.** Each host line contains a keyword typed in the check from a reading of that line.
  - **Rewrites.** The only rewrites are the declared title and As-of lines. The old As-of text after its version label is kept verbatim.
  - **Insertions.** Everything else is a pure insertion, 16 lines (6,524 B), in four blocks at the declared places:
    - the record, before the V4.94 record;
    - §2.95, between §2.94's last paragraph and Cluster J;
    - the Part VI row, between the polycrystal-floor row and the G-C1 row;
    - the changelog line, after the V4.94 line.
  - **§2.92.A** is unchanged.
  - Result: PASS on the first run.
