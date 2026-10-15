# Project Status

**Last updated:** October 14, 2026

> **Notice (October 14, 2026).** SLWE is off the KEM path; the status below replaces the May 8 status, which
> remains in git history. The October 10 notice is kept as written:
>
> > **Notice (October 10, 2026).** Module-SLWE is broken. Its wrapper's shared secret also carries at most one bit,
> > since it is SHA-256(bit ‖ ciphertext). So the SLWE half adds nothing to the hybrid's security, which rests on
> > ML-KEM-1024 alone. See the notice in `README.md`. The status below is as of May 8 and is kept as written.

## Phase: standards-only hybrid KEM landed, with known-answer tests

The hybrid KEM is now built entirely from NIST/IETF standards. The Module-SLWE
research scheme has been removed from the hybrid (its structural break is
documented separately); the SLWE code remains in `kem_slwe/` as a research
artifact but no longer sits on the KEM path.

### Done
- [x] **Standards hybrid** — `hybrid_kem.py`, two profiles:
  - `xwing`: ML-KEM-768 + X25519, X-Wing combiner (`draft-connolly-cfrg-xwing-kem-11`), Category 3.
  - `mlkem1024+x25519`: ML-KEM-1024 + X25519, BBF-G-S 2019 transcript-binding combiner, Category 5.
- [x] **ML-KEM leg** — `kem_standard/mlkem_wrapper.py`, real FIPS 203 via pyca/cryptography (768 + 1024), deterministic keygen from the DRBG.
- [x] **X25519 leg** — `kem_classical/x25519_kem.py`, ephemeral-static DH (RFC 7748).
- [x] **Vetted combiner** — `combiner/xwing.py` (X-Wing) + `combiner/kdf_combiner.py` (BBF-G-S generic).
- [x] **Entropy** — SP 800-90A DRBG (`entropy/drbg.py`) seeded through the SP 800-90B health-tested local source (`entropy/{health_tests,qrng_source}.py`).
- [x] **Known-answer tests** — all pinned to published vectors:
  - ML-KEM-768/1024: NIST ACVP (keygen-from-seed + decaps), `tests/test_kat_mlkem.py`.
  - X25519: RFC 7748 §5.2, `tests/test_kat_x25519.py`.
  - X-Wing: draft-11 Appendix C, all 3 vectors (keygen + decaps), `tests/test_kat_xwing.py`.
  - DRBG: SP 800-90A CTR/HMAC `.rsp`, `tests/test_drbg.py`.
- [x] **Test suite** — 226 passing (`pytest`), KATs byte-exact against the vectors above.

### Next (optional)
1. Add ML-DSA (FIPS 204) signatures as a parallel standards leg, if a signed handshake is wanted.
2. Replace `QRNGSource(provider="local")` with a validated hardware noise source for any real deployment, and run the SP 800-90B non-IID estimators on its raw output (the continuous RCT/APT are in place; the one-time entropy estimate is a deployment step).
3. Cross-check ML-KEM against liboqs in CI (`MLKEMWrapper.cross_check`) when the binding is installed.

### Decisions locked
- Hybrid is standards-only: ML-KEM (FIPS 203) + X25519 (RFC 7748). No research scheme on the KEM path.
- Prefer the `xwing` profile (vetted, interoperable); `mlkem1024+x25519` for a Category-5 target.
- HMAC-DRBG-SHA256 primary, AES-CTR-DRBG-256 alternate (SP 800-90A).
- Exotic entropy sources (celestial/irrational/quartz/radio/microphone) are **not** on the seeding path and carry no entropy credit; they remain as research code only.
