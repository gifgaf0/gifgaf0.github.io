# Quartz Entropy Module — Implementation Notes (Brief 04)

Software interface only; physical hardware is out of scope. This file
records the things the brief asks for *plus* anything that surprised
me along the way.

## What landed

- `entropy/quartz_entropy_source.py` — ADC protocol, Simulated and
  Serial backends, HKDF-Expand stress-schedule derivation,
  `SessionCommitment` dataclass + make / verify functions, audit-log
  appender, and `QuartzEntropySource` orchestrator (commitment →
  schedule → ADC sample → SP 800-90B RCT/APT → SHA-256
  rolling-hash digitisation).
- `entropy/decoy_field.py` — `DecoyField` with `advance`,
  `current_schedule`, and `overlap_fraction`.
- `entropy/__init__.py` exports the new symbols alongside the
  existing entropy layer.
- `hybrid_kem/tests/test_quartz_entropy.py` — 17 tests, all passing
  in well under 2 seconds.

The Definition-of-Done one-liner works:

```bash
python3 -c "
from hybrid_kem.entropy.quartz_entropy_source import (
    QuartzEntropySource, SimulatedADCBackend)
s = QuartzEntropySource(SimulatedADCBackend(5), b'testkey'*4, 5)
print(s.sample_raw(32).hex())
"
# → 64 hex chars
```

## Simulated noise floor — observations

The brief calls the H_min defaults (0.5 / 0.8 bits/sample) "placeholder
estimates". In the simulator they are not used directly; the more
operationally visible knob is `noise_floor` on
`SimulatedADCBackend`. Empirically:

- **`noise_floor = 0.02-0.1` (the brief's example default).** Samples
  cluster tightly around 0. After 16-bit mapping the uint16s sit in
  a narrow band around 0x8000 and the *high* byte (which the byte-
  stream presents to the health tests first) is severely biased to
  0x7F / 0x80. APT(W=1024) fires on the simulated stream at this
  amplitude. This is the *correct* behaviour for a fail-closed
  source — at such low amplitude the simulated crystal is not a
  healthy entropy source.
- **`noise_floor = 0.4` Gaussian.** Clipping at ±1 produces runs of
  saturated 0x00 / 0xFF bytes; RCT(C=5) fires on the run length.
- **`noise_floor = 1.0` uniform** (`distribution="uniform"`).
  Effectively `U(-1, 1)`; both APT and RCT pass over 256 KiB
  comfortably. This is the path the entropy-quality tests use as a
  stand-in for post-conditioning whitened entropy that a real
  hardware build would aim for.

The Gaussian / uniform distinction lives entirely in the simulated
backend. Real hardware will have a noise distribution shaped by
the analogue stages (preamp, filter, ADC reference); calibrating
those is the operator's job and is what the placeholder H_min
estimates are intended to cover until that work is done.

## Decoy field — `overlap_fraction` at default params

Default parameters: `n_decoy_crystals=15`, `n_levels=4`, mirroring
the brief's "3–10x n_keyed_crystals" recommendation when
`n_keyed_crystals=5`. With 15 decoys and 4 levels, the probability
that the decoy field misses every keyed level in a single slot is
`(3/4)^15 ≈ 1.34 %`. Empirically over five seeds and the default
schedule (5 keyed crystals × 20 slots) the overlap fraction is
**1.0 in every sample** — the decoy field saturates the level
space at these parameters.

That's exactly what the brief asks for ("Should be > 0.8 for
effective decoy field"). It also means an operator who *wants*
the decoys to be sparse (so an adversary's signal-space
classifier has more to bite on) should run with `n_decoy_crystals
≤ n_keyed_crystals` and `n_levels` higher, or accept partial
overlap by design. The current defaults trade information-theoretic
overlap for steganographic completeness.

## SP 800-22 subset

The full SP 800-22 short suite needs the NIST reference C
implementation or a comparable Python port; that's a substantial
dependency and out of scope for this brief. `test_nist_sp80022_subset`
runs two of the most-cited subtests — monobit / frequency, and
runs — on 256 KiB of simulated output (uniform mode). Sample
output:

```
[sp800-22 subset] monobit p=0.1985, runs p=0.3801
```

Both p-values are well inside the standard `> 0.01` SP 800-22
pass band. The test does *not* hard-fail on borderline values
(per the brief); it asserts only that the source produces output
and that both subtests run to completion, then prints the p-values
for record. Running the full short suite would require shipping
or vendoring an SP 800-22 test harness.

## Edge cases in stress-schedule derivation

- `window_ms / min_dwell_ms < n_levels` raises `ValueError`
  ("schedule degenerate") — the brief's specified behaviour.
  Verified by `test_stress_schedule_rejects_degenerate`.
- Single crystal (`n_crystals == 1`) is supported; the schedule
  has `window_ms // min_dwell_ms` entries for that one crystal.
- Same `key_material` → byte-identical schedule
  (`test_stress_schedule_deterministic`); different key →
  different schedule (`test_stress_schedule_key_sensitive`).
  Both hold because HKDF-Expand is deterministic in its
  `(secret, info, length)` tuple.

## Commitment audit trail

`entropy/quartz_commitments.jsonl` is the append-only log; tests
use a per-test `tmp_path` to avoid polluting the real log. Each
record is `{session_id, timestamp_utc, stress_schedule_hash,
key_material_hash, n_keyed_crystals, window_ms, n_levels}`.
The key itself never appears — only its SHA-256 hash.
`verify_commitment` uses `hmac.compare_digest` for the hash
comparisons to keep timing-side-channel surface minimal.

## Pipeline integration

The brief's pipeline diagram is

```
QuartzEntropySource.sample_raw()
  ↓ raw ADC bytes
HealthTests (SP 800-90B RCT + APT)
  ↓
[Optional] IrrationalConditioner  ← Brief 03
  ↓
DRBG (SP 800-90A) — unchanged
```

The **IrrationalConditioner is not present in this repo** —
Brief 03 from the brief's framing of reference exists in a
parallel project namespace, not in `hybrid_kem/`. The brief
explicitly marks the conditioner as `[Optional]`, so
`test_pipeline_integration` wires Quartz → built-in
HealthTests → `DRBG.instantiate()` directly and asserts the
DRBG reaches the `instantiated` state. The brief's spec is
satisfied without the conditioner; if it lands later, slotting
it in is a one-line change in the test.

## Open hardware questions (for the operator)

- **ADC resolution.** The brief specifies 16-bit packing. Real
  crystal preamps will likely benefit from 18–24-bit ADCs.
  Treat the 16-bit format as a *post-quantisation* convention;
  upstream stages should run at higher resolution.
- **Stress actuator latency.** `min_dwell_ms = 50` is a software
  default. Real piezo stress actuators (typically PZT stacks
  driven through a HV amp) have settling times of order 1–10 ms;
  the dwell time should comfortably exceed the actuator settling
  time plus the ADC integration window.
- **Crystal lot sourcing.** For the decoy-field steganography
  argument to hold, all crystals should come from the same
  manufacturer lot. Mixed lots open a spectral-distinguisher
  attack — see brief Security Note 5.
- **Tamper evidence.** The commitment trail proves the *schedule*
  was committed before sampling. It does not prove the hardware
  operated as intended. A separate tamper-evidence layer (sealed
  enclosure, anti-removal cabling, etc.) is required for the
  full non-repudiation argument.

## What I did *not* do

- Physical hardware fabrication, wiring, or driver beyond the
  `SerialADCBackend` stub.
- Crystal fingerprint calibration — flagged as a future brief.
- Formal SP 800-90B entropy estimation; requires the real
  hardware.
- IrrationalConditioner integration; the file is not in this
  repo.
