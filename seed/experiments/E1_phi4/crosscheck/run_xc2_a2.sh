#!/bin/bash
# worker A, second stage: DSV example at dx=0.05, neighbouring v at omega=0.99, then targeted Gaussian runs
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 xc2_spec.py dsv ex2
python3 xc2_spec.py targets
