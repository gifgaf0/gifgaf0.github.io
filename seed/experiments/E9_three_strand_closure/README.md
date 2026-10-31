# E9: three-strand closure (step 3 of the successor plan)

Read `PREREG.md` first, including Amendments A (§9) and B (§10). Steps 1–2 (classification and the 2D fractional-vortex calibration) are in `prior/`.

**Done so far:** `REPORT_control.md` (N = 0 control: P1 holds). `REPORT_N1.md` (first N = 1 session: start A at 49³ inconclusive because the start touched the box; start B not run because the script's start was wrong). Both errors are corrected under Amendment B. `REPORT_N1_rerun.md` (κ = 2, η = 0.1 at 65³: both starts COLLAPSE). `REPORT_N1_kappa_eta.md` (the other three pre-registered (κ, η) combinations at 65³: all COLLAPSE, so the §6 fallback condition is met; `trace_N1.py` takes `--e` and `--eta`).

**To run (rerun under Amendment B):**
```
cd seed/experiments/E9_three_strand_closure
python3 gl3.py                                 # gradient check; expect ~2e-7
python3 trace_N1.py A 65 6 4000 2              # Hopf-linked start
python3 trace_N1.py B 65 6 4000 2              # helix start
# only if a start does not collapse:  python3 trace_N1.py <start> 81 6 6000 2
```
Before running, confirm the starts: `python3 -c "from gl3 import GL3; from starts import start_fields; from linking import analyse; g=GL3(N=65); print([analyse(start_fields(g,s,6.0)) for s in 'AB'])"` should give |Lk12| = |Lk13| = 1 for both.

Apply PREREG §9–§10 to the output and write `REPORT_N1_rerun.md`. Do not re-tune κ or η. Model units only; no physical identification of the loop.
