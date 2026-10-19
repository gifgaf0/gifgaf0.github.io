#!/bin/bash
# E3: full pipeline, single-threaded. Each step is deterministic and re-runnable.
# SKIP_DONE=1 ./run_all.sh resumes after an interruption (steps with logs/<step>.done are skipped).
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
mkdir -p logs
for s in e3_g2_algebra e3_hedgehog e3_inertia e3_g2_reps e3_g2_su3_branching e3_stability e3_stability_refine e3_flag; do
  if [ -n "$SKIP_DONE" ] && [ -f "logs/$s.done" ]; then echo "skip $s"; continue; fi
  echo "=== $s $(date -u +%H:%M:%S)"
  t0=$(date +%s)
  python3 -u $s.py > logs/$s.log 2>&1 && touch logs/$s.done || { echo "FAILED $s"; exit 1; }
  echo "$s wall $(( $(date +%s) - t0 )) s"
done
python3 -u make_results.py > logs/make_results.log 2>&1 || echo "FAILED make_results"
echo "=== all done $(date -u +%H:%M:%S)"
