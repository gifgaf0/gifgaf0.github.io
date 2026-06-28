# Gate G-INT1 — Execution Report

**Date:** 2026-06-23 · **Pre-registration:** `G_INT1_EXECUTION_PREREGISTRATION.md`
(V4.46 CANONICAL basis) · **Instrument:** the rebuilt G-ζ1 soft-core GP/BdG core
(`gz1_core.py`, g=22/R=1/ρ₀=1, not retuned) + `octonion_fano.py` (structural).
Eddington-guarded: no ledger value loaded; λ symbolic; full spectrum reported.

## VERDICT: **STRUCTURAL-ONLY** (R1 structural + M.BRIDGE strengthened)

The registered, a-priori-expected arm. The internal octonion sector carries a
**gapped, Fano-selective fluctuation channel**, but **every dynamical magnitude is
class-(b)** (λ-dependent, μ-drifting) — **no geometry-protected pure number**. The
breach arm (GAPPED-SCALE-FREE) does **not** fire.

**λ is the located import for the INTERNAL channel** (the oriented-term coupling). It is
**not** §2.53/§2.64's import — those are *density-sector* quantities (§2.53 fold-convexity
sign; §2.64 C = ξ_vac/a healing length) whose import is the **density-sector roton /
healing-length profile**. **That density import is still OPEN, not examined:** G-ζ1
*used* the roton profile (took it as the I1–I3 ticket and computed the density spectrum) —
it did **not** derive it; and **angle-3** (the ξ_vac/a-forcing test — whether p6m
crystallization pins C to a pure number) **is UNEXECUTED**. So the density-sector import
remains the **live frontier**. G-INT1's contribution to the chokepoint cluster is
therefore narrow and real: it **eliminates the internal channel as a breach route** and
strengthens M.BRIDGE — two channels examined (density spectrum via G-ζ1, internal via
G-INT1), **two distinct imports** (the density roton/healing-length profile, still open;
λ, located here). This entry must not launder "serves §2.53/§2.64" into "resolves their
import," nor "G-ζ1 used the profile" into "the density import is examined." *(Scope
corrections adopted from the SQT second-leg audit + clearance, 2026-06-23.)*

## Independent second-leg verification (incorporated)
The three R1 structural pillars are confirmed by a from-scratch independent build
(`verify_gint1_secondleg.py`, SQT, not using `gz1_core.py`): φ on exactly 7 of 35 triples;
F₂₁ order 21, orders {1:1,3:14,7:6}, character ⟨χ,triv⟩=1, ⟨χ,χ⟩=3, remainder-norm²=2 ⇒
**1⊕3⊕3̄** (two distinct mult-1 irreps, dims 3+3 from 7−1); line {1,2,4} eigenstructure
**{0, ±i√3}**, non-line {1,2,3} the zero matrix. Two-method confirmation for the fold
record (this report's `gint1_execute.py` is the first leg).

## Results vs the pre-registered plan

| step | result |
|---|---|
| 1. GP crystal (big box, seed 7) | μ=55.21, k_c=5.04, **ψ₆=0.759 ≫ ψ₄=0.117** (p6m hexagonal) ✓ |
| 1b. primitive cell, a* by energy-min | a*=1.45, μ_cell=55.87 (consistent with the canonical MV-G1 row) |
| 2. two-body internal control | **GAPLESS at Γ** — ψ₀ is the *exact* internal zero mode (theorem below); lowest L_⊥ eig ≈ −7×10⁻⁴ ✓ (registered prediction; a gap here would have been a bug) |
| 3. Fano-line core {e₁,e₂,e₄} | oriented term **lifts** internal modes: eigenstructure {0, ±iσ} → **exactly 2 chiral modes + 1 unaffected** (count & ± chirality R1, see below), magnitude σ = ‖φ\|_line‖·λκ |
| 4. non-line core {e₁,e₂,e₃} | oriented coupling **‖M‖ = 0**, no mode lifted → **S_Fano = SELECTIVE** ✓ |
| 5. scale test | gap σ ∝ λ (→0 at λ=0) and drifts with μ-scale → **class-(b)**; the only λ/μ-independent quantity is the prefactor **‖φ\|_line‖ = √3** (the norm of φ on a Fano line — *not* a representation number, *not* the p6m lattice √3) |
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

- **2-chiral count + ± chirality (R1, profile-independent).** On a Fano line φ is
  *totally antisymmetric* over the 3 indices, so the induced internal coupling is a 3×3
  antisymmetric matrix; *every* such matrix has eigenstructure {0, ±iσ}. Hence a line core
  lifts **exactly two** internal modes in a **chiral ± pair** with one unaffected — a count
  and a chirality that are forced by antisymmetry, **independent of λ and of the core
  profile**. Only the magnitude σ depends on profile/λ. (Upgraded to R1 per the SQT audit;
  earlier draft hedged the count as "representative" — that was too conservative.)

These extend the §3.4.4/§3.4.5 selection-rule ladder **from the static linking charge
Q_φ to the dynamical fluctuation spectrum** — the gate's R1 structural contribution.

**See-also (cross-ref, not a new claim):** the 3/3̄ split *is* the QR/QNR split — the
i√7 appearing in the F₂₁ character is the Gauss-sum of 7th roots over the
quadratic-residue vs non-residue cosets — threading to §2.75/§2.76 and the §3.4.6
sign(φ) ↔ QR/QNR map. Worth a canonical cross-reference; not asserted as new here.

## Why the breach fails (class-(b), per M.REL axes)

The internal gap magnitude is σ = λ·κ·‖φ|_line‖, κ = core overlap. *Scale:* κ drifts
under μ-rescaling (core size is metric-set) → not scale-invariant. *Coupling:* ∝λ,
vanishes at λ=0. The only λ/μ-independent quantity is **‖φ|_line‖ = √3** — the norm of
the octonion structure constants on a Fano line (√(1²+1²+1²)). This is a *structural
prefactor on a class-(b) magnitude*, **not** a derived dynamical number (and **not** a
representation dimension — those are the integers 1,3,3 — nor the p6m lattice √3). There
is no λ-canceling dimensionless *dynamical* quantity. So the internal channel, like the
G-ζ1 density channel, carries no import-free dynamical number.

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
- **The full relaxed-core 7-component BdG is declined as a prerequisite** (SQT audit):
  it would only pin σ = ‖φ|_line‖·λ·(profile integral) — a **class-(b), import-classified
  magnitude**, not a derivation. Spending the heavy N=160 solve to fix an
  import-classified number is the M.CW "not worth pursuing" pattern (the §2.64 "100"
  again). Filed as **optional, low-priority R2-firming**, *not* load-bearing. The
  error-prone oriented-second-variation only touches σ; the 2-chiral count is fixed by
  φ's antisymmetry, which is rock-solid. **Future trigger:** if Gate-2a (spin–isospin
  locking) needs the explicit chiral-mode structure on the core, σ feeds in there — flag
  it for that, not now.

## What this settles / does not settle

- **Settles (R1 structural):** the §3.4.4 Fano selection rule extends to the dynamical
  internal spectrum (S_Fano selective; 1⊕3⊕3̄ classification; 2-chiral count + chirality).
  M.BRIDGE strengthened: the dynamical **internal** bridge requires the λ import, now
  concretely named — and the internal channel is **eliminated as a breach route**.
- **Does not settle:** any import-free dynamical number — none exists in this channel
  (breach arm negative); the internal gap is real but its scale is λ-set. **Nor does it
  resolve §2.53/§2.64's import** — those are density-sector; their import (the roton /
  healing-length profile) is **still open**, with **angle-3 unexecuted** and G-ζ1 having
  only *used* (not derived) the profile. That density import is the **live frontier**; λ
  is a *distinct* second import, not it.
- **Freeze:** §2.52 Open 3 untouched and frozen throughout; no numeric target loaded.
  M.CW/M.REL/M.2π respected (λ never tuned; magnitudes per-axis-classed; no 2π conflation).

## Proposed ledger rows (auditor fold-in; canonical V4.46 not in this repo)
> **G-INT1 / structural** | 2026-06-23 | **R1** | internal octonion sector: S_Fano
> selective in the *dynamical* spectrum; multiplet 1⊕3⊕3̄ under F₂₁; **2-chiral count +
> ± chirality** (forced by φ antisymmetry, profile-independent); two-body gapless (ψ₀ =
> exact zero mode). Extends §3.4.4/§3.4.5 ladder to fluctuations. Two-leg verified
> (gint1_execute + independent verify_gint1_secondleg). See-also: 3/3̄ = QR/QNR
> (§2.75/§2.76, §3.4.6). | not body.
> **G-INT1 / dynamical** | 2026-06-23 | **STRUCTURAL-ONLY (no R2 breach)** | every
> internal magnitude class-(b) (σ = ‖φ|_line‖·λ·profile, ∝λ, μ-drifting); no
> geometry-protected pure number; **λ = the INTERNAL-channel import** (NOT §2.53/§2.64's,
> which is the density roton profile). Internal channel eliminated as a breach route.
> Full relaxed-core BdG = optional low-priority R2-firming (trigger: Gate-2a). | not body.

*Files: `octonion_fano.py`, `gint1_execute.py`, `gint1_verdict.json`, this report,
`G_INT1_EXECUTION_PREREGISTRATION.md`; MANIFEST.md5 alongside.*
