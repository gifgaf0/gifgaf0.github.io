"""
make_results.py -- build results.json and the figures from analysis_raw.json.
Usage: python3 make_results.py   (after analyze.py)
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'analysis_raw.json')))
extra_path = os.path.join(HERE, 'analysis_extra.json')
EXTRA = json.load(open(extra_path)) if os.path.exists(extra_path) else {}

TARGET = {1: ('A11', 1.204), 2: ('A21', 1.967), 3: ('A~31', 2.754), 4: ('A22', 3.445),
          5: ('L^{1,1}_{1,2}', 4.095), 6: ('L^{1,1}_{2,2}', 4.650), 7: ('K32', 5.242)}
PRIMARY = {1: 'Q1_A11', 2: 'Q2_A21', 3: 'Q3_A31', 4: 'Q4_A22', 5: 'Q5_K32', 6: 'Q6_L22', 7: 'Q7_K32'}
BOUND_C = (3 / 16) ** (3 / 8)


def classify(e):
    """Configuration type from the position/linking curves of the finest field."""
    ca = e.get('curves_finest')
    if ca is None:
        return 'n/a', {}
    npos = ca['n_position']
    alex = [a[0] for a in ca['alexander']]
    alex_consistent = all(len(set(a)) == 1 for a in ca['alexander'])
    knotted = [a != '1' for a in alex]
    asym = e['inertia_axial_asym']
    ev = e['inertia_eigs']
    det = dict(n_position_components=npos, alexander=alex, alexander_consistent=alex_consistent,
               lk_position_position=ca['lk_position_position'], twist=ca['twist_per_component'],
               total_lk_per_component=ca['total_lk_per_component'], Q_from_linking=ca['Q_from_linking'],
               inertia_eigs=ev, axial_asymmetry=asym, tube_components=e['tube_components'][0],
               n_linking_components=ca['n_linking'])
    if npos == 1 and knotted[0]:
        if alex[0] in ('t**2 - t + 1',):
            return 'K32 (trefoil)', det
        return f'knot (Alexander {alex[0]})', det
    if npos == 1:
        # unknot: axial (two equal moments) or bent
        axial = asym < 0.01
        n = abs(round(ca['Q_from_linking']))
        return (f'A_{{{n},1}} axial' if axial else f'A~_{{{n},1}} bent (unknot, non-axial)'), det
    if npos >= 2:
        lk = np.array(ca['lk_position_position'])
        if np.allclose(lk, 0):
            return f'{npos} unlinked loops', det
        return f'{npos}-component link', det
    return 'none', det


def main():
    runs = A['runs']
    E1 = None
    rows = []
    out = dict(experiment='E8 Faddeev-Skyrme knots (Model C)', conventions=A['conventions'], headline=[], per_charge={},
               extra=EXTRA)
    for Q in range(1, 8):
        name = PRIMARY[Q]
        if name not in runs:
            continue
        e = runs[name]
        st = {round(s['h'], 4): s for s in e['stages']}
        s01 = st.get(0.1)
        if s01 is None:
            continue
        if Q == 1:
            E1 = s01['E']
            E1x = e['extrapolation'].get('E0_best')
        typ, det = classify(e)
        ex = e['extrapolation']
        rec = dict(run=name, initial_map=e['map'], E_h01=s01['E'], E_over_Q34_h01=s01['E'] / Q ** 0.75,
                   E_continuum_est=ex.get('E0_best'), E_continuum_spread=ex.get('E0_spread'),
                   E_by_h={str(k): v['E'] for k, v in st.items()}, Q_by_h={str(k): v['Q'] for k, v in st.items()},
                   hedgehogs_by_h={str(k): v['hedgehogs'] for k, v in st.items()},
                   minphi3_by_h={str(k): v['minphi3'] for k, v in st.items()},
                   virial_by_h={str(k): v['virial'] for k, v in st.items()},
                   converged_by_h={str(k): v['converged'] for k, v in st.items()},
                   type_found=typ, type_details=det, type_target=TARGET[Q][0], E_target=TARGET[Q][1],
                   E_over_Q34_target=TARGET[Q][1] / Q ** 0.75, bound_proven=BOUND_C * Q ** 0.75, ward_bound=Q ** 0.75)
        rec['E_rel_dev_h01'] = s01['E'] / TARGET[Q][1] - 1
        rec['verdict_E'] = 'CALIBRATED' if abs(rec['E_rel_dev_h01']) <= 0.02 else 'MISS'
        if rec['E_continuum_est'] is not None:
            rec['E_cont_rel_dev'] = rec['E_continuum_est'] / TARGET[Q][1] - 1
            rec['verdict_E_continuum'] = 'CALIBRATED' if abs(rec['E_cont_rel_dev']) <= 0.02 else 'MISS'
        if E1 is not None:
            rec['E_over_E1_h01'] = s01['E'] / E1
            rec['E_over_E1_target'] = TARGET[Q][1] / TARGET[1][1]
            rec['E_over_QE1_h01'] = s01['E'] / (Q * E1)
            rec['ratio_rel_dev'] = rec['E_over_E1_h01'] / rec['E_over_E1_target'] - 1
            rec['verdict_ratio'] = 'CALIBRATED' if abs(rec['ratio_rel_dev']) <= 0.01 else 'MISS'
            if rec['E_continuum_est'] is not None and E1x is not None:
                rec['E_over_E1_continuum'] = rec['E_continuum_est'] / E1x
        qdev = max(abs(v - round(v)) for v in rec['Q_by_h'].values())
        qint = all(round(v) == Q for v in rec['Q_by_h'].values())
        rec['Q_max_dev_from_integer'] = qdev
        rec['verdict_Q'] = 'CALIBRATED' if (qdev <= 0.05 and qint) else 'MISS'
        out['per_charge'][str(Q)] = rec
        rows.append((Q, rec))
    # headline list
    for Q, r in rows:
        out['headline'].append(dict(quantity=f'E_{Q} (dx=0.1, box [-7.5,7.5]^3)', value=r['E_h01'], target=r['E_target'],
                                    tolerance='2%', verdict=r['verdict_E']))
        if Q > 1:
            out['headline'].append(dict(quantity=f'E_{Q}/E_1 (dx=0.1)', value=r['E_over_E1_h01'],
                                        target=r['E_over_E1_target'], tolerance='1%', verdict=r['verdict_ratio']))
        out['headline'].append(dict(quantity=f'Q (Whitehead) for charge-{Q} run, all grids', value=list(r['Q_by_h'].values()),
                                    target=Q, tolerance='0.05', verdict=r['verdict_Q']))
        out['headline'].append(dict(quantity=f'type at Q={Q}', value=r['type_found'], target=r['type_target'],
                                    tolerance='topological type', verdict=None))
    json.dump(out, open(os.path.join(HERE, 'results.json'), 'w'), indent=1, default=float)

    # ---------------------------------------------------------------- figures
    Qs = [Q for Q, _ in rows]
    fig, ax = plt.subplots(figsize=(5.2, 3.4), dpi=110)
    ax.plot(Qs, [TARGET[Q][1] / Q ** 0.75 for Q in Qs], 's', mfc='none', color='0.35', label='Sutcliffe 2007 (dx=0.1)')
    ax.plot(Qs, [r['E_over_Q34_h01'] for _, r in rows], 'o', color='C0', label='this work, dx=0.1')
    xs = [Q for Q, r in rows if r['E_continuum_est'] is not None]
    ax.plot(xs, [r['E_continuum_est'] / Q ** 0.75 for Q, r in rows if r['E_continuum_est'] is not None], '^',
            color='C3', label='this work, dx -> 0 estimate')
    ax.axhline(1.0, color='0.6', lw=0.8, ls='--')
    ax.text(1.0, 1.005, 'Ward conjecture E = Q^{3/4}', fontsize=7, color='0.4')
    ax.set_xlabel('Hopf charge Q')
    ax.set_ylabel(r'$E/Q^{3/4}$')
    ax.set_ylim(0.98, 1.30)
    ax.legend(fontsize=7, loc='upper right')
    ax.set_title('Energy per Ward bound (proven bound: 0.534)', fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'fig_energy_ratio.png'))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.2, 3.4), dpi=110)
    for Q, r in rows:
        hh = sorted(float(k) for k in r['E_by_h'])
        EE = [r['E_by_h'][str(round(h, 4)) if str(round(h, 4)) in r['E_by_h'] else str(h)] for h in hh]
        ax.plot(np.array(hh) ** 2, np.array(EE) / Q ** 0.75, 'o-', ms=3, label=f'Q={Q}')
        if r['E_continuum_est'] is not None:
            ax.plot([0], [r['E_continuum_est'] / Q ** 0.75], 'k_', ms=8)
    ax.set_xlabel(r'$\Delta x^2$')
    ax.set_ylabel(r'$E/Q^{3/4}$')
    ax.set_title('Resolution study (box [-7.5,7.5]^3, fixed boundary)', fontsize=9)
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'fig_resolution.png'))
    plt.close(fig)

    # position curves
    n = len(rows)
    fig = plt.figure(figsize=(2.3 * min(n, 4), 2.4 * ((n + 3) // 4)), dpi=90)
    for idx, (Q, r) in enumerate(rows):
        ax = fig.add_subplot((n + 3) // 4, min(n, 4), idx + 1, projection='3d')
        z = np.load(os.path.join(HERE, 'runs', f"{r['run']}_curves.npz"))
        for k in sorted(z.files):
            c = z[k]
            c = np.vstack([c, c[:1]])
            if k.startswith('pos'):
                ax.plot(c[:, 0], c[:, 1], c[:, 2], lw=3.0, color=['C0', 'C1', 'C2'][int(k[3:]) % 3])
            else:
                ax.plot(c[:, 0], c[:, 1], c[:, 2], lw=0.8, color='0.25')
        lim = 3.2 if Q < 5 else 4.0
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        ax.set_title(f"Q={Q}: {r['type_found']}", fontsize=7)
        ax.view_init(elev=55, azim=30)
    fig.suptitle('position curves (thick, phi=-e3) and linking curves (thin), dx=0.1', fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'fig_position_curves.png'))
    plt.close(fig)
    for Q, r in rows:
        print(Q, r['type_found'], f"E(0.1)={r['E_h01']:.4f} target {r['E_target']} dev {100*r['E_rel_dev_h01']:+.2f}% {r['verdict_E']}",
              f"cont {r['E_continuum_est']}", f"ratio {r.get('E_over_E1_h01', float('nan')):.4f} vs {r.get('E_over_E1_target', float('nan')):.4f} {r.get('verdict_ratio')}",
              f"Q {r['Q_by_h']} {r['verdict_Q']}")


if __name__ == '__main__':
    main()
