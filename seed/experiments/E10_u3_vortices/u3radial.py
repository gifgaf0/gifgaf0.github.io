"""
E10 Route B (B2/B3): radial (equivariant) reduction of the 2D U(3) problem, used for the B3 scan (speed only).

Derivation (REPORT_B2B3.md §2.3).  With winding matrix N = diag(n_1, n_2, n_3) and g(theta) = exp(i theta N),
the fields
    H(r, theta) = g h(r),   W_r = g a_r(r) g^dag,   W_theta (coordinate) = g a(r) g^dag - N,
    What(r, theta) = g w(r) g^dag            (What = W_t - omega G: the Gauss-law field)
are invariant under spatial rotation combined with the gauge transformation g.  Then
    D_r H = g (h' + i a_r h),  D_theta H = g (i a h),  f_{r theta} = g (a' + i[a_r, a]) g^dag,
    D_theta What = g i[a, w] g^dag,  and  What H + omega H G = g (w h + omega h G).
The radial gauge a_r = 0 is reachable by an r-dependent gauge transformation u(r) with u(0) commuting with N.
In the frame where the string orientation is e_1 (N = diag(1,0,0)), the rotation generator becomes
G' = V^dag G V = m m^dag, m = (sin alpha, cos alpha, 0), where n = V e_1 = (cos alpha, sin alpha, 0) is the
orientation of the string in the original frame (PREREG §2 C5, B1 §3).  Any other n with the same |n_2| is
related by a symmetry of the ansatz.

Energies per unit length (PREREG §1 normalisation; 2D integral = 2 pi int r dr):
  T = 2 pi int r dr { Tr(a'^2)/r^2 + |h'|^2 + |a h|^2/r^2 + (lam^2/4) |1 - h h^dag|^2 }
  K_unit[w] = 2 pi int r dr { |w'|^2 + |[a, w]|^2/r^2 + |w h + h G'|^2 }            (omega = 1)
  I(h, a, alpha) = min_w K_unit       (convex quadratic: one sparse linear solve)
Twist dressing (W_z) gives the same quadratic form with omega -> -k, so J = I identically (§2.3).
B3 functional: E(k, q) = T + k^2 I + q^2 / (4 I);  omega = q / (2 I).
Envelope theorem: dE/d(h, a, alpha) = dT + (k^2 - omega^2) dK_unit|_{w = w*}.

Discretisation (as E9 option4_design): nodes r_j = j dr, j = 0..M; derivatives and all other terms at
midpoints with averaged node values; weights 2 pi r_m dr.  Boundary conditions: a(0) = N, rows of h with
n_a != 0 vanish at r = 0, w_{ab}(0) = 0 where n_a != n_b; h(r_max) = 1 (Dirichlet, matching the 2D box);
a(r_max), w(r_max) free.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu
from scipy.optimize import minimize
from u3common import EB, METRIC, herm, herm_params, herm_grad, dag

OPTS = dict(maxiter=20000, maxfun=40000, gtol=1e-9, ftol=1e-15, maxcor=20)


class Radial:
    def __init__(self, lam, N=(1, 0, 0), dr=0.05, rmax=20.0, relax_alpha=True):
        self.lam = float(lam); self.dr = dr; self.rmax = rmax
        self.M = M = int(round(rmax / dr))
        self.r = np.arange(M + 1) * dr
        self.rm = 0.5 * (self.r[1:] + self.r[:-1])
        self.w = 2 * np.pi * self.rm * dr
        self.N = np.diag(np.array(N, float)).astype(complex)
        self.nvec = np.array(N, float)
        self.relax_alpha = relax_alpha
        # free masks
        hmask = np.ones((M + 1, 3, 3), bool)
        hmask[M] = False
        for a_ in range(3):
            if self.nvec[a_] != 0:
                hmask[0, a_, :] = False
        self.hmask = hmask
        amask = np.ones((M + 1, 9), bool); amask[0] = False
        self.amask = amask
        wmask = np.ones((M + 1, 9), bool)
        for p in range(9):
            Ep = EB[p]; idx = np.argwhere(np.abs(Ep) > 0)
            for (x, y) in idx:
                if self.nvec[x] != self.nvec[y]:
                    wmask[0, p] = False
        self.wmask = wmask
        self.wfree = np.nonzero(wmask.ravel())[0]
        self.nh = 2 * hmask.sum(); self.na = amask.sum()
        # sparse pattern for the w-system (one 18x18 block per midpoint)
        loc = np.arange(18)
        rows = (9 * np.arange(M)[:, None, None] + loc[None, :, None]) + 0 * loc[None, None, :]
        cols = (9 * np.arange(M)[:, None, None] + loc[None, None, :]) + 0 * loc[None, :, None]
        self._rows = rows.ravel(); self._cols = cols.ravel()
        self.nw = 9 * (M + 1)
        self.alpha_fixed = np.pi / 4

    # ---------------- packing ----------------
    def pack(self, h, ap, alpha=None):
        v = [h[self.hmask].real, h[self.hmask].imag, ap[self.amask]]
        if self.relax_alpha:
            v.append([alpha if alpha is not None else self.alpha_fixed])
        return np.concatenate(v)

    def unpack(self, x):
        M = self.M; nh2 = self.nh // 2
        h = np.zeros((M + 1, 3, 3), complex)
        h[M] = np.eye(3)
        h[self.hmask] = x[:nh2] + 1j * x[nh2:2 * nh2]
        ap = np.zeros((M + 1, 9))
        ap[0] = herm_params(self.N)
        ap[self.amask] = x[2 * nh2:2 * nh2 + self.na]
        alpha = x[-1] if self.relax_alpha else self.alpha_fixed
        return h, ap, alpha

    def grad_pack(self, gh, ga, galpha):
        v = [gh[self.hmask].real, gh[self.hmask].imag, ga[self.amask]]
        if self.relax_alpha:
            v.append([galpha])
        return np.concatenate(v)

    def initial(self, core=1.0, alpha=None):
        r = self.r
        h = np.zeros((self.M + 1, 3, 3), complex)
        ap = np.zeros((self.M + 1, 9))
        A = np.tanh(r / core) ** 2
        a = np.zeros((self.M + 1, 3, 3), complex)
        for k in range(3):
            n = self.nvec[k]
            h[:, k, k] = np.tanh(r / core) ** abs(n) if n != 0 else 1.0
            a[:, k, k] = n * (1 - A)
        h[self.M] = np.eye(3)
        ap = herm_params(a)
        return self.pack(h, ap, alpha)

    @staticmethod
    def Gp(alpha):
        m = np.array([np.sin(alpha), np.cos(alpha), 0.0])
        dm = np.array([np.cos(alpha), -np.sin(alpha), 0.0])
        return np.outer(m, m).astype(complex), (np.outer(dm, m) + np.outer(m, dm)).astype(complex)

    # ---------------- static energy ----------------
    def T_grad(self, h, ap):
        a = herm(ap); dr, w, rm = self.dr, self.w, self.rm
        hm = 0.5 * (h[1:] + h[:-1]); am = 0.5 * (a[1:] + a[:-1])
        dh = (h[1:] - h[:-1]) / dr; da = (a[1:] - a[:-1]) / dr
        Y2 = am @ hm
        Mx = np.eye(3) - hm @ dag(hm)
        wr2 = w / rm ** 2
        dens = (wr2 * np.sum(np.abs(da) ** 2, axis=(1, 2)) + w * np.sum(np.abs(dh) ** 2, axis=(1, 2))
                + wr2 * np.sum(np.abs(Y2) ** 2, axis=(1, 2)) + w * 0.25 * self.lam ** 2 * np.sum(np.abs(Mx) ** 2, axis=(1, 2)))
        T = dens.sum()
        Cda = 2 * wr2[:, None, None] * da
        Cdh = 2 * w[:, None, None] * dh
        Ca_m = 2 * wr2[:, None, None] * (Y2 @ dag(hm))
        Ch_m = 2 * wr2[:, None, None] * (am @ Y2) - self.lam ** 2 * w[:, None, None] * (Mx @ hm)
        Ga = np.zeros_like(a); Gh = np.zeros_like(h)
        Ga[:-1] += -Cda / dr + 0.5 * Ca_m; Ga[1:] += Cda / dr + 0.5 * Ca_m
        Gh[:-1] += -Cdh / dr + 0.5 * Ch_m; Gh[1:] += Cdh / dr + 0.5 * Ch_m
        return T, Gh, herm_grad(Ga), dens

    # ---------------- Gauss-law (unit omega) ----------------
    def K_system(self, h, ap, alpha):
        a = herm(ap); w, rm, dr = self.w, self.rm, self.dr
        hm = 0.5 * (h[1:] + h[:-1]); am = 0.5 * (a[1:] + a[:-1])
        Gp, _ = self.Gp(alpha)
        comm = np.einsum('mab,pbc->mpac', am, EB) - np.einsum('pab,mbc->mpac', EB, am)
        Cm = np.real(np.einsum('mpab,mqab->mpq', comm.conj(), comm))
        Mh = hm @ dag(hm)
        Nm = np.real(np.einsum('pab,qbc,mca->mpq', EB, EB, Mh))
        Q = (w / rm ** 2)[:, None, None] * Cm + w[:, None, None] * Nm
        Dm = (w / dr ** 2)[:, None, None] * METRIC[None]
        B = np.empty((self.M, 18, 18))
        B[:, :9, :9] = Dm + 0.25 * Q; B[:, 9:, 9:] = Dm + 0.25 * Q
        B[:, :9, 9:] = -Dm + 0.25 * Q; B[:, 9:, :9] = -Dm + 0.25 * Q
        A = sp.csc_matrix((B.ravel(), (self._rows, self._cols)), shape=(self.nw, self.nw))
        s = hm @ Gp
        bm = w[:, None] * np.real(np.einsum('pab,mba->mp', EB, s @ dag(hm)))
        b = np.zeros((self.M + 1, 9)); b[:-1] += 0.5 * bm; b[1:] += 0.5 * bm
        c = float(np.sum(w * np.sum(np.abs(s) ** 2, axis=(1, 2))))
        return A, b.ravel(), c

    def K_solve(self, h, ap, alpha):
        A, b, c = self.K_system(h, ap, alpha)
        f = self.wfree
        Aff = A[f][:, f].tocsc()
        x = np.zeros(self.nw)
        x[f] = splu(Aff).solve(-b[f])
        I = c + b @ x
        return float(I), x.reshape(self.M + 1, 9)

    def K_eval_grad(self, h, ap, alpha, wp):
        """K_unit at fixed w, its density per midpoint, and gradients wrt h, a, alpha (envelope)."""
        a = herm(ap); X = herm(wp); w, rm, dr = self.w, self.rm, self.dr
        hm = 0.5 * (h[1:] + h[:-1]); am = 0.5 * (a[1:] + a[:-1]); Xm = 0.5 * (X[1:] + X[:-1])
        dX = (X[1:] - X[:-1]) / dr
        Gp, dGp = self.Gp(alpha)
        Z = am @ Xm - Xm @ am
        Y = Xm @ hm + hm @ Gp
        wr2 = w / rm ** 2
        dens = (w * np.sum(np.abs(dX) ** 2, axis=(1, 2)) + wr2 * np.sum(np.abs(Z) ** 2, axis=(1, 2))
                + w * np.sum(np.abs(Y) ** 2, axis=(1, 2)))
        Ch_m = 2 * w[:, None, None] * (Xm @ Y + Y @ Gp)
        Ca_m = 2 * wr2[:, None, None] * (Z @ Xm - Xm @ Z)
        galpha = float(np.sum(2 * w * np.real(np.einsum('mba,mbc,ca->m', Y.conj(), hm, dGp))))
        Gh = np.zeros_like(h); Ga = np.zeros_like(a)
        Gh[:-1] += 0.5 * Ch_m; Gh[1:] += 0.5 * Ch_m
        Ga[:-1] += 0.5 * Ca_m; Ga[1:] += 0.5 * Ca_m
        return float(dens.sum()), dens, Gh, herm_grad(Ga), galpha

    # ---------------- B3 functional ----------------
    def make_fg(self, k, q, store=None):
        k2 = k * k

        def fg(x):
            h, ap, alpha = self.unpack(x)
            T, Gh, Ga, _ = self.T_grad(h, ap)
            if k == 0 and q == 0:
                return T, self.grad_pack(Gh, Ga, 0.0)
            I, wp = self.K_solve(h, ap, alpha)
            _, _, Kh, Ka, Kal = self.K_eval_grad(h, ap, alpha, wp)
            coef = k2 - (q * q / (4 * I * I) if q != 0 else 0.0)
            E = T + k2 * I + (q * q / (4 * I) if q != 0 else 0.0)
            if store is not None:
                store['I'] = I
            return E, self.grad_pack(Gh + coef * Kh, Ga + coef * Ka, coef * Kal)
        return fg

    def solve(self, k, q, x0, opts=None):
        fg = self.make_fg(k, q)
        res = minimize(fg, x0, jac=True, method='L-BFGS-B', options=opts or OPTS)
        return res

    # ---------------- observables ----------------
    def observables(self, x, k, q):
        h, ap, alpha = self.unpack(x)
        T, _, _, Tdens = self.T_grad(h, ap)
        I, wp = self.K_solve(h, ap, alpha)
        K, kd, *_ = self.K_eval_grad(h, ap, alpha, wp)
        omega = q / (2 * I) if q != 0 else 0.0
        E = T + k * k * I + (q * q / (4 * I) if q != 0 else 0.0)
        rm = self.rm
        tot = kd.sum()
        leak = float(kd[rm > self.rmax - 4.0].sum() / tot) if tot > 0 else 0.0
        rq_rms = float(np.sqrt(np.sum(kd * rm ** 2) / tot)) if tot > 0 else float('nan')
        cum = np.cumsum(kd) / tot if tot > 0 else None
        rq_half = float(np.interp(0.5, cum, self.r[1:])) if tot > 0 else float('nan')
        d2 = np.abs(np.linalg.det(h)) ** 2
        idx = np.nonzero(d2 >= 0.5)[0]
        if len(idx) and idx[0] > 0:
            j = idx[0]; r_core = float(self.r[j - 1] + (0.5 - d2[j - 1]) / (d2[j] - d2[j - 1]) * self.dr)
        else:
            r_core = float('nan')
        # Tr B flux: f_xy = (1/r) a'  -> int Tr B d^2x = 2 pi int Tr(-a') dr = 2 pi Tr(a(0) - a(rmax))
        a = herm(ap)
        flux = float(2 * np.pi * np.real(np.trace(a[0] - a[-1])))
        return dict(E=float(E), T=float(T), I=float(I), omega=float(omega), alpha=float(alpha),
                    alpha_mod=float(np.mod(alpha, np.pi)), sin2cos2=float((np.sin(alpha) * np.cos(alpha)) ** 2),
                    leak=leak, r_charge_rms=rq_rms, r_charge_half=rq_half, r_core=r_core, flux_TrB=flux,
                    K_check=float(K - I))

    def profiles(self, x):
        h, ap, alpha = self.unpack(x)
        return h, herm(ap), alpha


def fd_check_radial(lam=1.0, k=0.3, q=1.7, seed=0, ncoord=40, eps=1e-4, dr=0.1, rmax=12.0):
    """Full outer gradient (with inner linear solve) against a 5-point FD stencil at random coordinates."""
    R = Radial(lam, dr=dr, rmax=rmax, relax_alpha=True)
    rng = np.random.default_rng(seed)
    x = R.initial(alpha=0.6) + 0.05 * rng.normal(size=R.initial().size)
    fg = R.make_fg(k, q)
    _, g = fg(x)
    nh2 = R.nh // 2
    idx = np.concatenate([rng.choice(np.arange(0, nh2), 12, replace=False),
                          rng.choice(np.arange(nh2, 2 * nh2), 12, replace=False),
                          rng.choice(np.arange(2 * nh2, 2 * nh2 + R.na), ncoord - 25, replace=False),
                          [x.size - 1]])
    worst = 0.0; rows = []
    for i in idx:
        def E(d):
            xx = x.copy(); xx[i] += d; return fg(xx)[0]
        fd = (-E(2 * eps) + 8 * E(eps) - 8 * E(-eps) + E(-2 * eps)) / (12 * eps)
        err = abs(fd - g[i]) / (abs(fd) + 1e-8)
        worst = max(worst, err); rows.append((int(i), float(g[i]), float(fd), float(err)))
    return worst, rows
