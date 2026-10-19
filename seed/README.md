# Seed experiments

A series of nine experiments testing `SEED.md`, a starting point for a theory in which the vacuum is taut,
matter is topological folds of a field, and the 60° (hexagonal) structure lives in the field's internal space.

- `SEED.md`: the seed. `hexagon_check.py`: its own check of §3.
- `PLAN.md`: the preregistration, committed before any experiment ran.
- `RESULTS.md`: what came out: verdicts for every seed claim, calibrations, misses, corrections, next steps.
- `experiments/E0_*` … `E8_*`: one folder per experiment, each with code, `results.json`, `REPORT.md`,
  an independent second computation in `crosscheck/`, and `RECONCILE.md` where the two had to be reconciled.
- `prior_address/`: the literature check made before the experiments.

Requirements: Python 3.13 with the packages in `requirements.txt`. Each `REPORT.md` ends with the exact
commands to reproduce it.
