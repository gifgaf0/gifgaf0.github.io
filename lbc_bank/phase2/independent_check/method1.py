"""Method 1: degree = signed count of preimages of the regular value w=(e^{i theta},0) in S^3.
Preimages lie on z2^{-1}(0) (union of the explicit D circles) where arg z1 = theta; found by 1D root finding."""
import numpy as np
from scipy.optimize import brentq
from fields import make_numeric, local_sign, circle_param, D_circles

def preimages_on_circles(name, theta, A0, N=40000):
    ev = make_numeric(name)
    pts, signs = [], []
    for D in D_circles[name]:
        t = np.linspace(0, 2*np.pi, N, endpoint=False)
        P = circle_param(D, t)
        z1v, z2v, _, _ = ev(P[:, 0], P[:, 1], P[:, 2], A0)
        assert np.max(np.abs(z2v)) < 1e-12, "z2 not zero on circle?"
        assert np.min(np.abs(z1v)) > 0, "z1 vanishes on z2 zero set"
        phi = z1v*np.exp(-1j*theta)
        g = phi.imag
        for i in range(N):
            j = (i + 1) % N
            if g[i] == 0 or g[i]*g[j] < 0:
                t0, t1 = t[i], (t[j] if j else 2*np.pi)
                def h(tt):
                    PP = circle_param(D, np.array([tt]))
                    v = ev(PP[:, 0], PP[:, 1], PP[:, 2], A0)[0][0]*np.exp(-1j*theta)
                    return v.imag
                tr = brentq(h, t0, t1, xtol=1e-14) if g[i] != 0 else t0
                PP = circle_param(D, np.array([tr]))
                z1r, z2r, d1, d2 = ev(PP[:, 0], PP[:, 1], PP[:, 2], A0)
                if (z1r[0]*np.exp(-1j*theta)).real > 0:   # positive ray only
                    s, det = local_sign(z1r, z2r, d1, d2)
                    pts.append(PP[0]); signs.append(int(s[0]))
    return pts, signs

if __name__ == '__main__':
    for name in ['c', 'e', 'b', 'f']:
        for A0 in [1.0, 250.0]:
            res = []
            for theta in [0.3, 1.7, 2.9, -2.2, 4.4]:
                pts, signs = preimages_on_circles(name, theta, A0)
                res.append((theta, len(pts), signs, sum(signs)))
            print(f"config ({name}) A0={A0}: " + "; ".join(f"th={th}: n={n} signs={s} deg={d}" for th, n, s, d in res))
