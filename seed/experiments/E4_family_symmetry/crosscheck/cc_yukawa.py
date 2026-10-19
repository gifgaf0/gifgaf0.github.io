"""
cc_yukawa.py -- independent cross-check of the E4 coupling tables, Schur test, alignment stabilisers
and the Majorana residual-symmetry obstruction for F21.

Coupling counts from characters (<chi_Lbar chi_R chi_H, 1>), mass-matrix forms from the Reynolds
projector over the whole group (not generator null spaces). Writes out/yukawa_cc.json.
"""
import json, math, cmath, itertools
import numpy as np

OUT, CHECKS = {}, {}
def check(name, ok):
    CHECKS[name] = bool(ok); print(("PASS " if ok else "FAIL ") + name)
base = "/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/"
F21 = np.load(base + "F21_elements.npy"); PSL = np.load(base + "PSL_elements.npy")
z = cmath.exp(2j * math.pi / 7); w = cmath.exp(2j * math.pi / 3)
D = np.diag([z, z ** 2, z ** 4]); C = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)

def word_in(G, gens):
    """express every element of G as (matrix, function giving the image in another rep via the same word)"""
    pass

# explicit F21 irreps through the parametrisation g = D^k C^m (unique for F21)
def decomp_F21(g):
    for k in range(7):
        for m in range(3):
            if np.allclose(np.linalg.matrix_power(D, k) @ np.linalg.matrix_power(C, m), g): return k, m
    raise ValueError
F21_km = [decomp_F21(g) for g in F21]
def rep_F21(lab):
    if lab == "1": return [np.eye(1)] * 21
    if lab == "1'": return [np.array([[w ** m]]) for k, m in F21_km]
    if lab == "1''": return [np.array([[w ** (2 * m)]]) for k, m in F21_km]
    if lab == "3": return [g for g in F21]
    if lab == "3b": return [g.conj() for g in F21]
def direct_sum(r1, r2):
    out = []
    for a, b in zip(r1, r2):
        M = np.zeros((a.shape[0] + b.shape[0],) * 2, dtype=complex)
        M[:a.shape[0], :a.shape[0]] = a; M[a.shape[0]:, a.shape[0]:] = b
        out.append(M)
    return out
R_F = {lab: rep_F21(lab) for lab in ("1", "1'", "1''", "3", "3b")}
R_F["1+1'+1''"] = direct_sum(direct_sum(R_F["1"], R_F["1'"]), R_F["1''"])

def n_invariants(reps):  # reps: list (over factors) of lists (over group) of matrices
    n = len(reps[0])
    tr = 0
    for gi in range(n):
        t = 1
        for r in reps: t *= np.trace(r[gi])
        tr += t
    return int(round((tr / n).real))

def dirac_count(RL, RR, RH):
    # invariant L^dagger R H : L-bar transforms as conj(rho_L)
    return n_invariants([[x.conj() for x in RL], RR, RH])

rows = [("3", "3"), ("3", "3b"), ("3", "1+1'+1''"), ("1+1'+1''", "1+1'+1''")]
cols = ["1", "1'", "1''", "3", "3b"]
tabF = {f"{l},{r}": [dirac_count(R_F[l], R_F[r], R_F[h]) for h in cols] for l, r in rows}
for k, v in tabF.items(): print(f"  F21 Dirac couplings L,R = {k:20s} H = {cols}: {v}")
target = {"3,3": [1, 1, 1, 1, 1], "3,3b": [0, 0, 0, 1, 2], "3,1+1'+1''": [0, 0, 0, 3, 0], "1+1'+1'',1+1'+1''": [3, 3, 3, 0, 0]}
check("F21 Dirac coupling table equals the report's table", tabF == target)
OUT["F21_dirac_table"] = tabF

# PSL irreps: 3, 3b explicit; 6 = Sym^2(3); 8 = traceless 3x3b; 7 by isotypic projection from 3 x 6
def sym2_basis():
    B = []
    for i in range(3):
        for j in range(i, 3):
            v = np.zeros(9); v[3 * i + j] += 1; v[3 * j + i] += 1
            B.append(v / np.linalg.norm(v))
    return np.array(B)
S2 = sym2_basis()
def restrict(Mbig, basis):  # basis rows orthonormal, invariant subspace
    return basis.conj() @ Mbig @ basis.T
R_P = {"1": [np.eye(1)] * 168, "3": list(PSL), "3b": [g.conj() for g in PSL]}
R_P["6"] = [restrict(np.kron(g, g), S2) for g in PSL]
# 8: traceless part of 3 x 3b
E = np.eye(9); vI = (E[0] + E[4] + E[8]) / math.sqrt(3)
Q, _ = np.linalg.qr(np.column_stack([vI] + [E[k] for k in range(9)]))
B8 = Q[:, 1:9].T
R_P["8"] = [restrict(np.kron(g, g.conj()), B8) for g in PSL]
chiP = lambda r: np.array([np.trace(x) for x in r])
# 7: projector with character of 7 = chi(3)chi(6) - chi(3b) - chi(8)
chi7 = chiP(R_P["3"]) * chiP(R_P["6"]) - chiP(R_P["3b"]) - chiP(R_P["8"])
big = [np.kron(a, b) for a, b in zip(R_P["3"], R_P["6"])]
P7 = 7 / 168 * sum(np.conj(c) * M for c, M in zip(chi7, big))
u, s, vh = np.linalg.svd(P7)
B7 = u[:, :7].T.conj()
B7 = B7.conj()  # rows
B7 = np.linalg.qr(u[:, :7])[0].T
R_P["7"] = [B7.conj() @ M @ B7.T for M in big]
hom_ok = all(np.allclose(R_P[l][i] @ R_P[l][j], R_P[l][[k for k in range(168) if np.allclose(PSL[k], PSL[i] @ PSL[j])][0]])
             for l in ("6", "7", "8") for (i, j) in ((1, 2), (5, 17), (40, 99)))
norms = {l: abs(np.vdot(chiP(R_P[l]), chiP(R_P[l])) / 168) for l in ("6", "7", "8")}
check("PSL 6, 7, 8 built as homomorphisms with irreducible characters (norm 1)", hom_ok and all(abs(v - 1) < 1e-9 for v in norms.values()))
colsP = ["1", "3", "3b", "6", "7", "8"]
tabP = {f"{l},{r}": [dirac_count(R_P[l], R_P[r], R_P[h]) for h in colsP] for l, r in (("3", "3"), ("3", "3b"))}
for k, v in tabP.items(): print(f"  PSL Dirac couplings L,R = {k}  H = {colsP}: {v}")
check("PSL: L=R=3 couples to H=1 and H=8 only (1 each); L=3,R=3b to H=3b and H=6 only",
      tabP["3,3"] == [1, 0, 0, 0, 0, 1] and tabP["3,3b"] == [0, 0, 1, 1, 0, 0])
OUT["PSL_dirac_table"] = tabP

# Majorana N N Phi, symmetric in N
def maj_count(RN, RPhi):
    n = len(RN)
    tr = 0
    for gi in range(n):
        x = RN[gi]
        chiS = (np.trace(x) ** 2 + np.trace(x @ x)) / 2
        tr += chiS * np.trace(RPhi[gi])
    return int(round((tr / n).real))
majF = {h: maj_count(R_F["3"], R_F[h]) for h in cols}
majP = {h: maj_count(R_P["3"], R_P[h]) for h in colsP}
print("  Majorana couplings, N in 3: F21", majF, " PSL", majP)
check("Majorana N=3: F21 allows Phi = 3 and 3b only (one each); PSL only Phi = 6; no singlet mass",
      majF == {"1": 0, "1'": 0, "1''": 0, "3": 1, "3b": 1} and majP == {"1": 0, "3": 0, "3b": 0, "6": 1, "7": 0, "8": 0})
OUT["majorana_counts"] = {"F21": majF, "PSL": majP}

# explicit forms via the Reynolds projector on L^dagger x R x H (F21, L=R=3)
def invariant_tensors(RL, RR, RH):
    n = len(RL)
    Pm = sum(np.kron(np.kron(a.conj(), b), c) for a, b, c in zip(RL, RR, RH)) / n
    u, s, vh = np.linalg.svd(Pm)
    k = int((s > 1e-9).sum())
    return [u[:, i] for i in range(k)], RL[0].shape[0], RR[0].shape[0], RH[0].shape[0]
def mass_matrix(T, dl, dr, dh, h):
    T = T.reshape(dl, dr, dh)
    return np.einsum('ijk,k->ij', T, h)
rng = np.random.default_rng(3)
h = rng.normal(size=3) + 1j * rng.normal(size=3)
forms = {}
for H in ("3", "3b"):
    (T,), dl, dr, dh = invariant_tensors(R_F["3"], R_F["3"], R_F[H])
    M = mass_matrix(T, dl, dr, dh, h)
    pattern = [[(None if abs(M[i, j]) < 1e-12 else int(np.argmin([abs(abs(M[i, j]) - abs(T.reshape(3, 3, 3)[i, j, k]) * abs(h[k])) for k in range(3)])) + 1) for j in range(3)] for i in range(3)]
    forms[H] = pattern
    sv = np.linalg.svd(M, compute_uv=False)
    print(f"  F21 L=R=3, H={H}: nonzero pattern (index of h) {pattern}; singular values / |h| sorted:",
          np.round(np.sort(sv) / np.sort(np.abs(h)) / (sv.max() / np.abs(h).max()), 6))
check("F21 L=R=3, H=3: M = [[0,0,h3],[h1,0,0],[0,h2,0]]; H=3b: M = [[0,h1,0],[0,0,h2],[h3,0,0]]",
      forms["3"] == [[None, None, 3], [1, None, None], [None, 2, None]] and forms["3b"] == [[None, 1, None], [None, None, 2], [3, None, None]])
(T,), *_ = invariant_tensors(R_F["3"], R_F["3"], R_F["1'"])
M1p = T.reshape(3, 3)
ratio = np.diag(M1p) / M1p[0, 0]
print("  H=1': diag ratios", np.round(ratio, 6), " off-diag max", np.abs(M1p - np.diag(np.diag(M1p))).max())
check("F21 L=R=3, H=1': M ~ diag(1, w, w^2) or diag(1, w^2, w): equal |masses|",
      np.allclose(np.abs(ratio), 1) and (np.allclose(ratio, [1, w, w ** 2]) or np.allclose(ratio, [1, w ** 2, w ** 2 * w ** 2])))
# Schur: trivial scalar
(T,), *_ = invariant_tensors(R_F["3"], R_F["3"], R_F["1"])
sv = np.linalg.svd(T.reshape(3, 3), compute_uv=False)
check("Schur: L=R=3, H=1 -> one coupling, three equal singular values (F21 and PSL)",
      np.allclose(sv, sv[0]) and dirac_count(R_P["3"], R_P["3"], R_P["1"]) == 1)
# commutant dimension
comm = lambda G: int(round(sum(abs(np.trace(g)) ** 2 for g in G).real / len(G)))
check("commutant of the triplet is 1-dimensional for F21 and PSL", comm(F21) == 1 and comm(PSL) == 1)
# 1 + 1' + 1'' Higgs, all with vevs -> distinct masses generically
Ms = [invariant_tensors(R_F["3"], R_F["3"], R_F[x])[0][0].reshape(3, 3) for x in ("1", "1'", "1''")]
Mgen = sum(c * M for c, M in zip(rng.normal(size=3) + 1j * rng.normal(size=3), Ms))
svg = np.sort(np.linalg.svd(Mgen, compute_uv=False))
check("1+1'+1'' vevs together give three distinct masses (generic)", min(np.diff(svg)) > 1e-3)
OUT["F21_forms"] = forms

# alignment stabilisers (on 3 and on 3bar) in F21 and PSL
aligns = {"Z3 (1,1,1)": np.array([1, 1, 1]), "Z7 (0,0,1)": np.array([0, 0, 1]), "LNR (-1,1,1)": np.array([-1, 1, 1]), "(0,1,-1)": np.array([0, 1, -1])}
stab = {}
for gname, G in (("F21", F21), ("PSL", PSL)):
    for rname, conj in (("3", False), ("3b", True)):
        for an, v in aligns.items():
            v = v.astype(complex)
            ex = sum(np.allclose((g.conj() if conj else g) @ v, v) for g in G)
            ph = sum(abs(abs(np.vdot(v, (g.conj() if conj else g) @ v)) - np.vdot(v, v).real) < 1e-9 for g in G)
            stab[f"{gname}/{rname}/{an}"] = (int(ex), int(ph))
for k, v in stab.items(): print(f"  stabiliser {k}: exact {v[0]}, up to phase {v[1]}")
check("F21: (1,1,1) fixed by Z3; (0,0,1) fixed by no non-trivial element but its ray by Z7; (-1,1,1), (0,1,-1) by nothing even up to phase",
      stab["F21/3/Z3 (1,1,1)"] == (3, 3) and stab["F21/3/Z7 (0,0,1)"] == (1, 7) and stab["F21/3/LNR (-1,1,1)"] == (1, 1) and stab["F21/3/(0,1,-1)"] == (1, 1))
OUT["stabilisers"] = stab

# Majorana residual symmetry obstruction for F21 subgroups on the 3
def maj_space_dim(gens):
    # symmetric M with g^T M g = M for all gens
    basis = []
    for i in range(3):
        for j in range(i, 3):
            Mb = np.zeros((3, 3)); Mb[i, j] = Mb[j, i] = 1; basis.append(Mb)
    A = np.array([np.concatenate([((g.T @ Mb @ g) - Mb).ravel() for g in gens]) for Mb in basis]).T
    u, s, vh = np.linalg.svd(A)
    null = vh[(s > 1e-9).sum():]
    return [sum(c * Mb for c, Mb in zip(v, basis)) for v in null]
Z7sp = maj_space_dim([D]); Z3sp = maj_space_dim([C])
Mz3 = sum((rng.normal() + 1j * rng.normal()) * M for M in Z3sp)
tak = np.sort(np.linalg.svd(Mz3, compute_uv=False))
print("  Majorana space invariant under Z7:", len(Z7sp), "; under Z3:", len(Z3sp), "; Z3 Takagi values", np.round(tak, 4))
check("F21 Z7 forces M_Maj = 0 on the 3; Z3 leaves a degenerate pair; F21 has no Z2 (odd order)",
      len(Z7sp) == 0 and len(Z3sp) == 2 and min(np.diff(tak)) < 1e-9 and not any(np.allclose(g @ g, np.eye(3)) and not np.allclose(g, np.eye(3)) for g in F21))
# also: all 7 Z3 subgroups (conjugate) behave the same
OUT["checks"] = CHECKS; OUT["all_pass"] = all(CHECKS.values())
json.dump(OUT, open(base + "yukawa_cc.json", "w"), indent=1, default=str)
print(f"\n{sum(CHECKS.values())}/{len(CHECKS)} checks pass")
