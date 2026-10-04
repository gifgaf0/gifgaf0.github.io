#!/usr/bin/env python3
"""xcheck3d.py -- independent 3D cross-check (second leg), written from scratch.

Model (units hbar = m = R = 1, mean density 1):
  e = <(1/2)|grad psi|^2> + (Lam/2) <n (U*n)>,  n = |psi|^2,
  U^(k) = 4 pi [sin k - k cos k] / k^3,  Lam = 2 Lam_c,  Lam_c = min_{U^<0} -k^2/(4 U^(k)).
Crystal: AB (hcp-type) stack, ORTHORHOMBIC 4-site cell (a, sqrt(3) a, c), sites (fractional)
  (0,0,0), (1/2,1/2,0), (1/2,1/6,1/2), (0,2/3,1/2).

Construction choices (deliberately different from a split-step / L-BFGS / sphere-cut / A-Cholesky route):
  * ground state: Newton-Krylov (bordered Newton system for (psi, mu), GMRES with a kinetic
    preconditioner, exact Hessian action), started from a variationally sized Gaussian-droplet guess;
    no imaginary time, no L-BFGS.
  * BdG basis: BOX cut |n_x| <= Mx, |n_y| <= My, |n_z| <= Mz on the orthorhombic reciprocal lattice
    G = 2 pi (n_x/Lx, n_y/Ly, n_z/Lz), projected on exact symmetry sectors (mirror, c-glide, centering).
  * exchange-like term X_{GG'} = Lam sum_K psi_{G-K} U^(|q+K|) psi_{K-G'} built as an explicit
    product W D W^dagger over an alias-free intermediate K set (no FFT in the BdG matrices).
  * algebra: Cholesky of L (not of A): L = D D^dagger, Hermitian D^dagger A D y = w^2 y,
    f_plus = D y / sqrt(w); full spectrum via eigh.  Check: full 2N non-Hermitian eig on a reduced basis.
  * chi_static = 2 <s|A^{-1}|s> by a direct dense linear solve (Cholesky solve), s = e^{iqx} psi0.

Stages (each caches to WORK; every foreground call stays well below 9 min, big cuts run under nohup):
  python3 xcheck3d.py lamc                      Lambda_c by three routes
  python3 xcheck3d.py gs 24 42 40               Newton-Krylov ground state (Gaussian-droplet guess)
  python3 xcheck3d.py gs 32 54 52 WORK/gs_24_42_40.npz   finer grid, spectrally interpolated seed
  python3 xcheck3d.py cut 7 12 11 nonherm       box cut M=(7,12,11): Gamma, q=0.15, 0.3 along x; q=0.15 along z
  python3 xcheck3d.py cut 9 15 14
  python3 xcheck3d.py cut 11 19 17 noq03 nogamma
  python3 xcheck3d.py final 7,12,11 9,15,14 11,19,17     -> xcheck3d_results.json
  python3 xcheck3d.py compare <md5 of results before comparison>   (post-save comparison with qb_results.json)
  python3 xcheck3d.py refine 11 19 17           (post-comparison diagnostic: Rayleigh-Ritz refined low modes)
The ground state used by all BdG stages is the 32x54x52 grid (GS_GRID).
"""
import os, sys, json, time, math
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
import numpy as np
import scipy.linalg as sla
import scipy.optimize as sopt
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = "/tmp/claude-0/-home-user-gifgaf0-github-io/6eab36f5-c943-5609-bc1f-38f855730ac1/scratchpad/work/xc3d"
os.makedirs(WORK, exist_ok=True)
RESULTS = os.path.join(HERE, "xcheck3d_results.json")

A_LAT = 1.3859646002819213
C_LAT = 2.2595969088482843
LX, LY, LZ = A_LAT, math.sqrt(3.0) * A_LAT, C_LAT
VOL = LX * LY * LZ
NCELL = VOL  # mean density 1
SITES = np.array([[0.0, 0.0, 0.0], [0.5, 0.5, 0.0], [0.5, 1.0 / 6.0, 0.5], [0.0, 2.0 / 3.0, 0.5]])


# ----------------------------------------------------------------------------------------------
# kernel and Lambda_c
# ----------------------------------------------------------------------------------------------
def uhat(k):
    """4 pi [sin k - k cos k]/k^3, series near 0."""
    k = np.asarray(k, dtype=float)
    out = np.empty_like(k)
    small = k < 0.1
    ks = k[small]
    k2 = ks * ks
    out[small] = 4.0 * np.pi * (1.0 / 3.0 - k2 / 30.0 + k2 * k2 / 840.0 - k2 ** 3 / 45360.0
                                + k2 ** 4 / 3991680.0)
    kb = k[~small]
    out[~small] = 4.0 * np.pi * (np.sin(kb) - kb * np.cos(kb)) / kb ** 3
    return out


def lambda_c():
    """Lam_c = min over k with U^<0 of -k^2/(4U^). Stationarity: 5(sin k - k cos k) = k^2 sin k."""
    f = lambda k: -k * k / (4.0 * uhat(np.array([k]))[0])
    g = lambda k: 5.0 * (math.sin(k) - k * math.cos(k)) - k * k * math.sin(k)
    # first negative window of U^: between the first two positive roots of tan k = k
    r1 = sopt.brentq(lambda k: math.sin(k) - k * math.cos(k), 4.0, 4.7, xtol=1e-15)
    r2 = sopt.brentq(lambda k: math.sin(k) - k * math.cos(k), 7.5, 7.9, xtol=1e-15)
    kst = sopt.brentq(g, r1 + 1e-6, r2 - 1e-6, xtol=1e-15, rtol=1e-15)
    # independent check: bounded scalar minimisation + dense scan in later windows
    res = sopt.minimize_scalar(f, bounds=(r1 + 1e-9, r2 - 1e-9), method="bounded",
                               options={"xatol": 1e-12})
    ks = np.linspace(0.01, 60.0, 600001)
    u = uhat(ks)
    neg = u < 0
    scan = (-ks[neg] ** 2 / (4.0 * u[neg])).min()
    return {"k_star": kst, "Lambda_c": f(kst), "Lambda_c_minscalar": float(res.fun),
            "k_star_minscalar": float(res.x), "Lambda_c_scan_0_60": float(scan),
            "window": [r1, r2]}


# ----------------------------------------------------------------------------------------------
# ground state on a real grid (pseudo-spectral), Newton-Krylov
# ----------------------------------------------------------------------------------------------
class Grid:
    def __init__(self, nx, ny, nz, lam):
        assert nx % 2 == 0 and ny % 6 == 0 and nz % 2 == 0
        self.n = (nx, ny, nz)
        self.lam = lam
        self.dv = VOL / (nx * ny * nz)
        kx = 2 * np.pi * np.fft.fftfreq(nx, d=LX / nx)
        ky = 2 * np.pi * np.fft.fftfreq(ny, d=LY / ny)
        kz = 2 * np.pi * np.fft.fftfreq(nz, d=LZ / nz)
        KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
        self.k2 = KX ** 2 + KY ** 2 + KZ ** 2
        self.kvec = (KX, KY, KZ)
        self.uk = lam * uhat(np.sqrt(self.k2))
        x = np.arange(nx) * LX / nx
        y = np.arange(ny) * LY / ny
        z = np.arange(nz) * LZ / nz
        self.X, self.Y, self.Z = np.meshgrid(x, y, z, indexing="ij")

    def kin(self, f):
        return np.fft.ifftn(0.5 * self.k2 * np.fft.fftn(f)).real

    def conv(self, f):
        return np.fft.ifftn(self.uk * np.fft.fftn(f)).real

    def inner(self, a, b):
        return float(np.sum(a * b) * self.dv)

    def sym(self, f):
        nx, ny, nz = self.n
        ix = (-np.arange(nx)) % nx
        f = 0.5 * (f + f[ix, :, :])                                   # mirror x -> -x
        iz = (-np.arange(nz)) % nz
        f = 0.5 * (f + f[:, :, iz])                                   # mirror z -> -z
        jy = (2 * ny // 3 - np.arange(ny)) % ny
        kz = (np.arange(nz) + nz // 2) % nz
        f = 0.5 * (f + f[:, jy, :][:, :, kz])                         # c-glide y->y0-y, z->z+c/2
        ix2 = (np.arange(nx) + nx // 2) % nx
        jy2 = (np.arange(ny) + ny // 2) % ny
        f = 0.5 * (f + f[ix2, :, :][:, jy2, :])                       # centering (1/2,1/2,0)
        return f

    def gaussians(self, sigma):
        f = np.zeros(self.n)
        for s in SITES:
            r0 = s * np.array([LX, LY, LZ])
            dx = (self.X - r0[0] + LX / 2) % LX - LX / 2
            dy = (self.Y - r0[1] + LY / 2) % LY - LY / 2
            dz = (self.Z - r0[2] + LZ / 2) % LZ - LZ / 2
            f += np.exp(-(dx ** 2 + dy ** 2 + dz ** 2) / (2 * sigma ** 2))
        return f * math.sqrt(NCELL / (np.sum(f * f) * self.dv))

    def energy(self, psi):
        rho = psi * psi
        phi = self.conv(rho)
        ekin = self.inner(psi, self.kin(psi))
        eint = 0.5 * self.inner(rho, phi)
        return ekin + eint, ekin, eint, phi

    def hpsi(self, psi, phi=None):
        if phi is None:
            phi = self.conv(psi * psi)
        return self.kin(psi) + phi * psi, phi


def ground_state(nx, ny, nz, lam, psi_init=None, tol=1e-12, maxit=60, verbose=True):
    g = Grid(nx, ny, nz, lam)
    log = []
    if psi_init is None:
        sig = np.linspace(0.08, 0.40, 33)
        es = []
        for s in sig:
            es.append(g.energy(g.gaussians(s))[0])
        s0 = sig[int(np.argmin(es))]
        # refine
        r = sopt.minimize_scalar(lambda s: g.energy(g.gaussians(s))[0], bounds=(s0 - 0.01, s0 + 0.01),
                                 method="bounded", options={"xatol": 1e-6})
        psi = g.gaussians(r.x)
        log.append({"guess_sigma": float(r.x), "guess_E_per_N": float(r.fun / NCELL)})
    else:
        psi = psi_init.copy()
        psi *= math.sqrt(NCELL / (np.sum(psi * psi) * g.dv))
    psi = g.sym(psi)
    hp, phi = g.hpsi(psi)
    mu = g.inner(psi, hp) / NCELL
    precond_shift = 1.0
    ntot = psi.size

    def resid(psi, mu):
        hp, phi = g.hpsi(psi)
        f1 = hp - mu * psi
        f2 = 0.5 * (g.inner(psi, psi) - NCELL)
        return f1, f2, phi

    f1, f2, phi = resid(psi, mu)
    for it in range(maxit):
        rn = math.sqrt(g.inner(f1, f1) / NCELL + f2 ** 2)
        log.append({"it": it, "resid": rn, "mu": mu, "E_per_N": g.energy(psi)[0] / NCELL})
        if verbose:
            print(f"  newton it {it}: |F| = {rn:.3e}  mu = {mu:.15f}", flush=True)
        if rn < tol:
            break
        phi_c = phi.copy()
        psi_c = psi.copy()
        mu_c = mu

        def matvec(v):
            d = v[:ntot].reshape(g.n)
            dm = v[ntot]
            out1 = g.kin(d) + (phi_c - mu_c) * d + 2.0 * psi_c * g.conv(psi_c * d) - dm * psi_c
            out2 = -g.inner(psi_c, d)
            return np.concatenate([out1.ravel(), [out2]])

        pk = 1.0 / (0.5 * g.k2 + precond_shift + abs(mu_c) * 0.0 + 1.0)

        def prec(v):
            d = v[:ntot].reshape(g.n)
            out1 = np.fft.ifftn(pk * np.fft.fftn(d)).real
            return np.concatenate([out1.ravel(), [v[ntot]]])

        Aop = spla.LinearOperator((ntot + 1, ntot + 1), matvec=matvec, dtype=float)
        Mop = spla.LinearOperator((ntot + 1, ntot + 1), matvec=prec, dtype=float)
        rhs = np.concatenate([-f1.ravel(), [f2]])
        sol, info = spla.gmres(Aop, rhs, M=Mop, rtol=min(1e-3, 0.1 * rn), atol=0.0,
                               restart=80, maxiter=40)
        d = g.sym(sol[:ntot].reshape(g.n))
        dm = sol[ntot]
        # backtracking on the residual norm
        t = 1.0
        while True:
            psi_n = psi + t * d
            mu_n = mu + t * dm
            f1n, f2n, phin = resid(psi_n, mu_n)
            rnn = math.sqrt(g.inner(f1n, f1n) / NCELL + f2n ** 2)
            if rnn < (1 - 1e-4 * t) * rn or t < 1e-3:
                break
            t *= 0.5
        psi, mu, f1, f2, phi = psi_n, mu_n, f1n, f2n, phin
        log[-1]["step"] = t
        log[-1]["gmres_info"] = int(info)
    # final normalisation & Rayleigh mu
    psi *= math.sqrt(NCELL / g.inner(psi, psi))
    E, ek, ei, phi = g.energy(psi)
    hp, _ = g.hpsi(psi, phi)
    mu = g.inner(psi, hp) / NCELL
    res = hp - mu * psi
    out = {"grid": [nx, ny, nz], "E_per_N": E / NCELL, "Ekin_per_N": ek / NCELL, "Eint_per_N": ei / NCELL,
           "mu": mu, "resid_rms": math.sqrt(g.inner(res, res) / NCELL), "log": log,
           "min_psi": float(psi.min()), "max_psi": float(psi.max())}
    return g, psi, out


def stage_gs(nx, ny, nz, lam, seed=None):
    fn = os.path.join(WORK, f"gs_{nx}_{ny}_{nz}.npz")
    if os.path.exists(fn):
        d = np.load(fn, allow_pickle=True)
        return d["psi"], json.loads(str(d["info"]))
    init = None
    if seed is not None:
        init = interp_fourier(seed, (nx, ny, nz))
    t0 = time.time()
    g, psi, info = ground_state(nx, ny, nz, lam, psi_init=init)
    info["time_s"] = time.time() - t0
    # Fourier decay diagnostics of psi
    pk = np.fft.fftn(psi) / psi.size
    info["psi_hat_max_edge"] = float(edge_max(pk))
    np.savez(fn, psi=psi, info=json.dumps(info))
    return psi, info


def edge_max(pk):
    """max |psi_G| on the outer shell of the FFT box (Nyquist planes and neighbours)."""
    nx, ny, nz = pk.shape
    m = 0.0
    a = np.abs(pk)
    for ax, n in enumerate(pk.shape):
        sl = [slice(None)] * 3
        sl[ax] = slice(n // 2 - 1, n // 2 + 2)
        m = max(m, float(a[tuple(sl)].max()))
    return m


def interp_fourier(psi, shape):
    """spectral interpolation of a periodic real array to a new grid shape."""
    n0 = psi.shape
    pk = np.fft.fftn(psi) / psi.size
    out = np.zeros(shape, dtype=complex)
    idx_old = [np.fft.fftfreq(n, d=1.0 / n).astype(int) for n in n0]
    for i0, ix in enumerate(idx_old[0]):
        if abs(ix) >= min(n0[0], shape[0]) // 2:
            continue
        for j0, iy in enumerate(idx_old[1]):
            if abs(iy) >= min(n0[1], shape[1]) // 2:
                continue
            kz = idx_old[2]
            ok = np.abs(kz) < min(n0[2], shape[2]) // 2
            out[ix % shape[0], iy % shape[1], kz[ok] % shape[2]] = pk[i0, j0, ok]
    return np.fft.ifftn(out).real * np.prod(shape)



# ----------------------------------------------------------------------------------------------
# Fourier data of the ground state (exact, alias-free products by zero padding)
# ----------------------------------------------------------------------------------------------
class FData:
    """psi_G, n_G, Phi_G stored in centred arrays: arr[n1+o1, n2+o2, n3+o3]."""

    def __init__(self, psi, lam, mu, pad):
        nx, ny, nz = psi.shape
        self.lam, self.mu = lam, mu
        pk = np.fft.fftn(psi) / psi.size
        h = (nx // 2 - 1, ny // 2 - 1, nz // 2 - 1)        # drop Nyquist planes (|psi_G| ~ 1e-14 there)
        self.hpsi = h
        # centred psi array large enough for all gathers: half-width = pad
        self.opsi = tuple(pad)
        shape = tuple(2 * p + 1 for p in pad)
        arr = np.zeros(shape, dtype=complex)
        for i in range(-h[0], h[0] + 1):
            for j in range(-h[1], h[1] + 1):
                ks = np.arange(-h[2], h[2] + 1)
                arr[i + pad[0], j + pad[1], ks + pad[2]] = pk[i % nx, j % ny, ks % nz]
        self.psi = arr
        # density and potential on a doubled grid (alias-free square)
        big = (2 * nx, 2 * ny, 2 * nz)
        pb = np.zeros(big, dtype=complex)
        for i in range(-h[0], h[0] + 1):
            for j in range(-h[1], h[1] + 1):
                ks = np.arange(-h[2], h[2] + 1)
                pb[i % big[0], j % big[1], ks % big[2]] = pk[i % nx, j % ny, ks % nz]
        psib = np.fft.ifftn(pb).real * np.prod(big)
        self.psi_imag_max = float(np.abs(np.fft.ifftn(pb).imag).max() * np.prod(big))
        nb = np.fft.fftn(psib * psib) / np.prod(big)
        hn = (nx - 1, ny - 1, nz - 1)
        self.ophi = hn
        phi = np.zeros(tuple(2 * x + 1 for x in hn), dtype=complex)
        nn = np.zeros_like(phi)
        for i in range(-hn[0], hn[0] + 1):
            for j in range(-hn[1], hn[1] + 1):
                ks = np.arange(-hn[2], hn[2] + 1)
                nn[i + hn[0], j + hn[1], ks + hn[2]] = nb[i % big[0], j % big[1], ks % big[2]]
        I, J, K = np.meshgrid(*[np.arange(-x, x + 1) for x in hn], indexing="ij")
        kk = 2 * np.pi * np.sqrt((I / LX) ** 2 + (J / LY) ** 2 + (K / LZ) ** 2)
        self.n = nn
        self.phi = lam * uhat(kk) * nn
        # psi support (index half-widths) at relative threshold
        a = np.abs(self.psi)
        self.amax = a.max()

    def support(self, eps):
        a = np.abs(self.psi)
        idx = np.argwhere(a >= eps * self.amax) - np.array(self.opsi)
        return idx


def g_of(n, q):
    return np.stack([q[0] + 2 * np.pi * n[..., 0] / LX, q[1] + 2 * np.pi * n[..., 1] / LY,
                     q[2] + 2 * np.pi * n[..., 2] / LZ], axis=-1)


def box_list(M):
    r = [np.arange(-m, m + 1) for m in M]
    I, J, K = np.meshgrid(*r, indexing="ij")
    n = np.stack([I.ravel(), J.ravel(), K.ravel()], axis=1)
    return n[(n[:, 0] + n[:, 1]) % 2 == 0]           # centering-even block (contains s = e^{iqx} psi0)


def op_images(n, kind):
    """images of index triples under the two commuting involutions of the q-sector, with phases."""
    def mz(n):
        m = n.copy(); m[:, 2] *= -1; return m, np.ones(len(n), dtype=complex)

    def mx(n):
        m = n.copy(); m[:, 0] *= -1; return m, np.ones(len(n), dtype=complex)

    def gl(n):  # c-glide (x, y, z) -> (x, y0 - y, z + c/2), y0 = 2/3 Ly, with e^{-i qz c/2} removed
        m = n.copy(); m[:, 1] *= -1
        return m, np.exp(1j * (4.0 * np.pi * n[:, 1] / 3.0 + np.pi * n[:, 2]))

    if kind == "x":      # q along x: mirror z and glide
        return mz, gl
    if kind == "z":      # q along z: mirror x and glide
        return mx, gl
    if kind == "gamma":
        return mz, gl
    if kind == "none":   # no symmetry reduction (identity ops): full centering-even block
        ident = lambda n: (n.copy(), np.ones(len(n), dtype=complex))
        return ident, ident
    raise ValueError(kind)


def sector_basis(M, kind, s1, s2):
    nl = box_list(M)
    N = len(nl)
    off = np.array(M)
    dims = 2 * off + 1
    lin = lambda n: ((n[:, 0] + off[0]) * dims[1] + (n[:, 1] + off[1])) * dims[2] + (n[:, 2] + off[2])
    pos = -np.ones(np.prod(dims), dtype=np.int64)
    pos[lin(nl)] = np.arange(N)
    S1, S2 = op_images(nl, kind)
    n1, p1 = S1(nl)
    n2, p2 = S2(nl)
    n12, p12b = S1(n2)
    i1, i2, i12 = pos[lin(n1)], pos[lin(n2)], pos[lin(n12)]
    assert (i1 >= 0).all() and (i2 >= 0).all() and (i12 >= 0).all()
    p12 = p2 * p12b
    idx = np.stack([np.arange(N), i1, i2, i12], axis=1)
    coef = np.stack([np.ones(N, dtype=complex), s1 * p1, s2 * p2, s1 * s2 * p12], axis=1) / 4.0
    rep = idx.min(axis=1) == np.arange(N)
    idx, coef = idx[rep], coef[rep]
    # merge duplicate indices within a column, normalise, drop null vectors
    cols_i, cols_c = [], []
    for r in range(len(idx)):
        d = {}
        for a in range(4):
            d[idx[r, a]] = d.get(idx[r, a], 0.0) + coef[r, a]
        ks = [k for k in d if abs(d[k]) > 1e-14]
        nrm = math.sqrt(sum(abs(d[k]) ** 2 for k in ks)) if ks else 0.0
        if nrm < 1e-12:
            continue
        ii = ks + [ks[0]] * (4 - len(ks))
        cc = [d[k] / nrm for k in ks] + [0.0] * (4 - len(ks))
        cols_i.append(ii); cols_c.append(cc)
    ci = np.array(cols_i, dtype=np.int64)
    cc = np.array(cols_c, dtype=complex)
    return nl, ci, cc


def check_orthonormal(N, ci, cc):
    import scipy.sparse as sp
    Ns = len(ci)
    rows = ci.ravel(); cols = np.repeat(np.arange(Ns), 4); vals = cc.ravel()
    Q = sp.csr_matrix((vals, (rows, cols)), shape=(N, Ns))
    G = (Q.conj().T @ Q).toarray()
    return float(np.abs(G - np.eye(Ns)).max()), Q


def build_sector(fd, q, M, kind, s1, s2, eps_psi=1e-14, kchunk=6144, verbose=True):
    t0 = time.time()
    nl, ci, cc = sector_basis(M, kind, s1, s2)
    Ns = len(ci)
    orth_err, Q = check_orthonormal(len(nl), ci, cc)
    Gn = nl[ci]                       # (Ns, 4, 3) index triples
    conjc = np.conj(cc)               # (Ns, 4)
    # --- L = kinetic + Phi - mu
    kin = 0.5 * np.sum(g_of(nl, q) ** 2, axis=1)
    diag_kin = np.sum(np.abs(cc) ** 2 * kin[ci], axis=1)
    o = np.array(fd.ophi)
    dph = np.array(fd.phi.shape)
    phif = fd.phi.ravel()
    Lm = np.zeros((Ns, Ns), dtype=complex)
    for a in range(4):
        for b in range(4):
            d = Gn[:, a, None, :] - Gn[None, :, b, :]
            assert (np.abs(d) <= o).all()
            li = ((d[..., 0] + o[0]) * dph[1] + (d[..., 1] + o[1])) * dph[2] + (d[..., 2] + o[2])
            Lm += (conjc[:, a, None] * cc[None, :, b]) * phif[li]
            del d, li
    Lm[np.diag_indices(Ns)] += diag_kin - fd.mu
    Lm = 0.5 * (Lm + Lm.conj().T)
    # --- X = lam W D W^dagger over alias-free K set (dilation of the box by the psi support)
    supp = fd.support(eps_psi)
    hs = np.abs(supp).max(axis=0)
    KM = np.array(M) + hs
    kd = 2 * KM + 1
    mark = np.zeros(kd, dtype=bool)
    for s in supp:
        lo = KM - np.array(M) - s
        mark[lo[0]:lo[0] + 2 * M[0] + 1, lo[1]:lo[1] + 2 * M[1] + 1, lo[2]:lo[2] + 2 * M[2] + 1] = True
    Kn = np.argwhere(mark) - KM
    Kn = Kn[(Kn[:, 0] + Kn[:, 1]) % 2 == 0]
    NK = len(Kn)
    uK = fd.lam * uhat(np.sqrt(np.sum(g_of(Kn, q) ** 2, axis=1)))
    op = np.array(fd.opsi)
    dps = np.array(fd.psi.shape)
    psif = fd.psi.ravel()
    Xm = np.zeros((Ns, Ns), dtype=complex)
    for k0 in range(0, NK, kchunk):
        Kc = Kn[k0:k0 + kchunk]
        W = np.zeros((Ns, len(Kc)), dtype=complex)
        for a in range(4):
            d = Gn[:, a, None, :] - Kc[None, :, :]
            assert (np.abs(d) <= op).all()
            li = ((d[..., 0] + op[0]) * dps[1] + (d[..., 1] + op[1])) * dps[2] + (d[..., 2] + op[2])
            W += conjc[:, a, None] * psif[li]
            del d, li
        Xm += (W * uK[k0:k0 + kchunk]) @ W.conj().T
        del W
    Xm = 0.5 * (Xm + Xm.conj().T)
    # --- s = e^{iq.r} psi0 and displacement probes h_j = e^{iq.r} psi0 d_j rho0
    sv = math.sqrt(VOL) * np.sum(conjc * psif[((Gn[..., 0] + op[0]) * dps[1] + (Gn[..., 1] + op[1]))
                                                * dps[2] + (Gn[..., 2] + op[2])], axis=1)
    info = {"Ns": Ns, "N_box_even": len(nl), "NK": NK, "psi_support_halfwidth": hs.tolist(),
            "orth_err": orth_err, "t_build": time.time() - t0}
    if verbose:
        print(f"   sector {kind}{s1:+d}{s2:+d} M={M}: Ns={Ns} NK={NK} build {info['t_build']:.1f}s", flush=True)
    return Lm, Xm, sv, (nl, ci, cc), info


def build_sector_multi(fd, qs, M, kind, s1, s2, eps_psi=1e-14, kchunk=6144, verbose=True):
    """same as build_sector, for several q sharing one sector basis (q_y = 0 and the q-components
    allowed by `kind`): the gathered W, the Phi part of L and s are q-independent; only the kinetic
    diagonal and U^(|q+K|) change."""
    t0 = time.time()
    nl, ci, cc = sector_basis(M, kind, s1, s2)
    Ns = len(ci)
    orth_err, Q = check_orthonormal(len(nl), ci, cc)
    Gn = nl[ci]
    conjc = np.conj(cc)
    o = np.array(fd.ophi)
    dph = np.array(fd.phi.shape)
    phif = fd.phi.ravel()
    # linear index of a centred array is affine in (n1, n2, n3): idx(G - G') = lin(G) - lin(G') + c0
    assert (2 * np.array(M) <= o).all()
    linp = lambda n, dd: (n[..., 0] * dd[1] + n[..., 1]) * dd[2] + n[..., 2]
    c0 = (o[0] * dph[1] + o[1]) * dph[2] + o[2]
    linG_phi = linp(Gn, dph)                     # (Ns, 4)
    Lphi = np.zeros((Ns, Ns), dtype=complex)
    for a in range(4):
        for b in range(4):
            li = linG_phi[:, a, None] - linG_phi[None, :, b] + c0
            Lphi += (conjc[:, a, None] * cc[None, :, b]) * phif[li]
            del li
    supp = fd.support(eps_psi)
    hs = np.abs(supp).max(axis=0)
    KM = np.array(M) + hs
    kd = 2 * KM + 1
    mark = np.zeros(kd, dtype=bool)
    for s in supp:
        lo = KM - np.array(M) - s
        mark[lo[0]:lo[0] + 2 * M[0] + 1, lo[1]:lo[1] + 2 * M[1] + 1, lo[2]:lo[2] + 2 * M[2] + 1] = True
    Kn = np.argwhere(mark) - KM
    Kn = Kn[(Kn[:, 0] + Kn[:, 1]) % 2 == 0]
    NK = len(Kn)
    uKs = [fd.lam * uhat(np.sqrt(np.sum(g_of(Kn, q) ** 2, axis=1))) for q in qs]
    op = np.array(fd.opsi)
    dps = np.array(fd.psi.shape)
    psif = fd.psi.ravel()
    Xs = [np.zeros((Ns, Ns), dtype=complex) for q in qs]
    assert (np.array(M) + np.abs(Kn).max(axis=0) <= op).all()
    cps = (op[0] * dps[1] + op[1]) * dps[2] + op[2]
    linG_psi = linp(Gn, dps)
    linK_psi = linp(Kn, dps)
    for k0 in range(0, NK, kchunk):
        lk = linK_psi[k0:k0 + kchunk]
        W = np.zeros((Ns, len(lk)), dtype=complex)
        for a in range(4):
            li = linG_psi[:, a, None] - lk[None, :] + cps
            W += conjc[:, a, None] * psif[li]
            del li
        Wh = W.conj().T
        for iq in range(len(qs)):
            Xs[iq] += (W * uKs[iq][k0:k0 + kchunk]) @ Wh
        del W, Wh
    sv = math.sqrt(VOL) * np.sum(conjc * psif[((Gn[..., 0] + op[0]) * dps[1] + (Gn[..., 1] + op[1]))
                                                * dps[2] + (Gn[..., 2] + op[2])], axis=1)
    mats = []
    for iq, q in enumerate(qs):
        kin = 0.5 * np.sum(g_of(nl, q) ** 2, axis=1)
        diag_kin = np.sum(np.abs(cc) ** 2 * kin[ci], axis=1)
        Lm = Lphi.copy()
        Lm[np.diag_indices(Ns)] += diag_kin - fd.mu
        Lm = 0.5 * (Lm + Lm.conj().T)
        Xm = 0.5 * (Xs[iq] + Xs[iq].conj().T)
        mats.append((Lm, Xm))
    Xs = None
    info = {"Ns": Ns, "N_box_even": len(nl), "NK": NK, "psi_support_halfwidth": hs.tolist(),
            "orth_err": orth_err, "t_build_all_q": time.time() - t0, "n_q_shared": len(qs)}
    if verbose:
        print(f"   sector {kind}{s1:+d}{s2:+d} M={M} ({len(qs)} q): Ns={Ns} NK={NK} build "
              f"{info['t_build_all_q']:.1f}s", flush=True)
    return mats, sv, (nl, ci, cc), info


def probes(fd, psi_grid, nl, ci, cc):
    """sector coefficients of h_j = psi0 d_j rho0 = 2 psi0^2 d_j psi0 (j = x, y, z)."""
    nx, ny, nz = psi_grid.shape
    big = (2 * nx, 2 * ny, 2 * nz)
    # spectral derivative on the doubled grid
    op = np.array(fd.opsi)
    pk = np.zeros(big, dtype=complex)
    h = fd.hpsi
    for i in range(-h[0], h[0] + 1):
        for j in range(-h[1], h[1] + 1):
            ks = np.arange(-h[2], h[2] + 1)
            pk[i % big[0], j % big[1], ks % big[2]] = fd.psi[i + op[0], j + op[1], ks + op[2]]
    kx = 2 * np.pi * np.fft.fftfreq(big[0], d=LX / big[0])
    ky = 2 * np.pi * np.fft.fftfreq(big[1], d=LY / big[1])
    kz = 2 * np.pi * np.fft.fftfreq(big[2], d=LZ / big[2])
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    ps = np.fft.ifftn(pk).real * np.prod(big)
    out = []
    for kk in (KX, KY, KZ):
        dpsi = np.fft.ifftn(1j * kk * pk).real * np.prod(big)
        hj = np.fft.fftn(2.0 * ps * ps * dpsi) / np.prod(big)
        n = nl[ci]
        vals = hj[n[..., 0] % big[0], n[..., 1] % big[1], n[..., 2] % big[2]]
        out.append(math.sqrt(VOL) * np.sum(np.conj(cc) * vals, axis=1))
    return out


def bdg_solve(Lm, Xm, sv, full=True, nlow=12):
    """L = D D^dagger; Hermitian D^dagger A D y = w^2 y; f_plus = D y / sqrt(w)."""
    t0 = time.time()
    Am = Lm + 2.0 * Xm
    D = sla.cholesky(Lm, lower=True)
    Mh = D.conj().T @ Am @ D
    Mh = 0.5 * (Mh + Mh.conj().T)
    w2, Y = sla.eigh(Mh, driver="evr") if full else sla.eigh(Mh, subset_by_index=[0, nlow - 1])
    w = np.sqrt(w2)
    Fp = (D @ Y) / np.sqrt(w)
    rho = sv.conj() @ Fp
    Z = np.abs(rho) ** 2
    # normalisation check  <f+|A|f+> / w = 1  on the lowest modes
    k = min(nlow, len(w))
    nrm = np.real(np.sum(Fp[:, :k].conj() * (Am @ Fp[:, :k]), axis=0)) / w[:k]
    # direct static response
    ca = sla.cho_factor(Am, lower=True)
    chi_direct = 2.0 * float(np.real(sv.conj() @ sla.cho_solve(ca, sv)))
    sLs = float(np.real(sv.conj() @ (Lm @ sv)))
    return {"w": w, "w2": w2, "Z": Z, "Fp": Fp, "norm_err": float(np.abs(nrm - 1).max()),
            "chi_direct": chi_direct, "sLs": sLs, "t_solve": time.time() - t0, "min_eig_L": None}


def eig_nonhermitian(Lm, Xm, nlow=10):
    """full 2N x 2N BdG matrix [[L+X, X], [-X, -(L+X)]] (non-Hermitian eig)."""
    Ns = Lm.shape[0]
    H = np.zeros((2 * Ns, 2 * Ns), dtype=complex)
    H[:Ns, :Ns] = Lm + Xm
    H[:Ns, Ns:] = Xm
    H[Ns:, :Ns] = -Xm
    H[Ns:, Ns:] = -(Lm + Xm)
    ev = sla.eigvals(H)
    pos = ev[ev.real > 0]
    pos = pos[np.argsort(pos.real)]
    return pos[:nlow], float(np.abs(ev.imag).max())


# ----------------------------------------------------------------------------------------------
# production driver (cached per case)
# ----------------------------------------------------------------------------------------------
GS_GRID = (32, 54, 52)
MMAX = (13, 22, 20)
_FD = {}


def get_fd():
    if "fd" not in _FD:
        lc = lambda_c()["Lambda_c"]
        lam = 2.0 * lc
        psi, info = stage_gs(*GS_GRID, lam)
        hp = (GS_GRID[0] // 2 - 1, GS_GRID[1] // 2 - 1, GS_GRID[2] // 2 - 1)
        pad = tuple(2 * MMAX[i] + hp[i] for i in range(3))
        _FD["fd"] = FData(psi, lam, info["mu"], pad)
        _FD["psi"] = psi
        _FD["info"] = info
    return _FD["fd"], _FD["psi"]


def case_name(M, q, kind, s1, s2):
    return f"case_M{M[0]}_{M[1]}_{M[2]}_q{q[0]:.4f}_{q[1]:.4f}_{q[2]:.4f}_{kind}{s1:+d}{s2:+d}"


def analyse_case(fd, psi, M, q, kind, s1, s2, Lm, Xm, sv, basis, info, nlow=16, nonherm=False):
    fn = os.path.join(WORK, case_name(M, q, kind, s1, s2) + ".json")
    nl, ci, cc = basis
    out = dict(info)
    out.update({"M": list(M), "q": list(q), "kind": kind, "s1": s1, "s2": s2})
    eL = sla.eigvalsh(Lm, subset_by_index=[0, 2])
    out["eigL_low"] = [float(x) for x in eL]
    if np.linalg.norm(q) == 0.0:
        Am = Lm + 2.0 * Xm
        out["eigA_low"] = [float(x) for x in sla.eigvalsh(Am, subset_by_index=[0, 3])]
        if eL[0] > 1e-8:   # L invertible in this sector: Gamma BdG spectrum via L-Cholesky form
            D = sla.cholesky(Lm, lower=True)
            w2 = sla.eigvalsh(D.conj().T @ Am @ D, subset_by_index=[0, 5])
            out["w2_gamma_low"] = [float(x) for x in w2]
        json.dump(out, open(fn, "w"), indent=1)
        print(f"   done {case_name(M, q, kind, s1, s2)}: eigA {out['eigA_low']}", flush=True)
        return out
    r = bdg_solve(Lm, Xm, sv, full=True, nlow=nlow)
    w, Z, Fp = r["w"], r["Z"], r["Fp"]
    hj = probes(fd, psi, nl, ci, cc)
    k = min(nlow, len(w))
    fn_nrm = np.sqrt(np.real(np.sum(Fp[:, :k].conj() * Fp[:, :k], axis=0)))
    P = [[float(abs(np.vdot(h, Fp[:, i])) / (np.linalg.norm(h) * fn_nrm[i] + 1e-300)) for i in range(k)]
         for h in hj]
    qq = float(np.dot(q, q))
    out.update({
        "w_low": [float(x) for x in w[:k]], "w2_min": float(r["w2"][0]), "Z_low": [float(x) for x in Z[:k]],
        "probe_x": P[0], "probe_y": P[1], "probe_z": P[2],
        "fsum_spectral": float(np.sum(w * Z)), "sLs": r["sLs"], "fsum_exact": NCELL * qq / 2.0,
        "chi_spectral": float(np.sum(2.0 * Z / w)), "chi_direct": r["chi_direct"],
        "norm_err": r["norm_err"], "t_solve": r["t_solve"], "ss": float(np.real(np.vdot(sv, sv))),
        "w_max": float(w[-1]),
    })
    if nonherm:
        t0 = time.time()
        ev, imax = eig_nonhermitian(Lm, Xm, nlow=10)
        out["nonherm_w_low"] = [float(x.real) for x in ev]
        out["nonherm_imag_max"] = imax
        out["nonherm_maxdiff_low"] = float(np.abs(np.array([x.real for x in ev]) - w[:len(ev)]).max())
        out["t_nonherm"] = time.time() - t0
    import resource
    out["maxrss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    json.dump(out, open(fn, "w"), indent=1)
    print(f"   done {case_name(M, q, kind, s1, s2)}: w_low {w[:4]} solve {r['t_solve']:.1f}s", flush=True)
    return out


def run_sector_multi(M, qs, kind, s1, s2, nonherm_q=None):
    todo = [q for q in qs if not os.path.exists(os.path.join(WORK, case_name(M, q, kind, s1, s2) + ".json"))]
    res = {}
    if todo:
        fd, psi = get_fd()
        mats, sv, basis, info = build_sector_multi(fd, todo, M, kind, s1, s2,
                                                   kchunk=4096 if len(box_list(M)) > 12000 else 6144)
        for q in todo:
            Lm, Xm = mats.pop(0)
            analyse_case(fd, psi, M, q, kind, s1, s2, Lm, Xm, sv, basis, info,
                         nonherm=(nonherm_q is not None and q == nonherm_q))
            del Lm, Xm
    for q in qs:
        res[q] = json.load(open(os.path.join(WORK, case_name(M, q, kind, s1, s2) + ".json")))
    return res


SECTORS = {"x": [(1, 1), (1, -1), (-1, 1)], "z": [(1, 1), (-1, 1), (1, -1)]}


def run_cut(M, qs_x=(0.15, 0.3), qs_z=(0.15,), gamma=True, nonherm=False):
    """kind 'x' sectors (mirror z, glide) serve Gamma and q along x with one shared basis/gather."""
    qx_list = ([(0.0, 0.0, 0.0)] if gamma else []) + [(qx, 0.0, 0.0) for qx in qs_x]
    for s in SECTORS["x"]:
        run_sector_multi(M, qx_list, "x", *s, nonherm_q=((0.15, 0.0, 0.0) if nonherm else None))
    qz_list = [(0.0, 0.0, qz) for qz in qs_z]
    for s in SECTORS["z"]:
        run_sector_multi(M, qz_list, "z", *s)



# ----------------------------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------------------------
def load_case(M, q, kind, s1, s2):
    fn = os.path.join(WORK, case_name(M, q, kind, s1, s2) + ".json")
    return json.load(open(fn)) if os.path.exists(fn) else None


def cut_summary(M, qs_x=(0.15, 0.3), qs_z=(0.15,)):
    out = {"M": list(M)}
    g = {}
    for s in SECTORS["x"]:
        c = load_case(M, (0.0, 0.0, 0.0), "x", *s)
        if c is not None:
            g[f"{s[0]:+d}{s[1]:+d}"] = {k: c.get(k) for k in ("Ns", "eigA_low", "eigL_low", "w2_gamma_low")}
    out["gamma"] = g
    for qx in qs_x:
        q = (qx, 0.0, 0.0)
        pp, pm, mp = (load_case(M, q, "x", *s) for s in SECTORS["x"])
        if pp is None or pm is None or mp is None:
            continue
        w, Z = pp["w_low"], pp["Z_low"]
        nq = NCELL * qx * qx / 2.0
        d = {"Ns_pp": pp["Ns"], "NK": pp["NK"],
             "w_pp_low": w[:6], "Z_pp_low": Z[:6], "probe_x_pp": pp["probe_x"][:6],
             "c2": w[0] / qx, "c1": w[1] / qx,
             "F2": w[0] * Z[0] / nq, "F1": w[1] * Z[1] / nq, "Z21": Z[0] / Z[1],
             "S2_over_spectral_sum": (2 * Z[0] / w[0]) / pp["chi_spectral"],
             "S2_over_chi_direct": (2 * Z[0] / w[0]) / pp["chi_direct"],
             "S1_over_spectral_sum": (2 * Z[1] / w[1]) / pp["chi_spectral"],
             "chi_direct": pp["chi_direct"], "chi_spectral": pp["chi_spectral"],
             "c_kappa": math.sqrt(VOL / pp["chi_direct"]),
             "c_kappa_from_spectral_sum": math.sqrt(VOL / pp["chi_spectral"]),
             "fsum_resid_vs_exact": pp["fsum_spectral"] / nq - 1.0,
             "fsum_resid_sLs_vs_exact": pp["sLs"] / nq - 1.0,
             "fsum_spectral_vs_sLs": pp["fsum_spectral"] / pp["sLs"] - 1.0,
             "static_resid_spectral_vs_direct": pp["chi_spectral"] / pp["chi_direct"] - 1.0,
             "F_sum_two_gapless": (w[0] * Z[0] + w[1] * Z[1]) / nq,
             "norm_err_max": max(pp["norm_err"], pm["norm_err"], mp["norm_err"]),
             "w2_min_all_sectors": min(pp["w2_min"], pm["w2_min"], mp["w2_min"]),
             "Zmax_odd_sectors": max(max(pm["Z_low"]), max(mp["Z_low"])),
             }
        # y-polarised transverse: glide-odd sector; pick by displacement probe among the two lowest
        iy = int(np.argmax(pm["probe_y"][:2]))
        d.update({"w_pm_low": pm["w_low"][:6], "probe_y_pm": pm["probe_y"][:6], "probe_x_pm": pm["probe_x"][:6],
                  "probe_z_pm": pm["probe_z"][:6], "iy": iy, "cT_y": pm["w_low"][iy] / qx,
                  "w_mp_low": mp["w_low"][:6], "probe_z_mp": mp["probe_z"][:6], "cT_z": mp["w_low"][0] / qx})
        if "nonherm_w_low" in pp:
            d["nonherm_check_pp"] = {k: pp[k] for k in ("nonherm_w_low", "nonherm_imag_max", "nonherm_maxdiff_low")}
        out[f"qx_{qx}"] = d
    for qz in qs_z:
        q = (0.0, 0.0, qz)
        pp, mp, pm = (load_case(M, q, "z", *s) for s in SECTORS["z"])
        if pp is None or mp is None or pm is None:
            continue
        nq = NCELL * qz * qz / 2.0
        iy = int(np.argmax(pm["probe_y"][:2]))
        out[f"qz_{qz}"] = {
            "cT_x": mp["w_low"][0] / qz, "w_mp_low": mp["w_low"][:6], "probe_x_mp": mp["probe_x"][:6],
            "cT_y": pm["w_low"][iy] / qz, "iy": iy, "w_pm_low": pm["w_low"][:6], "probe_y_pm": pm["probe_y"][:6],
            "w_pp_low": pp["w_low"][:6], "Z_pp_low": pp["Z_low"][:6], "probe_z_pp": pp["probe_z"][:6],
            "c_lower_long_z": pp["w_low"][0] / qz, "c_upper_long_z": pp["w_low"][1] / qz,
            "F_lower_z": pp["w_low"][0] * pp["Z_low"][0] / nq,
            "c_kappa_z": math.sqrt(VOL / pp["chi_direct"]),
            "fsum_resid_vs_exact": pp["fsum_spectral"] / nq - 1.0,
            "static_resid_spectral_vs_direct": pp["chi_spectral"] / pp["chi_direct"] - 1.0,
            "w2_min_all_sectors": min(pp["w2_min"], pm["w2_min"], mp["w2_min"]),
        }
    return out


def finalize(cuts):
    """assemble xcheck3d_results.json from cached cases; primary = largest complete cut."""
    lc = lambda_c()
    gsinfo = {}
    for gfile in sorted(os.listdir(WORK)):
        if gfile.startswith("gs_") and gfile.endswith(".npz"):
            d = np.load(os.path.join(WORK, gfile), allow_pickle=True)
            info = json.loads(str(d["info"]))
            gsinfo[gfile[3:-4]] = info
    summ = {}
    for M in cuts:
        s = cut_summary(M)
        if "qx_0.15" in s and "qz_0.15" in s:
            summ["M_%d_%d_%d" % tuple(M)] = s
    keys = list(summ.keys())
    P, Q = summ[keys[-1]], (summ[keys[-2]] if len(keys) > 1 else None)
    q1, q2 = 0.15, 0.3
    a = P["qx_0.15"]
    k03 = [k for k in keys if "qx_0.3" in summ[k]]
    b = summ[k03[-1]]["qx_0.3"] if k03 else None
    if b is not None and k03[-1] != keys[-1]:
        # q = 0.3 only at a smaller cut: pair it with q = 0.15 from the same cut for slopes/ratios
        a03 = summ[k03[-1]]["qx_0.15"]
    else:
        a03 = a
    prim = {
        "cut_used": keys[-1],
        "c2_q015": a["c2"], "c1_q015": a["c1"], "F2_q015": a["F2"], "F1_q015": a["F1"], "Z21_q015": a["Z21"],
        "S2_q015": a["S2_over_spectral_sum"], "S2_q015_over_chi_direct": a["S2_over_chi_direct"],
        "c_kappa_q015": a["c_kappa"], "chi_static_q015_direct": a["chi_direct"],
        "chi_static_q015_spectral": a["chi_spectral"],
        "cT_alongx_ypol_q015": a["cT_y"], "cT_alongx_zpol_q015": a["cT_z"],
        "cT_alongz_xpol_q015": P["qz_0.15"]["cT_x"], "cT_alongz_ypol_q015": P["qz_0.15"]["cT_y"],
        "fsum_resid_q015": a["fsum_resid_vs_exact"], "static_resid_q015": a["static_resid_spectral_vs_direct"],
        "sum_F_over_c2_two_gapless_q015": a["F2"] / a["c2"] ** 2 + a["F1"] / a["c1"] ** 2,
        "inv_c_kappa2_q015": 1.0 / a["c_kappa"] ** 2,
    }
    cts = [prim["cT_alongx_ypol_q015"], prim["cT_alongx_zpol_q015"], prim["cT_alongz_xpol_q015"],
           prim["cT_alongz_ypol_q015"]]
    prim["cT_min_xz_q015"] = min(cts)
    prim["cT_max_xz_q015"] = max(cts)
    prim["c2_gt_cT_any"] = bool(prim["c2_q015"] > min(cts))
    if b is not None:
        prim["cut_used_q03_and_slopes"] = k03[-1]
        a = a03
        lsq = lambda w1, w2: (w1 * q1 + w2 * q2) / (q1 * q1 + q2 * q2)
        prim.update({
            "c2_q03": b["c2"], "c1_q03": b["c1"], "F2_q03": b["F2"], "Z21_q03": b["Z21"],
            "S2_q03": b["S2_over_spectral_sum"], "c_kappa_q03": b["c_kappa"],
            "cT_alongx_ypol_q03": b["cT_y"], "cT_alongx_zpol_q03": b["cT_z"],
            "fsum_resid_q03": b["fsum_resid_vs_exact"], "static_resid_q03": b["static_resid_spectral_vs_direct"],
            "c2_lsq_015_03": lsq(a["c2"] * q1, b["c2"] * q2), "c1_lsq_015_03": lsq(a["c1"] * q1, b["c1"] * q2),
            "cT_alongx_ypol_lsq": lsq(a["cT_y"] * q1, b["cT_y"] * q2),
            "cT_alongx_zpol_lsq": lsq(a["cT_z"] * q1, b["cT_z"] * q2),
            "gapless_ratio_w03_over_w015": {"mode2": b["c2"] * q2 / (a["c2"] * q1),
                                            "mode1": b["c1"] * q2 / (a["c1"] * q1),
                                            "T_ypol": b["cT_y"] * q2 / (a["cT_y"] * q1),
                                            "T_zpol": b["cT_z"] * q2 / (a["cT_z"] * q1),
                                            "gapped_glide_odd": b["w_pm_low"][0] / a["w_pm_low"][0]},
        })
        bq = (b["c_kappa"] - a["c_kappa"]) / (q2 * q2 - q1 * q1)
        prim["c_kappa_q0_extrap_quadratic"] = a["c_kappa"] - bq * q1 * q1
        a = P["qx_0.15"]
    conv = {}
    if Q is not None:
        qa = Q["qx_0.15"]
        for k in ("c2", "c1", "F2", "Z21", "c_kappa", "cT_y", "cT_z"):
            conv[k + "_rel_change"] = a[k] / qa[k] - 1.0
        conv["S2_abs_change"] = a["S2_over_spectral_sum"] - qa["S2_over_spectral_sum"]
        conv["cT_alongz_xpol_rel_change"] = P["qz_0.15"]["cT_x"] / Q["qz_0.15"]["cT_x"] - 1.0
        conv["compared"] = [keys[-2], keys[-1]]
    table = {}
    for kname in keys:
        s = summ[kname]["qx_0.15"]
        z = summ[kname]["qz_0.15"]
        table[kname] = {"Ns_pp": s["Ns_pp"], "NK": s["NK"], "c2": s["c2"], "c1": s["c1"], "F2": s["F2"],
                        "Z21": s["Z21"], "S2": s["S2_over_spectral_sum"], "c_kappa": s["c_kappa"],
                        "cT_alongx_ypol": s["cT_y"], "cT_alongx_zpol": s["cT_z"], "cT_alongz_xpol": z["cT_x"],
                        "cT_alongz_ypol": z["cT_y"], "fsum_resid": s["fsum_resid_vs_exact"],
                        "static_resid": s["static_resid_spectral_vs_direct"], "norm_err_max": s["norm_err_max"]}
    # f_s estimate from the lowest eigenvalue of L(q) in the (+,+) sector (band curvature), extra only
    fs_est = {}
    for kname in keys:
        Mt = tuple(summ[kname]["M"])
        c = load_case(Mt, (0.15, 0.0, 0.0), "x", 1, 1)
        fs_est[kname] = 2.0 * c["eigL_low"][0] / 0.15 ** 2
    # dispersion along x at the cheapest converged cut (extra): w/q of the identified branches
    disp = {}
    Md = (7, 12, 11)
    for qx in (0.05, 0.1, 0.15, 0.3):
        q = (qx, 0.0, 0.0)
        pp, pm, mp = (load_case(Md, q, "x", *s) for s in SECTORS["x"])
        if pp is None or pm is None or mp is None:
            continue
        disp[str(qx)] = {"c2": pp["w_low"][0] / qx, "c1": pp["w_low"][1] / qx,
                         "glide_odd_two_lowest_w": pm["w_low"][:2], "glide_odd_probe_y": pm["probe_y"][:2],
                         "cT_zpol": mp["w_low"][0] / qx}
    out = {
        "dispersion_alongx_M7_12_11": disp,
        "task": "independent 3D cross-check (xcheck3d), second leg",
        "model": {"Lambda_c": lc, "Lambda": 2.0 * lc["Lambda_c"], "a": A_LAT, "c": C_LAT,
                  "cell": "orthorhombic (a, sqrt3 a, c), 4 sites", "vol": VOL, "N_cell": NCELL},
        "ground_state": gsinfo,
        "primary": prim,
        "convergence_last_two_cuts": conv,
        "convergence_table_q015": table,
        "f_s_estimate_from_band_curvature_q015": fs_est,
        "cuts": summ,
    }
    json.dump(out, open(RESULTS, "w"), indent=1)
    return out


def compare_with_qb(qb_path, pre_md5):
    """post-save comparison with this leg's main 3D instrument (qb_results.json). Appends one key;
    the own-number keys of the results file are left unchanged."""
    mine = json.load(open(RESULTS))
    qb = json.load(open(qb_path))
    P = mine["primary"]
    cuts = mine["cuts"]
    c11 = cuts["M_11_19_17"]
    c9 = cuts["M_9_15_14"]
    S, E = qb["schema"], qb["extras"]
    T = E["transverse_speeds_q015"]
    rows = [
        # (name, mine, qb, kind) kind: speed (0.3% rel), weight (2% rel), share (0.01 abs), info
        ("c2_q015", P["c2_q015"], S["c2"], "speed"),
        ("c1_q015", P["c1_q015"], S["c1_basal_q015"], "speed"),
        ("cT_min", P["cT_min_xz_q015"], S["cT_min"], "speed"),
        ("cT_max", P["cT_max_xz_q015"], S["cT_max"], "speed"),
        ("cT_alongx_zpol_q015", P["cT_alongx_zpol_q015"], T["x_Tz"], "speed"),
        ("cT_alongx_ypol_q015", P["cT_alongx_ypol_q015"], T["x_Ty"], "speed"),
        ("cT_alongz_xpol_q015", P["cT_alongz_xpol_q015"], T["z_Tx"], "speed"),
        ("cT_alongz_ypol_q015", P["cT_alongz_ypol_q015"], T["z_Ty"], "speed"),
        ("c_kappa_q015", P["c_kappa_q015"], S["c_kappa"], "speed"),
        ("F2_q015", P["F2_q015"], S["F2_basal_q015"], "weight"),
        ("F1_q015", P["F1_q015"], E["F1_basal_q015"], "weight"),
        ("Z21_q015", P["Z21_q015"], S["Z21_basal_q015"], "weight"),
        ("S2_q015", P["S2_q015"], S["S2_basal_q015"], "share"),
        ("S2_q015_cut9", c9["qx_0.15"]["S2_over_spectral_sum"], S["S2_basal_q015"], "share"),
        ("S1_q015", c11["qx_0.15"]["S1_over_spectral_sum"], E["S1_basal_q015"], "share"),
        ("c2_q03", P["c2_q03"], E["c2_q03"], "speed"),
        ("c1_q03", P["c1_q03"], E["c1_basal_q03"], "speed"),
        ("cT_alongx_zpol_q03", P["cT_alongx_zpol_q03"], E["speed_x_Tz_q0.3"], "speed"),
        ("cT_alongx_ypol_q03", P["cT_alongx_ypol_q03"], E["speed_x_Ty_q0.3"], "speed"),
        ("c_kappa_q03", P["c_kappa_q03"], E["c_kappa_q03"], "speed"),
        ("F2_q03", P["F2_q03"], E["F2_basal_q03"], "weight"),
        ("Z21_q03", P["Z21_q03"], E["Z21_basal_q03"], "weight"),
        ("S2_q03", P["S2_q03"], E["S2_basal_q03"], "share"),
        ("c2_lsq_x", P["c2_lsq_015_03"], E["lsq_speeds"]["x"]["L2"], "speed"),
        ("c1_lsq_x", P["c1_lsq_015_03"], E["lsq_speeds"]["x"]["L1"], "speed"),
        ("cT_zpol_lsq_x", P["cT_alongx_zpol_lsq"], E["lsq_speeds"]["x"]["Tz"], "speed"),
        ("cT_ypol_lsq_x", P["cT_alongx_ypol_lsq"], E["lsq_speeds"]["x"]["Ty"], "speed"),
        ("c_lower_alongz_q015", c11["qz_0.15"]["c_lower_long_z"], E["c2_z_q015"], "speed"),
        ("c_upper_alongz_q015", c11["qz_0.15"]["c_upper_long_z"], E["c1_z_q015"], "speed"),
        ("F_lower_alongz_q015", c11["qz_0.15"]["F_lower_z"], E["F2_z_q015"], "weight"),
        ("c_kappa_alongz_q015", c11["qz_0.15"]["c_kappa_z"], E["c_kappa_z_q015"], "speed"),
        ("E_per_N", mine["ground_state"]["32_54_52"]["E_per_N"],
         qb["ground_state"]["primary_prim_sphere_K50"]["e_per_particle"], "info"),
        ("mu", mine["ground_state"]["32_54_52"]["mu"], qb["ground_state"]["primary_prim_sphere_K50"]["mu"], "info"),
        ("Lambda_c", mine["model"]["Lambda_c"]["Lambda_c"], qb["Lambda_c"], "info"),
        ("gamma_A_first_nonzero", c9["gamma"]["+1+1"]["eigA_low"][1],
         E["gamma_sector"]["K50"]["A_lowest"][3], "info"),
        ("gamma_L_glide_odd_lowest", c9["gamma"]["+1-1"]["eigL_low"][0],
         E["gamma_sector"]["K50"]["L_lowest"][1], "info"),
    ]
    out = []
    worst = {"speed": 0.0, "weight": 0.0, "share": 0.0, "info": 0.0}
    for name, a, b, kind in rows:
        rel = (a - b) / b
        ab = a - b
        if kind == "speed":
            ok = abs(rel) <= 3e-3
            worst[kind] = max(worst[kind], abs(rel))
        elif kind == "weight":
            ok = abs(rel) <= 2e-2
            worst[kind] = max(worst[kind], abs(rel))
        elif kind == "share":
            ok = abs(ab) <= 1e-2
            worst[kind] = max(worst[kind], abs(ab))
        else:
            ok = True
            worst[kind] = max(worst[kind], abs(rel))
        out.append({"q": name, "xcheck3d": a, "qb": b, "rel_diff": rel, "abs_diff": ab, "kind": kind,
                    "within_threshold": bool(ok)})
    conv = {"c_kappa_q0_two_point_mine_c_linear_in_q2": P["c_kappa_q0_extrap_quadratic"],
            "c_kappa_q0_two_point_qb": E["c_kappa_q0_two_point"],
            "c_kappa_q0_two_point_qb_convention_c2_linear_in_q2_recomputed_from_qb_inputs":
                math.sqrt(S["c_kappa"] ** 2 - 0.0225 * (E["c_kappa_q03"] ** 2 - S["c_kappa"] ** 2) / 0.0675),
            "c_kappa_q0_qb_small_q_fit": E["c_kappa_q0_extrapolated"],
            "note": "different extrapolation variable (c vs c^2 linear in q^2), an O(q^4) convention difference;"
                    " not a schema quantity"}
    fs = {"qb_linear_response_fs_x_K50": E["superfluid_fraction_linear_response"]["K50"]["fs_x"],
          "xcheck3d_band_curvature_2lamL_over_q2_at_q015": mine["f_s_estimate_from_band_curvature_q015"]["M_11_19_17"],
          "note": "not the same estimator: band curvature at finite q carries an O(q^2) correction"}
    res = {"pre_comparison_results_md5": pre_md5,
           "thresholds": {"speed_and_c_kappa_rel": 3e-3, "F_and_Z21_rel": 2e-2, "S_abs": 1e-2},
           "rows": out, "max_abs_diff_by_kind": worst,
           "all_within_threshold": bool(all(r["within_threshold"] for r in out)),
           "extrapolation_convention": conv, "superfluid_fraction_estimators": fs,
           "sum_rule_residuals": {"qb_max_fsum": E["max_abs_fsum_rel_residual"],
                                  "qb_max_static": E["max_abs_static_rel_residual"],
                                  "xcheck3d_fsum_q015": P["fsum_resid_q015"],
                                  "xcheck3d_static_q015": P["static_resid_q015"]}}
    # post-comparison diagnostic: Rayleigh-Ritz refined lowest (+,+) modes (removes eigh rounding)
    refd = {}
    for Mt in ((9, 15, 14), (11, 19, 17)):
        f = os.path.join(WORK, "refine_" + case_name(Mt, (0.15, 0.0, 0.0), "x", 1, 1) + ".json")
        if os.path.exists(f):
            rr = json.load(open(f))
            refd["M_%d_%d_%d" % Mt] = {
                "values": {k: rr[k] for k in ("c2_refined", "c1_refined", "F2_refined", "Z21_refined",
                                               "S2_refined_over_spectral", "static_resid_refined",
                                               "fsum_resid_refined", "norm_err_refined", "norm_err_eigh")},
                "rel_diff_vs_qb": {"c2": rr["c2_refined"] / S["c2"] - 1.0,
                                   "c1": rr["c1_refined"] / S["c1_basal_q015"] - 1.0,
                                   "F2": rr["F2_refined"] / S["F2_basal_q015"] - 1.0,
                                   "Z21": rr["Z21_refined"] / S["Z21_basal_q015"] - 1.0},
                "abs_diff_vs_qb": {"S2": rr["S2_refined_over_spectral"] - S["S2_basal_q015"]}}
    res["refined_low_modes_post_comparison_diagnostic"] = refd
    mine["comparison_with_qb_results_post_save"] = res
    json.dump(mine, open(RESULTS, "w"), indent=1)
    return res


def refine_low_modes(M, q=(0.15, 0.0, 0.0), k=12):
    """diagnostic: Rayleigh-Ritz refinement of the lowest (+,+) modes on the pencil A f = w^2 L^{-1} f,
    using the eigh vectors as trial space (removes the eigh rounding of a graded spectrum)."""
    fn = os.path.join(WORK, "refine_" + case_name(M, q, "x", 1, 1) + ".json")
    if os.path.exists(fn):
        return json.load(open(fn))
    fd, psi = get_fd()
    mats, sv, basis, info = build_sector_multi(fd, [q], M, "x", 1, 1,
                                               kchunk=4096 if len(box_list(M)) > 12000 else 6144)
    Lm, Xm = mats.pop(0)
    r = bdg_solve(Lm, Xm, sv, full=True, nlow=k)
    Am = Lm + 2.0 * Xm
    F = r["Fp"][:, :k]
    cl = sla.cho_factor(Lm, lower=True)
    At = F.conj().T @ (Am @ F)
    Bt = F.conj().T @ sla.cho_solve(cl, F)
    At = 0.5 * (At + At.conj().T)
    Bt = 0.5 * (Bt + Bt.conj().T)
    w2r, C = sla.eigh(At, Bt)
    wr = np.sqrt(w2r)
    Fr = (F @ C) / np.sqrt(wr)              # <f|L^-1|f> = 1  ->  <f+|A|f+> = w
    Zr = np.abs(sv.conj() @ Fr) ** 2
    nrm = np.real(np.sum(Fr.conj() * (Am @ Fr), axis=0)) / wr
    w, Z = r["w"], r["Z"]
    chi_spec_ref = float(np.sum(2.0 * Z[k:] / w[k:]) + np.sum(2.0 * Zr / wr))
    fsum_ref = float(np.sum(w[k:] * Z[k:]) + np.sum(wr * Zr))
    qx = q[0]
    nq = NCELL * qx * qx / 2.0
    out = {"M": list(M), "q": list(q), "k": k,
           "w_eigh": [float(x) for x in w[:4]], "w_refined": [float(x) for x in wr[:4]],
           "Z_eigh": [float(x) for x in Z[:4]], "Z_refined": [float(x) for x in Zr[:4]],
           "norm_err_refined": float(np.abs(nrm - 1).max()), "norm_err_eigh": r["norm_err"],
           "c2_refined": float(wr[0] / qx), "c1_refined": float(wr[1] / qx),
           "F2_refined": float(wr[0] * Zr[0] / nq), "Z21_refined": float(Zr[0] / Zr[1]),
           "chi_direct": r["chi_direct"], "chi_spectral_refined": chi_spec_ref,
           "static_resid_refined": chi_spec_ref / r["chi_direct"] - 1.0,
           "fsum_resid_refined": fsum_ref / nq - 1.0,
           "S2_refined_over_spectral": float((2 * Zr[0] / wr[0]) / chi_spec_ref),
           "S2_refined_over_chi_direct": float((2 * Zr[0] / wr[0]) / r["chi_direct"])}
    json.dump(out, open(fn, "w"), indent=1)
    return out

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "help":
        print(__doc__)
    elif cmd == "lamc":
        print(json.dumps(lambda_c(), indent=1))
    elif cmd == "gs":
        nx, ny, nz = map(int, sys.argv[2:5])
        lc = lambda_c()["Lambda_c"]
        seed = None
        if len(sys.argv) > 5:
            seed = np.load(sys.argv[5])["psi"]
        psi, info = stage_gs(nx, ny, nz, 2.0 * lc, seed)
        info.pop("log", None)
        print(json.dumps(info, indent=1))
    elif cmd == "cut":
        M = tuple(map(int, sys.argv[2:5]))
        qs_x = (0.15, 0.3)
        qs_z = (0.15,)
        nonherm = "nonherm" in sys.argv
        if "noq03" in sys.argv:
            qs_x = (0.15,)
        run_cut(M, qs_x=qs_x, qs_z=qs_z, nonherm=nonherm, gamma=("nogamma" not in sys.argv))
    elif cmd == "compare":
        res = compare_with_qb(os.path.join(HERE, "qb_results.json"), sys.argv[2])
        for r in res["rows"]:
            print(f"{r['q']:32s} {r['xcheck3d']!r:>24} {r['qb']!r:>24} rel {r['rel_diff']: .3e} "
                  f"abs {r['abs_diff']: .3e} {'ok' if r['within_threshold'] else 'EXCEEDS'}")
        print(json.dumps(res["max_abs_diff_by_kind"]), res["all_within_threshold"])
    elif cmd == "refine":
        M = tuple(map(int, sys.argv[2:5]))
        print(json.dumps(refine_low_modes(M), indent=1))
    elif cmd == "final":
        cuts = [tuple(map(int, c.split(","))) for c in sys.argv[2:]]
        out = finalize(cuts)
        print(json.dumps(out["primary"], indent=1))
        print(json.dumps(out["convergence_last_two_cuts"], indent=1))
