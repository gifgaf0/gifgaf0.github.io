"""
E10 Route B, B4 run driver (PREREG_B4 §3-§4).  Label: Exploration.

Runs (PREREG_B4 §4; n, Q, R0 from verify_results.json V1b sign change #66 and b4_straight.json):
  REG   regression (flat mode, b4_axi docstring): straight string of length 2 pi R_eq(3), core at (20, 0)
  M3a/M3b  n = 3, Q = Q3, R0 = R_eq3, 1.5 R_eq3       M5a/M5b  n = 5, Q = Q5, R0 = R_eq5, 1.5 R_eq5
  C-a n = 0, Q = 0, R0 = R_eq3   C-b n = 3, Q = 0, R0 = R_eq3   C-c n = 0, Q = Q3, R0 = R_eq3
  C-d n = 0, Q = Q3, no vortex (b4_axi.ball_start)   C-d5 the same at Q5
with R_eq = n/k*, Q = 2 pi (n/k*) q* (k*, q* exact from the JSON).  Ring starts: b4_axi.ring_start from the
re-solved straight string at (k*, q*) (b4_straight.py), orientation V = rot12(alpha*), then the twist dressing
Wt_phi initialised by b4_axi.Axi.twist_init (n != 0).
Minimiser: b4_lbfgs.lbfgs (plain L-BFGS; scipy's L-BFGS-B is too slow at n ~ 1e6), OPTS below (fixed before any loop run).  Observables every 50 iterations and at the end.
Checkpoint (fields + history) every 50 iterations; a restarted run continues from the checkpoint (L-BFGS memory
is lost at a restart; restarts are counted).
h = 0.125 re-relaxation ('fine'): the h = 0.25 end state interpolated onto the h = 0.125 lattice
(b4_run.refine), then relaxed with the same options.

Run:  python3 b4_run.py RUN [fine]        (-> b4_fields/<RUN>[_fine].npz, b4_hist/<RUN>[_fine].json)
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import sys, json, time, platform
import numpy as np
import scipy
from b4_lbfgs import lbfgs
from b4_axi import Axi, ring_start, ball_start, I3
from u3radial import Radial
from u3common import rot12

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, 'b4_fields'); HD = os.path.join(HERE, 'b4_hist')
os.makedirs(FD, exist_ok=True); os.makedirs(HD, exist_ok=True)
OPTS = dict(maxiter=20000, m=20, gtol=1e-6, ftol=1e-14, patience=5)
CG_TOL_RUN, CG_TOL_OBS = 1e-8, 1e-12
EVERY = 50


def params():
    v = json.load(open(os.path.join(HERE, 'verify_results.json')))['V1b']
    s = [s for s in v['sign_changes'] if s['index'] == 66][0]
    ks, qs = s['k_star'], s['q_star']
    st = json.load(open(os.path.join(HERE, 'b4_straight.json')))
    out = dict(k_star=ks, q_star=qs, r_q_star=s['r_q_star'], E_cal_star=st['star']['E'], alpha_star=st['star']['alpha'])
    for n in (3, 5):
        out[f'R_eq{n}'] = n / ks
        out[f'Q{n}'] = 2 * np.pi * (n / ks) * qs
    return out


def run_spec(name):
    p = params()
    R3, R5, Q3, Q5 = p['R_eq3'], p['R_eq5'], p['Q3'], p['Q5']
    spec = {'REG': dict(n=3, Q=Q3, R0=20.0, mode='flat', R_L=R3),
            'M3a': dict(n=3, Q=Q3, R0=R3), 'M3b': dict(n=3, Q=Q3, R0=1.5 * R3),
            'M5a': dict(n=5, Q=Q5, R0=R5), 'M5b': dict(n=5, Q=Q5, R0=1.5 * R5),
            'C-a': dict(n=0, Q=0.0, R0=R3), 'C-b': dict(n=3, Q=0.0, R0=R3), 'C-c': dict(n=0, Q=Q3, R0=R3),
            'C-d': dict(n=0, Q=Q3, R0=None), 'C-d5': dict(n=0, Q=Q5, R0=None)}[name]
    spec.setdefault('mode', 'ring'); spec.setdefault('R_L', None)
    return spec, p


def straight_profiles():
    z = np.load(os.path.join(HERE, 'b4_fields', 'straight', 'star_0_0.npz'))
    R = Radial(1.0, dr=0.05, rmax=40.0, relax_alpha=True)
    h, a, alpha = R.profiles(z['x'])
    return h, a, alpha, R.r


def make(name, h):
    spec, p = run_spec(name)
    A = Axi(lam=1.0, h=h, n=spec['n'], Q=spec['Q'], mode=spec['mode'], R_L=spec['R_L'], cg_tol=CG_TOL_RUN)
    return A, spec, p


def start(name, A, spec):
    if spec['R0'] is None:
        v = ball_start(A); info = dict(kind='ball', radius=4.0, profile='H = 1 - (1 - r^2/16)^2 m m^+, m = (1,1,0)/sqrt2')
    else:
        hp, ap, alpha, rg = straight_profiles()
        v, mm = ring_start(A, hp, ap, rg, spec['R0'], rot12(alpha))
        info = dict(kind='ring', R0=spec['R0'], alpha=alpha, dirichlet_mismatch=mm)
        if A.n != 0:
            v = A.twist_init(v); info['twist_init_cg'] = int(A.twist_init_cg)
    return v, info


def obs(A, v, it, t0):
    tol = A.cg_tol; A.cg_tol = CG_TOL_OBS
    o = A.observables(v)
    A.cg_tol = tol
    o.update(iter=int(it), nfev=int(A.nfev), cg_total=int(A.cg_total), seconds=time.time() - t0)
    return o


def refine(Ac, vc, Af):
    """h -> h/2: interpolate the coarse end state onto the fine lattice.  H, Wt_phi: bilinear in (rho, z) of
    the site values; W_rho, W_z: bilinear of the coarse link parameters at the fine link midpoints (W ~ gauge
    field, U = exp(i h W) with the new h); outside the coarse sample range: nearest (edge) value.  Dirichlet
    H = 1 kept.  The relaxation that follows removes the interpolation error."""
    from scipy.interpolate import RegularGridInterpolator as RGI
    H, Wr, Wz, Pt = Ac.unpack(vc)
    hc = Ac.h

    def interp(arr, r0, z0, rf, zf):
        sh = arr.shape[2:]; flat = arr.reshape(arr.shape[0], arr.shape[1], -1)
        rr = np.clip(rf, r0[0], r0[-1]); zz = np.clip(zf, z0[0], z0[-1])
        pts = np.stack([rr.ravel(), zz.ravel()], -1)
        out = np.empty((pts.shape[0], flat.shape[2]), flat.dtype)
        for c in range(flat.shape[2]):
            out[:, c] = RGI((r0, z0), flat[:, :, c])(pts)
        return out.reshape(rf.shape + sh)
    rs, zs = Ac.rho, Ac.z
    Hf = interp(H, rs, zs, Af.RHO, Af.Z); Hf[Af.bd] = I3
    Ptf = interp(Pt, rs, zs, Af.RHO, Af.Z)
    rl, zl = (rs[:-1] + rs[1:]) / 2, zs
    Wrf = interp(Wr, rl, zl, (Af.RHO[:-1] + Af.RHO[1:]) / 2, Af.Z[:-1])
    rl, zl = rs, (zs[:-1] + zs[1:]) / 2
    Wzf = interp(Wz, rl, zl, Af.RHO[:, :-1], (Af.Z[:, :-1] + Af.Z[:, 1:]) / 2)
    return Af.pack(Hf, Wrf, Wzf, Ptf)


def main(name, fine=False):
    tag = name + ('_fine' if fine else '')
    h = 0.125 if fine else 0.25
    A, spec, p = make(name, h)
    ck = os.path.join(FD, f'{tag}_ckpt.npz'); hf = os.path.join(HD, f'{tag}.json')
    final = os.path.join(FD, f'{tag}.npz')
    if os.path.exists(final):
        print(f'[{tag}] already done'); return
    t0 = time.time()
    ck32 = os.path.join(FD, 'ckpt32', f'{tag}_ckpt32.npz')
    if not os.path.exists(ck) and os.path.exists(ck32) and os.path.exists(hf):
        ck = ck32                      # committed float32 copy (container restart); the relaxation continues from it
    if os.path.exists(ck):
        z = np.load(ck); v = z['x'].astype(float); rec = json.load(open(hf))
        ck = os.path.join(FD, f'{tag}_ckpt.npz')
        rec['restarts'] = rec.get('restarts', 0) + 1
        it0 = rec['history'][-1]['iter']
        print(f'[{tag}] restart {rec["restarts"]} from checkpoint at iter {it0}', flush=True)
    else:
        if fine:
            Ac, _, _ = make(name, 0.25)
            vc = np.load(os.path.join(FD, f'{name}.npz'))['x']
            v = refine(Ac, vc, A); info = dict(kind='refined from h = 0.25 end state')
        else:
            v, info = start(name, A, spec)
        rec = dict(run=tag, spec=spec, h=h, params=p, start=info, opts=OPTS, cg_tol_run=CG_TOL_RUN,
                   cg_tol_obs=CG_TOL_OBS, restarts=0, history=[],
                   software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
                   lattice=dict(Nr=A.Nr, Nz=A.Nz, rho_sites=[float(A.rho[0]), float(A.rho[-1])],
                                z_sites=[float(A.z[0]), float(A.z[-1])], dirichlet='rho = rho[-1], z = z[0], z[-1]'))
        it0 = 0
        o = obs(A, v, 0, t0); rec['history'].append(o)
        print(f'[{tag}] start E={o["E"]:.6f} R_f={o["R_f"]} tau={o["tau"]} omega={o["omega"]}', flush=True)
    cnt = [it0]

    def cb(xk, f, g, it, nfev):
        cnt[0] += 1
        if os.path.exists(os.path.join(HERE, 'STOP_' + tag)):
            return True
        if cnt[0] % EVERY == 0:
            o = obs(A, xk, cnt[0], t0); rec['history'].append(o)
            np.savez(ck + '.tmp.npz', x=xk); os.replace(ck + '.tmp.npz', ck)
            json.dump(rec, open(hf + '.tmp', 'w'), default=float); os.replace(hf + '.tmp', hf)
            print(f'[{tag}] it={cnt[0]} E={o["E"]:.8f} R_f={o["R_f"]} nvort={o["n_vortex_plaquettes"]} '
                  f'R_q={o["R_q"]} r_q={o["r_q"]} w/m={o["omega_over_mbulk"]} tau={o["tau"]} leak={o["leak"]:.2e} '
                  f'cg/fev={A.cg_total / max(A.nfev, 1):.1f} {time.time() - t0:.0f}s', flush=True)
    opts = dict(OPTS); opts['maxiter'] = max(1, OPTS['maxiter'] - it0)
    res = lbfgs(A.fg, v, callback=cb, **opts)
    o = obs(A, res['x'], cnt[0], t0)
    o.update(final=True, message=res['message'], memory_resets=res['memory_resets'], success=bool(res['success']), nit_this_leg=int(res['nit']),
             grad_max=float(np.abs(res['jac']).max()))
    res = type('R', (), dict(x=res['x'], message=res['message']))
    rec['history'].append(o); rec['end'] = o
    np.savez_compressed(final, x=res.x)
    json.dump(rec, open(hf + '.tmp', 'w'), default=float); os.replace(hf + '.tmp', hf)
    for f in (ck, ck32):
        if os.path.exists(f):
            os.remove(f)
    print(f'[{tag}] END {res.message} it={cnt[0]} E={o["E"]:.8f} R_f={o["R_f"]} tau={o["tau"]} '
          f'w/m={o["omega_over_mbulk"]} leak={o["leak"]} {time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    main(sys.argv[1], fine=len(sys.argv) > 2 and sys.argv[2] == 'fine')
