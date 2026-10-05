# Verify: (1) dim of SU(3)-invariant cubic (holomorphic) polynomials on the symmetric 6 (Phi -> U Phi U^T) is 1;
# (2) det is invariant; (3) center element w*1 acts on 6 as w^2; (4) degree-1,2 invariants vanish.
import itertools, numpy as np, sympy as sp
# basis of symmetric 3x3: E_ij, i<=j
pairs=[(i,j) for i in range(3) for j in range(i,3)]
def Ebasis(i,j):
    M=np.zeros((3,3),complex); M[i,j]=1; M[j,i]=1
    return M
# su(3) generators (complexified gl(3) generators e_ab suffice for invariance under sl(3))
gens=[]
for a in range(3):
    for b in range(3):
        if a!=b:
            g=np.zeros((3,3),complex); g[a,b]=1; gens.append(g)
for a in range(2):
    g=np.zeros((3,3),complex); g[a,a]=1; g[a+1,a+1]=-1; gens.append(g)
# action on symmetric matrices: delta Phi = X Phi + Phi X^T ; coordinates x_p = Phi_{ij} for (i,j) in pairs
x=sp.symbols('x0:6')
def Phi_of(xv):
    P=sp.zeros(3,3)
    for k,(i,j) in enumerate(pairs):
        P[i,j]=xv[k]; P[j,i]=xv[k]
    return P
P=Phi_of(x)
def vec_field(X):
    Xs=sp.Matrix(X.real.astype(int))+sp.I*sp.Matrix(X.imag.astype(int))
    dP=Xs*P+P*Xs.T
    return [sp.expand(dP[i,j]) for (i,j) in pairs]
def invariants(deg):
    monos=[sp.Mul(*c) for c in itertools.combinations_with_replacement(x,deg)]
    cs=sp.symbols('c0:%d'%len(monos))
    poly=sum(c*m for c,m in zip(cs,monos))
    eqs=[]
    for X in gens:
        v=vec_field(X)
        dpoly=sp.expand(sum(sp.diff(poly,x[k])*v[k] for k in range(6)))
        eqs+= sp.Poly(dpoly,*x).coeffs()
    sol=sp.linsolve(eqs,cs)
    sol=list(sol)[0]
    free=set().union(*[s.free_symbols for s in sol]) & set(cs)
    return len(free), sp.factor(sp.expand(poly.subs(dict(zip(cs,sol))))) if free else 0
for d in (1,2,3):
    n,p=invariants(d)
    print("degree",d,": number of independent SL(3)-invariants =",n, "; invariant =",p)
print("det Phi =",sp.factor(P.det()))
w=sp.exp(2*sp.pi*sp.I/3)
U=w*sp.eye(3)
print("center action: U Phi U^T = w^2 Phi ?", sp.simplify(U*P*U.T - w**2*P)==sp.zeros(3,3))
