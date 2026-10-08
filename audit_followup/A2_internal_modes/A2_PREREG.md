# A2 — Internal modes of the 16-component substrate: pre-registration

**Plain-language summary.** The substrate has sixteen internal field components, but the ledger's sound-and-light studies only ever used one. The other directions cost no energy to rotate into (the ledger proved this at G-INT1), so they form extra, very soft wave branches. This file fixes, before any calculation, how four questions will be decided:
1. How do those branches disperse, and what is the slowest speed at which a moving object can shed energy into them?
2. How many such soft modes does each candidate vacuum have?
3. Was the earlier vacuum-selection gate (G-VS1) counted under the right symmetry?
4. Do the ledger's matter knots couple to these branches strongly enough to feel friction at every speed?

**Lock.** Locked by its md5 in `A2_LOCK.txt` and by the commit that adds it, before any A2 computation or derivation file exists. Corrections go in dated addenda.

**Base.** V4.91, md5 `ce9ca6873adb5686227f5d103b41e3cc`. The objects of record are as follows.
- The action of record (G-2a-A1 Phase 0, §2.91.R): ψ ∈ ℂ⊗𝕆, 16 real fields; a single-scalar density kernel (the accidental O(16)); the oriented term O = ∫φ_abc ψ_a ∂_xψ_b ∂_yψ_c. The continuous stabilizer is g₂ ⊕ u(1)_ψ₀ and the diagonal phase is broken to ℤ₃. Time reversal is a symmetry (Q-VS-4).
- The canonical crystal (MV-G1 lineage, g = 22 soft-core, 2D, a* = 1.45747, f_s = 0.0952 two-leg). The 3D AB/hcp state of record.
- G-VS1 (§2.91.U) and its strata.
- The M.ONT annexes (Branch C, VC-B) and G-CC-ε1's existence boundary.

## Questions and decision rules

**DR-A2-1 (dispersion at the vacuum of record).**
- *Computation.* The lowest Bloch band ε₀(q) of L_⊥ = −½∇² + U*ρ₀ − μ on the canonical 2D crystal, for |q| ≤ 0.1·(2π/a*) along Γ–M and Γ–K. Internal fluctuations obey first-order dynamics, i∂_t δψ_⊥ = L_⊥ δψ_⊥, so ω = ε₀.
- *Rule.* If ε₀(q) − ε₀(0) ∝ q^p with p ∈ [1.9, 2.1], record: quadratic and gapless, internal Landau critical velocity 0 (R1). Report m* = q²/(2ε₀).
- *Cross-check.* m/m* against the banked f_s = 0.0952; agreement within 1 % is expected. A disagreement above 5 % is an honesty item to resolve, not a verdict change.
- If feasible, repeat on the 3D AB/hcp state (basal and axial m*).

**DR-A2-2 (Goldstone inventory per stratum).**
- *Computation.* For the vacuum of record (P0) and each G-VS1 stratum (R, P7, F7, I7, MP, MF, MI): broken generators under (i) the action's continuous symmetry G₂ × U(1)_ψ₀ and (ii) the accidental symmetry of the local potential sector at degree ≤ 4. Use Watanabe–Murayama counting with the GP symplectic form: n_B = ½ rank ρ, ρ_ab = ψ†[T_a, T_b]ψ, and n_A = n_BG − 2n_B. List the internal branches that are linear, quadratic or gapped, and what gaps them.
- No verdict; this is a deliverable table.

**DR-A2-3 (G-VS1 recount).**
- *Computation.* Exact dimensions of the invariant polynomials (all, and T-even) at degrees 2, 4, 6 on ℂ⊗Im𝕆 = ℝ¹⁴, and at degrees 2 and 4 on ℝ¹⁶ (degree 6 if feasible), under:
  - (a) G₂ × U(1)_global;
  - (b) G₂ × U(1)_ψ₀;
  - (c) G₂ × U(1)_ψ₀ × ℤ₃, the action's group.
- *Rule.*
  - If (c) differs from (a) at any computed degree, annotate §2.91.U: its inventory was computed under a phase symmetry the action of record does not have (E-VS-1(a)). Give the corrected inventory.
  - If (c) contains a T-even degree-6 invariant that depends on the 7-sector phase on the polar stratum, and with nonzero coefficient it gives π₁(V_P7) = 0, then the half-quantum protection on P7 and I7 is **DOWNGRADED** from protected to accidental. It would hold at degree ≤ 4, or only if that allowed coefficient is selected to zero.
  - Robust protection is then recorded for ψ₀ windings only, and the mixed strata are re-read accordingly.

**DR-A2-4 (linear coupling and friction).**
- *Determine* (i) whether the knots' declared coupling class couples linearly to the internal branches: the total density (Branch C) and the lattice vertex −ρ_n u̇·v_s.
- *Determine* (ii) whether a moving Fano-line core and a moving filled filament core couple linearly to the gapless internal branches, and whether the resulting emission has a velocity threshold, in a uniform background and in the crystal.
- *Rule.*
  - If a declared matter object has a nonzero linear coupling with no velocity threshold on the vacuum of record, record: moving matter of that kind feels internal-sector friction at every speed; the vacuum of record cannot host it unless an import gaps the internal sector; and the gapped direction's Landau speed √(2Δ/m*) must then reach c_T. This is a **DOWNGRADE** of the vacuum of record as a host for that matter.
  - If the coupling vanishes, or only threshold emission exists, record the threshold and do not downgrade.

**DR-A2-5 (order-by-disorder, optional).** Whether zero-point energy selects a stratum. Run only if time allows; otherwise register it as the named successor that could turn I6 from an import into a computation.

## Second leg

A blind agent repeats the decisive derivations without seeing the first leg:
- the invariant counts of DR-A2-3 by a different method;
- π₁ of the polar-stratum vacuum manifold with and without the degree-6 term;
- the Watanabe–Murayama types for P0, R, P7 and F7;
- the linear-coupling statements of DR-A2-4 (i);
- the moving-frame far-field argument of DR-A2-4 (ii).

*Agreement criterion:* identical integer counts and identical classifications. Any disagreement halts the verdict until a third derivation settles it. The m* number is cross-checked against the banked f_s, which comes from a different route (a relaxed phase twist), not by a second leg.

## Not in scope

- No magnitude for I6 or for the immiscibility import (M.CW).
- No re-scoring of G-QUANTA.
- No statement about §2.50.A beyond what DR-A2-3 forces; C2 re-reads it.
- §2.52 Open 3 is untouched.
