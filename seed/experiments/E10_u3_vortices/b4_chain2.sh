#!/bin/bash
# E10 B4: second half of b4_chain.sh (run by hand after the chain wrapper was stopped to start fine runs early):
# waits for M5b, then the remaining h = 0.125 re-relaxations (M5b, C-d, C-d5), then the analysis.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
until [ -e b4_fields/M5b.npz ]; do sleep 30; done
python3 b4_run.py C-d fine >> log_b4_C-d_fine.txt 2>&1 &
python3 b4_run.py M5b fine >> log_b4_M5b_fine.txt 2>&1 &
wait
python3 b4_run.py C-d5 fine >> log_b4_C-d5_fine.txt 2>&1
python3 b4_analyse.py > log_b4_analyse.txt 2>&1
echo CHAIN2 DONE >> log_b4_chain.txt
