"""
gz1_core.py — Gate G-zeta1 shared kernels (REBUILD)
====================================================
Reconstruction of the lost GZ1 instrument core, rebuilt from the surviving
GZ1_EXECUTION_PREREGISTRATION.md + GZ1_GATE_EXECUTION_REPORT.md (originals lost
to a sandbox reset; original gz1_core.py md5 13d01cf8). Self-contained:
numpy/scipy only; imports NO framework tool.

Model (binding, prereg): hbar = m = 1, 2-D.
    E[psi] = int 1/2|grad psi|^2 + 1/2 iint rho(x)U(x-x')rho(x') - mu int rho
Soft-core U(r) = g*theta(R-r), g=22.0, R=1.0, rho0=1.0.
Continuum Fourier kernel  Utilde(q) = 2*pi*g*R^2 * J1(qR)/(qR),  Utilde(0)=g*pi*R^2.

BdG (binding, prereg): omega^2 f = L(L+2X) f,  L = -1/2 grad^2 + (U*rho0) - mu
(PSD; psi0 its ground state), X f = psi0 * U*(psi0 f). Hermitian form
L^{1/2} (L+2X) L^{1/2}.

NOTE: the comparison target constant appears in NO function here (Eddington
isolation — comparison_step.py only).
"""

import numpy as np
from scipy.special import j1

G_COUPLING = 22.0
R_CORE = 1.0
RHO0 = 1.0


# ---------------------------------------------------------------- kernels ----
def U_tilde(q):
    """Continuum soft-core kernel FT: 2*pi*g*R^2 J1(qR)/(qR); U(0)=g*pi*R^2."""
    q = np.asarray(q, float)
    out = np.full(q.shape, G_COUPLING * np.pi * R_CORE**2)
    nz = q > 1e-12
    x = q[nz] * R_CORE
    out[nz] = 2.0 * np.pi * G_COUPLING * R_CORE**2 * j1(x) / x
    return out


def U_disk_fft(N, L):
    """Grid-FFT kernel of the real-space disk (the V4.26 mv_g1 discretisation),
    used ONLY for the phase-1 canonical-object replication cross-check."""
    dx = L / N
    x = (np.arange(N) - N // 2) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    Ur = np.where(np.sqrt(X**2 + Y**2) < R_CORE, G_COUPLING, 0.0)
    return np.fft.fft2(np.fft.ifftshift(Ur)).real * dx**2


# ----------------------------------------------------- square / rect grids ----
def rect_grids(Nx, Ny, Lx, Ly):
    dx, dy = Lx / Nx, Ly / Ny
    x = np.arange(Nx) * dx
    y = np.arange(Ny) * dy
    X, Y = np.meshgrid(x, y, indexing="ij")
    kx = 2 * np.pi * np.fft.fftfreq(Nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(Ny, d=dy)
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    return X, Y, KX, KY, KX**2 + KY**2, dx, dy


def relax_rect(psi, K2, Uk, dtau, steps, tol=1e-12, report_every=200):
    """Imaginary-time split-step GP relaxation at fixed mean density rho0.
    Uk = kernel array on the same k-grid. Returns (psi, mu, residual)."""
    N2 = psi.size
    norm_target = RHO0 * N2

    def renorm(p):
        return p * np.sqrt(norm_target / np.sum(np.abs(p) ** 2))

    psi = renorm(psi)
    Kprop = np.exp(-0.25 * K2 * dtau)
    e_prev = None
    for it in range(steps):
        psi = np.fft.ifft2(Kprop * np.fft.fft2(psi))
        rho = np.abs(psi) ** 2
        Uconv = np.fft.ifft2(Uk * np.fft.fft2(rho)).real
        psi = psi * np.exp(-Uconv * dtau)
        psi = np.fft.ifft2(Kprop * np.fft.fft2(psi))
        psi = renorm(psi)
        if it % report_every == 0 or it == steps - 1:
            mu, res = mu_residual_rect(psi, K2, Uk)
            if e_prev is not None and abs(mu - e_prev) < tol * max(1.0, abs(mu)):
                break
            e_prev = mu
    psi = np.real(psi)            # ground state is real up to phase
    psi = renorm(psi)
    mu, res = mu_residual_rect(psi, K2, Uk)
    return psi, mu, res


def mu_residual_rect(psi, K2, Uk):
    """mu = <psi|H|psi>/<psi|psi>; residual = ||H psi - mu psi|| / (mu ||psi||)."""
    rho = np.abs(psi) ** 2
    Uconv = np.fft.ifft2(Uk * np.fft.fft2(rho)).real
    Hpsi = np.fft.ifft2(0.5 * K2 * np.fft.fft2(psi)) + Uconv * psi
    mu = float(np.real(np.vdot(psi, Hpsi) / np.vdot(psi, psi)))
    res = float(np.linalg.norm(Hpsi - mu * psi) / (abs(mu) * np.linalg.norm(psi)))
    return mu, res


# ------------------------------------------------ peak / order diagnostics ----
def local_maxima(rho, thresh):
    m = np.ones_like(rho, dtype=bool)
    for sx in (-1, 0, 1):
        for sy in (-1, 0, 1):
            if sx == 0 and sy == 0:
                continue
            m &= rho >= np.roll(np.roll(rho, sx, axis=0), sy, axis=1)
    m &= rho > thresh
    return np.argwhere(m)


def bond_orientational(rho, dx, L, knn=6):
    """Local psi6/psi4 over detected peaks, minimum-image (replicates the V4.26
    estimator: peaks above mean+0.5*std, 6 nearest neighbours)."""
    mean, std = rho.mean(), rho.std()
    peaks = local_maxima(rho, mean + 0.5 * std)
    if len(peaks) < 7:
        return dict(psi4_local=0.0, psi6_local=0.0, n_peaks=int(len(peaks)))
    P = peaks.astype(float) * dx
    n = len(P)
    p4 = np.zeros(n, complex)
    p6 = np.zeros(n, complex)
    for i in range(n):
        d = P - P[i]
        d -= L * np.round(d / L)
        dist = np.hypot(d[:, 0], d[:, 1])
        nb = np.argsort(dist)[1:knn + 1]
        ang = np.arctan2(d[nb, 1], d[nb, 0])
        p4[i] = np.mean(np.exp(4j * ang))
        p6[i] = np.mean(np.exp(6j * ang))
    return dict(psi4_local=float(np.mean(np.abs(p4))),
                psi6_local=float(np.mean(np.abs(p6))), n_peaks=n)


def structure_kc(rho, KX, KY):
    S = np.abs(np.fft.fft2(rho - rho.mean())) ** 2
    S.flat[0] = 0.0
    kmag = np.sqrt(KX**2 + KY**2)
    return float(kmag.flat[np.argmax(S)])


# --------------------------------------------------------- oblique cell -------
class Cell:
    """Oblique triangular primitive cell: a1=(a,0), a2=(a/2, sqrt3 a/2),
    n x n fractional grid. FFT index (m1,m2) -> G = m1 b1 + m2 b2."""

    def __init__(self, a, n):
        self.a, self.n = float(a), int(n)
        s3 = np.sqrt(3.0)
        self.a1 = np.array([a, 0.0])
        self.a2 = np.array([a / 2.0, s3 * a / 2.0])
        self.area = a * a * s3 / 2.0
        self.b1 = 2 * np.pi * np.array([1.0 / a, -1.0 / (s3 * a)])
        self.b2 = 2 * np.pi * np.array([0.0, 2.0 / (s3 * a)])
        m = np.fft.fftfreq(n, d=1.0 / n)          # integers 0..n/2-1, -n/2..-1
        M1, M2 = np.meshgrid(m, m, indexing="ij")
        self.M1, self.M2 = M1.astype(int), M2.astype(int)
        self.Gx = M1 * self.b1[0] + M2 * self.b2[0]
        self.Gy = M1 * self.b1[1] + M2 * self.b2[1]
        self.G2 = self.Gx**2 + self.Gy**2
        self.Uk = U_tilde(np.sqrt(self.G2))
        # real-space points
        f = np.arange(n) / n
        F1, F2 = np.meshgrid(f, f, indexing="ij")
        self.X = F1 * self.a1[0] + F2 * self.a2[0]
        self.Y = F1 * self.a1[1] + F2 * self.a2[1]

    def relax(self, steps=3000, dtau=2e-3, sigma_seed=None, noise=0.0, seed=0,
              psi_init=None, tol=1e-13):
        n = self.n
        if psi_init is not None:
            psi = psi_init.astype(complex).copy()
        else:
            if sigma_seed is None:
                sigma_seed = 0.35 * self.a
            dxv = self.X - self.a1[0] / 2 - self.a2[0] / 2
            dyv = self.Y - self.a2[1] / 2
            psi = np.exp(-(dxv**2 + dyv**2) / (2 * sigma_seed**2)).astype(complex)
            if noise:
                rng = np.random.default_rng(seed)
                psi += noise * rng.standard_normal((n, n))
        norm_target = RHO0 * n * n

        def renorm(p):
            return p * np.sqrt(norm_target / np.sum(np.abs(p) ** 2))

        psi = renorm(psi)
        Kprop = np.exp(-0.25 * self.G2 * dtau)
        mu_prev = None
        for it in range(steps):
            psi = np.fft.ifft2(Kprop * np.fft.fft2(psi))
            rho = np.abs(psi) ** 2
            Uc = np.fft.ifft2(self.Uk * np.fft.fft2(rho)).real
            psi = psi * np.exp(-Uc * dtau)
            psi = np.fft.ifft2(Kprop * np.fft.fft2(psi))
            psi = renorm(psi)
            if it % 100 == 0 or it == steps - 1:
                mu, _ = self.mu_residual(psi.real)
                if mu_prev is not None and abs(mu - mu_prev) < tol * abs(mu):
                    break
                mu_prev = mu
        psi = renorm(np.real(psi))
        mu, res = self.mu_residual(psi)
        return psi, mu, res

    def mu_residual(self, psi):
        rho = np.abs(psi) ** 2
        Uc = np.fft.ifft2(self.Uk * np.fft.fft2(rho)).real
        Hpsi = np.fft.ifft2(0.5 * self.G2 * np.fft.fft2(psi)).real + Uc * psi
        mu = float(np.sum(psi * Hpsi) / np.sum(psi * psi))
        res = float(np.linalg.norm(Hpsi - mu * psi)
                    / (abs(mu) * np.linalg.norm(psi)))
        return mu, res

    def energy_density(self, psi):
        """(kinetic + interaction) per unit area at fixed mean density rho0=1
        (the canonical scan objective; the -mu*rho term is constant over the scan)."""
        n = self.n
        ps = np.fft.fft2(psi) / n**2
        kin = 0.5 * np.sum(self.G2 * np.abs(ps) ** 2)
        rh = np.fft.fft2(np.abs(psi) ** 2) / n**2
        inter = 0.5 * np.sum(self.Uk * np.abs(rh) ** 2)
        return float(kin + inter)        # already per-area (intensive coefficients)


# ------------------------------------------------------------- BdG (cell) -----
class BdG:
    """Plane-wave Bogoliubov-de Gennes on the crystallised cell.
    Basis: n_b x n_b plane waves G(m1,m2); psi0 Fourier coefficients are taken
    from the supplied real-space psi0 grid (its own n x n FFT; coefficient
    differences outside the available range are 0 — logged truncation)."""

    def __init__(self, cell, psi0, mu, n_b):
        self.cell, self.mu, self.n_b = cell, float(mu), int(n_b)
        n = cell.n
        coef = np.fft.fft2(psi0) / n**2                     # psi0_hat(m1,m2)
        rcoef = np.fft.fft2(np.abs(psi0) ** 2) / n**2       # rho0_hat
        Vcoef = cell.Uk * rcoef                             # (U*rho0)_hat
        m = np.fft.fftfreq(n_b, d=1.0 / n_b).astype(int)
        M1, M2 = np.meshgrid(m, m, indexing="ij")
        self.m1 = M1.ravel()
        self.m2 = M2.ravel()
        nb2 = n_b * n_b

        def coef_lookup(C, d1, d2):
            """C[(d1 mod n, d2 mod n)] if |d1|,|d2| < n/2 else 0 (anti-alias)."""
            out = np.zeros(d1.shape, complex)
            ok = (np.abs(d1) < n // 2) & (np.abs(d2) < n // 2)
            out[ok] = C[d1[ok] % n, d2[ok] % n]
            return out

        D1 = self.m1[:, None] - self.m1[None, :]
        D2 = self.m2[:, None] - self.m2[None, :]
        self.P = coef_lookup(coef, D1, D2)                  # psi0 Toeplitz block
        self.Vmat = coef_lookup(Vcoef, D1, D2)              # Hartree Toeplitz
        self.P = 0.5 * (self.P + self.P.conj().T)           # Hermitise (psi0 real)
        self.Vmat = 0.5 * (self.Vmat + self.Vmat.conj().T)
        self.nb2 = nb2

    def omegas(self, k, nbands=24):
        """BdG frequencies at Bloch vector k (lowest nbands)."""
        c = self.cell
        kgx = k[0] + self.m1 * c.b1[0] + self.m2 * c.b2[0]
        kgy = k[1] + self.m1 * c.b1[1] + self.m2 * c.b2[1]
        kin = 0.5 * (kgx**2 + kgy**2)
        Lmat = np.diag(kin - self.mu) + self.Vmat
        Lmat = 0.5 * (Lmat + Lmat.conj().T)
        D = U_tilde(np.sqrt(kgx**2 + kgy**2))
        Xmat = self.P @ (D[:, None] * self.P)
        Xmat = 0.5 * (Xmat + Xmat.conj().T)
        lam, U = np.linalg.eigh(Lmat)
        lam = np.clip(lam, 0.0, None)
        Lh = (U * np.sqrt(lam)) @ U.conj().T
        M = Lh @ (Lmat + 2.0 * Xmat) @ Lh
        M = 0.5 * (M + M.conj().T)
        w2 = np.linalg.eigvalsh(M)
        w = np.sqrt(np.clip(w2, 0.0, None))
        return np.sort(w)[:nbands]

    def L_gamma_check(self, psi0_cellgrid):
        """Sanity (a): min eig of L(Gamma) and overlap of its eigvec with psi0."""
        c = self.cell
        kgx = self.m1 * c.b1[0] + self.m2 * c.b2[0]
        kgy = self.m1 * c.b1[1] + self.m2 * c.b2[1]
        Lmat = np.diag(0.5 * (kgx**2 + kgy**2) - self.mu) + self.Vmat
        Lmat = 0.5 * (Lmat + Lmat.conj().T)
        lam, U = np.linalg.eigh(Lmat)
        # psi0 in the plane-wave basis
        n = c.n
        coef = np.fft.fft2(psi0_cellgrid) / n**2
        vec = np.zeros(self.nb2, complex)
        ok = (np.abs(self.m1) < n // 2) & (np.abs(self.m2) < n // 2)
        vec[ok] = coef[self.m1[ok] % n, self.m2[ok] % n]
        vec /= np.linalg.norm(vec)
        ov = float(np.abs(np.vdot(U[:, 0], vec)))
        return float(lam[0]), ov


# ------------------------------------------------------------ gap coverage ----
def gaps_from_bands(band_arrays, wmax=36.0, min_width=0.15):
    """Stop bands = intervals of omega not covered by any (continuous, sorted)
    band's [min,max] range, below wmax."""
    ivs = []
    nb = min(len(b) for b in band_arrays)
    B = np.array([b[:nb] for b in band_arrays])            # (nk, nb)
    for j in range(nb):
        ivs.append((float(B[:, j].min()), float(B[:, j].max())))
    ivs.sort()
    gaps = []
    cover_hi = ivs[0][1]
    for lo, hi in ivs[1:]:
        if lo > cover_hi + 1e-9:
            if lo - cover_hi >= min_width and cover_hi < wmax:
                gaps.append((cover_hi, lo))
            cover_hi = hi
        else:
            cover_hi = max(cover_hi, hi)
    return gaps


# ----------------------------------------------------------- strip response ----
class Strip:
    """16-row strip: Lx = a, Ly = 16*d (8 rectangular cells), periodic both
    directions. Rows at y_j = j*d with alternating x-offset 0, a/2."""

    def __init__(self, a, Nx=32, Ny=512, nrows=16):
        self.a = float(a)
        self.d = np.sqrt(3.0) * a / 2.0
        self.nrows = nrows
        self.Lx, self.Ly = a, nrows * self.d
        (self.X, self.Y, self.KX, self.KY, self.K2,
         self.dx, self.dy) = rect_grids(Nx, Ny, self.Lx, self.Ly)
        self.Uk = U_tilde(np.sqrt(self.K2))
        self.Nx, self.Ny = Nx, Ny

    def seed(self, sigma=None):
        if sigma is None:
            sigma = 0.35 * self.a
        psi = np.zeros((self.Nx, self.Ny))
        for j in range(self.nrows):
            x0 = (j % 2) * self.a / 2.0
            y0 = j * self.d
            dxv = self.X - x0
            dxv -= self.Lx * np.round(dxv / self.Lx)
            dyv = self.Y - y0
            dyv -= self.Ly * np.round(dyv / self.Ly)
            psi += np.exp(-(dxv**2 + dyv**2) / (2 * sigma**2))
        return psi.astype(complex)

    def relax(self, steps=6000, dtau=2e-3):
        psi, mu, res = relax_rect(self.seed(), self.K2, self.Uk, dtau, steps)
        self.psi0, self.mu = psi, mu
        rho = psi**2
        self.V = np.fft.ifft2(self.Uk * np.fft.fft2(rho)).real
        return psi, mu, res

    # -- driven response: (L+X-w-i eta)u + Xv = -S ; Xu + (L+X+w+i eta)v = 0 --
    def _Lop(self, f):
        return (np.fft.ifft2(0.5 * self.K2 * np.fft.fft2(f))
                + (self.V - self.mu) * f)

    def _Xop(self, f):
        return self.psi0 * np.fft.ifft2(self.Uk * np.fft.fft2(self.psi0 * f))

    def solve_response(self, omega, eta, source, rtol=3e-4, maxiter=250,
                       restart=200):
        from scipy.sparse.linalg import LinearOperator, gmres
        Nx, Ny = self.Nx, self.Ny
        sz = Nx * Ny

        def matvec(z):
            u = z[:sz].reshape(Nx, Ny)
            v = z[sz:].reshape(Nx, Ny)
            Lu, Lv = self._Lop(u), self._Lop(v)
            Xu, Xv = self._Xop(u), self._Xop(v)
            r1 = Lu + Xu - (omega + 1j * eta) * u + Xv
            r2 = Xu + Lv + Xv + (omega + 1j * eta) * v
            return np.concatenate([r1.ravel(), r2.ravel()])

        A = LinearOperator((2 * sz, 2 * sz), matvec=matvec, dtype=complex)
        b = np.concatenate([(-source).ravel(),
                            np.zeros(sz, complex)])
        z, info = gmres(A, b, rtol=rtol, restart=restart, maxiter=maxiter)
        resid = float(np.linalg.norm(matvec(z) - b) / np.linalg.norm(b))
        u = z[:sz].reshape(Nx, Ny)
        v = z[sz:].reshape(Nx, Ny)
        drho = self.psi0 * (u + v)
        return drho, resid

    def gaussian_source(self, sigma=0.5, row=0):
        """Isotropic Gaussian density source masked by psi0, centred on the
        row-`row` lattice site."""
        x0 = (row % 2) * self.a / 2.0
        y0 = row * self.d
        dxv = self.X - x0
        dxv -= self.Lx * np.round(dxv / self.Lx)
        dyv = self.Y - y0
        dyv -= self.Ly * np.round(dyv / self.Ly)
        return self.psi0 * np.exp(-(dxv**2 + dyv**2) / (2 * sigma**2))

    def row_envelope(self, drho):
        """Per-row envelope: max |drho| over each row window |y-y_j| <= d/2
        (wrap-aware)."""
        amp = np.zeros(self.nrows)
        for jj in range(self.nrows):
            y0 = jj * self.d
            dyv = self.Y - y0
            dyv -= self.Ly * np.round(dyv / self.Ly)
            mask = np.abs(dyv) <= self.d / 2.0
            amp[jj] = float(np.abs(drho[mask]).max())
        return amp


# ---------------------------------------------------------------- fitting ----
def envelope_fit(amp, d_row):
    """Decode of the original phase4_fits.json conventions:
      rows_rel        = amp / amp[0], reported rows 0..12
      wrap_min_row    = argmin over rows 1..nrows-1
      clean_ratios    = amp[i+1]/amp[i] for i = 1 .. max(wrap_min_row-2, 2)
      t_ratio_median  = median(clean_ratios); spread = population std
      kappa_fit       = -slope of ln(amp) vs y over rows 1..max(wrap_min_row-1, 6)
      t_fit           = exp(-kappa*d_row); fit_r2 = linear-fit r^2."""
    nrows = len(amp)
    rel = amp / amp[0]
    wmr = int(np.argmin(rel[1:nrows]) + 1)
    imax = max(wmr - 2, 2)
    ratios = [float(rel[i + 1] / rel[i]) for i in range(1, imax + 1)]
    med = float(np.median(ratios))
    spread = float(np.std(ratios))
    fit_hi = max(wmr - 1, 6)
    rows = np.arange(1, fit_hi + 1)
    yy = rows * d_row
    ln = np.log(rel[rows])
    A = np.vstack([yy, np.ones_like(yy)]).T
    coef, *_ = np.linalg.lstsq(A, ln, rcond=None)
    pred = A @ coef
    ss_res = float(np.sum((ln - pred) ** 2))
    ss_tot = float(np.sum((ln - ln.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    kappa = float(-coef[0])
    return dict(rows_rel=[round(float(v), 4) for v in rel[:13]],
                wrap_min_row=wmr,
                clean_ratios=[round(r, 4) for r in ratios],
                t_ratio_median=round(med, 4),
                t_ratio_spread=round(spread, 4),
                kappa_fit=round(kappa, 4),
                t_fit=round(float(np.exp(-kappa * d_row)), 4),
                fit_r2=round(r2, 5))
