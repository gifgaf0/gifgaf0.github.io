#!/bin/bash
# thread 2 (restarted driver): wait for the running coarse half, then the remaining E1d tasks, then DSV map (reverse)
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "xc_e1d.py coarse 0 2" > /dev/null; do sleep 15; done
python3 xc_e1d.py coarse 0 2
python3 xc_e1d.py coarse 1 2
python3 xc_e1d.py line 1.0 16.0
python3 xc_e1d.py single 80
python3 xc_e1d.py line 2.0 16.0
python3 xc_e1d.py dxself 100
python3 xc_e1c.py map reverse
