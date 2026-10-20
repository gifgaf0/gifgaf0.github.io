#!/bin/bash
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
while kill -0 26763 2>/dev/null; do sleep 5; done
python3 xc2_spec.py dsv ex5
