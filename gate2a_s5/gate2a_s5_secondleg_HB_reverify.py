"""G-2a-S5 SECOND LEG (CC) -- H-B RE-VERIFICATION of the errata-class canon correction.

The chat-side leg (g_2a_s5_chatleg.py) reported that §2.85 Part C's mechanism sentence
"the V4 kernel preserves each kernel individually" is FALSE at the kernel level: V4 fixes
each ZD *element* but permutes the SIX distinct line kernels. A canon sentence declared
false warrants an independent second leg. Chat filed a re-verification spec (framework data
only, zero shared code); this is that leg.

INDEPENDENCE:
  - The chat leg computed kernels over the prime field F_911.  This leg uses EXACT rationals
    (Fraction over Q) -- a different field, so any agreement cannot be a modular artifact.
  - All linear algebra (nullspace, rank, subspace equality/membership) is written fresh here.
  - Shared only as FRAMEWORK DATA (not code): the CD convention (a,b)(c,d)=(ac-conj(d)b, da+b conj(c)),
    the line L={1,2,3}, the twelve ZD labels e_a +- e_{b+8}, and the doubled transvection action.

Verdict targets (from the filed spec) -- each INDEPENDENTLY reproduced or challenged below:
  (1) each of the 12 labels e_a +- e_{b+8} has a dim-4 left-kernel;
  (2) exactly 6 DISTINCT kernels, 2 labels each, with the stated +/- pairing;
  (3) V4 fixes each ZD element but PERMUTES the six kernels:
      t1:(K0 K1)(K4 K5) fix K2,K3 ; t2:(K2 K3)(K4 K5) fix K0,K1 ; t3:(K0 K1)(K2 K3) fix K4,K5;
  (4) pattern: t_d fixes the two kernels of the pair {a,b} with a^b = m(d), m=(1->2->3->1);
  (5) headline R1 SURVIVES: all 24 Stab(L) elements preserve U(L)=span(6 kernels), dim 8;
  (6) each t_d is an involution on U(L) with eigdims (+1:4,-1:4); pairwise +1-meet = 2 (the 2.triv).
"""
from fractions import Fraction as Fr
import itertools

def rule(t): print("=" * 70); print(t); print("=" * 70)

# ===================== sedenions over Q (fresh CD build) =====================
def conj(x):
    n = len(x)
    if n == 1: return x[:]
    h = n // 2
    return conj(x[:h]) + [-t for t in x[h:]]
def cd(x, y):                     # framework convention (a,b)(c,d)=(ac-conj(d)b, da+b conj(c))
    n = len(x)
    if n == 1: return [x[0] * y[0]]
    h = n // 2
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    ac = cd(a, c); Db = cd(conj(d), b)
    left = [ac[i] - Db[i] for i in range(h)]
    da = cd(d, a); bC = cd(b, conj(c))
    right = [da[i] + bC[i] for i in range(h)]
    return left + right
N = 16
def basis(i):
    v = [Fr(0)] * N; v[i] = Fr(1); return v
E = [basis(i) for i in range(N)]
# sanity: octonion XOR structure e_i e_j = +- e_{i^j} for i,j in 1..7 (low octonion)
def low(i):
    v = [Fr(0)]*N; v[i] = Fr(1); return v
okxor = True
for i in range(1, 8):
    for j in range(1, 8):
        if i == j: continue
        pr = cd(low(i), low(j))
        supp = [k for k in range(N) if pr[k] != 0]
        if supp != [i ^ j]: okxor = False
print(f"sedenions/Q built; octonion e_i e_j = +-e_(i^j) (i,j<8): {okxor}")
assert okxor

# ===================== exact-rational linear algebra =====================
def rref(rows):
    M = [r[:] for r in rows]; R = 0; piv = []
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        pr = next((i for i in range(R, len(M)) if M[i][c] != 0), None)
        if pr is None: continue
        M[R], M[pr] = M[pr], M[R]
        inv = Fr(1) / M[R][c]
        M[R] = [x * inv for x in M[R]]
        for i in range(len(M)):
            if i != R and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[R][j] for j in range(ncol)]
        piv.append(c); R += 1
        if R == len(M): break
    return [M[i] for i in range(R)], piv
def rank(rows):
    return len(rref(rows)[0]) if rows else 0
def nullspace(A):                 # right null space of matrix A (list of rows), over Q
    red, piv = rref(A)
    ncol = len(A[0])
    pivset = set(piv); free = [c for c in range(ncol) if c not in pivset]
    basis_out = []
    for fc in free:
        v = [Fr(0)] * ncol; v[fc] = Fr(1)
        for ri, pc in enumerate(piv):
            v[pc] = -red[ri][fc]
        basis_out.append(v)
    return basis_out
def canon_subspace(vecs):         # canonical key of a subspace = tuple of rref rows
    red, _ = rref(vecs)
    return tuple(tuple(row) for row in red)
def in_span(v, vecs):
    return rank(vecs + [v]) == rank(vecs)
def subspace_eq(A, B):
    return canon_subspace(A) == canon_subspace(B)

def Lmat(x):                      # matrix (rows) of left multiplication y -> x*y, columns=images of e_j
    cols = [cd(x, E[j]) for j in range(N)]
    return [[cols[j][i] for j in range(N)] for i in range(N)]   # row i, col j

# ===================== (1)+(2) the twelve labels, six kernels =====================
rule("(1)-(2) twelve ZD labels -> dim-4 kernels -> six distinct kernels + pairing")
L = [1, 2, 3]
labels = []                       # (a, s, b) meaning x = e_a + s e_{b+8}
for a in L:
    for b in L:
        if a == b: continue
        for s in (1, -1):
            labels.append((a, s, b))
kernels = {}
for (a, s, b) in labels:
    x = [Fr(0)] * N; x[a] = Fr(1); x[b + 8] = Fr(s)
    ker = nullspace(Lmat(x))
    assert len(ker) == 4, (a, s, b, len(ker))
    kernels[(a, s, b)] = ker
print(f"all {len(labels)} labels have dim-4 left-kernels: True")
# group by canonical subspace
groups = {}
for lab, ker in kernels.items():
    groups.setdefault(canon_subspace(ker), []).append(lab)
print(f"# distinct kernels: {len(groups)} (expect 6)")
assert len(groups) == 6
for key, labs in groups.items():
    assert len(labs) == 2
print("each distinct kernel carries exactly 2 labels (a +/- pairing): True")
# assign K0..K5 by the chat's stated identifications and verify the pairing matches
def lab_str(l): a, s, b = l; return f"e{a}{'+' if s==1 else '-'}e{b+8}"
named = {}   # Kname -> canon key
spec_pairs = {
    "K0": [(1, 1, 2), (2, -1, 1)],   # ker(e1+e10)=ker(e2-e9)
    "K1": [(1, -1, 2), (2, 1, 1)],   # ker(e1-e10)=ker(e2+e9)
    "K2": [(1, 1, 3), (3, -1, 1)],   # ker(e1+e11)=ker(e3-e9)
    "K3": [(1, -1, 3), (3, 1, 1)],   # ker(e1-e11)=ker(e3+e9)
    "K4": [(2, 1, 3), (3, -1, 2)],   # ker(e2+e11)=ker(e3-e10)
    "K5": [(2, -1, 3), (3, 1, 2)],   # ker(e2-e11)=ker(e3+e10)
}
ok_pairs = True
for name, pair in spec_pairs.items():
    k0 = canon_subspace(kernels[pair[0]]); k1 = canon_subspace(kernels[pair[1]])
    same = (k0 == k1)
    named[name] = k0
    print(f"  {name}: ker({lab_str(pair[0])}) == ker({lab_str(pair[1])}) : {same}")
    ok_pairs = ok_pairs and same
assert ok_pairs
assert len(set(named.values())) == 6, "named kernels not all distinct!"
print("stated +/- pairing K0..K5 reproduced EXACTLY over Q: True")
Kbasis = {name: kernels[spec_pairs[name][0]] for name in spec_pairs}   # a basis per kernel
Knames = ["K0", "K1", "K2", "K3", "K4", "K5"]

# ===================== transvections, doubled action =====================
def gl32_transvection(d):
    # t_d(x) = x + f(x) d, f = the L-functional = top bit (bit 2); kernel = L = {1,2,3}
    def t(v):
        f = (v >> 2) & 1
        return v ^ d if f == 1 else v
    return t
def perm16_from_pointperm(pointmap):
    # pointmap: dict on 1..7 ; doubled to 9..15, fixes 0 and 8
    P = [[Fr(0)] * N for _ in range(N)]
    P[0][0] = Fr(1); P[8][8] = Fr(1)
    for k in range(1, 8):
        P[pointmap[k]][k] = Fr(1)
        P[pointmap[k] + 8][k + 8] = Fr(1)
    return P
def apply_P(P, v):
    return [sum(P[i][j] * v[j] for j in range(N)) for i in range(N)]
Tpoint = {}
for d in L:
    t = gl32_transvection(d)
    Tpoint[d] = {k: t(k) for k in range(1, 8)}
print("\noff-line action of the three transvections (should be (45)(67),(46)(57),(47)(56)):")
for d in L:
    off = {k: Tpoint[d][k] for k in (4, 5, 6, 7)}
    print(f"  t_{d}: fixes L pointwise={all(Tpoint[d][k]==k for k in L)}; off-line {off}")
Pmat = {d: perm16_from_pointperm(Tpoint[d]) for d in L}

# ===================== (3) V4 fixes each ZD element but permutes the kernels =====================
rule("(3) V4 fixes each ZD element; induced permutation of the six kernels")
# fixes each ZD element:
fixes_elements = True
for (a, s, b) in labels:
    x = [Fr(0)] * N; x[a] = Fr(1); x[b + 8] = Fr(s)
    for d in L:
        if apply_P(Pmat[d], x) != x:
            fixes_elements = False
print(f"every t_d fixes every ZD element e_a+-e_(b+8): {fixes_elements}  (a,b in L; indices 1,2,3,9,10,11 fixed)")
assert fixes_elements
# induced permutation on {K0..K5}:
def kernel_image_name(P, name):
    img = [apply_P(P, v) for v in Kbasis[name]]
    for nm in Knames:
        if subspace_eq(img, Kbasis[nm]):
            return nm
    return "OUTSIDE"
induced = {}
for d in L:
    perm = {nm: kernel_image_name(Pmat[d], nm) for nm in Knames}
    induced[d] = perm
    # express as cycle string
    fixed = [nm for nm in Knames if perm[nm] == nm]
    moved = [(nm, perm[nm]) for nm in Knames if perm[nm] != nm]
    print(f"  t_{d}: {perm}")
    print(f"        fixes {fixed}; moves {moved}")
# check against spec
spec_perm = {
    1: {"K0": "K1", "K1": "K0", "K4": "K5", "K5": "K4", "K2": "K2", "K3": "K3"},
    2: {"K2": "K3", "K3": "K2", "K4": "K5", "K5": "K4", "K0": "K0", "K1": "K1"},
    3: {"K0": "K1", "K1": "K0", "K2": "K3", "K3": "K2", "K4": "K4", "K5": "K5"},
}
match3 = all(induced[d] == spec_perm[d] for d in L)
print(f"\ninduced kernel permutations match the chat spec exactly: {match3}")
assert match3
print("=> §2.85 Part C 'preserves each kernel individually' is FALSE (kernels are permuted).")
print("   CC INDEPENDENTLY CONFIRMS the errata-class correction over Q.")

# ===================== (4) the m-cycle pattern =====================
rule("(4) pattern: t_d fixes the pair {a,b} with a^b = m(d), m=(1->2->3->1)")
pair_of = {"K0": (1, 2), "K1": (1, 2), "K2": (1, 3), "K3": (1, 3), "K4": (2, 3), "K5": (2, 3)}
for d in L:
    fixed = [nm for nm in Knames if induced[d][nm] == nm]
    xors = sorted({pair_of[nm][0] ^ pair_of[nm][1] for nm in fixed})
    print(f"  t_{d} fixes kernels {fixed} = pair(s) with a^b in {xors}  -> m({d}) = {xors[0] if len(xors)==1 else xors}")
m = {d: (sorted({pair_of[nm][0] ^ pair_of[nm][1] for nm in Knames if induced[d][nm]==nm})[0]) for d in L}
print(f"m map d -> a^b(fixed) = {m}  (expect {{1:2, 2:3, 3:1}} = the 3-cycle 1->2->3->1)")
assert m == {1: 2, 2: 3, 3: 1}
print("m-cycle (1->2->3->1) reproduced. (Provenance uninterpreted, R3.)")

# ===================== (5) headline R1: all 24 Stab(L) preserve U(L) =====================
rule("(5) headline R1: all 24 Stab(L) elements preserve U(L) (dim 8)")
UL = []
for nm in Knames: UL += Kbasis[nm]
dimUL = rank(UL)
print(f"dim U(L) = span of six kernels = {dimUL} (expect 8)")
assert dimUL == 8
# build all of GL(3,2) as point permutations, take Stab(L), double, check U(L)-invariance
def all_gl32_pointperms():
    # invertible linear maps on F2^3 <-> ways to permute 7 points that come from a matrix.
    # build from images of basis e1=1(001),e2=2(010),e4=4(100): any invertible assignment.
    perms = []
    bvecs = [1, 2, 4]
    for imgs in itertools.permutations(range(1, 8), 3):
        # linear extension: matrix columns = images of e1,e2,e4
        col = {1: imgs[0], 2: imgs[1], 4: imgs[2]}
        # check invertible: images of the 3 basis vectors independent <=> span all
        def lin(v):
            r = 0
            if v & 1: r ^= col[1]
            if v & 2: r ^= col[2]
            if v & 4: r ^= col[4]
            return r
        vals = {lin(v) for v in range(1, 8)}
        if len(vals) == 7:
            perms.append({v: lin(v) for v in range(1, 8)})
    return perms
GL = all_gl32_pointperms()
StabL = [pm for pm in GL if {pm[x] for x in L} == set(L)]
print(f"|GL(3,2)| = {len(GL)}, |Stab(L)| = {len(StabL)} (expect 168, 24)")
assert len(GL) == 168 and len(StabL) == 24
all_preserve = True
for pm in StabL:
    P = perm16_from_pointperm(pm)
    imgUL = [apply_P(P, v) for v in UL]
    if not subspace_eq(imgUL, UL):
        all_preserve = False
print(f"all 24 Stab(L) elements preserve U(L) as a subspace: {all_preserve}")
assert all_preserve
print("=> headline R1 SURVIVES the correction: U(L)-invariance holds for all 24 (mechanism: they")
print("   permute the six kernels among themselves; invariance does NOT require Stab(L) c Aut(S)).")

# ===================== (6) eigenstructure of each t_d on U(L) =====================
rule("(6) each t_d: involution on U(L), eigdims (+1:4,-1:4); pairwise +1-meet = 2 (2.triv)")
def restrict_matrix(P, spanbasis):
    red, piv = rref(spanbasis)            # canonical basis rows of the subspace
    dim = len(red)
    pivcols = piv
    R = [[Fr(0)] * dim for _ in range(dim)]
    for k in range(dim):
        img = apply_P(P, red[k])
        # coordinates of img in the rref basis: since basis rows are rref, coord_j = img[pivcols[j]]
        for j in range(dim):
            R[j][k] = img[pivcols[j]]
        # verify reconstruction
        recon = [Fr(0)] * N
        for j in range(dim):
            recon = [recon[t] + R[j][k] * red[j][t] for t in range(N)]
        assert recon == img, "restriction reconstruction failed (subspace not invariant?)"
    return R, red, pivcols
def eig_dim(R, val):
    dim = len(R)
    M = [[R[i][j] - (val if i == j else 0) for j in range(dim)] for i in range(dim)]
    return dim - rank(M)
def eigspace(R, val, red):
    dim = len(R)
    M = [[R[i][j] - (val if i == j else 0) for j in range(dim)] for i in range(dim)]
    coeffs = nullspace(M)            # vectors in coordinate space
    # lift to ambient
    out = []
    for cvec in coeffs:
        v = [Fr(0)] * N
        for j in range(dim):
            v = [v[t] + cvec[j] * red[j][t] for t in range(N)]
        out.append(v)
    return out
plus_spaces = {}
for d in L:
    R, red, _ = restrict_matrix(Pmat[d], UL)
    R2 = [[sum(R[i][k]*R[k][j] for k in range(len(R))) for j in range(len(R))] for i in range(len(R))]
    invol = all(R2[i][j] == (1 if i == j else 0) for i in range(len(R)) for j in range(len(R)))
    dp, dm = eig_dim(R, 1), eig_dim(R, -1)
    plus_spaces[d] = eigspace(R, 1, red)
    print(f"  t_{d}: involution on U(L): {invol}; eigdim(+1)={dp}, eigdim(-1)={dm}")
    assert invol and dp == 4 and dm == 4
print("\npairwise intersection of (+1)-eigenspaces (predict 2 = the 2.triv part):")
for d, e in itertools.combinations(L, 2):
    A, B = plus_spaces[d], plus_spaces[e]
    inter = rank(A) + rank(B) - rank(A + B)
    print(f"  dim( eig+1(t_{d}) ∩ eig+1(t_{e}) ) = {inter}")
    assert inter == 2
print("all pairwise +1-intersections = 2 -> the common 2.triv; each t_d additionally fixes the")
print("chi_d line in each std3 copy and negates the other two. Dictionary CONFIRMED (two legs).")

# ===================== summary =====================
rule("H-B RE-VERIFICATION SUMMARY (CC, exact over Q)")
print("(1) 12 labels -> dim-4 kernels: CONFIRMED")
print("(2) exactly 6 distinct kernels, stated +/- pairing: CONFIRMED")
print("(3) V4 fixes each ZD element but PERMUTES the six kernels")
print("    t1:(K0 K1)(K4 K5), t2:(K2 K3)(K4 K5), t3:(K0 K1)(K2 K3): CONFIRMED")
print("    => §2.85 Part C 'preserves each kernel individually' is FALSE -- errata CONFIRMED (2 legs)")
print("(4) m-cycle d->a^b(fixed) = (1->2->3->1): CONFIRMED")
print("(5) headline R1 survives: all 24 Stab(L) preserve U(L) (dim 8): CONFIRMED")
print("(6) each t_d involution, eigdims (4,4), pairwise +1-meet 2: CONFIRMED")
print("Independence: exact Q vs chat's F_911; fresh linear algebra; only framework data shared.")
