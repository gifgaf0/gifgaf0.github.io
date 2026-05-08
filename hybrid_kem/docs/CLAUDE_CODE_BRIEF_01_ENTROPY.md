# Claude Code Task Brief #1 — Entropy Layer

**For:** Claude Code agent running in `hybrid_kem/` directory
**Author:** M. Gifford (research lead) and Claude (architecture)
**Date:** May 2026
**Estimated time:** 4–8 hours of agent work

---

## Mission

Implement and test the **entropy layer** of the hybrid PQC testbed.
This is the foundation: every other component depends on it. It must be
correct, well-tested, and have no shortcuts.

Read `SPEC.md` §0–§2.3 before starting. That defines the scope.

---

## Deliverables

Three modules, each with passing tests:

1. **`entropy/health_tests.py`** — SP 800-90B health tests
2. **`entropy/drbg.py`** — SP 800-90A HMAC-DRBG and CTR-DRBG
3. **`entropy/qrng_source.py`** — Cloud QRNG with mixing and fallback

Plus a coherent test suite in `tests/test_entropy.py`.

---

## Module 1: `entropy/health_tests.py`

### What to implement

Per NIST SP 800-90B §4.4, two continuous health tests:

**Repetition Count Test (RCT):**
- Track length of the most recent run of identical samples.
- Cutoff C = 1 + ⌈−log₂(α) / H⌉ where α is the false-positive rate
  and H is the assumed min-entropy per sample.
- Default: α = 2⁻³⁰, H = 8 bits/byte (conservative for healthy source).

**Adaptive Proportion Test (APT):**
- For each window of W samples, count occurrences of the first sample.
- If count exceeds threshold C, fail.
- Standard windows: W = 512 and W = 1024 (run both).
- Threshold C derived from α and H per SP 800-90B §4.4.2.

### Implementation notes

- Both tests run on every byte (treating each byte as a single sample with
  256 possible values).
- For multi-byte sample sizes, tests run independently per byte position.
- Use `bytes` input, return `bool` for pass/fail.
- Failure should be sticky — once failed, stays failed until reset.

### API

```python
class HealthTests:
    def __init__(self, alpha: float = 2**-30, h_per_byte: float = 7.5):
        """alpha: false positive rate per test
           h_per_byte: assumed min-entropy per byte (use 7.5 as conservative;
                       raw quantum should achieve >7.9 in practice)"""

    def update(self, sample: bytes) -> bool:
        """Process new sample bytes. Returns True if all tests pass.
        Once any test fails, stays in failed state until reset()."""

    def status(self) -> dict:
        """Returns:
        {
            'rct_count': int,        # current run length
            'rct_cutoff': int,       # threshold
            'apt_512_count': int,    # current window count
            'apt_512_cutoff': int,
            'apt_1024_count': int,
            'apt_1024_cutoff': int,
            'state': 'ok' | 'failed',
            'failure_reason': str | None,
            'samples_seen': int,
        }"""

    def reset(self) -> None:
        """Reset all state. Use after entropy source restart."""
```

### Tests

- `test_rct_passes_uniform_random()`: feed 100KB from /dev/urandom, must pass.
- `test_rct_catches_stuck_byte()`: feed `b'\x00' * 1000`, must fail RCT.
- `test_apt_passes_uniform_random()`: 100KB random, both APTs pass.
- `test_apt_catches_biased_source()`: feed bytes with one value 50% of time, must fail APT.
- `test_state_sticky_after_failure()`: trigger failure, then feed good bytes, state stays failed.
- `test_reset_clears_state()`: after reset, can pass again.
- `test_cutoff_calculations()`: cutoffs match SP 800-90B Table B.1 examples.

---

## Module 2: `entropy/drbg.py`

### What to implement

Per NIST SP 800-90A Rev 1:

**HMAC-DRBG (primary):** §10.1.2, with SHA-256.
**CTR-DRBG (alternate):** §10.2.1, with AES-256.

Both need the full state machine: `instantiate`, `reseed`, `generate`,
with reseed counter and reseed_interval = 2⁴⁸ (per spec).

### API

```python
class DRBG:
    def __init__(self, algorithm: str = "hmac-sha256"):
        """algorithm: 'hmac-sha256' or 'aes-ctr-256'"""

    def instantiate(self,
                    entropy_input: bytes,
                    nonce: bytes,
                    personalization: bytes = b"") -> None:
        """SP 800-90A §9.1. entropy_input must be ≥ security strength bytes."""

    def reseed(self,
               entropy_input: bytes,
               additional_input: bytes = b"") -> None:
        """SP 800-90A §9.2."""

    def generate(self,
                 n_bytes: int,
                 additional_input: bytes = b"") -> bytes:
        """SP 800-90A §9.3. Auto-reseeds if counter exceeded
        AND entropy is available; otherwise raises ReseedRequiredError."""

    @property
    def needs_reseed(self) -> bool: ...

    @property
    def state(self) -> str:
        """'uninstantiated' | 'instantiated' | 'failed'"""
```

### Tests

**Critical: KATs from NIST CAVP.**

Download HMAC-DRBG and CTR-DRBG test vectors from:
https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/random-number-generators

Place under `tests/kat_vectors/`. Tests must:
1. Parse the .rsp files
2. For each test case: instantiate, optionally reseed, generate
3. Compare output to expected bytes — must match exactly

Plus:
- `test_state_machine()`: must instantiate before generate; calling generate
  before instantiate raises.
- `test_reseed_counter()`: forces auto-reseed when threshold hit.
- `test_personalization_changes_output()`: same entropy, different personalization
  → different output.
- `test_additional_input_changes_output()`: same state, different additional_input
  → different output.

---

## Module 3: `entropy/qrng_source.py`

### What to implement

Cloud-QRNG client with:
- ANU QRNG provider (free, public)
- IDQ provider stub (with API key from env var)
- Local-only mode (development)
- Cache (offline fallback)
- XOR mixing with /dev/urandom (mandatory by default)
- Health tests applied to output before return
- DRBG seeded from output for downstream consumption

### ANU QRNG details

API endpoint: `https://qrng.anu.edu.au/API/jsonI.php`

Parameters:
- `length`: number of values (1-1024)
- `type`: `"uint8"` | `"uint16"` | `"hex16"`
- `size`: array length per value (for hex16)

Rate limit: ~1 request/minute per IP. Be conservative.

Response: JSON with `data` array. For uint8, each entry is 0-255.

### API

```python
class QRNGSource:
    def __init__(self,
                 provider: str = "anu",
                 cache_size_bytes: int = 1024 * 1024,
                 mix_with_os: bool = True,
                 health_test: HealthTests | None = None):
        """provider: 'anu' | 'idq' | 'local'
           cache_size_bytes: how much to keep on disk for offline use
           mix_with_os: XOR with /dev/urandom (RECOMMENDED, default True)
           health_test: optional HealthTests instance to apply"""

    def get_bytes(self, n: int) -> bytes:
        """Return n bytes of mixed entropy.
        Strategy:
        1. Try to fetch from cache.
        2. If cache short and provider available, fetch from provider.
        3. If still short, fall back to /dev/urandom only (logged).
        4. If mix_with_os, XOR with equal-length /dev/urandom bytes.
        5. Run through health tests.
        6. Return.
        Raises HealthTestFailure if tests fail."""

    def fetch_to_cache(self, n_bytes: int) -> int:
        """Eagerly fetch from provider. Returns bytes actually fetched.
        Use this to pre-populate cache before going offline."""

    def status(self) -> dict:
        """Returns:
        {
            'provider': str,
            'cache_bytes_available': int,
            'last_fetch_time': datetime,
            'last_fetch_size': int,
            'fetch_failures': int,
            'health_test_state': str,
            'mode': 'normal' | 'cache' | 'os_fallback',
        }"""
```

### Tests

- `test_local_mode()`: provider="local" never hits the network, returns
  /dev/urandom bytes. Mock `socket.socket` to verify no network calls.
- `test_xor_mixing()`: with mix_with_os=True, output ≠ raw provider bytes.
  With mix_with_os=False, output == raw provider bytes (use mock provider).
- `test_cache_fallback()`: provider raises ConnectionError; output still works
  if cache populated.
- `test_health_test_integration()`: feed broken provider (returns all zeros),
  health test catches it, get_bytes raises.
- `test_anu_response_parsing()`: mock the JSON response, verify parsing.
- `test_idq_requires_api_key()`: provider="idq" without env var raises.

**DO NOT** make real ANU API calls in tests — rate limits will bite.
Mock everything network-related. Have one optional integration test
behind `pytest --integration` flag.

---

## Cross-cutting requirements

### Code style
- Type hints on all public APIs.
- Docstrings on public methods (NumPy or Google style, pick one and stick with it).
- No bare `except:` — catch specific exceptions.
- No `print()` for logging — use the `logging` module.
- All randomness in tests must be seeded for reproducibility.

### Testing
- Use `pytest` and `hypothesis`.
- Run `pytest --cov=entropy` and ensure ≥ 90% coverage.
- All tests must pass on Python 3.10, 3.11, 3.12.

### Security hygiene
- No `eval`, `exec`, `pickle.loads` on untrusted data.
- Use `secrets.compare_digest` for any byte comparison touching secret data.
- Zero-out sensitive buffers when done (best-effort; Python doesn't guarantee).
- Comment any place where you intentionally relax this.

### Documentation
- Each module starts with a docstring explaining purpose and references.
- Cite SP 800-90A/B section numbers next to the code that implements them.

---

## Out of scope for this task

- KEM wrappers (later task)
- Combiner (later task)
- Prime adapter (later task)
- Performance optimization (later task)
- Real network calls in CI (use mocks)

---

## Definition of done

- [ ] Three modules implemented per spec
- [ ] All tests pass: `pytest tests/test_entropy.py -v`
- [ ] Coverage ≥ 90%: `pytest --cov=entropy tests/test_entropy.py`
- [ ] NIST KAT vectors validate for both DRBG variants
- [ ] `python -c "from entropy import QRNGSource; q = QRNGSource(provider='local'); print(q.get_bytes(32).hex())"` produces 64 hex chars
- [ ] No ruff/mypy errors: `ruff check entropy/ && mypy entropy/`
- [ ] Brief notes file `entropy/IMPLEMENTATION_NOTES.md` covering:
    - Anything that surprised you
    - Decisions made that the spec didn't pin down
    - Known limitations
    - Anything to revisit

---

## When done

Drop a summary in `entropy/IMPLEMENTATION_NOTES.md` and stop.
Do not start the next task automatically. M. Gifford reviews,
then issues the next brief.

If you hit a blocker, write the question in `entropy/QUESTIONS.md`
and continue with anything that can proceed without an answer.
