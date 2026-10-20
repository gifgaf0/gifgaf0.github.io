#!/bin/bash
# E3 cross-check: full pipeline, single thread (about 12 minutes on one shared core).
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
set -e
python3 -u -W ignore cc_g2.py        > cc_g2.log 2>&1         # algebra, Dynkin indices, characters, rotor states (~5 s)
python3 -u -W ignore cc_skyrme.py    > cc_skyrme.log 2>&1     # profile, inertia (adjoint + 7), MeV, refit (~1 min)
python3 -u -W ignore cc_flag.py      > cc_flag.log 2>&1       # moment map, pi2, pi3 (~5 min)
python3 -u -W ignore cc_stability.py > cc_stability.log 2>&1  # second variation + Ritz (~6 min)
python3 -u cc_summary.py             > cc_summary.log 2>&1    # comparison with ../results.json -> crosscheck.json
grep -h "checks passed\|agree" cc_*.log
