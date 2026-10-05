#!/usr/bin/env python3
"""
lbc_weights.py -- Longitudinal branch coupling (exploration mode, base V4.88).

Reuses the G-TSH1 chat-leg instrument verbatim (cell geometry, relax, polish, BdG pencil):
  g_tsh1_chatleg.py  (gate_tsh1_staging/, branch claude/sqt-framework-perspectives-kMZyw)
and adds ONE new quantity: the long-wavelength density matrix element of every BdG mode,
  rho_nu(q) = <psi0 | f+_nu>_q   (G=0 Bloch component of delta-rho = psi0 * f+),
with BdG normalisation <f+, f->=1  ==>  f+ = L^{1/2} W / sqrt(omega),  |W| = 1.
Spectral weight Z_nu(q) = |rho_nu(q)|^2 (per primitive cell, N_cell = rho0 * area particles).
Checks: f-sum  sum_nu omega_nu Z_nu = N_cell q^2 / 2 ;  static  sum_nu 2 Z_nu/omega_nu = chi_static(q)
from a direct solve of (L+2X) f = -2 V psi0 with V = e^{iq.r}.
Substrate units (hbar = m = 1). No physical-unit statement exists in this file.
"""
import sys, os, json, time
import numpy as np
from numpy.fft import fft2, ifft2

sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging")
import g_tsh1_chatleg as T   # the instrument of record (functions only; its __main__ is guarded)

OUT = "/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc"

# ----------------------------------------------------------------------------- BdG with weights
def bdg_full(state, g, kern, qvec, n=32):
    """Same pencil as g_tsh1_chatleg.bdg, but returns ALL eigenpairs plus the density
    matrix element of each mode and the direct static response."""
    ge = state["ge"]; Nc = ge["Nc"]
    psi0 = state["psi"]; mu = state["mu"]
    ph = fft2(psi0)/Nc**2
    Phih = fft2(state["Phi"])/Nc**2
    mlist = np.arange(n)-n//2
    Mi, Ni = np.meshgrid(mlist, mlist, indexing="ij")
    mi = Mi.ravel(); ni = Ni.ravel(); P = n*n
    Gx = mi*ge["b1"][0]+ni*ge["b2"][0]; Gy = mi*ge["b1"][1]+ni*ge["b2"][1]
    dm = (mi[:,None]-mi[None,:]) % Nc
    dn = (ni[:,None]-ni[None,:]) % Nc
    Mpsi = ph[dm, dn]
    MPhi = Phih[dm, dn]
    kq2 = (Gx+qvec[0])**2+(Gy+qvec[1])**2
    Lq = 0.5*np.diag(kq2)+MPhi-mu*np.eye(P)
    Lq = 0.5*(Lq+Lq.conj().T)
    ev, V = np.linalg.eigh(Lq)
    lmin = float(ev.min())
    evc = np.clip(ev, 0, None)
    Lh = (V*np.sqrt(evc)) @ V.conj().T
    Ukq = T.KFN[kern](np.sqrt(kq2), g)
    Xq = Mpsi @ (Ukq[:,None]*Mpsi)
    M = Lh @ (Lq+2*Xq) @ Lh
    M = 0.5*(M+M.conj().T)
    w2, W = np.linalg.eigh(M)
    om = np.sqrt(np.clip(w2, 0, None))
    # psi0 plane-wave coefficient vector on the same basis (anti-aliased like the Toeplitz blocks)
    psivec = ph[mi % Nc, ni % Nc]
    area = ge["area"]
    # density matrix element: rho_nu(q) = int_cell e^{-iq r} psi0 f+ = area * sum_G conj(psi_G) f_G,
    # with f+ normalised so that int_cell (|u|^2-|v|^2) = 1, i.e. Euclidean <f+,f-> = 1/area:
    # Euclidean <W,MW>/om = om |W|^2 = 1/area  ->  f+ = Lh W / sqrt(om * area).
    Fplus = Lh @ W                      # columns: unnormalised f+ for each mode
    with np.errstate(divide="ignore", invalid="ignore"):
        scale = np.where(om > 1e-9, 1.0/np.sqrt(om*area), 0.0)
    Fplus = Fplus * scale[None, :]
    rho_q = area * (psivec.conj() @ Fplus)
    Z = np.abs(rho_q)**2
    # direct static response:  (L+2X) f = -2 V psi0,  V = e^{iq.r}  -> coefficient vector = psivec
    A = Lq + 2*Xq
    f_static = np.linalg.solve(A, -2.0*psivec)
    chi_static = -float((area * (psivec.conj() @ f_static)).real)   # -delta rho_q per unit V (per cell)
    # lattice-displacement / transverse classifier of the instrument (for the 6 lowest modes)
    cls = []
    rho0 = psi0**2
    rG = fft2(rho0)/Nc**2
    dxr = ifft2(1j*ge["Gx"]*rG).real*Nc**2
    dyr = ifft2(1j*ge["Gy"]*rG).real*Nc**2
    Amat = np.stack([dxr.ravel(), dyr.ravel()], axis=1); AtA = Amat.T @ Amat
    qn = np.hypot(*qvec); qh = np.array(qvec)/qn; qperp = np.array([-qh[1], qh[0]])
    for j in range(6):
        f = Lh @ W[:, j]
        grid = np.zeros((Nc, Nc), complex); grid[mi % Nc, ni % Nc] = f
        fr = ifft2(grid)*Nc**2; b = (psi0*fr).ravel(); nb = np.vdot(b, b).real
        s = np.linalg.solve(AtA, Amat.T @ b)
        pd = float(np.vdot(Amat@s, Amat@s).real/nb) if nb > 1e-20 else 0.0
        pl = abs(s @ qh)**2; pt = abs(s @ qperp)**2
        fT = float(pt/(pl+pt)) if (pl+pt) > 0 else 0.0
        cls.append(T.classify(dict(P=pd, fT=fT)))
    return dict(om=om, Z=Z, chi_static=chi_static, Lmin=lmin, cls=cls, Ncell=float(area))


def run_point(tag, g, kern, astar, kfs, dirs, n=32, Nc=96, res=None):
    """Rebuild the state at (g, kern, a*) exactly as the instrument does, then measure."""
    t0 = time.time()
    st, gpres = T.polish(T.relax_cell(astar, g, kern, Nc=Nc))
    w2m, wok = T.ward_check(st, g, kern)
    print(f"[{tag}] state rebuilt: mu={st['mu']:.5f} E/A={st['E_area']:.5f} GP-residual={gpres:.2e} "
          f"Ward w2min={w2m:.3e} ({'ok' if wok else 'FAIL'})  {time.time()-t0:.0f}s", flush=True)
    unit = 2*np.pi/astar
    out = dict(tag=tag, g=g, kern=kern, astar=astar, mu=st["mu"], E_area=st["E_area"],
               gp_residual=gpres, ward_w2min=w2m, Ncell=float(st["ge"]["area"]), n=n, rows=[])
    for dname, qhat in dirs.items():
        for kf in kfs:
            q = kf*unit*np.array(qhat); qn = kf*unit
            r = bdg_full(st, g, kern, q, n=n)
            om, Z = r["om"], r["Z"]
            Ncell = r["Ncell"]
            fsum = float(np.sum(om*Z)); fsum_exact = Ncell*qn**2/2
            stat = float(np.sum(2*Z[om > 1e-9]/om[om > 1e-9]))
            # the three gapless branches = the three lowest modes (sorted); identify by instrument class
            low = [dict(i=i, om=float(om[i]), Z=float(Z[i]), Zq=float(Z[i]/qn),
                        fshare=float(om[i]*Z[i]/fsum_exact), sshare=float((2*Z[i]/om[i])/stat if om[i] > 1e-9 else 0.0),
                        cls=r["cls"][i]) for i in range(6)]
            gapped_f = float(np.sum(om[6:]*Z[6:])/fsum_exact)
            row = dict(dir=dname, kf=kf, q=qn, modes=low, fsum=fsum, fsum_exact=fsum_exact,
                       fsum_ratio=fsum/fsum_exact, static_modesum=stat, static_direct=r["chi_static"],
                       static_ratio=stat/r["chi_static"], gapped_fshare=gapped_f, Lmin=r["Lmin"])
            out["rows"].append(row)
            m = low
            print(f"[{tag} {dname} kf={kf:.3f}] om={[f'{x['om']:.4f}' for x in m[:3]]} cls={[x['cls'] for x in m[:3]]} "
                  f"Z/q={[f'{x['Zq']:.4f}' for x in m[:3]]} fshare={[f'{x['fshare']:.4f}' for x in m[:3]]} "
                  f"gapped_f={gapped_f:.2e} | fsum {fsum/fsum_exact:.6f} static {stat/r['chi_static']:.6f}", flush=True)
    if res is not None:
        res[tag] = out
        with open(os.path.join(OUT, "lbc_results.json"), "w") as f:
            json.dump(res, f, indent=1, default=float)
    return out, st


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "canon"
    path = os.path.join(OUT, "lbc_results.json")
    res = json.load(open(path)) if os.path.exists(path) else {}
    dirs = {"GM": [1.0, 0.0], "GK": [np.cos(np.pi/6), np.sin(np.pi/6)]}
    if which == "canon":
        # canonical point of record (G-TSH1 phase-0): a* = 1.4574710087903182, g = 22 soft-core
        kfs = [0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20]
        run_point("soft_g22", 22.0, "soft", 1.4574710087903182, kfs, dirs, n=32, res=res)
    elif which == "conv":
        kfs = [0.02, 0.05, 0.10]
        run_point("soft_g22_n40", 22.0, "soft", 1.4574710087903182, kfs, {"GM": [1.0, 0.0]}, n=40, res=res)
    elif which == "sweep":
        # G-TSH1 axis-(i) points; a* re-scanned by the instrument's own astar_scan
        kfs = [0.02, 0.05, 0.10]
        for g in [28.0, 34.0, 44.0]:
            astar, _, _ = T.astar_scan(g, "soft")
            run_point(f"soft_g{int(g)}", g, "soft", astar, kfs, {"GM": [1.0, 0.0]}, n=32, res=res)
    elif which == "g6":
        kfs = [0.02, 0.05, 0.10]
        astar, _, _ = T.astar_scan(35.0, "g6", lo=1.35, hi=1.72)
        run_point("g6_g35", 35.0, "g6", astar, kfs, {"GM": [1.0, 0.0]}, n=32, res=res)
