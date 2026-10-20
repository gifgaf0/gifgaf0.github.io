#!/bin/bash
# reconcile_rerun.sh -- reruns the parts of E4 affected by the reconciliation (delta-pull fix, real-coupling
# variants), on one thread.  Resumable: e4_fits.py skips classes already in out/fits.jsonl.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "start $(date)"
[ -f out/.yukawa_done ] || { python3 e4_yukawa.py > out/yukawa.log && touch out/.yukawa_done; echo "yukawa done $(date)"; }
python3 e4_fits.py; echo "fits done $(date)"
python3 e4_structure.py > out/structure.log; echo "structure done $(date)"
[ -f out/.robust_done ] || { python3 e4_robustness.py > out/robustness.log && touch out/.robust_done; echo "robustness done $(date)"; }
echo "all done $(date)"
