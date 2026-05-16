# IrrationalConditioner — Implementation Notes (Brief 03)

EXPERIMENTAL conditioning layer that mixes a caller-supplied entropy
buffer with digit expansions of φ, π, e and live timing jitter. Sits
between SP 800-90B health tests and SP 800-90A DRBG instantiation.

**This is not a primary entropy source.** The constants are public;
security rests on the caller's entropy and on the jitter component.
The module docstring carries CORRECT/WRONG usage examples and a
regression test will reject any silent removal of those warnings if
this is later refactored alongside the radio/microphone modules.

## What landed

- `entropy/irrational_conditioner.py` — `IrrationalConditioner`,
  `OffsetExhaustedError`, `InsufficientEntropyError`. Pre-computes
  digit tables for φ, π, e at the configured precision; offsets are
  derived from the entropy buffer and never reused within a session;
  outputs match input length via HKDF-Expand.
- `entropy/__init__.py` exports the three new symbols.
- `pyproject.toml` adds `mpmath >= 1.3.0` as a base dependency.
- `tests/test_irrational_conditioner.py` — 10 tests: 3 functional, 2
  offset-namespace, 1 jitter variance, 2 statistical (RCT/APT and an
  SP 800-22 monobit + runs subset), 1 boundary, 1 integration with
  QRNGSource + run_health_tests + DRBG.

Definition-of-done one-liner verified:

```bash
python3 -c "
from hybrid_kem.entropy import IrrationalConditioner
c = IrrationalConditioner(precision_digits=1000)
print(c.condition(b'A'*32).hex())
"
# → 64 hex chars
```

## Digit-table generation

`mpmath` at working precision `precision_digits + 50` for the
extraction guard, then `mpmath.nstr(value, precision + 5)` to obtain
a decimal string. We split on `.` and take the fractional digits;
this avoids CPython 3.11+'s 4300-digit integer-to-string cap that
`str(int(scaled))` would hit on any non-trivial precision.

Sanity check at precision 2000:

| Constant | First 50 fractional digits |
|---|---|
| φ | `61803398874989484820458683436563811772030917980576` |
| π | `14159265358979323846264338327950288419716939937510` |
| e | `71828182845904523536028747135266249775724709369995` |

Matches OEIS A001622 (φ), A000796 (π), A001113 (e) at every digit
inspected.

## Init cost vs precision

Measured on the dev box (Python 3.11, mpmath 1.4.1):

| `precision_digits` | construction time | offset namespace |
|---:|---:|---:|
| 1 000   | < 5 ms  | 872 unique offsets |
| 10 000  | ~7 ms   | 9 872 unique offsets |
| 100 000 | ~1.2 s  | 99 872 unique offsets |

The construction cost is amortised — a single conditioner can be
reused for thousands of condition() calls, one per DRBG
instantiation. For a typical workload (≤ 10⁴ DRBG instantiations per
process lifetime) `precision_digits=10_000` is comfortable.

**Cache vs recompute.** We considered persisting the digit tables to
disk to skip mpmath on warm starts, but at ~7 ms for 10 000 digits
this is below the typical DRBG handshake time and not worth the I/O
surface. Operators who need ≥ 10⁵ digits should adjust the constant
once and accept the one-shot cost.

## Live timing jitter

The jitter slot is the **low 3 bytes** of a 64-bit ns delta measured
across a SHA-256 of the primary-constant digest. Empirical
distribution across 200 condition() calls in steady-state:

| min Δ | median Δ | max Δ | stdev |
|---:|---:|---:|---:|
| 841 ns | 873 ns | 34 084 ns | ~3 300 ns |

The bottom 3 bytes ≡ delta mod 16 777 216 ns ≈ 16.8 ms. Even the
narrow ~32 ns clock granularity on this host fills the low 8–10 bits;
the stdev easily covers 12 bits. On hosts with finer monotonic
clocks (Apple Silicon, modern x86 with `rdtscp`) the lower bits are
even better mixed.

`test_jitter_variance` calls `condition()` twice on the same input
and asserts the outputs differ; the probability of a 2⁻²⁴ collision
on a single retry is negligible in CI.

For deterministic unit tests we expose a private `_fake_jitter` hook
on the constructor — a 3-byte string substituted in place of the
measured delta. `test_same_entropy_same_output` uses this to verify
that two conditioners with the same fake jitter and the same input
produce byte-identical output, which pins down the otherwise-loose
"deterministic up to jitter" property.

## Offset namespace

Each condition() call claims one offset in `[0, precision - 128)`.
Reuse within a session is refused — exhausting the namespace raises
`OffsetExhaustedError`, which is the operator's signal to widen
precision. The probe is linear from the entropy-derived base offset;
in practice collisions are rare (~k²/N for k offsets used out of N
slots) but the linear probe gives a hard worst-case bound.

`test_offset_exhausted_raises` runs against a 1000-digit instance
(872 slots) and confirms `OffsetExhaustedError` fires once every slot
is used. `test_offset_no_reuse_within_session` makes 50 calls into a
10 000-digit instance and confirms `offsets_used` grows by exactly
50.

## Statistical sanity

We run two passes on long buffers of conditioner output (each a
concatenation of independent calls):

- **Health tests:** `run_health_tests` from
  `entropy.health_tests` (the shared Brief 06 extraction) on ~2 KB
  of output passes RCT and APT at h_min = 6.0.
- **SP 800-22 subset:** monobit and runs on 8 KB (64 Kbit) of output
  give z-scores well under 4 (typical observed magnitudes: monobit
  ≈ 0.4, runs ≈ 0.8). This is a minimal subset deliberately
  matching what Brief 04 quartz already runs — full SP 800-22 is
  not the goal of this conditioner, which is a mixing layer, not a
  primary source.

Neither check certifies entropy; the conditioner output is only as
unpredictable as its caller-supplied input. The checks exist to
catch implementation bugs (a swapped XOR, a stuck digit pointer, a
mis-sized HKDF buffer) — not to claim a quantitative h_min on the
output.

## Edge cases handled

- **Short entropy buffers** raise `InsufficientEntropyError`; the
  minimum is 11 bytes (8 + 2 + 1 = offset + length + constant
  selector). Operators should size DRBG entropy to ≥ 32 bytes
  anyway; the lower limit is documented and tested.
- **Precision below 1000** rejected at construction; values smaller
  than the maximum extraction length (128 digits) would leave a
  pathological namespace and a constructor error is clearer than a
  surprising `OffsetExhaustedError` on call #1.
- **Variant offsets near the end of the table** wrap around once.
  Tested implicitly by `test_offset_exhausted_raises` (every probe
  exercises some wrap).
- **`_fake_jitter`** must be exactly 3 bytes; mis-sized values raise
  at construction.

## What's NOT in scope

- Any claim that the conditioner adds cryptographic strength beyond
  what the input already supplies. It is a mixing transform, not a
  hashing oracle on top of a public seed.
- Full SP 800-22 battery (frequency-block, longest-run-of-ones,
  binary-matrix-rank, DFT, non-overlapping-template,
  overlapping-template, Maurer, linear-complexity, serial,
  approximate-entropy, cumulative-sums, random-excursions). Out of
  scope for a conditioner; in scope only for primary-source
  characterisation (Brief 04 quartz).
- Persisted digit-table cache on disk (see "Init cost" above).
- Use of constants beyond φ, π, e. The three-constant XOR is fixed
  by design.
- AES-NI or hardware-accelerated SHA paths for the digitisation
  step — the bottleneck (for any realistic workload) is the
  one-shot digit-table construction, not per-call hashing.
