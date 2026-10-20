#!/bin/sh
# E5 cross-check (independent code). About 5 minutes on one core.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 cc_hedgehog.py     # profile, EM currents from the matrix Lagrangian, refits, massive variant
python3 cc_pi0.py          # pi0 -> gamma gamma from B-H eq. 67 (needs cc_hedgehog.json for the fold's f)
python3 cc_charges.py      # Gelfand-Tsetlin charges
python3 cc_linear.py       # linearisation and vacuum T_mu nu
python3 cc_extra.py        # neutron enclosed-charge peak
python3 cc_compare.py      # comparison with ../results.json -> crosscheck.json
