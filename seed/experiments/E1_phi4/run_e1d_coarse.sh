#!/bin/bash
# E1d: coarse 3D scan and its controls. ~10 min on 2 cores.
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
python e1d_gauss.py coarse 2
python e1d_gauss.py single 2
python e1d_gauss.py dxcheck 2
