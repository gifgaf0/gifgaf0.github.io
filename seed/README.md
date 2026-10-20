# Seed experiments

A series of nine experiments testing `SEED.md`, a starting point for a theory in which the vacuum is taut,
matter is topological folds of a field, and the 60° (hexagonal) structure lives in the field's internal space.

- `SEED.md`: the seed. `hexagon_check.py`: its own check of §3.
- `PLAN.md`: the preregistration, committed before any experiment ran.
- `RESULTS.md`: what came out: verdicts for every seed claim that was tested, the seed statements that were
  not tested, the PLAN's own predictions, calibrations, misses, deviations, corrections, next steps.
- `experiments/E0_*` … `E8_*`: one folder per experiment, each with code, `results.json`, `REPORT.md`,
  an independent second computation in `crosscheck/`, and `RECONCILE.md`, which settles the differences
  between the two.
- `prior_address/`: the literature check made before the experiments.

## Reproducing

Python 3.13 with the packages in `requirements.txt`. E2, E3, E5 and E7 also read PDG 2026 values through the
optional `pdg` package; without it they fall back to built-in values. Each `REPORT.md` has a "How to reproduce"
section, just before its "Reconciliation" section, with the exact commands and run times.

Some paths are hard-coded and must be changed to rerun elsewhere:

- E8 writes its field checkpoints (about 1.8 GB) to a session scratch directory under `/tmp`, outside the
  repository: `SCRATCH_DEFAULT` in `relax.py` (or pass `--scratch`), and `SCRATCH` in `analyze.py`,
  `finalize_stage.py`, `qlink_coarse.py`, `stencil_check.py` and `stencil_relax.py`. The fields are not in the
  repository, so E8's analysis needs the relaxations rerun first.
- E3's `make_results.py` reads E2's `results.json` and `profile.json` by absolute path; it skips that
  comparison if they are missing.
- E7's "How to reproduce" starts with an absolute `cd`. `e7_dl_digitize.py` needs the Demidov–Levkov PDFs
  (their directory in `E7_LITDIR`); without them the committed readings are kept.
- Several scripts in the `crosscheck/` folders of E2, E4, E6, E7 and E8 hard-code absolute paths to the
  repository or to the session scratch directory.
