#!/usr/bin/env python3
"""Independent cross-check of E3 (G2 part): algebra, Dynkin indices, branching,
Casimirs, rotor states.

Methods deliberately different from the original:
  * g2 is built as the stabiliser in so(7) of Bryant's associative 3-form
    phi = e123 + e145 + e167 + e246 - e257 - e347 - e356   (not Der(O) with lines {i,i+1,i+3}).
  * Roots are found numerically from a Cartan subalgebra; SU(2) subgroups are
    built from root vectors.
  * Characters of all irreps up to dim 500 come from the Weyl character formula
    by exact Laurent-polynomial division (integer arithmetic), not Freudenthal.
  * SU(2)_L x SU(2)_S content is obtained by peeling highest weights, not by the
    2D difference formula.
Deterministic; prints its own checks; writes cc_g2.json and cc_g2_basis.npz.
"""
import json, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.linalg import null_space, expm

np.set_printoptions(precision=6, suppress=True, linewidth=150)
checks = []
def check(name, ok, val=None):
    checks.append({"check": name, "pass": bool(ok), "value": val})
    print(("PASS " if ok else "FAIL ") + name + ("" if val is None else f"  [{val}]"))

# ---------------------------------------------------------------- 3-form
phi = np.zeros((7, 7, 7))
terms = [((1, 2, 3), 1), ((1, 4, 5), 1), ((1, 6, 7), 1), ((2, 4, 6), 1),
         ((2, 5, 7), -1), ((3, 4, 7), -1), ((3, 5, 6), -1)]
for (i, j, k), s in terms:
    i, j, k = i - 1, j - 1, k - 1
    for p, sg in [((i, j, k), 1), ((j, k, i), 1), ((k, i, j), 1),
                  ((j, i, k), -1), ((i, k, j), -1), ((k, j, i), -1)]:
        phi[p] = s * sg

# so(7) basis
so7 = []
for i in range(7):
    for j in range(i + 1, 7):
        E = np.zeros((7, 7)); E[i, j] = 1; E[j, i] = -1; so7.append(E)
so7 = np.array(so7)

def act(X, T):  # infinitesimal action of X in gl(7) on a 3-tensor (vector-index convention)
    return (np.einsum('ai,ajk->ijk', X, T) + np.einsum('aj,iak->ijk', X, T)
            + np.einsum('ak,ija->ijk', X, T))

Amat = np.array([act(X, phi).ravel() for X in so7]).T   # 343 x 21
ns = null_space(Amat)
check("dim stab(phi) in so(7) = 14", ns.shape[1] == 14, ns.shape[1])
G = np.einsum('ka,kij->aij', ns, so7)                    # 14 generators 7x7

def Bform(X, Y):
    return -np.trace(X @ Y)

def orthonormalise(mats):
    M = np.array([m.ravel() for m in mats])
    gram = np.array([[Bform(a, b) for b in mats] for a in mats])
    w, V = np.linalg.eigh(gram)
    assert w.min() > 1e-12
    C = V @ np.diag(w ** -0.5) @ V.T
    return np.einsum('ab,bij->aij', C, np.array(mats))

G = orthonormalise(list(G))
# closure and structure constants f_abc: [T_a, T_b] = f_abc T_c
f = np.zeros((14, 14, 14))
res = 0
for a in range(14):
    for b in range(14):
        Cm = G[a] @ G[b] - G[b] @ G[a]
        coef = np.array([Bform(Cm, G[c]) for c in range(14)])
        res = max(res, np.abs(Cm - np.einsum('c,cij->ij', coef, G)).max())
        f[a, b] = coef
check("g2 closed under commutator", res < 1e-12, float(res))
check("f_abc totally antisymmetric", np.abs(f + f.transpose(0, 2, 1)).max() < 1e-12)
# Killing form
ad = np.array([f[a].T for a in range(14)])
K = np.array([[np.trace(ad[a] @ ad[b]) for b in range(14)] for a in range(14)])
check("Killing form = -4 B (B = -Tr_7)", np.abs(K + 4 * np.eye(14)).max() < 1e-10,
      float(np.abs(K + 4 * np.eye(14)).max()))

# ---------------------------------------------------------------- su(3) = stabiliser of e1
v = np.zeros(7); v[0] = 1
Av = np.array([(X @ v) for X in G]).T
ns3 = null_space(Av)
check("stabiliser of a unit imaginary octonion is 8-dim", ns3.shape[1] == 8, ns3.shape[1])
SU3 = orthonormalise(list(np.einsum('ka,kij->aij', ns3, G)))
# complex structure on e1-perp: J_{ij} = phi_{1ij}
J = phi[0]
check("J^2 = -1 on e1-perp", np.allclose((J @ J)[1:, 1:], -np.eye(6)))
check("su(3) commutes with J", max(np.abs(X @ J - J @ X).max() for X in SU3) < 1e-12)
# Casimir of su(3) on 7 (B-orthonormal basis)
C3 = -sum(X @ X for X in SU3)
check("su(3) Casimir on 7: 4/3 (x6), 0 (x1)  => 7 = 3+3bar+1",
      np.allclose(np.sort(np.linalg.eigvalsh(C3)), [0] + [4 / 3] * 6), np.round(np.sort(np.linalg.eigvalsh(C3)), 10).tolist())
C7 = -sum(X @ X for X in G)
check("G2 Casimir on 7 = 2 (long-root normalisation, B-orthonormal basis)", np.allclose(C7, 2 * np.eye(7)))
C14 = -sum(a @ a for a in ad)
check("G2 Casimir on 14 = 4", np.allclose(C14, 4 * np.eye(14)))

# ---------------------------------------------------------------- Cartan, roots
rng = np.random.default_rng(12345)
X0 = np.einsum('a,aij->ij', rng.normal(size=8), SU3)
x0 = np.array([Bform(X0, T) for T in G])
adX0 = np.einsum('a,aij->ij', x0, ad)
cent = null_space(adX0)
check("generic element of su(3) has 2-dim centraliser in g2 (rank 2)", cent.shape[1] == 2, cent.shape[1])
H = cent.T                     # 2 x 14 component vectors (orthonormal in B since components are B-ON)
adH = np.einsum('ra,aij->rij', H, ad)
# simultaneous diagonalisation: diagonalise generic combination
Mgen = adH[0] + np.pi * adH[1]
w, V = np.linalg.eig(Mgen)
roots = []
rootvecs = []
for k in range(14):
    if abs(w[k]) < 1e-8:
        continue
    vec = V[:, k]
    al = np.array([(adH[r] @ vec) @ vec.conj() / (vec @ vec.conj()) for r in range(2)])
    # ad(H_r) vec = i alpha_r vec
    alpha = (al / 1j).real
    roots.append(alpha); rootvecs.append(vec)
roots = np.array(roots)
check("12 roots", len(roots) == 12)
lens = np.round(np.sum(roots ** 2, axis=1), 10)
check("root lengths^2 in B-dual metric: 6 long = 1, 6 short = 1/3",
      np.sum(np.isclose(lens, 1)) == 6 and np.sum(np.isclose(lens, 1 / 3)) == 6, sorted(set(lens.tolist())))

def su2_from_root(alpha, vec):
    """standard su(2) (real 7x7) for root alpha: [T_a,T_b] = eps_abc T_c."""
    # Cartan element H_alpha (component vector) with B(H_alpha, H) = alpha(H)
    Halpha = alpha @ H                        # components in g2 basis
    T3c = -Halpha / (alpha @ alpha)           # ad(T3) E_alpha = -i E_alpha
    T3 = np.einsum('a,aij->ij', T3c, G)
    E = np.einsum('a,aij->ij', vec, G)
    T1 = E.real.copy()
    if np.abs(T1).max() < 1e-8:
        T1 = E.imag.copy()
    T2 = T3 @ T1 - T1 @ T3
    # scale so that [T1, T2] = T3
    C = T1 @ T2 - T2 @ T1
    s = Bform(C, T3) / Bform(T3, T3)
    if s < 0:
        T2 = -T2; C = -C; s = -s
    T1 /= np.sqrt(s); T2 /= np.sqrt(s)
    return [T1, T2, T3]

def is_su2(T):
    err = 0
    for (a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        err = max(err, np.abs(T[a] @ T[b] - T[b] @ T[a] - T[c]).max())
    return err

long_idx = [k for k in range(12) if np.isclose(lens[k], 1)]
short_idx = [k for k in range(12) if np.isclose(lens[k], 1 / 3)]
aL = long_idx[0]
# short root orthogonal to aL
aS = [k for k in short_idx if abs(roots[k] @ roots[aL]) < 1e-9][0]
TL = su2_from_root(roots[aL], rootvecs[aL])
TS = su2_from_root(roots[aS], rootvecs[aS])
check("long su(2) relations", is_su2(TL) < 1e-10, float(is_su2(TL)))
check("short su(2) relations", is_su2(TS) < 1e-10, float(is_su2(TS)))
check("[su(2)_L, su(2)_S] = 0", max(np.abs(a @ b - b @ a).max() for a in TL for b in TS) < 1e-10)
# the long-root su(2) must lie in some su(3) (long roots of G2 = roots of su(3)); check it lies in our su(3)
# only if the chosen Cartan is inside su(3) (it is) and aL is a root of su(3):
inSU3 = max(np.linalg.norm(np.array([Bform(T, X) for X in SU3])) ** 2 - Bform(T, T) for T in TL)
check("long-root su(2) lies inside su(3) = stab(e1)", abs(inSU3) < 1e-10, float(inSU3))

def dynkin_index(T):
    return float(-np.trace(T[2] @ T[2]))   # -Tr_7(T3^2) for standard generators; long root -> 1

idx = {"long": dynkin_index(TL), "short": dynkin_index(TS)}
TD = [TL[a] + TS[a] for a in range(3)]
check("diag(L x S) is an su(2)", is_su2(TD) < 1e-10)
idx["index4_diag"] = dynkin_index(TD)

# SO(3) inside SU(3): real structure on C^3 = e1-perp. Need a conjugation commuting appropriately:
# so(3) = {X in su(3) : X commutes with a real structure}. Build it as the su(3) elements that
# preserve a Lagrangian real 3-plane: pick plane spanned by u2,u3,u4 with J u_i orthogonal to plane
# Find a 3-plane P in e1-perp with J P perp P: e.g. P = span(e2, e4, e6)?  check
def so3_in_su3():
    # search over coordinate 3-planes in e1-perp
    for trip in itertools.combinations(range(1, 7), 3):
        P = np.zeros((7, 3));
        for c, t in enumerate(trip): P[t, c] = 1
        if np.abs(P.T @ J @ P).max() < 1e-12 and np.linalg.matrix_rank(np.hstack([P, J @ P])) == 6:
            # so(3) = elements of su(3) preserving P
            Q = np.eye(7) - P @ P.T
            cond = np.array([(Q @ X @ P).ravel() for X in SU3]).T
            nsp = null_space(cond)
            if nsp.shape[1] == 3:
                return trip, np.einsum('ka,kij->aij', nsp, SU3)
    return None, None
trip, SO3 = so3_in_su3()
check("found Lagrangian 3-plane and 3-dim so(3) in su(3)", SO3 is not None, trip)
# make standard generators: find T3 as normalised element and build su(2) basis
SO3 = orthonormalise(list(SO3))
# rescale so that relations [T_a,T_b] = eps T_c hold: compute commutator norm
c01 = SO3[0] @ SO3[1] - SO3[1] @ SO3[0]
lam = np.sqrt(Bform(c01, c01))          # [X0,X1] = lam * X2' with B-ON X's
TSO3 = [X / lam for X in SO3]
# fix orientation
if Bform(TSO3[0] @ TSO3[1] - TSO3[1] @ TSO3[0], TSO3[2]) < 0:
    TSO3[2] = -TSO3[2]
check("so(3) in su(3): su(2) relations", is_su2(TSO3) < 1e-10, float(is_su2(TSO3)))
idx["index4_SO3"] = dynkin_index(TSO3)

# principal su(2): T3P = element of Cartan with alpha_i(T3P) = 1 for simple roots... build via rho^vee
# choose positive system by a generic linear functional
gfun = np.array([1.0, 0.3141])
pos = [k for k in range(12) if roots[k] @ gfun > 0]
# simple roots: positive roots not sums of two positive roots
def is_sum(k):
    for a in pos:
        for b in pos:
            if np.allclose(roots[a] + roots[b], roots[k]):
                return True
    return False
simple = [k for k in pos if not is_sum(k)]
check("2 simple roots", len(simple) == 2)
# coroot vectors in Cartan coordinates: alpha^vee = 2 alpha/|alpha|^2 ; rho^vee = half sum of positive coroots
rho_vee = 0.5 * sum(2 * roots[k] / (roots[k] @ roots[k]) for k in pos)
# T3P in Cartan coordinates h (2-vector, components along H rows) with ad(T3P) E_alpha = -i alpha(h) E_alpha...
# we need alpha_i(T3P) = 1 for simple roots: alpha(h) = alpha . h  -> solve
A = np.array([roots[k] for k in simple])
h = np.linalg.solve(A, np.ones(2))
T3P = -np.einsum('r,ra,aij->ij', h, H, G)     # sign as in su2_from_root: ad(T3)E_alpha = -i alpha(h) E_alpha
check("principal T3 equals rho^vee direction", np.allclose(h, rho_vee * 1.0) or np.allclose(h, rho_vee), (h.tolist(), rho_vee.tolist()))
idx["principal"] = float(-np.trace(T3P @ T3P))
# complete the principal su(2): T+ = sum_i c_i E_{alpha_i}; solve for c with [T+, T-] = -2i T3
Es = [np.einsum('a,aij->ij', rootvecs[k], G) for k in simple]
# general element T+ = c1 E1 + c2 E2 with complex c; T- = conj(T+). [T+,T-] lies in Cartan for simple roots.
def comm(a, b): return a @ b - b @ a
M11 = comm(Es[0], Es[0].conj()); M22 = comm(Es[1], Es[1].conj())
# |c1|^2 M11 + |c2|^2 M22 = -2i T3P  (cross terms vanish since alpha1-alpha2 is not a root)
cross = comm(Es[0], Es[1].conj())
check("alpha1 - alpha2 not a root (cross commutator vanishes)", np.abs(cross).max() < 1e-10)
Ab = np.array([(M11).ravel(), (M22).ravel()]).T
rhs = (-2j * T3P).ravel()
sol, *_ = np.linalg.lstsq(Ab, rhs, rcond=None)
check("principal su(2) solvable with |c_i|^2 > 0", np.all(sol.real > 0) and np.abs(sol.imag).max() < 1e-10, sol.real.tolist())
Tp = np.sqrt(sol[0].real) * Es[0] + np.sqrt(sol[1].real) * Es[1]
T1P = ((Tp + Tp.conj()) / 2).real; T2P = ((Tp - Tp.conj()) / (2j)).real
TP = [T1P, T2P, T3P]
errP = is_su2(TP)
if errP > 1e-8:   # try other orientation
    TP = [T1P, -T2P, T3P]; errP = is_su2(TP)
check("principal su(2) relations", errP < 1e-10, float(errP))
w7P = np.sort(np.linalg.eigvals(1j * T3P).real)
check("7 under principal SU(2) is spin 3 (m = -3..3)", np.allclose(w7P, np.arange(-3, 4)), np.round(w7P, 9).tolist())
w14P = np.sort(np.linalg.eigvals(1j * np.einsum('a,aij->ij', np.array([Bform(T3P, T) for T in G]), ad)).real)
mults = {}
for m in np.round(w14P).astype(int):
    mults[int(m)] = mults.get(int(m), 0) + 1
check("14 under principal SU(2) = spin 1 + spin 5", mults == {m: (2 if abs(m) <= 1 else 1) for m in range(-5, 6)}, {str(k): v for k, v in mults.items()})

expected = {"long": 1, "short": 3, "index4_diag": 4, "index4_SO3": 4, "principal": 28}
for k in expected:
    check(f"Dynkin index {k} = {expected[k]}", abs(idx[k] - expected[k]) < 1e-9, idx[k])

# exp(2 pi T3^L) vs exp(2 pi T3^S)
eL = expm(2 * np.pi * TL[2]); eS = expm(2 * np.pi * TS[2])
check("exp(2 pi T3^L) = exp(2 pi T3^S) in G2 (7-dim)", np.abs(eL - eS).max() < 1e-10, float(np.abs(eL - eS).max()))
check("exp(2 pi T3^L) != 1 (acts as -1 on (2,2))", np.abs(eL - np.eye(7)).max() > 1, np.round(np.linalg.eigvalsh((eL + eL.T) / 2), 8).tolist())
# also the adjoint
def adj_of(T):
    c = np.array([Bform(T, X) for X in G])
    return np.einsum('a,aij->ij', c, ad)
check("exp(2 pi T3^L) = exp(2 pi T3^S) on 14", np.abs(expm(2 * np.pi * adj_of(TL[2])) - expm(2 * np.pi * adj_of(TS[2]))).max() < 1e-9)

# branching of 7 and 14 under L x S from explicit Casimirs
def LS_content(mats_L, mats_S, dimrep):
    CL = -sum(m @ m for m in mats_L); CS = -sum(m @ m for m in mats_S)
    Mx = CL + np.sqrt(2) * CS
    ev = np.linalg.eigvals(Mx).real
    cl = np.linalg.eigvals(CL).real
    out = {}
    # joint eigenvalues: diagonalise CL, CS simultaneously via generic combination
    wv, Vv = np.linalg.eig(Mx)
    for k in range(dimrep):
        vk = Vv[:, k]
        jl = (vk.conj() @ CL @ vk / (vk.conj() @ vk)).real
        js = (vk.conj() @ CS @ vk / (vk.conj() @ vk)).real
        jL = (-1 + np.sqrt(1 + 4 * jl)) / 2; jS = (-1 + np.sqrt(1 + 4 * js)) / 2
        key = f"({int(round(2 * jL + 1))},{int(round(2 * jS + 1))})"
        out[key] = out.get(key, 0) + 1
    return {k: v // (int(k[1:-1].split(',')[0]) * int(k[1:-1].split(',')[1])) for k, v in out.items()}

br7 = LS_content(TL, TS, 7)
br14 = LS_content([adj_of(T) for T in TL], [adj_of(T) for T in TS], 14)
check("7 = (2,2) + (1,3) [explicit matrices]", br7 == {"(2,2)": 1, "(1,3)": 1}, br7)
check("14 = (3,1) + (1,3) + (2,4) [explicit matrices]", br14 == {"(3,1)": 1, "(1,3)": 1, "(2,4)": 1}, br14)

# B-orthonormal basis adapted to blocks: long (3), short/sqrt3 (3), complement (8)
def comps(T): return np.array([Bform(T, X) for X in G])
Lc = np.array([comps(T) for T in TL]); Sc = np.array([comps(T) for T in TS])
check("long su(2) generators are B-orthonormal (index 1)", np.allclose(Lc @ Lc.T, np.eye(3)))
check("short su(2) generators have B-norm 3", np.allclose(Sc @ Sc.T, 3 * np.eye(3)))
Sc_n = Sc / np.sqrt(3)
P = np.vstack([Lc, Sc_n])
comp = null_space(P).T
basis_c = np.vstack([Lc, Sc_n, comp])                     # 14 x 14 orthogonal
check("adapted basis orthonormal", np.allclose(basis_c @ basis_c.T, np.eye(14)))
np.savez("cc_g2_basis.npz", G=G, f=f, H=H, basis_c=basis_c, TL=np.array(TL), TS=np.array(TS),
         SU3=SU3, phi=phi)

# ================================================================ abstract root system: characters
# omega basis; alpha1 short, alpha2 long; Cartan matrix A_ij = <alpha_i, alpha_j^vee>
Acart = np.array([[2, -1], [-3, 2]])
# simple roots in omega coordinates: alpha_i = sum_j A_ij omega_j
alpha_w = [np.array(Acart[0]), np.array(Acart[1])]
# inner products in alpha basis
Ga = np.array([[Fr(1, 3), Fr(-1, 2)], [Fr(-1, 2), Fr(1)]])
# omega_i = sum_j (A^{-1})... compute omega in alpha basis exactly: alpha = A omega -> omega = A^{-1} alpha
detA = Acart[0, 0] * Acart[1, 1] - Acart[0, 1] * Acart[1, 0]
Ainv = [[Fr(Acart[1, 1], detA), Fr(-Acart[0, 1], detA)], [Fr(-Acart[1, 0], detA), Fr(Acart[0, 0], detA)]]
def w_to_a(mu):   # omega coords -> alpha coords
    return [sum(Fr(mu[i]) * Ainv[i][j] for i in range(2)) for j in range(2)]
def ip(mu, nu):   # inner product of weights given in omega coords
    a = w_to_a(mu); b = w_to_a(nu)
    return sum(a[i] * Ga[i][j] * b[j] for i in range(2) for j in range(2))
# positive roots in alpha coords
pos_a = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)]
def a_to_w(c): return tuple(int(c[0] * alpha_w[0][j] + c[1] * alpha_w[1][j]) for j in range(2))
pos_w = [a_to_w(c) for c in pos_a]
rho = (1, 1)
check("rho = half sum of positive roots = (1,1) in omega basis",
      tuple(sum(p[j] for p in pos_w) // 2 for j in range(2)) == rho)

def refl(mu, i):
    return tuple(mu[j] - mu[i] * Acart[i][j] for j in range(2))
# Weyl group orbit with signs
def weyl_elements():
    els = {((1, 0), (0, 1)): 1}   # represent w by images of omega1, omega2
    frontier = [((1, 0), (0, 1))]
    while frontier:
        new = []
        for w_ in frontier:
            for i in range(2):
                img = tuple(refl(v, i) for v in w_)
                if img not in els:
                    els[img] = -els[w_]
                    new.append(img)
        frontier = new
    return els
W = weyl_elements()
check("|W(G2)| = 12", len(W) == 12)
def wact(w_, mu):
    return tuple(mu[0] * w_[0][j] + mu[1] * w_[1][j] for j in range(2))

def dim_weyl(lam):
    num = Fr(1); den = Fr(1)
    lr = (lam[0] + 1, lam[1] + 1)
    for p in pos_w:
        num *= ip(lr, p); den *= ip(rho, p)
    return num / den

def C2(lam):
    l2 = (lam[0] + 2 * rho[0], lam[1] + 2 * rho[1])
    return ip(lam, l2)

def character(lam):
    """multiplicities via Weyl character formula: chi = A_{lam+rho} e^{-rho} / prod_{alpha>0}(1 - e^{-alpha})."""
    P = {}
    lr = (lam[0] + rho[0], lam[1] + rho[1])
    for w_, s in W.items():
        mu = wact(w_, lr)
        mu = (mu[0] - rho[0], mu[1] - rho[1])
        P[mu] = P.get(mu, 0) + s
    for alpha in pos_w:
        # divide by (1 - e^{-alpha}): Q(mu) = sum_{k>=0} P(mu + k alpha)
        Q = {}
        # group by cosets: choose representative by projecting along alpha
        keys = list(P.keys())
        # parametrise mu = base + t*alpha; base found by stepping down while staying "in" lattice:
        cosets = {}
        for mu in keys:
            # canonical coset label: invariant  mu0*alpha1 - mu1*alpha0 (cross product) is constant along alpha
            lab = mu[0] * alpha[1] - mu[1] * alpha[0]
            # position t along alpha: need integer; use dot with a fixed functional
            t = Fr(mu[0] * alpha[0] + mu[1] * alpha[1], alpha[0] ** 2 + alpha[1] ** 2)
            cosets.setdefault(lab, []).append((t, mu))
        for lab, lst in cosets.items():
            lst.sort(key=lambda z: z[0], reverse=True)
            tmax = lst[0][1]; tmin = lst[-1][1]
            # walk from top mu down by alpha until below the lowest
            vals = dict((mu, P[mu]) for _, mu in lst)
            mu = tmax; acc = 0
            lowest_t = lst[-1][0]
            while True:
                acc += vals.get(mu, 0)
                t = Fr(mu[0] * alpha[0] + mu[1] * alpha[1], alpha[0] ** 2 + alpha[1] ** 2)
                if t < lowest_t:
                    assert acc == 0, "inexact division"
                    break
                if acc != 0:
                    Q[mu] = acc
                mu = (mu[0] - alpha[0], mu[1] - alpha[1])
        P = Q
    return P

# enumerate dominant weights with dim <= 500
irreps = []
for a in range(0, 12):
    for b in range(0, 8):
        d = dim_weyl((a, b))
        if d <= 500:
            irreps.append(((a, b), int(d)))
irreps.sort(key=lambda z: (z[1], -z[0][0]))
print("irreps up to dim 500:", [(lam, d) for lam, d in irreps])

# check characters: total dim and Weyl invariance
allok = True
chars = {}
for lam, d in irreps:
    ch = character(lam)
    chars[lam] = ch
    tot = sum(ch.values())
    inv = all(ch.get(wact(w_, mu), 0) == m for w_ in W for mu, m in ch.items())
    allok &= (tot == d) and inv and ch.get(lam, 0) == 1 and all(m > 0 for m in ch.values())
check("Weyl-formula characters: dims match, Weyl-invariant, positive", allok)
check("7 has weights 0 and the 6 short roots", sorted(chars[(1, 0)].items()) ==
      sorted({(0, 0): 1, (1, 0): 1, (-1, 0): 1, (-1, 1): 1, (1, -1): 1, (2, -1): 1, (-2, 1): 1}.items()), str(chars[(1, 0)]))
check("14 has zero weight with multiplicity 2", chars[(0, 1)].get((0, 0)) == 2)

# L x S projections: alpha_L = alpha2 (long), alpha_S = 2 alpha1 + alpha2 (short, orthogonal)
aLw = a_to_w((0, 1)); aSw = a_to_w((2, 1))
check("alpha_L . alpha_S = 0; |alpha_L|^2 = 1, |alpha_S|^2 = 1/3",
      ip(aLw, aSw) == 0 and ip(aLw, aLw) == 1 and ip(aSw, aSw) == Fr(1, 3))
def coroot_pair(mu, al):
    return 2 * ip(mu, al) / ip(al, al)

def LS_branch(ch):
    M = {}
    for mu, m in ch.items():
        key = (int(coroot_pair(mu, aLw)), int(coroot_pair(mu, aSw)))   # (2 m_L, 2 m_S)
        M[key] = M.get(key, 0) + m
    out = {}
    while M:
        amax = max(k[0] for k in M)
        bmax = max(k[1] for k in M if k[0] == amax)
        n = M[(amax, bmax)]
        assert n > 0
        out[(amax, bmax)] = n          # (2jL, 2jS)
        for x in range(-amax, amax + 1, 2):
            for y in range(-bmax, bmax + 1, 2):
                M[(x, y)] -= n
                if M[(x, y)] == 0:
                    del M[(x, y)]
                assert M.get((x, y), 0) >= 0
    return out

def label(lam, d):
    return f"{d}[{lam[0]},{lam[1]}]"

table = []
all_integer = True
for lam, d in irreps:
    br = LS_branch(chars[lam])
    for (a2, b2), n in br.items():
        if (a2 + b2) % 2 != 0:
            all_integer = False
    allowed = {k[0] / 2: n for k, n in br.items() if k[1] == 0}
    table.append({"lam": list(lam), "dim": d, "C2": str(C2(lam)),
                  "branching": {f"({a + 1},{b + 1})": n for (a, b), n in sorted(br.items())},
                  "allowed_J": {str(j): n for j, n in sorted(allowed.items())}})
check("every L x S component of every irrep (dim<=500) has jL + jS integer", all_integer)
check("C2(7) = 2, C2(14) = 4", C2((1, 0)) == 2 and C2((0, 1)) == 4)
c2checks = {"27": C2((2, 0)), "64": C2((1, 1)), "77[0,2]": C2((0, 2)), "77'[3,0]": C2((3, 0))}
check("C2(27)=14/3, C2(64)=7, C2(77[0,2])=10, C2(77'[3,0])=8",
      c2checks == {"27": Fr(14, 3), "64": 7, "77[0,2]": 10, "77'[3,0]": 8}, {k: str(v) for k, v in c2checks.items()})
b7 = LS_branch(chars[(1, 0)]); b14 = LS_branch(chars[(0, 1)])
check("7 = (2,2)+(1,3) [characters]", b7 == {(1, 1): 1, (0, 2): 1}, str(b7))
check("14 = (3,1)+(1,3)+(2,4) [characters]", b14 == {(2, 0): 1, (0, 2): 1, (1, 3): 1}, str(b14))

# SU(3) content: su(3) roots are the long roots; branch by peeling SU(3) highest weights
# su(3) simple roots among long roots: beta1 = alpha2, beta2 = 3alpha1 + alpha2
b1 = a_to_w((0, 1)); b2 = a_to_w((3, 1))
check("beta1, beta2 long with angle 120 deg", ip(b1, b1) == 1 and ip(b2, b2) == 1 and ip(b1, b2) == Fr(-1, 2))
def su3_dim(p, q): return (p + 1) * (q + 1) * (p + q + 2) // 2
def su3_char(p, q):
    # weights of SU(3) irrep via Freudenthal-free: use explicit tensor method? simple: Weyl formula for A2 by brute force
    # weights in Dynkin coords of A2; use the standard multiplicity rule: layers
    out = {}
    # generate via Gelfand-Tsetlin patterns
    for m12 in range(q, p + q + 1):
        for m22 in range(0, q + 1):
            for m11 in range(m22, m12 + 1):
                # pattern (p+q, q, 0; m12, m22; m11)
                w1 = m11 - (m12 + m22 - m11)                    # 2*I3-like
                # weight in A2 Dynkin labels: (a, b) with a = 2 m11 - m12 - m22, b = 2(m12+m22) - (p+q+q) - m11 - ...
                n1 = m11; n2 = m12 + m22; n3 = p + 2 * q
                a = 2 * n1 - n2
                b = 2 * n2 - n1 - n3
                out[(a, b)] = out.get((a, b), 0) + 1
    return out
def su3_branch(ch):
    M = {}
    for mu, m in ch.items():
        key = (int(coroot_pair(mu, b1)), int(coroot_pair(mu, b2)))
        M[key] = M.get(key, 0) + m
    out = {}
    def height(k):  # dominance order: use inner product with rho of A2 in Dynkin coords
        return (2 * k[0] + k[1], k[0] + 2 * k[1])
    while M:
        dom = [k for k in M if k[0] >= 0 and k[1] >= 0]
        top = max(dom, key=lambda k: (k[0] + k[1], k[0]))
        # highest: take maximal under sum of coords (level)
        n = M[top]
        out[top] = out.get(top, 0) + n
        sc = su3_char(*top)
        assert sum(sc.values()) == su3_dim(*top)
        for k, m in sc.items():
            M[k] = M.get(k, 0) - n * m
            if M[k] == 0: del M[k]
            assert M.get(k, 0) >= 0, (top, k)
    return out
def su3name(p, q):
    d = su3_dim(p, q)
    return f"{d}" + ("bar" if q > p else ("" if p >= q else ""))
su3_tab = {}
for lam, d in irreps[:8]:
    br = su3_branch(chars[lam])
    su3_tab[label(lam, d)] = {f"{su3_dim(*k)}({k[0]},{k[1]})": n for k, n in sorted(br.items())}
print("G2 -> SU(3):", json.dumps(su3_tab, indent=0))
check("7 -> 1 + 3 + 3bar", su3_tab["7[1,0]"] == {"1(0,0)": 1, "3(1,0)": 1, "3(0,1)": 1})
check("14 -> 8 + 3 + 3bar", su3_tab["14[0,1]"] == {"3(1,0)": 1, "3(0,1)": 1, "8(1,1)": 1})

# rotor energies: E - M in units of 1/I1 with ratio r = I1/I2 (supplied later by cc_skyrme.py); here symbolic list
states = []
for row in table:
    for J, n in row["allowed_J"].items():
        Jf = float(J)
        states.append({"R": f"{row['dim']}[{row['lam'][0]},{row['lam'][1]}]", "dim": row["dim"],
                       "C2": row["C2"], "J": Jf, "copies": n})
json.dump({"checks": checks, "dynkin_indices": idx, "branching_7": br7, "branching_14": br14,
           "irreps": table, "allowed_states": states, "su3_content": su3_tab,
           "n_irreps": len(irreps)}, open("cc_g2.json", "w"), indent=1)
nf = sum(not c["pass"] for c in checks)
print(f"\n{len(checks) - nf}/{len(checks)} checks passed")
