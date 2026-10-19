#!/usr/bin/env python3
"""Assemble results.json for E6 from out/stage_*.json (run after e6_solve.py and e6_stability.py)."""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def load(n):
    with open(os.path.join(OUT, f"stage_{n}.json")) as fh:
        return json.load(fh)


flat, crit, branch, fixed = load("flat"), load("crit"), load("branch"), load("fixed_alpha")
bvp, bvp4, ep, bm, phys, lin, stab = (load("bvp"), load("bvp_X400"), load("ep"), load("bm"), load("phys"),
                                     load("linear_metric"), load("stability"))
best = crit["runs"][2]
ac = best["alpha_crit"]
E2_value = 2 * 36.46164562523657           # E2 results.json M_cl in F_pi/e (186-MeV convention) -> f/e
E_flat = 4 * math.pi * flat["m0"]
# free-intercept fit of m(alpha) on the lower branch: intercept vs m0 (M_ADM(alpha->0) = E_flat)
A = np.array([r["alpha"] for r in ep["full"]])
Mfull = np.array([r["m_inf"] for r in ep["full"]])
cfree = np.polyfit(A, Mfull, 4)
intercept = float(cfree[-1])
p64, p92 = phys["f=64.5MeV"], phys["f=92.2MeV"]
spread = max(r["alpha_crit"] for r in crit["runs"]) - min(r["alpha_crit"] for r in crit["runs"])

headline = [
    dict(quantity="alpha_crit (fold of the hedgehog Einstein-Skyrme branch), alpha = 4 pi G f^2, f = F_pi/2",
         value=ac, unit="dimensionless", target=0.040378, tolerance="+-0.0002",
         source="PLAN.md E6 [summary: Zajac 2009; Bizon-Chmaj 1992 convention]",
         verdict="CALIBRATED" if abs(ac - 0.040378) <= 2e-4 else "MISS",
         note=f"maximised over b = -F'(0); spread over h in {{2e-3,1e-3,5e-4}}, x_max in {{1e5,1e6,1e7}}: {spread:.1e}; "
              f"BVP (solve_bvp, X=200/400): {bvp['alpha_crit']:.13f} / {bvp4['alpha_crit']:.13f}. "
              f"Agrees with the target to {ac - 0.040378:+.2e} (target's six digits = ours truncated; rounded ours is 0.040379). "
              f"In the F_pi convention (4 pi G F_pi^2) the fold is at {4 * ac:.6f} (factor 4)."),
    dict(quantity="branch structure", value="two branches (lower from the flat skyrmion, upper towards rescaled "
         "Bartnik-McKinnon) merging at alpha_crit; no solution of this family above it",
         unit="", target="two branches merge at alpha_crit, lower one connects to the flat skyrmion", tolerance="qualitative",
         source="PLAN.md E6", verdict="CALIBRATED",
         note=f"b_crit = {best['b_crit']:.7f}; lower branch b -> {flat['b_flat']:.6f} and m -> m0 as alpha -> 0; "
              f"upper branch sqrt(alpha) m(inf) -> {bm['upper_sqrt_alpha_m_extrap_linear']:.5f} vs Bartnik-McKinnon "
              f"m_BM = {bm['m_BM']:.6f} computed here (b_BM = {bm['b_BM']:.6f})"),
    dict(quantity="flat B=1 energy E_flat = 4 pi (f/e) m0", value=E_flat, unit="f/e", target=E2_value,
         tolerance="0.2%", source="E2 results.json M_cl = 36.4616 F_pi/e = 72.9233 f/e; PLAN 1.2315 x 6 pi^2 = 72.9265",
         verdict="CALIBRATED" if abs(E_flat / E2_value - 1) < 2e-3 else "MISS",
         note=f"rel. diff to E2 {E_flat / E2_value - 1:+.1e}; to 1.2315*6pi^2 {E_flat / (1.2315 * 6 * math.pi**2) - 1:+.1e}; "
              f"virial E2/E4-1 = {flat['virial']:.1e}; m0 = {flat['m0']:.12f}, b_flat = {flat['b_flat']:.12f}"),
    dict(quantity="M_ADM(alpha -> 0) / E_flat (gravitational mass = total energy incl. gradient + Skyrme terms)",
         value=intercept / flat["m0"], unit="", target=1.0, tolerance="1e-6", source="PLAN.md E6 (commitment 5)",
         verdict="CALIBRATED" if abs(intercept / flat["m0"] - 1) < 1e-6 else "MISS",
         note="free-intercept quartic fit of m(inf) on 10 lower-branch solutions, alpha = 2e-4..2e-3. Built into GR "
              "with minimal coupling (m' = 4 pi r^2 rho); a consistency check of the solver, not an independent test."),
    dict(quantity="O(alpha) coefficient m1 of m(inf) = m0 + m1 alpha (units 4 pi f/e): full solutions vs Newtonian "
                  "binding (1/2) int rho Phi with flat rho",
         value=ep["m1_full"], unit="4 pi f/e per unit alpha", target=ep["m1_newton"], tolerance="1% (PLAN prediction)",
         source="PLAN.md E6 equivalence-principle prediction",
         verdict="CALIBRATED" if abs(ep["newton_vs_full_rel"]) < 0.01 else "MISS",
         note=f"Newtonian value is {ep['newton_vs_full_rel']:+.2%} off (magnitude too small). The full slope equals the GR "
              f"first-order mass defect -G int (rho + p_r) m/r dV ({ep['m1_GR_first_order']:.8f}, rel {ep['GR_vs_full_rel']:+.1e}) "
              f"and the linearised-gravity (one-graviton) exchange energy between the full stress tensors "
              f"({ep['m1_linearised_harmonic']:.8f}, rel {ep['lin_vs_full_rel']:+.1e}). Radial stress p_r carries "
              f"{ep['pr_over_rho_weighted']:.4f} of the Newtonian weight. Not a numerical or convention problem."),
    dict(quantity="O(alpha) coefficient: full vs GR first order -G int (rho+p_r) m/r dV (derived here)",
         value=ep["m1_full"], unit="4 pi f/e", target=ep["m1_GR_first_order"], tolerance="1e-6 (internal)",
         source="this work (derivation in REPORT)", verdict="NO_TARGET",
         note=f"rel. diff {ep['GR_vs_full_rel']:.1e}; independent harmonic-gauge exchange formula rel. diff {ep['lin_vs_full_rel']:.1e}"),
    dict(quantity="fold solution: m(inf), M_ADM, sigma(0), N_min", value=dict(
         m_inf=best["m_inf"], M_ADM_f_over_e=4 * math.pi * best["m_inf"], sigma0=best["sigma0"], Nmin=best["Nmin"],
         x_at_Nmin=best["xNmin"], b_crit=best["b_crit"]), unit="x = e f r; M in f/e", target="none", tolerance="",
         source="this work", verdict="NO_TARGET",
         note=f"M_ADM at the fold is {4 * math.pi * best['m_inf'] / E_flat - 1:+.2%} relative to the flat skyrmion"),
    dict(quantity="radial (l=0) stability", value="lower branch: 0 negative modes; upper branch: exactly 1 negative mode",
         unit="", target="literature: upper branch unstable", tolerance="qualitative", source="PLAN.md E6 (literature only)",
         verdict="NO_TARGET",
         note=f"pulsation equation derived with sympy (derive_pulsation.py); lowest omega^2 crosses zero at b = "
              f"{stab['zero_crossing_b']['X=800']:.6f} (fold b_crit = {stab['b_crit']:.6f}); upper-branch omega^2 (units (ef)^2): "
              + ", ".join(f"{r['label']}: {r['omega2_lowest']:+.5f}" for r in stab["rows"] if r["label"].startswith("upper"))),
    dict(quantity="physical coupling alpha_phys (G = 6.70883e-39 GeV^-2, f = 64.5 MeV)", value=p64["alpha"],
         unit="dimensionless", target=3.5e-40, tolerance="rounding (2 digits)", source="PLAN.md E6",
         verdict="CALIBRATED" if abs(p64["alpha"] / 3.5e-40 - 1) < 0.015 else "MISS",
         note=f"alpha_phys/alpha_crit = {p64['alpha_over_alpha_crit']:.2e}; f = 92.2 MeV: alpha = {p92['alpha']:.4e}"),
    dict(quantity="metric deviation at the fold core, f = 64.5 MeV, e = 5.45", value=dict(
         one_minus_sigma_centre=p64["oneminus_sigma_core"], one_minus_gtt_centre=p64["oneminus_gtt_core"],
         one_minus_N_max=p64["oneminusN_max"], r_of_max_fm=p64["r_at_oneminusN_max_fm"],
         one_minus_N_1fm=p64["oneminusN_1fm"], one_minus_sigma_1fm=p64["oneminus_sigma_1fm"]),
         unit="dimensionless", target="of order 1e-39", tolerance="order of magnitude", source="PLAN.md E6",
         verdict="NO_TARGET", note="consistent with the PLAN's order-of-magnitude expectation; 1 - N vanishes at r = 0 "
                                    "(m ~ r^3), so the core value quoted is the maximum of 1 - N and the centre value of 1 - sigma"),
    dict(quantity="metric deviation, f = 92.2 MeV, e = 5.45", value=dict(
         one_minus_sigma_centre=p92["oneminus_sigma_core"], one_minus_N_max=p92["oneminusN_max"],
         one_minus_N_1fm=p92["oneminusN_1fm"], one_minus_sigma_1fm=p92["oneminus_sigma_1fm"]),
         unit="dimensionless", target="none", tolerance="", source="this work", verdict="NO_TARGET", note=""),
    dict(quantity="light deflection through/near a fold (weak field, linear in alpha)", value=dict(
         f64_max_rad=p64["deflection_max_rad"], f64_b_at_max_fm=p64["b_at_deflection_max_fm"],
         f64_at_1fm_rad=p64["deflection_1fm_rad"], f64_pointmass_at_1fm_rad=p64["pointmass_deflection_1fm_rad"],
         f92_max_rad=p92["deflection_max_rad"], f92_at_1fm_rad=p92["deflection_1fm_rad"]),
         unit="rad", target="none (tiny)", tolerance="", source="this work", verdict="NO_TARGET",
         note=f"per unit alpha: max {phys['per_alpha']['deflection_max']:.4f} at b = {phys['per_alpha']['b_at_max']:.3f} (x units); "
              f"-> 4 m0/b at large b (point mass, M = M_ADM)"),
    dict(quantity="Shapiro delay along a diameter, -1 fm to +1 fm", value=dict(
         f64_s=p64["shapiro_chord_pm1fm_s"], f92_s=p92["shapiro_chord_pm1fm_s"], f64_GM_over_c3_s=p64["GM_over_c3_s"]),
         unit="s", target="none (tiny)", tolerance="", source="this work", verdict="NO_TARGET",
         note="chord delay = int (h_00 + h_zz)/2 dz; beyond the fold it grows like 4GM ln(path) as for any mass"),
]

seed_claims = [
    dict(claim="SEED 7.5: a self-gravitating fold (skyrmion) exists", verdict="CONFIRMED",
         evidence=f"regular, asymptotically flat B=1 solutions exist for 0 <= alpha <= {ac:.10f}; physical alpha is {p64['alpha_over_alpha_crit']:.1e} of that"),
    dict(claim="SEED 2/5: equivalence principle -- the fold's gravitational mass is its total energy (gradient and Skyrme terms included)",
         verdict="CONFIRMED", evidence=f"M_ADM(alpha->0)/E_flat = {intercept / flat['m0']:.12f} (built in by minimal coupling)"),
    dict(claim="Commitment 5 'energy bends the cone' read as Newtonian binding -1/2 int rho Phi (PLAN E6 prediction)",
         verdict="AMENDED",
         evidence=f"the O(alpha) mass defect is {ep['m1_full'] / ep['m1_newton']:.4f} x the Newtonian one; stresses gravitate: "
                  f"-G int (rho+p_r) m/r dV reproduces it to {abs(ep['GR_vs_full_rel']):.0e}"),
    dict(claim="SEED 5: light bends and is delayed around a mass (optical index 1 + 2GM/r)", verdict="CONFIRMED",
         evidence="deflection -> 4 G M_ADM/b outside the fold (checked at b = 50/(ef) to 1e-5); reduced inside the core"),
    dict(claim="Gravity's effect on a single fold at the physical coupling (scale gap)", verdict="QUANTIFIED",
         evidence=f"1 - sigma(0) = {p64['oneminus_sigma_core']:.2e}, max(1 - N) = {p64['oneminusN_max']:.2e} (f = 64.5 MeV); "
                  f"deflection <= {p64['deflection_max_rad']:.1e} rad"),
]

res = dict(experiment="E6 -- a fold with gravity (hedgehog Einstein-Skyrme)",
           conventions="L = (f^2/4) Tr(dU dU^dag) + 1/(32 e^2) Tr[U^dag dU, U^dag dU]^2 (mostly-minus form), f = F_pi/2; "
                       "ds^2 = -sigma^2 N dt^2 + dr^2/N + r^2 dOmega^2, N = 1 - 2 G M(r)/r; x = e f r, alpha = 4 pi G f^2; "
                       "N = 1 - 2 alpha m(x)/x, M_ADM = 4 pi (f/e) m(inf); F(0) = pi, F ~ C/x^2, sigma(inf) = 1; massless pions",
           headline=headline, seed_claims=seed_claims,
           details=dict(alpha_crit_runs=crit["runs"], alpha_crit_richardson=crit["richardson_rk4"],
                        observed_order_rk4=crit["observed_order"], bvp=[bvp, bvp4], flat=flat,
                        ep={k: v for k, v in ep.items()}, ep_free_intercept_fit=cfree.tolist(), bartnik_mckinnon=bm,
                        physical=phys, linear_metric=lin,
                        stability={k: v for k, v in stab.items()},
                        fixed_alpha=fixed["rows"]))
with open(os.path.join(HERE, "results.json"), "w") as fh:
    json.dump(res, fh, indent=1)
for h in headline:
    v = h["value"]
    print(f"{h['verdict']:11s} {h['quantity'][:80]:80s} {v if not isinstance(v, float) else f'{v:.10g}'}")
print("intercept/m0 - 1 =", intercept / flat["m0"] - 1)
