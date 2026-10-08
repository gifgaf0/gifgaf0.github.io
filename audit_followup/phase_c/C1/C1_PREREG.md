# C1 pre-registration: the Singer-orbit SLWE public matrix at every module rank, and the spec parameters with a uniform matrix

**Plain-language summary.** The ledger already records that, at module rank k = 32, the public matrix of the program's lattice cryptosystem has rank at most 112 (measured 76) instead of 512. That makes the matrix easy to tell apart from a random one. The audit says the cause, a repeating column pattern of period 7, does not depend on k, but the ledger scoped the finding to k = 32 only. This file fixes in advance:
- how the rank will be computed at k = 8, 16, 32 and 64;
- what result would widen the finding to every k;
- how the security of the spec parameters will be judged if the public matrix were made uniform.

It is locked by commit before any C1 computation runs.

**Locked:** October 7, 2026, before computation. Brief of October 6, item C1: "Confirm by direct computation that the Singer-orbit public matrix has rank ≤ 112 at several module ranks: k = 8, 16, 32, 64. Run the lattice estimator on the spec parameters with a uniform matrix. State correctness as a worst-case noise bound (DFR = 0), replacing the 2^(-6.4×10^15) figure."

## 1. The object (enough to rebuild it without any code)

- **Field.** F_p, at two primes: the toy prime p = 911 and the spec prime q = 4,294,977,961. The spec prime is prime, ≡ 1 (mod 455), and the smallest such prime above 2³².
- **Sedenions.** Use the 16-dimensional Cayley–Dickson algebra over F_p, with basis e_0 … e_15 and e_{i+8} = (0, e_i). Build it from the reals by doubling four times, with (a, b)(c, d) = (ac − d̄b, da + bc̄) at each level, where the bar negates every imaginary coordinate.
- **Singer action σ.** σ moves the coefficient of e_i to e_{(i mod 7)+1} for i = 1 … 7. It moves the coefficient of e_{i+8} to e_{(i mod 7)+1+8} in step. It fixes e_0 and e_8. σ has order 7.
- **Public matrix.** A is k × k with sedenion entries A[i][j] = σ^j(seed_i). The k seeds are independent and uniform in F_p^16. (The reference rejects two-term zero divisors, which a uniform draw essentially never produces.)
- **Flattening.** M is the 16k × 16k matrix of the map s ↦ A·s, with (A·s)_i = Σ_j A[i][j]·s_j by left multiplication. Its entries are M[16i + r][16j + c] = coefficient r of A[i][j]·e_c.
- **Quantity.** rank_{F_p}(M).

This is the construction of `tools/sqt_slwe.py` (keygen and `rank_flat`), the code behind §2.69.5's k = 32 measurement.

## 2. DR-C1-1: does the rank collapse hold at every module rank? (decides the scope)

- **Runs.** For each k ∈ {8, 16, 32, 64} and each prime p ∈ {911, q_spec}, use three independent seed sets. Compute rank_{F_p}(M) exactly.
- **Control.** At each (k, p), one fully uniform A (every entry uniform in F_p^16), flattened the same way. Expected rank: 16k.
- **Rule.**
  - **(i) WIDENED** if every computed rank of the Singer-orbit matrix is ≤ 112. The collapse then holds at every module rank k ≥ 8, with a deficit of at least 16k − 112. The k = 32 scoping of §2.69.5 and the rows that depend on it is lifted.
  - **(ii) HALT** if any rank exceeds 112. The construction then differs from the one described. Report it and annotate nothing.
- **The bound itself.** Rank ≤ 112 has a two-line proof: σ⁷ = id, so column blocks j and j + 7 of M coincide, leaving at most 7 × 16 distinct columns. The computation confirms that proof on the actual construction.
- **Two legs.** Leg 1 runs in this session. Leg 2 is a blind subagent: it builds M from Section 1 of this file alone, without reading leg 1's code or outputs, and uses its own rank routine. **PASS** requires both legs to give rank ≤ 112 at all four k, and both controls to give full rank. Exact rank values are reported. Agreement on them is recorded but does not decide the verdict.

**Security reading (R2, stated in advance, not decided by a number).** Write r = rank(M). b − e = M·s lies in the r-dimensional column space V of M, so the noise e is a short vector in the coset b + V. Choose r coordinates on which a basis of V is invertible. Then e is the solution of an LWE-type instance with an r-dimensional secret (the noise on those coordinates) and 16k − r samples, whatever k is. The ciphertext's e_1 satisfies the same statement for the column space of M's adjoint. The estimate for that reduced instance (Section 3) is descriptive.

## 3. DR-C1-2: are the spec parameters secure with a uniform matrix? (decides OP-2.58.5 criterion (iii))

- **Parameters** (spec per §2.66.1: k = 32, n = 512):
  - q = 4,294,977,961;
  - secret: sparse ternary with Hamming weight 64 (32 entries +1, 32 entries −1);
  - error: centred binomial with η = 2;
  - m = 512 samples (one public key).
- **Tool.** The lattice estimator (`malb/lattice-estimator`, commit `53da5982597709ba0fdf94ea37a84d822310fd84`) under Sage (passagemath), with its default attack set (`LWE.estimate`). If Sage cannot be installed, the fallback is the estimator's `LWE.estimate.rough` logic reimplemented and labelled as such.
- **Rule.**
  - **Criterion (iii) FAILS** if the cheapest attack's cost (rop) is below 2^128. The spec parameters then do not reach 128-bit classical security by the estimator, even with a uniform matrix.
  - **Criterion (iii) is MET** if it is at least 2^128. Only the rank collapse then stands against the spec.
- **Cross-check.** An independent primal-uSVP core-SVP estimate (the 2016 estimate: smallest β with √(β/d)·σ ≤ δ_β^(2β−d−1)·q^(m/d), cost 2^(0.292β)), written in this session without reference to the estimator's code. It must fall on the same side of 2^128. If it does not, report both numbers and issue no verdict.
- **Descriptive only.** The same estimator on the reduced instance of Section 2: n = r, secret and error both centred binomial with η = 2, m = 512 − r, the same q.

## 4. DR-C1-3: correctness as a worst-case bound (arithmetic; no second leg)

- **The noise term.** Decryption computes N = ⟨e, r⟩ − ⟨s, e_1⟩ + e_2 with the Euclidean inner product on F_p^{16k} (§2.66.1). With entries of e and e_1 bounded by B and Hamming weights h_r, h_s, the bound is |N| ≤ B·(h_r + h_s) + B_{e_2}.
- **Rule.** If the bound is below q/4 at spec, decryption never fails (DFR = 0), and this replaces "2^(−6.4 × 10^15)".
- **Both noise models.** The bound is evaluated for CBD(η) noise (B = η) and for the §2.58.B confined kernel noise. For the latter, B is the largest entry of σ·(α₀k₀ + … + α₃k₃) over all kernels, all α ∈ {−1, 0, 1}⁴, and σ = 2, computed.

## 5. What C1 does not claim

C1 claims no key-recovery cost for the Singer-orbit scheme beyond the descriptive estimate in Section 3. It says nothing about the confined-noise trapdoor question (OP-2.58.2), and nothing about any other structured matrix. The ePrint note, if written, is a draft for the author.
