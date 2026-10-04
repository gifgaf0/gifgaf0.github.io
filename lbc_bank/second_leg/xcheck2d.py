#!/usr/bin/env python3
"""xcheck2d.py -- independent 2D cross-check of the second leg's 2D crystal numbers.

Method (deliberately different from the main 2D instrument):
  * rectangular two-droplet supercell Lx = a, Ly = sqrt(3) a (sites (0,0) and (a/2, sqrt(3)a/2)),
    Cartesian plane-wave basis exp(i G.r), G = (2 pi m / Lx, 2 pi n / Ly), SQUARE index cut |m|,|n| <= M;
  * ground state = Galerkin stationary point in that basis; all products evaluated exactly (no aliasing) on a
    zero-padded Cartesian FFT grid (>= 4M+1 points per axis); solved by L-BFGS on the normalised energy
    followed by a dense-Jacobian Newton iteration on the GP residual with the fixed-N constraint (bordered);
    never imaginary time;
  * lattice constant: scipy Brent minimisation of e(a) = E/area at rho = 1, refined by brentq on the analytic
    Hellmann-Feynman derivative de/da (fixed normalised coefficients => exact);
  * BdG: full non-Hermitian real 2N x 2N eigenproblem [[L+X, X], [-X, -(L+X)]] in the supercell basis,
    normalisation area*sum(|u|^2-|v|^2) = 1 per supercell, symplectic re-orthonormalisation of degenerate
    clusters, zone-folded (odd m+n) modes identified by their support, T/2/1 by mirror parity, displacement
    projection, density weight and gaplessness;
  * superfluid fraction from finite phase twists only (fixed cell), Richardson extrapolation k -> 0.

Stages (each caches json in WORK):  quad | astar CASE M | bdg CASE M | fs CASE M | collect | compare
CASE in {step44, step22, step13.25, g6_35}.
"""
import os
import sys
import json
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"

import numpy as np
import scipy.linalg as sla
from scipy.special import j0, j1, jv
from scipy.fft import fft2, ifft2, next_fast_len
from scipy.optimize import minimize_scalar, brentq, minimize

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = "/tmp/claude-0/-home-user-gifgaf0-github-io/6eab36f5-c943-5609-bc1f-38f855730ac1/scratchpad/work/xc2d"
os.makedirs(WORK, exist_ok=True)
TWOPI = 2.0 * np.pi
S3 = np.sqrt(3.0)


# ----------------------------------------------------------------------------------------------------------
# kernels
# ----------------------------------------------------------------------------------------------------------
class StepKernel:
    def __init__(self, g):
        self.g = float(g)
        self.name = "step"

    def uhat(self, k):
        k = np.asarray(k, dtype=float)
        out = np.empty_like(k)
        sm = k < 1e-6
        ks = k[~sm]
        out[~sm] = TWOPI * self.g * j1(ks) / ks
        k2 = k[sm] ** 2
        out[sm] = np.pi * self.g * (1.0 - k2 / 8.0 + k2 * k2 / 192.0)
        return out

    def kdu(self, k):
        # k dU/dk = -2 pi g J2(k)
        k = np.asarray(k, dtype=float)
        return -TWOPI * self.g * jv(2, k)


def gauss_legendre(n, a, b):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def tanh_sinh(a, b, h=2.0 ** -9, tmax=3.6):
    t = np.arange(-tmax, tmax + 0.5 * h, h)
    s = 0.5 * np.pi * np.sinh(t)
    x01 = 0.5 * (1.0 + np.tanh(s))
    w01 = 0.5 * h * 0.5 * np.pi * np.cosh(t) / np.cosh(s) ** 2
    keep = (x01 > 0) & (x01 < 1) & (w01 > 0)
    return a + (b - a) * x01[keep], (b - a) * w01[keep]


class Gamma6Kernel:
    """U(r) = g exp(-r^6); Uhat(k) = 2 pi g int_0^inf e^{-r^6} J0(k r) r dr (truncated at r = 2.5,
    integrand < 1e-100 there). Primary quadrature: Gauss-Legendre, 2400 nodes on [0, 2.5]."""

    def __init__(self, g, nodes=2400, rmax=2.5):
        self.g = float(g)
        self.name = "g6"
        self.r, self.w = gauss_legendre(nodes, 0.0, rmax)
        self.wf = self.w * np.exp(-self.r ** 6) * self.r

    def _apply(self, k, fun, chunk=4000):
        k = np.asarray(k, dtype=float)
        flat = k.ravel()
        # evaluate on unique values only (many symmetric duplicates)
        uq, inv = np.unique(np.round(flat, 13), return_inverse=True)
        res = np.empty(uq.size)
        for s in range(0, uq.size, chunk):
            kk = uq[s:s + chunk]
            res[s:s + chunk] = fun(np.outer(kk, self.r)) @ self.wf
        return (TWOPI * self.g * res)[inv].reshape(k.shape)

    def uhat(self, k):
        return self._apply(k, j0)

    def kdu(self, k):
        # k dU/dk = -2 pi g int e^{-r^6} (k r) J1(k r) r dr
        return self._apply(k, lambda z: -z * j1(z))


def uhat_g6_alt(k, g, which="ts"):
    """independent quadratures of the gamma6 transform (for validation only)"""
    k = np.atleast_1d(np.asarray(k, dtype=float))
    if which == "ts":
        r, w = tanh_sinh(0.0, 2.6)
    else:  # composite Gauss-Legendre, 260 panels x 20 nodes on [0, 2.6]
        edges = np.linspace(0.0, 2.6, 261)
        xs, ws = [], []
        for lo, hi in zip(edges[:-1], edges[1:]):
            x, ww = gauss_legendre(20, lo, hi)
            xs.append(x)
            ws.append(ww)
        r, w = np.concatenate(xs), np.concatenate(ws)
    wf = w * np.exp(-r ** 6) * r
    out = np.empty(k.size)
    for s in range(0, k.size, 2000):
        out[s:s + 2000] = j0(np.outer(k[s:s + 2000], r)) @ wf
    return TWOPI * g * out


def make_kernel(case):
    if case.startswith("step"):
        return StepKernel(float(case[4:]))
    if case.startswith("g6_"):
        return Gamma6Kernel(float(case[3:]))
    raise ValueError(case)


# ----------------------------------------------------------------------------------------------------------
# Galerkin plane-wave cell
# ----------------------------------------------------------------------------------------------------------
class Cell:
    def __init__(self, a, M, kernel):
        self.a = float(a)
        self.M = int(M)
        self.kernel = kernel
        self.Lx = self.a
        self.Ly = S3 * self.a
        self.area = self.Lx * self.Ly
        self.n1 = 2 * self.M + 1
        self.mi = np.arange(-self.M, self.M + 1)
        self.Ng = next_fast_len(4 * self.M + 2)
        self.gidx = self.mi % self.Ng
        f = np.fft.fftfreq(self.Ng, 1.0 / self.Ng)
        self.fint = np.rint(f).astype(int)
        KX = (TWOPI / self.Lx) * f[:, None]
        KY = (TWOPI / self.Ly) * f[None, :]
        self.kgrid = np.sqrt(KX ** 2 + KY ** 2)
        # the density has band 2M; mask beyond (it is zero there anyway, mask for exactness)
        band = (np.abs(self.fint)[:, None] <= 2 * self.M) & (np.abs(self.fint)[None, :] <= 2 * self.M)
        self.uK = kernel.uhat(self.kgrid) * band
        self.band = band
        m, n = np.meshgrid(self.mi, self.mi, indexing="ij")
        self.m = m
        self.n = n
        self.Gx = (TWOPI / self.Lx) * m
        self.Gy = (TWOPI / self.Ly) * n
        self.parity_even = ((m + n) % 2 == 0)

    # coefficient array (n1, n1) [or batch (..., n1, n1)] <-> padded grid
    def to_grid(self, C):
        shp = C.shape[:-2] + (self.Ng, self.Ng)
        Gd = np.zeros(shp, dtype=complex)
        Gd[..., self.gidx[:, None], self.gidx[None, :]] = C
        return ifft2(Gd, axes=(-2, -1), workers=2) * (self.Ng * self.Ng)

    def from_grid(self, f):
        F = fft2(f, axes=(-2, -1), workers=2) / (self.Ng * self.Ng)
        return F[..., self.gidx[:, None], self.gidx[None, :]]

    def kin(self, kvec=(0.0, 0.0)):
        return 0.5 * ((self.Gx + kvec[0]) ** 2 + (self.Gy + kvec[1]) ** 2)

    def fields(self, C):
        psi = self.to_grid(C)
        rho = (psi.real ** 2 + psi.imag ** 2)
        rhoK = fft2(rho, workers=2) / (self.Ng * self.Ng)
        PhiK = self.uK * rhoK
        Phi = (ifft2(PhiK, workers=2) * (self.Ng * self.Ng)).real
        PhiPsi = self.from_grid(Phi * psi)
        return psi, rhoK, Phi, PhiPsi

    def energy_density(self, C, kvec=(0.0, 0.0)):
        """E/area for coefficient array C (normalisation sum|C|^2 = rho_bar = 1 assumed by caller)"""
        psi, rhoK, Phi, PhiPsi = self.fields(C)
        T = self.kin(kvec)
        ekin = float(np.sum(T * np.abs(C) ** 2))
        eint = 0.5 * float(np.sum(self.uK * (rhoK.real ** 2 + rhoK.imag ** 2)))
        return ekin + eint, ekin, eint

    def dedA(self, C):
        """Hellmann-Feynman derivative de/da at fixed normalised coefficients (exact at a stationary point)"""
        psi, rhoK, Phi, PhiPsi = self.fields(C)
        T = self.kin()
        ekin = float(np.sum(T * np.abs(C) ** 2))
        kd = self.kernel.kdu(self.kgrid) * self.band
        s = 0.5 * float(np.sum(kd * (rhoK.real ** 2 + rhoK.imag ** 2)))
        return -(2.0 * ekin + s) / self.a

    def residual(self, C, kvec=(0.0, 0.0)):
        psi, rhoK, Phi, PhiPsi = self.fields(C)
        T = self.kin(kvec)
        HC = T * C + PhiPsi.real
        mu = float(np.sum(C * HC) / np.sum(C * C))
        return HC - mu * C, mu, psi, Phi

    def jac_apply(self, V, psi, Phi, mu, kvec=(0.0, 0.0)):
        """d(residual)/dC applied to a batch of real coefficient arrays V (nb, n1, n1), mu held fixed"""
        T = self.kin(kvec)
        dpsi = self.to_grid(V)
        drho = 2.0 * (np.conj(psi) * dpsi).real
        dPhi = (ifft2(self.uK * fft2(drho, axes=(-2, -1), workers=2), axes=(-2, -1), workers=2)).real
        out = self.from_grid(Phi * dpsi + dPhi * psi).real
        return T * V + out - mu * V


# symmetry orbits on the (m, n) index square ----------------------------------------------------------------
def orbit_struct(M, sym):
    """sym: 'gs' = mirrors x and y (+ two-droplet translation: m+n even);
    'twx' = mirror y only; 'twy' = mirror x only (both with m+n even). Returns (rep_i, rep_j, member lists)."""
    reps = []
    members = []
    for m in range(-M, M + 1):
        for n in range(-M, M + 1):
            if (m + n) % 2:
                continue
            if sym == "gs":
                if m < 0 or n < 0:
                    continue
                orb = {(m, n), (-m, n), (m, -n), (-m, -n)}
            elif sym == "twx":
                if n < 0:
                    continue
                orb = {(m, n), (m, -n)}
            elif sym == "twy":
                if m < 0:
                    continue
                orb = {(m, n), (-m, n)}
            else:
                raise ValueError(sym)
            reps.append((m + M, n + M))
            members.append([(a + M, b + M) for (a, b) in sorted(orb)])
    ri = np.array([r[0] for r in reps])
    rj = np.array([r[1] for r in reps])
    w = np.array([len(o) for o in members], dtype=float)
    return ri, rj, members, w


class Reducer:
    def __init__(self, M, sym):
        self.M = M
        self.n1 = 2 * M + 1
        self.ri, self.rj, self.members, self.w = orbit_struct(M, sym)
        self.nred = self.ri.size
        # expansion index: for every full index, which orbit (or -1)
        self.owner = -np.ones((self.n1, self.n1), dtype=int)
        for k, orb in enumerate(self.members):
            for (a, b) in orb:
                self.owner[a, b] = k

    def expand(self, x):
        C = np.zeros((self.n1, self.n1))
        msk = self.owner >= 0
        C[msk] = x[self.owner[msk]]
        return C

    def reduce(self, C):
        # orbit average (projects onto the symmetric subspace)
        x = np.zeros(self.nred)
        msk = self.owner >= 0
        np.add.at(x, self.owner[msk], C[msk])
        return x / self.w

    def basis_batch(self, idx):
        B = np.zeros((len(idx), self.n1, self.n1))
        for t, k in enumerate(idx):
            for (a, b) in self.members[k]:
                B[t, a, b] = 1.0
        return B


def solve_state(cell, C0, kvec=(0.0, 0.0), sym="gs", tol=1e-13, maxit=40, lbfgs=False, verbose=False):
    """Galerkin stationary state with sum C^2 = 1 (rho_bar = 1). Newton on the bordered GP system with a dense
    reduced Jacobian (exact analytic Jacobian-vector products). Optional L-BFGS pre-phase on the normalised
    energy."""
    red = Reducer(cell.M, sym)
    x = red.reduce(C0)
    x /= np.sqrt(np.sum(red.w * x * x))
    if lbfgs:
        def fun(y):
            nrm = np.sqrt(np.sum(red.w * y * y))
            C = red.expand(y / nrm)
            psi, rhoK, Phi, PhiPsi = cell.fields(C)
            T = cell.kin(kvec)
            e = float(np.sum(T * C * C)) + 0.5 * float(np.sum(cell.uK * np.abs(rhoK) ** 2))
            gC = 2.0 * (T * C + PhiPsi.real)  # de/dC (full)
            gx_rep = gC[red.ri, red.rj]  # symmetric, value at rep
            Cx = y / nrm
            lam = float(np.sum(red.w * gx_rep * Cx))
            grad = red.w * (gx_rep - lam * Cx) / nrm
            return e, grad
        res = minimize(fun, x, jac=True, method="L-BFGS-B",
                       options=dict(maxiter=4000, maxcor=30, gtol=1e-10, ftol=1e-15))
        x = res.x / np.sqrt(np.sum(red.w * res.x ** 2))
        if verbose:
            print("  lbfgs:", res.nit, res.fun, res.message, flush=True)
    hist = []
    for it in range(maxit):
        C = red.expand(x)
        R, mu, psi, Phi = cell.residual(C, kvec)
        rn = float(np.max(np.abs(R)))
        cn = float(np.sum(red.w * x * x)) - 1.0
        hist.append(rn)
        if verbose:
            print(f"  newton it {it} |R|={rn:.3e} norm-1={cn:.2e} mu={mu!r}", flush=True)
        if rn < tol and abs(cn) < 1e-14:
            break
        # dense reduced Jacobian
        J = np.empty((red.nred, red.nred))
        bs = 96
        for s in range(0, red.nred, bs):
            idx = list(range(s, min(s + bs, red.nred)))
            B = red.basis_batch(idx)
            JB = cell.jac_apply(B, psi, Phi, mu, kvec)
            J[:, s:s + len(idx)] = JB[:, red.ri, red.rj].T
        nb = red.nred
        Kb = np.zeros((nb + 1, nb + 1))
        Kb[:nb, :nb] = J
        Kb[:nb, nb] = -x
        Kb[nb, :nb] = red.w * x
        rhs = np.concatenate([-R[red.ri, red.rj], [-0.5 * cn]])
        d = sla.solve(Kb, rhs)
        dx = d[:nb]
        # damping: accept the step if the residual decreases, else halve (a few times)
        lam = 1.0
        for _ in range(8):
            xt = x + lam * dx
            Rt, _, _, _ = cell.residual(red.expand(xt), kvec)
            if np.max(np.abs(Rt)) < max(rn, 1e-14) * 1.5 or lam < 0.02:
                break
            lam *= 0.5
        x = xt
    else:
        if verbose:
            print("  newton: maxit reached", flush=True)
    C = red.expand(x)
    C /= np.sqrt(np.sum(C * C))
    R, mu, psi, Phi = cell.residual(C, kvec)
    e, ek, ei = cell.energy_density(C, kvec)
    return dict(C=C, mu=mu, e=e, ekin=ek, eint=ei, res=float(np.max(np.abs(R))), hist=hist)


def gaussian_guess(cell, sigma):
    # two Gaussian droplets at (0,0), (a/2, sqrt3 a/2): coefficients of the periodic sum
    G2 = cell.Gx ** 2 + cell.Gy ** 2
    C = np.exp(-0.5 * G2 * sigma ** 2) * (1.0 + (-1.0) ** (cell.m + cell.n))
    return C / np.sqrt(np.sum(C * C))


def regrid(C, M_new):
    """copy coefficients to a different index cut (truncate or zero-pad)"""
    M_old = (C.shape[0] - 1) // 2
    out = np.zeros((2 * M_new + 1, 2 * M_new + 1))
    mm = min(M_old, M_new)
    out[M_new - mm:M_new + mm + 1, M_new - mm:M_new + mm + 1] = C[M_old - mm:M_old + mm + 1,
                                                                  M_old - mm:M_old + mm + 1]
    return out / np.sqrt(np.sum(out ** 2))


# ----------------------------------------------------------------------------------------------------------
# cases
# ----------------------------------------------------------------------------------------------------------
CASES = ["step44", "step22", "step13.25", "g6_35"]
SEED_CHAIN = {"step44": None, "step22": "step44", "step13.25": "step22", "g6_35": None}
KAPPAS = [0.03, 0.05, 0.075, 0.10]


def fpath(stage, case, M):
    return os.path.join(WORK, f"{stage}_{case}_M{M}.json")


def save_json(path, obj):
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1)


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def save_state(case, M, a, C):
    np.savez(os.path.join(WORK, f"state_{case}_M{M}.npz"), a=a, C=C)


def load_state(case, M):
    p = os.path.join(WORK, f"state_{case}_M{M}.npz")
    if not os.path.exists(p):
        return None
    d = np.load(p)
    return float(d["a"]), d["C"]


# ----------------------------------------------------------------------------------------------------------
# stage: a*
# ----------------------------------------------------------------------------------------------------------
BRACKETS = {"step44": (1.30, 1.50), "step22": (1.40, 1.60), "step13.25": (1.45, 1.60), "g6_35": (1.35, 1.55)}


def contrast_of(cell, C):
    psi = cell.to_grid(C).real
    return float((psi.max() ** 2 - psi.min() ** 2) / (psi.max() ** 2 + psi.min() ** 2))


def stage_astar(case, M, a_lo=None, a_hi=None):
    t0 = time.time()
    ker = make_kernel(case)
    if a_lo is None:
        a_lo, a_hi = BRACKETS[case]
    cache = {}
    state = {"C": None}

    def evals(a):
        key = repr(float(a))
        if key in cache:
            return cache[key]
        cell = Cell(a, M, ker)
        r = None
        if state["C"] is not None:
            r = solve_state(cell, state["C"])
            if r["res"] > 1e-11 or contrast_of(cell, r["C"]) < 0.3:
                r = None
        if r is None:
            # fresh two-Gaussian seed + L-BFGS pre-phase (guards against collapse to the uniform state)
            r = solve_state(cell, gaussian_guess(cell, 0.2), lbfgs=True)
        state["C"] = r["C"]
        d = cell.dedA(r["C"])
        out = dict(a=float(a), e=r["e"], mu=r["mu"], res=r["res"], dedA=d, C=r["C"],
                   contrast=contrast_of(cell, r["C"]))
        cache[key] = out
        print(f"   a={a!r} e={r['e']!r} de/da={d!r} res={r['res']:.2e} mu={r['mu']!r} "
              f"contrast={out['contrast']:.4f}", flush=True)
        return out

    # coarse scan for the bracket
    grid = np.linspace(a_lo, a_hi, 9)
    vals = [evals(a)["e"] for a in grid]
    k = int(np.argmin(vals))
    if k == 0 or k == len(grid) - 1:
        raise RuntimeError("minimum not bracketed")
    br = (grid[k - 1], grid[k], grid[k + 1])
    fe = lambda a: evals(a)["e"]
    resB = minimize_scalar(fe, bracket=br, method="brent", tol=1e-12, options=dict(maxiter=200))
    a_brent = float(resB.x)
    # refine: root of the analytic derivative
    fd = lambda a: evals(a)["dedA"]
    lo, hi = a_brent - 2e-4, a_brent + 2e-4
    while fd(lo) > 0:
        lo -= 2e-4
    while fd(hi) < 0:
        hi += 2e-4
    a_root = brentq(fd, lo, hi, xtol=1e-15, rtol=4 * np.finfo(float).eps, maxiter=200)
    best = evals(a_root)
    # finite-difference check of de/da at a_root
    h = 1e-4
    fd_check = (evals(a_root + h)["e"] - evals(a_root - h)["e"]) / (2 * h)
    # curvature (for error estimate)
    e2 = (evals(a_root + 1e-3)["e"] - 2 * best["e"] + evals(a_root - 1e-3)["e"]) / 1e-6
    best = evals(a_root)
    save_state(case, M, a_root, best["C"])
    cell = Cell(a_root, M, ker)
    C = best["C"]
    # decay of coefficients at the cut (resolution diagnostic)
    edge = max(float(np.max(np.abs(C[[0, -1], :]))), float(np.max(np.abs(C[:, [0, -1]]))))
    edge_y = float(np.max(np.abs(C[:, [0, -1]])))
    edge_x = float(np.max(np.abs(C[[0, -1], :])))
    psi = cell.to_grid(C).real
    out = dict(case=case, M=M, Ng=cell.Ng, a_brent=a_brent, a_star=float(a_root),
               e_star=best["e"], mu_star=best["mu"], gp_residual=best["res"],
               dedA_at_astar=best["dedA"], dedA_fd_check=float(fd_check),
               d2e_da2=float(e2), brent_nfev=int(resB.nfev), a_brent_minus_root=float(a_brent - a_root),
               coef_edge_max=edge, coef_edge_x=edge_x, coef_edge_y=edge_y,
               psi_max=float(psi.max()), psi_min=float(psi.min()),
               contrast=float((psi.max() ** 2 - psi.min() ** 2) / (psi.max() ** 2 + psi.min() ** 2)),
               eps_c=best["e"], time_s=time.time() - t0)
    save_json(fpath("astar", case, M), out)
    print(json.dumps(out, indent=1), flush=True)
    return out


# ----------------------------------------------------------------------------------------------------------
# BdG
# ----------------------------------------------------------------------------------------------------------
def bdg_matrices(cell, C, mu, q):
    M = cell.M
    n1 = cell.n1
    mm = cell.m.ravel()
    nn = cell.n.ravel()
    qx, qy = q
    Gx = (TWOPI / cell.Lx) * mm + qx
    Gy = (TWOPI / cell.Ly) * nn + qy
    T = 0.5 * (Gx ** 2 + Gy ** 2)
    psi, rhoK, Phi, PhiPsi = cell.fields(C)
    PhiK = (cell.uK * rhoK)
    # Phi_{G_i - G_j}: difference indices in [-2M, 2M] -> grid index mod Ng
    dm = (mm[:, None] - mm[None, :]) % cell.Ng
    dn = (nn[:, None] - nn[None, :]) % cell.Ng
    Lmat = PhiK[dm, dn].real.copy()
    Lmat[np.diag_indices_from(Lmat)] += T - mu
    # X = P diag(U(|q+K|)) P^T, K over [-2M, 2M]^2, P[i,K] = C_{G_i - K}
    kr = np.arange(-2 * M, 2 * M + 1)
    km, kn = np.meshgrid(kr, kr, indexing="ij")
    km = km.ravel()
    kn = kn.ravel()
    Kx = (TWOPI / cell.Lx) * km + qx
    Ky = (TWOPI / cell.Ly) * kn + qy
    Uq = cell.kernel.uhat(np.sqrt(Kx ** 2 + Ky ** 2))
    Cp = np.zeros((6 * M + 1, 6 * M + 1))
    Cp[2 * M:4 * M + 1, 2 * M:4 * M + 1] = C
    P = Cp[(mm[:, None] - km[None, :]) + 3 * M, (nn[:, None] - kn[None, :]) + 3 * M]
    X = (P * Uq[None, :]) @ P.T
    X = 0.5 * (X + X.T)
    Lmat = 0.5 * (Lmat + Lmat.T)
    return Lmat, X, T


def bdg_solve(cell, C, mu, q, clus_tol=1e-9):
    """full non-Hermitian eigenproblem; returns positive-norm modes with normalisation and observables"""
    Lm, X, T = bdg_matrices(cell, C, mu, q)
    nb = Lm.shape[0]
    H = np.block([[Lm + X, X], [-X, -(Lm + X)]])
    t0 = time.time()
    lam, W = sla.eig(H, overwrite_a=True, check_finite=False)
    t_eig = time.time() - t0
    del H
    area = cell.area
    U = W[:nb, :]
    V = W[nb:, :]
    nrm = area * (np.sum(np.abs(U) ** 2, axis=0) - np.sum(np.abs(V) ** 2, axis=0))
    max_imag = float(np.max(np.abs(lam.imag)))
    pos = np.where(nrm > 0)[0]
    order = pos[np.argsort(lam[pos].real)]
    lam_p = lam[order]
    Wp = W[:, order]
    nrm_p = nrm[order]
    # symplectic (eta) orthonormalisation inside degenerate clusters
    eta = np.concatenate([np.ones(nb), -np.ones(nb)])
    wr = lam_p.real
    k = 0
    nclus = 0
    while k < wr.size:
        j = k + 1
        while j < wr.size and abs(wr[j] - wr[k]) < clus_tol * max(1.0, abs(wr[k])):
            j += 1
        if j - k == 1:
            Wp[:, k] /= np.sqrt(nrm_p[k])
        else:
            nclus += 1
            Wc = Wp[:, k:j]
            Gm = area * (Wc.conj().T @ (eta[:, None] * Wc))
            Gm = 0.5 * (Gm + Gm.conj().T)
            ev, evec = np.linalg.eigh(Gm)
            if np.min(ev) <= 0:
                raise RuntimeError("non-positive cluster Gram matrix")
            Wp[:, k:j] = Wc @ (evec / np.sqrt(ev)[None, :])
        k = j
    Up = Wp[:nb, :]
    Vp = Wp[nb:, :]
    c = C.ravel()
    fplus = Up + Vp
    rho_nu = area * (c @ fplus)
    Z = np.abs(rho_nu) ** 2
    om = lam_p.real
    # block support (even m+n = genuine Bloch q of the triangular lattice; odd = zone-folded q + M)
    ev_mask = cell.parity_even.ravel()
    wt = np.abs(Up) ** 2 + np.abs(Vp) ** 2
    frac_even = np.sum(wt[ev_mask, :], axis=0) / np.sum(wt, axis=0)
    # mirror y -> -y partner index: (m, n) -> (m, -n)
    n1 = cell.n1
    idx = np.arange(nb).reshape(n1, n1)
    mir_y = idx[:, ::-1].ravel()
    par_y = np.real(np.sum(np.conj(Up) * Up[mir_y, :] + np.conj(Vp) * Vp[mir_y, :], axis=0)) / np.sum(wt, axis=0)
    # displacement projections <exp(iqr) d_j psi0 | f+> (normalised)
    dxp = 1j * cell.Gx.ravel() * c
    dyp = 1j * cell.Gy.ravel() * c
    Px = np.abs(np.conj(dxp) @ fplus) / (np.linalg.norm(dxp) * np.linalg.norm(fplus, axis=0))
    Py = np.abs(np.conj(dyp) @ fplus) / (np.linalg.norm(dyp) * np.linalg.norm(fplus, axis=0))
    # sum rules
    qq = q[0] ** 2 + q[1] ** 2
    Ncell = area  # rho_bar = 1, per supercell
    fsum_spec = float(np.sum(om * Z))
    fsum_exact = 0.5 * Ncell * qq
    s = c.astype(complex)
    fsum_quad = float(area * np.real(s @ (Lm @ s)))
    chi_spec = float(np.sum(2.0 * Z / om))
    A = Lm + 2.0 * X
    xs = sla.solve(A, c, assume_a="pos")
    chi_dir = float(2.0 * area * (c @ xs))
    return dict(om=om, Z=Z, lam_imag=lam_p.imag, frac_even=frac_even, par_y=par_y, Px=Px, Py=Py,
                fsum_spec=fsum_spec, fsum_exact=fsum_exact, fsum_quad=fsum_quad,
                chi_spec=chi_spec, chi_dir=chi_dir, max_imag=max_imag, n_pos=int(om.size),
                nb=int(nb), t_eig=t_eig, nclus=nclus)


def gamma_checks(cell, C, mu):
    Lm, X, T = bdg_matrices(cell, C, mu, (0.0, 0.0))
    c = C.ravel()
    A = Lm + 2 * X
    dx = (1j * cell.Gx.ravel() * c)
    dy = (1j * cell.Gy.ravel() * c)
    r_phase = float(np.linalg.norm(Lm @ c) / (np.linalg.norm(Lm, 2) * np.linalg.norm(c)))
    r_dx = float(np.linalg.norm(A @ dx) / (np.linalg.norm(A, 2) * np.linalg.norm(dx)))
    r_dy = float(np.linalg.norm(A @ dy) / (np.linalg.norm(A, 2) * np.linalg.norm(dy)))
    evL = sla.eigvalsh(Lm, subset_by_index=[0, 2])
    evA = sla.eigvalsh(A, subset_by_index=[0, 3])
    return dict(L_psi0_rel=r_phase, A_dxpsi0_rel=r_dx, A_dypsi0_rel=r_dy,
                L_lowest3=[float(v) for v in evL], A_lowest4=[float(v) for v in evA])


def stage_bdg(case, M):
    t0 = time.time()
    ast = load_json(fpath("astar", case, M))
    a, C = load_state(case, M)
    ker = make_kernel(case)
    cell = Cell(a, M, ker)
    r = solve_state(cell, C)
    C = r["C"]
    mu = r["mu"]
    out = dict(case=case, M=M, a_star=a, nb=cell.n1 ** 2, mu=mu, gp_res=r["res"])
    out["gamma"] = gamma_checks(cell, C, mu)
    path = fpath("bdg", case, M)
    if os.path.exists(path):
        old = load_json(path)
        out["q"] = old.get("q", {})
    else:
        out["q"] = {}
    dirs = [("x", k) for k in KAPPAS] + [("d30", 0.05)]
    for (dname, kap) in dirs:
        key = f"{dname}_{kap!r}"
        if key in out["q"]:
            continue
        qa = kap * TWOPI / a
        ang = 0.0 if dname == "x" else np.pi / 6
        q = (qa * np.cos(ang), qa * np.sin(ang))
        res = bdg_solve(cell, C, mu, q)
        om, Z = res["om"], res["Z"]
        sel = np.where(res["frac_even"] > 0.5)[0]
        folded = np.where(res["frac_even"] <= 0.5)[0]
        low = sel[:6]
        rec = dict(kappa=kap, dir=dname, q=[float(q[0]), float(q[1])], qabs=float(qa),
                   t_eig=res["t_eig"], max_imag=res["max_imag"], n_pos=res["n_pos"], nclus=res["nclus"],
                   fsum_spec=res["fsum_spec"], fsum_exact=res["fsum_exact"], fsum_quad=res["fsum_quad"],
                   fsum_rel_resid=(res["fsum_spec"] - res["fsum_exact"]) / res["fsum_exact"],
                   chi_spec=res["chi_spec"], chi_dir=res["chi_dir"],
                   chi_rel_resid=(res["chi_spec"] - res["chi_dir"]) / res["chi_dir"],
                   low_even=[dict(om=float(om[i]), Z=float(Z[i]), frac_even=float(res["frac_even"][i]),
                                  par_y=float(res["par_y"][i]), Px=float(res["Px"][i]), Py=float(res["Py"][i]),
                                  F=float(om[i] * Z[i] / res["fsum_exact"]),
                                  S=float(2 * Z[i] / om[i] / res["chi_spec"]),
                                  lam_imag=float(res["lam_imag"][i])) for i in low],
                   low_folded=[dict(om=float(om[i]), Z=float(Z[i]), frac_even=float(res["frac_even"][i]))
                               for i in folded[:4]],
                   lowest_any=[float(v) for v in om[:8]])
        out["q"][key] = rec
        out["time_s"] = time.time() - t0
        save_json(path, out)
        print(f" {case} M={M} {key}: om={[round(x['om'], 6) for x in rec['low_even'][:4]]} "
              f"Z={[x['Z'] for x in rec['low_even'][:3]]} fsum={rec['fsum_rel_resid']:.2e} "
              f"chi={rec['chi_rel_resid']:.2e} t_eig={res['t_eig']:.1f}s", flush=True)
    out["time_s"] = time.time() - t0
    save_json(path, out)
    return out


# ----------------------------------------------------------------------------------------------------------
# superfluid fraction from phase twists
# ----------------------------------------------------------------------------------------------------------
def stage_fs(case, M, ks=(0.01, 0.02, 0.03, 0.04)):
    t0 = time.time()
    a, C0 = load_state(case, M)
    ker = make_kernel(case)
    cell = Cell(a, M, ker)
    r0 = solve_state(cell, C0)
    e0 = r0["e"]
    out = dict(case=case, M=M, a_star=a, e0=e0, ks=list(ks), dirs={})
    for dname, sym in (("x", "twx"), ("y", "twy")):
        fk = []
        es = []
        Cw = r0["C"]
        for k in ks:
            kvec = (k, 0.0) if dname == "x" else (0.0, k)
            r = solve_state(cell, Cw, kvec=kvec, sym=sym)
            Cw = r["C"]
            es.append(r["e"])
            fk.append(2.0 * (r["e"] - e0) / k ** 2)
            print(f"  {case} M={M} twist {dname} k={k}: e-e0={r['e'] - e0!r} f(k)={fk[-1]!r} res={r['res']:.1e}",
                  flush=True)
        ks_a = np.array(ks)
        fk_a = np.array(fk)
        # Richardson / polynomial extrapolation in k^2
        ex = {}
        for npts in (2, 3, 4):
            V = np.vander(ks_a[:npts] ** 2, npts, increasing=True)
            coef = np.linalg.solve(V, fk_a[:npts])
            ex[f"poly_{npts}pts"] = float(coef[0])
        out["dirs"][dname] = dict(e=es, f_of_k=fk, extrap=ex, f_s=ex["poly_3pts"])
    out["f_s"] = 0.5 * (out["dirs"]["x"]["f_s"] + out["dirs"]["y"]["f_s"])
    out["f_s_x"] = out["dirs"]["x"]["f_s"]
    out["f_s_y"] = out["dirs"]["y"]["f_s"]
    out["extrap_spread"] = float(abs(out["dirs"]["x"]["extrap"]["poly_3pts"] - out["dirs"]["x"]["extrap"]["poly_4pts"]))
    out["time_s"] = time.time() - t0
    save_json(fpath("fs", case, M), out)
    print(json.dumps({k: v for k, v in out.items() if k != "dirs"}, indent=1), flush=True)
    return out


# ----------------------------------------------------------------------------------------------------------
# collect: mode labelling, speeds, weights -> results json
# ----------------------------------------------------------------------------------------------------------
M_LO, M_HI = 14, 22


def label_x(rec):
    """q along a1 (mirror y -> -y): among the three lowest even-block (non-folded) positive modes,
    T = mirror-odd, 2 / 1 = lower / upper mirror-even."""
    low = rec["low_even"]
    ac = low[:3]
    odd = [m for m in ac if m["par_y"] < 0]
    evn = sorted([m for m in ac if m["par_y"] > 0], key=lambda m: m["om"])
    if len(odd) != 1 or len(evn) != 2:
        raise RuntimeError("labelling failed: parities " + str([m["par_y"] for m in ac]))
    return dict(T=odd[0], two=evn[0], one=evn[1], fourth=low[3])


def label_30(rec):
    low = rec["low_even"]
    ac = low[:3]
    zs = [m["Z"] for m in ac]
    iT = int(np.argmin(zs))
    rest = sorted([ac[i] for i in range(3) if i != iT], key=lambda m: m["om"])
    # displacement projection perpendicular to q (30 deg): d_perp = -sin30 d_x + cos30 d_y -> use |Py|,|Px|
    return dict(T=ac[iT], two=rest[0], one=rest[1], fourth=low[3], Zratio_T_over_max=float(zs[iT] / max(zs)))


def lsq_speed(qs, oms):
    qs = np.asarray(qs)
    oms = np.asarray(oms)
    return float(np.sum(oms * qs) / np.sum(qs * qs))


def summarize(case, M):
    ast = load_json(fpath("astar", case, M))
    bd = load_json(fpath("bdg", case, M))
    a = bd["a_star"]
    out = dict(M=M, basis_size=bd["nb"], bdg_matrix_dim=2 * bd["nb"], fft_grid=ast["Ng"],
               a_star=ast["a_star"], a_brent=ast["a_brent"], e_star=ast["e_star"], mu_star=ast["mu_star"],
               gp_residual=ast["gp_residual"], dedA_at_astar=ast["dedA_at_astar"], d2e_da2=ast["d2e_da2"],
               coef_edge_max=ast["coef_edge_max"], density_contrast=ast["contrast"], gamma_checks=bd["gamma"])
    qs, w2, wT, w1, rows = [], [], [], [], []
    fres, cres = [], []
    for kap in KAPPAS:
        rec = bd["q"][f"x_{kap!r}"]
        lab = label_x(rec)
        qs.append(rec["qabs"])
        w2.append(lab["two"]["om"])
        wT.append(lab["T"]["om"])
        w1.append(lab["one"]["om"])
        fres.append(rec["fsum_rel_resid"])
        cres.append(rec["chi_rel_resid"])
        rows.append(dict(kappa=kap, q=rec["qabs"], om_T=lab["T"]["om"], om_2=lab["two"]["om"], om_1=lab["one"]["om"],
                         om_4th_even=lab["fourth"]["om"], om_lowest_folded=rec["low_folded"][0]["om"],
                         Z_T=lab["T"]["Z"], Z_2=lab["two"]["Z"], Z_1=lab["one"]["Z"],
                         F_2=lab["two"]["F"], F_1=lab["one"]["F"], S_2=lab["two"]["S"], S_1=lab["one"]["S"],
                         Z21=lab["two"]["Z"] / lab["one"]["Z"],
                         par_T=lab["T"]["par_y"], par_2=lab["two"]["par_y"], par_1=lab["one"]["par_y"],
                         Px_T=lab["T"]["Px"], Py_T=lab["T"]["Py"], Px_2=lab["two"]["Px"], Py_2=lab["two"]["Py"],
                         Px_1=lab["one"]["Px"], Py_1=lab["one"]["Py"],
                         fsum_rel_resid=rec["fsum_rel_resid"], chi_rel_resid=rec["chi_rel_resid"],
                         fsum_quad_vs_exact=(rec["fsum_quad"] - rec["fsum_exact"]) / rec["fsum_exact"],
                         max_imag=rec["max_imag"], n_pos=rec["n_pos"], nclus=rec["nclus"],
                         sum_F_three=lab["T"]["F"] + lab["two"]["F"] + lab["one"]["F"],
                         sum_S_three=lab["T"]["S"] + lab["two"]["S"] + lab["one"]["S"]))
    out["table_x"] = rows
    out["c2"] = lsq_speed(qs, w2)
    out["cT"] = lsq_speed(qs, wT)
    out["c1"] = lsq_speed(qs, w1)
    out["c2_gt_cT"] = bool(out["c2"] > out["cT"])
    r05 = rows[1]
    out["F2"] = r05["F_2"]
    out["Z21"] = r05["Z21"]
    out["S2"] = r05["S_2"]
    out["F1"] = r05["F_1"]
    out["S1"] = r05["S_1"]
    out["fsum_resid_max_abs"] = float(max(abs(v) for v in fres))
    out["chi_resid_max_abs"] = float(max(abs(v) for v in cres))
    # gaplessness: omega/q spread over the four q
    for lab_, ws in (("T", wT), ("2", w2), ("1", w1)):
        r = np.array(ws) / np.array(qs)
        out[f"om_over_q_spread_{lab_}"] = float((r.max() - r.min()) / r.mean())
    out["gap_4th_even_at_0.03_over_om1"] = float(rows[0]["om_4th_even"] / rows[0]["om_1"])
    rec30 = bd["q"]["d30_0.05"]
    lab = label_30(rec30)
    out["cT30"] = lab["T"]["om"] / rec30["qabs"]
    out["d30"] = dict(om_T=lab["T"]["om"], om_2=lab["two"]["om"], om_1=lab["one"]["om"], Z_T=lab["T"]["Z"],
                      Z_2=lab["two"]["Z"], Z_1=lab["one"]["Z"], ZT_over_Zmax=lab["Zratio_T_over_max"],
                      c2_30=lab["two"]["om"] / rec30["qabs"], c1_30=lab["one"]["om"] / rec30["qabs"],
                      F2_30=lab["two"]["F"], S2_30=lab["two"]["S"],
                      fsum_rel_resid=rec30["fsum_rel_resid"], chi_rel_resid=rec30["chi_rel_resid"])
    out["fsum_resid_max_abs_incl_30"] = float(max(out["fsum_resid_max_abs"], abs(rec30["fsum_rel_resid"])))
    pfs = fpath("fs", case, M)
    if os.path.exists(pfs):
        fs = load_json(pfs)
        out["f_s"] = fs["f_s"]
        out["f_s_x"] = fs["f_s_x"]
        out["f_s_y"] = fs["f_s_y"]
        out["f_s_detail"] = fs["dirs"]
        out["f_s_twists"] = fs["ks"]
    plr = fpath("fslr", case, M)
    if os.path.exists(plr):
        lr = load_json(plr)
        out["f_s_linear_response_diagnostic"] = dict(x=lr["f_s_lr_x"], y=lr["f_s_lr_y"])
        if "f_s" in out:
            out["f_s_twist_vs_lr_rel"] = (out["f_s"] - lr["f_s_lr_x"]) / lr["f_s_lr_x"]
    return out


QUANTS = ["a_star", "c2", "cT", "c1", "F2", "Z21", "S2", "cT30", "f_s"]


def stage_collect():
    res = dict(schema="xcheck2d_v1", units="hbar = m = R = 1, rho_bar = 1",
               method=__doc__.strip(), resolutions=dict(lo=M_LO, hi=M_HI), kappas=KAPPAS,
               conventions=dict(
                   speeds="LSQ through origin over |q|a/2pi in kappas, q along a1 = x",
                   weights="at |q|a/2pi = 0.05 along a1; F = om Z/(N q^2/2), S = (2Z/om)/sum_all(2Z/om); Z per "
                           "supercell (= 2 x per primitive cell; F, S, Z ratios are intensive)",
                   cT30="omega_T/|q| at |q|a/2pi = 0.05, q at 30 deg to a1",
                   f_s="finite phase twists k in {0.01,0.02,0.03,0.04} along x and y at fixed cell; "
                       "f(k) = 2(e(k)-e(0))/k^2 extrapolated by a quadratic polynomial in k^2 through the first "
                       "three twists; reported value = mean of x and y",
                   fsum_resid="(sum_nu om Z - N q^2/2)/(N q^2/2) over the full spectrum, max abs over the 5 q"),
               cases={})
    qp = os.path.join(WORK, "quad_g6.json")
    if os.path.exists(qp):
        res["quadrature_g6"] = load_json(qp)
    for case in CASES:
        ent = {}
        for M in (M_LO, M_HI):
            try:
                ent[f"M{M}"] = summarize(case, M)
            except FileNotFoundError as exc:
                ent[f"M{M}"] = dict(missing=str(exc))
        lo, hi = ent[f"M{M_LO}"], ent[f"M{M_HI}"]
        conv = {}
        prim = {}
        for qn in QUANTS + ["e_star", "mu_star", "fsum_resid_max_abs", "chi_resid_max_abs"]:
            if qn in hi:
                prim[qn] = hi[qn]
            if qn in lo and qn in hi and isinstance(hi[qn], float):
                conv[qn] = dict(lo=lo[qn], hi=hi[qn], rel_diff=(lo[qn] - hi[qn]) / hi[qn] if hi[qn] else None)
        ent["primary"] = prim
        ent["convergence_lo_vs_hi"] = conv
        res["cases"][case] = ent
    save_json(os.path.join(HERE, "xcheck2d_results.json"), res)
    print(json.dumps({c: res["cases"][c]["primary"] for c in res["cases"]}, indent=1))
    return res


def stage_fslr(case, M):
    """diagnostic only (the reported f_s is the finite-twist value): linear-response
    f_s = 1 - (2/N) <d_j psi0 | L^-1 | d_j psi0> with the same Galerkin L at q = 0 (dense)."""
    a, C = load_state(case, M)
    cell = Cell(a, M, make_kernel(case))
    r = solve_state(cell, C)
    C = r["C"]
    Lm, X, T = bdg_matrices(cell, C, r["mu"], (0.0, 0.0))
    c = C.ravel()
    out = dict(case=case, M=M)
    for dname, G in (("x", cell.Gx), ("y", cell.Gy)):
        d = 1j * G.ravel() * c  # coefficients of d_j psi0 (orthogonal to psi0)
        # L is singular only along psi0; regularise with the projector onto psi0 (d is orthogonal to it)
        Lr = Lm + np.outer(c, c) * np.linalg.norm(Lm, 2)
        y = sla.solve(Lr, d)
        val = float(np.real(np.vdot(d, y)) * cell.area)
        out[f"f_s_lr_{dname}"] = 1.0 - 2.0 * val / cell.area
    save_json(fpath("fslr", case, M), out)
    print(json.dumps(out, indent=1))
    return out


# ----------------------------------------------------------------------------------------------------------
# compare (run only AFTER the own numbers were saved): overlap with the main instrument's qa_results.json
# ----------------------------------------------------------------------------------------------------------
QA_KEY = {"step44": "44", "step22": "22", "step13.25": "13.25", "g6_35": "35g6"}
# thresholds requested for this cross-check: speeds and a* 0.1 % rel; F2, Z21, f_s 1 % rel; S2 0.005 abs
THRESH = {"a_star": ("rel", 1e-3), "c2": ("rel", 1e-3), "cT": ("rel", 1e-3), "c1": ("rel", 1e-3),
          "cT30": ("rel", 1e-3), "F2": ("rel", 1e-2), "Z21": ("rel", 1e-2), "f_s": ("rel", 1e-2),
          "S2": ("abs", 5e-3)}


def stage_compare():
    mine_path = os.path.join(HERE, "xcheck2d_results.json")
    res = load_json(mine_path)
    qa = load_json(os.path.join(HERE, "qa_results.json"))
    comp = dict(note="relative difference = (xcheck - qa)/qa; own numbers above were saved before qa_results.json "
                     "was read (pre-comparison md5 recorded)", thresholds=THRESH, cases={})
    any_flag = False
    for case, key in QA_KEY.items():
        q = qa["points"][key]
        h = res["cases"][case]["M22"]
        pairs = {"a_star": (h["a_star"], q["astar"]), "c2": (h["c2"], q["c2"]), "cT": (h["cT"], q["cT"]),
                 "c1": (h["c1"], q["c1"]), "F2": (h["F2"], q["F2"]), "Z21": (h["Z21"], q["Z21"]),
                 "S2": (h["S2"], q["S2"]), "cT30": (h["cT30"], q["cT_30deg_kf005"])}
        if "f_s" in h:
            pairs["f_s"] = (h["f_s"], q["f_s"])
        rows = {}
        for name, (x, y) in pairs.items():
            kind, tol = THRESH[name]
            rel = (x - y) / y
            ab = x - y
            flag = (abs(rel) > tol) if kind == "rel" else (abs(ab) > tol)
            any_flag |= flag
            rows[name] = dict(xcheck=x, qa=y, rel_diff=rel, abs_diff=ab, exceeds_threshold=bool(flag))
        extra = {}
        extra["a_star_vs_qa_dedA_root"] = dict(xcheck=h["a_star"], qa=q["astar_crosscheck"]["dedA_root"],
                                               rel_diff=(h["a_star"] - q["astar_crosscheck"]["dedA_root"]) /
                                               q["astar_crosscheck"]["dedA_root"])
        extra["a_brent_xcheck_vs_qa_brent"] = dict(xcheck=h["a_brent"], qa=q["astar_crosscheck"]["brent"],
                                                   rel_diff=(h["a_brent"] - q["astar_crosscheck"]["brent"]) /
                                                   q["astar_crosscheck"]["brent"])
        extra["e_star"] = dict(xcheck=h["e_star"], qa=q["e_per_area"], rel_diff=(h["e_star"] - q["e_per_area"]) / q["e_per_area"])
        extra["mu_star"] = dict(xcheck=h["mu_star"], qa=q["mu"], rel_diff=(h["mu_star"] - q["mu"]) / q["mu"])
        extra["fsum_resid_max"] = dict(xcheck=h["fsum_resid_max_abs"], qa=q["fsum_resid_max"])
        extra["static_resid_max"] = dict(xcheck=h["chi_resid_max_abs"], qa=q["static_resid_max"])
        if "f_s" in h:
            fd = q["f_s_detail"]
            extra["f_s_twist_x_vs_qa_twist_x"] = dict(xcheck=h["f_s_x"], qa=fd["twist_x"],
                                                      rel_diff=(h["f_s_x"] - fd["twist_x"]) / fd["twist_x"])
            extra["f_s_twist_y_vs_qa_twist_y"] = dict(xcheck=h["f_s_y"], qa=fd["twist_y"],
                                                      rel_diff=(h["f_s_y"] - fd["twist_y"]) / fd["twist_y"])
            lr = h.get("f_s_linear_response_diagnostic")
            if lr:
                extra["f_s_lr_diag_vs_qa_lr"] = dict(xcheck=lr["x"], qa=fd["lr_x"], rel_diff=(lr["x"] - fd["lr_x"]) / fd["lr_x"])
        # per-q frequencies and weights along a1
        perq = []
        for r_m, r_q in zip(h["table_x"], q["per_q_a1"]):
            ent = dict(kappa=r_m["kappa"])
            for lab, lq in (("T", "T"), ("2", "2"), ("1", "1")):
                ent[f"om_{lab}_rel"] = (r_m[f"om_{lab}"] - r_q[lq]["omega"]) / r_q[lq]["omega"]
            ent["F2_rel"] = (r_m["F_2"] - r_q["2"]["F"]) / r_q["2"]["F"]
            ent["S2_abs"] = r_m["S_2"] - r_q["2"]["S"]
            ent["Z21_rel"] = (r_m["Z21"] - r_q["2"]["Z"] / r_q["1"]["Z"]) / (r_q["2"]["Z"] / r_q["1"]["Z"])
            ent["Z2_supercell_over_qa_Z2"] = r_m["Z_2"] / r_q["2"]["Z"]
            perq.append(ent)
        extra["per_q_a1"] = perq
        comp["cases"][case] = dict(qa_point=key, schema_quantities=rows, extra=extra)
    comp["any_exceeds_threshold"] = bool(any_flag)
    mx = {}
    for name in THRESH:
        vals = [abs(comp["cases"][c]["schema_quantities"][name]["rel_diff"]) for c in comp["cases"]
                if name in comp["cases"][c]["schema_quantities"]]
        mx[name] = max(vals)
    comp["max_abs_rel_diff_by_quantity"] = mx
    s2 = [abs(comp["cases"][c]["schema_quantities"]["S2"]["abs_diff"]) for c in comp["cases"]]
    comp["max_abs_diff_S2"] = max(s2)
    snap = os.path.join(WORK, "xcheck2d_results_precompare.json")
    if os.path.exists(snap):
        import hashlib
        comp["precompare_snapshot_md5"] = hashlib.md5(open(snap, "rb").read()).hexdigest()
        comp["precompare_snapshot_utc"] = "2026-10-04T16:14:23Z"
        comp["own_cases_identical_to_precompare_snapshot"] = bool(load_json(snap)["cases"] == res["cases"])
    diag = res.get("comparison_with_qa_results", {}).get("diagnosis_at_qa_reported_a")
    if diag is not None:
        comp["diagnosis_at_qa_reported_a"] = diag
    res["comparison_with_qa_results"] = comp
    save_json(mine_path, res)
    print(json.dumps({c: {k: (v["rel_diff"], v["exceeds_threshold"]) for k, v in comp["cases"][c]["schema_quantities"].items()}
                      for c in comp["cases"]}, indent=1))
    print("max", json.dumps(mx, indent=1), "S2 abs", comp["max_abs_diff_S2"], "any flag", any_flag)
    return comp


def stage_diag_qa_a(M=14):
    """post-comparison diagnosis only: re-evaluate this code's observables at the main instrument's reported
    (Brent, xatol = 1e-7 a) lattice constant, to test whether the residual ~1e-8..1e-7 differences are fully
    explained by that a* tolerance. Own reported numbers are NOT changed."""
    mine_path = os.path.join(HERE, "xcheck2d_results.json")
    res = load_json(mine_path)
    qa = load_json(os.path.join(HERE, "qa_results.json"))
    out = {}
    for case, key in QA_KEY.items():
        q = qa["points"][key]
        a_qa = q["astar"]
        a0, C0 = load_state(case, M)
        cell = Cell(a_qa, M, make_kernel(case))
        r = solve_state(cell, C0)
        C, mu = r["C"], r["mu"]
        qs, w = [], {"T": [], "2": [], "1": []}
        rec05 = None
        for kap in KAPPAS:
            qa_ = kap * TWOPI / a_qa
            b = bdg_solve(cell, C, mu, (qa_, 0.0))
            sel = np.where(b["frac_even"] > 0.5)[0][:4]
            rec = dict(low_even=[dict(om=float(b["om"][i]), Z=float(b["Z"][i]), par_y=float(b["par_y"][i]),
                                      F=float(b["om"][i] * b["Z"][i] / b["fsum_exact"]),
                                      S=float(2 * b["Z"][i] / b["om"][i] / b["chi_spec"])) for i in sel])
            lab = label_x(rec)
            qs.append(qa_)
            w["T"].append(lab["T"]["om"])
            w["2"].append(lab["two"]["om"])
            w["1"].append(lab["one"]["om"])
            if kap == 0.05:
                rec05 = lab
        vals = dict(c2=lsq_speed(qs, w["2"]), cT=lsq_speed(qs, w["T"]), c1=lsq_speed(qs, w["1"]),
                    F2=rec05["two"]["F"], Z21=rec05["two"]["Z"] / rec05["one"]["Z"], S2=rec05["two"]["S"],
                    e=r["e"], mu=mu)
        cmp_ = {}
        for nm, qn in (("c2", "c2"), ("cT", "cT"), ("c1", "c1"), ("F2", "F2"), ("Z21", "Z21"), ("S2", "S2"),
                       ("e", "e_per_area"), ("mu", "mu")):
            cmp_[nm] = dict(xcheck_at_qa_a=vals[nm], qa=q[qn], rel_diff=(vals[nm] - q[qn]) / q[qn])
        if case in ("step22", "step13.25"):
            Lm, X, T = bdg_matrices(cell, C, mu, (0.0, 0.0))
            c = C.ravel()
            d = 1j * cell.Gx.ravel() * c
            y = sla.solve(Lm + np.outer(c, c) * np.linalg.norm(Lm, 2), d)
            fs_lr = 1.0 - 2.0 * float(np.real(np.vdot(d, y)))
            cmp_["f_s_lr"] = dict(xcheck_at_qa_a=fs_lr, qa=q["f_s"], rel_diff=(fs_lr - q["f_s"]) / q["f_s"])
        out[case] = dict(a_qa=a_qa, M=M, gp_res=r["res"], values=cmp_)
        print(case, json.dumps({k: v["rel_diff"] for k, v in cmp_.items()}), flush=True)
    res.setdefault("comparison_with_qa_results", {})["diagnosis_at_qa_reported_a"] = out
    save_json(mine_path, res)
    return out


# ----------------------------------------------------------------------------------------------------------
# gamma6 quadrature validation
# ----------------------------------------------------------------------------------------------------------
def stage_quad():
    ker = Gamma6Kernel(1.0)
    k = np.concatenate([[0.0], np.linspace(1e-3, 260.0, 3001)])
    u1 = ker.uhat(k)
    u2 = uhat_g6_alt(k, 1.0, "ts")
    u3 = uhat_g6_alt(k, 1.0, "cgl")
    from scipy.special import gamma as Gf
    u0_exact = TWOPI * Gf(1.0 / 3.0) / 6.0
    from scipy.integrate import quad
    kq = [0.0, 1.0, 3.7, 4.5, 10.0, 25.0, 60.0]
    uq = []
    for kk in kq:
        v, err = quad(lambda r: np.exp(-r ** 6) * j0(kk * r) * r, 0.0, 2.6, limit=500, epsabs=1e-15, epsrel=1e-14)
        uq.append(TWOPI * v)
    u1q = ker.uhat(np.array(kq))
    # derivative check: k dU/dk by finite differences
    kk = np.linspace(0.5, 40.0, 50)
    h = 1e-5
    fd = kk * (ker.uhat(kk + h) - ker.uhat(kk - h)) / (2 * h)
    out = dict(U0_over_g_GL=float(u1[0]), U0_over_g_exact=float(u0_exact),
               max_abs_diff_GL_vs_tanhsinh_over_U0=float(np.max(np.abs(u1 - u2)) / u0_exact),
               max_abs_diff_GL_vs_compositeGL_over_U0=float(np.max(np.abs(u1 - u3)) / u0_exact),
               max_abs_diff_GL_vs_quadpack_over_U0=float(np.max(np.abs(u1q - np.array(uq))) / u0_exact),
               kdu_fd_max_rel=float(np.max(np.abs(fd - ker.kdu(kk))) / u0_exact),
               k_range=[0.0, 260.0], kmin_value=float(np.min(u1)), k_at_min=float(k[np.argmin(u1)]))
    save_json(os.path.join(WORK, "quad_g6.json"), out)
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    st = sys.argv[1]
    if st == "quad":
        stage_quad()
    elif st == "astar":
        stage_astar(sys.argv[2], int(sys.argv[3]),
                    *(float(v) for v in sys.argv[4:6]))
    elif st == "bdg":
        stage_bdg(sys.argv[2], int(sys.argv[3]))
    elif st == "fs":
        stage_fs(sys.argv[2], int(sys.argv[3]))
    elif st == "fslr":
        stage_fslr(sys.argv[2], int(sys.argv[3]))
    elif st == "compare":
        stage_compare()
    elif st == "diagqa":
        stage_diag_qa_a()
    elif st == "collect":
        stage_collect()
    else:
        raise SystemExit(__doc__)
