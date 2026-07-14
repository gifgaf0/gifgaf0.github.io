# R3 Bridge-Declaration — Paper II-B Acoustic Metric

**Memo ID:** BD-IIB-1
**Date filed:** July 13, 2026
**Register:** R3 — off-ledger staging. Fold candidate **post-V4.63 only**, at Matt's explicit authorization. No ledger anchor assigned (anchor assignment occurs at fold).
**Status:** DECLARED — filed **prior to any II-B computation** (Eddington guard). Algebra only; no data consulted; no simulation run.
**Discipline:** M.BRIDGE declaration · M.CW compliant (form/magnitude split) · LSF precondition attached (§8, blocking) · M.ONT-adjacent flag raised (A-SHEAR, §3)
**Cross-references:** Paper IIA §2.2, §3 (Lemma 3.1), §5.1, §6.1; Paper VII §10, §14 (κ thread), Ch. III Remark III.1 (Lucas identity); `Fold_Redshift_R3_STATUS_post_GFOLD1.md` (ρ_s, Z₀ "Imported" status); §2.89 (scale-filtered locality)

---

## 1. The Identification

**1.1 Composite modulus.** The macroscopic vacuum bulk modulus is declared as a composite of imports already on the books:

$$K \;\equiv\; \frac{Z_0^{\,2}}{\rho_s}$$

where ρ_s (substrate density) and Z₀ carry pre-existing "Imported" status per the G-FOLD1 status block. **Zero new dimensionful entries are added to the import ledger.** Dimensional check: [Z₀²/ρ_s] = (kg m⁻² s⁻¹)²/(kg m⁻³) = kg m⁻¹ s⁻² = Pa. ✓

**1.2 New identification (A-Z0).** Z₀ is identified as the substrate's specific acoustic impedance, Z₀ = ρ_s c_s. This is the memo's single new identification — a role assignment among existing imports, not a new quantity.

**1.3 Consistency relation.** Paper VII's dimensionless κ is formally identified as

$$\kappa \;\equiv\; \frac{K}{\rho_s c^2} \;=\; \varphi^{-4} \;=\; 5 - 3\varphi \;\approx\; 0.145898033750$$

**1.4 Longitudinal speed (fluid branch, LOCKED — see I-CONST, §3).** Under the pure-compression dispersion c_s² = K/ρ_s:

$$c_s \;=\; \sqrt{\kappa}\,c \;=\; \varphi^{-2} c \;=\; (2-\varphi)\,c \;\approx\; 0.381966011250\,c$$

**1.5 M.CW compliance.** κ carries the *form*; the *scale* resides entirely in {ρ_s, Z₀}. No dimensionful constant is produced from combinatorics. The relation contains no adjustable parameter: given the imports and A-Z0, c_s/c is forced.

---

## 2. The Bridge Claim — Scope and Exclusions

**2.1 Claim.** This identification serves the **Paper IIA emergent-Bjerknes thread exclusively.** Gravity in the longitudinal sector is formally modeled as the collective hydrodynamic response of the substrate, with the effective geometry given by the acoustic-metric construction (Unruh 1981; Visser; Barceló–Liberati–Visser, *Living Rev. Relativ.*). The fold-density → effective-metric bridge named in the July 13 session is this construction; II-B does not invent it, it instantiates it with SQT inputs.

**2.2 Exclusion — Paper VII §10.1.** The claim "gravity is the vacuum's intrinsic throat curvature at its own ground state" is **not** served by this declaration. The IIA (emergent Bjerknes) / VII §10.1 (intrinsic curvature) tension is hereby placed on record; reconciliation, if attempted, is separate work with its own declaration. The natural junction is noted for future reference: throat curvature → κ → propagation speed → Bjerknes transmission.

**2.3 Exclusion — Lucas identity.** φ⁴ + κ = 7 (Remark III.1) has **no mechanical role** in this bridge. It is excluded from the declaration.

**2.4 Exclusion — prior κ appearances.** The five Paper VII §14 appearances of κ (mass operator, f_c, top Z_f, gravity filtration, S-matrix dissipation) all predate the M.CW wall and none is load-bearing in a wave equation. This declaration is κ's **sixth role and first mechanical one.** The five priors are precedent, not support.

---

## 3. Assumption Inventory

| Tag | Content | Status |
|-----|---------|--------|
| A-IMP | ρ_s, Z₀ are declared dimensionful imports | Pre-existing (G-FOLD1 status block) |
| A-Z0 | Z₀ = ρ_s c_s (specific acoustic impedance) | **New, this memo** |
| A-SHEAR | The electromagnetic and emergent spin-2 radiative sectors both propagate on the **transverse** channel with c_T ≡ c (implying μ = ρ_s c² wherever a shear modulus is defined) | **New, this memo.** M.ONT-adjacent — this is a declaration of what a photon *is* on the substrate; not established in Paper IIA; required for the GW170817 structural pass (§9.2); flagged for the pending M.ONT adjudication |
| I-CONST | Constitutive-branch declaration (below) | **New, this memo** |

**I-CONST — constitutive branch (load-bearing; recorded, not smuggled):**

- **Fluid branch — LOCKED per directive.** Pure-compression dispersion c_s² = K/ρ_s → c_s = φ⁻²c ≈ 0.382c. Consonant with the "superfluid" identification. *Caveat:* a strict fluid supports no elastic transverse channel, so under this branch A-SHEAR requires a distinct transverse carrier (lattice registration vs. continuum fluid — open).
- **Solid branch — RECORDED, not locked.** Isotropic elastic solid with μ = ρ_s c² (from A-SHEAR): longitudinal speed c_L = √(κ + 4/3)·c ≈ **1.216236558850 c** (3D), Poisson ratio ν = (3κ−2)/(2(3κ+1)) ≈ **−0.543337** — strongly auxetic, within the isotropic stability bounds −1 < ν < ½. Note: zero viscosity (Paper IIA Thm 2.1) constrains *dissipation*, not elastic shear rigidity, so the solid branch is **not excluded** by Paper IIA.
- **Amendment rule.** Any branch switch is a visible amendment to this memo, never a silent re-derivation. All downstream II-B results must state which branch they stand on.

---

## 4. Kill Condition 1 — Scalar / Longitudinal Radiation

**Threshold.** Double-pulsar (PSR J0737−3039A/B) orbital decay agrees with the GR quadrupole formula at the **1.3 × 10⁻⁴** fractional level (Kramer et al. 2021, PRX 11, 041050).

**Requirement.** Longitudinal-channel radiative losses from bound binaries (monopole, dipole, or scalar emission at c_s = 0.382c) must be shown non-radiative or suppressed below that fractional level.

**Designated defense (to be tested, not assumed).** Lemma 3.1's global-drive structure: knots contribute *response amplitude* to a single common substrate drive, not independent source frequencies; independent monopole emission from individual bodies is therefore structurally suppressed. This must be proven at linear order in the II-B Lagrangian.

**PASS:** proof that longitudinal emission vanishes at quadrupole-comparable order, or is suppressed by ≥ 10⁴ relative to the transverse quadrupole channel.
**FAIL:** predicted fractional orbital-decay excess above 1.3 × 10⁻⁴ → the longitudinal acoustic bridge is retired (blast radius, §7).

---

## 5. Kill Condition 2 — Laplace Aberration

**Requirement.** The near-field Bjerknes interaction, propagating at c_s = 0.382c, must either

- **(a)** reproduce the aberration-cancelling, velocity-dependent (extrapolative) interaction structure demonstrated for electromagnetism and GR (Carlip 2000, *Phys. Lett. A* 267, 81) to the post-Newtonian orders bounded by planetary ephemerides, **or**
- **(b)** be shown **effectively static**: the force on a knot set by the local, instantaneous amplitude of the global standing drive rather than by retarded signals from the partner body — in which case no aberration arises to cancel.

**PASS:** (a) or (b) established at the order ephemerides constrain.
**FAIL:** residual aberration produces secular drift in orbital elements (angular-momentum non-conservation, perihelion anomalies) above ephemeris bounds → the longitudinal acoustic bridge is retired.

---

## 6. Shared-Dependency Flag

Both kill-condition defenses currently route through **Lemma 3.1** (global drive): KC1 via suppression of independent emission, KC2 via the effectively-static branch (b). **Single point of failure declared:** refutation of the global-drive structure fells both defenses simultaneously. Any independent defense discovered later is to be logged as an amendment to this memo.

---

## 7. Blast Radius on Failure

On failure of either kill condition:

1. The **longitudinal acoustic-metric bridge is retired.**
2. The identification K = Z₀²/ρ_s **survives** as dimensional bookkeeping (it asserts nothing dynamical by itself).
3. A-SHEAR and all transverse-sector statements are **independent** and unaffected.
4. Paper IIA §3–§4 parameterization is untouched (precedent: the §2.2 negative-result handling, where the equations never used the retired mechanism, only the parameterization).

---

## 8. LSF Precondition (BLOCKING — no II-B compute before completion)

Cross-dialect prior-art search under **target-field vocabulary**, not SQT vocabulary:

*acoustic metric · analogue gravity · analogue spacetime · effective metric in superfluids / BECs · elastic aether / bimetric elasticity · speed of gravity, aberration · scalar gravitational radiation, binary pulsar constraints · Lorentz violation, gravity sector, two-speed models*

Named anchors: Unruh (1981); Visser (1998, acoustic geometries); Barceló–Liberati–Visser (*Living Rev. Relativ.*, "Analogue Gravity"); Carlip (2000); Kramer et al. (2021); GW170817 speed bound (|c_gw/c − 1| ≲ 10⁻¹⁵).

Purpose: locate prior constructions in which a longitudinal/transverse two-speed split has been proposed and constrained, before any compute investment. (Standing lesson: OP-PSL.3 and the V4.42 collision both arose from searching internal vocabulary.)

---

## 9. Eddington Accounting

**9.1** This declaration is filed **before** any observable has been evaluated under c_s = φ⁻²c. No data was consulted in fixing K, κ, A-Z0, or the branch lock.

**9.2 Disclosure.** The GW170817 structural pass (both radiative sectors transverse at c_T ≡ c) was identified in-session *prior to filing* and motivated A-SHEAR. It constrains the **transverse** channel only and played no role in fixing κ, K, or c_s. It is recorded here as motivation, not as a post-hoc fit.

**9.3** KC1 and KC2 cite existing experimental constraints as **thresholds**, not as fitting targets. No SQT quantity has been adjusted toward them.

---

## 10. CC-Leg Replication Scope and Promotion Path

**CC leg verifies (zero shared machinery):**
1. Dimensional identity of K = Z₀²/ρ_s.
2. Exact forms φ⁻² = 2 − φ and φ⁻⁴ = 5 − 3φ.
3. Fluid-branch value c_s/c = 0.381966011250.
4. Solid-branch values c_L/c = 1.216236558850 and ν = −0.543337382198, with stability-bound check.
5. Lucas cross-check φ⁴ + φ⁻⁴ = 7 (exact) — noting §2.3's exclusion of this identity from any mechanical role.

**Promotion path:** R3 staging → CC-leg replication → fold candidate **after V4.63 completes**, at Matt's explicit fold authorization. This memo does not interleave into the pending Gate-2a / §2.87.J fold.

---

## Numerical Appendix (verified by chat-leg computation, July 13, 2026)

| Quantity | Exact form | Decimal |
|----------|-----------|---------|
| φ | (1+√5)/2 | 1.618033988750 |
| κ = φ⁻⁴ | 5 − 3φ | 0.145898033750 |
| c_s/c (fluid branch) | φ⁻² = 2 − φ | 0.381966011250 |
| c_L/c (solid branch, 3D) | √(κ + 4/3) | 1.216236558850 |
| ν (solid branch) | (3κ−2)/(2(3κ+1)) | −0.543337382198 |
| Lucas check | φ⁴ + φ⁻⁴ = L₄ | 7 (exact) |

---

*Status at filing: R3, off-ledger, MD5-locked at creation. Do not cite. Entry condition for any II-B computation: §8 LSF completion. Entry condition for fold: CC-leg replication (§10) + V4.63 completion + explicit fold authorization.*
