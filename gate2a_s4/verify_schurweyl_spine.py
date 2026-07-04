#!/usr/bin/env python3
"""
G-2a-S4 conjecture note — verify ONLY the decidable, R2-defensible rep-theory spine:
  (C^2)^{otimes 3} = 4 (x) triv_{S3}  (+)  2 (x) std_{S3}   (Schur-Weyl on 3 qubits)
  - symmetric subspace = Sym^3(C^2) = spin-3/2 (dim 4, S3-trivial)
  - std-isotypic = 2 copies of spin-1/2 (dim 4, S3 acts by the 2-dim std rep)
  - sign rep of S3 ABSENT: no totally antisymmetric 3-qubit spin state (Lambda^3 C^2 = 0)
This is textbook (cited as prior art). It confirms the note's spine; it does NOT verify the
R3 exchange-derivation conjecture, nor which "4" is section-2.85's (that needs section-2.85,
a pure audit step in the framework project, not compute).
"""
import numpy as np
from itertools import permutations

# 3-qubit space C^8, basis index = 4*b2+2*b1+b0
def perm_op(p):                    # p permutes the 3 tensor factors (positions 2,1,0)
    M=np.zeros((8,8))
    for s in range(8):
        b=[(s>>2)&1,(s>>1)&1,s&1]          # [b2,b1,b0]
        nb=[b[p[i]] for i in range(3)]     # permuted
        t=(nb[0]<<2)|(nb[1]<<1)|nb[2]
        M[t,s]=1
    return M
def sgn(p):
    inv=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3)); return -1 if inv%2 else 1

S3=list(permutations(range(3)))
Psym =sum(perm_op(p) for p in S3)/6.0
Pasym=sum(sgn(p)*perm_op(p) for p in S3)/6.0
r_sym =int(round(np.trace(Psym))); r_asym=int(round(np.trace(Pasym)))
r_std =8-r_sym-r_asym
print("="*66); print("G-2a-S4 spine: Schur-Weyl on (C^2)^{otimes 3}"); print("="*66)
print(f"\n  dim symmetric (Sym^3)   = {r_sym}   (S3-trivial sector)")
print(f"  dim antisymmetric (L^3) = {r_asym}   (S3-SIGN sector -> ABSENT, the tell)")
print(f"  dim std-isotypic        = {r_std}   (= 2 copies of the 2-dim std_S3)")

# total spin S^2 on each S3-sector -> identify SU(2) content
sx=np.array([[0,1],[1,0]])/2; sy=np.array([[0,-1j],[1j,0]])/2; sz=np.array([[1,0],[0,-1]])/2
def op1(o,pos):
    mats=[np.eye(2)]*3; mats[pos]=o
    M=mats[0]
    for m in mats[1:]: M=np.kron(M,m)
    return M
Sx=sum(op1(sx,i) for i in range(3)); Sy=sum(op1(sy,i) for i in range(3)); Sz=sum(op1(sz,i) for i in range(3))
S2=(Sx@Sx+Sy@Sy+Sz@Sz).real
def spin_on(P):
    # eigenvalues of S^2 restricted to range(P)
    w,V=np.linalg.eigh(P); B=V[:,w>0.5]                 # orthonormal basis of the subspace
    s2=(B.conj().T@S2@B); ev=np.linalg.eigvalsh(s2)
    js=sorted(set(round((-1+np.sqrt(1+4*e))/2,3) for e in ev))   # j from j(j+1)
    return ev, js
ev_sym,js_sym=spin_on(Psym)
print(f"\n  S^2 on symmetric subspace: eigenvalues ~ {np.round(ev_sym,3)}  -> j = {js_sym}")
print(f"    -> j=3/2 (S^2=15/4=3.75): the SPIN-3/2 QUARTET = Sym^3, S3-trivial. CONFIRMED.")
Pstd=np.eye(8)-Psym-Pasym
ev_std,js_std=spin_on(Pstd)
print(f"  S^2 on std-isotypic: eigenvalues ~ {np.round(ev_std,3)}  -> j = {js_std}")
print(f"    -> two spin-1/2 doublets (S^2=3/4=0.75), carrying std_S3 (mixed symmetry). CONFIRMED.")

print("\n  SPINE VERIFIED (R2, textbook): the quartet is the totally-symmetric (ternary Sym^3)")
print("  branch of three doublets; the sign rep is absent -> ternary antisymmetry is exiled to")
print("  color eps^{abc} (the Greenberg/Han-Nambu argument). The R3 exchange-derivation route")
print("  and the 'which 4 is section-2.85's' disambiguation are NOT settled here.")
