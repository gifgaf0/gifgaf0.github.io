"""
fs_lib.py -- Faddeev-Skyrme (Skyrme-Faddeev) model on a cubic lattice.

Energy (Sutcliffe 2007 normalisation, Ward bound E >= Q^{3/4}):

    E = C0 * Int [ d_i phi . d_i phi + 1/2 (d_i phi x d_j phi).(d_i phi x d_j phi) ] d^3x
      = C0 * Int [ sum_i |d_i phi|^2 + sum_{i<j} |d_i phi x d_j phi|^2 ] d^3x,
    C0 = 1/(32 sqrt(2) pi^2).

Discretisation (no checkerboard null modes):
  * sigma term: forward differences on lattice links,
        E2 = h * sum_links |phi(x+e_i) - phi(x)|^2
  * Skyrme term: on every plaquette (i,j) take the two i-edges {a, c} and the
    two j-edges {b, d}; the plaquette energy is the average over the 4 corner
    pairings,
        E4 = (1/(4h)) * sum_plaq [ |a x b|^2 + |a x d|^2 + |c x b|^2 + |c x d|^2 ].
    Every corner term is the exact cross product of two lattice edges meeting at
    that corner, so any plaquette with non-zero spherical area costs energy.
  * The gradient is the exact derivative of this discrete energy.
Field fixed to e3 on the whole boundary of the grid (as in Sutcliffe 2007).
Grid: N^3 points on [-L, L]^3, h = 2L/(N-1).
"""
import numpy as np
from numba import njit, prange

C0 = 1.0 / (32.0 * np.sqrt(2.0) * np.pi ** 2)


# ---------------------------------------------------------------------------
# energy and exact discrete gradient
# ---------------------------------------------------------------------------
@njit(inline='always', fastmath=True)
def _plaq(a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3):
    # a, c : the two edges along direction i ; b, d : along direction j
    aa = a1 * a1 + a2 * a2 + a3 * a3
    cc = c1 * c1 + c2 * c2 + c3 * c3
    bb = b1 * b1 + b2 * b2 + b3 * b3
    dd = d1 * d1 + d2 * d2 + d3 * d3
    ab = a1 * b1 + a2 * b2 + a3 * b3
    ad = a1 * d1 + a2 * d2 + a3 * d3
    cb = c1 * b1 + c2 * b2 + c3 * b3
    cd = c1 * d1 + c2 * d2 + c3 * d3
    en = (aa * bb - ab * ab) + (aa * dd - ad * ad) + (cc * bb - cb * cb) + (cc * dd - cd * cd)
    sbd = bb + dd
    sac = aa + cc
    # d(en)/da = 2*ga etc.
    ga1 = a1 * sbd - ab * b1 - ad * d1
    ga2 = a2 * sbd - ab * b2 - ad * d2
    ga3 = a3 * sbd - ab * b3 - ad * d3
    gc1 = c1 * sbd - cb * b1 - cd * d1
    gc2 = c2 * sbd - cb * b2 - cd * d2
    gc3 = c3 * sbd - cb * b3 - cd * d3
    gb1 = b1 * sac - ab * a1 - cb * c1
    gb2 = b2 * sac - ab * a2 - cb * c2
    gb3 = b3 * sac - ab * a3 - cb * c3
    gd1 = d1 * sac - ad * a1 - cd * c1
    gd2 = d2 * sac - ad * a2 - cd * c2
    gd3 = d3 * sac - ad * a3 - cd * c3
    return (en, ga1, ga2, ga3, gc1, gc2, gc3, gb1, gb2, gb3, gd1, gd2, gd3)


@njit(parallel=True, fastmath=True, cache=True)
def energy_grad(phi, h, grad, want_grad):
    """Return (E2, E4) WITHOUT the factor C0; fill grad = d(E2+E4)/d phi."""
    N = phi.shape[0]
    M = N - 1
    if want_grad:
        for i in prange(N):
            for j in range(N):
                for k in range(N):
                    grad[i, j, k, 0] = 0.0
                    grad[i, j, k, 1] = 0.0
                    grad[i, j, k, 2] = 0.0
    e2s = np.zeros(N)
    e4s = np.zeros(N)
    w2 = 2.0 * h
    w4 = 0.5 / h
    for par in range(2):
        nsl = (M - par + 1) // 2
        for s in prange(nsl):
            i = 2 * s + par
            e2 = 0.0
            e4 = 0.0
            for j in range(M):
                for k in range(M):
                    p0 = phi[i, j, k]
                    px = phi[i + 1, j, k]
                    py = phi[i, j + 1, k]
                    pz = phi[i, j, k + 1]
                    pxy = phi[i + 1, j + 1, k]
                    pxz = phi[i + 1, j, k + 1]
                    pyz = phi[i, j + 1, k + 1]
                    # links from base point
                    ex1 = px[0] - p0[0]; ex2 = px[1] - p0[1]; ex3 = px[2] - p0[2]
                    ey1 = py[0] - p0[0]; ey2 = py[1] - p0[1]; ey3 = py[2] - p0[2]
                    ez1 = pz[0] - p0[0]; ez2 = pz[1] - p0[1]; ez3 = pz[2] - p0[2]
                    e2 += (ex1 * ex1 + ex2 * ex2 + ex3 * ex3 + ey1 * ey1 + ey2 * ey2 + ey3 * ey3
                           + ez1 * ez1 + ez2 * ez2 + ez3 * ez3)
                    # other edges needed
                    # x-edge at (i,j+1,k): pxy - py ; x-edge at (i,j,k+1): pxz - pz
                    # y-edge at (i+1,j,k): pxy - px ; y-edge at (i,j,k+1): pyz - pz
                    # z-edge at (i+1,j,k): pxz - px ; z-edge at (i,j+1,k): pyz - py
                    xy1 = pxy[0] - py[0]; xy2 = pxy[1] - py[1]; xy3 = pxy[2] - py[2]   # x-edge, y+1
                    xz1 = pxz[0] - pz[0]; xz2 = pxz[1] - pz[1]; xz3 = pxz[2] - pz[2]   # x-edge, z+1
                    yx1 = pxy[0] - px[0]; yx2 = pxy[1] - px[1]; yx3 = pxy[2] - px[2]   # y-edge, x+1
                    yz1 = pyz[0] - pz[0]; yz2 = pyz[1] - pz[1]; yz3 = pyz[2] - pz[2]   # y-edge, z+1
                    zx1 = pxz[0] - px[0]; zx2 = pxz[1] - px[1]; zx3 = pxz[2] - px[2]   # z-edge, x+1
                    zy1 = pyz[0] - py[0]; zy2 = pyz[1] - py[1]; zy3 = pyz[2] - py[2]   # z-edge, y+1
                    # plaquette xy: a = ex, c = xy (x-edges); b = ey, d = yx (y-edges)
                    r = _plaq(ex1, ex2, ex3, ey1, ey2, ey3, xy1, xy2, xy3, yx1, yx2, yx3)
                    e4 += r[0]
                    if want_grad:
                        # a = ex : px - p0
                        grad[i + 1, j, k, 0] += w4 * r[1]; grad[i + 1, j, k, 1] += w4 * r[2]; grad[i + 1, j, k, 2] += w4 * r[3]
                        grad[i, j, k, 0] -= w4 * r[1]; grad[i, j, k, 1] -= w4 * r[2]; grad[i, j, k, 2] -= w4 * r[3]
                        # c = xy : pxy - py
                        grad[i + 1, j + 1, k, 0] += w4 * r[4]; grad[i + 1, j + 1, k, 1] += w4 * r[5]; grad[i + 1, j + 1, k, 2] += w4 * r[6]
                        grad[i, j + 1, k, 0] -= w4 * r[4]; grad[i, j + 1, k, 1] -= w4 * r[5]; grad[i, j + 1, k, 2] -= w4 * r[6]
                        # b = ey : py - p0
                        grad[i, j + 1, k, 0] += w4 * r[7]; grad[i, j + 1, k, 1] += w4 * r[8]; grad[i, j + 1, k, 2] += w4 * r[9]
                        grad[i, j, k, 0] -= w4 * r[7]; grad[i, j, k, 1] -= w4 * r[8]; grad[i, j, k, 2] -= w4 * r[9]
                        # d = yx : pxy - px
                        grad[i + 1, j + 1, k, 0] += w4 * r[10]; grad[i + 1, j + 1, k, 1] += w4 * r[11]; grad[i + 1, j + 1, k, 2] += w4 * r[12]
                        grad[i + 1, j, k, 0] -= w4 * r[10]; grad[i + 1, j, k, 1] -= w4 * r[11]; grad[i + 1, j, k, 2] -= w4 * r[12]
                    # plaquette xz: a = ex, c = xz ; b = ez, d = zx
                    r = _plaq(ex1, ex2, ex3, ez1, ez2, ez3, xz1, xz2, xz3, zx1, zx2, zx3)
                    e4 += r[0]
                    if want_grad:
                        grad[i + 1, j, k, 0] += w4 * r[1]; grad[i + 1, j, k, 1] += w4 * r[2]; grad[i + 1, j, k, 2] += w4 * r[3]
                        grad[i, j, k, 0] -= w4 * r[1]; grad[i, j, k, 1] -= w4 * r[2]; grad[i, j, k, 2] -= w4 * r[3]
                        # c = xz : pxz - pz
                        grad[i + 1, j, k + 1, 0] += w4 * r[4]; grad[i + 1, j, k + 1, 1] += w4 * r[5]; grad[i + 1, j, k + 1, 2] += w4 * r[6]
                        grad[i, j, k + 1, 0] -= w4 * r[4]; grad[i, j, k + 1, 1] -= w4 * r[5]; grad[i, j, k + 1, 2] -= w4 * r[6]
                        # b = ez : pz - p0
                        grad[i, j, k + 1, 0] += w4 * r[7]; grad[i, j, k + 1, 1] += w4 * r[8]; grad[i, j, k + 1, 2] += w4 * r[9]
                        grad[i, j, k, 0] -= w4 * r[7]; grad[i, j, k, 1] -= w4 * r[8]; grad[i, j, k, 2] -= w4 * r[9]
                        # d = zx : pxz - px
                        grad[i + 1, j, k + 1, 0] += w4 * r[10]; grad[i + 1, j, k + 1, 1] += w4 * r[11]; grad[i + 1, j, k + 1, 2] += w4 * r[12]
                        grad[i + 1, j, k, 0] -= w4 * r[10]; grad[i + 1, j, k, 1] -= w4 * r[11]; grad[i + 1, j, k, 2] -= w4 * r[12]
                    # plaquette yz: a = ey, c = yz ; b = ez, d = zy
                    r = _plaq(ey1, ey2, ey3, ez1, ez2, ez3, yz1, yz2, yz3, zy1, zy2, zy3)
                    e4 += r[0]
                    if want_grad:
                        grad[i, j + 1, k, 0] += w4 * r[1]; grad[i, j + 1, k, 1] += w4 * r[2]; grad[i, j + 1, k, 2] += w4 * r[3]
                        grad[i, j, k, 0] -= w4 * r[1]; grad[i, j, k, 1] -= w4 * r[2]; grad[i, j, k, 2] -= w4 * r[3]
                        # c = yz : pyz - pz
                        grad[i, j + 1, k + 1, 0] += w4 * r[4]; grad[i, j + 1, k + 1, 1] += w4 * r[5]; grad[i, j + 1, k + 1, 2] += w4 * r[6]
                        grad[i, j, k + 1, 0] -= w4 * r[4]; grad[i, j, k + 1, 1] -= w4 * r[5]; grad[i, j, k + 1, 2] -= w4 * r[6]
                        # b = ez : pz - p0
                        grad[i, j, k + 1, 0] += w4 * r[7]; grad[i, j, k + 1, 1] += w4 * r[8]; grad[i, j, k + 1, 2] += w4 * r[9]
                        grad[i, j, k, 0] -= w4 * r[7]; grad[i, j, k, 1] -= w4 * r[8]; grad[i, j, k, 2] -= w4 * r[9]
                        # d = zy : pyz - py
                        grad[i, j + 1, k + 1, 0] += w4 * r[10]; grad[i, j + 1, k + 1, 1] += w4 * r[11]; grad[i, j + 1, k + 1, 2] += w4 * r[12]
                        grad[i, j + 1, k, 0] -= w4 * r[10]; grad[i, j + 1, k, 1] -= w4 * r[11]; grad[i, j + 1, k, 2] -= w4 * r[12]
                    if want_grad:
                        # sigma-term gradient, 2h * e on each link
                        grad[i + 1, j, k, 0] += w2 * ex1; grad[i + 1, j, k, 1] += w2 * ex2; grad[i + 1, j, k, 2] += w2 * ex3
                        grad[i, j + 1, k, 0] += w2 * ey1; grad[i, j + 1, k, 1] += w2 * ey2; grad[i, j + 1, k, 2] += w2 * ey3
                        grad[i, j, k + 1, 0] += w2 * ez1; grad[i, j, k + 1, 1] += w2 * ez2; grad[i, j, k + 1, 2] += w2 * ez3
                        grad[i, j, k, 0] -= w2 * (ex1 + ey1 + ez1)
                        grad[i, j, k, 1] -= w2 * (ex2 + ey2 + ez2)
                        grad[i, j, k, 2] -= w2 * (ex3 + ey3 + ez3)
            e2s[i] = e2
            e4s[i] = e4
    return h * e2s.sum(), 0.25 / h * e4s.sum()


@njit(parallel=True, fastmath=True, cache=True)
def energy_density_cells(phi, h):
    """Energy density (without C0) attributed to cell centres (M^3 array):
    each link energy is shared by the 4 cells containing it, each plaquette by
    the 2 cells containing it.  Sum(dens)*h^3 = E2+E4 up to boundary links."""
    N = phi.shape[0]
    M = N - 1
    dens = np.zeros((M, M, M))
    for i in prange(M):
        for j in range(M):
            for k in range(M):
                tot = 0.0
                # 12 links of the cube, each weight 1/4
                for a in range(2):
                    for b in range(2):
                        # x-links
                        tot += 0.25 * h * _sq(phi, i, j + a, k + b, i + 1, j + a, k + b)
                        tot += 0.25 * h * _sq(phi, i + a, j, k + b, i + a, j + 1, k + b)
                        tot += 0.25 * h * _sq(phi, i + a, j + b, k, i + a, j + b, k + 1)
                # 6 faces, each weight 1/2
                for a in range(2):
                    tot += 0.5 * 0.25 / h * _plaqE(phi, i, j, k + a, 0, 1)
                    tot += 0.5 * 0.25 / h * _plaqE(phi, i, j + a, k, 0, 2)
                    tot += 0.5 * 0.25 / h * _plaqE(phi, i + a, j, k, 1, 2)
                dens[i, j, k] = tot / h ** 3
    return dens


@njit(inline='always', fastmath=True)
def _sq(phi, i0, j0, k0, i1, j1, k1):
    s = 0.0
    for c in range(3):
        d = phi[i1, j1, k1, c] - phi[i0, j0, k0, c]
        s += d * d
    return s


@njit(inline='always', fastmath=True)
def _plaqE(phi, i, j, k, d1, d2):
    o1 = np.zeros(3, np.int64)
    o2 = np.zeros(3, np.int64)
    o1[d1] = 1
    o2[d2] = 1
    p00 = phi[i, j, k]
    p10 = phi[i + o1[0], j + o1[1], k + o1[2]]
    p01 = phi[i + o2[0], j + o2[1], k + o2[2]]
    p11 = phi[i + o1[0] + o2[0], j + o1[1] + o2[1], k + o1[2] + o2[2]]
    r = _plaq(p10[0] - p00[0], p10[1] - p00[1], p10[2] - p00[2],
              p01[0] - p00[0], p01[1] - p00[1], p01[2] - p00[2],
              p11[0] - p01[0], p11[1] - p01[1], p11[2] - p01[2],
              p11[0] - p10[0], p11[1] - p10[1], p11[2] - p10[2])
    return r[0]


# ---------------------------------------------------------------------------
# arrested Newton flow update (sigma-model kinetic term, unit mass density)
# ---------------------------------------------------------------------------
@njit(fastmath=True, cache=True)
def _anf_slab(phi, vel, grad, i, N, ih3, dt, fmax, fsum):
    fm = 0.0
    fs_ = 0.0
    for j in range(1, N - 1):
        for k in range(1, N - 1):
            q1 = phi[i, j, k, 0]
            q2 = phi[i, j, k, 1]
            q3 = phi[i, j, k, 2]
            g1 = -grad[i, j, k, 0] * ih3
            g2 = -grad[i, j, k, 1] * ih3
            g3 = -grad[i, j, k, 2] * ih3
            fp = g1 * q1 + g2 * q2 + g3 * q3
            f1 = g1 - fp * q1
            f2 = g2 - fp * q2
            f3 = g3 - fp * q3
            ff = f1 * f1 + f2 * f2 + f3 * f3
            fs_ += ff
            fm = max(fm, ff)
            v1 = vel[i, j, k, 0] + dt * f1
            v2 = vel[i, j, k, 1] + dt * f2
            v3 = vel[i, j, k, 2] + dt * f3
            r1 = q1 + dt * v1
            r2 = q2 + dt * v2
            r3 = q3 + dt * v3
            nr = 1.0 / np.sqrt(r1 * r1 + r2 * r2 + r3 * r3)
            s1 = r1 * nr
            s2 = r2 * nr
            s3 = r3 * nr
            vp = v1 * s1 + v2 * s2 + v3 * s3
            vel[i, j, k, 0] = v1 - vp * s1
            vel[i, j, k, 1] = v2 - vp * s2
            vel[i, j, k, 2] = v3 - vp * s3
            phi[i, j, k, 0] = s1
            phi[i, j, k, 1] = s2
            phi[i, j, k, 2] = s3
    fmax[i] = fm
    fsum[i] = fs_


@njit(parallel=True, fastmath=True, cache=True)
def anf_step(phi, vel, grad, h, dt):
    """v += dt*F ; phi += dt*v ; normalise ; project v.  F = -(1/h^3) grad, tangent.
    Boundary points are not updated.  Returns (max|F|, sum|F|^2 h^3)."""
    N = phi.shape[0]
    ih3 = 1.0 / h ** 3
    fmax = np.zeros(N)
    fsum = np.zeros(N)
    for i in prange(1, N - 1):
        _anf_slab(phi, vel, grad, i, N, ih3, dt, fmax, fsum)
    return np.sqrt(fmax.max()), fsum.sum() * h ** 3


@njit(parallel=True, cache=True)
def zero_field(a):
    N = a.shape[0]
    for i in prange(N):
        for j in range(N):
            for k in range(N):
                a[i, j, k, 0] = 0.0
                a[i, j, k, 1] = 0.0
                a[i, j, k, 2] = 0.0


def min_phi3(phi):
    return float(phi[..., 2].min())


# ---------------------------------------------------------------------------
# grids and initial conditions
# ---------------------------------------------------------------------------
def grid(N, L=7.5):
    x = np.linspace(-L, L, N)
    return x, x[1] - x[0]


def stereo_to_phi(W):
    """phi from W = (phi1 + i phi2)/(1 + phi3); W=0 -> e3, W=inf -> -e3."""
    a = np.abs(W) ** 2
    phi = np.empty(W.shape + (3,))
    finite = np.isfinite(a)
    Wf = np.where(finite, W, 0.0)
    af = np.where(finite, a, 0.0)
    phi[..., 0] = np.where(finite, 2 * Wf.real / (1 + af), 0.0)
    phi[..., 1] = np.where(finite, 2 * Wf.imag / (1 + af), 0.0)
    phi[..., 2] = np.where(finite, (1 - af) / (1 + af), -1.0)
    return phi


def rational_map_field(N, mapfun, L=7.5, Lf=None, offset=(0.0, 0.0, 0.0), squash=(1.0, 1.0, 1.0)):
    """Field from W = p(Z1,Z0)/q(Z1,Z0) given as mapfun(Z1, Z0) -> (p, q).
    (Z1, Z0) = ((x1 + i x2) sin f / r, cos f + i x3 sin f / r), f = pi (Lf - r)/Lf for r < Lf.
    Large |W| handled via phi computed from (p, q) homogeneously."""
    if Lf is None:
        Lf = L
    x, h = grid(N, L)
    X1, X2, X3 = np.meshgrid(x - offset[0], x - offset[1], x - offset[2], indexing='ij')
    X1 = X1 / squash[0]; X2 = X2 / squash[1]; X3 = X3 / squash[2]
    r = np.sqrt(X1 ** 2 + X2 ** 2 + X3 ** 2)
    f = np.where(r < Lf, np.pi * (Lf - r) / Lf, 0.0)
    rs = np.where(r > 1e-12, r, 1.0)
    sf = np.where(r > 1e-12, np.sin(f) / rs, np.pi / Lf)  # sin f / r -> pi/Lf at r = 0
    Z1 = (X1 + 1j * X2) * sf
    Z0 = np.cos(f) + 1j * X3 * sf
    p, q = mapfun(Z1, Z0)
    # phi from homogeneous (p, q): W = p/q
    pp = np.abs(p) ** 2
    qq = np.abs(q) ** 2
    den = pp + qq
    phi = np.empty((N, N, N, 3))
    pq = p * np.conj(q)  # W*|q|^2
    phi[..., 0] = 2 * pq.real / den
    phi[..., 1] = 2 * pq.imag / den
    phi[..., 2] = (qq - pp) / den
    set_boundary(phi)
    return phi, h


def set_boundary(phi):
    for sl in [np.s_[0], np.s_[-1]]:
        for ax in range(3):
            idx = [slice(None)] * 3
            idx[ax] = sl
            phi[tuple(idx)] = (0.0, 0.0, 1.0)
    return phi


MAPS = {
    # name: (Q, function(Z1, Z0) -> (p, q))
    'A11': (1, lambda Z1, Z0: (Z1, Z0)),
    'A21': (2, lambda Z1, Z0: (Z1 ** 2, Z0)),
    'A12': (2, lambda Z1, Z0: (Z1, Z0 ** 2)),
    'A31': (3, lambda Z1, Z0: (Z1 ** 3, Z0)),
    'A22': (4, lambda Z1, Z0: (Z1 ** 2, Z0 ** 2)),
    'A41': (4, lambda Z1, Z0: (Z1 ** 4, Z0)),
    'K32_Q5': (5, lambda Z1, Z0: (Z1 * Z0, Z1 ** 3 + Z0 ** 2)),        # (alpha,beta)=(1,1)
    'K32_Q6': (6, lambda Z1, Z0: (Z1 ** 3, Z1 ** 3 + Z0 ** 2)),        # (alpha,beta)=(3,0)
    'L22_Q6': (6, lambda Z1, Z0: (Z1 ** 3, Z1 ** 2 - Z0 ** 2)),        # Sutcliffe (3.7), n = 2
    'K32_Q7': (7, lambda Z1, Z0: (Z1 ** 2 * Z0, Z1 ** 3 + Z0 ** 2)),   # trefoil, (alpha,beta)=(2,1)
}


def interpolate_field(phi_c, Nf, L=7.5):
    """Cubic-spline interpolation of a field on N_c^3 to N_f^3 (same box), renormalised."""
    from scipy.ndimage import map_coordinates
    Nc = phi_c.shape[0]
    xf = np.linspace(0, Nc - 1, Nf)
    G = np.meshgrid(xf, xf, xf, indexing='ij')
    coords = np.array(G)
    out = np.empty((Nf, Nf, Nf, 3))
    for c in range(3):
        out[..., c] = map_coordinates(phi_c[..., c], coords, order=3, mode='nearest')
    out /= np.linalg.norm(out, axis=-1, keepdims=True)
    set_boundary(out)
    return out


# ---------------------------------------------------------------------------
# Hopf charge (Whitehead integral) and lattice hedgehog detector
# ---------------------------------------------------------------------------
@njit(inline='always', fastmath=False)
def _tri_solid_angle(a0, a1, a2, b0, b1, b2, c0, c1, c2):
    # signed solid angle of spherical triangle (a,b,c), Van Oosterom-Strackee
    det = a0 * (b1 * c2 - b2 * c1) - a1 * (b0 * c2 - b2 * c0) + a2 * (b0 * c1 - b1 * c0)
    den = 1.0 + (a0 * b0 + a1 * b1 + a2 * b2) + (b0 * c0 + b1 * c1 + b2 * c2) + (c0 * a0 + c1 * a1 + c2 * a2)
    return 2.0 * np.arctan2(det, den)


@njit(inline='always')
def _quad(p, q, r, s):
    # oriented quad p -> q -> r -> s
    return (_tri_solid_angle(p[0], p[1], p[2], q[0], q[1], q[2], r[0], r[1], r[2])
            + _tri_solid_angle(p[0], p[1], p[2], r[0], r[1], r[2], s[0], s[1], s[2]))


@njit(parallel=True, cache=True)
def face_fluxes(phi):
    """Solid-angle fluxes through all plaquettes.
    Fx[i,j,k] : yz-plaquette at base (i,j,k), normal +x (orientation y->z), shape (N, M, M)
    Fy[i,j,k] : zx-plaquette, normal +y (orientation z->x), shape (M, N, M)
    Fz[i,j,k] : xy-plaquette, normal +z (orientation x->y), shape (M, M, N)."""
    N = phi.shape[0]
    M = N - 1
    Fx = np.zeros((N, M, M))
    Fy = np.zeros((M, N, M))
    Fz = np.zeros((M, M, N))
    for i in prange(N):
        for j in range(N):
            for k in range(N):
                if j < M and k < M:
                    Fx[i, j, k] = _quad(phi[i, j, k], phi[i, j + 1, k], phi[i, j + 1, k + 1], phi[i, j, k + 1])
                if i < M and k < M:
                    Fy[i, j, k] = _quad(phi[i, j, k], phi[i, j, k + 1], phi[i + 1, j, k + 1], phi[i + 1, j, k])
                if i < M and j < M:
                    Fz[i, j, k] = _quad(phi[i, j, k], phi[i + 1, j, k], phi[i + 1, j + 1, k], phi[i, j + 1, k])
    return Fx, Fy, Fz


def hopf_charge(phi, h, pad=1, workers=2):
    """Q = (1/16 pi^2) Int A.B,  B_i = 1/2 eps_ijk F_jk,  F_jk = phi.(d_j phi x d_k phi),
    curl A = B solved in Coulomb gauge by FFT (spectral wavenumbers).
    B at cell centres from solid-angle face fluxes (average of the two opposite faces).
    Returns (Q, n_hedgehog_cells, total_flux_check)."""
    import scipy.fft as sfft
    Fx, Fy, Fz = face_fluxes(phi)
    Bx = 0.5 * (Fx[:-1] + Fx[1:]) / h ** 2
    By = 0.5 * (Fy[:, :-1] + Fy[:, 1:]) / h ** 2
    Bz = 0.5 * (Fz[:, :, :-1] + Fz[:, :, 1:]) / h ** 2
    div = (Fx[1:] - Fx[:-1]) + (Fy[:, 1:] - Fy[:, :-1]) + (Fz[:, :, 1:] - Fz[:, :, :-1])
    nhh = int(np.sum(np.abs(div) > 2 * np.pi))
    M = Bx.shape[0]
    Mp = M * pad
    B = [np.zeros((Mp, Mp, Mp)) for _ in range(3)]
    for c, b in enumerate((Bx, By, Bz)):
        B[c][:M, :M, :M] = b
    k1 = 2 * np.pi * sfft.fftfreq(Mp, d=h)
    k3 = 2 * np.pi * sfft.rfftfreq(Mp, d=h)
    KX, KY, KZ = np.meshgrid(k1, k1, k3, indexing='ij', sparse=True)
    K2 = KX ** 2 + KY ** 2 + KZ ** 2
    K2[0, 0, 0] = 1.0
    Bk = [sfft.rfftn(b, workers=workers) for b in B]
    # A = i k x B / k^2
    Ak0 = 1j * (KY * Bk[2] - KZ * Bk[1]) / K2
    Ak1 = 1j * (KZ * Bk[0] - KX * Bk[2]) / K2
    Ak2 = 1j * (KX * Bk[1] - KY * Bk[0]) / K2
    for a in (Ak0, Ak1, Ak2):
        a[0, 0, 0] = 0.0
    A = [sfft.irfftn(a, s=(Mp, Mp, Mp), workers=workers) for a in (Ak0, Ak1, Ak2)]
    integrand = A[0] * B[0] + A[1] * B[1] + A[2] * B[2]
    Q = integrand.sum() * h ** 3 / (16 * np.pi ** 2)
    return float(Q), nhh, float(np.abs(div).sum())


# ---------------------------------------------------------------------------
# preimage curves, linking, knot type
# ---------------------------------------------------------------------------
def rotation_to_south(p):
    """Rotation R (3x3) with R p = -e3, rotating about the axis perpendicular to p and e3."""
    p = np.asarray(p, float) / np.linalg.norm(p)
    t = np.array([0, 0, -1.0])
    v = np.cross(p, t)
    s = np.linalg.norm(v)
    c = p @ t
    if s < 1e-14:
        return np.eye(3) if c > 0 else np.diag([1, -1, -1.0])
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * ((1 - c) / s ** 2)


def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def preimage_curves(phi, h, L=7.5, target=(0, 0, -1.0), thresh=0.0):
    """Extract the preimage of `target` as oriented closed polygons.
    The field is rotated so that target -> -e3; the curve is where w = psi1 + i psi2 = 0
    with psi3 < 0.  A plaquette is pierced when the winding of arg w around it is +-1
    (only plaquettes with all corners psi3 < thresh are considered).  Pierced faces are
    joined through cubes (in-face -> out-face), giving oriented loops.
    Returns (list of (n,3) arrays of points in physical coordinates, info dict)."""
    R = rotation_to_south(target)
    psi = phi @ R.T
    th = np.arctan2(psi[..., 1], psi[..., 0])
    neg = psi[..., 2] < thresh
    N = phi.shape[0]
    x0 = -L

    def wind(c00, c10, c11, c01):
        return np.rint((_wrap(c10 - c00) + _wrap(c11 - c10) + _wrap(c01 - c11) + _wrap(c00 - c01)) / (2 * np.pi)).astype(int)

    # x-faces (yz plaquettes) shape (N, N-1, N-1), orientation y->z
    Wx = wind(th[:, :-1, :-1], th[:, 1:, :-1], th[:, 1:, 1:], th[:, :-1, 1:])
    Mx = neg[:, :-1, :-1] & neg[:, 1:, :-1] & neg[:, 1:, 1:] & neg[:, :-1, 1:]
    Wx *= Mx
    # y-faces (zx plaquettes) shape (N-1, N, N-1), orientation z->x
    Wy = wind(th[:-1, :, :-1], th[:-1, :, 1:], th[1:, :, 1:], th[1:, :, :-1])
    My = neg[:-1, :, :-1] & neg[:-1, :, 1:] & neg[1:, :, 1:] & neg[1:, :, :-1]
    Wy *= My
    # z-faces (xy plaquettes) shape (N-1, N-1, N), orientation x->y
    Wz = wind(th[:-1, :-1, :], th[1:, :-1, :], th[1:, 1:, :], th[:-1, 1:, :])
    Mz = neg[:-1, :-1, :] & neg[1:, :-1, :] & neg[1:, 1:, :] & neg[:-1, 1:, :]
    Wz *= Mz
    wcomp = psi[..., 0] + 1j * psi[..., 1]

    # face list: key (axis, i, j, k)
    faces = {}
    pts = []

    def zero_loc(axis, i, j, k):
        # bilinear interpolation of w on the face; Newton from centre
        if axis == 0:
            c = [wcomp[i, j, k], wcomp[i, j + 1, k], wcomp[i, j, k + 1], wcomp[i, j + 1, k + 1]]
        elif axis == 1:
            c = [wcomp[i, j, k], wcomp[i, j, k + 1], wcomp[i + 1, j, k], wcomp[i + 1, j, k + 1]]
        else:
            c = [wcomp[i, j, k], wcomp[i + 1, j, k], wcomp[i, j + 1, k], wcomp[i + 1, j + 1, k]]
        # w(u,v) = c00 (1-u)(1-v) + c10 u (1-v) + c01 (1-u) v + c11 u v  (u first local dir, v second)
        c00, c10, c01, c11 = c
        u, v = 0.5, 0.5
        for _ in range(20):
            w = c00 * (1 - u) * (1 - v) + c10 * u * (1 - v) + c01 * (1 - u) * v + c11 * u * v
            wu = (c10 - c00) * (1 - v) + (c11 - c01) * v
            wv = (c01 - c00) * (1 - u) + (c11 - c10) * u
            J = np.array([[wu.real, wv.real], [wu.imag, wv.imag]])
            try:
                d = np.linalg.solve(J, [-w.real, -w.imag])
            except np.linalg.LinAlgError:
                break
            u += d[0]; v += d[1]
            u = min(max(u, 0.0), 1.0); v = min(max(v, 0.0), 1.0)
            if abs(d[0]) + abs(d[1]) < 1e-10:
                break
        base = np.array([x0 + i * h, x0 + j * h, x0 + k * h])
        if axis == 0:
            return base + h * np.array([0, u, v])
        elif axis == 1:
            return base + h * np.array([v, 0, u])
        else:
            return base + h * np.array([u, v, 0])

    for axis, Wa in enumerate((Wx, Wy, Wz)):
        for (i, j, k) in zip(*np.nonzero(Wa)):
            faces[(axis, i, j, k)] = int(Wa[i, j, k])
    # connect through cubes
    succ = {}
    ambiguous = 0
    cubes = {}
    for (axis, i, j, k), w in faces.items():
        # the face separates cube "minus" (index-1 along axis) and cube "plus" (index along axis)
        cm = [i, j, k]; cm[axis] -= 1
        cp = [i, j, k]
        # orientation +1 along +axis: leaves cube minus, enters cube plus
        if w > 0:
            src, dst = tuple(cm), tuple(cp)
        else:
            src, dst = tuple(cp), tuple(cm)
        cubes.setdefault(src, {'in': [], 'out': []})['out'].append((axis, i, j, k))
        cubes.setdefault(dst, {'in': [], 'out': []})['in'].append((axis, i, j, k))
    unmatched = 0
    for c, d in cubes.items():
        ins, outs = d['in'], d['out']
        if len(ins) != len(outs):
            unmatched += abs(len(ins) - len(outs))
        if len(ins) > 1:
            ambiguous += 1
        for a, b in zip(ins, outs):
            succ[a] = b
    # trace loops
    loops = []
    visited = set()
    open_chains = 0
    for f0 in faces:
        if f0 in visited:
            continue
        chain = [f0]
        visited.add(f0)
        f = f0
        closed = False
        while True:
            if f not in succ:
                break
            f = succ[f]
            if f == f0:
                closed = True
                break
            if f in visited:
                break
            chain.append(f)
            visited.add(f)
        if closed and len(chain) >= 4:
            loops.append(np.array([zero_loc(*fc) for fc in chain]))
        else:
            open_chains += 1
    info = dict(n_pierced=len(faces), ambiguous_cubes=ambiguous, unmatched=unmatched,
                open_chains=open_chains)
    return loops, info


def _segments_2d_cross(P, Q):
    """P, Q: (n,2) closed polygon vertices -> all proper crossings of segments.
    returns list of (ia, ta, ib, tb)."""
    out = []
    A0 = P; A1 = np.roll(P, -1, axis=0)
    B0 = Q; B1 = np.roll(Q, -1, axis=0)
    dB = B1 - B0
    for ia in range(len(P)):
        a0 = A0[ia]; a1 = A1[ia]
        da = a1 - a0
        den = da[0] * dB[:, 1] - da[1] * dB[:, 0]
        w = B0 - a0
        with np.errstate(divide='ignore', invalid='ignore'):
            ta = (w[:, 0] * dB[:, 1] - w[:, 1] * dB[:, 0]) / den
            tb = (w[:, 0] * da[1] - w[:, 1] * da[0]) / den
        ok = (np.abs(den) > 1e-14) & (ta >= 0) & (ta < 1) & (tb >= 0) & (tb < 1)
        for ib in np.nonzero(ok)[0]:
            out.append((ia, float(ta[ib]), int(ib), float(tb[ib])))
    return out


def crossing_data(loops, R):
    """Crossings of the projections (after rotation R, project on xy) of closed polygons.
    Returns list of dicts: comp/param of over and under strand, sign."""
    rl = [L @ R.T for L in loops]
    cr = []
    for a in range(len(rl)):
        for b in range(a, len(rl)):
            P = rl[a]; Qp = rl[b]
            lst = _segments_2d_cross(P[:, :2], Qp[:, :2])
            for (ia, ta, ib, tb) in lst:
                if a == b:
                    if ib <= ia:
                        continue
                    n = len(P)
                    if ib == ia or (ib - ia) % n in (1, n - 1):
                        continue
                za = P[ia, 2] + ta * (P[(ia + 1) % len(P), 2] - P[ia, 2])
                zb = Qp[ib, 2] + tb * (Qp[(ib + 1) % len(Qp), 2] - Qp[ib, 2])
                da = P[(ia + 1) % len(P), :2] - P[ia, :2]
                db = Qp[(ib + 1) % len(Qp), :2] - Qp[ib, :2]
                if za > zb:
                    over = (a, ia + ta, da); under = (b, ib + tb, db)
                else:
                    over = (b, ib + tb, db); under = (a, ia + ta, da)
                s = np.sign(over[2][0] * under[2][1] - over[2][1] * under[2][0])
                cr.append(dict(oc=over[0], os=over[1], uc=under[0], us=under[1], sign=int(s)))
    return cr


def linking_matrix(loops, seed=1):
    rng = np.random.default_rng(seed)
    R = random_rotation(rng)
    cr = crossing_data(loops, R)
    n = len(loops)
    Lk = np.zeros((n, n))
    wr = np.zeros(n)
    for c in cr:
        if c['oc'] != c['uc']:
            Lk[c['oc'], c['uc']] += 0.5 * c['sign']
            Lk[c['uc'], c['oc']] += 0.5 * c['sign']
        else:
            wr[c['oc']] += c['sign']
    return Lk, wr, cr


def random_rotation(rng):
    q = rng.normal(size=4)
    q /= np.linalg.norm(q)
    a, b, c, d = q
    return np.array([[a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)],
                     [2 * (b * c + a * d), a * a - b * b + c * c - d * d, 2 * (c * d - a * b)],
                     [2 * (b * d - a * c), 2 * (c * d + a * b), a * a - b * b - c * c + d * d]])


def alexander_polynomial(loop, seed=2):
    """Alexander polynomial of a closed polygon (single component), normalised so that
    the lowest power is t^0 and the leading coefficient is positive.  Returns a sympy Poly
    expression and the number of crossings in the projection used."""
    import sympy as sp
    t = sp.symbols('t')
    rng = np.random.default_rng(seed)
    R = random_rotation(rng)
    cr = crossing_data([loop], R)
    n = len(cr)
    if n == 0:
        return sp.Integer(1), 0
    us = np.array([c['us'] for c in cr])
    order = np.argsort(us)
    us_sorted = us[order]

    def arc(s):
        return int(np.sum(us_sorted < s)) % n

    Mx = sp.zeros(n, n)
    for m, ci in enumerate(order):
        c = cr[ci]
        i_in = m % n            # arc ending at this undercrossing
        j_out = (m + 1) % n     # arc starting after it
        k_ov = arc(c['os'])
        Mx[m, k_ov] += 1 - t
        if c['sign'] > 0:
            Mx[m, i_in] += t
            Mx[m, j_out] += -1
        else:
            Mx[m, i_in] += -1
            Mx[m, j_out] += t
    if n == 1:
        return sp.Integer(1), n
    D = sp.expand(Mx[:-1, :-1].det(method='berkowitz'))
    if D == 0:
        return sp.Integer(0), n
    P = sp.Poly(D, t)
    # strip powers of t
    coeffs = P.all_coeffs()[::-1]  # lowest first
    while coeffs and coeffs[0] == 0:
        coeffs.pop(0)
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    if coeffs[-1] < 0:
        coeffs = [-c for c in coeffs]
    expr = sum(c * t ** e for e, c in enumerate(coeffs))
    return sp.expand(expr), n


def energy_inertia(phi, h, L=7.5):
    """Centre and principal moments of the energy density (axial-symmetry diagnostic)."""
    d = energy_density_cells(phi, h)
    N = phi.shape[0]
    xc = -L + h * (np.arange(N - 1) + 0.5)
    X, Y, Z = np.meshgrid(xc, xc, xc, indexing='ij')
    w = d * h ** 3
    tot = w.sum()
    c = np.array([(w * X).sum(), (w * Y).sum(), (w * Z).sum()]) / tot
    Xs = [X - c[0], Y - c[1], Z - c[2]]
    I = np.zeros((3, 3))
    r2 = Xs[0] ** 2 + Xs[1] ** 2 + Xs[2] ** 2
    for a in range(3):
        for b in range(3):
            I[a, b] = (w * ((r2 if a == b else 0) - Xs[a] * Xs[b])).sum() / tot
    ev, evec = np.linalg.eigh(I)
    return c, ev, evec, tot
