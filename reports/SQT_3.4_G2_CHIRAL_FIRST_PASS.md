# §3.4-G2-CHIRAL First Pass — Magnitude Restored on a Genuine Borromean; sign(μ̄) Is Reflection-EVEN (Closed Negative)

**Date:** 2026-06-05
**Register:** **R1** — two exact group-theoretic results (a restored magnitude
on the right object; a reflection-EVEN finding for the triple-linking sign).
**Pre-registration:** `reports/SQT_3.4_SIGN_PREREGISTRATION.md` (criteria P1–P4,
committed before any sign was computed). **Tool:** `tools/g2_milnor_chiral.py`.
**Eddington watch:** ACTIVE — no sign was faked; the mirror operation is
self-validated on a Hopf control, so the non-flip is a topological fact, not a
code artifact.

> **The disciplined recheck demanded by the V4.29 retraction is done — exactly,
> with no geometry and no circularity.** Defining the Borromean rings *genuinely*
> by the braid word β = (σ₁σ₂⁻¹)³ and computing μ̄(123) from the Artin action +
> Magnus expansion gives two clean facts: (1) **the magnitude rule is RESTORED**
> — |μ̄(123)| = 1 on a genuine Borromean, 0 on the unlink — so the §3.4 rule was
> correct *as a statement* and only mis-instantiated on the amphichiral golden
> ellipses; (2) **sign(μ̄) is REFLECTION-EVEN** — the spatial mirror (proven
> genuine by a Hopf-link control that flips lk) leaves μ̄(123) unchanged. The
> triple-linking sign is **not** a spatial-chirality witness, not even on a
> genuine Borromean. The sign(μ̄)↔parity hypothesis is **closed negative.**

## §1 — Why a new object (and why exactly, not geometrically)

§3.4-G2-Milnor-SIGN proved the orthogonal golden-ellipse configuration is
**amphichiral** (z→−z fixes each ellipse setwise, reversing two orientations ⇒
μ̄ = −μ̄ ⇒ μ̄ = 0). Because μ̄(123) is an **integer** topological invariant, no
small symmetry-breaking perturbation can move it 0 → ±1: **the golden ellipses
are not the Borromean rings**, so "fix trap #4 on the ellipses" is moot — there
is no link there to read. The recheck must use a configuration that is *genuinely*
the Borromean rings, and must avoid the **circularity** that sank the original
(the "textbook |μ̄|=1" control *was* the uncorrected Seifert triple-point count
under test).

Both are achieved by leaving geometry entirely. The Borromean rings are the
closure of the **pure** 3-braid β = (σ₁σ₂⁻¹)³, and μ̄(123) is computed from the
**Artin representation** on the free group + the **Magnus expansion** — pure
group theory, completely independent of any Seifert surface or triple-point
count. The answer is an **integer read off an exact word**; nothing is discretized
and nothing is faked.

**Method (exact).** Artin action of B₃ on F₃=⟨x₁,x₂,x₃⟩
(σ_i: x_i↦x_i x_{i+1} x_i⁻¹, x_{i+1}↦x_i). For a pure braid β(x_i)=A_i x_i A_i⁻¹;
the longitude λ_i = A_i (well-defined mod ⟨x_i⟩, which only adds X_i terms,
irrelevant to the cross-coefficient). Magnus: x_i↦1+X_i, x_i⁻¹↦1−X_i+X_i²−…;
then **μ̄(ijk) = coeff of X_i X_j in Magnus(λ_k)**. Longitude reconstruction is
asserted (`A x_i A⁻¹ == β(x_i)`) inside the tool.

## §2 — The mirror operation is real (self-validating control)

The whole sign question turns on getting the spatial mirror right. The tool
**proves** its mirror is genuine before reading any μ̄:

| | lk(1,2) | |
|---|---:|---|
| Hopf link σ₁² | **+1** | — |
| spatial mirror σ₁⁻² | **−1** | ✓ mirror flips lk (reflection-odd at degree 1) |

Spatial mirror = **crossing inversion** (σ_i ↔ σ_i⁻¹), and it correctly flips the
Hopf linking number. **So anything crossing-inversion does *not* flip is genuinely
reflection-EVEN — not an artifact of the code.** This is the control that makes
the §3 finding airtight.

## §3 — Results (R1): magnitude restored, sign reflection-even

μ̄(123), computed exactly:

| configuration | μ̄(123) | reading |
|---|---:|---|
| genuine Borromean (σ₁σ₂⁻¹)³ | **+1** | 3-linked |
| **spatial mirror** (σ₁⁻¹σ₂)³ | **+1** | **NO FLIP ⇒ reflection-EVEN** |
| reverse all orientations | **−1** | flips — *orientation* multilinearity, **not** spatial parity |
| 3-unlink | **0** | not 3-linked |

Against the pre-registered criteria:

| # | Criterion | Result | |
|---|---|---|---|
| **P1** | split/unlink → 0 | μ̄_unlink = 0 | ✓ |
| **P3** | \|μ̄\| = 1 | \|μ̄\| = 1 | ✓ |
| **P4** | cyclic consistency | μ̄(231)=μ̄(312)=+1, μ̄(213)=−1 | ✓ |
| **P2** | mirror → −μ̄ | μ̄_mirror = +1 (**no flip**) | ✗ — *and the ✗ is the finding* |

**(1) Magnitude — RESTORED on the right object.** |μ̄(123)|=1 on a genuine
Borromean and 0 on the unlink, with the correct cyclic/transposition structure,
by an **exact** method **independent** of the triple-point count. So the §3.4
magnitude selection rule ("nonzero iff genuinely 3-linked") is **correct as a
statement**. The V4.29 retraction stands **only** because the *filed config*
(golden ellipses) was amphichiral (μ̄=0) — **not** because the rule is wrong. The
rule **re-instantiates** on a genuine Borromean.

**(2) Sign — μ̄(123) is REFLECTION-EVEN.** The spatial mirror (control-proven
genuine) leaves μ̄(123) **unchanged** (+1 → +1). μ̄ flips **only** under reversing
component **orientations** (the reverse-orientation row, −1) — that is
multilinearity in the component orientations, **not** spatial parity. This is
**triple-confirmed**:

- this exact braid/Magnus computation (mirror does not flip μ̄),
- `g2_milnor_int.py` independently finding the Massey integral **reflection-EVEN**
  (a product of two reflection-odd factors), and
- the textbook fact that the **Borromean rings are amphichiral**.

The hoped-for "odd Massey jump-correction" (the open term in the INT report) **does
not exist** — there was never an odd term to find, because the invariant itself is
even.

## §4 — Consequence: the sign(μ̄)↔parity half is CLOSED NEGATIVE

The QR/QNR parity **cannot** come from μ̄'s spatial chirality — the triple-linking
sign carries **no** spatial parity, even on a genuine Borromean. This is not a
gap awaiting a better method; it is a **closed negative**: the forced/geometric
half of the sign-map (sign(μ̄)↔parity) is settled — μ̄ does not encode it.

What this means for the framework, precisely:

- The parity sign must come from **φ** (the octonionic winding direction) via the
  registered **§2.75/§2.76/§2.86C consistency check** — exactly where
  `SQT_3.4_SIGNMAP_REGISTRATION.md` put it. The earlier hope of reading parity off
  the link's spatial handedness is **foreclosed**.
- The **registered sign(φ)↔QR/QNR map is UNTOUCHED** and stays **R3-pending** its
  consistency check. This build neither promotes nor refutes it; it only removes a
  *wrong alternative route* (μ̄-chirality) to the same sign.
- **No result is faked.** μ̄_mirror = +1 is reported as the finding, with the Hopf
  control proving it is topological, not a convention artifact.

**Survives intact / clarified:** the magnitude selection rule (now supported on a
genuine Borromean by an exact, non-circular method); the V4.29 **retraction** (the
filed *instantiation* was amphichiral); the whole vacuum/meson-sector stack
(G0/G1′/G1″/G2-orient, untouched). **Newly closed:** sign(μ̄)↔parity (negative).
**Still open, unchanged:** sign(φ)↔QR/QNR (R3-pending its consistency check).

## §5 — Proposed canonical update (additive)

| Task | Status |
|---|---|
| §3.4-G2-CHIRAL | **First pass — R1.** Exact braid/Magnus on a genuine Borromean: **(1)** magnitude **restored** (\|μ̄\|=1 vs unlink 0; P1,P3,P4) by a non-circular method ⇒ the §3.4 magnitude rule is correct *as a statement*; **(2)** sign(μ̄) is **reflection-EVEN** (mirror does not flip μ̄; Hopf control proves the mirror genuine; triple-confirmed by the even Massey integral + Borromean amphichirality). |
| §3.4 magnitude rule | **Re-instantiated (R1).** Holds on a genuine Borromean; the V4.29 retraction was about the amphichiral *config*, not the rule. |
| sign(μ̄) ↔ parity | **CLOSED NEGATIVE (R1).** The triple-linking sign carries no spatial parity; not a witness, even on a genuine Borromean. The "odd jump-correction" does not exist. |
| sign(φ) ↔ QR/QNR | **Unchanged — R3-pending** its §2.75/§2.76/§2.86C consistency check (the *only* route to the parity sign; registration untouched). |

*Reproduce: `python3 tools/g2_milnor_chiral.py`. Pre-registration:
`SQT_3.4_SIGN_PREREGISTRATION.md`. Append-only; this report does not modify
canonical content — it RECOMMENDS the magnitude re-instatement and the
sign(μ̄)↔parity negative above. Cross-refs: `g2_milnor_sign.py` (amphichirality of
the golden config), `g2_milnor_int.py` (even Massey integral),
`SQT_3.4_SIGNMAP_REGISTRATION.md` (the map — untouched).*
