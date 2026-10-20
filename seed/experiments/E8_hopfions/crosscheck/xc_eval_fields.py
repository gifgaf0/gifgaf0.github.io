#!/usr/bin/env python3
"""Cross-check E8: evaluate the ORIGINAL agent's relaxed field checkpoints with my
own, independently written tools (xc_lib3d.py):
  * E_lp : my implementation of the link/plaquette energy described in REPORT.md
           (should reproduce the reported energies if the description is right)
  * E_c2 : second-order centred-difference energy (REPORT.md's 'stencil' claim)
  * E_c4 : fourth-order centred-difference energy (near-continuum energy of the field)
  * Q_W  : Hopf charge, Whitehead integral, free-space Green function (zero padding)
  * curves (finest grid, and N=101): position curve phi=-e3, a framing curve
    phi=(sin a,0,-cos a) with a=0.6, and a far preimage phi=(sin 2,0,cos 2):
    components, Alexander polynomials (3 random projections), linking matrix,
    Q from linking, twists T_a = Lk(C_a, framing) - sum_b lk(C_a, C_b),
    planarity of each position loop, inertia of the (1-phi3) density.
Writes xc_fields.json (resumable, per-field cache).
"""
import json, os, sys, time
import numpy as np
import xc_lib3d as X

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'
OUT = os.path.join(HERE, 'xc_fields.json')
RUNS = ['Q1_A11', 'Q2_A21', 'Q3_A31', 'Q4_A22', 'Q5_K32', 'Q6_L22', 'Q7_K32']


def curve_analysis(phi, h, L, rng):
    pos, pr1 = X.preimage_curves(phi, h, L, [0, 0, -1])
    a = 0.6
    fr, pr2 = X.preimage_curves(phi, h, L, [np.sin(a), 0, -np.cos(a)])
    far, pr3 = X.preimage_curves(phi, h, L, [np.sin(2.0), 0, np.cos(2.0)])
    pos = [P for P in pos if len(P) >= 6]
    nP = len(pos)
    alex = []
    R = [X.random_rotation(rng) for _ in range(3)]
    for P in pos:
        alex.append([str(X.alexander(P, Ri)[0]) for Ri in R])
    lkm = [[0.0] * nP for _ in range(nP)]
    for i in range(nP):
        for j in range(i + 1, nP):
            lkm[i][j] = lkm[j][i] = X.linking_number(pos[i], pos[j])
    lk_far = [sum(X.linking_number(P, F) for F in far) for P in pos]
    lk_fr = [sum(X.linking_number(P, F) for F in fr) for P in pos]
    twists = [lk_fr[i] - sum(lkm[i][j] for j in range(nP) if j != i) for i in range(nP)]
    shapes = []
    for P in pos:
        c = P.mean(0); Y = P - c
        w, V = np.linalg.eigh(Y.T @ Y / len(Y))
        nrm = V[:, 0]
        rad = np.linalg.norm(Y - np.outer(Y @ nrm, nrm), axis=1)
        seg = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1).sum()
        shapes.append(dict(centre=c.round(3).tolist(), normal=nrm.round(3).tolist(),
                           mean_radius=float(rad.mean()),
                           out_of_plane_rms_over_radius=float(np.sqrt(np.mean((Y @ nrm) ** 2)) / rad.mean()),
                           radius_std_over_mean=float(rad.std() / rad.mean()), length=float(seg),
                           npts=len(P)))
    return dict(n_position=nP, n_framing=len(fr), n_far=len(far), tracing_problems=[pr1, pr2, pr3],
                alexander=alex, lk_position_matrix=lkm, Q_link_far=float(sum(lk_far)),
                lk_far_per_component=lk_far, Q_link_framing=float(sum(lk_fr)),
                twists=twists, shapes=shapes)


def inertia(phi, h, L):
    N = phi.shape[0]
    x = np.linspace(-L, L, N)
    w = 1 - phi[..., 2]
    Xg, Yg, Zg = np.meshgrid(x, x, x, indexing='ij', sparse=True)
    m = w.sum()
    c = np.array([(w * Xg).sum(), (w * Yg).sum(), (w * Zg).sum()]) / m
    Xs, Ys, Zs = Xg - c[0], Yg - c[1], Zg - c[2]
    I = np.empty((3, 3))
    comps = [Xs, Ys, Zs]
    for i in range(3):
        for j in range(3):
            I[i, j] = (w * comps[i] * comps[j]).sum() / m
    ev = np.sort(np.linalg.eigvalsh(I))
    return dict(centre=c.round(4).tolist(), second_moments=ev.tolist(),
                asym_low=float((ev[1] - ev[0]) / ev[2]), asym_high=float((ev[2] - ev[1]) / ev[2]))


def main():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    rng = np.random.default_rng(11)
    jobs = []
    for run in RUNS:
        for N in (76, 101, 121, 151):
            jobs.append((run, N, 7.5))
    jobs += [('box_Q1_L10', 101, 10.0), ('box_Q2_L10', 101, 10.0)]
    for run, N, L in jobs:
        key = f'{run}_N{N}'
        fn = os.path.join(SRC, f'{key}.phi.npy')
        if not os.path.exists(fn):
            continue
        if key in res and res[key].get('done'):
            continue
        t0 = time.time()
        phi = np.ascontiguousarray(np.load(fn))
        h = 2 * L / (N - 1)
        nrm = np.linalg.norm(phi, axis=-1)
        bd = np.concatenate([phi[0].reshape(-1, 3), phi[-1].reshape(-1, 3), phi[:, 0].reshape(-1, 3),
                             phi[:, -1].reshape(-1, 3), phi[:, :, 0].reshape(-1, 3), phi[:, :, -1].reshape(-1, 3)])
        ent = dict(N=N, L=L, h=h, unit_norm_maxdev=float(np.abs(nrm - 1).max()),
                   boundary_max_dev_from_e3=float(np.abs(bd - [0, 0, 1]).max()))
        ent['E_lp'], ent['E2_lp'], ent['E4_lp'] = X.energy_lp(phi, h)
        ent['E_c2'], ent['E2_c2'], ent['E4_c2'] = X.energy_c2(phi, h)
        ent['E_c4'], ent['E2_c4'], ent['E4_c4'] = X.energy_c4(phi, h)
        ent['Q_whitehead_freespace'] = X.hopf_whitehead(phi, h)
        ent['inertia_1mphi3'] = inertia(phi, h, L)
        ent['min_phi3'] = float(phi[..., 2].min())
        if N in (101, 151) or run.startswith('box'):
            ent['curves'] = curve_analysis(phi, h, L, rng)
        ent['secs'] = time.time() - t0
        ent['done'] = True
        res[key] = ent
        print(key, {k: v for k, v in ent.items() if k not in ('curves',)}, flush=True)
        if 'curves' in ent:
            c = ent['curves']
            print('   curves:', c['n_position'], c['alexander'], 'lk', c['lk_position_matrix'],
                  'Qlink', round(c['Q_link_far'], 3), round(c['Q_link_framing'], 3),
                  'tw', [round(t, 2) for t in c['twists']], 'probs', c['tracing_problems'],
                  [(round(s['mean_radius'], 3), round(s['out_of_plane_rms_over_radius'], 3), round(s['length'], 2))
                   for s in c['shapes']], flush=True)
        json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
