# E9: three-strand closure (step 3 of the successor plan)

Read `PREREG.md` first, including Amendment A. Steps 1–2 (the classification and the 2D fractional-vortex calibration) are in `prior/`.

**Done in the authoring session:** the control `REPORT_control.md` (P1 holds; instrument calibrated).

**To run (Claude Code session, this branch):**
```
cd seed/experiments/E9_three_strand_closure
python3 gl3.py                      # gradient check; expect ~2e-7
python3 run_N1.py A 49 6 4000       # Hopf-linked start, ~20 min
python3 run_N1.py B 49 6 4000       # meridian-loop start, ~20 min
python3 run_N1.py A 65 6 6000       # box check, only if the 49^3 run is not COLLAPSE (~1.5 h)
```
Apply the verdict rules of PREREG.md §9 to the output; write `REPORT_N1.md`; do not re-tune κ or η. The second computation ("two-leg") should be an independent re-implementation from `PREREG.md` alone, as in the Seed's `PLAN.md` method rules.
