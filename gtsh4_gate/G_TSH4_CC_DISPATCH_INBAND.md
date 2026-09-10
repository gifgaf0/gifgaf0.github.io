# G-TSH4 — CC DISPATCH, SELF-CONTAINED IN-BAND EDITION
**Supersedes** the reference-style handoff (`e04ef0400c743b5ff6ab83c7570fc2a5`). **Why:** three dispatches carried a handoff that *described* the locked artifacts by md5 but did not *contain* them — a D5 defect on the chat leg. This single file embeds both, byte-exact. For a blind leg, dispatch THIS FILE ONLY.

**Base canonical:** V4.71 md5 `9517f4fb7aa2de65b0b4a69985962d8f`. Chain live re-verified at assembly: reverse-splice of the 7 declared fold insertions (+12,797 B) reconstructs V4.70, 1,334,614 B, md5 `969124145cd3070b266d3c5ecf44434e`, byte-exact.

## SEALS
| block | md5 |
|---|---|
| Embedded LOCKED pre-registration | `e66b964d4467fcb9a5f328ef0db80a35` (equals the locked seal) |
| Embedded Amendment-1 PART A | `2c67670112844e9df9cf9909a06ac27a` (sealed at this assembly; parent file `908f4795380ac3461d79362b7d37d3d8`; PART B quarantined, intentionally absent) |

## Verify-then-build (mandatory first step)
```
python3 - <<'PY'
import hashlib
raw=open("G_TSH4_CC_DISPATCH_INBAND.md","rb").read()
B1=b"=====BEGIN LOCK"+b"ED PREREG====="; E1=b"=====END LOCK"+b"ED PREREG====="
B2=b"=====BEGIN AMEND"+b"MENT-1 PART A====="; E2=b"=====END AMEND"+b"MENT-1 PART A====="
def blk(b1,b2):
    s=raw.index(b1)+len(b1)+1; e=raw.index(b2)-1; return raw[s:e]
p=blk(B1,E1); a=blk(B2,E2)
open("G_TSH4_EXECUTION_PREREGISTRATION.md","wb").write(p)
open("G_TSH4_PREREG_AMENDMENT_1_PARTA.md","wb").write(a)
ok1=hashlib.md5(p).hexdigest()=="e66b964d4467fcb9a5f328ef0db80a35"
ok2=hashlib.md5(a).hexdigest()=="2c67670112844e9df9cf9909a06ac27a"
print("prereg:",ok1,"partA:",ok2); assert ok1 and ok2
PY
```
Build nothing until both print True.

## Blind-leg scope (full-from-scratch, E6)
- **Phase 0:** all five structures × both kernels, independent solver of your choosing, energies at each structure's own optimized geometry; apply the A-1.1 re-carved rule; report per kernel.
- **Route S:** elastic curvature set on AB (xz, xy, dev, bi, zz, iso) and FCC (xz, dev, iso), both kernels; raw A per mode with quartic/odd diagnostics; ε₀ and grids your own, declared before running.
- **Route D:** BdG transverse branches on AB **and** FCC at the step kernel over the full E4 direction sets (A-1.4), ≥2 |q| per direction, mode identification documented; Q-B statement.
- **Falsifiers/controls as locked:** F-CONV (deep, fixed-a*, continuation-seeded), F9 Ward, F-LIN, F-ISO both instantiations (A-1.5), C-NEG uniform Bogoliubov, C-POS Christoffel closed forms, T1 self-grep on every file.
- **Mapper:** build your own quarantined θ mapper, run last; θ₁/θ₂ appear only there.
- **Quarantine:** no chat-leg energies, constants, slopes, reports, or verdicts may be present in the blind instance's context. If any appear, HALT and report the exposure.

## Conditional block — A-2 residual validity gate [ACTIVE ONLY IF THE AUTHOR SAYS SO IN THE DISPATCH MESSAGE]
Every ground state used for any reported quantity must satisfy ||H psi0 - mu psi0||/mu <= 1e-6, with the residual reported alongside every energy. If A-2 is not activated, use your own convergence practice and report your own convergence evidence; the comparison stage adjudicates.

## Comparison protocol (after your numbers freeze)
C1 energies; C2 Q-A arms; C3 curvatures/constants; C4 Route-D slopes + mode identification; C5 falsifier/control ledger (every fire on either leg surfaced); C6 mapper outputs. Verdict-level divergence → S9; gate-fragility → S9-lite. Fold candidate V4.72 only after C1–C6 closes.

=====BEGIN LOCKED PREREG=====
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

=====END LOCKED PREREG=====

=====BEGIN AMENDMENT-1 PART A=====
# G-TSH4 — PRE-REGISTRATION AMENDMENT 1 (A-1 class: filed at the catch, pre-verdict, author-authorized)
**Amends:** `G_TSH4_EXECUTION_PREREGISTRATION.md` md5 `e66b964d4467fcb9a5f328ef0db80a35` (which remains byte-frozen; this artifact travels with it).
**Authorization:** author directive July 22, 2026 — *"Resolve Phase 0 Halt and Dispatch CC Leg"* — items 1–3 quoted in the ledger record.
**Base canonical:** V4.71 md5 `9517f4fb7aa2de65b0b4a69985962d8f`.

---

## PART A — amended rules (IN-BAND: travels to the CC leg)

**A-1.1 (Q-A arm re-carve; replaces §C's label map only, thresholds untouched).**
- **STACK-SELECTED (close-packed p6m stacks):** argmin ∈ {AB, ABC≡FCC}.
- **NON-STACK-SELECTED (non-close-packed):** argmin ∈ {AA, BCC}.
- Decision margin unchanged: (e₂ᶜˡᵃˢˢ − e₁ᶜˡᵃˢˢ)/|e₁| vs δ_E = 1e-4 computed **between the class minima**.
- **Stacking sequence (hcp vs fcc) is demoted to a sub-question**: reported as data with its own gap, never verdict-bearing at Q-A.
- Grounds on record: FCC **is** an ABC stack of triangular layers (c/a = √6 containment, exact lattice geometry); the original labels did not carve the structure space.

**A-1.2 (E5 halt resolution; Q-C scope).** Q-C (and Q-D) run on **both** close-packed structures — **AB (hexagonal class)** and **FCC (cubic class)** — at each elected kernel. The §2.88.B isotropy caveat is tested against both symmetry classes; agreement of the A_3D verdicts across the two classes is itself reportable structure-robustness data.

**A-1.3 (Route-D declarations, made before any Q-C quantity exists).**
- Route-D kernel: **step** — declared by TSH1–3 continuity (the TSH-era baseline kernel), not by any answer (KNOB discipline).
- Route-D scope per leg: chat leg = AB@step full E4 direction set + FCC@step as budget allows; **CC leg = the full Route-D set on both structures** (the heavier dynamical leg is deliberately placed on the CC side).
- Dynamical transverse identification: the two lowest-slope gapless branches at small |q| in each direction; their linear slopes are the dynamical transverse speeds.

**A-1.4 (E4 mapping for the cubic class).** The high-symmetry set for FCC is **[100], [110], [111]** plus the [110]-plane oblique implied by the Christoffel closed forms; for AB the locked set stands (basal Γ→K, Γ→M; axial Γ→A; one oblique at 45°).

**A-1.5 (F-ISO, Route-S instantiation).** For the static route on the hexagonal class, the in-basal-plane falsifier is instantiated as the tensor identity residual **|C66 − (C11−C12)/2| / C66 ≤ 2%** (basal elastic isotropy is a hexagonal tensor identity; its numerical residual is the instrument check). Basal-vs-axial difference remains the measurement, never a falsifier. For the dynamical route, Γ→K vs Γ→M slope agreement ≤ 2% stands as locked.

**A-1.6 (Route-S caveat, carried verbatim on every number).** Static-elastic speeds are lattice-elastic quantities; the superfluid-participation renormalization (the 2D W-μ record: μ_s/(ρc_T²) = 0.712/0.778/0.993 across kernels) is the known systematic. Route-D slopes are authoritative where the routes disagree.

**A-1.7 (Eddington).** θ₁ = 3%, θ₂ = 10%, δ_E = 1e-4, Λ = 2.0Λ_c, kernels, structures, and the E4 sets are unchanged and remain T3-immutable. Nothing in this amendment adds a candidate, moves a threshold, or licenses any observable comparison.


=====END AMENDMENT-1 PART A=====
