"""
cc2_lnr_closed.py -- second-pass cross-check of the LNR (arXiv:0706.2341) seesaw numbers in CLOSED FORM.

Different from both the original and the first cross-check pass (which scanned alpha on a grid / used
root finding on floats): here the alpha windows and the alpha refit are exact roots of a quadratic.
The mass matrices are the ones derived from the exact F21 invariants in cc2_exact_invariants.py
(M_Maj = diag(u_i^2) + alpha offdiag; M_Dir with I3 = 1 and all four I4 couplings = beta).
Writes out/lnr_closed_cc2.json.
"""
import json, math
import sympy as sp

OUT, CHECKS = {}, {}
def check(name, ok):
    CHECKS[name] = bool(ok); print(("PASS " if ok else "FAIL ") + name)

al, be, r = sp.symbols("alpha beta r", real=True)
def maj(u, a):
    return sp.Matrix(3, 3, lambda i, j: u[i] ** 2 if i == j else a * u[i] * u[j])
def dirac(up, u, c0, g1, g2, b1, b2):
    # rows: psi5 (vev up), columns: psi1 (vev u); gamma on {(1,2),(2,3),(3,1)}, beta on {(1,3),(2,1),(3,2)}
    M = sp.zeros(3, 3)
    for i in range(3): M[i, i] = c0 * up[i] * u[i]
    for (i, j) in ((0, 1), (1, 2), (2, 0)): M[i, j] = g1 * up[i] * u[j] + g2 * up[j] * u[i]
    for (i, j) in ((0, 2), (1, 0), (2, 1)): M[i, j] = b1 * up[i] * u[j] + b2 * up[j] * u[i]
    return M
u1 = (1, 1, 1); u5 = (-1, 1, 1)
MR = maj(u1, al); MD = dirac(u5, u1, 1, be, be, be, be)
Mnu = sp.simplify(-MD * MR.inv() * MD.T)
M11 = sp.simplify(Mnu.subs({al: -1, be: -1}))
print("M_Maj(-1) =", MR.subs(al, -1).tolist(), " M_Dir(-1) =", MD.subs(be, -1).tolist())
print("M_nu(-1,-1) =", M11.tolist())
check("M_nu(alpha=beta=-1) = (1/2)[[0,1,1],[1,-4,5],[1,5,-4]] (LNR display, overall sign included)",
      sp.simplify(M11 - sp.Rational(1, 2) * sp.Matrix([[0, 1, 1], [1, -4, 5], [1, 5, -4]])) == sp.zeros(3, 3))
# exact TBM eigenvectors
v1 = sp.Matrix([2, -1, -1]); v2 = sp.Matrix([1, 1, 1]); v3 = sp.Matrix([0, -1, 1])
Mb = sp.simplify(Mnu.subs(be, -1))
lams = []
for v in (v1, v2, v3):
    w = sp.simplify(Mb * v)
    k = [i for i in range(3) if v[i] != 0][0]
    lam = sp.simplify(w[k] / v[k])
    lams.append(sp.factor(lam))
    assert sp.simplify(w - lam * v) == sp.zeros(3, 1)
print("beta=-1 eigenvalues on TBM vectors (2,-1,-1),(1,1,1),(0,-1,1):", lams)
check("beta=-1: TBM vectors are exact eigenvectors for all alpha, eigenvalues 1/(a-1), -1/(2a+1), 9/(a-1)",
      sp.simplify(lams[0] - 1 / (al - 1)) == 0 and sp.simplify(lams[1] + 1 / (2 * al + 1)) == 0 and sp.simplify(lams[2] - 9 / (al - 1)) == 0)
m1, m2, m3 = lams
rr = sp.simplify((m3 ** 2 - m1 ** 2) / (m2 ** 2 - m1 ** 2))
print("r(alpha) =", sp.factor(rr))
check("r(alpha) = 80 (2 alpha+1)^2 / (-3 alpha (alpha+2)) and r(-1) = 80/3",
      sp.simplify(rr - 80 * (2 * al + 1) ** 2 / (-3 * al * (al + 2))) == 0 and rr.subs(al, -1) == sp.Rational(80, 3))
# normal ordering |m2| > |m1|  <=>  (alpha-1)^2 > (2 alpha+1)^2  <=>  -2 < alpha < 0
no_cond = sp.solve_univariate_inequality((al - 1) ** 2 - (2 * al + 1) ** 2 > 0, al, relational=False)
print("normal-ordering region (|m2|>|m1|):", no_cond)
# windows: r(alpha) = R  <=>  (320 + 3R) alpha^2 + (320 + 6R) alpha + 80 = 0
def roots_for(R):
    R = sp.nsimplify(R)
    sol = sp.solve(sp.Eq((320 + 3 * R) * al ** 2 + (320 + 6 * R) * al + 80, 0), al)
    return sorted(float(s) for s in sol)
lo, hi = roots_for("21.3"), roots_for("45.1")
win = [(hi[0], lo[0]), (lo[1], hi[1])]
print("alpha windows (exact roots):", [(round(a, 5), round(b, 5)) for a, b in win])
OUT["alpha_windows_exact"] = win
check("alpha windows (-1.1435, -0.9462), (-0.2202, -0.1537): within 0.01 of LNR's (-1.15,-0.95), (-0.22,-0.15)",
      all(abs(x - y) < 0.01 for x, y in zip([win[0][0], win[0][1], win[1][0], win[1][1]], [-1.15, -0.95, -0.22, -0.15]))
      and all(-2 < x < 0 for w_ in win for x in w_))
rN = 2.534e-3 / 7.49e-5
ref = roots_for(sp.Rational(2534, 74.9) if False else rN)
print(f"alpha refit to r = {rN:.4f}: {ref}")
OUT["alpha_refit_exact"] = ref
check("alpha refit to r = 33.83: -1.0621 and -0.1787", abs(ref[0] + 1.0621) < 1e-4 and abs(ref[1] + 0.1787) < 1e-4)

# ---------------------------------------------------------------- haze: LNR's U_MNSP = U_-1^dagger U_TB
UTB = sp.Matrix([[sp.sqrt(sp.Rational(2, 3)), 1 / sp.sqrt(3), 0],
                 [-1 / sp.sqrt(6), 1 / sp.sqrt(3), -1 / sp.sqrt(2)],
                 [-1 / sp.sqrt(6), 1 / sp.sqrt(3), 1 / sp.sqrt(2)]])
lam = sp.symbols("lambda", positive=True)
def Um1(s):  # exact rotation with sin = s, LNR's sign: U_-1 ~ [[1, lam, 0], [-lam, 1, 0], [0, 0, 1]]
    c = sp.sqrt(1 - s ** 2)
    return sp.Matrix([[c, s, 0], [-s, c, 0], [0, 0, 1]])
U = sp.simplify(Um1(lam).T * UTB)
lin = sp.Matrix([[sp.sqrt(sp.Rational(2, 3)) * (1 + lam / 2), (1 - lam) / sp.sqrt(3), lam / sp.sqrt(2)],
                 [-(1 - 2 * lam) / sp.sqrt(6), (1 + lam) / sp.sqrt(3), -1 / sp.sqrt(2)],
                 [-1 / sp.sqrt(6), 1 / sp.sqrt(3), 1 / sp.sqrt(2)]])
lin_ok = all(sp.simplify(sp.series(U[i, j] - lin[i, j], lam, 0, 2).removeO()) == 0 for i in range(3) for j in range(3))
check("sign fixed by LNR: U_-1^T U_TB reproduces LNR's displayed U_MNSP to linear order in lambda (all 9 entries)", lin_ok)
U_other = sp.simplify(Um1(-lam).T * UTB)
lin_other = all(sp.simplify(sp.series(U_other[i, j] - lin[i, j], lam, 0, 2).removeO()) == 0 for i in range(3) for j in range(3))
check("the opposite rotation sign does NOT reproduce LNR's displayed matrix", not lin_other)
res = {}
for lab, me, mmu in (("pole", 0.51099895, 105.6583755), ("MSbar_MZ", 0.48307, 101.766)):
    L = math.sqrt(me / mmu)
    for sgn, UU in (("LNR", U), ("opposite", U_other)):
        Un = [[float(UU[i, j].subs(lam, L)) for j in range(3)] for i in range(3)]
        s13 = abs(Un[0][2]); th13 = math.degrees(math.asin(s13))
        th12 = math.degrees(math.atan2(abs(Un[0][1]), abs(Un[0][0])))
        s23sq = Un[1][2] ** 2 / (1 - s13 ** 2)
        res[f"{lab}/{sgn}"] = dict(lam=L, th13=th13, th12=th12, s13sq=s13 ** 2, s12sq=math.sin(math.radians(th12)) ** 2, s23sq=s23sq)
    # variant: rotation ANGLE = lambda (instead of sin = lambda)
    Un = [[float(U[i, j].subs(lam, math.sin(L))) for j in range(3)] for i in range(3)]
    res[f"{lab}/LNR/angle=lambda"] = dict(th13=math.degrees(math.asin(abs(Un[0][2]))), th12=math.degrees(math.atan2(abs(Un[0][1]), abs(Un[0][0]))))
for k, v in res.items(): print("  haze", k, {kk: round(vv, 5) for kk, vv in v.items()})
OUT["haze"] = res
p = res["pole/LNR"]
check("theta13 = 2.819 deg, theta12 = 32.44 deg (pole masses, LNR sign); MS-bar theta13 = 2.792 deg; opposite sign theta12 = 38.09",
      abs(p["th13"] - 2.819) < 0.001 and abs(p["th12"] - 32.44) < 0.01 and abs(res["MSbar_MZ/LNR"]["th13"] - 2.792) < 0.001
      and abs(res["pole/opposite"]["th12"] - 38.09) < 0.01)
# pulls vs NuFIT 6.0 (IC19 w/o SK-atm, NO; sigma = (3sigma edge - bf)/3 one-sided)
nf = {"s12sq": (0.307, 0.275, 0.345), "s13sq": (0.02195, 0.02023, 0.02376), "s23sq": (0.561, 0.430, 0.596)}
def pull(k, x):
    bf, a, b = nf[k]; return (x - bf) / ((b - bf) / 3 if x > bf else (bf - a) / 3)
sr = rN * math.hypot(0.19 / 7.49, 0.024 / 2.534)
pl = {k: pull(k, p[k]) for k in nf}; pl["r"] = (80 / 3 - rN) / sr
pl["s23sq_1sigma(-0.015)"] = (p["s23sq"] - 0.561) / 0.015
print("  pulls (LNR + haze, pole):", {k: round(v, 2) for k, v in pl.items()}, f" r = {rN:.3f} +- {sr:.3f}")
OUT["pulls"] = pl
check("pulls: s13sq -34.1, r -7.8, s12sq -1.8, s23sq -1.4 (3sigma/3) / -4.1 (1sigma)",
      abs(pl["s13sq"] + 34.07) < 0.05 and abs(pl["r"] + 7.82) < 0.05 and abs(pl["s12sq"] + 1.80) < 0.05
      and abs(pl["s23sq"] + 1.42) < 0.05 and abs(pl["s23sq_1sigma(-0.015)"] + 4.15) < 0.05)
# LNR exact class without haze: theta13 = 0 -> chi2 contributions
chi_noh = pull("s13sq", 0.0) ** 2 + pull("s12sq", 1 / 3) ** 2 + pull("s23sq", 0.5) ** 2
print(f"  LNR exact point without haze (alpha refitted to r): chi2 = {chi_noh:.2f} (s13 pull {pull('s13sq', 0.0):.2f})")
OUT["LNR_exact_no_haze_chi2"] = chi_noh
check("LNR-exact class (no haze, r fitted) chi2 = 1472.0 with theta13 pull -38.3", abs(chi_noh - 1472.0) < 0.1 and abs(pull("s13sq", 0) + 38.28) < 0.01)
OUT["checks"] = CHECKS; OUT["all_pass"] = all(CHECKS.values())
json.dump(OUT, open("/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/lnr_closed_cc2.json", "w"), indent=1, default=str)
print(f"\n{sum(CHECKS.values())}/{len(CHECKS)} checks pass")
