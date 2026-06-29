# G-C1 (Angle-3) Execution Pre-Registration — the ξ_vac/a Forcing Test (§2.64 Inverse Problem)

**Date:** June 29, 2026. **Written before any computation.** **Gate label:** G-C1 (the C = ξ_vac/a forcing gate; "angle-3" of the density-sector cluster). **Sibling of** G-ζ1 (§2.88.D.1, density channel) and G-INT1 (§2.88.D.2, internal channel) — the third probe of the I1–I3 substrate-instantiation import.

---

## Question

§2.64.A (V4.46) traced the entire non-anchored empirical content of the §2.64 coarse-graining gate to the single dimensionless constant **C = ξ_vac/a** (vacuum-coherence / lattice-spacing ratio), with ξ_vac = 100φ ≈ 161.803. The disposition (Items B, C) flagged C as dimensionful-dynamical, M.CW-walled, landing on the I1–I3 substrate-instantiation import shared with §2.52 Open 3 and §2.53, and named the round decimal "100" as a fitted-parameter tell.

Angle-3 is the inverse problem:

> **Given that the GP + roton (soft-core) ground state crystallizes to a p6m triangular lattice with constant a, is C = ξ_vac/a forced to a pure number by the triangular geometry (class-(a): pure number × scale), or does it retain a free knob set by the roton kernel — depth/width / interaction strength — (class-(b): a second independent scale)?**

This is the §3.4 "certify class-(a) membership, or locate the class-(b) import" job (turn-2 reframe) applied to the §2.64 dial.

---

## Object

The instantiated substrate: the **mean-field Gross–Pitaevskii functional with a soft-core (roton-inducing) two-body kernel**, the MV-G1 family (V4.26 §3.4-SYM; canonical g = 22, R = 1, ρ₀ = 1; a\* = 1.4576, ξ ≈ 0.15 at the canonical point per the G-ζ1 / G-Φ1 R1 records). Imports limited to the I1–I3 ticket **plus the roton kernel** — the quantity whose import-status is precisely what is under test. No new tuned model.

---

## Quantities (fixed before compute)

- **k_min** — the roton wavevector, k_min = argmin Ṽ(q), Ṽ(q) the 2D Fourier transform of the soft-core kernel (Bogoliubov dispersion ℏω(q) = √[(q²/2)(q²/2 + 2ρṼ(q))]; crystallization onset when ω(k_min) → 0).
- **a** — the p6m lattice constant set by the roton minimum: a = 4π/(√3·k_min) (triangular first reciprocal shell).
- **ξ** — the GP healing length, ξ = 1/√(2 ρ Ṽ(0)) (the coherence scale §2.64.A Item A reads as ξ_vac).
- **a/R** — the dimensionless geometric packing factor (spacing in units of the kernel range).
- **ξ/a** — the candidate C, the density-sector dimensionless ratio under test.
- Kernel parameters: interaction strength U (≡ g), density ρ, range R.

## Test

Vary the kernel parameters (U, ρ at fixed R; and R) across the p6m-crystallizing window. Determine:

1. Is **a·k_min** (equivalently a/R) pinned to a fixed triangular geometric factor, independent of (U, ρ)? *[Prior: YES — k_min is set by the kernel shape, a by k_min.]*
2. Is **ξ/a** a fixed pure number (forced) or does it drift with (U, ρ) at fixed R? *[The crux: drift ⇒ class-(b) ⇒ the roton is a separate import.]*

## Comparison (Eddington-guarded; run last, in one step)

IF a pure-number ratio is found, compare to **100φ = 161.803** — and to its reciprocal and simple functions. The target enters ONLY at this final step, never the construction. No kernel parameter is tuned toward 161.8 (the §2.52 ZETA_TARGET-circularity hazard analog, caught previously by this cross-audit).

---

## Pre-registered arms

- **FORCED-MATCH (breach; very low prior).** C = ξ_vac/a is invariant across the kernel-parameter window (geometry-pinned pure number) AND equals 100φ (or a clean function). ⇒ the roton's 4th import folds into the I1–I3 ticket; §2.64 closes; the "100" is geometric, not fitted; a density-sector M.BRIDGE counterexample. *(Would bear on §2.52 Open 3's shared bottom — but that row stays frozen and untouched regardless.)*
- **FORCED-MISMATCH (informative).** a is geometry-pinned (a/R fixed) but ξ/a — or any candidate C — is a fixed number ≠ a value reproducing 100φ. ⇒ the triangular geometry fixes the spacing-to-range ratio, but ξ_vac = 100φ is a separate fitted scale on top of it; the import is located as the (still free) ξ/a normalization.
- **IMPORTED / class-(b) (expected; the registered a-priori).** ξ/a drifts with the roton depth/width (U, ρ) at fixed R. ⇒ C is imported, not forced by geometry; the density-sector import is LOCATED as the roton kernel (the independent ξ/a knob — the "4th import"); M.BRIDGE confirmed density-side; "100φ" a fitted tell (confirming §2.64.A Item B at the dynamical level). The parallel to G-INT1's class-(b) σ.
- **DEGENERATE / ill-posed (live).** §2.64's ξ_vac (≈ 161.8 lattice cells) is not a property the local crystallization sets — the GP healing length is sub-cell (ξ/a ≈ 0.1, the wrong magnitude and direction for ξ_vac/a ≈ 161.8) — so the identification C = (GP-crystal ratio) is category-mismatched; angle-3 then decides only that no local-crystallization ratio is ≈ 161.8, i.e. ξ_vac lives at a scale the instantiation does not reach (itself an M.BRIDGE statement).

---

## Literature-Search-First finding (run before compute; the rule, V4.42/V4.45)

The soft-core / roton supersolid literature (cross-dialect: supersolid, Brazovskii, Rydberg-dressed BEC, dipolar supersolid) settles the crux:

1. **The lattice constant is pinned to the kernel range.** The high-density soft-core triangular solid has unit cell A = √3(1.6 R_c)²/2 ⇒ a ≈ 1.6 R_c, with k_min set by the kernel Fourier transform (Henkel–Nath–Pohl class; arXiv:1302.4576). The spacing-to-range ratio is geometry-pinned.
2. **The healing-length-to-spacing ratio is NOT universal.** The supersolid region is bounded by hyperbolas R_c²ρU = const, so within it U and ρ move independently of R_c; ξ ∝ 1/√(ρU) drifts while a stays ∝ R. ξ/a is a free knob.
3. **2D mean-field GP gives a clean p6m supersolid with three Goldstone modes** (matches MV-G1's G-ζ1 result), with mean-field running up to ~30% above QMC at strong coupling.

**Consequence (the rule's purpose).** The core question — *is ξ/a a universal pure number?* — is **essentially closed-negative in the literature.** The expected verdict is class-(b)/IMPORTED, and the gate computation is therefore **confirmatory and light** (an analytic roton/Bogoliubov linear-stability calc on the instantiated soft-core kernel), **NOT** a heavy GP crystallization param-sweep (which the LSF rule explicitly bars when the literature has shown the question closed — cf. OP-PSL.3 / V4.45, a tracked direction closed on prior art before sinking compute).

---

## Freeze

**§2.52 Open 3 untouched, not advanced, not annotated.** Shared substrate work for §2.53/§2.64; pulsation = ζ is NOT worked. No target loaded into the construction; 100φ confined to the final comparison step.

## Provenance

`angle3_xivac_forcing.py` — self-contained roton/Bogoliubov linear-stability computation on the soft-core kernel (Ṽ(q), k_min, a/R, ξ, ξ/a across the parameter window); the target 100φ confined to the final comparison block; imports no tool under test.
