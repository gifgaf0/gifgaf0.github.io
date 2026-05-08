# Project Status

**Last updated:** May 8, 2026

## Phase: Brief 01 + skeleton protocol stack landed; full SLWE pending

### Done
- [x] Architectural spec (`SPEC.md`)
- [x] README and project layout
- [x] `pyproject.toml` with dependency list
- [x] Test fixtures (`tests/conftest.py`)
- [x] Brief 01: Entropy layer (`docs/CLAUDE_CODE_BRIEF_01_ENTROPY.md`)
- [x] Claude Code guide (`docs/CLAUDE_CODE_GUIDE.md`)
- [x] **Brief 01 implementation** — `entropy/{health_tests,drbg,qrng_source}.py`
- [x] **Combiner** — `combiner/kdf_combiner.py` (BBF-G-S 2019, length-prefixed info)
- [x] **KEM-standard wrapper** — `kem_standard/mlkem_wrapper.py`
      (liboqs / fips203 backends; X25519 test backend for CI)
- [x] **SLWE stub** — `kem_slwe/slwe_wrapper.py` (HMAC-derived shared secret)
- [x] **Top-level hybrid** — `hybrid_kem.py` + `demo.py` smoke test
- [x] **Test suite** — 50 passing pytest cases; 85% line coverage

### Next (in order)

1. **Brief 02 (KEM standard, real backends)** — install liboqs-python + fips203,
   wire up the cross-check fixture, add NIST FIPS 203 KAT vectors.
2. **Brief 03 (full SLWE wrap)** — replace `kem_slwe.SLWEWrapper(mode="stub")`
   with the toy and full parameter sets backed by `sqt_slwe__1_.py`.
3. **Brief 04 (prime adapter)** — `primes/prime_adapter.py` over
   `sqt_prime_core__1_.py`.
4. **Brief 05 (benchmarks + docs)** — `benchmarks/perf.py`, final write-up.

### Open questions to resolve as we go

- Wire format: stay with byte-string APIs, or define a binary format?
  (Decision: defer to brief 05 — integration time)
- Signatures (ML-DSA-87) as a follow-on testbed: yes/no?
  (Decision: defer until KEM testbed is solid)
- Should the prime adapter be early or late?
  (Decision: late — only SLWE consumes it; can build SLWE wrapper around it)

### Decisions locked
- ML-KEM-1024 as standard layer (Category 5)
- liboqs-python primary, fips203 (dkg) cross-check
- HMAC-DRBG-SHA256 primary, AES-CTR-DRBG-256 alternate
- ANU QRNG + /dev/urandom XOR mix
- BBF-G-S 2019 dual-PRF combiner
- Module-SLWE: stub mode for fast iteration, full mode for measurement
