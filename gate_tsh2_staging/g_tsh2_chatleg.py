#!/usr/bin/env python3
# g_tsh2_chatleg.py — Gate G-TSH2, chat leg, from scratch.
# Executed under G_TSH2_PREREGISTRATION_LOCKED.md, lock md5 99eb26a5d8ff1e32c54d5cff40386098.
# Phases: tables | p0 | p1 <K3|K4|K5|K6> | p2 <K3|K4|K5|K6> | p3
# T1 self-grep at every invocation (patterns assembled from fragments; H1-precedent guard).
import numpy as np, json, sys, os
from scipy.special import j0, j1, jv
from scipy.linalg import eigh, inv
from scipy.interpolate import CubicSpline

OUT = '/home/claude/gtsh2'
os.makedirs(OUT, exist_ok=True)
RNG = np.random.default_rng(20260719)

# ---------------- T1 self-grep ----------------
def t1_grep():
    pats = ["299" + "792458", "2.9" + "979", "GW" + "170817",
            "1.6" + "180", "0.6" + "180", "137" + ".03"]
    files = [os.path.abspath(__file__)]
    am = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arm_mapper.py')
    if os.path.exists(am):
        files.append(am)
    for f in files:
        s = open(f, 'r', errors='ignore').read()
        for p in pats:
            if p in s:
                print("T1 SELF-GREP TRIP:", p, "in", f); sys.exit(3)
    print("T1 grep clean:", len(files), "file(s)")
t1_grep()

# ---------------- kernels ----------------
def uhat_step(k):
    k = np.asarray(k, float); s = np.where(k < 1e-9, 1.0, k)
    out = 2*np.pi*j1(s)/s
    return np.where(k < 1e-9, np.pi, out)

def uhat_cap(k):
    k = np.asarray(k, float); s = np.where(k < 1e-9, 1.0, k)
    out = 4*np.pi*jv(2, s)/s**2
    return np.where(k < 1e-9, np.pi/2, out)

_gam_cache = {}
def uhat_gamma(gam):
    if gam in _gam_cache:
        return _gam_cache[gam]
    d = np.load(f'{OUT}/uhat_gam{gam}.npz')
    cs = CubicSpline(d['k'], d['u']); kmax = float(d['k'][-1])
    def fn(k):
        k = np.asarray(k, float); out = np.zeros_like(k)
        m = k <= kmax; out[m] = cs(k[m]); return out
    _gam_cache[gam] = fn; return fn

KDEF = {
 'K3': dict(gam=4,   grid=list(range(85, 150, 5)),  apred=1.472, fam='gamma'),
 'K4': dict(gam=8,   grid=list(range(25, 90, 5)),   apred=1.490, fam='gamma'),
 'K5': dict(gam=12,  grid=list(range(20, 85, 5)),   apred=1.460, fam='gamma'),
 'K6': dict(gam=None, grid=list(range(110, 175, 5)), apred=1.137, fam='cap'),
}
def kernel_fn(K):
    return uhat_cap if KDEF[K]['fam'] == 'cap' else uhat_gamma(KDEF[K]['gam'])

def build_tables():
    for gam in (4, 8, 12):
        ks = np.arange(0.0, 100.0001, 0.02)
        out = np.empty_like(ks)
        def tr(kv, rmax, dr):
            r = np.arange(dr, rmax, dr); w = r/(1.0 + r**gam)
            return np.array([2*np.pi*np.trapezoid(w*j0(k*r), r) for k in kv])
        lo = ks <= 2.0
        out[lo] = tr(ks[lo], 400.0 if gam == 4 else 120.0, 0.002)
        out[~lo] = tr(ks[~lo], 80.0, 0.002)
        out[0] = 2*np.pi*(np.pi/gam)/np.sin(2*np.pi/gam)
        np.savez(f'{OUT}/uhat_gam{gam}.npz', k=ks, u=out)
        print(f"table gam={gam}: U0={out[0]:.6f} min={out.min():.6f} at k={ks[out.argmin()]:.2f}")

# ---------------- cell ----------------
class Cell:
    def __init__(self, a1, a2, n, uf, g):
        self.a1 = np.array(a1, float); self.a2 = np.array(a2, float)
        self.n = n; self.g = g; self.uf = uf
        self.A = abs(self.a1[0]*self.a2[1] - self.a1[1]*self.a2[0])
        M = np.array([self.a1, self.a2]); B = 2*np.pi*np.linalg.inv(M).T
        self.b1, self.b2 = B[0], B[1]
        m = np.fft.fftfreq(n, 1.0/n)
        M1, M2 = np.meshgrid(m, m, indexing='ij')
        self.M1, self.M2 = M1, M2
        self.Gx = M1*self.b1[0] + M2*self.b2[0]
        self.Gy = M1*self.b1[1] + M2*self.b2[1]
        self.G2 = self.Gx**2 + self.Gy**2
        self.Ug = g*uf(np.sqrt(self.G2))
        s = np.arange(n)/n
        S1, S2 = np.meshgrid(s, s, indexing='ij')
        self.X = S1*self.a1[0] + S2*self.a2[0]
        self.Y = S1*self.a1[1] + S2*self.a2[1]
    def phi(self, rho):
        return np.fft.ifft2(self.Ug*np.fft.fft2(rho)).real
    def H(self, psi):
        kin = np.fft.ifft2(0.5*self.G2*np.fft.fft2(psi))
        return kin + self.phi(np.abs(psi)**2)*psi
    def energy(self, psi):
        c = np.fft.fft2(psi)/self.n**2
        ek = 0.5*np.sum(self.G2*np.abs(c)**2)*self.A
        rho = np.abs(psi)**2
        ei = 0.5*np.mean(self.phi(rho)*rho)*self.A
        return float((ek + ei).real)

def rhomb(a, n, uf, g):
    return Cell((a, 0.0), (a/2.0, np.sqrt(3)/2*a), n, uf, g)

# ---------------- ground state ----------------
def seed(cell, noise=0.10, rng=None):
    rng = rng or RNG
    n = cell.n; w = 0.30*np.linalg.norm(cell.a1)
    d2 = None
    for p in (-1, 0, 1):
        for q in (-1, 0, 1):
            dx = cell.X - (p*cell.a1[0] + q*cell.a2[0])
            dy = cell.Y - (p*cell.a1[1] + q*cell.a2[1])
            dd = dx*dx + dy*dy
            d2 = dd if d2 is None else np.minimum(d2, dd)
    ps = np.exp(-d2/(2*w*w)).astype(complex)
    amp = np.abs(ps).max()
    ps = ps + noise*amp*(rng.standard_normal((n, n)) + 1j*rng.standard_normal((n, n)))
    ps *= 1.0/np.sqrt(np.mean(np.abs(ps)**2))
    return ps

def imag_time(cell, psi, steps, dt=2e-3):
    kf = np.exp(-dt*0.5*cell.G2)
    for _ in range(steps):
        psi = np.fft.ifft2(kf*np.fft.fft2(psi))
        psi = psi*np.exp(-dt*cell.phi(np.abs(psi)**2))
        psi *= 1.0/np.sqrt(np.mean(np.abs(psi)**2))
    return psi

def polish(cell, psi, iters=400, tau=0.5):
    psi = np.real(psi).copy(); psi *= 1.0/np.sqrt(np.mean(psi**2))
    mu = 0.0; rn = 1.0
    E = cell.energy(psi)
    for _ in range(iters):
        Hp = np.real(cell.H(psi))
        mu = np.mean(psi*Hp)/np.mean(psi**2)
        r = Hp - mu*psi
        rn = float(np.sqrt(np.mean(r**2)))
        if rn < 1e-9*max(abs(mu), 1.0):
            break
        pre = 1.0/(0.5*cell.G2 + 1.0 + 0.02*abs(mu))
        d = np.fft.ifft2(pre*np.fft.fft2(r)).real
        psi2 = psi - tau*d
        psi2 *= 1.0/np.sqrt(np.mean(psi2**2))
        E2 = cell.energy(psi2)
        if E2 <= E + 1e-14*abs(E):
            psi, E = psi2, E2
            tau = min(tau*1.15, 1.0)
        else:
            tau *= 0.5
            if tau < 1e-4:
                break
    Hp = np.real(cell.H(psi))
    mu = np.mean(psi*Hp)/np.mean(psi**2)
    rn = float(np.sqrt(np.mean((Hp - mu*psi)**2)))
    return psi, float(mu), rn

def recenter(cell, psi):
    rho = np.abs(psi)**2; n = cell.n
    w1 = np.exp(-2j*np.pi*np.arange(n)/n)
    c1 = np.sum(rho*w1[:, None]); c2 = np.sum(rho*w1[None, :])
    s10 = (-np.angle(c1))/(2*np.pi); s20 = (-np.angle(c2))/(2*np.pi)
    sh = np.exp(2j*np.pi*(cell.M1*s10 + cell.M2*s20))
    return np.fft.ifft2(sh*np.fft.fft2(psi))

def solve_at(cell, steps, pol, rng=None):
    ps = seed(cell, rng=rng)
    ps = imag_time(cell, ps, steps)
    ps = recenter(cell, ps)
    ps, mu, rn = polish(cell, ps, pol)
    ps = np.real(recenter(cell, ps))
    ps, mu, rn = polish(cell, ps, 80)
    return ps, mu, rn

# ---------------- a*-scan + CERT ----------------
def parab_vertex(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    d = (x1 - x2)*(x1 - x3)*(x2 - x3)
    if abs(d) < 1e-14:
        return None
    A = (x3*(y2 - y1) + x2*(y1 - y3) + x1*(y3 - y2))/d
    B = (x3*x3*(y1 - y2) + x2*x2*(y3 - y1) + x1*x1*(y2 - y3))/d
    if A <= 0:
        return None
    return -B/(2*A)

def scanE(uf, g, apred, n, tier):
    steps, pol = (4000, 80) if tier == 1 else (20000, 400)
    aa = list(np.linspace(0.88, 1.12, 13)*apred)
    sol = {}
    for a in aa:
        c = rhomb(a, n, uf, g)
        ps, mu, rn = solve_at(c, steps, pol)
        sol[a] = (c.energy(ps)/c.A, ps, mu, rn)
    xs = sorted(sol.keys()); Es = [sol[a][0] for a in xs]
    i = int(np.argmin(Es)); interior = (0 < i < len(xs) - 1)
    for _ in range(2):
        xs = sorted(sol.keys()); Es = [sol[a][0] for a in xs]
        i = int(np.argmin(Es))
        if 0 < i < len(xs) - 1:
            av = parab_vertex((xs[i-1], Es[i-1]), (xs[i], Es[i]), (xs[i+1], Es[i+1]))
            if av is not None and xs[0] < av < xs[-1] and min(abs(av - x) for x in xs) > 1e-5:
                c = rhomb(av, n, uf, g)
                ps, mu, rn = solve_at(c, steps, pol)
                sol[av] = (c.energy(ps)/c.A, ps, mu, rn)
    xs = sorted(sol.keys()); Es = [sol[a][0] for a in xs]
    i = int(np.argmin(Es))
    astar = xs[i]; Estar, psis, mu, rn = sol[astar]
    return dict(astar=astar, E=Estar, psi=psis, mu=mu, rn=rn, interior=interior)

def cert(uf, g, apred, n, tier):
    r = scanE(uf, g, apred, n, tier)
    Eu = 0.5*g*float(uf(np.array([0.0]))[0])
    rho = np.abs(r['psi'])**2
    contrast = float((rho.max() - rho.min())/rho.mean())
    ok = (r['E'] <= Eu - 1e-5*abs(Eu)) and (contrast >= 0.5) and r['interior']
    r.update(Eu=Eu, contrast=contrast, ok=bool(ok))
    return r

def p1(K):
    kd = KDEF[K]; uf = kernel_fn(K)
    grid = list(kd['grid']); dev = []
    res1 = {}
    gstar = None
    for g in grid:
        r = cert(uf, g, kd['apred'], 32, 1)
        res1[g] = r
        print(f"{K} tier1 g={g}: a*={r['astar']:.4f} E/A={r['E']:.4f} Eu={r['Eu']:.4f} "
              f"contr={r['contrast']:.3f} int={r['interior']} ok={r['ok']}")
        if r['ok']:
            gstar = g
            break
    if gstar is None:
        out = dict(K=K, flag='FP-NONEXIST(p6m)', deviations=dev)
        json.dump(out, open(f'{OUT}/{K}_p1.json', 'w'), indent=1)
        print(K, 'FP-NONEXIST'); return
    while gstar == min(grid) and gstar - 5 >= 5:
        gdn = gstar - 5
        r = cert(uf, gdn, kd['apred'], 32, 1)
        res1[gdn] = r; grid.insert(0, gdn)
        dev.append(f"grid extended downward to {gdn}")
        print(f"{K} tier1 g={gdn}: ok={r['ok']} (downward extension)")
        if r['ok']:
            gstar = gdn
        else:
            break
    # tier-2 at g*
    r2 = cert(uf, gstar, kd['apred'], 32, 2)
    print(f"{K} tier2 g={gstar}: a*={r2['astar']:.5f} mu={r2['mu']:.4f} rn={r2['rn']:.2e} "
          f"contr={r2['contrast']:.3f} ok={r2['ok']}")
    if not r2['ok']:
        dev.append(f"tier2 fail at g={gstar}; advanced")
        gstar += 5
        r2 = cert(uf, gstar, kd['apred'], 32, 2)
        print(f"{K} tier2 g={gstar}: ok={r2['ok']} (advanced)")
    # 3 random-phase deep re-solves at a*
    astars = [r2['astar']]
    cellf = rhomb(r2['astar'], 32, uf, gstar)
    for t in range(3):
        rng = np.random.default_rng(1000 + t)
        ps, mu, rn = solve_at(cellf, 20000, 400, rng=rng)
        E = cellf.energy(ps)/cellf.A
        rel = abs(E - r2['E'])/abs(r2['E'])
        print(f"{K} rerun{t}: E/A={E:.6f} rel={rel:.2e}")
        if rel > 1e-5:
            dev.append(f"rerun{t} E rel dev {rel:.2e}")
    # g*-5 must fail deep
    if gstar - 5 >= 5:
        r3 = cert(uf, gstar - 5, kd['apred'], 32, 2)
        print(f"{K} tier2 g={gstar-5}: ok={r3['ok']} (must be False)")
        if r3['ok']:
            dev.append(f"g*-5={gstar-5} certified deep; downward walk")
            while r3['ok'] and gstar - 5 >= 10:
                gstar -= 5
                r2 = r3
                r3 = cert(uf, gstar - 5, kd['apred'], 32, 2)
                print(f"{K} walk: g*={gstar}, below ok={r3['ok']}")
    np.save(f'{OUT}/{K}_psi.npy', r2['psi'])
    out = dict(K=K, gstar=int(gstar), astar=float(r2['astar']), mu=float(r2['mu']),
               EperA=float(r2['E']), Eu=float(r2['Eu']), contrast=float(r2['contrast']),
               gp_residual=float(r2['rn']), deviations=dev, flag=None)
    json.dump(out, open(f'{OUT}/{K}_p1.json', 'w'), indent=1)
    print(K, 'P1 done:', out['gstar'], out['astar'])

# ---------------- BdG ----------------
def dense_ops(cell, psi, mu, kvec):
    n = cell.n; N = n*n
    G2k = (cell.Gx + kvec[0])**2 + (cell.Gy + kvec[1])**2
    Ugk = cell.g*cell.uf(np.sqrt(G2k))
    Phi = cell.phi(psi**2)
    Cid = np.eye(N, dtype=complex).reshape(N, n, n)
    F = np.fft.ifft2(Cid, axes=(1, 2))*N        # basis fields e^{iGx}
    Vm = (np.fft.fft2(Phi[None, :, :]*F, axes=(1, 2)).reshape(N, N)/N).T
    h = psi[None, :, :]*F
    W = np.fft.ifft2(Ugk[None, :, :]*np.fft.fft2(h, axes=(1, 2)), axes=(1, 2))
    Xm = (np.fft.fft2(psi[None, :, :]*W, axes=(1, 2)).reshape(N, N)/N).T
    L = np.diag(0.5*G2k.ravel() - mu) + Vm
    for nm, Mx in (('L', L), ('X', Xm)):
        herr = np.linalg.norm(Mx - Mx.conj().T)/max(np.linalg.norm(Mx), 1e-30)
        assert herr < 1e-9, f"{nm} hermiticity {herr:.2e}"
    L = 0.5*(L + L.conj().T); Xm = 0.5*(Xm + Xm.conj().T)
    return L, Xm

def bdg_modes(cell, psi, mu, kvec, nmodes=6):
    L, Xm = dense_ops(cell, psi, mu, kvec)
    Li = inv(L); Li = 0.5*(Li + Li.conj().T)
    w2, V = eigh(L + 2*Xm, Li)
    return w2[:nmodes], V[:, :nmodes]

def parity_maps(n):
    i = np.arange(n)
    I, J = np.meshgrid(i, i, indexing='ij')
    sM = ((-I - J) % n, J)          # x -> -x  (fixes GM = y-hat)
    sK = ((-I) % n, (I + J) % n)    # mirror fixing the GK direction
    return sM, sK

def mode_fields(cell, V):
    n = cell.n
    return [np.fft.ifft2(V[:, j].reshape(n, n))*n*n for j in range(V.shape[1])]

def f_odd(field, smap):
    fs = field[smap]
    num = np.sum(np.abs(0.5*(field - fs))**2)
    den = np.sum(np.abs(field)**2)
    return float(num/den)

def classify(cell, psi, w2, V, smap, mu):
    oms = np.sqrt(np.clip(w2, 0, None))
    fields = mode_fields(cell, V)
    fo = [f_odd(f, smap) for f in fields]
    wr = [float(np.abs(np.mean(psi*f))**2/np.mean(np.abs(f)**2)) for f in fields]
    ti = [j for j in range(len(oms)) if fo[j] >= 0.95]
    ei = [j for j in range(len(oms)) if fo[j] <= 0.05]
    T = ti[0] if ti else None
    E2 = sorted(ei, key=lambda j: oms[j])[:2]
    return oms, fo, wr, T, E2

def speeds_along(cell, psi, mu, khat, kmag, smap, tag):
    ks = [(j/40.0)*kmag for j in range(1, 9)]
    omT, omL1, om2, fTs = [], [], [], []
    neg = False
    for kv in ks:
        w2, V = bdg_modes(cell, psi, mu, (khat[0]*kv, khat[1]*kv), nmodes=6)
        if w2[0] < -1e-8*mu*mu:
            neg = True
        oms, fo, wr, T, E2 = classify(cell, psi, w2, V, smap, mu)
        if T is None or len(E2) < 2:
            return None, dict(fail='classify', tag=tag, fo=fo, om=list(oms))
        omT.append(oms[T]); fTs.append(fo[T])
        om2.append(oms[E2[0]]); omL1.append(oms[E2[1]])
    ks = np.array(ks); omT = np.array(omT); omL1 = np.array(omL1); om2 = np.array(om2)
    def zi(o, sl): return float(np.sum(o[sl]*ks[sl])/np.sum(ks[sl]**2))
    def pexp(o, sl):
        x = np.log(ks[sl]); y = np.log(o[sl])
        return float(np.polyfit(x, y, 1)[0])
    s26 = slice(1, 6); W1 = slice(1, 5); W2 = slice(3, 8)
    out = dict(tag=tag, neg=neg, fT_min=float(min(fTs)),
               cT=zi(omT, s26), cL1=zi(omL1, s26), c2=zi(om2, s26),
               pT=(pexp(omT, W1), pexp(omT, W2)),
               pL1=(pexp(omL1, W1), pexp(omL1, W2)),
               omT=list(map(float, omT)), omL1=list(map(float, omL1)),
               om2=list(map(float, om2)), ks=list(map(float, ks)))
    return out, None

def conv_proxy(cell, psi, mu, khat, kmag, smap):
    js = [3, 5]; kk, oT, oL = [], [], []
    for j in js:
        kv = (j/40.0)*kmag
        w2, V = bdg_modes(cell, psi, mu, (khat[0]*kv, khat[1]*kv), nmodes=6)
        oms, fo, wr, T, E2 = classify(cell, psi, w2, V, smap, mu)
        if T is None or len(E2) < 2:
            return None
        kk.append(kv); oT.append(oms[T]); oL.append(oms[E2[1]])
    kk = np.array(kk); oT = np.array(oT); oL = np.array(oL)
    return (float(np.sum(oT*kk)/np.sum(kk**2)), float(np.sum(oL*kk)/np.sum(kk**2)))

def ward(cell, psi, mu):
    def apL(f):
        kin = np.fft.ifft2(0.5*cell.G2*np.fft.fft2(f))
        return kin + cell.phi(psi**2)*f - mu*f
    def apX(f):
        return psi*np.fft.ifft2(cell.Ug*np.fft.fft2(psi*f))
    outs = []
    for Gc in (cell.Gx, cell.Gy):
        d = np.fft.ifft2(1j*Gc*np.fft.fft2(psi))
        r = apL(d) + 2*apX(d)
        outs.append(float(np.sqrt(np.mean(np.abs(r)**2))/(np.sqrt(np.mean(np.abs(d)**2))*abs(mu))))
    return outs

def p2(K):
    kd = KDEF[K]; uf = kernel_fn(K)
    st = json.load(open(f'{OUT}/{K}_p1.json'))
    if st.get('flag'):
        print(K, 'skipped:', st['flag']); return
    g, a = st['gstar'], st['astar']
    cell = rhomb(a, 32, uf, g)
    psi = np.load(f'{OUT}/{K}_psi.npy')
    psi, mu, rn = polish(cell, psi, 600)
    psi = np.real(recenter(cell, psi)); psi, mu, rn = polish(cell, psi, 200)
    sres = float(np.sqrt(np.mean((psi - psi[parity_maps(32)[0]])**2))/np.sqrt(np.mean(psi**2)))
    wx, wy = ward(cell, psi, mu)
    print(f"{K}: mu={mu:.4f} rn={rn:.2e} sres={sres:.2e} ward=({wx:.2e},{wy:.2e})")
    flags = []
    if max(wx, wy) > 5e-3:
        flags.append('F9-FIRE')
        print(K, 'F9 FIRE — halting kernel'); _save_p2_fail(K, st, flags); return
    sM, sK = parity_maps(32)
    kGM = 2*np.pi/(np.sqrt(3)*a)
    kGK = 4*np.pi/(3*a)
    hM = (0.0, 1.0)
    hK = (0.5, np.sqrt(3)/2)
    rM, eM = speeds_along(cell, psi, mu, hM, kGM, sM, 'GM')
    rK, eK = speeds_along(cell, psi, mu, hK, kGK, sK, 'GK')
    if rM is None or rK is None:
        flags.append('F-CLS'); print(K, 'classify fail', eM or eK)
        _save_p2_fail(K, st, flags); return
    if rM['neg'] or rK['neg']:
        flags.append('F-NEG')
    for r in (rM, rK):
        for p in list(r['pT']) + list(r['pL1']):
            if not (0.90 <= p <= 1.10):
                flags.append('F-LIN')
    isoT = abs(rM['cT'] - rK['cT'])/(0.5*(rM['cT'] + rK['cT']))*100
    isoL = abs(rM['cL1'] - rK['cL1'])/(0.5*(rM['cL1'] + rK['cL1']))*100
    if isoT > 2.0 or isoL > 2.0:
        flags.append('F-ISO')
    # n=40 convergence
    cell40 = rhomb(a, 40, uf, g)
    ps40, mu40, rn40 = solve_at(cell40, 12000, 400)
    sM40, sK40 = parity_maps(40)
    dcs = []
    for (cl, ps, m, sm, sk) in ((cell, psi, mu, sM, sK), (cell40, ps40, mu40, sM40, sK40)):
        a_ = conv_proxy(cl, ps, m, hM, kGM, sm)
        b_ = conv_proxy(cl, ps, m, hK, kGK, sk)
        dcs.append((a_, b_))
    convT = max(abs(dcs[0][0][0] - dcs[1][0][0])/dcs[0][0][0],
                abs(dcs[0][1][0] - dcs[1][1][0])/dcs[0][1][0])
    convL = max(abs(dcs[0][0][1] - dcs[1][0][1])/dcs[0][0][1],
                abs(dcs[0][1][1] - dcs[1][1][1])/dcs[0][1][1])
    if convT > 1e-3 or convL > 1e-3:
        flags.append('F-CONV')
    # W-mu witness
    E0 = None; mus = []
    cE = rhomb(a, 32, uf, g)
    psE, muE, rnE = solve_at(cE, 20000, 400)
    E0 = cE.energy(psE)
    for eps in (0.005, 0.01):
        Ep = []
        for sgn in (+1, -1):
            a2s = (a/2.0 + sgn*eps*np.sqrt(3)/2*a, np.sqrt(3)/2*a)
            cs = Cell((a, 0.0), a2s, 32, uf, g)
            pss, mss, rss = solve_at(cs, 20000, 400)
            Ep.append(cs.energy(pss))
        mus.append((Ep[0] + Ep[1] - 2*E0)/(cE.A*eps*eps))
    mu_s = float(np.mean(mus))
    cT = 0.5*(rM['cT'] + rK['cT']); cL1 = 0.5*(rM['cL1'] + rK['cL1'])
    RT = cT/cL1
    out = dict(K=K, gstar=g, astar=a, mu=float(mu), gp_residual=float(rn), sres=sres,
               ward_x=wx, ward_y=wy,
               cT_GM=rM['cT'], cT_GK=rK['cT'], cL1_GM=rM['cL1'], cL1_GK=rK['cL1'],
               c2_GM=rM['c2'], c2_GK=rK['c2'],
               p_T=[*rM['pT'], *rK['pT']], p_L1=[*rM['pL1'], *rK['pL1']],
               f_T_min=min(rM['fT_min'], rK['fT_min']),
               iso_T_pct=isoT, iso_L1_pct=isoL,
               conv_dcT=float(convT), conv_dcL1=float(convL),
               cT=cT, cL1=cL1, c2=0.5*(rM['c2'] + rK['c2']), R_T=float(RT),
               mu_static=mu_s, wmu_ratio=float(mu_s/(1.0*cT*cT)),
               mu_static_pair=[float(x) for x in mus],
               flags=flags, deviations=st['deviations'],
               raw=dict(GM=rM, GK=rK))
    json.dump(out, open(f'{OUT}/{K}_p2.json', 'w'), indent=1)
    print(f"{K} P2: cT={cT:.4f} cL1={cL1:.4f} c2={out['c2']:.4f} R_T={RT:.5f} "
          f"fT={out['f_T_min']:.3f} isoT={isoT:.2f}% conv=({convT:.1e},{convL:.1e}) "
          f"wmu={out['wmu_ratio']:.3f} flags={flags}")

def _save_p2_fail(K, st, flags):
    out = dict(K=K, gstar=st.get('gstar'), flags=flags, excluded=True,
               deviations=st.get('deviations', []))
    json.dump(out, open(f'{OUT}/{K}_p2.json', 'w'), indent=1)

# ---------------- controls ----------------
def p0():
    # C-NEG: uniform step fluid at g=8
    uf = uhat_step
    cell = rhomb(1.4575, 32, uf, 8.0)
    psi = np.ones((32, 32))
    mu = 8.0*float(uf(np.array([0.0]))[0])
    kGM = 2*np.pi/(np.sqrt(3)*1.4575)
    sM, _ = parity_maps(32)
    gapless_odd = 0; gapless_tot = None
    ok_an = True
    for j in (1, 2, 3, 4):
        kv = (j/40.0)*kGM
        w2, V = bdg_modes(cell, psi, mu, (0.0, kv), nmodes=6)
        oms = np.sqrt(np.clip(w2, 0, None))
        # analytic Bogoliubov for the k+0 branch
        an = np.sqrt(0.5*kv*kv*(0.5*kv*kv + 2*8.0*float(uf(np.array([kv]))[0])))
        rel = abs(oms[0] - an)/an
        ok_an &= rel < 1e-6
        fields = mode_fields(cell, V)
        gl = [m for m in range(6) if oms[m] < 3.0*an]
        gapless_tot = len(gl)
        gapless_odd += sum(1 for m in gl if f_odd(fields[m], sM) > 0.5)
    cneg = ok_an and gapless_tot == 1 and gapless_odd == 0
    print(f"C-NEG: analytic-match={ok_an} gapless={gapless_tot} odd-gapless={gapless_odd} -> "
          f"{'PASS' if cneg else 'FAIL'}")
    # C-POS: classical NN central springs on the triangular lattice
    dels = [np.array([np.cos(t), np.sin(t)]) for t in np.arange(6)*np.pi/3]
    def Dk(k):
        D = np.zeros((2, 2))
        for d in dels:
            D += 2*np.sin(0.5*np.dot(k, d))**2*np.outer(d, d)
        return D
    res = []
    for kh in (np.array([0.0, 1.0]), np.array([0.5, np.sqrt(3)/2])):
        for km in (1e-3, 5e-4):
            ev, evec = np.linalg.eigh(Dk(kh*km))
            cs = np.sqrt(ev)/km
            pol = abs(np.dot(evec[:, 0], kh))
            res.append((cs[1]/cs[0], pol))
    ratio_err = max(abs(r/np.sqrt(3) - 1.0) for r, _ in res)
    pol_ok = max(p for _, p in res) <= 0.05
    cpos = ratio_err < 1e-6 and pol_ok
    print(f"C-POS: max|cL/cT/sqrt3 - 1|={ratio_err:.2e} T-pol|e.k|<=0.05: {pol_ok} -> "
          f"{'PASS' if cpos else 'FAIL'}")
    json.dump(dict(cneg=bool(cneg), cpos=bool(cpos)), open(f'{OUT}/p0.json', 'w'))

def p3():
    out = dict(lock_md5='99eb26a5d8ff1e32c54d5cff40386098',
               anchors=dict(step_RT=[0.5228, 0.5286, 0.5348, 0.5436], gam6_RT=[0.4988]),
               controls=json.load(open(f'{OUT}/p0.json')), kernels={})
    for K in ('K3', 'K4', 'K5', 'K6'):
        f = f'{OUT}/{K}_p2.json'
        d = json.load(open(f)) if os.path.exists(f) else dict(missing=True)
        if 'wmu_ratio' in d:
            d['wmu_band_ok'] = bool(0.5 <= d['wmu_ratio'] <= 2.0)
            if not d['wmu_band_ok']:
                d.setdefault('flags', []).append('W-MU-BAND')
        d['excluded'] = bool(d.get('excluded') or
                             any(fl in d.get('flags', []) for fl in ('F-LIN', 'F-ISO', 'F9-FIRE', 'F-CLS', 'F-NEG')))
        out['kernels'][K] = d
    json.dump(out, open(f'{OUT}/gtsh2_results.json', 'w'), indent=1)
    print('P3 frozen: gtsh2_results.json')

if __name__ == '__main__':
    ph = sys.argv[1]
    if ph == 'tables':
        build_tables()
    elif ph == 'p0':
        p0()
    elif ph == 'p1':
        p1(sys.argv[2])
    elif ph == 'p2':
        p2(sys.argv[2])
    elif ph == 'p3':
        p3()
