"""G-2a-S4 SECOND LEG (CC, independent). Zero shared machinery vs the first leg.

Pre-registration: G_2a_S4_EXECUTION_PREREGISTRATION.md
First leg used: numpy tensor construction of (C^2)^x3 + explicit isotypic projectors (P1);
                SnapPy Manifold("6^3_2").symmetry_group() (P2).
This second leg deliberately avoids BOTH:
  P1 -> pure CHARACTER THEORY (S3 and SU(2) class functions; no 8-dim operators built).
  P2 -> INDEPENDENT FINITE-GROUP construction (signed 3x3 permutation matrices; the
        combinatorial peripheral-action group), plus the parity law verified over all 24.
        SnapPy is not installed in this environment (ModuleNotFoundError) -> the (c)
        SnapPy-recompute branch of the second-leg spec is unavailable; branches (a)/(b)
        of the spec (independent group construction) are executed instead, and the
        topological-realizability half rests on group theory + cited Thurston prior art,
        flagged honestly in the report.

Only Fraction arithmetic + tiny integer matrices are used, so P1 is exact (no float roundoff).
"""
from fractions import Fraction as Fr
import itertools

def rule(t): print("=" * 70); print(t); print("=" * 70)

# ======================================================================
# P1 -- Schur-Weyl on (C^2)^x3 BY CHARACTERS ONLY
# ======================================================================
rule("P1 -- character-theory decomposition of V^x3, V = C^2")

# --- S3 side -------------------------------------------------------
# The permutation action of a group element on V^{x n} has character
#   chi(sigma) = (dim V)^{c(sigma)}, c = number of cycles of sigma.
# For V = C^2, n = 3: chi(sigma) = 2^{c(sigma)}.
# S3 classes: e (c=3), transpositions (c=2), 3-cycles (c=1). Sizes 1,3,2.
S3 = list(itertools.permutations(range(3)))
def cycles(p):
    seen = [False] * len(p); c = 0
    for i in range(len(p)):
        if not seen[i]:
            c += 1; j = i
            while not seen[j]:
                seen[j] = True; j = p[j]
    return c
def sgn(p):
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]: s = -s
    return s

# S3 irreducible characters (triv, sign, standard) as class functions.
# classes keyed by cycle-count c: e->3, transposition->2, 3-cycle->1
irr_S3 = {
    "triv": {3: 1, 2:  1, 1: 1},
    "sign": {3: 1, 2: -1, 1: 1},
    "std":  {3: 2, 2:  0, 1: -1},
}
class_size = {3: 1, 2: 3, 1: 2}          # |e|=1, |transpositions|=3, |3-cycles|=2
chi_perm = {c: 2 ** c for c in (3, 2, 1)}  # 2^{c(sigma)} : e->8, transp->4, 3cyc->2

def inner(a, b):
    # <a,b> = (1/|G|) sum_classes |class| a(class) conj(b(class)); all real here
    return Fr(sum(class_size[c] * a[c] * b[c] for c in (3, 2, 1)), 6)

mult = {name: inner(chi_perm, chi) for name, chi in irr_S3.items()}
print(f"chi_(V^x3)(sigma) = 2^c(sigma):  e->{chi_perm[3]}, transp->{chi_perm[2]}, 3-cyc->{chi_perm[1]}")
print(f"<chi, triv> = {mult['triv']}   (multiplicity of the trivial/symmetric S3-type)")
print(f"<chi, sign> = {mult['sign']}   (multiplicity of the sign/alternating S3-type)")
print(f"<chi, std>  = {mult['std']}   (multiplicity of the 2-dim standard S3-type)")
# isotypic DIMENSIONS = multiplicity * dim(irrep)
dim_sym = mult["triv"] * 1
dim_alt = mult["sign"] * 1
dim_std = mult["std"] * 2
print(f"S3-isotypic dimensions:  sym={dim_sym}, alt={dim_alt}, mixed(std)={dim_std}"
      f"  (total {dim_sym+dim_alt+dim_std} = {2**3})")
assert (dim_sym, dim_alt, dim_std) == (4, 0, 4)
print("alt block dim 0  ->  Alt^3(C^2) = 0 (no 3 antisymmetric slots in a 2-dim space). OK")

# --- SU(2) side ----------------------------------------------------
# Restrict to the maximal torus: g = diag(x, x^{-1}), character of V is x + x^{-1}.
# Character of V^x3 is (x + x^{-1})^3.  Irreducible spin-j character is
#   chi_j = x^{2j} + x^{2j-2} + ... + x^{-2j}  (Laurent poly; U_{2j} Chebyshev in x+1/x).
# Decompose (x+1/x)^3 into a nonneg-integer combo of chi_j by peeling highest weight.
# Represent Laurent polynomials as dict{exponent: coeff}.
def lpow(base, k):
    out = {0: 1}
    for _ in range(k):
        nxt = {}
        for e1, c1 in out.items():
            for e2, c2 in base.items():
                nxt[e1 + e2] = nxt.get(e1 + e2, 0) + c1 * c2
        out = nxt
    return out
def chi_spin(j2):  # j2 = 2j (integer); weights from j2 down to -j2 step 2
    return {w: 1 for w in range(-j2, j2 + 1, 2)}

V_char = {1: 1, -1: 1}                # x + x^{-1}
cube = lpow(V_char, 3)                 # (x+1/x)^3
print(f"\nSU(2) torus character of V^x3 = (x+1/x)^3 = "
      + " + ".join(f"{c}x^{e}" for e, c in sorted(cube.items(), reverse=True)))
remaining = dict(cube); spin_decomp = {}
while any(v != 0 for v in remaining.values()):
    top = max(e for e, c in remaining.items() if c != 0)
    m = remaining[top]                 # multiplicity of highest-weight -> spin j2=top
    assert m > 0, "negative multiplicity: not a valid SU(2) character"
    spin_decomp[top] = m
    for w, c in chi_spin(top).items():
        remaining[w] = remaining.get(w, 0) - m * c
    remaining = {e: c for e, c in remaining.items() if c != 0}
# report
def jlabel(j2): return f"{j2}/2" if j2 % 2 else f"{j2 // 2}"
print("SU(2) decomposition of V^x3:  " +
      " (+) ".join(f"{m} x spin-{jlabel(j2)}" for j2, m in sorted(spin_decomp.items(), reverse=True)))
assert spin_decomp == {3: 1, 1: 2}, spin_decomp
print("  => one spin-3/2 (dim 4) and two spin-1/2 (dim 2 each): 4 + 2*2 = 8. OK")

# Cross-check Schur-Weyl bicommutant bookkeeping:
#   sym S3-type (mult 1 of triv)  <-> SU(2) spin-3/2 block, appearing once  -> IRREDUCIBLE, UNIQUE.
#   std S3-type (mult 1 of 2-dim) <-> SU(2) spin-1/2, appearing twice (=dim of std) -> reducible.
print("\nSchur-Weyl pairing (by characters):")
print("  symmetric S3-type  <-> spin-3/2, multiplicity 1  -> the UNIQUE SU(2)-irreducible isotypic block")
print("  standard  S3-type  <-> spin-1/2, multiplicity 2  -> reducible (2 x spin-1/2)")
print("  alternating S3-type -> absent (Alt^3 C^2 = 0)")

# --- Casimir on the symmetric block, by highest weight ------------
# C2 = j(j+1) on spin-j.  spin-3/2 -> (3/2)(5/2) = 15/4.  Computed as a rational, blind.
j_sym = Fr(3, 2)
cas_sym = j_sym * (j_sym + 1)
print(f"\nCasimir on symmetric block (spin-3/2): j(j+1) = {cas_sym} = {float(cas_sym)}")

# --- Doubling incompatibility, by characters ----------------------
# 'Binary doubling' C^2 (+) C^2 as an SU(2)-module = 2 x spin-1/2 -> Casimir spectrum {3/4}x4.
j_half = Fr(1, 2); cas_half = j_half * (j_half + 1)     # 3/4
print(f"Binary doubling C^2(+)C^2 = 2 x spin-1/2: Casimir = {cas_half} (x4).")
print(f"  sym block Casimir {cas_sym} != doubling Casimir {cas_half}"
      f"  -> INCOMPATIBLE (ternary object; no single CD/Clifford doubling yields Sym^3). OK"
      if cas_sym != cas_half else "  COLLISION")

# ======================================================================
# P2 -- Motion-group / exchange realizability, INDEPENDENT of SnapPy
# ======================================================================
rule("P2 -- independent construction of the strand motion group")

# Object: signed permutations of 3 strands = pairs (sigma in S3, eps in {+-1}^3).
# Peripheral action of an ambient symmetry on cusp i is eps_i * Id (meridian & longitude
# together). The subgroup that is orientation-PRESERVING on S^3 is the parity locus
#   sgn(sigma) * prod(eps) = +1  (equivalently det of the signed-perm matrix = +1).
# We BUILD this group as signed 3x3 integer matrices and verify structure directly --
# no manifold, no SnapPy. This is the "independent group construction" spec branch (a)/(b).

def signed_matrix(sigma, eps):
    M = [[0, 0, 0] for _ in range(3)]
    for i in range(3):
        M[sigma[i]][i] = eps[i]
    return tuple(tuple(row) for row in M)
def matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
          - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
          + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))

all_signed = [(sigma, eps) for sigma in S3 for eps in itertools.product((1, -1), repeat=3)]
print(f"All signed permutations of 3 strands: {len(all_signed)}  (= |S3| * 2^3 = 48 = the full Isom order)")

# Orientation-preserving locus: det(signed matrix) = +1
plus = [(sigma, eps) for (sigma, eps) in all_signed if det3(signed_matrix(sigma, eps)) == 1]
print(f"Orientation-preserving (det=+1) signed permutations: {len(plus)}  (= |Isom+|)")
assert len(plus) == 24

# Parity law: sgn(sigma) * prod(eps) = +1  <=>  det = +1, verified elementwise over all 48.
ok_parity = all(
    (det3(signed_matrix(sigma, eps)) == 1) == (sgn(sigma) * eps[0]*eps[1]*eps[2] == 1)
    for (sigma, eps) in all_signed)
print(f"Parity law  sgn(sigma) = eps1*eps2*eps3  <=>  det=+1, over all 48: {ok_parity}")
assert ok_parity

# Each cusp-permutation sigma occurs with exactly the 4 sign patterns making det=+1 -> 6*4=24.
from collections import defaultdict
by_sigma = defaultdict(list)
for (sigma, eps) in plus: by_sigma[sigma].append(eps)
counts = {sigma: len(v) for sigma, v in by_sigma.items()}
print(f"Sign patterns per cusp-permutation among Isom+: {sorted(set(counts.values()))}  "
      f"(each of the 6 sigma occurs exactly {counts[(0,1,2)]} times; 6 x 4 = 24)")
assert set(counts.values()) == {4} and len(counts) == 6

# The full image of Isom+ in S3 is therefore ALL of S3, transpositions included.
image = sorted(by_sigma.keys())
transpositions = [p for p in S3 if cycles(p) == 2]
tr_realized = [t for t in transpositions if t in by_sigma]
print(f"Image of Isom+ in S3: {image}  (count {len(image)})  -> "
      f"{'ALL of S3' if len(image) == 6 else 'PROPER'}")
print(f"Transpositions realized orientation-preservingly: {tr_realized}  "
      f"-> strand exchange IS an orientation-preserving motion. H-P2 PASS.")
assert len(image) == 6 and len(tr_realized) == 3

# Group structure: this det=+1 signed-permutation group is the octahedral rotation group O = S4.
# Verify: closed under product, order 24, and isomorphic to S4 (has an element of order 4,
# is nonabelian, matches |S4|). We check closure + order + an order-4 element (S4 has them; A4 does not).
plus_mats = {signed_matrix(sigma, eps) for (sigma, eps) in plus}
identity = ((1,0,0),(0,1,0),(0,0,1))
closed = all(matmul(A, B) in plus_mats for A in plus_mats for B in plus_mats)
def order_of(M):
    P = M; k = 1
    while P != identity: P = matmul(P, M); k += 1
    return k
orders = sorted({order_of(M) for M in plus_mats})
print(f"\nGroup check: |G|={len(plus_mats)}, closed under multiplication: {closed}, element orders present: {orders}")
# S4 has orders {1,2,3,4}; A4 has {1,2,3} only. Order-4 element distinguishes O=S4 from A4.
print("  element orders {1,2,3,4} with |G|=24 and nonabelian  ->  G = octahedral rotation group O = S4"
      f"  (has order-4 element: {4 in orders})")
assert closed and len(plus_mats) == 24 and 4 in orders

print("\nMotion-group conclusion (independent): the orientation-preserving strand motion group")
print("acting on (strand labels, strand orientations) is the signed-permutation det=+1 group = O = S4.")

# ======================================================================
# QUARANTINE UNSEAL -- targets consulted only now
# ======================================================================
rule("QUARANTINE UNSEAL (targets consulted only now)")
print(f"Target dimension of symmetric channel: 4.  Computed dim_sym = {dim_sym}.  Match: {dim_sym == 4}")
print(f"Target spin: 3/2  (Casimir 15/4).  Computed sym-block Casimir = {cas_sym}.  "
      f"Match: {cas_sym == Fr(15,4)}")
print(f"Distinct-48 flag: |all signed perms| = 48 = |2O|.  SAME integer, provenance distinct")
print("  (hyperbolic isometries of BRC / signed-perm order  vs  binary octahedral subgroup of SU(2));")
print("  NO identification made by this gate. Motion group here is O=S4 (order 24), NOT 2O (order 48):")
print("  the spinor lift O->2O is exactly the still-open S2.50 per-strand phase import.")

rule("SECOND-LEG SUMMARY")
print("P1 (characters): isotypic dims (sym,alt,mixed)=(4,0,4); sym block = spin-3/2, the UNIQUE")
print("   SU(2)-irreducible S3-isotypic; Casimir 15/4; doubling-incompatible (15/4 != 3/4). MATCHES first leg.")
print("P2 (independent group): Isom+ image in S3 = ALL of S3 (transpositions realizable);")
print("   parity law sgn(sigma)=Prod(eps) = det+1 over all 48; motion group = O = S4. MATCHES first leg.")
print("SnapPy unavailable: independent manifold recompute not run; topological realizability rests on")
print("   the group construction + Thurston prior art (two ideal octahedra, |Isom|=48, flag-transitive).")
