# Zero-Divisor Pair Graph Audit on R_3329

## Setup recap

Task 1 emits the CRT decomposition

```
R_3329 = Z_3329[X] / (X^256 + 1)
       ≅ ⨁_{j=0}^{127} F_3329[X] / (X^2 − r_j)
```

with `r_j = ζ^{2j+1}, ζ = 17, ord(ζ) = 256`.

A separate check (`pow(17, (q−1)/2, q) = −1`) shows **17 is a quadratic
non-residue in F_3329**, hence every odd power of 17 is a non-residue,
hence every `X^2 − r_j` is irreducible, hence each quotient is the
quadratic field extension F_{q²} = F_{3329²}. Therefore

```
R_3329 ≅ (F_{3329²})^{128}
```

as F_3329-algebras. **No factor contains an internal zero divisor**;
all zero divisors of R come from the product structure.

## ZD pair graph as defined

> "Build the ZD pair graph for elements supported on pairs of CRT
> factors."

Take vertices V = {0, 1, …, 127} (the 128 CRT factors). For an
unordered pair `{i, j}, i ≠ j`, an *element supported on {i,j}* is one
of the form `e_i · α + e_j · β` with `α, β ∈ F_{q²}, α, β ≠ 0`, where
`e_i` is the idempotent of factor i.

Such an element is a zero divisor whenever there is a *complementary*
nonzero element `x` with the support·support product zero. The
universal witness is `x = e_k` for any `k ∉ {i, j}`: orthogonality of
idempotents gives `(e_i α + e_j β) · e_k = 0`. So **every** pair is a
ZD-pair, and the ZD pair graph is the complete graph

```
G_ZD = K_128
```

(128 vertices, C(128, 2) = 8128 edges).

This is unsurprising: for any product-of-fields ring, two elements with
disjoint support multiply to zero, so every two-vertex support pattern
yields zero divisors. The graph carries no information beyond "the
ring is a product of 128 fields"; its automorphism group is the full
symmetric group:

```
Aut(G_ZD) = Sym(128).
```

## The PSL(2,7) / K_{7,7} question

The brief asks:

> Does PSL(2,7) act on the 128 factors (via the Z₇ subgroup found in
> Task 2) in a way that produces a K_{7,7}-like subgraph among any 14
> factors?

Two issues, in order:

1. **No Z₇ in F_3329×.** Per Task 2, `7 ∤ |F_3329×|`. The action route
   the brief specifies has no input; the question as posed is empty.

2. **Even if a Z₇ existed:** a `K_{7,7}` subgraph "among any 14
   factors" is automatic in a complete graph. Any 14-vertex subset of
   K_128 induces K_14, and K_14 contains every K_{a,b} with a+b ≤ 14
   as a subgraph, including K_{7,7}. So the condition "produces a
   K_{7,7}-like subgraph" is trivially satisfied by any choice of 14
   factors — it carries no algebraic content. The non-trivial form of
   the question would be **"is K_{7,7} a *natural* substructure
   distinguished by an automorphism of G_ZD induced by PSL(2,7)?"** —
   which we cannot answer because the prerequisite Z₇ action does not
   exist.

## Restricted automorphism structure

Per the brief: *"Report the automorphism structure of the ZD graph
restricted to any Z₇-orbit-closed subset of factors."* With no Z₇
action on the 128 factors, the only Z₇-invariant subsets are the
empty set and the full set. Their induced subgraphs are the empty
graph and `K_128`. Their automorphism groups are the trivial group
and `Sym(128)` respectively.

## Natural finer structure that *does* exist

Two cyclic structures are inherited from the ring rather than imposed
externally:

- **Multiplication by ζ²** permutes the factors via the index map
  `j ↦ (j + 1) mod 128` (since `r_{j+1} = ζ² · r_j`). This embeds
  Z/128 ⊂ Sym(128), and the orbit is the full 128-set.

- **The involution `X ↦ X⁻¹`** sends `r_j = ζ^{2j+1}` to
  `r_j^{-1} = ζ^{-(2j+1)} = ζ^{256−(2j+1)} = ζ^{255−2j}`. With
  `2j′ + 1 = 255 − 2j` we get `j′ = 127 − j`. This is a fixed-point-free
  involution on {0, …, 127} (since 127 is odd, no `j` equals
  `127 − j`).

Together these generate a dihedral subgroup `D_128 ⊂ Sym(128)` of
order 256, acting on the ZD graph by graph automorphisms. (Every
graph automorphism of K_128 is a graph automorphism, so the
restriction is trivially preserved — but `D_128` is the structure
that the *ring* singles out, not the graph.)

## Summary table

| Item | Result |
|---|---|
| CRT shape of R_3329 | `(F_{3329²})^{128}` |
| Internal ZDs per factor | none (each factor is a field) |
| ZD pair graph | `K_128` |
| `Aut(G_ZD)` | `Sym(128)` |
| Z₇ action via field-multiplication | does not exist (`7 ∤ q − 1`) |
| K_{7,7} as a subgraph | trivially present in any 14-vertex subset, no algebraic content |
| Natural ring-induced subgroup of `Aut(G_ZD)` | dihedral `D_128` of order 256 |

Per the brief: raw findings only, no interpretation.
