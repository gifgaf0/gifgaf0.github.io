# E9 N = 1 at the remaining pre-registered (κ, η): report

October 31, 2026. Label: Exploration. This report completes the 2 × 2 grid of `PREREG.md` §1 and §6: κ ∈ {2, 1}, η ∈ {0.1, 0}. The (κ = 2, η = 0.1) cell is the rerun of `REPORT_N1_rerun.md`, carried over unchanged. The three new cells are (κ = 2, η = 0), (κ = 1, η = 0.1) and (κ = 1, η = 0). Each was run from both Amendment B starts at 65³. Everything else is as fixed in §9 and §10: the energy of `gl3.py`, the starts of `starts.py`, h = 0.5, R0 = 6, open boundaries, L-BFGS-B with gtol = 10⁻⁵ and MAXITER = 4000, and a record every 2 iterations. No other value was tried.

**Units.** All outputs are model units. Lengths are in the coordinate units of `gl3.py`, where ξ = 1/√2 for every e and η used here, so a length ℓ is ℓ·√2 in units of ξ. The §9 core-scale threshold, 2ξ, is 1.41 coordinate units. Energies are measured above the true vacuum, |ψ_k|² = 1 + η, which is |ψ_k|² = 1 at η = 0. No physical identification of the loop is made or implied.

## 0. The value of e used for κ = 1

PREREG §9 defines the normalization: ξ = 1/√2 and λ = 1/(e√6). So κ = λ/ξ = √2/(e√6) = 1/(e√3), and e = 1/(κ√3).

- κ = 2: e = 1/√12 = 0.288675… This is the default in `gl3.py`, and §9 states it explicitly.
- **κ = 1: e = 1/√3 = 0.577350…** This gives λ = 1/(e√6) = 1/√2 = ξ.

The task brief suggested e = 1/√6. Under §9's definition that gives λ = 1 and κ = √2, not 1, so I did not use it. The brief's guess λ = ξ·1 = 1/√2 agrees with e = 1/√3. The runs pass e as `repr(1/math.sqrt(3))` and `repr(1/math.sqrt(12))`.

§1 writes λ = 1/(e√3) with ξ = 1. That is the same κ = 1/(e√3), written in the units where ξ = 1, so §1 and §9 agree on e for a given κ.

## Summary

All eight runs (4 combinations × 2 starts) are **COLLAPSE** by §9. Every one ends in the uniform vacuum with zero vortex segments in all three strands, so Lk = 0 and the Hopf charge is zero. None shows a finite stopping radius.

| κ | e | η | Start | Verdict (§9) | Mechanism (§10 rule) | Strand 1 first within one grid spacing of the composite (it) | Composite R at that point | Link state afterwards | Last record with any vortex line (it) | Iterations | Final E above vacuum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 1/√12 | 0.1 | A | **COLLAPSE** | Reconnection, not §10 | 19 (sep. 0.35 / mean 1.33) | 2.39 | Lk = 0 at 20 | 26 | 112 | 1.0 × 10⁻⁶ |
| 2 | 1/√12 | 0.1 | B | **COLLAPSE** | §10 merge | 12 (0.35 / 0.65); 0 from 15 | 4.11 | unresolved (curves coincide) | 35 | 119 | 8.6 × 10⁻⁷ |
| 2 | 1/√12 | 0 | A | **COLLAPSE** | Reconnection, not §10 | 14 (0.35 / 3.42) | 3.30 | Lk = 0 at 18 | 26 | 314 | 1.0 × 10⁻⁵ |
| 2 | 1/√12 | 0 | B | **COLLAPSE** | §10 merge | 18 (0.35 / 0.71); 0 from 20 | 3.44 | unresolved (curves coincide) | 32 | 264 | 1.1 × 10⁻⁵ |
| 1 | 1/√3 | 0.1 | A | **COLLAPSE** | §10 merge (after strand 1's loop swings around the ring) | 18 (0.35 / 1.33); 0 from 22 | 3.63 | unresolved (curves coincide) | 38 | 124 | 3.8 × 10⁻⁷ |
| 1 | 1/√3 | 0.1 | B | **COLLAPSE** | §10 merge | 12 (0.00 / 0.49) | 5.10 | unresolved (curves coincide) | 44 | 122 | 7.1 × 10⁻⁷ |
| 1 | 1/√3 | 0 | A | **COLLAPSE** | Reconnection, not §10 | 20 (0.35 / 2.58) | 3.30 | Lk = 0 at 22 | 32 | 275 | 5.4 × 10⁻⁶ |
| 1 | 1/√3 | 0 | B | **COLLAPSE** | §10 merge | 14 (0.35 / 0.62); 0 from 16 | 4.89 | unresolved (curves coincide) | 44 | 265 | 7.3 × 10⁻⁶ |

Column notes. "Sep." is the min / mean distance from strand 1's line to the composite line, as in `REPORT_N1_rerun.md`. One grid spacing is h = 0.5. R is the mean distance of composite-line points from the z-axis. The two (κ = 2, η = 0.1) rows come from `REPORT_N1_rerun.md` and its every-iteration diagnostic, so they are resolved to 1 iteration. The six new rows are resolved to the recording interval of 2 iterations. The box check at 81³ was not run for any cell, because §10 runs it only for a start that does not collapse.

**§6 fallback condition: met.** §6 reads "If COLLAPSE at both κ values and both η values: option 4 (… a vorton). That is a separate pre-registration." All four (κ, η) cells are COLLAPSE, from both starts. Under §6 the next step is the time-dependent vorton (option 4), under a new pre-registration. This report does not start it. Under §5, no further (κ, η) values are to be tried within step 3.

## 1. Commands run

```
cd seed/experiments/E9_three_strand_closure
pip install scipy                         # not present in the container (deviation 1)
python3 gl3.py                            # gradient check at the default e, eta
E1=$(python3 -c "import math;print(repr(1/math.sqrt(3)))")     # kappa = 1
E2=$(python3 -c "import math;print(repr(1/math.sqrt(12)))")    # kappa = 2
python3 trace_N1.py A 65 6 4000 2 --e $E2 --eta 0   > log_trace_A_N65_k2_eta0.txt
python3 trace_N1.py B 65 6 4000 2 --e $E2 --eta 0   > log_trace_B_N65_k2_eta0.txt
python3 trace_N1.py A 65 6 4000 2 --e $E1 --eta 0.1 > log_trace_A_N65_k1_eta0.1.txt
python3 trace_N1.py B 65 6 4000 2 --e $E1 --eta 0.1 > log_trace_B_N65_k1_eta0.1.txt
python3 trace_N1.py A 65 6 4000 2 --e $E1 --eta 0   > log_trace_A_N65_k1_eta0.txt
python3 trace_N1.py B 65 6 4000 2 --e $E1 --eta 0   > log_trace_B_N65_k1_eta0.txt
```

Regression check (deviation 3): in a scratch copy of the four scripts, `python3 trace_N1.py A 65 6 4000 2` with no flags.

## 2. Software, hardware, checks

- Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (installed with pip). Linux container, 4 cores.
- **The change to `trace_N1.py` (deviation 2).** The script hard-coded `GL3(N=N, h=0.5, eta=0.1)` and used gl3.py's default e. I added two optional flags, `--e` and `--eta`, which default to exactly those values (1/√12 and 0.1). The flags are passed to `GL3(N=N, h=0.5, e=..., eta=...)`. For non-default values the output name gets a suffix `_k<κ>_eta<η>`, so that the official (κ = 2, η = 0.1) histories cannot be overwritten. The output JSON now also records e, η and κ. Nothing else in the script changed: same start, same diagnostics, same minimizer call. `gl3.py`, `starts.py` and `linking.py` are unchanged.
- **Regression check.** The modified script with no flags reproduces the official `trace_N1_A_N65_R6.json` exactly: 57 of 57 records, maximum |ΔE| = 0.0, identical segment counts and Lk at every record, and the same final E (1.0427829693071544 × 10⁻⁶).
- **Gradient checks.** `python3 gl3.py`: worst relative error 2.09 × 10⁻⁷ (default e, η). The same `check_grad` with GL3 constructed at the new parameters gave 3.63 × 10⁻⁷ (e = 1/√3, η = 0), 3.63 × 10⁻⁷ (e = 1/√3, η = 0.1) and 1.65 × 10⁻⁷ (e = 1/√12, η = 0). `gl3.py` itself was not edited for this.
- **Start check.** Each run's iteration-0 record gives Lk12 = Lk13 = −1.000 for both starts at all (κ, η). The start fields do not depend on e or η, because A = 0 initially and the amplitude profile is fixed. The wall gap of strand 1's line at iteration 0 is 3.75 (A) and 7.75 (B), as in §10.
- **Convergence.** All six new runs stopped on `CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL`. Run times were 220–400 s each, run 4 + 1 concurrently and then 2 concurrently. The η = 0 runs take about 2.5 times as many iterations (264–314, against 122–124 at η = 0.1), and they end at about 10⁻⁵ above vacuum instead of about 10⁻⁶. All of those extra iterations come after the last vortex line has gone: the energy relaxes slowly in the vortex-free tail. At η = 0 the relative phases have no restoring force, which is the likely reason. This affects no verdict.
- **Common checks across all six new runs.** There are no open ends on any line at any record. The minimum wall gap over the whole run is the iteration-0 value (3.75 for A, 7.75 for B), so no line comes closer to the box than it started, and the 49³ wall artefact of `REPORT_N1.md` does not occur. The energy decreases at every record. The composite radius decreases at every record, except for one uptick of 0.064 (κ = 1, η = 0.1, B, iteration 8 → 10) and one of 0.008 (κ = 2, η = 0, B, same iterations). Both are well below one grid spacing.
- **Strands 2 and 3 coincide** at every record of every run, including η = 0: their line records are identical. This is exact symmetry, not dynamics. The two fields start identical, and the energy is symmetric under exchanging them, so the deterministic minimizer keeps them identical. At η = 0 the composite is therefore not tested for splitting into its 2 and 3 strands. Only strand 1 is free to separate.

## 3. The new cells, run by run

The (κ = 2, η = 0.1) cell is described in `REPORT_N1_rerun.md` §3–§4. In the tables below, "it" is the L-BFGS iteration, R is the mean distance of line points from the z-axis, and "sep" is the min / mean distance from strand 1's line to the composite line.

### 3.1 κ = 2, η = 0

**Start A.**

| it | E | R comp. | R line 1 | z_rms line 1 | length line 1 | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|
| 0 | 1747.4 | 5.92 | 6.15 | 4.18 | 48 | 5.49 / 5.76 | −1.000 |
| 8 | 885.3 | 3.83 | 6.01 | 2.61 | 31 | 1.54 / 3.94 | −1.000 |
| 12 | 778.6 | 3.73 | 6.01 | 2.36 | 27 | 1.06 / 3.63 | −1.000 |
| 14 | 716.3 | 3.30 | 6.01 | 1.96 | 23 | **0.35** / 3.42 | −0.500 (contact) |
| 16 | 656.1 | 3.13 | 6.01 | 1.84 | 23 | 0.35 / 3.31 | −0.500 (contact) |
| 18 | 579.5 | 2.66 | 5.90 | 1.28 | 16 | 1.50 / 3.39 | 0.000 |
| 20 | 485.8 | 2.34 | 5.79 | 0.96 | 13 | 2.00 / 3.64 | 0.000 |
| 22 | 401.1 | 1.57 | — | — | 0 | — | 0 (no line 1) |
| 26 | 203.7 | 0.42 | — | — | 0 | — | 0 |
| 28 | 129.7 | — | — | — | 0 | — | 0 (no lines) |
| 314 (final) | 1.0 × 10⁻⁵ | — | — | — | 0 | — | 0 |

The composite ring shrinks while the link is intact (R 5.92 → 3.73 by iteration 12). Strand 1's loop stays centred near x = 6 and flattens. At iterations 14–16 it touches the composite at one place only, while its mean separation is still above 3. At iteration 18 the link is gone (Lk = 0, separation 1.50). Strand 1's loop then shrinks away (gone by iteration 22), and the untwisted composite ring collapses from R = 2.66 through 0.42 to nothing by iteration 28. **COLLAPSE.** The mechanism is **not** the §10 merge. It is the same point reconnection as (κ = 2, η = 0.1) start A: strand 1's loop cuts through the composite core at one place, which removes the link. The ring then collapses as in the N = 0 control.

**Start B.**

| it | E | R comp. | R line 1 | z_rms line 1 | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|
| 0 | 1793.9 | 5.92 | 6.31 | 1.36 | 1.46 / 1.95 | −1.000 |
| 8 | 806.3 | 4.03 | 4.39 | 0.87 | 0.71 / 1.31 | −1.000 |
| 16 | 649.4 | 3.63 | 4.02 | 0.60 | 0.50 / 0.94 | −1.000 |
| 18 | 609.9 | 3.44 | 3.74 | 0.54 | **0.35** / 0.71 | −0.750 (contact) |
| 20 | 575.3 | 3.27 | 3.55 | 0.44 | 0.00 / 0.56 | −0.500 (unresolved) |
| 22 | 530.8 | 2.86 | 3.21 | 0.25 | 0.00 / 0.31 | 0.000 (unresolved) |
| 26 | 431.8 | 2.30 | 2.65 | 0.24 | 0.00 / 0.34 | 0.000 (unresolved) |
| 30 | 280.8 | 1.48 | 1.67 | 0.23 | 0.00 / 0.41 | −0.625 (unresolved) |
| 32 | 197.7 | 1.09 | 1.14 | 0.24 | 0.00 / 0.57 | −0.375 (unresolved) |
| 34 | 110.1 | — | — | — | — | 0 (no lines) |
| 264 (final) | 1.1 × 10⁻⁵ | — | — | — | — | 0 |

Strand 1's helix closes in on the composite. It falls below one grid spacing at iteration 18 and is at zero from iteration 20. From then on it rides the core: z_rms locks at about 0.24, W_z stays 1, and the mean separation is ≤ 0.57. The merged object shrinks through R = 1.09 (1.5ξ) and is gone by iteration 34. **COLLAPSE**, by the **§10 mechanism** (merge onto the core, then shrinkage). As in the η = 0.1 rerun, the composite was already shrinking before the merge (5.92 → 3.44).

### 3.2 κ = 1, η = 0.1

**Start A.**

| it | E | R comp. | R line 1 | z_rms line 1 | rxy_min line 1 | W_z(1) | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 | 6.15 | 4.18 | 0.35 | 0 | 5.49 / 5.76 | −1.000 |
| 8 | 1252.0 | 4.72 | 5.49 | 2.93 | — | 0 | 3.26 / 4.06 | −1.000 |
| 12 | 993.8 | 4.26 | 4.79 | 2.12 | 0.25 | 0 | 1.97 / 3.07 | −1.000 |
| 14 | 847.8 | 4.04 | 4.42 | 1.69 | 0.56 | 0 | 1.17 / 2.40 | −1.000 |
| 16 | 735.3 | 3.98 | 4.32 | 1.45 | 0.25 | **1** | 0.87 / 2.17 | −1.000 |
| 18 | 620.5 | 3.63 | 3.87 | 0.95 | 0.90 | 1 | **0.35** / 1.33 | −0.875 (contact) |
| 22 | 472.1 | 3.24 | 3.29 | 0.53 | — | 1 | 0.00 / 0.55 | −0.250 (unresolved) |
| 26 | 384.4 | 2.83 | 2.85 | 0.49 | — | 1 | 0.00 / 0.01 | −0.375 (unresolved) |
| 30 | 328.9 | 2.44 | 2.42 | 0.46 | — | 1 | 0.00 / 0.24 | 0.250 (unresolved) |
| 34 | 255.7 | 1.70 | 1.77 | 0.24 | — | 1 | 0.00 / 0.09 | 0.125 (unresolved) |
| 38 | 144.0 | 1.18 | 1.18 | 0.23 | — | 0 | 0.00 / 0.10 | 0.125 (unresolved) |
| 40 | 75.1 | — | — | — | — | — | — | 0 (no lines) |
| 124 (final) | 3.8 × 10⁻⁷ | — | — | — | — | — | — | 0 |

This is the only run in which a start changes mechanism relative to κ = 2. Strand 1's Hopf loop starts with its inner side at the z-axis, since it is a circle of radius 6 centred at x = 6. Between iterations 14 and 16 that inner side sweeps across the axis (rxy_min 0.25). The loop's winding around the z-axis goes from 0 to 1 while Lk stays −1.000. After that, strand 1's loop goes once around the ring, as the start B helix does. It then closes onto the composite core: below one grid spacing at iteration 18, zero from iteration 22, and a mean separation of 0.01–0.55 thereafter. Strand 1's radius tracks the composite radius to within 0.1. The merged object shrinks through R = 1.18 (1.7ξ) and is gone by iteration 40. **COLLAPSE**, by the **§10 mechanism**. The composite was shrinking throughout (5.92 → 3.63 before contact). W_z at iteration 38 reads 0 on a 14-segment line of radius 1.2 and is not meaningful at that size.

**Start B.**

| it | E | R comp. | R line 1 | z_rms line 1 | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 | 6.31 | 1.36 | 1.46 / 1.95 | −1.000 |
| 8 | 767.9 | 5.09 | 5.30 | 0.76 | 0.50 / 0.87 | −1.000 |
| 10 | 741.0 | 5.16 | 5.28 | 0.76 | 0.50 / 0.80 | −1.000 |
| 12 | 706.7 | 5.10 | 5.13 | 0.59 | **0.00** / 0.49 | −0.875 (unresolved) |
| 18 | 634.1 | 4.78 | 4.84 | 0.25 | 0.00 / 0.22 | 0.000 (unresolved) |
| 24 | 562.4 | 4.04 | 3.94 | 0.25 | 0.00 / 0.16 | 0.000 (unresolved) |
| 32 | 429.3 | 3.01 | 3.03 | 0.25 | 0.00 / 0.05 | 0.000 (unresolved) |
| 40 | 266.2 | 1.84 | 1.91 | 0.24 | 0.00 / 0.05 | −0.125 (unresolved) |
| 44 | 166.6 | 1.24 | 1.31 | 0.22 | 0.00 / 0.37 | −0.250 (unresolved) |
| 46 | 110.1 | — | — | — | — | 0 (no lines) |
| 122 (final) | 7.1 × 10⁻⁷ | — | — | — | — | 0 |

The helix merges onto the core at iteration 12, at a larger radius than in any other run (R = 5.10). The merged object then shrinks steadily, through R = 1.24 (1.8ξ) at iteration 44, and is gone by iteration 46. **COLLAPSE**, by the **§10 mechanism**. Iterations 8–10 are the closest thing to a pause in any run: the composite radius moves 5.09 → 5.16 → 5.10. That is a change of one-eighth of a grid spacing, during which the energy keeps falling (767.9 → 741.0 → 706.7), and the shrinkage resumes at once after the merge.

### 3.3 κ = 1, η = 0

**Start A.**

| it | E | R comp. | R line 1 | z_rms line 1 | length line 1 | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|---|
| 0 | 1747.4 | 5.92 | 6.15 | 4.18 | 48 | 5.49 / 5.76 | −1.000 |
| 8 | 895.6 | 4.83 | 6.01 | 3.18 | 39 | 3.10 / 4.50 | −1.000 |
| 16 | 697.5 | 4.05 | 6.02 | 2.19 | 27 | 1.54 / 3.28 | −1.000 |
| 18 | 626.0 | 3.64 | 5.84 | 1.81 | 24 | 0.61 / 2.97 | −1.000 |
| 20 | 543.1 | 3.30 | 5.78 | 1.41 | 20 | **0.35** / 2.58 | −0.625 (contact) |
| 22 | 470.6 | 2.89 | 5.76 | 0.91 | 12 | 1.00 / 2.61 | 0.000 |
| 24 | 371.2 | 2.44 | 5.75 | 0.48 | 8 | 2.00 / 3.02 | 0.000 |
| 26 | 310.5 | 2.20 | — | — | 0 | — | 0 (no line 1) |
| 30 | 198.1 | 1.46 | — | — | 0 | — | 0 |
| 32 | 139.6 | 0.74 | — | — | 0 | — | 0 |
| 34 | 86.5 | — | — | — | 0 | — | 0 (no lines) |
| 275 (final) | 5.4 × 10⁻⁶ | — | — | — | 0 | — | 0 |

This is the same history as (κ = 2, η = 0) start A, about 6 iterations later. Strand 1's loop stays near x = 6 and flattens. It touches the composite at one point (iteration 20, mean separation 2.58), and at iteration 22 it is unlinked. It then shrinks away. The untwisted composite, at R = 2.89 when the link was lost, collapses by iteration 34. **COLLAPSE.** The mechanism is a **reconnection, not the §10 merge**.

**Start B.**

| it | E | R comp. | R line 1 | z_rms line 1 | sep min / mean | Lk₁₂ |
|---|---|---|---|---|---|---|
| 0 | 1793.9 | 5.92 | 6.31 | 1.36 | 1.46 / 1.95 | −1.000 |
| 8 | 687.9 | 5.08 | 5.33 | 0.90 | 0.87 / 1.14 | −1.000 |
| 12 | 644.2 | 4.98 | 5.10 | 0.73 | 0.50 / 0.79 | −1.000 |
| 14 | 614.3 | 4.89 | 5.05 | 0.61 | **0.35** / 0.62 | −0.750 (contact) |
| 16 | 594.0 | 4.84 | 4.91 | 0.53 | 0.00 / 0.42 | −0.500 (unresolved) |
| 20 | 551.9 | 4.48 | 4.51 | 0.25 | 0.00 / 0.13 | −0.625 (unresolved) |
| 30 | 410.3 | 3.23 | 3.24 | 0.25 | 0.00 / 0.24 | 0.000 (unresolved) |
| 40 | 229.5 | 1.75 | 1.79 | 0.24 | 0.00 / 0.07 | 0.250 (unresolved) |
| 44 | 114.0 | 0.83 | 0.94 | 0.23 | 0.00 / 0.12 | −0.125 (unresolved) |
| 46 | 67.0 | — | — | — | — | 0 (no lines) |
| 265 (final) | 7.3 × 10⁻⁶ | — | — | — | — | 0 |

The helix merges onto the core at iteration 14–16 (R ≈ 4.9). The merged object shrinks through R = 0.83 and is gone by iteration 46. **COLLAPSE**, by the **§10 mechanism**.

## 4. Pattern across the grid

- **No cell stabilizes.** In all eight runs the composite radius falls at every record (apart from the two sub-grid upticks noted in §2), the energy falls at every record, and the end state is the vacuum. Neither κ nor η produces a plateau.
- **Mechanism by start.** Start B (the §9 helix) merges onto the core in all four cells. That is the §10 mechanism. Start A (the Hopf-linked circle) unlinks by a single-point reconnection in three cells: (2, 0.1), (2, 0) and (1, 0). In the fourth, (1, 0.1), its loop first swings round to wrap the ring and then merges, so it ends by the §10 mechanism. The two starts reach the same intermediate state only in the (1, 0.1) cell.
- **η = 0 versus 0.1.** Without the Josephson term the Hopf loop of start A stays further from the core: its mean separation is still 2.6–3.4 at contact, against 1.3 at η = 0.1. With η = 0.1 at κ = 1, the loop is pulled onto the core. This is the qualitative role §9 expected η to play ("the string of step 2 should pull strand 1's loop onto a helix"). It does happen, but the helix then merges and shrinks instead of holding the ring open.
- **κ = 1 versus 2.** At κ = 1 the merged object survives a few iterations longer (lines gone by iteration 40–46, against 26–36 at κ = 2), and the merge in start B happens at a larger radius. The order of events and the outcome do not change.
- **The composite is always shrinking before strand 1 reaches it,** whether strand 1 then merges or reconnects. Across all eight runs, the twisted state never held the ring at any radius while the link was intact.

## 5. Caveats

- The L-BFGS iterations are a minimizer path, not a time evolution. The histories show that the energy landscape runs downhill from each start to the vacuum. They do not show a physical trajectory.
- Statements at the level of one grid spacing (h = 0.5 = 0.71ξ) are resolution-limited. The six new runs record every 2 iterations, so event iterations are ±1. No every-iteration diagnostic was run for them, because no verdict depends on the exact iteration.
- Once the lattice curves coincide, the linking number of strand 1 with the composite is undefined, as in `REPORT_N1.md` §4. For the merge runs I therefore cannot say whether the link was undone before the lines vanished. It is −1 before contact and 0 at the end.
- The final-state claims rest on line detection (zero segments in every strand) and on the energy above vacuum (≤ 1.1 × 10⁻⁵, from 1747–2895 at the start). No field files were saved, as in the rerun.
- The 2 ↔ 3 symmetry (§2) means η = 0 tests only strand 1's freedom, not a splitting of the composite.

## 6. Files committed

- `REPORT_N1_kappa_eta.md` (this file).
- `trace_N1.py`: optional `--e` and `--eta` flags only (deviation 2).
- `trace_N1_{A,B}_N65_R6_k2_eta0.json`, `trace_N1_{A,B}_N65_R6_k1_eta0.1.json` and `trace_N1_{A,B}_N65_R6_k1_eta0.json`: the six run histories (every 2 iterations, plus the final record, with e, η and κ stored).
- `log_trace_{A,B}_N65_k2_eta0.txt`, `log_trace_{A,B}_N65_k1_eta0.1.txt` and `log_trace_{A,B}_N65_k1_eta0.txt`: their console output.
- The regression-check output was written in a scratch directory and is not committed. It is byte-for-byte the same history as the committed `trace_N1_A_N65_R6.json`.

## 7. Deviations, collected

1. **SciPy installed with pip.** It was not present in the container.
2. **`trace_N1.py` gained `--e` and `--eta` flags.** The task was to vary only κ and η, and to pass e and η on the command line rather than edit `gl3.py`. The script had η hard-coded and no way to set e, so this was the minimal change. The defaults reproduce the previous behaviour exactly (deviation 3).
3. **Regression run.** One extra run of (κ = 2, η = 0.1) start A, with the modified script and no flags, in a scratch directory. It reproduces the official history exactly.
4. **Concurrency.** Four new runs and the regression run ran concurrently, then the remaining two. L-BFGS-B is deterministic, and the regression run shows that concurrency does not change the path.
5. **The 81³ box check was not run** for any cell. Its §10 condition (a start that does not collapse) is never met.

No value of κ or η other than the four pre-registered combinations was run. No term was added to the energy, and `gl3.py`, `starts.py` and `linking.py` are unchanged.
