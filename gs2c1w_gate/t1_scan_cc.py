#!/usr/bin/env python3
"""t1_scan_cc.py — Gate G-S2C1-W, CC leg: independent T1 forbidden-string scanner.

Independent re-implementation of the disclosed rule only (lock record §4; memo §6.4 D-W-7);
no code was transferred from the scanner of record.

Rule implemented:
  * pattern-lines-only lists (blank lines and lines starting with '#' are documentation);
  * a NON-NUMERIC pattern is an unconditional HIT on any occurrence;
  * a bare-NUMERIC pattern (digits with optional . e E + -) is a HIT only when the occurrence
    is glued to a letter/underscore token (identifier glue) on either side; an exponent
    continuation (e/E followed by a digit or sign) does not count as identifier glue;
  * digit / sign / dot glue, exponent suffixes, and standalone occurrences of numeric
    patterns are LOGGED, not fatal (formatting-collision class);
  * patterns are reported by index only — never echoed.

The scan is a set union over any number of list files (base ∪ addenda); duplicate
pattern lines collapse to one distinct pattern.
"""
import sys, re, hashlib

IDENT = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_')
NUMERIC_SHAPE = re.compile(r'\d[\d.eE+\-]*\Z')


def load_patterns(list_paths):
    seen, pats = set(), []
    for p in list_paths:
        with open(p, encoding='utf-8') as fh:
            for line in fh:
                s = line.rstrip('\n')
                if not s.strip() or s.startswith('#'):
                    continue
                if s not in seen:
                    seen.add(s)
                    pats.append(s)
    return pats


def is_numeric_pattern(p):
    return bool(NUMERIC_SHAPE.match(p))


def scan_text(pats, text):
    """Return (hits, logged) as lists of (pattern_index, offset)."""
    hits, logged = [], []
    for idx, pat in enumerate(pats):
        numeric = is_numeric_pattern(pat)
        start = 0
        while True:
            pos = text.find(pat, start)
            if pos < 0:
                break
            start = pos + 1
            if not numeric:
                hits.append((idx, pos))
                continue
            before = text[pos - 1] if pos > 0 else ''
            end = pos + len(pat)
            after = text[end] if end < len(text) else ''
            nxt = text[end + 1] if end + 1 < len(text) else ''
            exp_cont = after in 'eE' and (nxt.isdigit() or nxt in '+-')
            glued = (before in IDENT) or (after in IDENT and not exp_cont)
            (hits if glued else logged).append((idx, pos))
    return hits, logged


def scan_file(pats, path):
    with open(path, encoding='utf-8') as fh:
        return scan_text(pats, fh.read())


def main(argv):
    # usage: t1_scan_cc.py <list1>[,<list2>...] <artifact>...
    lists = argv[1].split(',')
    pats = load_patterns(lists)
    rc = 0
    for art in argv[2:]:
        h, l = scan_file(pats, art)
        idxs = sorted({i for i, _ in h})
        tail = f' hit_pattern_idx={idxs}' if h else ' — PASS'
        print(f'{art}: distinct_patterns={len(pats)} HITS={len(h)} logged={len(l)}{tail}')
        rc |= 1 if h else 0
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv))
