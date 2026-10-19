"""Cross-check E8: 3D lattice tools written independently of the original code.

Field arrays: phi[i,j,k,c] on the grid x_i = -L + i h (i = 0..N-1), h = 2L/(N-1),
unit vectors, phi = e3 on the boundary and (by convention) outside the box.

Energies (all multiplied by C0 = 1/(32 sqrt2 pi^2)):
  energy_c2    second-order centred differences, D_i = (phi(x+h)-phi(x-h))/2h
  energy_c4    fourth-order centred differences
  energy_lp    link/plaquette energy as DESCRIBED in the original REPORT.md
               (sigma term on links, Skyrme term averaged over the 4 corner
               pairings of each plaquette) -- my own implementation of that text
  energy_grad_c4   value and exact gradient of energy_c4 (for relaxation)
Hopf charge:
  hopf_whitehead   B from 4th-order centred differences, A = curl (G * B) with the
                   free-space Green function by zero-padded FFT (no periodic images)
Curves:
  preimage_curves  oriented closed polygons phi^{-1}(p) from face windings
  linking_number   exact Gauss linking number of two closed polygons
  knot_det / alexander  knot determinant and Alexander polynomial from projections
"""
import numpy as np
import numba as nb

C0 = 1.0 / (32.0 * np.sqrt(2.0) * np.pi ** 2)


@nb.njit(cache=True, inline='always')
def _get(phi, i, j, k, c, N):
    if i < 0 or j < 0 or k < 0 or i >= N or j >= N or k >= N:
        return 1.0 if c == 2 else 0.0
    return phi[i, j, k, c]


@nb.njit(parallel=True, cache=True)
def _energy_centred(phi, h, order):
    N = phi.shape[0]
    tot2 = np.zeros(N); tot4 = np.zeros(N)
    for i in nb.prange(N):
        s2 = 0.0; s4 = 0.0
        D = np.empty((3, 3))
        for j in range(N):
            for k in range(N):
                for c in range(3):
                    if order == 2:
                        D[0, c] = (_get(phi, i + 1, j, k, c, N) - _get(phi, i - 1, j, k, c, N)) / (2 * h)
                        D[1, c] = (_get(phi, i, j + 1, k, c, N) - _get(phi, i, j - 1, k, c, N)) / (2 * h)
                        D[2, c] = (_get(phi, i, j, k + 1, c, N) - _get(phi, i, j, k - 1, c, N)) / (2 * h)
                    else:
                        D[0, c] = (-_get(phi, i + 2, j, k, c, N) + 8 * _get(phi, i + 1, j, k, c, N)
                                   - 8 * _get(phi, i - 1, j, k, c, N) + _get(phi, i - 2, j, k, c, N)) / (12 * h)
                        D[1, c] = (-_get(phi, i, j + 2, k, c, N) + 8 * _get(phi, i, j + 1, k, c, N)
                                   - 8 * _get(phi, i, j - 1, k, c, N) + _get(phi, i, j - 2, k, c, N)) / (12 * h)
                        D[2, c] = (-_get(phi, i, j, k + 2, c, N) + 8 * _get(phi, i, j, k + 1, c, N)
                                   - 8 * _get(phi, i, j, k - 1, c, N) + _get(phi, i, j, k - 2, c, N)) / (12 * h)
                for a in range(3):
                    s2 += D[a, 0] ** 2 + D[a, 1] ** 2 + D[a, 2] ** 2
                for a in range(3):
                    for b in range(a + 1, 3):
                        cx = D[a, 1] * D[b, 2] - D[a, 2] * D[b, 1]
                        cy = D[a, 2] * D[b, 0] - D[a, 0] * D[b, 2]
                        cz = D[a, 0] * D[b, 1] - D[a, 1] * D[b, 0]
                        s4 += cx * cx + cy * cy + cz * cz
        tot2[i] = s2; tot4[i] = s4
    return tot2.sum() * h ** 3, tot4.sum() * h ** 3


def energy_c2(phi, h):
    e2, e4 = _energy_centred(phi, h, 2)
    return C0 * (e2 + e4), C0 * e2, C0 * e4


def energy_c4(phi, h):
    e2, e4 = _energy_centred(phi, h, 4)
    return C0 * (e2 + e4), C0 * e2, C0 * e4


@nb.njit(cache=True, inline='always')
def _cr2(X0, X1, X2, Y0, Y1, Y2):
    cx = X1 * Y2 - X2 * Y1
    cy = X2 * Y0 - X0 * Y2
    cz = X0 * Y1 - X1 * Y0
    return cx * cx + cy * cy + cz * cz


@nb.njit(parallel=True, cache=True)
def _energy_lp(phi, h):
    N = phi.shape[0]
    t2 = np.zeros(N); t4 = np.zeros(N)
    off = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    for i in nb.prange(N):
        s2 = 0.0; s4 = 0.0
        for j in range(N):
            for k in range(N):
                p0 = phi[i, j, k]
                for a in range(3):
                    ia = i + off[a, 0]; ja = j + off[a, 1]; ka = k + off[a, 2]
                    if ia >= N or ja >= N or ka >= N:
                        continue
                    pa = phi[ia, ja, ka]
                    s2 += (pa[0] - p0[0]) ** 2 + (pa[1] - p0[1]) ** 2 + (pa[2] - p0[2]) ** 2
                    for b in range(a + 1, 3):
                        ib = i + off[b, 0]; jb = j + off[b, 1]; kb = k + off[b, 2]
                        if ib >= N or jb >= N or kb >= N:
                            continue
                        pb = phi[ib, jb, kb]
                        pab = phi[ia + off[b, 0], ja + off[b, 1], ka + off[b, 2]]
                        A0 = pa[0] - p0[0]; A1 = pa[1] - p0[1]; A2 = pa[2] - p0[2]      # a-edge at base
                        B0 = pb[0] - p0[0]; B1 = pb[1] - p0[1]; B2 = pb[2] - p0[2]      # b-edge at base
                        C0_ = pab[0] - pb[0]; C1 = pab[1] - pb[1]; C2 = pab[2] - pb[2]  # a-edge at base+b
                        D0 = pab[0] - pa[0]; D1 = pab[1] - pa[1]; D2 = pab[2] - pa[2]  # b-edge at base+a
                        s4 += (_cr2(A0, A1, A2, B0, B1, B2) + _cr2(A0, A1, A2, D0, D1, D2)
                               + _cr2(C0_, C1, C2, B0, B1, B2) + _cr2(C0_, C1, C2, D0, D1, D2))
        t2[i] = s2; t4[i] = s4
    return t2.sum() * h, t4.sum() / (4 * h)


def energy_lp(phi, h):
    e2, e4 = _energy_lp(phi, h)
    return C0 * (e2 + e4), C0 * e2, C0 * e4


# ------------------------------------------------------------ 4th-order energy + gradient
@nb.njit(parallel=True, cache=True)
def _c4_pass1(phi, h, G):
    """G[a,i,j,k,:] = d e / d D_a at each point; returns sums of e2, e4."""
    N = phi.shape[0]
    t2 = np.zeros(N); t4 = np.zeros(N)
    for i in nb.prange(N):
        D = np.empty((3, 3))
        s2 = 0.0; s4 = 0.0
        for j in range(N):
            for k in range(N):
                for c in range(3):
                    D[0, c] = (-_get(phi, i + 2, j, k, c, N) + 8 * _get(phi, i + 1, j, k, c, N)
                               - 8 * _get(phi, i - 1, j, k, c, N) + _get(phi, i - 2, j, k, c, N)) / (12 * h)
                    D[1, c] = (-_get(phi, i, j + 2, k, c, N) + 8 * _get(phi, i, j + 1, k, c, N)
                               - 8 * _get(phi, i, j - 1, k, c, N) + _get(phi, i, j - 2, k, c, N)) / (12 * h)
                    D[2, c] = (-_get(phi, i, j, k + 2, c, N) + 8 * _get(phi, i, j, k + 1, c, N)
                               - 8 * _get(phi, i, j, k - 1, c, N) + _get(phi, i, j, k - 2, c, N)) / (12 * h)
                dd = np.empty((3, 3))
                for a in range(3):
                    for b in range(3):
                        dd[a, b] = D[a, 0] * D[b, 0] + D[a, 1] * D[b, 1] + D[a, 2] * D[b, 2]
                s2 += dd[0, 0] + dd[1, 1] + dd[2, 2]
                s4 += (dd[0, 0] * dd[1, 1] - dd[0, 1] ** 2) + (dd[0, 0] * dd[2, 2] - dd[0, 2] ** 2) \
                    + (dd[1, 1] * dd[2, 2] - dd[1, 2] ** 2)
                for a in range(3):
                    for c in range(3):
                        g = 2 * D[a, c]
                        for b in range(3):
                            if b != a:
                                g += 2 * (D[a, c] * dd[b, b] - D[b, c] * dd[a, b])
                        G[a, i, j, k, c] = g
        t2[i] = s2; t4[i] = s4
    return t2.sum(), t4.sum()


@nb.njit(parallel=True, cache=True)
def _c4_pass2(G, h, out):
    N = G.shape[1]
    w = np.array([1.0, -8.0, 8.0, -1.0]) / (12 * h)   # coefficients of phi(x+s), s=-2,-1,1,2
    sh = np.array([-2, -1, 1, 2])
    for i in nb.prange(N):
        for j in range(N):
            for k in range(N):
                for c in range(3):
                    acc = 0.0
                    for q in range(4):
                        s = sh[q]; cw = w[q]
                        # phi(y) enters D_a(x) for x = y - s e_a with weight cw
                        ii = i - s
                        if ii >= 0 and ii < N:
                            acc += cw * G[0, ii, j, k, c]
                        jj = j - s
                        if jj >= 0 and jj < N:
                            acc += cw * G[1, i, jj, k, c]
                        kk = k - s
                        if kk >= 0 and kk < N:
                            acc += cw * G[2, i, j, kk, c]
                    out[i, j, k, c] = acc


class C4Energy:
    def __init__(self, N):
        self.G = np.zeros((3, N, N, N, 3))
        self.g = np.zeros((N, N, N, 3))

    def __call__(self, phi, h):
        s2, s4 = _c4_pass1(phi, h, self.G)
        _c4_pass2(self.G, h, self.g)
        E = C0 * h ** 3 * (s2 + s4)
        return E, C0 * h ** 3 * s2, C0 * h ** 3 * s4, self.g * (C0 * h ** 3)


# ------------------------------------------------------------ Hopf charge
def _d4(f, h, axis):
    """4th-order centred derivative of a scalar field padded with its far value 0
    or phi-components (treated by caller)."""
    return (-np.roll(f, -2, axis) + 8 * np.roll(f, -1, axis) - 8 * np.roll(f, 1, axis)
            + np.roll(f, 2, axis)) / (12 * h)


def hopf_whitehead(phi, h, pad=6):
    """Q = 1/(16 pi^2) Int A.B, B_i = 1/2 eps_ijk phi.(d_j phi x d_k phi),
    A = curl Psi, -Lap Psi = B solved with the free-space kernel (zero padding)."""
    N = phi.shape[0]
    P = N + 2 * pad
    f = np.zeros((P, P, P, 3)); f[..., 2] = 1.0
    f[pad:pad + N, pad:pad + N, pad:pad + N] = phi
    d = [np.stack([_d4(f[..., c], h, ax) for c in range(3)], -1) for ax in range(3)]
    # outermost 2 layers of the padded block: derivative wraps around but field = e3 there -> 0
    B = np.empty((P, P, P, 3))
    B[..., 0] = np.einsum('...c,...c->...', f, np.cross(d[1], d[2]))
    B[..., 1] = np.einsum('...c,...c->...', f, np.cross(d[2], d[0]))
    B[..., 2] = np.einsum('...c,...c->...', f, np.cross(d[0], d[1]))
    # free-space Poisson by zero-padded FFT (Hockney): grid 2P
    M = 2 * P
    idx = np.arange(M); idx = np.where(idx <= M // 2, idx, idx - M) * h
    X, Y, Z = np.meshgrid(idx, idx, idx, indexing='ij', sparse=True)
    R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    with np.errstate(divide='ignore'):
        Gk = 1.0 / (4 * np.pi * R)
    Gk[0, 0, 0] = 2.3800772 / (4 * np.pi * h)   # cell average of 1/(4 pi r) over a cube of side h
    Gh = np.fft.rfftn(Gk) * h ** 3
    Psi = np.empty((P, P, P, 3))
    for c in range(3):
        bp = np.zeros((M, M, M)); bp[:P, :P, :P] = B[..., c]
        Psi[..., c] = np.fft.irfftn(np.fft.rfftn(bp) * Gh, s=(M, M, M))[:P, :P, :P]
    A = np.empty_like(Psi)
    A[..., 0] = _d4(Psi[..., 2], h, 1) - _d4(Psi[..., 1], h, 2)
    A[..., 1] = _d4(Psi[..., 0], h, 2) - _d4(Psi[..., 2], h, 0)
    A[..., 2] = _d4(Psi[..., 1], h, 0) - _d4(Psi[..., 0], h, 1)
    s = slice(2, P - 2)
    Q = np.sum(A[s, s, s] * B[s, s, s]) * h ** 3 / (16 * np.pi ** 2)
    flux_check = np.sum(np.abs(B)) * h ** 3
    return float(Q)


# ------------------------------------------------------------ preimage curves
def preimage_curves(phi, h, L, p, cos_max=-0.5):
    """Oriented closed polygons of phi^{-1}(p).  A cell face is pierced when the
    projection of phi onto the plane perpendicular to p winds once around the face
    and phi.p > -cos_max... (i.e. phi near p: mean phi.p > -cos_max).
    Returns list of (n,3) arrays of points (face piercing points)."""
    p = np.asarray(p, float); p /= np.linalg.norm(p)
    t = np.array([1.0, 0, 0]) if abs(p[0]) < 0.9 else np.array([0, 1.0, 0])
    ea = np.cross(p, t); ea /= np.linalg.norm(ea); eb = np.cross(p, ea)
    wa = phi @ ea; wb = phi @ eb; wp = phi @ p
    ang = np.arctan2(wb, wa)
    N = phi.shape[0]
    faces = []   # (cellA, cellB, point, sign) curve passes from cell A to cell B
    def wrap(d):
        return (d + np.pi) % (2 * np.pi) - np.pi
    for ax in range(3):
        a1, a2 = [x for x in range(3) if x != ax]
        # face spanned by axes a1,a2 with lower corner at index; loop corners counter-clockwise in (a1,a2)
        sl = [slice(None)] * 3
        def sh(arr, d1, d2):
            idx = [slice(0, N - 1)] * 3
            idx[ax] = slice(0, N)
            idx[a1] = slice(d1, N - 1 + d1); idx[a2] = slice(d2, N - 1 + d2)
            return arr[tuple(idx)]
        c00, c10, c11, c01 = sh(ang, 0, 0), sh(ang, 1, 0), sh(ang, 1, 1), sh(ang, 0, 1)
        wind = wrap(c10 - c00) + wrap(c11 - c10) + wrap(c01 - c11) + wrap(c00 - c01)
        wsum = sh(wp, 0, 0) + sh(wp, 1, 0) + sh(wp, 1, 1) + sh(wp, 0, 1)
        nw = np.rint(wind / (2 * np.pi)).astype(int)
        sel = (nw != 0) & (wsum / 4 > -cos_max)
        for idx in zip(*np.nonzero(sel)):
            idx = list(idx)
            s = int(nw[tuple(idx)])
            # piercing point: zero of bilinear interpolation of (wa,wb) ~ use weights
            corners = [(0, 0), (1, 0), (1, 1), (0, 1)]
            vals = []
            pts = []
            for (d1, d2) in corners:
                q = idx.copy(); q[a1] += d1; q[a2] += d2
                vals.append(np.hypot(wa[tuple(q)], wb[tuple(q)]))
                pts.append(np.array(q, float))
            wts = 1.0 / (np.array(vals) + 1e-12)
            pt = (np.array(pts) * wts[:, None]).sum(0) / wts.sum()
            pt = -L + pt * h
            # cells on either side of the face along ax: lower cell index idx[ax]-1, upper idx[ax]
            lo = idx.copy(); lo[ax] -= 1
            hi = idx.copy()
            # orientation: winding counter-clockwise in (a1,a2) with right-handed (a1,a2,ax)?
            rh = (a1, a2, ax) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
            sg = s if rh else -s
            for _rep in range(abs(sg)):        # winding 2 = two strands through one face
                if sg > 0:
                    faces.append((tuple(lo), tuple(hi), pt))
                else:
                    faces.append((tuple(hi), tuple(lo), pt))
    # build cell graph: out-edges per cell
    from collections import defaultdict
    out_of = defaultdict(list); into = defaultdict(list)
    for fi, (A, B, pt) in enumerate(faces):
        out_of[A].append(fi); into[B].append(fi)
    used = np.zeros(len(faces), bool)
    curves = []; problems = 0
    for f0 in range(len(faces)):
        if used[f0]:
            continue
        chain = [f0]; used[f0] = True
        cur = f0
        while True:
            B = faces[cur][1]
            cand = [f for f in out_of[B] if not used[f]]
            if not cand:
                if faces[f0][0] == B and f0 in out_of[B]:
                    pass
                else:
                    problems += 1
                break
            if len(cand) > 1:
                problems += 1
                # choose nearest
                pc = faces[cur][2]
                cand.sort(key=lambda f: np.linalg.norm(faces[f][2] - pc))
            cur = cand[0]; used[cur] = True; chain.append(cur)
        curves.append(np.array([faces[f][2] for f in chain]))
    return curves, problems


def linking_number(P1, P2):
    """Exact Gauss linking number of two closed polygons (Klenin-Langowski)."""
    a1 = P1; a2 = np.roll(P1, -1, 0)
    b1 = P2; b2 = np.roll(P2, -1, 0)
    A1 = a1[:, None, :]; A2 = a2[:, None, :]; B1 = b1[None, :, :]; B2 = b2[None, :, :]
    r13 = B1 - A1; r14 = B2 - A1; r23 = B1 - A2; r24 = B2 - A2

    def nrm(v):
        return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-300)
    n1 = nrm(np.cross(r13, r14)); n2 = nrm(np.cross(r14, r24))
    n3 = nrm(np.cross(r24, r23)); n4 = nrm(np.cross(r23, r13))
    cl = lambda x: np.clip(x, -1, 1)
    om = (np.arcsin(cl(np.sum(n1 * n2, -1))) + np.arcsin(cl(np.sum(n2 * n3, -1)))
          + np.arcsin(cl(np.sum(n3 * n4, -1))) + np.arcsin(cl(np.sum(n4 * n1, -1))))
    sgn = np.sign(np.sum(np.cross(B2 - B1, A2 - A1) * r13, -1))
    return float(np.sum(om * sgn) / (4 * np.pi))


def _crossings(P, R):
    """Project closed polygon P (after rotation R) to xy; return list of crossings
    (seg_over, t_over, seg_under, t_under, sign)."""
    Q = P @ R.T
    n = len(Q)
    a = Q[:, :2]; b = np.roll(Q, -1, 0)[:, :2]
    za = Q[:, 2]; zb = np.roll(Q, -1, 0)[:, 2]
    d = b - a
    out = []
    for i in range(n):
        j = np.arange(i + 2, n)
        if i == 0:
            j = j[j != n - 1]
        if len(j) == 0:
            continue
        den = d[i, 0] * d[j, 1] - d[i, 1] * d[j, 0]
        w = a[j] - a[i]
        with np.errstate(divide='ignore', invalid='ignore'):
            s = (w[:, 0] * d[j, 1] - w[:, 1] * d[j, 0]) / den
            t = (w[:, 0] * d[i, 1] - w[:, 1] * d[i, 0]) / den
        ok = (np.abs(den) > 1e-14) & (s >= 0) & (s < 1) & (t >= 0) & (t < 1)
        for jj, ss, tt in zip(j[ok], s[ok], t[ok]):
            zi = za[i] + ss * (zb[i] - za[i]); zj = za[jj] + tt * (zb[jj] - za[jj])
            cr = d[i, 0] * d[jj, 1] - d[i, 1] * d[jj, 0]
            if zi > zj:   # i over
                sign = np.sign(cr)
                out.append((i, ss, jj, tt, sign))
            else:
                sign = -np.sign(cr)
                out.append((jj, tt, i, ss, sign))
    return out


def alexander(P, R):
    """Alexander polynomial (sympy expression, normalised) and determinant of the
    knot given by closed polygon P projected after rotation R."""
    import sympy as sp
    cr = _crossings(P, R)
    nc = len(cr)
    if nc == 0:
        return sp.Integer(1), 1, 0
    # under-crossing positions along the curve define arcs
    unders = sorted([(c[2] + c[3], ci) for ci, c in enumerate(cr)])
    pos = np.array([u[0] for u in unders])

    def arc_of(x):
        # arc k runs from under-crossing k to k+1 (cyclic); arc index of position x
        k = np.searchsorted(pos, x, side='right') - 1
        return k % nc
    t = sp.symbols('t')
    M = sp.zeros(nc, nc)
    for row, (u, ci) in enumerate(unders):
        so, to, su, tu, sg = cr[ci]
        ov = arc_of(so + to)
        uin = (row - 1) % nc     # arc ending at this under-crossing
        uout = row               # arc starting here
        if sg > 0:
            M[row, ov] += 1 - t; M[row, uin] += t; M[row, uout] += -1
        else:
            M[row, ov] += 1 - t; M[row, uin] += -1; M[row, uout] += t
    Mm = M[1:, 1:]
    poly = sp.expand(Mm.det()) if nc > 1 else sp.Integer(1)
    if poly == 0:
        return sp.Integer(0), 0, nc
    # normalise: divide by lowest power of t, fix sign so that leading coeff > 0 symmetric
    pl = sp.Poly(poly, t)
    terms = pl.terms()
    lo = min(e[0][0] for e in terms)
    poly = sp.expand(poly / t ** lo)
    pl = sp.Poly(poly, t)
    if pl.LC() < 0:
        poly = -poly
    det = abs(int(poly.subs(t, -1)))
    return sp.simplify(poly), det, nc


def random_rotation(rng):
    q = rng.standard_normal(4); q /= np.linalg.norm(q)
    a, b, c, d = q
    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                     [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
                     [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]])


# ------------------------------------------------------------ test fields
def rational_map_field(N, L, num, den, offset=(0, 0, 0), prof='sutcliffe'):
    """phi from W = num(Z1,Z0)/den(Z1,Z0); Z1 = (x1+ix2) sin f/r, Z0 = cos f + i x3 sin f/r."""
    x = np.linspace(-L, L, N)
    X, Y, Z = np.meshgrid(x - offset[0], x - offset[1], x - offset[2], indexing='ij')
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    if prof == 'sutcliffe':
        f = np.where(r < L, np.pi * (L - r) / L, 0.0)
    else:
        f = np.pi / (1 + (r / prof) ** 2)
    sfr = np.where(r > 0, np.sin(f) / np.where(r > 0, r, 1.0), 0.0)
    Z1 = (X + 1j * Y) * sfr
    Z0 = np.cos(f) + 1j * Z * sfr
    n = num(Z1, Z0); d = den(Z1, Z0)
    # phi from W = n/d without dividing: phi1+i phi2 = 2 n conj(d)/(|n|^2+|d|^2)
    an = np.abs(n) ** 2; ad = np.abs(d) ** 2
    w = 2 * n * np.conj(d) / (an + ad)
    phi = np.stack([w.real, w.imag, (ad - an) / (an + ad)], -1)
    phi[0, :, :] = phi[-1, :, :] = phi[:, 0, :] = phi[:, -1, :] = phi[:, :, 0] = phi[:, :, -1] = [0, 0, 1]
    return phi


# ------------------------------------------------------------ link/plaquette energy with stride s
# (value + exact gradient; stride 1 = the scheme described in REPORT.md, stride 2 =
#  the same on the 2h sub-lattices averaged over the 8 cosets; R4 = (4 E_1 - E_2)/3
#  cancels the h^2 error term: a fourth-order scheme without centred-stencil null modes)
@nb.njit(parallel=True, cache=True, fastmath=False)
def _lps_pass1(phi, s, w2, w4, Gl, Gc, off, pa_, pb_):
    N = phi.shape[0]
    t2 = np.zeros(N); t4 = np.zeros(N)
    for i in nb.prange(N):
        e2 = 0.0; e4 = 0.0
        for j in range(N):
            for k in range(N):
                p0x = phi[i, j, k, 0]; p0y = phi[i, j, k, 1]; p0z = phi[i, j, k, 2]
                for a in range(3):
                    ia = i + s * off[a, 0]; ja = j + s * off[a, 1]; ka = k + s * off[a, 2]
                    if ia < N and ja < N and ka < N:
                        dx = phi[ia, ja, ka, 0] - p0x; dy = phi[ia, ja, ka, 1] - p0y; dz = phi[ia, ja, ka, 2] - p0z
                        e2 += dx * dx + dy * dy + dz * dz
                        Gl[a, i, j, k, 0] = 2 * w2 * dx; Gl[a, i, j, k, 1] = 2 * w2 * dy; Gl[a, i, j, k, 2] = 2 * w2 * dz
                    else:
                        Gl[a, i, j, k, 0] = 0.0; Gl[a, i, j, k, 1] = 0.0; Gl[a, i, j, k, 2] = 0.0
                for p in range(3):
                    a = pa_[p]; b = pb_[p]
                    ia = i + s * off[a, 0]; ja = j + s * off[a, 1]; ka = k + s * off[a, 2]
                    ib = i + s * off[b, 0]; jb = j + s * off[b, 1]; kb = k + s * off[b, 2]
                    iab = ia + s * off[b, 0]; jab = ja + s * off[b, 1]; kab = ka + s * off[b, 2]
                    if iab < N and jab < N and kab < N:
                        Ax = phi[ia, ja, ka, 0] - p0x; Ay = phi[ia, ja, ka, 1] - p0y; Az = phi[ia, ja, ka, 2] - p0z
                        Bx = phi[ib, jb, kb, 0] - p0x; By = phi[ib, jb, kb, 1] - p0y; Bz = phi[ib, jb, kb, 2] - p0z
                        Cx = phi[iab, jab, kab, 0] - phi[ib, jb, kb, 0]
                        Cy = phi[iab, jab, kab, 1] - phi[ib, jb, kb, 1]
                        Cz = phi[iab, jab, kab, 2] - phi[ib, jb, kb, 2]
                        Dx = phi[iab, jab, kab, 0] - phi[ia, ja, ka, 0]
                        Dy = phi[iab, jab, kab, 1] - phi[ia, ja, ka, 1]
                        Dz = phi[iab, jab, kab, 2] - phi[ia, ja, ka, 2]
                        AA = Ax * Ax + Ay * Ay + Az * Az; BB = Bx * Bx + By * By + Bz * Bz
                        CC = Cx * Cx + Cy * Cy + Cz * Cz; DD = Dx * Dx + Dy * Dy + Dz * Dz
                        AB = Ax * Bx + Ay * By + Az * Bz; AD = Ax * Dx + Ay * Dy + Az * Dz
                        CB = Cx * Bx + Cy * By + Cz * Bz; CD = Cx * Dx + Cy * Dy + Cz * Dz
                        e4 += (AA * BB - AB * AB) + (AA * DD - AD * AD) + (CC * BB - CB * CB) + (CC * DD - CD * CD)
                        f = 2 * w4
                        dAx = f * (Ax * (BB + DD) - Bx * AB - Dx * AD)
                        dAy = f * (Ay * (BB + DD) - By * AB - Dy * AD)
                        dAz = f * (Az * (BB + DD) - Bz * AB - Dz * AD)
                        dBx = f * (Bx * (AA + CC) - Ax * AB - Cx * CB)
                        dBy = f * (By * (AA + CC) - Ay * AB - Cy * CB)
                        dBz = f * (Bz * (AA + CC) - Az * AB - Cz * CB)
                        dCx = f * (Cx * (BB + DD) - Bx * CB - Dx * CD)
                        dCy = f * (Cy * (BB + DD) - By * CB - Dy * CD)
                        dCz = f * (Cz * (BB + DD) - Bz * CB - Dz * CD)
                        dDx = f * (Dx * (AA + CC) - Ax * AD - Cx * CD)
                        dDy = f * (Dy * (AA + CC) - Ay * AD - Cy * CD)
                        dDz = f * (Dz * (AA + CC) - Az * AD - Cz * CD)
                        Gc[p, 0, i, j, k, 0] = -dAx - dBx; Gc[p, 0, i, j, k, 1] = -dAy - dBy; Gc[p, 0, i, j, k, 2] = -dAz - dBz
                        Gc[p, 1, i, j, k, 0] = dAx - dDx; Gc[p, 1, i, j, k, 1] = dAy - dDy; Gc[p, 1, i, j, k, 2] = dAz - dDz
                        Gc[p, 2, i, j, k, 0] = dBx - dCx; Gc[p, 2, i, j, k, 1] = dBy - dCy; Gc[p, 2, i, j, k, 2] = dBz - dCz
                        Gc[p, 3, i, j, k, 0] = dCx + dDx; Gc[p, 3, i, j, k, 1] = dCy + dDy; Gc[p, 3, i, j, k, 2] = dCz + dDz
                    else:
                        for q4 in range(4):
                            Gc[p, q4, i, j, k, 0] = 0.0; Gc[p, q4, i, j, k, 1] = 0.0; Gc[p, q4, i, j, k, 2] = 0.0
        t2[i] = e2; t4[i] = e4
    return w2 * t2.sum(), w4 * t4.sum()


@nb.njit(parallel=True, cache=True)
def _lps_pass2(Gl, Gc, s, out, off, pa_, pb_):
    N = out.shape[0]
    for i in nb.prange(N):
        for j in range(N):
            for k in range(N):
                for c in range(3):
                    g = 0.0
                    for a in range(3):
                        g -= Gl[a, i, j, k, c]
                        ii = i - s * off[a, 0]; jj = j - s * off[a, 1]; kk = k - s * off[a, 2]
                        if ii >= 0 and jj >= 0 and kk >= 0:
                            g += Gl[a, ii, jj, kk, c]
                    for p in range(3):
                        a = pa_[p]; b = pb_[p]
                        g += Gc[p, 0, i, j, k, c]
                        ii = i - s * off[a, 0]; jj = j - s * off[a, 1]; kk = k - s * off[a, 2]
                        if ii >= 0 and jj >= 0 and kk >= 0:
                            g += Gc[p, 1, ii, jj, kk, c]
                        ii = i - s * off[b, 0]; jj = j - s * off[b, 1]; kk = k - s * off[b, 2]
                        if ii >= 0 and jj >= 0 and kk >= 0:
                            g += Gc[p, 2, ii, jj, kk, c]
                        ii = i - s * (off[a, 0] + off[b, 0]); jj = j - s * (off[a, 1] + off[b, 1])
                        kk = k - s * (off[a, 2] + off[b, 2])
                        if ii >= 0 and jj >= 0 and kk >= 0:
                            g += Gc[p, 3, ii, jj, kk, c]
                    out[i, j, k, c] = g


_OFF = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.int64)
_PA = np.array([0, 0, 1], dtype=np.int64); _PB = np.array([1, 2, 2], dtype=np.int64)   # planes (0,1),(0,2),(1,2)


class LPEnergy:
    """kind='lp' : link/plaquette energy (stride 1); kind='R4': (4 E_s1 - E_s2)/3."""

    def __init__(self, N, kind='lp'):
        self.kind = kind
        self.Gl = np.zeros((3, N, N, N, 3)); self.Gc = np.zeros((3, 4, N, N, N, 3))
        self.g1 = np.zeros((N, N, N, 3)); self.g2 = np.zeros((N, N, N, 3))

    def stride(self, phi, h, s, out):
        if s == 1:
            w2, w4 = C0 * h, C0 / (4 * h)
        else:
            w2, w4 = C0 * h / 4, C0 / (64 * h)
        e2, e4 = _lps_pass1(phi, s, w2, w4, self.Gl, self.Gc, _OFF, _PA, _PB)
        _lps_pass2(self.Gl, self.Gc, s, out, _OFF, _PA, _PB)
        return e2, e4

    def __call__(self, phi, h):
        a2, a4 = self.stride(phi, h, 1, self.g1)
        if self.kind == 'lp':
            return a2 + a4, a2, a4, self.g1
        b2, b4 = self.stride(phi, h, 2, self.g2)
        e2 = (4 * a2 - b2) / 3; e4 = (4 * a4 - b4) / 3
        return e2 + e4, e2, e4, (4 * self.g1 - self.g2) / 3
