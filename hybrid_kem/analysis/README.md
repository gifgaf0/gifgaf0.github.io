# HYBRID-AKE — symbolic analysis (Tamarin)

Machine-checked symbolic analysis of the authenticated handshake specified in
`../docs/HYBRID_AKE_SPEC.md` and implemented in
`../protocols/authenticated_handshake.py`.

- `hybrid_ake.spthy` — the Tamarin model (mutually-authenticated protocol).
- `Makefile` — `make prove` to re-run; `make check` for well-formedness only.
- `prove_run.log` — captured output of the proof run below.

## Result

All lemmas were **verified** (no attack exists in the model), with
`tamarin-prover 1.12.0` + `Maude 3.5.1`:

| Lemma | Goal (spec §7) | Result |
|---|---|---|
| `executable` | sanity: an honest mutual run reaching agreement exists | verified |
| `key_secrecy` | G1 session-key secrecy (honest peer) | verified |
| `forward_secrecy` | G2 secrecy under long-term compromise *after* the handshake | verified |
| `responder_auth_injective` | G3 responder authentication, injective agreement on (transcript, key) | verified |
| `initiator_auth_injective` | G5 initiator authentication (mutual), injective agreement | verified |

```
  executable (exists-trace): verified (10 steps)
  key_secrecy (all-traces): verified (13 steps)
  forward_secrecy (all-traces): verified (13 steps)
  responder_auth_injective (all-traces): verified (15 steps)
  initiator_auth_injective (all-traces): verified (10 steps)
  processing time: 1.39s
```

`executable` is an `exists-trace` lemma: it confirms the model is not vacuous
(an honest run does reach mutual agreement on one key). The agreement lemmas had
teeth — an earlier version with an under-specified honest-peer premise was
*falsified* by Tamarin (the attacker fabricated a responder key `pk(c)` from a
public constant and signed the transcript itself); constraining the peer to a
genuinely registered identity closed that gap.

Transcript / key agreement (G4) and downgrade binding follow from the injective
agreement lemmas: both parties agree on the full transcript hash `TH`, which
contains the session key material and the suite identifier.

## Threat model in the model

Dolev–Yao attacker controlling the network, running unboundedly many concurrent
sessions in either role, registering its own identities, and **adaptively
compromising any party's long-term signing key** (`Reveal_ltk`). The ephemeral
KEM secret is not revealed.

## Abstractions (what "verified" does and does not cover)

Symbolic, perfect-cryptography model. In particular:

- The **hybrid KEM** is one idealised KEM: the encapsulator binds a fresh shared
  secret into the ciphertext and only the ephemeral-secret holder recovers it
  (`decap(k, encap(kempk(k), m)) = m`). This captures "the shared secret is
  secret unless the ephemeral secret key is known", which is the IND-CCA KEM
  abstraction.
- The **composite signature** is one idealised EUF-CMA signature (Tamarin's
  `signing` builtin).
- `H` (SHA3-256) and `KDF` (HKDF) are free, one-way, collision-free functions.

Therefore the analysis establishes the **handshake-level** goals *assuming the
primitives meet their stated security*. It does not re-derive the hybrid
robustness of the primitives themselves — that each is secure as long as either
component is — which is a property of the KEM / composite-signature
constructions (argued in the spec), nor does it provide a computational proof.
Ephemeral-key-reveal (and hence forward secrecy against ephemeral compromise) is
out of scope. A single ciphersuite is modelled, so downgrade binding is checked
only in the sense of transcript-agreement on the suite tag, not across two
concurrently-offered suites.

## Reproduce

Install the two tools (official GitHub release binaries), then run:

```bash
# tamarin-prover 1.12.0 + maude 3.5.1 on PATH, MAUDE_LIB set to Maude's prelude dir
make prove        # proves all lemmas (~2 s)
```
