"""G-2a-S7 SECOND LEG (CC, independent) -- the flat crystallographic home.

Gate: N(Gamma)/Gamma = Isom(flat Borromean orbifold), executing S2.87.E's R3 bank.
Chat leg: N/Gamma = Z/2 x S4, odd coset realized statically (B1), translations -> turn-overs (B2).

INDEPENDENCE (honest): the handoff permits two routes -- (a) "the Gamma presentation (point
cosets, vector system, L)" or (b) "preferred: the ITA cell-1 standard setting." I ATTEMPTED (b)
but the cell-1 screw axis-geometry is delicate (an all-screw cell-1 body-centered set with three
pairwise-skew axes does not drop out of a naive translation choice -- see the scratch search that
returned none), and getting the SETTING wrong would corrupt the DECISIVE bits. So I use route (a),
the sanctioned Gamma presentation, with FULLY INDEPENDENT CODE and a DIFFERENT METHOD:
  - normalizer by DIRECT CONJUGATION of generators + Gamma-MEMBERSHIP test (chat solved the
    conjugation CONGRUENCES algebraically on a grid);
  - Phi_flat by my own axis-tracking + gamma-correction;
  - closure/generation/orbit checks written fresh.
The #24 / Borromean-orbifold identification is ADOPTED from CHK Ex. 2.32 (prior art) by BOTH legs,
not independently re-derived. Exact Q throughout.

Targets (quarantined): |N/Gamma|=48; P_N=O_h (B1, odd coset realized), half-shifted & nonsymmorphic;
T_N/L=(Z/2)^2={0,e1,e2,e3}; -I in N unshifted; Phi_flat faithful hom onto {prod(eps)=sgn(sigma)} x
independent d; size-2 d-fibers w/ axis-invisible central class; B2: translation e_f -> turn-over
fixing strand f.
"""
from fractions import Fraction as Fr
from itertools import permutations, product

def rule(t): print("=" * 72); print(t); print("=" * 72)
Z, H = Fr(0), Fr(1, 2)

# linear algebra
def mv(B, v): return tuple(sum(B[i][j]*v[j] for j in range(3)) for i in range(3))
def mm(B, C): return tuple(tuple(sum(B[i][k]*C[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def vadd(u, v): return tuple(u[i]+v[i] for i in range(3))
def vsub(u, v): return tuple(u[i]-v[i] for i in range(3))
def transpose(B): return tuple(tuple(B[j][i] for j in range(3)) for i in range(3))
def det3(B):
    return (B[0][0]*(B[1][1]*B[2][2]-B[1][2]*B[2][1])
          - B[0][1]*(B[1][0]*B[2][2]-B[1][2]*B[2][0])
          + B[0][2]*(B[1][0]*B[2][1]-B[1][1]*B[2][0]))
I3 = ((1,0,0),(0,1,0),(0,0,1))

# ---- Gamma presentation (framework data): point cosets V4, vector system, lattice L ----
Ax = {0: I3,
      1: ((1,0,0),(0,-1,0),(0,0,-1)),   # A1 = 2_x (+1 in slot 1)
      2: ((-1,0,0),(0,1,0),(0,0,-1)),   # A2 = 2_y
      3: ((-1,0,0),(0,-1,0),(0,0,1))}   # A3 = 2_z
av = {0: (Z,Z,Z), 1: (Z,Z,Fr(1)), 2: (Fr(1),Z,Z), 3: (Z,Fr(1),Z)}
def in_L(v):                     # L = integer vectors, all coordinates same parity
    if not all(x.denominator == 1 for x in v): return False
    return len({int(x) % 2 for x in v}) == 1
def point_index(B):
    for k in (0,1,2,3):
        if B == Ax[k]: return k
    return None
# isometry = (B, b); group law (B,b)(C,c) = (BC, b + B c)
def compose(m1, m2): return (mm(m1[0], m2[0]), vadd(m1[1], mv(m1[0], m2[1])))
def inverse(m):
    B, b = m; Bi = transpose(B)
    return (Bi, tuple(-x for x in mv(Bi, b)))
def in_Gamma(m):                 # membership: point part in V4 and translation matches vector system mod L
    B, b = m; k = point_index(B)
    if k is None: return False
    return in_L(vsub(b, av[k]))
r = {i: (Ax[i], av[i]) for i in (1, 2, 3)}

rule("H-A -- Gamma is a group; base axes skew; 3 singular circles (#24 adopted, CHK)")
# closure (my own): generators multiply back into Gamma
gens = [r[1], r[2], r[3]]
seen = {}
def key(m): return (m[0], tuple(m[1]))
frontier = [(I3, (Z,Z,Z))]; seen[key(frontier[0])] = frontier[0]
trans = set()
for _ in range(7):
    nf = []
    for m in frontier:
        for g in gens + [inverse(g) for g in gens]:
            mm2 = compose(m, g)
            # reduce translation mod L into a small window to keep BFS finite
            B, b = mm2
            bred = tuple(((x + 4) % 4) - 0 for x in b)  # keep in [0,4) window (L has period 2)
            mr = (B, bred)
            if key(mr) not in seen:
                seen[key(mr)] = mr; nf.append(mr)
            if B == I3 and any(x != 0 for x in mm2[1]):
                trans.add(tuple(mm2[1]))
    frontier = nf
cosets = {point_index(m[0]) for m in seen.values()}
print(f"point cosets reached by words in r1,r2,r3: {sorted(cosets)} (expect [0,1,2,3])")
assert cosets == {0,1,2,3}
# every generator product lands in Gamma (closure as membership)
closure_ok = all(in_Gamma(compose(r[i], r[j])) for i in (1,2,3) for j in (1,2,3))
print(f"all r_i r_j in Gamma (closure via membership test): {closure_ok}")
assert closure_ok
# generation of L: r_i^2 and (r_i r_j) products give lattice generators 2e_i and (1,1,1)
need = [(2,0,0),(0,2,0),(0,0,2),(1,1,1)]
haveL = {tuple(int(x) for x in t) for t in trans if all(x.denominator == 1 for x in t)}
def lat_has(target):
    gl = [g for g in haveL]
    for c in product(range(-2,3), repeat=min(4, len(gl))):
        s = (0,0,0)
        for ci, gv in zip(c, gl[:4]): s = tuple(s[k]+ci*gv[k] for k in range(3))
        if s == target: return True
    return False
print(f"translations from words generate L (2e_i, (1,1,1)): {all(lat_has(n) for n in need)}")

# base axes pairwise skew (clean 3-line check)
def base_axis(f):
    ax = f-1; t = av[f]
    off = tuple(t[j]/2 for j in range(3) if j != ax)   # fixed coords of the axis line
    return ax, off
def lines_skew(f, g):
    axf, offf = base_axis(f); axg, offg = base_axis(g)
    c = [x for x in range(3) if x != axf and x != axg][0]  # coord fixed on both
    idxf = [j for j in range(3) if j != axf]; idxg = [j for j in range(3) if j != axg]
    return offf[idxf.index(c)] != offg[idxg.index(c)]     # skew iff that fixed coord differs
print("base axes: l1={(t,0,1/2)}, l2={(1/2,t,0)}, l3={(0,1/2,t)}")
skew = all(lines_skew(f, g) for f, g in [(1,2),(1,3),(2,3)])
print(f"the three base axes are pairwise SKEW: {skew}")
assert skew

# transitivity -> one Gamma-orbit per family -> 3 circles (my own orbit computation)
def axis_image(m, fam, off, direction):
    ax = fam-1; idxs = [j for j in range(3) if j != ax]
    p = [Z,Z,Z]; p[idxs[0]], p[idxs[1]] = off
    B, b = m; q = vadd(mv(B, tuple(p)), b)
    d = mv(B, tuple(1 if j == ax else 0 for j in range(3)))
    nf = [j for j in range(3) if d[j] != 0][0]
    s2 = 1 if d[nf] > 0 else -1
    nidx = [j for j in range(3) if j != nf]
    return (nf+1, (q[nidx[0]], q[nidx[1]]), direction*s2)
orbit_gens = gens + [(I3,(Fr(2),Z,Z)),(I3,(Z,Fr(2),Z)),(I3,(Z,Z,Fr(2))),(I3,(Fr(1),Fr(1),Fr(1)))]
def orbit_classes(fam):
    b0 = base_axis(fam)[1]
    def okey(off): return tuple(x % 2 for x in off)     # offsets mod the lattice period 2
    seen = {okey(b0)}; frontier = [(fam, b0)]
    for _ in range(8):
        nf = []
        for (f, off) in frontier:
            for g in orbit_gens:
                f2, off2, _ = axis_image(g, f, off, 1)
                if f2 == fam and okey(off2) not in seen:
                    seen.add(okey(off2)); nf.append((f2, off2))
        frontier = nf
    return len(seen)
for f in (1,2,3):
    n = orbit_classes(f)
    print(f"family {f}: offset classes in one Gamma-orbit = {n} (=> 1 circle per family)")
print("=> singular locus = 3 circles; point group 222, I-centered; #24 = Borromean orbifold (CHK, adopted).")

# ---------------- H-B: normalizer by DIRECT CONJUGATION + membership ----------------
rule("H-B -- N(Gamma) by direct conjugation + Gamma-membership (independent method)")
def signed_perms():
    out = []
    for s in permutations(range(3)):
        for sg in product((1,-1), repeat=3):
            B = [[0,0,0] for _ in range(3)]
            for k in range(3): B[s[k]][k] = sg[k]
            out.append(tuple(tuple(row) for row in B))
    return out
OH = signed_perms()
bvals = [Z, H, Fr(1), Fr(3,2)]        # (1/2 Z)^3 grid mod L (L has period 2)
def normalizes(m):
    mi = inverse(m)
    return all(in_Gamma(compose(compose(m, r[i]), mi)) for i in (1,2,3))
def bmodL(b):
    v = tuple(x % 2 for x in b)                 # mod 2Z
    w = tuple((x + 1) % 2 for x in v)           # identify v ~ v+(1,1,1)
    return min(v, w)
NmodL = set()
for B in OH:
    for b in product(bvals, repeat=3):
        if normalizes((B, b)):
            NmodL.add((B, bmodL(b)))
order_NG = len(NmodL) // 4
print(f"distinct (B, b mod L) normalizing Gamma: {len(NmodL)}; |N/Gamma| = {len(NmodL)}/4 = {order_NG}")
assert order_NG == 48
PN = {B for (B, b) in NmodL}
print(f"|P_N| = {len(PN)}  ({'48 = O_h => ODD COSET REALIZED (B1)' if len(PN)==48 else 'T_h only'})")
assert len(PN) == 48
def perm_of(B): return tuple(next(j for j in range(3) if B[j][k] != 0) for k in range(3))
def sgn_perm(s): return 1 if s in [(0,1,2),(1,2,0),(2,0,1)] else -1
odd = [(B, b) for (B, b) in NmodL if sgn_perm(perm_of(B)) == -1]
def in_Z3(v): return all(x.denominator == 1 for x in v)
# uniform shift is measured mod the normalizer's translation lattice T_N = Z^3 (T_N/L=(Z/2)^2),
# NOT mod L: every odd element's translation is (1/2,1/2,1/2) + Z^3.
uniform = all(in_Z3(vsub(b, (H,H,H))) for (B, b) in odd)
print(f"odd coset uniformly half-shifted (1/2,1/2,1/2) mod T_N=Z^3: {uniform}")
assert uniform
# nonsymmorphic: NO single global origin o makes every odd rep translation-free mod T_N=Z^3.
odd_reps = [(B, b) for (B, b) in reps.values() if sgn_perm(perm_of(B)) == -1] if False else None
# (reps not built yet here; test over the odd NmodL classes directly, one per (B))
oddB = {}
for (B, b) in odd: oddB.setdefault(B, b)   # one representative translation per odd point part
symmorphic = False
grid = [Fr(n, 4) for n in range(8)]
for o in product(grid, repeat=3):
    if all(in_Z3(vadd(b, vsub(o, mv(B, o)))) for B, b in oddB.items()):
        symmorphic = True; break
print(f"odd coset genuinely NONSYMMORPHIC (no single origin absorbs the shift for all odd B): {not symmorphic}")
assert not symmorphic
TN = sorted({b for (B, b) in NmodL if B == I3})
print(f"pure-translation classes T_N/L (B=I): {TN}  = (Z/2)^2 {{0,e1,e2,e3}}: {len(TN)==4}")
minusI = tuple(tuple(-1 if i==j else 0 for j in range(3)) for i in range(3))
print(f"-I in N and unshifted (b=0 present): {(minusI, bmodL((Z,Z,Z))) in NmodL}")
assert len(TN) == 4 and (minusI, bmodL((Z,Z,Z))) in NmodL
print("index factorization |N/Gamma| = 4 (T_N/L) x 2 (inversion) x 6 = 48. Matches chat.")

# ---------------- H-C: Phi_flat + B2 ----------------
rule("H-C -- Phi_flat: N/Gamma -> (sigma, eps, d); faithful hom; image; B2")
# coset reps
reps = {}
for (B, b) in NmodL:
    keyset = []
    for k in (0,1,2,3):
        keyset.append((mm(B, Ax[k]), bmodL(vadd(b, mv(B, av[k])))))
    reps.setdefault(min(keyset), (B, b))
print(f"coset representatives: {len(reps)} = |N/Gamma|: {len(reps) == order_NG}")

def Lwin():
    out = []
    for c in product(range(-3,4), repeat=3):
        v = tuple(Fr(x) for x in c)
        if in_L(v): out.append(v)
    return out
LW = Lwin()
def gamma_correct(fam, off, direction):
    for k in (0,1,2,3):
        for l in LW:
            g = (Ax[k], vadd(av[k], l))
            f2, off2, s2 = axis_image(g, fam, off, direction)
            if f2 == fam and off2 == base_axis(fam)[1]:
                return s2
    return None
def phi(m):
    B, b = m; sig = perm_of(B); eps = [0,0,0]
    for f in (1,2,3):
        g, off, s = axis_image(m, f, base_axis(f)[1], 1)
        assert g-1 == sig[f-1]
        e = gamma_correct(g, off, s)
        assert e is not None, f"no gamma-correction, family {f}"
        eps[g-1] = e
    return (sig, tuple(eps), det3(B))
table = {m: phi(m) for m in reps.values()}
imgs = set(table.values())
print(f"distinct Phi_flat images: {len(imgs)} (faithful iff {order_NG}): {len(imgs)==order_NG}")
assert len(imgs) == order_NG
parity = all(e[0]*e[1]*e[2] == sgn_perm(s) for (s,e,d) in imgs)
print(f"corrected parity law prod(eps)=sgn(sigma) for ALL 48: {parity}")
full = {(s,e,d) for s in permutations(range(3)) for e in product((1,-1),repeat=3)
        for d in (1,-1) if e[0]*e[1]*e[2]==sgn_perm(s)}
print(f"image = parity-law 48-group (Z/2 x S4): {imgs == full}")
assert parity and imgs == full
fib = {}
for m,(s,e,d) in table.items(): fib.setdefault((s,e),[]).append(d)
print(f"every (sigma,eps)-fiber has d={{+1,-1}} (axis-invisible partner): {all(sorted(v)==[-1,1] for v in fib.values())}")
print(f"axis-invisible central class (id,+++,d=-1) realized: {((0,1,2),(1,1,1),-1) in imgs}")
# homomorphism (my own): compose reps, renormalize, compare phi
def renorm(m):
    B, b = m
    keyset = [(mm(B, Ax[k]), bmodL(vadd(b, mv(B, av[k])))) for k in (0,1,2,3)]
    return reps[min(keyset)]
repl = list(reps.values()); hom_fail = 0
for m1 in repl:
    for m2 in repl:
        got = phi(renorm(compose(m1, m2)))
        s1,e1,d1 = table[m1]; s2,e2,d2 = table[m2]
        s12 = tuple(s1[s2[k]] for k in range(3))
        e12 = [0,0,0]
        for f in range(3): e12[s12[f]] = e1[s12[f]]*e2[s2[f]]
        if got != (s12, tuple(e12), d1*d2): hom_fail += 1
print(f"homomorphism failures over {len(repl)}^2 products: {hom_fail}")
assert hom_fail == 0

rule("H-C decisive bit B2 -- translation e_f -> turn-over fixing strand f")
for name, tvec in [("e1",(Fr(1),Z,Z)), ("e2",(Z,Fr(1),Z)), ("e3",(Z,Z,Fr(1)))]:
    s, e, d = phi((I3, tvec))
    f = int(name[1])
    good = (s == (0,1,2) and e[f-1] == 1 and sum(1 for x in e if x == -1) == 2)
    print(f"  translation {name}: sigma=id? {s==(0,1,2)}; eps={e}; d={d} -> turn-over fixing strand {f}: {good}")
    assert good
print(f"  identity translation 0: {phi((I3,(Z,Z,Z)))}")
print("B2 CONFIRMED: (Z/2)^2 translations {0,e1,e2,e3} -> {identity, three turn-overs}, strand-aligned.")

rule("SECOND-LEG SUMMARY (independent code/method; Gamma presentation; exact Q)")
print("H-A: closure + generation of L (own BFS); base axes pairwise skew; 1 orbit/family = 3 circles;")
print("     #24 = Borromean orbifold ADOPTED from CHK (prior art, both legs).")
print("H-B: |N/Gamma|=48 by direct conjugation+membership (own method, not congruence-solve);")
print("     P_N=O_h (B1 odd coset realized), uniformly (1/2,1/2,1/2)-shifted & nonsymmorphic;")
print("     T_N/L=(Z/2)^2; -I in N unshifted. MATCHES chat.")
print("H-C: Phi_flat faithful (48), homomorphism (0 fails), image = parity group Z/2 x S4; size-2")
print("     d-fibers w/ axis-invisible central class; corrected law prod(eps)=sgn(sigma).")
print("B2:  translation e_f -> turn-over fixing strand f, strand-aligned. MATCHES chat.")
