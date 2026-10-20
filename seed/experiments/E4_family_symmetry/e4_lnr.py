"""
e4_lnr.py -- E4 part 3: reproduce the Luhn-Nasri-Ramond Z7 x| Z3 seesaw example
(arXiv:0706.2341, Sec. 4.1-4.2) exactly, and compare it with NuFIT 6.0.

Mass matrices come from the five F21 invariants of  psi psi' xi xi'  (fermions in 3, familons in
3bar; e4_yukawa.py finds exactly 5).  Writing u = <xi> (paired with psi) and u' = <xi'>:
    M_ii = c0 u_i u'_i
    M_ij = c1 u_i u'_j + c2 u_j u'_i     (i,j) in O_A = {(1,3),(3,2),(2,1)}
    M_ij = c3 u_i u'_j + c4 u_j u'_i     (i,j) in O_B = {(1,2),(2,3),(3,1)}
(O_A, O_B are the two orbits of ordered pairs under C).  With psi = L (familon phi5, LNR's primed
vev a',b',c') and psi' = nu^c (phi1, vev a,b,c) this is LNR's M_Dir with (c1,c2,c3,c4) =
(beta1, beta2, gamma1, gamma2); the Majorana matrix is diag(u_i^2) + alpha (u_i u_j, i != j).
Run: python3 e4_lnr.py   (a few seconds)
"""
import json
import math
import os

import numpy as np
import sympy as sp

from data_targets import NUFIT, NUFIT_1SIGMA, R_ATM_SOL, R_ATM_SOL_ERR, MZ, chi2_pmns
from e4lib import angles_from_U, invariants

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
R = np.load(os.path.join(OUT, "reps.npz"))
CHECKS = {}


def check(name, ok, detail=""):
    CHECKS[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


O_A = [(0, 2), (2, 1), (1, 0)]
O_B = [(0, 1), (1, 2), (2, 0)]


def dirac(u, up, c):
    """u: familon paired with the row fermion, up: with the column fermion; c = (c0..c4)."""
    M = sp.zeros(3, 3)
    for i in range(3):
        M[i, i] = c[0] * u[i] * up[i]
    for (i, j) in O_A:
        M[i, j] = c[1] * u[i] * up[j] + c[2] * u[j] * up[i]
    for (i, j) in O_B:
        M[i, j] = c[3] * u[i] * up[j] + c[4] * u[j] * up[i]
    return M


def majorana(u, alpha):
    M = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            M[i, j] = u[i] ** 2 if i == j else alpha * u[i] * u[j]
    return M


# ---- 0. the five hand-written tensors are exactly the computed F21 invariant space
r3, r3b = R["F21_3"], R["F21_3b"]
gens = list(R["F21_gens"])
W = invariants([r3, r3, r3b, r3b], gens)          # numeric basis of invariant vectors


def tensor_of(k):
    T = np.zeros((3, 3, 3, 3), dtype=complex)
    if k == 0:
        for i in range(3):
            T[i, i, i, i] = 1
    else:
        orb = O_A if k in (1, 2) else O_B
        for (i, j) in orb:
            if k in (1, 3):
                T[i, j, i, j] = 1      # psi_i psi'_j xi_i xi'_j
            else:
                T[i, j, j, i] = 1      # psi_i psi'_j xi_j xi'_i
    return T


# invariance of sum T psi psi' xi xi' under the generators, convention-free (random fields)
rng = np.random.default_rng(7)
ok_inv = True
for k in range(5):
    T = tensor_of(k)
    for g in gens:
        f = [rng.normal(size=3) + 1j * rng.normal(size=3) for _ in range(4)]
        val = np.einsum("ijkl,i,j,k,l->", T, *f)
        reps_ = [r3[g], r3[g], r3b[g], r3b[g]]
        val2 = np.einsum("ijkl,i,j,k,l->", T, *[R_ @ x for R_, x in zip(reps_, f)])
        ok_inv &= abs(val - val2) < 1e-10
rank = np.linalg.matrix_rank(np.array([tensor_of(k).ravel() for k in range(5)]))
check("the five LNR-form tensors are F21 invariants, independent, and fill the computed 5-dim space",
      ok_inv and rank == 5 and W.shape[1] == 5)

# ---- 1. LNR's integer point
a, b, c = 1, 1, 1                    # <phi1> ~ (1,1,1)
ap, bp, cp = -1, 1, 1                # <phi5> ~ (-1,1,1)
alpha, beta = sp.Integer(-1), sp.Integer(-1)
MMaj = majorana([a, b, c], alpha)
MDir = dirac([ap, bp, cp], [a, b, c], [1, beta, beta, beta, beta])
Mnu = -MDir * MMaj.inv() * MDir.T
lnr_MMaj = sp.Matrix([[1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
lnr_MDir = sp.Matrix([[-1, 0, 0], [0, 1, -2], [0, -2, 1]])
lnr_Mnu = sp.Rational(1, 2) * sp.Matrix([[0, 1, 1], [1, -4, 5], [1, 5, -4]])
check("M_Maj = [[1,-1,-1],[-1,1,-1],[-1,-1,1]] (LNR)", MMaj == lnr_MMaj, str(MMaj.tolist()))
check("M_Dir = [[-1,0,0],[0,1,-2],[0,-2,1]] (LNR)", MDir == lnr_MDir, str(MDir.tolist()))
check("M_Maj^-1 = -(1/2)[[0,1,1],[1,0,1],[1,1,0]] (LNR intermediate)",
      MMaj.inv() == -sp.Rational(1, 2) * sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]]))
ratio_mat = [sp.nsimplify(Mnu[i, j] / lnr_Mnu[i, j]) for i in range(3) for j in range(3) if lnr_Mnu[i, j] != 0]
check("M_nu = -M_Dir M_Maj^-1 M_Dir^T is proportional to (1/2)[[0,1,1],[1,-4,5],[1,5,-4]] (LNR)",
      len(set(ratio_mat)) == 1 and Mnu[0, 0] == 0, f"M_nu = {Mnu.tolist()}, factor {ratio_mat[0]}")
tbm = (Mnu[0, 1] == Mnu[0, 2], Mnu[1, 1] == Mnu[2, 2], Mnu[1, 2] == Mnu[0, 0] + Mnu[0, 1] - Mnu[1, 1])
check("tri-bimaximal criteria M12 = M13, M22 = M33, M23 = M11 + M12 - M22 hold exactly", all(tbm))
UTB = sp.Matrix([[sp.sqrt(sp.Rational(2, 3)), 1 / sp.sqrt(3), 0],
                 [-1 / sp.sqrt(6), 1 / sp.sqrt(3), -1 / sp.sqrt(2)],
                 [-1 / sp.sqrt(6), 1 / sp.sqrt(3), 1 / sp.sqrt(2)]])
Dg = sp.simplify(UTB.T * Mnu * UTB)
masses = [Dg[i, i] for i in range(3)]
check("U_TB^T M_nu U_TB is diagonal", all(sp.simplify(Dg[i, j]) == 0 for i in range(3) for j in range(3) if i != j),
      f"diag = {masses}")
mr = [sp.nsimplify(m / masses[0]) for m in masses]
check("mass eigenvalues proportional to (1, -2, 9) (LNR), normal hierarchy", mr == [1, -2, 9], str(mr))
r_lnr = sp.nsimplify((masses[2] ** 2 - masses[0] ** 2) / (masses[1] ** 2 - masses[0] ** 2))
check("Dm^2_atm/Dm^2_sol = (81 - 1)/(4 - 1) = 80/3 exactly (LNR: 26.7)", r_lnr == sp.Rational(80, 3), str(r_lnr))

# ---- 2. the alpha windows LNR quote (beta = -1, phi5 = (-1,1,1), phi1 = (1,1,1))
al = sp.symbols("alpha", real=True)
Mnu_a = sp.simplify(-MDir * majorana([1, 1, 1], al).inv() * MDir.T)
Dg_a = sp.simplify(UTB.T * Mnu_a * UTB)
offd = [sp.simplify(Dg_a[i, j]) for i in range(3) for j in range(3) if i != j]
check("for beta = -1 the light matrix stays exactly tri-bimaximal for EVERY alpha (alpha only moves masses)",
      all(o == 0 for o in offd))
m_a = [sp.simplify(Dg_a[i, i]) for i in range(3)]
print("  masses(alpha) in the TBM basis:", m_a)
f_m = sp.lambdify(al, m_a, "numpy")


def r_of(alpha_v):
    m1, m2, m3 = (abs(complex(x)) for x in f_m(alpha_v))
    if m2 <= m1 or m3 <= m2:
        return np.nan          # not normal ordering with the TBM labelling (m1 < m2 < m3)
    return (m3 ** 2 - m1 ** 2) / (m2 ** 2 - m1 ** 2)


grid = np.linspace(-3, 3, 600001)
grid = grid[(np.abs(grid - 1) > 1e-6) & (np.abs(grid + 0.5) > 1e-6)]
rv = np.array([r_of(x) for x in grid])


def windows(lo, hi):
    ok = (rv >= lo) & (rv <= hi)
    out = []
    i = 0
    while i < len(grid):
        if ok[i]:
            j = i
            while j + 1 < len(grid) and ok[j + 1]:
                j += 1
            out.append((round(float(grid[i]), 3), round(float(grid[j]), 3)))
            i = j + 1
        else:
            i += 1
    return out


w_lnr = windows(21.3, 45.1)          # LNR's own 3sigma range (Schwetz 2006)
print("  alpha windows for r in [21.3, 45.1]:", w_lnr)
lnr_quoted = [(-1.15, -0.95), (-0.22, -0.15)]
match = len(w_lnr) == 2 and all(abs(w[0] - q[0]) < 0.01 and abs(w[1] - q[1]) < 0.01
                                for w, q in zip(sorted(w_lnr), sorted(lnr_quoted)))
check("LNR's alpha windows -1.15 < alpha < -0.95 and -0.22 < alpha < -0.15 reproduced from r in [21.3, 45.1] "
      "(normal ordering, TBM labelling), to the two decimals LNR quote", match, str(w_lnr))
lo3, hi3 = R_ATM_SOL - 3 * R_ATM_SOL_ERR, R_ATM_SOL + 3 * R_ATM_SOL_ERR
w_nufit = windows(lo3, hi3)
w_nufit1 = windows(R_ATM_SOL - R_ATM_SOL_ERR, R_ATM_SOL + R_ATM_SOL_ERR)
print(f"  alpha windows for NuFIT 6.0 r = {R_ATM_SOL:.2f} +- {R_ATM_SOL_ERR:.2f}: 1sigma {w_nufit1}, 3sigma {w_nufit}")
alpha_fit = []
from scipy.optimize import brentq
for (lo, hi) in w_nufit1:
    try:
        alpha_fit.append(brentq(lambda x: r_of(x) - R_ATM_SOL, lo - 1e-3, hi + 1e-3))
    except Exception:
        pass

# ---- 3. charged-lepton "Cabibbo haze" (LNR Sec. 4.2): theta13 and theta12
me_mmu_pdg = 0.51099895 / 105.6583755          # PDG pole masses
me_mmu_mz = MZ["me"][0] / MZ["mmu"][0]
UTBn = np.array(UTB.evalf(), dtype=float)
haze = {}
for label, ratio in (("pole masses", me_mmu_pdg), ("MS-bar at M_Z", me_mmu_mz)):
    le = math.sqrt(ratio)
    # LNR's linear-order matrix, as printed: U_MNSP = U_{-1}^dagger U_TB,
    # U_{-1} = [[1, le, 0], [-le, 1, 0], [0, 0, 1]]
    Um1 = np.array([[1, le, 0], [-le, 1, 0], [0, 0, 1]])
    U_lin = Um1.conj().T @ UTBn
    th13_lin = math.degrees(math.asin(abs(U_lin[0, 2])))
    th12_lin = math.degrees(math.atan2(abs(U_lin[0, 1]), abs(U_lin[0, 0])))
    # unitary version: rotation by angle arcsin(le) with the same sign
    s_ = le
    c_ = math.sqrt(1 - s_ ** 2)
    Rot = np.array([[c_, s_, 0], [-s_, c_, 0], [0, 0, 1]])
    U_ex = Rot.T @ UTBn
    s12, s13, s23, dl, J = angles_from_U(U_ex)
    # opposite relative sign (also allowed: the sign is an input)
    U_op = Rot @ UTBn
    s12o, s13o, s23o, _, _ = angles_from_U(U_op)
    c2, det = chi2_pmns(U_ex, include_delta=False)
    haze[label] = {"lambda_e": le, "theta13_linear_deg": th13_lin, "theta12_linear_deg": th12_lin,
                   "unitary": {"s12sq": s12, "s13sq": s13, "s23sq": s23,
                               "theta12_deg": math.degrees(math.asin(math.sqrt(s12))),
                               "theta13_deg": math.degrees(math.asin(math.sqrt(s13))),
                               "theta23_deg": math.degrees(math.asin(math.sqrt(s23)))},
                   "opposite_sign_theta12_deg": math.degrees(math.asin(math.sqrt(s12o))),
                   "pulls_vs_NuFIT6": det["pulls"]}
    print(f"  haze ({label}): lambda_e = {le:.5f}; linear: theta13 = {th13_lin:.3f} deg, theta12 = {th12_lin:.2f} deg; "
          f"unitary: theta12 = {haze[label]['unitary']['theta12_deg']:.2f}, theta13 = {haze[label]['unitary']['theta13_deg']:.3f}, "
          f"theta23 = {haze[label]['unitary']['theta23_deg']:.2f}; opposite sign theta12 = {haze[label]['opposite_sign_theta12_deg']:.2f}")
h = haze["pole masses"]
check("theta13 = 2.8 deg (LNR) from lambda_e = sqrt(me/mmu)", abs(h["theta13_linear_deg"] - 2.8) < 0.05,
      f"{h['theta13_linear_deg']:.3f} deg")
check("theta12 shifts from 35.26 deg (TBM) to 32.4 deg (LNR)", abs(h["theta12_linear_deg"] - 32.4) < 0.05,
      f"{h['theta12_linear_deg']:.3f} deg")

# ---- 4. comparison with NuFIT 6.0
s13_lnr = math.sin(math.radians(h["unitary"]["theta13_deg"])) ** 2
cmp = {
    "theta13_deg": {"LNR": h["theta13_linear_deg"], "NuFIT6": 8.52, "NuFIT6_1sigma": 0.11},
    "sin2_theta13": {"LNR": s13_lnr, "NuFIT6": NUFIT["s13sq"][0], "sigma_used": NUFIT["s13sq"][1],
                     "pull": (s13_lnr - NUFIT["s13sq"][0]) / NUFIT["s13sq"][1]},
    "sin2_theta12": {"LNR": h["unitary"]["s12sq"], "NuFIT6": NUFIT["s12sq"][0],
                     "pull": h["pulls_vs_NuFIT6"]["s12sq"]},
    "sin2_theta23": {"LNR": 0.5, "NuFIT6": NUFIT["s23sq"][0],
                     "pull_3sigma_range_convention": (0.5 - NUFIT["s23sq"][0]) / NUFIT["s23sq"][1],
                     "pull_1sigma": (0.5 - NUFIT["s23sq"][0]) / NUFIT_1SIGMA["s23sq"][0]},
    "r_atm_sol": {"LNR": 80 / 3, "NuFIT6": R_ATM_SOL, "sigma": R_ATM_SOL_ERR,
                  "pull": (80 / 3 - R_ATM_SOL) / R_ATM_SOL_ERR},
}
print("  comparison with NuFIT 6.0:", json.dumps(cmp, indent=1))
check("LNR's integer point is excluded by NuFIT 6.0: theta13 pull < -20 sigma and r pull < -5 sigma",
      cmp["sin2_theta13"]["pull"] < -20 and cmp["r_atm_sol"]["pull"] < -5,
      f"theta13 pull {cmp['sin2_theta13']['pull']:.1f}, r pull {cmp['r_atm_sol']['pull']:.1f}")

res = {"matrices": {"M_Maj": [[int(x) for x in r_] for r_ in MMaj.tolist()],
                    "M_Dir": [[int(x) for x in r_] for r_ in MDir.tolist()],
                    "M_nu": [[str(x) for x in r_] for r_ in Mnu.tolist()],
                    "eigenvalues_TBM_basis": [str(m) for m in masses],
                    "eigenvalue_ratios": [int(x) for x in mr]},
       "r_atm_sol_exact": "80/3", "r_atm_sol": 80 / 3,
       "tbm_for_all_alpha_at_beta_minus1": True,
       "masses_vs_alpha_TBM_basis": [str(m) for m in m_a],
       "alpha_windows_LNR_range_21.3_45.1": w_lnr, "alpha_windows_quoted_by_LNR": lnr_quoted,
       "alpha_windows_NuFIT6_1sigma": w_nufit1, "alpha_windows_NuFIT6_3sigma": w_nufit,
       "alpha_solving_r_eq_NuFIT6_central": alpha_fit,
       "haze": haze, "comparison_NuFIT6": cmp, "checks": CHECKS,
       "all_pass": all(v["pass"] for v in CHECKS.values())}
with open(os.path.join(OUT, "lnr.json"), "w") as f:
    json.dump(res, f, indent=1, default=float)
print(f"\n{sum(v['pass'] for v in CHECKS.values())}/{len(CHECKS)} checks pass")
