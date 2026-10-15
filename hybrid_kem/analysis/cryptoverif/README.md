# HYBRID-AKE — computational analysis (CryptoVerif)

Machine-checked computational proofs of the claims in
`../../docs/HYBRID_AKE_COMPUTATIONAL.md` (Theorems 1–2, Lemmas 1–2), for the
protocol of `../../docs/HYBRID_AKE_SPEC.md` as implemented in
`../../protocols/authenticated_handshake.py`. Checked with
**CryptoVerif 2.13** (Blanchet et al., Inria). Where the symbolic Tamarin models
in `..` treat the primitives as perfect, these models give the primitives only
their standard computational assumptions and produce explicit probability bounds.

## Result

Every query below is **proved** (`make` re-runs all eight models in about 8
seconds on two cores; the bounds are in `RESULTS.txt`).

| Model | Paper claim | What is proved | Assumptions | Library |
|---|---|---|---|---|
| `hybrid_ake.ocv` | Thm 1 (G3, G4) | responder authentication: injective agreement on the full transcript (both identities, `pk_e`, `ct`) and the key | KEM IND-CCA2; signature UF-CMA with corruption; `H` collision resistant; KDF a PRF keyed by `ss` | pq |
|  | Thm 1 (G5, G4) | initiator authentication (mutual mode): injective agreement, including `sig_R` | same | pq |
|  | Thm 2 (G1, G2) | real-or-random secrecy of every initiator key whose peer was honest and uncorrupted when it accepted, under adaptive corruption of all long-term keys at any time | same | pq |
|  | Thm 2 | the same for mutual-mode responder keys | same | pq |
| `hybrid_ake_ephleak.ocv` | Thm 1–2 with RevealEph | all four, when the adversary also learns the ephemeral secret of sessions it chooses | same | pq |
| `composite_sig.m4.ocv` `MLDSA_SECURE` | Lemma 2 | composite EUF-CMA, EdDSA fully broken | ML-DSA UF-CMA; pre-hash `PH` collision resistant | pq |
| `composite_sig.m4.ocv` `EDDSA_SECURE` | Lemma 2 | composite EUF-CMA, ML-DSA fully broken | EdDSA UF-CMA; `PH` collision resistant | pq |
| `kem_bbfgs.m4.ocv` `MLKEM_SECURE` | Lemma 1 | `mlkem1024+x25519` is IND-CCA2, X25519 fully broken | ML-KEM-1024 IND-CCA2; HKDF a PRF keyed by `ss_M` | pq |
| `kem_bbfgs.m4.ocv` `X25519_SECURE` | Lemma 1 | `mlkem1024+x25519` is IND-CCA2, ML-KEM fully broken | PRF-ODH for HKDF keyed by `ss_X` (standard model) | default |
| `kem_xwing.m4.ocv` `MLKEM_SECURE` | Lemma 1 | X-Wing is IND-CCA2, X25519 fully broken | ML-KEM-768 IND-CCA2; SHA3-256 a PRF keyed by `ss_M` | pq |
| `kem_xwing.m4.ocv` `X25519_SECURE` | Lemma 1 | X-Wing is IND-CCA2, ML-KEM broken except for C2PRI | strong DH; SHA3-256 a random oracle; ML-KEM C2PRI — the X-Wing paper's assumptions | default |

"Fully broken" means the adversary is handed that component's secret key at the
start. "pq" is CryptoVerif's post-quantum library (`-lib pq`), which contains only
assumptions known to hold against quantum adversaries (no random oracles, no
Diffie–Hellman assumptions); a proof that uses only it is post-quantum sound
[BJ24]. The two X25519 branches are classical by nature.

Each KEM model proves an `equivalence` that is **exactly** the `ind_cca2`
equivalence of CryptoVerif's `IND_CCA2_KEM` macro — the assumption the protocol
model makes about the KEM — with one extra oracle that hands out the broken leg's
secret key. So each KEM bound can be substituted for `Pkemcca` in the protocol
bound. The composite model proves standard single-key EUF-CMA; the protocol uses
CryptoVerif's multi-key UF-CMA-with-corruption macro, whose own bound is
`NK · Psign(single key)`. These two substitutions are the usual composition
step and are done by hand, not by CryptoVerif.

## The bounds

Notation: `Pkemcca`, `Psign`, `Pprf`, `Phash` are the adversary's advantages
against the KEM, signature, KDF and transcript hash; `#O` counts calls to oracle
`O` (`#OI1` initiator sessions, `#OR1` mutual-responder sessions, `#OA1`
responder-only sessions, `#OI2` decapsulations); `NK` honest parties; `N*`
are per-party session caps. The `P*coll` terms are collisions between honestly
generated keys or ciphertexts (negligible).

**Theorem 2** (key secrecy, `keyI` and `keyR`; `hybrid_ake.ocv`):

```
Adv ≤ 2·Pkemcca(t, #OI1, #OA1 + #OR1, #OI2)        one multi-key IND-CCA2 term
    + 2·NK·Psign(t, NI + NR + NRa)                  UF-CMA with corruption, NK keys
    + 2·(#OR1 + #OA1)·Pprf(t, 2)                    one PRF key per encapsulation
    + 18·Phash(t)  +  collision terms
```

**Theorem 1** (each agreement query):
`NK·Psign(t, NI + NR + NRa) + 6·Phash(t) + collision terms`.

There is **no session-guessing loss**: the sketch's `n_S²` factor does not appear.
CryptoVerif reasons about all sessions at once; the KEM enters once, as a
multi-instance IND-CCA2 advantage (reducing that to single-instance IND-CCA2
costs the usual hybrid factor in the number of encapsulations, i.e. linear, not
quadratic, in the number of sessions).

**Lemma 2** (composite signature): `PsignM(t, NS) + 2·Phash(t)` with EdDSA broken,
and `PsignT(t, NS) + 2·Phash(t)` with ML-DSA broken. Hence
`Adv^euf-cma_composite ≤ min(Adv_ML-DSA, Adv_EdDSA) + 2·Adv^cr_PH`.

**Lemma 1** (hybrid KEM, `N` users, `Qe` encapsulations, `#ODecap` decapsulations):

| Profile / leg relied on | Bound |
|---|---|
| `mlkem1024+x25519`, ML-KEM | `2·Pmcca(t, N, Qe, #ODecap) + 4·Qe·Pprf(t, Qd+1)` + collisions |
| `mlkem1024+x25519`, X25519 | `2·N·Qe·P_PRF-ODH(t, Qd+Qe, Qd)` + collisions |
| `xwing`, ML-KEM | `2·Pmcca(t, N, Qe, #ODecap) + 4·Qe·Pprf(t, Qd+1)` + collisions |
| `xwing`, X25519 | `2·N·Qe·pStDH(t, …) + 3·N·Qe·Pc2pri(t)` + collisions + `(2Qe+2N)·pDistRerandom` |

## What the mechanization changes in the paper sketch

These are recorded in `../../docs/HYBRID_AKE_COMPUTATIONAL.md` §7.

1. **Lemma 2 was missing a term.** The composite's components sign
   `M' = Prefix ‖ Label ‖ len(ctx) ‖ ctx ‖ PH(M)`, not `M`, so a composite
   forgery on a fresh `M` is a component forgery only if `PH(M)` is fresh too.
   The bound needs `Adv^cr_PH` (SHA-512, or SHAKE256 with 64-byte output).
   Without collision resistance of `PH` the proof does not go through (mutation
   `composite_no_prehash_collision_resistance`), and a `PH` collision would indeed
   transfer a signature from one message to another.
2. **For X-Wing, "either leg" is asymmetric.** Relying on ML-KEM needs only
   ML-KEM's IND-CCA2 and SHA3-256 as a PRF (standard model). Relying on X25519
   needs strong Diffie–Hellman with SHA3-256 as a random oracle **and** C2PRI of
   ML-KEM: given the decapsulation key and an honest encapsulation `(k0, c0)`,
   no other ciphertext decapsulates to `k0` (the X-Wing paper's Definition 7;
   close to LEAK-BIND-K-CT in [CDM24]). X-Wing does not hash `ct_M`, so if ML-KEM
   were broken *including* C2PRI, a second ciphertext with the same `ss_M` would
   decapsulate to the challenge key. Without C2PRI the proof fails (mutation
   `xwing_x25519_branch_no_mlkem_binding`). These are exactly the assumptions of
   the X-Wing paper's two theorems [XWing]; the paper proves C2PRI for ML-KEM-768
   from its hash functions alone, so it survives a break of the lattice problem.
   The `mlkem1024+x25519` profile hashes both ciphertexts and needs no C2PRI.
3. **The X25519 assumption is now precise.** The sketch's `Adv^dh_X25519` is
   PRF-ODH (standard model, with HKDF keyed by the Diffie–Hellman value) for the
   `mlkem1024+x25519` combiner, and strong DH in the random-oracle model for
   X-Wing.
4. **The Theorem 2 bound is tighter**, as described above.
5. **What the transcript must contain** (mutation tests, below): `ct` is
   load-bearing for secrecy, `vk_R` for initiator authentication, and the two
   context strings are a second, redundant layer of role separation on top of the
   different field counts of the two signed encodings.

## Modelling choices and what is not covered

- **The protocol model treats the hybrids abstractly.** The hybrid KEM is one
  IND-CCA2 KEM and the composite signature one UF-CMA scheme; the hybrid
  robustness is proved in the separate KEM and composite models and combined by
  hand (previous section). This mirrors how the Tamarin analysis is organised.
- **Parties and sessions.** `NK` honest parties, each running any number of
  initiator sessions (mutual or anonymous), mutual responder sessions and
  responder-only sessions; peers are chosen by the adversary and may be
  dishonest. Every long-term key can be corrupted at any time (the corruption
  oracle returns the key seed). A key is *tested* when its peer was honest and
  not yet corrupted when the session accepted; corrupting the peer later, or the
  session's own key at any time, is allowed (forward secrecy and resistance to
  key-compromise impersonation of the long-term key).
- **Key reveal.** A session's key is handed to the adversary when it is not
  tested, unless the session has a possible honest partner (initiator: a
  responder session with the same `TH`; responder: an initiator that sent the
  same msg1 and expects this responder), in which case it is withheld. The
  Bellare–Rogaway model would also allow revealing such a key when its partner
  is not the test session; withholding it is a small weakening of the adversary
  that the model does not mechanically justify. Responder-only sessions are
  never tested (they do not authenticate the initiator); their keys are covered
  through their initiator partners.
- **Ephemeral reveal** (`hybrid_ake_ephleak.ocv`) is static: the adversary picks,
  when an initiator session starts, whether it learns that session's ephemeral
  secret. Such a session's key, and the key of every responder session that
  encapsulated to that ephemeral key, are never tested — the sketch's freshness
  clause (ii). Revealing the responder's encapsulation coins is not modelled
  (the same as in the Tamarin model).
- **One ciphersuite.** `SUITE_ID` is a constant, so cross-suite downgrade is
  covered only by the Tamarin model (`suite_agreement`).
- **Encodings.** The length-prefixed encodings are modelled as injective
  constructors; the two signed hash inputs `LP(7 fields)` and `LP(TH, sig_R)` are
  declared disjoint, which holds because a byte string parses as at most one of
  them.
- **Correctness.** CryptoVerif's KEM macro assumes perfect correctness. ML-KEM's
  decapsulation failure probability (about 2^-165 for ML-KEM-768 and 2^-175 for
  ML-KEM-1024 per FIPS 203) adds at most that much per decapsulation.
- **X25519** is a prime-order group (clamping and the cofactor are not modelled);
  X-Wing's 32-byte seed is modelled as two independent seeds (SHAKE-256 as a PRG).
- **Hash functions.** SHA3-256 appears as a collision-resistant hash (transcript),
  as a PRF or random oracle (X-Wing combiner), and HKDF-SHA256 as a PRF keyed by
  its input keying material (the dual-PRF property of HMAC). Using different
  idealisations of one function relies on its uses having disjoint input formats.
- **C2PRI** (`kem_xwing.m4.ocv`) is stated for honestly generated keys, which
  the adversary may know, and an honest challenge encapsulation. It is not the
  stronger malicious-key binding (MAL-BIND-K-CT), which ML-KEM does not have
  [Sch24] and which is not needed here.
- **Proof scripts** name variables that CryptoVerif generates (`u_9`, `e_5`, …),
  so they are pinned to CryptoVerif 2.13.

## Mutation tests

`make mutations` re-runs the proofs on weakened models (`mutations.py`). Each
must fail where stated, and all do:

| Mutation | Removes | Outcome |
|---|---|---|
| `ake_no_ct_in_transcript` | `ct` from `TH` | proof aborts: the step "the initiator's decapsulated secret is the responder's encapsulated one" can no longer be justified (a man in the middle can swap `ct`) |
| `ake_no_vkR_in_transcript` | `vk_R` from `TH` | initiator authentication not proved (unknown key share); the other three still proved |
| `ake_no_context_strings` | `CTX_R` ≠ `CTX_I` | **still all proved** (control): the signed encodings already differ |
| `ake_no_context_strings_no_encoding_separation` | both of the above separations | initiator authentication not proved |
| `ephleak_test_revealed_sessions` | freshness clause (ii) | responder-key secrecy not proved (the adversary decapsulates); the rest proved |
| `composite_no_prehash_collision_resistance` | CR of `PH` | composite EUF-CMA not proved |
| `xwing_x25519_branch_no_mlkem_binding` | ML-KEM C2PRI | X-Wing IND-CCA2 (X25519 leg) not proved |

Failing to prove is not by itself an attack (CryptoVerif is sound, not
complete); each row's "Removes" column says why a proof should need it.

## Reproduce

```bash
# CryptoVerif 2.13 source; check it against the sha512 pinned in
# ocaml/opam-repository (packages/cryptoverif/cryptoverif.2.13/opam):
#   f05b70ff9ab72daf6d58fd598b89fcbf8415cf1adfd0c93be8f98c18364d7da1
#   c968be0a42cba7e0b17081f0bf73dd0b1c291ebc6df4306e93008a4a57e5ac61
tar xzf cryptoverif2.13.tar.gz && (cd cryptoverif2.13 && ./build)   # OCaml >= 4.08
make CVHOME=$PWD/cryptoverif2.13              # all models; writes logs/ and RESULTS.txt
make mutations CVHOME=$PWD/cryptoverif2.13    # negative controls
```

The results here were produced with CryptoVerif 2.13 built from that tarball
with OCaml 4.14.1 on Ubuntu 24.04.

## Files

- `hybrid_ake.ocv`, `hybrid_ake_ephleak.ocv` — protocol models (Theorems 1–2).
- `composite_sig.m4.ocv` — composite signature (Lemma 2); m4 variants.
- `kem_bbfgs.m4.ocv`, `kem_xwing.m4.ocv` — hybrid KEM profiles (Lemma 1); m4 variants.
- `mutations.py` — mutation tests. `Makefile` — runs everything.
- `RESULTS.txt` — every proved bound, with the runtime terms, from the last `make`.

## References

- [BJ24] B. Blanchet, C. Jacomme. *Post-quantum sound CryptoVerif and verification of hybrid TLS and SSH key-exchanges.* CSF 2024.
- [CDM24] C. Cremers, A. Dax, N. Medinger. *Keeping Up with the KEMs: Stronger Security Notions for KEMs and Automated Analysis of KEM-based Protocols.* ACM CCS 2024.
- [Sch24] S. Schmieg. *Unbindable Kemmy Schmidt: ML-KEM is neither MAL-BIND-K-CT nor MAL-BIND-K-PK.* IACR ePrint 2024/523.
- [XWing] M. Barbosa, D. Connolly, J. D. Duarte, A. Kaiser, P. Schwabe, K. Varner, B. Westerbaan. *X-Wing: The Hybrid KEM You've Been Looking For.* IACR Communications in Cryptology 1(1), 2024 (ePrint 2024/039); `draft-connolly-cfrg-xwing-kem`. Classical theorem: strong DH (ROM) + C2PRI of ML-KEM; post-quantum theorem: ML-KEM IND-CCA + SHA3-256 PRF (standard model).
- [ABHKLR21] J. Alwen, B. Blanchet, E. Hauck, E. Kiltz, B. Lipp, D. Riepel. *Analysing the HPKE Standard.* EUROCRYPT 2021 (the KEM-equivalence proof pattern used here).
- CryptoVerif 2.13 manual and examples (`examples/pq-ssh`, `examples/tls13/pq-tls`, `examples/hpke`).

*Reference details should be checked against the primary sources before external use.*
