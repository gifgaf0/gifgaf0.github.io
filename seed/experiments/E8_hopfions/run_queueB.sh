#!/bin/bash
# Production queue B (1 thread).  Restart-safe.  Run together with run_queueA.sh.
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=python3
$P relax.py --run Q2_A21 --map A21 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 76:400:1e-7,101:300:1e-7,121:300:1e-7,151:300:1e-7
$P relax.py --run Q4_A22 --map A22 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 76:2000:1e-7:400,101:400:1e-7,151:300:1e-7
$P relax.py --run Q6_L22 --map L22_Q6 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 76:1200:1e-7:300,101:400:1e-7,151:300:1e-7
echo QUEUE_B_DONE
