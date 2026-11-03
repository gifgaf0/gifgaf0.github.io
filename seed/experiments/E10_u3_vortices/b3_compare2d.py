"""
E10 Route B, B3: validation of the radial reduction against the full 2D lattice functional at one point.

Point: lam = 1, k = 0.2, q = 3.0, orientation fixed at alpha = pi/4 (n = (1,1,0)/sqrt2).  The 2D box has
Dirichlet H on its edge, which pins the orientation; the radial run therefore also fixes alpha = pi/4 (flagged).
The 2D fields are free to break the radial (equivariant) symmetry.
2D: E(k, q) = T + k^2 I + q^2/(4I) minimised over all H, W with an inner CG Gauss-law solve at every evaluation
(u3lattice.Lattice2D.make_fg), at h = 0.25 (L = 160) and h = 0.125 (L = 320), half-width 20; O(h^2) Richardson
extrapolation.  Radial: dr = 0.1 (the scan's grid) and dr = 0.05, rmax = 20.
Also: 2D full-functional gradient check (5-point FD) at this (k, q) on a small lattice is in checks_lattice.py.
Run: python3 b3_compare2d.py > log_b3_compare2d.txt  -> b3_compare2d.json
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np, json, time
from scipy.optimize import minimize
from u3common import rot12
from u3radial import Radial
from u3lattice import Lattice2D, OPTS2D

LAM, K, Q, ALPHA = 1.0, 0.2, 3.0, np.pi / 4
out = dict(point=dict(lam=LAM, k=K, q=Q, alpha=ALPHA), radial={}, lattice={})
ROPTS = dict(maxiter=50000, maxfun=100000, gtol=1e-10, ftol=1e-15, maxcor=20)
prof = None
for dr in (0.1, 0.05):
    R = Radial(LAM, dr=dr, rmax=20.0, relax_alpha=False)
    r0 = minimize(R.make_fg(0, 0), R.initial(), jac=True, method='L-BFGS-B', options=ROPTS)
    r1 = minimize(R.make_fg(K, Q), r0.x, jac=True, method='L-BFGS-B', options=ROPTS)
    o = R.observables(r1.x, K, Q); o.update(success=bool(r1.success), message=str(r1.message), nit=int(r1.nit))
    o0 = R.observables(r0.x, 0, 0)
    o['T_static'] = o0['T']; o['I_static'] = o0['I']
    out['radial'][f'dr={dr}'] = o
    print(f'radial dr={dr}: E={o["E"]:.7f} T={o["T"]:.7f} I={o["I"]:.7f} omega={o["omega"]:.6f} (static T={o0["T"]:.7f}, I={o0["I"]:.7f}) {o["message"]}', flush=True)
    if dr == 0.05:
        h, a, _ = R.profiles(r1.x); prof = (h, a, R.r)

for (L, hh) in ((160, 0.25), (320, 0.125)):
    t = time.time()
    Lt = Lattice2D(LAM, L=L, h=hh)
    v0 = Lt.from_radial(prof[0], prof[1], prof[2], (1, 0, 0), V=rot12(ALPHA))
    fg, st = Lt.make_fg(K, Q)
    res = minimize(fg, v0, jac=True, method='L-BFGS-B', options=OPTS2D)
    H, Wp = Lt.unpack(res.x)
    U, *_ = Lt.links(Wp)
    Ek, Eb, Ev, *_ = Lt.T_parts(H, U)
    I, xw, info = Lt.K_solve(H, U, x0=st.get('w'))
    T = Ek + Eb + Ev
    E = T + K * K * I + Q * Q / (4 * I)
    # breaking of the radial symmetry: compare |det H| on the four half-axes (90-degree rotations)
    dh = np.abs(np.linalg.det(H)); asym = float(np.max(np.abs(dh - np.rot90(dh))))
    o = dict(E=float(E), T=float(T), I=float(I), omega=float(Q / (2 * I)), success=bool(res.success), message=str(res.message),
             nit=int(res.nit), grad_max=float(np.max(np.abs(res.jac))), cg=info, seconds=time.time() - t,
             max_abs_detH_minus_rot90=asym, L=L, h=hh)
    out['lattice'][f'h={hh}'] = o
    print(f'2D L={L} h={hh}: E={E:.7f} T={T:.7f} I={I:.7f} omega={o["omega"]:.6f} ({o["message"]}, nit={o["nit"]}, grad_max={o["grad_max"]:.1e}, '
          f'{o["seconds"]:.0f} s); max|det H - rot90| = {asym:.1e}', flush=True)
    with open('b3_compare2d.json', 'w') as fh:
        json.dump(out, fh, indent=1, default=float)

l1, l2 = out['lattice']['h=0.25'], out['lattice']['h=0.125']
rich = {q: (4 * l2[q] - l1[q]) / 3 for q in ('E', 'T', 'I')}
out['lattice']['richardson_h0'] = rich
for key in ('dr=0.1', 'dr=0.05'):
    r_ = out['radial'][key]
    out[f'rel_dev_{key}'] = {q: dict(vs_h0125=r_[q] / l2[q] - 1, vs_richardson=r_[q] / rich[q] - 1) for q in ('E', 'T', 'I')}
    print(f'radial {key} vs 2D: ' + json.dumps(out[f'rel_dev_{key}']), flush=True)
with open('b3_compare2d.json', 'w') as fh:
    json.dump(out, fh, indent=1, default=float)
