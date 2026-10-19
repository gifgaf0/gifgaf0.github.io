#!/bin/bash
# worker B: random sample of 90 coarse-grid Gaussian points (spectral code)
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 xc2_spec.py gauss 0 1
