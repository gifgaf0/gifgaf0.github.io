#!/bin/bash
# Third agent: dx = 0.1 stage for Q5 (the N=76 and N=101 stages are loaded from their checkpoints).
# 2 threads (all other runs of this experiment had finished); dt = 0.07 h from the start (the value the
# instability safeguard settled to in the Q4 and Q6 N=151 stages).  Ended by stop_watcher.py
# (t >= 20, relative change over 10 units < 1e-6).
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
python3 relax.py --run Q5_K32 --map K32_Q5 --Lf 7.5 --offset 0.05,0.03,0.02 --dtfac 0.07 --stages 76:1500:1e-7:300,101:200:1e-7,151:120:1e-7
echo Q5_N151_DONE
