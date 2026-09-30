#!/usr/bin/env python3
"""sa_t1a1_build.py (v2: refuses a non-conformant file; adds integer, 3-digit-exponent and extra-zero renderings)
-- G-MSCS-A: builds the numeric part of the author's T1-A1 list from the sealed anchor file.
AUTHOR-SIDE TOOL. It writes every plausible rendering of every number in lo, hi, k_em_max and k_t_max to OUT_FILE and
prints ONLY the pattern count and the md5 / byte count of OUT_FILE -- never a pattern, never a value. The author then
appends, by hand, every catalog / event / collaboration / instrument identifier that appears in src (this tool cannot tell
an identifier from an ordinary word). Scanner of record: t1_scan.py 6b862900 -- a bare-numeric pattern hits only when the
whole numeric token equals it, so signed and unsigned forms, padded and unpadded exponents, and the house superscript
form are all written separately.
Usage:  python3 sa_t1a1_build.py ANCHOR_FILE OUT_FILE      (the anchor file must pass sa_anchor_validate.py first)"""
import hashlib, sys
from decimal import Decimal
SUP = str.maketrans('0123456789-+', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺')
NUMKEYS = ('lo', 'hi', 'k_em_max', 'k_t_max')
def sig_digits(s):
    m = s.lstrip('+-').lower().split('e')[0].replace('.', '').lstrip('0')
    return max(1, len(m.rstrip('0')) or 1)
def renderings(s):
    out = {s, s.lstrip('+'), s.lstrip('+-')}
    v = float(s)
    for x in {v, abs(v)}:
        if x == 0.0:
            out.update({'0', '0.0'}); continue
        n = sig_digits(s)
        out.update({repr(x), '%g' % x, format(Decimal(repr(x)), 'f')})
        if float(x).is_integer() and abs(x) < 1e22:
            out.add(str(int(x)))
        for p in {n - 1, max(0, n - 2), n, n + 1}:
            for E in ('e', 'E'):
                t = ('%.' + str(p) + E) % x
                out.add(t)
                mant, ex = t.split(E)
                out.add(mant + E + str(int(ex)))                     # unpadded exponent
                out.add(mant + E + ('-' if int(ex) < 0 else '+') + '%03d' % abs(int(ex)))   # 3-digit padded exponent
                out.add(mant + E + '%03d' % abs(int(ex)) if int(ex) >= 0 else mant + E + '-%03d' % abs(int(ex)))
                sgn = '-' if mant.startswith('-') else ''
                m = mant.lstrip('-')
                exp = str(int(ex))
                for times in ('×', 'x', '*'):
                    out.add(sgn + m + times + '10^' + exp)
                out.add(sgn + m + '×10' + exp.translate(SUP))        # house style, ASCII sign on the mantissa
                if sgn:
                    out.add('−' + m + '×10' + exp.translate(SUP))    # house style, Unicode minus
                    out.add('−' + m + 'e' + exp)
    return {r for r in out if r and r.strip() == r}
MINLEN = 4   # shorter renderings are too generic: they would match unrelated tokens in locked artifacts (memo section 4.6)
def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    import io, contextlib, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sa_anchor_validate as V
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            ok = V.validate(sys.argv[1])
        except Exception:
            ok = False
    if not ok:
        print('REFUSED: the anchor file does not pass sa_anchor_validate.py (run it for the reason codes); nothing written'); sys.exit(1)
    text = open(sys.argv[1], encoding='utf-8').read()
    pats = set()
    for line in text[:-1].split('\n'):
        fields = dict(f.split('=', 1) for f in line.split(' | '))
        for k in NUMKEYS:
            pats |= renderings(fields[k])
    short = {p for p in pats if len(p) < MINLEN}; pats -= short
    body = '# T1-A1 for G-MSCS-A -- numeric renderings written by sa_t1a1_build.py (values not printed by the tool)\n'
    body += ''.join(p + '\n' for p in sorted(pats))
    body += '# --- identifiers from src: the author appends each catalog / event / collaboration / instrument identifier below ---\n'
    open(sys.argv[2], 'w', encoding='utf-8', newline='\n').write(body)
    raw = body.encode('utf-8')
    print('T1-A1 numeric part written: %d pattern lines (%d renderings shorter than %d characters dropped);  md5 %s  bytes %d  (append the src identifiers, then re-hash)' % (len(pats), len(short), MINLEN, hashlib.md5(raw).hexdigest(), len(raw)))
if __name__ == '__main__':
    main()
