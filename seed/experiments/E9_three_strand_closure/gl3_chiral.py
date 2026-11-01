"""
E9 with the chiral term (PREREG_chiral_loop.md §1-§2). Label: Exploration. Model units only.

E = E_gl3[psi, A] + gamma * sum_x h^3 psi*(x) . (D x psi)(x),   D = grad - i e A,
with strand k locked to grid axis k (A5): (D x psi)_i = eps_ijk D_j psi_k, j a grid axis, k a strand index.

Lattice form (PREREG §2): symmetric covariant difference on gl3's links,
    D_j psi(x) = [U_j(x) psi(x+j) - U_j(x-j)^* psi(x-j)] / (2h),   U_j = exp(-i e h A_j)   (as in gl3.py).
Summed over x the backward half is the complex conjugate of the forward half, so
    E_chi = gamma h^3 sum_x psi*.(eps D psi) = gamma h^2 Re sum_j sum_{x, x+j in box} U_j(x) W_j(x),
    W_j(x) = psi*(x) . (e_j x psi(x+j)),
which is real by construction and exactly gauge covariant. On open boundaries the terms that cross the
box are dropped (forward and backward halves of the same link are dropped together).
Sign convention: (D x psi)_i = eps_ijk D_j psi_k, the same as chiral1d.py (psi*.(n x U psi(s+1))); the
helix psi = (cos qz, sin qz, 0) has psi*.(curl psi) = -q.

gamma == 0 returns GL3.energy_grad(v) unchanged (the same call, bitwise the same result).
Gradient convention as gl3.py: the psi block of the gradient is 2 dE/dpsi* (= d/dRe + i d/dIm).
"""
import numpy as np
from gl3 import GL3


def _ecross(j, v):
    """e_j x v for v of shape (3, ...)."""
    if j == 0: return np.stack([np.zeros_like(v[0]), -v[2], v[1]])
    if j == 1: return np.stack([v[2], np.zeros_like(v[0]), -v[0]])
    return np.stack([-v[1], v[0], np.zeros_like(v[0])])


def _sl(j, N):
    lo = [slice(None)] * 3; hi = [slice(None)] * 3
    lo[j] = slice(0, N - 1); hi[j] = slice(1, N)
    return tuple(lo), tuple(hi)


class GL3Chiral(GL3):
    def __init__(self, N=48, h=0.5, e=1 / np.sqrt(12.0), eta=0.1, gamma=0.0):
        super().__init__(N=N, h=h, e=e, eta=eta)
        self.gamma = float(gamma)

    # ---- chiral term ---------------------------------------------------------
    def chiral_energy_grad(self, psi, A, gamma=None, with_grad=True):
        """Returns E_chi and (gpsi, gA) of the chiral term alone (gl3 conventions)."""
        g = self.gamma if gamma is None else gamma
        N, h, e = self.N, self.h, self.e
        c = g * h ** 2
        E = 0.0
        gpsi = np.zeros_like(psi) if with_grad else None
        gA = np.zeros_like(A) if with_grad else None
        for j in range(3):
            lo, hi = _sl(j, N)
            U = np.exp(-1j * e * h * A[j][lo])
            plo = psi[(slice(None),) + lo]; phi = psi[(slice(None),) + hi]
            xphi = _ecross(j, phi)
            W = np.sum(np.conj(plo) * xphi, axis=0)
            UW = U * W
            E += c * np.sum(UW.real)
            if with_grad:
                gpsi[(slice(None),) + lo] += c * U * xphi
                gpsi[(slice(None),) + hi] -= c * np.conj(U) * _ecross(j, plo)
                gA[j][lo] += c * e * h * UW.imag
        if with_grad and self.pin is not None:
            gpsi[self.pin] = 0.0
        return E, gpsi, gA

    def energy_grad(self, v):
        if self.gamma == 0.0:
            return GL3.energy_grad(self, v)
        E, gr = GL3.energy_grad(self, v)
        psi, A = self.unpack(v)
        Ec, gpsi, gA = self.chiral_energy_grad(psi, A)
        return E + Ec, gr + np.concatenate([gpsi.real.ravel(), gpsi.imag.ravel(), gA.ravel()])

    # ---- diagnostics -----------------------------------------------------------
    def chiral_complex(self, psi, A):
        """Complex value of sum_x h^3 psi*.(eps D psi) with the symmetric difference, both halves summed
        separately (for the reality check). Not multiplied by gamma."""
        N, h, e = self.N, self.h, self.e
        fwd = 0j; bwd = 0j
        for j in range(3):
            lo, hi = _sl(j, N)
            U = np.exp(-1j * e * h * A[j][lo])
            plo = psi[(slice(None),) + lo]; phi = psi[(slice(None),) + hi]
            fwd += np.sum(np.conj(plo) * _ecross(j, U * phi))          # psi*(x).(e_j x U_j(x) psi(x+j)) at x = lo
            bwd += np.sum(np.conj(phi) * _ecross(j, np.conj(U) * plo))  # psi*(y).(e_j x U_j(y-j)* psi(y-j)) at y = hi
        return h ** 3 * (fwd - bwd) / (2 * h)

    def chiral_density(self, psi, A, gamma=None):
        """Site-local gamma h^3 Re[psi*(x).(eps D psi)(x)] (symmetric difference); sums to E_chi exactly."""
        g = self.gamma if gamma is None else gamma
        N, h, e = self.N, self.h, self.e
        d = np.zeros(psi.shape[1:])
        for j in range(3):
            lo, hi = _sl(j, N)
            U = np.exp(-1j * e * h * A[j][lo])
            plo = psi[(slice(None),) + lo]; phi = psi[(slice(None),) + hi]
            d[lo] += 0.5 * np.real(np.sum(np.conj(plo) * _ecross(j, U * phi), axis=0))
            d[hi] -= 0.5 * np.real(np.sum(np.conj(phi) * _ecross(j, np.conj(U) * plo), axis=0))
        return g * h ** 2 * d

    def split(self, psi, A):
        """Energy pieces: E_grad (sum |D psi|^2, covariant forward difference), E_mag, E_V (potential +
        Josephson above vacuum), E_chi, E_chi_AS = E_chi - E_chi[psi, A = 0] (the part carried by A; gauge
        dependent), and the per-site covariant |D psi|^2 (summed over k and the forward links of x)."""
        N, h, e, eta = self.N, self.h, self.e, self.eta
        h3 = h ** 3
        Eg = 0.0; w = np.zeros(psi.shape[1:])
        for mu in range(3):
            lo, hi = _sl(mu, N)
            U = np.exp(-1j * e * h * A[mu][lo])
            D2 = np.sum(np.abs((U * psi[(slice(None),) + hi] - psi[(slice(None),) + lo]) / h) ** 2, axis=0)
            Eg += h3 * np.sum(D2); w[lo] += D2
        rho = np.abs(psi) ** 2
        EV = h3 * 0.5 * np.sum((rho - 1) ** 2)
        for i in range(3):
            for j in range(i + 1, 3):
                EV -= eta * h3 * np.sum(np.real(psi[i] * np.conj(psi[j])))
        EV -= self.vacuum_energy()
        Em = 0.0
        for mu in range(3):
            for nu in range(mu + 1, 3):
                s = [slice(0, N - 1)] * 3; s[3 - mu - nu] = slice(None); s = tuple(s)
                def shift(arr, d):
                    t = list(s); t[d] = slice(1, N); return arr[tuple(t)]
                F = (shift(A[nu], mu) - A[nu][s] - shift(A[mu], nu) + A[mu][s]) / h
                Em += h3 * 0.5 * np.sum(F ** 2)
        Ec = self.chiral_energy_grad(psi, A, with_grad=False)[0]
        Ec0 = self.chiral_energy_grad(psi, np.zeros_like(A), with_grad=False)[0]
        return dict(E_grad=float(Eg), E_mag=float(Em), E_V=float(EV), E_chi=float(Ec), E_chi_AS=float(Ec - Ec0)), w


def S_field(psi):
    """S = i psi x psi* (real 3-vector per site)."""
    p, q = psi, np.conj(psi)
    cr = np.stack([p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0]])
    return np.real(1j * cr)


def check_grad(N=6, eta=0.1, gamma=0.3, seed=0, five_point=False, eps=None, n=40):
    """gl3.check_grad's body with GL3Chiral (N = 6, seed 0, 40 random components, scale 0.5).
    five_point: 5-point stencil (step 1e-3) instead of central differences (step 1e-6)."""
    g = GL3Chiral(N=N, h=0.5, eta=eta, gamma=gamma)
    rng = np.random.default_rng(seed)
    v = rng.normal(size=9 * g.nsite) * 0.5
    E, grad = g.energy_grad(v)
    idx = rng.choice(v.size, n, replace=False); worst = 0.0
    eps = (1e-3 if five_point else 1e-6) if eps is None else eps
    for i in idx:
        def f(t):
            vp = v.copy(); vp[i] += t; return g.energy_grad(vp)[0]
        if five_point:
            fd = (f(-2 * eps) - 8 * f(-eps) + 8 * f(eps) - f(2 * eps)) / (12 * eps)
        else:
            fd = (f(eps) - f(-eps)) / (2 * eps)
        worst = max(worst, abs(fd - grad[i]) / (abs(fd) + 1e-8))
    return worst


if __name__ == '__main__':
    print('gradient check (gl3 style), gamma = 0.3, worst relative error:', check_grad())
    print('gradient check (5-point),   gamma = 0.3, worst relative error:', check_grad(five_point=True))
