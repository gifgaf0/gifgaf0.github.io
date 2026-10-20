#!/bin/bash
# Second cross-check pass, in the order actually run (each python step is resumable; outputs JSON/JSONL here).
# First-pass outputs (xc_*.json[l], from xc_e1a.py, xc_e1b.py, xc_e1c.py, xc_e1d.py, xc_e1e.py) are reused as inputs.
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 xc2_spec.py selftest
python3 xc2_spec.py dsv ex  &   # (0.99,0.43) dx 0.1 dt 0.02 [the run was stopped after this first case]
python3 xc2_spec.py gauss 0 1   # 90-point random sample, ~40 min
wait
python3 xc2_spec.py dsv ex2     # (0.99,0.43) dx 0.05; (0.99,0.42/0.44/0.41) dx 0.1
python3 xc2_spec.py targets     # smallest producers, one-way phi_t, self-folding thresholds
python3 xc2_spec.py dsv ex3; python3 xc2_spec.py dsv ex4; python3 xc2_spec.py dsv ex5
# diagnosis with the ORIGINAL code: copy ../phi4core.py ../e1c_dsv.py to a scratch dir and run there
#   xc2_diag_origcode_dsv.py, xc2_diag_origcode_col099.py, xc2_diag_origcode_041.py,
#   xc2_diag_origcode_043fine.py, xc2_diag_origcode_043dt.py   (each takes the output JSON path as argument)
python3 xc2_confound.py
python3 xc2_compare.py && python3 xc2_audit.py && python3 xc2_audit_text.py && python3 xc2_write_json.py
