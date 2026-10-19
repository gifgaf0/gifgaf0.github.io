#!/bin/bash
# E1d: high-resolution 2D slices and the collision-phase diagnostic. ~30-40 min on 2 cores.
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
read S K < <(python choose_slices.py)
echo "slice sigma=$S k=$K"
python e1d_gauss.py sliceAk 2 $S
python e1d_gauss.py sliceAs 2 $K
python e1d_gauss.py phase 2 e1d_sliceAk_$S.json
