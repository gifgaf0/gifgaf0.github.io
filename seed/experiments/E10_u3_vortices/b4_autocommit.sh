#!/bin/bash
# E10 B4: commit work in progress every 20 min (histories, logs); float32 checkpoint copies every 2 h.
cd "$(dirname "$0")"
n=0
while true; do
  sleep 1200; n=$((n+1))
  if [ $((n % 6)) -eq 0 ]; then
    mkdir -p b4_fields/ckpt32
    for f in b4_fields/*_ckpt.npz; do
      [ -e "$f" ] || continue
      b=$(basename "$f" _ckpt.npz)
      python3 -c "import numpy as np,sys; x=np.load(sys.argv[1])['x']; np.savez_compressed(sys.argv[2], x=x.astype(np.float32))" "$f" "b4_fields/ckpt32/${b}_ckpt32.npz"
    done
    git add -A b4_fields/ckpt32 2>/dev/null
  fi
  git add b4_hist log_b4_*.txt b4_fields/*.npz 2>/dev/null
  git reset -q b4_fields/*_ckpt.npz 2>/dev/null
  git commit -qm "E10 B4: WIP run state (auto)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018eHnHSvDCa83rxhrzHYNaA" && \
  for i in 1 2 3 4; do git push -q origin claude/seed-step3-first-closure && break; sleep $((2**i)); done
done
