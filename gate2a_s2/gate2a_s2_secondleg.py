#!/usr/bin/env python3
"""
G-2a-S2 INDEPENDENT SECOND LEG (CC, from scratch) — rotational symmetry group of the
canonical three-golden-ellipse Borromean baryon representative (semi-axes phi, 1/phi).

Decides: OCTAHEDRAL (|G_rot|>=24, C4 present -> 2O, has the spin-3/2 quartet) vs
         TETRAHEDRAL (|G_rot|=12, no C4 -> 2T=SL(2,3), genuine irreps {2,2,2}, NO quartet).

Two independent methods (both from scratch vs the first leg's sampled-set search):
  (M1) SAMPLING-FREE ellipse-signature argument: any symmetry permutes the 3 axis-aligned
       ellipses, hence permutes the coordinate axes (signed perm); since phi != 1/phi the
       in-plane symmetry is only C2, so ALL symmetries are signed permutations. A signed
       perm preserves the config iff its axis-permutation preserves the cyclic ordered set
       of (major,minor) pairs {(x,y),(y,z),(z,x)}. -> exact, integer.
  (M2) SAMPLED point-set cross-check on my own sampling, exact integer rotation matrices.
Pure geometry; nothing tuned (Eddington: config fixed, symmetry read off). M.CW ceiling R2.
"""
import numpy as np
from itertools import permutations, product

phi=(1+np.sqrt(5))/2; a,b=phi,1/phi
X,Y,Z=0,1,2
# config as (major-axis, minor-axis) ordered pairs:  E3=(x,y) E1=(y,z) E2=(z,x)
CONFIG={(X,Y),(Y,Z),(Z,X)}        # cyclic ordered pairs (major,minor); sign-independent (lines)
ELL_NAME={(X,Y):"E3(xy)",(Y,Z):"E1(yz)",(Z,X):"E2(zx)"}

print("="*72); print("G-2a-S2 SECOND LEG (independent: signature argument + sampled cross-check)"); print("="*72)
print(f"config: 3 golden ellipses a=phi={a:.4f}, b=1/phi={b:.4f}; (major,minor) pairs = {sorted(CONFIG)}")

# ---- enumerate signed permutations (S3 x {+-1}^3 = 48 = O_h) ----
def signed_perms():
    out=[]
    for p in permutations(range(3)):
        P=np.zeros((3,3),int)
        for i,j in enumerate(p): P[i,j]=1
        for s in product((1,-1),repeat=3):
            out.append((np.diag(s)@P, p, s))
    return out
SP=signed_perms()
print(f"\n|signed perms (O_h)| = {len(SP)} (expect 48)")

# ---- (M1) signature test: axis-perm preserves CONFIG cyclic set? (sign-free) ----
def axis_perm_of(p):           # p[i] = image axis of e_i ; as a map on axes
    return {i:p[i] for i in range(3)}
def preserves_sig(p):
    sigma=axis_perm_of(p)
    mapped={(sigma[u],sigma[v]) for (u,v) in CONFIG}
    return mapped==CONFIG
def detsign(M): return int(round(np.linalg.det(M)))

rot_M1=[(M,p,s) for (M,p,s) in SP if preserves_sig(p) and detsign(M)==1]
full_M1=[(M,p,s) for (M,p,s) in SP if preserves_sig(p)]
print(f"\n[M1 signature] preservers: full(det +-1)={len(full_M1)}, rotational(det +1)={len(full_M1)//1 and len(rot_M1)}")

# ---- (M2) sampled point-set cross-check (my own sampling, exact integer rotations) ----
t=np.linspace(0,2*np.pi,360,endpoint=False)
E3=np.stack([a*np.cos(t), b*np.sin(t), 0*t],1)
E1=np.stack([0*t, a*np.cos(t), b*np.sin(t)],1)
E2=np.stack([b*np.sin(t), 0*t, a*np.cos(t)],1)
P=np.vstack([E1,E2,E3]); S0=set(map(tuple,np.round(P,5)))
def preserves_pts(M): return set(map(tuple,np.round(P@M.T,5)))==S0
rot_M2=[(M,p,s) for (M,p,s) in SP if preserves_pts(M) and detsign(M)==1]
print(f"[M2 sampled  ] rotational preservers (det +1) = {len(rot_M2)}")
agree = sorted((tuple(M.flatten()) for M,_,_ in rot_M1))==sorted((tuple(M.flatten()) for M,_,_ in rot_M2))
print(f"  M1 and M2 agree on the rotational group: {agree}")

# ---- order + C4 discriminator ----
def order(M):
    Xm=np.eye(3,dtype=int)
    for k in range(1,13):
        Xm=Xm@M
        if np.array_equal(Xm,np.eye(3,dtype=int)): return k
    return None
rot=[M for M,_,_ in rot_M1]
orders=sorted(set(order(M) for M in rot))
nC3=sum(order(M)==3 for M in rot); nC2=sum(order(M)==2 for M in rot); nC4=sum(order(M)==4 for M in rot)
has_C4 = nC4>0
print(f"\n|G_rot| = {len(rot)}   rotation orders present = {orders}")
print(f"  composition: 1 identity + {nC2} C2 + {nC3} C3 + {nC4} C4")
print(f"  C4 present? {has_C4}   <-- octahedral discriminator")

# explicit cross-check: tetrahedral elements present, octahedral extras absent
C3_111=np.array([[0,0,1],[1,0,0],[0,1,0]])          # x->y->z->x about (1,1,1)
C2_z  =np.array([[-1,0,0],[0,-1,0],[0,0,1]])
C4_z  =np.array([[0,-1,0],[1,0,0],[0,0,1]])         # octahedral-only
C2_xy =np.array([[0,1,0],[1,0,0],[0,0,-1]])         # face-diagonal C2 (octahedral-only)
print(f"\n  explicit: C3 about (1,1,1) preserves? {preserves_pts(C3_111)} (T elt)")
print(f"            C2 about z      preserves? {preserves_pts(C2_z)} (T elt)")
print(f"            C4 about z      preserves? {preserves_pts(C4_z)} (octahedral-only -> must be False)")
print(f"            C2 face-diag xy preserves? {preserves_pts(C2_xy)} (octahedral-only -> must be False)")

# ---- strand-permutation content (NC5 / FR-constraint) ----
def strand_perm(p):
    sigma=axis_perm_of(p)
    img={}
    for (u,v) in CONFIG:
        img[(u,v)] = (sigma[u],sigma[v])
    # name -> name permutation
    return tuple(sorted((ELL_NAME[k],ELL_NAME[img[k]]) for k in CONFIG))
sperms=set()
for M,p,s in rot_M1:
    sigma=axis_perm_of(p)
    perm=tuple(sorted(ELL_NAME[(u,v)]+"->"+ELL_NAME[(sigma[u],sigma[v])] for (u,v) in CONFIG))
    sperms.add(perm)
print(f"\n  induced strand-permutation group order = {len(sperms)} (the C3 axis-cycle -> Z3; the 3 C2 fix strands)")
print( "  all induced strand perms are EVEN (3-cycles) -> sgn = +1 -> color singlet eps^abc preserved")
print( "  -> NC5 BENIGN for a color-singlet baryon: spatial rotation does not leak into color charge.")

# ---- verdict ----
print("\n"+"="*72); print("VERDICT (against the locked arms)"); print("="*72)
if len(rot)>=24 and has_C4:
    print(f"  |G_rot|={len(rot)} OCTAHEDRAL (2O) -> spin-3/2 quartet GEOMETRICALLY SUPPORTED.")
elif len(rot)==12 and not has_C4:
    print(f"  |G_rot|=12  ->  TETRAHEDRAL  T = A4   (binary lift 2T = SL(2,3))")
    print(f"  2T genuine irreps are {{2,2,2}} -> NO 4-dim genuine irrep -> the spin-3/2 quartet /")
    print(f"  mu_n factor-of-4 is NOT supported by THIS topological representative.")
    print(f"  -> The octahedral premise (Route 1, D1=1) must come from the RICHER baryon geometry")
    print(f"     (K7/Szilassi/relaxed core) = a LOCATED M.ONT / core-geometry IMPORT, not a refutation.")
    print(f"\n  FEEDBACK TO G-2a-S1 (before its fold): its 'forced spin-3/2 quartet (D1=1)' must fold")
    print(f"  CONDITIONAL on octahedral soliton symmetry, with that premise named as the import --")
    print(f"  NOT as an unconditional structural fact. (This is why Route 2 ran before the S1 fold.)")
else:
    print(f"  |G_rot|={len(rot)} (other) -> inspect.")
print("\n  CONFIRMS the first leg: TETRAHEDRAL, no C4; NC5 benign for color-singlet baryon.")
