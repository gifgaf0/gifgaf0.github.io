#!/bin/sh
# E5 -- add light. Runs every step in order (about 2.7 minutes on one core).
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 symbolic_derivations.py > symbolic_log.txt 2>&1      # ~170 s, 39 sympy checks (all computed)
python3 hedgehog_em.py 2>&1 | grep -v "SAWarning\|for entry" > hedgehog_log.txt   # ~8 s
python3 rotor_charges.py > charges_log.txt 2>&1               # <1 s
python3 pi0_gamma_gamma.py 2>&1 | grep -v "SAWarning\|for entry" > pi0_log.txt     # ~1 s
python3 make_results.py > make_results_log.txt 2>&1           # ~2 s
grep -c "^FAIL" symbolic_log.txt || true
tail -1 symbolic_log.txt
