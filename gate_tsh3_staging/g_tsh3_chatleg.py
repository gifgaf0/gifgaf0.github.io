#!/usr/bin/env python3
"""
G-TSH3 chat leg -- kernel-set extension (GEM-{3,4,8} + cap-p2) on the p6m GP supersolid.
Executed under the LOCKED pre-registration G_TSH3_STAGING_MEMO.md
md5 dab46b332b83997d34f9e4ca64c07a4d (lock re-verified at execution start).

From-scratch implementation (TSH1/TSH2 chat solvers not imported).
Substrate units hbar = m = rho0 = 1 throughout (T4). No physical-speed target,
no observational string, no arm threshold appears in this file (T1); the arm
map lives only in the quarantined mapper, run last.

Phases (CLI):  p0a  p0b  p1 <kernel>  p2 <kernel>  p3w <point>  p3mu <kernel>
Checkpoints accumulate in gtsh3_results.json.
"""
import sys, json, os
import numpy as np
from scipy.special import j0, j1, jv
from scipy.integrate import quad
from scipy.optimize import minimize, minimize_scalar
from scipy.interpolate import CubicSpline
from scipy.linalg import eigh

# ---------------- T1 self-grep (every invocation) ----------------
FORBIDDEN = ["299792458", "2.998e8", "GW170817", "golden", "1.6180",
             "0.61803", "0.381966", "theta_1", "theta_2"]
def t1_selfgrep():
    src = open(os.path.abspath(__file__), "rb").read().decode()
    body = src.split("def t1_selfgrep")[1]
    for s in FORBIDDEN:
        assert s not in body, f"T1 VIOLATION: forbidden string {s!r} present"
    print("[T1] self-grep clean")
t1_selfgrep()

NASSERT = [0]
def A(cond, msg):
    assert cond, msg
    NASSERT[0] += 1

RESULTS = "gtsh3_results.json"
def ckpt(key, val):
    d = json.load(open(RESULTS)) if os.path.exists(RESULTS) else {}
    d[key] = val
    json.dump(d, open(RESULTS, "w"), indent=1)

SQ3 = np.sqrt(3.0)

# ---------------- kernels: U(r) and Uhat(|k|) ----------------
def hankel(U, rmax, k):
    v, _ = quad(lambda r: U(r) * j0(k * r) * r, 0.0, rmax, limit=600)
    return 2 * np.pi * v

# H-2 instrument fix (July 21): adaptive quad is oscillation-unsafe at high k
# (hundreds of J0 periods over the support -> garbage table values -> spurious
# short-wavelength attraction -> solver collapse; caught at P0b' pre-use, no
# recorded quantity affected; analytic kernels untouched). Replacement:
# per-k integration subdivided at the zeros of J0(kr), 12-pt Gauss-Legendre
# per subinterval (integrand smooth there); k=0 handled without oscillation.
_GLX, _GLW = np.polynomial.legendre.leggauss(12)
def hankel_table(U, rmax, ks):
    from scipy.special import jn_zeros
    nz = int(np.ceil(ks.max() * rmax / np.pi)) + 4
    z = np.concatenate([[0.0], jn_zeros(0, nz)])
    out = np.empty_like(ks)
    for i, k in enumerate(ks):
        if k < 1e-9:
            edges = np.linspace(0.0, rmax, 33)
        else:
            edges = z[z < k * rmax] / max(k, 1e-300)
            edges = np.append(edges, rmax)
        aa, bb = edges[:-1], edges[1:]
        mid = 0.5 * (aa + bb)[:, None]; half = 0.5 * (bb - aa)[:, None]
        r = mid + half * _GLX[None, :]
        w = half * _GLW[None, :]
        out[i] = 2 * np.pi * float(np.sum(w * U(r) * j0(k * r) * r))
    return out

def _validate_table_builder():
    ks = np.concatenate([np.linspace(0.01, 30, 40), np.linspace(30, 419, 60)])
    got = hankel_table(lambda r: np.ones_like(r) * (r < 1.0), 1.0, ks)
    ref = 2 * np.pi * j1(ks) / ks
    err = float(np.max(np.abs(got - ref)))
    A(err < 1e-9, f"hankel_table vs analytic step: max err {err:.2e}")
    print(f"[hankel_table] validated vs analytic step, max err {err:.2e}")

class Kernel:
    def __init__(self, name):
        self.name = name
        if name == "step":
            self.Uh = lambda k: np.where(np.asarray(k) < 1e-9, np.pi,
                        2*np.pi*j1(np.maximum(k, 1e-9))/np.maximum(k, 1e-9))
        elif name == "cap_p1":
            self.Uh = lambda k: np.where(np.asarray(k) < 1e-6, np.pi/2,
                        4*np.pi*jv(2, np.maximum(k, 1e-6))/np.maximum(k, 1e-6)**2)
        elif name == "cap_p2":
            self.Uh = lambda k: np.where(np.asarray(k) < 1e-6, np.pi/3,
                        16*np.pi*jv(3, np.maximum(k, 1e-6))/np.maximum(k, 1e-6)**3)
        else:
            tab = f"uhat_{name}_v2.npz"   # v2: oscillation-safe builder (H-2)
            if os.path.exists(tab):
                z = np.load(tab); ks, uk = z["ks"], z["uk"]
            else:
                if name.startswith("gem"):
                    p = float(name[3:]); U = lambda r: np.exp(-r**p)
                    rmax = {3.0: 6.0, 4.0: 5.0, 8.0: 3.0}[p]
                elif name.startswith("gamma"):
                    p = float(name[5:]); U = lambda r: 1.0/(1.0 + r**p); rmax = 14.0
                else:
                    raise ValueError(name)
                _validate_table_builder()
                ks = np.linspace(0.0, 420.0, 4200)
                uk = hankel_table(U, rmax, ks)
                np.savez(tab, ks=ks, uk=uk)
            sp = CubicSpline(ks, uk)
            self.Uh = lambda k, sp=sp: sp(np.clip(k, 0.0, 419.9))

# ---------------- oblique p6m cell ----------------
class Cell:
    """Triangular cell a1=a(1,0), a2=a(1/2,SQ3/2)+shear; n x n grid, fractional coords."""
    def __init__(self, a, n, shear=0.0):
        self.a, self.n = a, n
        a1 = np.array([a, 0.0]); a2 = np.array([a/2 + shear*a, a*SQ3/2])
        Amat = np.stack([a1, a2], axis=1)
        B = 2*np.pi*np.linalg.inv(Amat).T
        self.b1, self.b2 = B[:, 0], B[:, 1]
        m = np.fft.fftfreq(n, d=1.0/n)
        M1, M2 = np.meshgrid(m, m, indexing="ij")
        self.M1, self.M2 = M1.astype(int), M2.astype(int)
        self.Gx = M1*self.b1[0] + M2*self.b2[0]
        self.Gy = M1*self.b1[1] + M2*self.b2[1]
        self.G2 = self.Gx**2 + self.Gy**2
        self.area = abs(np.linalg.det(Amat))

def meanfield(cell, ker, g, rho):
    rG = np.fft.fft2(rho) / cell.n**2
    return np.real(np.fft.ifft2(ker.Uh(np.sqrt(cell.G2)) * rG * cell.n**2)) * g

def energy_mu_res(cell, ker, g, psi):
    n2 = cell.n**2
    pG = np.fft.fft2(psi) / n2
    kin = np.real(np.sum(cell.G2 * np.abs(pG)**2)) / 2.0
    rho = psi**2
    rG = np.fft.fft2(rho) / n2
    eint = 0.5 * g * np.real(np.sum(ker.Uh(np.sqrt(cell.G2)) * np.abs(rG)**2))
    Phi = meanfield(cell, ker, g, rho)
    Hpsi = np.real(np.fft.ifft2(cell.G2/2.0 * pG * n2)) + Phi * psi
    mu = float(np.mean(psi * Hpsi))
    res = float(np.sqrt(np.mean((Hpsi - mu*psi)**2)) / max(abs(mu), 1e-12))
    return kin + eint, mu, res, Hpsi

def solve_state(cell, ker, g, psi0=None, seed=None, deep=False):
    n = cell.n
    if psi0 is None:
        rng = np.random.default_rng(seed if seed is not None else 0)
        # D-2 (July 21, pre-P1, author-ratified): amp 0.4 -> 3.0. At marginal
        # first-passing points (gamma8@20 class: uniform locally stable below
        # g_c) small-amplitude inits fall into the uniform basin. Hex-triad
        # control confirmed the crystal basin exists (e=34.782937 < e_unif
        # =34.894320). Larger amp is basin-diagnostic only; the accepted state
        # is still an unconstrained stationary point at res<=1e-12.
        psi0 = 1.0 + 3.0*rng.standard_normal((n, n))
    def norm(p): return p / np.sqrt(np.mean(p**2))
    psi = norm(psi0.copy())
    def f_and_g(x):
        phi = x.reshape(n, n); s = 1.0/np.sqrt(np.mean(phi**2)); p = phi*s
        e, mu, _, Hp = energy_mu_res(cell, ker, g, p)
        grad = s * (2.0/n**2) * (Hp - mu*p)
        return e, grad.ravel()
    r = minimize(f_and_g, psi.ravel(), jac=True, method="L-BFGS-B",
                 options=dict(maxiter=4000, ftol=1e-16, gtol=1e-12))
    psi = norm(r.x.reshape(n, n))
    # H-3 (July 21): forward-Euler polish (dt=2e-3) is spectrally unstable at
    # this grid stiffness (dt*lam_max ~ 16); whenever L-BFGS exits unconverged
    # the map diverges to a seed-independent attractor (observed e=3053.417...
    # identical across random seeds at gamma8@20). Replacement: Sobolev-
    # preconditioned exact-gradient descent, P = (G^2/2 + max(|mu|,1))^-1 in
    # k-space. No operator splitting -> no Trotter bias -> Ward-safe (the TSH1
    # H3 lesson). Loop is inert when the residual is already at target, so all
    # previously recorded step results are unaffected.
    tgt = 1e-12 if deep else 1e-6
    iters = 20000 if deep else 6000
    dt = 0.6
    for it in range(iters):
        e, mu, res, Hp = energy_mu_res(cell, ker, g, psi)
        if res <= tgt: break
        gG = np.fft.fft2(Hp - mu*psi)
        pre = np.real(np.fft.ifft2(gG / (cell.G2/2.0 + max(abs(mu), 1.0))))
        psi = norm(psi - dt*pre)
    e, mu, res, _ = energy_mu_res(cell, ker, g, psi)
    return psi, e, mu, res

def center_on_peak(cell, psi):
    i, j = np.unravel_index(np.argmax(psi**2), psi.shape)
    pG = np.fft.fft2(psi) / cell.n**2
    frac = np.array([i, j]) / cell.n
    phase = np.exp(2j*np.pi*(cell.M1*frac[0] + cell.M2*frac[1]))
    out = np.real(np.fft.ifft2(pG*phase*cell.n**2))
    if out.flat[0] < 0: out = -out
    return out

MIR_K = lambda m1, m2: (m1, m1 - m2)   # mirror for q along Cartesian x (Gamma->K)
MIR_M = lambda m1, m2: (m1 - m2, -m2)  # mirror for q along b1-hat (Gamma->M)

def mirror_perm(cell, mir):
    n = cell.n
    iden = (np.mod(cell.M1, n)*n + np.mod(cell.M2, n)).ravel().astype(int)
    p1, p2 = mir(cell.M1, cell.M2)
    perm = (np.mod(p1, n)*n + np.mod(p2, n)).ravel().astype(int)
    return perm, iden

def apply_mirror(vec_flat, perm, iden):
    out = np.empty_like(vec_flat)
    out[perm] = vec_flat[iden]
    return out

def p6m_cert(cell, ker, g, psi, e, e_unif):
    psi_c = center_on_peak(cell, psi)
    rho = psi_c**2
    contrast = rho.max()/max(rho.min(), 1e-14)
    ok_e = e < e_unif - 1e-9*abs(e_unif)
    mres = []
    pG = (np.fft.fft2(psi_c)/cell.n**2).ravel()
    for mir in (MIR_K, MIR_M):
        perm, iden = mirror_perm(cell, mir)
        mres.append(float(np.max(np.abs(pG - apply_mirror(pG, perm, iden)))
                    / np.max(np.abs(pG))))
    return dict(crystal=bool(ok_e and contrast > 5.0), contrast=float(contrast),
                mirror_res=mres, psi=psi_c)

def astar_solve(ker, g, n, a_lo, a_hi, seed=0):
    memo = {}
    def e_of_a(a):
        a = float(a)
        if a not in memo:
            cell = Cell(a, n)
            psi, e, mu, res = solve_state(cell, ker, g, seed=seed)
            memo[a] = (cell, e, mu, res, psi)
        return memo[a][1]
    r = minimize_scalar(e_of_a, bounds=(a_lo, a_hi), method="bounded",
                        options=dict(xatol=2e-4))
    cell, e, mu, res, psi = memo[float(r.x)]
    return float(r.x), cell, psi, e, mu, res

# ---------------- BdG ----------------
def _wrap_index(cell):
    n = cell.n
    m1 = np.mod(cell.M1, n).ravel(); m2 = np.mod(cell.M2, n).ravel()
    d1 = np.mod(m1[:, None] - m1[None, :], n)
    d2 = np.mod(m2[:, None] - m2[None, :], n)
    return d1*n + d2

def _LX(cell, ker, g, psi, mu, qvec):
    n = cell.n; N = n*n
    Gx = cell.Gx.ravel() + qvec[0]; Gy = cell.Gy.ravel() + qvec[1]
    kin = (Gx**2 + Gy**2)/2.0
    Veff = meanfield(cell, ker, g, psi**2) - mu
    Vh = (np.fft.fft2(Veff)/N).ravel()
    ph = (np.fft.fft2(psi)/N).ravel()
    W = _wrap_index(cell)
    L = np.diag(kin) + Vh[W]
    Dk = ker.Uh(np.sqrt(Gx**2 + Gy**2))
    Amat = ph[W]
    X = g * (Amat.conj().T @ (Dk[:, None] * Amat))
    L = 0.5*(L + L.conj().T); X = 0.5*(X + X.conj().T)
    return L, X

def bdg_omegas(cell, ker, g, psi, mu, qvec, nev=6):
    L, X = _LX(cell, ker, g, psi, mu, qvec)
    lam, U = eigh(L)
    A(lam.min() > -1e-7, f"L not PSD: {lam.min():.3g}")
    S = (U * np.sqrt(np.clip(lam, 0, None))) @ U.conj().T
    Mm = S @ (L + 2*X) @ S
    Mm = 0.5*(Mm + Mm.conj().T)
    w2, V = eigh(Mm, subset_by_index=[0, nev-1])
    Sinv = (U * (1.0/np.sqrt(np.clip(lam, 1e-12, None)))) @ U.conj().T
    vecs = Sinv @ V
    return w2, vecs

def classify_speeds(cell, ker, g, psi, mu, direction, dq, jmax=6):
    if direction == "K":
        u = np.array([1.0, 0.0]); mir = MIR_K
    else:
        u = cell.b1/np.linalg.norm(cell.b1); mir = MIR_M
    perm, iden = mirror_perm(cell, mir)
    qs, wT, wL1, fT = [], [], [], []
    for j in range(1, jmax+1):
        w2, vecs = bdg_omegas(cell, ker, g, psi, mu, u*(j*dq), nev=6)
        A((w2 > -0.05).all(), f"F-NEG raw w2min {w2.min():.3g}")
        w = np.sqrt(np.clip(w2, 0, None))
        pars = []
        for k in range(vecs.shape[1]):
            s = vecs[:, k]; s = s/np.linalg.norm(s)
            pars.append(float(np.real(np.vdot(s, apply_mirror(s, perm, iden)))))
        pars = np.array(pars)
        idx = np.argsort(w)[:4]
        odd = [i for i in idx if pars[i] < -0.5]
        even = [i for i in idx if pars[i] > 0.5]
        A(len(odd) >= 1 and len(even) >= 2,
          f"F-CLS classifier parities {np.round(pars[idx],3)}")
        iT = odd[int(np.argmin(w[odd]))]
        ev = sorted(even, key=lambda i: w[i])[:2]
        qs.append(j*dq); wT.append(w[iT]); wL1.append(w[ev[1]]); fT.append(abs(pars[iT]))
    qs, wT, wL1 = map(np.array, (qs, wT, wL1))
    def zi(w): return float(np.sum(qs[1:6]*w[1:6]) / np.sum(qs[1:6]**2))
    def expo(w, i0, i1):
        x = np.log(qs[i0:i1+1]); y = np.log(w[i0:i1+1])
        return float(np.polyfit(x, y, 1)[0])
    return dict(cT=zi(wT), cL1=zi(wL1), fT=float(np.min(fT)),
                pT=[expo(wT, 1, 3), expo(wT, 3, 5)],
                pL1=[expo(wL1, 1, 3), expo(wL1, 3, 5)],
                wT=[float(x) for x in wT], wL1=[float(x) for x in wL1],
                qs=[float(x) for x in qs])

def ward_residual(cell, ker, g, psi, mu):
    L, X = _LX(cell, ker, g, psi, mu, np.zeros(2))
    ph = (np.fft.fft2(psi)/cell.n**2).ravel()
    out = []
    for Gc in (cell.Gx.ravel(), cell.Gy.ravel()):
        v = 1j*Gc*ph
        if np.linalg.norm(v) < 1e-14: continue
        r = (L + 2*X) @ v
        out.append(float(np.linalg.norm(r)/(np.linalg.norm(v)*max(abs(mu), 1e-12))))
    return max(out)

def certify(name, g, n=32, seed=0, a_hint=None):
    ker = Kernel(name)
    e_unif = 0.5*g*float(np.atleast_1d(ker.Uh(0.0))[0])
    lo, hi = (a_hint*0.75, a_hint*1.35) if a_hint else (0.8, 2.3)
    astar, cell, psi, e, mu, res = astar_solve(ker, g, n, lo, hi, seed=seed)
    cert = p6m_cert(cell, ker, g, psi, e, e_unif)
    if not cert["crystal"]:
        return dict(kernel=name, g=g, crystal=False, e=e, e_unif=e_unif,
                    contrast=cert["contrast"])
    psi = cert["psi"]
    ward = ward_residual(cell, ker, g, psi, mu)
    dq = 0.02*2*np.pi/astar  # D-1: halved vs first draft, anchor-calibrated pre-verdict
    dK = classify_speeds(cell, ker, g, psi, mu, "K", dq)
    dM = classify_speeds(cell, ker, g, psi, mu, "M", dq)
    cT = 0.5*(dK["cT"]+dM["cT"]); cL1 = 0.5*(dK["cL1"]+dM["cL1"])
    return dict(kernel=name, g=g, crystal=True, astar=astar, mu=mu, e=e, res=res,
                contrast=cert["contrast"], mirror_res=cert["mirror_res"], ward=ward,
                cT=cT, cL1=cL1, RT=cT/cL1, fT=min(dK["fT"], dM["fT"]),
                iso_T=abs(dK["cT"]-dM["cT"])/cT, iso_L=abs(dK["cL1"]-dM["cL1"])/cL1,
                pT=dK["pT"]+dM["pT"], pL1=dK["pL1"]+dM["pL1"],
                dirs=dict(K=dK, M=dM))

def falsifier_gates(c):
    ok, notes = True, []
    if c["ward"] > 5e-3: ok = False; notes.append(f"F9 ward {c['ward']:.2e}")
    if c["res"] > 1e-6: notes.append(f"H-class residual floor {c['res']:.2e} (Ward re-check is the cure)")
    if not all(0.95 <= p <= 1.05 for p in c["pT"]): ok = False; notes.append(f"F-LIN T {np.round(c['pT'],3)}")
    if not all(0.95 <= p <= 1.05 for p in c["pL1"]): ok = False; notes.append(f"F-LIN L1 {np.round(c['pL1'],3)}")
    if c["iso_T"] > 0.02 or c["iso_L"] > 0.02: ok = False; notes.append(f"F-ISO {c['iso_T']:.3%}/{c['iso_L']:.3%}")
    if c["fT"] < 0.95: ok = False; notes.append(f"F-CLS fT {c['fT']:.3f}")
    return ok, notes

# ---------------- phases ----------------
def p0a():
    ker = Kernel("step"); g = 8.0; a = 1.45; n = 32
    cell = Cell(a, n); psi = np.ones((n, n)); mu = g*float(np.atleast_1d(ker.Uh(0.0))[0])
    errs, odd_gapless = [], 0
    for (dirn, mir) in (("K", MIR_K), ("M", MIR_M)):
        u = np.array([1.0, 0.0]) if dirn == "K" else cell.b1/np.linalg.norm(cell.b1)
        perm, iden = mirror_perm(cell, mir)
        for j in (1, 3, 5):
            q = u*(j*0.05*2*np.pi/a)
            w2, vecs = bdg_omegas(cell, ker, g, psi, mu, q, nev=4)
            kq = float(np.linalg.norm(q)); ek = kq*kq/2
            ana = np.sqrt(max(ek*(ek + 2*g*float(np.atleast_1d(ker.Uh(kq))[0])), 0.0))
            errs.append(abs(np.sqrt(max(w2[0], 0.0)) - ana)/max(ana, 1e-12))
            for k in range(4):
                s = vecs[:, k]/np.linalg.norm(vecs[:, k])
                par = float(np.real(np.vdot(s, apply_mirror(s, perm, iden))))
                if par < -0.5 and w2[k] < 0.05*ek:
                    odd_gapless += 1
    A(max(errs) < 1e-6, f"C-NEG analytic mismatch {max(errs):.2e}")
    A(odd_gapless == 0, "C-NEG odd gapless present")
    kspr = mspr = aa = 1.0
    nbrs = [aa*np.array([np.cos(t), np.sin(t)]) for t in np.arange(6)*np.pi/3]
    def Dyn(q):
        D = np.zeros((2, 2), complex)
        for dv in nbrs:
            D += (kspr/mspr)*(1 - np.exp(1j*np.dot(q, dv)))*np.outer(dv, dv)/aa**2
        return 0.5*(D + D.conj().T)
    sp, sp_fq = [], []
    for th in (0.0, np.pi/6):
        u = np.array([np.cos(th), np.sin(th)])
        # exact q->0 acoustic matrix derived in-file: 1-exp(iq.d) -> (q.d)^2/2 (odd term cancels over the star)
        Ac = np.zeros((2, 2))
        for dv in nbrs:
            Ac += 0.5*(kspr/mspr)*np.dot(u, dv)**2*np.outer(dv, dv)/aa**2
        c2s, V = np.linalg.eigh(Ac)
        pol = [abs(np.dot(V[:, i], u)) for i in range(2)]
        iL = int(np.argmax(pol)); iT = 1 - iL
        A(pol[iT] < 1e-9, "C-POS classifier: T not transverse (exact)")
        sp.append(float(np.sqrt(c2s[iL]/c2s[iT])))
        qs = np.array([0.02, 0.03, 0.04]); wl, wt = [], []
        for qm in qs:
            w2, Vf = np.linalg.eigh(Dyn(u*qm))
            polf = [abs(np.dot(np.real(Vf[:, i]), u)) + abs(np.dot(np.imag(Vf[:, i]), u))
                    for i in range(2)]
            jL = int(np.argmax(polf)); jT = 1 - jL
            wl.append(np.sqrt(max(w2[jL], 0))); wt.append(np.sqrt(max(w2[jT], 0)))
        sp_fq.append(float(np.polyfit(qs, wl, 1)[0]/np.polyfit(qs, wt, 1)[0]))
    A(all(abs(s - SQ3) < 1e-9 for s in sp), f"C-POS exact ratio {sp}")
    A(all(abs(s - SQ3) < 1e-3 for s in sp_fq), f"C-POS finite-q corroboration {sp_fq}")
    ckpt("P0a", dict(cneg_maxerr=float(max(errs)), cpos_ratios=sp))
    print(f"[P0a] C-NEG max err {max(errs):.2e}; C-POS cL/cT = {sp} -> PASS")

ANCHOR_STEP22 = dict(astar=1.4575, mu=55.854, cT=5.7749, cL1=11.0453, RT=0.52284)  # read-only certified anchors

def p0b():
    c = certify("step", 22.0, a_hint=1.46)
    dev = {k: abs(c[k]-v)/v for k, v in ANCHOR_STEP22.items()}
    ckpt("P0b", dict(computed={k: float(c[k]) for k in ANCHOR_STEP22}, rel_dev=dev,
                     ward=c["ward"], fT=c["fT"], res=c["res"]))
    print("[P0b] step@22 anchor reproduction (read-only certified vs this leg):")
    for k, v in ANCHOR_STEP22.items():
        print(f"   {k:5s} certified {v:9.4f}  this-leg {c[k]:9.4f}  rel {dev[k]:.2e}")
    print(f"   ward {c['ward']:.2e}  fT {c['fT']:.3f}  res {c['res']:.1e}")

GC = dict(gem3=71.87, gem4=39.19, gem8=22.02, cap_p2=451.24,
          gamma8=22.75, cap_p1=105.46, step=14.74)          # diagnostic g_c (locked memo section 4/8)
AHINT = dict(gem3=1.46, gem4=1.42, gem8=1.38, cap_p2=0.96,
             gamma8=1.55, cap_p1=1.18, step=1.45)

def first_passing(name):
    n = 32
    g = 5.0*np.ceil(GC[name]/5.0)
    hist = {}
    def run(gv):
        if gv not in hist:
            hist[gv] = certify(name, float(gv), a_hint=AHINT[name])
        return hist[gv]
    c = run(g)
    while not c.get("crystal"):
        g += 5.0; c = run(g)
    while g - 5.0 > 0:
        c2 = run(g - 5.0)
        if c2.get("crystal"):
            g -= 5.0; c = c2
        else:
            break
    cfail = run(g - 5.0)
    A(not cfail.get("crystal"), f"deep-fail bracket violated at {g-5:.0f}")
    cell = Cell(c["astar"], n); ker = Kernel(name)
    # D-2 tier-2 rule: three random-init deep solves at fixed (g*, a*).
    # Accept iff >=2/3 crystallize (e < e_unif, contrast > 5) AND the
    # crystallized subset is machine-identical (rel spread <= 1e-8 on
    # (e, mu, rho_max)). Uniform landings are logged, not silently dropped.
    ckpt(f"P1scan_{name}", dict(gstar=float(g), astar=c["astar"], mu=c["mu"],
                                fail_bracket=float(g - 5.0)))
    e_unif = 0.5*float(g)*float(np.atleast_1d(ker.Uh(0.0))[0])
    detail, cry, unif_seeds = [], [], []
    for sd in (1, 2, 3):
        psi, e, mu, res = solve_state(cell, ker, float(g), seed=sd, deep=True)
        pc = p6m_cert(cell, ker, float(g), psi, e, e_unif)
        row = dict(seed=sd, e=float(e), mu=float(mu), res=float(res),
                   rhomax=float((psi**2).max()), crystal=bool(pc["crystal"]),
                   contrast=float(pc["contrast"]),
                   mirror_res=[float(x) for x in pc["mirror_res"]])
        detail.append(row)
        print(f"  [tier2 {name} seed {sd}] e={e:.12g} mu={mu:.12g} "
              f"rhomax={row['rhomax']:.8g} res={res:.1e} crystal={row['crystal']} "
              f"mir={np.round(pc['mirror_res'],3)}")
        if pc["crystal"]:
            cry.append(row)
        else:
            unif_seeds.append(sd)
    # dual comparator, diagnosis-grade: full = (e, mu, rhomax); inv = (e, mu)
    # (rhomax on a discrete grid is NOT translation-invariant; continuum
    #  registration of the crystal relative to grid points moves it)
    full = np.array([[r["e"], r["mu"], r["rhomax"]] for r in cry])
    inv = np.array([[r["e"], r["mu"]] for r in cry])
    t2_full = float(np.max(np.abs(full - full[0]) / np.abs(full[0]))) if len(cry) else np.inf
    t2_inv = float(np.max(np.abs(inv - inv[0]) / np.abs(inv[0]))) if len(cry) else np.inf
    ckpt(f"P1tier2_{name}", dict(detail=detail, t2_full=t2_full, t2_inv=t2_inv,
                                 ncrys=len(cry), uniform_seeds=unif_seeds))
    A(len(cry) >= 2, f"tier-2 D-2 fail: only {len(cry)}/3 seeds crystallize")
    # H-4 (self-caught, first tier-2 invocation, gem8): original comparator
    # included rhomax, which is not translation-invariant on the discrete grid
    # (continuum crystal registration moves the sampled peak value; observed
    # 5.03e-03 rhomax spread with (e,mu) spread 3.84e-14 on the SAME state).
    # Acceptance is therefore asserted on the translation-invariant scalars
    # (e, mu); rhomax remains recorded in the detail block for audit.
    t2 = t2_inv
    A(t2 <= 1e-8, f"tier-2 D-2 fail: invariant (e,mu) spread {t2:.2e} "
                  f"(full-tuple spread incl. rhomax {t2_full:.2e})")
    ckpt(f"P1_{name}", dict(gstar=float(g), astar=c["astar"], mu=c["mu"],
                            contrast=c["contrast"], tier2_maxrel=t2,
                            tier2_ncrys=len(cry), tier2_uniform_seeds=unif_seeds,
                            fail_bracket=float(g - 5.0)))
    print(f"[P1 {name}] g*={g:.0f}  a*={c['astar']:.5f}  mu={c['mu']:.3f}  "
          f"contrast={c['contrast']:.1f}  tier2 {t2:.2e} ({len(cry)}/3 cryst, "
          f"unif seeds {unif_seeds})  (deep fail at {g-5:.0f} verified)")

def p2(name):
    d = json.load(open(RESULTS)); p1 = d[f"P1_{name}"]
    c = certify(name, p1["gstar"], a_hint=p1["astar"])
    ok, notes = falsifier_gates(c)
    c40 = certify(name, p1["gstar"], n=40, a_hint=c["astar"])
    conv = max(abs(c40["cT"]-c["cT"])/c["cT"], abs(c40["cL1"]-c["cL1"])/c["cL1"])
    # H-5 (self-caught pre-use): leg had 1e-4 here; locked memo section 6 says
    # F-CONV <= 5e-6. Corrected before any P2 invocation.
    if conv > 5e-6:
        ok = False; notes.append(f"F-CONV {conv:.2e}")
    status = "CERTIFIED" if ok else "EXCLUDED"
    ckpt(f"P2_{name}", dict(status=status, notes=notes, RT=c["RT"], cT=c["cT"],
                            cL1=c["cL1"], fT=c["fT"], ward=c["ward"], res=c["res"],
                            iso_T=c["iso_T"], iso_L=c["iso_L"], pT=c["pT"],
                            pL1=c["pL1"], conv=conv, astar=c["astar"], mu=c["mu"],
                            RT40=c40["RT"]))
    print(f"[P2 {name}] {status}  RT={c['RT']:.5f} (cT={c['cT']:.4f}, cL1={c['cL1']:.4f})")
    print(f"   fT={c['fT']:.3f} ward={c['ward']:.1e} res={c['res']:.1e} "
          f"iso={c['iso_T']:.2%}/{c['iso_L']:.2%} conv(n40)={conv:.1e}")
    print(f"   pT={['%.3f' % p for p in c['pT']]}  pL1={['%.3f' % p for p in c['pL1']]}")
    if notes: print("   notes:", "; ".join(notes))

def p3w(point):
    r0 = 1.5
    gw = r0*GC[point]
    if point == "step":
        print(f"[P3w step] g_w={gw:.1f} within 0.5 of certified g=22 -> REUSE rule; logged")
        ckpt("P3w_step", dict(reuse=True, RT=ANCHOR_STEP22["RT"], gw=gw))
        return
    c = certify(point, float(gw), a_hint=AHINT[point])
    if not c.get("crystal"):
        ckpt(f"P3w_{point}", dict(dropped=True, reason="no crystallization", gw=gw))
        print(f"[P3w {point}] DROPPED (no crystal at g_w={gw:.1f})")
        return
    ok, notes = falsifier_gates(c)
    # memo section 8: "same falsifier bar" — taken literally, incl. F-CONV n40
    c40 = certify(point, float(gw), n=40, a_hint=c["astar"])
    conv = max(abs(c40["cT"]-c["cT"])/c["cT"], abs(c40["cL1"]-c["cL1"])/c["cL1"])
    if conv > 5e-6:
        ok = False; notes.append(f"F-CONV {conv:.2e}")
    ckpt(f"P3w_{point}", dict(gw=float(gw), RT=c["RT"], certified=bool(ok),
                              notes=notes, ward=c["ward"], fT=c["fT"],
                              conv=conv, astar=c["astar"]))
    print(f"[P3w {point}] g_w={gw:.1f}  RT={c['RT']:.5f}  "
          f"{'ok' if ok else 'DROP: ' + '; '.join(notes)}")

def p3mu(name):
    d = json.load(open(RESULTS)); p1 = d[f"P1_{name}"]; p2r = d[f"P2_{name}"]
    if p2r["status"] != "CERTIFIED":
        print(f"[P3mu {name}] kernel not certified; record-only skip")
        ckpt(f"P3mu_{name}", dict(skipped=True))
        return
    ker = Kernel(name); g = p1["gstar"]; a = p2r["astar"]; n = 32
    eps_list = [-0.06, -0.03, 0.0, 0.03, 0.06]
    # base state first; each sheared solve continues from the unsheared
    # crystal (adiabatic continuation for a static modulus). Prevents
    # spurious uniform landings at marginal first-passing g, which would
    # fake mu_s ~ 0. Base must crystallize or the point aborts loudly.
    cell0 = Cell(a, n)
    base, e0, mu0, _ = solve_state(cell0, ker, g, seed=0)
    e_unif = 0.5*float(g)*float(np.atleast_1d(ker.Uh(0.0))[0])
    A(e0 < e_unif, f"P3mu {name}: base state failed to crystallize")
    es = []
    for eps in eps_list:
        cell = Cell(a, n, shear=eps)
        psi, e, mu, res = solve_state(cell, ker, g, psi0=base.copy())
        es.append(e)
    co = np.polyfit(eps_list, es, 2)
    mus = float(2*co[0])
    ratio = mus / (p2r["cT"]**2)
    flag = not (0.5 <= ratio <= 2.0)
    ckpt(f"P3mu_{name}", dict(mu_s=mus, ratio=float(ratio), WMU_BAND_flag=bool(flag)))
    print(f"[P3mu {name}] mu_s={mus:.4f}  mu_s/(rho cT^2)={ratio:.3f}"
          + ("  [W-MU-BAND flag]" if flag else ""))

if __name__ == "__main__":
    ph = sys.argv[1]
    if ph == "p0a": p0a()
    elif ph == "p0b": p0b()
    elif ph == "p1": first_passing(sys.argv[2])
    elif ph == "p2": p2(sys.argv[2])
    elif ph == "p3w": p3w(sys.argv[2])
    elif ph == "p3mu": p3mu(sys.argv[2])
    else: raise SystemExit("unknown phase")
    print(f"[asserts this invocation: {NASSERT[0]}]")
