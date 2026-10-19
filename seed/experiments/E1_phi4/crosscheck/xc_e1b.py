"""E1b cross-check: kink-antikink collisions with a Fourier pseudo-spectral + RK4 code.

Independent of the original (4th-order FD + leapfrog, absorbing layers, x0=12).
Here: periodic box of half-length LB evolving delta = phi + 1 (periodic since phi -> -1
at both ends), spectral phi_xx, classical RK4, cubic sponge for |x| > LS, x0 = 15.

Outputs crosscheck/xc_e1b.json (resumable: each v run is cached).
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'xc_e1b.json')
SQ2 = np.sqrt(2.0)


def run(v, dx=0.2, dt=0.04, LB=260.0, LS=215.0, x0=15.0, tpost=800.0, rec=False):
    N = int(round(2 * LB / dx))
    x = -LB + dx * np.arange(N)
    i0 = int(np.argmin(np.abs(x)))
    assert abs(x[i0]) < 1e-9
    k = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = k * k
    s = np.clip((np.abs(x) - LS) / (LB - LS), 0, 1)
    gam = 0.5 * s ** 3
    g = 1 / np.sqrt(1 - v * v)
    a = g / SQ2
    phi = np.tanh(a * (x + x0)) - np.tanh(a * (x - x0)) - 1
    pi = -(g * v / SQ2) * (1 / np.cosh(a * (x + x0)) ** 2 + 1 / np.cosh(a * (x - x0)) ** 2)
    d = phi + 1.0

    def acc(d, p):
        lap = np.fft.irfft(-k2 * np.fft.rfft(d), n=N)
        f = d - 1.0
        return lap - f * (f * f - 1.0) - gam * p

    tend = x0 / v + tpost
    nst = int(np.ceil(tend / dt))
    phic = np.empty(nst + 1)
    phic[0] = d[i0] - 1
    zt, zx = [], []
    for n in range(nst):
        a1 = acc(d, pi)
        d2 = d + 0.5 * dt * pi; p2 = pi + 0.5 * dt * a1
        a2 = acc(d2, p2)
        d3 = d + 0.5 * dt * p2; p3 = pi + 0.5 * dt * a2
        a3 = acc(d3, p3)
        d4 = d + dt * p3; p4 = pi + dt * a3
        a4 = acc(d4, p4)
        d = d + dt / 6 * (pi + 2 * p2 + 2 * p3 + p4)
        pi = pi + dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        phic[n + 1] = d[i0] - 1
        if (n + 1) % 50 == 0:
            # innermost zero of phi on the right half (x>0) where phi goes from + to -
            f = d[i0:] - 1
            neg = np.where(f < 0)[0]
            zt.append((n + 1) * dt)
            if f[0] > 0 and len(neg):
                j = neg[0]
                zx.append(float(x[i0 + j - 1] + dx * f[j - 1] / (f[j - 1] - f[j])))
            else:
                zx.append(0.0)
    t = dt * np.arange(nst + 1)
    # bounce count with hysteresis
    nb, armed = 0, True
    for val in phic:
        if armed and val < -0.3:
            nb += 1; armed = False
        elif (not armed) and val > 0.3:
            armed = True
    zt = np.array(zt); zx = np.array(zx)
    zf = zx[-1]
    zprev = zx[np.argmin(np.abs(zt - (zt[-1] - 200)))]
    # last time phi(0) was below -0.3
    below = np.where(phic < -0.3)[0]
    tlast = t[below[-1]] if len(below) else 0.0
    vout = (zf - zprev) / 200.0
    # v2 criterion (fixed after the first pass): no zf > x0 requirement, which misclassified slow escapes
    escape = (phic[-1] > 0.3) and (zf > 0) and (vout > 0.001 or zf > LS - 5) and (t[-1] - tlast > 200)
    label = nb if escape else 0
    res = dict(v=v, nb=nb, escape=bool(escape), label=int(label), zf=float(zf), vout=float(vout),
               tlast=float(tlast), dx=dx, dt=dt, x0=x0, tpost=tpost)
    if rec:
        # bounce times (down-crossings through 0) for the resonance check
        dc = np.where((phic[:-1] > 0) & (phic[1:] <= 0))[0]
        res['bounce_times'] = [float(t[j]) for j in dc]
    return res


def load():
    if os.path.exists(OUT):
        return json.load(open(OUT))
    return {}


def save(db):
    tmp = OUT + '.tmp'
    json.dump(db, open(tmp, 'w'), indent=0)
    os.replace(tmp, OUT)


def get(db, v, dx=0.2, dt=0.04, **kw):
    key = f'{v:.6f}_{dx}_{dt}'
    if key in db:
        r = db[key]
        tend = r['x0'] / r['v'] + r['tpost']
        esc = (r['zf'] > 0) and (r['vout'] > 0.001 or r['zf'] > 215.0 - 5) and (tend - r['tlast'] > 200)
        r['escape'] = bool(esc); r['label'] = int(r['nb'] if esc else 0)
    if key not in db:
        t0 = time.time()
        db[key] = run(v, dx=dx, dt=dt, **kw)
        save(db)
        r = db[key]
        print(f'v={v:.6f} dx={dx} dt={dt} nb={r["nb"]} esc={r["escape"]} label={r["label"]} zf={r["zf"]:.1f} vout={r["vout"]:.4f} ({time.time()-t0:.1f}s)', flush=True)
    return db[key]['label']


def bisect(db, lo, hi, llo, lhi, tol, **kw):
    """Predicate bisection (v2): the predicate is 'label == L', where L is whichever of llo/lhi is
    the target label (2 for windows, 1 for v_c); converges to the edge of the label-L region."""
    tgt = lhi if lhi in (1, 2) else llo
    side_lo = (llo == tgt)
    while hi - lo > tol:
        mid = round(0.5 * (lo + hi), 6)
        lm = get(db, mid, **kw)
        if (lm == tgt) == side_lo:
            lo = mid
        else:
            hi = mid
    return lo, hi


if __name__ == '__main__':
    db = load()
    # self-checks: energy-free sanity (escape at high v, capture at low v)
    vs = [round(0.180 + 0.001 * i, 3) for i in range(91)]
    labels = [get(db, v) for v in vs]
    print('scan labels:', list(zip(vs, labels)), flush=True)
    # v_c: last scan point (from top) that is not a 1-bounce escape
    j = len(vs) - 1
    while labels[j] == 1:
        j -= 1
    lo, hi = bisect(db, vs[j], vs[j + 1], labels[j], 1, 1e-5)
    vc = 0.5 * (lo + hi)
    print('v_c bracket', lo, hi, flush=True)
    # windows: maximal runs of label 2 in the scan
    wins = []
    i = 0
    while i < len(vs):
        if labels[i] == 2:
            jj = i
            while jj + 1 < len(vs) and labels[jj + 1] == 2:
                jj += 1
            wins.append((i, jj))
            i = jj + 1
        else:
            i += 1
    edges = []
    for (a, b) in wins[:3]:
        if a == 0 or b == len(vs) - 1:
            continue
        l0, l1 = bisect(db, vs[a - 1], vs[a], labels[a - 1], 2, 1e-5)
        h0, h1 = bisect(db, vs[b], vs[b + 1], 2, labels[b + 1], 1e-5)
        edges.append([0.5 * (l0 + l1), 0.5 * (h0 + h1)])
        print('window', edges[-1], flush=True)
    # dt check: halve dt for v_c and window-1 edges
    lo2, hi2 = bisect(db, round(vc - 0.0002, 6), round(vc + 0.0002, 6), get(db, round(vc - 0.0002, 6), dt=0.02), 1, 1e-5, dt=0.02)
    w1 = edges[0]
    a0 = round(w1[0] - 0.0002, 6); a1 = round(w1[0] + 0.0002, 6)
    la0 = get(db, a0, dt=0.02); la1 = get(db, a1, dt=0.02)
    e1lo = bisect(db, a0, a1, la0, la1, 1e-5, dt=0.02) if la0 != la1 else (None, None)
    b0 = round(w1[1] - 0.0002, 6); b1 = round(w1[1] + 0.0002, 6)
    lb0 = get(db, b0, dt=0.02); lb1 = get(db, b1, dt=0.02)
    e1hi = bisect(db, b0, b1, lb0, lb1, 1e-5, dt=0.02) if lb0 != lb1 else (None, None)
    # resonance check: bounce times in the middle of windows 1 and 2
    rec = {}
    for w in edges[:3]:
        vm = round(0.5 * (w[0] + w[1]), 5)
        r = run(vm, rec=True)
        rec[str(vm)] = r['bounce_times']
    summary = dict(vc=vc, vc_bracket=[lo, hi], windows=edges, vc_dt002=[lo2, hi2],
                   w1_dt002=[e1lo, e1hi], scan=list(zip(vs, labels)), bounce_times=rec,
                   n_windows_in_scan=len(wins))
    json.dump(summary, open(os.path.join(HERE, 'xc_e1b_summary.json'), 'w'), indent=1)
    print('SUMMARY', json.dumps({k: summary[k] for k in ['vc', 'vc_bracket', 'windows', 'vc_dt002', 'w1_dt002', 'n_windows_in_scan']}), flush=True)
