#!/bin/bash
# E3: full pipeline, single-threaded. Each step is deterministic and re-runnable.
# SKIP_DONE=1 ./run_all.sh resumes after an interruption (steps with logs/<step>.done are skipped).
# reconcile_stability_r40 was added at reconciliation (assignment of the R = 40 (3,1) Hessian levels).
# A fresh end-to-end run (no SKIP_DONE) takes about 30 minutes on one shared core.
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
mkdir -p logs
T0=$(date +%s)
for s in e3_g2_algebra e3_hedgehog e3_inertia e3_g2_reps e3_g2_su3_branching e3_stability e3_stability_refine reconcile_stability_r40 e3_flag; do
  if [ -n "$SKIP_DONE" ] && [ -f "logs/$s.done" ]; then echo "skip $s"; continue; fi
  echo "=== $s $(date -u +%H:%M:%S)"
  t0=$(date +%s)
  python3 -u $s.py > logs/$s.log 2>&1 && touch logs/$s.done || { echo "FAILED $s"; exit 1; }
  echo "$s wall $(( $(date +%s) - t0 )) s"
done
python3 -u make_results.py > logs/make_results.log 2>&1 || { echo "FAILED make_results"; exit 1; }
echo "=== all done $(date -u +%H:%M:%S), total wall $(( $(date +%s) - T0 )) s"
