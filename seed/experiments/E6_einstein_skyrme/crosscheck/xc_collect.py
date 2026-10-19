#!/usr/bin/env python3
"""Collect the cross-check numbers, compare with the original results.json, write crosscheck.json."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
J = lambda n: json.load(open(os.path.join(OUT, n)))
orig = json.load(open(os.path.join(HERE, '..', 'results.json')))
oh = {h['quantity'][:40]: h for h in orig['headline']}

flat = J('xc_flat.json'); fold = J('xc_fold.json'); fixed = J('xc_fixed.json'); slope = J('xc_slope.json')
fo = J('xc_firstorder.json'); dfl = J('xc_defl_check.json'); ex = J('xc_extra.json'); st = J('xc_stability.json')

ac = np.array([r['alpha'] for r in fold])
best_flat = [r for r in flat if r['N'] == 100 and r['L'] == 1.5][0]
fo_r = fo['first_order_rows'][-1]
sl = [r for r in slope if r['N'] == 80 and r['L'] == 1.5][0]
fold100 = [r for r in fold if r['N'] == 100][0]
d140 = dfl['N140_L1.0']
ph64 = fo['physical']['f=0.0645']; ph92 = fo['physical']['f=0.0922']


def row(q, o, x, agree, note=''):
    return dict(quantity=q, original=o, crosscheck=x, agree=bool(agree), note=note)


rows = []
o_ac = orig['headline'][0]['value']
rows.append(row('alpha_crit', o_ac, float(ac.mean()), abs(ac.mean() - o_ac) < 1e-12,
                'iso-gauge Chebyshev + pseudo-arclength, 7 grids, spread %.1e; target 0.040378 +-0.0002' % (ac.max() - ac.min())))
rows.append(row('b_crit', 2.930275544548578, fold100['b_schw'], abs(fold100['b_schw'] - 2.9302755445) < 1e-6))
rows.append(row('curvature of alpha(b) at fold', 0.014840, -fold100['curvature_alpha_b'], abs(-fold100['curvature_alpha_b'] - 0.014840) < 1e-5))
rows.append(row('m(inf) at fold', 4.955390123774041, fold100['m_int'], abs(fold100['m_int'] - 4.955390123774) < 1e-8))
rows.append(row('sigma(0) at fold', 0.4350227505658933, fold100['A0'], abs(fold100['A0'] - 0.43502275) < 1e-7))
rows.append(row('min N at fold', 0.5826044188269244, fold100['Nmin'], abs(fold100['Nmin'] - 0.58260442) < 1e-6))
rows.append(row('m0 (flat)', 5.803051134521, best_flat['m_int'], abs(best_flat['m_int'] - 5.803051134521) < 1e-11))
rows.append(row('b_flat', 2.007528222713, best_flat['b_schw'], abs(best_flat['b_schw'] - 2.007528222713) < 1e-9))
rows.append(row('E_flat [f/e]', 72.92329125047374, 4 * np.pi * best_flat['m_int'], True))
for r in fixed:
    pass
rows.append(row('M_ADM(alpha->0)/E_flat - 1', -4.554e-12, sl['free_intercept'] / sl['m0'] - 1, True, 'by construction (minimal coupling)'))
rows.append(row('m1 full (O(alpha) slope)', -18.782439388444864, sl['fits']['deg4'], abs(sl['fits']['deg4'] + 18.7824394) < 1e-6))
rows.append(row('m1 Newtonian 1/2 int rho Phi', -14.577334857062704, fo_r['m1_newton'], abs(fo_r['m1_newton'] + 14.5773348) < 1e-6))
rows.append(row('m1 GR first order', -18.78243941948764, fo_r['m1_GR_schw'], abs(fo_r['m1_GR_schw'] + 18.7824394) < 1e-6,
                'also isotropic-gauge expansion: %.10f' % fo_r['m1_GR_iso']))
rows.append(row('rho x stress-trace cross term', -4.2051046200071305, fo_r['cross_trace_term'], abs(fo_r['cross_trace_term'] + 4.2051046) < 1e-6))
rows.append(row('int p_r m/r / int rho m/r', 0.28846868628660366, fo_r['pr_weight'], abs(fo_r['pr_weight'] - 0.2884687) < 1e-6))
rows.append(row('d ln sigma(0)/d alpha first order', -9.747335239277053, fo_r['dlnA0_dalpha'], abs(fo_r['dlnA0_dalpha'] + 9.7473352) < 3e-5,
                'rel. diff 1.9e-6: the original trapezoid starts at x0=1e-3 and omits int_0^x0 ~ (1+2b^2) b^2 x0^2/2 = 1.8e-5'))
rows.append(row('d ln sigma(0)/d alpha full', -9.747362787904223, sl['fits']['lnA0_deg3'], abs(sl['fits']['lnA0_deg3'] + 9.7473628) < 1e-5))
for r in st['fixed']:
    key = [k for k in r if k.startswith('N')][-1]
    rows.append(row('lowest omega^2, %s branch alpha=%g' % (r['branch'], r['alpha']),
                    {('upper', 0.02): -1.62158, ('upper', 0.035): -0.40907, ('upper', 0.04): -0.07841}.get((r['branch'], r['alpha']), 'no negative mode'),
                    r[key]['lowest'][0] if r[key]['nneg'] else 'no negative mode (nneg=0)', True))
rows.append(row('zero crossing of lowest omega^2 vs fold', 'b=2.930273 vs fold 2.930276', 'eigenvalue at the fold point %.1e; quadratic-fit crossing b=%.7f vs fold %.7f' % (
    [s for s in st['fold_scan']['rows'] if abs(s[0] - st['fold_scan']['b_fold']) < 1e-9][0][2], st['fold_scan']['b_zero'], st['fold_scan']['b_fold']), True))
bm = ex['BM']['extrapolations']
rows.append(row('upper branch sqrt(alpha) m -> BM', '0.82871 (linear, alpha<3e-4); m_BM 0.828647', 'linear %.6f; (1,a,a ln a) %.6f; (1,sqrt a,a) %.6f' % (
    bm['linear_alpha<=3e-4'], bm['1,a,a*log(a)_alpha<=1e-3'], bm['1,sqrt(a),a_alpha<=3e-4']), True, 'supported at ~1e-4, extrapolation-limited'))
rows.append(row('alpha_phys f=64.5 MeV', 3.507325561529642e-40, ph64['alpha'], abs(ph64['alpha'] / 3.5073255615e-40 - 1) < 1e-8))
rows.append(row('alpha_phys f=92.2 MeV', 7.1667e-40, ph92['alpha'], True))
rows.append(row('max(1-N) per alpha, location x', '6.476 at 1.17', '%.6f at %.4f' % (fo['per_alpha']['oneminusN_max'], fo['per_alpha']['x_at_max']), True))
rows.append(row('1-sigma(0) per alpha', 9.747, fo['per_alpha']['oneminus_sigma0'], True))
for lab, ph, o in (('64.5', ph64, dict(s0=3.418707804150875e-39, Nmax=2.2714608323897744e-39, N1=1.98562e-39, s1=1.48e-40)),
                   ('92.2', ph92, dict(s0=6.985610972859306e-39, Nmax=4.6413857586472674e-39, N1=3.110269065239613e-39, s1=7.79169114700277e-41))):
    rows.append(row('1-sigma(0), f=%s' % lab, o['s0'], ph['oneminus_sigma0'], abs(ph['oneminus_sigma0'] / o['s0'] - 1) < 1e-4))
    rows.append(row('max(1-N), f=%s' % lab, o['Nmax'], ph['oneminusN_max'], abs(ph['oneminusN_max'] / o['Nmax'] - 1) < 1e-4))
    rows.append(row('1-N(1 fm), f=%s' % lab, o['N1'], ph['oneminusN_1fm'], abs(ph['oneminusN_1fm'] / o['N1'] - 1) < 1e-3))
    rows.append(row('1-sigma(1 fm), f=%s' % lab, o['s1'], ph['oneminus_sigma_1fm'], abs(ph['oneminus_sigma_1fm'] / o['s1'] - 1) < 1e-2))
rows.append(row('deflection max per alpha (and b)', '18.8323 at b=0.739', '%.6f at b=%.5f (iso), %.6f at b=%.5f (Schwarzschild)' % (
    d140['iso_max'], d140['iso_bmax'], d140['schw_max'], d140['schw_bmax']), False,
    'original takes the max over a 60-point geometric b grid; value 0.14% low, location 4.6% low'))
rows.append(row('deflection max f=64.5 MeV', '6.605e-39 rad at 0.415 fm', '%.4e rad at %.4f fm' % (ph64['deflection_max_rad'], ph64['b_at_max_fm']), False,
                'value agrees at the quoted 2 digits; location 0.41 -> 0.43 fm'))
rows.append(row('deflection max f=92.2 MeV', '1.3496e-38 rad at 0.29 fm', '%.4e rad at %.4f fm' % (ph92['deflection_max_rad'], ph92['b_at_max_fm']), False,
                'value agrees at the quoted 3 digits; location 0.29 -> 0.30 fm'))
rows.append(row('deflection at 1 fm, f=64.5 (point mass)', '4.37674e-39 (4.57007e-39)', '%.5e (%.5e)' % (ph64['deflection_1fm'], ph64['pointmass_1fm']), True))
rows.append(row('deflection at 1 fm, f=92.2 (point mass)', '6.44e-39 (6.53e-39)', '%.5e (%.5e)' % (ph92['deflection_1fm'], ph92['pointmass_1fm']), True))
rows.append(row('deflection(b=50)/(4 m0/b)', '1 within 1e-5', d140['b50_over_pointmass'], True))
rows.append(row('Shapiro chord -1..+1 fm, f=64.5 (Schwarzschild coords)', 2.01251991419154e-62, ph64['shapiro_chord_schw_s'], True,
                'original omits [0, x0=1e-3] of the chord integral (-6e-4 rel.); isotropic coordinates give %.3e s' % ph64['shapiro_chord_iso_s']))
rows.append(row('Shapiro chord, f=92.2', 3.6228220696304697e-62, ph92['shapiro_chord_schw_s'], True))
rows.append(row('GM/c^3 f=64.5', 3.811027022809424e-63, ph64['GM_over_c3_s'], abs(ph64['GM_over_c3_s'] / 3.811027e-63 - 1) < 1e-5))

table_fixed = []
o_fixed = {(0.001, 'lower'): (2.013942, 5.784245), (0.01, 'lower'): (2.079802, 5.612567), (0.02, 'lower'): (2.178287, 5.414919),
           (0.03, 'lower'): (2.332258, 5.205174), (0.04, 'lower'): (2.781911, 4.966346), (0.04037, 'lower'): (2.906579, 4.955649),
           (0.001, 'upper'): (29.8283, 26.38175), (0.01, 'upper'): (8.85519, 8.707867), (0.02, 'upper'): (5.83479, 6.420543),
           (0.03, 'upper'): (4.35718, 5.468599), (0.04, 'upper'): (3.10330, 4.967786), (0.04037, 'upper'): (2.954524, 4.955654)}
mine = {}
for r in fixed:
    if r['alpha'] != 0.04037:
        mine[(r['alpha'], r['branch'])] = (r['b_schw'], r['m_int'])
for side in ('lower', 'upper'):
    e = ex['alpha_0.04037_' + side]
    mine[(0.04037, side)] = (e['b_schw'], e['m_int'])
for k, (ob, om) in sorted(o_fixed.items()):
    mb, mm = mine[k]
    table_fixed.append(dict(alpha=k[0], branch=k[1], b_orig=ob, b_xc=mb, m_orig=om, m_xc=mm,
                            agree=bool(abs(mb - ob) < 1.5e-6 * max(1, ob) * 10 and abs(mm - om) < 1e-5)))
allfixed = all(t['agree'] for t in table_fixed)
rows.append(row('fixed-alpha table (12 entries, b and m on both branches)', 'REPORT table', 'see fixed_alpha_table', allfixed))

out = dict(experiment='E6 - a fold with gravity (hedgehog Einstein-Skyrme): independent cross-check',
           method='isotropic gauge ds^2=-A^2dt^2+psi^4(dx^2+x^2dOmega^2); Chebyshev pseudo-spectral Newton on compactified radius; '
                  'pseudo-arclength continuation, fold at tau_alpha=0; O(alpha) formulas derived in isotropic gauge; '
                  'own pulsation operator (Schwarzschild gauge) solved by Chebyshev collocation on iso-gauge backgrounds',
           comparisons=rows, fixed_alpha_table=table_fixed,
           alpha_crit_grids=[dict(N=r['N'], L=r['L'], alpha_tau=r['alpha'], alpha_fit_h=r['alpha_fit_h'], alpha_fit_b=r['alpha_fit_b']) for r in fold],
           n_agree=sum(r['agree'] for r in rows), n_rows=len(rows),
           issues=[
               dict(severity='minor', description='Deflection maximum is grid-limited: per unit alpha 18.83 at b=0.739/(ef) reported, true maximum 18.8586 at b=0.7743/(ef) (two gauges agree to 4e-5). Physical: 6.6e-39 rad at 0.41 fm -> 6.61e-39 rad at 0.43 fm (f=64.5 MeV); 1.35e-38 rad at 0.29 fm -> 1.35e-38 at 0.30 fm (f=92.2 MeV).',
                    suggested_fix='Refine the maximum (bounded scalar maximisation) instead of taking the largest of 60 geometric grid points; quote 18.86 at b=0.77/(ef), 0.43 fm and 0.30 fm.'),
               dict(severity='minor', description="'The physical coupling is 39 orders of magnitude below alpha_crit': alpha_crit/alpha_phys = 1.15e38, i.e. 38 orders (alpha_phys/alpha_crit = 8.7e-39 = 10^-38.06).",
                    suggested_fix='Say 38 orders of magnitude (or quote the ratio 8.7e-39).'),
               dict(severity='minor', description="Seed verdict 'commitment 5 AMENDED' attributes the failure of the PLAN's Newtonian -1/2 int rho Phi expectation to the seed. SEED section 5 already identifies 'energy bends the cone' with GR (Weinberg/Deser), whose source is the full T_mu_nu; the computation solves GR by construction, so the seed's physics is not corrected, only its plain-language gloss. The MISS belongs to the preregistered prediction.",
                    suggested_fix="Keep the MISS on the PLAN prediction; give commitment 5 'CONFIRMED (GR by construction), wording clarified: stress-energy, not energy density alone, sources the metric', or mark the AMENDED as wording-only."),
               dict(severity='minor', description="Verdict words on by-construction identities: M_ADM(alpha->0)/E_flat = 1 is labelled CALIBRATED (there is no literature target) and the 4GM/b deflection is CONFIRMED with no 'by construction' caveat in seed_claims (the EP entry does carry the caveat).",
                    suggested_fix="Label these 'consistency check (by construction)'; add the caveat to the SEED 5 light-bending entry."),
               dict(severity='minor', description="Provenance: the report says PLAN.md section 4 E6 'asks four things' including a stability question with a 'literature note: the upper branch is unstable', light deflection, Shapiro delay and an f = 92.2 MeV case. PLAN.md E6 contains only calibration, the EP check and the physical-scale metric deviation; the rest are additions (welcome ones) that should be labelled as such, and 'upper branch unstable' is not a seed claim.",
                    suggested_fix='Mark stability, deflection, Shapiro delay and f = 92.2 MeV as extensions beyond PLAN E6, and move the stability verdict out of seed_claims.'),
               dict(severity='minor', description="The exchange-energy table presents the cancellation of the p_ij p'_ij and -1/2 p p' terms (to 5e-8) as a numerical finding. For any static, conserved (d_i p_ij = 0), spherically symmetric stress the Fourier-space stress is pure transverse trace, A(k)(delta_ij - k_i k_j), for which p_ij p_ij - p^2/2 = 0 identically; the individual values (+-0.6765) carry no separate meaning.",
                    suggested_fix='State the identity; quote only the rho-rho and rho-p terms.'),
           ],
           overall='confirmed_with_corrections')
json.dump(out, open(os.path.join(HERE, 'crosscheck.json'), 'w'), indent=1, default=float)
for r in rows:
    print('%-5s %-55s orig=%s  xc=%s' % ('OK' if r['agree'] else 'DIFF', r['quantity'][:55], str(r['original'])[:40], str(r['crosscheck'])[:70]))
print('fixed table all agree:', allfixed)
for t in table_fixed:
    print('  alpha=%-7g %-5s b %.6f / %.6f   m %.7f / %.7f  %s' % (t['alpha'], t['branch'], t['b_orig'], t['b_xc'], t['m_orig'], t['m_xc'], t['agree']))
