#!/bin/sh
# E7 scale audit: full reproduction (one core). Approximate runtimes: 40 s, 3-5 min, <5 s, 5 s, 3 s, 1 s.
# Optional: E7_LITDIR=<dir holding 1103.0013v2.pdf and 1103.2133v2.pdf> re-extracts the Demidov-Levkov
# curves from the PDF vector paths; without it the committed dl_digitized.json is used.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 e7_hedgehog.py   > hedgehog_log.txt 2>&1
python3 e7_hopfion.py    > hopfion_log.txt 2>&1
python3 e7_dl_digitize.py "${E7_LITDIR:-}" > dl_digitize_log.txt 2>&1
python3 e7_audit.py      > audit_log.txt 2>&1
python3 make_figures.py
python3 collect_results.py > collect_log.txt
