# G-2a-S4 FIRST-LEG REPORT (chat-side)
**Date:** July 8, 2026. **Pre-registration:** `G_2a_S4_EXECUTION_PREREGISTRATION.md` (filed prior to computation; targets quarantined until unseal). **Script:** `g_2a_s4_firstleg.py` + two follow-up checks (extension to S³; peripheral-orientation classification). **Base:** V4.52.

## P1 — Schur–Weyl (H-P1: PASS, R1 candidate)
(ℂ²)^⊗3, D = 8. S₃ slot-permutation action verified as a homomorphism (36 products); diagonal su(2) verified to commute with all of S₃.
- Isotypic dims: **sym = 4, alt = 0, mixed = 4** (alt vanishes: Alt³(ℂ²) = 0, as required for d = 2).
- su(2)-commutant on sym block: **dim 1 → irreducible**. On mixed block: dim 4 → reducible (2 × spin-1/2).
- The symmetric isotypic is the **unique** SU(2)-irreducible S₃-isotypic component. Casimir on sym block: uniformly 15/4.
- **Doubling incompatibility re-verified in context:** binary doubling ℂ²⊕ℂ² has Casimir spectrum {3/4 ×4} ≠ sym block {15/4 ×4} — not isomorphic as SU(2)-modules. The symmetric channel is a ternary object; no Cayley–Dickson/Clifford doubling step produces it. (Same-dimension trap: both are 4-dim — the incompatibility is module content, not dimension. Distinct-4 discipline held.)

**Quarantine unseal:** d_sym = 4 = target; Casimir 15/4 = spin-3/2. Consulted only after all computations.

## P2 — Motion-level exchange realizability (H-P2: PASS, R1 candidate)
Borromean rings complement `6^3_2` (SnapPy 3.3.2): 3 cusps, vol 7.32772475342 (two ideal regular octahedra, consistent with Thurston).
- Symmetry group: **Z/2 × octahedral group, order 48**. Orientation-preserving: 24.
- **All 48 isometries extend to ambient homeomorphisms of (S³, L):** every cusp map is ±Id (meridian ↦ ±meridian, longitude ↦ ±longitude; no shearing, no meridian/longitude mixing).
- **Image of extendable Isom⁺ in S₃ (cusp permutations): ALL of S₃**, including all three transpositions. A transposition of two strands IS realizable by an orientation-preserving ambient homeomorphism of S³. H-P2 verdict: exchange route ALIVE. Reconciliation with G-2a-S2: no contradiction — S2's rigid rotation group of the golden-ellipse representative is A₄ (cyclic strand action only); the transposition here is a non-rigid ambient motion class. Rigid symmetry ⊊ motion group.

## P2-bonus — The parity law and the motion-group structure (unregistered finding, R1 candidate)
Classifying every extendable orientation-preserving isometry by (cusp permutation σ, per-strand peripheral signs ε = (ε₁,ε₂,ε₃), εᵢ = ±: cusp map = εᵢ·Id):

| σ class | realized sign patterns |
|---|---|
| identity, 3-cycles (even) | +++, +−−, −+−, −−+ |
| transpositions (odd) | ++−, +−+, −++, −−− |

**Parity law: sgn(σ) = ε₁ε₂ε₃** — exactly the det = +1 condition on signed 3×3 permutation matrices. Each (σ, ε) pair with sgn(σ)Πεᵢ = +1 occurs exactly once; 6 × 4 = 24 = |Isom⁺|, so the peripheral-action map is an isomorphism:

**The orientation-preserving ambient symmetry group of the Borromean rings, acting on (strand labels, strand orientations), is exactly the octahedral rotation group O ≅ S₄ in its standard signed-permutation representation.**

Physical reading of ε = −1: cusp map −Id flips meridian AND longitude together — the strand "turned over" (rotation by π about a diameter). For a vortex ring this is a physical identity operation (circulation co-rotates; right-hand pairing preserved), so all 24 motions act on identical vortex strands. The law says: **exchanging two strands necessarily turns over an odd number of rings.**

**Consequence for Gate 2a (R2, stated carefully):** the octahedral premise killed by G-2a-S2 at the rigid-geometry level **reappears at the motion-group level** — the strand motion group is O ≅ S₄. G-2a-S1's banked forcing theorem (D1 = 1: 2O admits a unique genuine irrep of even dimension, the 4-dim quartet) was conditional on octahedral symmetry; the condition is now satisfied by the motion group, not the shape. The chain sharpens to:

  [motion group of strands = O ≅ S₄ — R1, this gate] → [spinor lift O → 2O, i.e. −1 ↦ −Id — **the §2.50 import, still open**] → [unique genuine 4-dim irrep — R1, G-2a-S1] → factor of 4.

Convergently, H-P1 gives: [per-strand carrier ℂ² with exchange statistics — same §2.50 import] → Sym³(ℂ²) = the unique irreducible symmetric channel → the same factor of 4. **Two independent routes, one shared bottleneck import.** M.BRIDGE respected: no observable computed; the import is located and shared, not resolved.

**Eddington record (distinct-48 / distinct-S₄):** |Isom(BRC)| = 48 = |2O| — same integer, different provenance; NO identification made. The motion-group S₄ (this gate) vs the Fano line-stabilizer S₄ (§2.85 Part C) vs spatial O — three S₄'s; any identification requires derivation. The suggestive convergence (motion-S₄ acts on strands-with-orientations exactly as O acts on axes-with-signs) is logged as R3.

## Falsification-condition audit
- P1 fail conditions: not triggered (sym block irreducible and unique).
- P2 fail condition (image = A₃ only): not triggered.
- P2-sign: NOT computed this session — the FR-type sign of the exchange motion in the spinor/framed lift is exactly the §2.50 per-strand spinor phase import, per pre-registration §3 third clause: verdict class = located-import, not derivation.

## Second-leg spec (CC)
Zero shared machinery required:
1. **P1:** character theory / Young symmetrizers (no numpy tensor construction): verify isotypic dims (4,0,4), irreducibility of sym block via ⟨χ,χ⟩ = 1 under SU(2) restricted to a dense subgroup or via highest-weight count; verify Casimir content and the doubling-module inequivalence.
2. **P2:** independent of SnapPy's symmetry_group: either (a) construct the two-ideal-octahedra gluing and compute the combinatorial symmetry group + cusp action directly, or (b) verify via the Wirtinger/π₁ presentation that an automorphism realizing a transposition with peripheral ±Id structure exists (Mostow: Out(π₁) = Isom), or (c) independent SnapPy install with `M.symmetry_group()` on an independently built triangulation (e.g. from a link diagram via `Link` → exterior), then verify vs (a)/(b) for at least the order, the S₃ image, and the parity law.
3. **Parity law:** independently verify sgn(σ) = Πεᵢ over all 24, and the exactly-once occurrence of each admissible (σ, ε).

## Verdict (first leg, pending second leg)
- H-P1: PASS (R1 candidate).
- H-P2: PASS (R1 candidate) — exchange realizable, extendable, orientation-preserving; full S₃.
- Parity law + motion group ≅ O ≅ S₄: NEW R1 candidate, the gate's principal yield.
- H-P3 conditional chain: sharpened to a single shared import (§2.50 per-strand spinor phase), now feeding TWO convergent routes.
- No register change proposed for anything prior; no §3.x; M.BRIDGE intact; §2.52 Open 3 untouched.
