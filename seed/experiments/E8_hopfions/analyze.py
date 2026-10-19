"""
analyze.py -- post-processing of the E8 relaxation runs (reads runs/*.json and the field
checkpoints in the scratch directory), writes analysis_raw.json and runs/<run>_curves.npz.

For every stage field (every grid spacing) of every run:
  * energy (E, E2, E4, virial), Whitehead Hopf charge, lattice-hedgehog count, min phi3
    (taken from the relaxation summary, recomputed only for the field analysed below);
For the two finest fields of every run:
  * position curve phi = -e3 and linking curve phi = (sqrt(2mu-mu^2), 0, -1+mu), mu = 0.1,
    as oriented closed polygons; number of components; Alexander polynomial of every
    position component (3 random projections); linking matrix (3 projections);
    Q from linking numbers; twist (framing) of every position component;
  * planarity/circularity of each position loop; principal moments of the energy density;
    the degree of the field on half-planes bounded by the symmetry axis (slice degree m);
  * number of connected components of the tube phi3 < -1 + 0.2 (Sutcliffe's nu = 0.2).
Sign convention: the Whitehead integral in the standard orientation of R^3 gives
Q_W = -Q_Sutcliffe for Sutcliffe's ansatz (his map R^3 -> S^3, eq. 3.1, reverses
orientation); every Q and linking number below is multiplied by -1 so that it is
reported with Sutcliffe's sign.
Usage: NUMBA_NUM_THREADS=2 python3 analyze.py
"""
import glob
import json
import os
import time
import numpy as np
import fs_lib as fs
import analysis_lib as al

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'
MU = 0.1
LINK_TARGET = (np.sqrt(2 * MU - MU ** 2), 0.0, -1 + MU)
CACHE = os.path.join(HERE, 'runs', 'analysis_cache.json')


def tube_components(phi, nu=0.2):
    from scipy.ndimage import label
    lab, n = label(phi[..., 2] < -1 + nu)
    sizes = np.bincount(lab.ravel())[1:]
    return int(n), sorted(sizes.tolist(), reverse=True)


def analyse_field(phi, h, L):
    t0 = time.time()
    res = {}
    Q, nhh, _ = fs.hopf_charge(phi, h)
    res['Q'] = -Q
    res['hedgehogs'] = nhh
    res['minphi3'] = float(phi[..., 2].min())
    pos, pinfo = fs.preimage_curves(phi, h, L=L)
    lnk, linfo = fs.preimage_curves(phi, h, L=L, target=LINK_TARGET)
    res.update(pos_info=pinfo, link_info=linfo, n_position=len(pos), n_linking=len(lnk))
    res['alexander'] = [[str(fs.alexander_polynomial(c, seed=s)[0]) for s in (2, 3, 4)] for c in pos]
    allc = pos + lnk
    lks = [-fs.linking_matrix(allc, seed=s)[0] for s in (1, 5, 9)]
    Lk = lks[0]
    res['linking_consistent_3_projections'] = bool(all(np.allclose(Lk, x) for x in lks))
    npos = len(pos)
    res['lk_position_position'] = Lk[:npos, :npos].tolist()
    res['Q_from_linking'] = float(Lk[:npos, npos:].sum())
    # assign each linking-curve component to the nearest position component -> twist (framing)
    owner = []
    for d in lnk:
        dists = [np.min(np.linalg.norm(d[:, None, :] - c[None, :, :], axis=-1), axis=1).mean() for c in pos]
        owner.append(int(np.argmin(dists)) if pos else -1)
    res['twist_per_component'] = [float(sum(Lk[a, npos + b] for b in range(len(lnk)) if owner[b] == a)) for a in range(npos)]
    res['total_lk_per_component'] = [float(Lk[a, npos:].sum()) for a in range(npos)]
    res['loop_shapes'] = [al.loop_shape(c) for c in pos]
    c, ev, evec, tot = fs.energy_inertia(phi, h, L=L)
    res['energy_centre'] = c.tolist()
    res['inertia_eigs'] = ev.tolist()
    # the symmetry-axis candidate: the eigenvector whose eigenvalue is most distinct
    gaps = [abs(ev[0] - ev[1]) + abs(ev[0] - ev[2]), abs(ev[1] - ev[0]) + abs(ev[1] - ev[2]),
            abs(ev[2] - ev[0]) + abs(ev[2] - ev[1])]
    ia = int(np.argmax(gaps))
    others = [i for i in range(3) if i != ia]
    res['inertia_axial_asym'] = float(abs(ev[others[0]] - ev[others[1]]) / ev[ia])
    degs = al.slice_degree(phi, h, L, c, evec[:, ia], evec[:, others[0]], np.linspace(0, 2 * np.pi, 6, endpoint=False))
    res['slice_degrees'] = [round(-d['degree'], 4) for d in degs]
    res['slice_min_phi3_on_edges'] = min(d['min_phi3_on_edges'] for d in degs)
    res['tube_components'] = tube_components(phi)
    res['analysis_wall_s'] = time.time() - t0
    return res, pos, lnk


def classify(a):
    """Sutcliffe-type label from the analysis of one field.
    Axial configurations (two equal principal moments of the energy density, every position
    loop a planar circle, no linking between position loops) are labelled A_{n,m}, with m the
    degree of the field on a half-plane bounded by the symmetry axis and n = Q/m (A_{2,2}, for
    example, has two stacked, unlinked position circles).  Otherwise: one unknotted loop ->
    bent A~_{T,1} (T = twist); one knotted loop -> K32 if its Alexander polynomial is that of the
    trefoil; two loops -> L^{lk,lk}_{T1,T2}."""
    npos = a['n_position']
    alex = [x[0] for x in a['alexander']]
    alex_ok = all(len(set(x)) == 1 for x in a['alexander'])
    Q = round(a['Q'])
    sd = np.array(a['slice_degrees'])
    m = int(round(abs(np.median(sd))))
    m_integer = bool(np.all(np.abs(np.abs(sd) - m) < 0.05))
    axial = a['inertia_axial_asym'] < 0.01
    planar = all(sh['out_of_plane_rms_over_radius'] < 0.03 and sh['radius_std_over_mean'] < 0.03 for sh in a['loop_shapes'])
    unknots = all(x == '1' for x in alex) and alex_ok
    unlinked = np.allclose(np.array(a['lk_position_position']), 0)
    if npos >= 1 and axial and planar and unknots and unlinked and m >= 1 and m_integer and Q % m == 0:
        return f'A{Q // m},{m}', axial
    if npos == 1:
        if alex_ok and alex[0] != '1':
            return ('K32' if alex[0] == 't**2 - t + 1' else f'knot[{alex[0]}]'), axial
        T = round(a['twist_per_component'][0])
        return f'A~{T},1', axial
    if npos == 2:
        lk = round(abs(a['lk_position_position'][0][1]))
        T = sorted(round(t) for t in a['twist_per_component'])
        return f'L{lk}{lk}_{T[0]}{T[1]}', axial
    return f'{npos}-component', axial


def extrapolate(hs, Es):
    hs = np.asarray(hs, float); Es = np.asarray(Es, float)
    o = np.argsort(-hs); hs = hs[o]; Es = Es[o]
    out = {}
    if len(hs) >= 2:
        A = np.vstack([np.ones(2), hs[-2:] ** 2]).T
        out['E0_h2_two_finest'] = float(np.linalg.solve(A, Es[-2:])[0])
    if len(hs) >= 3:
        A = np.vstack([np.ones(3), hs[-3:] ** 2, hs[-3:] ** 4]).T
        out['E0_h2h4_three_finest'] = float(np.linalg.solve(A, Es[-3:])[0])
        A = np.vstack([np.ones(3), hs[-3:] ** 2]).T
        out['E0_h2_three_finest_lsq'] = float(np.linalg.lstsq(A, Es[-3:], rcond=None)[0][0])
    if len(hs) >= 4:
        A = np.vstack([np.ones_like(hs), hs ** 2, hs ** 4]).T
        out['E0_h2h4_all_lsq'] = float(np.linalg.lstsq(A, Es, rcond=None)[0][0])
    vals = list(out.values())
    if vals:
        out['E0_best'] = out.get('E0_h2h4_three_finest', out['E0_h2_two_finest'])
        out['E0_spread'] = float(max(vals) - min(vals)) if len(vals) > 1 else None
        out['hs'] = hs.tolist()
    return out


def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    runs = sorted(glob.glob(os.path.join(HERE, 'runs', '*.json')))
    results = dict(conventions=dict(
        energy='E = 1/(32 sqrt2 pi^2) Int [ d_i phi.d_i phi + 1/2 (d_i phi x d_j phi)^2 ] d^3x (Sutcliffe 2007); Ward conjecture E >= Q^{3/4}; proven E >= (3/16)^{3/8} Q^{3/4}',
        lattice='forward-difference links (sigma term) + 4-corner plaquette average (Skyrme term), exact discrete gradient, field fixed to e3 on the boundary of [-L,L]^3',
        hopf='Q = -(1/16 pi^2) Int A.B, B_i = 1/2 eps_ijk phi.(d_j phi x d_k phi) from plaquette solid angles, curl A = B by FFT (Coulomb gauge); sign chosen so that Sutcliffe\'s ansatz W = Z1^n/Z0^m has Q = +nm',
        curves='position curve phi = -e3; linking curve phi = (sqrt(2mu-mu^2),0,-1+mu), mu = 0.1; tube phi3 < -0.8'),
        runs={})
    for rpath in runs:
        if os.path.basename(rpath).startswith('analysis'):
            continue
        R = json.load(open(rpath))
        if 'stages' not in R:
            continue
        name = R['run']
        Qn = fs.MAPS[R['map']][0]
        stages = sorted(R['stages'], key=lambda s: -s['h'])
        entry = dict(map=R['map'], Q_nominal=Qn, Lf=R['Lf'], L=R['L'], offset=R['offset'], initial=R.get('initial'),
                     stages=[dict(N=s['N'], h=s['h'], L=s['L'], E=s['E'], E2=s['E2'], E4=s['E4'],
                                  virial=(s['E2'] - s['E4']) / s['E'], Q=-s['Q'], hedgehogs=s['hedgehogs'],
                                  minphi3=s['minphi3'], t=s['t'], converged=s['converged'], wall_s=s['wall_s'],
                                  Frms=(s.get('last') or {}).get('Frms'), dt=(s.get('last') or {}).get('dt'))
                             for s in stages])
        entry['extrapolation'] = extrapolate([s['h'] for s in stages], [s['E'] for s in stages])
        entry['field_analysis'] = {}
        for k, st in enumerate(stages[-2:][::-1]):      # finest first
            ck = os.path.join(SCRATCH, f"{name}_N{st['N']}.phi.npy")
            if not os.path.exists(ck):
                continue
            key = f"{name}_N{st['N']}"
            mt = os.path.getmtime(ck)
            if key in cache and abs(cache[key]['mtime'] - mt) < 1e-6 and (k > 0 or os.path.exists(os.path.join(HERE, 'runs', f'{name}_curves.npz'))):
                a = cache[key]['a']
            else:
                phi = np.load(ck)
                a, pos, lnk = analyse_field(phi, st['h'], R['L'])
                cache[key] = dict(mtime=mt, a=a)
                json.dump(cache, open(CACHE, 'w'), default=float)
                if k == 0:
                    np.savez_compressed(os.path.join(HERE, 'runs', f'{name}_curves.npz'),
                                        **{f'pos{i}': p for i, p in enumerate(pos)}, **{f'lnk{i}': p for i, p in enumerate(lnk)})
            a['type'], a['axial'] = classify(a)
            entry['field_analysis'][str(st['N'])] = a
        results['runs'][name] = entry
        print(name, 'E(h):', [(round(s['h'], 4), round(s['E'], 5), round(-s['Q'], 4), s['converged']) for s in stages],
              'extrap', entry['extrapolation'].get('E0_best'))
        for N, a in entry['field_analysis'].items():
            print(f"   N={N}: type {a['type']} | comps {a['n_position']} alex {a['alexander']} lk {a['lk_position_position']} "
                  f"Q_link {a['Q_from_linking']} twist {a['twist_per_component']} slice m {a['slice_degrees']} "
                  f"asym {a['inertia_axial_asym']:.4f} tube {a['tube_components'][0]} Q {a['Q']:.4f}")
    json.dump(results, open(os.path.join(HERE, 'analysis_raw.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
