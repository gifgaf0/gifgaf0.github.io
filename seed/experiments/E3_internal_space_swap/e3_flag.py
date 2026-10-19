#!/usr/bin/env python3
"""
E3 part 6: the flag manifold F2 = SU(3)/T^2.

(a) Moment map: sample U (Haar, fixed seed), project diag(U diag(a) U^+) to the plane
    sum = const; compare the sample hull with the hexagon of the 6 permutations of a
    (Schur-Horn); degenerate a -> triangle (CP^2).
(b) pi_2(F2) = Z^2: maps S^2 -> F2 from holomorphic data (p(z), r(z)) with p.r = 0:
    L1 = [p], L3 = [conj r], L2 = (L1 + L3)^perp.  Charges Q_k = (1/2 pi) int F_k of the three
    tautological line bundles (pull-backs of the Fubini-Study form of the k-th line), computed
    (i) as a continuum integral of (1/2 pi i) Tr(P_k [d_theta P_k, d_phi P_k]) with Gauss
    quadrature and (ii) as an exact lattice sum of Berry phases of triangles.  Expected
    Q1 = deg p, Q3 = -deg r, Q1 + Q2 + Q3 = 0; non-holomorphic deformations W(n) in U(3)
    leave them unchanged.
(c) pi_3(F2) = Z: Hopf-type charge of explicit configurations via the SU(3) lift.  The
    lift's winding B = -(1/24 pi^2) int eps_ijk Tr(w_i w_j w_k), w = g^-1 dg (sign: hedgehog = +1),
    and the same number from the projector fields alone (Amari-Sawado 1805.10008 eq. 13 form):
    B = -(1/24 pi^2) int [ 3 sum_k A_k . B_k + eps_ijk Tr(theta_i theta_j theta_k) ],
    with B_k = curl A_k the curvature of line k and A_k obtained from B_k in Coulomb gauge (FFT).
Writes flag_results.json and fig_moment_map.png.
"""
import json
import sys
import time
import numpy as np
from scipy.spatial import ConvexHull
from scipy.linalg import expm

t0 = time.time()
res = {}
rng = np.random.default_rng(20261019)

# ============================================================ (a) moment map
u_ax = np.array([1, -1, 0]) / np.sqrt(2)
w_ax = np.array([1, 1, -2]) / np.sqrt(6)


def haar(nsamp, rng):
    Z = (rng.normal(size=(nsamp, 3, 3)) + 1j * rng.normal(size=(nsamp, 3, 3))) / np.sqrt(2)
    Q, R = np.linalg.qr(Z)
    d = np.diagonal(R, axis1=1, axis2=2)
    return Q * (d / np.abs(d))[:, None, :]


def project(a, U):
    B = np.abs(U) ** 2                       # unistochastic matrix
    d = B @ a
    return np.stack([d @ u_ax, d @ w_ax], 1)


def polygon(a):
    import itertools
    verts = np.array(sorted({tuple(np.round(np.array(p), 12)) for p in itertools.permutations(a)}))
    pts = np.stack([verts @ u_ax, verts @ w_ax], 1)
    h = ConvexHull(pts)
    return pts[h.vertices]


def poly_geometry(P):
    n = len(P)
    sides = [np.linalg.norm(P[(i + 1) % n] - P[i]) for i in range(n)]
    angs = []
    for i in range(n):
        v1, v2 = P[i - 1] - P[i], P[(i + 1) % n] - P[i]
        angs.append(np.degrees(np.arccos(v1 @ v2 / np.linalg.norm(v1) / np.linalg.norm(v2))))
    return sides, angs


def inside(P, x, tol=1e-12):
    h = ConvexHull(P)
    return np.all(x @ h.equations[:, :2].T + h.equations[:, 2] <= tol, axis=1)


def hausdorff_hull(P, Q):
    # max over polygon P's vertices of distance to hull Q (Q inside P): equals the Hausdorff distance
    hq = ConvexHull(Q)
    def dist_to_poly(x):
        best = np.inf
        V = Q[hq.vertices]
        for i in range(len(V)):
            a_, b_ = V[i], V[(i + 1) % len(V)]
            t = np.clip((x - a_) @ (b_ - a_) / ((b_ - a_) @ (b_ - a_)), 0, 1)
            best = min(best, np.linalg.norm(a_ + t * (b_ - a_) - x))
        return best
    return max(dist_to_poly(x) for x in P)


mm = {}
for label, a in [("generic a=(1, 0.3, -1.3)", np.array([1.0, 0.3, -1.3])),
                 ("degenerate a=(1, 1, -2)", np.array([1.0, 1.0, -2.0]))]:
    P = polygon(a)
    sides, angs = poly_geometry(P)
    entry = dict(n_vertices=len(P), sides=sides, interior_angles_deg=angs, convergence=[])
    allpts = []
    for nsamp in (10**3, 10**4, 10**5, 10**6):
        U = haar(nsamp, rng)
        X = project(a, U)
        allpts.append(X)
        hull = ConvexHull(X)
        entry["convergence"].append(dict(N=nsamp, all_inside=bool(inside(P, X).all()),
                                         hull_area_over_polygon_area=hull.volume / ConvexHull(P).volume,
                                         hausdorff=hausdorff_hull(P, X[hull.vertices])))
    entry["samples_for_figure"] = allpts[1][:6000].tolist()
    entry["polygon"] = P.tolist()
    mm[label] = entry
    print(f"(a) {label}: {len(P)} vertices, angles {np.round(angs, 6)}, sides {np.round(sides, 6)}")
    for c in entry["convergence"]:
        print(f"      N={c['N']:>8}: inside {c['all_inside']}, hull/polygon area {c['hull_area_over_polygon_area']:.6f}, "
              f"Hausdorff {c['hausdorff']:.2e}")
# a check of the side-length pattern: hexagon sides alternate |a1-a2|*sqrt2/... (two values for generic a)
res["moment_map"] = {k: {kk: vv for kk, vv in v.items() if kk != "samples_for_figure"} for k, v in mm.items()}

# figure
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.5))
    for ax, (label, e) in zip(axs, mm.items()):
        S = np.array(e["samples_for_figure"])
        P = np.array(e["polygon"])
        ax.scatter(S[:, 0], S[:, 1], s=1, color="#4C72B0", alpha=0.35, lw=0, label="diag(U a U$^\\dagger$), 6000 Haar samples")
        Pc = np.vstack([P, P[:1]])
        ax.plot(Pc[:, 0], Pc[:, 1], color="#C44E52", lw=1.4, label="hull of permutations of a")
        ax.set_aspect("equal"); ax.set_title(label, fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
    axs[0].legend(fontsize=7, loc="lower left", frameon=False)
    fig.suptitle("Moment map of SU(3) orbits: hexagon (flag manifold) and triangle (CP$^2$)", fontsize=10)
    fig.tight_layout()
    fig.savefig("fig_moment_map.png", dpi=110)
    plt.close(fig)
except Exception as ex:
    print("figure failed:", ex)

# ============================================================ (b) pi_2 charges
def frame_from(p_fun, r_fun, W=None):
    """returns function (theta, phi) -> (u1, u2, u3) orthonormal, from holomorphic p, r with p.r = 0"""
    def f(theta, phi):
        z = np.tan(theta / 2) * np.exp(1j * phi)
        p = p_fun(z); r = r_fun(z)
        u1 = p / np.linalg.norm(p, axis=-1, keepdims=True)
        u3 = np.conj(r) / np.linalg.norm(r, axis=-1, keepdims=True)
        u2 = np.conj(np.cross(u3, u1))
        U = np.stack([u1, u2, u3], -1)                     # columns
        if W is not None:
            nvec = np.stack([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)], -1)
            U = np.einsum('...ij,...jk->...ik', W(nvec), U)
        return U
    return f


def charges_continuum(frame, nth=64, nph=128, h=1e-6):
    mu, wmu = np.polynomial.legendre.leggauss(nth)
    th = np.arccos(-mu)                                   # theta increasing
    wth = wmu / np.sin(th)                                # d theta = d mu / sin theta
    ph = 2 * np.pi * np.arange(nph) / nph
    TH, PH = np.meshgrid(th, ph, indexing='ij')
    def proj(T, Pp):
        U = frame(T, Pp)
        return np.einsum('...ik,...jk->...kij', U, np.conj(U))   # P_k = u_k u_k^+  (shape ..., k, i, j)
    P0 = proj(TH, PH)
    dPt = (proj(TH + h, PH) - proj(TH - h, PH)) / (2 * h)
    dPp = (proj(TH, PH + h) - proj(TH, PH - h)) / (2 * h)
    dens = np.einsum('...kij,...kjl,...kli->...k', P0, dPt, dPp) - np.einsum('...kij,...kjl,...kli->...k', P0, dPp, dPt)
    dens = dens / (2j * np.pi)
    Q = np.einsum('a,abk->k', wth, dens) * (2 * np.pi / nph)
    return Q.real, np.abs(Q.imag).max()


def charges_lattice(frame, nth=200, nph=400):
    th = np.linspace(0, np.pi, nth + 1)
    th[0], th[-1] = 1e-9, np.pi - 1e-9
    ph = 2 * np.pi * np.arange(nph + 1) / nph
    TH, PH = np.meshgrid(th, ph, indexing='ij')
    U = frame(TH, PH)                                     # (nth+1, nph+1, 3, 3)
    Q = np.zeros(3)
    for k in range(3):
        u = U[..., :, k]
        ip = lambda a_, b_: np.sum(np.conj(a_) * b_, -1)
        a_, b_, c_, d_ = u[:-1, :-1], u[1:, :-1], u[1:, 1:], u[:-1, 1:]
        t1 = np.angle(ip(a_, b_) * ip(b_, c_) * ip(c_, a_))
        t2 = np.angle(ip(a_, c_) * ip(c_, d_) * ip(d_, a_))
        Q[k] = (t1.sum() + t2.sum()) / (2 * np.pi)     # orientation chosen to match the continuum sign convention
    return Q


sq2 = np.sqrt(2)
one = lambda z: np.ones_like(z)
zero = lambda z: np.zeros_like(z)
vec = lambda *c: (lambda z: np.stack([ci(z) for ci in c], -1))
cases = {
    "A: p=(1,z,0), r=p x (0,0,1)": (vec(one, lambda z: z, zero), vec(lambda z: z, lambda z: -one(z), zero), (1, 0, -1)),
    "B: p=(0,0,1), r=p x (1,z,0)": (vec(zero, zero, one), vec(lambda z: -z, one, zero), (0, 1, -1)),
    "C: p=(1,z,0), r=p x (0,1,z)": (vec(one, lambda z: z, zero), vec(lambda z: z**2, lambda z: -z, one), (1, 1, -2)),
    "D: p=(1,z,z^2), r=p x (0,1,z)": (vec(one, lambda z: z, lambda z: z**2), vec(zero, lambda z: -z, one), (2, -1, -1)),
    "E: Veronese Frenet frame": (vec(one, lambda z: sq2 * z, lambda z: z**2), vec(lambda z: sq2 * z**2, lambda z: -2 * z, lambda z: sq2 * one(z)), (2, 0, -2)),
    "F: p=(1,z,z^3), r=p x (0,0,1)": (vec(one, lambda z: z, lambda z: z**3), vec(lambda z: z, lambda z: -one(z), zero), (3, -2, -1)),
    "G: p=(1,conj z,0) (anti-holomorphic)": (vec(one, lambda z: np.conj(z), zero), vec(lambda z: np.conj(z), lambda z: -one(z), zero), (-1, 0, 1)),
}
Hs = rng.normal(size=(3, 3, 3)) + 1j * rng.normal(size=(3, 3, 3))
Hs = 0.5 * (Hs + np.conj(np.swapaxes(Hs, 1, 2)))
def Wdef(nvec):
    H = 1.3 * np.einsum('...i,ijk->...jk', nvec, Hs) + 0.4 * (nvec[..., :1, None] * nvec[..., 1:2, None]) * Hs[2]
    w_, V = np.linalg.eigh(H)
    return np.einsum('...ij,...j,...kj->...ik', V, np.exp(1j * w_), np.conj(V))
for key in ["D: p=(1,z,z^2), r=p x (0,1,z)", "F: p=(1,z,z^3), r=p x (0,0,1)"]:
    p_, r_, ex = cases[key]
    cases[key.split(":")[0] + "': same, deformed by a non-holomorphic W(n) in U(3)"] = (p_, r_, ex, Wdef)

pi2 = {}
for key, val in cases.items():
    p_, r_, ex = val[:3]
    W = val[3] if len(val) > 3 else None
    fr = frame_from(p_, r_, W)
    # orthonormality check
    Ut = fr(np.array([0.3, 1.7, 2.9]), np.array([0.1, 2.0, 4.0]))
    orth = np.abs(np.einsum('...ji,...jk->...ik', np.conj(Ut), Ut) - np.eye(3)).max()
    Qc, imag = charges_continuum(fr)
    Qc2, _ = charges_continuum(fr, nth=96, nph=192)
    Ql = charges_lattice(fr)
    ok = np.allclose(Qc2, ex, atol=1e-6) and np.allclose(Ql, ex, atol=1e-9)
    pi2[key] = dict(expected=list(ex), continuum_64x128=Qc.tolist(), continuum_96x192=Qc2.tolist(),
                    lattice_200x400=Ql.tolist(), max_dev_from_integer=float(np.abs(Qc2 - np.round(Qc2)).max()),
                    sum_Q=float(Qc2.sum()), orthonormality_err=float(orth), pass_=bool(ok))
    print(f"(b) {key:58s} Q = {np.round(Qc2, 9)}  lattice {np.round(Ql, 9)}  expected {ex}  {'PASS' if ok else 'FAIL'}")
res["pi2_charges"] = pi2
gens = np.array([pi2["A: p=(1,z,0), r=p x (0,0,1)"]["expected"][:2], pi2["B: p=(0,0,1), r=p x (1,z,0)"]["expected"][:2]])
res["pi2_A_B_generate_Z2"] = bool(abs(round(np.linalg.det(gens))) == 1)
print(f"   (Q1,Q2) of A and B: det = {np.linalg.det(gens):.0f} -> they generate Z^2")
sys.stdout.flush()

# ============================================================ (c) pi_3: Hopf-type charge via the SU(3) lift
R0 = 1.0


def step(t):
    """C-infinity step: 1 for t<=0, 0 for t>=1, all derivatives vanish at both ends"""
    t = np.clip(t, 0, 1)
    with np.errstate(divide='ignore', over='ignore', invalid='ignore'):
        a_ = np.where(t < 1, np.exp(-1 / np.maximum(1 - t, 1e-300)), 0.0)
        b_ = np.where(t > 0, np.exp(-1 / np.maximum(t, 1e-300)), 0.0)
    return a_ / (a_ + b_)


sig = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]])
X_up = np.zeros((3, 3, 3), complex); X_up[:, :2, :2] = 1j * sig          # SU(2) in the upper-left block
X_dn = np.zeros((3, 3, 3), complex); X_dn[:, 1:, 1:] = 1j * sig          # SU(2) in the lower-right block
L_so3 = np.zeros((3, 3, 3))
for a_, (i, j) in enumerate([(1, 2), (2, 0), (0, 1)]):
    L_so3[a_, i, j], L_so3[a_, j, i] = 1, -1    # (L_a)_ij = +eps_aij: exp(-f n.L) <-> SU(2) exp(f n.(i sigma)/2), so B = +4
Hm = rng.normal(size=(4, 3, 3)) + 1j * rng.normal(size=(4, 3, 3))
Hm = 0.5 * (Hm + np.conj(np.swapaxes(Hm, 1, 2)))
Hm -= np.trace(Hm, axis1=1, axis2=2)[:, None, None] * np.eye(3) / 3
alph = rng.normal(size=(2, 4))


def expm_herm(H):
    w_, V = np.linalg.eigh(H)
    return np.einsum('...ij,...j,...kj->...ik', V, np.exp(1j * w_), np.conj(V))


def hedgehog(xyz, X, f0=np.pi):
    r = np.linalg.norm(xyz, axis=-1)
    n = xyz / np.maximum(r, 1e-300)[..., None]
    f = f0 * step(r / R0)
    K = np.einsum('...a,aij->...ij', n, X)              # anti-Hermitian
    return expm_herm(-1j * f[..., None, None] * K)


def lift(name, xyz):
    r = np.linalg.norm(xyz, axis=-1)
    if name == "C1 hedgehog in SU(2)_upper":
        return hedgehog(xyz, X_up)
    if name == "C2 W(x) . hedgehog . T(x) (non-embedded, T diagonal)":
        n = xyz / np.maximum(r, 1e-300)[..., None]
        up = 1 - step(r / (0.6 * R0))                    # flat zero at r = 0 so the n-dependence is smooth
        k = 1.5 * up * step(r / (1.2 * R0))
        H = np.einsum('...a,aij->...ij', np.concatenate([np.ones(r.shape + (1,)), n], -1), Hm)
        W = expm_herm(k[..., None, None] * H)
        al = np.einsum('...a,ba->...b', np.concatenate([np.ones(r.shape + (1,)), n], -1), alph) * (up * step(r / R0))[..., None]
        T = np.zeros(r.shape + (3, 3), complex)
        T[..., 0, 0], T[..., 1, 1], T[..., 2, 2] = np.exp(1j * al[..., 0]), np.exp(1j * al[..., 1]), np.exp(-1j * (al[..., 0] + al[..., 1]))
        return W @ hedgehog(xyz, X_up) @ T
    if name == "C3 hedgehog_upper . hedgehog_lower (degree 2)":
        return hedgehog(xyz, X_up) @ hedgehog(0.8 * xyz + np.array([0.05, -0.03, 0.02]), X_dn)
    if name == "C4 SO(3) hedgehog, f(0) = 2 pi (real lines)":
        return _so3(xyz)
    if name == "C5 inverse hedgehog (degree -1)":
        return np.conj(np.swapaxes(hedgehog(xyz, X_up), -1, -2))
    raise KeyError(name)


def _so3(xyz):
    r = np.linalg.norm(xyz, axis=-1)
    n = xyz / np.maximum(r, 1e-300)[..., None]
    f = 2 * np.pi * step(r / R0)
    K = np.einsum('...a,aij->...ij', n, L_so3)          # real antisymmetric, K^3 = -K
    K2 = K @ K
    s, c = np.sin(f)[..., None, None], np.cos(f)[..., None, None]
    return (np.eye(3) + s * K + (1 - c) * K2).astype(complex)


EXPECTED = {"C1 hedgehog in SU(2)_upper": 1, "C2 W(x) . hedgehog . T(x) (non-embedded, T diagonal)": 1,
            "C3 hedgehog_upper . hedgehog_lower (degree 2)": 2, "C4 SO(3) hedgehog, f(0) = 2 pi (real lines)": 4,
            "C5 inverse hedgehog (degree -1)": -1}


def derivs(fun, xyz, h=1e-5):
    out = []
    for i in range(3):
        e = np.zeros(3); e[i] = h
        out.append((fun(xyz + e) - fun(xyz - e)) / (2 * h))
    return np.stack(out, 1)                              # (points, direction, ...)


EPS = np.zeros((3, 3, 3))
for (a_, b_, c_) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
    EPS[a_, b_, c_] = 1; EPS[b_, a_, c_] = -1


def lift_degree(name, nr=96, nmu=32, nph=64):
    """B = -(1/24 pi^2) int eps_ijk Tr(w_i w_j w_k), spherical quadrature on r < 1.25 R0 (g = const beyond)"""
    rr, wr = np.polynomial.legendre.leggauss(nr)
    Rmax = 1.25 * R0
    rr = 0.5 * Rmax * (rr + 1); wr = 0.5 * Rmax * wr
    mu, wmu = np.polynomial.legendre.leggauss(nmu)
    ph = 2 * np.pi * np.arange(nph) / nph
    tot = 0.0
    for r, w in zip(rr, wr):
        MU, PH = np.meshgrid(mu, ph, indexing='ij')
        st = np.sqrt(1 - MU**2)
        xyz = r * np.stack([st * np.cos(PH), st * np.sin(PH), MU], -1).reshape(-1, 3)
        wa = (wmu[:, None] * np.full(nph, 2 * np.pi / nph)).ravel()
        g = lift(name, xyz)
        dg = derivs(lambda y: lift(name, y), xyz)
        wv = np.einsum('pji,pkjl->pkil', np.conj(g), dg)        # w_i = g^+ d_i g
        dens = np.einsum('ijk,pimn,pjno,pkom->p', EPS, wv, wv, wv)
        tot += w * r**2 * np.sum(wa * dens)
    return float(np.real(-tot / (24 * np.pi**2)))


def f2_intrinsic(name, Ngrid=64, L=3.0 * R0, chunk=40000):
    """charge from the projector fields P_k = g e_k e_k^+ g^+ alone; A_k from B_k by FFT (Coulomb gauge)"""
    xs = (np.arange(Ngrid) - Ngrid / 2) * (L / Ngrid)
    dx = L / Ngrid
    Xg = np.stack(np.meshgrid(xs, xs, xs, indexing='ij'), -1).reshape(-1, 3)
    Bk = np.zeros((Xg.shape[0], 3, 3))                  # (point, line k, component)
    gam = np.zeros(Xg.shape[0])
    proj = lambda y: (lambda g: np.einsum('pik,pjk->pkij', g, np.conj(g)))(lift(name, y))
    rr = np.linalg.norm(Xg, axis=1)
    act = np.where(rr < 1.3 * R0)[0]                    # outside, P_k = const: B_k = 0, Gamma = 0
    for s0 in range(0, act.size, chunk):
        idx = act[s0:s0 + chunk]
        y = Xg[idx]
        P = proj(y)
        dP = derivs(proj, y)                             # (p, i, k, a, b)
        # curvature of line k:  F_ij = -i Tr(P [d_i P, d_j P]);  B_m = (1/2) eps_mij F_ij
        PdP = np.einsum('pkab,pikbc->pikac', P, dP)
        F = -1j * (np.einsum('pikab,pjkba->pkij', PdP, dP) - np.einsum('pjkab,pikba->pkij', PdP, dP))
        Bk[idx] = 0.5 * np.einsum('mij,pkij->pkm', EPS, F).real
        # eps_ijk Tr(theta_i theta_j theta_k) = sum over ordered triples (a,b,c) distinct of
        # eps_ijk Tr(P_a d_i P_b P_b d_j P_c P_c d_k P_a)
        g_ = 0.0
        for (a_, b_, c_) in [(0, 1, 2), (1, 2, 0), (2, 0, 1), (0, 2, 1), (2, 1, 0), (1, 0, 2)]:
            Ma = np.einsum('pxy,piyz,pzw->pixw', P[:, a_], dP[:, :, b_], P[:, b_])
            Mb = np.einsum('pxy,piyz,pzw->pixw', P[:, b_], dP[:, :, c_], P[:, c_])
            Mc = np.einsum('pxy,piyz,pzw->pixw', P[:, c_], dP[:, :, a_], P[:, a_])
            g_ = g_ + np.einsum('ijk,pixy,pjyz,pkzx->p', EPS, Ma, Mb, Mc)
        # Tr(theta^3) = sum over the 6 ordered triples (a,b,c) of distinct lines of theta_ab theta_bc theta_ca,
        # and P_a dP_b P_b = u_a theta_ab u_b^+, so each term is a trace of projector products (gauge invariant)
        gam[idx] = np.real(g_)
    # Coulomb gauge: A_hat = i k x B_hat / k^2
    kv = 2 * np.pi * np.fft.fftfreq(Ngrid, d=dx)
    KX, KY, KZ = np.meshgrid(kv, kv, kv, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K2[0, 0, 0] = 1.0
    cs = []
    divmax = 0.0
    for k in range(3):
        Bf = [np.fft.fftn(Bk[:, k, m].reshape(Ngrid, Ngrid, Ngrid)) for m in range(3)]
        divmax = max(divmax, float(np.abs(np.fft.ifftn(1j * (KX * Bf[0] + KY * Bf[1] + KZ * Bf[2]))).max()))
        Af = [1j * (KY * Bf[2] - KZ * Bf[1]) / K2, 1j * (KZ * Bf[0] - KX * Bf[2]) / K2, 1j * (KX * Bf[1] - KY * Bf[0]) / K2]
        for m in range(3):
            Af[m][0, 0, 0] = 0.0
        A = [np.real(np.fft.ifftn(a)) for a in Af]
        cs.append(float(sum(np.sum(A[m].ravel() * Bk[:, k, m]) for m in range(3)) * dx**3))
    G = float(np.sum(gam) * dx**3)
    flux = [float(np.abs(Bk[:, k, :].sum(0)).max() * dx**3) for k in range(3)]
    Bval = -(3 * sum(cs) + G) / (24 * np.pi**2)
    return dict(CS_k=cs, Gamma_term=G, B=Bval, max_divB=divmax, net_flux=flux)


def curvature_check(name, npts=20):
    """B_k from the projector formula vs curl of A_k = -i u_k^+ grad u_k of the lift, at random points"""
    y = rng.uniform(-0.8, 0.8, size=(npts, 3)) * R0
    proj = lambda z: (lambda g: np.einsum('pik,pjk->pkij', g, np.conj(g)))(lift(name, z))
    P = proj(y); dP = derivs(proj, y)
    PdP = np.einsum('pkab,pikbc->pikac', P, dP)
    F = -1j * (np.einsum('pikab,pjkba->pkij', PdP, dP) - np.einsum('pjkab,pikba->pkij', PdP, dP))
    Bp = 0.5 * np.einsum('mij,pkij->pkm', EPS, F).real
    def Afield(z):
        g = lift(name, z); dg = derivs(lambda q: lift(name, q), z)
        return np.real(-1j * np.einsum('pak,piak->pki', np.conj(g), dg))      # (p, k, i)
    h = 1e-4
    dA = []
    for j in range(3):
        e = np.zeros(3); e[j] = h
        dA.append((Afield(y + e) - Afield(y - e)) / (2 * h))
    dA = np.stack(dA, -1)                                                      # (p, k, i, j) = d_j A_i
    curl = np.einsum('mji,pkij->pkm', EPS, dA)
    return float(np.abs(curl - Bp).max()), float(np.abs(Bp).max())


if __name__ == "__main__":
    for name in ("C1 hedgehog in SU(2)_upper", "C2 W(x) . hedgehog . T(x) (non-embedded, T diagonal)"):
        err, scale = curvature_check(name)
        print(f"(c) curvature formula vs curl of lift connection, {name[:2]}: max |diff| {err:.1e} (scale {scale:.2f})")
        res.setdefault("curvature_formula_check", {})[name] = dict(max_abs_diff=err, scale=scale)
    pi3 = {}
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    for name, ex in EXPECTED.items():
        Bl = lift_degree(name)
        entry = dict(expected=ex, lift_degree=Bl)
        print(f"(c) {name:55s} lift degree {Bl:.8f} (expected {ex})   [{time.time()-t0:.0f}s]")
        sys.stdout.flush()
        for Ng in ((48,) if quick else (64, 96, 128)):
            fi = f2_intrinsic(name, Ngrid=Ng)
            entry[f"F2_intrinsic_N{Ng}"] = fi
            print(f"      from projectors only, N={Ng}: B = {fi['B']:.6f}  (CS terms {np.round(fi['CS_k'], 5)}, "
                  f"Gamma {fi['Gamma_term']:.5f}, max|div B| {fi['max_divB']:.1e})   [{time.time()-t0:.0f}s]")
            sys.stdout.flush()
        pi3[name] = entry
    res["pi3"] = pi3
    res["runtime_s"] = time.time() - t0
    with open("flag_results.json", "w") as fh:
        json.dump(res, fh, indent=1, default=float)
