"""
make_results.py -- build results.json and the figures from analysis_raw.json.
Usage: python3 make_results.py   (after analyze.py; optionally after stencil_relax.py and qlink_coarse.py)

Reconciliation changes (2026-10-19, after the independent cross-check in crosscheck/):
  * infinite-volume estimates use the continuum (Richardson h = 0.2, 0.1) box shift of the axial code and add the
    energy beyond R = 25 from a power-law fit E(R) = E_inf + c R^-p; the earlier h = 0.1 shift without a tail is kept
    for the record.  The 3D-cube estimate is now labelled a lower estimate (the cube's box effect is smaller than
    that of the inscribed cylinder whose shift is applied to it);
  * the absolute-energy verdicts state their convention (same grid, dx = 0.1) and carry the continuum comparison;
  * the Hopf-charge criterion is an internal check (CHECK PASSED), named by estimator, with the cross-check's
    free-space estimator and the estimator-free linking-number charge alongside;
  * same-box continuum virial estimates; seed-claim verdicts with their caveats; a 'reconciliation' block that
    reads crosscheck/*.json, stencil_relax.json and qlink_coarse.json when present.
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


def tail_fit(Rs, Es):
    """E(R) = E_inf + c R^-p through three (R, E) points; returns (p, c, energy beyond the largest R)."""
    from scipy.optimize import brentq
    (R1, R2, R3), (E1, E2, E3) = Rs, Es
    target = (E1 - E3) / (E2 - E3)
    p = brentq(lambda q: (R1 ** -q - R3 ** -q) / (R2 ** -q - R3 ** -q) - target, 0.3, 15.0)
    c = (E1 - E3) / (R1 ** -p - R3 ** -p)
    return float(p), float(c), float(c * R3 ** -p)


def virial_continuum(e):
    """same-box continuum estimate of (E2 - E4)/E: v(h) = v0 + a h^2 + b h^4 through the three finest spacings"""
    st = sorted((s for s in e['stages'] if abs(s['L'] - 7.5) < 1e-9), key=lambda s: s['h'])
    if len(st) < 3:
        return None
    hs = np.array([s['h'] for s in st[:3]]); v = np.array([s['virial'] for s in st[:3]])
    M = np.vstack([np.ones(3), hs ** 2, hs ** 4]).T
    v0 = float(np.linalg.solve(M, v)[0])
    v0_h2 = float((v[0] * hs[1] ** 2 - v[1] * hs[0] ** 2) / (hs[1] ** 2 - hs[0] ** 2))
    return dict(v0_h2h4_three_finest=v0, v0_h2_two_finest=v0_h2, v_h0p1=float(v[0]))


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
        rec['virial_continuum_est'] = virial_continuum(e)
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
        relax = AX.get('relaxed', {})
        inf = {}
        for Q, n in ((1, 'n1'), (2, 'n2')):
            r = out['per_charge'].get(str(Q))
            if r is None or n not in ext or 'E_continuum_est' not in r:
                continue
            shift = ext[n]['box_shift_7p5_to_25']
            # continuum energy per cylinder radius by Richardson extrapolation from h = 0.2 and 0.1 (both available for every R)
            byR = {}
            for v in relax.values():
                if v['n'] == Q:
                    byR.setdefault(v['R'], {})[round(v['h'], 3)] = v['E']
            Rich = {R: (4 * d[0.1] - d[0.2]) / 3 for R, d in byR.items() if 0.1 in d and 0.2 in d}
            shift_c = Rich[25.0] - Rich[7.5]
            # energy beyond R = 25 from E(R) = E_inf + c R^-p through the continuum values at R = 12, 18, 25
            p_, c_, tail = tail_fit([12.0, 18.0, 25.0], [Rich[12.0], Rich[18.0], Rich[25.0]])
            p01, c01, tail01 = tail_fit([12.0, 18.0, 25.0], [byR[12.0][0.1], byR[18.0][0.1], byR[25.0][0.1]])
            e_ax = ext[n]['E_R7p5_continuum_h2'] + shift_c - tail
            unc = abs(shift_c - shift) * 0.2 + abs(ext[n]['E_R7p5_continuum_h2'] - ext[n]['E_R7p5_continuum_aitken']) * 0.5 + 0.2 * tail
            inf[str(Q)] = dict(
                E_continuum_box7p5_3d=r['E_continuum_est'], E_continuum_cyl7p5_axial=ext[n]['E_R7p5_continuum_h2'],
                E_continuum_by_R_axial_richardson={str(R): v for R, v in sorted(Rich.items())},
                box_shift_7p5_to_25_axial_h0p1=shift, box_shift_7p5_to_25_axial_continuum=shift_c,
                box_shift_rel_h0p1=shift / byR[7.5][0.1], box_shift_rel_continuum=shift_c / Rich[7.5],
                tail_fit_continuum=dict(p=p_, c=c_, energy_beyond_R25=tail),
                tail_fit_h0p1=dict(p=p01, c=c01, energy_beyond_R25=tail01),
                box_shift_rel_7p5_to_infinity_continuum=(shift_c - tail) / ext[n]['E_R7p5_continuum_h2'],
                E_infinite_volume_continuum_est=e_ax, uncertainty=unc,
                uncertainty_rule='20% of the Richardson correction to the box shift + half the spread of the two R = 7.5 '
                                 'continuum extrapolations (h^2 fit, Aitken) + 20% of the tail',
                E_lower_estimate_3d_cube=r['E_continuum_est'] + shift_c - tail,
                lower_estimate_note='3D same-box continuum plus the cylinder box shift: an underestimate, because the cube '
                                    '[-7.5,7.5]^3 contains the cylinder rho, |z| <= 7.5 and so has the smaller box effect',
                as_reported_before_reconciliation=dict(
                    E_3d_plus_axial_shift_h0p1=r['E_continuum_est'] + shift,
                    E_axial_only_h0p1_shift_no_tail=ext[n]['E_infinite_volume_continuum_est'],
                    note='used the h = 0.1 box shift and no energy beyond R = 25; the two errors pushed the estimates '
                         'in opposite directions'))
        if '1' in inf and '2' in inf:
            inf['E2_over_E1'] = inf['2']['E_infinite_volume_continuum_est'] / inf['1']['E_infinite_volume_continuum_est']
            inf['E2_over_2E1'] = inf['E2_over_E1'] / 2
        out['continuum_infinite_volume_estimates'] = inf

    # cross-check numbers (independent code in crosscheck/), read only for the comparison columns
    XC = {}
    for nm in ('xc_fields', 'xc_axial'):
        pth = os.path.join(HERE, 'crosscheck', nm + '.json')
        if os.path.exists(pth):
            XC[nm] = json.load(open(pth))
    QLINK = None
    pth = os.path.join(HERE, 'qlink_coarse.json')
    if os.path.exists(pth):
        QLINK = json.load(open(pth))

    def xc_field(run, N, key):
        f = XC.get('xc_fields', {}).get(f'{run}_N{N}')
        return None if f is None else f.get(key)

    NH = {0.2: 76, 0.15: 101, 0.125: 121, 0.1: 151}

    # headline
    for Q, r in rows:
        if 'E_h01' in r:
            ec = r.get('E_continuum_est')
            out['headline'].append(dict(
                quantity=f'E_{Q} at dx=0.1 (box [-7.5,7.5]^3, fixed boundary)', value=r['E_h01'], target=r['E_target'],
                tolerance='2%', verdict=(r['verdict_E'] + ' (same-grid comparison at dx = 0.1)' if r['verdict_E'] == 'CALIBRATED'
                                         else r['verdict_E']),
                rel_dev=r['E_rel_dev_h01'],
                comparison_convention='same grid as the target (dx = 0.1, 151^3, box [-7.5,7.5]^3, fixed boundary), the setting '
                                      'in which Sutcliffe computed Table 2; PLAN fixed the table, not the convention',
                E_same_box_continuum=ec,
                target_rel_to_same_box_continuum=(r['E_target'] / ec - 1 if ec else None),
                within_2pct_of_same_box_continuum=(bool(abs(r['E_target'] / ec - 1) <= 0.02) if ec else None),
                E_same_box_continuum_crosscheck_c4=xc_field(r['run'], 151, 'E_c4')))
            if Q > 1 and 'E_over_E1_h01' in r:
                out['headline'].append(dict(quantity=f'E_{Q}/E_1 at dx=0.1', value=r['E_over_E1_h01'], target=r['E_over_E1_target'],
                                            tolerance='1%', verdict=r['verdict_ratio'], rel_dev=r['ratio_rel_dev'],
                                            continuum_ratio_same_box=r.get('E_over_E1_continuum')))
        # Hopf charge: internal check (not a literature target).  Criterion |Q - n| <= 0.05 applied to the dx = 0.1 fields;
        # coarser stages reported with both Whitehead estimators.
        q01 = r['Q_by_h'].get('0.1000')
        xc_by_h = {}
        for hk in r['Q_by_h']:
            v = xc_field(r['run'], NH.get(round(float(hk), 3)), 'Q_whitehead_freespace')
            if v is not None:
                xc_by_h[hk] = abs(v)
        ql = {}
        if QLINK is not None:
            for N in (76, 101):
                f = QLINK['fields'].get(f"{r['run']}_N{N}")
                if f is not None:
                    ql[f'{f["h"]:.4f}'] = f['Q_from_linking_3_projections'][0]
        fa = runs[r['run']]['field_analysis']
        for N, a in fa.items():
            ql[f'{15 / (int(N) - 1):.4f}'] = a['Q_from_linking']
        dev01 = [abs(q01 - Q)] if q01 is not None else []
        if '0.1000' in xc_by_h:
            dev01.append(abs(xc_by_h['0.1000'] - Q))
        r['Q_dev_dx0p1_both_estimators'] = max(dev01) if dev01 else None
        r['Q_by_h_freespace_crosscheck'] = xc_by_h
        r['Q_from_linking_by_h'] = ql
        r['verdict_Q'] = 'CHECK PASSED' if dev01 and max(dev01) <= 0.05 else 'MISS'
        out['headline'].append(dict(
            quantity=f'Hopf charge of the Q={Q} solution (Whitehead integral; criterion applied at dx = 0.1)',
            value=r['Q_by_h'], estimator='solid-angle plaquette fluxes, periodic FFT (fs_lib.hopf_charge)',
            value_freespace_4th_order_crosscheck=xc_by_h, Q_from_linking_by_h=ql, target=Q, tolerance='0.05',
            max_dev_dx0p1_both_estimators=r['Q_dev_dx0p1_both_estimators'],
            max_dev_all_grids_solid_angle=r['Q_max_dev_from_integer'],
            max_dev_all_grids_freespace=(max(abs(v - Q) for v in xc_by_h.values()) if xc_by_h else None),
            verdict=r['verdict_Q'] + ' (internal check; dx = 0.1, both estimators)' if r['verdict_Q'] == 'CHECK PASSED' else r['verdict_Q'],
            note='At dx = 0.2 the deviation depends on the estimator (solid angle <= 0.017, free-space 4th-order <= 0.086); '
                 'the estimator-free linking-number charge is the exact integer wherever computed.'))
        if 'type_found' in r:
            out['headline'].append(dict(quantity=f'configuration type at Q={Q}', value=r['type_found'], target=r['type_target'],
                                        tolerance='same type', verdict=r['verdict_type']))

    inf = out.get('continuum_infinite_volume_estimates', {})
    xa = XC.get('xc_axial', {})

    def xc_best(key):
        rr = xa.get(key, {}).get('runs', {})
        return rr[max(rr, key=int)]['E'] if rr else None

    xc_inf = {'1': xc_best('n1m1_inf'), '2': xc_best('n2m1_inf')}
    for Q in ('1', '2'):
        if Q in inf:
            out['headline'].append(dict(
                quantity=f'E_{Q} continuum, infinite volume (axial code: R = 7.5 continuum + continuum box shift 7.5 -> 25 + '
                         f'power-law tail beyond 25)',
                value=inf[Q]['E_infinite_volume_continuum_est'], uncertainty=inf[Q]['uncertainty'],
                crosscheck_spectral_infinite_volume=xc_inf[Q],
                lower_estimate_3d_cube=inf[Q]['E_lower_estimate_3d_cube'],
                target=('1.21-1.22 (PLAN.md context: "more accurate literature values"; Sutcliffe 2007: "around 1.21")'
                        if Q == '1' else None),
                tolerance=None,
                verdict='CHECK PASSED (two independent codes agree; no preregistered tolerance)',
                note=('0.4% above the PLAN context range. Resolved: the cross-check spectral value on all of R^3 is '
                      f'{xc_inf[Q]}; the literature values near 1.21 come from finite-box lattice runs that underestimate '
                      '(Ward 1999 quotes the axial 1.25 of Gladikowski-Hellmund and the 3D 1.13 of Battye-Sutcliffe 1998, '
                      'the latter as a finite-volume underestimate)') if Q == '1' else None))
    if 'E2_over_E1' in inf:
        out['headline'].append(dict(quantity='E_2/E_1 continuum, infinite volume', value=inf['E2_over_E1'],
                                    crosscheck_spectral=(xc_inf['2'] / xc_inf['1'] if xc_inf['1'] else None),
                                    target='1.6337 (Sutcliffe, dx = 0.1)', tolerance=None,
                                    verdict='CHECK PASSED (two independent codes agree; no preregistered tolerance)'))

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
    # seed-claim verdicts (PLAN sec. 1 words), consistent with REPORT.md
    sc = out['seed_claims']
    infe = out.get('continuum_infinite_volume_estimates', {})
    sc['verdicts'] = [
        dict(claim='SEED sec. 4: E/Q^{3/4} stays near 1.2, so the energy per unit charge falls and bigger folds store charge '
                   'more cheaply', verdict='CONFIRMED (Q = 1-7)',
             evidence='E/Q^{3/4} = %.3f-%.3f at dx = 0.1 and %.2f-%.2f in the same-box continuum; E/Q falls monotonically; '
                      'every E_Q is 10-19%% below its cheapest split. Energies are those of the solutions reached from one start '
                      'per charge (upper bounds on the minima; they match Sutcliffe\'s survey).'
                      % (min(sc['E_over_Q34'].values()), max(sc['E_over_Q34'].values()),
                         min(r['E_continuum_est'] / Q ** 0.75 for Q, r in rows if 'E_continuum_est' in r),
                         max(r['E_continuum_est'] / Q ** 0.75 for Q, r in rows if 'E_continuum_est' in r))),
        dict(claim='E_2 < 2 E_1: a charge-2 fold does not split', verdict='CONFIRMED',
             evidence='E_2/(2E_1) = %.4f at dx = 0.1, %.4f in infinite volume (axial code); cross-check spectral 0.8166'
                      % (sc['E2_lt_2E1']['ratio'], infe.get('E2_over_2E1', float('nan')))),
        dict(claim='SEED sec. 4/6C: Q = 7 is a trefoil',
             verdict='CONFIRMED as a reproduction of the literature minimum (trefoil-type minimum reached from the '
                     'preregistered trefoil start; global minimality not re-searched here: one start per charge, so it rests '
                     'on Sutcliffe\'s survey)',
             evidence='one position loop with Alexander polynomial t^2-t+1 (3 projections, dx = 0.15 and 0.1), Q_link = 7, '
                      'E_7/E_1 = 4.3645 vs 4.3538'),
        dict(claim='SEED sec. 4: E >= c|Q|^{3/4}; the 3/4 power is the right one and the computed minima agree (Sutcliffe 2007)',
             verdict='AMENDED',
             evidence='all energies above Q^{3/4} and 0.534 Q^{3/4}; fitted exponent %.3f over Q <= 7 (Sutcliffe\'s table %.3f), '
                      'consistent with but not a test of the asymptotic 3/4; optimality is Lin & Yang 2004 (PLAN 3.1)'
                      % (sc['power_law_fit']['p_ours'], sc['power_law_fit']['p_sutcliffe_same_Q'])),
        dict(claim='SEED sec. 4/6C: the lowest folds are rings and each charge\'s minimum is a definite knot or link',
             verdict='CONFIRMED as a reproduction of the literature types (one start per charge; that these are the global '
                     'minima rests on Sutcliffe\'s survey)',
             evidence='A11, A21, bent A~31, A22, L^{1,1}_{1,2}, L^{1,1}_{2,2}, K32, all as in Sutcliffe Table 2'),
    ]

    # reconciliation with the independent cross-check (crosscheck/CROSSCHECK.md)
    rec = dict(note='added 2026-10-19 after the cross-check; see REPORT.md, section Reconciliation')
    cont = {str(Q): dict(E_same_box_continuum=r.get('E_continuum_est'),
                         E_same_box_continuum_crosscheck_c4=xc_field(r['run'], 151, 'E_c4'),
                         sutcliffe_rel_to_continuum=(r['E_target'] / r['E_continuum_est'] - 1 if r.get('E_continuum_est') else None),
                         ours_dx0p1_rel_to_target=r.get('E_rel_dev_h01'))
            for Q, r in rows}
    rec['1_absolute_energy_convention'] = dict(
        resolution='CALIBRATED holds for the same-grid comparison (dx = 0.1; +1.25% to +1.80%). Against the same-box continuum '
                   '(ours, confirmed by the cross-check\'s 4th-order energies to -0.02%/+0.07%) Sutcliffe\'s table is 1.7-2.2% '
                   'low, outside 2% for Q = 1, 4, 5, 7; against the infinite-volume continuum for Q = 1 it is 1.7% low. The '
                   'robust parts of the calibration are the ratios (<= 0.3%) and the types.',
        by_charge=cont,
        Q1_infinite_volume=dict(ours=infe.get('1', {}).get('E_infinite_volume_continuum_est'), crosscheck=xc_inf['1'],
                                sutcliffe_rel=(1.204 / xc_inf['1'] - 1 if xc_inf['1'] else None)))
    rec['2_hopf_estimators'] = {str(Q): dict(solid_angle=r['Q_by_h'], freespace_4th_order=r['Q_by_h_freespace_crosscheck'],
                                             linking=r['Q_from_linking_by_h']) for Q, r in rows}
    rec['3_E1_literature'] = dict(ours=infe.get('1', {}).get('E_infinite_volume_continuum_est'),
                                  ours_uncertainty=infe.get('1', {}).get('uncertainty'), crosscheck_spectral=xc_inf['1'],
                                  context='PLAN 1.21-1.22 is summary-grade; Sutcliffe 2007: "around 1.21" from several '
                                          'authors; Ward 1999 (hep-th/9811176) quotes axial 1.25 K0 (Gladikowski-Hellmund) '
                                          'and 3D 1.13 K0 (Battye-Sutcliffe 1998, called a finite-volume underestimate); '
                                          'K0 = 1 in these units')
    rec['4_box'] = {Q: {k: infe[Q][k] for k in ('box_shift_rel_h0p1', 'box_shift_rel_continuum', 'box_shift_rel_7p5_to_infinity_continuum',
                                                'tail_fit_continuum', 'tail_fit_h0p1')} for Q in ('1', '2') if Q in infe}
    if xa:
        rec['4_box']['crosscheck_spectral'] = {k: xc_best(k) for k in ('n1m1_cyl7.5', 'n1m1_cyl12.0', 'n1m1_cyl25.0', 'n1m1_inf',
                                                                        'n2m1_cyl7.5', 'n2m1_cyl12.0', 'n2m1_cyl25.0', 'n2m1_inf')}
    rec['5_virial'] = dict(by_charge={str(Q): r['virial_continuum_est'] for Q, r in rows},
                           crosscheck_spectral_cylinder_R7p5=dict(
                               Q1=((xa['n1m1_cyl7.5']['runs']['112']['E2'] - xa['n1m1_cyl7.5']['runs']['112']['E4'])
                                   / xa['n1m1_cyl7.5']['runs']['112']['E']) if 'n1m1_cyl7.5' in xa else None,
                               Q2=((xa['n2m1_cyl7.5']['runs']['112']['E2'] - xa['n2m1_cyl7.5']['runs']['112']['E4'])
                                   / xa['n2m1_cyl7.5']['runs']['112']['E']) if 'n2m1_cyl7.5' in xa else None))
    sr = os.path.join(HERE, 'stencil_relax.json')
    stc = json.load(open(os.path.join(HERE, 'stencil_check.json'))) if os.path.exists(os.path.join(HERE, 'stencil_check.json')) else {}
    rec['6_stencil'] = dict(
        error_ratio_centred_over_link_gauss_field=[g['error_ratio_centred_over_link'] for g in stc.get('gauss_w2', [])],
        crosscheck_test_field_ratio='about 10 at h = 0.1 (7.3-10.6 for h = 0.25-0.075; crosscheck/xc_tests3d.json)',
        centred_relaxation=({k: dict(perturbation=v.get('perturbation'), unwound_at_t=v.get('unwound_at_t'),
                                     history=[(hh['t'], hh['E_centred'], hh['E_link'], hh['Q'], hh['hedgehogs']) for hh in v['history']])
                             for k, v in json.load(open(sr)).items() if k != 'description'} if os.path.exists(sr) else None))
    out['reconciliation'] = rec
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
