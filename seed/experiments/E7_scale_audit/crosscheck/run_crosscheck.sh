#!/bin/sh
# E7 independent cross-check (one core, ~3 min). The DL digitisation needs the two arXiv PDFs
# (1103.0013v2.pdf, 1103.2133v2.pdf from the arXiv GCS mirror) in $LITDIR; it is skipped if absent
# and the committed cc_dl_digitized.json is used.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
LITDIR=${LITDIR:-/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/lit/e7cc}
python3 cc_hedgehog.py > cc_hedgehog_log.txt 2>&1          # Ritz-spectral hedgehog + pion-mass family
python3 cc_hopfion.py  > cc_hopfion_log.txt 2>&1           # hedgehog-Hopf ansatz: identity + 3D FD check
if [ -f "$LITDIR/1103.0013v2.pdf" ]; then python3 cc_digitize_dl.py "$LITDIR" > cc_digitize_log.txt 2>&1; fi
python3 cc_audit.py    > cc_audit_log.txt 2>&1             # all E7 numbers
python3 cc_diag_hopfion_rms.py > cc_diag_hopfion_rms_log.txt 2>&1   # step-4 diagnosis (uses original e7_hopfion.py)
python3 cc_compare.py  > cc_compare_log.txt 2>&1           # writes crosscheck.json
