#!/bin/bash
# E10 B4: the 9 loop runs (4 at a time), then the h = 0.125 re-relaxations of the non-collapsing end states.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
printf "%s\n" M3a M3b M5a M5b C-a C-b C-c C-d C-d5 | xargs -P 4 -I{} sh -c 'python3 b4_run.py {} >> log_b4_{}.txt 2>&1'
python3 b4_finelist.py | xargs -r -P 4 -I{} sh -c 'python3 b4_run.py {} fine >> log_b4_{}_fine.txt 2>&1'
python3 b4_analyse.py > log_b4_analyse.txt 2>&1
echo CHAIN DONE >> log_b4_chain.txt
