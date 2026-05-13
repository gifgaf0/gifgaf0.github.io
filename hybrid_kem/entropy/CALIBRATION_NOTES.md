# Crystal Calibration — Implementation Notes (Brief 05)

Off-line tool that promotes (or falsifies) the T3 PUF claim from
Brief 04. Software-only deliverable: the simulated backend in
`FingerprintedSimulatedADCBackend` produces *synthetic* fingerprints
that are useful for exercising the pipeline but **must not** be
substituted for measured H_min on real hardware. The module enforces
this via `SimulatedCalibrationError` on
`update_health_test_params`.

## What landed

- `entropy/crystal_calibrator.py` — main module:
  `CrystalFingerprint`, `CalibrationResult`,
  `DiscriminabilityReport`, four SP 800-90B subset min-entropy
  estimators (MCV §6.3.1, Collision §6.3.2 simplified, Markov
  §6.3.3, Compression §6.3.4 via zlib proxy), Welch PSD,
  Jensen-Shannon distance, and `CrystalCalibrator` with
  `calibrate / identify / discriminability_report /
  update_health_test_params / export_report`.
- `entropy/quartz_entropy_source.py` extended with
  `FingerprintedSimulatedADCBackend` (per-channel tonal signatures
  for distinguishability tests) and a
  `QuartzEntropySource.verify_crystal_identity` tamper-detection
  hook with an append-only audit JSONL.
- `entropy/__init__.py` exports the new symbols.
- `pyproject.toml` adds `scipy >= 1.11`.
- `hybrid_kem/tests/test_crystal_calibrator.py` — 18 tests
  covering functional, discriminability, H_min estimation, tamper
  detection, and integration buckets from the brief.

Definition-of-done one-liner verified:

```bash
python3 -c "from hybrid_kem.entropy.crystal_calibrator import CrystalCalibrator; print('ok')"
# → ok
```

## PUF assessment on `FingerprintedSimulatedADCBackend`

The brief specifies that the simulated backend should yield
`puf_assessment='supported'` to confirm the pipeline works. **It
does — but the assessment is on simulated data and is not evidence
about real crystals.**

Observed numbers (5 channels × 1 stress level, n_fft=256,
calibration_samples=4096, seed=42):

| Quantity | Value |
|---|---:|
| min inter-crystal JS distance | **0.6342** |
| mean inter-crystal JS distance | 0.6387 |
| max inter-crystal JS distance | 0.6426 |
| max intra-crystal distance (single calibration per id) | n/a |
| PUF assessment | **supported (tier T2)** |
| recommended H_min | ≈ 0 (simulated; tonal signal is highly compressible) |
| recommended identity threshold | 0.15 (fallback default; no intra data) |

**Across all three stress levels** (5 crystals × 3 stress levels =
15 fingerprints), pairwise JS distance between *different* stress
levels of the *same* crystal becomes the dominant intra-class
distance source, and the assessment drops to **inconclusive (T3)**:

| Quantity | Value |
|---|---:|
| min inter-crystal JS distance | 0.4503 |
| mean inter-crystal JS distance | 0.4581 |
| max intra-crystal distance | **0.2013** |
| ratio min_inter / max_intra | 2.24 |
| PUF assessment | **inconclusive (tier T3)** |

This is the right behaviour for a simulated source — different
stress levels move the same channel's signature around as much as
the inter-channel separation, so the assessment is honestly
uncertain. The supported result at a fixed stress level confirms
the pipeline machinery works.

## Intra-crystal stability — drift across repeated calibrations

Running `cal.calibrate("crystal_x", ...)` twice on the same channel
with two fresh `FingerprintedSimulatedADCBackend` instances (seeds
1 and 2; same channel, same stress, same calibration parameters)
gave `max_intra = 0.0518` JS distance — small but non-zero, driven
by the channel-specific tones interacting with new Gaussian noise
realisations. With real hardware, the analogous test would measure
how much the noise PSD shifts between calibration runs under
temperature stability, and the recommended re-calibration interval
falls out of it directly.

A reasonable operator rule: re-calibrate at least monthly, and
warn if `calibrated_at` is more than 90 days stale.

## Recommended real-hardware calibration procedure

The brief asks for a recommended procedure, distinguishing
simulated from real. Notes for the operator:

1. **Setup.** Same crystal model and lot across all channels.
   `n_keyed_crystals + n_decoy_crystals` channels of ADC, each
   wired to a stress actuator with stable thermal environment.
2. **Per-crystal calibration.** For each crystal in the
   installation, for each stress level the protocol uses:
   - Set the actuator to the target stress level. Wait at least
     `10 × actuator_settling_time` for steady state.
   - Collect `calibration_samples ≥ 88,200` ADC reads (2 s @
     44.1 kHz). Brief 05's default is 44,100 (1 s); 2 s gives
     more stable Welch PSD estimates.
   - Run `CrystalCalibrator.calibrate(crystal_id, channel, adc,
     stress_levels)`.
3. **Intra-crystal stability check.** Repeat step 2 three times
   per crystal per stress level. Measure `max_intra` from the
   resulting `DiscriminabilityReport`. If `max_intra > 0.05`,
   investigate environmental controls (temperature, vibration)
   before proceeding.
4. **Inter-crystal discriminability check.** With all crystals
   calibrated, call `cal.discriminability_report(stress_level=L)`
   for each `L`. Promote PUF claim to T2 only if every stress
   level returns `puf_assessment='supported'`.
5. **Identity-threshold tuning.** Set
   `IDENTITY_THRESHOLD = 2 × max_intra_distance` from the
   discriminability report. The default `0.15` is an engineering
   placeholder; the report's `recommended_identity_threshold`
   field returns this value automatically.
6. **Re-calibration cadence.** Repeat the full sweep monthly.
   The `calibrated_at` field in each fingerprint is the audit
   record.

## Open hardware questions

- **ADC resolution.** 16-bit packing is the storage format. Real
  ADCs should probably operate at 18–24 bits internally and
  decimate; calibration at >16 bits would expose more PSD detail
  but would also require updating `_quantise_to_byte` if the
  H_min estimators are to consume the higher-resolution stream.
- **Sample count vs. PSD resolution.** Brief default is 44,100
  samples (1 s @ 44.1 kHz). At n_fft=512 that gives 256 PSD bins
  with ~86 Hz resolution. Production should use ≥ 88,200 samples
  and n_fft=1024 for ~43 Hz resolution.
- **Sample-count vs. minimum inter-crystal distinguishability.**
  How many samples are needed before two real (not synthetic)
  crystals' fingerprints separate reliably? Unknown without
  hardware. Calibration_samples × n_fft is the relevant product.

## What's *not* covered

- Real hardware measurement (this is the software interface only).
- Full SP 800-90B 10-estimator suite. We implement 4 of 10; the
  brief explicitly authorises this subset. A formal SP 800-90B
  submission would require all 10 plus the IID testing track.
- Automated re-calibration scheduling — the operator decides the
  cadence.
- Crystal aging model.

## T3 PUF claim status (simulated data only)

**On `FingerprintedSimulatedADCBackend` at a single stress level:
supported (T2).** This confirms the calibrator's pipeline works as
intended.

**On `FingerprintedSimulatedADCBackend` mixing stress levels:
inconclusive (T3).** Single-channel stress drift is comparable to
inter-channel separation under the simulator. Real hardware likely
behaves differently — but until that's measured, the conservative
documentation position is unchanged from Brief 04: the PUF claim
is T3 (conjectured / plausible) for real crystals, with this
module providing the apparatus to promote or falsify it
empirically.

**Falsification test, executed.**
`test_discriminability_report_identical_crystals` calibrates the
same channel twice under different IDs with identical seeds → JS
distance ≈ 0 → `puf_assessment='falsified'`. The falsification
path is exercised and `export_report` correctly emits the
FALSIFIED text required by the brief's §3 security note.
