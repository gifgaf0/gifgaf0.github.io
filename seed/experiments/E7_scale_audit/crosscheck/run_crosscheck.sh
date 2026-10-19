#!/bin/sh
# E7 independent cross-check (one core, about 2 min).
# First pass (cc_*): Ritz-spectral hedgehog, hopfion identity, DL digitisation, audit -> cc_crosscheck.json.
# Second pass (x2_*): shooting hedgehog, direct 3D hopfion, DL quadrature + tick-calibrated digitisation,
# audit by different routes, comparison -> crosscheck.json.
# The DL digitisations need the arXiv PDFs 1103.0013v2.pdf and 1103.2133v2.pdf (arXiv GCS mirror) in
# $LITDIR; without them the recorded readings are used.
set -e
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
LITDIR=${LITDIR:-/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/lit/e7cc}
LITDIR2=${LITDIR2:-/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/e7xc2/lit}
# ---- first pass
python3 cc_hedgehog.py > cc_hedgehog_log.txt 2>&1          # Ritz-spectral hedgehog + pion-mass family
python3 cc_hopfion.py  > cc_hopfion_log.txt 2>&1           # hedgehog-Hopf ansatz: identity + 3D FD check
if [ -f "$LITDIR/1103.0013v2.pdf" ]; then python3 cc_digitize_dl.py "$LITDIR" > cc_digitize_log.txt 2>&1; fi
python3 cc_audit.py    > cc_audit_log.txt 2>&1             # all E7 numbers
python3 cc_diag_hopfion_rms.py > cc_diag_hopfion_rms_log.txt 2>&1   # step-4 diagnosis (uses original e7_hopfion.py)
python3 cc_compare.py  > cc_compare_log.txt 2>&1           # writes cc_crosscheck.json (first pass)
# ---- second pass
python3 x2_hedgehog.py > x2_hedgehog_log.txt 2>&1          # shooting + bisection, analytic tails, pion-mass family
python3 x2_hopfion.py  > x2_hopfion_log.txt 2>&1           # direct 3D evaluation of the hopfion ansatz
python3 x2_dl.py "$LITDIR2" > x2_dl_log.txt 2>&1           # DL model + digitisation
python3 x2_audit.py    > x2_audit_log.txt 2>&1             # all derived numbers, different routes
python3 x2_compare.py  > x2_compare_log.txt 2>&1           # comparison table
python3 x2_crosscheck_json.py > x2_crosscheck_json_log.txt 2>&1   # writes crosscheck.json
