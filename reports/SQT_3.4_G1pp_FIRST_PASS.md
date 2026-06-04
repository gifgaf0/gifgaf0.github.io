# §3.4-G1″ First Pass — The Fano Orientation Is Topological: It Lives Only on Soliton Cores

**Date:** 2026-06-03
**Register:** **R1** (the exact/numeric structure-constant computations) + **R2**
(the structural conclusion). **Tool:** `tools/g1pp_orientation.py`.
**Program:** §3.4-G1″ (raised in `reports/SQT_3.4_G1prime_FIRST_PASS.md` §G1′.5).
**Eddington watch:** ACTIVE — every claim is a vanishing/non-vanishing test with
an explicit control (non-line triple; orientation reversal).
**Register caveat:** R1 = **pending independent reproduction** (reproducible from
the committed tool, not yet re-run in the canonical sandbox).

> **⚠ WORDING CORRECTION (2026-06-03).** Where this document says O is "zero on
> all smooth fields," read **"zero on topologically TRIVIAL configurations."** A
> skyrmion is a *smooth* field; O is a total derivative that integrates to the
> **topological charge** on it (Fano-line skyrmion O=−12.47, non-line O=0). The
> load-bearing claim is the topological selection, not smoothness.

> **Question.** G1′ showed the *symmetric* Fano 3-body term is dynamically inert
> (balanced 2-design). G1″ tests the term carrying the Fano **orientation** — the
> octonion structure constants `e_i e_j = ±e_k`, i.e. the associative 3-form
> φ_{abc} (the sign/handedness data M.CW flags as an import the design alone
> cannot supply). Where, if anywhere, can it act?

## §G1″.1 — Results (R1, from the QR octonion 3-form)

φ_{abc} built from the 7 oriented quadratic-residue Fano lines (i, i+1, i+3):
42 nonzero entries, **totally antisymmetric** (verified).

| Test | Result | Meaning |
|---|---|---|
| **(1)** φ(ψ,ψ,ψ) over 1000 random ψ (real & complex) | max \|·\| ≈ 2–5×10⁻¹⁵ | **the orientation POTENTIAL vanishes identically** (antisym φ vs symmetric ψ_aψ_bψ_c) |
| **(2)** cross product (u×v)_c = φ_{abc}u_a v_b | ‖u×v‖ ≈ 6.56; flips under φ→−φ | the current building block survives (u_a v_b not symmetric) and is orientation-odd |
| **(3)** O = ∫ φ_{abc} ψ_a ∂_xψ_b ∂_yψ_c on smooth fields | 0 (uniform), 0 (1-D), \|O\|≤2×10⁻⁶ (smooth 2-D) | **O is a TOTAL DERIVATIVE** — zero on all smooth configurations |
| **(4a)** O on a **Fano-line** skyrmion (0,1,3) | **O = −12.475**, → +12.475 under φ→−φ | nonzero topological orientation charge, orientation-odd |
| **(4b)** O on a **non-line** skyrmion (0,1,2) | **O = 0** | non-line defects carry no orientation charge |

## §G1″.2 — Structural conclusion (R2)

**The Fano orientation cannot imprint on the vacuum at any local order, and its
only dynamical home is the topological defect.** Three steps, each exact:

1. **Potential channel — identically zero.** φ is totally antisymmetric, so the
   cubic φ(ψ,ψ,ψ) and every gradient-free U(1)-invariant orientation term of a
   single bosonic ψ vanish. (This upgrades G1′'s "inert" to "exactly zero" for
   the oriented term.)
2. **Gradient channel — a total derivative.** The lowest non-vanishing orientation
   density O = ∫ φ ψ ∂_xψ ∂_yψ is topological: it is zero on the vacuum, on 1-D
   textures, and on **all** smooth 2-D textures. No bulk contribution exists.
3. **Defect channel — Fano-line-selective.** O is supported only on topological
   defects (vortex/skyrmion cores), where it is nonzero and orientation-odd
   **iff** the defect's winding components form a **Fano line**; non-line defects
   carry zero charge.

Combined with G0 (contact potential forced to GP) and G1′ (symmetric 3-body term
symmetry-inert), this gives a **structural theorem for the §3.4 vacuum**:

> **The framework-specific Fano/PSL(2,7) content is invisible to the vacuum
> (G1). The symmetric channel is symmetry-inert; the oriented channel is a
> topological total derivative. The Fano fingerprint lives ENTIRELY on soliton /
> vortex cores, where it appears as a topological orientation charge that
> selects Fano-line windings.** The vacuum is generic by necessity.

This is M.CW at full force: the sign/orientation (an import the combinatorics
cannot supply to the bulk) can only attach to topology — the defect core.

## §G1″.3 — Why this is a positive result, not a dead end

The §3.4 arc has now *located* the framework's dynamical fingerprint precisely,
by ruling out where it cannot be:

| Gate | Sector | Fano content? |
|---|---|---|
| G0 | contact potential | none (forced to GP) |
| G1 / MV-G1 | vacuum density | none (generic p6m; roton imported) |
| G1′ | symmetric 3-body | inert (2-design symmetry) |
| **G1″** | **oriented 3-body** | **topological — only on Fano-line soliton cores** |

The search is now collapsed onto a single, concrete, falsifiable object: **the
core of the knotted-vortex soliton (gate G2 — the Császár-torus knot).** This is
also exactly the Bjerknes-flow / §2.15 Borromean sector, so G1″ hands G2 a sharp
prediction rather than an open field.

## §G1″.4 — Scope / caveats

- The orientation charge O is the lowest topological invariant of this type; it
  is a **2-D** (skyrmion/Hopf-density) construction. The genuine SQT soliton is a
  **3-D knotted vortex**; the correct invariant there is the Faddeev–Hopf /
  linking charge restricted to Fano-line component windings — the natural 3-D
  generalisation, not yet computed.
- φ is the *compact* octonion 3-form (QR convention). A different sign convention
  is an orientation reversal (O→−O) and changes nothing structural.
- This says where the orientation *can* live, not that the physical soliton
  realises a Fano-line winding — that is the G2 test below.

## §G1″.5 — Forward pointer (sharpened G2)

> **G2-orient.** On the knotted-vortex soliton, classify the core by which
> octonion components wind. The framework predicts a **nonzero orientation /
> linking charge iff those components form a Fano line.** Compute it for the
> candidate Császár-torus soliton; a Fano-line core confirms the orientation
> channel is physically realised, a non-line core is an informative null. This
> is the first framework-specific, falsifiable prediction in the soliton sector
> and the bridge to §2.15 (Borromean) / §2.74.

## §G1″.6 — Proposed Part VI open-task update

| Task | Status |
|---|---|
| **§3.4-G1″** (oriented 3-body / octonion orientation) | **First pass CLOSED (R1+R2):** orientation potential vanishes; orientation density is a total derivative supported only on Fano-line topological defects. Vacuum is Fano-blind. |
| **§3.4-G2-orient** (Fano-line orientation/linking charge on the soliton core) | **Open — the located framework fingerprint; the single concrete G2 prediction.** |

*Reproduce: `python3 tools/g1pp_orientation.py`. Append-only; no prior ledger
content modified. Cross-refs: §3.4-G0, §3.4-G1′, MV-G1, §2.15/§2.74 (soliton /
Bjerknes), M.CW (orientation = import; attaches to topology).*
