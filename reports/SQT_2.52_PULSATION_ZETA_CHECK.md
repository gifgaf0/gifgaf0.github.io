# §2.52 Open 3 (Pulsation = ζ) — Status Clarified: ζ Is the p6m Packing Void Fraction (M.CW-LEGAL, unlike cos π/10); Value = Output, Dynamical Identification = Import

**Date:** 2026-06-06
**Register:** **R1** for the geometry/classification (ζ = 1−π/√12 = p6m packing
void fraction; M.CW-legal); **open** for the dynamical identification (pulsation
amplitude ratio = ζ), which is currently an import; **conditional on a banked-
definition promotion** (Z5). **Pre-registration:**
`reports/SQT_2.52_PULSATION_ZETA_PREREGISTRATION.md`. **Tool:**
`tools/pulsation_zeta_check.py`.
**Eddington / M.BRIDGE:** ACTIVE — no scale fitted, coupling power selected by the
data; no observable asserted.

> **What this is, plainly.** This is a **status clarification, not a closure** —
> and more modest than the bilateral-fold advance (there was a genuine negative
> finding there; here the substantive content is a classification). It establishes
> three things: (1) the framework's ζ ≈ 0.0931 **is** the p6m hexagonal packing
> **void fraction** ζ = 1 − π/√12 (π/√12 = Thue's densest-packing/occupied
> fraction) — a parameter-free geometric constant of the framework's *own*
> substrate; (2) because ζ is a **dimensionless packing ratio** (not a sign, not a
> scale) it is **M.CW-LEGAL** — the decisive contrast with the sister gate, where
> cos π/10 needed a **sign** and is permanently walled; (3) the **dynamical**
> claim "pulsation amplitude ratio = ζ" requires a specific **linear
> amplitude-area coupling** that the (Fano-blind) §3.4 vacuum action does **not**
> supply — it is currently an **import**, bottoming at the instantiated substrate.
> So both dynamical gates bottom at the same floor (substrate instantiation), but
> this one's target is **legal**, not walled — making it the genuinely promising
> one to instantiate.

## §1 — The value (Z1, Z2): ζ is the p6m packing void fraction, and it is M.CW-legal

- π/√12 = π/(2√3) = **0.906900** is the **densest 2D circle-packing density**
  (Thue), realised by the hexagonal **p6m** lattice — which **is** the framework's
  substrate (§2.1, §2.24). It is the **occupied-area fraction**.
- **ζ = 1 − π/√12 = 0.093100** is therefore the **void (vacant-area) fraction**,
  reproducing the framework's stated ζ ≈ 0.0931 with **no external fit** (Z1).
- ζ is **dimensionless** and an **area/area ratio** — not a sign, not a scale. By
  **M.CW**, combinatorics/geometry *may* fix such a quantity. So this gate is
  **M.CW-LEGAL** (Z2). This is the **decisive structural difference** from the
  bilateral-fold gate, whose target cos π/10 required a **sign** (convexity) and is
  therefore permanently walled. The earlier shared expectation ("pulsation=ζ likely
  bottoms at the same wall") is **refined**: same *floor* (instantiation), but a
  **legal** target here, not a walled one.

**Honest caveat on "output."** The arithmetic (1−π/√12 = 0.0931) and the packing
identity (π/√12 = Thue density) are **R1**. What is currently **not** canonical is
the *identification* of the framework's layer-tax ζ **with** this void fraction:
that closed form lives in a **banked R3 conjecture**
(`unaudited_conjecture_zeta_tax_unified_picture.md`; 5 audit flags, 4 promotion
gates, "do not cite/promote"). So "the value is a genuine output" holds **modulo
promoting that definition** (Z5) — a real prerequisite, not a formality.

## §2 — The dynamical identification (Z3, Z4): the gate's real open content

The gate is not the *value* but the *identification* pulsation-amplitude-ratio = ζ.
Modelling the per-vertex transmission as Φ_out = Φ_in·η^p (occupied fraction
η = π/√12, power p **left free**):

| coupling | loss per vertex = 1 − η^p | |
|---|---|---|
| p=1 (amplitude ∝ occupied area) | **0.0931** | ← matches ζ |
| p=½ (energy ∝ occupied area) | 0.0477 | ✗ |
| p=2 | 0.1775 | ✗ |

- **Z3:** **only** the linear coupling p=1 reproduces ζ. So the gate **requires**
  the amplitude-∝-occupied-area coupling specifically. **Honest register:** this
  *identifies the required coupling*; it does **not** motivate or derive it (the
  power was selected by matching the target — informative about *what closure
  needs*, not evidence the coupling is right).
- **Z4:** is that linear coupling derived from the §3.4 action? **No.** Per
  §3.4-SYM (V4.26) the substrate vacuum is Fano-blind at every local order, so the
  amplitude↔occupied-area coupling is **not** supplied by the vacuum action. It is
  an **import**, living in the instantiated substrate / defect sector — the same
  standing I1–I3 roton ticket that floors the bilateral-fold gate.

## §3 — Verdict and honest scope

**Split verdict (R1 classification; dynamical half open):**

- **Value-half — OUTPUT, M.CW-LEGAL.** ζ = 1−π/√12 is the substrate's packing void
  fraction; parameter-free; dimensionless ratio ⇒ M.CW permits it. Unlike cos π/10,
  **not walled**. (Conditional on promoting the banked definition, Z5.)
- **Dynamical-half — IMPORT, open.** "Pulsation amplitude ratio = ζ" needs the
  linear amplitude-area coupling (Z3), which the Fano-blind vacuum action does not
  supply (Z4). Bottoms at substrate instantiation.

**What is genuinely gained** (kept modest): the gate is **classified** — its target
is M.CW-legal, so it is the *promising* dynamical gate rather than a foregone wall;
ζ is given its **geometric meaning** (the p6m void fraction), which **names the
exact coupling closure requires** (amplitude carried by the occupied substrate,
lost in the void). **What is not gained:** no derivation of the coupling, no
closure, and the value-as-output rests on a banked definition. No observable
(M.BRIDGE).

**Contrast table (the two §3.4 dynamical gates):**

| | bilateral fold → cos π/10 | pulsation = ζ |
|---|---|---|
| target | cos π/10 (a **sign** via convexity) | ζ = void fraction (a **dimensionless ratio**) |
| M.CW status | **walled** (combinatorics can't fix a sign) | **legal** (a packing ratio) |
| value-half | conditional on two metric imports | **genuine geometric output** (Thue + p6m) |
| dynamical-half | convexity + single-seam (imports) | linear amplitude-area coupling (import) |
| bottom | substrate instantiation | substrate instantiation |
| prospect | conditional R2, permanently | **closable in principle** (legal target) |

## §4 — Proposed canonical update (additive)

| Task | Status |
|---|---|
| §2.52 Open 3 (pulsation = ζ) | **STATUS CLARIFIED (R1 classification; gate still open).** ζ = 1−π/√12 = p6m packing **void fraction** (Thue + §2.1/§2.24) — parameter-free, **dimensionless ⇒ M.CW-LEGAL** (unlike the walled cos π/10). **Value-half = genuine output** (conditional on promoting the banked ζ=1−π/√12 definition). **Dynamical-half open:** "pulsation amplitude ratio = ζ" needs the **linear amplitude-∝-occupied-area coupling** (uniquely reproduces ζ; p=½→0.0477), which the Fano-blind §3.4 vacuum action does **not** supply (import; I1–I3 roton floor). The gate is the **promising** dynamical one — legal target, closable in principle on substrate instantiation. |
| prerequisite | **Promote ζ = 1−π/√12** from its banked R3 status (`zeta_tax_unified_picture`, 4 gates) before the value-output is canonical. |
| both §3.4 dynamical gates | bottom at **substrate instantiation**; they differ in M.CW status (cos π/10 walled; ζ legal). |

*Reproduce: `python3 tools/pulsation_zeta_check.py`. Pre-registration:
`SQT_2.52_PULSATION_ZETA_PREREGISTRATION.md`. Append-only; no observable asserted
(M.BRIDGE); the banked-definition caveat (Z5) travels with the value-output. Cross-
refs: §2.52, §2.24 (p6m), §2.1 (substrate), §2.44 (ζ-tower),
`unaudited_conjecture_zeta_tax_unified_picture.md`, Paper II §3.4/§3.4.4,
`SQT_3.4_BILATERAL_FOLD_CHECK.md` (the walled sister gate).*
