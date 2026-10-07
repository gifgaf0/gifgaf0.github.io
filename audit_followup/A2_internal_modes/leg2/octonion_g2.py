"""A2 leg 2 -- octonion algebra, g2 = Der(O) derived from the multiplication table,
a Cartan subalgebra, the root decomposition, and a rational (Chevalley-normalised)
weight basis of the 7.  Everything exact (integers / Gaussian rationals via sympy).

Convention (task statement; checked against staging_memo_G_VS1_v2.md s2.1):
imaginary units e1..e7, Fano lines {i, i+1, i+3} mod 7 (labels 1..7), and
e_i e_{i+1} = e_{i+3} cyclically along each line.
"""
import itertools
import random
import sympy as sp
from sympy import I, Matrix, Rational

LINES = [tuple(((i - 1 + o) % 7) + 1 for o in (0, 1, 3)) for i in range(1, 8)]


def structure_constants():
    """C[i][j][k]: e_i e_j = sum_k C[i][j][k] e_k  (i,j,k in 0..7, e0 = 1)."""
    C = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for j in range(8):
        C[0][j][j] = 1
        C[j][0][j] = 1
    for i in range(1, 8):
        C[i][i][0] = -1
    for (a, b, c) in LINES:
        for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
            C[x][y][z] = 1
            C[y][x][z] = -1
    return C


C = structure_constants()


def omul(x, y):
    return [sum(x[i] * y[j] * C[i][j][k] for i in range(8) for j in range(8)) for k in range(8)]


def phi3():
    """phi_abc on Im O (a,b,c in 1..7, stored 0-based 7x7x7): e_a e_b = phi_abc e_c (a != b)."""
    P = [[[0] * 7 for _ in range(7)] for _ in range(7)]
    for a in range(1, 8):
        for b in range(1, 8):
            if a != b:
                for c in range(1, 8):
                    P[a - 1][b - 1][c - 1] = C[a][b][c]
    return P


def check_algebra(ntrials=200, seed=1):
    rnd = random.Random(seed)
    out = {}
    ok_alt = ok_norm = ok_moufang = True
    for _ in range(ntrials):
        x = [rnd.randint(-5, 5) for _ in range(8)]
        y = [rnd.randint(-5, 5) for _ in range(8)]
        z = [rnd.randint(-5, 5) for _ in range(8)]
        if omul(omul(x, x), y) != omul(x, omul(x, y)):
            ok_alt = False
        if omul(omul(y, x), x) != omul(y, omul(x, x)):
            ok_alt = False
        n = lambda v: sum(t * t for t in v)
        if n(omul(x, y)) != n(x) * n(y):
            ok_norm = False
        # Moufang: z(x(zy)) = ((zx)z)y
        if omul(z, omul(x, omul(z, y))) != omul(omul(omul(z, x), z), y):
            ok_moufang = False
    P = phi3()
    antisym = all(P[a][b][c] == -P[b][a][c] == -P[a][c][b]
                  for a in range(7) for b in range(7) for c in range(7))
    lines_from_phi = sorted({tuple(sorted((a + 1, b + 1, c + 1)))
                             for a in range(7) for b in range(7) for c in range(7) if P[a][b][c] != 0})
    out.update(alternative=ok_alt, norm_multiplicative=ok_norm, moufang=ok_moufang,
               phi_totally_antisymmetric=antisym,
               lines=[list(l) for l in LINES],
               lines_from_phi=[list(l) for l in lines_from_phi],
               # sign check of the convention e_i e_{i+1} = e_{i+3}
               convention_holds=all(C[a][b][c] == 1 for (a, b, c) in LINES))
    nonassoc = omul(omul([0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0]), [0, 0, 0, 1, 0, 0, 0, 0]) != \
        omul([0, 1, 0, 0, 0, 0, 0, 0], omul([0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0]))
    out["non_associative_witness_(e1e2)e3!=e1(e2e3)"] = nonassoc
    return out


def derivations():
    """Exact basis of Der(O) as 8x8 rational matrices D (column convention: D e_i = sum_l D[l,i] e_l).
    Condition D(e_i e_j) = D(e_i) e_j + e_i D(e_j) for all i, j (512 equations, 64 unknowns)."""
    rows = []
    idx = lambda a, b: 8 * a + b
    for i in range(8):
        for j in range(8):
            for m in range(8):
                r = [0] * 64
                for k in range(8):
                    if C[i][j][k]:
                        r[idx(m, k)] += C[i][j][k]
                for l in range(8):
                    if C[l][j][m]:
                        r[idx(l, i)] -= C[l][j][m]
                    if C[i][l][m]:
                        r[idx(l, j)] -= C[i][l][m]
                rows.append(r)
    A = Matrix(rows)
    ns = A.nullspace()
    mats = []
    for v in ns:
        den = sp.ilcm(*[sp.fraction(t)[1] for t in v])
        v = v * den
        g = sp.igcd(*[int(t) for t in v if t != 0])
        v = v / g
        mats.append(Matrix(8, 8, list(v)))
    return mats


def span_coeffs(basis, M):
    """Solve M = sum c_k basis_k exactly; return c or None."""
    A = Matrix.hstack(*[b.reshape(b.rows * b.cols, 1) for b in basis])
    rhs = M.reshape(M.rows * M.cols, 1)
    try:
        sol, params = A.gauss_jordan_solve(rhs)
    except ValueError:
        return None
    if params.shape[0]:
        sol = sol.subs({p: 0 for p in params})
    return sol


def g2_checks(D8):
    out = {"dim": len(D8)}
    out["kill_e0"] = all(all(D[l, 0] == 0 for l in range(8)) and all(D[0, l] == 0 for l in range(8)) for D in D8)
    D7 = [D[1:, 1:] for D in D8]
    out["antisymmetric"] = all(D + D.T == sp.zeros(7, 7) for D in D7)
    # Lie closure
    closed = True
    for a, b in itertools.combinations(range(len(D7)), 2):
        Cm = D7[a] * D7[b] - D7[b] * D7[a]
        if span_coeffs(D7, Cm) is None:
            closed = False
    out["lie_closed"] = closed
    # commutant of the 7 (irreducibility): M with [M, D] = 0 for all D
    syms = sp.symbols("m0:49")
    M = Matrix(7, 7, syms)
    eqs = []
    for D in D7:
        eqs += list(M * D - D * M)
    sol = sp.linsolve(eqs, syms)
    sol = list(sol)[0]
    free = set().union(*[s.free_symbols for s in sol])
    out["commutant_dim_on_7"] = len(free)
    # commutant on 1+7 (8x8)
    syms8 = sp.symbols("q0:64")
    M8 = Matrix(8, 8, syms8)
    eqs8 = []
    for D in D8:
        eqs8 += list(M8 * D - D * M8)
    sol8 = list(sp.linsolve(eqs8, syms8))[0]
    out["commutant_dim_on_1+7"] = len(set().union(*[s.free_symbols for s in sol8]))
    # preserves phi (g2 = stabiliser of the 3-form in so(7))
    P = phi3()
    pres = True
    for D in D7:
        for a in range(7):
            for b in range(7):
                for c in range(7):
                    s = sum(D[d, a] * P[d][b][c] + D[d, b] * P[a][d][c] + D[d, c] * P[a][b][d] for d in range(7))
                    if s != 0:
                        pres = False
    out["preserves_phi"] = pres
    # so(7) has dim 21: the phi-preserving subalgebra of so(7) computed independently
    syms_a = sp.symbols("a0:21")
    pairs = list(itertools.combinations(range(7), 2))
    A = sp.zeros(7, 7)
    for s, (i, j) in zip(syms_a, pairs):
        A[i, j] += s
        A[j, i] -= s
    eqs = []
    for a in range(7):
        for b in range(a + 1, 7):
            for c in range(b + 1, 7):
                eqs.append(sum(A[d, a] * P[d][b][c] + A[d, b] * P[a][d][c] + A[d, c] * P[a][b][d] for d in range(7)))
    solA = list(sp.linsolve(eqs, syms_a))[0]
    out["dim_stab_so7_of_phi"] = len(set().union(*[s.free_symbols for s in solA]))
    return out, D7


def transitivity_ranks(D7, seed=3):
    """rank of the g2 orbit map at a generic pair / triple of vectors (C-VS-3 style check)."""
    rnd = random.Random(seed)
    vec = lambda: Matrix([rnd.randint(-9, 9) for _ in range(7)])
    u, v, w = vec(), vec(), vec()
    r1 = Matrix.hstack(*[D * u for D in D7]).rank()
    r2 = Matrix.hstack(*[Matrix.vstack(D * u, D * v) for D in D7]).rank()
    r3 = Matrix.hstack(*[Matrix.vstack(D * u, D * v, D * w) for D in D7]).rank()
    return {"rank_single": int(r1), "rank_pair": int(r2), "rank_triple": int(r3)}


def cartan_and_weights(D7):
    """Cartan subalgebra inside span{R_jk} for the three planes paired by L_{e7};
    weight basis over Q(i); root decomposition; Chevalley-normalised rational basis."""
    # L_{e7} on Im O: e7 e_j = s e_k
    pairs = []
    seen = set()
    for j in range(1, 7):
        if j in seen:
            continue
        k = [kk for kk in range(8) if C[7][j][kk] != 0][0]
        pairs.append((j, k))
        seen |= {j, k}
    # rotation generators R_jk: e_j -> e_k, e_k -> -e_j (0-based on Im O index-1)
    Rs = []
    for (j, k) in pairs:
        R = sp.zeros(7, 7)
        R[k - 1, j - 1] = 1
        R[j - 1, k - 1] = -1
        Rs.append(R)
    # intersection span(Rs) cap span(D7)
    c = sp.symbols("c0:3")
    d = sp.symbols("d0:14")
    expr = sum((ci * R for ci, R in zip(c, Rs)), sp.zeros(7, 7)) - sum((di * D for di, D in zip(d, D7)), sp.zeros(7, 7))
    sol = list(sp.linsolve(list(expr), list(c) + list(d)))[0]
    csol = sol[:3]
    free = sorted(set().union(*[s.free_symbols for s in csol]), key=str)
    Hs = []
    for f in free:
        sub = {g: (1 if g == f else 0) for g in free}
        cc = [sp.nsimplify(x.subs(sub)) for x in csol]
        den = sp.ilcm(*[sp.fraction(x)[1] for x in cc])
        cc = [x * den for x in cc]
        Hs.append((cc, sum((ci * R for ci, R in zip(cc, Rs)), sp.zeros(7, 7))))
    assert len(Hs) == 2, "Cartan intersection not 2-dim"
    H1, H2 = Hs[0][1], Hs[1][1]
    assert H1 * H2 == H2 * H1
    # centraliser of span(H1,H2) in g2 must be 2-dim (maximal torus)
    expr = sum((di * D for di, D in zip(d, D7)), sp.zeros(7, 7))
    eqs = list(expr * H1 - H1 * expr) + list(expr * H2 - H2 * expr)
    solc = list(sp.linsolve(eqs, d))[0]
    cent_dim = len(set().union(*[s.free_symbols for s in solc]))
    # weight vectors: f+ = e_j - i e_k (eigenvalue +i c_p under sum c_p R_p), f- = e_j + i e_k; plus e7
    cols, wts, labels = [], [], []
    for p, (j, k) in enumerate(pairs):
        for sgn in (+1, -1):
            f = sp.zeros(7, 1)
            f[j - 1] = 1
            f[k - 1] = -sgn * I
            lam = (sgn * Hs[0][0][p], sgn * Hs[1][0][p])
            # verify eigen-equation
            assert sp.simplify(H1 * f - I * lam[0] * f) == sp.zeros(7, 1)
            assert sp.simplify(H2 * f - I * lam[1] * f) == sp.zeros(7, 1)
            cols.append(f)
            wts.append(lam)
            labels.append(f"e{j}{'-' if sgn > 0 else '+'}i e{k}")
    f7 = sp.zeros(7, 1)
    f7[6] = 1
    cols.append(f7)
    wts.append((0, 0))
    labels.append("e7")
    B = Matrix.hstack(*cols)
    Binv = B.inv()
    Xp = [sp.simplify(Binv * D * B) for D in D7]
    # root decomposition
    cand = sorted({(wts[a][0] - wts[b][0], wts[a][1] - wts[b][1]) for a in range(7) for b in range(7) if a != b})
    cs = sp.symbols("k0:14")
    roots = {}
    for al in cand:
        eqs = []
        M = sum((ci * X for ci, X in zip(cs, Xp)), sp.zeros(7, 7))
        for a in range(7):
            for b in range(7):
                if (wts[a][0] - wts[b][0], wts[a][1] - wts[b][1]) != al:
                    eqs.append(M[a, b])
        s = list(sp.linsolve(eqs, cs))[0]
        fr = sorted(set().union(*[x.free_symbols for x in s]), key=str)
        if len(fr) == 0:
            continue
        assert len(fr) == 1, f"root space dim {len(fr)} for {al}"
        sub = {fr[0]: 1}
        E = sp.simplify(sum((x.subs(sub) * X for x, X in zip(s, Xp)), sp.zeros(7, 7)))
        roots[al] = E
    # Cartan check: diagonal of H in weight basis
    return dict(pairs=pairs, H=Hs, cent_dim=cent_dim, B=B, wts=wts, labels=labels, Xp=Xp, roots=roots)


def chevalley_normalise(cw):
    wts, roots = cw["wts"], cw["roots"]
    rlist = list(roots.keys())
    ell = lambda m: 1000 * m[0] + 7 * m[1]
    assert all(ell(r) != 0 for r in rlist)
    pos = [r for r in rlist if ell(r) > 0]
    simple = [r for r in pos if not any((r[0] - a[0], r[1] - a[1]) in pos for a in pos)]
    assert len(simple) == 2, simple
    # order simple roots: short first (alpha1), using norms from trace form
    G = Matrix([[sum(w[i] * w[j] for w in wts) for j in range(2)] for i in range(2)])
    Gi = G.inv()
    ip = lambda x, y: (Matrix([x]) * Gi * Matrix([y]).T)[0, 0]
    simple.sort(key=lambda r: ip(r, r))
    E1, E2 = roots[simple[0]], roots[simple[1]]
    # tree of nonzero entries
    edges = [(a, b, E1[a, b]) for a in range(7) for b in range(7) if E1[a, b] != 0] + \
            [(a, b, E2[a, b]) for a in range(7) for b in range(7) if E2[a, b] != 0]
    assert len(edges) == 6, edges
    s = [None] * 7
    s[0] = sp.Integer(1)
    changed = True
    while changed:
        changed = False
        for (a, b, e) in edges:
            # want e * s[b] / s[a] = 1  ->  s[a] = e * s[b]
            if s[b] is not None and s[a] is None:
                s[a] = sp.simplify(e * s[b]); changed = True
            elif s[a] is not None and s[b] is None:
                s[b] = sp.simplify(s[a] / e); changed = True
    assert all(x is not None for x in s), "edge graph not connected"
    S = sp.diag(*s)
    Si = S.inv()
    E1n = sp.simplify(Si * E1 * S)
    E2n = sp.simplify(Si * E2 * S)
    Bn = sp.simplify(cw["B"] * S)
    # all positive root vectors by commutators (rational)
    def comm(X, Y):
        return sp.simplify(X * Y - Y * X)
    E = {simple[0]: E1n, simple[1]: E2n}
    frontier = [simple[0], simple[1]]
    while frontier:
        new = []
        for r in frontier:
            for sr in simple:
                t = (r[0] + sr[0], r[1] + sr[1])
                if t in pos and t not in E:
                    Ct = comm(E[sr], E[r])
                    if Ct != sp.zeros(7, 7):
                        E[t] = Ct
                        new.append(t)
        frontier = new
    rational = all(x.is_rational for M in E.values() for x in M)
    # negative root vectors in the normalised basis (scaled to rational if possible)
    F = {}
    for r in pos:
        nr = (-r[0], -r[1])
        Fm = sp.simplify(Si * roots[nr] * S)
        nz = [x for x in Fm if x != 0]
        Fm = sp.simplify(Fm / nz[0])
        F[nr] = Fm
    rationalF = all(x.is_rational for M in F.values() for x in M)
    return dict(pos=pos, simple=simple, E=E, F=F, Bn=Bn, s=s, rationalE=rational, rationalF=rationalF,
                ip=ip, G=G)


def weyl_group(roots, G):
    """Weyl group generated by reflections, acting on weight coordinates (values on H1,H2)."""
    Gi = G.inv()
    ip = lambda x, y: (x.T * Gi * y)[0, 0]
    refl = []
    for r in roots:
        a = Matrix(r)
        M = sp.eye(2) - 2 * a * (Gi * a).T / ip(a, a)
        refl.append(sp.simplify(M))
    group = {tuple(sp.eye(2))}
    mats = [sp.eye(2)]
    frontier = [sp.eye(2)]
    while frontier:
        new = []
        for g in frontier:
            for R in refl:
                h = sp.simplify(R * g)
                key = tuple(h)
                if key not in group:
                    group.add(key)
                    mats.append(h)
                    new.append(h)
        frontier = new
    return mats


def build_all(verbose=True):
    res = {}
    res["algebra_checks"] = check_algebra()
    D8 = derivations()
    chk, D7 = g2_checks(D8)
    res["g2_checks"] = chk
    res["transitivity"] = transitivity_ranks(D7)
    cw = cartan_and_weights(D7)
    ch = chevalley_normalise(cw)
    W = weyl_group(list(cw["roots"].keys()), ch["G"])
    res["cartan"] = {"pairs_from_L_e7": cw["pairs"], "H_coeffs": [h[0] for h in cw["H"]],
                     "centraliser_dim": cw["cent_dim"], "weights_of_7": [list(map(int, w)) for w in cw["wts"]],
                     "weight_vectors": cw["labels"], "n_roots": len(cw["roots"]),
                     "roots": sorted([list(map(int, r)) for r in cw["roots"]]),
                     "positive_roots": sorted([list(map(int, r)) for r in ch["pos"]]),
                     "simple_roots(short,long)": [list(map(int, r)) for r in ch["simple"]],
                     "E_rational_after_normalisation": bool(ch["rationalE"]),
                     "F_rational_after_normalisation": bool(ch["rationalF"]),
                     "weyl_group_order": len(W)}
    return res, D7, cw, ch, W


if __name__ == "__main__":
    import json
    res, D7, cw, ch, W = build_all()
    print(json.dumps(res, indent=1, default=str))
