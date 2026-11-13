# Sym²-scale exploratory session (2026-11-12): reproduction

EXPLORATORY. Nothing here is pre-registered or decisive. Read `sym2_session_note_2026-11-12.md` for what was computed and `session_log.md` for every choice and variant.

**Provenance.** The code, computations, figures and written notes in this folder were produced by Claude (Anthropic) sessions working under Matthew Gifford's direction. Matthew chose the questions, set the scope, approved each run and is responsible for this record.

## Software used
- Python 3.13.18, numpy 2.5.3, matplotlib 3.11.2.
- cypari2 2.2.4 linked to PARI/GP 2.17.2. Class numbers come from `qfbclassno` (unconditional for |D| < 2·10^10 per the PARI documentation read, version 2.15.2). `htable.py` refuses any N ≥ 2·10^10.
- Hardware: a 2-core, 7 GB Linux sandbox. The timings below are from that machine.

## Layout expected by the scripts
Run everything from one working folder containing the `code/` files at its top level, with subfolders `data/` and `figs/`. The scripts read and write `data/…` and `figs/…` by relative path, and import `sym2lib.py` and `plots.py` from the same folder.

Run them as `python3 script.py` from that folder. Do not use `-I`, which drops the script folder from the import path. `htable.py` has no local imports, so `-I` is fine there.

**Not in the project:** the class-number tables (`data/*.npz`, ~50 MB each) and the per-prime CSVs (`data/*.csv`). The CSVs were sent as chat attachments. With them in `data/`, steps 4–7 reproduce every figure and number in minutes. Without them, rebuild from step 1. (In this repository the ten CSVs are included in `data/`; only the class-number tables are omitted.)

## Steps

1. **Job lists.**
   - Path E (all t): `data/jobs_E.json` is `[[p, 0]]` for every prime p ≤ 11,323 (1,369 primes, largest first). It was made inline; to recreate it, use `json.dump([[p,0] for p in reversed(primes ≤ 11323)], …)`.
   - Path T (truncated t): `python3 cuts.py` writes `data/jobs_T300.json`, `data/jobs_T1000.json`, `data/jobs_T2500.json` and `data/cuts.json` (τ = 10⁻⁴, every r-th prime, r from the 6,000-prime cap).
2. **Class-number tables** (two workers each, run in parallel):
   ```
   python3 -I htable.py data/jobs_E.json     0 2 data/HE      &  python3 -I htable.py data/jobs_E.json     1 2 data/HE
   python3 -I htable.py data/jobs_T1000.json 0 2 data/HT1000  &  python3 -I htable.py data/jobs_T1000.json 1 2 data/HT1000
   python3 -I htable.py data/jobs_T2500.json 0 2 data/HT2500  &  python3 -I htable.py data/jobs_T2500.json 1 2 data/HT2500
   ```
   Path E took 28 min; T1000 and T2500 took roughly 30–35 min each.
3. **Validation:** `python3 validate.py` writes `data/validation.json`, the copy saved here as `validation.json`. It checks Kronecker–Hurwitz, the dimension-zero weights, `mfheckemat`, τ(p), and the §2.2 identity. `python3 trunc_check.py` prints the τ-truncation check at K = 300.
4. **Per-prime statistics** (CSV columns: per-class elliptic/hyperbolic/identity numerators and Σ w·dim):
   ```
   python3 run_stats.py data/HE      150  C 5  data/E_K150_C_5.csv
   python3 run_stats.py data/HE      150  N 5  data/E_K150_N_5.csv
   python3 run_stats.py data/HE      300  C 5  data/E_K300_C_5.csv
   python3 run_stats.py data/HE      300  N 5  data/E_K300_N_5.csv
   python3 run_stats.py data/HE      100  C c1 data/E_K100_C_c1.csv
   python3 run_stats.py data/HT1000 1000  C 5  data/T_K1000_C_5.csv truncated
   python3 run_stats.py data/HT2500 2500  C 5  data/T_K2500_C_5.csv truncated
   ```
   Only S1 is valid from the T files (the cut uses the combined weight).
5. **Figures:** `python3 make_figs.py` writes `figs/fig1`–`fig6`. Binning (frozen rule) is in `plots.binned`: width 0.2 on (0, 5], with n ≥ 30 required for a binned mean.

   | Figure | Input files |
   |---|---|
   | Fig 1–3 | E_K150_C_5, E_K300_C_5, T_K1000_C_5, T_K2500_C_5 |
   | Fig 4 | E_K150_C_5, E_K300_C_5 |
   | Fig 5 | E_K{150,300}_{C,N}_5 |
   | Fig 6 | E_K100_C_c1 |
6. **Cross-K description of the total:** `python3 describe.py` writes `data/describe.json` (saved here as `describe.json`).
7. **Follow-up readings:** `python3 followup_2026-11-12.py` writes `followup.json` and `followup_extra.json`. It covers the K = 100 line fit over x > 5, the bump/dip checks at K = 1000 and 2500, the width-2 rebin at K = 100 (a variant outside the frozen rule), the cross-K comparison of the elliptic part, and the window extrema at K = 300.

8. **Large x at K = 150 and 200** (follow-up 2):
   ```
   python3 run_stats.py data/HE 150 C 20   data/E_K150_C_20.csv
   python3 run_stats.py data/HE 200 C 11.3 data/E_K200_C_11.3.csv
   # extension table: primes 11,322 < p <= 15·X(200) = 15,046.6, largest first, t_lo = 0
   python3 -c "import json,cypari2;from math import pi;P=15*((199)/(2*pi))**2;json.dump([[int(p),0] for p in reversed(cypari2.Pari()(f'primes([11322,{int(P)}])'))],open('data/jobs_E_ext200.json','w'))"
   python3 -I htable.py data/jobs_E_ext200.json 0 2 data/HEx  &  python3 -I htable.py data/jobs_E_ext200.json 1 2 data/HEx   # 17 min
   python3 validate_ext.py                                   # -> validation_ext.json
   python3 run_stats.py "data/HE*" 200 C 15 data/E_K200_C_15.csv   # the glob reads HE and HEx together
   python3 largex_2026-11-12.py                              # adds F5_largex and F5b_offset_vs_K to followup.json
   ```
   Run `followup_2026-11-12.py` before `largex_2026-11-12.py`: the former rewrites `followup.json`, and the latter adds keys to it.

## Other files
`hproven.py` benchmarks and spot-checks unconditional H against `qfbhclassno`. `wdecay.py` measures how fast the conductor-window k-sum decays, which is what set τ and the truncation cost.
