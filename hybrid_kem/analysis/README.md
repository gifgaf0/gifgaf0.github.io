# HYBRID-AKE — symbolic analysis (Tamarin)

Machine-checked symbolic analysis of the authenticated handshake specified in
`../docs/HYBRID_AKE_SPEC.md` and implemented in
`../protocols/authenticated_handshake.py`.

- `hybrid_ake.spthy` — the base Tamarin model (mutually-authenticated protocol).
- `hybrid_ake_ext.spthy` — the extended model: adds an **ephemeral-key-reveal**
  oracle and a **second ciphersuite** (see "Extended model" below).
- `Makefile` — `make prove` / `make prove-ext` to re-run; `make check` for
  well-formedness only.
- `prove_run.log`, `prove_ext_run.log` — captured output of the two proof runs.

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

## Extended model (`hybrid_ake_ext.spthy`)

The extended model gives the attacker two further capabilities and proves the
corresponding sharper properties. All lemmas **verified** (tamarin-prover 1.12.0
+ Maude 3.5.1, ~3.3 s):

| Lemma | Meaning | Result |
|---|---|---|
| `executable` | honest run agrees on a key | verified |
| `eph_reveal_breaks_session` | revealing a session's ephemeral *does* leak its key (the oracle has effect) | verified (exists-trace) |
| `key_secrecy` | key secret iff peer honest **and** that session's ephemeral not revealed | verified |
| `forward_secrecy` | secret under post-handshake long-term compromise, ephemeral not revealed | verified |
| `responder_auth_injective` | responder authentication — **holds even when ephemerals are revealed** | verified |
| `initiator_auth_injective` | initiator authentication — holds even with ephemeral reveal | verified |
| `suite_agreement` | with two suites offered, both parties complete on the *same* suite (downgrade resistance) | verified |

Two things this establishes beyond the base model:

1. **The ephemeral is load-bearing and the boundary is exactly right.**
   `eph_reveal_breaks_session` shows that leaking a session's ephemeral KEM
   secret breaks *that* session (expected: the attacker then decapsulates), and
   `key_secrecy` shows secrecy holds for every session whose ephemeral stayed
   secret. Forward secrecy is therefore with respect to long-term-key compromise,
   not ephemeral compromise.
2. **Authentication is robust to ephemeral leakage.** The two agreement lemmas
   do not exclude `EphReveal`, so authentication rests on the long-term composite
   signature alone — leaking ephemerals does not let the attacker impersonate.
3. **Downgrade resistance across suites.** With `'suiteA'` and `'suiteB'` both
   available and the suite malleable in the first message, a party only completes
   with the suite it chose; `suite_agreement` confirms the two honest parties
   never split across suites.

Ephemeral reveal here is the initiator's KEM ephemeral secret. Reveal of the
responder's one-time encapsulation coins (which would equal leaking the shared
secret directly) is not separately modelled.

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
In the base model, ephemeral-key-reveal is out of scope and a single ciphersuite
is used; the extended model (`hybrid_ake_ext.spthy`) adds both. Even there, the
primitives remain idealised (no computational proof), and reveal of the
responder's one-time encapsulation coins is not modelled.

## Reproduce

Install the two tools (official GitHub release binaries), then run:

```bash
# tamarin-prover 1.12.0 + maude 3.5.1 on PATH, MAUDE_LIB set to Maude's prelude dir
make prove        # proves all lemmas (~2 s)
```
