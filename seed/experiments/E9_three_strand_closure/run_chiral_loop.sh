#!/bin/bash
# PREREG_chiral_loop.md §4 runs. 65^3, R0 = 6, maxiter 4000, record every 2. One BLAS thread per job, 4 jobs at a time.
# Stage 1 (P1 controls at +-0.3 and start A at +-0.1); stage 2 only after P1 has been checked at +-0.3.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
run() { echo "start $(date -u +%T) $*"; python3 "$@"; }
if [ "$1" = 1 ]; then
  run control_N0_chiral.py 65 6 0.3 4000 2  > log_control_N0_chiral_g+0.3.txt 2>&1 &
  run control_N0_chiral.py 65 6 -0.3 4000 2 > log_control_N0_chiral_g-0.3.txt 2>&1 &
  run trace_N1_chiral.py A 65 6 4000 2 0.1  > log_trace_chiral_A_g+0.1.txt 2>&1 &
  run trace_N1_chiral.py A 65 6 4000 2 -0.1 > log_trace_chiral_A_g-0.1.txt 2>&1 &
  wait
elif [ "$1" = 2 ]; then
  ( run trace_N1_chiral.py B 65 6 4000 2 0.1  > log_trace_chiral_B_g+0.1.txt 2>&1
    run trace_N1_chiral.py A 65 6 4000 2 0.3  > log_trace_chiral_A_g+0.3.txt 2>&1
    run trace_N1_chiral.py B 65 6 4000 2 -0.3 > log_trace_chiral_B_g-0.3.txt 2>&1 ) &
  ( run trace_N1_chiral.py B 65 6 4000 2 -0.1 > log_trace_chiral_B_g-0.1.txt 2>&1
    run trace_N1_chiral.py A 65 6 4000 2 -0.3 > log_trace_chiral_A_g-0.3.txt 2>&1 ) &
  ( run trace_N1_chiral.py A 65 6 4000 2 0.2  > log_trace_chiral_A_g+0.2.txt 2>&1
    run trace_N1_chiral.py B 65 6 4000 2 0.2  > log_trace_chiral_B_g+0.2.txt 2>&1 ) &
  ( run trace_N1_chiral.py A 65 6 4000 2 -0.2 > log_trace_chiral_A_g-0.2.txt 2>&1
    run trace_N1_chiral.py B 65 6 4000 2 -0.2 > log_trace_chiral_B_g-0.2.txt 2>&1
    run trace_N1_chiral.py B 65 6 4000 2 0.3  > log_trace_chiral_B_g+0.3.txt 2>&1 ) &
  wait
fi
echo "stage $1 done $(date -u +%T)"
