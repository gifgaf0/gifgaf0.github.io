"""
g0_invariants.py — §3.4-G0 first pass: symmetry-allowed interaction structure
=============================================================================
The linchpin of the §3.4 proof program (reports/SQT_3.4_PROOF_PROGRAM.md,
§3.4.3). Before computing any ground state we must enumerate the interaction
terms the framework's established symmetry PERMITS, so the kernel used in MV-G1
is audited rather than assumed. This script does the discrete, verifiable part:
the orbit structure of the Fano collineation group on k-subsets of the 7
octonion-imaginary directions, which fixes the allowed coupling tensors at each
body-order.

SETUP (import I1, declared). Order parameter ψ ∈ ℂ⊗𝕆: a U(1)_number superfluid
phase times the 8 octonion components (real part e₀ + seven imaginaries
e₁..e₇ ↔ the 7 Fano points). Internal symmetry: G₂ = Aut(𝕆) acting irreducibly
on Im(𝕆)=ℝ⁷, with the Fano collineation subgroup PSL(2,7) ≅ GL(3,2) permuting
e₁..e₇ as the 7 points of PG(2,2). The §1.1 generators (Lemma 2.2) are used
verbatim, so G0 is tied to the framework's own submission-ready result.

WHAT SYMMETRY FIXES (the parts this script verifies are discrete & exact):
  • A coupling tensor on the 7 imaginaries that is invariant under the
    collineation group is constrained by the group's ORBITS on k-tuples of
    points. The dimension of the invariant symmetric k-coupling space = number
    of orbits on unordered k-subsets (for the leading multilinear piece).
  • 2-body: orbits on unordered pairs ⇒ allowed K_ij.
  • 3-body: orbits on unordered triples ⇒ where Fano-LINE structure first enters.

KEY EXPECTED RESULTS (verified below, exact):
  • The group is 2-transitive on the 7 points ⇒ only TWO invariant symmetric
    2-tensors (I and J=all-ones) ⇒ the symmetry-allowed 2-body kernel is
    scalar-per-channel: K_ij(r) = a(r)·δ_ij + b(r)·J_ij. NO finer Fano structure
    at 2-body.
  • On unordered triples there are exactly TWO orbits: the 7 collinear triples
    (the Fano lines) and the 28 non-collinear triples ⇒ Fano-LINE structure
    first appears at the 3-BODY interaction (degree 6 in ψ), beyond the ≤4
    minimal truncation.

CONSEQUENCE FOR THE ROTON (M.CW-honest). Symmetry fixes the kernel FORM (scalar
× {I,J}) but NOT its radial profile a(r), b(r). A roton (negative Ũ-lobe at
finite k) is a property of the radial profile — a metric/scale, M.CW import.
So: symmetry PERMITS a roton but cannot FORCE one; the MV-G1 soft-core kernel is
a legitimate representative of the allowed 2-body form, but its roton is
imported (I2/I3), not derived. The framework's OWN structure (Fano lines) lives
at 3-body and is untested by MV-G1.

stdlib only. Author: §3.4-G0 first pass, 2026-06-03.
"""

from itertools import combinations, product


# ── F_2 linear algebra: GL(3,2) from the §1.1 generators ─────────────────────
def matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) % 2
                       for j in range(3)) for i in range(3))


G1 = ((1, 0, 0), (0, 0, 1), (0, 1, 0))      # §1.1 Lemma 2.2, g₁  (S₄ subgroup gen)
G2 = ((1, 1, 0), (0, 1, 1), (0, 0, 1))      # §1.1 Lemma 2.2, g₂  (S₄ subgroup gen)


def generate_group(gens):
    """Closure of the generator set under multiplication mod 2."""
    elems = set(gens)
    frontier = list(gens)
    while frontier:
        nxt = []
        for a in frontier:
            for g in gens:
                p = matmul(a, g)
                if p not in elems:
                    elems.add(p)
                    nxt.append(p)
        frontier = nxt
    return elems


def det3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % 2


def full_GL32():
    """All invertible 3×3 matrices over F_2 = GL(3,2) ≅ PSL(2,7), order 168."""
    out = []
    for bits in product((0, 1), repeat=9):
        M = (bits[0:3], bits[3:6], bits[6:9])
        if det3(M) == 1:                 # over F_2, invertible ⇔ det = 1
            out.append(M)
    return out


# ── Action on the 7 Fano points (nonzero vectors of F_2^3) ───────────────────
POINTS = [v for v in product((0, 1), repeat=3) if any(v)]      # 7 points
PIDX = {v: i for i, v in enumerate(POINTS)}


def apply(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(3)) % 2 for i in range(3))


def permutation(M):
    return tuple(PIDX[apply(M, v)] for v in POINTS)


# ── Orbit counting on k-subsets / k-tuples ───────────────────────────────────
def orbits_on(perms, items, canon):
    """Number and sizes of orbits of the permutation group on `items`,
    where canon(perm, item) maps an item under a permutation."""
    seen = set()
    orbits = []
    item_set = set(items)
    for it in items:
        if it in seen:
            continue
        orb = set()
        stack = [it]
        while stack:
            x = stack.pop()
            if x in orb:
                continue
            orb.add(x)
            for p in perms:
                y = canon(p, x)
                if y not in orb:
                    stack.append(y)
        seen |= orb
        orbits.append(orb)
    return orbits


def act_ordered(p, tup):
    return tuple(p[i] for i in tup)


def act_set(p, fs):
    return frozenset(p[i] for i in fs)


def is_collinear(triple):
    """Three Fano points are collinear iff they sum to 0 in F_2^3 (a line is a
    2-dim subspace {a,b,a+b})."""
    a, b, c = (POINTS[i] for i in triple)
    return all((a[k] + b[k] + c[k]) % 2 == 0 for k in range(3))


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    G = full_GL32()
    perms = [permutation(M) for M in G]
    S4 = generate_group([G1, G2])                 # §1.1 Lemma 2.2 subgroup
    print("=" * 74)
    print("§3.4-G0 FIRST PASS — symmetry-allowed interaction structure")
    print("=" * 74)
    print(f"  Full collineation group GL(3,2) ≅ PSL(2,7): |G| = {len(G)}  "
          f"(expect 168)  {'✓' if len(G) == 168 else '✗'}")
    print(f"  §1.1 Lemma 2.2 ⟨g₁,g₂⟩ subgroup: |H| = {len(S4)} "
          f"(= |S₄|, the §1.1 Thm 2.1 maximal subgroup); H ⊆ G: "
          f"{'✓' if S4 <= set(G) else '✗'}")
    print(f"  Action on the 7 Fano points: {len(set(perms))} distinct permutations")
    print()

    # 1-point: transitive?
    o1 = orbits_on(perms, [(i,) for i in range(7)], act_ordered)
    print(f"  1-point orbits (transitivity): {len(o1)}  "
          f"({'transitive ✓' if len(o1) == 1 else 'NOT transitive'})")

    # ordered distinct pairs -> orbitals -> centralizer / invariant-2-tensor dim
    ord_pairs = [(i, j) for i in range(7) for j in range(7) if i != j]
    o2o = orbits_on(perms, ord_pairs, act_ordered)
    orbitals = len(o2o) + 1     # +1 for the diagonal orbital (i,i)
    print(f"  ordered-distinct-pair orbits: {len(o2o)}  ⇒ orbitals (incl. diagonal): "
          f"{orbitals}")
    print(f"  ⇒ 2-transitive: {'YES ✓' if len(o2o) == 1 else 'no'}  "
          f"⇒ invariant symmetric 2-tensors: dim {orbitals} = span{{I, J}}")
    print("    ⚠ CORRECTION (per §2.79): {I,J} is the PERMUTATION-rep invariant —")
    print("      the WRONG module for the action. G₂ acts on the 7 as its irreducible")
    print("      7, so by Schur the action's invariant symmetric 2-tensor is UNIQUE")
    print("      (the metric) ⇒ 2-body kernel is a SINGLE scalar. The valid output")
    print("      of THIS tool is the 7+28 incidence split below, not the kernel.")
    print()

    # unordered k-subsets
    print("  ORBITS ON UNORDERED k-SUBSETS (= dim of leading invariant k-coupling):")
    for k in (2, 3, 4):
        subs = [frozenset(c) for c in combinations(range(7), k)]
        ok = orbits_on(perms, subs, act_set)
        sizes = sorted(len(o) for o in ok)
        tag = ""
        if k == 3:
            coll = [o for o in ok if all(is_collinear(tuple(sorted(s))) for s in o)]
            tag = (f"   <- collinear-triple (Fano-line) orbit size "
                   f"{len(coll[0]) if coll else '?'} = the 7 lines")
        print(f"    k={k}: {len(ok)} orbit(s), sizes {sizes}{tag}")
    print()

    # explicit Fano-line check
    triples = list(combinations(range(7), 3))
    lines = [t for t in triples if is_collinear(t)]
    line_orbit = orbits_on(perms, [frozenset(lines[0])], act_set)
    print(f"  Fano lines (collinear triples): {len(lines)} of {len(triples)}; "
          f"single orbit under G: {'✓' if len(line_orbit[0]) == len(lines) else '✗'} "
          f"(orbit size {len(line_orbit[0])})")
    print()

    # ── Verdict ──────────────────────────────────────────────────────────────
    print("=" * 74)
    print("G0 FIRST-PASS VERDICT")
    print("=" * 74)
    print("""\
  CONTACT POTENTIAL (no derivatives), U(1)×G₂-invariant, degree ≤4:
    Forced to standard GP:  V(ψ) = −μ|ψ|² + (g/2)|ψ|⁴.
    G₂ acts irreducibly on Im(𝕆)=ℝ⁷ ⇒ unique invariant quadratic (the norm);
    the coassociative 4-form is antisymmetric ⇒ no bosonic quartic beyond
    (|ψ|²)². The octonion structure adds NOTHING to the contact potential.

  2-BODY NON-LOCAL KERNEL  [CORRECTED per §2.79 — see warning above]:
    The action symmetry on the algebra is G₂ = Aut(𝕆) (only F₂₁⊂PSL(2,7) lifts
    as an unsigned basis permutation; all 168 lift with signs → G_sp order 1344).
    G₂ acts irreducibly on the 7 ⇒ (Schur) a UNIQUE invariant symmetric 2-tensor
    (the metric) ⇒ the 2-body kernel is a SINGLE scalar K_ij(r)=a(r)·δ_ij — even
    stricter than the {I,J}/scalar-per-channel the permutation rep suggests.
    (Verified in-env: dim 1 under G₂/G_sp, dim 2 under F₂₁ alone.)
    NO finer Fano structure at 2-body. A roton (negative Ũ-lobe at finite k)
    is PERMITTED via the radial profile a(r)/b(r) but is NOT FORCED by the
    symmetry — the profile is an M.CW import (I2/I3). The MV-G1 soft-core
    kernel is a legitimate representative of this allowed form; its p6m result
    is consistent with G0, but the roton it uses is imported, not derived.

  3-BODY INTERACTION (degree 6 in ψ):
    Two orbits on triples (7 collinear + 28 non-collinear) ⇒ a 3-body coupling
    CAN distinguish the Fano LINES. This is the FIRST place the framework's
    specific PSL(2,7)/Fano content enters the dynamics. It is beyond the ≤4
    minimal truncation and is the genuine framework-specific gate (forward
    pointer G0→G1′): does the Fano 3-body term select or modulate the lattice?

  PRE-REGISTERED TERM LIST (record before re-running MV-G1, per §3.4.3):
    S = ∫ ½|∇ψ|²  −  μ|ψ|²  +  (g/2)|ψ|⁴
        +  ½∫∫ |ψ(x)|² [a(r)δ + b(r)J] |ψ(x')|²            (2-body; roton imported)
        +  (λ/3)∫∫∫ Fano-line 3-body coupling on collinear triples   (G0→G1′)
    Imports remain exactly I1 (target), I2 (kinetic form), I3 (one scale) plus
    the radial profiles a(r),b(r) (M.CW metric class) — declared, not derived.
""")
    print("  Cross-refs: §1.1 (generators), §3.4.3 (G0), MV-G1 (tools/mv_g1_minimiser.py),")
    print("  M.CW (kernel radial profile = import), §2.55/§2.68 (Fano-line structure).")


if __name__ == "__main__":
    main()
