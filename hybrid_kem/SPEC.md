# Hybrid PQC Testbed — Architectural Specification

**Version:** 0.1 (initial)
**Author:** M. Gifford
**Date:** May 2026
**Status:** Research testbed. Not for production use.

---

## §0 — Scope and Non-Goals

### What this is
A research testbed for studying hybrid post-quantum key encapsulation. Combines:
- Quantum-derived entropy (cloud QRNG with local entropy mixing)
- Φ-modular structured prime generation
- ML-KEM-1024 (NIST FIPS 203, Category 5)
- Module-SLWE (research scheme from SLWE_Prime_Master_v1.md)
- KEM combiner construction (Bindel-Brendel-Fischlin-Goncalves-Stebila 2019)

### What this is NOT
- Not a production cryptosystem.
- Not a security proof for Module-SLWE.
- Not a claim that the combined construction is "unbreakable."
- Not a NIST submission.

### Threat model the testbed targets
A nation-state-class adversary with:
- Classical compute at scale
- A fault-tolerant quantum computer (Shor, Grover at full scale)
- Cryptanalytic budget comparable to NIST PQC analysis efforts
- Network observation of any cloud-QRNG traffic

### Honest security posture
Per BBF-G-S 2019, if the KEM combiner is built correctly, the hybrid KEM is
IND-CCA2 secure if **either** ML-KEM-1024 **or** Module-SLWE is IND-CCA2 secure.
ML-KEM-1024 has years of cryptanalysis. Module-SLWE has open problems
OP-B through OP-F (see master doc). The hybrid's security floor is therefore
ML-KEM-1024's security; Module-SLWE contributes whatever residual hardness it
has, providing diversification against a future cryptanalytic break of
Module-LWE.

---

## §1 — Architecture

```
ENTROPY LAYER
├── QRNG cloud source (ANU / IDQ) ──┐
├── /dev/urandom (OS entropy) ──────┼── XOR ──▶ Health tests ──▶ DRBG
├── Cache (offline fallback) ───────┘     (SP 800-90B)    (SP 800-90A)
                                                                  │
                                            ┌─────────────────────┘
                                            ▼ seed bytes
PRIME LAYER
└── Φ-modular finder (sqt_prime_core) ──▶ structured primes
                                            │
              ┌─────────────────────────────┴─────────────────────────────┐
              ▼                                                            ▼
KEM-A: ML-KEM-1024                                  KEM-B: Module-SLWE
├── Primary: liboqs-python                          ├── Stub mode (deterministic)
├── Cross-check: fips203 (dkg)                      ├── Full mode (sqt_slwe__1_.py)
└── Outputs: pk_A, sk_A, ct_A, ss_A                 └── Outputs: pk_B, sk_B, ct_B, ss_B
              │                                                            │
              └─────────────────────┬──────────────────────────────────────┘
                                    ▼
                         COMBINER (BBF-G-S 2019)
                         ss_final = HKDF(ss_A ‖ ss_B ‖ ct_A ‖ ct_B)
                                    │
                                    ▼
                              ss_final (32 bytes)
```

---

## §2 — Module Specifications

### §2.1 entropy/qrng_source.py
**Purpose:** Fetch entropy from cloud QRNG, with local mixing and offline fallback.

**API:**
```python
class QRNGSource:
    def __init__(self, provider: str = "anu",
                 cache_size: int = 1024 * 1024,
                 mix_with_os: bool = True): ...

    def get_bytes(self, n: int) -> bytes:
        """Return n bytes of entropy.
        If mix_with_os: XOR cloud QRNG with /dev/urandom.
        If cloud unavailable: fall back to cache, then OS entropy.
        Logs source provenance for each byte block."""
```

**Providers (initial):**
- `"anu"` → `https://qrng.anu.edu.au/API/jsonI.php` (free, public, rate-limited)
- `"idq"` → IDQ Cloud QRNG (requires API key)
- `"local"` → /dev/urandom only (development/offline)

**Security note (in code comments):** Cloud QRNG over HTTPS is not
end-to-end secret. The provider sees what entropy you fetched. XOR-mixing
with local entropy ensures that compromise of either source alone does not
compromise the seed. Document this prominently.

**Tests:**
- Health tests pass on output
- Mixing actually XORs (verify byte-level)
- Fallback chain works when network is unavailable
- Statistical test: NIST SP 800-22 short suite on 1MB sample

---

### §2.2 entropy/health_tests.py
**Purpose:** SP 800-90B entropy source health tests.

**Implements:**
- Repetition Count Test (continuous)
- Adaptive Proportion Test (continuous, 512-byte and 1024-byte windows)
- Startup tests (run on first 1024 samples)

**API:**
```python
class HealthTests:
    def __init__(self, alpha: float = 2**-30): ...
    def update(self, sample: bytes) -> bool:
        """Returns True if all tests pass; False if any fail.
        Failed health tests should halt entropy delivery."""
    def status(self) -> dict:
        """Returns counts, recent failures, current state."""
```

**Reference:** NIST SP 800-90B §4.4.

---

### §2.3 entropy/drbg.py
**Purpose:** Deterministic Random Bit Generator per SP 800-90A.

**Implements:**
- HMAC-DRBG with SHA-256 (primary)
- AES-CTR-DRBG with AES-256 (alternate, for cross-check)

**API:**
```python
class DRBG:
    def __init__(self, algorithm: str = "hmac-sha256"): ...
    def instantiate(self, entropy_input: bytes,
                    nonce: bytes,
                    personalization: bytes = b""): ...
    def reseed(self, entropy_input: bytes,
               additional_input: bytes = b""): ...
    def generate(self, n_bytes: int,
                 additional_input: bytes = b"") -> bytes: ...
```

**Tests:** NIST CAVP Known-Answer Test vectors. Non-negotiable.

---

### §2.4 primes/prime_adapter.py
**Purpose:** Wrap existing `sqt_prime_core__1_.py` with the testbed API.

**API:**
```python
class PrimeProvider:
    def __init__(self, mode: str = "phi_modular"):
        """Modes: 'phi_modular' (W=10920), 'mod_455', 'mod_3640', 'standard'."""

    def generate(self, bits: int,
                 entropy: DRBG,
                 require_safe: bool = False) -> int:
        """Generate certified prime of given bit length.
        entropy provides the random bytes for candidate selection."""
```

**Note:** Primes for ML-KEM are not user-supplied (q is fixed at 3329 by
FIPS 203). This module is for SLWE, prime-based signatures, and any future
component that needs primes. Keep it.

---

### §2.5 kem_standard/mlkem_wrapper.py
**Purpose:** ML-KEM-1024 with two backends and cross-validation.

**API:**
```python
class MLKEMWrapper:
    def __init__(self, backend: str = "liboqs"):
        """Backends: 'liboqs', 'fips203'."""

    def keygen(self, drbg: DRBG) -> tuple[bytes, bytes]:
        """Returns (public_key, secret_key)."""

    def encaps(self, pk: bytes, drbg: DRBG) -> tuple[bytes, bytes]:
        """Returns (ciphertext, shared_secret)."""

    def decaps(self, sk: bytes, ct: bytes) -> bytes:
        """Returns shared_secret."""

    @classmethod
    def cross_check(cls, drbg: DRBG) -> bool:
        """Run keygen+encaps+decaps with both backends.
        Verify identical shared secrets given identical entropy."""
```

**Critical:** ML-KEM is deterministic given the entropy seed. Both backends
must produce byte-identical output for byte-identical entropy. If they don't,
one is wrong, and we halt.

**Tests:** NIST KAT vectors for ML-KEM-1024 (from FIPS 203 test vectors).

---

### §2.6 kem_slwe/slwe_wrapper.py
**Purpose:** Module-SLWE with stub and full modes, identical API to MLKEMWrapper.

**API:**
```python
class SLWEWrapper:
    def __init__(self, mode: str = "stub",
                 params: dict = None):
        """Modes:
         - 'stub': returns deterministic test values, fast, for integration testing.
         - 'toy': p=911, k=4 (matches existing sqt_slwe__1_.py).
         - 'full': k=32, q ≈ 2^32, mod-455 prime (the target).
        """

    def keygen(self, drbg: DRBG) -> tuple[bytes, bytes]: ...
    def encaps(self, pk: bytes, drbg: DRBG) -> tuple[bytes, bytes]: ...
    def decaps(self, sk: bytes, ct: bytes) -> bytes: ...
```

**Wraps:** existing `sqt_slwe__1_.py` for toy/full modes.

**Stub mode:** returns 32-byte shared secret = HMAC-SHA256(drbg_seed, "stub-slwe").
This lets us test the combiner without running full SLWE every iteration.

---

### §2.7 combiner/kdf_combiner.py
**Purpose:** Combine two KEM outputs into a single shared secret per BBF-G-S 2019.

**Construction (the "dual-PRF" combiner from BBF-G-S §3.2):**
```
ss_final = HKDF-Extract-then-Expand(
    salt = SHA-256("hybrid-kem-v1"),
    ikm  = ss_A || ss_B,
    info = ct_A || ct_B || pk_A || pk_B,
    L    = 32 bytes
)
```

The inclusion of `ct_A || ct_B` is essential — it binds the shared secret to
the specific transcript and prevents certain attacks.

**API:**
```python
def combine(ss_a: bytes, ss_b: bytes,
            ct_a: bytes, ct_b: bytes,
            pk_a: bytes, pk_b: bytes) -> bytes:
    """Returns 32-byte combined shared secret."""
```

**Tests:**
- Test vector consistency
- If either ss is replaced, output changes
- If either ct is replaced, output changes (transcript binding)
- Combiner is deterministic (same inputs → same output)

---

### §2.8 Top-level: hybrid_kem.py
**Purpose:** The full hybrid KEM as a single object.

**API:**
```python
class HybridKEM:
    def __init__(self, slwe_mode: str = "stub", ...): ...

    def keygen(self) -> tuple[bytes, bytes]:
        """Returns (hybrid_pk, hybrid_sk).
        hybrid_pk = pk_A || pk_B
        hybrid_sk = sk_A || sk_B"""

    def encaps(self, hybrid_pk: bytes) -> tuple[bytes, bytes]:
        """Returns (hybrid_ct, ss_final)."""

    def decaps(self, hybrid_sk: bytes, hybrid_ct: bytes) -> bytes:
        """Returns ss_final."""
```

---

## §3 — Test Strategy

### §3.1 Test categories
1. **Known-Answer Tests (KATs)** — match published vectors exactly.
2. **Property tests (`hypothesis`)** — encaps∘decaps = identity, etc.
3. **Differential tests** — liboqs vs fips203 produce identical outputs.
4. **Statistical tests** — entropy source passes SP 800-22 short suite.
5. **Negative tests** — modified ciphertext fails decaps; malformed input rejected.
6. **End-to-end** — full hybrid keygen/encaps/decaps roundtrip.

### §3.2 Coverage targets
- Each module: ≥90% line coverage
- All API surface: 100% covered
- Failure modes: explicit test for every documented error case

### §3.3 What we are NOT testing
- We are not running cryptanalysis against the schemes.
- We are not measuring side-channel leakage (timing, cache).
- We are not certifying anything for FIPS compliance.

---

## §4 — Dependencies

```
liboqs-python    >= 0.10.0     # Primary ML-KEM
fips203          >= 0.1.0      # Cross-check ML-KEM (dkg)
cryptography     >= 42.0       # HMAC, HKDF, AES-CTR, SHA
gmpy2            >= 2.1        # Big integer arithmetic for primes
hypothesis       >= 6.0        # Property-based testing
pytest           >= 8.0        # Test runner
pytest-cov       >= 4.0        # Coverage
requests         >= 2.31       # ANU QRNG API
numpy            >= 1.24       # SLWE matrix ops
```

---

## §5 — Implementation Order

Build in this order; each step's output is independently testable:

1. **entropy/health_tests.py** — pure logic, no dependencies, fully testable.
2. **entropy/drbg.py** — KAT-tested against NIST vectors.
3. **entropy/qrng_source.py** — depends on (1) and (2); network-dependent tests mocked.
4. **kem_standard/mlkem_wrapper.py** — KAT-tested; cross-check between backends.
5. **combiner/kdf_combiner.py** — pure function; tested against the spec above.
6. **kem_slwe/slwe_wrapper.py** — stub first; full mode after wrapping sqt_slwe.
7. **hybrid_kem.py** — assembles all of the above.
8. **primes/prime_adapter.py** — independent of the rest; can be done anywhere.
9. **benchmarks/perf.py** — last; only meaningful when everything works.

---

## §6 — Open questions for later

- Should we add a third KEM (Classic McEliece, HQC) for additional diversification?
- Should the combiner output be 32 bytes (current) or longer (256 bits is enough
  for symmetric crypto but a larger output would future-proof against weaker
  symmetric primitives)?
- Do we want a wire format (binary) or stay with byte-string APIs?
- Signature scheme (ML-DSA-87) as a follow-on testbed?
