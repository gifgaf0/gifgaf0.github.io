# Hybrid PQC Testbed

A research testbed for hybrid post-quantum key encapsulation, combining
ML-KEM-1024 (NIST FIPS 203) with the Module-SLWE research scheme,
quantum-derived entropy from cloud QRNG, and the Φ-modular structured
prime finder.

**Threat model:** nation-state-class adversary with a fault-tolerant
quantum computer.

**Status:** under construction. Not for production use. See `SPEC.md`.

> **Notice (October 10, 2026).** The Module-SLWE half of this testbed adds no security.
> - **It is broken.** Its Singer-orbit public matrix has rank at most 76 at every module rank. So its public key can
>   be told apart from random, and its noise recovered from a 76-dimensional problem. With a uniform matrix it still
>   falls far short of its claims. See the SLWE negative-result note (Zenodo, doi:10.5281/zenodo.23270249) and its
>   revision in `audit_followup/closeout/step3/3b_slwe_eprint/`.
> - **Even unbroken, it would add at most one bit.** `kem_slwe/slwe_toy.py` derives its shared secret as
>   SHA-256(bit ‖ ciphertext), so anyone holding the ciphertext needs only two guesses.
> - **So item 2 under "What this is" does not hold:** SLWE gives no diversification. The combiner (item 1) is
>   unaffected, and the hybrid is secure if ML-KEM-1024 is, as "What this is NOT" says.
>
> The text below is kept as written.

## What this is

A working laboratory where:
1. The hybrid combiner (BBF-G-S 2019) gives the combined KEM the security
   floor of ML-KEM-1024 — well-studied, NIST-standardized.
2. Module-SLWE runs in parallel, contributing diversification: any future
   cryptanalytic break of Module-LWE doesn't immediately break the system.
3. Entropy comes from cloud QRNG (ANU/IDQ), XOR-mixed with /dev/urandom,
   so neither source alone reveals the seed.
4. The Φ-modular prime finder feeds whatever components need primes
   (currently SLWE; later, prime-based signatures).

## What this is NOT

- A production cryptosystem. Use NIST-standardized libraries for that.
- A security proof for Module-SLWE. The hybrid is secure if ML-KEM-1024 is.
- A claim that the construction is "unbreakable." Computational security is
  always conditional on hardness assumptions.

## Quick start (when implementation lands)

```bash
git clone <repo>
cd hybrid_kem
pip install -e .
pytest                  # full test suite
python demo.py          # end-to-end keygen+encaps+decaps
```

## Architecture

See `SPEC.md` for the full architectural specification. High-level:

```
QRNG ──▶ Health Tests ──▶ DRBG ──┐
                                  │
                       ┌──────────┼──────────┐
                       ▼          ▼          ▼
                   ML-KEM-1024  SLWE      Primes (Φ-modular)
                       │          │
                       └────┬─────┘
                            ▼
                       Combiner (BBF-G-S)
                            │
                            ▼
                      ss_final (32B)
```

## Project layout

```
hybrid_kem/
├── SPEC.md                # Architectural specification
├── README.md              # This file
├── entropy/               # QRNG, health tests, DRBG
├── primes/                # Φ-modular prime adapter
├── kem_standard/          # ML-KEM-1024 wrapper (liboqs + fips203)
├── kem_slwe/              # Module-SLWE wrapper (stub + full)
├── combiner/              # KEM combiner (BBF-G-S 2019)
├── tests/                 # Test suite
└── benchmarks/            # Performance measurement
```

## References

- FIPS 203 (ML-KEM): https://csrc.nist.gov/pubs/fips/203/final
- BBF-G-S 2019 (KEM combiners): https://eprint.iacr.org/2018/903
- SP 800-90A (DRBGs): https://csrc.nist.gov/publications/detail/sp/800-90a/rev-1/final
- SP 800-90B (entropy sources): https://csrc.nist.gov/publications/detail/sp/800-90b/final
- liboqs: https://openquantumsafe.org/
- ANU QRNG: https://qrng.anu.edu.au/

## Author

M. Gifford · 2026
