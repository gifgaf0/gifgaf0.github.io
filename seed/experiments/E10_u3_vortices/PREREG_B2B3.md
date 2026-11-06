# E10 / Route B: pre-registration for B2 (straight-string calibration) and B3 (fixed-charge feasibility)

*November 2, 2026. Label: Exploration. Written before any E10 code exists. Follows `NOTE_route_B.md` and `prior_address_routeB.md` (B1). No loop is computed in B2 or B3.*

## 1. Model (fixed by B1 §1)

U(3) gauge theory, single coupling, Auzzi–Eto–Vinci normalization. Rescaled units: H → vH, W → gvW, x → x/(gv). Energies per unit length are in units of v², lengths in units of 1/(gv).

**Static energy per unit length:**

  T[H, W] = ∫ d²x Tr[ ½ f_ij f_ij + (D_iH)(D_iH)† + (λ²/4)(1 − HH†)² ],

with:
- f_ij = ∂_iW_j − ∂_jW_i + i[W_i, W_j],
- D_iH = ∂_iH + iW_iH,
- W a Hermitian 3 × 3 matrix (U(3)),
- H a complex 3 × 3 matrix (rows colour, columns flavour).

**Vacuum and bulk masses.**
- Vacuum: H = 1.
- Bulk masses: vectors M_V = 1; adjoint and singlet scalars M_s = λ (B1 §1).
- Lightest SU(3)_{C+F}-charged bulk mode: m_bulk = min(1, λ).

**BPS check of the normalization (derived for this document).** For a single diagonal entry this is the abelian Higgs model B² + |Dφ|² + (λ²/4)(1 − |φ|²)². The Bogomolny completion needs (λ²/4) = ¼, so λ = 1, and gives a tension of 2π per unit winding. This agrees with B1's checked statement that BPS is at λ = 1, with tension 2πv².

**Parameters.** λ ∈ {0.8, 1.0, 1.2}, fixed in B1 §5. Nothing else is free.

## 2. B2: straight-string calibration (predictions)

Configurations, each minimized at fixed winding:
- the elementary string, diag(φ(r)e^{iθ}, 1, 1),
- the coincident winding-2 string in one entry, diag(φ(r)e^{2iθ}, 1, 1),
- the abelian composite, all three entries winding once.

| ID | Prediction | Tolerance | Basis |
|---|---|---|---|
| C1 | T(k = 1)/2π = 0.91231, 1.00000, 1.07922 at λ = 0.8, 1.0, 1.2 | 1e-3 relative | B1 table (Eto, arXiv:0810.4895) |
| C2 | T(k = 2, same entry)/2π = 1.77407, 2.00000, 2.20944 | 1e-3 relative | same |
| C3 | ∫Tr B (elementary) / ∫Tr B (composite) = 1/3 | 1e-6 | B1 §2, derived |
| C4 | T(composite) = 3·T(elementary) at every λ (entries decouple in the single-coupling model) | 1e-4 relative | B1 §2; B1 table caption |
| C5 | Moduli inertia at λ = 1. Take the elementary string at orientation n = (1, 1, 0)/√2. Rotate it slowly in time by U(t) = exp(−iωt G), G = diag(0, 1, 0), acting as H → U H U† (colour and flavour). Minimize the kinetic energy over the time component of the gauge field (Gauss law). Then E_rot / ω² → π·I as ω → 0, with **I = 1**. | 2 % | B1 §2–§3: worldsheet β = 2π/g²; energy 4πI ω² sin²α cos²α at α = π/4 |
| C6 | Also at λ = 0.8 and 1.2: report I. | none | descriptive, no prior |

**Prior.**
- C1–C4: 95 %. These are reproductions; a failure means an instrument error.
- C5: 75 %. The normalization chain from the worldsheet literature to this model's conventions is checked only at the level of B1 §1. A failure of C5 with C1–C4 passing would be a **normalization finding**, recorded and used, not a stop. B3 uses the measured I, not the literature value.

## 3. B3: fixed-charge straight string (predictions)

**Ansatz.**

  H(t, z, x, y) = U(kz − ωt) H(x, y) U(kz − ωt)†,  U(α) = exp(iαG),  G = diag(0, 1, 0),

with W_x, W_y similarly rotated, plus the dressings W_z and W_t, which are solved for. The static profile H(x, y), W_x, W_y relaxes fully, including the orientation angle and core deformation.

**Functional.** At fixed twist k and charge per length q:

  ℰ(k, q) = min over the static fields and W_z of [ T + k²·J ] + q²/(4I),

- J is the twist inertia, with W_z dressing.
- I(H) = min over W_t of the kinetic quadratic form divided by ω² (Gauss law).
- ω = q/(2I).
- Because I is defined as an inner minimum, the outer problem is a minimization over H of T + k²J + q²/(4I(H)). The gradient of the last term follows from the envelope theorem.

**Window.** A (k, q) point is in the window if:
- ω < m_bulk, and
- less than 1 % of the charge density lies within 4 units of the box edge (leak).

**Scan.**
- Primary: **k = 0 (charge only)**, q from 0 in steps of 0.1 until the window closes.
- Secondary: k = 0.05 to 1.0 in steps of 0.05, with q scanned the same way at each k.

**Thin-ring test (as in E9 Phase 0).**
- 𝒯 = ℰ − k∂_kℰ − q∂_qℰ.
- WINDOW if 𝒯 changes sign inside the window at a point where d²E/dR² > 0, for E(R) = 2πR·ℰ(n/R, Q/2πR) at fixed n and Q.
- At k = 0, take n = 0 and evaluate along R at fixed Q.
- NONE otherwise.
- Report the frozen-profile value 𝒯_frozen = T − (k² + ω²)·I(0) alongside.

| ID | Prediction | Prior |
|---|---|---|
| P1 | k = 0: NONE at every λ. The window closes (ω → m_bulk, or leak) while 𝒯 > 0. Frozen estimate: 𝒯 = 0 needs ω² = T/I ≈ 2 > m_bulk² (B1 §3). | 85 % |
| P2 | Along k = 0, I(q) grows as ω → m_bulk, because the W_t dressing's range ~ 1/√(m_bulk² − ω²) diverges. But not enough to bring 𝒯 to zero inside the window. | descriptive |
| P3 | k > 0: NONE at every λ inside the moduli-valid region k, ω < 0.5. Anywhere in the scanned window: NONE, with a prior of 85 %. | 85 % |
| P4 | The relaxed orientation angle sits near α = π/4 when q > 0 and k = 0 (maximal inertia). With k > 0 and q = 0, it moves to α → 0 or π/2: the current switches itself off, because a twist about G costs nothing when n is an eigenvector of G. | 80 % |
| **Overall** | **B3 finds a WINDOW somewhere: about 10 %** (B1 §5). | |

## 4. What follows from each outcome

- **NONE everywhere.** Route B's intrinsic vorton (B-i) is closed at thin-ring level in this model. Thick vortons are not excluded, but there is no window to aim a loop run at. B4 is not run. Route B's remaining question is B-ii (braids and links), which B1 found unprotected.
- **WINDOW somewhere.** B4 (axisymmetric loop) gets its own pre-registration, using the same selection discipline as E9 option 4 Amendment A. The selection rule is written before B4, and the passenger control is the cheapest charged bulk lump.

## 5. Eddington guard

- **Fixed:** λ values, G, the grids, the window tests and the thin-ring rule. No λ outside {0.8, 1.0, 1.2}. No other rotation generator. G = diag(0, 1, 0) is one representative U(1) inside U(3)_{C+F}, chosen now; other U(1)s (e.g. diag(1, −1, 0)) would be a new pre-registration.
- **Model units only.** No particle identification. The SU(3)_{C+F} charge is not electric charge.
- **Classical only.** The CP² worldsheet gap is a quantum effect and is outside this test (B1 §2).

## 6. Amendment A (November 3, 2026, after `REPORT_B2B3.md`, before any verification run or B4)

**Label: post-hoc.** Written after reading `REPORT_B2B3.md` (head 4edfd90). It adds verification and robustness checks only. It changes no B2/B3 verdict: λ = 1 stays WINDOW under the literal §3 rule. What it decides is whether that WINDOW is **confirmed**, which is the condition for writing a B4 pre-registration.

### A.1 Clarifications flagged by the report

- **Two I's.** §3's I (the inertia in q²/(4I)) equals π × the C5 I. No verdict depends on this, because 𝒯 was computed from ℰ directly. From here on: **I_C5** is the dimensionless worldsheet factor (1 at BPS), and **I_q** = π·I_C5·(4 sin²α cos²α) is the inertia in ℰ.
- **n and Q along the R ray.** The sign of d²E/dR² does not depend on n (report, ambiguity (b)). For anything that uses R_eq, fix n = the smallest integer with R_eq/r_q ≥ 3, where R_eq = n/k* and r_q is the charge rms radius at the sign change. Then Q = 2πR_eq q*.

### A.2 Why the WINDOW needs verifying (from the report)

- ω*/m_bulk = 0.977–0.999: the window sits at the leak threshold.
- 102 of 116 sign changes use one-sided k differences. Only 14 are central (k* = 0.287–0.300, q* = 23.5–24.8, ω*/m ≈ 0.981).
- The margin is small. At the representative point (k, q) = (0.30, 24.0), 𝒯_fd/ℰ = −0.0024.
- The radial scan used r_max = 20 with a Dirichlet edge (h(r_max) = 1). That could hold charge in near threshold.
- The radial reduction was checked against 2D at ω ≈ 0.44 only.
- It appears only at λ = 1, the fine-tuned BPS point.

### A.3 Verification runs (fixed now)

**Point set S.** The 14 central sign changes, plus four edge sign changes:
- the lowest-ω* stable one (k* = 0.258, q* = 29.1),
- the three with the largest k*.

For each, recompute its two bracketing grid points and all the neighbours its 𝒯 stencil uses. Warm-start from the original solutions, padded with vacuum.

| run | radial grid | purpose |
|---|---|---|
| V1a | r_max = 40, dr = 0.1 | box |
| V1b | r_max = 40, dr = 0.05 | box + resolution; **this is the decisive run** |
| V1c | r_max = 60, dr = 0.05, the single central sign change with the most negative 𝒯 bracket, only | box convergence |
| V2 | 2D lattice, half-width 30, h = 0.125, α fixed at the radial solution's value, at the two bracketing grid points of the V1c sign change | radial reduction at the window |

**Recorded for every recomputed point:** ℰ, T, I_q, ω/m, the leak fraction (band = within 4 of r_max), the charge rms radius, α, and 𝒯. For each sign change in S: whether the 𝒯 sign change persists, and d²E/dR² by direct solve.

### A.4 Confirmation rule (fixed now)

The λ = 1 WINDOW is **CONFIRMED** only if all of these hold:

1. **In V1b**, at least one **central** sign change in S persists: opposite 𝒯 signs at its bracketing points, computed with central differences. It also has d²E/dR² > 0 by direct solve, a leak fraction < 1 %, and ω < m_bulk at both bracketing points.
2. **In V1c**, the selected sign change persists, and its 𝒯 values change by less than |𝒯| itself (no sign flip).
3. **In V2**, ℰ at both bracketing points agrees with V1b to within 1e-3 relative, and 𝒯 has the same sign at both.

Otherwise the result is **NOT CONFIRMED**, and the reason is named: box, resolution, or reduction.

**Descriptive trend to report.** Whether the charge rms radius and I_q grow with r_max at fixed (k, q). If they do, the charge is delocalizing into the bulk.

### A.5 Robustness, post-hoc and descriptive only (cannot select a point)

All on the V1a grid (r_max = 40, dr = 0.1):
- **V3a.** λ ∈ {0.9, 1.1}, k ∈ {0.20, 0.25, …, 0.50}, q from 0 in steps of 0.1 until the window closes or q = 40.
- **V3b.** λ = 0.8, k ∈ {0, 0.05, …, 0.25}, q extended from 30 to 60.
- **Reported for each:** stable sign changes (count, k*, q*, ω*/m), or none.
- **Classification:**
  - **BPS-only** if no stable sign change at λ = 0.9 or 1.1.
  - **Range** if there is one at both.
  - **One-sided** otherwise.

**Neither V3 run feeds into the A.4 confirmation rule or into any later selection.**

### A.6 Predictions and consequences (written now)

| | Prediction | Prior |
|---|---|---|
| A-P1 | CONFIRMED | about 40 % |
| A-P2 | Charge rms radius and I_q change by < 5 % from r_max 20 to 40 at the 14 central points (the leak at (0.30, 24) is already 4 × 10⁻⁵) | about 70 % |
| A-P3 | V3a: BPS-only | about 50 % |

**What follows.**
- **CONFIRMED.** A B4 pre-registration is written before any loop code. It fixes in advance: a selection rule among confirmed sign changes, n from A.1, and the passenger control (the cheapest charged bulk lump at the same Q, no string). The V3 classification is carried into B4's caveats.
- **NOT CONFIRMED.** Route B's intrinsic vorton (B-i) closes at thin-ring level in this model, and the record says why (threshold, box, resolution or reduction). B4 is not run.

### A.7 Eddington guard

- No new λ is used for selection. λ = 0.9 and 1.1 are descriptive robustness only.
- G, the window tests, the 𝒯 and d²E/dR² machinery, and the B2 calibration are unchanged. No retuning.
