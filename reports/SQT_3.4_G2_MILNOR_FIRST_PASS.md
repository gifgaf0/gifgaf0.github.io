# §3.4-G2-Milnor First Pass — The φ-Weighted Triple Invariant on the Baryon

**Date:** 2026-06-03
**Register:** **R1** for the validated magnitude and the sign-independence
structure + **R3** for the open integral cross-check and the field-soliton step.
**Tool:** `tools/g2_milnor.py`. **Gate:** the baryon gate pre-registered in
`reports/SQT_3.4_G2_BORROMEAN_FIRST_PASS.md` §GB.2.
**Eddington watch:** ACTIVE — a reflection-even sign method was caught by the
built-in mirror control and replaced (logged below); the physical sign-map is
left as a framework pre-commit, not read off.

> **Gate.** G2-orient's Hopf charge is the meson (pairwise) sector and is blind
> to the Borromean baryon. The baryon's content is the cubic Milnor triple-
> linking μ̄(123). This computes the φ-weighted version μ̄^φ = φ_{d₁d₂d₃}·μ̄(123),
> with the pre-registered magnitude as the falsifiable core and the sign
> disentangled into its two independent pieces.

## §GM.1 — Results (R1)

| Quantity | Result | Status |
|---|---|---|
| \|μ̄\|, Borromean | **1** | textbook value ✓ |
| \|μ̄\|, split/unlink control | **0** | non-Borromean ⇒ 0 ✓ |
| \|μ̄\|, spatial mirror | **1** | \|μ̄\| reflection-invariant ✓ |
| **sign(μ̄)** (polar handedness) | **+0.45 → −0.45** under mirror | chiral, flips ✓ |
| **sign(φ)**, line (0,1,3) vs QNR (0,3,1) | **+1 → −1** | flips under reassignment ✓ |
| **\|μ̄^φ\|**, Fano line + Borromean | **1** | predicted 1 ✓ |
| **\|μ̄^φ\|**, non-line + Borromean | **0** | predicted 0 ✓ |
| **\|μ̄^φ\|**, Fano line + split | **0** | predicted 0 ✓ |

**Magnitude (the falsifiable core).** μ̄(123) is computed as the number of
transverse triple points of the three flat Seifert disks bounded by the three
strands — a method *validated on controls*: it returns the textbook |μ̄| = 1 on
a genuine Borromean (three orthogonal golden ellipses), **0** on a split/unlink
control, and is reflection-invariant. The φ-weighting then gives, as
pre-registered:

> **|μ̄^φ| = 1 if and only if (the windings form a Fano line AND the link is
> genuinely Borromean); 0 off-line; 0 on a non-Borromean link.** All three
> committed predictions hold.

This is the baryon-sector realization of the arity ladder: a cubic (triple)
invariant, matching the 3-point Fano lines and the associative 3-form φ, nonzero
exactly where G0 said Fano structure first becomes possible.

## §GM.2 — The two independent signs (R1 for the structure)

μ̄^φ = sign(φ)·|μ̄|·sign(μ̄) couples **two independent ±1 signs**, which flip under
**two independent operations** (all four combinations realized):

| windings | space | μ̄^φ |
|---|---|---:|
| Fano line | config | **+1** |
| Fano line | mirror | **−1** |
| QNR-conjugate | config | **−1** |
| QNR-conjugate | mirror | **+1** |

- **sign(μ̄)** — the geometric Borromean handedness — flips under a **spatial
  mirror** (verified: the polar handedness pseudoscalar +0.45 → −0.45).
- **sign(φ)** — the octonion orientation of the winding assignment — flips under
  **cyclic (QR↔QNR) reassignment** of the windings (φ_{013} = +1, φ_{031} = −1).

They are independent because the two operations are independent.

## §GM.3 — The physical sign-map: a framework pre-commit, NOT asserted

```
   sign(μ̄)  [flips under spatial mirror]       ↔  ???
   sign(φ)   [flips under QR↔QNR reassignment]   ↔  ???
```

Which **physical** chirality maps to which **computed** sign is a §2.75/§2.76
call that must be **registered before** it is read as a result — "sign =
chirality" is matchable to either, so reading it off post-hoc would be an
Eddington maneuver. The genuinely registrable prediction is whether **spatial
parity** and the **QR/QNR algebraic chirality** are *distinct* (one encoded in
each sign) or *coincide*. This computation supplies the two independent signs;
it does **not** decide the map.

## §GM.4 — Caught, not hidden (the control working)

A first attempt computed sign(μ̄) = sign det[surface normals]. That is a triple
product of **pseudovectors** and is **reflection-EVEN** — it *failed* the
built-in mirror control (μ̄ did not flip). It was replaced by the configuration's
**polar-vector** handedness pseudoscalar (reflection-odd, mirror-validated). The
normals still correctly certify the triple point is transverse (the
reflection-invariant magnitude). This is the same pseudovector trap caught in
G2-Borromean §(B) — the control discipline catching it again, by design.

## §GM.5 — Scope / open (honest)

- **Established (R1):** the pre-registered **magnitude** (|μ̄^φ| selection rule,
  validated on controls) and the **two-sign independence structure**.
- **Open — the two genuine remaining steps:**
  1. **The independent third-order-helicity (Massey) INTEGRAL** — both a *second*
     magnitude method (cross-check of the triple-point count) **and** the
     rigorous chiral sign(μ̄). The polar-handedness sign here is a validated
     chirality *detector*, not the rigorous invariant; the integral is the
     authority. **Not faked.**
  2. **The field-soliton realization** — whether a stable **Faddeev–Hopf** field
     soliton realizes a Borromean three-strand at all (Hopf solitons are π₃(S²)
     objects; Borromean field configs are exotic). This is the real **G2-knot**,
     deferred; brute-force soliton relaxation stays held.
- **Does NOT** assert any observable bridge or close §2.15.

## §GM.6 — Proposed Part VI open-task update

| Task | Status |
|---|---|
| §3.4-G2-Milnor (φ-weighted μ̄ — magnitude + sign structure) | **First pass CLOSED (R1):** |μ̄^φ| selection rule validated on controls (1 iff Fano-line genuine Borromean, 0 else); two independent signs (spatial-mirror sign(μ̄), QR↔QNR sign(φ)) exposed. Physical sign-map = framework pre-commit. |
| §3.4-G2-Milnor-INT (3rd-order-helicity integral; 2nd magnitude method + rigorous chiral sign) | **Open** — the remaining independent cross-check. |
| §3.4-G2-knot (field-soliton Borromean realization) | **Open — deferred hard step.** |

*Reproduce: `python3 tools/g2_milnor.py`. Append-only; no prior ledger content
modified. Cross-refs: §3.4-G2-Borromean (setup), §3.4-G2-orient (meson sector),
§2.15 (Borromean), §2.75/§2.76 (QR/QNR), §3.4-G0 (arity ladder).*
