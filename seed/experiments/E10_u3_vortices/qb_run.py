"""
E10 Route B, QB run driver (PREREG_QB §1-§3).  Label: Exploration.

Instrument: B4's axisymmetric code (b4_axi.Axi) with n = 0 and no vortex, unchanged and imported; the same box
(rho in [0, 40], z in [-20, 20], Dirichlet vacuum edge), h = 0.25, the same minimiser (b4_lbfgs.lbfgs) with the
same options (b4_run.OPTS), the same CG tolerances (b4_run.CG_TOL_RUN, CG_TOL_OBS) and the same checkpoint cadence.
Starts: S1 = b4_axi.ball_start(A, R=4)  (B4's C-d start),  S2 = b4_axi.ball_start(A, R=8).
m_bulk = min(1, lam) (PREREG_B2B3 §1); Axi.observables already reports omega / min(1, lam).

Run tags:  L<lam>_Q<Q>_<S1|S2>          main grid (h = 0.25, B4 box)
           <tag>_box                    box check: end state embedded (vacuum padding) in rho in [0, 60], z in [-30, 30]
           <tag>_fine                   resolution check: end state refined to h = 0.125 (b4_run.refine), B4 box
Run:  python3 qb_run.py TAG            (-> qb_fields/<TAG>.npz, qb_hist/<TAG>.json; resumes from a checkpoint)
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import sys, json, time, platform
import numpy as np
import scipy
from b4_lbfgs import lbfgs
from b4_axi import Axi, ball_start, I3
from b4_run import OPTS, CG_TOL_RUN, CG_TOL_OBS, EVERY, refine
from u3common import herm

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, 'qb_fields'); HD = os.path.join(HERE, 'qb_hist')
os.makedirs(FD, exist_ok=True); os.makedirs(HD, exist_ok=True)

LAMS = [0.8, 0.9, 1.0, 1.1, 1.2]
QS = [200.0, 400.0, 800.0, 1626.5329, 2710.9]          # PREREG_QB §2, literal values
STARTS = {'S1': 4.0, 'S2': 8.0}
BOX0 = dict(rho_max=40.0, zhalf=20.0)
BOXL = dict(rho_max=60.0, zhalf=30.0)


def tag_of(lam, Q, s):
    return f'L{lam:.1f}_Q{Q!r}_{s}'


def parse(tag):
    parts = tag.split('_')
    lam = float(parts[0][1:]); Q = float(parts[1][1:]); s = parts[2]
    variant = parts[3] if len(parts) > 3 else None
    return lam, Q, s, variant


def all_main():
    return [tag_of(l, q, s) for l in LAMS for q in QS for s in STARTS]


def make(lam, Q, h=0.25, box=BOX0):
    return Axi(lam=lam, h=h, rho_max=box['rho_max'], zhalf=box['zhalf'], n=0, Q=Q, cg_tol=CG_TOL_RUN)


def embed(As, vs, Al):
    """Same h, larger box: copy the small-box state into the large lattice (rho indices equal, z offset), vacuum
    (H = 1, W = 0, Wt_phi = 0) elsewhere.  The small box's Dirichlet sites carry H = 1, consistent with vacuum."""
    H, Wr, Wz, Pt = As.unpack(vs)
    off = int(round((As.z[0] - Al.z[0]) / Al.h))
    assert abs(Al.z[off] - As.z[0]) < 1e-9 and abs(Al.rho[0] - As.rho[0]) < 1e-12
    Hl = Al.Hb.copy(); Wrl = np.zeros(Al.shapes['Wr']); Wzl = np.zeros(Al.shapes['Wz']); Ptl = np.zeros(Al.shapes['P'])
    Nr, Nz = As.Nr, As.Nz
    Hl[:Nr, off:off + Nz] = H
    Wrl[:Nr - 1, off:off + Nz] = Wr
    Wzl[:Nr, off:off + Nz - 1] = Wz
    Ptl[:Nr, off:off + Nz] = Pt
    Hl[Al.bd] = I3
    return Al.pack(Hl, Wrl, Wzl, Ptl)


def lump_obs(A, v):
    """QB extras (descriptive + verdict inputs): 3D charge rms radius about the origin, charge fractions within
    r < 5, 10, 15, radius of the |det H| < 0.7 region (max 3D distance of such sites from the origin; also its max rho
    and max |z|), |det H| at the site nearest the origin.  Charge density = the Gauss-law density at the solved X."""
    H, Wr, Wz, Pt = A.unpack(v); U, _ = A.links(Wr, Wz); P = A.Pfull(Pt)
    tol = A.cg_tol; A.cg_tol = CG_TOL_OBS
    I, xw, _ = A.K_solve(H, U, P, A.X)
    A.cg_tol = tol
    dens = np.zeros((A.Nr, A.Nz)); A.K_full(H, U, P, herm(xw), 1.0, grads=False, dens=dens)
    tot = dens.sum()
    r3 = np.hypot(A.RHO, A.Z)
    rms = float(np.sqrt(np.sum(dens * r3 ** 2) / tot))
    cum = [float(dens[r3 < R].sum() / tot) for R in (5, 10, 15)]
    ad = np.abs(np.linalg.det(H))
    low = ad < 0.7
    j0 = int(np.argmin(np.abs(A.z)))
    return dict(r_rms_3D=rms, charge_within_r5_r10_r15=cum,
                detH07_radius=float(r3[low].max()) if low.any() else 0.0,
                detH07_rho_max=float(A.RHO[low].max()) if low.any() else 0.0,
                detH07_absz_max=float(np.abs(A.Z[low]).max()) if low.any() else 0.0,
                detH07_nsites=int(low.sum()),
                detH_origin=float(ad[0, j0]), detH_min_abs=float(ad.min()))


def obs(A, v, it, t0, extra=False):
    tol = A.cg_tol; A.cg_tol = CG_TOL_OBS
    o = A.observables(v)
    A.cg_tol = tol
    o.pop('windings', None)
    o.update(iter=int(it), nfev=int(A.nfev), cg_total=int(A.cg_total), seconds=time.time() - t0)
    if extra:
        o.update(lump_obs(A, v))
    return o


def main(tag):
    lam, Q, s, variant = parse(tag)
    base = tag_of(lam, Q, s)
    h = 0.125 if variant == 'fine' else 0.25
    box = BOXL if variant == 'box' else BOX0
    A = make(lam, Q, h, box)
    ck = os.path.join(FD, f'{tag}_ckpt.npz'); hf = os.path.join(HD, f'{tag}.json')
    final = os.path.join(FD, f'{tag}.npz')
    if os.path.exists(final) and os.path.exists(hf) and 'end' in json.load(open(hf)):
        print(f'[{tag}] already done'); return
    t0 = time.time()
    ck32 = os.path.join(FD, 'ckpt32', f'{tag}_ckpt32.npz')
    if not os.path.exists(ck) and os.path.exists(ck32) and os.path.exists(hf):
        ck = ck32
    if os.path.exists(ck) and os.path.exists(hf):
        v = np.load(ck)['x'].astype(float); rec = json.load(open(hf))
        ck = os.path.join(FD, f'{tag}_ckpt.npz')
        rec['restarts'] = rec.get('restarts', 0) + 1
        it0 = rec['history'][-1]['iter']
        print(f'[{tag}] restart {rec["restarts"]} from checkpoint at iter {it0}', flush=True)
    else:
        if variant is None:
            v = ball_start(A, R=STARTS[s])
            info = dict(kind='ball', radius=STARTS[s], profile=f'H = 1 - (1 - r^2/R^2)^2 m m^+, m = (1,1,0)/sqrt2, R = {STARTS[s]}')
        else:
            As = make(lam, Q, 0.25, BOX0)
            vs = np.load(os.path.join(FD, f'{base}.npz'))['x']
            if variant == 'box':
                v = embed(As, vs, A); info = dict(kind='h = 0.25 end state embedded in the large box (vacuum padding)')
            else:
                v = refine(As, vs, A); info = dict(kind='refined from h = 0.25 end state (b4_run.refine)')
        rec = dict(run=tag, lam=lam, Q=Q, start_id=s, variant=variant, m_bulk=min(1.0, lam), h=h, box=box, n=0,
                   start=info, opts=OPTS, cg_tol_run=CG_TOL_RUN, cg_tol_obs=CG_TOL_OBS, restarts=0, history=[],
                   software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
                   lattice=dict(Nr=A.Nr, Nz=A.Nz, rho_sites=[float(A.rho[0]), float(A.rho[-1])],
                                z_sites=[float(A.z[0]), float(A.z[-1])]))
        it0 = 0
        o = obs(A, v, 0, t0); rec['history'].append(o)
        print(f'[{tag}] start E={o["E"]:.6f} omega/m={o["omega_over_mbulk"]} leak={o["leak"]:.2e}', flush=True)
    cnt = [it0]
    mQ = min(1.0, lam) * Q

    def cb(xk, f, g, it, nfev):
        cnt[0] += 1
        if os.path.exists(os.path.join(HERE, 'STOP_' + tag)):
            return True
        if cnt[0] % EVERY == 0:
            o = obs(A, xk, cnt[0], t0); rec['history'].append(o)
            np.savez(ck + '.tmp.npz', x=xk); os.replace(ck + '.tmp.npz', ck)
            json.dump(rec, open(hf + '.tmp', 'w'), default=float); os.replace(hf + '.tmp', hf)
            print(f'[{tag}] it={cnt[0]} E={o["E"]:.8f} E/mQ={o["E"] / mQ:.6f} r_q={o["r_q"]} '
                  f'w/m={o["omega_over_mbulk"]} leak={o["leak"]:.2e} {time.time() - t0:.0f}s', flush=True)
    opts = dict(OPTS); opts['maxiter'] = max(1, OPTS['maxiter'] - it0)
    res = lbfgs(A.fg, v, callback=cb, **opts)
    o = obs(A, res['x'], cnt[0], t0, extra=True)
    o.update(final=True, message=res['message'], memory_resets=res['memory_resets'], success=bool(res['success']),
             nit_this_leg=int(res['nit']), grad_max=float(np.abs(res['jac']).max()), E_over_mQ=o['E'] / mQ)
    rec['history'].append(o); rec['end'] = o
    np.savez_compressed(final, x=res['x'])
    json.dump(rec, open(hf + '.tmp', 'w'), default=float); os.replace(hf + '.tmp', hf)
    for f in (ck, ck32):
        if os.path.exists(f):
            os.remove(f)
    print(f'[{tag}] END {res["message"]} it={cnt[0]} E={o["E"]:.8f} E/mQ={o["E"] / mQ:.6f} '
          f'w/m={o["omega_over_mbulk"]} leak={o["leak"]:.3e} rms3D={o["r_rms_3D"]:.3f} {time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'list':
        print('\n'.join(all_main()))
    else:
        main(sys.argv[1])
