#!/bin/bash
# After run_remaining.sh: single-packet controls for the slices, robustness probe, illustration,
# analyses, E1e and results.json.   Run: nohup ./run_post.sh > logs/post.log 2>&1 &
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
while ! grep -q "all done" logs/remaining.log 2>/dev/null; do sleep 10; done
t0=$(date +%s)
for f in e1d_sliceAk_*[0-9].json e1d_sliceAs_*[0-9].json; do
  [ -s "${f%.json}_single.json" ] || python e1d_single_slices.py "$f" 2
done
[ -s e1d_probe_min.json ] || python e1d_probe_min.py
python e1d_example.py
python analyze_e1b.py
python analyze_e1c.py
python analyze_e1d.py
python e1e_quanta.py
python collect_results.py
echo "[post done] $(( $(date +%s) - t0 )) s"
