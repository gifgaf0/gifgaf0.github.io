#!/usr/bin/env python3
"""Cross-check E8: the axial A_{2,2} (Q = 4) soliton with the spectral axial code.

Starting the A_{2,2} directly from the rational map W = Z1^2/Z0^2 made L-BFGS wander
into configurations where the interpolant u passes through zero (degree not
conserved in the u/|u| representation).  Here the initial field is instead the square
W -> W^2 of my converged A_{2,1} solution (n = 2, deg psi = 1 -> 2), which is smooth.
The degree is monitored and reported.  Writes xc_axial_a22.json.
"""
import json, os, sys
import numpy as np
import xc_axial_spectral as A

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'xc_axial_a22.json')


def square_psi(psi):
    a_mag = np.sqrt(np.clip((1 - psi[..., 2]) / 2, 0, 1))
    b = np.sqrt(np.clip((1 + psi[..., 2]) / 2, 0, 1))
    ph = np.arctan2(psi[..., 1], psi[..., 0])
    a = a_mag * np.exp(1j * ph)
    p, q = a ** 2, b ** 2 + 0j
    den = np.abs(p) ** 2 + np.abs(q) ** 2
    w = 2 * p * np.conj(q) / den
    return np.stack([w.real, w.imag, (np.abs(q) ** 2 - np.abs(p) ** 2) / den], -1)


def eval_inf_solution(u, Ns, Lmap, rho, z):
    r = np.hypot(rho, z)
    xc = (r - Lmap) / (r + Lmap)
    xc = np.where(np.isfinite(r), xc, 1.0)
    yc = 2 * np.arccos(np.clip(z / np.maximum(r, 1e-300), -1, 1)) / np.pi - 1
    Px = A.bary_matrix(Ns, xc.ravel()); Py = A.bary_matrix(Ns, yc.ravel())
    psi = np.stack([np.sum((Px @ u[:, :, c]) * Py, axis=1) for c in range(3)], -1)
    psi /= np.linalg.norm(psi, axis=1, keepdims=True)
    return psi.reshape(rho.shape + (3,))


CASES = [dict(name='n2m2_inf', kind='inf', L=2.0, Ns=[48, 64, 80, 96]),
         dict(name='n2m2_cyl7.5', kind='cyl', R=7.5, alpha=2.5, Ns=[64, 80, 96, 112]),
         dict(name='n2m2_cyl12.0', kind='cyl', R=12.0, alpha=3.2, Ns=[64, 80, 96, 112])]


def main():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    u21 = np.load(os.path.join(A.FDIR, 'n2m1_inf_N64.npy'))
    only = sys.argv[1:]
    for cs in CASES:
        if only and cs['name'] not in only:
            continue
        if cs['name'] in res and res[cs['name']].get('done'):
            continue
        print('case', cs['name'], flush=True)
        entry = {'runs': {}, 'init': 'square of n2m1_inf_N64'}
        u = None; Np = None
        for N in cs['Ns']:
            G = A.Geometry(cs['kind'], N, N, L=cs.get('L', 2.0), R=cs.get('R', 7.5), alpha=cs.get('alpha', 2.5))
            if u is None:
                rho = np.where(np.isfinite(G.node_rho), G.node_rho, 1e300)
                zz = np.where(np.isfinite(G.node_z), G.node_z, 0.0)
                u0 = square_psi(eval_inf_solution(u21, 64, 2.0, rho, zz))
            else:
                u0 = A.interp_nodes(u, Np, Np, N, N)
            u0 = A.set_boundary(u0, G)
            print('  initial', A.energy_grad(G, u0, 2, parts=True), flush=True)
            u, info = A.minimise(G, u0, 2, maxiter=40000, tag=cs['name'])
            entry['runs'][str(N)] = info
            Np = N
            res[cs['name']] = entry
            json.dump(res, open(OUT, 'w'), indent=1)
            np.save(os.path.join(A.FDIR, f"{cs['name']}_N{N}.npy"), u)
        entry['done'] = True
        res[cs['name']] = entry
        json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
