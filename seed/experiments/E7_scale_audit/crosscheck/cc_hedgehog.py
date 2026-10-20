#!/usr/bin/env python3
"""E7 cross-check: SU(2) Skyrme hedgehog by a Ritz (energy-minimisation) spectral method.

Independent of the original E7 code (which used solve_bvp collocation + shooting).
Method: compactified coordinate t in [0,1), x = L t/(1-t), x = e F_pi r (ANW units,
F_pi in the 186-MeV convention).  Trial profile

    F(t) = (1-t)^2 [ pi + t * sum_k c_k T_k(2t-1) ]

which has F(0) = pi and the C/x^2 tail built in.  The discretised energy (Gauss-Legendre
quadrature in t) is minimised by Newton's method with the exact analytic gradient and
Hessian of the quadrature sum.  Convergence is checked in the basis size N, the map scale
L and the quadrature order.

Energy (ANW):  M = (F_pi/e) * 4 pi int [x^2F'^2/8 + sin^2F/4 + sin^2F F'^2 + sin^4F/(2x^2)
                                      + (beta^2/4) x^2 (1 - cos F)] dx,  beta = m_pi/(e F_pi).
Deterministic; prints its own checks; writes cc_hedgehog.json.
"""
import json
import sys
import numpy as np
from numpy.polynomial import chebyshev as C
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq

PI = np.pi


def basis(t, N):
    """phi_k(t) = (1-t)^2 t T_k(2t-1) and d/dt, k = 0..N-1; plus fixed part F0 = pi (1-t)^2."""
    s = 2 * t - 1
    Phi = np.empty((N, t.size))
    dPhi = np.empty((N, t.size))
    for k in range(N):
        ck = np.zeros(k + 1); ck[k] = 1.0
        Tk = C.chebval(s, ck)
        dTk = 2 * C.chebval(s, C.chebder(ck))
        g = (1 - t) ** 2 * t
        dg = -2 * (1 - t) * t + (1 - t) ** 2
        Phi[k] = g * Tk
        dPhi[k] = dg * Tk + g * dTk
    F0 = PI * (1 - t) ** 2
    dF0 = -2 * PI * (1 - t)
    return Phi, dPhi, F0, dF0


class Hedgehog:
    def __init__(self, N=40, L=2.0, Nq=600, beta=0.0):
        self.N, self.L, self.beta = N, L, beta
        if Nq <= 2000:
            u, w = leggauss(Nq)
            t = 0.5 * (u + 1); w = 0.5 * w
        else:   # composite Gauss-Legendre: Nq//32 panels of 32 points (leggauss is O(n^3))
            u, w = leggauss(32)
            npan = Nq // 32
            edges = np.linspace(0, 1, npan + 1)
            a, b = edges[:-1, None], edges[1:, None]
            t = (0.5 * (b - a) * (u + 1) + a).ravel()
            w = (0.5 * (b - a) * w).ravel()
        self.t = t
        self.x = L * t / (1 - t)
        self.tx = (1 - t) ** 2 / L          # dt/dx
        self.W = w * L / (1 - t) ** 2       # dx = W (quadrature weight in x)
        self.Phi, self.dPhi, self.F0, self.dF0 = basis(t, N)
        self.c = np.zeros(N)

    def profile(self, c=None):
        c = self.c if c is None else c
        F = self.F0 + c @ self.Phi
        Fx = (self.dF0 + c @ self.dPhi) * self.tx
        return F, Fx

    def dens(self, F, p):
        x, b2 = self.x, self.beta ** 2
        s, co = np.sin(F), np.cos(F)
        e2 = x ** 2 * p ** 2 / 8 + s ** 2 / 4
        e4 = s ** 2 * p ** 2 + s ** 4 / (2 * x ** 2)
        e0 = b2 / 4 * x ** 2 * (1 - co)
        return e2, e4, e0

    def energy(self, c=None):
        F, p = self.profile(c)
        e2, e4, e0 = self.dens(F, p)
        return 4 * PI * np.sum(self.W * (e2 + e4 + e0))

    def grad_hess(self):
        F, p = self.profile()
        x, b2 = self.x, self.beta ** 2
        s, co = np.sin(F), np.cos(F)
        s2F, c2F = np.sin(2 * F), np.cos(2 * F)
        eF = s2F / 4 + s2F * p ** 2 + s ** 2 * s2F / x ** 2 + b2 / 4 * x ** 2 * s
        ep = x ** 2 * p / 4 + 2 * s ** 2 * p
        eFF = c2F / 2 + 2 * c2F * p ** 2 + (s2F ** 2 + 2 * s ** 2 * c2F) / x ** 2 + b2 / 4 * x ** 2 * co
        eFp = 2 * s2F * p
        epp = x ** 2 / 4 + 2 * s ** 2
        A = self.Phi
        B = self.dPhi * self.tx
        W = self.W
        g = A @ (W * eF) + B @ (W * ep)
        H = (A * (W * eFF)) @ A.T + (A * (W * eFp)) @ B.T + (B * (W * eFp)) @ A.T + (B * (W * epp)) @ B.T
        return 4 * PI * g, 4 * PI * H

    def solve(self, c0=None, tol=1e-13, maxit=200, verbose=False):
        if c0 is None:
            self.c = np.zeros(self.N); self.c[0] = 2 * PI   # F = pi (1-t)^2 (1+2t)
        else:
            self.c = np.array(c0, float)
        E = self.energy()
        for it in range(maxit):
            g, H = self.grad_hess()
            try:
                d = -np.linalg.solve(H, g)
                if g @ d > 0:      # not a descent direction: fall back to gradient
                    d = -g
            except np.linalg.LinAlgError:
                d = -g
            lam = 1.0
            while True:
                En = self.energy(self.c + lam * d)
                if En <= E + 1e-4 * lam * (g @ d) or lam < 1e-12:
                    break
                lam *= 0.5
            self.c = self.c + lam * d
            dE = E - En
            E = En
            gn = np.linalg.norm(g)
            if verbose:
                print(f"  it {it:3d}  E/(4pi)... a1 = {E:.15f}  |g| = {gn:.2e}  lam = {lam:.3g}")
            if gn < tol and lam == 1.0:
                break
        self.gnorm = np.linalg.norm(self.grad_hess()[0])
        return E


def observables(h, Nfine=40000):
    """Observables from the converged Chebyshev profile on a fine Gauss-Legendre grid."""
    hf = Hedgehog(N=h.N, L=h.L, Nq=Nfine, beta=h.beta)
    hf.c = h.c.copy()
    F, p = hf.profile()
    x, W = hf.x, hf.W
    e2, e4, e0 = hf.dens(F, p)
    E2 = 4 * PI * np.sum(W * e2); E4 = 4 * PI * np.sum(W * e4); E0 = 4 * PI * np.sum(W * e0)
    a1 = E2 + E4 + E0
    s = np.sin(F)
    Lam = np.sum(W * x ** 2 * s ** 2 * (1 + 4 * (p ** 2 + s ** 2 / x ** 2)))
    b = -(2 / PI) * s ** 2 * p                      # radial baryon density, int b dx = 1
    Bnorm = np.sum(W * b)
    xB2 = np.sum(W * x ** 2 * b)
    xM2 = np.sum(W * x ** 4 * b) / xB2              # isoscalar magnetic: <r^2 r^2 B>/<r^2 B>
    xmeanB = np.sum(W * x * b)                       # mean (not rms) baryon radius  [extra definition]
    eps = e2 + e4 + e0
    xE2 = np.sum(W * x ** 2 * eps) / np.sum(W * eps)
    # radius where F = pi/2 (= half-baryon radius, since 1-(F - sinF cosF)/pi = 1/2 at F = pi/2)
    def Fat(xx):
        tt = np.array([xx / (h.L + xx)])
        Phi, dPhi, F0, dF0 = basis(tt, h.N)
        return (F0 + h.c @ Phi)[0]
    x_half = brentq(lambda xx: Fat(xx) - PI / 2, 1e-3, 50)
    # also half baryon number directly (independent root find on the enclosed charge)
    def Benc(xx):
        f = Fat(xx)
        return 1 - (f - np.sin(f) * np.cos(f)) / PI - 0.5
    x_halfB = brentq(Benc, 1e-3, 50)
    # radius enclosing 90 % of the energy  [extra definition]
    order = np.argsort(x)
    cumE = np.cumsum((W * eps)[order]) * 4 * PI / a1
    x_E90 = np.interp(0.9, cumE, x[order])
    # slope at origin and tail coefficient
    slope0 = -(Fat(1e-5) - PI) / 1e-5
    Ctail = h.L ** 2 * (PI + np.sum(h.c)) if h.beta == 0 else None   # F -> C/x^2, T_k(1) = 1
    return dict(a1=a1, E2=E2, E4=E4, E0=E0, virial_E2_over_E4=E2 / E4,
                derrick_E2_minus_E4_plus_3E0=(E2 - E4 + 3 * E0) / a1,
                Lambda=Lam, Bnorm=Bnorm, xB=np.sqrt(xB2), xM=np.sqrt(xM2), xE=np.sqrt(xE2),
                x_half=x_half, x_halfB=x_halfB, xmeanB=xmeanB, x_E90=x_E90,
                slope0=slope0, Ctail=Ctail, gnorm=h.gnorm)


def main():
    out = {"method": "Ritz spectral: F = (1-t)^2[pi + t sum c_k T_k(2t-1)], x = L t/(1-t), "
                     "Newton on exact gradient/Hessian of Gauss-Legendre energy"}
    # --- convergence study, massless --------------------------------------------------
    conv = []
    ref = None
    for (N, L, Nq) in [(20, 2.0, 400), (30, 2.0, 600), (40, 2.0, 800), (50, 2.0, 1000),
                       (60, 2.0, 1200), (60, 1.5, 1200), (60, 3.0, 1200), (80, 2.0, 1600)]:
        h = Hedgehog(N=N, L=L, Nq=Nq)
        c0 = None
        if ref is not None and ref.L == L and ref.N <= N:
            c0 = np.zeros(N); c0[:ref.N] = ref.c
        h.solve(c0=c0)
        ob = observables(h)
        ob.update(N=N, L=L, Nq=Nq)
        conv.append(ob)
        print(f"N={N:3d} L={L:.1f} Nq={Nq:5d}: a1={ob['a1']:.10f} Lam={ob['Lambda']:.8f} "
              f"xB={ob['xB']:.8f} xM={ob['xM']:.8f} xE={ob['xE']:.8f} xh={ob['x_half']:.8f} "
              f"E2/E4={ob['virial_E2_over_E4']:.10f} B={ob['Bnorm']:.10f} |g|={ob['gnorm']:.1e}")
        sys.stdout.flush()
        if L == 2.0:
            ref = h
    best = conv[-1]
    keys = ["a1", "Lambda", "xB", "xM", "xE", "x_half", "xmeanB", "x_E90"]
    spread = {k: float(max(abs(c[k] - best[k]) for c in conv[-4:]) / abs(best[k])) for k in keys}
    print("relative spread over last 4 settings (N=60..80, L=1.5..3):", spread)
    out["convergence"] = conv
    out["rel_spread_last4"] = spread
    out["best"] = best
    print(f"best: a1 = {best['a1']:.10f}  a1/(3 pi^2) = {best['a1']/(3*PI**2):.10f}  "
          f"slope F'(0) = {best['slope0']:.8f}  C_tail = {best['Ctail']:.6f}")

    # --- pion-mass family ---------------------------------------------------------------
    fam = []
    for beta in [0.0, 0.1, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]:
        rows = []
        for L in [2.0 / np.sqrt(1 + beta), 1.4 / np.sqrt(1 + beta)]:
            h = Hedgehog(N=60, L=L, Nq=1500, beta=beta)
            h.solve()
            ob = observables(h)
            rows.append(ob)
        ob = rows[0]
        d = abs(rows[0]["xB"] * rows[0]["a1"] - rows[1]["xB"] * rows[1]["a1"]) / (rows[0]["xB"] * rows[0]["a1"])
        r = dict(beta=beta, a1=ob["a1"], xB=ob["xB"], xE=ob["xE"], x_half=ob["x_half"],
                 c0_B=ob["a1"] * ob["xB"], c0_E=ob["a1"] * ob["xE"], c0_half=ob["a1"] * ob["x_half"],
                 derrick=ob["derrick_E2_minus_E4_plus_3E0"], L_spread_c0B=d)
        fam.append(r)
        print(f"beta={beta:5.2f}: a1={r['a1']:.6f} xB={r['xB']:.6f} c0_B={r['c0_B']:.4f} "
              f"c0_E={r['c0_E']:.4f} c0_half={r['c0_half']:.4f} Derrick={r['derrick']:.1e} Lspread={d:.1e}")
        sys.stdout.flush()
    out["pion_mass_family"] = fam
    h = Hedgehog(N=60, L=2.0, Nq=1200); h.solve()
    np.savez("cc_hedgehog_profile.npz", c=h.c, N=h.N, L=h.L)
    with open("cc_hedgehog.json", "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("wrote cc_hedgehog.json")


if __name__ == "__main__":
    main()
