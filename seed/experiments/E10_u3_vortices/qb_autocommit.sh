#!/bin/bash
# E10 QB: commit work in progress every 20 min (histories, logs, final fields); float32 checkpoint copies every hour.
cd "$(dirname "$0")"
n=0
while true; do
  sleep 1200; n=$((n+1))
  if [ $((n % 3)) -eq 0 ]; then
    mkdir -p qb_fields/ckpt32
    for f in qb_fields/*_ckpt.npz; do
      [ -e "$f" ] || continue
      b=$(basename "$f" _ckpt.npz)
      python3 -c "import numpy as np,sys; x=np.load(sys.argv[1])['x']; np.savez_compressed(sys.argv[2], x=x.astype(np.float32))" "$f" "qb_fields/ckpt32/${b}_ckpt32.npz"
    done
    git add -A qb_fields/ckpt32 2>/dev/null
  fi
  git add qb_*.py qb_*.sh qb_hist log_qb_*.txt qb_fields/*.npz 2>/dev/null
  git reset -q qb_fields/*_ckpt.npz 2>/dev/null
  git commit -qm "E10 QB: WIP run state (auto)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018eHnHPc1ESAWEPQCqSCSc2" && \
  for i in 1 2 3 4; do git push -q origin claude/seed-step3-first-closure && break; sleep $((2**i)); done
done
