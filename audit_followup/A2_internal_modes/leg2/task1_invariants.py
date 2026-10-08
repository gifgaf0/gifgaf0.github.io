"""A2 leg 2 -- Task 1 (invariant counts) and Task 2 (explicit T-even basis, group (c), R^14).

Method A (primary, exact): complex coordinates z = psi, w = psi-bar (16 -> 2x8 independent complex
coordinates), rewritten in the rational (Chevalley-normalised) weight basis of the 7 derived in
octonion_g2.py.  For a compact connected group, f is g2-invariant iff f has weight 0 for the Cartan
AND is annihilated by the raising operators of the two simple roots (a weight-0 highest-weight vector
generates the trivial module).  The u(1)'s act diagonally on monomials (gradings), Z3 is a congruence on
the u(1)_7 grading, and T is the swap z <-> w (a permutation of monomials).  The kernel is computed
with exact integer linear algebra (FLINT fmpz_mat rank).  No invariant generators are assumed.

Method B (independent cross-check, exact): Molien-Weyl integral over the derived maximal torus with the
derived root system and Weyl group order (|W| computed by generating the reflection group):
   dim (Sym^p 7 (x) Sym^q 7)^G2 = (1/|W|) CT[ h_p h_q prod_{alpha}(1 - t^alpha) ]
and the T-trace on the p = q blocks:  tr(T | Inv(p,p)) = (1/|W|) CT[ h_p(t^2) prod(1 - t^alpha) ]
(swap trace identity tr((g(x)g) o swap) = tr(g^2)).

Method C (low-degree sanity check, floating point, REAL coordinates u, v): kernel of the PSD operator
sum_X D_X^T D_X for the 14 derived real derivations (+ the u(1) derivations), Z3 from the u(1)_7 charge
spectrum on the kernel, T-even part from the trace of T = (-1)^{deg v}.
"""
import itertools
import json
import math
import sys
import time
from collections import defaultdict

import numpy as np
import scipy.sparse as sps
import sympy as sp
from flint import fmpz_mat

import octonion_g2 as og

T0 = time.time()
RES, D7, CW, CH, WEYL = og.build_all()
WTS = [tuple(int(x) for x in w) for w in CW["wts"]]
SIMPLE = CH["simple"]
EMATS = {r: [[int(M[a, b]) for b in range(7)] for a in range(7)] for r, M in CH["E"].items()}
FMATS = {r: [[sp.Rational(M[a, b]) for b in range(7)] for a in range(7)] for r, M in CH["F"].items()}
# F's are rational up to scale; make integer
for r in list(FMATS):
    den = sp.ilcm(*[sp.fraction(x)[1] for row in FMATS[r] for x in row])
    FMATS[r] = [[int(x * den) for x in row] for row in FMATS[r]]
ROOTS = [tuple(map(int, r)) for r in CW["roots"].keys()]

# variable layout: 0..6 z'_a, 7..13 w'_a, 14 z0, 15 w0
def var_weight(i):
    if i < 7:
        return WTS[i]
    if i < 14:
        return WTS[i - 7]
    return (0, 0)


def charges(e, n):
    nz7 = sum(e[0:7]); nw7 = sum(e[7:14])
    nz0 = e[14] if n == 16 else 0
    nw0 = e[15] if n == 16 else 0
    return dict(glob=nz7 + nz0 - nw7 - nw0, psi0=nz0 - nw0, c7=nz7 - nw7, p=nz7, q=nw7, a=nz0, b=nw0)


def group_ok(ch, group):
    if group == "a":
        return ch["glob"] == 0
    if group == "b":
        return ch["psi0"] == 0
    if group == "c":
        return ch["psi0"] == 0 and ch["c7"] % 3 == 0
    if group == "g2only":
        return True
    raise ValueError(group)


def monomials(n, d):
    for combo in itertools.combinations_with_replacement(range(n), d):
        e = [0] * n
        for i in combo:
            e[i] += 1
        yield tuple(e)


def weight(e):
    w0 = w1 = 0
    for i, k in enumerate(e):
        if k:
            wi = var_weight(i)
            w0 += k * wi[0]; w1 += k * wi[1]
    return (w0, w1)


def T_of(e, n):
    if n == 16:
        return tuple(e[7:14]) + tuple(e[0:7]) + (e[15], e[14])
    return tuple(e[7:14]) + tuple(e[0:7])


def apply_D(Emat, e):
    """D_E = sum_ab E_ab (z'_b d/dz'_a + w'_b d/dw'_a) applied to monomial e -> dict monomial->coeff."""
    out = defaultdict(int)
    for off in (0, 7):
        for a in range(7):
            ea = e[off + a]
            if not ea:
                continue
            for b in range(7):
                c = Emat[a][b]
                if c:
                    f = list(e)
                    f[off + a] -= 1
                    f[off + b] += 1
                    out[tuple(f)] += c * ea
    return out


def kernel_dim(cols_polys, ops):
    """cols_polys: list of dict(monomial->coeff) spanning the source space (assumed independent);
    ops: list of operator matrices; returns (dim source, rank, kernel dim)."""
    rowidx = {}
    entries = []
    for j, poly in enumerate(cols_polys):
        for oi, Emat in enumerate(ops):
            acc = defaultdict(int)
            for m, c in poly.items():
                for mm, cc in apply_D(Emat, m).items():
                    acc[mm] += c * cc
            for mm, cc in acc.items():
                if cc:
                    key = (oi, mm)
                    if key not in rowidx:
                        rowidx[key] = len(rowidx)
                    entries.append((rowidx[key], j, cc))
    nr, nc = len(rowidx), len(cols_polys)
    if nc == 0:
        return 0, 0, 0
    if nr == 0:
        return nc, 0, nc
    M = fmpz_mat(nr, nc)
    for (r, c, v) in entries:
        M[r, c] = M[r, c] + v
    rk = M.rank()
    return nc, rk, nc - rk


def count(n, d, group, extra=None, ops_mode="simple"):
    """Return (all, T-even) invariant dimensions on R^n (n = 14 or 16) at degree d."""
    V0 = []
    for e in monomials(n, d):
        if weight(e) != (0, 0):
            continue
        ch = charges(e, n)
        if not group_ok(ch, group):
            continue
        if extra and not extra(ch):
            continue
        V0.append(e)
    if ops_mode == "simple":
        ops = [EMATS[SIMPLE[0]], EMATS[SIMPLE[1]]]
    elif ops_mode == "allpos":
        ops = list(EMATS.values())
    elif ops_mode == "allroots":
        ops = list(EMATS.values()) + list(FMATS.values())
    else:
        raise ValueError
    cols = [{e: 1} for e in V0]
    nall, rall, kall = kernel_dim(cols, ops)
    # T-even: orbit sums
    seen = set()
    orb = []
    for e in V0:
        if e in seen:
            continue
        t = T_of(e, n)
        seen.add(e); seen.add(t)
        orb.append({e: 1} if t == e else {e: 1, t: 1})
    neven, reven, keven = kernel_dim(orb, ops)
    return dict(all=kall, T_even=keven, dimV0=nall, rank=rall, dimV0_even=neven, rank_even=reven)


# ----------------------------------------------------------------------------------------------
# Method B: Molien-Weyl
def lp_mul(A, B):
    out = defaultdict(int)
    for k1, v1 in A.items():
        for k2, v2 in B.items():
            out[(k1[0] + k2[0], k1[1] + k2[1])] += v1 * v2
    return {k: v for k, v in out.items() if v}


def h_series(weights, P):
    """h[p] = complete homogeneous symmetric polynomial of degree p in t^{weights} (Laurent dicts)."""
    h = [dict() for _ in range(P + 1)]
    h[0] = {(0, 0): 1}
    for w in weights:
        # multiply generating function by 1/(1 - x t^w)
        new = [dict() for _ in range(P + 1)]
        for p in range(P + 1):
            acc = defaultdict(int)
            for k in range(p + 1):
                for key, v in h[p - k].items():
                    acc[(key[0] + k * w[0], key[1] + k * w[1])] += v
            new[p] = {kk: vv for kk, vv in acc.items() if vv}
        h = new
    return h


def molien_weyl(P=6):
    Wn = len(WEYL)
    Delta = {(0, 0): 1}
    for r in ROOTS:
        Delta = lp_mul(Delta, {(0, 0): 1, r: -1})
    ct = lambda F: sum(v * Delta.get((-k[0], -k[1]), 0) for k, v in F.items())
    h = h_series(WTS, P)
    h2 = h_series([(2 * w[0], 2 * w[1]) for w in WTS], P)
    I = {}
    for p in range(P + 1):
        for q in range(P + 1 - p):
            val = ct(lp_mul(h[p], h[q]))
            assert val % Wn == 0
            I[(p, q)] = val // Wn
    Jt = {}
    for p in range(P // 2 + 1):
        val = ct(h2[p])
        assert val % Wn == 0
        Jt[p] = val // Wn
    # controls
    e3 = defaultdict(int)
    for c in itertools.combinations(range(7), 3):
        k = tuple(sum(WTS[i][j] for i in c) for j in range(2))
        e3[k] += 1
    e2 = defaultdict(int)
    for c in itertools.combinations(range(7), 2):
        k = tuple(sum(WTS[i][j] for i in c) for j in range(2))
        e2[k] += 1
    controls = {"trivial": ct({(0, 0): 1}) // Wn, "Lambda2(7)": ct(e2) // Wn, "Lambda3(7)": ct(e3) // Wn,
                "Sym2(7)": I[(2, 0)], "Sym3(7)": I[(3, 0)]}
    return I, Jt, controls


def assemble(I, Jt, d, n, group):
    """Assemble group counts on R^n at degree d from the bigraded G2-invariant dims I(p,q) and the T-traces."""
    tot = 0
    trace = 0
    rng = range(d + 1)
    for a in (rng if n == 16 else [0]):
        for b in (rng if n == 16 else [0]):
            for p in rng:
                q = d - a - b - p
                if q < 0:
                    continue
                ch = dict(glob=p + a - q - b, psi0=a - b, c7=p - q)
                if not group_ok(ch, group):
                    continue
                tot += I[(p, q)]
                if a == b and p == q:
                    trace += Jt[p]
    # T pairs blocks (a,b,p,q) <-> (b,a,q,p); trace only from self-paired blocks
    return dict(all=tot, T_even=(tot + trace) // 2)


# ----------------------------------------------------------------------------------------------
# Method C: real coordinates, floating point, degrees 2 and 4.
def methodC(n, d):
    """Real coordinates: R^14 = (u_1..u_7, v_1..v_7); R^16 adds (u_0, v_0) as last two coordinates."""
    D7f = [np.array(D.tolist(), dtype=float) for D in D7]
    mons = list(monomials(n, d))
    idx = {m: i for i, m in enumerate(mons)}
    N = len(mons)

    def deriv_matrix(lin):  # lin: n x n matrix L, vector field x -> L x ; D = sum_ab L_ab x_b d/dx_a
        rows, cols, vals = [], [], []
        for j, m in enumerate(mons):
            for a in range(n):
                if m[a] == 0:
                    continue
                for b in range(n):
                    c = lin[a, b]
                    if c == 0:
                        continue
                    f = list(m); f[a] -= 1; f[b] += 1
                    rows.append(idx[tuple(f)]); cols.append(j); vals.append(c * m[a])
        return sps.csr_matrix((vals, (rows, cols)), shape=(N, N))

    def embed(D):
        L = np.zeros((n, n))
        L[0:7, 0:7] = D
        L[7:14, 7:14] = D
        return L
    G = [deriv_matrix(embed(D)) for D in D7f]
    J7 = np.zeros((n, n))
    for k in range(7):  # u_k -> -v_k ... vector field (u,v) -> (-v, u)
        J7[k, 7 + k] = -1.0
        J7[7 + k, k] = 1.0
    J0 = np.zeros((n, n))
    if n == 16:
        J0[14, 15] = -1.0
        J0[15, 14] = 1.0
    DJ7 = deriv_matrix(J7)
    DJ0 = deriv_matrix(J0)
    Tdiag = np.array([(-1) ** (sum(m[7:14]) + (m[15] if n == 16 else 0)) for m in mons], dtype=float)

    def null_basis(ops):
        M = sum((o.T @ o) for o in ops).toarray()
        w, V = np.linalg.eigh(M)
        tol = 1e-8 * max(1.0, w.max())
        k = int((w < tol).sum())
        gap = (w[k] if k < len(w) else float("nan"))
        return V[:, :k], k, gap

    out = {}
    for grp in ("a", "b", "c"):
        if grp == "a":
            K, k, gap = null_basis(G + [DJ7 + DJ0])
        else:
            K, k, gap = null_basis(G + ([DJ0] if n == 16 else []))
        if grp == "c":
            # Z3 on the 7-sector: keep u(1)_7 charges = 0 mod 3; J7 restricted to K is antisymmetric
            A = K.T @ (DJ7 @ K)
            ev, U = np.linalg.eig(A)
            charges_ = np.round(ev.imag).astype(int)
            assert np.allclose(ev.imag, charges_, atol=1e-6)
            sel = (charges_ % 3 == 0)
            Uc = U[:, sel]
            # real orthonormal basis of the selected (conjugation-closed) subspace
            Rb = np.hstack([Uc.real, Uc.imag])
            q, r = np.linalg.qr(Rb)
            s = np.linalg.svd(Rb, compute_uv=False)
            rk = int((s > 1e-8 * s.max()).sum()) if s.size else 0
            uu, ss, vh = np.linalg.svd(Rb, full_matrices=False)
            Bsel = uu[:, :rk]
            K = K @ Bsel
            k = rk
        tr = float(np.trace(K.T @ (Tdiag[:, None] * K))) if k else 0.0
        out[grp] = dict(all=k, T_even=int(round((k + tr) / 2)), trace_T=round(tr, 8), gap=float(gap))
    return out


def task2_basis():
    """Explicit T-even basis for group (c) on R^14 at degrees 2,4,6, checked against the machine dims;
    then evaluation on the polar orbit psi_7 = e^{i theta} n."""
    z = sp.symbols("z1:8"); w = sp.symbols("w1:8")
    N = sum(z[i] * w[i] for i in range(7)); S = sum(z[i] ** 2 for i in range(7)); Sb = sum(w[i] ** 2 for i in range(7))
    cand = {2: {"N": N}, 4: {"N^2": N ** 2, "|S|^2": S * Sb},
            6: {"N^3": N ** 3, "N|S|^2": N * S * Sb, "Re(S^3)": (S ** 3 + Sb ** 3) / 2}}
    out = {}
    for d, polys in cand.items():
        # invariance under the 14 derived derivations, acting identically on z and w
        inv_ok = True
        for D in D7:
            for name, f in polys.items():
                Df = sum(D[a, b] * (z[b] * sp.diff(f, z[a]) + w[b] * sp.diff(f, w[a])) for a in range(7) for b in range(7))
                if sp.expand(Df) != 0:
                    inv_ok = False
        # Z3 (z -> omega z, w -> omega^-1 w), T (z <-> w)
        def z3inv(f):
            P = sp.Poly(sp.expand(f), *z, *w)
            return all((sum(m[:7]) - sum(m[7:])) % 3 == 0 for m in P.monoms())
        def teven(f):
            g = f.subs({**{z[i]: w[i] for i in range(7)}, **{w[i]: z[i] for i in range(7)}}, simultaneous=True)
            return sp.expand(g - f) == 0
        # linear independence of the coefficient vectors
        allmons = set()
        Ps = {k: sp.Poly(sp.expand(f), *z, *w) for k, f in polys.items()}
        for P in Ps.values():
            allmons |= set(P.monoms())
        allmons = sorted(allmons)
        Mx = sp.Matrix([[P.coeff_monomial(m) for m in allmons] for P in Ps.values()])
        out[d] = dict(names=list(polys), invariant_under_14_derivations=inv_ok,
                      Z3_invariant=all(z3inv(f) for f in polys.values()),
                      T_even=all(teven(f) for f in polys.values()), rank=int(Mx.rank()))
    # polar-orbit evaluation: psi = e^{i th} n, n real unit
    rng = np.random.default_rng(7)
    nvec = rng.normal(size=7); nvec /= np.linalg.norm(nvec)
    thetas = np.linspace(0, np.pi, 7)
    evals = {}
    for d, polys in cand.items():
        for name, f in polys.items():
            fl = sp.lambdify(list(z) + list(w), f, "numpy")
            vals = []
            for th in thetas:
                psi = np.exp(1j * th) * nvec
                vals.append(complex(fl(*psi, *np.conj(psi))))
            evals[name] = [round(v.real, 10) for v in vals]
    return out, thetas.tolist(), evals


def task2_machine_kernel_on_polar():
    """Machine-side check without using the candidates: exact kernel of group (c), T-even, degree 6 on
    R^14 (FLINT nullspace), each kernel polynomial mapped back to original coordinates through the
    weight basis and evaluated on psi = e^{i th} n; report how many independent theta-dependent
    directions the kernel contains."""
    n, d = 14, 6
    V0 = [e for e in monomials(n, d) if weight(e) == (0, 0) and group_ok(charges(e, n), "c")]
    seen = set(); orb = []
    for e in V0:
        if e in seen:
            continue
        t = T_of(e, n); seen |= {e, t}
        orb.append({e: 1} if t == e else {e: 1, t: 1})
    ops = [EMATS[SIMPLE[0]], EMATS[SIMPLE[1]]]
    rowidx = {}; entries = []
    for j, poly in enumerate(orb):
        for oi, Emat in enumerate(ops):
            acc = defaultdict(int)
            for m, c in poly.items():
                for mm, cc in apply_D(Emat, m).items():
                    acc[mm] += c * cc
            for mm, cc in acc.items():
                if cc:
                    key = (oi, mm)
                    rowidx.setdefault(key, len(rowidx))
                    entries.append((rowidx[key], j, cc))
    M = fmpz_mat(len(rowidx), len(orb))
    for r, c, v in entries:
        M[r, c] = M[r, c] + v
    X, nul = M.nullspace()
    # check exactly A X = 0 on the first nul columns
    Xl = X.tolist()
    kern = [[int(Xl[i][k]) for i in range(len(orb))] for k in range(nul)]
    # map weight coords: z' = Bn^{-1} z, w' = Bn^{-1} w
    Bn = np.array(CH["Bn"].evalf().tolist(), dtype=complex)
    Bi = np.linalg.inv(Bn)
    rng = np.random.default_rng(11)
    nvec = rng.normal(size=7); nvec /= np.linalg.norm(nvec)
    thetas = np.linspace(0, np.pi / 3, 13)

    def evalpoly(vec, zz, ww):
        tot = 0j
        for j, coef in enumerate(vec):
            if coef == 0:
                continue
            for m, c in orb[j].items():
                val = c * coef
                for i in range(7):
                    if m[i]:
                        val *= zz[i] ** m[i]
                    if m[7 + i]:
                        val *= ww[i] ** m[7 + i]
                tot += val
        return tot
    vals = np.array([[evalpoly(v, Bi @ (np.exp(1j * th) * nvec), Bi @ (np.exp(-1j * th) * nvec)) for th in thetas] for v in kern])
    # theta-dependent directions: rank of the matrix of (values - mean over theta)
    centred = vals - vals.mean(axis=1, keepdims=True)
    sv = np.linalg.svd(centred, compute_uv=False)
    n_theta_dep = int((sv > 1e-8 * max(1.0, np.abs(vals).max())).sum())
    # fit the theta-dependent part to cos(6 theta)
    c6 = np.cos(6 * thetas)
    fits = []
    for row in vals:
        A = np.vstack([np.ones_like(thetas), c6]).T
        coef, resid, *_ = np.linalg.lstsq(A, row.real, rcond=None)
        fits.append(dict(const=round(float(coef[0]), 8), cos6theta=round(float(coef[1]), 8),
                         max_resid=float(np.abs(A @ coef - row.real).max()), max_imag=float(np.abs(row.imag).max())))
    return dict(kernel_dim=int(nul), n_theta_dependent_directions=n_theta_dep, singular_values=sv.tolist(), fits=fits)


if __name__ == "__main__":
    out = {"setup": RES}
    print("=== Setup (derived g2) ===")
    print(json.dumps({k: RES[k] for k in ("algebra_checks", "g2_checks", "transitivity")}, default=str))
    print("Cartan/weights:", json.dumps(RES["cartan"], default=str))

    # ---------------- Method A -----------------
    tA = time.time()
    A = {}
    for n, degs in ((14, (2, 4, 6)), (16, (2, 4, 6))):
        for g in ("a", "b", "c"):
            for d in degs:
                r = count(n, d, g)
                A[f"R{n}_{g}_d{d}"] = r
                print(f"[A] R^{n} group ({g}) degree {d}: all={r['all']} T-even={r['T_even']}  "
                      f"(dim V0={r['dimV0']}, rank={r['rank']}; T-even V0={r['dimV0_even']}, rank={r['rank_even']})", flush=True)
    print(f"[A] time {time.time()-tA:.1f}s")
    # cross-check A with all positive roots / all 12 roots on a subset
    Ax = {}
    for (n, g, d) in ((14, "c", 6), (16, "a", 4), (16, "c", 6), (16, "b", 4)):
        r1 = count(n, d, g, ops_mode="allpos")
        r2 = count(n, d, g, ops_mode="allroots")
        Ax[f"R{n}_{g}_d{d}"] = dict(allpos=(r1["all"], r1["T_even"]), allroots=(r2["all"], r2["T_even"]))
        print(f"[A-x] R^{n} ({g}) d{d}: all-positive-roots {r1['all']}/{r1['T_even']}, all-12-roots {r2['all']}/{r2['T_even']}")
    # bigraded G2-invariant table I(p,q) on the 7-sector by Method A
    IA = {}; ITA = {}
    for p in range(7):
        for q in range(7 - p):
            d = p + q
            r = count(14, d, "g2only", extra=lambda ch, p=p, q=q: ch["p"] == p and ch["q"] == q)
            IA[(p, q)] = r["all"]
            if p == q:
                ITA[p] = r["T_even"]

    # ---------------- Method B -----------------
    IB, JtB, controls = molien_weyl(6)
    print("[B] Molien-Weyl controls:", controls)
    print("[B] I(p,q) = dim (Sym^p 7 x Sym^q 7)^G2 :", {f"{k[0]},{k[1]}": v for k, v in sorted(IB.items())})
    print("[B] tr(T|Inv(p,p)) :", JtB)
    agreeI = all(IA[k] == IB[k] for k in IB)
    agreeT = all(ITA[p] == (IB[(p, p)] + JtB[p]) // 2 for p in JtB)
    print(f"[A vs B] bigraded I(p,q) agree: {agreeI}; T-even (p,p) agree: {agreeT}")
    B = {}
    for n, degs in ((14, (2, 4, 6)), (16, (2, 4, 6))):
        for g in ("a", "b", "c"):
            for d in degs:
                B[f"R{n}_{g}_d{d}"] = assemble(IB, JtB, d, n, g)
    agreeAB = all(A[k]["all"] == B[k]["all"] and A[k]["T_even"] == B[k]["T_even"] for k in B)
    print(f"[A vs B] all group counts agree: {agreeAB}")

    # ---------------- Method C -----------------
    C = {}
    for n in (14, 16):
        for d in (2, 4):
            tC = time.time()
            C[f"R{n}_d{d}"] = methodC(n, d)
            print(f"[C] R^{n} d{d}: {C[f'R{n}_d{d}']}  ({time.time()-tC:.1f}s)", flush=True)
    agreeAC = all(C[f"R{n}_d{d}"][g]["all"] == A[f"R{n}_{g}_d{d}"]["all"] and
                  C[f"R{n}_d{d}"][g]["T_even"] == A[f"R{n}_{g}_d{d}"]["T_even"]
                  for n in (14, 16) for d in (2, 4) for g in ("a", "b", "c"))
    print(f"[A vs C] degrees 2,4 agree: {agreeAC}")

    # ---------------- Task 2 -----------------
    t2, thetas, evals = task2_basis()
    print("[Task2] candidate basis checks:", json.dumps(t2))
    print("[Task2] polar-orbit values over theta =", [round(t, 4) for t in thetas])
    for k, v in evals.items():
        print(f"   {k:8s}: {v}")
    mk = task2_machine_kernel_on_polar()
    print("[Task2] machine kernel (group c, T-even, deg 6, R^14) on polar orbit:", json.dumps(mk))

    table = {}
    for k in A:
        table[k] = {"all": A[k]["all"], "T_even": A[k]["T_even"]}
    out.update(methodA=A, methodA_crosscheck=Ax, methodB={k: v for k, v in B.items()},
               methodB_bigraded={f"{k[0]},{k[1]}": v for k, v in IB.items()},
               methodB_Ttrace=JtB, methodB_controls=controls, methodC=C,
               agree_AB=agreeAB, agree_AC_deg2_4=agreeAC, agree_bigraded=agreeI and agreeT,
               counts=table, task2=dict(candidates=t2, thetas=thetas, polar_values=evals, machine_kernel=mk))
    with open("task1_results.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("\nFINAL TABLE (all / T-even)")
    for n in (14, 16):
        for g in ("a", "b", "c"):
            print(f"R^{n} ({g}): " + "  ".join(f"d{d}: {table[f'R{n}_{g}_d{d}']['all']}/{table[f'R{n}_{g}_d{d}']['T_even']}" for d in (2, 4, 6)))
    print(f"total time {time.time()-T0:.1f}s")
