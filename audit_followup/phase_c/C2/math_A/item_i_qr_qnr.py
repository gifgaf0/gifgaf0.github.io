"""
item_i_qr_qnr.py -- C2 math_A item (i): §2.84 Part A (L3187-3189) "QR/QNR mirror <-> Re/Im axes
of the e7-stabilizer su(3)".  Lead: "a labeling coincidence: 7 XOR a == -a mod 7 in these labels".

§2.84 A is verified by verify_2_84_partA.py in the CYCLIC Fano labelling
   LINES = (1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)   (e_a e_b = e_c on each)
(its text uses [e1,e7] = -2e3 and 'QR {1,2,4} is a Fano line', both true only in that labelling).
The program's sedenion code uses the CD/XOR labelling (lines {i, j, i^j}).
"""
import json
from itertools import permutations, combinations
from collections import Counter
from sedcore import OCT, PTS, LINES as XLINES, oriented_triples

OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = {}
QR, QNR = {1, 2, 4}, {3, 5, 6}

say("I1. identity 7 XOR a == -a (mod 7)")
rows = [(a, 7 ^ a, (-a) % 7, (7 ^ a) % 7 == (-a) % 7) for a in range(0, 8)]
for r in rows: say(f"   a={r[0]}: 7^a={r[1]}, -a mod 7={r[2]}, equal mod 7: {r[3]}")
say(f"   holds for a=1..7: {all(r[3] for r in rows[1:])}  (7^a = 7-a for 0<=a<=7)")
RES['identity_holds'] = all(r[3] for r in rows)

def table_from_oriented(lines):
    T = {}
    for (a, b, c) in lines:
        for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
            T[(x, y)] = (1, z); T[(y, x)] = (-1, z)
    return T
CYC = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]
TC = table_from_oriented(CYC)
TX = table_from_oriented(sorted(set(tuple(t) for t in oriented_triples())))

def Le7_pairing(T):
    return {a: T[(7, a)] for a in range(1, 7)}
pc = Le7_pairing(TC); px = Le7_pairing(TX)
say("\nI2. L_{e7} on e1..e6")
say(f"   cyclic labelling (verify_2_84_partA.py): {[(a, ('+' if s>0 else '-')+'e'+str(b)) for a,(s,b) in pc.items()]}")
say(f"   CD/XOR labelling (sedenion_Fp.py):      {[(a, ('+' if s>0 else '-')+'e'+str(b)) for a,(s,b) in px.items()]}")
for name, p in (("cyclic", pc), ("XOR", px)):
    swap = all((a in QR) == (p[a][1] in QNR) for a in p)
    neg = all(p[a][1] == (-a) % 7 for a in p)
    times3 = all(p[a][1] == (3 * a) % 7 for a in QR)
    say(f"   {name}: QR<->QNR swap: {swap};  pairing is a -> -a (mod 7) [the 7^a identity]: {neg};  "
        f"a -> 3a on QR: {times3}")
    RES[f'{name}_swap'] = swap; RES[f'{name}_is_minus_a'] = neg; RES[f'{name}_is_3a'] = times3

# I3. stabilizer of e7 in the pure-permutation automorphism group of each table, orbits on 1..6
def pure_auts(T):
    out = []
    for img in permutations(range(1, 8)):
        pi = dict(zip(range(1, 8), img))
        ok = all(T[(pi[a], pi[b])] == (s, pi[c]) for (a, b), (s, c) in T.items())
        if ok: out.append(pi)
    return out
say("\nI3. Stab(e7) in the unsigned automorphism group F21 of each table: orbits on {1..6}")
for name, T in (("cyclic", TC), ("XOR", TX)):
    A = pure_auts(T)
    st = [pi for pi in A if pi[7] == 7]
    orbs = set()
    for a in range(1, 7):
        orbs.add(frozenset(pi[a] for pi in st))
    say(f"   {name}: |F21| = {len(A)}, |Stab(e7)| = {len(st)}, orbits = {sorted(sorted(o) for o in orbs)}")
    RES[f'{name}_stab7_orbits'] = sorted(sorted(o) for o in orbs)

# I4. transversals of the J-pairing that are Fano lines (cyclic labelling)
pairs = [tuple(sorted((a, pc[a][1]))) for a in QR]
trans = [set(t) for t in __import__('itertools').product(*pairs)]
cyc_lines = [set(l) for l in CYC]
lt = [sorted(t) for t in trans if t in cyc_lines]
say(f"\nI4. cyclic labelling: J-pairs {pairs}; the 8 transversals, of which Fano lines: {lt}")
say(f"   -> QR = {{1,2,4}} is one of {len(lt)} line-transversals; J maps each to its complementary non-line transversal")
RES['line_transversals'] = lt

# I5. label dependence: over all 30 Fano planes on labels 1..7
planes = set()
for img in permutations(range(1, 8)):
    pi = dict(zip(range(1, 8), img))
    planes.add(frozenset(frozenset(pi[x] for x in l) for l in CYC))
good = 0
for P in planes:
    thr = [l - {7} for l in P if 7 in l]
    if all(len(set(t) & QR) == 1 for t in thr):
        good += 1
say(f"\nI5. Fano planes on labels 1..7: {len(planes)}; planes whose three lines through 7 each pair a QR with a QNR: {good}")
say(f"   perfect matchings of {{1..6}}: 15, QR/QNR-transversal ones: 6; each matching lies in {len(planes)//15} planes")
RES['planes'] = len(planes); RES['planes_with_swap'] = good

json.dump(RES, open("item_i_results.json", "w"), indent=1)
open("item_i_output.txt", "w").write("\n".join(OUT) + "\n")
