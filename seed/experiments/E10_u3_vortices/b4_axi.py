"""
E10 Route B, B4 (PREREG_B4 §3): axisymmetric (rho, z) lattice instrument for the U(3) single-coupling model
(PREREG_B2B3 §1, lam = 1, G = diag(0, 1, 0)).  Label: Exploration.

Ansatz (PREREG_B4 §3).  With beta = n phi - omega t, U(beta) = exp(i beta G) and co-moving fields (tilde dropped)
  H(rho, phi, z, t) = U H(rho, z) U^dag,  W_a = U W_a(rho, z) U^dag (a = rho, z),
  W_phi = U Wt_phi(rho, z) U^dag,  W_t = U Wt_t(rho, z) U^dag,
and the dressing combinations  P := Wt_phi + n G  (twist) and  X := Wt_t - omega G  (Gauss law), one finds
(derivation in REPORT_B4.md §2.2; the straight-string version is REPORT_B2B3 §2.3a,c):
  D_phi H = U i(P H - n H G) U^dag,   f_{a phi} = U (D_a P) U^dag,
  D_t H   = U i(X H + omega H G) U^dag, f_{t a} = -U (D_a X) U^dag, f_{phi t} = U i[P, X] U^dag.
Energy (metric d rho^2 + dz^2 + rho^2 dphi^2, measure 2 pi rho d rho dz):
  E_static = int 2 pi rho Tr[ f_rz^2 + |D_rho H|^2 + |D_z H|^2 + (lam^2/4)|1 - H H^dag|^2 ]
  E_twist  = int 2 pi rho (1/rho^2) Tr[ |D_a P|^2 + |P H - n H G|^2 ]
  K        = int 2 pi rho Tr[ |D_a X|^2 + (1/rho^2)|[P, X]|^2 + |X H + omega H G|^2 ],  K_min = omega^2 I(H, W, P)
  E_Q      = E_static + E_twist + Q^2 / (4 I),  omega = Q / (2 I)            (fixed Noether charge Q under G)
Wt_phi (equivalently P) is the phi component of the spatial gauge field: it is minimised over together with
H, W_rho, W_z (outer L-BFGS variable).  X is the only inner problem: a convex quadratic, solved by
preconditioned CG at every evaluation (warm-started).  Gradient of Q^2/(4I): envelope theorem,
d(Q^2/4I) = -omega^2 dK_unit|_{X = X*}.

Lattice (style of u3lattice.Lattice2D).  Sites rho_i = (i + 1/2) h, i = 0..Nr-1 (no site on the axis; no link
crosses it, which is the natural axis condition), z_j = -Z + j h, j = 0..Nz-1.  Dirichlet H = 1 on i = Nr-1
(rho = rho_max - h/2) and on j = 0, Nz-1 (z = -+Z).  Links U = exp(i h W) on rho- and z-links, all free;
P and X on all sites, free.  Discrete terms (m(rho) = 2 pi rho; flat mode: m = 2 pi R_L, rho^2 -> R_L^2):
  sum_links m(rho_l) |U H(x+mu) - H(x)|^2 + sum_plaq m(rho_p) (2/h^2) Re Tr(1 - P_plaq) + sum_sites m h^2 (lam^2/4)|1-HH^+|^2
  twist: sum_links m/rho_l^2 |U P(x+mu) U^+ - P(x)|^2 + sum_sites m h^2/rho^2 |P H - n H G|^2
  K: sum_links m |U X(x+mu) U^+ - X(x)|^2 + sum_sites m h^2 [ |[P, X]|^2/rho^2 + |X H + s H G|^2 ]
rho_l is the link midpoint for rho-links and the site rho for z-links; rho_p is the plaquette centre.
Exactly invariant under lattice gauge transformations Omega(rho, z): H -> Omega H, U -> Omega U Omega(x+mu)^+,
P -> Omega P Omega^+, X -> Omega X Omega^+.
'flat' mode (regression only): measure 2 pi R_L and metric R_L^2 constant, i.e. a straight string of length
2 pi R_L with twist k = n / R_L and charge per length Q / (2 pi R_L): E_flat = 2 pi R_L * calE_lattice(k, q).
"""
import os
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu
from u3common import EB, METRIC, herm, herm_params, herm_grad, dag, G_DIAG
from u3lattice import expi_herm, expi_pullback
import b4_fast as F

I3 = np.eye(3, dtype=complex)


class Axi:
    def __init__(self, lam=1.0, h=0.25, rho_max=40.0, zhalf=20.0, n=0, Q=0.0, mode='ring', R_L=None,
                 cg_tol=1e-10, cg_maxit=5000, fast=True):
        self.lam, self.h, self.n, self.Q = float(lam), float(h), int(n), float(Q)
        self.mode = mode; self.R_L = R_L
        self.rho_max, self.zhalf = rho_max, zhalf
        self.Nr = Nr = int(round(rho_max / h))
        self.Nz = Nz = int(round(2 * zhalf / h)) + 1
        self.rho = (np.arange(Nr) + 0.5) * h
        self.z = -zhalf + np.arange(Nz) * h
        self.RHO, self.Z = np.meshgrid(self.rho, self.z, indexing='ij')
        bd = np.zeros((Nr, Nz), bool); bd[-1, :] = True; bd[:, 0] = True; bd[:, -1] = True
        self.bd = bd
        self.Hb = np.broadcast_to(I3, (Nr, Nz, 3, 3)).copy()
        self.nHi = int((~bd).sum())
        self.G = G_DIAG
        if mode == 'ring':
            meas = lambda r: 2 * np.pi * r
            met = lambda r: r ** 2
        else:
            meas = lambda r: 2 * np.pi * R_L * np.ones_like(r)
            met = lambda r: R_L ** 2 * np.ones_like(r)
        h2 = h * h
        rs = self.RHO
        self.w_site = meas(rs) * h2                                   # (Nr, Nz)
        self.w_site_m = self.w_site / met(rs)                         # site weight / rho^2
        r_lr = (self.RHO[:-1] + self.RHO[1:]) / 2                     # rho-links (Nr-1, Nz)
        r_lz = self.RHO[:, :-1]                                       # z-links (Nr, Nz-1)
        self.w_link = (meas(r_lr), meas(r_lz))
        self.w_link_m = (meas(r_lr) / met(r_lr), meas(r_lz) / met(r_lz))
        r_p = (self.RHO[:-1, :-1] + self.RHO[1:, :-1]) / 2            # plaquette centres (Nr-1, Nz-1)
        self.w_plaq = meas(r_p) * 2.0 / h2
        self.shapes = dict(Wr=(Nr - 1, Nz, 9), Wz=(Nr, Nz - 1, 9), P=(Nr, Nz, 9))
        self.nW = (Nr - 1) * Nz * 9 + Nr * (Nz - 1) * 9
        self.cg_tol, self.cg_maxit = cg_tol, cg_maxit
        self.X = None; self.I = None; self.cg_last = 0; self.cg_total = 0; self._pre = None; self._pre_age = 10 ** 9
        self.nfev = 0
        self.fast = fast
        self._zeros_site = np.zeros((Nr, Nz))

    # ---------------- packing: H (interior, re/im), W_rho, W_z (params), Wt_phi (params) ----------------
    def pack(self, H, Wr, Wz, Pt):
        Hi = H[~self.bd]
        return np.concatenate([Hi.real.ravel(), Hi.imag.ravel(), Wr.ravel(), Wz.ravel(), Pt.ravel()])

    def unpack(self, v):
        n = self.nHi * 9
        H = self.Hb.copy()
        H[~self.bd] = (v[:n] + 1j * v[n:2 * n]).reshape(-1, 3, 3)
        o = 2 * n
        sWr = int(np.prod(self.shapes['Wr'])); sWz = int(np.prod(self.shapes['Wz']))
        Wr = v[o:o + sWr].reshape(self.shapes['Wr']); o += sWr
        Wz = v[o:o + sWz].reshape(self.shapes['Wz']); o += sWz
        Pt = v[o:].reshape(self.shapes['P'])
        return H, Wr, Wz, Pt

    def gpack(self, GH, GWr, GWz, GPt):
        Gi = GH[~self.bd]
        return np.concatenate([Gi.real.ravel(), Gi.imag.ravel(), GWr.ravel(), GWz.ravel(), GPt.ravel()])

    def Pfull(self, Pt):
        return self.hm(Pt) + self.n * self.G

    # ---------------- generic lattice terms ----------------
    @staticmethod
    def _sl(mu, A):
        """(x, x+mu) slices of a site array for direction mu (0: rho, 1: z)."""
        return (A[:-1], A[1:]) if mu == 0 else (A[:, :-1], A[:, 1:])

    def cov_H(self, H, U, GH, AU):
        E = 0.0
        for mu in (0, 1):
            w = self.w_link[mu][..., None, None]
            Hx, Hp = self._sl(mu, H)
            D = U[mu] @ Hp - Hx
            E += np.sum(self.w_link[mu] * np.sum(np.abs(D) ** 2, axis=(-1, -2)))
            gx, gp = self._sl(mu, GH)
            gp += 2 * w * (dag(U[mu]) @ D); gx -= 2 * w * D
            AU[mu] += 2 * w * (D @ dag(Hp))
        return E

    def cov_adj(self, X, U, wl, GX, AU, dens=None):
        """sum_links wl |U X(x+mu) U^+ - X(x)|^2; GX (complex, dE = Re Tr(GX^+ dX)), AU optional."""
        E = 0.0
        for mu in (0, 1):
            w = wl[mu]
            Xx, Xp = self._sl(mu, X)
            u = U[mu]
            UXp = u @ Xp
            D = UXp @ dag(u) - Xx
            dd = w * np.sum(np.abs(D) ** 2, axis=(-1, -2))
            E += dd.sum()
            if dens is not None:
                dx, dp = self._sl(mu, dens); dx += 0.5 * dd; dp += 0.5 * dd
            ww = w[..., None, None]
            gx, gp = self._sl(mu, GX)
            gp += 2 * ww * (dag(u) @ D @ u); gx -= 2 * ww * D
            if AU is not None:
                AU[mu] += 4 * ww * (D @ UXp)
        return E

    def plaq(self, U, AU):
        Ur, Uz = U
        a = Ur[:, :-1]; b = Uz[1:, :]; c = Ur[:, 1:]; d = Uz[:-1, :]
        ab = a @ b; dc = d @ c
        P = ab @ dag(c) @ dag(d)
        trP = np.real(np.trace(P, axis1=-2, axis2=-1))
        cf = self.w_plaq
        E = np.sum(cf * (3.0 - trP))
        cf = cf[..., None, None]
        AU[0][:, :-1] += -cf * (dc @ dag(b))
        AU[1][1:, :] += -cf * (dag(a) @ dc)
        AU[0][:, 1:] += -cf * (dag(d) @ ab)
        AU[1][:-1, :] += -cf * (ab @ dag(c))
        return E

    def hm(self, x):
        if self.fast:
            X = np.empty(x.shape[:-1] + (3, 3), complex); F.herm_nb(np.ascontiguousarray(x), X); return X
        return herm(x)

    def hg(self, C, scale=1.0):
        if self.fast:
            g = np.empty(C.shape[:-2] + (9,)); F.hgrad_nb(np.ascontiguousarray(C), g, scale); return g
        return scale * herm_grad(C)

    def links(self, Wr, Wz):
        if self.fast:
            out = []; eig = []
            for W in (Wr, Wz):
                mu, V = np.linalg.eigh(self.h * self.hm(W))
                U = np.empty(V.shape, complex); F.expi_from_eig(mu, V, U)
                out.append(U); eig.append((mu, V))
            return tuple(out), tuple(eig)
        Ur, mr, Vr = expi_herm(self.h * herm(Wr))
        Uz, mz, Vz = expi_herm(self.h * herm(Wz))
        return (Ur, Uz), ((mr, Vr), (mz, Vz))

    # ---------------- static + twist ----------------
    def static_twist(self, H, U, P, want_parts=False):
        if self.fast:
            return self._static_twist_fast(H, U, P)
        return self._static_twist_ref(H, U, P)

    def _static_twist_fast(self, H, U, P):
        GH = np.zeros_like(H); AU = [np.zeros_like(U[0]), np.zeros_like(U[1])]; GP = np.zeros_like(P)
        Ekin = F.link_H(H, U[0], U[1], self.w_link[0], self.w_link[1], GH, AU[0], AU[1])
        Emag = F.plaq(U[0], U[1], self.w_plaq, AU[0], AU[1])
        Epot, Etw_s = F.sites_static_twist(H, P, self.w_site, self.w_site_m, self.lam, float(self.n), GH, GP)
        Etw_l = F.link_adj(P, U[0], U[1], self.w_link_m[0], self.w_link_m[1], GP, AU[0], AU[1],
                           self._zeros_site, True, False)
        parts = dict(E_kin=Ekin, E_mag=Emag, E_pot=Epot, E_twist_links=Etw_l, E_twist_sites=Etw_s)
        return Ekin + Emag + Epot, Etw_l + Etw_s, GH, AU, GP, parts

    def _static_twist_ref(self, H, U, P):
        GH = np.zeros_like(H); AU = [np.zeros_like(U[0]), np.zeros_like(U[1])]; GP = np.zeros_like(P)
        Ekin = self.cov_H(H, U, GH, AU)
        Emag = self.plaq(U, AU)
        Mx = I3 - H @ dag(H)
        ws = self.w_site
        Epot = np.sum(ws * 0.25 * self.lam ** 2 * np.sum(np.abs(Mx) ** 2, axis=(-1, -2)))
        GH += -self.lam ** 2 * ws[..., None, None] * (Mx @ H)
        # twist
        Etw_l = self.cov_adj(P, U, self.w_link_m, GP, AU)
        Y = P @ H - self.n * (H @ self.G)
        wm = self.w_site_m
        Etw_s = np.sum(wm * np.sum(np.abs(Y) ** 2, axis=(-1, -2)))
        GH += 2 * wm[..., None, None] * (P @ Y - self.n * (Y @ self.G))
        GP += 2 * wm[..., None, None] * (Y @ dag(H))
        parts = dict(E_kin=Ekin, E_mag=Emag, E_pot=Epot, E_twist_links=Etw_l, E_twist_sites=Etw_s)
        return Ekin + Emag + Epot, Etw_l + Etw_s, GH, AU, GP, parts

    # ---------------- Gauss law ----------------
    def _wts(self, kind):
        """weights (link, commutator, site) of the quadratic form: 'K' Gauss law; 'tw' twist as a form in P."""
        if kind == 'K':
            return self.w_link, self.w_site_m, self.w_site
        return self.w_link_m, None, self.w_site_m

    def K_full(self, H, U, P, X, s, grads=True, dens=None, kind='K'):
        if self.fast:
            return self._K_full_fast(H, U, P, X, s, grads, dens, kind)
        return self._K_full_ref(H, U, P, X, s, grads, dens, kind)

    def _K_full_fast(self, H, U, P, X, s, grads, dens, kind):
        wl, wm, ws = self._wts(kind)
        GX = np.zeros_like(X)
        GH = np.zeros_like(H) if grads else X[:1, :1]
        AU = [np.zeros_like(U[0]), np.zeros_like(U[1])] if grads else [X[:1, :1], X[:1, :1]]
        GP = np.zeros_like(P) if grads else X[:1, :1]
        dd = dens if dens is not None else self._zeros_site
        X = np.ascontiguousarray(X)
        K = F.link_adj(X, U[0], U[1], wl[0], wl[1], GX, AU[0], AU[1], dd, grads, dens is not None)
        K += F.sites_K(X, H, P, ws, wm if wm is not None else ws, float(s), wm is not None, GX, GH, GP, dd,
                       grads, dens is not None)
        if not grads:
            return K, GX, None, None, None
        return K, GX, GH, AU, GP

    def _K_full_ref(self, H, U, P, X, s, grads=True, dens=None, kind='K'):
        """K at fixed X (Hermitian (Nr,Nz,3,3)) and source s; gradients wrt X, H, U (A-form), P.
        kind='tw': the twist form sum w_link_m |U X' U^+ - X|^2 + w_site_m |X H + s H G|^2 (no commutator)."""
        wl, wm, ws = self._wts(kind)
        GX = np.zeros_like(X); GH = np.zeros_like(H) if grads else None
        AU = [np.zeros_like(U[0]), np.zeros_like(U[1])] if grads else None
        GP = np.zeros_like(P) if grads else None
        K = self.cov_adj(X, U, wl, GX, AU, dens)
        if wm is not None:
            Z = P @ X - X @ P
            dz = wm * np.sum(np.abs(Z) ** 2, axis=(-1, -2))
            K += dz.sum()
            GX += 2 * wm[..., None, None] * (P @ Z - Z @ P)
        else:
            dz = 0.0
        Y = X @ H + s * (H @ self.G)
        dy = ws * np.sum(np.abs(Y) ** 2, axis=(-1, -2))
        K += dy.sum()
        GX += 2 * ws[..., None, None] * (Y @ dag(H))
        if dens is not None:
            dens += dz + dy
        if grads:
            if wm is not None:
                GP += 2 * wm[..., None, None] * (Z @ X - X @ Z)
            GH += 2 * ws[..., None, None] * (X @ Y + s * (Y @ self.G))
        return K, GX, GH, AU, GP

    def _Av(self, H, U, P, p, kind='K'):
        if self.fast:
            X = np.empty((self.Nr, self.Nz, 3, 3), complex); F.herm_nb(np.ascontiguousarray(p), X)
            _, gx, *_ = self.K_full(H, U, P, X, 0.0, grads=False, kind=kind)
            out = np.empty((self.Nr, self.Nz, 9)); F.hgrad_nb(gx, out, 0.5)
            return out
        _, gx, *_ = self.K_full(H, U, P, herm(p), 0.0, grads=False, kind=kind)
        return 0.5 * herm_grad(gx)

    def build_pre(self, H, U, P, kind='K'):
        """Componentwise scalar preconditioner: METRIC_pp * (weighted lattice Laplacian) + exact site diagonal."""
        Nr, Nz = self.Nr, self.Nz
        idx = np.arange(Nr * Nz).reshape(Nr, Nz)
        rows, cols, vals = [], [], []
        wl, wm, ws = self._wts(kind)
        for mu in (0, 1):
            ix, ip = self._sl(mu, idx); w = wl[mu]
            for (a, b, s_) in ((ix, ix, 1), (ip, ip, 1), (ix, ip, -1), (ip, ix, -1)):
                rows.append(a.ravel()); cols.append(b.ravel()); vals.append(s_ * w.ravel())
        Lap = sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(Nr * Nz,) * 2)
        HH = H @ dag(H)
        facs = []
        for p in range(9):
            Ep = EB[p]
            d1 = np.real(np.einsum('ab,xybc,ca->xy', Ep, HH, Ep))          # Re Tr(E_p H H^+ E_p)
            if wm is not None:
                C = P @ Ep - Ep @ P
                d2 = np.sum(np.abs(C) ** 2, axis=(-1, -2))
            else:
                d2 = 0.0
            diag = ws * d1 + (wm * d2 if wm is not None else 0.0) + 1e-12 * self.w_site
            A = METRIC[p, p] * Lap + sp.diags(diag.ravel())
            facs.append(splu(A.tocsc(), permc_spec='MMD_AT_PLUS_A'))
        return facs

    def apply_pre(self, r, pre):
        out = np.empty_like(r)
        rr = r.reshape(self.Nr * self.Nz, 9)
        oo = out.reshape(self.Nr * self.Nz, 9)
        for p in range(9):
            oo[:, p] = pre[p].solve(rr[:, p])
        return out

    def K_solve(self, H, U, P, x0=None, kind='K', s=1.0):
        """min_X of the quadratic form (kind 'K': K_unit, s = 1): returns its minimum, X params, CG iterations."""
        if kind == 'K':
            if self._pre is None or self._pre_age > 200 or self.cg_last > 60:
                self._pre = self.build_pre(H, U, P); self._pre_age = 0
            self._pre_age += 1
            pre = self._pre
        else:
            pre = self.build_pre(H, U, P, kind)
        Zr = np.zeros((self.Nr, self.Nz, 3, 3), complex)
        _, g0, *_ = self.K_full(H, U, P, Zr, s, grads=False, kind=kind)
        b = self.hg(g0, 0.5)
        x = np.zeros_like(b) if x0 is None else x0.copy()
        r = -b - self._Av(H, U, P, x, kind)
        z = self.apply_pre(r, pre); p = z.copy(); rz = np.sum(r * z)
        bn = np.sqrt(np.sum(b * b)); it = 0
        if bn == 0:
            self.cg_relres = 0.0
            return 0.0, x, 0
        while it < self.cg_maxit and np.sqrt(np.sum(r * r)) > self.cg_tol * bn:
            Ap = self._Av(H, U, P, p, kind); al = rz / np.sum(p * Ap)
            x += al * p; r -= al * Ap
            z = self.apply_pre(r, pre); rz2 = np.sum(r * z)
            p = z + (rz2 / rz) * p; rz = rz2; it += 1
        K, *_ = self.K_full(H, U, P, self.hm(x), s, grads=False, kind=kind)
        if kind == 'K':
            self.cg_last = it; self.cg_total += it
        self.cg_relres = float(np.sqrt(np.sum(r * r)) / bn)
        return float(K), x, it

    # ---------------- B4 functional ----------------
    def fg(self, v):
        self.nfev += 1
        H, Wr, Wz, Pt = self.unpack(v)
        U, eig = self.links(Wr, Wz)
        P = self.Pfull(Pt)
        S, Tw, GH, AU, GP, _ = self.static_twist(H, U, P)
        E = S + Tw
        if self.Q != 0:
            I, xw, _ = self.K_solve(H, U, P, self.X)
            self.X = xw; self.I = I
            _, _, KH, KAU, KP = self.K_full(H, U, P, self.hm(xw), 1.0, grads=True)
            om2 = (self.Q / (2 * I)) ** 2
            E += self.Q ** 2 / (4 * I)
            GH = GH - om2 * KH; GP = GP - om2 * KP
            AU = [AU[0] - om2 * KAU[0], AU[1] - om2 * KAU[1]]
        if self.fast:
            GWr = np.empty(self.shapes['Wr']); F.pullback(np.ascontiguousarray(AU[0]), eig[0][0], eig[0][1], self.h, GWr)
            GWz = np.empty(self.shapes['Wz']); F.pullback(np.ascontiguousarray(AU[1]), eig[1][0], eig[1][1], self.h, GWz)
        else:
            GWr = self.h * herm_grad(expi_pullback(AU[0], *eig[0]))
            GWz = self.h * herm_grad(expi_pullback(AU[1], *eig[1]))
        return float(E), self.gpack(GH, GWr, GWz, self.hg(GP))

    # ---------------- twist-only initial dressing for Wt_phi ----------------
    def twist_init(self, v):
        """Minimise E_twist over Wt_phi alone at fixed H, W (a convex quadratic in P = Wt_phi + n G with source
        -n H G; same preconditioned CG).  Used only to build starting configurations."""
        H, Wr, Wz, Pt = self.unpack(v)
        if self.n == 0:
            return self.pack(H, Wr, Wz, np.zeros(self.shapes['P']))
        U, _ = self.links(Wr, Wz)
        P0 = self.Pfull(np.zeros(self.shapes['P']))
        _, xp, it = self.K_solve(H, U, P0, herm_params(P0), kind='tw', s=-float(self.n))
        self.twist_init_cg = it
        return self.pack(H, Wr, Wz, xp - herm_params(self.n * self.G))

    # ---------------- observables ----------------
    def winding(self, H, U):
        """Gauge-invariant lattice winding of det H per plaquette (U(1) part of the links: det U)."""
        dH = np.linalg.det(H)
        du = (np.linalg.det(U[0]), np.linalg.det(U[1]))

        def th(mu):
            Hx, Hp = self._sl(mu, dH)
            return np.angle(np.conj(Hx) * du[mu] * Hp)
        tr, tz = th(0), th(1)
        s = tr[:, :-1] + tz[1:, :] - tr[:, 1:] - tz[:-1, :]
        uP = du[0][:, :-1] * du[1][1:, :] / du[0][:, 1:] / du[1][:-1, :]
        return np.rint((s - np.angle(uP)) / (2 * np.pi)).astype(int)

    def observables(self, v):
        H, Wr, Wz, Pt = self.unpack(v)
        U, _ = self.links(Wr, Wz)
        P = self.Pfull(Pt)
        S, Tw, _, _, _, parts = self.static_twist(H, U, P)
        out = dict(E_static=float(S), E_twist=float(Tw), **{k: float(x) for k, x in parts.items()})
        E = S + Tw
        nw = self.winding(H, U)
        pts = np.argwhere(nw != 0)
        rc = (self.RHO[:-1, :-1] + self.RHO[1:, :-1]) / 2; zc = (self.Z[:-1, :-1] + self.Z[:-1, 1:]) / 2
        out['windings'] = [dict(rho=float(rc[i, j]), z=float(zc[i, j]), w=int(nw[i, j])) for i, j in pts]
        out['n_vortex_plaquettes'] = int(len(pts))
        out['R_f'] = float(rc[pts[0][0], pts[0][1]]) if len(pts) == 1 else (
            float(np.mean([rc[i, j] for i, j in pts])) if len(pts) else None)
        out['z_f'] = float(zc[pts[0][0], pts[0][1]]) if len(pts) == 1 else None
        dens = np.zeros((self.Nr, self.Nz))
        I, xw, it = self.K_solve(H, U, P, self.X)
        if self.Q != 0:
            self.X = xw
            E += self.Q ** 2 / (4 * I)
        if I > 1e-12:
            K, *_ = self.K_full(H, U, P, herm(xw), 1.0, grads=False, dens=dens)
            om = self.Q / (2 * I)
            tot = dens.sum()
            Rq = float(np.sum(dens * self.RHO) / tot); zq = float(np.sum(dens * self.Z) / tot)
            rq = float(np.sqrt(np.sum(dens * ((self.RHO - Rq) ** 2 + (self.Z - zq) ** 2)) / tot))
            edge = (self.RHO > self.rho_max - 4.0) | (np.abs(self.Z) > self.zhalf - 4.0)
            leak = float(dens[edge].sum() / tot)
            M = I3 - dag(H) @ H
            trM = np.real(np.trace(M, axis1=-2, axis2=-1))
            pG = np.real(M[..., 1, 1])
            ok = trM > 1e-10
            pp = np.where(ok, pG / np.where(ok, trM, 1.0), 0.0)
            tau_loc = 4 * pp * (1 - pp)
            tau = float(np.sum((dens * tau_loc)[ok]) / np.sum(dens[ok])) if ok.any() else float('nan')
            out.update(I=float(I), omega=float(om), omega_over_mbulk=float(om / min(1.0, self.lam)), R_q=Rq, z_q=zq,
                       r_q=rq, leak=leak if self.Q != 0 else 0.0, leak_unit_density=leak, tau=tau,
                       K_check=float(K - I), cg_iters=int(it), cg_relres=float(self.cg_relres),
                       weights='charge density' if self.Q != 0 else 'unit (omega = 1) Gauss-law density (Q = 0)')
        else:
            out.update(I=float(I), omega=None, omega_over_mbulk=None, R_q=None, z_q=None, r_q=None, leak=0.0, tau=None)
        out['E'] = float(E)
        # core-scale radius of the det H deficit (descriptive): |det H|^2 < 0.5 region extent
        d2 = np.abs(np.linalg.det(H)) ** 2
        low = d2 < 0.5
        out['detH_min'] = float(np.sqrt(d2.min()))
        out['detH_low_rho_range'] = [float(self.RHO[low].min()), float(self.RHO[low].max())] if low.any() else None
        return out

    def fields(self, v):
        H, Wr, Wz, Pt = self.unpack(v)
        return dict(H=H, Wr=Wr, Wz=Wz, Pt=Pt)


# ---------------- starting configurations ----------------
def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def ring_start(A, hprof, aprof, rgrid, R0, V, z0=0.0, seg_mask=(2.0, 8.0)):
    """Map the straight string (radial profiles h(r), a(r), body frame N = diag(1,0,0), global orientation V)
    onto a ring of radius R0 in the z = z0 plane: distance d to the core circle, angle chi = atan2(z, rho - R0).
      H = V g(chi) h(d) V^+,  W_chi = V (g a(d) g^+ - N) V^+ (coordinate), W_rho = -W_chi sin(chi)/d, W_z = W_chi cos(chi)/d
    at link midpoints, U = exp(i h W).  Then a smooth lattice gauge transformation Omega = V exp(-i chi_ext N) V^+
    moves the winding off the outer edges (chi_ext = chi * m, m a smooth mask that vanishes within seg_mask[0] of the
    segment {z = z0, 0 <= rho <= R0} (the branch cut of chi) and is 1 beyond seg_mask[1]); H = 1 is then imposed on the
    Dirichlet sites (the mismatch there is the string tail, |h(d) - 1| at d >= 8).
    The winding thus sits, gauge-equivalently, on the axis (where H is free)."""
    N = np.diag([1.0, 0.0, 0.0]).astype(complex); nv = np.array([1.0, 0.0, 0.0])

    def interp(prof, rr):
        flat = prof.reshape(len(rgrid), -1)
        out = np.empty(rr.shape + (flat.shape[1],), complex)
        for c in range(flat.shape[1]):
            out[..., c] = np.interp(rr, rgrid, flat[:, c].real) + 1j * np.interp(rr, rgrid, flat[:, c].imag)
        return out.reshape(rr.shape + (3, 3))

    def gmat(th):
        return np.exp(1j * th[..., None] * nv)[..., :, None] * np.eye(3)

    def chi_ext(rho, z):
        chi = np.arctan2(z - z0, rho - R0)
        dseg = np.where(rho < R0, np.abs(z - z0), np.hypot(rho - R0, z - z0))
        return chi * smoothstep((dseg - seg_mask[0]) / (seg_mask[1] - seg_mask[0]))

    rho, z = A.RHO, A.Z
    d = np.hypot(rho - R0, z - z0); chi = np.arctan2(z - z0, rho - R0)
    H = V @ (gmat(chi) @ interp(hprof, d)) @ dag(V)
    Ws = []
    for mu in (0, 1):
        if mu == 0:
            rm, zm = (rho[:-1] + rho[1:]) / 2, z[:-1]
        else:
            rm, zm = rho[:, :-1], (z[:, :-1] + z[:, 1:]) / 2
        dm = np.hypot(rm - R0, zm - z0); cm = np.arctan2(zm - z0, rm - R0)
        g = gmat(cm)
        Wchi = V @ (g @ interp(aprof, dm) @ dag(g) - N) @ dag(V)
        unit = (-np.sin(cm) if mu == 0 else np.cos(cm)) / np.maximum(dm, 1e-12)
        Ws.append(Wchi * unit[..., None, None])
    U = [expi_herm(A.h * W)[0] for W in Ws]
    Om = V @ gmat(-chi_ext(rho, z)) @ dag(V)
    H = Om @ H
    U[0] = Om[:-1] @ U[0] @ dag(Om[1:]); U[1] = Om[:, :-1] @ U[1] @ dag(Om[:, 1:])
    mismatch = float(np.max(np.abs(H[A.bd] - I3)))
    H[A.bd] = I3
    Wr = herm_params(log_unitary(U[0]) / A.h); Wz = herm_params(log_unitary(U[1]) / A.h)
    v = A.pack(H, Wr, Wz, np.zeros(A.shapes['P']))
    return v, mismatch


def log_unitary(U):
    """Hermitian X with exp(i X) = U (principal branch, eigenphases in (-pi, pi])."""
    # U is normal; use Schur via eig of (U + U^+)/2 and (U - U^+)/2i jointly: U = V e^{i th} V^+
    Hm = (U + dag(U)) / 2; Am = (U - dag(U)) / 2j
    # diagonalise a generic combination to get a common eigenbasis
    mu, V = np.linalg.eigh(Hm + 0.6180339887 * Am)
    lam = np.einsum('...ji,...jk,...ki->...i', V.conj(), U, V)
    th = np.angle(lam)
    return (V * th[..., None, :]) @ dag(V)


def ball_start(A, R=4.0, nvec=(1 / np.sqrt(2), 1 / np.sqrt(2), 0.0)):
    """C-d / C-d5 (PREREG_B4 §4): no vortex.  H = 1 - f(r) m m^+ with r = sqrt(rho^2 + z^2), f = (1 - r^2/R^2)^2
    for r < R (0 outside), m = (1, 1, 0)/sqrt 2 (the main starts' orientation alpha = pi/4); W = 0, Wt_phi = 0.
    Under the ansatz (n = 0) it rotates as U(-omega t) H U^+; it has I > 0 because [m m^+, G] != 0."""
    m = np.array(nvec, complex)
    r = np.hypot(A.RHO, A.Z)
    f = np.where(r < R, (1 - (r / R) ** 2) ** 2, 0.0)
    H = I3 - f[..., None, None] * np.outer(m, m.conj())
    H[A.bd] = I3
    return A.pack(H, np.zeros(A.shapes['Wr']), np.zeros(A.shapes['Wz']), np.zeros(A.shapes['P']))


# ---------------- assembled Gauss-law matrix (fast inner solve) ----------------
def _ad_blocks(u):
    """R_pq = Re Tr(E_p u E_q u^+) for a stack of unitaries u (..., 3, 3) -> (..., 9, 9)."""
    M = np.einsum('...ab,qbc,...dc->...qad', u, EB, u.conj())        # u E_q u^+
    return np.real(np.einsum('pab,...qba->...pq', EB, M))


class Assembler:
    """Fixed sparsity pattern of the 9x9-block Gauss-law matrix on the (rho, z) lattice; fills data per call."""
    def __init__(self, A):
        self.A = A
        Nr, Nz = A.Nr, A.Nz
        idx = np.arange(Nr * Nz).reshape(Nr, Nz)
        pairs = [(idx.ravel(), idx.ravel())]                             # diagonal blocks
        for mu in (0, 1):
            ix, ip = A._sl(mu, idx)
            pairs.append((ix.ravel(), ip.ravel())); pairs.append((ip.ravel(), ix.ravel()))
        self.nblk = [len(p[0]) for p in pairs]
        bi = np.concatenate([p[0] for p in pairs]); bj = np.concatenate([p[1] for p in pairs])
        r = (9 * bi[:, None, None] + np.arange(9)[None, :, None] + 0 * np.arange(9)[None, None, :]).ravel()
        c = (9 * bj[:, None, None] + 0 * np.arange(9)[None, :, None] + np.arange(9)[None, None, :]).ravel()
        n = 9 * Nr * Nz
        coo = sp.coo_matrix((np.arange(len(r), dtype=float) + 1, (r, c)), shape=(n, n))
        csr = coo.tocsr(); csr.sum_duplicates()
        self.perm = csr.data.astype(np.int64) - 1          # position of each csr entry in the raw block order
        self.indices, self.indptr, self.n = csr.indices, csr.indptr, n

    def matrix(self, H, U, P, kind='K'):
        A = self.A
        wl, wm, ws = A._wts(kind)
        HH = H @ dag(H)
        Nsite = np.real(np.einsum('pab,qbc,...ca->...pq', EB, EB, HH))   # Re Tr(E_p E_q H H^+)
        D = ws[..., None, None] * Nsite
        if wm is not None:
            C = np.einsum('...ab,pbc->...pac', P, EB) - np.einsum('pab,...bc->...pac', EB, P)
            D = D + wm[..., None, None] * np.real(np.einsum('...pba,...qba->...pq', C.conj(), C))
        D = D.copy()
        offs = []
        for mu in (0, 1):
            w = wl[mu][..., None, None]
            dx, dp = A._sl(mu, D)
            dx += w * METRIC; dp += w * METRIC
            Rb = _ad_blocks(U[mu])                       # (x, x+mu) block is -w R, (x+mu, x) is -w R^T
            offs.append((-w * Rb).reshape(-1, 9, 9)); offs.append(np.swapaxes(-w * Rb, -1, -2).reshape(-1, 9, 9))
        raw = np.concatenate([D.reshape(-1, 9, 9)] + offs).ravel()
        return sp.csr_matrix((raw[self.perm], self.indices, self.indptr), shape=(self.n, self.n))

    def rhs(self, H, s, kind='K'):
        wl, wm, ws = self.A._wts(kind)
        HG = H @ self.A.G
        b = s * ws[..., None] * np.real(np.einsum('pab,...bc,...ac->...p', EB, HG, H.conj()))   # Re Tr(E_p H G H^+)
        c = s * s * np.sum(ws * np.sum(np.abs(HG) ** 2, axis=(-1, -2)))
        return b.ravel(), float(c)
