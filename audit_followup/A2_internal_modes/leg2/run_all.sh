#!/usr/bin/env bash
# A2 leg 2 -- runs every computation and writes the outputs next to the code.
# Requirements: python3 with sympy, numpy, scipy, python-flint (pip install --break-system-packages python-flint).
set -euo pipefail
cd "$(dirname "$0")"
python3 octonion_g2.py        > octonion_g2_output.txt 2>&1
python3 task1_invariants.py   > task1_output.txt 2>&1
python3 -W ignore task3_topology.py > task3_output.txt 2>&1
python3 task4_wm.py           > task4_output.txt 2>&1
python3 task5_coupling.py     > task5_output.txt 2>&1
python3 task6_moving.py       > task6_output.txt 2>&1
python3 make_summary.py       > make_summary_output.txt 2>&1
echo "done"
