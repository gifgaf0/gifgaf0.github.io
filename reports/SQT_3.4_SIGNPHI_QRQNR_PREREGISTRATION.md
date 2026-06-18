# §3.4 sign(φ)↔QR/QNR Consistency Check — Pre-Registration (conventions + criteria, committed before computing)

**Date:** 2026-06-06
**Status:** PRE-REGISTRATION. Written and committed **before** the structure
constants are transformed, so the criteria below — not a post-hoc match — decide
the result. **Scope:** the §3.4.6 consistency test that is now the **sole**
surviving route to the baryon QR/QNR parity (sign(μ̄) was closed-negative as a
parity witness in V4.32 / G2-CHIRAL — μ̄ is reflection-even). This tests the
**registered** map sign(φ)↔QR/QNR against the structure already fixed by
§2.75/§2.76/§2.77/§2.86C. It does **not** assert any observable (matter-vs-
antimatter is not measured here), and it explicitly **excludes** any mirror /
spatial-parity reading as evidence (forced, per §3.4.6).

**Eddington / discipline watch:** ACTIVE. The recent μ̄ episode turned on a
reflection-parity fact taken from memory; here **every** orientation / sign-flip
claim is computed explicitly from the octonion table, never asserted. There is a
real way to fail (criterion C3), and a failure **retires** the map (§3.4.6).

## §1 — Conventions (fixed now)

- **Octonions:** imaginary units e₁…e₇, standard cyclic Fano convention — the 7
  oriented lines are the cyclic shifts {i, i+1, i+3} (mod 7):
  (1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3), with eₐe_b=+e_c on the
  cyclic order (reverse = −), eᵢ²=−1. Structure 3-form φ_{abc} = +1 / −1 / 0 on
  positively-oriented / reverse / non-line triples.
- **QR/QNR:** quadratic residues mod 7 QR={1,2,4} (squares), non-residues
  QNR={3,5,6}; index 7≡0 is the χ-undefined special axis (the e₇-stabilizer axis
  of §2.84A). χ = quadratic character.
- **sign(φ) of a Fano line L={a,b,c}:** the orientation ε(L)∈{±1} with
  eₐe_b = ε(L) e_c in L's canonical (sorted) order. This is the baryon's
  φ-orientation sign: μ̄^φ = φ_{d₁d₂d₃}·μ̄(123), sign(φ)=ε(line of windings).
- **Principal anti-automorphism K:** conjugation e₀↦e₀, eᵢ↦−eᵢ (§2.86C); it
  realizes 𝕆 → 𝕆^op (product-order reversal).
- **Multiplier maps:** for m∈{1..6}, the index map ν_m : i ↦ (m·i mod 7). The
  QR↔QNR involution is ν₋₁ = ν₆ (index negation, the s↦−s of §2.86C); ν₂,ν₄ are
  the Singer (QR) multipliers.
- **Matter/antimatter:** identified with K / the chirality (orientation) Z₂ per
  §2.86C — a *structural* identification, not an observable.

## §2 — Validation criteria (committed; the result is judged against THESE)

| # | Criterion |
|---|---|
| **C1** | **K flips sign(φ) on all 7 lines.** K is the principal anti-automorphism (verify product-order reversal), and 𝕆^op has φ → −φ on every octonion line. [§2.86C] |
| **C2** | **Octonion automorphisms preserve sign(φ).** The Singer 7-cycle (and the QR multipliers) act as genuine automorphisms, fixing every ε(L). [orientation-preserving sanity] |
| **C3** | **CRUX — QR/QNR = the orientation Z₂.** The multiplier maps ν_m split EXACTLY as: m∈QR={1,2,4} orientation-**preserving** (collineations of the octonion Fano plane), m∈QNR={3,5,6} orientation-**reversing** (chirality-swap to the complementary plane). I.e. the QR/QNR partition of (ℤ/7)* coincides with the sign(φ)-preserving / sign(φ)-flipping partition. |
| **C4** | **Arithmetic tie (§2.86C nugget).** χ(−1) = −1 mod 7 ⇒ the seam negation ν₋₁ is a QNR multiplier ⇒ orientation-reversing ⇒ carries the chirality flip — the same Z₂ as K. |
| **C5** | **Distinctness from spatial parity.** sign(φ) is an internal/algebraic octonion-orientation sign; with sign(μ̄) reflection-even (G2-CHIRAL), the QR/QNR chirality and spatial parity do **not** collapse into one Z₂. |

## §3 — Promotion rule (committed)

- If **C1, C2, C3, C4 hold AND C5 holds** → the registered map sign(φ)↔QR/QNR is
  **CONSISTENT** with §2.75/§2.76/§2.77/§2.86C and **PASSES** the §3.4.6 check.
  It promotes from "R3-pending, registered pre-commitment" to **consistency-
  PASSED**: the group-theoretic core (sign(φ)'s Z₂ = the QR/QNR = anti-automorphism
  Z₂) is **R1**; the physical matter/antimatter identification remains **R2** (a
  structural identification — no observable bridge asserted).
- If **C3 FAILS** (the QR/QNR partition is *not* the orientation partition) → the
  map is **INCONSISTENT** and is **RETIRED** per §3.4.6. Reported honestly.
- **Either way:** which orbit is "matter" vs "antimatter" is the **one free
  convention** (§2.84A — "which class is real is the one free choice"); this check
  fixes *structure*, not that observable. The mirror flip / any spatial-parity
  reading is **excluded** as evidence. No sign is faked; the structure-constant
  computation decides.

*Cross-refs: §2.75/§2.76 (QR↔QNR two-orbit chirality), §2.77 (Galois twist on spin
reps), §2.84A (QR/QNR ↔ Re/Im of su(3)), §2.86C (chirality = principal
anti-automorphism; χ(−1)=−1), Paper II §3.4.6 (the registered map),
`reports/SQT_3.4_GOLDEN_LINK_TYPE_CORRECTION.md` (sign(μ̄) reflection-even ⇒ this is
the sole route). Append-only.*
