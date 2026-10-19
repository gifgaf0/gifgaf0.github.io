#!/usr/bin/env python3
"""Independent check of the linear stability of the embedded B=1 hedgehog inside G2.

Own implementation:
  * second variation of E[U0 exp(eps phi)] written in structure-constant (component) form in my own
    B-orthonormal g2 basis (cc_g2.py), pointwise kernel K(x) acting on v = (phi^A, d_i phi^A);
  * Ritz basis: cubic B-splines on sinh-spaced knots (Dirichlet at r = R, free at r = 0) x real
    harmonic polynomials l <= LMAX x internal block basis; Lebedev angular quadrature;
  * quadratic form validated against central finite differences of the full nonlinear energy
    (dexp via eigen-decomposition of ad), for random localised fields in each block;
  * pointwise SU(2)_short invariance => blocks (3,1), (1,3), (2,4) decouple (checked pointwise).
Normalisation: Q(phi) = eps^2 coefficient of E (units F/e), metric S = int |phi|^2 (B-norm), x = eFr,
the same normalisation as the original report (so (1,3) lowest = (1/32)(pi/R)^2).
Usage: python3 cc_stability.py [quick]
"""
import sys, json, time, itertools
import numpy as np
from scipy.integrate import lebedev_rule
from scipy.interpolate import BSpline, CubicHermiteSpline
from scipy.linalg import eigh, expm
import sympy as sp

QUICK = len(sys.argv) > 1 and sys.argv[1] == "quick"
checks = []
def check(name, ok, val=None):
    checks.append({"check": name, "pass": bool(ok), "value": val})
    print(("PASS " if ok else "FAIL ") + name + ("" if val is None else f"  [{val}]"), flush=True)

gb = np.load("cc_g2_basis.npz")
Bc = gb["basis_c"]; f0 = gb["f"]; G7 = gb["G"]; SU3 = gb["SU3"]
f = np.einsum('ai,bj,ck,ijk->abc', Bc, Bc, Bc, f0)       # structure constants in adapted basis
blocks = {"long (3,1)": list(range(0, 3)), "short (1,3)": list(range(3, 6)), "(2,4)": list(range(6, 14))}
# kaon directions: su(3) intersect (2,4)
T_ad = np.einsum('ab,bij->aij', Bc, G7)
su3c = np.array([[-np.trace(X @ T) for T in T_ad] for X in SU3])   # 8 x 14 components
P24 = np.zeros((14, 14)); P24[6:, 6:] = np.eye(8)
Msu3 = su3c.T @ np.linalg.pinv(su3c.T)                              # projector onto su(3)
w_, V_ = np.linalg.eigh(P24 @ Msu3 @ P24)
kaon = V_[:, w_ > 0.5].T                                            # 4 x 14 orthonormal
check("su(3) cap (2,4) is 4-dimensional (kaon directions)", kaon.shape[0] == 4, int(kaon.shape[0]))

prof_npz = np.load("cc_profile.npz")
spl = CubicHermiteSpline(prof_npz["x"], prof_npz["F"], prof_npz["P"])
Cc, Xmax = float(prof_npz["C"]), float(prof_npz["Xmax"])
x0 = prof_npz["x"][0]; Fp0 = prof_npz["P"][0]
def prof(r):
    r = np.asarray(r, float)
    F = np.where(r < x0, np.pi + Fp0 * r, 0.0); P = np.where(r < x0, Fp0, 0.0)
    m = (r >= x0) & (r <= Xmax)
    F = np.where(m, spl(np.clip(r, x0, Xmax)), F); P = np.where(m, spl(np.clip(r, x0, Xmax), 1), P)
    big = r > Xmax
    F = np.where(big, Cc / np.maximum(r, 1) ** 2 - Cc ** 3 / (21 * np.maximum(r, 1) ** 6), F)
    P = np.where(big, -2 * Cc / np.maximum(r, 1) ** 3 + 6 * Cc ** 3 / (21 * np.maximum(r, 1) ** 7), P)
    return F, P

sig = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], complex)
def currents(xyz):
    """l_i components (N,3,14) in adapted basis; only long components non-zero."""
    r = np.linalg.norm(xyz, axis=1); n = xyz / r[:, None]
    F, P = prof(r); sF, cF = np.sin(F), np.cos(F)
    ns = np.einsum('na,aij->nij', n, sig)
    U = cF[:, None, None] * np.eye(2) - 1j * sF[:, None, None] * ns
    Ud = np.conj(np.transpose(U, (0, 2, 1)))
    t = -0.5j * sig
    l = np.zeros((len(r), 3, 14))
    for i in range(3):
        dn = (np.eye(3)[i][None, :] - n[:, i:i + 1] * n) / r[:, None]
        dU = (-sF * P * n[:, i])[:, None, None] * np.eye(2) - 1j * (cF * P * n[:, i])[:, None, None] * ns \
             - 1j * sF[:, None, None] * np.einsum('na,aij->nij', dn, sig)
        L = Ud @ dU
        for a in range(3):
            l[:, i, a] = (-2 * np.einsum('ij,nji->n', t[a], L)).real
    return l, F, n, r

def adm(vec):  # (..., 14) -> (..., 14, 14) matrix of ad: (ad_X)_{cb} = f_abc X^a
    return np.einsum('...a,abc->...cb', vec, f)
def Fm(vec):   # (F(h))_{ab} = f_abc h^c ; <h,[X,Y]> = X^T F(h) Y
    return np.einsum('...c,abc->...ab', vec, f)

def kernel(xyz, E):
    """pointwise quadratic kernel K (N, 4b, 4b) for fields phi = sum_A phi^A E_A (E: b x 14 rows)."""
    l, F, n, r = currents(xyz)
    N = len(r); b = E.shape[0]
    S0 = np.zeros((14, 4 * b)); S0[:, :b] = E.T
    S = [np.zeros((14, 4 * b)) for _ in range(3)]
    for i in range(3):
        S[i][:, b * (i + 1):b * (i + 2)] = E.T
    A = adm(l)                                       # (N,3,14,14)
    D = [S[i][None] + A[:, i] @ S0[None] for i in range(3)]   # (N,14,4b)
    K = np.zeros((N, 4 * b, 4 * b))
    tr = lambda M: np.swapaxes(M, -1, -2)
    for i in range(3):
        K += tr(D[i]) @ D[i] / 32
        Fl = Fm(l[:, i])                             # (N,14,14)
        K += tr(D[i]) @ (Fl @ S0) / 32
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            G1 = A[:, i] @ D[j] - A[:, j] @ D[i]        # (N,14,4b)
            K += tr(G1) @ G1 / 64
            g0 = np.einsum('abc,na,nb->nc', f, l[:, i], l[:, j], optimize=True)
            h1 = np.einsum('abc,na,nb->nc', f, g0, l[:, i], optimize=True)        # [g0, l_i]
            h2 = np.einsum('abc,na,nb->nc', f, l[:, j], g0, optimize=True)        # [l_j, g0]
            T = tr(D[i]) @ Fm(g0) @ D[j]
            T += 0.5 * tr(D[j]) @ (Fm(h1) @ S0)
            T += 0.5 * tr(D[i]) @ (Fm(h2) @ S0)
            K += 2 * T / 64
    return 0.5 * (K + np.transpose(K, (0, 2, 1)))

# ---------------------------------------------------------------- pointwise block decoupling
rng = np.random.default_rng(99)
pts = rng.normal(size=(50, 3)) * 1.5
Kfull = kernel(pts, np.eye(14))
idx = {k: v for k, v in blocks.items()}
def slots(cols): return [s * 14 + c for s in range(4) for c in cols]
offmax = 0
for (k1, c1), (k2, c2) in itertools.combinations(blocks.items(), 2):
    offmax = max(offmax, np.abs(Kfull[:, slots(c1)][:, :, slots(c2)]).max())
check("pointwise kernel block-diagonal between (3,1), (1,3), (2,4) (SU(2)_short invariance)", offmax < 1e-12, float(offmax))

# ---------------------------------------------------------------- finite-difference validation
def energy_full(phi_fn, eps, nr=70, leb=29, Rmax=12.0):
    """E[U0 exp(eps phi)] - E[U0] over a ball of radius Rmax (phi localised inside)."""
    s, w = np.polynomial.legendre.leggauss(nr); r = 0.5 * Rmax * (s + 1); wr = 0.5 * Rmax * w
    nodes, wl = lebedev_rule(leb); nodes = nodes.T
    tot = 0.0
    for q in range(nr):
        xyz = r[q] * nodes
        l, F, n, rr = currents(xyz)
        ph, dph = phi_fn(xyz)                        # (N,14), (N,3,14)
        X = eps * ph
        adX = adm(X)                                 # (N,14,14) real antisymmetric
        AdInv = expm(-adX)
        # e^{-X} d e^{X} = g(ad_X) dX with g(z) = (1 - e^{-z})/z
        w2, V = np.linalg.eig(adX)
        gz = np.where(np.abs(w2) < 1e-12, 1.0 + 0j, (1 - np.exp(-w2)) / np.where(np.abs(w2) < 1e-12, 1, w2))
        gmat = np.einsum('nij,nj,njk->nik', V, gz, np.linalg.inv(V)).real
        L = np.einsum('nab,nib->nia', AdInv, l) + np.einsum('nab,nib->nia', gmat, eps * dph)
        cm = np.einsum('abc,nia,njb->nijc', f, L, L)
        e = np.einsum('nia,nia->n', L, L) / 32 + np.einsum('nijc,nijc->n', cm, cm) / 64
        tot += wr[q] * r[q] ** 2 * (wl @ e)
    return tot

def quad_form(phi_fn, nr=70, leb=29, Rmax=12.0, whole_space=False):
    s, w = np.polynomial.legendre.leggauss(nr); r = 0.5 * Rmax * (s + 1); wr = 0.5 * Rmax * w
    if whole_space:                                   # x = c t/(1-t), t in (0,1): all of R^3
        t = 0.5 * (s + 1); c = 2.0
        r = c * t / (1 - t); wr = 0.5 * w * c / (1 - t) ** 2
    nodes, wl = lebedev_rule(leb); nodes = nodes.T
    tot = 0.0
    for q in range(nr):
        xyz = r[q] * nodes
        K = kernel(xyz, np.eye(14))
        ph, dph = phi_fn(xyz)
        v = np.concatenate([ph, dph[:, 0], dph[:, 1], dph[:, 2]], axis=1)
        tot += wr[q] * r[q] ** 2 * (wl @ np.einsum('ni,nij,nj->n', v, K, v))
    return tot

def random_field(cols, seed):
    g = np.random.default_rng(seed)
    cen = g.normal(size=(3, 3)) * 0.8; wid = g.uniform(0.8, 1.6, 3); amp = g.normal(size=(3, 14))
    mask = np.zeros(14); mask[cols] = 1; amp *= mask
    lin = g.normal(size=(3, 3, 14)) * mask
    def fn(xyz):
        ph = np.zeros((len(xyz), 14)); dph = np.zeros((len(xyz), 3, 14))
        for k in range(3):
            d = xyz - cen[k]; gs = np.exp(-np.sum(d ** 2, 1) / wid[k] ** 2)
            pol = amp[k][None, :] + np.einsum('ni,ia->na', d, lin[k])        # (N,14)
            ph += gs[:, None] * pol
            dph += (-2 * d / wid[k] ** 2)[:, :, None] * (gs[:, None] * pol)[:, None, :] + gs[:, None, None] * lin[k][None]
        return ph, dph
    return fn

fd = {}
for name, cols in blocks.items():
    fn = random_field(cols, 7 + len(name))
    Q = quad_form(fn)
    E0 = energy_full(fn, 0.0)
    hs = [4e-3, 2e-3]
    d2 = []
    for h in hs:
        d2.append((energy_full(fn, h) - 2 * E0 + energy_full(fn, -h)) / h ** 2)
    rich = (4 * d2[1] - d2[0]) / 3
    rel = abs(rich / 2 - Q) / abs(Q)
    fd[name] = dict(Q=Q, fd_half_richardson=rich / 2, rel=rel)
    check(f"quadratic form = (1/2) d^2E/deps^2 by finite differences, block {name} (rel < 1e-6)", rel < 1e-6, (Q, rich / 2, rel))

# zero-mode test: iso-rotation phi = M-like: U0 -> exp(-eps T) U0 exp(eps T) = U0 exp(eps (Ad(U0^-1)T - T))
def zero_mode(Tvec):
    def fn(xyz):
        l, F, n, r = currents(xyz)
        # U0 = exp(X), X = 2F n.T^L; Ad(U0^{-1}) = expm(-ad X)
        Lc = np.eye(14)[:3]
        Xc = 2 * F[:, None] * (n @ Lc)
        Ainv = expm(-adm(Xc))
        ph = np.einsum('nab,b->na', Ainv, Tvec) - Tvec[None]
        # derivative: d_i(Ad(U0^{-1}) T) = -[l_i, Ad(U0^{-1}) T]
        AT = ph + Tvec[None]
        dph = -np.einsum('abc,nia,nb->nic', f, l, AT)
        return ph, dph
    return fn
zq = {}
for name, vec in [("iso-rotation (long)", np.eye(14)[0]), ("G2 rotation (2,4)", np.eye(14)[9]),
                  ("kaon rotation", kaon[1])]:
    q = quad_form(zero_mode(vec), nr=160, whole_space=True)
    qb = {R: quad_form(zero_mode(vec), nr=120, Rmax=R) for R in (30.0, 60.0)}
    zq[name] = q
    zq[name + " [ball R=30, R=60]"] = [qb[30.0], qb[60.0]]
    print(name, "whole space Q =", q, " ball R=30, 60:", qb[30.0], qb[60.0], " ratio", qb[30.0] / qb[60.0], flush=True)
check("exact rotational zero modes give Q ~ 0 over all space (|Q| < 1e-7); on a ball the defect is a -1/R^3 surface term",
      all(abs(v) < 1e-7 for k, v in zq.items() if "ball" not in k), {k: v for k, v in zq.items()})

# ---------------------------------------------------------------- Ritz analysis
def harmonics(lmax):
    x, y, z = sp.symbols('x y z')
    polys = []
    for l in range(lmax + 1):
        mons = [x ** a * y ** b * z ** (l - a - b) for a in range(l + 1) for b in range(l + 1 - a)]
        cs = sp.symbols(f'c0:{len(mons)}')
        P = sum(c * m for c, m in zip(cs, mons))
        lap = sp.expand(sp.diff(P, x, 2) + sp.diff(P, y, 2) + sp.diff(P, z, 2))
        eqs = sp.Poly(lap, x, y, z).coeffs() if lap != 0 else []
        sol = sp.linsolve(eqs, cs) if eqs else [cs]
        sol = list(sol)[0]
        free = sorted(set().union(*[s.free_symbols for s in sol]) & set(cs), key=str)
        for fsym in free:
            Pl = sp.expand(P.subs({c: v for c, v in zip(cs, sol)}).subs({g: (1 if g == fsym else 0) for g in free}))
            polys.append((l, Pl))
    funcs = []
    for l, Pl in polys:
        fP = sp.lambdify((x, y, z), Pl, 'numpy')
        fg = [sp.lambdify((x, y, z), sp.diff(Pl, v), 'numpy') for v in (x, y, z)]
        funcs.append((l, fP, fg))
    return funcs

def ang_basis(lmax, nodes, wl):
    funcs = harmonics(lmax)
    Np = nodes.shape[0]
    Y = np.zeros((len(funcs), Np)); Gr = np.zeros((len(funcs), Np, 3))
    for k, (l, fP, fg) in enumerate(funcs):
        P = np.broadcast_to(fP(*nodes.T), (Np,)).astype(float)
        g = np.stack([np.broadcast_to(fgi(*nodes.T), (Np,)).astype(float) for fgi in fg], 1)
        Y[k] = P; Gr[k] = g - l * P[:, None] * nodes        # surface gradient of P(x)/|x|^l at |x|=1
    # orthonormalise within each l (Lebedev exact for these degrees)
    ls = np.array([l for l, _, _ in funcs])
    for l in range(lmax + 1):
        ii = np.where(ls == l)[0]
        Gm = (Y[ii] * wl) @ Y[ii].T
        w, V = np.linalg.eigh(Gm); C = V @ np.diag(w ** -0.5) @ V.T
        Y[ii] = C @ Y[ii]; Gr[ii] = np.einsum('ab,bpi->api', C, Gr[ii])
    Gram = (Y * wl) @ Y.T
    assert np.allclose(Gram, np.eye(len(funcs)), atol=1e-11), np.abs(Gram - np.eye(len(funcs))).max()
    return Y, Gr, ls

def bspline_basis(R, nel, a=3.0, k=3):
    t = np.linspace(0, 1, nel + 1)
    br = R * np.sinh(a * t) / np.sinh(a)
    knots = np.concatenate([[0] * k, br, [R] * k])
    nb = len(knots) - k - 1
    return knots, nb, br

def ritz(E, R, nel, lmax=3, leb=23, ngl=6, nev=16):
    t0 = time.time()
    b = E.shape[0]
    knots, nb, br = bspline_basis(R, nel)
    keep = list(range(nb - 1))                               # Dirichlet at r = R
    nodes, wl = lebedev_rule(leb); nodes = nodes.T
    Y, Gr, ls = ang_basis(lmax, nodes, wl)
    nY = Y.shape[0]; Na = nY * b
    # angular-internal vectors: alpha0[p, slot, (m,A)] multiplies h; alpha_c multiplies h/r; alpha_b multiplies h'
    Np = nodes.shape[0]
    a0 = np.zeros((Np, 4 * b, nY, b)); ab = np.zeros((Np, 4 * b, nY, b)); ac = np.zeros((Np, 4 * b, nY, b))
    for A in range(b):
        a0[:, A, :, A] = Y.T
        for i in range(3):
            ab[:, b * (i + 1) + A, :, A] = (nodes[:, i][:, None] * Y.T)
            ac[:, b * (i + 1) + A, :, A] = Gr[:, :, i].T
    a0 = a0.reshape(Np, 4 * b, Na); ab = ab.reshape(Np, 4 * b, Na); ac = ac.reshape(Np, 4 * b, Na)
    s, w = np.polynomial.legendre.leggauss(ngl)
    bsp = [BSpline(knots, np.eye(nb)[kk], 3, extrapolate=False) for kk in range(nb)]
    dbsp = [b_.derivative() for b_ in bsp]
    H = np.zeros((nb, Na, nb, Na)); Sm = np.zeros((nb, nb))
    for e in range(nel):
        lo, hi = br[e], br[e + 1]
        rq = lo + 0.5 * (hi - lo) * (s + 1); wq = 0.5 * (hi - lo) * w
        for q in range(ngl):
            r = rq[q]
            K = kernel(r * nodes, E)                           # (Np,4b,4b)
            al = np.concatenate([a0 + ac / r, ab], axis=2)     # (Np,4b,2Na)
            KA = np.matmul(K, al)                              # (Np,4b,2Na)
            X = (al * wl[:, None, None]).reshape(-1, al.shape[2]).T @ KA.reshape(-1, al.shape[2])   # (2Na,2Na), BLAS
            # spline values
            hv = np.array([np.nan_to_num(b_(r)) for b_ in bsp]); hd = np.array([np.nan_to_num(d_(r)) for d_ in dbsp])
            nz = np.where((np.abs(hv) > 0) | (np.abs(hd) > 0))[0]
            cw = wq[q] * r ** 2
            for k1 in nz:
                for k2 in nz:
                    H[k1, :, k2, :] += cw * (hv[k1] * hv[k2] * X[:Na, :Na] + hv[k1] * hd[k2] * X[:Na, Na:]
                                             + hd[k1] * hv[k2] * X[Na:, :Na] + hd[k1] * hd[k2] * X[Na:, Na:])
                    Sm[k1, k2] += cw * hv[k1] * hv[k2]
    H = H[keep][:, :, keep].reshape(len(keep) * Na, len(keep) * Na)
    Sfull = np.kron(Sm[np.ix_(keep, keep)], np.eye(Na))
    H = 0.5 * (H + H.T)
    ev = eigh(H, Sfull, eigvals_only=True, subset_by_index=[0, nev - 1])
    return ev, time.time() - t0

runs = {}
if QUICK:
    plan = [("(2,4)", np.eye(14)[6:], 20.0, 12)]
else:
    plan = [("long (3,1)", np.eye(14)[0:3], 20.0, 30), ("long (3,1)", np.eye(14)[0:3], 20.0, 60),
            ("long (3,1)", np.eye(14)[0:3], 40.0, 40),
            ("short (1,3)", np.eye(14)[3:6], 20.0, 30), ("short (1,3)", np.eye(14)[3:6], 40.0, 40),
            ("kaon", kaon, 20.0, 30), ("kaon", kaon, 20.0, 60), ("kaon", kaon, 40.0, 40),
            ("(2,4)", np.eye(14)[6:], 20.0, 30), ("(2,4)", np.eye(14)[6:], 40.0, 40),
            ("long (3,1) lmax=4", np.eye(14)[0:3], 20.0, 30), ("(2,4) lmax=4", np.eye(14)[6:], 20.0, 24)]
for name, E, R, nel in plan:
    lm = 4 if "lmax=4" in name else 3
    ev, dt = ritz(E, R, nel, lmax=lm, leb=(29 if lm == 4 else 23), nev=(18 if name.startswith("(2,4)") else 12))
    runs[f"{name} R={R:g} nel={nel}"] = ev.tolist()
    print(f"{name:12s} R={R:4.0f} nel={nel:3d}  lowest: {np.array2string(ev[:10], precision=4)}  ({dt:.0f}s)", flush=True)
    json.dump({"checks": checks, "fd": fd, "zero_modes": zq, "ritz": runs},
              open("cc_stability.json" if not QUICK else "cc_stability_quick.json", "w"), indent=1)
minev = min(min(v) for v in runs.values())
check("no negative Ritz eigenvalue in any block / box / mesh (min > -1e-8)", minev > -1e-8, float(minev))
if not QUICK:
    s1 = runs["short (1,3) R=20 nel=30"][0]
    check("(1,3) lowest = (1/32)(pi/R)^2 at R=20 (free massless field, rel < 1e-3)", abs(s1 / ((np.pi / 20) ** 2 / 32) - 1) < 1e-3, (s1, (np.pi / 20) ** 2 / 32))
    k24 = np.array(runs["(2,4) R=40 nel=40"][:16]); kk = np.repeat(np.array(runs["kaon R=40 nel=40"][:8]), 2)
    check("(2,4) spectrum = kaon spectrum doubled (first 16, rel < 1e-8)", np.abs(k24 - kk).max() / kk.max() < 1e-8, float(np.abs(k24 - kk).max()))
json.dump({"checks": checks, "fd": fd, "zero_modes": zq, "ritz": runs},
          open("cc_stability.json" if not QUICK else "cc_stability_quick.json", "w"), indent=1)
nf = sum(not c["pass"] for c in checks)
print(f"\n{len(checks) - nf}/{len(checks)} checks passed")
