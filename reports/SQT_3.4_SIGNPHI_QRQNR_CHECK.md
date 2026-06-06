# §3.4 sign(φ)↔QR/QNR Consistency Check — PASSED: the φ-Orientation Sign Carries the QR/QNR Chirality

**Date:** 2026-06-06
**Register:** **R1** for the group-theoretic core (sign(φ)'s Z₂ = the QR↔QNR =
principal-anti-automorphism Z₂); **R2** for the matter/antimatter identification
(structural — no observable asserted). **Pre-registration:**
`reports/SQT_3.4_SIGNPHI_QRQNR_PREREGISTRATION.md` (criteria committed before
computing). **Tool:** `tools/signphi_qrqnr_check.py`.
**Eddington watch:** ACTIVE — every orientation/sign-flip was **computed** from
the octonion table, none asserted; the crux C3 was falsifiable and could have
retired the map.

> **The §3.4.6 consistency check — the *sole* surviving route to the baryon
> QR/QNR parity after sign(μ̄) was closed-negative (V4.32) — PASSES.** The
> baryon's φ-orientation sign, sign(φ) = ε(line of the three winding directions),
> is flipped by exactly the operation that swaps QR↔QNR and is the framework's
> chirality / matter–antimatter operation (the principal anti-automorphism of
> §2.86C), and is fixed by exactly the QR-preserving octonion automorphisms.
> The registered map sign(φ)↔QR/QNR is therefore **consistent** with
> §2.75/§2.76/§2.77/§2.86C and **promotes** from R3-pending.

## §1 — What was tested (and how it could have failed)

Paper II §3.4.6 registered — as a *pre-commitment*, not a result — that the
baryon's φ-orientation sign carries the QR/QNR algebraic chirality of §2.75/§2.76,
with the explicit instruction that it be **promoted only on a consistency check**
against how QR/QNR already enters the framework (the §2.77 Galois twist, the
§2.86C principal anti-automorphism, and the matter/antimatter assignment), and
**never on a mirror flip**. With sign(μ̄) now reflection-even (closed-negative as a
parity witness, V4.32 / G2-CHIRAL), this is the **only** route left to the baryon
parity.

The decisive, falsifiable test (pre-registered crux **C3**): *does the QR/QNR
partition of (ℤ/7)\* coincide exactly with the orientation-preserving/reversing
partition of the octonion multiplier group?* If the operation that flips sign(φ)
were a **QR-preserving** map — or a different Z₂ — the map would be inconsistent
and **retired**. The octonion table decides.

## §2 — Results (against the pre-registered criteria)

All computed from the standard cyclic-Fano octonions (lines = shifts of {1,2,4};
QR={1,2,4}, QNR={3,5,6}, special e₇):

| # | Criterion | Result | |
|---|---|---|---|
| **C1** | K (conjugation) flips sign(φ) on all 7 lines | anti-automorphism verified (42 pairs order-reversed; ≠ automorphism); φ→−φ on every line | ✓ |
| **C2** | octonion automorphisms preserve sign(φ) | QR multipliers ×1,×2,×4 are collineations fixing every ε(L) | ✓ |
| **C3** | **QR/QNR = the orientation Z₂** | preserving = {1,2,4} = **QR**; reversing = {3,5,6} = **QNR** — *exact* coincidence | ✓ |
| **C4** | χ(−1)=−1 ties seam negation to the QNR coset | χ(6)=−1; ν₋₁ orientation-reversing | ✓ |
| **C5** | distinct from spatial parity | sign(φ) internal/algebraic; sign(μ̄) reflection-even ⇒ no collapse | ✓ |

**The crux, C3, in detail.** The multiplier group (ℤ/7)\* ≅ ℤ₆ acts on the seven
octonion directions. The Singer multiplier ×2 is a genuine octonion automorphism;
its orbit ⟨2⟩ = {1,2,4} is **both** the quadratic-residue subgroup **and** the
orientation-preserving collineation subgroup of the octonion Fano plane. The
non-residue coset {3,5,6} are **chirality-swaps**: each maps the seven octonion
lines onto the seven lines of the *complementary* Fano plane (φ → off-plane), i.e.
they reverse orientation. So the orientation Z₂ — the thing that flips sign(φ) —
**is** the QR/QNR Z₂. This is the substantive content: it is a fact of the octonion
structure constants, and it could have come out otherwise.

**C1 + C4 close the loop to matter/antimatter.** The principal anti-automorphism
K (conjugation eᵢ↦−eᵢ) — which §2.86C identifies as *chirality* and ties to the
seam crossing — is product-order-reversing (verified) and sends 𝕆→𝕆^op, flipping
sign(φ) on every line. And χ(−1)=−1 mod 7 places the seam negation s↦−s in the
QNR/orientation-reversing coset. So the *same* Z₂ is reached three ways:
the QR↔QNR involution (C3), the anti-automorphism / chirality / matter–antimatter
(C1), and the 𝔽₇ arithmetic of the seam (C4) — exactly the agreement §3.4.6
demanded.

## §3 — Consequence: the registered map promotes (consistency PASSED)

The registered map **sign(φ) ↔ QR/QNR** passes its pre-committed consistency
check. Concretely:

- **R1 (group-theoretic core):** the Z₂ that flips sign(φ) is the QR↔QNR
  involution = the principal anti-automorphism Z₂. Verified from the octonion
  table; coincides with §2.86A's Császár-face result by an independent route, and
  with the §2.77 Galois twist ρ_QR↔ρ_QNR (the same involution lifted to the spin
  reps — §2.77's own R1).
- **R2 (physical identification):** the anti-automorphism is the framework's
  chirality / matter–antimatter operation (§2.86C); so sign(φ) carries the
  baryon's QR/QNR (matter/antimatter-type) chirality. This is a **structural**
  identification — **no observable** (no mass, no measured matter-vs-antimatter)
  is asserted.

**What it does *not* do (honest scope):**
- It does **not** fix *which* orbit is "matter" vs "antimatter" — that is the
  **one free convention** (§2.84A: "which class is real is the one free choice").
- It does **not** use any mirror / spatial-parity reading as evidence (forced;
  excluded per §3.4.6).
- It does **not** supply spatial parity. With sign(μ̄) reflection-even, the
  baryon's topological link carries **no** spatial-parity sign. The corrected
  two-Z₂ picture: **QR/QNR is internal** (carried by sign φ — confirmed here);
  **spatial parity is external** and is simply *not* encoded in the link's μ̄.
  They are distinct (C5), with parity not a topological observable of the baryon.
- It does **not** advance the §3.4 **dynamical** gates (the Bjerknes pulsation
  amplitude §2.52 Open 3, and the bilateral fold §2.45-NGA/§2.53), which remain
  the open frontier; nor does it realize a Borromean *field* soliton.

## §4 — The corrected sign-structure of the baryon (post-V4.32, this check)

| sign | what it is | reflection behavior | carries | status |
|---|---|---|---|---|
| sign(μ̄) | topological triple-linking sign | reflection-**even** | **not** spatial parity (closed-negative) | V4.32 |
| sign(φ) | octonion φ-orientation on the winding Fano line | internal/algebraic | **QR/QNR chirality** (matter/antimatter-type) | **consistency PASSED (this check)** |

The §3.4.6 two-sign factorization (R1) stands; what is now settled is the
*reading*: sign(μ̄) is not parity, and sign(φ) **is** the QR/QNR carrier — the one
sign the orientation-even Hopf charge (§3.4.5) and the reflection-even μ̄ (V4.32)
could not provide.

## §5 — Proposed canonical update (additive)

| Task | Status |
|---|---|
| §3.4 sign(φ)↔QR/QNR consistency check | **PASSED (R1 core / R2 physical).** The Z₂ flipping sign(φ) = the QR↔QNR involution = the principal anti-automorphism (§2.86C), with QR/QNR = the octonion orientation partition (C3, exact) and χ(−1)=−1 the 𝔽₇ tie. Promotes the registered map from R3-pending. |
| sign(μ̄) ↔ parity | unchanged — **closed-negative** (reflection-even, V4.32). |
| baryon spatial parity | **not carried by the link** (μ̄ reflection-even); a separate, external question. |
| matter/antimatter *observable* | **open** — this check fixes structure, not an observable; orbit-labeling is the free convention. |
| §3.4 dynamical gates (§2.52 Open 3, §2.45-NGA/§2.53) | **open — unchanged** (the real frontier). |

*Reproduce: `python3 tools/signphi_qrqnr_check.py`. Pre-registration:
`SQT_3.4_SIGNPHI_QRQNR_PREREGISTRATION.md`. Append-only; this report recommends
the promotion above and asserts no observable bridge. Cross-refs:
§2.75/§2.76 (QR↔QNR two-orbit chirality), §2.77 (Galois twist on spin reps),
§2.84A (QR/QNR ↔ Re/Im of su(3)), §2.86A/C (chirality-swap coset; principal
anti-automorphism; χ(−1)=−1), Paper II §3.4.6 (the registered map),
`SQT_3.4_GOLDEN_LINK_TYPE_CORRECTION.md` (why this is the sole route).*
