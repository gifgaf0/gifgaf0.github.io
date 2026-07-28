#!/usr/bin/env python3
"""
G-TSH4 Phase 0 — 3D structure determination (chat leg, from scratch).
Bound to G_TSH4_EXECUTION_PREREGISTRATION.md md5 e66b964d4467fcb9a5f328ef0db80a35.
Model: e = <0.5|grad psi|^2> + (Lam/2)<n (U*n)>, <n>=1, hbar=m=R=1. Single control parameter Lam.
"""
import numpy as np, hashlib, sys, os
from numpy.fft import fftn, ifftn, fftfreq
from scipy.special import gamma as Gamma
from scipy.interpolate import CubicSpline

# ---------------- T1 self-grep guard ----------------
# H-protocol note (self-caught, V4.72-era): the first version of this guard scanned the whole
# source INCLUDING its own FORBIDDEN literal list, so it fired on itself. Fixed by excising the
# delimited guard block before scanning. NOT fixed by fragment-assembly, which T1 forbids.
# T1-GUARD-BEGIN
FORBIDDEN = ["299792458", "2.99792458", "GW170817", "137.035", "1.618033", "6.674", "6.62607"]
# T1-GUARD-END
def t1_selfgrep(paths):
    for p in paths:
        src = open(p, encoding="utf-8").read()
        if "# T1-GUARD-BEGIN" in src:
            head, rest = src.split("# T1-GUARD-BEGIN", 1)
            _, tail = rest.split("# T1-GUARD-END", 1)
            src = head + tail
        for f in FORBIDDEN:
            if f in src:
                raise SystemExit(f"T1 VIOLATION: '{f}' in {p}")
    print("[T1] self-grep PASS (no forbidden physical-constant strings)")

# ---------------- kernels: analytic k-space ----------------
def utilde_step(k):
    """3D FT of Theta(1-r): 4*pi*(sin k - k cos k)/k^3, series for small k."""
    k = np.asarray(k, dtype=float)
    out = np.empty_like(k)
    small = k < 1e-3
    ks = k[small]
    out[small] = 4*np.pi*(1.0/3.0 - ks**2/30.0 + ks**4/840.0)
    kb = k[~small]
    out[~small] = 4*np.pi*(np.sin(kb) - kb*np.cos(kb))/kb**3
    return out

_GEM8_TABLE = None
def _build_gem8_table(kmax=500.0, nk=20001, nr=8000, rmax=3.0):
    """Utilde(k) = (4pi/k) int_0^inf r e^{-r^8} sin(kr) dr, Gauss-Legendre in r, dense k table."""
    x, w = np.polynomial.legendre.leggauss(nr)
    r = 0.5*rmax*(x+1.0); wr = 0.5*rmax*w
    f = r*np.exp(-r**8)*wr                      # (nr,)
    kk = np.linspace(0.0, kmax, nk)
    vals = np.empty_like(kk)
    vals[0] = 4*np.pi*(1.0/8.0)*Gamma(3.0/8.0)  # k->0 limit: 4pi int r^2 e^{-r^8} dr
    chunk = 200
    for i0 in range(1, nk, chunk):
        i1 = min(i0+chunk, nk)
        kc = kk[i0:i1][:, None]
        vals[i0:i1] = (4*np.pi/kk[i0:i1])*np.sum(f[None, :]*np.sin(kc*r[None, :]), axis=1)
    return CubicSpline(kk, vals)

def utilde_gem8(k):
    global _GEM8_TABLE
    if _GEM8_TABLE is None:
        _GEM8_TABLE = _build_gem8_table()
    return _GEM8_TABLE(np.asarray(k, dtype=float))

KERNELS = {"step": utilde_step, "gem8": utilde_gem8}

# ---------------- roton threshold Lam_c ----------------
def lambda_c(kernel, kmax=60.0):
    f = KERNELS[kernel]
    k = np.linspace(1e-6, kmax, 400001)
    u = f(k)
    neg = u < 0
    if not neg.any():
        raise SystemExit(f"{kernel}: Utilde never negative -> no roton instability")
    cand = -k[neg]**2/(4.0*u[neg])
    i = np.argmin(cand)
    kn, cn = k[neg], cand
    # local parabolic refine
    j = np.searchsorted(k, kn[i])
    lo, hi = max(j-50, 1), min(j+50, len(k)-1)
    kk = np.linspace(k[lo], k[hi], 20001)
    uu = f(kk); m = uu < 0
    c2 = -kk[m]**2/(4.0*uu[m])
    jj = np.argmin(c2)
    return float(c2[jj]), float(kk[m][jj])

# ---------------- lattice cells and seeds ----------------
def cell_sites(structure, a, c):
    """Return (Lx,Ly,Lz), list of (x,y,z) droplet sites."""
    if structure in ("AA", "AB", "ABC"):
        Lx, Ly = a, a*np.sqrt(3.0)
        Lz = c
        base = [(0.0, 0.0), (a/2.0, a*np.sqrt(3.0)/2.0)]           # triangular lattice in rect cell
        if structure == "AA":
            shifts = [(0.0, 0.0)]
        elif structure == "AB":
            shifts = [(0.0, 0.0), (a/2.0, a*np.sqrt(3.0)/6.0)]
        else:
            shifts = [(0.0, 0.0), (a/2.0, a*np.sqrt(3.0)/6.0), (a, a*np.sqrt(3.0)/3.0)]
        nl = len(shifts)
        sites = []
        for il, (sx, sy) in enumerate(shifts):
            z = Lz*il/nl
            for (bx, by) in base:
                sites.append(((bx+sx) % Lx, (by+sy) % Ly, z))
        return (Lx, Ly, Lz), sites
    if structure == "FCC":
        L = a
        s = [(0,0,0), (0.5,0.5,0), (0.5,0,0.5), (0,0.5,0.5)]
        return (L, L, L), [(L*u, L*v, L*w) for (u,v,w) in s]
    if structure == "BCC":
        L = a
        s = [(0,0,0), (0.5,0.5,0.5)]
        return (L, L, L), [(L*u, L*v, L*w) for (u,v,w) in s]
    raise ValueError(structure)

def make_grid(Ls, dx_target):
    Ns = []
    for L in Ls:
        n = int(np.ceil(L/dx_target))
        n += n % 2                       # even
        while max(_factors(n)) > 5:      # keep FFT-friendly
            n += 2
        Ns.append(n)
    return tuple(Ns)

def _factors(n):
    f, d = [], 2
    while d*d <= n:
        while n % d == 0:
            f.append(d); n //= d
        d += 1
    if n > 1: f.append(n)
    return f or [1]

def build_ksq(Ls, Ns):
    kx = 2*np.pi*fftfreq(Ns[0], d=Ls[0]/Ns[0])
    ky = 2*np.pi*fftfreq(Ns[1], d=Ls[1]/Ns[1])
    kz = 2*np.pi*fftfreq(Ns[2], d=Ls[2]/Ns[2])
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    return KX**2 + KY**2 + KZ**2

def seed_droplets(Ls, Ns, sites, width_frac=0.16, contrast=6.0):
    xs = [np.linspace(0, Ls[i], Ns[i], endpoint=False) for i in range(3)]
    X, Y, Z = np.meshgrid(*xs, indexing="ij")
    amin = min(Ls[0], Ls[1], Ls[2])
    sig = width_frac*amin
    n = np.ones(Ns)
    for (sx, sy, sz) in sites:
        dxp = np.abs(X-sx); dxp = np.minimum(dxp, Ls[0]-dxp)
        dyp = np.abs(Y-sy); dyp = np.minimum(dyp, Ls[1]-dyp)
        dzp = np.abs(Z-sz); dzp = np.minimum(dzp, Ls[2]-dzp)
        n += contrast*np.exp(-(dxp**2+dyp**2+dzp**2)/(2*sig**2))
    n *= 1.0/n.mean()
    return np.sqrt(n)

# ---------------- energy and relaxation ----------------
def energy(psi, ksq, Ut, Lam):
    n = psi*psi
    npts = psi.size
    nk = fftn(n)
    conv = np.real(ifftn(Ut*nk))
    kin = np.real(np.sum(0.5*ksq*np.abs(fftn(psi))**2))/npts**2
    inter = 0.5*Lam*np.mean(n*conv)
    return kin + inter, conv

def relax(psi, ksq, Ut, Lam, dt=0.01, max_steps=20000, tol=1e-13, report=False):
    # H-protocol note (self-caught): first version used exp(-0.5*dt*ksq) applied TWICE, which
    # realises exp(-dt*k^2) instead of exp(-dt*k^2/2) -> effective kinetic operator doubled,
    # i.e. Lam_eff = Lam/2. At Lam = 2*Lam_c that sits exactly at threshold and every seeded
    # crystal melted to uniform. Detected by the modulation-contrast sanity check.
    ekin_half = np.exp(-0.25*dt*ksq)
    e_prev, _ = energy(psi, ksq, Ut, Lam)
    it = 0
    for it in range(1, max_steps+1):
        n = psi*psi
        conv = np.real(ifftn(Ut*fftn(n)))
        psi = psi*np.exp(-0.5*dt*Lam*conv)
        psi = np.real(ifftn(ekin_half*fftn(psi)*ekin_half))
        n = psi*psi
        conv = np.real(ifftn(Ut*fftn(n)))
        psi = psi*np.exp(-0.5*dt*Lam*conv)
        psi = np.abs(psi)
        psi *= 1.0/np.sqrt(np.mean(psi*psi))
        if it % 25 == 0:
            e, _ = energy(psi, ksq, Ut, Lam)
            if abs(e-e_prev) < tol*max(1.0, abs(e)):
                e_prev = e
                break
            e_prev = e
    e, _ = energy(psi, ksq, Ut, Lam)
    if report:
        print(f"      relaxed in {it} steps, e={e:.10f}")
    return psi, e, it

def structure_energy(structure, a, c, kernel, Lam, dx, dt=0.01, max_steps=20000,
                     tol=1e-13, psi0=None):
    Ls, sites = cell_sites(structure, a, c)
    Ns = make_grid(Ls, dx)
    ksq = build_ksq(Ls, Ns)
    Ut = KERNELS[kernel](np.sqrt(ksq))
    psi = seed_droplets(Ls, Ns, sites) if (psi0 is None or psi0.shape != Ns) else psi0.copy()
    psi, e, it = relax(psi, ksq, Ut, Lam, dt=dt, max_steps=max_steps, tol=tol)
    return e, psi, Ls, Ns, sites

# ---------------- controls ----------------
def c_neg_check(kernel, Lam, dx=0.06):
    """Uniform state must return e = (Lam/2)*Utilde(0)."""
    Ls = (1.7, 1.7, 1.7)
    Ns = make_grid(Ls, dx)
    ksq = build_ksq(Ls, Ns)
    Ut = KERNELS[kernel](np.sqrt(ksq))
    psi = np.ones(Ns)
    e, _ = energy(psi, ksq, Ut, Lam)
    e_exact = 0.5*Lam*float(KERNELS[kernel](np.array([0.0]))[0])
    return e, e_exact, abs(e-e_exact)/abs(e_exact)

# ---------------- structure verification ----------------
def bragg_signature(psi, Ls, Ns, nkeep=12):
    n = psi*psi
    nk = np.abs(fftn(n))/n.size
    kx = 2*np.pi*fftfreq(Ns[0], d=Ls[0]/Ns[0])
    ky = 2*np.pi*fftfreq(Ns[1], d=Ls[1]/Ns[1])
    kz = 2*np.pi*fftfreq(Ns[2], d=Ls[2]/Ns[2])
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    Kmag = np.sqrt(KX**2+KY**2+KZ**2)
    flat = nk.ravel(); km = Kmag.ravel()
    idx = np.argsort(flat)[::-1]
    out, seen = [], set()
    for i in idx:
        if km[i] < 1e-9: continue
        key = round(km[i], 3)
        if key in seen: continue
        seen.add(key); out.append((float(km[i]), float(flat[i])))
        if len(out) >= nkeep: break
    return out

def modulation_contrast(psi):
    n = psi*psi
    return float(n.max()), float(n.min())

if __name__ == "__main__":
    t1_selfgrep([os.path.abspath(__file__)])
    print("[core] module self-test")
    for kern in ("step", "gem8"):
        Lc, kstar = lambda_c(kern)
        print(f"  {kern}: Lam_c = {Lc:.6f}  at k* = {kstar:.4f}  (lattice spacing 2pi/k* = {2*np.pi/kstar:.4f})")
        Lam = 2.0*Lc
        e, ex, rel = c_neg_check(kern, Lam)
        print(f"  {kern}: C-NEG uniform e={e:.10f} exact={ex:.10f} rel.err={rel:.2e}")
