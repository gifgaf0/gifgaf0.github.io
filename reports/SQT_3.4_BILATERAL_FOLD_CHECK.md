# §3.4 Bilateral-Fold → cos(π/10) Gate — ADVANCED (conditional R2): the Fold Is Forced by the Convex Kinetic Term, Not the Topological One

**Date:** 2026-06-06
**Register:** **R1** for the geometry (deficit Δ=36°) and the value identity
(cos18°=cos π/10); **R2 (conditional on an import)** for the gate's open step —
the bilateral split is forced *iff* the substrate fold-energy is strictly convex,
which the §3.4.4 GP kinetic term supplies. **Pre-registration:**
`reports/SQT_3.4_BILATERAL_FOLD_PREREGISTRATION.md` (criteria committed before
computing). **Tool:** `tools/bilateral_fold_check.py`.
**Eddington watch:** ACTIVE — the split θ was left **free** and the action chose
it; nothing reverse-engineered. **M.BRIDGE:** no observable asserted (the
(1−cos18°) void correction is downstream).

> **The gate is advanced, not closed.** Leaving the deficit split free, the §3.4
> substrate action forces the symmetric 18°+18° fold **only through its convex
> (Gross–Pitaevskii) kinetic term**; its **topological deficit-angle (Regge) term
> is split-indifferent and cannot force it** — a clean negative that sharpens the
> gate. So step (3) closes **modulo the substrate having a convex kinetic energy**,
> exactly the GP functional §3.4.4 already imports; it is **not** an unconditional
> "from lattice axioms alone" derivation. With (3) in hand, cos18°=cos(π/10)
> follows (step 4).

## §1 — The gate and what is genuinely at issue

The §2.45-NGA / §2.53 prior-address of cos(π/10) has four steps; the ledger marks
**only step (3)** open ("show the §3.4 substrate action forces bilateral
splitting; once shown, cos18°=cos(π/10) is fully prior-addressed"):

1. vacuum vertex: 3 hexagons × 120° = 360° → flat;
2. seam vertex: 3 pentagons × 108° = 324° → **deficit Δ = 36° = π/5**;
3. **the 36° splits bilaterally → 18° + 18°** — the open step;
4. cos(18°) = the surviving fraction across the seam.

The disciplined question is *what in the action forces (3)*. The split is a degree
of freedom (θ, Δ−θ), θ∈[0,Δ]; "bilateral" is the specific claim θ=Δ/2. I did **not**
assume it — I parametrized θ and asked each form of the §3.4 action which θ it
selects.

## §2 — Results (against the pre-registered criteria)

| # | Criterion | Result | |
|---|---|---|---|
| **B1** | deficit arithmetic | 360° (flat) → 324° → Δ=36°=π/5; Σ over 20 dodecahedral vertices = 720° = 4π | ✓ R1 |
| **B2** | θ=Δ/2 a symmetric critical point | reflection symmetry of the seam ⇒ E′(Δ/2)=0 for any symmetric f | ✓ (necessary) |
| **B3** | **convexity decides** | Regge f=θ: curvature 0 — **split-indifferent**; GP f=θ²: curvature +4 — **min at 18°**; concave f=√θ: curvature <0 — max | ✓ |
| **B4** | GP supplies it, Regge doesn't | the §3.4.4 gradient term is the convex one that forces the fold; the deficit-angle term is linear | ✓ |
| **B5** | the value | cos18° = cos(π/10) = √(10+2√5)/4 = √(2+φ)/2 = 0.951056516295; (1−cos18°)=0.048943 | ✓ R1 |

**The substantive content (B3/B4).** With θ free, the fold-energy
E(θ)=f(θ)+f(Δ−θ) selects:

- **deficit-angle / Regge** (the topological term, **linear** in deficit): E is
  *constant* in θ — **every split is degenerate**. The bare topological action
  **cannot** force the bilateral fold. *This is the genuinely informative result*:
  a tempting reading — "the deficit/Regge action forces the symmetric fold" — is
  **false**.
- **GP / Bjerknes kinetic** (§3.4.4 gradient energy, **convex**): E is strictly
  convex with its unique minimum at θ=Δ/2=18°. The convex term **forces** the
  bilateral split.

So the operative mechanism is identified: **convexity of the kinetic term**, not
the topological term, forces step (3).

## §3 — Honest scope: what is forced, what is imported, what is standard

This must be stated precisely so the result is not over-read (the same discipline
that tempered the sign(φ) check):

1. **The "convexity ⇒ symmetric split" step is standard (Jensen).** For any
   strictly convex symmetric f, f(θ)+f(Δ−θ) is minimized at the midpoint. The
   gate does **not** turn on a deep new fact here; it turns on *which* term of the
   action is the operative one.
2. **The genuinely new content is the negative + the disambiguation:** the
   topological deficit-angle (Regge) term is **split-indifferent** (linear), so the
   forcing **must** come from the convex kinetic term — it cannot come from the
   topological action the gate's wording most naturally suggests.
3. **The convex kinetic energy is an IMPORT (M.CW).** The GP gradient functional
   ∫|∇ψ|² is a metric-class import (§3.4.4 / §3.4 state this explicitly: metric,
   scale, and sign are imports, not combinatorial outputs). So the gate's closure
   is **conditional on that import**, not derived "from lattice axioms alone."
4. **The single-seam bilateral-fold ansatz is also an import.** That the 36°
   deficit is absorbed as *one* fold along *one* seam (with two sides), rather than
   spread smoothly or over several seams, is assumed; the action then fixes the
   split *within* that ansatz.
5. **Step (4) (cos18° as the surviving fraction) is the ledger's R2 projection
   ansatz**, not re-derived here; this report verifies the *identity*
   cos18°=cos(π/10) and that it follows once 18° is in hand.
6. **No observable** (the (1−cos18°) void correction) is asserted — M.BRIDGE.

**Net register:** the gate moves from **open** to **reduced to the GP-convexity
import** — **R2, conditional**. It is *not* the unconditional R1 closure the
ledger's "fully prior-addressed from lattice axioms alone" envisioned, because the
convexity (and the seam ansatz) are imports. What the framework *gains* is a sharp
statement of exactly what the remaining unconditional closure would require:
**derive a strictly convex kinetic energy (and the single-seam absorption) from
the lattice axioms** rather than importing them.

## §4 — Proposed canonical update (additive)

| Task | Status |
|---|---|
| §2.45-NGA / §2.53 bilateral-fold gate (step 3) | **ADVANCED — conditional R2.** The split is forced by the substrate's **convex kinetic term** (GP, §3.4.4), not by the **linear deficit-angle (Regge) term** (split-indifferent — a new negative). Closes step (3) **modulo** the convex-kinetic **import** + single-seam ansatz (M.CW); the "convex ⇒ midpoint" step is Jensen-standard. cos18°=cos(π/10) then follows. |
| remaining unconditional closure | **Open — sharpened:** derive a strictly convex kinetic energy (and single-seam deficit absorption) from the lattice axioms, rather than importing the GP functional. |
| §2.52 Open 3 (pulsation = ζ) | **open — unchanged** (the other dynamical gate). |

*Reproduce: `python3 tools/bilateral_fold_check.py`. Pre-registration:
`SQT_3.4_BILATERAL_FOLD_PREREGISTRATION.md`. Append-only; asserts no observable
(M.BRIDGE) and flags the convex-kinetic + seam imports (M.CW). Cross-refs:
§2.45-NGA (gate + 4-step argument), §2.53 (Rung-2 face inheritance), Paper II
§3.4/§3.4.4 (substrate action + GP representation), §3.06/§3.07 (chord-CR and
enrichment routes to cos(π/10), both closed-negative).*
