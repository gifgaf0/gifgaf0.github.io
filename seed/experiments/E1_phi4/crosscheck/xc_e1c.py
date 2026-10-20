"""E1c cross-check: Dutta-Steer-Vachaspati breather trains (arXiv:0803.0670 eqs. 11-13, read in
the paper itself), evolved with 6th-order FD + RK4 at dx=0.08, cubic sponge.

f(t,x) = -1 + sum_{n=-Nb..Nb, n!=0} (4/pi) atan[ eta sin(omega T_n) / cosh(eta omega X_n) ]
T_n = gamma [t - v_n (x - x0n)],  X_n = gamma [(x - x0n) - v_n t]
x0n = a + n d, v_n = -v for n>0;  x0n = -a + n d, v_n = +v for n<0
eta = sqrt(1-omega^2)/omega, Nb = int(2/sqrt(1-omega^2)) + 1, a = 10/sqrt(1-w^2), d = 2/sqrt(1-w^2)
Lattice half-width 600 (DSV Fig. 1 axis), evolve for one light-crossing time T = 1200 (and on to
1.25 T to see whether the pair survives).  Call: report's pair test at t = T.
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xc_core import rk4_steps, sponge, make_grid, energy, pair_test_report, pair_test_mine, MKINK

HERE = os.path.dirname(os.path.abspath(__file__))
DX, DT, W, LP = 0.08, 0.032, 80.0, 600.0


def dsv_init(x, om, v):
    s = np.sqrt(1 - om * om)
    eta = s / om
    Nb = int(2 / s) + 1
    a = 10 / s; d = 2 / s
    g = 1 / np.sqrt(1 - v * v)
    phi = -np.ones_like(x); pi = np.zeros_like(x)
    for n in list(range(-Nb, 0)) + list(range(1, Nb + 1)):
        if n > 0:
            x0n = a + n * d; vn = -v
        else:
            x0n = -a + n * d; vn = v
        T = g * (0 - vn * (x - x0n))
        X = g * ((x - x0n) - vn * 0)
        Y = eta * om * X
        u = eta * np.sin(om * T) / np.cosh(Y)
        sech = 1.0 / np.cosh(Y)  # overflow-safe: sinh/cosh^2 = tanh*sech
        ut = eta * om * g * (np.cos(om * T) * sech + eta * vn * np.sin(om * T) * np.tanh(Y) * sech)
        phi += (4 / np.pi) * np.arctan(u)
        pi += (4 / np.pi) * ut / (1 + u * u)
    return phi, pi, Nb


def run(om, v, dx=DX, dt=DT, tmax_fac=1.25, track=False):
    x = make_grid(LP + W, dx)
    gam = sponge(x, LP, W, 1.0)
    phi, pi, Nb = dsv_init(x, om, v)
    E0 = energy(phi, pi, dx)
    T = 2 * LP
    out = dict(omega=om, v=v, Nb=Nb, E_over_2M=E0 / (2 * MKINK), dx=dx)
    t = 0.0
    if track:
        dt = 0.03125   # 320 steps per 10 time units exactly
        hist = []
        step = 10.0
        while t < tmax_fac * T - 1e-9:
            nst = int(round(step / dt))
            rk4_steps(phi, pi, gam, dx, dt, nst)
            t += nst * dt
            hist.append((round(t, 3), pair_test_report(phi, dx), pair_test_mine(phi, dx)))
        out['hist'] = hist
        first = [h[0] for h in hist if h[1]]
        out['first_pair_t'] = first[0] if first else None
        out['pair_at_T'] = [h[1] for h in hist if abs(h[0] - T) < 1e-3][0]
        out['pair_at_end'] = hist[-1][1]
        return out
    res = {}
    for c in [0.9, 1.0, tmax_fac]:
        nst = int(round((c * T - t) / dt))
        rk4_steps(phi, pi, gam, dx, dt, nst)
        t += nst * dt
        res[c] = (pair_test_report(phi, dx), pair_test_mine(phi, dx))
    out['pair_09T'] = res[0.9][0]
    out['pair_T'] = res[1.0][0]
    out['pair_T_mine'] = res[1.0][1]
    out['pair_end'] = res[tmax_fac][0]
    out['Ef_over_E0'] = energy(phi, pi, dx) / E0
    return out


def append(path, r):
    with open(path, 'a') as f:
        f.write(json.dumps(r) + '\n'); f.flush(); os.fsync(f.fileno())


def load(path):
    out = {}
    if os.path.exists(path):
        for line in open(path):
            try:
                r = json.loads(line)
                out[(r['omega'], r['v'], r['dx'])] = r
            except Exception:
                pass
    return out


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode in ('example', 'map'):
        p = os.path.join(HERE, 'xc_e1c_example.json')
        if not os.path.exists(p):
            t0 = time.time()
            r = run(0.99, 0.43, tmax_fac=1.5, track=True)
            json.dump(r, open(p, 'w'))
            print('example', {k: r[k] for k in r if k != 'hist'}, f'{time.time()-t0:.0f}s', flush=True)
    if mode == 'map':
        p = os.path.join(HERE, 'xc_e1c_map.jsonl')
        done = load(p)
        oms = [0.90, 0.92, 0.94, 0.96, 0.98, 0.99]
        vs = [round(0.40 + 0.02 * i, 2) for i in range(26)]
        pts = [(o, v) for o in oms for v in vs] + [(0.995, v) for v in [0.3, 0.35, 0.4, 0.45, 0.5, 0.6]]
        if len(sys.argv) > 2 and sys.argv[2] == 'reverse':
            pts = pts[::-1]
        t0 = time.time()
        for n, (o, v) in enumerate(pts):
            done = load(p)   # re-read: another worker may share the file
            if (o, v, DX) in done:
                continue
            r = run(o, v)
            append(p, r)
            print(f'{n}/{len(pts)} omega={o} v={v} E/2M={r["E_over_2M"]:.2f} pair_T={r["pair_T"]} end={r["pair_end"]} '
                  f'Ef/E0={r["Ef_over_E0"]:.3f} ({time.time()-t0:.0f}s)', flush=True)
