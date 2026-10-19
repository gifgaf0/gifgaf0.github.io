#!/bin/bash
# worker A: DSV example point (spectral code), resolution/time-step variants, then neighbours
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 xc2_spec.py dsv ex
python3 xc2_spec.py dsv nb
