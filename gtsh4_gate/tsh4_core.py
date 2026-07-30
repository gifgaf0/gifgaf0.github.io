"""
G-TSH4 CC leg -- core solver (full-from-scratch, E6).

Independent numpy/scipy implementation of the dimensionless 3D Gross-Pitaevskii
energy functional specified in G_TSH4_EXECUTION_PREREGISTRATION.md (LOCKED,
md5 e66b964d4467fcb9a5f328ef0db80a35), with the Amendment-1 PART A rules
(md5 2c67670112844e9df9cf9909a06ac27a).

    e = <1/2 |grad psi|^2> + (Lambda/2) <n (Uhat * n)>,   n=|psi|^2, <n>=1

exactly one control parameter Lambda = rho_bar * U0, units hbar^2/mR^2.

Kernels are used analytically in k-space (pre-reg sec.B): the step kernel's
real-space discontinuity would inject O(dx) error above delta_E otherwise.

T1 discipline: this file introduces no forbidden physical-constant or
observable-target strings (the forbidden set is defined and enforced in
tsh4_selfgrep.py). Everything here is dimensionless.
"""
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma as Gamma
from scipy.interpolate import CubicSpline

# --------------------------------------------------------------------------
# Kernels in k-space (Uhat = U/U0, dimensionless; here U0=1 so Uhat is the raw
# transform -- the /U0 is absorbed into Lambda).
# --------------------------------------------------------------------------

def step_khat(k):
    """Fourier transform of U(r)=Theta(1-r):  4 pi (sin k - k cos k)/k^3."""
    k = np.asarray(k, float)
    out = np.empty(k.shape, float)
    small = k < 1e-6
    ks = k[~small]
    out[~small] = 4*np.pi*(np.sin(ks) - ks*np.cos(ks))/ks**3
    out[small] = 4*np.pi/3.0
    return out


class Gem8Khat:
    """FT of U(r)=exp(-r^8) built once by high-accuracy quadrature on a dense
    radial table with cubic-spline interpolation (pre-reg tol 1e-10)."""
    def __init__(self, kmax=80.0, nk=4000):
        self.U0 = 4*np.pi*(1/8)*Gamma(3/8)
        kt = np.linspace(0.0, kmax, nk)
        vals = np.empty_like(kt)
        vals[0] = self.U0
        for i, k in enumerate(kt[1:], 1):
            f = lambda r: r*np.exp(-r**8)*np.sin(k*r)
            v, _ = quad(f, 0, np.inf, limit=500, epsabs=1e-12, epsrel=1e-11)
            vals[i] = 4*np.pi/k*v
        self.spline = CubicSpline(kt, vals)
        self.kmax = kmax

    def __call__(self, k):
        k = np.asarray(k, float)
        out = self.spline(k)
        # exp(-r^8) is compact enough that Uhat -> 0 well before kmax; clamp tail
        out = np.where(k > self.kmax, 0.0, out)
        return out


def lambda_c(khat, kmax, ngrid=40000):
    """roton threshold: Lambda_c = min_{k: Uhat<0} [ -k^2/(4 Uhat(k)) ]."""
    ks = np.linspace(1e-3, kmax, ngrid)
    U = khat(ks)
    cand = np.full_like(ks, np.inf)
    neg = U < 0
    cand[neg] = -ks[neg]**2/(4*U[neg])
    i = int(np.argmin(cand))
    # parabolic refine around the discrete minimum
    lo, hi = max(i-3, 0), min(i+4, len(ks))
    kk, cc = ks[lo:hi], cand[lo:hi]
    m = np.isfinite(cc)
    p = np.polyfit(kk[m], cc[m], 2)
    kstar = -p[1]/(2*p[0])
    lc = np.polyval(p, kstar)
    return float(lc), float(kstar)


# --------------------------------------------------------------------------
# Structure definitions.  Fractional site positions in an orthorhombic cell.
# Hexagonal family: orthorhombic cell (a, a*sqrt3, c).  Cubic family: (L,L,L).
# --------------------------------------------------------------------------
S3 = np.sqrt(3.0)

def sites_hex(name):
    """fractional (u,v,w) site positions in the orthorhombic hex cell.
    In-plane rectangle a x a*sqrt3 holds two triangular-lattice points:
    (0,0) and (a/2, a*sqrt3/2) -> fractional (0,0),(1/2,1/2)."""
    base = [(0.0, 0.0), (0.5, 0.5)]                     # triangular layer
    shift_B = (0.5, 1.0/6.0)                            # (a/2, a*sqrt3/6)
    shift_C = (0.0, 1.0/3.0)                            # (a, a*sqrt3/3) mod cell -> u=0
    if name == 'AA':
        layers = [(0.0, (0.0, 0.0))]
    elif name == 'AB':
        layers = [(0.0, (0.0, 0.0)), (0.5, shift_B)]
    elif name == 'ABC':
        layers = [(0.0, (0.0, 0.0)), (1.0/3.0, shift_B), (2.0/3.0, shift_C)]
    else:
        raise ValueError(name)
    out = []
    for w, (du, dv) in layers:
        for (u, v) in base:
            out.append(((u+du) % 1.0, (v+dv) % 1.0, w % 1.0))
    return np.array(out)

def sites_cubic(name):
    if name == 'FCC':
        return np.array([(0,0,0),(0,0.5,0.5),(0.5,0,0.5),(0.5,0.5,0)], float)
    if name == 'BCC':
        return np.array([(0,0,0),(0.5,0.5,0.5)], float)
    raise ValueError(name)

STRUCTURES = {
    'AA':  dict(family='hex',  sites=sites_hex('AA')),
    'AB':  dict(family='hex',  sites=sites_hex('AB')),
    'ABC': dict(family='hex',  sites=sites_hex('ABC')),
    'FCC': dict(family='cubic', sites=sites_cubic('FCC')),
    'BCC': dict(family='cubic', sites=sites_cubic('BCC')),
}


# --------------------------------------------------------------------------
# GP relaxation on a periodic orthorhombic cell.
# --------------------------------------------------------------------------
class Cell:
    def __init__(self, L, n):
        self.L = np.asarray(L, float)          # (Lx,Ly,Lz)
        self.n = tuple(int(x) for x in n)      # grid points
        kx = 2*np.pi*np.fft.fftfreq(self.n[0], d=self.L[0]/self.n[0])
        ky = 2*np.pi*np.fft.fftfreq(self.n[1], d=self.L[1]/self.n[1])
        kz = 2*np.pi*np.fft.fftfreq(self.n[2], d=self.L[2]/self.n[2])
        KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
        self.K2 = KX**2 + KY**2 + KZ**2
        self.Kmag = np.sqrt(self.K2)
        self.N = np.prod(self.n)

    def seed(self, frac_sites, width):
        """sum of periodic Gaussians at fractional sites, then normalise <n>=1."""
        xs = [ (np.arange(self.n[d]) + 0.5)/self.n[d] for d in range(3) ]
        X, Y, Z = np.meshgrid(xs[0], xs[1], xs[2], indexing='ij')
        rho = np.zeros(self.n)
        for (u, v, w) in frac_sites:
            for su in (-1,0,1):
                for sv in (-1,0,1):
                    for sw in (-1,0,1):
                        dx = (X-(u+su))*self.L[0]
                        dy = (Y-(v+sv))*self.L[1]
                        dz = (Z-(w+sw))*self.L[2]
                        rho += np.exp(-(dx*dx+dy*dy+dz*dz)/(2*width*width))
        rho += 1e-6
        psi = np.sqrt(rho)
        psi /= np.sqrt((psi*psi).mean())
        return psi


def relax(cell, khat_on_grid, Lam, psi0, dt=0.008, itmax=20000,
          restol=1e-10, adapt=True, verbose=False):
    """normalised imaginary-time gradient flow for  dpsi/dtau = -(H - mu) psi,
    semi-implicit (implicit kinetic, explicit interaction, mu-shift consistent):

        (1 + dt/2 K^2) psihat_new = ( (1 + dt mu) psi - dt Lam (Uhat*n) psi )hat

    The mu-shift makes the DISCRETE fixed point the exact ground state
    (H psi = mu psi) for any stable dt -- without it there is an O(dt*mu) bias.
    Adaptive: if a step raises the energy (onset of instability) dt is halved.

    Returns psi, e, residual, iters, (ke, ie)."""
    K2 = cell.K2
    psi = psi0.copy()
    denom = 1.0 + dt*0.5*K2
    e_prev = energy(cell, khat_on_grid, Lam, psi)
    it_done = 0
    for it in range(1, itmax+1):
        n = psi*psi
        conv = np.fft.ifftn(khat_on_grid*np.fft.fftn(n)).real
        Hpsi = np.fft.ifftn(0.5*K2*np.fft.fftn(psi)).real + Lam*conv*psi
        mu = (psi*Hpsi).mean()/(psi*psi).mean()
        rhs = np.fft.fftn((1.0 + dt*mu)*psi - dt*Lam*conv*psi)
        psi_new = np.fft.ifftn(rhs/denom).real
        psi_new /= np.sqrt((psi_new*psi_new).mean())
        if it % 25 == 0 or it < 5:
            e = energy(cell, khat_on_grid, Lam, psi_new)
            if adapt and e > e_prev + 1e-9*abs(e_prev):   # instability -> back off
                dt *= 0.5
                denom = 1.0 + dt*0.5*K2
                if dt < 1e-5:
                    it_done = it; break
                continue
            res = gp_residual(cell, khat_on_grid, Lam, psi_new)
            psi = psi_new; e_prev = e; it_done = it
            if res < restol:
                break
        else:
            psi = psi_new
    e, ke, ie = energy(cell, khat_on_grid, Lam, psi, split=True)
    res = gp_residual(cell, khat_on_grid, Lam, psi)
    return psi, e, res, it_done, (ke, ie)


def energy(cell, khat_on_grid, Lam, psi, split=False):
    N = cell.N
    psik = np.fft.fftn(psi)
    ke = 0.5*np.sum(cell.K2*np.abs(psik)**2)/N**2
    n = psi*psi
    cG = np.fft.fftn(n)/N                     # continuous Fourier coeffs of n
    ie = 0.5*Lam*np.sum((np.abs(cG)**2)*khat_on_grid)
    if split:
        return float(ke+ie), float(ke), float(ie)
    return float(ke+ie)


def gp_residual(cell, khat_on_grid, Lam, psi):
    """||H psi - mu psi|| / |mu|, H psi = -1/2 lap psi + Lam (Uhat*n) psi."""
    n = psi*psi
    conv = np.fft.ifftn(khat_on_grid*np.fft.fftn(n)).real
    Hpsi = np.fft.ifftn(0.5*cell.K2*np.fft.fftn(psi)).real + Lam*conv*psi
    mu = (psi*Hpsi).mean()/(psi*psi).mean()
    r = Hpsi - mu*psi
    return float(np.sqrt((r*r).mean())/abs(mu))


def khat_grid(cell, khat):
    """evaluate kernel transform on the cell's reciprocal grid (G=0 -> Uhat(0))."""
    return khat(cell.Kmag)


def bragg_report(cell, psi, topk=8):
    """dominant nonzero Fourier peaks of the density (fractional Miller-ish)."""
    n = psi*psi
    cG = np.abs(np.fft.fftn(n))/cell.N
    cG_flat = cG.copy()
    cG_flat.flat[0] = 0.0
    idx = np.argsort(cG_flat.ravel())[::-1][:topk]
    peaks = []
    fx = np.fft.fftfreq(cell.n[0])*cell.n[0]
    fy = np.fft.fftfreq(cell.n[1])*cell.n[1]
    fz = np.fft.fftfreq(cell.n[2])*cell.n[2]
    for ii in idx:
        i, j, k = np.unravel_index(ii, cell.n)
        peaks.append((int(fx[i]), int(fy[j]), int(fz[k]), float(cG[i, j, k])))
    return peaks
