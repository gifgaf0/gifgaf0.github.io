import numpy as np
from itertools import combinations, product

# ---- 1. Octonion Fano lines (standard cyclic convention), indices 1..7 ----
lines = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]
def cyc(t):  # cyclic + reverse closure of a triple
    a,b,c=t; return {(a,b,c),(b,c,a),(c,a,b)}, {(c,b,a),(a,c,b),(b,a,c)}

# totally antisymmetric structure tensor phi on 1..7
phi = {}
for L in lines:
    pos,neg = cyc(L)
    for t in pos: phi[t]=+1
    for t in neg: phi[t]=-1

all_triples = list(combinations(range(1,8),3))
support = [t for t in all_triples if any((perm in phi) for perm in [t]) or tuple(sorted(t)) in [tuple(sorted(L)) for L in lines]]
nz = [t for t in all_triples if tuple(sorted(t)) in {tuple(sorted(L)) for L in lines}]
print(f"[1] triples total={len(all_triples)}  phi-nonzero (lines)={len(nz)}  expected 35,7 -> {'OK' if len(all_triples)==35 and len(nz)==7 else 'FAIL'}")

# ---- 2. F21 = <x: i->i+1 mod7,  y: i->2i mod7> on points 1..7; permutation character ----
def perm_from(f): return {i:((f(i-1)%7)+1) for i in range(1,8)}  # work 0-indexed internally
x = {i:(i%7)+1 for i in range(1,8)}                 # 7-cycle  i->i+1 (mod 7, on 1..7)
y = {i:(((2*(i-1))%7)+1) for i in range(1,8)}       # multiply-by-2 map (order 3: 2^3=8=1 mod7)
def compose(p,q): return {i:p[q[i]] for i in range(1,8)}
def order(p):
    n=1; r=p
    while any(r[i]!=i for i in range(1,8)): r=compose(p,r); n+=1
    return n
# generate the group
G=set(); frontier=[{i:i for i in range(1,8)}]
gens=[x,y]
seen={tuple(sorted(d.items()))}  if False else set()
def key(p): return tuple(p[i] for i in range(1,8))
group={key({i:i for i in range(1,8)}):{i:i for i in range(1,8)}}
changed=True
while changed:
    changed=False
    for p in list(group.values()):
        for g in gens:
            r=compose(g,p)
            if key(r) not in group:
                group[key(r)]=r; changed=True
elts=list(group.values())
print(f"[2] |F21| generated = {len(elts)}  expected 21 -> {'OK' if len(elts)==21 else 'FAIL'}")

# class data by order, permutation character chi(g)=#fixed points
from collections import Counter
ords=Counter(order(p) for p in elts)
print(f"    element orders: {dict(sorted(ords.items()))}  expected {{1:1,3:14,7:6}}")
def fix(p): return sum(1 for i in range(1,8) if p[i]==i)
# average inner products of the permutation character with itself and with trivial
chi=[fix(p) for p in elts]
inner_triv=sum(chi)/len(elts)
inner_self=sum(c*c for c in chi)/len(elts)
print(f"    <chi_perm, triv> = {inner_triv:.3f} (->#trivial)   <chi_perm,chi_perm> = {inner_self:.3f}")
# remainder chi - triv ; its squared norm = number of distinct nontrivial irreducibles (each once)
rem_norm = inner_self - inner_triv**2  # since <chi,chi> = sum m_i^2, <chi,triv>=m_triv
print(f"    remainder squared-norm = <chi,chi> - <chi,triv>^2 = {rem_norm:.3f}  (2 => two distinct irreps each once)")
print(f"    => decomposition 1 (+) {int(round((inner_self-1)/2))}-dim (+) {int(round((inner_self-1)/2))}-dim conj : "
      f"{'1 + 3 + 3bar  OK' if abs(inner_triv-1)<1e-9 and abs(rem_norm-2)<1e-9 else 'CHECK'}")

# ---- 3. Line-restricted antisymmetric internal coupling: eigenstructure ----
def restricted_matrix(triple):
    idx=list(triple); M=np.zeros((3,3))
    for a in range(3):
        for b in range(3):
            t=(idx[a],idx[b])
            # M_ab = sum_c phi_{a b c} over c in the triple (weight 1) -> antisymmetric coupling
            s=0
            for c in range(3):
                key3=(idx[a],idx[b],idx[c])
                s+=phi.get(key3,0)
            M[a,b]=s
    return M

L=(1,2,4)        # a Fano line  -> expect 2 chiral (+- i*sqrt3), 1 zero
NL=(1,2,3)       # not a line   -> expect zero matrix (inert)
for name,T in [("line {1,2,4}",L),("non-line {1,2,3}",NL)]:
    M=restricted_matrix(T)
    ev=np.linalg.eigvals(M)
    ev=sorted(ev,key=lambda z:(abs(z.imag),z.imag))
    antisym = np.allclose(M,-M.T)
    nz_modes=sum(1 for e in ev if abs(e)>1e-9)
    print(f"[3] {name}: antisymmetric={antisym}  ||M||_F={np.linalg.norm(M):.4f}  "
          f"eigs={[complex(round(e.real,4),round(e.imag,4)) for e in ev]}  nonzero modes={nz_modes}")
print(f"    sqrt(3) = {np.sqrt(3):.6f}  (the |+- i*c| magnitude on a line)")
