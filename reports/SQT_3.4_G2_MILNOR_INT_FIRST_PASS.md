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

**V1 robustness (pressure-tested).** The +0.150 is **not** a discretization
artifact: it is **resolution-stable to four digits** (0.1498 across n = 400→1200
and solid-angle subsample every = 2/4/8) and falls off **smoothly and
monotonically** as 3-linkedness breaks — sep 0/1/2/4 → 0.150 / 0.041 / 0.003 / 0,
with the split control pinned at 0. So the integral is a converged,
(largely) configuration-independent functional that detects 3-linkedness by a
genuinely different route than the triple-point count. **Precision:** 0.150 is
*un-normalized* — it cross-checks the **binary** |μ̄| (nonzero on Borromean, zero
on split), **not** the quantitative value 1; the normalization is part of what
the (still-open) jump-correction would supply.

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

The genuine chiral μ̄ requires a **reflection-odd** construction, and — per the
sign's danger — it must itself get the **two-method discipline** the magnitude
just received. The cleaner pairing (agent steer):

1. **The oriented Seifert triple-point count** — the *combinatorial* sign,
   computed directly and robustly from the piercing orientations and disk
   co-orientations. This is the cleaner route to the sign than regularizing the
   jump inside the integral.
2. **The reflection-odd Massey integral** — the jump-correction term (C₃'s ±4π
   crossings through C₁'s Seifert disk), as the *independent* cross-check.

Both must pass (V1)–(V3) (split→0, mirror→flip, |·|→integer), with the
**piercing / co-orientation conventions pre-committed before any sign is read**
(the jump term's sign/normalization is exactly where a wrong "clean ±1" hides).
Only then does sign(μ̄) promote out of R3-pending — and even then it promotes
**only** the witness↔invariant identification, **not** the substantive
sign(φ)↔QR/QNR map (still R3-pending its §2.75/§2.76/§2.86C consistency check).
Until then the registration's guard holds: the mirror flip is **not** evidence.

## §INT.5 — Proposed Part VI open-task update

| Task | Status |
|---|---|
| §3.4-G2-Milnor-INT (Massey integral) | **First pass: PARTIAL (R1).** Independent integral confirms 3-linkedness (V1: split→0, Borromean nonzero) — a second magnitude method. But the naive ∮Ω₁(B₂·dl₃) is **reflection-even** (V2 fails) ⇒ NOT the chiral μ̄; the rigorous sign(μ̄) stays **R3-pending** the Massey jump-correction (the odd term, not faked). |

*Reproduce: `python3 tools/g2_milnor_int.py`. Append-only; no prior ledger
content modified. Cross-refs: §3.4-G2-Milnor (the config-specialized count +
witness), `SQT_3.4_SIGNMAP_REGISTRATION.md` (the sign-map this would promote).*
