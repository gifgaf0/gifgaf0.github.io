"""
cc_residual.py -- independent cross-check of the residual-symmetry ("direct approach") mixing patterns
for F21 and the seed's PSL(2,7), and of the PSL Z2-partial classes.

My own conventions (checked against the report's stated ones):
  * G_l: abelian subgroup with non-degenerate joint eigenspaces on the 3 (cyclic Z3, Z4, Z7 or Klein V4);
  * G_nu: same set for Dirac neutrinos; Klein V4 for Majorana neutrinos;
  * U = V_l^dagger V_nu, fitted over all 36 row/column permutations and complex conjugation; 0 parameters;
  * Z2-partial: G_nu = Z2 = <t>, fixed column = +1 eigenvector of t; the -1 eigenspace rotated by
    R(theta, phi) (2 parameters); grid + Nelder-Mead from many starts.
  * chi^2 with NuFIT 6.0 (IC19 w/o SK-atm, NO) one-sided sigma = (3sigma edge - bf)/3, as in the report;
    delta handled two ways: (a) pull with the representation of delta (mod 360) giving the smaller
    |pull| (respects the 3sigma range 96..422 deg), (b) delta mapped into [bf-180, bf+180).
Writes out/residual_cc.json.
"""
import json, math, cmath, itertools
import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2 as chi2dist

base = "/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/"
OUT, CHECKS = {}, {}
def check(name, ok):
    CHECKS[name] = bool(ok); print(("PASS " if ok else "FAIL ") + name)
F21 = list(np.load(base + "F21_elements.npy")); PSL = list(np.load(base + "PSL_elements.npy"))
I = np.eye(3, dtype=complex)
key = lambda M: tuple(np.round(M, 6).ravel().view(float))

NU = {"s12sq": (0.307, 0.275, 0.345), "s13sq": (0.02195, 0.02023, 0.02376), "s23sq": (0.561, 0.430, 0.596), "delta": (177., 96., 422.)}
def pull1(name, x):
    bf, lo, hi = NU[name]
    return (x - bf) / ((hi - bf) / 3 if x > bf else (bf - lo) / 3)
def pull_delta(d, mode="a"):
    if d is None: return 0.0
    if mode == "a":
        return min((pull1("delta", d + k * 360) for k in (-1, 0, 1)), key=abs)
    dd = (d - 177 + 180) % 360 - 180 + 177
    return pull1("delta", dd)

def angles(U):
    Ua = np.abs(U)
    s13sq = Ua[0, 2] ** 2
    c13sq = 1 - s13sq
    if c13sq < 1e-14: return None
    s12sq = Ua[0, 1] ** 2 / c13sq; s23sq = Ua[1, 2] ** 2 / c13sq
    J = np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0]))
    s12, c12, s23, c23, s13 = math.sqrt(s12sq), math.sqrt(max(0, 1 - s12sq)), math.sqrt(s23sq), math.sqrt(max(0, 1 - s23sq)), math.sqrt(s13sq)
    den = s12 * c12 * s23 * c23 * s13
    if den < 1e-10:
        return s12sq, s13sq, s23sq, None, J
    cosd = (Ua[1, 0] ** 2 - s12sq * c23 ** 2 - c12 ** 2 * s23sq * s13sq) / (2 * den)
    sind = J / (den * c13sq)
    d = math.degrees(math.atan2(sind, cosd)) % 360
    return s12sq, s13sq, s23sq, d, J

def chi2_lepton(U, mode="a"):
    a = angles(U)
    if a is None: return 1e9, None
    s12sq, s13sq, s23sq, d, J = a
    p = [pull1("s12sq", s12sq), pull1("s13sq", s13sq), pull1("s23sq", s23sq), pull_delta(d, mode)]
    return sum(x * x for x in p), dict(s12sq=s12sq, s13sq=s13sq, s23sq=s23sq, delta=d, J=J, pulls=p)

PERMS = [np.eye(3)[list(p)] for p in itertools.permutations(range(3))]
def best_over_perms(U, f):
    best = (1e18, None)
    for Pr in PERMS:
        for Pc in PERMS:
            for Uc in (U, U.conj()):
                c, info = f(Pr @ Uc @ Pc)
                if c < best[0]: best = (c, info)
    return best

# CKM
CK = {"lambda": (0.22519, 0.00083), "A": (0.828, 0.011), "rhobar": (0.1609, 0.0095), "etabar": (0.347, 0.010)}
def ckm_obs(V):
    Va = np.abs(V)
    den = math.sqrt(Va[0, 0] ** 2 + Va[0, 1] ** 2)
    if den < 1e-12: return None
    lam = Va[0, 1] / den
    if lam < 1e-12 or Va[0, 0] < 1e-12: return None
    A = Va[1, 2] / (lam * Va[0, 1]) if Va[0, 1] > 1e-12 else 1e6
    x = V[1, 0] * np.conj(V[1, 2])
    if abs(x) < 1e-14: return None
    z = -(V[0, 0] * np.conj(V[0, 2])) / x
    return lam, A, z.real, z.imag
def chi2_ckm(V):
    o = ckm_obs(V)
    if o is None: return 1e12, None
    c = sum(((v - CK[k][0]) / CK[k][1]) ** 2 for v, k in zip(o, ("lambda", "A", "rhobar", "etabar")))
    return c, dict(zip(("lambda", "A", "rhobar", "etabar"), o))

def elem_order(g):
    P = I.copy()
    for n in range(1, 30):
        P = P @ g
        if np.allclose(P, I): return n

def abelian_nondeg_subgroups(G):
    subs = {}
    for g in G:
        o = elem_order(g)
        if o in (3, 4, 7):
            H = [np.linalg.matrix_power(g, k) for k in range(o)]
            ks = frozenset(key(h) for h in H)
            if ks not in subs: subs[ks] = (f"Z{o}", H, [g])
    invol = [g for g in G if elem_order(g) == 2]
    for a, b in itertools.combinations(invol, 2):
        if np.allclose(a @ b, b @ a):
            H = [I, a, b, a @ b]
            ks = frozenset(key(h) for h in H)
            if ks not in subs: subs[ks] = ("Z2xZ2", H, [a, b])
    return list(subs.values())

def joint_eigvecs(gens):
    # random combination of generators has distinct eigenvalues iff joint eigenspaces are 1-dim
    rng = np.random.default_rng(11)
    M = sum((rng.normal() + 1j * rng.normal()) * g for g in gens)
    vals, V = np.linalg.eig(M)
    assert min(abs(vals[i] - vals[j]) for i in range(3) for j in range(i + 1, 3)) > 1e-6
    # orthonormalise (eigenvectors of commuting unitaries are orthogonal)
    V = V / np.linalg.norm(V, axis=0)
    return V

def residual_patterns(G, gname):
    subs = abelian_nondeg_subgroups(G)
    counts = {}
    for t, H, g in subs: counts[t] = counts.get(t, 0) + 1
    print(f"  {gname}: non-degenerate abelian subgroups {counts}")
    Vs = [(t, joint_eigvecs(g)) for t, H, g in subs]
    res = {"lepton-Dirac": [], "lepton-Majorana": [], "CKM": []}
    structs = set()
    best = {k: (1e18, None, None) for k in res}
    for (tl, Vl), (tn, Vn) in itertools.product(Vs, Vs):
        U = Vl.conj().T @ Vn
        A2 = np.round(np.abs(U) ** 2, 6)
        # canonical |U|^2 up to row/col perms
        can = min(tuple(np.round((Pr @ A2 @ Pc), 6).ravel()) for Pr in PERMS for Pc in PERMS)
        structs.add(can)
        cD, iD = best_over_perms(U, chi2_lepton)
        if cD < best["lepton-Dirac"][0]: best["lepton-Dirac"] = (cD, iD, f"{tl} x {tn}")
        if tn == "Z2xZ2" and cD < best["lepton-Majorana"][0]: best["lepton-Majorana"] = (cD, iD, f"{tl} x {tn}")
        cQ, iQ = best_over_perms(U, chi2_ckm)
        if cQ < best["CKM"][0]: best["CKM"] = (cQ, iQ, f"{tl} x {tn}")
    print(f"  {gname}: distinct |U|^2 structures (up to row/col perms): {len(structs)}")
    for k, v in best.items():
        print(f"  {gname} best {k}: chi2 = {v[0]:.4g} ({v[2]}) {v[1]}")
    return subs, structs, best

OUT["F21"] = {}; OUT["PSL"] = {}
subsF, structF, bestF = residual_patterns(F21, "F21")
subsP, structP, bestP = residual_patterns(PSL, "PSL")
nF = {}; [nF.__setitem__(t, nF.get(t, 0) + 1) for t, _, _ in subsF]
nP = {}; [nP.__setitem__(t, nP.get(t, 0) + 1) for t, _, _ in subsP]
n_invol = sum(1 for g in PSL if elem_order(g) == 2)
check("subgroup counts: F21 Z7 x1, Z3 x7; PSL Z7 x8, Z3 x28, Z4 x21, V4 x14, Z2 x21",
      nF == {"Z7": 1, "Z3": 7} and nP == {"Z7": 8, "Z3": 28, "Z4": 21, "Z2xZ2": 14} and n_invol == 21)
check("F21: 3 |U|^2 structures; best lepton chi2 = 2459 (+-1); best CKM chi2 ~ 1.08e5 (+-1%)",
      len(structF) == 3 and abs(bestF["lepton-Dirac"][0] - 2459.1) < 1 and abs(bestF["CKM"][0] / 1.08e5 - 1) < 0.01)
check("F21 has no Klein subgroup -> no Majorana pattern", bestF["lepton-Majorana"][0] > 1e17)
check("PSL: best lepton (Dirac) chi2 = 200 (Z3 x Z7), best Klein-Majorana 692, best CKM 7.7e4 (each +-1%)",
      abs(bestP["lepton-Dirac"][0] / 200.0 - 1) < 0.01 and abs(bestP["lepton-Majorana"][0] / 692 - 1) < 0.01 and abs(bestP["CKM"][0] / 7.72e4 - 1) < 0.01)
# delta convention (b)
def best_mode_b(subs):
    Vs = [joint_eigvecs(g) for t, H, g in subs]
    b = 1e18
    for Vl, Vn in itertools.product(Vs, Vs):
        c, _ = best_over_perms(Vl.conj().T @ Vn, lambda U: chi2_lepton(U, "b"))
        b = min(b, c)
    return b
bPb = best_mode_b(subsP)
print(f"  PSL best lepton chi2 with delta mapped into [bf-180, bf+180): {bPb:.4g}")
OUT["F21"] = {"n_structures": len(structF), "best": {k: [v[0], v[2], v[1]] for k, v in bestF.items()}}
OUT["PSL"] = {"n_structures": len(structP), "best": {k: [v[0], v[2], v[1]] for k, v in bestP.items()}, "best_lepton_delta_mode_b": bPb}

# ---------------------------------------------------------------- Z2-partial classes (PSL)
invol = [g for g in PSL if elem_order(g) == 2]
def conj_class_reps_of_subgroups(subs, G):
    reps = []
    seen = set()
    for t, H, gens in subs:
        ks = frozenset(key(h) for h in H)
        if ks in seen: continue
        orbit = set()
        for x in G:
            orbit.add(frozenset(key(x @ h @ x.conj().T) for h in H))
        seen |= orbit
        reps.append((t, H, gens))
    return reps
sub_reps = conj_class_reps_of_subgroups(subsP, PSL)
print("  PSL conjugacy classes of non-degenerate abelian subgroups:", [t for t, _, _ in sub_reps])

def fixed_and_W(t):
    vals, V = np.linalg.eigh((t + t.conj().T) / 2)   # involution is hermitian-unitary: eigenvalues +-1
    ip = int(np.argmax(vals))
    vplus = V[:, ip]; W = np.delete(V, ip, axis=1)
    return vplus, W

def U_partial(Vl, t, th, ph):
    vplus, W = fixed_and_W(t)
    R = np.array([[math.cos(th), math.sin(th) * cmath.exp(-1j * ph)], [-math.sin(th) * cmath.exp(1j * ph), math.cos(th)]])
    Wr = W @ R
    return Vl.conj().T @ np.column_stack([vplus, Wr[:, 0], Wr[:, 1]])

def fit_partial(Vl, t):
    best = (1e18, None, None)
    ths = np.linspace(0, math.pi, 61); phs = np.linspace(0, 2 * math.pi, 48, endpoint=False)
    for Pr in PERMS:
        for Pc in PERMS:
            f = lambda x: chi2_lepton(Pr @ U_partial(Vl, t, x[0], x[1]) @ Pc)[0]
            grid = [(f((a, b)), a, b) for a in ths for b in phs]
            grid.sort(key=lambda q: q[0])
            for c0, a0, b0 in grid[:3]:
                r = minimize(f, [a0, b0], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000))
                if r.fun < best[0]:
                    best = (r.fun, r.x.copy(), (Pr, Pc))
    th, ph = best[1]; Pr, Pc = best[2]
    c, info = chi2_lepton(Pr @ U_partial(Vl, t, th, ph) @ Pc)
    return c, info

classes = []
for tl, H, gens in sub_reps:
    Vl = joint_eigvecs(gens)
    Hk = set(key(h) for h in H)
    # normaliser of H
    N = [x for x in PSL if set(key(x @ h @ x.conj().T) for h in H) == Hk]
    seen = set(); orbits = []
    for i, t in enumerate(invol):
        if key(t) in seen: continue
        orb = set(key(x @ t @ x.conj().T) for x in N)
        seen |= orb; orbits.append(t)
    for t in orbits:
        vplus, W = fixed_and_W(t)
        col = np.sort(np.round(np.abs(Vl.conj().T @ vplus) ** 2, 6))
        classes.append(dict(G_l=tl, t=t, Vl=Vl, col=col, inH=key(t) in Hk))
print(f"  Z2-partial (G_l class, involution orbit under N(G_l)) pairs: {len(classes)}")
# dedupe by (G_l type, fixed column pattern)
uniq = {}
for c in classes:
    k = (c["G_l"], tuple(c["col"]))
    uniq.setdefault(k, []).append(c)
print(f"  distinct (G_l type, fixed-column |.|^2) classes: {len(uniq)}")
part = []
for (tl, col), cl in sorted(uniq.items(), key=lambda q: (q[0][0], q[0][1])):
    # the reachable PMNS set depends only on |fixed column|^2 (row rephasing + the U(2) rotation of the
    # complement), so one member per (type, column) suffices; a second member is fitted as a check
    c = cl[0]
    chi, info = fit_partial(c["Vl"], c["t"])
    if len(cl) > 1:
        chi_b, _ = fit_partial(cl[-1]["Vl"], cl[-1]["t"])
        assert abs(chi_b - chi) < 1e-3 * max(1, chi), (chi, chi_b)
    p = 1 - chi2dist.cdf(chi, 2)
    part.append(dict(G_l=tl, fixed_col=list(col), chi2=chi, p=p, n_members=len(cl), info=info))
    print(f"    G_l={tl:6s} col={list(col)} members={len(cl)}  chi2={chi:9.3f}  p={p:.3g}  "
          + (f"s12sq={info['s12sq']:.3f} s13sq={info['s13sq']:.4f} s23sq={info['s23sq']:.3f} delta={info['delta']}" if info else ""))
surv = [q for q in part if q["p"] > 0.01]
OUT["z2_partial"] = [{k: (v if k != "info" else {kk: vv for kk, vv in v.items()}) for k, v in q.items()} for q in part]
print(f"  survivors (p > 0.01): {[(q['G_l'], q['fixed_col'], round(q['chi2'], 2)) for q in surv]}")
def has(tl, col, chi):
    return any(q["G_l"] == tl and np.allclose(sorted(q["fixed_col"]), sorted(col), atol=1e-4) and abs(q["chi2"] - chi) < 0.05 for q in surv)
check("Z2-partial: exactly three classes with p > 0.01: Z7 (chi2 2.13), Z3 TM1 (2.54), Z3 TM2 (7.63)",
      len(surv) == 3 and has("Z7", [0.131512, 0.204495, 0.663993], 2.13) and has("Z3", [1 / 6, 1 / 6, 2 / 3], 2.54) and has("Z3", [1 / 3, 1 / 3, 1 / 3], 7.63))
nxt = sorted(q["chi2"] for q in part if q["p"] <= 0.01)
print(f"  next-best chi2 after the survivors: {nxt[:3]}")
check("next class after survivors has chi2 = 31.5", abs(nxt[0] - 31.53) < 0.05)

OUT["checks"] = CHECKS; OUT["all_pass"] = all(CHECKS.values())
def js(x):
    if isinstance(x, dict): return {str(k): js(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [js(v) for v in x]
    if isinstance(x, np.ndarray): return js(x.tolist())
    if isinstance(x, (np.floating, np.integer)): return x.item()
    if isinstance(x, complex): return [x.real, x.imag]
    return x
json.dump(js(OUT), open(base + "residual_cc.json", "w"), indent=1)
print(f"\n{sum(CHECKS.values())}/{len(CHECKS)} checks pass")
