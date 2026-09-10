#!/usr/bin/env python3
# cc_p2_pv_xcheck.py — F-CONV controls on the PV step, per substrate, at k = 0.3 and k = 0.0046875 (T channel):
#  (a) settings variation: pole-extraction PV recomputed with maxdegree 10, different interval splits and a
#      different near-pole fallback threshold  -> max_rel_change vs the stage-2 D(k)
#  (b) method variation (REQUESTED_VARIATION (iii)): epsilon-regularized weight (k_M^2-q^2)/((k_M^2-q^2)^2+eps^2)
#      at eps = eps0, eps0/2, eps0/4 with quadratic Richardson extrapolation in eps -> eps_richardson_rel
import json
from mpmath import mp, mpf, quad, log, diff, pi, inf

mp.dps = 30
ph1 = json.load(open("cc_p2_phase1.json"))
ph2 = json.load(open("cc_p2_phase2.json"))
KCHECK = [0.3, 0.0046875]

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

def J_alt(phi, r, k):
    kM = r * k
    g = lambda q: q**4 * F_mp(phi, q, k)
    gk, g1, g2 = g(kM), diff(lambda q: q**4 * F_mp(phi, q, k), kM), diff(lambda q: q**4 * F_mp(phi, q, k), kM, 2)
    def h(q):
        if abs(q - kM) < mpf("1e-7") * kM:
            return -(g1 + g2 * (q - kM) / 2) / (q + kM)
        return (g(q) - gk) / (kM * kM - q * q)
    I1 = quad(h, [0, kM / 2, kM, 3 * kM / 2, 2 * kM], maxdegree=10) + gk * log(3) / (2 * kM)
    I2 = quad(lambda q: g(q) / (kM * kM - q * q), [2 * kM, 0.7, 2, 10, 60, inf], maxdegree=10)
    return I1 + I2

def J_eps(phi, r, k, eps):
    kM = r * k
    g = lambda q: q**4 * F_mp(phi, q, k)
    w = eps / (2 * kM)
    pts = sorted(set([0, max(kM - 30 * w, kM / 2), kM - w, kM, kM + w, min(kM + 30 * w, 2 * kM), 2 * kM]))
    def f(q):
        x = kM * kM - q * q
        return g(q) * x / (x * x + eps * eps)
    return quad(f, pts, maxdegree=10) + quad(f, [2 * kM, 1, 5, 30, inf], maxdegree=9)

out = {}
for name, d in ph1.items():
    VT, VL = mpf(repr(d["V_T"])), mpf(repr(d["V_L"]))
    NT, NL = 1 / (VT**4), 1 / (VT * VT * VL * VL)
    phiT = [mpf(repr(x)) for x in d["phi024"]["TT"]]
    phiL = [mpf(repr(x)) for x in d["phi024"]["TL"]]
    rL = VT / VL
    maxrel, maxeps = mpf(0), mpf(0)
    for k in KCHECK:
        kq = mpf(repr(k))
        i = ph2[name]["T"]["k"].index(k)
        D_base = mpf(repr(ph2[name]["T"]["D"][i]))
        D_alt = (NT * J_alt(phiT, mpf(1), kq) + NL * J_alt(phiL, rL, kq)) / pi
        maxrel = max(maxrel, abs(D_alt - D_base) / abs(D_base))
        # epsilon-regularized Richardson: quadratic in eps through 3 points
        Js = []
        for mode_phi, r in ((phiT, mpf(1)), (phiL, rL)):
            e0 = mpf("0.05") * (r * kq) ** 2
            vals = [J_eps(mode_phi, r, kq, e0 / 2**m) for m in range(3)]
            # fit J = J0 + a e + b e^2 at e = e0, e0/2, e0/4  ->  J0 = (vals[2]*8 - vals[1]*6 + vals[0])/3
            J0 = (8 * vals[2] - 6 * vals[1] + vals[0]) / 3
            Js.append(J0)
        D_eps = (NT * Js[0] + NL * Js[1]) / pi
        maxeps = max(maxeps, abs(D_eps - D_base) / abs(D_base))
    out[name] = {"max_rel_change": float(maxrel), "eps_richardson_rel": float(maxeps)}
    print(name, "settings-variation rel %.2e  eps-Richardson rel %.2e" % (out[name]["max_rel_change"], out[name]["eps_richardson_rel"]), flush=True)
json.dump(out, open("cc_p2_pv_xcheck.json", "w"), indent=1, sort_keys=True)
