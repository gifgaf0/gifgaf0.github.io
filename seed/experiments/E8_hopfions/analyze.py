"""
analyze.py -- post-processing of the E8 relaxation runs.

For every run in runs/*.json (and the fields saved in the scratch directory) it computes
  * energies at every grid spacing, the Hopf charge Q (Whitehead integral), lattice hedgehog
    count and min phi3;
  * the position curve phi = -e3 and the linking curve phi = (sqrt(2mu-mu^2), 0, -1+mu), mu=0.1
    (Sutcliffe 2007), as oriented closed polygons; number of components; Alexander polynomial
    of every component (3 random projections); linking matrix; Q from the linking number
    lk(position, linking);
  * the number of connected components of the tube phi3 < -1 + 0.2;
  * principal moments of the energy density (axial-symmetry diagnostic);
  * continuum extrapolation of E(h);
and writes results.json plus figures.
Usage: NUMBA_NUM_THREADS=2 python3 analyze.py
"""
import glob
import json
import os
import numpy as np
import fs_lib as fs

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'

TARGET = {  # Sutcliffe 2007 Table 2 (PLAN.md E8)
    1: ('A11', 1.204), 2: ('A21', 1.967), 3: ('A~31 (bent)', 2.754), 4: ('A22', 3.445),
    5: ('L^{1,1}_{1,2}', 4.095), 6: ('L^{1,1}_{2,2}', 4.650), 7: ('K32 (trefoil)', 5.242)}
MU = 0.1
LINK_TARGET = (np.sqrt(2 * MU - MU ** 2), 0.0, -1 + MU)


def curve_analysis(phi, h, L=7.5):
    pos, pinfo = fs.preimage_curves(phi, h, L=L)
    lnk, linfo = fs.preimage_curves(phi, h, L=L, target=LINK_TARGET)
    res = dict(pos_info=pinfo, link_info=linfo, n_position=len(pos), n_linking=len(lnk))
    res['position_lengths'] = [float(np.sum(np.linalg.norm(np.diff(np.vstack([c, c[:1]]), axis=0), axis=1))) for c in pos]
    alex = []
    for c in pos:
        al = [str(fs.alexander_polynomial(c, seed=s)[0]) for s in (2, 3, 4)]
        alex.append(al)
    res['alexander'] = alex
    allc = pos + lnk
    lks = []
    for s in (1, 5, 9):
        Lk, wr, _ = fs.linking_matrix(allc, seed=s)
        lks.append(Lk)
    Lk = -lks[0]   # all linking numbers reported with Sutcliffe's orientation (spatially reflected)
    res['linking_matrix_consistent'] = bool(all(np.allclose(Lk, x) for x in lks))
    npos = len(pos)
    res['lk_position_position'] = Lk[:npos, :npos].tolist()
    res['lk_position_linking'] = Lk[:npos, npos:].tolist()
    res['Q_from_linking'] = float(Lk[:npos, npos:].sum())   # Sutcliffe sign (see conventions)
    # per position component: total lk with linking curves, and with the linking-curve components
    # closest to it (twist)
    twist = []
    for a, c in enumerate(pos):
        near = []
        for b, d in enumerate(lnk):
            dist = np.min(np.linalg.norm(d[:, None, :] - c[None, :, :], axis=-1), axis=1).mean()
            dists = [np.min(np.linalg.norm(d[:, None, :] - cc[None, :, :], axis=-1), axis=1).mean() for cc in pos]
            if int(np.argmin(dists)) == a:
                near.append(b)
        twist.append(float(sum(Lk[a, npos + b] for b in near)))
    res['twist_per_component'] = twist
    res['total_lk_per_component'] = [float(Lk[a, npos:].sum()) for a in range(npos)]
    return res, pos, lnk


def tube_components(phi, nu=0.2):
    from scipy.ndimage import label
    lab, n = label(phi[..., 2] < -1 + nu)
    sizes = np.bincount(lab.ravel())[1:]
    return int(n), sizes.tolist()


def extrapolate(hs, Es):
    hs = np.asarray(hs); Es = np.asarray(Es)
    out = {}
    if len(hs) >= 2:
        A = np.vstack([np.ones_like(hs[-2:]), hs[-2:] ** 2]).T
        c = np.linalg.solve(A, Es[-2:])
        out['E0_h2_two_finest'] = float(c[0])
    if len(hs) >= 3:
        A = np.vstack([np.ones_like(hs), hs ** 2, hs ** 4]).T
        c, *_ = np.linalg.lstsq(A, Es, rcond=None)
        out['E0_h2h4_all'] = float(c[0])
        A = np.vstack([np.ones_like(hs[-3:]), hs[-3:] ** 2]).T
        c2, *_ = np.linalg.lstsq(A, Es[-3:], rcond=None)
        out['E0_h2_three_finest'] = float(c2[0])
    vals = [v for v in out.values()]
    if vals:
        out['E0_best'] = out.get('E0_h2h4_all', out.get('E0_h2_two_finest'))
        out['E0_spread'] = float(max(vals) - min(vals)) if len(vals) > 1 else None
    return out


def main():
    runs = sorted(glob.glob(os.path.join(HERE, 'runs', 'Q*.json')))
    results = dict(conventions=dict(
        energy='E = 1/(32 sqrt2 pi^2) Int [ d_i phi.d_i phi + 1/2 (d_i phi x d_j phi)^2 ] d^3x (Sutcliffe 2007), Ward bound E >= Q^{3/4}',
        lattice='forward-difference links (sigma term) + 4-corner plaquette average (Skyrme term), exact discrete gradient, field fixed to e3 on the boundary of [-L,L]^3, L = 7.5',
        hopf='Q_W = (1/16 pi^2) Int A.B, B_i = 1/2 eps_ijk phi.(d_j phi x d_k phi), curl A = B (Coulomb gauge, FFT); with W=(phi1+i phi2)/(1+phi3) and Sutcliffe\'s (Z1,Z0) the rational map W=Z1^n/Z0^m gives Q_W = -nm in the standard orientation of R^3 (the map R^3 -> S^3 of Sutcliffe eq. 3.1 reverses orientation). Q is reported with Sutcliffe\'s sign, Q = -Q_W.',
        position_curve='preimage of -e3; linking curve: preimage of (sqrt(2mu-mu^2),0,-1+mu), mu=0.1; tube phi3 < -0.8'),
        runs={})
    for rpath in runs:
        R = json.load(open(rpath))
        name = R['run']
        Q = fs.MAPS[R['map']][0]
        stages = sorted(R['stages'], key=lambda s: -s['h'])
        entry = dict(map=R['map'], Q_nominal=Q, Lf=R['Lf'], L=R['L'], offset=R['offset'], initial=R.get('initial'),
                     stages=[dict(N=s['N'], h=s['h'], E=s['E'], E2=s['E2'], E4=s['E4'], virial=(s['E2'] - s['E4']) / s['E'],
                                  Q=-s['Q'], hedgehogs=s['hedgehogs'], minphi3=s['minphi3'], t=s['t'],
                                  converged=s['converged'], wall_s=s['wall_s']) for s in stages])
        hs = [s['h'] for s in stages if s['L'] == 7.5]
        Es = [s['E'] for s in stages if s['L'] == 7.5]
        entry['extrapolation'] = extrapolate(hs, Es)
        # analysis of the finest field
        fin = stages[-1]
        ck = os.path.join(SCRATCH, f"{name}_N{fin['N']}.phi.npy")
        if os.path.exists(ck):
            phi = np.load(ck)
            h = fin['h']
            ca, pos, lnk = curve_analysis(phi, h, L=R['L'])
            entry['curves_finest'] = ca
            entry['tube_components'] = tube_components(phi)
            c, ev, evec, tot = fs.energy_inertia(phi, h, L=R['L'])
            entry['energy_centre'] = c.tolist()
            entry['inertia_eigs'] = ev.tolist()
            # axial symmetry: two principal moments equal (relative difference of the closest pair)
            entry['inertia_axial_asym'] = float(min(ev[1] - ev[0], ev[2] - ev[1]) / ev[2])
            np.savez_compressed(os.path.join(HERE, 'runs', f'{name}_curves.npz'),
                                **{f'pos{i}': p for i, p in enumerate(pos)}, **{f'lnk{i}': p for i, p in enumerate(lnk)})
            # also classify at the next-coarser grid for robustness
            if len(stages) > 1:
                prev = stages[-2]
                ck2 = os.path.join(SCRATCH, f"{name}_N{prev['N']}.phi.npy")
                if os.path.exists(ck2):
                    phi2 = np.load(ck2)
                    ca2, _, _ = curve_analysis(phi2, prev['h'], L=R['L'])
                    entry['curves_previous_grid'] = dict(N=prev['N'], n_position=ca2['n_position'],
                                                         alexander=ca2['alexander'], Q_from_linking=ca2['Q_from_linking'],
                                                         lk_position_position=ca2['lk_position_position'])
        results['runs'][name] = entry
        print(name, 'E(h):', [(round(s['h'], 4), round(s['E'], 5), round(-s['Q'], 4)) for s in stages],
              'extrap', entry['extrapolation'].get('E0_best'))
        if 'curves_finest' in entry:
            ca = entry['curves_finest']
            print('   position comps', ca['n_position'], 'alexander', ca['alexander'], 'lk pos-pos', ca['lk_position_position'],
                  'Q_link', ca['Q_from_linking'], 'twist', ca['twist_per_component'], 'tube comps', entry['tube_components'][0],
                  'inertia', np.round(entry['inertia_eigs'], 4))
    json.dump(results, open(os.path.join(HERE, 'analysis_raw.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
