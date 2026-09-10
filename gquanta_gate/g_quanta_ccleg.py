#!/usr/bin/env python3
"""g_quanta_ccleg.py -- Gate G-QUANTA, CC-leg instrument (independent implementation).

Written from the frozen staging memo (md5 0039d001769569297c2aa8ccbded5a3b) sections 2 and 4
and the lock record section 4 ONLY. The chat-leg instrument, checkpoint, and compare file were
QUARANTINED (base64-armored, undecoded) at the time this file was written.

Commands
  evaluate   md5-guard the memo, parse the section-4 table at run time, evaluate the
             discriminator by two structurally different routes (asserting per-row agreement),
             and write g_quanta_ccleg_checkpoint.json.
  compare    read the checkpoint back and compare machine verdicts against the memo's
             section-5 hypotheses (parsed at run time); write g_quanta_ccleg_compare.json.
             Never modifies the checkpoint. Run LAST (Eddington quarantine).
  selftest   tamper-guard, route-agreement, and truth-table spot checks on synthetic rows.

Design notes (CC-DD register in the dispatch return):
  - The section-4 table is the sole input; no row values are hand-copied into this source.
  - No object-to-outcome mapping appears anywhere in this source; the outcome vocabulary
    strings exist only as the boolean-to-label map required by the checkpoint schema.
  - Route A is predicate logic; route B is a 16-entry literal lookup table over the
    (config_space, invariant_present, functional_class) triple. Both must agree per row.
  - T1 forbidden-string list was not supplied to the CC leg: deviation D-T1 (CC),
    state LIST_ABSENT, recorded in the checkpoint.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone

MEMO_PATH = 'staging_memo_G_QUANTA_v2.md'
MEMO_LOCK_MD5 = '0039d001769569297c2aa8ccbded5a3b'
MEMO_LOCK_BYTES = 4863
CHECKPOINT_PATH = 'g_quanta_ccleg_checkpoint.json'
COMPARE_PATH = 'g_quanta_ccleg_compare.json'

PERSPECTIVES = ('L-Perspective', 'E-Perspective')
CONFIG_SPACES = ('Continuous', 'Discrete')
FUNCTIONAL_CLASSES = ('Rigid Constraint', 'Competing Exponents', 'Single Exponent', 'None')
DERRICK_EVADING = ('Rigid Constraint', 'Competing Exponents')

# ---------------------------------------------------------------- memo guard


def load_memo_guarded():
    raw = open(MEMO_PATH, 'rb').read()
    got = hashlib.md5(raw).hexdigest()
    if got != MEMO_LOCK_MD5 or len(raw) != MEMO_LOCK_BYTES:
        print(f'HALT: memo guard failed: md5 {got} (want {MEMO_LOCK_MD5}), '
              f'{len(raw)} B (want {MEMO_LOCK_BYTES})', file=sys.stderr)
        sys.exit(1)
    return raw.decode('utf-8')


def memo_section(text, number):
    for chunk in text.split('\n## '):
        if chunk.startswith(f'{number}.'):
            return chunk
    print(f'HALT: memo section {number} not found', file=sys.stderr)
    sys.exit(1)


def ledger_base_md5(text):
    m = re.search(r'\*\*Base:\*\*\s+`[^`]+`\s+\(md5\s+`([0-9a-f]{32})`\)', text)
    if not m:
        print('HALT: ledger base md5 not found in memo header', file=sys.stderr)
        sys.exit(1)
    return m.group(1)

# ------------------------------------------------------------- table parsing


def parse_inventory(text):
    """Parse the section-4 matrix at run time. Vocabulary-locked: unknown values halt."""
    sec = memo_section(text, 4)
    rows = []
    for line in sec.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) != 6 or cells[0] == 'Object' or set(cells[0]) <= set(':- '):
            continue
        obj, ref, persp, cspace, inv_raw, fc_raw = cells
        fc = re.sub(r'\s*\([^)]*\)\s*$', '', fc_raw)
        if persp not in PERSPECTIVES:
            print(f'HALT: unknown perspective {persp!r} in row {obj!r}', file=sys.stderr)
            sys.exit(1)
        if cspace not in CONFIG_SPACES:
            print(f'HALT: unknown config space {cspace!r} in row {obj!r}', file=sys.stderr)
            sys.exit(1)
        if fc not in FUNCTIONAL_CLASSES:
            print(f'HALT: unknown functional class {fc_raw!r} in row {obj!r}', file=sys.stderr)
            sys.exit(1)
        invariant_present = not inv_raw.startswith('None')
        rows.append({
            'object': obj,
            'ledger_ref': ref,
            'perspective': persp,
            'config_space': cspace,
            'invariant': inv_raw if invariant_present else None,
            'functional_class': fc,
            'invariant_present': invariant_present,
        })
    if not rows:
        print('HALT: no inventory rows parsed from section 4', file=sys.stderr)
        sys.exit(1)
    return rows

# ------------------------------------------------------- discriminator routes


def route_a(config_space, invariant_present, functional_class):
    """Route A: predicate logic straight off the section-2 definitions."""
    c1 = (config_space == 'Continuous') and invariant_present
    c2 = functional_class in DERRICK_EVADING
    return c1, c2


# Route B: exhaustive literal lookup over the (config_space, invariant_present,
# functional_class) triple. Written out by hand, entry by entry, as the structurally
# independent second route required by the dispatch.
ROUTE_B = {
    ('Continuous', True,  'Rigid Constraint'):    (True,  True),
    ('Continuous', True,  'Competing Exponents'): (True,  True),
    ('Continuous', True,  'Single Exponent'):     (True,  False),
    ('Continuous', True,  'None'):                (True,  False),
    ('Continuous', False, 'Rigid Constraint'):    (False, True),
    ('Continuous', False, 'Competing Exponents'): (False, True),
    ('Continuous', False, 'Single Exponent'):     (False, False),
    ('Continuous', False, 'None'):                (False, False),
    ('Discrete',   True,  'Rigid Constraint'):    (False, True),
    ('Discrete',   True,  'Competing Exponents'): (False, True),
    ('Discrete',   True,  'Single Exponent'):     (False, False),
    ('Discrete',   True,  'None'):                (False, False),
    ('Discrete',   False, 'Rigid Constraint'):    (False, True),
    ('Discrete',   False, 'Competing Exponents'): (False, True),
    ('Discrete',   False, 'Single Exponent'):     (False, False),
    ('Discrete',   False, 'None'):                (False, False),
}


def evaluate_row(row):
    key = (row['config_space'], row['invariant_present'], row['functional_class'])
    a = route_a(*key)
    b = ROUTE_B[key]
    assert a == b, f'route disagreement on {row["object"]!r}: A={a} B={b}'
    c1, c2 = a
    ok = c1 and c2
    return {
        'object': row['object'],
        'ledger_ref': row['ledger_ref'],
        'perspective': row['perspective'],
        'config_space': row['config_space'],
        'invariant': row['invariant'],
        'functional_class': row['functional_class'],
        'C1': c1,
        'C2': c2,
        'verdict': ('FAIL', 'PASS')[ok],
    }

# ------------------------------------------------------------------ evaluate


def cmd_evaluate():
    memo_text = load_memo_guarded()
    rows = parse_inventory(memo_text)
    results = [evaluate_row(r) for r in rows]

    f1_fires = any(r['functional_class'] == 'Single Exponent' for r in results)
    f2_fires = any('Tower' in r['object'] and r['C1'] and r['C2'] for r in results)
    n_pass = sum(1 for r in results if r['C1'] and r['C2'])
    n_fail = len(results) - n_pass
    witnesses = [r['object'] for r in results
                 if r['C1'] and r['C2'] and r['functional_class'] != 'Rigid Constraint']

    checkpoint = {
        'gate': 'G-QUANTA',
        'leg': 'cc',
        'instrument': 'g_quanta_ccleg.py',
        'instrument_md5': hashlib.md5(open(__file__, 'rb').read()).hexdigest(),
        'memo': MEMO_PATH,
        'memo_md5': MEMO_LOCK_MD5,
        'memo_bytes': MEMO_LOCK_BYTES,
        'ledger_base_md5': ledger_base_md5(memo_text),
        'elections': {
            'E-Q-1': '(b) promote standalone -- CC-leg wording',
            'E-Q-2': '(a) E-perspective for envelopes, L-perspective for defects; '
                     'extended defects in scope -- CC-leg wording',
        },
        'utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'inventory_rows': len(results),
        'results': results,
        'falsifiers': {
            'F-QUANTA-1': {'state': ('SILENT', 'FIRES')[f1_fires],
                           'note': 'inert-by-inventory: the locked table declares no '
                                   'Single Exponent row, so silence is not a test passed'},
            'F-QUANTA-2': {'state': ('SILENT', 'FIRES')[f2_fires]},
            'F-QUANTA-3': {'state': 'REGISTERED_NOT_EXECUTED'},
        },
        'promotion_conditions': {
            'PC-1_nontrivial_partition': {'met': n_pass >= 1 and n_fail >= 1,
                                          'n_pass': n_pass, 'n_fail': n_fail},
            'PC-2_independence_witness': {'met': len(witnesses) >= 1,
                                          'witnesses': witnesses},
        },
        'T1': {'state': 'LIST_ABSENT', 'deviation': 'D-T1 (CC)',
               'note': 'T1 forbidden-string list (13 lines, md5 prefix 04438b74) not '
                       'supplied to the CC leg; self-grep not performed'},
        'deviations': ['D-T1 (CC): T1 list absent, self-grep skipped, state LIST_ABSENT'],
        'route_agreement': 'route A (predicate) and route B (literal lookup) agreed on '
                           'every row (asserted per row at evaluation time)',
    }
    blob = json.dumps(checkpoint, ensure_ascii=False, indent=2)
    open(CHECKPOINT_PATH, 'w', encoding='utf-8').write(blob + '\n')
    md5 = hashlib.md5(open(CHECKPOINT_PATH, 'rb').read()).hexdigest()
    print(f'checkpoint written: {CHECKPOINT_PATH}  md5 {md5}')
    for r in results:
        print(f"  {r['verdict']}  C1={r['C1']!s:5} C2={r['C2']!s:5}  {r['object']}")
    print(f"  F-QUANTA-1 {checkpoint['falsifiers']['F-QUANTA-1']['state']} (inert-by-inventory) | "
          f"F-QUANTA-2 {checkpoint['falsifiers']['F-QUANTA-2']['state']} | "
          f"F-QUANTA-3 REGISTERED_NOT_EXECUTED")
    print(f"  PC-1 met={checkpoint['promotion_conditions']['PC-1_nontrivial_partition']['met']} "
          f"({n_pass} pass / {n_fail} fail) | PC-2 met="
          f"{checkpoint['promotion_conditions']['PC-2_independence_witness']['met']} "
          f"witnesses={witnesses}")

# ------------------------------------------------------------------- compare


def parse_hypotheses(text):
    """Parse section-5 predicted outcomes at run time (consulted only here, never in evaluate)."""
    sec = memo_section(text, 5)
    out = []
    for m in re.finditer(r'^\*\s+\*\*(.+?):\*\*\s+(PASS|FAIL)', sec, re.M):
        name = re.sub(r'\s*\([^)]*\)\s*$', '', m.group(1)).strip()
        out.append((name, m.group(2)))
    if not out:
        print('HALT: no hypotheses parsed from section 5', file=sys.stderr)
        sys.exit(1)
    return out


def cmd_compare():
    memo_text = load_memo_guarded()
    checkpoint = json.load(open(CHECKPOINT_PATH, encoding='utf-8'))
    hyps = parse_hypotheses(memo_text)
    results = checkpoint['results']
    rows = []
    for name, predicted in hyps:
        matches = [r for r in results if name in r['object'] or r['object'] in name]
        if len(matches) != 1:
            print(f'HALT: hypothesis {name!r} matches {len(matches)} inventory rows',
                  file=sys.stderr)
            sys.exit(1)
        r = matches[0]
        rows.append({'object': r['object'], 'predicted': predicted,
                     'machine': r['verdict'], 'concordant': predicted == r['verdict']})
    if len(rows) != len(results):
        print(f'HALT: {len(rows)} hypotheses vs {len(results)} inventory rows', file=sys.stderr)
        sys.exit(1)
    out = {'gate': 'G-QUANTA', 'leg': 'cc',
           'checkpoint_md5': hashlib.md5(open(CHECKPOINT_PATH, 'rb').read()).hexdigest(),
           'rows': rows, 'PC-3_met': all(r['concordant'] for r in rows)}
    blob = json.dumps(out, ensure_ascii=False, indent=2)
    open(COMPARE_PATH, 'w', encoding='utf-8').write(blob + '\n')
    md5 = hashlib.md5(open(COMPARE_PATH, 'rb').read()).hexdigest()
    print(f'compare written: {COMPARE_PATH}  md5 {md5}')
    for r in rows:
        mark = 'concordant' if r['concordant'] else 'DISCORDANT'
        print(f"  {mark}  predicted {r['predicted']} / machine {r['machine']}  {r['object']}")
    print(f"  PC-3_met={out['PC-3_met']}")

# ------------------------------------------------------------------ selftest


def cmd_selftest():
    import copy
    import os
    import tempfile
    # S1: every lookup-table entry agrees with route A over the full triple domain.
    for cs in CONFIG_SPACES:
        for inv in (True, False):
            for fc in FUNCTIONAL_CLASSES:
                assert route_a(cs, inv, fc) == ROUTE_B[(cs, inv, fc)], (cs, inv, fc)
    print('  green  S1 route A == route B on all 16 triples')
    # S2: outcome truth table spot checks (synthetic rows, no ledger objects named).
    mk = lambda cs, inv, fc: evaluate_row({'object': 'synthetic', 'ledger_ref': 'none',
                                           'perspective': 'L-Perspective', 'config_space': cs,
                                           'invariant': 'X' if inv else None,
                                           'functional_class': fc, 'invariant_present': inv})
    assert mk('Continuous', True, 'Rigid Constraint')['verdict'] == 'PASS'
    assert mk('Continuous', True, 'Competing Exponents')['verdict'] == 'PASS'
    assert mk('Continuous', False, 'Rigid Constraint')['verdict'] == 'FAIL'
    assert mk('Discrete', True, 'Competing Exponents')['verdict'] == 'FAIL'
    assert mk('Continuous', True, 'None')['verdict'] == 'FAIL'
    assert mk('Continuous', True, 'Single Exponent')['verdict'] == 'FAIL'
    print('  green  S2 truth-table spot checks (6 cases)')
    # S3: memo guard halts on a one-byte tamper.
    raw = bytearray(open(MEMO_PATH, 'rb').read())
    raw[100] ^= 1
    with tempfile.TemporaryDirectory() as td:
        tampered = os.path.join(td, MEMO_PATH)
        open(tampered, 'wb').write(bytes(raw))
        import subprocess
        p = subprocess.run([sys.executable, os.path.abspath(__file__), 'evaluate'],
                           cwd=td, capture_output=True, text=True)
        assert p.returncode == 1 and 'memo guard failed' in p.stderr, (p.returncode, p.stderr)
    print('  green  S3 one-byte memo tamper -> halt, exit 1, no checkpoint')
    print('ALL 3/3 SUITES GREEN')


def main():
    cmds = {'evaluate': cmd_evaluate, 'compare': cmd_compare, 'selftest': cmd_selftest}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        print(f'usage: {sys.argv[0]} {{evaluate|compare|selftest}}', file=sys.stderr)
        sys.exit(2)
    cmds[sys.argv[1]]()


if __name__ == '__main__':
    main()
