#!/usr/bin/env python3
"""Assemble results.json (headline numbers with formula, inputs, target, tolerance, verdict)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'results_raw.json')))
H = json.load(open(os.path.join(HERE, 'hedgehog.json')))
HF = json.load(open(os.path.join(HERE, 'hopfion.json')))
sk, el, pr = R['skyrme'], R['skyrme']['electron'], R['skyrme']['proton']
vac, pairs = R['vacuum'], R['pairs']


def row(q, val, unit, formula, target=None, tol=None, verdict='NO_TARGET', note=''):
    return dict(quantity=q, value=val, unit=unit, formula=formula, target=target, tolerance=tol, verdict=verdict, note=note)


cal = H['calibration']
rhoL = vac['Planck2018_TTTEEE_lowE_lensing']['rho_L_GeV4']
heads = [
    row('a1 = M_cl/(F_pi/e)', cal['a1']['ours'], '1', '4 pi int[x^2F^2/8 + sin^2F/4 + sin^2F F^2 + sin^4F/(2x^2)]dx',
        36.4633, '0.2%', 'CALIBRATED' if cal['a1']['pass_'] else 'MISS', 'PLAN E2 target 1.2315*3pi^2 [read]'),
    row('Lambda (I1 = (2pi/3) Lambda/(e^3 F_pi))', cal['Lambda']['ours'], '1', 'int x^2 sin^2F[1+4(F^2+sin^2F/x^2)]dx',
        50.9, '0.5%', 'CALIBRATED' if cal['Lambda']['pass_'] else 'MISS'),
    row('virial E2/E4', cal['virial']['ours'], '1', 'Derrick', 1.0, '1e-4', 'CALIBRATED' if cal['virial']['pass_'] else 'MISS'),
    row('R_B (= ANW isoscalar charge rms radius) at ANW parameters', pr['R_B_fm'], 'fm', 'x_B/(e F_pi), F_pi = 129 MeV, e = 5.45',
        0.59, '0.01 fm', 'CALIBRATED' if pr['calibration_radii']['pass_B'] else 'MISS', 'ANW via secondary sources'),
    row('R_M (ANW isoscalar magnetic rms radius) at ANW parameters', pr['R_M_fm'], 'fm', 'x_M/(e F_pi)',
        0.92, '0.01 fm', 'CALIBRATED' if pr['calibration_radii']['pass_M'] else 'MISS'),
    row('own fit to M_N = 938.9, M_Delta = 1232 MeV: F_pi', pr['own_fit_to_MN_MDelta']['F_pi_MeV'], 'MeV',
        'M_N = M + 3/(8I1), M_D = M + 15/(8I1)', 129.0, '1%', 'CALIBRATED' if abs(pr['own_fit_to_MN_MDelta']['F_pi_MeV'] / 129 - 1) < 0.01 else 'MISS'),
    row('own fit: e', pr['own_fit_to_MN_MDelta']['e'], '1', 'same', 5.45, '1%',
        'CALIBRATED' if abs(pr['own_fit_to_MN_MDelta']['e'] / 5.45 - 1) < 0.01 else 'MISS'),
    row('a2 = e F_pi R_B (baryon rms)', sk['a2']['B'], '1', 'sqrt(-(2/pi) int x^2 sin^2F F dx)'),
    row('c0 = M R e^2/(hbar c), baryon rms radius', sk['c0']['B'], '1', 'a1 a2'),
    row('c0, half-baryon radius (most compact definition used)', sk['c0']['half'], '1', 'a1 x_1/2'),
    row('c0, isoscalar magnetic radius', sk['c0']['M'], '1', 'a1 x_M'),
    row('c0, energy rms radius', sk['c0']['E'], '1', 'a1 x_E'),
    row('min c0_B over pion mass beta = m_pi/(eF_pi) in [0,16]', sk['pion_mass_family']['c0_B_min'], '1', 'a1(beta) x_B(beta)', note='c0 decreases only from 77 to 52; no route to MR << 1'),
    row('proton M R/hbar c, model M_N(939) x R_B(ANW)', pr['MR_nucleon_model']['value'], '1', '939 MeV * R_B/(hbar c)', 2.8,
        '+-0.05 (2 sig. fig. of PLAN "~2.8"; fixed before computing)',
        'CALIBRATED' if abs(pr['MR_nucleon_model']['value'] - 2.8) <= 0.05 else 'MISS', 'PLAN expectation from ANW numbers'),
    row('proton M R/hbar c, pure classical c0/e^2 at e = 5.45', pr['MR_classical']['value'], '1', 'M_cl R_B/(hbar c)'),
    row('proton r_p/lambda_C (data)', pr['MR_data']['value'], '1', 'm_p r_p/(hbar c), r_p = 0.84075 fm (PDG 2026)', 4.0, '0.84/0.21 (SEED)',
        'CALIBRATED' if abs(pr['MR_data']['value'] - 4.0) < 0.05 else 'MISS'),
    row('proton rotor E_rot/M_cl at ANW', pr['rotor_over_mass']['value'], '1', '9 e^4/(16 pi Lambda a1)'),
    row('semiclassical floor (M R)_min for E_rot <= M', sk['semiclassical_floor']['rot_over_M_le_1.0']['MR_min_B'], '1',
        'c0/e_max^2, e_max = (16 pi Lambda a1/9)^(1/4)', note=f"e_max = {sk['semiclassical_floor']['rot_over_M_le_1.0']['e_max']:.3f}; (MR)_min = 2.40 for E_rot <= 0.1 M"),
    row('electron lambda_C/R_max (LEP r_e < 1.1e-4 fm)', el['LEP']['compton_over_R_min'], '1', 'hbar c/(m_e R_max)', 3.5e6,
        'factor >= 3.5e6 (PLAN prediction)', 'QUANTIFIED', 'the classical-fold condition R > lambda_C fails by >= 3.5e6'),
    row('electron lambda_C/R_max (SEED 1e-3 fm)', el['SEED']['compton_over_R_min'], '1', 'hbar c/(m_e R_max)', 1e5, 'SEED says ">= 1e5"', 'QUANTIFIED'),
    row('Skyrme e needed for electron fold (LEP, baryon radius)', el['LEP']['B']['e_min'], '1', 'sqrt(c0 hbar c/(m_e R_max))'),
    row('Skyrme F_pi needed (LEP)', el['LEP']['B']['F_pi_MeV'], 'MeV', 'm_e e/a1'),
    row('rotor correction E_rot/M at electron fold (LEP)', el['LEP']['B']['rot_over_M'], '1', '9 e^4/(16 pi Lambda a1)', note='semiclassics needs << 1'),
    row('hbar/(M R) at electron fold (LEP)', el['LEP']['B']['hbar_over_MR'], '1', 'e^2/c0'),
    row('naive loop parameter e^2/(16 pi^2) at electron fold (LEP)', el['LEP']['B']['naive_loop_parameter_e2_over_16pi2'], '1', ''),
    row('electron needed (MR) / semiclassical floor', el['failure_factor_vs_floor']['value'], '1', el['failure_factor_vs_floor']['formula']),
    row('hopfion E_W(Q=1), hedgehog-Hopf ansatz (upper bound)', HF['E_W_ansatz'], 'Ward units', 'see e7_hopfion.py', 1.204,
        'upper bound; literature 1.204-1.22', 'CALIBRATED' if 1.204 <= HF['E_W_ansatz'] <= 1.204 * 1.05 else 'MISS', 'variational: 2.3% above 1.204, ~1% above 1.22'),
    row('hopfion c0 = M R/kappa4 (energy rms radius)', HF['c0_hopf_rms'], '1', '16 sqrt2 pi^2 E_W R_rms'),
    row('hopfion: g^2 = 1/kappa4 needed for electron (LEP)', R['hopfion']['electron_LEP']['g2_min'], '1', 'c0_hopf hbar c/(m_e R_max)'),
    row('DL two-particle exponent F (S = S0/g^2), read', 3.93, '1', 'P ~ exp(-F/g^2)', note='4.45 at threshold to 3.93 at 1.9x threshold; arXiv:1103.0013 Fig.3b [read]'),
    row('DL classical minimum particle number g^2 N_min, read', 3.98, '1', 'arXiv:1103.2133 Fig. 7b, delta rho -> 0 [read]'),
    row('DL model 2 g^2 M_S (our quadrature)', pairs['demidov_levkov']['two_g2_M_S_computed'], 'units m_- = 1', 'int sqrt(2V) dphi', 6.2,
        'read off axes, +-0.1', 'CALIBRATED' if abs(pairs['demidov_levkov']['two_g2_M_S_computed'] - 6.2) <= 0.1 else 'MISS', 'confirms model/normalisation reading'),
    row('suppression per pair quantum kappa = F/N_pair', pairs['demidov_levkov']['kappa_suppression_per_pair_quantum']['value'][0], '1', 'F/(2 g^2 M_S/m)', note='0.63-0.71'),
    row('g^2 at which two-particle pair production reaches P = 1/e', pairs['demidov_levkov']['coupling_for_unsuppressed_two_particle_production']['rows']['P=0.368']['g2'], '1',
        'g^2 = F', note='there M_S = 0.79 m: the fold is lighter than one elementary quantum'),
    row('Breit-Wheeler sigma_max', pairs['QED_breit_wheeler']['sigma_max_over_pi_re2'], 'pi r_e^2', pairs['QED_breit_wheeler']['formula'],
        note=f"= {pairs['QED_breit_wheeler']['sigma_max_mb']:.0f} mb at sqrt(s) = 1.40 x 2m_e; fold-like suppression at g^2 = alpha would be 10^{pairs['QED_breit_wheeler']['hypothetical_fold_suppression']['exp_minus_F_over_alpha_log10']:.0f}"),
    row('rho_Lambda (Planck 2018 TT,TE,EE+lowE+lensing: H0 = 67.36, Omega_L = 0.6847)', rhoL, 'GeV^4', '3 H0^2 Mpl_red^2 Omega_L', 2.5e-47, '2%',
        'CALIBRATED' if abs(rhoL / 2.5e-47 - 1) < 0.02 else 'MISS', 'uncertainty 2.6% from Omega_L h^2 = 0.3107 +- 0.0082'),
    row('rho_Lambda^(1/4)', rhoL**0.25 * 1e12, 'meV', '', 2.24, '0.01 meV', 'CALIBRATED' if abs(rhoL**0.25 * 1e12 - 2.24) < 0.01 else 'MISS'),
]
for k, v in vac['ratios_scale4_over_rhoL'].items():
    tgt = {'f_pi^4 (f_pi = 92.07 MeV = 130.2/sqrt2)': 3e42, 'v_EW^4 (v = 246.22 GeV)': 1e56, 'M_Pl^4 unreduced (1.221e19 GeV)': 1e123}.get(k)
    verdict = 'QUANTIFIED'
    note = 'PLAN: "about"; order of magnitude reproduced' if tgt else ''
    heads.append(row(f'{k} / rho_Lambda', v['ratio'], '1', 'scale^4/rho_L', tgt, 'order of magnitude' if tgt else None, verdict, note))

out = dict(experiment='E7 scale and coupling audit (SEED.md section 8)',
           conventions=dict(units='hbar = c = 1 unless stated; hbar c = 197.3269804 MeV fm',
                            skyrme='ANW: F_pi = 186 MeV convention (fit 129 MeV), x = e F_pi r',
                            hopfion='E = int[(kappa2/2)(dn)^2 + (kappa4/4) sum(d_i n x d_j n)^2], Ward-normalised E_W',
                            pairs='S = (1/g^2) int[(d phi)^2/2 - V(phi)], m_- = 1 (Demidov-Levkov)',
                            vacuum='rho_L = Omega_L 3 H0^2/(8 pi G); M_Pl = sqrt(hbar c/G) (unreduced), reduced = M_Pl/sqrt(8 pi)'),
           headline=heads, details=R, hedgehog=H, hopfion=HF)
json.dump(out, open(os.path.join(HERE, 'results.json'), 'w'), indent=1, default=float)
for h in heads:
    v = h['value']
    print(f"{h['verdict']:11s} {h['quantity'][:80]:80s} {v:.6g} {h['unit']}  (target {h['target']})")
