#!/bin/bash
# worker A, third stage: after stage 2 finishes, DSV (0.99, 0.41) at dx=0.05
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
while kill -0 17239 2>/dev/null; do sleep 10; done
python3 xc2_spec.py dsv ex3
