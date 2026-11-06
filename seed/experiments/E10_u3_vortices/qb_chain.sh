#!/bin/bash
# E10 QB: the 49 non-regression grid runs, 4 at a time (each resumes from its checkpoint or skips if done);
# then the box and resolution checks chosen by qb_analyse.py; then the final analysis.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
grep -q "END" log_qb_L1.0_Q1626.5329_S1.txt || { echo "regression not finished" >> log_qb_chain.txt; exit 1; }
python3 qb_analyse.py regression >> log_qb_chain.txt 2>&1 || { echo "REGRESSION FAILED: stop" >> log_qb_chain.txt; exit 1; }
python3 qb_run.py list | grep -v '^L1.0_Q1626.5329_S1$' | xargs -P 4 -I{} sh -c 'python3 qb_run.py {} >> log_qb_{}.txt 2>&1'
echo "GRID DONE" >> log_qb_chain.txt
python3 qb_analyse.py checklist | xargs -r -P 4 -I{} sh -c 'python3 qb_run.py {} >> log_qb_{}.txt 2>&1'
echo "CHECKS DONE" >> log_qb_chain.txt
python3 qb_analyse.py > log_qb_analyse.txt 2>&1
echo "CHAIN DONE" >> log_qb_chain.txt
