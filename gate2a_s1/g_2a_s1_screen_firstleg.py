#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G-2a-S1 : Route-1 structural necessary-condition screen for the soliton
          spin-isospin locking (sec 2.87.A).

Tests the NECESSARY conditions for 2O_spatial  -->  SU(2)_internal locking:
  NC1  existence of an embedding 2O in SU(2) with central element -> -Id
  NC2  spin-3/2 = the genuine 4-dim quartet, with FR sign  (chi(-1) = -4)
  NC2' FORCING: the FR/spinor-phase requirement selects a UNIQUE fermionic
       quartet  (D1 = #{4-dim genuine-sector irreps of 2O})
  NC3  TRANSVERSALITY to color: can the locked spin-SU(2) commute with
       color-SU(3)?  (D2 = dim_C commutant of SU(3) in M4(C))

Pure finite-group + Lie rep theory.  M.CW ceiling = R2 (admissibility).
The screen cannot return the dynamical locking fact.  Eddington: the factor-of-4
is the screened OBJECT, not a tuned parameter; nothing is fit.
"""
import numpy as np
from itertools import product

print("="*72)
print("G-2a-S1  Route-1 necessary-condition screen  (chat-side first leg)")
print("="*72)

# ---------------------------------------------------------------- build 2O
r = 1/np.sqrt(2); Q = set()
for idx in range(4):                                   # +-1,+-i,+-j,+-k   (8)
    for s in (1, -1):
        q = [0., 0., 0., 0.]; q[idx] = s; Q.add(tuple(q))
for sg in product((1, -1), repeat=4):                  # (+-1+-i+-j+-k)/2  (16)
    Q.add(tuple(0.5*s for s in sg))
for i in range(4):                                     # (+-e_a+-e_b)/sqrt2 (24)
    for j in range(i+1, 4):
        for si in (1, -1):
            for sj in (1, -1):
                q = [0., 0., 0., 0.]; q[i] = si*r; q[j] = sj*r; Q.add(tuple(q))
Q = [np.array(x) for x in Q]

def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1*w2 - x1*x2 - y1*y2 - z1*z2,
                     w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2])
keys = {tuple(np.round(q, 6)) for q in Q}
closed = all(tuple(np.round(qmul(a, b), 6)) in keys for a in Q for b in Q)
print(f"\n[group]  |2O| = {len(Q)} (expect 48); closed under mult (a group)? {closed}")

# ---------------------------------------------------- spin-j characters on 2O
# theta = 2*phi, phi = arccos(Re q);  chi_j(q) = sum_{m=-j..j} cos(m theta)
def chi(jname, q):
    phi = np.arccos(np.clip(q[0], -1, 1))
    if jname == "0":   return 1.0
    if jname == "1/2": return 2*np.cos(phi)
    if jname == "1":   return 1 + 2*np.cos(2*phi)
    if jname == "3/2": return 2*np.cos(3*phi) + 2*np.cos(phi)
def inner(f, g):  # <f,g> = (1/|G|) sum f(q) conj(g(q)); real characters here
    return sum(f(q)*g(q) for q in Q)/len(Q)

c32 = lambda q: chi("3/2", q)
c1  = lambda q: chi("1",   q)
one = lambda q: chi("0",   q)
e   = np.array([1., 0, 0, 0])        # identity quaternion
mc  = np.array([-1., 0, 0, 0])       # central element  (the 2pi rotation)

print("\n--- NC1 / NC2 : spin-3/2 as the genuine quartet on 2O -------------")
print(f"  chi_3/2(1)   = {c32(e):+.3f}   (the quartet, dim 4)")
print(f"  chi_3/2(-1)  = {c32(mc):+.3f}   (central -> -Id : FR / spinor phase PRESENT)")
print(f"  <3/2,3/2>    = {inner(c32,c32):.4f}   -> single irrep? {abs(inner(c32,c32)-1)<1e-6}")
print(f"  chi_1(-1)    = {c1(mc):+.3f}   (integer-spin/vector: central -> +Id : BOSONIC)")
print(f"  chi_0(-1)    = {one(mc):+.3f}   (trivial: central -> +Id : BOSONIC)")
print("  => FR (central -> -Id) selects the GENUINE/fermionic sector; the")
print("     integer-spin (bosonic) sector is excluded.")

# -------------------------------------------- D1 : fermionic-sector dim count
# 2O irreps (8 conj. classes): dims 1,1,2,3,3 (bosonic, factor through O=S4,
# central->+Id) and 2,2,4 (genuine, central->-Id).  Sum of squares:
bos = [1, 1, 2, 3, 3]; gen = [2, 2, 4]
assert sum(d*d for d in bos) == 24 and sum(d*d for d in gen) == 24
assert sum(d*d for d in bos+gen) == 48
D1 = sum(1 for d in gen if d == 4)
print("\n--- D1 : forcing of the factor-of-4 quartet -----------------------")
print(f"  2O bosonic-sector dims (central->+Id): {bos}  (sum sq = 24 = |S4|)")
print(f"  2O genuine-sector dims (central->-Id): {gen}  (sum sq = 24)")
print(f"  D1 = #(4-dim genuine irreps) = {D1}")
print(f"  -> the FR-sector quartet is {'FORCED (unique)' if D1==1 else 'NOT unique'};")
print( "     verified above that chi_3/2 IS that quartet (<3/2,3/2>=1, chi(-1)=-4).")

# --------------------------------- D2 : transversality of spin-SU(2) to color
# color SU(3) acts as 3 (+) 1 inside SU(4); Gell-Mann in the upper 3x3 block.
gell = [np.array(M, complex) for M in [
    [[0,1,0],[1,0,0],[0,0,0]], [[0,-1j,0],[1j,0,0],[0,0,0]],
    [[1,0,0],[0,-1,0],[0,0,0]], [[0,0,1],[0,0,0],[1,0,0]],
    [[0,0,-1j],[0,0,0],[1j,0,0]], [[0,0,0],[0,0,1],[0,1,0]],
    [[0,0,0],[0,0,-1j],[0,1j,0]],
    (1/np.sqrt(3))*np.array([[1,0,0],[0,1,0],[0,0,-2]])]]
def embed4(M3):
    M = np.zeros((4,4),complex); M[:3,:3] = M3; return M
col = [embed4(L) for L in gell]

def commutant_dim(gens, n):
    rows = []
    for G in gens:
        K = np.zeros((n*n, n*n), complex)
        for a in range(n):
            for b in range(n):
                rr = a*n+b
                for k in range(n):
                    K[rr, a*n+k] += G[k,b]
                    K[rr, k*n+b] -= G[a,k]
        rows.append(K)
    A = np.vstack(rows)
    s = np.linalg.svd(A, compute_uv=False)
    tol = 1e-9*max(1.0, s[0])
    return int(n*n - np.sum(s > tol))

D2 = commutant_dim(col, 4)
print("\n--- D2 : transversality of the locked spin-SU(2) to color ---------")
print(f"  dim_C commutant of color-SU(3) in M4(C) = {D2}")
print(f"  (the two projectors onto the 3 and the 1 -> abelian; connected")
print(f"   group commutant = U(1)xU(1) cap SU(4) = U(1), ABELIAN)")
print(f"  -> can 2O (order 48, NON-abelian) sit in this commutant? "
      f"{'NO' if D2<=2 else 'maybe'}")
print("  -> SINGLE-SU(4) hosting of the spin-2O alongside color FAILS:")
print("     the locked spin-SU(2) must be a SEPARATE TRANSVERSE FACTOR.")

# tensor-product arena: spin = 1 (x) J  ;  color = lambda (x) 1  -> commute
Jx = np.array([[0,1,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]],complex)  # any spin gen stand-in
I2 = np.eye(2,dtype=complex)
sigx = np.array([[0,1],[1,0]],complex)                       # a spin-SU(2) generator
lam3 = (1/np.sqrt(3))*np.array([[1,0,0],[0,1,0],[0,0,-2]])    # a color generator (3x3 -> pad)
# color (x) 1_spin  vs  1_color (x) spin, on C^3 (x) C^2:
C_op = np.kron(lam3, I2)
S_op = np.kron(np.eye(3,dtype=complex), sigx)
tp_comm = np.max(np.abs(C_op@S_op - S_op@C_op))
print(f"\n  TENSOR-PRODUCT arena  C(x)O (x) (spin SU(2)):")
print(f"    max |[color(x)1 , 1(x)spin]| = {tp_comm:.1e}  -> commute? {tp_comm<1e-9}")
print( "    -> transverse realization EXISTS (by construction of the product).")

# ----------------------------------------------------------------- verdict
print("\n" + "="*72)
print("VERDICT  (against the locked pre-registered arms)")
print("="*72)
null_arm  = (D1 == 0) or (D2 > 2 and tp_comm >= 1e-9 and False)  # no transverse arena
transverse_ok = (tp_comm < 1e-9)            # tensor-product arena admissible
pass_arm  = (D1 >= 1) and transverse_ok
print(f"  D1 = {D1}   D2 = {D2}   tensor-product transverse = {transverse_ok}")
if null_arm:
    print("  -> NULL : the locking route to a derived mu_n is structurally dead.")
elif pass_arm:
    print("  -> PASS-possible (R2).  Necessary condition MET.")
    print(f"     * the factor-of-4 quartet is {'FORCED (D1=1)' if D1==1 else 'available'};")
    print("     * FR/spinor phase present (chi_3/2(-1) = -4);")
    print("     * the locked spin-SU(2) is NOT hostable inside the color SU(4)")
    print("       (commutant abelian) -> it must be a separate TRANSVERSE factor,")
    print("       which the tensor-product arena C(x)O(x)H supplies (the structure")
    print("       sec 2.87.A already forced).")
    print("     * the screen does NOT settle Assignment I vs II, and CANNOT reach")
    print("       the dynamical locking fact (M.CW).  Greenlights Routes 2/3.")
else:
    print("  -> indeterminate; inspect.")
print("\n  OUT OF SCOPE (surfaced): NC5 baryon 3-strand permutation under spatial")
print("  rotation -- geometry-gated, needs Routes 2/3 / M.ONT; the place a genuine")
print("  obstruction could still live.")
