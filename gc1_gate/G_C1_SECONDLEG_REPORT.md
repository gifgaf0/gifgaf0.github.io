# G-C1 (angle-3) — Independent Second-Leg Verification

**Date:** 2026-06-29 · **Pre-registration:** `G_C1_ANGLE3_EXECUTION_PREREGISTRATION.md`
(SQT, target-quarantined) · **First leg:** `angle3_xivac_forcing_firstleg.py` (SQT) ·
**Second leg:** `gc1_secondleg.py` (this, independent — own 2D FT, own k_min, own sweep;
imports no tool under test; 100φ confined to the final block).

## Result: **CONFIRMS the first leg — IMPORTED / class-(b); the FORCED-MATCH breach does not fire.**

C = ξ_vac/a is **not** forced to a pure number by the triangular geometry. The density-sector
import is located as the roton kernel (the free ξ/a knob). Two legs agree to the digit.

## What the second leg verified (and strengthened)

| claim | first leg (SQT) | second leg (this) | status |
|---|---|---|---|
| 2D FT of soft-disk | 2πUR·J₁(qR)/q | own quadrature vs closed form, max diff **4.7e-10** | ✓ self-checked |
| roton k_min·R (soft-disk) | 5.13 | **5.13562 = j₂,₁ exactly** (first zero of J₂) | ✓ + analytic |
| a/R (soft-disk) | 1.41 | **1.41272** = 4π/(√3·j₂,₁) | ✓ |
| a/R (γ=6 bracket) | 1.51 | 1.5052 | ✓ |
| vs MV-G1 a*=1.4576 | ~3% | soft-disk 3.1%, γ=6 3.3% | ✓ |
| a/R under U,ρ sweep | 0.00% spread | **0.000% — and EXACTLY so, analytically** | ✓ strengthened |
| ξ/a under sweep | 4.0× drift, ∝1/√(Uρ) | **4.0× (0.0213–0.0851), 1/√2 law exact (0.7071)** | ✓ exact match |
| any ratio = 100φ? | no (off 114×) | **no** (a/R off 115×; ξ/a sub-cell) | ✓ |

**The strengthening (why a/R is *forced*, not just flat).** For the soft-disk
V(r)=U·θ(R−r), Ṽ(q) = 2πUR·J₁(qR)/q, and d/dx[J₁(x)/x] = −J₂(x)/x, so the roton minimum
sits **exactly at the first positive zero of J₂**: k_min·R = j₂,₁ = 5.13562…, giving the
closed form **a/R = 4π/(√3·j₂,₁) = 1.41272** — a pure number set by the kernel *shape*. It
is **rigorously** U- and ρ-independent: U is an overall prefactor of Ṽ(q) (cannot move the
argmin) and ρ never enters Ṽ(q) at all. So the sweep's 0.000% spread is not numerical
luck — the spacing-to-range ratio is analytically forced. The geometry *does* force a pure
number; it is just **a/R ≈ 1.41, not ξ_vac/a, and 115× away from 100φ**.

**Why ξ/a is the free knob (class-b).** ξ = 1/√(2ρṼ(0)) = 1/√(2πρUR²) ∝ (ρU)^(−1/2),
while a is pinned to R. So ξ/a ∝ (ρU)^(−1/2) drifts: over U∈[11,88]×ρ∈[1,2] it spans
0.0213–0.0851 (4.0×), with the U:22→44 step giving exactly 1/√2 = 0.7071. The roton
depth/interaction (U, ρ) is a second, independent scale — the located density-sector import.

**The category mismatch (degenerate caveat).** The GP healing length is **sub-cell**
(ξ/a ≈ 0.06); ξ_vac = 100φ = 161.8 would be 115× the lattice spacing. No intrinsic ratio
of the crystallized state is ≈ 161.8 — ξ_vac is a macroscopic scale the *local*
crystallization does not set.

## Discipline / caveats (carried)
- **Eddington:** 100φ entered only the final block; no kernel parameter tuned toward it.
- **Mean-field GP only** (the framework's instantiation level; QMC runs ~30% off at strong
  coupling per the literature). Verdict is **within the §2.64.A local roton-GP scope**; if
  ξ_vac = 100φ is meant to descend from larger-scale structure (global K₇ topology, not the
  local crystallization), that is a different, unspecified computation — the honest
  statement is that the *instantiated substrate does not force it*.
- **γ=6 numerical note (benign):** the γ=6 FT quadrature throws a slow-convergence warning
  (oscillatory J₀ tail) — it is only the *bracketing control*; the canonical MV-G1 soft-disk
  is the **closed-form exact** case and carries the verdict.
- **§2.52 Open 3 untouched**, not loaded, not advanced. No observable bridge.

## Standing of the gate
Two-leg verified (SQT analytic first leg + this independent kernel second leg), and
corroborated by the supersolid literature (SQT's Literature-Search-First: ξ/a parameter-
dependent) and the existing MV-G1 a*=1.4576 (reproduced to ~3%). The density-sector frontier
the V4.47 fold named is **examined and located as class-(b)/imported**: the roton kernel is
the import; §2.64's honest two-anchor count (m_e, ξ_vac) stands, ξ_vac a genuine second
anchor; §2.64.A Item B's "round-decimal fitted-parameter tell" is now confirmed *at the
dynamical level*. Three probes, three distinct imports (G-ζ1 density-gapless; G-INT1 λ;
G-C1 roton kernel) — M.BRIDGE strengthened, not breached.

*Fold (when authorized, SQT-proposed): §2.64.B + one Part VI G-C1 row, V4.47 → V4.48, same
byte-splice discipline, §2.52 row byte-identical. Canonical lives in the framework project.*
