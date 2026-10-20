#!/bin/bash
# Third agent: Q5 (optional in PLAN.md), started on the thread freed when the Q6 resumption finishes.
# Stages as in run_queueA.sh, but only N=76 and N=101 (compute budget); the N=101 stage may be ended
# by the stop_watcher rule.  Its energy is reported at the finest spacing reached, clearly labelled.
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
until grep -q Q6_DONE runs/resume_Q6.out; do sleep 20; done
python3 relax.py --run Q5_K32 --map K32_Q5 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 76:1500:1e-7:300,101:200:1e-7
echo Q5_DONE
