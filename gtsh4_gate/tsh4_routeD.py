"""
G-TSH4 CC leg -- Route D (dynamical BdG transverse branches).

Bogoliubov-de Gennes excitation spectrum of a crystal ground state psi0 in a
plane-wave basis.  For real periodic psi0 and Bloch quasimomentum q the
excitation frequencies satisfy

    omega^2 = eig[ L0(q)^{1/2} ( L0(q) + 2 X(q) ) L0(q)^{1/2} ]

with, in the reciprocal-lattice plane-wave basis {G} (phi_G = Fourier coeffs of
psi0, rho_G of n0=|psi0|^2, mu the chemical potential),

    L0(q)_{G,G'} = 1/2 |q+G|^2 delta + Lam Uhat(|G-G'|) rho_{G-G'} - mu delta
    X(q)_{G,G'}  = Lam * sum_P phi_{G-P} Uhat(|q+P|) phi_{P-G'}

Uniform limit (psi0=1): L0=q^2/2, X=Lam Uhat(q) -> omega^2=(q^2/2)(q^2/2+2 Lam Uhat(q)),
the pre-registered C-NEG uniform Bogoliubov control.

Declared before any Q-D quantity (KNOB): step kernel (A-1.3); >=2 |q| per
direction; transverse speed = slope of the two lowest gapless (acoustic)
branches at small |q|; Goldstone check omega(q->0)->0.
"""
import numpy as np
import itertools
import tsh4_core as C

S3 = np.sqrt(3.0)

class PWBasis:
    """plane-wave (reciprocal-lattice) basis for a crystal with lattice matrix H
    and ground state psi0 sampled on an fft grid; keeps |G| <= gcut.
    Fourier coeffs are read from the full fft grid by modular index lookup, so
    difference coefficients phi_{a-b} are obtained by array indexing (aliasing of
    the vanishing high-index tail is negligible for a resolved psi0)."""
    def __init__(self, H, psi0, gcut):
        self.H = np.asarray(H, float)
        self.nn = psi0.shape
        n = self.nn
        self.Binv = 2*np.pi*np.linalg.inv(self.H).T       # reciprocal basis (cols)
        self.phi_full = np.fft.fftn(psi0)/np.prod(n)      # coeffs of psi0
        self.rho_full = np.fft.fftn(psi0*psi0)/np.prod(n) # coeffs of n0
        mx = np.rint(np.fft.fftfreq(n[0])*n[0]).astype(int)
        my = np.rint(np.fft.fftfreq(n[1])*n[1]).astype(int)
        mz = np.rint(np.fft.fftfreq(n[2])*n[2]).astype(int)
        MX, MY, MZ = np.meshgrid(mx, my, mz, indexing='ij')
        GX = self.Binv[0,0]*MX + self.Binv[0,1]*MY + self.Binv[0,2]*MZ
        GY = self.Binv[1,0]*MX + self.Binv[1,1]*MY + self.Binv[1,2]*MZ
        GZ = self.Binv[2,0]*MX + self.Binv[2,1]*MY + self.Binv[2,2]*MZ
        G2 = GX**2 + GY**2 + GZ**2
        sel = G2 <= gcut*gcut
        self.m = np.stack([MX[sel], MY[sel], MZ[sel]], axis=1)   # (NG,3) integer
        self.G = np.stack([GX[sel], GY[sel], GZ[sel]], axis=1)   # (NG,3) cart
        self.NG = self.m.shape[0]

    def coef(self, arr_full, dm):
        """coefficient array_full at integer-triple differences dm (...,3)."""
        ix = dm[..., 0] % self.nn[0]
        iy = dm[..., 1] % self.nn[1]
        iz = dm[..., 2] % self.nn[2]
        return arr_full[ix, iy, iz]


def bdg_omega2(basis, khat, Lam, mu, q, nlow=6):
    """lowest nlow omega^2 at Bloch vector q (3-vector). omega^2 are eigenvalues
    of L0(q)^{1/2}(L0(q)+2X(q))L0(q)^{1/2} (Hermitian, PSD ground state)."""
    NG = basis.NG
    m = basis.m                          # (NG,3) integer triples
    G = basis.G                          # (NG,3) cartesian
    q = np.asarray(q, float)
    # pairwise integer differences
    dm = m[:, None, :] - m[None, :, :]   # (NG,NG,3)
    rho_d = basis.coef(basis.rho_full, dm)          # rho_{a-b}
    phi_d = basis.coef(basis.phi_full, dm)          # phi_{a-b}
    # |G_a - G_b| for the Hartree kernel argument
    Gdiff = (dm[..., 0, None]*basis.Binv[:, 0] + dm[..., 1, None]*basis.Binv[:, 1]
             + dm[..., 2, None]*basis.Binv[:, 2])   # (NG,NG,3)
    absGd = np.sqrt((Gdiff**2).sum(-1))
    Uhat_Gd = khat(absGd.ravel()).reshape(absGd.shape)
    L0 = Lam*Uhat_Gd*rho_d               # full Hartree matrix (incl. diagonal)
    qa = q[None, :] + G
    L0 = L0 + np.diag(0.5*(qa*qa).sum(1) - mu)   # add kinetic - mu on diagonal
    # X(q) = Lam * W diag(Uhat(|q+G_P|)) W^H,  W_{a,P}=phi_{a-P}
    W = phi_d
    Uq = khat(np.sqrt(((q[None, :] + G)**2).sum(1)))
    X = Lam*(W*Uq[None, :]) @ W.conj().T
    L0 = 0.5*(L0 + L0.conj().T)
    X = 0.5*(X + X.conj().T)
    A_plus = L0 + 2*X
    w, V = np.linalg.eigh(L0)
    sq = (V*np.sqrt(np.clip(w, 1e-12, None))) @ V.conj().T
    Mmat = sq @ A_plus @ sq
    Mmat = 0.5*(Mmat + Mmat.conj().T)
    ev = np.linalg.eigvalsh(Mmat)
    return np.sort(ev.real)[:nlow]


def relax_truncated(cell, kg, Lam, gcut, psi0, dt=0.008, itmax=15000, restol=1e-9):
    """relax the GP ground state INSIDE the plane-wave cutoff |G|<=gcut so that
    psi0 is exactly stationary in the BdG basis (-> L0 has an exact zero mode and
    L0+2X is PSD for a genuine minimum). Returns psi, mu, e, res."""
    mask = (cell.Kmag <= gcut)
    psi = np.fft.ifftn(np.fft.fftn(psi0)*mask).real
    psi /= np.sqrt((psi*psi).mean())
    K2 = cell.K2; denom = 1.0 + dt*0.5*K2
    e_prev = np.inf
    for it in range(1, itmax+1):
        n = psi*psi
        conv = np.fft.ifftn(kg*np.fft.fftn(n)).real
        Hpsi = np.fft.ifftn(0.5*K2*np.fft.fftn(psi)).real + Lam*conv*psi
        mu = (psi*Hpsi).mean()/(psi*psi).mean()
        rhs = np.fft.fftn((1.0+dt*mu)*psi - dt*Lam*conv*psi)*mask
        psi = np.fft.ifftn(rhs/denom).real
        psi = np.fft.ifftn(np.fft.fftn(psi)*mask).real
        psi /= np.sqrt((psi*psi).mean())
        if it % 50 == 0:
            e = C.energy(cell, kg, Lam, psi)
            if abs(e-e_prev) < 1e-13*max(1, abs(e)):
                break
            e_prev = e
    n = psi*psi
    conv = np.fft.ifftn(kg*np.fft.fftn(n)).real
    Hpsi = np.fft.ifftn(0.5*K2*np.fft.fftn(psi)).real + Lam*conv*psi
    mu = (psi*Hpsi).mean()/(psi*psi).mean()
    r = Hpsi - mu*psi
    res = np.sqrt((r*r).mean())/abs(mu)
    return psi, float(mu), float(C.energy(cell, kg, Lam, psi)), float(res)


def acoustic_branches(basis, khat, Lam, mu, direction, qmags, nlow=5):
    """omega(|q|) for the lowest nlow branches along a Cartesian direction.
    Returns dict with per-|q| omegas and linear slopes (through origin, LSQ)."""
    d = np.asarray(direction, float); d = d/np.linalg.norm(d)
    W = []
    for qm in qmags:
        ev = bdg_omega2(basis, khat, Lam, mu, qm*d, nlow=nlow)
        W.append(np.sqrt(np.clip(ev, 0.0, None)))
    W = np.array(W)                        # (nq, nlow)
    qs = np.array(qmags)
    slopes = (qs @ W)/(qs @ qs)            # slope through origin per branch
    return dict(direction=[float(x) for x in d], qmags=list(qs),
                omegas=[[float(x) for x in row] for row in W],
                slopes=[float(s) for s in slopes])
    """C-NEG: single-plane-wave basis reproduces analytic uniform Bogoliubov."""
    # psi0 = 1 on a trivial cell
    H = np.eye(3)*3.0
    n = (8, 8, 8)
    psi0 = np.ones(n)
    mu = Lam*khat(np.array([0.0]))[0]
    basis = PWBasis(H, psi0, gcut=0.1)   # only G=0
    out = []
    for qmag in [0.5, 1.0, 2.0, 5.4486, 8.0]:
        q = np.array([qmag, 0, 0])
        ev = bdg_omega2(basis, khat, Lam, mu, q, nlow=1)
        w2_num = ev[0]
        w2_an = (qmag**2/2)*(qmag**2/2 + 2*Lam*khat(np.array([qmag]))[0])
        out.append((qmag, w2_num, w2_an, abs(w2_num-w2_an)))
    return out
