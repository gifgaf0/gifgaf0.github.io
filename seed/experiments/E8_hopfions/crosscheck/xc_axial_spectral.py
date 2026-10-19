#!/usr/bin/env python3
"""Cross-check E8: axially symmetric Faddeev-Skyrme solitons A_{n,m} by a
Chebyshev pseudo-spectral energy minimisation (independent of the original code).

Ansatz  phi(rho, theta, z) = R_3(n theta) psi(q1, q2), psi a unit vector on the
meridian half-plane, psi = e3 on the symmetry axis and on the outer boundary;
deg(psi) = m, Hopf charge |Q| = n m.

Energy (Sutcliffe 2007 / PLAN.md E8 normalisation)
   E = C0 Int [ d_i phi.d_i phi + sum_{i<j} |d_i phi x d_j phi|^2 ] d^3x,
   C0 = 1/(32 sqrt2 pi^2).
With a = psi_rho, b = psi_z, c = (n/rho) e3 x psi (orthonormal frame),
   e = |a|^2+|b|^2+|c|^2 + |a x b|^2 + |a x c|^2 + |b x c|^2,
   E = C0 Int e 2 pi rho drho dz.

Domains
  'inf' : polar meridian coordinates r = L(1+x)/(1-x) (x in [-1,1] -> r in [0,inf)),
          theta = pi(1+y)/2 : the whole R^3, i.e. infinite volume, no box.
  'cyl' : cylinder rho <= R, |z| <= R with psi = e3 on its surface (fixed
          boundary, like the original axial2d runs), sinh-clustered maps.

Discretisation: u(x,y) in R^3 is the Chebyshev-Lobatto interpolant of nodal
values (boundary nodes fixed to e3), psi = u/|u| evaluated at Gauss-Legendre
points (over-integrated), energy by Gauss quadrature, exact gradient by
hand-coded reverse mode, minimised with L-BFGS.  Convergence is spectral.

Run:  NUMBA_NUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 python3 xc_axial_spectral.py
Writes xc_axial.json (resumable: finished cases are skipped).
"""
import json, os, sys, time
import numpy as np
from scipy.optimize import minimize

C0 = 1.0 / (32.0 * np.sqrt(2.0) * np.pi ** 2)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'xc_axial.json')
FDIR = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/xc_E8/fields_axial'


# ---------------------------------------------------------------- spectral tools
def cheb_nodes(N):
    return np.cos(np.pi * np.arange(N + 1) / N)


def cheb_D(N):
    x = cheb_nodes(N)
    c = np.ones(N + 1); c[0] = c[-1] = 2.0
    c = c * (-1.0) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1.0 / c) / (dX + np.eye(N + 1))
    D = D - np.diag(D.sum(axis=1))
    return D


def bary_matrix(N, t):
    x = cheb_nodes(N)
    w = (-1.0) ** np.arange(N + 1); w[0] *= 0.5; w[-1] *= 0.5
    diff = t[:, None] - x[None, :]
    exact = np.abs(diff) < 1e-14
    diff[exact] = 1.0
    M = w[None, :] / diff
    M = M / M.sum(axis=1, keepdims=True)
    rows = np.where(exact.any(axis=1))[0]
    for r in rows:
        M[r, :] = 0.0
        M[r, np.where(exact[r])[0][0]] = 1.0
    return M


# ---------------------------------------------------------------- geometry
class Geometry:
    """Orthogonal meridian coordinates (q1,q2) with scale factors h1,h2 and
    cylindrical radius rho, all evaluated at the Gauss points."""

    def __init__(self, kind, Nx, Ny, L=1.6, R=7.5, alpha=2.5, over=1.6):
        self.kind, self.Nx, self.Ny = kind, Nx, Ny
        Mx, My = int(over * Nx) + 4, int(over * Ny) + 4
        gx, wx = np.polynomial.legendre.leggauss(Mx)
        gy, wy = np.polynomial.legendre.leggauss(My)
        self.Px = bary_matrix(Nx, gx); self.Dx = self.Px @ cheb_D(Nx)
        self.Py = bary_matrix(Ny, gy); self.Dy = self.Py @ cheb_D(Ny)
        X, Y = np.meshgrid(gx, gy, indexing='ij')
        WX, WY = np.meshgrid(wx, wy, indexing='ij')
        if kind == 'inf':
            r = L * (1 + X) / (1 - X); dr = 2 * L / (1 - X) ** 2
            th = np.pi * (1 + Y) / 2; dth = np.pi / 2 * np.ones_like(Y)
            self.h1q = dr                 # h1 * dq1/dx
            self.h2q = r * dth            # h2 * dq2/dy
            self.rho = r * np.sin(th)
        elif kind == 'cyl':
            s = (1 + X) / 2
            rho = R * np.sinh(alpha * s) / np.sinh(alpha)
            drho = R * alpha * np.cosh(alpha * s) / np.sinh(alpha) / 2
            z = R * np.sinh(alpha * Y) / np.sinh(alpha)
            dz = R * alpha * np.cosh(alpha * Y) / np.sinh(alpha)
            self.h1q, self.h2q, self.rho = drho, dz, rho
        else:
            raise ValueError(kind)
        self.W = C0 * 2 * np.pi * self.rho * self.h1q * self.h2q * WX * WY
        self.WXY = WX * WY
        # physical coordinates of the Lobatto nodes (for initial data / plots)
        xn, yn = cheb_nodes(Nx), cheb_nodes(Ny)
        XN, YN = np.meshgrid(xn, yn, indexing='ij')
        with np.errstate(divide='ignore', invalid='ignore'):
            if kind == 'inf':
                rn = L * (1 + XN) / (1 - XN); tn = np.pi * (1 + YN) / 2
                self.node_rho = rn * np.sin(tn); self.node_z = rn * np.cos(tn)
            else:
                sn = (1 + XN) / 2
                self.node_rho = R * np.sinh(alpha * sn) / np.sinh(alpha)
                self.node_z = R * np.sinh(alpha * YN) / np.sinh(alpha)
        self.interior = np.zeros((Nx + 1, Ny + 1), bool)
        self.interior[1:-1, 1:-1] = True


def cross(a, b):
    return np.stack([a[..., 1] * b[..., 2] - a[..., 2] * b[..., 1],
                     a[..., 2] * b[..., 0] - a[..., 0] * b[..., 2],
                     a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]], axis=-1)


def dot(a, b):
    return np.einsum('...i,...i->...', a, b)


def _apply(A, u, B):
    # out[i,j,c] = sum_kl A[i,k] u[k,l,c] B[j,l]
    return np.stack([A @ u[:, :, c] @ B.T for c in range(u.shape[2])], axis=-1)


def _applyT(A, g, B):
    # out[k,l,c] = sum_ij A[i,k] g[i,j,c] B[j,l]
    return np.stack([A.T @ g[:, :, c] @ B for c in range(g.shape[2])], axis=-1)


def fields(G, u):
    return _apply(G.Px, u, G.Py), _apply(G.Dx, u, G.Py), _apply(G.Px, u, G.Dy)


def energy_grad(G, u, n, want_grad=True, parts=False):
    U, Ux, Uy = fields(G, u)
    nU = np.sqrt(dot(U, U))[..., None]
    psi = U / nU
    sx = dot(psi, Ux)[..., None]; sy = dot(psi, Uy)[..., None]
    px = (Ux - psi * sx) / nU
    py = (Uy - psi * sy) / nU
    s1 = (1.0 / G.h1q)[..., None]; s2 = (1.0 / G.h2q)[..., None]
    a = px * s1; b = py * s2
    kc = (n / G.rho)[..., None]
    e3xpsi = np.stack([-psi[..., 1], psi[..., 0], np.zeros_like(psi[..., 0])], -1)
    c = kc * e3xpsi
    aa, bb, cc = dot(a, a), dot(b, b), dot(c, c)
    ab, ac, bc = dot(a, b), dot(a, c), dot(b, c)
    e2 = aa + bb + cc
    e4 = (aa * bb - ab ** 2) + (aa * cc - ac ** 2) + (bb * cc - bc ** 2)
    W = G.W
    E2 = float(np.sum(W * e2)); E4 = float(np.sum(W * e4))
    E = E2 + E4
    if parts:
        deg = float(np.sum(G.WXY * dot(psi, cross(px, py)))) / (4 * np.pi)
        return E, E2, E4, deg
    if not want_grad:
        return E
    Wv = W[..., None]
    AA, BB, CC = aa[..., None], bb[..., None], cc[..., None]
    AB, AC, BC = ab[..., None], ac[..., None], bc[..., None]
    ga = Wv * (2 * a + 2 * (a * BB - b * AB) + 2 * (a * CC - c * AC))
    gb = Wv * (2 * b + 2 * (b * AA - a * AB) + 2 * (b * CC - c * BC))
    gc = Wv * (2 * c + 2 * (c * AA - a * AC) + 2 * (c * BB - b * BC))
    gpx = ga * s1; gpy = gb * s2
    gpsi = kc * np.stack([gc[..., 1], -gc[..., 0], np.zeros_like(gc[..., 0])], -1)
    # px = (Ux - psi (psi.Ux))/nU
    gUx = (gpx - psi * dot(psi, gpx)[..., None]) / nU
    gUy = (gpy - psi * dot(psi, gpy)[..., None]) / nU
    gpsi = gpsi - (gpx * sx + Ux * dot(psi, gpx)[..., None]) / nU \
                - (gpy * sy + Uy * dot(psi, gpy)[..., None]) / nU
    gnU = -(dot(gpx, px) + dot(gpy, py))[..., None] / nU
    gU = (gpsi - psi * dot(psi, gpsi)[..., None]) / nU + gnU * psi
    g = _applyT(G.Px, gU, G.Py) + _applyT(G.Dx, gUx, G.Py) + _applyT(G.Px, gUy, G.Dy)
    return E, g


# ---------------------------------------------------------------- initial data
def rational_map_psi(rho, z, n, m, s=1.0):
    """Sutcliffe's ansatz W = Z1^n/Z0^m evaluated on the theta = 0 half plane,
    profile f(r) = pi/(1 + (r/s)^2) (f(0)=pi, f(inf)=0)."""
    r = np.sqrt(rho ** 2 + z ** 2)
    f = np.pi / (1 + (r / s) ** 2)
    with np.errstate(divide='ignore', invalid='ignore'):
        sf_r = np.where(r > 0, np.sin(f) / np.where(r > 0, r, 1), 0.0)
    Z1 = rho * sf_r
    Z0 = np.cos(f) + 1j * z * sf_r
    W = Z1 ** n / Z0 ** m
    W = np.where(np.isfinite(W), W, 1e12)
    aW = np.abs(W) ** 2
    psi = np.stack([2 * W.real / (1 + aW), 2 * W.imag / (1 + aW), (1 - aW) / (1 + aW)], -1)
    return psi


def set_boundary(u, G):
    u[~G.interior] = np.array([0.0, 0.0, 1.0])
    return u


def interp_nodes(u_old, Nx_old, Ny_old, Nx, Ny):
    Mx = bary_matrix(Nx_old, cheb_nodes(Nx)); My = bary_matrix(Ny_old, cheb_nodes(Ny))
    return _apply(Mx, u_old, My)


def _sym_maps(G):
    """Reflection symmetry z -> -z combined with psi2 -> -psi2 (both domains are
    symmetric under y -> -y, node l <-> Ny-l).  It removes the z-translation zero
    mode, which a non-uniform grid would otherwise turn into a spurious drift."""
    Nx, Ny = G.Nx, G.Ny
    ind = [(k, l) for k in range(1, Nx) for l in range(1, Ny) if l < Ny - l]
    mid = [(k, Ny // 2) for k in range(1, Nx)] if Ny % 2 == 0 else []
    return ind, mid


def _unpack(G, v, u, ind, mid):
    ni = len(ind)
    a = v[:3 * ni].reshape(-1, 3)
    ki = np.array([p[0] for p in ind]); li = np.array([p[1] for p in ind])
    u[ki, li] = a
    u[ki, G.Ny - li] = a * np.array([1.0, -1.0, 1.0])
    if mid:
        km = np.array([p[0] for p in mid])
        b = v[3 * ni:].reshape(-1, 2)
        u[km, G.Ny // 2, 0] = b[:, 0]; u[km, G.Ny // 2, 1] = 0.0; u[km, G.Ny // 2, 2] = b[:, 1]
    return u


def _pack(G, u, ind, mid, grad=False):
    ki = np.array([p[0] for p in ind]); li = np.array([p[1] for p in ind])
    if grad:
        a = u[ki, li] + u[ki, G.Ny - li] * np.array([1.0, -1.0, 1.0])
    else:
        a = u[ki, li]
    parts = [a.ravel()]
    if mid:
        km = np.array([p[0] for p in mid])
        parts.append(u[km, G.Ny // 2][:, [0, 2]].ravel())
    return np.concatenate(parts)


def minimise(G, u0, n, maxiter=20000, tag=''):
    ind, mid = _sym_maps(G)
    u = u0.copy()

    def f(v):
        _unpack(G, v, u, ind, mid)
        E, g = energy_grad(G, u, n)
        return E, _pack(G, g, ind, mid, grad=True)

    t0 = time.time()
    res = minimize(f, _pack(G, u, ind, mid), jac=True, method='L-BFGS-B',
                   options=dict(maxiter=maxiter, maxfun=maxiter * 2, maxcor=40,
                                ftol=1e-16, gtol=1e-11))
    _unpack(G, res.x, u, ind, mid)
    u = u / np.linalg.norm(u, axis=-1, keepdims=True)
    E, E2, E4, deg = energy_grad(G, u, n, parts=True)
    gn = np.linalg.norm(f(_pack(G, u, ind, mid))[1])
    print(f'  {tag} N=({G.Nx},{G.Ny}) E={E:.9f} E2={E2:.6f} E4={E4:.6f} deg={deg:.8f} '
          f'iters={res.nit} |g|={gn:.2e} {time.time()-t0:.1f}s msg={res.message}', flush=True)
    return u, dict(E=E, E2=E2, E4=E4, deg=deg, Q=n * deg, iters=int(res.nit),
                   gnorm=float(gn), msg=str(res.message), secs=time.time() - t0)


def grad_check():
    G = Geometry('inf', 12, 10, L=1.5)
    u = set_boundary(rational_map_psi(G.node_rho, G.node_z, 1, 1).copy(), G)
    rng = np.random.default_rng(1)
    u[G.interior] += 0.05 * rng.standard_normal(u[G.interior].shape)
    E, g = energy_grad(G, u, 1)
    errs = []
    for _ in range(6):
        i, j, c = rng.integers(1, 12), rng.integers(1, 10), rng.integers(0, 3)
        e = 1e-6; up = u.copy(); um = u.copy(); up[i, j, c] += e; um[i, j, c] -= e
        fd = (energy_grad(G, up, 1, False) - energy_grad(G, um, 1, False)) / (2 * e)
        errs.append(abs(fd - g[i, j, c]) / max(abs(fd), 1e-8))
    return max(errs)


def quadrature_check():
    """Energy of an analytic axial test field psi from W = Z1/Z0 with the profile
    f = pi/(1+r^2): compare 'inf' spectral quadrature at increasing N, and the
    'cyl' domain R=40 (tail beyond R is ~1e-5 relative)."""
    out = {}
    for N in (24, 48, 96):
        G = Geometry('inf', N, N, L=1.5)
        u = set_boundary(rational_map_psi(G.node_rho, G.node_z, 1, 1), G)
        # energy of the interpolant converges spectrally to the analytic field's energy
        out[f'inf_N{N}'] = energy_grad(G, u, 1, parts=True)[0]
    return out


CASES = []
NS_INF = {(1, 1): [24, 32, 48, 64, 80], (2, 1): [24, 32, 48, 64, 80], (2, 2): [48, 64, 80, 96]}
NS_CYL = {(1, 1): [32, 48, 64, 80, 96, 112], (2, 1): [32, 48, 64, 80, 96, 112],
          (2, 2): [48, 64, 80, 96, 112]}
for (n, m) in [(1, 1), (2, 1), (2, 2)]:
    CASES.append(dict(name=f'n{n}m{m}_inf', n=n, m=m, kind='inf', L=1.6 if n == 1 else 2.0,
                      Ns=NS_INF[(n, m)]))
# axial A_{3,1} (a saddle in 3D according to Sutcliffe; the Q = 3 minimum is the bent A~_{3,1})
CASES.append(dict(name='n3m1_inf', n=3, m=1, kind='inf', L=2.2, Ns=[24, 32, 48, 64, 80]))
CASES.append(dict(name='n3m1_cyl7.5', n=3, m=1, kind='cyl', R=7.5, alpha=2.5, Ns=[32, 48, 64, 80, 96]))
for (n, m) in [(1, 1), (2, 2)]:
    for L in (1.1, 2.6):     # independence of the radial map scale
        CASES.append(dict(name=f'n{n}m{m}_infL{L}', n=n, m=m, kind='inf', L=L,
                          Ns=[32, 48, 64] if m == 1 else [48, 64, 80]))
for (n, m) in [(1, 1), (2, 1), (2, 2)]:
    for R in (7.5, 12.0, 25.0):
        CASES.append(dict(name=f'n{n}m{m}_cyl{R}', n=n, m=m, kind='cyl', R=R,
                          alpha={7.5: 2.5, 12.0: 3.2, 25.0: 4.5}[R], Ns=NS_CYL[(n, m)]))


def main():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    if 'checks' not in res:
        res['checks'] = dict(grad_rel_err=grad_check(), quadrature=quadrature_check())
        print('checks', res['checks'], flush=True)
        json.dump(res, open(OUT, 'w'), indent=1)
    only = sys.argv[1:]
    for cs in CASES:
        if only and cs['name'] not in only:
            continue
        if cs['name'] in res and res[cs['name']].get('done'):
            continue
        print('case', cs['name'], flush=True)
        entry = res.get(cs['name'], {'runs': {}})
        u = None; Nprev = None
        for N in cs['Ns']:
            kw = dict(L=cs.get('L', 1.6), R=cs.get('R', 7.5), alpha=cs.get('alpha', 2.5))
            G = Geometry(cs['kind'], N, N, **kw)
            if u is None:
                u0 = rational_map_psi(G.node_rho, G.node_z, cs['n'], cs['m'],
                                      s={1: 1.0, 2: 1.4, 3: 1.7}[cs['n']])
            else:
                u0 = interp_nodes(u, Nprev, Nprev, N, N)
            u0 = set_boundary(u0, G)
            u, info = minimise(G, u0, cs['n'], maxiter=8000 if cs['m'] == 1 else 40000, tag=cs['name'])
            entry['runs'][str(N)] = info
            Nprev = N
            res[cs['name']] = entry
            json.dump(res, open(OUT, 'w'), indent=1)
            np.save(os.path.join(FDIR, f"{cs['name']}_N{N}.npy"), u)
        entry['done'] = True
        res[cs['name']] = entry
        json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    os.makedirs(FDIR, exist_ok=True)
    main()
