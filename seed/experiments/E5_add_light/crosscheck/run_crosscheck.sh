#!/bin/sh
# E5 cross-check (independent code), end to end. About 4.5 minutes wall on one shared core.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 cc_hedgehog.py > /dev/null     # shooting profile, Noether currents of the matrix Lagrangian, refits, massive variant -> cc_hedgehog_log.txt
python3 cc_pi0.py 2>&1 | grep -v "SAWarning\|for entry" > /dev/null   # pi0 -> gg from B-H eq. 67 (uses cc_hedgehog.json) -> cc_pi0_log.txt
python3 cc_charges.py > /dev/null      # Gelfand-Tsetlin charges -> cc_charges_log.txt
python3 cc_linear.py > /dev/null       # linearisation and vacuum T_mu nu -> cc_linear_log.txt
python3 cc_extra.py > cc_extra_log.txt # neutron enclosed-charge peak
python3 cc_new.py 2>&1 | grep -v "SAWarning\|for entry\|RuntimeWarning\|F = 2" > /dev/null   # pass 2: FE-minimisation solver, WZ charge, N_c charges, PDG, textbook pi0 -> cc_new_log.txt
python3 cc_compare.py > cc_compare_log.txt   # comparison with ../results.json -> crosscheck_numbers.json
python3 cc_audit.py > cc_audit_log.txt       # REPORT text audit, issues, claim audit -> crosscheck.json
tail -1 cc_compare_log.txt
tail -1 cc_audit_log.txt
