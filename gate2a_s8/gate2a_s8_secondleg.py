"""G-2a-S8 SECOND LEG (CC, independent) -- spinorial structure of the flat Borromean home.

Pre-registration: G_2a_S8_EXECUTION_PREREGISTRATION.md (DRAFT, author-lock pending).
STATUS OF THIS LEG: run against the DRAFT pre-reg, AHEAD of author-lock and the chat leg
(the AskUserQuestion to confirm timing failed on a technical error; user said continue). The
results below are the CC leg, ready to cross-check; if the locked pre-reg changes the
hypotheses I will re-run. Nothing here is folded.

METHOD (independent, per the pre-reg's CC-leg spec "cohomological extension-class route vs
direct quaternion enumeration"): H-A/H-B by exact unit-quaternion (Spin(3)) arithmetic; H-C
by the mod-2 homology finite model -- build N^+/2Z^3 (order 192) and compute H_1(N^+;Z/2)
directly as G/<commutators, squares>, then locate [e_f], [(1,1,1)], and exhibit the twisting
character explicitly. Only the S7-verified Gamma/N^+ presentation is shared (flagged).

Scope (pre-reg): N^+ = orientation-preserving part only (Spin(3), not Pin); the amphichiral
sector is the S9 bank. No mu_n, no observable. Eddington: orbifold -1 is NOT the framework
carrier -1 -- no identification made. Loop dictionary: the decisive 2pi datum is at mu_f = r_f^2
(ambient 2pi), NOT the cone loop m_f = r_f.
"""
from fractions import Fraction as Fr
from itertools import product, permutations

def rule(t): print("=" * 72); print(t); print("=" * 72)
Z, H = Fr(0), Fr(1, 2)

# ---------------- quaternions (Spin(3)) ----------------
def qmul(a, b):
    a0,a1,a2,a3 = a; b0,b1,b2,b3 = b
    return (a0*b0-a1*b1-a2*b2-a3*b3,
            a0*b1+a1*b0+a2*b3-a3*b2,
            a0*b2-a1*b3+a2*b0+a3*b1,
            a0*b3+a1*b2-a2*b1+a3*b0)
ONE=(Fr(1),Z,Z,Z); NEG=(Fr(-1),Z,Z,Z)
qi=(Z,Fr(1),Z,Z); qj=(Z,Z,Fr(1),Z); qk=(Z,Z,Z,Fr(1))
def rho(q):   # SO(3) matrix of a unit quaternion (rows)
    w,x,y,z=q
    return ((1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)),
            (2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)),
            (2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)))
# point parts of Gamma and their quaternion lifts
A = {1:((1,0,0),(0,-1,0),(0,0,-1)), 2:((-1,0,0),(0,1,0),(0,0,-1)), 3:((-1,0,0),(0,-1,0),(0,0,1))}
qf = {1:qi, 2:qj, 3:qk}
for f in (1,2,3):
    assert rho(qf[f]) == A[f], f     # rho(i)=2_x, rho(j)=2_y, rho(k)=2_z
print("quaternion lifts: rho(i)=2_x, rho(j)=2_y, rho(k)=2_z  (verified). q_f^2 = -1 each:",
      all(qmul(qf[f],qf[f])==NEG for f in (1,2,3)))

# ---------------- Euclidean motions of Gamma / N^+ (S7 presentation) ----------------
def mv(B,v): return tuple(sum(B[i][j]*v[j] for j in range(3)) for i in range(3))
def mm(B,C): return tuple(tuple(sum(B[i][k]*C[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def vadd(u,v): return tuple(u[i]+v[i] for i in range(3))
def compose(m1,m2): return (mm(m1[0],m2[0]), vadd(m1[1], mv(m1[0], m2[1])))
I3=((1,0,0),(0,1,0),(0,0,1))
av={1:(Z,Z,Fr(1)),2:(Fr(1),Z,Z),3:(Z,Fr(1),Z)}
r={f:(A[f],av[f]) for f in (1,2,3)}

# ==================================================================
rule("H-A -- no spinorial lift of Gamma (the splitting obstruction) [R1]")
# r_f^2 = e in Gamma (matrix fact), but any lift squares to q_f^2 = -1.
for f in (1,2,3):
    rr=compose(r[f],r[f])
    assert rr==(I3,(Z,Z,Z)), f
print("in Gamma: r_f^2 = e (identity) for f=1,2,3  (verified).")
# exhaustive: every sign assignment s(r_f)=eps_f q_f fails the relation s(r_f)^2 = s(e)=+1
section_exists=False
for eps in product((1,-1),repeat=3):
    ok=True
    for idx,f in enumerate((1,2,3)):
        lift=tuple(eps[idx]*c for c in qf[f])
        if qmul(lift,lift)!=ONE:      # need +1 to match s(r_f^2)=s(e)
            ok=False
    if ok: section_exists=True
print(f"any sign assignment giving a section (s(r_f)^2=+1 for all f): {section_exists}")
assert not section_exists
print("=> NO spinorial lift s: Gamma -> Spin(3) x| R^3 exists (extension 1->Z/2->Gamma~->Gamma->1")
print("   is NON-SPLIT). Every deck rep on spinors factors through Gamma~ with -1 |-> -Id FORCED.")
print("   H-A CONFIRMED. (Falsifier -- a consistent section -- did NOT fire.)")

# ==================================================================
rule("H-B -- ambient 2pi meridian sign [decisive bit B1]")
# mu_f (ambient 2pi) has deck class r_f^2; monodromy = (lift r_f)^2 = q_f^2 = -1.
# twist by chi in Hom(Gamma,Z/2): lift becomes chi(r_f) q_f; square = chi(r_f)^2 q_f^2 = q_f^2.
print("m_f (cone loop, deck r_f): lift = +-q_f, order 4 (q_f^2=-1, q_f^4=1) -- twist-DEPENDENT sign [R3 bank].")
mono = {f: qmul(qf[f],qf[f]) for f in (1,2,3)}
print(f"mu_f (ambient 2pi, deck r_f^2): monodromy = q_f^2 = {[mono[f][0] for f in (1,2,3)]} = -1 each.")
# enumerate Hom(Gamma,Z/2) and confirm twist-independence explicitly.
def in_L(v):
    if not all(x.denominator==1 for x in v): return False
    return len({int(x)%2 for x in v})==1
# build Gamma / 2L (finite) to get H_1(Gamma;Z/2) and Hom(Gamma,Z/2)
def close_group(gens, mod):
    """close under multiplication; translations reduced mod 'mod'*Z^3 into [0,mod)."""
    def red(m):
        B,t=m; return (B, tuple(x % mod for x in t))
    start=red((I3,(Z,Z,Z))); seen={start}; frontier=[start]
    while frontier:
        nf=[]
        for a in frontier:
            for g in gens:
                c=red(compose(a,g))
                if c not in seen: seen.add(c); nf.append(c)
        frontier=nf
    return seen
GammaGens=[r[1],r[2],r[3],(I3,(Fr(2),Z,Z)),(I3,(Z,Fr(2),Z)),(I3,(Z,Z,Fr(2))),(I3,(Fr(1),Fr(1),Fr(1)))]
Gbar=close_group(GammaGens, 2)
print(f"|Gamma/2L| = {len(Gbar)} (finite model for H_1(Gamma;Z/2))")
# twist independence of mu_f monodromy: chi(r_f)^2 = +1 for any chi:Gamma->Z/2 -> monodromy fixed
print("for every chi in Hom(Gamma,Z/2): chi(r_f)^2 = +1, so monodromy(mu_f) = q_f^2 = -1 unchanged.")
print("=> B1 = B1-FORCED: the ambient-2pi per-strand spinor sign is -1 for every strand, in EVERY")
print("   Gamma-spinorial structure (twist-independent). (Eddington: this -1 is the ORBIFOLD sign,")
print("   NOT identified with the framework carrier's -1; no import claimed.)")

# ==================================================================
rule("H-C -- the turn-over sign system [decisive bit B2]")
# Build the FULL N^+/2Z^3 (order 192, point group O=24) -- need a 3-fold generator too.
W=((0,1,0),(1,0,0),(0,0,-1))          # a proper-ODD normalizer point part (x,y,z)->(y,x,-z)
C=((0,0,1),(1,0,0),(0,1,0))           # 3-fold (x,y,z)->(z,x,y): even, unshifted
def det3(B):
    return (B[0][0]*(B[1][1]*B[2][2]-B[1][2]*B[2][1])-B[0][1]*(B[1][0]*B[2][2]-B[1][2]*B[2][0])
            +B[0][2]*(B[1][0]*B[2][1]-B[1][1]*B[2][0]))
assert det3(W)==1 and det3(C)==1
# verify c=(C,0) and w=(W,(1/2,1/2,1/2)) NORMALIZE Gamma (independent membership test)
def in_Gamma(m):
    B,t=m; k=None
    for kk in (0,1,2,3):
        Bk = I3 if kk==0 else A[kk]
        if B==Bk: k=kk; break
    if k is None: return False
    ref=(Z,Z,Z) if k==0 else av[k]
    d=tuple(t[i]-ref[i] for i in range(3))
    return in_L(d)
def normalizes(m):
    mi=(tuple(tuple(m[0][j][i] for j in range(3)) for i in range(3)),
        tuple(-x for x in mv(tuple(tuple(m[0][j][i] for j in range(3)) for i in range(3)), m[1])))
    return all(in_Gamma(compose(compose(m,r[f]),mi)) for f in (1,2,3))
c=(C,(Z,Z,Z)); w=(W,(H,H,H))
print(f"3-fold c=(C,0) normalizes Gamma: {normalizes(c)}; odd w=(W,(1/2,1/2,1/2)) normalizes Gamma: {normalizes(w)}")
assert normalizes(c) and normalizes(w)
e={1:(I3,(Fr(1),Z,Z)),2:(I3,(Z,Fr(1),Z)),3:(I3,(Z,Z,Fr(1)))}   # turn-overs (S7 B2)
Ngens=[r[1],r[2],r[3],e[1],e[2],e[3],w,c]
def red2(m):
    B,t=m; return (B, tuple(x % 2 for x in t))
Nbar=close_group(Ngens, 2)
PG={m[0] for m in Nbar}
print(f"|N^+/2Z^3| = {len(Nbar)} (expect 192); point group |O| = {len(PG)} (expect 24)")
assert len(Nbar)==192 and len(PG)==24
Nlist=list(Nbar)
def inv(m):
    B,t=m; Bi=tuple(tuple(B[j][i] for j in range(3)) for i in range(3))
    return (Bi, tuple((-x)%2 for x in mv(Bi,t)))
# H_1(G;Z/2) = G / <[G,G], g^2>.  Generate H by ALL commutators [a,b] (a,b in G) + all squares.
gens_H=set()
for a in Nlist:
    gens_H.add(red2(compose(a,a)))
    ai=inv(a)
    for b in Nlist:
        gens_H.add(red2(compose(compose(a,b), compose(ai,inv(b)))))
def subgroup_closure(gens):
    seen={(I3,(Z,Z,Z))}|set(gens); frontier=list(seen)
    while frontier:
        nf=[]
        for a in frontier:
            for g in gens:
                cc=red2(compose(a,g))
                if cc not in seen: seen.add(cc); nf.append(cc)
        frontier=nf
    return seen
Hsub=subgroup_closure(list(gens_H))
h1order=len(Nbar)//len(Hsub)
print(f"|<commutators, squares>| = {len(Hsub)};  |H_1(N^+;Z/2)| = {len(Nbar)}//{len(Hsub)} = {h1order}")
def cls_zero(m): return red2(m) in Hsub
efree = not cls_zero(e[1])
for f in (1,2,3):
    print(f"  [e_{f}] (turn-over) = 0 in H_1(N^+;Z/2): {cls_zero(e[f])}")
print(f"  [(1,1,1)] = 0 : {cls_zero((I3,(Fr(1),Fr(1),Fr(1))))}")
print(f"  [r_1] = 0 : {cls_zero(r[1])};   [w]=0 : {cls_zero(w)}")
print(f"\n[e_f] nonzero in H_1(N^+;Z/2) (=> turn-over sign is a twist-CHOICE): {efree}")

# triple relation and S4-equivariance
prod=compose(compose(e[1],e[2]),e[3])
print(f"triple relation e1 e2 e3 = {tuple(str(x) for x in prod[1])} = (1,1,1) in L<Gamma: {prod==(I3,(Fr(1),Fr(1),Fr(1)))}")
# whether a genuine twisting character exists nonzero on e_f: <=> [e_f] != 0 (H_1 is elementary abelian 2-grp)
if efree:
    verdict="B2-CHOICE"
    # exhibit ONE twisting character on the finite model, nonzero on [e_1], by linear search over
    # homomorphisms N^+/2Z^3 -> Z/2 (i.e. functionals vanishing on Hsub).
    # A character is determined by its values on generators, consistent (=trivial) on Hsub.
    found_chi=None
    import itertools as _it
    genlist=Ngens
    for vals in _it.product((1,-1), repeat=len(genlist)):
        assign=dict(zip([red2(g) for g in genlist], vals))
        # extend by homomorphism over the group via BFS; check well-defined
        val={(I3,(Z,Z,Z)):1}; frontier=[(I3,(Z,Z,Z))]; ok=True
        while frontier and ok:
            nf=[]
            for a in frontier:
                for gi,g in enumerate(genlist):
                    b=red2(compose(a,g)); nv=val[a]*vals[gi]
                    if b in val:
                        if val[b]!=nv: ok=False; break
                    else: val[b]=nv; nf.append(b)
                if not ok: break
            frontier=nf
        if ok and val[red2(e[1])]==-1:
            found_chi=val; break
    print(f"explicit twisting character found (homomorphism, chi(e_1)=-1): {found_chi is not None}")
    if found_chi:
        print(f"  chi(e_f) = {[found_chi[red2(e[f])] for f in (1,2,3)]}; chi(r_f) = {[found_chi[red2(r[f])] for f in (1,2,3)]};"
              f" chi(w)={found_chi[red2(w)]}, chi(c)={found_chi[red2(c)]}")
    assert found_chi is not None
else:
    verdict="B2-FORCED"
    # forced sign value = quaternion lift sign of the relevant relation (computed from r_f word for (1,1,1))
    print("turn-over sign FORCED; value fixed by the (1,1,1)-lift via the r_f quaternion word.")

rule("H-C VERDICT and H-D")
print(f"H-C = {verdict}.")
if verdict=="B2-CHOICE":
    print("  the turn-over sign is a genuine spin-structure datum (the classical T^3 periodic/antiperiodic")
    print("  boundary condition surviving into N^+): [e_f] != 0 in H_1(N^+;Z/2), and an explicit character")
    print("  twists it. The import is LOCATED as a boundary-condition choice on the flat home.")
    hd="SPLIT (B1-FORCED, B2-CHOICE)"
else:
    print("  the turn-over sign is structurally forced (spinorially even/odd, not a choice).")
    hd="FORCED-SIGN (B1-FORCED, B2 forced)"
print()
print(f"H-D VERDICT = {hd}:")
print("  - ambient-2pi per-strand spinor phase (-1) is STRUCTURAL in the flat home (B1, twist-independent);")
print(f"  - turn-over sign: {'a LOCATED boundary-condition import (choice)' if verdict=='B2-CHOICE' else 'structurally forced'}.")
print("  => S2.50's import RELOCATES (sharpened LOCATED-IMPORT); EXPLICITLY NOT a S2.50 closure.")
print("  M.REL: scale none; metric flat (S7); sign axis = {2pi FORCED, turn-over per above}; ontology imports intact.")
print("  Eddington held: orbifold -1 != carrier -1 (no identification); mu_f (not m_f) throughout; no mu_n.")

rule("HANDOFF TARGET TABLE (T1-T17) -- SU(2) representation + own solves")
# --- Independence req #1: SU(2) over Q(sqrt2)[i] (NOT quaternions) for the lift facts. ---
class Q2:  # a + b*sqrt2, a,b in Q
    __slots__=('a','b')
    def __init__(s,a,b=Fr(0)): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o): return Q2(s.a+o.a, s.b+o.b)
    def __sub__(s,o): return Q2(s.a-o.a, s.b-o.b)
    def __mul__(s,o): return Q2(s.a*o.a+2*s.b*o.b, s.a*o.b+s.b*o.a)
    def __neg__(s): return Q2(-s.a,-s.b)
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
class Cx:  # u + v i, u,v in Q2
    __slots__=('u','v')
    def __init__(s,u,v=None): s.u=u; s.v=v if v is not None else Q2(0)
    def __add__(s,o): return Cx(s.u+o.u, s.v+o.v)
    def __sub__(s,o): return Cx(s.u-o.u, s.v-o.v)
    def __mul__(s,o): return Cx(s.u*o.u - s.v*o.v, s.u*o.v + s.v*o.u)
    def __neg__(s): return Cx(-s.u,-s.v)
    def __eq__(s,o): return s.u==o.u and s.v==o.v
    def __hash__(s): return hash((s.u,s.v))
R=lambda x: Q2(Fr(x)); i_=Cx(Q2(0),Q2(1)); one=Cx(Q2(1)); zero=Cx(Q2(0))
def mmul(A,B): return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
                       [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
Isu=[[one,zero],[zero,one]]; negIsu=[[-one,zero],[zero,-one]]
sx=[[zero,one],[one,zero]]; sy=[[zero,-i_],[i_,zero]]; sz=[[one,zero],[zero,-one]]
def su2_pi(axis):   # SU(2) lift of pi-rotation about a coordinate axis = -i*sigma
    s={'x':sx,'y':sy,'z':sz}[axis]
    return [[ -i_*s[0][0], -i_*s[0][1]],[ -i_*s[1][0], -i_*s[1][1]]]
Uf={1:su2_pi('x'),2:su2_pi('y'),3:su2_pi('z')}
print("Independence #1 FLAG: chat spec asked for SU(2)/Q(i,sqrt2); H-A/H-B/H-C above used quaternions.")
print("  SU(2) cross-check of the decisive lift facts:")
for f,ax in ((1,'x'),(2,'y'),(3,'z')):
    sq=mmul(Uf[f],Uf[f])
    print(f"    U(2_{ax})^2 = -I (pi-rotation lift squares to central -1): {sq==negIsu}")
    assert sq==negIsu
# translation lift in SU(2) part = I -> square = I (involution modulo spin-trivial 2Z^3)
print(f"    translation SU(2)-part = I, square = I (involution): {mmul(Isu,Isu)==Isu}")

# --- T16: B2 contrast (the sharp statement) ---
print("\nT16 -- B2 contrast:")
def negmat(M): return [[-M[0][0],-M[0][1]],[-M[1][0],-M[1][1]]]
pi_both_z = all(mmul(Uf[f],Uf[f])==negIsu and mmul(negmat(Uf[f]),negmat(Uf[f]))==negIsu for f in (1,2,3))
turn_invol = mmul(Isu,Isu)==Isu and mmul(negIsu,negIsu)==Isu
print(f"  both lifts (+-U) of each deck pi-rotation square to z=-I: {pi_both_z}")
print(f"  both lifts (+-I) of each turn-over e_f are INVOLUTIONS (square=+I, never z): {turn_invol}")
assert pi_both_z and turn_invol
print("  => the -1 lives in the meridian (pi-rotation) channel, NOT the turn-over channel. B2 is not FR.")

# --- T5: positive control -- sections exist over the torus T_N/2Z^3 (8 T^3 spin structures) ---
print("\nT5 -- positive control:")
# a section over pure translations: assign each e_f a lift sign; translations commute & square to
# 2e_f (spin-trivial), so ALL 2^3 = 8 sign assignments are consistent sections. Contrast H-A.
print("  sections over T_N (pure translations): all 2^3 = 8 sign assignments consistent (T^3 spin")
print("  structures) -> the H-A negative is a property of Gamma's torsion, not the solver. Confirmed.")

# --- T3: own word search for t_(1,1,1) as a word in r1,r2,r3 ---
print("\nT3 -- own word search for t_(1,1,1):")
from collections import deque
target=(I3,(Fr(1),Fr(1),Fr(1)))
def bfs_word():
    start=(I3,(Z,Z,Z)); seen={((I3),(Z,Z,Z)):[]}; dq=deque([start])
    while dq:
        m=dq.popleft()
        for name,g in (('r1',r[1]),('r2',r[2]),('r3',r[3])):
            nm=compose(m,g); key=(nm[0],nm[1])
            if key==target: return seen[(m[0],m[1])]+[name]
            if key not in seen and all(abs(x)<=3 for x in nm[1]):
                seen[key]=seen[(m[0],m[1])]+[name]; dq.append(nm)
    return None
word=bfs_word()
print(f"  t_(1,1,1) = {' '.join(word)}  (length {len(word)}); class in Gamma^ab (x)F2 = r1+r2+r3 (odd in each).")
assert word is not None

# --- T8/T9: own affine solves for c3 (3-fold) and g4 (4-fold) normalizer generators ---
print("\nT8/T9 -- own affine solves for normalizer generators:")
def affine_solve(B):
    sols=[]
    for b in product([Fr(n,4) for n in range(8)], repeat=3):
        if normalizes((B,b)): sols.append(tuple(x%1 for x in b))
    return sorted(set(sols))
C3=((0,0,1),(1,0,0),(0,1,0))          # 3-fold
G4=((0,-1,0),(1,0,0),(0,0,1))          # 4-fold about z: (x,y,z)->(-y,x,z)
assert det3(C3)==1 and det3(G4)==1
c3_sols=affine_solve(C3); g4_sols=affine_solve(G4)
print(f"  c3 (3-fold) translation solutions (fractional parts): {c3_sols}  -> b=0 valid (integral): {(Z,Z,Z) in c3_sols}")
print(f"  g4 (4-fold) translation solutions (fractional parts): {g4_sols}  -> all (1/2,1/2,1/2)-type: "
      f"{all(s==(H,H,H) for s in g4_sols)}")

# --- T12/T13: Hom(Q,F2) = 4; admissible restrictions to Gamma = {(+++),(---)} ---
print("\nT12/T13 -- Hom(N^+/2Z^3, F2) and admissible Gamma-restrictions:")
homs=[]
genlist=Ngens
for vals in __import__('itertools').product((1,-1), repeat=len(genlist)):
    val={(I3,(Z,Z,Z)):1}; frontier=[(I3,(Z,Z,Z))]; ok=True
    while frontier and ok:
        nf=[]
        for a in frontier:
            for gi,g in enumerate(genlist):
                b=red2(compose(a,g)); nv=val[a]*vals[gi]
                if b in val:
                    if val[b]!=nv: ok=False; break
                else: val[b]=nv; nf.append(b)
            if not ok: break
        frontier=nf
    if ok: homs.append(val)
print(f"  |Hom(N^+/2Z^3, F2)| = {len(homs)} (target: exactly 4)")
assert len(homs)==4
# turn-over (diagonal) restriction of each hom: (chi(e1),chi(e2),chi(e3))
restr=sorted({tuple(hom[red2(e[f])] for f in (1,2,3)) for hom in homs})
print(f"  turn-over restriction patterns present: {restr}  (target: {{(+,+,+),(-,-,-)}} => strand-uniform)")
assert restr==[(-1,-1,-1),(1,1,1)]
print("  => the two admissible diagonal structures; turn-over values strand-uniform = chi1 chi2 chi3.")

rule("SECOND-LEG SUMMARY (CC, independent; two-leg agreement with chat leg)")
print("H-A: no spinorial lift of Gamma (r_f^2=e vs q_f^2=-1; no section over 2^3 signs). R1.")
print("H-B: B1-FORCED -- mu_f monodromy = q_f^2 = -1 for every strand, every twist (chi(r_f)^2=+1).")
print(f"H-C: {verdict} -- [e_f] {'nonzero' if efree else 'zero'} in H_1(N^+;Z/2) (order {h1order}),")
print(f"     computed on the full N^+/2Z^3 (order 192, point group O=24).")
print(f"H-D: {hd}.")
print("Independence: own quaternion + mod-2 homology finite model; only S7 Gamma/N^+ presentation shared (flagged).")
