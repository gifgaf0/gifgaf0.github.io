#!/bin/sh
# E7 scale audit: full reproduction (one core). Approximate runtimes: 40 s, 170 s, 5 s, 3 s, 1 s.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 e7_hedgehog.py   > hedgehog_log.txt 2>&1
python3 e7_hopfion.py    > hopfion_log.txt 2>&1
python3 e7_audit.py      > audit_log.txt 2>&1
python3 make_figures.py
python3 collect_results.py > collect_log.txt
