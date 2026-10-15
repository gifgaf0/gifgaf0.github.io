# HYBRID-AKE v1 — computational security analysis

A reduction-based (game-hopping) analysis of the handshake specified in
`HYBRID_AKE_SPEC.md`. It reduces the protocol's security to standard
computational assumptions on its primitives, and — via two hybrid-robustness
lemmas — to the security of the underlying ML-KEM / X25519 / ML-DSA / Ed25519.
This complements the symbolic (Tamarin) analysis in `../analysis/`, which works
in the perfect-cryptography model; here the primitives are real and the
guarantees are quantitative.

**Status and honesty.** This is a detailed proof *sketch* at the level of rigour
of a protocol paper's body, not a fully formalised or machine-checked proof. A
mechanized computational proof (CryptoVerif) is the natural next step; its
tooling was not installable in the build environment (the CryptoVerif
distribution host is unreachable through the network allowlist), so it is left
as future work. Numerical constants in the bounds are the usual
loss factors; they are stated to show the shape of the reduction, not tuned.

> **Update (October 15, 2026).** The CryptoVerif mechanization is done:
> `../analysis/cryptoverif/` machine-checks Theorems 1–2 and Lemmas 1–2
> (CryptoVerif 2.13). It also **corrects** two statements of this sketch — Lemma 2
> needs collision resistance of the composite pre-hash, and Lemma 1 for X-Wing
> needs ML-KEM's C2PRI when relying on X25519 — and gives a tighter Theorem 2
> bound. The original text below is kept as written; corrected statements are
> marked ⚠ and the corrections are in §7.

---

## 1. Primitives and assumptions

Let `λ` be the security parameter. The protocol uses:

- a key-encapsulation mechanism `KEM = (KGen, Encaps, Decaps)`, `δ`-correct;
- a signature scheme `Sig = (SKGen, Sign, Verify)` (the composite);
- `H = SHA3-256`, modelled as collision-resistant;
- `KDF = HKDF-SHA256`.

**Definition 1 (IND-CCA KEM).** For adversary `A`,
`Adv^{ind-cca}_{KEM}(A) = |Pr[IND-CCA^A ⇒ 1] − 1/2|`, in the standard game: `A`
gets `pk`, a challenge `(ct*, K_b)` with `K_0 = Decaps(sk, ct*)` the real key and
`K_1` uniform, and a decapsulation oracle on any `ct ≠ ct*`. Because each
protocol ephemeral key is used for **exactly one** decapsulation (the initiator
decapsulates the single ciphertext it receives), IND-1CCA — one decapsulation
query — already suffices; IND-CCA (which ML-KEM targets) implies it.

**Definition 2 (EUF-CMA signature).**
`Adv^{euf-cma}_{Sig}(A)` is `A`'s probability of producing `(m*, σ*)` with
`Verify(vk, σ*, m*) = 1` and `m*` never queried to the signing oracle.

**Definition 3 (KDF as a PRF).** `KDF(k; ·)` keyed by its input-keying-material
`k` is a pseudorandom function: for uniform `k`,
`Adv^{prf}_{KDF}(A) = |Pr[A^{KDF(k;·)} ⇒ 1] − Pr[A^{RF(·)} ⇒ 1]|` is small. For
HKDF this follows from HMAC-SHA256 being a (dual-)PRF [Kra10]; the per-session
salt `TH` is public and distinct per session, which is the regime HKDF targets.

### Hybrid-robustness lemmas

These make precise the claim the symbolic model abstracted: each hybrid
primitive is secure if **either** of its components is.

**Lemma 1 (hybrid KEM).** ⚠ *Refined in §7: the X25519 assumption differs per
profile, and X-Wing's X25519 direction also needs C2PRI of ML-KEM.* The hybrid KEM (X-Wing = ML-KEM-768 + X25519 with the
SHA3-256 combiner, or ML-KEM-1024 + X25519 with the BBF-GS transcript-binding
combiner) is IND-CCA if *either* component is secure:
`Adv^{ind-cca}_{KEM} ≤ min( Adv^{ind-cca}_{ML-KEM}, Adv^{dh}_{X25519} ) + ε_comb`,
where `ε_comb` is the combiner's statistical / PRF loss. For X-Wing this is the
content of its security analysis [XWing, GHP18, BBFGS19]; the combiner is a
dual-PRF so breaking the KEM requires breaking both legs.

**Lemma 2 (composite signature).** ⚠ *Corrected in §7: the bound is missing
`+ 2·Adv^cr_PH`.* The composite signature (`σ = (σ_1, σ_2)`,
both required to verify) is EUF-CMA if *either* component is EUF-CMA:
`Adv^{euf-cma}_{Sig} ≤ min( Adv^{euf-cma}_{ML-DSA}, Adv^{euf-cma}_{Ed} )`.
*Proof.* A composite forgery on a fresh `m*` is a pair `(σ_1*, σ_2*)` that both
verify; in particular each `σ_i*` is a valid component signature on `m*`, which
was never a component-signing query (the composite signer signs `m*` under both
only when asked to sign `m*`). So a composite forger yields a forger against
*each* component; whichever component is unforgeable bounds it. ∎ (See also the
composite-sigs draft security considerations and [BBFGS19] for signature
combiners.)

Under Lemmas 1–2, every bound below in terms of `Adv^{ind-cca}_{KEM}` and
`Adv^{euf-cma}_{Sig}` is also a bound in terms of the *better* of the two KEM
legs and the *better* of the two signature components — i.e. the protocol is
secure as long as, in each hybrid, at least one component stands.

---

## 2. Execution model

A Bellare–Rogaway-style model [BR93, CK01]. `n_P` parties each hold a long-term
`Sig` key pair; `n_S` sessions run. A session `π` at a party has local state
(role, intended/learned peer, ephemeral key, transcript, status ∈
{running, accepted, rejected}, session key). The adversary `A` is the network
and makes queries:

- `Send(π, m)` — deliver `m` to `π`, get its reply; `A` schedules everything.
- `Corrupt(P)` — get `P`'s long-term signing key (records time; enables
  adaptive and forward-secrecy reasoning).
- `RevealEph(π)` — get the ephemeral KEM secret of initiator session `π`.
- `RevealKey(π)` — get an accepted session's key.
- `Test(π)` — once, on an accepted session: return `K_π` (real) or uniform,
  per a secret bit `b`.

**Partnering.** The session identifier is `sid = TH` (the transcript hash). Two
sessions are *partners* iff they hold equal `sid` with opposite roles. By
correctness, partners derive equal `K`.

**Freshness (for `Test(π)`).** `π` is fresh if: (i) neither `π` nor its partner
was `RevealKey`-ed; (ii) `RevealEph(π)` was not called, nor `RevealEph` on its
partner-initiator; and (iii) the peer was not `Corrupt`-ed **before** `π`
accepted (corruption afterwards is allowed — this is the forward-secrecy
clause). `Adv^{ki} = |Pr[b' = b] − 1/2|` over fresh Test sessions.

Two goals: **entity authentication / key agreement** (§3) and **key
indistinguishability** (§4).

---

## 3. Theorem 1 — authentication and agreement

**Theorem 1.** For any efficient `A`,
```
Adv^{auth}(A) ≤ Adv^{euf-cma}_{Sig}(B1) + Adv^{cr}_{H}(B2) + n_S^2 · δ,
```
where `Adv^{auth}` is the probability that some session `π` accepts with an
uncorrupted-at-acceptance peer but has **no** unique partner session with
matching `sid` and `K`.

*Proof (games).*

- **G0**: the real authentication game.
- **G1**: abort if any session accepts a component against an honest peer `vk`
  whose signature was not produced by a session of the peer. Concretely, an
  initiator accepts only if `Verify(vk_R, σ_R, TH, CTX_R)=1`; a responder accepts
  (mutual) only if `Verify(vk_I, H(TH,σ_R), CTX_I)=1`. We bound the event that
  such a `σ` verifies on a `TH`/`H(TH,σ_R)` value that no honest peer session
  signed. Reduction `B1` to EUF-CMA: `B1` plants the challenge `vk` at a guessed
  honest party, answers that party's signatures with its signing oracle, and
  outputs the first accepted signature on an unsigned message as a forgery. The
  context strings `CTX_R ≠ CTX_I` are part of the signed message, so a responder
  signature can never be replayed as an initiator signature or vice versa.
  `Pr[G0 ⇒ 1] − Pr[G1 ⇒ 1] ≤ Adv^{euf-cma}_{Sig}(B1)`.
- **G2**: in `G1`, every accepting session's signature was produced by an honest
  peer session on the *same* `TH`. Since `TH = H(SUITE, id_I, vk_I, id_R, vk_R,
  pk_e, ct)`, agreement on `TH` implies agreement on all of these unless two
  distinct inputs collide under `H`; charge `Adv^{cr}_H(B2)`. Equal inputs ⇒ same
  `pk_e, ct` ⇒ (by `δ`-correctness, losing `n_S^2·δ`) same `ss` ⇒ same
  `K = KDF(ss; TH)`. So the two sessions are partners and agree on the key.
- **Injectivity (no replay).** A second session accepting the *same* `sid=TH`
  would share the initiator's `pk_e`, which is sampled freshly per initiator
  session; two initiator sessions with the same `pk_e` occur only on a KEM
  key-generation collision, already inside the `H`/correctness terms. Hence the
  partner is unique. ∎

Theorem 1 gives responder-to-initiator authentication (two-message mode) and, in
mutual mode, additionally initiator-to-responder authentication; the two use the
two context strings and the `H(TH,σ_R)` binding of `msg3` so that `σ_I` is tied
to this exact handshake and cannot be replayed.

---

## 4. Theorem 2 — key indistinguishability (with forward secrecy)

**Theorem 2.** For any efficient `A`,
```
Adv^{ki}(A) ≤ Adv^{auth}(A) + n_S^2 · ( Adv^{ind-cca}_{KEM}(B3) + Adv^{prf}_{KDF}(B4) ) + n_S^2·δ.
```

*Proof (games).*

- **G0**: the real KI game with the `Test` query.
- **G1 (single session).** Guess the `Test` session `π` and, by Theorem 1, its
  unique honest partner. Incorrect guess ⇒ abort. Loss `≤ n_S^2`. From here one
  fixed fresh session pair with ephemeral public key `pk_e`, ciphertext `ct`,
  shared secret `ss`, transcript `TH`, key `K = KDF(ss; TH)`.
- **G2 (authenticated transcript).** By Theorem 1 the partner is an honest
  responder session that ran `Encaps(pk_e) → (ct, ss)` for *this* `pk_e`; if no
  such partner exists, abort — bounded by `Adv^{auth}(A)`. Crucially, the `ss`
  underlying the Test key is the output of an honest encapsulation to the Test
  session's own honest ephemeral key. The ephemeral secret `sk_e` is not revealed
  (freshness), and long-term keys play no role in producing `ss`.
- **G3 (idealise the KEM).** Replace `ss` by a uniform `ss*`. Reduction `B3` to
  IND-CCA: `B3` receives `(pk*, ct*, K_b)`, uses `pk*` as the Test session's
  `pk_e` and `ct*` as the received `ct`, and sets the pre-key to `K_b`. The single
  decapsulation the initiator would perform is answered by `K_b` (for the honest
  `ct*`) or, for any *other* ciphertext an adversary delivers to this ephemeral
  key, by the CCA decapsulation oracle (`ct ≠ ct*`). Long-term keys are chosen by
  `B3`, so *all* `Corrupt` queries — including those **after** acceptance — are
  answered honestly; this is exactly why forward secrecy holds: the hop does not
  rely on any long-term secret staying hidden. `K_0` = real ⇒ `G2`; `K_1` = uniform
  ⇒ `G3`. Gap `≤ Adv^{ind-cca}_{KEM}(B3)` per session, `n_S^2` with the guess.
- **G4 (idealise the KDF).** Now `K = KDF(ss*; TH, INFO‖SUITE)` with `ss*` uniform.
  Replace `KDF(ss*; ·)` by a random function (`B4`, PRF). Then `K` is uniform and
  independent of the transcript and of `b`. Gap `≤ Adv^{prf}_{KDF}(B4)`.
- In `G4` the Test key is uniform regardless of `b`, so `A`'s advantage is 0.
  Collecting the hops gives the bound. ∎

**Why forward secrecy.** The only hop touching confidentiality (G3) reduces to
the KEM and is simulated with all long-term keys known to the reduction;
therefore corrupting long-term signing keys after the Test session accepted
gives the adversary nothing about `K`. Forward secrecy is thus w.r.t. long-term
compromise. It is **not** claimed against ephemeral compromise: `RevealEph` on
the Test session is excluded by freshness, matching the symbolic result
(`analysis/hybrid_ake_ext.spthy`), where revealing a session's ephemeral is shown
to break exactly that session's key and nothing else.

---

## 5. Concrete statement over the real primitives

⚠ *This substitutes Lemmas 1–2 as originally stated; with the corrected
lemmas of §7 add `2·Adv^cr_PH` to the signature term and, for X-Wing, the C2PRI
term to the X25519 alternative. §7 also gives the tighter mechanized bound.*

Substituting Lemmas 1–2:
```
Adv^{ki}(A) ⪅ n_S^2 · [ min(Adv^{ind-cca}_{ML-KEM}, Adv^{dh}_{X25519}) + ε_comb
                        + min(Adv^{euf-cma}_{ML-DSA}, Adv^{euf-cma}_{Ed25519})
                        + Adv^{prf}_{HKDF} ]
              + Adv^{cr}_{SHA3-256} + n_S^2·δ.
```
So HYBRID-AKE provides authenticated, forward-secret session keys as long as, in
the KEM, at least one of ML-KEM / X25519 is secure, **and**, in the signature, at
least one of ML-DSA / Ed25519 is unforgeable — the intended post-quantum/classical
hybrid guarantee, now at the computational level rather than only symbolically.

---

## 6. Gaps, caveats, and what a mechanized proof would add

- **Sketch, not a formal proof.** The game hops are standard but written at
  paper-body rigour. A CryptoVerif development would discharge the PRF/IND-CCA
  rewrites and the multi-session bookkeeping mechanically and remove the `n_S^2`
  guessing via its built-in session reasoning; it is the recommended next step.
  *(Done October 15, 2026; see §7.)*
- **Model choice.** A BR-style model is used; a Canetti–Krawczyk or eCK model
  (with session-state reveal) would be stronger. The present freshness forbids
  ephemeral reveal of the Test session, so no eCK-style key-compromise-
  impersonation claim is made.
- **KDF idealisation.** HKDF is treated as a PRF keyed by `ss`. An alternative
  is the random-oracle model for `H`/`KDF`, which would also absorb the
  collision term; the PRF route keeps the standard model except for `H`'s
  collision resistance.
- **KEM assumption strength.** IND-1CCA suffices here (one decapsulation per
  ephemeral key); we assume IND-CCA, which ML-KEM provides, so this is slack in
  our favour.
- **Not covered.** Denial of service, side channels, implementation-level
  concerns (constant-time, nonce handling), and the responder's one-time
  encapsulation-coin compromise (equivalent to leaking `ss`).

For production, prefer TLS 1.3 with a standardised hybrid group and a reviewed
implementation; this analysis is for the research construction in this package.

---

## 7. Mechanization (CryptoVerif) and corrections — October 15, 2026

All four claims above are machine-checked with CryptoVerif 2.13 in
`../analysis/cryptoverif/` (models, proof scripts, bounds in `RESULTS.txt`,
mutation tests; `README.md` there has the details). The protocol and the
post-quantum legs are checked with CryptoVerif's post-quantum-sound library.

**Theorem 1** — proved as two injective correspondences (responder and, in
mutual mode, initiator authentication), each agreeing on the whole transcript
(both identities, `pk_e`, `ct`, and `sig_R` for the initiator) and on the key,
for `NK` honest parties running any number of sessions in both roles and both
modes, with adaptive corruption of every long-term key.
Bound: `NK·Adv^euf-cma_Sig + O(1)·Adv^cr_H + collisions`.

**Theorem 2** — proved as real-or-random secrecy of all keys of sessions whose
peer was honest and uncorrupted at acceptance (initiators, and mutual-mode
responders), with corruption at any time afterwards and of the session's own
key at any time (forward secrecy; resistance to key-compromise impersonation of
the long-term key). A second model adds ephemeral-key reveal on sessions the
adversary chooses; everything still holds, with the freshness clause (ii) above
shown necessary (mutation test). Bound:

```
Adv^ki ≤ 2·Adv^ind-cca_KEM(multi-instance) + 2·NK·Adv^euf-cma_Sig
         + 2·(#encapsulations)·Adv^prf_KDF + O(1)·Adv^cr_H + collisions
```

There is no session-guessing loss, so the `n_S^2` factors of §4–§5 are an
artefact of the sketch's proof strategy, not of the protocol.

**Lemma 2 — corrected.** The components sign `M' = Prefix ‖ Label ‖ len(ctx) ‖
ctx ‖ PH(M)`, so a composite forgery on a fresh `M` is a component forgery only
when `PH(M)` is also fresh. The proof of Lemma 2 above omits this step. The
correct statement is

```
Adv^euf-cma_Sig ≤ min(Adv^euf-cma_ML-DSA, Adv^euf-cma_Ed) + 2·Adv^cr_PH
```

with `PH` = SHA-512 (`id-MLDSA65-Ed25519-SHA512`) or SHAKE256/64
(`id-MLDSA87-Ed448-SHAKE256`). Without collision resistance of `PH` the proof
fails, and a `PH` collision would transfer a signature between messages.

**Lemma 1 — refined, per profile and per leg.** Each statement below is proved
as the exact IND-CCA2 equivalence the protocol model assumes, with the other
leg's secret key given to the adversary:

| Profile | Relying on ML-KEM | Relying on X25519 |
|---|---|---|
| `mlkem1024+x25519` (BBF-G-S HKDF combiner) | ML-KEM-1024 IND-CCA2 + HKDF a PRF keyed by `ss_M` | PRF-ODH for HKDF keyed by `ss_X` (standard model) |
| `xwing` (SHA3-256 combiner) | ML-KEM-768 IND-CCA2 + SHA3-256 a PRF keyed by `ss_M` | strong DH + SHA3-256 as a random oracle **+ C2PRI of ML-KEM-768** |

The last cell is the correction. X-Wing does not hash `ct_M`; if ML-KEM were
broken including its ciphertext binding, a second ciphertext decapsulating to
the same `ss_M` would decapsulate the whole hybrid to the challenge key. These
are exactly the X-Wing paper's assumptions (its classical theorem uses C2PRI),
and that paper proves C2PRI for ML-KEM-768 from its hash functions alone, so the
X-Wing guarantee still survives a break of the lattice problem — but the
"either leg" claim is not symmetric, and the bound in Lemma 1 should read

```
Adv^ind-cca_X-Wing ≤ min(Adv^ind-cca_ML-KEM + Adv^prf_SHA3,
                         Adv^sdh_X25519 + Adv^c2pri_ML-KEM)       (up to the stated factors)
```

**Design elements the proofs depend on** (mutation tests): `ct` in `TH` (or a
man in the middle swaps it), and `vk_R` in `TH` (or initiator authentication
fails by unknown key share). The two context strings are a second layer of role
separation: the proofs still go through without them, because the two signed
hash inputs already have different field counts, and fail only when both
separations are removed.

**Not mechanized.** The composition of the hybrid-primitive results (Lemmas 1–2)
into the protocol bound is the standard substitution, done by hand. Modelling
choices that limit the statement are listed in the CryptoVerif README: one
ciphersuite, static ephemeral reveal, perfect KEM correctness, X25519 as a
prime-order group, and keys of potentially partnered sessions withheld rather
than revealed.

---

## References

- [BR93] Bellare, Rogaway. *Entity Authentication and Key Distribution.* CRYPTO 1993.
- [CK01] Canetti, Krawczyk. *Analysis of Key-Exchange Protocols and Their Use for Building Secure Channels.* EUROCRYPT 2001.
- [Kra03] Krawczyk. *SIGMA: The 'SIGn-and-MAc' Approach to Authenticated Diffie–Hellman.* CRYPTO 2003.
- [Kra10] Krawczyk. *Cryptographic Extraction and Key Derivation: The HKDF Scheme.* CRYPTO 2010.
- [GHP18] Giacon, Heuer, Poettering. *KEM Combiners.* PKC 2018.
- [BBFGS19] Bindel, Brendel, Fischlin, Goncalves, Stebila. *Hybrid Key Encapsulation Mechanisms and Authenticated Key Exchange.* PQCrypto 2019.
- [DFGS21] Dowling, Fischlin, Günther, Stebila. *A Cryptographic Analysis of the TLS 1.3 Handshake Protocol.* J. Cryptology 2021.
- [SSW20] Schwabe, Stebila, Wiggers. *Post-Quantum TLS Without Handshake Signatures (KEMTLS).* ACM CCS 2020.
- [XWing] Connolly, Schwabe, Westerbaan et al. *X-Wing: The Hybrid KEM You've Been Looking For* / `draft-connolly-cfrg-xwing-kem`.
- FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), RFC 7748 (X25519), RFC 8032 (EdDSA),
  `draft-ietf-lamps-pq-composite-sigs` (composite signatures).

*Reference details (authors, venues, years) should be verified against the
primary sources before any external use.*
