#!/bin/sh
# E2 cross-check: run every step in order (single thread, about 40 s). Logs go to xc_*.log.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for s in xc_derive xc_hedgehog xc_densities xc_rotor xc_axial xc_collect; do
  echo "=== $s"
  python3 -W ignore "$s.py" > "$s.log" 2>&1
  tail -1 "$s.log"
done
