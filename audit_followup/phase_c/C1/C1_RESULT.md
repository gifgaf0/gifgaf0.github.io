# C1 — The crypto negative result: rank 76 at every module rank, and no 128-bit security at spec even with a uniform matrix

**Plain-language summary.** The program's lattice cryptosystem (sedenion Module-LWE, "SLWE") fails at its own parameters, for two independent reasons.
- **The structured public matrix is degenerate at every size, not just at k = 32.** Built as the design says, from Singer-cycle orbits, the matrix has rank exactly 76 whatever the module rank, from k = 7 upward. A random matrix of the same shape has full rank, 16k. The reason is structural: the matrix factors through a fixed 256 × 112 matrix whose rank is 76. An attacker can therefore shrink the problem to dimension 76, which the standard lattice estimator puts at about 2^39 operations.
- **A uniform matrix does not rescue the spec.** The crypto project's later fix (Brief 06) makes the matrix uniform. Even so, the spec parameters (dimension 512, modulus about 2^32, noise ±2, secrets with 64 nonzero entries) give about 2^51, not the 2^128 target. The modulus is so large relative to the noise that the lattice problem is easy.
- **Decryption never fails at spec.** The noise term is bounded by 258, against a decryption threshold of about 10⁹. The ledger's "2^(−6.4 × 10¹⁵)" came from a Gaussian tail evaluated far outside the range the noise can take.

The ledger's §§2.59–2.61 also rest on the "sum-to-14" pairing rule that §3.05 superseded in May. On the actual kernels, the rule holds for only 6 of the 21 pairs. All of this goes into the Phase C fold as annotations. A short ePrint note is drafted and not submitted.

## DR-C1-1: the rank at every module rank (pre-registration `C1_PREREG.md`, md5 `778e3d4a…`, locked at ce82bdc)

**Verdict: PASS, WIDENED.** Both legs computed exact ranks over F_p, and leg 1 was committed (782594c) before leg 2 started.
- Leg 1 used the reference construction itself: `tools/sedenion_Fp.py` and the `tools/sqt_slwe.py` orbit rule.
- Leg 2 was a blind subagent. It built the algebra from the pre-registration text alone, and computed every rank twice, with python-flint and with its own elimination.

| p | k | 16k | leg 1 (3 seed sets) | leg 2 (3 seed sets) | uniform control (both legs) |
|---|---|---|---|---|---|
| 911 | 8 / 16 / 32 / 64 | 128 / 256 / 512 / 1024 | 76, 76, 76 at every k | 76, 76, 76 at every k | full rank, 16k |
| 4,294,977,961 | 8 / 16 / 32 / 64 | 128 / 256 / 512 / 1024 | 76, 76, 76 at every k | 76, 76, 76 at every k | full rank, 16k |

- **Agreement.** The two legs agree exactly in every cell (`c1_compare.py`).
- **Period-7 columns.** Column block j equals block j + 7 in every Singer matrix. Leg 1 checked all of them; leg 2 checked 558 block pairs.
- **Curve at p = 911** (both legs, identical). The rank at k = 1 … 10 is 16, 32, 48, 64, **72, 74, 76**, 76, 76, 76.
  - The collapse starts at k = 5, not k = 8: 72 of 80, then 74 of 96, then 76 of 112.
  - So §2.69.5's parenthesis "k ≤ 7 (no periodicity, no collapse)" holds only for k ≤ 4.

**Why 76, for every seed (found by leg 2, confirmed from the reference table in `c1_compare.py`).** Write s for the seed matrix (k × 16). M[16i + r][16j + c] is coefficient r of σ^j(seed_i)·e_c, which is linear in the seed. So M = (S ⊗ I₁₆)·N_k, where:
- N[16m + r][16j + c] is coefficient r of σ^j(e_m)·e_c;
- N_k repeats N's seven column blocks with period 7, because σ⁷ = id.

N is a fixed 256 × 112 integer matrix of **rank 76 over ℚ**, and also mod 911 and mod the spec prime. Hence **rank(M) ≤ 76 for every k and every choice of seeds**. Equality holds generically from k = 7. Leg 2 also notes that σ is not an algebra automorphism: the "PSL(2,7) symmetry" of A is a relabelling of coordinates.

**Security reading (R2, as pre-registered).**
- b − e = M·s lies in the 76-dimensional column space of M. So the noise e is the short vector of an LWE instance with a 76-dimensional secret (the noise on 76 coordinates) and 16k − 76 samples. The same holds for the ciphertext noise e₁, through M's adjoint.
- With e and e₁ recovered, the shared bit follows. ⟨b − e, r′⟩ = ⟨M·s, r⟩ for any r′ with M^H r′ = c₁ − e₁, so c₂ − ⟨b − e, r′⟩ = ⟨e, r⟩ + e₂ + m⌊q/2⌋, with |⟨e, r⟩ + e₂| ≤ 130.
- The lattice estimator on that reduced instance (n = 76, q = 4,294,977,961, secret and noise CBD(2), m = 436) gives **2^38.6** (usvp and bdd). β = 40 is the estimator's floor, so lattice reduction at LLL scale suffices.

## DR-C1-2: the spec parameters with a uniform matrix (OP-2.58.5, criterion (iii))

**Verdict: criterion (iii) FAILS.** The parameters are the spec of §2.66.1:
- n = 512 (k = 32);
- q = 4,294,977,961;
- sparse ternary secret with 32 entries of +1 and 32 of −1;
- CBD(2) noise;
- m = 512.

The tool is the lattice estimator (`malb/lattice-estimator` 53da5982, run under passagemath 10.8.12 Sage) with its default attack set.

| attack | bdd | bdd_hybrid | dual_hybrid | usvp | dual | bdd_mitm_hybrid | bkw | arora-gb |
|---|---|---|---|---|---|---|---|---|
| log₂ rop | **51.0** | 51.0 | 51.5 | 52.1 (β = 72) | 53.2 | 58.2 | 111.8 | 412.5 |

- **Cross-check.** `c1_coresvp_crosscheck.py` was written before the estimator was run and without reading its code. Its primal core-SVP 2016 estimate gives β = 72, d = 937 and 2^21.0. That is identical to the estimator's own `rough` usvp (β = 72), and on the same side of 2^128.
- **More samples do not change it.** With m = 1024 (a public key plus one ciphertext), the minimum is again 2^51.0.

**Descriptive (not pre-registered): the two smallest primes ≡ 1 (mod 455), same n, secret and noise.**

| q | cheapest attack | without bkw (which needs about 2^110 samples) |
|---|---|---|
| 911 | 2^122.2 (bkw) | 2^127.4 (bdd_mitm_hybrid) |
| 2731 | 2^114.4 (dual_hybrid) | 2^114.4 |

So at n = 512 with these secret and noise distributions, neither of the two smallest such primes reaches 2^128, and the large spec modulus is far worse. Whether any (q, η) meets all three OP-2.58.5 criteria at k = 32 was not searched. The two points above suggest a larger n or wider noise would be needed.

**The repository's earlier security table is not the spec.**
- `tools/lattice_estimate_results.md` reports "> 512 bits" for "full | k = 32, q = 2³²". It assumed noise σ = √q/(2√(2π)) ≈ 13,000 and n = k·256 = 8192, and its estimator run failed (returned infinity).
- `tools/SLWE_Prime_Master_v2.md` §4.4 lists β and "bits" that do not match core-SVP (for example, "Kyber-512: β = 120, 166b"). The same section's scenario "Z₇ folds n to 73 … BROKEN — NOT demonstrated" is now demonstrated: the rank is 76.

These are crypto-project files outside the ledger, flagged for the author.

## DR-C1-3: correctness as a worst-case bound (`c1_checks.py`)

N = ⟨e, r⟩ − ⟨s, e₁⟩ + e₂, with the Euclidean inner product. With entries of e, e₁ and e₂ bounded by B and weights h_r = h_s = 64:

| noise | worst case abs(N) | against q_spec/4 = 1.07 × 10⁹ | DFR at spec | q needed for DFR = 0 |
|---|---|---|---|---|
| CBD(η = 2), the spec | 258 | margin 4.2 × 10⁶ | **0** | q > 1032 |
| CBD(η = 512), the top of §2.66.1's sweep | 66,048 | margin 16,257 | **0** | q > 264,192 |
| §2.58.B confined kernel noise, σ = 2 | 258 | margin 4.2 × 10⁶ | **0** | q > 1032 |

- **Confined-noise bound.** All 84 two-term cross-edge zero divisors have 4-dimensional kernels whose reduced-echelon bases have entries in {0, ±1}. So σ·Σα_j k_j has entries of at most 2.
- **Where "2^(−6.4 × 10¹⁵)" came from.** §2.66.1 applied a Gaussian tail with σ_N = 11.36 at z = q/(4σ_N) = 9.45 × 10⁷. That reproduces log₂ DFR = −6.45 × 10¹⁵, but the point lies about 4 × 10⁶ times beyond the largest value N can take. The same holds for §2.66's −1.29 × 10¹⁶ … −2.52 × 10¹³.
- **The exact distribution.** For CBD noise, N is exactly CBD(258) (sums of independent symmetric CBD draws), so tails are exact binomial sums. At the toy prime 911, P(|N| > 227) = **2^−353.5**, not the 2^−294.7 of the Gaussian formula. At q = 2731 and at spec it is exactly 0.

## The §3.05 correction carried into §§2.59–2.61 (`c1_checks.py`, part 3)

§3.05 (May 16) superseded the "complement to 14" pairing on the zero-divisor kernels. It had been read off one sample; the general structure is the Fano-plane co-line action of §2.55. §2.59 (May 18) still builds on it: (a), the "sum-to-14 ZD complement rule". So do §2.60's "sum-14 complement constraint" (7 polynomial families, 13 components) and §2.61's complement layer and family automaton.

On the actual kernels (all 84 zero divisors at p = 911):
- the kernel supports are exactly the co-line partners of the third point of each pair's Fano line, for all 21 pairs, as §2.55 says;
- the sum-to-14 rule holds for only **6 of the 21** pairs: {1,2}, {1,4}, {1,6}, {2,4}, {2,5}, {3,4}.

§§2.59–2.61's counts therefore describe the superseded rule, not the kernels.

## Other findings for the record

- **§2.66.2's toy leakage runs were on rank-deficient matrices.** They used k = 7 and k = 14, where the public matrix has rank 76, of 112 and of 224.
- **§2.69.5's k = 32 scoping is lifted.** Its rank-76 finding holds for every k ≥ 7.

## Ledger annotations for the Phase C fold (V4.93 line numbers)

| Line | Entry | Bracket (gist) |
|---|---|---|
| 3241 | §2.58.B status | KeyGen step 3's matrix has rank 76 for every k ≥ 7 (fixed 256 × 112 factor of rank 76). The spec fails 128-bit security even with a uniform matrix (2^51). DFR = 0 |
| 3290 | OP-2.58.1.a, "~10¹⁵ bits of headroom" | DFR = 0 exactly (worst case 258 < q/4); the headroom figure is a Gaussian tail beyond the support |
| 3292, 4452 | OP-2.58.5 | Criterion (iii) fails at spec (estimator 2^51.0; core-SVP β = 72). (ii) holds deterministically for q > 1032 |
| 3332 | §2.59 (a) | the sum-to-14 rule is the one §3.05 superseded; it holds for 6 of 21 pairs |
| 3347 | §2.60 Result I | computed on the superseded rule |
| 3359 | §2.61 Result I | its family automaton is §2.60's sum-14 families |
| 3445 | §2.66 production scaling | Gaussian tail beyond the support; DFR = 0 for every η in the sweep |
| 3474, 3490 | §2.66.1 figure and closure | worst-case bound 258 < q/4; DFR = 0, replacing 2^(−6.4 × 10¹⁵) |
| 3525 | §2.66.2 "What this DOES establish" | the toy runs (k = 7, 14) were on rank-76 matrices; (A, b) is distinguishable by elimination at every k ≥ 5 |
| 3539, 4447 | OP-2.58.2c | moot at spec |
| 3541, 4449 | OP-2.58.2e | false for the Singer matrix (A·s fills a 76-dimensional subspace) |
| 3817 | §2.69.5 security reading | not k-specific: rank 76 for every k ≥ 7, collapse from k = 5 |
| 4421, 4448 | G-BKZ32, OP-2.58.2d | rank 76 at every k ≥ 7, not only k = 32 |
| 4446 | OP-2.58.2 | any hardness claim at spec is refuted independently of the trapdoor question |
| 4611 | OP-2.58.1.a list item | as at 3290 |

## Files

| File | md5 |
|---|---|
| `C1_PREREG.md` | `778e3d4a2417b2361282730781a295e4` |
| `leg1/c1_rank_leg1.py` / `.json` / `_output.txt` | `b57ebd4a…` / `bdc85fb3…` / `077cc7ab…` |
| `leg2/c1_leg2.py` / `leg2_results.json` / `leg2_seeds.json` / `leg2_run.log` / `LEG2_REPORT.md` | `6df3de12…` / `7484a20a…` / `e8d1b03d…` / `7b3d5deb…` / `4f4d5547…` |
| `c1_compare.py` / `.json` / `_output.txt` | `3a34342d…` / `684cfae9…` / `993ba226…` |
| `c1_coresvp_crosscheck.py` / `.json` / `_output.txt` | `9be0adfa…` / `05be2746…` / `265b01cc…` |
| `estimator/c1_estimator_run.py` / `c1_estimator_results.json` / `c1_estimator_run.log` | `694c08d4…` / `3f5c0116…` / `11dc269e…` |
| `c1_checks.py` / `.json` / `_output.txt` | `a1c75aaa…` / `9e809fd1…` / `cc58d1e6…` |
