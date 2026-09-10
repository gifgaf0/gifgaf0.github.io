#!/usr/bin/env python3
"""t1_scan.py — T1 forbidden-string scanner for Gate G-S2C1-W (pattern-lines-only; D-W-7 contextual numeric rule).
Usage: t1_scan.py <t1_list> <artifact>... ; exit 1 on any unconditional hit. Reports patterns by index only (never echoes them)."""
import sys, re
GLUE = r'[A-Za-z0-9_.\-]'
def load(path):
    return [l.rstrip('\n') for l in open(path, encoding='utf-8') if l.strip() and not l.startswith('#')]
def scan(pats, text):
    hits, logged = [], []
    for i, p in enumerate(pats):
        numeric = re.fullmatch(r'[0-9][0-9.eE+\-]*', p) is not None
        for m in re.finditer(re.escape(p), text):
            ctx = text[max(0, m.start()-1):m.start()] + '|' + text[m.end():m.end()+1]
            before = text[m.start()-1] if m.start() > 0 else ''
            after  = text[m.end()] if m.end() < len(text) else ''
            after2 = text[m.end()+1] if m.end()+1 < len(text) else ''
            if numeric:
                # D-W-7 (memo §6.4): a bare-numeric pattern is a HIT only when glued to a unit/identifier token
                # (letter or underscore). Digit/sign/dot glue and an exponent suffix are formatting collisions:
                # LOGGED, not fatal (H-S2C-3/12, H-CC-P2-2 lineage).
                ident = r'[A-Za-z_]'
                glued_before = bool(re.fullmatch(ident, before or ' '))
                exponent = after in 'eE' and after != '' and bool(re.fullmatch(r'[0-9+\-]', after2 or ' '))
                glued_after = bool(re.fullmatch(ident, after or ' ')) and not exponent
                (hits if (glued_before or glued_after) else logged).append((i, m.start()))
            else:
                hits.append((i, m.start()))            # non-numeric patterns are unconditional
    return hits, logged
if __name__ == '__main__':
    pats = load(sys.argv[1]); rc = 0
    for a in sys.argv[2:]:
        t = open(a, encoding='utf-8').read()
        h, l = scan(pats, t)
        print(f'{a}: patterns={len(pats)} HITS={len(h)} logged_numeric={len(l)}' + (f' hit_pattern_idx={sorted(set(i for i,_ in h))}' if h else ' — PASS'))
        rc |= 1 if h else 0
    sys.exit(rc)
