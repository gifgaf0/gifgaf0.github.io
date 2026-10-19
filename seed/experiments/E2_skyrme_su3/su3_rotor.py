#!/usr/bin/env python3
"""E2 -- SU(2) and SU(3) rigid-rotor quantisation of the hedgehog, fits, spectrum, N_c parity,
and (optional, clearly labelled) first-order symmetry breaking / Guadagnini relation.

Rotor (Diakonov-Petrov-Polyakov hep-ph/9703373 eqs. 5-8; Praszalowicz hep-ph/0308114 eq. 3):
   H = M + (1/2I1) sum_{a=1..3} R_a^2 + (1/2I2) sum_{a=4..7} R_a^2,
   Wess-Zumino constraint Y_R = N_c B/3 (B = 1); allowed irreps (p,q) contain states with Y = N_c/3,
   and the isospin of those states is the spin J. Then
   E(p,q,J) = M + C2(p,q)/(2I2) + (1/2I1 - 1/2I2) J(J+1) - N_c^2/(24 I2),
   C2(p,q) = (p^2 + q^2 + pq + 3(p+q))/3.
SU(2) rotor (ANW): E = M + J(J+1)/(2 I1), J = I = 1/2 (N), 3/2 (Delta).

SU(3) irreps are built explicitly (tensor powers of 3 and 3bar, highest-weight vector, lowering
operators), so the Casimir, the rotor Hamiltonian and D^(8) matrix elements are computed, not quoted.
Matrix elements of Wigner D functions use intertwiners V_R -> V_8 (x) V_R' (SU(3) Clebsch-Gordan
coefficients obtained as the null space of the intertwining equations), with
   <R nu nu'| D^(8)_ab |R' mu mu'> = sqrt(d_R'/d_R) sum_gamma C^{R gamma nu}_{8a,R'mu} C^{R gamma nu'*}_{8b,R'mu'}.

Reads out/hedgehog.json (from skyrme_hedgehog.py); writes out/rotor.json. Runtime ~30 s.
"""
import itertools
import json
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

# ----------------------------------------------------------------------------- su(3) basics
lam = np.zeros((8, 3, 3), complex)
lam[0][0, 1] = lam[0][1, 0] = 1
lam[1][0, 1] = -1j; lam[1][1, 0] = 1j
lam[2][0, 0] = 1; lam[2][1, 1] = -1
lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2] = -1j; lam[4][2, 0] = 1j
lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2] = -1j; lam[6][2, 1] = 1j
lam[7] = np.diag([1, 1, -2]) / np.sqrt(3)
T3f = lam / 2
fabc = np.zeros((8, 8, 8))
for a in range(8):
    for b in range(8):
        for c in range(8):
            fabc[a, b, c] = (-0.25j * np.trace((lam[a] @ lam[b] - lam[b] @ lam[a]) @ lam[c])).real
T8adj = np.array([-1j * fabc[a] for a in range(8)])     # (T_a)_{bc} = -i f_abc ; e_8 is the eta direction


def C2(p, q):
    return Fr(p * p + q * q + p * q + 3 * (p + q), 3)


def dim(p, q):
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def gt_content(p, q):
    """Isospin multiplets (Y, I) of irrep (p,q) from Gelfand-Tsetlin patterns: top row (p+q, q, 0)."""
    out = []
    for m12 in range(q, p + q + 1):
        for m22 in range(0, q + 1):
            Y = Fr(m12 + m22) - Fr(2 * (p + 2 * q), 3)
            out.append((Y, Fr(m12 - m22, 2)))
    return out


def irrep_name(p, q):
    d = dim(p, q)
    names = {(0, 0): "1", (1, 0): "3", (0, 1): "3bar", (2, 0): "6", (0, 2): "6bar", (1, 1): "8",
             (3, 0): "10", (0, 3): "10bar", (2, 1): "15", (1, 2): "15bar", (4, 0): "15'", (0, 4): "15'bar",
             (2, 2): "27", (4, 1): "35", (1, 4): "35bar", (5, 0): "21", (0, 5): "21bar", (3, 3): "64",
             (3, 2): "42", (2, 3): "42bar", (6, 0): "28", (0, 6): "28bar", (5, 1): "48", (1, 5): "48bar"}
    return names.get((p, q), f"{d}({p},{q})")


def build_irrep(p, q):
    """Explicit irrep (p,q): Hermitian generators T[8] (d x d) in a basis of (Y, I, I3) states with
    Condon-Shortley phases inside each isospin multiplet. Returns dict."""
    fund = [T3f[a] for a in range(8)]
    anti = [-T3f[a].T for a in range(8)]
    facs = [fund] * p + [anti] * q
    n = len(facs)
    D = 3 ** n
    X = []
    for a in range(8):
        M = np.zeros((D, D), complex)
        for k in range(n):
            ops = [np.eye(3)] * n
            ops[k] = facs[k][a]
            K = ops[0]
            for o in ops[1:]:
                K = np.kron(K, o)
            M += K
        X.append(M)
    hw = np.array([1.0 + 0j])
    for k in range(n):
        e = np.zeros(3, complex)
        e[0 if k < p else 2] = 1.0
        hw = np.kron(hw, e)
    low = [X[0] - 1j * X[1], X[3] - 1j * X[4], X[5] - 1j * X[6]]
    basis = hw[:, None] / np.linalg.norm(hw)
    frontier = basis
    while True:
        new = np.hstack([Lo @ frontier for Lo in low])
        allv = np.hstack([basis, new])
        u, s, vh = np.linalg.svd(allv, full_matrices=False)
        r = int(np.sum(s > 1e-9 * s[0]))
        if r == basis.shape[1]:
            break
        Qb = u[:, :r]
        frontier = Qb
        basis = Qb
    Q = basis
    d = Q.shape[1]
    assert d == dim(p, q), (p, q, d)
    T = np.array([Q.conj().T @ Xa @ Q for Xa in X])
    # label basis by (Y, I, I3)
    Y = (2 / np.sqrt(3)) * T[7]
    I2 = T[0] @ T[0] + T[1] @ T[1] + T[2] @ T[2]
    Hlab = Y * 1.0 + I2 * np.sqrt(2) * 0.137 + T[2] * np.pi * 0.0113
    w, V = np.linalg.eigh(Hlab)
    labels = []
    for k in range(d):
        v = V[:, k]
        yv = (v.conj() @ Y @ v).real
        iv = (v.conj() @ I2 @ v).real
        i3 = (v.conj() @ T[2] @ v).real
        Ival = (-1 + np.sqrt(1 + 4 * iv)) / 2
        labels.append((Fr(round(3 * yv), 3), Fr(round(2 * Ival), 2), Fr(round(2 * i3), 2)))
    groups = {}
    for k, lb in enumerate(labels):
        groups.setdefault((lb[0], lb[1]), []).append(k)
    Iminus = T[0] - 1j * T[1]
    newV = []
    newlab = []
    for (yv, Iv), ks in sorted(groups.items(), key=lambda z: (-z[0][0], -z[0][1])):
        assert len(ks) == int(2 * Iv + 1), "isospin multiplet multiplicity problem"
        top = [k for k in ks if labels[k][2] == Iv][0]
        v = V[:, top].copy()
        j = np.argmax(np.abs(v))
        v = v * np.exp(-1j * np.angle(v[j]))
        m = Iv
        while True:
            newV.append(v)
            newlab.append((yv, Iv, m))
            if m == -Iv:
                break
            v = Iminus @ v / np.sqrt(float((Iv + m) * (Iv - m + 1)))
            m -= 1
    B = np.array(newV).T
    Tl = np.array([B.conj().T @ Ta @ B for Ta in T])
    index = {lb: k for k, lb in enumerate(newlab)}
    return {"p": p, "q": q, "d": d, "T": Tl, "labels": newlab, "index": index}


def intertwiners(XA, XB, C2A):
    """Orthonormal intertwiners T_gamma: V_A -> V_B (T X^A = X^B T for all generators)."""
    dA = XA[0].shape[0]
    C2B = sum(X @ X for X in XB)
    w, V = np.linalg.eigh(C2B)
    P = V[:, np.abs(w - C2A) < 1e-8]
    k = P.shape[1]
    if k == 0:
        return []
    Yg = [P.conj().T @ X @ P for X in XB]
    M = np.vstack([np.kron(XA[a].T, np.eye(k)) - np.kron(np.eye(dA), Yg[a]) for a in range(len(XA))])
    u, s, vh = np.linalg.svd(M)
    ns = vh.shape[0]
    svals = np.concatenate([s, np.zeros(ns - s.size)])
    null = vh[svals < 1e-9].conj()
    Ts = [P @ nv.reshape((k, dA), order="F") for nv in null]
    if not Ts:
        return []
    G = np.array([[np.trace(a.conj().T @ b) / dA for b in Ts] for a in Ts])
    ev, U = np.linalg.eigh(G)
    Ginvh = U @ np.diag(ev ** -0.5) @ U.conj().T
    Ts = [sum(Ginvh[j, g] * Ts[j] for j in range(len(Ts))) for g in range(len(Ts))]
    for Tg in Ts:
        for a in range(len(XA)):
            assert np.max(np.abs(Tg @ XA[a] - XB[a] @ Tg)) < 1e-9
        assert np.max(np.abs(Tg.conj().T @ Tg - np.eye(dA))) < 1e-9
    return Ts


def Dme(R, Rp, left, right, a=7, b=7, adj=None):
    """<R left right| D^(8)_ab |Rp left right> (same labels on both sides); a, b are 0-based Gell-Mann
    indices (7 = lambda_8). adj: generators of the 'adjoint' factor (default su(3) adjoint)."""
    adj = T8adj if adj is None else adj
    dA = adj.shape[1]
    XB = [np.kron(adj[g], np.eye(Rp["d"])) + np.kron(np.eye(dA), Rp["T"][g]) for g in range(len(adj))]
    XA = [R["T"][g] for g in range(len(adj))]
    c2 = (sum(X @ X for X in XA))[0, 0].real
    Ts = intertwiners(XA, XB, c2)
    nu = R["index"][left]; nup = R["index"][right]
    mu = Rp["index"][left]; mup = Rp["index"][right]
    val = 0.0
    for Tg in Ts:
        val += Tg[a * Rp["d"] + mu, nu] * np.conj(Tg[b * Rp["d"] + mup, nup])
    return np.sqrt(Rp["d"] / R["d"]) * val, len(Ts)


# ----------------------------------------------------------------------------- PDG masses
def pdg_masses():
    names = {"p": "p", "n": "n", "Lambda": "Lambda", "Sigma+": "Sigma+", "Sigma0": "Sigma0", "Sigma-": "Sigma-",
             "Xi0": "Xi0", "Xi-": "Xi-", "Sigma*+": "Sigma(1385)+", "Sigma*0": "Sigma(1385)0",
             "Sigma*-": "Sigma(1385)-", "Xi*0": "Xi(1530)0", "Xi*-": "Xi(1530)-", "Omega-": "Omega-"}
    m = {}
    src = "PDG 2026 via the pdg Python package (pdg 2026.0, sqlite)"
    try:
        import warnings
        warnings.filterwarnings("ignore")
        import pdg
        api = pdg.connect()
        for k, nm in names.items():
            ps = api.get_particles_by_name(nm)
            m[k] = 1000.0 * float(ps[0].mass)
        dl = api.get_particles_by_name("Delta(1232)++")[0]
        dmass = [x for x in dl.masses()][0]
        m["Delta"] = float(dmass.value)
        m["_Delta_note"] = f"PDG B033M Breit-Wigner mass, mixed charges: {dmass.display_value_text}"
        m["_edition"] = str(api.edition)
    except Exception as ex:  # fallback: values read from PDG 2026 on 2026-10-18 with the same package
        src = f"fallback table (pdg package unavailable: {ex})"
        m = {"p": 938.2720894, "n": 939.5654219, "Lambda": 1115.683139, "Sigma+": 1189.370041,
             "Sigma0": 1192.641932, "Sigma-": 1197.449382, "Xi0": 1314.860776, "Xi-": 1321.710838,
             "Sigma*+": 1382.833139, "Sigma*0": 1383.814792, "Sigma*-": 1387.183058, "Xi*0": 1531.800943,
             "Xi*-": 1534.972219, "Omega-": 1672.451953, "Delta": 1232.0,
             "_Delta_note": "PDG B033M Breit-Wigner mass, mixed charges: 1230 to 1234 (~1232)"}
    iso = {
        "N": (m["p"] + m["n"]) / 2, "Lambda": m["Lambda"],
        "Sigma": (m["Sigma+"] + m["Sigma0"] + m["Sigma-"]) / 3, "Xi": (m["Xi0"] + m["Xi-"]) / 2,
        "Delta": m["Delta"], "Sigma*": (m["Sigma*+"] + m["Sigma*0"] + m["Sigma*-"]) / 3,
        "Xi*": (m["Xi*0"] + m["Xi*-"]) / 2, "Omega": m["Omega-"],
    }
    c8 = (2 * iso["N"] + iso["Lambda"] + 3 * iso["Sigma"] + 2 * iso["Xi"]) / 8
    c10 = (4 * iso["Delta"] + 3 * iso["Sigma*"] + 2 * iso["Xi*"] + iso["Omega"]) / 10
    return m, iso, c8, c10, src


# ----------------------------------------------------------------------------- fits
def fit_su2(MN, MD, mhat, l1):
    """ANW: MN = M + 3/(8 I1), MD = M + 15/(8 I1); M = mhat F/e, I1 = l1/(e^3 F)."""
    invI1 = 2.0 * (MD - MN) / 3.0
    M = MN - 3.0 * invI1 / 8.0
    k = M / mhat              # F/e
    j = l1 * invI1            # e^3 F
    e = (j / k) ** 0.25
    return {"e": e, "F_pi": k * e, "M_cl": M, "invI1": invI1}


def fit_su3(E8, E10, mhat, l1, l2):
    invI1 = 2.0 * (E10 - E8) / 3.0
    invI2 = invI1 * l1 / l2
    M = E8 - 3.0 * invI1 / 8.0 - 3.0 * invI2 / 4.0
    k = M / mhat
    j = l1 * invI1
    e = (j / k) ** 0.25
    return {"e": e, "F_pi": k * e, "M_cl": M, "invI1": invI1, "invI2": invI2}


def E_su3(M, invI1, invI2, p, q, J, Nc=3):
    JJ = float(J * (J + 1))
    return M + float(C2(p, q)) * invI2 / 2 + (invI1 / 2 - invI2 / 2) * JJ - Nc ** 2 * invI2 / 24


def allowed(Nc, pqmax):
    """All (p,q) with p+q <= pqmax containing Y = Nc/3, with the spins J (isospins at that Y)."""
    out = []
    for p in range(pqmax + 1):
        for q in range(pqmax + 1 - p):
            Js = sorted({I for (Y, I) in gt_content(p, q) if Y == Fr(Nc, 3)})
            if Js:
                out.append(((p, q), Js))
    return out


# ----------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    with open(os.path.join(OUT, "hedgehog.json")) as f:
        hh = json.load(f)["reference_halfline_N160"]
    mhat, l1, l2 = hh["M_over_Fpi_e"], hh["I1_coef"], hh["I2_coef"]
    ok = True
    checks = {}

    def chk(name, cond, detail=""):
        nonlocal ok
        ok &= bool(cond)
        checks[name] = bool(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

    print("E2 SU(3) rotor. Hedgehog inputs: M = %.6f F/e, I1 = %.6f/(e^3F), I2 = %.6f/(e^3F)\n" % (mhat, l1, l2))

    # --- explicit irreps: Casimir, GT content
    print("explicit irreps (tensor construction):")
    irr = {}
    for pq in [(1, 0), (0, 1), (1, 1), (3, 0), (0, 3), (2, 2), (4, 1), (1, 4), (2, 0), (0, 2), (2, 1), (1, 2), (3, 3)]:
        R = build_irrep(*pq)
        irr[pq] = R
        T = R["T"]
        Cas = sum(Ta @ Ta for Ta in T)
        cas_ok = np.max(np.abs(Cas - float(C2(*pq)) * np.eye(R["d"]))) < 1e-9
        comm_ok = True
        for a in range(8):
            for b in range(8):
                lhs = T[a] @ T[b] - T[b] @ T[a]
                rhs = 1j * sum(fabc[a, b, c] * T[c] for c in range(8))
                comm_ok &= np.max(np.abs(lhs - rhs)) < 1e-9
        content = sorted({(lb[0], lb[1]) for lb in R["labels"]})
        gt_ok = content == sorted(set(gt_content(*pq)))
        print(f"  {irrep_name(*pq):6s} d={R['d']:3d} C2={str(C2(*pq)):5s} Casimir ok={cas_ok} [T,T]=ifT ok={comm_ok} "
              f"GT content ok={gt_ok}")
        ok &= cas_ok and comm_ok and gt_ok
    checks["irreps_casimir_commutators_GT"] = bool(ok)

    # --- rotor Hamiltonian from explicit generators vs closed formula (right action on Y_R = 1 states)
    print("\nrotor Hamiltonian from explicit generators on the Y_R = Nc/3 = 1 states (I1, I2 at ANW-like values):")
    i1, i2 = 1 / 195.0, 1 / 513.0
    rot_ok = True
    for pq in [(1, 1), (3, 0), (0, 3), (2, 2), (4, 1), (1, 4), (3, 3)]:
        R = irr[pq]
        T = R["T"]
        H = sum(T[a] @ T[a] for a in range(3)) / (2 * i1) + sum(T[a] @ T[a] for a in range(3, 7)) / (2 * i2)
        for (Y, I, I3), k in R["index"].items():
            if Y == 1:
                val = H[k, k].real
                # H = C2/2I2 + (1/2I1 - 1/2I2) I^2 - T8^2/2I2 with T8^2 = (3/4) Y^2 = 3/4 at Y = 1
                form = float(C2(*pq)) / (2 * i2) + (1 / (2 * i1) - 1 / (2 * i2)) * float(I * (I + 1)) - (3.0 / 4.0) * 1.0 / (2 * i2)
                rot_ok &= abs(val - form) < 1e-8 * abs(form)
                offd = np.max(np.abs(np.delete(H[k], k)))
                rot_ok &= offd < 1e-11 * abs(form)
        print(f"  {irrep_name(*pq):6s}: H on Y=1 states diagonal and equal to C2/2I2 + (1/2I1-1/2I2)J(J+1) - (3/4)Y^2/2I2 : {rot_ok}")
    chk("rotor_H_explicit_equals_formula", rot_ok)

    # --- N_c parity rule
    print("\nWess-Zumino constraint Y_R = Nc/3: allowed irreps and spins (lowest by rotor energy, I1/I2 = %.4f)" % (l1 / l2))
    nc_table = {}
    parity_ok = True
    for Nc in range(1, 8):
        al = allowed(Nc, 16)
        states = []
        for (p, q), Js in al:
            for J in Js:
                e_rot = float(C2(p, q) - J * (J + 1) - Fr(Nc * Nc, 12)) + float(J * (J + 1)) * (l2 / l1)
                states.append((e_rot, (p, q), J))       # in units of 1/(2 I2)
                parity_ok &= ((2 * J) % 2 == Nc % 2)
        states.sort()
        # triality check
        tri_ok = all(((p + 2 * q) - Nc) % 3 == 0 for (p, q), _ in al)
        parity_ok &= tri_ok
        low = states[:6]
        nc_table[Nc] = {
            "lowest_states": [{"irrep": irrep_name(*pq), "pq": list(pq), "J": str(J), "E_rot_2I2": e} for e, pq, J in low],
            "all_J_half_integer": all((2 * J) % 2 == 1 for _, _, J in states),
            "all_J_integer": all((2 * J) % 2 == 0 for _, _, J in states),
            "n_irreps_checked": len(al),
        }
        desc = ", ".join(f"{irrep_name(*pq)}(J={J})" for _, pq, J in low)
        kind = "fermions (all J half-integer)" if nc_table[Nc]["all_J_half_integer"] else (
            "bosons (all J integer)" if nc_table[Nc]["all_J_integer"] else "MIXED")
        print(f"  Nc={Nc}: {kind:30s} lowest: {desc}")
    # wider sweep of the rule
    sweep_ok = True
    for Nc in range(1, 16):
        for (p, q), Js in allowed(Nc, 30):
            for J in Js:
                sweep_ok &= ((2 * J) % 2 == Nc % 2)
    chk("J half-integer iff Nc odd (Nc=1..7, p+q<=16; sweep Nc<=15, p+q<=30)", parity_ok and sweep_ok)

    # --- exact level differences for Nc = 3
    def coef(p, q, J):
        # E - M = a/I1 + b/I2 with exact rationals
        JJ = J * (J + 1)
        return (JJ / 2, C2(p, q) / 2 - JJ / 2 - Fr(9, 24))
    a8, b8 = coef(1, 1, Fr(1, 2)); a10, b10 = coef(3, 0, Fr(3, 2)); ab, bb = coef(0, 3, Fr(1, 2))
    print(f"\nexact: E(8)-M = {a8}/I1 + {b8}/I2;  E(10)-E(8) = {a10-a8}/I1 + {b10-b8}/I2;  "
          f"E(10bar)-E(8) = {ab-a8}/I1 + {bb-b8}/I2")
    chk("E(10)-E(8) = 3/(2 I1) exactly", (a10 - a8, b10 - b8) == (Fr(3, 2), 0))
    chk("E(10bar)-E(8) = 3/(2 I2) exactly", (ab - a8, bb - b8) == (0, Fr(3, 2)))
    chk("E(8) - E_SU2(N) = 3/(4 I2) exactly", (a8, b8) == (Fr(3, 8), Fr(3, 4)))

    # --- PDG and fits
    m, iso, c8, c10, src = pdg_masses()
    print(f"\nPDG ({src}) isospin-averaged masses [MeV]:")
    print("  " + ", ".join(f"{k} {v:.3f}" for k, v in iso.items()))
    print(f"  octet centre (2N+L+3S+2X)/8 = {c8:.3f};  decuplet centre (4D+3S*+2X*+O)/10 = {c10:.3f}  [{m.get('_Delta_note','')}]")

    sets = {}
    su2 = fit_su2(939.0, 1232.0, mhat, l1)
    su2["invI2"] = su2["invI1"] * l1 / l2
    sets["ANW_SU2_fit"] = su2
    su3 = fit_su3(c8, c10, mhat, l1, l2)
    sets["SU3_refit_PDG_centres"] = su3
    gA_coef = hh["gA_times_e2"]
    spectra = {}
    for name, ps in sets.items():
        M, iI1, iI2 = ps["M_cl"], ps["invI1"], ps["invI2"]
        ps["gA_SU2"] = gA_coef / ps["e"] ** 2
        ps["I1_fm"] = 197.3269804 / iI1
        ps["I2_fm"] = 197.3269804 / iI2
        ps["E_N_SU2"] = M + 3 * iI1 / 8
        ps["E_Delta_SU2"] = M + 15 * iI1 / 8
        lev = []
        for (pq, Js) in allowed(3, 6):
            for J in Js:
                lev.append((E_su3(M, iI1, iI2, *pq, J), irrep_name(*pq), str(J), pq))
        lev.sort()
        spectra[name] = [{"irrep": n_, "J": J_, "pq": list(pq), "E_MeV": E} for E, n_, J_, pq in lev[:12]]
        E8 = E_su3(M, iI1, iI2, 1, 1, Fr(1, 2)); E10 = E_su3(M, iI1, iI2, 3, 0, Fr(3, 2)); E10b = E_su3(M, iI1, iI2, 0, 3, Fr(1, 2))
        ps.update({"E8": E8, "E10": E10, "E10bar": E10b, "E10_minus_E8": E10 - E8, "E10bar_minus_E8": E10b - E8,
                   "E8_minus_EN_SU2": E8 - ps["E_N_SU2"], "lowest_irreps_order": [x[1] + "(J=" + x[2] + ")" for x in lev[:6]]})
        print(f"\n{name}: F_pi = {ps['F_pi']:.3f} MeV, e = {ps['e']:.4f}, M_cl = {M:.2f} MeV, 1/I1 = {iI1:.2f} MeV, "
              f"1/I2 = {iI2:.2f} MeV, g_A(SU2 formula) = {ps['gA_SU2']:.4f}")
        print(f"   SU(2): N {ps['E_N_SU2']:.1f}, Delta {ps['E_Delta_SU2']:.1f};  SU(3): E8 {E8:.1f}, E10 {E10:.1f}, "
              f"E10bar {E10b:.1f};  E10-E8 = {E10-E8:.1f}, E10bar-E8 = {E10b-E8:.1f}, E8-E_N(SU2) = {E8-ps['E_N_SU2']:.1f}")
        print("   lowest allowed levels: " + "; ".join(f"{n_}(J={J_}) {E:.0f}" for E, n_, J_, pq in lev[:9]))

    # --- one mass per multiplet with exact SU(3): H acts on the right index only
    deg_ok = True
    for pq in [(1, 1), (3, 0), (0, 3)]:
        R = irr[pq]
        T = R["T"]
        H = sum(T[a] @ T[a] for a in range(3)) / 2 * su3["invI1"] + sum(T[a] @ T[a] for a in range(3, 7)) / 2 * su3["invI2"]
        # full rotor Hilbert space block for irrep R: left (flavour) index untouched -> H_tot = 1_flavour (x) H_right
        Ht = np.kron(np.eye(R["d"]), H)
        Jr = [k for (Y, I, I3), k in R["index"].items() if Y == 1]
        sub = np.ix_([a * R["d"] + j for a in range(R["d"]) for j in Jr], [a * R["d"] + j for a in range(R["d"]) for j in Jr])
        ev = np.linalg.eigvalsh(Ht[sub])
        deg_ok &= (ev.max() - ev.min()) < 1e-9 * abs(ev.max())
    chk("exact SU(3): all d_R x (2J+1) states of 8, 10, 10bar degenerate", deg_ok)

    # --- D-function matrix elements (needed for g_A in SU(3) and the optional symmetry breaking)
    print("\nD^(8) matrix elements from explicit Clebsch-Gordan intertwiners:")
    R8, R10, R10b, R27, R35, R35b = irr[(1, 1)], irr[(3, 0)], irr[(0, 3)], irr[(2, 2)], irr[(4, 1)], irr[(1, 4)]
    h = Fr(1, 2)
    st8 = {"N": (Fr(1), h, h), "Lambda": (Fr(0), Fr(0), Fr(0)), "Sigma": (Fr(0), Fr(1), Fr(1)), "Xi": (Fr(-1), h, h)}
    st10 = {"Delta": (Fr(1), Fr(3, 2), Fr(3, 2)), "Sigma*": (Fr(0), Fr(1), Fr(1)), "Xi*": (Fr(-1), h, h), "Omega": (Fr(-2), Fr(0), Fr(0))}
    st10b = {"Theta+": (Fr(2), Fr(0), Fr(0)), "N*": (Fr(1), h, h), "Sigma_10bar": (Fr(0), Fr(1), Fr(1)), "Xi_3/2": (Fr(-1), Fr(3, 2), Fr(3, 2))}
    right8 = (Fr(1), h, -h)          # Y' = 1, J = 1/2, J3 = -S3 for S3 = +1/2
    right10 = (Fr(1), Fr(3, 2), Fr(-3, 2))
    delta = {}
    for nmR, R, sts, rt in [("8", R8, st8, right8), ("10", R10, st10, right10), ("10bar", R10b, st10b, right8)]:
        for b, lb in sts.items():
            v, mult = Dme(R, R, lb, rt)
            v2, _ = Dme(R, R, lb, (rt[0], rt[1], -rt[2]))
            delta[b] = (v.real, mult, abs(v - v2))
    lit_delta = {"N": Fr(3, 10), "Lambda": Fr(1, 10), "Sigma": Fr(-1, 10), "Xi": Fr(-2, 10),
                 "Delta": Fr(1, 8), "Sigma*": Fr(0), "Xi*": Fr(-1, 8), "Omega": Fr(-2, 8),
                 "Theta+": Fr(2, 8), "N*": Fr(1, 8), "Sigma_10bar": Fr(0), "Xi_3/2": Fr(-1, 8)}
    dl_ok = True
    for b, (v, mult, dj) in delta.items():
        dl_ok &= abs(v - float(lit_delta[b])) < 1e-10 and dj < 1e-12
        print(f"  <{b:11s}|D88|{b:11s}> = {v:+.12f}  (Praszalowicz eqs.17-19: {str(lit_delta[b]):5s}; multiplicity {mult}; J3-independent)")
    chk("diagonal D88 elements reproduce Praszalowicz (17)-(19)", dl_ok)
    # second-order (delta^{R'}_B)^2
    lit2 = {("N", "10bar"): Fr(1, 20), ("N", "27"): Fr(6, 100), ("Sigma", "10bar"): Fr(1, 20), ("Sigma", "27"): Fr(4, 100),
            ("Lambda", "10bar"): Fr(0), ("Lambda", "27"): Fr(9, 100), ("Xi", "10bar"): Fr(0), ("Xi", "27"): Fr(6, 100),
            ("Delta", "27"): Fr(15, 128), ("Delta", "35"): Fr(25, 896), ("Sigma*", "27"): Fr(8, 128), ("Sigma*", "35"): Fr(40, 896),
            ("Xi*", "27"): Fr(3, 128), ("Xi*", "35"): Fr(45, 896), ("Omega", "27"): Fr(0), ("Omega", "35"): Fr(40, 896),
            ("Theta+", "8"): Fr(0), ("Theta+", "27"): Fr(0), ("Theta+", "35bar"): Fr(72, 896),
            ("N*", "8"): Fr(1, 20), ("N*", "27"): Fr(3, 640), ("N*", "35bar"): Fr(81, 896),
            ("Sigma_10bar", "8"): Fr(1, 20), ("Sigma_10bar", "27"): Fr(8, 640), ("Sigma_10bar", "35bar"): Fr(72, 896),
            ("Xi_3/2", "8"): Fr(0), ("Xi_3/2", "27"): Fr(15, 640), ("Xi_3/2", "35bar"): Fr(45, 896)}
    Rmap = {"8": R8, "10": R10, "10bar": R10b, "27": R27, "35": R35, "35bar": R35b}
    home = {**{b: ("8", right8) for b in st8}, **{b: ("10", right10) for b in st10}, **{b: ("10bar", right8) for b in st10b}}
    allst = {**st8, **st10, **st10b}
    d2 = {}
    d2_ok = True
    for (b, Rp), lit in lit2.items():
        hR, rt = home[b]
        lb = allst[b]
        if lb not in Rmap[Rp]["index"] or rt not in Rmap[Rp]["index"]:
            val = 0.0
        else:
            v, _ = Dme(Rmap[hR], Rmap[Rp], lb, rt)
            val = abs(v) ** 2
        d2[f"{b}|{Rp}"] = val
        d2_ok &= abs(val - float(lit)) < 1e-10
    print("  second-order (delta^{R'}_B)^2: " + ", ".join(f"{k}={v:.6f}" for k, v in list(d2.items())[:8]) + ", ...")
    chk("all 28 (delta^R'_B)^2 reproduce Praszalowicz (17)-(19)", d2_ok)

    # g_A: <p up|D_33|p up> in SU(2) and SU(3)
    tau_adj = np.array([[[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], [[0, 0, 1j], [0, 0, 0], [-1j, 0, 0]], [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]])
    s_half = {"d": 2, "T": np.array([[[0, 0.5], [0.5, 0]], [[0, -0.5j], [0.5j, 0]], [[0.5, 0], [0, -0.5]]], complex),
              "index": {(Fr(1), h, h): 0, (Fr(1), h, -h): 1}}
    D33_su2, _ = Dme(s_half, s_half, (Fr(1), h, h), (Fr(1), h, -h), a=2, b=2, adj=tau_adj)
    D33_su3, _ = Dme(R8, R8, (Fr(1), h, h), right8, a=2, b=2)
    print(f"  <p up|D_33|p up>: SU(2) {D33_su2.real:+.12f} (ANW -1/3),  SU(3) octet {D33_su3.real:+.12f} (-7/30 = {-7/30:+.6f})")
    chk("<p|D33|p> = -1/3 (SU2) and -7/30 (SU3, Schechter-Weigel 7/10 factor)",
        abs(D33_su2.real + 1 / 3) < 1e-10 and abs(D33_su3.real + 7 / 30) < 1e-10)
    for ps in sets.values():
        ps["gA_SU3_symmetric"] = 0.7 * ps["gA_SU2"]

    # --- OPTIONAL: first-order symmetry breaking H' = -alpha D88 + beta Y (Guadagnini's form)
    print("\nOPTIONAL (two extra fitted inputs alpha, beta): first-order H' = -alpha D88 + beta Y")
    obs = ["N", "Lambda", "Sigma", "Xi", "Delta", "Sigma*", "Xi*", "Omega"]
    Yv = {"N": 1, "Lambda": 0, "Sigma": 0, "Xi": -1, "Delta": 1, "Sigma*": 0, "Xi*": -1, "Omega": -2}
    mult = {"N": 2, "Lambda": 1, "Sigma": 3, "Xi": 2, "Delta": 4, "Sigma*": 3, "Xi*": 2, "Omega": 1}
    cen = {b: (c8 if b in st8 else c10) for b in obs}
    # centres unchanged at first order: multiplicity-weighted sums vanish
    s8 = sum(mult[b] * delta[b][0] for b in st8); s10 = sum(mult[b] * delta[b][0] for b in st10)
    chk("first-order shifts average to zero over each multiplet (centres = rotor energies)", abs(s8) < 1e-12 and abs(s10) < 1e-12)
    A = np.array([[-delta[b][0], Yv[b]] for b in obs])
    y = np.array([iso[b] - cen[b] for b in obs])
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    alpha, beta = sol
    pred = {b: cen[b] + A[i] @ sol for i, b in enumerate(obs)}
    rms = float(np.sqrt(np.mean([(pred[b] - iso[b]) ** 2 for b in obs])))
    print(f"  fitted inputs: alpha = {alpha:.1f} MeV, beta = {beta:.1f} MeV (least squares on 8 isospin multiplets, centres fixed)")
    for b in obs:
        print(f"   {b:7s} PDG {iso[b]:8.2f}  fit {pred[b]:8.2f}  diff {pred[b]-iso[b]:+6.2f}")
    print(f"  rms deviation {rms:.1f} MeV")
    # sum rules: exact coefficients with the computed delta's
    dfr = {b: Fr(delta[b][0]).limit_denominator(1000) for b in obs}
    def rule_coeffs(c):
        return sum(c[b] * dfr[b] for b in c), sum(c[b] * Yv[b] for b in c)
    gu = {"N": 8, "Xi*": 8, "Sigma": 3, "Lambda": -11, "Sigma*": -8}
    gmo = {"N": 2, "Xi": 2, "Lambda": -3, "Sigma": -1}
    es1 = {"Sigma*": 2, "Delta": -1, "Xi*": -1}
    es2 = {"Xi*": 2, "Sigma*": -1, "Omega": -1}
    rules = {}
    for nm_, c, cen_c in [("Guadagnini 8(N+Xi*)+3Sigma-11Lambda-8Sigma*", gu, 8 * c8 + 8 * c10 + 3 * c8 - 11 * c8 - 8 * c10),
                          ("GMO 2(N+Xi)-3Lambda-Sigma", gmo, 0.0),
                          ("equal spacing 2Sigma*-Delta-Xi*", es1, 0.0), ("equal spacing 2Xi*-Sigma*-Omega", es2, 0.0)]:
        cd, cy = rule_coeffs(c)
        val = sum(c[b] * iso[b] for b in c)
        scale = sum(abs(c[b]) * iso[b] for b in c) / 2
        rules[nm_] = {"coeff_D88": str(cd), "coeff_Y": str(cy), "PDG_value_MeV": val, "relative": val / scale}
        print(f"  {nm_:45s}: model coefficients (D88, Y) = ({cd}, {cy});  PDG LHS-RHS = {val:+.2f} MeV ({val/scale*100:+.3f}%)")
    chk("Guadagnini, GMO, equal spacing hold identically for -alpha D88 + beta Y",
        all(r["coeff_D88"] == "0" and r["coeff_Y"] == "0" for r in rules.values()))

    out = {
        "inputs_from_hedgehog": {"M_over_Fpi_e": mhat, "I1_coef": l1, "I2_coef": l2, "gA_times_e2": gA_coef},
        "pdg": {"source": src, "raw_MeV": {k: v for k, v in m.items()}, "isospin_averaged_MeV": iso,
                "octet_centre_MeV": c8, "decuplet_centre_MeV": c10},
        "parameter_sets": sets, "spectra": spectra,
        "Nc_table": nc_table,
        "exact_level_differences": {"E8_minus_M": f"{a8}/I1 + {b8}/I2", "E10_minus_E8": f"{a10-a8}/I1 + {b10-b8}/I2",
                                    "E10bar_minus_E8": f"{ab-a8}/I1 + {bb-b8}/I2"},
        "D88_diagonal": {b: v[0] for b, v in delta.items()},
        "D88_second_order_sq": d2,
        "D33_p_up": {"SU2": D33_su2.real, "SU3_octet": D33_su3.real},
        "optional_symmetry_breaking": {"form": "H' = -alpha D^(8)_88 + beta Y, first order, centres fixed to PDG centres",
                                       "alpha_MeV": alpha, "beta_MeV": beta, "fit_MeV": pred, "rms_MeV": rms,
                                       "sum_rules": rules},
        "checks": checks, "all_checks_pass": bool(ok), "runtime_s": time.time() - t0,
    }
    with open(os.path.join(OUT, "rotor.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(f"\nall checks pass: {ok};  runtime {time.time()-t0:.1f} s")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
