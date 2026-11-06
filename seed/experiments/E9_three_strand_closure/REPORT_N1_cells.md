# E9 static N = 1 runs in the remaining §6 cells: report

October 31, 2026. Label: Exploration. This report covers the three (κ, η) cells that `PREREG.md` §6 needs and that had not been run: κ = 1 with η = 0.1, κ = 2 with η = 0, and κ = 1 with η = 0. The fourth cell, κ = 2 with η = 0.1, is in `REPORT_N1_rerun.md` and was not rerun. Everything else is as fixed in §9 (Amendment A) and §10 (Amendment B): h = 0.5, R0 = 6, open boundaries, a 65³ grid (box half-width 16), the starts of `starts.py`, maxiter 4000 and a record every 2 iterations. The energy is the one in `gl3.py`. No file in the experiment directory that existed before this session was modified.

**Units.** All outputs are in model units. Lengths are in the coordinate units of `gl3.py`, where ξ = 1/√2, so a length ℓ is ℓ·√2 in units of ξ. The core-scale threshold of §9, 2ξ, is 1.41 coordinate units. Energies are measured above the vacuum as `gl3.vacuum_energy()` gives it (§2.3). No physical identification of the loop is made or implied.

## Summary

| Cell | Start | N = 0 control (P1) | Verdict (§9) | Mechanism |
|---|---|---|---|---|
| κ = 1, η = 0.1 | A (Hopf-linked circle) | collapses, P1 holds | **COLLAPSE** | **Merge onto the core (the §10 mechanism).** Strand 1's loop is drawn inward, re-wraps around the ring (W_z 0 → 1 at it 16), first touches the composite line at a point (it 18), and then lies along it (mean separation 0.01 by it 26). The merged object shrinks to zero (it 40). |
| κ = 1, η = 0.1 | B (§9 helix) | (same control) | **COLLAPSE** | **Merge onto the core (the §10 mechanism).** Closest approach 0 from it 12; merged object shrinks to zero (it 46). |
| κ = 2, η = 0 | A | collapses, P1 holds | **COLLAPSE** | **Point reconnection, then separation.** Strand 1's loop stays centred where it started and is not drawn to the core. The shrinking composite ring sweeps through it at one point (it 14–16), which unlinks it (Lk = 0 at it 18). The two loops then move apart and vanish separately (strand 1 at it 22, composite at it 28). |
| κ = 2, η = 0 | B | (same control) | **COLLAPSE** | **Merge onto the core (the §10 mechanism).** Closest approach 0 from it 20; merged object shrinks to zero (it 34). |
| κ = 1, η = 0 | A | collapses, P1 holds | **COLLAPSE** | **Point reconnection, then separation**, as at κ = 2, η = 0. Point contact at it 20, Lk = 0 at it 22, separation grows to 2.0 by it 24; strand 1 vanishes at it 26, composite at it 34. |
| κ = 1, η = 0 | B | (same control) | **COLLAPSE** | **Merge onto the core (the §10 mechanism).** Closest approach 0 from it 16; merged object shrinks to zero (it 46). |
| all | 81³ box check | — | **Not run** | §10 runs it only for a start that does not collapse. All six collapse. |

Every run ends in the uniform vacuum with no vortex lines in any strand, so Lk = 0 and the Hopf charge is zero. No finite R* exists from any start in any cell.

**§6 outcome.** With `REPORT_N1_rerun.md` (κ = 2, η = 0.1: both starts COLLAPSE), the static N = 1 ring is **COLLAPSE in all four (κ, η) cells, from both starts**. The condition of §6 ("COLLAPSE at both κ values and both η values") is met.

## 1. Commands run

```
cd seed/experiments/E9_three_strand_closure
pip install scipy                    # not present in the container (deviation 1)
python3 prechecks_cells.py > log_cells_prechecks.txt   # coupling, gradient checks, vacuum reference, start checks
./run_cells.sh                       # the 9 runs, 4 concurrent streams
python3 tables_cells.py trace_N1_*_k*.json > log_tables_cells.txt   # the tables below
```

`run_cells.sh` runs, with e = 0.5773502691896258 (κ = 1) and e = 0.2886751345948129 (κ = 2):

```
python3 control_N0_cell.py 65 6 <e> <eta>                  # N = 0 control, per cell
python3 trace_N1_cell.py A 65 6 4000 2 <e> <eta>           # N = 1, start A
python3 trace_N1_cell.py B 65 6 4000 2 <e> <eta>           # N = 1, start B
```

for (κ, η) = (1, 0.1), (2, 0), (1, 0). The runs were grouped as four concurrent streams, with one BLAS/OpenMP thread each (deviation 4): the three controls in sequence; then the A and B starts in sequence, one stream per cell.

### 1.1 The two cell scripts

`trace_N1_cell.py` and `control_N0_cell.py` are copies of `trace_N1.py` and `control_N0.py`. Their diffs against the originals (also in `diff_trace_N1_cell.txt` and `diff_control_N0_cell.txt`):

```diff
--- trace_N1.py	2026-10-31 19:12:29.140274775 +0000
+++ trace_N1_cell.py	2026-10-31 19:13:04.225909307 +0000
@@ -1,6 +1,7 @@
 """Diagnostic re-run of run_N1.py with fine-grained history. Same model, same start, same minimizer call
 (L-BFGS-B is deterministic, so the trajectory is the one run_N1.py follows); only the callback differs.
-usage: python3 trace_N1.py START N R0 MAXITER EVERY
+usage: python3 trace_N1_cell.py START N R0 MAXITER EVERY E ETA [SAVEDIR]
+(trace_N1_cell.py: copy of trace_N1.py; only e, eta as arguments and kappa, eta in the output tag differ.)
 Records every EVERY iterations: energy above vacuum, composite ring radius, strand 1 loop geometry,
 linking number of strand 1's vortex lines with strand 2's and strand 3's (linking.py), and the closest
 approach of any vortex line to the box faces. Prints no verdict.
@@ -9,11 +10,12 @@
 from gl3 import GL3
 from linking import vortex_segments, linking
 start, N, R0, maxiter, every = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
-g = GL3(N=N, h=0.5, eta=0.1)
+e, eta = float(sys.argv[6]), float(sys.argv[7])
+g = GL3(N=N, h=0.5, e=e, eta=eta)
 from starts import start_fields   # Amendment B: corrected starts
 psi = start_fields(g, start, R0); A = np.zeros((3, N, N, N))
 half = (N // 2) * g.h; ax0 = -half
-tag = f'trace_N1_{start}_N{N}_R{R0:g}'
+tag = f'trace_N1_{start}_N{N}_R{R0:g}_k{1 / (e * np.sqrt(3)):.3g}_eta{eta:g}'
 hist = []; t0 = time.time(); it = [0]
 
 def diag(v):
@@ -48,7 +50,7 @@
     d['R23_gl3'] = g.core_radius(p[1]); d['t'] = time.time() - t0
     return d
 
-save = sys.argv[6] if len(sys.argv) > 6 else None
+save = sys.argv[8] if len(sys.argv) > 8 else None
 def cb(v):
     it[0] += 1
     if save and it[0] % every == 0 and it[0] <= 60:
```

```diff
--- control_N0.py	2026-10-31 19:12:28.597468324 +0000
+++ control_N0_cell.py	2026-10-31 19:13:04.226113298 +0000
@@ -1,9 +1,12 @@
-"""N = 0 control (P1): a composite ring with no twist should shrink. Free relaxation from R0."""
+"""N = 0 control (P1): a composite ring with no twist should shrink. Free relaxation from R0.
+control_N0_cell.py: copy of control_N0.py; only e, eta as arguments and kappa, eta in the output tag differ.
+usage: python3 control_N0_cell.py N R0 E ETA"""
 import numpy as np, json, sys, time
 from gl3 import GL3
 N = int(sys.argv[1]) if len(sys.argv) > 1 else 49
 R0 = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
-g = GL3(N=N, h=0.5, eta=0.1)
+e, eta = float(sys.argv[3]), float(sys.argv[4])
+g = GL3(N=N, h=0.5, e=e, eta=eta)
 f = g.ring_field((0, 0, 0), (0, 0, 1), R0)
 psi = np.stack([f, f, f]); A = np.zeros((3, N, N, N))
 E0 = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
@@ -20,5 +23,5 @@
 out = dict(N=N, h=0.5, R0=R0, E_start=float(E0), E_end=float(E), R_end=g.core_radius(psi[1]),
            iters=int(r.nit), converged=bool(r.success), msg=str(r.message), seconds=time.time() - t0,
            history=[x for x in hist if x])
-json.dump(out, open(f'control_N0_N{N}_R{R0:g}.json', 'w'), indent=1)
+json.dump(out, open(f'control_N0_N{N}_R{R0:g}_k{1 / (e * np.sqrt(3)):.3g}_eta{eta:g}.json', 'w'), indent=1)
 print('FINAL', json.dumps({k: out[k] for k in ('E_start', 'E_end', 'R_end', 'iters', 'converged', 'seconds')}))
```

The changes are the two the brief asked for: e and η are arguments passed to `GL3(N=N, h=0.5, e=e, eta=eta)`, and κ and η appear in the output tag. Two further changes follow from them and are recorded as deviation 2:
- In `trace_N1_cell.py` the optional save directory moves from `argv[6]` to `argv[8]`, because `argv[6]` and `argv[7]` are now e and η. It was not used in any run.
- Each docstring has a line saying what the file is and how to call it.

The tag writes κ as `1/(e√3)` to 3 significant figures, so `k1` and `k2`.

## 2. Software, hardware, checks

- Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (installed with pip). Linux container, 4 cores, 15 GB RAM.

### 2.1 Coupling

The `gl3.py` docstring gives ξ = 1/√2 and λ = 1/(e√6). So κ = λ/ξ = √2/(e√6) = 1/(e√3), and e = 1/(κ√3). This is the same relation as `PREREG.md` §1, which writes it with different length units. As computed in `prechecks_cells.py`:

| κ | e | λ | ξ | λ/ξ |
|---|---|---|---|---|
| 1 | 1/√3 = 0.5773502691896258 | 0.707107 | 0.707107 | 1.000000 |
| 2 | 1/√12 = 0.2886751345948129 | 1.414214 | 0.707107 | 2.000000 |

κ = 2 gives e = 1/√12, the value used before.

### 2.2 Gradient checks

`gl3.check_grad` does not take e. `prechecks_cells.py` therefore repeats its body verbatim (N = 6, seed 0, 40 random components, central differences with step 10⁻⁶) with `GL3(N=N, h=0.5, e=e, eta=eta)`. `gl3.py` itself was not edited.

| Cell | Worst relative error |
|---|---|
| κ = 1, η = 0.1 | 3.63 × 10⁻⁷ |
| κ = 2, η = 0 | 1.65 × 10⁻⁷ |
| κ = 1, η = 0 | 3.63 × 10⁻⁷ |

The worst over the three cells is 3.6 × 10⁻⁷. That is the same order as the expected ~2 × 10⁻⁷ (2.09 × 10⁻⁷ at κ = 2, η = 0.1 in `REPORT_N1_rerun.md`). The two κ = 1 values agree to all printed digits. This is plausible: the same random point and components are used, and the worst component evidently does not involve the η term. I did not investigate it further.

### 2.3 Vacuum reference at η = 0

`gl3.vacuum_energy()` returns 3(½η² − η(1 + η))·h³·N³, which is exactly **0** at η = 0. That is the right reference. At η = 0 the vacuum is |ψ_k|² = 1 with A = 0. Its gradient, potential and Josephson energies are all zero (the Josephson term is skipped when η = 0). From `log_cells_prechecks.txt`, on the 65³ grid:

- At η = 0, the energy of the uniform state with |ψ_k|² = 1 minus `vacuum_energy()` is 0. The uniform states with |ψ_k|² = 0.9 and 1.1 lie above it by 514.9 each.
- The uniform state with |ψ_k|² = 1 and relative phases 0°, 120°, 240° also has energy 0. At η = 0 the vacuum is degenerate in the relative phases, as expected: nothing locks them.
- At η = 0.1 (κ = 1), the uniform state with |ψ_k|² = 1.1 matches `vacuum_energy()` to 7 × 10⁻¹², as it should.
- **Final energies above vacuum** for the η = 0 N = 1 runs are 1.0 × 10⁻⁵, 1.4 × 10⁻⁵, 8.9 × 10⁻⁶ and 7.7 × 10⁻⁶. For the η = 0 controls they are 6.2 × 10⁻⁷ and 8.0 × 10⁻⁸. All are positive and ~0, consistent with the reference. The η = 0 runs carry a slower tail than the η = 0.1 runs (§6, note 3).

A further consistency check: the starts are built with A = 0, so e does not enter their energy. Accordingly, the iteration-0 energies at η = 0 are identical at κ = 1 and κ = 2: 1747.4 for A, 1793.9 for B, and 2466.79 for the control's E_start.

### 2.4 Start checks

The start check was run at each cell's (e, η) at N = 65, R0 = 6. The starts do not depend on e or η, and the README's own check (default `GL3(N=65)`) was also run. All four calls give the same output:

```
[{'nseg': [96, 96, 96], 'Lk12': -1.0, 'Lk13': -1.0, 'Lk23': 0.0}, {'nseg': [114, 96, 96], 'Lk12': -1.0000000000000004, 'Lk13': -1.0000000000000004, 'Lk23': 0.0}]
```

So |Lk12| = |Lk13| = 1 for starts A and B in every cell. At iteration 0, strand 1's wall gap is 3.75 (A) and 7.75 (B), matching §10. In no run did strand 1's line come closer to a box face than its iteration-0 gap, and no run ever had an open end on strand 1's line.

### 2.5 Run times and convergence

Every run stopped on `CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL`, well before maxiter.

| Cell | Control: iters / s / E_end | A: iters / s | B: iters / s |
|---|---|---|---|
| κ = 1, η = 0.1 | 85 / 42 / 8.8 × 10⁻⁸ | 124 / 85 | 122 / 85 |
| κ = 2, η = 0 | 113 / 55 / 6.2 × 10⁻⁷ | 326 / 211 | 260 / 168 |
| κ = 1, η = 0 | 86 / 42 / 8.0 × 10⁻⁸ | 273 / 175 | 265 / 171 |

## 3. N = 0 controls (P1)

`control_N0_cell.py` keeps `control_N0.py`'s own settings: maxiter 600 and a history row every 25 iterations (deviation 3). Outputs: `control_N0_N65_R6_k*_eta*.json`, `log_control_N0_k*_eta*.txt`.

| Cell | E_start | it 25: E / R | it 50: E / R | E_end | R_end | P1 |
|---|---|---|---|---|---|---|
| κ = 1, η = 0.1 | 3031.0 | 542.2 / 3.97 | 17.6 / 0 | 8.8 × 10⁻⁸ | 0 | **holds** |
| κ = 2, η = 0 | 2466.8 | 656.2 / 3.72 | 6.8 / 0 | 6.2 × 10⁻⁷ | 0 | **holds** |
| κ = 1, η = 0 | 2466.8 | 505.5 / 4.05 | 10.5 / 0 | 8.0 × 10⁻⁸ | 0 | **holds** |

(R is `gl3.core_radius` of strand 2.) In every cell the untwisted ring shrinks and vanishes within 50 iterations, and the energy falls to the vacuum. **P1 holds in all three cells**, so each cell's N = 1 runs proceeded.

## 4. N = 1 tables, per cell

The columns are as in `REPORT_N1_rerun.md` §3.
- "comp." is the composite line (strands 2 and 3, which coincide in every run: equal segment counts throughout).
- R is the mean distance of line points from the z-axis.
- "centroid x line 1" is the x-coordinate of the centroid of strand 1's line. It is added because it shows whether strand 1's loop moves toward the ring. For start B the helix's centroid sits near the origin from the start, so this column means little there.
- "sep" is the min / mean distance from strand 1's line to the composite line.
- W_z(1) is the winding of strand 1's line around the z-axis.

Every recorded row (every 2 iterations) is shown, up to the first row with no lines, followed by the final record. The rows were generated by `tables_cells.py` from the JSONs. A non-integer Lk₁₂ means the two lattice curves touch, where the linking number is not defined (`REPORT_N1.md` §4, caveat 2).

### 4.1 Cell κ = 1, η = 0.1

**Start A** (`trace_N1_A_N65_R6_k1_eta0.1.json`)

| it | E | R comp. | length comp. | R line 1 | centroid x line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 | 48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 |
| 2 | 1797.2 | 5.74 | 47.0 | 5.82 | 5.81 | 3.80 | 44.0 | 4.75 | 0 | 0 | 5.01 / 5.34 | -1.000 |
| 4 | 1571.1 | 5.31 | 43.0 | 5.98 | 5.97 | 3.62 | 43.0 | 4.75 | 0 | 0 | 4.37 / 5.06 | -1.000 |
| 6 | 1425.5 | 4.99 | 40.0 | 5.79 | 5.78 | 3.30 | 40.0 | 5.25 | 0 | 0 | 3.92 / 4.61 | -1.000 |
| 8 | 1252.0 | 4.72 | 39.0 | 5.49 | 5.44 | 2.93 | 37.0 | 6.25 | 0 | 0 | 3.26 / 4.06 | -1.000 |
| 10 | 1157.5 | 4.60 | 39.0 | 5.34 | 5.28 | 2.62 | 36.0 | 6.25 | 0 | 0 | 3.06 / 3.75 | -1.000 |
| 12 | 993.8 | 4.26 | 38.0 | 4.79 | 4.66 | 2.12 | 35.0 | 7.25 | 0 | 0 | 1.97 / 3.07 | -1.000 |
| 14 | 847.8 | 4.04 | 35.0 | 4.42 | 4.17 | 1.69 | 35.0 | 7.75 | 0 | 0 | 1.17 / 2.40 | -1.000 |
| 16 | 735.3 | 3.98 | 35.0 | 4.32 | 3.95 | 1.45 | 33.0 | 7.75 | 0 | 1 | 0.87 / 2.17 | -1.000 |
| 18 | 620.5 | 3.63 | 32.0 | 3.87 | 3.08 | 0.95 | 33.0 | 8.75 | 0 | 1 | 0.35 / 1.33 | -0.875 |
| 20 | 543.2 | 3.52 | 32.0 | 3.69 | 2.67 | 0.84 | 30.0 | 9.25 | 0 | 1 | 0.35 / 1.04 | -0.750 |
| 22 | 472.1 | 3.24 | 28.0 | 3.29 | 1.83 | 0.53 | 29.0 | 10.25 | 0 | 1 | 0.00 / 0.55 | -0.250 |
| 24 | 422.5 | 3.07 | 27.0 | 3.16 | 1.67 | 0.51 | 27.0 | 10.75 | 0 | 1 | 0.00 / 0.40 | -0.250 |
| 26 | 384.4 | 2.83 | 25.0 | 2.85 | 1.25 | 0.49 | 24.0 | 11.75 | 0 | 1 | 0.00 / 0.01 | -0.375 |
| 28 | 357.9 | 2.80 | 24.0 | 2.81 | 1.22 | 0.48 | 24.0 | 11.75 | 0 | 1 | 0.00 / 0.01 | 0.000 |
| 30 | 328.9 | 2.44 | 20.0 | 2.42 | 0.91 | 0.46 | 22.0 | 12.75 | 0 | 1 | 0.00 / 0.24 | 0.250 |
| 32 | 296.3 | 2.20 | 19.0 | 2.28 | 1.03 | 0.40 | 19.0 | 12.75 | 0 | 1 | 0.00 / 0.15 | -0.250 |
| 34 | 255.7 | 1.70 | 13.0 | 1.77 | 1.00 | 0.24 | 14.0 | 13.25 | 0 | 1 | 0.00 / 0.09 | 0.125 |
| 36 | 200.9 | 1.48 | 11.0 | 1.48 | 1.00 | 0.24 | 11.0 | 13.75 | 0 | 1 | 0.00 / 0.00 | 0.000 |
| 38 | 144.0 | 1.18 | 7.0 | 1.18 | 1.00 | 0.23 | 7.0 | 14.25 | 0 | 0 | 0.00 / 0.10 | 0.125 |
| 40 | 75.1 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |
| 124 (final) | 3.83e-07 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |

**Start B** (`trace_N1_B_N65_R6_k1_eta0.1.json`)

| it | E | R comp. | length comp. | R line 1 | centroid x line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 | 48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 |
| 2 | 1182.5 | 5.82 | 47.0 | 5.84 | 1.35 | 1.27 | 55.0 | 8.75 | 0 | 1 | 1.12 / 1.55 | -1.000 |
| 4 | 932.8 | 5.43 | 44.0 | 5.68 | 1.63 | 1.13 | 52.0 | 8.75 | 0 | 1 | 1.12 / 1.41 | -1.000 |
| 6 | 846.4 | 5.22 | 43.0 | 5.48 | 1.48 | 0.90 | 47.0 | 9.25 | 0 | 1 | 0.71 / 1.17 | -1.000 |
| 8 | 767.9 | 5.09 | 42.0 | 5.30 | 1.23 | 0.76 | 46.0 | 9.75 | 0 | 1 | 0.50 / 0.87 | -1.000 |
| 10 | 741.0 | 5.16 | 42.0 | 5.28 | 1.20 | 0.76 | 46.0 | 9.75 | 0 | 1 | 0.50 / 0.80 | -1.000 |
| 12 | 706.7 | 5.10 | 43.0 | 5.13 | 0.97 | 0.59 | 45.0 | 9.75 | 0 | 1 | 0.00 / 0.49 | -0.875 |
| 14 | 670.6 | 4.90 | 41.0 | 5.02 | 0.76 | 0.47 | 42.0 | 10.25 | 0 | 1 | 0.00 / 0.23 | -0.500 |
| 16 | 652.6 | 4.88 | 41.0 | 4.97 | 0.72 | 0.37 | 42.0 | 10.25 | 0 | 1 | 0.00 / 0.13 | -0.000 |
| 18 | 634.1 | 4.78 | 41.0 | 4.84 | 0.50 | 0.25 | 39.0 | 10.75 | 0 | 1 | 0.00 / 0.22 | -0.000 |
| 20 | 612.2 | 4.60 | 40.0 | 4.56 | 0.49 | 0.25 | 39.0 | 10.75 | 0 | 1 | 0.00 / 0.31 | -0.625 |
| 22 | 590.8 | 4.47 | 38.0 | 4.40 | 0.50 | 0.25 | 35.0 | 11.25 | 0 | 1 | 0.00 / 0.25 | -0.000 |
| 24 | 562.4 | 4.04 | 34.0 | 3.94 | 0.50 | 0.25 | 31.0 | 11.75 | 0 | 1 | 0.00 / 0.16 | 0.000 |
| 26 | 533.7 | 3.99 | 32.0 | 3.94 | 0.50 | 0.25 | 31.0 | 11.75 | 0 | 1 | 0.00 / 0.16 | 0.000 |
| 28 | 497.2 | 3.62 | 30.0 | 3.54 | 0.68 | 0.25 | 30.0 | 11.75 | 0 | 1 | 0.00 / 0.09 | 0.000 |
| 30 | 465.2 | 3.43 | 28.0 | 3.37 | 0.54 | 0.25 | 27.0 | 12.25 | 0 | 1 | 0.00 / 0.03 | 0.000 |
| 32 | 429.3 | 3.01 | 24.0 | 3.03 | 0.67 | 0.25 | 26.0 | 12.25 | 0 | 1 | 0.00 / 0.05 | -0.000 |
| 34 | 394.9 | 2.80 | 23.0 | 2.82 | 0.57 | 0.24 | 23.0 | 12.75 | 0 | 1 | 0.00 / 0.03 | 0.000 |
| 36 | 357.0 | 2.63 | 22.0 | 2.61 | 0.75 | 0.24 | 22.0 | 12.75 | 0 | 1 | 0.00 / 0.10 | -0.000 |
| 38 | 316.7 | 2.30 | 19.0 | 2.23 | 0.61 | 0.24 | 19.0 | 13.25 | 0 | 1 | 0.00 / 0.07 | 0.125 |
| 40 | 266.2 | 1.84 | 15.0 | 1.91 | 0.72 | 0.24 | 16.0 | 13.25 | 0 | 1 | 0.00 / 0.05 | -0.125 |
| 42 | 217.5 | 1.57 | 13.0 | 1.54 | 0.75 | 0.24 | 12.0 | 13.75 | 0 | 1 | 0.00 / 0.13 | -0.125 |
| 44 | 166.6 | 1.24 | 10.0 | 1.31 | 0.79 | 0.22 | 12.0 | 14.25 | 0 | 1 | 0.00 / 0.37 | -0.250 |
| 46 | 110.1 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |
| 122 (final) | 7.1e-07 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |

### 4.2 Cell κ = 2, η = 0

**Start A** (`trace_N1_A_N65_R6_k2_eta0.json`)

| it | E | R comp. | length comp. | R line 1 | centroid x line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1747.4 | 5.92 | 48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 |
| 2 | 1312.5 | 5.49 | 46.0 | 5.98 | 5.97 | 3.86 | 43.0 | 4.75 | 0 | 0 | 4.51 / 5.32 | -1.000 |
| 4 | 1174.0 | 4.94 | 39.0 | 6.01 | 6.00 | 3.38 | 39.0 | 5.25 | 0 | 0 | 3.48 / 4.79 | -1.000 |
| 6 | 1054.1 | 4.19 | 35.0 | 6.01 | 6.00 | 2.87 | 35.0 | 5.75 | 0 | 0 | 2.09 / 4.14 | -1.000 |
| 8 | 885.3 | 3.83 | 31.0 | 6.01 | 6.00 | 2.61 | 31.0 | 6.25 | 0 | 0 | 1.54 / 3.94 | -1.000 |
| 10 | 829.5 | 3.83 | 31.0 | 6.01 | 6.01 | 2.60 | 31.0 | 6.25 | 0 | 0 | 1.54 / 3.94 | -1.000 |
| 12 | 778.6 | 3.73 | 31.0 | 6.01 | 6.00 | 2.36 | 27.0 | 6.75 | 0 | 0 | 1.06 / 3.63 | -1.000 |
| 14 | 716.3 | 3.30 | 27.0 | 6.01 | 6.00 | 1.96 | 23.0 | 7.25 | 0 | 0 | 0.35 / 3.42 | -0.500 |
| 16 | 656.1 | 3.13 | 27.0 | 6.01 | 6.00 | 1.84 | 23.0 | 7.25 | 0 | 0 | 0.35 / 3.31 | -0.500 |
| 18 | 579.5 | 2.66 | 23.0 | 5.90 | 5.89 | 1.28 | 16.0 | 8.25 | 0 | 0 | 1.50 / 3.39 | 0.000 |
| 20 | 485.8 | 2.34 | 20.0 | 5.79 | 5.79 | 0.96 | 13.0 | 8.75 | 0 | 0 | 2.00 / 3.64 | 0.000 |
| 22 | 401.1 | 1.57 | 15.0 | — | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 24 | 293.0 | 1.35 | 11.0 | — | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 26 | 203.7 | 0.42 | 4.0 | — | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 28 | 129.7 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |
| 326 (final) | 1.02e-05 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |

**Start B** (`trace_N1_B_N65_R6_k2_eta0.json`)

| it | E | R comp. | length comp. | R line 1 | centroid x line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1793.9 | 5.92 | 48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 |
| 2 | 1278.1 | 5.47 | 45.0 | 5.85 | 1.87 | 1.29 | 53.0 | 8.25 | 0 | 1 | 1.46 / 1.73 | -1.000 |
| 4 | 1107.8 | 4.85 | 39.0 | 5.26 | 1.74 | 1.17 | 48.0 | 9.25 | 0 | 1 | 1.17 / 1.62 | -1.000 |
| 6 | 976.6 | 4.21 | 35.0 | 4.61 | 1.90 | 0.94 | 41.0 | 9.75 | 0 | 1 | 1.00 / 1.46 | -1.000 |
| 8 | 806.3 | 4.03 | 34.0 | 4.39 | 1.72 | 0.87 | 38.0 | 10.25 | 0 | 1 | 0.71 / 1.31 | -1.000 |
| 10 | 758.1 | 4.03 | 34.0 | 4.39 | 1.72 | 0.86 | 38.0 | 10.25 | 0 | 1 | 0.71 / 1.30 | -1.000 |
| 12 | 721.1 | 3.86 | 31.0 | 4.31 | 1.66 | 0.80 | 38.0 | 10.25 | 0 | 1 | 0.50 / 1.24 | -1.000 |
| 14 | 681.7 | 3.77 | 31.0 | 4.09 | 1.51 | 0.62 | 35.0 | 10.75 | 0 | 1 | 0.50 / 1.04 | -1.000 |
| 16 | 649.4 | 3.63 | 30.0 | 4.02 | 1.47 | 0.60 | 33.0 | 10.75 | 0 | 1 | 0.50 / 0.94 | -1.000 |
| 18 | 609.9 | 3.44 | 28.0 | 3.74 | 1.25 | 0.54 | 32.0 | 11.25 | 0 | 1 | 0.35 / 0.71 | -0.750 |
| 20 | 575.3 | 3.27 | 27.0 | 3.55 | 1.17 | 0.44 | 30.0 | 11.25 | 0 | 1 | 0.00 / 0.56 | -0.500 |
| 22 | 530.8 | 2.86 | 23.0 | 3.21 | 0.94 | 0.25 | 27.0 | 11.75 | 0 | 1 | 0.00 / 0.31 | 0.000 |
| 24 | 483.5 | 2.68 | 23.0 | 2.93 | 0.71 | 0.24 | 24.0 | 12.25 | 0 | 1 | 0.00 / 0.22 | 0.000 |
| 26 | 431.8 | 2.30 | 19.0 | 2.65 | 0.52 | 0.24 | 21.0 | 12.75 | 0 | 1 | 0.00 / 0.34 | -0.000 |
| 28 | 368.3 | 1.95 | 16.0 | 2.26 | 0.47 | 0.24 | 19.0 | 13.25 | 0 | 1 | 0.00 / 0.37 | -0.000 |
| 30 | 280.8 | 1.48 | 12.0 | 1.67 | 0.47 | 0.23 | 17.0 | 13.75 | 0 | 1 | 0.00 / 0.41 | -0.625 |
| 32 | 197.7 | 1.09 | 7.0 | 1.14 | 0.25 | 0.24 | 10.0 | 14.75 | 0 | 1 | 0.00 / 0.57 | -0.375 |
| 34 | 110.1 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |
| 260 (final) | 1.39e-05 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |

### 4.3 Cell κ = 1, η = 0

**Start A** (`trace_N1_A_N65_R6_k1_eta0.json`)

| it | E | R comp. | length comp. | R line 1 | centroid x line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1747.4 | 5.92 | 48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 |
| 2 | 1122.0 | 5.73 | 47.0 | 6.11 | 6.10 | 3.95 | 48.0 | 4.25 | 0 | 0 | 4.83 / 5.46 | -1.000 |
| 4 | 1011.0 | 5.26 | 43.0 | 6.01 | 6.00 | 3.68 | 43.0 | 4.75 | 0 | 0 | 4.29 / 5.12 | -1.000 |
| 6 | 958.8 | 4.93 | 39.0 | 6.01 | 6.00 | 3.37 | 39.0 | 5.25 | 0 | 0 | 3.48 / 4.76 | -1.000 |
| 8 | 895.6 | 4.83 | 39.0 | 6.01 | 6.00 | 3.18 | 39.0 | 5.25 | 0 | 0 | 3.10 / 4.50 | -1.000 |
| 10 | 865.3 | 4.83 | 39.0 | 5.90 | 5.89 | 3.04 | 36.0 | 5.75 | 0 | 0 | 3.02 / 4.34 | -1.000 |
| 12 | 815.0 | 4.56 | 39.0 | 5.99 | 5.98 | 2.66 | 33.0 | 5.75 | 0 | 0 | 2.26 / 3.84 | -1.000 |
| 14 | 753.4 | 4.38 | 35.0 | 6.04 | 6.03 | 2.53 | 31.0 | 6.25 | 0 | 0 | 1.97 / 3.73 | -1.000 |
| 16 | 697.5 | 4.05 | 35.0 | 6.02 | 6.02 | 2.19 | 27.0 | 6.75 | 0 | 0 | 1.54 / 3.28 | -1.000 |
| 18 | 626.0 | 3.64 | 31.0 | 5.84 | 5.83 | 1.81 | 24.0 | 7.25 | 0 | 0 | 0.61 / 2.97 | -1.000 |
| 20 | 543.1 | 3.30 | 28.0 | 5.78 | 5.78 | 1.41 | 20.0 | 7.75 | 0 | 0 | 0.35 / 2.58 | -0.625 |
| 22 | 470.6 | 2.89 | 25.0 | 5.76 | 5.75 | 0.91 | 12.0 | 8.75 | 0 | 0 | 1.00 / 2.61 | -0.000 |
| 24 | 371.2 | 2.44 | 21.0 | 5.75 | 5.75 | 0.48 | 8.0 | 9.25 | 0 | 0 | 2.00 / 3.02 | 0.000 |
| 26 | 310.5 | 2.20 | 20.0 | — | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 28 | 245.9 | 1.86 | 17.0 | — | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 30 | 198.1 | 1.46 | 12.0 | — | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 32 | 139.6 | 0.74 | 7.0 | — | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 34 | 86.5 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |
| 273 (final) | 8.89e-06 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |

**Start B** (`trace_N1_B_N65_R6_k1_eta0.json`)

| it | E | R comp. | length comp. | R line 1 | centroid x line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1793.9 | 5.92 | 48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 |
| 2 | 933.0 | 5.74 | 47.0 | 5.94 | 1.85 | 1.31 | 53.0 | 8.25 | 0 | 1 | 1.46 / 1.66 | -1.000 |
| 4 | 785.8 | 5.31 | 43.0 | 5.58 | 1.71 | 1.20 | 52.0 | 8.75 | 0 | 1 | 1.17 / 1.56 | -1.000 |
| 6 | 736.8 | 5.13 | 42.0 | 5.37 | 1.67 | 0.96 | 46.0 | 9.25 | 0 | 1 | 1.00 / 1.33 | -1.000 |
| 8 | 687.9 | 5.08 | 42.0 | 5.33 | 1.48 | 0.90 | 47.0 | 9.25 | 0 | 1 | 0.87 / 1.14 | -1.000 |
| 10 | 667.5 | 5.08 | 42.0 | 5.33 | 1.45 | 0.89 | 47.0 | 9.25 | 0 | 1 | 0.71 / 1.10 | -1.000 |
| 12 | 644.2 | 4.98 | 41.0 | 5.10 | 1.18 | 0.73 | 46.0 | 9.75 | 0 | 1 | 0.50 / 0.79 | -1.000 |
| 14 | 614.3 | 4.89 | 39.0 | 5.05 | 1.18 | 0.61 | 42.0 | 9.75 | 0 | 1 | 0.35 / 0.62 | -0.750 |
| 16 | 594.0 | 4.84 | 39.0 | 4.91 | 0.83 | 0.53 | 42.0 | 10.25 | 0 | 1 | 0.00 / 0.42 | -0.500 |
| 18 | 572.8 | 4.68 | 41.0 | 4.78 | 0.76 | 0.42 | 42.0 | 10.25 | 0 | 1 | 0.00 / 0.13 | -0.250 |
| 20 | 551.9 | 4.48 | 38.0 | 4.51 | 0.68 | 0.25 | 36.0 | 10.75 | 0 | 1 | 0.00 / 0.13 | -0.625 |
| 22 | 523.8 | 4.18 | 36.0 | 4.20 | 0.50 | 0.25 | 35.0 | 11.25 | 0 | 1 | 0.00 / 0.29 | -0.250 |
| 24 | 501.4 | 4.05 | 36.0 | 4.13 | 0.50 | 0.25 | 35.0 | 11.25 | 0 | 1 | 0.00 / 0.25 | -0.000 |
| 26 | 475.2 | 3.85 | 33.0 | 3.77 | 0.50 | 0.25 | 31.0 | 11.75 | 0 | 1 | 0.00 / 0.14 | 0.125 |
| 28 | 439.4 | 3.55 | 28.0 | 3.44 | 0.50 | 0.25 | 29.0 | 12.25 | 0 | 1 | 0.00 / 0.19 | 0.000 |
| 30 | 410.3 | 3.23 | 26.0 | 3.24 | 0.44 | 0.25 | 27.0 | 12.25 | 0 | 1 | 0.00 / 0.24 | -0.000 |
| 32 | 381.8 | 2.87 | 24.0 | 2.79 | 0.50 | 0.24 | 23.0 | 12.75 | 0 | 1 | 0.00 / 0.11 | -0.125 |
| 34 | 346.0 | 2.78 | 22.0 | 2.71 | 0.52 | 0.24 | 23.0 | 12.75 | 0 | 1 | 0.00 / 0.14 | -0.000 |
| 36 | 305.9 | 2.30 | 19.0 | 2.30 | 0.55 | 0.24 | 19.0 | 13.25 | 0 | 1 | 0.00 / 0.00 | 0.000 |
| 38 | 267.2 | 2.14 | 18.0 | 2.14 | 0.72 | 0.24 | 18.0 | 13.25 | 0 | 1 | 0.00 / 0.00 | -0.000 |
| 40 | 229.5 | 1.75 | 15.0 | 1.79 | 0.60 | 0.24 | 15.0 | 13.75 | 0 | 1 | 0.00 / 0.07 | 0.250 |
| 42 | 173.4 | 1.29 | 12.0 | 1.35 | 0.69 | 0.24 | 12.0 | 13.75 | 0 | 1 | 0.00 / 0.21 | 0.125 |
| 44 | 114.0 | 0.83 | 6.0 | 0.94 | 0.75 | 0.23 | 6.0 | 14.75 | 0 | 0 | 0.00 / 0.12 | -0.125 |
| 46 | 67.0 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |
| 265 (final) | 7.72e-06 | — | 0 | — | — | — | 0 | — | — | — | — | 0 (no lines) |

## 5. Verdicts and mechanisms

The §9 rule: STABLE if the free relaxation from R = 6 stops at a finite R* > 2ξ, with strand 1's loop still linked, and the result survives the 81³ box (§10). COLLAPSE if the ring shrinks to core scale or strand 1's loop unlinks by reconnection. MARGINAL otherwise. The §10 rule: if strand 1's line merges onto the composite core (closest approach below one grid spacing) and the configuration then shrinks, the mechanism is "the twist has no protected place to live where all three amplitudes vanish". The report must say whether that mechanism, or a different one, is what happened.

### 5.1 κ = 1, η = 0.1

**Start A: COLLAPSE, by merge onto the core (§10 mechanism).**
- **Linked phase, it 0–16.** Lk = −1.000 exactly. Strand 1's loop is drawn inward as a whole: its centroid moves from x = 6.13 to 3.95, and the composite ring shrinks from R = 5.92 to 3.98.
- **Re-wrapping, it 16.** Strand 1's loop passes through x = 0 at the start, so its inner arc lies near the z-axis (rxy_min 0.35 at it 0). At it 16 that arc crosses the axis, and W_z(1) goes from 0 to 1. No other line is near the axis then (the composite is at R ≈ 4), so this is not a contact with the composite. After it, strand 1's loop goes once around the ring, as the start-B helix does.
- **Contact and merge, it 18–26.** The first contact (min separation 0.35 < h) is at it 18, at one point: the mean separation is still 1.33. From it 22 the min separation is 0, and the mean falls to 0.55, then 0.40, then 0.01 at it 26–28. Strand 1's radius then tracks the composite radius to within 0.1.
- **Shrinking after the merge.** The merged object shrinks monotonically from R ≈ 2.8 to 1.18 at it 38 (0.83ξ, below core scale), and all lines are gone at it 40.

By the literal §10 test (closest approach below one grid spacing, then the configuration shrinks), this is the §10 mechanism. It differs from κ = 2, η = 0.1 start A, where strand 1's loop cut through the core at a point and vanished at once. Here it lies along the core for about 20 iterations.

**Flag:** contact began at a single point (it 18) before the merge spread along the core. Lk is non-integer from it 18, so I cannot tell whether the link was undone at that first contact or later. In either reading the configuration ends merged and shrinks to nothing.

**Start B: COLLAPSE, by merge onto the core (§10 mechanism).**
- **Approach, it 0–10.** The helix closes in on the core: mean separation 1.95 → 0.80, z_rms 1.36 → 0.76. Lk = −1.000 and W_z = 1.
- **Merge, from it 12.** The min separation is 0 from it 12. The mean stays ≤ 0.49 to the end, and strand 1's z_rms locks at 0.25 from it 18.
- **Shrinking after the merge.** The merged object shrinks monotonically, R 5.1 → 1.24 (0.88ξ) at it 44. All lines are gone at it 46.
- **The composite was barely shrinking before the merge** (R 5.92 → 5.10 by it 12, then nearly flat over it 8–12). Most of its shrinkage came after the merge.

### 5.2 κ = 2, η = 0

**Start A: COLLAPSE, by point reconnection, then separation.**
- **Strand 1 is not attracted to the core.** Through the linked phase (it 0–12, Lk = −1.000) strand 1's loop keeps its centroid near x = 6: 6.13 at it 0, then 5.97–6.01, and 6.00 ± 0.01 from it 4 to it 16. It shrinks about its own centre, length 48 → 27. Its inner and outer arcs close in symmetrically (rxy_min/max 0.35/12.25 → 2.75/9.25). Meanwhile the composite ring shrinks inward, from 5.92 to 3.73.
- **Unlinking at a point, it 14–16.** The inward-moving composite line meets strand 1's inner arc at one place: min separation 0.35 (< h) with mean 3.42 and 3.31, and Lk = −0.5. At it 18 the link is gone (Lk = 0.000), and the min separation is back up to 1.50.
- **Separation, it 18–20.** The two loops move apart (min separation 1.50 → 2.00, mean 3.39 → 3.64). Each shrinks on its own: strand 1 stays near x = 5.8 and vanishes at it 22, away from the composite. The untwisted composite shrinks through R = 1.35 (0.95ξ) at it 24 and vanishes at it 28, as in the N = 0 control.

**Mechanism.** This is not the §10 mechanism: strand 1's line never lies along the core. Of the named mechanisms, the unlinking event is a **point reconnection**: a single-point crossing of the two lines, as in κ = 2, η = 0.1 start A. What follows is **separation**: the unlinked loops move apart and vanish separately.

What is new compared with η = 0.1 is that strand 1's loop shows no attraction to the core before the crossing. Its centroid does not move, and the crossing happens because the composite ring's contraction carries its line through strand 1's line. That is the behaviour expected when the strands are not phase-locked (step 2: strand 1's fractional vortex is then only log-confined to the composite). A static run cannot test that attribution.

**Flag (literal reading of "separation").** A loop linked with another cannot move away from it without a crossing. So "separation" cannot be the whole unlinking mechanism; it can only be what happens after the crossing. I record the mechanism as "point reconnection, then separation", and I flag the brief's category "separation (rather than merging or reconnecting)" as not realisable on its own.

**Start B: COLLAPSE, by merge onto the core (§10 mechanism).**
- **Approach, it 0–16.** The helix closes in on the core (mean separation 1.95 → 0.94) while both shrink (composite 5.92 → 3.63). Lk = −1.000 and W_z = 1.
- **Merge.** The first contact below h is at it 18 (0.35, mean 0.71). From it 20 the min separation is 0, the mean stays ≤ 0.57, and strand 1's z_rms locks at 0.24.
- **Shrinking after the merge.** The merged object shrinks, R 3.27 → 1.09 (0.77ξ) at it 32, and all lines are gone at it 34. Strand 1's loop did **not** separate from the composite, even though the strands are not phase-locked.

### 5.3 κ = 1, η = 0

**Start A: COLLAPSE, by point reconnection, then separation**, the same sequence as κ = 2, η = 0.
- **Linked phase.** Strand 1's centroid stays at x = 5.75–6.13, and its R at 5.75–6.15, throughout. Lk = −1.000 to it 18, while the composite shrinks 5.92 → 3.64.
- **Unlinking at a point, it 20.** Point contact: min separation 0.35, mean 2.58, Lk = −0.625. At it 22 Lk is 0 and the min separation is 1.00.
- **Separation.** At it 24 the min separation is 2.00. Strand 1 vanishes on its own at it 26. The untwisted composite shrinks through R = 0.74 (0.52ξ) at it 32 and vanishes at it 34.
- Not the §10 mechanism. The same flag on "separation" applies.

**Start B: COLLAPSE, by merge onto the core (§10 mechanism).**
- **Approach.** The first contact below h is at it 14 (0.35, mean 0.62). The min separation is 0 from it 16, the mean stays ≤ 0.42 after that, and z_rms locks at 0.25 from it 20.
- **Shrinking after the merge.** The merged object shrinks, R 4.84 → 0.83 (0.59ξ) at it 44, and all lines are gone at it 46. No separation.

### 5.4 Across cells

| Start | κ = 2, η = 0.1 (rerun) | κ = 1, η = 0.1 | κ = 2, η = 0 | κ = 1, η = 0 |
|---|---|---|---|---|
| A | point reconnection | merge onto the core | point reconnection, then separation | point reconnection, then separation |
| B | merge onto the core | merge onto the core | merge onto the core | merge onto the core |
| Composite gone at it (A / B) | 27 / 36 | 40 / 46 | 28 / 34 | 34 / 46 |

- **Start B merges in all four cells.** This includes η = 0, where strand 1 is not phase-locked to the composite.
- **Start A's route depends on the cell.** At η = 0.1, strand 1's loop is drawn inward toward the ring: its centroid moves from 6.1 to 3.9 at κ = 1, and its R falls from 6.15 to 4.4 at κ = 2 in the rerun. At η = 0 it stays where it started. At η = 0 the unlinking crossing is caused by the composite's own contraction, and the unlinked loops then part.
- **No run shows a pause in R or a plateau in E while strand 1 is linked.** In every run the composite radius at the recorded iterations is non-increasing up to small lattice jitter: equal values at a few consecutive records, +0.06 at it 10 in κ = 1, η = 0.1, B and +0.01 at it 10 in κ = 2, η = 0, B. E falls at every recorded iteration.
- The N = 0 controls vanish within 50 iterations (recorded every 25). The N = 1 composites vanish at it 28–46. Because the controls are sampled more coarsely, this comparison is qualitative only.

## 6. Notes and caveats

1. As in the earlier reports, L-BFGS iterations are a minimizer path, not a time evolution. The histories show that the energy landscape is downhill from each start to the vacuum. They do not show a physical trajectory.
2. Statements at the level of one grid spacing (h = 0.5 = 0.71ξ) are resolution-limited. Where Lk is non-integer (touching lattice curves), the moment of unlinking is not resolved. I did not run every-iteration diagnostics, as `REPORT_N1_rerun.md` did (its deviation 2). The every-2 records were enough to identify each mechanism, and the brief did not ask for them.
3. **Slow tail at η = 0.** After all lines are gone (it 28–46), the η = 0 runs take a further 220–300 iterations to bring E from ~100 to ~10⁻⁵. The η = 0.1 runs take 76–84 (see the JSONs). I did not diagnose the cause. A plausible reading, not checked, is that relative-phase gradients left by the strand-1 loop relax slowly when η = 0 because nothing gives the relative phases a mass. No fields were saved, so this cannot be checked from the outputs.
4. No field files were saved. As in the rerun, the final-state claims rest on the line detection (zero segments in every strand) and on E above vacuum.

## 7. Deviations, collected

1. **SciPy installed with pip.** SciPy was not present in the container, and `gl3.py` needs it.
2. **Two changes to the cell scripts beyond the two the brief listed** (§1.1). In `trace_N1_cell.py` the save-directory argument moves from `argv[6]` to `argv[8]`; this is forced by the new arguments and the directory was unused. Each docstring gained one descriptive line. Nothing else differs (diffs in §1.1).
3. **The controls use `control_N0.py`'s own maxiter 600 and its every-25 history, not maxiter 4000 and every-2.** The brief says to write `control_N0_cell.py` "the same way" as `trace_N1_cell.py`, changing only e, η and the tag. The general run settings ("maxiter 4000, record every 2 iterations") also appear under the per-cell runs. I took the script-copy instruction as the more literal and specific one. **Flagged as an ambiguity.** It has no effect on the outcome: all three controls converged in 85–113 iterations, far below 600.
4. **Concurrency and threads.** The 9 runs went in four concurrent streams with `OMP_NUM_THREADS = OPENBLAS_NUM_THREADS = MKL_NUM_THREADS = 1`. The earlier runs used default threading. L-BFGS-B is deterministic for a given floating-point path. A different BLAS thread count can change the last bits of reductions, so a bit-for-bit match with a default-threaded run is not guaranteed. No such rerun was made.
5. **Gradient check adapted, not called.** `gl3.check_grad` cannot take e, so its body was repeated with e passed (`prechecks_cells.py`), as the brief allowed.
6. **Helper scripts added:** `prechecks_cells.py` (coupling, gradient checks, vacuum reference, start checks), `run_cells.sh` (the run list) and `tables_cells.py` (the tables of §4). None changes a run.
7. **No 81³ box check.** Its condition in §10 (a start that does not collapse) was not met in any cell.
8. **"Separation" as a mechanism** is recorded as "point reconnection, then separation" for the η = 0 start-A runs (§5.2 flag). This is my literal reading.
9. `log_run_cells.txt` holds only the runner's final line. Each run's start time is the first line of its own log.

No parameter was re-tuned. Only the three cells named in the brief were run. h, R0, the box and the starts are as fixed. No term was added to the energy. `gl3.py`, `starts.py`, `linking.py`, `trace_N1.py`, `control_N0.py` and `STATUS_step3.md` are unchanged.

## 8. What is and isn't established

**Established, at h = 0.5, 65³, R0 = 6, from starts A and B:**
- In each of the three new cells the N = 0 control collapses (P1 holds), and both N = 1 starts COLLAPSE by §9, ending in the vacuum with no vortex lines.
- Together with `REPORT_N1_rerun.md`, the static twisted ring collapses in all four (κ, η) cells of §6, so the §6 condition is met.
- The §10 mechanism (merge onto the core, then shrinkage) occurs in 4 of the 6 new runs: start B in all three cells, and start A at κ = 1, η = 0.1.
- At η = 0, start A unlinks by a point crossing, driven by the composite's contraction, with no visible attraction of strand 1's loop to the core. The loops then separate and vanish independently.

**Not established:**
- That no stable twisted ring exists anywhere in these cells. Only two starts, one R0, one grid spacing and one box were used. Resolution was not varied: h = 0.5 is 0.71ξ, and the merge and contact events happen at the one-grid-spacing scale.
- The exact iteration at which each link is lost, wherever the lattice curves touch (non-integer Lk).
- Any statement about time evolution. These are minimizer paths.
- That the η = 0 "no attraction" reflects the log confinement of step 2. This is consistent with it, but not tested.
- The cause of the slow η = 0 tail (§6, note 3).
- Anything outside the four cells, the model of `gl3.py`, or assumptions A1–A2. No physical identification is made or implied.
