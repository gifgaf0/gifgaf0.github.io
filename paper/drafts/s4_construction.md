## §4 The Module-SLWE Construction

### §4.1 Public Parameter Setup

**Definition 4.1 (Parameters).** A Module-SLWE parameter set is (p, k, η, d) where p is a mod-455 prime, k is the module rank, η is the CBD noise parameter, and d = 16 is the sedenion dimension. Effective LWE dimension n = k·d. Target production set: (p=8191, k=32, η=2, d=16), n=512.

**Definition 4.2 (Public matrix).** A ∈ 𝕊_p^{k×k} is drawn uniformly at random. Each entry Aᵢⱼ ∈ 𝕊_p is sampled independently and uniformly over F_p^{16}.

*Implementation note.* An earlier Singer-orbit construction is rank-deficient by ~6.7× at k=32 due to column periodicity at distance 112 = 7·16. It is retained as a documented baseline (tools/singer_rank_demo.py) but not used for key generation. The uniform random construction achieves F_p-rank 512 with overwhelming probability and retains the algebraic shield.

### §4.2 Secret and Error Distributions

**Definition 4.3 (CBD-rejection sampler).** χ_{p,η} samples each of 16 coefficients from CBD(η) — centered binomial distribution on {−η,...,η} — and rejects if the result is a zero divisor. Rejection rate ≈ 10⁻⁵ at p=8191.

**Remark 4.4.** ZD elements z have rank(L_z) = 12. A ZD secret collapses the module equation to a rank-12 system enabling recovery. ZD rejection ensures secrets and errors are in the full-rank regime.

**Definition 4.5.** Secret s ∈ 𝕊_p^k and error e ∈ 𝕊_p^k have each component drawn from χ_{p,η}. Randomness r ∈ 𝕊_p^k and errors e₁ ∈ 𝕊_p^k, e₂ ∈ 𝕊_p likewise.

**Noise budget (T1).** Inner product magnitude is O(k·d·η²), independent of p. At p=8191, k=4, η=2: DFR = 0/5000 trials.

### §4.3 Key Generation

**Algorithm 4.6 (KeyGen).**
```

Input: (p, k, η) Output: pk = (A, b), sk = s

1. A ← uniform random in 𝕊_p^{k×k}
2. s ← χ_{p,η}^k
3. e ← χ_{p,η}^k
4. b ← A·s + e
5. return pk = (A, b), sk = s

```

Key sizes at p=8191, k=4: pk ≈ 640 bytes, sk ≈ 128 bytes.

### §4.4 Encapsulation

**Algorithm 4.7 (Encaps).**
```

Input: pk = (A, b) Output: ct = (c₁, c₂), K

1. m ← {0,1}^256
2. r ← χ_{p,η}^k
3. e₁ ← χ_{p,η}^k
4. e₂ ← χ_{p,η}
5. c₁ ← Aᵀ·r + e₁
6. c₂ ← ⟨b, r⟩_norm + e₂ + m·⌊p/2⌋
7. K ← H(m)
8. return ct = (c₁, c₂), K

```

Ciphertext size at toy parameters: ct ≈ 106 bytes. Shared secret K is 256 bits.

### §4.5 Decapsulation

**Algorithm 4.8 (Decaps).**
```

Input: sk = s, ct = (c₁, c₂) Output: K

1. v ← c₂ − ⟨s, c₁⟩_norm
2. m̃ ← round(v, ⌊p/2⌋)
3. K ← H(m̃)
4. return K

```

### §4.6 Correctness

**Theorem 4.9.** Decaps(sk, Encaps(pk)) = K whenever |ε| < p/4, where ε = ⟨e, r⟩_norm − ⟨s, e₁⟩_norm + e₂.

*Proof.* Expanding the residual and applying the adjoint identity (Lemma 2.11): ⟨As, r⟩_norm = ⟨s, Aᵀr⟩_norm, giving v = ε + m·⌊p/2⌋. Rounding recovers m when |ε| < p/4. □

**Remark 4.10 (DFR, T1).** At (p=8191, k=4, η=2): DFR = 0/5000. DFR at production parameters (k=32) not yet measured; see §6.

### §4.7 IND-CCA2 Transformation

The construction achieves IND-CPA security under the Module-SLWE assumption. Standard conversion to IND-CCA2 follows the Fujisaki-Okamoto transform [9] or its modular variant [10]. The formal security argument is standard given OW-CPA; the open question is whether Module-SLWE achieves OW-CPA — equivalently, whether Module-LWE over 𝕊_p is hard.
