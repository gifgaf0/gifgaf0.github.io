"""
E9 option 4, Phase 0 (PREREG_option4 §2): straight composite string, 1D radial. No loop is computed here.

Fixed-charge line functional (PREREG_option4 §1.2, §2.2):
    E(k, q) = T_static(k) + q^2 / (4 I),   I = 2 pi int r s^2 dr,
where T_static is option4_design's functional with its q2 argument = k^2 (k^2 s^2 included, no w^2).
Gradient of the extra term: -(q^2 / 4 I^2) dI/ds.  omega = q / (2 I).

Grid (§2.1): beta in {1,2,3,5}, mu2 = eps0(beta) + delta, delta in {0.25,0.5,1.0}, lam = mu2^2 / (1.6 D), D = 1.815.
Per point: C3 vacuum check, existence window in (k, q), thin-ring equilibrium Tcal = E - k dE/dk - q dE/dq,
d^2E/dR^2 along the fixed-(n, Q) ray, verdict WINDOW / NONE, selection rule (§2.3).

Run: python3 option4_phase0.py  -> phase0_results.json (console output is log_phase0.txt)
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np, json, time, sys, platform
from multiprocessing import Pool
from scipy.optimize import minimize
from scipy.interpolate import CloughTocher2DInterpolator
import scipy
import option4_design as od
from option4_design import e, eta, dr, rmax, r, M, rm, fv, Vvac, unpack, eps0

BETAS = (1.0, 2.0, 3.0, 5.0)
DELTAS = (0.25, 0.5, 1.0)
D = 1.815
DK, DQ = 0.05, 0.25
SIG_MIN, R_TAIL, TAIL_MAX = 0.05, 16.0, 0.01
Q_CAP = 400            # safety cap on q steps at one k (never reached is recorded)
K_CAP = 200
W = 2 * np.pi * rm * dr
OPTS = dict(maxiter=50000, maxfun=100000, gtol=1e-10, ftol=1e-16)   # as option4_design.solve()


def make_fg(beta, mu2, lam, k, q):
    """Line energy E(k, q) and its analytic gradient; same discretisation as option4_design.solve()."""
    q2 = k * k                      # T_static(k): k^2 s^2 included, no omega^2

    def parts(x):
        f, a, s = unpack(x, True)
        fp = np.diff(f) / dr; ap = np.diff(a) / dr; sp = np.diff(s) / dr
        fm = 0.5 * (f[1:] + f[:-1]); am = 0.5 * (a[1:] + a[:-1]); sm = 0.5 * (s[1:] + s[:-1])
        return f, a, s, fp, ap, sp, fm, am, sm

    def fg(x):
        f, a, s, fp, ap, sp, fm, am, sm = parts(x)
        dens = (3 * (fp ** 2 + fm ** 2 * (1 - am) ** 2 / rm ** 2 + 0.5 * (fm ** 2 - 1) ** 2) - 3 * eta * fm ** 2 - Vvac
                + ap ** 2 / (2 * e ** 2 * rm ** 2)
                + sp ** 2 + (3 * beta * fm ** 2 - mu2 + q2) * sm ** 2 + 0.5 * lam * sm ** 4)
        T = np.sum(W * dens)
        I = np.sum(W * sm ** 2)
        Eq = q * q / (4 * I) if q != 0 else 0.0
        dfp = W * 6 * fp
        dfm = W * (6 * fm * (1 - am) ** 2 / rm ** 2 + 6 * fm * (fm ** 2 - 1) - 6 * eta * fm + 6 * beta * fm * sm ** 2)
        dap = W * ap / (e ** 2 * rm ** 2)
        dam = W * (-6 * fm ** 2 * (1 - am) / rm ** 2)
        dsp = W * 2 * sp
        dsm = W * (2 * (3 * beta * fm ** 2 - mu2 + q2) * sm + 2 * lam * sm ** 3)
        if q != 0:
            dsm = dsm - (q * q / (4 * I * I)) * (W * 2 * sm)       # -(q^2/4I^2) dI/ds

        def node(dp, dm):
            g = np.zeros(M + 1)
            g[:-1] += -dp / dr + 0.5 * dm
            g[1:] += dp / dr + 0.5 * dm
            return g
        gf = node(dfp, dfm); ga = node(dap, dam); gs = node(dsp, dsm)
        return T + Eq, np.concatenate([gf[1:M], ga[1:M], gs[:M]])

    def observables(x):
        f, a, s, fp, ap, sp, fm, am, sm = parts(x)
        E, _ = fg(x)
        I = float(np.sum(W * sm ** 2))
        tail = float(np.sum((W * sm ** 2)[rm > R_TAIL]) / I) if I > 0 else float('nan')
        return dict(E=float(E), T_static=float(E - (q * q / (4 * I) if q != 0 else 0.0)), I=I,
                    sigma0=float(abs(s[0])), omega=float(q / (2 * I)) if I > 0 else float('inf'), tail_frac=tail)
    return fg, observables


def solve_line(P, k, q, x0):
    beta, mu2, lam = P
    fg, obs = make_fg(beta, mu2, lam, k, q)
    res = minimize(fg, x0, jac=True, method='L-BFGS-B', options=OPTS)
    o = obs(res.x)
    g = fg(res.x)[1]
    o.update(k=round(k, 10), q=round(q, 10), success=bool(res.success), message=str(res.message), nit=int(res.nit),
             grad_max=float(np.max(np.abs(g))))
    return o, res.x


def gradient_check(seed=0, P=(2.0, 3.6, 4.0), k=0.3, q=1.7):
    """Same definition as gl3.check_grad: 40 random coordinates, central FD step 1e-6, |fd-g|/(|fd|+1e-8)."""
    fg, _ = make_fg(*P, k, q)
    rng = np.random.default_rng(seed)
    x = np.concatenate([fv * np.tanh(r[1:M] / 0.8), (r[1:M] / 3) ** 2 / (1 + (r[1:M] / 3) ** 2),
                        0.8 * np.exp(-r[:M] ** 2 / 2)])
    x = x + 0.1 * rng.normal(size=x.size)
    _, g = fg(x)
    idx = np.concatenate([rng.choice(np.arange(0, M - 1), 14, replace=False),
                          rng.choice(np.arange(M - 1, 2 * M - 2), 13, replace=False),
                          rng.choice(np.arange(2 * M - 2, 3 * M - 2), 13, replace=False)])
    eps = 1e-6; worst = 0.0
    for i in idx:
        xp = x.copy(); xp[i] += eps; xm = x.copy(); xm[i] -= eps
        fd = (fg(xp)[0] - fg(xm)[0]) / (2 * eps)
        worst = max(worst, abs(fd - g[i]) / (abs(fd) + 1e-8))
    return worst


def consistency_check(P=(2.0, 3.6, 4.0), k=0.3, seed=1):
    """At q = 0, E must equal option4_design's functional with q2 = k^2 (evaluated on a random state)."""
    beta, mu2, lam = P
    rd = od.solve((beta, mu2, lam, k * k), with_s=True)      # only to obtain its fg closure
    rng = np.random.default_rng(seed)
    x = rd.x + 0.05 * rng.normal(size=rd.x.size)
    fg, _ = make_fg(beta, mu2, lam, k, 0.0)
    E1, g1 = fg(x); E2, g2 = rd.fg(x)
    return float(abs(E1 - E2) / abs(E2)), float(np.max(np.abs(g1 - g2)))


def c3_check(beta, mu2, lam):
    """Global min of V(rho,S) = 3/2(rho-1)^2 - 3 eta rho - mu2 S + lam/2 S^2 + 3 beta rho S on rho,S >= 0."""
    V = lambda p: 1.5 * (p[0] - 1) ** 2 - 3 * eta * p[0] - mu2 * p[1] + 0.5 * lam * p[1] ** 2 + 3 * beta * p[0] * p[1]
    cands = {'psi_vacuum': (1 + eta, 0.0), 'zero': (0.0, 0.0), 'sigma_vacuum': (0.0, mu2 / lam)}
    Hdet = 3 * lam - 9 * beta ** 2
    if abs(Hdet) > 1e-14:   # interior stationary point
        rho, S = np.linalg.solve([[3.0, 3 * beta], [3 * beta, lam]], [3 + 3 * eta, mu2])
        if rho >= 0 and S >= 0:
            cands['interior'] = (float(rho), float(S))
    analytic = {kk: dict(rho=v[0], S=v[1], V=float(V(v))) for kk, v in cands.items()}
    amin = min(analytic, key=lambda kk: analytic[kk]['V'])
    # fine grid + local polish (bounded L-BFGS-B), as an independent check
    rg = np.linspace(0, 3, 601); Sg = np.linspace(0, 3 * mu2 / lam + 1, 601)
    RR, SS = np.meshgrid(rg, Sg, indexing='ij'); VV = V((RR, SS))
    i, j = np.unravel_index(np.argmin(VV), VV.shape)
    pol = minimize(lambda p: V(p), [RR[i, j], SS[i, j]], method='L-BFGS-B', bounds=[(0, None), (0, None)],
                   options=dict(gtol=1e-14, ftol=1e-16))
    Vpsi = analytic['psi_vacuum']['V']
    passed = (amin == 'psi_vacuum') and abs(pol.x[0] - (1 + eta)) < 1e-5 and pol.x[1] < 1e-5
    return dict(passed=bool(passed), analytic_min=amin, candidates=analytic, Hessian_det=Hdet,
                grid_polish=dict(rho=float(pol.x[0]), S=float(pol.x[1]), V=float(pol.fun)),
                V_psi_vac=Vpsi, D_check=float(1.5 - Vpsi),
                sigma_vac_above_psi_vac=float(analytic['sigma_vacuum']['V'] - Vpsi))


def in_window(o, mvac):
    return bool(o['sigma0'] > SIG_MIN and o['omega'] < mvac and o['tail_frac'] < TAIL_MAX)


def scan_point(args):
    tag, beta, delta, mu2, lam, mvac, xbare = args
    P = (beta, mu2, lam)
    t0 = time.time()
    sol = {}      # (i, j) -> (rec, x)
    recs = []
    log = []

    def warm(i, j):
        if not sol:
            return np.concatenate([xbare, 0.6 * np.exp(-r[:M] ** 2 / 2)]), 'bare+gaussian'
        best = min(sol, key=lambda ij: ((ij[0] - i) * DK) ** 2 + ((ij[1] - j) * DQ) ** 2 + 1e-12 * ij[1])
        return sol[best][1], f'({best[0] * DK:.2f},{best[1] * DQ:.2f})'

    i = 0
    while i <= K_CAP:
        k = i * DK; any_in = False; j = 0
        while j <= Q_CAP:
            q = j * DQ
            x0, src = warm(i, j)
            o, x = solve_line(P, k, q, x0)
            o['warm_from'] = src; o['i'] = i; o['j'] = j
            o['in_window'] = in_window(o, mvac)
            sol[(i, j)] = (o, x); recs.append(o)
            if not o['success']:
                log.append(f'[{tag}] NOT CONVERGED k={k:.2f} q={q:.2f}: {o["message"]} nit={o["nit"]} '
                           f'grad_max={o["grad_max"]:.2e}')
            if not o['in_window']:
                break
            any_in = True; j += 1
        if j > Q_CAP:
            log.append(f'[{tag}] Q_CAP reached at k={k:.2f}')
        print(f'[{tag}] k={k:.2f}: last q={q:.2f}, in-window q up to {(j - 1) * DQ if any_in else None}, '
              f'{time.time() - t0:.0f} s', flush=True)
        if not any_in:
            break
        i += 1
    summ = analyse(tag, P, mvac, sol, log)
    summ['scan_seconds'] = time.time() - t0
    msg = (f'[{tag}] beta={beta} delta={delta} mu2={mu2:.4f} lam={lam:.4f} m_vac={mvac:.4f}: '
           f'{len(recs)} solves, {summ["n_in_window"]} in window, k_max_in={summ["k_max_in_window"]}, '
           f'sign changes={len(summ["sign_changes"])}, min(T/E)={summ["min_Tcal_over_E"]:.4f}, '
           f'verdict={summ["verdict"]}, {summ["scan_seconds"]:.0f} s')
    log.append(msg)
    for l in log:
        print(l, flush=True)
    return tag, recs, summ, log


def analyse(tag, P, mvac, sol, log):
    beta, mu2, lam = P
    win = {ij: v[0] for ij, v in sol.items() if v[0]['in_window']}
    Tc = {}
    for (i, j), o in win.items():
        flags = []
        # dE/dk
        if i == 0:
            dEk = 0.0; flags.append('k=0 (k dE/dk = 0)')
        elif (i - 1, j) in win and (i + 1, j) in win:
            dEk = (win[(i + 1, j)]['E'] - win[(i - 1, j)]['E']) / (2 * DK)
        elif (i + 1, j) in win:
            dEk = (win[(i + 1, j)]['E'] - o['E']) / DK; flags.append('one-sided k (forward)')
        elif (i - 1, j) in win:
            dEk = (o['E'] - win[(i - 1, j)]['E']) / DK; flags.append('one-sided k (backward)')
        else:
            dEk = None; flags.append('no k neighbour in window')
        if j == 0:
            dEq = 0.0; flags.append('q=0 (q dE/dq = 0)')
        elif (i, j - 1) in win and (i, j + 1) in win:
            dEq = (win[(i, j + 1)]['E'] - win[(i, j - 1)]['E']) / (2 * DQ)
        elif (i, j + 1) in win:
            dEq = (win[(i, j + 1)]['E'] - o['E']) / DQ; flags.append('one-sided q (forward)')
        elif (i, j - 1) in win:
            dEq = (o['E'] - win[(i, j - 1)]['E']) / DQ; flags.append('one-sided q (backward)')
        else:
            dEq = None; flags.append('no q neighbour in window')
        k, q = i * DK, j * DQ
        if dEk is None or dEq is None:
            T = None
        else:
            T = o['E'] - k * dEk - q * dEq
        # envelope-theorem value (cross-check only): dE/dk = 2 k I, dE/dq = omega
        Tenv = o['E'] - 2 * k * k * o['I'] - q * o['omega']
        o['Tcal'] = T; o['Tcal_envelope'] = Tenv; o['dEdk'] = dEk; o['dEdq'] = dEq; o['Tcal_flags'] = flags
        if T is not None:
            Tc[(i, j)] = T
    # sign changes between adjacent in-window points
    sc = []
    for (i, j), T in Tc.items():
        for (di, dj) in ((1, 0), (0, 1)):
            nb = (i + di, j + dj)
            if nb in Tc and np.sign(T) != np.sign(Tc[nb]) and T != 0:
                Tb = Tc[nb]; t = T / (T - Tb)
                ks = (i + t * di) * DK; qs = (j + t * dj) * DQ
                oa, ob = win[(i, j)], win[nb]
                om = oa['omega'] + t * (ob['omega'] - oa['omega'])
                sc.append(dict(between=[[i * DK, j * DQ], [nb[0] * DK, nb[1] * DQ]], k_star=ks, q_star=qs,
                               omega_star=om, omega_star_over_mvac=om / mvac,
                               flags=sorted(set(oa['Tcal_flags'] + ob['Tcal_flags']))))
    # d2E/dR2 along fixed-(n, Q) ray through each equilibrium, from an interpolant of the E grid
    pts = np.array([[i, j] for (i, j) in win], float)       # index coordinates (k/DK, q/DQ)
    Ev = np.array([win[ij]['E'] for ij in win])
    interp = CloughTocher2DInterpolator(pts, Ev) if len(pts) >= 3 else None
    for c in sc:
        ks, qs = c['k_star'], c['q_star']
        n = max(1, int(round(8 * ks))) if ks > 0 else 1
        Req = n / ks if ks > 0 else float('inf')
        Q = 2 * np.pi * Req * qs
        c.update(n=n, R_eq=Req, Q=Q)
        def Efun(R, ip=interp):
            kk = n / R; qq = Q / (2 * np.pi * R)
            return 2 * np.pi * R * float(ip(kk / DK, qq / DQ)) if ip is not None else float('nan')
        d2 = {}
        for h in (0.03, 0.06):
            if np.isfinite(Req):
                Rp, Rm_ = Req * (1 + h), Req * (1 - h)
                d2[f'h={h}'] = (Efun(Rp) - 2 * Efun(Req) + Efun(Rm_)) / (Req * h) ** 2
            else:
                d2[f'h={h}'] = float('nan')
        c['d2E_dR2_interp'] = d2
        c['d2E_dR2'] = d2['h=0.03']
        c['stable_R'] = bool(np.isfinite(c['d2E_dR2']) and c['d2E_dR2'] > 0)
        # cross-check (not part of the verdict): direct solves on the ray, warm-started from the nearest grid point
        if np.isfinite(Req):
            Ed = {}
            for u in (-0.03, 0.0, 0.03):
                R = Req * (1 + u); kk, qq = n / R, Q / (2 * np.pi * R)
                near = min(sol, key=lambda ij: ((ij[0] * DK - kk)) ** 2 + ((ij[1] * DQ - qq)) ** 2)
                o, _ = solve_line(P, kk, qq, sol[near][1])
                Ed[u] = 2 * np.pi * R * o['E']
                if not o['success']:
                    log.append(f'[{tag}] ray cross-check solve not converged k={kk:.4f} q={qq:.4f}: {o["message"]}')
            c['d2E_dR2_direct'] = (Ed[0.03] - 2 * Ed[0.0] + Ed[-0.03]) / (Req * 0.03) ** 2
    good = [c for c in sc if c['stable_R']]
    verdict = 'WINDOW' if good else 'NONE'
    ratios = [(o['Tcal'] / o['E'], o['k'], o['q']) for o in win.values() if o['Tcal'] is not None]
    mn = min(ratios) if ratios else (float('nan'), None, None)
    kmax = max((ij[0] for ij in win), default=None)
    qmax_by_k = {f'{i * DK:.2f}': max(j for (ii, j) in win if ii == i) * DQ for i in sorted({ij[0] for ij in win})}
    o00 = sol[(0, 0)][0]
    return dict(n_solves=len(sol), n_in_window=len(win), n_not_converged=sum(not v[0]['success'] for v in sol.values()),
                k_max_in_window=None if kmax is None else kmax * DK, q_max_in_window_by_k=qmax_by_k,
                sign_changes=sc, verdict=verdict,
                best_omega_star_over_mvac=min((c['omega_star_over_mvac'] for c in good), default=None),
                min_Tcal_over_E=float(mn[0]), argmin_Tcal_over_E=dict(k=mn[1], q=mn[2]),
                T00=o00['E'], I00=o00['I'], sigma0_00=o00['sigma0'], in_window_00=o00['in_window'])


def crude(summ, mu2, e0, mvac):
    """PREREG_option4 §1.3 crude estimate: ring holds iff k^2 + w^2 ~ T/I_c, reachable only if
    T/I_c <= (mu2 - eps0) + 2 m_vac^2 (sigma profile frozen at k = q = 0)."""
    TI = summ['T00'] / summ['I00']; lim = (mu2 - e0) + 2 * mvac ** 2
    return dict(T_over_Ic=TI, limit=lim, crude_feasible=bool(TI <= lim))


if __name__ == '__main__':
    t_start = time.time()
    print(f'Python {platform.python_version()}, NumPy {np.__version__}, SciPy {scipy.__version__}, '
          f'{os.cpu_count()} cores', flush=True)
    gc = gradient_check()
    print('gradient check (full functional, k=0.3, q=1.7, beta=2, mu2=3.6, lam=4), worst relative error:', gc, flush=True)
    gc0 = gradient_check(seed=2, P=(1.0, 2.5, 2.0), k=0.0, q=0.5)
    print('gradient check (k=0, q=0.5, beta=1, mu2=2.5, lam=2), worst relative error:', gc0, flush=True)
    cc = consistency_check()
    print('consistency with option4_design functional at q=0 (rel. energy diff, max grad diff):', cc, flush=True)

    rb = od.solve((0, 0, 1, 0), with_s=False)
    fb, ab, _ = unpack(rb.x, False)
    T0 = float(rb.fun)
    print(f'bare string: T0 = {T0:.4f}, converged={rb.success} ({rb.message}), '
          f'r(f^2=(1+eta)/2) = {np.interp(0.5 * (1 + eta), fb ** 2, r):.3f}', flush=True)
    e0s = {b: float(eps0(fb, b)) for b in BETAS}
    print('eps0(beta):', {b: round(v, 3) for b, v in e0s.items()}, '(PREREG §1.3: 2.047, 3.163, 4.025, 5.397)', flush=True)

    points, c3 = [], {}
    for b in BETAS:
        for d in DELTAS:
            tag = f'b{b:g}_d{d:g}'
            mu2 = e0s[b] + d; lam = mu2 ** 2 / (1.6 * D); m2 = 3 * b * (1 + eta) - mu2
            c = c3_check(b, mu2, lam); c3[tag] = c
            print(f'[{tag}] mu2={mu2:.4f} lam={lam:.4f} m2_vac={m2:.4f} C3 {"PASS" if c["passed"] else "FAIL"} '
                  f'(min: {c["analytic_min"]}, polish rho={c["grid_polish"]["rho"]:.6f} S={c["grid_polish"]["S"]:.2e}, '
                  f'sigma-vac above psi-vac by {c["sigma_vac_above_psi_vac"]:.4f})', flush=True)
            points.append(dict(tag=tag, beta=b, delta=d, mu2=mu2, lam=lam, m2_vac=m2,
                               m_vac=float(np.sqrt(m2)) if m2 > 0 else float('nan'), eps0=e0s[b], C3=c['passed']))
    jobs = [(p['tag'], p['beta'], p['delta'], p['mu2'], p['lam'], p['m_vac'], rb.x) for p in points if p['C3'] and p['m2_vac'] > 0]
    with Pool(min(4, os.cpu_count())) as pool:
        out = pool.map(scan_point, jobs, chunksize=1)
    res = {tag: (recs, summ, log) for tag, recs, summ, log in out}

    results = dict(meta=dict(label='Exploration', prereg='PREREG_option4.md §2', dr=dr, rmax=rmax, dk=DK, dq=DQ,
                             sigma_min=SIG_MIN, r_tail=R_TAIL, tail_max=TAIL_MAX, D=D, eta=eta, e=e,
                             minimizer=dict(method='L-BFGS-B', **OPTS),
                             software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)),
                   gradient_check=dict(worst_rel_err=gc, worst_rel_err_k0=gc0),
                   consistency_with_design=dict(rel_E_diff=cc[0], max_grad_diff=cc[1]),
                   bare=dict(T0=T0, converged=bool(rb.success), eps0=e0s), C3=c3, points=[])
    print('\nper-point summary', flush=True)
    for p in points:
        entry = dict(p)
        if p['tag'] in res:
            recs, summ, log = res[p['tag']]
            entry['summary'] = summ; entry['solves'] = recs
            entry['crude'] = crude(summ, p['mu2'], p['eps0'], p['m_vac'])
            # crude per-(k,q) sign: Tc = T00 - (k^2 + w_c^2) I_c, w_c = q / (2 I_c)
            agree = tot = 0
            for o in recs:
                if o['in_window'] and o['Tcal'] is not None:
                    wc = o['q'] / (2 * summ['I00'])
                    tcr = summ['T00'] - (o['k'] ** 2 + wc ** 2) * summ['I00']
                    o['Tcal_crude'] = tcr
                    tot += 1; agree += int(np.sign(tcr) == np.sign(o['Tcal']))
            entry['crude']['sign_agreement'] = dict(agree=agree, total=tot)
            print(f"{p['tag']}: verdict {summ['verdict']}, n_in={summ['n_in_window']}, k_max={summ['k_max_in_window']}, "
                  f"min(T/E)={summ['min_Tcal_over_E']:.4f} at {summ['argmin_Tcal_over_E']}, "
                  f"crude T/I_c={entry['crude']['T_over_Ic']:.3f} vs limit {entry['crude']['limit']:.3f}, "
                  f"crude sign agreement {agree}/{tot}", flush=True)
        else:
            entry['summary'] = dict(verdict='DROPPED (C3)')
        results['points'].append(entry)
    scanned = [p for p in results['points'] if 'solves' in p]
    win_pts = [p for p in scanned if p['summary']['verdict'] == 'WINDOW']
    if win_pts:
        sel = min(win_pts, key=lambda p: (p['summary']['best_omega_star_over_mvac'], p['beta']))
        c = min((c for c in sel['summary']['sign_changes'] if c['stable_R']), key=lambda c: c['omega_star_over_mvac'])
        results['selection'] = dict(kind='selected (WINDOW)', tag=sel['tag'], k_star=c['k_star'], q_star=c['q_star'],
                                    omega_star_over_mvac=c['omega_star_over_mvac'], n=c['n'], R_eq=c['R_eq'], Q=c['Q'])
    else:
        prb = min(scanned, key=lambda p: p['summary']['min_Tcal_over_E'])
        am = prb['summary']['argmin_Tcal_over_E']
        ks, qs = am['k'], am['q']
        n = max(1, int(round(8 * ks))); Req = n / ks if ks > 0 else float('inf'); Q = 2 * np.pi * Req * qs
        results['selection'] = dict(kind='thick-vorton probe (all NONE)', tag=prb['tag'],
                                    min_Tcal_over_E=prb['summary']['min_Tcal_over_E'], at_k=ks, at_q=qs,
                                    n=n, R_eq=Req, Q=Q,
                                    note='no equilibrium exists; (k, q) taken at argmin(Tcal/E) (flagged reading)')
    results['P0_at_least_one_WINDOW'] = bool(win_pts)
    results['total_seconds'] = time.time() - t_start
    print('\nselection:', json.dumps(results['selection']), flush=True)
    print('P0 (at least one WINDOW):', bool(win_pts), flush=True)
    print(f'total {results["total_seconds"]:.0f} s', flush=True)
    with open('phase0_results.json', 'w') as fh:
        json.dump(results, fh, indent=1, default=float)
