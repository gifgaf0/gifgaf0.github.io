#!/bin/bash
# Resumption (third agent, after a container restart): finish Q6 L22 from its N=76 checkpoint.
# Deviation for the compute budget: minimum flow time of the N=76 stage lowered from 300 to 150
# (the stage had already passed the metastable drop at t~50 and its energy changed by < 1e-7
# per 10 time units at t=140 before the restart).  N=101 and N=151 stages as in run_queueB.sh;
# the N=151 stage is ended by stop_watcher.py (t >= 20, relative change over 10 units < 1e-6).
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 relax.py --run Q6_L22 --map L22_Q6 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 76:1200:1e-7:150,101:400:1e-7,151:300:1e-7
echo Q6_DONE
