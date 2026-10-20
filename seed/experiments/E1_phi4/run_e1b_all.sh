#!/bin/bash
# E1b: all collision scans (baseline + convergence checks). ~30-40 min on 2 cores.
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
python e1b_kkbar.py 0.05 12 base 600 0.15 0.30 0.0001 2
python e1b_kkbar.py 0.1 12 dx0.1 600 0.15 0.30 0.0001 2
python e1b_kkbar.py 0.05 20 x0_20 600 0.15 0.30 0.0001 2
python e1b_kkbar.py 0.05 12 tpost1500 1500 0.15 0.30 0.0002 2
python e1b_kkbar.py 0.025 12 dx0.025 600 0.15 0.30 0.0002 2
