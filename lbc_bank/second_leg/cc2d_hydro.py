#!/usr/bin/env python3
"""cc2d_hydro -- static hydrodynamic route (task Q-A', step kernel, g = 22) for the second leg.

Units hbar = m = 1, R = 1, reference mean density rho = 1.  2D GP crystal, triangular lattice, one droplet
per primitive cell.  Everything here is static (no excitations).

Quantities (SPEC section 4; dispatch Sec. 3 Q-A'):
  e(rho, eps) = E_cell / A_eps,  cell rows a_i -> (I + eps) a_i,  N_cell = rho * A_eps,
  reference = relaxed cell (a = a*, rho = 1).
  alpha = d2e/drho2 (eps = 0);  M = C_xxxx = d2e/deps_xx2;  C_xxyy = d2e/deps_xx deps_yy;
  mu_shear = C_xyxy = (1/4) d2e/ds2 with eps_xy = eps_yx = s;  gamma = d2e/drho deps_xx.
  f_s from linear response 1 - (2/N) <d_x psi0| L^-1 |d_x psi0> and from phase-twist energies.
  Then a, b, c_minus, c_plus, c_T, c_*^2, F_minus, static share of the lower branch.

Routes
  (FD) finite strains / densities at fixed plane-wave index set (Galerkin, fractional coordinates), ground
       states by the leg library cc2d (L-BFGS + Newton-Krylov, no imaginary time), energies re-evaluated
       with this file's own plane-wave functional (class PW, its own FFT box 4R+2, its own kernel code);
       central differences with steps h and h/2 + Richardson.
  (LR) independent analytic route: with x the coefficient vector (sum |x|^2 = rho) and
       F(x, eps) = sum 1/2 |G_eps|^2 x_G^2 + 1/2 sum_K Uhat(|K_eps|) |rho_K|^2  (rho_K is eps independent),
       the bordered (constrained) second-order response gives
         alpha  = 1 / (2 x.A^-1 x),
         gamma_a = (x.A^-1 beta_a) / (x.A^-1 x),
         C_ab   = d2F_ab|_x - 2 beta_a.A^-1 beta_b + 2 (x.A^-1 beta_a)(x.A^-1 beta_b)/(x.A^-1 x),
       with A = L + 2X (dense, on the inversion-even real subspace), beta_a = (dH/deps_a) psi0.
  (fs) dense L^-1 on the odd real subspace (linear response); twist energies E(k) by this file's own dense
       Newton in the real-coefficient subspace (inversion x complex conjugation symmetric), Richardson in k^2;
       cc2d.superfluid_fraction (projected CG + cc2d Newton) as a further cross-check.

CLI (run from this directory; results cached in WORK):
  python3 cc2d_hydro.py astar  [N]     own a* (root of the analytic stress), compare cc2d.optimize_a
  python3 cc2d_hydro.py fd     [N]     finite-difference moduli at the relaxed cell
  python3 cc2d_hydro.py lr     [N]     analytic linear-response moduli, dN/dmu, f_s (LR)
  python3 cc2d_hydro.py twist  [N]     twist energies (own dense Newton) + cc2d.superfluid_fraction
  python3 cc2d_hydro.py collect        hydrodynamic formulas, checks, convergence -> qa_prime_results.json
  python3 cc2d_hydro.py compare        (after collect) cross-check vs this leg's Q-A BdG point g = 22
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '2'
import sys
import json
import time
import math
import numpy as np
from numpy.fft import fft2, ifft2
import scipy.linalg as sla
from scipy.special import j1, jv
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cc2d  # noqa: E402

WORK = '/tmp/claude-0/-home-user-gifgaf0-github-io/6eab36f5-c943-5609-bc1f-38f855730ac1/scratchpad/work'
OUTJSON = os.path.join(HERE, 'qa_prime_results.json')
G_COUPLING = 22.0
SQ3 = math.sqrt(3.0)
TWOPI = 2.0 * math.pi
RHO0 = 1.0
STRAIN_STEPS = (2e-3, 1e-3)      # h, h/2 for strains
RHO_STEPS = (2e-3, 1e-3)         # h, h/2 for density
GS_TOL = 1e-12                   # GP residual tolerance for the FD ground states


def cache(name):
    return os.path.join(WORK, 'qap_' + name)


def jdump(obj, path):
    with open(path, 'w') as f:
        json.dump(cc2d.jsonable(obj), f, indent=1)


def jload(path):
    with open(path) as f:
        return json.load(f)


# ----------------------------------------------------------------------------------------------------------
# own kernel code (step):  Uhat(k) = 2 pi g J1(k)/k ;  V(s) = Uhat(sqrt s):  V' = -pi g J2/k^2,
#                          V'' = pi g J3 / (2 k^3)
# ----------------------------------------------------------------------------------------------------------
class StepKernel:
    def __init__(self, g):
        self.g = float(g)

    def u(self, k):
        k = np.asarray(k, float)
        ks = np.where(k > 1e-6, k, 1.0)
        big = TWOPI * self.g * j1(ks) / ks
        small = math.pi * self.g * (1.0 - k * k / 8.0 + k ** 4 / 192.0)
        return np.where(k > 1e-6, big, small)

    def v1(self, k):
        """dUhat/d(k^2)."""
        k = np.asarray(k, float)
        ks = np.where(k > 1e-6, k, 1.0)
        big = -math.pi * self.g * jv(2, ks) / ks ** 2
        small = -math.pi * self.g * (1.0 / 8.0 - k * k / 96.0)
        return np.where(k > 1e-6, big, small)

    def v2(self, k):
        """d2Uhat/d(k^2)^2."""
        k = np.asarray(k, float)
        ks = np.where(k > 1e-6, k, 1.0)
        big = math.pi * self.g * jv(3, ks) / (2.0 * ks ** 3)
        small = math.pi * self.g * (1.0 / 96.0 - k * k / 1536.0)
        return np.where(k > 1e-6, big, small)


# strain basis: 'xx' = diag(1,0), 'yy' = diag(0,1), 'xy' = [[0,1],[1,0]] (eps_xy = eps_yx = s)
SBASIS = {'xx': np.array([[1.0, 0.0], [0.0, 0.0]]),
          'yy': np.array([[0.0, 0.0], [0.0, 1.0]]),
          'xy': np.array([[0.0, 1.0], [1.0, 0.0]])}
SNAMES = ('xx', 'yy', 'xy')


def qform(E, gx, gy):
    return E[0, 0] * gx * gx + (E[0, 1] + E[1, 0]) * gx * gy + E[1, 1] * gy * gy


def strained_cell(cell, eps):
    """rows a_i -> (I + eps) a_i."""
    return np.asarray(cell, float) @ (np.eye(2) + np.asarray(eps, float)).T


# ----------------------------------------------------------------------------------------------------------
# own plane-wave functional on a fixed integer index set (fractional coordinates)
# ----------------------------------------------------------------------------------------------------------
class PW:
    """psi(r) = sum_G c_G exp(i G.r) on the index set (mi, ni);  sum |c|^2 = rho.
    F = E_cell / A = sum 1/2 |G+k|^2 |c_G|^2 + 1/2 sum_K Uhat(|K|) |rho_K|^2.
    Products on a P x P box, P = 4R + 2 (R = max index): rho_K exact and the projection of (Phi psi)
    back onto the index set exact (aliases of |index| <= 3R land at distance >= P > 4R)."""

    def __init__(self, mi, ni, kern):
        self.mi = np.asarray(mi, int)
        self.ni = np.asarray(ni, int)
        self.n = self.mi.size
        self.R = R = int(max(np.abs(self.mi).max(), np.abs(self.ni).max()))
        self.P = P = 4 * R + 2
        self.ib = self.mi % P
        self.jb = self.ni % P
        f = np.rint(np.fft.fftfreq(P) * P).astype(int)
        self.Km, self.Kn = np.meshgrid(f, f, indexing='ij')
        self.kern = kern
        lut = -np.ones((2 * R + 1, 2 * R + 1), int)
        lut[self.mi + R, self.ni + R] = np.arange(self.n)
        self.neg = lut[-self.mi + R, -self.ni + R]
        if np.any(self.neg < 0):
            raise ValueError('index set not inversion symmetric')
        self.zero = int(np.where((self.mi == 0) & (self.ni == 0))[0][0])
        self.rep = np.where((self.mi > 0) | ((self.mi == 0) & (self.ni > 0)))[0]
        self.nrep = self.rep.size
        self.neven = 1 + self.nrep

    # geometry --------------------------------------------------------------------------------------
    def geometry(self, cell):
        cell = np.asarray(cell, float)
        B = TWOPI * np.linalg.inv(cell).T          # rows b_j, a_i . b_j = 2 pi delta_ij
        gx = self.mi * B[0, 0] + self.ni * B[1, 0]
        gy = self.mi * B[0, 1] + self.ni * B[1, 1]
        kx = self.Km * B[0, 0] + self.Kn * B[1, 0]
        ky = self.Km * B[0, 1] + self.Kn * B[1, 1]
        k = np.sqrt(kx * kx + ky * ky)
        U = self.kern.u(k)
        U[self.Km == -self.P // 2] = 0.0           # never populated (|K index| <= 2R < P/2)
        U[self.Kn == -self.P // 2] = 0.0
        return {'cell': cell, 'B': B, 'A': abs(np.linalg.det(cell)), 'gx': gx, 'gy': gy,
                'kx': kx, 'ky': ky, 'k': k, 'U': U}

    # transforms (batched over leading axes) ---------------------------------------------------------
    def tobox(self, c):
        c = np.asarray(c)
        buf = np.zeros(c.shape[:-1] + (self.P, self.P), dtype=complex)
        buf[..., self.ib, self.jb] = c
        return ifft2(buf, axes=(-2, -1)) * (self.P * self.P)

    def frombox(self, f):
        return fft2(f, axes=(-2, -1))[..., self.ib, self.jb] / (self.P * self.P)

    # functional --------------------------------------------------------------------------------------
    def evaluate(self, geo, c, kvec=(0.0, 0.0)):
        c = np.asarray(c, complex)
        kin = 0.5 * ((geo['gx'] + kvec[0]) ** 2 + (geo['gy'] + kvec[1]) ** 2)
        psi = self.tobox(c)
        rhoK = fft2(np.abs(psi) ** 2) / (self.P * self.P)
        Phi = (ifft2(geo['U'] * rhoK) * (self.P * self.P)).real
        Fkin = float(np.sum(kin * np.abs(c) ** 2))
        Fint = 0.5 * float(np.sum(geo['U'] * np.abs(rhoK) ** 2))
        Hc = kin * c + self.frombox(Phi * psi)
        nn = float(np.sum(np.abs(c) ** 2))
        mu = float(np.real(np.vdot(c, Hc))) / nn
        r = Hc - mu * c
        return {'F': Fkin + Fint, 'Fkin': Fkin, 'Fint': Fint, 'mu': mu, 'Hc': Hc, 'r': r,
                'resid': float(np.sqrt(np.sum(np.abs(r) ** 2) / nn)), 'rhoK': rhoK, 'Phi': Phi, 'psi': psi,
                'kin': kin, 'c': c, 'norm': nn, 'kvec': kvec}

    def hess(self, geo, ev, D):
        """real-linear constrained Hessian/2 applied to rows of D: (H - mu) d + P[psi U*(2 Re(conj(psi) d))]."""
        D = np.atleast_2d(D)
        pd = self.tobox(D)
        w = 2.0 * np.real(np.conj(ev['psi'])[None] * pd)
        Uw = ifft2(geo['U'][None] * fft2(w, axes=(-2, -1)), axes=(-2, -1)).real
        return (ev['kin'] - ev['mu'])[None] * D + self.frombox(ev['Phi'][None] * pd + ev['psi'][None] * Uw)

    def lop(self, geo, ev, D):
        """L = H - mu applied to rows of D."""
        D = np.atleast_2d(D)
        pd = self.tobox(D)
        return (ev['kin'] - ev['mu'])[None] * D + self.frombox(ev['Phi'][None] * pd)

    # strain derivatives of F at fixed coefficients --------------------------------------------------
    def strain_derivs(self, geo, ev):
        """first/second derivatives of F at fixed x w.r.t. strain amplitudes (xx, yy, xy), and
        beta_a = (dH/deps_a) psi0."""
        c, rhoK = ev['c'], ev['rhoK']
        gx, gy = geo['gx'], geo['gy']
        kx, ky, k = geo['kx'], geo['ky'], geo['k']
        V1 = self.kern.v1(k)
        V2 = self.kern.v2(k)
        mask_nyq = (self.Km == -self.P // 2) | (self.Kn == -self.P // 2)
        V1[mask_nyq] = 0.0
        V2[mask_nyq] = 0.0
        c2 = np.abs(c) ** 2
        r2 = np.abs(rhoK) ** 2
        qG = {a: qform(SBASIS[a], gx, gy) for a in SNAMES}
        qK = {a: qform(SBASIS[a], kx, ky) for a in SNAMES}
        dF, d2F, beta = {}, {}, {}
        for a in SNAMES:
            # d|G|^2/deps_a = -2 G.E_a.G
            dF[a] = 0.5 * float(np.sum(-2.0 * qG[a] * c2)) + 0.5 * float(np.sum(V1 * (-2.0 * qK[a]) * r2))
            dPhi = (ifft2(V1 * (-2.0 * qK[a]) * rhoK) * (self.P * self.P)).real
            beta[a] = 0.5 * (-2.0 * qG[a]) * c + self.frombox(dPhi * ev['psi'])
        for i, a in enumerate(SNAMES):
            for b in SNAMES[i:]:
                Eab = SBASIS[a] @ SBASIS[b] + SBASIS[b] @ SBASIS[a]
                pG = qform(Eab, gx, gy)
                pK = qform(Eab, kx, ky)
                # d2|G|^2 = 3 G.(E_a E_b + E_b E_a).G
                t = 0.5 * float(np.sum(3.0 * pG * c2))
                t += 0.5 * float(np.sum((V2 * 4.0 * qK[a] * qK[b] + V1 * 3.0 * pK) * r2))
                d2F[a + ',' + b] = t
                d2F[b + ',' + a] = t
        return dF, d2F, beta

    # subspace maps -----------------------------------------------------------------------------------
    def even_from(self, y):
        """even real function coefficients (c_G = c_-G real) from rep vector y (len neven)."""
        c = np.zeros(self.n, complex)
        c[self.zero] = y[0]
        c[self.rep] = y[1:] / math.sqrt(2.0)
        c[self.neg[self.rep]] = y[1:] / math.sqrt(2.0)
        return c

    def even_to(self, r):
        r = np.atleast_2d(r)
        out = np.empty((r.shape[0], self.neven))
        out[:, 0] = r[:, self.zero].real
        out[:, 1:] = (r[:, self.rep].real + r[:, self.neg[self.rep]].real) / math.sqrt(2.0)
        return out

    def odd_from(self, y):
        c = np.zeros(self.n, complex)
        c[self.rep] = 1j * y / math.sqrt(2.0)
        c[self.neg[self.rep]] = -1j * y / math.sqrt(2.0)
        return c

    def odd_to(self, r):
        r = np.atleast_2d(r)
        return (r[:, self.rep].imag - r[:, self.neg[self.rep]].imag) / math.sqrt(2.0)

    def even_basis_rows(self, j0, j1_):
        rows = np.zeros((j1_ - j0, self.n), complex)
        for t, j in enumerate(range(j0, j1_)):
            if j == 0:
                rows[t, self.zero] = 1.0
            else:
                p = self.rep[j - 1]
                rows[t, p] = 1.0 / math.sqrt(2.0)
                rows[t, self.neg[p]] = 1.0 / math.sqrt(2.0)
        return rows

    def odd_basis_rows(self, j0, j1_):
        rows = np.zeros((j1_ - j0, self.n), complex)
        for t, j in enumerate(range(j0, j1_)):
            p = self.rep[j]
            rows[t, p] = 1j / math.sqrt(2.0)
            rows[t, self.neg[p]] = -1j / math.sqrt(2.0)
        return rows

    def dense_A_even(self, geo, ev, batch=96):
        n = self.neven
        A = np.empty((n, n))
        for j0 in range(0, n, batch):
            j1_ = min(n, j0 + batch)
            R = self.hess(geo, ev, self.even_basis_rows(j0, j1_))
            A[:, j0:j1_] = self.even_to(R).T
        asym = float(np.max(np.abs(A - A.T)) / np.max(np.abs(A)))
        return 0.5 * (A + A.T), asym

    def dense_L_odd(self, geo, ev, batch=96):
        n = self.nrep
        L = np.empty((n, n))
        for j0 in range(0, n, batch):
            j1_ = min(n, j0 + batch)
            R = self.lop(geo, ev, self.odd_basis_rows(j0, j1_))
            L[:, j0:j1_] = self.odd_to(R).T
        asym = float(np.max(np.abs(L - L.T)) / np.max(np.abs(L)))
        return 0.5 * (L + L.T), asym

    def dense_H_realcoef(self, geo, ev, batch=96):
        """constrained Hessian/2 on the real-coefficient subspace (basis e_G), and max |imag| leak."""
        n = self.n
        H = np.empty((n, n))
        leak = 0.0
        for j0 in range(0, n, batch):
            j1_ = min(n, j0 + batch)
            rows = np.zeros((j1_ - j0, n), complex)
            rows[np.arange(j1_ - j0), np.arange(j0, j1_)] = 1.0
            R = self.hess(geo, ev, rows)
            leak = max(leak, float(np.max(np.abs(R.imag))))
            H[:, j0:j1_] = R.real.T
        asym = float(np.max(np.abs(H - H.T)) / np.max(np.abs(H)))
        return 0.5 * (H + H.T), asym, leak


# ----------------------------------------------------------------------------------------------------------
# reference state / solver wrappers (cc2d is the minimiser)
# ----------------------------------------------------------------------------------------------------------
def kernel_cc():
    return cc2d.Kernel('step', G_COUPLING)


def solve(cell, N, rho, seed, mask, tol=GS_TOL):
    return cc2d.ground_state(cell, kernel_cc(), N=N, rho=rho, seed=seed, mask=mask, tol=tol)


def own_eval(pw, st):
    geo = pw.geometry(st.cell)
    ev = pw.evaluate(geo, st.c)
    return geo, ev


def stress_hex(pw, st):
    """analytic d e/d a at fixed rho for a hexagonal cell (Hellmann-Feynman, own code)."""
    geo, ev = own_eval(pw, st)
    dF, _, _ = pw.strain_derivs(geo, ev)
    a = float(np.linalg.norm(st.cell[0]))
    return (dF['xx'] + dF['yy']) / a, ev


def ref_path(N):
    return cache('ref_N%d.npz' % N)


def save_ref(st, N, extra):
    np.savez(ref_path(N), c=st.c, mi=st.grid.mi, ni=st.grid.ni, cell=st.cell, N=N, rho=st.rho,
             **{k: np.asarray(v) for k, v in extra.items()})


def load_ref(N):
    z = np.load(ref_path(N))
    kern = kernel_cc()
    grid = cc2d.Grid(z['cell'], int(z['N']), kern, mask=(z['mi'], z['ni']))
    st = cc2d.State(grid, z['c'].astype(complex), float(z['rho']))
    return st, z


# ----------------------------------------------------------------------------------------------------------
# step 1: own a*
# ----------------------------------------------------------------------------------------------------------
def cmd_astar(N=64):
    t0 = time.time()
    kern = kernel_cc()
    out = {'N': N, 'g': G_COUPLING}
    # coarse scan from a Gaussian seed (crystal side), then continuation
    st0 = cc2d.ground_state(cc2d.hex_cell(1.47), kern, N=N, tol=GS_TOL)
    mask = st0.grid.mask_index()
    pw = PW(mask[0], mask[1], StepKernel(G_COUPLING))
    states = {1.47: st0}

    def nearest(a):
        ak = min(states.keys(), key=lambda x: abs(x - a))
        return states[ak]

    def st_at(a):
        a = float(a)
        if a not in states:
            states[a] = solve(cc2d.hex_cell(a), N, RHO0, nearest(a), mask)
        return states[a]

    scan = []
    for a in np.arange(1.40, 1.561, 0.02):
        st = st_at(a)
        s, ev = stress_hex(pw, st)
        scan.append({'a': float(a), 'e_cc2d': st.e, 'e_own': ev['F'], 'dedA_own': s,
                     'dedA_cc2d_envelope': cc2d.dedA_envelope(st), 'resid': st.resid,
                     'contrast': st.contrast})
    out['scan'] = scan
    # bracket the stress root
    ss = [r['dedA_own'] for r in scan]
    i = [j for j in range(len(ss) - 1) if ss[j] < 0 <= ss[j + 1]][0]
    aL, aR = scan[i]['a'], scan[i + 1]['a']

    def fs(a):
        return stress_hex(pw, st_at(a))[0]

    ar = brentq(fs, aL, aR, xtol=1e-15, rtol=1e-15, maxiter=200)
    # polish: secant steps with fresh, tightly converged states
    hist = []
    for _ in range(3):
        st = st_at(ar)
        s = fs(ar)
        h = 1e-6 * ar
        sp, sm = fs(ar + h), fs(ar - h)
        slope = (sp - sm) / (2 * h)
        hist.append({'a': ar, 'stress': s, 'slope': slope})
        if abs(s / slope) < 1e-16 * ar:
            break
        ar = ar - s / slope
    out['astar_stress_root'] = ar
    out['stress_root_hist'] = hist
    st = st_at(ar)
    s, ev = stress_hex(pw, st)
    out['state'] = st.summary()
    out['e_own_at_astar'] = ev['F']
    out['e_cc2d_at_astar'] = st.e
    out['mu_own_at_astar'] = ev['mu']
    out['resid_own_at_astar'] = ev['resid']
    out['stress_at_astar'] = s
    # e(a) polynomial fit around the root (independent of the derivative formula)
    hs = np.array([-3, -2, -1, 0, 1, 2, 3], float) * 2e-3 * ar
    es = np.array([pw.evaluate(pw.geometry(st_at(ar + h).cell), st_at(ar + h).c)['F'] for h in hs])
    p6 = np.polyfit(hs / ar, es - es[3], 6)
    dp = np.polyder(p6)
    ddp = np.polyder(dp)
    x = 0.0
    for _ in range(60):
        x -= np.polyval(dp, x) / np.polyval(ddp, x)
    out['astar_poly6_fit'] = float(ar * (1.0 + x))
    out['d2e_da2_poly6'] = float(np.polyval(ddp, x) / ar ** 2)
    out['e_fit_points'] = {'a': (ar + hs).tolist(), 'e': es.tolist()}
    # cc2d's own optimizer, for comparison
    oc = cc2d.optimize_a(kern, ar * 0.97, ar * 1.03, N=N, seed=st, mask=mask, tol=GS_TOL)
    out['cc2d_optimize_a'] = {k: oc[k] for k in ('astar', 'a_parabolic_quartic5', 'a_parabolic_3pt',
                                                 'e_second_derivative_d2e_da2', 'a_dedA_root',
                                                 'e_per_area', 'mu') if k in oc}
    if 'a_dedA_root' in oc:
        out['rel_diff_own_root_vs_cc2d_dedA_root'] = (ar - oc['a_dedA_root']) / ar
    out['rel_diff_own_root_vs_cc2d_brent'] = (ar - oc['astar']) / ar
    out['rel_diff_own_root_vs_poly6'] = (ar - out['astar_poly6_fit']) / ar
    out['time'] = time.time() - t0
    save_ref(st, N, {'astar': ar})
    jdump(out, cache('astar_N%d.json' % N))
    print(json.dumps(cc2d.jsonable({k: v for k, v in out.items() if k not in ('scan', 'e_fit_points')}),
                     indent=1))


# ----------------------------------------------------------------------------------------------------------
# step 2: finite differences
# ----------------------------------------------------------------------------------------------------------
def fd_states(N):
    """all (rho, eps) evaluations needed; cached per N."""
    st0, z = load_ref(N)
    mask = st0.grid.mask_index()
    pw = PW(mask[0], mask[1], StepKernel(G_COUPLING))
    cell0 = st0.cell
    pts = {}

    def key(r, exx, eyy, s):
        return '%r|%r|%r|%r' % (r, exx, eyy, s)

    needed = [(1.0, 0.0, 0.0, 0.0)]
    for h in RHO_STEPS:
        needed += [(1.0 + h, 0, 0, 0), (1.0 - h, 0, 0, 0)]
    for h in STRAIN_STEPS:
        for sx in (h, -h):
            needed += [(1.0, sx, 0, 0), (1.0, 0, sx, 0), (1.0, 0, 0, sx), (1.0, sx, sx, 0)]
            for sy in (h, -h):
                needed += [(1.0, sx, sy, 0)]
            for sr in (h, -h):
                needed += [(1.0 + sr, sx, 0, 0)]
            needed += [(1.0, sx, -sx, 0)]
    cpath = cache('fd_N%d.json' % N)
    old = jload(cpath) if os.path.exists(cpath) else {}
    t0 = time.time()
    for (r, exx, eyy, s) in needed:
        kk = key(float(r), float(exx), float(eyy), float(s))
        if kk in old:
            pts[kk] = old[kk]
            continue
        eps = np.array([[exx, s], [s, eyy]], float)
        cell = strained_cell(cell0, eps)
        st = solve(cell, N, r, st0, mask)
        geo = pw.geometry(st.cell)
        ev = pw.evaluate(geo, st.c)
        pts[kk] = {'rho': float(r), 'exx': float(exx), 'eyy': float(eyy), 's': float(s),
                   'e_cc2d': st.e, 'e_own': ev['F'], 'mu_cc2d': st.mu, 'mu_own': ev['mu'],
                   'resid_cc2d': st.resid, 'resid_own': ev['resid'], 'A': st.A,
                   'newton_it': st.info.get('newton', {}).get('it'), 'n_ops': len(st.grid.perms())}
    jdump(pts, cpath)
    return pts, key, time.time() - t0


def richardson(d1, d2):
    """central-difference error ~ h^2: d(h), d(h/2) -> (4 d(h/2) - d(h))/3."""
    return (4.0 * d2 - d1) / 3.0


def cmd_fd(N=64):
    pts, key, tt = fd_states(N)

    def E(r, exx=0.0, eyy=0.0, s=0.0, which='e_own'):
        return pts[key(float(r), float(exx), float(eyy), float(s))][which]

    res = {'N': N, 'time_states': tt}
    for which in ('e_own', 'e_cc2d'):
        e0 = E(1.0, which=which)
        D = {}
        for name, f in (
                ('alpha', lambda h: (E(1 + h, which=which) - 2 * e0 + E(1 - h, which=which)) / h ** 2),
                ('M', lambda h: (E(1, h, which=which) - 2 * e0 + E(1, -h, which=which)) / h ** 2),
                ('Cyyyy', lambda h: (E(1, 0, h, which=which) - 2 * e0 + E(1, 0, -h, which=which)) / h ** 2),
                ('Cxxyy', lambda h: (E(1, h, h, which=which) - E(1, h, -h, which=which)
                                     - E(1, -h, h, which=which) + E(1, -h, -h, which=which)) / (4 * h * h)),
                ('mu', lambda h: 0.25 * (E(1, 0, 0, h, which=which) - 2 * e0
                                         + E(1, 0, 0, -h, which=which)) / h ** 2),
                ('gamma', lambda h: (E(1 + h, h, which=which) - E(1 + h, -h, which=which)
                                     - E(1 - h, h, which=which) + E(1 - h, -h, which=which)) / (4 * h * h)),
                ('bulk_iso', lambda h: (E(1, h, h, which=which) - 2 * e0 + E(1, -h, -h, which=which)) / h ** 2),
                ('pure_shear', lambda h: (E(1, h, -h, which=which) - 2 * e0
                                          + E(1, -h, h, which=which)) / h ** 2),
                ('stress_xx', lambda h: (E(1, h, which=which) - E(1, -h, which=which)) / (2 * h)),
                ('stress_yy', lambda h: (E(1, 0, h, which=which) - E(1, 0, -h, which=which)) / (2 * h)),
                ('stress_xy', lambda h: (E(1, 0, 0, h, which=which) - E(1, 0, 0, -h, which=which)) / (2 * h)),
                ('dedrho_mu', lambda h: (E(1 + h, which=which) - E(1 - h, which=which)) / (2 * h)),
        ):
            hs = RHO_STEPS if name in ('alpha', 'dedrho_mu') else STRAIN_STEPS
            d1, d2 = f(hs[0]), f(hs[1])
            D[name] = {'h': list(hs), 'd_h': d1, 'd_h2': d2, 'richardson': richardson(d1, d2),
                       'rich_minus_h2': richardson(d1, d2) - d2}
        res[which] = D
    # gamma also from mu(rho=1, eps_xx) (GP eigenvalue = de/drho):
    gm = {}
    for h in STRAIN_STEPS:
        gm[repr(h)] = (pts[key(1.0, h, 0.0, 0.0)]['mu_own'] - pts[key(1.0, -h, 0.0, 0.0)]['mu_own']) / (2 * h)
    hs = STRAIN_STEPS
    res['gamma_from_mu'] = {'d_h': gm[repr(hs[0])], 'd_h2': gm[repr(hs[1])],
                            'richardson': richardson(gm[repr(hs[0])], gm[repr(hs[1])])}
    am = {}
    for h in RHO_STEPS:
        am[repr(h)] = (pts[key(1.0 + h, 0.0, 0.0, 0.0)]['mu_own'] - pts[key(1.0 - h, 0.0, 0.0, 0.0)]['mu_own']) / (2 * h)
    res['alpha_from_mu'] = {'d_h': am[repr(RHO_STEPS[0])], 'd_h2': am[repr(RHO_STEPS[1])],
                            'richardson': richardson(am[repr(RHO_STEPS[0])], am[repr(RHO_STEPS[1])])}
    res['max_rel_diff_e_own_vs_cc2d'] = max(abs(p['e_own'] - p['e_cc2d']) / abs(p['e_own']) for p in pts.values())
    res['max_resid_own'] = max(p['resid_own'] for p in pts.values())
    res['max_resid_cc2d'] = max(p['resid_cc2d'] for p in pts.values())
    res['n_states'] = len(pts)
    res['mu_ref_own'] = pts[key(1.0, 0.0, 0.0, 0.0)]['mu_own']
    res['e_ref_own'] = pts[key(1.0, 0.0, 0.0, 0.0)]['e_own']
    # solver convergence of the energies: re-solve two strained states at a looser and a tighter tolerance
    st0, z = load_ref(N)
    mask = st0.grid.mask_index()
    pw = PW(mask[0], mask[1], StepKernel(G_COUPLING))
    conv = []
    for (r, exx, eyy, s) in ((1.0, STRAIN_STEPS[0], 0.0, 0.0), (1.0, 0.0, 0.0, STRAIN_STEPS[0]),
                             (1.0 + RHO_STEPS[0], -STRAIN_STEPS[0], 0.0, 0.0)):
        eps = np.array([[exx, s], [s, eyy]], float)
        row = {'rho': r, 'exx': exx, 'eyy': eyy, 's': s}
        for tol in (1e-9, 1e-10, 3e-13):
            st = solve(strained_cell(st0.cell, eps), N, r, st0, mask, tol=tol)
            row['e_own_tol%.0e' % tol] = pw.evaluate(pw.geometry(st.cell), st.c)['F']
            row['resid_tol%.0e' % tol] = st.resid
        row['e_used'] = pts[key(float(r), float(exx), float(eyy), float(s))]['e_own']
        row['rel_change_used_vs_3e-13'] = abs(row['e_used'] - row['e_own_tol3e-13']) / abs(row['e_used'])
        row['rel_change_1e-9_vs_3e-13'] = abs(row['e_own_tol1e-09'] - row['e_own_tol3e-13']) / abs(row['e_used'])
        conv.append(row)
    res['solver_energy_convergence'] = conv
    jdump(res, cache('fdres_N%d.json' % N))
    for which in ('e_own',):
        for k, v in res[which].items():
            print(N, k, repr(v['d_h']), repr(v['d_h2']), repr(v['richardson']))
    print('gamma_from_mu', res['gamma_from_mu'])
    print('alpha_from_mu', res['alpha_from_mu'])
    print('max rel e own vs cc2d', res['max_rel_diff_e_own_vs_cc2d'], 'max resid', res['max_resid_own'])
    print('solver conv', json.dumps(cc2d.jsonable(conv), indent=0))


# ----------------------------------------------------------------------------------------------------------
# step 3: analytic linear response
# ----------------------------------------------------------------------------------------------------------
def geometric_selftest():
    """check d|G_eps|^2 formulas against the exact |(I+eps)^-1 G|^2 by finite differences."""
    rng = np.random.default_rng(7)
    G = rng.normal(size=2)
    out = {}
    h = 1e-4

    def g2(t):
        eps = sum(t[a] * SBASIS[a] for a in SNAMES)
        return float(np.sum((np.linalg.inv(np.eye(2) + eps) @ G) ** 2))
    zero = {a: 0.0 for a in SNAMES}
    worst = 0.0
    for i, a in enumerate(SNAMES):
        tp = dict(zero); tp[a] = h
        tm = dict(zero); tm[a] = -h
        d1 = (g2(tp) - g2(tm)) / (2 * h)
        worst = max(worst, abs(d1 - (-2.0 * qform(SBASIS[a], G[0], G[1]))))
        for b in SNAMES[i:]:
            def tt(sa, sb):
                t = dict(zero)
                t[a] += sa * h
                t[b] += sb * h
                return t
            d2 = (g2(tt(1, 1)) - g2(tt(1, -1)) - g2(tt(-1, 1)) + g2(tt(-1, -1))) / (4 * h * h)
            Eab = SBASIS[a] @ SBASIS[b] + SBASIS[b] @ SBASIS[a]
            worst = max(worst, abs(d2 - 3.0 * qform(Eab, G[0], G[1])))
    out['max_abs_err_geometric_derivs'] = worst
    # kernel derivative check
    kern = StepKernel(G_COUPLING)
    ks = np.array([0.5, 3.0, 7.7, 21.3])
    hs = 1e-4
    s = ks ** 2
    num1 = (kern.u(np.sqrt(s + hs)) - kern.u(np.sqrt(s - hs))) / (2 * hs)
    num2 = (kern.u(np.sqrt(s + hs)) - 2 * kern.u(np.sqrt(s)) + kern.u(np.sqrt(s - hs))) / hs ** 2
    out['max_rel_err_V1'] = float(np.max(np.abs(num1 - kern.v1(ks)) / G_COUPLING))
    out['max_rel_err_V2'] = float(np.max(np.abs(num2 - kern.v2(ks)) / G_COUPLING))
    return out


def cmd_lr(N=64):
    t0 = time.time()
    st, z = load_ref(N)
    mask = st.grid.mask_index()
    pw = PW(mask[0], mask[1], StepKernel(G_COUPLING))
    geo, ev = own_eval(pw, st)
    out = {'N': N, 'selftest': geometric_selftest(), 'e_ref_own': ev['F'], 'mu_ref_own': ev['mu'],
           'resid_own': ev['resid'], 'e_ref_cc2d': st.e,
           'rel_e_own_vs_cc2d': abs(ev['F'] - st.e) / st.e}
    dF, d2F, beta = pw.strain_derivs(geo, ev)
    out['stress_analytic'] = dF
    out['d2F_fixed_x'] = d2F
    A, asym = pw.dense_A_even(geo, ev)
    out['A_even_dim'] = int(A.shape[0])
    out['A_even_asym'] = asym
    w = sla.eigvalsh(A)
    out['A_even_lowest_eigs'] = w[:6].tolist()
    cf = sla.cho_factor(A)
    x0 = pw.even_to(ev['c'])[0]
    out['x0_odd_leak'] = float(np.max(np.abs(ev['c'] - pw.even_from(x0))))
    bet = {a: pw.even_to(beta[a])[0] for a in SNAMES}
    out['beta_leak'] = {a: float(np.max(np.abs(beta[a] - pw.even_from(bet[a])))) for a in SNAMES}
    Ax0 = sla.cho_solve(cf, x0)
    Ab = {a: sla.cho_solve(cf, bet[a]) for a in SNAMES}
    xAx = float(x0 @ Ax0)
    alpha = 1.0 / (2.0 * xAx)
    gam = {a: float(x0 @ Ab[a]) / xAx for a in SNAMES}
    C = {}
    for a in SNAMES:
        for b in SNAMES:
            C[a + ',' + b] = d2F[a + ',' + b] - 2.0 * float(bet[a] @ Ab[b]) \
                + 2.0 * float(x0 @ Ab[a]) * float(x0 @ Ab[b]) / xAx
    A_cell = st.A
    out['dN_dmu_cell'] = 2.0 * A_cell * xAx       # 2 <psi0|A^-1|psi0>_cell
    out['alpha_lr'] = alpha
    out['alpha_check_A_over_dNdmu'] = A_cell / out['dN_dmu_cell']
    out['gamma_lr'] = gam
    out['C_lr'] = C
    out['M_lr'] = C['xx,xx']
    out['Cyyyy_lr'] = C['yy,yy']
    out['Cxxyy_lr'] = C['xx,yy']
    out['mu_lr'] = 0.25 * C['xy,xy']
    out['gamma_xx_lr'] = gam['xx']
    # matrix-free cross-check of A^-1 x0 with cc2d's Hessian (projected nothing; even subspace, plain CG)
    ctx = st.ctx
    xc = st.c

    def app(v):
        return ctx.hess(v)
    yv, info = cc2d.pcg(app, xc.copy(), lambda r: r / (st.grid.kin0 + max(1.0, abs(st.mu))), [],
                        tol=1e-14, maxit=5000)
    xAx_cg = cc2d.rdot(xc, yv)
    out['xAx_dense_own'] = xAx
    out['xAx_cg_cc2d_hess'] = xAx_cg
    out['xAx_rel_diff'] = abs(xAx - xAx_cg) / abs(xAx)
    out['xAx_cg_info'] = info
    # superfluid fraction, linear response, dense L on the odd subspace (x and y)
    Lo, lasym = pw.dense_L_odd(geo, ev)
    wl = sla.eigvalsh(Lo)
    out['L_odd_dim'] = int(Lo.shape[0])
    out['L_odd_asym'] = lasym
    out['L_odd_lowest_eigs'] = wl[:6].tolist()
    cl = sla.cho_factor(Lo)
    fs = {}
    ysol = {}
    for nm, (ex, ey) in (('x', (1.0, 0.0)), ('y', (0.0, 1.0)), ('d30', (SQ3 / 2, 0.5))):
        dpsi = 1j * (ex * geo['gx'] + ey * geo['gy']) * ev['c']
        d = pw.odd_to(dpsi)[0]
        leak = float(np.max(np.abs(dpsi - pw.odd_from(d))))
        y = sla.cho_solve(cl, d)
        ysol[nm] = y
        fs[nm] = {'fs_lr': 1.0 - 2.0 * float(d @ y) / st.rho, 'odd_leak': leak}
    out['fs_lr_dense'] = fs
    np.save(cache('lr_yx_N%d.npy' % N), ysol['x'])
    # cc2d's own LR (projected PCG), for comparison
    sf = cc2d.superfluid_fraction(st, (1.0, 0.0), twist=False)
    out['fs_lr_cc2d_pcg'] = sf['fs_lr']
    out['time'] = time.time() - t0
    jdump(out, cache('lr_N%d.json' % N))
    print(json.dumps(cc2d.jsonable({k: v for k, v in out.items()}), indent=1))


# ----------------------------------------------------------------------------------------------------------
# step 4: twist energies (own dense Newton in the real-coefficient subspace)
# ----------------------------------------------------------------------------------------------------------
def twist_newton(pw, geo, x, rho, kvec, tol=1e-13, maxit=8, log=None):
    x = np.asarray(x, float)
    x = x * math.sqrt(rho / float(x @ x))
    hist = []
    for it in range(maxit):
        ev = pw.evaluate(geo, x.astype(complex), kvec)
        r = ev['r']
        leak = float(np.max(np.abs(r.imag)))
        rr = r.real
        res = float(np.sqrt(rr @ rr / rho))
        hist.append({'it': it, 'resid': res, 'F': ev['F'], 'imag_leak_r': leak})
        if log:
            log('    twist it %d resid %.3e F %r' % (it, res, ev['F']))
        if res < tol:
            break
        H, asym, hleak = pw.dense_H_realcoef(geo, ev)
        n = x.size
        Kb = np.zeros((n + 1, n + 1))
        Kb[:n, :n] = H
        Kb[:n, n] = -x
        Kb[n, :n] = -x
        rhs = np.concatenate([-rr, [0.0]])
        sol = np.linalg.solve(Kb, rhs)
        x = x + sol[:n]
        x = x * math.sqrt(rho / float(x @ x))
        hist[-1]['H_asym'] = asym
        hist[-1]['H_imag_leak'] = hleak
    ev = pw.evaluate(geo, x.astype(complex), kvec)
    # second-order check: lowest eigenvalue of the constrained Hessian on x-perp
    return x, ev, hist


def cmd_twist(N=64, kfracs=(0.02, 0.04, 0.06), directions=('x', 'y')):
    t0 = time.time()
    st, z = load_ref(N)
    mask = st.grid.mask_index()
    pw = PW(mask[0], mask[1], StepKernel(G_COUPLING))
    geo, ev0 = own_eval(pw, st)
    F0 = ev0['F']
    bn = float(np.linalg.norm(geo['B'][0]))
    ylr = np.load(cache('lr_yx_N%d.npy' % N))
    out = {'N': N, 'F0': F0, 'b1_norm': bn, 'kfracs': list(kfracs)}
    lrj = jload(cache('lr_N%d.json' % N))
    for dname in directions:
        e = np.array([1.0, 0.0]) if dname == 'x' else np.array([0.0, 1.0])
        rows = []
        for kf in kfracs:
            kap = kf * bn
            kv = (kap * e[0], kap * e[1])
            if dname == 'x':
                chi = pw.odd_from(ylr)                 # L^-1 d_x psi0 (odd real function)
                seed = (ev0['c'] + 1j * kap * chi)     # phi = psi0 + i k L^-1 d_x psi0  (real coefficients)
                seed_wrong = (ev0['c'] - 1j * kap * chi)
                nrm = math.sqrt(st.rho / float(np.sum(np.abs(seed) ** 2)))   # same norm for both signs
                Fseed = pw.evaluate(geo, seed * nrm, kv)['F']
                Fseed_wrong = pw.evaluate(geo, seed_wrong * nrm, kv)['F']
            else:
                seed = ev0['c'].copy()
                Fseed = Fseed_wrong = float('nan')
            if np.max(np.abs(seed.imag)) > 1e-12:
                raise RuntimeError('seed not real-coefficient')
            x, ev, hist = twist_newton(pw, geo, seed.real, st.rho, kv, log=print)
            fk = 2.0 * (ev['F'] - F0) / (st.rho * kap * kap)
            rows.append({'kfrac_of_b1': kf, 'k': kap, 'F_k': ev['F'], 'dF': ev['F'] - F0, 'f_k': fk,
                         'resid': ev['resid'], 'newton_hist': hist, 'F_seed_first_order': Fseed,
                         'F_seed_opposite_sign': Fseed_wrong})
            print(dname, kf, repr(fk), ev['resid'], flush=True)
        ks = np.array([r['k'] for r in rows])
        fk = np.array([r['f_k'] for r in rows])
        V = np.vander(ks ** 2, len(ks), increasing=True)
        coef = np.linalg.solve(V, fk)
        V2 = np.vander(ks[:2] ** 2, 2, increasing=True)
        c2 = np.linalg.solve(V2, fk[:2])
        out[dname] = {'rows': rows, 'fs_twist_richardson_all': float(coef[0]),
                      'fs_twist_richardson_2pt': float(c2[0]), 'k4_coef': float(coef[1])}
        lr = lrj['fs_lr_dense'][dname]['fs_lr']
        out[dname]['fs_lr_dense'] = lr
        out[dname]['twist_vs_lr_rel'] = abs(coef[0] - lr) / abs(lr)
    # cc2d's own route (pcg LR + cc2d Newton twist)
    sf = cc2d.superfluid_fraction(st, (1.0, 0.0), twist=True, kfracs=kfracs)
    out['cc2d_superfluid_fraction_x'] = {k: v for k, v in sf.items()}
    out['time'] = time.time() - t0
    jdump(out, cache('twist_N%d.json' % N))
    print(json.dumps(cc2d.jsonable({k: (v if k not in ('x', 'y') else
                                        {kk: vv for kk, vv in v.items() if kk != 'rows'})
                                    for k, v in out.items() if k != 'cc2d_superfluid_fraction_x'}), indent=1))
    print('cc2d fs', sf['fs_lr'], sf.get('fs_twist'))


# ----------------------------------------------------------------------------------------------------------
# step 5: hydrodynamic formulas + collection
# ----------------------------------------------------------------------------------------------------------
def hydro(fs, alpha, M, mu, gamma, rho=1.0):
    rn = (1.0 - fs) * rho
    rs = fs * rho
    a = rho * alpha - 2.0 * gamma + M / rn
    b = (rs / rn) * (alpha * M - gamma ** 2)
    disc = a * a - 4.0 * b
    cp2 = 0.5 * (a + math.sqrt(disc))
    cm2 = 0.5 * (a - math.sqrt(disc))
    cT2 = mu / rn
    cs2 = rs * M / (rho * rn)
    Fm = (cs2 - cm2) / (cp2 - cm2)
    Fp = 1.0 - Fm
    share = (Fm / cm2) / (Fm / cm2 + Fp / cp2)
    out = {'rho_n': rn, 'rho_s': rs, 'a': a, 'b': b, 'discriminant': disc,
           'c_minus2': cm2, 'c_plus2': cp2, 'c_minus': math.sqrt(cm2), 'c_plus': math.sqrt(cp2),
           'c_T2': cT2, 'c_T': math.sqrt(cT2), 'c_star2': cs2, 'F_minus': Fm, 'F_plus': Fp,
           'static_share_minus': share,
           'sum_F_over_c2': Fm / cm2 + Fp / cp2,
           'sum_F_over_c2_expected_M_over_rho_alphaM_minus_gamma2': M / (rho * (alpha * M - gamma ** 2)),
           'c_minus_over_c_T': math.sqrt(cm2 / cT2), 'c_minus_gt_c_T': bool(cm2 > cT2)}
    out['sum_rule_rel_resid'] = abs(out['sum_F_over_c2'] - out['sum_F_over_c2_expected_M_over_rho_alphaM_minus_gamma2']) \
        / out['sum_F_over_c2_expected_M_over_rho_alphaM_minus_gamma2']
    return out


def response_check(fs, alpha, M, gamma, rho=1.0):
    """independent check of c_pm and F_minus: linearised Lagrangian
    L = -n phi_t - rho/2 phi_x^2 + rho_n/2 (u_t - phi_x)^2 - alpha/2 n^2 - gamma n u_x - M/2 u_x^2 + V n,
    plane waves exp(i(kx - wt)), k = 1: solve the 3x3 system for n(w)/V, locate poles, residues ->
    chi(w) = rho sum_nu F_nu / (w^2 - c_nu^2) (sign convention fixed by the f-sum: sum F = 1)."""
    rn, rs = (1.0 - fs) * rho, fs * rho

    def nresp(w):
        k = 1.0
        # unknowns (n, phi, u); equations from delta n, delta phi, delta u
        Mx = np.array([[-alpha, 1j * w, -1j * k * gamma],
                       [-1j * w, -k * k * rs, rn * k * w],
                       [1j * k * gamma, rn * w * k, rn * w * w - M * k * k]], complex)
        rhs = np.array([-1.0, 0.0, 0.0], complex)    # -V with V = 1 moved to the right
        sol = np.linalg.solve(Mx, rhs)
        return sol[0]
    # determinant polynomial in w^2: (w^2/alpha - rs)(rn w^2 - M + gamma^2/alpha) - w^2 (rn - gamma/alpha)^2
    p2 = rn / alpha
    p1 = -(M - gamma ** 2 / alpha) / alpha - rs * rn - (rn - gamma / alpha) ** 2
    p0 = rs * (M - gamma ** 2 / alpha)
    roots = np.sort(np.roots([p2, p1, p0]).real)
    res = []
    for c2 in roots:
        dw = 1e-6 * c2
        # residue in w^2: lim (w^2 - c2) n(w)
        vals = []
        for s in (1.0, -1.0):
            w2 = c2 + s * dw
            vals.append((w2 - c2) * nresp(math.sqrt(w2)).real)
        res.append(0.5 * (vals[0] + vals[1]))
    F = np.array(res) / rho
    F = F * np.sign(F.sum())
    return {'c2_roots': roots.tolist(), 'F_from_residues': F.tolist(), 'sum_F': float(F.sum()),
            'chi_static_numeric': float(nresp(1e-7).real), 'chi_static_expected': M / (alpha * M - gamma ** 2)}


def cmd_collect(Nprim=64, Nconv=(32, 48, 64, 80)):
    out = {'task': "Q-A' static hydrodynamic route", 'kernel': 'step', 'g': G_COUPLING, 'rho': RHO0,
           'N_primary': Nprim, 'units': 'hbar = m = R = 1; e per area; moduli per area'}
    asj = jload(cache('astar_N%d.json' % Nprim))
    fdj = jload(cache('fdres_N%d.json' % Nprim))
    lrj = jload(cache('lr_N%d.json' % Nprim))
    twj = jload(cache('twist_N%d.json' % Nprim))
    fdv = fdj['e_own']
    fs_tw = twj['x']['fs_twist_richardson_all']
    fs_lr = lrj['fs_lr_dense']['x']['fs_lr']
    out['a_star'] = asj['astar_stress_root']
    out['a_star_checks'] = {k: asj[k] for k in ('astar_poly6_fit', 'cc2d_optimize_a', 'rel_diff_own_root_vs_poly6',
                                                'rel_diff_own_root_vs_cc2d_brent', 'stress_at_astar',
                                                'e_own_at_astar', 'e_cc2d_at_astar', 'mu_own_at_astar',
                                                'd2e_da2_poly6') if k in asj}
    if 'rel_diff_own_root_vs_cc2d_dedA_root' in asj:
        out['a_star_checks']['rel_diff_own_root_vs_cc2d_dedA_root'] = asj['rel_diff_own_root_vs_cc2d_dedA_root']
    out['e_per_area'] = asj['e_own_at_astar']
    out['mu_chem'] = asj['mu_own_at_astar']
    out['A_cell'] = math.sqrt(3.0) / 2.0 * out['a_star'] ** 2
    out['contrast'] = asj['state']['contrast']
    # primary values: FD Richardson (own energies)
    out['f_s'] = fs_lr
    out['f_s_lr_dense'] = fs_lr
    out['f_s_lr_y'] = lrj['fs_lr_dense']['y']['fs_lr']
    out['f_s_lr_30deg'] = lrj['fs_lr_dense']['d30']['fs_lr']
    out['f_s_lr_cc2d_pcg'] = lrj['fs_lr_cc2d_pcg']
    out['f_s_twist_x'] = fs_tw
    out['f_s_twist_y'] = twj['y']['fs_twist_richardson_all']
    out['f_s_twist_x_2pt'] = twj['x']['fs_twist_richardson_2pt']
    out['f_s_twist_rows_x'] = [{k: r[k] for k in ('kfrac_of_b1', 'k', 'dF', 'f_k', 'resid')} for r in twj['x']['rows']]
    out['f_s_twist_rows_y'] = [{k: r[k] for k in ('kfrac_of_b1', 'k', 'dF', 'f_k', 'resid')} for r in twj['y']['rows']]
    out['f_s_twist_vs_lr_rel_x'] = twj['x']['twist_vs_lr_rel']
    out['f_s_twist_vs_lr_rel_y'] = twj['y']['twist_vs_lr_rel']
    out['f_s_cc2d_superfluid_fraction'] = {k: twj['cc2d_superfluid_fraction_x'][k] for k in
                                           ('fs_lr', 'fs_twist', 'fs_twist_2pt', 'twist_vs_lr_rel')
                                           if k in twj['cc2d_superfluid_fraction_x']}
    out['alpha'] = fdv['alpha']['richardson']
    out['M'] = fdv['M']['richardson']
    out['Cxxyy'] = fdv['Cxxyy']['richardson']
    out['mu'] = fdv['mu']['richardson']
    out['gamma'] = fdv['gamma']['richardson']
    out['Cyyyy'] = fdv['Cyyyy']['richardson']
    out['fd_steps'] = {'strain': list(STRAIN_STEPS), 'rho': list(RHO_STEPS)}
    out['fd_table_own_energies'] = fdv
    out['fd_table_cc2d_energies'] = fdj['e_cc2d']
    out['fd_gamma_from_mu'] = fdj['gamma_from_mu']
    out['fd_alpha_from_mu'] = fdj['alpha_from_mu']
    out['fd_solver_energy_convergence'] = fdj['solver_energy_convergence']
    out['fd_max_rel_diff_e_own_vs_cc2d'] = fdj['max_rel_diff_e_own_vs_cc2d']
    out['fd_max_resid'] = max(fdj['max_resid_own'], fdj['max_resid_cc2d'])
    # linear-response values
    out['lr'] = {'alpha': lrj['alpha_lr'], 'M': lrj['M_lr'], 'Cyyyy': lrj['Cyyyy_lr'], 'Cxxyy': lrj['Cxxyy_lr'],
                 'mu': lrj['mu_lr'], 'gamma': lrj['gamma_xx_lr'], 'gamma_all': lrj['gamma_lr'],
                 'C_all': lrj['C_lr'], 'dN_dmu_cell': lrj['dN_dmu_cell'],
                 'alpha_A_over_dNdmu': lrj['alpha_check_A_over_dNdmu'],
                 'A_even_lowest_eigs': lrj['A_even_lowest_eigs'], 'L_odd_lowest_eigs': lrj['L_odd_lowest_eigs'],
                 'xAx_dense_vs_cc2d_cg_rel': lrj['xAx_rel_diff'], 'selftest': lrj['selftest']}
    rel = {}
    for k in ('alpha', 'M', 'Cxxyy', 'mu', 'gamma', 'Cyyyy'):
        rel[k] = (out[k] - out['lr'][k]) / out['lr'][k]
    out['checks'] = {}
    ch = out['checks']
    ch['fd_vs_lr_rel'] = rel
    ch['max_abs_fd_vs_lr_rel'] = max(abs(v) for v in rel.values())
    ch['stress_fd_rho1'] = {k: fdv['stress_' + k]['richardson'] for k in ('xx', 'yy', 'xy')}
    ch['stress_analytic_rho1'] = lrj['stress_analytic']
    ch['stress_rel_to_M'] = max(abs(v) for v in lrj['stress_analytic'].values()) / abs(out['M'])
    ch['isotropy_Cxxxx_minus_Cxxyy'] = out['M'] - out['Cxxyy']
    ch['isotropy_2Cxyxy'] = 2.0 * out['mu']
    ch['isotropy_rel_resid'] = (out['M'] - out['Cxxyy'] - 2.0 * out['mu']) / (2.0 * out['mu'])
    ch['isotropy_lr_rel_resid'] = (out['lr']['M'] - out['lr']['Cxxyy'] - 2.0 * out['lr']['mu']) / (2.0 * out['lr']['mu'])
    ch['hex_Cxxxx_vs_Cyyyy_rel'] = (out['M'] - out['Cyyyy']) / out['M']
    ch['pure_shear_quarter_vs_mu_rel'] = (0.25 * fdv['pure_shear']['richardson'] - out['mu']) / out['mu']
    ch['bulk_iso_vs_2M_plus_2Cxxyy_rel'] = (fdv['bulk_iso']['richardson'] - 2 * out['M'] - 2 * out['Cxxyy']) \
        / fdv['bulk_iso']['richardson']
    ch['bulk_iso_vs_a2_d2e_da2_poly6_rel'] = (fdv['bulk_iso']['richardson'] - out['a_star'] ** 2 * asj['d2e_da2_poly6']) \
        / fdv['bulk_iso']['richardson']
    ch['alpha_fd'] = out['alpha']
    ch['alpha_A_over_dNdmu'] = lrj['alpha_check_A_over_dNdmu']
    ch['alpha_fd_vs_A_over_dNdmu_rel'] = (out['alpha'] - lrj['alpha_check_A_over_dNdmu']) / lrj['alpha_check_A_over_dNdmu']
    ch['alpha_from_mu_fd'] = fdj['alpha_from_mu']['richardson']
    ch['gamma_from_mu_fd'] = fdj['gamma_from_mu']['richardson']
    ch['gamma_energy_vs_mu_rel'] = (out['gamma'] - fdj['gamma_from_mu']['richardson']) / out['gamma']
    ch['dedrho_vs_mu_rel'] = (fdv['dedrho_mu']['richardson'] - fdj['mu_ref_own']) / fdj['mu_ref_own']
    ch['fs_twist_vs_lr_rel_x'] = twj['x']['twist_vs_lr_rel']
    ch['fs_twist_vs_lr_rel_y'] = twj['y']['twist_vs_lr_rel']
    ch['fs_isotropy_x_vs_y_rel'] = (out['f_s_lr_y'] - fs_lr) / fs_lr
    ch['fs_lr_dense_vs_cc2d_pcg_rel'] = (lrj['fs_lr_cc2d_pcg'] - fs_lr) / fs_lr
    ch['richardson_correction_rel'] = {k: fdv[k]['rich_minus_h2'] / fdv[k]['richardson']
                                       for k in ('alpha', 'M', 'Cxxyy', 'mu', 'gamma')}
    # hydrodynamics
    H = hydro(out['f_s'], out['alpha'], out['M'], out['mu'], out['gamma'])
    out['hydro'] = H
    for k in ('a', 'b', 'c_minus', 'c_plus', 'c_T', 'c_star2', 'F_minus', 'F_plus', 'static_share_minus',
              'c_minus2', 'c_plus2', 'c_T2', 'rho_n', 'rho_s'):
        out[k] = H[k]
    out['hydro_lr_inputs'] = hydro(out['f_s'], out['lr']['alpha'], out['lr']['M'], out['lr']['mu'], out['lr']['gamma'])
    out['hydro_twist_fs'] = hydro(fs_tw, out['alpha'], out['M'], out['mu'], out['gamma'])
    ch['hydro_sum_rule_rel_resid'] = H['sum_rule_rel_resid']
    rc = response_check(out['f_s'], out['alpha'], out['M'], out['gamma'])
    ch['response_function_check'] = rc
    ch['response_c2_vs_formula_rel'] = [(rc['c2_roots'][0] - H['c_minus2']) / H['c_minus2'],
                                        (rc['c2_roots'][1] - H['c_plus2']) / H['c_plus2']]
    ch['response_Fminus_vs_formula_abs'] = rc['F_from_residues'][0] - H['F_minus']
    ch['c_minus_gt_c_T'] = H['c_minus_gt_c_T']
    # convergence in N
    conv = []
    for N in Nconv:
        p = cache('fdres_N%d.json' % N)
        q = cache('lr_N%d.json' % N)
        a_ = cache('astar_N%d.json' % N)
        if not (os.path.exists(p) and os.path.exists(q) and os.path.exists(a_)):
            continue
        f, l, s = jload(p), jload(q), jload(a_)
        row = {'N': N, 'a_star': s['astar_stress_root'], 'e': s['e_own_at_astar'],
               'f_s_lr': l['fs_lr_dense']['x']['fs_lr']}
        for k in ('alpha', 'M', 'Cxxyy', 'mu', 'gamma'):
            row[k + '_fd'] = f['e_own'][k]['richardson']
        row.update({'alpha_lr': l['alpha_lr'], 'M_lr': l['M_lr'], 'Cxxyy_lr': l['Cxxyy_lr'], 'mu_lr': l['mu_lr'],
                    'gamma_lr': l['gamma_xx_lr']})
        hh = hydro(row['f_s_lr'], row['alpha_fd'], row['M_fd'], row['mu_fd'], row['gamma_fd'])
        row.update({k: hh[k] for k in ('c_minus', 'c_plus', 'c_T', 'F_minus', 'static_share_minus')})
        conv.append(row)
    out['convergence_N'] = conv
    if len(conv) > 1:
        ref = [r for r in conv if r['N'] == Nprim][0]
        md = {}
        for k in ref:
            if k == 'N':
                continue
            md[k] = max(abs(r[k] - ref[k]) / abs(ref[k]) for r in conv)
        ch['convergence_max_rel_dev_over_N'] = md
    out['timings_s'] = {'astar_N%d' % Nprim: asj.get('time'), 'fd_states_N%d' % Nprim: fdj.get('time_states'),
                        'lr_N%d' % Nprim: lrj.get('time'), 'twist_N%d' % Nprim: twj.get('time')}
    out['method_summary'] = ('a*: root of the analytic (Hellmann-Feynman) stress de/da at fixed rho, own code; '
                             'FD: cc2d ground states (L-BFGS + Newton-Krylov) at fixed plane-wave index set, energies '
                             're-evaluated with own PW functional, central differences h = 2e-3 and 1e-3 + Richardson; '
                             'LR: dense constrained response on the inversion-even subspace (independent check); '
                             'f_s: dense L^-1 on the odd subspace (primary) and own dense-Newton twist energies '
                             '(k = 0.02, 0.04, 0.06 |b1|, Richardson in k^2)')
    jdump(out, OUTJSON)
    show = {k: out[k] for k in ('a_star', 'f_s', 'alpha', 'M', 'Cxxyy', 'mu', 'gamma', 'a', 'b', 'c_minus',
                                'c_plus', 'c_T', 'c_star2', 'F_minus', 'static_share_minus')}
    print(json.dumps(show, indent=1))
    print(json.dumps(cc2d.jsonable(ch), indent=1))


def cmd_compare(gkey='22'):
    """cross-check against this leg's Q-A BdG results (qa_results.json, point g = 22).  Run only after
    qa_prime_results.json (static numbers) has been written."""
    out = jload(OUTJSON)
    qa = jload(os.path.join(HERE, 'qa_results.json'))
    sm = qa['summary'][gkey]
    pt = qa['points'][gkey]
    pairs = (('c2', 'c_minus'), ('c1', 'c_plus'), ('cT', 'c_T'), ('F2', 'F_minus'), ('S2', 'static_share_minus'),
             ('f_s', 'f_s'), ('astar', 'a_star'))
    cmp_ = {'source': 'qa_results.json summary/points[%s]' % gkey, 'direct': {}}
    for qk, hk in pairs:
        cmp_['direct'][hk + '_vs_' + qk] = {'hydro': out[hk], 'bdg': sm[qk], 'rel_diff_hydro_minus_bdg': (out[hk] - sm[qk]) / sm[qk],
                                            'abs_diff_hydro_minus_bdg': out[hk] - sm[qk]}
    cmp_['cT_30deg_kf005'] = {'bdg': sm.get('cT_30deg_kf005'),
                              'rel_diff_hydro_minus_bdg': (out['c_T'] - sm['cT_30deg_kf005']) / sm['cT_30deg_kf005']}
    # q -> 0 extrapolation of the per-q BdG data (polynomial in q^2), the hydrodynamic limit
    pq = pt['per_q_a1']
    q = np.array([r['qabs'] for r in pq])
    ext = {'q': q.tolist(), 'fracs': [r['frac'] for r in pq]}
    tg = {('T', 'v_over_q'): out['c_T'], ('2', 'v_over_q'): out['c_minus'], ('1', 'v_over_q'): out['c_plus'],
          ('2', 'F'): out['F_minus'], ('2', 'S'): out['static_share_minus']}
    for (lab, key), hv in tg.items():
        v = np.array([r[lab][key] for r in pq])
        row = {'per_q': v.tolist(), 'hydro': hv}
        for deg in (1, 2, 3):
            c = np.polyfit(q ** 2, v, deg)
            row['q0_poly%d_in_q2' % deg] = float(c[-1])
            row['rel_diff_hydro_minus_q0_poly%d' % deg] = (hv - float(c[-1])) / float(c[-1])
        ext[lab + '_' + key] = row
    cmp_['q_to_0_extrapolation_of_bdg'] = ext
    cmp_['note'] = ('direct differences are hydro (q -> 0) vs LSQ slopes over |q|a/2pi in {0.03,...,0.10} and weights at '
                    '0.05 (finite-q dispersion); the q -> 0 extrapolation removes it.  The BdG point was solved at the '
                    'Brent a (%r), this route at the stress root a (%r).' % (sm['astar'], out['a_star']))
    out['crosscheck_qa_point22'] = cmp_
    jdump(out, OUTJSON)
    print(json.dumps(cc2d.jsonable(cmp_), indent=1))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    N = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 64
    if cmd == 'astar':
        cmd_astar(N)
    elif cmd == 'fd':
        cmd_fd(N)
    elif cmd == 'lr':
        cmd_lr(N)
    elif cmd == 'twist':
        cmd_twist(N)
    elif cmd == 'collect':
        cmd_collect()
    elif cmd == 'compare':
        cmd_compare()
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
