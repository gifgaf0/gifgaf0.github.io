#!/bin/bash
# thread 1: E1b (already launched separately) -> DSV example -> DSV map (forward)
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "python3 xc_e1b.py" > /dev/null; do sleep 20; done
python3 xc_e1b.py
python3 xc_e1c.py example
python3 xc_e1c.py map
