#!/usr/bin/env python3
"""Cross-check E8: my own 3D relaxation of Hopf solitons in the box [-7.5,7.5]^3
with phi = e3 on (and outside) the boundary, using the FOURTH-order centred-difference
energy (xc_lib3d.C4Energy) and L-BFGS on an unconstrained field u, phi = u/|u|.
Grid spacings h = 15/(N-1) with N = 81, 97, 111 (h = 0.1875, 0.15625, 0.13636),
none of which was used by the original agent.  Initial data: Sutcliffe's rational
map ansatz, centre offset (0.04,-0.03,0.02); finer stages start from a tricubic
interpolation of the previous stage.  Checkpointed in chunks; resumable.

usage: python3 xc_relax3d.py Q1 [Q2 ...]
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
STAGES = {'Q1': [81, 97, 111], 'Q2': [81, 97, 111], 'Q4': [81, 97], 'Q7': [81, 97]}
CHUNK = 300


def load_res():
    return json.load(open(OUT)) if os.path.exists(OUT) else {}


def save_res(res):
    tmp = OUT + '.tmp'
    json.dump(res, open(tmp, 'w'), indent=1); os.replace(tmp, OUT)


def interp(phi_old, N):
    No = phi_old.shape[0]
    c = np.linspace(0, No - 1, N)
    I, J, K = np.meshgrid(c, c, c, indexing='ij')
    out = np.stack([map_coordinates(phi_old[..., q], [I, J, K], order=3, mode='nearest')
                    for q in range(3)], -1)
    out /= np.linalg.norm(out, axis=-1, keepdims=True)
    return out


def relax_stage(phi, N, tag, res, key, max_chunks=40, tol=2e-9):
    h = 2 * L / (N - 1)
    c4 = X.C4Energy(N)
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


def main(which):
    os.makedirs(SCR, exist_ok=True)
    res = load_res()
    for q in which:
        prev = None
        for N in STAGES[q]:
            key = f'{q}_N{N}'
            fn = os.path.join(SCR, f'{key}.npy')
            if key in res and res[key].get('done'):
                prev = np.load(fn)
                continue
            if os.path.exists(fn) and key in res:
                phi = np.load(fn)
            elif prev is None:
                phi = X.rational_map_field(N, L, *MAPS[q], offset=(0.04, -0.03, 0.02))
            else:
                phi = interp(prev, N)
                phi[0] = phi[-1] = phi[:, 0] = phi[:, -1] = phi[:, :, 0] = phi[:, :, -1] = [0, 0, 1]
            phi = relax_stage(phi, N, q, res, key)
            h = 2 * L / (N - 1)
            ent = res[key]
            ent['E_c4'] = X.energy_c4(phi, h)[0]
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
    main(sys.argv[1:] or ['Q1', 'Q2'])
