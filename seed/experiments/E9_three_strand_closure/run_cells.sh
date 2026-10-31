#!/bin/bash
# Runs the three new (kappa, eta) cells of PREREG §6: N = 0 control and N = 1 starts A and B, 65^3, R0 = 6.
# e = 1/(kappa*sqrt 3): kappa = 1 -> 0.5773502691896258, kappa = 2 -> 0.2886751345948129
cd "$(dirname "$0")"
E1=0.5773502691896258; E2=0.2886751345948129
run() { echo "start $(date -u +%T) $*"; python3 "$@"; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
( run control_N0_cell.py 65 6 $E1 0.1 > log_control_N0_k1_eta0.1.txt 2>&1
  run control_N0_cell.py 65 6 $E2 0   > log_control_N0_k2_eta0.txt   2>&1
  run control_N0_cell.py 65 6 $E1 0   > log_control_N0_k1_eta0.txt   2>&1 ) &
( run trace_N1_cell.py A 65 6 4000 2 $E1 0.1 > log_trace_A_N65_k1_eta0.1.txt 2>&1
  run trace_N1_cell.py B 65 6 4000 2 $E1 0.1 > log_trace_B_N65_k1_eta0.1.txt 2>&1 ) &
( run trace_N1_cell.py A 65 6 4000 2 $E2 0 > log_trace_A_N65_k2_eta0.txt 2>&1
  run trace_N1_cell.py B 65 6 4000 2 $E2 0 > log_trace_B_N65_k2_eta0.txt 2>&1 ) &
( run trace_N1_cell.py A 65 6 4000 2 $E1 0 > log_trace_A_N65_k1_eta0.txt 2>&1
  run trace_N1_cell.py B 65 6 4000 2 $E1 0 > log_trace_B_N65_k1_eta0.txt 2>&1 ) &
wait
echo all done $(date -u +%T)
