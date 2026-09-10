#!/usr/bin/env python3
"""g_quanta_compare_v1_0.py -- Gate G-QUANTA two-leg comparator, v1.0 (FROZEN September 10, 2026).

Usage
  compare  --chat CK --cc CK [--chat-cmp CMP --cc-cmp CMP] [--schema g_quanta_schema_v1_0.json] [--out OUT]
  selftest

Checks (every verdict-bearing quantity is a boolean or a short label -> EXACT identity;
free text is NEVER compared -- lesson H-S5 / H-W-6):
  C-Q-0  provenance: required keys per schema; memo_md5 == lock on both legs; instrument_md5 is a
         real 32-hex md5 on both legs; NO placeholder tokens; INDEPENDENCE WITNESS: the two
         instrument_md5 values differ and the two checkpoints are not byte-identical
  C1     lock identity: memo_md5 / memo_bytes / ledger_base_md5 identical on both legs
  C2     inventory identity: same objects in the same order; ledger_ref, perspective, config_space,
         invariant, functional_class identical per object
  C3     criteria identity: per-object C1 and C2 booleans identical
  C4     verdict identity: per-object PASS/FAIL identical
  C5     falsifier + promotion-condition identity: F-QUANTA-1/2/3 states; PC-1 met/n_pass/n_fail;
         PC-2 met + witness SET
  C6     compare-step identity (when both compare files supplied): per-row predicted/machine/
         concordant identical; PC-3_met identical. Elections compared by choice letter only.
Any MISS -> S9 counter-cross-check. Representational vs definitional classification is a
human step after the machine report; this file only reports.
"""
import argparse, hashlib, json, os, re, sys, copy, tempfile

MEMO_LOCK_MD5 = '0039d001769569297c2aa8ccbded5a3b'
MEMO_LOCK_BYTES = 4863
LEDGER_BASE_MD5 = 'b4e55aaea76a2152f7b1873309aec077'
PLACEHOLDER_TOKENS = ('TBD', 'PLACEHOLDER', 'xxxx', 'XXXX', '<', '>')
HEX32 = re.compile(r'^[0-9a-f]{32}$')
SCHEMA_DEFAULT = 'g_quanta_schema_v1_0.json'


def md5f(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def getpath(d, dotted):
    cur = d
    for k in dotted.split('.'):
        if not isinstance(cur, dict) or k not in cur:
            return None, False
        cur = cur[k]
    return cur, True


def choice_letter(s):
    m = re.match(r'\s*\(([a-z])\)', str(s))
    return m.group(1) if m else None


def run_checks(chat, cc, schema, chat_cmp=None, cc_cmp=None, chat_bytes=None, cc_bytes=None):
    R = []

    def rec(check, item, ok, chat_v=None, cc_v=None):
        R.append({'check': check, 'item': item, 'result': 'PASS' if ok else 'MISS',
                  'chat': chat_v, 'cc': cc_v})

    # ---- C-Q-0 provenance
    for leg, ck in (('chat', chat), ('cc', cc)):
        for key in schema['required_keys']:
            _, present = getpath(ck, key)
            rec('C-Q-0', f'{leg}: required key {key}', present)
        for i, r in enumerate(ck.get('results', [])):
            for key in schema['result_keys']:
                rec('C-Q-0', f'{leg}: results[{i}].{key}', key in r)
        rec('C-Q-0', f'{leg}: memo_md5 == lock', ck.get('memo_md5') == MEMO_LOCK_MD5, ck.get('memo_md5'), MEMO_LOCK_MD5)
        rec('C-Q-0', f'{leg}: memo_bytes == lock', ck.get('memo_bytes') == MEMO_LOCK_BYTES, ck.get('memo_bytes'), MEMO_LOCK_BYTES)
        rec('C-Q-0', f'{leg}: instrument_md5 real 32-hex', bool(HEX32.match(str(ck.get('instrument_md5', '')))), ck.get('instrument_md5'))
        flat = json.dumps(ck, ensure_ascii=False)
        rec('C-Q-0', f'{leg}: no placeholder tokens', not any(t in flat for t in PLACEHOLDER_TOKENS if t not in '<>')
            and not re.search(r'<[a-z_ ]+>', flat))
    rec('C-Q-0', 'INDEPENDENCE: instrument_md5 differ', chat.get('instrument_md5') != cc.get('instrument_md5'),
        chat.get('instrument_md5'), cc.get('instrument_md5'))
    if chat_bytes is not None and cc_bytes is not None:
        rec('C-Q-0', 'INDEPENDENCE: checkpoints not byte-identical', chat_bytes != cc_bytes)

    # ---- C1 lock identity
    for key in ('memo_md5', 'memo_bytes', 'ledger_base_md5'):
        rec('C1', key, chat.get(key) == cc.get(key), chat.get(key), cc.get(key))
    rec('C1', 'ledger_base_md5 == V4.81', chat.get('ledger_base_md5') == LEDGER_BASE_MD5 == cc.get('ledger_base_md5'))

    # ---- C2 inventory identity
    a, b = chat.get('results', []), cc.get('results', [])
    rec('C2', 'row count', len(a) == len(b), len(a), len(b))
    for i, (ra, rb) in enumerate(zip(a, b)):
        for key in ('object', 'ledger_ref', 'perspective', 'config_space', 'invariant', 'functional_class'):
            rec('C2', f'[{i}].{key}', ra.get(key) == rb.get(key), ra.get(key), rb.get(key))
        # ---- C3 criteria, C4 verdict
        for key in ('C1', 'C2'):
            rec('C3', f'[{i}].{key} ({ra.get("object")})', ra.get(key) is rb.get(key) and isinstance(ra.get(key), bool),
                ra.get(key), rb.get(key))
        rec('C4', f'[{i}].verdict ({ra.get("object")})', ra.get('verdict') == rb.get('verdict') and ra.get('verdict') in ('PASS', 'FAIL'),
            ra.get('verdict'), rb.get('verdict'))

    # ---- C5 falsifiers + PCs
    for f in ('F-QUANTA-1', 'F-QUANTA-2', 'F-QUANTA-3'):
        va, _ = getpath(chat, f'falsifiers.{f}.state'); vb, _ = getpath(cc, f'falsifiers.{f}.state')
        rec('C5', f'{f}.state', va == vb and va is not None, va, vb)
    for key in ('PC-1_nontrivial_partition.met', 'PC-1_nontrivial_partition.n_pass',
                'PC-1_nontrivial_partition.n_fail', 'PC-2_independence_witness.met'):
        va, _ = getpath(chat, f'promotion_conditions.{key}'); vb, _ = getpath(cc, f'promotion_conditions.{key}')
        rec('C5', key, va == vb and va is not None, va, vb)
    wa, _ = getpath(chat, 'promotion_conditions.PC-2_independence_witness.witnesses')
    wb, _ = getpath(cc, 'promotion_conditions.PC-2_independence_witness.witnesses')
    rec('C5', 'PC-2 witness set', set(wa or []) == set(wb or []) and wa is not None, wa, wb)
    for e in ('E-Q-1', 'E-Q-2'):
        la, lb = choice_letter((chat.get('elections') or {}).get(e)), choice_letter((cc.get('elections') or {}).get(e))
        rec('C5', f'election {e} choice letter', la == lb and la is not None, la, lb)

    # ---- C6 compare step
    if chat_cmp is not None and cc_cmp is not None:
        ra, rb = chat_cmp.get('rows', []), cc_cmp.get('rows', [])
        rec('C6', 'row count', len(ra) == len(rb), len(ra), len(rb))
        for i, (x, y) in enumerate(zip(ra, rb)):
            for key in ('object', 'predicted', 'machine', 'concordant'):
                rec('C6', f'[{i}].{key}', x.get(key) == y.get(key), x.get(key), y.get(key))
        rec('C6', 'PC-3_met', chat_cmp.get('PC-3_met') is cc_cmp.get('PC-3_met') and isinstance(chat_cmp.get('PC-3_met'), bool),
            chat_cmp.get('PC-3_met'), cc_cmp.get('PC-3_met'))
    else:
        rec('C6', 'compare files supplied', False, chat_cmp is not None, cc_cmp is not None)

    misses = [r for r in R if r['result'] == 'MISS']
    return {'checks': R, 'n_checks': len(R), 'n_miss': len(misses), 'misses': misses,
            'S9_triggered': bool(misses), 'overall': 'C1-C6 ALL PASS' if not misses else 'MISS -> S9'}


def cmd_compare(a):
    schema = json.load(open(a.schema, encoding='utf-8'))
    cb, ccb = open(a.chat, 'rb').read(), open(a.cc, 'rb').read()
    chat, cc = json.loads(cb), json.loads(ccb)
    chat_cmp = json.load(open(a.chat_cmp, encoding='utf-8')) if a.chat_cmp else None
    cc_cmp = json.load(open(a.cc_cmp, encoding='utf-8')) if a.cc_cmp else None
    out = run_checks(chat, cc, schema, chat_cmp, cc_cmp, cb, ccb)
    out.update({'comparator': os.path.basename(__file__), 'comparator_md5': md5f(os.path.abspath(__file__)),
                'schema_md5': md5f(a.schema), 'chat_checkpoint_md5': hashlib.md5(cb).hexdigest(),
                'cc_checkpoint_md5': hashlib.md5(ccb).hexdigest()})
    json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for m in out['misses']:
        print(f'MISS {m["check"]:6} {m["item"]}  chat={m["chat"]!r} cc={m["cc"]!r}')
    print(f'{out["overall"]}  ({out["n_checks"]} checks, {out["n_miss"]} miss)  -> {a.out} {md5f(a.out)}')


# ---------------------------------------------------------------------- selftest
def _synthetic():
    rows = [('A', 'Continuous', 'Linking Number', 'Rigid Constraint', True, True, 'PASS'),
            ('K', 'Continuous', 'Fano Winding', 'Competing Exponents', True, True, 'PASS'),
            ('CD Tower', 'Discrete', None, 'None', False, False, 'FAIL')]
    ck = {'gate': 'G-QUANTA', 'leg': 'chat', 'instrument': 'x.py', 'instrument_md5': 'a' * 32,
          'memo': 'm', 'memo_md5': MEMO_LOCK_MD5, 'memo_bytes': MEMO_LOCK_BYTES,
          'ledger_base_md5': LEDGER_BASE_MD5, 'elections': {'E-Q-1': '(b) x', 'E-Q-2': '(a) y'},
          'utc': 't', 'inventory_rows': 3,
          'results': [{'object': o, 'ledger_ref': '§', 'perspective': 'L-Perspective', 'config_space': cs,
                       'invariant': inv, 'functional_class': fc, 'C1': c1, 'C2': c2, 'verdict': v}
                      for o, cs, inv, fc, c1, c2, v in rows],
          'falsifiers': {'F-QUANTA-1': {'state': 'SILENT'}, 'F-QUANTA-2': {'state': 'SILENT'},
                         'F-QUANTA-3': {'state': 'REGISTERED_NOT_EXECUTED'}},
          'promotion_conditions': {'PC-1_nontrivial_partition': {'met': True, 'n_pass': 2, 'n_fail': 1},
                                   'PC-2_independence_witness': {'met': True, 'witnesses': ['K']}}}
    cmp_ = {'rows': [{'object': 'A', 'predicted': 'PASS', 'machine': 'PASS', 'concordant': True}], 'PC-3_met': True}
    return ck, cmp_


def cmd_selftest(a):
    schema = json.load(open(a.schema, encoding='utf-8'))
    ck, cmp_ = _synthetic()
    cc = copy.deepcopy(ck); cc['leg'] = 'cc'; cc['instrument_md5'] = 'b' * 32
    cc['elections'] = {'E-Q-1': '(b) standalone (CC wording)', 'E-Q-2': '(a) defects in scope (CC wording)'}
    base = run_checks(ck, cc, schema, cmp_, copy.deepcopy(cmp_), b'chat', b'cc')
    assert base['n_miss'] == 0, base['misses']
    print('  green  S1 identical legs (different wording, different md5) -> ALL PASS')

    def expect_miss(name, mutate, check):
        c2 = copy.deepcopy(cc); mutate(c2)
        out = run_checks(ck, c2, schema, cmp_, copy.deepcopy(cmp_), b'chat', b'cc2')
        assert any(m['check'] == check for m in out['misses']), (name, out['misses'])
        print(f'  green  {name} -> fires {check}')

    expect_miss('S2 verdict flip', lambda c: c['results'][0].update(verdict='FAIL'), 'C4')
    expect_miss('S3 criterion flip', lambda c: c['results'][1].update(C2=False), 'C3')
    expect_miss('S4 functional class swap', lambda c: c['results'][1].update(functional_class='Rigid Constraint'), 'C2')
    expect_miss('S5 falsifier state', lambda c: c['falsifiers']['F-QUANTA-2'].update(state='FIRES'), 'C5')
    expect_miss('S6 witness set', lambda c: c['promotion_conditions']['PC-2_independence_witness'].update(witnesses=['A']), 'C5')
    expect_miss('S7 placeholder md5', lambda c: c.update(instrument_md5='<fill>'), 'C-Q-0')
    expect_miss('S8 election letter', lambda c: c['elections'].update({'E-Q-1': '(a) joint'}), 'C5')
    expect_miss('S9 independence (same instrument md5)', lambda c: c.update(instrument_md5='a' * 32), 'C-Q-0')
    out = run_checks(ck, cc, schema, cmp_, None, b'chat', b'cc')
    assert any(m['check'] == 'C6' for m in out['misses'])
    print('  green  S10 missing compare file -> C6 MISS')
    print(f'ALL 10/10 SUITES GREEN  (comparator {md5f(os.path.abspath(__file__))})')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('cmd', choices=['compare', 'selftest'])
    p.add_argument('--chat'); p.add_argument('--cc')
    p.add_argument('--chat-cmp'); p.add_argument('--cc-cmp')
    p.add_argument('--schema', default=SCHEMA_DEFAULT)
    p.add_argument('--out', default='g_quanta_twoleg_comparison.json')
    a = p.parse_args()
    {'compare': cmd_compare, 'selftest': cmd_selftest}[a.cmd](a)


if __name__ == '__main__':
    main()
