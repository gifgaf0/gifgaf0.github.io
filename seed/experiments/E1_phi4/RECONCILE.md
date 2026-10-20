# E1 reconciliation: φ⁴ in 1+1 D

*October 19, 2026. The inputs were `REPORT.md` (the run agent's report), `crosscheck/CROSSCHECK.md` and `crosscheck.json` (verdict: confirmed with corrections), and both codes. The work list is the cross-check's four major and five minor issues.*

**Outcome.** Every issue is resolved except one calibration point, which stays OPEN because it is chaotic: DSV's example point (ω, v) = (0.99, 0.43). The cross-check was right on all four major issues. On the example point it was right that the call was not demonstrated, but not that the point fails to produce. Two further corrections turned up during this pass:

- the E1e DSV quanta count rested on an unconverged producer;
- the PLAN E1d speed prediction, on a decisive test, is refuted rather than merely unsupported.

## How this pass ran

- **Earlier interrupted attempt.** It had written `e1c_reconcile.py` (a fourth-order integrator for the DSV runs; four passes, 59 runs), `e1_timereversal.py`, `e1d_confound.py`, `e1c_reconcile_analysis.py`, `dsv_fig2_reading.json` and a draft `reconcile_results.py`. These were committed, but `results.json`, `seed_claims.json` and `REPORT.md` had not been changed. I reviewed them and kept them. The last two planned runs, at dx = 0.0125, had not been done.
- **New computations** (about 85 min on two cores):
  - The DSV (dx, dt) ladder was finished. Passes F and G were added to `e1c_reconcile.py`: a fourth-order ladder at v = 0.40 and 0.42, scans between grid points at 0.405–0.435, a resolution check of the hole (0.91, 0.80–0.83), and neighbourhood ensembles in the 0.41 and 0.43 cells. That makes 96 runs in all.
  - `e1d_speedtest.py` is a phase-averaged speed test at fixed packet shape, 3,402 runs. Its decision rule was fixed in the script before it ran.
  - `e1c_example_y4.py` makes the space-time figure `fig_e1c_example_y4.png`.
- **Bookkeeping.**
  - `e1c_reconcile_analysis.py` gained convergence classes and the ensemble summary.
  - `reconcile_results.py` was rewritten. It is idempotent, and it applies every change to `results.json` and `seed_claims.json`.
  - `run_all.sh` gained the new stages.
  - Nothing was committed. No file outside `seed/experiments/E1_phi4/` was touched.

## Issues

### M1. DSV example point (0.99, 0.43): CALIBRATED → OPEN

**Diagnosis.** There is no bug in either code. The point is chaotic. The trains leave a long-lived central oscillation, and whether it releases a pair is decided at t ≈ 830–870. By then any two affordable discretisations have separated:

- φ(0, t) of the two finest fourth-order runs differ by 4 × 10⁻³ at t = 800 and by order 1 at t = 850, and pass 0.1 at t = 831.
- With fourth-order time stepping there is no pair at (dx, dt) = (0.05, 0.02), (0.05, 0.01), (0.025, 0.01) or (0.025, 0.005). At (0.0125, 0.005) a pair forms at t = 870 and sits at ±128 at T; the cross-check read about ±140 in DSV Fig. 1.
- The original leapfrog produces at 4 of 11 distinct settings, including the cross-check's runs, at t = 780–1160.
- The cross-check's FD6 and spectral codes produce at 0 of 4.
- Inside DSV's 0.01-wide cell, 0 of 11 neighbouring initial data produce (v = 0.425–0.435, step 0.001; fourth order, dx = 0.05).

**Who was right.** The cross-check, that "CALIBRATED is not demonstrated" and that "the pair is real" generalised from one run. Its stronger reading, that the call "is a property of the (0.1, 0.04) discretisation", does not survive: the finest runs of both integrators produce.

**Converged neighbour.** (0.99, 0.41) forms its pair at t = 590 at all five fourth-order settings and in all three spectral runs, and the leapfrog converges to that as dt → 0. Around it, 3 of 11 initial data produce (0.407, 0.41, 0.411). v = 0.40 produces at 3 of 4 fourth-order settings. Production at ω = 0.99 is a sparse, fractured set near v ≈ 0.40–0.41.

**What the DSV calibration is.** CALIBRATED, and agreed by both codes:

- the band and its trend (Spearman −0.99 with the converged column; cross-check −0.94);
- high-v pass-through;
- no production above ω = 0.99;
- the hole at (0.91, 0.82). New in this pass: it makes no pair at four discretisations, while (0.91, 0.80) produces at all four and (0.91, 0.85) at the three where it was run. The extent of the hole varies.

**Not reproduced.** The point-level map: 58 of DSV's 81 producing points hit, 22 extra. Five of the original map's 14 lowest-energy producers are not reproduced with fourth-order stepping. The example point is OPEN: unresolvable at affordable resolution, with the reason stated.

**Action.**

- Calibration row → OPEN, with the full call table.
- A new row for the ω = 0.99 ladder.
- A new row for the point-by-point map comparison.
- The hole row now carries the resolution check.
- REPORT: the E1c section and table rewritten from the digitised DSV Fig. 2, "band by band" withdrawn, the dx-check caveat added, and the new figures added.

### M2. §4 "most easily at low speed": CONFIRMED → AMENDED

**Diagnosis.** DSV say that higher ω needs lower v and that fast trains pass through. Neither their map nor ours shows production that is easiest at low speed:

- at fixed ω nothing produces below the band (ω = 0.90: nothing for v < 0.73);
- the slow bands at high ω cost no less energy (lowest-energy converged producers at v = 0.59–0.79, E ≈ 7.8–8.2 × 2M; the ω = 0.99 producer at v = 0.41 needs 12.3 × 2M).

**Who was right.** The cross-check.

**Action.** Seed claim → AMENDED: pairs form over a wide range, in an ω-dependent velocity band that moves to lower v as the pulses weaken.

### M3. E1d low-speed preference: confounded; the PLAN prediction "favours low speed" → REFUTED

**Diagnosis.** At matched energy slow packets are taller (band [2, 4): mean A 0.85–0.90 at v_g ≤ 0.33 against 0.36 at v_g = 0.90), and amplitude controls production.

- **Stored grid** (`e1d_confound.py`). With A, or A and σ, held fixed there is no slow preference. Logistic v_g coefficient (z) given log A and log σ: +0.56 (1.9) baseline, +0.16 (0.6) one-way, −0.18 (−0.6) and −0.53 (−1.7) collision-needed.
- **Decisive test** (`e1d_speedtest.py`): A ∈ 0.5–1.0, σ ∈ {2, 4, 8}, nine speeds and 8 collision phases, in both φ_t forms, with single-packet controls. Logistic slope on v_g with one intercept per shape (95% CI; positive = faster produces more):
  - all production: +1.36 [0.80, 1.92] baseline, +0.62 [0.07, 1.16] one-way;
  - packets that do not fold on their own: +1.32 [0.53, 2.10] and +0.71 [−0.24, 1.67];
  - dx = 0.05 subset: +1.35 [0.44, 2.27].
- **Decision.** The pre-set rule says "not a speed effect" in both forms: every interval excludes −1.19, half the matched-energy effect.

**Who was right.** The cross-check. The new test goes further: at fixed shape, faster packets produce as much or more.

**Action.**

- Seed claims: the PLAN E1d prediction is split. "Favours low speed" → REFUTED. "Favours wide packets" → AMENDED (it was NOT SUPPORTED, which is not a PLAN word): wider wins at fixed amplitude (log σ z = 13.4), not at matched energy.
- results.json: the speed rows → REFUTED, the width rows → AMENDED, plus two new rows (stored-grid confound and decisive test).

### M4. §2 threshold: AMENDED → CONFIRMED

**Diagnosis.** The φ⁴ equation is time-reversal invariant. Reversing a slow captured kink–antikink pair gives kink-free initial data that make an escaping pair at E = 2Mγ(v) → 2M.

`e1_timereversal.py` demonstrates this on the lattice: at v = 0.05 the data have φ < 0 everywhere and E = 1.0012 × 2M (v = 0.1: 1.0050). They are tuned beyond 10⁻⁸: noise of that size, a halved time step, or truncating the far radiation each prevents the pair. DSV 2008 (p. 1) describe the same construction.

**Who was right.** The cross-check.

**What is and is not shown.**

- Shown: the floor (no production below 2M in any run, in any code), and that the infimum over all initial data is 2M, approached only by finely tuned data.
- Family-specific: the onsets 1.86, 2.70 and 7.81 × 2M, which are upper bounds for the Gaussian, one-way and DSV families.
- Withdrawn as a general statement: "a classical field needs extra energy".

**Action.** Seed claim → CONFIRMED. A new results row for the time-reversal demonstration, and notes on the lowest-energy rows.

### Minor issues

| # | Issue | Diagnosis | Action |
|---|---|---|---|
| 1 | CALIBRATED used for the energy-floor sanity check | Correct: it has no literature target | → CHECK PASSED. The internal dx = 0.05 slice check is also CHECK PASSED (was CONFIRMED) |
| 2 | Unconverged region, hole and switch counts used as headline numbers | Correct: the k = 2 line has 9 switches in one code and 17 in the other | Labelled illustrative. The report leads with the robust facts: non-monotonic lines with the same onset in both codes, stable fractions |
| 3 | Self-folding mechanism "not analysed" | Correct: a trough at φ = −1 − A is above the barrier V(0) = 1/4 when A > √2 − 1 = 0.414 (observed 0.375–0.425) | Estimate added. Collision-needed fractions per band added; below 4 × 2M all production needs the collision |
| 4 | DSV table simplified; "band by band" | Correct | Replaced by the digitised Fig. 2, with hits, extras and misses per ω. The wording is withdrawn |
| 5 | v_c offset "no diagnosis" | Correct: the independent code agrees to 10⁻⁵ | The offset is attributed to the [summary] target; CALIBRATED stands |

### Found during reconciliation

- **E1e, DSV trains.** (0.95, 0.62), the producer behind the DSV quanta count, is not converged. With fourth-order stepping it makes a pair at dx = 0.05 but not at 0.025, and the two runs separate at t = 168, before the pair forms.
  - The lowest-energy converged producer is (0.94, 0.67): E = 7.81 × 2M, N_min·λ/m² = 5.20 (N = E/m) or 4.14 (N_lin).
  - The old rows → OPEN (withdrawn), and a new QUANTIFIED row is added. The Gaussian headline numbers, 1.24 / 1.69, are unchanged.
- **Point-level DSV map.** Five of the 14 lowest-energy producers of the dx = 0.1 leapfrog map are not reproduced with fourth-order stepping. That map should be read as bands, not points.

## Final verdicts

**Calibration**

- E1a M_kink, ω_s: CALIBRATED.
- E1b v_c = 0.26006, first window [0.19256, 0.20343], 20 narrowing windows: CALIBRATED.
- E1c DSV trend, pass-through, hole (0.91, 0.82), ω > 0.99 null: CALIBRATED.
- E1c DSV example point (0.99, 0.43): OPEN (chaotic).

**Checks**

- E1d, no production below 2M: CHECK PASSED.

**Seed claims**

| Claim | Verdict |
|---|---|
| §2 pairs; threshold 2M | CONFIRMED (was AMENDED) |
| §4 small packet passes through | CONFIRMED |
| §4 pile in energy and it folds | AMENDED (amplitude controls; self-folding at A > √2 − 1) |
| §4 DSV trains, "most easily at low speed" | AMENDED (was CONFIRMED) |
| §4/§7.1 ragged boundary | CONFIRMED |
| PLAN E1d, favours low speed | REFUTED (was part of AMENDED) |
| PLAN E1d, favours wide packets | AMENDED (fixed amplitude only) |
| §8 / E1e, N ~ 1/λ quanta | QUANTIFIED: Gaussian 1.24–1.80 (N = E/m), 1.69–1.96 (N_lin); DSV 5.20 / 4.14; floor 2/3 |
| §8, few-quanta production exponentially rare | OPEN (needs a semiclassical computation) |

## Still open

- **DSV's example point.** Settling it would need errors 10²–10³ times smaller than at (dx, dt) = (0.0125, 0.005): at least two more halvings of dx and dt, about 2 h per run on one core, and two runs that agree. Even then, a chaotic call carries little meaning; the neighbourhood frequency (0 of 11 in its cell, 3 of 11 in the 0.41 cell) is the useful number.
- **DSV's discretisation.** It is not stated, so a v-offset between their map and ours cannot be excluded.

## Files

New:

- Code: `e1d_speedtest.py`, `e1c_example_y4.py`.
- Data: `e1d_speedtest.jsonl`, `e1d_speedtest.json`, `e1c_example_y4.npz`.
- Figure: `fig_e1c_example_y4.png`.
- Logs: `logs/e1d_speedtest.log`, `logs/e1c_example_y4.log`, `logs/e1c_reconcile_analysis.log`, `logs/e1d_confound.log`.

Extended:

- `e1c_reconcile.py` (passes F and G), with `e1c_reconcile.jsonl` and `reconcile_data/` (now 96 runs).
- `e1c_reconcile_analysis.py` and `.json`, `fig_e1c_reconcile.png`.
- `reconcile_results.py`, `run_all.sh`.

Updated:

- `results.json` (verdicts, notes, new rows, a `reconciliation` block), `seed_claims.json`.
- `REPORT.md`, corrected in place, with a Reconciliation section appended.
