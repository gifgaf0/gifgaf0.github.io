# E9 N = 1 rerun under Amendment B (P2): report

October 31, 2026. Label: Exploration. The model, parameters, starts and verdict rules are those fixed in `PREREG.md` §9 (Amendment A) and §10 (Amendment B): κ = 2 (e = 1/√12), η = 0.1, h = 0.5, R0 = 6, open boundaries, 65³ grid (box half-width 16). The energy is exactly as in `gl3.py`, and the starts are as in `starts.py`. Nothing in the model, the parameters, the starts or the scripts was changed.

**Units.** All outputs are model units. Lengths are in the coordinate units of `gl3.py`, where ξ = 1/√2, so a length ℓ is ℓ·√2 in units of ξ. The core-scale threshold of §9, 2ξ, is 1.41 coordinate units. Energies are measured above the true vacuum (|ψ_k|² = 1 + η). No physical identification of the loop is made or implied.

## Summary

| Start | Grid | Verdict (§9) | Mechanism (§10 rule) |
|---|---|---|---|
| A (Hopf-linked circle) | 65³ | **COLLAPSE** | Not the §10 mechanism. Strand 1's loop contracts and cuts through the composite core at a single point (iteration 19), which unlinks it (a reconnection). It then vanishes (iteration 21). The composite ring, now untwisted, shrinks to zero like the N = 0 control (iteration 27). |
| B (§9 (1,1) helix) | 65³ | **COLLAPSE** | The §10 mechanism. Strand 1's line merges onto the composite core: its closest approach falls below one grid spacing at iteration 12 and reaches 0 at iteration 15. The merged object then shrinks to zero (iterations 35–36). |
| Box check | 81³ | **Not run** | §10 runs it only if a start does not collapse. Both collapse. |

Both starts end in the uniform vacuum with no vortex lines, so Lk = 0 and the Hopf charge is zero. No finite R* exists from either start. **P2 is answered COLLAPSE** at κ = 2, η = 0.1, which is the outcome the pre-run prior gave about 60 %.

## 1. Commands run

```
cd seed/experiments/E9_three_strand_closure
pip install scipy                                   # not present in the container (deviation 1)
python3 gl3.py                                      # gradient check
python3 -c "from gl3 import GL3; from starts import start_fields; from linking import analyse; g=GL3(N=65); print([analyse(start_fields(g,s,6.0)) for s in 'AB'])"
python3 trace_N1.py A 65 6 4000 2 > log_trace_A_N65.txt
python3 trace_N1.py B 65 6 4000 2 > log_trace_B_N65.txt
```

The two trace runs ran concurrently. Afterwards I added a diagnostic (deviation 2). It is the same script with the same arguments except MAXITER = 40 and EVERY = 1, run on copies of the four scripts in a scratch directory so that it could not overwrite the official outputs:

```
python3 trace_N1.py A 65 6 40 1
python3 trace_N1.py B 65 6 40 1
```

## 2. Software, hardware, checks

- Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (installed with pip). Linux container, 4 cores, 15 GB RAM.
- **Gradient check:** `gradient check, worst relative error: 2.0925355138465372e-07`. This is the expected ~2 × 10⁻⁷.
- **Start check:** `[{'nseg': [96, 96, 96], 'Lk12': -1.0, 'Lk13': -1.0, 'Lk23': 0.0}, {'nseg': [114, 96, 96], 'Lk12': -1.0000000000000004, 'Lk13': -1.0000000000000004, 'Lk23': 0.0}]`. So |Lk12| = |Lk13| = 1 for both starts, as required. The sign is an orientation convention, and §10 states |Lk|. At iteration 0 the wall gap of strand 1's line is 3.75 (A) and 7.75 (B), matching §10.
- **Run times:** A converged in 112 iterations and 106 s; B converged in 119 iterations and 107 s. Both stopped on `CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL`.
- **Final energies above vacuum:** 1.04 × 10⁻⁶ (A) and 8.61 × 10⁻⁷ (B). Both final states have zero vortex segments in all three strands.
- **Determinism:** the 40-iteration diagnostic re-runs reproduce the official histories exactly at every common iteration: same E (difference 0.0), same segment counts and same Lk. L-BFGS-B is deterministic, so the every-iteration records below are the histories of the official runs.

## 3. Start A (Hopf-linked circle), 65³

Column meanings are as in `REPORT_N1.md` §4. "comp." is the composite line (strands 2 and 3, which coincide throughout). R is the mean distance of line points from the z-axis. "sep" is the min / mean distance from strand 1's line to the composite line. Rows from iteration 15 on come from the every-iteration diagnostic.

| it | E | R comp. | length comp. | R line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 | 48 | 6.15 | 4.18 | 48 | 3.75 | 0 | 0 | 5.49 / 5.76 | −1.000 |
| 4 | 1763.2 | 5.22 | 43 | 5.80 | 3.45 | 40 | 5.25 | 0 | 0 | 4.29 / 4.88 | −1.000 |
| 8 | 1220.7 | 4.25 | 36 | 5.27 | 2.61 | 34 | 6.75 | 0 | 0 | 2.62 / 3.55 | −1.000 |
| 12 | 940.2 | 3.57 | 29 | 5.09 | 1.92 | 27 | 7.75 | 0 | 0 | 1.62 / 2.80 | −1.000 |
| 16 | 728.0 | 3.03 | 25 | 4.77 | 1.26 | 20 | 8.75 | 0 | 0 | 0.94 / 2.07 | −1.000 |
| 17 | 663.1 | 2.85 | 24 | 4.60 | 1.08 | 19 | — | 0 | 0 | 0.61 / 1.81 | −1.000 |
| 18 | 617.6 | 2.68 | 21 | 4.57 | 0.90 | 17 | 9.25 | 0 | 0 | 0.50 / 1.83 | −1.000 |
| 19 | 560.0 | 2.39 | 20 | 4.36 | 0.54 | 10 | — | 0 | 0 | **0.35** / 1.33 | −0.250 (contact) |
| 20 | 498.1 | 2.27 | 20 | 4.51 | 0.22 | 5 | 10.75 | 0 | 0 | 0.50 / 1.27 | 0.000 |
| 21 | 453.0 | 2.10 | 17 | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 23 | 344.6 | 1.54 | 12 | — | — | 0 | — | — | — | — | 0 |
| 26 | 215.2 | 0.84 | 7 | — | — | 0 | — | — | — | — | 0 |
| 27 | 163.6 | — | 0 | — | — | 0 | — | — | — | — | 0 (no lines) |
| 112 (final) | 1.0 × 10⁻⁶ | — | 0 | — | — | 0 | — | — | — | — | 0 |

(A "—" in the wall-gap column of this table and the next means the value was not copied in. It is in the `*_every1_it40.json` file.)

**What happened.**
1. **No wall contact.** Strand 1's wall gap grows from 3.75 to 10.75, there are never any open ends, and the winding around the z-axis stays W_z = 0 throughout. The boundary artefact of the 49³ run (`REPORT_N1.md` §4, caveat 1) does not occur.
2. **Shrinking while linked.** From iteration 0 to 18 the link is intact (Lk = −1.000 exactly). Over that stretch the composite ring shrinks monotonically, from R = 5.92 to 2.68, and strand 1's loop shortens from 48 to 17. The energy falls monotonically. The twist does not stop the shrinkage at any radius while the link exists.
3. **Unlinking.** At iteration 19 strand 1's line comes within 0.35 (< h = 0.5) of the composite line at one place only (mean separation 1.33). The Gauss sum is non-integer there, which is the signature of touching segments. At iteration 20 the link is gone (Lk = 0.000, separation back to 0.50). What is left of strand 1 is a small flat loop (length 5, z_rms 0.22) lying outside the composite ring. This is a single-point crossing of strand 1's loop through the composite core, i.e. a reconnection. It is not a merge along the core.
4. **Collapse.** Strand 1's loop vanishes at iteration 21. The composite ring was at R = 2.27 (3.2ξ) when the link was lost. It then shrinks on its own, untwisted: 2.10 → 1.54 → 0.84, and it is gone at iteration 27. The energy decays to the vacuum.

**Verdict by §9: COLLAPSE.** Both clauses of §9 are met: strand 1's loop unlinks by reconnection, and the ring then shrinks to core scale and vanishes.

**§10 interpretation rule.** The §10 mechanism (strand 1 merges onto the core, then the configuration shrinks) is **not** what happened in start A. Strand 1's line never lies along the composite core. Its closest approach falls below one grid spacing only at iteration 19, at one point, with a mean separation above 1. The mechanism is different: **strand 1's Hopf loop contracts under its own line tension and cuts through the composite core (a reconnection), which removes the link. The remaining untwisted composite ring then collapses as in the N = 0 control.** Both rings were already shrinking before the reconnection, so the link did not hold the configuration open at any size.

## 4. Start B (§9 (1,1) helix of minor radius 2), 65³

| it | E | R comp. | length comp. | R line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 | 48 | 6.31 | 1.36 | 57 | 7.75 | 0 | 1 | 1.46 / 1.95 | −1.000 |
| 4 | 1339.6 | 5.30 | 43 | 5.55 | 1.17 | 52 | 8.75 | 0 | 1 | 1.17 / 1.50 | −1.000 |
| 8 | 938.1 | 4.52 | 38 | 4.78 | 0.78 | 43 | 9.75 | 0 | 1 | 0.50 / 1.01 | −1.000 |
| 11 | 834.9 | 4.27 | 35 | 4.48 | 0.58 | 38 | — | 0 | 1 | 0.50 / 0.76 | −1.000 |
| 12 | 806.2 | 4.11 | 34 | 4.34 | 0.57 | 37 | 10.75 | 0 | 1 | **0.35** / 0.65 | −0.875 (contact) |
| 15 | 758.1 | 3.94 | 32 | 4.18 | 0.48 | 37 | — | 0 | 1 | **0.00** / 0.48 | 0.125 (unresolved) |
| 17 | 719.9 | 3.77 | 31 | 3.93 | 0.25 | 32 | — | 0 | 1 | 0.00 / 0.18 | −0.000 (unresolved) |
| 20 | 672.1 | 3.61 | 30 | 3.66 | 0.25 | 31 | 11.75 | 0 | 1 | 0.00 / 0.09 | 0.000 (unresolved) |
| 24 | 573.9 | 3.07 | 26 | 2.98 | 0.24 | 25 | 12.75 | 0 | 1 | 0.00 / 0.52 | −0.500 (unresolved) |
| 28 | 453.0 | 2.41 | 19 | 2.19 | 0.24 | 19 | 13.75 | 0 | 1 | 0.00 / 0.48 | 0.000 (unresolved) |
| 32 | 297.9 | 1.68 | 14 | 1.29 | 0.24 | 11 | 14.75 | 0 | 1 | 0.00 / 0.40 | 0.125 (unresolved) |
| 34 | 209.0 | 1.13 | 8 | 0.70 | 0.23 | 6 | 15.25 | 0 | 1 | 0.00 / 0.18 | 0.000 (unresolved) |
| 35 | 156.0 | 0.79 | 5 | — | — | 0 | — | — | — | — | 0 (no line 1) |
| 36 | 147.2 | — | 0 | — | — | 0 | — | — | — | — | 0 (no lines) |
| 119 (final) | 8.6 × 10⁻⁷ | — | 0 | — | — | 0 | — | — | — | — | 0 |

**What happened.**
1. **Approach.** From iteration 0 to 11 strand 1's helix is linked (Lk = −1.000) and winds once around the z-axis (W_z = 1). The helix closes in on the composite core: the mean separation falls from 1.95 to 0.76, and z_rms from 1.36 to 0.58. The composite ring shrinks over the same stretch, from R = 5.92 to 4.27.
2. **Merge.** At iteration 12 the closest approach falls below one grid spacing (0.35 < h). From iteration 15 on it is 0, and the mean separation stays at 0.09–0.54 (≤ about one grid spacing) until the end. Strand 1's radius tracks the composite radius to within about 0.4, and its z_rms locks at 0.24. Strand 1 has merged onto the composite core. W_z stays 1 throughout, so strand 1's line remains a closed loop going once around the ring with it.
3. **Shrinking after the merge.** The merged object shrinks monotonically, from R ≈ 4.1 to 0.7, and the energy falls monotonically. Strand 1's line vanishes at iteration 35 and the composite at 36. The energy then decays to the vacuum.
4. **When the link is lost is not resolved.** From iteration 12 onward the two lattice curves touch, and the Gauss sum gives non-integer values (−0.875, −0.75, 0.125, −0.5, …). As in `REPORT_N1.md` §4 caveat 2, the linking number of coincident lattice curves is not defined, so I cannot say whether the link was undone before the lines vanished. It was −1 at iteration 11 and is 0 at the end.

**Verdict by §9: COLLAPSE.** The ring shrinks to core scale: through R = 1.13 (1.6ξ) at iteration 34 to zero. No finite R* exists, and the end state is not linked.

**§10 interpretation rule.** This **is** the §10 mechanism. Strand 1's line merges onto the composite core (closest approach below one grid spacing from iteration 12, zero from iteration 15), and the configuration then shrinks to nothing. In the words of §10: the twist has no protected place to live where all three amplitudes vanish. One qualification is recorded: the composite ring was already shrinking before the merge (5.92 → 4.11), so the merge did not trigger the shrinkage. It removed the only thing that might have stopped it.

## 5. The two starts compared

The two starts do **not** reach the same intermediate state, which §9 hoped the second start would check. Start A unlinks by a point reconnection while strand 1's loop is still far from the core on average. Start B merges strand 1 along the core. They do reach the same final state, the vacuum, and the same verdict.

Neither start shows any sign of a finite stopping radius. Neither shows a plateau in E, and in both the composite radius decreases monotonically at every recorded iteration. The composite vanishes at iteration 27 (A) and 36 (B). For comparison, the N = 0 control at 49³ vanished within about 50 iterations (`REPORT_control.md`). Because the grids differ, this is a qualitative comparison only.

The 49³ start A of `REPORT_N1.md` merged onto the core (as start B does here) after its wall episode. At 65³, with no wall contact, start A instead unlinks by reconnection. This supports the caveat in `REPORT_N1.md` that the wall shaped the 49³ trajectory. Note also that the 49³ start was built with the old `ring_field` construction, not `starts.py`.

Caveats carried over from `REPORT_N1.md` §4:
- L-BFGS iterations are a minimizer path, not a time evolution, and steps can be large. The histories show that the energy landscape is downhill from each start to the vacuum. They do not show a physical trajectory.
- Statements at the level of one grid spacing (h = 0.5 = 0.71ξ) are resolution-limited.

## 6. Files committed

- `REPORT_N1_rerun.md` (this file).
- `trace_N1_A_N65_R6.json` and `trace_N1_B_N65_R6.json`: the official run histories (every 2 iterations, plus the final record). Their console output is in `log_trace_A_N65.txt` and `log_trace_B_N65.txt`.
- `trace_N1_A_N65_R6_every1_it40.json` and `trace_N1_B_N65_R6_every1_it40.json`: the every-iteration diagnostic for iterations 0–40 (deviation 2). They were renamed from the script's default output name so that they do not overwrite the official histories.
- No field files. `trace_N1.py` as called by the README saves no fields: the 6th argument, a save directory, was not given, and the script writes no final `.npz`. The final-state claims rest on the line detection (zero segments in every strand) and the energy above vacuum (~10⁻⁶). The per-site |ψ|² check done in `REPORT_N1.md` was not repeated.

## 7. Deviations, collected

1. **SciPy installed with pip.** SciPy was not present in the container, and `gl3.py` needs it.
2. **Extra diagnostic runs.** After the official runs I re-ran both starts with MAXITER = 40 and EVERY = 1, to resolve the iterations at which the link was lost. I used unchanged copies of the scripts in a scratch directory. Same model, same start, same minimizer call: only the iteration cap and the recording interval differ. The trajectory is identical to the official one wherever both recorded, so this changes no result. It was not in the README's run list.
3. **The two official runs ran concurrently** on the 4-core container. This does not affect the deterministic L-BFGS-B path. The diagnostic re-runs, also concurrent, reproduce it exactly.
4. **The 81³ box check was not run.** Its condition in §10 (a start that does not collapse) is not met.
5. **No final fields saved** (see §6).

No parameter was re-tuned: κ, η, h, R0 and the starts are as fixed. No term was added to the energy, and no script in the experiment directory was modified.
