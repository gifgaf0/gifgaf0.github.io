#!/bin/bash
# E1c: DSV breather trains. ~20 min on 2 cores.
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
# example already run
python e1c_dsv.py grid 2
python e1c_dsv.py fine 2
python e1c_dsv.py high 2
python e1c_dsv.py dxcheck 2
