"""
item_d_matchings.py -- C2 math_A item (d): "the 42 Moreno quadruples are the 42 size-2
matchings of K_{7,7} - M" (§2.68.1 L1995-2010, L496, §2.68.5/§2.68.6).

Definitions:
  K77 - M : bipartite graph A={1..7}, B={1'..7'}, edge (a,b') iff a != b  (42 edges);
            edge (a,b') <-> assessor twoset (a, b+8) <-> element e_a + e_(b+8).
  size-2 matching : unordered pair of vertex-disjoint edges.
  Moreno quadruple (moreno_quadruple_geometry_search.py, Stage 1): unordered pair of
            cross-copy twosets (L,R) with (e_a + e_b)(e_c + e_d) = 0, both coefficients +1.
"""
import json
from itertools import combinations, product
from collections import Counter
from sedcore import *

OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = {}

edges = [(a, b) for a in PTS for b in PTS if a != b]           # (a, b') with b' = b
assert len(edges) == 42
pairs = list(combinations(edges, 2))
m2 = [(e, f) for (e, f) in pairs if e[0] != f[0] and e[1] != f[1]]
say(f"edges of K77-M: {len(edges)};  unordered edge pairs: {len(pairs)};  size-2 matchings: {len(m2)}")
say(f"  check by formula C(42,2) - 14*C(6,2) = {len(pairs)} - {14*15} = {len(pairs) - 14*15}")
RES['size2_matchings'] = len(m2)

def labels(e, f):
    return {e[0], e[1], f[0], f[1]}
def vec(a, b, s=1):
    v = basis(a); v[b] += s; return v
def zero(v):
    return all(c == 0 for c in v)

cat = Counter()
LC = [frozenset(set(PTS) - set(L)) for L in LINES]
quadset = set()
coassessor_set = set()
for (e, f) in m2:
    lab = labels(e, f)
    x = vec(e[0], e[1] + 8); y = vec(f[0], f[1] + 8)
    ypm = vec(f[0], f[1] + 8, -1)
    pp = zero(mul(x, y)); pm = zero(mul(x, ypm))
    xm = vec(e[0], e[1] + 8, -1)
    mp = zero(mul(xm, y)); mm = zero(mul(xm, ypm))
    if len(lab) < 4:
        kind = f"{len(lab)} distinct labels"
    elif frozenset(lab) in LC:
        kind = "4 labels = Fano-line complement"
    else:
        kind = "4 labels containing a Fano line"
    ann = "++ annihilating" if pp else ("+- annihilating" if (pm or mp) else ("--" if mm else "not annihilating"))
    cat[(kind, ann)] += 1
    if pp:
        quadset.add(frozenset((e, f)))
    if pp or pm or mp or mm:
        coassessor_set.add(frozenset((e, f)))
say("classification of the 651 size-2 matchings (label pattern, annihilation of the signed diagonals):")
for k, v in sorted(cat.items()):
    say(f"   {v:4d}  {k}")
RES['classification'] = {str(k): v for k, v in cat.items()}

# reproduce the ledger's 42 'Moreno quadruples' exactly as the provenance script defines them
cross = [(i, j) for i in range(1, 8) for j in range(9, 16)]
ledger_quads = []
for L in cross:
    for R in cross:
        if L >= R:
            continue
        if zero(mul(vec(*L), vec(*R))):
            ledger_quads.append((L, R))
say(f"\nmoreno_quadruple_geometry_search.py Stage-1 definition reproduces {len(ledger_quads)} quadruples")
as_edges = set(frozenset(((L[0], L[1] - 8), (R[0], R[1] - 8))) for (L, R) in ledger_quads)
say(f"  all are size-2 matchings: {all(len(labels(*tuple(q)))==4 or True for q in as_edges) and as_edges <= set(frozenset(p) for p in m2)}")
say(f"  they equal the '++ annihilating' class above: {as_edges == quadset}")
say(f"  every quadruple's 4 labels form a Fano-line complement: "
    f"{all(frozenset(labels(*tuple(q))) in LC for q in as_edges)}")
say(f"  any diagonal (identity) edge involved: {any(a == b for q in as_edges for (a, b) in q)}")
# the 84 line-complement matchings are exactly the box-kite co-assessor pairs
lc84 = set(frozenset((e, f)) for (e, f) in m2 if frozenset(labels(e, f)) in LC)
say(f"  size-2 matchings with 4 labels forming a line complement: {len(lc84)}; "
    f"equal to the set of mutually annihilating (any signs) assessor pairs: {lc84 == coassessor_set}")
def strut(e):
    return e[0] ^ e[1]
say(f"  each of these 84 lies inside one box-kite (equal strut constant a XOR b'): "
    f"{all(strut(tuple(q)[0]) == strut(tuple(q)[1]) for q in lc84)}")
per_lc = Counter(frozenset(labels(*tuple(q))) for q in as_edges)
say(f"  quadruples per line complement: {sorted(per_lc.values())}")
# the ledger's '84 ordered / 2' reading
ordered = sum(1 for L in cross for R in cross if L != R and zero(mul(vec(*L), vec(*R))))
say(f"  ordered (L,R) with (e_L)(e_R)=0 (both +): {ordered};  two-term ZD elements e_a +- e_b: "
    f"{2*len(cross) - 2*7} (the §2.31 '84' counts elements, not ordered pairs)")
# relation to Y of §2.74/§2.75 (pairs of assessors in Y), using the ledger's list
YB_PAIRS_RAW = [
    ((1,10),(4,15)), ((1,10),(6,13)), ((1,11),(6,12)), ((1,11),(7,13)), ((1,12),(3,14)), ((1,12),(7,10)),
    ((1,13),(2,14)), ((1,13),(3,15)), ((1,14),(4,11)), ((1,14),(5,10)), ((1,15),(2,12)), ((1,15),(5,11)),
    ((2,9),(5,14)), ((2,9),(7,12)), ((2,11),(4,13)), ((2,11),(7,14)), ((2,12),(5,11)), ((2,13),(3,12)),
    ((2,13),(6,9)), ((2,14),(3,15)), ((2,15),(4,9)), ((2,15),(6,11)), ((3,9),(4,14)), ((3,9),(5,15)),
    ((3,10),(5,12)), ((3,10),(6,15)), ((3,12),(6,9)), ((3,13),(4,10)), ((3,13),(7,9)), ((3,14),(7,10)),
    ((4,9),(6,11)), ((4,10),(7,9)), ((4,11),(5,10)), ((4,13),(7,14)), ((4,14),(5,15)), ((4,15),(6,13)),
    ((5,9),(6,10)), ((5,9),(7,11)), ((5,12),(6,15)), ((5,14),(7,12)), ((6,10),(7,11)), ((6,12),(7,13))]
Yedges = set(frozenset(((L[0], L[1] - 8), (R[0], R[1] - 8))) for (L, R) in YB_PAIRS_RAW)
say(f"  Y (§2.75) as edge pairs: {len(Yedges)}; Y subset of the 84 line-complement matchings: {Yedges <= lc84}; "
    f"|Y cap Moreno quadruples| = {len(Yedges & as_edges)}")
RES.update(dict(ledger_quads=len(ledger_quads), equal_pp_class=(as_edges == quadset), lc84=len(lc84),
                lc84_equals_coassessor=(lc84 == coassessor_set), Y_cap_quads=len(Yedges & as_edges),
                ordered_pp=ordered))
json.dump(RES, open("item_d_results.json", "w"), indent=1)
open("item_d_output.txt", "w").write("\n".join(OUT) + "\n")
