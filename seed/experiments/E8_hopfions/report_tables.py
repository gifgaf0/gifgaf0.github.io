"""
report_tables.py -- print the Markdown tables used in the E8 report from results.json,
analysis_raw.json and axial2d.json (no computation).
Usage: python3 report_tables.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'results.json')))
AX = json.load(open(os.path.join(HERE, 'axial2d.json'))) if os.path.exists(os.path.join(HERE, 'axial2d.json')) else None
PRETTY = {'A1,1': 'A₁,₁', 'A2,1': 'A₂,₁', 'A~3,1': 'Ã₃,₁ (bent)', 'A2,2': 'A₂,₂', 'L11_12': 'L^{1,1}_{1,2}', 'L11_22': 'L^{1,1}_{2,2}',
          'K32': 'K₃,₂ (trefoil)'}

pc = R['per_charge']
print('| Q | type found | type target | E (dx=0.1) | target | dev | E/E₁ | target | dev | Q measured (all dx) | verdicts (E / ratio / type / Q) |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for q in sorted(pc, key=int):
    r = pc[q]
    qs = ', '.join(f'{v:.3f}' for v in r['Q_by_h'].values())
    E = r.get('E_h01'); dev = r.get('E_rel_dev_h01')
    rat = r.get('E_over_E1_h01'); rt = r.get('E_over_E1_target'); rd = r.get('ratio_rel_dev')
    if E is None:
        print(f"| {q} | {PRETTY.get(r.get('type_found'), r.get('type_found'))} (dx={r['h_finest']:.3g}) | {PRETTY[r['type_target']]} | not reached | {r['E_target']} | | | | | {qs} | |")
        continue
    print(f"| {q} | {PRETTY.get(r.get('type_found'), r.get('type_found'))} | {PRETTY[r['type_target']]} | "
          f"{E:.4f} | {r['E_target']} | {100 * dev:+.2f}% | "
          + (f"{rat:.4f} | {rt:.4f} | {100 * rd:+.2f}% | " if (rat is not None and int(q) > 1) else "1 | 1 | – | ")
          + f"{qs} | {r.get('verdict_E')} / {r.get('verdict_ratio') if int(q) > 1 else '–'} / {r.get('verdict_type')} / {r['verdict_Q']} |")
print()
print('| Q | E(0.2) | E(0.15) | E(0.125) | E(0.1) | dx→0 estimate (box 7.5) | spread | E/Q^{3/4} (0.1) | E/(Q E₁) (0.1) | 0.534 Q^{3/4} |')
print('|---|---|---|---|---|---|---|---|---|---|')
for q in sorted(pc, key=int):
    r = pc[q]
    Eh = r['E_by_h']
    g = lambda k: f"{Eh[k]:.4f}" if k in Eh else '–'
    ce = r.get('E_continuum_est'); sp = r.get('E_continuum_spread')
    print(f"| {q} | {g('0.2000')} | {g('0.1500')} | {g('0.1250')} | {g('0.1000')} | "
          f"{(f'{ce:.4f}' if ce else '–')} | {(f'{sp:.4f}' if sp else '–')} | {r.get('E_over_Q34_h01', float('nan')):.4f} | "
          f"{r.get('E_over_QE1_h01', float('nan')):.4f} | {r['proven_bound']:.3f} |")
print()
print('virial (E2-E4)/E by dx:')
for q in sorted(pc, key=int):
    print(q, {k: round(v, 4) for k, v in pc[q]['virial_by_h'].items()}, 'converged', pc[q]['converged_by_h'],
          'flow t', {k: round(v, 1) for k, v in pc[q]['flow_time_by_h'].items()},
          'wall', {k: (round(v) if v is not None else None) for k, v in pc[q]['wall_s_by_h'].items()})
print()
print('type details (finest):')
for q in sorted(pc, key=int):
    d = pc[q].get('type_details_finest', {})
    print(q, pc[q].get('type_found_by_N'), 'ncomp', d.get('n_position'), 'alex', d.get('alexander'), 'lk', d.get('lk_position_position'),
          'Qlink', d.get('Q_from_linking'), 'twist', d.get('twist_per_component'), 'slice', d.get('slice_degrees'),
          'asym', round(d.get('inertia_axial_asym', float('nan')), 4),
          'shapes', [(round(s['out_of_plane_rms_over_radius'], 3), round(s['radius_std_over_mean'], 3), round(s['mean_radius'], 2), round(s['length'], 2)) for s in d.get('loop_shapes', [])],
          'tube', d.get('tube_components'), 'curve info', d.get('pos_info'))
print()
print('box study:', json.dumps(R['box_study'], indent=1))
print('seed claims:', json.dumps(R['seed_claims'], indent=1))
if AX:
    print('axial2d:', json.dumps({k: AX[k] for k in AX if k != 'relaxed'}, indent=1))
    for k, v in AX.get('relaxed', {}).items():
        print(k, round(v['E'], 6), v['iters'], v['msg'][:40], round(v.get('wall_s', 0)))
