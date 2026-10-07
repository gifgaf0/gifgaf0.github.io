"""
item_k_attribution.py -- C2 math_A item (k): de Marrais 2000 (arXiv:math/0011260) attribution.

(1) Scans the ledger sections §2.55 (L1965-1990), §2.68.4 (L2034-2055), §2.41.B (L1746-1779)
    for any literature attribution keyword, and prints the sentences that present the structures.
(2) Verifies by computation that what those sections describe IS the de Marrais structure as the
    ledger itself defines it in §2.78 (L2570, L2577, L2587): 42 assessors (e_i + e_j, i in 1..7,
    j in 9..15, j != i+8), seven box-kites = components of the mutual-zero-division graph, each an
    octahedron on 6 assessors; box-kite label = the octonion index missing from its supports.
"""
import re, json
from itertools import combinations, product
from collections import Counter
import flint
from sedcore import *

LEDGER = "/home/claude/fold/SQT_Master_Ledger_v4_93_CANONICAL.md"
lines = open(LEDGER, encoding="utf-8").read().split("\n")
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
KW = re.compile(r"de Marrais|Marrais|box-kite|assessor|Moreno|Cawagas|Guterman|Đoković|Dokovic|arXiv|Bol\. Soc", re.I)
for name, a, b in (("§2.55", 1965, 1990), ("§2.68.4", 2034, 2055), ("§2.41.B", 1746, 1779)):
    hits = [(n, m.group(0)) for n in range(a, b + 1) for m in KW.finditer(lines[n - 1])]
    say(f"{name} (L{a}-L{b}): literature/attribution keyword hits: {hits if hits else 'NONE'}")
say("  (the only §2.55 hit, L1967, is the V4.17 forward pointer's word 'assessor-sum', not an attribution)")
for n in (1972, 1973, 2036, 2050, 1760):
    say(f"  L{n}: {lines[n-1][:400]}")

# (2) computation
ASS = [(a, b) for a in PTS for b in range(9, 16) if b != a + 8]
def v(a, b, s=1):
    x = basis(a); x[b] += s; return x
def strut(t): return t[0] ^ (t[1] - 8)
missing = {t: sorted(set(PTS) - set(i if i < 8 else i - 8 for x in [ (t[0], t[1]) ] for i in x)) for t in ASS}
groups = {}
for t in ASS: groups.setdefault(strut(t), []).append(t)
say(f"\nassessors: {len(ASS)}; grouped by strut constant a XOR b' -> {len(groups)} groups of sizes {sorted(len(g) for g in groups.values())}")
# missing element of each group = strut constant
ok_missing = all(all(s not in (t[0], t[1] - 8) for t in g) and
                 set(PTS) - set(x for t in g for x in (t[0], t[1] - 8)) == {s} for s, g in groups.items())
say(f"each group's supports miss exactly its strut constant (the §2.31/§2.55 'missing element' m): {ok_missing}")
# kernels: clean two-term vectors in ker L_x are diagonals of the 4 co-assessors in x's box-kite
two = [(i, j, s) for i, j in combinations(range(1, 16), 2) for s in (1, -1)]
ok_ker = True; ok_rank = True
for t in ASS:
    for s in (1, -1):
        x = v(t[0], t[1], s); M = Lmat(x)
        inker = [(i, j, s2) for (i, j, s2) in two if all(c == 0 for c in (M @ __import__('numpy').array(v(i, j, s2))).tolist())]
        partners = set((i, j) for (i, j, _) in inker)
        g = groups[strut(t)]
        strut_opp = (t[1] - 8, t[0] + 8)
        expect = set(g) - {t, strut_opp}
        ok_ker &= (partners == expect and len(inker) == 4)
        rk = flint.fmpz_mat([v(i, j, s2) for (i, j, s2) in inker]).rank()
        ok_rank &= (rk == 4 and exact_rank(M) == 12)
say(f"for all 84 two-term ZDs x: ker L_x contains exactly 4 clean two-term vectors, one diagonal of each of the 4 "
    f"co-assessors (box-kite minus x's assessor and its strut-opposite): {ok_ker}; they span ker L_x (dim 4): {ok_rank}")
json.dump(dict(groups=len(groups), missing_ok=ok_missing, kernel_ok=ok_ker, span_ok=ok_rank),
          open("item_k_results.json", "w"), indent=1)
open("item_k_output.txt", "w").write("\n".join(OUT) + "\n")
