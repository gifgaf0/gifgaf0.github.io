#!/usr/bin/env python3
"""
lbc_3d.py -- 3D check of the branch weights on the G-TSH4 AB (hcp) stack, step kernel,
Lambda = 2 Lambda_c, using the CC G-TSH4 route-D machinery verbatim (tsh4_core / tsh4_routeD,
gtsh4_gate/ on main) plus the density matrix element of each BdG mode.
The state is relaxed INSIDE the plane-wave cutoff (D.relax_truncated) so the Goldstone floor
is clean before weights are read.  Substrate units; <n> = 1.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "/home/claude/gifgaf0/gifgaf0.github.io/gtsh4_gate")
import tsh4_core as C
import tsh4_routeD as D

OUT = "/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc"
GCUT = 22.0; PPL = 30
S3 = np.sqrt(3.0)

def ev(x): x = int(round(x)); return x + (x & 1)

def bdg_weights(basis, khat, Lam, mu, q, nlow=10):
    NG = basis.NG; m = basis.m; G = basis.G
    q = np.asarray(q, float)
    dm = m[:, None, :] - m[None, :, :]
    rho_d = basis.coef(basis.rho_full, dm)
    phi_d = basis.coef(basis.phi_full, dm)
    Gdiff = (dm[..., 0, None]*basis.Binv[:, 0] + dm[..., 1, None]*basis.Binv[:, 1]
             + dm[..., 2, None]*basis.Binv[:, 2])
    absGd = np.sqrt((Gdiff**2).sum(-1))
    L0 = Lam*khat(absGd.ravel()).reshape(absGd.shape)*rho_d
    qa = q[None, :] + G
    L0 = L0 + np.diag(0.5*(qa*qa).sum(1) - mu)
    Uq = khat(np.sqrt((qa**2).sum(1)))
    X = Lam*(phi_d*Uq[None, :]) @ phi_d.conj().T
    L0 = 0.5*(L0 + L0.conj().T); X = 0.5*(X + X.conj().T)
    w, V = np.linalg.eigh(L0)
    lmin = float(w.min())
    sq = (V*np.sqrt(np.clip(w, 0.0, None))) @ V.conj().T
    A_plus = L0 + 2*X
    Mmat = sq @ A_plus @ sq; Mmat = 0.5*(Mmat + Mmat.conj().T)
    w2, VM = np.linalg.eigh(Mmat)
    om = np.sqrt(np.clip(w2, 0.0, None))
    vol = abs(np.linalg.det(basis.H))
    phiG = basis.coef(basis.phi_full, m)                 # psi0 coefficients on the basis
    F = sq @ VM
    with np.errstate(divide="ignore", invalid="ignore"):
        F = F * np.where(om > 1e-9, 1.0/np.sqrt(om*vol), 0.0)[None, :]
    rho_q = vol*(phiG.conj() @ F)
    Z = np.abs(rho_q)**2
    qn = float(np.linalg.norm(q))
    fsum_exact = vol*qn**2/2
    fsum = float(np.sum(om*Z))
    ok = om > 1e-9
    stat = float(np.sum(2*Z[ok]/om[ok]))
    f_static = np.linalg.solve(A_plus, -2.0*phiG)
    chi_direct = -float((vol*(phiG.conj() @ f_static)).real)
    return dict(q=qn, om=om[:nlow].tolist(), Z=Z[:nlow].tolist(), Zq=(Z[:nlow]/qn).tolist(),
                fshare=(om[:nlow]*Z[:nlow]/fsum_exact).tolist(),
                sshare=[(2*Z[i]/om[i])/stat if om[i] > 1e-9 else 0.0 for i in range(nlow)],
                fsum_ratio=fsum/fsum_exact, static_ratio=stat/chi_direct, chi_direct=chi_direct,
                gapped_fshare=float(np.sum(om[nlow:]*Z[nlow:])/fsum_exact), L0_min=lmin, vol=vol)

def main():
    t0 = time.time()
    ph = json.load(open("/home/claude/gifgaf0/gifgaf0.github.io/gtsh4_gate/tsh4_phase0_measurements.json"))
    lc, kstar = C.lambda_c(C.step_khat, 40.0); Lam = 2*lc
    khat = C.step_khat
    a, c = ph['results']['step']['structures']['AB']['params']
    H = np.diag([a, a*S3, c]).astype(float)
    sites = C.STRUCTURES['AB']['sites']
    lens = np.diag(H); n = tuple(ev(PPL*l) for l in lens)
    cell = C.Cell(list(lens), n); kg = C.khat_grid(cell, khat)
    psi = cell.seed(sites, 0.24*lens[0])
    psi, e, res, it, _ = C.relax(cell, kg, Lam, psi, dt=0.008, restol=1e-10)
    print(f"[3D] AB a={a:.5f} c={c:.5f} Lam={Lam:.4f} grid={n} relax: e={e:.6f} res={res:.2e} it={it} ({time.time()-t0:.0f}s)", flush=True)
    psi_t, mu_t, e_t, res_t = D.relax_truncated(cell, kg, Lam, GCUT, psi)
    print(f"[3D] in-basis relax: e={e_t:.6f} mu={mu_t:.5f} res={res_t:.2e} ({time.time()-t0:.0f}s)", flush=True)
    basis = D.PWBasis(H, psi_t, GCUT)
    print(f"[3D] NG={basis.NG}", flush=True)
    out = dict(a=a, c=c, Lam=Lam, grid=list(n), e=e_t, mu=mu_t, res=res_t, NG=basis.NG, gcut=GCUT, rows=[])
    r0 = bdg_weights(basis, khat, Lam, mu_t, np.array([1e-4, 0, 0]))
    print(f"[3D] near-Gamma om: {[f'{x:.4f}' for x in r0['om'][:8]]}  L0_min={r0['L0_min']:.2e}", flush=True)
    out["near_gamma"] = r0
    for lbl, d in (("basal_GM", [1, 0, 0]), ("axial", [0, 0, 1]), ("basal_GK", [np.cos(np.pi/6), np.sin(np.pi/6), 0])):
        d = np.array(d, float); d /= np.linalg.norm(d)
        for qm in [0.15, 0.3, 0.6]:
            r = bdg_weights(basis, khat, Lam, mu_t, qm*d); r["dir"] = lbl
            out["rows"].append(r)
            print(f"[3D {lbl} q={qm}] om={[f'{x:.4f}' for x in r['om'][:8]]}\n      Z/q={[f'{x:.4f}' for x in r['Zq'][:8]]}\n      fshare={[f'{x:.4f}' for x in r['fshare'][:8]]} gapped={r['gapped_fshare']:.2e} | fsum {r['fsum_ratio']:.6f} static {r['static_ratio']:.6f} ({time.time()-t0:.0f}s)", flush=True)
            with open(os.path.join(OUT, "lbc_3d.json"), "w") as f: json.dump(out, f, indent=1, default=float)

if __name__ == "__main__":
    main()
