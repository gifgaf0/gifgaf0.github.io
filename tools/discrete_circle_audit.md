# Discrete-Circle / (2,3,7)-Angle Audit on the 256-th Roots of Unity in F_3329

## Setup

The 256-th roots of unity in F_3329 are `ζ^k` for `k = 0, …, 255`,
where `ζ = 17` is the canonical generator (FIPS 203). The
**primitive** 256-th roots are those with `gcd(k, 256) = 1`,
i.e. `k` odd, giving exactly φ(256) = 128 of them.

Treating discrete logs as angles in units of `2π/256`, the
hyperbolic (2,3,7) triangle has angles `π/2 : π/3 : π/7 = 21 : 14 : 6`
in units of `π/42`.

## Definition of a "(2,3,7) triple"

We say an unordered triple `{k₁, k₂, k₃}` of distinct integers in
Z/256 is **(2,3,7)-proportional** iff there exist `m ∈ Z/256` and a
permutation `π` of `(21, 14, 6)` such that

```
{k₁, k₂, k₃} = { m · π(0)  mod 256, m · π(1) mod 256, m · π(2) mod 256 }.
```

Two domains of interest:

- **Restricted to primitive 256-th roots** — both `k_i` odd.
- **Full circle** — any `k_i ∈ Z/256`.

## Findings

Computed by exhaustive enumeration over `m ∈ Z/256` and the six
permutations of `(21, 14, 6)`; all data reproducible from
`tools/_discrete_circle.py` and dumped verbatim into
`tools/discrete_circle_audit.json`.

| Quantity | Restricted to primitives | Full circle |
|---|---:|---:|
| Population (n) | 128 | 256 |
| Total unordered triples | C(128, 3) = 341 376 | C(256, 3) = 2 763 520 |
| (2,3,7)-proportional unordered triples | **0** | 248 |
| Match rate vs. uniform random | **0** | 8.97 × 10⁻⁵ |

### Parity obstruction (raw observation, no interpretation)

For all `m ∈ Z/256`, `14·m mod 256` is even and `6·m mod 256` is
even. A (2,3,7)-proportional triple therefore contains at most one
odd coordinate (the `21·m` slot when `m` is odd). Primitive 256-th
roots correspond to **odd** indices, so a triple of primitive 256-th
roots can contain at most one (2,3,7) coordinate, never the required
three. Hence the restricted count is exactly 0.

### Examples from the full-circle enumeration

First eight unordered (2,3,7)-proportional triples in `Z/256`,
sorted lexicographically (taken from the JSON dump):

```
(1, 86, 110)
(2, 3, 74)
(2, 7, 90)
(2, 74, 131)
(2, 90, 135)
(2, 172, 220)
(4, 6, 148)
(4, 14, 180)
```

(These are not primitive 256-th roots in general. For instance
`{1, 86, 110}`: `1` is primitive, `86 = 2·43` and `110 = 2·55` are
not.)

### Comparison to a uniform-random null

For a uniformly random unordered triple drawn from Z/256, the rate
of (2,3,7)-proportional triples is `248 / 2 763 520 ≈ 8.97 × 10⁻⁵`.
For a uniformly random unordered triple drawn from the 128
primitive 256-th roots, the rate is exactly **0** (the 128-set
contains no such triples by the parity obstruction).

## Summary

| | |
|---|---:|
| Primitive 256-th roots in F_3329 | 128 |
| (2,3,7)-proportional triples among primitives | 0 |
| (2,3,7)-proportional triples in full circle | 248 |
| Excess over uniform random (primitives) | 0 (the natural null is also 0 by parity) |
| Excess over uniform random (full circle) | none — the count *equals* the uniform-random expectation by definition |

Per the brief: raw findings only. M. Gifford to interpret.
