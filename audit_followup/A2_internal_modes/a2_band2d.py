#!/usr/bin/env python3
"""A2 / DR-A2-1 (first leg): the internal L_perp band of the canonical 2D crystal (MV-G1 lineage, soft core, g = 22).

Internal fluctuations delta psi_perp (perpendicular, in C^8, to the condensate direction) carry no density at
linear order, so they obey i d_t delta psi_perp = L_perp delta psi_perp with
    L_perp = -(1/2) grad^2 + U*rho0 - mu      (the stationary GP operator; L_perp psi0 = 0),
and their frequencies are the eigenvalues of L_perp at Bloch wavevector q (first-order dynamics: omega = eps, not sqrt).
The state is rebuilt exactly as the two-leg-closed first leg did (relax_cell -> polish -> gsolve2d.tight at a*).
Locked pre-registration: A2_PREREG.md md5 fd2e95973de02d9a0e6d719cb579ccc0.
"""
import sys, json, hashlib, time, math
import numpy as np
from numpy.fft import fft2
REPO = "/home/claude/gifgaf0.github.io"
sys.path.insert(0, REPO + "/lbc_bank/deps"); import g_tsh1_chatleg as T
sys.path.insert(0, REPO + "/lbc_bank/closure"); from gsolve2d import tight, residual

assert hashlib.md5(open(REPO + "/audit_followup/A2_internal_modes/A2_PREREG.md", "rb").read()).hexdigest() == "fd2e95973de02d9a0e6d719cb579ccc0"
A = json.load(open(REPO + "/lbc_bank/closure/jobA_2d.json"))["soft_g22"]
astar, g, kern = A["astar"], 22.0, "soft"
FS_BANKED = A["f_s"]                       # 0.0951759 (phase-twist route, two-leg)
t0 = time.time()
st = T.relax_cell(astar, g, kern, Nc=96)
st, r_pol = T.polish(st)
st, r_lb, r_nk = tight(st)
res, mu, _ = residual(st["psi"], st["ge"], st["Uk"])
print(f"state: a*={astar:.10f}  mu={mu:.6f} (banked {A['mu_c']:.6f})  GP residual {res:.2e}  ({time.time()-t0:.0f}s)", flush=True)

def L_matrix(st, q, n):
    ge = st["ge"]; Nc = ge["Nc"]
    Phih = fft2(st["Phi"])/Nc**2
    ml = np.arange(n) - n//2
    Mi, Ni = np.meshgrid(ml, ml, indexing="ij"); mi = Mi.ravel(); ni = Ni.ravel()
    Gx = mi*ge["b1"][0] + ni*ge["b2"][0]; Gy = mi*ge["b1"][1] + ni*ge["b2"][1]
    dm = (mi[:, None] - mi[None, :]) % Nc; dn = (ni[:, None] - ni[None, :]) % Nc
    L = 0.5*np.diag((Gx + q[0])**2 + (Gy + q[1])**2) + Phih[dm, dn] - st["mu"]*np.eye(n*n)
    return 0.5*(L + L.conj().T)

unit = 2*np.pi/astar
dirs = {"0deg": np.array([1.0, 0.0]), "30deg": np.array([math.cos(math.pi/6), math.sin(math.pi/6)]),
        "90deg": np.array([0.0, 1.0])}
KF = [0.0, 0.0025, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.10]
out = {"state": dict(astar=astar, mu=mu, gp_residual=res, f_s_banked=FS_BANKED), "bands": {}, "fits": {}}
for n in (24, 32, 40):
    for dname, dvec in dirs.items():
        rows = []
        for kf in KF:
            ev = np.linalg.eigvalsh(L_matrix(st, kf*unit*dvec, n))
            rows.append(dict(kf=kf, q=kf*unit, e0=float(ev[0]), e1=float(ev[1]), e2=float(ev[2])))
        out["bands"][f"n{n}_{dname}"] = rows
        e00 = rows[0]["e0"]
        qs = np.array([r["q"] for r in rows[1:]]); de = np.array([r["e0"] - e00 for r in rows[1:]])
        # exponent from the two smallest q
        p_small = float(np.log(de[1]/de[0])/np.log(qs[1]/qs[0]))
        # fit de = A q^2 + B q^4 on kf <= 0.05
        msk = np.array([r["kf"] <= 0.05 for r in rows[1:]])
        M = np.stack([qs[msk]**2, qs[msk]**4], axis=1); coef, *_ = np.linalg.lstsq(M, de[msk], rcond=None)
        mstar = 1.0/(2*coef[0])
        out["fits"][f"n{n}_{dname}"] = dict(e0_Gamma=e00, gap_Gamma_band2=rows[0]["e1"] - e00, p_small=p_small,
                                            A=float(coef[0]), B=float(coef[1]), mstar=float(mstar), m_over_mstar=float(1/mstar),
                                            landau_ratio_smallest_q=float(de[0]/qs[0]))
        f = out["fits"][f"n{n}_{dname}"]
        print(f"n={n:2d} {dname:6s} eps0(Gamma)={e00:+.2e}  exponent p={p_small:.4f}  m*={mstar:.5f}  m/m*={1/mstar:.6f}"
              f"  (f_s banked {FS_BANKED:.6f}; rel diff {abs(1/mstar-FS_BANKED)/FS_BANKED:.2e})  gap to band 2 at Gamma {f['gap_Gamma_band2']:.4f}"
              f"  eps0/q at smallest q {f['landau_ratio_smallest_q']:.2e}", flush=True)

# band edges at the zone-boundary points (n = 32): M at b1/2 and K at (b1 + b2)/3 ... computed from the cell geometry
ge = st["ge"]; b1, b2 = ge["b1"], ge["b2"]
for lab, qv in (("M=b1/2", 0.5*b1), ("M'=b2/2", 0.5*b2), ("K=(2b1+b2)/3", (2*b1 + b2)/3), ("K'=(b1+2b2)/3", (b1 + 2*b2)/3)):
    ev = np.linalg.eigvalsh(L_matrix(st, qv, 32))
    out["bands"][f"zone_{lab}"] = [float(x) for x in ev[:4]]
    print(f"  {lab:14s} |q|={np.hypot(*qv):.4f}  lowest L_perp eigenvalues {ev[:4].round(5)}", flush=True)
json.dump(out, open(REPO + "/audit_followup/A2_internal_modes/a2_band2d.json", "w"), indent=1, default=float)
print(f"done ({time.time()-t0:.0f}s)")
