# E9 N = 1 runs (P2): report

October 31, 2026. Label: Exploration. Model, parameters and verdict rules as fixed in `PREREG.md` §9 (Amendment A): κ = 2 (e = 1/√12), η = 0.1, h = 0.5, open boundaries, energy exactly as in `gl3.py`. Nothing in the model, the parameters or the starts was changed. All outputs are energies and lengths in model units (ξ = 1/√2; lengths below are in grid units of the code, i.e. the units of `gl3.py` coordinates, not divided by ξ unless stated).

## Summary

| Start | Grid | Verdict (§9) | Short reason |
|---|---|---|---|
| A (Hopf-linked) | 49³ | **COLLAPSE** (with a caveat on the start, see §4) | The composite ring shrank from radius 5.9 to 1.8 and vanished at iteration 46; the final state is the uniform vacuum with no vortex lines, so strand 1 is not linked with anything. |
| B | 49³ | **Not run: deviation** | `run_N1.py` start B is not the start that §9 fixes, and as coded it is not linked at all (Lk = 0). See §3. |
| A (box check) | 65³ | **Not run** | The plan runs the box check only if neither 49³ run is a COLLAPSE. Start A is a COLLAPSE. |

## 1. Commands run

```
cd seed/experiments/E9_three_strand_closure
python3 gl3.py                                   # gradient check
python3 run_N1.py A 49 6 4000 > log_A_N49.txt    # the pre-registered run
python3 linking.py --start A 6                   # linking of the analytic starts (also B, and B_xz for comparison)
python3 linking.py --start B 6
python3 trace_N1.py A 49 6 4000 2 /tmp/traceA > log_trace_A_N49.txt   # diagnostic re-run, history every 2 iterations
python3 linking.py N1_A_N49_R6_final.npz
```

`linking.py` and `trace_N1.py` are new in this session and are diagnostics only: they import `gl3.py` unchanged and add no term to the energy. `trace_N1.py` builds the same start and makes the same `g.minimize(..., maxiter=4000, gtol=1e-5)` call as `run_N1.py`; only the callback differs. L-BFGS-B is deterministic, and the re-run reproduces the official run exactly (133 iterations, final E − E_vac = 5.451611286844127 × 10⁻⁷ in both), so its fine-grained history is the history of the pre-registered run.

## 2. Software and hardware

Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (SciPy was not present in the container and was installed with `pip install scipy` at the start of the session). Linux container, 4 cores, 15 GB RAM.

Gradient check: `gradient check, worst relative error: 2.0925355138465372e-07`, as expected.

Run time: start A at 49³ took 29 s (133 iterations) to converge (`CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL`), not the ~20 min the hand-off estimated, because the configuration annihilated early.

## 3. Deviation: start B is not the pre-registered start, and is unlinked

§9 fixes the second start as "strand 1 on a (1,1) helix of minor radius 2 around the ring core". `run_N1.py` start B instead puts strand 1 on a circle of radius 2 centred on the ring core at (R0, 0, 0) with plane normal (1, 0, 0), i.e. in the y–z plane. That has two problems:

1. It is a meridian circle, not a (1,1) helix. Even a meridian circle placed correctly is a different start, not the one §9 fixes.
2. With normal (1, 0, 0) the circle lies in the plane x = R0, which contains the ring's tangent at (R0, 0, 0). The composite ring touches that plane only tangentially and does not pass through the disk. The circle crosses the z = 0 plane at (6, ±2, 0), both outside the ring (distance √40 > 6). **So the start is not linked with the composite ring.** Measured with `linking.py` (method in §5): Lk(strand 1, strand 2) = 0.000 for start B as coded. For comparison, the same circle with normal (0, 1, 0) (x–z plane) gives Lk = 1.000, and start A gives Lk = 1.000.

So start B, as coded, would test an unlinked (N = 0-like) start that the pre-registration does not contain. Per the session instructions I did not fix it and did not run it. To be decided by the author: implement the (1,1) helix start of §9 (e.g. strand 1's phase from a helical core curve) and run it as start B.

## 4. Start A at 49³: what happened

The full history (every 2 iterations) is in `trace_N1_A_N49_R6.json`; the official run's own history (every 100 iterations) is in `N1_A_N49_R6.json`. Columns: E is the energy above the true vacuum; "comp." is the composite (strands 2 and 3, whose lines coincide throughout); R is the mean distance of the vortex-line points from the z-axis; R23 gl3 is `gl3.core_radius` of strand 2; W_z is the winding of strand 1's line around the z-axis (0 for a Hopf loop, ±1 for a ring around the axis); "open ends" counts places where strand 1's line ends (only possible on a box face); sep is the min/mean distance from strand 1's line to the composite line.

| it | E | R comp. | R23 gl3 | length comp. | R line 1 | z_rms line 1 | length line 1 | wall gap line 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ (Gauss) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 4784.8 | 5.93 | 6.03 | 64.0 | 5.85 | 4.24 | 63.0 | 0.25 | 0 | 0 | 5.39 / 5.77 | 1.000 |
| 4 | 3889.3 | 5.63 | 5.83 | 46.0 | 5.25 | 4.09 | 44.0 | 0.00 | 2 | −1 | 5.01 / 5.42 | (open) |
| 8 | 2697.9 | 5.19 | 5.09 | 45.0 | 5.26 | 3.60 | 47.0 | 0.00 | 2 | −1 | 3.91 / 4.74 | (open) |
| 12 | 2210.6 | 4.84 | 4.95 | 42.0 | 5.48 | 3.15 | 52.0 | 0.00 | 2 | −1 | 2.81 / 4.05 | (open) |
| 16 | 1642.4 | 4.53 | 4.54 | 39.0 | 5.66 | 2.40 | 54.0 | 0.00 | 2 | −1 | 1.54 / 3.17 | (open) |
| 20 | 1165.7 | 4.17 | 4.25 | 36.0 | 5.09 | 1.88 | 49.0 | 1.75 | 0 | −1 | 0.50 / 2.25 | 1.000 |
| 24 | 853.4 | 3.83 | 3.92 | 35.0 | 4.10 | 1.48 | 39.0 | 4.75 | 0 | −1 | 0.00 / 0.93 | (unresolved) |
| 28 | 702.3 | 3.57 | 3.51 | 33.0 | 3.85 | 1.19 | 36.0 | 5.25 | 0 | −1 | 0.00 / 0.53 | (unresolved) |
| 32 | 605.2 | 3.29 | 3.13 | 30.0 | 3.44 | 0.97 | 31.0 | 6.25 | 0 | −1 | 0.00 / 0.26 | (unresolved) |
| 36 | 505.9 | 2.83 | 2.78 | 25.0 | 2.88 | 0.74 | 26.0 | 7.25 | 0 | −1 | 0.00 / 0.26 | (unresolved) |
| 40 | 379.8 | 2.20 | 2.27 | 15.0 | 2.20 | 0.56 | 17.0 | 8.75 | 0 | −1 | 0.00 / 0.40 | (unresolved) |
| 44 | 212.3 | 1.76 | 1.87 | 4.0 | 1.89 | 0.23 | 8.0 | 9.25 | 0 | 0 | 0.35 / 0.52 | (unresolved) |
| 46 | 130.4 | — | 0 | 0 | — | — | 0 | — | — | — | — | 0 (no lines) |
| 48 | 65.6 | — | 0 | 0 | — | — | 0 | — | — | — | — | 0 |
| 100 | 6.3 × 10⁻⁴ | — | 0 | 0 | — | — | 0 | — | — | — | — | 0 |
| 133 (final) | 5.5 × 10⁻⁷ | — | 0 | 0 | — | — | 0 | — | — | — | — | 0 |

**Energy.** E falls monotonically, from 4785 to 130 by iteration 46, when the last vortex line disappears. It then decays to the vacuum value (5 × 10⁻⁷ at convergence). There is no plateau at any finite size.

**Core radii.** The composite ring shrinks monotonically, from R ≈ 5.9 to 1.8 (≈ 2.5 ξ) at iteration 44, with its line length falling from 64 to 4. It is gone at iteration 46. Strand 1's line follows a sequence:
- Iterations 2–16: its outer part, which starts at the box face x = +12 (see the caveat below), is attached to that open face (two open ends). While it is attached, its winding around the z-axis changes from 0 to −1.
- Iterations 18–20: it is a closed curve again, still linked with the composite (Lk = 1.000) and now also winding once around the z-axis. It has become a (1,1) curve wrapped around the composite core, the helical configuration Amendment A anticipated.
- Iteration 22 onward: it falls onto the composite core. Its radius tracks the composite radius, z_rms drops to 0.2, and the mean separation from the composite line falls to 0.25–0.5, i.e. ≤ h.
- Iteration 46: it vanishes with the ring.

**Final state.** |ψ_k|² = 1.1000 ± 10⁻⁵ = 1 + η at every site for all three strands. There are no vortex lines in any component. Strand 1 is **not** linked with the composite ring at the end, because neither line exists. Lk = 0 and the Hopf charge is zero.

**Verdict by §9: COLLAPSE.** "The ring shrinks to core scale" is met: the composite ring went monotonically through R ≈ 1.8 to zero, and the energy reached the vacuum. No finite R* exists, and the end state is not linked.

**Caveat on this verdict (inconclusive part, stated honestly).**
1. **The start touches the box.** On the 49³ grid the box runs from −12 to +12. Start A's strand-1 circle (radius R0 = 6, centred at (6, 0, 0)) reaches x = 12, so its core sits on the box face (wall gap 0.25 at iteration 0, 0 from iteration 2). With open boundaries, a vortex line can end on the face. The change of strand 1's topology at iterations 2–16 (W_z 0 → −1) happened while the line was attached there, so the boundary took part in it.
   - What this does not affect: the linking number with the composite was 1 both before (iteration 0) and after (iterations 18–20) the wall episode.
   - What this run cannot exclude: that the later fall of strand 1 onto the composite core, and the collapse, were helped by the shape the wall episode produced.
   - The obvious clean test is start A at 65³ (box ±16, 4 units of margin), the run listed as the box check. §9 and the hand-off run it only if the 49³ run is not a COLLAPSE, so I did not run it. Whether to run it as a diagnostic is the author's decision.
2. **When the link is lost is not resolved.** From iteration 22 to 44 strand 1's line lies within one lattice spacing of the composite core along part of its length (min separation 0). There the linking number of the two lattice curves is not defined: the Gauss sum gives non-integers (0.75, 0.5, 1.375, −0.125, …), which is the signature of coincident segments, not a physical value. I can therefore say that the link existed at iteration 20 and does not exist at iteration 46. I cannot say whether it was undone by a reconnection of strand 1 through the composite core before the ring disappeared, or simply vanished with the ring. Under §9 either reading is a COLLAPSE.
3. **The history is not a time evolution.** L-BFGS iterations are a minimizer path, not a physical time evolution, and L-BFGS can take large steps. The history shows the energy landscape is downhill all the way from this start to the vacuum. It does not show a dynamical trajectory.

For reference, the untwisted N = 0 control (`REPORT_control.md`) also vanished within about 50 iterations from R = 6 on the same grid. On this grid, start A collapsed on the same scale as the control.

## 5. Method for the linking check

`linking.py`, applied to the saved fields (`*_final.npz`) and, during the diagnostic re-run, to the fields at every second iteration:

1. **Vortex lines** of component k are the dual links through plaquettes on which the raw phase of ψ_k winds by 2πw (sum of wrapped phase differences around the plaquette). The raw winding counts enclosed zeros and does not depend on A. A random perturbation of size 10⁻¹⁰ is added before taking phases. This breaks exact ties: phase differences of exactly ±π, and ψ exactly 0, both of which occur in the analytic starts centred on a site plane.
2. **Closure** is checked by in/out degree at every dual node ("open ends" = 0 means all lines are closed loops).
3. **Linking number** Lk₁₂ of strand 1's lines with strand 2's lines (strand 3 gives identical values) is the Gauss double integral, evaluated exactly for straight segments (signed solid-angle formula of Klenin and Langowski). It was tested on analytic polygonal curves: a Hopf link gives −1.0000000 / +1.0000000 depending on orientation, and a distant pair gives 0.
4. **Winding around the z-axis**, W_z, is the sum of azimuth increments along each line. It is a second, non-degenerate topological label: a Hopf loop has W_z = 0, and a ring around the axis has ±1.

The Hopf charge itself was not computed separately. With no vortex lines in the final state it is zero, and in the intermediate states it equals the linking number where that is defined.

## 6. Files committed

- `REPORT_N1.md` (this file).
- `N1_A_N49_R6.json`: history of the pre-registered run (`run_N1.py`, every 100 iterations); `log_A_N49.txt`: its console output.
- `trace_N1_A_N49_R6.json`, `log_trace_A_N49.txt`: fine-grained history of the identical diagnostic re-run.
- `N1_A_N49_R6_final.npz` (6.4 MB, under the 50 MB limit): final fields of start A.
- `linking.py`, `trace_N1.py`: the diagnostic scripts.
- Not committed: `N1_A_N49_R6_ckpt.npz` (the iteration-100 checkpoint, already vacuum) and the intermediate fields saved by the trace in `/tmp`. Both can be regenerated by the commands above.

## 7. Deviations from the plan, collected

1. Start B was not run, because the scripted start contradicts §9 and is unlinked (§3).
2. The 65³ box check was not run, because the plan's condition (no COLLAPSE at 49³) is not met.
3. Two diagnostic scripts were added (`linking.py`, `trace_N1.py`). They change nothing in the model or the minimization.
4. The grids are 49³ and 65³, not the 48³ and 64³ named in §9: odd sizes put a site plane at z = 0, as adopted in the control before any N = 1 run. This was inherited, not changed here.
5. SciPy had to be installed in the container.

No parameter was re-tuned and no term was added to the energy.
