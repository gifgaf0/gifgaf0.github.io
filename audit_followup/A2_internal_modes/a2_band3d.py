#!/usr/bin/env python3
"""A2 / DR-A2-1 (first leg), 3D: the internal L_perp band of the 3D AB (hcp) crystal of record (G-TSH4 step kernel,
Lambda = 2 Lambda_c), built exactly as the two-leg-closed 3D first leg (jobB_3d.py): full-grid relax, then the in-basis
state converged by L-BFGS on the masked field (|G| <= 22). Internal frequencies = eigenvalues of
L0(q) = 1/2|q+G|^2 + Lam*Uhat*rho - mu in the same plane-wave basis (tsh4_routeD.PWBasis).
Reported: eps0 at Gamma (zero mode), the small-q exponent and the band mass along basal (x) and axial (z) directions.
The 3D superfluid fraction is computed independently by a relaxed phase twist (energy of the twisted ground state)."""
import sys, json, time, math, hashlib
import numpy as np
from scipy.optimize import minimize
REPO = "/home/claude/gifgaf0.github.io"
sys.path.insert(0, REPO + "/gtsh4_gate"); import tsh4_core as C, tsh4_routeD as D
assert hashlib.md5(open(REPO + "/audit_followup/A2_internal_modes/A2_PREREG.md", "rb").read()).hexdigest() == "fd2e95973de02d9a0e6d719cb579ccc0"
S3 = math.sqrt(3.0); GCUT = 22.0; PPL = 30
ev_ = lambda x: int(round(x)) + (int(round(x)) & 1)

def masked_tight(cell, kg, Lam, gcut, psi0, maxiter=6000):            # verbatim logic of lbc_bank/closure/jobB_3d.py
    mask = (cell.Kmag <= gcut); N = cell.N
    P = lambda f: np.fft.ifftn(np.fft.fftn(f)*mask).real
    def Hpsi(psi):
        n = psi*psi; conv = np.fft.ifftn(kg*np.fft.fftn(n)).real
        return np.fft.ifftn(0.5*cell.K2*np.fft.fftn(psi)).real + Lam*conv*psi
    def EG(u):
        U = P(u.reshape(cell.n)); s = 1.0/np.sqrt((U*U).mean()); psi = s*U
        Hp = Hpsi(psi); e = C.energy(cell, kg, Lam, psi); g = (2.0/N)*Hp
        gu = s*g - s*U*np.sum(U*g)/np.sum(U*U)
        return e, P(gu).ravel()
    u0 = P(psi0); u0 /= np.sqrt((u0*u0).mean())
    r = minimize(EG, u0.ravel(), jac=True, method="L-BFGS-B", options=dict(maxiter=maxiter, maxcor=30, ftol=1e-16, gtol=1e-15))
    U = P(r.x.reshape(cell.n)); psi = U/np.sqrt((U*U).mean())
    Hp = Hpsi(psi); mu = (psi*Hp).mean()/(psi*psi).mean()
    rp = P(Hp - mu*psi); return psi, float(mu), float(np.sqrt((rp*rp).mean())/abs(mu))

t0 = time.time()
ph = json.load(open(REPO + "/gtsh4_gate/tsh4_phase0_measurements.json"))
lc, kstar = C.lambda_c(C.step_khat, 40.0); Lam = 2*lc; khat = C.step_khat
a, c = ph['results']['step']['structures']['AB']['params']
H = np.diag([a, a*S3, c]).astype(float); sites = C.STRUCTURES['AB']['sites']
lens = np.diag(H); n = tuple(ev_(PPL*l) for l in lens)
cell = C.Cell(list(lens), n); kg = C.khat_grid(cell, khat)
psi = cell.seed(sites, 0.24*lens[0])
psi, e, resf, it, _ = C.relax(cell, kg, Lam, psi, dt=0.008, restol=1e-10)
psi, mu, resp = masked_tight(cell, kg, Lam, GCUT, psi)
print(f"[3D AB] a={a:.6f} c={c:.6f} Lam={Lam:.6f} grid={n}  mu={mu:.6f}  projected residual {resp:.2e}  ({time.time()-t0:.0f}s)", flush=True)
basis = D.PWBasis(H, psi, GCUT)
m = basis.m; G = basis.G
dm = m[:, None, :] - m[None, :, :]
rho_d = basis.coef(basis.rho_full, dm)
Gdiff = dm[..., 0, None]*basis.Binv[:, 0] + dm[..., 1, None]*basis.Binv[:, 1] + dm[..., 2, None]*basis.Binv[:, 2]
Hart = Lam*khat(np.sqrt((Gdiff**2).sum(-1)).ravel()).reshape(dm.shape[:2])*rho_d
Hart = 0.5*(Hart + Hart.conj().T)
def lowest(q, k=3):
    qa = np.asarray(q)[None, :] + G
    L0 = Hart + np.diag(0.5*(qa*qa).sum(1) - mu)
    return np.linalg.eigvalsh(L0)[:k]
out = dict(a=a, c=c, Lam=Lam, mu=mu, proj_residual=resp, NG=int(basis.NG), dirs={})
e0G = lowest([0, 0, 0])
print(f"   NG={basis.NG}  L_perp at Gamma: {e0G.round(6)}", flush=True)
for dname, dvec in (("basal_x", [1, 0, 0]), ("basal_y", [0, 1, 0]), ("axial_z", [0, 0, 1])):
    dvec = np.array(dvec, float); qs = np.array([0.01, 0.02, 0.04, 0.06, 0.08]); de = []
    for qm in qs:
        de.append(lowest(qm*dvec, 1)[0] - e0G[0])
    de = np.array(de); p = float(np.log(de[1]/de[0])/np.log(qs[1]/qs[0]))
    M = np.stack([qs**2, qs**4], 1); coef, *_ = np.linalg.lstsq(M, de, rcond=None)
    out["dirs"][dname] = dict(q=qs.tolist(), de=de.tolist(), p_small=p, A=float(coef[0]), mstar=float(1/(2*coef[0])))
    print(f"   {dname:8s} exponent p={p:.4f}  m*={1/(2*coef[0]):.4f}  m/m*={2*coef[0]:.6f}", flush=True)
# independent superfluid fraction: energy of the relaxed ground state with a Bloch twist k (E(k)-E(0) = 1/2 N f_s k^2)
def twisted_energy(kvec):
    mask = (cell.Kmag <= GCUT); N = cell.N
    kx, ky, kz = cell.KX + kvec[0], cell.KY + kvec[1], cell.KZ + kvec[2]
    K2t = kx*kx + ky*ky + kz*kz
    P = lambda f: np.fft.ifftn(np.fft.fftn(f)*mask)
    def unpack(u): return (u[:N] + 1j*u[N:]).reshape(cell.n)
    def EG(u):
        U = P(unpack(u)); nrm = np.sqrt((np.abs(U)**2).mean()); ps = U/nrm
        Hk = np.fft.ifftn(0.5*K2t*np.fft.fftn(ps)); dens = np.abs(ps)**2
        conv = np.fft.ifftn(kg*np.fft.fftn(dens)).real
        E = ((ps.conj()*Hk).real.mean() + 0.5*Lam*(conv*dens).mean())
        g = 2*(Hk + Lam*conv*ps)/N
        gU = (g - ps*np.sum((ps.conj()*g).real)/np.sum(np.abs(ps)**2))/nrm
        gU = P(gU)
        return float(E), np.concatenate([gU.real.ravel(), gU.imag.ravel()])
    u0 = np.concatenate([psi.ravel(), np.zeros(N)])
    r = minimize(EG, u0, jac=True, method="L-BFGS-B", options=dict(maxiter=4000, maxcor=30, ftol=1e-16, gtol=1e-13))
    return r.fun
if not hasattr(cell, "KX"):
    kxv = 2*np.pi*np.fft.fftfreq(n[0], d=lens[0]/n[0]); kyv = 2*np.pi*np.fft.fftfreq(n[1], d=lens[1]/n[1]); kzv = 2*np.pi*np.fft.fftfreq(n[2], d=lens[2]/n[2])
    cell.KX, cell.KY, cell.KZ = np.meshgrid(kxv, kyv, kzv, indexing="ij")
E0 = twisted_energy([0, 0, 0])
for dname, dvec in (("basal_x", [1, 0, 0]), ("axial_z", [0, 0, 1])):
    kk = 0.02; Ek = twisted_energy(kk*np.array(dvec, float))
    fs = (Ek - E0)/(0.5*kk*kk)
    out["dirs"][dname]["f_s_twist"] = float(fs)
    print(f"   {dname:8s} relaxed-twist f_s = {fs:.6f}  vs band m/m* = {1/out['dirs'][dname]['mstar']:.6f}", flush=True)
json.dump(out, open(REPO + "/audit_followup/A2_internal_modes/a2_band3d.json", "w"), indent=1, default=float)
print(f"done ({time.time()-t0:.0f}s)")
