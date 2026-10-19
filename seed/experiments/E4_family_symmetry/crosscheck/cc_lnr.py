"""
cc_lnr.py -- independent cross-check of the Luhn-Nasri-Ramond (arXiv:0706.2341) Z7 x| Z3 seesaw example,
its confrontation with NuFIT 6.0, and the residual-symmetry status of its M_nu.

Mass matrices written directly from LNR 0706.2341 Sec. 4.1 (their displayed general forms), in sympy:
  M_Maj(a,b,c; alpha) = [[a^2, alpha ab, alpha ac], [alpha ab, b^2, alpha bc], [alpha ac, alpha bc, c^2]]
  M_Dir = [[a'a, g1 a'b + g2 b'a, b1 a'c + b2 c'a],
           [b1 b'a + b2 a'b, b'b, g1 b'c + g2 c'b],
           [g1 c'a + g2 a'c, b1 c'b + b2 b'c, c'c]]
  M_nu = - M_Dir M_Maj^-1 M_Dir^T
Prints checks; writes out/lnr_cc.json.
"""
import json, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq

OUT, CHECKS = {}, {}
def check(name, ok):
    CHECKS[name] = bool(ok); print(("PASS " if ok else "FAIL ") + name)

al, be = sp.symbols('alpha beta')
def M_maj(v, alpha):
    a, b, c = v
    return sp.Matrix([[a * a, alpha * a * b, alpha * a * c], [alpha * a * b, b * b, alpha * b * c], [alpha * a * c, alpha * b * c, c * c]])
def M_dir(v1, v5, b1, b2, g1, g2):
    a, b, c = v1; ap, bp, cp = v5
    return sp.Matrix([[ap * a, g1 * ap * b + g2 * bp * a, b1 * ap * c + b2 * cp * a],
                      [b1 * bp * a + b2 * ap * b, bp * b, g1 * bp * c + g2 * cp * b],
                      [g1 * cp * a + g2 * ap * c, b1 * cp * b + b2 * bp * c, cp * c]])

v1 = (1, 1, 1); v5 = (-1, 1, 1)
MR = M_maj(v1, al)
MD = M_dir(v1, v5, be, be, be, be)
Mnu = sp.simplify(-MD * MR.inv() * MD.T)
MR1 = MR.subs(al, -1); MD1 = MD.subs(be, -1)
Mnu1 = sp.simplify(Mnu.subs({al: -1, be: -1}))
print("M_Maj(alpha=-1) =", MR1.tolist())
print("M_Dir(beta=-1)  =", MD1.tolist())
print("M_nu(alpha=beta=-1) =", Mnu1.tolist())
check("M_Maj = [[1,-1,-1],[-1,1,-1],[-1,-1,1]] (LNR)", MR1 == sp.Matrix([[1, -1, -1], [-1, 1, -1], [-1, -1, 1]]))
check("M_Dir = [[-1,0,0],[0,1,-2],[0,-2,1]] (LNR)", MD1 == sp.Matrix([[-1, 0, 0], [0, 1, -2], [0, -2, 1]]))
target = sp.Rational(1, 2) * sp.Matrix([[0, 1, 1], [1, -4, 5], [1, 5, -4]])
ratio_ok = any(sp.simplify(Mnu1 - s * target) == sp.zeros(3, 3) for s in (1, -1))
check("M_nu = +-(1/2)[[0,1,1],[1,-4,5],[1,5,-4]] (LNR)", ratio_ok)
OUT["Mnu_sign_vs_LNR_display"] = "+" if sp.simplify(Mnu1 - target) == sp.zeros(3, 3) else "-"
ev = sorted(Mnu1.eigenvals().keys(), key=lambda x: abs(x))
print("eigenvalues:", ev)
ratios = [sp.nsimplify(e / ev[0]) for e in ev]
check("eigenvalue ratios 1 : -2 : 9", ratios == [1, -2, 9])
r = sp.nsimplify((ev[2] ** 2 - ev[0] ** 2) / (ev[1] ** 2 - ev[0] ** 2))
print("Dm31^2/Dm21^2 =", r, float(r))
check("Dm31^2/Dm21^2 = 80/3", r == sp.Rational(80, 3))
OUT["eigenvalues"] = [str(e) for e in ev]; OUT["r"] = str(r)

# TBM: check U_TB diagonalises M_nu for every alpha at beta=-1, and the mass formula
UTB = sp.Matrix([[sp.sqrt(sp.Rational(2, 3)), 1 / sp.sqrt(3), 0], [-1 / sp.sqrt(6), 1 / sp.sqrt(3), -1 / sp.sqrt(2)], [-1 / sp.sqrt(6), 1 / sp.sqrt(3), 1 / sp.sqrt(2)]])
Mb = sp.simplify(Mnu.subs(be, -1))
Dg = sp.simplify(UTB.T * Mb * UTB)
offd = [sp.simplify(Dg[i, j]) for i in range(3) for j in range(3) if i != j]
print("U_TB^T M_nu(alpha, beta=-1) U_TB diag =", [sp.factor(Dg[i, i]) for i in range(3)])
check("beta=-1: M_nu exactly tri-bimaximal for every alpha (off-diagonal of U_TB^T M U_TB vanish)", all(o == 0 for o in offd))
m1, m2, m3 = [sp.factor(Dg[i, i]) for i in range(3)]
OUT["masses_beta_m1"] = [str(m1), str(m2), str(m3)]
check("|m3/m1| = 9 for every alpha", sp.simplify((m3 / m1) ** 2 - 81) == 0)
# masses as claimed by the original: 1/(alpha-1), -1/(2 alpha+1), 9/(alpha-1)  (up to common sign/scale)
claim = [1 / (al - 1), -1 / (2 * al + 1), 9 / (al - 1)]
sc = sp.simplify(m1 / claim[0])
check("masses proportional to (1/(a-1), -1/(2a+1), 9/(a-1)) with one common factor",
      all(sp.simplify(mi - sc * ci) == 0 for mi, ci in zip((m1, m2, m3), claim)))
# general beta: is TBM exact only at beta = -1 ? (LNR: third criterion fixes beta = -1)
Mg = sp.simplify(Mnu)
crit3 = sp.factor(sp.simplify(Mg[1, 2] - (Mg[0, 0] + Mg[0, 1] - Mg[1, 1])))
crit1 = sp.simplify(Mg[0, 1] - Mg[0, 2]); crit2 = sp.simplify(Mg[1, 1] - Mg[2, 2])
print("TBM criteria: M12-M13 =", crit1, " M22-M33 =", crit2, " M23-(M11+M12-M22) =", crit3)
sol = sp.solve(sp.numer(sp.together(crit3)), be)
print("third criterion solved for beta:", sol)
check("TBM criteria 1,2 hold identically; criterion 3 fixes beta = -1 (LNR)", crit1 == 0 and crit2 == 0 and -1 in sol)

# alpha windows: r(alpha) in [21.3, 45.1], normal ordering (|m2|>|m1|, |m3| largest)
rfun_s = sp.lambdify(al, (m3 ** 2 - m1 ** 2) / (m2 ** 2 - m1 ** 2))
def rfun(a): return float(rfun_s(a))
def NO(a):
    mm = [abs(float(sp.N(x.subs(al, a)))) for x in (m1, m2, m3)]
    return mm[1] > mm[0] and mm[2] > mm[1]
grid = np.linspace(-3, 3, 600001)
vals = np.array([rfun(a) if abs(a - 1) > 1e-9 and abs(2 * a + 1) > 1e-9 else np.nan for a in grid[::50]])
# do it properly with root finding on r - 21.3 and r - 45.1 within NO region
m1f = sp.lambdify(al, m1); m2f = sp.lambdify(al, m2); m3f = sp.lambdify(al, m3)
def ok(a):
    x1, x2, x3 = abs(m1f(a)), abs(m2f(a)), abs(m3f(a))
    if not (x2 > x1 and x3 > x2): return False
    rr = (x3 ** 2 - x1 ** 2) / (x2 ** 2 - x1 ** 2)
    return 21.3 <= rr <= 45.1
g = np.linspace(-3, 3, 600001)
mask = np.array([ok(a) if abs(a - 1) > 1e-12 and abs(2 * a + 1) > 1e-12 else False for a in g])
edges = np.flatnonzero(np.diff(mask.astype(int)))
wins = []
for i in range(0, len(edges), 2):
    wins.append((round(float(g[edges[i] + 1]), 4), round(float(g[edges[i + 1]]), 4)))
print("alpha windows (beta=-1, NO, r in [21.3,45.1]):", wins)
OUT["alpha_windows"] = wins
check("alpha windows = (-1.15,-0.95) and (-0.22,-0.15) to 0.01 (LNR)",
      len(wins) == 2 and abs(wins[0][0] + 1.15) < 0.01 and abs(wins[0][1] + 0.95) < 0.01 and abs(wins[1][0] + 0.22) < 0.01 and abs(wins[1][1] + 0.15) < 0.01)
# refit alpha to NuFIT r = 33.83
def rr(a):
    x1, x2, x3 = abs(m1f(a)), abs(m2f(a)), abs(m3f(a))
    return (x3 ** 2 - x1 ** 2) / (x2 ** 2 - x1 ** 2)
r_nufit = 2.534e-3 / 7.49e-5
roots = [brentq(lambda a: rr(a) - r_nufit, w[0], w[1]) for w in wins]
print(f"alpha giving r = {r_nufit:.3f}: {roots}")
OUT["alpha_refit"] = roots

# ---------------------------------------------------------------- haze (LNR Sec. 4.2)
UTBn = np.array(UTB.evalf(), dtype=float)
def pmns_angles(U):
    s13 = abs(U[0, 2]); c13 = math.sqrt(1 - s13 ** 2)
    s12sq = abs(U[0, 1]) ** 2 / c13 ** 2; s23sq = abs(U[1, 2]) ** 2 / c13 ** 2
    return s12sq, s13 ** 2, s23sq
def haze(lam, sign=+1, exact_angle=False):
    s = math.sin(lam) if exact_angle else lam
    c = math.sqrt(1 - s * s)
    Um1 = np.array([[c, sign * s, 0], [-sign * s, c, 0], [0, 0, 1]])   # LNR: U_-1 ~ [[1, lam, 0], [-lam, 1, 0], [0,0,1]]
    return Um1.T @ UTBn                                                 # U_MNSP = U_-1^dagger U_TB
me_pole, mmu_pole = 0.51099895, 105.6583755
me_mz, mmu_mz = 0.48307, 101.766
res_h = {}
for lab, (me, mmu) in (("pole", (me_pole, mmu_pole)), ("MSbar_MZ", (me_mz, mmu_mz))):
    lam = math.sqrt(me / mmu)
    for sign in (+1, -1):
        U = haze(lam, sign)
        s12sq, s13sq, s23sq = pmns_angles(U)
        res_h[f"{lab}_sign{sign:+d}"] = dict(lam=lam, th13=math.degrees(math.asin(math.sqrt(s13sq))), th12=math.degrees(math.atan(abs(U[0, 1]) / abs(U[0, 0]))),
                                            s12sq=s12sq, s13sq=s13sq, s23sq=s23sq)
    # LNR's linearised matrix (1,1) entry sqrt(2/3)(1+lam/2): fixes the sign
    U = haze(lam, +1)
    res_h[f"{lab}_LNR_sign_is_plus"] = bool(abs(U[0, 0] - math.sqrt(2 / 3) * (1 + lam / 2)) < lam ** 2)
for k, v in res_h.items(): print(" haze", k, v)
OUT["haze"] = res_h
hp = res_h["pole_sign+1"]
check("theta13 = 2.8 deg (+-0.05) with lambda_e = sqrt(me/mmu), pole masses", abs(hp["th13"] - 2.8) < 0.05)
check("theta12 = 32.4 deg (+-0.05) with the same haze", abs(hp["th12"] - 32.4) < 0.05)
check("LNR's displayed U_MNSP (1,1) entry sqrt(2/3)(1+lam/2) fixes the haze sign (no free choice)", res_h["pole_LNR_sign_is_plus"])

# ---------------------------------------------------------------- NuFIT 6.0 pulls (IC19 w/o SK-atm, NO), my own read of Table 1
nufit = {"s12sq": (0.307, 0.275, 0.345, 0.011, 0.012), "s23sq": (0.561, 0.430, 0.596, 0.015, 0.012),
         "s13sq": (0.02195, 0.02023, 0.02376, 0.00058, 0.00054), "delta": (177., 96., 422., 20., 19.)}
def pull(name, x, conv="3sig"):
    bf, lo, hi, s1m, s1p = nufit[name]
    if conv == "3sig":
        sm, sp_ = (bf - lo) / 3, (hi - bf) / 3
    else:
        sm, sp_ = s1m, s1p
    return (x - bf) / (sp_ if x > bf else sm)
r_err = r_nufit * math.sqrt((0.19 / 7.49) ** 2 + (0.024 / 2.534) ** 2)
pl = {"s13sq": pull("s13sq", hp["s13sq"]), "s12sq": pull("s12sq", hp["s12sq"]), "s23sq": pull("s23sq", hp["s23sq"]),
      "s23sq_1sigma": pull("s23sq", hp["s23sq"], "1sig"), "r": (80 / 3 - r_nufit) / r_err}
print(f"NuFIT r = {r_nufit:.3f} +- {r_err:.3f}; LNR+haze: s13sq={hp['s13sq']:.5f} s12sq={hp['s12sq']:.4f} s23sq={hp['s23sq']:.4f}")
print("pulls:", {k: round(v, 2) for k, v in pl.items()})
OUT["nufit_pulls_LNR_haze"] = pl; OUT["r_nufit"] = [r_nufit, r_err]
check("LNR+haze sin^2 th13 = 0.00242 and pull -34.1 (3sigma/3 convention)", abs(hp["s13sq"] - 0.00242) < 5e-6 and abs(pl["s13sq"] + 34.1) < 0.1)
check("r: 26.67 vs 33.83+-0.92, pull -7.8", abs(r_nufit - 33.83) < 0.01 and abs(r_err - 0.92) < 0.01 and abs(pl["r"] + 7.8) < 0.05)
check("s12^2 = 0.288 (pull -1.8); s23^2 = 0.499 (pull -1.4, or -4.1 with 1 sigma)",
      abs(hp["s12sq"] - 0.288) < 0.0015 and abs(pl["s12sq"] + 1.8) < 0.1 and abs(hp["s23sq"] - 0.499) < 0.0015 and abs(pl["s23sq"] + 1.4) < 0.1 and abs(pl["s23sq_1sigma"] + 4.1) < 0.1)

# ---------------------------------------------------------------- residual symmetry of LNR's M_nu inside the seed's PSL(2,7)
PSL = np.load("/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/PSL_elements.npy")
Mn = np.array(Mnu1.evalf(), dtype=float)
inv = [g for g in PSL if np.allclose(g.T @ Mn @ g, Mn, atol=1e-10)]
inv_phase = [g for g in PSL if np.linalg.matrix_rank(np.stack([(g.T @ Mn @ g).ravel(), Mn.ravel()]), tol=1e-9) == 1]
print("PSL elements g with g^T M_nu g = M_nu:", len(inv), "; up to a phase:", len(inv_phase))
S = np.array([[-1, 2, 2], [2, -1, 2], [2, 2, -1]]) / 3
U23 = -np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
inS = any(np.allclose(g, S) for g in PSL); inU = any(np.allclose(g, U23) for g in PSL)
check("M_nu invariant under TBM Klein pair S and (-)mu-tau", np.allclose(S.T @ Mn @ S, Mn) and np.allclose(U23.T @ Mn @ U23, Mn))
check("only the identity of the seed's PSL(2,7) leaves LNR's M_nu invariant; S and mu-tau not in PSL", len(inv) == 1 and np.allclose(inv[0], np.eye(3)) and not inS and not inU)
OUT["Mnu_stabilizer_in_PSL"] = len(inv); OUT["S_in_PSL"] = inS; OUT["mutau_in_PSL"] = inU
# Also for general alpha (beta=-1): any PSL element?
Mfun = sp.lambdify(al, Mb)
cnt = []
for a in (-1.0621, -0.1787, -0.6, 0.3):
    Ma = np.array(Mfun(a), dtype=float)
    cnt.append(sum(np.allclose(g.T @ Ma @ g, Ma, atol=1e-10) for g in PSL))
print("stabilizer sizes in PSL for alpha in (-1.0621,-0.1787,-0.6,0.3):", cnt)
OUT["stabilizer_general_alpha"] = cnt

OUT["checks"] = CHECKS; OUT["all_pass"] = all(CHECKS.values())
json.dump(OUT, open("/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/lnr_cc.json", "w"), indent=1, default=str)
print(f"\n{sum(CHECKS.values())}/{len(CHECKS)} checks pass")
