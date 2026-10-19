#!/bin/bash
# Third batch (resumed attempt): waits for run_extra2.sh, then probes the one-way minimum producers.
#   nohup ./run_extra3.sh > logs/extra3.log 2>&1 &
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
while ! grep -q "extra2 done" logs/extra2.log 2>/dev/null; do sleep 15; done
[ -s e1d_oneway_min.json ] || python e1d_oneway_min.py
echo "[extra3 done] $(date +%T)"
