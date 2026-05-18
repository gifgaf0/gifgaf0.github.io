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
