#!/usr/bin/env python3
"""E7 cross-check: independent recomputation of every E7 headline number.

Inputs: cc_hedgehog.json (own Ritz-spectral hedgehog), cc_hopfion.json (own hopfion check),
cc_dl_digitized.json (own digitisation of Demidov-Levkov figures; optional), and
../../E1_phi4/e1e_results.json (E1e, read-only; optional).  Constants are typed in here from
CODATA 2022 / PDG 2026 (checked against the `pdg` package if importable).
Writes cc_audit.json.  Deterministic.
"""
import json
import os
import numpy as np
from scipy.optimize import brentq, minimize_scalar, fsolve
from scipy.integrate import quad

PI = np.pi
out = {}

# ---------------------------------------------------------------- constants
hbarc = 197.3269804          # MeV fm (CODATA 2022, exact-derived)
m_e = 0.51099895069          # MeV (CODATA 2022 / PDG 2026)
m_p = 938.27208943           # MeV
r_p = 0.84075                # fm, PDG 2026 proton charge radius
alpha = 1 / 137.035999177    # CODATA 2022
G_SI = 6.67430e-11           # m^3 kg^-1 s^-2 (CODATA 2022)
hbar_SI = 1.054571817e-34
c_SI = 299792458.0
eV_J = 1.602176634e-19
Mpc_m = 3.0856775814913673e22
m_H = 125.1309438281615      # GeV, PDG 2026 (pdg package)
v_EW = 246.21965             # GeV, (sqrt2 G_F)^(-1/2), G_F = 1.1663788e-5
f_pi = 130.2 / np.sqrt(2)    # MeV, PDG f_pi+ = 130.2 MeV
try:
    import pdg
    api = pdg.connect()
    out["pdg_check"] = dict(m_e=api.get("S003M").best_summary().value, m_p=api.get("S016M").best_summary().value,
                            m_H=api.get("S126M").best_summary().value)
except Exception as ex:   # pragma: no cover
    out["pdg_check"] = f"pdg package unavailable: {ex}"

# ---------------------------------------------------------------- hedgehog
H = json.load(open("cc_hedgehog.json"))
b = H["best"]
a1, Lam = b["a1"], b["Lambda"]
xr = dict(B=b["xB"], M=b["xM"], E=b["xE"], half=b["x_half"], meanB=b["xmeanB"], E90=b["x_E90"])
c0 = {k: a1 * v for k, v in xr.items()}
out["hedgehog"] = dict(a1=a1, a1_over_3pi2=a1 / (3 * PI ** 2), Lambda=Lam, x=xr, c0=c0,
                       virial=b["virial_E2_over_E4"], slope0=b["slope0"], Ctail=b["Ctail"],
                       targets=dict(a1=(1.2315 * 3 * PI ** 2, 0.002), Lambda=(50.9, 0.005)),
                       pass_a1=abs(a1 / (1.2315 * 3 * PI ** 2) - 1) < 0.002, pass_Lambda=abs(Lam / 50.9 - 1) < 0.005)

# ANW parameters: F_pi = 129 MeV (186-MeV convention), e = 5.45
def skyrme_phys(Fpi, e):
    unit = hbarc / (e * Fpi)                          # fm per unit x
    M = a1 * Fpi / e
    I_inv = 3 * e ** 3 * Fpi / (2 * PI * Lam)         # 1/I1 in MeV
    return dict(unit_fm=unit, M_cl=M, I1_inv=I_inv, M_N=M + 0.375 * I_inv, M_D=M + 1.875 * I_inv,
                R={k: v * unit for k, v in xr.items()}, rot_over_M=0.375 * I_inv / M)

anw = skyrme_phys(129.0, 5.45)
anw["MR_classical_B"] = anw["M_cl"] * anw["R"]["B"] / hbarc
anw["MR_939_B"] = 939.0 * anw["R"]["B"] / hbarc
anw["MR_mp_B"] = m_p * anw["R"]["B"] / hbarc
anw["c0B_over_e2"] = c0["B"] / 5.45 ** 2
anw["hbar_over_MR_classical"] = 1 / anw["MR_classical_B"]
out["ANW"] = anw

# own fit of (F_pi, e) to M_N, M_Delta (two variants of the nucleon mass)
def fit(MN, MD):
    def eqs(p):
        Fpi, e = p
        s = skyrme_phys(Fpi, e)
        return [s["M_N"] - MN, s["M_D"] - MD]
    Fpi, e = fsolve(eqs, [129.0, 5.45], xtol=1e-14)
    return dict(F_pi=Fpi, e=e)
out["fit"] = {"939_1232": fit(939.0, 1232.0), "938.9_1232": fit(938.9, 1232.0)}

# data: proton r_p / lambda_C
lamC_p = hbarc / m_p
out["proton_data"] = dict(lambda_C_fm=lamC_p, rp_over_lambdaC=r_p / lamC_p)

# ---------------------------------------------------------------- electron fold
lamC_e = hbarc / m_e
el = dict(lambda_C_fm=lamC_e)
for name, Rmax in [("LEP", 1.1e-4), ("SEED", 1e-3)]:
    MRmax = m_e * Rmax / hbarc
    d = dict(R_max_fm=Rmax, MR_max=MRmax, lambdaC_over_R=1 / MRmax, log10=np.log10(1 / MRmax))
    for k in ["B", "M", "E", "half", "meanB"]:
        e2 = c0[k] / MRmax
        e = np.sqrt(e2)
        Fpi = m_e * e / a1                               # M_cl = m_e
        I_inv = 3 * e ** 3 * Fpi / (2 * PI * Lam)
        E_rot = 0.375 * I_inv                            # J = 1/2 rotor, MeV
        d[k] = dict(e=e, e2=e2, F_pi_MeV=Fpi, E_rot_MeV=E_rot, rot_over_M=E_rot / m_e,
                    rot_over_M_formula=9 * e ** 4 / (16 * PI * Lam * a1),
                    hbar_over_MR=e2 / c0[k], e2_over_a1=e2 / a1, e2_over_16pi2=e2 / (16 * PI ** 2))
    el[name] = d
# semiclassical floor: E_rot/M = 9 e^4/(16 pi Lambda a1) <= rho  ->  M R >= c0 / e_max^2
floor = {}
for rho in [1.0, 0.3, 0.1]:
    emax = (rho * 16 * PI * Lam * a1 / 9) ** 0.25
    floor[str(rho)] = dict(e_max=emax, MR_min_B=c0["B"] / emax ** 2, MR_min_half=c0["half"] / emax ** 2)
el["floor"] = floor
el["floor_over_electron_LEP"] = floor["1.0"]["MR_min_B"] / el["LEP"]["MR_max"]
out["electron"] = el

# ---------------------------------------------------------------- pion-mass family: c0 and floor
from cc_hedgehog import Hedgehog, observables
fam = []
for beta in [0.0, 1.0, 4.0, 16.0]:
    h = Hedgehog(N=60, L=1.4 / np.sqrt(1 + beta), Nq=1500, beta=beta)
    h.solve()
    ob = observables(h)
    emax = (16 * PI * ob["Lambda"] * ob["a1"] / 9) ** 0.25       # E_rot <= M_cl (rotor uses Lambda(beta))
    fam.append(dict(beta=beta, a1=ob["a1"], Lambda=ob["Lambda"], c0_B=ob["a1"] * ob["xB"],
                    e_max=emax, MR_floor_B=ob["a1"] * ob["xB"] / emax ** 2))
out["pion_mass_floor"] = fam

# ---------------------------------------------------------------- hopfion
Hp = json.load(open("cc_hopfion.json"))
kfac = 16 * np.sqrt(2) * PI ** 2
EW = Hp["analytic"]["E_W"]
hop = dict(E_W=EW, R_rms=Hp["analytic"]["R_rms"], R_ring=Hp["analytic"]["R_ring"],
           c0_rms=kfac * EW * Hp["analytic"]["R_rms"], c0_ring=kfac * EW * Hp["analytic"]["R_ring"],
           E_W_numeric=Hp["numeric"]["Nr500_Nth64_phi0.0"]["E"], R_rms_numeric=Hp["numeric"]["Nr500_Nth64_phi0.0"]["Rrms"])
for name, Rmax in [("LEP", 1.1e-4), ("SEED", 1e-3)]:
    MRmax = m_e * Rmax / hbarc
    k4_rms = MRmax / hop["c0_rms"]; k4_ring = MRmax / hop["c0_ring"]
    sqrt_k2 = m_e / (kfac * EW * np.sqrt(k4_rms))
    hop[name] = dict(kappa4_max_rms=k4_rms, g2_min_rms=1 / k4_rms, g2_min_ring=1 / k4_ring, sqrt_kappa2_MeV_rms=sqrt_k2)
hop["E_W_vs_lattice_1.204"] = EW / 1.204 - 1
hop["E_W_vs_1.22"] = EW / 1.22 - 1
out["hopfion"] = hop

# ---------------------------------------------------------------- Demidov-Levkov model
a = 0.4
W = lambda x: np.exp(-x ** 2) * (x + x ** 3 + x ** 5)
res = minimize_scalar(lambda x: -W(x), bounds=(0.1, 3), method="bounded", options=dict(xatol=1e-14))
xstar = res.x; v = 1 / W(xstar)
phip = 1 + a * xstar
V = lambda p: 0.5 * (p + 1) ** 2 * (1 - v * W((p - 1) / a))
g2MS = quad(lambda p: np.sqrt(max(2 * V(p), 0.0)), -1, phip, limit=400, epsabs=1e-13, epsrel=1e-12)[0]
# masses
hstep = 1e-4
m_minus = np.sqrt((V(-1 + hstep) - 2 * V(-1) + V(-1 - hstep)) / hstep ** 2)
m_plus = np.sqrt((V(phip + hstep) - 2 * V(phip) + V(phip - hstep)) / hstep ** 2)
dl = dict(v_degenerate=v, x_star=xstar, phi_plus=phip, m_minus=m_minus, m_plus=m_plus,
          g2_MS=g2MS, two_g2_MS=2 * g2MS)
dig = json.load(open("cc_dl_digitized.json")) if os.path.exists("cc_dl_digitized.json") else None
if dig:
    F_thr = dig["fig3b_1103.0013v2"]["F_at_left_edge"]
    F_hi = dig["fig3b_1103.0013v2"]["F_at_g2E_11p5"]
    F_min = dig["fig3b_1103.0013v2"]["F_min"]
    g2Nmin = dig["fig7b_1103.2133v2"]["g2Nmin_high_energy_mean"]
    dl["digitized"] = dict(F_threshold=F_thr, F_at_11p5=F_hi, F_min=F_min, g2Nmin_high=g2Nmin,
                           left_edge_g2E_fig3b=dig["fig3b_1103.0013v2"]["left_edge_g2E"])
    rows = {}
    for P in [0.1, np.exp(-1), 0.5]:
        g2 = F_hi / np.log(1 / P)
        rows[f"P={P:.3g}"] = dict(g2=g2, M_S_over_m=g2MS / g2, N_pair=2 * g2MS / g2)
    dl["unsuppressed"] = rows
    dl["kappa_per_pair_quantum"] = [F_hi / (2 * g2MS), F_thr / (2 * g2MS)]
    dl["Nmin_over_Npair"] = g2Nmin / (2 * g2MS)
    dl["log10_exp_minus_F_over_alpha"] = -F_hi / alpha / np.log(10)
    dl["log10_exp_minus_F_over_4pialpha"] = -F_hi / (4 * PI * alpha) / np.log(10)
out["demidov_levkov"] = dl

# E1e phi^4 (now available): N_min lambda / m^2, g^2 = 2 lambda/m^2
e1e_path = "../../E1_phi4/e1e_results.json"
if os.path.exists(e1e_path):
    e1e = json.load(open(e1e_path))
    c = e1e["implication"]["c"]                       # N_lin lambda/m^2 (smallest reproduced producer)
    out["E1e_phi4"] = dict(N_min_lambda_over_m2=c, g2_N_min=2 * c, g2_N_pair=4 / 3,
                           Nmin_over_Npair=2 * c / (4 / 3),
                           lambda_over_m2_for_N_min_le_2=c / 2, g2_for_N_min_le_2=c,
                           note="classical production only seen for N >= c m^2/lambda (upper bound on the true minimum)")

# ---------------------------------------------------------------- Breit-Wheeler
r_e = alpha * hbarc / m_e
sig = lambda bb: 0.5 * (1 - bb ** 2) * ((3 - bb ** 4) * np.log((1 + bb) / (1 - bb)) - 2 * bb * (2 - bb ** 2))
rr = minimize_scalar(lambda bb: -sig(bb), bounds=(0.01, 0.99), method="bounded", options=dict(xatol=1e-12))
bmax = rr.x
out["breit_wheeler"] = dict(r_e_fm=r_e, beta_max=bmax, sigma_max_over_pi_re2=sig(bmax),
                            sigma_max_mb=sig(bmax) * PI * r_e ** 2 * 10.0,   # 1 fm^2 = 10 mb
                            sqrt_s_over_2me=1 / np.sqrt(1 - bmax ** 2))

# ---------------------------------------------------------------- vacuum energy
GeV_J = 1e9 * eV_J
hbarc_GeVm = hbar_SI * c_SI / GeV_J                    # GeV m
def rho_L(H0, OL):
    H = H0 * 1e3 / Mpc_m                               # s^-1
    rho_c_kg = 3 * H ** 2 / (8 * PI * G_SI)            # kg/m^3
    rho_c_GeV4 = rho_c_kg * c_SI ** 2 / GeV_J * hbarc_GeVm ** 3
    return rho_c_GeV4, OL * rho_c_GeV4
rc, rl = rho_L(67.36, 0.6847)
M_Pl = np.sqrt(hbar_SI * c_SI / G_SI) * c_SI ** 2 / GeV_J        # GeV
M_Pl_red = M_Pl / np.sqrt(8 * PI)
Lam_eV2 = 4.24e-66
rl_from_Lambda = Lam_eV2 * 1e-18 * M_Pl_red ** 2                   # rho = Lambda Mbar^2 (GeV^4)
rl_from_OLh2 = 0.3107 * rho_L(100.0, 1.0)[0]
vac = dict(rho_crit_GeV4=rc, rho_L_GeV4=rl, rho_L_quarter_meV=rl ** 0.25 * 1e12,
           rho_L_PLAN_rounded=rho_L(67.4, 0.685)[1], rho_L_from_Lambda=rl_from_Lambda, rho_L_from_OLh2=rl_from_OLh2,
           rel_unc_OLh2=0.0082 / 0.3107, M_Pl=M_Pl, M_Pl_red=M_Pl_red,
           Lambda_over_MPl2=Lam_eV2 * 1e-18 / M_Pl ** 2)
scales = {"f_pi (92.07 MeV)": (f_pi * 1e-3) ** 4, "f_ANW = 64.5 MeV": (0.0645) ** 4, "m_e": (m_e * 1e-3) ** 4,
          "v_EW 246.22 GeV": v_EW ** 4, "Higgs depth m_H^2 v^2/8": m_H ** 2 * v_EW ** 2 / 8,
          "M_Pl reduced": M_Pl_red ** 4, "M_Pl unreduced": M_Pl ** 4}
vac["ratios"] = {k: s / rl for k, s in scales.items()}
out["vacuum"] = vac

# ---------------------------------------------------------------- Weinberg-Witten selection rule
ww = {}
for hh in [0, 0.5, 1, 1.5, 2]:
    ww[str(hh)] = dict(charge_J_allowed=bool(2 * hh <= 1), energy_T_allowed=bool(2 * hh <= 2))
out["weinberg_witten"] = ww

with open("cc_audit.json", "w") as f:
    json.dump(out, f, indent=1, default=float)

# ---------------------------------------------------------------- print
def p(*a_):
    print(*a_)
p(f"a1 = {a1:.10f} (target 36.4633, pass {out['hedgehog']['pass_a1']}),  Lambda = {Lam:.6f} (50.9, pass {out['hedgehog']['pass_Lambda']})")
p("c0:", {k: round(v, 4) for k, v in c0.items()})
p(f"ANW: M_cl={anw['M_cl']:.3f} M_N={anw['M_N']:.3f} M_D={anw['M_D']:.3f} R_B={anw['R']['B']:.5f} R_M={anw['R']['M']:.5f} R_E={anw['R']['E']:.5f} fm")
p(f"ANW: MR classical={anw['MR_classical_B']:.4f}, MR(939)={anw['MR_939_B']:.4f}, MR(m_p)={anw['MR_mp_B']:.4f}, rot/M={anw['rot_over_M']:.5f}")
p("fit:", out["fit"])
p(f"proton data r_p/lambda_C = {r_p/lamC_p:.5f}")
for nm in ["LEP", "SEED"]:
    d = el[nm]
    p(f"electron {nm}: lambda_C/R = {d['lambdaC_over_R']:.5e}; e(B) = {d['B']['e']:.2f}, F_pi = {d['B']['F_pi_MeV']:.3f} MeV, "
      f"E_rot/M = {d['B']['rot_over_M']:.4e}, hbar/MR = {d['B']['hbar_over_MR']:.4e}, e^2/a1 = {d['B']['e2_over_a1']:.3e}, "
      f"e^2/16pi^2 = {d['B']['e2_over_16pi2']:.4e}; e range = {min(d[k]['e'] for k in ['B','M','E','half']):.4g}..{max(d[k]['e'] for k in ['B','M','E','half']):.4g}")
p("floor:", floor, " floor/electron =", el["floor_over_electron_LEP"])
p("pion-mass floor:", [(r['beta'], round(r['c0_B'], 3), round(r['MR_floor_B'], 4)) for r in fam])
p("hopfion:", {k: v for k, v in hop.items() if not isinstance(v, dict)}, hop["LEP"])
p("DL:", {k: v for k, v in dl.items() if k not in ("unsuppressed",)})
p("DL unsuppressed:", dl.get("unsuppressed"))
p("E1e:", out.get("E1e_phi4"))
p("BW:", out["breit_wheeler"])
p("vacuum:", {k: v for k, v in vac.items() if k != "ratios"})
p("ratios:", {k: f"{v:.4e}" for k, v in vac["ratios"].items()})
