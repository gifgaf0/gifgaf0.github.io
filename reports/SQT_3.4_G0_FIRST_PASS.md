# §3.4-G0 First Pass — The Symmetry-Allowed Action (Pre-Registered Term List)

**Date:** 2026-06-03
**Register:** **R1** for the discrete orbit computation (exact, `tools/g0_invariants.py`,
ties to §1.1) + **R2** for the invariant-theory reading (contact potential forced
to GP; 2-body kernel form) + **R3** for the forward program (the 3-body Fano gate).
**Program:** `reports/SQT_3.4_PROOF_PROGRAM.md`, gate §3.4.3 / §3.4-G0.
**Eddington watch:** ACTIVE — this entry IS the pre-registration required by
§3.4.3 before any MV-G1 result may be promoted.

> **Purpose.** §3.4.3 requires the symmetry-allowed interaction terms to be
> enumerated and recorded **before** computing the ground state, so the MV-G1
> kernel is audited rather than assumed. This is that record.

---

## §G0.1 — Import declaration (I1, restated)

Order parameter **ψ ∈ ℂ⊗𝕆**: a U(1)_number superfluid phase × the 8 octonion
components (real e₀ + seven imaginaries e₁..e₇ ↔ the 7 Fano points). Internal
symmetry: **G₂ = Aut(𝕆)** acting irreducibly on Im(𝕆)=ℝ⁷, with the Fano
collineation subgroup **PSL(2,7) ≅ GL(3,2)** permuting e₁..e₇ as PG(2,2). Imports
remain exactly I1 (this target), I2 (GP kinetic form), I3 (one scale).

## §G0.2 — Exact computation (R1)

`tools/g0_invariants.py` builds the **full** GL(3,2) (all 168 invertible 3×3
F₂ matrices) and its action on the 7 Fano points. (The §1.1 Lemma 2.2 generators
g₁,g₂ generate only the **S₄** maximal subgroup of Theorem 2.1, order 24,
verified ⊆ GL(3,2) — a consistency tie to §1.1, **not** the full symmetry.)

| Quantity | Value | Consequence |
|---|---|---|
| \|GL(3,2)\| | **168** ✓ | = \|PSL(2,7)\| |
| §1.1 ⟨g₁,g₂⟩ = S₄ ⊆ G | **24 ⊆ 168** ✓ | consistency with §1.1 Thm 2.1 |
| orbits on 7 points | **1** | transitive |
| orbits on ordered distinct pairs | **1** (→ 2 orbitals) | **2-transitive** |
| invariant symmetric 2-tensors | **dim 2 = span{I, J}** | fixes the 2-body kernel |
| orbits on unordered triples | **2** (sizes **7 + 28**) | Fano lines vs non-lines |
| collinear triples (Fano lines) | **7**, single orbit | the lines are one G-orbit |

## §G0.3 — Invariant-theory reading (R2)

**(a) Contact potential is forced to standard GP.** U(1)×G₂ invariance with
degree ≤ 4 admits only `V(ψ) = −μ|ψ|² + (g/2)|ψ|⁴`. G₂ acts irreducibly on
Im(𝕆)=ℝ⁷ ⇒ a unique invariant quadratic (the norm); the G₂-invariant
coassociative 4-form is totally antisymmetric, so it gives **no** bosonic quartic
(antisymmetric contracted with the symmetric ψ_iψ_j vanishes) beyond (|ψ|²)².
**The octonion structure adds nothing to the contact potential** — a clean M.CW
instance (combinatorics fixes the form; the form is generic GP).

**(b) 2-body kernel is scalar-per-channel.** 2-transitivity ⇒ the only invariant
2-tensors are I and J ⇒ the symmetry-allowed non-local 2-body interaction is

    K_ij(r) = a(r)·δ_ij + b(r)·J_ij .

**No finer Fano structure survives at 2-body.** The two channels are
"same-component" (I) and "all-pairs" (J); each carries an arbitrary radial
profile.

**(c) Fano-line structure first appears at 3-body.** Triples split into 2 orbits
(7 collinear + 28 non-collinear), so a 3-body coupling — degree 6 in ψ, beyond
the ≤ 4 minimal truncation — is the **first** interaction that can distinguish
the Fano lines. This is where the framework's specific PSL(2,7)/Fano content
genuinely enters the dynamics.

## §G0.4 — The roton verdict (M.CW-honest, load-bearing)

Symmetry fixes the kernel **form** (scalar × {I,J}) but **not** its radial
profile a(r), b(r). A roton — a negative Ũ(k) lobe at finite k — is a property of
that profile, i.e. a metric/scale, which **M.CW classifies as an import.**
Therefore:

> **The framework's symmetry PERMITS a roton but cannot FORCE one.** The roton
> that produces the p6m vacuum is imported (I2/I3), not derived.

The MV-G1 soft-core kernel (`reports/MV_G1_RESULT.md`) is a **legitimate
representative of the allowed 2-body form**, so the MV-G1 p6m result is
**consistent with G0** — but it inherits this caveat: at 2-body the substrate
story is *generic supersolid physics*, and the framework-specific content
(Fano lines) is untested there.

## §G0.5 — Pre-registered term list (the §3.4.3 deliverable)

Recorded **now**, before any further MV runs:

```
S[ψ] = ∫ dt d³x [ (i/2)(ψ†∂_tψ − c.c.) − ½|∇ψ|² − μ|ψ|² + (g/2)|ψ|⁴ ]
     − ½ ∫∫ |ψ(x)|² [ a(r)δ + b(r)J ] |ψ(x')|²               (2-body; roton imported)
     − (λ/3) ∫∫∫  Σ_{lines ℓ}  ρ_ℓ(x)ρ_ℓ(x')ρ_ℓ(x'')         (3-body; Fano-line, G0→G1′)
```
Declared imports: I1 (target), I2 (kinetic form), I3 (one scale), and the radial
profiles a(r), b(r) (M.CW metric class). Everything else is fixed by symmetry.

## §G0.6 — What this does and does not establish

- **Establishes (R1):** the exact orbit structure of PSL(2,7) on the Fano points,
  hence the *dimensions and forms* of the invariant couplings at each body-order.
  These are not estimates; they are finite-group facts.
- **Establishes (R2):** the contact potential is generic GP; the 2-body kernel is
  scalar-per-channel; Fano structure first enters at 3-body.
- **Does NOT establish:** that a roton exists from first principles (it is an
  imported profile, §G0.4); that the 3-body Fano term produces any specific
  lattice effect (that is the open G0→G1′ gate); anything about a scale or sign
  (M.CW imports, undisturbed).

## §G0.7 — Forward pointer: the genuine framework gate (G0→G1′)

The decision-relevant new gate this pass surfaces:

> **G1′ — does the Fano-line 3-body coupling select or modulate the lattice?**
> Add the §G0.5 λ-term to the MV-G1 minimiser and test whether it (i) shifts the
> p6m selection, (ii) stabilises a specific orientation/sublattice keyed to the
> 7 lines, or (iii) does nothing observable. This is the first test that probes
> *framework-specific* content rather than generic supersolid physics. A null
> here would mean the Fano structure leaves no dynamical fingerprint at this
> order — itself an informative bound on the substrate hypothesis.

## §G0.8 — Proposed Part VI open-task update

| Task | Status |
|---|---|
| **§3.4-G0** (symmetry-allowed term list) | **First pass CLOSED (R1 orbit computation + R2 reading); term list pre-registered (§G0.5).** Octonion target; full enumeration of higher-order G₂ quartic tensors beyond the coassociative 4-form remains a tidy-up R2 item. |
| **§3.4-G1′** (Fano 3-body lattice effect) | **Open — the genuine framework-specific gate; newly raised by G0.** Add the λ-term to `tools/mv_g1_minimiser.py`. |
| **§3.4-MV-G1** | unchanged — PASS stands as "mechanism viable"; G0 confirms its kernel is an allowed representative, roton imported. |

*Reproduce: `python3 tools/g0_invariants.py`. Append-only; no prior ledger
content modified. Cross-refs: §1.1 (generators/subgroup), §3.4.3 (G0 requirement),
MV-G1, M.CW (radial profile = import), §2.55/§2.68 (Fano-line structure).*
