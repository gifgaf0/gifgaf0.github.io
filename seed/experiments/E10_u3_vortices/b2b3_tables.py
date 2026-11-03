"""Read-only tables for REPORT_B2B3.md from b2_results.json, b3_results.json, b3_compare2d.json.
Run: python3 b2b3_tables.py > log_tables.txt"""
import json, numpy as np

b2 = json.load(open('b2_results.json'))
print('== B2 ==')
for lam, e in b2['lambdas'].items():
    c = e['checks']
    print(f"lam={lam}: C1 {c['C1']['value']:.6f} (target {c['C1']['target']}, rel {c['C1']['rel_dev']:+.2e}); "
          f"C2 {c['C2']['value']:.6f} (target {c['C2']['target']}, rel {c['C2']['rel_dev']:+.2e}); "
          f"C3 {c['C3']['value']:.9f} (dev {c['C3']['abs_dev']:+.1e}); C4 {c['C4']['value']:.8f} (rel {c['C4']['rel_dev']:+.1e}); "
          f"I(2D) {c['C5C6']['I']:.5f}; I(radial dr=0.05) {e['radial']['elementary']['I_over_pi']:.5f}")
    for n, r in e['radial'].items():
        print(f"   radial {n}: T/2pi {r['T_over_2pi']:.6f} flux {r['flux_TrB']:.6f} I(pi/4) {r['I_alpha_pi4']:.6f} {r['message']}")
    for n, r in e['lattice'].items():
        print(f"   lattice {n}: T/2pi {r['T_over_2pi']:.6f} flux {r['flux_TrB']:.9f} nit {r['nit']} grad {r['grad_max']:.1e} {r['message']} {r['seconds']:.0f}s")
    print('   decay 2D', e['decay_2d'], ' radial', e['radial']['elementary']['decay'])
    print('   inertia rows', [(r['omega'], round(r['E_rot_over_omega2'], 7), round(r['I'], 7), r['cg_iters']) for r in e['inertia_2d']['rows']],
          'T_rotated', e['inertia_2d']['T_rotated'])
for k, o in b2.get('convergence', {}).items():
    print(f"conv {k}: T/2pi {o['T_over_2pi']:.7f} I {o['inertia_2d']['I_extrapolated']:.6f} {o['message']} nit {o['nit']}")

try:
    cmp = json.load(open('b3_compare2d.json'))
    print('== 2D vs radial ==')
    print(json.dumps({k: v for k, v in cmp.items() if k != 'meta'}, indent=1, default=float))
except FileNotFoundError:
    pass

b3 = json.load(open('b3_results.json'))
print('== B3 ==')
for L in b3['lambdas']:
    s = L['summary']; sol = L['solves']; mb = L['m_bulk']
    win = [o for o in sol if o['in_window']]
    print(f"\nlam={L['lam']} m_bulk={mb}: solves {s['n_solves']}, in window {s['n_in_window']}, not converged {s['n_not_converged']}, "
          f"verdict {s['verdict']}, sign changes {len(s['sign_changes'])}, min T/E {s['min_Tcal_over_E']:.4f} at {s['argmin_Tcal_over_E']}, "
          f"max|Tfd-Tenv|/E {s['max_abs_Tcal_fd_minus_env_over_E']:.1e}, I0 {s['I0_static_alpha_pi4']:.6f} T0 {s['T0_static']:.6f}, q capped {s['q_capped_at_k']}")
    print(' k   | q_max in window | closed by (q, omega/m, leak) | min Tcal in row (q) | min Tcal_frozen | alpha at q_max | I at q_max | iter max')
    for kk in sorted({o['k'] for o in sol}):
        row = [o for o in sol if o['k'] == kk]
        rw = [o for o in row if o['in_window']]
        last = row[-1]
        mt = min(((o['Tcal'], o['q']) for o in rw if o.get('Tcal') is not None), default=(None, None))
        mf = min((o['Tcal_frozen'] for o in rw), default=None)
        top = rw[-1] if rw else None
        print(f" {kk:.2f} | {top['q'] if top else None} | ({last['q']:.1f}, {last['omega_over_mbulk']:.4f}, {last['leak']:.1e}) | "
              f"{mt[0] if mt[0] is None else round(mt[0], 4)} ({mt[1]}) | {None if mf is None else round(mf, 4)} | "
              f"{None if top is None else round(top['alpha_mod'], 4)} | {None if top is None else round(top['I'], 4)} | {max(o['nit'] for o in row)}")
    for c in s['sign_changes']:
        print('  sign change', json.dumps(c, default=float))
    k0 = [o for o in sol if o['k'] == 0]
    print('  k=0 row (q, E, T, I, omega/m, alpha, Tcal, Tcal_env, Tcal_frozen, r_core, r_q_rms, leak):')
    for o in k0[::5] + [k0[-1]]:
        print(f"   {o['q']:.1f} {o['E']:.6f} {o['T']:.6f} {o['I']:.6f} {o['omega_over_mbulk']:.4f} {o['alpha_mod']:.4f} "
              f"{o.get('Tcal')} {o.get('Tcal_envelope')} {o['Tcal_frozen']:.4f} {o['r_core']:.4f} {o['r_charge_rms']:.4f} {o['leak']:.1e}")
    bad = [o for o in sol if not o['success']]
    print(f'  not converged: {len(bad)}; iteration cap hit: {sum(o["iter_cap_hit"] for o in sol)}')
    for o in bad:
        print(f"   k={o['k']:.2f} q={o['q']:.1f}: {o['message']} nit={o['nit']} grad_max={o['grad_max']:.1e} in_window={o['in_window']}")
