# Route B status (E10): non-abelian U(3) vortices, November 4, 2026

Label: Exploration. This note summarizes the E10 reports and adds nothing to them; where it and a report differ, the report governs. Branch `claude/seed-step3-first-closure`.

## The question

Route A (E9) gave no stable closure in any of three stabilizer families. Route B asks the same question in the colour-flavour-locked U(3) model. There the thirds are exact by group structure, the 1/3-flux strings are free, and each string carries its own CP² orientation. Can a closed loop of the elementary string settle at a finite size?

## What has been run

| step | what | result | report |
|---|---|---|---|
| B1 | Prior address | Model fixed: single-coupling U(3), with λ the only parameter (BPS at λ = 1). Normalizations checked. A crude estimate predicted a charge-only ring would leak. Colour-flavour-locked vortons appear untested in the literature. | `prior_address_routeB.md` |
| B2 | Straight-string calibration | Passes everywhere. Published tensions reproduced to ≤ 4.4 × 10⁻⁴. Flux 1/3 and additivity exact. Moduli inertia I = 0.9993 at BPS (predicted 1). | `REPORT_B2B3.md` |
| B3 | Fixed-charge straight-string scan | **WINDOW at λ = 1**, against a prior of about 10 %: 116 sign changes at ω/m ≈ 0.98. NONE at λ = 1.2. At λ = 0.8, NONE only up to the q cap. Charge alone never holds a ring at any λ. | `REPORT_B2B3.md` |
| Amendment A | Verification of the λ = 1 window | **CONFIRMED.** It survives box doubling and tripling, dr halving and the full 2D lattice (agreement 4 × 10⁻⁶). The charge is genuinely bound to the string. Robustness is **one-sided**: the window also exists at λ = 0.8 and 0.9, and not at λ = 1.1. | `REPORT_verify.md` |
| B4 | Axisymmetric loop at #66, n = 3 and 5 | **METASTABLE at both n, "string not required".** The ring stops within 2 % of R_eq, from both starts. Twist retained (τ = 1), leak 3 × 10⁻⁵, half-spacing check passed. E = 1.066 m_bulk·Q. **A bound, vortex-free charged lump at the same Q is cheaper:** E = 0.977 m_bulk·Q at n = 3's Q and 0.967 at n = 5's. A charge-only ring collapses into the same lump. | `PREREG_B4.md`, `REPORT_B4.md` |

## What this establishes

- **A twisted, charged loop of the elementary 1/3-flux string exists as a classical, axisymmetric local minimum** at λ = 1. It needs no added field, and its size matches the straight-string prediction to 2 %. This is the first finite-size closure found in the programme.
- **It is not the cheapest object carrying its charge.** It sits above dispersal into free bulk quanta (+6.6 %). More importantly, it sits **above a non-topological charged lump** (a Q-ball of the SU(3)_{C+F} charge), by 9–10 %.
- **That lump is a genuine bound state.** A box configuration with a vacuum edge extends to infinite space at the same energy and charge. So E < m_bulk·Q in the box implies a bound state below dispersal in infinite space. Its interior is the same partly unhiggsed orientation structure as the string core, without winding.
- **The string is a passenger: the charge binds on its own.** This is the same outcome as E9 option 4, now found in an independent model.
- Under PREREG_B4 §5, Phase 3 (3D stability of the ring) is **not triggered**.

## What is still open

- **Does the bulk Q-ball track the straight-string window?** The window exists at λ ≤ 1 and not at λ ≥ 1.1. If lumps bind exactly where the window exists, the two failures share a mechanism. If they bind more widely, Q-balls are generic in the model. Pre-registered in `PREREG_QB.md`.
- **The ring's barrier to decay into the lump** was not measured. The ring is tested only against axisymmetric deformations. Only one lump start was tried per Q, and whether the lump is the global minimum at fixed Q is not established.
- **B-ii (braids and links)** is untested and unprotected: non-abelian strings always reconnect at BPS (Eto et al., PRL 98, 091602, 2007).
- **Quantum effects:** the CP² moduli acquire a gap. Every result here is classical.

No particle identification is made or implied anywhere in E10.
