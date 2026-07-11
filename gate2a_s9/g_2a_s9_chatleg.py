#!/usr/bin/env python3
# =============================================================================
# g_2a_s9_chatleg.py — Gate G-2a-S9, chat-side leg (second in time; CC b6dbb2a first)
# Pre-registration: G_2a_S9_EXECUTION_PREREGISTRATION.md (draft, byte-identical
# at execution; lock-by-forwarding deviation recorded in the report).
# Base: SQT_Master_Ledger_v4_59_CANONICAL.md (md5 863424269d593d0a3ed2cbbf6406b9c4)
# Exact arithmetic: Fractions; Q(sqrt2); Clifford Cl(3)^q with q = e_i^2 = +-1.
# =============================================================================
from fractions import Fraction as F
import itertools, hashlib, math, sys

PASS = 0
def ok(label, cond):
    global PASS
    if not cond:
        print(f"[FAIL] {label}"); sys.exit(1)
    PASS += 1; print(f"[PASS] {label}")
def note(s): print(f"[NOTE] {s}")

# ---------------- exact Q(sqrt2) ----------------
class R2:
    __slots__ = ("a","b")
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): return R2(s.a+o.a, s.b+o.b)
    def __sub__(s,o): return R2(s.a-o.a, s.b-o.b)
    def __mul__(s,o): return R2(s.a*o.a+2*s.b*o.b, s.a*o.b+s.b*o.a)
    def __neg__(s): return R2(-s.a,-s.b)
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def sign(s):
        if s.a==0 and s.b==0: return 0
        if s.a>=0 and s.b>=0: return 1
        if s.a<=0 and s.b<=0: return -1
        d = s.a*s.a - 2*s.b*s.b
        return (1 if d>0 else -1)*(1 if s.a>0 else -1)
R0_=R2(0); R1_=R2(1)

# ---------------- Clifford Cl(3)^q over Q(sqrt2) ----------------
class Cl:
    __slots__=("c","q")
    def __init__(s, c, q):
        s.c={k:v for k,v in c.items() if not (v.a==0 and v.b==0)}; s.q=q
    def __add__(s,o):
        d=dict(s.c)
        for k,v in o.c.items(): d[k]=d.get(k,R0_)+v
        return Cl(d,s.q)
    def __neg__(s): return Cl({k:-v for k,v in s.c.items()}, s.q)
    def __mul__(s,o):
        out={}
        for A,va in s.c.items():
            for B,vb in o.c.items():
                sign=1; res=sorted(A); qpow=0
                for j in sorted(B):
                    cnt=sum(1 for x in res if x>j)
                    sign*=(-1)**cnt
                    if j in res:
                        res.remove(j); qpow+=1
                    else:
                        res.append(j); res.sort()
                val=va*vb
                if sign==-1: val=-val
                if qpow%2==1 and s.q==-1: val=-val
                key=frozenset(res)
                out[key]=out.get(key,R0_)+val
        return Cl(out,s.q)
    def __eq__(s,o): return s.q==o.q and s.c==o.c
    def __hash__(s):
        return hash((s.q,tuple(sorted((tuple(sorted(k)),(v.a,v.b)) for k,v in s.c.items()))))
    def is_scalar(s): return all(len(k)==0 for k in s.c)
    def scalar(s): return s.c.get(frozenset(),R0_)
    def alpha(s):
        return Cl({k:(v if len(k)%2==0 else -v) for k,v in s.c.items()}, s.q)
def cl_scal(x,q): return Cl({frozenset():R2(x)},q)
def E(i,q): return Cl({frozenset([i]):R1_},q)

def rev(x):
    return Cl({k:(v if (len(k)*(len(k)-1)//2)%2==0 else -v) for k,v in x.c.items()}, x.q)
def cinv(x):
    r=rev(x); n=x*r
    assert n.is_scalar(), "non-unit element"
    s=n.scalar()
    assert s==R2(1) or s==R2(-1), f"norm {s.a}+{s.b}sqrt2"
    return r if s==R2(1) else -r
def rho_matrix(x,q):
    xi=cinv(x); cols=[]
    for i in (1,2,3):
        p=x.alpha()*E(i,q)*xi
        col=[]
        for j in (1,2,3):
            v=p.c.get(frozenset([j]),R0_)
            assert v.b==0 and v.a.denominator==1, "rho non-integer"
            col.append(int(v.a))
        for k,v in p.c.items():
            assert len(k)==1 or (v.a==0 and v.b==0), "rho image not a vector"
        cols.append(col)
    return tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))

# ---------------- affine machinery ----------------
def mv(M,v): return tuple(sum(F(M[i][j])*v[j] for j in range(3)) for i in range(3))
def mm(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def tr(M): return tuple(tuple(M[j][i] for j in range(3)) for i in range(3))
def vadd(a,b): return tuple(a[i]+b[i] for i in range(3))
def vsub(a,b): return tuple(a[i]-b[i] for i in range(3))
I3=((1,0,0),(0,1,0),(0,0,1)); A1=((1,0,0),(0,-1,0),(0,0,-1))
A2=((-1,0,0),(0,1,0),(0,0,-1)); A3=((-1,0,0),(0,-1,0),(0,0,1))
def aff(M,t): return (M,tuple(F(x) for x in t))
def acomp(g,h): return (mm(g[0],h[0]), vadd(mv(g[0],h[1]),g[1]))
def ainv(g):
    Mi=tr(g[0]); return (Mi, tuple(-x for x in mv(Mi,g[1])))
r1=aff(A1,(0,0,1)); r2=aff(A2,(1,0,0)); r3=aff(A3,(0,1,0))
avec={I3:(F(0),)*3, A1:(F(0),F(0),F(1)), A2:(F(1),F(0),F(0)), A3:(F(0),F(1),F(0))}
def in_L(v):
    if any(x.denominator!=1 for x in v): return False
    xs=[int(x) for x in v]
    return all(x%2==0 for x in xs) or all(x%2==1 for x in xs)
def in_Gamma(g):
    M,t=g
    return M in avec and in_L(vsub(t,avec[M]))
def normalizes(g):
    gi=ainv(g)
    return all(in_Gamma(acomp(acomp(g,rf),gi)) for rf in (r1,r2,r3)) and \
           all(in_Gamma(acomp(acomp(gi,rf),g)) for rf in (r1,r2,r3))

print("="*78); print("PART 0 — element dictionary adjudication (Eddington trap 3)"); print("="*78)
GLIDE  = aff(((-1,0,0),(0,1,0),(0,0,1)), (0,0,1))
MINUSI = aff(((-1,0,0),(0,-1,0),(0,0,-1)), (0,0,0))
MIRROR23 = ((1,0,0),(0,0,1),(0,1,0))
H_EL = aff(MIRROR23, (F(1,2),F(1,2),F(1,2)))
ok("glide, -I, h all normalize Gamma (two-sided)", all(normalizes(g) for g in (GLIDE,MINUSI,H_EL)))
ok("glide o (-I) = r1 exactly  => glide and -I are the SAME N/Gamma class",
   acomp(GLIDE,MINUSI)==r1)
hh=acomp(H_EL,H_EL)
ok("h^2 = t_(1,1,1) on the nose", hh[0]==I3 and tuple(int(x) for x in hh[1])==(1,1,1))

BASE={1:((F(0),F(0),F(1,2)),(1,0,0)), 2:((F(1,2),F(0),F(0)),(0,1,0)), 3:((F(0),F(1,2),F(0)),(0,0,1))}
def line_eq(pa,da,pb,db):
    if tuple(abs(x) for x in da)!=tuple(abs(x) for x in db): return False
    d=vsub(pb,pa)
    for i in range(3):
        if da[i]==0 and d[i]!=0: return False
    return True
def family_of(d): return [i for i in range(3) if d[i]!=0][0]+1
def gamma_correctors(p,d,f_target):
    bp,bd=BASE[f_target]; sgns=[]
    for M in (I3,A1,A2,A3):
        for v in itertools.product(range(-4,5),repeat=3):
            vv=tuple(F(x) for x in v)
            if not in_L(vv): continue
            g=(M, vadd(avec[M],vv))
            ip=vadd(mv(M,p),g[1]); idd=tuple(int(x) for x in mv(M,tuple(F(x) for x in d)))
            if line_eq(ip,idd,bp,tuple(F(x) for x in bd)):
                sgns.append(1 if idd==bd else -1)
                if len(sgns)>=2: return sgns
    return sgns
def detM(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
           -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
           +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
def phi(n):
    M,t=n; sig=[]; eps=[]
    for f in (1,2,3):
        p,d=BASE[f]
        ip=vadd(mv(M,p),t); idv=tuple(int(x) for x in mv(M,tuple(F(x) for x in d)))
        f2=family_of(idv); sig.append(f2)
        cors=gamma_correctors(ip,idv,f2)
        assert len(cors)>=1, "no corrector found"
        assert all(c==cors[0] for c in cors), "gamma-correction ill-defined"
        eps.append(cors[0])   # composite sign: corrector acts on the post-n direction
    return (tuple(sig), tuple(eps), 1 if detM(M)>0 else -1)

E1a=aff(I3,(1,0,0)); E2a=aff(I3,(0,1,0)); E3a=aff(I3,(0,0,1))
ok("regression vs S7 dictionary: Phi(e1)=(id;(+,-,-);+1)", phi(E1a)==((1,2,3),(1,-1,-1),1))
ok("regression: Phi(e2)=(id;(-,+,-);+1)", phi(E2a)==((1,2,3),(-1,1,-1),1))
ok("regression: Phi(e3)=(id;(-,-,+);+1)", phi(E3a)==((1,2,3),(-1,-1,1),1))
ph_mI=phi(MINUSI); ph_gl=phi(GLIDE); ph_h=phi(H_EL)
print(f"   Phi(-I)    = {ph_mI}")
print(f"   Phi(glide) = {ph_gl}")
print(f"   Phi(h)     = {ph_h}")
ok("COSET INVARIANCE (the structural falsifier that exposed the chat-leg eps bug): "
   "Phi(glide) == Phi(-I)  [same N/Gamma class]", ph_gl==ph_mI)
ok("coset invariance again: Phi(r3 o h) == Phi(h)", phi(acomp(r3,H_EL))==ph_h)
ok("coset invariance: Phi(r2 o -I) == Phi(-I)", phi(acomp(r2,MINUSI))==ph_mI)
ok("Phi(-I) = (id;(+,+,+);-1): -I IS the amphichiral class "
   "(CC dictionary contrast FALSE; chat pre-reg sketch FALSIFIED)",
   ph_mI==((1,2,3),(1,1,1),-1))
ok("Phi(glide) = (id;(+,+,+);-1), as forced by glide = r1 o (-I)",
   ph_gl==((1,2,3),(1,1,1),-1))
note(f"h's own class: {ph_h} — the (23)-transposition improper carrying (1/2,1/2,1/2).")

# ---------------- Pin sectors ----------------
print("="*78); print("PART 1 — Pin(+/-) calibration and S8 regression"); print("="*78)
for q in (1,-1):
    lab="Pin+" if q==1 else "Pin-"
    om=E(1,q)*E(2,q)*E(3,q)
    ok(f"[{lab}] omega^2 = -q  (scalar {-q})", (om*om)==cl_scal(-q,q))
    for (i,j) in ((2,3),(3,1),(1,2)):
        b=E(i,q)*E(j,q)
        ok(f"[{lab}] (e{i}e{j})^2 = -1  (Pin-blind common Spin sector)", (b*b)==cl_scal(-1,q))
mer=0
for q in (1,-1):
    for chi in itertools.product((1,-1),repeat=3):
        for (i,j) in ((2,3),(3,1),(1,2)):
            b=E(i,q)*E(j,q)
            m=b if chi[0]==1 else -b
            assert (m*m)==cl_scal(-1,q); mer+=1
ok(f"S8 meridian regression in both algebras: {mer}/48 give -1", mer==48)

print("="*78); print("PART 2 — Q~(+/-) (768), full Hom enumeration, B2"); print("="*78)
def fm2(x): return x-2*math.floor(x/2)
def tm2(t): return tuple(fm2(x) for x in t)

def qt_build(q):
    e1_,e2_,e3_=E(1,q),E(2,q),E(3,q)
    biv={1:e2_*e3_, 2:e3_*e1_, 3:e1_*e2_}
    half=cl_scal(F(1,2),q)
    C3T=((0,0,1),(1,0,0),(0,1,0)); G4T=((1,0,0),(0,0,-1),(0,1,0))
    c3q=None
    for s in (1,-1):
        cand=half + (biv[1]*half if s==1 else -(biv[1]*half)) \
                  + (biv[2]*half if s==1 else -(biv[2]*half)) \
                  + (biv[3]*half if s==1 else -(biv[3]*half))
        if rho_matrix(cand,q)==C3T: c3q=cand; break
    assert c3q is not None, "no c3 lift covers the 3-cycle"
    s2h=Cl({frozenset():R2(0,F(1,2))},q)
    g4q=None
    for s in (1,-1):
        cand=s2h + (biv[1]*s2h if s==1 else -(biv[1]*s2h))
        if rho_matrix(cand,q)==G4T: g4q=cand; break
    assert g4q is not None, "no g4 lift covers R4x"
    uq  = Cl({frozenset([2]):R2(0,F(1,2)), frozenset([3]):-R2(0,F(1,2))},q)
    om  = e1_*e2_*e3_
    assert rho_matrix(biv[1],q)==A1 and rho_matrix(biv[2],q)==A2 and rho_matrix(biv[3],q)==A3
    assert rho_matrix(om,q)==tuple(tuple(-1 if i==j else 0 for j in range(3)) for i in range(3))
    assert rho_matrix(uq,q)==MIRROR23
    gens={
        "r1":(biv[1],tm2((F(0),F(0),F(1)))),
        "r2":(biv[2],tm2((F(1),F(0),F(0)))),
        "r3":(biv[3],tm2((F(0),F(1),F(0)))),
        "E1":(cl_scal(1,q),(F(1),F(0),F(0))),
        "c3":(c3q,(F(0),)*3),
        "g4":(g4q,(F(1,2),F(1,2),F(1,2))),
        "om":(om,(F(0),)*3),
    }
    cache={}
    def rho_of(x):
        if x not in cache: cache[x]=rho_matrix(x,q)
        return cache[x]
    def mul(a,b): return (a[0]*b[0], tm2(vadd(a[1], mv(rho_of(a[0]),b[1]))))
    ID=(cl_scal(1,q),(F(0),)*3); Z=(cl_scal(-1,q),(F(0),)*3)
    grp={ID}; front=[ID]
    while front:
        x=front.pop()
        for g in gens.values():
            y=mul(x,g)
            if y not in grp: grp.add(y); front.append(y)
    return gens,grp,mul,ID,Z

results={}
for q in (1,-1):
    lab="Pin+" if q==1 else "Pin-"
    gens,grp,mul,ID,Z=qt_build(q)
    ok(f"[{lab}] |Q~| = 768", len(grp)==768)
    ok(f"[{lab}] z central (vs generators)", all(mul(Z,g)==mul(g,Z) for g in gens.values()))
    def keyfirst(x):
        for k in sorted(x.c, key=lambda s:(len(s),sorted(s))):
            sg=x.c[k].sign()
            if sg!=0: return sg
        return 0
    def norm(el):
        s=keyfirst(el[0])
        return ((el[0] if s>0 else -el[0]), el[1])
    Q={norm(x) for x in grp}
    ok(f"[{lab}] |Q| = 384", len(Q)==384)
    def qmul(a,b): return norm(mul(a,b))
    gQ={n:norm(g) for n,g in gens.items()}
    QID=norm(ID)
    homs=[]
    for assign in itertools.product((1,-1),repeat=7):
        s=dict(zip(gens.keys(),assign))
        lb={QID:1}; front=[QID]; okc=True
        while front and okc:
            x=front.pop()
            for n in gens:
                y=qmul(x,gQ[n]); v=lb[x]*s[n]
                if y in lb:
                    if lb[y]!=v: okc=False; break
                else: lb[y]=v; front.append(y)
        if okc and len(lb)==384: homs.append((s,lb))
    print(f"   [{lab}] |Hom(Q,F2)| = {len(homs)}  (full 768-model relation audit)")
    T111=norm((cl_scal(1,q),(F(1),F(1),F(1))))
    E2q=norm((cl_scal(1,q),(F(0),F(1),F(0)))); E3q=norm((cl_scal(1,q),(F(0),F(0),F(1))))
    ok(f"[{lab}] B2 DECISIVE: no character with chi(t111) = -1 — the S8 boundary bit "
       f"is CONSUMED (forced +1)", all(lb[T111]==1 for _,lb in homs))
    ok(f"[{lab}] all characters trivial on Gamma and turn-overs ([r_f]=[e_f]=[t111]=0)",
       all(s['r1']==s['r2']==s['r3']==1 and lb[gQ['E1']]==lb[E2q]==lb[E3q]==1
           for s,lb in homs))
    ok(f"[{lab}] |Hom| = 4  (= d x sgn residual)", len(homs)==4)
    dv=sorted(set((lb[gQ['om']],s['g4']) for s,lb in homs))
    note(f"[{lab}] residual character values (w on -I class, w on g4): {dv}")
    hlift=(Cl({frozenset([2]):R2(0,F(1,2)),frozenset([3]):-R2(0,F(1,2))},q),
           (F(1,2),F(1,2),F(1,2)))
    ok(f"[{lab}] h-lift lies in Q~ (closure membership)",
       hlift in grp or ((-hlift[0]),hlift[1]) in grp)
    hsq=mul(hlift,hlift)
    ok(f"[{lab}] h-lift squared = (q, (1,1,1)) elementwise",
       hsq[0]==cl_scal(q,q) and tuple(hsq[1])==(F(1),F(1),F(1)))
    note(f"[{lab}] B2 mechanism isolated: w(h)^2 = +1 = w(h^2) = w(t111).")
    glift=(Cl({frozenset([1]):R1_},q),(F(0),F(0),F(1)))
    gsq=mul(glift,glift); osq=mul(gens["om"],gens["om"])
    def ev(sq):
        assert sq[0].is_scalar()
        return 1 if sq[0].scalar()==R2(1) else -1
    results[q]=dict(glide=ev(gsq), minusI=ev(osq), h=ev(hsq))
    print(f"   [{lab}] amphichiral-square, evaluated on the surviving structures: "
          f"glide {results[q]['glide']:+d}   (-I) {results[q]['minusI']:+d}   h {results[q]['h']:+d}")

print("="*78); print("PART 3 — B1 invariance analysis (decisive, re-posed)"); print("="*78)
ok("representative-DEPENDENCE within each Pin type (glide vs -I opposite)",
   all(results[q]['glide']==-results[q]['minusI'] for q in (1,-1)))
ok("comparative fork ACROSS types: every representative evaluates oppositely in "
   "Pin+ vs Pin- (the invariant Pin-DISTINGUISHING statement)",
   all(results[1][k]==-results[-1][k] for k in ('glide','minusI','h')))
note("Absolute amphichiral-square sign = deck-representative GAUGE (glide = r1 o (-I);")
note("lift-squares differ by z x t~). Invariant content: (i) opposite across Pin types")
note("per fixed representative; (ii) structure-independent (surviving characters are")
note("trivial on Gamma and turn-overs). PRE-REGISTRATION CORRECTION recorded: B1's")
note("'square of the pinned representative' framing presupposed a class invariant")
note("that does not exist; corrected in execution by canon's own machinery.")

print("="*78); print("SUMMARY"); print("="*78)
print(f"total assertions passed: {PASS}")
print("""
Dictionary [R1]: -I IS (id;(+,+,+);-1); glide = r1 o (-I), same class. CC's
  contrast line FALSE (gamma-correction miss); chat pre-reg sketch FALSIFIED.
H-A [R1]: both Pin types populated; |Hom| = 4 each at the full 768 model
  (CC's flagged depth gap closed).
B2  [R1]: FORCED both types; mechanism = h with h^2 = t_(1,1,1). The S8
  boundary bit chi(t111) is CONSUMED by the improper sector. Confirms CC.
B1  [R1, re-posed]: absolute sign = deck gauge; INVARIANT = per-representative
  opposite evaluation across Pin types, structure-independent. Fork real and
  binary in the comparative sense; CC's headline survives, CC's absolute
  assignment and dictionary justification do not.
VERDICT: OPEN-FORK (refined) — chi(t111) consumed; the Pin type is the new
  located Z/2 import, comparatively distinguished by the amphichiral square.
  No Section 2.50 closure; ontology quarantine intact; Open 3 untouched.
""")
with open(__file__,"rb") as fh:
    print("self md5:", hashlib.md5(fh.read()).hexdigest())
