#!/bin/bash
# thread 1 (restarted driver): wait for DSV example, then E1b (fixed bisection, cached runs reused), then DSV map
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "xc_e1c.py example" > /dev/null; do sleep 10; done
python3 xc_e1b.py
python3 xc_e1c.py map
