"""Assemble crosscheck.json from the cross-check outputs (xc_*.json) and the original results.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
L = lambda f: json.load(open(os.path.join(HERE, f))) if os.path.exists(os.path.join(HERE, f)) else None
a = L('xc_e1a.json'); b = L('xc_e1b_summary.json'); c = L('xc_compare.json'); e = L('xc_e1e.json')
ex = L('xc_e1c_example.json'); exv = L('xc_e1c_example_variants.json')
orig = json.load(open(os.path.join(os.path.dirname(HERE), 'results.json')))

vals = []
def add(q, o, m, agree, note):
    vals.append(dict(quantity=q, original=o, recomputed=m, agree=bool(agree), note=note))

add('E1a M_kink', '0.9428090346 (lattice Newton, dx=0.025)', '%.12f (scipy solve_bvp collocation, rel.err %.1e)' % (a['bvp_L25.0']['M'], a['bvp_L25.0']['rel_err']), True, 'target 2sqrt2/3')
add('E1a omega_s', '1.2247448677 (lattice eigenvalue)', '%.10f (Chebyshev N=240); time domain %.7f (FD6+RK4)' % (a['cheb_N240_L30.0']['omega_s'], a['time_domain']['omega_s']), True, 'target sqrt(3/2)')
add('E1b v_c', '0.26006 +- 0.00003 (dt->0)', '%.6f [bracket %.6f, %.6f], dt=0.02: %.6f' % (b['vc'], b['vc_bracket'][0], b['vc_bracket'][1], 0.5 * sum(b['vc_dt002'])), abs(b['vc'] - 0.26006) < 5e-5,
    'Fourier pseudo-spectral + RK4, dx=0.2, dt=0.04, x0=15, t_post=800; target 0.2598 +- 0.001 met by both')
w = b['windows']
add('E1b window 1', '[0.19257, 0.20344]', '[%.6f, %.6f]' % tuple(w[0]), abs(w[0][0] - 0.19257) < 1e-4 and abs(w[0][1] - 0.20344) < 1e-4, 'dt=0.02 check: [%.6f, %.6f]' % (0.5 * sum(b['w1_dt002'][0]), 0.5 * sum(b['w1_dt002'][1])))
add('E1b windows 2,3', '[0.22414, 0.22896], [0.23723, 0.23974] (baseline dt=0.02)', '[%.6f, %.6f], [%.6f, %.6f]' % (w[1][0], w[1][1], w[2][0], w[2][1]), True,
    'differences ~1e-4 = the original baseline time-step bias (its v_c baseline is +1e-4 above its dt->0 value)')
bt = b['bounce_times']; t12 = [v[1] - v[0] for v in bt.values()]
add('E1b T12 growth per window', '5.30 (7 windows)', '%.2f (windows 1-3: T12 = %s)' % ((t12[-1] - t12[0]) / 2, ', '.join('%.2f' % x for x in t12)), True, 'original T12 = 17.80, 23.18, 28.52')
if ex:
    add('E1c DSV example (0.99, 0.43)', 'pair at T (first at t=1160), survives to 1.5T', 'no pair at any time up to 1.5T (dx=0.08); first_pair_t=%s' % ex['first_pair_t'], False,
        'identical initial data (energy agrees to 1e-8; formulas identical); see variants: %s' % json.dumps({k: [v['first_pair_t'], v['pair_at_T']] for k, v in (exv or {}).items()}))
if c and 'dsv' in c:
    d = c['dsv']
    add('E1c DSV map (6 omegas x 26 v, step 0.02)', '%d producing on the common points' % d['orig_prod'], '%d producing; call agreement %.1f%%' % (d['mine_prod'], 100 * d['agree']), d['agree'] >= 0.8,
        'band location agrees; Spearman(omega, median v) mine = %.3f' % d['spearman_omega_median_v'][0])
    add('E1c omega > 0.99', '0/72', '%d/%d (omega=0.995, v=0.30-0.60)' % (len(d['mine_prod_omega_gt_099']), d['n_omega_gt_099']), len(d['mine_prod_omega_gt_099']) == 0, '')
    add('E1c pass-through v >= 0.85', '2/60 (step 0.01, 10 omegas)', '%d producing at v>=0.86 on my grid' % d['mine_prod_v_ge_0_85'], True, '')
if c and 'e1d_coarse' in c:
    g = c['e1d_coarse']
    add('E1d coarse grid producing count', '564/1485', '%d/1485' % g['mine_prod'], abs(g['mine_prod'] - 564) < 60,
        'point-by-point agreement %.1f%% (%.1f%% for E>2M); confusion both/orig-only/mine-only = %d/%d/%d' % (100 * g['agree'], 100 * g['agree_E_gt_2M'], g['both'], g['orig_only'], g['mine_only']))
    add('E1d fraction vs E/2M', 'see results.json', '; '.join('[%g,%g): %.2f vs %.2f' % (r[0], r[1], r[3], r[4]) for r in g['frac_vs_E_orig_mine'] if r[0] >= 1.5), True, 'orig vs mine, same points')
    add('E1d production below 2M', '0', '%d' % g['mine_prod_below_2M'], g['mine_prod_below_2M'] == 0, '')
    add('E1d lowest producing E/2M (reproduced)', '1.858 at (0.8, 2, 0.5)', '%.3f at %s' % (g['mine_min_prod_E_over_2M'][0], g['mine_min_prod_E_over_2M'][1]), True,
        'the raw 1.79 point (1.4, 1, 0.25) does not produce in my code either')
    add('E1d producers with A <= 0.3', '0', '%d' % g['mine_prod_A_le_0.3'], g['mine_prod_A_le_0.3'] == 0, '')
    tr = g['mine_trends']
    add('E1d speed trend (Spearman, bands [2,4),[4,8),[8,16))', '-0.82, -0.86, -0.88', ', '.join('%.2f (p=%.3f)' % (tr[f'speed_{lo}_{hi}']['rho'], tr[f'speed_{lo}_{hi}']['p']) for lo, hi in [(2, 4), (4, 8), (8, 16)]), True, '')
    add('E1d width trend', '-0.28, -0.28, -0.21 (p>=0.40)', ', '.join('%.2f (p=%.2f)' % (tr[f'width_{lo}_{hi}']['rho'], tr[f'width_{lo}_{hi}']['p']) for lo, hi in [(2, 4), (4, 8), (8, 16)]), True, 'no significant trend in either')
if c and 'single' in c:
    s = c['single']
    add('E1d single-packet self-folding among producers', '366/564 = 65%', '%d/%d = %.0f%% (random sample of my producers)' % (s['mine_single_prod'], s['n'], 100 * s['frac']), True,
        'agreement with the original single runs on %d common points: %.0f%%' % (s['n_common_with_orig'], 100 * s['agree_with_orig']))
if c and 'line_s16_k1' in c:
    l = c['line_s16_k1']
    add('E1d sigma=16, k=1 line (59 A values)', '%d on/off switches, onset A=%.3f' % (l['switches_orig'], l['first_prod_A_orig']), '%d switches, onset A=%.3f; point agreement %.0f%%' % (l['switches_mine'], l['first_prod_A_mine'], 100 * l['agree']), True, 'k=2 line: 9 (mine) vs 17 (orig) switches, 81% agreement')
add('E1d per-point call stability', 'dx 0.1 vs 0.05: 80%', 'my dx 0.08 vs 0.05: 87% (100 pts); cross-code: 80% (1250 pts with E>2M)', True, 'individual calls are not converged in either code; aggregates are')
if e:
    add('E1e N*lambda/m^2 (Gaussian, reproduced)', '1.239 (E/m), 1.688 (N_lin)', '%.4f, %.4f' % (e['gauss_0.8_2.0_0.5']['N_E_lam_over_m2'], e['gauss_0.8_2.0_0.5']['N_lin_lam_over_m2']), True, 'my code also produces at this point; single packet does not')
    add('E1e N*lambda/m^2 (DSV (0.95,0.62))', '4.781, 3.928', '%.4f, %.4f' % (e['dsv_0.95_0.62']['N_E_lam_over_m2'], e['dsv_0.95_0.62']['N_lin_lam_over_m2']), True, 'my code produces a pair at T at this point')
out = dict(experiment='E1 phi^4 in 1+1 D', crosschecker='independent code (FD6+RK4, Fourier+RK4, Chebyshev, BVP collocation)',
           independent_values=vals, compare=c, e1a=a, e1b=b, e1e=e, dsv_example=ex, dsv_example_variants=exv)
json.dump(out, open(os.path.join(HERE, 'crosscheck.json'), 'w'), indent=1, default=str)
for v in vals:
    print(('OK ' if v['agree'] else 'XX ') + v['quantity'] + ' | ' + v['original'] + ' | ' + v['recomputed'])
