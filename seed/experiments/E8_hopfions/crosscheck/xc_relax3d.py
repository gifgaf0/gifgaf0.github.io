#!/usr/bin/env python3
"""Cross-check E8: my own 3D relaxation of Hopf solitons in the box [-7.5,7.5]^3
with phi = e3 on the boundary, L-BFGS on an unconstrained field u, phi = u/|u|.
Energy (first argument): 'R4' = (4 E_lp(h) - E_lp(2h))/3, a fourth-order scheme built
from link/plaquette energies (no centred-stencil null modes), or 'lp' = the
second-order link/plaquette scheme described in the original REPORT.md (my own code).
NOTE: the 4th-order CENTRED energy (C4Energy) is NOT usable for relaxation: from the
relaxed axial Q=1 start at h=0.1875 L-BFGS unwound it to E=0.135 within 300 iterations
(grid-scale modes are free for centred stencils).
Grid spacings h = 15/(N-1) with N = 81, 97, 111 (h = 0.1875, 0.15625, 0.13636),
none of which was used by the original agent.  Initial data: my own infinite-volume
axial solution (xc_axial_spectral.py) embedded in 3D, centre offset (0.04,-0.03,0.02),
truncated to e3 outside the box.  (Centred stencils are blind to the grid-scale
mode, so a far-from-minimal start such as the wide rational-map ansatz can unwind
through the lattice at coarse h; a test at h = 0.3 did exactly that.)  Finer stages
start from a tricubic interpolation of the previous stage.  Checkpointed; resumable.

usage: python3 xc_relax3d.py R4|lp Q1 [Q2 ...]
"""
import json, os, sys, time
import numpy as np
from scipy.optimize import minimize
from scipy.ndimage import map_coordinates
import xc_lib3d as X

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/xc_E8/relax'
OUT = os.path.join(HERE, 'xc_relax3d.json')
L = 7.5
MAPS = {'Q1': (lambda a, b: a, lambda a, b: b),
        'Q2': (lambda a, b: a ** 2, lambda a, b: b),
        'Q4': (lambda a, b: a ** 2, lambda a, b: b ** 2),
        'Q7': (lambda a, b: a ** 2 * b, lambda a, b: a ** 3 + b ** 2)}
STAGES = {'R4': {'Q1': [81, 97], 'Q2': [81], 'Q4': [81, 97], 'Q7': [81, 97]},
          'lp': {'Q1': [81, 111, 131], 'Q2': [81, 111, 131], 'Q4': [81, 111], 'Q7': [81, 111]}}
CHUNK = 300


def load_res():
    return json.load(open(OUT)) if os.path.exists(OUT) else {}


def save_res(res):
    tmp = OUT + '.tmp'
    json.dump(res, open(tmp, 'w'), indent=1); os.replace(tmp, OUT)


def axial_embed(N, name, n, offset=(0.04, -0.03, 0.02), Ns=64, Lmap=1.6):
    import xc_axial_spectral as A
    u = np.load(os.path.join(A.FDIR, f'{name}_N{Ns}.npy'))
    x = np.linspace(-L, L, N)
    Xg, Yg, Zg = np.meshgrid(x - offset[0], x - offset[1], x - offset[2], indexing='ij')
    rho = np.hypot(Xg, Yg).ravel(); z = Zg.ravel(); th = np.arctan2(Yg, Xg).ravel()
    r = np.hypot(rho, z)
    xc = (r - Lmap) / (r + Lmap)                      # inverse of r = L(1+x)/(1-x)
    yc = 2 * np.arccos(np.clip(z / np.maximum(r, 1e-300), -1, 1)) / np.pi - 1
    psi = np.empty((len(r), 3))
    for a in range(0, len(r), 100000):
        b = slice(a, a + 100000)
        Px = A.bary_matrix(Ns, xc[b]); Py = A.bary_matrix(Ns, yc[b])
        for c in range(3):
            psi[b, c] = np.sum((Px @ u[:, :, c]) * Py, axis=1)
    psi /= np.linalg.norm(psi, axis=1, keepdims=True)
    w = (psi[:, 0] + 1j * psi[:, 1]) * np.exp(1j * n * th)
    phi = np.stack([w.real, w.imag, psi[:, 2]], -1).reshape(N, N, N, 3)
    # smooth taper of phi_perp to zero at the box faces (the infinite-volume far
    # field is ~0.15 at the faces; a hard cut would leave a jump on the boundary)
    t1 = 1 - (np.abs(x) / L) ** 6
    T = t1[:, None, None] * t1[None, :, None] * t1[None, None, :]
    phi[..., 0] *= T; phi[..., 1] *= T
    phi /= np.linalg.norm(phi, axis=-1, keepdims=True)
    phi[0] = phi[-1] = phi[:, 0] = phi[:, -1] = phi[:, :, 0] = phi[:, :, -1] = [0, 0, 1]
    return phi


AXIAL_START = {'Q1': ('n1m1_inf', 1, 1.6), 'Q2': ('n2m1_inf', 2, 2.0)}


def interp(phi_old, N):
    No = phi_old.shape[0]
    c = np.linspace(0, No - 1, N)
    I, J, K = np.meshgrid(c, c, c, indexing='ij')
    out = np.stack([map_coordinates(phi_old[..., q], [I, J, K], order=3, mode='nearest')
                    for q in range(3)], -1)
    out /= np.linalg.norm(out, axis=-1, keepdims=True)
    return out


def relax_stage(phi, N, tag, res, key, kind='R4', max_chunks=8, tol=1e-8):
    h = 2 * L / (N - 1)
    c4 = X.LPEnergy(N, kind)
    sl = (slice(1, N - 1),) * 3
    u = phi.copy()
    shape = u[sl].shape

    def f(v):
        u[sl] = v.reshape(shape)
        nu = np.linalg.norm(u, axis=-1, keepdims=True)
        ph = u / nu
        E, E2, E4, g = c4(ph, h)
        gu = (g - ph * np.sum(ph * g, -1, keepdims=True)) / nu
        return E, gu[sl].ravel()

    hist = res.get(key, {}).get('hist', [])
    for ch in range(len(hist), max_chunks):
        t0 = time.time()
        r = minimize(f, u[sl].ravel(), jac=True, method='L-BFGS-B',
                     options=dict(maxiter=CHUNK, maxcor=8, ftol=1e-15, gtol=1e-12))
        u[sl] = r.x.reshape(shape)
        u /= np.linalg.norm(u, axis=-1, keepdims=True)
        E, E2, E4, g = c4(u, h)
        gt = g - u * np.sum(u * g, -1, keepdims=True)
        gnorm = float(np.sqrt(np.sum(gt[sl] ** 2)) / h ** 1.5)
        hist.append(dict(chunk=ch, E=E, E2=E2, E4=E4, gnorm=gnorm, nit=int(r.nit),
                         secs=time.time() - t0, msg=str(r.message)))
        np.save(os.path.join(SCR, f'{key}.npy'), u)
        res[key] = dict(N=N, h=h, hist=hist, done=False)
        save_res(res)
        print(f'{key} chunk {ch} E={E:.10f} E2={E2:.6f} E4={E4:.6f} |g|={gnorm:.3e} '
              f'nit={r.nit} {time.time()-t0:.0f}s', flush=True)
        if len(hist) >= 2:
            dE = abs(hist[-2]['E'] - hist[-1]['E']) / E
            if dE < tol or r.nit < CHUNK and dE < 1e-8:
                break
    return u


def main(kind, which):
    os.makedirs(SCR, exist_ok=True)
    res = load_res()
    for q in which:
        prev = None
        for N in STAGES[kind][q]:
            key = f'{kind}_{q}_N{N}'
            fn = os.path.join(SCR, f'{key}.npy')
            if key in res and res[key].get('done'):
                prev = np.load(fn)
                continue
            if os.path.exists(fn) and key in res:
                phi = np.load(fn)
            elif prev is None and q in AXIAL_START:
                nm, n, Lm = AXIAL_START[q]
                phi = axial_embed(N, nm, n, Lmap=Lm)
                res.setdefault('initial', {})[key] = dict(E_c4=X.energy_c4(phi, 2 * L / (N - 1))[0],
                                                          Q=X.hopf_whitehead(phi, 2 * L / (N - 1)))
                print('initial', key, res['initial'][key], flush=True)
            elif prev is None:
                phi = X.rational_map_field(N, L, *MAPS[q], offset=(0.04, -0.03, 0.02))
            else:
                phi = interp(prev, N)
                phi[0] = phi[-1] = phi[:, 0] = phi[:, -1] = phi[:, :, 0] = phi[:, :, -1] = [0, 0, 1]
            phi = relax_stage(phi, N, q, res, key, kind=kind, max_chunks=5 if prev is None else 3)
            h = 2 * L / (N - 1)
            ent = res[key]
            ent['E_c4'] = X.energy_c4(phi, h)[0]
            ent['E_R4'] = X.LPEnergy(N, 'R4')(phi, h)[0]
            ent['E_lp'] = X.energy_lp(phi, h)[0]
            ent['E_c2'] = X.energy_c2(phi, h)[0]
            ent['Q_whitehead'] = X.hopf_whitehead(phi, h)
            pos, pr = X.preimage_curves(phi, h, L, [0, 0, -1])
            far, pr2 = X.preimage_curves(phi, h, L, [np.sin(2.0), 0, np.cos(2.0)])
            ent['n_position'] = len(pos)
            ent['Q_link'] = float(sum(X.linking_number(P, F) for P in pos for F in far))
            rng = np.random.default_rng(7)
            ent['alexander'] = [[str(X.alexander(P, X.random_rotation(rng))[0]) for _ in range(3)] for P in pos]
            ent['done'] = True
            res[key] = ent
            save_res(res)
            print(key, 'final', {k: v for k, v in ent.items() if k != 'hist'}, flush=True)
            prev = phi


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:] or ['Q1', 'Q2'])
