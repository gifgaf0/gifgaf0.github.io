#!/usr/bin/env python3
"""
E5 numerics: the B = 1 hedgehog in ANW conventions and its static electromagnetic properties.

Conventions (PLAN.md E2/E5): L = (F^2/16) Tr dU dU^+ + (1/32e^2) Tr[L_mu,L_nu]^2 [+ (F^2 m^2/16) Tr(U+U^+-2)],
F = F_pi in the 186-MeV convention (f_pi = F/2), x = e F r, beta = m_pi/(e F).

Profile ODE (derived from the energy functional; verified symbolically in symbolic_derivations.py):
  (x^2/4 + 2 s^2) F'' = s c/2 + 2 s^3 c/x^2 - 2 s c F'^2 - x F'/2 + beta^2 x^2 s/4,   s = sin F, c = cos F
  F(0) = pi;  massless: F ~ C/x^2 - C^3/(21 x^6) (analytic tail, BC applied at x = X);
              massive : F ~ C' k_1(beta x) (BC F'/F = d ln k_1/dx at x = X).
Static EM formulas (derived in symbolic_derivations.py):
  <r^2>_{I=0} = -(2/pi) int r^2 s^2 F' dr      (normalised baryon density)
  mu_{p,n}   = 2 M_N [ <r^2>_{I=0}/(12 lambda) +- lambda/6 ]   (nuclear magnetons, M_N = 939 MeV)
  g_A        = (pi/(3e^2)) |int x^2 D dx| = 2 pi C/(3 e^2)  (massless; pion-pole shape factor 3/2 included)
  g_piNN     = 2 M_N g_A / F   (Goldberger-Treiman, 186-convention)
Outputs: hedgehog_results.json, fig_charge_densities.png (convergence table in hedgehog_log.txt / JSON).
"""
import json, math, os, sys, time
import numpy as np
from scipy.integrate import solve_bvp, solve_ivp, quad
from scipy.optimize import brentq

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
HBARC = 197.3269804           # MeV fm
M_N = 939.0                   # MeV (ANW's nucleon mass, used in the magneton and the fits)
PI = math.pi


def log(*a):
    print(*a); sys.stdout.flush()


# ------------------------------------------------------------------ ODE
def rhs(x, y, beta):
    F, G = y
    s, c = np.sin(F), np.cos(F)
    num = 0.5 * s * c + 2 * s**3 * c / x**2 - 2 * s * c * G**2 - 0.5 * x * G + 0.25 * beta**2 * x**2 * s
    den = 0.25 * x**2 + 2 * s**2
    return np.vstack([G, num / den])


def dlnk1(beta, X):
    z = beta * X
    return beta * (-1.0 - (z + 2.0) / (z * (z + 1.0)))


def series_b(a, beta):
    """x^3 coefficient of F = pi + a x + b x^3 + ... near x = 0 (from the profile ODE)."""
    return (-(a**3 / 3.0) * (1 + 2 * a**2) - beta**2 * a / 4.0) / (2.5 + 20 * a**2)


def solve_profile(beta=0.0, X=100.0, x0=1e-2, tol=1e-10, nodes=3000, guess=None):
    x = np.geomspace(x0, X, nodes)
    if guess is None:
        R = 2.08
        F = 2 * np.arctan((R / x)**2) if beta == 0 else 2 * np.arctan((R / x)**2) * np.exp(-beta * x)
        G = np.gradient(F, x)
        y = np.vstack([F, G])
    else:
        y = guess.sol(x)

    def bc(ya, yb):
        # third-order regular series at the origin: F = pi + a x + b(a) x^3 (b derived from the ODE)
        a = ya[1]
        for _ in range(3):
            a = ya[1] - 3 * series_b(a, beta) * x0**2
        left = ya[0] - PI - a * x0 - series_b(a, beta) * x0**3
        if beta == 0:
            Ct = yb[0] * X**2
            right = yb[1] + 2 * yb[0] / X - 4 * Ct**3 / (21 * X**7)
        else:
            right = yb[1] - dlnk1(beta, X) * yb[0]
        return np.array([left, right])

    sol = solve_bvp(lambda xx, yy: rhs(xx, yy, beta), bc, x, y, tol=tol, max_nodes=2_000_000, bc_tol=1e-12)
    if not sol.success:
        raise RuntimeError("solve_bvp failed: " + sol.message)
    sol.beta, sol.X, sol.x0 = beta, X, x0
    return sol


# ------------------------------------------------------------------ integrals
def panels(x0, X, n=400):
    edges = np.unique(np.concatenate([np.geomspace(x0, X, n), [1.0, 2.0, 5.0]]))
    return edges[(edges >= x0) & (edges <= X)]


GLX, GLW = np.polynomial.legendre.leggauss(12)


def integrate(fun, sol, a=None, b=None):
    a = sol.x0 if a is None else a
    b = sol.X if b is None else b
    edges = panels(a, b)
    tot = 0.0
    if a == sol.x0:
        # [0, x0]: integrand ~ k x^p near the origin; p estimated from x0 and x0/2 (series values)
        xa = np.array([0.5 * a, a])
        aa = sol.sol(a)[1]
        bb = series_b(aa, sol.beta)
        Fs = PI + aa * xa + bb * xa**3
        Gs = aa + 3 * bb * xa**2
        fv = fun(xa, Fs, Gs)
        if abs(fv[1]) > 0 and abs(fv[0]) > 0:
            pexp = math.log(abs(fv[1] / fv[0])) / math.log(2.0)
            tot += a * fv[1] / (pexp + 1.0)
    for lo, hi in zip(edges[:-1], edges[1:]):
        xm, xr = 0.5 * (hi + lo), 0.5 * (hi - lo)
        xx = xm + xr * GLX
        F, G = sol.sol(xx)
        tot += xr * np.dot(GLW, fun(xx, F, G))
    return tot


def dens(name, beta):
    """Radial integrands in x (already multiplied by x^2 where appropriate; 4 pi not included)."""
    s = np.sin; c = np.cos
    if name == "energy":      # M = 4 pi (F/e) int
        return lambda x, F, G: x**2 * (0.125 * (G**2 + 2 * s(F)**2 / x**2)
                                       + 0.5 * (s(F)**2 / x**2) * (s(F)**2 / x**2 + 2 * G**2)
                                       + 0.25 * beta**2 * (1 - c(F)))
    if name == "E2":
        return lambda x, F, G: x**2 * 0.125 * (G**2 + 2 * s(F)**2 / x**2)
    if name == "E4":
        return lambda x, F, G: x**2 * 0.5 * (s(F)**2 / x**2) * (s(F)**2 / x**2 + 2 * G**2)
    if name == "Emass":
        return lambda x, F, G: x**2 * 0.25 * beta**2 * (1 - c(F))
    if name == "Lambda":      # lambda = (2 pi/3) Lambda / (e^3 F)
        return lambda x, F, G: x**2 * s(F)**2 * (1 + 4 * (G**2 + s(F)**2 / x**2))
    if name == "K2":          # I2 = (pi/2) K2 / (e^3 F)
        return lambda x, F, G: x**2 * (1 - c(F)) * (1 + G**2 + 2 * s(F)**2 / x**2)
    if name == "B":           # baryon number = -(2/pi) int s^2 F'
        return lambda x, F, G: -(2 / PI) * s(F)**2 * G
    if name == "R2":
        return lambda x, F, G: -(2 / PI) * x**2 * s(F)**2 * G
    if name == "R4":
        return lambda x, F, G: -(2 / PI) * x**4 * s(F)**2 * G
    if name == "D":           # g_A (massless) = (pi/(3 e^2)) |int D|
        return lambda x, F, G: x**2 * (G + np.sin(2 * F) / x + 4 * (np.sin(2 * F) * G**2 / x
                                       + 2 * s(F)**2 * G / x**2 + s(F)**2 * np.sin(2 * F) / x**3))
    if name == "Lambda_r2":   # isovector charge <r^2>: int x^2 * [x^2 s^2(1+4(..))]
        return lambda x, F, G: x**4 * s(F)**2 * (1 + 4 * (G**2 + s(F)**2 / x**2))
    raise KeyError(name)


def tail_C(sol):
    """massless: C from F(X) X^2 = C - C^3/(21 X^4)."""
    X = sol.X
    Fx = float(sol.sol(X)[0]) * X**2
    C = Fx
    for _ in range(20):
        C = Fx + C**3 / (21 * X**4)
    return C


def static_dimensionless(sol):
    """All dimensionless integrals with analytic tails beyond X (massless) or none (massive)."""
    beta, X = sol.beta, sol.X
    out = {}
    for k in ["energy", "E2", "E4", "Emass", "Lambda", "K2", "B", "R2", "R4", "D"]:
        out[k] = integrate(dens(k, beta), sol)
    if beta == 0:
        C = tail_C(sol)
        out["C"] = C
        # analytic tails from F = C/x^2 (leading order)
        out["energy"] += C**2 / (4 * X**3); out["E2"] += C**2 / (4 * X**3)
        out["Lambda"] += C**2 / X
        out["K2"] += C**2 / (2 * X)
        out["B"] += 0.0
        out["R2"] += C**3 / (PI * X**4)
        out["R4"] += 2 * C**3 / (PI * X**2)
        # D integrand -> x^2[(F'+sin2F/x) + Skyrme] ~ -(8/7) C^3/x^5 (with F = C/x^2 - C^3/(21x^6))
        out["D"] += -(2.0 / 7.0) * C**3 / X**4
    else:
        out["C"] = float("nan")
    F0, G0 = sol.sol(sol.x0)
    out["Fprime0"] = float(G0 - 3 * series_b(G0, beta) * sol.x0**2)
    out["Mtilde"] = 4 * PI * out["energy"]
    out["lam_tilde"] = (2 * PI / 3) * out["Lambda"]
    out["I2_tilde"] = (PI / 2) * out["K2"]
    out["virial_E2_minus_E4_plus_3Em_over_E"] = (out["E2"] - out["E4"] + 3 * out["Emass"]) / out["energy"]
    return out


def physical(d, Fpi, e, beta=0.0, gA_rule="massless"):
    """Physical observables at (F_pi [186-conv, MeV], e)."""
    L = HBARC / (e * Fpi)                 # fm per unit x
    lam = d["lam_tilde"] / (e**3 * Fpi)   # MeV^-1
    I2 = d["I2_tilde"] / (e**3 * Fpi)
    M = d["Mtilde"] * Fpi / e
    r2_0 = d["R2"] / (e * Fpi)**2         # MeV^-2
    r4_0 = d["R4"] / (e * Fpi)**4
    mu_s = 2 * M_N * r2_0 / (12 * lam)    # isoscalar part (each nucleon), n.m.
    mu_v = 2 * M_N * lam / 6              # isovector part
    if gA_rule == "massless":
        gA = (PI / 3) * abs(d["D"]) / e**2
    else:                                  # massive pions: no pion-pole shape factor at q = 0
        gA = (2.0 / 3.0) * (PI / 3) * abs(d["D"]) / e**2
    return {
        "F_pi_MeV": Fpi, "e": e, "f_pi_MeV": Fpi / 2,
        "M_cl_MeV": M, "lambda_inv_MeV": 1 / lam, "I2_inv_MeV": 1 / I2,
        "M_N_rotor_MeV": M + 3 / (8 * lam), "M_Delta_rotor_MeV": M + 15 / (8 * lam),
        "r_I0_fm": math.sqrt(d["R2"]) * L,
        "r2_I0_fm2": d["R2"] * L**2,
        "rM_I0_ANW_def_fm": math.sqrt(d["R4"] / d["R2"]) * L,
        "rM_I0_Sachs_fm": math.sqrt(0.6 * d["R4"] / d["R2"]) * L,
        "mu_p": mu_s + mu_v, "mu_n": mu_s - mu_v, "mu_p_over_mu_n": (mu_s + mu_v) / (mu_s - mu_v),
        "mu_isoscalar_p_plus_n": 2 * mu_s, "mu_isovector_p_minus_n": 2 * mu_v,
        "g_A": gA, "g_piNN_GT": 2 * M_N * gA / Fpi,
    }


def fit_su2(d, MN=939.0, MD=1232.0):
    lam = 3.0 / (2.0 * (MD - MN))
    P = d["lam_tilde"] / lam                       # e^3 F
    Q = (MN - 3.0 / (8.0 * lam)) / d["Mtilde"]      # F/e
    e = (P / Q)**0.25
    return Q * e, e


def fit_su3(d, E8, E10):
    I1 = 3.0 / (2.0 * (E10 - E8))
    P = d["lam_tilde"] / I1                         # e^3 F
    I2 = d["I2_tilde"] / P
    Q = (E8 - 3.0 / (8.0 * I1) - 3.0 / (4.0 * I2)) / d["Mtilde"]
    e = (P / Q)**0.25
    return Q * e, e, I1, I2


# ------------------------------------------------------------------ shooting cross-check (massless)
def shoot(a, X=40.0, x0=1e-2):
    b = series_b(a, 0.0)
    y0 = [PI + a * x0 + b * x0**3, a + 3 * b * x0**2]
    sol = solve_ivp(lambda x, y: rhs(np.array([x]), np.array(y).reshape(2, 1), 0.0).ravel(),
                    (x0, X), y0, rtol=1e-12, atol=1e-14, method="DOP853")
    F, G = sol.y[:, -1]
    if sol.status != 0:
        return float("nan")
    return G + 2 * F / X


def main():
    res = {"conventions": {
        "lagrangian": "(F^2/16) Tr dU dU^+ + (1/32 e^2) Tr[L_mu,L_nu]^2 (+ (F^2 m^2/16) Tr(U+U^+-2) for the massive variant)",
        "F_pi": "186-MeV convention (f_pi = F_pi/2)", "x": "e F_pi r", "hbar_c_MeV_fm": HBARC, "M_N_MeV": M_N}}

    # ---------------- convergence study (massless)
    log("== convergence study (massless) ==")
    conv = []
    base = None
    for X in [25.0, 50.0, 100.0, 200.0, 400.0]:
        for tol in ([1e-8, 1e-10] if X == 100.0 else [1e-10]):
            sol = solve_profile(0.0, X=X, tol=tol, guess=base)
            d = static_dimensionless(sol)
            row = {"X": X, "tol": tol, "nodes": int(sol.x.size), "Fprime0": d["Fprime0"], "C": d["C"],
                   "Mtilde": d["Mtilde"], "Lambda": d["Lambda"], "K2": d["K2"], "R2": d["R2"], "R4": d["R4"],
                   "D": d["D"], "B": d["B"], "virial": d["virial_E2_minus_E4_plus_3Em_over_E"]}
            conv.append(row)
            log("X=%6.0f tol=%.0e nodes=%6d F'(0)=%.7f C=%.6f M/(3pi^2)=%.7f Lambda=%.5f K2=%.5f R2=%.6f R4=%.5f D=%.5f B=%.9f vir=%.1e"
                % (X, tol, sol.x.size, d["Fprime0"], d["C"], d["Mtilde"] / (3 * PI**2), d["Lambda"], d["K2"],
                   d["R2"], d["R4"], d["D"], d["B"], d["virial_E2_minus_E4_plus_3Em_over_E"]))
            if X == 100.0 and tol == 1e-10:
                base = sol
    x0chk = static_dimensionless(solve_profile(0.0, X=100.0, x0=3e-3, tol=1e-10, guess=base))
    log("x0=3e-3 check: F'(0)=%.7f Lambda=%.5f R2=%.6f" % (x0chk["Fprime0"], x0chk["Lambda"], x0chk["R2"]))
    res["convergence_massless"] = conv
    res["x0_check"] = {"x0": 3e-3, "Fprime0": x0chk["Fprime0"], "Lambda": x0chk["Lambda"], "R2": x0chk["R2"], "D": x0chk["D"]}

    ref = solve_profile(0.0, X=200.0, tol=1e-10, guess=base)
    d0 = static_dimensionless(ref)
    # spread over X in {100,200,400} at tol 1e-10 as the numerical uncertainty
    keys = ["Mtilde", "Lambda", "K2", "R2", "R4", "D", "C", "Fprime0"]
    sel = [r for r in conv if r["tol"] == 1e-10 and r["X"] >= 100]
    spread = {k: max(abs(r[k] - d0[k]) for r in sel) for k in keys}
    res["massless_dimensionless"] = {k: d0[k] for k in keys + ["B", "E2", "E4", "lam_tilde", "I2_tilde", "virial_E2_minus_E4_plus_3Em_over_E"]}
    res["massless_dimensionless"]["M_over_3pi2"] = d0["Mtilde"] / (3 * PI**2)
    res["massless_dimensionless"]["numerical_spread_X100_400"] = spread
    # (reconciliation) the short boxes X = 25, 50 are less accurate; record their relative deviation from the X = 200 reference
    short = {}
    for r_ in conv:
        if r_["X"] < 100:
            short["X=%d" % r_["X"]] = {k: abs(r_[k] - d0[k]) / abs(d0[k]) for k in ["Lambda", "C", "Mtilde", "R2"]}
            short["X=%d" % r_["X"]]["B_minus_1"] = r_["B"] - 1.0
    res["massless_dimensionless"]["relative_deviation_short_boxes"] = short
    rel100 = max(abs(r_["Lambda"] - d0["Lambda"]) / d0["Lambda"] for r_ in sel)
    log("relative deviation from X=200 reference: X=100-400 Lambda <= %.1e; " % rel100
        + "; ".join("%s Lambda %.1e C %.1e B-1 %.1e" % (k, v["Lambda"], v["C"], v["B_minus_1"]) for k, v in short.items()))
    res["massless_dimensionless"]["gA_tail_coefficient_2piC_over_3"] = 2 * PI * d0["C"] / 3
    res["massless_dimensionless"]["gA_D_formula_pi_over_3_absD"] = PI / 3 * abs(d0["D"])

    # shooting cross-check
    a_star = brentq(shoot, -1.02, -0.99, xtol=1e-13)
    res["shooting_Fprime0_X40"] = a_star
    log("shooting F'(0) (X=40) = %.8f   vs BVP %.8f" % (a_star, d0["Fprime0"]))

    # Derrick: without the Skyrme term, E(lambda-scaled) = lambda^-1 E2 -> collapse
    res["derrick_scaling"] = {"E2": d0["E2"], "E4": d0["E4"], "E2_over_E4": d0["E2"] / d0["E4"],
                              "note": "under x -> x/l: E2 -> l E2, E4 -> E4/l; stationary only if E2 = E4; with E4 = 0, dE/dl = E2 > 0 so shrinking lowers E"}

    # cross-check against the symbolically derived densities if available
    symp = os.path.join(HERE, "symbolic_results.json")
    if os.path.exists(symp):
        import sympy as sp
        sj = json.load(open(symp))
        s_, c_, Fp_, r_ = sp.symbols('s c Fp r', real=True)
        fs = {k: sp.lambdify((s_, c_, Fp_, r_), sp.sympify(sj[k]), "numpy") for k in
              ["energy_density", "vector_g", "axial_sphere_density_f1_plus_f2_over_3", "lambda_density_derived_from_isospin_charge"]}
        Eint = integrate(lambda x, F, G: 4 * PI * x**2 * fs["energy_density"](np.sin(F), np.cos(F), G, x), ref) + 4 * PI * d0["C"]**2 / (4 * ref.X**3)
        gint = integrate(lambda x, F, G: 4 * PI * x**2 * x * fs["vector_g"](np.sin(F), np.cos(F), G, x), ref)
        gint += 1.5 * (2 * PI / 3) * d0["C"]**2 / ref.X          # analytic tail of int r g d^3x (= 3/2 x lambda tail)
        Ga = integrate(lambda x, F, G: 4 * PI * x**2 * fs["axial_sphere_density_f1_plus_f2_over_3"](np.sin(F), np.cos(F), G, x), ref)
        lamI = integrate(lambda x, F, G: 4 * PI * x**2 * fs["lambda_density_derived_from_isospin_charge"](np.sin(F), np.cos(F), G, x), ref) + (2 * PI / 3) * d0["C"]**2 / ref.X
        res["derived_density_crosscheck"] = {
            "M_from_derived_energy_density": Eint, "M_closed_form": d0["Mtilde"],
            "int_r_g_d3x": gint, "1.5_lambda_tilde": 1.5 * d0["lam_tilde"],
            "lambda_from_isospin_charge": lamI, "lambda_closed_form": d0["lam_tilde"],
            "G_sphere_axial": Ga, "pi_over_3_D": PI / 3 * d0["D"], "2piC_over_3": 2 * PI * d0["C"] / 3}
        log("derived-density cross-check:", json.dumps(res["derived_density_crosscheck"]))

    # ---------------- ANW parameters (published, rounded): F = 129 MeV, e = 5.45 (fitted inputs)
    anw = physical(d0, 129.0, 5.45)
    res["ANW_parameters"] = anw
    log("== ANW parameters F=129, e=5.45 ==")
    for k, v in anw.items():
        log("  %-24s %.5g" % (k, v))
    # own SU(2) refit to M_N = 939, M_Delta = 1232
    Ffit, efit = fit_su2(d0)
    own = physical(d0, Ffit, efit)
    res["own_SU2_fit"] = own
    log("== own SU(2) fit: F=%.3f MeV e=%.4f ==" % (Ffit, efit))
    for k in ["M_cl_MeV", "M_N_rotor_MeV", "M_Delta_rotor_MeV", "r_I0_fm", "rM_I0_ANW_def_fm", "rM_I0_Sachs_fm", "mu_p", "mu_n", "mu_p_over_mu_n", "g_A", "g_piNN_GT"]:
        log("  %-24s %.5g" % (k, own[k]))

    # ---------------- SU(3) refit to PDG 2026 octet and decuplet centres
    masses = pdg_masses()
    E8 = np.mean(masses["octet"]); E10 = np.mean(masses["decuplet"])
    F3, e3, I1s, I2s = fit_su3(d0, E8, E10)
    su3 = physical(d0, F3, e3)
    su3.update({"E8_centre_MeV": E8, "E10_centre_MeV": E10, "I1_inv_MeV": 1 / I1s, "I2_inv_MeV": 1 / I2s,
                "E10bar_MeV": E8 + 3 / (2 * I2s),
                "E27_J12_MeV": E8 + (8 - 3) / (2 * I2s),          # C2(27)=8 vs C2(8)=3, same J
                "E27_J32_MeV": E8 + (8 - 3) / (2 * I2s) + 3 / (2 * I1s) - 3 / (2 * I2s),
                "SU3_octet_minus_SU2_nucleon_at_ANW_MeV": 3 / (4 * d0["I2_tilde"] / (5.45**3 * 129.0)),
                "mass_inputs": masses})
    res["own_SU3_fit"] = su3
    log("== own SU(3) fit to E8=%.2f E10=%.2f: F=%.3f e=%.4f f=F/2=%.3f; 10bar at %.1f ==" % (E8, E10, F3, e3, F3 / 2, su3["E10bar_MeV"]))

    # ---------------- charge dressing: isovector radius with massless pions
    Lam_full = d0["Lambda"]
    C = d0["C"]
    cut = []
    for R in [2, 5, 10, 20, 50, 100, 200]:
        num = integrate(dens("Lambda_r2", 0.0), ref, b=float(R))
        cut.append({"R_x": R, "R_fm_ANW": R * HBARC / (5.45 * 129.0), "r2_I1_x2": num / Lam_full,
                    "asymptotic_slope_C2_over_Lambda": C**2 / Lam_full})
    res["isovector_radius_cutoff_massless"] = cut
    log("isovector <r^2>(R) [x^2 units]: " + ", ".join("R=%g: %.3f" % (c_["R_x"], c_["r2_I1_x2"]) for c_ in cut)
        + "   slope C^2/Lambda = %.4f" % (C**2 / Lam_full))

    # ---------------- massive pions (optional, no target): m_pi = 138 MeV
    log("== massive pions ==")
    mpi = 138.0
    sol_m = None
    Fm, em = 108.0, 4.84
    massive = {}
    for name, (Fpar, epar) in {"AN84_parameters": (108.0, 4.84)}.items():
        beta = mpi / (epar * Fpar)
        sol_m = solve_profile(beta, X=60.0, tol=1e-10)
        dm = static_dimensionless(sol_m)
        ph = physical(dm, Fpar, epar, beta, gA_rule="massive")
        L = HBARC / (epar * Fpar)
        Rv = integrate(dens("Lambda_r2", beta), sol_m) / dm["Lambda"]
        r2_1 = Rv * L**2
        ph.update({"beta": beta, "r_I1_fm": math.sqrt(r2_1), "r2_I1_fm2": r2_1,
                   "r_p_fm": math.sqrt(0.5 * (ph["r2_I0_fm2"] + r2_1)),
                   "r2_n_fm2": 0.5 * (ph["r2_I0_fm2"] - r2_1),
                   "g_A_naive_D_formula": (PI / 3) * abs(dm["D"]) / epar**2,
                   "virial": dm["virial_E2_minus_E4_plus_3Em_over_E"]})
        massive[name] = ph
        sol_check = solve_profile(beta, X=40.0, tol=1e-10)
        dm2 = static_dimensionless(sol_check)
        ph["X_check_Lambda_rel"] = abs(dm2["Lambda"] - dm["Lambda"]) / dm["Lambda"]
        log("  %s beta=%.4f: M_N=%.1f M_D=%.1f r0=%.3f rI1=%.3f rp=%.3f <r2>n=%.3f mu_p=%.3f mu_n=%.3f gA=%.3f gpiNN=%.2f"
            % (name, beta, ph["M_N_rotor_MeV"], ph["M_Delta_rotor_MeV"], ph["r_I0_fm"], ph["r_I1_fm"], ph["r_p_fm"],
               ph["r2_n_fm2"], ph["mu_p"], ph["mu_n"], ph["g_A"], ph["g_piNN_GT"]))
    # own massive refit (iterate beta)
    Fi, ei = 108.0, 4.84
    for it in range(30):
        beta = mpi / (ei * Fi)
        sm = solve_profile(beta, X=60.0, tol=1e-10)
        dm = static_dimensionless(sm)
        Fn, en = fit_su2(dm)
        if abs(Fn - Fi) < 1e-6 and abs(en - ei) < 1e-8:
            Fi, ei = Fn, en
            break
        Fi, ei = Fn, en
    phf = physical(dm, Fi, ei, mpi / (ei * Fi), gA_rule="massive")
    massive["own_fit_mpi138"] = {"F_pi_MeV": Fi, "e": ei, "iterations": it + 1, "M_N_rotor_MeV": phf["M_N_rotor_MeV"],
                                 "M_Delta_rotor_MeV": phf["M_Delta_rotor_MeV"]}
    log("  own massive fit: F=%.3f MeV e=%.4f (AN84 quoted 108, 4.84)" % (Fi, ei))
    res["massive_pions"] = massive

    # ---------------- figures
    try:
        make_figures(ref, d0, sol_m, massive["AN84_parameters"], conv)
    except Exception as ex:
        log("figure error:", ex)

    res["runtime_s"] = round(time.time() - T0, 1)
    with open(os.path.join(HERE, "hedgehog_results.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    log("done in %.1f s" % res["runtime_s"])


def pdg_masses():
    try:
        import pdg
        api = pdg.connect()
        get = lambda nm: api.get_particles_by_name(nm)[0].mass * 1000.0
        octet = [get("p"), get("n"), get("Lambda"), get("Sigma+"), get("Sigma0"), get("Sigma-"), get("Xi0"), get("Xi-")]
        dec = [1232.0] * 4 + [get("Sigma(1385)+"), get("Sigma(1385)0"), get("Sigma(1385)-"),
                              get("Xi(1530)0"), get("Xi(1530)-"), get("Omega-")]
        src = "PDG 2026 (pdg package); Delta(1232) = 1232 MeV (Breit-Wigner, PDG range 1230-1234)"
    except Exception as ex:    # fallback values (PDG 2026, as read during the literature pass)
        octet = [938.272, 939.565, 1115.683, 1189.370, 1192.642, 1197.449, 1314.861, 1321.711]
        dec = [1232.0] * 4 + [1382.833, 1383.815, 1387.183, 1531.801, 1534.972, 1672.452]
        src = "hard-coded PDG 2026 values (pdg package unavailable: %s)" % ex
    return {"octet": octet, "decuplet": dec, "source": src}


def make_figures(ref, d0, sol_m, ph_m, conv):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.6), dpi=110)
    # ANW massless densities
    e, F = 5.45, 129.0
    L = HBARC / (e * F)
    x = np.geomspace(1e-3, 60, 1500)
    Fx, Gx = ref.sol(x)
    rho0 = -(2 / PI) * np.sin(Fx)**2 * Gx / L / 2                         # 4 pi r^2 rho_{I=0}, per fm, charge 1/2
    rho1 = x**2 * np.sin(Fx)**2 * (1 + 4 * (Gx**2 + np.sin(Fx)**2 / x**2)) / d0["Lambda"] / L / 2
    r = x * L
    ax[0].plot(r, rho0 + rho1, color="#1f5aa6", label="proton (massless pions)")
    ax[0].plot(r, rho0 - rho1, color="#c0392b", label="neutron (massless pions)")
    if sol_m is not None:
        em, Fm = ph_m["e"], ph_m["F_pi_MeV"]
        Lm = HBARC / (em * Fm)
        xm = np.geomspace(1e-3, 59, 1500)
        Fm_, Gm_ = sol_m.sol(xm)
        dm_L = integrate(dens("Lambda", ph_m["beta"]), sol_m)
        r0m = -(2 / PI) * np.sin(Fm_)**2 * Gm_ / Lm / 2
        r1m = xm**2 * np.sin(Fm_)**2 * (1 + 4 * (Gm_**2 + np.sin(Fm_)**2 / xm**2)) / dm_L / Lm / 2
        ax[0].plot(xm * Lm, r0m + r1m, color="#1f5aa6", ls="--", label="proton, m$_\\pi$=138 MeV (AN84)")
        ax[0].plot(xm * Lm, r0m - r1m, color="#c0392b", ls="--", label="neutron, m$_\\pi$=138 MeV (AN84)")
    ax[0].axhline(0, color="0.6", lw=0.6)
    ax[0].set_xlim(0, 3.0); ax[0].set_xlabel("r [fm]"); ax[0].set_ylabel("4$\\pi$r$^2\\rho_E$(r) [fm$^{-1}$]")
    ax[0].set_title("Nucleon charge densities", fontsize=10)
    ax[0].legend(fontsize=7, frameon=False)
    # cumulative isovector <r^2>
    Rs = np.geomspace(0.5, 200, 40)
    cum = [integrate(dens("Lambda_r2", 0.0), ref, b=float(R)) / d0["Lambda"] * L**2 for R in Rs]
    ax[1].plot(Rs * L, cum, color="#1f5aa6", label="massless pions: grows linearly")
    if sol_m is not None:
        Rm = np.geomspace(0.5, 59, 40)
        cumm = [integrate(dens("Lambda_r2", ph_m["beta"]), sol_m, b=float(R)) / dm_L * Lm**2 for R in Rm]
        ax[1].plot(Rm * Lm, cumm, color="#e67e22", label="m$_\\pi$ = 138 MeV: converges")
    ax[1].plot(Rs * L, d0["C"]**2 / d0["Lambda"] * Rs * L**2, color="0.5", ls=":", lw=1, label="asymptote (C$^2/\\Lambda$) R")
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel("cutoff radius R [fm]"); ax[1].set_ylabel("<r$^2$>$_{I=1}$ inside R [fm$^2$]")
    ax[1].set_title("Isovector charge radius vs cutoff", fontsize=10)
    ax[1].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_charge_densities.png"))
    plt.close(fig)


if __name__ == "__main__":
    main()
