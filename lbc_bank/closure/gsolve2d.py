"""Tight 2D ground state on the first leg's 96x96 cell grid: L-BFGS on the energy at fixed norm, then
Newton-Krylov on the augmented GP system [H psi - mu psi ; norm] (unknowns psi and mu)."""
import numpy as np
from numpy.fft import fft2, ifft2
from scipy.optimize import minimize, newton_krylov

def Hpsi_of(psi, ge, Uk):
    rho = psi**2; Phi = ifft2(Uk*fft2(rho)).real
    return -0.5*ifft2(-ge["G2"]*fft2(psi)).real + Phi*psi, Phi

def residual(psi, ge, Uk):
    Hp, Phi = Hpsi_of(psi, ge, Uk)
    mu = np.sum(psi*Hp)/np.sum(psi*psi)
    return float(np.sqrt(np.mean((Hp-mu*psi)**2))/np.sqrt(np.mean(psi**2))), float(mu), Phi

def make_state(psi, ge, Uk):
    Nc = ge["Nc"]; Ntot = ge["area"]; rho = psi**2; Phi = ifft2(Uk*fft2(rho)).real
    c = fft2(psi)/Nc**2; rk = fft2(rho)/Nc**2
    Ekin = np.sum(0.5*ge["G2"]*np.abs(c)**2)*ge["area"]; Eint = 0.5*np.sum(Uk*np.abs(rk)**2)*ge["area"]
    return dict(psi=psi, ge=ge, Uk=Uk, E_area=(Ekin+Eint)/ge["area"], mu=(Ekin+2*Eint)/Ntot, Phi=Phi)

def tight(st, nk_tol=1e-11, verbose=False):
    ge, Uk = st["ge"], st["Uk"]; Nc = ge["Nc"]; dA = ge["area"]/Nc**2; Ntot = ge["area"]
    def EG(u):
        U = u.reshape(Nc, Nc); s = np.sqrt(Ntot/(dA*np.sum(U*U))); psi = s*U
        Hp, Phi = Hpsi_of(psi, ge, Uk)
        E = dA*np.sum(psi*(Hp - 0.5*Phi*psi))
        gpsi = 2*dA*Hp
        gu = s*gpsi - s*U*np.sum(U*gpsi)/np.sum(U*U)
        return E, gu.ravel()
    r = minimize(EG, st["psi"].ravel().copy(), jac=True, method="L-BFGS-B",
                 options=dict(maxiter=20000, maxcor=50, ftol=1e-16, gtol=1e-14))
    U = r.x.reshape(Nc, Nc); psi = np.abs(np.sqrt(Ntot/(dA*np.sum(U*U)))*U)
    res_lbfgs, mu0, _ = residual(psi, ge, Uk)
    def F(x):
        p = x[:-1].reshape(Nc, Nc); m = x[-1]
        Hp, _ = Hpsi_of(p, ge, Uk)
        return np.concatenate([(Hp - m*p).ravel(), [(dA*np.sum(p*p) - Ntot)/Ntot]])
    x0 = np.concatenate([psi.ravel(), [mu0]])
    try:
        x = newton_krylov(F, x0, f_tol=nk_tol, maxiter=40, method="lgmres", verbose=verbose)
        p = np.abs(x[:-1].reshape(Nc, Nc)); p *= np.sqrt(Ntot/(dA*np.sum(p*p)))
        res_nk, _, _ = residual(p, ge, Uk)
        if res_nk < res_lbfgs:
            psi = p
    except Exception as e:
        res_nk = float("nan")
    return make_state(psi, ge, Uk), res_lbfgs, res_nk
