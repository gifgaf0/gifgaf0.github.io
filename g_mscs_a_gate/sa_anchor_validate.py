#!/usr/bin/env python3
"""sa_anchor_validate.py -- G-MSCS-A sealed-anchor file validator (staging memo v1, section 4; v2 after the independent
audit: control characters, Unicode separators, and T1-A1 BOM/whitespace now rejected). BLIND BY CONSTRUCTION:
it reports md5, byte count, census, key order and a format verdict per key, and NEVER prints, logs or returns a field
value (not even inside an error message). Intended to be run by the author before sealing, and by either leg only to
confirm the census; the mapper's own masked parse is the read of record.

Usage:  python3 sa_anchor_validate.py ANCHOR_FILE [T1_A1_FILE]
Exit:   0 = every check passed; 1 = at least one check failed; 2 = usage error.

Format (memo section 4.2): UTF-8 without BOM; LF line endings only; no CR, no TAB; exactly one row per line; no blank,
comment or marker lines; the file ends with exactly one LF. A row is  key=value | key=value | ...  with the separator
' | ' (space, bar, space); no leading or trailing bar; no bar anywhere else. Keys in the canonical order below; required
keys exactly once; optional keys at most once, after the required ones, in canonical order."""
import hashlib, math, re, sys

REQUIRED = ['id', 'class', 'delta_def', 'lo', 'hi', 'cl', 'reading', 'geom', 'k_em_max', 'k_t_max', 'src']
OPTIONAL = ['q', 'note']
CANON = REQUIRED + OPTIONAL
FREE_TEXT = {'src', 'note'}                      # the only fields that may hold non-ASCII text; never parsed as numbers
NUM = re.compile(r'^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$')   # ASCII decimal or e-notation only
SEP = ' | '

BAD_UNICODE = {'\u0085', '\u2028', '\u2029', '\ufeff'}
def bad_char(c):
    o = ord(c)
    return (o < 32 and c != '\n') or 127 <= o < 160 or c in BAD_UNICODE

def num_ok(s):
    if not NUM.match(s):
        return False
    try:
        return math.isfinite(float(s))
    except ValueError:
        return False

def check_value(key, val):
    """Return a reason code ('OK' or a failure code). Never echoes the value."""
    if val == '' or val != val.strip():
        return 'EMPTY_OR_PADDED'
    if key not in FREE_TEXT and not all(32 <= ord(c) < 127 for c in val):
        return 'NON_ASCII'            # catches the Unicode minus, superscripts, the multiplication sign, NBSP
    if key == 'class':
        return 'OK' if val == 'spd' else 'CLASS_NOT_READ_BY_THIS_GATE'
    if key == 'delta_def':
        return 'OK' if val == 'tensor_over_EM_minus_1' else 'WRONG_DELTA_DEF'
    if key in ('lo', 'hi'):
        return 'OK' if num_ok(val) else 'NOT_A_PLAIN_NUMBER'
    if key == 'cl':
        if val == 'hard':
            return 'OK'
        return 'OK' if (num_ok(val) and 0.0 < float(val) < 1.0) else 'CL_NOT_IN_(0,1)_OR_hard'
    if key == 'reading':
        return 'OK' if val == 'bound' else ('READING_NOT_MAPPED' if val in ('ceiling', 'margin', 'criterion') else 'UNKNOWN_READING')
    if key == 'geom':
        return 'OK' if val in ('single', 'population') else 'UNKNOWN_GEOM'
    if key in ('k_em_max', 'k_t_max'):
        return 'OK' if (num_ok(val) and float(val) > 0.0) else 'NOT_A_POSITIVE_PLAIN_NUMBER'
    if key == 'q':
        return 'OK' if val in ('phase', 'group') else 'UNKNOWN_Q'
    return 'OK'                        # src, note: free text (bar, CR, LF, TAB already excluded at file level)

def validate(path):
    raw = open(path, 'rb').read()
    ok = True
    print('file: md5 %s  bytes %d' % (hashlib.md5(raw).hexdigest(), len(raw)))
    def fail(msg):
        nonlocal ok
        ok = False
        print('  FAIL ' + msg)
    if raw.startswith(b'\xef\xbb\xbf'):
        fail('BOM present')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        fail('not UTF-8'); return False
    if '\r' in text: fail('CR present (LF line endings only)')
    if '\t' in text: fail('TAB present')
    if any(bad_char(c) for c in text): fail('control character or Unicode line/paragraph separator present (other than the row-ending LF)')
    if not text.endswith('\n'): fail('file does not end with LF')
    if text.endswith('\n\n'): fail('blank line(s) at end of file')
    lines = text[:-1].split('\n') if text.endswith('\n') else text.split('\n')
    if lines == ['']:
        fail('no rows'); return False
    census = {}
    for n, line in enumerate(lines, 1):
        tag = 'row %d' % n
        if line.strip() == '':
            fail(tag + ': blank line'); continue
        if line.startswith('|') or line.rstrip().endswith('|'):
            fail(tag + ': leading or trailing bar')
        fields = line.split(SEP)
        if any('|' in f for f in fields):
            fail(tag + ': SEPARATOR_COLLISION (a bar not in the form " | ")')
        keys, vals = [], {}
        for f in fields:
            if '=' not in f:
                fail(tag + ': field without key=value'); continue
            k, v = f.split('=', 1)
            if k in vals:
                fail(tag + ': duplicate key ' + (k if k in CANON else '<unknown>'))
            if k not in CANON:
                fail(tag + ': unknown key (name withheld)'); continue
            keys.append(k); vals[k] = v
        missing = [k for k in REQUIRED if k not in vals]
        if missing: fail(tag + ': missing required key(s) ' + ','.join(missing))
        order = [k for k in CANON if k in keys]
        if keys != order: fail(tag + ': keys not in canonical order')
        if vals.get('id') != 'SA-%d' % n: fail(tag + ': id is not SA-%d (rows numbered in file order)' % n)
        cls = vals.get('class', '?'); census[cls if cls == 'spd' else 'other'] = census.get(cls if cls == 'spd' else 'other', 0) + 1
        verdicts = {k: check_value(k, vals[k]) for k in keys}
        bad = {k: c for k, c in verdicts.items() if c != 'OK'}
        for k, c in bad.items(): fail('%s: key %s -> %s' % (tag, k, c))
        if 'lo' in vals and 'hi' in vals and verdicts.get('lo') == 'OK' and verdicts.get('hi') == 'OK':
            if not float(vals['lo']) <= float(vals['hi']): fail(tag + ': ORDER (lo must not exceed hi)')
        print('  %s: fields %d  keys-in-order %s  per-key %s' % (tag, len(fields), 'yes' if keys == order else 'NO',
              'all OK' if not bad else '%d failing' % len(bad)))
    print('census: rows %d  per-class %s' % (len(lines), census))
    return ok

def validate_t1a1(path):
    raw = open(path, 'rb').read(); ok = True
    print('T1-A1: md5 %s  bytes %d' % (hashlib.md5(raw).hexdigest(), len(raw)))
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        print('  FAIL not UTF-8'); return False
    if raw.startswith(b'\xef\xbb\xbf'): print('  FAIL BOM present'); ok = False
    if '\r' in text: print('  FAIL CR present'); ok = False
    if any(bad_char(c) for c in text): print('  FAIL control character (TAB included) or Unicode separator present'); ok = False
    if not text.endswith('\n'): print('  FAIL does not end with LF'); ok = False
    pats = [l for l in text.split('\n') if l.strip() and not l.startswith('#')]
    padded = sum(1 for p in pats if p != p.strip())
    if padded: print('  FAIL %d pattern line(s) with leading or trailing whitespace (the scanner would never match them)' % padded); ok = False
    print('  pattern lines %d (values withheld)' % len(pats))
    if not pats: print('  FAIL no pattern lines'); ok = False
    return ok

if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        print(__doc__); sys.exit(2)
    good = validate(sys.argv[1])
    if len(sys.argv) == 3:
        good = validate_t1a1(sys.argv[2]) and good
    print('RESULT: ' + ('PASS' if good else 'FAIL'))
    sys.exit(0 if good else 1)
