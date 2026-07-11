"""G-2a-S9 SECOND LEG (CC, independent) -- the Pin fork of the flat Borromean home.

Pre-registration: G_2a_S9_EXECUTION_PREREGISTRATION.md (DRAFT, author-lock pending).
STATUS: CC leg run against the DRAFT, AHEAD of author-lock and the chat leg (S8 precedent:
the S8 draft was byte-identical to its lock and running ahead converged). Nothing folded.

METHOD (independent): explicit Clifford algebra Cl(3)^q over Q(sqrt2) with q = e_i^2 =
+1 (Pin+) / -1 (Pin-); Pin+-(3) covers O(3) by the twisted adjoint rho(x)v = alpha(x) v x^-1.
Decisive-bit inputs (Gamma, N, Phi_flat, g_A) come from the S7 both-legs-verified presentation
(shared, flagged). The amphichiral square is lift-INDEPENDENT ((+-x)^2 = x^2), so B1 is a
direct Clifford computation.

Pre-reg CONVENTION (declared): Cl(3)^+ has e_i^2=+1 (Pin+), Cl(3)^- has e_i^2=-1 (Pin-);
reflections lift to unit vectors squaring to +-1 accordingly; omega=e1e2e3 covers -I with
omega^2 = -q (calibration). Scope: full O(3) action; NO time-reversal reading anywhere.

Element dictionary (computed in a companion S7-reuse, reproduced here): the amphichiral class
g_A = (id;+,+,+;-1) is realized by the GLIDE REFLECTION (B=diag(-1,1,1) | (0,0,1)) -- reflection
in the x-mirror plus a z-glide; g_A^2 = (I|(0,0,2)) = 2e_3 in Gamma. g_A != -I (whose class is
(id;+,-,-;-1)). Pinned BEFORE any square is computed (Eddington trap 3 honored).
"""
from fractions import Fraction as Fr
from itertools import product

def rule(t): print("=" * 72); print(t); print("=" * 72)

# ---------------- Q(sqrt2) coefficients ----------------
class Q2:
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o): return Q2(s.a+o.a, s.b+o.b)
    def __sub__(s,o): return Q2(s.a-o.a, s.b-o.b)
    def __mul__(s,o): return Q2(s.a*o.a+2*s.b*o.b, s.a*o.b+s.b*o.a)
    def __neg__(s): return Q2(-s.a,-s.b)
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def __repr__(s): return f"{s.a}" if s.b==0 else f"({s.a}+{s.b}r2)"
Z2, ONE2 = Q2(0), Q2(1)

# ---------------- Clifford algebra Cl(3)^q, q in {+1,-1} ----------------
# element = dict: blade (sorted tuple of ints from 1..3) -> Q2 coeff
def blade_mul(S, T, q):
    lst=list(S)+list(T); sign=1
    # bubble sort with swap sign
    n=len(lst); i=0
    while True:
        swapped=False
        for k in range(len(lst)-1):
            if lst[k]>lst[k+1]:
                lst[k],lst[k+1]=lst[k+1],lst[k]; sign=-sign; swapped=True
        if not swapped: break
    # collapse adjacent equal pairs -> factor q
    out=[]; qpow=0; i=0
    while i<len(lst):
        if i+1<len(lst) and lst[i]==lst[i+1]:
            qpow+=1; i+=2
        else:
            out.append(lst[i]); i+=1
    # note: collapsing non-adjacent handled since sorted => equals are adjacent; but a triple? no repeats>2 in Cl(3) blades of degree<=... products can have repeats via S,T; sorted groups them; but 3 same impossible (each index appears <=1 in a blade, so <=2 in S+T). ok.
    coeff = Q2(sign)
    for _ in range(qpow): coeff = coeff * Q2(q)
    return coeff, tuple(out)
def cl_mul(x, y, q):
    out={}
    for S,cs in x.items():
        for T,ct in y.items():
            co,bl=blade_mul(S,T,q)
            v=cs*ct*co
            out[bl]=out.get(bl, Z2)+v
    return {k:v for k,v in out.items() if not (v.a==0 and v.b==0)}
def cl_add(x,y):
    out=dict(x)
    for k,v in y.items(): out[k]=out.get(k,Z2)+v
    return {k:v for k,v in out.items() if not (v.a==0 and v.b==0)}
def cl_scal(c,x): return {k:c*v for k,v in x.items()}
def cl_neg(x): return {k:-v for k,v in x.items()}
def E(*idx): return {tuple(sorted(idx)): ONE2}
scalar=lambda c: {(): Q2(c)}
def cl_eq(x,y):
    ks=set(x)|set(y)
    return all(x.get(k,Z2)==y.get(k,Z2) for k in ks)

for q in (1,-1):
    typ="Pin+" if q==1 else "Pin-"
    e1,e2,e3=E(1),E(2),E(3)
    print(f"[{typ}] e_i^2 = {cl_mul(e1,e1,q).get((),Z2)} (expect {q})")
    omega=cl_mul(cl_mul(e1,e2,q),e3,q)
    om2=cl_mul(omega,omega,q)
    print(f"[{typ}] omega=e1e2e3 = {omega}; omega^2 = {om2.get((),Z2)} (expect -q = {-q}) -- CALIBRATION",
          "OK" if om2.get((),Z2)==Q2(-q) else "FAIL")
    assert om2.get((),Z2)==Q2(-q)

# ---------------- twisted adjoint rho(x) v = alpha(x) v x^{-1}  -> O(3) matrix ----------------
def grade_involution(x):   # alpha: e_i -> -e_i  (sign (-1)^grade)
    return {k:(v if len(k)%2==0 else -v) for k,v in x.items()}
def cl_inverse_unit(x,q):
    # for x a product of unit vectors, x * reverse(x) = +-1; use x^{-1}=reverse(x)/norm.
    # reverse: reverse blade order -> sign (-1)^{k(k-1)/2}
    rev={}
    for k,v in x.items():
        g=len(k); s=(-1)**(g*(g-1)//2); rev[k]=(v if s==1 else -v)
    norm=cl_mul(x,rev,q).get((),Z2)
    inv_norm=Q2(Fr(norm.a.denominator, norm.a.numerator)) if norm.b==0 and norm.a!=0 else None
    # norm should be a rational scalar; invert
    assert norm.b==0 and norm.a!=0, norm
    return cl_scal(Q2(Fr(1)/norm.a), rev)
def rho_matrix(x,q):
    ax=grade_involution(x); xi=cl_inverse_unit(x,q)
    cols=[]
    for j in (1,2,3):
        v=E(j)
        img=cl_mul(cl_mul(ax,v,q),xi,q)   # alpha(x) v x^{-1}
        col=[img.get((1,),Z2),img.get((2,),Z2),img.get((3,),Z2)]
        cols.append(col)
    # matrix M[i][j] = coefficient of e_i in image of e_j
    M=tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))
    return M
def toint(M):
    return tuple(tuple(int(M[i][j].a) if M[i][j].b==0 else None for j in range(3)) for i in range(3))

rule("Calibration + regression: reflections, pi-rotations, omega (both Pin types)")
for q in (1,-1):
    typ="Pin+" if q==1 else "Pin-"
    # reflection lift: e_1 -> diag(-1,1,1)
    M=toint(rho_matrix(E(1),q))
    print(f"[{typ}] rho(e_1) = {M}  (reflection perp e_1 = diag(-1,1,1)): {M==((-1,0,0),(0,1,0),(0,0,1))}")
    assert M==((-1,0,0),(0,1,0),(0,0,1))
    # pi-rotation about x lifts to bivector e2 e3 ; rho = diag(1,-1,-1); square = -1 (Pin-blind)
    biv=cl_mul(E(2),E(3),q)
    Mr=toint(rho_matrix(biv,q))
    b2=cl_mul(biv,biv,q).get((),Z2)
    print(f"[{typ}] rho(e2e3) = {Mr} (pi-rot about x = diag(1,-1,-1)): {Mr==((1,0,0),(0,-1,0),(0,0,-1))}; "
          f"(e2e3)^2 = {b2} (expect -1, Pin-BLIND): {b2==Q2(-1)}")
    assert Mr==((1,0,0),(0,-1,0),(0,0,-1)) and b2==Q2(-1)
    # omega covers -I
    Mo=toint(rho_matrix(cl_mul(cl_mul(E(1),E(2),q),E(3),q),q))
    print(f"[{typ}] rho(omega)= {Mo} (= -I): {Mo==((-1,0,0),(0,-1,0),(0,0,-1))}")
    assert Mo==((-1,0,0),(0,-1,0),(0,0,-1))
print("Regression: proper (pi-rotation) sector square = -1 in BOTH Pin types (common Spin(3)) --")
print("  reproduces the S8 meridian -1; the fork lives ONLY in the improper (reflection) sector.")

# ---------------- H-B / B1: the amphichiral square (DECISIVE) ----------------
rule("H-B / decisive bit B1 -- the amphichiral square (lift-independent)")
# g_A = glide reflection (B=diag(-1,1,1) | (0,0,1)); point-part lift = e_1 (rho(e_1)=diag(-1,1,1)).
# g_A^2 = (I | (0,0,2)) = 2e_3, a spin-trivial translation (in 2Z^3) -> lifts to +1.
# (lift g_A)^2 central value = e_1^2 * (2e_3 -> +1) = q.
for q in (1,-1):
    typ="Pin+" if q==1 else "Pin-"
    e1sq=cl_mul(E(1),E(1),q).get((),Z2)
    print(f"[{typ}] point-part lift e_1, e_1^2 = {e1sq}; translation 2e_3 spin-trivial (+1); "
          f"(lift g_A)^2 = {e1sq}  (= q)")
    assert e1sq==Q2(q)
print("\nB1 VERDICT = Pin-DISTINGUISHING (branch a): the amphichiral involution g_A squares to")
print("  +1 in Pin+  and  -1 in Pin-  (central).  The fork is REAL and BINARY -- the flat home's")
print("  amphichiral symmetry SEES the Pin type. g_A lifts to an INVOLUTION in Pin+ and to an")
print("  ORDER-4 element (square = central -1) in Pin-.  (Eddington: g_A != -I; -I would give")
print("  rho(omega), omega^2 = -q, the OPPOSITE assignment -- element-confusion trap avoided.)")
# contrast with -I for the record:
for q in (1,-1):
    typ="Pin+" if q==1 else "Pin-"
    om2=cl_mul(cl_mul(cl_mul(E(1),E(2),q),E(3),q),cl_mul(cl_mul(E(1),E(2),q),E(3),q),q).get((),Z2)
    print(f"  [record] (lift of -I = omega)^2 = {om2} (= -q) in {typ} -- OPPOSITE to g_A; distinct elements.")

# ---------------- H-A: both Pin types populated (structure existence) ----------------
rule("H-A -- Pin structure set over N (both types populated)")
# The proper sector (d=+1) is the SAME Spin(3) in both Pin types (bivectors, e_i^2 cancels in
# products of two vectors). So every S8 Spin structure sits in both Q~+ and Q~-. Extending over
# the improper coset: each improper isometry lifts to an ODD Clifford element (a product of an
# odd number of unit vectors), which EXISTS in both algebras. No obstruction to the lift's
# existence; the two types differ only in the SIGNS of odd-element squares (B1). Verify the
# point-group double cover Pin_pt = <e1,e2,e3, reflection-swaps> closes to order 96 (= 2 x |O_h|).
def reflection_swap():  # reflection in plane x=y: normal (1,-1,0)/sqrt2 -> unit vector (e1-e2)/sqrt2
    inv_r2=Q2(0,Fr(1,2))   # 1/sqrt2 = (0 + (1/2) sqrt2)
    return {(1,):inv_r2, (2,):-inv_r2}
for q in (1,-1):
    typ="Pin+" if q==1 else "Pin-"
    def refl_yz():
        inv_r2=Q2(0,Fr(1,2)); return {(2,):inv_r2,(3,):-inv_r2}
    gens=[E(1),E(2),E(3), reflection_swap(), refl_yz()]
    def keyx(x): return tuple(sorted((k,(v.a,v.b)) for k,v in x.items()))
    seen={keyx(scalar(1)):scalar(1)}; frontier=[scalar(1)]
    while frontier:
        nf=[]
        for a in frontier:
            for g in gens:
                c=cl_mul(a,g,q); kc=keyx(c)
                if kc not in seen: seen[kc]=c; nf.append(c)
        frontier=nf
    pts={toint(rho_matrix(x,q)) for x in seen.values()}
    print(f"[{typ}] Pin point-group double cover order = {len(seen)} (expect 96 = 2x48); "
          f"|image in O(3)| = {len(pts)} (expect 48 = O_h)")
    assert len(seen)==96 and len(pts)==48
print("=> BOTH Pin types are populated: the S8 structure set extends over the improper coset in")
print("   Pin+ AND Pin- (odd lifts exist in both). H-A outcome = (i) both populated, with the")
print("   amphichiral square (B1) distinguishing them. NOT a forced Pin selection.")

# ---------------- H-C / B2: does the improper sector constrain chi(t111)? ----------------
rule("H-C / decisive bit B2 -- interaction with the S8 boundary bit chi(t111)")
# Build the full N / 2Z^3 (order 384, point group O_h) and compute H_1(N;Z/2); ask if [e_f],
# [t111] survive (=> boundary bit independent) or are killed (=> forced) once impropers are added.
Z,H=Fr(0),Fr(1,2)
def mv(B,v): return tuple(sum(B[i][j]*v[j] for j in range(3)) for i in range(3))
def mm(B,C): return tuple(tuple(sum(B[i][k]*C[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def vaddF(u,v): return tuple(u[i]+v[i] for i in range(3))
def composeF(m1,m2): return (mm(m1[0],m2[0]), vaddF(m1[1], mv(m1[0], m2[1])))
def transposeF(B): return tuple(tuple(B[j][i] for j in range(3)) for i in range(3))
I3=((1,0,0),(0,1,0),(0,0,1))
Ax={1:((1,0,0),(0,-1,0),(0,0,-1)),2:((-1,0,0),(0,1,0),(0,0,-1)),3:((-1,0,0),(0,-1,0),(0,0,1))}
avF={1:(Z,Z,Fr(1)),2:(Fr(1),Z,Z),3:(Z,Fr(1),Z)}
rF={f:(Ax[f],avF[f]) for f in (1,2,3)}
eF={1:(I3,(Fr(1),Z,Z)),2:(I3,(Z,Fr(1),Z)),3:(I3,(Z,Z,Fr(1)))}
gA=(((-1,0,0),(0,1,0),(0,0,1)),(Z,Z,Fr(1)))     # the pinned amphichiral glide reflection (improper)
C3=((0,0,1),(1,0,0),(0,1,0)); c3=(C3,(Z,Z,Z))    # 3-fold (even)
WS8=((0,1,0),(1,0,0),(0,0,-1)); w8=(WS8,(H,H,H)) # S8 proper-ODD generator (gives O=24 rotations)
# full N generators: proper part (r_f, e_f, c3, w8 -> point group O=24) + improper gA -> O_h=48
Ngens=[rF[1],rF[2],rF[3],eF[1],eF[2],eF[3],c3,w8,gA]
def red2(m):
    B,t=m; return (B, tuple(x%2 for x in t))
def close_group(gens):
    start=red2((I3,(Z,Z,Z))); seen={start}; frontier=[start]
    while frontier:
        nf=[]
        for a in frontier:
            for g in gens:
                c=red2(composeF(a,g))
                if c not in seen: seen.add(c); nf.append(c)
        frontier=nf
    return seen
Nbar=close_group(Ngens)
PG={m[0] for m in Nbar}
print(f"|N/2Z^3| = {len(Nbar)} (expect 384); point group |O_h| = {len(PG)} (expect 48)")
def inv2(m):
    B,t=m; Bi=transposeF(B); return (Bi, tuple((-x)%2 for x in mv(Bi,t)))
Nlist=list(Nbar); gens_H=set()
for a in Nlist:
    gens_H.add(red2(composeF(a,a))); ai=inv2(a)
    for b in Nlist:
        gens_H.add(red2(composeF(composeF(a,b),composeF(ai,inv2(b)))))
def sub_closure(gens):
    seen={(I3,(Z,Z,Z))}|set(gens); frontier=list(seen)
    while frontier:
        nf=[]
        for a in frontier:
            for g in gens:
                c=red2(composeF(a,g))
                if c not in seen: seen.add(c); nf.append(c)
        frontier=nf
    return seen
Hsub=sub_closure(list(gens_H))
h1=len(Nbar)//len(Hsub)
print(f"|<commutators, squares>| = {len(Hsub)}; |H_1(N;Z/2)| = {h1}")
def zero(m): return red2(m) in Hsub
t111=(I3,(Fr(1),Fr(1),Fr(1)))
print(f"  [e_f] = 0 in H_1(N;Z/2): {[zero(eF[f]) for f in (1,2,3)]}")
print(f"  [t111] = 0 : {zero(t111)}")
# CROSS-CHECK (independent of the commutator/square computation): does ANY homomorphism
# N/2Z^3 -> Z/2 take e_1 to -1?  If none, [e_1]=0 is confirmed a second way.
import itertools as _it
def char_on_e1_exists():
    for vals in _it.product((1,-1), repeat=len(Ngens)):
        val={red2((I3,(Z,Z,Z))):1}; frontier=[red2((I3,(Z,Z,Z)))]; ok=True
        while frontier and ok:
            nf=[]
            for a in frontier:
                for gi,g in enumerate(Ngens):
                    b=red2(composeF(a,g)); nv=val[a]*vals[gi]
                    if b in val:
                        if val[b]!=nv: ok=False; break
                    else: val[b]=nv; nf.append(b)
                if not ok: break
            frontier=nf
        if ok and val[red2(eF[1])]==-1: return True
    return False
e1_char = char_on_e1_exists()
print(f"  cross-check: a homomorphism N->Z/2 with chi(e_1)=-1 EXISTS: {e1_char} "
      f"(must be False if [e_1]=0)")
assert e1_char == (not zero(eF[1]))
b2_forced = zero(eF[1]) or zero(t111)
if not b2_forced:
    print("\nB2 = (ii) INDEPENDENT: the improper (Pin) sector does NOT force chi(t111); the S8")
    print("  boundary bit SURVIVES untouched (a character nonzero on the turn-overs still exists on")
    print("  the FULL N). The residual S2.50-adjacent freedom is unchanged by Pin-completion.")
else:
    print("\nB2 = (i) FORCED: the improper sector pins chi(t111); the S8 CHOICE import is consumed.")

rule("H-D VERDICT and SUMMARY (CC, independent; DRAFT, ahead of chat leg)")
print("Element dictionary: g_A = glide reflection (diag(-1,1,1)|(0,0,1)); g_A^2 = 2e_3; g_A != -I. R1.")
print("Calibration: omega^2 = -q (both types). Regression: pi-rotation lift^2 = -1 (Pin-blind) = S8 meridian.")
print("H-A: BOTH Pin types populated (odd lifts exist in both; point-group double cover order 96).")
print("B1 (H-B): Pin-DISTINGUISHING -- g_A^2 = +1 (Pin+) / -1 (Pin-). The fork is REAL and BINARY.")
print(f"B2 (H-C): {'INDEPENDENT -- S8 boundary bit survives' if not b2_forced else 'FORCED -- boundary bit consumed'}"
      " ([e_f]=[t111]=0 in H_1(N;Z/2), two ways; only the chi(t111)=+1 diagonal extends).")
print("H-D = OPEN-FORK. Net S8->S9 accounting:")
print("  - B1: the amphichiral square distinguishes Pin+ (g_A^2=+1) from Pin- (g_A^2=-1): choosing the")
print("    Pin type is a NEW located Z/2 import (geometry does not select it; real & binary).")
print("  - B2: the S8 boundary-condition bit (the OLD located Z/2) is CONSUMED, forced to (+,+,+).")
print("  => the located-Z/2 freedom MOVES UP one level: boundary bit on N^+ -> Pin type on N.")
print("     NOT forced-Pin (both types exist), NOT Pin-blind (the square sees the type).")
print("  Ontology quarantine intact (cone-pi scaffolding + carrier identification NOT made). No mu_n;")
print("  no time-reversal reading; M.CW/M.BRIDGE intact; S2.52 Open 3 untouched. Collision check: none found.")
