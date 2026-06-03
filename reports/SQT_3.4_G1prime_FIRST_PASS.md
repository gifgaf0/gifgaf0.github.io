# §3.4-G1′ First Pass — The Fano-Line 3-Body Term Is Dynamically Inert (and Why)

**Date:** 2026-06-03
**Register:** **R1** for the single-site energetics (PART A, exact) and the
multi-seed 2-D measurements (PART B) + **R2** for the mechanism (the 2-design
symmetry argument). **Informative null**, not a failure.
**Tool:** `tools/g1prime_fano3body.py`. **Program:** §3.4-G1′ (raised in
`reports/SQT_3.4_G0_FIRST_PASS.md` §G0.7).
**Eddington watch:** ACTIVE — a control (non-line triples) was run under
identical protocol; the result is a comparison, not a single-arm claim.

> **Question.** G0 showed the first place the framework's Fano/PSL(2,7) content
> can enter the dynamics is a 3-body coupling on the 7 collinear triples (Fano
> lines), `E_Fano = −λ∫ Σ_lines ρ_iρ_jρ_k`. Does adding it to the crystallising
> GP action leave a framework-specific fingerprint — relative to the same
> coupling on 7 NON-collinear triples (the placebo control)?

## §G1′.1 — PART A: single-site energetics (R1, exact)

Global minimum of the 3-body site energy `E(n) = −Σ_triples n_i n_j n_k` on the
7-component probability simplex:

| triple set | min site-energy | minimiser |
|---|---:|---|
| **7 Fano lines** | **−1/27 = −0.037037** (exact) | 100% of density on one line |
| 7 random non-line triples (12 draws) | **−0.0428 ± 0.0042** | concentrated, over-weighting shared points |

**Finding.** The Fano minimum is *exactly* −1/27 because the lines are a balanced
**2-(7,3,1) design** — every point on exactly 3 lines, every pair on exactly 1 —
so no over-concentration is possible. **Irregular** control sets do slightly
*better* (more negative): a point lying in many triples lets density
over-concentrate. So **local energetics do not select the Fano lines** — if
anything they are the *least* favourable (maximally balanced) 3-body target. Any
Fano distinction is therefore structural/collective, not single-site.

## §G1′.2 — PART B: 7-component GP, Fano vs control (R1)

Seven-component imaginary-time GP (N=80, L=12, soft-core roton g=22 on the
**total** density → p6m per MV-G1) plus the 3-body term at perturbative λ=0.5.
Order parameter **Q** = per-site density fraction on the site's best triple
(uniform baseline = 3/7 = 0.429). Robust across seeds {7, 11, 19, 23}:

| coupling | ψ₆ (total) | line-lock Q | Δ vs uniform |
|---|---:|---:|---:|
| **Fano lines** | 0.77–0.85 | **0.431 ± 0.000** | **+0.002** (none) |
| non-line control | 0.77–0.84 | **0.65–0.77** | +0.22 … +0.34 (strong) |

**The p6m lattice survives in both** (ψ₆ ≈ 0.83 ≈ MV-G1). But the **Fano-line term
leaves the component distribution completely unordered** (Q pinned at the uniform
baseline, every seed), while the **generic control strongly orders the
components** (Q jumps to ~0.73).

Stability is also ordered by symmetry: the Fano arm stays stable to larger λ
(≈1) than the control (collapses by λ≈1); both collapse by λ≈2. The balanced
term resists the runaway concentration a 6th-order attraction otherwise drives.

## §G1′.3 — Verdict (R2) and mechanism

**The framework's minimal Fano-line 3-body coupling is dynamically INERT for
component ordering — precisely because of the framework's own symmetry.** The 7
lines form a balanced 2-design, so the symmetric term has the uniform
component state as a fixed point and supplies **no symmetry-breaking gradient**.
A generic (irregular) triple coupling of identical form and strength orders the
components strongly; the Fano one does not. The distinguishing feature of the
Fano structure here is an **absence** of ordering, not a presence — it is "too
symmetric to imprint" through this channel.

This is an **informative null** (mechanism fully understood), not a numerical
failure: the control proves the apparatus can detect ordering, and the Fano
inertness is reproduced exactly across seeds with a clean 2-design explanation.
It is the dynamical counterpart of G0's local finding (2-transitivity collapses
the pair structure) and is M.CW-flavoured: the combinatorial design's symmetry
means it does not break the symmetry it encodes.

## §G1′.4 — Scope / what this does and does not establish

- **Establishes:** for the natural **U(1)-invariant density-product** line term
  (the G0 minimal one), at the order where Fano structure first appears, the
  Fano coupling imprints **no** component order on the p6m crystal, while a
  generic control does — robustly, with a symmetry mechanism.
- **Does NOT establish** anything about an **orientation/sign** term built from
  the octonion *multiplication* (structure constants `e_i e_j = ±e_k`). That
  term carries the Fano *orientation* and net U(1) charge; it is **not** the
  symmetric density-product tested here and is not U(1)-invariant alone (needs
  pairing, e.g. via ψ₀). It is the natural next candidate (G1″).
- **Does NOT** rule out collective Fano effects in observables other than per-site
  Q, nor at non-perturbative λ (where both arms collapse and the comparison is
  ill-posed).

## §G1′.5 — Forward pointers

| Gate | Question |
|---|---|
| **G1″ — orientation term** | Does the octonion-multiplication 3-body term `Σ_lines Re(ψ₀* ψ_i ψ_j ψ_k)` (U(1)-invariant via ψ₀, sign-carrying) break the component symmetry where the density-product term cannot? This is where the Fano *orientation* (not just incidence) could enter. |
| **G1‴ — collective tiling** | If any term does lock sites, do line-locked sites tile coherently (neighbours sharing the single common point of their lines)? Moot for the density-product term (no locking), live for G1″. |

## §G1′.6 — Proposed Part VI open-task update

| Task | Status |
|---|---|
| **§3.4-G1′** (Fano density-product 3-body) | **First pass CLOSED — informative null (R1+R2):** Fano term is inert for component order (balanced 2-design); generic control orders. p6m survives. |
| **§3.4-G1″** (octonion-multiplication / orientation 3-body) | **Open — newly raised; the orientation channel is the next place Fano content could act.** |

*Reproduce: `python3 tools/g1prime_fano3body.py` (PART A + B) or `--partA-only`.
Append-only; no prior ledger content modified. Cross-refs: §3.4-G0 (the 3-body
term's origin), MV-G1 (the roton/p6m base), M.CW, §2.55/§2.68 (Fano-line / 2-design
structure).*
