# G-κ1 — EXECUTION PRE-REGISTRATION

**Gate:** G-κ1 (mass-budget **channel (iii)** parameterization — curvature-coupled core
dilation in the tight-knot limit).
**Registered:** V4.51 (with the M.ONT declaration whose mass clause names this channel).
**Status:** PRE-REGISTERED, NOT EXECUTED. Written before any computation.
**Mode:** Audit. **Eddington watch: ACTIVE.** **Register ceiling:** R2-conditional on the
I1–I3 substrate ticket + the class-(b) roton kernel (G-C1/V4.48) — the same conditionality
class as G-ζ1/G-INT1/G-C1. **Two-leg required** for any load-bearing numeric result.

---

## Why this gate exists (the threat it answers)

The M.ONT mass clause makes filament-core mass = ideal ropelength at **uniform** thickness
r_eff, leading order. Channel (iii) is the one correction that is **not parametrically
suppressed**: tight knots have curvature κ ~ 1/r_eff on exactly the contact arcs that
dominate the configuration, and local strain dilates the core there, converting uniform
ropelength into a **weighted** ropelength. Because curvature distributions are
knot-shape-dependent, this channel can shift mass **ratios** — a direct threat to the
zero-parameter mass claims. The gate's job: determine whether the coupling is **entirely
governed by already-imported structure** (the roton kernel), and **bound** its magnitude.

## The question (two parts, separable verdicts)

**Q1 (import test — the structural question).** From the instantiated §3.4 substrate action
(GP + the declared kernel), derive the static core-radius response to filament curvature:

    r_eff(s) = ξ · (1 + f(ξκ(s)) + …),   f(x) = c₂x² + c₄x⁴ + …  (parity: f even in κ)

Is the leading coefficient **c₂ a functional of the declared roton kernel alone** (the same
class-(b) object that set ξ_vac = 100φ), or does it require new data (a new dimensionless
import)? Note the expected parity: a straight filament (κ=0) is the reference; the sign of κ
is orientation, so f should be even — the pre-registered form starts at (ξκ)². If the
derivation produces an odd term, that itself is a finding (flags a chirality coupling; report,
do not suppress).

**Q2 (magnitude bound — the physical question).** For the tight Borromean configuration
(CKS criticality solution — piecewise-circular/straight geometry, published), compute the
curvature distribution κ(s), combine with the Q1 dilation law, and bound the fractional mass
correction:

    δ ≡ ΔE/E = [∫ (1 + f(ξκ(s))) ds − L] / L   (weighted vs uniform ropelength)

against the ~3% ratio-agreement budget the clean monomial currently enjoys.

## Decision scalars (locked)

- **D1 (import verdict):** trichotomy — **(a) FORCED/no-new-import** (c₂ = an explicit
  functional of the declared kernel; channel (iii) is parameterized by existing imports; the
  zero-NEW-parameter property of the mass sector survives); **(b) NEW-IMPORT** (c₂ depends on
  kernel details or substrate data not previously declared — name the import per M.BRIDGE;
  the mass sector acquires one more located knob); **(c) NULL/ill-posed** (the static
  curvature-response problem is not well-posed at this order — report why).
- **D2 (magnitude):** δ for the tight Borromean configuration, reported with the kernel-
  uncertainty band that D1's verdict implies; decision threshold δ vs 0.03 (the ratio budget).
- **Auxiliary (reported, not decisional):** the exponent check — leading power of f (expected
  2); whether δ is dominated by the contact arcs (expected) or distributed.

## Falsification / outcome arms (locked; ARM labels per standing convention)

- **ARM-R (FORCED + small):** D1=(a) and δ < 0.03. Channel (iii) is roton-kernel-governed
  with no new import, and quantitatively inside the ratio budget — the strongest outcome; the
  ~3% agreements survive as predictions.
- **ARM-N (FORCED + large):** D1=(a) and δ ≥ 0.03. No new import, but the correction is
  material — the clean ratios then require either cancellation across knot types (computable:
  compare δ across the spectrum's configurations) or revision of the leading-order claim.
  Informative, not a defeat; fold as a finding.
- **ARM-D (NEW-IMPORT):** D1=(b). The import is named and located (M.BRIDGE strengthened
  again); channel (iii) carries one declared knob; δ is then reported conditional on it.
- **ARM-X (NULL):** D1=(c). Report the obstruction; the channel remains named-but-unbounded.

No arm retracts the M.ONT declaration or any filed result; the declaration named this channel
precisely so that any arm lands as annotation, not retraction.

## Declared imports (up front)

- The **I1–I3 substrate ticket** (the instantiated §3.4 action) — same conditionality as
  G-ζ1/G-INT1/G-C1; this is a dynamical/metric computation, exactly the class M.CW reserves
  for the substrate action, and its verdict is conditional on that instantiation.
- The **class-(b) roton kernel** (G-C1/V4.48) — the object under test is whether c₂ is *its*
  functional; the kernel itself remains an import (this gate cannot and does not convert it).
- The **CKS tight-Borromean geometry** (published criticality solution) as the reference
  configuration for Q2 — prior art, the V4.50 citation.
- **No observable target enters the construction**: the 0.03 threshold is a *comparison*
  bound (the existing ratio-agreement budget), quarantined to the final D2 comparison line;
  no mass value is consulted during the derivation (Eddington guard).

## Execution plan (order mandatory)

1. **Literature-Search-First (mandatory, cross-dialect, BEFORE any compute).** Curved-vortex
   core structure is studied GP territory. Search at minimum: GP/BEC vortex-ring core
   deformation and energy corrections in ξ/R; local-induction-approximation corrections;
   "core deformation" / "vortex core dilation" / curvature corrections to the vortex line
   tension; Kelvin-wave zero-point literature (channel (ii) adjacency); and the
   ideal-knot/tight-link side (curvature-active arcs, contact-force distributions — CKS and
   successors). Cross-dialect risk: the GP literature says "vortex line energy / core
   parameter," the knot literature says "thickness / reach"; the same object under two
   vocabularies. If the dilation law already exists in the literature, Q1 becomes a
   prior-art closure (the OP-PSL.3/V4.45/V4.50 pattern) and compute is spent only on Q2.
2. **Q1 derivation** (chat-side first leg): static GP perturbation about a curved filament;
   extract c₂ as a kernel functional or locate the failure. CC second leg from scratch.
3. **Q2 bound**: CKS geometry κ(s) + the Q1 law → δ. Two-leg on the numeric.
4. Fold per arm.

## What this gate does NOT do

Does not derive channel (i) (envelope energy — separate physics), channel (ii) (Kelvin
zero-point — flagged adjacency only), or channel (iv) (discreteness — already bounded
~0.6% by ξ_vac/a). Does not touch the μ_n line, G-2a-*, §2.50, or Assignment I/II. Does not
convert the class-(b) kernel import. §2.52 Open 3 untouched.

## Provenance plan

`G_K1_EXECUTION_PREREGISTRATION.md` (this file, written before compute); execution scripts
to be deposited on execution (`gk1_q1_dilation_law.py`, `gk1_q2_cks_bound.py` — names
reserved); CC second legs; fold script on whichever arm fires.
