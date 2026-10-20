"""Independent cross-check core for E1 (phi^4 in 1+1 D).

Written without reading the original E1 scripts.  Method deliberately differs
from the original (4th-order FD + velocity Verlet):

  * space : 6th-order centred finite differences for phi_xx
  * time  : classical 4th-order Runge-Kutta (RK4)
  * edges : cubic-ramp sponge  -gamma(x) phi_t  (gamma -> GMAX over width W),
            ghost values phi = -1 beyond the array ends
  * grid  : dx = 0.08 by default (original: 0.1 and 0.05)

Convention (PLAN.md E1): V = (phi^2-1)^2/4,  phi_tt = phi_xx - phi(phi^2-1),
m = sqrt2, M_kink = 2 sqrt2/3, kink tanh(x/sqrt2).
"""
import numpy as np
import numba as nb

SQ2 = np.sqrt(2.0)
MKINK = 2.0 * SQ2 / 3.0
KW = SQ2  # kink width


@nb.njit(cache=True, fastmath=False)
def _accel(phi, pi, gam, inv12, out):
    # 6th-order second derivative: (2 f_{i-3} -27 f_{i-2} +270 f_{i-1} -490 f_i +270 f_{i+1} -27 f_{i+2} +2 f_{i+3})/(180 dx^2)
    n = phi.shape[0]
    for i in range(n):
        fm3 = phi[i - 3] if i - 3 >= 0 else -1.0
        fm2 = phi[i - 2] if i - 2 >= 0 else -1.0
        fm1 = phi[i - 1] if i - 1 >= 0 else -1.0
        fp1 = phi[i + 1] if i + 1 < n else -1.0
        fp2 = phi[i + 2] if i + 2 < n else -1.0
        fp3 = phi[i + 3] if i + 3 < n else -1.0
        f = phi[i]
        lap = (2.0 * (fm3 + fp3) - 27.0 * (fm2 + fp2) + 270.0 * (fm1 + fp1) - 490.0 * f) * inv12
        out[i] = lap - f * (f * f - 1.0) - gam[i] * pi[i]


@nb.njit(cache=True)
def rk4_steps(phi, pi, gam, dx, dt, nsteps):
    """Classical RK4 for (phi, pi), in place."""
    n = phi.shape[0]
    inv = 1.0 / (180.0 * dx * dx)
    a = np.empty(n)
    ps = np.empty(n)
    vs = np.empty(n)
    sv = np.empty(n)   # accumulated velocities  pi + 2 pi2 + 2 pi3 + pi4
    sa = np.empty(n)   # accumulated accelerations
    h = 0.5 * dt
    for s in range(nsteps):
        _accel(phi, pi, gam, inv, a)
        for i in range(n):
            sv[i] = pi[i]
            sa[i] = a[i]
            ps[i] = phi[i] + h * pi[i]
            vs[i] = pi[i] + h * a[i]
        _accel(ps, vs, gam, inv, a)
        for i in range(n):
            sv[i] += 2.0 * vs[i]
            sa[i] += 2.0 * a[i]
            ps[i] = phi[i] + h * vs[i]
            vs[i] = pi[i] + h * a[i]
        _accel(ps, vs, gam, inv, a)
        for i in range(n):
            sv[i] += 2.0 * vs[i]
            sa[i] += 2.0 * a[i]
            ps[i] = phi[i] + dt * vs[i]
            vs[i] = pi[i] + dt * a[i]
        _accel(ps, vs, gam, inv, a)
        for i in range(n):
            sv[i] += vs[i]
            sa[i] += a[i]
            phi[i] += dt / 6.0 * sv[i]
            pi[i] += dt / 6.0 * sa[i]
    return phi, pi


def sponge(x, Lphys, W, gmax=1.0):
    s = np.clip((np.abs(x) - Lphys) / W, 0.0, 1.0)
    return gmax * s ** 3


def make_grid(Ltot, dx):
    n = int(round(Ltot / dx))
    x = dx * np.arange(-n, n + 1)
    return x


def energy(phi, pi, dx):
    """Energy with 6th-order first derivative, ghost -1 beyond ends."""
    f = np.concatenate(([-1.0] * 3, phi, [-1.0] * 3))
    d = (-f[0:-6] + 9 * f[1:-5] - 45 * f[2:-4] + 45 * f[4:-2] - 9 * f[5:-1] + f[6:]) / (60 * dx)
    e = 0.5 * pi ** 2 + 0.5 * d ** 2 + 0.25 * (phi ** 2 - 1) ** 2
    return float(np.sum(e) * dx)


def intervals_pos(phi):
    """Maximal index intervals where phi > 0. Returns list of (i0, i1) inclusive."""
    pos = phi > 0
    if not pos.any():
        return []
    d = np.diff(np.concatenate(([0], pos.astype(np.int8), [0])))
    st = np.where(d == 1)[0]
    en = np.where(d == -1)[0] - 1
    return list(zip(st, en))


def pair_test_report(phi, dx):
    """Pair test as described (in words) in the original REPORT.md:
    a maximal phi>0 interval longer than 4 kink widths with phi>0.5 on >=80% of its points."""
    for i0, i1 in intervals_pos(phi):
        length = (i1 - i0 + 1) * dx
        if length > 4 * KW:
            seg = phi[i0:i1 + 1]
            if np.mean(seg > 0.5) >= 0.8:
                return True
    return False


def pair_test_mine(phi, dx):
    """My own variant: a phi>0 interval of length > 3 kink widths whose median exceeds 0.8
    (i.e. a plateau near the +1 vacuum)."""
    for i0, i1 in intervals_pos(phi):
        length = (i1 - i0 + 1) * dx
        if length > 3 * KW:
            if np.median(phi[i0:i1 + 1]) > 0.8:
                return True
    return False
