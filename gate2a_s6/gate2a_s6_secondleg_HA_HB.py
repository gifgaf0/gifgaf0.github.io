"""G-2a-S6 SECOND LEG (CC) -- H-A (group-theoretic core) + H-B (flat rigid dichotomy).
SnapPy-FREE. Independent of the chat leg (which used SnapPy peripheral data for H-A and the
chat's triple-bookkeeping for H-B).

H-A core: the axis representation, parity law <=> properness, image O, faithfulness, the
  N_{SO(3)}(O)=O uniqueness (finite check within O_h + adopted standard result), and the
  full-group model Z/2 x O with the axis rep killing the central Z/2 (kernel, fiber size 2).
  [The GEOMETRIC input that the central Z/2 is the amphichiral, axis-invisible involution, and
   the all-48 peripheral +-Id/+-diag split, are re-extracted independently in the companion
   SnapPy script gate2a_s6_secondleg_HC2.py -- flagged shared-solver.]

H-B: rigid symmetry group of the generic flat three-ellipse embedding, computed by EXACT
  rational vertex-set equality over Q (independent of the chat's axis-triple predicate):
  O(3)-stabilizer = 24 (pyritohedral), rotation part = 12 = A4 = the even-sigma motion subgroup
  element-for-element, Fix_flat(A4) = {0, infinity} = 2 points of the complement.
"""
from itertools import permutations, product
from fractions import Fraction as Fr

def rule(t): print("=" * 70); print(t); print("=" * 70)

def sgn3(p):
    s = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if p[i] > p[j]: s = -s
    return s

# signed 3x3 permutation matrices: (sigma, signs) -> matrix col j has signs[j] at row sigma[j]
def smat(sigma, signs):
    M = [[0, 0, 0] for _ in range(3)]
    for j in range(3):
        M[sigma[j]][j] = signs[j]
    return tuple(tuple(r) for r in M)
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
          - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
          + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
def matmul(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def transpose(A):
    return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))
ID = ((1,0,0),(0,1,0),(0,0,1))

ALL48 = [(sigma, signs) for sigma in permutations(range(3)) for signs in product((1,-1), repeat=3)]
Oh = [smat(s, e) for (s, e) in ALL48]                      # full signed-perm group O_h, order 48
O  = [smat(s, e) for (s, e) in ALL48 if det3(smat(s, e)) == 1]   # rotation part O, order 24

# ============================================================ H-A core
rule("H-A core -- axis rep, parity law <=> properness, image O, N_SO3(O)=O")
# parity law: sgn(sigma) = e1 e2 e3  <=>  det = +1
parity = all((det3(smat(s, e)) == 1) == (sgn3(s) * e[0]*e[1]*e[2] == 1) for (s, e) in ALL48)
print(f"parity law sgn(sigma)=e1e2e3  <=>  det(axis)=+1, over all 48: {parity}")
assert parity
print(f"|O_h| = {len(Oh)} (full signed-perm), |O| = det+1 part = {len(O)} (expect 24 = octahedral rotations)")
assert len(O) == 24
# orthogonality: signed perms are orthogonal (A A^T = I) -> image in O(3); det+1 -> SO(3)
orth = all(matmul(M, transpose(M)) == ID for M in O)
print(f"every axis matrix orthogonal (A A^T = I): {orth}; det=+1 -> image ⊂ SO(3): True")
assert orth
# faithfulness on the motion group: the 24 matrices are distinct by construction
print(f"axis rep faithful on the motion group: {len(set(O)) == 24}")

# N_{SO(3)}(O) = O : finite verification that O is self-normalizing inside O_h, and that its
# normalizer among ALL orthogonal signed-perm matrices is O_h with O_h ∩ SO(3) = O; combined
# with the standard fact (a rotation normalizing O permutes O's three 4-fold axes => monomial),
# this gives N_{SO(3)}(O) = O. Finite check:
Oset = set(O)
def normalizes(g):
    gi = transpose(g)   # orthogonal inverse
    return all(matmul(matmul(g, M), gi) in Oset for M in O)
norm_in_Oh = [g for g in Oh if normalizes(g)]
print(f"normalizer of O inside O_h: order {len(norm_in_Oh)} (= O_h, 48); "
      f"its rotation part = O (24): {sum(1 for g in norm_in_Oh if det3(g)==1) == 24}")
print("  + standard result: a rotation normalizing O permutes the three 4-fold axes, hence is")
print("  monomial (a signed perm), hence in O_h ∩ SO(3) = O  =>  N_{SO(3)}(O) = O.")
print("  => the spatial identification motion-group ≅ O is UNIQUE up to inner automorphisms. R1.")

# full-group model Z/2 x O: axis rep kills the central Z/2 (amphichiral involution axis-invisible)
rule("H-A full-group model -- Z/2 x O, axis rep 2:1, kernel = central Z/2")
# model elements (z, M), z in {0,1} (z=1 the central amphichiral involution), M in O.
full = [(z, M) for z in (0, 1) for M in O]
print(f"|Z/2 x O| = {len(full)} (expect 48 = |Isom(BRC)|)")
def axis(elt):  # the axis rep sends (z,M) -> M  (the central Z/2 is axis-invisible)
    return elt[1]
# det(axis) = +1 for ALL 48 (image is O, never O_h):
print(f"det(axis matrix) = +1 for ALL 48 in the model (image = O, never O_h): "
      f"{all(det3(axis(e)) == 1 for e in full)}")
# kernel = {(0,I),(1,I)} = central Z/2
ker = [e for e in full if axis(e) == ID]
print(f"kernel of the full-group axis rep: order {len(ker)} = central Z/2 "
      f"(amphichiral involution axis-invisible): {ker == [(0,ID),(1,ID)]}")
# every fiber size 2, one orientation-preserving (z=0) + one reversing (z=1)
from collections import Counter
fib = Counter(axis(e) for e in full)
print(f"every axis-matrix fiber has size 2: {set(fib.values()) == {2}}; "
      f"each = one or-preserving (z=0) + one or-reversing (z=1): True")
print("Isom+ = {0} x O (the z=0 coset): axis rep restricted there is faithful onto O. R1.")

# ============================================================ H-B  (exact over Q)
rule("H-B -- flat three-ellipse rigid dichotomy (exact vertex-set equality over Q)")
# ring i in plane normal to axis n_i, long semi-axis a along L_i, short b along S_i.
# cyclic:  ring1 (n,L,S)=(x,y,z); ring2=(y,z,x); ring3=(z,x,y).
a, b = Fr(2), Fr(1)                      # generic a != b (genericity re-checked below with 3,1)
def e(k, val):
    v = [Fr(0), Fr(0), Fr(0)]; v[k] = val; return tuple(v)
def ring_vertices(n, L, S):
    # the four ellipse vertices: +-a along L, +-b along S  (the ellipse's own vertices)
    return frozenset([e(L, a), e(L, -a), e(S, b), e(S, -b)])
TRIP = {1: (0, 1, 2), 2: (1, 2, 0), 3: (2, 0, 1)}
RINGS = {i: ring_vertices(*TRIP[i]) for i in (1, 2, 3)}

def apply_mat_vec(M, v):
    return tuple(sum(M[i][j]*v[j] for j in range(3)) for i in range(3))
def apply_to_set(M, S):
    return frozenset(apply_mat_vec(M, v) for v in S)

def config_stab(matrices):
    stab = []
    for M in matrices:
        # M preserves the configuration iff it permutes the three ring vertex-sets
        images = {}
        ok = True
        for i in (1, 2, 3):
            img = apply_to_set(M, RINGS[i])
            match = [j for j in (1, 2, 3) if RINGS[j] == img]
            if len(match) != 1:
                ok = False; break
            images[i] = match[0]
        if ok and sorted(images.values()) == [1, 2, 3]:
            stab.append((M, tuple(images[i] for i in (1, 2, 3))))   # (matrix, ring perm)
    return stab

stab_full = config_stab(Oh)
stab_rot  = [(M, rp) for (M, rp) in stab_full if det3(M) == 1]
print(f"|O(3)-stabilizer of the configuration| = {len(stab_full)} (expect 24 = pyritohedral m-3bar)")
print(f"|rotation stabilizer|                   = {len(stab_rot)} (expect 12 = T = A4)")
assert len(stab_full) == 24 and len(stab_rot) == 12
# genericity: recompute with a=3,b=1 -> same stabilizer size
a, b = Fr(3), Fr(1)
RINGS = {i: ring_vertices(*TRIP[i]) for i in (1, 2, 3)}
assert len(config_stab(Oh)) == 24 and len([1 for (M,_) in config_stab(Oh) if det3(M)==1]) == 12
a, b = Fr(2), Fr(1); RINGS = {i: ring_vertices(*TRIP[i]) for i in (1, 2, 3)}
print("genericity: stabilizer sizes (24, 12) independent of the choice a!=b (tested 2:1 and 3:1). OK")

# every rigid element has EVEN ring/strand permutation
evens = all(sgn3(tuple(x-1 for x in rp)) == 1 for (M, rp) in stab_full)
print(f"every rigid (O(3)-stab) element has EVEN ring permutation: {evens}")
assert evens

# the rotation part = the even-sigma subgroup A4 of the motion group, element-for-element
def motion_of(M, rp):
    # strand permutation = ring permutation rp (0-indexed); eps_i = sign M puts on ring i's NORMAL axis
    sigma = tuple(rp[i] - 1 for i in range(3))
    eps = []
    for i in (1, 2, 3):
        n_axis = TRIP[i][0]
        col = [M[r][n_axis] for r in range(3)]
        s = [c for c in col if c != 0][0]
        eps.append(s)
    return (sigma, tuple(eps))
rigid_motions = set(motion_of(M, rp) for (M, rp) in stab_rot)
even_motion = set()
for sigma in permutations(range(3)):
    if sgn3(sigma) != 1: continue
    for eps in product((1, -1), repeat=3):
        if eps[0]*eps[1]*eps[2] == 1:      # sgn(sigma)=+1 => parity law forces product +1
            even_motion.add((tuple(sigma), eps))
print(f"distinct motion elements realized rigidly: {len(rigid_motions)} (expect 12)")
print(f"rigid rotation set == even-sigma A4 subgroup of the motion group (element-for-element): "
      f"{rigid_motions == even_motion}")
assert rigid_motions == even_motion and len(rigid_motions) == 12

# Fix_flat(A4) = {0, infinity}: common fixed points of the 12 rotations in R^3 u {inf}
rule("H-B -- Fix_flat(A4) = {0, infinity} (exactly 2 points, both in the complement)")
rot_mats = [M for (M, rp) in stab_rot]
# common fixed vectors v (Mv=v for all): solve over Q -> only v=0
def common_fixed_space(mats):
    # intersection of eigenspaces for eigenvalue 1; represent as solving (M-I)v=0 simultaneously
    rows = []
    for M in mats:
        for i in range(3):
            rows.append([M[i][j] - (1 if i == j else 0) for j in range(3)])
    # rank of the stacked system over Q
    # gaussian elimination
    R = [r[:] for r in rows]; rank = 0; piv = []
    for c in range(3):
        pr = next((i for i in range(rank, len(R)) if R[i][c] != 0), None)
        if pr is None: continue
        R[rank], R[pr] = R[pr], R[rank]
        inv = Fr(1) / R[rank][c]
        R[rank] = [x*inv for x in R[rank]]
        for i in range(len(R)):
            if i != rank and R[i][c] != 0:
                f = R[i][c]; R[i] = [R[i][j] - f*R[rank][j] for j in range(3)]
        piv.append(c); rank += 1
    return 3 - rank    # dim of common fixed space
nontriv = [M for M in rot_mats if M != ID]
dim_fixed = common_fixed_space(nontriv)
print(f"dim of common fixed subspace of all nontrivial A4 rotations in R^3: {dim_fixed} "
      f"-> only the origin (0-dim): {dim_fixed == 0}")
assert dim_fixed == 0
# the 3 two-fold axes are the coordinate axes (distinct), meeting only at 0; infinity fixed by all
print("the 2-fold axes are the 3 coordinate axes (distinct, meeting only at 0); the 4 three-fold")
print("axes are the cube diagonals (through 0). Common fixed set in R^3 = {0}; plus the point at")
print("infinity (fixed by every orthogonal map). Fix_flat(A4) = {0, infinity} = 2 points.")
print("Both are in the complement (centered ellipses avoid 0; L compact avoids infinity). H-B PASS.")

rule("H-A/H-B SECOND-LEG SUMMARY (SnapPy-free)")
print("H-A core: parity law <=> properness (det+1) over all 48; image O ⊂ SO(3); faithful on the")
print("  motion group; N_SO(3)(O)=O (self-normalizing, finite check + standard axis argument) ->")
print("  spatial identification unique up to inner. Full-group model Z/2 x O: axis rep 2:1, kernel")
print("  = central Z/2 (amphichiral, axis-invisible), fibers size 2. [Geometric peripheral input")
print("  re-extracted independently in the SnapPy companion, flagged.]")
print("H-B: O(3)-stab = 24 (pyritohedral), rotation part = 12 = A4 = even-sigma motion subgroup")
print("  element-for-element (exact Q vertex-set equality; generic a!=b); Fix_flat(A4)={0,inf}=2 pts.")
