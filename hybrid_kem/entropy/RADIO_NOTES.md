# Radio + Atmospheric Entropy Module — Implementation Notes (Brief 07)

Three-channel software interface; hardware out of scope. Keeps R1
(receiver thermal noise → entropy), R2 (atmospheric/cosmic →
conditioner only), and R3 (local RF fingerprint → personalisation
only) on separate code paths and never combines them. See the
module docstring for CORRECT vs WRONG three-channel usage.

## What landed

- `entropy/radio_atmospheric_entropy_source.py` — `SDRBackend`
  protocol; `SimulatedSDRBackend` with four modes (`thermal`,
  `atmospheric`, `rf_environment`, `saturated`); `SoapySDRBackend`
  stub guarded by `SOAPYSDR_AVAILABLE`; `detect_saturation` /
  `detect_strong_signal` diagnostics; `RadioAtmosphericEntropySource`
  with `thermal_sample_raw` (R1), `atmospheric_conditioner` (R2),
  `rf_environment_fingerprint` (R3), `run_h_min_estimation` (refuses
  simulated backends), and `status`.
- `entropy/__init__.py` exports the new symbols.
- `pyproject.toml` adds `[radio]` optional-dependency group for
  SoapySDR (with note that it's typically installed via system
  package manager).
- `hybrid_kem/tests/test_radio_atmospheric_entropy.py` — 22 tests
  across functional (6), saturation/signal detection (4),
  atmospheric (3), health (3), H_min (3), integration (2), plus
  the SoapySDR stub.

Definition-of-done one-liner verified:

```bash
python3 -c "
from hybrid_kem.entropy.radio_atmospheric_entropy_source import (
    RadioAtmosphericEntropySource, SimulatedSDRBackend)
s = RadioAtmosphericEntropySource(SimulatedSDRBackend('thermal'))
print(s.thermal_sample_raw(32).hex())
"
# → 64 hex chars
```

## Per-mode noise characteristics

Measured at 1.420 GHz (R1 default), 4096 IQ samples, seed=42:

| Mode | re_rms | im_rms | crest | saturated? | strong_signal? | peak_db_over_median |
|---|---:|---:|---:|:---:|:---:|---:|
| `thermal`         | 0.060 | 0.060 | **3.73** | ✗ | ✗ | 10.3 |
| `atmospheric`     | 0.060 | 0.060 | 3.73 | ✗ | ✗ | 10.3 |
| `rf_environment`  | 0.290 | 0.289 | 2.00 | ✗ | **✓** | **45.3** |
| `saturated`       | 0.990 | 0.990 | **1.00** | **✓** | ✗ | 11.0 |

Key observations:

- **`thermal` and `atmospheric` look identical at 1.42 GHz.** The
  simulator gates atmospheric content to frequencies below 100 MHz
  (HF only) — atmospheric/sferic activity in real life is an HF
  phenomenon, and a single SDR sampling at UHF for R1 and HF for
  R2 should see clean noise at UHF regardless of HF activity. This
  matches real operator setups; both channels can share one SDR.
- **`rf_environment` injects a strong narrowband tone** at 10% of
  the sample rate. `detect_strong_signal` fires at 45 dB above
  median noise floor → `SignalPresentError`. This is the correct
  fail-closed behaviour when an R1 frequency is contaminated.
- **`saturated` clips to ±0.99**, dropping crest factor to 1.0;
  `detect_saturation` fires → `SaturationError`. Correct
  fail-closed for over-gain conditions.
- **The Gaussian crest factor of ≈ 3.73 ≈ 12 dB** matches the
  Brief 06 reference for unprocessed noise.

## Atmospheric conditioner per mode

| Mode (at atmospheric_freq=10 MHz) | `atmospheric_conditioner(32)` |
|---|---|
| `thermal`         | raises `InsufficientAtmosphericActivityError` |
| `atmospheric`     | returns 32 bytes (sferic signature picked up) |
| `rf_environment`  | returns 32 bytes (the tone provides a peak) |
| `saturated`       | raises `InsufficientAtmosphericActivityError` |

The conditioner uses **complex IQ PSD via Welch** (not magnitude
PSD), with `return_onesided=False` because IQ signals carry
information in both halves of the spectrum. A constant-amplitude
narrowband CW tone in IQ produces a clear single-bin PSD peak — it
would NOT show in magnitude PSD because |a·e^{jωt}| is constant.
This is a subtlety from initial development that's worth retaining
as a comment in the code.

## Recommended frequency selection per device family

R1 thermal-noise frequency (must be quiet):

- **RTL-SDR** (24 MHz – 1.7 GHz): hydrogen line at 1420.405 MHz is
  ideal — globally protected from transmissions. Avoid 1090 MHz
  (ADS-B), 1575 MHz (GPS L1), 433 MHz / 868 MHz / 915 MHz (ISM).
- **HackRF One** (1 MHz – 6 GHz): same hydrogen line, or quiet
  pockets in 4–6 GHz licensed-but-unused bands. Above 3 GHz the
  receiver's own LNA noise dominates → more entropy per sample.
- **LimeSDR Mini** (10 MHz – 3.5 GHz): hydrogen line works;
  GPS L1 (1575 MHz) is good if GPS isn't relevant locally.
- **Airspy R2** (24 MHz – 1.8 GHz): hydrogen line.

R2 atmospheric frequency (HF, sferic-rich):

- **5–15 MHz** is the global sweet spot; 10 MHz is a reasonable
  default. Sub-30 MHz coverage requires an upconverter on
  RTL-SDR (Ham It Up or similar); HackRF and LimeSDR natively
  cover this range.
- Nighttime reception is generally 5–10 dB stronger due to
  ionospheric refraction of distant sferics.
- Indoor operation degrades signal; window-adjacent or outdoor
  antenna recommended.

R3 RF fingerprint band:

- **FM broadcast (88–108 MHz)** is the most reliable global
  default — every populated area has a stable station layout.
- For higher spatial resolution, **2.4 GHz ISM** (Wi-Fi /
  Bluetooth) gives a sharper location signature but is more
  dynamic (devices come and go).
- **Cellular (700–900 MHz, 1800–2100 MHz)** is stable but
  requires a wideband SDR.

## AGC disable procedure per device

| Device | How to disable AGC |
|---|---|
| RTL-SDR (Realtek RTL2832U) | `rtl_test` accepts `-g <gain>` flag; SoapySDR: set `gainMode = false`, then `gain = N` |
| HackRF One | No AGC by default; gain stages are LNA / VGA / amp via `setGain` |
| LimeSDR | `setGainMode(SOAPY_SDR_RX, ch, "MANUAL")` then explicit gain |
| Airspy R2 | `setGainMode(false)`, manual gain via SoapySDR API |

The `SoapySDRBackend` stub does not currently issue these calls;
the integrator must add them to the vendor-specific
`__init__` path. Operator verification: after instantiating the
SDR, call `detect_saturation` and `detect_strong_signal` on a
known-quiet frequency and inspect the rms / crest values.

## SoapySDR installation

`pip install SoapySDR` typically does NOT pull in the device
drivers — those are vendor-specific shared libraries that must
be installed via the system package manager:

```bash
# Debian/Ubuntu
sudo apt install soapysdr-tools soapysdr-module-rtlsdr \
                 soapysdr-module-hackrf soapysdr-module-lms7

# macOS
brew install soapysdr soapyrtlsdr soapyhackrf soapyremote
```

After installing the system packages, the Python `SoapySDR`
binding (named "SoapySDR" on PyPI) should import. The `[radio]`
optional dependency in `pyproject.toml` lists the PyPI package;
the underlying C library and driver modules are the operator's
responsibility.

## IQ imbalance

Real SDR hardware has gain and phase mismatch between the I and
Q signal paths. The brief mitigates this for R1 by using *only*
the imaginary component of IQ samples — IQ imbalance affects the
I/Q cross-correlation but each component's variance is unbiased.
A future improvement would add an IQ calibration routine
(complex correlation analysis on a known reference tone,
applied as a corrective transform on raw IQ before low-byte
extraction). Not in scope for this brief.

## Channel separation security summary

- **R1 (thermal_sample_raw):** primary entropy. The only channel
  whose output should ever pass through `entropy_input` of a
  DRBG instantiation. Quantum-mechanical origin (Johnson–Nyquist
  + shot noise + ADC LSB noise), non-injectable without
  physical access to the receiver. T2 after H_min calibration on
  target hardware.
- **R2 (atmospheric_conditioner):** XOR conditioner. Adds
  geographic and temporal diversity. **Observable** by adversaries
  with distributed HF receiver networks (same lightning strike
  reaches global receivers within milliseconds). T2 for
  conditioner use; T3 for any primary-entropy claim (would
  require a formal observability analysis we have not done).
- **R3 (rf_environment_fingerprint):** personalisation only.
  Fully observable and reproducible by any nearby receiver. **T1
  decision** — this is explicitly a personalisation input by
  design, not by limitation. It's a "MAC address for the radio
  environment" — useful for diversification across DRBG
  instances; never for unpredictability.

The CORRECT/WRONG usage examples in the module docstring make
this concrete. `test_wrong_channel_usage_documented` asserts the
"WRONG" pattern is present in the docstring so the warning
cannot be silently lost in a future refactor.

## What's *not* in scope

- `SoapySDRBackend.read_iq_samples` / `scan_power_spectrum` real
  implementation (stubs raise `NotImplementedError`).
- IQ imbalance calibration / correction.
- Direction finding, localisation, or multi-SDR aggregation.
- GNSS noise sources.
- Formal SP 800-90B characterisation on real hardware.

## Operator setup checklist

1. **Choose hardware.** Any SoapySDR-compatible device. RTL-SDR
   is the cheapest entry; HackRF / LimeSDR are recommended for
   sub-30 MHz coverage.
2. **Install drivers via system package manager** (see above).
3. **Antenna.** R1 doesn't need an antenna at all — the
   front-end thermal noise dominates with the input terminated
   or capped. R2 needs an HF-capable antenna (long-wire / random
   wire / loop). R3 works with the stock telescopic antenna on
   most consumer SDRs.
4. **Disable AGC and DSP** in the driver layer (see per-device
   table).
5. **Pick a quiet R1 frequency**, ideally the hydrogen line at
   1.42 GHz. Run `detect_strong_signal` to verify.
6. **Calibrate H_min** via `run_h_min_estimation()` on the
   actual hardware (refuses on `SimulatedSDRBackend` to prevent
   sim-numbers from being mistaken for measured numbers).
7. **Test the full pipeline** with the three-channel CORRECT
   pattern: R1 ⊕ R2 → DRBG `entropy_input`, R3 → DRBG
   `personalization_string`.
