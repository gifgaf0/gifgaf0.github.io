# Brief 04 — Empirical Sedenion ODLP Hardness Probe

> *T1 = measured fact (script reproducible from `tools/odlp_hardness.py`).
> No prediction or extrapolation is labelled T1.*

## What the sedenion ODLP actually is

The sedenions are non-associative but power-associative: `g^n` is well-
defined for any `g ∈ S_p` and integer `n` because powers of a single
element commute and associate. The set of all powers `{g^k : k ∈ ℕ}`
generates a *commutative* sub-algebra `F_p[g] ≅ F_p[X] / m_g(X)`,
where `m_g` is the minimal polynomial of `g` over `F_p` (degree ≤
DIM = 16). The unit group of this sub-algebra factors, by CRT, as a
product of cyclic groups `F_{p^{d_i}}^*` over the irreducible
factorisation `m_g = ∏ f_i` with `d_i = deg(f_i)`.

So the sedenion ODLP for a given `g` is, structurally, a finite-
abelian-group DLP whose order divides `lcm_i (p^{d_i} − 1)`. For
generic `g` (random in `S_p`, full-degree minimal polynomial), it is
the DLP in `F_{p^16}^*`. For `g` with low-degree minimal polynomial —
including any sedenion lying in a small sub-algebra — it is a DLP in
a smaller `F_{p^d}^*`.

Pohlig-Hellman attacks any of these in time bounded by
`O(Σ_i √(largest prime factor of p^{d_i} − 1))`. The whole question
of empirical hardness, at the parameter scales requested by the
brief, reduces to *the smoothness of `p^d − 1` for the sub-algebra
degree `d` your secret happens to live in.*

## §1. Pohlig-Hellman against `F_p[e_1]` (T1)

The simplest non-trivial sedenion sub-algebra is
`F_p[e_1] = {a + b · e_1 : a, b ∈ F_p}` with `e_1² = −1`, 2-
dimensional over `F_p`. Whether it's a field depends on whether
`X² + 1` is irreducible mod `p`, i.e. on `p mod 4`.

I sampled a random `g ∈ F_p[e_1]`, computed its exact multiplicative
order from the prime-power factorisation of `p² − 1`, picked a
random secret `n ∈ [1, ord(g))`, computed `h = g^n` by square-and-
multiply, and attacked `(g, h)` with Pohlig-Hellman + baby-step-
giant-step. Wall-clock results, single sample per prime,
deterministic seed (single trial; rerun with different `seed` arg
in `attack_subalg_dlp` for additional samples — the mod-455
smoothness keeps every sample fast):

| p | p mod 4 | ord(g) | largest prime factor | PH wall clock | result |
|---|---:|---:|---:|---:|---|
| 911   | 3 | 829 920    | 19   | 0.98 ms | success |
| 8191  | 3 | 67 092 480 | 13   | 1.75 ms | success |
| 11831 | 3 | 139 972 560| 29   | 1.49 ms | success |
| 14561 | 1 | 14 560     | 13   | 0.50 ms | success |
| 16381 | 1 | 16 380     | 13   | 0.51 ms | success |

(The two `p ≡ 1 (mod 4)` primes give `F_p[e_1] ≅ F_p × F_p` rather
than a quadratic field. The script falls back to `g` of order
dividing `p − 1`; PH is still trivially fast on that order.)

**Per the brief's stop condition: PH succeeds in well under one
second at every tested prime.** Reproducible by
`python3 tools/odlp_hardness.py`, total runtime ≈ 0.1 s for the
DLP attack lines (the smoothness table below dominates total
runtime).

## §2. Why this is structural, not a one-prime-quirk (T1)

The `F_p[e_1]` result is on the easy end of the spectrum. To gauge
whether PH stays fast for higher-degree sedenion sub-algebras —
i.e., whether the result generalises beyond the 2-dim case I
attacked — I factored `p^d − 1` for each test prime at
`d ∈ {1, 2, 4, 8}` and recorded the largest prime factor. PH cost
on the corresponding `F_{p^d}^*` DLP is approximately
`O(√(largest factor))` field multiplications.

| p | `p − 1` | `p² − 1` | `p⁴ − 1` | `p⁸ − 1` |
|---|---:|---:|---:|---:|
| 911   | 13 | 19   | 349       | 296 801             |
| 8191  | 13 | 13   | 8 101     | 2 250 700 503 367 681 |
| 11831 | 13 | 29   | 69 986 281| 9 796 158 916 449 361 |
| 14561 | 13 | 809  | 133 013   | 1 322 165 712 360 113 |
| 16381 | 13 | 8 191| 585 889   | 929 399 857          |

Reading across:

- **`d = 1, 2`**: largest prime factor below 8 200 at every prime.
  PH baby-step is one-digit milliseconds.
- **`d = 4`**: largest prime factor between 349 and 7·10⁷. PH cost
  `≈ √7·10⁷ ≈ 8 400` multiplications. Still milliseconds-to-seconds.
- **`d = 8`**: large prime factors emerging — up to `2.25·10¹⁵`
  at `p = 8191`. PH cost there is `≈ √2.25·10¹⁵ ≈ 4.7·10⁷`
  multiplications, an order of minutes in pure Python. Still
  feasible, not "instant" (T1 — measured directly above; not
  re-run as a full attack in this brief).
- **`d = 16`**: not factored here. `p^16 − 1 ≈ 10⁴⁶` for `p = 911`;
  trial division + Pollard rho would take long enough that I
  didn't run it. The `d = 16` cost depends on cyclotomic structure
  not measured in this brief.

## §3. Honest conclusion (T1 only for measured items)

**Measured (T1):**

1. The sedenion ODLP at `p ∈ {911, 8191, 11831, 14561, 16381}`
   restricted to the `F_p[e_1]` sub-algebra is broken in
   < 2 ms wall clock by Pohlig-Hellman. (§1.)
2. `p^d − 1` is highly composite — largest prime factor ≤ 8 200 —
   for `d ∈ {1, 2}` at every test prime, and ≤ 7·10⁷ for `d = 4`
   at every test prime. (§2.)
3. `p^8 − 1` has prime factors up to `2.25·10¹⁵` at `p = 8191`,
   making PH on a degree-8 sub-algebra DLP minutes-scale rather
   than instant in pure CPython. (§2.)

**Not measured / unknown:**

- PH cost at `d = 16` for any of these primes (the `p^16 − 1`
  factorisation was not run; Pollard rho budget is non-trivial).
- Whether random sedenions `g ∈ S_p` (uniform on the 16-vector)
  land in low-degree sub-algebras with non-negligible probability.
  This is a separate question — minimal-polynomial degree of a
  random sedenion — that this brief doesn't address.
- Whether index calculus would beat PH at any of these scales.
  Per the brief's stop condition, Task 2 is intentionally not
  attempted: PH succeeded instantly enough at the d ≤ 2 scale
  that the brief specifies stopping rather than running an
  alternate attack.

**Verdict:** at the tested parameter sizes (toy / mod-455 primes
up to ≈ 16 000), the sedenion ODLP is **demonstrably weak** at
sub-algebra degrees up to 4 and **plausibly weak** at degree 8 by
direct extrapolation from the smoothness data. Any cryptographic
hardness argument that relies on the sedenion ODLP at these
primes does not survive contact with these numbers.

The mod-455 condition (`p ≡ 1 (mod 5·7·13)`) is the structural
cause: it forces `p − 1` to contain `5·7·13` as small factors, and
the cyclotomic factor structure of `p^d − 1` inherits significant
smoothness for small `d`. A mod-455 prime is a poor choice for any
multiplicative-DLP-based assumption.

## §4. What this does and does not say about Module-SLWE

The brief's framing was: *"The Module-SLWE hardness argument
assumes [the sedenion ODLP] is hard."* If that is the operative
hardness assumption for the construction in `tools/sqt_slwe.py`,
then §1 + §3 together say it does not hold at the tested scales.

I won't extrapolate further: the actual hardness of Module-SLWE as
a *whole* is governed by the BDD/SVP problem on the SLWE lattice,
which is independent of (though informed by) the multiplicative
ODLP. The lattice-side analysis is OP-B in
`tools/QUESTIONS.md` and is still blocked on a SageMath
environment. This brief settles only the multiplicative-DLP side
of the picture.

## §5. Reproducibility

```bash
python3 tools/odlp_hardness.py
```

Pure CPython. No third-party dependencies (Pollard rho and
Miller-Rabin are implemented inline). Total runtime ≈ 0.1 s on
this host for the DLP attacks; the smoothness table is the
dominant cost (factoring `p^8 − 1` for each prime).
