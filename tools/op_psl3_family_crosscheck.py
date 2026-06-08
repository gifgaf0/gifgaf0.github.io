"""
op_psl3_family_crosscheck.py — OP-PSL.3 independent cross-check (pure Python)
============================================================================
Deliverable 2 of the CC BRIEF (OP-PSL.3). The Eddington-guard / independent-
verification leg: builds every group FROM SCRATCH as permutations and imports
nothing under test (only the std lib + a from-scratch permutation toolkit below).
It cross-checks the GAP sweep (op_psl3_family_sweep.g) on every shared quantity.

What it verifies, with NO external group theory and NO character table:
  • all 7 primes: PSL(2,p) on P^1(F_p) (Mobius), |G| = p(p^2-1)/2, and
    2-transitivity (one orbit on ordered distinct pairs) ⟺ rank 2 ⟺
    C[G/Borel] = 1 ⊕ St ⟺ n1(Borel; St) = 1  (PR-5 baseline);
  • trinity degree-p actions: A5 on 5 pts (p=5), GL(3,2) on 7 pts (p=7),
    PSL(2,11) on 11 pts (p=11, generators sourced from GAP as DATA, every claimed
    property re-verified here): |G|, point-stabilizer order/index, 2-transitivity;
  • the index-p stabilizer's type (A4 / S4 / A5) by order + perfect-or-not;
  • INDEPENDENT n1(.; rho_{p-1}) reproduction for p=5,7 over the maximal classes,
    using ONLY permutation characters:  rho_{p-1}(g) = fix_main(g) − 1, and
    n1(M; rho_{p-1}) = (1/|G|) Σ_g (fix_main(g) − 1) · fix_{G/M}(g),
    with the maximal actions built as: point action (index-p stab), Sylow-p
    conjugation (the Borel, index p+1), 2-subsets (p=5: the S3, index 10),
    PG(2,2) lines (p=7: the line-stabilizer S4, index 7).  This reproduces the
    GAP n1 columns — including the p=5 non-uniqueness (S3 also = 1) — from scratch.

Std lib only. Author: OP-PSL.3 cross-check, 2026-06-08.
"""

from itertools import combinations, product
from collections import deque


# ── from-scratch permutation toolkit (0-indexed tuples) ──────────────────────
def compose(a, b):                      # (a∘b)(i) = a[b[i]]
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a):
    inv = [0] * len(a)
    for i, ai in enumerate(a):
        inv[ai] = i
    return tuple(inv)


def closure(gens, n):
    """BFS closure of <gens> as a set of permutation tuples on n points."""
    idn = tuple(range(n))
    G = {idn}
    frontier = deque([idn])
    while frontier:
        x = frontier.popleft()
        for g in gens:
            y = compose(g, x)
            if y not in G:
                G.add(y)
                frontier.append(y)
    return G


def fix_points(g):
    return sum(1 for i, gi in enumerate(g) if gi == i)


def orbit_of_pair(gens, pair):
    """Orbit of an ordered pair under <gens> (generator BFS)."""
    seen = {pair}
    frontier = deque([pair])
    while frontier:
        (x, y) = frontier.popleft()
        for g in gens:
            q = (g[x], g[y])
            if q not in seen:
                seen.add(q)
                frontier.append(q)
    return seen


def is_two_transitive(gens, n):
    """True iff one orbit on ordered distinct pairs (== n(n-1))."""
    orb = orbit_of_pair(gens, (0, 1))
    return len(orb) == n * (n - 1)


def point_stabilizer(G, pt=0):
    return [g for g in G if g[pt] == pt]


def subgroup_closure(elts):
    """Closure of a set of perm tuples (assumed same degree) under multiplication."""
    n = len(next(iter(elts)))
    return closure(tuple(elts), n)


def is_perfect(elts):
    """Is the subgroup <elts> perfect (= its own derived subgroup)?"""
    H = list(elts)
    comms = set()
    for a in H:
        ia = inverse(a)
        for b in H:
            comms.add(compose(compose(a, b), compose(ia, inverse(b))))
    return len(subgroup_closure(comms)) == len(elts)


# ── derived actions → fix-count as a class function on g ─────────────────────
def fix_on_subsets(g, subsets):
    """#subsets S with {g[x]:x in S} == S."""
    return sum(1 for S in subsets if frozenset(g[x] for x in S) == S)


def sylow_q_subgroups(G, q):
    """All Sylow-q subgroups (q prime; each cyclic order q) as frozensets."""
    subs = set()
    for x in G:
        # order of x
        y, o = x, 1
        idn = tuple(range(len(x)))
        while y != idn:
            y = compose(y, x); o += 1
        if o == q:
            cyc = [idn]
            z = x
            while z != idn:
                cyc.append(z); z = compose(z, x)
            subs.add(frozenset(cyc))
    return list(subs)


def fix_on_conj(g, subgroups):
    """#subgroups P (frozensets of perms) fixed by conjugation x↦ g x g^{-1}."""
    ig = inverse(g)
    cnt = 0
    for P in subgroups:
        if frozenset(compose(compose(g, h), ig) for h in P) == P:
            cnt += 1
    return cnt


def n1_via_permchars(G, rho_fix, M_fix):
    """n1(M; rho) = (1/|G|) Σ_g rho(g)·π_M(g), rho(g)=rho_fix(g), π_M(g)=M_fix(g)."""
    tot = sum(rho_fix(g) * M_fix(g) for g in G)
    assert tot % len(G) == 0, "non-integer inner product"
    return tot // len(G)


# ── group constructions (from scratch) ───────────────────────────────────────
def psl_on_P1(p):
    """PSL(2,p) on P^1(F_p) = {0..p-1, ∞(=p)} via S:z↦z+1, T:z↦−1/z."""
    n = p + 1
    INF = p
    S = [0] * n; T = [0] * n
    for z in range(p):
        S[z] = (z + 1) % p
        T[z] = (pow(z, p - 2, p) * (p - 1)) % p if z != 0 else INF   # −1/z
    S[INF] = INF
    T[INF] = 0
    return [tuple(S), tuple(T)], n


def a5_on_5():
    a = (1, 2, 3, 4, 0)            # (1 2 3 4 5)
    b = (0, 1, 3, 4, 2)            # (3 4 5)
    return [a, b], 5


def gl32_on_7():
    """GL(3,2)≅PSL(2,7) on the 7 nonzero vectors of F_2^3 (points of PG(2,2)).

    NOTE (verified discrepancy): the CC-brief's §1.1 'Lemma 2.5' generators
    g1=[[1,0,0],[0,0,1],[0,1,0]], g2=[[1,1,0],[0,1,1],[0,0,1]] generate only the
    ORDER-24 point-stabilizer S4 (both fix the vector (1,0,0)) — confirmed in
    Python and GAP — NOT GL(3,2) (order 168). We therefore build GL(3,2) by full
    enumeration of all 168 invertible 3x3 matrices over F_2 (det=1), which is the
    cleanest from-scratch construction. The generator discrepancy is flagged in
    the memo for chat-side."""
    vecs = [v for v in product((0, 1), repeat=3) if any(v)]
    vecs.sort(key=lambda v: v[0] + 2 * v[1] + 4 * v[2])
    idx = {v: i for i, v in enumerate(vecs)}

    def det3(M):                              # det over F_2
        return (M[0][0] * (M[1][1] * M[2][2] ^ M[1][2] * M[2][1])
                ^ M[0][1] * (M[1][0] * M[2][2] ^ M[1][2] * M[2][0])
                ^ M[0][2] * (M[1][0] * M[2][1] ^ M[1][1] * M[2][0])) & 1

    def matperm(M):
        out = [0] * 7
        for v in vecs:
            w = tuple(sum(M[r][c] * v[c] for c in range(3)) % 2 for r in range(3))
            out[idx[v]] = idx[w]
        return tuple(out)

    perms = []
    for e in product((0, 1), repeat=9):
        M = (e[0:3], e[3:6], e[6:9])
        if det3(M) == 1:
            perms.append(matperm(M))         # all 168 invertible matrices
    lines = []
    for u, v in combinations(vecs, 2):
        w = tuple((u[c] ^ v[c]) for c in range(3))
        L = frozenset({idx[u], idx[v], idx[w]})
        if len(L) == 3 and L not in lines:
            lines.append(L)
    return perms, 7, lines


def psl_on_11():
    """PSL(2,11) degree-11 exceptional action. Generators are DATA from GAP
    (FactorCosetAction on the index-11 A5); every property re-verified below."""
    g1 = tuple(x - 1 for x in [7, 6, 1, 8, 2, 4, 10, 5, 3, 9, 11])
    g2 = tuple(x - 1 for x in [8, 4, 11, 3, 7, 6, 1, 9, 5, 2, 10])
    return [g1, g2], 11


# ── per-prime cross-check ────────────────────────────────────────────────────
EXPECT = {}   # collect (label, got, want) for the agreement summary


def check(label, got, want):
    EXPECT[label] = (got, want, got == want)
    flag = "OK" if got == want else "*** MISMATCH ***"
    print(f"    {label}: got={got} want={want}  {flag}")


def main():
    primes = [5, 7, 11, 13, 17, 19, 23]
    print("=" * 78)
    print("OP-PSL.3 — pure-Python independent cross-check (from scratch)")
    print("=" * 78)

    # ---- PR-5 baseline: P^1 construction, |G| and 2-transitivity, all primes ----
    print("\n[A] P^1(F_p) Mobius construction — |G| and 2-transitivity (PR-5 baseline):")
    for p in primes:
        gens, n = psl_on_P1(p)
        G = closure(gens, n)
        order = len(G)
        twoT = is_two_transitive(gens, n)
        print(f"  p={p}: deg={n}  |G|={order}  expect {p*(p*p-1)//2}  2-transitive={twoT}"
              f"  ⇒ n1(Borel;St)=1 via rank2={twoT}")
        check(f"|G| p={p} (P1)", order, p * (p * p - 1) // 2)
        check(f"2-transitive p={p} (P1)", twoT, True)

    # ---- trinity degree-p actions: PR-1/PR-2 + stabilizer type ----
    print("\n[B] Trinity index-p (degree-p) actions — PR-1 / PR-2 + stabilizer type:")

    # p=5
    gens, n = a5_on_5(); G5 = closure(gens, n)
    st = point_stabilizer(G5, 0)
    print(f"  p=5  A5-on-5: |G|={len(G5)} deg={n} 2-trans={is_two_transitive(gens,n)} "
          f"|stab|={len(st)} index={len(G5)//len(st)} stab_perfect={is_perfect(st)}")
    check("|G| p=5", len(G5), 60)
    check("index-5 stab order (A4)", len(st), 12)
    check("p=5 2-transitive on 5", is_two_transitive(gens, n), True)

    # p=7
    gens, n, lines7 = gl32_on_7(); G7 = closure(gens, n)
    st7 = point_stabilizer(G7, 0)
    print(f"  p=7  GL(3,2)-on-7: |G|={len(G7)} deg={n} 2-trans={is_two_transitive(gens,n)} "
          f"|stab|={len(st7)} index={len(G7)//len(st7)} stab_perfect={is_perfect(st7)} "
          f"#PG(2,2)-lines={len(lines7)}")
    check("|G| p=7", len(G7), 168)
    check("index-7 stab order (S4)", len(st7), 24)
    check("p=7 2-transitive on 7", is_two_transitive(gens, n), True)
    check("p=7 #lines", len(lines7), 7)

    # p=11
    gens, n = psl_on_11(); G11 = closure(gens, n)
    st11 = point_stabilizer(G11, 0)
    print(f"  p=11 deg-11 (GAP-sourced gens, re-verified): |G|={len(G11)} deg={n} "
          f"2-trans={is_two_transitive(gens,n)} |stab|={len(st11)} "
          f"index={len(G11)//len(st11)} stab_perfect={is_perfect(st11)} (A5⇔perfect&|60|)")
    check("|G| p=11", len(G11), 660)
    check("index-11 stab order (A5)", len(st11), 60)
    check("p=11 2-transitive on 11", is_two_transitive(gens, n), True)
    check("p=11 stab perfect (A5 evidence)", is_perfect(st11), True)

    # ---- INDEPENDENT n1(.; rho_{p-1}) columns for p=5, p=7 (perm-chars only) ----
    print("\n[C] Independent n1(.; rho_{p-1}) reproduction (permutation characters only):")

    # p=5 : rho4 = fix_5 − 1 ; maximal actions: 5-pts(A4), 6=Sylow5-conj(D10), 10=2subsets(S3)
    rho4 = lambda g: fix_points(g) - 1
    subsets5_2 = [frozenset(s) for s in combinations(range(5), 2)]      # 10 two-subsets
    syl5 = sylow_q_subgroups(G5, 5)                                     # 6 Sylow-5 (Borel)
    n1_A4 = n1_via_permchars(G5, rho4, lambda g: fix_points(g))         # point action
    n1_D10 = n1_via_permchars(G5, rho4, lambda g: fix_on_conj(g, syl5)) # Borel
    n1_S3 = n1_via_permchars(G5, rho4, lambda g: fix_on_subsets(g, subsets5_2))
    print(f"  p=5  ρ4 column: n1(A4·idx5)={n1_A4}  n1(D10·Borel idx6)={n1_D10}  "
          f"n1(S3·idx10)={n1_S3}   [#Sylow5={len(syl5)}]")
    check("p=5 n1(A4;ρ4)", n1_A4, 1)
    check("p=5 n1(D10;ρ4) Borel", n1_D10, 0)
    check("p=5 n1(S3;ρ4) — NON-uniqueness witness", n1_S3, 1)

    # p=7 : rho6 = fix_7 − 1 ; maximal actions: 7-pts(S4 point), 7-lines(S4 line),
    #       8 = Sylow7-conj (7:3 Borel)
    rho6 = lambda g: fix_points(g) - 1
    syl7 = sylow_q_subgroups(G7, 7)                                     # 8 Sylow-7 (Borel)
    n1_S4pt = n1_via_permchars(G7, rho6, lambda g: fix_points(g))
    n1_S4ln = n1_via_permchars(G7, rho6, lambda g: fix_on_subsets(g, lines7))
    n1_73 = n1_via_permchars(G7, rho6, lambda g: fix_on_conj(g, syl7))
    print(f"  p=7  ρ6 column: n1(S4·points idx7)={n1_S4pt}  n1(S4·lines idx7)={n1_S4ln}  "
          f"n1(7:3·Borel idx8)={n1_73}   [#Sylow7={len(syl7)}]")
    check("p=7 n1(S4 point;ρ6)", n1_S4pt, 1)
    check("p=7 n1(S4 line;ρ6)", n1_S4ln, 1)
    check("p=7 n1(7:3;ρ6) Borel", n1_73, 0)

    # p=11 : rho10 = fix_11 − 1 ; n1(A5;rho10) and n1(Borel 11:5; rho10) from scratch
    rho10 = lambda g: fix_points(g) - 1
    syl11 = sylow_q_subgroups(G11, 11)                                  # 12 Sylow-11 (Borel)
    n1_A5 = n1_via_permchars(G11, rho10, lambda g: fix_points(g))
    n1_B11 = n1_via_permchars(G11, rho10, lambda g: fix_on_conj(g, syl11))
    print(f"  p=11 ρ10 column (partial): n1(A5·idx11)={n1_A5}  "
          f"n1(11:5·Borel idx12)={n1_B11}   [#Sylow11={len(syl11)}]")
    check("p=11 n1(A5;ρ10)", n1_A5, 1)
    check("p=11 n1(11:5;ρ10) Borel", n1_B11, 0)

    # ---- agreement summary ----
    print("\n" + "=" * 78)
    print("AGREEMENT SUMMARY (Python vs GAP/known-shared quantities)")
    print("=" * 78)
    bad = [k for k, (g, w, ok) in EXPECT.items() if not ok]
    for k, (g, w, ok) in EXPECT.items():
        if not ok:
            print(f"  MISMATCH {k}: got {g}, want {w}")
    print(f"  {len(EXPECT)} checks; {len(EXPECT)-len(bad)} OK; {len(bad)} mismatches.")
    print("  => " + ("ALL PYTHON CROSS-CHECKS AGREE." if not bad
                     else "*** DISAGREEMENT — investigate before folding. ***"))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
