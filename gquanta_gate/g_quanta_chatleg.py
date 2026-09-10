#!/usr/bin/env python3
"""g_quanta_chatleg.py -- Gate G-QUANTA chat-leg instrument, v1 (September 10, 2026).

Evaluates the LOCKED section-4 inventory of staging_memo_G_QUANTA_v2.md against the
section-2 discriminator (C1, C2). This file contains NO per-object verdict: every
PASS/FAIL is computed at run time from the encoded columns of the memo table, which
is md5-guarded against the lock before it is read.

Subcommands
  selftest   internal suites on synthetic tables (no memo read, no checkpoint written)
  evaluate   md5-guard memo -> T1 self-grep -> parse section 4 -> evaluate -> checkpoint
  compare    run LAST (Eddington quarantine): checkpoint vs section-5 hypotheses,
             written to a SEPARATE artifact; the verdict checkpoint is never modified

Encoding rules (transcribed from memo section 2; the only logic in this file)
  C1  := ConfigSpace == Continuous AND InvariantType != None
         (a non-None invariant over a Discrete space evaluates to NO, per section 2)
  C2  := FunctionalClass in {Rigid Constraint, Competing Exponents}
  PASS := C1 AND C2
Falsifiers
  F-QUANTA-1  fires on any row of FunctionalClass == Single Exponent
              (single dilation scaling, no constraint); inert-by-inventory if no such row
  F-QUANTA-2  fires on any tower row with C1 AND C2
  F-QUANTA-3  REGISTERED, NOT EXECUTED (no derived E_binding in the framework)
Promotion conditions (lock-record annotations PC-1/PC-2; PC-3 is the compare step)
  PC-1  non-trivial partition: >= 1 PASS and >= 1 FAIL
  PC-2  independence witness: >= 1 PASS whose FunctionalClass is NOT the ropelength
        class (Rigid Constraint), i.e. the rule is not a restatement of L_B
"""
import argparse, datetime, hashlib, json, os, sys, tempfile

# ----------------------------------------------------------------- lock pins ---
MEMO_DEFAULT      = 'staging_memo_G_QUANTA_v2.md'
MEMO_LOCK_MD5     = '0039d001769569297c2aa8ccbded5a3b'
MEMO_LOCK_BYTES   = 4863
LEDGER_BASE       = 'SQT_Master_Ledger_v4_81_CANONICAL.md'
LEDGER_BASE_MD5   = 'b4e55aaea76a2152f7b1873309aec077'
ELECTIONS = {
    'E-Q-1': '(b) Promote standalone.',
    'E-Q-2': '(a) E-perspective (3D) for envelopes, L-perspective (2D/3D) for defects; '
             'extended (infinite-energy) defects explicitly in scope.',
}
CHECKPOINT_DEFAULT = 'g_quanta_chatleg_checkpoint.json'
COMPARE_DEFAULT    = 'g_quanta_chatleg_compare.json'
T1_DEFAULT         = 'T1_forbidden_strings.txt'

# ---------------------------------------------------------- vocabulary lock ---
COLUMNS            = ['Object', 'Ledger Ref', 'Perspective', 'Config Space',
                      'Invariant Type', 'Functional Class']
PERSPECTIVES       = {'L-Perspective', 'E-Perspective'}
CONFIG_SPACES      = {'Continuous', 'Discrete'}
FUNCTIONAL_CLASSES = {'Rigid Constraint', 'Competing Exponents', 'Single Exponent', 'None'}
C2_PASSING         = {'Rigid Constraint', 'Competing Exponents'}
ROPELENGTH_CLASS   = 'Rigid Constraint'      # class of the motivating case (L_B)
TOWER_TOKEN        = 'Tower'                 # identifies combinatorial-tower rows for F-QUANTA-2


def md5b(b): return hashlib.md5(b).hexdigest()
def md5f(p): return md5b(open(p, 'rb').read())
def bytes_label(p): return f'{os.path.getsize(p):,} B'


# ------------------------------------------------------------------ parsing ---
def section(text, heading_prefix):
    lines = text.split('\n')
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith(heading_prefix))
    except StopIteration:
        raise ValueError(f'section {heading_prefix!r} not found')
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
    return lines[start:end]


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def parse_inventory(text):
    rows = [l for l in section(text, '## 4.') if l.strip().startswith('|')]
    if len(rows) < 3:
        raise ValueError('section 4 table missing or empty')
    header = split_row(rows[0])
    if header != COLUMNS:
        raise ValueError(f'column header mismatch: {header}')
    out = []
    for r in rows[2:]:
        cells = split_row(r)
        if len(cells) != len(COLUMNS):
            raise ValueError(f'row arity {len(cells)} != {len(COLUMNS)}: {r}')
        out.append(dict(zip(COLUMNS, cells)))
    return out


def base_token(s):
    """'Competing Exponents (GP)' -> 'Competing Exponents'; 'None (Trivial Knot)' -> 'None'."""
    return s.split('(')[0].strip()


def parse_hypotheses(text):
    """section 5 bullets of the form '*   **Label:** PASS|FAIL ...' -> {label: verdict}."""
    hyp = {}
    for l in section(text, '## 5.'):
        l = l.strip()
        if not l.startswith('*'):
            continue
        if '**' not in l:
            continue
        label = l.split('**')[1].rstrip(':').strip()
        label = base_token(label)
        rest = l.split('**')[2].strip()
        verdict = rest.split('.')[0].split(' ')[0].split('(')[0].strip()
        if verdict not in ('PASS', 'FAIL'):
            raise ValueError(f'unparseable hypothesis line: {l}')
        hyp[label] = verdict
    return hyp


# --------------------------------------------------------------- evaluation ---
def evaluate_row(row):
    cs, persp = row['Config Space'], row['Perspective']
    if cs not in CONFIG_SPACES:
        raise ValueError(f'unknown Config Space {cs!r} in row {row["Object"]!r}')
    if persp not in PERSPECTIVES:
        raise ValueError(f'unknown Perspective {persp!r} in row {row["Object"]!r}')
    inv = base_token(row['Invariant Type'])
    inv = None if inv == 'None' else inv
    fc = base_token(row['Functional Class'])
    if fc not in FUNCTIONAL_CLASSES:
        raise ValueError(f'unknown Functional Class {fc!r} in row {row["Object"]!r}')

    if cs != 'Continuous':
        c1, c1_reason = False, 'configuration space is Discrete (section 2: discrete labels evaluate to NO)'
    elif inv is None:
        c1, c1_reason = False, 'no conserved invariant declared (trivial)'
    else:
        c1, c1_reason = True, f'continuous configuration space with invariant {inv}'

    c2 = fc in C2_PASSING
    c2_reason = (f'functional class {fc} is Derrick-evading' if c2
                 else f'functional class {fc} is not Derrick-evading')
    return {
        'object': row['Object'], 'ledger_ref': row['Ledger Ref'], 'perspective': persp,
        'config_space': cs, 'invariant': inv, 'functional_class': fc,
        'C1': c1, 'C1_reason': c1_reason, 'C2': c2, 'C2_reason': c2_reason,
        'verdict': 'PASS' if (c1 and c2) else 'FAIL',
    }


def falsifiers(results):
    f1 = [r['object'] for r in results if r['functional_class'] == 'Single Exponent']
    f2 = [r['object'] for r in results if TOWER_TOKEN in r['object'] and r['C1'] and r['C2']]
    tower_rows = [r['object'] for r in results if TOWER_TOKEN in r['object']]
    return {
        'F-QUANTA-1': {'state': 'FIRES' if f1 else 'SILENT', 'hits': f1,
                       'inert_by_inventory': not f1 and all(r['functional_class'] != 'Single Exponent' for r in results),
                       'note': 'fires only on a Single Exponent functional class; the locked inventory '
                               'declares none, so silence here is inert-by-inventory, not a test passed'},
        'F-QUANTA-2': {'state': 'FIRES' if f2 else 'SILENT', 'hits': f2, 'tower_rows_examined': tower_rows},
        'F-QUANTA-3': {'state': 'REGISTERED_NOT_EXECUTED',
                       'note': 'no derived E_binding exists in the framework; tests scale separation, '
                               'not the stability discriminator'},
    }


def promotion_conditions(results):
    passes = [r for r in results if r['verdict'] == 'PASS']
    fails = [r for r in results if r['verdict'] == 'FAIL']
    witnesses = [r['object'] for r in passes if r['functional_class'] != ROPELENGTH_CLASS]
    return {
        'PC-1_nontrivial_partition': {'met': bool(passes) and bool(fails),
                                      'n_pass': len(passes), 'n_fail': len(fails)},
        'PC-2_independence_witness': {'met': bool(witnesses), 'witnesses': witnesses,
                                      'excluded_class': ROPELENGTH_CLASS},
        'PC-3_concordance_with_section_5': 'DEFERRED to `compare` (comparison step last)',
    }


def evaluate_text(text):
    rows = parse_inventory(text)
    results = [evaluate_row(r) for r in rows]
    return {'inventory_rows': len(rows), 'results': results,
            'falsifiers': falsifiers(results), 'promotion_conditions': promotion_conditions(results)}


# -------------------------------------------------------------- T1 self-grep ---
def t1_scan(paths, t1_path):
    """Returns None if no list is available; else a list of (path, pattern_index) hits.
    Pattern text is never echoed (H-16 masking lesson)."""
    if not t1_path or not os.path.exists(t1_path):
        return None
    pats = [l.rstrip('\n') for l in open(t1_path, encoding='utf-8')
            if l.strip() and not l.startswith('#')]
    hits = []
    for p in paths:
        data = open(p, 'rb').read().decode('utf-8', 'replace')
        for i, pat in enumerate(pats):
            if pat in data:
                hits.append((p, i))
    return hits


def t1_gate(paths, t1_path, allow_absent):
    hits = t1_scan(paths, t1_path)
    if hits is None:
        if not allow_absent:
            sys.exit('HALT: T1 forbidden-string list not found; supply --t1 PATH or pass '
                     '--no-t1-halt to record the omission as a deviation (D-T1) and continue')
        return {'state': 'LIST_ABSENT', 'deviation': 'D-T1: self-grep skipped, list not supplied'}
    if hits:
        sys.exit('HALT: T1 self-grep HIT ' + ', '.join(f'{p}#{i}' for p, i in hits))
    return {'state': 'CLEAN', 'files': [os.path.basename(p) for p in paths]}


# ---------------------------------------------------------------- commands ---
def cmd_evaluate(a):
    raw = open(a.memo, 'rb').read()
    got = md5b(raw)
    if got != MEMO_LOCK_MD5 or len(raw) != MEMO_LOCK_BYTES:
        sys.exit(f'HALT: memo does not match the lock (md5 {got}, {len(raw)} B; '
                 f'lock {MEMO_LOCK_MD5}, {MEMO_LOCK_BYTES} B)')
    t1_pre = t1_gate([os.path.abspath(__file__), a.memo], a.t1, a.no_t1_halt)

    text = raw.decode('utf-8')
    ev = evaluate_text(text)
    ck = {
        'gate': 'G-QUANTA', 'leg': 'chat', 'instrument': os.path.basename(__file__),
        'instrument_md5': md5f(os.path.abspath(__file__)),
        'memo': os.path.basename(a.memo), 'memo_md5': got, 'memo_bytes': len(raw),
        'ledger_base': LEDGER_BASE, 'ledger_base_md5': LEDGER_BASE_MD5,
        'elections': ELECTIONS, 'utc': datetime.datetime.utcnow().isoformat() + 'Z',
        'T1_pre_evaluation': t1_pre, **ev,
    }
    with open(a.checkpoint, 'w', encoding='utf-8') as f:
        json.dump(ck, f, ensure_ascii=False, indent=2)
    t1_post = t1_gate([a.checkpoint], a.t1, True)
    # append the post-write scan result without altering the evaluation content
    ck['T1_post_write'] = t1_post
    with open(a.checkpoint, 'w', encoding='utf-8') as f:
        json.dump(ck, f, ensure_ascii=False, indent=2)

    print(f'memo {got} ({len(raw):,} B) == lock  |  instrument {ck["instrument_md5"]}')
    print(f'T1 pre: {t1_pre["state"]}  post: {t1_post["state"]}')
    for r in ev['results']:
        print(f'{r["verdict"]:4}  C1={int(r["C1"])} C2={int(r["C2"])}  {r["object"]}  [{r["ledger_ref"]}]')
    for k, v in ev['falsifiers'].items():
        print(f'{k}: {v["state"]}' + (f'  hits={v["hits"]}' if v.get('hits') else ''))
    pc = ev['promotion_conditions']
    print(f'PC-1 partition: {pc["PC-1_nontrivial_partition"]["met"]}  '
          f'({pc["PC-1_nontrivial_partition"]["n_pass"]} PASS / {pc["PC-1_nontrivial_partition"]["n_fail"]} FAIL)')
    print(f'PC-2 witness: {pc["PC-2_independence_witness"]["met"]}  {pc["PC-2_independence_witness"]["witnesses"]}')
    print(f'checkpoint {a.checkpoint} {md5f(a.checkpoint)} ({bytes_label(a.checkpoint)})')


def match_hypotheses(results, hyp):
    """Match each section-5 label to exactly one inventory object by substring."""
    rows = []
    for label, predicted in hyp.items():
        cands = [r for r in results if label in r['object']]
        if len(cands) != 1:
            raise ValueError(f'hypothesis {label!r} matches {len(cands)} objects')
        rows.append({'label': label, 'object': cands[0]['object'],
                     'predicted': predicted, 'machine': cands[0]['verdict'],
                     'concordant': predicted == cands[0]['verdict']})
    return rows


def cmd_compare(a):
    ck = json.load(open(a.checkpoint, encoding='utf-8'))
    raw = open(a.memo, 'rb').read()
    if md5b(raw) != ck['memo_md5'] or md5b(raw) != MEMO_LOCK_MD5:
        sys.exit('HALT: memo/checkpoint/lock md5 disagreement')
    hyp = parse_hypotheses(raw.decode('utf-8'))
    rows = match_hypotheses(ck['results'], hyp)
    unmatched = [r['object'] for r in ck['results'] if r['object'] not in {x['object'] for x in rows}]
    out = {'gate': 'G-QUANTA', 'step': 'compare (PC-3, comparison last)',
           'checkpoint': os.path.basename(a.checkpoint), 'checkpoint_md5': md5f(a.checkpoint),
           'memo_md5': ck['memo_md5'], 'rows': rows,
           'objects_without_hypothesis': unmatched,
           'PC-3_met': all(r['concordant'] for r in rows) and not unmatched,
           'utc': datetime.datetime.utcnow().isoformat() + 'Z'}
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for r in rows:
        print(f'{"OK " if r["concordant"] else "MISS"}  H:{r["predicted"]:4} M:{r["machine"]:4}  {r["object"]}')
    print(f'PC-3 concordance: {out["PC-3_met"]}   unmatched={unmatched}')
    print(f'compare {a.out} {md5f(a.out)} ({bytes_label(a.out)})')


# ----------------------------------------------------------------- selftest ---
SYN_HEAD = ('# synthetic\n\n## 4. Instrument Encoding\n\n'
            '| Object | Ledger Ref | Perspective | Config Space | Invariant Type | Functional Class |\n'
            '| :--- | :--- | :--- | :--- | :--- | :--- |\n')


def syn(rows, hyp=None):
    t = SYN_HEAD + ''.join('| ' + ' | '.join(r) + ' |\n' for r in rows)
    if hyp is not None:
        t += '\n## 5. Hypotheses\n' + ''.join(f'*   **{k}:** {v}.\n' for k, v in hyp.items())
    t += '\n## 6. End\n'
    return t


def cmd_selftest(a):
    ok = 0

    def suite(name, fn):
        nonlocal ok
        fn(); ok += 1; print(f'  green  {name}')

    def s1():  # parser round-trip + normalisation
        rows = parse_inventory(syn([['A', '§1', 'L-Perspective', 'Continuous', 'Linking Number', 'Rigid Constraint'],
                                    ['B', '§2', 'E-Perspective', 'Discrete', 'None (Trivial)', 'Competing Exponents (GP)']]))
        assert len(rows) == 2 and rows[0]['Object'] == 'A'
        assert base_token(rows[1]['Invariant Type']) == 'None'
        assert base_token(rows[1]['Functional Class']) == 'Competing Exponents'

    def s2():  # C1/C2 truth table
        cases = [('Continuous', 'Winding Number', 'Rigid Constraint', True, True, 'PASS'),
                 ('Continuous', 'Winding Number', 'Competing Exponents', True, True, 'PASS'),
                 ('Continuous', 'None', 'Rigid Constraint', False, True, 'FAIL'),
                 ('Continuous', 'Winding Number', 'None', True, False, 'FAIL'),
                 ('Discrete', 'Chirality/Algebraic', 'None', False, False, 'FAIL'),
                 ('Discrete', 'Chirality/Algebraic', 'Competing Exponents', False, True, 'FAIL'),
                 ('Continuous', 'Winding Number', 'Single Exponent', True, False, 'FAIL')]
        for cs, inv, fc, c1, c2, v in cases:
            r = evaluate_row({'Object': 'X', 'Ledger Ref': '§', 'Perspective': 'L-Perspective',
                              'Config Space': cs, 'Invariant Type': inv, 'Functional Class': fc})
            assert (r['C1'], r['C2'], r['verdict']) == (c1, c2, v), (cs, inv, fc, r)

    def s3():  # F-QUANTA-2 fires on a tower row that is continuous + competing
        ev = evaluate_text(syn([['CD Tower Rungs', '§', 'E-Perspective', 'Continuous', 'Linking Number', 'Competing Exponents']]))
        assert ev['falsifiers']['F-QUANTA-2']['state'] == 'FIRES'
        ev = evaluate_text(syn([['CD Tower Rungs', '§', 'E-Perspective', 'Discrete', 'Chirality', 'None']]))
        assert ev['falsifiers']['F-QUANTA-2']['state'] == 'SILENT'

    def s4():  # F-QUANTA-1 fires on Single Exponent; inert flag otherwise
        ev = evaluate_text(syn([['Z', '§', 'L-Perspective', 'Continuous', 'Winding Number', 'Single Exponent']]))
        assert ev['falsifiers']['F-QUANTA-1']['state'] == 'FIRES'
        ev = evaluate_text(syn([['Z', '§', 'L-Perspective', 'Continuous', 'Winding Number', 'Rigid Constraint']]))
        f1 = ev['falsifiers']['F-QUANTA-1']
        assert f1['state'] == 'SILENT' and f1['inert_by_inventory'] is True

    def s5():  # PC-1 / PC-2
        only_rope = syn([['A', '§', 'L-Perspective', 'Continuous', 'Linking Number', 'Rigid Constraint'],
                         ['B', '§', 'E-Perspective', 'Discrete', 'None', 'None']])
        pc = evaluate_text(only_rope)['promotion_conditions']
        assert pc['PC-1_nontrivial_partition']['met'] and not pc['PC-2_independence_witness']['met']
        with_gp = syn([['A', '§', 'L-Perspective', 'Continuous', 'Linking Number', 'Rigid Constraint'],
                       ['K', '§', 'L-Perspective', 'Continuous', 'Fano Winding', 'Competing Exponents (GP)']])
        pc = evaluate_text(with_gp)['promotion_conditions']
        assert not pc['PC-1_nontrivial_partition']['met'] and pc['PC-2_independence_witness']['witnesses'] == ['K']

    def s6():  # vocabulary lock rejects unknown classes / spaces
        for bad in [dict(cs='Continuous', inv='X', fc='Soft Constraint'),
                    dict(cs='Fuzzy', inv='X', fc='None')]:
            try:
                evaluate_row({'Object': 'X', 'Ledger Ref': '§', 'Perspective': 'L-Perspective',
                              'Config Space': bad['cs'], 'Invariant Type': bad['inv'], 'Functional Class': bad['fc']})
                raise AssertionError('accepted bad vocabulary')
            except ValueError:
                pass

    def s7():  # md5 guard: a tampered memo (one byte) is not the lock
        raw = open(a.memo, 'rb').read() if os.path.exists(a.memo) else b'x' * MEMO_LOCK_BYTES
        tampered = raw[:-1] + (b'\n' if raw[-1:] != b'\n' else b' ')
        assert md5b(tampered) != MEMO_LOCK_MD5 and md5b(tampered) != md5b(raw)

    def s8():  # hypothesis parsing + matching (substring, unique)
        t = syn([['Cluster M SLWE Matrices', '§', 'E-Perspective', 'Discrete', 'None', 'None'],
                 ['Clifford Unknot / Rule 17', '§', 'L-Perspective', 'Continuous', 'None (Trivial Knot)', 'Rigid Constraint']],
                hyp={'SLWE Matrices': 'FAIL', 'Clifford Unknot': 'FAIL'})
        ev = evaluate_text(t)
        rows = match_hypotheses(ev['results'], parse_hypotheses(t))
        assert len(rows) == 2 and all(r['concordant'] for r in rows)
        try:
            match_hypotheses(ev['results'], {'Nothing': 'PASS'}); raise AssertionError('matched nothing')
        except ValueError:
            pass

    def s9():  # T1 scan mechanics: absent list -> None; planted token -> hit by index only
        with tempfile.TemporaryDirectory() as d:
            lst = os.path.join(d, 't1.txt'); tgt = os.path.join(d, 'x.txt')
            open(lst, 'w').write('# comment\nZZQX_SELFTEST_TOKEN\n')
            open(tgt, 'w').write('clean text')
            assert t1_scan([tgt], lst) == []
            open(tgt, 'w').write('has ZZQX_SELFTEST_TOKEN inside')
            assert t1_scan([tgt], lst) == [(tgt, 0)]
            assert t1_scan([tgt], os.path.join(d, 'missing.txt')) is None

    for name, fn in [('S1 parser/normalisation', s1), ('S2 C1/C2 truth table', s2),
                     ('S3 F-QUANTA-2 firing', s3), ('S4 F-QUANTA-1 firing + inert flag', s4),
                     ('S5 PC-1/PC-2', s5), ('S6 vocabulary lock', s6), ('S7 md5 guard', s7),
                     ('S8 hypothesis match', s8), ('S9 T1 scan mechanics', s9)]:
        suite(name, fn)
    print(f'ALL {ok}/9 SUITES GREEN  (instrument {md5f(os.path.abspath(__file__))})')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--memo', default=MEMO_DEFAULT)
    p.add_argument('--t1', default=T1_DEFAULT, help='T1 forbidden-string list (one pattern per line)')
    p.add_argument('--no-t1-halt', action='store_true', help='record D-T1 instead of halting when the list is absent')
    p.add_argument('--checkpoint', default=CHECKPOINT_DEFAULT)
    p.add_argument('--out', default=COMPARE_DEFAULT, help='compare-step output (separate from the checkpoint)')
    p.add_argument('cmd', choices=['selftest', 'evaluate', 'compare'])
    a = p.parse_args()
    {'selftest': cmd_selftest, 'evaluate': cmd_evaluate, 'compare': cmd_compare}[a.cmd](a)


if __name__ == '__main__':
    main()
