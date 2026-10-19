"""
e4_yukawa.py -- E4 part 2: which Yukawa couplings F21 and PSL(2,7) allow for three generations.

  A. invariant tensors in Lbar x R x H (Dirac) and R x R x Phi (Majorana), for three generations
     in 3, 3bar or 1+1'+1'' (F21) / 3, 3bar, 1+1+1 (PSL), all scalar irreps;
     the general mass matrix as a function of the scalar vevs (F21: closed form)
  B. Schur: with the group unbroken (only trivial scalars get vevs) an irreducible triplet has
     three equal masses (or none)
  C. vacuum alignments that leave Z3 (vev ~ (1,1,1)) or Z7 (D-eigenvector vevs) unbroken, and
     the resulting masses and mixing matrices
  D. residual symmetries: every pair of subgroups (G_l, G_nu) of F21 and PSL(2,7) with a
     non-degenerate action fixes a mixing matrix; compare with NuFIT 6.0 and UTfit 2022

Conventions: Dirac term  Lbar_i M_ij R_j  with  M_ij = sum_a Y_ija <H_a>; covariance
M(rho_H v) = rho_L M(v) rho_R^dagger.  Majorana term  N_i M_ij N_j  with M symmetric.
Run: python3 e4_yukawa.py   (needs out/reps.npz from e4_groups.py; about 20 s)
"""
import itertools
import json
import math
import os
import sys
import time

import numpy as np

from e4lib import OMEGA, angles_from_U, invariants, recognize, rref, wolfenstein_from_V, pdg_matrix
from data_targets import NUFIT, UTFIT, chi2_pmns, chi2_ckm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
t0 = time.time()
R = np.load(os.path.join(OUT, "reps.npz"))
CHECKS = {}


def check(name, ok, detail=""):
    CHECKS[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


GROUPS = {
    "F21": {"irreps": {k: R[f"F21_{k}"] for k in ("1", "1'", "1''", "3", "3b")},
            "gens": list(R["F21_gens"]), "mt": R["F21_mt"], "order": R["F21_order"]},
    "PSL": {"irreps": {k: R[f"PSL_{k}"] for k in ("1", "3", "3b", "6", "7", "8")},
            "gens": list(R["PSL_gens"]), "mt": R["PSL_mt"], "order": R["PSL_order"]},
}


def dsum(*reps):
    n = reps[0].shape[0]
    d = sum(r.shape[1] for r in reps)
    out = np.zeros((n, d, d), dtype=complex)
    o = 0
    for r in reps:
        k = r.shape[1]
        out[:, o:o + k, o:o + k] = r
        o += k
    return out


FI = GROUPS["F21"]["irreps"]
PI = GROUPS["PSL"]["irreps"]
GROUPS["F21"]["gen3"] = {"3": FI["3"], "3b": FI["3b"], "1+1'+1''": dsum(FI["1"], FI["1'"], FI["1''"])}
GROUPS["PSL"]["gen3"] = {"3": PI["3"], "3b": PI["3b"], "1+1+1": dsum(PI["1"], PI["1"], PI["1"])}


def dirac_tensors(G, rL, rR, rH):
    """Basis of Y (dL, dR, dH) with  Lbar Y R H  invariant.  Canonical (rref) basis."""
    W = invariants([np.conj(rL), rR, rH], G["gens"])
    if W.shape[1] == 0:
        return []
    Wc = rref(np.conj(W).T)          # rows: canonical invariant tensors Y (flattened)
    dL, dR, dH = rL.shape[1], rR.shape[1], rH.shape[1]
    return [w.reshape(dL, dR, dH) for w in Wc]


def majorana_tensors(G, rN, rP):
    W = invariants([rN, rN, rP], G["gens"])
    if W.shape[1] == 0:
        return []
    d, dP = rN.shape[1], rP.shape[1]
    sym = []
    for k in range(W.shape[1]):
        T = np.conj(W[:, k]).reshape(d, d, dP)
        sym.append(((T + T.transpose(1, 0, 2)) / 2).ravel())
    M = np.array(sym)
    u, s, vh = np.linalg.svd(M)
    r = int(np.sum(s > 1e-9))
    if r == 0:
        return []
    basis = rref(vh[:r])
    return [b.reshape(d, d, dP) for b in basis]


def mass_matrix(Ys, couplings, v):
    return sum(c * np.einsum("ija,a->ij", Y, v) for c, Y in zip(couplings, Ys))


def sym_string(Ys, vnames):
    """Closed form of M = sum_k y_k Y_k . v  (entries recognized as phases / surds)."""
    d1, d2 = Ys[0].shape[:2]
    rows = []
    for i in range(d1):
        row = []
        for j in range(d2):
            terms = []
            for k, Y in enumerate(Ys):
                for a in range(Y.shape[2]):
                    c = Y[i, j, a]
                    if abs(c) > 1e-9:
                        cs = recognize(c)
                        cs = "" if cs == "1" else ("-" if cs == "-1" else cs + "*")
                        terms.append(f"{cs}y{k + 1}*{vnames[a]}")
            row.append(" + ".join(terms) if terms else "0")
        rows.append(row)
    return rows


rng = np.random.default_rng(20261018)

# =====================================================================================
# A. invariant tensors and general mass matrices
# =====================================================================================
yuk = {}
for gname, G in GROUPS.items():
    tab = {}
    print(f"\n=== {gname}: Dirac Yukawa invariants  Lbar x R x H  (number of independent couplings)")
    gen3 = G["gen3"]
    header = list(G["irreps"])
    print("  L      R          " + "  ".join(f"{h:>4}" for h in header))
    cov_ok = True
    for Ln, rL in gen3.items():
        for Rn, rR in gen3.items():
            counts = {}
            for Hn, rH in G["irreps"].items():
                Ys = dirac_tensors(G, rL, rR, rH)
                counts[Hn] = len(Ys)
                if Ys:
                    # covariance check with random couplings / vev / group element
                    y = rng.normal(size=len(Ys)) + 1j * rng.normal(size=len(Ys))
                    v = rng.normal(size=rH.shape[1]) + 1j * rng.normal(size=rH.shape[1])
                    g = int(rng.integers(rL.shape[0]))
                    lhs = mass_matrix(Ys, y, rH[g] @ v)
                    rhs = rL[g] @ mass_matrix(Ys, y, v) @ np.conj(rL[g] if False else rR[g]).T
                    cov_ok &= np.allclose(lhs, rhs, atol=1e-9)
                    if gname == "F21":
                        vn = ["h"] if rH.shape[1] == 1 else [f"h{a + 1}" for a in range(rH.shape[1])]
                        tab.setdefault(f"{Ln}|{Rn}", {})[Hn] = {"n": len(Ys), "M": sym_string(Ys, vn)}
                    else:
                        tab.setdefault(f"{Ln}|{Rn}", {})[Hn] = {"n": len(Ys)}
            print(f"  {Ln:<6} {Rn:<10} " + "  ".join(f"{counts[h]:>4}" for h in header))
    check(f"{gname}: Dirac mass matrices transform covariantly, M(rho_H v) = rho_L M rho_R^+", cov_ok)
    yuk[gname] = tab

print("\n=== F21 closed forms (L = R = 3; D-diagonal basis; h_a are the scalar vev components)")
for Hn, info in yuk["F21"]["3|3"].items():
    print(f"  H = {Hn}:  M = " + " | ".join("[" + ", ".join(r) + "]" for r in info["M"]))
print("=== F21 closed forms (L = 3, R = 3bar)")
for Hn, info in yuk["F21"]["3|3b"].items():
    print(f"  H = {Hn}:  M = " + " | ".join("[" + ", ".join(r) + "]" for r in info["M"]))

maj = {}
for gname, G in GROUPS.items():
    tab = {}
    print(f"\n=== {gname}: Majorana invariants  N x N x Phi (symmetric)")
    for Nn, rN in G["gen3"].items():
        row = {}
        for Pn, rP in G["irreps"].items():
            Ys = majorana_tensors(G, rN, rP)
            entry = {"n": len(Ys)}
            if gname == "F21" and Ys:
                vn = ["f"] if rP.shape[1] == 1 else [f"f{a + 1}" for a in range(rP.shape[1])]
                entry["M"] = sym_string(Ys, vn)
            row[Pn] = entry
        tab[Nn] = row
        print(f"  N = {Nn:<9} " + "  ".join(f"{p}:{row[p]['n']}" for p in G["irreps"]))
    maj[gname] = tab
for Pn, info in maj["F21"]["3"].items():
    if info["n"]:
        print(f"  F21 N=3, Phi={Pn}: M_R = " + " | ".join("[" + ", ".join(r) + "]" for r in info["M"]))

# LNR-type effective operators (arXiv:0706.2341): fermions psi, psi' in 3, familons xi, xi' in 3bar,
# Higgs a flavour singlet: invariants in 3 x 3 x 3bar x 3bar
G = GROUPS["F21"]
W4 = invariants([FI["3"], FI["3"], FI["3b"], FI["3b"]], G["gens"])
W4m = invariants([FI["3"], FI["3"], FI["3b"]], G["gens"])
check("LNR effective operator psi psi' xi xi' (3 x 3 x 3bar x 3bar): 5 invariants (I3 + four of type I4, "
      "LNR Sec. 3.1 and 4.1)", W4.shape[1] == 5, f"found {W4.shape[1]}")
WM = invariants([FI["3"], FI["3"], FI["3b"], FI["3b"]], G["gens"])
# symmetric in fermions AND familons (Majorana psi=psi', xi=xi')
Wsym = []
for k in range(WM.shape[1]):
    T = WM[:, k].reshape(3, 3, 3, 3)
    S = (T + T.transpose(1, 0, 2, 3) + T.transpose(0, 1, 3, 2) + T.transpose(1, 0, 3, 2)) / 4
    Wsym.append(S.ravel())
rk = np.linalg.matrix_rank(np.array(Wsym), tol=1e-9)
check("Majorana version (psi = psi', xi = xi'): 2 independent invariants (I3 and one I4: LNR's alpha)", rk == 2,
      f"rank {rk}")
# I3 (3 x 3' x 3bar): Dirac coupling with ONE familon (renormalizable-like with a 3bar scalar)
n333 = invariants([FI["3"], FI["3"], FI["3"]], G["gens"]).shape[1]
n3333 = invariants([FI["3"]] * 4, G["gens"]).shape[1]
n333b3 = invariants([FI["3"], FI["3"], FI["3"], FI["3b"]], G["gens"]).shape[1]
check("LNR invariant multiplicities (0706.2341 Sec. 3.1): 3x3x3bar -> 1 (I2^(3)); 3x3x3 -> 2 (I1^(3)); "
      "3x3x3x3 -> 4 (I1^(4)); 3x3x3x3bar -> 3 (I2^(4)); 3x3x3barx3bar -> 5 (I3^(4) + four I4^(4))",
      W4m.shape[1] == 1 and n333 == 2 and n3333 == 4 and n333b3 == 3 and W4.shape[1] == 5,
      f"{W4m.shape[1]}, {n333}, {n3333}, {n333b3}, {W4.shape[1]}")

# =====================================================================================
# B. Schur's lemma: unbroken group -> no hierarchy inside an irreducible triplet
# =====================================================================================
schur = {}
for gname, G in GROUPS.items():
    gens = G["gens"]
    r3 = G["irreps"]["3"]
    # commutant of the triplet
    comm = invariants([r3, np.conj(r3)], gens).shape[1]
    trivial = G["irreps"]["1"]
    res = {"commutant_dim_3": int(comm)}
    for (Ln, Rn) in (("3", "3"), ("3", "3b"), ("3b", "3b")):
        Ys = dirac_tensors(G, G["gen3"][Ln], G["gen3"][Rn], trivial)
        if Ys:
            Mx = mass_matrix(Ys, rng.normal(size=len(Ys)) + 1j * rng.normal(size=len(Ys)), np.array([1.0 + 0j]))
            sv = np.linalg.svd(Mx, compute_uv=False)
            res[f"{Ln}|{Rn}|H=1"] = {"n_couplings": len(Ys), "singular_values": sv.round(12).tolist(),
                                     "degenerate": bool(np.ptp(sv) < 1e-12)}
        else:
            res[f"{Ln}|{Rn}|H=1"] = {"n_couplings": 0, "singular_values": [0, 0, 0], "degenerate": True}
    # Majorana with a trivial scalar
    res["Majorana N=3, Phi=1"] = len(majorana_tensors(G, G["irreps"]["3"], trivial))
    schur[gname] = res
    print(f"\n=== Schur ({gname}): commutant of the 3 has dimension {comm}; "
          f"Lbar 3 R 3 H=1 -> {res['3|3|H=1']}; Lbar 3 R 3bar H=1 -> {res['3|3b|H=1']['n_couplings']} couplings; "
          f"Majorana 3x3x1 -> {res['Majorana N=3, Phi=1']} couplings")
check("Schur: commutant of the triplet is 1-dimensional for F21 and PSL(2,7)",
      schur["F21"]["commutant_dim_3"] == 1 and schur["PSL"]["commutant_dim_3"] == 1)
check("Schur: with only a trivial scalar, an irreducible triplet gets three EQUAL masses (L=R) or none "
      "(L=3, R=3bar), and no Majorana mass, for both groups",
      all(schur[g]["3|3|H=1"]["degenerate"] and schur[g]["3|3|H=1"]["n_couplings"] == 1
          and schur[g]["3|3b|H=1"]["n_couplings"] == 0 and schur[g]["Majorana N=3, Phi=1"] == 0 for g in schur))
# F21 non-trivial singlets keep F21's Z7 but break Z3; with one of them alone masses stay degenerate
deg_1p = {}
for Hn in ("1'", "1''"):
    Ys = dirac_tensors(GROUPS["F21"], FI["3"], FI["3"], FI[Hn])
    Mx = mass_matrix(Ys, [1.3 - 0.4j], np.array([1.0 + 0j]))
    deg_1p[Hn] = np.linalg.svd(Mx, compute_uv=False).round(12).tolist()
Ys_all = [dirac_tensors(GROUPS["F21"], FI["3"], FI["3"], FI[h])[0] for h in ("1", "1'", "1''")]
Mx = sum(c * Y[:, :, 0] for c, Y in zip([1.0, 0.45 + 0.2j, -0.3 + 0.1j], Ys_all))
sv_all = np.linalg.svd(Mx, compute_uv=False)
check("F21: a single 1' (or 1'') vev alone still gives three equal |masses|; 1 + 1' + 1'' vevs together "
      "(F21 broken to Z7) give a diagonal matrix with three free entries",
      all(np.ptp(v) < 1e-12 for v in deg_1p.values()) and np.ptp(sv_all) > 0.1
      and np.allclose(Mx, np.diag(np.diag(Mx))), f"{deg_1p}; three singlets: {sv_all.round(4).tolist()}")
schur["F21_single_nontrivial_singlet"] = deg_1p
schur["F21_three_singlets_example_sv"] = sv_all.tolist()

# =====================================================================================
# C. vacuum alignments: stabilizers, masses, mixing
# =====================================================================================
def stabilizer(G, rH, v, twisted=False):
    """Elements g with rho_H(g) v = v  (or  ~ v up to a phase if twisted)."""
    out = []
    for g in range(rH.shape[0]):
        w = rH[g] @ v
        if twisted:
            ph = np.vdot(v, w) / np.vdot(v, v)
            if abs(abs(ph) - 1) < 1e-9 and np.allclose(w, ph * v, atol=1e-9):
                out.append(g)
        elif np.allclose(w, v, atol=1e-9):
            out.append(g)
    return out


def describe_subgroup(G, els):
    orders = sorted(int(G["order"][g]) for g in els)
    n = len(els)
    if n == 1:
        return "1"
    if n == 3:
        return "Z3"
    if n == 7:
        return "Z7"
    if n == 21:
        return "F21"
    return f"order {n} (element orders {sorted(set(orders))})"


FOUR = np.array([[1, 1, 1], [1, OMEGA, OMEGA ** 2], [1, OMEGA ** 2, OMEGA]]) / math.sqrt(3)
align = {"Z3: (1,1,1)": np.array([1, 1, 1], dtype=complex) / math.sqrt(3),
         "Z7: (0,0,1)": np.array([0, 0, 1], dtype=complex),
         "LNR: (-1,1,1)": np.array([-1, 1, 1], dtype=complex) / math.sqrt(3),
         "(0,1,-1)": np.array([0, 1, -1], dtype=complex) / math.sqrt(2)}
G = GROUPS["F21"]
align_res = {}
print("\n=== F21 vacuum alignments of a triplet scalar: stabilizer (exact) and stabilizer up to a phase")
for nm, v in align.items():
    for Hn in ("3", "3b"):
        st = stabilizer(G, FI[Hn], v)
        stt = stabilizer(G, FI[Hn], v, twisted=True)
        align_res[f"{nm} in {Hn}"] = {"stabilizer": describe_subgroup(G, st), "ray_stabilizer": describe_subgroup(G, stt)}
        print(f"  {nm:<14} in {Hn:<2}: stabilizer {describe_subgroup(G, st):<4}  ray stabilizer {describe_subgroup(G, stt)}")
check("F21: (1,1,1) is fixed by a Z3; D-eigenvectors (0,0,1) are fixed by no element but their ray is "
      "fixed by Z7; LNR's (-1,1,1) and (0,1,-1) are fixed by nothing (not even up to a phase)",
      align_res["Z3: (1,1,1) in 3"]["stabilizer"] == "Z3" and align_res["Z7: (0,0,1) in 3"]["stabilizer"] == "1"
      and align_res["Z7: (0,0,1) in 3"]["ray_stabilizer"] == "Z7"
      and align_res["LNR: (-1,1,1) in 3"]["ray_stabilizer"] == "1" and align_res["(0,1,-1) in 3"]["ray_stabilizer"] == "1")


def mixing_info(M):
    U, s, Vh = np.linalg.svd(M)
    order = np.argsort(s)
    U = U[:, order]
    s = s[order]
    return s, U


aligned_masses = {}
print("\n=== F21, L = R = 3 with triplet Higgs fields: masses (singular values) for aligned vevs")
Y3 = dirac_tensors(G, FI["3"], FI["3"], FI["3"])
Y3b = dirac_tensors(G, FI["3"], FI["3"], FI["3b"])
Y1 = dirac_tensors(G, FI["3"], FI["3"], FI["1"])
cases = {}
for anm in ("Z3: (1,1,1)", "Z7: (0,0,1)"):
    v = align[anm] * math.sqrt(3) if anm.startswith("Z3") else align[anm]
    s3, U3 = mixing_info(mass_matrix(Y3, [1.0], v))
    s3b, _ = mixing_info(mass_matrix(Y3b, [1.0], v))
    Mcomb = mass_matrix(Y1, [0.7], np.array([1.0 + 0j])) + mass_matrix(Y3, [0.4 + 0.3j], v) + mass_matrix(Y3b, [-0.2 + 0.5j], v)
    sc, Uc = mixing_info(Mcomb)
    cases[anm] = {"H=3 alone": s3.round(10).tolist(), "H=3bar alone": s3b.round(10).tolist(),
                  "H=1+3+3bar": sc.round(6).tolist(), "|U_L|^2 (1+3+3bar)": (np.abs(Uc) ** 2).round(6).tolist()}
    print(f"  vev {anm}: H=3 alone sv {s3.round(4)}, H=3bar alone sv {s3b.round(4)}, "
          f"H=1+3+3bar sv {sc.round(4)}; |U_L|^2 = {(np.abs(Uc) ** 2).round(3).tolist()}")
v_gen = np.array([0.02, 0.3, 1.0], dtype=complex)
s_gen, U_gen = mixing_info(mass_matrix(Y3, [1.0], v_gen))
cases["generic (0.02,0.3,1)"] = {"H=3 alone": s_gen.round(10).tolist(),
                                 "|U_L|^2": (np.abs(U_gen) ** 2).round(6).tolist()}
print(f"  generic vev (0.02, 0.3, 1), H=3 alone: sv {s_gen.round(4)} (masses = |vev components|), "
      f"|U_L|^2 is a permutation: {(np.abs(U_gen) ** 2).round(3).tolist()}")
aligned_masses["F21 L=R=3"] = cases
check("F21, single triplet Higgs (L=R=3): Z3-aligned vev -> three equal masses; Z7-aligned -> rank 1; "
      "generic vev -> masses equal to |vev components| with no mixing (generalized permutation)",
      np.ptp(cases["Z3: (1,1,1)"]["H=3 alone"]) < 1e-9
      and sum(x > 1e-9 for x in cases["Z7: (0,0,1)"]["H=3 alone"]) == 1
      and np.allclose(sorted(s_gen), sorted(np.abs(v_gen)))
      and np.allclose(np.sort((np.abs(U_gen) ** 2).ravel()), [0] * 6 + [1] * 3, atol=1e-9))
check("F21, Higgs in 1 + 3 + 3bar all Z3-aligned: M is circulant, |U_L|^2 = 1/3 everywhere (trimaximal "
      "Fourier matrix)", np.allclose(np.array(cases["Z3: (1,1,1)"]["|U_L|^2 (1+3+3bar)"]), 1 / 3, atol=1e-9))
Mz7 = mass_matrix(Y1, [0.7], np.array([1.0 + 0j])) + mass_matrix(Y3, [0.4 + 0.3j], align["Z7: (0,0,1)"]) \
    + mass_matrix(Y3b, [-0.2 + 0.5j], align["Z7: (0,0,1)"])
H = Mz7 @ Mz7.conj().T
check("F21, Higgs in 1 + 3 + 3bar with D-eigenvector vevs (0,0,1): M = [[y0,0,y3],[0,y0,0],[y3b,0,y0]] mixes "
      "generations 1 and 3 -- the vevs of 3 and 3bar carry different Z7 phases (zeta^4 vs zeta^3), so no common "
      "residual Z7 survives; only Z7-INVARIANT vevs (1', 1'' of F21) give a diagonal M",
      abs(H[0, 2]) > 1e-3 and np.allclose(Mz7[[0, 0, 1, 1, 2, 2], [1, 2, 0, 2, 0, 1]], [0, 0.4 + 0.3j, 0, 0, -0.2 + 0.5j, 0]),
      f"M = {np.round(Mz7, 3).tolist()}")

# =====================================================================================
# D. residual symmetries: mixing matrices from pairs of subgroups
# =====================================================================================
def cyclic_subgroups(G):
    mt = G["mt"]
    n = mt.shape[0]
    seen = set()
    subs = []
    for g in range(1, n):
        els = [0]
        x = g
        while x != 0:
            els.append(int(x))
            x = mt[x, g]
        key = frozenset(els)
        if key not in seen:
            seen.add(key)
            subs.append((int(G["order"][g]), g, sorted(els)))
    return subs


def klein_subgroups(G):
    mt = G["mt"]
    inv2 = [g for g in range(mt.shape[0]) if G["order"][g] == 2]
    seen = set()
    subs = []
    for a, b in itertools.combinations(inv2, 2):
        if mt[a, b] == mt[b, a] and G["order"][mt[a, b]] == 2:
            key = frozenset([0, a, b, int(mt[a, b])])
            if key not in seen:
                seen.add(key)
                subs.append((a, b))
    return subs


def eigbasis(r3, g):
    w, V = np.linalg.eig(r3[g])
    return w, V


def nondeg_basis(r3, elems_gen):
    """Common eigenbasis of the listed generators if it is unique (non-degenerate joint spectrum)."""
    M = sum((k + 1.37) * r3[g] for k, g in enumerate(elems_gen))
    # joint eigenvectors of commuting unitaries: diagonalise a generic combination
    w, V = np.linalg.eig(M)
    labels = [tuple(np.round([np.vdot(V[:, i], r3[g] @ V[:, i]) for g in elems_gen], 8)) for i in range(3)]
    nondeg = len(set(labels)) == 3
    Q, _ = np.linalg.qr(V)
    # QR keeps column spans for orthogonal eigenvectors; re-normalize original columns instead
    V = V / np.linalg.norm(V, axis=0)
    return nondeg, V


def residual_catalogue(gname):
    G = GROUPS[gname]
    r3 = G["irreps"]["3"]
    cyc = cyclic_subgroups(G)
    kl = klein_subgroups(G) if gname == "PSL" else []
    dirac, maj_full, maj_z2 = [], [], []
    for (o, g, els) in cyc:
        nd, V = nondeg_basis(r3, [g])
        if nd:
            dirac.append((f"Z{o}", V, g))
        if o == 2:
            w, Vz = np.linalg.eig(r3[g])
            maj_z2.append(("Z2", Vz, w, g))
    for (a, b) in kl:
        nd, V = nondeg_basis(r3, [a, b])
        assert nd
        dirac.append(("Z2xZ2", V, (a, b)))
        maj_full.append(("Z2xZ2", V, (a, b)))
    # Majorana residual symmetry needs eigenvalues +-1 only: check Z3/Z7 force degeneracy or vanish
    return dirac, maj_full, maj_z2, cyc


def pattern_key(U):
    """|U|^2 up to row and column permutations (canonical sorted form)."""
    A = np.abs(U) ** 2
    best = None
    for pr in itertools.permutations(range(3)):
        for pc in itertools.permutations(range(3)):
            t = tuple(np.round(A[np.ix_(pr, pc)], 6).ravel())
            if best is None or t < best:
                best = t
    return best


def best_fit_perm(U, kind):
    best = (np.inf, None, None)
    for pr in itertools.permutations(range(3)):
        for pc in itertools.permutations(range(3)):
            Up = U[np.ix_(pr, pc)]
            for conj in (False, True):
                Uc = np.conj(Up) if conj else Up
                c2, det = chi2_pmns(Uc) if kind == "PMNS" else chi2_ckm(Uc)
                if c2 < best[0]:
                    best = (c2, det, (pr, pc, conj))
    return best


resid = {}
for gname in ("F21", "PSL"):
    dirac, maj_full, maj_z2, cyc = residual_catalogue(gname)
    G = GROUPS[gname]
    r3 = G["irreps"]["3"]
    counts = {}
    for (o, g, els) in cyc:
        counts[f"Z{o}"] = counts.get(f"Z{o}", 0) + 1
    if gname == "PSL":
        counts["Z2xZ2"] = len(maj_full)
    # Majorana compatibility of each cyclic subgroup: general symmetric M with g^T M g = M
    maj_compat = {}
    for (o, g, els) in cyc:
        if f"Z{o}" in maj_compat:
            continue
        rows = [np.kron(r3[g].T, r3[g].T) - np.eye(9)]
        from e4lib import nullspace
        Nsp = nullspace(np.vstack(rows))
        Ms = []
        for k in range(Nsp.shape[1]):
            T = Nsp[:, k].reshape(3, 3)
            T = (T + T.T) / 2
            if np.linalg.norm(T) > 1e-9:
                Ms.append(T)
        if Ms:
            Mr = sum((rng.normal() + 1j * rng.normal()) * T for T in Ms)
            sv = np.linalg.svd(Mr, compute_uv=False)
            svs = np.sort(sv)
            degenerate = bool(min(np.diff(svs)) < 1e-9 * max(1, svs[-1]))
            maj_compat[f"Z{o}"] = {"dim_invariant_sym_M": len(Ms), "random_sv": svs.round(6).tolist(),
                                   "degenerate_or_zero": degenerate or svs[0] < 1e-9}
        else:
            maj_compat[f"Z{o}"] = {"dim_invariant_sym_M": 0, "degenerate_or_zero": True}
    print(f"\n=== {gname}: cyclic subgroups {counts}; Majorana compatibility: "
          + "; ".join(f"{k}: dim {v['dim_invariant_sym_M']}, degenerate/zero={v['degenerate_or_zero']}" for k, v in maj_compat.items()))

    # Dirac x Dirac (quarks, or Dirac neutrinos) and Dirac x Majorana-Klein (leptons)
    patterns = {}
    def add(kind, nl, Vl, nn, Vn, label_extra=""):
        U = Vl.conj().T @ Vn
        key = pattern_key(U)
        tag = (kind, nl, nn, key)
        if tag in patterns:
            patterns[tag]["count"] += 1
            return
        if kind == "quark":
            c2, det, perm = best_fit_perm(U, "CKM")
        else:
            c2, det, perm = best_fit_perm(U, "PMNS")
        patterns[tag] = {"kind": kind, "G1": nl, "G2": nn, "absU2_canonical": np.array(key).reshape(3, 3).tolist(),
                         "chi2": float(c2), "best": det, "count": 1}

    for (nl, Vl, gl) in dirac:
        for (nn, Vn, gn) in dirac:
            add("quark", nl, Vl, nn, Vn)
            add("lepton-Dirac-nu", nl, Vl, nn, Vn)
        for (nn, Vn, gn) in maj_full:
            add("lepton-Majorana", nl, Vl, nn, Vn)
    resid[gname] = {"subgroup_counts": counts, "majorana_compatibility": maj_compat,
                    "patterns": list(patterns.values()), "maj_z2": maj_z2, "dirac": dirac}

# Z2-partial Majorana classes (PSL only): one column fixed, angle theta and phase phi free
def fit_z2_partial(Vl, Vz, wz):
    plus = np.where(np.abs(wz - 1) < 1e-8)[0]
    minus = np.where(np.abs(wz + 1) < 1e-8)[0]
    if len(plus) != 1 or len(minus) != 2:
        return None
    u0 = Vz[:, plus[0]] / np.linalg.norm(Vz[:, plus[0]])
    Q, _ = np.linalg.qr(Vz[:, minus])
    u1, u2 = Q[:, 0], Q[:, 1]
    best = (np.inf, None)
    th_grid = np.linspace(0, np.pi, 91)
    ph_grid = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    for th in th_grid:
        for ph in ph_grid:
            a = math.cos(th) * u1 + math.sin(th) * np.exp(1j * ph) * u2
            b = -math.sin(th) * np.exp(-1j * ph) * u1 + math.cos(th) * u2
            Vn = np.column_stack([u0, a, b])
            U = Vl.conj().T @ Vn
            for pr in itertools.permutations(range(3)):
                for pc in itertools.permutations(range(3)):
                    c2, det = chi2_pmns(U[np.ix_(pr, pc)])
                    if c2 < best[0]:
                        best = (c2, (th, ph, pr, pc))
    # refine
    from scipy.optimize import minimize
    th0, ph0, pr, pc = best[1]
    def f(x):
        a = math.cos(x[0]) * u1 + math.sin(x[0]) * np.exp(1j * x[1]) * u2
        b = -math.sin(x[0]) * np.exp(-1j * x[1]) * u1 + math.cos(x[0]) * u2
        U = Vl.conj().T @ np.column_stack([u0, a, b])
        return chi2_pmns(U[np.ix_(pr, pc)])[0]
    r = minimize(f, [th0, ph0], method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 4000})
    a = math.cos(r.x[0]) * u1 + math.sin(r.x[0]) * np.exp(1j * r.x[1]) * u2
    b = -math.sin(r.x[0]) * np.exp(-1j * r.x[1]) * u1 + math.cos(r.x[0]) * u2
    U = Vl.conj().T @ np.column_stack([u0, a, b])
    c2, det = chi2_pmns(U[np.ix_(pr, pc)])
    fixed_col = np.abs(Vl.conj().T @ u0) ** 2
    return {"chi2": float(c2), "best": det, "theta": float(r.x[0]), "phi": float(r.x[1]),
            "fixed_column_abs2": np.sort(fixed_col).round(6).tolist()}


z2_partial = []
seen_keys = set()
for (nl, Vl, gl) in resid["PSL"]["dirac"]:
    for (nz, Vz, wz, gz) in resid["PSL"]["maj_z2"]:
        u0 = Vz[:, np.argmin(np.abs(wz - 1))]
        key = (nl, tuple(np.sort(np.round(np.abs(Vl.conj().T @ u0) ** 2, 6))))
        if key in seen_keys:
            continue
        seen_keys.add(key)
        out = fit_z2_partial(Vl, Vz, wz)
        if out:
            out.update({"G_l": nl, "G_nu": "Z2"})
            z2_partial.append(out)
print(f"\n=== PSL Z2-partial Majorana classes (column fixed by a Z2, 2 free real parameters): {len(z2_partial)} distinct")
for o in sorted(z2_partial, key=lambda x: x["chi2"]):
    print(f"  G_l={o['G_l']:<6} fixed column |U|^2 {o['fixed_column_abs2']}  chi2_min={o['chi2']:.2f}  "
          f"s12^2={o['best']['s12sq']:.3f} s13^2={o['best']['s13sq']:.4f} s23^2={o['best']['s23sq']:.3f} delta={o['best']['delta_deg']:.0f}")

# summarize residual patterns
from scipy.stats import chi2 as chi2dist
summary_resid = {}
for gname in ("F21", "PSL"):
    rows = []
    for p in resid[gname]["patterns"]:
        ndof = 4
        pval = float(chi2dist.sf(p["chi2"], ndof))
        p["p_value"] = pval
        p["survives(p>0.01)"] = bool(pval > 0.01)
        rows.append(p)
    rows.sort(key=lambda x: (x["kind"], x["chi2"]))
    print(f"\n=== {gname}: residual-symmetry mixing patterns (masses free; 0 mixing parameters; 4 observables)")
    for p in rows:
        b = p["best"]
        if p["kind"] == "quark":
            desc = f"lambda={b['lambda']:.4f} A={b['A']:.3f} rhobar={b['rhobar']:.3f} etabar={b['etabar']:.3f}"
        else:
            desc = f"s12^2={b['s12sq']:.3f} s13^2={b['s13sq']:.4f} s23^2={b['s23sq']:.3f} delta={b['delta_deg']:.0f}"
        print(f"  {p['kind']:<16} G1={p['G1']:<6} G2={p['G2']:<6} chi2={p['chi2']:9.1f} p={p['p_value']:.1e} "
              f"{'SURVIVES' if p['survives(p>0.01)'] else 'excluded'}  {desc}")
    summary_resid[gname] = rows
for o in z2_partial:
    o["p_value"] = float(chi2dist.sf(o["chi2"], 2))
    o["survives(p>0.01)"] = bool(o["p_value"] > 0.01)

f21_pat_sets = {tuple(map(tuple, np.round(np.array(p["absU2_canonical"]), 4))) for p in summary_resid["F21"]}
check("F21 residual patterns: only identity, trimaximal (all |U|^2 = 1/3) and Z3-Z3' patterns arise",
      len(f21_pat_sets) <= 3, f"{len(f21_pat_sets)} distinct |U|^2 patterns")
check("F21: no subgroup can be the residual symmetry of a non-degenerate Majorana mass matrix "
      "(F21 has odd order: no Z2; Z3 -> degenerate pair, Z7 -> M = 0)",
      all(v["degenerate_or_zero"] for v in resid["F21"]["majorana_compatibility"].values()))

# =====================================================================================
# does LNR's light-neutrino matrix have a residual symmetry inside the seed's PSL(2,7)?
# =====================================================================================
Mnu_lnr = 0.5 * np.array([[0, 1, 1], [1, -4, 5], [1, 5, -4]], dtype=complex)
r3P = PI["3"]
stab_nu = [g for g in range(r3P.shape[0]) if np.allclose(r3P[g].T @ Mnu_lnr @ r3P[g], Mnu_lnr, atol=1e-9)]
stab_nu_F = [g for g in range(FI["3"].shape[0]) if np.allclose(FI["3"][g].T @ Mnu_lnr @ FI["3"][g], Mnu_lnr, atol=1e-9)]
S_tbm = np.array([[-1, 2, 2], [2, -1, 2], [2, 2, -1]]) / 3
U_mt = -np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
in_psl = lambda M: any(np.allclose(r3P[g], M, atol=1e-9) for g in range(r3P.shape[0]))
lnr_resid = {"elements_of_PSL_leaving_Mnu_invariant": len(stab_nu), "elements_of_F21": len(stab_nu_F),
             "TBM_S_in_PSL": bool(in_psl(S_tbm)), "minus_mu_tau_swap_in_PSL": bool(in_psl(U_mt)),
             "TBM_S_invariance": bool(np.allclose(S_tbm.T @ Mnu_lnr @ S_tbm, Mnu_lnr)),
             "mu_tau_invariance": bool(np.allclose(U_mt.T @ Mnu_lnr @ U_mt, Mnu_lnr))}
print("\n=== LNR light-neutrino matrix: residual symmetry inside the seed's groups:", lnr_resid)
check("LNR's M_nu is invariant under the TBM Klein group (S, mu-tau) but only the identity of the seed's "
      "PSL(2,7) leaves it invariant: its TBM structure is accidental (parameter choice), not residual",
      lnr_resid["TBM_S_invariance"] and lnr_resid["mu_tau_invariance"] and len(stab_nu) == 1)

res = {"dirac_invariants": yuk, "majorana_invariants": maj, "schur": schur,
       "alignments_F21": align_res, "aligned_mass_cases": aligned_masses,
       "residual_subgroups": {g: {"subgroup_counts": resid[g]["subgroup_counts"],
                                  "majorana_compatibility": resid[g]["majorana_compatibility"]} for g in resid},
       "residual_patterns": summary_resid, "z2_partial_PSL": z2_partial, "lnr_residual": lnr_resid,
       "checks": CHECKS, "all_pass": all(v["pass"] for v in CHECKS.values()),
       "runtime_s": round(time.time() - t0, 1)}


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    if isinstance(o, complex):
        return [o.real, o.imag]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    return o


with open(os.path.join(OUT, "yukawa.json"), "w") as f:
    json.dump(clean(res), f, indent=1)
print(f"\n{sum(v['pass'] for v in CHECKS.values())}/{len(CHECKS)} checks pass; runtime {time.time() - t0:.1f} s")
sys.exit(0 if res["all_pass"] else 1)
