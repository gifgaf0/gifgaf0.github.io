# Microphone Entropy Module — Implementation Notes (Brief 06)

Dual-channel software interface; hardware out of scope. The module
keeps preamp thermal noise (Channel A → entropy) and room acoustic
content (Channel B → personalisation only) on separate code paths
and never combines them. See the module docstring for CORRECT vs
WRONG usage patterns.

## What landed

- `entropy/microphone_entropy_source.py` — `AudioBackend` protocol,
  `SimulatedAudioBackend` with three modes (`thermal`,
  `acoustic`, `agc`), `PyAudioBackend` stub gated on
  `PYAUDIO_AVAILABLE`, `detect_processing` (AGC gain-probe / noise
  gate / compression diagnostics), `_silence_probe` (RMS / crest
  factor / zero-crossing-rate / FFT-peak tone detection), and
  `MicrophoneEntropySource` with `preamp_sample_raw`,
  `acoustic_fingerprint`, `run_h_min_estimation`, and `status`.
- `entropy/health_tests.py` extended with stateless `rct() / apt() /
  run_health_tests()` plus a `HealthTestResult` dataclass — the
  brief's Refactor Gate. The canonical stateful `HealthTests` class
  was already shared between Brief 04 (`quartz_entropy_source.py`)
  and Brief 01 (`health_tests.py`); the new function-style API is
  a thin layer over the same cutoff calculators (`rct_cutoff`,
  `apt_cutoff`), so there is exactly one source of truth for both
  test definitions.
- `entropy/__init__.py` exports the new symbols.
- `pyproject.toml` adds `pyaudio >= 0.2.13` as an
  `[project.optional-dependencies] audio` extra. The full
  `MicrophoneEntropySource` test suite runs without `pyaudio`
  installed; only `PyAudioBackend.__init__` requires it.
- `hybrid_kem/tests/test_microphone_entropy.py` — 21 tests across
  the 6 buckets the brief specifies.

Definition-of-done one-liner verified:

```bash
python3 -c "
from hybrid_kem.entropy.microphone_entropy_source import (
    MicrophoneEntropySource, SimulatedAudioBackend)
s = MicrophoneEntropySource(SimulatedAudioBackend('thermal'))
print(s.preamp_sample_raw(32).hex())
"
# → 64 hex chars
```

## Crest factor and RMS on simulated modes

Measured on 4096-sample probes with deterministic seed 42:

| Mode | crest factor | RMS (dBFS) | AGC | noise-gate | compression | `processing_free` |
|---|---:|---:|:---:|:---:|:---:|:---:|
| `thermal`   | **3.93** | −40.0 | ✗ | ✗ | ✗ | **True** |
| `acoustic`  | 2.13 | −26.7 | ✗ | ✗ | ✗ | True |
| `agc`       | **1.16** | −47.3 | ✗ | ✗ | **✓** | **False** |

- `thermal` sits at the Gaussian-noise crest-factor reference (≈ 4 ≡ 12 dB),
  which is the brief's "uncompressed" target.
- `acoustic` is lower because the deterministic tones add to RMS without
  raising the peak proportionally — still above the 2.0 compression
  threshold, so it doesn't false-fire.
- `agc` is dragged below 2.0 by the simulator's peak-clamping
  behaviour; compression is detected and `processing_free` is False,
  exactly as the brief intends.

## Silence-probe results

| Mode | RMS (dBFS) | crest | tonal_content_detected |
|---|---:|---:|:---:|
| `thermal`  | −40.1 | 3.49 | False |
| `acoustic` | −26.7 | 2.20 | **True** |

Implementation detail: the FFT tone test trims the DC bin and the
top two near-Nyquist bins before computing peak / median, and uses a
20 dB threshold (not the 10 dB suggested by the brief). With pure
Gaussian noise, a 256-bin spectrum routinely shows peaks 8–12 dB
above the median by chance alone — a 10 dB threshold caused
false positives on `thermal` and was tightened.

## Low-8-bit extraction rationale (verified)

The brief asserts that the low byte of 16-bit PCM carries the
thermal-noise entropy while the high byte is dominated by DC drift
and slow hum. Measured on 8192 samples of `SimulatedAudioBackend
('thermal', seed=0xdead)` (low-amplitude Gaussian):

| Byte selected | H_min (bits/sample, min of 4-estimator subset) |
|---|---:|
| **Low byte**  | **2.94** |
| High byte | ≈ 0      |

The high-byte H_min is ≈ 0 because most samples sit within ±32k of
zero, so the high byte is overwhelmingly `0x00` or `0xff` after
two's-complement wrap-around (i.e. the high byte tracks the sign bit
plus a tiny drift). The low byte, in contrast, sees the per-sample
thermal noise without the DC clipping pattern and carries the
useful entropy. **Low-8-bit extraction is the correct digitisation
path** on this simulated backend, and the same argument applies to
real consumer preamps where the thermal floor amplitude is well
below full-scale.

The placeholder `H_min = 1.5 bits/sample` in `preamp_sample_raw` is
**conservative against the measured value** (2.94 ≫ 1.5) for the
simulator. Real hardware should be characterised via
`run_h_min_estimation()` — which the module refuses to honour on
`SimulatedAudioBackend` (`SimulatedEstimationError`), matching the
Brief 05 guard.

## Health-test extraction status (Refactor Gate)

The brief asks for an extraction of RCT / APT into
`entropy/health_tests.py`. The extraction was already done by
Brief 01 / Brief 04 — `health_tests.py` has held the canonical
`HealthTests` class since Brief 01, and `quartz_entropy_source.py`
already imports from it. What this brief added:

```python
# stateless function-style API (Brief 06 refactor gate)
rct(samples, h_min)                  -> bool
apt(samples, h_min, window=512)      -> bool
run_health_tests(samples, h_min)     -> HealthTestResult
```

These are convenience wrappers over the existing `rct_cutoff()` and
`apt_cutoff()` calculators. The microphone module uses
`run_health_tests` in batch mode after every `read_samples` call
(fail-closed: `HealthTestFailureError` aborts output on failure).
The same `RCT` cutoff formula (`C = 1 + ⌈−log₂α / H_min⌉`) is used
across Brief 01, 04, and 06.

A regression test (`test_health_test_extraction_refactored`)
asserts that the microphone module does **not** redefine `rct` or
`apt` locally and that the canonical implementations live in
`health_tests.py`.

## pyaudio optional-dependency behaviour

```python
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except Exception:
    PYAUDIO_AVAILABLE = False
```

- `SimulatedAudioBackend` works unconditionally.
- `PyAudioBackend.__init__` raises `ImportError` with a clear message
  if `pyaudio` is missing.
- `read_samples` on `PyAudioBackend` raises `NotImplementedError`
  with a pointer to the vendor SDK integration — same stub pattern
  as `SerialADCBackend` in Brief 04.

`pyaudio` is wired as `[project.optional-dependencies] audio` in
`pyproject.toml`. Install with `pip install hybrid_kem[audio]`.

## Operator guidance: verifying a real device is processing-free

Before deploying `PyAudioBackend` in production:

1. **OS-level disabling.** Open the OS audio settings and turn off
   any "noise suppression," "echo cancellation," and "automatic
   level adjustment" features for the target input device. On
   Linux, prefer `pavucontrol`'s raw monitor source; on macOS use
   `Audio MIDI Setup` and disable "Use ambient noise reduction"
   per-device; on Windows, "Microphone Enhancements" must all be
   disabled.
2. **Pyaudio path.** Some Pyaudio installations route through
   PulseAudio / WASAPI which apply DSP regardless. Verify by
   running `detect_processing(backend)` on the actual device:
   - `crest_factor` should be ≈ 4 for unprocessed Gaussian thermal
     noise.
   - `noise_gate_detected` should be False.
   - `agc_detected` should be False (this requires the backend to
     expose `set_gain`; many USB Audio Class devices do, laptop
     built-ins typically do not).
3. **Capsule check.** Block the microphone capsule with a foam plug
   so only preamp thermal noise reaches the ADC. RMS should be
   detectable but small (typically −40 dBFS or quieter). Tone test
   in `_silence_probe` should report `tonal_content_detected =
   False` once the capsule is blocked.
4. **Long-term stability.** Run `run_h_min_estimation()` once at
   installation and again after 24 h. Drift > 0.5 bits/sample
   suggests temperature-dependent gain that may also be observable
   to a remote adversary via thermal modelling.

## What's *not* in scope

- Real `PyAudioBackend.read_samples` (stub raises `NotImplementedError`).
- Formal SP 800-90B characterisation on real hardware.
- Multi-microphone array / beamforming.
- Radio / atmospheric noise source (separate brief).

## Open hardware questions

- Which consumer audio devices reliably expose raw PCM without
  DSP? Working list of "known good": USB Audio Class 2.0 devices
  in raw-streaming mode (Linux ALSA with `dsnoop` disabled);
  most prosumer USB interfaces (Focusrite Scarlett series with
  vendor DSP disabled).
- Which devices to avoid? Built-in laptop microphones (almost
  always apply OS-level DSP); USB headsets with "noise
  cancellation" branding; conference-call devices (Jabra, Polycom)
  that apply AEC at the firmware level.
- ADC resolution: 16-bit is the minimum; 24-bit gives more
  headroom for the low-bit extraction step without compressing
  the thermal noise into the LSB.

## Channel-separation security claim (T1 verified at interface level)

The module's two output methods produce disjoint byte streams.
`test_preamp_and_acoustic_outputs_independent` verifies this. The
*operator* is responsible for routing the streams correctly into
the DRBG; the module cannot prevent a caller from manually
concatenating the two (`test_wrong_channel_mixing_is_higher_entropy_floor_doc`
records this as an interface-level defect — both halves hash through
SHA-256, so the wrong-mixing output looks uniform statistically;
the security failure is architectural, not output-distribution).
