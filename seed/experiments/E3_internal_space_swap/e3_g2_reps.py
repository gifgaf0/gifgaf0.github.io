#!/usr/bin/env python3
"""
E3 part 4: G2 irreps, Casimirs, branching to SU(2)_long x SU(2)_short, and the rotor
spectrum of the B = 1 G2 fold (no Wess-Zumino term).

Weights are written in the coordinates (m_L, m_S) = eigenvalues of (i T3^L, i T3^S) on the
Cartan subalgebra span(T3^L, T3^S) (e3_g2_algebra.py).  Inner product dual to B = -Tr_7:
(l, l') = mL mL' + mS mS'/3, so long roots have length^2 1, short roots 1/3 and the long-root
su(2) Casimir is J(J+1).  Simple roots a1 = (-1/2, 1/2) (short), a2 = (1, 0) (long);
fundamental weights w1 = (0, 1) (the 7), w2 = (1/2, 3/2) (the 14).
C2(lambda) = (lambda, lambda + 2 rho).
Multiplicities: Freudenthal's formula in exact rational arithmetic.
Branching: n(jL, jS) = m(jL,jS) - m(jL+1,jS) - m(jL,jS+1) + m(jL+1,jS+1).
Rotor: states = (R, J) with right-acting SU(2)_short singlet, spin J from right SU(2)_long:
  E = M + J(J+1)/(2 I1) + [C2(R) - J(J+1)] / (2 I2).
Cross-check: explicit tensor-product representations built from the 7x7 generators
(Sym^2 7, Lambda^2 7, 7 x 14, Sym^2 14, Lambda^2 14) decomposed numerically.
Writes reps_results.json.
"""
import json
from fractions import Fraction as Fr
from itertools import product
import numpy as np

half = Fr(1, 2)
POS = [(Fr(1), Fr(0)), (-half, half), (half, half), (Fr(0), Fr(1)), (-half, Fr(3, 2)), (half, Fr(3, 2))]
A1, A2 = (-half, half), (Fr(1), Fr(0))
W1, W2 = (Fr(0), Fr(1)), (half, Fr(3, 2))
RHO = (W1[0] + W2[0], W1[1] + W2[1])


def ip(a, b):
    return a[0] * b[0] + a[1] * b[1] / 3


def add(a, b, k=1):
    return (a[0] + k * b[0], a[1] + k * b[1])


def hw(a, b):
    return (a * W1[0] + b * W2[0], a * W1[1] + b * W2[1])


def weyl_dim(lam):
    num = den = Fr(1)
    for al in POS:
        num *= ip(add(lam, RHO), al)
        den *= ip(RHO, al)
    return num / den


def reflect(mu, al):
    c = 2 * ip(mu, al) / ip(al, al)
    return add(mu, al, -c)


def dominant(mu):
    changed = True
    while changed:
        changed = False
        for al in (A1, A2):
            if ip(mu, al) < 0:
                mu = reflect(mu, al)
                changed = True
    return mu


def coeffs(v):
    """v = n1 a1 + n2 a2  ->  (n1, n2)"""
    n1 = 2 * v[1]                 # a1 has mS = 1/2, a2 has mS = 0
    n2 = v[0] + n1 / 2
    return n1, n2


def freudenthal(a, b):
    lam = hw(a, b)
    N1, N2 = coeffs((2 * lam[0], 2 * lam[1]))        # lambda - (-lambda)
    lr2 = ip(add(lam, RHO), add(lam, RHO))
    mult = {lam: 1}
    order = sorted(((n1, n2) for n1 in range(int(N1) + 1) for n2 in range(int(N2) + 1)), key=lambda t: t[0] + t[1])
    for n1, n2 in order:
        if n1 == 0 and n2 == 0:
            continue
        mu = add(add(lam, A1, -n1), A2, -n2)
        md = dominant(mu)
        d1, d2 = coeffs(add(lam, md, -1))
        if d1 < 0 or d2 < 0 or d1.denominator != 1 or d2.denominator != 1:
            continue                                     # outside the weight polytope
        s = Fr(0)
        for al in POS:
            k = 1
            while True:
                nu = add(mu, al, k)
                e1, e2 = coeffs(add(lam, nu, -1))
                if e1 < 0 or e2 < 0:          # nu is no longer below lambda
                    break
                s += ip(nu, al) * mult.get(nu, 0)
                k += 1
        den = lr2 - ip(add(mu, RHO), add(mu, RHO))
        m = 2 * s / den
        assert m.denominator == 1 and m >= 0, (a, b, mu, m)
        if m:
            mult[mu] = int(m)
    return mult


def branching(mult):
    m = lambda jl, js: mult.get((jl, js), 0)
    out = {}
    for (jl, js) in mult:
        if jl >= 0 and js >= 0:
            n = m(jl, js) - m(jl + 1, js) - m(jl, js + 1) + m(jl + 1, js + 1)
            if n:
                out[(jl, js)] = n
    return out


def lab(j):
    return str(int(2 * j + 1))


if __name__ == "__main__":
    res = {}
    # ---------------- irreps up to dimension ~ 300 (plus the next few, for the spectrum)
    irreps = []
    for a in range(0, 9):
        for b in range(0, 6):
            d = weyl_dim(hw(a, b))
            if d <= 500:
                irreps.append((int(d), a, b))
    irreps.sort()
    table = []
    names_seen = {}
    all_integer = True
    for d, a, b in irreps:
        mult = freudenthal(a, b)
        dimsum = sum(mult.values())
        assert dimsum == d, (a, b, dimsum, d)
        # Weyl invariance of multiplicities
        for mu, k in mult.items():
            for al in POS:
                assert mult.get(reflect(mu, al), 0) == k
        lam = hw(a, b)
        C2 = ip(lam, add(lam, add(RHO, RHO)))
        br = branching(mult)
        assert sum(n * (2 * jl + 1) * (2 * js + 1) for (jl, js), n in br.items()) == d
        integ = all((jl + js).denominator == 1 for (jl, js) in br)
        all_integer &= integ
        names_seen[d] = names_seen.get(d, 0) + 1
        name = str(d) + ("'" if names_seen[d] > 1 else "")
        allowed = {jl: n for (jl, js), n in br.items() if js == 0}
        table.append(dict(name=name, dim=d, dynkin=[a, b], highest_weight_mLmS=[str(lam[0]), str(lam[1])],
                          C2=str(C2), C2_float=float(C2),
                          branching={f"({lab(jl)},{lab(js)})": n for (jl, js), n in sorted(br.items())},
                          jL_plus_jS_always_integer=integ,
                          allowed_J={str(jl): n for jl, n in sorted(allowed.items())}))
    res["irreps"] = table
    res["all_irreps_jL_plus_jS_integer"] = all_integer
    print(f"{'R':>5} {'[a,b]':>6} {'C2':>6}   branching under SU(2)_L x SU(2)_S          allowed J (mult)")
    for t in table:
        if t["dim"] <= 300:
            print(f"{t['name']:>5} {str(t['dynkin']):>6} {t['C2']:>6}   {' + '.join(f'{v}{k}' if v > 1 else k for k, v in t['branching'].items())[:70]:<70} {t['allowed_J']}")
    print("every component of every irrep has jL + jS integer:", all_integer)

    # ---------------- explicit tensor-product cross-check
    alg = np.load("g2_basis.npz")
    basis, TL, TS = alg["basis"], alg["TL"], alg["TS"]
    G = list(basis)
    adT = lambda T: np.array([[-np.trace((T @ b_ - b_ @ T) @ a_) for b_ in G] for a_ in G])
    I7, I14 = np.eye(7), np.eye(14)

    def sym_proj(n, sign):
        P = np.zeros((n * n, n * n))
        for i in range(n):
            for j in range(n):
                P[i * n + j, i * n + j] += 0.5
                P[j * n + i, i * n + j] += 0.5 * sign
        w, V = np.linalg.eigh(P)
        return V[:, w > 0.5]

    reps = {}
    for nm, (gen, n1, sign) in {"Sym2(7)": ("7", 7, 1), "Lam2(7)": ("7", 7, -1), "Sym2(14)": ("14", 14, 1),
                                 "Lam2(14)": ("14", 14, -1)}.items():
        Q = sym_proj(n1, sign)
        rep = lambda T, gen=gen, n1=n1, Q=Q: Q.T @ (np.kron(T if gen == "7" else adT(T), np.eye(n1)) +
                                                   np.kron(np.eye(n1), T if gen == "7" else adT(T))) @ Q
        reps[nm] = rep
    reps["7x14"] = lambda T: np.kron(T, I14) + np.kron(I7, adT(T))
    numeric = {}
    for nm, rep in reps.items():
        Rg = [rep(g) for g in G]
        C = -sum(r @ r for r in Rg)
        CL = -sum(rep(t) @ rep(t) for t in TL)
        CS = -sum(rep(t) @ rep(t) for t in TS)
        Cs = 0.5 * (C + C.T)
        w, V = np.linalg.eigh(Cs)
        comps = {}
        for c in sorted(set(np.round(w, 6))):
            Vc = V[:, np.abs(w - c) < 1e-5]
            cl = Vc.T @ CL @ Vc
            cs = Vc.T @ CS @ Vc
            M = 0.5 * (cl + cl.T) + np.sqrt(2) * 0.5 * (cs + cs.T)
            ww, U = np.linalg.eigh(M)
            jl = np.einsum('ia,ij,ja->a', U, Vc.T @ CL @ Vc, U)
            js = np.einsum('ia,ij,ja->a', U, Vc.T @ CS @ Vc, U)
            J = lambda x: Fr(int(round((-1 + np.sqrt(1 + 4 * max(x, 0))))), 2)
            cnt = {}
            for x, y in zip(jl, js):
                k = (J(x), J(y)); cnt[k] = cnt.get(k, 0) + 1
            br = {f"({lab(k[0])},{lab(k[1])})": v // int((2 * k[0] + 1) * (2 * k[1] + 1)) for k, v in sorted(cnt.items())}
            comps[f"C2={c:g} (dim {Vc.shape[1]})"] = br
        numeric[nm] = comps
        print(nm, comps)
    res["tensor_product_numeric"] = numeric
    # compare with Freudenthal: match by (dim, C2)
    by_dc = {(t["dim"], round(t["C2_float"], 6)): t for t in table}
    mism = []
    nmatch = 0
    for nm, comps in numeric.items():
        for key, br in comps.items():
            c = float(key.split("=")[1].split(" ")[0]); d = int(key.split("dim ")[1].rstrip(")"))
            # an eigenspace may hold several copies of one irrep
            cands = [t for (dd, cc), t in by_dc.items() if abs(cc - c) < 1e-5 and d % dd == 0]
            ok = False
            for t in cands:
                k = d // t["dim"]
                if {kk: v * k for kk, v in t["branching"].items()} == br:
                    ok = True; nmatch += 1
            if not ok:
                mism.append((nm, key, br))
    res["tensor_product_vs_freudenthal_mismatches"] = mism
    res["tensor_product_vs_freudenthal_matches"] = nmatch
    print("tensor-product components matched to Freudenthal branching:", nmatch, " mismatches:", mism)

    # ---------------- rotor spectrum
    hh = json.load(open("hedgehog_results.json"))["final"]
    ine = json.load(open("inertia_results.json"))
    m_cl, i1, i2 = hh["M"], ine["I1_3d"], ine["I2_3d"]
    states = []
    for t in table:
        for J, n in t["allowed_J"].items():
            J = float(Fr(J))
            states.append(dict(R=t["name"], dim=t["dim"], C2=t["C2_float"], J=J, copies=n,
                               E_over_inv_I1=J * (J + 1) / 2 + (i1 / i2) * (t["C2_float"] - J * (J + 1)) / 2))
    states.sort(key=lambda s: s["E_over_inv_I1"])
    res["inputs"] = dict(M_cl_F_over_e=m_cl, I1_e3F=i1, I2_e3F=i2, I1_over_I2=i1 / i2)

    def physical(Fpi, e):
        u = e**3 * Fpi
        return dict(F_pi=Fpi, e=e, M=m_cl * Fpi / e, inv_I1=u / i1, inv_I2=u / i2)

    # SU(3) refit (inputs: octet and decuplet centres; SU(3) rotor with N_c = 3, Y_R = 1)
    try:
        import warnings
        warnings.filterwarnings("ignore")
        import pdg
        api = pdg.connect()
        mass = lambda nm: api.get_particles_by_name(nm)[0].mass * 1000
        octet = [mass('p'), mass('n'), mass('Lambda'), mass('Sigma+'), mass('Sigma0'), mass('Sigma-'),
                 mass('Xi0'), mass('Xi-')]
        mD = [m_.value for m_ in api.get_particles_by_name('Delta(1232)++')[0].masses()][0]
        dec = [mD] * 4 + [mass('Sigma(1385)+'), mass('Sigma(1385)0'), mass('Sigma(1385)-'),
                          mass('Xi(1530)0'), mass('Xi(1530)-'), mass('Omega-')]
        E8c, E10c = float(np.mean(octet)), float(np.mean(dec))
        src = "PDG 2026 via the pdg package (Delta(1232): mixed-charge 1232.0 MeV)"
    except Exception as ex:   # fall back to the centres quoted in PLAN.md
        E8c, E10c, src = 1151.0, 1382.0, f"PLAN.md values (pdg unavailable: {ex})"
    u = (2.0 / 3.0) * i1 * (E10c - E8c)                     # e^3 F from E(10)-E(8) = 3/(2 I1)
    FoverE = (E8c - 0.375 * u / i1 - 0.75 * u / i2) / m_cl     # E(8) = M + 3/(8 I1) + 3/(4 I2)
    e_fit = (u / FoverE) ** 0.25
    F_fit = FoverE * e_fit
    res["su3_refit"] = dict(octet_centre_MeV=E8c, decuplet_centre_MeV=E10c, source=src, F_pi=F_fit, e=e_fit,
                            antidecuplet_MeV=physical(F_fit, e_fit)["M"] + 0.375 * u / i1 + 2.25 * u / i2,   # E(8) + 3/(2 I2)
                            note="fitted inputs, not predictions")
    print(f"SU(3) refit to octet {E8c:.2f} / decuplet {E10c:.2f} MeV: F_pi = {F_fit:.2f} MeV, e = {e_fit:.4f}")
    points = {"ANW (F_pi=129, e=5.45)": physical(129.0, 5.45), "SU(3) refit": physical(F_fit, e_fit)}
    res["parameter_points"] = points
    for s_ in states:
        for k, p in points.items():
            s_["E_MeV " + k] = p["M"] + s_["J"] * (s_["J"] + 1) / 2 * p["inv_I1"] + (s_["C2"] - s_["J"] * (s_["J"] + 1)) / 2 * p["inv_I2"]
            s_["Exc_MeV " + k] = s_["E_MeV " + k] - p["M"]
    res["states"] = states
    print(f"\nrotor spectrum (I1/I2 = {i1/i2:.5f}); E - M in units of 1/I1 and MeV")
    print(f"{'R':>5} {'C2':>7} {'J':>3} {'copies':>6} {'(E-M) I1':>9} {'E ANW':>8} {'E refit':>8}")
    for s_ in states:
        if s_["dim"] <= 300:
            print(f"{s_['R']:>5} {s_['C2']:7.3f} {s_['J']:3.0f} {s_['copies']:6d} {s_['E_over_inv_I1']:9.4f} "
                  f"{s_['E_MeV ANW (F_pi=129, e=5.45)']:8.1f} {s_['E_MeV SU(3) refit']:8.1f}")
    res["all_allowed_J_integer"] = all(float(s_["J"]).is_integer() for s_ in states)
    res["seven_allowed"] = any(s_["R"] == "7" for s_ in states)
    res["lowest_two"] = [(s_["R"], s_["J"]) for s_ in states[:2]]
    print("all allowed J integer:", res["all_allowed_J_integer"], "| 7 allowed:", res["seven_allowed"],
          "| lowest:", res["lowest_two"])
    with open("reps_results.json", "w") as fh:
        json.dump(res, fh, indent=1, default=str)
