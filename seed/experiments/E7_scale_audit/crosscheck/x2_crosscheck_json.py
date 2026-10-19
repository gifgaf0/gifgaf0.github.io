#!/usr/bin/env python3
"""E7 cross-check: assemble crosscheck.json from the x2 comparison table, the first-pass
cross-check (cc_*), the issues and the claim audit.  Run last (see run_crosscheck.sh)."""
import json
import os

T = json.load(open("x2_compare_table.json"))
CC = json.load(open("cc_crosscheck.json")) if os.path.exists("cc_crosscheck.json") else None

issues = [
    dict(severity="major",
         description="Demidov-Levkov two-particle exponent at high energy is misread: E7 hard-codes F = 3.93 "
                     "(e7_audit.py, 'F2 = 3.93', an eye reading of arXiv:1103.0013 Fig. 3b) with a stated "
                     "+-0.05 reading uncertainty. Pixel digitisation with the axes calibrated on the tick marks "
                     "(4.4/4.2/4.0 ticks at 111 px spacing at 600 dpi; x ticks 7..11 at 166.5 px) gives a plateau "
                     "F = 3.845 for g^2E >= 10.5 (3.845 at g^2E = 11.5); the panel's left edge reads g^2E = 6.240 "
                     "= 2 g^2 M_S, which validates the calibration. Two independent digitisations (first pass 3.846, "
                     "this pass 3.845) agree. The error (-0.085) is outside the stated tolerance and propagates "
                     "into six more headline numbers: kappa 0.63 -> 0.62, g^2 for P = 0.1/1/e/0.5 = 1.71/3.93/5.67 "
                     "-> 1.67/3.84/5.55, M_S/m at P = 0.1: 1.83 -> 1.87, and the illustrative 10^-234 -> 10^-229. "
                     "No conclusion or seed verdict changes.",
         suggested_fix="Use F = 3.85 (plateau) and 4.48 (threshold) in e7_audit.py, results.json, "
                       "fig_vacuum_pairs.png, REPORT.md and the summary; state the reading uncertainty as about "
                       "+-0.01 for a tick-calibrated digitisation."),
    dict(severity="major",
         description="Hopfion energy-rms radius is wrong: R_rms = 2.144 (Ward units) should be 2.0608. "
                     "Cause (found in e7_hopfion.py after the comparison): the profile is a 24-node not-a-knot "
                     "cubic spline in t = r/(1+r) with f(t=1) = 0 but free slope, so f ~ a/r at large r; then "
                     "int r^2 eps d^3r diverges linearly and is cut off by the last Gauss node. My direct 3D "
                     "evaluation with the exact optimal profile f(r) = F_Skyrme(sqrt2 r) gives 2.060816 at four "
                     "resolutions and two radial maps; adding an a/r tail with a = 2e-3 moves R_rms to 2.10-2.13 "
                     "(map dependent) while E_W changes by < 1e-6, which reproduces the mechanism. Consequences: "
                     "hopfion c0 = 341 to 567 (not 590), electron g^2 = 1/kappa4 >= 1.2e9 to 2.0e9 (not 2.1e9), "
                     "sqrt(kappa2) = 82.9 MeV (not 84.5). Energy and ring radius are unaffected. No conclusion changes.",
         suggested_fix="Impose f ~ C/r^2 in the spline (e.g. fit f(t)/(1-t)^2) or use f(r) = F_Skyrme(sqrt2 r); "
                       "report R_rms = 2.061, c0 = 341-567, g^2 >= 1.2-2.0e9."),
    dict(severity="minor",
         description="Hopfion 'CALIBRATED' is not an independent calibration: for the hedgehog-Hopf ansatz the "
                     "angle-averaged Faddeev-Skyrme energy of f(r) is exactly (1/(3 pi^2)) x the ANW hedgehog "
                     "functional of F(x) = f(x/sqrt2), so E_W(ansatz) = a1/(3 pi^2) = 1.2314457 identically "
                     "(confirmed by my 3D quadrature to 2e-8). The '<= 5% above 1.204' tolerance was set by the "
                     "original agent; PLAN has no E7 hopfion target, and E8's preregistered 2% would not pass (2.3%).",
         suggested_fix="Label it 'variational upper bound, consistent with 1.204-1.22' (no CALIBRATED)."),
    dict(severity="minor",
         description="Proton M R/hbar c labelled CALIBRATED against PLAN's '~2.8', which is a PLAN expectation, "
                     "not a literature target, with a tolerance (+-0.05) chosen by the original agent. PLAN's own "
                     "formula c0/e^2 gives 2.598, outside that band; the pass relies on M_N = 939 MeV x classical "
                     "radius (2.826). The model radius is the isoscalar radius, while the data value 3.998 uses the "
                     "proton charge radius (which diverges in the massless-pion Skyrme model), so the comparison "
                     "is indicative only.",
         suggested_fix="Report 2.60 (classical) and 2.83 (M_N) as CONFIRMED for PLAN's expectation 'classical "
                       "fold, ~2.8', not CALIBRATED."),
    dict(severity="minor",
         description="The QED illustration 'a fold-like exp(-F/alpha) factor would be about 10^-234' depends on "
                     "identifying DL's g^2 with alpha. With the loop-counting coupling of QED in the same "
                     "normalisation, g^2 = e^2 = 4 pi alpha, it is 10^-18.6 (10^-18.2 with F = 3.85). e7_audit.py "
                     "computes both and the figure marks 4 pi alpha, but the report and summary quote only 10^-234. "
                     "The qualitative point (QED pair production is perturbative, not fold-like) holds either way.",
         suggested_fix="Quote both identifications (10^-229 for g^2 = alpha, 10^-18 for g^2 = 4 pi alpha), or only "
                       "the 4 pi alpha one."),
    dict(severity="minor",
         description="Pairs: the PLAN-specified combination with E1e can now be made (E1 finished after E7 ran). "
                     "E1's smallest classical producer reproduced at dx = 0.05 has N_lin lambda/m^2 = 1.688, i.e. "
                     "g^2 N_min(phi^4) <= 3.38 = 2.53 N_pair (g^2 = 2 lambda/m^2); N = 2 quanta needs g^2 >= 1.69 "
                     "(lambda/m^2 >= 0.84). This corroborates the DL-based estimate (P = 0.1 at g^2 = 1.67). "
                     "Separately, 'unsuppressed for g^2 >~ 1.7-5.7' extrapolates the leading semiclassical exponent "
                     "exp(-F/g^2) to g^2 = O(1), where prefactors and higher orders are uncontrolled; indicative only.",
         suggested_fix="Add the E1e numbers to the Pairs section and drop deviation 1 or mark it superseded; "
                       "call the thresholds indicative."),
    dict(severity="minor",
         description="Small inconsistencies: (a) the floor for E_rot <= 0.1 M is 2.3947, printed 2.40 in the "
                     "results.json note and 2.39 in the report; (b) lambda_C/R and the vacuum ratios are QUANTIFIED "
                     "in results.json but NO_TARGET in the summary; (c) 'c0 stays >= 52 with any pion mass' holds for "
                     "the baryon-rms radius only: with the half-baryon radius c0 falls to 47.3 at beta = 16 "
                     "(c0_half_min in results.json, not mentioned in the report); (d) the floor 0.757 is for the "
                     "baryon-rms radius (0.627 with the half-baryon radius).",
         suggested_fix="Harmonise rounding and labels; state the radius definition with each floor and pion-mass number."),
    dict(severity="minor",
         description="The LEP bound r_e < 1.1e-19 m (Schael et al. 2013, Eq. 3.9) is model dependent: it is the "
                     "VV contact-interaction scale with positive interference and electromagnetic coupling strength "
                     "converted to a size. The report quotes it without this qualifier.",
         suggested_fix="Add the qualifier where the bound is introduced."),
    dict(severity="minor",
         description="Unlisted deviation: PLAN says 'compute c0 from the E2 profile'; E7 solved its own hedgehog. "
                     "It agrees with E2's profile.json (a1 = 36.46164562524, Lambda = 50.97873911, C = 8.6385782) "
                     "to <= 1e-9, so the effect is nil.",
         suggested_fix="List it among the deviations."),
    dict(severity="minor",
         description="Generalisation wording: the scaling statement M R = c0/(g^2 hbar) is a theorem for theories "
                     "with one length and one overall coupling; with extra dimensionless parameters c0 can move, and "
                     "only the pion-mass family and the hopfion were tested. What is fully general is the "
                     "semiclassical criterion (action per light-crossing ~ M R c >> hbar, i.e. R >> lambda_C); the "
                     "corollary 'needs g^2 >> 1' requires c0 >~ O(1). The report's General statement says this, but "
                     "the seed-claim text ('this holds for any soliton with action S0/g^2') is broader.",
         suggested_fix="Qualify the seed-claim sentence: 'for any one-scale soliton family; two-parameter families "
                       "tested (pion mass, hopfion) keep c0 >= 47'."),
]

claims = [
    ("Skyrme a1 = 36.4616 F_pi/e, Lambda = 50.979 (CALIBRATED vs PLAN E2 targets)", "supported",
     "Three independent codes (original collocation, first-pass Ritz spectral, this pass's shooting) agree to <= 1e-9; "
     "also equal to E2's numbers."),
    ("ANW radii 0.594 fm and 0.922 fm vs 0.59 and 0.92; own fit F_pi = 129.26 MeV, e = 5.4446", "supported",
     "Reproduced to 1e-9. ANW targets are via secondary sources (as PLAN says)."),
    ("c0 = 77.16 (baryon rms), 63.9-119.8 across radius definitions", "supported", "Reproduced to 1e-9."),
    ("With a pion mass c0_B falls only to 52.1 at beta = 16 (plateau)", "supported",
     "Reproduced to 1e-10 at beta = 0.5...16; holds for the baryon-rms radius (half-baryon: 47.3)."),
    ("Proton M R/hbar c = 2.826 CALIBRATED (target ~2.8 +- 0.05)", "overstated",
     "Number right; CALIBRATED misused (PLAN expectation, self-set band); classical c0/e^2 = 2.598 misses the band."),
    ("Data r_p/lambda_C = 3.998", "supported", "PDG 2026 r_p = 0.84075 fm, m_p = 938.272 MeV."),
    ("Electron lambda_C/R >= 3.51e6 (LEP), 3.86e5 (SEED 1e-3 fm)", "supported",
     "Arithmetic reproduced; LEP Eq. (3.9) read: 1.1e-19 m, model dependent (VV, positive interference)."),
    ("Electron Skyrme fold needs e >= 1.65e4 (1.50-2.05e4), F_pi = 231 MeV; E_rot/M = 7.1e12, hbar/(MR) = 3.5e6, "
     "e^2/16pi^2 = 1.7e6", "supported", "Reproduced via MeV-level route (I1, M at each e, F_pi) to 1e-9."),
    ("Semiclassical floor (MR)_min = 0.757 (E_rot <= M), 2.39 (E_rot <= 0.1 M); electron 2.66e6 below", "supported",
     "Reproduced by root-finding; baryon-rms definition (0.627 with half-baryon radius)."),
    ("Hopfion E_W(ansatz) = 1.2314, CALIBRATED as upper bound of 1.204-1.22", "overstated",
     "Value right (direct 3D evaluation), but it is identically a1/(3 pi^2), i.e. not an independent calibration; "
     "tolerance self-set."),
    ("Hopfion c0 = 341 to 590; electron needs 1/kappa4 >= 1.2e9 to 2.1e9", "wrong",
     "Upper ends wrong: R_rms = 2.061 not 2.144, so c0 = 341-567 and g^2 >= 1.2-2.0e9 (spline tail artefact)."),
    ("DL model 2 g^2 M_S = 6.236 (CALIBRATED vs axes)", "supported",
     "Quadrature reproduced to 1e-15; Fig. 3b left edge digitised at 6.240."),
    ("DL exponent F = 4.45 (threshold) to 3.93 (high energy), +-0.05", "wrong",
     "Threshold 4.48 is within tolerance; the plateau is 3.845, 0.085 below the quoted value."),
    ("DL classical g^2 N_min = 3.98 at high energy", "supported", "Digitised 3.977 (Fig. 7b, tick calibrated)."),
    ("P ~ exp(-(0.63-0.71) N_pair); unsuppressed (P >= 0.1-0.5) only for g^2 >= 1.7-5.7, M_S <= 1.8 m", "overstated",
     "Corrected: kappa = 0.62-0.72, g^2 >= 1.67-5.55, M_S <= 1.87 m; leading-exponent extrapolation, indicative only."),
    ("Breit-Wheeler peak 0.682 pi r_e^2 = 170 mb at sqrt(s) = 1.40 x 2 m_e", "supported", "Reproduced."),
    ("A fold-like exp(-F/alpha) would be ~1e-234", "overstated",
     "1e-229 with F = 3.85; convention dependent (1e-18 with g^2 = 4 pi alpha). Conclusion unaffected."),
    ("rho_L = 2.515e-47 GeV^4 = (2.2395 meV)^4, 2.6% uncertainty; Lambda/m_Pl^2 = 2.8445e-122 vs 2.846e-122",
     "supported", "Recomputed from SI constants; Planck 2018 Eqs. (14)-(15) and Table 2 read."),
    ("Ratios f_pi^4 2.86e42, v^4 1.46e56, Higgs depth 4.7e54, M_Pl^4 8.83e122 / 1.40e120 (reduced)", "supported",
     "Reproduced (f_pi ratio to 2e-4 because of 92.065 vs 92.07 MeV)."),
    ("Weinberg-Witten: no massless |h| > 1 with covariant conserved T; no charged |h| > 1/2 with covariant J; "
     "composite graviton excluded, neutral composite photon allowed", "supported",
     "Standard statement, consistent with PLAN section 3 item 8; helicity table correct."),
    ("Scaling: M R = c0/(g^2 hbar); semiclassical <=> R >> lambda_C", "supported",
     "Correct for one-scale theories; see the wording issue on 'any soliton'."),
    ("Solver accuracy (shooting and collocation slopes agree to 7e-9; X-scan <= 1e-6)", "supported",
     "My shooting slope 1.00376411061 equals the collocation value to 1e-12."),
    ("SEED 8: proton is a classical fold -> CONFIRMED", "supported", "Model 2.6-2.8, data 4.0."),
    ("SEED 8: electron misses by >= 1e5 -> AMENDED (3.5e6)", "supported", "Matches PLAN section 3 item 3."),
    ("SEED 8: electron-like fold needs strong coupling -> CONFIRMED; 'like baryons in QCD' -> AMENDED", "supported",
     "Numbers reproduced (Skyrme corrections 1e6-1e13; hopfion needs g^2 >= 1.2e9)."),
    ("SEED 8: few-quanta pair folding exponentially rare at weak coupling -> CONFIRMED", "supported",
     "DL (corrected F) plus scaling; E1e now corroborates for phi^4 (g^2 N_min <= 3.38)."),
    ("SEED 8: 'electron pairs form readily, so the fold sector is strongly coupled' -> AMENDED", "supported",
     "Defensible: QED pair creation is perturbative (sigma ~ alpha^2), so this inference does not hold as stated; "
     "the strong-coupling conclusion survives only via the size argument. REFUTED (for the inference) would also be defensible."),
    ("SEED 8 vacuum tension -> QUANTIFIED; Weinberg-Witten -> AMENDED; SEED 2 one cone -> OPEN", "supported", ""),
    ("Figures fig_scale.png and fig_vacuum_pairs.png exist and match the text", "supported",
     "Both present (100 KB, 74 KB); the pairs panel uses F = 3.93 and should be redrawn with 3.85."),
]

rows = T["rows"]
key = ["a1 = M_cl/(F_pi/e)", "Lambda", "c0 (B)", "R_B at ANW (fm) [target 0.59 +- 0.01]",
       "proton M R/hbar c (939 MeV x R_B)", "lambda_C/R (LEP)", "e needed (LEP, B)",
       "E_rot/M at electron fold (LEP, B)", "floor (MR)_min, E_rot <= M", "hopfion E_W (ansatz)",
       "hopfion R_rms energy (Ward)", "hopfion c0 (rms)", "DL F high-energy plateau (Fig. 3b, g^2E >= 10.5)",
       "DL g^2 N_min high energy (Fig. 7b)", "rho_Lambda (GeV^4)", "M_Pl unreduced^4/rho_L"]
out = dict(
    experiment="E7 scale and coupling audit (SEED.md section 8) - independent cross-check",
    method=("Second, independent pass (x2_*): own shooting/bisection hedgehog with analytic tails "
            "(+ pion-mass family), direct 3D finite-difference evaluation of the hedgehog-Hopf energy and radii, "
            "Demidov-Levkov quadrature plus tick-mark-calibrated pixel digitisation of arXiv:1103.0013 Fig. 3b and "
            "1103.2133 Fig. 7b, all derived numbers via different routes (MeV-level rotor, root-found floors, SI "
            "vacuum energy). The first-pass cross-check (cc_*, Ritz-spectral hedgehog, hopfion identity) was "
            "re-run from scratch and reproduced its numbers exactly; its results are kept as cc_crosscheck.json."),
    n_compared=T["n_compared"], n_disagree=T["n_disagree"],
    disagreement_root_causes=["DL F plateau misread (3.93 vs 3.845)", "hopfion R_rms spline-tail artefact (2.144 vs 2.061)"],
    key_quantities=[r for r in rows if r["quantity"] in key],
    comparisons=rows,
    extra_independent=T["extra"],
    first_pass_crosscheck=None if CC is None else dict(n_quantities=CC.get("n_quantities"),
                                                      n_disagree=CC.get("n_disagree"),
                                                      overall=CC.get("overall"),
                                                      reproduced_on_rerun=True),
    issues=issues,
    claim_audit=[dict(claim=c, verdict=v, note=n) for c, v, n in claims],
    overall="confirmed_with_corrections",
)
json.dump(out, open("crosscheck.json", "w"), indent=1, default=float)
print(f"crosscheck.json written: {T['n_compared']} compared, {T['n_disagree']} disagree, "
      f"{len(issues)} issues ({sum(i['severity'] == 'major' for i in issues)} major), overall {out['overall']}")
