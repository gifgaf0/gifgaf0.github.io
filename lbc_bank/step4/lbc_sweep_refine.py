#!/usr/bin/env python3
"""
lbc_sweep_refine.py -- refine the low-g end of the LBC sweep: follow the crystal branch
continuously (each g seeded from the previous crystal on the same fractional grid) to
(a) pin the fixed-density coexistence boundary Lambda_c (h = 0) and (b) find where the
metastable crystal disappears, measuring c2/c_T, weights and f_s at each point.
Re-uses lbc_sweep_low.point machinery but with continuation seeding.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging")
import g_tsh1_chatleg as T
SCR = "/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc"
sys.path.insert(0, SCR)
from lbc_weights import bdg_full
from lbc_sweep_low import fs_twist, identify, KF

OUT = os.path.join(SCR, "lbc_sweep_refine.json")


def scan_cont(g, a_c, psi_seed, da=(-0.03, 0.05), npts=9):
    alist = np.linspace(a_c+da[0], a_c+da[1], npts); Es = []; psis = []
    for a in alist:
        st = T.relax_cell(a, g, "soft", Nc=96, psi_init=psi_seed)
        Es.append(st["E_area"]); psis.append(st["psi"])
    Es = np.array(Es); i = int(np.argmin(Es)); i0 = min(max(i, 1), npts-2)
    p = np.polyfit(alist[i0-1:i0+2], Es[i0-1:i0+2], 2)
    astar = -p[1]/(2*p[0]) if p[0] > 0 else alist[i]
    return float(astar), alist.tolist(), Es.tolist(), psis[i]


def measure(g, astar, psi_seed):
    st, gpres = T.polish(T.relax_cell(astar, g, "soft", Nc=96, psi_init=psi_seed))
    w2m, wok = T.ward_check(st, g, "soft")
    rho = st["psi"]**2
    contrast = float((rho.max()-rho.min())/rho.mean())
    out = dict(g=g, astar=astar, eps_c=float(st["E_area"]), mu_c=float(st["mu"]), eps_u=float(np.pi*g/2),
               gp_residual=gpres, ward_w2min=w2m, contrast=contrast, rho_min=float(rho.min()))
    out["h"] = float(g*(out["mu_c"]-out["eps_c"]) - out["mu_c"]**2/(2*np.pi))
    if contrast < 0.05:
        out["crystal"] = False
        return out, st
    out["crystal"] = True
    out["f_s"], _ = fs_twist(st, g)
    unit = 2*np.pi/astar; rows = []
    for dname, qhat, kfs in (("GM", [1.0, 0.0], KF), ("GK", [np.cos(np.pi/6), np.sin(np.pi/6)], [0.05])):
        for kf in kfs:
            q = kf*unit
            r = bdg_full(st, g, "soft", q*np.array(qhat), n=32)
            iT, iLm, iLp, zTq, _ = identify(r, q)
            om, Z = r["om"], r["Z"]; fex = r["Ncell"]*q*q/2
            stat = float(np.sum(2*Z[om > 1e-9]/om[om > 1e-9]))
            rows.append(dict(dir=dname, kf=kf, q=q, c_Lm=float(om[iLm]/q), c_T=float(om[iT]/q), c_Lp=float(om[iLp]/q),
                             Zq_Lm=float(Z[iLm]/q), Zq_Lp=float(Z[iLp]/q), Zq_T=zTq,
                             F_Lm=float(om[iLm]*Z[iLm]/fex), F_Lp=float(om[iLp]*Z[iLp]/fex),
                             S_Lm=float(2*Z[iLm]/om[iLm]/stat), order=[int(iLm), int(iT), int(iLp)],
                             fsum_ratio=float(np.sum(om*Z)/fex), static_ratio=float(stat/r["chi_static"])))
    out["rows"] = rows
    gm = [rw for rw in rows if rw["dir"] == "GM"]; qs = np.array([rw["q"] for rw in gm])
    for lab in ("c_Lm", "c_T", "c_Lp"):
        om = np.array([rw[lab]*rw["q"] for rw in gm]); out[lab+"_fit"] = float(np.sum(qs*om)/np.sum(qs*qs))
    out["ratio_c2_cT_fit"] = out["c_Lm_fit"]/out["c_T_fit"]
    return out, st


if __name__ == "__main__":
    res = {}
    t0 = time.time()
    # anchor: g = 13.0 crystal from the standard Gaussian seed at the sweep's a*
    st13 = T.relax_cell(1.5102, 13.0, "soft", Nc=96)
    psi = st13["psi"]; a_c = 1.5102
    # upward point first (13.25), then descend
    for g in [13.25, 13.0, 12.9, 12.8, 12.7, 12.6, 12.55, 12.5, 12.45, 12.4]:
        astar, alist, Es, psi_best = scan_cont(g, a_c, psi)
        o, st = measure(g, astar, psi_best)
        o["a_scan"] = alist; o["E_scan"] = Es
        res[f"{g:g}"] = o
        msg = (f"[g={g}] a*={astar:.4f} contrast={o['contrast']:.3f} eps_c-eps_u={o['eps_c']-o['eps_u']:+.5f} "
               f"h={o['h']:+.4f} res={o['gp_residual']:.1e} ward={o['ward_w2min']:.2e}")
        if o["crystal"]:
            msg += (f" f_s={o['f_s']:.4f} c2={o['c_Lm_fit']:.4f} cT={o['c_T_fit']:.4f} c1={o['c_Lp_fit']:.4f} "
                    f"c2/cT={o['ratio_c2_cT_fit']:.4f}")
            if g <= 13.0:
                psi = st["psi"]; a_c = astar
        print(msg + f"  ({time.time()-t0:.0f}s)", flush=True)
        with open(OUT, "w") as f:
            json.dump(res, f, indent=1, default=float)
        if not o["crystal"]:
            print(f"[g={g}] crystal branch lost; stopping descent", flush=True)
            break
    print("REFINE DONE", flush=True)
