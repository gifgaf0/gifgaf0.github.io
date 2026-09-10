#!/usr/bin/env python3
# G-POLY1 full-precision layer -- CC LEG (independent instrument, written from scratch).
# Formalism: Roy-Kube assembly per the pin record (md5 621120e5...), hexagonal arm by
# exact-degree SO(3) quadrature validated against the pinned cubic closed form.
# Conventions per addendum section C: general VRH chain for C2; Phi_G with the
# symmetry-pinned G_V; scattering reference = general Voigt (lam, mu); rho = 1; a = 1; d = 2a.
# Consumes ONLY the md5-verified embedded input file. All gates hard-halt on miss.
import json, hashlib, math, os, sys, itertools
from datetime import datetime, timezone
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(HERE, "poly_vrh_results.json")
INPUT_MD5 = "200e7a8b775577564369c6924d38a84c"
PIN_MD5 = "621120e50d395beea2e914d54c929600"
PREREG_MD5 = "dab462d2e133d0962c512a34bb7bc635"

FAILURES = []
def gate(name, val, tol):
    ok = abs(val) <= tol
    if not ok:
        FAILURES.append(f"{name}: {val} > {tol}")
    print(f"  gate {name}: {val:.3e} (tol {tol:.0e}) {'PASS' if ok else 'FAIL'}")
    return ok

# ---------------- tensor / Voigt machinery ----------------
VP = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]

def tensor_from_voigt(M6):
    C = np.zeros((3, 3, 3, 3))
    for A, (i, j) in enumerate(VP):
        for B, (k, l) in enumerate(VP):
            v = M6[A, B]
            for a, b in ((i, j), (j, i)):
                for c, d in ((k, l), (l, k)):
                    C[a, b, c, d] = v
    return C

def voigt_hex(c11, c12, c13, c33, c44, c66):
    M = np.zeros((6, 6))
    M[0, 0] = M[1, 1] = c11; M[2, 2] = c33
    M[0, 1] = M[1, 0] = c12
    M[0, 2] = M[2, 0] = M[1, 2] = M[2, 1] = c13
    M[3, 3] = M[4, 4] = c44; M[5, 5] = c66
    return M

def voigt_cubic(c11, c12, c44):
    M = np.zeros((6, 6))
    for i in range(3):
        M[i, i] = c11
        M[i + 3, i + 3] = c44
    for i in range(3):
        for j in range(3):
            if i != j:
                M[i, j] = c12
    return M

def gen_chain(M6):
    """General VRH chain: Voigt from <C>, Reuss from S = C^-1 (6x6), Hill mean."""
    KV = (M6[0, 0] + M6[1, 1] + M6[2, 2] + 2 * (M6[0, 1] + M6[0, 2] + M6[1, 2])) / 9.0
    GV = (M6[0, 0] + M6[1, 1] + M6[2, 2] - M6[0, 1] - M6[0, 2] - M6[1, 2]
          + 3 * (M6[3, 3] + M6[4, 4] + M6[5, 5])) / 15.0
    S = np.linalg.inv(M6)
    KR = 1.0 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
    GR = 15.0 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2])
                 + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    return KV, GV, KR, GR

def hex_pinned(c11, c12, c13, c33, c44, c66):
    """Berryman (22)-(26) + product formulas; plus the 1606-class K_R = Csq/M."""
    KV = (2 * (c11 + c12) + 4 * c13 + c33) / 9.0
    Geffv = (c11 + c33 - 2 * c13 - c66) / 3.0
    GV = (Geffv + 2 * c44 + 2 * c66) / 5.0
    KR = c13 + 1.0 / (1.0 / (c11 - c66 - c13) + 1.0 / (c33 - c13))
    Geffr = KR * Geffv / KV
    GR = 1.0 / ((1.0 / Geffr + 2.0 / c44 + 2.0 / c66) / 5.0)
    Mh = c11 + c12 + 2 * c33 - 4 * c13
    Csq = (c11 + c12) * c33 - 2 * c13 * c13
    KR1606 = Csq / Mh
    prod = c33 * (c11 - c66) - c13 * c13
    chk = (abs(3 * KR * Geffv / prod - 1.0), abs(3 * KV * Geffr / prod - 1.0))
    return dict(KV=KV, GV=GV, KR=KR, GR=GR, Geffv=Geffv, Geffr=Geffr,
                KR1606=KR1606, product_selfchecks=list(chk))

def cubic_closed(c11, c12, c44):
    K = (c11 + 2 * c12) / 3.0
    GV = (c11 - c12 + 3 * c44) / 5.0
    GR = 5.0 * (c11 - c12) * c44 / (4 * c44 + 3 * (c11 - c12))
    return dict(K=K, GV=GV, GR=GR)

# ---------------- SO(3) orientation average (pinned hexagonal arm) ----------------
def euler_zyz(a, b, g):
    ca, sa, cb, sb, cg, sg = math.cos(a), math.sin(a), math.cos(b), math.sin(b), math.cos(g), math.sin(g)
    Rz1 = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
    Rz2 = np.array([[cg, -sg, 0], [sg, cg, 0], [0, 0, 1]])
    return Rz1 @ Ry @ Rz2

def so3_moments(C4, nb=10, na=12):
    """First and second SO(3) moments of the rotated tensor.
    Gauss-Legendre in cos(beta) (nb nodes), uniform alpha/gamma grids (na nodes)."""
    xg, wg = np.polynomial.legendre.leggauss(nb)
    angs = [2.0 * math.pi * j / na for j in range(na)]
    mean = np.zeros((3, 3, 3, 3))
    M2 = np.zeros((81, 81))
    for x, w in zip(xg, wg):
        b = math.acos(x)
        for a in angs:
            for g in angs:
                R = euler_zyz(a, b, g)
                Cr = np.einsum('ia,jb,kc,ld,abcd->ijkl', R, R, R, R, C4, optimize=True)
                wt = (w / 2.0) / (na * na)
                mean += wt * Cr
                v = Cr.reshape(81)
                M2 += wt * np.outer(v, v)
    return mean, M2

def xi_quadrature(C4, nb=10, na=12):
    mean, M2 = so3_moments(C4, nb, na)
    Xi = M2 - np.outer(mean.reshape(81), mean.reshape(81))
    return Xi.reshape((3,) * 8), mean

# ---------------- pinned cubic closed form Xi = a*T_A + b*T_B + c*T_C ----------------
def _delta_tensor(pairs):
    T = np.zeros((3,) * 8)
    for vals in itertools.product(range(3), repeat=4):
        idx = [0] * 8
        for (p, q), v in zip(pairs, vals):
            idx[p] = v; idx[q] = v
        T[tuple(idx)] += 1.0
    return T

_TABC = None
def basis_tabc():
    """T_A / T_B / T_C pairing-class basis per pin (A.3)-(A.4) class descriptions."""
    global _TABC
    if _TABC is not None:
        return _TABC
    lat, grk = [0, 1, 2, 3], [4, 5, 6, 7]
    def pairings2(idx):
        a, b, c, d = idx
        return [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]
    TA = np.zeros((3,) * 8); TB = np.zeros((3,) * 8); TC = np.zeros((3,) * 8)
    for pl in pairings2(lat):
        for pg in pairings2(grk):
            TA += _delta_tensor(list(pl) + list(pg))
    for perm in itertools.permutations(grk):
        TB += _delta_tensor(list(zip(lat, perm)))
    for ll in itertools.combinations(lat, 2):
        rl = [x for x in lat if x not in ll]
        for gg in itertools.combinations(grk, 2):
            rg = [x for x in grk if x not in gg]
            for m in (((rl[0], rg[0]), (rl[1], rg[1])), ((rl[0], rg[1]), (rl[1], rg[0]))):
                TC += _delta_tensor([ll, gg] + list(m))
    _TABC = (TA, TB, TC)
    return _TABC

def fit_xi_in_basis(Xi):
    """Machine-derive the (a, b, c) expansion of Xi in the T_A/T_B/T_C basis.
    The pinned b/c digit strings were corrupted in transport and are NOT
    consumed (pin E3); the clean A-string and the A-anchor gate the machinery."""
    TA, TB, TC = basis_tabc()
    B = np.stack([TA.reshape(-1), TB.reshape(-1), TC.reshape(-1)], axis=1)
    coef, _, _, _ = np.linalg.lstsq(B, Xi.reshape(-1), rcond=None)
    resid = Xi - (coef[0] * TA + coef[1] * TB + coef[2] * TC)
    return coef, float(np.max(np.abs(resid)) / np.max(np.abs(Xi)))

# ---------------- contraction machinery (pinned slot assignment) ----------------
def phi_pm(Xi8, mode_p, mode_m, mu):
    p = np.array([0.0, 0.0, 1.0])
    s = np.array([math.sqrt(max(0.0, 1.0 - mu * mu)), 0.0, mu])
    I = np.eye(3)
    Pol = np.outer(p, p) if mode_p == 'L' else 0.5 * (I - np.outer(p, p))
    Dy = np.outer(s, s) if mode_m == 'L' else (I - np.outer(s, s))
    return float(np.einsum('ijklmnop,im,jn,ko,lp->', Xi8, Pol, np.outer(p, p),
                           Dy, np.outer(s, s), optimize=True))

def int_phi(Xi8, mode_p, mode_m, n=24):
    xg, wg = np.polynomial.legendre.leggauss(n)
    return sum(w * phi_pm(Xi8, mode_p, mode_m, x) for x, w in zip(xg, wg))

def alpha_finite(Xi8, VT, VL, kTa, n=48):
    """Finite-spectrum Born attenuation for a transverse incident wave, a = 1.
    alpha_T = sum_M [kT*kM^3/(2 VT^2 VM^2)] Int Phi_TM(mu)/(1+q^2)^2 dmu,
    q^2 = kT^2 + kM^2 - 2 kT kM mu (spectrum eta(q) = a^3/(pi^2 (1+q^2 a^2)^2),
    the pi^2 a^3 cancelling against the Rayleigh normalization)."""
    xg, wg = np.polynomial.legendre.leggauss(n)
    out = 0.0
    for mode_m, VM in (('T', VT), ('L', VL)):
        kM = kTa * VT / VM
        s = 0.0
        for x, w in zip(xg, wg):
            q2 = kTa * kTa + kM * kM - 2.0 * kTa * kM * x
            s += w * phi_pm(Xi8, 'T', mode_m, x) / (1.0 + q2) ** 2
        out += kTa * kM ** 3 / (2.0 * VT * VT * VM * VM) * s
    return out

def iso_tensor(lam, mu):
    I = np.eye(3)
    return (lam * np.einsum('ij,kl->ijkl', I, I)
            + mu * (np.einsum('ik,jl->ijkl', I, I) + np.einsum('il,jk->ijkl', I, I)))

def fro2(C4):
    return float(np.sum(C4 * C4))

# ---------------- per-config phase 1 (a + b) ----------------
def run_phase1(name, sym, M6, pinned, extra_nu=None):
    C4 = tensor_from_voigt(M6)
    KVg, GVg, KRg, GRg = gen_chain(M6)
    Xi, meanC = xi_quadrature(C4)
    Xi2, _ = xi_quadrature(C4, nb=20, na=24)
    lam = KVg - 2.0 * GVg / 3.0
    mu = GVg
    iso = iso_tensor(lam, mu)
    Vtot = float(np.einsum('ijklijkl->', Xi))
    Vtot2 = float(np.einsum('ijklijkl->', Xi2))
    Vtot_closed = fro2(C4) - fro2(iso)
    out = {
        "sym": sym,
        "KV_pinned": pinned["KV"], "KR_pinned": pinned["KR"],
        "GV_pinned": pinned["GV"], "GR_pinned": pinned["GR"],
        "KV_gen": KVg, "GV_gen": GVg, "KR_gen": KRg, "GR_gen": GRg,
        "quad_doubling_rel": abs(Vtot2 / Vtot - 1.0),
        "mean_vs_voigtiso_rel": math.sqrt(fro2(meanC - iso) / fro2(iso)),
        "V_tot": Vtot, "V_tot_closed": Vtot_closed,
        "V_tot_rel_resid": abs(Vtot / Vtot_closed - 1.0),
        "Phi_G": Vtot / pinned["GV"] ** 2,
        "Phi_full": Vtot / fro2(iso),
    }
    vk = {"dc15_sq": (0, 4, 0, 4), "dc25_sq": (1, 4, 1, 4), "dc35_sq": (2, 4, 2, 4),
          "dc45_sq": (3, 4, 3, 4), "dc55_sq": (4, 4, 4, 4), "dc56_sq": (4, 5, 4, 5),
          "dc15dc25": (0, 4, 1, 4), "dc15dc35": (0, 4, 2, 4), "dc25dc35": (1, 4, 2, 4)}
    tp = {0: (0, 0), 1: (1, 1), 2: (2, 2), 3: (1, 2), 4: (0, 2), 5: (0, 1)}
    out["pinned_46i_contractions"] = {
        k: float(Xi[tp[A] + tp[B] + tp[A2] + tp[B2]]) for k, (A, B, A2, B2) in vk.items()}
    print(f" {name}: V_tot {Vtot:.6f} (closed {Vtot_closed:.6f})")
    gate(f"{name}.Vtot_identity", out["V_tot_rel_resid"], 1e-9)
    gate(f"{name}.doubling", out["quad_doubling_rel"], 1e-9)
    gate(f"{name}.mean_voigtiso", out["mean_vs_voigtiso_rel"], 1e-10)
    if sym == "cubic":
        nu = extra_nu
        out["nu"] = nu
        coef, fit_resid = fit_xi_in_basis(Xi)
        out["closed_basis_fit_resid"] = fit_resid
        out["abc_machine"] = [float(x) for x in coef]
        out["a_vs_pinned_clean_string_rel"] = abs(coef[0] / (2.0 * nu * nu / 1575.0) - 1.0)
        out["bc_pinned_strings"] = "corrupted in transport -- not consumed (pin E3); machine values above"
        out["cubic_collapse_rel"] = abs(Vtot / (1.2 * nu * nu) - 1.0)
        anc = max(abs(phi_pm(Xi, 'L', 'L', m) / ((nu * nu / 525.0) * (3.0 + m * m) ** 2) - 1.0)
                  for m in (-1.0, -0.6, -0.2, 0.2, 0.5, 0.8, 1.0))
        out["A_anchor_rel"] = anc
        gate(f"{name}.closed_basis_fit", fit_resid, 1e-9)
        gate(f"{name}.a_string_clean", out["a_vs_pinned_clean_string_rel"], 1e-9)
        gate(f"{name}.cubic_collapse", out["cubic_collapse_rel"], 1e-9)
        gate(f"{name}.A_anchor", anc, 1e-9)
    # ---- phase 1b: Rayleigh assembly + finite-ka ----
    VT = math.sqrt(mu)
    VL = math.sqrt(lam + 2.0 * mu)
    iTT = int_phi(Xi, 'T', 'T')
    iTL = int_phi(Xi, 'T', 'L')
    iLL = int_phi(Xi, 'L', 'L')
    iLT = int_phi(Xi, 'L', 'T')
    QTT = iTT / (2.0 * VT ** 4)
    QTL = VT * iTL / (2.0 * VL ** 5)
    QT = QTT + QTL
    QL = iLL / (2.0 * VL ** 4) + VL * iLT / (2.0 * VT ** 5)
    grid = [0.02, 0.03, 0.05, 0.08, 0.12]
    al = [alpha_finite(Xi, VT, VL, k) for k in grid]
    lk = [math.log(k) for k in grid[:3]]
    la = [math.log(x) for x in al[:3]]
    mb = sum(lk) / 3.0
    fit = sum((x - mb) * y for x, y in zip(lk, la)) / sum((x - mb) ** 2 for x in lk)
    q1, q2 = al[0] / grid[0] ** 4, al[1] / grid[1] ** 4
    qext = (grid[1] ** 2 * q1 - grid[0] ** 2 * q2) / (grid[1] ** 2 - grid[0] ** 2)
    p1b = {
        "mu_bar": mu, "lam_bar": lam, "VT0": VT, "VL0": VL,
        "int_Phi_TT": iTT, "int_Phi_TL": iTL,
        "Q_T_a": QT, "Q_T_TT_a": QTT, "Q_T_TL_a": QTL, "Q_L_a": QL,
        "kTa_grid": grid, "alpha_T_a": al, "fit_exponent": fit,
        "Q_ext_richardson": qext, "Q_T_d": QT / 8.0,
        "Qprime_G": (QT / 8.0) / out["Phi_G"], "status": "FULL"}
    if sym == "cubic":
        nu = extra_nu
        c011 = lam + 2.0 * mu
        p1b["eps_L"] = math.sqrt(4.0 * nu * nu / 525.0) / c011
        p1b["eps_T"] = math.sqrt(3.0 * nu * nu / 700.0) / mu
    gate(f"{name}.richardson_vs_closed", qext / QT - 1.0, 1e-4)
    gate(f"{name}.fit_exp_class4", fit - 4.0, 0.05)
    return out, p1b, Xi

# ---------------- HS bounds ----------------
def cubic_hs(c11, c12, c44):
    """Pinned cubic HS-1962 closed forms, Eqs. (9)-(10); K exact = (c11+2c12)/3.
    Zener > 1 here, so (1) = lower, (2) = upper."""
    K = (c11 + 2 * c12) / 3.0
    dc = c11 - c12
    mu1 = dc / 2.0 + 3.0 / (10.0 / (2 * c44 - dc)
                            + 24.0 * (K + dc) / (5.0 * dc * (3 * K + 2 * dc)))
    mu2 = c44 + 1.0 / (5.0 / (dc - 2 * c44)
                       + 9.0 * (K + 2 * c44) / (5.0 * c44 * (3 * K + 4 * c44)))
    return K, (mu1, mu2) if mu1 <= mu2 else (mu2, mu1)

def cubic_hs_bigK(c11, c12, c44):
    """K >> c limit forms, Eqs. (11)-(12) -- implementation control only."""
    dc = c11 - c12
    mu1 = dc / 2.0 + 3.0 / (10.0 / (2 * c44 - dc) + 8.0 / (5.0 * dc))
    mu2 = c44 + 1.0 / (5.0 / (dc - 2 * c44) + 3.0 / (5.0 * c44))
    return mu1, mu2

def hex_k_hs(c11, c12, c13, c33, c44, c66):
    """PMW/Berryman node11 K bounds, Eqs. (27)-(31): K_HS(G) = K_V (Geffr + z)/(Geffv + z)
    with z = (G/6)(9K+8G)/(K+2G), K = K_V (Geffr - G)/(Geffv - G).
    Operationalization (logged): tightest-lower = max of K_HS over admissible
    G in [0, min(C44, Geffr, C66)]; tightest-upper = min over
    G in (max(C44, Geffv, C66), 200*max]; grid + golden refinement."""
    h = hex_pinned(c11, c12, c13, c33, c44, c66)
    KV, Geffv, Geffr = h["KV"], h["Geffv"], h["Geffr"]
    def khs(G):
        if G <= 0.0:
            return KV * Geffr / Geffv
        Kpm = KV * (Geffr - G) / (Geffv - G)
        z = (G / 6.0) * (9.0 * Kpm + 8.0 * G) / (Kpm + 2.0 * G)
        return KV * (Geffr + z) / (Geffv + z)
    def refine(lo, hi, sign):
        for _ in range(200):
            m1 = lo + (hi - lo) * 0.381966
            m2 = hi - (hi - lo) * 0.381966
            if sign * khs(m1) < sign * khs(m2):
                lo = m1
            else:
                hi = m2
        return 0.5 * (lo + hi)
    gmin = min(c44, Geffr, c66)
    gmax = max(c44, Geffv, c66)
    grid_lo = np.linspace(0.0, gmin, 4001)
    vals_lo = [khs(g) for g in grid_lo]
    i = int(np.argmax(vals_lo))
    a, b = grid_lo[max(0, i - 1)], grid_lo[min(len(grid_lo) - 1, i + 1)]
    g_lo = refine(a, b, +1.0)
    if khs(0.0) >= khs(g_lo):
        g_lo = 0.0
    grid_hi = np.linspace(gmax * (1.0 + 1e-6), 200.0 * gmax, 40001)
    vals_hi = [khs(g) for g in grid_hi]
    j = int(np.argmin(vals_hi))
    a, b = grid_hi[max(0, j - 1)], grid_hi[min(len(grid_hi) - 1, j + 1)]
    g_hi = refine(a, b, -1.0)
    if khs(grid_hi[-1]) <= khs(g_hi):
        g_hi = grid_hi[-1]
    return h, [khs(g_lo), khs(g_hi)], [float(g_lo), float(g_hi)]

# ================= main =================
def main():
    raw = open(INPUT, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    if got != INPUT_MD5:
        print("INPUT MD5 MISMATCH -- HALT", got)
        sys.exit(9)
    print("input md5 verified:", got)
    data = json.loads(raw)
    lits = json.loads(raw, parse_float=lambda s: s)

    # ---- controls: Al benchmark (SI, this control only) + Table I + iso-null Xi ----
    print("controls:")
    MAl = voigt_cubic(103.4, 57.1, 28.6)
    KVa, GVa, _, _ = gen_chain(MAl)
    lamA = KVa - 2.0 * GVa / 3.0
    vTA = math.sqrt(GVa * 1e9 / 2700.0)
    vLA = math.sqrt((lamA + 2.0 * GVa) * 1e9 / 2700.0)
    gate("al.lam", lamA / 54.92 - 1.0, 1e-4)
    gate("al.mu", GVa / 26.42 - 1.0, 1e-4)
    gate("al.vT", vTA / 3128.13 - 1.0, 1e-4)
    gate("al.vL", vLA / 6317.52 - 1.0, 1e-4)
    t1lo, t1hi = cubic_hs_bigK(0.0490 + 1.0, 1.0, 0.1828)  # dc = 0.0490 via c12-shift invariance
    gate("tableI.hs_lo", t1lo / 0.0712 - 1.0, 1e-3)
    gate("tableI.hs_hi", t1hi / 0.1028 - 1.0, 1e-3)
    grc = cubic_closed(0.0490 + 1.0, 1.0, 0.1828)
    gate("tableI.vr_lo", grc["GR"] / 0.0510 - 1.0, 1e-3)
    gate("tableI.vr_hi", grc["GV"] / 0.1195 - 1.0, 1e-3)
    Xi_iso, _ = xi_quadrature(iso_tensor(85.0, 73.0))
    gate("iso_null_Xi", float(np.max(np.abs(Xi_iso))) / 85.0 ** 2, 1e-12)
    al_bench = {"lam": lamA, "mu": GVa, "VT": vTA, "VL": vLA,
                "tableI_control": {"VR": [grc["GR"], grc["GV"]], "HS": [t1lo, t1hi]}}

    # ---- config tensors (full precision, from the verified file ONLY) ----
    v = data["vrh"]
    cfg = {}
    cs = v["hex:step"]["C_over_rho"]; cfg["step_hex"] = ("hex", [cs[k] for k in ("C11", "C12", "C13", "C33", "C44", "C66")])
    cs = v["hex:gem8"]["C_over_rho"]; cfg["gem8_hex"] = ("hex", [cs[k] for k in ("C11", "C12", "C13", "C33", "C44", "C66")])
    cs = v["cubic:step"]["C_over_rho"]; cfg["step_cubic"] = ("cubic", [cs["C11"], cs["C12"], cs["C44"]])
    cs = v["cubic:gem8"]["C_over_rho"]; cfg["gem8_cubic"] = ("cubic", [cs["C11"], cs["C12"], cs["C44"]])
    key_map = {"step_hex": "hex:step", "gem8_hex": "hex:gem8",
               "step_cubic": "cubic:step", "gem8_cubic": "cubic:gem8"}

    # ---- C2: reproduce every stored scalar at printed precision (general chain) ----
    print("phase 0-full (C2):")
    def tol_of(lit):
        d = len(lit.split(".")[1]) if "." in lit else 0
        return 0.6 * 10.0 ** (-d)
    c2 = {}
    worst = 0.0
    hill_g = {}
    hill_v = {}
    for name, (sym, cc) in cfg.items():
        M6 = voigt_hex(*cc) if sym == "hex" else voigt_cubic(*cc)
        KVg, GVg, KRg, GRg = gen_chain(M6)
        KH, GH = 0.5 * (KVg + KRg), 0.5 * (GVg + GRg)
        hill_g[name] = GH
        vals = {"K_VRH": KH, "G_V": GVg, "G_R": GRg, "G_VRH": GH,
                "VR_spread_pct": 100.0 * (GVg - GRg) / GH,
                "AU": 5.0 * GVg / GRg + KVg / KRg - 6.0,
                "vT_V": math.sqrt(GVg), "vT_R": math.sqrt(GRg), "vT_VRH": math.sqrt(GH),
                "vT_halfwidth_pct": 100.0 * (math.sqrt(GVg) - math.sqrt(GRg)) / (2.0 * math.sqrt(GH))}
        hill_v[name] = vals["vT_VRH"]
        block = {}
        for q, gotv in vals.items():
            lit = lits["vrh"][key_map[name]][q]
            stored = float(lit); tol = tol_of(lit)
            res = abs(gotv - stored)
            block[q] = {"got": gotv, "stored": stored, "absres": res, "tol": tol,
                        "ok": bool(res <= tol)}
            worst = max(worst, res / tol)
        c2[name] = block
    for mixname, lo, hi in (("mixture:step", "step_cubic", "step_hex"),
                            ("mixture:gem8", "gem8_cubic", "gem8_hex")):
        block = {}
        g0, g1 = hill_g[lo], hill_g[hi]
        vv = {}
        for fs, lit in lits["vrh"][mixname]["f_hcp -> vT"].items():
            f = float(fs)
            gv = (1 - f) * g0 + f * g1
            gr = 1.0 / ((1 - f) / g0 + f / g1)
            vv[fs] = math.sqrt(0.5 * (gv + gr))
            stored = float(lit); tol = tol_of(lit)
            res = abs(vv[fs] - stored)
            block[f"vT(f={fs})"] = {"got": vv[fs], "stored": stored, "absres": res,
                                    "tol": tol, "ok": bool(res <= tol)}
            worst = max(worst, res / tol)
        span = 100.0 * (vv["1.0"] - vv["0.0"]) / (0.5 * (vv["1.0"] + vv["0.0"]))
        lit = lits["vrh"][mixname]["phase_span_pct"]
        stored = float(lit); tol = tol_of(lit)
        res = abs(span - stored)
        block["phase_span_pct"] = {"got": span, "stored": stored, "absres": res,
                                   "tol": tol, "ok": bool(res <= tol)}
        worst = max(worst, res / tol)
        c2[mixname] = block
    bad = [f"{c}.{q}" for c, blk in c2.items() for q, r in blk.items() if not r["ok"]]
    if bad:
        FAILURES.extend(["C2:" + b for b in bad])
    print(f"  C2 {'PASS' if not bad else 'FAIL'} worst residual/tol {worst:.4f}")

    # ---- phase 0b-full: HS ----
    print("phase 0b-full:")
    p0b = {}
    for name in ("step_cubic", "gem8_cubic"):
        sym, cc = cfg[name]
        K, (lo, hi) = cubic_hs(*cc)
        vlo, vhi = math.sqrt(lo), math.sqrt(hi)
        _, GVg, _, GRg = gen_chain(voigt_cubic(*cc))
        p0b[name] = {"K": K, "mu_HS": [lo, hi], "vT_HS": [vlo, vhi],
                     "vT_VR": [math.sqrt(GRg), math.sqrt(GVg)],
                     "HS_halfwidth_pct": 100.0 * (vhi - vlo) / (2.0 * hill_v[name]),
                     "VR_halfwidth_pct": 100.0 * (math.sqrt(GVg) - math.sqrt(GRg)) / (2.0 * hill_v[name]),
                     "status": "FULL"}
    for name in ("step_hex", "gem8_hex"):
        sym, cc = cfg[name]
        h, khs, gopt = hex_k_hs(*cc)
        _, GVg, _, GRg = gen_chain(voigt_hex(*cc))
        p0b[name] = {"K_V": h["KV"], "K_R_berryman": h["KR"], "K_R_1606": h["KR1606"],
                     "Geffv": h["Geffv"], "Geffr": h["Geffr"],
                     "product_selfchecks": h["product_selfchecks"],
                     "K_HS": khs, "G_optimizers": gopt,
                     "K_band_note": "degenerate at input-identity-residual floor",
                     "G_HS": "PENDING-verbatim (pin S2 elided term); VR shear bracket "
                             f"[{GRg:.4f}, {GVg:.4f}]",
                     "status": "K FULL; G PENDING"}
        gate(f"{name}.product_id_1", h["product_selfchecks"][0], 1e-12)
        gate(f"{name}.product_id_2", h["product_selfchecks"][1], 1e-12)

    # ---- phase 1 (a+b), full precision, all four configs ----
    print("phase 1-full:")
    p1a, p1b = {}, {}
    x1 = {}
    for name, (sym, cc) in cfg.items():
        if sym == "hex":
            pin = hex_pinned(*cc)
            pinned = {"KV": pin["KV"], "KR": pin["KR"], "GV": pin["GV"], "GR": pin["GR"]}
            M6 = voigt_hex(*cc)
            nu = None
        else:
            cl = cubic_closed(*cc)
            pinned = {"KV": cl["K"], "KR": cl["K"], "GV": cl["GV"], "GR": cl["GR"]}
            M6 = voigt_cubic(*cc)
            nu = cc[0] - cc[1] - 2.0 * cc[2]
        a1, b1, _ = run_phase1(name, sym, M6, pinned, extra_nu=nu)
        p1a[name], p1b[name] = a1, b1

    meta = {"instrument": "poly1_fullprec_ccleg.py", "leg": "cc",
            "input_file": os.path.basename(INPUT), "input_md5": INPUT_MD5,
            "pin_record_md5": PIN_MD5, "prereg_md5": PREREG_MD5,
            "time": str(datetime.now(timezone.utc))}

    def dump(obj, fn):
        blob = json.dumps(obj, indent=1)
        open(os.path.join(HERE, fn), "w").write(blob)
        print(f"  wrote {fn} md5 {hashlib.md5(blob.encode()).hexdigest()}")

    dump({"C2": c2, "C2_verdict": "PASS" if not bad else "FAIL",
          "worst_residual_of_tol": worst, "al_benchmark": al_bench, "_meta": dict(meta, phase="0-full (C2)")},
         "poly1_phase0full_cc.json")
    dump({"phase0b": p0b, "_meta": dict(meta, phase="0b-full")}, "poly1_phase0bfull_cc.json")
    dump({"phase1a": p1a, "phase1b": p1b, "_meta": dict(meta, phase="1-full")},
         "poly1_phase1full_cc.json")

    # ---- quoted-layer phase 1 cross-check (main-dispatch C3/C4 control) ----
    print("phase 1-quoted cross-check:")
    qcfg = {
        "step_hex": ("hex", [238.42, 108.54, 57.48, 287.67, 60.03, 64.92]),
        "gem8_cubic": ("cubic", [272.08, 179.38, 131.54]),
        "step_cubic": ("cubic", [73.46, 0.0, 85.29]),  # c12 = 0 surrogate; Xi invariant
    }
    q1a, q1b = {}, {}
    for name, (sym, cc) in qcfg.items():
        if sym == "hex":
            pin = hex_pinned(*cc)
            pinned = {"KV": pin["KV"], "KR": pin["KR"], "GV": pin["GV"], "GR": pin["GR"]}
            M6 = voigt_hex(*cc)
            nu = None
        else:
            cl = cubic_closed(*cc)
            pinned = {"KV": cl["K"], "KR": cl["K"], "GV": cl["GV"], "GR": cl["GR"]}
            M6 = voigt_cubic(*cc)
            nu = cc[0] - cc[1] - 2.0 * cc[2]
        a1, b1, _ = run_phase1(name, sym, M6, pinned, extra_nu=nu)
        if name == "step_cubic":
            b1["status"] = "PARTIAL-at-quoted: T-to-T verdict class (K surrogate c12=0; " \
                           "Q_T_TT exact by Xi shift-invariance)"
        q1a[name], q1b[name] = a1, b1
    # Xi shift-invariance control on step_cubic (quoted): c12 = 0 vs c12 = 50 at fixed nu
    XiA, _ = xi_quadrature(tensor_from_voigt(voigt_cubic(73.46, 0.0, 85.29)))
    XiB, _ = xi_quadrature(tensor_from_voigt(voigt_cubic(173.46, 100.0, 85.29)))
    shift_ctrl = float(np.max(np.abs(XiA - XiB)) / np.max(np.abs(XiA)))
    gate("xi_shift_invariance", shift_ctrl, 1e-9)
    for nm, key in (("step_hex", "Q_T_a"), ("gem8_cubic", "Q_T_a")):
        x1[nm] = p1b[nm][key] / q1b[nm][key] - 1.0
    x1["step_cubic_TT"] = p1b["step_cubic"]["Q_T_TT_a"] / q1b["step_cubic"]["Q_T_TT_a"] - 1.0
    Kq, (loq, hiq) = cubic_hs(272.08, 179.38, 131.54)
    dump({"phase1a": q1a, "phase1b": q1b,
          "phase0b_quoted_gem8": {"K": Kq, "mu_HS": [loq, hiq]},
          "xi_shift_invariance_ctrl": shift_ctrl,
          "x1_layer_deltas_fullprec_over_quoted": x1,
          "_meta": dict(meta, phase="1-quoted-crosscheck")},
         "poly1_phase1quoted_cc.json")

    print("FAILURES:", FAILURES if FAILURES else "none")
    print("VERDICT:", "ALL GATES PASS" if not FAILURES else "GATE MISS -- S9")
    sys.exit(0 if not FAILURES else 9)

if __name__ == "__main__":
    main()
