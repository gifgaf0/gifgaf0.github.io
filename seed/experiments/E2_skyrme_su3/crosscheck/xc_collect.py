"""Cross-check E2, step 6: compare my numbers with the original's OUTPUTS (results.json, out/rotor.json,
out/hedgehog.json, out/derrick.json) and write crosscheck.json.  Reads no original code.
Run after xc_derive.py, xc_hedgehog.py, xc_densities.py, xc_rotor.py, xc_axial.py.
"""
import json, math

D = '/home/user/gifgaf0.github.io/seed/experiments/E2_skyrme_su3/'
X = D + 'crosscheck/'
L = lambda p: json.load(open(p))
res = L(D + 'results.json'); rot = L(D + 'out/rotor.json'); hh = L(D + 'out/hedgehog.json')['reference_halfline_N160']
dv = L(D + 'out/derrick.json')
mh = L(X + 'xc_hedgehog.json'); mr = L(X + 'xc_rotor.json'); md = L(X + 'xc_densities.json'); ma = L(X + 'xc_axial.json')
mdv = L(X + 'xc_derive.json')
oA = rot['parameter_sets']['ANW_SU2_fit']; oR = rot['parameter_sets']['SU3_refit_PDG_centres']
A = mr['ANW']; R = mr['SU3refit']
rows = []


def cmp(q, orig, mine, tol, note='', kind='rel'):
    if kind == 'rel':
        dev = abs(mine/orig - 1)
    else:
        dev = abs(mine - orig)
    rows.append(dict(quantity=q, original=orig, recomputed=mine, deviation=dev, tolerance=tol,
                     agree=bool(dev <= tol), note=note))


cmp('M_cl [F_pi/e]', hh['M_over_Fpi_e'], mh['M'], 1e-9, 'shooting (DOP853) vs Chebyshev collocation')
cmp('M_cl / (3 pi^2 F_pi/e)', hh['M_over_3pi2'], mh['M_over_3pi2'], 1e-9)
cmp('Lambda', hh['Lambda'], mh['Lambda'], 1e-9, 'tail C^2/X from asymptotic series in both')
cmp('I1 coefficient (2pi/3)Lambda', hh['I1_coef'], mh['I1_coef'], 1e-9)
cmp('J2', hh['J2'], mh['J2'], 1e-9, 'my first attempt had a 1-cos F underflow bug (-4.7e-5); fixed, see CROSSCHECK.md')
cmp('I2 coefficient (pi/2)J2', hh['I2_coef'], mh['I2_coef'], 1e-9)
cmp('I1/I2', hh['I1_over_I2'], mh['I1_over_I2'], 1e-9)
cmp('C (F -> C/x^2)', hh['C'], mh['C'], 1e-8, "original's C is the less precise one (its own D/(-2C)-1 = 7e-10)")
cmp("F'(0)", hh['Fp0'], mh['Fprime0'], 1e-10)
cmp('D (ANW g_A bracket)', hh['D_gA'], mh['D'], 1e-9)
cmp('<r^2>_B (eF)^2', hh['r2B'], mh['r2B'], 1e-10)
cmp('virial E2/E4 - 1', hh['virial_dev'], mh['virial'], 1e-9, 'both numerical zero', kind='abs')
cmp('E2 = E4 [F_pi/e]', dv['E2'], mh['E2'], 1e-10)
cmp('von Laue int x^2 p dx (abs)', dv['von_Laue_integral'], mh['vonLaue_int'], 1e-10, 'both numerical zero', kind='abs')
cmp('pressure node x', dv['pressure_nodes_x'][0], mh['pressure_node_x'], 5e-4,
    'original = midpoint of the grid interval with the sign change (2.15221); root 2.15237', kind='abs')
cmp('p(0) [(F/e)(eF)^3]', dv['p0'], mh['p0'], 1e-3)
cmp('Derrick: max |E2(mu) mu/E2 - 1|', dv['scaling_max_rel_dev'], mh['derrick_dev'], 1e-12, kind='abs')
cmp('arctan-ansatz I2 coefficient', 40.5435, mh['arctan']['I2_coef'], 1e-5, 'Praszalowicz eq. 28, x0 = sqrt(15/4) [read]')
cmp('ANW fit F_pi [MeV]', oA['F_pi'], A['Fpi'], 1e-9)
cmp('ANW fit e', oA['e'], A['e'], 1e-9)
cmp('g_A at ANW fit (-(pi/3e^2) D)', oA['gA_SU2'], A['gA_SU2'], 1e-8, 'also = far-field (Goldberger-Treiman) 2piC/(3e^2), derived independently')
cmp('g_A ball integral at ANW fit', 2/3*oA['gA_SU2'], ma['gA_ball_ANWfit'] if ma['gA_ball_ANWfit'] > 0 else -ma['gA_ball_ANWfit'], 1e-4,
    'my Noether current from the Lagrangian, ball R = 24')
cmp('1/I2 at ANW fit [MeV]', oA['invI2'], A['invI2'], 1e-9)
cmp('E(8) - E_SU2(N) = 3/(4I2) at ANW [MeV]', oA['E8_minus_EN_SU2'], A['E8_minus_ESU2N'], 1e-9)
cmp('r_B rms at ANW [fm]', res['extras']['r_baryon_rms_fm_ANW']['value'], mh['ANW']['r_rms_fm'], 1e-9)
cmp('ANW set E(8) [MeV]', oA['E8'], A['levels'][0][2], 1e-9)
cmp('ANW set E(10) [MeV]', oA['E10'], A['levels'][1][2], 1e-9)
cmp('ANW set E(10bar) [MeV]', oA['E10bar'], A['levels'][2][2], 1e-9)
cmp('PDG 2026 octet centre [MeV]', rot['pdg']['octet_centre_MeV'], mr['octet_centre'], 1e-12)
cmp('PDG 2026 decuplet centre [MeV]', rot['pdg']['decuplet_centre_MeV'], mr['decuplet_centre'], 1e-12)
cmp('SU(3) refit F_pi [MeV]', oR['F_pi'], R['Fpi'], 1e-9)
cmp('SU(3) refit e', oR['e'], R['e'], 1e-9)
cmp('SU(3) refit M_cl [MeV]', oR['M_cl'], R['Mcl'], 1e-9)
cmp('SU(3) refit E(10bar) [MeV]', oR['E10bar'], R['levels'][2][2], 1e-9)
cmp('SU(3) refit E(27, J=3/2) [MeV]', 1786.0, R['levels'][3][2], 0.5, 'report rounds to 1786', kind='abs')
cmp('SU(3) refit g_A (SU(2) form)', oR['gA_SU2'], R['gA_SU2'], 1e-8)
cmp('SU(3) refit g_A x 7/10', oR['gA_SU3_symmetric'], R['gA_SU2']*mr['gA_SU3_factor'], 1e-8)
cmp('|<p up|D33|p up>| SU(3) octet', 7/30, abs(mr['D33_SU3']['s=E13']), 1e-12, 'exact Weingarten integral vs CG intertwiners')
so = rot['optional_symmetry_breaking']
cmp('optional fit alpha [MeV]', so['alpha_MeV'], mr['breaking_fit']['alpha'], 1e-9)
cmp('optional fit beta [MeV]', so['beta_MeV'], mr['breaking_fit']['beta'], 1e-9)
cmp('optional fit rms [MeV]', so['rms_MeV'], mr['breaking_fit']['rms'], 1e-9)
cmp('Guadagnini LHS-RHS (PDG 2026) [MeV]', res['headline'][-1]['value'], mr['guadagnini'], 1e-9)
for X_, lam_o in zip(['10.0', '20.0', '40.0'], [37.09, 44.11, 47.59]):
    cmp('Dirichlet box X=%s, no tail: Lambda' % X_[:-2], lam_o, ma['dirichlet'][X_]['Lambda'], 0.006, 'report quotes 2 decimals', kind='abs')

exact = {
    'lowest Y_R=1 multiplets 8(1/2),10(3/2),10bar(1/2),27(3/2),35(5/2),27(1/2)':
        [a + ' J=' + b for a, b, _ in mr['lowest']['3'][:6]],
    'E(10)-E(8)': mr['level_differences']['E10-E8'], 'E(10bar)-E(8)': mr['level_differences']['E10bar-E8'],
    'E(8)-E_SU2(N)': mr['level_differences']['E8-ESU2(N)'],
    'N_c parity 2J = N_c mod 2 (N_c = 1..15)': all(v['parity_ok'] for v in mr['parity'].values()),
    'N_c = 1..7 lowest four': {k: [a + ' J=' + b for a, b, _ in v[:4]] for k, v in mr['lowest'].items() if int(k) <= 7},
    'densities from the Lagrangian (eps, i_11, i_44, i_88, T_ij)': md['worst'],
    'asymptotic series -C^3/(21x^6) - (4/3)C^3/x^8': mdv['asym_report_ok'],
    'D = -2C (total derivative, symbolic)': mdv['D_total_derivative'],
}
allagree = all(r['agree'] for r in rows)
allchecks = all([mh['all_pass'], mr['all_pass'], md['all_pass'], ma['all_pass']])
issues = [
    dict(severity='minor', description='Verdict vocabulary: N_c parity, Derrick, virial and von Laue are labelled CALIBRATED in '
         'results.json/REPORT headline tables; PLAN reserves CALIBRATED for literature targets. N_c parity is a preregistered seed '
         'prediction (CONFIRMED, conditional on the imported Y_R = N_c B/3 rule); E(10)-E(8), E(10bar)-E(8), the ordering at both '
         'parameter sets and "e is the only pure number" are identities / dimensional analysis, true by construction.',
         fix='Relabel N_c parity as CONFIRMED (given the imported WZ rule) and the identities as checks; keep the numbers.'),
    dict(severity='minor', description='The corrected reading of the 30% claim ("most static properties land within about 30%") '
         'is not demonstrated in E2: the only non-fit nucleon observable E2 computes is g_A (-52%); the fitted F_pi (-30.5%) is a fit '
         'parameter. The AMENDED verdict itself is supported by g_A.',
         fix='Keep AMENDED on the g_A evidence; mark the "most static properties" clause provisional until E5.'),
    dict(severity='minor', description='Target provenance: "36.5 F_pi/e = 1.2315 x 3pi^2" does not appear in the cited [read] texts. '
         'Schechter-Weigel hep-ph/9907554 gives E = 23.2 pi f_pi/e (= 36.44 F_pi/e) and alpha^2 = 53.3/(e^3 f_pi) (-> Lambda = 50.90); '
         'Praszalowicz hep-ph/0308114 has only the arctan-ansatz formulas (eqs. 26-28, I2 coefficient 40.54 at x0 = sqrt(15/4)). '
         '36.5 is ANW\'s own number. Calibration passes against SW\'s 36.44 as well (+0.05%). ANW F_pi = 129 (f_pi = 64.5), e = 5.45, '
         'g_A = 0.61 are readable in Acus et al. hep-ph/9605435 Table 1 (ANW column).',
         fix='State the provenance as SW 23.2 pi f_pi/e and 53.3/(e^3 f_pi) [read]; upgrade ANW numbers to [read: Acus Table 1].'),
    dict(severity='minor', description='The I2 calibration compares the exact profile with a variational (arctan-ansatz) value, not a '
         'published exact-profile I2; it only bounds formula slips above 1.5%. The I2 density itself is independently verified '
         '(original: explicit SU(3) matrices; here: finite differences of the PLAN Lagrangian, 7e-11).',
         fix='Say in the table that the target is an ansatz value; no verdict change.'),
    dict(severity='minor', description='collect_results.py hard-codes CALIBRATED for the multiplet ordering, exact level differences, '
         'Derrick and N_c parity; the ordering of the lowest multiplets is printed by su3_rotor.py but not asserted by any check. '
         'Values are correct (independently reproduced), but a regression would not flip these verdicts.',
         fix='Derive these verdicts from asserted checks.'),
    dict(severity='minor', description='PDG 2026 g_A/g_V is -1.2753 +- 0.0013 (pdg 2026.0: -1.275335); the report quotes 1.2754 '
         '(the PDG 2024 value). The -52% conclusion is unchanged.', fix='Quote 1.2753(13).'),
    dict(severity='minor', description='N_c table naming: (p,q) = (1,3) is written "24" at N_c = 4 and N_c = 7, but by the report\'s own '
         'convention (6bar = (0,2), 15bar = (1,2)) it is 24bar; results.json says "24=(1,3)".', fix='Write 24bar (1,3).'),
    dict(severity='minor', description='Small numeric slips: pressure node 2.1522 in results.json is a grid-interval midpoint (root '
         '2.15237; the report\'s 2.152 is fine); the asymptotic residuals "6e-7, 2e-9, 5e-10" are relative and the x = 40 value is '
         'solver noise (series remainder ~5e-12); "E2 = E4 to 6e-13" vs "4e-13" in different places; the report\'s "-2C = '
         '-17.2771564357" is not the results.json C (-2C = -17.2771564286; that C is good to 4.5e-10).', fix='Cosmetic.'),
]
out = dict(experiment='E2 cross-check (independent recomputation)', issues=issues, all_numbers_agree=allagree, all_my_checks_pass=allchecks,
           comparisons=rows, exact_results=exact,
           my_scripts=['xc_derive.py', 'xc_hedgehog.py', 'xc_densities.py', 'xc_rotor.py', 'xc_axial.py', 'xc_collect.py'],
           overall='confirmed_with_corrections')
json.dump(out, open(X + 'crosscheck.json', 'w'), indent=1, default=float)
for r in rows:
    print('%-45s orig %-22.12g mine %-22.12g dev %.1e  %s' % (r['quantity'], r['original'], r['recomputed'], r['deviation'],
                                                            'OK' if r['agree'] else 'DISAGREE'))
print('all numbers agree:', allagree, '  all my checks pass:', allchecks)
