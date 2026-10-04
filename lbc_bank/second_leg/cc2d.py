#!/usr/bin/env python3
"""cc2d -- 2D periodic Gross-Pitaevskii crystal instrument (second leg, independent build; numpy/scipy only).

Units: hbar = m = 1, core radius R = 1, mean density rho (default 1).
  E[psi] = int_cell 1/2 |grad psi|^2 + 1/2 int_cell int rho(r) U(r-r') rho(r') ,   rho = |psi|^2
  GP:  mu psi = -1/2 lap psi + (U*rho) psi
Kernels (class Kernel):  'step'  Uhat(k) = 2 pi g J1(k)/k   (Uhat(0) = pi g)
                         'g6'    Uhat(k) = 2 pi g int_0^inf exp(-r^6) J0(k r) r dr
                                 (Gauss-Legendre production quadrature; tanh-sinh and the small-k power
                                 series are independent checks: Kernel.check_quadratures)

DISCRETISATION (plane-wave Galerkin, exact products)
  A cell is a 2x2 array whose ROWS are the lattice vectors a1, a2 (any shape: strained cells are fine).
  Fields are periodic in fractional coordinates s in [0,1)^2, r = s1 a1 + s2 a2.  psi is stored as its
  Fourier coefficients c_G (psi(r) = sum_G c_G exp(i G.r), G = m b1 + n b2, a_i.b_j = 2 pi delta_ij) on an
  integer index set 'mask' inside the N x N FFT box.  Default mask: the inscribed disc |G| < pi N/max|a_i|,
  made exactly invariant under the cell's point group.  All products are evaluated on a 2N x 2N grid, which
  makes rho_G exact and the projection of (U*rho) psi back onto the mask exact: the discrete energy is an
  exact functional of a trigonometric polynomial (exactly translation invariant, point-group symmetric).
  Normalisation: sum_G |c_G|^2 = rho  (i.e. int_cell |psi|^2 = rho * A = N_cell).
  For finite differences in the cell shape at fixed basis pass  mask=ref_state.grid.mask_index()  so the
  same plane waves are used for every strained cell (the index set is cell independent).

GROUND STATES (no imaginary time, no split step)
  preconditioned L-BFGS on the energy with normalisation by scaling (only when the seed is far), then
  Newton-Krylov polish: projected preconditioned CG on the constrained Hessian (A = L + 2X restricted to the
  complement of {psi, i psi, d_x psi, d_y psi}), until ||H psi - mu psi|| / ||psi|| < tol (default 1e-11).
  Collapse to the uniform state is detected (modulation (max-min)/(max+min) of rho < 1e-6 -> state.uniform).

API (import cc2d)
  cc2d.hex_cell(a)                      -> 2x2 cell (rows a1=(a,0), a2=(a/2, sqrt(3) a/2))
  cc2d.Kernel(kind, g)                  kind in {'step','g6'};  .uhat(k), .duhat(k), .uhat0
  cc2d.ground_state(cell, kernel, N=64, rho=1.0, seed=None, mask=None, tol=1e-11, symmetrize=True,
                    sigma_seed=0.22, bg_seed=0.05, verbose=False)
        seed: None (Gaussian droplet on a background), a State (resampled in fractional coordinates;
              works across cells, N and masks), a real N'xN' array of psi samples on the fractional grid,
              or a dict {'c','mi','ni'} of coefficients.
        -> State with fields: grid, cell, N, rho, Ncell, A, c (coefficients), E, e (=E/A), eps (=E/Ncell),
           mu, resid, rho_max, rho_min, contrast (=rho_max/rho_min), modulation, uniform (bool), info,
           and methods psi_grid(Ngrid) (real samples on the fractional grid), to_dict(), energy_parts().
  cc2d.optimize_a(kernel, a_lo, a_hi, N=64, rho=1.0, seed=None, xatol_rel=1e-7, tol=1e-11, mask=None)
        -> dict: astar (bounded Brent on e(a)=E_cell/A at fixed rho; e(a) is flat, so Brent's answer carries a
           round-off jitter of a few 1e-8 relative), a_parabolic_quartic5 / a_parabolic_3pt (fits),
           a_dedA_root (root of the envelope-theorem derivative de/da, precise to ~1e-15) with state_root,
           state (at astar), e_per_area, eps_per_particle, mu, contrast, rho_max, rho_min, evaluations ...
  cc2d.find_astar(kernel, a_guess, N=64, seed=None, rho=1.0, step=0.01)
        robust wrapper: coarse continuation scan in a (keeps the bracket inside the crystal region, detects
        collapse to uniform -> {'collapsed': True}) then optimize_a.  Use this for continuation in g:
        o = find_astar(Kernel('step', g), a_prev, N=64, seed=prev_state);  st = o['state'].
  cc2d.dedA_envelope(state)             de/da of a hexagonal-cell state (fixed rho).
  cc2d.bdg(state, q, Kcut, nlow=8, chi_cg=True, full_check=True)
        Bloch-sector BdG (dense, plane waves exp(i(q+G).r) with |q+G| < Kcut, Cholesky route A = C C^T,
        K = C^T L C).  Full spectrum, sum rules (f-sum vs N q^2/2, static vs matrix-free CG chi), mirror
        parity blocks (auto-detected mirror with R q = q), displacement projections.
        -> dict with 'T', '2', '1' (omega, Z, F, S, parity, Px, Py), 'modes_even', 'modes_odd',
           fsum_resid, static_resid, chi_cg, chi_spec, unstable, ...
  cc2d.speeds(state, angle_deg=0.0, fracs=(0.03,0.05,0.075,0.10), Kcut=..., ref_frac=0.05)
        -> dict: c2, cT, c1 (LSQ through origin), per-q data, F2/Z21/S2 at ref_frac, gaplessness info.
  cc2d.superfluid_fraction(state, direction=(1,0), twist=True, kfracs=(0.02,0.04,0.06))
        -> dict: fs_lr (linear response 1 - (2/N) <d psi|L^-1|d psi>), fs_twist (Richardson in k^2),
           per-k twist energies.
  cc2d.gamma_checks(state, Kcut)        q = 0 sector: ||L psi0||, ||A d_j psi0||, lowest eigenvalues of L, A.
  cc2d.stability_scan(state, Kcut=50, nq=8)   min eigenvalue of A(q) on an nq x nq grid of the BZ (+M, K points);
        A(q) > 0 for all q <=> local minimum and dynamically stable.
  cc2d.run_point(kind, g, a_guess, seed=None, N=64, Kcut=80)   full Q-A point (a*, BdG, f_s, checks).
  cc2d.save_states(path, {name: State}), cc2d.load_state(npzfile, name) -> dict;
  cc2d.state_from_saved(dict) -> State (polished to tol if needed).  Saved states of this leg:
        WORK/qa_states.npz, names step_g<g> (continuation path 44 ... 13), g6_g35, and <name>_aroot (the same
        point re-solved at the envelope-derivative root a*; use these as the relaxed reference for strains).

STRAIN USAGE (fixed density rho, same plane waves for every strained cell):
  ref = state_from_saved(load_state(npz, 'step_g22_aroot'))
  st  = ground_state(ref.cell @ (np.eye(2) + eps).T, ref.kernel, ref.N, rho, seed=ref, mask=ref.grid.mask_index())
  st.e (= E_cell/A), st.E, st.mu ; the point group of the strained cell is detected automatically.
SPEED NOTES: ground_state from a nearby seed ~0.05-0.3 s (N=64); bdg at Kcut=80 ~2-4 s per q (Kcut=60 is already
  converged to <1e-9 for all reported quantities); superfluid_fraction(..., twist=False) ~0.1 s.

CLI:  python3 cc2d.py selftest | conv | qa | point ...   (see main())
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '2')
import sys
import json
import time
import math
import numpy as np
from numpy.fft import fft2, ifft2
import scipy.linalg as sla
from scipy.special import j0, j1, jv, roots_legendre, gamma
from scipy.optimize import minimize, minimize_scalar, brentq

TWOPI = 2.0 * np.pi
SQ3 = np.sqrt(3.0)
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = '/tmp/claude-0/-home-user-gifgaf0-github-io/6eab36f5-c943-5609-bc1f-38f855730ac1/scratchpad/work'


def hex_cell(a):
    """Triangular lattice cell, rows a1 = (a, 0), a2 = (a/2, sqrt(3) a/2)."""
    return np.array([[a, 0.0], [0.5 * a, 0.5 * SQ3 * a]], dtype=float)


# ----------------------------------------------------------------------------------------------------------
# kernels
# ----------------------------------------------------------------------------------------------------------
class Kernel:
    """Interaction kernel.  kind 'step': U = g theta(1-r); kind 'g6': U = g exp(-r^6)."""

    def __init__(self, kind, g, gl_nodes=2400, rmax=2.5):
        if kind not in ('step', 'g6'):
            raise ValueError(kind)
        self.kind = kind
        self.g = float(g)
        if kind == 'g6':
            x, w = roots_legendre(gl_nodes)
            r = 0.5 * rmax * (x + 1.0)
            w = 0.5 * rmax * w
            e6 = np.exp(-r ** 6)
            self._r = r
            self._w0 = w * e6 * r
            self._w1 = w * e6 * r * r
            self.uhat0 = TWOPI * self.g * gamma(1.0 / 3.0) / 6.0
        else:
            self.uhat0 = np.pi * self.g
        self._cache = {}

    def key(self):
        return (self.kind, self.g)

    def _gl(self, k, order):
        k = np.asarray(k, dtype=float)
        shp = k.shape
        ku, inv = np.unique(k.ravel(), return_inverse=True)
        out = np.empty(ku.size)
        w = self._w0 if order == 0 else self._w1
        fn = j0 if order == 0 else j1
        for s in range(0, ku.size, 1024):
            kk = ku[s:s + 1024]
            out[s:s + 1024] = fn(np.outer(kk, self._r)) @ w
        return out[inv].reshape(shp)

    def uhat(self, k):
        k = np.asarray(k, dtype=float)
        if self.kind == 'step':
            out = np.empty_like(k)
            sm = k < 1e-6
            kk = k[~sm]
            out[~sm] = TWOPI * self.g * j1(kk) / kk
            ks = k[sm]
            out[sm] = np.pi * self.g * (1.0 - ks * ks / 8.0 + ks ** 4 / 192.0)
            return out
        return TWOPI * self.g * self._gl(k, 0)

    def duhat(self, k):
        """d Uhat / dk."""
        k = np.asarray(k, dtype=float)
        if self.kind == 'step':
            out = np.empty_like(k)
            sm = k < 1e-6
            kk = k[~sm]
            out[~sm] = -TWOPI * self.g * jv(2, kk) / kk
            ks = k[sm]
            out[sm] = -np.pi * self.g * ks / 4.0
            return out
        return -TWOPI * self.g * self._gl(k, 1)

    # --- independent quadratures for the g6 transform (checks only) ---
    def uhat_tanhsinh(self, k, h=1.0 / 1024, b=3.0, tmax=3.6):
        """tanh-sinh (double exponential) quadrature of 2 pi g int_0^b exp(-r^6) J0(k r) r dr."""
        t = np.arange(-tmax, tmax + 0.5 * h, h)
        u = 0.5 * np.pi * np.sinh(t)
        r = 0.5 * b * (1.0 + np.tanh(u))
        wr = 0.5 * b * 0.5 * np.pi * np.cosh(t) / np.cosh(u) ** 2 * h
        f = np.exp(-r ** 6) * r * wr
        k = np.atleast_1d(np.asarray(k, float))
        out = np.empty(k.size)
        for s in range(0, k.size, 256):
            out[s:s + 256] = j0(np.outer(k[s:s + 256], r)) @ f
        return TWOPI * self.g * out

    def uhat_series(self, k, nterms=90):
        """power series 2 pi g sum_n (-1)^n (k/2)^(2n)/(n!)^2 Gamma((n+1)/3)/6  (accurate for k <~ 6)."""
        k = np.atleast_1d(np.asarray(k, float))
        out = np.zeros(k.size)
        for n in range(nterms):
            lg = math.lgamma((n + 1) / 3.0) - 2.0 * math.lgamma(n + 1.0) - math.log(6.0)
            with np.errstate(divide='ignore'):
                term = np.where(k > 0, np.exp(lg + 2 * n * np.log(np.maximum(k, 1e-300) / 2.0)),
                                (1.0 if n == 0 else 0.0) * math.exp(lg))
            out += (-1) ** n * term
        return TWOPI * self.g * out

    def check_quadratures(self, kvals):
        """max |GL - tanh-sinh| / Uhat(0) over kvals (and vs series for k <= 6)."""
        kvals = np.unique(np.asarray(kvals, float))
        a = self.uhat(kvals)
        b = self.uhat_tanhsinh(kvals)
        res = {'n_k': int(kvals.size), 'kmax': float(kvals.max()),
               'max_abs_diff_GL_vs_tanhsinh_over_U0': float(np.max(np.abs(a - b)) / self.uhat0)}
        sm = kvals <= 6.0
        if np.any(sm):
            c = self.uhat_series(kvals[sm])
            res['max_abs_diff_GL_vs_series_over_U0_k_le_6'] = float(np.max(np.abs(a[sm] - c)) / self.uhat0)
            res['max_abs_diff_tanhsinh_vs_series_over_U0_k_le_6'] = float(np.max(np.abs(b[sm] - c)) / self.uhat0)
        return res


# ----------------------------------------------------------------------------------------------------------
# lattice geometry
# ----------------------------------------------------------------------------------------------------------
def recip(cell):
    return TWOPI * np.linalg.inv(np.asarray(cell, float)).T


def point_group(cell, tol=1e-10):
    """Integer 2x2 matrices W acting on reciprocal indices (m,n) -> (m,n) W that preserve |G| (the point
    group of the Bravais lattice of this cell)."""
    B = recip(cell)
    gm = B @ B.T
    ops = []
    for e in np.ndindex(3, 3, 3, 3):
        W = np.array(e, dtype=int).reshape(2, 2) - 1
        d = round(np.linalg.det(W))
        if abs(d) != 1:
            continue
        if np.max(np.abs(W @ gm @ W.T - gm)) <= tol * np.max(np.abs(gm)):
            ops.append(W)
    return ops


def cart_of_W(cell, W):
    """Cartesian orthogonal R corresponding to index-space W: (m,n) W B = ((m,n) B) R^T."""
    B = recip(cell)
    RT = np.linalg.solve(B, W @ B)
    return RT.T


class Grid:
    """Plane-wave basis + FFT machinery for one cell, box size N, mask (index set)."""

    def __init__(self, cell, N, kernel, mask=None):
        self.cell = np.array(cell, dtype=float)
        self.N = N = int(N)
        if N % 2:
            raise ValueError('N must be even')
        self.kernel = kernel
        self.A = abs(np.linalg.det(self.cell))
        self.B = recip(self.cell)
        f = np.rint(np.fft.fftfreq(N) * N).astype(int)
        mN, nN = np.meshgrid(f, f, indexing='ij')
        self.ops = point_group(self.cell)
        if mask is None:
            amax = max(np.linalg.norm(self.cell[0]), np.linalg.norm(self.cell[1]))
            R = np.pi * N / amax
            G2 = self.g2(mN, nN)
            mk = (G2 < R * R * (1.0 - 1e-9)) & (np.abs(mN) < N // 2) & (np.abs(nN) < N // 2)
            # make exactly invariant under the point group
            for W in self.ops:
                m2 = mN * W[0, 0] + nN * W[1, 0]
                n2 = mN * W[0, 1] + nN * W[1, 1]
                ok = (np.abs(m2) < N // 2) & (np.abs(n2) < N // 2)
                mk &= ok
                mk &= mk[m2 % N, n2 % N]
            self.mi = mN[mk]
            self.ni = nN[mk]
        else:
            mi, ni = mask
            mi = np.asarray(mi, int)
            ni = np.asarray(ni, int)
            if np.max(np.abs(mi)) >= N // 2 or np.max(np.abs(ni)) >= N // 2:
                raise ValueError('mask does not fit in the N box')
            self.mi, self.ni = mi.copy(), ni.copy()
        self.nm = self.mi.size
        self.Gx = self.mi * self.B[0, 0] + self.ni * self.B[1, 0]
        self.Gy = self.mi * self.B[0, 1] + self.ni * self.B[1, 1]
        self.kin0 = 0.5 * (self.Gx ** 2 + self.Gy ** 2)
        self.Gmax = float(np.sqrt(2.0 * self.kin0.max()))
        self.iN, self.jN = self.mi % N, self.ni % N
        self.M = M = 2 * N
        self.iM, self.jM = self.mi % M, self.ni % M
        fM = np.rint(np.fft.fftfreq(M) * M).astype(int)
        mM, nM = np.meshgrid(fM, fM, indexing='ij')
        self.mM, self.nM = mM, nM
        GM = np.sqrt(self.g2(mM, nM))
        U = kernel.uhat(GM)
        U[mM == -M // 2] = 0.0
        U[nM == -M // 2] = 0.0
        self.UM = U
        self.GM = GM
        # position lookup for permutations of the mask
        self._pos = -np.ones((N, N), dtype=int)
        self._pos[self.iN, self.jN] = np.arange(self.nm)
        self._perms = None

    def g2(self, m, n):
        gx = m * self.B[0, 0] + n * self.B[1, 0]
        gy = m * self.B[0, 1] + n * self.B[1, 1]
        return gx * gx + gy * gy

    def mask_index(self):
        return (self.mi.copy(), self.ni.copy())

    def perms(self):
        if self._perms is None:
            P = []
            for W in self.ops:
                m2 = self.mi * W[0, 0] + self.ni * W[1, 0]
                n2 = self.mi * W[0, 1] + self.ni * W[1, 1]
                ok = (np.abs(m2) < self.N // 2) & (np.abs(n2) < self.N // 2)
                if not np.all(ok):
                    continue
                p = self._pos[m2 % self.N, n2 % self.N]
                if np.all(p >= 0):
                    P.append(p)
            self._perms = P
        return self._perms

    def symmetrize(self, c):
        P = self.perms()
        out = np.zeros_like(c)
        for p in P:
            out += c[p]
        return out / len(P)

    # transforms ---------------------------------------------------------------------------------------
    def toM(self, c):
        buf = np.zeros((self.M, self.M), dtype=complex)
        buf[self.iM, self.jM] = c
        return ifft2(buf) * (self.M * self.M)

    def fromM(self, f):
        return fft2(f)[self.iM, self.jM] / (self.M * self.M)

    def toN(self, c):
        buf = np.zeros((self.N, self.N), dtype=complex)
        buf[self.iN, self.jN] = c
        return ifft2(buf) * (self.N * self.N)

    def fromN(self, f):
        return fft2(f)[self.iN, self.jN] / (self.N * self.N)

    def kin(self, kvec=(0.0, 0.0)):
        if kvec[0] == 0.0 and kvec[1] == 0.0:
            return self.kin0
        return 0.5 * ((self.Gx + kvec[0]) ** 2 + (self.Gy + kvec[1]) ** 2)

    def rhohat(self, psiM):
        return fft2(np.abs(psiM) ** 2) / (self.M * self.M)

    def phiM(self, rhoh):
        return ifft2(self.UM * rhoh).real * (self.M * self.M)

    def eval_points(self, c, frac_pts):
        """psi at fractional points (exact Fourier sum)."""
        fp = np.atleast_2d(np.asarray(frac_pts, float))
        ph = np.exp(1j * TWOPI * (np.outer(fp[:, 0], self.mi) + np.outer(fp[:, 1], self.ni)))
        return ph @ c


# ----------------------------------------------------------------------------------------------------------
# energy, Hamiltonian, Hessian
# ----------------------------------------------------------------------------------------------------------
class _Ctx:
    """psi-dependent quantities for one coefficient vector."""

    def __init__(self, grid, c, kvec=(0.0, 0.0)):
        self.grid = grid
        self.c = c
        self.kvec = (float(kvec[0]), float(kvec[1]))
        self.kin = grid.kin(self.kvec)
        self.psiM = grid.toM(c)
        self.rhoh = grid.rhohat(self.psiM)
        self.phiM = grid.phiM(self.rhoh)
        self.Ekin = grid.A * float(np.sum(self.kin * np.abs(c) ** 2))
        self.Eint = 0.5 * grid.A * float(np.sum(grid.UM * np.abs(self.rhoh) ** 2))
        self.E = self.Ekin + self.Eint
        self.Hc = self.kin * c + grid.fromM(self.phiM * self.psiM)
        nn = float(np.sum(np.abs(c) ** 2))
        self.mu = float(np.real(np.vdot(c, self.Hc))) / nn
        self.r = self.Hc - self.mu * c
        self.resid = float(np.sqrt(np.sum(np.abs(self.r) ** 2) / nn))

    def H(self, d):
        g = self.grid
        return self.kin * d + g.fromM(self.phiM * g.toM(d))

    def hess(self, d):
        """(H - mu) d + P[psi U*(2 Re(conj(psi) d))]   (real-linear; = A d for real psi, d)."""
        g = self.grid
        dM = g.toM(d)
        w = 2.0 * np.real(np.conj(self.psiM) * dM)
        Uw = ifft2(g.UM * fft2(w)).real
        return self.kin * d - self.mu * d + g.fromM(self.phiM * dM + self.psiM * Uw)

    def Lop(self, d):
        return self.H(d) - self.mu * d


def rdot(a, b):
    return float(np.sum(a.real * b.real + a.imag * b.imag))


def _orthonormal(vecs):
    out = []
    for v in vecs:
        w = v.copy()
        for u in out:
            w = w - rdot(u, w) * u
        for u in out:
            w = w - rdot(u, w) * u
        nr = math.sqrt(rdot(w, w))
        if nr > 1e-12 * max(1.0, math.sqrt(rdot(v, v))):
            out.append(w / nr)
    return out


def pcg(apply, b, prec, Z, tol=1e-10, maxit=2000):
    """Projected preconditioned CG in the real inner product on the complement of span(Z) (orthonormal)."""
    def Q(x):
        for z in Z:
            x = x - rdot(z, x) * z
        return x
    b = Q(b)
    nb = math.sqrt(rdot(b, b))
    x = np.zeros_like(b)
    if nb == 0.0:
        return x, {'it': 0, 'rel': 0.0, 'negcurv': False}
    r = b.copy()
    z = Q(prec(r))
    p = z.copy()
    rz = rdot(r, z)
    negc = False
    it = 0
    rel = 1.0
    for it in range(1, maxit + 1):
        Ap = Q(apply(p))
        pAp = rdot(p, Ap)
        if pAp <= 0.0:
            negc = True
            if it == 1:
                x = p * (rz / max(abs(pAp), 1e-300))
            break
        al = rz / pAp
        x = x + al * p
        r = r - al * Ap
        rel = math.sqrt(rdot(r, r)) / nb
        if rel < tol:
            break
        z = Q(prec(r))
        rz2 = rdot(r, z)
        p = z + (rz2 / rz) * p
        rz = rz2
    return x, {'it': it, 'rel': rel, 'negcurv': negc}


# ----------------------------------------------------------------------------------------------------------
# State
# ----------------------------------------------------------------------------------------------------------
class State:
    def __init__(self, grid, c, rho, kvec=(0.0, 0.0), info=None):
        self.grid = grid
        self.cell = grid.cell
        self.N = grid.N
        self.A = grid.A
        self.rho = float(rho)
        self.Ncell = self.rho * self.A
        self.kvec = (float(kvec[0]), float(kvec[1]))
        self.c = c
        self.info = info or {}
        self.kernel = grid.kernel
        self.refresh()

    def refresh(self):
        ctx = _Ctx(self.grid, self.c, self.kvec)
        self.ctx = ctx
        self.E = ctx.E
        self.e = ctx.E / self.A
        self.eps = ctx.E / self.Ncell
        self.mu = ctx.mu
        self.resid = ctx.resid
        rhoM = np.abs(ctx.psiM) ** 2
        mx, mn = float(rhoM.max()), float(rhoM.min())
        pts = [(0.0, 0.0), (1.0 / 3, 1.0 / 3), (2.0 / 3, 2.0 / 3), (0.5, 0.0), (0.0, 0.5), (0.5, 0.5)]
        vals = np.abs(self.grid.eval_points(self.c, pts)) ** 2
        mx = max(mx, float(vals.max()))
        mn = min(mn, float(vals.min()))
        self.rho_max, self.rho_min = mx, mn
        self.contrast = mx / mn if mn > 0 else float('inf')
        self.modulation = (mx - mn) / (mx + mn)
        self.uniform = bool(self.modulation < 1e-6)
        self.psi_min_sign = float(np.min(ctx.psiM.real)) if self.kvec == (0.0, 0.0) else None

    def energy_parts(self):
        return {'E': self.E, 'Ekin': self.ctx.Ekin, 'Eint': self.ctx.Eint}

    def psi_grid(self, Ng=None):
        Ng = Ng or self.N
        if Ng == self.N:
            return self.grid.toN(self.c)
        g2 = Grid(self.cell, Ng, self.kernel, mask=self.grid.mask_index())
        return g2.toN(self.c)

    def to_dict(self):
        return {'c': self.c, 'mi': self.grid.mi, 'ni': self.grid.ni, 'N': self.N, 'cell': self.cell,
                'rho': self.rho, 'kind': self.kernel.kind, 'g': self.kernel.g, 'mu': self.mu, 'E': self.E}

    def summary(self):
        return {'E_cell': self.E, 'e_per_area': self.e, 'eps_per_particle': self.eps, 'mu': self.mu,
                'resid': self.resid, 'rho_max': self.rho_max, 'rho_min': self.rho_min,
                'contrast': self.contrast, 'modulation': self.modulation, 'uniform': self.uniform,
                'A_cell': self.A, 'N_cell': self.Ncell, 'N_grid': self.N, 'n_planewaves': int(self.grid.nm),
                'Gmax': self.grid.Gmax}


def _resample(grid, seed):
    """coefficients of a seed on the grid's mask (fractional-coordinate resampling)."""
    if isinstance(seed, State):
        mi, ni, cs = seed.grid.mi, seed.grid.ni, seed.c
    elif isinstance(seed, dict):
        mi, ni, cs = np.asarray(seed['mi']), np.asarray(seed['ni']), np.asarray(seed['c'])
    else:
        arr = np.asarray(seed)
        Ns = arr.shape[0]
        F = fft2(arr) / (Ns * Ns)
        f = np.rint(np.fft.fftfreq(Ns) * Ns).astype(int)
        mm, nn = np.meshgrid(f, f, indexing='ij')
        keep = (np.abs(mm) < Ns // 2) & (np.abs(nn) < Ns // 2)
        mi, ni, cs = mm[keep], nn[keep], F[keep]
    R = int(max(np.max(np.abs(mi)), np.max(np.abs(grid.mi)))) + 1
    lut = np.zeros((2 * R + 1, 2 * R + 1), dtype=complex)
    lut[mi + R, ni + R] = cs
    return lut[grid.mi + R, grid.ni + R].copy()


def gaussian_seed(grid, rho, sigma_frac=0.22, bg=0.05):
    N = grid.N
    s = np.arange(N) / N
    S1, S2 = np.meshgrid(s, s, indexing='ij')
    a1, a2 = grid.cell
    sig = sigma_frac * math.sqrt(grid.A)
    dens = np.zeros((N, N))
    for i in range(-2, 3):
        for j in range(-2, 3):
            X = (S1 - i) * a1[0] + (S2 - j) * a2[0]
            Y = (S1 - i) * a1[1] + (S2 - j) * a2[1]
            dens += np.exp(-(X * X + Y * Y) / (2 * sig * sig))
    dens = bg + dens / dens.mean()
    psi = np.sqrt(dens)
    return grid.fromN(psi.astype(complex))


def _normalize(c, rho):
    return c * math.sqrt(rho / float(np.sum(np.abs(c) ** 2)))


def _lbfgs(grid, c0, rho, sigma, maxiter, gtol_res, verbose=False):
    """preconditioned L-BFGS on E(psi(y)), psi = sqrt(rho) T y / ||T y||, T = (kin+sigma)^(-1/2) on mask."""
    N = grid.N
    T = 1.0 / np.sqrt(grid.kin0 + sigma)
    box = np.zeros((N, N), dtype=complex)
    box[grid.iN, grid.jN] = c0 / T
    y0 = ifft2(box).real * (N * N)
    sr = math.sqrt(rho)
    state = {'res': 1.0, 'n': 0}

    class _Stop(Exception):
        pass

    def fun(y):
        yh = fft2(y.reshape(N, N))[grid.iN, grid.jN] / (N * N)
        cu = T * yh
        nr = math.sqrt(float(np.sum(np.abs(cu) ** 2)))
        c = sr * cu / nr
        ctx = _Ctx(grid, c)
        gc = 2.0 * grid.A * ctx.Hc
        gcu = (sr / nr) * (gc - cu * rdot(cu, gc) / nr ** 2)
        hb = np.zeros((N, N), dtype=complex)
        hb[grid.iN, grid.jN] = T * gcu
        gy = ifft2(hb).real
        state['res'] = ctx.resid
        state['c'] = c
        state['n'] += 1
        return ctx.E, gy.ravel()

    def cb(xk):
        if state['res'] < gtol_res:
            raise _Stop()

    try:
        minimize(fun, y0.ravel(), jac=True, method='L-BFGS-B', callback=cb,
                 options={'maxiter': maxiter, 'maxcor': 30, 'ftol': 1e-16, 'gtol': 1e-14, 'maxls': 50})
    except _Stop:
        pass
    if verbose:
        print('   lbfgs evals', state['n'], 'res', state['res'], flush=True)
    return state['c'], state['res'], state['n']


def newton(grid, c, rho, kvec=(0.0, 0.0), tol=1e-11, maxit=40, symmetrize=False, sigma=None,
           verbose=False, real=True):
    """Newton-Krylov on the constrained energy.  Returns (c, ctx, info)."""
    kin = grid.kin(kvec)
    gx = grid.Gx + kvec[0]
    gy = grid.Gy + kvec[1]
    c = _normalize(c, rho)
    ctx = _Ctx(grid, c, kvec)
    hist = []
    if sigma is None:
        sigma = max(1.0, abs(ctx.mu))
    for it in range(maxit):
        hist.append(ctx.resid)
        if verbose:
            print('   newton it', it, 'res', ctx.resid, 'E', ctx.E, flush=True)
        if ctx.resid < tol:
            break
        Z = _orthonormal([c, 1j * c, 1j * grid.Gx * c, 1j * grid.Gy * c])
        eta = min(1e-3, max(1e-2 * ctx.resid, 1e-12))
        d, ci = pcg(ctx.hess, -ctx.r, lambda x: x / (kin + sigma), Z, tol=eta, maxit=3000)
        if ci['negcurv']:
            return c, ctx, {'converged': False, 'negcurv': True, 'hist': hist, 'it': it}
        # backtracking on the residual (full step normally accepted)
        step = 1.0
        for _ in range(8):
            cn = _normalize(c + step * d, rho)
            if symmetrize:
                cn = grid.symmetrize(cn)
            if real:
                pass
            cn_ctx = _Ctx(grid, cn, kvec)
            if cn_ctx.resid < ctx.resid or cn_ctx.resid < tol:
                break
            step *= 0.5
        c, ctx = cn, cn_ctx
    conv = ctx.resid < tol
    return c, ctx, {'converged': bool(conv), 'negcurv': False, 'hist': hist, 'it': len(hist)}


def ground_state(cell, kernel, N=64, rho=1.0, seed=None, mask=None, tol=1e-11, symmetrize=True,
                 sigma_seed=0.22, bg_seed=0.05, lbfgs_switch=1e-3, lbfgs_maxiter=4000, verbose=False,
                 grid=None):
    t0 = time.time()
    if grid is None:
        grid = Grid(cell, N, kernel, mask=mask)
    if seed is None:
        c = gaussian_seed(grid, rho, sigma_seed, bg_seed)
    else:
        c = _resample(grid, seed)
    c = _normalize(c, rho)
    if symmetrize:
        c = grid.symmetrize(c)
    c = c.real.astype(complex) if symmetrize else c
    ctx = _Ctx(grid, c)
    info = {'seed_resid': ctx.resid}
    sigma = max(1.0, kernel.uhat0 * rho)
    nl = 0
    for attempt in range(4):
        if ctx.resid > lbfgs_switch:
            c, res, n = _lbfgs(grid, c, rho, sigma, lbfgs_maxiter, lbfgs_switch * 0.1, verbose)
            nl += n
            if symmetrize:
                c = grid.symmetrize(c).real.astype(complex)
        c, ctx, ni = newton(grid, c, rho, (0.0, 0.0), tol, symmetrize=symmetrize, verbose=verbose)
        if ni['converged']:
            break
        lbfgs_switch *= 0.1
        # force an L-BFGS pass next round
        ctx = _Ctx(grid, c)
        if ctx.resid <= lbfgs_switch:
            lbfgs_switch = ctx.resid * 0.5
    info.update({'lbfgs_evals': nl, 'newton': ni, 'time': time.time() - t0})
    st = State(grid, c, rho, info=info)
    return st


def uniform_state(cell, kernel, N=32, rho=1.0):
    grid = Grid(cell, N, kernel)
    c = np.zeros(grid.nm, dtype=complex)
    c[(grid.mi == 0) & (grid.ni == 0)] = math.sqrt(rho)
    return State(grid, c, rho, info={'uniform_constructed': True})


# ----------------------------------------------------------------------------------------------------------
# lattice constant optimisation
# ----------------------------------------------------------------------------------------------------------
def dedA_envelope(st):
    """d e/d a for the hexagonal cell at fixed rho (envelope theorem, fractional coordinates fixed)."""
    g = st.grid
    a = np.linalg.norm(st.cell[0])
    c = st.c
    G2 = 2.0 * g.kin0
    t1 = -float(np.sum(G2 * np.abs(c) ** 2)) / a
    rh = st.ctx.rhoh
    k = g.GM
    dU = g.kernel.duhat(k)
    dU[g.mM == -g.M // 2] = 0.0
    dU[g.nM == -g.M // 2] = 0.0
    t2 = -0.5 * float(np.sum(dU * k * np.abs(rh) ** 2)) / a
    return t1 + t2


def optimize_a(kernel, a_lo, a_hi, N=64, rho=1.0, seed=None, xatol_rel=1e-7, tol=1e-11, mask=None,
               parabolic_h=2e-3, verbose=False, root_check=True):
    t0 = time.time()
    evals = []
    states = {}

    def nearest_seed(a):
        if not states:
            return seed
        ak = min(states.keys(), key=lambda x: abs(x - a))
        return states[ak]

    def solve(a):
        if a in states:
            return states[a]
        st = ground_state(hex_cell(a), kernel, N, rho, seed=nearest_seed(a), mask=mask, tol=tol)
        states[a] = st
        evals.append({'a': a, 'e': st.e, 'mu': st.mu, 'resid': st.resid, 'uniform': st.uniform,
                      'contrast': st.contrast})
        if verbose:
            print('  a=%r e=%r res=%.3g contrast=%.6g' % (a, st.e, st.resid, st.contrast), flush=True)
        return st

    def fe(a):
        st = solve(float(a))
        return st.e

    amid = 0.5 * (a_lo + a_hi)
    res = minimize_scalar(fe, bounds=(a_lo, a_hi), method='bounded',
                          options={'xatol': xatol_rel * amid, 'maxiter': 500})
    astar = float(res.x)
    st = solve(astar)
    out = {'astar': astar, 'brent_nfev': int(res.nfev), 'xatol': xatol_rel * amid,
           'bracket': [a_lo, a_hi], 'state': st}
    # parabolic cross-check
    hs = np.array([-2, -1, 0, 1, 2], float) * parabolic_h * astar
    es = np.array([solve(astar + h).e for h in hs])
    p = np.polyfit(hs / astar, es, 4)
    # vertex of the quartic near 0 (Newton on derivative)
    dp = np.polyder(p)
    ddp = np.polyder(dp)
    x = 0.0
    for _ in range(50):
        x -= np.polyval(dp, x) / np.polyval(ddp, x)
    p2 = np.polyfit(hs[1:4] / astar, es[1:4], 2)
    out['a_parabolic_quartic5'] = float(astar * (1.0 + x))
    out['a_parabolic_3pt'] = float(astar * (1.0 - p2[1] / (2 * p2[0])))
    out['e_second_derivative_d2e_da2'] = float(2 * p[2] / astar ** 2)
    # envelope-theorem derivative root (independent route)
    if root_check:
        d0 = dedA_envelope(st)
        out['dedA_at_astar'] = d0
        try:
            def fd(a):
                return dedA_envelope(solve(float(a)))
            h = 5e-3 * astar
            aL, aR = astar - h, astar + h
            if fd(aL) * fd(aR) < 0:
                ar = brentq(fd, aL, aR, xtol=1e-14 * astar, rtol=1e-15, maxiter=100)
                out['a_dedA_root'] = float(ar)
                out['state_root'] = solve(float(ar))
        except Exception as ex:  # pragma: no cover
            out['a_dedA_root_error'] = repr(ex)
    st = solve(astar)
    out.update({'e_per_area': st.e, 'eps_per_particle': st.eps, 'mu': st.mu, 'contrast': st.contrast,
                'rho_max': st.rho_max, 'rho_min': st.rho_min, 'modulation': st.modulation,
                'uniform': st.uniform, 'resid': st.resid, 'evaluations': evals, 'time': time.time() - t0})
    out['state'] = st
    return out


# ----------------------------------------------------------------------------------------------------------
# BdG
# ----------------------------------------------------------------------------------------------------------
class _BdGContext:
    """Fourier lookup tables of psi0, rho0, Phi0 for one ground state."""

    def __init__(self, st):
        g = st.grid
        self.st = st
        self.g = g
        N = g.N
        self.off = 2 * N
        sz = 2 * self.off + 1
        self.cr = np.max(np.abs(st.c.imag)) <= 1e-13 * np.max(np.abs(st.c))
        dt = float if self.cr else complex
        self.LP = np.zeros((sz, sz), dtype=dt)
        cc = st.c.real if self.cr else st.c
        self.LP[g.mi + self.off, g.ni + self.off] = cc
        rh = st.ctx.rhoh
        keep = (np.abs(g.mM) < N) & (np.abs(g.nM) < N)
        mm, nn = g.mM[keep], g.nM[keep]
        self.LR = np.zeros((sz, sz), dtype=dt)
        self.LF = np.zeros((sz, sz), dtype=dt)
        rv = rh[keep].real if self.cr else rh[keep]
        self.LR[mm + self.off, nn + self.off] = rv
        self.LF[mm + self.off, nn + self.off] = g.UM[keep] * rv
        # support of psi0 used for the intermediate sum in X (coefficients below 1e-18 of the max are
        # round-off noise of the ground-state solve)
        self.psi_support = float(np.sqrt(2.0 * np.max(g.kin0[np.abs(st.c) > 1e-18 * np.max(np.abs(st.c))])))
        self.cell = g.cell
        self.B = g.B

    def lookup(self, T, dm, dn):
        ok = (np.abs(dm) <= self.off) & (np.abs(dn) <= self.off)
        out = np.zeros(dm.shape, dtype=T.dtype)
        out[ok] = T[dm[ok] + self.off, dn[ok] + self.off]
        return out


def _index_disc(B, cell, q, radius):
    a1n = np.linalg.norm(cell[0])
    a2n = np.linalg.norm(cell[1])
    mmax = int(math.ceil((radius + np.linalg.norm(q)) * a1n / TWOPI)) + 1
    nmax = int(math.ceil((radius + np.linalg.norm(q)) * a2n / TWOPI)) + 1
    m, n = np.meshgrid(np.arange(-mmax, mmax + 1), np.arange(-nmax, nmax + 1), indexing='ij')
    m, n = m.ravel(), n.ravel()
    gx = q[0] + m * B[0, 0] + n * B[1, 0]
    gy = q[1] + m * B[0, 1] + n * B[1, 1]
    k2 = gx * gx + gy * gy
    sel = k2 < radius * radius
    order = np.lexsort((n[sel], m[sel], k2[sel]))
    return m[sel][order], n[sel][order], gx[sel][order], gy[sel][order]


def bdg_matrices(st, q, Kcut, ctx=None):
    """Dense L(q), X(q) in the orthonormal basis exp(i(q+G).r)/sqrt(A), |q+G| < Kcut."""
    ctx = ctx or _BdGContext(st)
    g = st.grid
    q = np.asarray(q, float)
    mb, nb, gxb, gyb = _index_disc(g.B, g.cell, q, Kcut)
    kin = 0.5 * (gxb ** 2 + gyb ** 2)
    L = ctx.lookup(ctx.LF, mb[:, None] - mb[None, :], nb[:, None] - nb[None, :])
    L[np.diag_indices_from(L)] += kin - st.mu
    mK, nK, gxK, gyK = _index_disc(g.B, g.cell, q, Kcut + ctx.psi_support + 1e-9)
    PsiBK = ctx.lookup(ctx.LP, mb[:, None] - mK[None, :], nb[:, None] - nK[None, :])
    UK = g.kernel.uhat(np.sqrt(gxK ** 2 + gyK ** 2))
    X = (PsiBK * UK[None, :]) @ PsiBK.conj().T
    X = 0.5 * (X + X.conj().T)
    L = 0.5 * (L + L.conj().T)
    s = math.sqrt(g.A) * ctx.lookup(ctx.LP, mb, nb)
    return {'L': L, 'X': X, 's': s, 'mb': mb, 'nb': nb, 'gx': gxb, 'gy': gyb, 'kin': kin,
            'PsiBK': PsiBK, 'mK': mK, 'nK': nK, 'gxK': gxK, 'gyK': gyK, 'ctx': ctx}


class _QOps:
    """matrix-free FFT application of L(q), A(q) on the basis (mb, nb) -- independent code path."""

    def __init__(self, st, q, mb, nb):
        g = st.grid
        self.st = st
        mmax_b = int(max(np.max(np.abs(mb)), np.max(np.abs(nb))))
        mmax_p = int(max(np.max(np.abs(g.mi)), np.max(np.abs(g.ni))))
        MB = max(2 * (mmax_b + mmax_p) + 4, 4 * mmax_p + 4)
        MB += MB % 2
        self.MB = MB
        self.mb, self.nb = mb % MB, nb % MB
        gx = q[0] + mb * g.B[0, 0] + nb * g.B[1, 0]
        gy = q[1] + mb * g.B[0, 1] + nb * g.B[1, 1]
        self.kin = 0.5 * (gx * gx + gy * gy)
        buf = np.zeros((MB, MB), dtype=complex)
        buf[g.mi % MB, g.ni % MB] = st.c
        self.psi = ifft2(buf) * MB * MB
        rhoh = fft2(np.abs(self.psi) ** 2) / (MB * MB)
        f = np.rint(np.fft.fftfreq(MB) * MB).astype(int)
        mm, nn = np.meshgrid(f, f, indexing='ij')
        Gq = np.sqrt((q[0] + mm * g.B[0, 0] + nn * g.B[1, 0]) ** 2 + (q[1] + mm * g.B[0, 1] + nn * g.B[1, 1]) ** 2)
        G0 = np.sqrt((mm * g.B[0, 0] + nn * g.B[1, 0]) ** 2 + (mm * g.B[0, 1] + nn * g.B[1, 1]) ** 2)
        U0 = g.kernel.uhat(G0)
        Uq = g.kernel.uhat(Gq)
        for U in (U0, Uq):
            U[mm == -MB // 2] = 0.0
            U[nn == -MB // 2] = 0.0
        self.Uq = Uq
        self.phi = ifft2(U0 * rhoh).real * MB * MB
        self.mu = st.mu

    def _emb(self, x):
        buf = np.zeros((self.MB, self.MB), dtype=complex)
        buf[self.mb, self.nb] = x
        return ifft2(buf) * self.MB * self.MB

    def _ext(self, f):
        return fft2(f)[self.mb, self.nb] / (self.MB * self.MB)

    def L(self, x):
        f = self._emb(x)
        return (self.kin - self.mu) * x + self._ext(self.phi * f)

    def A(self, x):
        f = self._emb(x)
        gq = fft2(self.psi * f)
        u = ifft2(self.Uq * gq)
        return (self.kin - self.mu) * x + self._ext(self.phi * f + 2.0 * self.psi * u)


def chi_static_cg(st, q, mb, nb, s, tol=1e-14):
    ops = _QOps(st, np.asarray(q, float), mb, nb)
    sig = max(1.0, st.kernel.uhat0 * st.rho)
    x, info = pcg(ops.A, s.astype(complex), lambda r: r / (ops.kin + sig), [], tol=tol, maxit=20000)
    chi = 2.0 * rdot(s.astype(complex), x)
    return chi, info, ops


def find_mirror(cell, q, tol=1e-10):
    """index-space mirror W (det R = -1) with R q = q, or None."""
    qn = np.linalg.norm(q)
    for W in point_group(cell):
        R = cart_of_W(cell, W)
        if np.linalg.det(R) > 0:
            continue
        if qn == 0 or np.linalg.norm(R @ q - q) <= tol * qn:
            return W, R
    return None, None


def _perm_from_W(mb, nb, W):
    m2 = mb * W[0, 0] + nb * W[1, 0]
    n2 = mb * W[0, 1] + nb * W[1, 1]
    lut = {(int(a), int(b)): i for i, (a, b) in enumerate(zip(mb, nb))}
    return np.array([lut[(int(a), int(b))] for a, b in zip(m2, n2)])


def _solve_block(L, A, s, nlow, Ncell, qq):
    """Cholesky route on one block: returns omega (all), Z (all), low-mode f+ vectors."""
    C = sla.cholesky(A, lower=True)
    LC = L @ C
    K = C.conj().T @ LC
    K = 0.5 * (K + K.conj().T)
    w2, W = sla.eigh(K)
    om = np.sqrt(np.abs(w2)) * np.sign(w2)
    t = sla.solve_triangular(C, s, lower=True)
    pr = W.conj().T @ t
    Z = np.abs(om) * np.abs(pr) ** 2
    nl = min(nlow, W.shape[1])
    fp = sla.solve_triangular(C, W[:, :nl] * np.sqrt(np.abs(om[:nl]))[None, :], lower=True, trans='C')
    return om, Z, fp, w2


def bdg(st, q, Kcut, nlow=8, chi_cg=True, full_check=True, ctx=None, mirror='auto'):
    t0 = time.time()
    q = np.asarray(q, float)
    qq = float(q @ q)
    mats = bdg_matrices(st, q, Kcut, ctx)
    L, X, s = mats['L'], mats['X'], mats['s']
    A = L + 2.0 * X
    mb, nb = mats['mb'], mats['nb']
    nbas = L.shape[0]
    Ncell = st.Ncell
    out = {'q': [float(q[0]), float(q[1])], 'qabs': math.sqrt(qq), 'Kcut': Kcut, 'nbasis': int(nbas),
           'real_arith': bool(not np.iscomplexobj(L))}
    fan = 0.5 * Ncell * qq
    out['fsum_analytic'] = fan
    out['sLs'] = float(np.real(np.vdot(s, L @ s)))
    out['s_norm2_vs_Ncell'] = float(np.real(np.vdot(s, s))) / Ncell - 1.0
    # stability: smallest eigenvalue of A (L > 0 for q != 0)
    try:
        om, Z, fp, w2 = _solve_block(L, A, s, nlow, Ncell, qq)
        out['unstable'] = False
    except np.linalg.LinAlgError:
        Dc = sla.cholesky(L, lower=True)
        Kp = Dc.conj().T @ A @ Dc
        w2 = sla.eigvalsh(0.5 * (Kp + Kp.conj().T))
        out['unstable'] = True
        out['min_omega2'] = float(w2.min())
        out['n_negative_omega2'] = int(np.sum(w2 < 0))
        out['omega2_low'] = [float(x) for x in w2[:nlow]]
        out['time'] = time.time() - t0
        return out
    out['min_omega2'] = float(w2.min())
    fsum = float(np.sum(om * Z))
    chi_spec = float(np.sum(2.0 * Z / om))
    out['fsum_spec'] = fsum
    out['fsum_resid'] = abs(fsum - fan) / fan
    out['fsum_resid_vs_sLs'] = abs(fsum - out['sLs']) / out['sLs']
    out['chi_spec'] = chi_spec
    if chi_cg:
        chi, ci, _ = chi_static_cg(st, q, mb, nb, s)
        out['chi_cg'] = chi
        out['chi_cg_info'] = {'it': ci['it'], 'rel': ci['rel']}
        out['static_resid'] = abs(chi_spec - chi) / chi
    # displacement vectors w_j = exp(iqr) psi0 d_j rho0 projected on basis
    ctx = mats['ctx']
    rK = ctx.lookup(ctx.LR, mats['mK'], mats['nK'])
    Kx = mats['gxK'] - q[0]
    Ky = mats['gyK'] - q[1]
    wx = math.sqrt(st.A) * (mats['PsiBK'] @ (1j * Kx * rK))
    wy = math.sqrt(st.A) * (mats['PsiBK'] @ (1j * Ky * rK))
    # mirror blocks
    W, R = (find_mirror(st.cell, q) if mirror == 'auto' else (None, None))
    out['mirror'] = None if W is None else W.tolist()

    nwx, nwy = float(np.linalg.norm(wx)), float(np.linalg.norm(wy))

    def mode_rec(omv, Zv, f, par=None):
        Px = abs(np.vdot(wx, f))
        Py = abs(np.vdot(wy, f))
        nf = float(np.linalg.norm(f))
        return {'omega': float(omv), 'Z': float(Zv), 'F': float(omv * Zv / fan),
                'Px_cos': float(Px / (nwx * nf)) if nwx * nf > 0 else 0.0,
                'Py_cos': float(Py / (nwy * nf)) if nwy * nf > 0 else 0.0,
                'S': float(2 * Zv / omv / chi_spec), 'S_vs_chi_cg': float(2 * Zv / omv / out['chi_cg']) if chi_cg else None,
                'rho_abs': float(math.sqrt(Zv)), 'parity': None if par is None else float(par),
                'Px': float(Px), 'Py': float(Py), 'v_over_q': float(omv / math.sqrt(qq))}

    if W is not None:
        perm = _perm_from_W(mb, nb, W)
        idx = np.arange(nbas)
        fixed = idx[perm == idx]
        pa = idx[(perm > idx)]
        pb = perm[pa]
        ne, no = fixed.size + pa.size, pa.size
        Pe = np.zeros((nbas, ne))
        Po = np.zeros((nbas, no))
        Pe[fixed, np.arange(fixed.size)] = 1.0
        r2 = 1.0 / math.sqrt(2.0)
        Pe[pa, fixed.size + np.arange(pa.size)] = r2
        Pe[pb, fixed.size + np.arange(pa.size)] = r2
        Po[pa, np.arange(no)] = r2
        Po[pb, np.arange(no)] = -r2
        blocks = {}
        for name, P in (('even', Pe), ('odd', Po)):
            Lb = P.T @ L @ P
            Ab = P.T @ A @ P
            sb = P.T @ s
            omb, Zb, fpb, _ = _solve_block(Lb, Ab, sb, nlow, Ncell, qq)
            fpf = P @ fpb
            recs = []
            for j in range(fpf.shape[1]):
                par = float(np.real(np.vdot(fpf[:, j], fpf[perm, j])) / np.real(np.vdot(fpf[:, j], fpf[:, j])))
                recs.append(mode_rec(omb[j], Zb[j], fpf[:, j], par))
            blocks[name] = {'omega': omb, 'Z': Zb, 'recs': recs, 's_norm': float(np.linalg.norm(sb))}
        out['modes_even'] = blocks['even']['recs']
        out['modes_odd'] = blocks['odd']['recs']
        out['s_norm_odd_block'] = blocks['odd']['s_norm']
        omu = np.concatenate([blocks['even']['omega'], blocks['odd']['omega']])
        Zu = np.concatenate([blocks['even']['Z'], blocks['odd']['Z']])
        out['fsum_resid_blocks'] = abs(float(np.sum(omu * Zu)) - fan) / fan
        out['chi_spec_blocks'] = float(np.sum(2 * Zu / omu))
        out['spectrum_full_vs_blocks_maxdiff_low'] = float(np.max(np.abs(np.sort(omu)[:3 * nlow] - om[:3 * nlow])))
        out['T'] = dict(out['modes_odd'][0], label='T')
        out['2'] = dict(out['modes_even'][0], label='2')
        # upper longitudinal branch: normally the 2nd even mode; cross-check by f-sum weight among the
        # next three even modes (a gapped mode dipping below it would carry little weight)
        cand = out['modes_even'][1:4]
        jmax = int(np.argmax([m['F'] for m in cand]))
        out['1'] = dict(cand[jmax], label='1')
        out['label1_is_second_even'] = bool(jmax == 0)
        if full_check:
            # parity of the unblocked eigenvectors; rho of the odd ones
            chk = []
            for j in range(fp.shape[1]):
                f = fp[:, j]
                par = float(np.real(np.vdot(f, f[perm])) / np.real(np.vdot(f, f)))
                chk.append({'omega': float(om[j]), 'Z': float(Z[j]), 'parity': par})
            out['full_solve_low'] = chk
            odd = [c for c in chk if c['parity'] < -0.999999]
            ev = [c for c in chk if c['parity'] > 0.999999]
            if odd and ev:
                out['full_rhoT_over_rho2'] = float(math.sqrt(odd[0]['Z'] / max(ev[0]['Z'], 1e-300)))
    else:
        recs = [mode_rec(om[j], Z[j], fp[:, j]) for j in range(fp.shape[1])]
        out['modes_all'] = recs
        low = sorted(recs[:3], key=lambda r: r['Z'])
        out['T'] = dict(low[0], label='T(min Z of lowest 3; no mirror)')
        rest = sorted(low[1:], key=lambda r: r['omega'])
        out['2'] = dict(rest[0], label='2')
        out['1'] = dict(rest[1], label='1')
    out['omega_low'] = [float(x) for x in om[:nlow]]
    out['time'] = time.time() - t0
    return out


def gamma_checks(st, Kcut):
    """q = 0 sector: L psi0 = 0, A d_j psi0 = 0, lowest eigenvalues of L and A."""
    mats = bdg_matrices(st, np.zeros(2), Kcut)
    L, X, s = mats['L'], mats['X'], mats['s']
    A = L + 2 * X
    dx = 1j * mats['gx'] * s
    dy = 1j * mats['gy'] * s
    nrm = lambda v: float(np.linalg.norm(v))
    out = {'Kcut': Kcut, 'nbasis': int(L.shape[0]),
           'L_psi0_rel': nrm(L @ s) / nrm(s),
           'A_dxpsi0_rel': nrm(A @ dx) / nrm(dx), 'A_dypsi0_rel': nrm(A @ dy) / nrm(dy)}
    eL = sla.eigvalsh(L)
    eA = sla.eigvalsh(A)
    out['L_lowest'] = [float(x) for x in eL[:4]]
    out['A_lowest'] = [float(x) for x in eA[:5]]
    # BdG frequencies at q=0 (non-Hermitian L A), smallest |omega^2|
    w2 = np.sort(np.abs(np.linalg.eigvals(L @ A)))
    out['abs_omega2_LA_lowest'] = [float(x) for x in w2[:6]]
    return out


# ----------------------------------------------------------------------------------------------------------
# speeds along a direction
# ----------------------------------------------------------------------------------------------------------
def speeds(st, angle_deg=0.0, fracs=(0.03, 0.05, 0.075, 0.10), Kcut=None, ref_frac=0.05, nlow=8,
           chi_cg=True):
    a = np.linalg.norm(st.cell[0])
    th = math.radians(angle_deg)
    e = np.array([math.cos(th), math.sin(th)])
    ctx = _BdGContext(st)
    per = []
    for f in fracs:
        q = f * TWOPI / a * e
        r = bdg(st, q, Kcut, nlow=nlow, chi_cg=chi_cg, ctx=ctx)
        r['frac'] = f
        per.append(r)
    out = {'angle_deg': angle_deg, 'fracs': list(fracs), 'Kcut': Kcut, 'per_q': per}
    if any(r.get('unstable') for r in per):
        out['unstable'] = True
        return out
    qs = np.array([r['qabs'] for r in per])
    for lab in ('T', '2', '1'):
        oms = np.array([r[lab]['omega'] for r in per])
        out['c' + lab] = float(np.sum(oms * qs) / np.sum(qs * qs))
        out['v_over_q_' + lab] = [float(x) for x in oms / qs]
    # gaplessness: next modes in each block
    gaps = []
    for r in per:
        nx = []
        if 'modes_even' in r:
            nx.append(r['modes_even'][2]['omega'])
            nx.append(r['modes_odd'][1]['omega'])
        gaps.append(min(nx) if nx else None)
    out['lowest_gapped_omega_per_q'] = gaps
    if ref_frac in fracs:
        r = per[list(fracs).index(ref_frac)]
        out['ref'] = {'frac': ref_frac, 'F2': r['2']['F'], 'Z21': r['2']['Z'] / r['1']['Z'], 'S2': r['2']['S'],
                      'F1': r['1']['F'], 'S1': r['1']['S'], 'FT': r['T']['F'],
                      'cT_point': r['T']['omega'] / r['qabs']}
    out['fsum_resid_max'] = float(max(r['fsum_resid'] for r in per))
    if chi_cg:
        out['static_resid_max'] = float(max(r['static_resid'] for r in per))
    return out


# ----------------------------------------------------------------------------------------------------------
# superfluid fraction
# ----------------------------------------------------------------------------------------------------------
def superfluid_fraction(st, direction=(1.0, 0.0), twist=True, kfracs=(0.02, 0.04, 0.06), tol=1e-12,
                        verbose=False):
    g = st.grid
    e = np.asarray(direction, float)
    e = e / np.linalg.norm(e)
    c0 = st.c
    ctx = st.ctx
    dpsi = 1j * (e[0] * g.Gx + e[1] * g.Gy) * c0
    Z = _orthonormal([c0])
    sig = max(1.0, abs(st.mu))
    y, ci = pcg(ctx.Lop, dpsi, lambda x: x / (g.kin0 + sig), Z, tol=1e-14, maxit=20000)
    corr = 2.0 * g.A * rdot(dpsi, y) / st.Ncell
    out = {'direction': e.tolist(), 'fs_lr': 1.0 - corr, 'lr_cg': {'it': ci['it'], 'rel': ci['rel']}}
    if not twist:
        return out
    bn = np.linalg.norm(g.B[0])
    E0 = st.E
    rows = []
    for kf in kfracs:
        kap = kf * bn
        kv = (kap * e[0], kap * e[1])
        cs = c0 - 1j * kap * y
        cn, cx, inf = newton(g, cs, st.rho, kv, tol=tol, maxit=30, symmetrize=False, verbose=verbose)
        fk = 2.0 * (cx.E - E0) / (st.Ncell * kap * kap)
        rows.append({'kfrac_of_b1': kf, 'k': kap, 'E': cx.E, 'dE': cx.E - E0, 'f_k': fk, 'resid': cx.resid,
                     'converged': inf['converged']})
    ks = np.array([r['k'] for r in rows])
    fk = np.array([r['f_k'] for r in rows])
    # Richardson / polynomial in k^2
    V = np.vander(ks ** 2, len(ks), increasing=True)
    coef = np.linalg.solve(V, fk)
    out['twist'] = rows
    out['fs_twist'] = float(coef[0])
    if len(ks) >= 2:
        V2 = np.vander(ks[:2] ** 2, 2, increasing=True)
        out['fs_twist_2pt'] = float(np.linalg.solve(V2, fk[:2])[0])
    out['twist_vs_lr_rel'] = abs(out['fs_twist'] - out['fs_lr']) / abs(out['fs_lr'])
    return out


# ----------------------------------------------------------------------------------------------------------
# persistence
# ----------------------------------------------------------------------------------------------------------
def save_states(path, states, extra=None):
    d = {}
    for name, st in states.items():
        dd = st.to_dict()
        dd['psi'] = st.psi_grid().real          # psi samples on the N x N fractional grid (s_i = i/N)
        dd['astar'] = float(np.linalg.norm(st.cell[0]))
        for k, v in dd.items():
            d['%s__%s' % (name, k)] = np.asarray(v)
    if extra:
        for k, v in extra.items():
            d[k] = np.asarray(v)
    np.savez(path, **d)


def load_state(path, name):
    z = np.load(path, allow_pickle=False)
    d = {}
    for k in ('c', 'mi', 'ni', 'N', 'cell', 'rho', 'kind', 'g', 'mu', 'E', 'psi', 'astar'):
        kk = '%s__%s' % (name, k)
        if kk in z:
            d[k] = z[kk]
    return d


def state_from_saved(d, kernel=None, tol=1e-11, polish=True):
    kernel = kernel or Kernel(str(d['kind']), float(d['g']))
    grid = Grid(np.asarray(d['cell']), int(d['N']), kernel, mask=(d['mi'], d['ni']))
    st = State(grid, np.asarray(d['c']).astype(complex), float(d['rho']))
    if polish and st.resid > tol:
        st = ground_state(st.cell, kernel, st.N, st.rho, seed=st, mask=(d['mi'], d['ni']), tol=tol)
    return st


# ----------------------------------------------------------------------------------------------------------
# JSON helpers
# ----------------------------------------------------------------------------------------------------------
def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items() if not isinstance(v, State)}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return [jsonable(v) for v in o.tolist()]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, complex):
        return [o.real, o.imag]
    return o


def json_dump(obj, path):
    with open(path, 'w') as f:
        json.dump(jsonable(obj), f, indent=1, allow_nan=True)


# ----------------------------------------------------------------------------------------------------------
# stability scan over the Brillouin zone (A(q) > 0 for all q  <=>  local minimum / dynamically stable)
# ----------------------------------------------------------------------------------------------------------
def stability_scan(st, Kcut=50.0, nq=8):
    ctx = _BdGContext(st)
    B = st.grid.B
    rows = []
    for i in range(nq):
        for j in range(nq):
            if i == 0 and j == 0:
                continue
            q = (i / nq) * B[0] + (j / nq) * B[1]
            mats = bdg_matrices(st, q, Kcut, ctx)
            A = mats['L'] + 2.0 * mats['X']
            ev = sla.eigvalsh(A, subset_by_index=[0, 0])[0]
            rows.append((float(ev), i, j, float(np.linalg.norm(q))))
    rows.sort()
    # M point (1/2,0) and K point (1/3,1/3) explicitly
    special = {}
    for nm, fr in (('M', (0.5, 0.0)), ('K', (1.0 / 3.0, 1.0 / 3.0))):
        q = fr[0] * B[0] + fr[1] * B[1]
        mats = bdg_matrices(st, q, Kcut, ctx)
        A = mats['L'] + 2.0 * mats['X']
        special[nm] = float(sla.eigvalsh(A, subset_by_index=[0, 0])[0])
    return {'Kcut': Kcut, 'nq': nq, 'min_eig_A': rows[0][0], 'argmin_frac': [rows[0][1] / nq, rows[0][2] / nq],
            'argmin_qabs': rows[0][3], 'n_negative': int(sum(1 for r in rows if r[0] < 0)),
            'min_eig_A_M': special['M'], 'min_eig_A_K': special['K']}


# ----------------------------------------------------------------------------------------------------------
# a* search with a coarse pre-scan (keeps Brent inside the crystal region)
# ----------------------------------------------------------------------------------------------------------
def find_astar(kernel, a_guess, N=64, seed=None, rho=1.0, step=0.01, xatol_rel=1e-7, verbose=False,
               mask=None):
    t0 = time.time()
    scan = {}
    cur = seed

    def solve(a, sd):
        st = ground_state(hex_cell(a), kernel, N, rho, seed=sd, mask=mask)
        scan[a] = st
        if verbose:
            print('  scan a=%.6f e=%r uniform=%s contrast=%.6g' % (a, st.e, st.uniform, st.contrast), flush=True)
        return st

    st0 = solve(a_guess, cur)
    if st0.uniform:
        return {'collapsed': True, 'a_guess': a_guess, 'state': st0, 'scan': [(a_guess, st0.e, True)]}
    lo, hi = a_guess, a_guess
    # walk down and up until the minimum is bracketed (by a crystal point on each side)
    left = solve(a_guess * (1 - step), st0)
    right = solve(a_guess * (1 + step), st0)
    pts = {a_guess: st0, a_guess * (1 - step): left, a_guess * (1 + step): right}
    it = 0
    while it < 40:
        it += 1
        ks = sorted(pts)
        es = [pts[k].e if not pts[k].uniform else np.inf for k in ks]
        jm = int(np.argmin(es))
        if pts[ks[0]].uniform and jm == 1:
            # crystal ends just below; refine bracket with smaller steps
            step *= 0.5
        if 0 < jm < len(ks) - 1 and not pts[ks[jm - 1]].uniform and not pts[ks[jm + 1]].uniform:
            break
        if jm == 0:
            anew = ks[0] * (1 - step)
            pts[anew] = solve(anew, pts[ks[0]])
        elif jm == len(ks) - 1:
            anew = ks[-1] * (1 + step)
            pts[anew] = solve(anew, pts[ks[-1]])
        else:
            # neighbour uniform: insert a midpoint
            k2 = ks[jm - 1] if pts[ks[jm - 1]].uniform else ks[jm + 1]
            anew = 0.5 * (ks[jm] + k2)
            pts[anew] = solve(anew, pts[ks[jm]])
    ks = sorted(pts)
    es = [pts[k].e if not pts[k].uniform else np.inf for k in ks]
    jm = int(np.argmin(es))
    a_lo, a_hi = ks[max(jm - 1, 0)], ks[min(jm + 1, len(ks) - 1)]
    o = optimize_a(kernel, a_lo, a_hi, N=N, rho=rho, seed=pts[ks[jm]], xatol_rel=xatol_rel, mask=mask,
                   verbose=verbose)
    o['prescan'] = [(k, pts[k].e, pts[k].uniform, pts[k].contrast) for k in ks]
    o['collapsed'] = bool(o['state'].uniform)
    o['time_total'] = time.time() - t0
    return o


# ----------------------------------------------------------------------------------------------------------
# full point (Q-A)
# ----------------------------------------------------------------------------------------------------------
QA_FRACS = (0.03, 0.05, 0.075, 0.10)


def run_point(kind, g, a_guess, seed=None, N=64, Kcut=80.0, fracs=QA_FRACS, twist_kfracs=(0.02, 0.04, 0.06),
              stab_Kcut=50.0, stab_nq=8, verbose=False, full=True):
    t0 = time.time()
    kern = Kernel(kind, g)
    o = find_astar(kern, a_guess, N=N, seed=seed, verbose=verbose)
    st = o['state']
    res = {'kind': kind, 'g': g, 'N': N, 'Kcut': Kcut}
    if o.get('collapsed'):
        res['collapsed_to_uniform'] = True
        res['prescan'] = o.get('prescan', o.get('scan'))
        return res, st
    res['collapsed_to_uniform'] = False
    res['astar'] = o['astar']
    res['astar_crosscheck'] = {'brent': o['astar'], 'parabolic_quartic5': o['a_parabolic_quartic5'],
                               'parabolic_3pt': o['a_parabolic_3pt'], 'dedA_root': o.get('a_dedA_root'),
                               'dedA_at_astar': o.get('dedA_at_astar'), 'brent_xatol': o['xatol'],
                               'brent_nfev': o['brent_nfev'], 'bracket': o['bracket'],
                               'd2e_da2': o['e_second_derivative_d2e_da2']}
    res['prescan'] = o['prescan']
    res['e_per_particle'] = st.eps
    res['e_per_area'] = st.e
    res['mu'] = st.mu
    res['pressure_mu_minus_eps'] = st.mu - st.eps
    res['contrast'] = st.contrast
    res['rho_max_peak'] = st.rho_max
    res['rho_min'] = st.rho_min
    res['modulation'] = st.modulation
    res['gs_resid'] = st.resid
    res['uniform_energy_pi_g_over_2'] = kern.uhat0 / 2.0
    res['E_crystal_minus_uniform_per_particle'] = st.eps - kern.uhat0 / 2.0
    res['ground_state'] = st.summary()
    if not full:
        res['time'] = time.time() - t0
        return res, st
    sp = speeds(st, 0.0, fracs, Kcut)
    if sp.get('unstable'):
        res['bdg_unstable'] = True
        res['speeds_a1'] = sp
        res['time'] = time.time() - t0
        return res, st
    res['c2'], res['cT'], res['c1'] = sp['c2'], sp['cT'], sp['c1']
    res['c2_gt_cT'] = bool(sp['c2'] > sp['cT'])
    res['F2'], res['Z21'], res['S2'] = sp['ref']['F2'], sp['ref']['Z21'], sp['ref']['S2']
    res['fsum_resid_max'] = sp['fsum_resid_max']
    res['static_resid_max'] = sp['static_resid_max']
    per = []
    for r in sp['per_q']:
        d = {'frac': r['frac'], 'qabs': r['qabs'], 'nbasis': r['nbasis'], 'fsum_resid': r['fsum_resid'],
             'static_resid': r['static_resid'], 'chi_cg': r['chi_cg'], 'chi_spec': r['chi_spec'],
             'full_rhoT_over_rho2': r.get('full_rhoT_over_rho2'), 'label1_is_second_even': r.get('label1_is_second_even'),
             's_norm_odd_block': r.get('s_norm_odd_block')}
        for lab in ('T', '2', '1'):
            d[lab] = {k: r[lab][k] for k in ('omega', 'Z', 'F', 'S', 'S_vs_chi_cg', 'parity', 'Px_cos', 'Py_cos',
                                             'v_over_q')}
        d['next_even'] = [{k: m[k] for k in ('omega', 'Z', 'F', 'S', 'parity')} for m in r['modes_even'][:6]]
        d['next_odd'] = [{k: m[k] for k in ('omega', 'Z', 'F', 'parity', 'Py_cos')} for m in r['modes_odd'][:4]]
        per.append(d)
    res['per_q_a1'] = per
    res['v_over_q'] = {lab: sp['v_over_q_' + lab] for lab in ('T', '2', '1')}
    res['lowest_gapped_omega_per_q'] = sp['lowest_gapped_omega_per_q']
    res['ref_q005'] = sp['ref']
    sp30 = speeds(st, 30.0, (0.05,), Kcut)
    r30 = sp30['per_q'][0]
    res['cT_30deg_kf005'] = r30['T']['omega'] / r30['qabs']
    res['q30_detail'] = {'c2_30_point': r30['2']['omega'] / r30['qabs'], 'c1_30_point': r30['1']['omega'] / r30['qabs'],
                         'F2_30': r30['2']['F'], 'fsum_resid': r30['fsum_resid'], 'static_resid': r30['static_resid'],
                         'mirror': r30['mirror'], 'rhoT_full_over_rho2': r30.get('full_rhoT_over_rho2'),
                         'T_parity': r30['T']['parity']}
    res['cT_a1_point_kf005'] = sp['ref']['cT_point']
    fsx = superfluid_fraction(st, (1.0, 0.0), True, twist_kfracs)
    fsy = superfluid_fraction(st, (0.0, 1.0), True, twist_kfracs)
    res['f_s'] = fsx['fs_lr']
    res['f_s_detail'] = {'lr_x': fsx['fs_lr'], 'lr_y': fsy['fs_lr'], 'twist_x': fsx['fs_twist'],
                         'twist_y': fsy['fs_twist'], 'twist_x_2pt': fsx['fs_twist_2pt'], 'twist_y_2pt': fsy['fs_twist_2pt'],
                         'twist_vs_lr_rel_x': fsx['twist_vs_lr_rel'], 'twist_vs_lr_rel_y': fsy['twist_vs_lr_rel'],
                         'isotropy_lr_rel': abs(fsx['fs_lr'] - fsy['fs_lr']) / abs(fsx['fs_lr']),
                         'twist_rows_x': fsx['twist'], 'twist_rows_y': fsy['twist']}
    res['gamma_checks'] = gamma_checks(st, min(Kcut, 60.0))
    if stab_nq:
        res['stability_scan'] = stability_scan(st, stab_Kcut, stab_nq)
    res['time'] = time.time() - t0
    return res, st


# ----------------------------------------------------------------------------------------------------------
# self tests
# ----------------------------------------------------------------------------------------------------------
def run_selftests(N=64, Kcut=80.0, verbose=True):
    T = {}
    t0 = time.time()
    # kernels
    ks = Kernel('step', 10.0)
    k6 = Kernel('g6', 35.0)
    kk = np.linspace(0.0, 400.0, 4001)
    T['kernel'] = {
        'step_uhat0_over_pi_g': float(ks.uhat(np.array([0.0]))[0] / (np.pi * 10.0)),
        'step_uhat_small_k_continuity': float(abs(ks.uhat(np.array([1e-6 * (1 - 1e-9)]))[0] - ks.uhat(np.array([1.0000001e-6]))[0]) / ks.uhat0),
        'g6_uhat0_over_g': float(k6.uhat(np.array([0.0]))[0] / 35.0),
        'g6_uhat0_over_g_analytic_2pi_Gamma13_over_6': float(TWOPI * gamma(1.0 / 3.0) / 6.0),
        'g6_quadrature_GL_vs_tanhsinh_vs_series_k0_400': k6.check_quadratures(kk),
        'g6_duhat_fd_check': float(np.max(np.abs((k6.uhat(kk[1:200] + 1e-5) - k6.uhat(kk[1:200] - 1e-5)) / 2e-5
                                                 - k6.duhat(kk[1:200]))) / k6.uhat0),
        'step_duhat_fd_check': float(np.max(np.abs((ks.uhat(kk[1:200] + 1e-5) - ks.uhat(kk[1:200] - 1e-5)) / 2e-5
                                                   - ks.duhat(kk[1:200]))) / ks.uhat0),
    }
    # uniform-state instability of the step kernel
    f = lambda k: -k * k / (4.0 * ks.uhat(np.array([k]))[0] / ks.g)
    r = minimize_scalar(f, bracket=(4.5, 4.8, 5.1), tol=1e-12)
    T['kernel']['step_g_inst'] = float(r.fun)
    T['kernel']['step_k_inst'] = float(r.x)
    f6 = lambda k: -k * k / (4.0 * k6.uhat(np.array([k]))[0] / k6.g)
    kg = np.linspace(2, 12, 2001)
    u6 = k6.uhat(kg) / k6.g
    neg = u6 < 0
    j = int(np.argmin(np.where(neg, -kg ** 2 / (4 * np.where(neg, u6, -1.0)), np.inf)))
    r6 = minimize_scalar(f6, bracket=(kg[j - 1], kg[j], kg[j + 1]), tol=1e-12)
    T['kernel']['g6_g_inst'] = float(r6.fun)
    T['kernel']['g6_k_inst'] = float(r6.x)
    # uniform energetics and Bogoliubov
    U = {}
    for kind, g in (('step', 10.0), ('g6', 5.0)):
        kern = Kernel(kind, g)
        a = 1.6
        st = uniform_state(hex_cell(a), kern, N=32)
        rec = {'e_per_area': st.e, 'e_expected_uhat0_over_2': kern.uhat0 / 2, 'mu': st.mu, 'mu_expected_uhat0': kern.uhat0,
               'rel_err_e': abs(st.e - kern.uhat0 / 2) / (kern.uhat0 / 2), 'rel_err_mu': abs(st.mu - kern.uhat0) / kern.uhat0,
               'resid': st.resid}
        if kind == 'step':
            rec['e_expected_pi_g_over_2'] = np.pi * g / 2
            rec['mu_expected_pi_g'] = np.pi * g
        q = np.array([0.05 * TWOPI / a, 0.0])
        b = bdg(st, q, 30.0, nlow=12)
        # analytic spectrum: every plane wave q+G decoupled
        mats = bdg_matrices(st, q, 30.0)
        eps_k = mats['kin']
        Uk = kern.uhat(np.sqrt(2 * eps_k))
        om_an = np.sort(np.sqrt(eps_k * (eps_k + 2 * Uk)))
        om_num = np.array(sorted([m['omega'] for m in b['modes_even']] + [m['omega'] for m in b['modes_odd']]))
        nn = min(len(om_num), 12)
        e0 = 0.5 * q @ q
        om0 = math.sqrt(e0 * (e0 + 2 * kern.uhat(np.array([math.sqrt(q @ q)]))[0]))
        rec['bogoliubov'] = {'omega_q_numeric': b['2']['omega'], 'omega_q_analytic': om0,
                             'rel_err': abs(b['2']['omega'] - om0) / om0, 'F_q_mode': b['2']['F'],
                             'Z_q_mode': b['2']['Z'], 'Z_expected_Ncell_eps_over_omega': st.Ncell * e0 / om0,
                             'max_F_other_modes': float(max(abs(m['F']) for m in (b['modes_even'][1:] + b['modes_odd']))),
                             'low_spectrum_max_rel_err': float(np.max(np.abs(np.sort(b['omega_low'])[:nn] - om_an[:nn]) / om_an[:nn])),
                             'fsum_resid': b['fsum_resid'], 'static_resid': b['static_resid'],
                             'chi_expected_2Ncell_over_(eps+2U)...': None}
        chi_an = 2 * st.Ncell * e0 / (om0 ** 2) * 1.0
        rec['bogoliubov']['chi_expected'] = chi_an
        rec['bogoliubov']['chi_rel_err'] = abs(b['chi_cg'] - chi_an) / chi_an
        del rec['bogoliubov']['chi_expected_2Ncell_over_(eps+2U)...']
        U[kind] = rec
    T['uniform'] = U
    if verbose:
        print('kernel/uniform done', time.time() - t0, flush=True)
    # crystal checks at g = 22
    kern = Kernel('step', 22.0)
    o = find_astar(kern, 1.457, N=N)
    st = o['state']
    a = o['astar']
    C = {'astar': a, 'e': st.e, 'mu': st.mu, 'resid': st.resid, 'newton_hist': st.info.get('newton', {}).get('hist')}
    # gradient / Hessian vs finite differences of the discrete energy
    rng = np.random.default_rng(1)
    g = st.grid
    d = rng.standard_normal(g.nm) * np.exp(-g.kin0 / 200.0)
    d = g.fromN(g.toN(d.astype(complex)).real.astype(complex))   # coefficients of a real function
    Ef = lambda t: _Ctx(g, st.c + t * d).E
    h = 1e-4
    g_fd = (Ef(h) - Ef(-h)) / (2 * h)
    g_an = 2.0 * g.A * rdot(d, st.ctx.Hc)
    h2 = 1e-3
    H_fd = (Ef(h2) - 2 * Ef(0.0) + Ef(-h2)) / h2 ** 2
    H_an = 2.0 * g.A * rdot(d, st.ctx.hess(d) + st.mu * d)
    C['gradient_fd_rel'] = abs(g_fd - g_an) / abs(g_an)
    C['hessian_fd_rel'] = abs(H_fd - H_an) / abs(H_an)
    # exact translation invariance and point-group symmetry of the discrete energy
    dvec = np.array([0.1234, 0.0456]) * a
    cs = st.c * np.exp(-1j * (g.Gx * dvec[0] + g.Gy * dvec[1]))
    Es = _Ctx(g, cs).E
    C['translation_invariance_rel'] = abs(Es - st.E) / st.E
    C['translated_state_resid'] = _Ctx(g, cs).resid
    C['symmetry_resid_rel'] = float(np.max(np.abs(g.symmetrize(st.c) - st.c)) / np.max(np.abs(st.c)))
    C['point_group_order'] = len(g.perms())
    C['psi_min_value'] = float(np.min(st.ctx.psiM.real))
    C['psi_imag_max'] = float(np.max(np.abs(st.ctx.psiM.imag)))
    # mu = dE/dN at fixed cell (Richardson)
    def E_at(rho):
        s2 = ground_state(st.cell, kern, N, rho, seed=st)
        return s2.E
    hh = 1e-3
    d1 = (E_at(1 + hh) - E_at(1 - hh)) / (2 * hh * st.A)
    d2 = (E_at(1 + 2 * hh) - E_at(1 - 2 * hh)) / (4 * hh * st.A)
    C['mu_vs_dEdN'] = {'mu': st.mu, 'dEdN_richardson': (4 * d1 - d2) / 3, 'rel': abs((4 * d1 - d2) / 3 - st.mu) / st.mu}
    # Gamma sector zero modes
    C['gamma_sector'] = gamma_checks(st, Kcut)
    # BdG: sum rules, transverse density weight, LR vs twist
    qx = np.array([0.05 * TWOPI / a, 0.0])
    b = bdg(st, qx, Kcut)
    C['bdg_q005_a1'] = {'fsum_resid': b['fsum_resid'], 'static_resid': b['static_resid'],
                        'fsum_resid_blocks': b['fsum_resid_blocks'], 'rhoT_full_over_rho2': b.get('full_rhoT_over_rho2'),
                        'rhoT_block_Z': b['T']['Z'], 's_norm_odd_block': b['s_norm_odd_block'],
                        'T_parity': b['T']['parity'], 'T_Px_cos': b['T']['Px_cos'], 'T_Py_cos': b['T']['Py_cos'],
                        'omega_T2_1': [b['T']['omega'], b['2']['omega'], b['1']['omega']],
                        'spectrum_full_vs_blocks_maxdiff_low': b['spectrum_full_vs_blocks_maxdiff_low']}
    q30 = 0.05 * TWOPI / a * np.array([math.cos(math.pi / 6), math.sin(math.pi / 6)])
    b30 = bdg(st, q30, Kcut)
    C['bdg_q005_30deg'] = {'mirror': b30['mirror'], 'rhoT_full_over_rho2': b30.get('full_rhoT_over_rho2'),
                           'T_parity': b30['T']['parity'], 'fsum_resid': b30['fsum_resid'], 'static_resid': b30['static_resid']}
    # independent algebra: full non-Hermitian 2n x 2n BdG eigenproblem (small basis)
    mats = bdg_matrices(st, qx, 40.0)
    L, X = mats['L'], mats['X']
    Mbig = np.block([[L + X, X], [-X, -(L + X)]])
    ev = np.linalg.eigvals(Mbig)
    evp = np.sort(ev.real[ev.real > 1e-9])
    b40 = bdg(st, qx, 40.0, chi_cg=False)
    om40 = np.array(b40['omega_low'])
    C['bdg_nonhermitian_2n_vs_cholesky_low8_maxrel'] = float(np.max(np.abs(evp[:8] - om40[:8]) / om40[:8]))
    C['bdg_nonhermitian_max_imag'] = float(np.max(np.abs(ev.imag)))
    # 3 gapless branches at small q
    vq = []
    for fr in (0.01, 0.02):
        bb = bdg(st, fr * TWOPI / a * np.array([1.0, 0.0]), 50.0, chi_cg=False)
        vq.append([bb['T']['omega'] / bb['qabs'], bb['2']['omega'] / bb['qabs'], bb['1']['omega'] / bb['qabs'],
                   bb['modes_even'][2]['omega'], bb['modes_odd'][1]['omega']])
    C['gapless_branches_v_over_q_at_0.01_0.02'] = vq
    for dname, dvec2 in (('x', (1.0, 0.0)), ('y', (0.0, 1.0))):
        fs = superfluid_fraction(st, dvec2, True)
        C['f_s_' + dname] = {'lr': fs['fs_lr'], 'twist': fs['fs_twist'], 'twist_2pt': fs['fs_twist_2pt'],
                             'rel': fs['twist_vs_lr_rel']}
    # dense plane-wave LR f_s as a second route (q = 0 sector, pseudo-inverse of L on psi0-complement)
    mats0 = bdg_matrices(st, np.zeros(2), 60.0)
    L0 = mats0['L']
    s0 = mats0['s']
    dpx = 1j * mats0['gx'] * s0
    wL, VL = sla.eigh(L0)
    keep = wL > 1e-8
    proj = VL.conj().T @ dpx
    C['f_s_dense_planewave_route'] = float(1.0 - 2.0 / st.Ncell * np.real(np.sum(np.abs(proj[keep]) ** 2 / wL[keep])))
    T['crystal_g22'] = C
    T['time'] = time.time() - t0
    return T


# ----------------------------------------------------------------------------------------------------------
# convergence study
# ----------------------------------------------------------------------------------------------------------
def conv_point(kind, g, a_guess, seed, Ns=(32, 48, 64, 96), Kcuts=(40.0, 50.0, 60.0, 70.0, 80.0, 90.0),
               N_bdg=64, verbose=False, fracs=QA_FRACS):
    kern = Kernel(kind, g)
    out = {'kind': kind, 'g': g, 'Ns': list(Ns), 'Kcuts': list(Kcuts), 'N_rows': [], 'K_rows': []}
    states = {}
    for N in Ns:
        o = find_astar(kern, a_guess, N=N, seed=seed)
        st = o['state']
        states[N] = st
        fs = superfluid_fraction(st, (1.0, 0.0), False)
        sp = speeds(st, 0.0, fracs, 70.0, chi_cg=True)
        row = {'N': N, 'Gmax': st.grid.Gmax, 'n_planewaves': int(st.grid.nm), 'astar': o['astar'],
               'a_dedA_root': o.get('a_dedA_root'), 'e': st.e, 'mu': st.mu, 'contrast': st.contrast,
               'rho_max': st.rho_max, 'f_s_lr': fs['fs_lr'], 'resid': st.resid,
               'c2': sp['c2'], 'cT': sp['cT'], 'c1': sp['c1'], 'F2': sp['ref']['F2'], 'Z21': sp['ref']['Z21'],
               'S2': sp['ref']['S2'], 'fsum_resid_max': sp['fsum_resid_max'], 'static_resid_max': sp['static_resid_max']}
        out['N_rows'].append(row)
        if verbose:
            print('  conv N', N, row['astar'], row['e'], row['c2'], flush=True)
    st = states[N_bdg]
    for Kc in Kcuts:
        sp = speeds(st, 0.0, fracs, Kc, chi_cg=True)
        sp30 = speeds(st, 30.0, (0.05,), Kc, chi_cg=False)
        row = {'Kcut': Kc, 'nbasis_q005': sp['per_q'][1]['nbasis'], 'c2': sp['c2'], 'cT': sp['cT'], 'c1': sp['c1'],
               'F2': sp['ref']['F2'], 'Z21': sp['ref']['Z21'], 'S2': sp['ref']['S2'],
               'cT_30': sp30['per_q'][0]['T']['omega'] / sp30['per_q'][0]['qabs'],
               'fsum_resid_max': sp['fsum_resid_max'], 'static_resid_max': sp['static_resid_max']}
        out['K_rows'].append(row)
        if verbose:
            print('  conv K', Kc, row['c2'], row['F2'], flush=True)
    # summary: max relative deviation from the finest setting, over settings >= production
    def maxdev(rows, keys, ref, sel):
        d = {}
        for k in keys:
            vals = [r[k] for r in rows if sel(r)]
            d[k] = float(max(abs(v - ref[k]) / abs(ref[k]) for v in vals))
        return d
    keysN = ['astar', 'e', 'mu', 'contrast', 'rho_max', 'f_s_lr', 'c2', 'cT', 'c1', 'F2', 'Z21', 'S2']
    refN = out['N_rows'][-1]
    out['maxreldev_N_ge_48_vs_finest'] = maxdev(out['N_rows'], keysN, refN, lambda r: r['N'] >= 48)
    out['maxreldev_N_all_vs_finest'] = maxdev(out['N_rows'], keysN, refN, lambda r: True)
    keysK = ['c2', 'cT', 'c1', 'F2', 'Z21', 'S2', 'cT_30']
    refK = out['K_rows'][-1]
    out['maxreldev_K_ge_60_vs_finest'] = maxdev(out['K_rows'], keysK, refK, lambda r: r['Kcut'] >= 60)
    out['maxreldev_K_all_vs_finest'] = maxdev(out['K_rows'], keysK, refK, lambda r: True)
    return out, states


# ----------------------------------------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------------------------------------
QA_STEP_G = [44.0, 28.0, 22.0, 16.0, 14.0, 13.5, 13.25, 13.0]
QA_CONT_G = [44.0, 40.0, 36.0, 32.0, 28.0, 25.0, 22.0, 20.0, 18.0, 16.0, 15.0, 14.5, 14.0, 13.75, 13.5, 13.25, 13.0]
PROD = {'N': 64, 'Kcut': 80.0, 'fracs': list(QA_FRACS), 'twist_kfracs_of_b1': [0.02, 0.04, 0.06],
        'stab_Kcut': 50.0, 'stab_nq': 8, 'gs_tol': 1e-11, 'brent_xatol_rel': 1e-7, 'rho': 1.0}


def gname(g):
    s = repr(float(g))
    return s[:-2] if s.endswith('.0') else s


def _load_json(p):
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def cmd_qa(args):
    os.makedirs(WORK, exist_ok=True)
    N, Kcut = PROD['N'], PROD['Kcut']
    states = {}
    sp = os.path.join(WORK, 'qa_states.npz')
    seed = None
    a_guess = 1.39
    prev_a = []
    for g in QA_CONT_G:
        nm = 'step_g' + gname(g)
        pj = os.path.join(WORK, 'qa_point_%s.json' % nm)
        report = g in QA_STEP_G
        cached = _load_json(pj)
        if cached is not None and os.path.exists(sp):
            d = load_state(sp, nm)
            if 'c' in d:
                st = state_from_saved(d, Kernel('step', g))
                states[nm] = st
                seed = st
                prev_a.append((g, cached['astar']))
                print('cached', nm, cached['astar'], flush=True)
                continue
        if len(prev_a) >= 2:
            (g1, a1), (g2, a2) = prev_a[-2], prev_a[-1]
            a_guess = a2 + (a2 - a1) / (g2 - g1) * (g - g2)
        elif len(prev_a) == 1:
            a_guess = prev_a[-1][1]
        print('point', nm, 'a_guess', a_guess, flush=True)
        res, st = run_point('step', g, a_guess, seed=seed, N=N, Kcut=Kcut, full=report,
                            stab_nq=PROD['stab_nq'] if report else 0, verbose=False)
        res['reported_point'] = report
        json_dump(res, pj)
        if res.get('collapsed_to_uniform'):
            print('COLLAPSE at', g, flush=True)
            break
        states[nm] = st
        seed = st
        prev_a.append((g, res['astar']))
        save_states(sp, states, extra={'settings_json': json.dumps(PROD)})
        print('  done', nm, res['astar'], res.get('c2'), res.get('cT'), res.get('time'), flush=True)
    # g6 point
    nm = 'g6_g35'
    pj = os.path.join(WORK, 'qa_point_%s.json' % nm)
    if _load_json(pj) is None:
        res, st = run_point('g6', 35.0, 1.5, seed=None, N=N, Kcut=Kcut, full=True, stab_nq=PROD['stab_nq'])
        # g6 quadrature agreement on the k values actually used
        kern = st.kernel
        kv = np.unique(np.round(st.grid.GM.ravel(), 12))
        mats = bdg_matrices(st, np.array([0.05 * TWOPI / res['astar'], 0.0]), Kcut)
        kv2 = np.sqrt(mats['gxK'] ** 2 + mats['gyK'] ** 2)
        res['g6_quadrature_check_used_k'] = {'padded_box': kern.check_quadratures(kv),
                                             'bdg_K_set_q005': kern.check_quadratures(kv2)}
        json_dump(res, pj)
        states[nm] = st
        save_states(sp, states, extra={'settings_json': json.dumps(PROD)})
        print('  done', nm, res['astar'], res.get('c2'), res.get('cT'), res.get('time'), flush=True)


def cmd_aroot(args):
    """re-solve every saved point at its envelope-derivative root a* and store it as <name>_aroot."""
    sp = os.path.join(WORK, 'qa_states.npz')
    z = np.load(sp)
    names = sorted(set(k.split('__')[0] for k in z.files if '__' in k and not k.split('__')[0].endswith('_aroot')))
    states, rep = {}, {}
    for nm in names:
        st = state_from_saved(load_state(sp, nm))
        states[nm] = st
        js = _load_json(os.path.join(WORK, 'qa_point_%s.json' % nm))
        ar = js['astar_crosscheck']['dedA_root']
        s2 = ground_state(hex_cell(ar), st.kernel, st.N, st.rho, seed=st, mask=st.grid.mask_index())
        states[nm + '_aroot'] = s2
        rep[nm] = {'a_brent': float(np.linalg.norm(st.cell[0])), 'a_root': ar, 'dedA_at_brent': dedA_envelope(st),
                   'dedA_at_root': dedA_envelope(s2), 'e_brent': st.e, 'e_root': s2.e, 'mu_brent': st.mu,
                   'mu_root': s2.mu, 'resid_root': s2.resid}
        print(nm, rep[nm]['a_root'], rep[nm]['dedA_at_root'], flush=True)
    extra = {k: z[k] for k in z.files if '__' not in k}
    save_states(sp, states, extra=extra)
    json_dump(rep, os.path.join(WORK, 'qa_aroot.json'))


def cmd_selftest(args):
    T = run_selftests(PROD['N'], PROD['Kcut'])
    json_dump(T, os.path.join(WORK, 'qa_selftests.json'))
    print('selftests done', T['time'])


def cmd_conv(args):
    sp = os.path.join(WORK, 'qa_states.npz')
    which = args[0] if args else 'all'
    jobs = [('step', 44.0, 'step_g44'), ('step', 13.0, 'step_g13'), ('g6', 35.0, 'g6_g35')]
    for kind, g, nm in jobs:
        if which != 'all' and which != nm:
            continue
        pj = os.path.join(WORK, 'qa_conv_%s.json' % nm)
        if _load_json(pj) is not None:
            continue
        d = load_state(sp, nm)
        seed = state_from_saved(d, Kernel(kind, g))
        a0 = float(np.linalg.norm(seed.cell[0]))
        t0 = time.time()
        out, _ = conv_point(kind, g, a0, seed, verbose=True)
        out['time'] = time.time() - t0
        json_dump(out, pj)
        print('conv done', nm, out['time'], flush=True)


def cmd_collect(args):
    res = {'settings': dict(PROD), 'points': {}, 'convergence': {}, 'selftests': None}
    res['settings'].update({
        'discretisation': 'plane-wave Galerkin on fractional grid; psi coefficients on the inscribed disc |G| < pi N/a '
                          'of the N x N FFT box; products on a 2N x 2N grid (exact, no aliasing)',
        'ground_state_solver': 'preconditioned L-BFGS on E with normalisation by scaling (only from far seeds), '
                               'then Newton-Krylov (projected PCG on the constrained Hessian) to ||H psi - mu psi||/||psi|| < 1e-11',
        'astar': 'bounded Brent on e(a)=E_cell/A at rho=1, xatol = 1e-7 a; cross-checks: 5-point quartic fit, '
                 'envelope-theorem de/da root',
        'bdg': 'dense plane waves |q+G| < Kcut, Cholesky route A = C C^T, K = C^T L C, full spectrum; mirror parity blocks; '
               'chi_static by matrix-free FFT CG in the same basis',
        'continuation_path_step_g': QA_CONT_G,
    })
    T = _load_json(os.path.join(WORK, 'qa_selftests.json'))
    res['selftests'] = T
    for kind, g, nm, key in [('step', g, 'step_g' + gname(g), gname(g)) for g in QA_STEP_G] + [('g6', 35.0, 'g6_g35', '35g6')]:
        d = _load_json(os.path.join(WORK, 'qa_point_%s.json' % nm))
        if d is not None:
            res['points'][key] = d
    cont = {}
    for g in QA_CONT_G:
        nm = 'step_g' + gname(g)
        d = _load_json(os.path.join(WORK, 'qa_point_%s.json' % nm))
        if d is not None and g not in QA_STEP_G:
            cont[gname(g)] = {k: d.get(k) for k in ('astar', 'e_per_particle', 'mu', 'contrast', 'collapsed_to_uniform',
                                                    'gs_resid', 'E_crystal_minus_uniform_per_particle')}
    res['continuation_intermediate_points'] = cont
    ar = _load_json(os.path.join(WORK, 'qa_aroot.json'))
    if ar is not None:
        res['astar_envelope_root_states'] = ar
    for nm, key in (('step_g44', 'step_44'), ('step_g13', 'step_13'), ('g6_g35', 'g6_35')):
        d = _load_json(os.path.join(WORK, 'qa_conv_%s.json' % nm))
        if d is not None:
            res['convergence'][key] = d
    # compact summary table (same numbers as in 'points')
    keys = ('astar', 'e_per_particle', 'mu', 'contrast', 'rho_max_peak', 'c2', 'cT', 'c1', 'F2', 'Z21', 'S2', 'f_s',
            'cT_30deg_kf005', 'fsum_resid_max', 'static_resid_max', 'c2_gt_cT')
    res['summary'] = {k: {kk: v.get(kk) for kk in keys} for k, v in res['points'].items()}
    res['summary_any_c2_gt_cT'] = bool(any(v.get('c2_gt_cT') for v in res['points'].values()))
    res['summary_max_c2_over_cT'] = max(v['c2'] / v['cT'] for v in res['points'].values() if 'c2' in v)
    json_dump(res, os.path.join(HERE, 'qa_results.json'))
    print('written', os.path.join(HERE, 'qa_results.json'))


def cmd_point(args):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--kind', default='step')
    ap.add_argument('--g', type=float, required=True)
    ap.add_argument('--a', type=float, required=True)
    ap.add_argument('--N', type=int, default=PROD['N'])
    ap.add_argument('--Kcut', type=float, default=PROD['Kcut'])
    ap.add_argument('--out', default=None)
    ns = ap.parse_args(args)
    res, st = run_point(ns.kind, ns.g, ns.a, N=ns.N, Kcut=ns.Kcut, verbose=True)
    if ns.out:
        json_dump(res, ns.out)
    print(json.dumps(jsonable({k: res.get(k) for k in ('astar', 'e_per_particle', 'mu', 'c2', 'cT', 'c1', 'F2', 'Z21',
                                                         'S2', 'f_s', 'cT_30deg_kf005')}), indent=1))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd, args = sys.argv[1], sys.argv[2:]
    {'qa': cmd_qa, 'selftest': cmd_selftest, 'conv': cmd_conv, 'collect': cmd_collect, 'point': cmd_point,
     'aroot': cmd_aroot}[cmd](args)


if __name__ == '__main__':
    main()
