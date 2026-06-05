# §3.4-G2-Milnor-INT First Pass — The Massey Integral: Magnitude Cross-Check, Sign Still Pending

**Date:** 2026-06-04
**Register:** **R1** for the magnitude-level result (an independent integral
detects 3-linkedness) + the honest negative (the naive integral is
reflection-even ⇒ not the chiral μ̄). **Tool:** `tools/g2_milnor_int.py`.
**Gate:** §3.4-G2-Milnor-INT (the configuration-independent authority opened in
the V4.29 ladder).
**Eddington watch:** ACTIVE — the rigorous chiral sign was **not** delivered and
is **not** faked; the mirror control caught that the naive integral is even.

> **Goal.** Provide the config-independent cross-check of §3.4-G2-Milnor: (a) a
> second magnitude method, independent of the config-specialized Seifert
> triple-point count, and (b) the rigorous *topological* sign(μ̄) — which would
> promote the reflection-odd handedness *witness* of `g2_milnor.py` to the genuine
> invariant and the registered sign-map's substantive half off R3-pending.

## §INT.1 — Method

The Gauss–Massey integral via solid-angle potentials (computed from scratch —
Van Oosterom–Strackee solid angle over a disk triangulation, discrete
Biot–Savart field):

    I = (1/4π) ∮_{C₃}  Ω₁(x) · (B₂(x)·dl₃),

with Ω₁ the solid angle subtended by C₁ (∇Ω₁ = −4π B₁; jumps 4π across a Seifert
surface) and B₂ the Biot–Savart field of C₂ (∮_{Cj} B_i·dl = lk(i,j)). Genuinely
independent of the triple-point count, and configuration-independent. Pre-stated
validation criteria: (V1) split ⇒ I≈0; (V2) mirror ⇒ I→−I (reflection-odd =
the rigorous sign); (V3) |I| equal for config and mirror, integer after norm.

## §INT.2 — Result (R1; pairwise lk verified ≈ 0)

| | I = (1/4π)∮Ω₁(B₂·dl₃) | criterion |
|---|---:|---|
| Borromean | **+0.150** | — |
| split / unlink | **0.000** | **(V1) ✓** |
| spatial mirror | **+0.150** | **(V2) ✗ — does NOT flip** |

**(V1) holds — an independent magnitude cross-check.** The integral vanishes on
the split/unlink and is nonzero on the genuine Borromean. So a configuration-
independent route confirms the Borromean is genuinely 3-linked and the split is
not — corroborating the triple-point count's |μ̄| : 1 vs 0 by a different method.

**(V2) fails — and the diagnosis is exact.** The integral is **reflection-EVEN**
(+0.150 → +0.150 under mirror), so it is **not** the chiral Milnor invariant.
`∮ Ω₁(B₂·dl₃)` is a product of **two** reflection-odd factors — the solid angle
Ω₁ and the pseudoscalar B₂·dl₃ — hence even. The chiral part of μ̄ lives in the
**Massey jump-correction**: Ω₁ jumps by 4π where C₃ pierces C₁'s Seifert disk,
and that crossing term is the reflection-**odd** piece. It was **not computed
here and not faked**.

## §INT.3 — Consequence (exactly the registered status)

- The rigorous **topological sign(μ̄) is NOT yet delivered.** It stays **R3-
  pending**, precisely where `SQT_3.4_SIGNMAP_REGISTRATION.md` put it. The
  handedness *witness* of `g2_milnor.py` is **not** promoted to the invariant by
  this attempt; the registered sign-map's substantive half (sign(φ)↔QR/QNR)
  likewise stays R3-pending its §2.75/§2.76/§2.86C consistency check.
- What is robust from `g2_milnor.py` **stands unchanged**: the magnitude
  selection rule (R1) and the two-sign factorization (R1). This first pass
  **adds** an independent magnitude-level confirmation (V1) and **subtracts
  nothing**.

## §INT.4 — What remains (the precise next step)

The genuine chiral μ̄ requires a **reflection-odd** construction. Two routes:
1. **The Massey jump-correction term** — add the contribution of C₃'s crossings
   through C₁'s Seifert disk (each a ±4π jump in Ω₁), which is the odd piece. The
   sign/normalization of that term is the delicate part — to be done with the
   same two-method care, not rushed.
2. **A grid third-order-helicity** with an explicitly odd integrand (e.g. a genuine
   Massey product of the three Biot–Savart fields), validated on the same
   controls (split→0, mirror→flip, |·|→integer).

Either must pass (V1)–(V3) before sign(μ̄) promotes out of R3-pending. Until then,
the registration's discipline holds: the mirror flip is **not** evidence.

## §INT.5 — Proposed Part VI open-task update

| Task | Status |
|---|---|
| §3.4-G2-Milnor-INT (Massey integral) | **First pass: PARTIAL (R1).** Independent integral confirms 3-linkedness (V1: split→0, Borromean nonzero) — a second magnitude method. But the naive ∮Ω₁(B₂·dl₃) is **reflection-even** (V2 fails) ⇒ NOT the chiral μ̄; the rigorous sign(μ̄) stays **R3-pending** the Massey jump-correction (the odd term, not faked). |

*Reproduce: `python3 tools/g2_milnor_int.py`. Append-only; no prior ledger
content modified. Cross-refs: §3.4-G2-Milnor (the config-specialized count +
witness), `SQT_3.4_SIGNMAP_REGISTRATION.md` (the sign-map this would promote).*
