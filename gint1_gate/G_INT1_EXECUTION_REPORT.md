# Gate G-INT1 — Execution Report

**Date:** 2026-06-23 · **Pre-registration:** `G_INT1_EXECUTION_PREREGISTRATION.md`
(V4.46 CANONICAL basis) · **Instrument:** the rebuilt G-ζ1 soft-core GP/BdG core
(`gz1_core.py`, g=22/R=1/ρ₀=1, not retuned) + `octonion_fano.py` (structural).
Eddington-guarded: no ledger value loaded; λ symbolic; full spectrum reported.

## VERDICT: **STRUCTURAL-ONLY** (R1 structural + M.BRIDGE strengthened)

The registered, a-priori-expected arm. The internal octonion sector carries a
**gapped, Fano-selective fluctuation channel**, but **every dynamical magnitude is
class-(b)** (λ-dependent, μ-drifting) — **no geometry-protected pure number**. The
breach arm (GAPPED-SCALE-FREE) does **not** fire. **λ is named as the located second
import** for the §2.53/§2.64 dynamical bridge.

## Results vs the pre-registered plan

| step | result |
|---|---|
| 1. GP crystal (big box, seed 7) | μ=55.21, k_c=5.04, **ψ₆=0.759 ≫ ψ₄=0.117** (p6m hexagonal) ✓ |
| 1b. primitive cell, a* by energy-min | a*=1.45, μ_cell=55.87 (consistent with the canonical MV-G1 row) |
| 2. two-body internal control | **GAPLESS at Γ** — ψ₀ is the *exact* internal zero mode (theorem below); lowest L_⊥ eig ≈ −7×10⁻⁴ ✓ (registered prediction; a gap here would have been a bug) |
| 3. Fano-line core {e₁,e₂,e₄} | oriented term **lifts** internal modes: 2 chiral splits, magnitude √3·λκ |
| 4. non-line core {e₁,e₂,e₃} | oriented coupling **‖M‖ = 0**, no mode lifted → **S_Fano = SELECTIVE** ✓ |
| 5. scale test | gap ∝ λ (→0 at λ=0) and drifts with μ-scale → **class-(b)**; only λ/μ-independent quantity is the structural split factor √3 (a representation number) |
| limit checks | (a) λ→0 recovers the gapless control ✓; (b) non-line core inert ✓ |

## The two-body gapless control is a theorem, not just a measurement

L_⊥ = −½∇² + (U*ρ − μ). The GP stationarity condition *is* −½∇²ψ₀ + (U*ρ)ψ₀ = μψ₀,
i.e. **L_⊥ψ₀ = 0**: the GP ground state is the exact internal zero mode (rotating ψ₀
into an imaginary direction costs nothing at two-body order — the accidental O(8)
flatness). Verified numerically: residual ‖L_⊥ψ₀‖/(μ‖ψ₀‖) ≈ 2×10⁻³ (relax-limited) and
the lowest plane-wave eigenvalue ≈ 0. No framework content can appear at two-body order
in the internal sector (consistent with §3.4.4).

## The structural results are symmetry-determined (R1, λ-independent)

- **S_Fano selective** is a property of the octonion structure constants φ_abc, which are
  supported **exactly on the seven Fano lines** (`octonion_fano.py`: support = lines,
  each point on 3 lines). The oriented term's coherent self-coupling on a winding triple
  T is φ_abc with a,b,c ∈ T — nonzero **iff T is a line**. {e₁,e₂,e₄} is a line (active);
  {e₁,e₂,e₃} is not (φ=0, inert). This is a yes/no fact, not a magnitude.
- **Multiplet 1 ⊕ 3 ⊕ 3̄:** F₂₁ = ℤ/7⋊ℤ/3 acts on the seven imaginary units as
  pure-permutation octonion automorphisms (⊂ G₂; verified order 21, element orders
  {1:1, 3:14, 7:6}). The 7 decomposes as **1 ⊕ 3 ⊕ 3̄** (character: rank-3 transitive
  action ⇒ one trivial + two conjugate 3-dim irreps). *This is standard G₂/F₂₁
  representation theory — used to classify the channel, not claimed as new.*

These extend the §3.4.4/§3.4.5 selection-rule ladder **from the static linking charge
Q_φ to the dynamical fluctuation spectrum** — the gate's R1 structural contribution.

## Why the breach fails (class-(b), per M.REL axes)

The internal gap magnitude is λ·κ·(structural factor), κ = core overlap. *Scale:* κ
drifts under μ-rescaling (core size is metric-set) → not scale-invariant. *Coupling:* ∝λ,
vanishes at λ=0. The only λ/μ-independent quantity is the **structural split factor √3**,
which is a representation number (the ‖imag-eigenvalue‖ of the 3×3 antisymmetric φ-block
on a line), **not a dynamical magnitude** — it is the same kind of object as the
multiplet content, already banked as R1 structural. There is no λ-canceling dimensionless
*dynamical* quantity. So the internal channel, like the G-ζ1 density channel, carries no
import-free dynamical number.

## Honest scope (what was and was not computed)

- **Executed in full:** the GP crystal reproduction (step 1) and the two-body internal
  gapless control (step 2, exact + numeric).
- **Symmetry-determined + representatively demonstrated:** S_Fano selectivity and the
  multiplet content (steps 3–4) follow from the octonion/F₂₁ structure (rigorous) and are
  shown on the oriented-term-induced internal coupling with a **representative** core
  overlap κ. The **fully spatially-resolved, relaxed-N=160, 7-component defect-core BdG
  eigenproblem is NOT performed here.** The structural verdicts (S_Fano, 1⊕3⊕3̄) are
  **profile-independent** (symmetry-fixed, λ-independent — exactly the registered basis
  for their being R1); only the gap *magnitudes* depend on the profile, and those are
  class-(b) regardless. The per-core spectrum shows a line-triplet lifted (1 inert + 2
  chiral); the global 1⊕3⊕3̄ assignment is the F₂₁ group-theory result, not read off a
  single-core spectrum.

## What this settles / does not settle

- **Settles (R1 structural):** the §3.4.4 Fano selection rule extends to the dynamical
  internal spectrum (S_Fano selective; 1⊕3⊕3̄). M.BRIDGE strengthened: the dynamical
  internal bridge **requires** the λ import, now concretely named for §2.53/§2.64.
- **Does not settle:** any import-free dynamical number — none exists in this channel
  (breach arm negative). The internal gap is a real channel but its scale is λ-set.
- **Freeze:** §2.52 Open 3 untouched and frozen throughout; no numeric target loaded.
  M.CW/M.REL/M.2π respected (λ never tuned; magnitudes per-axis-classed; no 2π conflation).

## Proposed ledger rows (auditor fold-in; canonical V4.46 not in this repo)
> **G-INT1 / structural** | 2026-06-23 | **R1** | internal octonion sector: S_Fano
> selective in the *dynamical* spectrum; multiplet 1⊕3⊕3̄ under F₂₁; two-body gapless
> (ψ₀ = exact zero mode). Extends §3.4.4/§3.4.5 ladder to fluctuations. | not body.
> **G-INT1 / dynamical** | 2026-06-23 | **STRUCTURAL-ONLY (no R2 breach)** | every
> internal magnitude class-(b) (∝λ, μ-drifting); no geometry-protected pure number;
> **λ named as the second import** for §2.53/§2.64. | not body.

*Files: `octonion_fano.py`, `gint1_execute.py`, `gint1_verdict.json`, this report,
`G_INT1_EXECUTION_PREREGISTRATION.md`; MANIFEST.md5 alongside.*
