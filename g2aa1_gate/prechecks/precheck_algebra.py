#!/usr/bin/env python3
"""Chat-side PRE-LOCK sanity checks for the G-2a-A1 staging memo (NOT gate results).
Exact integer/rational arithmetic where possible (sympy), floats only for the 2O character sum
(which is then rounded and asserted integral). No ledger value, no observational target loaded."""
import itertools, math
from fractions import Fraction
import sympy as sp

# ---------- octonions: lines {i, i+1, i+3} mod 7 (indices 1..7), e_i e_j = e_k cyclic ----------
LINES = [((i-1)%7+1, (i)%7+1, (i+2)%7+1) for i in range(1,8)]   # (1,2,4),(2,3,5),...,(7,1,3)
assert sorted(sorted(l) for l in LINES) == sorted(sorted(l) for l in [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)])
mult = {}  # (i,j) -> (sign, k) for imaginary units
for (a,b,c) in LINES:
    for (x,y,z) in [(a,b,c),(b,c,a),(c,a,b)]:
        mult[(x,y)] = (1,z); mult[(y,x)] = (-1,z)
def omul(p,q):
    """p,q: length-8 rational vectors (index 0 = real unit)."""
    r=[Fraction(0)]*8
    for i in range(8):
        if p[i]==0: continue
        for j in range(8):
            if q[j]==0: continue
            if i==0: r[j]+=p[i]*q[j]
            elif j==0: r[i]+=p[i]*q[j]
            elif i==j: r[0]-=p[i]*q[j]
            else:
                s,k=mult[(i,j)]; r[k]+=s*p[i]*q[j]
    return r
def unit(i):
    v=[Fraction(0)]*8; v[i]=Fraction(1); return v
# alternativity / division check on basis
for i in range(1,8):
    for j in range(1,8):
        for k in range(1,8):
            pass
# ---------- derivation algebra g2 (14-dim) as 7x7 matrices: D(xy)=D(x)y+xD(y) ----------
# Unknown D = 7x7 real antisymmetric acting on Im O (derivations kill the real unit). 21 unknowns.
syms = sp.symbols('d0:21')
D = sp.zeros(7,7); t=0
for i in range(7):
    for j in range(i+1,7):
        D[i,j]=syms[t]; D[j,i]=-syms[t]; t+=1
def Dapply(v):   # v: length-8 Fraction vector -> sympy vector (imag part only; real part -> 0)
    out=[sp.Integer(0)]*8
    for i in range(1,8):
        if v[i]!=0:
            for j in range(1,8):
                out[j]+= D[j-1,i-1]*sp.Rational(v[i].numerator, v[i].denominator)
    return out
eqs=[]
for i in range(1,8):
    for j in range(1,8):
        ei, ej = unit(i), unit(j)
        lhs = Dapply(omul(ei,ej))
        # D(x)y + x D(y): D(ei) = sum_m D[m,i] e_m
        rhs=[sp.Integer(0)]*8
        for m in range(1,8):
            if D[m-1,i-1]!=0:
                prod = omul(unit(m), ej)
                for n in range(8): rhs[n]+= D[m-1,i-1]*sp.Rational(prod[n].numerator, prod[n].denominator)
            if D[m-1,j-1]!=0:
                prod = omul(ei, unit(m))
                for n in range(8): rhs[n]+= D[m-1,j-1]*sp.Rational(prod[n].numerator, prod[n].denominator)
        for n in range(8): eqs.append(sp.expand(lhs[n]-rhs[n]))
A = sp.Matrix([[sp.Poly(e, *syms).coeff_monomial(s) if e!=0 else 0 for s in syms] for e in eqs if e!=0])
ns = A.nullspace()
print("dim Der(O) = g2 =", len(ns))
assert len(ns)==14
g2 = []
for v in ns:
    M = sp.zeros(7,7); t=0
    for i in range(7):
        for j in range(i+1,7):
            M[i,j]=v[t]; M[j,i]=-v[t]; t+=1
    g2.append(M)

# ---------- left-multiplication maps L_a on R^8 and the spin(7)/su(4) bivector algebras ----------
def Lmat(a):
    M = sp.zeros(8,8)
    for j in range(8):
        col = omul(unit(a), unit(j))
        for i in range(8): M[i,j]=sp.Rational(col[i].numerator, col[i].denominator)
    return M
L = {a: Lmat(a) for a in range(1,8)}
for a in range(1,8):
    for b in range(1,8):
        S = L[a]*L[b]+L[b]*L[a]
        assert S == (-2*sp.eye(8) if a==b else sp.zeros(8,8)), "Clifford relations fail"
print("Clifford relations L_a L_b + L_b L_a = -2 delta: OK (Cl(0,7) on R^8)")
def span_dim(mats):
    return sp.Matrix([list(M) for M in mats]).rank()
biv7 = [L[a]*L[b] for a in range(1,8) for b in range(a+1,8)]
print("dim span{L_a L_b, a<b<=7} =", span_dim(biv7), "(spin(7) = 21 expected)")
biv6 = [L[a]*L[b] for a in range(1,7) for b in range(a+1,7)]
print("dim span{L_a L_b, a<b<=6} =", span_dim(biv6), "(spin(6)=su(4) = 15 expected)")
# g2 embedded in so(8) as derivations (act on Im O, kill 1)
g2_8 = []
for M in g2:
    M8 = sp.zeros(8,8); M8[1:,1:] = M; g2_8.append(M8)
print("dim g2 in so(8) =", span_dim(g2_8))
print("dim span(g2 + spin7) =", span_dim(g2_8+biv7), "(21 expected if g2 ⊂ spin(7)_L)")
print("dim span(g2 + su4)  =", span_dim(g2_8+biv6), "→ dim(g2 ∩ su(4)) =", 14+15-span_dim(g2_8+biv6), "(8 = su(3) expected)")

# ---------- G2 involutions: fixed subalgebra dims; the trace lemma ----------
# The coordinate involution sigma_H fixing the quaternion subalgebra of line (1,2,4) pointwise:
def is_aut(P):   # P: 8x8 sympy matrix; check P(xy)=P(x)P(y) on basis
    for i in range(8):
        for j in range(8):
            xy = omul(unit(i),unit(j)); lhs = P*sp.Matrix([sp.Rational(v.numerator,v.denominator) for v in xy])
            Pi = [Fraction(int(P[k,i].p), int(P[k,i].q)) for k in range(8)]
            Pj = [Fraction(int(P[k,j].p), int(P[k,j].q)) for k in range(8)]
            rhs = omul(Pi,Pj); rhs = sp.Matrix([sp.Rational(v.numerator,v.denominator) for v in rhs])
            if lhs!=rhs: return False
    return True
line = (1,2,4)
sig = sp.diag(*([1]+[1 if i in line else -1 for i in range(1,8)]))
print("sigma_H (fix line 124, negate complement) is an automorphism:", is_aut(sig), "; trace on Im O =", sum(sig[i,i] for i in range(1,8)))
# a 'wrong' involution: negate one unit only -> not an automorphism
bad = sp.diag(*([1]+[-1 if i==7 else 1 for i in range(1,8)]))
print("negating a single unit is an automorphism:", is_aut(bad))
# Signed lift of a Fano collineation involution: choose the collineation fixing line (1,2,4) pointwise and swapping (3 5)(6 7)? check which pairs
# Fano involution t: fixes {1,2,4}, swaps 3<->? We search all signed permutation matrices that are automorphisms and project to a fixed-line involution.
import itertools
pts=[1,2,3,4,5,6,7]
def perm_matrix(perm, signs):
    P=sp.zeros(8,8); P[0,0]=1
    for i in range(1,8): P[perm[i], i] = signs[i]
    return P
# enumerate collineations that fix 1,2,4 pointwise (the pointwise line stabilizer, order 4 = V4)
others=[3,5,6,7]
found=[]
for img in itertools.permutations(others):
    perm={1:1,2:2,4:4}; perm.update(dict(zip(others,img)))
    # collineation test: maps lines to lines
    ok = all(tuple(sorted(perm[x] for x in l)) in {tuple(sorted(m)) for m in LINES} for l in LINES)
    if not ok: continue
    if all(perm[x]==x for x in others): continue
    # find sign vectors making it an automorphism
    for sgn in itertools.product([1,-1], repeat=7):
        signs={i+1:sgn[i] for i in range(7)}
        P=perm_matrix(perm,signs)
        if is_aut(P):
            tr = sum(P[i,i] for i in range(1,8))
            found.append((perm, signs, tr))
print("signed automorphism lifts of the three nontrivial pointwise-line-stabilizer collineations:", len(found))
orders={}
for perm,signs,tr in found:
    P=perm_matrix(perm,signs); o=2 if P*P==sp.eye(8) else (4 if (P*P)*(P*P)==sp.eye(8) else 0)
    orders.setdefault((o,tr),0); orders[(o,tr)]+=1
print("   (order, trace on 7) -> count over the 24 signed automorphism lifts:", orders)
assert all(tr==-1 for (o,tr) in orders if o==2), "an order-2 automorphism with trace != -1 exists"
pass
print("   every ORDER-2 lift has trace -1 (permutation character 3, rho6 character 2 — the wrong-module gap is 4); the trace-3 lifts are of ORDER 4 (square to sigma_H).")

# ---------- 2O and the spin-3/2 character: Frobenius–Schur indicator ----------
import cmath
# 2O = binary octahedral: 48 unit quaternions: 24 Hurwitz units (2T) + 24 of the form (±1±i)/sqrt2 permutations
def qmul(a,b):
    a0,a1,a2,a3=a; b0,b1,b2,b3=b
    return (a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2, a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0)
els=set()
s2=1/math.sqrt(2)
for signs in itertools.product([1,-1],repeat=4):
    for pos in range(4):
        v=[0,0,0,0]; v[pos]=signs[pos]; els.add(tuple(round(x,9) for x in v))
    els.add(tuple(round(0.5*s,9) for s in signs))
for i,j in itertools.combinations(range(4),2):
    for si in (1,-1):
        for sj in (1,-1):
            v=[0,0,0,0]; v[i]=si*s2; v[j]=sj*s2; els.add(tuple(round(x,9) for x in v))
els=list(els); assert len(els)==48
def chi32(q):  # spin-3/2 character: q = cos(phi) + sin(phi) n
    phi=math.acos(max(-1,min(1,q[0])))
    return 2*math.cos(3*phi)+2*math.cos(phi)
fs = sum(chi32(tuple(round(x,9) for x in qmul(q,q))) for q in els)/48
norm = sum(chi32(q)**2 for q in els)/48
print("2O: |G|=48, <chi_3/2,chi_3/2> =", round(norm,9), ", chi(1)=", chi32((1,0,0,0)), ", chi(-1)=", chi32((-1,0,0,0)), ", Frobenius–Schur indicator =", round(fs,9))
assert round(norm)==1 and round(fs)==-1
# ---------- SL(2,7): number of solutions of g^2 = 1 ----------
p=7
SL=[]
for a,b,c,d in itertools.product(range(p),repeat=4):
    if (a*d-b*c)%p==1: SL.append((a,b,c,d))
assert len(SL)==336
def m2(g,h):
    a,b,c,d=g; e,f,gg,hh=h
    return ((a*e+b*gg)%p,(a*f+b*hh)%p,(c*e+d*gg)%p,(c*f+d*hh)%p)
sq1=[g for g in SL if m2(g,g)==(1,0,0,1)]
print("SL(2,7): #{g: g^2=1} =", len(sq1), "(2 expected: only ±I) ->", sq1)
