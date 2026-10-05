#!/usr/bin/env python3
"""First leg: superfluid fraction for the Table 2 rows that lacked one (g = 44, 34, 28, the gamma6 kernel at 35,
and the metastable 12.4; 12.5 recomputed as a check). Same instrument and route as the rest of the column:
the state is rebuilt at the first leg's a* (relax_cell + polish + tight, as in jobA_2d.py) and f_s comes from the
energy of a Bloch phase twist, E(k) - E(0) = (1/2) N f_s k^2 with k = 0.02 (fs_twist, verbatim from
step4/lbc_sweep_low.py). The metastable points follow jobC_melt.py: seeded continuation at the second leg's a*."""
import sys, json, time
import numpy as np
from numpy.fft import fft2, ifft2
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging"); import g_tsh1_chatleg as T
from gsolve2d import tight, residual

def fs_twist(st, g, k=0.02, dt=1e-4, nsteps=12000):
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
    return float((E1-E0)/(0.5*N*k*k))

A = json.load(open("jobA_2d.json"))
out = {}; t0 = time.time()
def save(): json.dump(out, open("fs_rows.json", "w"), indent=1, default=float)
def build(a, g, kern, seed=None):
    st = T.relax_cell(a, g, kern, Nc=96, psi_init=seed)
    st, _ = T.polish(st); st, _, _ = tight(st)
    res, _, _ = residual(st["psi"], st["ge"], st["Uk"])
    rho = st["psi"]**2
    return st, float(res), float((rho.max()-rho.min())/rho.mean())
for lab, g, kern in (("soft_g44", 44.0, "soft"), ("soft_g34", 34.0, "soft"), ("soft_g28", 28.0, "soft"), ("g6_g35", 35.0, "g6")):
    a = A[lab]["astar"]; st, res, con = build(a, g, kern)
    fs = fs_twist(st, g)
    out[lab] = dict(g=g, kernel=kern, astar=a, gp_residual=res, contrast=con, f_s=fs)
    print(f"[{lab}] a*={a:.5f} res={res:.1e} contrast={con:.2f} f_s={fs:.6f} ({time.time()-t0:.0f}s)", flush=True); save()
# metastable continuation (jobC_melt.py's path and a* values)
seed = None
for g, a in [(12.55, 1.514654767906371), (12.50, 1.51529816851384), (12.45, 1.516002330056777), (12.40, 1.5168103105250197)]:
    st, res, con = build(a, g, "soft", seed)
    seed = st["psi"] if con > 0.05 else seed
    if g in (12.50, 12.40):
        fs = fs_twist(st, g)
        out[f"meta_g{g}"] = dict(g=g, kernel="soft", astar=a, gp_residual=res, contrast=con, f_s=fs)
        print(f"[meta g={g}] a={a:.5f} res={res:.1e} contrast={con:.2f} f_s={fs:.6f} ({time.time()-t0:.0f}s)", flush=True); save()
    else:
        print(f"[meta g={g}] seed step, contrast={con:.2f} ({time.time()-t0:.0f}s)", flush=True)
print("FS_ROWS DONE", flush=True)
