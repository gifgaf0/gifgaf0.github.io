# G-INT1 — Execution Pre-Registration

**Question:** In the instantiated substrate (the I1–I3 roton-GP ticket, V4.26 §3.4-SYM), does the **internal octonion sector** carry a *gapped, Fano-selective* fluctuation channel whose dynamical content includes a **scale-free (pure-number) quantity** — i.e. class-(a) content per the V4.46 ledger framing — or is the internal channel, like the density channel G-ζ1 already tested, free of any import-free dynamical number?

**Status:** PRE-REGISTRATION (before compute). Object, decision scalars, outcome arms, declared imports, and falsifiers locked below. No eigenvalue computed yet.
**Ledger basis:** V4.46 CANONICAL. Successor channel to **G-ζ1** (§2.88.D.1 — verdict DEGENERATE/INFORMATIVE-FAIL: the *density* channel is gapless at Γ, three Goldstone zeros, t→1 Bloch-transparent; finite-k density stop bands t = 0.36/0.54/0.75 reported, none in any target window). Gate name: **G-INT1** (internal octonion-sector channel).
**Register target:** Structural selection results (S_Fano; F₂₁ multiplet content) → R1. Any dynamical magnitude → R2 at most, import-contingent (see §4). The gate does **not** promote a physical bridge to R1.

---

## 0. Scope and freeze discipline (binding)

This gate is **substrate-instantiation work serving §2.53 (bilateral fold, cos π/10) and §2.64 (C = ξ_vac/a)** — the two non-frozen members of the V4.46 chokepoint cluster. **§2.52 Open 3 (pulsation = ζ) is frozen per standing instruction and is not worked here.** The instantiated substrate is the *shared bottom* of all three gates; characterizing its internal channel is upstream of, and common to, the cluster (the V4.46 §2.64.A Item C observation, made operational). No numeric target tied to §2.52 Open 3 enters before the final flagged comparison step, and even a coincident value is reported as "consistent with," never "derives," with the §2.52 Open 3 row left byte-identical and untouched.

---

## 1. Prior-turn correction (registered now, before compute)

The chat-side framing that motivated this gate asserted the internal octonion-sector modes are "gapped (not Goldstones of the phase)." Half right, half wrong — and the correction sharpens the object:

- **Right:** the internal (octonion-imaginary) fluctuations are *not* Goldstones of the U(1) condensate phase. That Goldstone is the density/acoustic mode G-ζ1 already found gapless.
- **Wrong → corrected:** at **two-body** order the internal sector is **not** gapped. The symmetric two-body kernel is forced by Schur to K_ij = a(r)δ_ij (§3.4.4, R1), so the interaction sees only the total density ρ = |ψ|² = Σ_k|ψ_k|² and is **accidentally O(16)-symmetric**. The seven imaginary directions are exact flat directions of the two-body action — gapless, roton-free; in the crystallized cell the lowest transverse Bloch band touches zero at Γ by the same accidental-symmetry zero-mode argument. No framework content can appear at two-body order in the internal sector (consistent with §3.4.4: "Fano content cannot imprint on the vacuum at any local order").
- **Consequence — the real object:** a gapped, framework-specific internal channel can appear **only** where the three-body Fano content lifts the accidental O(16) degeneracy down to G₂, and by the §3.4.4 locality result that content is active only **on/around a topological defect core carrying a Fano-line winding**. The *symmetric* three-body term is itself inert (§3.4.4 result 1); the carrier is the **oriented** term O = ∫ φ_abc ψ_a ∂_x ψ_b ∂_y ψ_c, a total derivative that is nonzero only on a defect core, Fano-line-selective. G-INT1 therefore targets the **internal-sector BdG spectrum around a Fano-line defect core**, not the uniform two-body vacuum.

This correction is part of the registration: if the two-body internal sector turns out *not* flat, that is a **surprise and an error flag**, not a pass.

---

## 2. Object (the registered §3.4.4 object, not a new model)

ℏ = m = 1, 2-D. Field ψ ∈ ℂ⊗𝕆 (eight components ψ₀…ψ₇; e₀ the real **1** of G₂, e₁…e₇ ↔ the seven Fano points, the irreducible **7**).

  E[ψ] = ∫ ½|∇ψ|² + ½∫∫ ρ(x) U(x−x′) ρ(x′) − μ∫ρ + (oriented three-body term on cores)

Soft-core kernel **U(r) = g·θ(R−r)** with the MV-G1 canonical values **g = 22.0, R = 1.0, ρ₀ = 1.0** (`mv_g1_minimiser.py` defaults; the V4.26 R1 row). Continuum Fourier kernel Ũ(q) = 2πgR²·J₁(qR)/(qR), Ũ(0) = gπR². ρ = Σ_k|ψ_k|². **These three numbers are the I1–I3 instantiation already on the ledger; nothing in this session retunes them.** The only structural additions over G-ζ1 are both already ledger-R1 (§3.4.4), not new model: (i) carrying the octonion-component index on ψ; (ii) the oriented three-body term, included at the registered form with coupling λ (status declared in §4).

**Reference scale:** μ ≡ the chemical potential. Every decision scalar is a **dimensionless ratio in units of μ**, so the "one scale" (I3) is divided out by construction.

---

## 3. Decision scalars (committed now)

**Primary (structural; crosses no M.CW axis; the bankable, import-free content):**

- **S_Fano ∈ {selective, non-selective}.** Does the three-body term gap / bind / chirally-split an internal mode at the core **iff** the core winding directions form a Fano line, and leave the internal sector unaffected on a non-line core? (The §3.4.4 / §3.4.5 selection rule, now read off the *dynamical fluctuation spectrum* rather than a static charge — new territory: §3.4.5 established it for the static linking charge Q_φ only.)
- **Multiplet content.** The affected internal modes carry the F₂₁ representation **1 ⊕ 3 ⊕ 3̄** of the seven (the §3.4.4 splitting under the realized F₂₁ ⊂ G₂). A λ-independent, scale-independent group-theoretic fact; confirming it in the spectrum is R1 structural.

**Secondary (the breach test; a priori narrow):**

- **Any geometry-protected pure number** in the internal spectrum — a dimensionless quantity fixed by lattice geometry alone, independent of λ, μ, g. Registered candidates: (a) a protected ratio between two distinct gapped internal branches; (b) the internal roton wavevector ratio k_int/k_dens, if the core induces an internal roton at a geometry-fixed wavevector. **A priori expectation (registered):** none exists — the internal gap *magnitude* scales with the new coupling λ (class b), so the breach arm requires a genuine surprise (a quantity in which λ cancels). Committing this expectation makes a positive result a real surprise, not a fitted one.

---

## 4. Declared imports (state honestly; do not derive past these)

- **I1–I3 ticket — unchanged.** g = 22.0, R = 1.0, ρ₀ = 1.0; scalar soft-core; one scale (μ). Not retuned.
- **λ (the oriented three-body coupling) — the located candidate import.** By M.CW a coupling magnitude is not a combinatorial output. The structural results (S_Fano, the 1⊕3⊕3̄ content) are **λ-independent** — they are yes/no and representation facts, not magnitudes. Any internal *gap magnitude* is λ-dependent and therefore class-(b) unless it appears inside a λ-canceling dimensionless ratio. **If the gate ends STRUCTURAL-ONLY, λ is the named second import for §2.53/§2.64** — the concrete object M.BRIDGE predicts must exist.
- **Per-axis (M.REL) accounting, committed now.** *Scale:* a gap value in μ-units is admissible only if invariant under rescaling μ (else class b). *Sign:* the oriented term's chirality (sign of any ± split) is sign-class — reportable as structure, not credited as a derived value (M.CW). *Metric:* any wavevector (k_int, k_dens, ξ-related) is metric-class — a *ratio* of two such may be import-free, a single value is not. *Ontology:* the "gap = attenuation channel" reading is M.ONT-adjacent and stays R2.

---

## 5. Outcome arms (fixed now, before first eigenvalue)

| Outcome | Verdict | Meaning |
|---|---|---|
| **STRUCTURAL-ONLY** (expected) | R1 structural + M.BRIDGE strengthened | S_Fano = selective and the 1⊕3⊕3̄ content confirmed **in the dynamical spectrum**, but every dynamical magnitude is class-(b) (λ-dependent; no geometry-protected pure number). Extends the §3.4.4 selection-rule ladder from static charges to the fluctuation spectrum; confirms the dynamical bridge needs the λ import; **names λ as the located second import** for §2.53/§2.64. A closure-shaped characterization, not an empty wall-hit. |
| **GAPPED-SCALE-FREE** (breach) | R2 (import-contingent) → flagged compare | A geometry-protected dimensionless dynamical quantity exists (pure number, λ/μ/g-independent). Class-(a). **Only then** load comparisons, flagged, freeze intact — a coincident value is "consistent with," never "derives." This would be the program's first import-free dynamical number, the analogue of the PSL(2,7) λ₁ = 2/3 precedent in the *dynamical* sector. |
| **DEGENERATE** (stronger null) | INFORMATIVE-FAIL | The three-body content fails to gap/bind/split even on a Fano-line core (the oriented term's total-derivative character persists into the fluctuation spectrum; internal sector gapless everywhere). Then **neither density (G-ζ1) nor internal channel carries a gapped channel, two-body or three-body** — the strongest M.BRIDGE-as-theorem evidence to date. |

No arm "wins." STRUCTURAL-ONLY and DEGENERATE are both findings at full weight; GAPPED-SCALE-FREE survives only at the cost of a flagged, freeze-respecting comparison and is a priori unlikely.

---

## 6. Eddington guard

The breach arm requires a **λ-canceling** dimensionless quantity. The failure mode to guard against: quoting a gap "≈ [target]" after implicitly choosing λ to land it there. λ is therefore **fixed by structure or left symbolic** — never tuned post-spectrum. A second guard inherited from G-ζ1: report the **full** internal spectrum, never a frequency selected by proximity to any ledger value. A third, from M.2π: the internal roton wavevector (if any) is **2π-B-class** (lattice closure budget on K₇) — do not conflate it with the azimuthal 2π-A or the SO(3) 2π-C.

---

## 7. Execution plan (on go)

Standalone, self-verifying, no framework number under test (Eddington guard):

1. **Object reproduction (R1 baseline).** Re-crystallize the big-box p6m ground state at the canonical parameters (N=160, L=20, quench, seed 7); confirm local ψ₆ dominant; measure k_c. Relax in the oblique triangular primitive cell; select a* by energy-density minimization (the crystal picks its own a).
2. **Two-body internal control (registered prediction).** Build the transverse BdG operator L_⊥ = −½∇² + (U*ρ(x) − μ) on the crystallized cell (no anomalous X term — δ|ψ|² is purely longitudinal). **Assert gapless at Γ** (lowest transverse Bloch band → 0; eigenvector in an imaginary direction). A nonzero gap here is a bug/surprise flag, not a result.
3. **Fano-line core.** Embed a single defect core whose internal winding lies in a **Fano line** (e.g. {e₁, e₂, e₄}) in the crystallized vacuum; relax. Build the second-variation internal operator **including the oriented three-body term**. Diagonalize. Catalogue in-gap / bound / chirally-split internal modes; classify by F₂₁ rep (target 1 ⊕ 3 ⊕ 3̄).
4. **Non-line control.** Repeat (3) on a **non-Fano-line** core ({e₁, e₂, e₃}). Pre-registered prediction: no gap/bound/split internal mode (S_Fano selective). A null core that still shows an internal mode falsifies S_Fano.
5. **Scale test (the class-(a) discriminant).** Recompute the spectrum at rescaled μ (and at fixed dimensionless coupling) and at two values of λ. Any quantity proposed as class-(a) must be **constant** across the μ-rescaling **and** independent of λ. Report which quantities are constant and which drift.
6. **Limit checks (must pass before any verdict).** (a) λ → 0: internal sector decouples, recover the step-2 gapless control. (b) Static limit: recover the §3.4.5 selection rule on Q_φ (Fano-line core carries the static charge; non-line core zero). (c) Plane-wave cutoff stability.
7. **Comparison (last, separate, only if GAPPED-SCALE-FREE).** Only here is any ledger value loaded, and only as a flagged "consistent with." §2.52 Open 3 stays frozen regardless.

**Falsifiers:** two-body internal sector gapped (→ bug); S_Fano non-selective (the dynamical channel does *not* track Fano lines → the §3.4.4 ladder does not extend to fluctuations, a real negative); multiplet content ≠ 1⊕3⊕3̄ (→ recompute the realized-symmetry decomposition); a quantity claimed class-(a) that drifts under μ-rescaling or λ (→ class b, not a breach — accept the demotion, do not re-pick λ).

---

*Pre-registration only. Not folded. Serves §2.53 / §2.64; §2.52 Open 3 frozen and untouched. Connects to §3.4.4 (locality / single-scalar kernel), §3.4.5 (static selection rule), G-ζ1 (§2.88.D density channel), and M.BRIDGE / M.REL / M.CW. Execute as a separate gated step; outcome block to be written against the canonical at fold time.*
