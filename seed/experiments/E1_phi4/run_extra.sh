#!/bin/bash
# Robustness runs added by the third (resumed) attempt; resumable (JSONL checkpoints, stages skipped
# when complete). 2 worker processes x 1 thread.   nohup ./run_extra.sh > logs/extra.log 2>&1 &
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
[ -s e1_verify.json ] || python e1_verify.py

python e1d_extra.py coarse_oneway 2
python e1d_extra.py single_oneway 2
python e1d_extra.py slice_dx05 2
python e1d_extra.py slice_dx05_single 2
[ -s e1b_boxcheck.json ] || python e1b_boxcheck.py
echo "[extra done] $(date +%T)"
