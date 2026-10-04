#!/usr/bin/env python3
"""Corrected first leg, 2D: every point of the paper's Table 1 rebuilt at the first leg's own a*, relaxed and
polished exactly as before, then converged tightly (gsolve2d.tight, L-BFGS at fixed norm), then measured with the
first leg's own BdG (lbc_weights.bdg_full) and mode identification (lbc_sweep_low.identify), unchanged."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging"); import g_tsh1_chatleg as T
sys.path.insert(0, "/home/claude/lbc_exploration"); from lbc_weights import bdg_full
from gsolve2d import tight, residual
OLD = "/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc/"
A = json.load(open("/home/claude/lbc_exploration/lbc_results.json"))
LOW = json.load(open(OLD+"lbc_sweep_low.json")); REF = json.load(open(OLD+"lbc_sweep_refine.json"))
KF = [0.03, 0.05, 0.075, 0.10]
OUT = "jobA_2d.json"

def identify(r, q):
    om, Z = r["om"][:4], r["Z"][:4]
    zq = [Z[i]/q for i in range(3)]
    iT = int(np.argmin(zq)); rest = sorted([i for i in range(3) if i != iT], key=lambda i: om[i])
    return iT, rest[0], rest[1]

def measure(st, g, kern, astar, want_gk=False):
    unit = 2*np.pi/astar; rows = []
    dirs = [("GM", [1.0, 0.0], KF)] + ([("GK", [np.cos(np.pi/6), np.sin(np.pi/6)], [0.05])] if want_gk else [])
    for dname, qhat, kfs in dirs:
        for kf in kfs:
            q = kf*unit; r = bdg_full(st, g, kern, q*np.array(qhat), n=32)
            iT, iLm, iLp = identify(r, q); om, Z = r["om"], r["Z"]
            fex = r["Ncell"]*q*q/2; ok = om > 1e-9
            stat = float(np.sum(2*Z[ok]/om[ok]))
            rows.append(dict(dir=dname, kf=kf, q=q, c_Lm=float(om[iLm]/q), c_T=float(om[iT]/q), c_Lp=float(om[iLp]/q),
                             Z_Lm=float(Z[iLm]), Z_Lp=float(Z[iLp]), F_Lm=float(om[iLm]*Z[iLm]/fex),
                             S_Lm=float(2*Z[iLm]/om[iLm]/stat), fsum_ratio=float(np.sum(om*Z)/fex),
                             static_ratio=float(stat/r["chi_static"]), Lmin=float(r["Lmin"])))
    gm = [x for x in rows if x["dir"] == "GM"]; qs = np.array([x["q"] for x in gm])
    fit = lambda lab: float(np.sum(qs*np.array([x[lab]*x["q"] for x in gm]))/np.sum(qs*qs))
    r5 = [x for x in gm if abs(x["kf"]-0.05) < 1e-12][0]
    out = dict(c2=fit("c_Lm"), cT=fit("c_T"), c1=fit("c_Lp"), F2=r5["F_Lm"], Z21=r5["Z_Lm"]/r5["Z_Lp"], S2=r5["S_Lm"],
               rows=rows, fsum_resid_max=max(abs(x["fsum_ratio"]-1) for x in rows),
               static_resid_max=max(abs(x["static_ratio"]-1) for x in rows))
    gk = [x for x in rows if x["dir"] == "GK"]
    if gk: out["cT_GK_kf005"] = gk[0]["c_T"]
    return out

def run(label, g, kern, astar, f_s_old, phase, seed=None, want_gk=False):
    t0 = time.time()
    st0 = T.relax_cell(astar, g, kern, Nc=96, psi_init=seed)
    st1, res_old = T.polish(st0)
    w_old, _ = T.ward_check(st1, g, kern)
    st2, rl, rn = tight(st1)
    res_new, _, _ = residual(st2["psi"], st2["ge"], st2["Uk"]); w_new, _ = T.ward_check(st2, g, kern)
    rho = st2["psi"]**2; contrast = float((rho.max()-rho.min())/rho.mean())
    m = measure(st2, g, kern, astar, want_gk)
    rec = dict(label=label, g=g, kernel=kern, astar=astar, phase=phase, f_s=f_s_old, eps_c=float(st2["E_area"]),
               mu_c=float(st2["mu"]), eps_u=float(np.pi*g/2) if kern == "soft" else None, contrast=contrast,
               gp_residual_old=res_old, ward_old=w_old, gp_residual_new=res_new, ward_new=w_new, **m)
    print(f"[{label}] res {res_old:.1e}->{res_new:.1e} ward {w_old:+.4f}->{w_new:+.5f} contrast {contrast:.2f} "
          f"c2={m['c2']:.5f} cT={m['cT']:.5f} c1={m['c1']:.4f} c2/cT={m['c2']/m['cT']:.5f} F2={m['F2']:.5f} ({time.time()-t0:.0f}s)", flush=True)
    return rec, st2["psi"]

if __name__ == "__main__":
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    def save():
        json.dump(res, open(OUT, "w"), indent=1, default=float)
    jobs = [("soft_g44", 44.0, "soft", A["soft_g44"]["astar"], None, "stable", False),
            ("soft_g34", 34.0, "soft", A["soft_g34"]["astar"], None, "stable", False),
            ("soft_g28", 28.0, "soft", A["soft_g28"]["astar"], None, "stable", False),
            ("soft_g22", 22.0, "soft", A["soft_g22"]["astar"], 0.0951759, "stable", True),
            ("g6_g35", 35.0, "g6", A["g6_g35"]["astar"], None, "stable", False)]
    for k in ["20", "18", "17", "16", "15.5", "15", "14.5", "14", "13.5", "13"]:
        jobs.append((f"soft_g{k}", LOW[k]["g"], "soft", LOW[k]["astar"], LOW[k].get("f_s"), "stable", False))
    for lab, g, kern, a, fs, ph, gk in jobs:
        if lab in res: continue
        rec, _ = run(lab, g, kern, a, fs, ph, want_gk=gk); res[lab] = rec; save()
    # continuation chain (first leg's refine points), seeded downward
    seed = None
    for k, ph in [("13.25", "stable (continuation)"), ("13", "continuation"), ("12.9", "metastable"), ("12.8", "metastable"),
                  ("12.7", "metastable"), ("12.6", "metastable"), ("12.55", "metastable")]:
        lab = f"ref_g{k}"
        if lab in res:
            continue
        o = REF[k]
        rec, seed = run(lab, o["g"], "soft", o["astar"], o.get("f_s"), ph, seed=seed); res[lab] = rec; save()
    print("JOB A DONE", flush=True)
