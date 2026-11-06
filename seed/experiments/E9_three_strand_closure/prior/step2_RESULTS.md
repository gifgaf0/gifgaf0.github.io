# Step 2 results: fractional flux and confinement (exploration), October 30, 2026
Pre-registration `PREREG.md` (written before any run). Script `frac.py`, box check `bigbox.py`. Logs: `log0.txt` (η = 0), `log2.txt` (η = 0.02), `big241.txt` and `big321.txt`. Every minimization converged (max gradient ≤ 5×10⁻⁷); total flux is 1.000000 in every run.

| Prediction | Predicted | Found | Verdict |
|---|---|---|---|
| P1: fractional flux | isolated vortex 1/3, remaining pair 2/3 | Within R = 10: 0.2704 and 0.5399. Screening-tail theory, (1/3, 2/3)·[1 − (R/λ)K₁(R/λ)], gives 0.2718 and 0.5435 | **Confirmed** |
| P2: η = 0, log confinement | slope 4π/3 = 4.19 per unit ln d | Slope 16→32: 3.77 (161² box), 3.98 (241²), 4.04 (321²). It rises toward 4.19 as the box grows; the shortfall is a box-edge effect | **Confirmed** (with the finite-size trend shown) |
| P3: η = 0.02, linear confinement | slope ≈ 1.31 | 1.305 (d = 24→32); the slope is constant from d ≈ 12 | **Confirmed** (0.4 %) |

## What this establishes
In a three-component condensate with one gauge field and equal densities:
1. **Flux comes in thirds.** A vortex in one component carries 1/3 of a flux quantum. Only the composite of all three carries a whole quantum.
2. **Pulling one third out costs energy that grows without bound.** It grows as ln d without inter-component coupling, and linearly (a string, tension 1.31 in lattice units) with it. So the thirds are confined, and the free object is the whole-flux composite.

Both results reproduce known results (Babaev 2002; the sine-Gordon wall between fractional vortices). **Nothing here is new physics.** It confirms the route works and the instrument is calibrated.

## Limits
- **2D, London limit.** Amplitudes are fixed and vortex cores are cut off by the lattice spacing. The d-dependence is meaningful; the core constants are not.
- **η is an input.** The linear string exists only if inter-component phase locking exists. Whether something forces η > 0 is open; it is the E3 question for this route.
- **Equal densities were assumed.** Unequal densities give non-third fractions (Step 1).
- **Flux, not electric charge.** See Step 1.
- **Static energies only.** These are the same for the relativistic and non-relativistic versions, so the relativity check I flagged earlier does not bite here. It will matter for dynamics.

## Next (step 3)
A closed composite loop in 3D (the "first stable closure"), with the full Ginzburg–Landau amplitudes. Derrick's theorem says a loop shrinks unless something stabilizes it, so the stabilizer must be declared before computing.
