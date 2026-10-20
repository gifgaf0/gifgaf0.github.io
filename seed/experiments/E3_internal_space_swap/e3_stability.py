#!/usr/bin/env python3
"""
E3 part 5: second variation of the static Skyrme energy of the embedded B = 1 hedgehog
inside G2, in each block of g2 = su(2)_L (3) + su(2)_S (3) + (2,4) (8).

Fluctuation U = U0 exp(phi), phi(x) in g2.  With l_i = U0^T d_i U0 and D_i phi = d_i phi + [l_i, phi],
  L_i = l_i + D_i phi + (1/2)[D_i phi, phi] + O(phi^3).
Static energy (units F/e, x = eFr, normalisation N = 1/2 for Tr_7):
  E = int [ -(N/16) Tr(L_i L_i) - (N/32) sum_ij Tr([L_i, L_j]^2) ]
Second-order part Q[phi]:
  -(N/16) [Tr(D_i phi D_i phi) + Tr(l_i [D_i phi, phi])]
  -(N/32) sum_ij [Tr(G1 G1) + 2 Tr(G0 G2)],  G0 = [l_i,l_j],  G1 = [l_i, D_j phi] + [D_i phi, l_j],
   G2 = [D_i phi, D_j phi] + (1/2)([l_i, [D_j phi, phi]] + [[D_i phi, phi], l_j]).
The blocks are not coupled by the Hessian (they carry different SU(2)_short irreps: 1, 3, 4).
Checks: (a) Q agrees with a finite-difference second derivative of the full energy;
(b) the exact zero modes (translation, iso-rotation, G2 rotation) give Q = 0;
(c) Ritz analysis: phi = sum h_k(r) Y_lm(n) E_A (hat functions, Dirichlet at r = R, real spherical
harmonics l <= lmax), generalized eigenproblem H c = lambda S c with S the L^2 metric.
Stable means no negative eigenvalue.  Also: the (2,4) spectrum equals the SU(3) kaon-block
spectrum with doubled multiplicity (Schur on SU(2)_short).
Writes stability_results.json.
"""
import json
import sys
import time
import numpy as np
from scipy.linalg import eigh
import e3_inertia as inr

alg = np.load("g2_basis.npz")
basis, TL, TS, TG = alg["basis"], alg["TL"], alg["TS"], alg["TG"]
XL = -2 * TL
N = 0.5
SECTORS = {"long (3,1)": basis[0:3], "short (1,3)": basis[3:6], "(2,4)": basis[6:14],
           "kaon (su(3) part of (2,4))": None}
# kaon generators T4..T7 normalised in B
kaon = np.array([TG[k] for k in (3, 4, 5, 6)])
kaon = kaon / np.sqrt(-np.einsum('aij,aji->a', kaon, kaon))[:, None, None]
SECTORS["kaon (su(3) part of (2,4))"] = kaon


def comm(A, B):
    return A @ B - B @ A


def tr(A, B):
    return np.einsum('...ij,...ji->...', A, B)


def _trpair(X, Y):
    """Tr(X_p Y_q) for stacks X (g,P,d,d), Y (g,Q,d,d) -> (g,P,Q), via batched matmul"""
    g, P, d, _ = X.shape
    Q = Y.shape[1]
    return np.matmul(X.reshape(g, P, d * d), np.swapaxes(Y, -1, -2).reshape(g, Q, d * d).transpose(0, 2, 1))


def local_forms(x, n, E):
    """symmetric local bilinear form M[g, p, q] on v = (phi^A, d_1 phi^A, d_2 phi^A, d_3 phi^A)"""
    U, dU = inr.hedgehog_fields(XL, x, n)
    l = np.matmul(np.swapaxes(U, -1, -2)[:, None], dU)            # (g, 3, 7, 7)  l_i = U^T d_i U
    d = E.shape[0]
    P = 4 * d
    phi = np.zeros((P, 7, 7)); dphi = np.zeros((P, 3, 7, 7))
    for A in range(d):
        phi[A] = E[A]
        for i in range(3):
            dphi[(i + 1) * d + A, i] = E[A]
    ng = n.shape[0]
    # a_i(p) = d_i phi_p + [l_i, phi_p]          -> (g, 3, P, 7, 7)
    a = np.swapaxes(dphi, 0, 1)[None] + (np.matmul(l[:, :, None], phi[None, None]) - np.matmul(phi[None, None], l[:, :, None]))
    phiG = np.broadcast_to(phi[None], (ng, P, 7, 7))
    M = np.zeros((ng, P, P))
    # E2: Tr(a_i(p) a_i(q)) + (1/2)[Tr([l_i, a_i(p)] phi_q) + (p<->q)]
    for i in range(3):
        M += -(N / 16) * _trpair(a[:, i], a[:, i])
    la = sum(np.matmul(l[:, i][:, None], a[:, i]) - np.matmul(a[:, i], l[:, i][:, None]) for i in range(3))
    X = _trpair(la, phiG)
    M += -(N / 16) * 0.5 * (X + np.swapaxes(X, 1, 2))
    # E4
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            li, lj = l[:, i][:, None], l[:, j][:, None]
            ai, aj = a[:, i], a[:, j]
            g0 = (l[:, i] @ l[:, j] - l[:, j] @ l[:, i])[:, None]
            G1 = (li @ aj - aj @ li) + (ai @ lj - lj @ ai)
            T = _trpair(G1, G1)
            Ca = g0 @ ai - ai @ g0                       # [G0, a_i(p)]
            S1 = _trpair(Ca, aj)
            Y = g0 @ li - li @ g0                        # [G0, l_i]
            Z = lj @ g0 - g0 @ lj                        # [l_j, G0]
            YZa = (Y @ aj - aj @ Y) + (Z @ ai - ai @ Z)
            S2 = _trpair(YZa, phiG)
            twoG0G2 = (S1 + np.swapaxes(S1, 1, 2)) + 0.5 * (S2 + np.swapaxes(S2, 1, 2))
            M += -(N / 32) * (T + twoG0G2)
    return 0.5 * (M + np.swapaxes(M, 1, 2))


# ------------------------------------------------------------------ harmonic polynomials
def monomials(l):
    return [(a, b, l - a - b) for a in range(l + 1) for b in range(l + 1 - a)]


def harmonic_basis(lmax, n, w):
    """real orthonormal (on the sphere) harmonic polynomials P (deg l) evaluated at n, with gradients"""
    funcs = []
    for l in range(lmax + 1):
        mons = monomials(l)
        if l >= 2:
            lower = {m: k for k, m in enumerate(monomials(l - 2))}
            Lap = np.zeros((len(lower), len(mons)))
            for k, (a, b, c) in enumerate(mons):
                for (e, idx) in ((a, 0), (b, 1), (c, 2)):
                    if e >= 2:
                        m = [a, b, c]; m[idx] -= 2
                        Lap[lower[tuple(m)], k] += e * (e - 1)
            _, s, Vt = np.linalg.svd(Lap)
            null = Vt[np.sum(s > 1e-10):]
        else:
            null = np.eye(len(mons))
        vals = np.array([[np.prod(n ** np.array(m), axis=1) for m in mons]])[0].T     # (g, nmon)
        grads = np.zeros((n.shape[0], 3, len(mons)))
        for k, m in enumerate(mons):
            for i in range(3):
                if m[i] > 0:
                    mm = list(m); mm[i] -= 1
                    grads[:, i, k] = m[i] * np.prod(n ** np.array(mm), axis=1)
        Pv = vals @ null.T                          # (g, 2l+1)
        Pg = np.einsum('gik,mk->gim', grads, null)  # (g, 3, 2l+1)
        # orthonormalise on the sphere
        Gm = np.einsum('g,gm,gk->mk', w, Pv, Pv)
        Lc = np.linalg.cholesky(Gm)
        Tm = np.linalg.inv(Lc).T
        Pv, Pg = Pv @ Tm, np.einsum('gim,mk->gik', Pg, Tm)
        # gradient of P(x)/r^l on the unit sphere: dP - l P n
        Yg = Pg - l * Pv[:, None, :] * n[:, :, None]
        for k in range(Pv.shape[1]):
            funcs.append((l, Pv[:, k], Yg[:, :, k]))
    return funcs


def hats(R, nr, beta=3.0):
    """radial nodes (denser in the core) and hat functions h_k, k = 0..nr-1 (node nr at R excluded)"""
    s = np.linspace(0, 1, nr + 1)
    rn = R * np.sinh(beta * s) / np.sinh(beta)
    return rn


def ritz(sector, R=30.0, nr=40, lmax=3, nmu=14, nphi=28, nquad=4, nev=12):
    E = SECTORS[sector]
    d = E.shape[0]
    n, w = inr.angular_grid(nmu, nphi)
    Y = harmonic_basis(lmax, n, w)
    nY = len(Y)
    na = nY * d
    rn = hats(R, nr)
    K = nr                                   # hats at nodes 0..nr-1 (h vanishes at R)
    H = np.zeros((K * na, K * na))
    S = np.zeros((K * na, K * na))
    gq, gw = np.polynomial.legendre.leggauss(nquad)
    # angular blocks: v = h(r) * S0 + h'(r) * S1  on local index p = (slot, A)
    S0v = np.zeros((n.shape[0], na, 4 * d))
    S0g = np.zeros((n.shape[0], na, 4 * d))
    S1 = np.zeros((n.shape[0], na, 4 * d))
    for y, (l, Pv, Yg) in enumerate(Y):
        for A in range(d):
            c = y * d + A
            S0v[:, c, A] = Pv
            for i in range(3):
                S0g[:, c, (i + 1) * d + A] = Yg[:, i]          # times 1/r
                S1[:, c, (i + 1) * d + A] = n[:, i] * Pv
    for e in range(nr):
        r0, r1 = rn[e], rn[e + 1]
        for t, wt in zip(gq, gw):
            r = 0.5 * (r0 + r1) + 0.5 * (r1 - r0) * t
            wr = 0.5 * (r1 - r0) * wt * r**2
            M = local_forms(r, n, E)
            S0 = S0v + S0g / r
            MS0 = np.einsum('gij,gqj->giq', M, S0)
            MS1 = np.einsum('gij,gqj->giq', M, S1)
            wS0, wS1 = w[:, None, None] * S0, w[:, None, None] * S1
            A00 = np.tensordot(wS0, MS0, axes=([0, 2], [0, 1]))
            A01 = np.tensordot(wS0, MS1, axes=([0, 2], [0, 1]))
            A11 = np.tensordot(wS1, MS1, axes=([0, 2], [0, 1]))
            # hats on this element: left node e (value (r1-r)/(r1-r0)), right node e+1
            hl, hr = (r1 - r) / (r1 - r0), (r - r0) / (r1 - r0)
            dl, dr = -1 / (r1 - r0), 1 / (r1 - r0)
            loc = [(e, hl, dl), (e + 1, hr, dr)]
            for (k1, h1, d1) in loc:
                for (k2, h2, d2) in loc:
                    if k1 >= K or k2 >= K:
                        continue
                    blk = h1 * h2 * A00 + h1 * d2 * A01 + d1 * h2 * A01.T + d1 * d2 * A11
                    H[k1 * na:(k1 + 1) * na, k2 * na:(k2 + 1) * na] += wr * blk
                    S[k1 * na:(k1 + 1) * na, k2 * na:(k2 + 1) * na] += wr * h1 * h2 * np.eye(na)
    H = 0.5 * (H + H.T)
    ev = eigh(H, S, eigvals_only=True, subset_by_index=[0, nev - 1])
    return ev


def energy_full(phi_fun, eps, nr=40, nmu=10, nphi=20):
    """full static energy of U0 exp(eps phi) by 3D quadrature (for the finite-difference check)"""
    xs, wx = inr.radial_grid(nr)
    n, wa = inr.angular_grid(nmu, nphi)
    tot = 0.0
    for x, wr in zip(xs, wx):
        U, dU = inr.hedgehog_fields(XL, x, n)
        ph, dph = phi_fun(x, n)                  # (g,7,7), (g,3,7,7)
        # exp(eps phi) and its derivative (eigen formula, phi real antisymmetric)
        wv, V = np.linalg.eigh(1j * eps * ph)
        ev = -1j * wv
        Vi = np.conj(np.swapaxes(V, 1, 2))
        Ex = np.einsum('gij,gj,gjk->gik', V, np.exp(ev), Vi)
        mi, mj = ev[:, :, None], ev[:, None, :]
        dd = mi - mj
        small = np.abs(dd) < 1e-6
        fac = np.where(small, np.exp(mj) * (1 + dd / 2 + dd**2 / 6), (np.exp(mi) - np.exp(mj)) / np.where(small, 1, dd))
        dE = np.einsum('gab,gibc,gcd->giad', V, fac[:, None] * np.einsum('gab,gibc,gcd->giad', Vi, eps * dph, V), Vi)
        Uf = np.einsum('gij,gjk->gik', U, Ex)
        dUf = np.einsum('gikl,glm->gikm', dU, Ex) + np.einsum('gkl,gilm->gikm', U, dE)
        Uf, dUf = Uf.real, dUf.real
        L = np.einsum('gji,gkjl->gkil', Uf, dUf)
        e2 = -(N / 16) * sum(tr(L[:, i], L[:, i]) for i in range(3))
        e4 = 0
        for i in range(3):
            for j in range(3):
                if i != j:
                    c = comm(L[:, i], L[:, j])
                    e4 = e4 - (N / 32) * tr(c, c)
        tot += wr * x**2 * np.sum(wa * (e2 + e4))
    return tot


def Q_direct(phi_fun, E_unused=None, nr=40, nmu=10, nphi=20):
    """Q[phi] by quadrature of the local forms, for a phi given analytically"""
    xs, wx = inr.radial_grid(nr)
    n, wa = inr.angular_grid(nmu, nphi)
    full = basis                                   # use the full 14-dim basis as local internal basis
    tot = 0.0
    for x, wr in zip(xs, wx):
        M = local_forms(x, n, full)
        ph, dph = phi_fun(x, n)
        cA = -np.einsum('aij,gji->ga', full, ph)          # B-components
        cdA = -np.einsum('aij,gkji->gka', full, dph)
        v = np.concatenate([cA, cdA[:, 0], cdA[:, 1], cdA[:, 2]], 1)
        tot += wr * x**2 * np.sum(wa * np.einsum('gp,gpq,gq->g', v, M, v))
    return tot


if __name__ == "__main__":
    t0 = time.time()
    res = {}
    rng = np.random.default_rng(7)
    # (a) finite-difference check of the quadratic form with a random localized fluctuation in each block
    fd = {}
    for sec, (lo, hi) in {"long": (0, 3), "short": (3, 6), "(2,4)": (6, 14)}.items():
        coef = rng.normal(size=(hi - lo, 4))       # internal x (1, n_x, n_y, n_z) components
        Eb = basis[lo:hi]

        def phi_fun(x, n, coef=coef, Eb=Eb):
            g = np.exp(-x**2 / 2) * (1 + 0.3 * x)
            dg = np.exp(-x**2 / 2) * (0.3 - x * (1 + 0.3 * x))
            ang = coef[:, 0][None, :] + n @ coef[:, 1:].T                  # (g, A)
            ph = g * np.einsum('ga,aij->gij', ang, Eb)
            # d_i [g(r) (c0 + c.n)] = g' n_i (c0 + c.n) + g (c_i - n_i (c.n))/r
            cn = n @ coef[:, 1:].T
            dang = (dg * n[:, :, None] * ang[:, None, :] + g * (coef[:, 1:].T[None] - n[:, :, None] * cn[:, None, :]) / x)
            dph = np.einsum('gia,ajk->gijk', dang, Eb)
            return ph, dph
        E0 = energy_full(phi_fun, 0.0)
        fds = []
        for h in (4e-3, 2e-3):
            Ep, Em = energy_full(phi_fun, h), energy_full(phi_fun, -h)
            fds.append((Ep + Em - 2 * E0) / (2 * h**2))          # = Q + O(h^2)
        fd2 = (4 * fds[1] - fds[0]) / 3                          # Richardson: removes the h^2 term
        qd = Q_direct(phi_fun)
        fd[sec] = {"Q_formula": qd, "Q_fd_h=4e-3": fds[0], "Q_fd_h=2e-3": fds[1], "Q_fd_richardson": fd2,
                   "rel_diff_richardson": abs(qd - fd2) / abs(qd), "rel_diff_h=2e-3": abs(qd - fds[1]) / abs(qd)}
        print(f"(a) {sec:6s}: Q formula {qd:.8f}   FD h=4e-3 {fds[0]:.8f}, h=2e-3 {fds[1]:.8f}, Richardson {fd2:.8f}"
              f"   rel diff {abs(qd-fd2)/abs(qd):.1e}")
    res["finite_difference_check"] = fd
    # (b) exact zero modes
    zm = {}
    def rot_mode(T):
        def f(x, n):
            U, dU = inr.hedgehog_fields(XL, x, n)
            l = np.einsum('pji,pkjl->pkil', U, dU)
            R = np.einsum('gji,jk,gkl->gil', U, T, U)
            ph = R - T[None]
            dph = np.einsum('gij,gkjl->gkil', R, l) - np.einsum('gkij,gjl->gkil', l, R)
            return ph, dph
        return f
    for name, T in [("iso-rotation (long)", TL[2]), ("G2 rotation ((2,4) direction)", basis[9]),
                    ("SU(3) kaon rotation", TG[3])]:
        z = Q_direct(rot_mode(T), nr=48)
        zm[name] = z
        print(f"(b) zero mode {name:32s}: Q = {z:.2e}")
    # translation mode phi = l_3 : d_i l_3 = d_3 l_i + [l_i, l_3]  (zero curvature of U^-1 dU)
    def trans_mode(x, n):
        h = 1e-5
        U, dU = inr.hedgehog_fields(XL, x, n)
        l = np.einsum('pji,pkjl->pkil', U, dU)
        # d_3 l_i by central differences along z
        def lfield(shift):
            pts = x * n + shift * np.array([0, 0, 1.0])
            rr = np.linalg.norm(pts, axis=1)
            out = np.zeros((n.shape[0], 3, 7, 7))
            for k in range(n.shape[0]):
                Uk, dUk = inr.hedgehog_fields(XL, rr[k], (pts[k] / rr[k])[None])
                out[k] = np.einsum('ji,kjl->kil', Uk[0], dUk[0])
            return out
        d3l = (lfield(h) - lfield(-h)) / (2 * h)
        ph = l[:, 2]
        # zero curvature: d_i l_3 = d_3 l_i - [l_i, l_3]
        dph = d3l - (np.einsum('gkij,gjl->gkil', l, l[:, 2]) - np.einsum('gij,gkjl->gkil', l[:, 2], l))
        return ph, dph
    zt = Q_direct(trans_mode, nr=40, nmu=8, nphi=16)
    zm["translation (long)"] = zt
    print(f"(b) zero mode {'translation (long)':32s}: Q = {zt:.2e}")
    res["zero_modes_Q"] = zm
    print(f"   [{time.time()-t0:.0f}s]")
    sys.stdout.flush()
    # (c) Ritz spectra
    spec = {}
    settings = [dict(R=20.0, nr=30, lmax=3), dict(R=40.0, nr=40, lmax=3)]
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        settings = [dict(R=20.0, nr=16, lmax=2)]
    for sec in ["long (3,1)", "short (1,3)", "kaon (su(3) part of (2,4))", "(2,4)"]:
        spec[sec] = {}
        for st in settings:
            ev = ritz(sec, **st, nev=16 if sec == "(2,4)" else 12)
            key = f"R={st['R']:g},nr={st['nr']},lmax={st['lmax']}"
            spec[sec][key] = ev.tolist()
            print(f"(c) {sec:28s} {key}: lowest {np.round(ev[:10], 5)}   [{time.time()-t0:.0f}s]")
            sys.stdout.flush()
    res["ritz_lowest_eigenvalues"] = spec
    mins = {s_: min(min(v) for v in d_.values()) for s_, d_ in spec.items()}
    res["min_eigenvalue_per_block"] = mins
    # Schur: (2,4) spectrum = kaon spectrum with doubled multiplicity
    k = list(spec["(2,4)"].keys())[-1]
    e24 = np.array(spec["(2,4)"][k]); ek = np.array(spec["kaon (su(3) part of (2,4))"][k])
    res["schur_check_(2,4)_vs_kaon"] = dict(e24_first16=e24.tolist(), kaon_doubled_first16=np.repeat(ek, 2)[:16].tolist(),
                                           max_abs_diff=float(np.abs(e24[:12] - np.repeat(ek, 2)[:12]).max()))
    print("Schur check max |e(2,4) - e(kaon) doubled| (first 12):", res["schur_check_(2,4)_vs_kaon"]["max_abs_diff"])
    res["stable_no_negative_mode"] = bool(all(m > -1e-6 for m in mins.values()))
    print("no negative eigenvalue in any block:", res["stable_no_negative_mode"], mins)
    res["runtime_s"] = time.time() - t0
    with open("stability_results.json", "w") as fh:
        json.dump(res, fh, indent=1, default=float)
