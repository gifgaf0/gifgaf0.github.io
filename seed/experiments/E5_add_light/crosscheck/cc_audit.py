"""E5 cross-check: audit of the original REPORT.md against the original's own results.json and logs,
plus assembly of crosscheck.json (numbers from crosscheck_numbers.json, issues, claim audit, verdict).
Every text finding below is re-derived here by string search so that it is reproducible."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.join(HERE, '..')
rep = open(os.path.join(UP, 'REPORT.md'), encoding='utf-8').read()
res = json.load(open(os.path.join(UP, 'results.json')))
symlog = open(os.path.join(UP, 'symbolic_log.txt')).read()
nums = json.load(open(os.path.join(HERE, 'crosscheck_numbers.json')))
new = json.load(open(os.path.join(HERE, 'cc_new.json')))
extra = json.load(open(os.path.join(HERE, 'cc_extra.json')))

text = {}
m = re.search(r'(\d+) checks passed, (\d+) failed, ([\d.]+) s', symlog)
text['symbolic_log'] = {'passed': int(m.group(1)), 'failed': int(m.group(2)), 'runtime_s': float(m.group(3))}
text['report_says_38'] = len(re.findall(r'38/38|38 checks', rep))
text['results_json_symbolic_row'] = next(c['value'] for c in res['calibration'] if c['quantity'].startswith('symbolic'))
text['report_runtime_claim_150_170s'] = '150–170 s' in rep
text['report_pi0_dA_with_48pi2'] = 'N_c e²/48π²f) ε^{μναβ}∂_μA_ν' in rep
text['report_convergence_5e-8_for_X25'] = 'X = 25, 50, 100, 200, 400' in rep and '5×10⁻⁸' in rep
text['results_json_X25_rel_dev_Lambda'] = res['hedgehog_numerics']['relative_deviation_short_boxes']['X=25']['Lambda']
text['report_uses_QUANTIFIED'] = 'QUANTIFIED' in rep
text['results_json_uses_QUANTIFIED'] = any('QUANTIFIED' in c['verdict'] for c in res['seed_claims'])
text['report_3_of_7_framing'] = '3 of 7 finite predictions are within 30%' in rep
text['results_json_6B_evidence'] = next(c['evidence'] for c in res['seed_claims'] if c['claim'].startswith('SEED 6B'))[:120]
text['report_internal_checks_CALIBRATED'] = bool(re.search(r'charges of 8, 10, 10̄, 27 integral.*CALIBRATED', rep)) and \
    bool(re.search(r'symbolic derivations, one cone, taut vacuum \| 38/38.*CALIBRATED', rep))
text['results_json_internal_checks'] = [c['verdict'] for c in res['calibration'] if c['quantity'].startswith(('rotor', 'symbolic'))]
text['report_commitment4_verdict'] = re.search(r'\*\*Commitment 4, charge dressed, not slowed: ([A-Z ()a-z]+)\.\*\*', rep).group(1)
text['results_json_commitment4_verdict'] = next(c['verdict'] for c in res['seed_claims'] if c['claim'].startswith('Commitment 4'))
text['results_json_reconciliation_changes'] = res['reconciliation']['changes']
text['neutron_peak_true'] = {'Q_n': extra['massless_ANW']['Qn_peak'], 'R_fm': extra['massless_ANW']['R_peak_fm']}
text['report_neutron_table_1fm'] = '| 1 | 0.764 | +0.185 |' in rep
text['tail_check_R10fm_rel'] = abs(res['isovector_tail_check'][-1]['isovector_outside'] /
                                   res['isovector_tail_check'][-1]['asymptotic_C2_over_2Lambda_xR'] - 1)
text['figures_exist'] = {f: os.path.getsize(os.path.join(UP, f)) for f in ('fig_charge_densities.png', 'fig_vs_pdg.png')
                         if os.path.exists(os.path.join(UP, f))}
for k, v in text.items():
    print(f'{k:42s} {v}')

issues = [
    {'severity': 'major',
     'description': 'REPORT.md (and the structured summary handed to the orchestrator) is out of date with respect to the '
                    "original's own results.json. results.json carries a 'reconciliation' block (8 changes made after the first "
                    'cross-check pass) and code-generated seed verdicts that differ from the REPORT text: the REPORT still says '
                    '38/38 symbolic checks (log and results.json: 39/39, all computed), still labels the integer-charge and symbolic '
                    'rows CALIBRATED (results.json: CHECK PASSED), still gives the f_pi tension the verdict QUANTIFIED (results.json: '
                    'no SEED verdict), still frames SEED 6B as "3 of 7 within 30%" (results.json: 6 of 7 within 33%, amendment carried '
                    'by g_A and the charge radii), still gives Commitment 4 an unqualified CONFIRMED (results.json: "in the '
                    'preregistered operational sense only"), and still contains the pi0-coupling typo and the X = 25 convergence '
                    'overstatement that results.json lists as corrected. Two deliverables of one experiment therefore disagree on '
                    'seed-verdict wording; whichever feeds RESULTS.md decides what the series claims.',
     'suggested_fix': 'Regenerate REPORT.md (and the summary) from the current results.json: apply every item of '
                      "results.json['reconciliation']['changes'] to the text, use 39/39, CHECK PASSED for internal checks, drop "
                      'QUANTIFIED, and adopt the qualified verdict wording for Commitment 4, SEED 6B and the N_c = 1 exclusion.'},
    {'severity': 'minor',
     'description': 'REPORT Method: "L = (N_c e²/48π²f) ε^{μναβ}∂_μA_ν A_α ∂_β π⁰" is a factor 2 too small. With ∂_μA_ν the coefficient '
                    'is N_c e²/(24π²f); 48π² goes with F_μν. The quoted amplitude N_c e²/(12π²f) and all numbers are right '
                    '(symbolic check 9g in the code and cc_pi0.py both give 24π² for ∂_μA_ν).',
     'suggested_fix': 'Write F_μν in place of ∂_μA_ν, or 24π² in place of 48π².'},
    {'severity': 'minor',
     'description': 'REPORT Method: "X = 25, 50, 100, 200, 400 ... agree to within 5×10⁻⁸ relative in Λ". results.json '
                    '(relative_deviation_short_boxes) shows X = 25 off by 7.2e-7 in Λ and 1.2e-6 in C; the 5e-8 spread holds for '
                    'X = 100–400 (X = 50: 2.8e-8).',
     'suggested_fix': 'State the X = 100–400 spread and the X = 25 deviation separately.'},
    {'severity': 'minor',
     'description': 'Symbolic-check count and runtime: REPORT says 38/38 and 150–170 s (total 2 min 59 s); symbolic_log.txt says '
                    '39 checks passed in 302.6 s. Check 10d is now a computed expansion (earlier "by inspection"), and 9g was added.',
     'suggested_fix': 'Quote 39/39 and the logged runtime.'},
    {'severity': 'minor',
     'description': 'Verdict vocabulary in the REPORT: CALIBRATED for internal checks with no literature target (integer charges, '
                    'symbolic derivations) and QUANTIFIED for a SEED 6B paraphrase ("one parameter set for all predictions, '
                    'anomaly sector included"). PLAN reserves CALIBRATED for literature targets and QUANTIFIED for §8 gaps; the '
                    'paraphrase is not SEED.md text (SEED 6B says only that F sets the units and e is the only pure number). '
                    'results.json already uses CHECK PASSED and no SEED verdict.',
     'suggested_fix': 'Follow results.json.'},
    {'severity': 'minor',
     'description': 'The "fold sector and anomaly prefer different f_pi" result is not an independent tension: Γ ∝ 1/f², so 2.03× '
                    'is (92.0/64.5)², i.e. ANW\'s fitted f_pi = F_pi/2 = 64.5 MeV is 30% below 92.2 MeV (SU(3) refit: 38% below). '
                    "That f_pi miss belongs in the SEED 6B tally (it is itself 'roughly 30%'); the width only squares it. "
                    'results.json mentions the 30% f_pi deficit; the REPORT presents the factor 2 as a separate finding.',
     'suggested_fix': 'Add f_pi (−30%) as an eighth row of the 6B comparison and describe the Γ factor as its square.'},
    {'severity': 'minor',
     'description': 'SEED 6B framing in the REPORT: "3 of 7 within 30%" counts μ_p (−33%), μ_n (−31%) and g_πNN (−32%) as misses '
                    'of "roughly 30%". The AMENDED verdict is earned by g_A (−52%) and by r_p, ⟨r²⟩_n being infinite with massless '
                    'pions. Recomputed tally (PDG 2026, queried independently): 3 of 7 within 30%, 6 of 7 within 33%.',
     'suggested_fix': 'Use results.json wording (6 of 7 within ~33%; exceptions g_A and the individual charge radii).'},
    {'severity': 'minor',
     'description': 'Commitment 4: the preregistered prediction (isovector ⟨r²⟩ diverges linearly, 0.411 fm × R; finite with m_pi) '
                    'is confirmed, but the test cannot distinguish "dressing by vacuum polarization" from any extended charge '
                    'distribution, and "not slowed" holds by construction. The REPORT verdict is an unqualified CONFIRMED; '
                    'results.json qualifies it.',
     'suggested_fix': 'CONFIRMED (in the preregistered operational sense: classical pion-cloud structure, not vacuum polarization).'},
    {'severity': 'minor',
     'description': 'Structured summary, Commitment 4 evidence: "the neutron\'s enclosed charge peaks at +0.185 at 1 fm". 1 fm is a '
                    'table grid point; the maximum is +0.2057 at R = 0.7255 fm (massless ANW), as results.json and cc_extra.json both '
                    'give. The REPORT table value +0.185 at 1 fm is itself correct.',
     'suggested_fix': 'Quote +0.206 at 0.73 fm.'},
    {'severity': 'minor',
     'description': 'g_πNN is CALIBRATED only under the post hoc ±0.05 tolerance (disclosed); with the moments\' ±0.02 it fails '
                    '(|8.868 − 8.9| = 0.032). Acceptable because g_A, which fixes g_πNN by Goldberger–Treiman, passes its '
                    'preregistered ±0.01, but the verdict line should say so (results.json does).',
     'suggested_fix': 'Note "fails ±0.02" next to the verdict in the REPORT table.'},
    {'severity': 'minor',
     'description': 'Unverified attribution: "ANW\'s own table (as reproduced by Rakhimov) already excepted g_A". Neither ANW nor '
                    'Rakhimov was read in this run or the original (ANW predates arXiv; publisher sites are blocked).',
     'suggested_fix': 'Mark as [summary] or drop.'},
]

claims = [
    {'claim': 'SEED 7.4: gauging a U(1) inside the internal symmetry gives the folds integer electric charges (CONFIRMED)',
     'verdict': 'supported',
     'note': 'Reproduced with Gelfand-Tsetlin patterns: 8 {-1,0,1}, 10 {-1..2}, 10bar {-2..1}, 27 {-2..2}; SU(2) Q = I3 + B/2. '
             'The gauged-WZ A-linear term gives charge N_c/6 per unit B (numerically 0.16666667, isovector part 1e-19), i.e. '
             'B/2 at N_c = 3. The U(1) generator (quark charge matrix) is an input chosen to match nature; integrality follows '
             'because the WZ constraint Y_R = 1 selects triality-zero irreps. The N_c caveat is stated.'},
    {'claim': 'SEED 7.4/2: one light cone, no vacuum dispersion (CONFIRMED by construction)',
     'verdict': 'supported',
     'note': 'Independent sympy linearisation: pion omega^2 = k^2 + m^2, photon omega = |k| (Maxwell kernel rank 3 off cone, 1 on '
             'cone, gauge mode null), no mixing, Skyrme term starts at 4th order. Correctly labelled "by construction".'},
    {'claim': 'Commitment 1: vacuum T_mu nu proportional to g_mu nu, p = -rho in every frame (CONFIRMED by construction)',
     'verdict': 'supported',
     'note': 'T_mu nu = V0 g_mu nu (mostly minus), boost invariant. V0 is an arbitrary added constant (zero for the Skyrme '
             'Lagrangian as written); the check says nothing about its value. Correctly labelled.'},
    {'claim': 'Commitment 4: charge is dressed, not slowed (REPORT: CONFIRMED; results.json: CONFIRMED in the preregistered operational sense only)',
     'verdict': 'overstated',
     'note': 'All dressing numbers reproduced (slope C^2/Lambda = 1.463846, 0.4109 fm x R; outside-charge 0.2054 fm/R; enclosed '
             'charges to 1e-10; neutron peak +0.2057 at 0.7255 fm). The qualified results.json verdict is supported; the '
             'unqualified REPORT verdict is overstated (classical pion cloud, not vacuum polarization; "not slowed" by construction).'},
    {'claim': 'SEED 6B: within roughly 30% for nucleons (AMENDED)',
     'verdict': 'supported',
     'note': 'Tally recomputed from an independent PDG 2026 query: 3 of 7 within 30%, 6 of 7 within 33%; g_A -52%; r_p and '
             '<r^2>_n infinite with massless pions. AMENDED is earned by g_A and the radii. The REPORT\'s "3 of 7" framing '
             'overstates the miss (minor issue); f_pi itself (-30%) should be in the tally.'},
    {'claim': 'SEED 6B one parameter set incl. anomaly sector (REPORT: QUANTIFIED; results.json: preregistered prediction confirmed, no SEED verdict)',
     'verdict': 'overstated',
     'note': 'Numbers reproduced (15.862 eV = 2.03x, 20.399 eV = 2.61x; f ratio 1.43-1.62). QUANTIFIED is the wrong verdict word '
             '(PLAN: §8 gaps only), the claim is a paraphrase, and the factor is the square of the known 30% f_pi miss, not an '
             'independent tension. The PLAN prediction itself is confirmed.'},
    {'claim': 'SEED 2 / PLAN: the WZ term that makes the fold a fermion also fixes pi0 -> gamma gamma; N_c = 1 excluded (CONFIRMED with caveat)',
     'verdict': 'supported',
     'note': 'Gamma = alpha^2 m^3 N_c^2/(576 pi^3 f^2) re-derived (B-H eq. 67 plane-wave amplitude, and textbook A = N_c alpha/(3 pi f)); '
             '7.7611 eV, -0.35 sigma vs PrimEx-II. The same -N_c/48pi^2 coefficient gives the B/2 charge (new numerical check). '
             'The N_c = 1 exclusion holds only with fixed quark charges; Bar-Wiese hep-ph/0105258 (read in the mirror this pass) '
             'states exactly this, and the anomaly-consistent nucleon charges {0,1} for N_c = 1..9 are reproduced.'},
]

out = {
    'experiment': 'E5 -- Add light (cross-check, second pass)',
    'rows': nums['rows'], 'n_rows': nums['n_rows'], 'n_agree': nums['n_agree'],
    'n_calibration_rows': nums['n_calibration_rows'],
    'n_calibration_rows_crosscheck_within_target': nums['n_calibration_rows_crosscheck_within_target'],
    'charges_agree_and_integral': nums['charges_agree_and_integral'], 'Nc_charge_table_agrees': nums['Nc_charge_table_agrees'],
    'WZ_charge_per_Nc': nums['WZ_charge_per_Nc'], 'linearisation': nums['linearisation'], 'pi0_symbolic': nums['pi0_symbolic'],
    'third_solver_fe_richardson': new['fe_profile']['richardson'],
    'text_audit': text, 'issues': issues, 'claim_audit': claims,
    'overall': 'confirmed_with_corrections',
    'summary': 'All headline numbers reproduced (100/100 rows, three independent profile solvers, Noether currents from the matrix '
               'Lagrangian, independent pi0 derivation, Gelfand-Tsetlin charges, independent PDG query). No numeric disagreement. '
               'One major presentation issue: REPORT.md and the structured summary were not updated after the original\'s '
               'reconciliation, so they disagree with results.json on verdict wording and the check count. Ten minor issues.',
}
json.dump(out, open(os.path.join(HERE, 'crosscheck.json'), 'w'), indent=1, ensure_ascii=False)
print(f"wrote crosscheck.json: {out['n_agree']}/{out['n_rows']} rows agree; {len(issues)} issues "
      f"({sum(i['severity'] == 'major' for i in issues)} major); overall {out['overall']}")
