# G-κ1 — First-Leg Results Memo (Q1b + Q2, chat-side)

**Date:** July 5, 2026
**Status:** FIRST LEG COMPLETE. No arm formally fires until the CC second leg + the two
named stand-in replacements (below). Nothing folded. Scripts:
`gk1_q1b_core_parameter.py`, `gk1_q2_borromean_bound.py` (with one documented in-file
correction: the first run misclassified the vertex flanks of the convex ellipse as
self-contact via a too-small index-exclusion window; corrected to genuinely-opposite arcs;
thickness verdict changed from the artifact value to the correct curvature-limited one).

---

## Q1b — the core parameter is a kernel functional (ARM-R structural component: SECURED)

Solved the vortex-profile ODE from scratch (Newton/Thomas relaxation, residual ~10⁻¹¹,
convergence in R verified at R = 20/40/59) for the local kernel family U′(n) = n^γ:

| kernel | C (core parameter) |
|---|---|
| γ = 1 (GP) | **+0.3810** — literature 0.3809 (ln 1.464, Roberts–Grant / Pitaevskii–Stringari): **verified to 4 digits** |
| γ = 2 | +0.6156 |
| γ = 3 | +0.7273 |

C is fully determined by the kernel, converged, with **no residual freedom** — the
functional dependence C = C[kernel] is demonstrated, not asserted. Combined with LSF
Finding 1 (the law's coefficient and scale are kernel-independent and already-declared),
**the no-new-import structural verdict is secured at first-leg level**: channel (iii)'s
entire kernel-dependence is one computable constant. Remaining for the second leg: evaluate
C for the *declared roton kernel* (nonlocal solve; Berloff–Roberts method, precedent in
print). Until then the numeric C is GP-conditional — inheriting the kernel's class-(b)
status, which is the pre-reg's stated register ceiling, not a new import.

## Q2 — the bound on canon's Borromean representative (stand-in geometry, declared)

Configuration: the golden-ellipse Borromean (canon's §3.4-G2/§3.09 standing
representative; the CKS-tight configuration is the pre-reg's named target and is assigned
to the second leg). Corrected thickness analysis:

- τ = 0.2361 = 1/κ_max = φ⁻³ (ellipse units) — **curvature-limited**, with the vertices
  exactly curvature-active: **ξκ_max = 1.000**. Inter-strand: 0.2814; genuine self: 0.875.
- ξκ(s) ∈ [0.0557 (= φ⁻⁶), 1.000] — a ×17.9 spread. Screening distances d/ξ ∈ [2.38, 4.24
  (= φ³)]. Ropelength L/ξ = 93.8. **Near-cusp (Jones–Roberts) arclength fraction: 11.8%**
  (ξκ > 0.5) — the validity band the LSF amendment required is genuinely occupied.
- Tension field T(s) = ln(min(c₁/ξκ, c₂·d)) + C over the pre-registered sensitivity grid:
  - **Internal dispersion of T along the strand: ~8–13%** (central cutoff choices;
    collapses to ~1% only in the screening-saturated corner c₂ = 0.5).
  - **Cross-configuration shift vs the tight unknot (ξκ = 1 ring): −13% to −66%**,
    headline (c₁=8, c₂=1) **−41%**. Sign robust across the whole grid: the compact tangle
    is *screened* (flow cut off at inter-strand distance 2.4–4.2ξ) while the isolated ring
    is not — a genuinely knot-class-dependent tension.
  - Kernel-robustness note: C enters T *additively*, so the **dispersion and the
    T-differences are kernel-independent**; only the ratio normalization shifts mildly
    with C. The Q2 shape results will survive the roton-kernel evaluation.

## Verdict indication (no arm fired)

**ARM-N-leaning: kernel-governed (no new import) but LARGE.** D1 → (a) at the structural
level (Q1a prior art + Q1b demonstration). D2: both the internal dispersion (~10%) and the
cross-class shift (tens of %) sit far above the 0.03 budget **at this level of treatment**.
Per the pre-reg, ARM-N is informative, not a defeat: it demands the cross-knot cancellation
analysis (compare δ across the spectrum's configurations) or a revision of how the
leading-order claim consumes L — and it retracts nothing (the M.ONT declaration named this
channel precisely so any arm lands as annotation).

## The three gates between this and a fired arm (second-leg spec)

1. **CKS-exact geometry** (replaces the golden-ellipse stand-in). The tight configuration
   plausibly *equalizes* constraints (that is what tight means), so the internal dispersion
   likely shrinks; the screening shift vs the unknot should persist. CC: encode the CKS
   §10 piecewise data; rerun the Q2 pipeline.
2. **Roton-kernel C** (replaces the GP stand-in). Nonlocal profile solve, Berloff–Roberts
   method. Expected to shift T normalization only (additive), not the shape results.
3. **The §2.14-consumption reading** (interpretive, chat-side/author). The exponential-
   amplification flag: if mass consumed L as exp(L_eff/Φr_eff) with L_eff the
   energy-equivalent length, tension shifts of tens of % would be amplified by ~L/(Φξ)
   e-folds — absurdly large, which most plausibly means §2.14's L is the *geometric*
   ropelength and the vortex-energy channel enters differently (or the identification is
   itself the next located import). **This reading must precede any fold** — it determines
   what δ is actually compared against, and it may be the most consequential single item
   this gate has produced.

## Eddington / discipline check

No mass value consulted anywhere in Q1b/Q2; the 0.03 threshold appears only in the verdict
comparison; the stand-ins are declared, not silent; the one computational error (self-
distance window) was caught, documented in-file, and corrected before any interpretation
was drawn from it. §2.52 untouched.
