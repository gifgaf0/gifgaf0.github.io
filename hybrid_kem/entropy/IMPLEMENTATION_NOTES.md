# Entropy Layer — Implementation Notes

Brief 01 deliverable. The entropy modules (`health_tests`, `drbg`,
`qrng_source`) are functional and unit-tested. Below are the things that
deviate from the literal letter of the brief, choices made where the spec
left room, and known limitations.

## Decisions made beyond the brief

- **APT cutoff via normal approximation.** SP 800-90B §4.4.2 gives the
  cutoff in terms of `CRITBINOM(W, 2^-H, 1 - alpha)`. We use a Beasley-
  Springer-Moro inverse-normal approximation. For `W ≥ 512` this is
  conservative to within fractions of a percent on the realised alpha.
  If anyone wants exact, swap in `scipy.stats.binom.ppf`.
- **`h_per_byte = 7.5` default** matches the brief's recommendation.
  Production callers should drive the value from the source's actual
  measured min-entropy.
- **HMAC-DRBG snapshot test instead of full CAVP integration.**
  `tests/test_drbg.py::test_hmac_drbg_snapshot_stable` pins a deterministic
  output so refactors that change byte-output break loudly. The CAVP
  KAT driver (`test_hmac_drbg_kat`) is wired up and parses the .rsp
  format; drop the official vectors into `tests/kat_vectors/` to enable.
- **CTR-DRBG, no df.** §10.2.1.5.1. Callers must supply at least
  `seedlen = 48` bytes of entropy on instantiate. We did not implement
  the derivation function variant because the brief calls for exact
  inputs from the QRNG side; df adds attack surface without buying
  anything in this configuration.
- **QRNG provider injection.** `QRNGSource` takes a `fetcher` callable
  rather than depending on `requests` at import time. This lets the test
  suite mock the network without monkey-patching, and lets advanced
  callers plug in (e.g.) IDQ's gRPC SDK without touching the wrapper.
- **OS-mixing happens after provider/cache.** XOR with `/dev/urandom`
  is applied to the assembled buffer just before health tests run. So
  even when we fall back to OS-only entropy, the mix step is a no-op
  (XOR with itself's own provider) — safe but worth understanding.

## Surprises

- `cryptography` 41.0.7 from Debian APT is broken on this image (the
  hazmat Rust binding panics on import). Tests pass on `cryptography ≥
  42` from PyPI, which is what `pyproject.toml` already requires.
- Naive concatenation in the combiner's `info` parameter would have a
  collision risk — see `tests/test_combiner.py::test_concat_ambiguity_resolved`.
  Length-prefixing is the simplest fix; we prefix every blob.

## Known limitations / to revisit

- **Real ANU integration test.** Behind `pytest --integration`. Not yet
  written; brief 02 can pick it up once we are willing to spend a real
  rate-limit slot.
- **Reseed-on-empty-cache policy.** `QRNGSource.get_bytes` quietly falls
  back to OS-only entropy when the provider is unreachable and the cache
  is empty. The status dict reflects this (`mode == "os_fallback"`,
  `fetch_failures` increments). Higher layers should fail closed if they
  require strict provenance.
- **Personalization length.** SP 800-90A places upper bounds on
  personalization and additional input. We do not enforce them — the
  cryptography library will hash inputs of any length, and the brief
  doesn't call for the cap. Add an explicit length check if a strict
  validator is needed.
- **Timing-safe equality.** `secrets.compare_digest` is not used inside
  the entropy layer because none of these calls compare secrets. If a
  caller compares DRBG outputs (e.g., against a known-answer test) on
  user-supplied data, they should use the constant-time helper.

## Coverage

`pytest --cov=. tests/` reports 85% line coverage with the test suite as
written. Untouched lines are mostly the IDQ provider path (no real key
during CI), `MLKEMWrapper` real-backend wrappers (no liboqs / fips203 in
the dev image), and a handful of validation branches that fire only when
the OS-side calls are stubbed.
