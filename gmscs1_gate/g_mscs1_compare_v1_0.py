#!/usr/bin/env python3
"""g_mscs1_compare_v1_0.py -- Gate G-MSCS1 two-leg comparator, v1.0 (CANDIDATE; freezes on the author's lock word).

Usage
  compare  --chat CK --cc CK [--chat-cmp CMP --cc-cmp CMP] [--schema g_mscs1_schema_v1_0.json] [--out OUT]
  selftest [--schema ...]

All lock constants and tolerances come from the schema file; this file carries no gate numbers.
Checks (every verdict-bearing quantity is a boolean, a label, or a float with a declared tolerance;
free text is NEVER compared):
  C-M-0  provenance: required keys; memo_md5/bytes == lock; ledger base; T1 list md5 == lock and state CLEAN;
         X-1 md5/bytes; instrument_md5 real 32-hex; no placeholders; INDEPENDENCE WITNESS (instrument md5s differ,
         checkpoints not byte-identical); elections by canonical choice code
  C1     controls: every passed flag True on both legs; control floats within control_abs
  C2     phase1: per config key -- v_* within phase1_v_rel; r_xtal_* within phase1_r_abs; lambda_* within
         phase1_lambda_abs; cov within phase1_cov_abs; shares key-for-key within phase1_share_abs; branch label exact
  C3     phase2: pins within pins_rel; r_agg arrays elementwise within r_agg_abs; S_t within S_t_abs;
         kappa2 within max(kappa2_rel*|x|, kappa2_abs_floor); halving_dev_kappa2 <= kappa2_rel on each leg;
         lambda_mean_t elementwise within phase1_lambda_abs; born_t0 per base config within born_rel
  C4     falsifier states + verdict_class exact and in domain; quadrature n_theta/n_phi identical; t_grid == schema
  C5     compare-step identity (when both compare files supplied): rows id+concordant identical; verdict_class identical
Any MISS -> S9 counter-cross-check. Representational-vs-definitional classification is a human step after this report.
"""
import argparse, hashlib, json, os, re, sys, copy, math

HEX32 = re.compile(r'^[0-9a-f]{32}$')
PLACEHOLDER = re.compile(r'<[a-z_ ]+>|TBD|PLACEHOLDER|xxxx')
SCHEMA_DEFAULT = 'g_mscs1_schema_v1_0.json'


def md5f(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def getpath(d, dotted):
    cur = d
    for k in dotted.split('.'):
        if not isinstance(cur, dict) or k not in cur:
            return None, False
        cur = cur[k]
    return cur, True


def choice_code(s):
    m = re.match(r'\s*\(([^)]+)\)', str(s))
    return m.group(1).strip() if m else None


def close_abs(a, b, tol):
    return isinstance(a, (int, float)) and isinstance(b, (int, float)) and math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol


def close_rel(a, b, tol, floor=0.0):
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))) or not (math.isfinite(a) and math.isfinite(b)):
        return False
    return abs(a - b) <= max(tol * max(abs(a), abs(b)), floor)


def run_checks(chat, cc, S, chat_cmp=None, cc_cmp=None, chat_bytes=None, cc_bytes=None):
    R = []
    T = S['tolerances']

    def rec(check, item, ok, a=None, b=None):
        R.append({'check': check, 'item': item, 'result': 'PASS' if ok else 'MISS', 'chat': a, 'cc': b})

    # ---- C-M-0 provenance
    for leg, ck in (('chat', chat), ('cc', cc)):
        for key in S['required_keys']:
            _, present = getpath(ck, key); rec('C-M-0', f'{leg}: required key {key}', present)
        rec('C-M-0', f'{leg}: memo_md5 == lock', ck.get('memo_md5') == S['memo_lock_md5'], ck.get('memo_md5'), S['memo_lock_md5'])
        rec('C-M-0', f'{leg}: memo_bytes == lock', ck.get('memo_bytes') == S['memo_lock_bytes'], ck.get('memo_bytes'), S['memo_lock_bytes'])
        rec('C-M-0', f'{leg}: ledger_base_md5', ck.get('ledger_base_md5') == S['ledger_base_md5'])
        v, _ = getpath(ck, 'T1.list_md5'); rec('C-M-0', f'{leg}: T1 list md5 == lock', v == S['t1_list_md5'], v, S['t1_list_md5'])
        v, _ = getpath(ck, 'T1.state'); rec('C-M-0', f'{leg}: T1 state CLEAN', v == 'CLEAN', v)
        v, _ = getpath(ck, 'inputs.X1_md5'); rec('C-M-0', f'{leg}: X-1 md5', v == S['x1_md5'], v)
        v, _ = getpath(ck, 'inputs.X1_bytes'); rec('C-M-0', f'{leg}: X-1 bytes', v == S['x1_bytes'], v)
        rec('C-M-0', f'{leg}: instrument_md5 real 32-hex', bool(HEX32.match(str(ck.get('instrument_md5', '')))))
        rec('C-M-0', f'{leg}: no placeholders', not PLACEHOLDER.search(json.dumps(ck, ensure_ascii=False)))
        for e, code in S['value_domains']['election_choice'].items():
            got = choice_code((ck.get('elections') or {}).get(e))
            rec('C-M-0', f'{leg}: election {e} code', got == code, got, code)
    rec('C-M-0', 'INDEPENDENCE: instrument_md5 differ', chat.get('instrument_md5') != cc.get('instrument_md5'),
        chat.get('instrument_md5'), cc.get('instrument_md5'))
    if chat_bytes is not None and cc_bytes is not None:
        rec('C-M-0', 'INDEPENDENCE: checkpoints not byte-identical', chat_bytes != cc_bytes)

    # ---- C1 controls
    for name, fkeys in S['control_float_keys'].items():
        pa, _ = getpath(chat, f'controls.{name}.passed'); pb, _ = getpath(cc, f'controls.{name}.passed')
        rec('C1', f'{name}.passed (both True)', pa is True and pb is True, pa, pb)
        for k in fkeys:
            a, _ = getpath(chat, f'controls.{name}.{k}'); b, _ = getpath(cc, f'controls.{name}.{k}')
            rec('C1', f'{name}.{k}', close_abs(a, b, T['control_abs']), a, b)

    # ---- C2 phase1
    p1a, p1b = chat.get('phase1', {}), cc.get('phase1', {})
    rec('C2', 'config key set', set(p1a) == set(p1b) == set(S['config_keys']), sorted(p1a), sorted(p1b))
    for key in S['config_keys']:
        ra, rb = p1a.get(key, {}), p1b.get(key, {})
        for k in ('v_EM', 'v_S2E2', 'v_S2h'):
            rec('C2', f'[{key}].{k}', close_rel(ra.get(k), rb.get(k), T['phase1_v_rel']), ra.get(k), rb.get(k))
        for k in ('r_xtal_E2', 'r_xtal_h'):
            rec('C2', f'[{key}].{k}', close_abs(ra.get(k), rb.get(k), T['phase1_r_abs']), ra.get(k), rb.get(k))
        for k in ('lambda_mean', 'lambda_max'):
            rec('C2', f'[{key}].{k}', close_abs(ra.get(k), rb.get(k), T['phase1_lambda_abs']), ra.get(k), rb.get(k))
        rec('C2', f'[{key}].cov_lambda_v', close_abs(ra.get('cov_lambda_v'), rb.get('cov_lambda_v'), T['phase1_cov_abs']),
            ra.get('cov_lambda_v'), rb.get('cov_lambda_v'))
        rec('C2', f'[{key}].lambda_max_branch', ra.get('lambda_max_branch') == rb.get('lambda_max_branch')
            and ra.get('lambda_max_branch') in S['value_domains']['lambda_max_branch'], ra.get('lambda_max_branch'), rb.get('lambda_max_branch'))
        for sk in ('share_EM', 'share_S2E2'):
            sa, sb = ra.get(sk) or {}, rb.get(sk) or {}
            rec('C2', f'[{key}].{sk} keys', set(sa) == set(sb) and bool(sa), sorted(sa), sorted(sb))
            for br in sorted(set(sa) & set(sb)):
                rec('C2', f'[{key}].{sk}.{br}', close_abs(sa[br], sb[br], T['phase1_share_abs']), sa[br], sb[br])

    # ---- C3 phase2 + born_t0
    p2a, p2b = chat.get('phase2', {}), cc.get('phase2', {})
    rec('C3', 'phase2 key set', set(p2a) == set(p2b) == set(S['config_keys']))
    n_t = len(S['t_grid'])
    for key in S['config_keys']:
        ra, rb = p2a.get(key, {}), p2b.get(key, {})
        for k in ('vT_VRH', 'vT_HS_lo', 'vT_HS_hi'):
            rec('C3', f'[{key}].{k}', close_rel(ra.get(k), rb.get(k), T['pins_rel']), ra.get(k), rb.get(k))
        for k in ('r_agg_E2_VRH', 'r_agg_h_VRH', 'r_agg_E2_HS'):
            xa, xb = ra.get(k), rb.get(k)
            ok = isinstance(xa, list) and isinstance(xb, list) and len(xa) == len(xb) == n_t and all(close_abs(u, v, T['r_agg_abs']) for u, v in zip(xa, xb))
            rec('C3', f'[{key}].{k}[{n_t}]', ok)
        for k in ('S_t_E2', 'S_t_h'):
            rec('C3', f'[{key}].{k}', close_abs(ra.get(k), rb.get(k), T['S_t_abs']), ra.get(k), rb.get(k))
        for k in ('kappa2_E2', 'kappa2_h'):
            rec('C3', f'[{key}].{k}', close_rel(ra.get(k), rb.get(k), T['kappa2_rel'], T['kappa2_abs_floor']), ra.get(k), rb.get(k))
        for leg, r in (('chat', ra), ('cc', rb)):
            hd = r.get('halving_dev_kappa2')
            rec('C3', f'[{key}].halving_dev_kappa2 ({leg}) <= kappa2_rel', isinstance(hd, (int, float)) and hd <= T['kappa2_rel'], hd)
        xa, xb = ra.get('lambda_mean_t'), rb.get('lambda_mean_t')
        rec('C3', f'[{key}].lambda_mean_t[{n_t}]', isinstance(xa, list) and isinstance(xb, list) and len(xa) == len(xb) == n_t
            and all(close_abs(u, v, T['phase1_lambda_abs']) for u, v in zip(xa, xb)))
    ba, bb = chat.get('born_t0', {}), cc.get('born_t0', {})
    rec('C3', 'born_t0 key set', set(ba) == set(bb) == set(S['base_configs']))
    for key in S['base_configs']:
        for k in S['born_t0_keys']:
            a, b = (ba.get(key) or {}).get(k), (bb.get(key) or {}).get(k)
            rec('C3', f'born_t0[{key}].{k}', close_rel(a, b, T['born_rel'], T['tau_agg']), a, b)

    # ---- C4 states, verdict, quadrature, t-grid
    for f in ('F-MS-3', 'F-MS-2', 'F-MS-1'):
        a, _ = getpath(chat, f'falsifiers.{f}.state'); b, _ = getpath(cc, f'falsifiers.{f}.state')
        rec('C4', f'{f}.state', a == b and a in S['value_domains'][f'{f}.state'], a, b)
    a, b = chat.get('verdict_class'), cc.get('verdict_class')
    rec('C4', 'verdict_class', a == b and a in S['value_domains']['verdict_class'], a, b)
    for k in ('n_theta', 'n_phi'):
        a, _ = getpath(chat, f'quadrature.{k}'); b, _ = getpath(cc, f'quadrature.{k}')
        rec('C4', f'quadrature.{k}', a == b == S['quadrature'][k], a, b)
    for leg, ck in (('chat', chat), ('cc', cc)):
        dr, _ = getpath(ck, 'quadrature.doubling_residual')
        rec('C4', f'{leg}: doubling_residual <= tol', isinstance(dr, (int, float)) and dr <= S['quadrature']['doubling_tol'], dr)
        rec('C4', f'{leg}: t_grid == schema', ck.get('t_grid') == S['t_grid'])

    # ---- C5 compare step
    if chat_cmp is not None and cc_cmp is not None:
        ra, rb = chat_cmp.get('rows', []), cc_cmp.get('rows', [])
        rec('C5', 'rows count', len(ra) == len(rb), len(ra), len(rb))
        for i, (x, y) in enumerate(zip(ra, rb)):
            for k in S['compare_row_keys']:
                rec('C5', f'rows[{i}].{k}', x.get(k) == y.get(k), x.get(k), y.get(k))
        rec('C5', 'compare verdict_class', chat_cmp.get('verdict_class') == cc_cmp.get('verdict_class') == chat.get('verdict_class'))
    else:
        rec('C5', 'compare files supplied', False, chat_cmp is not None, cc_cmp is not None)

    misses = [r for r in R if r['result'] == 'MISS']
    return {'checks': R, 'n_checks': len(R), 'n_miss': len(misses), 'misses': misses,
            'S9_triggered': bool(misses), 'overall': 'C-M-0..C5 ALL PASS' if not misses else 'MISS -> S9'}


def cmd_compare(a):
    S = json.load(open(a.schema, encoding='utf-8'))
    cb, ccb = open(a.chat, 'rb').read(), open(a.cc, 'rb').read()
    chat, cc = json.loads(cb), json.loads(ccb)
    chat_cmp = json.load(open(a.chat_cmp, encoding='utf-8')) if a.chat_cmp else None
    cc_cmp = json.load(open(a.cc_cmp, encoding='utf-8')) if a.cc_cmp else None
    out = run_checks(chat, cc, S, chat_cmp, cc_cmp, cb, ccb)
    out.update({'comparator': os.path.basename(__file__), 'comparator_md5': md5f(os.path.abspath(__file__)),
                'schema_md5': md5f(a.schema), 'chat_checkpoint_md5': hashlib.md5(cb).hexdigest(),
                'cc_checkpoint_md5': hashlib.md5(ccb).hexdigest()})
    json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for m in out['misses']:
        print(f'MISS {m["check"]:6} {m["item"]}  chat={m["chat"]!r} cc={m["cc"]!r}')
    print(f'{out["overall"]}  ({out["n_checks"]} checks, {out["n_miss"]} miss)  -> {a.out} {md5f(a.out)}')


# ---------------------------------------------------------------------- selftest
def synthetic(S, leg, seed):
    import random
    rnd = random.Random(seed)
    def f(x, jitter=0.0): return x + (rnd.random() - 0.5) * jitter
    ck = {'gate': 'G-MSCS1', 'leg': leg, 'instrument': f'g_mscs1_{leg}.py', 'instrument_md5': ('a' if leg == 'chat' else 'b') * 32,
          'memo_md5': S['memo_lock_md5'], 'memo_bytes': S['memo_lock_bytes'], 'ledger_base_md5': S['ledger_base_md5'], 'utc': 't',
          'elections': {'E-MS-1': '(a) descriptors', 'E-MS-2': '(a) all four', 'E-MS-2b': '(a+b) both arms',
                        'E-MS-2c': '(001+111) both axes', 'E-MS-3': '(a) t=0 Born', 'E-MS-4': '(a)', 'E-MS-5': '(a) fiber', 'E-MS-6': '(a) none'},
          'T1': {'list_md5': S['t1_list_md5'], 'state': 'CLEAN', 'numeric_collisions': 0},
          'inputs': {'X1_md5': S['x1_md5'], 'X1_bytes': S['x1_bytes']},
          'quadrature': {'n_theta': 64, 'n_phi': 128, 'doubling_residual': 3e-11}, 't_grid': list(S['t_grid']),
          'controls': {'F-CTRL-ISO': {'passed': True, 'r_xtal_E2': f(0, 1e-15), 'r_xtal_h': 0.0, 'lambda_max': 0.0, 'r_agg_max': 0.0},
                       'F-CTRL-SO3': {'passed': True, 'w_S2_mean_t0': f(0.4, 1e-12), 'dev_from_0p4': 1e-12, 'r_agg_0_E2': 0.0},
                       'F-CTRL-TEX': {'passed': True, 'r_agg_t1': f(0.03, 1e-9)},
                       'F-CTRL-POL': {'passed': True, 'split_plus_minus': 0.0, 'split_plus_avg': 0.0},
                       'PIN-A2AGG': {'passed': True, 'worst_rel_residual': 2e-10},
                       'F-CTRL-ADMIX': {'passed': True, 'r_xtal_h_projected': f(0, 1e-12)}},
          'phase1': {}, 'phase2': {}, 'born_t0': {},
          'falsifiers': {'F-MS-3': {'state': 'SILENT', 'worst_S_t': 1e-9}, 'F-MS-2': {'state': 'REGISTERED_NOT_EXECUTED'},
                         'F-MS-1': {'state': 'RETIRED_TO_CONTROL'}},
          'verdict_class': 'IDENTITY-DELIVERED'}
    for i, key in enumerate(S['config_keys']):
        ck['phase1'][key] = {'v_EM': f(8.0 + i, 1e-10), 'v_S2E2': f(7.8 + i, 1e-10), 'v_S2h': f(7.99 + i, 1e-10),
                             'r_xtal_E2': f(-0.025, 1e-10), 'r_xtal_h': f(-0.0012, 1e-10), 'lambda_mean': f(0.011, 1e-10),
                             'lambda_max': f(0.04, 1e-10), 'lambda_max_branch': 'qSV', 'cov_lambda_v': f(0.003, 1e-10),
                             'share_EM': {'qT1': 0.5, 'qT2': 0.49, 'qL': 0.01}, 'share_S2E2': {'qT1': 0.6, 'qT2': 0.4, 'qL': 0.0}}
        n = len(S['t_grid'])
        ck['phase2'][key] = {'vT_VRH': f(8.4, 1e-10), 'vT_HS_lo': f(8.3, 1e-10), 'vT_HS_hi': f(8.5, 1e-10),
                             'r_agg_E2_VRH': [f(-0.02 * t * t, 1e-8) for t in S['t_grid']],
                             'r_agg_h_VRH': [f(-0.001 * t * t, 1e-8) for t in S['t_grid']],
                             'r_agg_E2_HS': [f(-0.021 * t * t, 1e-8) for t in S['t_grid']],
                             'S_t_E2': f(0, 1e-9), 'S_t_h': f(0, 1e-9), 'kappa2_E2': f(-0.02, 1e-7), 'kappa2_h': f(-0.001, 1e-7),
                             'kappa3_E2': f(0.001, 1e-6), 'fit_residual': 1e-9, 'halving_dev_kappa2': 2e-5,
                             'lambda_mean_t': [f(0.01 * t * t, 1e-10) for t in S['t_grid']]}
    for key in S['base_configs']:
        ck['born_t0'][key] = {'D0_plus': f(-0.02, 1e-9), 'D0_minus': f(-0.02, 1e-9), 'D0_avg': f(-0.02, 1e-9), 'D2_avg': f(-0.018, 1e-9), 'a2agg_residual_rel': 2e-10}
    cmp_ = {'rows': [{'id': f'H-MS-{i}', 'predicted': 'x', 'machine': 'y', 'concordant': True} for i in range(1, 6)], 'verdict_class': 'IDENTITY-DELIVERED'}
    return ck, cmp_


def cmd_selftest(a):
    S = json.load(open(a.schema, encoding='utf-8'))
    chat, ccmp = synthetic(S, 'chat', 1); cc, cccmp = synthetic(S, 'cc', 2)
    base = run_checks(chat, cc, S, ccmp, cccmp, b'chat', b'cc')
    assert base['n_miss'] == 0, base['misses'][:5]
    print(f'  green  S1 two independent synthetic legs within tolerance -> ALL PASS ({base["n_checks"]} checks)')

    def expect(name, mutate, check):
        c2 = copy.deepcopy(cc); mutate(c2)
        out = run_checks(chat, c2, S, ccmp, copy.deepcopy(cccmp), b'chat', b'cc2')
        assert any(m['check'] == check for m in out['misses']), (name, out['misses'][:3])
        print(f'  green  {name} -> fires {check}')
    k0 = S['config_keys'][0]; b0 = S['base_configs'][0]
    expect('S2 verdict flip', lambda c: c.update(verdict_class='PROTECTION-BREACH'), 'C4')
    expect('S3 control flag False', lambda c: c['controls']['F-CTRL-SO3'].update(passed=False), 'C1')
    expect('S4 r_xtal beyond 1e-8', lambda c: c['phase1'][k0].update(r_xtal_E2=c['phase1'][k0]['r_xtal_E2'] + 1e-6), 'C2')
    expect('S5 branch label', lambda c: c['phase1'][k0].update(lambda_max_branch='qSH'), 'C2')
    expect('S6 S_t beyond 1e-6', lambda c: c['phase2'][k0].update(S_t_E2=5e-6), 'C3')
    expect('S7 kappa2 beyond 1e-4 rel', lambda c: c['phase2'][k0].update(kappa2_E2=c['phase2'][k0]['kappa2_E2'] * 1.01), 'C3')
    expect('S8 r_agg array element', lambda c: c['phase2'][k0]['r_agg_E2_VRH'].__setitem__(3, 0.5), 'C3')
    expect('S9 born_t0 beyond 1e-6 rel', lambda c: c['born_t0'][b0].update(D0_avg=c['born_t0'][b0]['D0_avg'] * 1.001), 'C3')
    expect('S10 T1 LIST_ABSENT rejected', lambda c: c['T1'].update(state='LIST_ABSENT'), 'C-M-0')
    expect('S11 election code', lambda c: c['elections'].update({'E-MS-1': '(b) envelope route'}), 'C-M-0')
    expect('S12 same instrument md5 (independence)', lambda c: c.update(instrument_md5='a' * 32), 'C-M-0')
    expect('S13 t_grid drift', lambda c: c['t_grid'].__setitem__(0, -0.6), 'C4')
    expect('S14 memo md5 not lock', lambda c: c.update(memo_md5='0' * 32), 'C-M-0')
    expect('S15 F-MS-3 state', lambda c: c['falsifiers']['F-MS-3'].update(state='FIRES'), 'C4')
    out = run_checks(chat, cc, S, ccmp, None, b'chat', b'cc'); assert any(m['check'] == 'C5' for m in out['misses'])
    print('  green  S16 missing compare file -> C5 MISS')
    # kappa2 tolerance is rel-with-floor: a 5e-5 relative change must PASS
    c3 = copy.deepcopy(cc); c3['phase2'][k0]['kappa2_E2'] *= (1 + 5e-5)
    out = run_checks(chat, c3, S, ccmp, copy.deepcopy(cccmp), b'chat', b'cc3'); assert out['n_miss'] == 0
    print('  green  S17 kappa2 within 1e-4 rel -> PASS')
    print(f'ALL 17/17 SUITES GREEN  (comparator {md5f(os.path.abspath(__file__))}, schema {md5f(a.schema)})')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('cmd', choices=['compare', 'selftest'])
    p.add_argument('--chat'); p.add_argument('--cc'); p.add_argument('--chat-cmp'); p.add_argument('--cc-cmp')
    p.add_argument('--schema', default=SCHEMA_DEFAULT)
    p.add_argument('--out', default='g_mscs1_twoleg_comparison.json')
    a = p.parse_args()
    {'compare': cmd_compare, 'selftest': cmd_selftest}[a.cmd](a)


if __name__ == '__main__':
    main()
