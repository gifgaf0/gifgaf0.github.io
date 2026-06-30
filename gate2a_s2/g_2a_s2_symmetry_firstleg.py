#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G-2a-S2 : rotational symmetry group of the canonical Borromean baryon
          representative (three mutually perpendicular golden ellipses,
          semi-axes phi, 1/phi; the sec 3.4-G2 / sec 3.09 config = t12067).

Decides: octahedral (2O, has the spin-3/2 quartet) vs tetrahedral
         (2T = SL(2,3), genuine irreps {2,2,2}, NO spin-3/2 quartet).

The mu_n factor-of-4 (Route 1, D1=1) was FORCED *given* octahedral 2O.
This screen tests whether the in-canon Borromean geometry supplies it.
Pure geometry; nothing tuned (Eddington: config fixed, symmetry read off).
"""
import numpy as np
from itertools import permutations, product

phi = (1+np.sqrt(5))/2
a, b = phi, 1/phi                      # major, minor semi-axes

# ---- the three perpendicular golden ellipses (cyclic major-axis arrangement) ----
t = np.linspace(0, 2*np.pi, 720, endpoint=False)
E3 = np.stack([a*np.cos(t),  b*np.sin(t),  0*t], 1)   # xy-plane: major x, minor y
E1 = np.stack([0*t,          a*np.cos(t),  b*np.sin(t)], 1)  # yz: major y, minor z
E2 = np.stack([b*np.sin(t),  0*t,          a*np.cos(t)], 1)  # zx: major z, minor x
pts = np.vstack([E1, E2, E3])
print(f"config: 3 golden ellipses (a=phi={a:.4f}, b=1/phi={b:.4f}); {len(pts)} sample pts")

# ---- canonical point set for fast equality test ----
def canon(P):
    return set(map(tuple, np.round(P, 5)))
S0 = canon(pts)

def preserves(M):
    return canon(pts @ M.T) == S0

# ---- enumerate the full signed-permutation group B3 (48 elements) ----
B3 = []
for perm in permutations(range(3)):
    P = np.zeros((3,3))
    for i,j in enumerate(perm): P[i,j] = 1
    for signs in product((1,-1), repeat=3):
        B3.append(np.diag(signs) @ P)
print(f"|B3| (octahedral O_h, signed perms) = {len(B3)} (expect 48)")

sym = [M for M in B3 if preserves(M)]
rot = [M for M in sym if np.linalg.det(M) > 0]      # det +1 = proper rotations
print(f"\n|full symmetry group (in O_h)| = {len(sym)}")
print(f"|rotational subgroup (det +1)| = {len(rot)}  <-- decision scalar |G_rot|")

# ---- C4 test: any order-4 proper rotation preserving the config? ----
def order(M):
    X = np.eye(3); 
    for k in range(1,13):
        X = X @ M
        if np.allclose(X, np.eye(3), atol=1e-6): return k
    return None
has_C4 = any(order(M) == 4 for M in rot)
print(f"rotation orders present: {sorted(set(order(M) for M in rot))}")
print(f"C4 (order-4 rotation) present? {has_C4}   <-- octahedral discriminator")

# ---- classify ----
nrot = len(rot)
if nrot >= 24 and has_C4:
    gtype, binlift, quartet = "OCTAHEDRAL O", "2O", "HAS the unique 4-dim genuine irrep (spin-3/2)"
elif nrot == 12 and not has_C4:
    gtype, binlift, quartet = "TETRAHEDRAL T = A4", "2T = SL(2,3)", "genuine irreps {2,2,2}: NO 4-dim quartet"
elif nrot == 6:
    gtype, binlift, quartet = "DIHEDRAL D3", "2D3", "no 4-dim genuine irrep"
else:
    gtype, binlift, quartet = f"order-{nrot} (other)", "?", "inspect"

print("\n" + "="*68)
print("VERDICT (against the locked arms)")
print("="*68)
print(f"  |G_rot| = {nrot}  ->  {gtype}")
print(f"  binary lift = {binlift}")
print(f"  spin-3/2 quartet: {quartet}")
print()
if "OCTAHEDRAL" in gtype:
    print("  -> OCTAHEDRAL arm: the topological representative realizes 2O;")
    print("     the factor-of-4 (Route 1 D1=1) is geometrically SUPPORTED here.")
else:
    print("  -> TETRAHEDRAL-or-lower arm: the in-canon Borromean representative")
    print("     does NOT carry octahedral symmetry, so 2T (or lower) has NO")
    print("     4-dim genuine irrep -> the spin-3/2 quartet / mu_n factor-of-4 is")
    print("     NOT supported by THIS geometry.  The octahedral premise (sec 2.85)")
    print("     must come from the richer baryon geometry (K7/Szilassi/relaxed")
    print("     core) -> a located M.ONT / core-geometry IMPORT, not a refutation.")
    print()
    print("  Feedback to G-2a-S1: its 'forced spin-3/2 quartet (D1=1)' must fold")
    print("  CONDITIONAL on octahedral soliton symmetry, with that premise named")
    print("  as the import -- not as an unconditional structural fact.")

# ---- which symmetry ops permute the 3 strands (the NC5 / FR-constraint content) ----
def strand_perm(M):
    # how M permutes (E1,E2,E3): match transformed-ellipse point sets
    blocks = {0: canon(E1), 1: canon(E2), 2: canon(E3)}
    sigma = []
    for E in (E1, E2, E3):
        Et = canon(E @ M.T)
        sigma.append(next(k for k,v in blocks.items() if v == Et))
    return tuple(sigma)
perms = sorted(set(strand_perm(M) for M in rot))
print("\n  strand permutations induced by the rotational symmetry:")
print(f"    {perms}")
print(f"    -> induced strand-permutation group order = {len(perms)}")
print("    (these are the FR / color-Weyl content of NC5: a strand permutation")
print("     acts on the color singlet eps^abc only by sgn(sigma) -> color charge")
print("     preserved -> NC5 benign FOR A COLOR-SINGLET baryon; the residual is")
print("     standard spin-statistics, not spin<->color mixing.)")
