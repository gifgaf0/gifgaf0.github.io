# G-2a-S8 EXECUTION PRE-REGISTRATION
## The spinorial structure of the flat crystallographic home

**Filed:** July 10, 2026 — before any machine computation.
**Status:** DRAFT pending author lock. No compute has run against any hypothesis below.
**Base ledger:** SQT_Master_Ledger_v4_56_CANONICAL.md (md5 1b1dc6b8824daf5c9c06c521d97065db).
**Executes:** the §2.50-adjacent R3 bank of §2.87.F, item (a): "turn-over = half-lattice translation in the flat home, strand-aligned — adjacent to §2.50 thinking, NO import claimed." This gate tests whether the flat home *forces* spinorial signs, and which ones.
**Standing constraints honored:** the §2.52 Open 3 row untouched. No observable, no μ_n. M.CW / M.BRIDGE / M.REL / M.ONT govern.

---

## 0. Objects (all inherited from S7, both-legs-verified there)

- Γ = the #24 cube-folding group: ⟨r₁, r₂, r₃⟩, π-rotations about the pairwise-skew axes {(t,0,½)}, {(½,t,0)}, {(0,½,t)}; lattice L = {v ∈ ℤ³ : all coordinates even or all odd}; E³/Γ = the flat Borromean orbifold, cone angle π (CHK Ex. 2.32, adopted prior art per S7).
- N = the Euclidean normalizer at the cubic point; N/Γ ≅ ℤ/2 × S₄ via Φ_flat (S7 H-C, R1 two-leg); T_N = ℤ³; turn-over of strand f = translation by e_f ∈ T_N ∖ L (S7 B2, R1 two-leg).
- **N⁺** = the orientation-preserving part of N (kernel of d = det); N⁺/Γ ≅ S₄ = the motion group. **Scope restriction: this gate works in Spin(3)⋉ℝ³ over N⁺ only.** The orientation-reversing sector requires Pin⁺/Pin⁻ and is OUT OF SCOPE — banked as the S9 candidate (the amphichiral involution's spinorial behavior is Pin-structure-dependent; the fork is real and deferred, not ignored).
- ρ : Spin(3)⋉ℝ³ → SO(3)⋉ℝ³, the double cover; Spin(3) = unit quaternions; ker ρ = {±1} central. Pure translations have preimage {±(1, t)}.

**Definitions.**
- A *spinorial lift* (spin structure over H ≤ SO(3)⋉ℝ³) = a homomorphism s : H → Spin(3)⋉ℝ³ with ρ∘s = incl.
- H̃ = the full preimage ρ⁻¹(H): the canonical central ℤ/2 extension of H.
- A *Γ-spinorial structure* = a Γ̃-equivariance datum on spinor fields over ℝ³ with the central −1 acting as −Id. If lifts of Γ do not exist, these structures are the only spinorial objects available; their twist set is a torsor over Hom(Γ, ℤ/2) (twisting a generator lift by χ(g) = ±1).
- **Loop dictionary (M.2π discipline — declared up front, the trap surface of this gate):**
  - *Orbifold cone loop* m_f: once around the singular circle of strand f in the quotient; deck class = r_f (the local π-rotation); total quotient angle π.
  - *Ambient 2π meridian* μ_f: the full 2π loop around the strand axis upstairs in ℝ³ (the physical "rotate once fully around the vortex filament"); projects to the cone loop traversed twice; deck class = r_f².
  - The FR / §2.50 per-strand datum lives at μ_f (2π-C), NOT at m_f. Any silent substitution of m_f for μ_f is the pre-declared failure mode.

---

## 1. Hypotheses and decisive bits

### H-A — the splitting obstruction [R1 target]
**Claim:** the extension 1 → ℤ/2 → Γ̃ → Γ → 1 does NOT split: no spinorial lift s : Γ → Spin(3)⋉ℝ³ exists.

**Registration-time hand-sketch (disclosed, per S7 practice):** any section must send a torsion π-rotation r_f (r_f² = e in Γ, S7 H-A) to ±q_f with (±q_f)² = q_f² = −1 ≠ s(e) = 1. One-line obstruction. Superseded by the machine leg.

**Consequence if H-A holds:** every representation of the flat home's deck group on spinor fields factors through Γ̃ with **−1 ↦ −Id forced** — the exact algebraic shape of the §2.50 desideratum, realized structurally *in the orbifold home* (identification hazard quarantined; see Eddington §4).

**Machine leg:** exact verification q_f² = −1 for the three axis lifts + exhaustive sweep over all 2³ generator sign assignments against the S7-verified relation set, confirming no consistent section. **Falsifier (live):** a consistent section found ⇒ H-A false ⇒ gate re-scoped before proceeding.

### H-B — the ambient-2π meridian sign [decisive bit B1]
**Claim under test:** in every Γ-spinorial structure (all twists χ ∈ Hom(Γ, ℤ/2)), the monodromy assigned to the ambient 2π meridian μ_f is **−1, for every strand f**.

**Registration-time hand-sketch (disclosed):** μ_f ↦ r_f² upstairs; monodromy = (χ(r_f)·(±q_f))² = q_f² = −1, twist-independent since χ(r_f)² = +1. Superseded by the machine leg, which must verify this over the full enumerated twist set, not the sketch.

**Pre-declared branches, equal weight:**
- **B1-FORCED:** −1 across the entire structure set → the per-strand 2π spinor phase is structural in the flat home (conditional on the imports of §3).
- **B1-FAILS:** any structure with monodromy +1 at μ_f → the flat home does NOT force the phase → INFORMATIVE-NEGATIVE, filed at full weight; the §2.50 import stays exactly where it is.

**Also banked if confirmed (R3, uninterpreted):** the cone loop m_f carries ±q_f — order 4, twist-DEPENDENT in sign — a ℤ/4 refinement of the ℤ/2 phase native to the cone-π scaffolding. Logged only; no interpretation, no import claimed.

### H-C — the turn-over sign system [decisive bit B2]
**Question:** for the strand-f turn-over e_f ∈ T_N ∖ L (S7 B2), is its sign on spinors *forced* or a *structure choice*, over the set of N⁺-compatible spinorial structures?

**Computation plan (finite-model reduction; ℤ/2-linear):**
- (c1) Compute the mod-2 abelianization classes: [e_f] ∈ H₁(N⁺; ℤ/2) and [r_f], [(1,1,1)] ∈ H₁(Γ; ℤ/2). Twist-invariance of a sign ⟺ vanishing of the class. Explicit relation audit validates the finite model (all consistency conditions are ℤ/2-linear over the finite presentations; the chat leg asserts model validity by exhibiting the relation set and checking closure).
- (c2) **The triple relation (registration-time hand-sketch, disclosed):** e₁e₂e₃ = translation by (1,1,1) ∈ L ⊂ Γ (the word attainment is S7 H-A, R1). Hence the *product* of the three turn-over signs equals the (1,1,1)-lift sign in the underlying Γ-structure. Compute whether that product is twist-forced, and if so its value. No hand-sketch exists for the *individual* e_f verdict — genuinely open, all branches live.
- (c3) S₄-equivariance constraint: the conjugation relations g e_f g⁻¹ = e_{σ_g(f)} (S7's strand-aligned dictionary) impose sign relations across the strand triple for structures on which the N⁺-action is defined; compute the invariant-twist subset (restriction-invariance layer) and the extension-sign layer separately, and report which combinations exist.

**Pre-declared branches, equal weight:**
- **B2-FORCED(−1):** the turn-over is spinorially odd, structurally.
- **B2-FORCED(+1):** the turn-over is spinorially even — kills the naive "turn-over carries the FR sign in the flat home" reading. Decisive negative, full weight.
- **B2-CHOICE:** the sign is a genuine spin-structure datum (the classical T³ periodic/antiperiodic boundary condition surviving into N⁺) — the import LOCATED as a boundary-condition choice on the flat home. Flagged now: possibly the most M.BRIDGE-informative branch; not privileged by this registration.

### H-D — verdict [R2; M.REL per-axis]
Grade the outcome per axis: **scale** — none anywhere in this gate; **metric** — flat, inherited from S7 (unchanged); **sign** — THE axis under test (forced vs import, per B1/B2 branches); **ontology** — two layers: (i) the cone-π singular scaffolding (S7's undeclared physical import, R3 — everything in this gate is conditional on it), (ii) the NEW hazard: identifying the framework's per-strand carrier ℂ² with orbifold spinors — **NOT claimed by this gate**, quarantined (§4).

**Verdict classes pre-declared:**
- **FORCED-SIGN** (B1-FORCED and B2 forced either way): the sign content of the per-strand phase is structural in the flat home; §2.50's import RELOCATES to {orbifold scaffolding} + {carrier identification} — a sharpened LOCATED-IMPORT. **Explicitly NOT a §2.50 closure.**
- **SPLIT** (B1-FORCED, B2-CHOICE): the 2π phase structural, the turn-over sign a located boundary-condition import.
- **NEGATIVE** (B1-FAILS): the flat home forces nothing; filed at full evidential weight.

---

## 2. Two-leg plan
- **Chat leg** `g_2a_s8_chatleg.py`: exact arithmetic throughout. The binary octahedral machinery precedent is canon's own `spin32_2O.py` (§2.85); this leg builds its sign systems independently and reuses no S7 result without re-assertion. All decisive bits computed as exact ℤ/2-linear solves over explicitly listed presentations; every relation asserted before use.
- **CC leg:** own implementation, different method (e.g., cohomological extension-class route vs. direct quaternion enumeration), commit cited by hash. Shared-presentation caveat expected per the S4/S7 precedent (the Γ presentation is the both-legs-verified S7 object); independence at the code+method level; flag, don't hide.
- Deviations between legs logged verbatim; resolution bugs distinguished from substantive disagreements per the S7 record style.

## 3. Declared imports (standing)
Cone-π orbifold scaffolding (S7, R3, physically undeclared); flat metric (S6/S7 axis); M.ONT filament-core strand ↔ singular-circle dictionary (V4.51). No new import is *introduced*; the gate tests which signs sit above vs. below the existing ones.

## 4. Eddington traps (declared)
1. **The −1 = −1 trap** (the S7 48=48 pattern): orbifold-spinor −1 (this gate) vs. framework per-strand carrier −1 (§2.50). Same symbol, unidentified objects. The identification is an import this gate does NOT make. Any drift toward "therefore μ_n" fails the gate's own scope clause.
2. **The 2π substitution trap** (M.2π class): m_f vs μ_f per the loop dictionary of §0. The decisive bit is defined at μ_f only. 2π-C throughout; 2π-B (closure budget, §2.14/§2.50 mass sector) is a different object and is not touched.
3. **No numeric targets.** μ_n sealed; no mass, no moment, no observable consulted at any step.
4. **Prior-art expectation HIGH:** disclination/cosmic-string spinor holonomy (condensed-matter dialect); Dekimpe–Sadowski–Szczepański 2006 and the GHW literature (flat-manifold dialect — governs the torsion-free sister #19, not the torsion orbifold directly). LSF report travels with the gate; expected novelty class: novel-in-assembly. If the assembled result itself is located in the literature during execution, the gate downgrades to prior-art adoption with attribution — that outcome is pre-accepted.

## 5. What this gate does NOT claim
No §2.50 closure (structurally impossible from here: the carrier identification and the orbifold ontology remain imports on any branch). No spinor physics for the actual K₇ tube. No μ_n, no observable — M.CW/M.BRIDGE intact. No Pin/orientation-reversing content (S9 bank). The §2.52 Open 3 row untouched.

## 6. LSF registration record (chat-side, July 10, 2026, pre-compute)
- Dekimpe, Sadowski, Szczepański, *Spin structures on flat manifolds*, Monatsh. Math. 148 (2006) 283–296 — lift-classification method; adopted.
- Hantzsche–Wendt / GHW literature (Rossetti–Szczepański 2005; Lutowski–Popko–Szczepański Spin^c) — the torsion-free sister #19 context; adopted for contrast.
- Disclination holonomy for half-integer spin (graphitic cones; 2π-disclination rotation holonomy with U(R_2π) = −1): established physics — the *local* monodromy content is prior art; adopted with attribution.
- No published treatment found, in any searched dialect, of the spinorial lift structure of the #24 Borromean orbifold in link-symmetry terms with a strand-aligned turn-over sign system.

## 7. Sibling item registered alongside (not a gate)
**KF partial-discharge memo:** the S7 Koch–Fischer cross-check is now partially corroborated from three openly retrievable fragments — (i) cctbx general-metric normalizer generators for #24 (translations (½,0,0),(0,½,0); inversion at origin — matches T_N/L ≅ (ℤ/2)² and −I unshifted); (ii) the published relation N_E(highest-symmetry metric) = N_A with m·n = 6 for orthorhombic types (exceptions Ibca, Imma only), giving [N_E(a=b=c) : Γ] = 6 × 8 = 48 under the n = 1 reading for #24 (reading flagged; the three axial projections are equivalent by the body-diagonal C₃, itself corroborated by fragment iii); (iii) the metric-specialization supergroup pairing I2₁2₁2₁ → I2₁3 (cubic C₃ extension genuinely crystallographic). The verbatim IT-A Table 15.2.1.4 row remains unretrieved (paywalled). Proposed disposition: additive annotation on §2.87.F's cross-check note, honestly labeled reconstruction-from-fragments — upgrades "rests on two agreeing computations" to "two agreeing computations + three published fragments"; does NOT claim the table row. Author authorization required before fold.

---
*Append-only discipline: this file stages; nothing folds without authorization. Final § designation assigned on fold-in.*
