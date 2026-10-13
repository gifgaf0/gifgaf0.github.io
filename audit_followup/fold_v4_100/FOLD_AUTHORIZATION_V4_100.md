# FOLD AUTHORIZATION — V4.100 (the SLWE decryption threshold, and three Zenodo deposits)

**Plain-language summary.** This fold corrects one number in the ledger and records what you put on Zenodo.
- **The number.** The ledger said decryption at the spec's noise never fails "for any q > 1032". In fact it fails at q = 1033 and never fails from q = 1036, so the first safe prime is 1039.
- **The deposits.**
  - The SLWE note (October 9).
  - The gauge paper v6.4 (October 13).
  - *Fluid Lattice Topology* with the notice withdrawing its security claims (October 13).
- **How it is added.** There is one new section, §2.100, and there are seven short pointers. Nothing already in the ledger was changed or removed, and the independent check confirms that.
- **Three things still to do on Zenodo**, listed below; none blocks the fold.

**Recorded:** October 13, 2026, 14:31 PDT (21:31 UTC).

| Item | Value |
|---|---|
| Base | `SQT_Master_Ledger_v4_99_CANONICAL.md`, md5 `a86fa0907310b34413b42d7ebdbcb067` (1,913,925 B), at the repository root on `main` (`08ebc62`) |
| Result | `SQT_Master_Ledger_v4_100_CANONICAL.md`, md5 `35a20a1f2db1ad66663b4cd60b7c8234` (1,923,114 B; +9,189 B) |
| Kind | One correction of fact, computed once (`../closeout/step3/3b_slwe_eprint/v2_runs/dfr_exact.py`), plus deposit facts read from Zenodo's record pages and DataCite at fold time. No verdict rests on any of it, so there is no second leg |
| Edits | Title; As-of prepend; the V4.100 fold-in record (before the V4.99 record); §2.100 (after §2.99, before Cluster J); seven in-line "[→ V4.100 (§2.100): …]" pointers; one changelog line |
| Checks | Reverse splice byte-identical to V4.99 (`fold_v4_100_output.txt`). The independent check passes too (`verify_v4_100_additive.py`, `verify_v4_100_output.txt`): seven appends on the typed lines, each stating the typed facts; three insertions at the declared places; the deposit facts present; §2.94's heading and C1 paragraph, §2.97, §2.99 and the §2.52 Open 3 row unchanged. Dry runs passed on October 10 and on October 13, after the deposits were added, and their ledger files were deleted |
| Estate | Branch `claude/ledger-v4-100-fold`, head at fold `7e195bf`, on top of `claude/gauge-v6-4-final-pass` (`6970915`); live `git ls-remote` 2026-10-13 21:31:05 UTC: main = `08ebc62` |

## The author's words (verbatim)

Tuesday, October 13, 2026, 14:20 PDT, the fold word:

> Both the gauge group paper and the flt have been uploaded to zenodo. Can we fold into The canonical v4.100?

14:26 PDT, the FLT record:

> Flt - https://doi.org/10.5281/zenodo.23351706

The October 10 staging was drafted on the author's "Yes" of 19:43 PDT to drafting the ledger entry (`STAGED.md`). The 14:20 word asks for the two new deposits to be folded in as well, so the staging was extended first (`STAGED.md`, addendum).

## The seven pointers (V4.99 line numbers)

| Line | Entry | What the pointer says |
|---|---|---|
| 3484 | OP-2.58.5 | Not for any q > 1032: q = 1033 fails under every decoder and rounding tried; deterministic from q = 1036, first prime 1039 |
| 3682 | Closure of OP-2.58.1.a (§2.66.1) | The bound 258 < q/4 ignores the half unit lost in rounding q/2; nothing changes at spec |
| 4651 | OP-2.58.1.b row | The differential needs q ≤ 1035, not 1032 |
| 4746 | OP-2.58.1a harness-port row | DFR = 0 from q = 1036; the conclusion is unchanged |
| 4638 | "Phase C draft awaiting the author" row | The note was deposited on October 9 (doi:10.5281/zenodo.23270249) and revised on October 10, for you to deposit as version 2. *Fluid Lattice Topology* has carried the notice since October 13 (doi:10.5281/zenodo.23351706) |
| 1724 | §2.93.B1, the gauge paper's correction | v6.4 was deposited on October 13 (doi:10.5281/zenodo.23351330) |
| 4635 | "Phase B drafts awaiting the author" row | The gauge paper v6.4 was deposited (doi:10.5281/zenodo.23351330). The pointer says nothing about the row's other drafts, and the row's status is unchanged |

## The deposits, as read at fold time

| Paper | DOI | Zenodo version | All-versions DOI | File (md5) |
|---|---|---|---|---|
| SLWE note | 10.5281/zenodo.23270249 | v1 | 10.5281/zenodo.23270248 | — (deposited October 9; recorded then) |
| Gauge paper v6.4 | 10.5281/zenodo.23351330 | v6 | 10.5281/zenodo.19157947 | `Gifford_Csaszar_Gauge_Group_v6_4_2026.pdf` (`d1b8507a5efe0c67edd4c6178c3c61d9`) |
| *Fluid Lattice Topology*, with the notice | 10.5281/zenodo.23351706 | v4 | 10.5281/zenodo.20078311 | `Fluid_Lattice_Topology_v3.pdf` (`6bd55206b83c817ff07c74fa7bd2340e`) |

Both new files are the PDFs built in the repository. The gauge PDF was built in `../closeout/step2/2a_gauge_paper/` (on `claude/gauge-v6-4-final-pass`), and the FLT PDF in `../closeout/step3/3b_slwe_eprint/flt_v3/`. Each rebuilds byte-identical.

## Reported, not changed

1. **The gauge record's description.** Read on October 13, it still gives the earlier abstract, which lists hypercharge assignments and the leading CKM mixing angle among the results. Replace it with the v6.4 abstract; that edits metadata only.
2. **The revised SLWE note is not yet on Zenodo.** DataCite lists one version under its all-versions DOI. The FLT notice quotes figures that only the revision contains: about 2¹⁶⁷ for version 2's parameters with a uniform matrix, against 2²⁶² for ML-KEM-1024. Depositing the revision (`../closeout/step3/3b_slwe_eprint/ZENODO_V2_DRAFT.md`) completes the citation.
3. **FLT's version label.** The record says v4, while the file calls itself version 3. DataCite also lists a version 10.5281/zenodo.23351115, which could not be read; you reported deleting the paper by accident at 13:48 PDT. If you prefer, change the label to v3, which edits metadata only.

## Where the ledger lives

- **V4.100 at the root.** V4.100 takes V4.99's place at the repository root, so the root still holds one canonical.
- **V4.99 stays in the history.** It remains in `main`'s history (at `08ebc62`). The fold script and the check read V4.99 from the root, so to rerun them, restore it there first: `git show 08ebc62:SQT_Master_Ledger_v4_99_CANONICAL.md > SQT_Master_Ledger_v4_99_CANONICAL.md`.
- **Merging.** Merge the pull request with a merge commit. That keeps `6970915`, which built the gauge PDF, and `7e195bf`, the head at fold, in `main`'s history.
