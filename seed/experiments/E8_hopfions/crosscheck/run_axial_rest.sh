#!/bin/bash
# after the m=1 axial cases: A_{3,1} and A_{2,2} (single thread)
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "^python3 -W ignore xc_axial_spectral.py n1m1" > /dev/null; do sleep 5; done
python3 -W ignore xc_axial_a22.py n2m2_inf n2m2_cyl7.5 > xc_axial_a22.log 2>&1
python3 -W ignore xc_axial_spectral.py n3m1_inf > xc_axial_c.log 2>&1
