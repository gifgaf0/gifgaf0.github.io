#!/usr/bin/env python3
"""E7 second cross-check (x2): every derived E7 number from my own inputs.

Inputs: x2_hedgehog.json, x2_hopfion.json, x2_dl.json (my own computations), PDG 2026 via the
`pdg` package when available (fallback constants typed in), CODATA 2022 G, Planck 2018
(arXiv:1807.06209 Table 2, TT,TE,EE+lowE+lensing: H0 = 67.36 +- 0.54, Omega_L = 0.6847 +- 0.0073),
LEP (Schael et al. 2013, arXiv:1302.3415, Eq. (3.9): r_e < 1.1e-19 m), E1e (read-only,
../../E1_phi4/results.json, optional).
Routes deliberately differ from the closed forms quoted in the E7 report where possible:
  - rotor and mass in MeV from I1 = (2pi/3) Lambda/(e^3 F_pi), M = a1 F_pi/e at each (e, F_pi);
  - the semiclassical floor by root-finding E_rot(e) = rho M(e) in MeV;
  - rho_Lambda from SI units: Omega_L * 3 H0^2/(8 pi G) * c^2, converted with (hbar c)^3;
  - Breit-Wheeler maximum by bounded scalar minimisation.
Writes x2_audit.json.
"""
import json
import os
import numpy as np
from scipy.optimize import brentq, minimize_scalar, fsolve

PI = np.pi
HH = json.load(open("x2_hedgehog.json"))
HP = json.load(open("x2_hopfion.json"))
DL = json.load(open("x2_dl.json"))

# ---------------- constants ----------------
hbarc = 197.3269804          # MeV fm (exact SI-derived value 197.32698046...)
alpha = 1 / 137.035999177
try:
    import pdg
    api = pdg.connect()
    m_e = api.get("S003M").best_summary().value
    m_p = api.get("S016M").best_summary().value
    m_H = api.get("S126M").best_summary().value
    src = "PDG 2026 (pdg package)"
except Exception:                                         # pragma: no cover
    m_e, m_p, m_H = 0.51099895069, 938.27208943, 125.13
    src = "fallback constants"
r_p = 0.84075                 # fm, CODATA 2022 / PDG 2026 proton charge radius
G_SI = 6.67430e-11            # CODATA 2022
c_SI = 299792458.0
hbar_SI = 1.054571817e-34
eV = 1.602176634e-19
Mpc = 3.0856775814913673e22
out = {"constants": dict(hbarc=hbarc, alpha=alpha, m_e=m_e, m_p=m_p, m_H=m_H, r_p=r_p, source=src)}

# ---------------- Skyrme ----------------
S = HH["massless"]
a1, Lam = S["a1"], S["Lambda"]
xr = {"B": S["xB"], "half": S["x_half"], "E": S["xE"], "M": S["xM"]}
c0 = {k: a1 * v for k, v in xr.items()}


def skyrme_MeV(e, Fpi):
    M = a1 * Fpi / e
    I1 = (2 * PI / 3) * Lam / (e ** 3 * Fpi)        # MeV^-1
    R = {k: v / (e * Fpi) * hbarc for k, v in xr.items()}   # fm
    return M, I1, R


# ANW point
M, I1, R = skyrme_MeV(5.45, 129.0)
anw = dict(M_cl=M, M_N=M + 3 / (8 * I1), M_D=M + 15 / (8 * I1), R_B=R["B"], R_M=R["M"],
           R_E=R["E"], R_half=R["half"], rot_over_M=(3 / (8 * I1)) / M,
           MR_classical=M * R["B"] / hbarc, MR_939=939.0 * R["B"] / hbarc,
           hbar_over_MR=hbarc / (M * R["B"]))
out["anw"] = anw


def fit(MN, MD):
    def eqs(p):
        e, F = p
        M, I1, _ = skyrme_MeV(e, F)
        return [M + 3 / (8 * I1) - MN, M + 15 / (8 * I1) - MD]
    e, F = fsolve(eqs, [5.4, 129.0], xtol=1e-14)
    return e, F


e_fit, F_fit = fit(938.9, 1232.0)
e_fit939, F_fit939 = fit(939.0, 1232.0)
out["fit"] = dict(e=e_fit, F_pi=F_fit, e_939=e_fit939, F_pi_939=F_fit939)
out["proton_data_rp_over_lambdaC"] = r_p * m_p / hbarc


# semiclassical floor: E_rot(e) = rho M(e) at an arbitrary F_pi (result is F_pi independent)
def floor(rho, Fpi=100.0, key="B"):
    g = lambda e: (3 / (8 * skyrme_MeV(e, Fpi)[1])) - rho * skyrme_MeV(e, Fpi)[0]
    e = brentq(g, 0.1, 1e3, xtol=1e-14)
    M, I1, R = skyrme_MeV(e, Fpi)
    return e, M * R[key] / hbarc


fl = {}
for rho in (1.0, 0.3, 0.1):
    e1, mr = floor(rho)
    e2, mr2 = floor(rho, Fpi=250.0)
    fl[str(rho)] = dict(e_max=e1, MR_min_B=mr, MR_min_B_check_other_Fpi=mr2, MR_min_half=floor(rho, key="half")[1])
out["floor"] = fl

# electron
lamC_e = hbarc / m_e
el = {"lambda_C_fm": lamC_e}
for name, Rmax in (("LEP", 1.1e-4), ("SEED", 1e-3)):
    MRmax = m_e * Rmax / hbarc
    d = {"MR_required_max": MRmax, "compton_over_R": lamC_e / Rmax}
    for k in ("B", "half", "E", "M"):
        e = np.sqrt(c0[k] / MRmax)
        Fpi = m_e * e / a1
        M, I1, R = skyrme_MeV(e, Fpi)
        d[k] = dict(e_min=e, F_pi=Fpi, check_M=M, check_R_fm=R[k], rot_over_M=(3 / (8 * I1)) / M,
                    hbar_over_MR=hbarc / (M * R[k]), e2_over_16pi2=e * e / (16 * PI ** 2),
                    e2_over_a1=e * e / a1)
    d["floor_over_MR"] = fl["1.0"]["MR_min_B"] / MRmax
    el[name] = d
out["electron"] = el

# ---------------- hopfion ----------------
EW, Rrms, Rring = HP["E_W"], HP["R_rms"], HP["R_ring"]
cH = 16 * np.sqrt(2) * PI ** 2
hop = dict(E_W=EW, R_rms=Rrms, R_ring=Rring, c0_rms=cH * EW * Rrms, c0_ring=cH * EW * Rring)
for name, Rmax in (("LEP", 1.1e-4), ("SEED", 1e-3)):
    MRmax = m_e * Rmax / hbarc
    k4_rms = MRmax / hop["c0_rms"]
    k4_ring = MRmax / hop["c0_ring"]
    hop[name] = dict(kappa4_max_rms=k4_rms, g2_min_rms=1 / k4_rms, kappa4_max_ring=k4_ring,
                     g2_min_ring=1 / k4_ring, sqrt_kappa2_MeV_rms=m_e / (cH * EW * np.sqrt(k4_rms)),
                     sqrt_kappa2_MeV_ring=m_e / (cH * EW * np.sqrt(k4_ring)))
out["hopfion"] = hop

# ---------------- pairs: DL + E1e ----------------
pairs = dict(DL["derived"])
pairs["two_g2MS"] = DL["model"]["two_g2MS"]
pairs["g2Nmin_DL"] = DL["fig7b"]["g2Nmin_plateau_mean_E_gt_8p5"]
pairs["phi4_g2_Npair"] = 4.0 / 3.0            # g^2 = 2 lambda/m^2, M_kink = (2/3) m/g^2
e1p = "../../E1_phi4/results.json"
if os.path.exists(e1p):
    E1 = json.load(open(e1p))
    for h in E1.get("headline", []):
        if h.get("quantity", "").startswith("E1e smallest classical N_lin"):
            c = h["value"]
            pairs["E1e_Nlin_lambda_over_m2"] = c
            pairs["E1e_g2Nmin_phi4"] = 2 * c
            pairs["E1e_g2Nmin_over_g2Npair"] = 2 * c / (4 / 3)
            pairs["E1e_g2_for_N_eq_2"] = c       # N = c m^2/lambda = 2 c/g^2 -> N = 2 at g^2 = c
        if h.get("quantity", "").startswith("E1e Gaussian packets, min_E_reproduced"):
            pairs["E1e_NE_lambda_over_m2_minE"] = h["value"]["N_E_times_lambda_over_m2"]
out["pairs"] = pairs

# ---------------- Breit-Wheeler ----------------
def sigma_bw(b):
    return 0.5 * (1 - b * b) * ((3 - b ** 4) * np.log((1 + b) / (1 - b)) - 2 * b * (2 - b * b))


r = minimize_scalar(lambda b: -sigma_bw(b), bounds=(0.01, 0.99), method="bounded", options={"xatol": 1e-12})
b = r.x
re_fm = alpha * hbarc / m_e
out["breit_wheeler"] = dict(beta_max=b, sigma_max_over_pi_re2=sigma_bw(b),
                            sqrt_s_over_2m=1 / np.sqrt(1 - b * b),
                            sigma_max_mb=sigma_bw(b) * PI * re_fm ** 2 * 10.0, r_e_fm=re_fm)

# ---------------- vacuum ----------------
H0 = 67.36e3 / Mpc                                 # s^-1
OL = 0.6847
rho_SI = OL * 3 * H0 ** 2 / (8 * PI * G_SI) * c_SI ** 2          # J/m^3
hbarc_GeVm = hbar_SI * c_SI / eV / 1e9                            # GeV m
rho_GeV4 = rho_SI / eV / 1e9 * hbarc_GeVm ** 3
MPl = np.sqrt(hbar_SI * c_SI / G_SI) * c_SI ** 2 / eV / 1e9       # GeV
MPl_red = MPl / np.sqrt(8 * PI)
Lam_eV2 = 3 * OL * (hbar_SI * H0 / eV) ** 2
vac = dict(H0_inv_s=H0, rho_Lambda_GeV4=rho_GeV4, rho_quarter_meV=rho_GeV4 ** 0.25 * 1e12,
           rel_unc_from_OLh2=0.0082 / 0.3107, OLh2_check=OL * 0.6736 ** 2,
           M_Pl_GeV=MPl, M_Pl_red_GeV=MPl_red, Lambda_eV2=Lam_eV2,
           Lambda_over_MPl2=Lam_eV2 / (MPl * 1e9) ** 2,
           Lambda_over_MPl2_from_4p24=4.24e-66 / (MPl * 1e9) ** 2,
           rho_with_PLAN_rounded=0.685 * 3 * (67.4e3 / Mpc) ** 2 / (8 * PI * G_SI) * c_SI ** 2 / eV / 1e9 * hbarc_GeVm ** 3)
scales = {"f_pi 92.07 MeV": 0.09207, "f ANW 64.5 MeV": 0.0645, "m_e": m_e * 1e-3, "v_EW 246.22 GeV": 246.22,
          "M_Pl reduced": MPl_red, "M_Pl unreduced": MPl}
vac["ratios"] = {k: v ** 4 / rho_GeV4 for k, v in scales.items()}
vac["ratios"]["Higgs depth m_H^2 v^2/8"] = (m_H ** 2 * 246.22 ** 2 / 8) / rho_GeV4
out["vacuum"] = vac


def show(d, pre=""):
    for k, v in d.items():
        if isinstance(v, dict):
            show(v, pre + k + ".")
        elif isinstance(v, float):
            print(f"{pre}{k} = {v:.10g}")
        else:
            print(f"{pre}{k} = {v}")


show(out)
with open("x2_audit.json", "w") as fh:
    json.dump(out, fh, indent=1, default=float)
