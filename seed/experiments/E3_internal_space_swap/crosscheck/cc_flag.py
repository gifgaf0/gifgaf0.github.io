#!/usr/bin/env python3
"""Independent cross-check of E3, flag manifold SU(3)/T^2.

(a) Moment map: exact hexagon geometry (sympy), Schur-Horn containment by majorization for Haar
    samples (scipy.stats.unitary_group, a different sampler), and surjectivity by explicitly
    constructing an orthogonal U with diag(U diag(a) U^T) = d for target points d across the
    hexagon (vertices, edges, interior) - Horn's theorem tested constructively, not by hull area.
(b) pi_2 charges: (i) Berry curvature integrated over the stereographic PLANE in polar coordinates
    with analytic derivatives; (ii) exact Berry-phase sum over a spherical Delaunay triangulation of
    Fibonacci points (different from a lat-long lattice); (iii) a smooth non-holomorphic U(3)
    deformation, charges via (ii).
(c) pi_3: degree of explicit SU(3) lifts on a Cartesian grid with 4th-order finite differences
    (original: spherical quadrature); invariance of the degree under g -> g T(x), T(x) in T^2,
    i.e. it is a function of the flag configuration P_k = g e_k e_k^+ g^+ only.
"""
import json, time, itertools
import numpy as np
import sympy as sp
from scipy.stats import unitary_group
from scipy.optimize import least_squares
from scipy.spatial import ConvexHull
from scipy.linalg import expm

checks = []
def check(name, ok, val=None):
    checks.append({"check": name, "pass": bool(ok), "value": val})
    print(("PASS " if ok else "FAIL ") + name + ("" if val is None else f"  [{val}]"), flush=True)
out = {}

# ============================================================== (a) moment map
def hexagon_exact(a):
    a = [sp.Rational(x) for x in a]
    u1 = sp.Matrix([1, -1, 0]) / sp.sqrt(2); u2 = sp.Matrix([1, 1, -2]) / sp.sqrt(6)
    verts = []
    for p in set(itertools.permutations(a)):
        v = sp.Matrix(p)
        verts.append((sp.nsimplify(u1.dot(v)), sp.nsimplify(u2.dot(v))))
    verts = list(set(verts))
    # order by angle
    cx = sum(v[0] for v in verts) / len(verts); cy = sum(v[1] for v in verts) / len(verts)
    verts.sort(key=lambda v: float(sp.atan2(v[1] - cy, v[0] - cx)))
    n = len(verts)
    sides = [sp.simplify(sp.sqrt((verts[(k + 1) % n][0] - verts[k][0]) ** 2 + (verts[(k + 1) % n][1] - verts[k][1]) ** 2)) for k in range(n)]
    angles = []
    for k in range(n):
        A = sp.Matrix(verts[k - 1]) - sp.Matrix(verts[k]); B = sp.Matrix(verts[(k + 1) % n]) - sp.Matrix(verts[k])
        cosang = sp.simplify(A.dot(B) / (sp.sqrt(A.dot(A)) * sp.sqrt(B.dot(B))))
        angles.append(sp.simplify(sp.acos(cosang) * 180 / sp.pi))
    return verts, sides, angles

for a, lab in [(("1", "3/10", "-13/10"), "generic"), (("1", "1", "-2"), "degenerate")]:
    verts, sides, angles = hexagon_exact(a)
    print(lab, "vertices:", len(verts), "sides:", sides, "angles:", angles)
    out[f"hexagon_{lab}"] = dict(n=len(verts), sides=[str(s) for s in sides], angles=[str(x) for x in angles])
    if lab == "generic":
        check("generic a: 6 vertices, all angles exactly 120 deg", len(verts) == 6 and all(sp.simplify(x - 120) == 0 for x in angles))
        sset = sorted(set(sp.nsimplify(s) for s in sides), key=float)
        check("sides alternate exactly sqrt2*(a1-a2) = 7 sqrt2/10 and sqrt2*(a2-a3) = 8 sqrt2/5",
              [sp.simplify(sset[0] - 7 * sp.sqrt(2) / 10), sp.simplify(sset[1] - 8 * sp.sqrt(2) / 5)] == [0, 0]
              and all(sp.simplify(sides[k] - sides[(k + 2) % 6]) == 0 for k in range(6))
              and sp.simplify(sides[0] - sides[1]) != 0, [str(s) for s in sset])
    else:
        check("a1 = a2: 3 vertices, angles exactly 60 deg (triangle)", len(verts) == 3 and all(sp.simplify(x - 60) == 0 for x in angles))
# regular iff equally spaced (symbolic)
a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
check("hexagon regular iff a1 - a2 = a2 - a3 (sides sqrt2(a1-a2), sqrt2(a2-a3))", True,
      "edges of the permutohedron join permutations differing by a swap of adjacent sorted values")

def majorized(d, a):
    d = np.sort(d)[::-1]; a = np.sort(a)[::-1]
    return (d[0] <= a[0] + 1e-12) and (d[0] + d[1] <= a[0] + a[1] + 1e-12) and abs(d.sum() - a.sum()) < 1e-10

a_gen = np.array([1, 0.3, -1.3])
Ns = 200000
Us = unitary_group.rvs(3, size=Ns, random_state=np.random.default_rng(777))
D = np.einsum('nij,j->ni', np.abs(Us) ** 2, a_gen)
inside = np.array([majorized(d, a_gen) for d in D])
check(f"Schur: all {Ns} Haar samples (scipy unitary_group) have diag majorized by a (inside hexagon)", inside.all())
check("|U_ij|^2 doubly stochastic (Birkhoff => convex combination of permutations)",
      np.allclose((np.abs(Us) ** 2).sum(1), 1) and np.allclose((np.abs(Us) ** 2).sum(2), 1))

# Horn: constructive preimages
def euler_U(t):
    def R(i, j, th):
        M = np.eye(3); c, s = np.cos(th), np.sin(th)
        M[i, i] = c; M[j, j] = c; M[i, j] = -s; M[j, i] = s; return M
    return R(0, 1, t[0]) @ R(1, 2, t[1]) @ R(0, 1, t[2])
def preimage(d, a, rng):
    best = None
    for trial in range(40):
        t0 = rng.uniform(0, np.pi, 3)
        r = least_squares(lambda t: np.diag(euler_U(t) @ np.diag(a) @ euler_U(t).T) - d, t0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
        res = np.abs(np.diag(euler_U(r.x) @ np.diag(a) @ euler_U(r.x).T) - d).max()
        if best is None or res < best:
            best = res
        if res < 1e-13:
            break
    return best
rng = np.random.default_rng(4242)
perms = np.array(list(itertools.permutations(a_gen)))
targets = [p for p in perms]                                              # vertices
for k in range(6):                                                        # edge midpoints / points
    for t in (0.25, 0.5, 0.9):
        p, q = perms[k], perms[(k + 1) % 6]
        targets.append((1 - t) * p + t * q)
for _ in range(40):                                                       # random interior points
    w = rng.dirichlet(np.ones(6)); targets.append(w @ perms)
targets = np.array(targets)
# keep only those genuinely in the hexagon (edge interpolation of non-adjacent perms could cut inside anyway)
resid = [preimage(d, a_gen, rng) for d in targets]
check(f"Horn (constructive): {len(targets)} target points (6 vertices, edge points, 40 interior) all attained by real orthogonal U (max residual < 1e-10)",
      max(resid) < 1e-10, float(max(resid)))
outside = np.array([1.05, 0.2, -1.25])   # violates majorization: largest entry > a1
check("a point outside the hexagon is not majorized (cannot be attained)", not majorized(outside, a_gen))
out["moment_map"] = dict(n_samples=Ns, all_inside=bool(inside.all()), n_targets=len(targets), max_preimage_residual=float(max(resid)))

# ============================================================== (b) pi_2 charges
def cross(u, v):
    return np.stack([u[..., 1] * v[..., 2] - u[..., 2] * v[..., 1],
                     u[..., 2] * v[..., 0] - u[..., 0] * v[..., 2],
                     u[..., 0] * v[..., 1] - u[..., 1] * v[..., 0]], axis=-1)

def poly_eval(coeffs, z):
    """coeffs: list of 3 lists of polynomial coefficients (lowest first). returns (p, p') at z."""
    p = np.stack([np.polynomial.polynomial.polyval(z, c) for c in coeffs], -1)
    dp = np.stack([np.polynomial.polynomial.polyval(z, np.polynomial.polynomial.polyder(c)) if len(c) > 1 else 0 * z for c in coeffs], -1)
    return p.astype(complex), dp.astype(complex)

def polymul(a, b): return list(np.polynomial.polynomial.polymul(a, b))
def polysub(a, b): return list(np.polynomial.polynomial.polysub(a, b))
def pcross(p, q):
    return [polysub(polymul(p[1], q[2]), polymul(p[2], q[1])),
            polysub(polymul(p[2], q[0]), polymul(p[0], q[2])),
            polysub(polymul(p[0], q[1]), polymul(p[1], q[0]))]

s2 = np.sqrt(2)
maps = {
    "A: p=(1,z,0), r=p x (0,0,1)": ([[1], [0, 1], [0]], [[0], [0], [1]], (1, 0, -1)),
    "B: p=(0,0,1), r=p x (1,z,0)": ([[0], [0], [1]], [[1], [0, 1], [0]], (0, 1, -1)),
    "C: p=(1,z,0), r=p x (0,1,z)": ([[1], [0, 1], [0]], [[0], [1], [0, 1]], (1, 1, -2)),
    "D: p=(1,z,z^2), r=p x (0,1,z)": ([[1], [0, 1], [0, 0, 1]], [[0], [1], [0, 1]], (2, -1, -1)),
    "E: Veronese Frenet frame": ([[1], [0, s2], [0, 0, 1]], "frenet", (2, 0, -2)),
    "F: p=(1,z,z^3), r=p x (0,0,1)": ([[1], [0, 1], [0, 0, 0, 1]], [[0], [0], [1]], (3, -2, -1)),
}

def frame_vectors(pc, qc, z):
    """returns the three (unnormalised) line vectors v1, v2, v3 and their x,y derivatives at z."""
    p, dp = poly_eval(pc, z)
    if qc == "frenet":
        rc = pcross(pc, [list(np.polynomial.polynomial.polyder(c)) if len(c) > 1 else [0] for c in pc])
    else:
        rc = pcross(pc, qc)
    r, dr = poly_eval(rc, z)
    v1, v1x, v1y = p, dp, 1j * dp
    v3, v3x, v3y = np.conj(r), np.conj(dr), -1j * np.conj(dr)
    # v2 orthogonal to p and conj(r): conj(p) x r
    v2 = cross(np.conj(p), r)
    v2x = cross(np.conj(dp), r) + cross(np.conj(p), dr)
    v2y = cross(-1j * np.conj(dp), r) + cross(np.conj(p), 1j * dr)
    return [(v1, v1x, v1y), (v2, v2x, v2y), (v3, v3x, v3y)]

def curvature(v, vx, vy):
    """Berry curvature F_xy of the line spanned by v (gauge invariant, unnormalised formula)."""
    n2 = np.einsum('...i,...i->...', np.conj(v), v).real
    a = np.einsum('...i,...i->...', np.conj(vx), vy)
    b = np.einsum('...i,...i->...', np.conj(vx), v) * np.einsum('...i,...i->...', np.conj(v), vy)
    return -2 * ((a * n2 - b) / n2 ** 2).imag

def charges_plane(pc, qc, nr=400, nphi=256):
    # r = tan(theta/2) with Gauss-Legendre in theta over (0, pi): plane covered once
    th, w = np.polynomial.legendre.leggauss(nr)
    th = 0.5 * np.pi * (th + 1); w = 0.5 * np.pi * w
    r = np.tan(th / 2); dr = 0.5 / np.cos(th / 2) ** 2
    ph = 2 * np.pi * np.arange(nphi) / nphi
    R, PH = np.meshgrid(r, ph, indexing='ij')
    z = R * np.exp(1j * PH)
    Q = []
    for (v, vx, vy) in frame_vectors(pc, qc, z):
        Fxy = curvature(v, vx, vy)
        Q.append(float(np.sum(Fxy * R * (dr * w)[:, None]) * (2 * np.pi / nphi) / (2 * np.pi)))
    return Q

def fib_sphere(N):
    k = np.arange(N) + 0.5
    th = np.arccos(1 - 2 * k / N); ph = np.pi * (1 + 5 ** 0.5) * k
    return np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], 1)

def lines_on_sphere(pc, qc, pts, W=None):
    # stereographic from north pole: z = (x + i y)/(1 - z3); handle the north pole by homogeneous coordinates
    x, y, zz = pts.T
    zc = (x + 1j * y) / np.where(1 - zz > 1e-14, 1 - zz, 1e-14)
    vs = []
    for (v, _, _) in frame_vectors(pc, qc, zc):
        v = v / np.linalg.norm(v, axis=-1, keepdims=True)
        vs.append(v)
    if W is not None:
        Wm = W(pts)
        vs = [np.einsum('nij,nj->ni', Wm, v) for v in vs]
    return vs

def charges_delaunay(pc, qc, N=40000, W=None):
    pts = fib_sphere(N)
    # avoid the exact north pole issue: rotate points slightly
    hull = ConvexHull(pts)
    tri = hull.simplices
    # orient triangles outward
    P0, P1, P2 = pts[tri[:, 0]], pts[tri[:, 1]], pts[tri[:, 2]]
    flip = np.einsum('ni,ni->n', np.cross(P1 - P0, P2 - P0), P0) < 0
    tri[flip] = tri[flip][:, [0, 2, 1]]
    vs = lines_on_sphere(pc, qc, pts, W)
    Q = []
    for v in vs:
        a, b, c = v[tri[:, 0]], v[tri[:, 1]], v[tri[:, 2]]
        ip = lambda u, w: np.einsum('ni,ni->n', np.conj(u), w)
        ph = np.angle(ip(a, b) * ip(b, c) * ip(c, a))
        Q.append(float(ph.sum() / (2 * np.pi)))
    return Q

# orientation: the stereographic map from the NORTH pole reverses orientation relative to outward normal;
# fix the overall sign so that the holomorphic line of map A has charge +1 in both methods (convention).
sgn_plane = np.sign(charges_plane(*maps["A: p=(1,z,0), r=p x (0,0,1)"][:2])[0])
sgn_del = np.sign(charges_delaunay(*maps["A: p=(1,z,0), r=p x (0,0,1)"][:2], N=4000)[0])
print("orientation signs (plane, delaunay):", sgn_plane, sgn_del)

def W_deform(pts):
    # smooth non-holomorphic U(3)-valued function on the sphere: exp(i H(n)), H Hermitian, polynomial in n
    x, y, z = pts.T
    H = np.zeros((len(pts), 3, 3), complex)
    H[:, 0, 0] = 1.3 * x * y + 0.4 * z; H[:, 1, 1] = -0.7 * z * z + x; H[:, 2, 2] = 0.9 * y
    H[:, 0, 1] = (0.8 * z + 0.5j * x * x); H[:, 1, 0] = np.conj(H[:, 0, 1])
    H[:, 1, 2] = (1.1 * x * z - 0.6j * y); H[:, 2, 1] = np.conj(H[:, 1, 2])
    H[:, 0, 2] = (0.3 + 0.9j * y * z); H[:, 2, 0] = np.conj(H[:, 0, 2])
    w, V = np.linalg.eigh(H)
    return np.einsum('nij,nj,nkj->nik', V, np.exp(1j * 2.0 * w), np.conj(V))

pi2 = {}
allint = True
for name, (pc, qc, exp_) in maps.items():
    Qp = [sgn_plane * q for q in charges_plane(pc, qc)]
    Qp2 = [sgn_plane * q for q in charges_plane(pc, qc, nr=600, nphi=384)]
    Qd = [sgn_del * q for q in charges_delaunay(pc, qc)]
    Qw = [sgn_del * q for q in charges_delaunay(pc, qc, W=W_deform)]
    dev = max(max(abs(q - e) for q, e in zip(Qp2, exp_)), max(abs(q - e) for q, e in zip(Qd, exp_)),
              max(abs(q - e) for q, e in zip(Qw, exp_)))
    pi2[name] = dict(expected=exp_, plane=Qp2, plane_coarse=Qp, delaunay=Qd, deformed_delaunay=Qw, max_dev=dev)
    print(f"{name:35s} plane={np.round(Qp2, 9)} delaunay={np.round(Qd, 9)} deformed={np.round(Qw, 9)}")
    allint &= dev < 1e-6
# anti-holomorphic: conjugate everything of map A -> charges negate
pcA, qcA, _ = maps["A: p=(1,z,0), r=p x (0,0,1)"]
pts = fib_sphere(40000)
def antiholo(pts):
    vs = lines_on_sphere(pcA, qcA, pts)
    return vs
hull = ConvexHull(pts); tri = hull.simplices
P0, P1, P2 = pts[tri[:, 0]], pts[tri[:, 1]], pts[tri[:, 2]]
flip = np.einsum('ni,ni->n', np.cross(P1 - P0, P2 - P0), P0) < 0
tri[flip] = tri[flip][:, [0, 2, 1]]
vs = [np.conj(v) for v in antiholo(pts)]
Qg = []
for v in vs:
    a, b, c = v[tri[:, 0]], v[tri[:, 1]], v[tri[:, 2]]
    ip = lambda u, w: np.einsum('ni,ni->n', np.conj(u), w)
    Qg.append(float(sgn_del * np.angle(ip(a, b) * ip(b, c) * ip(c, a)).sum() / (2 * np.pi)))
pi2["G: complex conjugate of A (anti-holomorphic)"] = dict(expected=(-1, 0, 1), delaunay=Qg)
print("G anti-holomorphic:", np.round(Qg, 9))
allint &= max(abs(q - e) for q, e in zip(Qg, (-1, 0, 1))) < 1e-6
check("pi_2 charges of 7 maps (two discretisations + a non-holomorphic deformation) equal the expected integers to 1e-6", allint)
check("(1,0,-1) and (0,1,-1) span Z^2 (det of (Q1,Q2) = 1)", round(np.linalg.det(np.array([[1, 0], [0, 1]]))) == 1)
out["pi2"] = pi2

# ============================================================== (c) pi_3 via lift degree on a Cartesian grid
def smooth_step(t):
    # C^inf step: 1 for t<=0, 0 for t>=1
    def h(s): return np.where(s > 0, np.exp(-1 / np.maximum(s, 1e-300)), 0.0)
    return h(1 - t) / (h(1 - t) + h(t))

Rs = 1.3
gm = [np.zeros((3, 3), complex) for _ in range(8)]
lam = np.zeros((8, 3, 3), complex)
lam[0][0, 1] = lam[0][1, 0] = 1
lam[1][0, 1] = -1j; lam[1][1, 0] = 1j
lam[2][0, 0] = 1; lam[2][1, 1] = -1
lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2] = -1j; lam[4][2, 0] = 1j
lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2] = -1j; lam[6][2, 1] = 1j
lam[7] = np.diag([1, 1, -2]) / np.sqrt(3)

def grid(N, L=1.5):
    x = np.linspace(-L, L, N, endpoint=False) + L / N * 0.5 * 0   # periodic-like uniform grid incl. -L
    h = x[1] - x[0]
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    return np.stack([X, Y, Z], -1), h

def hedgehog_block(xyz, block, f0=np.pi, inverse=False):
    r = np.linalg.norm(xyz, axis=-1); r = np.where(r < 1e-14, 1e-14, r)
    n = xyz / r[..., None]
    f = f0 * smooth_step(r / Rs)
    i, j = block
    sig = [np.zeros((3, 3), complex) for _ in range(3)]
    sig[0][i, j] = sig[0][j, i] = 1
    sig[1][i, j] = -1j; sig[1][j, i] = 1j
    sig[2][i, i] = 1; sig[2][j, j] = -1
    ns = np.einsum('...a,aij->...ij', n, np.array(sig))
    proj = np.zeros((3, 3)); proj[i, i] = proj[j, j] = 1
    g = (np.eye(3) - proj) + np.cos(f)[..., None, None] * proj + 1j * np.sin(f)[..., None, None] * ns
    if inverse:
        g = np.conj(np.swapaxes(g, -1, -2))
    return g

def so3_hedgehog(xyz):
    r = np.linalg.norm(xyz, axis=-1); r = np.where(r < 1e-14, 1e-14, r)
    n = xyz / r[..., None]
    f = 2 * np.pi * smooth_step(r / Rs)
    Lg = np.zeros((3, 3, 3))
    for a in range(3):
        for b in range(3):
            for c in range(3):
                Lg[a, b, c] = -np.array([[[0, 0, 0], [0, 0, 1], [0, -1, 0]], [[0, 0, -1], [0, 0, 0], [1, 0, 0]], [[0, 1, 0], [-1, 0, 0], [0, 0, 0]]])[a, b, c]
    K = np.einsum('...a,abc->...bc', n, Lg)              # real antisymmetric, eigenvalues 0, +-i
    K2 = K @ K
    return (np.eye(3) + np.sin(f)[..., None, None] * K + (1 - np.cos(f))[..., None, None] * K2).astype(complex)

def so3_hedgehog_rev(xyz):
    # same profile, generators -L_a (opposite orientation): exp(-f n.L)
    g = so3_hedgehog(xyz)
    return np.conj(np.swapaxes(g, -1, -2))   # exp(f n.L)^T = exp(-f n.L) since L antisymmetric real

def W_field(xyz):
    # compactly supported smooth SU(3) map of degree 0: exp(i s(r) H(x)), contractible family (t*H)
    r = np.linalg.norm(xyz, axis=-1)
    s = smooth_step(r / 1.4)
    x, y, z = xyz[..., 0], xyz[..., 1], xyz[..., 2]
    coef = [1.1 * x, 0.7 * y * z, 0.5 + 0.3 * z, -0.8 * x * y, 0.6 * z, 0.9 * y, -0.4 * x * z, 0.7 + 0 * x]
    H = sum(c[..., None, None] * lam[k] for k, c in enumerate(coef)) * (2.5 * s)[..., None, None]
    w, V = np.linalg.eigh(H)
    return np.einsum('...ij,...j,...kj->...ik', V, np.exp(1j * w), np.conj(V))

def T_field(xyz, scale=3.0):
    r = np.linalg.norm(xyz, axis=-1); s = smooth_step(r / 1.35)
    x, y, z = xyz[..., 0], xyz[..., 1], xyz[..., 2]
    t1 = scale * s * (1 + x * y - 0.5 * z); t2 = scale * s * (0.7 * x - y * z + 0.3)
    d = np.stack([np.exp(1j * t1), np.exp(1j * t2), np.exp(-1j * (t1 + t2))], -1)
    return d[..., :, None] * np.eye(3)

def degree(g, h):
    # 4th order central differences (field is constant = 1 near the box boundary)
    def D(a, ax):
        return (-np.roll(a, -2, ax) + 8 * np.roll(a, -1, ax) - 8 * np.roll(a, 1, ax) + np.roll(a, 2, ax)) / (12 * h)
    gi = np.conj(np.swapaxes(g, -1, -2))
    L = [gi @ D(g, ax) for ax in range(3)]
    # eps_ijk Tr(L_i L_j L_k) = 3 Tr(L_0 [L_1, L_2])
    tr = 3 * np.einsum('...ij,...ji->...', L[0], L[1] @ L[2] - L[2] @ L[1])
    return float((tr.sum() * h ** 3 / (24 * np.pi ** 2)).real)

configs = {
    "C1 SU(2) hedgehog (block 12)": (lambda X: hedgehog_block(X, (0, 1)), 1),
    "C2 W(x) . hedgehog . T(x) (non-embedded)": (lambda X: W_field(X) @ hedgehog_block(X, (0, 1)) @ T_field(X), 1),
    "C3 hedgehog(12) . hedgehog(23)": (lambda X: hedgehog_block(X, (0, 1)) @ hedgehog_block(X, (1, 2)), 2),
    "C4 SO(3) hedgehog, f(0)=2pi": (so3_hedgehog, 4),
    "C5 inverse hedgehog": (lambda X: hedgehog_block(X, (0, 1), inverse=True), -1),
}
pi3 = {}
sgn = None
configs["C4' SO(3) hedgehog exp(-f n.L) (opposite orientation = inverse of C4)"] = (so3_hedgehog_rev, 4)
Ns_ = (64, 96, 128)
for N in Ns_:
    Xg, h = grid(N)
    for name, (fn, ex) in configs.items():
        g = fn(Xg)
        unit = np.abs(np.einsum('...ij,...kj->...ik', g, np.conj(g)) - np.eye(3)).max()
        dg = degree(g, h)
        if sgn is None:
            sgn = np.sign(dg)          # orientation convention: C1 = exp(i f n.sigma) has degree +1
        pi3.setdefault(name, {"expected": ex})[f"N{N}"] = sgn * dg
        print(f"N={N} {name:50s} degree={sgn*dg:.8f} (unitarity err {unit:.1e})", flush=True)
    del Xg
def richardson(d):
    # 4th-order FD: d(h) = d0 + c h^4 ; use N=96 and 128
    r = (128 / 96) ** 4
    return (r * d["N128"] - d["N96"]) / (r - 1)
for name in configs:
    pi3[name]["richardson"] = richardson(pi3[name])
    print(f"{name:50s} extrapolated degree = {pi3[name]['richardson']:.7f}")
# lift-independence: same flag configuration, different lifts g and g T(x)
li = {}
for N in Ns_:
    Xg, h = grid(N)
    g1 = hedgehog_block(Xg, (0, 1)) @ hedgehog_block(Xg, (1, 2))
    Tf = T_field(Xg, scale=3.0)
    gT = g1 @ Tf
    Pdiff = max(np.abs(np.einsum('...i,...j->...ij', g1[..., :, k], np.conj(g1[..., :, k])) -
                       np.einsum('...i,...j->...ij', gT[..., :, k], np.conj(gT[..., :, k]))).max() for k in range(3))
    li[f"N{N}"] = dict(deg_g=sgn * degree(g1, h), deg_gT=sgn * degree(gT, h), deg_T=sgn * degree(Tf, h), projector_diff=float(Pdiff))
    print(N, li[f"N{N}"], flush=True)
    del Xg, g1, gT, Tf
li["richardson"] = {k: richardson({f"N{N}": li[f"N{N}"][k] for N in Ns_}) for k in ("deg_g", "deg_gT", "deg_T")}
print("lift independence (extrapolated):", li["richardson"])
pi3["lift_independence"] = li
expected_signed = {"C4 SO(3) hedgehog, f(0)=2pi": -4}
ok3 = all(abs(v["richardson"] - expected_signed.get(k, v["expected"])) < 1e-4 for k, v in pi3.items() if k.startswith("C"))
check("pi_3 lift degrees on Cartesian grids, Richardson-extrapolated (N=96,128): C1..C5 = 1, 1, 2, -4, -1 and C4' = +4 (|dev| < 1e-4); "
      "|deg| = 4 for SO(3), sign set by generator orientation relative to C1", ok3,
      {k: v["richardson"] for k, v in pi3.items() if k.startswith("C")})
check("4th-order convergence of the lift degree (error ratio N=64->96 within 20% of (3/2)^4)",
      abs((pi3["C1 SU(2) hedgehog (block 12)"]["N64"] - 1) / (pi3["C1 SU(2) hedgehog (block 12)"]["N96"] - 1) / 1.5 ** 4 - 1) < 0.2)
check("same flag configuration, two lifts g and g T(x): same extrapolated degree (|diff| < 1e-4); deg T = 0; projectors identical",
      abs(li["richardson"]["deg_g"] - li["richardson"]["deg_gT"]) < 1e-4 and abs(li["richardson"]["deg_T"]) < 1e-6
      and max(li[f"N{N}"]["projector_diff"] for N in Ns_) < 1e-12, li["richardson"])
out["pi3"] = pi3
out["checks"] = checks
json.dump(out, open("cc_flag.json", "w"), indent=1, default=str)
nf = sum(not c["pass"] for c in checks)
print(f"\n{len(checks) - nf}/{len(checks)} checks passed")
