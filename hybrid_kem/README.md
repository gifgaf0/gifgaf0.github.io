# Hybrid PQC KEM

A standards-only hybrid post-quantum key encapsulation mechanism, combining
**ML-KEM (NIST FIPS 203)** with **X25519 (RFC 7748)** through a vetted combiner,
seeded by an **SP 800-90A** DRBG under **SP 800-90B** health tests.

**Status:** working, with known-answer tests pinned to published vectors. This
is research/engineering code — for production, use a maintained library
(pyca/cryptography, liboqs, BoringSSL) that carries the same standards.

> **Notice (October 14, 2026).** The Module-SLWE half has been removed: the hybrid is now ML-KEM + X25519 only,
> built entirely from standards. Why SLWE was removed is recorded in the October 10 notice, kept verbatim under
> [History](#history) below.

## Profiles

| Profile | Legs | Combiner | NIST category |
|---|---|---|---|
| `xwing` (default) | ML-KEM-768 + X25519 | X-Wing SHA3-256 combiner (`draft-connolly-cfrg-xwing-kem-11`) | 3 |
| `mlkem1024+x25519` | ML-KEM-1024 + X25519 | BBF-G-S 2019 transcript-binding (HKDF-SHA256) | 5 |

The shared secret stays secure as long as **either** leg does: a future break
of ML-KEM leaves X25519's classical security, and a quantum computer that
breaks X25519 leaves ML-KEM's. Prefer `xwing` — it is the interoperable,
externally vetted construction; use `mlkem1024+x25519` when a Category-5 target
is required (X-Wing specifies no 1024 variant).

## Signatures (composite ML-DSA + EdDSA)

A matching hybrid signature, `CompositeMLDSA`, implements
`draft-ietf-lamps-pq-composite-sigs-19`. A composite signature verifies only if
*both* components do, so it stays unforgeable as long as either ML-DSA or EdDSA
does.

| Profile | Components | Pre-hash |
|---|---|---|
| `id-MLDSA65-Ed25519-SHA512` (default) | ML-DSA-65 + Ed25519 | SHA-512 |
| `id-MLDSA87-Ed448-SHAKE256` | ML-DSA-87 + Ed448 | SHAKE256/64 |

```python
from hybrid_kem import CompositeMLDSA

c = CompositeMLDSA("id-MLDSA65-Ed25519-SHA512")
pk, sk = c.keygen()
sig = c.sign(sk, message, context=b"my-app")
assert c.verify(pk, sig, message, context=b"my-app")
```

## Authenticated handshake

`protocols/authenticated_handshake.py` ties the two together into an
authenticated key exchange: an *ephemeral* hybrid-KEM agreement for secrecy, and
a composite signature over the full transcript for authentication — the TLS 1.3
/ SIGMA pattern, built from the primitives above. The initiator derives a key
only if the responder's signature verifies; the transcript binds both
identities, their keys, the ciphertext and the suite.

```python
from hybrid_kem.protocols.authenticated_handshake import Identity, Initiator, Responder

server, client = Identity.generate("server"), Identity.generate("client")
resp = Responder("xwing", identity=server, require_peer=client.public)  # mutual
init = Initiator("xwing", peer=server.public, identity=client)

st_i, m1 = init.start()          # client -> server
st_r, m2 = resp.respond(m1)      # server -> client (encapsulate + sign transcript)
key_i, m3 = init.finish(st_i, m2)  # client verifies server, derives key, signs back
key_r = resp.confirm(st_r, m3)   # server verifies client
assert key_i == key_r            # authenticated 32-byte session key
```

Omit `identity`/`require_peer` for responder-only authentication (the common
"server-authenticated" case). This is an engineering construction following a
reviewed design, not itself a standardised or formally analysed protocol — for
production use TLS 1.3 with hybrid groups from a maintained library.

## Quick start

```bash
cd hybrid_kem
pip install cryptography            # FIPS 203 ML-KEM + X25519
pytest                             # 226 tests, incl. byte-exact KATs
python -m hybrid_kem.demo          # keygen/encaps/decaps, both profiles
```

```python
from hybrid_kem.hybrid_kem import HybridKEM

h = HybridKEM(profile="xwing")
pk, sk = h.keygen()               # seeds from the health-tested local source
ct, ss_sender = h.encaps(pk)
ss_receiver = h.decaps(sk, ct)
assert ss_sender == ss_receiver   # 32-byte shared secret
```

## Architecture

```
local noise ─▶ SP 800-90B health tests (RCT/APT) ─▶ SP 800-90A DRBG ─┐
                                                                      │
                                  ┌───────────────────────────────────┤
                                  ▼                                   ▼
                            ML-KEM (FIPS 203)                     X25519 (RFC 7748)
                                  │                                   │
                                  └─────────────── combiner ──────────┘
                                         X-Wing (SHA3-256)  |  BBF-G-S (HKDF)
                                                  │
                                                  ▼
                                           ss_final (32 B)
```

## Known-answer tests

Every primitive is pinned to a published answer (vectors vendored under
`tests/kat_vectors/` with provenance notes):

- **ML-KEM-768/1024** — NIST ACVP (final FIPS 203): keygen-from-seed and
  decapsulation, both reproduced byte-for-byte by pyca.
- **X25519** — RFC 7748 §5.2.
- **X-Wing** — draft-11 Appendix C, all three vectors (keygen and decapsulation,
  which runs the full combiner). Encapsulation is randomised and covered by
  round-trip tests.
- **ML-DSA-44/65/87** — NIST ACVP (final FIPS 204): keygen-from-seed and
  verification of the published signature.
- **Ed25519 / Ed448** — RFC 8032 (full deterministic signing).
- **Composite signatures** — draft-19 Appendix E, both profiles, with and
  without context.
- **DRBG** — SP 800-90A CTR-DRBG and HMAC-DRBG `.rsp` vectors.

## Entropy

The KEM draws randomness from an SP 800-90A DRBG. The DRBG is seeded from
`QRNGSource(provider="local")`, which runs the SP 800-90B continuous health
tests (Repetition Count + Adaptive Proportion) over the raw bytes. For a real
deployment, point the source at a validated hardware noise source and run the
one-time SP 800-90B entropy estimate on its output. The project's exotic
"entropy" experiments (celestial, irrational-constant, quartz, radio,
microphone) are **not** on this path and carry no entropy credit.

## Project layout

```
hybrid_kem/
├── hybrid_kem.py          # the hybrid KEM (two profiles)
├── kem_standard/          # ML-KEM (FIPS 203) via pyca/cryptography
├── kem_classical/         # X25519 leg (RFC 7748)
├── combiner/              # xwing.py (X-Wing) + kdf_combiner.py (BBF-G-S)
├── sig_standard/          # ML-DSA (FIPS 204) via pyca/cryptography
├── sig_classical/         # Ed25519 / Ed448 legs (RFC 8032)
├── sig_composite/         # composite ML-DSA + EdDSA (LAMPS draft-19)
├── protocols/             # authenticated_handshake.py (AKE over KEM + composite sig)
├── entropy/               # SP 800-90A DRBG, SP 800-90B health tests, QRNG
├── kem_slwe/              # research scheme — NOT on the KEM path
└── tests/                 # suite + tests/kat_vectors/ (published vectors)
```

## References

- FIPS 203 (ML-KEM): https://csrc.nist.gov/pubs/fips/203/final
- RFC 7748 (X25519): https://www.rfc-editor.org/rfc/rfc7748
- X-Wing: https://datatracker.ietf.org/doc/draft-connolly-cfrg-xwing-kem/
- FIPS 204 (ML-DSA): https://csrc.nist.gov/pubs/fips/204/final
- RFC 8032 (EdDSA): https://www.rfc-editor.org/rfc/rfc8032
- Composite ML-DSA: https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/
- BBF-G-S 2019 (KEM combiners): https://eprint.iacr.org/2018/903
- SP 800-90A (DRBGs): https://csrc.nist.gov/pubs/sp/800/90/a/r1/final
- SP 800-90B (entropy sources): https://csrc.nist.gov/pubs/sp/800/90/b/final

## History

The notice below was written on October 10, 2026, for the earlier SLWE-based README, which remains in git
history. It is kept as written. The SLWE note it cites was later revised as Zenodo
doi:10.5281/zenodo.23352161.

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

## Author

M. Gifford · 2026
