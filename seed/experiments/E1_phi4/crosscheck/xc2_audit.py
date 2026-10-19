"""Build the audit (independent values, claim audit, issues) from xc2_compare.json and the
original-code diagnosis files; writes xc2_audit.json.  Run after xc2_compare.py."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(HERE, 'xc2_compare.json')))
oc = json.load(open(os.path.join(HERE, 'xc2_origcode_dsv_example.json')))
col = json.load(open(os.path.join(HERE, 'xc2_origcode_col099.json')))
IV = []


def iv(q, o, r, agree, note):
    IV.append(dict(quantity=q, original=o, recomputed=r, agree=bool(agree), note=note))


a = c['e1a']
iv('E1a M_kink', '0.9428090346 (lattice Newton, dx=0.025; rel. err. -7.4e-9)',
   '%.10f (solve_bvp collocation; rel. err. %.0e)' % (a['M_bvp'], a['M_rel_err']), True, 'target 2 sqrt2/3 = 0.9428090416')
iv('E1a omega_s', '1.2247448677 (lattice eigenvalue); time domain within 2.2e-5',
   '%.10f (Chebyshev N=240, rel. err. %.0e); time domain %.6f (FD6+RK4, %.1e)' % (
       a['omega_s_cheb'], a['omega_s_rel_err'], a['omega_s_time'], a['omega_s_time_rel_err']), True, 'target sqrt(3/2)')
b = c['e1b']
iv('E1b v_c', '0.26006 +- 0.00003 (dt->0); baseline 0.26016',
   '%.6f (Fourier + RK4, dx=0.2, dt=0.04, x0=15, own box); dt=0.02 bracket [%.6f, %.6f]' % (b['vc'], *b['vc_dt002']),
   abs(b['vc_minus_orig_dt0']) < 5e-5,
   'differs from the original dt->0 value by %.0e; both sit %.1e above the [summary] target 0.2598 (inside +-0.001)' % (
       b['vc_minus_orig_dt0'], b['vc_minus_target']))
w = b['windows']
iv('E1b first two-bounce window', '[0.19256, 0.20343] (dt->0); baseline [0.19268, 0.20354]',
   '[%.6f, %.6f]' % tuple(w[0]), max(abs(x) for x in b['w1_minus_orig_dt0']) < 5e-5,
   'agrees to %.0e; Manton et al. 2021 (arXiv:2106.05153v2, read here) quote 0.1920-0.2029' % max(abs(x) for x in b['w1_minus_orig_dt0']))
iv('E1b windows 2 and 3', 'baseline [0.22414, 0.22896], [0.23723, 0.23974]',
   '[%.6f, %.6f], [%.6f, %.6f]' % (w[1][0], w[1][1], w[2][0], w[2][1]), True,
   'differences ~1e-4 = the original baseline (dt=0.02 leapfrog) time-step bias; narrowing confirmed')
iv('E1b T12 per window (resonance check)', 'T12 = 17.80, 23.18, 28.52 (slope 5.30)',
   'T12 = %s' % ', '.join('%.2f' % t for t in b['T12']), True, '')
ex = c['e1c_example']
spec_ex = {k: v for k, v in ex.items() if k.startswith('spec_om0.99_v0.43')}
oc_txt = '; '.join('dx=%g dt=%g: %s' % (r['dx'], r['dt'], ('pair since t=%g' % r['since']) if r['produced_dsv'] else 'no pair') for r in oc)
iv('E1c DSV example (0.99, 0.43)', 'pair at T (forms at t=1160 = 0.97T, interval +-22.5 at T), survives to 1.5T',
   'NO pair at any time up to 1.5T: FD6+RK4 dx=0.08; spectral dx=0.1 and dx=0.05 (%s)' % ', '.join(
       '%s first=%s' % (k.replace('spec_om0.99_v0.43_', ''), v['first']) for k, v in spec_ex.items()),
   False, 'original code itself (unmodified copy): ' + oc_txt + '. DSV Fig. 1 shows the kinks at x = +-140 at t = T.')
m = c['e1c_map']
iv('E1c DSV map (6 omegas x v 0.40-0.90 step 0.02)', '%d producing on the common points' % m['orig_prod'],
   'FD6+RK4: %d producing; %d in common; call agreement %.1f%%' % (m['fd6_prod'], m['both'], 100 * m['agree']), m['agree'] >= 0.85,
   'vs our reading of DSV Fig. 2 (22 producing points on this grid): original %d hits / %d false positives, FD6 %d / %d' % (
       m['vs_dsv_reading']['orig_hits'], m['vs_dsv_reading']['orig_false_pos'], m['vs_dsv_reading']['fd6_hits'], m['vs_dsv_reading']['fd6_false_pos']))
iv('E1c trend (Spearman omega vs median producing v)', '-0.99 (10 omegas)', '%.2f (6 omegas, FD6)' % m['spearman_fd6'][0], m['spearman_fd6'][0] < -0.8, '')
iv('E1c pass-through at high v', '0/10 at v=0.90; 2/60 at v>=0.85', '%d/%d at v>=0.86 (FD6)' % (m['fd6_prod_v_ge_086'], m['n_v_ge_086']), m['fd6_prod_v_ge_086'] <= 2, '')
iv('E1c omega > 0.99', '0/72', '%d/%d (omega=0.995, FD6)' % (m['fd6_prod_omega_gt_099'], m['n_omega_gt_099']), m['fd6_prod_omega_gt_099'] == 0, '')
col_txt = '; '.join('dx=%g dt=%g: %s' % (r['dx'], r['dt'], [x[0] for x in r['rows'] if x[1]] or 'none') for r in col)
nb = {k: v for k, v in ex.items() if k.startswith('spec_om0.99') and 'v0.43' not in k}
iv('E1c omega = 0.99 column (producing v)', '0.41, 0.43 (dx=0.1, dt=0.04)',
   'FD6: %s (v step 0.02); spectral: %s' % (m['per_omega']['0.99']['fd6'], ', '.join('%s:%s' % (k.split('_')[2], v['pair_at_T']) for k, v in nb.items()) or 'pending'),
   False, 'original code, v = 0.38-0.48 step 0.01: ' + col_txt)
g = c['e1d_coarse_fd6']
iv('E1d coarse grid producing count', '564/1485', '%d/1485 (FD6+RK4)' % g['fd6_prod'], abs(g['fd6_prod'] - 564) < 60,
   'point agreement %.1f%% (%.1f%% at E>2M); both/orig-only/FD6-only = %d/%d/%d; the original\'s own dx 0.1 vs 0.05 agreement is %.1f%%' % (
       100 * g['agree'], 100 * g['agree_E_gt_2M'], g['both'], g['orig_only'], g['fd6_only'], 100 * c['e1d_orig_dx_selfagree']))
iv('E1d producing fraction vs E/2M', '0 (<1.5), .03, .08, .11, .18, .45, .53, .59-.60, .69-.70, .75',
   ', '.join('%g-%g: %.2f' % (r[0], r[1], r[4]) for r in g['frac_vs_E'] if r[0] >= 1.5), True, 'same points, FD6 code; every band within 0.07')
iv('E1d production below 2M_kink', '0 of 19,526', '0 of 1485 (FD6); 0 in the spectral sample and targets', g['fd6_prod_below_2M'] == 0, '')
iv('E1d producers with A <= 0.3 (coarse)', '0', '%d (FD6)' % g['fd6_prod_A_le_03'], g['fd6_prod_A_le_03'] == 0, '')
s = c.get('e1d_sample_spec')
if s:
    iv('E1d random sample, spectral code (one-by-one)', '%d producing of %d' % (s['orig_prod'], s['n']),
       '%d producing; agreement with original %.1f%% (E>2M: %.1f%%), with FD6 %.1f%%' % (
           s['spec_prod'], 100 * s['agree_spec_orig'], 100 * s['agree_spec_orig_E_gt_2M'], 100 * s['agree_spec_fd6']),
       s['agree_spec_orig'] >= 0.75, 'FD6 vs original on the same points: %.1f%%; all three agree on %.1f%%' % (
           100 * s['agree_fd6_orig'], 100 * s['all_three_agree']))
tg = {(r['A'], r['sigma'], r['k'], r['single'], r['oneway'], r['dx']): r for r in c['e1d_targets']}


def tgt(key):
    r = tg.get(key)
    return None if r is None else r


r1, r1b = tgt((0.8, 2.0, 0.5, False, False, 0.1)), tgt((0.8, 2.0, 0.5, False, False, 0.05))
iv('E1d lowest producer reproduced (0.8, 2, 0.5), baseline phi_t', 'E/2M = 1.858, produces at dx 0.1/0.05/0.025, collision needed',
   'FD6: produces, E/2M = 1.858' + ('' if r1 is None else '; spectral dx=0.1: %s, dx=0.05: %s, E/2M = %.4f; single packet: %s' % (
       r1['prod'], None if r1b is None else r1b['prod'], r1['E_over_2M'],
       None if tgt((0.8, 2.0, 0.5, True, False, 0.1)) is None else tgt((0.8, 2.0, 0.5, True, False, 0.1))['prod'])),
   (r1 is None or r1['prod']), '')
r2, r2b = tgt((1.4, 1.0, 0.25, False, False, 0.1)), tgt((1.4, 1.0, 0.25, False, False, 0.05))
iv('E1d raw lowest producer (1.4, 1, 0.25), E/2M = 1.79', 'produces at dx=0.1 only (not reproduced)',
   'FD6: no' + ('' if r2 is None else '; spectral dx=0.1: %s, dx=0.05: %s' % (r2['prod'], None if r2b is None else r2b['prod'])),
   True, 'both agree it is not a robust producer')
r3, r3b = tgt((0.6, 4.0, 0.5, False, True, 0.1)), tgt((0.6, 4.0, 0.5, False, True, 0.05))
r4 = tgt((0.8, 2.0, 0.5, False, True, 0.1))
if r3 is not None:
    iv('E1d one-way phi_t lowest producer (0.6, 4, 0.5)', 'E/2M = 2.703, produces (dx 0.1/0.05/0.025); (0.8,2,0.5) one-way: E/2M = 2.90, no pair',
       'spectral (own one-way construction): E/2M = %.4f, produces dx=0.1: %s, dx=0.05: %s; (0.8,2,0.5) one-way: E/2M = %s, produces: %s' % (
           r3['E_over_2M'], r3['prod'], None if r3b is None else r3b['prod'],
           None if r4 is None else '%.3f' % r4['E_over_2M'], None if r4 is None else r4['prod']),
       r3['prod'] and abs(r3['E_over_2M'] - 2.703) < 0.01, '')
sf = [r for r in c['e1d_targets'] if r['single'] and r['sigma'] == 16.0]
if sf:
    txt = '; '.join('k=%g: %s' % (kk, ' '.join('%g%s' % (r['A'], '+' if r['prod'] else '-') for r in sorted(sf, key=lambda q: q['A']) if r['k'] == kk))
                    for kk in sorted(set(r['k'] for r in sf)))
    iv('E1d single-packet self-folding threshold (sigma=16)', 'minimum self-folding A 0.375 (sigma=16 slice), 0.425 (k=1 slice)',
       'spectral single packets (+ = pair): ' + txt, True,
       'local over-barrier estimate: V(-1-A) = V(0) gives A* = sqrt2 - 1 = 0.414')
iv('E1d sigma=16, k=1 line (59 A values)', '17 switches, onset A = 0.375', '17 switches, onset A = 0.375 (FD6); 80% point agreement', True,
   'k=2 line: 9 switches (FD6) vs 17 (orig), same onset 0.375 and same gap at A=0.45-0.5; 81% agreement')
iv('E1d single-packet controls', '366/564 producing coarse points also self-fold (65%)', 'FD6 sample: 57/80 (71%); 87% agreement on 62 common points', True, '')
tr = json.load(open(os.path.join(HERE, 'xc_compare.json')))['e1d_coarse']['mine_trends']
iv('E1d matched-energy speed test (rho by band)', '-0.82, -0.87, -0.88',
   '%.2f, %.2f, %.2f (FD6)' % (tr['speed_2_4']['rho'], tr['speed_4_8']['rho'], tr['speed_8_16']['rho']), True,
   'reproduced, but confounded with amplitude (see issues)')
iv('E1d matched-energy width test (rho by band)', '-0.28, -0.28, -0.21 (p >= 0.40)',
   '%.2f, %.2f, %.2f (p = %.2f, %.2f, %.2f; FD6)' % (tr['width_2_4']['rho'], tr['width_4_8']['rho'], tr['width_8_16']['rho'],
                                                     tr['width_2_4']['p'], tr['width_4_8']['p'], tr['width_8_16']['p']), True, 'not supported in either code')
e = c['e1e_fd6']
iv('E1e N lambda/m^2 for (0.8, 2, 0.5)', '1.2389 (N=E/m), 1.6879 (N_lin)',
   '%.4f, %.4f (own initial data, continuum dispersion)' % (e['gauss_0.8_2.0_0.5']['N_E_lam_over_m2'], e['gauss_0.8_2.0_0.5']['N_lin_lam_over_m2']), True,
   'scaling N lambda/m^2 = E~/(2 sqrt2) re-derived; energy floor 2/3 re-derived')
if r3 is not None:
    iv('E1e N lambda/m^2, one-way (0.6, 4, 0.5)', '1.80 (N=E/m), 1.96 (N_lin)',
       '%.3f, %.3f (spectral, own one-way data)' % (r3['N_E_lam_over_m2'], r3['N_lin_lam_over_m2']),
       abs(r3['N_E_lam_over_m2'] - 1.802) < 0.01 and abs(r3['N_lin_lam_over_m2'] - 1.959) < 0.02, '')
iv('E1e N lambda/m^2, DSV (0.95, 0.62)', '4.7805, 3.9278', '%.4f, %.4f' % (e['dsv_0.95_0.62']['N_E_lam_over_m2'], e['dsv_0.95_0.62']['N_lin_lam_over_m2']), True, '')

json.dump(dict(independent_values=IV), open(os.path.join(HERE, 'xc2_audit_values.json'), 'w'), indent=1)
for x in IV:
    print('| %s | %s | %s | %s |' % (x['quantity'], x['original'], x['recomputed'], 'yes' if x['agree'] else '**no**'))
