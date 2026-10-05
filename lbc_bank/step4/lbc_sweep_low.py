#!/usr/bin/env python3
"""
lbc_sweep_low.py -- extend the LBC branch-weight sweep below g = 22 toward the
supersolid-superfluid transition (2D soft-core, rho0 = 1, R = 1).

Per g: a* scan (instrument's relax_cell), dt-staged polish, F9 Ward check, density contrast,
phase-twist superfluid fraction, BdG weights (lbc_weights.bdg_full) at kf in KF along Gamma-M
and kf = 0.05 along Gamma-K. Modes are identified by polarisation, NOT by frequency order:
the transverse mode is the gapless mode with zero density weight; the two longitudinal modes
are the remaining gapless modes, labelled L- / L+ by frequency. So c2 > c_T is detectable.
Energetics: eps_c(g) = E/N of the crystal at rho = 1 (polished), eps_u = pi g / 2,
mu_c = GP chemical potential -> fixed-density crossing and the common-tangent (coexistence)
boundary Lambda_c solving  Lambda (mu_c - eps_c) = mu_c^2 / (2 pi).
Substrate units (hbar = m = 1).
"""
import sys, os, json, time
import numpy as np
from numpy.fft import fft2, ifft2
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging")
import g_tsh1_chatleg as T
SCR = "/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc"
sys.path.insert(0, SCR)
from lbc_weights import bdg_full

OUT = os.path.join(SCR, "lbc_sweep_low.json")
KF = [0.03, 0.05, 0.075, 0.10]


def fs_twist(st, g, k=0.02, dt=1e-4, nsteps=12000):
    """Superfluid fraction from the energy of a Bloch phase twist k along x, lattice fixed:
    E(k) - E(0) = (1/2) N f_s k^2.  Relaxes complex psi with kinetic |G+k|^2/2 from psi0."""
    ge = st["ge"]; Nc = ge["Nc"]; Uk = st["Uk"]; area = ge["area"]; N = 1.0*area
    def run(kv):
        K2 = (ge["Gx"]+kv)**2 + ge["Gy"]**2
        psi = st["psi"].astype(complex).copy()
        Kin = np.exp(-0.5*dt*0.5*K2)
        def renorm(p): return p*np.sqrt(N/(np.sum(np.abs(p)**2)*area/Nc**2))
        psi = renorm(psi)
        for _ in range(nsteps):
            psi = ifft2(Kin*fft2(psi)); rho = np.abs(psi)**2
            Phi = ifft2(Uk*fft2(rho)).real
            psi = psi*np.exp(-dt*Phi)
            psi = ifft2(Kin*fft2(psi)); psi = renorm(psi)
        c = fft2(psi)/Nc**2; rho = np.abs(psi)**2; rk = fft2(rho)/Nc**2
        return (np.sum(0.5*K2*np.abs(c)**2) + 0.5*np.sum(Uk*np.abs(rk)**2))*area
    E0 = run(0.0); E1 = run(k)
    return float((E1-E0)/(0.5*N*k*k)), float(E0)


def identify(r, q):
    """Return indices (iT, iLm, iLp) among the 4 lowest modes using density weight."""
    om, Z = r["om"][:4], r["Z"][:4]
    order = list(range(3))                       # three gapless = three lowest at small q
    zq = [Z[i]/q for i in order]
    iT = int(order[int(np.argmin(zq))])
    rest = sorted([i for i in order if i != iT], key=lambda i: om[i])
    return iT, rest[0], rest[1], float(min(zq)), float(max(zq))


def point(g, a_lo, a_hi, npts=13):
    t0 = time.time()
    astar, alist, Es = T.astar_scan(g, "soft", lo=a_lo, hi=a_hi, npts=npts)
    st, gpres = T.polish(T.relax_cell(astar, g, "soft", Nc=96))
    w2m, wok = T.ward_check(st, g, "soft")
    rho = st["psi"]**2
    contrast = float((rho.max()-rho.min())/rho.mean())
    out = dict(g=g, astar=astar, a_scan=alist, E_scan=Es, eps_c=float(st["E_area"]), mu_c=float(st["mu"]),
               eps_u=float(np.pi*g/2), mu_u=float(np.pi*g), gp_residual=gpres, ward_w2min=w2m, ward_ok=bool(wok),
               contrast=contrast, rho_max=float(rho.max()), rho_min=float(rho.min()))
    print(f"[g={g}] a*={astar:.4f} (scan {a_lo:.3f}-{a_hi:.3f}) eps_c={out['eps_c']:.5f} eps_u={out['eps_u']:.5f} "
          f"d={out['eps_c']-out['eps_u']:+.5f} mu_c={out['mu_c']:.4f} contrast={contrast:.3f} rho_min={out['rho_min']:.2e} "
          f"res={gpres:.1e} ward={w2m:.2e}  ({time.time()-t0:.0f}s)", flush=True)
    if contrast < 0.05:
        out["crystal"] = False
        print(f"[g={g}] crystal collapsed to uniform -- no BdG", flush=True)
        return out
    out["crystal"] = True
    fs, E0 = fs_twist(st, g)
    out["f_s"] = fs
    unit = 2*np.pi/astar
    rows = []
    for dname, qhat, kfs in (("GM", [1.0, 0.0], KF), ("GK", [np.cos(np.pi/6), np.sin(np.pi/6)], [0.05])):
        for kf in kfs:
            q = kf*unit
            r = bdg_full(st, g, "soft", q*np.array(qhat), n=32)
            iT, iLm, iLp, zTq, zmax = identify(r, q)
            om, Z = r["om"], r["Z"]
            fex = r["Ncell"]*q*q/2
            stat = float(np.sum(2*Z[om > 1e-9]/om[om > 1e-9]))
            row = dict(dir=dname, kf=kf, q=q, c_Lm=float(om[iLm]/q), c_T=float(om[iT]/q), c_Lp=float(om[iLp]/q),
                       Zq_Lm=float(Z[iLm]/q), Zq_Lp=float(Z[iLp]/q), Zq_T=zTq,
                       F_Lm=float(om[iLm]*Z[iLm]/fex), F_Lp=float(om[iLp]*Z[iLp]/fex),
                       S_Lm=float(2*Z[iLm]/om[iLm]/stat), S_Lp=float(2*Z[iLp]/om[iLp]/stat),
                       order=[int(iLm), int(iT), int(iLp)], cls=r["cls"][:4], om4=[float(x) for x in om[:4]],
                       fsum_ratio=float(np.sum(om*Z)/fex), static_ratio=float(stat/r["chi_static"]),
                       chi_static=float(r["chi_static"]), Lmin=float(r["Lmin"]))
            rows.append(row)
            print(f"   {dname} kf={kf:<5} c(L-,T,L+)=({row['c_Lm']:.4f}, {row['c_T']:.4f}, {row['c_Lp']:.4f}) "
                  f"c2/cT={row['c_Lm']/row['c_T']:.4f} Z/q(L-,L+)=({row['Zq_Lm']:.4f},{row['Zq_Lp']:.4f}) ZT/q={zTq:.1e} "
                  f"F-={row['F_Lm']:.4f} S-={row['S_Lm']:.3f} order={row['order']} cls={row['cls']} "
                  f"sum {row['fsum_ratio']:.6f}/{row['static_ratio']:.6f}", flush=True)
    out["rows"] = rows
    gm = [rw for rw in rows if rw["dir"] == "GM"]
    qs = np.array([rw["q"] for rw in gm])
    for lab in ("c_Lm", "c_T", "c_Lp"):
        om = np.array([rw[lab]*rw["q"] for rw in gm])
        out[lab+"_fit"] = float(np.sum(qs*om)/np.sum(qs*qs))
    out["ratio_c2_cT_fit"] = out["c_Lm_fit"]/out["c_T_fit"]
    print(f"[g={g}] f_s={fs:.4f}  fit c2={out['c_Lm_fit']:.4f} cT={out['c_T_fit']:.4f} c1={out['c_Lp_fit']:.4f} "
          f"c2/cT={out['ratio_c2_cT_fit']:.4f}  ({time.time()-t0:.0f}s)", flush=True)
    return out


if __name__ == "__main__":
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    glist = [float(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else \
        [20.0, 18.0, 17.0, 16.0, 15.5, 15.0, 14.5, 14.0, 13.5, 13.0, 12.5, 12.0, 11.5, 11.0]
    a_prev = 1.4575
    for g in glist:
        key = f"{g:g}"
        if key in res and res[key].get("done"):
            a_prev = res[key]["astar"]; continue
        try:
            o = point(g, a_prev-0.10, a_prev+0.14, npts=13)
            o["done"] = True
            res[key] = o
            if o.get("crystal"):
                a_prev = o["astar"]
        except Exception as e:
            print(f"[g={g}] ERROR {type(e).__name__}: {e}", flush=True)
            res[key] = dict(g=g, error=str(e), done=False)
        with open(OUT, "w") as f:
            json.dump(res, f, indent=1, default=float)
    print("SWEEP DONE", flush=True)
