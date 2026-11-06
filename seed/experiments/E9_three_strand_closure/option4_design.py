"""
E9 option 4, design calculation (straight string only; no loop is computed here).

Model of PREREG_option4 §2: the E9 three-strand energy (gl3.py units, kappa = 2, e = 1/sqrt 12, eta = 0.1)
plus a neutral core field sigma with
    |grad sigma|^2 - mu2 |sigma|^2 + (lam/2)|sigma|^4 + beta |sigma|^2 sum_k |psi_k|^2.
Straight composite vortex along z, all three strands psi_k = f(r) e^{i theta}, gauge a(r), sigma = s(r) e^{i(k z - w t)}.
Static functional per unit length (relativistic, fixed w and k):
    T = 2 pi int r dr [ 3(f'^2 + f^2 (1-a)^2/r^2 + 1/2 (f^2-1)^2) - 3 eta f^2 - Vvac + a'^2/(2 e^2 r^2)
                        + s'^2 + (3 beta f^2 - mu2 + k^2 + w^2) s^2 + lam/2 s^4 ]
At w = k = 0 this is the energy. Outputs: T0 (bare string tension), eps0 (lowest m=0 eigenvalue of
-lap + 3 beta f^2 on the bare string), and with sigma: T, I_c = 2 pi int r s^2 dr.
"""
import numpy as np, sys, json
from scipy.optimize import minimize
from scipy.linalg import eigh_tridiagonal
# Run: python3 option4_design.py  -> bare string T0, core size, eps0(beta), and the k = w = 0 sigma scan of PREREG_option4 §1.3

e = 1 / np.sqrt(12.0); eta = 0.1
dr = 0.04; rmax = 24.0
r = np.arange(0, rmax + dr / 2, dr); M = len(r) - 1
rm = 0.5 * (r[1:] + r[:-1])           # midpoints
fv = np.sqrt(1 + eta)
Vvac = 3 * (0.5 * eta ** 2 - eta * (1 + eta))

def unpack(x, with_s):
    f = np.concatenate([[0.0], x[:M - 1], [fv]])
    a = np.concatenate([[0.0], x[M - 1:2 * M - 2], [1.0]])
    s = np.concatenate([x[2 * M - 2:], [0.0]]) if with_s else np.zeros(M + 1)
    return f, a, s

def solve(P, with_s, x0=None):
    beta, mu2, lam, q2 = P
    if x0 is None:
        f0 = fv * np.tanh(r[1:M] / 0.8); a0 = (r[1:M] / 3.0) ** 2 / (1 + (r[1:M] / 3.0) ** 2)
        s0 = 0.8 * np.exp(-r[:M] ** 2 / 2)
        x0 = np.concatenate([f0, a0] + ([s0] if with_s else []))
    W = 2 * np.pi * rm * dr
    def fg(x):
        f, a, s = unpack(x, with_s)
        fp = np.diff(f) / dr; ap = np.diff(a) / dr; sp = np.diff(s) / dr
        fm = 0.5 * (f[1:] + f[:-1]); am = 0.5 * (a[1:] + a[:-1]); sm = 0.5 * (s[1:] + s[:-1])
        dens = (3 * (fp ** 2 + fm ** 2 * (1 - am) ** 2 / rm ** 2 + 0.5 * (fm ** 2 - 1) ** 2) - 3 * eta * fm ** 2 - Vvac
                + ap ** 2 / (2 * e ** 2 * rm ** 2)
                + sp ** 2 + (3 * beta * fm ** 2 - mu2 + q2) * sm ** 2 + 0.5 * lam * sm ** 4)
        E = np.sum(W * dens)
        dfp = W * 6 * fp
        dfm = W * (6 * fm * (1 - am) ** 2 / rm ** 2 + 6 * fm * (fm ** 2 - 1) - 6 * eta * fm + 6 * beta * fm * sm ** 2)
        dap = W * ap / (e ** 2 * rm ** 2)
        dam = W * (-6 * fm ** 2 * (1 - am) / rm ** 2)
        dsp = W * 2 * sp
        dsm = W * (2 * (3 * beta * fm ** 2 - mu2 + q2) * sm + 2 * lam * sm ** 3)
        def node(dp, dm):
            g = np.zeros(M + 1)
            g[:-1] += -dp / dr + 0.5 * dm
            g[1:] += dp / dr + 0.5 * dm
            return g
        gf = node(dfp, dfm); ga = node(dap, dam); gs = node(dsp, dsm)
        grad = [gf[1:M], ga[1:M]] + ([gs[:M]] if with_s else [])
        return E, np.concatenate(grad)
    res = minimize(fg, x0, jac=True, method='L-BFGS-B', options=dict(maxiter=50000, maxfun=100000, gtol=1e-10, ftol=1e-16))
    res.fg = fg
    return res

def eps0(f, beta):
    # lowest eigenvalue of -(1/r)(r s')' + 3 beta f^2 s, m = 0, s'(0)=0, s(rmax)=0; symmetric form on nodes 0..M-1
    n = M
    w = np.empty(n); w[0] = dr ** 2 / 8; w[1:] = r[1:M] * dr   # node volume weights (2 pi dropped)
    rmid = rm[:n]                                               # flux faces
    diag = np.zeros(n); off = np.zeros(n - 1)
    for i in range(n):
        if i > 0: diag[i] += rm[i - 1] / dr
        diag[i] += rm[i] / dr
    off[:] = -rm[:n - 1] / dr
    diag += 3 * beta * f[:n] ** 2 * w
    # generalized problem K s = eps W s -> symmetric W^-1/2 K W^-1/2
    Wi = 1 / np.sqrt(w)
    d = diag * Wi * Wi; o = off * Wi[:-1] * Wi[1:]
    vals = eigh_tridiagonal(d, o, select='i', select_range=(0, 0))[0]
    return vals[0]

if __name__ == '__main__':
    out = {}
    r0 = solve((0, 0, 1, 0), with_s=False)
    f, a, _ = unpack(r0.x, False)
    T0 = r0.fun; out['T0'] = T0; out['bare_converged'] = bool(r0.success)
    # core size: radius where f^2 = 0.5 (1+eta)
    out['r_half_f2'] = float(np.interp(0.5 * (1 + eta), f ** 2, r))
    for beta in (0.5, 1.0):
        out[f'eps0_beta{beta}'] = float(eps0(f, beta))
    print(json.dumps(out, indent=1))
    beta, lam = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0, 1.0
    for mu2 in [float(m) for m in (sys.argv[2:] or ['1.5', '1.7', '1.8'])]:
        rs = solve((beta, mu2, lam, 0.0), with_s=True, x0=np.concatenate([r0.x, 0.6 * np.exp(-r[:M] ** 2 / 2)]))
        f2, a2, s2 = unpack(rs.x, True)
        Ic = 2 * np.pi * np.sum(rm * (0.5 * (s2[1:] + s2[:-1])) ** 2) * dr
        print(json.dumps(dict(beta=beta, mu2=mu2, lam=lam, m2_vac=3 * beta * (1 + eta) - mu2,
                              eps0=float(eps0(f, beta)), T=rs.fun, T0=T0, s0=float(s2[0]), Ic=float(Ic),
                              converged=bool(rs.success), msg=str(rs.message)[:40])))
