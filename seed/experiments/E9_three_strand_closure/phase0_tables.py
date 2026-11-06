"""Read-only post-processing of phase0_results.json into the tables of REPORT_phase0.md. Run: python3 phase0_tables.py"""
import json, math

R = json.load(open('phase0_results.json'))
fmt = lambda v, p=3: '—' if v is None or (isinstance(v, float) and not math.isfinite(v)) else f'{v:.{p}f}'

print('| point | β | δ | μ² | λ | m²_vac | m_vac | C3 | βS−(1+η) | solves | in window | k_max | q_max at k=0 | q capped (k rows) | not conv. | box-affected (r_σ>12) | min 𝒯/ℰ (k, q) | 𝒯 sign change | verdict |')
print('|' + '---|' * 19)
for p in R['points']:
    s = p['summary']; c3 = R['C3'][p['tag']]
    if 'solves' not in p:
        print(f"| {p['tag']} | {p['beta']:g} | {p['delta']:g} | {p['mu2']:.3f} | {p['lam']:.3f} | {p['m2_vac']:.3f} | — | FAIL | — | — | — | — | — | — | — | — | — | — | {s['verdict']} |"); continue
    am = s['argmin_Tcal_over_E']
    print(f"| {p['tag']} | {p['beta']:g} | {p['delta']:g} | {p['mu2']:.3f} | {p['lam']:.3f} | {p['m2_vac']:.3f} | {p['m_vac']:.3f} | "
          f"{'PASS' if c3['passed'] else 'FAIL'} | {c3['betaS_minus_1_plus_eta']:+.3f} | {s['n_solves']} | {s['n_in_window']} | "
          f"{fmt(s['k_max_in_window'], 2)} | {s['q_max_in_window_by_k'].get('0.00')} | {len(s['q_capped_at_k'])} | {s['n_not_converged']} | "
          f"{s['n_box_affected_in_window']} | {s['min_Tcal_over_E']:.4f} ({am['k']:.2f}, {am['q']:.2f}) | "
          f"{'y (' + str(len(s['sign_changes'])) + ')' if s['sign_changes'] else 'n'} | {s['verdict_label']} |")

print('\nSign changes')
print('| point | between | k* | q* | ω*/m_vac | r_σ* | n | R_eq | Q | R_eq/r_σ | d²E/dR² (h=0.03) | (h=0.06) | direct-solve check | flags |')
print('|' + '---|' * 14)
for p in R['points']:
    for c in p['summary'].get('sign_changes', []):
        d = c['d2E_dR2_interp']
        print(f"| {p['tag']} | {c['between']} | {c['k_star']:.4f} | {c['q_star']:.3f} | {c['omega_star_over_mvac']:.4f} | {fmt(c['r_sigma_star'], 2)} | "
              f"{c['n']} | {fmt(c['R_eq'], 2)} | {fmt(c['Q'], 1)} | {fmt(c['R_eq_over_r_sigma'], 2)}{' (unreliable)' if c['thin_ring_unreliable'] else ''} | "
              f"{fmt(d['h=0.03'], 4)} | {fmt(d['h=0.06'], 4)} | {fmt(c.get('d2E_dR2_direct'), 4)} | {'; '.join(c['flags'])}{'; box-affected endpoint' if c['box_affected_endpoint'] else ''} |")

print('\nCrude §1.3 estimate vs exact')
print('| point | T(0,0) | I_c | T/I_c | (μ²−ε₀)+2m²_vac | crude feasible | verdict | crude/exact 𝒯 sign agreement |')
print('|' + '---|' * 8)
for p in R['points']:
    if 'crude' not in p: continue
    c = p['crude']; s = p['summary']
    print(f"| {p['tag']} | {s['T00']:.3f} | {s['I00']:.3f} | {c['T_over_Ic']:.3f} | {c['limit']:.3f} | {'y' if c['crude_feasible'] else 'n'} | "
          f"{s['verdict']} | {c['sign_agreement']['agree']}/{c['sign_agreement']['total']} |")

print('\nNon-converged solves')
for p in R['points']:
    for o in p.get('solves', []):
        if not o['success']:
            print(f"- {p['tag']} k={o['k']:.2f} q={o['q']:.2f}: {o['message']}, nit={o['nit']}, max|grad|={o['grad_max']:.1e}, in_window={o['in_window']}, sigma0={o['sigma0']:.3g}")

print('\nVirial cross-check: max |Tcal_fd - (G+2B-2k^2 I)| / E over in-window points with central differences')
for p in R['points']:
    w = [o for o in p.get('solves', []) if o['in_window'] and o.get('Tcal') is not None and not any('one-sided' in f for f in o['Tcal_flags'])]
    if w:
        print(f"- {p['tag']}: fd vs virial {max(abs(o['Tcal'] - o['Tcal_virial']) / o['E'] for o in w):.2e}, "
              f"fd vs envelope {max(abs(o['Tcal'] - o['Tcal_envelope']) / o['E'] for o in w):.2e}, n={len(w)}")
print('\nselection:', json.dumps(R['selection']))
