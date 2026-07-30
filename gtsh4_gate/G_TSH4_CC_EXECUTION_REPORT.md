# Gate G-TSH4 — CC-leg Execution Report (full-from-scratch, E6)

**Date executed:** 2026-07-30 · **Leg:** CC, full-from-scratch (E6) · **Dispatch:**
`G_TSH4_CC_DISPATCH_INBAND.md` (self-contained in-band edition). **Base canonical:**
SQT Master Ledger V4.71, md5 `9517f4fb7aa2de65b0b4a69985962d8f`. **Instrument:** an
independent numpy/scipy solver built from scratch from the locked model spec —
`tsh4_core.py` and drivers. No chat-leg machinery, energies, constants, slopes,
reports, or verdicts were present in this instance's context (quarantine intact).

## Verify-then-build (mandatory first step) — PASSED
The two embedded artifacts were extracted and hashed byte-exact before any build:
- Embedded LOCKED pre-registration → md5 `e66b964d4467fcb9a5f328ef0db80a35` ✓
- Embedded Amendment-1 PART A → md5 `2c67670112844e9df9cf9909a06ac27a` ✓

A-2 residual gate: **not activated** by the dispatch message; own convergence
practice reported below (residuals driven to 1e-9…1e-13; F-CONV pin honoured).

## VERDICT SUMMARY
| arm | result |
|---|---|
| **Q-A (Phase 0)** | **STACK-SELECTED**, argmin **AB (hcp)** — kernel-independent (step and gem8) |
| **Q-C (Route S)** | **A_3D THREE-D-DISTINCT** (axial-vs-basal compression > θ₂), robust across both kernels and both symmetry classes; F-ISO tensor identity holds to ~1e-6 |
| **Q-D (Route D)** | **NON-CERTIFIED** in the CC leg — BdG solver validated on the analytic uniform control (~2e-13) but the crystal transverse spectrum was not certified; deferred per A-1.6 |
| **E5 halt** | not triggered (no DEGENERATE-STRUCTURE) |

---

## §1 Model and coupling (from the LOCKED spec)
Dimensionless 3D Gross–Pitaevskii energy per particle, ħ=m=R=1, one control
parameter Λ≡ρ̄U₀:

  e = ⟨½|∇ψ̃|²⟩ + (Λ/2)⟨ñ (Û∗ñ)⟩ ,  ñ=|ψ̃|², ⟨ñ⟩=1.

Kernels used analytically in k-space (step: 4π(sin k − k cos k)/k³; gem8:
exp(−r⁸) transformed by high-accuracy quadrature + cubic spline, tol 1e-10).
Coupling pre-declared at **Λ = 2.0 Λ_c** (roton threshold), fixed before any
structure energy existed:

| kernel | Λ_c | k* | Λ = 2Λ_c |
|---|---|---|---|
| step | 21.713735 | 5.4486 | 43.427469 |
| gem8 | 33.783379 | 5.5655 | 67.566757 |

Relaxation: normalised imaginary-time gradient flow for dψ/dτ=−(H−μ)ψ, μ-shift
made consistent so the discrete fixed point is the exact ground state (an
uncorrected semi-implicit scheme carries an O(dt·μ) bias; μ here ≈118, so the
correction is essential). Spectral kinetic operator; convolution by FFT against
the analytic Û̃(G) at the cell's exact reciprocal-lattice vectors (exact periodic
lattice sum, no minimum-image restriction).

## §2 Phase 0 — energies and Q-A (both kernels)
Each structure optimised over (a,c) [hex] or L [cubic] at fixed Λ; F-CONV pin,
symmetry verification, and C-NEG control applied.

**Energies per particle at each structure's own optimum (finer-grid reported):**

| structure | class | e (step) | e (gem8) |
|---|---|---|---|
| **AB** (hcp) | close-packed | **68.34275** | **98.94293** |
| FCC | close-packed | 68.35082 | 98.95386 |
| ABC | close-packed | 68.35124 | 98.95428 |
| BCC | non-close-packed | 69.19142 | 99.85736 |
| AA | non-close-packed | 69.68528 | 100.70063 |

**Q-A decision (A-1.1 class re-carve; margin between class minima vs δ_E=1e-4):**
- close-packed minimum = AB; non-close-packed minimum = BCC.
- class margin = (e_BCC − e_AB)/e_AB = **1.24 %** (step) / **0.92 %** (gem8) ≫ δ_E.
- argmin ∈ close-packed ⇒ **STACK-SELECTED**, both kernels. No E5b halt.
- Stacking sub-question (demoted per A-1.1, *not* verdict-bearing): hcp(AB)
  marginally below fcc(FCC), gap ≈ 1.2e-4 (step) / 1.1e-4 (gem8) — consistent
  across kernels but at the δ_E floor.

**Containment bug-catch (recorded, non-verdict-bearing):** ABC relaxed to
c/a = 3.3919/1.3855 = **2.448 ≈ √6**; its energy matches the independently-seeded
cubic FCC to ~1e-5 (both kernels) — the ABC-contains-FCC consistency check
**passes**, cross-validating two independent relaxation paths.

## §3 Route S — static-elastic curvatures (AB and FCC, both kernels)
Homogeneous strain H→(I+ε)H₀, ψ re-relaxed at fixed ⟨ñ⟩=1 and Λ, raw curvature
A=d²e/dδ² fit over δ∈[−0.02,0.02] (7 pts) with quartic/odd diagnostics
(A_odd ≲ 1e-12 on symmetry-even modes; quartic contributions ≲1% at ε₀).

**Elastic constants (energy-per-volume units; ⟨ñ⟩=1 so per-particle = per-volume):**

| kernel | structure | C11 | C12 | C33 | C44 | C66 |
|---|---|---|---|---|---|---|
| step | AB | 211.9 | 83.8 | 238.6 | 59.9 | 64.0 |
| step | FCC | — | — | — | 92.1 | (C11−C12)=81.6 |
| gem8 | AB | 313.5 | 137.5 | 365.5 | 84.5 | 88.0 |
| gem8 | FCC | — | — | — | 140.4 | (C11−C12)=101.6 |

**F-ISO (A-1.5 tensor identity)** |C66 − (C11−C12)/2|/C66 = **1.34e-6** (step) /
**1.27e-6** (gem8) — deep inside the 2 % gate. Basal elastic isotropy confirmed;
this is the instrument check, not a physics claim.

**A_3D anisotropy (the measurement; θ₁=3 %, θ₂=10 %):**

| kernel | AB axial-vs-basal shear \|C44−C66\|/C66 | AB axial-vs-basal compression \|C33−C11\|/C11 | FCC Zener \|2C44/(C11−C12) −1\| |
|---|---|---|---|
| step | 0.065 (MILD) | **0.126 (THREE-D-DISTINCT)** | **1.256 (THREE-D-DISTINCT)** |
| gem8 | 0.040 (MILD) | **0.166 (THREE-D-DISTINCT)** | **1.763 (THREE-D-DISTINCT)** |

**A_3D verdict:** the 3-D stack is elastically **three-dimensionally distinct** —
the axial-vs-basal *compression* anisotropy exceeds θ₂ for both kernels, and the
cubic (FCC) Zener anisotropy is likewise 3-D-distinct. Cross-class agreement
(hexagonal AB and cubic FCC both THREE-D-DISTINCT, A-1.2) is reportable
structure-robustness. Route-S caveat (A-1.6) carried: these are lattice-elastic
speeds; the superfluid-participation renormalization is the known systematic and
Route-D would be authoritative where the routes disagree.

## §4 Route D — dynamical BdG (NON-CERTIFIED in the CC leg)
A plane-wave Bogoliubov–de Gennes solver was built,
ω² = eig[L0(q)^{1/2}(L0(q)+2X(q))L0(q)^{1/2}], and **validated against the
analytic uniform Bogoliubov spectrum** ω²=(k²/2)(k²/2+2ΛÛ̃(k)) — the C-NEG
dynamical control — to **~2e-13** for both kernels (this exercises the
Hartree+exchange assembly). For the *crystal*, however, a sign-definite (PSD)
fluctuation operator was not achieved at accessible compute: the full-grid ground
state truncated to |G|≤g_cut produces a ground-state/BdG basis inconsistency
(spurious negative ω² growing with g_cut), and the theoretically clean fix
(relaxing ψ₀ self-consistently inside the cutoff) did not converge to a low enough
in-subspace residual to certify PSD-ness within the available budget. Reporting
negative/near-zero ω² as transverse speeds would be false; per **A-1.6** the
Route-S static-elastic result stands as the elastic measurement and the CC-leg
**Route-D dynamical slopes are DEFERRED**. **Q-B statement:** not issued by the CC
leg. This is surfaced for the comparison stage as **gate-fragility (S9-lite
eligible)**; the chat-leg Route-D (full E4 set on AB+FCC@step, A-1.3) is the
authoritative dynamical leg.

## §5 Falsifiers and controls ledger
| control | result |
|---|---|
| **C-NEG** (Phase 0, uniform e=(Λ/2)Û̃(0)) | exact, abs err 0.0 both kernels |
| **C-NEG** (BdG uniform Bogoliubov) | max abs err 2.27e-13 both kernels |
| **F-CONV** (×1.5 resolution at fixed a\*) | \|Δe\|/e ~1e-16 all structures (spectral), gate 5e-6 → PASS |
| **F-ISO** (Route S tensor identity) | 1.3e-6 both kernels → PASS |
| **T1 self-grep** | PASS on every computation file (no forbidden physical-constant / observable-target strings) |
| **symmetry verification** | PASS — relaxed Bragg content matches seed for all structures |

## §6 Mapper (quarantined, run last)
`tsh4_mapper.py` consumes only the frozen measurement files and the thresholds
θ₁=3 %, θ₂=10 %, δ_E=1e-4 (which appear in no other file). Outputs in
`tsh4_mapper_output.json`. It reproduces the Q-A verdict from the ordered e-list
via the A-1.1 re-carve and classifies the A_3D anisotropy against the θ gates as
tabulated in §3.

## §7 For the comparison stage (C1–C6)
- **C1 energies:** §2 tables (both kernels).
- **C2 Q-A arms:** STACK-SELECTED, argmin AB, both kernels; class margins 1.24 %/0.92 %.
- **C3 curvatures/constants:** §3 elastic tables; F-ISO 1.3e-6.
- **C4 Route-D slopes + mode ID:** CC leg **not adjudicated** (Route-D non-certified);
  defer to chat-leg Route-D.
- **C5 falsifier/control ledger:** §5 (every fire surfaced).
- **C6 mapper outputs:** §6 / `tsh4_mapper_output.json`.

Fold candidate V4.72 only after C1–C6 closes. Verdict-level divergence → S9;
the Route-D CC-leg gap is gate-fragility → **S9-lite**.
