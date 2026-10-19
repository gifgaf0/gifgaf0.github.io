#!/bin/bash
# worker C: waits for worker A (DSV), then targeted Gaussian runs (smallest producers, self-folding threshold)
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "run_xc2_a.sh" > /dev/null; do sleep 15; done
python3 xc2_spec.py targets
