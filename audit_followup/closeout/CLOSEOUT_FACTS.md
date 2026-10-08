# Close-out: the author's facts and elections (October 8, 2026)

**Plain-language summary.** The close-out brief left seven facts and elections for the author. This file records:
- what the author supplied, in his own words;
- which defaults apply;
- the two decisions still waiting for his word.

## Supplied by the author (Thursday, October 8, 2026, 07:09 PDT; verbatim)

> F1. Gauge group paper isn't under review
>
> F3. https://doi.org/10.5281/zenodo.20448930. 5/29/26
>
> F5. Hollister CA

## The seven items

| Item | Value used | Source |
|---|---|---|
| F1 | The gauge paper is not under review at any journal, so no editor letter | Author (matches §2.93.B1(4)) |
| F2 | v2.1 is the Zenodo v2 text (10.5281/zenodo.20532770), and no journal submission is open, so no withdrawal letter | **Default, flagged.** The ledger records no fourth submission (V4.45, OP-PSL.3) |
| F3 | Alpha-decay deposit DOI 10.5281/zenodo.20448930, deposited May 29, 2026 | Author. "Same text as the May 28 store copy?" was not answered: the corrected version is built on the store copy (md5 770ac497…), **flagged** |
| F4 | The old public calculator is live in all likelihood. The repository is public with Pages enabled (`has_pages: true`), and `main` carries `index.html`, "SQT Geometric Mass Calculator v3". The Pages endpoint and the site itself could not be fetched from this session | Checked |
| F5 | Byline "Matthew Gifford"; affiliation and contact "Independent researcher, Hollister, CA" | Author (byline by default, matching the Zenodo records) |
| F6 | Gauge paper title: "Gauge Group and Generation Structure from the Császár Polyhedron". PSL(2,7) note: two titles proposed in its draft | **Default, flagged** |
| F7 | §2.52 Open 3: §2.97.C(f) as drafted (text untouched, listed as closed with the program); the bracketed alternative is not folded | **Default, flagged** |

## Waiting for the author's word

These cannot be undone, so they are not done.
1. **Canonical ledger in the repository.**
   - The brief says "The canonical ledger lives in the repository from now on".
   - The repository is public and Pages-enabled: anything on `main` is served at gifgaf0.github.io, and anything on a branch is readable on GitHub.
   - This reverses the June 18 policy (`FOLD_LEDGER_2026-06-18.md`).
   - Until the author confirms, the canonical stays out of the repository, as before. The fold scripts and the base md5 reproduce it exactly.
2. **Deleting V4.95 from the project store.**
   - The store has 5,709 B free. STATUS.md and the three phase reports need about 37 KB, so they fit only if the canonical leaves the store.
   - Until the author confirms, the store keeps V4.95. Small items are written to the store when they fit.

## Addendum, October 8, 2026: the store copy
- Item 2 above names V4.95. The store's copy has been **V4.96** since October 7, 20:13 PDT (2026-10-08 03:13:44 UTC). Re-read on October 8, it is byte-identical to the V4.96 fold output (md5 `120b076a…`).
- "5,709 B free" was the store's counter at the V4.96 fold, and the counter is not in bytes. V4.96 and the two store calculators alone come to 2,019,219 B, more than the 1,997,416 it reports for every file in the store. After the Flach note it reports 2,584 free, in its own units.
- The decision is unchanged: deleting the store's ledger copy waits for the author (`../CLOSEOUT_REPORT.md`, section 4).

## Addendum, October 8, 2026, 08:43 PDT: the author's answers and decisions
The directive is saved verbatim in `../inputs/DIRECTIVE_2026-10-08_finalize_v4_99.md`. For the items above:
- **F3, second part:** "Yes, the deposited v1 alpha-decay paper is exactly the same text as the May 28 store copy."
- **F2, F4, F6, F7:** "Confirmed. All defaults you applied are correct. For the PSL(2,7) note, we will proceed with Title Option A."
- **Waiting item 1, the ledger in the repository: done.**
  - V4.98 was committed at the root of the branch in `5d9577c`, replacing `FOLD_LEDGER_2026-06-18.md`.
  - V4.99 then replaced it at the root in `64af32c`.
  - Nothing was pushed to `main`.
- **Waiting item 2, the store copy: done.** V4.96 was deleted from the store at 08:48 PDT. The counter fell from 1,997,416 to 1,353,522.
