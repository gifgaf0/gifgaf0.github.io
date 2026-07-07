# G-κ1 — CC HANDOFF: GO for CKS-Exact Q2 (+ conditional C[K_roton])

**Date:** July 5, 2026. **Authorization:** author-relayed GO for the task CC offered
(`db5555d` §"If you want, I'll take the CKS-exact Q2 next"). Fold is HELD until this lands.
This memo is self-contained on conventions; the pipeline scripts referenced are
`gk1_q1b_core_parameter.py` and `gk1_q2_borromean_bound.py` (already in CC's hands).

---

## Task 1 (primary): CKS-exact Q2 — the tight-Borromean tension distribution

**Geometry.** Encode the tight Borromean configuration from Cantarella–Kusner–Sullivan,
*Criticality for the Gehring Link Problem*, arXiv:math/0402212, §10 (the pyritohedral
configuration: each component planar, piecewise circular arcs; fetch the paper for the
exact piecewise data). Honesty note to carry in the output: CKS solve the **Gehring**
problem; canon's L_B = 60.194 sits in the **ropelength** Ashton interval [58.006, 62.0]
whose floor 58.006 is the CKS number. Encode the CKS critical configuration and state
plainly that it is the Gehring-critical representative; if a ropelength-ideal numerical
tight shape is also encodable cheaply, run both — the comparison object is the
curvature/contact distribution, not the last digit of L.

**Pipeline (unchanged — comparability is the point).** Exactly the first-leg pipeline:
1. Sample the strands; κ(s) (analytic per arc — piecewise-circular makes this exact);
   arclength elements; nearest-other-strand distance d(s).
2. Thickness τ = min(1/κ_max, d_inter/2, genuine self/2) — use the *corrected*
   self-distance treatment (genuinely-opposite arcs only; the first leg's in-file note
   documents the vertex-flank bug and fix).
3. Scale to tube radius = ξ = τ; compute ξκ(s), d(s)/ξ, L/ξ.
4. T(s) = ln(max(min(c₁/ξκ, c₂·d), 2)) + C, with **C = 0.3810** (GP handshake value —
   already two-leg verified; keep it fixed here so the ONLY change from the first leg is
   the geometry).
5. Report the identical stat block: τ and its limiting constraint; ξκ range and spread;
   near-cusp fraction (ξκ > 0.5); the full (c₁, c₂) ∈ {4,8,16}×{0.5,1,2} sensitivity
   table; headline (8,1): T̄, dispersion, range, δ vs the tight-unknot reference
   T_ref = ln(c₁) + C.

**Pre-stated expectations (lightweight pre-registration — state before running, report
against):** (i) internal dispersion SHRINKS vs the golden-ellipse stand-in (~8–13%) —
tightness equalizes constraints; (ii) the screening shift vs the unknot PERSISTS at tens
of % (it is a topology-class effect, not a shape accident); (iii) the near-cusp fraction
likely GROWS (tight = curvature-active on more arclength). Deviations from these
expectations are findings, not failures.

## Task 2 (conditional, if tractable): C[K_roton] against the locked thresholds

**Convention handshake is mandatory:** the solver must first reproduce **C_GP = 0.3810**
under the first-leg definition — C = lim[e(R)/2π − ln R], e(R) = ∫[(f′)² + f²/r² +
**½**(1−f²)²] r dr, profile equation f″ + f′/r − f/r² + (1−f²)f = 0 — before any nonlocal
evaluation. Numbers in any other convention are incomparable to the thresholds (the
0.879 episode is the cautionary precedent, by CC's own correction).

**Kernel honesty:** canon's class-(b) roton kernel is an import whose functional form is
not uniquely pinned (G-C1: ξ/a drifts as 1/√(Uρ) — a free knob). Therefore do NOT invent
"the" SQT kernel. Evaluate C over **representative roton-bearing nonlocal kernels of the
Berloff–Roberts class** (their helium-tuned forms are the precedent in print) and report
the RANGE. The verdict question, pre-locked (July 5, BEFORE any such value existed):
does any admissible member approach **C ≳ 5.3** (dispersion route) or **C ≳ 32**
(cross-class route)? Expected: O(1) across the class → route (b) closed for the nonlocal
class too, upgrading "strongly disfavored (R2)" toward closed. If any member lands high,
that is a major finding — report, don't suppress.

## Discipline block

Eddington: the 0.03 budget and the 5.3/32 thresholds are comparison values only — nothing
tuned toward them. No mass values consulted anywhere. Register: Q2-CKS output is the
second leg of a two-leg numeric; C[K_roton] is an evaluation of the existing class-(b)
import, not a new import either way. §2.52 untouched. On completion: return the stat
block + scripts + commit hash; the chat side audits, then executes the single V4.52 fold
carrying the full hybrid verdict (D1=(a) two-leg; exponent sealed per the §2.14 reading;
δ in the E_hydro ledger; the E_hydro↔mass coupling as the located import; route (b)
dispositioned at whatever register the results support).
