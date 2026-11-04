"""
E10 Amendment A §A.3, run V2: full 2D lattice (u3lattice.Lattice2D, unchanged) at the two bracketing grid points
of the V1c sign change.  Half-width 30, h = 0.125 (L = 480), lam = 1.  Label: Exploration, post-hoc verification.

- Orientation alpha fixed at the radial (V1b) solution's value at that (k, q): the 2D Dirichlet edge pins it
  (as b3_compare2d.py, REPORT ambiguity (c)); the 2D fields are otherwise free (all H, all links).
- Warm start: the original radial solution (dr = 0.1, r_max = 20) padded with vacuum to r = 45 (> box corner
  30*sqrt2), mapped onto the lattice by Lattice2D.from_radial with V = rot12(alpha).
- E(k, q) = T + k^2 I + q^2/(4I) with the inner CG Gauss-law solve (Lattice2D.make_fg), L-BFGS-B OPTS2D.
- Recorded: E, T, I_q, omega/m, leak (fraction of the unit kinetic density with distance to the box edge < 4),
  charge rms radius, alpha, T-cal.  T-cal: envelope value T - (k^2 + omega^2) I_q (exact at the minimiser), and the
  finite-difference stencil if the stencil neighbours were also solved ('stencil' stage).
- Checkpoint every 5 L-BFGS iterations (container restarts).

Run:  python3 verify_v2.py solve            (the two bracketing points, 2 workers)
      python3 verify_v2.py stencil          (their T-cal stencil neighbours, optional)
      python3 verify_v2.py analyse          (-> verify_V2.json)
      V2_FINALIZE=1 python3 verify_v2.py solve   (stop an unfinished solve: evaluate at the last checkpoint, 1 L-BFGS step)
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import sys, json, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import minimize
import b3_scan as B
import verify_common as V
from u3common import rot12
from u3radial import Radial
from u3lattice import Lattice2D, OPTS2D

L2D, H2D = 480, 0.125
CK = os.path.join(V.FIELDS, 'V2_ckpt')


def selection():
    sel = json.load(open(os.path.join(V.HERE, 'verify_V1b.json')))['V1c_selection']
    return [V.ij_of(kq) for kq in sel['between']], sel


def alpha_V1b(ij):
    return V.load('V1b', *ij)[0]['alpha']


def solve2d(ij):
    i, j = ij
    out_f = os.path.join(V.WIP, 'V2', f'{i}_{j}.json')
    if os.path.exists(out_f):
        return json.load(open(out_f))
    os.makedirs(os.path.dirname(out_f), exist_ok=True); os.makedirs(CK, exist_ok=True)
    k, q = i * B.DK, j * B.DQ
    alpha = alpha_V1b(ij) if V.load('V1b', *ij) is not None else None
    if alpha is None:   # stencil neighbour not in V1b: use the nearest bracketing point's alpha
        alpha = alpha_V1b(selection()[0][0])
    Ro = V.radial('orig')
    Rp = Radial(V.LAM, dr=0.1, rmax=45.0, relax_alpha=True)
    xp = V.pad(Ro, V.load('orig', i, j)[1], Rp)
    h, a, _ = Rp.profiles(xp)
    Lt = Lattice2D(V.LAM, L=L2D, h=H2D)
    v0 = Lt.from_radial(h, a, Rp.r, (1, 0, 0), V=rot12(alpha))
    fg, st = Lt.make_fg(k, q)
    ck = os.path.join(CK, f'{i}_{j}.npy'); resumed = 0
    if os.path.exists(ck):
        v0 = np.load(ck); resumed = 1
    it = [0]; t = time.time()

    def cb(x):
        it[0] += 1
        if it[0] % 5 == 0:
            np.save(ck + '.tmp.npy', x); os.replace(ck + '.tmp.npy', ck)
            print(f'[V2 {k:.2f},{q:.1f}] iter {it[0]} E={st.get("E_last", float("nan"))} {time.time() - t:.0f}s', flush=True)
    fg0 = fg

    def fgl(v):
        E, g = fg0(v); st['E_last'] = E; return E, g
    opts = OPTS2D if not os.environ.get('V2_FINALIZE') else dict(OPTS2D, maxiter=1)
    res = minimize(fgl, v0, jac=True, method='L-BFGS-B', options=opts, callback=cb)
    np.save(ck, res.x)
    H, Wp = Lt.unpack(res.x)
    U, *_ = Lt.links(Wp)
    Ek, Eb, Ev, *_ = Lt.T_parts(H, U)
    I, xw, info = Lt.K_solve(H, U, x0=st.get('w'))
    _, _, _, _, dens = Lt.K_parts(H, U, __import__('u3common').herm(xw), 1.0)
    T = Ek + Eb + Ev; omega = q / (2 * I)
    E = T + k * k * I + q * q / (4 * I)
    tot = dens.sum()
    o = dict(i=i, j=j, k=k, q=q, E=float(E), T=float(T), I_q=float(I), omega_over_mbulk=float(omega), alpha=float(alpha),
             leak=float(dens[Lt.edge_dist < 4.0].sum() / tot), r_charge_rms=float(np.sqrt(np.sum(dens * Lt.r ** 2) / tot)),
             Tcal_envelope=float(T - (k * k + omega * omega) * I), success=bool(res.success), message=str(res.message),
             nit=int(res.nit), grad_max=float(np.max(np.abs(res.jac))), cg=info, seconds=time.time() - t,
             resumed_from_checkpoint=resumed, finalized_from_checkpoint=bool(os.environ.get('V2_FINALIZE')), L=L2D, h=H2D, half_width=L2D * H2D / 2,
             max_abs_detH_minus_rot90=float(np.max(np.abs(np.abs(np.linalg.det(H)) - np.rot90(np.abs(np.linalg.det(H)))))))
    json.dump(o, open(out_f, 'w'), indent=1, default=float)
    print(f'[V2] ({k:.2f},{q:.1f}) E={E:.8f} T={T:.8f} I={I:.6f} w/m={omega:.6f} leak={o["leak"]:.1e} '
          f'rq={o["r_charge_rms"]:.4f} Tenv={o["Tcal_envelope"]:.5f} {res.message} nit={res.nit} {o["seconds"]:.0f}s', flush=True)
    return o


def stencil_pts():
    br, _ = selection()
    win = {ij: o for ij, o in V.orig_records().items() if o['in_window']}
    s = set()
    for ij in br:
        s |= set(V.stencil_points(win, ij))
    return sorted(s - set(br))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'solve':
        br, sel = selection()
        print('V2 points:', br, sel, flush=True)
        with Pool(2) as pool:
            list(pool.imap_unordered(solve2d, br))
    elif cmd == 'stencil':
        pts = stencil_pts(); print('V2 stencil neighbours:', pts, flush=True)
        with Pool(int(os.environ.get('VERIFY_WORKERS', 4))) as pool:
            list(pool.imap_unordered(solve2d, pts))
    elif cmd == 'analyse':
        br, sel = selection()
        pts = {}
        for f in os.listdir(os.path.join(V.WIP, 'V2')):
            o = json.load(open(os.path.join(V.WIP, 'V2', f))); pts[(o['i'], o['j'])] = o
        win = {ij: dict(E=o['E']) for ij, o in pts.items() if o['omega_over_mbulk'] < 1 and o['leak'] < B.LEAK_MAX}
        rows = []
        for ij in br:
            o = pts[ij]; r1b = V.load('V1b', *ij)[0]
            T_fd = B.tcal(win, *ij) if all(nb in win for nb in V.stencil_points(
                {x: 1 for x, oo in V.orig_records().items() if oo['in_window']}, ij)) else None
            v1b = json.load(open(os.path.join(V.HERE, 'verify_V1b.json')))
            v1b_row = [p for p in v1b['points'] if (p['i'], p['j']) == ij][0]
            rows.append(dict(point=o, Tcal_fd_2d=None if T_fd is None else T_fd[0], Tcal_fd_2d_flags=None if T_fd is None else T_fd[3],
                             V1b=dict(E=r1b['E'], Tcal=v1b_row['Tcal'], Tcal_envelope=v1b_row['Tcal_envelope'], I_q=r1b['I'],
                                      T=r1b['T'], alpha=r1b['alpha']),
                             rel_dE_vs_V1b=o['E'] / r1b['E'] - 1))
        json.dump(dict(selection=sel, bracket=rows, all_points=list(pts.values())), open(os.path.join(V.HERE, 'verify_V2.json'), 'w'),
                  indent=1, default=float)
        for r in rows:
            print(r['point']['k'], r['point']['q'], 'rel dE vs V1b', r['rel_dE_vs_V1b'], 'Tenv 2D', r['point']['Tcal_envelope'],
                  'Tfd 2D', r['Tcal_fd_2d'], 'V1b Tcal', r['V1b']['Tcal'], flush=True)
