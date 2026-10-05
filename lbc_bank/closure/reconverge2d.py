#!/usr/bin/env python3
"""Chat-side check of the second leg's diagnosis (2D): re-converge the first leg's ground state with a
non-split solver (L-BFGS on the energy at fixed norm, then Newton-Krylov on the GP equation), then rerun the
first leg's own BdG (lbc_weights.bdg_full, unchanged) and compare transverse speeds and the Ward value."""
import sys, json, time
import numpy as np
from numpy.fft import fft2, ifft2
from scipy.optimize import minimize, newton_krylov
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging")
import g_tsh1_chatleg as T
sys.path.insert(0, "/home/claude/lbc_exploration")
from lbc_weights import bdg_full

def residual(psi, ge, Uk):
    Nc = ge["Nc"]; rho = psi**2; Phi = ifft2(Uk*fft2(rho)).real
    lap = ifft2(-ge["G2"]*fft2(psi)).real
    Hpsi = -0.5*lap + Phi*psi
    mu = np.sum(psi*Hpsi)/np.sum(psi*psi)
    r = np.sqrt(np.mean((Hpsi - mu*psi)**2))/np.sqrt(np.mean(psi**2))
    return float(r), float(mu), Phi

def make_state(psi, ge, Uk):
    Nc = ge["Nc"]; Ntot = ge["area"]
    rho = psi**2; Phi = ifft2(Uk*fft2(rho)).real
    c = fft2(psi)/Nc**2; rk = fft2(rho)/Nc**2
    Ekin = np.sum(0.5*ge["G2"]*np.abs(c)**2)*ge["area"]; Eint = 0.5*np.sum(Uk*np.abs(rk)**2)*ge["area"]
    return dict(psi=psi, ge=ge, Uk=Uk, E_area=(Ekin+Eint)/ge["area"], mu=(Ekin+2*Eint)/Ntot, Phi=Phi)

def reconverge(st):
    ge, Uk = st["ge"], st["Uk"]; Nc = ge["Nc"]; dA = ge["area"]/Nc**2; Ntot = ge["area"]
    u0 = st["psi"].ravel().copy()
    def EG(u):
        U = u.reshape(Nc, Nc); s = np.sqrt(Ntot/(dA*np.sum(U*U))); psi = s*U
        rho = psi**2; Phi = ifft2(Uk*fft2(rho)).real
        lap = ifft2(-ge["G2"]*fft2(psi)).real
        E = dA*np.sum(psi*(-0.5*lap)) + 0.5*dA*np.sum(rho*Phi)
        gpsi = 2*dA*(-0.5*lap + Phi*psi)
        gu = s*gpsi - s*U*np.sum(U*gpsi)/np.sum(U*U)
        return E, gu.ravel()
    r = minimize(EG, u0, jac=True, method="L-BFGS-B", options=dict(maxiter=20000, maxcor=50, ftol=1e-16, gtol=1e-13))
    U = r.x.reshape(Nc, Nc); psi = np.sqrt(Ntot/(dA*np.sum(U*U)))*U
    res_lbfgs, mu, _ = residual(psi, ge, Uk)
    # Newton-Krylov on F(psi) = H psi - mu(psi) psi, with the norm restored after convergence
    def F(p):
        p = p.reshape(Nc, Nc); rho = p**2; Phi = ifft2(Uk*fft2(rho)).real
        lap = ifft2(-ge["G2"]*fft2(p)).real; Hp = -0.5*lap + Phi*p
        m = np.sum(p*Hp)/np.sum(p*p)
        return (Hp - m*p).ravel()
    try:
        p = newton_krylov(F, psi.ravel(), f_tol=1e-11, maxiter=60, method="lgmres")
        p = p.reshape(Nc, Nc); p *= np.sqrt(Ntot/(dA*np.sum(p*p)))
        if np.min(p) < -1e-8: p = -p
        res_nk, mu, _ = residual(p, ge, Uk)
        if res_nk < res_lbfgs: psi = p
    except Exception as e:
        res_nk = float("nan")
    return make_state(np.abs(psi), ge, Uk), res_lbfgs, res_nk

def transverse_speeds(st, g, astar, kfs, dirs):
    unit = 2*np.pi/astar; out = {}
    for dname, qhat in dirs.items():
        rows = []
        for kf in kfs:
            q = kf*unit*np.array(qhat); qn = kf*unit
            r = bdg_full(st, g, "soft", q, n=32)
            om, Z = r["om"][:3], r["Z"][:3]
            it = int(np.argmin(Z/qn)); il = [i for i in range(3) if i != it]
            rows.append(dict(kf=kf, q=qn, cT=float(om[it]/qn), c2=float(min(om[il])/qn), c1=float(max(om[il])/qn)))
        out[dname] = rows
    return out

if __name__ == "__main__":
    g = float(sys.argv[1]); astar = float(sys.argv[2]); tag = sys.argv[3]
    kfs = [0.01, 0.02, 0.03, 0.05, 0.075, 0.10]
    dirs = {"0deg": [1.0, 0.0], "30deg": [np.cos(np.pi/6), np.sin(np.pi/6)]}
    t0 = time.time()
    st1, res1 = T.polish(T.relax_cell(astar, g, "soft", Nc=96))
    w1, _ = T.ward_check(st1, g, "soft")
    st2, rl, rn = reconverge(st1)
    res2, _, _ = residual(st2["psi"], st2["ge"], st2["Uk"])
    w2, _ = T.ward_check(st2, g, "soft")
    print(f"[{tag}] first-leg state: residual {res1:.2e}, Ward w2min {w1:.4e} | reconverged: L-BFGS {rl:.2e}, NK {rn:.2e}, final {res2:.2e}, Ward w2min {w2:.4e}, dE/A {st2['E_area']-st1['E_area']:.3e}  ({time.time()-t0:.0f}s)", flush=True)
    A = transverse_speeds(st1, g, astar, kfs, dirs); B = transverse_speeds(st2, g, astar, kfs, dirs)
    for d in dirs:
        for a, b in zip(A[d], B[d]):
            print(f"[{tag} {d} kf={a['kf']:.3f}] cT first-leg {a['cT']:.5f} -> reconverged {b['cT']:.5f} ({(b['cT']/a['cT']-1)*100:+.2f}%) | c2 {a['c2']:.5f} -> {b['c2']:.5f} | c1 {a['c1']:.4f} -> {b['c1']:.4f}", flush=True)
    json.dump(dict(g=g, astar=astar, res_first=res1, ward_first=w1, res_reconv=res2, ward_reconv=w2, first=A, reconv=B),
              open(f"reconverge2d_{tag}.json", "w"), indent=1)
