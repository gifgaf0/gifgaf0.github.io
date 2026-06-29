"""
G-INT1 structural core (R1, bankable, import-free) — octonion / Fano / F_21.

Establishes the LAMBDA-INDEPENDENT, scale-independent facts the gate's primary
decision scalars turn on, with NO GP numerics and NO ledger value:
  (i)   octonion structure constants phi_abc are supported exactly on Fano lines
        -> the oriented three-body term O = phi_abc psi_a d_x psi_b d_y psi_c is
        Fano-line-selective by construction (S_Fano carrier);
  (ii)  F_21 = Z/7 ><| Z/3 acts on the seven imaginary units as pure-permutation
        octonion automorphisms (subgroup of G_2);
  (iii) the 7 decomposes under F_21 as 1 (+) 3 (+) 3bar  (character computation).

Convention: cyclic octonions e_i e_{i+1} = e_{i+3} (indices mod 7, 1..7~0), which
makes the Singer shift i->i+1 and the Frobenius i->2i manifest automorphisms.
"""
import numpy as np
import itertools

# ---- cyclic octonion multiplication on imaginary units 0..6 (e_7 == e_0) -----
# oriented lines L_i = {i, i+1, i+3} mod 7 ; on each, e_a e_b = e_c cyclically.
def build_octonions():
    phi = np.zeros((7, 7, 7))            # e_a e_b = sum_c phi[a,b,c] e_c  (a,b,c in 0..6)
    sgn = {}                            # (a,b) -> (sign, c) for a!=b
    for i in range(7):
        trip = [i % 7, (i + 1) % 7, (i + 3) % 7]
        a, b, c = trip
        # oriented cycle a->b->c->a gives +1
        for (x, y, z) in [(a, b, c), (b, c, a), (c, a, b)]:
            phi[x, y, z] = +1.0
            phi[y, x, z] = -1.0          # antisymmetry
    return phi

def lines():
    return [frozenset({i % 7, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]

def verify_algebra(phi):
    L = set(lines())
    # phi supported exactly on lines
    support = set()
    for a in range(7):
        for b in range(7):
            for c in range(7):
                if abs(phi[a, b, c]) > 0.5:
                    support.add(frozenset({a, b, c}))
    support_is_lines = (support == L)
    # antisymmetry e_a e_b = - e_b e_a
    anti = np.allclose(phi, -phi.transpose(1, 0, 2))
    # each pair on exactly one line; 7 lines, 3 points each, each point on 3 lines
    pt_deg = [sum(1 for ln in L if p in ln) for p in range(7)]
    return dict(support_is_lines=support_is_lines, antisym=anti,
                n_lines=len(L), point_degrees=set(pt_deg))

def mult_matrix(phi):
    """Left-mult table M[a,b]=c with sign s, for verifying automorphisms."""
    tab = {}
    for a in range(7):
        for b in range(7):
            if a == b:
                tab[(a, b)] = (0, -1)          # e_a^2 = -1 (the real unit; sentinel)
                continue
            cs = [(c, phi[a, b, c]) for c in range(7) if abs(phi[a, b, c]) > 0.5]
            assert len(cs) == 1, (a, b, cs)
            c, s = cs[0]
            tab[(a, b)] = (c, int(round(s)))
    return tab

def is_automorphism(perm, sign, phi, tab):
    """perm: i->perm[i]; sign[i] in {+-1}. Automorphism iff
       M(e_a e_b) = M(e_a) M(e_b) for all a!=b, where M(e_i)=sign[i] e_perm[i]."""
    for a in range(7):
        for b in range(7):
            if a == b:
                continue
            c, s = tab[(a, b)]                 # e_a e_b = s e_c
            # LHS: M(s e_c) = s * sign[c] e_perm[c]
            lhs_sign = s * sign[c]; lhs_idx = perm[c]
            # RHS: M(e_a) M(e_b) = sign[a] sign[b] (e_perm[a] e_perm[b])
            pc, ps = tab[(perm[a], perm[b])]
            rhs_sign = sign[a] * sign[b] * ps; rhs_idx = pc
            if lhs_idx != rhs_idx or lhs_sign != rhs_sign:
                return False
    return True

def perm_matrix(perm, sign):
    M = np.zeros((7, 7))
    for i in range(7):
        M[perm[i], i] = sign[i]
    return M

if __name__ == "__main__":
    phi = build_octonions()
    info = verify_algebra(phi)
    print("=== (i) octonion structure constants / Fano lines (R1) ===")
    print(f"  phi supported exactly on Fano lines: {info['support_is_lines']}")
    print(f"  antisymmetric e_a e_b = -e_b e_a:    {info['antisym']}")
    print(f"  #lines={info['n_lines']} (expect 7); each point on {info['point_degrees']} lines (expect {{3}})")
    L = lines()
    line_124 = frozenset({0, 1, 3})       # {1,2,4} in 1-indexed = {0,1,3} here
    nonline_123 = frozenset({0, 1, 2})    # {1,2,3} = {0,1,2}
    print(f"  {{e1,e2,e4}} is a Fano line: {line_124 in set(L)}   (oriented term ACTIVE)")
    print(f"  {{e1,e2,e3}} is a Fano line: {nonline_123 in set(L)}  (oriented term INERT -> S_Fano selective)")

    tab = mult_matrix(phi)
    print("\n=== (ii) F_21 = <rho: i->i+1 , sigma: i->2i> as octonion automorphisms ===")
    rho = [(i + 1) % 7 for i in range(7)]
    sig = [(2 * i) % 7 for i in range(7)]
    sgn1 = [1] * 7
    aut_rho = is_automorphism(rho, sgn1, phi, tab)
    aut_sig = is_automorphism(sig, sgn1, phi, tab)
    print(f"  rho (Singer 7-cycle) is an automorphism (pure perm): {aut_rho}")
    print(f"  sigma (Frobenius i->2i, order 3) is an automorphism: {aut_sig}")
    # generate the group, confirm order 21
    Mrho, Msig = perm_matrix(rho, sgn1), perm_matrix(sig, sgn1)
    G = {tuple(np.eye(7).flatten())}
    frontier = [np.eye(7)]
    gens = [Mrho, Msig]
    while frontier:
        X = frontier.pop()
        for g in gens:
            Y = g @ X
            key = tuple(np.round(Y).astype(int).flatten())
            if key not in G:
                G.add(key); frontier.append(Y)
    print(f"  |<rho,sigma>| = {len(G)}   (expect 21)")

    print("\n=== (iii) decomposition of the 7 under F_21 (character) ===")
    mats = [np.array(k).reshape(7, 7) for k in G]
    chars = [np.trace(M) for M in mats]
    # order of each element
    def order(M):
        P = M.copy(); k = 1
        while not np.allclose(P, np.eye(7)):
            P = M @ P; k += 1
            if k > 50: break
        return k
    from collections import Counter
    by_ord = Counter(order(M) for M in mats)
    print(f"  element orders in F_21: {dict(sorted(by_ord.items()))}  (expect {{1:1,3:14,7:6}})")
    # class sums for the permutation character: chi(e)=7, chi(order7)=#fix, chi(order3)=#fix
    fix_by_order = {}
    for M in mats:
        o = order(M); f = int(round(np.trace(M)))
        fix_by_order.setdefault(o, []).append(f)
    print(f"  trace (fixed pts) by order: " +
          ", ".join(f"ord{o}->{sorted(set(v))}" for o, v in sorted(fix_by_order.items())))
    # <chi,chi> = (1/|G|) sum |chi(g)|^2  -> rank of the transitive action
    rank = sum(c * c for c in chars) / len(G)
    print(f"  <chi_7, chi_7> = {rank:.3f}   (rank-3 action -> 1 + two nontrivial irreps)")
    # <chi,1> = (1/|G|) sum chi  = # trivial copies
    n_triv = sum(chars) / len(G)
    print(f"  <chi_7, triv> = {n_triv:.3f}   (one trivial copy = the '1')")
    print(f"  => 7 = 1 (+) 3 (+) 3bar  : {abs(rank-3.0)<1e-9 and abs(n_triv-1.0)<1e-9}")
    print("     (rank 3 = trivial + two 3-dim irreps; the two 3's are complex-conjugate")
    print("      since the order-7 generator's nonreal eigenvalues pair up -> 3 and 3bar.)")
