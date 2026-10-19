"""Second cross-check code for E1 (written fresh in this cross-check pass, without reading the
original E1 scripts).  Method deliberately different from both the original (4th-order FD +
velocity-Verlet) and the first cross-check code (6th-order FD + RK4):

  * variable  delta = phi + 1 (-> 0 at both ends), periodic Fourier grid of half-length LB
  * equation  delta_tt = delta_xx - 2 delta + 3 delta^2 - delta^3 - gamma(x) delta_t
              (= phi_tt = phi_xx - phi(phi^2 - 1), V = (phi^2 - 1)^2 / 4, m = sqrt 2)
  * time      exponential (Gautschi-type) splitting: the linear Klein-Gordon part
              omega_k^2 = k^2 + 2 is propagated EXACTLY in Fourier space; the nonlinear force
              3 delta^2 - delta^3 and the sponge are applied as kicks in real space.
              Strang kick-drift-kick, composed into a 4th-order Yoshida triple step.
  * sponge    cubic ramp gamma = GMAX ((|x| - LP)/W)^3 on LP < |x| < LP + W, constant GMAX beyond.

Pair test used for the comparison with the original: the original REPORT's words
("a maximal interval with phi > 0, longer than 4 kink widths (5.66), with phi > 0.5 on at least
80% of its points", whole array searched).  A second, own test is also recorded
(phi > 0 interval longer than 3 kink widths whose median exceeds 0.8).

Modes (results appended to JSONL files; every mode is resumable):
  dsv  <tag>             DSV breather-train runs listed in DSV_CASES[tag], tracked every 10 t.u.
  gauss <worker> <nw>    random sample of coarse-grid Gaussian-packet points (see GAUSS_SAMPLE)
  vc  <x0>               (unused helper)
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SQ2 = np.sqrt(2.0)
MKINK = 2 * SQ2 / 3
KW = SQ2

# Yoshida 4th-order composition coefficients
_C1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
_C0 = -2.0 ** (1.0 / 3.0) * _C1
YOSHIDA = (_C1, _C0, _C1)


class Spec:
    def __init__(self, LB, dx, LP, W, gmax=1.0):
        N = int(round(2 * LB / dx))
        if N % 2:
            N += 1
        self.N = N
        self.dx = 2 * LB / N
        self.x = -LB + self.dx * np.arange(N)
        self.k = 2 * np.pi * np.fft.rfftfreq(N, d=self.dx)
        self.w = np.sqrt(self.k ** 2 + 2.0)
        s = np.clip((np.abs(self.x) - LP) / W, 0.0, 1.0)
        self.gam = gmax * s ** 3
        self._cache = {}

    def _rot(self, h):
        if h not in self._cache:
            c = np.cos(self.w * h)
            sn = np.sin(self.w * h)
            self._cache[h] = (c, sn / self.w, -self.w * sn)
        return self._cache[h]

    def strang(self, d, p, h):
        # half kick (nonlinear force + sponge), exact linear drift, half kick
        hh = 0.5 * h
        p *= np.exp(-self.gam * hh)
        p += hh * (3.0 * d * d - d * d * d)
        D = np.fft.rfft(d)
        P = np.fft.rfft(p)
        c, s_w, mws = self._rot(h)
        D, P = c * D + s_w * P, mws * D + c * P
        d = np.fft.irfft(D, n=self.N)
        p = np.fft.irfft(P, n=self.N)
        p += hh * (3.0 * d * d - d * d * d)
        p *= np.exp(-self.gam * hh)
        return d, p

    def step4(self, d, p, dt, n):
        for _ in range(n):
            for c in YOSHIDA:
                d, p = self.strang(d, p, c * dt)
        return d, p

    def energy(self, d, p, mask=None):
        dd = np.fft.irfft(1j * self.k * np.fft.rfft(d), n=self.N)
        phi = d - 1.0
        e = 0.5 * p * p + 0.5 * dd * dd + 0.25 * (phi * phi - 1) ** 2
        if mask is not None:
            e = e[mask]
        return float(np.sum(e) * self.dx)


def intervals_pos(phi):
    pos = phi > 0
    if not pos.any():
        return []
    dd = np.diff(np.concatenate(([0], pos.astype(np.int8), [0])))
    st = np.where(dd == 1)[0]
    en = np.where(dd == -1)[0] - 1
    return list(zip(st, en))


def pair_report(phi, dx):
    for i0, i1 in intervals_pos(phi):
        if (i1 - i0 + 1) * dx > 4 * KW and np.mean(phi[i0:i1 + 1] > 0.5) >= 0.8:
            return True
    return False


def pair_mine(phi, dx):
    for i0, i1 in intervals_pos(phi):
        if (i1 - i0 + 1) * dx > 3 * KW and np.median(phi[i0:i1 + 1]) > 0.8:
            return True
    return False


def widest_pos(phi, dx):
    iv = intervals_pos(phi)
    if not iv:
        return 0.0
    return float(max((b - a + 1) for a, b in iv) * dx)


# ------------------------------------------------------------------ DSV breather trains
def dsv_init(x, om, v):
    s = np.sqrt(1 - om * om)
    eta = s / om
    Nb = int(2 / s) + 1
    a = 10 / s
    dd = 2 / s
    g = 1 / np.sqrt(1 - v * v)
    phi = -np.ones_like(x)
    pt = np.zeros_like(x)
    with np.errstate(over='ignore'):
        for n in list(range(-Nb, 0)) + list(range(1, Nb + 1)):
            if n > 0:
                x0n, vn = a + n * dd, -v
            else:
                x0n, vn = -a + n * dd, v
            T = g * (0.0 - vn * (x - x0n))
            X = g * (x - x0n)
            Y = eta * om * X
            sech = 1.0 / np.cosh(Y)
            u = eta * np.sin(om * T) * sech
            # d/dt of u at t = 0: T_t = g, X_t = -g vn
            ut = eta * om * g * np.cos(om * T) * sech + eta * np.sin(om * T) * (-np.tanh(Y) * sech) * eta * om * (-g * vn)
            phi += (4 / np.pi) * np.arctan(u)
            pt += (4 / np.pi) * ut / (1 + u * u)
    return phi, pt, Nb


DSV_CASES = {
    'ex': [(0.99, 0.43, 0.1, 0.02), (0.99, 0.43, 0.05, 0.01), (0.99, 0.43, 0.1, 0.01)],
    'nb': [(0.99, 0.42, 0.1, 0.02), (0.99, 0.44, 0.1, 0.02), (0.99, 0.41, 0.1, 0.02), (0.99, 0.40, 0.1, 0.02)],
    # second-stage list (the dx=0.05 run uses dt=0.02: the linear part is exact, so no CFL limit)
    'ex2': [(0.99, 0.43, 0.05, 0.02), (0.99, 0.42, 0.1, 0.02), (0.99, 0.44, 0.1, 0.02), (0.99, 0.41, 0.1, 0.02)],
    'ex3': [(0.99, 0.41, 0.05, 0.02)],   # added after the dx=0.1 run at v=0.41 produced
    'ex4': [(0.99, 0.41, 0.1, 0.01)],    # time-step check of the v=0.41 producer
    'map': [],   # filled from the command line: dsv map om v ...
}


def run_dsv(om, v, dx, dt, LP=600.0, W=60.0, tfac=1.5, every=10.0):
    LB = LP + W + 20.0
    S = Spec(LB, dx, LP, W)
    phi, pt, Nb = dsv_init(S.x, om, v)
    d = phi + 1.0
    p = pt.copy()
    E0 = S.energy(d, p)
    T = 2 * LP
    nper = int(round(every / dt))
    hist = []
    t = 0.0
    i0 = int(np.argmin(np.abs(S.x)))
    while t < tfac * T - 1e-9:
        d, p = S.step4(d, p, dt, nper)
        t += nper * dt
        ph = d - 1.0
        hist.append([round(t, 4), pair_report(ph, S.dx), pair_mine(ph, S.dx), round(widest_pos(ph, S.dx), 2),
                     round(float(ph[i0]), 3)])
    first = None
    for h in hist:
        if h[1]:
            first = h[0]
            break
    atT = [h for h in hist if abs(h[0] - T) < 1e-6][0]
    # persistent-from time: earliest time after which the report test is true at every sample
    pers = None
    for j in range(len(hist)):
        if all(hh[1] for hh in hist[j:]):
            pers = hist[j][0]
            break
    return dict(omega=om, v=v, dx=dx, dt=dt, Nb=Nb, E_over_2M=E0 / (2 * MKINK), T=T,
                first_pair_t=first, pair_at_T=bool(atT[1]), pair_at_T_mine=bool(atT[2]),
                width_at_T=atT[3], pair_at_end=bool(hist[-1][1]), persistent_from=pers,
                Ef_over_E0=S.energy(d, p) / E0, hist=hist)


# ------------------------------------------------------------------ Gaussian packets
def gauss_init(x, A, sig, k, x0, single=False):
    w = np.sqrt(k * k + 2.0)
    yl = x + x0
    Gl = np.exp(-yl ** 2 / (2 * sig ** 2))
    phi = -1.0 + A * Gl * np.cos(k * yl)
    pt = A * w * Gl * np.sin(k * yl)          # left packet moves right
    if not single:
        yr = x - x0
        Gr = np.exp(-yr ** 2 / (2 * sig ** 2))
        phi += A * Gr * np.cos(k * yr)
        pt -= A * w * Gr * np.sin(k * yr)     # right packet moves left
    return phi, pt


def oneway_velocity(S, A, sig, k, x0, single=False):
    """Exact one-way initial velocity: every Fourier component of each packet gets its own
    free Klein-Gordon velocity toward the centre: phi_t^ = -i sign(q) omega_q delta^ (right-moving)."""
    x = S.x
    out = np.zeros_like(x)
    packs = [(+1, x + x0)] + ([] if single else [(-1, x - x0)])
    for direction, y in packs:
        dl = A * np.exp(-y ** 2 / (2 * sig ** 2)) * np.cos(k * y)
        D = np.fft.rfft(dl)      # rfft: q >= 0 only; real field => phi_t^ = -i dir omega_q D
        out += np.fft.irfft(-1j * direction * S.w * D, n=S.N)
    return out


def run_gauss(A, sig, k, dx=0.1, dt=0.02, single=False, oneway=False, x0shift=0.0):
    w = np.sqrt(k * k + 2.0)
    vg = k / w
    x0 = 4 * sig + 10 + x0shift
    tcoll = x0 / vg
    T = max(tcoll + 400, 1.25 * (tcoll + 100))
    LP = x0 + 4 * sig + 40
    W = 60.0
    S = Spec(LP + W + 20.0, dx, LP, W)
    phi, pt = gauss_init(S.x, A, sig, k, x0, single)
    if oneway:
        pt = oneway_velocity(S, A, sig, k, x0, single)
    d = phi + 1.0
    p = pt.copy()
    E0 = S.energy(d, p)
    t = 0.0
    rep, mine = [], []
    for c in (0.80, 0.85, 0.90, 0.95, 1.00):
        n = int(round((c * T - t) / dt))
        d, p = S.step4(d, p, dt, n)
        t += n * dt
        ph = d - 1.0
        rep.append(pair_report(ph, S.dx))
        mine.append(pair_mine(ph, S.dx))
    # free-field occupation of the initial fluctuation about -1 (continuum dispersion), N_lin / phi0^2
    D = np.fft.rfft(phi + 1.0) * S.dx
    P = np.fft.rfft(pt) * S.dx
    wgt = np.ones_like(S.k)
    wgt[1:] = 2.0
    if S.N % 2 == 0:
        wgt[-1] = 1.0
    Lbox = S.N * S.dx
    Nlin = float(np.sum(wgt * (np.abs(P) ** 2 + S.w ** 2 * np.abs(D) ** 2) / (2 * S.w)) / Lbox)
    return dict(A=A, sigma=sig, k=k, single=single, oneway=oneway, x0shift=x0shift, dx=dx, dt=dt,
                E_over_2M=E0 / (2 * MKINK), N_lin=Nlin, T=T,
                prod=bool(all(rep)), prod_mine=bool(all(mine)), rep=rep, Ef_over_E0=S.energy(d, p) / E0)


TARGETS = (
    # (A, sigma, k, single, oneway, dx, dt)  -- smallest producers quoted in the report, both phi_t forms
    [(0.8, 2.0, 0.5, False, False, 0.1, 0.02), (0.8, 2.0, 0.5, False, False, 0.05, 0.01),
     (1.4, 1.0, 0.25, False, False, 0.1, 0.02), (1.4, 1.0, 0.25, False, False, 0.05, 0.01),
     (0.6, 4.0, 0.5, False, True, 0.1, 0.02), (0.6, 4.0, 0.5, False, True, 0.05, 0.01),
     (0.8, 2.0, 0.5, False, True, 0.1, 0.02), (0.8, 2.0, 0.5, True, False, 0.1, 0.02),
     (0.275, 16.0, 0.2, False, False, 0.1, 0.02)]
    # single-packet self-folding threshold scan (sigma = 16)
    + [(A, 16.0, kk, True, False, 0.1, 0.02) for kk in (0.25, 1.0) for A in (0.3, 0.35, 0.375, 0.4, 0.425, 0.45, 0.5)]
)


AS = [round(0.1 * i, 1) for i in range(1, 16)]
SIGS = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0]
KS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]


def gauss_sample(n=90, seed=20261019):
    """Random sample of coarse-grid points with A >= 0.3 (so that most have E > 2M);
    drawn with a fixed seed, independent of any outcome."""
    pts = [(A, s, k) for A in AS if A >= 0.3 for s in SIGS for k in KS]
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(pts), size=n, replace=False)
    return [pts[i] for i in sorted(idx)]


def jl_load(path):
    out = []
    if os.path.exists(path):
        for line in open(path):
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def append(path, r):
    with open(path, 'a') as f:
        f.write(json.dumps(r) + '\n')
        f.flush()
        os.fsync(f.fileno())


def selftest():
    """Energy conservation (no sponge) and kink-mass check of the spectral code."""
    S = Spec(60.0, 0.1, 1e9, 1.0)
    x = S.x
    # static kink-antikink far apart: energy should be 2 M_kink
    phi = np.tanh((x + 25) / SQ2) - np.tanh((x - 25) / SQ2) - 1
    E = S.energy(phi + 1, np.zeros_like(x))
    print('static pair E/2M = %.10f' % (E / (2 * MKINK)))
    d, p = gauss_init(x, 0.9, 3.0, 1.0, 15.0)
    d = d + 1
    E0 = S.energy(d, p)
    d, p = S.step4(d, p, 0.02, 5000)
    print('Gaussian collision, no sponge, t=100: rel. energy drift %.2e' % (S.energy(d, p) / E0 - 1))
    return E / (2 * MKINK)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'selftest':
        selftest()
    elif mode == 'dsv':
        tag = sys.argv[2]
        cases = DSV_CASES.get(tag, [])
        if tag == 'map':
            vals = [float(z) for z in sys.argv[3:]]
            cases = [(vals[i], vals[i + 1], 0.1, 0.02) for i in range(0, len(vals), 2)]
        path = os.path.join(HERE, 'xc2_dsv.jsonl')
        for (om, v, dx, dt) in cases:
            done = [(r['omega'], r['v'], r['dx'], r['dt']) for r in jl_load(path)]
            if (om, v, dx, dt) in done:
                continue
            t0 = time.time()
            r = run_dsv(om, v, dx, dt)
            r['wall_s'] = time.time() - t0
            append(path, r)
            print(f'DSV om={om} v={v} dx={dx} dt={dt} E/2M={r["E_over_2M"]:.3f} first_pair={r["first_pair_t"]} '
                  f'pair@T={r["pair_at_T"]} width@T={r["width_at_T"]} pair@1.5T={r["pair_at_end"]} '
                  f'persistent_from={r["persistent_from"]} ({r["wall_s"]:.0f}s)', flush=True)
    elif mode == 'targets':
        path = os.path.join(HERE, 'xc2_targets.jsonl')
        for (A, s, k, single, oneway, dx, dt) in TARGETS:
            done = {(r['A'], r['sigma'], r['k'], r['single'], r['oneway'], r['dx'], r['dt']) for r in jl_load(path)}
            if (A, s, k, single, oneway, dx, dt) in done:
                continue
            t0 = time.time()
            r = run_gauss(A, s, k, dx=dx, dt=dt, single=single, oneway=oneway)
            append(path, r)
            print(f'target A={A} s={s} k={k} single={single} oneway={oneway} dx={dx} E/2M={r["E_over_2M"]:.4f} '
                  f'N_lin={r["N_lin"]:.4f} prod={r["prod"]} rep={r["rep"]} ({time.time()-t0:.0f}s)', flush=True)
    elif mode == 'gauss':
        wk, nw = int(sys.argv[2]), int(sys.argv[3])
        pts = gauss_sample()
        path = os.path.join(HERE, f'xc2_gauss_w{wk}.jsonl')
        done = {(r['A'], r['sigma'], r['k']) for r in jl_load(path)}
        t0 = time.time()
        for j, (A, s, k) in enumerate(pts):
            if j % nw != wk or (A, s, k) in done:
                continue
            r = run_gauss(A, s, k)
            append(path, r)
            print(f'[w{wk}] {j}/{len(pts)} A={A} s={s} k={k} E/2M={r["E_over_2M"]:.2f} prod={r["prod"]} '
                  f'Ef/E0={r["Ef_over_E0"]:.3f} ({time.time()-t0:.0f}s)', flush=True)
        print(f'[w{wk}] gauss done', flush=True)
