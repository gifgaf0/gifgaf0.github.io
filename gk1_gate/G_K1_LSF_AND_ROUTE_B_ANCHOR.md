# G-κ1 — LSF closure of Q1 + route-(b) anchor (CC); handoff targets scoped

**Date:** 2026-07-05 · **Pre-reg:** `G_K1_EXECUTION_PREREGISTRATION.md` (channel (iii),
curvature-coupled core dilation) · **Re-scoping:** `G_K1_SEC214_CONSUMPTION_READING.md`
(the "seal the container" audit). This records the mandatory LSF (step 1), a
definition-robust anchor for the route-(b) crux, and an honest scope of the two CC-handoff
compute targets.

## 1. Literature-Search-First (mandatory step 1) — Q1 structure is prior art
Curved quantum-vortex core deformation is **established GP territory**:
- the curvature response is the **local-induction / Biot–Savart self-interaction** with a
  **healing-length core cutoff** (the core-radius dependence enters as the short-distance
  cutoff of the diverging self-interaction);
- the core size is set by ξ; energy corrections organize in **ξ/R**; the response is even in
  κ (orientation-independent) — exactly the pre-registered form r_eff(s)=ξ(1+c₂(ξκ)²+…).

So **Q1's structure is prior art** (curved-vortex core dilation is a known GP-perturbation
problem; c₂ is a **functional of the kernel**, not a new dimensionless import). Only the
kernel-specific coefficient is a demonstration. This supports the re-scoping's **D1 = (a)**
("no new dimensionless import; Q1a prior art + Q1b demonstration"). *(Sources in the chat
reply; representative: GP curved-vortex / local-induction and vortex-ring core-energy
literature on arXiv.)*

## 2. The re-scoping (faithful record; the §2.14 audit is chat-side)
The chat-side §2.14 ledger audit **seals the container**: the mass exponent
m = m₀·(A/Z_f)·exp(L/(Φ·r_eff(L))) consumes **strictly the geometric (ideal ropelength) L**
— nothing hydrodynamic. Four confirmations (formula structure; the electron L_e=2π lattice
closure count; the proton falsification clause in *geometric* ropelength L_B=60.194 ∈ Ashton
[58.006,62.0]; and canon's own precedent rejecting a physical-mechanism insertion into the
exponent). **Consequence:** channel (iii)'s tension **cannot enter the exponent** — the
exponential-amplification catastrophe does not occur; the mass ratios are safe *through this
route*, by construction. **This is a §2.14 ledger read (canonical, framework project) — I
cannot second-leg it from this code repo; recorded as chat-side-audited.**

**The located import (the honest price of the seal):** E_hydro=∫T(s)ds is a real,
knot-class-dependent energy that, being barred from the exponent, must couple to observed
mass in some declared way — and canon declares none. That coupling scale is the new located
import (M.BRIDGE). Pre-locked thresholds (route (b), core-dominance) from the already-run
Q2 stats (std(ln R_cut)=0.192, cross-class ΔT≈1.0): internal dispersion <3% needs **C≳5.3**;
cross-class shift <3% needs **C≳32**; calibration **C_GP=0.38**.

## 3. Route-(b) anchor + Q1b second leg (CC, independent)

**3a. GP vortex energy split (`gk1_gp_vortex_anchor.py`).** Flow (azimuthal 1/r²) energy is a
**universal log** (E(R)/π = 1.000·ln R + O(1), slope exactly 1); the core is a convergent
O(1). The flow log is set by Γ and ρ_∞ — *identical for any single-charge superfluid vortex,
GP or roton*. Only the O(1) core constant is kernel-dependent. **[Correction:** an earlier
note here mislabeled the core/flow *ratio* (0.389) as "reproducing C_GP=0.38." That was a
coincidence — the memo's C_GP=0.38 is the **additive core constant** ln(1.464), reproduced
properly in 3b below, not the core/flow ratio. The route-(b) physics is unaffected.]

**3b. Q1b two-leg (`gk1_q1b_secondleg.py`) — the decidable, bankable piece.** I recomputed the
core parameter C[kernel] (= additive core constant, C = lim[e(R)−ln R]) by an **independent
method** (scipy solve_bvp; the first leg used Newton/Thomas relaxation), across the local
kernel family U′(n)=n^γ:

| kernel | C (second leg) | first leg |
|---|---|---|
| γ=1 (GP) | **+0.3809** (= ln 1.464) | +0.3810 |
| γ=2 | +0.6156 | +0.6156 |
| γ=3 | +0.7272 | +0.7273 |

Match to **3–4 digits, zero shared machinery** — Q1b is **two-leg verified**. C is a bounded
O(1) kernel functional with no residual freedom ⇒ **no new dimensionless import** (D1=(a)).

**Route-(b) verdict — now directly supported (not just by the universality argument).** Route
(b) needs C ≳ 5.3 (dispersion) / 32 (cross-class) vs the O(1) family C ∈ [0.38, 0.73]. That is
**14×–84× outside** the entire local kernel family — the core would have to swamp the universal
flow by tens. **Route (b) fails robustly ⇒ the E_hydro↔mass coupling is a genuine located
import (route c)** — the hybrid fold the re-scoping proposes. The one remaining numeric — the
*nonlocal roton* C[K_roton] via Berloff–Roberts — is an **evaluation of this existing (class-b)
import**, expected O(1) (both the family and the universality argument point there), and is
*not* fold-deciding.

## 4. Status after the first-leg scripts arrived
The chat-side first-leg scripts (`gk1_q1b_core_parameter.py`, `gk1_q2_borromean_bound.py`,
`G_K1_FIRST_LEG_RESULTS.md`) are now in hand and archived here. Updated status:
- **Q1b — two-leg DONE** (§3b): C[kernel] reproduced independently to 3–4 digits; no new
  import; route (b) directly closed.
- **Q2 (golden-ellipse stand-in) — first-leg pipeline in hand.** It gives large tension
  structure: internal dispersion ~8–13%, cross-class shift vs the tight unknot ≈ **−41%**
  (screening: a compact tangle's flow is cut off at 2.4–4.2ξ by neighbor strands, an isolated
  ring's is not). C enters T *additively*, so these **shape** results are kernel-robust (C
  cancels). Two refinements remain, neither fold-deciding after the §2.14 seal: **(i)** an
  independent Q2 second leg / **CKS-exact** tight-Borromean geometry (expected to *shrink* the
  internal dispersion — tightness equalizes constraints — while the screening shift persists);
  **(ii)** the **nonlocal roton C[K_roton]** (Berloff–Roberts) — an evaluation of the existing
  class-(b) import, expected O(1).
- **The decisive move was interpretive, not numeric:** the §2.14-consumption reading. The
  first leg itself flagged the exponential-amplification hazard (a tension shift in
  exp(L/Φr_eff) would be amplified by ~L/Φξ e-folds); the re-scoping audit resolved it by
  showing **L is geometric ropelength** and the exponent is sealed, so the −41% lands in the
  E_hydro ledger, not the exponent.

**The fold can state the hybrid verdict now:** D1=(a) (no new dimensionless import — Q1
prior-art + Q1b two-leg), exponent **sealed** (ARM-R for the container), δ material but in the
**E_hydro ledger not the exponent** (ARM-N magnitude lands there), and **one located import**
(E_hydro↔mass coupling). CKS-exact δ and roton C[K_roton] refine the *magnitude* of that
import, not the verdict. §2.52 untouched; no observable target entered the construction (0.03
is a comparison bound only); Eddington guard held; the first leg's one bug (vertex-flank
self-contact) was caught and corrected in-file before interpretation.
