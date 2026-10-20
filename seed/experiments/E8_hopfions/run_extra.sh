#!/bin/bash
# Extra checks (1 thread), run after queue B:
#  1. axially symmetric 2D reduction for Q = 1, 2 (independent code; resolution and box-size sequences);
#  2. 3D box-size study at dx = 0.2 (same initial rational map, larger fixed-boundary box).
cd "$(dirname "$0")"
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=python3
[ -f axial2d.done ] || { $P axial2d.py > runs/axial2d.log 2>&1 && touch axial2d.done; }
$P relax.py --run box_Q1_L10 --map A11 --L 10 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 101:400:1e-7
$P relax.py --run box_Q2_L10 --map A21 --L 10 --Lf 7.5 --offset 0.05,0.03,0.02 --stages 101:400:1e-7
echo EXTRA_DONE
