#!/usr/bin/env python3
# g_tsh1_chatleg.py -- Gate G-TSH1 chat leg (from-scratch per election D3(a)).
# Locked pre-registration: G_TSH1_EXECUTION_PREREGISTRATION.md md5 c4b6c37b2abba7911329c6bebd6f5db7
# Corpus base: V4.67 canonical md5 3cef6d9832c448ecd0cb2f3cdd4c581c
# Stages: t1check | phase0 | phaseC | phase1 | phase2 | verdict   (verdict quarantined LAST)
# All quantities in substrate units (hbar = m = 1). No physical-unit statement exists in this file.
import numpy as np, json, hashlib, sys, os, time
from numpy.fft import fft2, ifft2
from scipy.special import j0, j1
from scipy.ndimage import maximum_filter

WD = "/home/claude/tsh1"
RES = os.path.join(WD, "g_tsh1_results.json")
LOCK_MD5 = "c4b6c37b2abba7911329c6bebd6f5db7"

def load_res():
    if os.path.exists(RES):
        with open(RES) as f: return json.load(f)
    return {"lock_md5": LOCK_MD5, "honesty": [], "deviations": []}

def save_res(r):
    with open(RES, "w") as f: json.dump(r, f, indent=1, default=float)

# ---------------- T1 self-grep (forbidden strings, list built by concat so the check cannot self-trip)
FORBID = ["2997"+"92458", "GW17"+"0817", "0.38"+"1966", "1.6"+"18", "0.14"+"5898",
          "1.2"+"162", "0.61"+"237", "0.57"+"735", "Cau"+"chy"]
def t1check():
    src = open(__file__, encoding="utf-8").read()
    bad = [s for s in FORBID if s in src]  # raw-source grep; the FORBID list itself is concat-split
    assert not bad, f"T1 VIOLATION: {bad}"
    print("[T1] forbidden-string grep clean on", os.path.basename(__file__))

# ---------------- kernels
def Uq_soft(q, g, R=1.0):
    x = np.asarray(q, float) * R
    out = np.full_like(x, 0.5)
    m = x > 1e-9
    out[m] = j1(x[m]) / x[m]
    return 2*np.pi*g*R*R*out

_G6 = {}
def Uq_g6(q, g, R=1.0):
    key = R
    if key not in _G6:
        r = np.linspace(0, 4*R, 4001)
        qs = np.linspace(0, 80, 8001)
        w = np.exp(-(r/R)**6) * r
        tab = np.array([np.trapezoid(w*j0(qq*r), r) for qq in qs])
        _G6[key] = (qs, 2*np.pi*tab)
    qs, tab = _G6[key]
    return g*np.interp(np.abs(q), qs, tab)

KFN = {"soft": Uq_soft, "g6": Uq_g6}

# ---------------- big-box quench (square, L=20, N=160, seed 7)
def quench(g, kern, L=20.0, N=160, rho0=1.0, seed=7, tau=40.0, dt=0.002):
    rng = np.random.default_rng(seed)
    psi = np.sqrt(rho0)*(1+0.1*(rng.standard_normal((N,N))+1j*rng.standard_normal((N,N))))
    k = 2*np.pi*np.fft.fftfreq(N, d=L/N)
    KX, KY = np.meshgrid(k, k, indexing="ij"); K2 = KX**2+KY**2
    Uk = KFN[kern](np.sqrt(K2), g)
    Kin = np.exp(-0.5*dt*0.5*K2)
    Ntot = rho0*L*L
    steps = int(tau/dt); Eprev = None
    for it in range(steps):
        psi = ifft2(Kin*fft2(psi))
        rho = np.abs(psi)**2
        Phi = ifft2(Uk*fft2(rho)).real
        psi = psi*np.exp(-dt*Phi)
        psi = ifft2(Kin*fft2(psi))
        psi *= np.sqrt(Ntot/(np.sum(np.abs(psi)**2)*(L/N)**2))
        if it % 2000 == 1999:
            c = fft2(psi)/N**2; rho = np.abs(psi)**2; rk = fft2(rho)/N**2
            E = (np.sum(0.5*K2*np.abs(c)**2)+0.5*np.sum(Uk*np.abs(rk)**2))*L*L
            if Eprev is not None and abs(E-Eprev) < 1e-8*abs(E): break
            Eprev = E
    return np.abs(psi)**2, L, N

def psi6(rho, L, N, a_guess=1.46):
    dx = L/N
    fp = max(3, int(0.5*a_guess/dx)//2*2+1)
    mx = maximum_filter(rho, size=fp, mode="wrap")
    pk = np.argwhere((rho == mx) & (rho > 0.5*rho.max()))
    P = pk*dx
    npk = len(P)
    if npk < 20: return 0.0, 0.0, npk
    s6 = 0j; s4 = 0j
    for j in range(npk):
        d = P - P[j]
        d -= L*np.round(d/L)
        r = np.hypot(d[:,0], d[:,1]); r[j] = 1e9
        nn = np.argsort(r)[:6]
        th = np.arctan2(d[nn,1], d[nn,0])
        s6 += np.mean(np.exp(6j*th)); s4 += np.mean(np.exp(4j*th))
    return abs(s6)/npk, abs(s4)/npk, npk

# ---------------- cell machinery (oblique p6m primitive cell, one droplet)
def cellgeom(a, Nc=96):
    a1 = np.array([a, 0.0]); a2 = np.array([0.5*a, np.sqrt(3)/2*a])
    b1 = (2*np.pi/a)*np.array([1.0, -1/np.sqrt(3)])
    b2 = (2*np.pi/a)*np.array([0.0,  2/np.sqrt(3)])
    m = np.fft.fftfreq(Nc)*Nc
    MM, NN = np.meshgrid(m, m, indexing="ij")
    Gx = MM*b1[0]+NN*b2[0]; Gy = MM*b1[1]+NN*b2[1]
    area = a*a*np.sqrt(3)/2
    s = (np.arange(Nc)+0.5)/Nc
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    X = S1*a1[0]+S2*a2[0]; Y = S1*a1[1]+S2*a2[1]
    return dict(a=a, a1=a1, a2=a2, b1=b1, b2=b2, Gx=Gx, Gy=Gy,
                G2=Gx**2+Gy**2, area=area, X=X, Y=Y, Nc=Nc)

def relax_cell(a, g, kern, rho0=1.0, Nc=96, dt=0.001, tau=6.0, psi_init=None):
    ge = cellgeom(a, Nc)
    Uk = KFN[kern](np.sqrt(ge["G2"]), g)
    Kin = np.exp(-0.5*dt*0.5*ge["G2"])
    Ntot = rho0*ge["area"]
    if psi_init is None:
        rc = 0.5*(ge["a1"]+ge["a2"])
        d2 = (ge["X"]-rc[0])**2+(ge["Y"]-rc[1])**2
        psi = np.exp(-d2/(2*0.35**2))+0.05+0j
    else:
        psi = psi_init.astype(complex)
    psi *= np.sqrt(Ntot/(np.sum(np.abs(psi)**2)*ge["area"]/Nc**2))
    Eprev = None
    for it in range(int(tau/dt)):
        psi = ifft2(Kin*fft2(psi))
        rho = np.abs(psi)**2
        Phi = ifft2(Uk*fft2(rho)).real
        psi = psi*np.exp(-dt*Phi)
        psi = ifft2(Kin*fft2(psi))
        psi *= np.sqrt(Ntot/(np.sum(np.abs(psi)**2)*ge["area"]/Nc**2))
        if it % 500 == 499:
            E = cell_energy(psi, ge, Uk)
            if Eprev is not None and abs(E-Eprev) < 1e-11*max(1,abs(E)): break
            Eprev = E
    rho = np.abs(psi)**2
    Phi = ifft2(Uk*fft2(rho)).real
    c = fft2(psi)/Nc**2; rk = fft2(rho)/Nc**2
    Ekin = np.sum(0.5*ge["G2"]*np.abs(c)**2)*ge["area"]
    Eint = 0.5*np.sum(Uk*np.abs(rk)**2)*ge["area"]
    mu = (Ekin+2*Eint)/Ntot
    return dict(psi=np.abs(psi), ge=ge, Uk=Uk, E_area=(Ekin+Eint)/ge["area"], mu=mu, Phi=Phi)

def cell_energy(psi, ge, Uk):
    Nc = ge["Nc"]
    c = fft2(psi)/Nc**2; rho = np.abs(psi)**2; rk = fft2(rho)/Nc**2
    return (np.sum(0.5*ge["G2"]*np.abs(c)**2)+0.5*np.sum(Uk*np.abs(rk)**2))*ge["area"]

def polish(st, stages=((1e-4, 20000), (3e-5, 15000))):
    """dt-staged split-step polish killing the Trotter-bias residual (F9 support; H3)."""
    ge = st["ge"]; Nc = ge["Nc"]; Uk = st["Uk"]
    psi = st["psi"].astype(complex); Ntot = 1.0*ge["area"]
    for dt, ns in stages:
        Kin = np.exp(-0.5*dt*0.5*ge["G2"])
        for _ in range(ns):
            psi = ifft2(Kin*fft2(psi)); rho = np.abs(psi)**2
            Phi = ifft2(Uk*fft2(rho)).real
            psi = psi*np.exp(-dt*Phi)
            psi = ifft2(Kin*fft2(psi))
            psi *= np.sqrt(Ntot/(np.sum(np.abs(psi)**2)*ge["area"]/Nc**2))
    psi = np.abs(psi)
    rho = psi**2; Phi = ifft2(Uk*fft2(rho)).real
    c = fft2(psi)/Nc**2; rk = fft2(rho)/Nc**2
    Ekin = np.sum(0.5*ge["G2"]*np.abs(c)**2)*ge["area"]
    Eint = 0.5*np.sum(Uk*np.abs(rk)**2)*ge["area"]
    st2 = dict(psi=psi, ge=ge, Uk=Uk, E_area=(Ekin+Eint)/ge["area"],
               mu=(Ekin+2*Eint)/Ntot, Phi=Phi)
    lap = ifft2(-ge["G2"]*fft2(psi)).real
    res = np.sqrt(np.mean((-0.5*lap+Phi*psi-st2["mu"]*psi)**2))/np.sqrt(np.mean(psi**2))
    return st2, float(res)

def ward_check(st, g, kern, tol_w2=-0.05, kf=0.005):
    unit = 2*np.pi/st["ge"]["a"]
    rr = bdg(st, g, kern, kf*unit*np.array([1.0, 0.0]), n=32, want_modes=False)
    return rr["w2min"], bool(rr["w2min"] > tol_w2)

def astar_scan(g, kern, lo=1.30, hi=1.60, npts=17, Nc=96):
    alist = np.linspace(lo, hi, npts); Es = []
    for a in alist:
        st = relax_cell(a, g, kern, Nc=Nc)
        Es.append(st["E_area"])
    Es = np.array(Es); i = int(np.argmin(Es))
    i0 = min(max(i,1), npts-2)
    x = alist[i0-1:i0+2]; y = Es[i0-1:i0+2]
    p = np.polyfit(x, y, 2)
    astar = -p[1]/(2*p[0]) if p[0] > 0 else alist[i]
    return float(astar), alist.tolist(), Es.tolist()

# ---------------- BdG on the cell:  omega^2 f = L(L+2X) f,  Hermitian M = L^1/2 (L+2X) L^1/2
def bdg(state, g, kern, qvec, n=32, nmodes=6, want_modes=True):
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
    negfrac = -ev.min()/max(ev.max(),1e-12)
    ev = np.clip(ev, 0, None)
    Lh = (V*np.sqrt(ev)) @ V.conj().T
    Ukq = KFN[kern](np.sqrt(kq2), g)
    Xq = Mpsi @ (Ukq[:,None]*Mpsi)
    M = Lh @ (Lq+2*Xq) @ Lh
    M = 0.5*(M+M.conj().T)
    w2, W = np.linalg.eigh(M)
    om = np.sqrt(np.clip(w2, 0, None))
    out = dict(om=om[:nmodes].tolist(), Lneg=float(negfrac), w2min=float(w2[0]))
    if want_modes:
        modes = []
        rho0 = psi0**2
        rG = fft2(rho0)/Nc**2
        dxr = ifft2(1j*ge["Gx"]*rG).real*Nc**2
        dyr = ifft2(1j*ge["Gy"]*rG).real*Nc**2
        A = np.stack([dxr.ravel(), dyr.ravel()], axis=1)
        AtA = A.T @ A
        qn = np.hypot(*qvec); qh = np.array(qvec)/qn
        qperp = np.array([-qh[1], qh[0]])
        okA = np.linalg.norm(A) > 1e-8
        for j in range(nmodes):
            f = Lh @ W[:, j]
            grid = np.zeros((Nc, Nc), complex)
            grid[mi % Nc, ni % Nc] = f
            fr = ifft2(grid)*Nc**2
            drho = psi0*fr
            b = drho.ravel()
            nb = np.vdot(b, b).real
            if okA and nb > 1e-20:
                s = np.linalg.solve(AtA, A.T @ b)
                pd = float(np.vdot(A@s, A@s).real/nb)
                sv = np.array([s[0], s[1]])
                pl = abs(sv @ qh)**2; pt = abs(sv @ qperp)**2
                fT = float(pt/(pl+pt)) if (pl+pt) > 0 else 0.0
            else:
                pd, fT = 0.0, 0.0
            modes.append(dict(om=float(om[j]), P=pd, fT=fT))
        out["modes"] = modes
    return out

def classify(mode):
    if mode["P"] < 0.5: return "phase"
    if mode["fT"] >= 0.8: return "T"
    if mode["fT"] <= 0.2: return "L"
    return "MIX"

def branch_speeds(state, g, kern, qhat, klist_frac, n=32):
    a = state["ge"]["a"]; unit = 2*np.pi/a
    rows = []
    for kf in klist_frac:
        q = kf*unit*np.array(qhat)
        r = bdg(state, g, kern, q, n=n)
        cl = [classify(m) for m in r["modes"]]
        rows.append(dict(kf=kf, k=kf*unit, modes=r["modes"], cls=cl, Lneg=r["Lneg"]))
    def pick(rows, want):
        ks, oms, extra = [], [], []
        for rw in rows:
            cand = [(m, c) for m, c in zip(rw["modes"], rw["cls"]) if c == want]
            if want == "L" and len(cand) > 1:
                cand = [max(cand, key=lambda t: t[0]["P"])]
            if len(cand) >= 1:
                m = cand[0][0]
                ks.append(rw["k"]); oms.append(m["om"]); extra.append((m["P"], m["fT"]))
        return np.array(ks), np.array(oms), extra
    return rows, pick

def fits(ks, oms, kfs, win):
    sel = [(kf >= win[0]-1e-9) and (kf <= win[1]+1e-9) for kf in kfs]
    k = ks[sel]; o = oms[sel]
    if len(k) < 3: return None
    c = float(np.sum(k*o)/np.sum(k*k))
    p = float(np.polyfit(np.log(k), np.log(o), 1)[0])
    return dict(c=c, p=p, npts=len(k))

# ---------------- stages ------------------------------------------------------
def phase0(r):
    t0 = time.time()
    rho, L, N = quench(22.0, "soft")
    p6, p4, npk = psi6(rho, L, N)
    print(f"[P0] quench g=22 soft: psi6={p6:.4f} psi4={p4:.4f} peaks={npk}  ({time.time()-t0:.0f}s)")
    astar, alist, Es = astar_scan(22.0, "soft")
    st, res = polish(relax_cell(astar, 22.0, "soft"))
    mu = st["mu"]
    print(f"[P0] a*={astar:.4f}  mu={mu:.4f}  E/A={st['E_area']:.4f}")
    unit = 2*np.pi/astar
    rr = bdg(st, 22.0, "soft", 0.002*unit*np.array([1.0, 0.0]), n=32)
    om = rr["om"]
    print(f"[P0] near-Gamma omegas: {['%.4f'%x for x in om[:5]]}")
    ideal = (20.0*20.0)/(np.sqrt(3)/2*astar**2)
    F1 = dict(
        psi6=p6, psi4=p4, npeaks=npk, ideal_peaks=ideal,
        # per Amendment 1 (author-authorized July 18, 2026; lock c4b6c37b untouched):
        psi6_pass=bool(p6 >= 0.814 and p6 > p4 and abs(npk-ideal)/ideal <= 0.10),
        astar=astar, astar_pass=bool(abs(astar-1.4576)/1.4576 <= 0.005),
        mu=mu, mu_pass=bool(55.6 <= mu <= 56.2),
        goldstone3=om[:4], gold_pass=bool(om[2] < 0.1*om[3]),
        gp_residual=res, w2min_tiny=rr["w2min"],
        ward_pass=bool(res <= 5e-3 and rr["w2min"] > -0.05))  # F9
    r["phase0"] = F1
    r["phase0"]["PASS"] = bool(all([F1["psi6_pass"], F1["astar_pass"], F1["mu_pass"],
                                    F1["gold_pass"], F1["ward_pass"]]))
    np.save(os.path.join(WD, "psi0_g22.npy"), st["psi"])
    r["phase0"]["astar_curve"] = dict(a=alist, E=Es)
    save_res(r)
    assert r["phase0"]["PASS"], f"F1 HALT: {F1}"
    print("[P0] PASS")

def load_state(g, kern, astar, Nc=96):
    st, res = polish(relax_cell(astar, g, kern, Nc=Nc))
    w2m, ok = ward_check(st, g, kern)
    assert res <= 5e-3 and ok, f"F9 WARD HALT: res={res:.2e} w2min={w2m:.3f}"
    return st

def phaseC(r):
    astar = r["phase0"]["astar"]
    # C-NEG: uniform superfluid, soft-core g=10 (below crystallization), same cell geometry
    stU = relax_cell(astar, 10.0, "soft", psi_init=np.ones((96, 96)))
    con = float(stU["psi"].max()/stU["psi"].min())
    unit = 2*np.pi/astar
    rows, pick = branch_speeds(stU, 10.0, "soft", [1.0, 0.0], [0.05, 0.10, 0.15], n=32)
    Tcount = sum(c == "T" for rw in rows for c in rw["cls"])
    gl = bdg(stU, 10.0, "soft", 0.002*unit*np.array([1.0, 0.0]), n=32)["om"]
    ngl = int(np.sum(np.array(gl[:5]) < 0.1*gl[5] if len(gl) > 5 else np.array(gl[:5]) < 0.05))
    F6 = dict(contrast=con, Tcount=Tcount, near_gamma=gl[:5], n_gapless=ngl,
              PASS=bool(Tcount == 0 and ngl == 1 and con < 1.02))
    print(f"[C-NEG] contrast={con:.4f} T-classified={Tcount} gapless={ngl} -> {'PASS' if F6['PASS'] else 'FAIL'}")
    # C-POS: classical triangular NN central springs (ks=m=1, a=1); analytic inside this control
    import sympy as sp
    qx, qy, aS, ks = sp.symbols("qx qy aS ks", positive=True)
    ebs = [sp.Matrix([1, 0]), sp.Matrix([sp.Rational(1, 2), sp.sqrt(3)/2]),
           sp.Matrix([-sp.Rational(1, 2), sp.sqrt(3)/2])]
    q = sp.Matrix([qx, qy])
    Dm = sp.zeros(2, 2)
    for e in ebs:
        Dm += 2*ks*sp.sin((q.T*e)[0]*aS/2)**2*(e*e.T)
    Dq = Dm.subs(qy, 0).applyfunc(lambda e: sp.series(e, qx, 0, 3).removeO())
    lam = list(sp.Matrix(Dq).eigenvals().keys())
    cs2 = sorted([sp.simplify(l/qx**2).subs({aS: 1, ks: 1}) for l in lam], key=lambda z: float(z))
    cT_sym, cL_sym = [float(sp.sqrt(c)) for c in cs2]
    def Dnum(qv, a=1.0, k_s=1.0):
        E = [np.array([1, 0.]), np.array([.5, np.sqrt(3)/2]), np.array([-.5, np.sqrt(3)/2])]
        D = np.zeros((2, 2))
        for e in E:
            D += 2*k_s*np.sin(np.dot(qv, e)*a/2)**2*np.outer(e, e)
        return D
    ks_ = np.array([0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.20])*2*np.pi
    cT_fit = []
    ok_pol = True
    for ang in [0.0, np.pi/6]:
        qh = np.array([np.cos(ang), np.sin(ang)])
        oms = []
        for kk in ks_:
            w2, V = np.linalg.eigh(Dnum(kk*qh))
            fTs = [abs(np.dot(V[:, i], [-qh[1], qh[0]]))**2 for i in range(2)]
            iT = int(np.argmax(fTs))
            ok_pol &= fTs[iT] >= 0.95
            oms.append(np.sqrt(w2[iT]))
        oms = np.array(oms)
        c = np.sum(ks_*oms)/np.sum(ks_**2)
        p = np.polyfit(np.log(ks_), np.log(oms), 1)[0]
        cT_fit.append(dict(ang=float(ang), c=float(c), p=float(p)))
    errs = [abs(d["c"]-cT_sym)/cT_sym for d in cT_fit]
    F7 = dict(cT_sym=cT_sym, cL_sym=cL_sym, fits=cT_fit, pol_ok=bool(ok_pol),
              PASS=bool(ok_pol and max(errs) <= 0.05  # 5% tol: finite-window sin-dispersion bias (H2)
                        and all(0.9 <= d["p"] <= 1.1 for d in cT_fit)))
    print(f"[C-POS] cT_sym={cT_sym:.5f} fits={[('%.5f' % d['c'], '%.3f' % d['p']) for d in cT_fit]} -> {'PASS' if F7['PASS'] else 'FAIL'}")
    r["phaseC"] = dict(C_NEG=F6, C_POS=F7)
    save_res(r)
    assert F6["PASS"], "F6 INSTRUMENT-NULL (C-NEG)"
    assert F7["PASS"], "F7 INSTRUMENT-NULL (C-POS)"
    print("[PC] controls PASS")

KLIST = [0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.20]
WIN_P = (0.05, 0.20); WIN_R = (0.03, 0.15)

def band_pass(st, g, kern, qhat, n, klist=KLIST):
    rows, pick = branch_speeds(st, g, kern, qhat, klist, n=n)
    kfs = [rw["kf"] for rw in rows]
    out = {}
    for lab in ["T", "L", "phase"]:
        ks, oms, ex = pick(rows, lab)
        kf_used = [rw["kf"] for rw in rows if lab in rw["cls"]]
        out[lab] = dict(k=ks.tolist(), om=oms.tolist(), kf=kf_used,
                        fit_P=fits(ks, oms, kf_used, WIN_P), fit_R=fits(ks, oms, kf_used, WIN_R))
    out["rows"] = [dict(kf=rw["kf"], cls=rw["cls"],
                        om=[m["om"] for m in rw["modes"]],
                        P=[round(m["P"], 3) for m in rw["modes"]],
                        fT=[round(m["fT"], 3) for m in rw["modes"]]) for rw in rows]
    return out

def phase1(r):
    astar = r["phase0"]["astar"]
    st = load_state(22.0, "soft", astar)
    t0 = time.time()
    GM = band_pass(st, 22.0, "soft", [1.0, 0.0], 32)          # Gamma-M along b1
    ang = np.array([np.cos(np.pi/6), np.sin(np.pi/6)])
    GK = band_pass(st, 22.0, "soft", ang.tolist(), 32)        # 30 deg = Gamma-K family
    print(f"[P1] n=32 both directions done ({time.time()-t0:.0f}s)")
    # convergence: n=40, Gamma-M, primary-window points
    sub = [kf for kf in KLIST if kf >= WIN_P[0]]
    GM40 = band_pass(st, 22.0, "soft", [1.0, 0.0], 40, klist=sub)
    r["phase1"] = dict(GM=GM, GK=GK, GM40=GM40)
    save_res(r)
    print("[P1] saved")

def sweep_point(r, g, kern, tag, arange=(1.30, 1.60), tau=40.0, gate=None):
    if gate is None:
        rho, L, N = quench(g, kern, tau=tau)
        p6, p4, npk = psi6(rho, L, N, a_guess=(1.55 if kern == "g6" else 1.46))
    else:
        p6, p4, npk = gate
    ok = bool(p6 >= 0.6 and p6 > p4)
    entry = dict(g=g, kern=kern, psi6=p6, psi4=p4, npeaks=npk, cryst=ok, tau_anneal=tau)
    print(f"[P2:{tag}] g={g} {kern}: psi6={p6:.3f} psi4={p4:.3f} cryst={ok}")
    if not ok:
        r["phase2"]["points"][tag] = entry; save_res(r); return
    astar, _, _ = astar_scan(g, kern, lo=arange[0], hi=arange[1])
    st, res = polish(relax_cell(astar, g, kern))
    w2m, wok = ward_check(st, g, kern)
    entry_ward = dict(res=res, w2min=w2m, ok=bool(res <= 5e-3 and wok))
    entry["astar"] = astar; entry["mu"] = st["mu"]; entry["ward"] = entry_ward
    assert entry_ward["ok"], f"F9 WARD HALT at {tag}: {entry_ward}"
    sub4 = [0.05, 0.10, 0.15, 0.20]
    B32 = band_pass(st, g, kern, [1.0, 0.0], 32, klist=KLIST)
    B32s = band_pass(st, g, kern, [1.0, 0.0], 32, klist=sub4)
    B40s = band_pass(st, g, kern, [1.0, 0.0], 40, klist=sub4)
    entry["B32"] = dict(T=B32["T"], L=B32["L"], rows=B32["rows"])
    def RT(B):
        fT = B["T"]["fit_P"]; fL = B["L"]["fit_P"]
        return (fT["c"]/fL["c"]) if (fT and fL) else None
    entry["RT32"] = RT(B32); entry["RT32sub"] = RT(B32s); entry["RT40sub"] = RT(B40s)
    entry["cT32"] = B32["T"]["fit_P"]["c"] if B32["T"]["fit_P"] else None
    entry["cL32"] = B32["L"]["fit_P"]["c"] if B32["L"]["fit_P"] else None
    print(f"[P2:{tag}] a*={astar:.4f} RT={entry['RT32']}")
    r["phase2"]["points"][tag] = entry; save_res(r)

def phase2(r):
    if "phase2" not in r: r["phase2"] = {"points": {}}
    # canonical g=22 point reuses phase1 numbers (recorded in verdict); axis (i) additions:
    for g in [28.0, 34.0, 44.0]:
        tag = f"soft_g{int(g)}"
        if tag not in r["phase2"]["points"]:
            sweep_point(r, g, "soft", tag)
    # axis (ii): gamma-6 kernel, g-grid {15,20,...,60}, first crystallizing value
    if "g6_choice" not in r["phase2"]:
        chosen = None; tried = []
        for g in [15, 20, 25, 30, 35, 40, 45, 50, 55, 60]:
            k = np.linspace(0.01, 12, 2000)
            crit = float(np.min(k**2/4 + Uq_g6(k, g)))
            tried.append(dict(g=g, uniform_min=crit))
            if crit >= 0: continue
            rho, L, N = quench(float(g), "g6")
            p6, p4, npk = psi6(rho, L, N, a_guess=1.55)
            tried[-1].update(psi6=p6, psi4=p4)
            print(f"[P2:g6] g={g} crit={crit:.2f} psi6={p6:.3f}")
            if p6 >= 0.6 and p6 > p4:
                chosen = g; break
            if len([t for t in tried if "psi6" in t]) >= 5: break
        r["phase2"]["g6_search"] = tried; r["phase2"]["g6_choice"] = chosen
        save_res(r)
    if r["phase2"]["g6_choice"] is not None and "g6" not in r["phase2"]["points"]:
        sweep_point(r, float(r["phase2"]["g6_choice"]), "g6", "g6", arange=(1.35, 1.72))
    save_res(r)
    print("[P2] done")

# ---------------- VERDICT (quarantined; reads results only; thresholds per locked Sections 4-6)
def verdict(r):
    v = {}
    P1 = r["phase1"]; GM, GK, GM40 = P1["GM"], P1["GK"], P1["GM40"]
    fTP, fTR = GM["T"]["fit_P"], GM["T"]["fit_R"]
    ok_lin = fTP and fTR and (0.9 <= fTP["p"] <= 1.1) and (0.9 <= fTR["p"] <= 1.1)
    quad = fTP and fTR and (1.8 <= fTP["p"] <= 2.2) and (1.8 <= fTR["p"] <= 2.2)
    exists = fTP is not None
    if not exists: q1 = "T-ABSENT"
    elif ok_lin: q1 = "T-LINEAR"
    elif quad: q1 = "T-NONLINEAR"
    else: q1 = "UNCLASSIFIED-HALT"
    cT, cL = (fTP["c"] if fTP else None), (GM["L"]["fit_P"]["c"] if GM["L"]["fit_P"] else None)
    # second sound = the lower L-classified gapless branch (supersolid: it carries lattice
    # character, P>=0.5, so the "phase" pick sees only gapped optical modes -- H4); secondary only.
    ks2, o2 = [], []
    for rw in GM["rows"]:
        cand = [om for om, c in zip(rw["om"], rw["cls"]) if c == "L" and om < 10.0]
        if cand and WIN_P[0]-1e-9 <= rw["kf"] <= WIN_P[1]+1e-9:
            ks2.append(rw["kf"]*2*np.pi/r["phase0"]["astar"]); o2.append(min(cand))
    ks2, o2 = np.array(ks2), np.array(o2)
    c2 = float(np.sum(ks2*o2)/np.sum(ks2*ks2)) if len(ks2) >= 3 else None
    conv = None
    if GM40["T"]["fit_P"] and GM40["L"]["fit_P"] and cT and cL:
        # same-subset comparison: refit n=32 on the n=40 k-subset
        dT = abs(GM40["T"]["fit_P"]["c"]-cT)/cT
        dL = abs(GM40["L"]["fit_P"]["c"]-cL)/cL
        conv = dict(dT=dT, dL=dL, PASS=bool(dT <= 0.01 and dL <= 0.01))
    iso = None
    if GK["T"]["fit_P"] and cT:
        iso = abs(GK["T"]["fit_P"]["c"]-cT)/cT
    v["Q1"] = dict(arm=q1, cT=cT, cL1=cL, c2=c2, RT=(cT/cL if cT and cL else None),
                   pP=fTP["p"] if fTP else None, pR=fTR["p"] if fTR else None,
                   conv=conv, iso_GK=iso)
    # ---- Q2
    pts = {"soft_g22": dict(RT32=v["Q1"]["RT"], cryst=True, astar=r["phase0"]["astar"])}
    pts.update(r.get("phase2", {}).get("points", {}))
    ax1 = [(t, p) for t, p in pts.items() if p.get("cryst") and t.startswith("soft") and p.get("RT32")]
    RTs = np.array([p["RT32"] for _, p in ax1])
    if len(ax1) < 3:
        q2 = "UNDERDETERMINED-HALT(axis-i points<3)"
        D1 = None
    else:
        D1 = float(np.max(np.abs(RTs-RTs.mean()))/RTs.mean())
        if D1 <= 0.03: ax1v = "PINNED"
        elif D1 >= 0.10: ax1v = "KNOB"
        else: ax1v = "UNDERDETERMINED"
        g6p = pts.get("g6"); D2 = None
        if g6p and g6p.get("cryst") and g6p.get("RT32"):
            allRT = np.append(RTs, g6p["RT32"])
            D2 = float(np.max(np.abs(allRT-allRT.mean()))/allRT.mean())
            if ax1v == "PINNED" and D2 <= 0.03: q2 = "FULLY-PINNED"
            elif ax1v == "PINNED" and D2 >= 0.10: q2 = "KERNEL-CLASS-PINNED"
            elif ax1v == "PINNED": q2 = "PINNED(axis-i); axis-ii UNDERDETERMINED"
            else: q2 = ax1v
        else:
            q2 = ax1v + " (axis-ii NOT-EVALUABLE)" if ax1v == "PINNED" else ax1v
    convs = []
    for t, p in pts.items():
        if p.get("RT32sub") and p.get("RT40sub"):
            convs.append(dict(tag=t, d=abs(p["RT40sub"]-p["RT32sub"])/p["RT32sub"]))
    v["Q2"] = dict(arm=q2, D_axis_i=D1, D_axis_ii=(D2 if len(ax1)>=3 else None), RT_points={t: p.get("RT32") for t, p in pts.items()},
                   conv=convs, import_set="in-set {kernel form, g, rho0}",
                   subclass=("DERIVED-OF-LOCATED-IMPORT" if q2 in
                             ("KNOB", "KERNEL-CLASS-PINNED") else
                             ("DERIVED-RATIO" if q2 == "FULLY-PINNED" else "n/a")))
    if v["Q1"]["arm"] == "T-LINEAR":
        head = f"Q1=T-LINEAR; Q2={q2}"
    elif v["Q1"]["arm"] in ("T-NONLINEAR", "T-ABSENT"):
        head = "CARRIER-ROUTE-CLOSED"
    else:
        head = v["Q1"]["arm"]
    v["HEADLINE"] = head
    r["verdict"] = v
    save_res(r)
    print(json.dumps(v, indent=1, default=float))

if __name__ == "__main__":
    stage = sys.argv[1]
    t1check()
    r = load_res()
    {"t1check": lambda r: None, "phase0": phase0, "phaseC": phaseC,
     "phase1": phase1, "phase2": phase2, "verdict": verdict}[stage](r)
