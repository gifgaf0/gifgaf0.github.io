#!/bin/bash
# E6: full pipeline from scratch (about 5 minutes on one core).  Deterministic; no random numbers.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
rm -rf out
mkdir -p logs
( time python3 derive_equations.py )  > logs/derive_equations.log 2>&1
( time python3 derive_pulsation.py )  > logs/derive_pulsation.log 2>&1
( time python3 e6_solve.py )          > logs/e6_solve.log 2>&1
( time python3 e6_stability.py )      > logs/e6_stability.log 2>&1
( time python3 collect_results.py )   > logs/collect_results.log 2>&1
( time python3 make_figures.py )      > logs/make_figures.log 2>&1
grep -h "real" logs/*.log
