"""
cc2_exact_invariants.py -- second-pass cross-check (written in the resumed cross-check session).

A THIRD method for the F21 invariant counting, different from both the original (numerical null spaces
of the generator equations) and the first cross-check pass (characters / Reynolds projector):

  Every F21 irrep is realised in a D-diagonal *monomial* basis:
      D e_a = zeta7^{w_a} e_a,     C e_a = (root of unity) e_{pi(a)}.
  Tensor products, conjugates, Sym^2 and Alt^2 of monomial reps are again monomial.  An invariant vector
  must have total D-weight 0 mod 7 (exact integer test) and be constant (up to the phases) along the
  C-orbits; a C-orbit carries an invariant iff the product of phases around it is 1.  So invariant
  counts and the invariant tensors themselves are EXACT integer combinatorics (phases as exponents
  mod 42), with no floating point and no group averaging.

Checks:
  * the relations D^7 = C^3 = 1, C^-1 D C = D^4 hold for each monomial irrep (so they are reps);
  * F21 Kronecker products (all pairs, with Sym/Alt split) = report / LNR;
  * Dirac coupling table L-bar x R x H (L, R in {3, 3b, 1+1'+1''}, H in every irrep) = report;
  * Majorana N N Phi counts = report;
  * closed-form Dirac matrices for L=R=3, H = 3, 3b, 1' = report;
  * psi psi' xi xi' (3 3 3b 3b): 5 invariants, and the general Dirac matrix built from them equals LNR's
    displayed M_Dir form (diagonal c0 u'_i u_i; orbit {(1,2),(2,3),(3,1)}: gamma1 u'_i u_j + gamma2 u'_j u_i;
    orbit {(1,3),(2,1),(3,2)}: beta1 ..., beta2 ...);
  * Sym^2(3) x Sym^2(3b): 2 invariants -> LNR's M_Maj = diag(u_i^2) + alpha (u_i u_j)_{i!=j};
  * residual-symmetry obstruction, exactly: no symmetric M on the 3 is Z7-invariant; Z3-invariant
    symmetric M has a degenerate pair (sympy, all 7 Z3 subgroups).
Writes out/exact_invariants_cc2.json.
"""
import itertools, json, collections
import sympy as sp

OUT, CHECKS = {}, {}
def check(name, ok):
    CHECKS[name] = bool(ok); print(("PASS " if ok else "FAIL ") + name)

N = 42                      # phases as exponents of zeta42: zeta7 = z^6, omega = z^14, -1 = z^21
W7, W3, NEG = 6, 14, 21

class Mono:
    """monomial rep: list of (D-weight mod 7, C-image index, C-phase exponent mod 42)"""
    def __init__(self, w, pi, ph, name=""):
        self.w, self.pi, self.ph, self.name = list(w), list(pi), list(ph), name
        self.d = len(w)
    def conj(self):
        return Mono([(-x) % 7 for x in self.w], self.pi, [(-p) % N for p in self.ph], self.name + "*")
    def is_rep(self):
        d = self.d
        # C^3 = 1
        ok = True
        for a in range(d):
            b, tot = a, 0
            for _ in range(3):
                tot += self.ph[b]; b = self.pi[b]
            ok &= (b == a and tot % N == 0)
        # D C = C D^4  <=>  w[pi(a)] = 4 w[a] mod 7 ; D^7 = 1 trivially (weights mod 7)
        ok &= all((self.w[self.pi[a]] - 4 * self.w[a]) % 7 == 0 for a in range(d))
        return ok

def tensor(*reps):
    idx = list(itertools.product(*[range(r.d) for r in reps]))
    pos = {t: k for k, t in enumerate(idx)}
    w = [sum(r.w[i] for r, i in zip(reps, t)) % 7 for t in idx]
    pi = [pos[tuple(r.pi[i] for r, i in zip(reps, t))] for t in idx]
    ph = [sum(r.ph[i] for r, i in zip(reps, t)) % N for t in idx]
    m = Mono(w, pi, ph, "x".join(r.name for r in reps)); m.labels = idx
    return m

def sym2(r, anti=False):
    """Sym^2 / Alt^2 of a monomial rep: basis e_i e_j (i<=j) or e_i ^ e_j (i<j)"""
    idx = [(i, j) for i in range(r.d) for j in range(i, r.d) if (i < j or not anti)]
    pos = {t: k for k, t in enumerate(idx)}
    w, pi, ph = [], [], []
    for (i, j) in idx:
        a, b = r.pi[i], r.pi[j]
        p = (r.ph[i] + r.ph[j]) % N
        if a > b:
            a, b = b, a
            if anti: p = (p + NEG) % N
        w.append((r.w[i] + r.w[j]) % 7); pi.append(pos[(a, b)]); ph.append(p)
    m = Mono(w, pi, ph, ("A2" if anti else "S2") + "(" + r.name + ")"); m.labels = idx
    return m

def direct_sum(*reps):
    w, pi, ph, off = [], [], [], 0
    for r in reps:
        w += r.w; pi += [off + x for x in r.pi]; ph += r.ph; off += r.d
    return Mono(w, pi, ph, "+".join(r.name for r in reps))

def invariants(r):
    """exact invariant vectors: dict basis-index -> phase exponent (coefficient zeta42^e), one per good orbit"""
    seen, inv = set(), []
    for a in range(r.d):
        if a in seen or r.w[a] % 7: continue
        orb, b = [a], r.pi[a]
        while b != a:
            orb.append(b); b = r.pi[b]
        seen |= set(orb)
        # C e_t = z^{ph_t} e_{pi t};  invariant v = sum c_t e_t needs c_{pi t} = z^{ph_t} c_t
        coef, e, t = {a: 0}, 0, a
        for _ in range(len(orb) - 1):
            e = (e + r.ph[t]) % N; t = r.pi[t]; coef[t] = e
        if (e + r.ph[t]) % N == 0:           # closes consistently around the orbit
            inv.append(coef)
    return inv

# ---------------------------------------------------------------- F21 irreps in monomial form
T3 = Mono([1, 2, 4], [2, 0, 1], [0, 0, 0], "3")          # C e1 = e3, C e2 = e1, C e3 = e2  (C = [[0,1,0],[0,0,1],[1,0,0]])
T3b = T3.conj(); T3b.name = "3b"
S1 = Mono([0], [0], [0], "1"); S1p = Mono([0], [0], [W3], "1'"); S1pp = Mono([0], [0], [2 * W3], "1''")
IRR = {"1": S1, "1'": S1p, "1''": S1pp, "3": T3, "3b": T3b}
check("monomial F21 irreps satisfy D^7 = C^3 = 1, C^-1 D C = D^4", all(r.is_rep() for r in IRR.values()))
# identify my monomial 3 with the matrices: D = diag(z, z^2, z^4); C columns e3, e1, e2  -> identical by construction
DUAL = {"1": "1", "1'": "1''", "1''": "1'", "3": "3b", "3b": "3"}

def n_inv(r): return len(invariants(r))
def mult(c, r):  # multiplicity of irrep c in rep r = # invariants of c-bar x r
    return n_inv(tensor(IRR[DUAL[c]], r))

labs = ["1", "1'", "1''", "3", "3b"]
kron = {}
for i, a in enumerate(labs):
    for b in labs[i:]:
        if a == b:
            S, A = sym2(IRR[a]), sym2(IRR[a], anti=True)
            kron[f"{a} x {b}"] = {"sym": {c: mult(c, S) for c in labs if mult(c, S)},
                                  "antisym": {c: mult(c, A) for c in labs if mult(c, A)}}
        else:
            P = tensor(IRR[a], IRR[b])
            kron[f"{a} x {b}"] = {c: mult(c, P) for c in labs if mult(c, P)}
print("  F21 3x3:", kron["3 x 3"], "  3x3b:", kron["3 x 3b"], "  3b x 3b:", kron["3b x 3b"])
print("  1'x1':", kron["1' x 1'"], " 1'x1'':", kron["1' x 1''"], " 1'x3:", kron["1' x 3"])
OUT["F21_kron_monomial"] = kron
check("F21 (monomial, exact): 3x3 = (3+3b)_s + 3b_a ; 3x3b = 1+1'+1''+3+3b ; 3b x 3b = (3+3b)_s + 3_a",
      kron["3 x 3"] == {"sym": {"3": 1, "3b": 1}, "antisym": {"3b": 1}}
      and kron["3 x 3b"] == {"1": 1, "1'": 1, "1''": 1, "3": 1, "3b": 1}
      and kron["3b x 3b"] == {"sym": {"3": 1, "3b": 1}, "antisym": {"3": 1}})
check("F21 (monomial): 1'x1' = 1'' (sym), 1'x1'' = 1, 1'x3 = 3, 1'x3b = 3b",
      kron["1' x 1'"] == {"sym": {"1''": 1}, "antisym": {}} and kron["1' x 1''"] == {"1": 1}
      and kron["1' x 3"] == {"3": 1} and kron["1' x 3b"] == {"3b": 1})

# ---------------------------------------------------------------- Dirac coupling table  L-bar x R x H
SUM3 = direct_sum(S1, S1p, S1pp); SUM3.name = "1+1'+1''"
REPS = {"3": T3, "3b": T3b, "1+1'+1''": SUM3}
rows = [("3", "3"), ("3", "3b"), ("3", "1+1'+1''"), ("1+1'+1''", "1+1'+1''")]
tab = {f"{l},{r}": [n_inv(tensor(REPS[l].conj(), REPS[r], IRR[h])) for h in labs] for l, r in rows}
for k, v in tab.items(): print(f"  Dirac couplings L,R = {k:20s} H = {labs}: {v}")
OUT["F21_dirac_table_monomial"] = tab
check("Dirac coupling table (exact monomial count) = report's table",
      tab == {"3,3": [1, 1, 1, 1, 1], "3,3b": [0, 0, 0, 1, 2], "3,1+1'+1''": [0, 0, 0, 3, 0], "1+1'+1'',1+1'+1''": [3, 3, 3, 0, 0]})
maj = {h: n_inv(tensor(sym2(T3), IRR[h])) for h in labs}
print("  Majorana N N Phi (N in 3):", maj)
OUT["F21_majorana_monomial"] = maj
check("Majorana N=3 (exact): only Phi = 3 and 3b (one each), no singlet", maj == {"1": 0, "1'": 0, "1''": 0, "3": 1, "3b": 1})

# ---------------------------------------------------------------- explicit tensors -> mass matrices (sympy)
z42 = sp.exp(2 * sp.pi * sp.I / N)
def tensor_coeffs(rep_list):
    t = tensor(*rep_list)
    return [{t.labels[k]: sp.nsimplify(z42 ** e) for k, e in v.items()} for v in invariants(t)], t

h1, h2, h3 = sp.symbols("h1 h2 h3"); hv = [h1, h2, h3]
def dirac_form(H):
    invs, _ = tensor_coeffs([T3.conj(), T3, IRR[H]])
    assert len(invs) == 1
    M = sp.zeros(3, 3)
    for (i, j, k), c in invs[0].items():
        M[i, j] += c * (hv[k] if IRR[H].d == 3 else 1)
    return sp.simplify(M)
M3, M3b, M1p = dirac_form("3"), dirac_form("3b"), dirac_form("1'")
print("  L=R=3, H=3 :", M3.tolist()); print("  L=R=3, H=3b:", M3b.tolist()); print("  L=R=3, H=1':", M1p.tolist())
w = sp.exp(2 * sp.pi * sp.I / 3)
check("closed forms: H=3 -> [[0,0,h3],[h1,0,0],[0,h2,0]]; H=3b -> [[0,h1,0],[0,0,h2],[h3,0,0]]; H=1' -> diag(1,w^a,w^2a)",
      M3 == sp.Matrix([[0, 0, h3], [h1, 0, 0], [0, h2, 0]]) and M3b == sp.Matrix([[0, h1, 0], [0, 0, h2], [h3, 0, 0]])
      and all(sp.simplify(abs(M1p[i, i]) - 1) == 0 for i in range(3)) and sp.simplify(M1p - sp.diag(*[M1p[i, i] for i in range(3)])) == sp.zeros(3, 3)
      and sp.simplify(M1p[0, 0] + M1p[1, 1] + M1p[2, 2]) == 0)

# ---------------------------------------------------------------- the LNR operator  psi(3) psi'(3) xi(3b) xi'(3b)
invs, t4 = tensor_coeffs([T3, T3, T3b, T3b])
print("  psi psi' xi xi' invariants:", len(invs))
check("F21 invariants of 3 x 3 x 3b x 3b = 5 (exact monomial count)", len(invs) == 5)
# symmetric: Sym^2(3) x Sym^2(3b)
n_sym = n_inv(tensor(sym2(T3), sym2(T3b)))
check("F21 invariants of Sym^2(3) x Sym^2(3b) = 2", n_sym == 2)
OUT["psi_psi_xi_xi_invariants"] = {"general": len(invs), "symmetric": n_sym}
# Dirac matrix M_ij for psi5_i psi1_j phi5_k phi1_l : u' = <phi5> (row field), u = <phi1> (column field)
up = sp.symbols("ap bp cp"); u = sp.symbols("a b c"); cc = sp.symbols("k0:5")
Mgen = sp.zeros(3, 3)
for a_, inv in enumerate(invs):
    for (i, j, k, l), c in inv.items():
        Mgen[i, j] += cc[a_] * c * up[k] * u[l]
Mgen = sp.expand(Mgen)
# LNR's displayed form
a, b, c = u; ap, bp, cp = up
g1, g2, b1, b2, k0 = sp.symbols("gamma1 gamma2 beta1 beta2 c0")
M_LNR = sp.Matrix([[ap * a, g1 * ap * b + g2 * bp * a, b1 * ap * c + b2 * cp * a],
                   [b1 * bp * a + b2 * ap * b, bp * b, g1 * bp * c + g2 * cp * b],
                   [g1 * cp * a + g2 * ap * c, b1 * cp * b + b2 * bp * c, cp * c]])
# compare: span of coefficient tensors.  Each invariant is a monomial pattern; show the linear map from
# (k0..k4) to (c0, gamma1, gamma2, beta1, beta2) is a bijection (up to the overall c0 normalisation of LNR's I3).
pattern = {}
for i in range(3):
    for j in range(3):
        poly = sp.Poly(Mgen[i, j], *up, *u)
        for mon, coef in poly.terms():
            pattern.setdefault((i, j, mon), coef)
# group by which k appears: each invariant must reproduce one of LNR's five structures
structs = []
for a_ in range(5):
    Ma = Mgen.subs({cc[x]: (1 if x == a_ else 0) for x in range(5)})
    structs.append(Ma)
LNR_structs = {"c0 (I3)": M_LNR.subs({g1: 0, g2: 0, b1: 0, b2: 0}),
               "gamma1": M_LNR.subs({g1: 1, g2: 0, b1: 0, b2: 0}) - M_LNR.subs({g1: 0, g2: 0, b1: 0, b2: 0}),
               "gamma2": M_LNR.subs({g1: 0, g2: 1, b1: 0, b2: 0}) - M_LNR.subs({g1: 0, g2: 0, b1: 0, b2: 0}),
               "beta1": M_LNR.subs({g1: 0, g2: 0, b1: 1, b2: 0}) - M_LNR.subs({g1: 0, g2: 0, b1: 0, b2: 0}),
               "beta2": M_LNR.subs({g1: 0, g2: 0, b1: 0, b2: 1}) - M_LNR.subs({g1: 0, g2: 0, b1: 0, b2: 0})}
match = {}
for nm, S in LNR_structs.items():
    for a_, Ma in enumerate(structs):
        r = None
        nz = [(i, j) for i in range(3) for j in range(3) if S[i, j] != 0]
        if all(sp.simplify(Ma[i, j]) == 0 for i in range(3) for j in range(3) if S[i, j] == 0):
            ratios = {sp.simplify(Ma[i, j] / S[i, j]) for (i, j) in nz}
            if len(ratios) == 1 and list(ratios)[0] != 0: match[nm] = (a_, str(list(ratios)[0]))
print("  LNR structure <-> exact invariant (index, ratio):", match)
check("the 5 exact F21 invariants are exactly LNR's five M_Dir structures (I3 diagonal; gamma1,2 on {(1,2),(2,3),(3,1)}; beta1,2 on {(1,3),(2,1),(3,2)})",
      len(match) == 5 and len({m[0] for m in match.values()}) == 5)
OUT["LNR_Mdir_structure_match"] = match
# Majorana from Sym^2(3) x Sym^2(3b)
S2a, S2b = sym2(T3), sym2(T3b)
t = tensor(S2a, S2b); invM = invariants(t)
al = sp.symbols("alpha")
Mm = [sp.zeros(3, 3) for _ in invM]
for a_, inv in enumerate(invM):
    for k, e in inv.items():
        pa, pb = t.labels[k]
        (i, j), (k1, l1) = S2a.labels[pa], S2b.labels[pb]
        val = sp.nsimplify(z42 ** e) * u[k1] * u[l1]
        Mm[a_][i, j] += val
        if i != j: Mm[a_][j, i] += val
forms = sorted([sp.simplify(m) for m in Mm], key=lambda m: str(m))
diagform = sp.diag(a * a, b * b, c * c)
offform = sp.Matrix([[0, a * b, a * c], [a * b, 0, b * c], [a * c, b * c, 0]])
okM = any(sp.simplify(f - diagform) == sp.zeros(3, 3) for f in forms) and any(sp.simplify(f - offform) == sp.zeros(3, 3) for f in forms)
check("Sym^2 invariants = diag(u_i^2) and (u_i u_j)_{i!=j}: LNR's M_Maj = diag + alpha offdiag", okM)

# ---------------------------------------------------------------- residual-symmetry obstruction, exact
zeta = sp.exp(2 * sp.pi * sp.I / 7)
Dm = sp.diag(zeta, zeta ** 2, zeta ** 4); Cm = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
m = sp.symbols("m0:6"); Msym = sp.Matrix([[m[0], m[1], m[2]], [m[1], m[3], m[4]], [m[2], m[4], m[5]]])
sol7 = sp.solve(list(Dm.T * Msym * Dm - Msym), m, dict=True)
z7_zero = (len(sol7) == 1 and all(sol7[0].get(x, x) == 0 for x in m))
degenerate = []
for k in range(7):
    g = Dm ** k * Cm * Dm ** (-k)          # the 7 Sylow-3 subgroups <D^k C D^-k>
    sol = sp.solve(list(sp.simplify(g.T * Msym * g - Msym)), m, dict=True)[0]
    Mz = Msym.subs(sol)
    free = sorted(Mz.free_symbols, key=str)
    # numerical Takagi values at a random complex point (exact structure, numeric spectrum)
    import random
    random.seed(k)
    vals = {s: complex(random.gauss(0, 1), random.gauss(0, 1)) for s in free}
    import numpy as np
    Mn = np.array(Mz.subs(vals).evalf(), dtype=complex)
    sv = np.sort(np.linalg.svd(Mn, compute_uv=False))
    degenerate.append((len(free), bool(min(np.diff(sv)) < 1e-9)))
print("  Z7-invariant symmetric M on the 3:", sol7, "  Z3 subgroups (free params, degenerate pair):", degenerate)
check("exact: Z7 = <D> admits no nonzero symmetric Majorana matrix on the 3; each of the 7 Z3 leaves 2 parameters and a degenerate pair",
      z7_zero and all(d == (2, True) for d in degenerate))

OUT["checks"] = CHECKS; OUT["all_pass"] = all(CHECKS.values())
json.dump(OUT, open("/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/exact_invariants_cc2.json", "w"), indent=1, default=str)
print(f"\n{sum(CHECKS.values())}/{len(CHECKS)} checks pass")
