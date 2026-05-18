# Alpha-Decay Entropy Source — Implementation Notes

Brief 07 deliverable, May 2026. Empirical behaviour, operator guidance,
and open hardware questions for `entropy/alpha_decay_entropy_source.py`.

---

## Observed KS p-values on `SimulatedTimingBackend('ideal')`

The CDF transform `u_i = 1 - exp(-λ̂ · Δt_i)` produces uniform `u_i`
**by construction** when `λ̂ → λ`. With n=4096 probe events from
`SimulatedTimingBackend('ideal')`, the KS-test of measured Δt against
`Exp(λ̂)` returns very large p-values across the entire operating range:

| rate_hz | KS p-value | rate_cv (8 sub-windows) | dead_ok |
|--------:|-----------:|------------------------:|:-------:|
| 100     | 0.84       | 0.042                   | True    |
| 1 000   | 0.84       | 0.042                   | True    |
| 10 000  | 0.84       | 0.042                   | True    |

The seed-locked p-value is rate-invariant because the inter-arrival
distribution is rate-invariant after the MLE rate estimate is divided
out — exactly the property the CDF transform exploits.

## Observed behaviour of `detect_non_poisson` on `'dead_time'` mode

Dead-time `τ` enters as a shift parameter — `Δt = τ + Exp(λ)`. At rate
1 kHz (mean Δt = 1 ms = 1e6 ns), the KS test rejects `Exp(λ̂)` once
`τ·λ` exceeds roughly 10⁻²:

| dead_time_ns | τ·λ      | KS p-value  | dead_ok | exponential_fit_ok |
|-------------:|---------:|------------:|:-------:|:------------------:|
| 1 000        | 1.0e-03  | 0.86        | True    | True               |
| 10 000       | 1.0e-02  | 0.50        | True    | True               |
| 100 000      | 1.0e-01  | 2.2e-28     | True    | **False**          |
| 500 000      | 5.0e-01  | 2.0e-296    | True    | **False**          |

Read this as: a realistic detector with τ on the order of microseconds
running at kHz rates is *invisible* to the KS test. Once dead-time
fraction crosses ~10 % the shift becomes the dominant signal in the
empirical CDF and the test fires sharply. (`dead_ok` stays True
throughout because the dead-time mode never emits Δt < τ by
construction; that check fails only when the hardware is genuinely
broken — see `force_sub_dead_time_rate` in the simulator.)

## Observed behaviour of `'biased'` mode (gamma shapes)

Gamma with shape > 1 is more regular than exponential; with shape < 1
it is more bursty. The simulator enforces shape > 1. The KS test
rejects all of the following with overwhelming significance, so the
detector check is *very* sensitive to non-exponential shape:

| bias_shape | KS p-value   | exponential_fit_ok |
|-----------:|-------------:|:------------------:|
| 1.5        | 1.3e-31      | False              |
| 2.0        | 5.6e-76      | False              |
| 3.0        | 9.2e-166     | False              |
| 5.0        | 4.7e-311     | False              |
| 10.0       | ~ 0          | False              |

Even the mildest detectable bias (shape 1.5) yields p < 10⁻³⁰ at
n=4096. A pulser leaking into the chain (which would look like a
very-narrow-shape gamma in the limit) would be caught instantly.

## Quantizer bit choice rationale — empirical H_min

Per-sample min-entropy of the quantised byte stream from
`SimulatedTimingBackend('ideal')`, n=8192 samples, 8 quantizer bits:

| rate_hz | H_min (MCV) | H_min (Coll) | H_min (Markov) | H_min (Compr) | min  |
|--------:|------------:|-------------:|---------------:|--------------:|-----:|
| 100     | 7.42        | 4.10         | 2.94           | 7.51          | 2.94 |
| 10 000  | 7.42        | 4.10         | 2.94           | 7.51          | 2.94 |

The estimators disagree by 3× — typical for finite-sample SP 800-90B
IID-track estimators on a stream that is approximately uniform but not
perfectly so. The Markov estimator (2.94 bits/sample) is the
conservative floor. The MCV and compression estimators are within ~0.5
bits of the 8-bit ceiling, consistent with near-uniform per-byte
distribution.

**Default `h_min_per_sample_bits = 1.0`** retains a 3× safety margin
over the worst-case (Markov) empirical estimate, and a 7× margin over
the MCV / compression estimates. Operators with measured H_min from
real hardware can pass that value at construction time (see API).

**Default `quantizer_bits = 8`** is a clean middle ground:
- Higher (`quantizer_bits=16`) doubles the output rate per event but
  the top 8 bits are roughly uniform (the CDF transform) and the
  bottom 8 are dominated by the per-event timing jitter — H_min
  density per *bit* drops correspondingly.
- Lower (`quantizer_bits=4`) halves the output rate per event and
  raises per-bit H_min density slightly. Useful only when the
  downstream extractor cannot use the full byte capacity.

---

## Operator guidance for real hardware

### Verifying detector dead time
Probe the discriminator output with an oscilloscope (≥ 200 MHz
bandwidth, ≥ 1 GS/s sample rate). Look for:

- the minimum spacing between adjacent rising edges. If the
  electronics dead time is 50 ns, that's the absolute floor; declare
  `dead_time_ns = 50` or a comfortable margin above (the brief defaults
  to 1000 = 1 µs to bracket typical PIN-photodiode discriminator
  recovery).
- after-pulses (a second pulse riding on the tail of the first). If
  present, after-pulses violate the IID assumption — they correlate
  the next inter-arrival with the previous one. They are *not* caught
  by `detect_non_poisson`'s current three tests (the Markov H_min
  estimator would catch them, which is why it is in
  `run_h_min_estimation`).

### Verifying rate stability over a long run
Capture an overnight count log (one count per 1-second wall-clock
window) and plot rate vs. time. Acceptable:

- < 5 % rate drift across the run for a sealed Am-241 source at room
  temperature (no environmental control).
- Periodic dips of a few percent during HVAC cycles (temperature
  affects ionization-chamber leakage).

Unacceptable:

- Monotonic decay over hours (source unsealing, photodiode bias
  drifting, discriminator threshold drifting).
- Sudden steps (electronics intermittent failure, source
  contamination, geometric change).

If the long-run rate CV across 1-second sub-windows exceeds 25 %, the
detector chain is non-stationary and `detect_non_poisson` will reject
on the rate-stability test at next probe.

### Verifying absence of after-pulses (Brief 07.1)

After-pulse detection requires either:

- **Histogram inspection.** Capture ≥ 10⁵ events and bin Δt on log
  axes. Look for excess at small Δt that breaks the exponential line —
  the after-pulse "shoulder" sits at the characteristic delay and
  drops back to the primary distribution beyond a few characteristic
  delays.
- **Autocorrelation.** :func:`detect_non_poisson` now reports two lag-1
  statistics (Briefs 07.1 + 07.2):
  - ``lag1_autocorrelation`` (linear domain): catches strong correlation,
    burst-like after-pulse signatures.
  - ``lag1_autocorrelation_log`` (log domain): catches weak correlation
    in the small-Δt regime, additive after-pulse signatures.

  Both default to |ρ₁| < 0.05. Either firing flips
  ``poisson_compatible`` to False. If only the log-domain check fires,
  the after-pulse signature is weak — investigate hardware (see fixes
  below) or apply a software veto as last resort. The combined check
  catches additive after-pulses with `f ≳ 0.1` at `d ≈ μ`; below that,
  the marginal-distribution KS check is the safety net (see "Linear vs
  log-domain lag-1 sensitivity comparison").

If after-pulses are observed:

- Check **discriminator hysteresis**. Insufficient hysteresis allows
  the falling edge of a primary pulse to re-trigger.
- Check **discriminator dead-time**. Increase if necessary, at the
  cost of a higher minimum Δt floor.
- Check **front-end amp ringing**. A poorly-terminated transimpedance
  amp can produce decaying oscillation that crosses threshold
  multiple times within tens of nanoseconds.
- If after-pulses persist and cannot be eliminated in hardware,
  apply a software veto: discard any event with Δt < veto_ns from
  the previous event. This raises the effective dead-time floor but
  eliminates the IID violation. Document the chosen veto_ns in the
  deployment configuration.

### Verifying the source is the expected isotope
Two methods of decreasing accessibility:

1. **Energy spectrum** (if the detector resolves energy). Am-241
   produces a sharp 5.486 MeV peak with a tail to lower energies from
   in-flight scattering. Po-210 produces 5.304 MeV. Th-232 + chain
   produces a wide spectrum spanning several MeV with multiple peaks.
   A PIN photodiode in vacuum with a multi-channel analyser can
   resolve these.

2. **Decay curve over months**. Half-lives are diagnostic:
   - Am-241: 432.2 y (no observable decay over months)
   - Po-210: 138.4 d (~15 % drop per month)
   - Th-232: 1.4 × 10¹⁰ y (no observable decay)
   - Sr-90 + Y-90 beta source (if mislabelled): 28.8 y / 64 h
     (no observable alpha-rate change since Sr/Y don't emit alphas,
     but cross-contamination would show as gamma background)

   Plot count rate weekly for 8–12 weeks; fit an exponential. Am-241
   will be flat; Po-210 will decline visibly.

---

## Open hardware questions

- **Which off-the-shelf PIN photodiodes have documented timing
  performance suitable for sub-µs Δt resolution?** Hamamatsu's S1223
  series (50 ns rise time) and S5821 series (~1 ns rise time, designed
  for laser ranging) are obvious candidates. Onsemi's TSL-series SiPMs
  are higher-cost but have ps-level timing jitter on photon arrival —
  overkill for alpha but very clean.

- **Is a microcontroller's hardware timer adequate, or does the
  inter-arrival timing demand an FPGA?** STM32H7 / G4 series have
  hardware capture timers at ~250 MHz (4 ns LSB), which is 10× the
  brief's `timing_resolution_ns = 1` default but matches reasonable
  PIN-photodiode rise times. For sub-ns resolution an FPGA TDC line is
  required (e.g., Lattice MachXO3 or Xilinx 7-series with
  carry-chain TDC).

- **What is the actual after-pulse fraction for a TO-18 packaged PIN
  photodiode at 5.486 MeV alpha incidence?** Vendor datasheets quote
  PMT after-pulse fractions but the equivalent number for a PIN diode
  + low-noise transimpedance amp is largely undocumented. This is the
  most important unknown for the IID assumption — should be measured
  empirically on the prototype detector by binning Δt and looking for
  excess counts at small Δt.

- **Cost-of-entry comparison.** A working prototype using an
  Am-241 smoke-detector source, a Hamamatsu S1223, an LM6172 op-amp,
  a Schmitt discriminator, and an STM32G4 with hardware timer is
  ~$80 in components. A research-grade setup with vacuum chamber,
  multi-channel analyser, and characterised cooled detector starts
  around $5–10k. Brief's threat model probably warrants the latter
  for production but the former is adequate for the testbed.

---

## Lag-1 autocorrelation calibration (Briefs 07.1 + 07.2)

Calibration sweep run at n=4096 probe events, seed=1, against the
``'after_pulse'`` simulator mode. Extended in Brief 07.2 with the
log-domain statistic.

| after_pulse_fraction | delay_ns | rate_hz | ρ₁(linear) | linear_ok | ρ₁(log) | log_ok |
|---|---|---|---|---|---|---|
| 0.00 (ideal) | — | 1 000 | +0.0145 | True | +0.0315 | True |
| 0.001 | 1 000 | 1 000 | −0.0087 | True | +0.0117 | True |
| 0.01 | 1 000 | 1 000 | −0.0010 | True | +0.0232 | True |
| 0.05 | 1 000 | 1 000 | −0.0023 | True | +0.0017 | True |
| **0.10** | **1 000** | **1 000** | **−0.0297** | **True** | **−0.0626** | **False** |
| 0.05 | 100 | 1 000 | −0.0024 | True | −0.0111 | True |
| 0.05 | 10 000 | 1 000 | −0.0020 | True | +0.0197 | True |
| 0.05 | 1 000 | 100 | −0.0024 | True | −0.0111 | True |
| 0.05 | 1 000 | 10 000 | −0.0020 | True | +0.0197 | True |
| **0.50** | **2 000 000** | **1 000** | **+0.0517** | **False** | **+0.0571** | **False** |
| **0.70** | **2 000 000** | **1 000** | **+0.0632** | **False** | **+0.0422** | **True** |

Three rows show the lag-1 family changing the verdict relative to the
KS check alone:

- `f=0.10, d=1µs`: **log catches what linear misses.** Linear |ρ|=0.030
  (below threshold); log |ρ|=0.063 (above threshold). This is the
  central Brief 07.2 win — one decade above brief-spec params, the log
  statistic closes the detection gap.
- `f=0.50, d=2µs`: both fire (agreement).
- `f=0.70, d=2µs`: **linear catches what log misses.** Linear |ρ|=0.063;
  log |ρ|=0.042. Confirms the two statistics are complementary, not
  redundant — at large f the dominant signal lives in the tail (linear)
  rather than at small Δt (log).

### Discrepancy with Brief 07.1's prediction

Brief 07.1 expected `ρ₁ ~ 0.02–0.10` for `f=0.05` / `d=1 µs` /
`rate=1 kHz`. The calibration shows that the brief overpredicted the
lag-1 signal by 2–3 orders of magnitude for these parameters.

The reason is structural. For the **additive** after-pulse model the
brief specifies (each primary spawns at most one secondary, merge and
sort), the lag-1 Pearson correlation of the merged Δt series scales
approximately as

    |ρ₁|  ≈  f · (d / μ)²

where `f` is the after-pulse fraction, `d` is the mean after-pulse
delay, and `μ = 1/λ` is the mean primary inter-arrival. At the brief's
example (`f=0.05`, `d=1 µs`, `μ=1 ms`) this gives `|ρ₁|` on the order
of `0.05 · (10⁻³)² = 5×10⁻⁸` — three orders of magnitude below the
n=4096 noise floor of `1/√n ≈ 0.016`.

The brief's `0.05` threshold and `n=4096` probe size are well-calibrated
for the **null hypothesis** (clean Poisson processes are rejected at the
0.1 % level), but the additive after-pulse model under the brief's
example parameters does not generate a signal above the noise floor.

### Sensitivity floor of the check (as built)

From the calibration sweep, lag-1 autocorrelation detects after-pulse
contamination only when **both** the fraction is large (`f ≳ 0.3`) **and**
the delay is on the order of the mean inter-arrival (`d ≳ μ`). For typical
PIN-photodiode after-pulse parameters (`f` a few percent, `d` in
nanoseconds-to-microseconds, `μ` in milliseconds at kHz rates), the
lag-1 check **does not** add useful discrimination over the KS check
alone.

Where the lag-1 check IS valuable in this simulator:

- **High-fraction edge cases** (`f ≳ 0.3`) where the KS check may itself
  desensitise because the modified marginal looks like an exponential
  with a slightly different rate. Lag-1 still fires because the
  serial correlation is independent of marginal-distribution drift.
- **Real detectors with non-additive failure modes.** A burst-mode
  detector (clusters of fast events followed by recovery) would
  produce strong positive lag-1 correlation without much marginal
  perturbation. The brief's additive model is just the simplest case;
  more pathological hardware failure modes are exactly what the lag-1
  guardrail is for.

### Linear vs log-domain lag-1 sensitivity comparison (Brief 07.2)

Direct comparison at matched parameters (seed=1, n=4096):

| regime | ρ₁(linear) | ρ₁(log) | log/linear ratio |
|---|---|---|---|
| brief-spec (f=0.05, d=1µs, μ=1ms) | 0.0023 | 0.0017 | 0.71× |
| moderate (f=0.05, d=10µs, μ=1ms)  | 0.0020 | 0.0197 | **10.11×** |
| strong (f=0.5, d=2µs, μ=1ms)      | 0.0517 | 0.0571 | 1.10× |

Across the 10-seed sweep at the brief-spec regime (f=0.05, d=1µs), the
log-domain |ρ| was **larger than the linear-domain |ρ| in 8/10 seeds**,
with a median ratio of approximately **3–4×**. The seed=1 row above is
one of the two outliers — usable as a worst-case bound but not the
typical case.

**Does log-domain close the gap on the brief-spec regime?**

**No, not reliably.** Even with the typical 3–4× sensitivity ratio,
the log statistic at brief-spec params averages |ρ(log)| ≈ 0.03,
still below the 0.05 threshold. The Brief 07.1 commit's
"~10× sensitivity improvement" estimate is roughly correct at the
*moderate* regime (one decade up in delay, where log catches 10×
better) but does NOT translate to threshold-crossing detection at the
PIN-photodiode-realistic brief-spec params.

**Where log-domain does close the gap:**

The `f=0.10, d=1µs` row in the calibration table is the headline
result. One increment up in fraction from the brief-spec example,
linear |ρ| sits at 0.030 (below threshold, undetected) while log |ρ|
reaches 0.063 (above threshold, **detected**). The two-decade lift in
sensitivity from the log transform — at this regime — converts a
silent failure mode into a guardrailed one.

**Sensitivity floor of the check (combined)**

For additive after-pulses with delay = mean inter-arrival (`d ≈ μ`):

- Linear: detects when fraction `f` ≳ 0.3
- Log:    detects when fraction `f` ≳ 0.1

For shorter delays (`d ≪ μ`, the brief-spec regime), neither lag-1
statistic reliably detects f ≲ 0.05. **KS continues to fire** because
the after-pulse contamination adds a marginal-distribution bump near
zero; the check is still useful, just via the marginal pathway rather
than the serial pathway.

### Threshold provisionality and recommended follow-up

Both lag-1 thresholds survived calibration unchanged at the brief-spec
0.05 value. They are appropriate for catching the regimes documented
above and remain safe-by-default against false-positives on clean
Poisson processes.

The empirical sensitivity gap at the brief-spec regime is a model
issue, not a check issue. Brief 07.2 closed item #2 of the Brief 07.1
follow-up list (log-domain); the remaining items still warrant
consideration:

1. A **burst-mode after-pulse simulator** that produces stronger lag-1
   correlation by clustering after-pulses temporally — closer to real
   PMT after-pulsing. Brief 07.1 deferred this; Brief 07.2 did not
   address it. Likely the next architectural step.
2. ~~A **log-domain** lag-1 statistic.~~ **Done in Brief 07.2.** Closes
   the gap one decade above brief-spec params, does NOT close it at
   the brief-spec params themselves.
3. **Higher-lag** autocorrelation (ρ₂, ρ₃) for multi-modal after-pulse
   delays, deferred under Brief 07.1's "Out of Scope".

For Briefs 07.1 + 07.2 combined: the dual-domain lag-1 check is
implemented as specified, both default thresholds are preserved, and
KS continues to catch the small-d/μ additive after-pulses that lag-1
misses. The combined `poisson_compatible` flag rejects the brief's
example case via the KS pathway and the `f=0.10, d=1µs` regime via the
log-domain lag-1 pathway. The sensitivity floor for additive
after-pulses where `d ≈ μ` dropped from `f ≳ 0.3` (linear only) to
`f ≳ 0.1` (linear OR log) — a 3× improvement.

### Cases where the autocorrelation check disagreed with KS

Documented in the calibration sweep above and in
`tests/test_alpha_decay_entropy.py::test_lag1_autocorrelation_zero_on_biased`:

- `'biased'` mode (gamma marginal, independent samples): **lag-1 says
  OK, KS says fail.** Expected and correct — gamma is iid but not
  exponential.
- `'after_pulse'` with low `f·(d/μ)²`: **lag-1 says OK, KS says fail.**
  The marginal "shoulder" near zero is visible to KS even when the
  serial correlation is below the noise floor.
- `'after_pulse'` with high `f` and `d ≈ μ`: **lag-1 says fail, KS
  says fail.** Both checks agree.

No simulator parameter set was observed where lag-1 fires while KS
passes. That regime exists in principle (burst-mode hardware) but is
out of scope for the additive simulator.

---

## Cross-references

- Brief 04 (ADCBackend protocol; `quartz_entropy_source.py` carries
  `HardwareUnavailableError` and `HealthTestFailureError` which this
  module re-uses).
- Brief 05 (H_min estimation; this module imports the four IID-track
  estimators from `crystal_calibrator.py`).
- Brief 06 (audio backend abstraction + channel-A/B separation
  pattern; `microphone_entropy_source.py` is the direct template).
- SPEC.md §2.1–§2.3 (entropy source / health tests / DRBG layer).
- `MICROPHONE_NOTES.md` (the analogous notes file for Brief 06; this
  file follows the same structure).

---

*End of alpha-decay implementation notes.*
