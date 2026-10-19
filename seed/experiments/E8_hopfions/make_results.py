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
TESTS = json.load(open(os.path.join(HERE, 'tests_output.json')))
ANSATZ = json.load(open(os.path.join(HERE, 'check_ansatz_energy.json')))

# Sutcliffe 2007, Table 2 (PLAN.md E8): type label, E
TARGET = {1: ('A1,1', 1.204), 2: ('A2,1', 1.967), 3: ('A~3,1', 2.754), 4: ('A2,2', 3.445),
          5: ('L11_12', 4.095), 6: ('L11_22', 4.650), 7: ('K32', 5.242)}
TYPE_PRETTY = {'A1,1': 'A_{1,1}', 'A2,1': 'A_{2,1}', 'A~3,1': 'bent A~_{3,1}', 'A2,2': 'A_{2,2}',
               'L11_12': 'link L^{1,1}_{1,2}', 'L11_22': 'link L^{1,1}_{2,2}', 'K32': 'trefoil K_{3,2}'}
PRIMARY = {1: 'Q1_A11', 2: 'Q2_A21', 3: 'Q3_A31', 4: 'Q4_A22', 5: 'Q5_K32', 6: 'Q6_L22', 7: 'Q7_K32'}
BOUND_C = (3 / 16) ** (3 / 8)
H_REF = 0.1


def stage_at(e, h):
    for s in e['stages']:
        if abs(s['h'] - h) < 1e-6 and abs(s['L'] - 7.5) < 1e-9:
            return s
    return None


def main():
    runs = A['runs']
    out = dict(experiment='E8 Faddeev-Skyrme Hopf solitons (Model C), SEED.md sec. 4 and 6C; preregistered in PLAN.md sec. 4 E8',
               conventions=A['conventions'],
               units='energies in units of 32 sqrt(2) pi^2 x (sigma-model coupling); dimensionless as in Sutcliffe 2007',
               target_source='Sutcliffe 2007 (arXiv:0705.1468), Table 2: dx = 0.1, 151^3 grid, fixed boundary; '
                             'absolute energies about 1% low, relative energies about 0.1%',
               tolerances='E_Q within 2% of the table (Q=1-4 required), E_Q/E_1 within 1%, type match, |Q - integer| <= 0.05',
               library_tests=dict(gradient_rel_err=TESTS['grad_check_rel_err'],
                                  continuum_order_ratio_E2=TESTS['continuum_ratio_E2'],
                                  continuum_order_ratio_E4=TESTS['continuum_ratio_E4'],
                                  alexander=[TESTS['alexander_parametric_trefoil'], TESTS['alexander_unknot'], TESTS['alexander_fig8']],
                                  ansatz_energy_quadrature_vs_lattice=ANSATZ),
               headline=[], per_charge={}, box_study={}, seed_claims={})
    rows = []
    E1 = E1c = None
    for Q in range(1, 8):
        name = PRIMARY[Q]
        if name not in runs:
            continue
        e = runs[name]
        s01 = stage_at(e, H_REF)
        fa = e['field_analysis']
        Nfin = max(int(k) for k in fa) if fa else None
        afin = fa[str(Nfin)] if fa else None
        rec = dict(run=name, initial_map=e['map'], Q_nominal=Q, L=e['L'],
                   E_by_h={f"{s['h']:.4f}": s['E'] for s in e['stages']},
                   E2_by_h={f"{s['h']:.4f}": s['E2'] for s in e['stages']},
                   E4_by_h={f"{s['h']:.4f}": s['E4'] for s in e['stages']},
                   virial_by_h={f"{s['h']:.4f}": s['virial'] for s in e['stages']},
                   Q_by_h={f"{s['h']:.4f}": s['Q'] for s in e['stages']},
                   hedgehogs_by_h={f"{s['h']:.4f}": s['hedgehogs'] for s in e['stages']},
                   minphi3_by_h={f"{s['h']:.4f}": s['minphi3'] for s in e['stages']},
                   converged_by_h={f"{s['h']:.4f}": s['converged'] for s in e['stages']},
                   flow_time_by_h={f"{s['h']:.4f}": s['t'] for s in e['stages']},
                   wall_s_by_h={f"{s['h']:.4f}": s['wall_s'] for s in e['stages']},
                   extrapolation=e['extrapolation'],
                   E_target=TARGET[Q][1], type_target=TARGET[Q][0], ward_bound=Q ** 0.75, proven_bound=BOUND_C * Q ** 0.75)
        rec['h_finest'] = min(s['h'] for s in e['stages'])
        if afin is not None:
            rec['type_found'] = afin['type']
            rec['type_found_by_N'] = {N: a['type'] for N, a in fa.items()}
            rec['type_details_finest'] = {k: afin[k] for k in ('n_position', 'alexander', 'lk_position_position', 'Q_from_linking',
                                                               'twist_per_component', 'twist_from_total_lk', 'total_lk_per_component', 'slice_degrees',
                                                               'inertia_eigs', 'inertia_axial_asym', 'loop_shapes', 'tube_components',
                                                               'linking_consistent_3_projections', 'pos_info', 'link_info')}
            rec['verdict_type'] = 'CALIBRATED' if afin['type'] == TARGET[Q][0] and all(a['type'] == TARGET[Q][0] for a in fa.values()) else 'MISS'
        qvals = list(rec['Q_by_h'].values())
        rec['Q_max_dev_from_integer'] = float(max(abs(v - Q) for v in qvals))
        rec['verdict_Q'] = 'CALIBRATED' if rec['Q_max_dev_from_integer'] <= 0.05 else 'MISS'
        # diagnostic (not a pass criterion): our dx = 0.2 energy against the dx = 0.1 table value.  A second-order
        # centred-difference scheme has a leading truncation error 4x that of our link differences, i.e. equal to ours
        # at twice the spacing; whether Sutcliffe's code is of that kind is not stated in his paper.
        s02 = stage_at(e, 0.2)
        if s02 is not None:
            rec['E_h02'] = s02['E']
            rec['E_h02_rel_to_target'] = s02['E'] / TARGET[Q][1] - 1
        fin = min(e['stages'], key=lambda s: s['h'])
        rec['E_finest'] = fin['E']
        rec['E_finest_rel_to_target'] = fin['E'] / TARGET[Q][1] - 1
        if s01 is not None:
            rec['E_h01'] = s01['E']
            rec['E_over_Q34_h01'] = s01['E'] / Q ** 0.75
            rec['E_rel_dev_h01'] = s01['E'] / TARGET[Q][1] - 1
            rec['verdict_E'] = 'CALIBRATED' if abs(rec['E_rel_dev_h01']) <= 0.02 else 'MISS'
            if Q == 1:
                E1 = s01['E']
            if E1 is not None:
                rec['E_over_E1_h01'] = s01['E'] / E1
                rec['E_over_E1_target'] = TARGET[Q][1] / TARGET[1][1]
                rec['E_over_QE1_h01'] = s01['E'] / (Q * E1)
                rec['ratio_rel_dev'] = rec['E_over_E1_h01'] / rec['E_over_E1_target'] - 1
                rec['verdict_ratio'] = 'CALIBRATED' if abs(rec['ratio_rel_dev']) <= 0.01 else 'MISS'
        ex = e['extrapolation']
        if ex.get('E0_best') is not None and len(ex.get('hs', [])) >= 3 and min(ex['hs']) <= H_REF + 1e-6:
            rec['E_continuum_est'] = ex['E0_best']
            rec['E_continuum_spread'] = ex['E0_spread']
            if Q == 1:
                E1c = ex['E0_best']
            if E1c is not None:
                rec['E_over_E1_continuum'] = ex['E0_best'] / E1c
        out['per_charge'][str(Q)] = rec
        rows.append((Q, rec))

    # box study (dx = 0.2)
    for name, e in runs.items():
        if not name.startswith('box_'):
            continue
        base = runs.get('Q1_A11' if e['map'] == 'A11' else 'Q2_A21')
        s = e['stages'][0]
        b = stage_at(base, s['h']) if base else None
        out['box_study'][name] = dict(L=e['L'], h=s['h'], E=s['E'], virial=s['virial'], Q=s['Q'], converged=s['converged'],
                                      E_L7p5_same_h=(b['E'] if b else None),
                                      rel_change_vs_L7p5=(s['E'] / b['E'] - 1 if b else None))

    # axially symmetric 2D reduction (independent code): resolution and box-size sequences for A_{1,1}, A_{2,1}
    axp = os.path.join(HERE, 'axial2d.json')
    if os.path.exists(axp):
        AX = json.load(open(axp))
        out['axial2d'] = dict(description=AX.get('description'), grad_check_rel_err=AX.get('grad_check_rel_err'),
                              ansatz_checks=dict(linear_Lf4=AX.get('ansatz_linear_Lf4'), gauss_w2=AX.get('ansatz_gauss_w2')),
                              relaxed={k: dict(n=v['n'], R=v['R'], h=v['h'], E=v['E'], iters=v['iters'], msg=v['msg'])
                                       for k, v in AX.get('relaxed', {}).items()},
                              extrapolated=AX.get('extrapolated'))
        ext = AX.get('extrapolated') or {}
        inf = {}
        for Q, n in ((1, 'n1'), (2, 'n2')):
            r = out['per_charge'].get(str(Q))
            if r is None or n not in ext or 'E_continuum_est' not in r:
                continue
            shift = ext[n]['box_shift_7p5_to_25']
            inf[str(Q)] = dict(E_continuum_box7p5_3d=r['E_continuum_est'], E_continuum_cyl7p5_axial=ext[n]['E_R7p5_continuum_h2'],
                               box_shift_7p5_to_25_axial_h0p1=shift,
                               E_infinite_volume_continuum_est=r['E_continuum_est'] + shift,
                               E_infinite_volume_continuum_est_axial_only=ext[n]['E_infinite_volume_continuum_est'])
        if '1' in inf and '2' in inf:
            inf['E2_over_E1'] = inf['2']['E_infinite_volume_continuum_est'] / inf['1']['E_infinite_volume_continuum_est']
        out['continuum_infinite_volume_estimates'] = inf

    # headline
    for Q, r in rows:
        if 'E_h01' in r:
            out['headline'].append(dict(quantity=f'E_{Q} at dx=0.1 (box [-7.5,7.5]^3)', value=r['E_h01'], target=r['E_target'],
                                        tolerance='2%', verdict=r['verdict_E'], rel_dev=r['E_rel_dev_h01']))
            if Q > 1 and 'E_over_E1_h01' in r:
                out['headline'].append(dict(quantity=f'E_{Q}/E_1 at dx=0.1', value=r['E_over_E1_h01'], target=r['E_over_E1_target'],
                                            tolerance='1%', verdict=r['verdict_ratio'], rel_dev=r['ratio_rel_dev']))
        out['headline'].append(dict(quantity=f'Hopf charge of the Q={Q} solution (all grids)', value=r['Q_by_h'], target=Q,
                                    tolerance='0.05', verdict=r['verdict_Q']))
        if 'type_found' in r:
            out['headline'].append(dict(quantity=f'configuration type at Q={Q}', value=r['type_found'], target=r['type_target'],
                                        tolerance='same type', verdict=r['verdict_type']))

    inf = out.get('continuum_infinite_volume_estimates', {})
    for Q in ('1', '2'):
        if Q in inf:
            out['headline'].append(dict(quantity=f'E_{Q} continuum, infinite volume (3D dx->0 in box 7.5 + axial box shift 7.5->25)',
                                        value=inf[Q]['E_infinite_volume_continuum_est'],
                                        target=('1.21-1.22 (PLAN.md: more accurate literature values)' if Q == '1' else None),
                                        tolerance=None, verdict='NO_TARGET'))

    # seed claims
    have ={Q: r for Q, r in rows if 'E_h01' in r}
    if 1 in have and 2 in have:
        out['seed_claims']['E2_lt_2E1'] = dict(E2=have[2]['E_h01'], twoE1=2 * have[1]['E_h01'],
                                               ratio=have[2]['E_h01'] / (2 * have[1]['E_h01']),
                                               holds=bool(have[2]['E_h01'] < 2 * have[1]['E_h01']))
    out['seed_claims']['E_over_Q34'] = {str(Q): r['E_over_Q34_h01'] for Q, r in have.items()}
    out['seed_claims']['E_over_QE1'] = {str(Q): r.get('E_over_QE1_h01') for Q, r in have.items()}
    # stability against fission into any two lower-charge solutions reached (same dx = 0.1, same box)
    fis = {}
    for Q in sorted(have):
        splits = [(a, Q - a) for a in sorted(have) if a <= Q - a and (Q - a) in have]
        if splits:
            worst = min(splits, key=lambda s: have[s[0]]['E_h01'] + have[s[1]]['E_h01'])
            fis[str(Q)] = dict(splits_checked=[list(s) for s in splits], E_Q=have[Q]['E_h01'],
                               cheapest_split=list(worst), E_split=have[worst[0]]['E_h01'] + have[worst[1]]['E_h01'],
                               binding_rel=1 - have[Q]['E_h01'] / (have[worst[0]]['E_h01'] + have[worst[1]]['E_h01']))
    out['seed_claims']['fission_check'] = fis
    out['seed_claims']['above_ward_and_proven_bounds'] ={str(Q): bool(r['E_h01'] > Q ** 0.75 > BOUND_C * Q ** 0.75) for Q, r in have.items()}
    if 7 in dict(rows):
        out['seed_claims']['Q7_type'] = dict(rows)[7].get('type_found')
    # power-law fit E = c Q^p over the charges reached (ours at dx = 0.1, and Sutcliffe's table)
    if len(have) >= 3:
        qq = np.array(sorted(have)); ee = np.array([have[q]['E_h01'] for q in qq])
        p, lc = np.polyfit(np.log(qq), np.log(ee), 1)
        pt, lct = np.polyfit(np.log(qq), np.log([TARGET[q][1] for q in qq]), 1)
        out['seed_claims']['power_law_fit'] = dict(Q=qq.tolist(), p_ours=float(p), c_ours=float(np.exp(lc)),
                                                   p_sutcliffe_same_Q=float(pt), c_sutcliffe_same_Q=float(np.exp(lct)))
        out['seed_claims']['E_over_Q_monotone_decreasing'] = bool(np.all(np.diff(ee / qq) < 0))
        out['seed_claims']['E_over_Q'] = {str(q): float(have[q]['E_h01'] / q) for q in qq}
    json.dump(out, open(os.path.join(HERE, 'results.json'), 'w'), indent=1, default=float)

    # ---------------------------------------------------------------- figures
    Qs = [Q for Q, r in rows if 'E_h01' in r]
    fig, ax = plt.subplots(figsize=(5.2, 3.4), dpi=110)
    ax.plot(range(1, 8), [TARGET[Q][1] / Q ** 0.75 for Q in range(1, 8)], 's', mfc='none', color='0.35', ms=7,
            label='Sutcliffe 2007 (dx = 0.1)')
    ax.plot(Qs, [have[Q]['E_over_Q34_h01'] for Q in Qs], 'o', color='C0', ms=4, label='this work, dx = 0.1')
    xs = [Q for Q, r in rows if 'E_continuum_est' in r]
    ax.plot(xs, [dict(rows)[Q]['E_continuum_est'] / Q ** 0.75 for Q in xs], '^', color='C3', ms=4,
            label='this work, dx -> 0 (same box)')
    ax.set_xlabel('Hopf charge Q')
    ax.set_ylabel(r'$E/Q^{3/4}$')
    ax.set_ylim(1.14, 1.27)
    ax.legend(fontsize=7, loc='lower right')
    ax.set_title('Energy over Ward\'s conjectured bound (proven bound: 0.534)', fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'fig_energy_ratio.png'))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.2, 3.4), dpi=110)
    for Q, r in rows:
        hh = sorted(float(k) for k in r['E_by_h'])
        EE = [r['E_by_h'][f'{h:.4f}'] for h in hh]
        ax.plot(np.array(hh) ** 2, np.array(EE) / Q ** 0.75, 'o-', ms=3, label=f'Q={Q}')
        if 'E_continuum_est' in r:
            ax.plot([0], [r['E_continuum_est'] / Q ** 0.75], '_', color='k', ms=9)
    ax.set_xlabel(r'$\Delta x^2$')
    ax.set_ylabel(r'$E/Q^{3/4}$')
    ax.set_xlim(-0.002, 0.042)
    ax.set_title('Resolution study (box [-7.5,7.5]^3; bars: extrapolation)', fontsize=9)
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'fig_resolution.png'))
    plt.close(fig)

    if 'axial2d' in out:
        rel = out['axial2d']['relaxed']
        fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.8), dpi=110)
        for n, col in ((1, 'C0'), (2, 'C1')):
            for h, mk in ((0.2, 's'), (0.1, 'o')):
                pts = sorted((v['R'], v['E']) for v in rel.values() if v['n'] == n and abs(v['h'] - h) < 1e-9)
                if pts:
                    R_, E_ = np.array(pts).T
                    axs[0].plot(1 / R_ ** 3, 100 * (E_ / E_[np.argmax(R_)] - 1), mk + '-', color=col, ms=3.5, mfc='none' if h == 0.2 else col,
                                label=f'n={n}, dx={h}')
            r3 = out['per_charge'].get(str(n))
            Eref = r3.get('E_continuum_est') if r3 else None
            if Eref is None:
                continue
            pts = sorted((v['h'], v['E']) for v in rel.values() if v['n'] == n and abs(v['R'] - 7.5) < 1e-9)
            if pts:
                h_, E_ = np.array(pts).T
                axs[1].plot(h_ ** 2, 100 * (E_ / Eref - 1), 'o-', color=col, ms=3.5, label=f'axial 2D, n={n} (cylinder R=7.5)')
            hh = sorted(float(k) for k in r3['E_by_h'])
            axs[1].plot(np.array(hh) ** 2, [100 * (r3['E_by_h'][f'{h:.4f}'] / Eref - 1) for h in hh], 'x--', color=col, ms=4,
                        label=f'3D lattice, Q={n} (cube L=7.5)')
        axs[0].set_xlabel(r'$1/R^3$'); axs[0].set_ylabel(r'$100\,(E(R)/E(R{=}25) - 1)$')
        axs[0].set_title('box size (axial 2D)', fontsize=8); axs[0].legend(fontsize=6)
        axs[1].set_xlabel(r'$\Delta x^2$'); axs[1].set_ylabel(r'$100\,(E/E_{3D,\Delta x\to 0} - 1)$'); axs[1].set_title('resolution: 2D vs 3D codes', fontsize=8)
        axs[1].legend(fontsize=5.5)
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, 'fig_box_axial.png'))
        plt.close(fig)

    n = len(rows)
    ncol = min(n, 4)
    nrow = (n + 3) // 4
    fig = plt.figure(figsize=(2.2 * ncol, 2.3 * nrow), dpi=90)
    for idx, (Q, r) in enumerate(rows):
        ax = fig.add_subplot(nrow, ncol, idx + 1, projection='3d')
        p = os.path.join(HERE, 'runs', f"{r['run']}_curves.npz")
        if os.path.exists(p):
            z = np.load(p)
            for k in sorted(z.files):
                c = z[k]
                c = np.vstack([c, c[:1]])
                if k.startswith('pos'):
                    ax.plot(c[:, 0], c[:, 1], c[:, 2], lw=2.6, color=['C0', 'C1', 'C2'][int(k[3:]) % 3])
                else:
                    ax.plot(c[:, 0], c[:, 1], c[:, 2], lw=0.7, color='0.2')
        lim = 2.6 if Q < 3 else 3.4
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        ax.set_title(f"Q={Q}: {TYPE_PRETTY.get(r.get('type_found'), r.get('type_found'))}\n(dx={r['h_finest']:.3g})", fontsize=7)
        ax.view_init(elev=60, azim=30)
    fig.suptitle('position curves (thick, phi = -e3) and linking curves (thin)', fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'fig_position_curves.png'))
    plt.close(fig)

    for Q, r in rows:
        print(f"Q={Q} {r.get('type_found')} (target {r['type_target']}) E(h)={ {k: round(v, 5) for k, v in r['E_by_h'].items()} } "
              f"E(0.1)={r.get('E_h01', float('nan')):.4f} vs {r['E_target']} ({100 * r.get('E_rel_dev_h01', float('nan')):+.2f}%) "
              f"{r.get('verdict_E')}  ratio {r.get('E_over_E1_h01', float('nan')):.4f} vs {r.get('E_over_E1_target', float('nan')):.4f} "
              f"{r.get('verdict_ratio')}  cont {r.get('E_continuum_est')}  Qdev {r['Q_max_dev_from_integer']:.4f} {r['verdict_Q']}")
    print('box study', out['box_study'])
    print('seed claims', out['seed_claims'])


if __name__ == '__main__':
    main()
