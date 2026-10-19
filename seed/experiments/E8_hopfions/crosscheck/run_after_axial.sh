#!/bin/bash
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "^python3 -W ignore xc_axial_spectral.py" > /dev/null; do sleep 3; done
python3 -W ignore xc_eval_R4.py > xc_eval_R4.log 2>&1
python3 -W ignore xc_tests3d.py > xc_tests3d.log 2>&1
