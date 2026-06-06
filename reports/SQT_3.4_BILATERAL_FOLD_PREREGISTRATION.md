# §3.4 Bilateral-Fold → cos(π/10) Gate — Pre-Registration (conventions + criteria, committed before computing)

**Date:** 2026-06-06
**Status:** PRE-REGISTRATION, committed **before** the energetics are computed.
**Scope:** the §2.45-NGA / §2.53 open gate — the *one* open step is to show that
the §3.4 substrate (Bjerknes / Gross–Pitaevskii / deficit-angle) action **forces
bilateral (symmetric) splitting** of the 36° pentagon-seam deficit into 18°+18°.
Per the ledger, "once shown, cos 18° = cos(π/10) is fully prior-addressed from
lattice axioms alone." This is a **dynamical** gate (the topology thread is closed);
it asserts **no observable** (the (1−cos 18°) void correction is downstream — M.BRIDGE).

**Eddington / discipline watch:** ACTIVE and especially relevant — this is exactly
the kind of result where a model can be built to *yield* cos 18° by construction.
The guard: I do **not** assume the split is symmetric; I parametrize the split by
an asymmetry θ and ask the action which θ it selects, with a pre-committed
**negative branch** (if the relevant energy is split-indifferent or concave, the
gate does **not** close and I say so). Nothing load-bearing is asserted from
memory; the energetics are computed.

## §1 — Conventions and the object (fixed now)

- **Vacuum vertex:** 3 hexagonal faces meet, 3×120° = 360° — flat, zero deficit
  (the p6m / graphene vertex).
- **Seam vertex:** 3 pentagonal faces, 3×108° = 324° — angular deficit
  **Δ = 36° = π/5** (the trivalent dodecahedral-vertex disclination; Σ over the
  20 dodecahedron vertices = 720° = 4π, Descartes ✓).
- **The split d.o.f.:** the deficit Δ is absorbed by a fold along a seam through
  the vertex; the fold distributes as (θ, Δ−θ) between the two sides of the seam.
  θ ∈ [0, Δ]. "Bilateral" = symmetric split θ = Δ/2 = 18°.
- **Substrate action (§3.4):** two forms in play —
  (a) **deficit-angle / Regge** S = ζ^(2n) Σ_v Φ(v)·κ(v): the topological term,
      **linear** in the deficit;
  (b) **Gross–Pitaevskii / Bjerknes** kinetic functional (§3.4.4): gradient energy
      ∝ ∫|∇ψ|², **quadratic** (convex) in the local fold.
- **Fold-energy model:** E(θ) = f(θ) + f(Δ−θ), with f the per-side fold-energy
  density of the chosen action form (f linear for (a), f ∝ θ² for (b)).
- **Projection (step 4, ledger ansatz, R2):** the surviving fraction across the
  seam is cos(Δ/2) = cos 18°; (1−cos 18°) is the "void."

## §2 — Validation criteria (committed; the result is judged against THESE)

| # | Criterion |
|---|---|
| **B1** | **Deficit arithmetic (R1 geometry).** hexagon vertex = 360° (flat); pentagon vertex = 324°; Δ = 36° = π/5; Σ over 20 dodecahedral vertices = 720°. |
| **B2** | **Reflection-symmetric critical point.** The seam vertex has a reflection symmetry swapping the two sides; hence θ = Δ/2 is a critical point of E(θ)=f(θ)+f(Δ−θ) for *any* symmetric f (E′(Δ/2)=0). [necessary, not sufficient] |
| **B3** | **CRUX — convexity decides.** For **strictly convex** f, θ=Δ/2=18° is the **unique minimizer** (bilateral split FORCED). For **linear** f (the bare Regge term), E is **constant in θ** (split-indifferent — NOT forced). For concave f, θ=Δ/2 is a **maximum** (anti-forced). Demonstrated by the convexity lemma + a numeric θ-scan for each f. |
| **B4** | **The GP kinetic term supplies the convexity; Regge does not.** The §3.4.4 gradient energy ∝ ∫\|∇ψ\|² is strictly convex in the fold mode ⇒ forces the symmetric split; the deficit-angle (Regge) term is linear ⇒ cannot. |
| **B5** | **The value.** cos(Δ/2) = cos 18° = cos(π/10) = √(10+2√5)/4 = √(2+φ)/2, verified to machine precision; report (1−cos 18°). |

## §3 — Promotion rule (committed)

- If **B1 + B2 + B3 + B5 hold AND B4 identifies the convex (GP) term as the one
  that forces it** → the gate's open step is **ADVANCED**: bilateral splitting is
  forced **iff** the substrate fold-energy is strictly convex, and the GP kinetic
  energy (already imported at §3.4.4) supplies exactly that, while the bare
  deficit-angle (Regge) term is **insufficient** (split-indifferent) — a clean
  sharpening. **Register R2**, conditional on the convex-kinetic **import** and the
  single-seam **ansatz** (both M.CW-class, flagged). The gate moves from "open" to
  "**reduced to the GP-convexity import**"; cos(π/10) then follows (B5). This is
  **not** unconditional R1 closure.
- If **B3's crux fails** — i.e. the operative substrate energy is linear/concave
  in the split, so the symmetric fold is not selected — the gate **does NOT close**
  and that is reported as the result (no cos(π/10) prior-address from the action).
- **Either way:** no observable is asserted (the void correction is downstream,
  M.BRIDGE); the single-seam bilateral-fold ansatz and the GP convexity are
  **imports**, not combinatorial outputs (M.CW); no value is reverse-engineered —
  θ is left free and the action chooses.

*Cross-refs: §2.45-NGA (the gate + 4-step argument), §2.53 (Rung-2 face inheritance:
cos 18° is pentagon/A₅-level, reaches K₇ by inheritance — not (2,3,7) geometry),
§2.23 (PSL vs Clifford register), Paper II §3.4 / §3.4.4 (the substrate action and
its GP representation), §3.06/§3.07 (the chord-CR and enrichment routes to cos(π/10),
both closed-negative — leaving this the operative path). Append-only.*
