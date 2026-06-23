# Staging Memo — §2.64 Three-Part Disposition

**Vortex-log form promotion · ξ_vac second-anchor declaration · §2.64 ↔ §2.52 Open 3 ↔ §2.53 chokepoint merger**

**Date filed:** June 23, 2026
**Prepared against:** canonical V4.45
**Status:** STAGING — audit before fold. Not yet folded. Fold author assigns version.
**Mode:** Audit (derivation-standard; registers assigned per item)

**Register summary:**
- Item 0/1 — algebraic identity behind the gate: **R1**
- Item A — vortex-log form identification: **R2** (form motivated; K₇ discrete-sum derivation *retained as open*)
- Item B — ξ_vac second-anchor: **status correction**, R2-backed argument
- Item C — three-gate chokepoint merger: **R2** (cross-cutting structural observation)

**Cross-references:**
- §2.64 (L4.5 gate, angular debt; continuum-limit fidelity two-part condition (a)+(b))
- §2.50 / §2.50.A (electron = unit trap; r_eff(electron) ≡ 1 definitional anchor; 3.81% interpolation slack → m₀)
- §2.48 (angle as fundamental coordinate; energy = cost of holding angle against lattice)
- Paper VII §9.1 (m₀ = m_e / e^(2π/Φ); "one observational anchor, zero tuned parameters")
- §2.52 Open 3 (pulsation = ζ from §3.4 first principles; **frozen per standing instruction**; blocked on substrate-instantiation import)
- §2.53 bilateral fold at cos(π/10) (V4.34 conditional-R2; bottoms at the I1–I3 import)
- V4.26 §3.4-SYM (I1–I3 roton ticket — the standing substrate-instantiation import)
- M.BRIDGE (observable bridges require an undeclared import; pattern has theorem shape)
- M.REL (per-axis import test: scale / metric / sign / ontology)
- M.CW (combinatorics cannot fix dimensionful constants, a metric, or a sign)
- `HANDOFF_MASS_CALC_v3.md`, `sqt_v20_merged.jsx`, `SQTCalculator.jsx` — carry the load-bearing string "Zero Free Parameters" (see Item B)

---

## 0. One-line disposition

The §2.64 coarse-graining gate does **not** resolve into an independent bounded target. Traced to the bottom, its entire non-anchored empirical content is the single dimensionless constant **C = ξ_vac / a** (vortex-core / lattice-spacing ratio). C is dimensionful-dynamical in origin — barred from combinatorial derivation by M.CW — and lands on the **same I1–I3 substrate-instantiation import** that already blocks §2.52 Open 3 and §2.53. This memo files three consequences and changes no prior body content.

---

## 1. The arithmetic that drives the gate (R1)

The mass anchor is fixed:

  **m₀ = m_e / e^(2π/Φ)**,  Φ = 2π − φ²/(8π²) ≈ 6.250028,  m_e = 0.511 MeV (the single observational anchor).
  Check: 2π/Φ = 1.005305 → e^(2π/Φ) = 2.73289 → m₀ = 0.511 / 2.73289 = **0.18699 MeV**. ✓

The continuum interpolation is r_eff(L) = 1 + ln(1 + L/ξ_vac), ξ_vac = 100φ ≈ 161.803 fm. Its value at the electron closure L = 2π:

  r_eff(2π) = 1 + ln(1 + 2π/(100φ)) = 1 + ln(1.038833) = 1 + 0.038097 = **1.0381**. ✓

The definitional anchor (§2.50.A) sets r_eff(electron) ≡ 1. Therefore:

> **The entire "3.81% slack" of §2.50.A is the identity ln(1 + 2π/ξ_vac), controlled by ξ_vac alone.**

Because the MeV scale is carried by m_e, the §2.64 gate cannot and does not produce a scale. The only non-anchored quantity it touches is this one logarithmic term, hence the one constant ξ_vac (equivalently C = ξ_vac/a). This is an exact algebraic statement, not an interpretation. **R1.**

---

## 2. Item A — Vortex-log form: R2 structural identification (derivation gap retained)

**Mathematical fact (R1).** The logarithm is the continuum image of a harmonic sum. With cell index n and step a:

  r_eff(N) = 1 + Σ_{n=0}^{N−1} 1/(C + n) = 1 + [ψ(C + N) − ψ(C)],  C = ξ_vac/a, N = L/a,

and since ψ(x) ~ ln x for large argument, ψ(C+N) − ψ(C) → ln(1 + N/C) = ln(1 + L/ξ_vac). So the log form is exactly the large-C limit of a digamma (harmonic) sum. This is pure mathematics.

**Structural identification (R2; itself an import).** A harmonic/logarithmic self-energy is the standard form for a **superfluid vortex line**: ε ∼ (stiffness) · ln(R_outer / a_core), with ξ_vac playing the role of the core / healing scale and L the running outer scale. This re-reads r_eff not as an arbitrary curve fitted to asymptotic ropelength behavior, but as the **expected functional form of a logarithmic vortex self-energy**, with the digamma identity supplying the explicit discrete↔continuum bridge.

**What this improves.** §2.50.A currently describes r_eff(L) = 1 + ln(1 + L/ξ_vac) as "a Register-2 functional form chosen to match asymptotic ropelength behavior, **not derived from K₇ lattice geometry**." Item A upgrades the *justification of the form* from "guessed interpolation" to "motivated vortex self-energy with an explicit harmonic-sum origin." Net effect: the imported content of r_eff is **isolated to a single dimensionless constant C**, rather than spread across an unmotivated functional shape.

**What this does NOT close (retained open, honest).**
- The vortex-energy logarithm is **imported physics**, not SQT-native (consistent with the §2.64 stiffness table, where Z₀ and ρ_s are flagged "Imported" and only κ = φ⁻⁴ is SQT-derived). Item A leans on that import; it does not remove it.
- The explicit demonstration that the **K₇ per-hinge angular-debt summand equals 1/(C+n)** — i.e. that the SQT discrete sum *is* this harmonic sum, not merely analogous to a generic vortex log — is **not performed here**. It remains the separate Tier-2 derivation target named in §2.50.A ("replace the continuum form with a derived discrete sum over lattice contributions").
- Whether the 3.81% is best read as an Euler–Maclaurin **endpoint correction** [ψ(C) = ln C − 1/(2C) − …, leading term O(1/C)], as genuine **running over the closure circumference**, or as a **bookkeeping artifact** of where L starts for the base unit, is **not adjudicated** — that adjudication is the §2.64(b) content and is downstream of the discrete summand. Candidate (endpoint correction) is flagged **R3**.

**Filing.** Item A is **R2**: structural-form identification, with the discrete-sum derivation and the import status both explicitly retained as open. It is *not* a derivation of r_eff from K₇ axioms and must not be cited as one.

---

## 3. Item B — ξ_vac second-anchor declaration (status correction, R2-backed)

**The "100" has no combinatorial home.** Structural search (this memo, no new compute):
- **Not a structural count.** The framework's load-bearing integers are 7, 21, 42, 168, 600 (and Fibonacci indices). None is 100 and none reduces to it. The nearest, |PSL(2,7)| = 168, is 40% away; reaching for it to manufacture 100 would itself be an Eddington grab.
- **Not a golden-ratio power.** φ⁹ = 76.01, φ¹⁰ = 122.99. The value 100 falls strictly between; no clean power lands there.
- **Not from the one native stiffness.** κ = φ⁻⁴ gives 1/κ = φ⁴ = 6.854 or 1/√κ = φ² = 2.618 — short by ~1.5 orders of magnitude.

**What C is, structurally.** C = ξ_vac/a is a **cutoff ratio** — vortex-core/healing length over lattice spacing — i.e. a ratio of two dynamically-set microscopic lengths. By **M.CW**, combinatorics cannot fix a dimensionful constant; the dimensionless ratio is the only combinatorially-admissible part, and the structural search above finds no combinatorial address for its value. By **M.REL**, the scale axis is a distinct import from the metric/sign axes; ξ_vac is a scale-axis quantity.

**The round-decimal tell.** A genuine healing-length/spacing ratio derived from substrate dynamics would be expected to come out irrational-looking (e.g. 147.3, 173.9), not exactly **100**. An exact round decimal in a φ/π/integer-topology framework is the signature of a value *selected* to fit the spectrum shape adequately and then frozen — not of a derived constant.

**Honest accounting.** Pending a derivation of C through the substrate import (Item C), the framework's parameter count should be stated as:

> **Two anchors:** m_e (sets the mass *scale*) and ξ_vac (sets the *logarithmic running scale* of r_eff). Zero further tuned parameters.

This is defensible and clean. It is a *correction*, not a retreat: every mass ratio, coupling, and ropelength still follows from geometry plus these two anchors.

**Load-bearing string flag.** "Zero Free Parameters" / "zero tuned parameters" appears in:
- Paper VII §9.1 (text),
- `sqt_v20_merged.jsx` header ("Superfluid Quantum Topology — Zero Free Parameters"),
- `SQTCalculator.jsx` header and the constants banner.

If Item B is adopted, these strings are inaccurate and must be updated to the two-anchor statement. **This is a separate task** (calculator + Paper VII edit), not part of the canonical body fold; it is flagged here so the discrepancy is tracked rather than drifting.

**Door left open (no overclaim).** This memo does **not** assert that C is *provably* unfittable — only that the structural search found no combinatorial address and that the round value is a fitted-parameter tell. Should the I1–I3 derivation (Item C) yield C, ξ_vac is reclassified from anchor to derived at that time.

---

## 4. Item C — Chokepoint merger (R2, cross-cutting)

**The bottom of §2.64.** Item B shows §2.64's residual content is C = ξ_vac/a, a vortex-core/healing-length ratio. The healing length is set by substrate density and interaction strength — i.e. by the **instantiated substrate dynamics**, the I1–I3 roton ticket of V4.26 §3.4-SYM. §2.64 therefore bottoms out at I1–I3.

**The existing merge (credit, V4.34).** The ledger already records that **§2.52 Open 3** (pulsation = ζ) and **§2.53** (bilateral fold at cos π/10) bottom out at the *same* place: the V4.34 fold states the §2.53 closure "needs the instantiated substrate metric/dynamics, full stop — the same standing import (the I1–I3 roton ticket of V4.26 §3.4-SYM) that blocks §2.52 Open 3 (pulsation = ζ)," and that "**both §3.4 dynamical gates bottom out at the same place.**"

**This memo's contribution.** Extend that cluster to include §2.64. The merged statement:

> **§2.64, §2.52 Open 3, and §2.53 share one chokepoint: the I1–I3 substrate-instantiation import (V4.26 §3.4-SYM). Closing that single import closes all three; none is independently closable above it.**

**Interpretation (instance of M.BRIDGE).** The same undeclared import reappearing at a third, independently-motivated gate is exactly the M.BRIDGE pattern asserting itself with theorem shape rather than as three separate temporary gaps. The program has **one** §3.4 dynamical frontier, approached from three directions (mass-shape running; pulsation amplitude; fold convexity), not three frontiers.

**Freeze respected.** §2.52 Open 3 is frozen per standing instruction. This item is an **observation of shared structure only**. It proposes no work on §2.52 Open 3 and no unfreezing. It simply records that §2.64 joins the frozen cluster, so future effort is not misallocated to §2.64 as if it were a separate bounded problem.

**Filing.** Item C is **R2**, cross-cutting.

---

## 5. What this memo does NOT claim

- Does **not** derive m₀, the MeV scale, or ξ_vac. The scale remains anchored to m_e.
- Does **not** derive r_eff from K₇ axioms (Item A is form-identification with the discrete-sum derivation retained as open).
- Does **not** close §2.64. It reclassifies §2.64 as non-independent (merged into the I1–I3 cluster) and isolates its content to one constant.
- Does **not** assert C is provably non-combinatorial; it asserts no combinatorial address was found and that the round value is a fitted-parameter tell.
- Does **not** modify, attack, or unfreeze §2.52 Open 3.
- Does **not** edit the calculator or Paper VII; it flags those string updates as a tracked, separate task.

---

## 6. Audit flags (travel with this entry)

**Flag 1 — Item A's vortex analogy is an import, not a derivation.** The logarithmic self-energy is borrowed superfluid physics. The K₇-native demonstration that the angular-debt summand equals the harmonic sum 1/(C+n) is unperformed. Do not let "r_eff is the vortex log" be cited as "r_eff is derived."

**Flag 2 — The 3.81% interpretation is unadjudicated.** Endpoint-correction vs running vs bookkeeping artifact is R3 until the discrete summand exists. The §2.64(b) condition is precisely this adjudication and is not satisfied here.

**Flag 3 — "Two anchors" depends on the negative search holding.** Item B rests on "no combinatorial address found for 100." This is a search, not a proof. A later structural identification of 100 (e.g. as a genuine lattice count) would revise the count back toward one anchor. Track, do not harden.

**Flag 4 — String-update task must not silently lapse.** If Item B is adopted but the "Zero Free Parameters" headers are left standing, the public-facing claim (calculator, Paper VII) becomes inconsistent with the ledger. The update is out of body-fold scope but must be queued.

**Flag 5 — Merger must not become an excuse.** Item C correctly merges three gates; it must not be read as "therefore §2.64 is solved." It is the opposite: §2.64 is *not* independently solvable. The merger reallocates effort to the one real chokepoint (I1–I3), which is frozen.

---

## 7. Fold instructions

Append-only. No prior body content modified. On fold:
1. **Item A** → R2 annotation on §2.50.A and §2.64: r_eff form identified as a logarithmic vortex self-energy via the digamma/harmonic-sum identity; import status and discrete-sum derivation explicitly retained as open.
2. **Item B** → status note (Preamble-adjacent or §2.64 tail): parameter count restated as two anchors (m_e, ξ_vac); structural no-address search recorded; calculator/Paper VII string update queued as separate task.
3. **Item C** → R2 cross-cutting note extending the V4.34 §2.52-Open-3 ↔ §2.53 common-chokepoint finding to include §2.64 under the I1–I3 import; M.BRIDGE instance recorded; §2.52 freeze explicitly preserved.

The five audit flags above are part of this entry and travel with it.

---

*Filed under Audit Mode for staging. Append-only. No prior content modified. Fold author assigns canonical version.*
