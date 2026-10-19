"""E5 cross-check: compare the independent numbers (cc_*.json) with the original results.json.
Writes crosscheck.json and prints the agreement table."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
orig = json.load(open(os.path.join(HERE, '..', 'results.json')))
hh = json.load(open(os.path.join(HERE, 'cc_hedgehog.json')))
pi = json.load(open(os.path.join(HERE, 'cc_pi0.json')))
ch = json.load(open(os.path.join(HERE, 'cc_charges.json')))
li = json.load(open(os.path.join(HERE, 'cc_linear.json')))

cal = {c['quantity']: c for c in orig['calibration']}
cmpd = {c['quantity']: c for c in orig['comparison_with_PDG2026_ANW_parameters']}
ocal = lambda key: next(v['value'] for k, v in cal.items() if k.startswith(key))
anw, fit, am = hh['ANW'], hh['SU2_refit'], hh['massive_AN84']
pn = pi['numbers']
rows = []


def row(q, o, c, tol, target=None, tol_target=None, note=''):
    agree = abs(o - c) <= tol
    r = {'quantity': q, 'original': o, 'crosscheck': c, 'abs_diff': abs(o - c), 'agreement_tol': tol, 'agree': agree,
         'note': note}
    if target is not None:
        r['target'] = target; r['target_tol'] = tol_target
        r['crosscheck_within_target'] = abs(c - target) <= tol_target
    rows.append(r)


row('r_I0 [fm], ANW params', ocal('isoscalar charge radius'), anw['r_I0_fm'], 1e-4, 0.59, 0.01)
row('rM_I0 ANW def [fm]', ocal('isoscalar magnetic radius'), anw['rM_I0_ANWdef_fm'], 1e-4, 0.92, 0.01)
row('rM_I0 Sachs [fm]', cmpd['r_M_I0_fm']['skyrme_ANW_massless'], anw['rM_I0_Sachs_fm'], 1e-4)
row('mu_p', ocal('mu_p'), anw['mu_p'], 1e-4, 1.87, 0.02)
row('mu_n', ocal('mu_n'), anw['mu_n'], 1e-4, -1.31, 0.02)
row('mu_p/mu_n', ocal('mu_p/mu_n'), anw['mu_p_over_mu_n'], 1e-4, -1.43, 0.02)
row('g_A (ANW formula)', ocal('g_A'), anw['gA_ANW_pole_removed'], 1e-4, 0.61, 0.01)
row('g_piNN (GT)', ocal('g_piNN'), anw['g_piNN_GT'], 1e-3, 8.9, 0.05, 'tolerance +-0.05 is post hoc')
row('Gamma(pi0->gg) Nc=3 f=92.21 [eV]', ocal('Gamma(pi0->gg), N_c = 3'), pn['Nc3_f92.21'], 2e-3, 7.802, 0.234)
row('Gamma Nc=1 [eV]', ocal('Gamma(pi0->gg), N_c = 1'), pn['Nc1_f92.21'], 1e-3)
row('Gamma at f=64.5 [eV]', orig['pi0']['Gamma_at_ANW_f64.5_eV'], pn['Nc3_f64.5_ANW'], 2e-3)
row('Gamma at SU(3)-refit f [eV]', orig['pi0']['Gamma_at_own_SU3_refit_eV'], pn.get('Nc3_f_SU3_refit', float('nan')), 5e-3)
row('SU(3) refit f [MeV]', orig['pi0']['own_SU3_refit_f_MeV'], hh['SU3']['f'], 5e-3)
row('pull vs PrimEx-II [sigma]', orig['pi0']['pull_vs_PrimExII_sigma'], pn['pull_PrimExII'], 0.01)
row('pull vs PDG 2026 [sigma]', orig['pi0']['pull_vs_PDG2026_sigma'], pn['pull_PDG2026'], 0.01)
row('Nc=1 pull [sigma]', orig['pi0']['Nc1_pull_vs_PrimExII_sigma'], pn['pull_Nc1_PrimExII'], 0.05)
row('isovector slope C^2/Lambda', orig['no_target'][2]['value'], hh['massless']['C'] ** 2 / (hh['massless']['Lambda_tilde'] / (2 * 3.141592653589793 / 3)), 1e-4)
for item in orig['no_target'][2]['values_x2']:
    R = item['R_x']
    row(f'isovector <r^2>(R={R}) [x^-2]', item['r2_I1_x2'], hh['isovector_r2_cutoff_x2'][str(R)], 2e-3 * max(1, item['r2_I1_x2']))
for o_, c_ in zip(orig['enclosed_charge_massless_ANW'], hh['enclosed_massless_ANW']):
    row(f"Q_p(<{o_['R_fm']} fm) massless", o_['Q_p_inside'], c_['Q_p'], 1e-3)
    row(f"Q_n(<{o_['R_fm']} fm) massless", o_['Q_n_inside'], c_['Q_n'], 1e-3)
for o_, c_ in zip(orig['enclosed_charge_massive_AN84'], hh['enclosed_massive_AN84']):
    row(f"Q_p(<{o_['R_fm']} fm) m_pi=138", o_['Q_p_inside'], c_['Q_p'], 1e-3)
row('AN84 refit F [MeV]', orig['no_target'][3]['value'][0], hh['massive_refit']['F'], 0.01)
row('AN84 refit e', orig['no_target'][3]['value'][1], hh['massive_refit']['e'], 1e-3)
row('massive r_p [fm]', orig['no_target'][4]['value'][0], am['r_p_fm'], 1e-3)
row('massive <r^2>_n [fm^2]', orig['no_target'][4]['value'][1], am['r2_n_fm2'], 1e-3)
row('massive r_I1 [fm]', orig['no_target'][4]['value'][2], am['r_I1_fm'], 1e-3)
row('massive mu_p', cmpd['mu_p']['skyrme_AN84_massive_no_target'], am['mu_p'], 1e-3)
row('massive mu_n', cmpd['mu_n']['skyrme_AN84_massive_no_target'], am['mu_n'], 1e-3)
row('massive g_A (sphere)', cmpd['g_A']['skyrme_AN84_massive_no_target'], am['gA_sphere'], 1e-3)
hn = orig['hedgehog_numerics']
m = hh['massless']
row('M/(3 pi^2)', hn['M_over_3pi2'], m['M'] / (3 * 3.141592653589793 ** 2), 1e-7)
row('Lambda', hn['Lambda'], m['Lambda_tilde'] / (2 * 3.141592653589793 / 3), 1e-5)
row('C', hn['C'], m['C'], 1e-5)
row("F'(0)", hn['Fprime0'], m['Fprime0'], 1e-8)
row('<x^2>_B', hn['R2'], m['R2'], 1e-6)
row('<x^4>_B', hn['R4'], m['R4'], 1e-4)
row('I2 (pi/2) K2', 3.141592653589793 / 2 * hn['K2'], hh['SU3']['I_tilde']['I_44'], 1e-4)

charges_ok = (ch['all_integer'] and ch['Y1_obeys_I3_plus_half']
              and all(sorted(ch['irreps'][k]['charges'], key=lambda s: eval(s)) == sorted(orig['charges_summary'][k]['charges'], key=lambda s: eval(s))
                      for k in ('8', '10', '10bar', '27')))
for r in rows:
    flag = 'OK ' if r['agree'] else 'DIFF'
    print(f"{flag} {r['quantity']:38s} orig {r['original']:<14.7g} cc {r['crosscheck']:<14.7g} |d| {r['abs_diff']:.2e}"
          + (f"  target {r['target']} +- {r['target_tol']}: {'pass' if r['crosscheck_within_target'] else 'FAIL'}" if 'target' in r else ''))
print('charges agree with original and integral:', charges_ok)
print('linearisation: pion', li['pion_dispersion'], '; photon', li['photon']['omega'], '; mixing zero', li['pion_photon_mixing_zero'],
      '; vacuum p+rho =', li['p_plus_rho'], '; boost invariant', li['boost_invariant'])
print('pi0 Gamma/PLAN-formula =', pi['Gamma_over_PLAN_formula'], '; coefficient of eps dA A dpi:', pi['coefficient_of_eps_dA_A_dpi'])
out = {'rows': rows, 'charges_agree_and_integral': charges_ok, 'linearisation': li, 'pi0_symbolic': {k: v for k, v in pi.items() if k != 'numbers'},
       'n_rows': len(rows), 'n_agree': sum(r['agree'] for r in rows)}
json.dump(out, open(os.path.join(HERE, 'crosscheck_numbers.json'), 'w'), indent=1)
print(f"{out['n_agree']}/{out['n_rows']} numeric rows agree")

# ---------------------------------------------------------------- audit verdict (written by the cross-checker)
extra = json.load(open(os.path.join(HERE, 'cc_extra.json')))
issues = [
    {'severity': 'minor', 'description': 'REPORT Method states the pi0 coupling as (N_c e^2/48 pi^2 f) eps^{mu nu a b} d_mu A_nu A_a d_b pi0; '
     'with d_mu A_nu this is a factor 2 too small and inconsistent with the quoted amplitude N_c e^2/(12 pi^2 f). The code '
     '(symbolic_derivations.py) correctly uses (d_mu A_nu - d_nu A_mu) = F_mu nu. Cross-check derivation from B-H eq. 67: '
     'N_c e^2/(48 pi^2 f) eps F A d pi0 = N_c e^2/(24 pi^2 f) eps dA A d pi0. Numbers unaffected.',
     'suggested_fix': 'Replace d_mu A_nu by F_mu nu in the text (or use 24 pi^2).'},
    {'severity': 'minor', 'description': 'Convergence claim "X = 25, 50, 100, 200, 400 ... agree to within 5e-8 relative in Lambda" is not what '
     'hedgehog_log.txt shows: X = 25 differs by 8e-7 in Lambda, 1.2e-6 in C and B = 0.99999944. The 5e-8 spread holds for X = 100-400.',
     'suggested_fix': 'Say "X = 100-400 agree to 5e-8; X = 25 is off by ~1e-6".'},
    {'severity': 'minor', 'description': 'Summary/REPORT: "the neutron enclosed charge peaks at +0.185 at 1 fm" is a sampling artifact of the '
     f"table grid. Its true maximum is +{extra['massless_ANW']['Qn_peak']:.3f} at R = {extra['massless_ANW']['R_peak_fm']:.2f} fm "
     f"(massless ANW); massive AN84: +{extra['massive_AN84']['Qn_peak']:.3f} at {extra['massive_AN84']['R_peak_fm']:.2f} fm.",
     'suggested_fix': 'Quote the peak (+0.206 at 0.73 fm) or say "reaches +0.185 at 1 fm".'},
    {'severity': 'minor', 'description': '"38/38 symbolic checks pass" includes check 10d, hard-coded True "by inspection" (not computed), and checks 5c/7b that '
     'pass only up to an overall sign. The statements are true (the cross-check confirms them), but 38/38 overstates what was computed.',
     'suggested_fix': 'Mark 10d as an inspection, not a computed check (37 computed + 1 by inspection).'},
    {'severity': 'minor', 'description': 'Verdict vocabulary: CALIBRATED is used for internal checks with no literature target (symbolic derivations, '
     'integral charges); QUANTIFIED is used for a SEED 6B claim although PLAN reserves it for §8 gaps. The 6B paraphrase '
     '"one parameter set covers all predictions (anomaly sector included)" is the agent\'s, not SEED.md\'s wording.',
     'suggested_fix': 'Use "check passed" for internal checks; label the f_pi tension as a confirmed preregistered prediction (no SEED verdict) or AMENDED.'},
    {'severity': 'minor', 'description': 'SEED 6B AMENDED: the headline "3 of 7 within 30%" counts mu_p (-33%), mu_n (-31%), g_piNN (-32%) as failures of '
     '"roughly 30%". The amendment is really carried by g_A (-52%) and the infinite r_p, <r^2>_n in the massless model. The verdict holds; the framing overstates it.',
     'suggested_fix': 'State that 6 of 7 finite quantities are within ~33%; the exceptions are g_A and the individual charge radii.'},
    {'severity': 'minor', 'description': 'Commitment 4 CONFIRMED: the preregistered test passes (the isovector radius diverges linearly; finite with m_pi). '
     'But any extended charge distribution has an R-dependent enclosed charge, so the test does not tell "dressing" from ordinary structure, '
     'and "not slowed" holds by construction. The caveat is in the report; the verdict word is generous.',
     'suggested_fix': 'Write "CONFIRMED in the preregistered operational sense (classical pion-cloud structure, not vacuum polarization)".'},
    {'severity': 'minor', 'description': 'g_piNN is CALIBRATED only under a post hoc tolerance of +-0.05. Under the moments\' +-0.02 it would fail '
     '(|8.868 - 8.9| = 0.032). This is disclosed. The rounding-based tolerance is reasonable, and g_piNN is tied to g_A by Goldberger-Treiman, '
     'and g_A passes its preregistered tolerance.',
     'suggested_fix': 'None needed beyond the existing disclosure; optionally note it fails at +-0.02.'},
    {'severity': 'minor', 'description': 'N_c = 1 exclusion holds only with N_c-independent quark charges, which is disclosed. The report\'s own extra shows that at N_c = 1 those charges '
     'make the baryon charges fractional, so the excluded hypothesis is not a consistent N_c = 1 world. "CONFIRMED" for the WZ / pi0 claim should '
     'carry that qualifier in the verdict itself.',
     'suggested_fix': 'Verdict: "CONFIRMED (the anomaly normalisation); the N_c = 1 exclusion holds only with fixed quark charges".'},
]
out['issues'] = issues
out['overall'] = 'confirmed_with_corrections'
out['extra'] = extra
json.dump(out, open(os.path.join(HERE, 'crosscheck.json'), 'w'), indent=1)
print('wrote crosscheck.json')
