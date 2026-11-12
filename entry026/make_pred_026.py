"""make_pred_026.py -- assemble the frozen predictions and the power table for Entry 026.
Reads ladder_{arm}_{q}.json (exact absorption ladder, predict_026.py) and writes pred_026.json.
Rules (fixed in the entry):
  c216  = ladder value with nothing absorbed (LO-S eq. 2.16 at modulus q).
  cfull = ladder value with every prime <= 19 absorbed (except those dividing q).
  tau   = 3 * max(|step 13|, |step 17|, |step 19|), the model tolerance.
Planned sample sizes: E all pairs in [1e12, 1.02e12) (about 7.24e8); R64 10,000 and R128 20,000 runs x 9,999 pairs.
Planned s.e. = binomial sqrt((1 - c^2)/N) (conservative for arm E, whose counts scatter sub-multinomially).
"""
import json, math
from scipy import stats
ARMS = ['E', 'R64', 'R128']; QS = (3, 4, 5)
NAME = {3: 'chi_-3', 4: 'chi_-4', 5: '(./5)'}
NPAIRS = {'E': 7.24e8, 'R64': 10_000 * 9_999, 'R128': 20_000 * 9_999}
cells = {}
for a in ARMS:
    for q in QS:
        d = json.load(open(f'ladder_{a}_{q}.json'))
        P = d['P']; c = {int(k): v for k, v in d['corr'].items()}
        ladder = {'-': c[0]}
        for k in range(1, len(P) + 1): ladder[str(P[k - 1])] = c[k]
        steps = {str(P[k - 1]): c[k] - c[k - 1] for k in range(1, len(P) + 1)}
        tau = 3 * max(abs(steps[p]) for p in ('13', '17', '19'))
        c216, cfull = c[0], c[len(P)]
        if a != 'E':
            # random starts are uniform in y: uniform-in-y average over [2^(b-1), 2^b) replaces the local
            # density at 2^(b-0.5). (2.16) is evaluated directly; for the absorbed rungs the shift
            # computed through 17 is added (it changes by < 1e-7 from 11 to 17; ushift_*.log).
            us = json.load(open(f'ushift_{a}_{q}.json'))
            s0 = us['0'][1] - us['0'][0]; s17 = us['6'][1] - us['6'][0]
            c216 = us['0'][1]; cfull = cfull + s17
            ladder = {k: v + (s0 if k == '-' else s17) for k, v in ladder.items()}
        cells[f'{a}_{q}'] = dict(c216=c216, cfull=cfull, tau=tau, ladder=ladder, steps=steps, absorbed=P)
n_dec = 9 + 9 + 3
alpha = 0.01 / n_dec
z1, z2 = stats.norm.isf(alpha), stats.norm.isf(alpha / 2)
pred = dict(alpha_prime=alpha, n_decisive=n_dec, cells=cells, npairs_planned=NPAIRS,
            decisive=dict(T216=[], Tfull=[], Theight=['3', '4', '5']))
print(f"alpha' = 0.01/{n_dec} = {alpha:.3e}; z one-sided {z1:.3f}, two-sided {z2:.3f}\n")
print("cell        (2.16)      full HL     ratio   tau      tau/|c|  planned se  T216 power (gap-tau)  Tfull miss@80%")
for a in ARMS:
    for q in QS:
        x = cells[f'{a}_{q}']; c = x['cfull']; N = NPAIRS[a]
        se = math.sqrt((1 - c * c) / N)
        gap = abs(x['cfull'] - x['c216']) - x['tau']
        pw = stats.norm.cdf(gap / se - z1)
        miss = x['tau'] + (z2 + stats.norm.isf(0.2)) * se
        x.update(se_planned=se, power_T216=pw, Tfull_miss80=miss)
        pred['decisive']['T216'].append(f'{a}_{q}') if pw >= 0.8 else None
        pred['decisive']['Tfull'].append(f'{a}_{q}')
        print(f"{a:4s} {NAME[q]:7s} {x['c216']:+.6f}  {c:+.6f}  {c/x['c216']:.4f}  {x['tau']:.2e} {x['tau']/abs(c)*100:5.2f}%  {se:.2e}    {pw:.3f}               {miss:.2e} ({miss/abs(c)*100:.2f}%)")
print()
for q in QS:
    e, h = cells[f'E_{q}'], cells[f'R128_{q}']
    D = e['cfull'] / e['c216'] - h['cfull'] / h['c216']
    Dlow = D - e['tau'] / abs(e['c216']) - h['tau'] / abs(h['c216'])
    se = math.hypot(e['se_planned'] / abs(e['c216']), h['se_planned'] / abs(h['c216']))
    pw = stats.norm.cdf(Dlow / se - z1)
    print(f"Theight {NAME[q]}: D predicted {D:+.4f} (lowest within tau {Dlow:+.4f}), planned se {se:.4f}, power {pw:.3f}")
    pred[f'Theight_{q}'] = dict(D=D, Dlow=Dlow, se_planned=se, power=pw)
if len(pred['decisive']['T216']) < 9:
    print("NOTE: some T216 cells below 0.8 power are report-only; alpha' was computed for 21 tests (conservative).")
json.dump(pred, open('pred_026.json', 'w'), indent=1)
