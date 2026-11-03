"""
E10 Route B, B2 (PREREG_B2B3 §2): straight-string calibration on the 2D lattice (u3lattice.py), with the radial
reduction (u3radial.py) as cross-check and as the source of the abelian-Higgs-like starting profiles.

  C1  T(elementary)/2pi;  C2  T(winding 2, same entry)/2pi;  C3  int Tr B (elem) / int Tr B (composite) = 1/3;
  C4  T(composite) = 3 T(elementary);  C5/C6  moduli inertia I = E_rot / (pi omega^2) at n = (1,1,0)/sqrt 2.
  Descriptive: tail decay lengths (scalar: 1 - |det H|; magnetic: Tr B), against bulk masses lam and 1.
Primary lattice: half-width 20, h = 0.125 (L = 320).  Convergence at lam = 1 (C1, and I): h = 0.25, 0.125,
0.0625 at half-width 20; h = 0.125 at half-width 30.
Run: python3 b2_run.py > log_b2.txt  -> b2_results.json
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np, json, time, platform
import scipy
from scipy.optimize import minimize
from u3common import LAMBDAS, C1_TARGET, C2_TARGET, rot12, herm, G_DIAG
from u3radial import Radial
from u3lattice import Lattice2D, OPTS2D

HW, HPRIM = 20.0, 0.125
CONFIGS = {'elementary': (1, 0, 0), 'winding2': (2, 0, 0), 'composite': (1, 1, 1)}
OMEGAS = (0.01, 0.02, 0.05)


def radial(lam, N):
    R = Radial(lam, N=N, dr=0.05, rmax=30.0, relax_alpha=False)
    res = minimize(R.make_fg(0, 0), R.initial(), jac=True, method='L-BFGS-B',
                   options=dict(maxiter=50000, maxfun=100000, gtol=1e-10, ftol=1e-16, maxcor=20))
    o = R.observables(res.x, 0, 0)
    h, a, _ = R.profiles(res.x)
    return R, res, o, h, a


CKPT = '/tmp/claude-0/ckpt'


def lattice_solve(lam, N, hprof, aprof, rgrid, L, h, ckpt=None):
    """ckpt: checkpoint name (used only by the resumed convergence runs after container restarts): x is saved
    every 5 iterations and a restarted solve continues from it (L-BFGS memory is lost; same minimum)."""
    Lt = Lattice2D(lam, L=L, h=h)
    v0 = Lt.from_radial(hprof, aprof, rgrid, N)
    t = time.time()
    cb = None; restarts = 0
    if ckpt:
        os.makedirs(CKPT, exist_ok=True); f = os.path.join(CKPT, ckpt + '.npy'); fm = os.path.join(CKPT, ckpt + '.meta')
        if os.path.exists(f):
            v0 = np.load(f); restarts = int(open(fm).read()) + 1 if os.path.exists(fm) else 1
            open(fm, 'w').write(str(restarts))
        it = [0]

        def cb(x):
            it[0] += 1
            if it[0] % 5 == 0:
                np.save(f + '.tmp.npy', x); os.replace(f + '.tmp.npy', f)
    res = minimize(Lt.T_fg, v0, jac=True, method='L-BFGS-B', options=OPTS2D, callback=cb)
    o = Lt.observables(res.x)
    o.update(success=bool(res.success), message=str(res.message), nit=int(res.nit),
             grad_max=float(np.max(np.abs(res.jac))), seconds=time.time() - t, L=L, h=h, half_width=L * h / 2,
             T_over_2pi=o['T'] / (2 * np.pi), checkpoint_restarts=restarts)
    return Lt, res.x, o


def inertia_2d(Lt, v):
    """Rotate the converged elementary string to n = (1,1,0)/sqrt2 and solve the Gauss law at several omega."""
    V = rot12(np.pi / 4)
    v1 = Lt.rotate_global(v, V)
    H, Wp = Lt.unpack(v1)
    U, *_ = Lt.links(Wp)
    # check that the rotated string has the same static energy (global SU(3)_{C+F})
    Ek, Eb, Ev, *_ = Lt.T_parts(H, U)
    rows = []
    for om in OMEGAS:
        K, x, info = Lt.K_solve(H, U, G=G_DIAG, omega=om, tol=1e-12)
        rows.append(dict(omega=om, E_rot=K, E_rot_over_omega2=K / om ** 2, I=K / (np.pi * om ** 2), **info))
    w2 = np.array([r['omega'] ** 2 for r in rows]); y = np.array([r['I'] for r in rows])
    cfit = np.polyfit(w2, y, 1)
    # charge density radius and leak, descriptive
    _, _, _, _, dens = Lt.K_parts(H, U, herm(x), OMEGAS[-1])
    rq = float(np.sqrt(np.sum(dens * Lt.r ** 2) / dens.sum()))
    return dict(rows=rows, I_extrapolated=float(cfit[1]), slope_in_omega2=float(cfit[0]),
                T_rotated=float(Ek + Eb + Ev), r_charge_rms=rq)


def fit_decay(r, d, lo, hi):
    m = (r >= lo) & (r <= hi) & (np.abs(d) > 0)
    if m.sum() < 3:
        return float('nan')
    p = np.polyfit(r[m], np.log(np.abs(d[m]) * np.sqrt(r[m])), 1)
    return float(-p[0])


def decay_2d(Lt, v):
    H, Wp = Lt.unpack(v)
    U, *_ = Lt.links(Wp)
    L, h = Lt.L, Lt.h
    j = L // 2
    xs = Lt.x[:, j]; sel = xs > 0
    r = np.hypot(xs, Lt.y[0, j])[sel]
    ds = (1 - np.abs(np.linalg.det(H[:, j])))[sel]
    P = U[0, :-1, j - 1] @ U[1, 1:, j - 1] @ np.conj(np.swapaxes(U[0, :-1, j], -1, -2)) @ np.conj(np.swapaxes(U[1, :-1, j - 1], -1, -2))
    B = np.angle(np.linalg.det(P)) / h ** 2
    xc = Lt.x[:-1, j] + h / 2
    selb = xc > 0
    return dict(m_scalar=fit_decay(r, ds, 4.0, 9.0), m_magnetic=fit_decay(xc[selb], B[selb], 4.0, 9.0), window=[4.0, 9.0])


def decay_1d(R, h, a):
    r = R.r; ds = 1 - np.abs(np.linalg.det(h))
    b = np.real(np.diff(np.trace(a, axis1=1, axis2=2))) / R.dr / R.rm
    return dict(m_scalar=fit_decay(r, ds, 5.0, 12.0), m_magnetic=fit_decay(R.rm, b, 5.0, 12.0), window=[5.0, 12.0])


def convergence_resume():
    """Re-run the lam = 1 convergence entries missing from b2_results.json (used after the container restart,
    REPORT §7).  Starting profile: the same radial lam = 1 elementary solve as the main run (deterministic)."""
    out = json.load(open('b2_results.json'))
    R, _, _, hp, ap = radial(1.0, (1, 0, 0))
    # h = 0.0625 (L = 640) was started twice and dropped (about 5 L-BFGS iterations per 30 min under the B3 load,
    # killed by container restarts; REPORT §7).  Halving h once is covered by h = 0.25 -> 0.125.
    for (L, h) in ((160, 0.25), (480, 0.125)):
        key = f'L{L}_h{h}'
        if key in out['convergence']:
            continue
        Lt, v, ol = lattice_solve(1.0, (1, 0, 0), hp, ap, R.r, L, h, ckpt=key)
        ol['inertia_2d'] = inertia_2d(Lt, v)
        ol['note'] = 'computed in the resumed run after container restarts (checkpointed)'
        out['convergence'][key] = ol
        print(f'convergence lam=1: L={L} h={h} half-width={L * h / 2}: T/2pi={ol["T_over_2pi"]:.7f} ({ol["message"]}, nit={ol["nit"]}, '
              f'{ol["seconds"]:.0f} s); I={ol["inertia_2d"]["I_extrapolated"]:.6f}', flush=True)
        with open('b2_results.json', 'w') as fh:
            json.dump(out, fh, indent=1, default=float)
    print('convergence done', flush=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'convergence':
        convergence_resume(); sys.exit(0)
    t0 = time.time()
    print(f'Python {platform.python_version()}, NumPy {np.__version__}, SciPy {scipy.__version__}', flush=True)
    out = dict(meta=dict(label='Exploration', prereg='PREREG_B2B3.md §2', primary=dict(half_width=HW, h=HPRIM, L=int(2 * HW / HPRIM)),
                         minimizer=dict(method='L-BFGS-B', **OPTS2D), omegas=OMEGAS,
                         software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)),
               lambdas={}, convergence={})
    keep = {}
    for lam in LAMBDAS:
        ent = dict(radial={}, lattice={})
        for name, N in CONFIGS.items():
            R, res, o, hp, ap = radial(lam, N)
            ent['radial'][name] = dict(T_over_2pi=o['T'] / (2 * np.pi), flux_TrB=o['flux_TrB'], I_alpha_pi4=o['I'],
                                       success=bool(res.success), nit=int(res.nit), message=str(res.message))
            if name == 'elementary':
                ent['radial'][name]['I_over_pi'] = o['I'] / np.pi
                ent['radial'][name]['decay'] = decay_1d(R, hp, ap)
            Lt, v, ol = lattice_solve(lam, N, hp, ap, R.r, int(2 * HW / HPRIM), HPRIM)
            ent['lattice'][name] = ol
            print(f'lam={lam} {name}: lattice T/2pi={ol["T_over_2pi"]:.6f} flux={ol["flux_TrB"]:.8f} ({ol["message"]}, nit={ol["nit"]}, '
                  f'grad_max={ol["grad_max"]:.1e}, {ol["seconds"]:.0f} s); radial T/2pi={o["T"] / (2 * np.pi):.6f}', flush=True)
            if name == 'elementary':
                keep[lam] = (R, hp, ap)
                ent['inertia_2d'] = inertia_2d(Lt, v)
                ent['decay_2d'] = decay_2d(Lt, v)
                print(f'lam={lam} I (2D): ' + ', '.join(f'omega={r["omega"]}: E_rot/omega^2={r["E_rot_over_omega2"]:.6f}, I={r["I"]:.6f} '
                                                       f'(CG {r["cg_iters"]}, res {r["rel_res"]:.1e})' for r in ent['inertia_2d']['rows'])
                      + f'; extrapolated I={ent["inertia_2d"]["I_extrapolated"]:.6f}; radial I={o["I"] / np.pi:.6f}', flush=True)
                print(f'lam={lam} decay (2D): {ent["decay_2d"]}; (radial): {ent["radial"]["elementary"]["decay"]}', flush=True)
        le, lw, lc = ent['lattice']['elementary'], ent['lattice']['winding2'], ent['lattice']['composite']
        ent['checks'] = dict(
            C1=dict(value=le['T_over_2pi'], target=C1_TARGET[lam], rel_dev=le['T_over_2pi'] / C1_TARGET[lam] - 1),
            C2=dict(value=lw['T_over_2pi'], target=C2_TARGET[lam], rel_dev=lw['T_over_2pi'] / C2_TARGET[lam] - 1),
            C3=dict(value=le['flux_TrB'] / lc['flux_TrB'], target=1 / 3, abs_dev=le['flux_TrB'] / lc['flux_TrB'] - 1 / 3),
            C4=dict(value=lc['T'] / (3 * le['T']), target=1.0, rel_dev=lc['T'] / (3 * le['T']) - 1),
            C5C6=dict(I=ent['inertia_2d']['I_extrapolated'], target=1.0 if lam == 1.0 else None))
        print(f'lam={lam} checks: ' + json.dumps(ent['checks'], default=float), flush=True)
        out['lambdas'][str(lam)] = ent
        with open('b2_results.json', 'w') as fh:
            json.dump(out, fh, indent=1, default=float)
    # convergence at lam = 1
    R, hp, ap = keep[1.0]
    for (L, h) in ((160, 0.25), (640, 0.0625), (480, 0.125)):
        Lt, v, ol = lattice_solve(1.0, (1, 0, 0), hp, ap, R.r, L, h)
        ol['inertia_2d'] = inertia_2d(Lt, v)
        out['convergence'][f'L{L}_h{h}'] = ol
        print(f'convergence lam=1: L={L} h={h} half-width={L * h / 2}: T/2pi={ol["T_over_2pi"]:.7f} ({ol["message"]}, nit={ol["nit"]}, '
              f'{ol["seconds"]:.0f} s); I={ol["inertia_2d"]["I_extrapolated"]:.6f}', flush=True)
        with open('b2_results.json', 'w') as fh:
            json.dump(out, fh, indent=1, default=float)
    out['total_seconds'] = time.time() - t0
    with open('b2_results.json', 'w') as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f'total {out["total_seconds"]:.0f} s', flush=True)
