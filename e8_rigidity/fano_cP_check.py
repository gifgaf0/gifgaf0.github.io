"""Fano c_P across the seven maximal orders of integral octonions; weight-24 eigenforms. Exploration, Oct 22 2026."""
import numpy as np, itertools, math
from sympy import symbols, sqrt, Matrix, simplify, nsimplify
# ---- octonions: coordinates [1, e0..e6]; Fano lines (i,i+1,i+3) mod 7, e_a e_b = e_c (g1pp/§3.4-SIGNPHI convention)
LINES=[(i%7,(i+1)%7,(i+3)%7) for i in range(7)]
T=np.zeros((8,8,8))
for a in range(8): T[0,a,a]=T[a,0,a]=1
for a in range(1,8): T[a,a,0]=-1
for (a,b,c) in LINES:
    for (x,y,z) in ((a,b,c),(b,c,a),(c,a,b)):
        T[x+1,y+1,z+1]=1; T[y+1,x+1,z+1]=-1
mul=lambda u,v: np.einsum('i,j,ijk->k',u,v,T)
rng=np.random.default_rng(0)
u,v,w=rng.normal(size=(3,8))
assert abs(np.linalg.norm(mul(u,v))-np.linalg.norm(u)*np.linalg.norm(v))<1e-9   # composition algebra
# ---- the 30 3-(8,4,1) designs on points 0..7 (0 = real unit, k+1 = e_k)
base=[frozenset({0}|{a+1 for a in L}) for L in LINES]; base+= [frozenset(range(8))-b for b in base]
designs=set()
for p in itertools.permutations(range(8)):
    designs.add(frozenset(frozenset(p[i] for i in b) for b in base))
designs=list(designs); print("3-(8,4,1) designs:",len(designs))
def units(D):
    U=[s*np.eye(8)[i] for i in range(8) for s in (1,-1)]
    for b in D:
        b=sorted(b)
        for sg in itertools.product((1,-1),repeat=4):
            x=np.zeros(8); x[b]=np.array(sg)/2; U.append(x)
    return np.array(U)
key=lambda x: tuple(np.round(2*x).astype(int))
orders=[]
for D in designs:
    U=units(D); S={key(x) for x in U}
    P=np.einsum('ai,bj,ijk->abk',U,U,T).reshape(-1,8)
    if all(key(x) in S for x in P): orders.append((D,U))
print("designs whose 240 units are closed under multiplication (maximal orders):",len(orders))
# ---- degree-8 Fano weighting: Q(x)=sum over planes H of |proj_H x|^8 ; c_P8 = sum_units Q - 240*<Q>_sphere
def Qsum(U,planes):
    return sum((np.sum(U[:,list(H)]**2,axis=1)**4).sum() for H in planes)
def sphere_mean(dimH,deg=4,d=8):  # E[(|proj|^2)^deg], |proj|^2 ~ Beta(dimH/2,(d-dimH)/2)
    a,b=dimH/2,(d-dimH)/2; return math.prod((a+i)/(a+b+i) for i in range(deg))
assoc=[[0]+[a+1 for a in L] for L in LINES]                      # span{1,e_a,e_b,e_c}, the 7 quaternion subalgebras
nonline=[[0]+[a+1 for a in t] for t in itertools.combinations(range(7),3) if tuple(sorted(t)) not in {tuple(sorted(L)) for L in LINES}]
imag=[[a+1 for a in L] for L in LINES]                            # span{e_a,e_b,e_c}
def cP(U,planes): return Qsum(U,planes)-240*len(planes)*sphere_mean(len(planes[0]))
print("\nc_P8 per order (Fano labelling fixed):")
print(" order | design blocks containing the real unit (as e-indices)        | assoc 4-planes | imag 3-planes | 28 non-line 4-planes (control, per plane x7)")
for D,U in orders:
    lines_in=sorted(tuple(sorted(i-1 for i in b if i)) for b in D if 0 in b)
    print(f"   {orders.index((D,U))}  | {lines_in} | {cP(U,assoc):+9.4f} | {cP(U,imag):+9.4f} | {7*cP(U,nonline)/28:+9.4f}")
# ---- shell-2 check of the full statement for one order: sum Q = c0*n^4*240*sigma3(n) + tau(n)*c_P8
D,U=orders[0]
S2={key(x+y) for x in U for y in U if abs(np.dot(x+y,x+y)-2)<1e-9}; V2=np.array([np.array(k)/2 for k in S2])
lhs=Qsum(V2,assoc); c0=7*sphere_mean(4); pred=c0*2**4*240*9 + (-24)*cP(U,assoc)
print(f"\nshell n=2: {len(V2)} vectors (expect 2160); sum Q = {lhs:.6f}, predicted c0*16*240*9 + tau(2)*c_P8 = {pred:.6f}")
# ---- weight-24 Hecke eigenforms in basis {Delta*E4^3, Delta^2}
N=8
D_=[0]*(N+1); D_[0]=1
for m in range(1,N+1):
    for _ in range(24):
        for i in range(N,m-1,-1): D_[i]-=D_[i-m]
Delta=[0]+D_[:N]
E4=[1]+[240*sum(d**3 for d in range(1,m+1) if m%d==0) for m in range(1,N+1)]
def mult(a,b): return [sum(a[i]*b[n-i] for i in range(n+1)) for n in range(N+1)]
f1=mult(Delta,mult(E4,mult(E4,E4))); f2=mult(Delta,Delta)
print("\nf1=Delta*E4^3:",f1[1:5]," f2=Delta^2:",f2[1:5])
# T2 on weight 24: (T2 f)_n = a_{2n} + 2^23 a_{n/2}; express in basis by coefficients n=1,2
def T2(f): return [0]+[f[2*n]+(2**23*f[n//2] if n%2==0 else 0) for n in range(1,N//2+1)]
B=Matrix([[f1[1],f2[1]],[f1[2],f2[2]]])
M=B.inv()*Matrix([[T2(f1)[1],T2(f2)[1]],[T2(f1)[2],T2(f2)[2]]])
for ev,mult_,vecs in M.eigenvects():
    vv=vecs[0]; vv=vv/(vv[0]*f1[1]+vv[1]*f2[1])
    print(f"eigenvalue a(2) = {simplify(ev)}   eigenform = ({simplify(vv[0])})*Delta*E4^3 + ({simplify(vv[1])})*Delta^2")
# ---- which automorphisms permute the seven orders? (sign changes; index maps k -> a*k+b, a in {1,2,4}, with signs)
key_set=lambda U: frozenset(key(x) for x in U)
sets=[key_set(U) for _,U in orders]
def is_aut(M): return all(np.allclose(mul(M[:,i],M[:,j]), M@mul(np.eye(8)[i],np.eye(8)[j])) for i in range(8) for j in range(8))
signs=[np.diag((1,)+s) for s in itertools.product((1,-1),repeat=7) if is_aut(np.diag((1,)+s))]
line_auts=[]
for a in (1,2,4):
    for b in range(7):
        for s in itertools.product((1,-1),repeat=7):
            M=np.zeros((8,8)); M[0,0]=1
            for k in range(7): M[(a*k+b)%7+1,k+1]=s[k]
            if is_aut(M): line_auts.append(M); break
reach=lambda G: sorted({sets.index(key_set(orders[0][1]@M.T)) for M in G if key_set(orders[0][1]@M.T) in sets})
print(f"\nsign-change automorphisms: {len(signs)}; orders reached from order 0: {reach(signs)}")
print(f"line-preserving index automorphisms (k -> ak+b with signs): {len(line_auts)}; orders reached from order 0: {reach(line_auts)}")
