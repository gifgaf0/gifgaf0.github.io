#!/usr/bin/env python3
"""Corrected first leg, 3D: the first leg's AB (hcp) cell and kernel (lbc_3d.py / tsh4_core, unchanged), with the
in-basis ground state converged tightly by L-BFGS on the masked field (projected GP residual reported), then the first
leg's own bdg_weights (imported from lbc_3d.py, unchanged) at the same q rows, for cut-offs 22 and 30."""
import sys, os, json, time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, "/home/claude/gifgaf0.github.io/gtsh4_gate")
import tsh4_core as C, tsh4_routeD as D
sys.path.insert(0, "/home/claude/lbc_exploration")
import lbc_3d as L3
S3 = np.sqrt(3.0); OUT = "jobB_3d.json"

def masked_tight(cell, kg, Lam, gcut, psi0, maxiter=6000):
    mask = (cell.Kmag <= gcut); N = cell.N
    P = lambda f: np.fft.ifftn(np.fft.fftn(f)*mask).real
    def Hpsi(psi):
        n = psi*psi; conv = np.fft.ifftn(kg*np.fft.fftn(n)).real
        return np.fft.ifftn(0.5*cell.K2*np.fft.fftn(psi)).real + Lam*conv*psi
    def EG(u):
        U = P(u.reshape(cell.n)); s = 1.0/np.sqrt((U*U).mean()); psi = s*U
        Hp = Hpsi(psi); e = C.energy(cell, kg, Lam, psi)
        g = (2.0/N)*Hp
        gu = s*g - s*U*np.sum(U*g)/np.sum(U*U)
        return e, P(gu).ravel()
    u0 = P(psi0); u0 /= np.sqrt((u0*u0).mean())
    r = minimize(EG, u0.ravel(), jac=True, method="L-BFGS-B", options=dict(maxiter=maxiter, maxcor=30, ftol=1e-16, gtol=1e-15))
    U = P(r.x.reshape(cell.n)); psi = U/np.sqrt((U*U).mean())
    Hp = Hpsi(psi); mu = (psi*Hp).mean()/(psi*psi).mean()
    rp = P(Hp - mu*psi); res_proj = float(np.sqrt((rp*rp).mean())/abs(mu))
    return psi, float(mu), float(C.energy(cell, kg, Lam, psi)), res_proj, int(r.nit)

def proj_res(cell, kg, Lam, gcut, psi):
    mask = (cell.Kmag <= gcut); P = lambda f: np.fft.ifftn(np.fft.fftn(f)*mask).real
    n = psi*psi; conv = np.fft.ifftn(kg*np.fft.fftn(n)).real
    Hp = np.fft.ifftn(0.5*cell.K2*np.fft.fftn(psi)).real + Lam*conv*psi
    mu = (psi*Hp).mean()/(psi*psi).mean(); rp = P(Hp - mu*psi)
    return float(np.sqrt((rp*rp).mean())/abs(mu))

def transverse_pick(r):
    om = np.array(r["om"]); q = r["q"]; Zq = np.array(r["Zq"])
    cand = [i for i in range(len(om)) if 4.0 < om[i]/q < 12.0]
    cand = sorted(cand, key=lambda i: Zq[i])[:2]
    return sorted(cand, key=lambda i: om[i])

if __name__ == "__main__":
    t0 = time.time(); res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    ph = json.load(open("/home/claude/gifgaf0.github.io/gtsh4_gate/tsh4_phase0_measurements.json"))
    lc, kstar = C.lambda_c(C.step_khat, 40.0); Lam = 2*lc; khat = C.step_khat
    a, c = ph['results']['step']['structures']['AB']['params']
    H = np.diag([a, a*S3, c]).astype(float); sites = C.STRUCTURES['AB']['sites']
    lens = np.diag(H); n = tuple(L3.ev(L3.PPL*l) for l in lens)
    cell = C.Cell(list(lens), n); kg = C.khat_grid(cell, khat)
    psi = cell.seed(sites, 0.24*lens[0])
    psi, e, resf, it, _ = C.relax(cell, kg, Lam, psi, dt=0.008, restol=1e-10)
    print(f"[3D] full-grid relax e={e:.9f} res={resf:.2e} ({time.time()-t0:.0f}s)", flush=True)
    for gcut in (22.0, 30.0):
        key = f"K{gcut:g}"
        if key in res: continue
        psi_old, mu_old, e_old, res_old = D.relax_truncated(cell, kg, Lam, gcut, psi)
        pr_old = proj_res(cell, kg, Lam, gcut, psi_old)
        psi_t, mu_t, e_t, pr_new, nit = masked_tight(cell, kg, Lam, gcut, psi_old)
        print(f"[3D {key}] first-leg in-basis state: e={e_old:.9f} projected res={pr_old:.2e} (reported res {res_old:.2e}) | "
              f"tight: e={e_t:.9f} projected res={pr_new:.2e} nit={nit} ({time.time()-t0:.0f}s)", flush=True)
        basis = D.PWBasis(H, psi_t, gcut)
        rec = dict(gcut=gcut, NG=basis.NG, e_old=e_old, e_new=e_t, mu=mu_t, projres_old=pr_old, projres_new=pr_new, rows=[])
        r0 = L3.bdg_weights(basis, khat, Lam, mu_t, np.array([1e-4, 0, 0]))
        rec["near_gamma_om"] = r0["om"][:8]
        print(f"[3D {key}] NG={basis.NG} near-Gamma om={[f'{x:.6f}' for x in r0['om'][:8]]}", flush=True)
        qs = (0.15, 0.3, 0.6) if gcut < 25 else (0.15,)
        for lbl, d in (("basal_GM", [1, 0, 0]), ("axial", [0, 0, 1]), ("basal_GK", [np.cos(np.pi/6), np.sin(np.pi/6), 0])):
            d = np.array(d, float); d /= np.linalg.norm(d)
            for qm in qs:
                r = L3.bdg_weights(basis, khat, Lam, mu_t, qm*d); r["dir"] = lbl
                iT = transverse_pick(r); r["iT"] = iT
                r["cT"] = [r["om"][i]/r["q"] for i in iT]
                rec["rows"].append(r)
                print(f"[3D {key} {lbl} q={qm}] om={[f'{x:.4f}' for x in r['om'][:8]]} cT={[f'{x:.5f}' for x in r['cT']]} "
                      f"c2={r['om'][0]/r['q']:.5f} F2={r['fshare'][0]:.5f} fsum {r['fsum_ratio']:.6f} static {r['static_ratio']:.6f} ({time.time()-t0:.0f}s)", flush=True)
                res[key] = rec; json.dump(res, open(OUT, "w"), indent=1, default=float)
        res[key] = rec; json.dump(res, open(OUT, "w"), indent=1, default=float)
    print("JOB B DONE", flush=True)
