"""
E10 Route B, B4: verdicts (PREREG_B4 §5, applied literally) and b4_results.json.  Label: Exploration.

Per-run end-state class (from b4_hist/<run>.json, last record; history for the mechanism):
  collapse : no det-H vortex plaquette left, or R_f / r_q < 1
             mechanism: 'unwinding first' if tau < 0.1 at a recorded iteration before the collapse iteration,
             'charge loss first' if leak > 1 % or omega >= m_bulk before it (whichever came first), else
             'plain shrinkage'
  expands  : R_f > rho_max - 4 (the vortex inside the 4-unit edge band; reading of "reaches the box edge")
  leak     : leak > 1 % or omega >= m_bulk
  ring     : otherwise
Pair verdict (n = 3: M3a/M3b; n = 5: M5a/M5b):
  both collapse -> COLLAPSE (mechanisms listed); both leak -> LEAK; both expand -> EXPANDS;
  both ring: STABLE (absolute) if |R_f,a - R_f,b| / mean <= 10 %, R_f/r_q >= 2, tau >= 0.5, omega < m, leak < 1 %,
             h = 0.125 check passes (both), E < min(m Q, E_disp) (both); METASTABLE if all but the last;
             otherwise MARGINAL;
  any other combination -> MARGINAL.
E_disp(n = 3) = E(C-d), E_disp(n = 5) = E(C-d5).
"Reading" choices are recorded in REPORT_B4.md (deviations / ambiguities).
"""
import os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
HD = os.path.join(HERE, 'b4_hist')
MB = 1.0
RHO_MAX = 40.0


def load(tag):
    f = os.path.join(HD, tag + '.json')
    return json.load(open(f)) if os.path.exists(f) else None


def has_core(o):
    return o['n_vortex_plaquettes'] > 0


def classify(rec):
    end = rec['end']; hist = rec['history']
    def collapsed(o):
        return (not has_core(o)) or (o['r_q'] is not None and o['R_f'] is not None and o['R_f'] / o['r_q'] < 1)
    if collapsed(end):
        ic = next(o['iter'] for o in hist if collapsed(o))
        tu = next((o['iter'] for o in hist if o['tau'] is not None and o['tau'] < 0.1), None)
        tl = next((o['iter'] for o in hist if (o['leak'] or 0) > 0.01 or (o['omega_over_mbulk'] or 0) >= 1.0), None)
        cand = [(t, m) for t, m in ((tu, 'unwinding first (tau < 0.1, then shrinkage)'), (tl, 'charge loss first'))
                if t is not None and t < ic]
        mech = min(cand)[1] if cand else 'plain shrinkage'
        return dict(cls='collapse', mechanism=mech, collapse_iter=ic, tau_lt_0p1_iter=tu, charge_loss_iter=tl)
    if end['R_f'] is not None and end['R_f'] > RHO_MAX - 4:
        return dict(cls='expands')
    if (end['leak'] or 0) > 0.01 or (end['omega_over_mbulk'] or 0) >= 1.0:
        return dict(cls='leak')
    return dict(cls='ring')


def fine_check(tag):
    c, f = load(tag), load(tag + '_fine')
    if c is None or f is None or 'end' not in f:
        return None
    ec, ef = c['end'], f['end']
    if ec['R_f'] is None or ef['R_f'] is None or not has_core(ef):
        return dict(passes=False, reason='no core at h = 0.125', E_c=ec['E'], E_f=ef['E'])
    dR = abs(ef['R_f'] / ec['R_f'] - 1); dE = abs(ef['E'] / ec['E'] - 1)
    return dict(passes=bool(dR < 0.05 and dE < 1e-3), dR_rel=dR, dE_rel=dE, R_f=[ec['R_f'], ef['R_f']], E=[ec['E'], ef['E']])


def pair(n, Edisp):
    a, b = load(f'M{n}a'), load(f'M{n}b')
    if a is None or b is None or 'end' not in a or 'end' not in b:
        return dict(verdict='INCOMPLETE')
    ca, cb = classify(a), classify(b)
    mQ = MB * a['spec']['Q']
    out = dict(n=n, Q=a['spec']['Q'], m_bulk_Q=mQ, E_disp=Edisp, runs={f'M{n}a': ca, f'M{n}b': cb})
    for k, r in ((f'M{n}a', a), (f'M{n}b', b)):
        e = r['end']
        out['runs'][k].update(E=e['E'], E_over_mQ=e['E'] / mQ, E_over_Edisp=(e['E'] / Edisp if Edisp else None),
                              R_f=e['R_f'], r_q=e['r_q'], R_q=e['R_q'], tau=e['tau'], omega_over_mbulk=e['omega_over_mbulk'],
                              leak=e['leak'], iters=e['iter'], message=e.get('message'), fine=fine_check(k))
    cl = {ca['cls'], cb['cls']}
    if cl == {'collapse'}:
        out['verdict'] = 'COLLAPSE'; out['mechanism'] = [ca['mechanism'], cb['mechanism']]
    elif cl == {'leak'}:
        out['verdict'] = 'LEAK'
    elif cl == {'expands'}:
        out['verdict'] = 'EXPANDS'
    elif cl == {'ring'}:
        ra, rb = out['runs'][f'M{n}a'], out['runs'][f'M{n}b']
        conds = dict(
            same_R_f_10pc=abs(ra['R_f'] - rb['R_f']) / (0.5 * (ra['R_f'] + rb['R_f'])) <= 0.10,
            R_f_over_r_q_ge_2=all(r['R_f'] / r['r_q'] >= 2 for r in (ra, rb)),
            tau_ge_0p5=all(r['tau'] >= 0.5 for r in (ra, rb)),
            omega_lt_m=all(r['omega_over_mbulk'] < 1 for r in (ra, rb)),
            leak_lt_1pc=all(r['leak'] < 0.01 for r in (ra, rb)),
            fine_check=all(r['fine'] is not None and r['fine']['passes'] for r in (ra, rb)),
        )
        Emin = min(mQ, Edisp) if Edisp is not None else mQ
        conds['E_lt_min_mQ_Edisp'] = all(r['E'] < Emin for r in (ra, rb))
        out['conditions'] = {k: bool(v) for k, v in conds.items()}
        base = all(v for k, v in conds.items() if k != 'E_lt_min_mQ_Edisp')
        out['verdict'] = ('STABLE (absolute)' if base and conds['E_lt_min_mQ_Edisp'] else
                          'METASTABLE' if base else 'MARGINAL')
    else:
        out['verdict'] = 'MARGINAL'; out['reason'] = f'starts ended in different classes: {ca["cls"]}, {cb["cls"]}'
    return out


def controls():
    out = {}
    for k in ('C-a', 'C-b', 'C-c', 'C-d', 'C-d5'):
        r = load(k)
        if r is None or 'end' not in r:
            out[k] = None; continue
        e = r['end']
        d = dict(E=e['E'], R_f=e['R_f'], n_vortex_plaquettes=e['n_vortex_plaquettes'], tau=e['tau'], r_q=e['r_q'],
                 R_q=e['R_q'], leak=e['leak'], omega_over_mbulk=e['omega_over_mbulk'], I=e['I'], iters=e['iter'],
                 message=e.get('message'))
        if k in ('C-a', 'C-b', 'C-c'):
            d['class'] = classify(r)
        if k in ('C-d', 'C-d5'):
            d['m_bulk_Q'] = r['spec']['Q']
            d['E_over_mQ'] = e['E'] / r['spec']['Q']
            d['localized_lump'] = bool(e['leak'] is not None and e['leak'] < 0.01 and e['r_q'] is not None)
        out[k] = d
    return out


if __name__ == '__main__':
    C = controls()
    Ed3 = C['C-d']['E'] if C.get('C-d') else None
    Ed5 = C['C-d5']['E'] if C.get('C-d5') else None
    V = {3: pair(3, Ed3), 5: pair(5, Ed5)}
    for n, Ed, cd in ((3, Ed3, C.get('C-d')), (5, Ed5, C.get('C-d5'))):
        v = V[n]
        if cd and v.get('runs'):
            Emain = min(r['E'] for r in v['runs'].values())
            v['string_not_required'] = bool(cd['localized_lump'] and cd['E'] < Emain)
    V['n_dependence'] = 'n-dependent' if V[3].get('verdict') != V[5].get('verdict') else 'same verdict at n = 3 and 5'
    V['carried_forward'] = V[5].get('verdict')
    reg = load('REG')
    res = dict(label='Exploration', prereg='PREREG_B4.md', verdicts=V, controls=C,
               regression=(reg['end'] if reg and 'end' in reg else None))
    json.dump(res, open(os.path.join(HERE, 'b4_verdicts.json'), 'w'), indent=1, default=float)
    print(json.dumps(res, indent=1, default=float))
