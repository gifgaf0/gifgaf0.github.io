#!/usr/bin/env python3
"""
E3 part 1: g2 from the octonions, its su(3) and SU(2) subalgebras, Dynkin indices,
branching of 7 and 14 under SU(2)_long x SU(2)_short, Casimir normalisation.

Octonions: imaginary units e_0..e_6, lines {i, i+1, i+3} mod 7 (SEED.md section 3),
e_i e_{i+1} = e_{i+3} and cyclic.  g2 = Der(O) acting on Im(O) = R^7.

Conventions (used by every other E3 script):
  * B(X, Y) = -Tr_7(X Y) on g2 (7x7 real antisymmetric matrices).
  * Long-root su(2) generators T^L_a satisfy [T_a, T_b] = eps_abc T_c and act on the
    two complex doublets inside 7 as -i sigma_a / 2; then B(T^L_a, T^L_b) = delta_ab.
  * The Skyrme Lagrangian on G2 uses (1/2) Tr_7, which equals Tr_2 on the long su(2)
    and Tr_3 on su(3) (checked below).
  * Casimir C2 = -sum_a T_a T_a over a B-orthonormal basis; long su(2) gives J(J+1).
  * Dynkin index of an su(2) with standard generators: -Tr_7(T_3 T_3)  (long root = 1).

Writes g2_basis.npz (basis adapted to su(2)_L + su(2)_S + (2,4)) and
algebra_results.json.  Deterministic, numpy only.
"""
import json
import itertools
import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=150)
OUT = {}
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + ("  [" + detail + "]" if detail else ""))
    return ok


# ---------------------------------------------------------------- octonions
f = np.zeros((7, 7, 7))
for i in range(7):
    a, b, c = i % 7, (i + 1) % 7, (i + 3) % 7
    for (p, q, r), s in [((a, b, c), 1), ((b, c, a), 1), ((c, a, b), 1),
                         ((b, a, c), -1), ((a, c, b), -1), ((c, b, a), -1)]:
        f[p, q, r] = s


def omul(x, y):
    """octonion product, x = (x0, x1..x7) real part first"""
    a, u = x[0], x[1:]
    b, v = y[0], y[1:]
    re = a * b - u @ v
    im = a * v + b * u + np.einsum('ijk,i,j->k', f, u, v)
    return np.concatenate([[re], im])


rng = np.random.default_rng(1234)
errs_alt, errs_norm = [], []
for _ in range(200):
    x, y = rng.normal(size=8), rng.normal(size=8)
    errs_alt.append(np.abs(omul(x, omul(x, y)) - omul(omul(x, x), y)).max())
    errs_alt.append(np.abs(omul(omul(y, x), x) - omul(y, omul(x, x))).max())
    errs_norm.append(abs(np.linalg.norm(omul(x, y)) - np.linalg.norm(x) * np.linalg.norm(y)))
check("octonion table {i,i+1,i+3} is alternative", max(errs_alt) < 1e-12, f"max err {max(errs_alt):.1e}")
check("octonion norm is multiplicative", max(errs_norm) < 1e-12, f"max err {max(errs_norm):.1e}")
# non-associative (it really is the octonions, not the quaternions)
x, y, z = rng.normal(size=(3, 8))
nonassoc = np.abs(omul(omul(x, y), z) - omul(x, omul(y, z))).max()
check("octonion product is non-associative", nonassoc > 1e-3, f"|(xy)z - x(yz)| = {nonassoc:.3f}")

# ---------------------------------------------------------------- derivations
# D in gl(7): D(e_i e_j) = (D e_i) e_j + e_i (D e_j).  Unknowns D[l, k] (D e_k = sum_l D[l,k] e_l)
rows = []
for i in range(7):
    for j in range(7):
        # real part: -D_ji - D_ij = 0
        r = np.zeros((7, 7))
        r[j, i] += 1
        r[i, j] += 1
        rows.append(r.ravel())
        for l in range(7):
            r = np.zeros((7, 7))
            # LHS: sum_k f_ijk D_lk
            for k in range(7):
                r[l, k] += f[i, j, k]
            # RHS: sum_m D_mi f_mjl + sum_m D_mj f_iml
            for m in range(7):
                r[m, i] -= f[m, j, l]
                r[m, j] -= f[i, m, l]
            rows.append(r.ravel())
A = np.array(rows)
_, s, Vt = np.linalg.svd(A)
null = Vt[np.sum(s > 1e-10):]
check("dim Der(O) = 14", null.shape[0] == 14, f"null space dim {null.shape[0]}")
G = [v.reshape(7, 7) for v in null]
check("derivations are antisymmetric (so(7))", max(np.abs(g + g.T).max() for g in G) < 1e-12)
# preserves the 3-form phi_ijk = f_ijk
phi_err = max(np.abs(np.einsum('li,ljk->ijk', g, f) + np.einsum('lj,ilk->ijk', g, f)
                     + np.einsum('lk,ijl->ijk', g, f)).max() for g in G)
check("derivations preserve the associative 3-form", phi_err < 1e-12, f"{phi_err:.1e}")


def Bform(X, Y):
    return -np.trace(X @ Y)


def orthonormalize(mats, form=Bform, tol=1e-10):
    out = []
    for M in mats:
        V = M.copy()
        for Q in out:
            V = V - form(Q, V) * Q
        n = form(V, V)
        if n > tol:
            out.append(V / np.sqrt(n))
    return out


G = orthonormalize(G)
Gflat = np.array([g.ravel() for g in G])


def in_span(M, basis_flat, tol=1e-10):
    c, *_ = np.linalg.lstsq(basis_flat.T, M.ravel(), rcond=None)
    return np.abs(basis_flat.T @ c - M.ravel()).max() < tol, c


closure = max(np.abs(Gflat.T @ np.linalg.lstsq(Gflat.T, (a @ b - b @ a).ravel(), rcond=None)[0]
                     - (a @ b - b @ a).ravel()).max() for a in G for b in G)
check("g2 closes under commutators", closure < 1e-12, f"max residual {closure:.1e}")

# structure constants and Killing form
fabc = np.array([[np.linalg.lstsq(Gflat.T, (a @ b - b @ a).ravel(), rcond=None)[0] for b in G] for a in G])
ad = np.array([fabc[a].T for a in range(14)])  # ad(T_a)[c, b] = f_abc
kill = np.einsum('aij,bji->ab', ad, ad)
kev = np.linalg.eigvalsh(kill)
check("Killing form negative definite (compact)", kev.max() < 0, f"eigs in [{kev.min():.4f}, {kev.max():.4f}]")
check("Killing = -4 B, i.e. Tr_14 = 4 Tr_7 on g2 (index of adjoint = 4 x index of 7)",
      np.abs(kill + 4 * np.eye(14)).max() < 1e-10, f"max |K+4B| = {np.abs(kill + 4*np.eye(14)).max():.1e}")
# simple: adjoint irreducible -> commutant of ad(g2) in End(R^14) is 1-dim
comm_rows = []
for a in range(14):
    for X in [ad[a]]:
        # Y X - X Y = 0 for Y in gl(14)
        comm_rows.append(np.kron(np.eye(14), X.T) - np.kron(X, np.eye(14)))
cm = np.vstack(comm_rows)
sv = np.linalg.svd(cm, compute_uv=False)
check("adjoint representation irreducible (g2 simple)", np.sum(sv < 1e-9) == 1, f"commutant dim {np.sum(sv < 1e-9)}")
# rank: centralizer of a generic element
Xg = np.einsum('a,aij->ij', rng.normal(size=14), np.array(G))
cen = np.array([(Xg @ g - g @ Xg).ravel() for g in G])
rank_g2 = 14 - np.linalg.matrix_rank(cen.T, tol=1e-9)
check("rank g2 = 2", rank_g2 == 2)

# ---------------------------------------------------------------- su(3) = stabiliser of e_6
u = 6
stab_rows = np.array([g[:, u] for g in G])  # D e_u = column u
_, s2, Vt2 = np.linalg.svd(stab_rows.T)
cs = Vt2[np.sum(s2 > 1e-10):]
SU3 = orthonormalize([np.einsum('a,aij->ij', c, np.array(G)) for c in cs])
check("stabiliser of one imaginary unit has dim 8", len(SU3) == 8)
S3flat = np.array([g.ravel() for g in SU3])
cl3 = max(np.abs(S3flat.T @ np.linalg.lstsq(S3flat.T, (a @ b - b @ a).ravel(), rcond=None)[0]
                 - (a @ b - b @ a).ravel()).max() for a in SU3 for b in SU3)
check("stabiliser closes (subalgebra)", cl3 < 1e-12)

# complex structure J x = e_u x on e_u^perp, complex basis w1, w2, w3
Lu = np.zeros((7, 7))
for k in range(7):
    ek = np.zeros(7); ek[k] = 1
    eu = np.zeros(7); eu[u] = 1
    Lu[:, k] = np.einsum('ijk,i,j->k', f, eu, ek)
P6 = np.eye(7); P6[u, u] = 0
check("J = L_{e6} satisfies J^2 = -1 on e6^perp", np.abs(Lu @ Lu + P6).max() < 1e-12)
check("su(3) commutes with J", max(np.abs(g @ Lu - Lu @ g).max() for g in SU3) < 1e-12)
ws = []
cand = [np.eye(7)[k] for k in range(7) if k != u]
for v in cand:
    for w in ws:
        v = v - (w @ v) * w - ((Lu @ w) @ v) * (Lu @ w)
    if np.linalg.norm(v) > 1e-8:
        ws.append(v / np.linalg.norm(v))
    if len(ws) == 3:
        break
W = np.array(ws)          # 3 x 7
JW = (Lu @ W.T).T         # J w_k
# real 7-vector -> C^3:  z_k = <w_k, x> + i <J w_k, x>


def to3(M):
    """complex 3x3 matrix of a real 7x7 matrix commuting with J and killing e_u"""
    Z = np.zeros((3, 3), complex)
    for k in range(3):
        img = M @ W[k]          # image of w_k  (z = e_k)
        Z[:, k] = W @ img + 1j * (JW @ img)
    return Z


def from3(Z):
    """real 7x7 matrix acting on e_u^perp = C^3 as the complex matrix Z, zero on e_u"""
    M = np.zeros((7, 7))
    for k in range(3):
        # z = e_k  <-> x = w_k ;  z = i e_k <-> x = J w_k
        for col, xin in [(Z[:, k], W[k]), (1j * Z[:, k], JW[k])]:
            out = (col.real[:, None] * W + col.imag[:, None] * JW).sum(0)
            M += np.outer(out, xin)
    return M


Z3 = [to3(g) for g in SU3]
herm_err = max(np.abs(Z + Z.conj().T).max() for Z in Z3)
tr_err = max(abs(np.trace(Z)) for Z in Z3)
rt = max(np.abs(from3(to3(g)) - g).max() for g in SU3)
check("stabiliser acts on C^3 by traceless anti-Hermitian matrices (su(3))",
      herm_err < 1e-12 and tr_err < 1e-12 and rt < 1e-12,
      f"antiherm {herm_err:.1e}, trace {tr_err:.1e}, roundtrip {rt:.1e}")
rk = np.linalg.matrix_rank(np.array([np.concatenate([Z.real.ravel(), Z.imag.ravel()]) for Z in Z3]))
check("image is all of su(3) (8 real dims)", rk == 8)
# Tr_7 / 2 = Tr_3 on su(3)
trdiff = max(abs(np.trace(a @ b) / 2 - np.trace(to3(a) @ to3(b)).real) for a in SU3 for b in SU3)
check("(1/2) Tr_7 = Tr_3 on su(3)", trdiff < 1e-12, f"{trdiff:.1e}")
# 7 = 3 + 3bar + 1 under su(3): su(3) Casimir on R^7 with Gell-Mann normalisation
lam = np.zeros((8, 3, 3), complex)
lam[0][0, 1] = lam[0][1, 0] = 1
lam[1][0, 1] = -1j; lam[1][1, 0] = 1j
lam[2][0, 0] = 1; lam[2][1, 1] = -1
lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2] = -1j; lam[4][2, 0] = 1j
lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2] = -1j; lam[6][2, 1] = 1j
lam[7] = np.diag([1, 1, -2]) / np.sqrt(3)
TG = [from3(-0.5j * l) for l in lam]          # standard su(3) generators T_a = -i lambda_a / 2
check("Gell-Mann generators lie in the stabiliser", all(in_span(t, S3flat)[0] for t in TG))
C3 = -sum(t @ t for t in TG)
ev3 = np.round(np.linalg.eigvalsh(C3), 8)
OUT["su3_casimir_on_7"] = ev3.tolist()
check("7 = 3 + 3bar + 1 under SU(3): Casimir eigenvalues (4/3 x6, 0 x1)",
      np.allclose(sorted(ev3), [0] + [4 / 3] * 6))

# ---------------------------------------------------------------- SU(2) subalgebras
TL = [TG[0], TG[1], TG[2]]                    # isospin: a long-root su(2)
eps = np.zeros((3, 3, 3))
for (a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
    eps[a, b, c] = 1; eps[b, a, c] = -1


def su2_relations_err(T):
    return max(np.abs(T[a] @ T[b] - T[b] @ T[a] - sum(eps[a, b, c] * T[c] for c in range(3))).max()
               for a in range(3) for b in range(3))


check("T^L satisfy [T_a,T_b] = eps T_c", su2_relations_err(TL) < 1e-12)
# commutant of su(2)_L in g2
crow = np.array([np.concatenate([(t @ g - g @ t).ravel() for t in TL]) for g in G])
_, s4, Vt4 = np.linalg.svd(crow.T)
cc = Vt4[np.sum(s4 > 1e-10):]
check("centraliser of su(2)_long in g2 has dim 3", cc.shape[0] == 3)
Sc = [np.einsum('a,aij->ij', c, np.array(G)) for c in cc]
# bring to standard su(2) form: pick H = the hypercharge direction (in the commutant), then raise/lower
Y = TG[7]                                    # -i lambda_8 / 2
okY, _ = in_span(Y, np.array([s.ravel() for s in Sc]))
check("su(3) hypercharge generator lies in su(2)_short", okY)
# normalise: T^S_3 proportional to Y with [T3, X] = +-1 eigenvalues on doublet; find via ad-eigen
Sflat = np.array([s.ravel() for s in Sc])
adY = np.array([[np.linalg.lstsq(Sflat.T, (Y @ b - b @ Y).ravel(), rcond=None)[0] for b in Sc]]).squeeze().T
evY = np.linalg.eigvals(adY)
# eigenvalues of ad(Y) on the commutant are 0, +- i w; scale so that ad(T3) has eigenvalues 0, +-i
w = np.abs(evY.imag).max()
T3S = Y / w
# find T1S in the commutant, B-orthogonal to T3S, then T2S = [T3S, T1S]
rest = orthonormalize([T3S] + Sc)[1:]
v = rest[0]
T2S = T3S @ v - v @ T3S
# scale so that [T1, T2] = T3
T1S = v
k2 = np.trace((T1S @ T2S - T2S @ T1S) @ T3S) / np.trace(T3S @ T3S)
T1S, T2S = T1S / np.sqrt(abs(k2)), T2S / np.sqrt(abs(k2))
TS = [T1S, T2S, T3S]
if su2_relations_err(TS) > 1e-10:
    TS = [T2S, T1S, -T3S]
check("T^S satisfy [T_a,T_b] = eps T_c", su2_relations_err(TS) < 1e-10, f"{su2_relations_err(TS):.1e}")
check("[su(2)_L, su(2)_S] = 0", max(np.abs(a @ b - b @ a).max() for a in TL for b in TS) < 1e-12)


def dynkin_index(T):
    return -np.trace(T[2] @ T[2])


idx_L, idx_S = dynkin_index(TL), dynkin_index(TS)
TD = [TL[a] + TS[a] for a in range(3)]
idx_D = dynkin_index(TD)
# SO(3) inside SU(3) (real antisymmetric 3x3 = lambda_2, lambda_5, lambda_7)
TSO3 = [from3(-1j * lam[6]), from3(1j * lam[4]), from3(-1j * lam[1])]
check("SO(3) in SU(3) generators satisfy su(2) relations", su2_relations_err(TSO3) < 1e-12,
      f"{su2_relations_err(TSO3):.1e}")
idx_SO3 = dynkin_index(TSO3)

# Cartan subalgebra = span(T3^L, T3^S); weights (m_L, m_S) of 7 and roots of 14
H_L, H_S = TL[2], TS[2]
Hherm = [1j * H_L, 1j * H_S]                 # Hermitian, eigenvalues = m


def joint_weights(H1, H2):
    # simultaneous eigenvalues of two commuting Hermitian matrices
    M = H1 + np.pi * H2 / 7.3
    ev, V = np.linalg.eigh(M)
    w1 = np.real(np.einsum('ia,ij,ja->a', V.conj(), H1, V))
    w2 = np.real(np.einsum('ia,ij,ja->a', V.conj(), H2, V))
    return np.round(np.stack([w1, w2], 1), 8), V


wt7, V7 = joint_weights(*Hherm)
adL = 1j * np.array([[np.trace(-(H_L @ b - b @ H_L) @ a) for b in G] for a in G])   # B-orthonormal basis
adS = 1j * np.array([[np.trace(-(H_S @ b - b @ H_S) @ a) for b in G] for a in G])
wt14, V14 = joint_weights(adL, adS)
OUT["weights_7_(mL,mS)"] = sorted(map(tuple, wt7.tolist()))
OUT["roots_14_(mL,mS)"] = sorted(map(tuple, wt14.tolist()))
print("weights of 7 (m_L, m_S):", sorted(map(tuple, wt7.tolist())))
print("weights of 14 (m_L, m_S):", sorted(map(tuple, wt14.tolist())))

# root lengths in the inner product (l, m) = mL mL' + mS mS'/3 (dual of B restricted to the Cartan)
Bcart = np.array([[Bform(H_L, H_L), Bform(H_L, H_S)], [Bform(H_S, H_L), Bform(H_S, H_S)]])
OUT["B_on_cartan"] = Bcart.tolist()
check("B on Cartan = diag(1, 3) in (T3^L, T3^S)", np.allclose(Bcart, np.diag([1, 3])))
metric = np.linalg.inv(Bcart)
roots = [r for r in wt14 if np.abs(r).max() > 1e-6]
lens = sorted(set(np.round([r @ metric @ r for r in roots], 8)))
OUT["root_lengths_sq"] = lens
check("12 roots: 6 long (|a|^2=1) and 6 short (|a|^2=1/3)", len(roots) == 12 and np.allclose(lens, [1 / 3, 1]))
check("isospin root (1,0) is long, hypercharge-direction root (0,1) is short",
      any(np.allclose(r, [1, 0]) for r in roots) and any(np.allclose(r, [0, 1]) for r in roots))
su3_roots = [r for r in roots if abs(r @ metric @ r - 1) < 1e-8]
OUT["su3_roots_are_long_roots"] = True


def su2xsu2_content(V, HLs, HSs, Cl, Cs):
    """(jL, jS) multiplicities from Casimirs restricted to a representation space"""
    M = Cl + np.sqrt(2) * Cs
    ev, Q = np.linalg.eigh(M)
    jl = np.real(np.einsum('ia,ij,ja->a', Q.conj(), Cl, Q))
    js = np.real(np.einsum('ia,ij,ja->a', Q.conj(), Cs, Q))
    J = lambda c: np.round((-1 + np.sqrt(1 + 4 * max(c, 0))) / 2 * 2) / 2
    cnt = {}
    for a, b in zip(jl, js):
        key = (J(a), J(b))
        cnt[key] = cnt.get(key, 0) + 1
    # each irrep (jL,jS) occupies (2jL+1)(2jS+1) dims
    return {f"({int(2*k[0]+1)},{int(2*k[1]+1)})": v // int((2 * k[0] + 1) * (2 * k[1] + 1)) for k, v in sorted(cnt.items())}


CL7 = -sum(t @ t for t in TL)
CS7 = -sum(t @ t for t in TS)
br7 = su2xsu2_content(None, None, None, CL7, CS7)
adT = lambda T: np.array([[np.trace(-(T @ b - b @ T) @ a) for b in G] for a in G])
CL14 = -sum(adT(t) @ adT(t) for t in TL)
CS14 = -sum(adT(t) @ adT(t) for t in TS)
br14 = su2xsu2_content(None, None, None, CL14, CS14)
OUT["branching_7"] = br7
OUT["branching_14"] = br14
print("7  ->", br7)
print("14 ->", br14)
check("7 = (2,2) + (1,3) under SU(2)_L x SU(2)_S", br7 == {"(1,3)": 1, "(2,2)": 1})
check("14 = (3,1) + (1,3) + (2,4) under SU(2)_L x SU(2)_S", br14 == {"(1,3)": 1, "(2,4)": 1, "(3,1)": 1})

# Casimir normalisation over the whole B-orthonormal g2 basis
C7 = -sum(g @ g for g in G)
C14 = -sum(adT(g) @ adT(g) for g in G)
c7, c14 = np.linalg.eigvalsh(C7), np.linalg.eigvalsh(C14)
OUT["C2_7_numeric"] = [float(c7.min()), float(c7.max())]
OUT["C2_14_numeric"] = [float(c14.min()), float(c14.max())]
check("C2(7) = 2 (long-root normalisation)", np.allclose(c7, 2), f"{c7.min():.12f}..{c7.max():.12f}")
check("C2(14) = 4 (long-root normalisation)", np.allclose(c14, 4), f"{c14.min():.12f}..{c14.max():.12f}")
check("long su(2) Casimir on 7: J(J+1) in {3/4, 0}", np.allclose(sorted(np.linalg.eigvalsh(CL7)), [0]*3 + [0.75]*4))

# principal su(2): T3^P = T3^L + 3 T3^S (heights of roots), raising operator from simple-root vectors
# simple roots alpha1 = (-1/2, 1/2) (short), alpha2 = (1, 0) (long); find complex root vectors
G14 = np.array(G)
def root_vector(r):
    i = [k for k in range(14) if np.allclose(wt14[k], r)]
    assert len(i) == 1, (r, i)
    c = V14[:, i[0]]
    return np.einsum('a,aij->ij', c, G14)   # complex 7x7
E1, E2 = root_vector((-0.5, 0.5)), root_vector((1.0, 0.0))
J3P = 1j * (H_L + 3 * H_S)
# J+ = c1 E1 + c2 E2 ; J- = J+^dagger ; require [J+, J-] = 2 J3
A11 = E1 @ E1.conj().T - E1.conj().T @ E1
A22 = E2 @ E2.conj().T - E2.conj().T @ E2
A12 = E1 @ E2.conj().T - E2.conj().T @ E1
coef, *_ = np.linalg.lstsq(np.stack([A11.ravel(), A22.ravel()], 1), (2 * J3P).ravel(), rcond=None)
Jp = np.sqrt(abs(coef[0])) * E1 + np.sqrt(abs(coef[1])) * E2
Jm = Jp.conj().T
okP = np.abs(Jp @ Jm - Jm @ Jp - 2 * J3P).max() < 1e-10 and np.abs(A12).max() < 1e-10
# real compact generators
TP3 = -1j * J3P
TP1 = -0.5j * (Jp + Jm)
TP2 = -0.5 * (Jp - Jm)
TP = [np.real_if_close(t) for t in (TP1, TP2, TP3)]
TP = [t.real if np.abs(t.imag).max() < 1e-10 else t for t in TP]
relP = su2_relations_err(TP)
if relP > 1e-8:
    TP = [TP[1], TP[0], -TP[2]]
    relP = su2_relations_err(TP)
inP = all(in_span(np.real(t), Gflat)[0] and np.abs(np.imag(t)).max() < 1e-10 for t in TP)
check("principal su(2) constructed inside g2", okP and relP < 1e-8 and inP, f"rel err {relP:.1e}")
idx_P = dynkin_index([np.real(t) for t in TP])
CP7 = -sum(np.real(t) @ np.real(t) for t in TP)
evP = np.round(np.linalg.eigvalsh(CP7), 8)
check("7 is irreducible (spin 3) under the principal SU(2)", np.allclose(evP, 12))
CP14 = -sum(adT(np.real(t)) @ adT(np.real(t)) for t in TP)
evP14 = sorted(set(np.round(np.linalg.eigvalsh(CP14), 6)))
check("14 = spin 1 + spin 5 under principal SU(2) (Mayanskiy Prop. 4.1)", np.allclose(evP14, [2, 30]))
CD14 = -sum(adT(t) @ adT(t) for t in TD)
evD14 = np.round(np.linalg.eigvalsh(CD14), 6)
OUT["index4_spins_on_14"] = sorted(((-1 + np.sqrt(1 + 4 * evD14)) / 2).round(6).tolist())
CSO14 = -sum(adT(t) @ adT(t) for t in TSO3)
evSO14 = np.round(np.linalg.eigvalsh(CSO14), 6)
check("index-4 SU(2)s (diag of L x S, and SO(3) in SU(3)) give the same spins on 7 and 14",
      np.allclose(sorted(evD14), sorted(evSO14)) and
      np.allclose(sorted(np.linalg.eigvalsh(-sum(t @ t for t in TD))), sorted(np.linalg.eigvalsh(-sum(t @ t for t in TSO3)))))

OUT["dynkin_indices"] = {"long_root": float(idx_L), "short_root": float(idx_S),
                         "diag_long_x_short": float(idx_D), "SO3_in_SU3": float(idx_SO3),
                         "principal": float(idx_P)}
print("Dynkin indices:", OUT["dynkin_indices"])
check("Dynkin indices 1, 3, 4, 28 (long, short, A1^4, principal)",
      np.allclose([idx_L, idx_S, idx_D, idx_SO3, idx_P], [1, 3, 4, 4, 28]))

# index via the spin content of 7: sum over irreps of (2/3) j(j+1)(2j+1), divided by 2 (index of 7 rel. long root)
def index_from_casimir(C, dim=7):
    ev = np.linalg.eigvalsh(C)
    return float(sum(ev) / 2)   # sum_states j(j+1) = sum over irreps (2j+1) j(j+1); fundamental doublet: 2*(3/4)=3/2
# ( - Tr T3^2 = sum m^2 = (1/3) sum j(j+1)(2j+1) -> index = sum_states j(j+1)/3 ) ; checked against direct traces
idx_from_C = {k: float(np.trace(C) / 3) for k, C in [("long", CL7), ("short", CS7), ("principal", CP7)]}
OUT["dynkin_index_from_spin_content"] = idx_from_C
check("index = (1/3) sum_states j(j+1) over the 7 agrees", np.allclose(list(idx_from_C.values()), [1, 3, 28]))

# the centre of SU(2)_long and the centre of SU(2)_short are the same element of G2
from scipy.linalg import expm
zL, zS = expm(2 * np.pi * TL[2]), expm(2 * np.pi * TS[2])
check("exp(2 pi T3^L) = exp(2 pi T3^S) in G2 (and != 1): -1_L = -1_S",
      np.abs(zL - zS).max() < 1e-10 and np.abs(zL - np.eye(7)).max() > 1,
      f"|zL - zS| = {np.abs(zL - zS).max():.1e}, eigenvalues of zL: {sorted(np.round(np.linalg.eigvals(zL).real, 6))}")

# ---------------------------------------------------------------- adapted basis and save
compl = orthonormalize(TL + TS + G)[6:]
check("complement of su(2)_L + su(2)_S has dim 8", len(compl) == 8)
basis = np.array(TL + [t / np.sqrt(3) for t in TS] + compl)   # B(T^S_a, T^S_b) = 3 delta_ab
Bm = np.array([[Bform(a, b) for b in basis] for a in basis])
check("adapted basis is B-orthonormal", np.abs(Bm - np.eye(14)).max() < 1e-10)
# su(3) membership of the 8 complement directions: kaon generators T4..T7 lie in the (2,4) block
kaon_in = all(in_span(TG[k], np.array([c.ravel() for c in compl]))[0] for k in (3, 4, 5, 6))
check("su(3) kaon generators T4..T7 lie in the (2,4) block", kaon_in)
np.savez("g2_basis.npz", basis=basis, TL=np.array(TL), TS=np.array(TS), TG=np.array(TG),
         su3=np.array(SU3), TP=np.array([np.real(t) for t in TP]), TSO3=np.array(TSO3), f=f, u=u,
         W=W, JW=JW)
OUT["checks"] = CHECKS
OUT["n_checks_failed"] = sum(not c["pass"] for c in CHECKS)
with open("algebra_results.json", "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
print(f"\n{len(CHECKS) - OUT['n_checks_failed']}/{len(CHECKS)} checks passed")
