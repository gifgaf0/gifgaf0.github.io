#!/bin/bash
# E1 end to end, resumable: every stage is skipped when its output exists.
# 2 worker processes x 1 thread. Total about 105 min of wall time on 2 free cores
# (measured stage times are listed in REPORT.md, How to reproduce).
#   nohup ./run_all.sh > logs/run_all.log 2>&1 &
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
mkdir -p logs
stage() { out=$1; shift; if [ -s "$out" ]; then echo "[skip] $out"; return; fi
          echo "[start] $out $(date +%T)"; t0=$(date +%s); "$@"; echo "[done] $out $(( $(date +%s) - t0 )) s"; }
# E1a
stage e1a_results.json python e1a_static.py
# E1b: scans (dx, x0, tag, t_post, vmin, vmax, step, nproc) and the time-step check
stage e1b_base.json      python e1b_kkbar.py 0.05 12 base 600 0.15 0.30 0.0001 2
stage e1b_dx0.1.json     python e1b_kkbar.py 0.1 12 dx0.1 600 0.15 0.30 0.0001 2
stage e1b_x0_20.json     python e1b_kkbar.py 0.05 20 x0_20 600 0.15 0.30 0.0001 2
stage e1b_tpost1500.json python e1b_kkbar.py 0.05 12 tpost1500 1500 0.15 0.30 0.0002 2
stage e1b_dx0.025.json   python e1b_kkbar.py 0.025 12 dx0.025 600 0.15 0.30 0.0002 2
stage e1b_dtcheck.json   python e1b_dtcheck.py
# E1c: DSV breather trains
stage e1c_example.json   python e1c_dsv.py example
stage e1c_grid.json      python e1c_dsv.py grid 2
stage e1c_fine.json      python e1c_dsv.py fine 2
stage e1c_high.json      python e1c_dsv.py high 2
stage e1c_dxcheck.json   python e1c_dsv.py dxcheck 2
# E1d: Gaussian packets (slice rule in choose_slices.py)
stage e1d_coarse.json    python e1d_gauss.py coarse 2
stage e1d_single.json    python e1d_gauss.py single 2
read S K < <(python choose_slices.py)
stage e1d_sliceAk_$S.json python e1d_gauss.py sliceAk 2 $S
stage e1d_sliceAs_$K.json python e1d_gauss.py sliceAs 2 $K
stage e1d_phase.json     python e1d_gauss.py phase 2 e1d_sliceAk_$S.json
stage e1d_dxcheck.json   python e1d_gauss.py dxcheck 2
stage e1d_sliceAk_${S}_single.json python e1d_single_slices.py e1d_sliceAk_$S.json 2
stage e1d_sliceAs_${K}_single.json python e1d_single_slices.py e1d_sliceAs_$K.json 2
stage e1d_probe_min.json python e1d_probe_min.py
stage e1d_example.json   python e1d_example.py
# robustness checks added by the third attempt (not preregistered); e1d_extra.py resumes from its .jsonl files
stage e1_verify.json     python e1_verify.py
stage e1b_boxcheck.json  python e1b_boxcheck.py
python e1d_extra.py coarse_oneway 2
python e1d_extra.py single_oneway 2
python e1d_extra.py slice_dx05 2
python e1d_extra.py slice_dx05_single 2
stage e1d_dxladder.json  python e1d_dxladder.py 2
stage e1d_oneway_min.json python e1d_oneway_min.py
# analyses, E1e, results.json, figures
python analyze_e1b.py && python analyze_e1c.py && python analyze_e1d.py && python e1e_quanta.py && python analyze_extra.py && python collect_results.py
echo "[all done] $(date +%T)"
