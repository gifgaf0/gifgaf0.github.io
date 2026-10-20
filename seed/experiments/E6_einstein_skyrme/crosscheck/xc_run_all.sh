#!/bin/bash
# Independent cross-check of E6, whole pipeline from scratch (one core).
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p logs out
python3 xc_derive.py            > logs/xc_derive.log 2>&1             # symbolic equations (iso + Schwarzschild gauges)
python3 xc_pulsation_derive.py  > logs/xc_pulsation_derive.log 2>&1   # radial pulsation operator
python3 xc_run.py               > logs/xc_run_all.log 2>&1            # spectral iso-gauge solver: flat, branch, fold, fixed alpha, slope, upper branch
python3 xc_firstorder.py        > logs/xc_firstorder.log 2>&1         # O(alpha) formulas from the flat profile + physical scale
python3 xc_defl_check.py        > logs/xc_defl_check.log 2>&1         # deflection in two gauges, precise maximum
python3 xc_extra.py             > logs/xc_extra.log 2>&1              # alpha=0.04037 pair, BM extrapolation, stress diagnostics
python3 xc_stability.py         > logs/xc_stability.log 2>&1          # radial stability on iso-gauge backgrounds
python3 xc_collect.py           > logs/xc_collect.log 2>&1             # comparison with the original -> crosscheck.json
echo done
