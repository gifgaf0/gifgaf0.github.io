#!/bin/bash
# Resumable driver for the stages not finished before the container restart.
# Each stage is skipped if its output JSON already exists. 2 worker processes,
# 1 thread each (thread budget 2). Run: nohup ./run_remaining.sh > logs/remaining.log 2>&1 &
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
stage() { # stage <output.json> <command...>
  out=$1; shift
  if [ -s "$out" ]; then echo "[skip] $out exists"; return; fi
  echo "[start] $out $(date +%T)"; t0=$(date +%s)
  "$@"
  echo "[done] $out $(( $(date +%s) - t0 )) s"
}
stage e1d_coarse.json python e1d_gauss.py coarse 2
read S K < <(python choose_slices.py)
echo "slice rule -> sigma=$S k=$K"
stage e1d_sliceAk_$S.json python e1d_gauss.py sliceAk 2 $S
stage e1c_fine.json python e1c_dsv.py fine 2
stage e1d_single.json python e1d_gauss.py single 2
stage e1d_sliceAs_$K.json python e1d_gauss.py sliceAs 2 $K
stage e1c_high.json python e1c_dsv.py high 2
stage e1d_phase.json python e1d_gauss.py phase 2 e1d_sliceAk_$S.json
stage e1c_dxcheck.json python e1c_dsv.py dxcheck 2
stage e1d_dxcheck.json python e1d_gauss.py dxcheck 2
stage e1b_dtcheck.json python e1b_dtcheck.py
echo "[all done] $(date +%T)"
