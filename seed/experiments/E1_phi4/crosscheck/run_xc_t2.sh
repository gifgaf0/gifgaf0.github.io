#!/bin/bash
# thread 2: Gaussian coarse grid (both halves) -> sigma=16,k=1 line -> single-packet controls -> DSV map (reverse)
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 xc_e1d.py coarse 0 2
python3 xc_e1d.py coarse 1 2
python3 xc_e1d.py line 1.0 16.0
python3 xc_e1d.py single 80
python3 xc_e1c.py map reverse
