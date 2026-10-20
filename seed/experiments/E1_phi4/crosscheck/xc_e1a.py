"""E1a cross-check: static kink mass and shape mode by methods different from the original
(lattice Newton + sparse lattice eigensolver):
  (1) static BVP phi'' = phi^3 - phi on [-L, L], phi(+-L) = +-tanh(L/sqrt2), solved by
      scipy's collocation solver solve_bvp from a crude initial guess (no analytic input);
      mass = integral of phi'^2 (virial: gradient = potential) and of phi'^2/2 + V, by quadrature
      of the collocation spline.
  (2) shape mode: Chebyshev collocation of -d^2 + 3 phi_k^2 - 1 on a mapped infinite line
      x = c * tan(theta)... here simply on [-L, L] with Dirichlet ends, N = 160 and 240.
  (3) time domain: excite the shape mode in the 6th-order FD + RK4 code and measure the frequency.
"""
import json, os, sys
import numpy as np
from scipy.integrate import solve_bvp, quad
from scipy.linalg import eig
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SQ2 = np.sqrt(2.0)
MK = 2 * SQ2 / 3
WS = np.sqrt(1.5)
out = {}

# (1) BVP
for L in (15.0, 25.0):
    xs = np.linspace(-L, L, 401)
    y0 = np.vstack([np.clip(xs / 3, -1, 1), np.where(np.abs(xs) < 3, 1 / 3, 0.0)])
    fun = lambda x, y: np.vstack([y[1], y[0] ** 3 - y[0]])
    bc = lambda ya, yb: np.array([ya[0] + np.tanh(L / SQ2), yb[0] - np.tanh(L / SQ2)])
    sol = solve_bvp(fun, bc, xs, y0, tol=1e-10, max_nodes=200000)
    grad = quad(lambda x: 0.5 * sol.sol(x)[1] ** 2, -L, L, limit=2000, epsabs=1e-13, epsrel=1e-13)[0]
    pot = quad(lambda x: 0.25 * (sol.sol(x)[0] ** 2 - 1) ** 2, -L, L, limit=2000, epsabs=1e-13, epsrel=1e-13)[0]
    M = grad + pot
    out[f'bvp_L{L}'] = dict(status=int(sol.status), M=M, rel_err=M / MK - 1, virial_grad_minus_pot=grad - pot,
                           max_dev_from_tanh=float(np.max(np.abs(sol.sol(xs)[0] - np.tanh(xs / SQ2)))))
    print('BVP L=%g: M=%.12f rel.err=%.2e  grad-pot=%.1e  max|phi-tanh|=%.1e' % (
        L, M, M / MK - 1, grad - pot, out[f'bvp_L{L}']['max_dev_from_tanh']))


# (2) Chebyshev collocation of the fluctuation operator
def cheb(N):
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.hstack([2, np.ones(N - 1), 2]) * (-1) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1 / c) / (dX + np.eye(N + 1))
    D = D - np.diag(D.sum(axis=1))
    return D, x


for N, L in ((160, 20.0), (240, 30.0)):
    D, y = cheb(N)
    x = L * y
    D2 = (D @ D) / L ** 2
    Hm = -D2 + np.diag(3 * np.tanh(x / SQ2) ** 2 - 1)
    Hi = Hm[1:-1, 1:-1]
    ev = np.sort(np.real(eig(Hi, right=False)))
    w0, w1 = ev[0], ev[1]
    out[f'cheb_N{N}_L{L}'] = dict(ev0=float(w0), omega_s=float(np.sqrt(w1)), rel_err=float(np.sqrt(w1) / WS - 1),
                                 next=float(ev[2]))
    print('Chebyshev N=%d L=%g: lowest ev %.2e, omega_s=%.12f rel.err %.2e, next ev %.4f (continuum starts at 2)' % (
        N, L, w0, np.sqrt(w1), np.sqrt(w1) / WS - 1, ev[2]))

# (3) time domain with the RK4/FD6 code
from xc_core import rk4_steps, make_grid, energy, sponge
dx, dt = 0.08, 0.02
x = make_grid(60.0, dx)
# kink -> need +1 at right end; the core uses ghost -1 at both ends, so use a kink-antikink pair far apart
X0 = 25.0
eps = 0.01
psi = lambda y: np.sinh(y / SQ2) / np.cosh(y / SQ2) ** 2  # shape mode of a kink (unnormalised)
phi = np.tanh((x + X0) / SQ2) - np.tanh((x - X0) / SQ2) - 1 + eps * psi(x + X0)
pi = np.zeros_like(x)
gam = sponge(x, 50.0, 10.0, 0.5)
E0 = energy(phi, pi, dx)
Estat = energy(np.tanh((x + X0) / SQ2) - np.tanh((x - X0) / SQ2) - 1, pi, dx)
i0 = int(np.argmin(np.abs(x + X0 + 1.0)))
nrec = 6000
sig = np.empty(nrec)
for n in range(nrec):
    rk4_steps(phi, pi, gam, dx, dt, 1)
    sig[n] = phi[i0]
t = dt * np.arange(1, nrec + 1)
s = sig - sig.mean()
zc = np.where((s[:-1] < 0) & (s[1:] >= 0))[0]
tz = t[zc] - dt * s[zc] / (s[zc + 1] - s[zc])
per = (tz[-1] - tz[0]) / (len(tz) - 1)
wtd = 2 * np.pi / per
out['time_domain'] = dict(omega_s=wtd, rel_err=wtd / WS - 1, n_periods=len(tz) - 1, E_pair_static=Estat,
                          E_pair_static_over_2M=Estat / (2 * MK))
print('time domain: omega_s=%.7f rel.err %.1e over %d periods; static pair energy/2M = %.9f' % (
    wtd, wtd / WS - 1, len(tz) - 1, Estat / (2 * MK)))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xc_e1a.json'), 'w'), indent=1)
