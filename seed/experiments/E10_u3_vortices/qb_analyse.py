"""
E10 Route B, QB: verdicts (PREREG_QB §3-§5, applied literally), tables, qb_results.json.  Label: Exploration.

  python3 qb_analyse.py regression   QB-P1 (exit 1 if it fails)
  python3 qb_analyse.py checklist    the box / resolution check runs required by the main-grid verdicts
  python3 qb_analyse.py              everything -> qb_results.json, markdown tables on stdout

Per-run verdict (end state; m = min(1, lam)):
  BOUND      leak < 1 % and E/(m Q) < 0.995 and omega/m < 1 and 3D charge rms radius < 15
  DISPERSED  leak >= 1 % or E/(m Q) >= 1
  MARGINAL   otherwise
Per (lam, Q): the verdict of the start with the lower final E (both reported).
Box check: per lam, the largest-Q and the smallest-Q BOUND point (its lower-E start), re-relaxed in rho in [0, 60],
z in [-30, 30].  Resolution check: per lam with any BOUND point, one BOUND point (reading: the smallest-Q one, the one
nearest the threshold) at h = 0.125.  Pass: same verdict and |dE/E| < 1e-3.
Q_min(lam) bracket: (largest DISPERSED Q, smallest BOUND Q].
Classification: B = {lam with >= 1 BOUND point on the main grid}, W = {0.8, 0.9, 1.0}.
"""
import os, sys, json
import numpy as np
import qb_run as R

HERE = os.path.dirname(os.path.abspath(__file__))
E_REG = 1589.9110            # PREREG_QB §1 (B4 C-d, rounded); B4's unrounded value is also reported
W = [0.8, 0.9, 1.0]


def load(tag):
    f = os.path.join(R.HD, tag + '.json')
    if not os.path.exists(f):
        return None
    r = json.load(open(f))
    return r if 'end' in r else None


def run_verdict(e, mb, Q):
    eq = e['E'] / (mb * Q)
    if e['leak'] < 0.01 and eq < 0.995 and e['omega_over_mbulk'] < 1 and e['r_rms_3D'] < 15:
        return 'BOUND'
    if e['leak'] >= 0.01 or eq >= 1:
        return 'DISPERSED'
    return 'MARGINAL'


def summary(tag):
    r = load(tag)
    if r is None:
        return None
    e = r['end']; mb = r['m_bulk']; Q = r['Q']
    return dict(tag=tag, lam=r['lam'], Q=Q, start=r['start_id'], variant=r['variant'], h=r['h'], box=r['box'],
                E=e['E'], E_over_mQ=e['E'] / (mb * Q), omega_over_mbulk=e['omega_over_mbulk'], leak=e['leak'],
                r_rms_3D=e['r_rms_3D'], r_q=e['r_q'], R_q=e['R_q'], z_q=e['z_q'], I=e['I'],
                detH07_radius=e['detH07_radius'], detH07_rho_max=e['detH07_rho_max'],
                detH07_absz_max=e['detH07_absz_max'], detH_origin=e['detH_origin'], detH_min=e['detH_min_abs'],
                charge_within_r5_r10_r15=e['charge_within_r5_r10_r15'], tau=e['tau'],
                iters=e['iter'], message=e['message'], grad_max=e['grad_max'], restarts=r.get('restarts', 0),
                seconds=e['seconds'], verdict=run_verdict(e, mb, Q))


def regression():
    s = summary('L1.0_Q1626.5329_S1')
    b4 = json.load(open(os.path.join(HERE, 'b4_hist', 'C-d.json')))['end']['E']
    if s is None:
        return None
    d = abs(s['E'] / E_REG - 1); d4 = abs(s['E'] / b4 - 1)
    return dict(E=s['E'], E_target=E_REG, rel_dev=d, E_B4_unrounded=b4, rel_dev_unrounded=d4, passes=bool(d < 1e-6),
                iters=s['iters'], message=s['message'])


def grid():
    pts = {}
    for lam in R.LAMS:
        for Q in R.QS:
            ss = {k: summary(R.tag_of(lam, Q, k)) for k in R.STARTS}
            if any(v is None for v in ss.values()):
                pts[(lam, Q)] = dict(lam=lam, Q=Q, verdict='INCOMPLETE', starts=ss); continue
            lo = min(ss, key=lambda k: ss[k]['E'])
            pts[(lam, Q)] = dict(lam=lam, Q=Q, lower=lo, verdict=ss[lo]['verdict'], starts=ss,
                                 dE_S2_minus_S1=ss['S2']['E'] - ss['S1']['E'],
                                 same_verdict=ss['S1']['verdict'] == ss['S2']['verdict'])
    return pts


def check_targets(pts):
    box, fine = {}, {}
    for lam in R.LAMS:
        bq = [Q for Q in R.QS if pts[(lam, Q)]['verdict'] == 'BOUND']
        if not bq:
            continue
        tg = lambda Q: R.tag_of(lam, Q, pts[(lam, Q)]['lower'])
        box[lam] = sorted({tg(max(bq)), tg(min(bq))})
        fine[lam] = tg(min(bq))
    return box, fine


def check_result(base, variant):
    b, c = summary(base), summary(base + '_' + variant)
    if b is None or c is None:
        return dict(base=base, variant=variant, status='INCOMPLETE')
    dE = abs(c['E'] / b['E'] - 1)
    return dict(base=base, variant=variant, E=[b['E'], c['E']], rel_dE=dE, verdict=[b['verdict'], c['verdict']],
                E_over_mQ=[b['E_over_mQ'], c['E_over_mQ']], leak=[b['leak'], c['leak']],
                omega_over_mbulk=[b['omega_over_mbulk'], c['omega_over_mbulk']], r_rms_3D=[b['r_rms_3D'], c['r_rms_3D']],
                iters=c['iters'], message=c['message'],
                passes=bool(b['verdict'] == c['verdict'] and dE < 1e-3))


def qmin(pts, lam):
    d = [Q for Q in R.QS if pts[(lam, Q)]['verdict'] == 'DISPERSED']
    b = [Q for Q in R.QS if pts[(lam, Q)]['verdict'] == 'BOUND']
    lo = max(d) if d else None; hi = min(b) if b else None
    note = None
    if lo is not None and hi is not None and lo > hi:
        note = 'non-monotone: a DISPERSED Q lies above the smallest BOUND Q'
    return dict(largest_dispersed_Q=lo, smallest_bound_Q=hi, note=note,
                text=(f'({lo if lo is not None else 0:g}, {hi:g}]' if hi is not None else
                      f'> {max(R.QS):g} (no BOUND point)'))


def classify(B):
    sB, sW = set(B), set(W)
    if sB == sW:
        return 'TRACKS'
    if sB > sW:
        return 'BROADER'
    if sB < sW:
        return 'NARROWER'
    return 'MIXED'


def f(x, p=4):
    if x is None:
        return '—'
    if isinstance(x, (int, np.integer)):
        return str(x)
    if x != 0 and (abs(x) < 1e-3 or abs(x) >= 1e5):
        return f'{x:.2e}'
    return f'{x:.{p}f}'


def main():
    reg = regression()
    pts = grid()
    box, fine = check_targets(pts)
    boxr = {lam: [check_result(t, 'box') for t in ts] for lam, ts in box.items()}
    finer = {lam: check_result(t, 'fine') for lam, t in fine.items()}
    B = [lam for lam in R.LAMS if any(pts[(lam, Q)]['verdict'] == 'BOUND' for Q in R.QS)]
    cls = classify(B)
    qm = {lam: qmin(pts, lam) for lam in R.LAMS}
    # predictions
    p3a = {}
    for lam in B:
        bq = [Q for Q in R.QS if pts[(lam, Q)]['verdict'] == 'BOUND']
        e = [pts[(lam, Q)]['starts'][pts[(lam, Q)]['lower']]['E_over_mQ'] for Q in bq]
        p3a[lam] = dict(Q=bq, E_over_mQ=e, falls=bool(all(e[i + 1] < e[i] for i in range(len(e) - 1))))
    sb = [qm[lam]['smallest_bound_Q'] for lam in R.LAMS]
    sbv = [x if x is not None else np.inf for x in sb]
    rises = bool(all(sbv[i + 1] >= sbv[i] for i in range(len(sbv) - 1)) and sbv[-1] > sbv[0])
    p34 = pts[(1.2, 2710.9)]
    s4 = p34['starts'][p34['lower']] if p34['verdict'] != 'INCOMPLETE' else None
    preds = {
        'QB-P1': dict(holds=bool(reg and reg['passes']), detail=reg),
        'QB-P2': dict(holds=cls == 'BROADER' and all(any(pts[(l, Q)]['verdict'] == 'BOUND' for Q in R.QS[-2:]) for l in (1.1, 1.2)),
                      classification=cls),
        "QB-P2'": dict(holds=cls == 'TRACKS', classification=cls),
        'QB-P3': dict(holds=bool(all(v['falls'] for v in p3a.values()) and rises),
                      E_over_mQ_falls_with_Q=p3a, Q_min_rises_with_lam=rises, smallest_bound_Q=sb,
                      reading='falls: strictly decreasing over the BOUND Q at each lam in B; rises: smallest BOUND Q '
                              'non-decreasing in lam and larger at lam = 1.2 than at 0.8 (no BOUND = +inf)'),
        'QB-P4': dict(holds=bool(s4 and p34['verdict'] == 'BOUND' and 0.95 < s4['E_over_mQ'] < 0.995),
                      verdict=p34['verdict'], E_over_mQ=s4['E_over_mQ'] if s4 else None),
    }
    out = dict(label='Exploration', prereg='PREREG_QB.md', regression=reg,
               runs={s['tag']: s for p in pts.values() for s in p['starts'].values() if s},
               points=[dict({k: v for k, v in p.items() if k != 'starts'},
                            S1=p['starts']['S1'] and {k: p['starts']['S1'][k] for k in ('E', 'E_over_mQ', 'verdict')},
                            S2=p['starts']['S2'] and {k: p['starts']['S2'][k] for k in ('E', 'E_over_mQ', 'verdict')})
                       for p in pts.values()],
               box_check={str(k): v for k, v in boxr.items()}, resolution_check={str(k): v for k, v in finer.items()},
               check_runs={t + '_' + vv: summary(t + '_' + vv) for lam, ts in box.items() for t in ts for vv in ('box',)} |
                          {t + '_fine': summary(t + '_fine') for t in fine.values()},
               B=B, W=W, classification=cls, Q_min={str(k): v for k, v in qm.items()}, predictions=preds)
    json.dump(out, open(os.path.join(HERE, 'qb_results.json'), 'w'), indent=1, default=float)

    # ---- tables ----
    print('## regression'); print(json.dumps(reg, indent=1))
    print('\n## all runs')
    print('| λ | Q | start | E | E/(m Q) | ω/m | leak | 3D rms | r_q | \\|det H\\|<0.7 radius | iters | stop | verdict |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for p in pts.values():
        for k, s in p['starts'].items():
            if s is None:
                print(f"| {p['lam']} | {p['Q']:g} | {k} | (not done) |"); continue
            print(f"| {s['lam']} | {s['Q']:g} | {k} | {f(s['E'])} | {f(s['E_over_mQ'], 5)} | {f(s['omega_over_mbulk'], 5)} | "
                  f"{f(s['leak'])} | {f(s['r_rms_3D'], 3)} | {f(s['r_q'], 3)} | {f(s['detH07_radius'], 3)} | {s['iters']} | "
                  f"{'ftol' if s['message'].startswith('ftol') else s['message']} | {s['verdict']} |")
    print('\n## verdict grid (lower-E start; S1/S2 verdicts in brackets)')
    print('| λ \\ Q | ' + ' | '.join(f'{Q:g}' for Q in R.QS) + ' | Q_min bracket |')
    print('|---|' + '---|' * (len(R.QS) + 1))
    for lam in R.LAMS:
        cells = []
        for Q in R.QS:
            p = pts[(lam, Q)]
            if p['verdict'] == 'INCOMPLETE':
                cells.append('—'); continue
            cells.append(f"**{p['verdict']}** ({p['lower']}; {p['starts']['S1']['verdict'][0]}/{p['starts']['S2']['verdict'][0]}) "
                         f"{p['starts'][p['lower']]['E_over_mQ']:.4f}")
        print(f'| {lam} | ' + ' | '.join(cells) + f" | {qm[lam]['text']} |")
    print('\n## box check'); print(json.dumps(out['box_check'], indent=1, default=float))
    print('\n## resolution check'); print(json.dumps(out['resolution_check'], indent=1, default=float))
    print('\nB =', B, ' W =', W, ' classification:', cls)
    print('\n## predictions'); print(json.dumps(preds, indent=1, default=float))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'regression':
        r = regression(); print(json.dumps(r, indent=1))
        sys.exit(0 if r and r['passes'] else 1)
    if len(sys.argv) > 1 and sys.argv[1] == 'checklist':
        pts = grid()
        assert all(p['verdict'] != 'INCOMPLETE' for p in pts.values()), 'grid incomplete'
        box, fine = check_targets(pts)
        ts = [t + '_box' for v in box.values() for t in v] + [t + '_fine' for t in fine.values()]
        print('\n'.join(ts))
    else:
        main()
