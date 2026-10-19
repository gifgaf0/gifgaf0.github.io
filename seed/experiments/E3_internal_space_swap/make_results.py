#!/usr/bin/env python3
"""
E3: collect the part results into results.json, compare with E2's profile (read only at the
end, as allowed by the plan), and draw the spectrum figure.
"""
import json
import os
import numpy as np

J = lambda f: json.load(open(f))
alg, hh, ine, rep = J("algebra_results.json"), J("hedgehog_results.json"), J("inertia_results.json"), J("reps_results.json")
stab = J("stability_results.json") if os.path.exists("stability_results.json") else None
refine = J("stability_refine_results.json") if os.path.exists("stability_refine_results.json") else None
su3br = J("su3_branching_results.json") if os.path.exists("su3_branching_results.json") else None
flag = J("flag_results.json") if os.path.exists("flag_results.json") else None

H = []


def head(quantity, value, target, tolerance, verdict, note, units="", source=""):
    H.append(dict(quantity=quantity, value=value, units=units, target=target, tolerance=tolerance,
                  source=source, verdict=verdict, note=note))


di = alg["dynkin_indices"]
head("Dynkin indices of SU(2) subgroups of G2 (long, short, A1^4, principal)",
     [round(di["long_root"], 10), round(di["short_root"], 10), round(di["diag_long_x_short"], 10), round(di["principal"], 10)],
     [1, 3, 4, 28], "exact (|dev| < 1e-9)", "CALIBRATED" if np.allclose(
         [di["long_root"], di["short_root"], di["diag_long_x_short"], di["principal"]], [1, 3, 4, 28], atol=1e-9) else "MISS",
     "index = -Tr_7(T3 T3) for standard su(2) generators; long root = 1. The SO(3) in SU(3) also has index 4. "
     "Confirmed again by the baryon number of the embedded hedgehogs: B = 1, 3, 4, 4, 28.",
     source="Mayanskiy arXiv:1611.04070 Table 2 [read]")
head("14 under SU(2)_L x SU(2)_S", alg["branching_14"], {"(3,1)": 1, "(1,3)": 1, "(2,4)": 1}, "exact",
     "CALIBRATED" if alg["branching_14"] == {"(1,3)": 1, "(2,4)": 1, "(3,1)": 1} else "MISS",
     "from explicit 14x14 adjoint matrices", source="Mayanskiy Prop. 4.1 [read]")
head("7 under SU(2)_L x SU(2)_S", alg["branching_7"], {"(2,2)": 1, "(1,3)": 1}, "exact",
     "CALIBRATED" if alg["branching_7"] == {"(1,3)": 1, "(2,2)": 1} else "MISS",
     "from the 7x7 generators; PLAN 'expected' (derived, not literature)", source="PLAN.md E3 (expected)")
head("Casimirs C2(7), C2(14) in long-root normalisation", [alg["C2_7_numeric"][0], alg["C2_14_numeric"][0]], [2, 4], "exact",
     "CALIBRATED" if np.allclose([alg["C2_7_numeric"][0], alg["C2_14_numeric"][0]], [2, 4]) else "MISS",
     "C2 = -sum_a T_a T_a over a basis orthonormal in B = -Tr_7; equals (lambda, lambda+2 rho) with long roots of length^2 1",
     source="PLAN.md E3")
f = hh["final"]
head("Hedgehog mass M_cl", f["M"], 1.2315 * 3 * np.pi**2, "0.2%", "CALIBRATED" if abs(f["M"] / (1.2315 * 3 * np.pi**2) - 1) < 0.002 else "MISS",
     f"own two-sided shooting solver; E2=E4 to {abs(hh['virial_E2_minus_E4_rel']):.0e}", units="F_pi/e",
     source="PLAN.md E2 target (Schechter-Weigel, Praszalowicz) [read]")
head("Lambda (I1 = (2 pi/3) Lambda/(e^3 F_pi))", f["Lambda"], 50.9, "0.5%", "CALIBRATED" if abs(f["Lambda"] / 50.9 - 1) < 0.005 else "MISS",
     "ANW quote 50.9; ours 0.15% higher (the exact-profile value is 50.979)", source="ANW via PLAN.md E2")
head("I2 (strange/kaon moment of inertia)", f["I2_radial"], 40.5, "within 1.5% of the arctan-ansatz value",
     "CALIBRATED" if abs(f["I2_radial"] / 40.5 - 1) < 0.015 else "MISS", "exact profile 0.44% above the arctan ansatz",
     units="1/(e^3 F_pi)", source="Praszalowicz hep-ph/0308114 (arctan) [read]")
ev = np.array(ine["g2_inertia_eigenvalues_fine"])
head("G2 inertia tensor eigenvalues (3D quadrature, all 14 directions)",
     {"I1 (x3)": ine["I1_3d"], "I2 (x8)": ine["I2_3d"], "zero (x3)": ine["short_block_max_abs"]},
     {"I1": f["I1"], "I2": f["I2_radial"], "zero": 0}, "1e-6 relative; zero block < 1e-10",
     "CALIBRATED" if all(ine["checks"].values()) else "MISS",
     "eigenvalue multiplicities 3, 8, 3 = (3,1), (2,4), (1,3); I1 equals the SU(2) value, I2 the SU(3) strange value "
     f"(rel. diff {abs(ine['I2_3d']/f['I2_radial']-1):.1e}); the SU(3) directions in G2 with Tr_7/2 equal the 3x3 SU(3) result "
     f"to {ine['su3_vs_g2_max_diff']:.0e}", units="1/(e^3 F_pi)", source="PLAN.md E3 (expected)")
st_ = rep["states"]
low = [(s["R"], int(s["J"])) for s in st_[:6]]
head("Lowest G2 rotor states (R, J)", low, "1 (J=0), then 14 (J=1); 7 not allowed", "exact",
     "CALIBRATED" if low[:2] == [("1", 0), ("14", 1)] and not rep["seven_allowed"] else "MISS",
     "states = G2 irreps R with a right SU(2)_short singlet; J from right SU(2)_long", source="PLAN.md E3 (seed prediction)")
head("All allowed J integer (irreps up to dim 500)", rep["all_allowed_J_integer"], True, "exact",
     "CALIBRATED" if rep["all_allowed_J_integer"] else "MISS",
     "reason: in every G2 irrep jL + jS is an integer (exp(2 pi T3^L) = exp(2 pi T3^S) in G2)", source="SEED.md section 2")
anw = rep["parameter_points"]["ANW (F_pi=129, e=5.45)"]
refit = rep["su3_refit"]
e14 = [s for s in st_ if s["R"] == "14"][0]
head("G2 fold: E(14, J=1) - E(1, J=0) at ANW parameters", e14["Exc_MeV ANW (F_pi=129, e=5.45)"], None, None, "NO_TARGET",
     f"= 1/I1 + 1/I2; M_cl = {anw['M']:.1f} MeV, 1/I1 = {anw['inv_I1']:.1f} MeV, 1/I2 = {anw['inv_I2']:.1f} MeV", units="MeV")
head("SU(3) refit point (fitted inputs)", {"F_pi": refit["F_pi"], "e": refit["e"]}, {"F_pi": 114, "e": 5.25},
     "PLAN 'roughly'", "NO_TARGET",
     f"fit of the N_c=3 SU(3) rotor to octet {refit['octet_centre_MeV']:.1f} and decuplet {refit['decuplet_centre_MeV']:.1f} MeV "
     f"({refit['source']}); antidecuplet {refit['antidecuplet_MeV']:.0f} MeV", units="MeV, -")
if stab is not None:
    mins = stab["min_eigenvalue_per_block"]
    head("Embedded hedgehog in G2: lowest Hessian eigenvalue per block (Ritz, box R)", mins, ">= 0", "> -1e-6",
         "NO_TARGET", "no negative mode found; lowest values are box-limited continuum / zero modes", units="(F/e) units, L2 metric")
if refine is not None:
    tr = {sec: {nr: round(min(v), 8) for nr, v in d.items()} for sec, d in refine.items() if isinstance(d, dict)}
    head("Hessian: lowest eigenvalue vs radial mesh (R = 20, lmax = 3)", tr, "-> 0+ (zero modes), never negative", "> -1e-6",
         "NO_TARGET", "the box/mesh-limited zero modes fall with refinement; no negative eigenvalue appears",
         units="(F/e) units, L2 metric")
if flag is not None:
    mmap = flag["moment_map"]
    gen = mmap["generic a=(1, 0.3, -1.3)"]
    deg = mmap["degenerate a=(1, 1, -2)"]
    head("Moment map image of the SU(3) orbit through diag(a)",
         {"generic: vertices": gen["n_vertices"], "angles_deg": [round(x, 9) for x in gen["interior_angles_deg"]],
          "hull/hexagon area at N=1e6": gen["convergence"][-1]["hull_area_over_polygon_area"],
          "degenerate: vertices": deg["n_vertices"]},
         "hexagon (120 deg angles, alternating sides); triangle when two eigenvalues coincide", "exact geometry; all samples inside",
         "CALIBRATED" if gen["n_vertices"] == 6 and deg["n_vertices"] == 3 and all(c["all_inside"] for c in gen["convergence"]) else "MISS",
         "Schur-Horn", source="PLAN.md E3 (Schur-Horn)")
    p2 = flag["pi2_charges"]
    head("pi_2(F2) charges of explicit maps", {k.split(":")[0]: [round(q, 8) for q in v["continuum_96x192"]] for k, v in p2.items()},
         {k.split(":")[0]: v["expected"] for k, v in p2.items()}, "integers to 1e-6 (continuum), exact (lattice)",
         "CALIBRATED" if all(v["pass_"] for v in p2.values()) else "MISS", "(Q1,Q2,Q3), Q1+Q2+Q3=0; A and B generate Z^2")
    p3 = flag.get("pi3", {})
    if p3:
        vals = {}
        for k, v in p3.items():
            fi = [kk for kk in v if kk.startswith("F2_intrinsic")]
            vals[k.split(" ")[0]] = dict(lift=round(v["lift_degree"], 6), projectors_only=round(v[fi[-1]]["B"], 4) if fi else None,
                                         expected=v["expected"])
        head("pi_3(F2) Hopf-type charge via SU(3) lift", vals, "integers = lift degree", "1e-3 (projector/FFT route)",
             "CALIBRATED" if all(abs(x["lift"] - x["expected"]) < 1e-4 for x in vals.values()) else "MISS",
             "projector-only route uses Coulomb-gauge CS terms + Gamma term (Amari-Sawado eq. 13)",
             source="Affleck-Bykov-Wamer 2101.11638 sec. 1.4; Amari-Sawado 1805.10008 [read]")

# comparison with E2's profile (independent code)
e2p = "/home/user/gifgaf0.github.io/seed/experiments/E2_skyrme_su3/profile.json"
comp = None
if os.path.exists(e2p):
    E2 = J(e2p)
    pr = np.load("profile_e3.npz")
    from scipy.interpolate import CubicHermiteSpline
    s = CubicHermiteSpline(pr["x"], pr["F"], pr["dF"])
    x2 = np.array(E2["x"]); F2 = np.array(E2["F"])
    m = x2 <= 150
    comp = dict(max_abs_dF=float(np.abs(s(x2[m]) - F2[m]).max()),
                M=(f["M"], E2["M_over_Fpi_e"]), Lambda=(f["Lambda"], E2["Lambda"]),
                I2_integral=(f["I2_integral"], E2["J2"]), C=(f["C_tail"], E2["C"]), Fprime0=(f["slope_F'(0)"], E2["Fprime0"]))
    print("comparison with E2 profile.json:", comp)

out = dict(experiment="E3 swap the internal space (G2 and SU(3)/T^2)",
           conventions=dict(skyrme="L = (F^2/16) Tr dU dU^+ + (1/32e^2) Tr[L,L]^2, F_pi 186-MeV convention, x = e F_pi r",
                            g2="Lagrangian with (1/2) Tr_7; basis orthonormal in B = -Tr_7; long-root su(2) generators -i sigma/2",
                            casimir="C2 = (lambda, lambda + 2 rho), long roots |a|^2 = 1: C2(7)=2, C2(14)=4",
                            rotor="E = M + J(J+1)/(2 I1) + [C2(R) - J(J+1)]/(2 I2)",
                            units="I in 1/(e^3 F_pi), M in F_pi/e"),
           headline=H, E2_profile_comparison=comp,
           g2_states=[{k: v for k, v in s.items()} for s in st_ if s["dim"] <= 500],
           g2_irreps=[{k: t[k] for k in ("name", "dim", "dynkin", "C2", "branching", "allowed_J")} for t in rep["irreps"]],
           hedgehog=dict(final=f, ANW=hh["ANW"]),
           inertia=dict(eigenvalues=ine["g2_inertia_eigenvalues_fine"], I1=ine["I1_3d"], I2=ine["I2_3d"],
                        hedgehogs_in_su2_subgroups=ine["hedgehogs_in_su2_subgroups"]),
           su3_refit=refit, parameter_points=rep["parameter_points"],
           stability=stab, stability_refine=refine, g2_to_su3_branching=su3br, flag=flag)
with open("results.json", "w") as fh:
    json.dump(out, fh, indent=1, default=float)
print("results.json written:", len(H), "headline entries")

# ---------------------------------------------------------------- spectrum figure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
i1, i2 = ine["I1_3d"], ine["I2_3d"]
p = anw
u1, u2 = p["inv_I1"], p["inv_I2"]
su3 = [("N (SU(2))", 0.375 * u1, "#888888"), ("Δ (SU(2))", 1.875 * u1, "#888888"),
       ("8, J=½", 0.375 * u1 + 0.75 * u2, "#4C72B0"), ("10, J=3/2", 1.875 * u1 + 0.75 * u2, "#4C72B0"),
       ("10̄, J=½", 0.375 * u1 + 2.25 * u2, "#4C72B0"), ("27, J=½", 0.375 * u1 + 3.25 * u2, "#4C72B0"),
       ("27, J=3/2", 1.875 * u1 + 1.75 * u2, "#4C72B0")]
fig, ax = plt.subplots(figsize=(6.4, 4.6))
def spread(ys, gap=95.0):
    """label positions with a minimum vertical gap (levels themselves are drawn at their true energies)"""
    order = np.argsort(ys)
    out = np.array(ys, float)
    for a_, b_ in zip(order[:-1], order[1:]):
        if out[b_] - out[a_] < gap:
            out[b_] = out[a_] + gap
    return out


for grp in ("SU(2)", "SU(3)"):
    items = [(lab, e, c) for lab, e, c in su3 if ("SU(2)" in lab) == (grp == "SU(2)")]
    x0 = 0.0 if grp == "SU(2)" else 1.0
    ly = spread([p["M"] + e for _, e, _ in items])
    for (lab, e, c), yl in zip(items, ly):
        ax.hlines(p["M"] + e, x0, x0 + 0.7, color=c, lw=2)
        ax.text(x0 + 0.72, yl, lab, va="center", fontsize=7)
g2items = [(f"{s['R']}, J={int(s['J'])}", s["E_MeV ANW (F_pi=129, e=5.45)"]) for s in st_
           if s["dim"] <= 300 and s["E_MeV ANW (F_pi=129, e=5.45)"] <= 3700]
ly = spread([e for _, e in g2items])
for (lab, e), yl in zip(g2items, ly):
    ax.hlines(e, 2.4, 3.1, color="#C44E52", lw=2)
    ax.text(3.12, yl, lab, va="center", fontsize=7)
ax.set_xticks([0.35, 1.35, 2.75])
ax.set_xticklabels(["SU(2)\n(FR sign)", "SU(3), N_c=3\n(WZ term: fermions)", "G$_2$\n(no WZ term: bosons)"], fontsize=8)
ax.set_xlim(-0.1, 3.9)
ax.set_ylabel("rotor energy E (MeV) at F$_\\pi$=129 MeV, e=5.45")
ax.set_title("B = 1 fold: rigid-rotor multiplets for three internal spaces", fontsize=9)
ax.axhline(p["M"], color="k", lw=0.5, ls=":")
ax.text(3.85, p["M"] + 20, "M$_{cl}$", fontsize=7, ha="right")
fig.tight_layout()
fig.savefig("fig_g2_spectrum.png", dpi=110)
print("fig_g2_spectrum.png written")
