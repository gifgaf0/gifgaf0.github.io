#!/usr/bin/env python3
"""
Driver for the isotropic-gauge spectral cross-check (see xc_iso.py).
Stages (each checkpointed to out/xc_<stage>.json; delete to recompute):
  flat    : flat skyrmion, convergence in (N, L)
  cont    : pseudo-arclength continuation flat -> fold -> upper branch (with regridding)
  fold    : Moore-Spence fold location for several (N, L)
  fixed   : solutions at fixed alpha on both branches (table comparison)
  slope   : small-alpha lower-branch masses -> O(alpha) coefficient (fit)
  upper   : upper branch towards small alpha, sqrt(alpha) m -> Bartnik-McKinnon
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xc_iso as X

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(*a):
    print('[%7.1fs]' % (time.time() - T0), *a, flush=True)


def ck(name):
    return os.path.join(OUT, 'xc_%s.json' % name)


def save(name, obj):
    json.dump(obj, open(ck(name), 'w'), indent=1, default=float)


def have(name):
    return os.path.exists(ck(name))


def flat_solution(N, L):
    g = X.Grid(N, L)
    U, ok = X.newton(X.flat_guess(g), 0.0, g)
    assert ok
    return g, U


def x_half(U, g):
    F = X.fields(U, g)[0]
    sd = np.linspace(1e-4, 0.99, 3000)
    Fd = g.interp(F, sd)
    k = np.argmax(Fd < np.pi / 2)
    s0 = sd[k - 1] + (sd[k] - sd[k - 1]) * (Fd[k - 1] - np.pi / 2) / (Fd[k - 1] - Fd[k])
    return g.L * s0 / (1 - s0)


def summary(U, a, g):
    d = dict(alpha=a, N=g.N, L=g.L)
    d.update(X.central(U, g))
    mm = X.masses(U, a, g)
    d.update(mm)
    R, Nn, xd = X.N_profile(U, g)
    k = np.argmin(Nn)
    d.update(Nmin=Nn[k], R_at_Nmin=R[k])
    d['xhalf'] = x_half(U, g)
    return d


# ------------------------------------------------------------------ stage: flat
if not have('flat'):
    rows = []
    for N in (40, 60, 80, 100):
        for L in (1.0, 1.5, 2.5):
            g, U = flat_solution(N, L)
            s = summary(U, 0.0, g)
            rows.append(s)
            log('flat N=%d L=%.1f m0=%.13f b=%.11f E2-E4=%.2e vonLaue=%.2e' % (N, L, s['m_int'], s['b_schw'], s['E2_flatform'] - s['E4_flatform'], s['tolman_minus_rho_int']))
    save('flat', rows)

# ------------------------------------------------------------------ stage: continuation
W = 100.0
if not have('cont'):
    N, L = 60, 1.5
    g, U = flat_solution(N, L)
    a = 0.0
    n = U.size
    Y = np.concatenate([U, [a * W]])
    tau0 = np.zeros(n + 1); tau0[-1] = 1.0
    tau = X.tangent(U, a, g, tau0, W)
    if tau[-1] < 0:
        tau = -tau
    ds = 0.3
    rows = []
    passed_fold = False
    fold_bracket = None
    step = 0
    while True:
        Ypred = Y + ds * tau
        Ynew, ok = X.corrector(Ypred.copy(), tau, Ypred, g, W)
        if not ok or Ynew[-1] / W < -1e-12:
            ds *= 0.5
            if ds < 1e-6:
                log('step too small; stop'); break
            continue
        Unew, anew = Ynew[:-1], Ynew[-1] / W
        taunew = X.tangent(Unew, anew, g, tau, W)
        if taunew @ tau < 0:
            taunew = -taunew
        if tau[-1] > 0 and taunew[-1] <= 0 and fold_bracket is None:
            fold_bracket = dict(a1=Y[-1] / W, a2=anew)
            passed_fold = True
            np.save(os.path.join(OUT, 'xc_fold_guess.npy'), np.concatenate([Y, tau]))
            save('fold_guess_meta', dict(N=g.N, L=g.L, W=W))
        Y, tau = Ynew, taunew
        step += 1
        s = summary(Unew, anew, g)
        s['branch'] = 'upper' if passed_fold else 'lower'
        s['tau_alpha'] = tau[-1]
        rows.append(s)
        if step % 5 == 0:
            log('cont step %d alpha=%.8f b=%.6f m=%.6f xhalf=%.4f L=%.4f ds=%.3g %s' % (step, anew, s['b_schw'], s['m_int'], s['xhalf'], g.L, ds, s['branch']))
        ds = min(ds * 1.3, 0.6 if abs(anew - 0.0404) > 0.002 else 0.1)
        # regrid on the upper branch as the soliton shrinks
        xh = s['xhalf']
        if xh / g.L < 0.45 or xh / g.L > 1.8:
            gnew = X.Grid(g.N, max(xh, 1e-3))
            Ur = X.regrid(Unew, g, gnew)
            Ur, ok2 = X.newton(Ur, anew, gnew)
            if not ok2:
                log('regrid newton failed'); break
            g = gnew
            Y = np.concatenate([Ur, [anew * W]])
            tprev = np.zeros(Ur.size + 1); tprev[-1] = (-1.0 if passed_fold else 1.0)
            tau = X.tangent(Ur, anew, g, tprev, W)
            if (tau[-1] > 0) == passed_fold:
                tau = -tau
            log('  regrid -> L=%.4g' % g.L)
        if passed_fold and anew < 2e-3:
            break
        if step > 400:
            break
    save('cont', dict(rows=rows, fold_bracket=fold_bracket))

# ------------------------------------------------------------------ stage: fold
# (A Moore-Spence extended system was tried first and hit a singular bordered matrix;
#  replaced by locating tau_alpha = 0 along the pseudo-arclength branch on every grid,
#  plus a quadratic fit of alpha(arclength) around the maximum as a second estimator.)
def fold_on_grid(g, U_init, a_init, W=100.0):
    J = X.jac(U_init, a_init, g); J[:, -1] /= W
    t = np.linalg.svd(J)[2][-1]
    Y0 = np.concatenate([U_init, [a_init * W]])
    Yc, ok = X.corrector(Y0.copy(), t, Y0, g, W)
    assert ok
    tb = X.tangent(Yc[:-1], Yc[-1] / W, g, t, W)
    # orient along increasing central slope b
    b0 = X.central(Yc[:-1], g)['b_schw']
    if X.central(Yc[:-1] + 1e-4 * tb[:-1], g)['b_schw'] < b0:
        tb = -tb

    cache = {}

    def at(h):
        if h in cache:
            return cache[h]
        Yp = Yc + h * tb
        Yh, ok = X.corrector(Yp.copy(), tb, Yp, g, W)
        th = X.tangent(Yh[:-1], Yh[-1] / W, g, tb, W)
        if th @ tb < 0:
            th = -th
        cache[h] = (th[-1], Yh, th)
        return cache[h]

    # bracket
    hs = [0.0]
    f0 = at(0.0)[0]
    step = 0.02 if f0 > 0 else -0.02
    h1, f1 = 0.0, f0
    for k in range(40):
        h2 = h1 + step
        f2 = at(h2)[0]
        if f2 * f1 <= 0:
            break
        h1, f1 = h2, f2
    lo, hi = (h1, h2) if f1 > 0 else (h2, h1)
    flo, fhi = at(lo)[0], at(hi)[0]
    for k in range(60):
        hm = lo - flo * (hi - lo) / (fhi - flo) if k % 3 else 0.5 * (lo + hi)
        fm, Ym, tm = at(hm)
        if fm > 0:
            lo, flo = hm, fm
        else:
            hi, fhi = hm, fm
        if abs(fm) < 1e-14 or abs(hi - lo) < 1e-13:
            break
    a_tau = Ym[-1] / W
    # quadratic fit of alpha(h) on 7 points around the fold
    hh = hm + np.linspace(-0.06, 0.06, 7)
    aa = np.array([at(h)[1][-1] / W for h in hh])
    bb = np.array([X.central(at(h)[1][:-1], g)['b_schw'] for h in hh])
    cf = np.polyfit(hh - hm, aa, 4)
    pp = np.poly1d(cf)
    r = [z.real for z in np.roots(np.polyder(pp)) if abs(z.imag) < 1e-12 and abs(z.real) < 0.06]
    hstar = min(r, key=abs)
    a_fit = pp(hstar)
    cfb = np.polyfit(bb, aa, 4); pb = np.poly1d(cfb)
    rb = [z.real for z in np.roots(np.polyder(pb)) if abs(z.imag) < 1e-12 and bb.min() < z.real < bb.max()]
    bstar = rb[0]
    curv = 0.5 * np.polyder(pb, 2)(bstar)
    return Ym[:-1], a_tau, tm[:-1], dict(alpha_tau=a_tau, alpha_fit_h=a_fit, alpha_fit_b=pb(bstar), b_fit=bstar,
                                         curvature_alpha_b=curv, tau_resid=fm)


if not have('fold'):
    meta = json.load(open(ck('fold_guess_meta')))
    z = np.load(os.path.join(OUT, 'xc_fold_guess.npy'))
    g0 = X.Grid(meta['N'], meta['L'])
    n0 = 3 * (meta['N'] + 1)
    Yb = z[:n0 + 1]
    U0, a0 = Yb[:-1], Yb[-1] / meta['W']
    U0, a0, t0, info = fold_on_grid(g0, U0, a0)
    log('fold base grid N=%d L=%.4f: alpha=%.15f' % (g0.N, g0.L, a0))
    rows = []
    for (N, L) in [(60, g0.L), (80, g0.L), (100, g0.L), (120, g0.L), (80, 0.4), (80, 1.2), (100, 1.0)]:
        g = X.Grid(N, L)
        U = X.regrid(U0, g0, g)
        U, a, v, info = fold_on_grid(g, U, a0)
        s = summary(U, a, g)
        s.update(info)
        gr, grs = X.Grr_residual(U, a, g)
        s['Grr_resid'] = gr; s['Grr_scale'] = grs
        s['res_max'] = float(np.abs(X.residual(U, a, g)).max())
        rows.append(s)
        log('  N=%d L=%.3f alpha_crit=%.15f (fit_h %.15f, fit_b %.15f) b_crit=%.8f curv=%.6f b_schw=%.9f m_int=%.10f m_adm_tail=%.10f m_komar=%.10f A0=%.8f Nmin=%.8f@R=%.5f Grr=%.1e' % (
            N, L, a, info['alpha_fit_h'], info['alpha_fit_b'], info['b_fit'], info['curvature_alpha_b'], s['b_schw'], s['m_int'],
            s['m_adm_tail'], s['m_komar_int'], s['A0'], s['Nmin'], s['R_at_Nmin'], gr))
        if N == 100 and abs(L - g0.L) < 1e-12:
            np.save(os.path.join(OUT, 'xc_fold_U.npy'), np.concatenate([U, [a]]))
            np.save(os.path.join(OUT, 'xc_fold_grid.npy'), np.array([N, L]))
    save('fold', rows)

# ------------------------------------------------------------------ stage: fixed alpha
if not have('fixed'):
    cont = json.load(open(ck('cont')))['rows']
    alphas = [0.001, 0.01, 0.02, 0.03, 0.035, 0.04, 0.04037]
    rows = []
    # redo a short continuation and snap to the requested alphas (Newton at fixed alpha)
    N, L = 80, 1.5
    g, U = flat_solution(N, L)
    a = 0.0
    W = 100.0
    Y = np.concatenate([U, [0.0]])
    tau0 = np.zeros(U.size + 1); tau0[-1] = 1
    tau = X.tangent(U, a, g, tau0, W)
    if tau[-1] < 0: tau = -tau
    targets_lower = sorted(alphas)
    targets_upper = sorted(alphas, reverse=True)
    passed = False
    ds = 0.2
    prevY, prevg = Y.copy(), g
    sols = {'lower_0_U': U.copy(), 'lower_0_NL': np.array([g.N, g.L])}
    done_l, done_u = set(), set()
    it = 0
    while it < 600:
        it += 1
        Ypred = Y + ds * tau
        Yn, ok = X.corrector(Ypred.copy(), tau, Ypred, g, W)
        if not ok:
            ds *= 0.5; continue
        tn = X.tangent(Yn[:-1], Yn[-1] / W, g, tau, W)
        if tn @ tau < 0: tn = -tn
        a_old, a_new = Y[-1] / W, Yn[-1] / W
        if tau[-1] > 0 and tn[-1] <= 0:
            passed = True
        lst = targets_upper if passed else targets_lower
        for at in lst:
            key = ('u' if passed else 'l', at)
            if key in (done_u | done_l):
                continue
            if (a_old - at) * (a_new - at) <= 0 and a_old != a_new:
                # interpolate start and Newton at fixed alpha
                w = (at - a_old) / (a_new - a_old)
                Ust = (1 - w) * Y[:-1] + w * Yn[:-1]
                Us, okk = X.newton(Ust, at, g)
                s = summary(Us, at, g)
                s['branch'] = 'upper' if passed else 'lower'
                rows.append(s)
                sols['%s_%g_U' % (s['branch'], at)] = Us
                sols['%s_%g_NL' % (s['branch'], at)] = np.array([g.N, g.L])
                (done_u if passed else done_l).add(key)
                log('fixed alpha=%.5f %s b=%.6f m=%.7f (adm tail %.7f)' % (at, s['branch'], s['b_schw'], s['m_int'], s['m_adm_tail']))
        Y, tau = Yn, tn
        ds = min(ds * 1.3, 0.05 if a_new > 0.0402 else (0.4 if a_new > 0.039 else 0.6))
        xh = x_half(Yn[:-1], g)
        if xh / g.L < 0.45 or xh / g.L > 1.8:
            gnew = X.Grid(g.N, xh)
            Ur = X.regrid(Yn[:-1], g, gnew)
            Ur, ok2 = X.newton(Ur, a_new, gnew)
            g = gnew
            Y = np.concatenate([Ur, [a_new * W]])
            tp = np.zeros(Ur.size + 1); tp[-1] = (-1.0 if passed else 1.0)
            tau = X.tangent(Ur, a_new, g, tp, W)
            if (tau[-1] > 0) == passed: tau = -tau
        if passed and a_new < 0.0009:
            break
    np.savez(os.path.join(OUT, 'xc_fixed_sols.npz'), **sols)
    save('fixed', rows)

# ------------------------------------------------------------------ stage: slope
if not have('slope'):
    rows = []
    for (N, L) in [(60, 1.5), (80, 1.5), (80, 2.5)]:
        g, U = flat_solution(N, L)
        m0 = X.masses(U, 0.0, g)['m_int']
        A00 = U[2 * (N + 1)]
        pts = []
        for a in np.arange(1, 11) * 2e-4:
            U, ok = X.newton(U, a, g)
            mm = X.masses(U, a, g)
            c = X.central(U, g)
            pts.append(dict(alpha=a, m_int=mm['m_int'], m_adm_tail=mm['m_adm_tail'], m_komar_int=mm['m_komar_int'],
                            A0=c['A0'], b_schw=c['b_schw']))
        al = np.array([p['alpha'] for p in pts]); mi = np.array([p['m_int'] for p in pts])
        A0 = np.array([p['A0'] for p in pts])
        fits = {}
        for deg in (2, 3, 4):
            cf = np.polyfit(al, (mi - m0) / al, deg - 1)
            fits['deg%d' % deg] = cf[-1]
            cfA = np.polyfit(al, (np.log(A0)) / al, deg - 1)
            fits['lnA0_deg%d' % deg] = cfA[-1]
        # free-intercept fit (does M_ADM -> E_flat?)
        cf_free = np.polyfit(al, mi, 4)
        rows.append(dict(N=N, L=L, m0=m0, pts=pts, fits=fits, free_intercept=cf_free[-1], free_slope=cf_free[-2]))
        log('slope N=%d L=%.1f m1(deg2,3,4)=%.9f %.9f %.9f  dlnA0/dalpha=%.7f  intercept/m0-1=%.2e' % (
            N, L, fits['deg2'], fits['deg3'], fits['deg4'], fits['lnA0_deg3'], cf_free[-1] / m0 - 1))
    save('slope', rows)

# ------------------------------------------------------------------ stage: upper branch to small alpha
if not have('upper'):
    z = np.load(os.path.join(OUT, 'xc_fold_U.npy'))
    NL = np.load(os.path.join(OUT, 'xc_fold_grid.npy'))
    g = X.Grid(int(NL[0]), float(NL[1]))
    U, a = z[:-1], z[-1]
    # step down the upper branch at fixed alpha values by natural continuation in b-space:
    # use pseudo-arclength from the fold heading to smaller alpha on the upper side.
    W = 100.0
    J = X.jac(U, a, g)
    uu, ss, vh = np.linalg.svd(J[:, :-1]); v = vh[-1]
    tau = np.concatenate([v, [0.0]])
    # choose direction of increasing b (upper branch)
    c0 = X.central(U, g)['b_schw']
    Up = U + 1e-3 * v
    if X.central(Up, g)['b_schw'] < c0:
        tau = -tau
    Y = np.concatenate([U, [a * W]])
    ds = 0.05
    rows = []
    targets = [0.03, 0.02, 0.01, 0.005, 0.002, 0.001, 5e-4, 3e-4, 2e-4, 1e-4, 5e-5]
    it = 0
    while it < 3000 and targets:
        it += 1
        Ypred = Y + ds * tau
        Yn, ok = X.corrector(Ypred.copy(), tau, Ypred, g, W)
        if not ok:
            ds *= 0.5
            if ds < 1e-7: log('upper: stuck'); break
            continue
        tn = X.tangent(Yn[:-1], Yn[-1] / W, g, tau, W)
        if tn @ tau < 0: tn = -tn
        a_old, a_new = Y[-1] / W, Yn[-1] / W
        while targets and (a_old - targets[0]) * (a_new - targets[0]) <= 0:
            at = targets.pop(0)
            w = (at - a_old) / (a_new - a_old)
            Us, okk = X.newton((1 - w) * Y[:-1] + w * Yn[:-1], at, g)
            # resolution check: same solution on a finer grid
            g2 = X.Grid(g.N + 30, g.L)
            Us2, ok2 = X.newton(X.regrid(Us, g, g2), at, g2)
            s = summary(Us, at, g); s2 = summary(Us2, at, g2)
            s['m_int_finer'] = s2['m_int']; s['m_adm_tail_finer'] = s2['m_adm_tail']
            s['sqrt_alpha_m'] = np.sqrt(at) * s2['m_int']
            rows.append(s)
            log('upper alpha=%.2e b=%.5f m=%.7f (finer %.7f) sqrt(a) m=%.7f A0=%.4e L=%.4f' % (at, s['b_schw'], s['m_int'], s2['m_int'], s['sqrt_alpha_m'], s['A0'], g.L))
        Y, tau = Yn, tn
        ds = min(ds * 1.25, 0.5)
        xh = x_half(Yn[:-1], g)
        if xh / g.L < 0.6 or xh / g.L > 1.6:
            gnew = X.Grid(g.N, xh)
            Ur = X.regrid(Yn[:-1], g, gnew)
            Ur, ok2 = X.newton(Ur, a_new, gnew)
            if not ok2: log('upper regrid failed'); break
            g = gnew
            Y = np.concatenate([Ur, [a_new * W]])
            tp = np.zeros(Ur.size + 1); tp[-1] = -1.0
            tau = X.tangent(Ur, a_new, g, tp, W)
            if tau[-1] > 0: tau = -tau
            ds = min(ds, 0.2)
        if it % 20 == 0:
            log('  upper it %d alpha=%.3e L=%.4f' % (it, a_new, g.L))
        save('upper_partial', rows)
    save('upper', rows)

log('done')
