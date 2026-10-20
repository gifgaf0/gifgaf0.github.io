"""
axial2d.py -- independent check of the Q = 1 and Q = 2 energies with an axially symmetric
reduction (a different code and discretisation from the 3D lattice of fs_lib.py).

Ansatz (exact for the A_{n,1} solitons, which are axially symmetric):
    phi(rho, theta, z) = R_3(n theta) psi(rho, z),  psi a unit vector on the half-plane,
so that d_theta phi = n R (e3 x psi).  Energy (Sutcliffe normalisation C0 = 1/(32 sqrt2 pi^2)):
    E = 2 pi C0 Int rho drho dz [ |psi_rho|^2 + |psi_z|^2 + n^2 |e3 x psi|^2 / rho^2
                                + |psi_rho x psi_z|^2
                                + n^2 ( |psi_rho x (e3 x psi)|^2 + |psi_z x (e3 x psi)|^2 ) / rho^2 ].
Discretisation on nodes rho_i = i h (i = 0..I), z_j = -Zm + j h (j = 0..J); psi = e3 on the axis
and on the outer boundary (rho = I h, |z| = Zm):
    sigma terms on links (weight rho at the link midpoint / node), the theta term at nodes,
    the (rho,z) Skyrme term as the 4-corner-pairing average on every plaquette (no checkerboard
    null modes), the mixed Skyrme terms on links averaged over the two link ends.
Minimisation: L-BFGS on an unconstrained 3-vector v, psi = v/|v|, exact gradient.
Usage: OMP_NUM_THREADS=1 python3 axial2d.py   (writes axial2d.json)
"""
import json
import os
import sys
import time
import numpy as np
from scipy.optimize import minimize

C0 = 1.0 / (32.0 * np.sqrt(2.0) * np.pi ** 2)
HERE = os.path.dirname(os.path.abspath(__file__))


def cross2(a, b):
    """|a x b|^2 and its gradients wrt a and b (last axis = vector)."""
    aa = (a * a).sum(-1); bb = (b * b).sum(-1); ab = (a * b).sum(-1)
    e = aa * bb - ab * ab
    ga = 2 * (bb[..., None] * a - ab[..., None] * b)
    gb = 2 * (aa[..., None] * b - ab[..., None] * a)
    return e, ga, gb


def Jmul(p):   # e3 x p
    return np.stack([-p[..., 1], p[..., 0], np.zeros_like(p[..., 0])], -1)


def JTmul(g):  # transpose of (e3 x .) applied to g
    return np.stack([g[..., 1], -g[..., 0], np.zeros_like(g[..., 0])], -1)


class Axial:
    def __init__(self, n, h, R, Zm):
        self.n = n; self.h = h
        self.I = int(round(R / h)); self.J = int(round(2 * Zm / h))
        self.rho = np.arange(self.I + 1) * h
        self.z = -Zm + np.arange(self.J + 1) * h

    def full(self, v):
        psi = np.zeros((self.I + 1, self.J + 1, 3)); psi[..., 2] = 1.0
        V = v.reshape(self.I - 1, self.J - 1, 3)
        nv = np.linalg.norm(V, axis=-1, keepdims=True)
        psi[1:-1, 1:-1] = V / nv
        return psi, V, nv

    def energy(self, psi, want_grad=True):
        n2 = self.n ** 2
        rho = self.rho
        g = np.zeros_like(psi)
        E = 0.0
        # (a) sigma, rho-links
        a = psi[1:] - psi[:-1]                         # (I, J+1, 3)
        wr = (rho[:-1] + 0.5 * self.h)[:, None]        # rho at link midpoint
        E += (wr * (a * a).sum(-1)).sum()
        g[1:] += 2 * wr[..., None] * a; g[:-1] -= 2 * wr[..., None] * a
        # (b) sigma, z-links
        b = psi[:, 1:] - psi[:, :-1]                   # (I+1, J, 3)
        wz = rho[:, None]
        E += (wz * (b * b).sum(-1)).sum()
        g[:, 1:] += 2 * wz[..., None] * b; g[:, :-1] -= 2 * wz[..., None] * b
        # (c) theta sigma term at interior nodes: n^2 h^2 |e3 x psi|^2 / rho
        wi = np.zeros_like(rho); wi[1:] = n2 * self.h ** 2 / rho[1:]
        E += (wi[:, None] * (psi[..., 0] ** 2 + psi[..., 1] ** 2)).sum()
        g[..., 0] += 2 * wi[:, None] * psi[..., 0]; g[..., 1] += 2 * wi[:, None] * psi[..., 1]
        # (d) (rho,z) Skyrme term, plaquettes: weight rho_c / (4 h^2)
        A = psi[1:, :-1] - psi[:-1, :-1]; Cc = psi[1:, 1:] - psi[:-1, 1:]     # rho-edges
        B = psi[:-1, 1:] - psi[:-1, :-1]; D = psi[1:, 1:] - psi[1:, :-1]      # z-edges
        wp = ((rho[:-1] + 0.5 * self.h) / (4 * self.h ** 2))[:, None, None]
        gA = np.zeros_like(A); gB = np.zeros_like(A); gC = np.zeros_like(A); gD = np.zeros_like(A)
        for (X, Y, gX, gY) in ((A, B, gA, gB), (A, D, gA, gD), (Cc, B, gC, gB), (Cc, D, gC, gD)):
            e, ga, gb = cross2(X, Y)
            E += (wp[..., 0] * e).sum()
            gX += wp * ga; gY += wp * gb
        g[1:, :-1] += gA; g[:-1, :-1] -= gA
        g[1:, 1:] += gC; g[:-1, 1:] -= gC
        g[:-1, 1:] += gB; g[:-1, :-1] -= gB
        g[1:, 1:] += gD; g[1:, :-1] -= gD
        # (e) mixed Skyrme terms: n^2 |d psi x (e3 x psi_k)|^2 / rho_k^2, averaged over link ends
        s = Jmul(psi)
        inv2 = np.zeros_like(rho); inv2[1:] = 1.0 / rho[1:] ** 2
        # rho-links: area rho_mid h^2, derivative a/h  ->  n^2 rho_mid * 0.5 * sum_k |a x s_k|^2 / rho_k^2
        for (sk, slk, ik) in ((s[:-1], np.s_[:-1], inv2[:-1]), (s[1:], np.s_[1:], inv2[1:])):
            w = (0.5 * n2 * wr[:, 0] * ik)[:, None]
            e, ga, gs = cross2(a, sk)
            E += (w * e).sum()
            ga = w[..., None] * ga; gs = w[..., None] * gs
            g[1:] += ga; g[:-1] -= ga
            g[slk] += JTmul(gs)
        # z-links: area rho_i h^2 -> n^2 rho_i * 0.5 * sum_k |b x s_k|^2 / rho_i^2
        wzl = (0.5 * n2 * rho * inv2)[:, None]
        for (sk, slk) in ((s[:, :-1], np.s_[:, :-1]), (s[:, 1:], np.s_[:, 1:])):
            e, gb_, gs = cross2(b, sk)
            E += (wzl * e).sum()
            gb_ = wzl[..., None] * gb_; gs = wzl[..., None] * gs
            g[:, 1:] += gb_; g[:, :-1] -= gb_
            g[slk] += JTmul(gs)
        return 2 * np.pi * C0 * E, 2 * np.pi * C0 * g

    def fun(self, v):
        psi, V, nv = self.full(v)
        E, g = self.energy(psi)
        gi = g[1:-1, 1:-1]
        P = psi[1:-1, 1:-1]
        gv = (gi - (gi * P).sum(-1, keepdims=True) * P) / nv
        return E, gv.ravel()

    def ansatz(self, Lf, prof='linear'):
        Rr, Zz = np.meshgrid(self.rho, self.z, indexing='ij')
        r = np.sqrt(Rr ** 2 + Zz ** 2)
        if prof == 'linear':
            f = np.where(r < Lf, np.pi * (Lf - r) / Lf, 0.0)
        else:
            f = np.pi * np.exp(-r ** 2 / Lf ** 2)
        sf = np.where(r > 1e-12, np.sin(f) / np.where(r > 1e-12, r, 1.0), np.pi / Lf)
        Z1 = Rr * sf
        Z0 = np.cos(f) + 1j * Zz * sf
        p = Z1 ** self.n; q = Z0
        pp = np.abs(p) ** 2; qq = np.abs(q) ** 2
        pq = p * np.conj(q)
        psi = np.stack([2 * pq.real, 2 * pq.imag, qq - pp], -1) / (pp + qq)[..., None]
        psi[0] = (0, 0, 1); psi[-1] = (0, 0, 1); psi[:, 0] = (0, 0, 1); psi[:, -1] = (0, 0, 1)
        return psi

    def relax(self, psi0, maxiter=20000, gtol=1e-9):
        v0 = psi0[1:-1, 1:-1].ravel().copy()
        res = minimize(self.fun, v0, jac=True, method='L-BFGS-B',
                       options=dict(maxiter=maxiter, maxfun=2 * maxiter, gtol=gtol, ftol=1e-15, maxcor=20))
        psi, _, _ = self.full(res.x)
        return psi, res


def interp(psi_c, mc, mf):
    """bilinear interpolation of a relaxed psi from model mc to model mf (same physical box)."""
    from scipy.interpolate import RegularGridInterpolator
    out = np.empty((mf.I + 1, mf.J + 1, 3))
    Rr, Zz = np.meshgrid(mf.rho, mf.z, indexing='ij')
    pts = np.stack([np.clip(Rr, 0, mc.rho[-1]), np.clip(Zz, mc.z[0], mc.z[-1])], -1)
    for c in range(3):
        out[..., c] = RegularGridInterpolator((mc.rho, mc.z), psi_c[..., c])(pts)
    out /= np.linalg.norm(out, axis=-1, keepdims=True)
    out[0] = (0, 0, 1); out[-1] = (0, 0, 1); out[:, 0] = (0, 0, 1); out[:, -1] = (0, 0, 1)
    return out


def main():
    out = dict(description='axially symmetric 2D reduction, A_{n,1}; energies in Sutcliffe normalisation')
    t0 = time.time()
    # 1. gradient check and ansatz energy vs the quadrature of check_ansatz_energy.py
    m = Axial(1, 0.1, 6.0, 6.0)
    rng = np.random.default_rng(7)
    psi = m.ansatz(4.0) + 0.05 * rng.normal(size=(m.I + 1, m.J + 1, 3))
    v = psi[1:-1, 1:-1].ravel()
    E, gv = m.fun(v)
    d = rng.normal(size=v.shape); eps = 1e-6
    fd = (m.fun(v + eps * d)[0] - m.fun(v - eps * d)[0]) / (2 * eps)
    out['grad_check_rel_err'] = abs(fd - gv @ d) / abs(fd)
    print(f"[axial] gradient check rel err {out['grad_check_rel_err']:.2e}")
    ans = []
    for h in (0.1, 0.05, 0.025):
        m = Axial(1, h, 4.5, 4.5)
        ans.append((h, m.energy(m.ansatz(4.0), False)[0]))
    out['ansatz_linear_Lf4'] = dict(lattice=ans, quadrature_3d_check=1.7368573257590636)
    print('[axial] A11 linear-ansatz energy (Lf=4):', ans, ' quadrature 1.736857')
    ans = []
    for h in (0.1, 0.05, 0.025):
        m = Axial(1, h, 7.5, 7.5)
        ans.append((h, m.energy(m.ansatz(2.0, 'gauss'), False)[0]))
    out['ansatz_gauss_w2'] = dict(lattice=ans, quadrature_3d_check=1.5225976006498694,
                                  richardson=(4 * ans[2][1] - ans[1][1]) / 3)
    print('[axial] A11 Gaussian-ansatz energy (w=2):', ans, ' Richardson', out['ansatz_gauss_w2']['richardson'], ' quadrature 1.522598')
    # 2. relaxed A_{n,1} in a cylinder rho <= R, |z| <= R (psi = e3 on its surface)
    #    resolution sequence h = 0.2, 0.1, 0.05 at R = 7.5; box sequence R = 7.5 ... 25 at h = 0.2, 0.1
    res = {}

    def run(n, R, h, init):
        m = Axial(n, h, R, R)
        psi0 = m.ansatz(7.5) if init is None else interp(init[0], init[1], m)
        tt = time.time()
        psi, r = m.relax(psi0)
        key = f'n{n}_R{R}_h{h}'
        res[key] = dict(n=n, R=R, h=h, E=float(r.fun), iters=int(r.nit), success=bool(r.success), msg=str(r.message),
                        gmax=float(np.abs(r.jac).max()), wall_s=time.time() - tt)
        print(f'[axial] n={n} R={R} h={h}: E = {r.fun:.6f}  ({r.nit} it, {r.message})  t={time.time()-t0:.0f}s', flush=True)
        json.dump(dict(out, relaxed=res), open(os.path.join(HERE, 'axial2d.json'), 'w'), indent=1)
        return psi, m

    for n in (1, 2):
        s02 = run(n, 7.5, 0.2, None)
        s01 = run(n, 7.5, 0.1, s02)
        run(n, 7.5, 0.05, s01)
        for R in (12.0, 18.0, 25.0):
            a = run(n, R, 0.2, s02)
            run(n, R, 0.1, a)
    out['relaxed'] = res
    ext = {}
    for n in (1, 2):
        Ea, Eb, Ec = (res[f'n{n}_R7.5_h{h}']['E'] for h in (0.2, 0.1, 0.05))
        Ecyl = (4 * Ec - Eb) / 3                       # second-order Richardson (0.1, 0.05)
        Ecyl3 = Ec + (Ec - Eb) * (Ec - Eb) / ((Eb - Ea) - (Ec - Eb))   # Aitken (order-free)
        box01 = {R: res[f'n{n}_R{R}_h0.1']['E'] for R in (7.5, 12.0, 18.0, 25.0)}
        dbox = box01[25.0] - box01[7.5]
        ext[f'n{n}'] = dict(E_R7p5_continuum_h2=Ecyl, E_R7p5_continuum_aitken=Ecyl3,
                            order_ratio=(Ea - Eb) / (Eb - Ec), E_h0p1_by_R=box01, box_shift_7p5_to_25=dbox,
                            E_infinite_volume_continuum_est=Ecyl + dbox)
    out['extrapolated'] = ext
    print('[axial] extrapolated:', json.dumps(ext, indent=1))
    json.dump(out, open(os.path.join(HERE, 'axial2d.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
