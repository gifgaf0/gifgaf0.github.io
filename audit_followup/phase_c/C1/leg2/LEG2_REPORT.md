# C1 leg 2 (blind): rank of the flattened Singer-orbit public matrix

I built the matrix from the pre-registration text alone. Over F_p it has rank exactly 76 at every module rank tested (k = 8, 16, 32, 64), at both primes and for all three seed sets, so it is always within the bound of 112, while a fully uniform matrix of the same shape had full rank 16k every time. Two independent exact rank routines (python-flint and my own Gaussian elimination in Python integers) agree on all 42 matrices, and the sedenion algebra passed every sanity check.

## Results (DR-C1-1 runs)

Rank of the 16k × 16k matrix M over F_p. Each rank was computed twice: flint `nmod_mat.rank()` and my own elimination. The two agreed in every cell, so each number below stands for both.

| k | prime | 16k | Singer-orbit rank, set 0 / 1 / 2 | ≤ 112 | deficit 16k − rank | control (uniform A) rank | control full? |
|---|---|---|---|---|---|---|---|
| 8 | 911 | 128 | 76 / 76 / 76 | yes | 52 | 128 | yes |
| 16 | 911 | 256 | 76 / 76 / 76 | yes | 180 | 256 | yes |
| 32 | 911 | 512 | 76 / 76 / 76 | yes | 436 | 512 | yes |
| 64 | 911 | 1024 | 76 / 76 / 76 | yes | 948 | 1024 | yes |
| 8 | 4294977961 | 128 | 76 / 76 / 76 | yes | 52 | 128 | yes |
| 16 | 4294977961 | 256 | 76 / 76 / 76 | yes | 180 | 256 | yes |
| 32 | 4294977961 | 512 | 76 / 76 / 76 | yes | 436 | 512 | yes |
| 64 | 4294977961 | 1024 | 76 / 76 / 76 | yes | 948 | 1024 | yes |

**Leg 2's side of the PASS rule (§2):** rank ≤ 112 at all four k, at both primes and for every seed set, holds. Both controls have full rank at every (k, p). This leg does not decide the verdict. It also cannot judge agreement with leg 1, which it has not seen. The k = 32 value matches the "measured 76" quoted in the pre-registration's own summary.

### Descriptive curve, p = 911, k = 1 … 10

I drew one list of 10 seeds. The matrix at each k uses the first k of them, so M_k is the leading principal block of M_{k+1}. Flint and my own elimination agree at every k.

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| rank M | 16 | 32 | 48 | 64 | 72 | 74 | 76 | 76 | 76 | 76 |
| min(16k, 112) | 16 | 32 | 48 | 64 | 80 | 96 | 112 | 112 | 112 | 112 |

The rank is full (16k) up to k = 4. It falls short from k = 5 onwards (72, 74) and stays flat at 76 from k = 7 onwards.

### Item 5: column block j against column block j + 7

**Yes.** In every Singer-orbit matrix built, column block j of M equals column block j + 7 for every j with j + 7 < k. That covers 24 main-run matrices and the 3 curve matrices with k ≥ 8, 558 block pairs in all, with no failures. This is a real test, not a property built into the code: A[i][j] was formed by applying σ literally j times, with no reduction of j mod 7. Each matrix with k ≥ 7 has exactly 7 distinct column blocks (min(k, 7) in general), so blocks whose indices differ by something other than a multiple of 7 never coincide.

### Extra (descriptive, not pre-registered): why the value is 76 for every seed

M factors as (S ⊗ I_16)·N_k. Here S is the k × 16 seed matrix. N is a fixed 256 × 112 matrix that does not depend on the seeds: N[16m + r][16j + c] = coefficient r of σ^j(e_m)·e_c, for m = 0..15 and j = 0..6. N_k repeats N's 7 column blocks with period 7. Hence rank M ≤ rank N, with equality whenever rank S = 16.

- rank N = 76 at both primes, by both flint and my own elimination.
- rank S = 16 in every main run with k ≥ 16, which forces rank M = 76.
- At k = 8 (rank S = 8), rank M still equals 76.

Every Singer run is consistent with this factorisation. So the exact value 76 is a property of the construction (σ together with the sedenion product), not seed noise. σ is **not** an automorphism of the algebra (checked on random pairs; descriptive only).

## Sanity checks of the algebra

All checks ran at both primes. The "exact" checks were run over the integers.

| check | p = 911 | p = 4294977961 |
|---|---|---|
| e_i·e_i = −e_0 for i = 1..15 | pass (no failures) | pass (no failures) |
| e_0 is a two-sided identity on all 16 basis vectors | pass | pass |
| e_0 is a two-sided identity on 100 random sedenions | pass | pass |
| Octonions (span e_0..e_7): left alternative (xx)y = x(xy) | 200 / 200 | 200 / 200 |
| Octonions: right alternative (yx)x = y(xx) | 200 / 200 | 200 / 200 |
| Octonions: product stays in e_0..e_7 | 200 / 200 | 200 / 200 |
| Octonions: norm multiplicative N(xy) = N(x)N(y) | 200 / 200 | 200 / 200 |
| Sedenions: left alternative (xx)y = x(xy) | **0 / 200** (not alternative) | **0 / 200** (not alternative) |
| Sedenions: right alternative | 0 / 200 | 0 / 200 |
| Sedenions: norm multiplicative | 0 / 200 | 0 / 200 |
| Sedenions: flexible (xy)x = x(yx) (expected to hold) | 200 / 200 | 200 / 200 |
| Left-multiplication matrices L_a equal the direct product a·b (30 random a, b, every column a·e_c) | pass | pass |

**Exact checks over the integers:**
- For every basis pair, e_i·e_j = ±e_{i XOR j}, and the imaginary units anticommute.
- e_1e_2 = e_3, e_1e_4 = e_5 and e_1e_8 = e_9.
- Deterministic witness that the sedenions are not alternative: x = e_1 + e_10, y = e_4 gives (xx)y = −2e_4 but x(xy) = −2e_4 − 2e_15.
- The same family of test pairs restricted to e_0..e_7 gives 0 counterexamples.

**σ:**
- Images: e_1→e_2→…→e_7→e_1 and e_9→e_10→…→e_15→e_9; e_0 and e_8 are fixed.
- σ^7 = id on all basis vectors and on a random vector, while σ^d ≠ id for d = 1..6. So σ has order 7.

**Fields:**
- Both 911 and 4294977961 are prime, by my own deterministic Miller–Rabin and by flint.
- Both are ≡ 1 (mod 455).
- 4294977961 is the smallest prime above 2^32 that is ≡ 1 (mod 455), as the pre-registration states.

**Seeds:** none of the 730 distinct Singer seeds drawn had two or fewer nonzero coordinates. That is 720 in the main runs plus the 10 curve seeds. The reference's rejection of two-term zero divisors would therefore never have fired, and I did not implement it.

## Method

- **Algebra.** Recursive Cayley–Dickson product (a, b)(c, d) = (ac − conj(d)·b, d·a + b·conj(c)) on coordinate vectors split into halves, so e_{i+8} = (0, e_i), and likewise at every level. conj keeps coordinate 0 and negates the rest. All arithmetic is mod p in Python integers. L_a is assembled from the 256 nonzero structure constants, which were themselves computed by the recursive product, and was checked against the direct product.
- **σ.** σ(v)[(i mod 7)+1] = v[i] and σ(v)[(i mod 7)+9] = v[i+8] for i = 1..7.
- **A and M.** A[i][j] = σ^j(seed_i). M[16i + r][16j + c] = coefficient r of A[i][j]·e_c.
- **Randomness.** `random.Random(int(sha256("SQT-C1-leg2|" + tag)))`, then `randrange(p)` per coordinate.
  - Tags `singer|p=<p>|k=<k>|set=<s>`, `control|p=<p>|k=<k>` and `curve|p=911`.
  - Every Singer seed vector is stored in `leg2_seeds.json`. The control matrices are identified by SHA-256 in `leg2_results.json`.
- **Rank, two ways.**
  - flint `nmod_mat(M, p).rank()`.
  - My own row-echelon elimination (`rank_own`), exact in Python integers, with no floats and no fixed-width integers. It ran on all 42 matrices, including the four 1024 × 1024 controls: 46 s at p = 911 and 78 s at p = q.
- **Run.**
  - Python 3.13.16, python-flint 0.9.0, Linux x86_64.
  - Wall time 221 s. Reproduce with `python3 -I -B c1_leg2.py`. `--selftest` prints quick checks and writes nothing.

## Blindness and scope

- **Files read.** The only repository file I read was `audit_followup/phase_c/C1/C1_PREREG.md` (md5 `778e3d4a2417b2361282730781a295e4`; its md5 is also recorded in the JSON).
- **Files not touched.** I opened, listed and grepped nothing in `leg1/`, `tools/`, `hybrid_kem/` or anywhere else. I ran no git commands.
- **Where outputs went.** All output is in this directory.

## Problems hit

None affected any result.

- **Selftest bug, fixed before running.** In my first draft, the `--selftest` path re-created its random generator for every seed, which would have made all selftest seeds identical. I caught this in review and fixed it before the selftest was ever run. The full run always used one generator per seed set.
- **Pre-run edit.** Before the recorded run I also added traceback logging to the log file. The script md5 recorded in the JSON (`6df3de127cbb12320c340321893e9063`) is the version that produced every number here.
- **The bound is not tight.** The exact rank (76) is well below the 112 bound. This does not affect the rule, which asks only for ≤ 112.

## Files (md5)

| file | md5 |
|---|---|
| `c1_leg2.py` (script) | `6df3de127cbb12320c340321893e9063` |
| `leg2_results.json` (every rank, checks, timings, provenance) | `7484a20ab1f05a6b16ee44ea2f645fd5` |
| `leg2_seeds.json` (all Singer seed vectors) | `e8d1b03d9bc4f15163a1afef1719e381` |
| `leg2_run.log` (run log) | `7b3d5deb686c7442e15acac3604df462` |
| `LEG2_REPORT.md` (this file) | not listed here, since a file cannot contain its own md5; given in the hand-off message |
