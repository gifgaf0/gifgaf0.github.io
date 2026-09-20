#!/usr/bin/env python3
"""t1_scan.py — T1 forbidden-string scanner, G-MSCS1 (frozen with the gate list).
Rules: pattern lines only ('#' comment lines and blank lines ignored); case-sensitive substring;
bare numeric patterns (regex ^[0-9.e+\-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+$) under the contextual numeric rule:
a match counts only if the maximal token of numeric characters containing it equals the pattern;
otherwise it is logged as a formatting COLLISION (not a hit). Hits are reported by pattern INDEX only.
Usage: t1_scan.py LIST FILE [FILE...]   -> exit 0 clean, 1 hit, 2 usage.
"""
import re, sys
NUMCHARS = set("0123456789.eE+-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
def load(list_path):
    pats = [l.rstrip("\n") for l in open(list_path, encoding="utf-8")]
    return [p for p in pats if p.strip() and not p.startswith("#")]
def is_numeric(p): return all(c in NUMCHARS for c in p)
def scan_text(text, pats):
    hits, collisions = [], []
    for i, p in enumerate(pats):
        start = 0
        while True:
            j = text.find(p, start)
            if j < 0: break
            if is_numeric(p):
                a = j
                while a > 0 and text[a-1] in NUMCHARS and text[a-1] != " ": a -= 1
                b = j + len(p)
                while b < len(text) and text[b] in NUMCHARS and text[b] != " ": b += 1
                tok = text[a:b]
                (hits if tok == p else collisions).append((i, j))
            else:
                hits.append((i, j))
            start = j + 1
    return hits, collisions
def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(2)
    pats = load(sys.argv[1]); rc = 0
    for f in sys.argv[2:]:
        text = open(f, "rb").read().decode("utf-8", "replace")
        hits, coll = scan_text(text, pats)
        print(f"{f}: {'HIT' if hits else 'CLEAN'}  hits={[i for i,_ in hits]}  numeric_collisions={len(coll)}")
        if hits: rc = 1
    sys.exit(rc)
if __name__ == "__main__": main()
