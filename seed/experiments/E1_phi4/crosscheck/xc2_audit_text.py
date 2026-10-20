"""Claim audit, issues and verdict of the second cross-check pass; numbers pulled from
xc2_compare.json and the original-code diagnosis files.  Writes xc2_audit_text.json."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(HERE, 'xc2_compare.json')))
s = c.get('e1d_sample_spec', {})
m = c['e1c_map']
ex = c['e1c_example']
tg = {(r['A'], r['sigma'], r['k'], r['single'], r['oneway'], r['dx']): r for r in c['e1d_targets']}
g = lambda *k: tg.get(k)
sp41 = ex.get('spec_om0.99_v0.41_dx0.05_dt0.02')
sp41_txt = 'pending' if sp41 is None else ('pair since t=%s' % sp41['first'] if sp41['pair_at_T'] else 'no pair')
sp43 = {k.replace('spec_om0.99_v0.43_', ''): v for k, v in ex.items() if k.startswith('spec_om0.99_v0.43')}
sp43_txt = ', '.join('%s: %s' % (k, 'pair' if v['pair_at_T'] else 'no pair') for k, v in sp43.items())
samp_txt = ('%d random coarse points (A >= 0.3), spectral vs original %.0f%% agreement (E > 2M: %.0f%%), spectral vs FD6 %.0f%%, '
            'FD6 vs original %.0f%%' % (s['n'], 100 * s['agree_spec_orig'], 100 * s['agree_spec_orig_E_gt_2M'],
                                       100 * s['agree_spec_fd6'], 100 * s['agree_fd6_orig'])) if s else 'pending'
r3 = g(0.6, 4.0, 0.5, False, True, 0.1)
r3b = g(0.6, 4.0, 0.5, False, True, 0.05)
r1b = g(0.8, 2.0, 0.5, False, False, 0.05)
sf = sorted([r for r in c['e1d_targets'] if r['single'] and r['sigma'] == 16.0], key=lambda r: (r['k'], r['A']))
sf_min = {}
for r in sf:
    if r['prod'] and r['k'] not in sf_min:
        sf_min[r['k']] = r['A']
sf_txt = ', '.join('k=%g: first self-folding A = %s' % (k, v) for k, v in sorted(sf_min.items())) or 'pending'

claims = [
    dict(claim='E1a: M_kink = 0.9428090346 and omega_s = 1.2247448677, CALIBRATED', verdict='supported',
         note='Collocation BVP gives M = 0.9428090416 (rel. err. 3e-15), Chebyshev omega_s = 1.2247448717.'),
    dict(claim='E1b: v_c = 0.26006 +- 0.00003 (dt -> 0), CALIBRATED against 0.2598 +- 0.001', verdict='supported',
         note='Fourier + RK4 code with x0 = 15 and its own box gives 0.260066 (dt = 0.02 bracket 0.26006-0.260066). The 2.6e-4 '
              'offset from the [summary] target is common to both codes, so it is not numerical.'),
    dict(claim='E1b: first two-bounce window [0.19256, 0.20343], >= 3 windows narrowing toward v_c', verdict='supported',
         note='Independent: [0.192566, 0.203433]; windows 2 and 3 agree to 1e-4; T12 = 17.80, 23.16, 28.52 against 17.80, 23.18, 28.52.'),
    dict(claim='E1b: Manton et al. 2021 quote the first window as 0.1920-0.2029', verdict='supported',
         note='Read in arXiv:2106.05153v2 here: "the first 2-bounce window occurs for 0.1920 < vin < 0.2029".'),
    dict(claim='E1c: (omega, v) = (0.99, 0.43) produces a pair, CALIBRATED; "the pair is real: it is still separating at 1.5T"',
         verdict='unsupported',
         note='The call is not reproducible. The original code itself (unmodified copy) produces at only 4 of 10 (dx, dt) settings: '
              'yes at (0.1, 0.04) [t = 1160], (0.1, 0.02) [780], (0.025, 0.005) and (0.0125, 0.005) [840]; no at (0.1, 0.01), '
              '(0.05, 0.02), (0.05, 0.01), (0.05, 0.005), (0.025, 0.01) and (0.025, 0.0025). The two independent, higher-order-in-time '
              'codes give no pair up to 1.5T (FD6+RK4 dx 0.08; spectral %s). The point was never resolution-checked in E1, and its '
              'formation time (1160) is the latest of all 80 producers (median 120). It is a sensitive point, not a calibration point. '
              'The DSV-like event does exist 0.02 lower: (0.99, 0.41) forms a pair at t = 590 in the spectral code at '
              '(dx, dt) = (0.1, 0.02), (0.05, 0.02) and (0.1, 0.01), and in the finest original setting (0.025, 0.005).' % sp43_txt),
    dict(claim='E1c reproduces DSV Fig. 2 band by band, including the example point', verdict='overstated',
         note='Band location and trend are reproduced for omega = 0.90-0.98 by both codes: 91%% call agreement on %d common points, '
              'FD6 Spearman %.2f. At v step 0.02 the original hits %d of DSV\'s 22 producing points with %d false positives (FD6: %d and %d). '
              'The omega = 0.99 column is not converged: original code, v 0.38-0.48, gives producers {0.39, 0.41, 0.43} at '
              '(0.1, 0.04), {0.43} at (0.1, 0.02) and none at (0.05, 0.02). The spectral code gives a converged producer at v = 0.41 '
              '(dx 0.05: %s); FD6 gives v = 0.40 on its step-0.02 grid. So DSV\'s omega = 0.99 production near v ~ 0.4 is reproduced, '
              'but at 0.41, not at the quoted 0.43.' % (m['n_common'], m['spearman_fd6'][0], m['vs_dsv_reading']['orig_hits'],
                                         m['vs_dsv_reading']['orig_false_pos'], m['vs_dsv_reading']['fd6_hits'],
                                         m['vs_dsv_reading']['fd6_false_pos'], sp41_txt)),
    dict(claim='E1c: dx = 0.05 rerun agrees on 74 of 78 calls; the four disagreements are band-edge points', verdict='overstated',
         note='True as counted, but the omega = 0.99 column agrees only trivially: its producers at dx = 0.1 (0.41, 0.43) are not on '
              'the dx = 0.05 grid, and the dx = 0.05 column has no producer at all. The example point was never resolution-checked.'),
    dict(claim='E1c: trend to lower v as omega rises, pass-through at high v, none above omega = 0.99', verdict='supported',
         note='FD6: Spearman %.2f; 0/%d producing at v >= 0.86; 0/%d at omega = 0.995.' % (
             m['spearman_fd6'][0], m['n_v_ge_086'], m['n_omega_gt_099'])),
    dict(claim='E1c hole at (0.91, 0.81-0.82)', verdict='supported',
         note='Not on the FD6 grid. The original dx = 0.05 rerun keeps v = 0.82 empty between producing 0.80 and 0.84.'),
    dict(claim='E1d: no production below 2 M_kink (0 of 19,526 runs), CALIBRATED', verdict='supported',
         note='0 of 1485 (FD6) and 0 in the spectral runs. This is a sanity check, not a literature calibration, so the CALIBRATED label is a misuse (minor).'),
    dict(claim='E1d: producing fraction vs E/2M table; no coarse producer with A <= 0.3', verdict='supported',
         note='FD6 on the same 1485 points: 587 vs 564 producing, every band within 0.07, 0 producers with A <= 0.3. '
              'Point agreement 83% (80% at E > 2M) equals the original\'s own dx-halving agreement (80%). ' + samp_txt + '.'),
    dict(claim='E1d: lowest resolution-checked producers E/2M = 1.86 (baseline phi_t, (0.8, 2, 0.5)) and 2.70 (one-way phi_t, (0.6, 4, 0.5))',
         verdict='supported',
         note='FD6 lowest producer is the same point at 1.858. Spectral: (0.8, 2, 0.5) produces at dx 0.1 (E/2M = 1.8584) and dx 0.05 (%s); '
              'own one-way construction (0.6, 4, 0.5): E/2M = %s, produces %s / %s at dx 0.1 / 0.05. The raw 1.79 point is not '
              'a robust producer in any code.' % (
                  None if r1b is None else r1b['prod'], None if r3 is None else '%.4f' % r3['E_over_2M'],
                  None if r3 is None else r3['prod'], None if r3b is None else r3b['prod'])),
    dict(claim='E1d: single packets with A >~ 0.4 fold on their own (65% of producing coarse points)', verdict='supported',
         note='FD6 sample: 57/80 self-fold, 87%% agreement with the original. Spectral sigma = 16 scan: %s. A simple mechanism the report '
              'leaves unanalysed: the field at a trough, phi = -1 - A, already has potential energy above the barrier V(0) = 1/4 '
              'when A > sqrt2 - 1 = 0.414.' % sf_txt),
    dict(claim='E1d: the production boundary is ragged (fractured), CONFIRMED', verdict='supported',
         note='Qualitatively reproduced: on the sigma = 16, k = 1 line FD6 and the original both switch 17 times with onset A = 0.375 '
              '(80% point agreement). On the k = 2 line both are non-monotonic with the same onset and the same gap at A = 0.45-0.5, but '
              'with 9 vs 17 switches. Region, hole and switch counts are not converged numbers.'),
    dict(claim='E1d: slower packets produce more at matched energy (rho -0.82 to -0.88), CONFIRMED; seed claim "low speed holds"',
         verdict='overstated',
         note='The correlation reproduces (FD6: -0.82, -0.93, -0.92), but it is an amplitude effect. At matched energy slow packets have '
              'larger A (mean A 0.80-0.90 at v_g <= 0.47 against 0.36-0.42 at v_g >= 0.82 in the [2, 4) band). At fixed A '
              '(E > 2M) no amplitude level shows a significant negative speed trend in the original data (one marginal case, A = 0.5, '
              'p = 0.045) and none for collision-needed production. In the independent FD6 data the only significant fixed-A '
              'trend runs the other way (A = 1.2, rho = +0.75, p = 0.02). Computed by xc2_confound.py.'),
    dict(claim='E1d: no width preference at matched energy (NOT SUPPORTED)', verdict='supported',
         note='FD6: rho = -0.31, +0.12, +0.41, all p > 0.2.'),
    dict(claim='E1e: N_min lambda/m^2 = 1.24 (N = E/m), 1.69 (N_lin) Gaussian; 4.78 / 3.93 DSV; floor 2/3', verdict='supported',
         note='Scaling N lambda/m^2 = E~/(2 sqrt2) re-derived. The values are reproduced from independently built initial data '
              '(1.2389 / 1.6879; 4.7805 / 3.9278). They are upper bounds within the scanned families, as the report says.'),
    dict(claim='Seed section 2 AMENDED: "2M is a floor, not where classical production starts; a classical field needs extra energy for radiation and kink motion"',
         verdict='overstated',
         note='True only within the scanned families. The phi^4 equation is time-reversal invariant: reversing a slow (v << v_c) '
              'kink-antikink capture, whose bion radiates its energy away, gives radiation-only initial data that make a pair '
              'with E = 2M gamma(v) -> 2M. So the classical infimum is 2M. 1.86 / 2.70 / 7.2 x 2M are family-specific upper bounds '
              'on the onset. The seed\'s floor statement is consistent with E1 (no violation), so CONFIRMED, plus a note on '
              'generic data, fits better than AMENDED.'),
    dict(claim='Seed section 4: a small, spread-out packet is linear and passes through, CONFIRMED', verdict='supported',
         note='No producer with A <= 0.3 in either code.'),
    dict(claim='Seed section 4: pile in enough energy and the packet can fold, AMENDED (amplitude, not energy, controls it)',
         verdict='supported', note='Consistent with the local over-barrier threshold A* = 0.41 and with both codes\' fraction-vs-energy curves.'),
    dict(claim='Seed section 4: DSV trains make pairs over a wide range, "most easily at low speed", CONFIRMED', verdict='overstated',
         note='DSV and E1c both show production in an omega-dependent velocity band with nothing below it (omega = 0.90: no producer '
              'for v < 0.73 in the original grid). The lowest-energy producers are at omega = 0.90-0.95 and v = 0.62-0.73 '
              '(E/2M ~ 7), not at low v. What holds is that the band moves to lower v as the pulses weaken. AMENDED is the earned verdict.'),
    dict(claim='Seed sections 4 / 7.1: ragged boundary, CONFIRMED', verdict='supported', note='See the E1d ragged row.'),
    dict(claim='Seed section 8: classical pair needs N ~ (1.2-2) m^2/lambda quanta, QUANTIFIED; exponential suppression OPEN',
         verdict='supported', note='Numbers reproduced; OPEN is appropriate.'),
]

issues = [
    dict(severity='major',
         description='E1c headline "DSV example (0.99, 0.43) produces a pair (appears at t ~ 1160), still separating at 1.5T: CALIBRATED" '
                     'is not demonstrated. The point is resolution-sensitive and was never resolution-checked. The original code itself '
                     'produces at 4 of 10 (dx, dt) settings, with no monotone trend down to dt = 0.0025: (0.1, 0.04) yes; (0.1, 0.02) '
                     'yes; (0.1, 0.01) no; (0.05, 0.02 / 0.01 / 0.005) no; (0.025, 0.01) no; (0.025, 0.005) yes; (0.025, 0.0025) no; '
                     '(0.0125, 0.005) yes. Two independent, higher-order-in-time codes give no pair at all. The report\'s "the pair is '
                     'real: it is still separating at 1.5T" generalises from one discretisation. The dx = 0.05 rerun\'s 74/78 agreement '
                     'is trivial in the omega = 0.99 column, whose producing v (0.41, 0.43) are not on that grid; at dx = 0.05 the '
                     'original finds no omega = 0.99 producer at v = 0.38-0.48.',
         suggested_fix='Re-label the row: (0.99, 0.43) is a sensitive point whose call depends on dx and dt in every code (3 of 3 '
                       'independent runs give no pair). Report that a converged DSV-like producer exists at (0.99, 0.41): pair at '
                       't = 590 in the spectral code at three (dx, dt) settings and in the finest original setting. Replace "the pair '
                       'is real" with that statement, and add a resolution check for every map point that carries a verdict.'),
    dict(severity='major',
         description='Seed section 4 DSV claim marked CONFIRMED although its "most easily at low speed" part contradicts E1c\'s own map. '
                     'At fixed omega there is no production below the band (omega = 0.90: none for v < 0.73), and the lowest-energy '
                     'producers sit at v = 0.62-0.73.',
         suggested_fix='AMENDED: production occurs in an omega-dependent velocity band that moves to lower v as the pulses weaken; it '
                       'is not easiest at low speed.'),
    dict(severity='major',
         description='The E1d "slower produces more at matched energy" result (CONFIRMED, and "low speed holds" in the seed-claim '
                     'evidence) is confounded with amplitude. At matched energy slow packets carry larger A, and production is '
                     'controlled by A (self-folding needs A >~ 0.4). At fixed A no level shows a significant negative speed trend '
                     '(original: one marginal case, A = 0.5, p = 0.045; FD6: only A = 1.2, rho = +0.75), and collision-needed '
                     'production shows none at any A. In the '
                     'one-way form the collision-needed speed test is NOT SUPPORTED (results.json), yet the seed-claim text says '
                     'low speed holds in both forms.',
         suggested_fix='State that the matched-energy speed correlation is explained by amplitude. Report the fixed-A test, under '
                       'which no speed preference is found. Mark the PLAN speed prediction NOT SUPPORTED as a speed effect.'),
    dict(severity='major',
         description='Seed section 2 verdict AMENDED rests on "in classical dynamics 2M is a floor and not the onset; a classical field '
                     'needs extra energy for radiation and kink motion". That is true only of the scanned families. Time reversal of a '
                     'slow sub-v_c capture gives radiation-only data that make a pair at E -> 2M, so the classical infimum is 2M itself.',
         suggested_fix='Keep the data (no producer below 2M; family onsets 1.86 / 2.70 / 7.2 x 2M as upper bounds) and either mark the '
                       'claim CONFIRMED (floor holds) with a note on generic initial data, or restrict the amendment explicitly to the '
                       'scanned families.'),
    dict(severity='minor',
         description='CALIBRATED is used for the energy-conservation sanity check (no production below 2M); PLAN defines CALIBRATED as '
                     'reproducing a literature target.',
         suggested_fix='Use CONFIRMED or "check passed".'),
    dict(severity='minor',
         description='Region, hole and switch counts of the slices appear in the headline and seed-claim evidence as numbers, but they '
                     'are not converged. On the sigma = 16, k = 2 line the independent code switches 9 times against the original\'s 17 '
                     '(same onset, same gap). The report says this in the text but still quotes the counts as results.',
         suggested_fix='Quote the counts as illustrative only, and lead with the robust statements: onset A, non-monotonic lines in '
                       'both codes, production fractions.'),
    dict(severity='minor',
         description='The self-folding mechanism is called unanalysed, but the observed threshold (minimum A 0.375-0.425) matches a '
                     'one-line estimate: a trough at phi = -1 - A has potential energy above the barrier 1/4 when A > sqrt2 - 1 = '
                     '0.414. Most E1d production (65%) is this local over-barrier effect rather than collision dynamics, which limits '
                     'what the fraction-vs-energy curves say about collisions.',
         suggested_fix='Add the estimate and separate collision-needed statistics in the headline.'),
    dict(severity='minor',
         description='The E1c table simplifies DSV Fig. 2 in places. Omega = 0.95 is given as 0.64-0.77; the figure shows gaps '
                     '(about 0.64-0.65, 0.67-0.70, 0.72-0.73, 0.75-0.77). Point-level overlap with DSV is only about 2/3.',
         suggested_fix='Quote the hit / false-positive counts rather than "band by band".'),
    dict(severity='minor',
         description='The report has no diagnosis for the 2.6e-4 v_c offset. The independent spectral code (other x0, box and '
                     'integrator) lands within 1e-5 of the original, so the offset lies in the [summary] target, not in either '
                     'computation.',
         suggested_fix='Say so; keep CALIBRATED (inside +-0.001).'),
]

summary = ('Independent recomputation with two different codes (6th-order FD + RK4; Fourier exact-linear 4th-order splitting) '
           'plus collocation and Chebyshev solvers. E1a, E1b (v_c 0.260066 vs 0.26006; first window to 1e-5), the E1c map trend, '
           'pass-through and omega > 0.99 null, all E1d statistics (564 vs 587 producing coarse runs; band fractions within 0.07; '
           'zero producers below 2M or with A <= 0.3; the same lowest producers; self-folding; ragged lines) and the E1e quanta '
           'counts are confirmed. Point-level E1d calls agree 73-84% between codes, the same as the original\'s own dx-halving '
           'agreement (80%). One headline calibration is not demonstrated: the DSV example point (0.99, 0.43) is '
           'resolution-sensitive. The original code produces it at 4 of 10 (dx, dt) settings, the independent codes never do; '
           'a converged DSV-like producer exists at (0.99, 0.41). Three seed-level verdicts are overstated: section 4 DSV "most '
           'easily at low speed"; the E1d low-speed preference, which is an amplitude confound; and the section 2 AMENDED '
           'rationale, which is family-specific since the ''classical infimum is 2M by time reversal.')

json.dump(dict(claim_audit=claims, issues=issues, overall='confirmed_with_corrections', summary=summary),
          open(os.path.join(HERE, 'xc2_audit_text.json'), 'w'), indent=1)
print('claims', len(claims), 'issues', len(issues))
