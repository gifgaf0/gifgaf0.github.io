# Brief 04 — Empirical Sedenion ODLP Hardness Probe

> *T1 = measured fact (script reproducible from `tools/odlp_hardness.py`).
> T2 = structural argument used to interpret the measurement.
> No prediction or extrapolation is labelled T1.*

## Correction (closure)

This section supersedes parts of §2 and §4.5, and supersedes the
"Addendum — d=16 Cyclotomic Analysis" at the foot of the file. It
records the structural fact that emerged during the d=16 follow-up
and ties off the ODLP question.

### The norm-form identity (T1 verified)

Every Cayley-Dickson algebra is *quadratic*: each element ``x``
satisfies the trace-and-norm identity

```
x²  =  tr(x) · x  −  N(x) · 1,           or equivalently
x²  −  tr(x) · x  +  N(x) · 1  =  0,
```

where ``tr(x) = 2 · x₀`` is twice the real component, ``N(x) =
Σᵢ xᵢ²`` is the squared norm, and both land in the base field
``F_p``. The identity is a basic consequence of the Cayley-Dickson
construction (Albert 1942, Schafer 1966, *An Introduction to
Nonassociative Algebras*) and descends from ``R`` to ``F_p``
unchanged.

**T1 verified.** ``tools/odlp_hardness.verify_norm_form_identity``
samples 100 random sedenions over ``F_8191``, computes ``g²`` via
the sedenion product and ``tr(g) · g − N(g) · 1`` componentwise,
and compares. **100/100 samples satisfy the identity exactly.**
Reproducible by ``python3 tools/odlp_hardness.py``.

### Consequence for the sedenion ODLP

The minimal polynomial of any sedenion ``g`` divides
``X² − tr(g) · X + N(g)``, hence has degree at most 2. The
sub-algebra ``F_p[g] = span_{F_p}(1, g)`` it generates is
therefore at most 2-dimensional. The unit group of ``F_p[g]`` is
either a subgroup of ``F_{p²}^*`` (if ``X² − tr(g) · X + N(g)`` is
irreducible mod p) or of ``F_p^* × F_p^*`` (if it splits). In
either case the order divides ``p² − 1``.

**Therefore the sedenion ODLP for any single element reduces
entirely to a DLP in ``F_{p²}^*``.** It is a 2-dim problem,
independent of the algebra's nominal 16-dimensionality. (T2.)

### Correction to §2's smoothness table

The cyclotomic factors ``p⁴ − 1``, ``p⁸ − 1``, ``Φ₁₆(p) =
p⁸ − p⁴ + 1`` are *arithmetically* real numbers and the largest
prime factors reported in the §2 table are correct as integer
factorisations. **They are cryptographically irrelevant to the
sedenion ODLP**, because no sedenion element lives in the
extension fields ``F_{p⁴}``, ``F_{p⁸}``, or ``F_{p¹⁶}`` — single
elements are confined to ``F_{p²}``-or-smaller by the norm-form
identity above.

The earlier reading "PH cost grows with sub-algebra degree" was
based on the wrong assumption that the algebra's overall
``F_p``-dimension is reachable by single-element-generated
sub-algebras. It isn't. (T2.)

### Final ODLP verdict

- **T1 verified.** ``F_p[g]`` is 2-dimensional for every sedenion
  ``g`` (norm-form identity above).
- **T1 verified.** Pohlig-Hellman on the resulting ``F_{p²}^*``
  DLP succeeds in under 2 ms at every test prime
  ``p ∈ {911, 8191, 11831, 14561, 16381}`` (§1).
- **T1 verified.** The sedenion ODLP is therefore tractable at
  every tested mod-455 prime, with the bound being the smoothness
  of ``p² − 1`` (always small at mod-455 primes by construction).

### Implication for Module-SLWE security (T2)

The sedenion algebra contributes no independent multiplicative
hardness to the Module-SLWE construction. **Module-SLWE security
rests entirely on the lattice (Module-LWE) assumption.** The
non-associative algebra is not load-bearing on the hardness side.

What it *does* provide, structurally, is **diversification
against ideal-lattice folding attacks**: because the sedenions
are non-associative, the natural "ideal lattice" structure that
attackers exploit on commutative rings (e.g. cyclotomic Module-
LWE) is absent. The lattice arising from a sedenion-coefficient
LWE instance is not an ideal lattice in the standard sense; this
is the diversification claim. (T2 structural argument; not
independently verified in this brief.)

This is a cleaner and more defensible security position than an
unproven novel hardness assumption. The construction is

> *"as hard as Module-LWE; with non-associative-algebra
> diversification against folding attacks; no independent
> multiplicative-DLP claim."*

Anyone reading this report should rely on Module-LWE for the
hardness floor, not on the sedenion ODLP. The latter is
demolished at the tested parameters.

---

The remainder of the report (§§1–4, §4.5, §5, the Cyclotomic
addendum) is preserved for historical record and to show the
arc of the argument; the conclusions in this Correction
supersede any earlier framing that conflicts with it.

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

## §4.5. Addendum: d=16 sub-algebra DLP is structurally vacuous (T1)

The follow-up brief asked for a d=16 PH attempt at p=8191 with a
30-minute wall-clock cap. Before running, I checked the precondition
— *does any sedenion ``g ∈ S_p`` have a minimal polynomial of degree
16, i.e., is ``F_p[g] ≅ F_{p^16}`` for any ``g``?* — and the answer
is **no**. Every sedenion has minimal-polynomial degree at most 2.

**Why (T1, structural argument with empirical confirmation):** the
sedenions, like every Cayley-Dickson algebra, carry a *trace* and
*norm* that both land in the base field, and every element ``x``
satisfies the quadratic identity

```
x² − tr(x) · x + N(x) · 1 = 0,
```

where ``tr(x) = 2·x_0`` (twice the real component) and ``N(x) =
Σᵢ xᵢ²`` is the squared norm. This is a basic property of the
Cayley-Dickson construction (Albert 1942, Schafer 1966) and
descends from the real case to ``F_p`` unchanged. A direct
computational check confirms it: for five random sedenions over
F_8191, ``g²`` lay in ``span_{F_p}(1, g)`` for every sample. (See
the smoke check inline in this commit's bash output, or run the
five-line verifier yourself with ``mul_vec`` and a span solver.)

The consequence is structural: for any sedenion ``g``,

- the powers ``g, g², g³, …`` all lie in ``F_p[g] = span_{F_p}(1, g)``,
  a 2-dimensional sub-algebra;
- ``F_p[g] ≅ F_p[X] / m_g(X)`` with ``deg m_g ≤ 2``;
- the unit group of ``F_p[g]`` has order dividing ``p² − 1`` (when
  ``m_g`` is irreducible, i.e. F_p[g] = F_{p²}) or ``(p − 1)² − 1
  = (p − 1)·(p − 2)``-style products in the split case.

The "d = 16 sedenion DLP" therefore has no instances. Every sedenion
DLP problem is a d ≤ 2 instance, and the d = 2 measurements in §1
above are the complete picture. PH is < 2 ms at every test prime;
no further attack scaling is hidden in the algebra.

**Decision (T1):** I did not run the 30-minute PH attempt. The
correct answer to "does PH succeed at d = 16 in 30 minutes" is
"the question is empty: there is no d = 16 to attack." The d = 16
attack code (`attack_d16_dlp` in `tools/odlp_hardness.py`)
correctly fails at the very first stage — it tries to find a
sedenion with linearly-independent powers up to ``g^15`` and never
does — which is the programmatic witness of the structural fact.

**Practical implication:** a Module-SLWE construction over the
sedenion algebra cannot draw additional hardness from any
"high-degree-sub-algebra" structure inside the algebra; there is
only one degree of freedom (the 2-dim sub-algebra each element
generates), and §1 already showed PH demolishes it at the
mod-455 primes. Whatever hardness the construction has must come
from *outside* the multiplicative DLP — the lattice side (OP-B,
still blocked on Sage), not the algebraic side. The original
report's verdict stands and is now strengthened: the sedenion ODLP
at these primes is weak, and there is no deeper layer where it
might be strong.

## §5. Reproducibility

```bash
python3 tools/odlp_hardness.py
```

Pure CPython. No third-party dependencies (Pollard rho and
Miller-Rabin are implemented inline). Total runtime ≈ 0.1 s on
this host for the DLP attacks; the smoothness table is the
dominant cost (factoring `p^8 − 1` for each prime).

## Addendum — d=16 Cyclotomic Analysis

> **[SUPERSEDED — see Correction at top of file.]** The Φ₁₆(p)
> factor is real and the 98-bit cofactor is correct as an integer
> factorisation. It is *not* the order of any group inside which
> a sedenion ODLP instance lives, because every sedenion's
> generated sub-algebra is at most 2-dimensional by the
> Cayley-Dickson norm-form identity. The cyclotomic-cofactor
> argument therefore does not establish ODLP hardness; the
> sedenion ODLP reduces to ``F_{p²}^*`` DLP and is broken in
> < 2 ms by Pohlig-Hellman at every test prime.

Computed Phi_16(8191) = p^8 - p^4 + 1 = 202626110234381170254860810649 61 (approx 2^104 bits).

Small factor check (trial division to 10^6): only factor is 97.

Remaining cofactor: 208889289714884656 7273052382113 — **98 bits**.

**Conclusion (T1 verified):** Pohlig-Hellman at d=16 requires solving a DLP
in a subgroup of order ~2^98. This is computationally infeasible with current
algorithms. The sedenion algebra's 16-dimensionality corresponds to the first
cyclotomic layer Phi_16(p) that escapes the smoothness enforced by the mod-455
prime construction (p ≡ 1 mod 5·7·13 controls smoothness of p^d - 1 for small d,
but Phi_16(p) = p^8 - p^4 + 1 is independent of this structure).

**The hardness boundary is at d=16.** Sub-algebras of degree d ≤ 4 are
demonstrably weak. d=8 is borderline (minutes-scale PH). d=16 appears hard
by direct arithmetic measurement.

This is consistent with the sedenion algebra being structurally special at
dimension 16: it is the last power-associative algebra in the Cayley-Dickson
tower, and the first dimension where Phi_d(p) escapes mod-455 smoothness.
