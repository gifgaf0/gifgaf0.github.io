#!/usr/bin/env python3
"""
lbc_hydro.py -- independent hydrodynamic cross-check of the branch weights.

Computes, with NO BdG input, the T=0 supersolid hydrodynamic inputs on the canonical state:
  f_s      superfluid fraction (phase-twist energy, lattice fixed)
  alpha    = d2e/drho2 at fixed lattice           (alpha_rho-rho)
  M        = C_xxxx = d2e/deps_x2 at fixed rho    (alpha_uu)
  gamma    = d2e/drho deps_x                      (alpha_rho-u)
  C_xxyy, C_xyxy (shear modulus mu) for the isotropy / c_T check
and evaluates the Yoo-Dorsey / Platt-Baillie-Blakie relations (my derivation, EXPECTATION note):
  a = rho*alpha - 2 gamma + M/rho_n ; b = (rho_s/rho_n)(alpha M - gamma^2)
  c_+-^2 = (a -+ sqrt(a^2-4b))/2 ;  c_T^2 = mu/rho_n
  F_-  = (c_*^2 - c_-^2)/(c_+^2 - c_-^2),  c_*^2 = rho_s M/(rho_n rho)   (lower-branch f-sum share)
  Z_nu/q per cell = area * F_nu /(2 c_nu)
Substrate units; rho = 1.
"""
import sys, os, json, time
import numpy as np
from numpy.fft import fft2, ifft2
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging")
import g_tsh1_chatleg as T

OUT = "/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc"
G = 22.0; KERN = "soft"; ASTAR = 1.4574710087903182; NC = 96

def cellgeom_F(a, F, Nc=NC):
    """Oblique p6m cell with real-space vectors deformed by the 2x2 matrix F."""
    a1 = F @ np.array([a, 0.0]); a2 = F @ np.array([0.5*a, np.sqrt(3)/2*a])
    A = np.array([a1, a2])                     # rows
    B = 2*np.pi*np.linalg.inv(A).T             # rows b1, b2 with a_i.b_j = 2 pi delta_ij
    b1, b2 = B[0], B[1]
    m = np.fft.fftfreq(Nc)*Nc
    MM, NN = np.meshgrid(m, m, indexing="ij")
    Gx = MM*b1[0]+NN*b2[0]; Gy = MM*b1[1]+NN*b2[1]
    area = abs(np.linalg.det(A))
    s = (np.arange(Nc)+0.5)/Nc
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    X = S1*a1[0]+S2*a2[0]; Y = S1*a1[1]+S2*a2[1]
    return dict(a=a, a1=a1, a2=a2, b1=b1, b2=b2, Gx=Gx, Gy=Gy, G2=Gx**2+Gy**2, area=area, X=X, Y=Y, Nc=Nc)

def relax_ge(ge, rho_bar, kvec=(0.0, 0.0), psi_init=None, dt=0.001, tau=6.0,
             polish_stages=((1e-4, 6000),), tol=1e-12):
    """Imaginary-time GP relaxation on a given cell geometry at mean density rho_bar,
    with an optional Bloch twist kvec (kinetic |G+k|^2/2, complex psi kept)."""
    Nc = ge["Nc"]; Uk = T.KFN[KERN](np.sqrt(ge["G2"]), G)
    K2 = (ge["Gx"]+kvec[0])**2 + (ge["Gy"]+kvec[1])**2
    Ntot = rho_bar*ge["area"]
    if psi_init is None:
        rc = 0.5*(ge["a1"]+ge["a2"])
        d2 = (ge["X"]-rc[0])**2+(ge["Y"]-rc[1])**2
        psi = np.exp(-d2/(2*0.35**2))+0.05+0j
    else:
        psi = psi_init.astype(complex).copy()
    def renorm(p): return p*np.sqrt(Ntot/(np.sum(np.abs(p)**2)*ge["area"]/Nc**2))
    def energy(p):
        c = fft2(p)/Nc**2; rho = np.abs(p)**2; rk = fft2(rho)/Nc**2
        Ek = np.sum(0.5*K2*np.abs(c)**2)*ge["area"]; Ei = 0.5*np.sum(Uk*np.abs(rk)**2)*ge["area"]
        return Ek, Ei
    psi = renorm(psi)
    for (dtt, nsteps) in ((dt, int(tau/dt)),) + tuple(polish_stages):
        Kin = np.exp(-0.5*dtt*0.5*K2); Eprev = None
        for it in range(nsteps):
            psi = ifft2(Kin*fft2(psi)); rho = np.abs(psi)**2
            Phi = ifft2(Uk*fft2(rho)).real
            psi = psi*np.exp(-dtt*Phi)
            psi = ifft2(Kin*fft2(psi)); psi = renorm(psi)
            if it % 500 == 499:
                Ek, Ei = energy(psi); E = Ek+Ei
                if Eprev is not None and abs(E-Eprev) < tol*max(1, abs(E)): break
                Eprev = E
    Ek, Ei = energy(psi)
    mu = (Ek+2*Ei)/Ntot
    return dict(psi=psi, Ek=Ek, Ei=Ei, E=Ek+Ei, e=(Ek+Ei)/ge["area"], mu=mu, area=ge["area"], N=Ntot)

def main():
    res = {}
    t0 = time.time()
    I = np.eye(2)
    base = relax_ge(cellgeom_F(ASTAR, I), 1.0)
    psi0 = base["psi"]
    print(f"[base] e={base['e']:.8f} mu={base['mu']:.6f} area={base['area']:.6f} ({time.time()-t0:.0f}s)", flush=True)
    res["base"] = dict(e=base["e"], mu=base["mu"], area=base["area"])

    # ---- superfluid fraction: phase twist along x and along y, lattice fixed
    fs = {}
    for kk in [0.02, 0.04]:
        for lab, kv in (("x", (kk, 0.0)), ("y", (0.0, kk))):
            tw = relax_ge(cellgeom_F(ASTAR, I), 1.0, kvec=kv, psi_init=psi0, tau=4.0)
            f = (tw["E"]-base["E"])/(0.5*base["N"]*kk**2)
            fs[f"{lab}_{kk}"] = f
            print(f"[fs] twist {lab} k={kk}: f_s={f:.6f}  ({time.time()-t0:.0f}s)", flush=True)
    res["fs"] = fs
    f_s = float(np.mean([fs["x_0.02"], fs["y_0.02"]]))

    # ---- elastic constants and compressibility by central differences (relaxed psi each time)
    def e_of(rho_bar, ex=0.0, ey=0.0, sh=0.0):
        F = np.array([[1+ex, sh], [0.0, 1+ey]])
        r = relax_ge(cellgeom_F(ASTAR, F), rho_bar, psi_init=psi0, tau=4.0)
        return r["e"]
    h = 0.01
    e0 = base["e"]
    # alpha = d2e/drho2 (fixed lattice)
    ep, em = e_of(1+h), e_of(1-h)
    alpha = (ep-2*e0+em)/h**2
    ep2, em2 = e_of(1+2*h), e_of(1-2*h)
    alpha2 = (ep2-2*e0+em2)/(2*h)**2
    alpha_R = (4*alpha-alpha2)/3
    print(f"[alpha] h={h}: {alpha:.5f}  h=2h: {alpha2:.5f}  Richardson {alpha_R:.5f}  (mu check: dmu/drho ~ {(ep-em)/(2*h):.5f} vs mu {base['mu']:.5f})", flush=True)
    # M = C_xxxx (fixed rho)
    exp_, exm = e_of(1.0, ex=h), e_of(1.0, ex=-h)
    Mx = (exp_-2*e0+exm)/h**2
    exp2, exm2 = e_of(1.0, ex=2*h), e_of(1.0, ex=-2*h)
    Mx2 = (exp2-2*e0+exm2)/(2*h)**2
    M_R = (4*Mx-Mx2)/3
    print(f"[M=C_xxxx] h: {Mx:.5f}  2h: {Mx2:.5f}  Richardson {M_R:.5f}; first-derivative (stress) check {(exp_-exm)/(2*h):.2e}", flush=True)
    # C_xxyy
    epp, epm, emp, emm = e_of(1, h, h), e_of(1, h, -h), e_of(1, -h, h), e_of(1, -h, -h)
    Cxxyy = (epp-epm-emp+emm)/(4*h*h)
    # also C_yyyy for isotropy
    eyp, eym = e_of(1.0, ey=h), e_of(1.0, ey=-h)
    My = (eyp-2*e0+eym)/h**2
    # shear modulus from simple shear
    esp, esm = e_of(1.0, sh=h), e_of(1.0, sh=-h)
    mu_sh = (esp-2*e0+esm)/h**2
    esp2, esm2 = e_of(1.0, sh=2*h), e_of(1.0, sh=-2*h)
    mu_sh2 = (esp2-2*e0+esm2)/(2*h)**2
    mu_R = (4*mu_sh-mu_sh2)/3
    print(f"[elastic] C_xxyy={Cxxyy:.5f} C_yyyy={My:.5f} (C_xxxx={Mx:.5f}); mu(shear)={mu_sh:.5f}/{mu_sh2:.5f} R={mu_R:.5f}; "
          f"(C_xxxx-C_xxyy)/2={(Mx-Cxxyy)/2:.5f}", flush=True)
    # gamma = d2e/drho deps_x
    g_pp, g_pm, g_mp, g_mm = e_of(1+h, ex=h), e_of(1+h, ex=-h), e_of(1-h, ex=h), e_of(1-h, ex=-h)
    gamma = (g_pp-g_pm-g_mp+g_mm)/(4*h*h)
    # and the y-strain cross term (isotropy check)
    gy_pp, gy_pm, gy_mp, gy_mm = e_of(1+h, ey=h), e_of(1+h, ey=-h), e_of(1-h, ey=h), e_of(1-h, ey=-h)
    gamma_y = (gy_pp-gy_pm-gy_mp+gy_mm)/(4*h*h)
    print(f"[gamma] d2e/drho deps_x = {gamma:.5f}   (y: {gamma_y:.5f})  ({time.time()-t0:.0f}s)", flush=True)
    res["elastic"] = dict(alpha=alpha, alpha_R=alpha_R, M=Mx, M_R=M_R, Cyyyy=My, Cxxyy=Cxxyy, mu_shear=mu_sh, mu_R=mu_R,
                          gamma=gamma, gamma_y=gamma_y, f_s=f_s, h=h)

    # ---- hydrodynamic predictions (rho = 1)
    def predict(alpha, M, gamma, mu, f_s):
        rho = 1.0; rs = f_s; rn = 1-f_s
        a = rho*alpha - 2*gamma + M/rn
        b = (rs/rn)*(alpha*M - gamma**2)
        disc = np.sqrt(a*a-4*b)
        cp2, cm2 = (a+disc)/2, (a-disc)/2
        cT2 = mu/rn
        cstar2 = rs*M/(rn*rho)
        Fm = (cstar2-cm2)/(cp2-cm2); Fp = 1-Fm
        ckappa2 = rho*(alpha - gamma**2/M)            # static (uniaxial, lattice-relaxed) compressibility speed
        return dict(c_plus=float(np.sqrt(cp2)), c_minus=float(np.sqrt(cm2)), c_T=float(np.sqrt(cT2)),
                    c_star2=cstar2, F_minus=Fm, F_plus=Fp,
                    Zq_minus_percell=base["area"]*Fm/(2*np.sqrt(cm2)), Zq_plus_percell=base["area"]*Fp/(2*np.sqrt(cp2)),
                    static_share_minus=(Fm/cm2)/(Fm/cm2+Fp/cp2), c_kappa=float(np.sqrt(ckappa2)),
                    chi_static_percell=base["area"]/ckappa2)
    pred = predict(alpha_R, M_R, gamma, mu_R, f_s)
    res["prediction"] = pred
    print("[hydro prediction]", json.dumps(pred, indent=1), flush=True)
    with open(os.path.join(OUT, "lbc_hydro.json"), "w") as f: json.dump(res, f, indent=1, default=float)

if __name__ == "__main__":
    main()
