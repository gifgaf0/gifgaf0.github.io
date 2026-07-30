# G-TSH4 — EXECUTION PRE-REGISTRATION (LOCKED)
**Gate:** G-TSH4, the 3D-stack shear gate. Registered address §2.91.I Q3 item (3) (§2.88.B caveat).
**Minted:** July 22, 2026, chat leg, on author directive "Authorize V4.71 and Lock G-TSH4."
**Source memo:** `staging_memo_G_TSH4_3D_stack_gate.md`, **LOCKED byte-identical md5 `bfee456f0d936584401fcabd2b75dc13`**.
**Base canonical:** SQT Master Ledger **V4.71**, md5 `9517f4fb7aa2de65b0b4a69985962d8f` — authorized this directive (P-a). ANNEX-CDEF-1 is canonical; the §5.3 Q3(1) carrier-identity coupling is a **live canonical stake**.
**D5:** this artifact travels in-band to the CC leg. It is self-contained: the model below is fully specified so the CC leg builds from scratch with no shared machinery.

---

## §A. Author elections (recorded, immutable after mint)

| | Election | Value |
|---|---|---|
| **P** | Base disposition | **(P-a)** V4.71 authorized; base = `9517f4fb`; Q3(1) coupling live |
| **E1** | Kernel set | **step + gem8** |
| **E2** | Route | **S+D** (static-elastic across the kernel set; dynamical BdG cross-check at one named kernel) |
| **E3** | Structure candidates | **{AA, AB, ABC, FCC, BCC}** |
| **E4** | Direction/polarization sampling | **high-symmetry only**: basal Γ→K, Γ→M; axial Γ→A; one oblique |
| **E5** | DEGENERATE-STRUCTURE handling | **(b) halt to author** |
| **E6** | CC leg | **full-from-scratch** |
| **E7** | Thresholds | **θ₁ = 3%, θ₂ = 10%, δ_E = 10⁻⁴ — T3 immutable** |

## §B. Model specification (exact; both legs bind to this)

Dimensionless 3D Gross–Pitaevskii energy functional, ħ = m = R = 1 (R = kernel range):

  **E[ψ]/V = ⟨ ½|∇ψ|² ⟩ + ½ ⟨ n (U∗n) ⟩ ,  n = |ψ|²**

Scaling out the mean density (ψ = √ρ̄ ψ̃, ñ = |ψ̃|², ⟨ñ⟩ = 1) gives the energy **per particle**

  **e ≡ E/N = ⟨ ½|∇ψ̃|² ⟩ + (Λ/2) ⟨ ñ (Û∗ñ) ⟩ ,  Û ≡ U/U₀**

so the functional has **exactly one control parameter, Λ ≡ ρ̄U₀**, in units ħ²/mR². e is reported in these units. No physical scale is introduced anywhere (T4).

**Kernels (analytic k-space; no real-space kernel sampling — the step kernel's discontinuity would otherwise inject O(dx) error above δ_E):**
- **step:** Û(r) = Θ(1−r); **Û̃(k) = 4π(sin k − k cos k)/k³**, Û̃(0) = 4π/3.
- **gem8:** Û(r) = exp(−r⁸); **Û̃(k) = (4π/k)∫₀^∞ r e^{−r⁸} sin(kr) dr**, Û̃(0) = 4π·(1/8)Γ(3/8); evaluated by high-accuracy quadrature on a dense radial table with cubic-spline interpolation (declared tolerance 1e-10).

**Coupling election (pre-declared, kernel-independent regime convention):** for each kernel, **Λ = 2.0 × Λ_c**, where Λ_c is the roton-instability threshold of the uniform state,
  ω²(k) = (k²/2)[ k²/2 + 2Λ Û̃(k) ],  **Λ_c = min_{k: Û̃(k)<0} [ −k² / (4 Û̃(k)) ]**.
This places both kernels at the same distance above their own crystallization threshold — the "same regime" convention — and is fixed before any structure energy exists.

**Structures and cells (E3):**
- **AA** — simple hexagonal. Orthorhombic cell a × a√3 × c; in-plane basis (0,0), (a/2, a√3/2); one layer per period. Free: (a, c).
- **AB** — 2-layer stacking. Same in-plane cell; layers at z = 0, c/2; B-layer shift (a/2, a√3/6). Free: (a, c).
- **ABC** — 3-layer stacking. Layers at z = 0, c/3, 2c/3; shifts 0, (a/2, a√3/6), (a, a√3/3) mod cell. Free: (a, c).
- **FCC** — conventional cubic cell, 4 sites. Free: L.
- **BCC** — conventional cubic cell, 2 sites. Free: L.

*Recorded containment note (reporting only, not an instrument change):* ABC with free c/a **contains FCC** at c/a = √6, and AB contains ideal hcp at c/a = √(8/3). The separately-seeded cubic FCC run is therefore also a **bug-catch consistency check** on the ABC relaxation. It is explicitly **not** verdict-bearing and cannot alter any arm.

**Optimization:** at fixed Λ, minimize e over (a, c) per hexagonal family and over L per cubic family. Relaxation by normalized imaginary-time gradient flow, spectral kinetic operator, convolution via FFT against analytic Û̃(k) at the cell's discrete reciprocal vectors (this is the exact periodic lattice sum — no minimum-image restriction, small cells legitimate). Seeds: Gaussian droplets at the structure's sites. **Post-relaxation symmetry verification is mandatory**: the relaxed density's Bragg content must still match the seeded structure; if a seeded structure relaxes into a different one, that is reported as data, never silently re-seeded.

## §C. Q-A decision rule (Phase 0)

Order structures by e at their own optimum. With e₁ ≤ e₂ ≤ …:
- **STACK-SELECTED** — argmin ∈ {AA, AB, ABC} and (e₂ − e₁)/|e₁| > δ_E = 1e-4.
- **NON-STACK-SELECTED** — argmin ∈ {FCC, BCC} and (e₂ − e₁)/|e₁| > δ_E.
- **DEGENERATE-STRUCTURE** — (e₂ − e₁)/|e₁| ≤ δ_E → **halt to author (E5b)**.
Reported per kernel. A kernel-dependent structure verdict is itself a reportable finding and inherits the V4.70 KNOB naming requirement.

## §D. Falsifiers and controls, as instantiated for Phase 0

- **F-CONV (the V4.70 successor-binding pin, transposed):** truncation here = plane-wave/grid resolution. Measured **deep** (relaxation residual driven to the declared floor), at **fixed optimized a\*** (never during the a-scan), **continuation-seeded** from the coarser solution. Gate: relative change in e ≤ **5×10⁻⁶** under a resolution increase of ×1.5 per direction. *Rationale on record: the V4.70 H-6 correction — shallow/moving-a\* measurement produced ~10⁻⁵ noise that spuriously dropped six witness points.*
- **C-NEG (Phase 0 instantiation):** uniform state ñ ≡ 1 must return e = (Λ/2)Û̃(0) analytically, to declared tolerance.
- **F-NEG / F9 / F-LIN / F-ISO:** Phase 1–2 falsifiers, not exercised in Phase 0. **F-ISO remains re-scoped as locked:** in-basal-plane isotropy ≤ 2% is the falsifier; basal-vs-axial difference is the measurement and is never a falsifier.
- **T1 self-grep:** every computation file asserts absence of forbidden physical-constant strings before execution; no physical-c, GW, or φ-target string may appear.

## §E. Two-leg plan

Chat leg from scratch. CC leg **full-from-scratch** (E6) with independent solver, seeded only by this artifact. Comparison C1–C6; S9 on any verdict-level divergence; S9-lite available for gate-fragility disputes. Arm mapper quarantined and run last with its own T1 grep — for Phase 0 the mapper consumes only the ordered e-list and δ_E.

## §F. Eddington guard

θ₁ = 3%, θ₂ = 10%, δ_E = 1e-4, Λ = 2.0Λ_c, and the structure-candidate list are fixed **now**, before any structure energy exists. No candidate may be added post-hoc except by author-authorized amendment filed at the catch, pre-verdict. Kernel set fixed; no kernel may be selected by its answer (KNOB). Dead zones are honored, never re-tuned. No observable is evaluated; no comparison to any measured quantity is performed or licensed by this gate.
