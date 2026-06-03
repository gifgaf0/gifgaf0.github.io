# Ledger Entry — §3.4 — Proof Program (R2 method / R3 program; named R1 gates)
## The Bjerknes Substrate Action: What a Proof Would Require, and the Five Gates That Decide It

**Date:** June 3, 2026
**Register:** R2 (the methodology — what "proof of an action" can mean under M.CW, and the necessity/sufficiency/minimality structure) + R3 (the candidate action itself and the five gate conjectures) + named **R1 promotion targets** per gate.
**Cluster:** Continuum-limit / substrate dynamics (Paper II scope). Companion to the §3.4 Bjerknes-action audit line already open in Part VI.
**Status:** Program of record. **Not a result.** Nothing here is promoted to §2.x. Files the structure a §3.4 proof must take, the single import ticket it may spend, and the five falsifiable gates whose conjunction would constitute the proof.
**Eddington watch:** ACTIVE (high). The central risk — tuning the action to reproduce known targets — is addressed by a mandatory pre-registration step (§3.4.3); read that before §3.4.4.

---

## §3.4.0 — What "proof of an action" can mean (R2, load-bearing framing)

**M.CW forbids the naive reading.** An action carries a metric, a sign, and a
scale — the three quantities the Category Wall states combinatorics cannot
output. Therefore the substrate action **cannot be derived** from the
K₇ / Fano / sedenion combinatorics. Any attempt to do so is itself the M.CW
error and must be caught. "Proving the Bjerknes substrate action" cannot mean
"deriving it from the discrete structure."

**What is provable** is the standard physics statement about any action — a
**necessity + sufficiency + minimality** claim:

> The posited action is the **minimal** local functional **invariant under the
> framework's established symmetry group** (Fano/G₂ multiplication
> automorphisms + the PSL(2,7) action of §1.1) whose **ground state, solitons,
> and excitation modes reproduce the framework's independently-derived T1/T2
> structure**, importing only the field-target space and one scale.

This mirrors how the Standard Model Lagrangian is justified: gauge invariance
fixes the allowed terms, minimality removes the rest, experiment fixes the
couplings. The SQT analog replaces "gauge invariance + experiment" with
"**§1.1 PSL(2,7) / G₂ invariance + the existing §2.x results.**" The proof is a
consistency-and-uniqueness argument, not a derivation from nothing.

**M.BRIDGE context.** This is the one bridge the program has not yet attempted
under a declared ticket. M.BRIDGE records that every prior observable bridge
required an import it could not name. This program's discipline is to name the
import up front (§3.4.1) and keep it minimal; absent that, §3.4 is an M.CW
crossing without a ticket and will not survive audit.

---

## §3.4.1 — The import ticket (Prior Address Standard, declared up front)

Exactly three imports are permitted. Spending more voids the ticket; deriving
any of the §3.4.4 outputs from a *fourth* import is an audit failure.

| Import | What is posited | Why it is an import (M.CW class) |
|---|---|---|
| **I1 — Field target** | ψ : spacetime → 𝔸, with 𝔸 the CD level the framework already uses (𝕆 with the K₇ structure, or 𝕊) | Choice of target space / signature; not a combinatorial output |
| **I2 — Kinetic form** | First-order-in-time (GP) kinetic term + gradient term | A metric on field space; M.CW metric class |
| **I3 — One scale** | A single dimensionful constant (sets m₀) | A scale; M.CW scale class — already the framework's sole calibration (§2.14, §2.50.A) |

Everything in §3.4.4 must be **derived**, not imported. The interaction
*couplings* are fixed by symmetry (form, §3.4.3) up to a small finite set, then
by matching to existing T1/T2 results — never by matching to a target the gate
is supposed to predict.

---

## §3.4.2 — The candidate action (R3, posited)

A Gross–Pitaevskii / Bjerknes superfluid functional for the order parameter ψ
(ρ ≡ |ψ|²):

$$S[\psi]=\int dt\,d^3x\;\Big[\tfrac{i\hbar}{2}\big(\psi^\dagger\partial_t\psi-\text{c.c.}\big)-\tfrac{\hbar^2}{2m}\,|\nabla\psi|^2-V(\psi)\Big]-\tfrac12\!\int dt\,d^3x\,d^3x'\;\rho(x)\,K(x-x')\,\rho(x')$$

with local potential V = −μρ + (g/2)ρ² and a **non-local kernel K** chosen to
give a roton-minimum dispersion (the ingredient that crystallizes the vacuum
rather than leaving it uniform).

- **Particles** = knotted vortex solitons (phase defects of ψ; zeros with
  winding).
- **Interaction** = the **secondary Bjerknes force** between pulsating cores:
  the literal acoustic radiation force, ∝ 1/d², **attractive in phase,
  repulsive out of phase**. The phase that sets the sign is the §2.17 Lemma-θ
  phase-lock variable.

The candidate is R3 (an import) until §3.4.3 fixes its allowed-term content by
symmetry and §3.4.4 matches the couplings.

---

## §3.4.3 — The linchpin: symmetry-first term derivation (R2 → R1 gate)

**This step is what separates a proof from an Eddington fit. It must be
executed and pre-registered before any computation in §3.4.4.**

1. Fix the field target 𝔸 (import I1).
2. **Enumerate every local invariant** of degree ≤ 4 in ψ and ≤ 2 in ∂ under the
   framework's established symmetry group (Fano/G₂ multiplication automorphisms +
   §1.1 PSL(2,7)). M.CW guarantees this yields admissible **forms**, never
   coefficients.
3. **Minimality**: retain the lowest-dimension representative of each allowed
   type. The surviving functional should carry only a small finite set of
   couplings.

**R1 promotion target (G0):** the symmetry-allowed term list is computed
explicitly and shown to be (near-)unique up to a stated finite coupling set,
**recorded before §3.4.4 is run.** If the list is not essentially unique, that
non-uniqueness is the finding and is reported as such.

**Pre-registration clause (binding).** The term list of G0 is written to the
ledger *before* the ground state (G1) is computed. Adjusting K, V, or 𝔸 after
seeing that p6m / ζ / a mass is needed is the Eddington Maneuver and voids the
program.

---

## §3.4.4 — The five structural gates (each R3 now; R1/R2 targets and falsifiers named)

Each gate is a derivation **from** the §3.4.3-fixed action **of** an
already-established framework structure. Each therefore has an informative null.

| Gate | Derive (R-target) | Closes / connects | **Falsified if** |
|---|---|---|---|
| **G1 — Vacuum** | minimizer of S is the **p6m** lattice; energy density carries the packing tax **ζ = 1 − π/√12 ≈ 0.09310** | §2.26, §2.24 (frustration constant T) | minimizer is uniform / square / any non-hexagonal lattice |
| **G2 — Soliton** | stable finite-energy solitons are **knotted vortex tori**; the simplest closed one is the **Császár torus** (7 vertices, valence 6, χ = 0); Rule 17 (unknot ↔ Clifford torus) is the profile; the gradient energy on the embedding is the **§2.7 ε-per-edge** | §2.7, the knot→particle map (§2.1) | lowest soliton is a bare unknot ring with no 7-vertex / K₇ structure |
| **G3 — Seam fold** | surface-energy minimization at a pentagon seam forces the **36° → 18° bilateral split** | **§2.45-NGA promotion gate** (the *sole* surviving prior address for cos 18° after the seven-circles enrichment was retired, §3.07) | the seam minimizer does not bisect, or bisects at an angle ≠ 18° |
| **G4 — Pulsation** | the soliton breathing mode (the Bjerknes pulsation) yields the mass exponent **2π/Φ** and a pulsation amplitude that **resolves the 0.0948-vs-ζ=0.0931 gap** of §2.52 | §2.52 Open 3, **ζ-tax gates 1–4**, §2.50 (2π without electron-mass circularity), §2.14 | the breathing amplitude is unrelated to ζ and does not explain the §2.52 gap |
| **G5 — Confinement** | three phase-locked pulsating rings are **mutually Bjerknes-bound only as a triple** (pairwise unbound) — a Borromean configuration | **§2.15** (supplies the physical confinement mechanism the baryon entry currently lacks) | the secondary Bjerknes force gives pairwise binding, not a genuinely 3-body Borromean bound state |

**G5 is the program's strongest unforced test.** Borromean topology
(pairwise-free, triple-bound) is exactly the qualitative signature of three
sources whose phase-locked secondary Bjerknes forces cancel pairwise but bind
collectively. If S delivers that *without being asked*, it is strong evidence;
the attractive/repulsive sign is set by the §2.17 Lemma-θ phase, tying G5 to an
existing T2 result rather than a new parameter.

**A completed proof = G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5**, with the §3.4.1 ticket
unspent beyond I1–I3.

---

## §3.4.5 — Imported-vs-derived ledger (the M.CW ticket accounting)

| | Item |
|---|---|
| **Imported (I1–I3 only)** | field target 𝔸; GP kinetic form; one scale (m₀) |
| **Derived (must be)** | the symmetry-allowed term list (G0); p6m + ζ (G1); Császár soliton + ε-per-edge (G2); bilateral fold + cos 18° (G3); pulsation + 2π/Φ (G4); Borromean confinement (G5) |

Three imports, six structural outputs. That ratio is the ticket M.BRIDGE says no
prior bridge has presented; presenting it is the point of the program.

---

## §3.4.6 — Eddington / Vocabulary discipline (active watch, three rules)

1. **Pre-register G0 before G1** (§3.4.3). Tuning the action after seeing the
   target is the canonical Eddington Maneuver.
2. **Every gate's null is a result.** A G1 failure (no p6m ground state) retires
   the substrate hypothesis cleanly and hands the decision to M.BRIDGE — that is
   information the program wants, not a failure to conceal.
3. **No vocabulary drift.** "Bjerknes force" must remain the literal secondary
   acoustic radiation force with its known 1/d² law and phase-dependent sign. The
   moment it becomes "topological Bjerknes tension" carrying new free parameters,
   it fails Vocabulary Substitution and is struck.

---

## §3.4.7 — The bounded entry point (MV-G1; days, not months)

The full program (G0–G5) is multi-paper. Its decisive **cheap** entry point:

> **MV-G1.** Take the §3.4.3 symmetry-fixed action with a roton kernel, minimize
> S numerically on a 2-D periodic domain, and check *only* (i) whether the
> ground state is hexagonal (p6m) and (ii) whether **ζ = 1 − π/√12** appears in
> its energy density.

- **Pass** → first derived rung; fund G2–G5.
- **Fail** → the substrate picture is in doubt for the price of one
  minimization; report the null.

Because §3.4 silently gates §2.45-NGA, §2.50, §2.52, the ζ-tax cluster, and
(post-§3.07) the **sole** prior address for cos 18°, MV-G1 is the
**highest-leverage single computation in the physics ledger**: one run converts
§3.4 from an open narrative into a measured gate.

---

## §3.4.8 — What this entry does NOT claim

- It does **not** assert the action is correct, that any gate will pass, or that
  a substrate exists. It states the structure a proof must have and the tests
  that decide it.
- It does **not** derive the action from combinatorics (M.CW forbids it); the
  action is declared an import (I1–I3).
- It does **not** weaken any existing result. G1–G5 are *targets*; the §2.x
  structures they aim to reproduce stand on their own current register
  independently of whether §3.4 ever closes.
- It does **not** promote the cos 18° prior address. G3 is the *gate*; §2.45-NGA
  remains at its current register until G3 closes.

---

## §3.4.9 — Relation to existing ledger items

Closes / promotes **if and only if** the corresponding gate passes:
§2.26 + §2.24 (G1) · §2.7 ε-per-edge (G2) · §2.45-NGA bilateral fold and thereby
cos 18° (G3) · §2.50 2π-without-circularity, §2.52 Open 3 pulsation = ζ, §2.14
mass exponent, ζ-tax gates 1–4 (G4) · §2.15 Borromean confinement mechanism (G5).
The L4.5 / §2.64 continuum-fidelity gate is the discretization control under
which G1–G2 must be computed.

Cross-refs: M.CW, M.BRIDGE, Prior Address Standard, Vocabulary Substitution,
§1.1 (symmetry source for G0), §2.17 (Lemma-θ phase sign for G5), Rule 17 (G2
profile), §4.10 (radial soliton-energy landscape, downstream of G2/G4).

---

## §3.4.10 — Proposed Part VI open-task entries

| Task | Status |
|---|---|
| **§3.4-G0** (symmetry-allowed term list; explicit invariant enumeration under Fano/G₂ + §1.1 PSL(2,7); pre-registered before G1) | **Open — gating; R1 target** |
| **§3.4-MV-G1** (2-D roton-GP minimizer: is the ground state p6m and does ζ = 1 − π/√12 appear?) | **Open — bounded first computation; highest leverage** |
| **§3.4-G1** (full vacuum derivation, p6m + ζ) | **Open — R2 target, gated on G0** |
| **§3.4-G2** (Császár-torus soliton + ε-per-edge from gradient energy) | **Open — gated on G1; closes §2.7 if positive** |
| **§3.4-G3** (seam-fold 36°→18°; §2.45-NGA promotion) | **Open — closes the sole cos 18° prior-address gate if positive** |
| **§3.4-G4** (breathing mode → 2π/Φ; pulsation vs ζ, §2.52 gap) | **Open — closes §2.52 Open 3 + ζ-tax gates if positive** |
| **§3.4-G5** (three-ring Borromean Bjerknes binding; §2.17 phase sign) | **Open — supplies §2.15 confinement mechanism if positive** |

---

## §3.4.11 — Fold-in notes

- File under the existing §3.4 Bjerknes-action audit line (Part VI lower-priority
  / Paper II scope); this entry supersedes the bare "audit — Open" placeholder
  with a structured program. Append-only; no §2.x modified.
- Register honesty: the entry is R2 (method) + R3 (program); **only the gate
  *targets* carry R1/R2 labels**, and only G0 is immediately actionable. Do not
  cite any gate as a result.
- The pre-registration clause (§3.4.3) is binding the moment G0 is attempted;
  record the term list in the ledger before running MV-G1.
- Eddington watch travels with every sub-gate until closed.

*Append-only discipline preserved. No prior ledger content modified. June 3, 2026.*
