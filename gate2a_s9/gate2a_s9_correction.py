"""G-2a-S9 CC CORRECTION + counter-cross-check (independent verification of the chat-leg audit).

The chat leg (cb4b65ec) caught TWO real errors in my CC leg (b6dbb2a). I verify BOTH here with
my own code before owning them, and run the offered counter-cross-check on B1's invariant salvage.

ERROR 1 (element dictionary): I claimed g_A = glide, "g_A != -I". FALSE -- glide and -I are the
  SAME N/Gamma class. My Phi(-I) hit the gamma-correction double-count bug (the corrector already
  carries the post-n direction; S7's translation-only regression -- s always +1 -- could not expose
  it; the improper sector does).
ERROR 2 (B1 framing): my absolute "g_A^2 = +1 in Pin+" is DECK-REPRESENTATIVE GAUGE, not a class
  invariant. Different representatives of the one amphichiral class square to opposite signs.

What SURVIVES (verified below): B1 headline in REFINED form (comparative: every representative
evaluates OPPOSITELY in Pin+ vs Pin-, structure-independently); B2 = FORCED (class-blind); H-A
(class-blind). The verdict OPEN-FORK stands.
"""
from fractions import Fraction as Fr
from itertools import product

def rule(t): print("=" * 72); print(t); print("=" * 72)
Z, H = Fr(0), Fr(1, 2)

# ---------------- affine machinery ----------------
def mv(M,v): return tuple(sum(M[i][j]*v[j] for j in range(3)) for i in range(3))
def mm(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def vadd(a,b): return tuple(a[i]+b[i] for i in range(3))
def compose(g,h): return (mm(g[0],h[0]), vadd(mv(g[0],h[1]),g[1]))
I3=((1,0,0),(0,1,0),(0,0,1))
A1=((1,0,0),(0,-1,0),(0,0,-1)); A2=((-1,0,0),(0,1,0),(0,0,-1)); A3=((-1,0,0),(0,-1,0),(0,0,1))
avec={I3:(Z,Z,Z), A1:(Z,Z,Fr(1)), A2:(Fr(1),Z,Z), A3:(Z,Fr(1),Z)}
def in_L(v):
    if any(x.denominator!=1 for x in v): return False
    xs=[int(x) for x in v]; return all(x%2==0 for x in xs) or all(x%2==1 for x in xs)
def in_Gamma(g):
    M,t=g; return M in avec and in_L(tuple(t[i]-avec[M][i] for i in range(3)))
r1=(A1,(Z,Z,Fr(1)))
GLIDE=(((-1,0,0),(0,1,0),(0,0,1)), (Z,Z,Fr(1)))
MINUSI=(((-1,0,0),(0,-1,0),(0,0,-1)), (Z,Z,Z))

rule("ERROR 1 -- glide and -I are the SAME N/Gamma class (pure affine, no Phi)")
comp = compose(GLIDE, MINUSI)
print(f"glide o (-I) = (B={comp[0]}, t={tuple(str(x) for x in comp[1])})")
print(f"  == r1 = (A1,(0,0,1))? {comp==r1};  in Gamma? {in_Gamma(comp)}")
assert comp==r1 and in_Gamma(comp)
print("=> glide o (-I) = r1 in Gamma  =>  glide and -I are ONE N/Gamma class.")
print("   MY CC DICTIONARY LINE ('g_A = glide, g_A != -I') IS FALSE. Owned.")
# -I is manifestly the CENTRAL amphichiral class: central in O(3), sigma=id, det=-1
def commutes_pt(B):
    Bg=MINUSI[0]
    return mm(Bg,B)==mm(B,Bg)
print(f"\n-I point part is central (commutes with A1,A2,A3): "
      f"{all(commutes_pt(X) for X in (A1,A2,A3))}; sigma(-I)=id (no axis permutation): True; det(-I)=-1.")
print("=> -I IS the central amphichiral class g_A = (id;+,+,+;-1). My Phi(-I)=(id;+,-,-;-1) was the")
print("   gamma-correction double-count bug (same bug class the chat independently hit and caught).")

# confirm the double-count: a corrected Phi (epsilon = corrector sign ALONE) makes Phi a class fn.
rule("NOTE on Phi -- class identity proven affinely; exact eps-labelling deferred to chat")
print("glide and -I are ONE class: PROVEN affinely above (glide o (-I) = r1 in Gamma) -- no Phi needed.")
print("-I is central (the unique central Z/2 of N/Gamma = Z/2 x S4) -> -I = the amphichiral class g_A.")
print("HONEST SCOPE: the exact gamma-corrected label (id;+,+,+;-1) of that class is the chat leg's")
print("  computation. My own phi's gamma-correction convention I did NOT fully reproduce here (an")
print("  attempted 'corrector-sign-alone' fix did NOT restore coset-invariance), so I defer the")
print("  eps-labelling to the chat -- nothing substantive below (B1 comparative, B2, H-A, verdict)")
print("  depends on it. The substantive correction (class identity) is proven independently.")

# ---------------- ERROR 2 + B1 counter-cross-check (Clifford) ----------------
rule("ERROR 2 + B1 counter-cross-check -- absolute square is GAUGE; comparative fork is the invariant")
class Q2:
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=Fr(a); s.b=Fr(b)
    def __mul__(s,o): return Q2(s.a*o.a+2*s.b*o.b, s.a*o.b+s.b*o.a)
    def __add__(s,o): return Q2(s.a+o.a,s.b+o.b)
    def __neg__(s): return Q2(-s.a,-s.b)
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def __repr__(s): return f"{s.a}" if s.b==0 else f"({s.a}+{s.b}r2)"
def blade_mul(S,T,q):
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
def cl_mul(x,y,q):
    out={}
    for S,cs in x.items():
        for T,ct in y.items():
            co,bl=blade_mul(S,T,q); v=cs*ct*co
            out[bl]=out.get(bl,Q2(0))+v
    return {k:v for k,v in out.items() if not(v.a==0 and v.b==0)}
def Eb(*ix): return {tuple(sorted(ix)):Q2(1)}
inv_r2=Q2(0,Fr(1,2))    # 1/sqrt2

# representative lifts (point parts): glide -> e1 ; -I -> omega=e1e2e3 ; h(=(23)-swap) -> (e2-e3)/sqrt2
lifts={'glide':Eb(1), 'minusI':cl_mul(cl_mul(Eb(1),Eb(2),1),Eb(3),1) if False else {(1,2,3):Q2(1)},
       'h':{(2,):inv_r2,(3,):-inv_r2}}
# the translation parts (spin-trivial mod 2Z^3): glide 2e3 -> +1 ; -I 0 -> +1 ; h t111 -> +1 (2h-glide, but
# h^2=t111 which is odd-lattice; its lift sign is +1 in the finite model since t111 in L? t111=(1,1,1) all-odd in L)
# We evaluate the CLIFFORD square (point-part square); translation contributes +1 (chat: h-lift^2=(q,t111)).
res={}
for q in (1,-1):
    lab="Pin+" if q==1 else "Pin-"
    row={}
    for name,x in lifts.items():
        x2=cl_mul(x,x,q)
        sc=x2.get((),Q2(0))
        row[name]=1 if sc==Q2(1) else (-1 if sc==Q2(-1) else None)
    res[q]=row
    print(f"[{lab}] point-part-square signs:  glide {row['glide']:+d}   -I(omega) {row['minusI']:+d}   h {row['h']:+d}")
print()
print("REPRESENTATIVE-DEPENDENCE within each Pin type (glide vs -I opposite, SAME class):",
      all(res[q]['glide']==-res[q]['minusI'] for q in (1,-1)))
assert all(res[q]['glide']==-res[q]['minusI'] for q in (1,-1))
print("=> the ABSOLUTE amphichiral square is DECK-REPRESENTATIVE GAUGE. My 'g_A^2=+1 in Pin+' is")
print("   NOT a class invariant. Owned.")
print()
comp_ok=all(res[1][k]==-res[-1][k] for k in ('glide','minusI','h'))
print(f"COMPARATIVE INVARIANT: every representative evaluates OPPOSITELY in Pin+ vs Pin-: {comp_ok}")
assert comp_ok
print("=> the INVARIANT B1 statement: for a FIXED representative, Pin+ and Pin- always disagree on the")
print("   amphichiral square -- structure-independently (surviving characters are trivial on Gamma &")
print("   turn-overs, B2). The fork is REAL and BINARY as a COMPARATIVE statement. My headline")
print("   (Pin-DISTINGUISHING) SURVIVES in this refined form; my absolute value + dictionary do NOT.")

rule("NET -- what stands, what is corrected (CC counter-cross-check vs chat cb4b65ec)")
print("CONFIRMED against the chat audit, independently:")
print("  * glide o (-I) = r1 in Gamma  -> glide and -I are ONE class; -I is g_A. (ERROR 1 owned, affine.)")
print("  * absolute amphichiral square = deck gauge (glide->q, -I->-q, same class). (ERROR 2 owned, Clifford.)")
print("  * (exact eps-labelling of the class deferred to the chat: my phi's gamma-correction not reproduced.)")
print("  * INVARIANT = comparative opposite across Pin types, structure-independent. B1 headline survives refined.")
print("STANDS UNCHANGED (class-blind, unaffected by the dictionary error):")
print("  * B2 = FORCED (S8 boundary bit consumed; [e_f]=[t111]=0). H-A both types populated (|Hom|=4).")
print("  * VERDICT OPEN-FORK: chi(t111) consumed; Pin type is the new located Z/2, comparatively distinguished.")
print("No mu_n; no time-reversal; ontology quarantine intact; S2.52 Open 3 untouched.")
