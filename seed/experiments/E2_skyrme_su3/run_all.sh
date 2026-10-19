#!/bin/sh
# E2: run every script in order (single thread). Total runtime about 26 s on one core.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for s in skyrme_hedgehog.py verify_densities.py su3_rotor.py derrick_virial.py make_figures.py collect_results.py; do
  echo "=== $s"
  t0=$(date +%s.%N)
  python3 "$s"
  t1=$(date +%s.%N)
  echo "    [$s: $(echo "$t1 - $t0" | bc) s wall]"
done
