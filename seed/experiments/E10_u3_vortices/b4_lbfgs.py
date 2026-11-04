"""
E10 Route B, B4: plain (unbounded) L-BFGS for the 1e6-variable lattice problems.  Label: Exploration.
scipy's L-BFGS-B spends ~0.6 s per iteration in its bound-constrained bookkeeping at n ~ 1.1e6 (more than the
energy evaluation itself); there are no bounds here, so the standard two-loop recursion is used instead
(Nocedal & Wright Alg. 7.4/7.5), memory m, initial scaling gamma = s.y / y.y.
Line search: backtracking from step 1 (first iteration: step 1/|g|_inf) with the Armijo condition (c1 = 1e-4) and
quadratic/cubic interpolation; the (s, y) pair is stored only if s.y > 1e-12 |s||y| (curvature).
Stop (first that holds): max|g| <= gtol; relative decrease (f_k - f_k+1)/max(|f_k|, |f_k+1|, 1) <= ftol on
`patience` consecutive iterations; maxiter; line-search failure (30 reductions); callback returns True.
"""
import numpy as np


def lbfgs(fg, x0, m=20, maxiter=20000, gtol=1e-6, ftol=1e-14, patience=5, callback=None):
    x = x0.copy(); f, g = fg(x)
    S, Y, RHO = [], [], []
    nfev = 1; it = 0; small = 0; msg = 'maxiter reached'
    while it < maxiter:
        if np.max(np.abs(g)) <= gtol:
            msg = 'gtol: max|g| <= %g' % gtol; break
        q = g.copy(); al = []
        for s, y, r in zip(reversed(S), reversed(Y), reversed(RHO)):
            a = r * np.dot(s, q); q -= a * y; al.append(a)
        if S:
            gam = np.dot(S[-1], Y[-1]) / np.dot(Y[-1], Y[-1]); q *= gam
        else:
            q *= 1.0 / max(np.max(np.abs(g)), 1e-300)
        for (s, y, r), a in zip(zip(S, Y, RHO), reversed(al)):
            b = r * np.dot(y, q); q += (a - b) * s
        d = -q
        dg = np.dot(d, g)
        if dg >= 0:                       # not a descent direction: reset memory
            S, Y, RHO = [], [], []; d = -g / max(np.max(np.abs(g)), 1e-300); dg = np.dot(d, g)
        t = 1.0; ok = False
        for ls in range(30):
            xn = x + t * d; fn, gn = fg(xn); nfev += 1
            if np.isfinite(fn) and fn <= f + 1e-4 * t * dg:
                ok = True; break
            # quadratic interpolation of phi(t) = f(x + t d)
            if np.isfinite(fn):
                tn = -dg * t * t / (2 * (fn - f - dg * t))
                t = min(max(tn, 0.1 * t), 0.5 * t)
            else:
                t *= 0.1
        if not ok:
            msg = 'line search failed'; break
        s = xn - x; y = gn - g; sy = np.dot(s, y)
        if sy > 1e-12 * np.linalg.norm(s) * np.linalg.norm(y):
            S.append(s); Y.append(y); RHO.append(1.0 / sy)
            if len(S) > m:
                S.pop(0); Y.pop(0); RHO.pop(0)
        rel = (f - fn) / max(abs(f), abs(fn), 1.0)
        x, f, g = xn, fn, gn; it += 1
        small = small + 1 if rel <= ftol else 0
        if callback is not None and callback(x, f, g, it, nfev):
            msg = 'stopped by callback'; break
        if small >= patience:
            msg = 'ftol: relative decrease <= %g on %d consecutive iterations' % (ftol, patience); break
    return dict(x=x, fun=f, jac=g, nit=it, nfev=nfev, message=msg,
                success=msg.startswith('gtol') or msg.startswith('ftol'))
