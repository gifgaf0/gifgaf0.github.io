#!/bin/bash
# Production queue A (1 thread).  Restart-safe: completed stages are loaded, an interrupted
# stage resumes from its last checkpoint.  Run together with run_queueB.sh (2 threads in total).
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=python3
$P relax.py --run Q1_A11 --map A11 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 76:400:1e-7,101:300:1e-7,121:300:1e-7,151:300:1e-7
$P relax.py --run Q3_A31 --map A31 --Lf 7.5 --offset 0.05,0.03,0.02 --squash 1.02,0.98,1 --stages 76:2000:1e-7:400,101:200:1e-7,151:120:1e-7
$P relax.py --run Q7_K32 --map K32_Q7 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 76:1200:1e-7:300,101:200:1e-7,151:120:1e-7
$P relax.py --run Q5_K32 --map K32_Q5 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 76:1500:1e-7:300,101:200:1e-7,151:120:1e-7
echo QUEUE_A_DONE
