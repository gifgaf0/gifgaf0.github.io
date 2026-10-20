"""Core numerics for experiment E1 (phi^4 in 1+1 dimensions).

Convention (Dutta-Steer-Vachaspati, PLAN.md E1):
    L = (1/2) phi_t^2 - (1/2) phi_x^2 - (1/4)(phi^2 - 1)^2
    EOM: phi_tt = phi_xx - phi (phi^2 - 1)
    vacua phi = +-1, meson mass m = sqrt(2), kink tanh(x/sqrt2), M_kink = 2 sqrt2 / 3.

Discretization: uniform grid with a node at x = 0, fourth-order centred
finite differences for phi_xx, velocity-Verlet (leapfrog) time stepping.
Absorbing layers: a damping term -gamma(x) phi_t outside |x| < Lphys, with
gamma rising quadratically to gmax over a width W; applied by exact
exponential splitting  e^{-gamma dt/2} . kick . drift . kick . e^{-gamma dt/2}.
Field values beyond the array ends (ghost points) are fixed to bL, bR.
"""
import numpy as np
import numba as nb

SQ2 = np.sqrt(2.0)
M_KINK = 2.0 * SQ2 / 3.0
M_MESON = SQ2
KINK_WIDTH = SQ2          # tanh(x / w)


def grid(L, dx):
    """Symmetric grid on [-L, L] with a node at x = 0."""
    n_half = int(round(L / dx))
    x = dx * np.arange(-n_half, n_half + 1, dtype=np.float64)
    return x


def sponge(x, Lphys, W, gmax, dt):
    """Return exp(-gamma(x) dt / 2) for the absorbing layer."""
    ax = np.abs(x)
    s = np.clip((ax - Lphys) / W, 0.0, None)
    gam = gmax * np.minimum(s, 1.0) ** 2
    gam[ax > Lphys + W] = gmax
    return np.exp(-0.5 * gam * dt), gam


@nb.njit(cache=True, fastmath=False)
def force(phi, F, inv12dx2, bL, bR):
    n = phi.size
    # interior
    for i in range(2, n - 2):
        p0 = phi[i]
        F[i] = (-phi[i - 2] + 16.0 * phi[i - 1] - 30.0 * p0 + 16.0 * phi[i + 1]
                - phi[i + 2]) * inv12dx2 - p0 * (p0 * p0 - 1.0)
    # edges with ghost values
    for i in (0, 1, n - 2, n - 1):
        p0 = phi[i]
        pm1 = phi[i - 1] if i >= 1 else bL
        pm2 = phi[i - 2] if i >= 2 else bL
        pp1 = phi[i + 1] if i + 1 < n else bR
        pp2 = phi[i + 2] if i + 2 < n else bR
        F[i] = (-pm2 + 16.0 * pm1 - 30.0 * p0 + 16.0 * pp1 - pp2) * inv12dx2 \
            - p0 * (p0 * p0 - 1.0)


@nb.njit(cache=True, fastmath=False)
def leapfrog(phi, pi, F, dt, nsteps, inv12dx2, bL, bR, dampfac, ic, rec):
    """Advance nsteps of velocity Verlet. F must hold force(phi) on entry and
    holds force(phi) on exit. rec[s] = phi[ic] after step s."""
    n = phi.size
    hdt = 0.5 * dt
    for s in range(nsteps):
        for i in range(n):
            pi[i] = pi[i] * dampfac[i] + hdt * F[i]
            phi[i] += dt * pi[i]
        force(phi, F, inv12dx2, bL, bR)
        for i in range(n):
            pi[i] = (pi[i] + hdt * F[i]) * dampfac[i]
        rec[s] = phi[ic]


@nb.njit(cache=True, fastmath=False)
def energy_density(phi, pi, dx, bL, bR):
    """e(x) = pi^2/2 + phi_x^2/2 + (phi^2-1)^2/4 with a 4th-order phi_x."""
    n = phi.size
    e = np.empty(n)
    for i in range(n):
        pm1 = phi[i - 1] if i >= 1 else bL
        pm2 = phi[i - 2] if i >= 2 else bL
        pp1 = phi[i + 1] if i + 1 < n else bR
        pp2 = phi[i + 2] if i + 2 < n else bR
        d = (pm2 - 8.0 * pm1 + 8.0 * pp1 - pp2) / (12.0 * dx)
        p = phi[i]
        e[i] = 0.5 * pi[i] * pi[i] + 0.5 * d * d + 0.25 * (p * p - 1.0) ** 2
    return e


def energy(phi, pi, dx, bL=-1.0, bR=-1.0, mask=None):
    e = energy_density(phi, pi, dx, bL, bR)
    if mask is not None:
        e = e[mask]
    return float(np.sum(e) * dx)


class Sim:
    """Thin stateful wrapper: holds fields and advances them in chunks."""

    def __init__(self, x, phi, pi, dt, Lphys=None, W=40.0, gmax=1.0,
                 bL=-1.0, bR=-1.0):
        self.x = x
        self.dx = x[1] - x[0]
        self.phi = np.ascontiguousarray(phi, dtype=np.float64).copy()
        self.pi = np.ascontiguousarray(pi, dtype=np.float64).copy()
        self.dt = dt
        self.bL, self.bR = bL, bR
        self.inv12dx2 = 1.0 / (12.0 * self.dx * self.dx)
        if Lphys is None:
            self.dampfac = np.ones_like(x)
            self.gamma = np.zeros_like(x)
        else:
            self.dampfac, self.gamma = sponge(x, Lphys, W, gmax, dt)
        self.F = np.empty_like(x)
        force(self.phi, self.F, self.inv12dx2, bL, bR)
        self.ic = int(np.argmin(np.abs(x)))
        self.t = 0.0
        self.nstep = 0

    def run(self, nsteps):
        rec = np.empty(nsteps)
        leapfrog(self.phi, self.pi, self.F, self.dt, nsteps, self.inv12dx2,
                 self.bL, self.bR, self.dampfac, self.ic, rec)
        self.nstep += nsteps
        self.t = self.nstep * self.dt
        return rec

    def energy(self, mask=None):
        return energy(self.phi, self.pi, self.dx, self.bL, self.bR, mask)


# ---------------------------------------------------------------- detection
def positive_intervals(x, phi):
    """Maximal intervals where phi > 0. Returns list of
    (z_left, z_right, frac_above_half, max_phi), zeros linearly interpolated."""
    s = phi > 0.0
    if not s.any():
        return []
    d = np.diff(s.astype(np.int8))
    starts = list(np.where(d == 1)[0] + 1)
    ends = list(np.where(d == -1)[0])
    if s[0]:
        starts = [0] + starts
    if s[-1]:
        ends = ends + [len(s) - 1]
    out = []
    for a, b in zip(starts, ends):
        if a > 0:
            zl = x[a - 1] + (x[a] - x[a - 1]) * (0.0 - phi[a - 1]) / (phi[a] - phi[a - 1])
        else:
            zl = x[0]
        if b < len(s) - 1:
            zr = x[b] + (x[b + 1] - x[b]) * (0.0 - phi[b]) / (phi[b + 1] - phi[b])
        else:
            zr = x[-1]
        seg = phi[a:b + 1]
        out.append((float(zl), float(zr), float(np.mean(seg > 0.5)), float(seg.max())))
    return out


# Production criterion, fixed before any E1c/E1d scan was run:
#   a "pair" at time t is a maximal interval with phi > 0 whose length between
#   the interpolated zeros exceeds 4 kink widths (4 sqrt2 = 5.657) and on which
#   phi > 0.5 at >= 80% of the grid points;
#   a run "produces" if at least one pair is present at each of the five times
#   0.80 T, 0.85 T, 0.90 T, 0.95 T, T (T = end of the run).
PAIR_MIN_LEN = 4.0 * KINK_WIDTH
PAIR_MIN_FRAC = 0.8
PERSIST_FRACS = (0.80, 0.85, 0.90, 0.95, 1.00)


def count_pairs(x, phi):
    n = 0
    for zl, zr, frac, mx in positive_intervals(x, phi):
        if (zr - zl) > PAIR_MIN_LEN and frac >= PAIR_MIN_FRAC:
            n += 1
    return n


def outer_zero(x, phi):
    """Largest x at which phi crosses zero (x > 0 side); 0 if phi <= 0 there."""
    iv = positive_intervals(x, phi)
    if not iv:
        return 0.0
    return max(zr for zl, zr, f, m in iv)


def kk_initial(x, v, x0):
    """Kink at -x0 moving right, antikink at +x0 moving left, speed v each."""
    g = 1.0 / np.sqrt(1.0 - v * v)
    a = g * (x + x0) / SQ2
    b = g * (x - x0) / SQ2
    phi = np.tanh(a) - np.tanh(b) - 1.0
    pi = -(g * v / SQ2) * (1.0 / np.cosh(a) ** 2 + 1.0 / np.cosh(b) ** 2)
    return phi, pi


def free_quanta(phi, pi, dx, vac=-1.0):
    """Quadratic (free-field) energy and particle number of the fluctuation
    delta = phi - vac about the vacuum, using the lattice dispersion of the
    4th-order stencil: omega_q^2 = 2 + (30 - 32 cos(q dx) + 2 cos(2 q dx))/(12 dx^2).
    N_lin = sum_q (|pi_q|^2 + omega_q^2 |delta_q|^2) / (2 omega_q) / (n dx),
    in units where hbar = 1 and the action is S/phi0^2 (multiply by phi0^2)."""
    n = phi.size
    d = np.fft.fft(phi - vac) * dx
    p = np.fft.fft(pi) * dx
    q = 2 * np.pi * np.fft.fftfreq(n, d=dx)
    w2 = 2.0 + (30.0 - 32.0 * np.cos(q * dx) + 2.0 * np.cos(2 * q * dx)) / (12.0 * dx * dx)
    w = np.sqrt(w2)
    dens = (np.abs(p) ** 2 + w2 * np.abs(d) ** 2) / (n * dx)
    return float(np.sum(dens) / 2.0), float(np.sum(dens / (2.0 * w)))
