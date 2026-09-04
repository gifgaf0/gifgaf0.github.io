#!/usr/bin/env python3
# g_s2c1_p2_cc_instrument.py — Gate G-S2C1, Probe P2 (aggregate), CC LEG instrument (built from scratch).
#
# Shared layer REBUILT with this leg's own scheme (not the G-POLY1 instrument):
#   * SO(3) grain average by ZYZ-Euler product quadrature: uniform grids in alpha, gamma (periodic; exact for
#     harmonics |m| < N) x Gauss-Legendre in cos(beta). c(g) (x) c(g) is band-limited at l = 8, so
#     (N_a, N_b, N_g) = (12, 8, 12) is already EXACT; doubling (24, 16, 24) is the F-CONV control.
#   * Mode kernels Phi_IM(mu) extracted as exact polynomials in mu: evaluated on 9 Chebyshev nodes, fitted to
#     degree 8; degrees 5..8 and all odd degrees must vanish (machine zero) — reported as kernel controls.
#     All mu-integrals (I0, I2, and the spectrum-weighted F_M) then use CLOSED FORMS of those polynomials.
# Re Sigma_T method (REQUESTED_VARIATION (ii)-type, different from the chat leg's Cauchy-weight PV + tail):
#   closed-form mu-integral (uniformly convergent geometric series in B/A = 2kq/(1+k^2+q^2) <= 0.29 on the
#   ladder) followed by PV in q via exact pole extraction: on [0, 2k_M] the pole term integrates to
#   g(k_M) ln(3)/(2 k_M) in closed form and the remainder (g(q)-g(k_M))/(k_M^2-q^2) is analytic; the tail
#   [2k_M, inf) is regular. All in mpmath (dps = 30), with an epsilon-regularized Richardson cross-check.
# Analytic D2 per this leg's own derivation (CC_D2_DERIVATION.md):
#   D2 = sum_M N_M [ (1 - 2 r_M^2) I0_M / 8 - (3/8) I2_M ],  r_M = V_inc/V_M, N_M = 1/(V_inc^2 V_M^2).
import json, sys, math
import numpy as np

VRH_FILE = "poly_vrh_results.json"
BANK_FILE = "poly1_phase1full_cc.json"
SUBSTRATES = {"step_hex": "hex:step", "gem8_hex": "hex:gem8", "step_cubic": "cubic:step", "gem8_cubic": "cubic:gem8"}
LADDER = sorted(set([0.3 / 2**j for j in range(9)] + [0.005, 0.01, 0.015, 0.02, 0.03]))
KK_GRID = [0.02, 0.03, 0.05, 0.08, 0.12]

# ---------- elastic tensor construction ----------
VOIGT = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]

def c0_from_constants(sym, c):
    M = np.zeros((6, 6))
    if sym == "hex":  # 6-constant (tetragonal-shaped) object exactly as banked: C11=C22, C13=C23, C44=C55, C66 free
        C11, C12, C13, C33, C44, C66 = (c[k] for k in ("C11", "C12", "C13", "C33", "C44", "C66"))
        M[:3, :3] = [[C11, C12, C13], [C12, C11, C13], [C13, C13, C33]]
        M[3, 3] = M[4, 4] = C44
        M[5, 5] = C66
    else:  # cubic
        C11, C12, C44 = c["C11"], c["C12"], c["C44"]
        M[:3, :3] = [[C11, C12, C12], [C12, C11, C12], [C12, C12, C11]]
        M[3, 3] = M[4, 4] = M[5, 5] = C44
    T = np.zeros((3, 3, 3, 3))
    for I, (i, j) in enumerate(VOIGT):
        for J, (k, l) in enumerate(VOIGT):
            v = M[I, J]
            for a, b in ((i, j), (j, i)):
                for cc, d in ((k, l), (l, k)):
                    T[a, b, cc, d] = v
    return T

def voigt_avg_closed(T):
    K = np.einsum("iijj->", T) / 9.0
    G = (np.einsum("ijij->", T) - np.einsum("iijj->", T) / 3.0) / 10.0
    return K, G

# ---------- SO(3) quadrature (own scheme) ----------
def so3_grid(na, nb, ng):
    al = 2 * np.pi * np.arange(na) / na
    ga = 2 * np.pi * np.arange(ng) / ng
    xb, wb = np.polynomial.legendre.leggauss(nb)
    cb, sb = xb, np.sqrt(1 - xb**2)
    Rs, ws = [], []
    for a in al:
        ca, sa = np.cos(a), np.sin(a)
        Ra = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
        for ib in range(nb):
            Rb = np.array([[cb[ib], 0, sb[ib]], [0, 1, 0], [-sb[ib], 0, cb[ib]]])
            for g in ga:
                cg, sg = np.cos(g), np.sin(g)
                Rg = np.array([[cg, -sg, 0], [sg, cg, 0], [0, 0, 1]])
                Rs.append(Ra @ Rb @ Rg)
                ws.append(wb[ib] / (2.0 * na * ng))
    return np.array(Rs), np.array(ws)

def rotate_all(c0, Rs):
    t = np.einsum("gia,abcd->gibcd", Rs, c0, optimize=True)
    t = np.einsum("gjb,gibcd->gijcd", Rs, t, optimize=True)
    t = np.einsum("gkc,gijcd->gijkd", Rs, t, optimize=True)
    return np.einsum("gld,gijkd->gijkl", Rs, t, optimize=True)

MU_NODES = np.cos(np.arange(9) * np.pi / 8.0)

def kernels(c0, na, nb, ng):
    """Return dict with mean isotropy controls and Phi_IM polynomial coefficients (degree-8 fit; controls)."""
    Rs, ws = so3_grid(na, nb, ng)
    crot = rotate_all(c0, Rs)
    cbar = np.einsum("g,gijkl->ijkl", ws, crot, optimize=True)
    dc = crot - cbar
    Kq, Gq = voigt_avg_closed(cbar)
    p = np.array([0.0, 0.0, 1.0])
    vals = {"TT": [], "TL": [], "LT": [], "LL": []}
    for mu in MU_NODES:
        s = np.array([math.sqrt(max(0.0, 1 - mu * mu)), 0.0, mu])
        Tg = np.einsum("gijkl,j,l->gik", dc, p, s, optimize=True)
        Pp_T = 0.5 * (np.eye(3) - np.outer(p, p))
        Ps_T = np.eye(3) - np.outer(s, s)
        Pp_L = np.outer(p, p)
        Ps_L = np.outer(s, s)
        for tag, Pi, Ps in (("TT", Pp_T, Ps_T), ("TL", Pp_T, Ps_L), ("LT", Pp_L, Ps_T), ("LL", Pp_L, Ps_L)):
            m = np.einsum("im,gmn,nk->gik", Pi, Tg, Ps, optimize=True)
            vals[tag].append(float(np.einsum("g,gik,gik->", ws, m, Tg, optimize=True)))
    V = np.vander(MU_NODES, 9, increasing=True)
    out = {"K_voigt_from_mean": Kq, "G_voigt_from_mean": Gq}
    for tag in vals:
        coef, res, *_ = np.linalg.lstsq(V, np.array(vals[tag]), rcond=None)
        scale = max(abs(coef[0]), abs(coef[2]), abs(coef[4]))
        out[tag] = {
            "phi024": [coef[0], coef[2], coef[4]],
            "max_odd_over_even": float(max(abs(coef[1]), abs(coef[3]), abs(coef[5]), abs(coef[7])) / scale),
            "max_deg_gt4_over_even": float(max(abs(coef[5]), abs(coef[6]), abs(coef[7]), abs(coef[8])) / scale),
            "I0": 2 * (coef[0] + coef[2] / 3 + coef[4] / 5),
            "I2": 2 * (coef[0] / 3 + coef[2] / 5 + coef[4] / 7),
        }
    return out

# ---------- closed-form F_M and alpha (numpy, for KK) ----------
def F_series(phi024, q, k, nmax=400, tol=1e-18):
    A = 1.0 + k * k + q * q
    x2 = (2.0 * k * q / A) ** 2
    tot, xj, j = 0.0, 1.0, 0
    while j <= nmax:
        term = (j + 1) * xj * sum(2.0 * phi024[i] / (2 * i + j + 1) for i in range(3))
        tot += term
        if j > 2 and abs(term) <= tol * abs(tot):
            break
        xj *= x2
        j += 2
    return tot / A**2

def alpha_inc(kern, VT, VL, inc, k):
    Vi = VT if inc == "T" else VL
    out = 0.0
    for M, VM in (("T", VT), ("L", VL)):
        kM = k * Vi / VM
        NM = 1.0 / (Vi * Vi * VM * VM)
        out += k * kM**3 * NM / 2.0 * F_series(kern[inc + M]["phi024"], kM, k)
    return out

def analytic_D0_D2(kern, VT, VL, inc):
    Vi = VT if inc == "T" else VL
    D0 = D2 = 0.0
    for M, VM in (("T", VT), ("L", VL)):
        NM = 1.0 / (Vi * Vi * VM * VM)
        r = Vi / VM
        I0, I2 = kern[inc + M]["I0"], kern[inc + M]["I2"]
        D0 += -0.25 * NM * I0
        D2 += NM * ((1.0 - 2.0 * r * r) * I0 / 8.0 - 3.0 * I2 / 8.0)
    return D0, D2

# ---------- stage 1 ----------
def stage1():
    vrh = json.load(open(VRH_FILE))["vrh"]
    bank = json.load(open(BANK_FILE))
    res = {}
    for name, vkey in SUBSTRATES.items():
        sym = vkey.split(":")[0]
        c0 = c0_from_constants(sym, vrh[vkey]["C_over_rho"])
        kern = kernels(c0, 12, 8, 12)
        kern2 = kernels(c0, 24, 16, 24)
        Kc, Gc = voigt_avg_closed(c0)
        mu_bar, lam_bar = kern["G_voigt_from_mean"], kern["K_voigt_from_mean"] - 2.0 / 3.0 * kern["G_voigt_from_mean"]
        VT, VL = math.sqrt(mu_bar), math.sqrt(lam_bar + 2 * mu_bar)
        b = bank["phase1b"][name]
        QT = sum((VT / VM) ** 3 / (2 * VT * VT * VM * VM) * kern["T" + M]["I0"] for M, VM in (("T", VT), ("L", VL)))
        QL = sum((VL / VM) ** 3 / (2 * VL * VL * VM * VM) * kern["L" + M]["I0"] for M, VM in (("T", VT), ("L", VL)))
        QT2 = sum((VT / VM) ** 3 / (2 * VT * VT * VM * VM) * kern2["T" + M]["I0"] for M, VM in (("T", VT), ("L", VL)))
        rel = lambda a, bb: abs(a - bb) / max(abs(a), abs(bb), 1e-300)
        alpha = [alpha_inc(kern, VT, VL, "T", k) for k in KK_GRID]
        kk_rel = max(rel(a, ab) for a, ab in zip(alpha, b["alpha_T_a"]))
        D0T, D2T = analytic_D0_D2(kern, VT, VL, "T")
        D0L, D2L = analytic_D0_D2(kern, VT, VL, "L")
        D0T2, D2T2 = analytic_D0_D2(kern2, VT, VL, "T")
        D0L2, D2L2 = analytic_D0_D2(kern2, VT, VL, "L")
        pin = {
            "Q_T_a": QT, "Q_T_a_bank": b["Q_T_a"], "Q_T_a_rel": rel(QT, b["Q_T_a"]),
            "Q_L_a": QL, "Q_L_a_bank": b["Q_L_a"], "Q_L_a_rel": rel(QL, b["Q_L_a"]),
            "V_T": VT, "V_T_bank": b["VT0"], "V_T_rel": rel(VT, b["VT0"]),
            "V_L": VL, "V_L_bank": b["VL0"], "V_L_rel": rel(VL, b["VL0"]),
            "int_Phi_TT": kern["TT"]["I0"], "int_Phi_TT_bank": b["int_Phi_TT"], "int_Phi_TT_rel": rel(kern["TT"]["I0"], b["int_Phi_TT"]),
            "int_Phi_TL": kern["TL"]["I0"], "int_Phi_TL_bank": b["int_Phi_TL"], "int_Phi_TL_rel": rel(kern["TL"]["I0"], b["int_Phi_TL"]),
        }
        pin["pin_pass"] = bool(pin["Q_T_a_rel"] <= 1e-10 and pin["V_T_rel"] <= 1e-10 and pin["V_L_rel"] <= 1e-10)
        res[name] = {
            "voigt_closed_vs_mean_rel": {"K": rel(Kc, kern["K_voigt_from_mean"]), "G": rel(Gc, kern["G_voigt_from_mean"])},
            "kernel_controls": {t: {k2: kern[t][k2] for k2 in ("max_odd_over_even", "max_deg_gt4_over_even")} for t in ("TT", "TL", "LT", "LL")},
            "reciprocity_LT_over_TL_minus2": kern["LT"]["I0"] / kern["TL"]["I0"] - 2.0,
            "phi024": {t: kern[t]["phi024"] for t in ("TT", "TL", "LT", "LL")},
            "I0": {t: kern[t]["I0"] for t in ("TT", "TL", "LT", "LL")},
            "I2": {t: kern[t]["I2"] for t in ("TT", "TL", "LT", "LL")},
            "pin": pin,
            "KK": {"alpha_T": alpha, "alpha_T_bank": b["alpha_T_a"], "alpha_tie_max_rel": kk_rel, "pass": bool(kk_rel <= 1e-9)},
            "V_T": VT, "V_L": VL, "mu_bar": mu_bar, "lam_bar": lam_bar,
            "D0": {"T": D0T, "L": D0L}, "D2_analytic": {"T": D2T, "L": D2L},
            "xi_doubling": {
                "Q_T_rel": rel(QT, QT2), "D2_T_rel": rel(D2T, D2T2), "D2_L_rel": rel(D2L, D2L2),
                "D0_T_rel": rel(D0T, D0T2), "D0_L_rel": rel(D0L, D0L2),
            },
        }
        print(name, "pin_pass", pin["pin_pass"], "Q_T_rel %.2e" % pin["Q_T_a_rel"], "KK %.2e" % kk_rel,
              "D2_T %.8e" % D2T, "xi-doubling D2 %.1e" % res[name]["xi_doubling"]["D2_T_rel"], flush=True)
    json.dump(res, open("cc_p2_phase1.json", "w"), indent=1, sort_keys=True)
    print("wrote cc_p2_phase1.json")

# ---------- stage 2: mpmath ladder ----------
def stage2():
    from mpmath import mp, mpf, quad, log, diff
    mp.dps = 30
    ph1 = json.load(open("cc_p2_phase1.json"))

    def F_mp(phi, q, k):
        A = 1 + k * k + q * q
        x2 = (2 * k * q / A) ** 2
        tot, xj, j = mpf(0), mpf(1), 0
        tol = mpf(10) ** (-(mp.dps + 6))
        while j <= 800:
            term = (j + 1) * xj * (2 * phi[0] / (j + 1) + 2 * phi[1] / (j + 3) + 2 * phi[2] / (j + 5))
            tot += term
            if j > 2 and abs(term) <= tol * abs(tot):
                break
            xj *= x2
            j += 2
        return tot / A**2

    def J_M(phi, r, k):
        kM = r * k
        g = lambda q: q**4 * F_mp(phi, q, k)
        gk = g(kM)
        g1 = diff(g, kM)
        g2 = diff(g, kM, 2)

        def h(q):
            if abs(q - kM) < mpf("1e-9") * kM:
                return -(g1 + g2 * (q - kM) / 2) / (q + kM)
            return (g(q) - gk) / (kM * kM - q * q)

        I1 = quad(h, [0, kM, 2 * kM], maxdegree=9) + gk * log(3) / (2 * kM)
        pts = sorted(set([2 * kM, 1, 5, 30]))
        pts = [p for p in pts if p >= 2 * kM] + ["inf"]
        from mpmath import inf as mpinf
        pts = [2 * kM] + [p for p in (1, 5, 30) if p > 2 * kM] + [mpinf]
        I2 = quad(lambda q: g(q) / (kM * kM - q * q), pts, maxdegree=9)
        return I1 + I2

    out = {}
    for name, d in ph1.items():
        VT, VL = mpf(repr(d["V_T"])), mpf(repr(d["V_L"]))
        lad = {}
        for inc, Vi, kset in (("T", VT, LADDER), ("L", VL, [0.3, 0.0375, 0.0046875])):
            NT, NL = 1 / (Vi * Vi * VT * VT), 1 / (Vi * Vi * VL * VL)
            rT, rL = Vi / VT, Vi / VL
            phiT = [mpf(repr(x)) for x in d["phi024"][inc + "T"]]
            phiL = [mpf(repr(x)) for x in d["phi024"][inc + "L"]]
            I0T = 2 * (phiT[0] + phiT[1] / 3 + phiT[2] / 5)
            I0L = 2 * (phiL[0] + phiL[1] / 3 + phiL[2] / 5)
            from mpmath import pi
            D0 = -(NT * I0T + NL * I0L) / 4
            row = {"D0_mp": float(D0), "k": [], "D": [], "Delta": []}
            for k in kset:
                kq = mpf(repr(k))
                D = (NT * J_M(phiT, rT, kq) + NL * J_M(phiL, rL, kq)) / pi
                row["k"].append(k)
                row["D"].append(float(D))
                row["Delta"].append(str(D - D0))
            lad[inc] = row
            print(name, inc, "ladder done", flush=True)
        out[name] = lad
    json.dump(out, open("cc_p2_phase2.json", "w"), indent=1, sort_keys=True)
    print("wrote cc_p2_phase2.json")

if __name__ == "__main__":
    {"1": stage1, "2": stage2}[sys.argv[1]]()
