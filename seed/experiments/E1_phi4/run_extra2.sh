#!/bin/bash
# Second batch of robustness runs (resumed attempt). Waits for run_extra.sh, then runs the E1b
# box check and the E1d dx ladder. 2 worker processes x 1 thread.
#   nohup ./run_extra2.sh > logs/extra2.log 2>&1 &
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
while ! grep -q "extra done" logs/extra.log 2>/dev/null; do sleep 15; done
[ -s e1b_boxcheck.json ] || python e1b_boxcheck.py
[ -s e1d_dxladder.json ] || python e1d_dxladder.py 2
echo "[extra2 done] $(date +%T)"
