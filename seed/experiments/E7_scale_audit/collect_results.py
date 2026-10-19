#!/usr/bin/env python3
"""Assemble results.json (headline numbers with formula, inputs, target, tolerance, verdict; seed-claim
verdicts; reconciliation log). Reads results_raw.json, hedgehog.json, hopfion.json.

Verdict words: CALIBRATED (literature target within a stated tolerance), CONSISTENT (agrees with a
reference that is not an independent, preregistered literature target: a PLAN expectation or a
non-independent check), QUANTIFIED (a section-8 gap measured), NO_TARGET, MISS.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'results_raw.json')))
H = json.load(open(os.path.join(HERE, 'hedgehog.json')))
HF = json.load(open(os.path.join(HERE, 'hopfion.json')))
sk, el, pr = R['skyrme'], R['skyrme']['electron'], R['skyrme']['proton']
vac, pairs = R['vacuum'], R['pairs']
DL = pairs['demidov_levkov']
E1E = pairs.get('E1e_phi4') if isinstance(pairs.get('E1e_phi4'), dict) and 'error' not in pairs.get('E1e_phi4') else None


def row(q, val, unit, formula, target=None, tol=None, verdict='NO_TARGET', note=''):
    return dict(quantity=q, value=val, unit=unit, formula=formula, target=target, tolerance=tol, verdict=verdict, note=note)


cal = H['calibration']
rhoL = vac['Planck2018_TTTEEE_lowE_lensing']['rho_L_GeV4']
fl1, fl01 = sk['semiclassical_floor']['rot_over_M_le_1.0'], sk['semiclassical_floor']['rot_over_M_le_0.1']
pmf = sk['pion_mass_family']
hop = R['hopfion']
Fr = DL['F2_exponent_read']; Nr = DL['g2Nmin_classical_read']
unsup = DL['coupling_for_unsuppressed_two_particle_production']['rows']
hfs = pairs['QED_breit_wheeler']['hypothetical_fold_suppression']
ip = (HF.get('exact_profile_check') or {}).get('identity_predictions', {})
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
    row('min c0_B over pion mass beta = m_pi/(eF_pi) in [0,16]', pmf['c0_B_min'], '1', 'a1(beta) x_B(beta)',
        note=f"baryon-rms radius: c0 falls only from 77 to 52; with the half-baryon radius from 64 to {pmf['c0_half_min']:.1f}; no route to MR << 1"),
    row('min c0_half over pion mass beta in [0,16]', pmf['c0_half_min'], '1', 'a1(beta) x_half(beta)', note='smallest c0 found in this run'),
    row('proton M R/hbar c, model M_N(939) x R_B(ANW)', pr['MR_nucleon_model']['value'], '1', '939 MeV * R_B/(hbar c)', 2.8,
        '+-0.05 (self-set reading of PLAN "~2.8"; PLAN gives no tolerance)',
        'CONSISTENT' if abs(pr['MR_nucleon_model']['value'] - 2.8) <= 0.05 else 'MISS',
        'reconciled: was CALIBRATED; 2.8 is a PLAN expectation, not a literature target. PLAN\'s formula c0/e^2 with the '
        f"classical mass gives {pr['MR_classical']['value']:.3f}, outside the self-set band; both are > 1 (classical fold)"),
    row('proton M R/hbar c, pure classical c0/e^2 at e = 5.45', pr['MR_classical']['value'], '1', 'M_cl R_B/(hbar c)'),
    row('proton r_p/lambda_C (data)', pr['MR_data']['value'], '1', 'm_p r_p/(hbar c), r_p = 0.84075 fm (PDG 2026)', 4.0, '0.84/0.21 (SEED)',
        'CALIBRATED' if abs(pr['MR_data']['value'] - 4.0) < 0.05 else 'MISS',
        'data use the proton charge radius; the model numbers use the isoscalar radius (the isovector radius diverges for '
        'massless pions), so model vs data is indicative only'),
    row('proton rotor E_rot/M_cl at ANW', pr['rotor_over_mass']['value'], '1', '9 e^4/(16 pi Lambda a1)'),
    row('semiclassical floor (M R)_min for E_rot <= M, baryon rms radius', fl1['MR_min_B'], '1',
        'c0/e_max^2, e_max = (16 pi Lambda a1/9)^(1/4)',
        note=f"e_max = {fl1['e_max']:.3f}; half-baryon radius {fl1['MR_min_half']:.3f}; for E_rot <= 0.1 M: "
             f"{fl01['MR_min_B']:.2f} (baryon rms), {fl01['MR_min_half']:.2f} (half-baryon)"),
    row('electron lambda_C/R_max (LEP r_e < 1.1e-4 fm)', el['LEP']['compton_over_R_min'], '1', 'hbar c/(m_e R_max)', 3.5e6,
        'factor >= 3.5e6 (PLAN prediction)', 'QUANTIFIED',
        'the classical-fold condition R > lambda_C fails by >= 3.5e6; the LEP bound is model dependent (VV contact '
        'interaction, positive interference, electromagnetic coupling strength)'),
    row('electron lambda_C/R_max (SEED 1e-3 fm)', el['SEED']['compton_over_R_min'], '1', 'hbar c/(m_e R_max)', 1e5, 'SEED says ">= 1e5"', 'QUANTIFIED'),
    row('Skyrme e needed for electron fold (LEP, baryon radius)', el['LEP']['B']['e_min'], '1', 'sqrt(c0 hbar c/(m_e R_max))',
        note=f"{min(el['LEP'][k]['e_min'] for k in ['B', 'M', 'E', 'half']):.4g} to "
             f"{max(el['LEP'][k]['e_min'] for k in ['B', 'M', 'E', 'half']):.4g} across radius definitions"),
    row('Skyrme F_pi needed (LEP)', el['LEP']['B']['F_pi_MeV'], 'MeV', 'm_e e/a1'),
    row('rotor correction E_rot/M at electron fold (LEP)', el['LEP']['B']['rot_over_M'], '1', '9 e^4/(16 pi Lambda a1)', note='semiclassics needs << 1'),
    row('hbar/(M R) at electron fold (LEP)', el['LEP']['B']['hbar_over_MR'], '1', 'e^2/c0'),
    row('naive loop parameter e^2/(16 pi^2) at electron fold (LEP)', el['LEP']['B']['naive_loop_parameter_e2_over_16pi2'], '1', ''),
    row('electron needed (MR) / semiclassical floor', el['failure_factor_vs_floor']['value'], '1', el['failure_factor_vs_floor']['formula']),
    row('hopfion E_W(Q=1), hedgehog-Hopf ansatz (upper bound)', HF['E_W_ansatz'], 'Ward units', 'see e7_hopfion.py', 1.204,
        'upper bound expected; literature 1.204 (lattice, ~1% low) to 1.22',
        'CONSISTENT' if HF['E_W_ansatz'] >= 1.204 else 'MISS',
        f"reconciled: was CALIBRATED. E_W(ansatz) = a1/(3 pi^2) = {ip.get('E_W', float('nan')):.7f} identically (symbolic "
        "identity), so it is the Skyrme number again, not an independent calibration; 2.3% above 1.204, ~1% above 1.22; "
        "E8's preregistered 2% would not pass"),
    row('hopfion energy-rms radius R_rms (Ward units)', HF['R_rms_energy_ward'], 'Ward length', 'energy-weighted rms radius at Derrick scale',
        ip.get('R_rms'), '1e-4 (identity x_E/sqrt2)', 'CONSISTENT' if ip and abs(HF['R_rms_energy_ward'] - ip['R_rms']) < 1e-4 else 'MISS',
        'reconciled: v1 gave 2.1441 from a spurious a/r spline tail; identity value x_E/sqrt2'),
    row('hopfion ring radius R_ring (Ward units)', HF['R_ring_ward'], 'Ward length', 'radius where n = -e3',
        ip.get('R_ring'), '1e-4 (identity x_half/sqrt2)', 'CONSISTENT' if ip and abs(HF['R_ring_ward'] - ip['R_ring']) < 1e-4 else 'MISS'),
    row('hopfion c0 = M R/kappa4 (energy rms radius)', HF['c0_hopf_rms'], '1', '16 sqrt2 pi^2 E_W R_rms',
        note=f"ring radius: {HF['c0_hopf_ring']:.1f}; v1 (wrong tail) gave 589.7"),
    row('hopfion: g^2 = 1/kappa4 needed for electron (LEP, rms radius)', hop['electron_LEP']['g2_min'], '1', 'c0_hopf hbar c/(m_e R_max)',
        note=f"ring radius: {hop['electron_LEP_ring']['g2_min']:.3g}; sqrt(kappa2) = {hop['electron_LEP']['sqrt_kappa2_MeV']:.1f} MeV (rms)"),
    row('DL two-particle exponent F at high energy (S = S0/g^2), plateau minimum', Fr['minimum'], '1', 'P ~ exp(-F/g^2)',
        note=f"F = {Fr['at_threshold']:.3f} at threshold (g^2E = {Fr['at_threshold_g2E']:.2f}) to {Fr['at_g2E_11p5']:.3f} at g^2E = 11.5 "
             f"(min {Fr['minimum']:.3f} at {Fr['minimum_at_g2E']:.1f}); {Fr['uncertainty']}; arXiv:1103.0013v2 Fig. 3b vector path [read]. "
             "Reconciled: v1 eye reading 3.93 was wrong by -0.085"),
    row('DL two-particle exponent F at threshold', Fr['at_threshold'], '1', 'P ~ exp(-F/g^2)', note='v1 eye reading 4.45'),
    row('DL classical minimum particle number g^2 N_min, high energy', Nr['high_energy'], '1', 'arXiv:1103.2133v2 Fig. 7b, delta rho -> 0 [read, vector path]',
        note=f"range {Nr['high_energy_range'][0]:.3f}-{Nr['high_energy_range'][1]:.3f} over g^2E = 8.5-10.5; {Nr['near_threshold']:.2f} near threshold"),
    row('DL model 2 g^2 M_S (our quadrature)', DL['two_g2_M_S_computed'], 'units m_- = 1', 'int sqrt(2V) dphi', 6.2,
        'read off axes, +-0.1', 'CALIBRATED' if abs(DL['two_g2_M_S_computed'] - 6.2) <= 0.1 else 'MISS',
        'confirms model/normalisation reading; ' + DL['two_g2_M_S_read_from_axes']),
    row('suppression per pair quantum kappa = F/N_pair', DL['kappa_suppression_per_pair_quantum']['value'][0], '1', 'F/(2 g^2 M_S/m)',
        note=f"{DL['kappa_suppression_per_pair_quantum']['value'][0]:.3f}-{DL['kappa_suppression_per_pair_quantum']['value'][1]:.3f}"),
    row('g^2 at which two-particle pair production reaches P = 1/e', unsup['P=0.368']['g2'], '1', 'g^2 = F_min',
        note=f"there M_S = {unsup['P=0.368']['M_S_over_m']:.2f} m; P = 0.1 at g^2 = {unsup['P=0.1']['g2']:.2f} (M_S = {unsup['P=0.1']['M_S_over_m']:.2f} m), "
             f"P = 0.5 at g^2 = {unsup['P=0.5']['g2']:.2f}; extrapolated leading exponent, indicative only"),
]
if E1E:
    heads.append(row('E1e (phi^4): classical g^2 N_min upper bound (g^2 = 2 lambda/m^2)', E1E['g2_N_min']['N_E'], '1',
                     '2 x (N lambda/m^2) of the smallest producer reproduced at dx = 0.05 (E1)',
                     note=f"N = E/m (preregistered); {E1E['g2_N_min']['N_lin']:.3f} with N_lin; N_min/N_pair <= "
                          f"{E1E['Nmin_over_Npair']['N_E']:.2f}-{E1E['Nmin_over_Npair']['N_lin']:.2f}; classical pair from 2 quanta needs "
                          f"g^2 >= {E1E['g2_for_classical_pair_from_2_quanta']['N_E']:.2f}-{E1E['g2_for_classical_pair_from_2_quanta']['N_lin']:.2f}; "
                          "read from E1 (reconciled separately)"))
heads += [
    row('Breit-Wheeler sigma_max', pairs['QED_breit_wheeler']['sigma_max_over_pi_re2'], 'pi r_e^2', pairs['QED_breit_wheeler']['formula'],
        note=f"= {pairs['QED_breit_wheeler']['sigma_max_mb']:.0f} mb at sqrt(s) = {pairs['QED_breit_wheeler']['sqrt_s_at_max_over_2me']:.2f} x 2m_e; "
             f"an illustrative fold-like exp(-F/g^2) with F = {hfs['F_used']:.2f} would be 10^{hfs['exp_minus_F_over_alpha_log10']:.0f} "
             f"(g^2 = alpha) or 10^{hfs['exp_minus_F_over_4pialpha_log10']:.1f} (g^2 = 4 pi alpha)"),
    row('rho_Lambda (Planck 2018 TT,TE,EE+lowE+lensing: H0 = 67.36, Omega_L = 0.6847)', rhoL, 'GeV^4', '3 H0^2 Mpl_red^2 Omega_L', 2.5e-47, '2%',
        'CALIBRATED' if abs(rhoL / 2.5e-47 - 1) < 0.02 else 'MISS', 'uncertainty 2.6% from Omega_L h^2 = 0.3107 +- 0.0082'),
    row('rho_Lambda^(1/4)', rhoL**0.25 * 1e12, 'meV', '', 2.24, '0.01 meV', 'CALIBRATED' if abs(rhoL**0.25 * 1e12 - 2.24) < 0.01 else 'MISS'),
]
for k, v in vac['ratios_scale4_over_rhoL'].items():
    tgt = {'f_pi^4 (f_pi = 92.07 MeV = 130.2/sqrt2)': 3e42, 'v_EW^4 (v = 246.22 GeV)': 1e56, 'M_Pl^4 unreduced (1.221e19 GeV)': 1e123}.get(k)
    note = 'PLAN: "about"; order of magnitude reproduced' if tgt else ''
    heads.append(row(f'{k} / rho_Lambda', v['ratio'], '1', 'scale^4/rho_L', tgt, 'order of magnitude' if tgt else None, 'QUANTIFIED', note))

g2N = E1E['g2_N_min'] if E1E else None
seed_claims = [
    dict(claim="SEED 8: a fold is a classical shape only if it is larger than its Compton wavelength; the proton is (0.84 fm vs 0.21 fm)",
         verdict='CONFIRMED',
         evidence=f"PDG 2026: r_p/lambda_C = {pr['MR_data']['value']:.3f}. Skyrme fold at ANW parameters: M R/hbar c = "
                  f"{pr['MR_classical']['value']:.2f} (classical mass) or {pr['MR_nucleon_model']['value']:.2f} (939 MeV), rotor "
                  f"E_rot/M = {pr['rotor_over_mass']['value']:.3f}: semiclassical, but only just."),
    dict(claim="SEED 8: the electron misses the classical-fold condition by at least 1e5", verdict='AMENDED',
         evidence=f"True but conservative: with LEP's r_e < 1.1e-4 fm (Schael et al. 2013 Eq. 3.9; model dependent, VV contact "
                  f"interaction) lambda_C/R >= {el['LEP']['compton_over_R_min']:.3g}; with SEED's 1e-3 fm {el['SEED']['compton_over_R_min']:.3g}."),
    dict(claim="SEED 8 / PLAN E7: any soliton whose classical action is S0/g^2 has M R = c0/g^2, so an electron-like fold needs g^2 >> 1",
         verdict='CONFIRMED',
         evidence=(f"Theorem for one-scale theories (scaling, sympy-checked for Skyrme); the general criterion is action per light-crossing "
                   f"~ M R c >> hbar, i.e. R >> lambda_C. Skyrme c0 = {sk['c0']['half']:.0f}-{sk['c0']['M']:.0f} (radius definition); "
                   f"two-parameter families tested keep c0 >= {pmf['c0_half_min']:.1f} (pion mass to beta = 16, half-baryon radius; "
                   f"{pmf['c0_B_min']:.1f} baryon rms) and hopfion c0 = {HF['c0_hopf_ring']:.0f}-{HF['c0_hopf_rms']:.0f}. Electron fold needs "
                   f"Skyrme e >= {min(el['LEP'][k]['e_min'] for k in ['B','M','E','half']):.3g}-{max(el['LEP'][k]['e_min'] for k in ['B','M','E','half']):.3g} "
                   f"(E_rot/M ~ {el['LEP']['B']['rot_over_M']:.1e}) or hopfion 1/kappa4 >= {hop['electron_LEP_ring']['g2_min']:.2g}-"
                   f"{hop['electron_LEP']['g2_min']:.2g}. Semiclassical Skyrme floor M R >= {fl1['MR_min_B']:.3f} hbar/c "
                   f"({fl1['MR_min_half']:.3f} half-baryon radius), {el['failure_factor_vs_floor']['value']:.3g} times above the electron. "
                   "Not shown for theories with extra dimensionless parameters beyond those tested.")),
    dict(claim="SEED 8: this points toward a strongly coupled fold sector, 'the way baryons are in QCD'", verdict='AMENDED',
         evidence="Strong coupling is necessary, but there the classical fold picture is gone (corrections 1e6-1e13 x the classical "
                  "mass), so no classical simulation in the seed can model the electron. The QCD baryon is only moderately quantum "
                  "(M R/hbar c = 2.6-4); the electron needs M R/hbar c <= 2.85e-7."),
    dict(claim="SEED 8: in weakly coupled theories, folding a few quanta into a pair is exponentially rare", verdict='CONFIRMED',
         evidence=(f"Demidov-Levkov (read; curve values from the PDF vector paths): P_2 ~ exp(-F/g^2), F = {Fr['at_threshold']:.2f} at "
                   f"threshold to {Fr['minimum']:.2f} at high energy, i.e. exp(-({DL['kappa_suppression_per_pair_quantum']['value'][0]:.2f}-"
                   f"{DL['kappa_suppression_per_pair_quantum']['value'][1]:.2f}) N_pair). Classical creation needs g^2 N >= {Nr['high_energy']:.2f}; "
                   f"N_min = n0/g^2 in any one-coupling model by scaling. E1e (phi^4, classical): g^2 N_min <= "
                   + (f"{g2N['N_E']:.2f} (N = E/m) to {g2N['N_lin']:.2f} (N_lin)" if g2N else "n/a")
                   + f". Unsuppressed (P >= 0.1-0.5) only for g^2 >~ {unsup['P=0.1']['g2']:.2f}-{unsup['P=0.5']['g2']:.2f} "
                   f"(indicative), where M_S <= {unsup['P=0.1']['M_S_over_m']:.2f} m.")),
    dict(claim="SEED 8: in nature electron pairs form readily, so the fold sector is strongly coupled", verdict='AMENDED',
         evidence=f"Electron pairs form readily because QED is weakly coupled and perturbative: Breit-Wheeler peaks at "
                  f"{pairs['QED_breit_wheeler']['sigma_max_over_pi_re2']:.3f} pi r_e^2 = {pairs['QED_breit_wheeler']['sigma_max_mb']:.0f} mb, "
                  f"power law in alpha. A fold-like exp(-F/g^2) would be 10^{hfs['exp_minus_F_over_alpha_log10']:.0f} (g^2 = alpha) or "
                  f"10^{hfs['exp_minus_F_over_4pialpha_log10']:.0f} (g^2 = 4 pi alpha). The inference in SEED does not follow; the seed must "
                  "produce a pointlike, perturbatively coupled electron out of a strongly coupled fold sector (untested)."),
    dict(claim="SEED 8: why is the vacuum's tension so small (open)", verdict='QUANTIFIED',
         evidence=f"rho_L = {rhoL:.4g} GeV^4 = ({rhoL**0.25*1e12:.3f} meV)^4 (Planck 2018), 1e42 (f_pi^4) to 8.8e122 (M_Pl^4) below natural scales."),
    dict(claim="SEED 8: can light and the cone be built from the field? (Weinberg-Witten)", verdict='AMENDED',
         evidence="With commitment 1's Lorentz-covariant conserved T^mu nu, a composite massless |h| = 2 graviton is excluded; commitment 5's "
                  "metric must be fundamental or emergent only via an evasion. A neutral composite photon is not excluded."),
    dict(claim="SEED 2: one cone, no vacuum dispersion", verdict='OPEN', evidence="Not tested in E7 (E5 checks it by construction)."),
]

reconciliation = [
    dict(issue='Demidov-Levkov high-energy exponent misread (major)', resolved=True,
         action=f"F read from the PDF vector paths (e7_dl_digitize.py): {Fr['at_g2E_11p5']:.3f} at g^2E = 11.5, min {Fr['minimum']:.3f}, "
                f"{Fr['at_threshold']:.3f} at threshold; v1 3.93/4.45 replaced; downstream kappa, g^2 thresholds, M_S/m, QED illustration and figure updated. "
                "Cross-check (3.845, 4.48) was right."),
    dict(issue='Hopfion energy-rms radius (major)', resolved=True,
         action=f"Profile now f = (1-t)^2 h(t) (C/r^2 tail); R_rms = {HF['R_rms_energy_ward']:.4f} (identity x_E/sqrt2 = {ip.get('R_rms', float('nan')):.4f}); "
                f"c0 = {HF['c0_hopf_ring']:.1f}-{HF['c0_hopf_rms']:.1f}; g^2 >= {hop['electron_LEP_ring']['g2_min']:.3g}-{hop['electron_LEP']['g2_min']:.3g}. "
                "Cross-check (2.0608) was right."),
    dict(issue='Hopfion CALIBRATED not independent (minor)', resolved=True, action='relabelled CONSISTENT (upper bound); identity E_W = a1/(3 pi^2) stated and verified symbolically'),
    dict(issue='Proton M R CALIBRATED against a PLAN expectation (minor)', resolved=True, action='relabelled CONSISTENT; classical 2.60 reported alongside'),
    dict(issue='QED illustration depends on g^2 identification (minor)', resolved=True, action='both g^2 = alpha and g^2 = 4 pi alpha quoted'),
    dict(issue='E1e combination missing (minor)', resolved=bool(E1E), action='E1e numbers read from E1_phi4/e1e_results.json and combined' if E1E else 'E1e file absent'),
    dict(issue='label/rounding inconsistencies; radius definition of floors and pion-mass minimum (minor)', resolved=True,
         action='QUANTIFIED for gap numbers throughout; 2.39 for the 0.1 M floor; half-baryon numbers stated'),
    dict(issue='LEP bound model dependence (minor)', resolved=True, action='qualifier added'),
    dict(issue='unlisted deviation: own hedgehog instead of E2 profile (minor)', resolved=True, action='listed as a deviation; agrees with E2 to <= 1e-9'),
    dict(issue="generalisation wording 'any soliton' (minor)", resolved=True, action='seed-claim text restricted to one-scale families plus the tested two-parameter families'),
]

out = dict(experiment='E7 scale and coupling audit (SEED.md section 8)',
           version='v2 (after reconciliation with the independent cross-check)',
           verdict_words='CALIBRATED: literature target within tolerance; CONSISTENT: agrees with a PLAN expectation or a non-independent '
                         'check (not counted as calibration); QUANTIFIED: section-8 gap measured; NO_TARGET; MISS',
           conventions=dict(units='hbar = c = 1 unless stated; hbar c = 197.3269804 MeV fm',
                            skyrme='ANW: F_pi = 186 MeV convention (fit 129 MeV), x = e F_pi r',
                            hopfion='E = int[(kappa2/2)(dn)^2 + (kappa4/4) sum(d_i n x d_j n)^2], Ward-normalised E_W',
                            pairs='S = (1/g^2) int[(d phi)^2/2 - V(phi)], m_- = 1 (Demidov-Levkov)',
                            vacuum='rho_L = Omega_L 3 H0^2/(8 pi G); M_Pl = sqrt(hbar c/G) (unreduced), reduced = M_Pl/sqrt(8 pi)'),
           headline=heads, seed_claims=seed_claims, reconciliation=reconciliation, details=R, hedgehog=H, hopfion=HF)
json.dump(out, open(os.path.join(HERE, 'results.json'), 'w'), indent=1, default=float)
for h in heads:
    v = h['value']
    print(f"{h['verdict']:11s} {h['quantity'][:80]:80s} {v:.6g} {h['unit']}  (target {h['target']})")
print()
for c in seed_claims:
    print(f"{c['verdict']:10s} {c['claim'][:100]}")
