#!/usr/bin/env python3
"""cc3d.py -- second-leg 3D instrument (task Q-B): soft-sphere (step kernel) supersolid, AB (hcp-type)
stack of droplets.  Ground state by preconditioned L-BFGS on the energy + Newton-Krylov (GMRES) polish;
Bogoliubov-de Gennes spectrum in a plane-wave basis with a sphere cut |q+G| < Kcut (real-symmetric
Cholesky reduction, origin placed on an inversion centre so all BdG matrices are real).

Units hbar = m = R = 1, mean density 1.  e = <|grad psi|^2/2> + (Lam/2) <n (U*n)>,
Uhat(k) = 4 pi (sin k - k cos k)/k^3.

Discretisations of the ground state
  'sphere' : Galerkin plane-wave basis |G| < Kpsi with exact (alias-free) quadrature on an FFT grid of
             size M >= 4 h + 1 per axis (h = max Miller index in the sphere).  The discrete energy is an
             exact functional of the retained coefficients, invariant under all space-group operations.
  'box'    : classical pseudo-spectral FFT grid (all grid modes), odd grid sizes.

Usage (steps cache to WORK and are resumable):
  python3 cc3d.py lambdac
  python3 cc3d.py gs  --cell prim|orth --disc sphere|box --kpsi K | --grid N1 N2 N3
  python3 cc3d.py bdg --kpsi K --kcut K --dir x|y|z|xz45 --q 0.15 [--full]
  python3 cc3d.py assemble
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import sys
import json
import time
import argparse
import numpy as np
from scipy import fft as sfft
from scipy import optimize, linalg
from scipy.sparse.linalg import LinearOperator, gmres, cg

WORK = "/tmp/claude-0/-home-user-gifgaf0-github-io/6eab36f5-c943-5609-bc1f-38f855730ac1/scratchpad/work/qb"
OUTDIR = os.path.dirname(os.path.abspath(__file__))
A_LAT = 1.3859646002819213
C_LAT = 2.2595969088482843
NWORK = 2
os.makedirs(WORK, exist_ok=True)


# ----------------------------------------------------------------------------------------------
# kernel
# ----------------------------------------------------------------------------------------------
def _series_coeffs(nterms=18):
    # (sin k - k cos k)/k^3 = sum_{n>=1} (-1)^{n+1} 2n k^{2n-2} / (2n+1)!
    from math import factorial
    return np.array([(-1) ** (n + 1) * 2.0 * n / factorial(2 * n + 1) for n in range(1, nterms + 1)])


_SC = _series_coeffs()


def uhat(k):
    """Fourier transform of the unit step theta(1-r) in 3D."""
    k = np.asarray(k, dtype=float)
    out = np.empty_like(k)
    sm = k < 1.0
    if np.any(sm):
        k2 = k[sm] ** 2
        acc = np.zeros_like(k2)
        for cc in _SC[::-1]:
            acc = acc * k2 + cc
        out[sm] = acc
    if np.any(~sm):
        kb = k[~sm]
        out[~sm] = (np.sin(kb) - kb * np.cos(kb)) / kb ** 3
    return 4.0 * np.pi * out


def lambda_c():
    from scipy.optimize import brentq, minimize_scalar
    s = lambda k: np.sin(k) - k * np.cos(k)
    k0 = brentq(s, 4.0, 4.7, xtol=1e-15, rtol=1e-15)
    k1 = brentq(s, 7.5, 7.9, xtol=1e-15, rtol=1e-15)
    f = lambda k: float(-k * k / (4.0 * uhat(np.array([k]))[0]))
    res = minimize_scalar(f, bounds=(k0 + 1e-9, k1 - 1e-9), method="bounded",
                          options=dict(xatol=1e-14, maxiter=500))
    # stationarity: d/dk [k^5 / s(k)] = 0  <=>  5 s(k) = k^2 sin k
    g = lambda k: 5.0 * s(k) - k * k * np.sin(k)
    kst = brentq(g, res.x - 0.05, res.x + 0.05, xtol=1e-15, rtol=1e-15)
    lam_b, lam_s = f(res.x), f(kst)
    # brute-force scan check
    kk = np.linspace(k0 + 1e-6, k1 - 1e-6, 400001)
    vv = -kk ** 2 / (4 * uhat(kk))
    return dict(k_neg_window=[k0, k1], k_bounded=float(res.x), Lambda_c_bounded=lam_b,
                k_star=float(kst), Lambda_c_stationary=lam_s,
                abs_diff=abs(lam_b - lam_s), scan_min=float(vv.min()), scan_k=float(kk[vv.argmin()]),
                Lambda_c=lam_s, Lambda=2.0 * lam_s)


def get_lambda():
    p = os.path.join(WORK, "lambdac.json")
    if not os.path.exists(p):
        json.dump(lambda_c(), open(p, "w"), indent=1)
    return json.load(open(p))["Lambda"]


# ----------------------------------------------------------------------------------------------
# cells
# ----------------------------------------------------------------------------------------------
def cell_def(kind, a=A_LAT, c=C_LAT):
    if kind == "prim":
        lat = np.array([[a, 0, 0], [a / 2, np.sqrt(3) * a / 2, 0], [0, 0, c]], float)
        # origin on the inversion centre between the A site and the B site
        sites = np.array([[-1 / 6, -1 / 6, -1 / 4], [1 / 6, 1 / 6, 1 / 4]])
    elif kind == "orth":
        lat = np.array([[a, 0, 0], [0, np.sqrt(3) * a, 0], [0, 0, c]], float)
        sites = np.array([[0, 0, 0], [0.5, 0.5, 0], [0.5, 1 / 6, 0.5], [0, 2 / 3, 0.5]])
    else:
        raise ValueError(kind)
    return lat, sites


def recip(lat):
    return 2 * np.pi * np.linalg.inv(lat).T  # rows b_i, b_i . a_j = 2 pi delta_ij


def sphere_hmax(lat, K):
    # |m_i| = |G . a_i| / 2pi <= K |a_i| / 2pi
    return [int(np.floor(K * np.linalg.norm(lat[i]) / (2 * np.pi) + 1e-12)) for i in range(3)]


def odd_at_least(n):
    n = int(n)
    return n if n % 2 == 1 else n + 1


class Grid:
    """real-space FFT grid on the cell, rfft layout along the last axis."""

    def __init__(self, lat, shape, Lam):
        self.lat = np.array(lat, float)
        self.B = recip(self.lat)
        self.V = abs(np.linalg.det(self.lat))
        self.shape = tuple(int(s) for s in shape)
        self.Np = int(np.prod(self.shape))
        self.dV = self.V / self.Np
        self.N = self.V  # particles per cell at mean density 1
        self.Lam = Lam
        N1, N2, N3 = self.shape
        m1 = sfft.fftfreq(N1) * N1
        m2 = sfft.fftfreq(N2) * N2
        m3 = sfft.rfftfreq(N3) * N3
        self.m = (m1, m2, m3)
        Gx = (m1[:, None, None] * self.B[0, 0] + m2[None, :, None] * self.B[1, 0] + m3[None, None, :] * self.B[2, 0])
        Gy = (m1[:, None, None] * self.B[0, 1] + m2[None, :, None] * self.B[1, 1] + m3[None, None, :] * self.B[2, 1])
        Gz = (m1[:, None, None] * self.B[0, 2] + m2[None, :, None] * self.B[1, 2] + m3[None, None, :] * self.B[2, 2])
        self.G2 = Gx ** 2 + Gy ** 2 + Gz ** 2
        self.Gabs = np.sqrt(self.G2)
        self.Uk = uhat(self.Gabs)
        self.mask = np.ones(self.G2.shape, bool)
        self.sym = False  # True: restrict to inversion-even real functions (real Fourier coefficients)

    def spec(self, fh):
        return fh.real.astype(complex) if self.sym else fh

    def set_sphere(self, K):
        self.mask = self.Gabs < K
        self.K = K
        # alias-free check: max Miller index in sphere must satisfy N_i >= 4 h_i + 1
        h = sphere_hmax(self.lat, K)
        ok = all(self.shape[i] >= 4 * h[i] + 1 for i in range(3))
        return ok, h

    def rfft(self, f):
        return sfft.rfftn(f, workers=NWORK)

    def irfft(self, fh):
        return sfft.irfftn(fh, s=self.shape, workers=NWORK)

    def project(self, f):
        return self.irfft(self.spec(self.rfft(f)) * self.mask)

    def mult(self, f, m):
        return self.irfft(m * self.spec(self.rfft(f)))

    def parts(self, psi):
        ph = self.rfft(psi)
        lap = self.irfft(-self.G2 * ph)
        n = psi * psi
        nh = self.rfft(n)
        Phi = self.Lam * self.irfft(self.Uk * nh)
        return lap, n, Phi

    def energy(self, psi):
        lap, n, Phi = self.parts(psi)
        ekin = -0.5 * self.dV * np.sum(psi * lap)
        eint = 0.5 * self.dV * np.sum(n * Phi)
        return ekin, eint, lap, n, Phi

    def hpsi(self, psi):
        lap, n, Phi = self.parts(psi)
        return self.project(-0.5 * lap + Phi * psi)

    def initial(self, sites, sigma=0.3):
        N1, N2, N3 = self.shape
        s1 = np.arange(N1) / N1
        s2 = np.arange(N2) / N2
        s3 = np.arange(N3) / N3
        S = np.stack(np.meshgrid(s1, s2, s3, indexing="ij"), -1)
        psi = np.zeros(self.shape)
        for st in sites:
            d = S - st
            d -= np.round(d)
            for sh in np.array(np.meshgrid([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], indexing="ij")).reshape(3, -1).T:
                r = (d + sh) @ self.lat
                psi += np.exp(-np.sum(r * r, -1) / (2 * sigma ** 2))
        psi = self.project(psi + 0.02)
        psi *= np.sqrt(self.N / (self.dV * np.sum(psi * psi)))
        return psi


# ----------------------------------------------------------------------------------------------
# ground state: preconditioned L-BFGS + Newton-Krylov
# ----------------------------------------------------------------------------------------------
def lbfgs_ground_state(g, psi0, alpha=20.0, maxiter=5000, log=None):
    Mh = np.sqrt(alpha / (alpha + 0.5 * g.G2)) * g.mask
    y0 = g.mult(psi0, g.mask / np.where(Mh > 0, Mh, 1.0))
    nfev = [0]

    def fun(yflat):
        y = yflat.reshape(g.shape)
        phi = g.mult(y, Mh)
        nphi = g.dV * np.sum(phi * phi)
        s = np.sqrt(g.N / nphi)
        psi = s * phi
        ekin, eint, lap, n, Phi = g.energy(psi)
        E = ekin + eint
        gpsi = 2 * g.dV * (-0.5 * lap + Phi * psi)
        gphi = s * (gpsi - phi * (g.dV * np.sum(phi * gpsi)) / nphi)
        gy = g.mult(gphi, Mh)
        nfev[0] += 1
        return E, gy.ravel()

    t0 = time.time()
    res = optimize.minimize(fun, y0.ravel(), jac=True, method="L-BFGS-B",
                            options=dict(maxiter=maxiter, maxcor=40, ftol=1e-17, gtol=1e-13, maxfun=4 * maxiter))
    y = res.x.reshape(g.shape)
    phi = g.mult(y, Mh)
    psi = phi * np.sqrt(g.N / (g.dV * np.sum(phi * phi)))
    info = dict(lbfgs_nit=int(res.nit), lbfgs_nfev=nfev[0], lbfgs_msg=str(res.message), lbfgs_time=time.time() - t0,
                lbfgs_E=float(res.fun))
    return psi, info


def gs_residual(g, psi):
    hp = g.hpsi(psi)
    mu = np.sum(psi * hp) / np.sum(psi * psi)
    r = hp - mu * psi
    return mu, r


def newton_polish(g, psi, tol=1e-11, maxit=12, log=None):
    """Newton on F(psi,mu) = [P(H psi - mu psi); (dV sum psi^2 - N)/2] with GMRES and a kinetic preconditioner."""
    shp, Np = g.shape, g.Np
    hist = []
    sig = 20.0
    pre = g.mask / (0.5 * g.G2 + sig)
    border = not g.sym  # without the inversion restriction, border the system with the 3 translation modes
    nb = 4 if border else 1
    for it in range(maxit):
        mu, r = gs_residual(g, psi)
        nrm = (g.dV * np.sum(psi * psi) - g.N) / 2
        res_max = float(np.max(np.abs(r)))
        res_rms = float(np.sqrt(np.mean(r * r)) / np.sqrt(np.mean(psi * psi)))
        hist.append(dict(it=it, mu=float(mu), res_max=res_max, res_rel_rms=res_rms, norm_err=float(nrm)))
        if log:
            log(f"  newton it {it}: mu={mu!r} res_max={res_max:.3e} rel_rms={res_rms:.3e} norm={nrm:.2e}")
        if res_max < tol and abs(nrm) < 1e-12 * g.N:
            break
        lap, n, Phi = g.parts(psi)
        if border:
            ph = g.rfft(psi)
            Gc = [None] * 3
            m1, m2, m3 = g.m
            for j in range(3):
                Gc[j] = (m1[:, None, None] * g.B[0, j] + m2[None, :, None] * g.B[1, j] + m3[None, None, :] * g.B[2, j])
            dts = [g.irfft(1j * Gc[j] * ph * g.mask) for j in range(3)]
            dts = [dd / np.sqrt(g.dV * np.sum(dd * dd)) for dd in dts]

        def jac(x):
            d = x[:Np].reshape(shp)
            dmu = x[Np]
            dlap = g.irfft(-g.G2 * g.rfft(d))
            dPhi = g.Lam * g.irfft(g.Uk * g.rfft(2 * psi * d))
            out = -0.5 * dlap + Phi * d - mu * d + dPhi * psi - dmu * psi
            extra = [g.dV * np.sum(psi * d)]
            if border:
                for j in range(3):
                    out = out + x[Np + 1 + j] * dts[j]
                    extra.append(g.dV * np.sum(dts[j] * d))
            out = g.project(out)
            return np.concatenate([out.ravel(), extra])

        def prec(x):
            d = x[:Np].reshape(shp)
            return np.concatenate([g.mult(d, pre).ravel(), [x[Np] / g.N], x[Np + 1:]])

        J = LinearOperator((Np + nb, Np + nb), matvec=jac, dtype=float)
        P = LinearOperator((Np + nb, Np + nb), matvec=prec, dtype=float)
        rhs = -np.concatenate([r.ravel(), [nrm], np.zeros(nb - 1)])
        dx, info = gmres(J, rhs, M=P, rtol=1e-9, atol=0.0, restart=100, maxiter=20)
        psi = psi + dx[:Np].reshape(shp)
        psi = g.project(psi)
    mu, r = gs_residual(g, psi)
    return psi, float(mu), hist


def lat_tag(a, c):
    return "" if (a == A_LAT and c == C_LAT) else f"_a{a!r}_c{c!r}"


def gs_key(cell, disc, kpsi=None, grid=None, a=A_LAT, c=C_LAT):
    if disc == "sphere":
        return f"gs_{cell}_sphere_K{kpsi:g}" + lat_tag(a, c)
    return f"gs_{cell}_box_{grid[0]}x{grid[1]}x{grid[2]}" + lat_tag(a, c)


def solve_gs(cell, disc, kpsi=None, grid=None, mfac=4, log=print, seed_from=None, a=A_LAT, c=C_LAT):
    Lam = get_lambda()
    lat, sites = cell_def(cell, a, c)
    if disc == "sphere":
        h = sphere_hmax(lat, kpsi)
        shape = [odd_at_least(mfac * hh + 1) for hh in h]
        g = Grid(lat, shape, Lam)
        ok, h = g.set_sphere(kpsi)
        assert ok
    else:
        g = Grid(lat, grid, Lam)
    g.sym = (cell == "prim")  # origin on an inversion centre only in the primitive set-up
    key = gs_key(cell, disc, kpsi, grid, a, c)
    t0 = time.time()
    psi0 = None
    if seed_from is not None and os.path.exists(os.path.join(WORK, seed_from + ".npz")):
        psi0 = interp_seed(g, os.path.join(WORK, seed_from + ".npz"))
    if psi0 is None:
        psi0 = g.initial(sites)
    psi, info = lbfgs_ground_state(g, psi0, maxiter=3000, log=log)
    log(f"  lbfgs: {info}")
    psi, mu, hist = newton_polish(g, psi, log=log)
    ekin, eint, lap, n, Phi = g.energy(psi)
    E = ekin + eint
    mu2, r = gs_residual(g, psi)
    # mu from virial-type formula: (Ekin + 2 Eint)/N
    mu_alt = (ekin + 2 * eint) / g.N
    ph = g.rfft(psi) / g.Np
    out = dict(cell=cell, disc=disc, kpsi=kpsi, a=a, c=c, shape=list(g.shape), V=g.V, Ncell=g.N, Lambda=Lam,
               E_cell=float(E), e_per_particle=float(E / g.N), ekin_per_particle=float(ekin / g.N),
               eint_per_particle=float(eint / g.N), mu=float(mu2), mu_alt=float(mu_alt),
               res_max=float(np.max(np.abs(r))), res_rel_rms=float(np.sqrt(np.mean(r * r) / np.mean(psi * psi))),
               norm_check=float(g.dV * np.sum(psi * psi) / g.N - 1), psi_min=float(psi.min()),
               psi_max=float(psi.max()), n_max=float((psi ** 2).max()), n_min=float((psi ** 2).min()),
               newton=hist, time=time.time() - t0, **info)
    if disc == "sphere":
        out["n_coeffs"] = int(g.mask.sum())
    # Fourier tail diagnostics: max |psi_hat| on shells
    ga = g.Gabs
    shells = {}
    for kk in [10, 15, 20, 25, 30, 35, 40, 45, 50, 60]:
        sel = ga >= kk
        if sel.any():
            shells[str(kk)] = float(np.max(np.abs(ph[sel])))
    out["psihat_tail_max_beyond_K"] = shells
    out["psihat_imag_max"] = float(np.max(np.abs(ph.imag)))
    np.savez(os.path.join(WORK, key + ".npz"), psi=psi, shape=np.array(g.shape), lat=lat, mu=mu2, E=E,
             kpsi=(kpsi if kpsi is not None else -1.0))
    json.dump(out, open(os.path.join(WORK, key + ".json"), "w"), indent=1)
    return out


def interp_seed(g, path):
    """Fourier-interpolate a cached state of the same cell onto grid g (truncate/zero-pad), then project."""
    d = np.load(path)
    # the grid lives in fractional coordinates, so coefficients are copied by Miller index (any lattice)
    psi_old = d["psi"]
    sh_old = tuple(int(s) for s in d["shape"])
    ph_old = sfft.fftn(psi_old, workers=NWORK) / np.prod(sh_old)
    ph_new = np.zeros(g.shape, complex)
    # copy common index ranges (odd sizes, symmetric index sets)
    idx = []
    for so, sn in zip(sh_old, g.shape):
        h = min((so - 1) // 2, (sn - 1) // 2)
        idx.append(np.r_[0:h + 1, -h:0])
    io = np.ix_(*[np.mod(ix, so) for ix, so in zip(idx, sh_old)])
    inew = np.ix_(*[np.mod(ix, sn) for ix, sn in zip(idx, g.shape)])
    ph_new[inew] = ph_old[io]
    psi = np.real(sfft.ifftn(ph_new * g.Np, workers=NWORK))
    psi = g.project(psi)
    psi *= np.sqrt(g.N / (g.dV * np.sum(psi * psi)))
    return psi


def load_gs(cell, disc, kpsi=None, grid=None, a=A_LAT, c=C_LAT):
    key = gs_key(cell, disc, kpsi, grid, a, c)
    d = np.load(os.path.join(WORK, key + ".npz"))
    info = json.load(open(os.path.join(WORK, key + ".json")))
    return d, info




# ----------------------------------------------------------------------------------------------
# BdG in the plane-wave sphere basis |q+G| < Kcut (primitive cell, inversion-centred origin)
# ----------------------------------------------------------------------------------------------
DIRS = {"x": np.array([1.0, 0.0, 0.0]), "y": np.array([0.0, 1.0, 0.0]), "z": np.array([0.0, 0.0, 1.0]),
        "xz45": np.array([1.0, 0.0, 1.0]) / np.sqrt(2.0)}


def symmetry_ops(a=A_LAT, c=C_LAT):
    """space-group operations r -> R r + t of the primitive set-up (sites at +-(1/6,1/6,1/4))."""
    return {
        "mirror_z": (np.diag([1.0, 1.0, -1.0]), np.array([0.0, 0.0, -c / 2])),        # through a layer
        "glide_y": (np.diag([1.0, -1.0, 1.0]), np.array([0.0, -np.sqrt(3) * a / 2, c / 2])),  # c-glide normal to y
        "mirror_x": (np.diag([-1.0, 1.0, 1.0]), np.array([-a / 2, 0.0, 0.0])),
    }


LITTLE = {"x": ["mirror_z", "glide_y"], "y": ["mirror_x", "mirror_z"], "z": ["mirror_x", "glide_y"],
          "xz45": ["glide_y"]}


def enum_sphere(lat, B, q, K):
    h = sphere_hmax(lat, K + np.linalg.norm(q))
    r = [np.arange(-hh, hh + 1) for hh in h]
    M = np.stack(np.meshgrid(*r, indexing="ij"), -1).reshape(-1, 3)
    kq = q + M @ B
    kn = np.linalg.norm(kq, axis=1)
    sel = kn < K
    M, kq, kn = M[sel], kq[sel], kn[sel]
    order = np.lexsort((M[:, 2], M[:, 1], M[:, 0], np.round(kn, 10)))
    return M[order], kq[order], kn[order]


def padded(arr_c, W):
    """embed a centred array (odd sizes) into a zero-padded/truncated centred array of half-widths W."""
    W = [int(w) for w in W]
    out = np.zeros([2 * w + 1 for w in W], dtype=arr_c.dtype)
    sl_o, sl_i = [], []
    for ax, w in enumerate(W):
        h = (arr_c.shape[ax] - 1) // 2
        o = min(h, w)
        sl_o.append(slice(w - o, w + o + 1))
        sl_i.append(slice(h - o, h + o + 1))
    out[tuple(sl_o)] = arr_c[tuple(sl_i)]
    return out


class GSData:
    def __init__(self, kpsi, a=A_LAT, c=C_LAT):
        d, info = load_gs("prim", "sphere", kpsi, a=a, c=c)
        self.a, self.c = a, c
        self.info = info
        self.kpsi = float(kpsi)
        self.psi = d["psi"]
        self.shape = tuple(int(s) for s in d["shape"])
        self.lat = np.array(d["lat"])
        self.B = recip(self.lat)
        self.V = abs(np.linalg.det(self.lat))
        self.N = self.V
        self.mu = float(info["mu"])
        self.Lam = float(info["Lambda"])
        Np = int(np.prod(self.shape))
        ph = sfft.fftn(self.psi, workers=NWORK) / Np
        mm = [np.rint(sfft.fftfreq(n) * n).astype(int) for n in self.shape]
        Mg = np.stack(np.meshgrid(*mm, indexing="ij"), -1)
        Gn = np.linalg.norm(Mg @ self.B, axis=-1)
        self.psihat_imag_max = float(np.max(np.abs(ph.imag)))
        self.psihat_outside_max = float(np.max(np.abs(ph[Gn >= kpsi])))
        phr = np.where(Gn < kpsi, ph.real, 0.0)
        nh = sfft.fftn(self.psi ** 2, workers=NWORK) / Np
        self.nhat_imag_max = float(np.max(np.abs(nh.imag)))
        nhr = np.where(Gn < 2 * kpsi, nh.real, 0.0)
        self.cpsi = sfft.fftshift(phr)
        self.cn = sfft.fftshift(nhr)
        self.cPhi = sfft.fftshift(self.Lam * uhat(Gn) * nhr)
        G = Mg @ self.B
        self.dnorm = [float(np.sqrt(np.sum((G[..., j] * nhr) ** 2))) for j in range(3)]
        self.hpsi = np.array(sphere_hmax(self.lat, kpsi))
        self.hgrid = np.array([(n - 1) // 2 for n in self.shape])


class BdGq:
    """dense real-symmetric L(q), X(q) in the sphere basis; A = L + 2X."""

    def __init__(self, gsd, qvec, kcut, chunk=2500, log=print):
        t0 = time.time()
        self.g = gsd
        q = np.asarray(qvec, float)
        self.q = q
        self.kcut = float(kcut)
        lat, B = gsd.lat, gsd.B
        self.Mb, self.kq, self.kn = enum_sphere(lat, B, q, kcut)
        Nb = len(self.Mb)
        self.Nb = Nb
        hb = np.max(np.abs(self.Mb), 0)
        self.hb = hb
        # density vector s = e^{iqr} psi0 in the orthonormal basis e^{i(q+G)r}/sqrt(V)
        Pp0 = padded(gsd.cpsi, hb)
        self.s = np.sqrt(gsd.V) * Pp0[tuple((self.Mb + hb).T)]
        # ---- L
        W2 = 2 * hb
        Pphi = padded(gsd.cPhi, W2).ravel()
        n1, n2 = 2 * W2[1] + 1, 2 * W2[2] + 1
        lin = self.Mb[:, 0] * (n1 * n2) + self.Mb[:, 1] * n2 + self.Mb[:, 2]
        base = W2[0] * n1 * n2 + W2[1] * n2 + W2[2]
        L = np.empty((Nb, Nb), order="F")
        for i0 in range(0, Nb, 1000):
            i1 = min(Nb, i0 + 1000)
            L[i0:i1, :] = Pphi[base + lin[i0:i1, None] - lin[None, :]]
        L[np.diag_indices(Nb)] += 0.5 * self.kn ** 2 - gsd.mu
        self.L = L
        # ---- X = Lam * Psi diag(U) Psi^T, Psi_{ik} = psi_hat(G_i - G''_k), |q+G''| < Kcut + Kpsi
        Mpp, kqpp, knpp = enum_sphere(lat, B, q, kcut + gsd.kpsi)
        self.Npp = len(Mpp)
        hpp = np.max(np.abs(Mpp), 0)
        Wd = hb + hpp
        Ppsi = padded(gsd.cpsi, Wd).ravel()
        n1, n2 = 2 * Wd[1] + 1, 2 * Wd[2] + 1
        lin_b = self.Mb[:, 0] * (n1 * n2) + self.Mb[:, 1] * n2 + self.Mb[:, 2]
        lin_p = Mpp[:, 0] * (n1 * n2) + Mpp[:, 1] * n2 + Mpp[:, 2]
        base = Wd[0] * n1 * n2 + Wd[1] * n2 + Wd[2]
        Upp = uhat(knpp)
        X = np.zeros((Nb, Nb), order="F")
        syrk = linalg.blas.dsyrk
        for k0 in range(0, self.Npp, chunk):
            k1 = min(self.Npp, k0 + chunk)
            PT = Ppsi[base + lin_b[None, :] - lin_p[k0:k1, None]]  # (nk, Nb), C order
            u = Upp[k0:k1]
            for sgn, sel in ((1.0, u > 0), (-1.0, u < 0)):
                if not np.any(sel):
                    continue
                Aw = PT[sel] * np.sqrt(np.abs(u[sel]))[:, None]
                X = syrk(sgn, Aw.T, beta=1.0, c=X, trans=0, lower=0, overwrite_c=1)
        iu = np.triu_indices(Nb, 1)
        X[(iu[1], iu[0])] = X[iu]
        X *= gsd.Lam
        self.X = X
        self.t_build = time.time() - t0
        log(f"  built L,X: Nb={Nb} Npp={self.Npp} hb={hb.tolist()} in {self.t_build:.1f}s")

    def sLs(self):
        return float(self.s @ (self.L @ self.s))

    def solve(self, nlow=30, full=False, keep_vectors=True, log=print):
        t0 = time.time()
        Nb = self.Nb
        A = self.L + 2.0 * self.X
        self.X = None
        sLs = self.sLs()
        C = linalg.cholesky(A, lower=True, overwrite_a=True, check_finite=False)
        A = None
        t = linalg.solve_triangular(C, self.s, lower=True, check_finite=False)
        chi_direct = 2.0 * float(t @ t)
        Wm = linalg.blas.dtrmm(1.0, C, self.L, side=1, lower=1, overwrite_b=1)  # L C
        self.L = None
        K = linalg.blas.dtrmm(1.0, C, Wm, side=0, lower=1, trans_a=1, overwrite_b=1)  # C^T L C
        Wm = None
        t1 = time.time()  # eigh reads the lower triangle of K only
        if full:
            w2, Wv = linalg.eigh(K, driver="evd", overwrite_a=True, check_finite=False)
        else:
            w2, Wv = linalg.eigh(K, subset_by_index=[0, nlow - 1], driver="evr", overwrite_a=True,
                                 check_finite=False)
        K = None
        t2 = time.time()
        neg = int(np.sum(w2 < 0))
        om = np.sqrt(np.abs(w2))
        proj = t @ Wv
        Z = om * proj ** 2
        res = dict(Nb=Nb, chi_direct=chi_direct, sLs=sLs, omega2_min=float(w2[0]), n_negative_omega2=neg,
                   t_chol_trmm=t1 - t0, t_eigh=t2 - t1)
        if full:
            res["fsum_spectral"] = float(np.sum(om * Z))
            res["static_spectral"] = float(np.sum(2.0 * Z / om))
            res["omega_max"] = float(om[-1])
        nk = min(nlow, len(om))
        fp = linalg.solve_triangular(C, Wv[:, :nk], trans="T", lower=True, check_finite=False) * np.sqrt(om[:nk])
        self.C = C if keep_vectors else None
        return res, om, Z, fp


class MFq:
    """matrix-free FFT application of L(q), X(q), A(q) on sphere-basis vectors (independent code path)."""

    def __init__(self, gsd, bq):
        self.g, self.bq = gsd, bq
        q = bq.q
        hb = bq.hb
        hp = gsd.hpsi
        M = [odd_at_least(2 * hp[i] + 2 * hb[i] + 1) for i in range(3)]
        self.M = tuple(M)
        self.Mt = int(np.prod(M))
        hm = np.array([(m - 1) // 2 for m in M])
        mm = [np.rint(sfft.fftfreq(n) * n).astype(int) for n in M]
        Mg = np.stack(np.meshgrid(*mm, indexing="ij"), -1)
        self.Gc = Mg @ gsd.B  # G (without q) on the grid
        kq = q + self.Gc
        self.U = gsd.Lam * uhat(np.linalg.norm(kq, axis=-1))
        cps = padded(gsd.cpsi, hm)
        self.psi = np.real(sfft.ifftn(sfft.ifftshift(cps), workers=NWORK)) * self.Mt
        p = np.minimum(2 * hp, 2 * hb)
        cph = padded(padded(gsd.cPhi, p), hm)
        self.Phi = np.real(sfft.ifftn(sfft.ifftshift(cph), workers=NWORK)) * self.Mt
        self.nhat = sfft.ifftshift(padded(gsd.cn, hm))
        self.pos = tuple(np.mod(bq.Mb[:, i], M[i]) for i in range(3))
        self.kin = 0.5 * bq.kn ** 2 - gsd.mu

    def to_grid(self, f):
        F = np.zeros(self.M, complex)
        F[self.pos] = f
        return sfft.ifftn(F, workers=NWORK) * self.Mt

    def coeffs(self, gr):
        return sfft.fftn(gr, workers=NWORK) / self.Mt

    def apply_L(self, f):
        fr = self.to_grid(f)
        return self.kin * f + self.coeffs(self.Phi * fr)[self.pos]

    def apply_X(self, f):
        fr = self.to_grid(f)
        gh = self.coeffs(self.psi * fr) * self.U
        h = sfft.ifftn(gh, workers=NWORK) * self.Mt
        return self.coeffs(self.psi * h)[self.pos]

    def apply_A(self, f):
        fr = self.to_grid(f)
        Lf = self.kin * f + self.coeffs(self.Phi * fr)[self.pos]
        gh = self.coeffs(self.psi * fr) * self.U
        h = sfft.ifftn(gh, workers=NWORK) * self.Mt
        Xf = self.coeffs(self.psi * h)[self.pos]
        return Lf + 2.0 * Xf

    def chi_cg(self, tol=1e-14):
        bq = self.bq
        n = bq.Nb
        Aop = LinearOperator((n, n), matvec=lambda v: np.real(self.apply_A(v)), dtype=float)
        Pop = LinearOperator((n, n), matvec=lambda v: v / (0.5 * bq.kn ** 2 + 50.0), dtype=float)
        it = [0]

        def cb(xk):
            it[0] += 1
        x, info = cg(Aop, bq.s, M=Pop, rtol=tol, atol=0.0, maxiter=20000, callback=cb)
        r = bq.s - Aop.matvec(x)
        return 2.0 * float(bq.s @ x), dict(cg_info=int(info), cg_iter=it[0],
                                            cg_rel_residual=float(np.linalg.norm(r) / np.linalg.norm(bq.s)))

    def density_coeffs(self, f):
        return self.coeffs(self.psi * self.to_grid(f))

    def disp_cos(self, f):
        """cosines between delta rho = psi0 f_plus and e^{iqr} d_j rho0, j = x,y,z."""
        dr = self.density_coeffs(f)
        out = []
        ndr = np.sqrt(np.sum(np.abs(dr) ** 2))
        for j in range(3):
            dj = 1j * self.Gc[..., j] * self.nhat
            out.append(float(np.abs(np.vdot(dj, dr)) / (self.g.dnorm[j] * ndr)))
        return out


def sym_action(bq, R, t):
    """index permutation + phases of the operation (R,t) on the sphere basis at q (requires R q = q)."""
    q = bq.q
    assert np.allclose(R @ q, q)
    G = bq.kq - q
    RG = G @ R.T
    Mp = np.rint(RG @ bq.g.lat.T / (2 * np.pi)).astype(int)
    assert np.allclose(Mp @ bq.g.B, RG, atol=1e-9)
    hb = bq.hb
    lut = -np.ones([2 * h + 1 for h in hb], dtype=np.int64)
    lut[tuple((bq.Mb + hb).T)] = np.arange(bq.Nb)
    perm = lut[tuple((Mp + hb).T)]
    assert np.all(perm >= 0)
    phase = np.exp(-1j * ((q + RG) @ t))
    return perm, phase


def apply_sym(f, perm, phase):
    out = np.zeros(f.shape, complex)
    out[perm] = f * phase
    return out


def superfluid_fraction_lr(K, log=print):
    """EXTRA: linear-response superfluid fraction tensor (diagonal) f_s,j = 1 - (2/N) <d_j psi0| L^-1 |d_j psi0>
    in the Gamma sector (d_j psi0 is inversion-odd, hence orthogonal to the zero mode psi0)."""
    path = os.path.join(WORK, f"fs_lr_P{K:g}_C{K:g}.json")
    if os.path.exists(path):
        return json.load(open(path))
    gsd = GSData(K)
    bq = BdGq(gsd, np.zeros(3), K, log=log)
    s = bq.s
    Lr = bq.L + np.outer(s, s) / float(s @ s)  # lifts the phase zero mode; does not act on odd vectors
    Cf = linalg.cho_factor(Lr, lower=True, overwrite_a=True, check_finite=False)
    out = dict(K=K, Nb=bq.Nb)
    for j, nm in enumerate("xyz"):
        dv = bq.kq[:, j] * s  # real representative of the coefficients of d_j psi0
        x = linalg.cho_solve(Cf, dv, check_finite=False)
        out[f"orth_check_{nm}"] = float(abs(dv @ s) / (np.linalg.norm(dv) * np.linalg.norm(s)))
        out[f"fs_{nm}"] = float(1.0 - 2.0 / gsd.N * (dv @ x))
    json.dump(out, open(path, "w"), indent=1)
    return out


def bdg_key(kpsi, kcut, dname, qmag, full, a=A_LAT, c=C_LAT):
    return f"bdg_P{kpsi:g}_C{kcut:g}_{dname}_q{qmag:g}" + ("_full" if full else "") + lat_tag(a, c)


def run_bdg(kpsi, kcut, dname, qmag, nlow=30, full=False, log=print, do_cg=True, a=A_LAT, c=C_LAT):
    key = bdg_key(kpsi, kcut, dname, qmag, full, a, c)
    path = os.path.join(WORK, key + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    T0 = time.time()
    gsd = GSData(kpsi, a, c)
    qv = qmag * DIRS[dname]
    bq = BdGq(gsd, qv, kcut, log=log)
    mf = MFq(gsd, bq)
    ops = symmetry_ops(a, c)
    lg = LITTLE[dname]
    acts = {nm: sym_action(bq, *ops[nm]) for nm in lg}
    # symmetry check of the ground state through s: O s = e^{-i q.t} s
    symchk = {}
    for nm in lg:
        Os = apply_sym(bq.s, *acts[nm])
        ph = np.exp(-1j * (qv @ ops[nm][1]))
        symchk[nm] = float(np.linalg.norm(Os - ph * bq.s) / np.linalg.norm(bq.s))
    # cross-check of dense vs matrix-free operators on a random vector
    rng = np.random.default_rng(1)
    v = rng.standard_normal(bq.Nb) / (1.0 + bq.kn ** 2)
    Ad = bq.L @ v + 2.0 * (bq.X @ v)
    Am = np.real(mf.apply_A(v))
    dense_vs_mf = float(np.linalg.norm(Ad - Am) / np.linalg.norm(Ad))
    Ls_mf = float(bq.s @ np.real(mf.apply_L(bq.s)))
    res, om, Z, fp = bq.solve(nlow=nlow, full=full, log=log)
    res.update(dense_vs_matrixfree_rel=dense_vs_mf, sLs_matrixfree=Ls_mf, sym_check_s=symchk)
    Ncell = gsd.N
    fsum_exact = Ncell * qmag ** 2 / 2.0
    res["fsum_exact"] = fsum_exact
    res["sLs_rel_dev"] = (res["sLs"] - fsum_exact) / fsum_exact
    if do_cg:
        t0 = time.time()
        chi_cg, cginfo = mf.chi_cg()
        res.update(chi_cg=chi_cg, t_cg=time.time() - t0, **cginfo)
        res["chi_direct_vs_cg_rel"] = (res["chi_direct"] - chi_cg) / chi_cg
    if full:
        res["fsum_rel_residual"] = (res["fsum_spectral"] - fsum_exact) / fsum_exact
        if do_cg:
            res["static_rel_residual_vs_cg"] = (res["static_spectral"] - chi_cg) / chi_cg
        res["static_rel_residual_vs_direct"] = (res["static_spectral"] - res["chi_direct"]) / res["chi_direct"]
    chi = res["chi_direct"]
    res["c_kappa"] = float(np.sqrt(gsd.V / chi))
    # ---- per-mode diagnostics
    nk = fp.shape[1]
    # degenerate groups -> diagonalise the first little-group operation inside the group
    fpc = fp.astype(complex)
    i = 0
    groups = []
    while i < nk:
        j = i + 1
        while j < nk and abs(om[j] - om[i]) < 1e-6 * max(om[i], 1e-3):
            j += 1
        if j - i > 1 and j <= nk:
            groups.append([i, j])
            F = fp[:, i:j]
            OF = np.stack([apply_sym(F[:, k], *acts[lg[0]]) for k in range(j - i)], 1)
            T = np.linalg.lstsq(F.astype(complex), OF, rcond=None)[0]
            ev, E = np.linalg.eig(T)
            newF = F.astype(complex) @ E
            for k in range(j - i):
                fk = newF[:, k]
                # make it real if possible (remove global phase), normalise in the A-metric
                ph = np.exp(-1j * np.angle(fk[np.argmax(np.abs(fk))]))
                fk = fk * ph
                nrm = np.real(np.vdot(fk, mf.apply_A(fk))) / om[i + k]
                fpc[:, i + k] = fk / np.sqrt(nrm)
        i = j
    modes = []
    snorm = np.linalg.norm(bq.s)
    for k in range(nk):
        f = fpc[:, k]
        rho = np.vdot(bq.s, f)
        Zk = float(np.abs(rho) ** 2)
        par = {}
        for nm in lg:
            Of = apply_sym(f, *acts[nm])
            ph = np.exp(-1j * (qv @ ops[nm][1]))
            par[nm] = complex(np.vdot(f, Of) / np.vdot(f, f) / ph)
        dc = mf.disp_cos(f)
        modes.append(dict(omega=float(om[k]), Z=Zk, Z_from_eig=float(Z[k]), F=float(om[k] * Zk / fsum_exact),
                          S=float(2 * Zk / om[k] / chi),
                          rho_rel=float(np.abs(rho) / (snorm * np.linalg.norm(f))),
                          parity={nm: [par[nm].real, par[nm].imag] for nm in lg},
                          disp_cos=dc))
    res.update(kpsi=kpsi, kcut=kcut, dir=dname, q=qmag, a=a, c=c, qvec=qv.tolist(), Npp=bq.Npp, hb=bq.hb.tolist(),
               mf_grid=list(mf.M), t_build=bq.t_build, degenerate_groups=groups, modes=modes, V=gsd.V, Ncell=Ncell,
               mu=gsd.mu, psihat_imag_max=gsd.psihat_imag_max, t_total=time.time() - T0)
    json.dump(res, open(path, "w"), indent=1)
    return res


def gamma_check(kpsi, kcut, nev=8, log=print):
    """q = 0 sector: lowest eigenvalues of L(0) (phase mode) and A(0) (translations)."""
    key = f"gamma_P{kpsi:g}_C{kcut:g}"
    path = os.path.join(WORK, key + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    gsd = GSData(kpsi)
    bq = BdGq(gsd, np.zeros(3), kcut, log=log)
    eL = linalg.eigh(bq.L, eigvals_only=True, subset_by_index=[0, nev - 1])
    A = bq.L + 2 * bq.X
    eA, vA = linalg.eigh(A, subset_by_index=[0, nev - 1])
    # residual of L psi0 and A d_j psi0 in this basis
    s = bq.s
    Lpsi = bq.L @ s
    out = dict(kpsi=kpsi, kcut=kcut, Nb=bq.Nb, L_lowest=eL.tolist(), A_lowest=eA.tolist(),
               L_psi0_rel=float(np.linalg.norm(Lpsi) / np.linalg.norm(s)))
    for j, nm in enumerate("xyz"):
        dpsi = 1j * bq.kq[:, j] * s  # coefficients of d_j psi0 (imaginary since psi_hat real & even)
        dv = dpsi.imag
        out[f"A_dpsi_{nm}_rel"] = float(np.linalg.norm(A @ dv) / np.linalg.norm(dv))
    json.dump(out, open(path, "w"), indent=1)
    return out


# ----------------------------------------------------------------------------------------------
# mode identification and assembly
# ----------------------------------------------------------------------------------------------
SECTORS = {"x": {(1, 1): "L", (1, -1): "Ty", (-1, 1): "Tz", (-1, -1): "odd_odd"},
           "y": {(1, 1): "L", (-1, 1): "Tx", (1, -1): "Tz", (-1, -1): "odd_odd"},
           "z": {(1, 1): "L", (-1, 1): "Tx", (1, -1): "Ty", (-1, -1): "odd_odd"},
           "xz45": {(1,): "L_mixed", (-1,): "Ty"}}


def mode_sector(dname, m):
    sig = tuple(int(np.sign(np.round(m["parity"][nm][0], 6))) for nm in LITTLE[dname])
    return SECTORS[dname].get(sig, "unclassified")


def identify(dname, rA, rB, nmax=12):
    """match modes of two runs at qA < qB (same direction) sector by sector; gapless <=> omega ratio ~ qB/qA."""
    qa, qb = rA["q"], rB["q"]
    want = qb / qa
    mA, mB = rA["modes"][:nmax], rB["modes"][:nmax]
    secA = [mode_sector(dname, m) for m in mA]
    secB = [mode_sector(dname, m) for m in mB]
    table = []
    for i, m in enumerate(mA):
        cands = [j for j in range(len(mB)) if secB[j] == secA[i]]
        if not cands:
            continue
        j = min(cands, key=lambda jj: abs(mB[jj]["omega"] / m["omega"] - want))
        ratio = mB[j]["omega"] / m["omega"]
        jg = min(cands, key=lambda jj: abs(mB[jj]["omega"] / m["omega"] - 1.0))
        table.append(dict(iA=i, iB=j, sector=secA[i], omegaA=m["omega"], omegaB=mB[j]["omega"], ratio=ratio,
                          gapless=bool(abs(ratio - want) < 0.05 * want),
                          ratio_to_nearest_same_omega=mB[jg]["omega"] / m["omega"]))
    gapless = [t for t in table if t["gapless"]]
    lab = {}
    Lsec = "L_mixed" if dname == "xz45" else "L"
    Lg = sorted([t for t in gapless if t["sector"] == Lsec], key=lambda t: t["omegaA"])
    if dname == "xz45":
        for k, t in enumerate(Lg):
            lab[f"A{k}"] = t
    else:
        if len(Lg) >= 1:
            lab["L2"] = Lg[0]
        if len(Lg) >= 2:
            lab["L1"] = Lg[1]
    for sname in set(SECTORS[dname].values()):
        if sname.startswith("T"):
            Tg = sorted([t for t in gapless if t["sector"] == sname], key=lambda t: t["omegaA"])
            if Tg:
                lab[sname] = Tg[0]
    return lab, table


def mode_summary(r, i):
    m = r["modes"][i]
    q = r["q"]
    return dict(omega=m["omega"], speed=m["omega"] / q, Z=m["Z"], F=m["F"], S=m["S"], rho_rel=m["rho_rel"],
                disp_cos=m["disp_cos"], parity={k: v[0] for k, v in m["parity"].items()})


def direction_block(P, C, dname, qs=(0.15, 0.3), a=A_LAT, c=C_LAT):
    runs = {qq: json.load(open(os.path.join(WORK, bdg_key(P, C, dname, qq, False, a, c) + ".json"))) for qq in qs}
    lab, table = identify(dname, runs[qs[0]], runs[qs[1]])
    out = {}
    for k, qq in enumerate(qs):
        r = runs[qq]
        blk = dict(q=qq, Nb=r["Nb"], chi_static=r["chi_direct"], chi_static_cg=r.get("chi_cg"),
                   c_kappa=r["c_kappa"], sLs_rel_dev=r["sLs_rel_dev"],
                   F_sum_low_modes=float(sum(m["F"] for m in r["modes"])),
                   S_sum_low_modes=float(sum(m["S"] for m in r["modes"])),
                   n_low_modes=len(r["modes"]), modes={})
        for name, t in lab.items():
            idx = t["iA"] if k == 0 else t["iB"]
            ms = mode_summary(r, idx)
            ms["omega_ratio_q03_q015"] = t["ratio"]
            blk["modes"][name] = ms
        if "L2" in blk["modes"] and "L1" in blk["modes"]:
            blk["Z21"] = blk["modes"]["L2"]["Z"] / blk["modes"]["L1"]["Z"]
        blk["low_modes"] = [dict(omega=m["omega"], sector=mode_sector(dname, m), Z=m["Z"], F=m["F"], S=m["S"],
                                 disp_cos=m["disp_cos"]) for m in r["modes"][:10]]
        out[repr(qq) if qq not in (0.15, 0.3) else ("0.15" if qq == 0.15 else "0.3")] = blk
    # LSQ slopes through the origin over both q
    lsq = {}
    for name, t in lab.items():
        w = np.array([t["omegaA"], t["omegaB"]])
        qq = np.array(qs)
        lsq[name] = float(np.sum(w * qq) / np.sum(qq * qq))
    out["lsq_speed_over_q015_q03"] = lsq
    out["identification"] = table
    out["n_gapless"] = int(sum(1 for t in table if t["gapless"]))
    return out


def schema_from(dirs):
    x15 = dirs["x"]["0.15"]["modes"]
    tlist = []
    for d in ("x", "y", "z"):
        for nm, ms in dirs[d]["0.15"]["modes"].items():
            if nm.startswith("T"):
                tlist.append((d, nm, ms["speed"]))
    sch = dict(c2=x15["L2"]["speed"],
               cT_min=min(t[2] for t in tlist), cT_max=max(t[2] for t in tlist),
               c1_basal_q015=x15["L1"]["speed"], F2_basal_q015=x15["L2"]["F"],
               Z21_basal_q015=dirs["x"]["0.15"]["Z21"], S2_basal_q015=x15["L2"]["S"],
               c_kappa=dirs["x"]["0.15"]["c_kappa"])
    return sch, tlist


def assemble():
    lam = json.load(open(os.path.join(WORK, "lambdac.json")))
    res = {}
    res["settings"] = dict(
        units="hbar=m=R=1, mean density 1", kernel="Uhat(k)=4 pi (sin k - k cos k)/k^3",
        a=A_LAT, c=C_LAT, structure="AB (hcp-type) stack",
        bdg_cell="2-site hexagonal primitive cell, origin on the inversion centre, sites at +-(1/6,1/6,1/4)",
        orth_cell="(a, sqrt3 a, c), sites (0,0,0),(1/2,1/2,0),(1/2,1/6,1/2),(0,2/3,1/2)",
        gs_method="preconditioned L-BFGS on the energy (normalisation by rescaling) + Newton-GMRES polish; "
                  "Galerkin plane-wave sphere |G|<Kpsi with alias-free quadrature (grid >= 4h+1); "
                  "independent pseudo-spectral box grids for the orthorhombic cell",
        bdg_method="plane-wave sphere |q+G|<Kcut, real-symmetric L(q), A(q)=L+2X; A=CC^T, K=C^T L C, eigh",
        primary_cut="Kpsi = Kcut = 50 (consistent Galerkin)", prod_cuts=PROD_K, q_values=QS,
        threads="OMP/OPENBLAS/MKL = 2")
    res["Lambda_c"] = lam["Lambda_c"]
    res["Lambda"] = lam["Lambda"]
    res["Lambda_c_details"] = lam
    # ---------------- ground state
    gsb = {}
    for K in GS_PRIM_K:
        p = os.path.join(WORK, gs_key("prim", "sphere", K) + ".json")
        if os.path.exists(p):
            d = json.load(open(p))
            gsb[f"prim_sphere_K{K}"] = {k: d[k] for k in ("e_per_particle", "mu", "mu_alt", "res_max", "res_rel_rms",
                                                          "n_coeffs", "shape", "psi_max", "n_max", "n_min",
                                                          "ekin_per_particle", "eint_per_particle", "V", "Ncell",
                                                          "time", "psihat_tail_max_beyond_K", "norm_check")}
    for K in GS_ORTH_K:
        p = os.path.join(WORK, gs_key("orth", "sphere", K) + ".json")
        if os.path.exists(p):
            d = json.load(open(p))
            gsb[f"orth_sphere_K{K}"] = {k: d[k] for k in ("e_per_particle", "mu", "mu_alt", "res_max", "res_rel_rms",
                                                          "n_coeffs", "shape", "n_max", "n_min", "V", "Ncell", "time",
                                                          "norm_check")}
    for gr in ORTH_BOX:
        p = os.path.join(WORK, gs_key("orth", "box", grid=gr) + ".json")
        if os.path.exists(p):
            d = json.load(open(p))
            gsb[f"orth_box_{gr[0]}x{gr[1]}x{gr[2]}"] = {k: d[k] for k in ("e_per_particle", "mu", "res_max",
                                                                         "res_rel_rms", "shape", "n_max", "n_min",
                                                                         "time")}
    comp = {}
    for K in GS_ORTH_K:
        kp, ko = f"prim_sphere_K{K}", f"orth_sphere_K{K}"
        if kp in gsb and ko in gsb:
            comp[f"K{K}"] = dict(
                e_rel_diff=(gsb[ko]["e_per_particle"] - gsb[kp]["e_per_particle"]) / gsb[kp]["e_per_particle"],
                mu_rel_diff=(gsb[ko]["mu"] - gsb[kp]["mu"]) / gsb[kp]["mu"])
    ref = gsb.get("prim_sphere_K50")
    boxk = [k for k in gsb if k.startswith("orth_box")]
    if ref and boxk:
        lastb = boxk[-1]
        comp["orth_box_finest_vs_prim_sphere_K50"] = dict(
            grid=lastb, e_rel_diff=(gsb[lastb]["e_per_particle"] - ref["e_per_particle"]) / ref["e_per_particle"],
            mu_rel_diff=(gsb[lastb]["mu"] - ref["mu"]) / ref["mu"])
        comp["orth_box_series_e_rel_vs_prim_K50"] = {
            k: (gsb[k]["e_per_particle"] - ref["e_per_particle"]) / ref["e_per_particle"] for k in boxk}
    gs_primary = dict(e_per_particle=ref["e_per_particle"], mu=ref["mu"], cell_volume_prim=ref["V"],
                      N_cell_prim=ref["Ncell"], res_max=ref["res_max"], n_max=ref["n_max"], n_min=ref["n_min"])
    res["ground_state"] = dict(primary_prim_sphere_K50=gs_primary, runs=gsb, cell_agreement=comp)
    # ---------------- BdG directions at the primary cut
    Kp = PROD_K[-1]
    dirs = {d: direction_block(Kp, Kp, d) for d in ("x", "y", "z")}
    res["directions"] = dirs
    sch, tlist = schema_from(dirs)
    res["schema"] = sch
    # ---------------- convergence
    conv = {}
    for K in PROD_K:
        try:
            dk = {d: direction_block(K, K, d) for d in ("x", "y", "z")}
        except FileNotFoundError:
            continue
        sk, tl = schema_from(dk)
        row = dict(sk)
        for d, nm, sp in tl:
            row[f"cT_{d}_{nm}"] = sp
        row["c2_q03"] = dk["x"]["0.3"]["modes"]["L2"]["speed"]
        row["c1_q03"] = dk["x"]["0.3"]["modes"]["L1"]["speed"]
        row["F2_q03"] = dk["x"]["0.3"]["modes"]["L2"]["F"]
        row["c_kappa_q03"] = dk["x"]["0.3"]["c_kappa"]
        row["Nb_x_q015"] = dk["x"]["0.15"]["Nb"]
        conv[f"K{K}"] = row
    keys = list(conv[f"K{Kp}"].keys())
    reld = {}
    for K in PROD_K[:-1]:
        if f"K{K}" in conv:
            reld[f"K{K}_vs_K{Kp}"] = {k: (conv[f"K{K}"][k] - conv[f"K{Kp}"][k]) / conv[f"K{Kp}"][k]
                                     for k in keys if not k.startswith("Nb")}
    maxrel = {}
    for tag, dd in reld.items():
        maxrel[tag] = float(max(abs(v) for v in dd.values()))
    # off-diagonal (ground-state resolution vs BdG cut)
    off = {}
    for (P, C) in ((50, 40), (60, 40), (60, 50), (60, 30), (60, 35), (60, 45), (40, 40), (50, 50)):
        try:
            b = direction_block(P, C, "x")
        except FileNotFoundError:
            continue
        m = b["0.15"]["modes"]
        off[f"P{P}_C{C}"] = dict(c2=m["L2"]["speed"], c1=m["L1"]["speed"], F2=m["L2"]["F"], Z21=b["0.15"]["Z21"],
                                 S2=m["L2"]["S"], cT_Ty=m["Ty"]["speed"], cT_Tz=m["Tz"]["speed"],
                                 c_kappa=b["0.15"]["c_kappa"], F2_q03=b["0.3"]["modes"]["L2"]["F"])
    res["convergence"] = dict(consistent_cuts=conv, rel_diff_vs_primary=reld, max_abs_rel_diff=maxrel,
                              gs_resolution_vs_bdg_cut_x=off,
                              note="primary = consistent Galerkin Kpsi=Kcut=50; rel diffs are (K - 50)/50-values")
    # ---------------- extras
    ex = {}
    for d in ("x", "y", "z"):
        for qq in ("0.15", "0.3"):
            for nm, ms in dirs[d][qq]["modes"].items():
                ex[f"speed_{d}_{nm}_q{qq}"] = ms["speed"]
    x3 = dirs["x"]["0.3"]
    ex.update(c2_q03=x3["modes"]["L2"]["speed"], c1_basal_q03=x3["modes"]["L1"]["speed"],
              F2_basal_q03=x3["modes"]["L2"]["F"], F1_basal_q03=x3["modes"]["L1"]["F"],
              Z21_basal_q03=x3["Z21"], S2_basal_q03=x3["modes"]["L2"]["S"], c_kappa_q03=x3["c_kappa"],
              F1_basal_q015=dirs["x"]["0.15"]["modes"]["L1"]["F"], S1_basal_q015=dirs["x"]["0.15"]["modes"]["L1"]["S"])
    ex["lsq_speeds"] = {d: dirs[d]["lsq_speed_over_q015_q03"] for d in ("x", "y", "z")}
    ts = [t[2] for t in tlist]
    ex["transverse_speeds_q015"] = {f"{d}_{nm}": sp for d, nm, sp in tlist}
    ex["cT_mean_all_dir_pol_q015"] = float(np.mean(ts))
    tl3 = []
    for d in ("x", "y", "z"):
        for nm, ms in dirs[d]["0.3"]["modes"].items():
            if nm.startswith("T"):
                tl3.append(ms["speed"])
    ex["cT_mean_all_dir_pol_q03"] = float(np.mean(tl3))
    tlsq = [v for d in ("x", "y", "z") for nm, v in dirs[d]["lsq_speed_over_q015_q03"].items() if nm.startswith("T")]
    ex["cT_mean_all_dir_pol_lsq"] = float(np.mean(tlsq))
    ex["cT_min_lsq"], ex["cT_max_lsq"] = float(min(tlsq)), float(max(tlsq))
    ex["flag_c2_gt_cT"] = bool(sch["c2"] > sch["cT_min"])
    ex["ratio_c2_over_cTmin"] = sch["c2"] / sch["cT_min"]
    ex["n_gapless_branches"] = {d: dirs[d]["n_gapless"] for d in ("x", "y", "z")}
    # longitudinal pairs along y and z (extra)
    for d in ("y", "z"):
        m = dirs[d]["0.15"]["modes"]
        ex[f"c2_{d}_q015"] = m["L2"]["speed"]
        ex[f"c1_{d}_q015"] = m["L1"]["speed"]
        ex[f"F2_{d}_q015"] = m["L2"]["F"]
        ex[f"S2_{d}_q015"] = m["L2"]["S"]
        ex[f"Z21_{d}_q015"] = dirs[d]["0.15"]["Z21"]
        ex[f"c_kappa_{d}_q015"] = dirs[d]["0.15"]["c_kappa"]
    # sum rules (full spectrum)
    sr = {}
    for (K, qq) in ((40, 0.15), (50, 0.15), (40, 0.3)):
        p = os.path.join(WORK, bdg_key(K, K, "x", qq, True) + ".json")
        if os.path.exists(p):
            r = json.load(open(p))
            sr[f"K{K}_x_q{qq}"] = {k: r.get(k) for k in ("Nb", "fsum_spectral", "fsum_exact", "fsum_rel_residual",
                                                         "static_spectral", "chi_direct", "chi_cg",
                                                         "static_rel_residual_vs_cg", "static_rel_residual_vs_direct",
                                                         "chi_direct_vs_cg_rel", "omega_max", "cg_iter",
                                                         "cg_rel_residual", "t_eigh", "sLs_rel_dev",
                                                         "dense_vs_matrixfree_rel")}
    ex["sum_rules_full_spectrum"] = sr
    if sr:
        ex["max_abs_fsum_rel_residual"] = float(max(abs(v["fsum_rel_residual"]) for v in sr.values()))
        ex["max_abs_static_rel_residual"] = float(max(abs(v["static_rel_residual_vs_cg"]) for v in sr.values()))
    gam = {}
    for K in (40, 50):
        p = os.path.join(WORK, f"gamma_P{K}_C{K}.json")
        if os.path.exists(p):
            gam[f"K{K}"] = json.load(open(p))
    ex["gamma_sector"] = gam
    # small-q behaviour and c_kappa(q -> 0)
    sq = {}
    for d in ("x", "y", "z"):
        rows = []
        for qq in (0.02, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3):
            p = os.path.join(WORK, bdg_key(SMALLQ_K, SMALLQ_K, d, qq, False) + ".json")
            if os.path.exists(p):
                rows.append(json.load(open(p)))
        if len(rows) < 3:
            continue
        r15 = [r for r in rows if r["q"] == 0.15][0]
        r30 = [r for r in rows if r["q"] == 0.3][0]
        lab, _ = identify(d, r15, r30)
        # follow each labelled branch to other q by sector + displacement/omega continuity
        br = {}
        for name, t in lab.items():
            sec = t["sector"]
            c0 = t["omegaA"] / 0.15
            pts = []
            for r in rows:
                cands = [m for m in r["modes"][:12] if mode_sector(d, m) == sec]
                mm = min(cands, key=lambda m: abs(m["omega"] / r["q"] - c0))
                pts.append([r["q"], mm["omega"] / r["q"], mm["F"], mm["S"]])
            br[name] = pts
        qv = np.array([r["q"] for r in rows])
        ck2 = np.array([r["V"] / r["chi_direct"] for r in rows])
        A = np.vstack([np.ones_like(qv), qv ** 2, qv ** 4]).T
        coef = np.linalg.lstsq(A, ck2, rcond=None)[0]
        i15, i30 = list(qv).index(0.15), list(qv).index(0.3)
        rich = (ck2[i15] * 0.3 ** 2 - ck2[i30] * 0.15 ** 2) / (0.3 ** 2 - 0.15 ** 2)
        sq[d] = dict(K=SMALLQ_K, q=qv.tolist(), c_kappa=np.sqrt(ck2).tolist(), branches_q_speed_F_S=br,
                     c_kappa_q0_fit_q2q4=float(np.sqrt(coef[0])), c_kappa_q0_two_point_q015_q03=float(np.sqrt(rich)))
    ex["small_q"] = sq
    if "x" in sq:
        ex["c_kappa_q0_extrapolated"] = sq["x"]["c_kappa_q0_fit_q2q4"]
        ex["c_kappa_q0_two_point"] = sq["x"]["c_kappa_q0_two_point_q015_q03"]
    fsl = {}
    for K in (40, 50):
        p = os.path.join(WORK, f"fs_lr_P{K}_C{K}.json")
        if os.path.exists(p):
            fsl[f"K{K}"] = json.load(open(p))
    if fsl:
        ex["superfluid_fraction_linear_response"] = fsl
    p = os.path.join(WORK, "init_independence_K30.json")
    if os.path.exists(p):
        ex["gs_initial_width_independence_K30"] = json.load(open(p))
    # oblique direction, optimum (filled if available)
    p = os.path.join(WORK, "extra_xz45.json")
    if os.path.exists(p):
        ex["oblique_xz45"] = json.load(open(p))
    p = os.path.join(WORK, "extra_optimum.json")
    if os.path.exists(p):
        ex["own_optimum"] = json.load(open(p))
    # timings (wall seconds, 2 BLAS/FFT threads)
    tim = {}
    for K in PROD_K:
        for d in ("x", "y", "z"):
            for qq in QS:
                p = os.path.join(WORK, bdg_key(K, K, d, qq, False) + ".json")
                if os.path.exists(p):
                    r = json.load(open(p))
                    tim[f"bdg_K{K}_{d}_q{qq}"] = dict(Nb=r["Nb"], Npp=r["Npp"], t_build=r["t_build"],
                                                    t_eigh_low=r["t_eigh"], t_total=r["t_total"])
    for (K, qq) in ((40, 0.15), (50, 0.15), (40, 0.3)):
        p = os.path.join(WORK, bdg_key(K, K, "x", qq, True) + ".json")
        if os.path.exists(p):
            r = json.load(open(p))
            tim[f"bdg_full_K{K}_x_q{qq}"] = dict(Nb=r["Nb"], t_eigh_full=r["t_eigh"], t_total=r["t_total"])
    for k, v in res["ground_state"]["runs"].items():
        tim[f"gs_{k}"] = v.get("time")
    res["settings"]["timings_s"] = tim
    res["settings"]["memory_note"] = ("largest dense BdG matrices Nb ~ 7.9e3 (K=50): ~0.5 GB each; observed RSS "
                                      "about 1.2 GB while building L, X; full-spectrum K=50 run estimated below 3 GB")
    res["extras"] = ex
    out = os.path.join(OUTDIR, "qb_results.json")
    json.dump(res, open(out, "w"), indent=1)
    print("schema:", json.dumps(sch, indent=1))
    return res


# ----------------------------------------------------------------------------------------------
# production pipeline (every step cached in WORK; re-running skips finished steps)
# ----------------------------------------------------------------------------------------------
PROD_K = [30, 35, 40, 45, 50]          # consistent Galerkin cuts Kpsi = Kcut
GS_PRIM_K = [20, 30, 35, 40, 45, 50, 60]
GS_ORTH_K = [30, 40, 50]
ORTH_BOX = [(15, 25, 23), (19, 33, 29), (23, 41, 37), (27, 47, 43), (31, 55, 49), (35, 61, 57)]
QS = [0.15, 0.3]
SMALLQ_K = 40                          # cut used for the extra small-q scan (q->0 limits)


def gs_cached(cell, disc, kpsi=None, grid=None, seed=None, log=print, a=A_LAT, c=C_LAT):
    key = gs_key(cell, disc, kpsi, grid, a, c)
    p = os.path.join(WORK, key + ".json")
    if os.path.exists(p):
        return json.load(open(p))
    log(f"[gs] {key}")
    return solve_gs(cell, disc, kpsi, grid, seed_from=seed, log=log, a=a, c=c)


def quad_fit_min(pts, a0, c0):
    """fit e = p0 + p1 x + p2 y + p3 x^2 + p4 x y + p5 y^2 (x = a/a0-1, y = c/c0-1); return minimiser."""
    P = np.array(pts)
    x, y, e = P[:, 0] / a0 - 1, P[:, 1] / c0 - 1, P[:, 2]
    Mx = np.vstack([np.ones_like(x), x, y, x * x, x * y, y * y]).T
    p, *_ = np.linalg.lstsq(Mx, e, rcond=None)
    H = np.array([[2 * p[3], p[4]], [p[4], 2 * p[5]]])
    gvec = np.array([p[1], p[2]])
    d = -np.linalg.solve(H, gvec)
    fit_res = float(np.max(np.abs(Mx @ p - e)))
    return a0 * (1 + d[0]), c0 * (1 + d[1]), p, H, fit_res


def optimum_search(K=40, Kb=45, log=print):
    """own (a, c) optimum of the energy per particle at mean density 1 (EXTRA only)."""
    path = os.path.join(WORK, "extra_optimum.json")
    if os.path.exists(path):
        return json.load(open(path))
    seed = gs_key("prim", "sphere", K)
    a0, c0 = A_LAT, C_LAT
    stages = []
    for h in (0.01, 0.003, 0.001):
        pts = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                a, c = a0 * (1 + i * h), c0 * (1 + j * h)
                r = gs_cached("prim", "sphere", K, seed=seed, a=a, c=c, log=log)
                pts.append((a, c, r["e_per_particle"], r["mu"]))
        an, cn, p, H, fr = quad_fit_min(pts, a0, c0)
        stages.append(dict(step=h, centre=[a0, c0], points=pts, fit_coeffs=p.tolist(), hessian_xy=H.tolist(),
                           fit_max_residual=fr, predicted_min=[an, cn]))
        log(f"[opt] step {h}: predicted a={an!r} c={cn!r}")
        a0, c0 = an, cn
    r = gs_cached("prim", "sphere", K, seed=seed, a=a0, c=c0, log=log)
    rb = gs_cached("prim", "sphere", Kb, seed=gs_key("prim", "sphere", K, a=a0, c=c0), a=a0, c=c0, log=log)
    ref = json.load(open(os.path.join(WORK, gs_key("prim", "sphere", Kb) + ".json")))
    out = dict(K_gs_search=K, a_opt=a0, c_opt=c0, c_over_a_opt=c0 / a0, e_opt_K=r["e_per_particle"], mu_opt_K=r["mu"],
               e_opt_Kb=rb["e_per_particle"], mu_opt_Kb=rb["mu"], Kb=Kb,
               e_given_point_Kb=ref["e_per_particle"], mu_given_point_Kb=ref["mu"],
               e_gain_rel=(rb["e_per_particle"] - ref["e_per_particle"]) / ref["e_per_particle"],
               a_rel_shift=a0 / A_LAT - 1, c_rel_shift=c0 / C_LAT - 1, stages=stages)
    # BdG at the optimum (consistent cut Kb)
    dirs = {}
    for d in ("x", "y", "z"):
        for qq in QS:
            run_bdg(Kb, Kb, d, qq, nlow=16, log=log, a=a0, c=c0)
        dirs[d] = direction_block(Kb, Kb, d, a=a0, c=c0)
    sch, tl = schema_from(dirs)
    out["schema_at_optimum"] = sch
    out["transverse_speeds_q015_at_optimum"] = {f"{d}_{nm}": sp for d, nm, sp in tl}
    out["F2_basal_q03_at_optimum"] = dirs["x"]["0.3"]["modes"]["L2"]["F"]
    out["directions_at_optimum"] = {d: {qq: {k: v for k, v in dirs[d][qq].items() if k != "low_modes"}
                                        for qq in ("0.15", "0.3")} for d in dirs}
    json.dump(out, open(path, "w"), indent=1)
    return out


def oblique_extra(K=50, log=print):
    path = os.path.join(WORK, "extra_xz45.json")
    if os.path.exists(path):
        return json.load(open(path))
    rr = [run_bdg(K, K, "xz45", qq, nlow=16, log=log) for qq in QS]
    lab, table = identify("xz45", rr[0], rr[1])
    out = dict(K=K, direction="45 deg in the x-z plane", identification=table)
    for k, qq in enumerate(QS):
        blk = dict(c_kappa=rr[k]["c_kappa"], modes={})
        for nm, t in lab.items():
            blk["modes"][nm] = mode_summary(rr[k], t["iA"] if k == 0 else t["iB"])
        out[repr(qq)] = blk
    json.dump(out, open(path, "w"), indent=1)
    return out


def pipeline(stage="all", log=print):
    T = time.time()
    if stage in ("all", "gs"):
        prev = None
        for K in GS_PRIM_K:
            gs_cached("prim", "sphere", K, seed=prev, log=log)
            prev = gs_key("prim", "sphere", K)
        prev = None
        for K in GS_ORTH_K:
            gs_cached("orth", "sphere", K, seed=prev, log=log)
            prev = gs_key("orth", "sphere", K)
        prev = None
        for gr in ORTH_BOX:
            gs_cached("orth", "box", grid=gr, seed=prev, log=log)
            prev = gs_key("orth", "box", grid=gr)
        log(f"[gs done] {time.time() - T:.0f}s")
    if stage in ("all", "bdg"):
        for K in PROD_K:
            for d in ("x", "y", "z"):
                for qq in QS:
                    t0 = time.time()
                    run_bdg(K, K, d, qq, nlow=16, log=log)
                    log(f"[bdg] K={K} {d} q={qq} {time.time() - t0:.0f}s")
        log(f"[bdg done] {time.time() - T:.0f}s")
    if stage in ("all", "full"):
        for K in (40, 50):
            t0 = time.time()
            run_bdg(K, K, "x", 0.15, nlow=16, full=True, log=log)
            log(f"[full] K={K} {time.time() - t0:.0f}s")
        run_bdg(40, 40, "x", 0.3, nlow=16, full=True, log=log)
        for K in (40, 50):
            gamma_check(K, K, log=log)
        log(f"[full/gamma done] {time.time() - T:.0f}s")
    if stage in ("all", "offdiag"):
        # ground-state resolution at fixed BdG cut, and BdG cut at fixed ground state
        for (P, C) in ((50, 40), (60, 40), (60, 50), (60, 30), (60, 35), (60, 45)):
            for qq in QS:
                run_bdg(P, C, "x", qq, nlow=16, log=log)
        log(f"[offdiag done] {time.time() - T:.0f}s")
    if stage in ("all", "smallq"):
        for d in ("x", "y", "z"):
            for qq in (0.02, 0.05, 0.075, 0.1, 0.2):
                run_bdg(SMALLQ_K, SMALLQ_K, d, qq, nlow=16, log=log)
        log(f"[smallq done] {time.time() - T:.0f}s")
    if stage in ("all", "extras", "fs"):
        for K in (40, 50):
            superfluid_fraction_lr(K, log=log)
        log(f"[fs done] {time.time() - T:.0f}s")
    if stage in ("all", "extras"):
        oblique_extra(log=log)
        log(f"[xz45 done] {time.time() - T:.0f}s")
        optimum_search(log=log)
        log(f"[optimum done] {time.time() - T:.0f}s")


# ----------------------------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["lambdac", "gs", "bdg", "gamma", "assemble", "pipeline"])
    ap.add_argument("--stage", default="all")
    ap.add_argument("--cell", default="prim")
    ap.add_argument("--disc", default="sphere")
    ap.add_argument("--kpsi", type=float, default=None)
    ap.add_argument("--kcut", type=float, default=None)
    ap.add_argument("--grid", type=int, nargs=3, default=None)
    ap.add_argument("--seed", default=None)
    ap.add_argument("--mfac", type=int, default=4)
    ap.add_argument("--dir", default="x")
    ap.add_argument("--q", type=float, nargs="+", default=[0.15])
    ap.add_argument("--nlow", type=int, default=30)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--nocg", action="store_true")
    a = ap.parse_args()
    if a.cmd == "lambdac":
        r = lambda_c()
        json.dump(r, open(os.path.join(WORK, "lambdac.json"), "w"), indent=1)
        print(json.dumps(r, indent=1))
    elif a.cmd == "gs":
        r = solve_gs(a.cell, a.disc, a.kpsi, a.grid, mfac=a.mfac, seed_from=a.seed)
        print(json.dumps({k: v for k, v in r.items() if k != "newton"}, indent=1))
    elif a.cmd == "gamma":
        print(json.dumps(gamma_check(a.kpsi, a.kcut), indent=1))
    elif a.cmd == "bdg":
        for qq in a.q:
            r = run_bdg(a.kpsi, a.kcut, a.dir, qq, nlow=a.nlow, full=a.full, do_cg=not a.nocg)
            print(json.dumps({k: v for k, v in r.items() if k != "modes"}, indent=1))
            for m in r["modes"][:16]:
                print(f"  w={m['omega']:.10f} Z={m['Z']:.3e} F={m['F']:.6f} S={m['S']:.6f} "
                      f"par={ {k: round(v[0], 6) for k, v in m['parity'].items()} } "
                      f"disp={[round(x, 4) for x in m['disp_cos']]}")
    elif a.cmd == "assemble":
        assemble()
    elif a.cmd == "pipeline":
        def _log(m):
            print(time.strftime("%H:%M:%S"), m, flush=True)
        pipeline(a.stage, log=_log)
