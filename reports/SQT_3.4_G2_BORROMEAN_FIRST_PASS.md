# §3.4-G2-Borromean First Pass — The Baryon Needs a Triple Invariant

**Date:** 2026-06-03
**Register:** **R1** for (A)–(C) below (exact / robust, reproducible) + **R3**
for the pre-registered φ-weighted Milnor μ̄ gate.
**Tool:** `tools/g2_borromean.py`. **Reframe source:** SQT-agent audit of
G2-orient (the Hopf charge is the meson-sector, pairwise invariant; the baryon
needs the cubic triple-linking).
**Eddington watch:** ACTIVE — Hopf-link validation accompanies the pairwise-zero
result; a wrong handedness scalar (reflection-even) was caught and replaced.

> **Why this gate, not a knotted soliton.** G2-orient's charge Q_φ = ∫A·B is a
> **pairwise / helicity** invariant — the **meson sector** (§2.7). The §2.15
> baryon is the three-strand **Borromean** configuration, **pairwise unlinked by
> definition**, so the Hopf charge is **blind** to it. The baryon's content is
> the **cubic Milnor triple-linking μ̄(123)**. This first pass establishes the
> blindness, the available chirality, and the φ-selection, then pre-registers the
> μ̄ computation. It does **not** brute-force a knotted Faddeev–Hopf soliton.

## §GB.1 — Results (R1)

| Test | Result | Meaning |
|---|---|---|
| **(A)** pairwise Gauss linking, Borromean | lk(1,2)=lk(1,3)=lk(2,3) = **0.000** | pairwise UNLINKED ✓ |
| (A) validation: Hopf link | \|lk\| = **1.000** | the linking integral is correct; the 0s are real |
| **(B)** handedness pseudoscalar | **+4.24 → −4.24** under mirror | the configuration is **CHIRAL** (a sign exists) |
| **(C)** φ-weight, **Fano line** (0,1,3) | φ_abc = **+1** | triple invariant can be nonzero ✓ |
| (C) φ-weight, **non-line** (0,1,2) | φ_abc = **0** | μ̄^φ ≡ 0 off the lines ✓ |

**(A) The meson-sector observable is identically blind to the baryon.** On a
genuine Borromean configuration (three mutually-perpendicular golden ellipses)
all three pairwise Gauss linking integrals vanish, while a Hopf link gives
\|lk\|=1. So the pairwise Hopf/helicity charge of G2-orient cannot see the
Borromean's defining inter-strand binding. The reframe is confirmed: the baryon
requires a higher-arity invariant.

**(B) The chirality the Hopf charge lacked is present in the link topology.** A
configuration handedness pseudoscalar (det of one sample point per loop — a
genuine reflection-odd quantity) flips sign under mirror, so the Borromean is
chiral. (The first attempt — a triple product of the loops' area-*normals* — was
reflection-*even* and was dropped; pseudovector triple products are reflection-
invariant.) The *invariant* handedness is sign(μ̄); this is the cheap check that
a sign is available.

**(C) The φ-weighted selection is exact at arity 3.** A triple invariant
contracts the associative 3-**form** φ, which is ±1 on a Fano line and 0
otherwise — the same arity ladder as G0 (2-body blind; Fano structure first at
3-body). A triple-linking observable is the right order to carry it.

## §GB.2 — The pre-registered gate (R3 → R1 target)

> **G2-Borromean (proper).** Compute the **φ-weighted Milnor triple-linking
> μ̄₁₂₃^φ** on the Borromean strands (third-order helicity / Massey product;
> tractable precisely because all pairwise linkings vanish). **Predictions,
> recorded now:**
> 1. **μ̄₁₂₃^φ ≠ 0 iff** the three winding directions form a **Fano line**
>    (arity match: triple invariant ↔ 3-point line ↔ associative 3-form φ).
> 2. **sign(μ̄₁₂₃^φ) = the Borromean chirality** (left/right ⇒ ±1) — supplying the
>    handedness the orientation-even Q_φ could not carry, and tying it to QR/QNR
>    (§2.75/§2.76) and matter/antimatter.
>
> Milnor invariants are subtle to evaluate; the numeric is **not faked** in this
> first pass. **Hold** any brute-force knotted-soliton energy relaxation until
> this gate reports.

## §GB.3 — Scope / what this does and does not establish

- **Does (R1):** prove the pairwise Hopf/helicity (meson) invariant is
  identically blind to the Borromean baryon; show the configuration is chiral
  (a sign is available); show the φ-weighted triple selection is exact.
- **Does NOT:** compute μ̄ (open — the pre-registered gate); identify the
  physical baryon soliton; assert any observable bridge; close §2.15. The
  handedness scalar in (B) is a sample-dependent chirality check, not the
  topological invariant.

## §GB.4 — Proposed Part VI open-task update

| Task | Status |
|---|---|
| §3.4-G2-Borromean (first pass: pairwise-blindness + chirality + φ-selection) | **First pass CLOSED (R1):** Hopf charge identically blind to the Borromean; config chiral; φ-selection exact at arity 3. |
| §3.4-G2-Milnor (φ-weighted μ̄₁₂₃ numeric; Fano-selective; sign = chirality) | **Open — the pre-registered baryon gate.** |

*Reproduce: `python3 tools/g2_borromean.py`. Append-only; no prior ledger
content modified. Cross-refs: §3.4-G2-orient (meson/pairwise sector), §2.15
(Borromean), §2.75/§2.76 (QR/QNR), §2.7 (meson 2:3), §3.4-G0 (arity ladder).*
