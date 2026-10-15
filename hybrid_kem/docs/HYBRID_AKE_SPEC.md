# HYBRID-AKE v1 — protocol specification

Status: engineering specification for the construction implemented in
`hybrid_kem/protocols/authenticated_handshake.py`. This is not an IETF document
and the protocol is not standardised. It reuses the design pattern of TLS 1.3 /
SIGMA with post-quantum-hybrid primitives, so that the construction can be
stated precisely and analysed (see `hybrid_kem/analysis/`).

## 1. Overview

HYBRID-AKE is a two-party authenticated key-exchange protocol. Two parties
establish a shared 32-byte session key. Confidentiality of the key comes from an
**ephemeral hybrid KEM** exchange; authentication comes from a **composite
signature** over the handshake transcript. It runs in two modes:

- **responder-authenticated** (two messages): the initiator learns it shares the
  key with a specific responder identity; the initiator is anonymous.
- **mutually authenticated** (three messages): both parties authenticate.

## 2. Primitives

| Symbol | Instantiation | Reference |
|---|---|---|
| `KEM` = (`KeyGen`, `Encaps`, `Decaps`) | HybridKEM profile (X-Wing, or ML-KEM-1024+X25519) | `hybrid_kem.py` |
| `Sig` = (`KeyGen`, `Sign`, `Verify`) | Composite ML-DSA + EdDSA | `sig_composite/` |
| `H` | SHA3-256 | FIPS 202 |
| `KDF` | HKDF-SHA256 | RFC 5869 |

`KEM.Encaps(pk) -> (ct, ss)` returns a ciphertext and a 32-byte shared secret;
`KEM.Decaps(sk, ct) -> ss`. `Sig.Sign(sk, m, ctx)` and `Sig.Verify(pk, sig, m,
ctx)` take a domain-separation context string.

## 3. Identities, keys, parameters

- Each authenticating party has a long-term composite signature key pair
  `(vk, sk)` and a human-readable `name`. `vk` is the authenticated identity; a
  verifier must obtain the peer's `vk` out of band (certificate, pinning, TOFU).
- The initiator generates a fresh **ephemeral** KEM key pair `(pk_e, sk_e)` per
  handshake and destroys `sk_e` immediately after deriving the session key.
- `SUITE_ID = "hybrid-ake/v1" ‖ " " ‖ kem_profile ‖ " " ‖ sig_profile` — a fixed
  byte string naming both chosen algorithms. Signing it binds the handshake to
  the suite (downgrade binding over the single offered suite).
- Context strings: `CTX_R = "hybrid-ake/responder-auth/v1"`,
  `CTX_I = "hybrid-ake/initiator-auth/v1"`, session-key label
  `INFO = "hybrid-ake/session-key/v1"`.

Notation: `LP(x1, ..., xn)` is the concatenation of each `xi` prefixed by its
4-byte big-endian length (an unambiguous encoding). `id_I`, `vk_I` are the
initiator's name and verification key (empty in responder-only mode); `id_R`,
`vk_R` the responder's.

## 4. Transcript and key schedule

The **transcript hash** is computed by both parties once `ct` is known:

```
TH = H( LP( SUITE_ID, id_I, vk_I, id_R, vk_R, pk_e, ct ) )
```

The **session key** is

```
K = KDF( ikm = ss, salt = TH, info = INFO ‖ " " ‖ SUITE_ID, L = 32 ).
```

Because `TH` is the HKDF salt, the two parties derive equal keys only if they
agree on the entire transcript; because `ss` is the HKDF input keying material,
`K` is secret whenever `ss` is.

## 5. Message flow

```
Initiator I                                           Responder R
  (pk_e, sk_e) <- KEM.KeyGen()
  --- msg1 = LP(SUITE_ID, id_I, vk_I, pk_e) -------------->
                                        check SUITE_ID matches
                                        (ct, ss) <- KEM.Encaps(pk_e)
                                        TH = H(LP(SUITE_ID,id_I,vk_I,id_R,vk_R,pk_e,ct))
                                        sig_R = Sig.Sign(sk_R, TH, CTX_R)
                                        K = KDF(ss; TH)
  <-- msg2 = LP(id_R, vk_R, ct, sig_R) --------------------
  ss = KEM.Decaps(sk_e, ct)
  TH = H(LP(SUITE_ID,id_I,vk_I,id_R,vk_R,pk_e,ct))
  require Sig.Verify(vk_R, sig_R, TH, CTX_R)      <-- abort if false
  K = KDF(ss; TH)
  [mutual] sig_I = Sig.Sign(sk_I, H(LP(TH, sig_R)), CTX_I)
  --- msg3 = LP(sig_I) ----------------------------------->   [mutual]
                                        require Sig.Verify(vk_I, sig_I, H(LP(TH,sig_R)), CTX_I)
```

**Acceptance rules.** The initiator outputs `K` only if `Sig.Verify(vk_R, sig_R,
TH, CTX_R)` holds; otherwise it aborts (no key). In mutual mode the responder
outputs `K` to the application only after `Sig.Verify(vk_I, ...)` holds. The
initiator binds its own signature to `sig_R` (via `H(LP(TH, sig_R))`) so it
cannot be replayed into another handshake.

## 6. Threat model

Dolev–Yao network attacker: it controls all messages (read, drop, inject,
reorder, replay), may run any number of concurrent sessions in either role, and
may register its own identities. It may **compromise** the long-term signing key
of any party (adaptively). Cryptographic primitives are idealised (symbolic): the
KEM reveals nothing about `ss` without `sk_e`; signatures are existentially
unforgeable; `H`, `KDF` are one-way and collision-free. The ephemeral `sk_e` is
not revealed (no separate ephemeral-key-reveal oracle is modelled).

## 7. Security goals

Stated for the mutual protocol; the responder-authenticated protocol provides
G1–G4 (no initiator authentication, G5 absent).

- **G1 — Session-key secrecy.** If an honest initiator completes a handshake
  with an honest responder (peer's long-term key uncompromised), the session key
  is unknown to the attacker.
- **G2 — Forward secrecy.** G1 holds even if the long-term signing keys of both
  parties are compromised *after* the handshake completes. (The key depends only
  on the ephemeral KEM exchange, not on any long-term secret.)
- **G3 — Responder authentication (injective agreement).** If an honest
  initiator completes with peer identity `vk_R` and `vk_R` is uncompromised, then
  the holder of `vk_R` ran the responder role with the *same* transcript `TH` and
  session key `K`, and distinct initiator completions correspond to distinct
  responder runs (no replay).
- **G4 — Transcript / key agreement.** Both parties that complete agree on `TH`,
  `K`, the suite, and both identities.
- **G5 — Initiator authentication (mutual mode, injective agreement).**
  Symmetric to G3 for the responder's view of the initiator.
- **Downgrade binding.** A signature over `TH` commits to `SUITE_ID`; a party
  will not complete a handshake whose suite differs from the one it signed.

**Hybrid robustness (primitive level, not re-proven by the handshake analysis).**
Because the KEM is a hybrid (ML-KEM + X25519) and the signature is composite
(ML-DSA + EdDSA, both required to verify), G1–G2 hold as long as *either* KEM
component is secure, and G3/G5 hold as long as *either* signature component is
unforgeable. The symbolic analysis abstracts each hybrid primitive as a single
idealised primitive and therefore establishes the handshake-level goals assuming
the primitive meets its stated (hybrid) security; it does not re-derive the
hybrid robustness of the primitives themselves.

## 8. Non-goals and limitations

- Not a standardised or formally reviewed protocol; no computational proof. For
  production, use TLS 1.3 with a hybrid group from a maintained library.
- No negotiation: exactly one suite per handshake (named in `SUITE_ID`).
- No 0-RTT, no session resumption, no re-keying, no record layer.
- No protection against ephemeral-key compromise (not modelled); forward secrecy
  is with respect to long-term-key compromise only.
- Identity binding is only as good as the out-of-band distribution of `vk`.
- Denial of service is out of scope (KEM/signature work is done before
  authentication in responder-only mode).

## 9. Symbolic analysis

A Tamarin model of this specification and the machine-checked results for
G1–G5 and downgrade binding are in `hybrid_kem/analysis/` (`hybrid_ake.spthy`,
`RESULTS.md`).
