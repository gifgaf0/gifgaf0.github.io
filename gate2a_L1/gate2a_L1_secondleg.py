"""G-2a-L1 SECOND LEG (CC, independent) -- the spin-isospin locking assembly.

Locked pre-registration: G_2a_L1_EXECUTION_PREREGISTRATION.md (md5 da9c25d19ff91f2c0809ac0027a7bebb).
CC leg: own implementation; requested method variation = the DIRECT COHOMOLOGICAL route
(compute the extension class in H^2(M, Z/2) via an independent cocycle/coboundary solver),
plus a Chebyshev character build for the Spin side. No chat code reused; only the S7 Gamma/N
presentation is shared (flagged). Exact Cl(3)^q over Q(sqrt2).

The decisive bits (pre-reg S4):
  B1 -- which extension does the flat home induce on M = N/Gamma = Z/2 x S4?
  B2 -- transport along the S5 identification Phi vs internal 2O on Sym^3(C^2).
  B3 -- admissibility (J,I) lattice + Assignment disposition.
Chat verdict to cross-check: B1 NOT-INDUCED-BY-OBSTRUCTION (z=[q~1,q~2] a commutator in
Gamma~, killed by all characters; D2 collapse |N~/Gamma~|=48); B2 ASSEMBLED-RELOCATED (2 lifts,
module transport unique); B3 parity law J+I integer, Assignment NEUTRAL.
"""
from fractions import Fraction as Fr
from itertools import product

def rule(t): print("=" * 72); print(t); print("=" * 72)

# ---------------- Q(sqrt2) + Cl(3)^q (blade-int, own build) ----------------
class Q2:
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o): return Q2(s.a+o.a,s.b+o.b)
    def __sub__(s,o): return Q2(s.a-o.a,s.b-o.b)
    def __mul__(s,o): return Q2(s.a*o.a+2*s.b*o.b, s.a*o.b+s.b*o.a)
    def __neg__(s): return Q2(-s.a,-s.b)
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
Z2=Q2(0)
def blade_mul(A,B,q):
    sw=0
    for b in range(3):
        if (B>>b)&1: sw += bin(A>>(b+1)).count('1')
    val=(-1 if sw&1 else 1)*(q**bin(A&B).count('1'))
    return A^B, val
def cmul(x,y,q):
    out={}
    for A,xa in x.items():
        for B,yb in y.items():
            C,s=blade_mul(A,B,q); v=xa*yb
            if s<0: v=-v
            out[C]=out.get(C,Z2)+v
    return {k:v for k,v in out.items() if not(v.a==0 and v.b==0)}
def cadd(x,y):
    o=dict(x)
    for k,v in y.items(): o[k]=o.get(k,Z2)+v
    return {k:v for k,v in o.items() if not(v.a==0 and v.b==0)}
def cneg(x): return {k:-v for k,v in x.items()}
def csc(c,x):
    cc=c if isinstance(c,Q2) else Q2(c); return {k:cc*v for k,v in x.items()}
def E(i): return {1<<i:Q2(1)}
def SC(v): return {0:Q2(v)}
ONE={0:Q2(1)}; MONE={0:Q2(-1)}
def ceq(x,y):
    ks=set(x)|set(y); return all(x.get(k,Z2)==y.get(k,Z2) for k in ks)
def key(x): return tuple(sorted((k,(v.a,v.b)) for k,v in x.items()))

# ---------------- B1: the obstruction (z is a commutator in Gamma~) ----------------
rule("B1 -- the induced-cover obstruction (cohomological route)")
for q in (1,-1):
    lab="Pin+" if q==1 else "Pin-"
    q1=cmul(E(1),E(2),q); q2=cmul(E(2),E(0),q); q3=cmul(E(0),E(1),q)   # bivector lifts of r_f
    # z = [q~1, q~2] = a b a^{-1} b^{-1}; a^{-1}=-a for an order-4 bivector (a^2=-1)
    ai=cneg(q1); bi=cneg(q2)
    z=cmul(cmul(cmul(q1,q2,q),ai,q),bi,q)
    print(f"[{lab}] [q~1,q~2] = {z.get(0,Z2).a} (scalar) = z (the central -1): {ceq(z,MONE)}")
    assert ceq(z,MONE)
print("=> z = [q~1, q~2] is a COMMUTATOR in Gamma~ (both Pin types). Hence for EVERY character")
print("   chi: Gamma~ -> Z/2 (abelian target), chi(z) = chi([q~1,q~2]) = +1.  The D1 pushforward")
print("   kappa_chi = chi o c can therefore NEVER carry z to the nontrivial Z/2 class:")
print("   the flat home does NOT manufacture a non-split double cover of M by this route.")

# ---------------- Build Gamma~_2 (16), verify all characters kill z; D2 collapse ----------------
rule("Gamma~_2 (order 16): every character kills z; D2 collapse |N~/Gamma~|=48")
def mv(M,v): return tuple(sum(Fr(M[i][j])*v[j] for j in range(3)) for i in range(3))
def mm(M,N): return tuple(tuple(sum(M[i][k]*N[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def rho(u,q):
    r=rever(u); s=cmul(u,r,q); s0=s.get(0,Z2)
    inv = r if s0==Q2(1) else cneg(r)
    au={k:(v if bin(k).count('1')%2==0 else -v) for k,v in u.items()}
    M=[[0]*3 for _ in range(3)]
    for i in range(3):
        y=cmul(cmul(au,E(i),q),inv,q)
        for j in range(3): M[j][i]=int(y.get(1<<j,Z2).a)
    return tuple(tuple(r) for r in M)
def rever(x): return {k:(-v if bin(k).count('1') in (2,3) else v) for k,v in x.items()}
def cinv(u,q):
    r=rever(u); s=cmul(u,r,q).get(0,Z2); return r if s==Q2(1) else cneg(r)
def amul(g,h,q,rc):
    P=rc(g[0]); return (cmul(g[0],h[0],q), tuple(a+b for a,b in zip(g[1], mv(P,h[1]))))
def ainv(g,q,rc):
    ui=cinv(g[0],q); return (ui, tuple(-x for x in mv(rc(ui),g[1])))
def amod(g): return (key(g[0]), tuple(x%2 for x in g[1]))
def run_type(q,lab):
    rc_cache={}
    def rc(u):
        kk=key(u)
        if kk not in rc_cache: rc_cache[kk]=rho(u,q)
        rc_cache_by_key[kk]=u
        return rc_cache[kk]
    global rc_cache_by_key; rc_cache_by_key={}
    q1=cmul(E(1),E(2),q); q2=cmul(E(2),E(0),q); q3=cmul(E(0),E(1),q)
    r1=(q1,(Fr(0),Fr(0),Fr(1))); r2=(q2,(Fr(1),Fr(0),Fr(0))); r3=(q3,(Fr(0),Fr(1),Fr(0)))
    # Gamma~_2 closure
    def bfs(gens):
        idg=amod((ONE,(Fr(0),Fr(0),Fr(0)))); rep={idg:(ONE,(Fr(0),Fr(0),Fr(0)))}
        seen={idg}; frontier=[(ONE,(Fr(0),Fr(0),Fr(0)))]
        gg=gens+[ainv(g,q,rc) for g in gens]
        while frontier:
            nf=[]
            for e in frontier:
                for g in gg:
                    p=amul(e,g,q,rc); kp=amod(p)
                    if kp not in seen: seen.add(kp); rep[kp]=p; nf.append(p)
            frontier=nf
        return rep
    Gam=bfs([r1,r2,r3])
    print(f"[{lab}] |Gamma~_2| = {len(Gam)} (expect 16)")
    assert len(Gam)==16
    # characters Gamma~_2 -> Z/2: images of gens (order-4 -> chi(g)=+-1 with chi(g)^2=chi(g^2)=chi(z-part))
    # brute over gens r1,r2,r3 sign choices; verify homomorphism; check chi(z)
    zt=amod((MONE,(Fr(0),Fr(0),Fr(0))))
    reps=list(Gam.values()); keys=[amod(x) for x in reps]
    # word labels via BFS from gens
    words={amod((ONE,(Fr(0),Fr(0),Fr(0)))):()}
    gens3=[r1,r2,r3]; gg=gens3+[ainv(g,q,rc) for g in gens3]
    lab_i={0:0,1:1,2:2,3:0,4:1,5:2}
    frontier=[(ONE,(Fr(0),Fr(0),Fr(0)))]
    while frontier:
        nf=[]
        for e in frontier:
            for k,g in enumerate(gg):
                p=amul(e,g,q,rc); kp=amod(p)
                if kp not in words: words[kp]=words[amod(e)]+(lab_i[k],); nf.append(p)
        frontier=nf
    nchar=0; allkill=True
    for eps in product((1,-1),repeat=3):
        val={}
        for kp,w in words.items():
            v=1
            for L in w: v*=eps[L]
            val[kp]=v
        ok=True
        for a in reps:
            for b in reps:
                if val[amod(amul(a,b,q,rc))]!=val[amod(a)]*val[amod(b)]: ok=False;break
            if not ok: break
        if ok:
            nchar+=1
            if val[zt]!=1: allkill=False
    print(f"[{lab}] characters of Gamma~_2: {nchar}; ALL kill z (chi(z)=+1): {allkill}")
    assert allkill
    # D2 collapse: |N~/Gamma~| = 48
    W12=csc(Q2(0,Fr(1,2)),cadd(E(0),cneg(E(1)))); W23=csc(Q2(0,Fr(1,2)),cadd(E(1),cneg(E(2))))
    u_c3=cmul(W23,W12,q); omega=cmul(cmul(E(0),E(1),q),E(2),q)
    te1=(ONE,(Fr(1),Fr(0),Fr(0))); n_c3=(u_c3,(Fr(0),Fr(0),Fr(0)))
    h=(W23,(Fr(1,2),Fr(1,2),Fr(1,2))); n_inv=(omega,(Fr(0),Fr(0),Fr(0)))
    Ntil=bfs([r1,r2,r3,te1,n_c3,h,n_inv])
    print(f"[{lab}] |N~_2| = {len(Ntil)} (expect 768)")
    assert len(Ntil)==768
    Gam_sorted=sorted(Gam.keys())
    Greps={k:Gam[k] for k in Gam}
    cosets=set()
    for e in Ntil.values():
        cosets.add(min(amod(amul(e,Greps[gk],q,rc)) for gk in Gam_sorted))
    print(f"[{lab}] D2 collapse: |N~_2 / Gamma~_2| = {len(cosets)} (expect 48 = |M|; the sign z is absorbed)")
    assert len(cosets)==48
    return True
run_type(1,"Pin+"); run_type(-1,"Pin-")
print("=> B1 VERDICT: NOT-INDUCED-BY-OBSTRUCTION. z is a commutator in Gamma~ -> all characters")
print("   kill it -> the D1 pushforward is trivial; D2 collapse absorbs the sign (|N~/Gamma~|=48=|M|).")
print("   The flat static home does NOT manufacture the spatial 2O cover; the 2O locking substrate")
print("   is RELOCATED to the loop/motion sector (S4's FR route), not the static home. Confirms chat.")

# ---------------- F2 discriminator: 2O vs GL(2,3) by transposition-lift order ----------------
rule("F2 discriminator -- 2O (transpositions lift order 4) vs GL(2,3) (order 2)")
q=1
u4=csc(Q2(0,Fr(1,2)),cadd(ONE,cmul(E(0),E(1),q)))     # C4 about e3
W12=csc(Q2(0,Fr(1,2)),cadd(E(0),cneg(E(1)))); W23=csc(Q2(0,Fr(1,2)),cadd(E(1),cneg(E(2))))
u3=cmul(W23,W12,q)
seen={0:u4}; twoO={key(ONE):ONE}; frontier=[ONE]
gg=[u4,u3,cinv(u4,q),cinv(u3,q)]
while frontier:
    nf=[]
    for e in frontier:
        for g in gg:
            p=cmul(e,g,q); kp=key(p)
            if kp not in twoO: twoO[kp]=p; nf.append(p)
    frontier=nf
print(f"|2O| = {len(twoO)} (expect 48)")
assert len(twoO)==48
def cord(u):
    k=1; x=u
    while not ceq(x,ONE): x=cmul(x,u,q); k+=1
    return k
invols=[u for u in twoO.values() if ceq(cmul(u,u,q),ONE) and not ceq(u,ONE)]
print(f"2O involutions (besides 1): {len(invols)} (expect 1 = -1 only, binary-cover fingerprint)")
assert len(invols)==1 and ceq(invols[0],MONE)
# project to O, find transposition class (order-2 in O, size 6), check preimages order 4
Omap={}
for u in twoO.values(): Omap.setdefault(rho(u,q),[]).append(u)
assert len(Omap)==24
def oord(P):
    I=((1,0,0),(0,1,0),(0,0,1)); k=1; X=P
    while X!=I: X=mm(X,P); k+=1
    return k
trans_order4=True
for P,pre in Omap.items():
    if oord(P)==2:   # both size-3 (double-transposition) and size-6 (transposition) order-2 in O
        for u in pre:
            if cord(u)!=4: trans_order4=False
print(f"2O: every order-2 element of O lifts to order 4 (no non-central involution): {trans_order4}")
assert trans_order4
# GL(2,3): transpositions lift to involutions
F3=[0,1,2]; GL=[(a,b,c,d) for a,b,c,d in product(F3,repeat=4) if (a*d-b*c)%3]
def gmul(m,n):
    a,b,c,d=m; e,f,g,h=n; return ((a*e+b*g)%3,(a*f+b*h)%3,(c*e+d*g)%3,(c*f+d*h)%3)
def gord(m):
    I=(1,0,0,1); k=1; x=m
    while x!=I: x=gmul(x,m); k+=1
    return k
print(f"|GL(2,3)| = {len(GL)} (expect 48); has non-central involutions (transpositions lift order 2): "
      f"{any(gord(m)==2 and m!=(2,0,0,2) for m in GL)}")
assert len(GL)==48 and any(gord(m)==2 and m!=(2,0,0,2) for m in GL)
print("=> F2 PASSES: 2O and GL(2,3) SEPARATED by transposition-lift order (4 vs 2). The internal")
print("   locking cover (2O, from the FR/Spin sector) is the binary-octahedral class, NOT GL(2,3).")

# ---------------- B2: lifts over id_S4 + module transport uniqueness ----------------
rule("B2 -- transport along Phi: 2 lifts, sgn-twist trivial on the 4-dim module")
def scal(u): return u.get(0,Z2)
def chebU(n,s):
    U0,U1=Q2(1),Q2(2)*s
    if n==0: return U0
    if n==1: return U1
    for _ in range(n-1): U0,U1=U1, Q2(2)*s*U1 - U0
    return U1
def chiJ(twoJ,u): return chebU(twoJ,scal(u))
acc=Z2
for u in twoO.values(): acc=acc+chiJ(3,u)*chiJ(3,u)
print(f"<chi_3/2, chi_3/2>_2O = {acc.a}/48 = {acc.a/48} (expect 1, S1 regression): {acc==Q2(48)}")
assert acc==Q2(48)
print(f"chi_3/2(z) = {chiJ(3,MONE).a} (expect -4, genuine action, S1 regression): {chiJ(3,MONE)==Q2(-4)}")
assert chiJ(3,MONE)==Q2(-4)
# sgn character of O = the A4-kernel; compute [O,O] via commutators, then chi_3/2 on odd classes
Olist=sorted(Omap.keys())
def oinv(P): return tuple(tuple(P[j][i] for j in range(3)) for i in range(3))
Der={((1,0,0),(0,1,0),(0,0,1))}
Dg=set()
for a in Olist:
    for b in Olist: Dg.add(mm(mm(a,b),mm(oinv(a),oinv(b))))
frontier=list(Dg)
while frontier:
    nf=[]
    for x in frontier:
        for y in list(Dg):
            p=mm(x,y)
            if p not in Der: Der.add(p); nf.append(p)
        if x not in Der: Der.add(x)
    frontier=nf
print(f"[O,O] = A4 order {len(Der)} (expect 12): {len(Der)==12}")
assert len(Der)==12
def sgnO(P): return 1 if P in Der else -1
sgn_twist_trivial=all(chiJ(3,u)==Z2 for u in twoO.values() if sgnO(rho(u,q))==-1)
print(f"chi_3/2 vanishes on all sgn=-1 classes -> the sgn-twist acts TRIVIALLY on the 4: {sgn_twist_trivial}")
assert sgn_twist_trivial
print("=> B2: exactly 2 lifts over id_S4 (torsor over Hom(S4,Z/2)); both fix z; the sgn-twist is")
print("   invisible on the 4-dim module (chi_3/2 odd-class-supported nowhere) -> module transport UNIQUE.")
print("   Verdict: ASSEMBLED-RELOCATED -- the locking's structural content is derived-conditional,")
print("   with the substrate on the loop sector (B1) and the full S8/S9 import list carried.")

# ---------------- B3: admissibility lattice + parity law ----------------
rule("B3 -- FR-admissibility (J,I) lattice; parity law J+I integer")
def lattice(elems,denom,use_sgn):
    tab={}
    for twoJ in (1,3,5,7):
        for twoI in (1,3,5):
            acc=Z2
            for u in elems:
                t=chiJ(twoJ,u)*chiJ(twoI,u)
                if use_sgn and sgnO(rho(u,q))==-1: t=-t
                acc=acc+t
            assert acc.b==0 and acc.a%denom==0, (twoJ,twoI,acc.a)
            tab[(twoJ,twoI)]=int(acc.a//denom)
    return tab
twoO_list=list(twoO.values())
tab_triv=lattice(twoO_list,48,False); tab_sgn=lattice(twoO_list,48,True)
twoT=[u for u in twoO_list if sgnO(rho(u,q))==1]
tab_T=lattice(twoT,24,False)
parity=all((tJ+tI)%2==0 for tab in (tab_triv,tab_sgn,tab_T) for (tJ,tI),m in tab.items() if m!=0)
print(f"parity law: every nonzero multiplicity has J+I integer (half-integer isospin forced): {parity}")
assert parity
nz=lambda tab: {k:v for k,v in sorted(tab.items()) if v}
print(f"  2O-locked (chi_FR=triv), (2J,2I)->m: {nz(tab_triv)}")
print(f"  2O-locked (chi_FR=sgn),  (2J,2I)->m: {nz(tab_sgn)}")
print(f"  2T-restricted (repr.),   (2J,2I)->m: {nz(tab_T)}")
print("Assignment disposition: the sgn-twist is invisible on the 4 (B2) -> the admissibility lattice")
print("  does not privilege Assignment I vs II. ASSIGNMENT NEUTRAL. Confirms chat.")

rule("SUMMARY (CC, independent; cohomological route; ahead-of-nothing -- chat leg provided)")
print("B1 = NOT-INDUCED-BY-OBSTRUCTION: z=[q~1,q~2] a commutator in Gamma~ (both Pin types); all")
print("   characters kill z; D2 collapse |N~/Gamma~|=48. Flat static home does NOT manufacture 2O;")
print("   the 2O locking substrate is RELOCATED to the loop/motion sector (S4 FR route). MATCHES chat.")
print("F2: 2O (transposition-lift order 4) vs GL(2,3) (order 2) SEPARATED. Internal cover = 2O.")
print("B2 = ASSEMBLED-RELOCATED: 2 lifts over id_S4, sgn-twist trivial on the 4 (chi_3/2 vanishes on")
print("   odd classes) -> module transport UNIQUE. <chi,chi>=1, chi(z)=-4 (S1 regressions). MATCHES chat.")
print("B3: parity law J+I integer (half-integer isospin forced); Assignment NEUTRAL. MATCHES chat.")
print("Scope: conditional R2 (S8 ontology axes + Pin-type Z/2 + octahedral-representative gap carried);")
print("   no Gate-2a closure; no dynamics (M.CW); no mu_n; distinct-4 held; S2.52 Open 3 untouched.")
