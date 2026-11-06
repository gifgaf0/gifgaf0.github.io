"""
E10 Route B (B2/B3): 2D (x, y) lattice gauge discretisation of the U(3) single-coupling model (PREREG_B2B3 §1).

  T[H, W] = int d^2x Tr[ 1/2 f_ij f_ij + (D_i H)(D_i H)^dag + (lam^2/4)(1 - H H^dag)^2 ],
  D_i H = d_i H + i W_i H,  f_ij = d_i W_j - d_j W_i + i[W_i, W_j].

Lattice (style of E9 gl3.py): L x L sites, spacing h, coordinates (i - (L-1)/2) h (the string axis sits at a
plaquette centre).  H (complex 3x3) on sites; link matrices U_mu(x) = exp(i h W_mu(x)) with W_mu Hermitian
(9 real parameters per link) on links x -> x + mu.  Then
  kinetic   sum_links |U_mu(x) H(x+mu) - H(x)|^2                    (-> h^2 sum |D_mu H|^2)
  magnetic  (2/h^2) sum_plaq Re Tr(1 - U_x(x) U_y(x+x) U_x(x+y)^dag U_y(x)^dag)   (-> h^2 sum Tr f_xy^2)
  potential h^2 (lam^2/4) sum_sites |1 - H H^dag|^2
This is exactly invariant under lattice gauge transformations H -> Omega H, U -> Omega(x) U Omega(x+mu)^dag.
Boundary: H fixed (Dirichlet) on the outermost ring of sites to the vacuum with the string's winding;
all link variables free.

Gauss law (PREREG §2 C5, §3): with H(t) = U(t) H U(t)^dag, U(t) = exp(-i omega t G), and W_i rotated likewise,
the kinetic energy is K = int Tr[ (D_i What)^2 + |What H + omega H G|^2 ],  What = W_t - omega G
(derivation in REPORT_B2B3.md §2.3).  On the lattice
  K = sum_links |U What(x+mu) U^dag - What(x)|^2 + h^2 sum_sites |What H + omega H G|^2 ,
a convex quadratic in What, minimised by conjugate gradients.  K_min = omega^2 I.
All gradients analytic (exp derivative by Daleckii-Krein in the eigenbasis of h W).
"""
import numpy as np
from scipy.optimize import minimize
from u3common import EB, METRIC, herm, herm_params, herm_grad, dag, G_DIAG

OPTS2D = dict(maxiter=30000, maxfun=60000, gtol=1e-8, ftol=1e-15, maxcor=20)


def expi_herm(X):
    """U = exp(i X) for Hermitian X (..., 3, 3); returns U, eigenvalues, eigenvectors."""
    mu, V = np.linalg.eigh(X)
    U = (V * np.exp(1j * mu)[..., None, :]) @ dag(V)
    return U, mu, V


def expi_pullback(A, mu, V):
    """Given dE = Re Tr(A^dag dU), U = exp(iX): return C with dE = Re Tr(C^dag dX)."""
    d = mu[..., :, None] - mu[..., None, :]
    s = mu[..., :, None] + mu[..., None, :]
    Gam = 1j * np.exp(0.5j * s) * np.sinc(d / (2 * np.pi))
    At = dag(V) @ A @ V
    B = At * np.conj(Gam)
    return V @ B @ dag(V)


class Lattice2D:
    def __init__(self, lam, L=160, h=0.25):
        self.lam, self.L, self.h = float(lam), L, h
        ax = (np.arange(L) - (L - 1) / 2) * h
        self.x, self.y = np.meshgrid(ax, ax, indexing='ij')
        self.r = np.hypot(self.x, self.y); self.th = np.arctan2(self.y, self.x)
        bd = np.zeros((L, L), bool); bd[0, :] = bd[-1, :] = bd[:, 0] = bd[:, -1] = True
        self.bd = bd
        self.Hb = None          # boundary values (L, L, 3, 3); only bd sites used
        self.nH = 2 * 9 * int((~bd).sum())
        self.half_width = L * h / 2
        # distance of each site to the box edge (|x| or |y| = half_width)
        self.edge_dist = self.half_width - np.maximum(np.abs(self.x), np.abs(self.y))

    # ---------- packing: H on interior sites (re, im), W on all links (2, L, L, 9) ----------
    def pack(self, H, Wp):
        Hi = H[~self.bd]
        return np.concatenate([Hi.real.ravel(), Hi.imag.ravel(), Wp.ravel()])

    def unpack(self, v):
        L = self.L; n = self.nH // 2
        H = self.Hb.copy()
        H[~self.bd] = (v[:n] + 1j * v[n:2 * n]).reshape(-1, 3, 3)
        Wp = v[2 * n:].reshape(2, L, L, 9)
        return H, Wp

    def gpack(self, GH, GW):
        Gi = GH[~self.bd]
        return np.concatenate([Gi.real.ravel(), Gi.imag.ravel(), GW.ravel()])

    def links(self, Wp):
        return expi_herm(self.h * herm(Wp))

    # ---------- static energy ----------
    def T_parts(self, H, U):
        """Energy pieces and gradients wrt H (complex) and U (A-form: dE = Re Tr(A^dag dU))."""
        h, L = self.h, self.L
        GH = np.zeros_like(H); AU = np.zeros_like(U)
        Ek = 0.0
        Ux, Uy = U[0], U[1]
        D = Ux[:-1] @ H[1:] - H[:-1]
        Ek += np.sum(np.abs(D) ** 2)
        GH[1:] += 2 * dag(Ux[:-1]) @ D; GH[:-1] += -2 * D; AU[0, :-1] += 2 * D @ dag(H[1:])
        D = Uy[:, :-1] @ H[:, 1:] - H[:, :-1]
        Ek += np.sum(np.abs(D) ** 2)
        GH[:, 1:] += 2 * dag(Uy[:, :-1]) @ D; GH[:, :-1] += -2 * D; AU[1, :, :-1] += 2 * D @ dag(H[:, 1:])
        Mx = np.eye(3) - H @ dag(H)
        Ev = h * h * 0.25 * self.lam ** 2 * np.sum(np.abs(Mx) ** 2)
        GH += -self.lam ** 2 * h * h * (Mx @ H)
        a = Ux[:-1, :-1]; b = Uy[1:, :-1]; c = Ux[:-1, 1:]; d = Uy[:-1, :-1]
        ab = a @ b; dc = d @ c
        P = ab @ dag(c) @ dag(d)
        trP = np.real(np.trace(P, axis1=-2, axis2=-1))
        cf = 2.0 / h ** 2
        Eb = cf * np.sum(3.0 - trP)
        AU[0, :-1, :-1] += -cf * (dc @ dag(b))
        AU[1, 1:, :-1] += -cf * (dag(a) @ dc)
        AU[0, :-1, 1:] += -cf * (dag(d) @ ab)
        AU[1, :-1, :-1] += -cf * (ab @ dag(c))
        return Ek, Eb, Ev, GH, AU, (3.0 - trP)

    def T_fg(self, v):
        H, Wp = self.unpack(v)
        U, mu, V = self.links(Wp)
        Ek, Eb, Ev, GH, AU, _ = self.T_parts(H, U)
        GW = self.h * herm_grad(expi_pullback(AU, mu, V))
        return Ek + Eb + Ev, self.gpack(GH, GW)

    # ---------- Gauss law ----------
    def K_parts(self, H, U, X, src, G=G_DIAG):
        """K at fixed What = X (L,L,3,3), source coefficient src (omega); gradients wrt X (params), H, U."""
        h = self.h
        GX = np.zeros(X.shape, complex); GH = np.zeros_like(H); AU = np.zeros_like(U)
        K = 0.0; dens = np.zeros((self.L, self.L))
        for mu_ in (0, 1):
            Um = U[mu_]
            if mu_ == 0:
                u, Xp, Xm = Um[:-1], X[1:], X[:-1]
            else:
                u, Xp, Xm = Um[:, :-1], X[:, 1:], X[:, :-1]
            D = u @ Xp @ dag(u) - Xm
            dd = np.sum(np.abs(D) ** 2, axis=(-1, -2))
            K += dd.sum()
            if mu_ == 0:
                GX[1:] += 2 * dag(u) @ D @ u; GX[:-1] += -2 * D; AU[0, :-1] += 4 * D @ u @ Xp
                dens[:-1] += 0.5 * dd; dens[1:] += 0.5 * dd
            else:
                GX[:, 1:] += 2 * dag(u) @ D @ u; GX[:, :-1] += -2 * D; AU[1, :, :-1] += 4 * D @ u @ Xp
                dens[:, :-1] += 0.5 * dd; dens[:, 1:] += 0.5 * dd
        Y = X @ H + src * (H @ G)
        ys = h * h * np.sum(np.abs(Y) ** 2, axis=(-1, -2))
        K += ys.sum(); dens += ys
        GX += 2 * h * h * (Y @ dag(H))
        GH += 2 * h * h * (X @ Y + src * (Y @ G))
        return K, herm_grad(GX), GH, AU, dens

    def K_solve(self, H, U, G=G_DIAG, x0=None, tol=1e-12, maxit=20000, omega=1.0):
        """Minimise K over What (conjugate gradients) at source omega. Returns K_min (= I for omega = 1),
        What params, info."""
        Lsh = (self.L, self.L, 9)
        Z = np.zeros((self.L, self.L, 3, 3), complex)
        _, g0, *_ = self.K_parts(H, U, Z, omega, G)
        b = 0.5 * g0                      # K = x^T A x + 2 b^T x + c

        def Av(p):
            _, gp, *_ = self.K_parts(H, U, herm(p), 0.0, G)
            return 0.5 * gp
        pre = 1.0 / (4.0 * METRIC.diagonal() + self.h ** 2)
        x = np.zeros(Lsh) if x0 is None else x0.copy()
        rres = -b - Av(x)
        z = rres * pre; p = z.copy(); rz = np.sum(rres * z)
        bn = np.sqrt(np.sum(b * b)); it = 0
        while it < maxit:
            if np.sqrt(np.sum(rres * rres)) <= tol * bn:
                break
            Ap = Av(p); al = rz / np.sum(p * Ap)
            x += al * p; rres -= al * Ap
            z = rres * pre; rz2 = np.sum(rres * z)
            p = z + (rz2 / rz) * p; rz = rz2; it += 1
        K, *_ = self.K_parts(H, U, herm(x), omega, G)
        return float(K), x, dict(cg_iters=it, rel_res=float(np.sqrt(np.sum(rres * rres)) / bn))

    # ---------- B3 functional (2D) ----------
    def make_fg(self, k, q, G=G_DIAG, state=None):
        st = state if state is not None else {}

        def fg(v):
            H, Wp = self.unpack(v)
            U, mu, V = self.links(Wp)
            Ek, Eb, Ev, GH, AU, _ = self.T_parts(H, U)
            I, xw, info = self.K_solve(H, U, G, x0=st.get('w'))
            st['w'] = xw; st['I'] = I
            _, _, KH, KAU, _ = self.K_parts(H, U, herm(xw), 1.0, G)
            coef = k * k - q * q / (4 * I * I)
            E = Ek + Eb + Ev + k * k * I + q * q / (4 * I)
            GW = self.h * herm_grad(expi_pullback(AU + coef * KAU, mu, V))
            return E, self.gpack(GH + coef * KH, GW)
        return fg, st

    # ---------- initial / transformed configurations ----------
    def from_radial(self, hprof, aprof, rgrid, N, V=None):
        """Build (H, W) from radial profiles h(r), a(r) (body frame) by the equivariant ansatz, then rotate
        globally by V (colour+flavour).  Link W evaluated at link midpoints."""
        Nm = np.diag(np.array(N, float)).astype(complex)
        nv = np.array(N, float)

        def interp(prof, rr):
            flat = prof.reshape(len(rgrid), -1)
            out = np.empty(rr.shape + (flat.shape[1],), complex)
            for c in range(flat.shape[1]):
                out[..., c] = np.interp(rr, rgrid, flat[:, c].real) + 1j * np.interp(rr, rgrid, flat[:, c].imag)
            return out.reshape(rr.shape + (3, 3))

        def gmat(th):
            return np.exp(1j * th[..., None] * nv) [..., :, None] * np.eye(3)
        g = gmat(self.th)
        H = g @ interp(hprof, self.r)
        Hb = g.copy() @ np.broadcast_to(np.eye(3), g.shape)
        Wp = np.zeros((2, self.L, self.L, 9))
        for mu_ in (0, 1):
            xm = self.x + (0.5 * self.h if mu_ == 0 else 0); ym = self.y + (0.5 * self.h if mu_ == 1 else 0)
            rr = np.hypot(xm, ym); th = np.arctan2(ym, xm)
            gm = gmat(th)
            Wth = gm @ interp(aprof, rr) @ dag(gm) - Nm          # coordinate component W_theta
            unit = (-np.sin(th) if mu_ == 0 else np.cos(th)) / rr
            Wp[mu_] = herm_params(Wth * unit[..., None, None])
        if V is not None:
            H = V @ H @ dag(V); Hb = V @ Hb @ dag(V)
            Wp = herm_params(V @ herm(Wp) @ dag(V))
        self.Hb = Hb
        return self.pack(H, Wp)

    def rotate_global(self, v, V):
        H, Wp = self.unpack(v)
        self.Hb = V @ self.Hb @ dag(V)
        H = V @ H @ dag(V)
        return self.pack(H, herm_params(V @ herm(Wp) @ dag(V)))

    def observables(self, v, G=G_DIAG, with_K=True):
        H, Wp = self.unpack(v)
        U, *_ = self.links(Wp)
        Ek, Eb, Ev, _, _, plaq = self.T_parts(H, U)
        out = dict(T=float(Ek + Eb + Ev), T_kin=float(Ek), T_mag=float(Eb), T_pot=float(Ev))
        # Tr B flux from plaquette phases: sum_plaq arg det(P) = h^2 sum Tr f_xy
        Ux, Uy = U[0], U[1]
        P = Ux[:-1, :-1] @ Uy[1:, :-1] @ dag(Ux[:-1, 1:]) @ dag(Uy[:-1, :-1])
        out['flux_TrB'] = float(np.sum(np.angle(np.linalg.det(P))))
        return out
