# HYBRID-AKE — computational analysis (CryptoVerif)

Machine-checked computational proofs of the claims in
`../../docs/HYBRID_AKE_COMPUTATIONAL.md` (Theorems 1–2, Lemmas 1–2), for the
protocol of `../../docs/HYBRID_AKE_SPEC.md` as implemented in
`../../protocols/authenticated_handshake.py`. Checked with
**CryptoVerif 2.13** (Blanchet et al., Inria). Where the symbolic Tamarin models
in `..` treat the primitives as perfect, these models give the primitives only
computational assumptions, named precisely below, and produce explicit
probability bounds.

These results were revised after an independent post-merge review; see
[Review history](#review-history).

## Result

Every query below is **proved** (`make` re-runs all nine models in about 12
seconds on two cores; every bound is in `RESULTS.txt`).

| Model | Paper claim | What is proved | Assumptions | Library |
|---|---|---|---|---|
| `hybrid_ake.ocv` | Thm 1 (G3, G4) | responder authentication: injective agreement on the full transcript (both identities, `pk_e`, `ct`) and the key | KEM IND-CCA2 (multi-instance); signature UF-CMA with corruption; `H` collision resistant; KDF a PRF keyed by `ss` (HMAC swap-PRF) | pq |
|  | Thm 1 (G5, G4) | initiator authentication (mutual mode): injective agreement, including `sig_R` | same | pq |
|  | Thm 2 (G1, G2) | per-role real-or-random secrecy, with many test queries, of all fresh initiator keys and of all fresh mutual-responder keys, under adaptive corruption and RevealKey (see [Freshness](#freshness-and-revealkey)) | same | pq |
|  | — | cross-role key uniqueness: an accepting initiator and an accepting responder hold the same key only for the same transcript | same | pq |
| `hybrid_ake_ephleak.ocv` | Thm 1–2 with RevealEph | all of the above (uniqueness for fresh keys) when the adversary also learns the ephemeral secret of sessions it picks when they start (**static** RevealEph) | same | pq |
| `composite_sig.m4.ocv` `MLDSA_SECURE` | Lemma 2 | composite EUF-CMA, EdDSA fully broken | ML-DSA UF-CMA; pre-hash `PH` collision resistant | pq |
| `composite_sig.m4.ocv` `EDDSA_SECURE` | Lemma 2 | composite EUF-CMA, ML-DSA fully broken | EdDSA UF-CMA; `PH` collision resistant | pq |
| `kem_bbfgs.m4.ocv` `MLKEM_SECURE` | Lemma 1 | `mlkem1024+x25519` is IND-CCA2, X25519 fully broken | ML-KEM-1024 IND-CCA2; HKDF a PRF keyed by the `ss_M` half of its ikm (**split-key**, see [Assumptions](#assumptions-stated-precisely)) | pq |
| `kem_bbfgs.m4.ocv` `X25519_SECURE` | Lemma 1 | `mlkem1024+x25519` is IND-CCA2, ML-KEM fully broken | **PRF-ODH variant**: HKDF keyed by the DH value `ss_X`, the second half of its ikm (standard model) | default |
| `kem_bbfgs_x25519_rom.ocv` | Lemma 1 | the same, by a second route | strong DH; HKDF a random oracle — standard assumptions, no binding property of ML-KEM | default |
| `kem_xwing.m4.ocv` `MLKEM_SECURE` | Lemma 1 | X-Wing is IND-CCA2, X25519 fully broken | ML-KEM-768 IND-CCA2; SHA3-256 a PRF keyed by `ss_M` | pq |
| `kem_xwing.m4.ocv` `X25519_SECURE` | Lemma 1 | X-Wing is IND-CCA2, ML-KEM broken except for C2PRI | strong DH; SHA3-256 a random oracle; ML-KEM C2PRI — the X-Wing paper's assumptions, with X25519 a prime-order group instead of the paper's nominal group | default |

"Fully broken" means the adversary is handed that component's secret key at the
start. "pq" is CryptoVerif's post-quantum library (`-lib pq`), which contains only
assumptions known to have instantiations against quantum adversaries (no random
oracles, no Diffie–Hellman assumptions); a proof that uses only it is
post-quantum sound [BJ24]. The macros used from it are identical in the default
library. The X25519 directions are classical by nature.

## How the pieces compose (by hand)

CryptoVerif proves each model separately. Combining them into one bound for
the deployed protocol takes these steps, which are standard but **not**
mechanized:

1. **KEM.** Each KEM model proves the `ind_cca2` equivalence of CryptoVerif's
   `IND_CCA2_KEM` macro — the assumption the protocol model makes — for the
   hybrid KEM, up to presentation: users are created by an `Osetup` oracle with a
   pair of seeds `(sM, x)`, an extra oracle `Oleak` hands out the broken leg's
   key, and the random-oracle models add the oracle and its key on both sides.
   None of these weakens the substitution of a KEM bound for `Pkemcca`.
2. **Signature.** The composite model proves single-key EUF-CMA; the protocol uses
   CryptoVerif's multi-key UF-CMA-with-corruption macro, whose bound is
   `NK · Psign(single key)`.
3. **KEM side conditions.** The protocol model also uses the KEM macro's
   perfect-correctness equation and its collision statements for honestly
   generated keys and ciphertexts (`Pkemkeycoll`, `Pkemctxtcoll`). No KEM file
   proves these. The collision statements hold statistically for the hybrid,
   because every honest key and ciphertext contains a fresh X25519 point.
   Correctness costs ML-KEM's decapsulation failure rate per decapsulation:
   2^-164.8 for ML-KEM-768 and 2^-174.8 for ML-KEM-1024 (FIPS 203, Table 1).
4. **One hash, several idealisations.** SHA3-256 is a collision-resistant hash
   (transcript), a PRF (X-Wing, ML-KEM direction) and a random oracle (X-Wing,
   X25519 direction), in different files. This is sound only because their
   inputs have disjoint lengths: the transcript input is several kilobytes
   (it holds at least one composite verification key, a hybrid public key and a
   hybrid ciphertext), the msg3 input holds a composite signature (over 3 KB),
   and the X-Wing combiner input is 134 bytes. That argument is by hand.

## The bounds

Notation: `Pkemcca`, `Psign`, `Pprf`, `Phash` are the adversary's advantages
against the KEM, signature, KDF and transcript hash; `#O` counts calls to oracle
`O` (`#OI1` initiator sessions, `#OR1` mutual-responder sessions, `#OA1`
responder-only sessions, `#OI2` decapsulations); `NK` honest parties; `N*`
are per-party session caps. The `P*coll` terms are collisions between honestly
generated keys or ciphertexts (negligible). `RESULTS.txt` has every term.

**Theorem 2** (key secrecy, each of `keyI` and `keyR`; `hybrid_ake.ocv`):

```
Adv ≤ 2·Pkemcca(t, #OI1, #OA1 + #OR1, #OI2)        multi-key, multi-challenge IND-CCA2
    + 2·NK·Psign(t, NI + NR + NRa)                  UF-CMA with corruption, NK keys
    + 2·(#OR1 + #OA1)·Pprf(t, 2)                    one PRF key per encapsulation
    + 24·Phash(t)  +  collision terms
```

**Theorem 1** (each agreement query): `NK·Psign(t, NI + NR + NRa) + 6·Phash(t)` +
collision terms. **Key uniqueness:** about half the Theorem 2 bound (each
assumption term once instead of twice), plus
`(2·#OI2·#OR1 + #OA2·#OR1 + #OR1²/2) / |sesskey|`.

**On tightness.** The proof has no session-guessing step, but that does not make
the bound tighter than the sketch's `n_S²` in the usual sense. The KEM term is a
*multi-key, multi-challenge* advantage: `#OI1` keys and up to `#OR1 + #OA1`
challenges, since one msg1 can be delivered to every responder. The generic
reduction to single-key, single-challenge IND-CCA2 loses a factor of about
keys × challenges [BBM00], i.e. `#OI1 · (#OR1 + #OA1) ≈ n_S²`, the same order as
the sketch. What is better than the sketch is that the signature term is
`NK·Psign` (not `n_S²·Psign`) and the PRF term is linear in the sessions. A
tighter overall bound would need a tight multi-user bound for the KEM, which is
not claimed here.

**Lemma 2** (composite signature): `PsignM(t, NS) + 2·Phash(t)` with EdDSA broken,
and `PsignT(t, NS) + 2·Phash(t)` with ML-DSA broken. Hence
`Adv^euf-cma_composite ≤ min(Adv_ML-DSA, Adv_EdDSA) + 2·Adv^cr_PH`.

**Lemma 1** (hybrid KEM, `N` users, `Qe` encapsulations, `#ODecap` decapsulations):

| Profile / leg relied on | Bound |
|---|---|
| `mlkem1024+x25519`, ML-KEM | `2·Pmcca(t, N, Qe, #ODecap) + 4·Qe·Pprf(t, Qd+1)` + collisions |
| `mlkem1024+x25519`, X25519 (PRF-ODH) | `2·N·Qe·P_PRF-ODH(t, Qd+Qe, Qd)` + collisions |
| `mlkem1024+x25519`, X25519 (ROM) | `2·N·Qe·pStDH(t, …) + (2Qe+2N)·pDistRerandom` + collisions |
| `xwing`, ML-KEM | `2·Pmcca(t, N, Qe, #ODecap) + 4·Qe·Pprf(t, Qd+1)` + collisions |
| `xwing`, X25519 | `2·N·Qe·pStDH(t, …) + 3·N·Qe·Pc2pri(t) + (2Qe+2N)·pDistRerandom` + collisions |

## Assumptions, stated precisely

- **KDF in the protocol.** `K = HKDF(ikm = ss, salt = TH, info)` is assumed to be a
  PRF keyed by `ss`. HKDF-Extract is HMAC keyed by the salt, so this is HMAC
  keyed through its *message* input: the swap-PRF ("dual-PRF") property.
  [BBGS23] prove it for HMAC when keys come from "feasible" sets, which they show
  covers the fixed-length keys of TLS 1.3 and KEMTLS; `ss` is a fixed-length
  32-byte key of the same kind. Feasibility was not checked formally for this
  protocol.
- **`mlkem1024+x25519`, ML-KEM direction.** HKDF with `ikm = ss_M ‖ ss_X` is
  assumed to be a PRF keyed by the `ss_M` half alone, with `ss_X`, the
  ciphertexts and the public keys as input. This **split-key** PRF assumption is
  outside what [BBGS23] prove (their key is the whole message input). It is the
  same kind of assumption that CryptoVerif's PQ-TLS model makes for HKDF-Extract
  over a concatenated hybrid secret [BJ24] (`examples/tls13/pq-tls`).
- **`mlkem1024+x25519`, X25519 direction.** `kem_bbfgs.m4.ocv` assumes a
  **PRF-ODH variant**: HKDF keyed by the Diffie–Hellman value, which here is the
  second half of the ikm, after the adversary-controlled `ss_M`. That is
  non-standard, with the same precedent as above (where the DH value comes
  first). `kem_bbfgs_x25519_rom.ocv` proves the same statement from **standard
  assumptions** instead: strong DH, with the HKDF call a random oracle. The
  mutation tests show that this route needs no binding property of ML-KEM
  only because the combiner hashes `ct_M`.
- **X-Wing.** ML-KEM direction: SHA3-256 as a PRF keyed by its first 32 bytes
  (`ss_M`), as in the X-Wing paper's post-quantum theorem. X25519 direction:
  strong DH, SHA3-256 as a random oracle, and C2PRI of ML-KEM (given the
  decapsulation key and an honest encapsulation `(k0, c0)`, no other ciphertext
  decapsulates to `k0`; the X-Wing paper's Definition 7), as in its classical
  theorem [XWing]. C2PRI is stated for honestly generated keys, which the
  adversary may know, and an honest challenge. It is neither the malicious-key
  binding that ML-KEM lacks [Sch24] nor needed in that form. Because the
  collision statement is a two-way rewrite, it also asserts that `c0`
  decapsulates to `k0`, so `Pc2pri` absorbs ML-KEM's correctness error.
- **X25519** is a **prime-order group**: clamping, the cofactor, the twist and
  low-order points are not modelled. CryptoVerif's HPKE analysis [ABHKLR21] makes
  the same abstraction, and the X-Wing paper's "nominal group" is close to it
  (its bound has a statistical term `2∆N`). A cofactor-aware model, as in the
  WireGuard analysis [LBB19] (`DH_X25519_expth`, gap-DH on the subgroup), was not
  attempted. The 32-byte X-Wing seed is modelled as two independent seeds
  (SHAKE-256 as a PRG).
- **Implementation note (outside the models).** X-Wing draft-11 applies no
  check to the X25519 output (§5.4, §5.5), and the models follow the draft:
  decapsulation always returns a key. pyca/cryptography raises `ValueError`
  when an X25519 output is all-zero, which for clamped scalars happens exactly
  on low-order points. Since October 15, 2026, `combiner/xwing.py` then uses
  the RFC 7748 value, 32 zero bytes, as the draft does, in both encapsulation
  and decapsulation. Before, it passed the error on (checked with
  pyca 50.0.1), a conformance difference that the known-answer tests did not
  cover. `tests/test_xwing_low_order.py` now pins the behaviour. The
  `mlkem1024+x25519` profile still rejects all-zero outputs, as RFC 9180
  §7.1.4 requires of DHKEM recipients. Its models don't include that
  rejection, but it depends only on the public point, so the adversary learns
  nothing from it that it couldn't compute, and secrecy is unaffected.

## Freshness and RevealKey

`NK` honest parties each run any number of initiator sessions (mutual or
anonymous), mutual-responder sessions and responder-only sessions; peers are
chosen by the adversary and may be dishonest. Every long-term key can be
corrupted at any time (the corruption oracle returns the key seed).

- A session is **fresh** when it accepted with an honest peer that was not
  corrupted at acceptance, and no partner session (same transcript `TH`) had its
  key revealed. The keys of all fresh initiators are tested together (`keyI`),
  as are those of all fresh mutual responders (`keyR`). Responder-only sessions
  are never fresh, since they do not authenticate the initiator; their keys are
  covered through their initiator partners.
- **RevealKey** (oracles `OI3`, `OR3`, `OA2`): every accepted session that is not
  fresh can have its key revealed on request. A reveal is refused only when a
  partner's key is under test, and a session whose partner was revealed is not
  tested. The mutation tests `fresh_*` remove each of these guards in turn: the
  corresponding secrecy query then fails, so each guard has effect.
- As in CryptoVerif's TLS 1.3 analysis, each role's keys are proved secret with
  the other role's test variable not public, since partners share a key. The
  key-uniqueness query shows the two roles' keys coincide only for matching
  transcripts.
- **Relative to §2's model.** Stronger: many test queries over all fresh
  sessions, with no partner required, so active attacks are covered;
  compromise of the session's own long-term key at any time (key-compromise
  impersonation); agreement proved with the keys public, on the whole
  transcript and, for G5, on `sig_R`; anonymous initiators tested. Weaker or
  different: a fresh session's key cannot be revealed *instead of* tested;
  RevealEph is static (the adversary chooses when the session starts; the spec
  deletes `sk_e` at acceptance); one ciphersuite. The reduction from this
  formulation to §2's single-Test game is not mechanized.

## Other modelling choices

- **The protocol model treats the hybrids abstractly** (one IND-CCA2 KEM, one
  UF-CMA signature); their hybrid robustness is proved in the separate KEM and
  composite models, combined as above. This mirrors the Tamarin analysis.
- **Ephemeral reveal** (`hybrid_ake_ephleak.ocv`): the revealed session's key, and
  that of every responder that encapsulated to the revealed ephemeral key, are
  not fresh (the sketch's freshness clause (ii)). Revealing the responder's
  encapsulation coins is not modelled (as in Tamarin). Key uniqueness is stated
  for fresh keys only: keys derived from a shared secret the adversary knows
  would need collision resistance of HKDF to be unique, which is not assumed.
- **One ciphersuite.** `SUITE_ID` is a constant; cross-suite downgrade is covered
  only by the Tamarin model (`suite_agreement`).
- **Encodings.** The length-prefixed encodings are injective constructors. The two
  signed hash inputs `LP(7 fields)` and `LP(TH, sig_R)` are declared disjoint,
  which holds because a byte string parses as at most one of them. Anonymous mode
  sends `LP("", "")`, which equals a named identity with an empty name and an
  empty key; that is harmless because an empty key never verifies.
- **Proof scripts** name variables that CryptoVerif generates (`u_9`, `e_5`, …)
  and count occurrences (`at_nth`), so they are pinned to CryptoVerif 2.13 and
  to the model text. After editing a model, regenerate them. A mis-targeted
  `replace` fails, because CryptoVerif proves each equality; it cannot make a
  false statement go through.

## Mutation tests

`make mutations` re-runs the proofs on modified models (`mutations.py`; about 45
seconds). All 16 behave as listed:

| Mutation | Change | Outcome |
|---|---|---|
| `ake_auth_only_baseline` | none (control), authentication-only proof | both agreement queries proved |
| `ake_no_ct_in_transcript` | `ct` removed from `TH` | both agreement queries **not** proved (a man in the middle swaps `ct`) |
| `ake_no_ct_in_transcript_full_proof` | the same, full proof | aborts: the KEM-correctness step cannot be justified |
| `ake_no_vkR_in_transcript` | `vk_R` removed from `TH` | initiator authentication not proved (unknown key share); the rest proved |
| `ake_no_context_strings` | `CTX_R` = `CTX_I` | still all proved (control): the signed encodings already differ |
| `ake_no_context_strings_no_encoding_separation` | both separations removed | initiator authentication not proved |
| `fresh_test_I_despite_revealed_partner` | initiator tested although a partner was revealed | `keyI` secrecy not proved |
| `fresh_reveal_I_despite_tested_R` | initiator revealed although its partner is tested | `keyR` secrecy not proved |
| `fresh_test_R_despite_revealed_I` | responder tested although its partner was revealed | `keyR` secrecy not proved |
| `fresh_reveal_R_despite_tested_I` | responder revealed although its partner is tested | `keyI` secrecy not proved |
| `fresh_reveal_A_despite_tested_I` | responder-only key revealed although its partner is tested | `keyI` secrecy not proved |
| `fresh_reveal_tested_I` | RevealKey answers for a tested initiator | `keyI` secrecy not proved |
| `ephleak_test_revealed_sessions` | freshness clause (ii) removed | `keyR` secrecy not proved (the adversary decapsulates); the rest proved |
| `composite_no_prehash_collision_resistance` | no CR for `PH` | composite EUF-CMA not proved |
| `xwing_x25519_branch_no_c2pri` | no ML-KEM C2PRI | X-Wing IND-CCA2 (X25519 direction) not proved |
| `bbfgs_rom_no_ctM_in_combiner` | `ct_M` removed from the ML-KEM-1024 combiner | IND-CCA2 (X25519 direction, ROM) not proved |

Failing to prove is not by itself an attack, since CryptoVerif is sound but not
complete; each row says what the proof should depend on.

## Reproduce

```bash
# CryptoVerif 2.13 source; check it against the sha512 pinned in
# ocaml/opam-repository (packages/cryptoverif/cryptoverif.2.13/opam):
#   f05b70ff9ab72daf6d58fd598b89fcbf8415cf1adfd0c93be8f98c18364d7da1
#   c968be0a42cba7e0b17081f0bf73dd0b1c291ebc6df4306e93008a4a57e5ac61
tar xzf cryptoverif2.13.tar.gz && (cd cryptoverif2.13 && ./build)   # OCaml >= 4.08
make CVHOME=$PWD/cryptoverif2.13              # all models; writes logs/ and RESULTS.txt
make mutations CVHOME=$PWD/cryptoverif2.13    # mutation tests
```

The results here were produced with CryptoVerif 2.13 built from that tarball
with OCaml 4.14.1 on Ubuntu 24.04.

## Files

- `hybrid_ake.ocv`, `hybrid_ake_ephleak.ocv` — protocol models (Theorems 1–2).
- `composite_sig.m4.ocv` — composite signature (Lemma 2); m4 variants.
- `kem_bbfgs.m4.ocv`, `kem_bbfgs_x25519_rom.ocv`, `kem_xwing.m4.ocv` — hybrid KEM
  profiles (Lemma 1).
- `mutations.py` — mutation tests. `Makefile` — runs everything.
- `RESULTS.txt` — every proved bound, with the runtime terms, from the last `make`.

## Review history

- **October 15, 2026 — initial version** (PR #47).
- **October 15, 2026 — post-merge independent review.** No proof step was found
  unsound and no proved query vacuous; probes reproduced all results. Changes
  made in response:
  - The protocol models now give the adversary **RevealKey on request** for every
    non-fresh session, with partner-based freshness. Before, some keys were
    withheld whenever a *possible* partner existed, matched on msg1 alone.
    A **key-uniqueness** query was added.
  - The claim that the Theorem 2 bound has "no session-guessing loss" was
    **wrong as stated**: the multi-instance KEM term costs about `n_S²` when
    reduced to single-instance IND-CCA2 (see [On tightness](#the-bounds)).
  - The KDF assumptions are now named precisely: the HMAC swap-PRF for the
    protocol, and a split-key PRF and a PRF-ODH variant for the ML-KEM-1024
    combiner. A random-oracle proof from standard assumptions was added for
    that combiner's X25519 direction.
  - "Exactly the X-Wing paper's assumptions" now says that X25519 is a
    prime-order group rather than a nominal group. The pyca low-order-point
    behaviour is recorded as an implementation note.
  - The composition side conditions are listed, and "static" is added to every
    RevealEph claim.
  - The `ct` mutation now checks the agreement queries directly, and six
    freshness-guard mutations and a combiner mutation were added.
  - m4 no longer rewrites model comments.
- **October 15, 2026 — X-Wing low-order points.** `combiner/xwing.py` now
  follows draft-11 on low-order X25519 points: it returns the all-zero X25519
  value instead of passing on pyca's `ValueError` (implementation note above;
  `tests/test_xwing_low_order.py`). No model changed; one model comment was
  updated.

## References

- [ABHKLR21] J. Alwen, B. Blanchet, E. Hauck, E. Kiltz, B. Lipp, D. Riepel. *Analysing the HPKE Standard.* EUROCRYPT 2021 (the KEM-equivalence proof pattern used here; X25519 as a prime-order group).
- [BBGS23] M. Backendal, M. Bellare, F. Günther, M. Scarlata. *When Messages are Keys: Is HMAC a dual-PRF?* CRYPTO 2023 (ePrint 2023/861).
- [BBM00] M. Bellare, A. Boldyreva, S. Micali. *Public-Key Encryption in a Multi-user Setting: Security Proofs and Improvements.* EUROCRYPT 2000.
- [BJ24] B. Blanchet, C. Jacomme. *Post-quantum sound CryptoVerif and verification of hybrid TLS and SSH key-exchanges.* CSF 2024 (models in the CryptoVerif distribution, `examples/tls13/pq-tls`, `examples/pq-ssh`).
- [CDM24] C. Cremers, A. Dax, N. Medinger. *Keeping Up with the KEMs: Stronger Security Notions for KEMs and Automated Analysis of KEM-based Protocols.* ACM CCS 2024.
- [LBB19] B. Lipp, B. Blanchet, K. Bhargavan. *A Mechanised Cryptographic Proof of the WireGuard Virtual Private Network Protocol.* EuroS&P 2019.
- [Sch24] S. Schmieg. *Unbindable Kemmy Schmidt: ML-KEM is neither MAL-BIND-K-CT nor MAL-BIND-K-PK.* IACR ePrint 2024/523.
- [XWing] M. Barbosa, D. Connolly, J. D. Duarte, A. Kaiser, P. Schwabe, K. Varner, B. Westerbaan. *X-Wing: The Hybrid KEM You've Been Looking For.* IACR Communications in Cryptology 1(1), 2024 (ePrint 2024/039); `draft-connolly-cfrg-xwing-kem-11`. Classical theorem: strong DH (ROM) + C2PRI of ML-KEM, X25519 as a nominal group; post-quantum theorem: ML-KEM IND-CCA + SHA3-256 PRF (standard model).
- FIPS 203, *Module-Lattice-Based Key-Encapsulation Mechanism Standard* (Table 1: decapsulation failure rates).
- CryptoVerif 2.13 manual and examples (`examples/hpke`, `examples/tls13`, `examples/wireguard`, `examples/pq-ssh`).

*Reference details should be checked against the primary sources before external use.*
