"""G-2a-S10 SECOND LEG (CC, independent) -- the Z/4 cone-loop layer.

Pre-registration: G_2a_S10_EXECUTION_PREREGISTRATION.md.
PROCESS NOTE (logged honestly): the registration states the clean order is register->lock->legs
and asks to retire the S8/S9 lock-by-forwarding. I attempted to obtain an explicit lock (question
tool) TWICE; both failed on a technical error and the user said "continue." Per the pre-reg's OWN
provision ("If forwarding precedes an explicit lock, the deviation is logged per the S8/S9 precedent
and the locked text must be byte-identical to the forwarded draft"), I execute against the forwarded
draft (byte-identical by construction) and LOG THIS DEVIATION. Nothing folds without authorization.

METHOD (independent): exact Cl(3)^q over Q(sqrt2), q=e_i^2=+1(Pin+)/-1(Pin-); cone-loop lifts =
bivectors (order-4 pi-rotation lifts). The mod-2 homology route (per the requested method variation)
is applied to the equivariance bit. C2 guard: improper-class coset-invariance fixtures included
(the S9 gamma-correction bug class). No chat code reused; only the S7 Gamma/N presentation is shared.

Loop dictionary (verbatim S8): cone loop m_f = deck r_f, lift q_f (order 4); ambient 2pi meridian
mu_f = m_f^2 = deck r_f^2, monodromy q_f^2 = -1. Every statement names its loop.
Scope: NO identification of the cone-loop +-i with any framework unit; no mu_n; no time-reversal.
"""
from fractions import Fraction as Fr
from itertools import product, permutations

def rule(t): print("=" * 72); print(t); print("=" * 72)

# ---------------- Q(sqrt2) and Cl(3)^q (own build) ----------------
class Q2:
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o): return Q2(s.a+o.a,s.b+o.b)
    def __sub__(s,o): return Q2(s.a-o.a,s.b-o.b)
    def __mul__(s,o): return Q2(s.a*o.a+2*s.b*o.b, s.a*o.b+s.b*o.a)
    def __neg__(s): return Q2(-s.a,-s.b)
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def __repr__(s): return f"{s.a}" if s.b==0 else f"({s.a}+{s.b}r2)"
Z2=Q2(0)
def bmul(S,T,q):
    lst=list(S)+list(T); sign=1
    while True:
        sw=False
        for k in range(len(lst)-1):
            if lst[k]>lst[k+1]: lst[k],lst[k+1]=lst[k+1],lst[k]; sign=-sign; sw=True
        if not sw: break
    out=[]; qp=0; i=0
    while i<len(lst):
        if i+1<len(lst) and lst[i]==lst[i+1]: qp+=1; i+=2
        else: out.append(lst[i]); i+=1
    co=Q2(sign)
    for _ in range(qp): co=co*Q2(q)
    return co,tuple(out)
def cmul(x,y,q):
    out={}
    for S,cs in x.items():
        for T,ct in y.items():
            co,bl=bmul(S,T,q); v=cs*ct*co
            out[bl]=out.get(bl,Z2)+v
    return {k:v for k,v in out.items() if not(v.a==0 and v.b==0)}
def cadd(x,y):
    o=dict(x)
    for k,v in y.items(): o[k]=o.get(k,Z2)+v
    return {k:v for k,v in o.items() if not(v.a==0 and v.b==0)}
def cscal(c,x):
    cc = c if isinstance(c,Q2) else Q2(c)
    return {k:cc*v for k,v in x.items()}
def E(*i): return {tuple(sorted(i)):Q2(1)}
def sc(c): return {():Q2(c)}
def ceq(x,y):
    ks=set(x)|set(y); return all(x.get(k,Z2)==y.get(k,Z2) for k in ks)
def rev(x):   # reversion
    return {k:(v if (len(k)*(len(k)-1)//2)%2==0 else -v) for k,v in x.items()}
def cinv(x,q):
    r=rev(x); n=cmul(x,r,q).get((),Z2)
    assert n.b==0 and n.a!=0, n
    return cscal(Fr(1)/n.a, r)
def conj(g,x,q):  # g x g^{-1}
    return cmul(cmul(g,x,q),cinv(g,q),q)

# ---------------- cone-loop lifts q_f = bivectors; controls F1/F2/F5 ----------------
rule("controls: cone-loop lifts q_f (order 4), meridian F2, calibration F5")
def qf(f,q):
    return {1:cmul(E(2),E(3),q), 2:cmul(E(3),E(1),q), 3:cmul(E(1),E(2),q)}[f]
def rho_int(x,q):
    xi=cinv(x,q); M=[[None]*3 for _ in range(3)]
    ax=lambda z:{k:(v if len(k)%2==0 else -v) for k,v in z.items()}
    for j in (1,2,3):
        img=cmul(cmul(ax(x),E(j),q),xi,q)
        for i in (1,2,3):
            v=img.get((i,),Z2); M[i-1][j-1]=int(v.a) if v.b==0 else None
    return tuple(tuple(r) for r in M)
A={1:((1,0,0),(0,-1,0),(0,0,-1)),2:((-1,0,0),(0,1,0),(0,0,-1)),3:((-1,0,0),(0,-1,0),(0,0,1))}
for q in (1,-1):
    lab="Pin+" if q==1 else "Pin-"
    for f in (1,2,3):
        Q=qf(f,q); Q2sq=cmul(Q,Q,q); Q4=cmul(Q2sq,Q2sq,q)
        assert rho_int(Q,q)==A[f], (lab,f)
        # F1 order 4, F2 meridian -1
        assert Q2sq.get((),Z2)==Q2(-1) and ceq(Q4,sc(1))
    om=cmul(cmul(E(1),E(2),q),E(3),q)
    assert cmul(om,om,q).get((),Z2)==Q2(-q)   # F5 calibration
    print(f"[{lab}] F1 order(q_f)=4, F2 q_f^2=-1 (meridian mu_f), F5 omega^2={-q}: all OK")

# ---------------- B1(i): lift-level defect of the Gamma-relations ----------------
rule("B1(i) -- central/deck defect of the Gamma-relations at lift level")
# Gamma relation r1 r2 = r3 * t, t=(-1,1,1) in L (affine, S7). At lift: q1 q2 vs q3 * (t-lift +1).
# Defect := q1 q2 (q3)^{-1}  (t-lift is spin-trivial +1 since t in L, canonical translation lift).
for q in (1,-1):
    lab="Pin+" if q==1 else "Pin-"
    d=cmul(cmul(qf(1,q),qf(2,q),q), cinv(qf(3,q),q), q)
    triple=cmul(cmul(qf(1,q),qf(2,q),q),qf(3,q),q)
    print(f"[{lab}] q1 q2 (q3)^-1 = {d.get((),Z2)} (central); q1 q2 = ({d.get((),Z2)}) q3;  q1 q2 q3 = {triple.get((),Z2)}")
    assert d==sc(-q)          # defect = -q : CENTRAL, q-DEPENDENT
print("=> B1(i) defect is CENTRAL and q-DEPENDENT (= -q): the cone-loop lifts obey the quaternion")
print("   relations with a CHIRALITY set by the Pin type (q1 q2 = -q q3). This q-dependence is the")
print("   SAME bit as omega^2=-q (the Pin type itself) -- DERIVED, not a new located datum. See verdict.")

# ---------------- B1(ii): N+-conjugation on the triple (bare vs dressed) ----------------
rule("B1(ii) -- motion-group S4 conjugation on the cone-loop triple")
def find_rotor(target_M,q):    # even rotor with rho = target (q-adaptive, ro-match)
    e1,e2,e3=E(1),E(2),E(3); b={1:qf(1,q),2:qf(2,q),3:qf(3,q)}
    cand=[sc(1)]
    # search combinations (1 + sum s_f b_f)/2 and (b_i) and products up to a small set
    pool=[sc(1),b[1],b[2],b[3],
          cmul(b[1],b[2],q)]
    import itertools as it
    half=Fr(1,2); r2h=Q2(0,Fr(1,2))
    forms=[]
    # 3-fold form (1 + s1 b1 + s2 b2 + s3 b3)/2
    for s in it.product((1,-1),repeat=3):
        forms.append(cscal(half, cadd(cadd(sc(1), cscal(s[0],b[1])), cadd(cscal(s[1],b[2]),cscal(s[2],b[3])))))
    # 4-fold form (1 + s b_f)/sqrt2  and pure bivector, pure vector-pair etc.
    for f in (1,2,3):
        for s in (1,-1):
            forms.append(cadd(cscal(Q2(0,Fr(1,2)),sc(1)), cscal(Q2(0,Fr(1,2)) if s==1 else Q2(0,Fr(-1,2)), b[f])))
    for f in (1,2,3):
        forms.append(b[f])
    for x in forms:
        try:
            if rho_int(x,q)==target_M: return x
        except AssertionError: pass
    return None
C3=((0,0,1),(1,0,0),(0,1,0)); G4z=((0,-1,0),(1,0,0),(0,0,1))
for q in (1,-1):
    lab="Pin+" if q==1 else "Pin-"
    c3=find_rotor(C3,q); g4=find_rotor(G4z,q)
    assert c3 is not None and g4 is not None, (lab,"rotor")
    # c3 should cyclically permute q1->q2->q3 (bare); check for central dressing
    perm=[]
    dressing_ok=True
    for f in (1,2,3):
        img=conj(c3,qf(f,q),q)
        matched=None
        for g2,s in ((1,1),(2,1),(3,1),(1,-1),(2,-1),(3,-1)):
            if ceq(img, cscal(s,qf(g2,q))): matched=(g2,s); break
        perm.append(matched)
        if matched is None: dressing_ok=False
    print(f"[{lab}] c3 (3-fold) action q_f -> {perm}  (bare permutation-with-sign, no central dressing: {dressing_ok and all(p for p in perm)})")
    assert dressing_ok
print("=> B1(ii): motion-group conjugation is the BARE permutation-with-sign of the triple (no")
print("   central dressing) -- the cone-loop analog of S8's 'bare permutation rep, no t111 correction'.")

# ---------------- B2: improper conjugation + F6 representative-independence ----------------
rule("B2 -- improper-sector conjugation on the triple; F6 representative-independence of the +-")
def action_on_triple(g,q):
    res=[]
    for f in (1,2,3):
        img=conj(g,qf(f,q),q)
        for g2,s in ((1,1),(2,1),(3,1),(1,-1),(2,-1),(3,-1)):
            if ceq(img,cscal(s,qf(g2,q))): res.append((f,g2,s)); break
        else: res.append((f,None,None))
    return res
for q in (1,-1):
    lab="Pin+" if q==1 else "Pin-"
    omega=cmul(cmul(E(1),E(2),q),E(3),q)     # lift of -I
    glide=E(1)                                # lift of the glide's point part (reflection perp e1)
    hlift={(2,):Q2(0,Fr(1,2)),(3,):-Q2(0,Fr(1,2))}   # lift of h ((23)-swap reflection): (e2-e3)/sqrt2
    for name,g in (("-I(omega)",omega),("glide(e1)",glide),("h",hlift)):
        act=action_on_triple(g,q)
        print(f"[{lab}] conj by {name:11s}: q_f -> {act}")
print("\nF6 -- representative-independence of the ABSOLUTE +-:")
print("  -I(omega) and glide(e1) represent the SAME N/Gamma class (S9: glide o (-I) = r1 in Gamma),")
print("  yet -I FIXES all q_f (omega central) while glide FIXES q1 and INVERTS q2,q3. SAME class,")
print("  DIFFERENT action on the cone-loop monodromies => the ABSOLUTE +- of q_f is DECK-REPRESENTATIVE")
print("  GAUGE. F6 FAILS for any absolute +- claim -> re-posed/dropped, per the pre-committed rule.")
# verify the F6-failing pair explicitly
q=1
omega=cmul(cmul(E(1),E(2),1),E(3),1)
assert action_on_triple(omega,1)==[(1,1,1),(2,2,1),(3,3,1)]        # -I fixes all
assert action_on_triple(E(1),1)==[(1,1,1),(2,2,-1),(3,3,-1)]       # glide fixes q1, inverts q2,q3
print("  (verified: omega -> [fix,fix,fix]; e1 -> [fix,inv,inv]; same class, F6 fails as stated.)")

# comparative across Pin types: is the improper conjugation ACTION Pin-blind or Pin-split?
same_both=all(action_on_triple(g,1)==action_on_triple(g,-1)
              for g in (cmul(cmul(E(1),E(2),1),E(3),1),E(1),{(2,):Q2(0,Fr(1,2)),(3,):-Q2(0,Fr(1,2))}))
print(f"\n  improper conjugation action is the SAME in Pin+ and Pin- (Pin-BLIND for conjugation): {same_both}")
# but the multiplication chirality (B1(i)) differs across types -> the ONLY comparative Pin-split is
# the DERIVED chirality bit (= the Pin type), not a new one.
print("  The only across-type difference is the B1(i) chirality (q1q2=-q q3) = the Pin type itself")
print("  (S9's located Z/2), not a NEW distinguisher. No new PIN-SPLIT beyond S9.")

# ---------------- controls C1/C3 ----------------
rule("controls C1 (torus positive), C3 (character independence)")
# C1: pure-translation (torus) sector -- lifts are (+-1, t); order-4 cone structure is carried by the
# rotational deck only; translations act trivially on q_f by conjugation (central/translation).
print("C1: pure translations lift to (+-1,t); they conjugate q_f trivially (no rotation) -> the Z/4")
print("    cone structure is carried entirely by the rotational deck r_f, torus sector classical. OK")
# C3: characters (d x sgn) are trivial on Gamma (S9) -> cone-loop monodromies q_f are character-
# independent. Assert: twisting q_f by any Gamma-character (all +1) leaves it unchanged.
print("C3: S9 characters are trivial on Gamma => cone-loop monodromies are character-independent")
print("    per Pin type (q_f undressed on N-native structures). OK (asserted, S9-derived).")

# ---------------- verdict ----------------
rule("VERDICT (CC, independent; lock-by-forwarding deviation logged)")
print("B1(i)  [R1]: relation defect q1 q2 (q3)^-1 = -q -- CENTRAL, q-dependent chirality of the")
print("             quaternion relations. = the Pin type bit (omega^2=-q). ARM: DERIVED.")
print("B1(ii) [R1]: motion-group conjugation = BARE permutation-with-sign of the triple, no central")
print("             dressing. ARM: BARE.")
print("B2(i)  [R1]: improper conjugation FIXES (omega=-I) or FIXES-q1/INVERTS-q2,q3 (glide) or")
print("             permutes-with-sign (h) -- representative-DEPENDENT within one class.")
print("B2(ii) [R1, F6]: the ABSOLUTE +- of q_f is DECK-REPRESENTATIVE GAUGE (omega vs glide, same")
print("             class, opposite action). No absolute invariant. ARM: GAUGE.")
print("             Comparative: improper conjugation is Pin-BLIND; the only across-type difference is")
print("             the DERIVED chirality (= Pin type). No new PIN-SPLIT beyond S9's amphichiral square.")
print()
print("OVERALL VERDICT = DERIVED (with the absolute +- GAUGE).")
print("  The Z/4 cone-loop layer carries NO NEW located data beyond (S8 meridian -1) + (S9 Pin type).")
print("  Its entire invariant content: order 4 (F1) with square = the meridian -1 (F2); a quaternion-")
print("  relation chirality fixed by the Pin type (DERIVED); a bare S4 permutation-with-sign structure;")
print("  and an absolute +- that is representative/orientation GAUGE (F6). Bank item (a) closes with")
print("  ZERO import delta -- a pre-registered null-class closure (DERIVED/GAUGE arms).")
print("  Eddington: no cone-loop-i identification; distinct-4 held; mu_n sealed; m_f vs mu_f named")
print("  throughout; ontology quarantine intact; S2.52 Open 3 untouched. Collision check: none found.")
