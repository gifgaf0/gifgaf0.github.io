"""E1d cross-check: colliding Gaussian packets, recomputed with 6th-order FD + RK4 (dx=0.08).

Initial data and run rules follow the description in PLAN.md / the original REPORT.md
(not its code):
  phi = -1 + A G(x+x0) cos(k(x+x0)) + A G(x-x0) cos(k(x-x0)),  G(y)=exp(-y^2/2 sigma^2)
  phi_t chosen so that each packet moves TOWARD the centre at v_g = k/omega_k,
  omega_k = sqrt(k^2+2):  phi_t = +A w G(x+x0) sin(k(x+x0)) - A w G(x-x0) sin(k(x-x0)).
  x0 = 4 sigma + 10, t_coll = x0/v_g, T = max(t_coll+400, 1.25(t_coll+100)),
  L_phys = x0 + 4 sigma + 40.  My sponge: cubic ramp over W=60 (original: quadratic, W=50).
Production = report's pair test at 0.80,0.85,0.90,0.95,1.00 T.  My own pair test is also recorded.

Modes:  coarse  (full 1485-point coarse grid, random order, resumable JSONL)
        single  (single right-moving packet for producing coarse points, sample)
        line    (constant-k line on the sigma=16 slice: A = 0.05..1.5 step 0.025 at k=1.0)
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xc_core import rk4_steps, sponge, make_grid, energy, pair_test_report, pair_test_mine, MKINK

HERE = os.path.dirname(os.path.abspath(__file__))
DX, DT, W = 0.08, 0.032, 60.0

AS = [round(0.1 * i, 1) for i in range(1, 16)]
SIGS = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0]
KS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]


def init(x, A, sig, k, x0, single=False):
    w = np.sqrt(k * k + 2.0)
    yl = x + x0; yr = x - x0
    Gl = np.exp(-yl ** 2 / (2 * sig ** 2)); Gr = np.exp(-yr ** 2 / (2 * sig ** 2))
    phi = -1.0 + A * Gl * np.cos(k * yl)
    pi = A * w * Gl * np.sin(k * yl)
    if not single:
        phi = phi + A * Gr * np.cos(k * yr)
        pi = pi - A * w * Gr * np.sin(k * yr)
    return phi, pi


def run(A, sig, k, single=False, dx=DX, dt=DT, x0shift=0.0):
    w = np.sqrt(k * k + 2.0); vg = k / w
    x0 = 4 * sig + 10 + x0shift
    tcoll = x0 / vg
    T = max(tcoll + 400, 1.25 * (tcoll + 100))
    Lp = x0 + 4 * sig + 40
    x = make_grid(Lp + W, dx)
    gam = sponge(x, Lp, W, 1.0)
    phi, pi = init(x, A, sig, k, x0, single)
    E0 = energy(phi, pi, dx)
    checks = [0.80, 0.85, 0.90, 0.95, 1.00]
    t = 0.0
    rep, mine = [], []
    for c in checks:
        nst = int(round((c * T - t) / dt))
        rk4_steps(phi, pi, gam, dx, dt, nst)
        t += nst * dt
        rep.append(pair_test_report(phi, dx))
        mine.append(pair_test_mine(phi, dx))
    Ef = energy(phi, pi, dx)
    return dict(A=A, sigma=sig, k=k, single=single, E_over_2M=E0 / (2 * MKINK), T=T,
                prod=bool(all(rep)), prod_mine=bool(all(mine)), rep=rep, Ef_over_E0=Ef / E0,
                maxphi_end=float(phi.max()), x0shift=x0shift, dx=dx)


def jsonl_load(path):
    out = {}
    if os.path.exists(path):
        for line in open(path):
            try:
                r = json.loads(line)
            except Exception:
                continue
            out[(r['A'], r['sigma'], r['k'], r.get('single', False), r.get('x0shift', 0.0), r.get('dx', DX))] = r
    return out


def append(path, r):
    with open(path, 'a') as f:
        f.write(json.dumps(r) + '\n')
        f.flush(); os.fsync(f.fileno())


def mode_coarse(worker=0, nworkers=1):
    path = os.path.join(HERE, f'xc_e1d_coarse_w{worker}.jsonl')
    done = jsonl_load(path)
    pts = [(A, s, k) for A in AS for s in SIGS for k in KS]
    rng = np.random.default_rng(20261019)
    order = rng.permutation(len(pts))
    mine = [pts[i] for j, i in enumerate(order) if j % nworkers == worker]
    t0 = time.time()
    for n, (A, s, k) in enumerate(mine):
        if (A, s, k, False, 0.0, DX) in done:
            continue
        r = run(A, s, k)
        append(path, r)
        if n % 25 == 0:
            print(f'[w{worker}] {n}/{len(mine)} A={A} s={s} k={k} E/2M={r["E_over_2M"]:.2f} prod={r["prod"]} '
                  f'Ef/E0={r["Ef_over_E0"]:.4f} elapsed {time.time()-t0:.0f}s', flush=True)
    print(f'[w{worker}] coarse done', flush=True)


def mode_line(k=1.0, sig=16.0):
    path = os.path.join(HERE, f'xc_e1d_line_s{sig}_k{k}.jsonl')
    done = jsonl_load(path)
    for i in range(59):
        A = round(0.05 + 0.025 * i, 3)
        if (A, sig, k, False, 0.0, DX) in done:
            continue
        r = run(A, sig, k)
        append(path, r)
        print(f'line A={A} prod={r["prod"]} E/2M={r["E_over_2M"]:.2f}', flush=True)


def mode_single(nmax=100):
    """Single-packet control for a random sample of MY producing coarse points."""
    prod = []
    for wkr in range(4):
        p = os.path.join(HERE, f'xc_e1d_coarse_w{wkr}.jsonl')
        prod += [r for r in jsonl_load(p).values() if r['prod']]
    prod.sort(key=lambda r: (r['A'], r['sigma'], r['k']))
    rng = np.random.default_rng(7)
    idx = rng.permutation(len(prod))[:nmax]
    path = os.path.join(HERE, 'xc_e1d_single.jsonl')
    done = jsonl_load(path)
    for i in idx:
        r0 = prod[i]
        key = (r0['A'], r0['sigma'], r0['k'], True, 0.0, DX)
        if key in done:
            continue
        r = run(r0['A'], r0['sigma'], r0['k'], single=True)
        append(path, r)
        print(f'single A={r["A"]} s={r["sigma"]} k={r["k"]} prod={r["prod"]}', flush=True)


def mode_dxself(n=100):
    """Self-consistency of MY code: rerun a random subset (E>2M by original energy) at dx=0.05, dt=0.02."""
    orig = json.load(open(os.path.join(os.path.dirname(HERE), 'e1d_coarse.json')))['runs']
    pts = sorted([(r['A'], r['sigma'], r['k']) for r in orig if r['E_over_2M'] > 1.0])
    rng = np.random.default_rng(11)
    idx = rng.permutation(len(pts))[:n]
    path = os.path.join(HERE, 'xc_e1d_dxself.jsonl')
    done = jsonl_load(path)
    for i in idx:
        A, s, k = pts[i]
        if (A, s, k, False, 0.0, 0.05) in done:
            continue
        r = run(A, s, k, dx=0.05, dt=0.02)
        append(path, r)
        print(f'dxself A={A} s={s} k={k} prod={r["prod"]}', flush=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'coarse':
        mode_coarse(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == 'line':
        mode_line(float(sys.argv[2]), float(sys.argv[3]))
    elif mode == 'dxself':
        mode_dxself(int(sys.argv[2]))
    elif mode == 'single':
        mode_single(int(sys.argv[2]))
