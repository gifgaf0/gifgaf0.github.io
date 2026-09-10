"""
G-TSH4 CC leg -- Route S (static-elastic curvatures).

Homogeneous strain of the optimised crystal, wavefunction re-relaxed at fixed
mean density <n>=1 and fixed Lambda, energy-per-particle curvature A = d2e/ddelta2
extracted per strain mode with quartic and odd-term diagnostics.

Declared BEFORE running (KNOB discipline, made before any Q-C quantity exists):
  * strain amplitude set: delta in {-e0,...,+e0}, 7 points, e0 = 0.02.
  * fit: e(delta) = e0c + A_odd*delta + (1/2)A*delta^2 + c3*delta^3 + c4*delta^4.
    A is the reported raw curvature; A_odd and c4 are the odd/quartic diagnostics.
  * convention: strain deforms the lattice matrix H -> (I+eps)H0; fractional site
    positions are carried affinely; <n>=1 held (volume-changing modes therefore
    compare equal-mean-density crystals -- declared, not tuned).
  * grids: same points-per-length as Phase-0 F-CONV fine grid (ppl=30).

Modes:
  hex (AB): xz (C44), xy (C66), dev (C11-C12), bi (C11+C12), zz (C33), iso (bulk)
  cubic (FCC): xz (C44), dev (C11-C12), iso (bulk modulus 3B=C11+2C12)

F-ISO (A-1.5, hex): |C66 - (C11-C12)/2|/C66 <= 2%  (basal-isotropy tensor identity).
"""
import numpy as np
import tsh4_core as C

S3 = np.sqrt(3.0)

class CellH:
    """periodic cell with a general 3x3 lattice matrix H (columns = cell vectors).
    Exposes K2, Kmag, N, n so tsh4_core.relax/energy/gp_residual work unchanged."""
    def __init__(self, H, n):
        self.H = np.asarray(H, float)
        self.n = tuple(int(x) for x in n)
        self.N = int(np.prod(self.n))
        self.vol = abs(np.linalg.det(self.H))
        Ginv = 2*np.pi*np.linalg.inv(self.H).T          # G = 2pi H^{-T} m
        mx = np.fft.fftfreq(self.n[0])*self.n[0]
        my = np.fft.fftfreq(self.n[1])*self.n[1]
        mz = np.fft.fftfreq(self.n[2])*self.n[2]
        MX, MY, MZ = np.meshgrid(mx, my, mz, indexing='ij')
        GX = Ginv[0,0]*MX + Ginv[0,1]*MY + Ginv[0,2]*MZ
        GY = Ginv[1,0]*MX + Ginv[1,1]*MY + Ginv[1,2]*MZ
        GZ = Ginv[2,0]*MX + Ginv[2,1]*MY + Ginv[2,2]*MZ
        self.K2 = GX**2 + GY**2 + GZ**2
        self.Kmag = np.sqrt(self.K2)

    def seed(self, frac_sites, width):
        s = [ (np.arange(self.n[d]) + 0.5)/self.n[d] for d in range(3) ]
        SX, SY, SZ = np.meshgrid(s[0], s[1], s[2], indexing='ij')
        rho = np.zeros(self.n)
        for (u, v, w) in frac_sites:
            for iu in (-1,0,1):
                for iv in (-1,0,1):
                    for iw in (-1,0,1):
                        ds0 = SX-(u+iu); ds1 = SY-(v+iv); ds2 = SZ-(w+iw)
                        dx = self.H[0,0]*ds0 + self.H[0,1]*ds1 + self.H[0,2]*ds2
                        dy = self.H[1,0]*ds0 + self.H[1,1]*ds1 + self.H[1,2]*ds2
                        dz = self.H[2,0]*ds0 + self.H[2,1]*ds1 + self.H[2,2]*ds2
                        rho += np.exp(-(dx*dx+dy*dy+dz*dz)/(2*width*width))
        rho += 1e-6
        psi = np.sqrt(rho); psi /= np.sqrt((psi*psi).mean())
        return psi


def H0_hex(a, c):   return np.diag([a, a*S3, c]).astype(float)
def H0_cubic(L):    return np.diag([L, L, L]).astype(float)

def strain_tensor(mode, d):
    E = np.zeros((3,3))
    if mode == 'iso':   E = d*np.eye(3)
    elif mode == 'zz':  E[2,2] = d
    elif mode == 'bi':  E[0,0] = E[1,1] = d
    elif mode == 'dev': E[0,0] = d; E[1,1] = -d            # basal volume-conserving
    elif mode == 'xy':  E[0,1] = E[1,0] = d                # basal shear (engineering 2d)
    elif mode == 'xz':  E[0,2] = E[2,0] = d                # axial shear
    else: raise ValueError(mode)
    return E

def grid_for(H, ppl):
    # points along each cell vector proportional to its length
    lens = np.linalg.norm(H, axis=0)
    def ev(x):
        x = int(round(x)); return max(16, x + (x & 1))
    return tuple(ev(ppl*l) for l in lens)

def e_at_strain(structure, H0, mode, d, khat, Lam, ppl, wfac=0.24):
    E = strain_tensor(mode, d)
    H = (np.eye(3) + E) @ H0
    n = grid_for(H, ppl)
    cell = CellH(H, n)
    kg = khat(cell.Kmag)
    psi0 = cell.seed(C.STRUCTURES[structure]['sites'], width=wfac*np.linalg.norm(H0[:,0]))
    psi, e, res, it, _ = C.relax(cell, kg, Lam, psi0, dt=0.006, restol=1e-9)
    return e, res

def curvature(structure, H0, mode, khat, Lam, ppl, e0=0.02, npts=7):
    ds = np.linspace(-e0, e0, npts)
    es, ress = [], []
    for d in ds:
        e, r = e_at_strain(structure, H0, mode, d, khat, Lam, ppl)
        es.append(e); ress.append(r)
    es = np.array(es)
    # fit up to quartic
    coef = np.polyfit(ds, es, 4)                # [c4,c3,c2,c1,c0]
    c4, c3, c2, c1, c0 = coef
    A = 2*c2                                     # d2e/dd2 = 2*c2
    return dict(mode=mode, A=float(A), A_odd=float(c1), c3=float(c3),
                c4=float(c4), e_min=float(es.min()), deltas=list(np.round(ds,4)),
                energies=[float(x) for x in es], res_max=float(max(ress)))
