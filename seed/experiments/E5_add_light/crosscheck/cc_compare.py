"""E5 cross-check: compare the independent numbers (cc_*.json, cc_new.json) with the original results.json
as it stands now (after the original's reconciliation pass).  Writes crosscheck_numbers.json and prints the
agreement table.  The audit (issues, claim verdicts) is written by cc_audit.py."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
orig = json.load(open(os.path.join(HERE, '..', 'results.json')))
hh = json.load(open(os.path.join(HERE, 'cc_hedgehog.json')))
pi = json.load(open(os.path.join(HERE, 'cc_pi0.json')))
ch = json.load(open(os.path.join(HERE, 'cc_charges.json')))
li = json.load(open(os.path.join(HERE, 'cc_linear.json')))
nw = json.load(open(os.path.join(HERE, 'cc_new.json')))
ex = json.load(open(os.path.join(HERE, 'cc_extra.json')))
PI = 3.141592653589793

cal = {c['quantity']: c for c in orig['calibration']}
cmpd = {c['quantity']: c for c in orig['comparison_with_PDG2026_ANW_parameters']}


def ocal(key):
    return next(v['value'] for k, v in cal.items() if k.startswith(key))


anw, fit, am = hh['ANW'], hh['SU2_refit'], hh['massive_AN84']
fe = nw['fe_ANW']
pn = pi['numbers']
rows = []


def row(q, o, c, tol, target=None, tol_target=None, method='', note=''):
    agree = abs(o - c) <= tol
    r = {'quantity': q, 'original': o, 'crosscheck': c, 'abs_diff': abs(o - c), 'agreement_tol': tol, 'agree': agree,
         'method': method, 'note': note}
    if target is not None:
        r['target'] = target
        r['target_tol'] = tol_target
        r['crosscheck_within_target'] = abs(c - target) <= tol_target
        r['original_within_target'] = abs(o - target) <= tol_target
    rows.append(r)


N = 'Noether currents of the matrix Lagrangian on a shooting profile'
FE = 'finite-element energy minimisation profile + textbook integrals'
# ---- calibrations, two independent cross-check methods each where possible
row('r_I0 [fm], ANW params', ocal('isoscalar charge radius'), anw['r_I0_fm'], 1e-4, 0.59, 0.01, N)
row('r_I0 [fm], ANW params (FE)', ocal('isoscalar charge radius'), fe['r_I0_fm'], 1e-4, 0.59, 0.01, FE)
row('rM_I0 ANW def [fm]', ocal('isoscalar magnetic radius'), anw['rM_I0_ANWdef_fm'], 1e-4, 0.92, 0.01, N)
row('rM_I0 ANW def [fm] (FE)', ocal('isoscalar magnetic radius'), fe['rM_ANW_fm'], 1e-4, 0.92, 0.01, FE)
row('rM_I0 Sachs [fm]', cmpd['r_M_I0_fm']['skyrme_ANW_massless'], anw['rM_I0_Sachs_fm'], 1e-4, method=N)
row('mu_p', ocal('mu_p'), anw['mu_p'], 1e-4, 1.87, 0.02, N)
row('mu_p (FE)', ocal('mu_p'), fe['mu_p'], 1e-4, 1.87, 0.02, FE)
row('mu_n', ocal('mu_n'), anw['mu_n'], 1e-4, -1.31, 0.02, N)
row('mu_n (FE)', ocal('mu_n'), fe['mu_n'], 1e-4, -1.31, 0.02, FE)
row('mu_p/mu_n', ocal('mu_p/mu_n'), anw['mu_p_over_mu_n'], 1e-4, -1.43, 0.02, N)
row('g_A (ANW, pion pole removed)', ocal('g_A'), anw['gA_ANW_pole_removed'], 1e-4, 0.61, 0.01, N + ' (axial sphere integral x 3/2)')
row('g_A (surface term 2 pi C/3e^2, FE)', ocal('g_A'), fe['g_A'], 1e-4, 0.61, 0.01, FE)
row('g_piNN (GT)', ocal('g_piNN'), anw['g_piNN_GT'], 1e-3, 8.9, 0.05, N, 'tolerance +-0.05 is post hoc; fails +-0.02')
row('Gamma(pi0->gg) Nc=3 f=92.21 [eV]', ocal('Gamma(pi0->gg), N_c = 3'), pn['Nc3_f92.21'], 2e-3, 7.802, 0.234,
    'sympy plane-wave amplitude from B-H eq. 67')
row('Gamma Nc=3 f=92.21 [eV] (textbook A)', ocal('Gamma(pi0->gg), N_c = 3'), nw['pi0_textbook']['Nc3_f92.21'], 2e-3, 7.802, 0.234,
    'A = N_c alpha/(3 pi f), Gamma = A^2 m^3/(64 pi)')
row('Gamma Nc=1 [eV]', ocal('Gamma(pi0->gg), N_c = 1'), pn['Nc1_f92.21'], 1e-3)
row('Gamma at f=64.5 [eV]', orig['pi0']['Gamma_at_ANW_f64.5_eV'], pn['Nc3_f64.5_ANW'], 2e-3)
row('Gamma at SU(3)-refit f [eV]', orig['pi0']['Gamma_at_own_SU3_refit_eV'], pn['Nc3_f_SU3_refit'], 5e-3)
row('Gamma at own SU(2)-fit f [eV]', orig['pi0']['Gamma_at_own_SU2_fit_eV'], pn['Nc3_f_SU2_refit'], 5e-3)
row('SU(3) refit f [MeV]', orig['pi0']['own_SU3_refit_f_MeV'], hh['SU3']['f'], 5e-3, note='cc uses 1151.19/1382.11 exactly')
row('pull vs PrimEx-II [sigma]', orig['pi0']['pull_vs_PrimExII_sigma'], pn['pull_PrimExII'], 0.01)
row('pull vs PDG 2026 [sigma]', orig['pi0']['pull_vs_PDG2026_sigma'], pn['pull_PDG2026'], 0.01)
row('Nc=1 pull [sigma]', orig['pi0']['Nc1_pull_vs_PrimExII_sigma'], pn['pull_Nc1_PrimExII'], 0.05)
row('f needed for PrimEx-II central [MeV]', orig['pi0']['f_needed_for_PrimExII_central_MeV'], pn['f_for_PrimExII_central'], 1e-3)
row('PDG 2026 Gamma(gg) [eV]', orig['pi0']['inputs']['PDG2026']['Gamma_gg_eV'], nw['data_side']['Gamma_gg_eV'], 1e-3)
# ---- own SU(2) refit
row('own SU(2) refit F [MeV]', 129.263, fit['F_pi'], 2e-3, note='original value from hedgehog_log.txt (129.263)')
row('own SU(2) refit e', 5.4440, fit['e'], 2e-4, note='original value from hedgehog_log.txt (5.4440)')
row('mu_p at own SU(2) refit', 1.8788, fit['mu_p'], 1e-4)
row('mu_n at own SU(2) refit', -1.3260, fit['mu_n'], 1e-4)
row('g_A at own SU(2) refit', 0.61047, fit['gA_ANW_pole_removed'], 1e-5)
# ---- dressing
row('isovector slope C^2/Lambda', orig['no_target'][2]['value'],
    hh['massless']['C'] ** 2 / (hh['massless']['Lambda_tilde'] / (2 * PI / 3)), 1e-4)
row('isovector slope C^2/Lambda (FE)', orig['no_target'][2]['value'], fe['isovector_slope_C2_over_Lambda'], 1e-4, method=FE)
for item in orig['no_target'][2]['values_x2']:
    R = item['R_x']
    row(f'isovector <r^2>(R={R}) [x^-2]', item['r2_I1_x2'], hh['isovector_r2_cutoff_x2'][str(R)], 2e-3 * max(1, item['r2_I1_x2']))
for o_, c_ in zip(orig['enclosed_charge_massless_ANW'], hh['enclosed_massless_ANW']):
    row(f"Q_p(<{o_['R_fm']} fm) massless", o_['Q_p_inside'], c_['Q_p'], 1e-3)
    row(f"Q_n(<{o_['R_fm']} fm) massless", o_['Q_n_inside'], c_['Q_n'], 1e-3)
for o_, c_ in zip(orig['isovector_tail_check'], hh['enclosed_massless_ANW']):
    row(f"isovector charge outside {o_['R_fm']} fm", o_['isovector_outside'], c_['ivec_outside'], 1e-4)
for o_, c_ in zip(orig['enclosed_charge_massive_AN84'], hh['enclosed_massive_AN84']):
    row(f"Q_p(<{o_['R_fm']} fm) m_pi=138", o_['Q_p_inside'], c_['Q_p'], 1e-3)
    row(f"Q_n(<{o_['R_fm']} fm) m_pi=138", o_['Q_n_inside'], c_['Q_n'], 1e-3)
pk = orig['neutron_enclosed_charge_peak']
row('neutron Q_n peak, massless ANW', pk['massless_ANW']['Q_n_peak'], ex['massless_ANW']['Qn_peak'], 1e-4)
row('neutron Q_n peak radius [fm], massless ANW', pk['massless_ANW']['R_peak_fm'], ex['massless_ANW']['R_peak_fm'], 1e-3)
row('neutron Q_n peak, massive AN84', pk['massive_AN84']['Q_n_peak'], ex['massive_AN84']['Qn_peak'], 1e-4)
row('neutron Q_n peak radius [fm], massive AN84', pk['massive_AN84']['R_peak_fm'], ex['massive_AN84']['R_peak_fm'], 1e-3)
# ---- massive variant
row('AN84 refit F [MeV]', orig['no_target'][3]['value'][0], hh['massive_refit']['F'], 0.01)
row('AN84 refit e', orig['no_target'][3]['value'][1], hh['massive_refit']['e'], 1e-3)
row('massive r_p [fm]', orig['no_target'][4]['value'][0], am['r_p_fm'], 1e-3)
row('massive <r^2>_n [fm^2]', orig['no_target'][4]['value'][1], am['r2_n_fm2'], 1e-3)
row('massive r_I1 [fm]', orig['no_target'][4]['value'][2], am['r_I1_fm'], 1e-3)
row('massive mu_p', cmpd['mu_p']['skyrme_AN84_massive_no_target'], am['mu_p'], 1e-3)
row('massive mu_n', cmpd['mu_n']['skyrme_AN84_massive_no_target'], am['mu_n'], 1e-3)
row('massive g_A (sphere)', cmpd['g_A']['skyrme_AN84_massive_no_target'], am['gA_sphere'], 1e-3)
row('massive r_I0 [fm]', cmpd['r_E_I0_fm']['skyrme_AN84_massive_no_target'], am['r_I0_fm'], 1e-3)
# ---- hedgehog numerics, three solvers
hn = orig['hedgehog_numerics']
m = hh['massless']
fr = nw['fe_profile']['richardson']
row('M/(3 pi^2) (shooting)', hn['M_over_3pi2'], m['M'] / (3 * PI ** 2), 1e-7)
row('M/(3 pi^2) (FE minimisation)', hn['M_over_3pi2'], fr['M_over_3pi2'], 1e-7, method=FE)
row('Lambda (shooting)', hn['Lambda'], m['Lambda_tilde'] / (2 * PI / 3), 1e-5)
row('Lambda (FE minimisation)', hn['Lambda'], fr['Lambda'], 2e-5, method=FE)
row('C (shooting)', hn['C'], m['C'], 1e-5)
row('C (FE minimisation)', hn['C'], fr['C'], 1e-5, method=FE)
row("F'(0) (shooting)", hn['Fprime0'], m['Fprime0'], 1e-8)
row("F'(0) (FE minimisation)", hn['Fprime0'], fr['Fprime0'], 1e-6, method=FE)
row('<x^2>_B (shooting)', hn['R2'], m['R2'], 1e-6)
row('<x^2>_B (FE minimisation)', hn['R2'], fr['R2'], 1e-6, method=FE)
row('<x^4>_B (shooting)', hn['R4'], m['R4'], 1e-4)
row('<x^4>_B (FE minimisation)', hn['R4'], fr['R4'], 1e-4, method=FE)
row('I2 tilde = (pi/2) K2', PI / 2 * hn['K2'], hh['SU3']['I_tilde']['I_44'], 1e-4, method='3x3 embedded matrix Lagrangian, lambda_4 rotation')
row('D = -2C check: G33 vs 2 pi C/3', 2 * PI * hn['C'] / 3, m['G33'], 1e-6, method='Noether axial current sphere integral')
# ---- data side
ds = nw['data_side']
row('PDG isoscalar charge radius [fm]', cmpd['r_E_I0_fm']['data'], ds['rE_I0_fm'], 1e-5)
row('PDG isoscalar magnetic radius [fm]', cmpd['r_M_I0_fm']['data'], ds['rM_I0_fm'], 1e-5)
row('within 30% count (of 7 finite)', orig['within_30pct']['n_within'], ds['n_within_30'], 0)
row('within 33% count (of 7 finite)', orig['within_30pct']['n_within_33pct'], ds['n_within_33'], 0)

charges_ok = (ch['all_integer'] and ch['Y1_obeys_I3_plus_half']
              and all(sorted(ch['irreps'][k]['charges'], key=lambda s: eval(s)) ==
                      sorted(orig['charges_summary'][k]['charges'], key=lambda s: eval(s)) for k in ('8', '10', '10bar', '27')))
nc_ok = all(r['Q_consistent'] == o['nonstrange_charges_anomaly_consistent'] and r['Q_fixed'] == o['nonstrange_charges_fixed_quark_charges']
            for r, o in zip(nw['charges_Nc'], orig['charges_Nc_extra']['rows']))
for r in rows:
    flag = 'OK  ' if r['agree'] else 'DIFF'
    print(f"{flag} {r['quantity']:44s} orig {r['original']:<14.8g} cc {r['crosscheck']:<14.8g} |d| {r['abs_diff']:.1e}"
          + (f"  target {r['target']}+-{r['target_tol']}: {'pass' if r['crosscheck_within_target'] else 'FAIL'}" if 'target' in r else ''))
print('charges (8, 10, 10bar, 27) agree with original and integral:', charges_ok, '; N_c table (fixed and anomaly-consistent) agrees:', nc_ok)
print('WZ A-linear charge per unit N_c:', nw['WZ_charge_per_Nc'])
print('linearisation: pion', li['pion_dispersion'], '; photon', li['photon']['omega'], '; ranks', li['photon']['ranks'],
      '; mixing zero', li['pion_photon_mixing_zero'], '; vacuum p+rho =', li['p_plus_rho'], '; boost invariant', li['boost_invariant'])
print('pi0 Gamma/PLAN-formula =', pi['Gamma_over_PLAN_formula'], '; coefficient of eps dA A dpi:', pi['coefficient_of_eps_dA_A_dpi'])
out = {'rows': rows, 'charges_agree_and_integral': charges_ok, 'Nc_charge_table_agrees': nc_ok, 'linearisation': li,
       'pi0_symbolic': {k: v for k, v in pi.items() if k != 'numbers'}, 'WZ_charge_per_Nc': nw['WZ_charge_per_Nc'],
       'n_rows': len(rows), 'n_agree': sum(r['agree'] for r in rows),
       'n_calibration_rows_crosscheck_within_target': sum(r.get('crosscheck_within_target', False) for r in rows),
       'n_calibration_rows': sum('target' in r for r in rows)}
json.dump(out, open(os.path.join(HERE, 'crosscheck_numbers.json'), 'w'), indent=1)
print(f"{out['n_agree']}/{out['n_rows']} numeric rows agree; calibration rows within target (cross-check value): "
      f"{out['n_calibration_rows_crosscheck_within_target']}/{out['n_calibration_rows']}")
