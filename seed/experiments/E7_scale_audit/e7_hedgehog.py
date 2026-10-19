#!/usr/bin/env python3
"""E7 part 1a: SU(2) Skyrme hedgehog in ANW conventions, solved independently for the scale audit.

Lagrangian (Adkins-Nappi-Witten 1983):
    L = (F_pi^2/16) Tr(d_mu U d^mu U^+) + 1/(32 e^2) Tr[U^+ d_mu U, U^+ d_nu U]^2
    (+ optional pion mass term (F_pi^2 m_pi^2/16) Tr(U + U^+ - 2))
Hedgehog U = exp(i tau.rhat F(r)), F(0) = pi, F(inf) = 0, dimensionless x = e F_pi r.

    M = 4 pi (F_pi/e) Ehat,
    Ehat = int dx [ x^2 F'^2/8 + sin^2F/4 + sin^2F F'^2 + sin^4F/(2 x^2) + beta^2 x^2 (1-cosF)/4 ],
    beta = m_pi/(e F_pi).
So a1 := M/(F_pi/e) = 4 pi Ehat (ANW: 36.5).

EOM (beta = 0):
    (x^2/4 + 2 sin^2F) F'' + (x/2) F' + sin2F F'^2 - sin2F/4 - sin^2F sin2F/x^2 [- beta^2 x^2 sinF/4] = 0.
Tail: F ~ C/x^2 (beta = 0), F ~ C (1 + beta x) e^{-beta x}/x^2 (beta > 0).

Moment of inertia I1 = (2 pi/3) Lambda/(e^3 F_pi), Lambda = int x^2 sin^2F [1 + 4 (F'^2 + sin^2F/x^2)] dx.

Radii (in units of 1/(e F_pi)):
    baryon density rho_B = -(1/(2 pi^2)) sin^2F F'/x^2, <x^2>_B = -(2/pi) int x^2 sin^2F F' dx.
    ANW isoscalar electric density = rho_B/2 (normalised to Q = 1/2), so <r^2>_{E,I=0} = <r^2>_B exactly.
    ANW isoscalar magnetic radius: <x^2>_{M,I=0} = int x^4 rho_B d^3x / int x^2 rho_B d^3x.
    energy rms radius: <x^2>_E = int x^2 eps / int eps.
    half-baryon radius x_1/2: baryon number inside x is 1 - (F - sinF cosF)/pi = 1/2.

Two independent solvers: scipy solve_bvp (collocation) and shooting on the slope at the origin.
Writes hedgehog.json and hedgehog_profile.npz. Deterministic, ~1-2 min on one core.
"""
import json, time, sys, os
import numpy as np
from scipy.integrate import solve_bvp, solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
EPS0 = 1e-4   # inner boundary


def rhs(x, y, beta=0.0):
    F, P = y
    s, c = np.sin(F), np.cos(F)
    s2F = 2 * s * c
    num = -(x / 2) * P - s2F * P**2 + s2F / 4 + s**2 * s2F / x**2 + beta**2 * x**2 * s / 4
    den = x**2 / 4 + 2 * s**2
    return np.vstack([P, num / den])


def tail_logderiv(X, beta):
    # d ln F/dx for F = C (1 + beta x) e^{-beta x} / x^2
    return beta / (1 + beta * X) - beta - 2.0 / X


def solve_profile(X=60.0, beta=0.0, tol=1e-10, nodes=4000):
    xs_ = min(5.0, 0.5 * X)
    x = np.concatenate([np.linspace(EPS0, xs_, nodes // 2), np.geomspace(xs_, X, nodes // 2)[1:]])
    # simple robust guess: F = 2 arctan((x0/x)^2) (rational, C/x^2 tail), F(0) = pi
    w = 1.5 / np.sqrt(max(1.0, beta))          # heavy pions shrink the fold roughly as beta^-1/2
    F0 = 2 * np.arctan((w / x)**2)
    P0 = np.gradient(F0, x)

    def bc(ya, yb):
        # inner: F(eps) = pi + eps F'(eps) (regular solution F = pi - a x + O(x^3));
        # outer: asymptotic log-derivative
        return np.array([ya[0] - np.pi - EPS0 * ya[1], yb[1] - tail_logderiv(X, beta) * yb[0]])

    # progressive refinement: a cold start at tol <= 1e-8 makes solve_bvp over-refine, so the
    # tolerance is tightened in steps, each run starting from the previous mesh and solution
    y = np.vstack([F0, P0])
    sol = None
    for t in [1e-4, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10]:
        if t < tol:
            break
        s_new = solve_bvp(lambda xx, yy: rhs(xx, yy, beta), bc, x, y, tol=t, max_nodes=60000, verbose=0)
        if s_new.status != 0:
            if sol is None:
                raise RuntimeError(f"solve_bvp failed: {s_new.message} (X={X}, beta={beta}, tol={t})")
            sol.achieved_tol = getattr(sol, 'achieved_tol', None)
            break
        sol = s_new
        sol.achieved_tol = t
        x, y = sol.x, sol.y
    return sol


def integrals(sol, X, beta=0.0, npts=400001):
    """Quadrature on the collocation solution plus analytic tails beyond X."""
    xs_ = min(8.0, 0.6 * X)
    x = np.concatenate([np.linspace(EPS0, xs_, npts // 2), np.geomspace(xs_, X, npts // 2)[1:]])
    F, P = sol.sol(x)
    s = np.sin(F)
    e2 = x**2 * P**2 / 8 + s**2 / 4                     # stretching (quadratic) part
    e4 = s**2 * P**2 + s**4 / (2 * x**2)                # Skyrme (quartic) part
    e0 = beta**2 * x**2 * (1 - np.cos(F)) / 4           # mass term
    lam = x**2 * s**2 * (1 + 4 * (P**2 + s**2 / x**2))
    bdens = -(2 / np.pi) * s**2 * P                      # 4 pi x^2 rho_B
    T = lambda f: np.trapezoid(f, x)
    E2, E4, E0, Lam = T(e2), T(e4), T(e0), T(lam)
    B0, B2, B4 = T(bdens), T(bdens * x**2), T(bdens * x**4)
    eps = e2 + e4 + e0
    Ex2 = T(eps * x**2)
    # analytic tails x > X for beta = 0, where F = C/x^2, F' = -2C/x^3, sinF = F:
    #   E2: 3C^2/(4x^4) -> C^2/(4X^3);  E4 ~ x^-10 (dropped);  Lambda: C^2/x^2 -> C^2/X
    #   4 pi x^2 rho_B = (4C^3/pi) x^-7:  B0 -> 2C^3/(3 pi X^6), B2 -> C^3/(pi X^4), B4 -> 2C^3/(pi X^2)
    #   x^2 eps: 3C^2/(4x^2) -> 3C^2/(4X).   With beta > 0 the tails are exponentially small.
    C = F[-1] * X**2
    tails = dict(E2=0.0, Lam=0.0, B0=0.0, B2=0.0, B4=0.0, Ex2=0.0)
    if beta == 0.0:
        tails = dict(E2=C**2 / (4 * X**3), Lam=C**2 / X, B0=2 * C**3 / (3 * np.pi * X**6),
                     B2=C**3 / (np.pi * X**4), B4=2 * C**3 / (np.pi * X**2), Ex2=0.75 * C**2 / X)
    E2 += tails['E2']; Lam += tails['Lam']; B0 += tails['B0']; B2 += tails['B2']; B4 += tails['B4']; Ex2 += tails['Ex2']
    Etot = E2 + E4 + E0
    # half-baryon radius
    Fhalf = brentq(lambda f: f - np.sin(f) * np.cos(f) - np.pi / 2, 0.1, 3.0)
    xh = brentq(lambda xx: sol.sol(xx)[0] - Fhalf, EPS0 * 2, X * 0.999)
    return dict(
        Ehat=Etot, E2=E2, E4=E4, E0=E0, a1=4 * np.pi * Etot, Lambda=Lam, B=B0,
        x2_B=B2 / B0, xrms_B=np.sqrt(B2 / B0),
        x2_M=B4 / B2, xrms_M=np.sqrt(B4 / B2),
        x2_E=Ex2 / Etot, xrms_E=np.sqrt(Ex2 / Etot),
        x_half=xh, F_half=Fhalf,
        slope0=float(-sol.sol(EPS0)[1]), C_tail=float(C), tails=tails)


def shoot_check(beta=0.0, xmax=30.0):
    """Independent solver: shooting on a = -F'(0), F = pi - a x near the origin (beta = 0 only).
    Linearised tail solutions are C/x^2 and D x; the sign of D tells overshoot from undershoot:
    F crosses zero (D < 0), F turns up (D > 0), otherwise sign(F' + 2F/x) = sign(D) at xmax."""
    def f1(x, y):
        return rhs(x, np.asarray(y).reshape(2, 1), beta)[:, 0]
    def ev_cross(x, y): return y[0]
    ev_cross.terminal = True
    def ev_turn(x, y): return y[1]
    ev_turn.terminal = True
    def sign_D(a):
        x0 = 1e-4
        s = solve_ivp(f1, (x0, xmax), [np.pi - a * x0, -a], method='DOP853', rtol=1e-13, atol=1e-15,
                      events=[ev_cross, ev_turn])
        if s.t_events[0].size:
            return -1
        if s.t_events[1].size:
            return +1
        F, P = s.y[:, -1]
        return 1 if (P + 2 * F / s.t[-1]) > 0 else -1
    lo, hi = 1.0, 4.0           # small a: undershoot (D > 0); large a: overshoot (D < 0)
    for _ in range(55):
        mid = 0.5 * (lo + hi)
        if sign_D(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    t0 = time.time()
    out = dict(conventions="ANW: L = (F_pi^2/16) Tr dU dU^+ + 1/(32 e^2) Tr[L_mu,L_nu]^2, F_pi = 186 MeV convention (ANW fit F_pi = 129 MeV), x = e F_pi r")
    # --- convergence in outer radius and tolerance
    conv = []
    best = None
    for X, tol in [(30.0, 1e-7), (60.0, 1e-7), (120.0, 1e-7), (120.0, 1e-10), (240.0, 1e-10)]:
        sol = solve_profile(X=X, tol=tol)
        r = integrals(sol, X)
        r.update(X=X, tol_requested=tol, tol_achieved=sol.achieved_tol, nodes=int(sol.x.size))
        conv.append({k: (float(v) if not isinstance(v, dict) else v) for k, v in r.items()})
        print(f"X={X:6.1f} tol={sol.achieved_tol:.0e} nodes={sol.x.size:6d}  a1={r['a1']:.6f}  E2/E4={r['E2']/r['E4']:.7f}  "
              f"Lambda={r['Lambda']:.5f}  B={r['B']:.7f}  xB={r['xrms_B']:.6f}  xM={r['xrms_M']:.6f}  "
              f"xE={r['xrms_E']:.6f}  x1/2={r['x_half']:.6f}  a=-F'(0)={r['slope0']:.6f}  C={r['C_tail']:.5f}", flush=True)
        if X == 120.0 and tol == 1e-10:
            best = (sol, r)
    sol, r = best
    out['convergence'] = conv
    # spread over the three most accurate runs as the numerical uncertainty
    keys = ['a1', 'Lambda', 'xrms_B', 'xrms_M', 'xrms_E', 'x_half', 'slope0', 'C_tail']
    spread = {k: float(np.ptp([c[k] for c in conv[2:]])) for k in keys}
    out['numerical_spread_last3'] = spread
    # independent shooting solver for the slope
    a_shoot = shoot_check()
    out['shooting_slope'] = a_shoot
    print(f"shooting a = {a_shoot:.8f}  vs collocation {r['slope0']:.8f}", flush=True)
    out['best'] = {k: (float(v) if not isinstance(v, dict) else v) for k, v in r.items()}
    # virial / Derrick check
    out['virial_E2_over_E4'] = r['E2'] / r['E4']
    # calibration vs ANW / PLAN targets
    a1_target = 1.2315 * 3 * np.pi**2
    out['calibration'] = dict(
        a1=dict(ours=r['a1'], target=a1_target, rel_tol=2e-3, rel_dev=r['a1'] / a1_target - 1,
                pass_=bool(abs(r['a1'] / a1_target - 1) < 2e-3), source="PLAN E2: M_cl = 36.5 F_pi/e = 1.2315*3pi^2 F_pi/e [read: Schechter-Weigel, Praszalowicz]"),
        Lambda=dict(ours=r['Lambda'], target=50.9, rel_tol=5e-3, rel_dev=r['Lambda'] / 50.9 - 1,
                    pass_=bool(abs(r['Lambda'] / 50.9 - 1) < 5e-3), source="PLAN E2: I1 = (2pi/3) Lambda/(e^3 F_pi), Lambda = 50.9"),
        virial=dict(ours=r['E2'] / r['E4'], target=1.0, abs_tol=1e-4, pass_=bool(abs(r['E2'] / r['E4'] - 1) < 1e-4), source="Derrick: E2 = E4"),
        baryon_number=dict(ours=r['B'], target=1.0, abs_tol=1e-6, pass_=bool(abs(r['B'] - 1) < 1e-6)),
    )
    # --- pion-mass family: c0(beta) = a1(beta) * x_rms_B(beta)
    fam = []
    for beta in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]:
        X = 120.0 if beta == 0 else min(120.0, 40.0 / beta + 4.0 / np.sqrt(beta))
        try:
            s_b = solve_profile(X=X, beta=beta, tol=1e-8)
            rb = integrals(s_b, X, beta=beta)
            fam.append(dict(beta=beta, a1=float(rb['a1']), xrms_B=float(rb['xrms_B']), xrms_E=float(rb['xrms_E']),
                            x_half=float(rb['x_half']), c0_B=float(rb['a1'] * rb['xrms_B']),
                            c0_E=float(rb['a1'] * rb['xrms_E']), c0_half=float(rb['a1'] * rb['x_half']),
                            virial_E2_minus_E4_plus_3E0=float((rb['E2'] - rb['E4'] + 3 * rb['E0']) / rb['Ehat'])))
            print(f"beta={beta:5.2f}: a1={rb['a1']:.4f} xB={rb['xrms_B']:.4f} c0_B={rb['a1']*rb['xrms_B']:.3f} "
                  f"c0_half={rb['a1']*rb['x_half']:.3f}  Derrick (E2-E4+3E0)/E={(rb['E2']-rb['E4']+3*rb['E0'])/rb['Ehat']:.2e}", flush=True)
        except Exception as ex:
            print(f"beta={beta}: FAILED {ex}", flush=True)
            fam.append(dict(beta=beta, error=str(ex)))
    out['pion_mass_family'] = fam
    # profile output
    xs = np.concatenate([np.linspace(EPS0, 10, 2000), np.geomspace(10, 120, 400)[1:]])
    Fs, Ps = sol.sol(xs)
    np.savez(os.path.join(HERE, 'hedgehog_profile.npz'), x=xs, F=Fs, dF=Ps)
    out['runtime_s'] = time.time() - t0
    with open(os.path.join(HERE, 'hedgehog.json'), 'w') as f:
        json.dump(out, f, indent=1)
    # printed checks
    print("\nCHECKS")
    for k, v in out['calibration'].items():
        print(f"  {k:14s} ours={v['ours']:.6f} target={v['target']}  {'PASS' if v['pass_'] else 'FAIL'}")
    print(f"  shooting vs collocation slope: |diff| = {abs(a_shoot - r['slope0']):.2e}")
    print(f"runtime {out['runtime_s']:.1f} s")


if __name__ == '__main__':
    main()
