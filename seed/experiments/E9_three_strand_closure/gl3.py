"""
E9: three-component Ginzburg-Landau model in 3D, one U(1) gauge field.

E = sum_k [ |D psi_k|^2 + 1/2 (|psi_k|^2 - 1)^2 ] + 1/2 (curl A)^2 - eta * sum_{i<j} Re(psi_i conj(psi_j))
D = grad - i e A.  Coherence length xi = 1/sqrt(2); penetration depth lambda = 1/(e sqrt 6).

Lattice: sites on an N^3 grid with spacing h; psi_k on sites; A_mu on links (non-compact);
covariant difference (exp(-i e h A) psi(x+mu) - psi(x))/h; open boundaries.
All gradients are analytic and checked against finite differences by `check_grad()`.
Nothing in this file refers to any particle mass or measured number.
"""
import numpy as np
from scipy.optimize import minimize

class GL3:
    def __init__(self, N=48, h=0.5, e=1/np.sqrt(12.0), eta=0.1):
        self.N, self.h, self.e, self.eta = N, h, e, eta
        ax = (np.arange(N) - N // 2) * h   # N odd puts a site plane at z = 0
        self.x, self.y, self.z = np.meshgrid(ax, ax, ax, indexing='ij')
        self.nsite = N ** 3
        self.pin = None  # boolean mask of pinned (psi=0) sites per component, or None

    # ---- packing ------------------------------------------------------------
    def pack(self, psi, A):
        return np.concatenate([psi.real.ravel(), psi.imag.ravel(), A.ravel()])
    def unpack(self, v):
        n = 3 * self.nsite; N = self.N
        psi = (v[:n] + 1j * v[n:2 * n]).reshape(3, N, N, N)
        A = v[2 * n:].reshape(3, N, N, N)   # A[mu] lives on link x -> x+mu (last slice unused)
        return psi, A

    # ---- energy and gradient ------------------------------------------------
    def energy_grad(self, v):
        psi, A = self.unpack(v); N, h, e, eta = self.N, self.h, self.e, self.eta
        h3 = h ** 3
        gpsi = np.zeros_like(psi); gA = np.zeros_like(A)
        E = 0.0
        sl = [slice(None)] * 3
        for mu in range(3):
            lo = [slice(None)] * 3; hi = [slice(None)] * 3
            lo[mu] = slice(0, N - 1); hi[mu] = slice(1, N)
            lo, hi = tuple(lo), tuple(hi)
            U = np.exp(-1j * e * h * A[mu][lo])            # link phase
            for k in range(3):
                a = psi[k][lo]; b = psi[k][hi]
                D = (U * b - a) / h
                E += h3 * np.sum(np.abs(D) ** 2)
                gpsi[k][lo] += -2 * D / h * h3           # dE/d conj(a) convention -> real/imag parts
                gpsi[k][hi] += 2 * np.conj(U) * D / h * h3
                gA[mu][lo] += e * h * (-2 * np.imag(U * b * np.conj(a)) / h ** 2) * h3
        # potential
        rho = np.abs(psi) ** 2
        E += h3 * 0.5 * np.sum((rho - 1) ** 2)
        gpsi += 2 * (rho - 1) * psi * h3
        # Josephson
        if eta:
            for i in range(3):
                for j in range(i + 1, 3):
                    E -= eta * h3 * np.sum(np.real(psi[i] * np.conj(psi[j])))
                    gpsi[i] -= eta * h3 * psi[j]
                    gpsi[j] -= eta * h3 * psi[i]
        # magnetic: F_{mu nu} on plaquettes
        for mu in range(3):
            for nu in range(mu + 1, 3):
                s = [slice(0, N - 1)] * 3; s[3 - mu - nu] = slice(None)  # plaquette base sites
                s = tuple(s)
                def shift(arr, d):
                    t = list(s); t[d] = slice(1, N); return arr[tuple(t)]
                F = (shift(A[nu], mu) - A[nu][s] - shift(A[mu], nu) + A[mu][s]) / h
                E += h3 * 0.5 * np.sum(F ** 2)
                g = F / h * h3
                t = list(s); t[mu] = slice(1, N); gA[nu][tuple(t)] += g
                gA[nu][s] -= g
                t = list(s); t[nu] = slice(1, N); gA[mu][tuple(t)] -= g
                gA[mu][s] += g
        if self.pin is not None:
            gpsi[self.pin] = 0.0
        # real-parameter gradient: d/dRe = 2 Re(dE/dconj), d/dIm = 2 Im(dE/dconj); the factors above
        # already carry the 2 where derived from |D|^2; potential and Josephson need the factor too.
        return E, np.concatenate([gpsi.real.ravel(), gpsi.imag.ravel(), gA.ravel()])

    def vacuum_energy(self):
        # true vacuum: equal phases, |psi_k|^2 = 1 + eta (minimizes 1/2(rho-1)^2 - eta*rho per pair-sum)
        eta = self.eta
        return 3 * (0.5 * eta ** 2 - eta * (1 + eta)) * self.h ** 3 * self.nsite

    # ---- geometry helpers ---------------------------------------------------
    def ring_phase(self, center, normal, R):
        """Phase winding once around a circle of radius R (unit normal n, center c)."""
        c = np.asarray(center, float); n = np.asarray(normal, float); n /= np.linalg.norm(n)
        P = np.stack([self.x - c[0], self.y - c[1], self.z - c[2]], -1)
        zloc = P @ n
        rad = np.linalg.norm(P - zloc[..., None] * n, axis=-1)
        return np.arctan2(zloc, rad - R), np.sqrt((rad - R) ** 2 + zloc ** 2)
    def ring_field(self, center, normal, R, core=1.0):
        chi, rho = self.ring_phase(center, normal, R)
        return np.tanh(rho / core) * np.exp(1j * chi)
    def pin_ring(self, components, center, normal, R):
        _, rho = self.ring_phase(center, normal, R)
        mask = np.zeros((3, self.N, self.N, self.N), bool)
        # a connected chain of sites around the circle, in the site plane containing it
        inplane = np.abs(np.stack([self.x, self.y, self.z], -1) @ (np.asarray(normal, float) / np.linalg.norm(normal))
                         - np.dot(center, np.asarray(normal, float) / np.linalg.norm(normal))) < 0.51 * self.h
        for k in components: mask[k] = (rho < 0.75 * self.h) & inplane
        self.pin = mask
    def core_radius(self, psi_k, thresh=0.25):
        """Mean distance from the z-axis of low-amplitude sites near the z=0 plane."""
        m = (np.abs(psi_k) ** 2 < thresh) & (np.abs(self.z) < 1.01 * self.h)
        if not m.any(): return 0.0
        return float(np.mean(np.sqrt(self.x[m] ** 2 + self.y[m] ** 2)))

    # ---- minimizer ------------------------------------------------------------
    def minimize(self, psi, A, maxiter=3000, gtol=1e-5, callback=None):
        if self.pin is not None: psi = psi.copy(); psi[self.pin] = 0.0
        r = minimize(self.energy_grad, self.pack(psi, A), jac=True, method='L-BFGS-B',
                     options=dict(maxiter=maxiter, maxfun=2 * maxiter, gtol=gtol, ftol=1e-13),
                     callback=callback)
        psi, A = self.unpack(r.x)
        return psi, A, r

def check_grad(N=6, eta=0.1, seed=0):
    g = GL3(N=N, h=0.5, eta=eta)
    rng = np.random.default_rng(seed)
    v = rng.normal(size=9 * g.nsite) * 0.5
    E, grad = g.energy_grad(v)
    idx = rng.choice(v.size, 40, replace=False); eps = 1e-6; worst = 0.0
    for i in idx:
        vp = v.copy(); vp[i] += eps; vm = v.copy(); vm[i] -= eps
        fd = (g.energy_grad(vp)[0] - g.energy_grad(vm)[0]) / (2 * eps)
        worst = max(worst, abs(fd - grad[i]) / (abs(fd) + 1e-8))
    return worst

if __name__ == '__main__':
    print('gradient check, worst relative error:', check_grad())
