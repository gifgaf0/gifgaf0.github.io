"""Method 2: degree = signed count of preimages of a GENERIC w=(w1,w2) in S^3 (both components nonzero),
found by vectorized multi-start Newton in R^3 (no spatial integration)."""
import numpy as np, sys
from fields import local_sign, circle_param, D_circles
from fast_fields import make_fast as make_numeric

def ellipse_pts(name, n=300):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    c, s = np.cos(t), np.sin(t)
    A = np.stack([2*c, s, 0*t], 1)            # x^2/4+y^2=1, z=0
    B = np.stack([0*t, 2*c, s], 1)            # y^2/4+z^2=1, x=0
    C = np.stack([s, 0*t, 2*c], 1)            # z^2/4+x^2=1, y=0
    if name == 'e':
        B = B + np.array([0, 0, 2.5]); C = C + np.array([0, 0, -2.5])
    return [A, B, C]

def tube_starts(curves, radii=(0.003, 0.01, 0.03, 0.1, 0.3), nang=8):
    out = []
    for P in curves:
        T = np.roll(P, -1, 0) - np.roll(P, 1, 0); T /= np.linalg.norm(T, axis=1)[:, None]
        tmp = np.where(np.abs(T[:, [0]]) < 0.9, np.array([[1.0, 0, 0]]), np.array([[0, 1.0, 0]]))
        N1 = np.cross(T, tmp); N1 /= np.linalg.norm(N1, axis=1)[:, None]
        N2 = np.cross(T, N1)
        for r in radii:
            for ang in np.linspace(0, 2*np.pi, nang, endpoint=False):
                out.append(P + r*(np.cos(ang)*N1 + np.sin(ang)*N2))
    return np.concatenate(out, 0)

def newton_roots(ev, w1, w2, A0, starts, iters=70, maxstep=0.3, rkill=12.0):
    P = starts.copy()
    active = np.arange(len(P))
    done = np.zeros(len(P), bool)
    for it in range(iters):
        if len(active) == 0:
            break
        Q = P[active]
        z1v, z2v, d1, d2 = ev(Q[:, 0], Q[:, 1], Q[:, 2], A0)
        g = z1v*w2 - z2v*w1
        mu = z1v*np.conj(w1) + z2v*np.conj(w2)
        dg = d1*w2 - d2*w1
        dmu = d1*np.conj(w1) + d2*np.conj(w2)
        G = np.stack([g.real, g.imag, mu.imag], 1)
        J = np.stack([dg.real, dg.imag, dmu.imag], 1)
        ok = np.isfinite(G).all(1) & np.isfinite(J).all((1, 2))
        Jsafe = np.where(ok[:, None, None], J, np.eye(3))
        det = np.linalg.det(Jsafe)
        ok &= np.abs(det) > 1e-280
        step = np.zeros_like(Q)
        step[ok] = -np.linalg.solve(Jsafe[ok], G[ok][:, :, None])[:, :, 0]
        nrm = np.linalg.norm(step, axis=1)
        fac = np.minimum(1.0, maxstep/np.maximum(nrm, 1e-300))
        Q = Q + step*fac[:, None]
        P[active] = Q
        conv = ok & (nrm < 1e-13)
        dead = (~ok) | (np.linalg.norm(Q, axis=1) > rkill)
        done[active[conv]] = True
        active = active[~(conv | dead)]
    P = P[done | np.isin(np.arange(len(P)), active)]
    z1v, z2v, d1, d2 = ev(P[:, 0], P[:, 1], P[:, 2], A0)
    g = z1v*w2 - z2v*w1
    mu = z1v*np.conj(w1) + z2v*np.conj(w2)
    scale = np.abs(z1v) + np.abs(z2v)
    res = np.sqrt(np.abs(g)**2 + mu.imag**2)/scale
    good = res < 1e-11
    return P[good], mu.real[good]

def dedupe(P, tol=1e-6):
    P = np.asarray(P); keep = []
    while len(P):
        p = P[0]; keep.append(p)
        P = P[np.linalg.norm(P - p, axis=1) > tol]
    return np.array(keep)

def degree_generic(name, w1, w2, A0, L=9.0, h=0.25):
    ev = make_numeric(name)
    g1 = np.arange(-L, L + 1e-9, h) + 0.0137    # offset to avoid symmetric planes
    X, Y, Z = np.meshgrid(g1, g1, g1, indexing='ij')
    grid = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    curves = ellipse_pts(name) + [circle_param(D, np.linspace(0, 2*np.pi, 300, endpoint=False)) for D in D_circles[name]]
    starts = np.concatenate([grid, tube_starts(curves)], 0)
    out = {}
    for label, (u1, u2) in {'+w': (w1, w2), '-w': (-w1, -w2)}.items():
        roots_all = []
        for chunk in np.array_split(starts, max(1, len(starts)//200000)):
            Pc, mur = newton_roots(ev, u1, u2, A0, chunk)
            roots_all.append(Pc[mur > 0])
        R = dedupe(np.concatenate(roots_all, 0)) if sum(len(r) for r in roots_all) else np.zeros((0, 3))
        signs = []
        for p in R:
            z1v, z2v, d1, d2 = ev(p[[0]], p[[1]], p[[2]], A0)
            s, det = local_sign(z1v, z2v, d1, d2)
            signs.append(int(s[0]))
        out[label] = (R, signs)
    return out

if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    names = sys.argv[1].split(',') if len(sys.argv) > 1 else ['c', 'e', 'b', 'f']
    for name in names:
        for A0 in [1.0, 250.0]:
            for ratio in [0.05, 0.4, 3.0]:
                al = np.arctan(ratio)
                w1 = np.sin(al)*np.exp(1j*rng.uniform(0, 2*np.pi))
                w2 = np.cos(al)*np.exp(1j*rng.uniform(0, 2*np.pi))
                out = degree_generic(name, w1, w2, A0)
                msg = []
                for lab, (R, s) in out.items():
                    rmax = np.max(np.linalg.norm(R, axis=1)) if len(R) else 0
                    msg.append(f"{lab}: #pre={len(R)} signs={s} sum={sum(s)} (max|p|={rmax:.2f})")
                print(f"({name}) A0={A0} |w1|/|w2|={ratio} w=({w1:.3f},{w2:.3f}) :: " + " | ".join(msg), flush=True)
