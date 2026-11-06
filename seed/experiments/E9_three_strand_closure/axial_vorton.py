"""
E9 option 4, Phase 1 (PREREG_option4 §3 as amended by §9, Amendment A): the charged, current-carrying loop,
axisymmetric, on the (rho, z) half-plane. Label: Exploration, post-hoc selection (§9). Model units only.

Energy (PREREG_option4 §1.1 reduced to (rho, z), plus §1.2's fixed-charge term), weight 2 pi rho:
    E = sum_k [ |D psi_k|^2 + 1/2 (|psi_k|^2 - 1)^2 ] + 1/2 F_{rho z}^2 - eta sum_{i<j} Re(psi_i conj psi_j)
      + |grad s|^2 + n^2 |s|^2 / rho^2 - mu2 |s|^2 + lam/2 |s|^4 + beta |s|^2 sum_k |psi_k|^2
      + Q^2 / (4 I),   I = int 2 pi rho |s|^2 drho dz,      sigma = s(rho, z) e^{i n phi} e^{-i omega t}
measured above the true vacuum (|psi_k|^2 = 1 + eta, s = 0) on the same grid.

Lattice (mirrors gl3.py): sites rho_i = (i + 1/2) h, z_j = -32 + j h, h = 0.25, rho <= 32, z in [-32, 32];
psi_k and s complex on sites; A_rho, A_z on links, non-compact; covariant difference
(exp(-i e h A) psi(x + mu) - psi(x)) / h; s is neutral (plain differences); open boundaries.
Weights: site and z-link 2 pi rho_i h^2; rho-link and plaquette 2 pi rho_{i+1/2} h^2 with rho_{i+1/2} = (i + 1) h.
The face at rho = 0 has zero weight, so omitting it is exact (no axis boundary condition is imposed).

Usage:
    python3 axial_vorton.py gradcheck          -> gradient checks (full functional, n^2/rho^2 term, Q^2/4I term)
    python3 axial_vorton.py profiles           -> phase1_profiles.json (straight string at b3_d1, (k*, q*))
    python3 axial_vorton.py run                -> all 11 runs, 4 in parallel -> phase1_results.json, phase1_<run>.npz
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np, json, sys, time, platform
from scipy.optimize import minimize
import scipy

E_CH = 1 / np.sqrt(12.0); ETA = 0.1
H = 0.25; RHO_MAX = 32.0; ZMAX = 32.0
VVAC = 3 * (0.5 * ETA ** 2 - ETA * (1 + ETA))       # vacuum energy density (gl3.vacuum_energy per volume)
FV = np.sqrt(1 + ETA)
XI2 = 2 / np.sqrt(2.0)                               # 2 xi = 1.41 coordinate units
LEAK_W = 4.0                                         # leak band: within 4 units of a box edge
MAXITER = 50000; GTOL = 1e-5; FTOL = 1e-13           # gl3.minimize options, maxiter chosen before any run
EVERY = 50


class Axial:
    def __init__(self, beta, mu2, lam, n, Q, h=H, rho_max=RHO_MAX, zmax=ZMAX, e=E_CH, eta=ETA):
        self.beta, self.mu2, self.lam, self.n, self.Q = beta, mu2, lam, n, Q
        self.h, self.e, self.eta = h, e, eta
        self.Nr = int(np.floor(rho_max / h - 0.5 + 1e-9)) + 1          # rho_i = (i + 1/2) h <= rho_max
        self.Nz = int(round(2 * zmax / h)) + 1
        self.rho = (np.arange(self.Nr) + 0.5) * h
        self.z = -zmax + np.arange(self.Nz) * h
        self.R, self.Z = np.meshgrid(self.rho, self.z, indexing='ij')
        self.rho_max, self.zmax = rho_max, zmax
        h2 = h * h
        self.ws = (2 * np.pi * self.rho * h2)[:, None]                      # sites, z-links
        self.wr = (2 * np.pi * (np.arange(1, self.Nr) * h) * h2)[:, None]   # rho-links, plaquettes
        self.ns = self.Nr * self.Nz
        self.nar = (self.Nr - 1) * self.Nz; self.naz = self.Nr * (self.Nz - 1)
        self.size = 8 * self.ns + self.nar + self.naz
        self.Evac = VVAC * float(np.sum(self.ws) * self.Nz)
        self.terms = None     # None = all; else a set of term names (used only by the gradient check)

    # ---- packing ------------------------------------------------------------
    def pack(self, psi, s, Ar, Az):
        return np.concatenate([psi.real.ravel(), psi.imag.ravel(), s.real.ravel(), s.imag.ravel(), Ar.ravel(), Az.ravel()])

    def unpack(self, v):
        n3 = 3 * self.ns; Nr, Nz = self.Nr, self.Nz
        psi = (v[:n3] + 1j * v[n3:2 * n3]).reshape(3, Nr, Nz)
        o = 2 * n3
        s = (v[o:o + self.ns] + 1j * v[o + self.ns:o + 2 * self.ns]).reshape(Nr, Nz); o += 2 * self.ns
        Ar = v[o:o + self.nar].reshape(Nr - 1, Nz); o += self.nar
        Az = v[o:o + self.naz].reshape(Nr, Nz - 1)
        return psi, s, Ar, Az

    def on(self, t):
        return self.terms is None or t in self.terms

    # ---- energy and gradient ------------------------------------------------
    def energy_grad(self, v, parts=False):
        psi, s, Ar, Az = self.unpack(v)
        h, e, eta, beta, mu2, lam, n, Q = self.h, self.e, self.eta, self.beta, self.mu2, self.lam, self.n, self.Q
        ws, wr = self.ws, self.wr
        gpsi = np.zeros_like(psi); gs = np.zeros_like(s); gAr = np.zeros_like(Ar); gAz = np.zeros_like(Az)
        P = {}
        # psi kinetic: rho links (weight wr) and z links (weight ws)
        if self.on('psi_kin'):
            Ek = 0.0
            U = np.exp(-1j * e * h * Ar)
            a = psi[:, :-1, :]; b = psi[:, 1:, :]
            D = (U * b - a) / h
            Ek += np.sum(wr * np.abs(D) ** 2)
            gpsi[:, :-1, :] += -2 * D / h * wr
            gpsi[:, 1:, :] += 2 * np.conj(U) * D / h * wr
            gAr += np.sum(e * h * (-2 * np.imag(U * b * np.conj(a)) / h ** 2) * wr, axis=0)
            U = np.exp(-1j * e * h * Az)
            a = psi[:, :, :-1]; b = psi[:, :, 1:]
            D = (U * b - a) / h
            Ek += np.sum(ws * np.abs(D) ** 2)
            gpsi[:, :, :-1] += -2 * D / h * ws
            gpsi[:, :, 1:] += 2 * np.conj(U) * D / h * ws
            gAz += np.sum(e * h * (-2 * np.imag(U * b * np.conj(a)) / h ** 2) * ws, axis=0)
            P['psi_kin'] = Ek
        rho2 = np.abs(psi) ** 2
        if self.on('psi_pot'):
            P['psi_pot'] = float(np.sum(ws * 0.5 * (rho2 - 1) ** 2))
            gpsi += 2 * (rho2 - 1) * psi * ws
        if self.on('josephson') and eta:
            Ej = 0.0
            for i in range(3):
                for j in range(i + 1, 3):
                    Ej -= eta * np.sum(ws * np.real(psi[i] * np.conj(psi[j])))
                    gpsi[i] -= eta * ws * psi[j]
                    gpsi[j] -= eta * ws * psi[i]
            P['josephson'] = Ej
        if self.on('magnetic'):
            F = (Az[1:, :] - Az[:-1, :] - Ar[:, 1:] + Ar[:, :-1]) / h     # plaquette (i..i+1, j..j+1)
            P['magnetic'] = float(np.sum(wr * 0.5 * F ** 2))
            g = wr * F / h
            gAz[1:, :] += g; gAz[:-1, :] -= g; gAr[:, 1:] -= g; gAr[:, :-1] += g
        s2 = np.abs(s) ** 2
        if self.on('sig_grad'):
            Dr = (s[1:, :] - s[:-1, :]) / h; Dz = (s[:, 1:] - s[:, :-1]) / h
            P['sig_grad'] = float(np.sum(wr * np.abs(Dr) ** 2) + np.sum(ws * np.abs(Dz) ** 2))
            gs[:-1, :] += -2 * Dr / h * wr; gs[1:, :] += 2 * Dr / h * wr
            gs[:, :-1] += -2 * Dz / h * ws; gs[:, 1:] += 2 * Dz / h * ws
        if self.on('sig_wind') and n:
            c = (n * n / self.rho ** 2)[:, None]
            P['sig_wind'] = float(np.sum(ws * c * s2))
            gs += 2 * c * s * ws
        if self.on('sig_pot'):
            P['sig_pot'] = float(np.sum(ws * (-mu2 * s2 + 0.5 * lam * s2 ** 2)))
            gs += 2 * (-mu2 + lam * s2) * s * ws
        if self.on('coupling'):
            sp = np.sum(rho2, axis=0)
            P['coupling'] = float(beta * np.sum(ws * s2 * sp))
            gs += 2 * beta * sp * s * ws
            gpsi += 2 * beta * s2[None] * psi * ws
        if self.on('charge') and Q:
            I = float(np.sum(ws * s2))
            P['charge'] = Q * Q / (4 * I)
            gs += -(Q * Q / (4 * I * I)) * 2 * s * ws
        E = sum(P.values())
        if self.terms is None:
            E -= self.Evac                         # E above the true vacuum on this grid
        grad = np.concatenate([gpsi.real.ravel(), gpsi.imag.ravel(), gs.real.ravel(), gs.imag.ravel(),
                               gAr.ravel(), gAz.ravel()])
        if parts:
            return E, grad, P
        return E, grad

    # ---- observables ----------------------------------------------------------
    def windings(self, psi, Ar, Az):
        """Gauge-invariant winding of each strand around each plaquette, counter-clockwise in (rho, z)."""
        e, h = self.e, self.h
        lr = np.angle(np.conj(psi[:, :-1, :]) * np.exp(-1j * e * h * Ar) * psi[:, 1:, :])   # (3, Nr-1, Nz)
        lz = np.angle(np.conj(psi[:, :, :-1]) * np.exp(-1j * e * h * Az) * psi[:, :, 1:])   # (3, Nr, Nz-1)
        circ = lr[:, :, :-1] + lz[:, 1:, :] - lr[:, :, 1:] - lz[:, :-1, :]
        flux = e * h * (Ar[:, :-1] + Az[1:, :] - Ar[:, 1:] - Az[:-1, :])
        return np.rint((circ + flux[None]) / (2 * np.pi)).astype(int)

    def observables(self, v):
        psi, s, Ar, Az = self.unpack(v)
        E, g, P = self.energy_grad(v, parts=True)
        h, ws = self.h, self.ws
        s2 = np.abs(s) ** 2; I = float(np.sum(ws * s2))
        W = self.windings(psi, Ar, Az)
        pr = (np.arange(self.Nr - 1) + 1.0) * h; pz = self.z[:-1] + 0.5 * h     # plaquette centres
        zeros = []
        for k in range(3):
            ii, jj = np.nonzero(W[k])
            zeros.append([[float(pr[a]), float(pz[b]), int(W[k][a, b])] for a, b in zip(ii, jj)])
        net = [int(W[k].sum()) for k in range(3)]
        # R_f: rho of the winding zeros (mean over all zeros of all three strands), if every strand has exactly one +1 zero
        allz = [z for zz in zeros for z in zz]
        one_each = all(len(zz) == 1 for zz in zeros)
        R_core = float(np.mean([z[0] for z in allz])) if allz else None
        z_core = float(np.mean([z[1] for z in allz])) if allz else None
        R_sig = float(np.sum(ws * self.R * s2) / I) if I > 0 else None
        z_sig = float(np.sum(ws * self.Z * s2) / I) if I > 0 else None
        smax = float(np.sqrt(s2.max()))
        r_sig = float(np.sqrt(h * h * np.count_nonzero(s2 > 0.5 * s2.max()) / np.pi)) if s2.max() > 0 else None
        mpsi = np.mean(np.abs(psi) ** 2, axis=0)
        r_psi = float(np.sqrt(h * h * np.count_nonzero(mpsi < 0.5 * (1 + self.eta)) / np.pi))
        im = np.unravel_index(np.argmin(mpsi), mpsi.shape)
        edge = (self.R > self.rho_max - LEAK_W) | (np.abs(self.Z) > self.zmax - LEAK_W)
        leak = float(np.sum((ws * s2)[edge]) / I) if I > 0 else None
        mvac = np.sqrt(3 * self.beta * (1 + self.eta) - self.mu2)
        om = self.Q / (2 * I) if I > 0 else None
        Rf = R_core if R_core is not None else None
        kk = self.n / Rf if (Rf and self.n) else 0.0
        return dict(E=float(E), parts={k_: float(v_) for k_, v_ in P.items()}, grad_max=float(np.max(np.abs(g))),
                    winding_zeros=zeros, net_winding=net, one_zero_per_strand=bool(one_each),
                    R_core=R_core, z_core=z_core, R_sigma_weighted=R_sig, z_sigma_weighted=z_sig,
                    sigma_max=smax, r_sigma=r_sig, r_psi=r_psi,
                    min_mean_psi2=float(mpsi[im]), min_mean_psi2_at=[float(self.rho[im[0]]), float(self.z[im[1]])],
                    I=I, omega=om, m_vac=float(mvac), omega_over_mvac=(om / mvac if om is not None else None),
                    k_ring=kk, omega2_lt_mvac2_plus_k2=(bool(om ** 2 < mvac ** 2 + kk ** 2) if om is not None else None),
                    leak_frac=leak, mvacQ=float(mvac * self.Q),
                    E_lt_mvacQ=bool(E < mvac * self.Q) if self.Q else None)

    # ---- minimizer (gl3.minimize options) -----------------------------------------
    def minimize(self, v0, maxiter=MAXITER, gtol=GTOL, every=EVERY, log=None):
        hist = []; it = [0]; t0 = time.time()

        def cb(xk):
            it[0] += 1
            if it[0] % every == 0:
                o = self.observables(xk); o['it'] = it[0]; o['t'] = time.time() - t0
                hist.append(slim(o))
                if log:
                    log(f"it={it[0]} E={o['E']:.4f} R_core={fmt(o['R_core'])} R_sig={fmt(o['R_sigma_weighted'])} "
                        f"I={o['I']:.3f} w/m={fmt(o['omega_over_mvac'])} leak={fmt(o['leak_frac'])} "
                        f"net={o['net_winding']} |g|={o['grad_max']:.2e} t={o['t']:.0f}s")
        o = self.observables(v0); o['it'] = 0; o['t'] = 0.0; hist.insert(0, slim(o))
        r = minimize(self.energy_grad, v0, jac=True, method='L-BFGS-B', callback=cb,
                     options=dict(maxiter=maxiter, maxfun=2 * maxiter, gtol=gtol, ftol=FTOL))
        return r, hist


def fmt(x):
    return 'None' if x is None else f'{x:.4f}'


def slim(o):
    d = dict(o); d['winding_zeros'] = [len(z) for z in o['winding_zeros']]
    return d


# ---- straight string at b3_d1, (k*, q*) (option4_phase0's functional) -------------------
def selected():
    """§9.2 replacement rule applied to phase0_results.json: stable (interp and direct d2E/dR2 > 0, same sign),
    R_eq/r_sigma >= 3, smallest omega*/m_vac."""
    d = json.load(open('phase0_results.json'))
    best = None
    for p in d['points']:
        for c in p.get('summary', {}).get('sign_changes', []):
            dd = c.get('d2E_dR2_direct')
            if c['stable_R'] and dd is not None and dd > 0 and c['R_eq_over_r_sigma'] >= 3:
                if best is None or c['omega_star_over_mvac'] < best[1]['omega_star_over_mvac']:
                    best = (p, c)
    p, c = best
    return dict(tag=p['tag'], beta=p['beta'], mu2=p['mu2'], lam=p['lam'], m_vac=p['m_vac'],
                k_star=c['k_star'], q_star=c['q_star'], omega_star_over_mvac=c['omega_star_over_mvac'],
                r_sigma_star=c['r_sigma_star'])


def straight_string(sel):
    import option4_phase0 as p0, option4_design as od
    rb = od.solve((0, 0, 1, 0), with_s=False)
    x0 = np.concatenate([rb.x, 0.6 * np.exp(-od.r[:od.M] ** 2 / 2)])      # Phase 0's first-solve warm start
    o, x = p0.solve_line((sel['beta'], sel['mu2'], sel['lam']), sel['k_star'], sel['q_star'], x0)
    f, a, s = od.unpack(x, True)
    return dict(r=od.r.tolist(), f=f.tolist(), a=a.tolist(), s=s.tolist(), solve=o,
                warm_start='bare string (option4_design.solve, sigma=0) + 0.6 exp(-r^2/2), as Phase 0 first solve',
                bare_converged=bool(rb.success))


# ---- starts ---------------------------------------------------------------------------
def start_state(ax, prof, kind, R0):
    r = np.asarray(prof['r']); f = np.asarray(prof['f']); a = np.asarray(prof['a']); sp = np.asarray(prof['s'])
    h, e = ax.h, ax.e
    F = lambda d: np.interp(d, r, f, right=FV)
    Aa = lambda d: np.interp(d, r, a, right=1.0)
    S = lambda d: np.interp(d, r, sp, right=0.0)
    R, Z = ax.R, ax.Z
    d = np.hypot(R - R0, Z) if R0 is not None else None
    if kind in ('wound', 'unwound'):
        chi = np.arctan2(Z, R - R0)
        ph = np.exp(1j * chi) if kind == 'wound' else 1.0
        psi = np.broadcast_to(F(d) * ph, (3,) + R.shape).astype(complex).copy()
        s = S(d).astype(complex)
        if kind == 'wound':
            # A = a(d)/(e d) chi_hat, chi_hat = (-z/d, (rho - R0)/d), evaluated at link midpoints
            def Avec(rr, zz):
                dd = np.hypot(rr - R0, zz); dd = np.where(dd < 1e-12, 1e-12, dd)
                amp = Aa(dd) / (e * dd)
                return amp * (-zz / dd), amp * ((rr - R0) / dd)
            rl = 0.5 * (R[1:, :] + R[:-1, :]); zl = Z[1:, :]
            Ar = Avec(rl, zl)[0]
            rl = R[:, 1:]; zl = 0.5 * (Z[:, 1:] + Z[:, :-1])
            Az = Avec(rl, zl)[1]
        else:
            Ar = np.zeros((ax.Nr - 1, ax.Nz)); Az = np.zeros((ax.Nr, ax.Nz - 1))
    elif kind == 'ball':
        psi = np.full((3,) + R.shape, FV, complex)
        s = np.where(np.hypot(R, Z) < 4.0, np.sqrt(ax.mu2 / ax.lam), 0.0).astype(complex)
        Ar = np.zeros((ax.Nr - 1, ax.Nz)); Az = np.zeros((ax.Nr, ax.Nz - 1))
    return ax.pack(psi, s, Ar, Az)


# ---- gradient check (gl3.check_grad definition) -------------------------------------------
def check_grad(ax, seed=0, terms=None, ncoord=40, eps=1e-6, order=2):
    """order=2: exactly gl3.check_grad (central FD, step eps). order=4: five-point stencil (truncation O(eps^4)),
    used with a larger step to get below the floating-point floor of the order-2 check on large energies."""
    ax.terms = terms
    rng = np.random.default_rng(seed)
    v = rng.normal(size=ax.size) * 0.5
    E, g = ax.energy_grad(v)
    if terms is not None:
        nz = np.nonzero(g)[0]
        idx = rng.choice(nz, min(ncoord, nz.size), replace=False)
    else:
        idx = rng.choice(v.size, ncoord, replace=False)
    worst = 0.0
    for i in idx:
        vp = v.copy(); vp[i] += eps; vm = v.copy(); vm[i] -= eps
        if order == 2:
            fd = (ax.energy_grad(vp)[0] - ax.energy_grad(vm)[0]) / (2 * eps)
        else:
            vp2 = v.copy(); vp2[i] += 2 * eps; vm2 = v.copy(); vm2[i] -= 2 * eps
            fd = (-ax.energy_grad(vp2)[0] + 8 * ax.energy_grad(vp)[0] - 8 * ax.energy_grad(vm)[0]
                  + ax.energy_grad(vm2)[0]) / (12 * eps)
        worst = max(worst, abs(fd - g[i]) / (abs(fd) + 1e-8))
    ax.terms = None
    return float(worst)


def run_list(sel):
    k, q = sel['k_star'], sel['q_star']
    Q7 = 2 * np.pi * (7 / k) * q; Q10 = 2 * np.pi * (10 / k) * q
    R7, R10 = 7 / k, 10 / k
    return [
        dict(name='main_n7_R1.0', n=7, Q=Q7, kind='wound', R0=R7, role='main'),
        dict(name='main_n7_R1.5', n=7, Q=Q7, kind='wound', R0=1.5 * R7, role='main'),
        dict(name='main_n10_R1.0', n=10, Q=Q10, kind='wound', R0=R10, role='main'),
        dict(name='main_n10_R1.5', n=10, Q=Q10, kind='wound', R0=1.5 * R10, role='main'),
        dict(name='Ca_n0_Q0', n=0, Q=0.0, kind='wound', R0=R7, role='C-a'),
        dict(name='Cb_n7_Q0', n=7, Q=0.0, kind='wound', R0=R7, role='C-b'),
        dict(name='Cc_n0_Q7', n=0, Q=Q7, kind='wound', R0=R7, role='C-c'),
        dict(name='Cd_n7', n=7, Q=Q7, kind='unwound', R0=R7, role='C-d'),
        dict(name='Cd_n10', n=10, Q=Q10, kind='unwound', R0=R10, role='C-d'),
        dict(name='Ce_Q7', n=0, Q=Q7, kind='ball', R0=None, role='C-e'),
        dict(name='Ce_Q10', n=0, Q=Q10, kind='ball', R0=None, role='C-e'),
    ]


def do_run(args):
    spec, sel, prof = args
    ax = Axial(sel['beta'], sel['mu2'], sel['lam'], spec['n'], spec['Q'])
    v0 = start_state(ax, prof, spec['kind'], spec['R0'])
    lines = []
    def log(m):
        m = f"[{spec['name']}] {m}"; lines.append(m); print(m, flush=True)
    t0 = time.time()
    r, hist = ax.minimize(v0, log=log)
    fin = ax.observables(r.x)
    psi, s, Ar, Az = ax.unpack(r.x)
    np.savez_compressed(f"phase1_{spec['name']}.npz", psi=psi, s=s, A_rho=Ar, A_z=Az, rho=ax.rho, z=ax.z,
                        n=spec['n'], Q=spec['Q'], beta=ax.beta, mu2=ax.mu2, lam=ax.lam, h=ax.h)
    out = dict(spec=spec, nit=int(r.nit), nfev=int(r.nfev), message=str(r.message), success=bool(r.success),
               hit_maxiter=bool(r.nit >= MAXITER), seconds=time.time() - t0, final=fin, history=hist)
    log(f"done: nit={r.nit} nfev={r.nfev} msg={r.message} E={fin['E']:.4f} R_core={fmt(fin['R_core'])} "
        f"zeros={[len(z) for z in fin['winding_zeros']]} R_sig={fmt(fin['R_sigma_weighted'])} "
        f"w/m={fmt(fin['omega_over_mvac'])} leak={fmt(fin['leak_frac'])} {out['seconds']:.0f}s")
    return out


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'run'
    print(f'Python {platform.python_version()}, NumPy {np.__version__}, SciPy {scipy.__version__}, '
          f'{os.cpu_count()} cores', flush=True)
    sel = selected()
    print('selection (§9.2 rule on phase0_results.json):', json.dumps(sel), flush=True)
    if cmd == 'gradcheck':
        res = {}
        for label, kw in (('small grid 8x9', dict(rho_max=2.0, zmax=1.0)), ('full grid', {})):
            ax = Axial(sel['beta'], sel['mu2'], sel['lam'], 7, 2889.0, **kw)
            res[label] = dict(Nr=ax.Nr, Nz=ax.Nz, unknowns=ax.size)
            for tag, kw2 in (('gl3 definition (order 2, eps 1e-6)', dict(order=2, eps=1e-6)),
                             ('order 4, eps 1e-3', dict(order=4, eps=1e-3))):
                r_all = check_grad(ax, seed=0, **kw2)
                r_wind = check_grad(ax, seed=1, terms={'sig_wind'}, **kw2)
                r_q = check_grad(ax, seed=2, terms={'charge'}, **kw2)
                res[label][tag] = dict(full=r_all, n2_over_rho2_only=r_wind, Q2_over_4I_only=r_q)
                print(f'gradient check [{label}, Nr={ax.Nr}, Nz={ax.Nz}, {ax.size} unknowns, n=7, Q=2889, {tag}]: '
                      f'full functional worst rel err {r_all:.3e}; n^2/rho^2 term only {r_wind:.3e}; '
                      f'Q^2/(4I) term only {r_q:.3e}', flush=True)
        json.dump(res, open('phase1_gradcheck.json', 'w'), indent=1)
    elif cmd == 'profiles':
        t0 = time.time()
        prof = straight_string(sel)
        prof['selection'] = sel
        print('straight string:', json.dumps(prof['solve']), f'{time.time() - t0:.1f}s', flush=True)
        json.dump(prof, open('phase1_profiles.json', 'w'))
    elif cmd == 'run':
        from multiprocessing import Pool
        prof = json.load(open('phase1_profiles.json'))
        runs = run_list(sel)
        only = sys.argv[2:]
        if only:
            runs = [r for r in runs if r['name'] in only]
        for r in runs:
            print('run spec:', json.dumps(r), flush=True)
        t0 = time.time()
        with Pool(min(4, os.cpu_count())) as pool:
            outs = pool.map(do_run, [(r, sel, prof) for r in runs], chunksize=1)
        res = dict(meta=dict(label='Exploration, post-hoc selection (PREREG_option4 §9)', grid=dict(h=H, rho_max=RHO_MAX, zmax=ZMAX),
                             e=E_CH, eta=ETA, minimizer=dict(method='L-BFGS-B', maxiter=MAXITER, maxfun=2 * MAXITER, gtol=GTOL, ftol=FTOL),
                             history_every=EVERY, leak_band=LEAK_W,
                             software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)),
                   selection=sel, runs={o['spec']['name']: o for o in outs}, total_seconds=time.time() - t0)
        fn = 'phase1_results.json' if not only else 'phase1_results_partial.json'
        json.dump(res, open(fn, 'w'), default=float)
        print(f'total {time.time() - t0:.0f} s', flush=True)
