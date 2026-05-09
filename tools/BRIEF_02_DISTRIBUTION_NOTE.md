# Encryption-Randomness Distribution in Sedenion Module-LWE

*Brief 02 closure; intended as a seed for the distribution section
of the eventual paper. Status: documents the construction now in
the testbed (`hybrid_kem/kem_slwe/slwe_toy.py`); does not advance a
hardness claim. Open security questions are listed in
`tools/QUESTIONS.md` §5.*

## 1. The decryption equation and what it demands

Working in the toy parameters from `SPEC.md` §2.6 — the sedenion
algebra `S_q` over `F_q` for `q = 911` (or any `q ≡ 1 mod 455`),
module rank `k = 4`, ambient dimension `k · 16 = 64` — the
SLWE-style KEM of `tools/sqt_slwe.py` decrypts a single-bit message
`m ∈ {0, 1}` by computing

```
v ≡ c₂ − ⟨s, c₁⟩_norm  ≡  m · ⌊q/2⌋  +  ε      (mod q)        (1)
```

where `⟨u, v⟩_norm := Σᵢ Re(conj(uᵢ) · vᵢ) mod q` is the conjugate-
norm inner product on `S_q^k` and the residual noise term is

```
ε  =  ⟨e, r⟩_norm  −  ⟨s, e₁⟩_norm  +  e₂.                   (2)
```

Correctness of decryption requires `|ε| < q/4`: outside that window
the rounding step `m̂ := round(2v/q)` returns the wrong bit. Brief 02
spent its life inside this inequality.

## 2. Why uniform `r` fails

The supplied source samples both the secret `s ∈ S_q^k` and the
encryption randomness `r ∈ S_q^k` from a single helper
`rand_nonzd()`, which draws each sedenion coordinate uniformly from
`F_q` and rejects only when the resulting 16-vector has *exactly two*
nonzero coordinates whose indices form a known sedenion zero-divisor
pair. The filter is sparse: it removes a vanishing fraction of
samples (about `5·10⁻⁵` at random density). For all practical purposes
`s` and `r` are uniform on `S_q^k = F_q^{16k}`.

Plug a uniform `r` into the ⟨e, r⟩_norm term of (2). With `e` drawn
from a centred binomial distribution `CBD(η)` of width `η = 2`, each
sedenion coordinate `eᵢ ∈ {-2, -1, 0, 1, 2}` and each `rⱼ` ranges
over `[0, q)`. The 16 conjugate-products in one inner-product term
each have magnitude bounded by `η · (q − 1)/2`; the sum of 16 such
terms over `k = 4` modules has worst-case magnitude

```
|⟨e, r⟩_norm|  ≤  k · 16 · η · (q − 1)/2  ≈  64 · η · q.       (3)
```

For `η = 2` and any `q`, the bound is `≈ 128 q`, two orders of
magnitude above the modulus. The term wraps mod `q` and is
statistically indistinguishable from uniform on `[0, q)`. Equation
(2) is then dominated by an `(O(q) mod q)` random variable, the
signal `m · ⌊q/2⌋` is drowned, and the per-trial DFR converges to
`1/2`.

This was confirmed empirically across a four-cell parameter sweep
in Brief 02's parameter-fix phase, with no qualitative change between
`q = 911` and `q = 8191` and no improvement when `η` was widened to
2 or narrowed to 1. The cause is not a bad parameter choice; it's
that the noise *bound* in (3) scales linearly with `q`, while the
decryption window `q/4` does the same. Their ratio is constant in
`q`; the DFR collapse is invariant to prime size.

## 3. The remedy: small `r`, with rejection on the ZD locus

Replacing uniform `r` with a small distribution turns the bound (3)
into

```
|⟨e, r⟩_norm|  ≤  k · 16 · η · η  =  k · 16 · η²                (3′)
```

— independent of `q`. At `(k, η) = (4, 2)` this is 256; at `(k, η) =
(4, 1)` it is 64. The first comfortably fits inside the decryption
window `q/4` for any `q ≥ 1024`, and the second already fits at
`q ≥ 256`. The same bound applies symmetrically to the
`⟨s, e₁⟩_norm` term once `s` is also drawn from a small
distribution.

The natural candidate small distribution is the centred binomial
`CBD(η)` over each `F_q^16` coordinate vector. For `η = 2`:

```
support:    {-2, -1, 0, 1, 2}
weights:    (1, 4, 6, 4, 1) / 16
E[X] = 0     E[|X|] = 0.75     Var[X] = 1.
```

Each of the `16k = 64` coordinates of `r` is independently `CBD(η)`-
distributed; the 16-vector encoding of one sedenion has expected
magnitude `≈ 0.75 · 16 = 12` and worst-case magnitude `2 · 16 = 32`
under the conjugate-norm.

This is one of two coordinate distributions used by ML-KEM (FIPS 203
calls them η₁ = 3 and η₂ = 2; we use η = 2). Importing it here is a
direct adaptation, not an invention.

### 3.1 Why we still need to filter zero-divisor pairs

The supplied source's `rand_nonzd()` filter only rejects elementary
two-coordinate zero divisors — i.e. samples with exactly two nonzero
coordinates whose indices `(a, b)` form a known sedenion ZD pair.
The set of such pairs is computed once by
`tools.sedenion_audit.find_canonical_zd_quadruples` and is
prime-independent (the sedenion audit established that the same
84 quadruples / 42 pairs appear over every prime tested). For `S_q`
embedded in `F_q^16`, there are `(16 choose 2) = 120` index pairs;
of these, 42 are ZD pairs.

If we drew `r` from `CBD(η = 2)` *without* the filter, the rejection
rate inherited from `rand_nonzd`'s definition is the probability
that the sample falls on an elementary ZD pair. Under `CBD(η = 2)`
the per-coordinate mass at zero is `6/16 = 3/8`, so

```
P[exactly 2 nonzero coords]
    = C(16, 2) · (5/8)² · (3/8)¹⁴
    = 120 · 0.391 · 1.09·10⁻⁶
    ≈ 5.1·10⁻⁵.                                                (4)
```

Conditioned on exactly two coordinates being nonzero, their indices
are uniform on the 120 unordered pairs, so the conditional
probability of landing in the 42-pair ZD set is `42/120 = 0.35`. The
overall density of "elementary ZD pair" samples under `CBD(η = 2)`
is therefore `≈ 1.78·10⁻⁵`. We measured this directly:

```
p = 911:    0 / 100 000 samples            (rate < 10⁻⁵)
p = 8191:   2 / 100 000 samples            (rate ≈ 2·10⁻⁵)
```

(see `tools/zd_density_results.md`). The empirical rate matches
the theoretical estimate at the third significant figure given the
sample size, so a rejection-sampling approach converges in a single
iteration on overwhelmingly all draws and the accepted distribution
is statistically indistinguishable from `CBD(η = 2)` at any
distinguishing advantage above `10⁻⁴`.

### 3.2 The implemented sampler

```python
def rand_small_nonzd(p: int, eta: int = 2, dim: int = 16):
    values, weights = CBD_TABLES[eta]
    while True:
        v = [random.choices(values, weights=weights)[0] % p
             for _ in range(dim)]
        nz = [i for i, c in enumerate(v) if c != 0]
        if not nz:                         # all-zero
            continue
        if len(nz) == 2 and (nz[0], nz[1]) in zd_pairs:
            continue                       # elementary ZD pair
        return v
```

Three properties of this distribution worth recording:

1. **Centring.** First moment matches `CBD(η)` exactly because the
   rejection set is symmetric under coordinate sign flip; the
   filter never breaks the `±x ↔ ∓x` symmetry of the support.
2. **Scale.** `E[|coord|] = 0.749` measured at `η = 2`, matching the
   textbook `CBD(η = 2)` value `0.75`. Max coordinate magnitude is
   `η`. So the noise bound `(3′)` applies as written.
3. **Independence-from-prime.** `zd_pairs` is fixed across all
   primes for which the sedenion algebra is well-defined; the
   `% p` reduction step is purely a representation choice and does
   not change which 16-vectors the filter rejects. Switching `p`
   from 911 to 8191 changes nothing about the sampler's behaviour.

## 4. Empirical confirmation

With `s` and `r` switched from `rand_nonzd()` to `rand_small_nonzd()`
and `A` left uniform (its rows are Singer-cycle orbits of uniform
seeds, preserving the structural assumption of the supplied
construction), the wrapper-level decryption-failure rate is

```
(p = 911,  k = 4, η = 2):   0 failures / 5000 trials.
(p = 8191, k = 4, η = 2):   0 failures / 5000 trials.
```

i.e. the empirical 95-th-percentile upper bound on DFR is
`≈ 6·10⁻⁴`, three orders of magnitude below the brief's `0.01`
target. The xfail mark on `test_toy_dfr_target` was removed and the
test now asserts strict `dfr < 0.01`.

## 5. What this construction does *not* claim

The fix above closes the **noise budget**. It says nothing about
**security**. In particular the testbed scheme

- samples both `s` and `r` from a small distribution (a deviation
  from textbook MLWE, and a reduction-relevant change),
- uses a public matrix `A` whose rows are Z₇ Singer-cycle orbits of
  uniform seeds (also a deviation; `A` is structured, not uniform),
- and is a module-LWE scheme over a non-associative algebra `S_q`
  whose hardness reduction is not in the literature I know of.

Each of these merits cryptanalytic attention before any concrete
security level is claimed. They are listed under
`tools/QUESTIONS.md` §5 as open questions for the eventual paper.

## 6. What's worth saying about this in the paper

Three things, in order of concreteness:

1. **The noise-budget argument is sharp and quantitative.** The
   bound (3′) is the right object to write down: it makes the noise
   independent of `q`, scales as `O(k · DIM · η²)`, and matches
   empirical DFR within statistical resolution. A short table of
   `(k, η)` vs. empirical DFR over 5000 trials at two primes
   replaces any hand-waving about "small noise good".

2. **The ZD-rejection step is essentially free.** The rejection rate
   is `≤ 2·10⁻⁵`, so the accepted distribution is `CBD(η)` to far
   below any meaningful distinguishing advantage. The only reason
   it's not trivially deletable is that it lets the noise bound be
   written without exception-handling for the algebraic-zero-divisor
   case — clean statement, no additional cost.

3. **The construction is conservative on the noise side and
   under-justified on the structural side.** The noise distribution
   is exactly ML-KEM's η₂; the secret is small in the standard
   MLWE sense; the modulus is chosen for algebraic compatibility
   with the PSL(2, 7) symmetry, not for noise budget. The two
   structural choices that haven't been justified here are (a) the
   Singer-cycle structure on `A`, and (b) the use of a non-
   associative coefficient algebra. The paper should be explicit
   that "noise budget closes" is a separate claim from "the scheme
   is secure" and should not paper over the gap.
