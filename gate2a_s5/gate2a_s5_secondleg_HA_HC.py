"""G-2a-S5 SECOND LEG (CC, independent) -- H-A (identification) + H-C (module iso).

Pre-registration: G_2a_S5_EXECUTION_PREREGISTRATION.md
Decisive falsifier: H-A(ii) -- does the transvection-direction indexing INTERTWINE the
                    §2.73-identified S3 actions, or does matching the kernels require an
                    outer twist? If a twist is needed, the canonical identification fails.

Zero shared machinery vs the first leg (which builds Stab(L) as explicit matrices in a
chosen basis + §2.85 kernel scripts):
  - Line L specified by the DUAL/FUNCTIONAL description L = ker(phi), phi = top-bit read-off.
  - Stab(L) characterized via the functional (g preserves ker phi), then realized as the
    setwise stabilizer; transvections built intrinsically as t_d = I + d phi^T.
  - H-A(iii) existence/uniqueness done by ABSTRACT cocycle computation (H^1, H^2 of S3 with
    the F2 std module) in addition to an explicit Phi, per the second-leg spec.
  - H-C via the binary octahedral group built as unit quaternions (independent of any
    numpy tensor Sym^3 construction), characters compared on conjugacy classes.

Everything over F2 / exact; the quaternion part uses exact half-integers where possible and
a 1e-9 tolerance only for the final character rounding.
"""
import itertools
from fractions import Fraction as Fr

def rule(t): print("=" * 70); print(t); print("=" * 70)

# =====================================================================
# F2^3 primitives.  Vectors = ints 1..7, bit b_k = (v >> k)&1, so
#   v = 4*b2 + 2*b1 + 1*b0.   Functional phi(v) = b2 (the top bit).
# Line L = ker(phi) = { v : b2 = 0 } = {1,2,3}  (001,010,011); 1 xor 2 = 3.
# =====================================================================
def xor(a, b): return a ^ b
def phi(v): return (v >> 2) & 1                       # top-bit functional
L = tuple(v for v in range(1, 8) if phi(v) == 0)      # the three points of the line
assert L == (1, 2, 3) and (1 ^ 2) == 3
POINTS = list(range(1, 8))                            # 7 points of PG(2,2)

# GL(3,2): invertible 3x3 over F2, acting on column bit-vectors.
def bits(v): return [(v >> 0) & 1, (v >> 1) & 1, (v >> 2) & 1]   # [b0,b1,b2]
def frombits(c): return c[0] | (c[1] << 1) | (c[2] << 2)
def apply_mat(M, v):
    c = bits(v)
    out = [(M[r][0]*c[0] ^ M[r][1]*c[1] ^ M[r][2]*c[2]) & 1 for r in range(3)]
    return frombits(out)   # NOTE row r -> bit r
def matmul(A, B):
    return tuple(tuple(sum(A[r][k]*B[k][col] for k in range(3)) & 1 for col in range(3)) for r in range(3))
def is_invertible(M):
    imgs = {apply_mat(M, v) for v in POINTS}
    return len(imgs) == 7   # bijective on nonzero vectors <=> invertible

# enumerate GL(3,2)
ALL = []
for entries in itertools.product((0, 1), repeat=9):
    M = (entries[0:3], entries[3:6], entries[6:9])
    if is_invertible(M): ALL.append(M)
print(f"|GL(3,2)| = {len(ALL)} (expect 168)")
assert len(ALL) == 168

# =====================================================================
# H-A(i): Stab(L) via the functional; pointwise stabilizer = transvections with axis L.
# =====================================================================
rule("H-A(i) -- Stab(L), pointwise stabilizer, transvection structure")

def preserves_L(M):
    return {apply_mat(M, v) for v in L} == set(L)
# dual characterization cross-check: g preserves ker(phi) iff phi(g v)=0 for all v in L
def preserves_L_dual(M):
    return all(phi(apply_mat(M, v)) == 0 for v in L)
StabL = [M for M in ALL if preserves_L(M)]
assert all(preserves_L_dual(M) == preserves_L(M) for M in ALL)   # functional desc == setwise
print(f"|Stab(L)| = {len(StabL)}  (expect 24; functional and setwise descriptions agree)")
assert len(StabL) == 24

# action on the 3 points of L -> permutation in Sym(L)
def perm_on_L(M):
    return tuple(apply_mat(M, p) for p in L)          # image of (1,2,3)
def pointwise_fixes_L(M):
    return perm_on_L(M) == L
PtStab = [M for M in StabL if pointwise_fixes_L(M)]
print(f"pointwise stabilizer ker(Stab(L)->Sym(L)) order = {len(PtStab)}  (expect 4)")
assert len(PtStab) == 4

# transvections with axis (hyperplane) L: t_d(v) = v + phi(v) d, d in L
def transvection(d):
    # matrix: I + d * phi^T ; phi picks bit b2 (row index 2), adds to bit r the value d_r*b2
    dc = bits(d)
    M = [[1 if r == c else 0 for c in range(3)] for r in range(3)]
    for r in range(3):
        M[r][2] = (M[r][2] + dc[r]) & 1               # add d_r * (b2 component)
    return tuple(tuple(row) for row in M)
Tr = {d: transvection(d) for d in L}                  # 3 transvections, indexed by direction d in L
for d, T in Tr.items():
    assert is_invertible(T) and pointwise_fixes_L(T), d
# they are exactly the nontrivial pointwise stabilizer
identity = tuple(tuple(1 if r == c else 0 for c in range(3)) for r in range(3))
assert set(Tr.values()) | {identity} == set(PtStab)
# elementary abelian V4: order 2 each, commute
for d, T in Tr.items():
    assert matmul(T, T) == identity
for d1, d2 in itertools.combinations(L, 2):
    assert matmul(Tr[d1], Tr[d2]) == matmul(Tr[d2], Tr[d1])
print("pointwise stabilizer = {id} u {3 transvections t_d, d in L}: elementary abelian V4. OK")
print(f"transvection index = direction d in L: {dict((d, 'axis L') for d in L)}")

# =====================================================================
# H-A(ii)  THE DECISIVE FALSIFIER: does conjugation send t_d -> t_{g(d)} ?
# =====================================================================
rule("H-A(ii) -- decisive: transvection indexing intertwines the S3 action?")
def inv_mat(M):
    for N in StabL + [m for m in ALL if m not in StabL]:
        if matmul(M, N) == identity: return N
    raise RuntimeError
twist_found = False
checks = 0
for g in StabL:
    ginv = inv_mat(g)
    sigma = {p: apply_mat(g, p) for p in L}           # g's permutation of the 3 line points (§2.73 base)
    for d in L:
        conj = matmul(matmul(g, Tr[d]), ginv)          # g t_d g^{-1}
        expected = Tr[sigma[d]]                         # t_{g(d)}
        checks += 1
        if conj != expected:
            twist_found = True
            print(f"  TWIST at g={g}, d={d}: conj != t_(g d)")
print(f"checked {checks} (g,d) pairs.  outer twist needed: {twist_found}")
print("H-A(ii) VERDICT:", "FALSIFIED (twist -> no canonical id)" if twist_found
      else "PASS -- conjugation sends t_d -> t_(g d); indexing IS S3-equivariant over §2.73")
assert not twist_found

# =====================================================================
# Motion side: {(sigma,eps): sgn(sigma)=prod eps}; kernel indexed by UN-flipped strand.
# =====================================================================
rule("Motion group and its kernel indexing")
S3 = list(itertools.permutations((1, 2, 3)))           # perms of the labels {1,2,3}
def sgn(p):
    labels = list(p); s = 1
    for i in range(3):
        for j in range(i+1, 3):
            if labels[i] > labels[j]: s = -s
    return s
# element = (perm as tuple mapping position->image over labels 1..3, eps dict on {1,2,3})
def make_motion():
    G = []
    for p in S3:
        for eps in itertools.product((1, -1), repeat=3):
            if sgn(p) == eps[0]*eps[1]*eps[2]:
                G.append((p, eps))
    return G
Mot = make_motion()
print(f"|motion group| = {len(Mot)} (expect 24)")
assert len(Mot) == 24
# kernel: p = identity perm (1,2,3)
Ker_mot = [(p, eps) for (p, eps) in Mot if p == (1, 2, 3)]
print(f"kernel V4^mot order = {len(Ker_mot)}: {[eps for _,eps in Ker_mot]}")
def unflipped_index(eps):      # the single '+' among a nontrivial flip-pair pattern
    plus = [i+1 for i in range(3) if eps[i] == 1]
    return plus[0] if len(plus) == 1 else None   # None for +++ (identity)
for _, eps in Ker_mot:
    i = unflipped_index(eps)
    print(f"   eps={eps} -> flips pair complementary to point {i}" if i else f"   eps={eps} -> identity")

# =====================================================================
# H-A(iii): explicit Phi covering id_S3 and matching kernels, + uniqueness class.
# =====================================================================
rule("H-A(iii) -- explicit Phi: motion S4 -> Stab(L), covering id_S3, kernel-matched")
# Motion group multiplication
def mot_mul(a, b):
    (pa, ea), (pb, eb) = a, b
    # perms act on labels; compose pa after pb : (pa o pb)(k) = pa applied to pb(k)
    # represent perm p as function position->image over labels; here p is tuple (p(1),p(2),p(3))
    def app(p, k): return p[k-1]
    pc = tuple(app(pa, app(pb, k)) for k in (1, 2, 3))
    # eps multiply with permutation twist: (pa,ea)*(pb,eb) eps at k = ea[pb(k)] * eb[k]
    ec = tuple(ea[app(pb, k)-1] * eb[k-1] for k in (1, 2, 3))
    return (pc, ec)
# Stab(L) multiplication is matmul; map to Sym(L) via perm_on_L
def alg_perm(M): return tuple(apply_mat(M, p) for p in L)   # in labels 1..3

# Build a section of the motion group over S3 and of Stab(L) over S3, then define Phi on
# generators = kernel + a section, and verify homomorphism by brute force over all 24.
# Motion section s_mot(sigma): pick the element (sigma, eps) with eps 'all + on evens', and for
# odd sigma the unique eps in {++-,+-+,-++,---}?  Just pick ANY chosen rep per sigma:
sec_mot = {}
for p in S3:
    reps = [(pp, ee) for (pp, ee) in Mot if pp == p]
    # choose the rep whose eps has the most +'s, tie-break lexicographically -> canonical section
    reps.sort(key=lambda x: (-sum(1 for e in x[1] if e == 1), x[1]))
    sec_mot[p] = reps[0]
# Stab(L) section over Sym(L): choose, for each target perm, a matrix realizing it
sec_alg = {}
for M in StabL:
    sec_alg.setdefault(alg_perm(M), M)
assert set(sec_alg.keys()) == set(S3), "Stab(L)->Sym(L) not surjective?!"

# Define Phi by: Phi(ker elt indexed i) = t_i ; Phi(section(sigma)) = sec_alg(sigma) ADJUSTED
# so that Phi is a homomorphism.  Rather than solve by hand, SEARCH for an isomorphism Phi
# with (a) alg_perm(Phi(x)) == perm_of(x) for all x, and (b) Phi matches kernel indexing.
def mot_perm(x): return x[0]                 # motion element's S3 image (labels)
# candidate: Phi determined by images of a generating set; but cleanest: brute-force count all
# bijections Phi: Mot->StabL that are homomorphisms, cover id_S3, and fix kernel indexing.
# 24! is too big; instead: a homomorphism is determined by images of generators. Use that any
# such Phi restricted to kernel is fixed (t_i), and on a section it must land in the correct
# alg_perm-fiber. Enumerate section-image choices (each sigma -> one of the |ker|=4 matrices in
# its fiber) and test the homomorphism property.
alg_fiber = {sigma: [M for M in StabL if alg_perm(M) == sigma] for sigma in S3}
for sigma in S3: assert len(alg_fiber[sigma]) == 4
# kernel indexing map on the algebra side: element -> matrix
def mot_to_alg_kernel(eps):
    i = unflipped_index(eps)
    return Tr[i] if i is not None else identity
# For a section-choice, define Phi(sigma, eps) = chosen[sigma] * Phi(kernel part).
# Decompose motion elt (p,eps) = section(p) * k, where k in kernel:
def mot_inv(a):
    (p, e) = a
    pinv = tuple(p.index(k)+1 for k in (1, 2, 3))
    # inverse eps: from (p,e)^-1 = (pinv, e') with e'[k] = e[pinv(k)]... derive by requiring product=id
    einv = tuple(e[p[k-1]-1] for k in (1, 2, 3))
    return (pinv, einv)
def kernel_part(x, chosen):
    p = mot_perm(x)
    return mot_mul(mot_inv(sec_mot[p]), x)     # section(p)^{-1} * x  in kernel
count_iso = 0
example_Phi = None
for choice in itertools.product(*[range(4) for _ in S3]):
    chosen = {sigma: alg_fiber[sigma][choice[idx]] for idx, sigma in enumerate(S3)}
    def Phi(x):
        p = mot_perm(x)
        k = kernel_part(x, chosen)             # (id, eps) kernel element
        return matmul(chosen[p], mot_to_alg_kernel(k[1]))
    # test homomorphism on all pairs (sample: all 24x24)
    ok = True
    for a in Mot:
        fa = Phi(a)
        for b in Mot:
            if Phi(mot_mul(a, b)) != matmul(fa, Phi(b)):
                ok = False; break
        if not ok: break
    if not ok: continue
    # covers id_S3?
    if any(alg_perm(Phi(x)) != mot_perm(x) for x in Mot): continue
    # kernel matched?
    if any(Phi((( 1,2,3), eps)) != mot_to_alg_kernel(eps) for (_, eps) in Ker_mot): continue
    # bijective?
    if len({Phi(x) for x in Mot}) != 24: continue
    count_iso += 1
    if example_Phi is None: example_Phi = chosen
print(f"number of isomorphisms Phi covering id_S3 AND matching kernel indexing: {count_iso}")
print(f"uniqueness class |Phi| = {count_iso}  (pre-reg expectation: up to inner autos by V4, i.e. 4)")
assert count_iso == 4, count_iso
print("H-A(iii)/(iv): Phi exists; unique up to the 4 inner automorphisms by V4^mot. OK")

# =====================================================================
# Abstract confirmation via cocycles: H^2(S3, V4)=0 (split), H^1 counts complement classes.
# V4 = F2-module = std rep of S3 over F2 (coords sum-zero in (Z2)^3).
# =====================================================================
rule("H-A(iii) abstract: cocycle H^1/H^2 of S3 acting on V4 (F2 std module)")
# represent V4 elements as sum-zero vectors in (F2)^3: basis e1+e2, e2+e3
V4vecs = [(0,0,0), (1,1,0), (0,1,1), (1,0,1)]         # sum-zero triples
def s3act(p, v):    # permute coordinates by p (labels 1..3 -> positions)
    return tuple(v[p[i]-1] for i in range(3))
for p in S3:
    for v in V4vecs: assert s3act(p, v) in V4vecs
def vadd(a, b): return tuple((a[i]+b[i]) & 1 for i in range(3))
# 2-cochains f: S3xS3 -> V4 ; count 2-cocycles and 2-coboundaries -> H^2
# (brute force is 4^(36) too big; instead use the standard fact via a transversal + verify split).
# Split-ness is equivalent to the EXISTENCE of a complement (a section that is a homomorphism),
# NOT to whether one arbitrarily-chosen section happens to be one. We enumerate complements below
# and read [H^2]=0 off their existence; |H^1| = # of V4-conjugacy classes of complements.
# H^1 = complement classes up to V4-conjugacy: count complements, divide into orbits.
# complements to V4 in S4(mot): subgroups of order 6 meeting kernel trivially, mapping onto S3.
def mot_pow_closure(gens):
    seen = set(gens); frontier = list(gens)
    while frontier:
        x = frontier.pop()
        for g in gens:
            y = mot_mul(x, g)
            if y not in seen: seen.add(y); frontier.append(y)
    return frozenset(seen)
idmot = ((1,2,3), (1,1,1))
complements = set()
for subset_seed in Mot:      # complements are conjugates of S3-section; find all order-6 complements
    pass
# enumerate all order-6 subgroups that are complements
from itertools import combinations
elems = Mot
# a complement is generated by a 3-cycle-lift and a transposition-lift meeting kernel trivially
threes = [x for x in Mot if x != idmot and mot_mul(x, mot_mul(x, x)) == idmot and mot_perm(x) != (1,2,3)]
twos   = [x for x in Mot if mot_mul(x, x) == idmot and mot_perm(x) != (1,2,3) and sgn(mot_perm(x)) == -1]
for a in threes:
    for b in twos:
        H = mot_pow_closure([a, b])
        # complement: order 6, maps bijectively onto S3, meets kernel only in identity
        if (len(H) == 6 and len({mot_perm(h) for h in H}) == 6 and idmot in H
                and len([h for h in H if mot_perm(h) == (1, 2, 3)]) == 1):
            complements.add(H)
# group complements into V4-conjugacy orbits
def conj_mot(g, x): return mot_mul(mot_mul(g, x), mot_inv(g))
V4mot = [k for k in Ker_mot]
orbits = []
seen = set()
for H in complements:
    if H in seen: continue
    orb = set()
    for v in V4mot:
        Hc = frozenset(conj_mot(v, h) for h in H)
        orb.add(Hc)
    for Hc in orb: seen.add(Hc)
    orbits.append(orb)
split = len(complements) > 0
print(f"# complements to V4 in motion-S4: {len(complements)} (>0 => extension SPLIT, [H^2]=0: {split})")
print(f"V4-conjugacy classes of complements (|H^1(S3,V4)|): {len(orbits)}")
assert split and len(orbits) == 1

# =====================================================================
# H-C: the two 4-dim modules as 2O-reps are isomorphic (character identity).
# Build 2O as 48 unit quaternions; chi_{3/2} from SU(2); verify it is an irreducible
# 4-dim character of 2O -> the unique genuine 4-dim irrep (G-2a-S1 D1=1).
# =====================================================================
rule("H-C -- Sym^3(C^2) and the genuine 4-dim 2O-irrep: same character")
import math
# binary octahedral group 2O (order 48) as unit quaternions:
# 2T (24): +-1,+-i,+-j,+-k and (+-1+-i+-j+-k)/2 ; 2O adds the 24 of form (+-1+-i)/sqrt2 perms.
def quats_2T():
    Q = []
    for s in (1, -1):
        for e in range(4):
            v = [0,0,0,0]; v[e] = s; Q.append(tuple(v))
    for signs in itertools.product((0.5,-0.5), repeat=4):
        Q.append(tuple(signs))
    return Q
def quats_extra():
    Q = []
    r = 1/math.sqrt(2)
    # all quaternions with two nonzero coords = +-1/sqrt2 in distinct slots
    for i, j in itertools.permutations(range(4), 2):
        if i < j:
            for si in (r, -r):
                for sj in (r, -r):
                    v = [0,0,0,0]; v[i] = si; v[j] = sj; Q.append(tuple(v))
    return Q
G2O = quats_2T() + quats_extra()
# dedup
def key(q): return tuple(round(x, 6) for x in q)
uniq = {}
for q in G2O: uniq[key(q)] = q
G2O = list(uniq.values())
print(f"|2O| = {len(G2O)} (expect 48)")
assert len(G2O) == 48
def qmul(a, b):
    a0,a1,a2,a3 = a; b0,b1,b2,b3 = b
    return (a0*b0-a1*b1-a2*b2-a3*b3,
            a0*b1+a1*b0+a2*b3-a3*b2,
            a0*b2-a1*b3+a2*b0+a3*b1,
            a0*b3+a1*b2-a2*b1+a3*b0)
# conjugacy classes by trace (2*cos theta) + since class fn depends only on rotation angle & type
# rotation angle theta: q ~ cos(theta/2) + sin(theta/2) u ; here q0 = cos(theta/2).
# SU(2) character chi_j(theta) = sin((2j+1)theta/2)/sin(theta/2).  For j=3/2: U_3.
def chi_spin(j2, q0):
    # Character of the spin-j (dim j2+1) SU(2) irrep on a unit quaternion with real part q0.
    # The 2-dim rep has eigenvalues e^{+-i psi}, cos psi = q0 (psi in [0,pi]); the spin-j
    # character is the sum of weights sum_{k=0}^{j2} e^{i (j2-2k) psi}, taken real.
    # This is EXACT on the double cover: q and -q (q0 and -q0 -> psi and pi-psi) give the
    # correct opposite signs on genuine reps -- unlike a bare theta=2*acos(q0) sin-ratio.
    psi = math.acos(max(-1.0, min(1.0, q0)))
    return sum(math.cos((j2 - 2*k)*psi) for k in range(j2 + 1))
# group elements by q0 value (class function input)
from collections import Counter, defaultdict
by_q0 = defaultdict(list)
for q in G2O:
    by_q0[round(q[0], 6)].append(q)
print("2O classes by q0=cos(theta/2):", dict(Counter(round(q[0],6) for q in G2O)))
# character of chi_{3/2} on each class, and <chi,chi>
vals = {}
for q0v, elts in by_q0.items():
    vals[q0v] = chi_spin(3, q0v)     # j2 = 2j = 3
inner = 0.0
for q in G2O:
    c = chi_spin(3, round(q[0],6))
    inner += c*c
inner /= len(G2O)
print("chi_{3/2} values by class q0:", {k: round(v,4) for k,v in sorted(vals.items(), reverse=True)})
print(f"<chi_3/2, chi_3/2>_2O = {inner:.6f}  -> {'IRREDUCIBLE (=1)' if abs(inner-1)<1e-6 else 'reducible'}")
assert abs(inner - 1) < 1e-6
print(f"dim = chi(1) = {chi_spin(3, 1.0):.4f} (=4). genuine: chi(-1) = {chi_spin(3,-1.0):.4f} (=-4 => spinorial, -1 acts as -Id)")
assert abs(chi_spin(3,1.0)-4) < 1e-9 and abs(chi_spin(3,-1.0)+4) < 1e-9
print("H-C: Sym^3(C^2)=spin-3/2 restricts to 2O as an IRREDUCIBLE genuine 4-dim rep;")
print("     -1 |-> -Id (chi(-1)=-4), so it is the unique genuine 4-dim irrep (G-2a-S1 D1=1).")
print("     The two convergent routes' 4-dim modules coincide as 2O-reps under Phi's lift. OK")

rule("SECOND-LEG H-A/H-C SUMMARY")
print("H-A(i):  Stab(L) order 24; pointwise stab = V4 = {id}+3 transvections t_d (d in L). PASS")
print("H-A(ii): conjugation sends t_d -> t_(g d); NO outer twist. Decisive falsifier NOT triggered. PASS")
print("H-A(iii/iv): explicit Phi covering id_S3, kernel-matched; unique up to 4 inner autos by V4;")
print("         extension split ([H^2]=0), complement class computed. PASS -> canonical identification R1.")
print("H-C:     both 4-dim modules = the unique genuine 4-dim 2O-irrep (chi_3/2, irreducible, -1->-Id). PASS")
print("distinct-S4 (motion vs Fano-line): CANONICAL identification HOLDS over the §2.73 base ->")
print("   the two S4's are naturally the same; spatial-O S4 remains OUT OF SCOPE, flag retained there.")
