#!/usr/bin/env python3
"""g_mscs_a_compare_v1_0.py -- two-leg comparator for Gate G-MSCS-A, FROZEN v1.0 (September 29, 2026).

Compares the chat-leg and CC-leg checkpoints against g_mscs_a_schema_v1_0.json (md5 asserted at load).
Checks (memo section 6.5):
  C-SA-0 provenance (memo, pinned inputs, T1 list, schema, elections, ledger base equal the schema on both legs);
         phase 0 passed on both legs with every float rule re-evaluated from the reported float; phase 2 all passed.
  C-SA-1 every numeric field of phase3 across legs at |a-b| <= rel*max(|a|,|b|) + floor (null only equals null).
  C-SA-2 every class, sub-reason, flag and OOM class identical (strings / bools / ints exact); the tree shapes identical.
  C-SA-3 sealed_md5, sealed_bytes, census, row_md5s identical.
  C-SA-4 pinned_inputs_md5 on both legs equals the schema's.
  C-SA-5 every null within its tolerance on each leg, its odf_reading token present, values across legs at pin_derived_rel.
  C-SA-6 T1 hits == 0 on both legs (F-CTRL-SA-T1 and the post-write scan).
  C-SA-7 grid counts recomputed here from the generators equal the checkpoint counts on both legs.
  C-SA-8 instrument_md5 differs between legs.
Never compared: free text (utc, detail strings). Never present: any anchor value (the checkpoint layout has no field for one;
the comparator additionally refuses a checkpoint carrying a key named lo, hi, k_em_max, k_t_max, src, note or cl).

Usage:  compare : python3 g_mscs_a_compare_v1_0.py compare CHAT.json CC.json [--schema S.json] [--out OUT.json]
        selftest: python3 g_mscs_a_compare_v1_0.py selftest [--schema S.json]
Exit: 0 all PASS, 1 any MISS, 2 usage/fatal."""
import copy, hashlib, json, math, sys

SCHEMA_DEFAULT = 'g_mscs_a_schema_v1_0.json'
SCHEMA_MD5 = '5323e11fc27d688f61aaf57302c875c0'
FORBIDDEN_KEYS = {'lo', 'hi', 'k_em_max', 'k_t_max', 'src', 'note', 'cl'}
FREE_TEXT = {'utc', 'detail', 'note_free_text'}


def load_schema(path):
    raw = open(path, 'rb').read()
    h = hashlib.md5(raw).hexdigest()
    if h != SCHEMA_MD5:
        raise SystemExit('FATAL: schema md5 %s != frozen %s' % (h, SCHEMA_MD5))
    return json.loads(raw.decode('ascii')), h


def isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


class Rec:
    def __init__(self):
        self.rows = []

    def add(self, check, name, ok, note=''):
        self.rows.append({'check': check, 'name': name, 'pass': bool(ok), 'note': note})

    def summary(self):
        n = len(self.rows)
        p = sum(r['pass'] for r in self.rows)
        return {'checks': n, 'pass': p, 'miss': n - p}


def rule_ok(v, rule):
    if rule['rule'] == 'eq':
        return isnum(v) and v == rule['threshold']
    if not isnum(v):
        return False
    return v <= rule['threshold'] if rule['rule'] == 'le' else v >= rule['threshold']


def walk_keys(node, path=''):
    if isinstance(node, dict):
        for k, v in node.items():
            yield path + '/' + k, k
            yield from walk_keys(v, path + '/' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_keys(v, '%s[%d]' % (path, i))


def compare_tree(a, b, rel, floor, rec, check, path):
    """generic two-leg comparison: numbers at tolerance, everything else exact, shapes identical"""
    if isinstance(a, dict) and isinstance(b, dict):
        if sorted(a) != sorted(b):
            rec.add(check, path, False, 'key sets differ')
            return
        for k in a:
            if k in FREE_TEXT:
                continue
            compare_tree(a[k], b[k], rel, floor, rec, check, path + '/' + k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            rec.add(check, path, False, 'lengths differ')
            return
        for i in range(len(a)):
            compare_tree(a[i], b[i], rel, floor, rec, check, '%s[%d]' % (path, i))
    elif isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str) or a is None or b is None:
        rec.add(check + '/exact', path, a == b and type(a) == type(b))
    elif isnum(a) and isnum(b):
        rec.add(check + '/num', path, abs(a - b) <= rel * max(abs(a), abs(b)) + floor)
    else:
        rec.add(check, path, False, 'type mismatch or non-finite')


def recount(g):
    D = g['D']
    tg = g['t_grid']
    return {'n_t_grid': len(tg), 'n_fit_window_inclusive': sum(abs(t) <= D for t in tg), 'n_fit_window_strict': sum(abs(t) < D for t in tg),
            'n_window_0p1_inclusive': sum(abs(t) <= 0.1 for t in tg), 'n_window_0p1_strict': sum(abs(t) < 0.1 for t in tg),
            'n_t2t4_axis': len(g['t2t4_axis']), 'n_t2t4_grid': len(g['t2t4_axis']) ** 2, 'n_area_grid': g['area_nodes_per_axis'] ** 2}


def compare(chat, cc, S, schema_md5):
    rec = Rec()
    T = S['tolerances']
    legs = {'chat': chat, 'cc': cc}
    # refusal: any forbidden key anywhere
    for leg, ck in legs.items():
        bad = sorted({k for _, k in walk_keys(ck) if k in FORBIDDEN_KEYS})
        rec.add('C-SA-refuse', leg + ' no anchor-value field', not bad, ', '.join(bad))
    # C-SA-0 provenance and phase 0 / phase 2
    for leg, ck in legs.items():
        for field, want in (('memo_lock_md5', S['memo_lock_md5']), ('pinned_inputs_md5', S['pinned_inputs_md5']), ('t1_list_md5', S['t1_list_md5']),
                            ('schema_md5', schema_md5), ('ledger_base_md5', S['ledger_base_md5']), ('gate', S['gate']), ('scanner_md5', S['scanner_md5'])):
            rec.add('C-SA-0', '%s %s' % (leg, field), ck.get(field) == want)
        rec.add('C-SA-0', leg + ' elections', ck.get('elections') == S['elections'])
        rec.add('C-SA-0', leg + ' leg label', ck.get('leg') == leg)
        P0 = ck.get('phase0') or {}
        for item in S['phase0']['items']:
            e = P0.get(item)
            rec.add('C-SA-0/phase0', '%s %s passed' % (leg, item), isinstance(e, dict) and e.get('passed') is True)
            rec.add('C-SA-0/phase0', '%s %s odf_reading' % (leg, item), isinstance(e, dict) and e.get('odf_reading') == S['phase0']['odf_reading'][item])
            for fname, rule in S['phase0']['float_rules'][item].items():
                rec.add('C-SA-0/phase0/float', '%s %s.%s' % (leg, item, fname), isinstance(e, dict) and rule_ok(e.get(fname), rule))
        P2 = ck.get('phase2') or {}
        for suite in S['phase2']['suites']:
            rec.add('C-SA-0/phase2', '%s %s' % (leg, suite), isinstance(P2.get(suite), dict) and P2[suite].get('passed') is True)
    # C-SA-4
    for leg, ck in legs.items():
        rec.add('C-SA-4', leg + ' pinned md5', ck.get('pinned_inputs_md5') == S['pinned_inputs_md5'])
    # C-SA-8
    rec.add('C-SA-8', 'instrument md5 differs', chat.get('instrument_md5') != cc.get('instrument_md5') and bool(chat.get('instrument_md5')))
    # C-SA-6
    for leg, ck in legs.items():
        rec.add('C-SA-6', leg + ' F-CTRL-SA-T1 hits', (ck.get('phase0') or {}).get('F-CTRL-SA-T1', {}).get('hits') == 0)
        rec.add('C-SA-6', leg + ' post-write hits', (ck.get('T1_post_write') or {}).get('hits') == 0)
    # C-SA-7
    for leg, ck in legs.items():
        g = ck.get('grids') or {}
        try:
            want = recount(g)
            for k, v in want.items():
                rec.add('C-SA-7', '%s %s' % (leg, k), g.get(k) == v)
        except Exception as e:
            rec.add('C-SA-7', leg + ' generators', False, str(e))
    # C-SA-5 nulls
    for leg, ck in legs.items():
        N = ck.get('nulls') or {}
        for nid, spec in S['nulls'].items():
            if nid == 'rule':
                continue
            block = N.get(nid) or {}
            rec.add('C-SA-5', '%s %s present' % (leg, nid), bool(block))
            for cell, rec_ in block.items():
                rec.add('C-SA-5/token', '%s %s %s' % (leg, nid, cell), rec_.get('odf_reading') in S['odf_reading_tokens'])
                for k in spec['keys']:
                    v = rec_.get(k)
                    if v is None:
                        rec.add('C-SA-5/null-value', '%s %s %s %s' % (leg, nid, cell, k), k == 'k12_chat_t2sq' or k == 'fit', 'absent')
                    else:
                        rec.add('C-SA-5/tol', '%s %s %s %s' % (leg, nid, cell, k), isnum(v) and abs(v) <= spec['tolerance'])
    compare_tree(chat.get('nulls'), cc.get('nulls'), T['pin_derived_rel'], T['pin_derived_abs'], rec, 'C-SA-5/twoleg', 'nulls')
    # C-SA-1/2/3: phase 3
    p3c, p3cc = chat.get('phase3'), cc.get('phase3')
    if p3c is None and p3cc is None:
        rec.add('C-SA-3', 'phase3 absent on both legs (pre-read run)', True)
    else:
        for k in S['phase3']['identity']:
            rec.add('C-SA-3', k, (p3c or {}).get(k) == (p3cc or {}).get(k) and (p3c or {}).get(k) is not None)
        compare_tree(p3c, p3cc, T['edge_twoleg_rel'], T['edge_twoleg_abs_floor'], rec, 'C-SA-1/2', 'phase3')
        for leg, p3 in (('chat', p3c), ('cc', p3cc)):
            rec.add('C-SA-2', leg + ' gate class in precedence list', isinstance(p3, dict) and (p3.get('gate') or {}).get('gate_class') in S['phase3']['class_precedence'])
    return rec


# ------------------------------------------------------------------------------------------------ self-test
def synthetic_checkpoint(S, leg, schema_md5):
    keys, arms = S['keys'], S['arms']
    ck = {'gate': S['gate'], 'leg': leg, 'utc': '2026-09-29T00:00:00Z', 'instrument_md5': ('a' if leg == 'chat' else 'b') * 32,
          'memo_lock_md5': S['memo_lock_md5'], 'memo_lock_bytes': S['memo_lock_bytes'], 'pinned_inputs_md5': S['pinned_inputs_md5'],
          't1_list_md5': S['t1_list_md5'], 't1_a1_md5': 'c' * 32, 'scanner_md5': S['scanner_md5'], 'schema_md5': schema_md5,
          'ledger_base_md5': S['ledger_base_md5'], 'elections': dict(S['elections']), 'lock_record_md5': 'd' * 32,
          'phase0': {}, 'nulls': {}, 'phase2': {s: {'passed': True, 'detail': 'synthetic'} for s in S['phase2']['suites']},
          'grids': {'t_grid': [-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0], 't2t4_axis': [-0.25, -0.125, 0.0, 0.125, 0.25],
                    'D': 0.25, 'area_nodes_per_axis': 201},
          'T1_post_write': {'hits': 0, 'collisions': 0}}
    ck['grids'].update(recount(ck['grids']))
    for item in S['phase0']['items']:
        e = {'passed': True, 'odf_reading': S['phase0']['odf_reading'][item]}
        for f, rule in S['phase0']['float_rules'][item].items():
            e[f] = rule['threshold'] if rule['rule'] == 'eq' else (0.5 * rule['threshold'] if rule['rule'] == 'le' else rule['threshold'])
        ck['phase0'][item] = e
    ck['nulls'] = {'N-1': {'%s/E2_Hill/t4' % k: {'odf_reading': 'hexP4' if 'hex' in k else 'cubK4', 'fit': 1e-11, 'bi': 2e-12} for k in keys},
                   'N-2': {k: {'odf_reading': 'hexP2P4' if 'hex' in k else 'cubP2K4-i', 'fit7': 1e-8, 'bi_chat': 1e-12, 'bi_cc': 1e-12, 'bi_5x5': 1e-12} for k in keys},
                   'N-3': {k: {'odf_reading': 'cubP2-i', 'fit': 1e-15, 'bi': 1e-13} for k in S['cubic_keys']},
                   'N-4': {k: {'odf_reading': 'cubP2K4-i', 'fit7': 1e-9, 'bi_5x5': 1e-14, 'k12_chat_t2sq': None} for k in S['cubic_keys']}}
    fam = {k: {a: {f: {'class': 'BINDING', 't_star': 0.1234, 't_star_bi': 0.1234, 'class_bi': 'BINDING', 'resolution_sensitive': False,
                       'sigma_star': 0.04, 'window_lo': -0.1234, 'window_hi': 0.1234, 'trunc_T': 1e-4, 'truncation_sensitive': False,
                       'nu': 1e-9, 'nu_is_inf': False, 'nullfloor_sensitive': False, 'binding_end': 'hi'} for f in ('t4', 't2')} for a in arms} for k in keys}
    ck['phase3'] = {'sealed_md5': 'e' * 32, 'sealed_bytes': 321, 'census': {'rows': 1, 'per_class': {'spd': 1}, 'fields_per_row': [11]},
                    'row_md5s': ['f' * 32], 't1_a1_md5': 'c' * 32, 'n_void_rows': 0, 'combined_empty': False, 'contains_zero': True,
                    'rows': [{'id': 'SA-1', 'row_md5': 'f' * 32, 'void_regime': False, 'contains_zero': True}],
                    'combined': {'families': fam, 'exclusion': None, 'two_param': {}},
                    'gate': {'gate_class': 'WINDOW-DELIVERED', 'sigma_union_hi': 0.05, 'sigma_strict_hi': 0.04, 'oom_class_x10': 'INERT-IN-D',
                             'oom_class_x0p1': 'WINDOW-DELIVERED', 'oom_robust': False, 'contains_zero': True, 'combined_empty': False, 'n_void_rows': 0}}
    return ck


def selftest(S, schema_md5):
    base_c, base_cc = synthetic_checkpoint(S, 'chat', schema_md5), synthetic_checkpoint(S, 'cc', schema_md5)
    ok0 = compare(base_c, base_cc, S, schema_md5).summary()['miss'] == 0
    suites = {}
    def mut(name, f, expect_miss=True):
        c, d = copy.deepcopy(base_c), copy.deepcopy(base_cc)
        f(c, d)
        miss = compare(c, d, S, schema_md5).summary()['miss']
        suites[name] = (miss > 0) == expect_miss
    mut('A1 edge differs beyond tolerance', lambda c, d: d['phase3']['combined']['families']['hex_step|a']['E2_Hill']['t4'].__setitem__('t_star', 0.1234 * (1 + 1e-9)))
    mut('A2 edge differs within tolerance', lambda c, d: d['phase3']['combined']['families']['hex_step|a']['E2_Hill']['t4'].__setitem__('t_star', 0.1234 * (1 + 1e-11)), expect_miss=False)
    mut('A3 class differs', lambda c, d: d['phase3']['combined']['families']['hex_step|a']['E2_Hill']['t4'].__setitem__('class', 'INERT-IN-D'))
    mut('A4 gate class differs', lambda c, d: d['phase3']['gate'].__setitem__('gate_class', 'INERT-IN-D'))
    mut('A5 sealed md5 differs', lambda c, d: d['phase3'].__setitem__('sealed_md5', '0' * 32))
    mut('A6 row md5 differs', lambda c, d: d['phase3'].__setitem__('row_md5s', ['0' * 32]))
    mut('A7 pinned md5 wrong on one leg', lambda c, d: c.__setitem__('pinned_inputs_md5', '0' * 32))
    mut('A8 same instrument md5', lambda c, d: d.__setitem__('instrument_md5', c['instrument_md5']))
    mut('A9 phase0 passed but float violates rule', lambda c, d: c['phase0']['F-CTRL-SA-ZERO'].__setitem__('worst_abs_r0', 1e-11))
    mut('A10 phase0 passed false', lambda c, d: d['phase0']['F-CTRL-SA-S'].__setitem__('passed', False))
    mut('A11 null exceeds tolerance', lambda c, d: c['nulls']['N-2']['hex_step|a'].__setitem__('bi_cc', 2e-6))
    mut('A12 null token missing', lambda c, d: c['nulls']['N-1']['hex_step|a/E2_Hill/t4'].pop('odf_reading'))
    mut('A13 count field typed wrong', lambda c, d: d['grids'].__setitem__('n_fit_window_inclusive', 7))
    mut('A14 T1 hit on one leg', lambda c, d: c['phase0']['F-CTRL-SA-T1'].__setitem__('hits', 1))
    mut('A15 anchor value field present', lambda c, d: d['phase3']['rows'][0].__setitem__('lo', -1.0))
    mut('A16 phase2 suite failed', lambda c, d: d['phase2']['C-SYN-9'].__setitem__('passed', False))
    mut('A17 flag differs', lambda c, d: d['phase3']['combined']['families']['cubic_gem8|111']['h_Hill']['t4'].__setitem__('nullfloor_sensitive', True))
    mut('A18 elections differ', lambda c, d: c['elections'].__setitem__('E-SA-9', 'b'))
    mut('A19 census differs', lambda c, d: d['phase3']['census'].__setitem__('rows', 2))
    mut('A20 gate class not in precedence list', lambda c, d: [x['phase3']['gate'].__setitem__('gate_class', 'KILLED') for x in (c, d)])
    mut('A21 utc differs (free text)', lambda c, d: d.__setitem__('utc', 'other'), expect_miss=False)
    mut('A22 null differs across legs', lambda c, d: d['nulls']['N-3']['cubic_step|001'].__setitem__('bi', 1.1e-13))
    return ok0, suites


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    args = sys.argv[1:]
    schema = args[args.index('--schema') + 1] if '--schema' in args else SCHEMA_DEFAULT
    S, smd5 = load_schema(schema)
    if args[0] == 'selftest':
        ok0, suites = selftest(S, smd5)
        print('baseline synthetic pair: %s' % ('PASS' if ok0 else 'FAIL'))
        for k, v in suites.items():
            print('  %-42s %s' % (k, 'ok' if v else 'FAILED'))
        good = ok0 and all(suites.values())
        print('SELFTEST: %s (%d/%d)' % ('PASS' if good else 'FAIL', sum(suites.values()), len(suites)))
        return 0 if good else 1
    if args[0] == 'compare' and len(args) >= 3:
        chat, cc = json.load(open(args[1])), json.load(open(args[2]))
        rec = compare(chat, cc, S, smd5)
        s = rec.summary()
        out = {'schema_md5': smd5, 'summary': s, 'misses': [r for r in rec.rows if not r['pass']]}
        if '--out' in args:
            json.dump({'rows': rec.rows, **out}, open(args[args.index('--out') + 1], 'w'), indent=1, sort_keys=True)
        print('checks %d  pass %d  miss %d' % (s['checks'], s['pass'], s['miss']))
        for r in out['misses'][:40]:
            print('  MISS %s %s %s' % (r['check'], r['name'], r['note']))
        print('RESULT: ' + ('PASS' if s['miss'] == 0 else 'MISS'))
        return 0 if s['miss'] == 0 else 1
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
