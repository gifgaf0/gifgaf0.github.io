#!/usr/bin/env python3
"""
G-2a-S3 — CC second leg for the DECIDABLE R1 rep-theory piece only:
  spin-3/2 is IRREDUCIBLE over 2O (<chi,chi>=1, the quartet) but SPLITS AS 2+2 over 2T
  (<chi,chi>=2 = two distinct 2-dim genuine irreps). The quartet does not vanish under
  tetrahedral symmetry -- it FRAGMENTS.
Independent build: 2O and 2T as SU(2) matrices (matrix closure), Chebyshev characters.
(The R3 construction-literature verdict is NOT second-legged here -- it is literature-based
and correctly banked as a suggestive negative.)
"""
import numpy as np
from itertools import product

def q2su2(w,x,y,z): return np.array([[w+1j*x, y+1j*z],[-y+1j*z, w-1j*x]],complex)
def close(gens):
    key=lambda M:tuple(np.round(M.flatten(),6))
    G={key(np.eye(2,dtype=complex)):np.eye(2,dtype=complex)}; fr=[np.eye(2,dtype=complex)]
    while fr:
        A=fr.pop()
        for g in gens:
            for B in (g@A,A@g):
                if key(B) not in G: G[key(B)]=B; fr.append(B)
    return list(G.values())
def U(n,x):
    U0=1.0; U1=2*x
    if n==0: return 1.0
    if n==1: return U1
    for _ in range(2,n+1): U0,U1=U1,2*x*U1-U0
    return U1
def chi(j2,M): return U(j2, np.real(np.trace(M))/2.0)
def norm2(grp,j2): return np.mean([chi(j2,M)**2 for M in grp]).real
def nclasses(grp):
    key=lambda M:tuple(np.round(M.flatten(),6)); seen=set(); c=0
    for g in grp:
        if key(g) in seen: continue
        orb={key(h@g@np.linalg.inv(h)) for h in grp}; seen|=orb; c+=1
    return c

# 2O = <order-8, order-6>  ;  2T = <order-6 (binary 3-fold), quaternion i (order 4)>
O2 = close([q2su2(*( (1/np.sqrt(2))*np.array([1,1,0,0]) )), q2su2(*(0.5*np.array([1,1,1,1])))])
T2 = close([q2su2(*(0.5*np.array([1,1,1,1]))), q2su2(0,1,0,0)])
mI=-np.eye(2,dtype=complex)
print("="*70); print("G-2a-S3 decidable-piece second leg (spin-3/2 over 2O vs 2T)"); print("="*70)
print(f"\n|2O| = {len(O2)} (48)   |2T| = {len(T2)} (24)   2T subset 2O: "
      f"{all(any(np.allclose(t,o) for o in O2) for t in T2)}")
print(f"central -I in 2T: {any(np.allclose(t,mI) for t in T2)}")

print("\n--- spin-3/2 norm over each group ---")
n2O=norm2(O2,3); n2T=norm2(T2,3)
print(f"  <chi_3/2, chi_3/2>_2O = {n2O:.4f}  -> {'IRREDUCIBLE quartet' if abs(n2O-1)<1e-6 else '?'}")
print(f"  <chi_3/2, chi_3/2>_2T = {n2T:.4f}  -> {'SPLITS 2+2 (two distinct genuine 2s)' if abs(n2T-2)<1e-6 else '?'}")
print(f"  spin-1/2 over 2T: <1/2,1/2>_2T = {norm2(T2,1):.4f} (irreducible genuine 2)")
print(f"  chi_3/2(-I)_2T = {chi(3,mI):+.1f} (still genuine/FR); chi_3/2(I) = {chi(3,np.eye(2,dtype=complex)):+.1f}")

print("\n--- 2T genuine-irrep structure (why {2,2,2}, no 4-dim) ---")
c2T=nclasses(T2)                       # = # irreps of 2T
# bosonic = irreps of A4 = 2T/{+-I}; A4 has 4 classes -> 4 bosonic irreps (dims 1,1,1,3)
print(f"  #classes(2T) = {c2T} (=# irreps; expect 7);  bosonic (A4) = 4 (dims 1,1,1,3, sumsq 12)")
print(f"  genuine = {c2T-4} irreps, sumsq = 24-12 = 12 -> dims (2,2,2): NO 4-dim genuine irrep")
print(f"  => the 2O quartet (4) has no home in 2T; it fragments into two of the three 2s. R1 CONFIRMED.")
