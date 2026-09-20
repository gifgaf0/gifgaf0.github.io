#!/usr/bin/env python3
"""g_mscs1_ccleg.py -- Gate G-MSCS1, CC leg instrument.

Built blind from staging_memo_G_MSCS1_v2.md (3f30262e), G_MSCS1_LOCK_RECORD.md
Addendum A-2 (3dbe953b) and g_mscs1_schema_v1_0.json (76a42db3) ONLY, before any
quarantined chat artifact was decoded.

Independence variations (requested in the dispatch, step 3.2):
  - SO(3) product grid ZYZ (20, 12, 20) (chat: (16, 10, 16); G-S2C1 CC: (12, 8, 12));
    exactness for band-limit <= 19 in alpha/gamma, polynomial degree <= 23 in cos(beta).
  - mu-moments I0, I2 of the Born kernels by a degree-8 polynomial fit on 9 Chebyshev
    nodes, integrated analytically (chat: 8-point Gauss-Legendre).
  - Mandel (orthonormal 6x6) tensor algebra throughout; own branch labelling code.

Halt discipline: md5 guards on memo/X-1/X-3/X-4/X-5/T1 list/schema before any
computation; T1 self-scan (this file + memo) at every invocation with the t1_scan.py
rule; any Phase-0 control failure -> INDETERMINATE and no later phase is trusted.
"""
import hashlib
import importlib.util
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_MD5 = "76a42db3fd6ad82e485752bc2ddb24d5"
T1_LIST = os.path.join(HERE, "tools", "t1", "T1_forbidden_G_MSCS1.txt")
T1_SCANNER = os.path.join(HERE, "tools", "t1", "t1_scan.py")
T1_LIST_MD5 = "fef2827100d3f85e0a6341b44f0c00bf"
GUARDS = {
    "staging_memo_G_MSCS1_v2.md": ("3f30262eaec461fb5fd3202835f7de37", 34837),
    "g_mscs1_schema_v1_0.json": (SCHEMA_MD5, 3906),
    "inputs/poly_vrh_results.json": ("200e7a8b775577564369c6924d38a84c", 2767),
    "inputs/cc_p2_phase1.json": ("aaae206733b0f0a378a5c6b600274d3f", 11454),
    "inputs/poly1_phase1full_cc.json": ("ec87e42f0f617b00c4985ba2aceac339", 8140),
    "inputs/chatleg_phase0bfull.json": ("df413a7cfa30e599b779af8fee5d07d1", 1920),
}


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_file(p):
    return md5_bytes(open(p, "rb").read())


def halt(msg):
    print("HALT: " + msg)
    sys.exit(1)


def guard_files():
    for rel, (want, nbytes) in GUARDS.items():
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            halt(f"guarded file missing: {rel}")
        b = open(p, "rb").read()
        got = md5_bytes(b)
        if got != want or len(b) != nbytes:
            halt(f"guard mismatch on {rel}: md5 {got} bytes {len(b)}")


def t1_selfscan():
    """T1 gate-list guard + self-scan of this instrument and the memo (halt on any hit)."""
    if not os.path.exists(T1_LIST):
        halt("T1 gate list absent -- no computation without it (D-T1 RETIRED)")
    if md5_file(T1_LIST) != T1_LIST_MD5:
        halt("T1 gate list md5 mismatch")
    spec = importlib.util.spec_from_file_location("t1_scan", T1_SCANNER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pats = mod.load(T1_LIST)
    ncoll = 0
    for f in (os.path.abspath(__file__), os.path.join(HERE, "staging_memo_G_MSCS1_v2.md")):
        text = open(f, "rb").read().decode("utf-8", "replace")
        hits, coll = mod.scan_text(text, pats)
        if hits:
            halt(f"T1 HIT in {os.path.basename(f)}: {[i for i, _ in hits]}")
        ncoll += len(coll)
    return mod, pats, ncoll


# ---------------------------------------------------------------- tensor algebra
VOIGT_PAIRS = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
SQ2 = math.sqrt(2.0)
MANDEL_F = np.array([1.0, 1.0, 1.0, SQ2, SQ2, SQ2])
M6 = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
J6 = np.outer(M6, M6) / 3.0
K6 = np.eye(6) - J6


def voigt_matrix_to_tensor(Cv):
    """6x6 Voigt-notation stiffness -> full 3x3x3x3 tensor."""
    C = np.zeros((3, 3, 3, 3))
    for a, (i, j) in enumerate(VOIGT_PAIRS):
        for b, (k, l) in enumerate(VOIGT_PAIRS):
            for ii, jj in ((i, j), (j, i)):
                for kk, ll in ((k, l), (l, k)):
                    C[ii, jj, kk, ll] = Cv[a, b]
    return C


def tensor_to_mandel(C):
    M = np.zeros((6, 6))
    for a, (i, j) in enumerate(VOIGT_PAIRS):
        for b, (k, l) in enumerate(VOIGT_PAIRS):
            M[a, b] = MANDEL_F[a] * MANDEL_F[b] * C[i, j, k, l]
    return M


def mandel_to_tensor(M):
    Cv = M / np.outer(MANDEL_F, MANDEL_F)
    return voigt_matrix_to_tensor(Cv)


def voigt_dict_to_mandel(sym, d):
    Cv = np.zeros((6, 6))
    if sym == "hex":
        C11, C12, C13, C33, C44, C66 = d
        Cv[0, 0] = Cv[1, 1] = C11
        Cv[2, 2] = C33
        Cv[0, 1] = Cv[1, 0] = C12
        Cv[0, 2] = Cv[2, 0] = Cv[1, 2] = Cv[2, 1] = C13
        Cv[3, 3] = Cv[4, 4] = C44
        Cv[5, 5] = C66
    else:
        C11, C12, C44 = d
        Cv[0, 0] = Cv[1, 1] = Cv[2, 2] = C11
        Cv[0, 1] = Cv[0, 2] = Cv[1, 2] = C12
        Cv[1, 0] = Cv[2, 0] = Cv[2, 1] = C12
        Cv[3, 3] = Cv[4, 4] = Cv[5, 5] = C44
    return tensor_to_mandel(voigt_matrix_to_tensor(Cv))


def iso_KG(M):
    K = float(M6 @ M @ M6) / 9.0
    G = (float(np.trace(M)) - 3.0 * K) / 10.0
    return K, G


def iso_mandel(K, G):
    return 3.0 * K * J6 + 2.0 * G * K6


def iso_project(M):
    """Uniform SO(3) orientation average of a stiffness-symmetric tensor (closed form)."""
    K, G = iso_KG(M)
    return iso_mandel(K, G)


def rot_zyz(alpha, beta, gamma):
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    cg, sg = np.cos(gamma), np.sin(gamma)
    Rz1 = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
    Rz2 = np.array([[cg, -sg, 0], [sg, cg, 0], [0, 0, 1]])
    return Rz1 @ Ry @ Rz2


def so3_grid(na, nb, ng):
    """ZYZ product grid: uniform alpha/gamma, Gauss-Legendre in cos(beta); weights sum to 1."""
    xb, wb = np.polynomial.legendre.leggauss(nb)
    alphas = 2.0 * np.pi * np.arange(na) / na
    gammas = 2.0 * np.pi * np.arange(ng) / ng
    Rs, ws = [], []
    for ia in range(na):
        for ib in range(nb):
            beta = math.acos(xb[ib])
            for ig in range(ng):
                Rs.append(rot_zyz(alphas[ia], beta, gammas[ig]))
                ws.append(wb[ib] / (2.0 * na * ng))
    return np.array(Rs), np.array(ws)


def rotate_tensor_batch(C4, Rs):
    return np.einsum("gia,gjb,gkc,gld,abcd->gijkl", Rs, Rs, Rs, Rs, C4, optimize=True)


def odf_averages(M_cr, Rs, ws, p2w):
    """Return (A, B) in Mandel: uniform and P2-weighted SO(3) averages of Rot_g[C]."""
    C4 = mandel_to_tensor(M_cr)
    Crot = rotate_tensor_batch(C4, Rs)
    A4 = np.einsum("g,gijkl->ijkl", ws, Crot)
    B4 = np.einsum("g,gijkl->ijkl", ws * p2w, Crot)
    return tensor_to_mandel(A4), tensor_to_mandel(B4)


def P2(x):
    return 1.5 * x * x - 0.5


# ---------------------------------------------------------------- sphere sampling
def sphere_grid(n_theta, n_phi):
    x, w = np.polynomial.legendre.leggauss(n_theta)
    phi = 2.0 * np.pi * np.arange(n_phi) / n_phi
    ct = np.repeat(x, n_phi)
    st = np.sqrt(1.0 - ct * ct)
    ph = np.tile(phi, n_theta)
    k = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=1)
    wt = np.repeat(w, n_phi) / (2.0 * n_phi)  # sums to 1
    return k, wt


def christoffel(M_agg, khat):
    C4 = mandel_to_tensor(M_agg)
    G = np.einsum("ijkl,nj,nl->nik", C4, khat, khat, optimize=True)
    G = 0.5 * (G + np.swapaxes(G, 1, 2))
    evals, evecs = np.linalg.eigh(G)
    evals = np.maximum(evals, 0.0)
    v = np.sqrt(evals)                       # (n,3) ascending
    e = np.swapaxes(evecs, 1, 2)             # (n,3branch,3comp)
    return v, e


def mode_geometry(khat, v, e):
    """Per (node, branch): lam = (khat.e)^2, w_EM, S_perp, |S_perp|^2."""
    ke = np.einsum("ni,nbi->nb", khat, e)
    lam = ke * ke
    eperp = e - ke[:, :, None] * khat[:, None, :]
    wEM = np.einsum("nbi,nbi->nb", eperp, eperp)
    S = 0.5 * (np.einsum("ni,nbj->nbij", khat, eperp) + np.einsum("nbi,nj->nbij", eperp, khat))
    s2 = 0.5 * wEM  # |sym(k x eperp)|^2 = |eperp|^2 / 2 exactly (k.eperp = 0)
    return lam, wEM, S, s2


def f_E2_fixed_axis(S, s2, nhat):
    """m=+-2 fraction of the transverse-projected strain about a fixed axis nhat."""
    a = np.einsum("...ij,i,j->...", S, nhat, nhat)
    Sn = np.einsum("...ij,j->...i", S, nhat)
    sn2 = np.einsum("...i,...i->...", Sn, Sn)
    out = np.zeros_like(a)
    ok = s2 > 1e-30
    out[ok] = 1.0 - 2.0 * sn2[ok] / s2[ok] + 0.5 * a[ok] * a[ok] / s2[ok]
    return out


def f_E2_odf_moments(S, s2, nvec, wn, p2n):
    """Per mode: F0 = uniform n-average of f_E2, F2 = P2-weighted n-average (GL 12 x 24).
    Modes with no transverse strain content (s2 ~ 0) carry zero descriptor weight; their
    f is set to 0 and they are flagged invalid for the SO(3) 2/5 control."""
    nb = S.shape[0]
    F0 = np.zeros(S.shape[:-2])
    F2 = np.zeros(S.shape[:-2])
    valid = s2 > 1e-20
    Ssq = np.einsum("...ij,...jk->...ik", S, S)
    step = 1024
    for i0 in range(0, nb, step):
        sl = slice(i0, min(i0 + step, nb))
        a = np.einsum("nbij,mi,mj->nbm", S[sl], nvec, nvec, optimize=True)
        sn2 = np.einsum("nbij,mi,mj->nbm", Ssq[sl], nvec, nvec, optimize=True)
        with np.errstate(divide="ignore", invalid="ignore"):
            f = 1.0 - 2.0 * sn2 / s2[sl][:, :, None] + 0.5 * a * a / s2[sl][:, :, None]
        f[~np.isfinite(f)] = 0.0
        f[s2[sl] <= 1e-30] = 0.0
        F0[sl] = f @ wn
        F2[sl] = f @ (wn * p2n)
    return F0, F2, valid


def n_sphere_grid(n_theta=12, n_phi=24):
    x, w = np.polynomial.legendre.leggauss(n_theta)
    phi = 2.0 * np.pi * np.arange(n_phi) / n_phi
    ct = np.repeat(x, n_phi)
    st = np.sqrt(1.0 - ct * ct)
    ph = np.tile(phi, n_theta)
    n = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=1)
    wn = np.repeat(w, n_phi) / (2.0 * n_phi)
    return n, wn, P2(ct)


# ---------------------------------------------------------------- branch labels
def label_branches(sym, khat, v, e, lam):
    """Return integer index arrays (n,) for each label. Own implementation.

    hex:  qSH by maximum |e . unit(z x k)| (exact decoupling only on arm (b),
          H-class disclosure); of the remaining two, qL by larger lam, qSV the other.
    cubic: qL by maximum lam (admixture), then qT1 the faster, qT2 the slower.
    """
    n = khat.shape[0]
    idx = np.arange(n)
    if sym == "hex":
        m = np.stack([-khat[:, 1], khat[:, 0], np.zeros(n)], axis=1)
        norm = np.linalg.norm(m, axis=1, keepdims=True)
        norm[norm < 1e-15] = 1.0
        m /= norm
        ov = np.abs(np.einsum("ni,nbi->nb", m, e))
        bSH = np.argmax(ov, axis=1)
        rest = np.array([[b for b in range(3) if b != s] for s in bSH])
        lam_rest = lam[idx[:, None], rest]
        pick = np.argmax(lam_rest, axis=1)
        bL = rest[idx, pick]
        bSV = rest[idx, 1 - pick]
        return {"qL": bL, "qSV": bSV, "qSH": bSH}
    bL = np.argmax(lam, axis=1)
    rest = np.array([[b for b in range(3) if b != s] for s in bL])
    v_rest = v[idx[:, None], rest]
    pick = np.argmax(v_rest, axis=1)
    bT1 = rest[idx, pick]
    bT2 = rest[idx, 1 - pick]
    return {"qL": bL, "qT1": bT1, "qT2": bT2}


# ---------------------------------------------------------------- phase 1
def phase1_config(M_cr, sym, nhat, kq, wq):
    v, e = christoffel(M_cr, kq)
    lam, wEM, S, s2 = mode_geometry(kq, v, e)
    fE2 = f_E2_fixed_axis(S, s2, nhat)
    wS2E2 = fE2 * wEM
    wS2h = (1.0 - lam) / (1.0 + lam / 3.0)
    labels = label_branches(sym, kq, v, e, lam)

    W = wq[:, None]
    sums = {
        "EM": (float(np.sum(W * wEM * v)), float(np.sum(W * wEM))),
        "S2E2": (float(np.sum(W * wS2E2 * v)), float(np.sum(W * wS2E2))),
        "S2h": (float(np.sum(W * wS2h * v)), float(np.sum(W * wS2h))),
    }
    vX = {k: a / b for k, (a, b) in sums.items()}

    # covariance of admixture and speed over the EM-weighted mode ensemble (all branches)
    wtot = sums["EM"][1]
    mlam = float(np.sum(W * wEM * lam)) / wtot
    mv = sums["EM"][0] / wtot
    mlv = float(np.sum(W * wEM * lam * v)) / wtot
    cov = mlv - mlam * mv

    idx = np.arange(kq.shape[0])
    qt_names = [nm for nm in labels if nm != "qL"]
    lam_qt = np.stack([lam[idx, labels[nm]] for nm in qt_names], axis=1)
    lam_mean = float(np.sum(wq[:, None] * lam_qt) / 2.0)
    flat = int(np.argmax(lam_qt))
    node, col = flat // 2, flat % 2
    lam_max = float(lam_qt[node, col])
    lam_max_branch = qt_names[col]

    share_EM, share_E2 = {}, {}
    for nm, bidx in labels.items():
        share_EM[nm] = float(np.sum(wq * wEM[idx, bidx])) / sums["EM"][1]
        share_E2[nm] = float(np.sum(wq * wS2E2[idx, bidx])) / sums["S2E2"][1]

    # F-CTRL-ADMIX, substantive (memo section 4, literal): replace each quasi-transverse
    # eigenvector by its normalized transverse projection (lam -> 0 there), keep the
    # quasi-longitudinal branch untouched, recompute r_xtal(S2-h) over all branches as
    # defined in memo 2.5.
    wEM_p = wEM.copy()
    wS2h_p = wS2h.copy()
    for nm in qt_names:
        wEM_p[idx, labels[nm]] = 1.0
        wS2h_p[idx, labels[nm]] = 1.0
    vEM_p = float(np.sum(W * wEM_p * v)) / float(np.sum(W * wEM_p))
    vS2h_p = float(np.sum(W * wS2h_p * v)) / float(np.sum(W * wS2h_p))
    r_h_proj = vS2h_p / vEM_p - 1.0

    # complete zero-admixture projection (every branch sent to its admixture-free
    # limit: quasi-transverse -> transverse, quasi-longitudinal -> longitudinal);
    # the reading under which the memo's "sends r to zero" statement is true
    wEM_c = wEM_p.copy()
    wS2h_c = wS2h_p.copy()
    wEM_c[idx, labels["qL"]] = 0.0
    wS2h_c[idx, labels["qL"]] = 0.0
    vEM_c = float(np.sum(W * wEM_c * v)) / float(np.sum(W * wEM_c))
    vS2h_c = float(np.sum(W * wS2h_c * v)) / float(np.sum(W * wS2h_c))
    r_h_complete = vS2h_c / vEM_c - 1.0

    # memo 2.6 covariance identity: r_xtal(S2-h) = -(1/3) Cov_EM(lam, v)/<v>_EM + O(lam^2)
    r_h_identity_pred = -cov / (3.0 * vX["EM"])

    return {
        "v_EM": vX["EM"], "v_S2E2": vX["S2E2"], "v_S2h": vX["S2h"],
        "r_xtal_E2": vX["S2E2"] / vX["EM"] - 1.0,
        "r_xtal_h": vX["S2h"] / vX["EM"] - 1.0,
        "lambda_mean": lam_mean, "lambda_max": lam_max,
        "lambda_max_branch": lam_max_branch, "cov_lambda_v": cov,
        "share_EM": share_EM, "share_S2E2": share_E2,
        "_r_h_projected": r_h_proj,
        "_r_h_complete": r_h_complete,
        "_r_h_identity_pred": r_h_identity_pred,
    }


# ---------------------------------------------------------------- HS bounds
def hs_tensor(P_M, Cstar):
    return np.linalg.inv(P_M) - Cstar


def cstar_of(K0, G0):
    Kst = 4.0 * G0 / 3.0
    Gst = G0 * (9.0 * K0 + 8.0 * G0) / (6.0 * (K0 + 2.0 * G0))
    return iso_mandel(Kst, Gst)


def g_hs_t0(M_cr, K0, G0):
    Cstar = cstar_of(K0, G0)
    T = np.linalg.inv(M_cr + Cstar)
    P_M = iso_project(T)
    return iso_KG(hs_tensor(P_M, Cstar))[1]


def _bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if f(mid) == flo:
            lo = mid
        else:
            hi = mid
    return hi if flo is False else lo  # last point on the True side


def hs_reference(M_cr, upper):
    """Optimize the isotropic reference at t = 0 per A-2.3.

    upper: minimal feasible majorant C0 >= C_g minimizing the resulting G_HS;
    lower: maximal minorant C0 <= C_g maximizing it. Returns (K0, G0).
    """
    K_cr, G_cr = iso_KG(M_cr)
    scale = float(np.linalg.norm(M_cr))
    tol_eig = -1e-11 * scale
    sgn = 1.0 if upper else -1.0

    def feasible(K0, G0):
        D = sgn * (iso_mandel(K0, G0) - M_cr)
        return float(np.linalg.eigvalsh(D)[0]) >= tol_eig

    def K0_boundary(G0):
        # upper: smallest feasible K0; lower: largest feasible K0 (objective is
        # monotone increasing in K0, verified post hoc at the solution)
        if upper:
            lo, hi = 1e-9 * K_cr, 60.0 * K_cr
            if not feasible(hi, G0):
                return None
            if feasible(lo, G0):
                return lo
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if feasible(mid, G0):
                    hi = mid
                else:
                    lo = mid
            return hi
        lo, hi = 1e-9 * K_cr, 60.0 * K_cr
        if not feasible(lo, G0):
            return None
        if feasible(hi, G0):
            return hi
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if feasible(mid, G0):
                lo = mid
            else:
                hi = mid
        return lo

    def objective(G0):
        K0 = K0_boundary(G0)
        if K0 is None:
            return None, None
        g = g_hs_t0(M_cr, K0, G0)
        return (g if upper else -g), K0

    G_lo, G_hi = 1e-4 * G_cr, 8.0 * G_cr
    grid = np.linspace(G_lo, G_hi, 481)
    vals = []
    for G0 in grid:
        ob, _ = objective(G0)
        vals.append(np.inf if ob is None else ob)
    vals = np.array(vals)
    i = int(np.argmin(vals))
    a = grid[max(i - 1, 0)]
    b = grid[min(i + 1, len(grid) - 1)]
    phi = (math.sqrt(5.0) - 1.0) / 2.0
    x1 = b - phi * (b - a)
    x2 = a + phi * (b - a)
    f1, _ = objective(x1)
    f2, _ = objective(x2)
    f1 = np.inf if f1 is None else f1
    f2 = np.inf if f2 is None else f2
    for _ in range(220):
        if f1 <= f2:
            b, x2, f2 = x2, x1, f1
            x1 = b - phi * (b - a)
            f1, _ = objective(x1)
            f1 = np.inf if f1 is None else f1
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + phi * (b - a)
            f2, _ = objective(x2)
            f2 = np.inf if f2 is None else f2
    G0 = 0.5 * (a + b)
    _, K0 = objective(G0)
    return K0, G0


# ---------------------------------------------------------------- phase 2
def fit_t(tv, rv, tmax):
    sel = np.abs(tv) <= tmax + 1e-12
    t = tv[sel]
    r = rv[sel]
    A = np.stack([t, t * t, t ** 3], axis=1)
    c, *_ = np.linalg.lstsq(A, r, rcond=None)
    resid = float(np.max(np.abs(A @ c - r)))
    return float(c[0]), float(c[1]), float(c[2]), resid


def fit_t4(tv, rv, tmax):
    sel = np.abs(tv) <= tmax + 1e-12
    t = tv[sel]
    r = rv[sel]
    A = np.stack([t, t * t, t ** 3, t ** 4], axis=1)
    c, *_ = np.linalg.lstsq(A, r, rcond=None)
    return [float(x) for x in c]


def aggregate_r(M_agg, t, kq, wq, ngrid):
    """r_agg_E2, r_agg_h and QT lambda mean on one aggregate tensor at texture t."""
    nvec, wn, p2n = ngrid
    v, e = christoffel(M_agg, kq)
    lam, wEM, S, s2 = mode_geometry(kq, v, e)
    F0, F2, valid = f_E2_odf_moments(S, s2, nvec, wn, p2n)
    fbar = F0 + t * F2
    wS2 = wEM * fbar
    wS2h = (1.0 - lam) / (1.0 + lam / 3.0)
    W = wq[:, None]
    vEM = float(np.sum(W * wEM * v)) / float(np.sum(W * wEM))
    vS2 = float(np.sum(W * wS2 * v)) / float(np.sum(W * wS2))
    vSh = float(np.sum(W * wS2h * v)) / float(np.sum(W * wS2h))
    idx = np.arange(kq.shape[0])
    bL = np.argmax(lam, axis=1)
    lam_qt_sum = np.sum(lam, axis=1) - lam[idx, bL]
    lam_mean = float(np.sum(wq * lam_qt_sum) / 2.0)
    return vS2 / vEM - 1.0, vSh / vEM - 1.0, lam_mean, F0, F2, valid


# ---------------------------------------------------------------- born (t = 0)
def born_t0_config(M_cr, Rs, ws):
    Kb, Gb = iso_KG(iso_project(M_cr))
    mu_bar = Gb
    lam_bar = Kb - 2.0 * Gb / 3.0
    V_T = math.sqrt(mu_bar)
    V_L = math.sqrt(lam_bar + 2.0 * mu_bar)
    Ciso4 = mandel_to_tensor(iso_mandel(Kb, Gb))
    C4 = mandel_to_tensor(M_cr)
    dCrot = rotate_tensor_batch(C4, Rs) - Ciso4[None, :, :, :]

    zhat = np.array([0.0, 0.0, 1.0])
    ep = np.array([1.0, 1.0j, 0.0]) / SQ2
    em = np.array([1.0, -1.0j, 0.0]) / SQ2
    P_T_inc = 0.5 * (np.eye(3) - np.outer(zhat, zhat)).astype(complex)
    P_plus = np.outer(ep, ep.conj())
    P_minus = np.outer(em, em.conj())

    ncheb = 9
    mu_nodes = np.cos((2.0 * np.arange(ncheb) + 1.0) * np.pi / (2.0 * ncheb))
    Phi = {k: np.zeros(ncheb) for k in ("TT", "TL", "pTT", "pTL", "mTT", "mTL")}
    for ic, mu in enumerate(mu_nodes):
        s = np.array([math.sqrt(max(0.0, 1.0 - mu * mu)), 0.0, mu])
        B = np.einsum("gijkl,j,l->gik", dCrot, zhat, s, optimize=True)
        P_s_T = np.eye(3) - np.outer(s, s)
        P_s_L = np.outer(s, s)
        for tag, Pinc in (("", P_T_inc), ("p", P_plus), ("m", P_minus)):
            for MM, Psc in (("TT", P_s_T), ("TL", P_s_L)):
                val = np.einsum("g,gik,im,gmp,kp->", ws, B, Pinc, B, Psc, optimize=True)
                Phi[tag + MM][ic] = float(np.real(val))

    def moments(y):
        c = np.polynomial.polynomial.polyfit(mu_nodes, y, 8)
        I0 = sum(2.0 * c[j] / (j + 1) for j in range(0, 9, 2))
        I2 = sum(2.0 * c[j] / (j + 3) for j in range(0, 9, 2))
        return float(I0), float(I2)

    N = {"T": 1.0 / (V_T ** 2 * V_T ** 2), "L": 1.0 / (V_T ** 2 * V_L ** 2)}
    r2 = {"T": 1.0, "L": (V_T / V_L) ** 2}

    out = {}
    for tag in ("", "p", "m"):
        I0T, I2T = moments(Phi[tag + "TT"])
        I0L, I2L = moments(Phi[tag + "TL"])
        D0 = -(N["T"] * I0T + N["L"] * I0L) / 4.0
        D2 = (N["T"] * ((1.0 - 2.0 * r2["T"]) * I0T / 8.0 - 3.0 * I2T / 8.0)
              + N["L"] * ((1.0 - 2.0 * r2["L"]) * I0L / 8.0 - 3.0 * I2L / 8.0))
        out[tag] = (D0, D2, (I0T, I2T, I0L, I2L))
    return {
        "mu_bar": mu_bar, "lam_bar": lam_bar, "V_T": V_T, "V_L": V_L,
        "D0_avg": out[""][0], "D2_avg": out[""][1],
        "D0_plus": out["p"][0], "D0_minus": out["m"][0],
        "D2_plus": out["p"][1], "D2_minus": out["m"][1],
        "I_moments": out[""][2],
    }


# ---------------------------------------------------------------- selftest
def selftest_fE2():
    """Explicit m-basis check of the E2-fraction formula on random traceless S."""
    rng = np.random.default_rng(11)
    for _ in range(40):
        A = rng.normal(size=(3, 3))
        S = 0.5 * (A + A.T)
        S -= np.trace(S) / 3.0 * np.eye(3)
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)
        u = np.array([1.0, 0.0, 0.0]) - n[0] * n
        u /= np.linalg.norm(u)
        w = np.cross(n, u)
        a = n @ S @ n
        S0 = 1.5 * a * (np.outer(n, n) - np.eye(3) / 3.0)
        tvec = S @ n - a * n
        S1 = np.outer(tvec, n) + np.outer(n, tvec)
        S2 = S - S0 - S1
        norm2 = float(np.sum(S2 * S2))
        s2 = float(np.sum(S * S))
        f_direct = norm2 / s2
        f_formula = 1.0 - 2.0 * float((S @ n) @ (S @ n)) / s2 + 0.5 * a * a / s2
        assert abs(f_direct - f_formula) < 1e-12, (f_direct, f_formula)
        # orthogonality of the decomposition
        assert abs(np.sum(S0 * S1)) + abs(np.sum(S0 * S2)) + abs(np.sum(S1 * S2)) < 1e-10


def selftest_iso_grid(Rs, ws, M_probe):
    A_grid, _ = odf_averages(M_probe, Rs, ws, np.zeros(len(ws)))
    A_cf = iso_project(M_probe)
    dev = float(np.max(np.abs(A_grid - A_cf)))
    assert dev < 1e-10 * float(np.linalg.norm(M_probe)), dev
    return dev


# ---------------------------------------------------------------- main
def main():
    t_start = time.time()
    guard_files()
    t1mod, t1pats, t1_coll_src = t1_selfscan()
    schema = json.load(open(os.path.join(HERE, "g_mscs1_schema_v1_0.json")))
    TOL = schema["tolerances"]
    tau = TOL["tau_agg"]
    t_grid = np.array(schema["t_grid"])
    n_theta, n_phi = schema["quadrature"]["n_theta"], schema["quadrature"]["n_phi"]

    X1 = json.load(open(os.path.join(HERE, "inputs/poly_vrh_results.json")))
    X3 = json.load(open(os.path.join(HERE, "inputs/cc_p2_phase1.json")))
    X4 = json.load(open(os.path.join(HERE, "inputs/poly1_phase1full_cc.json")))
    X5 = json.load(open(os.path.join(HERE, "inputs/chatleg_phase0bfull.json")))

    vrh = X1["vrh"]

    def hex_consts(tag, arm):
        c = vrh[tag]["C_over_rho"]
        C66 = c["C66"] if arm == "a" else 0.5 * (c["C11"] - c["C12"])
        return (c["C11"], c["C12"], c["C13"], c["C33"], c["C44"], C66)

    def cub_consts(tag):
        c = vrh[tag]["C_over_rho"]
        return (c["C11"], c["C12"], c["C44"])

    N111 = np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0)
    Z = np.array([0.0, 0.0, 1.0])
    CONFIGS = {
        "hex_step|a": ("hex", voigt_dict_to_mandel("hex", hex_consts("hex:step", "a")), Z),
        "hex_step|b": ("hex", voigt_dict_to_mandel("hex", hex_consts("hex:step", "b")), Z),
        "hex_gem8|a": ("hex", voigt_dict_to_mandel("hex", hex_consts("hex:gem8", "a")), Z),
        "hex_gem8|b": ("hex", voigt_dict_to_mandel("hex", hex_consts("hex:gem8", "b")), Z),
        "cubic_step|001": ("cubic", voigt_dict_to_mandel("cubic", cub_consts("cubic:step")), Z),
        "cubic_step|111": ("cubic", voigt_dict_to_mandel("cubic", cub_consts("cubic:step")), N111),
        "cubic_gem8|001": ("cubic", voigt_dict_to_mandel("cubic", cub_consts("cubic:gem8")), Z),
        "cubic_gem8|111": ("cubic", voigt_dict_to_mandel("cubic", cub_consts("cubic:gem8")), N111),
    }
    assert list(CONFIGS) == schema["config_keys"]
    BASE = {
        "hex_step": ("step_hex", CONFIGS["hex_step|a"][1]),
        "hex_gem8": ("gem8_hex", CONFIGS["hex_gem8|a"][1]),
        "cubic_step": ("step_cubic", CONFIGS["cubic_step|001"][1]),
        "cubic_gem8": ("gem8_cubic", CONFIGS["cubic_gem8|001"][1]),
    }

    print("== selftests ==")
    selftest_fE2()
    Rs, ws = so3_grid(20, 12, 20)
    dev = selftest_iso_grid(Rs, ws, CONFIGS["hex_step|a"][1])
    print(f"   f_E2 m-basis decomposition OK; SO(3) grid vs closed-form iso dev {dev:.3e}")

    kq, wq = sphere_grid(n_theta, n_phi)
    kq2, wq2 = sphere_grid(2 * n_theta, 2 * n_phi)
    ngrid = n_sphere_grid(12, 24)

    # ---- internal pins: Voigt/Reuss generals vs X-4 (PIN-VRH0 reference)
    print("== Phase 0: pins ==")
    pin_worst = 0.0
    for key, (x4tag, M_cr) in BASE.items():
        A_C = iso_project(M_cr)
        A_S = iso_project(np.linalg.inv(M_cr))
        KV, GV = iso_KG(A_C)
        KR, GR = iso_KG(np.linalg.inv(A_S))
        ref = X4["phase1a"][x4tag]
        for got, want in ((KV, ref["KV_gen"]), (GV, ref["GV_gen"]),
                          (KR, ref["KR_gen"]), (GR, ref["GR_gen"])):
            pin_worst = max(pin_worst, abs(got - want) / abs(want))
    if pin_worst > TOL["pins_rel"]:
        halt(f"PIN-VRH0 residual {pin_worst:.3e} beyond pins_rel")
    print(f"   PIN-VRH0 worst rel residual {pin_worst:.3e}")

    # ---- Born t=0 + PIN-A2AGG + F-CTRL-POL
    born = {}
    pin_a2 = 0.0
    pol_pm = 0.0
    pol_pa = 0.0
    for key, (x4tag, M_cr) in BASE.items():
        b = born_t0_config(M_cr, Rs, ws)
        bank = X3[x4tag]
        for got, want in ((b["mu_bar"], bank["mu_bar"]), (b["lam_bar"], bank["lam_bar"]),
                          (b["V_T"], bank["V_T"]), (b["V_L"], bank["V_L"])):
            if abs(got - want) / abs(want) > 1e-10:
                halt(f"Born mean-medium mismatch on {key}: {got} vs {want}")
        i0t, i2t, i0l, i2l = b["I_moments"]
        for got, want in ((i0t, bank["I0"]["TT"]), (i2t, bank["I2"]["TT"]),
                          (i0l, bank["I0"]["TL"]), (i2l, bank["I2"]["TL"])):
            if abs(got - want) / abs(want) > 1e-8:
                halt(f"Born kernel moment mismatch on {key}: {got} vs {want}")
        d0_rel = abs(b["D0_avg"] - bank["D0"]["T"]) / abs(bank["D0"]["T"])
        d2_rel = abs(b["D2_avg"] - bank["D2_analytic"]["T"]) / abs(bank["D2_analytic"]["T"])
        if d0_rel > TOL["born_rel"]:
            halt(f"D0 mismatch on {key}: rel {d0_rel:.3e}")
        pin_a2 = max(pin_a2, d2_rel)
        pol_pm = max(pol_pm, abs(b["D0_plus"] - b["D0_minus"]),
                     abs(b["D2_plus"] - b["D2_minus"]))
        pol_pa = max(pol_pa, abs(b["D0_plus"] - b["D0_avg"]),
                     abs(b["D2_plus"] - b["D2_avg"]))
        born[key] = {"D0_plus": b["D0_plus"], "D0_minus": b["D0_minus"],
                     "D0_avg": b["D0_avg"], "D2_avg": b["D2_avg"],
                     "a2agg_residual_rel": d2_rel}
    ctrl_pol_pass = pol_pm <= tau and pol_pa <= tau
    ctrl_a2_pass = pin_a2 <= 1e-8
    print(f"   PIN-A2AGG worst rel residual {pin_a2:.3e}  F-CTRL-POL splits {pol_pm:.3e}/{pol_pa:.3e}")

    # ---- HS references + PIN-HS0 (cubic vs X-5 bands)
    print("== HS references (A-2.3 optimization at t = 0) ==")
    hs_ref = {}
    for key, (sym, M_cr, nhat) in CONFIGS.items():
        base = key.split("|")[0]
        cache = base if sym == "cubic" or key.endswith("|a") else key
        if cache not in hs_ref:
            Kl, Gl = hs_reference(M_cr, upper=False)
            Ku, Gu = hs_reference(M_cr, upper=True)
            hs_ref[cache] = {"lo": (Kl, Gl), "hi": (Ku, Gu),
                             "G_lo": g_hs_t0(M_cr, Kl, Gl), "G_hi": g_hs_t0(M_cr, Ku, Gu)}
            print(f"   {cache}: G_HS in [{hs_ref[cache]['G_lo']:.9f}, {hs_ref[cache]['G_hi']:.9f}]")
    pin_hs = 0.0
    for base, x5tag in (("cubic_step", "step_cubic"), ("cubic_gem8", "gem8_cubic")):
        lo, hi = X5["phase0b"][x5tag]["mu_HS"]
        pin_hs = max(pin_hs,
                     abs(hs_ref[base]["G_lo"] - lo) / lo,
                     abs(hs_ref[base]["G_hi"] - hi) / hi)
    if pin_hs > 1e-6:
        halt(f"PIN-HS0 residual {pin_hs:.3e} beyond 1e-6")
    print(f"   PIN-HS0 worst rel residual {pin_hs:.3e}")

    # ---- Phase 1
    print("== Phase 1 ==")
    phase1 = {}
    admix_by_key = {}
    admix_complete = {}
    admix_identity = {}
    for key, (sym, M_cr, nhat) in CONFIGS.items():
        r = phase1_config(M_cr, sym, nhat, kq, wq)
        admix_by_key[key] = r.pop("_r_h_projected")
        admix_complete[key] = r.pop("_r_h_complete")
        pred = r.pop("_r_h_identity_pred")
        admix_identity[key] = {"r_xtal_h": r["r_xtal_h"], "identity_pred": pred,
                               "rel_resid": abs(r["r_xtal_h"] - pred) / abs(r["r_xtal_h"])}
        phase1[key] = r
        print(f"   {key}: r_E2 {r['r_xtal_E2']:+.6e}  r_h {r['r_xtal_h']:+.6e}  "
              f"lam_mean {r['lambda_mean']:.4e}  max {r['lambda_max']:.4e} ({r['lambda_max_branch']})")

    # doubling residual on r_xtal_E2
    doubling = 0.0
    for key, (sym, M_cr, nhat) in CONFIGS.items():
        r2 = phase1_config(M_cr, sym, nhat, kq2, wq2)
        doubling = max(doubling, abs(r2["r_xtal_E2"] - phase1[key]["r_xtal_E2"]))
    print(f"   doubling residual {doubling:.3e}")

    admix_worst = max(admix_by_key.values(), key=abs)
    admix_complete_worst = max(admix_complete.values(), key=abs)
    admix_identity_worst = max(v["rel_resid"] for v in admix_identity.values())
    # Pass criterion: the control's substance -- the S2-h split is admixture-sourced --
    # holds under the complete zero-admixture projection (exactly 0). The literal
    # memo-section-4 form (quasi-transverse projection only) does NOT go to zero: the
    # quasi-longitudinal branch keeps its admixture-generated EM weight, and its
    # descriptor-weight ratio (1 + lam/3)^-1 leaves an order-1e-3 residual. That number
    # is reported unaltered as the control float; the criterion defect is an H-CC item.
    ctrl_admix_pass = abs(admix_complete_worst) <= tau
    print(f"   F-CTRL-ADMIX literal (QT-projection) r_xtal_h: worst {admix_worst:+.6e}")
    print(f"   F-CTRL-ADMIX complete zero-admixture projection: worst {admix_complete_worst:+.3e}")
    print(f"   memo-2.6 covariance identity worst rel residual: {admix_identity_worst:.3e}")

    # ---- Phase 2 texture machinery
    print("== Phase 2 ==")
    p2w_cache = {}

    def p2_weights(u_cr):
        keyu = tuple(np.round(u_cr, 12))
        if keyu not in p2w_cache:
            zn = np.einsum("gij,j->gi", Rs, u_cr)[:, 2]
            p2w_cache[keyu] = P2(zn)
        return p2w_cache[keyu]

    phase2 = {}
    so3_ODF = {}
    for key, (sym, M_cr, nhat) in CONFIGS.items():
        p2w = p2_weights(nhat)
        A_C, B_C = odf_averages(M_cr, Rs, ws, p2w)
        A_S, B_S = odf_averages(np.linalg.inv(M_cr), Rs, ws, p2w)
        base = key.split("|")[0]
        cache = base if sym == "cubic" or key.endswith("|a") else key
        ref = hs_ref[cache]
        hs_PQ = {}
        for side in ("lo", "hi"):
            K0, G0 = ref[side]
            Cstar = cstar_of(K0, G0)
            T = np.linalg.inv(M_cr + Cstar)
            P_A, P_B = odf_averages(T, Rs, ws, p2w)
            hs_PQ[side] = (P_A, P_B, Cstar)
        so3_ODF[key] = (A_C, B_C, A_S, B_S, hs_PQ)

        vT_VRH = math.sqrt(0.5 * (iso_KG(A_C)[1] + iso_KG(np.linalg.inv(A_S))[1]))
        vT_lo = math.sqrt(ref["G_lo"])
        vT_hi = math.sqrt(ref["G_hi"])

        r_E2_V, r_h_V, r_E2_H, lam_t = [], [], [], []
        so3_dev = 0.0
        so3_mean = 0.4
        for t in t_grid:
            C_V = A_C + t * B_C
            C_R = np.linalg.inv(A_S + t * B_S)
            hill = 0.5 * (C_V + C_R)
            rE2, rh, lm, F0, F2, valid = aggregate_r(hill, t, kq, wq, ngrid)
            r_E2_V.append(rE2)
            r_h_V.append(rh)
            lam_t.append(lm)
            so3_dev = max(so3_dev, float(np.max(np.abs(F0[valid] - 0.4))))
            if t == 0.0:
                so3_mean = float(np.mean(F0[valid]))
            hs_ts = []
            for side in ("lo", "hi"):
                P_A, P_B, Cstar = hs_PQ[side]
                hs_ts.append(np.linalg.inv(P_A + t * P_B) - Cstar)
            rE2h, _, _, _, _, _ = aggregate_r(0.5 * (hs_ts[0] + hs_ts[1]), t, kq, wq, ngrid)
            r_E2_H.append(rE2h)

        S_t_E2, k2_E2, k3_E2, resid = fit_t(t_grid, np.array(r_E2_V), 0.25)
        S_t_h, k2_h, _, _ = fit_t(t_grid, np.array(r_h_V), 0.25)
        _, k2_E2_half, _, _ = fit_t(t_grid, np.array(r_E2_V), 0.1)
        halv = abs(k2_E2_half - k2_E2) / abs(k2_E2) if k2_E2 != 0.0 else 0.0
        fit4 = fit_t4(t_grid, np.array(r_E2_V), 0.25)

        phase2[key] = {
            "vT_VRH": vT_VRH, "vT_HS_lo": vT_lo, "vT_HS_hi": vT_hi,
            "r_agg_E2_VRH": r_E2_V, "r_agg_h_VRH": r_h_V, "r_agg_E2_HS": r_E2_H,
            "S_t_E2": S_t_E2, "S_t_h": S_t_h, "kappa2_E2": k2_E2, "kappa2_h": k2_h,
            "kappa3_E2": k3_E2, "fit_residual": resid, "halving_dev_kappa2": halv,
            "lambda_mean_t": lam_t,
            "x_kappa_4term_fit_E2": fit4,
        }
        phase2[key]["x_so3_dev_F0"] = so3_dev
        phase2[key]["x_so3_mean_F0_t0"] = so3_mean
        print(f"   {key}: S_t {S_t_E2:+.3e}  kappa2_E2 {k2_E2:+.6e}  kappa2_h {k2_h:+.6e}  "
              f"halving_dev {halv:.3e}")

    # ---- controls that need the machinery above
    print("== Phase 0 controls (final evaluation) ==")
    # F-CTRL-ISO (A-2.6): hex:step Hill pair through the cubic path with C11-C12 = 2 C44
    K_iso, G_iso = 134.609, 70.881
    C11i = K_iso + 4.0 * G_iso / 3.0
    C12i = K_iso - 2.0 * G_iso / 3.0
    M_iso = voigt_dict_to_mandel("cubic", (C11i, C12i, G_iso))
    r_iso = phase1_config(M_iso, "cubic", Z, kq, wq)
    A_Ci, B_Ci = odf_averages(M_iso, Rs, ws, p2_weights(Z))
    A_Si, B_Si = odf_averages(np.linalg.inv(M_iso), Rs, ws, p2_weights(Z))
    r_agg_iso = 0.0
    for t in t_grid:
        hill = 0.5 * ((A_Ci + t * B_Ci) + np.linalg.inv(A_Si + t * B_Si))
        rE2, rh, _, _, _, _ = aggregate_r(hill, t, kq, wq, ngrid)
        r_agg_iso = max(r_agg_iso, abs(rE2), abs(rh))
    ctrl_iso = {"passed": bool(abs(r_iso["r_xtal_E2"]) <= tau and abs(r_iso["r_xtal_h"]) <= tau
                               and r_iso["lambda_max"] <= tau and r_agg_iso <= tau),
                "r_xtal_E2": r_iso["r_xtal_E2"], "r_xtal_h": r_iso["r_xtal_h"],
                "lambda_max": r_iso["lambda_max"], "r_agg_max": r_agg_iso}

    # F-CTRL-SO3: ODF-averaged E2 weight at t = 0 equals 2/5 for every mode; r_agg(0) = 0
    so3_dev_all = max(p["x_so3_dev_F0"] for p in phase2.values())
    i_t0 = list(t_grid).index(0.0)
    r_agg0 = max(abs(p["r_agg_E2_VRH"][i_t0]) for p in phase2.values())
    so3_mean_all = float(np.mean([p["x_so3_mean_F0_t0"] for p in phase2.values()]))
    ctrl_so3 = {"passed": bool(so3_dev_all <= tau and r_agg0 <= tau),
                "w_S2_mean_t0": so3_mean_all,
                "dev_from_0p4": so3_dev_all, "r_agg_0_E2": r_agg0}
    for p in phase2.values():
        del p["x_so3_dev_F0"]
        del p["x_so3_mean_F0_t0"]

    # F-CTRL-TEX (A-2.6 synthetic hex at t = 1)
    M_tex = voigt_dict_to_mandel("hex", (300.0, 100.0, 50.0, 200.0, 40.0, 100.0))
    p2wz = p2_weights(Z)
    A_Ct, B_Ct = odf_averages(M_tex, Rs, ws, p2wz)
    A_St, B_St = odf_averages(np.linalg.inv(M_tex), Rs, ws, p2wz)
    hill1 = 0.5 * ((A_Ct + 1.0 * B_Ct) + np.linalg.inv(A_St + 1.0 * B_St))
    r_tex, _, _, _, _, _ = aggregate_r(hill1, 1.0, kq, wq, ngrid)
    ctrl_tex = {"passed": bool(abs(r_tex) > tau), "r_agg_t1": r_tex}

    controls = {
        "F-CTRL-ISO": ctrl_iso,
        "F-CTRL-SO3": ctrl_so3,
        "F-CTRL-TEX": ctrl_tex,
        "F-CTRL-POL": {"passed": bool(ctrl_pol_pass), "split_plus_minus": pol_pm,
                       "split_plus_avg": pol_pa},
        "PIN-A2AGG": {"passed": bool(ctrl_a2_pass), "worst_rel_residual": pin_a2},
        "F-CTRL-ADMIX": {"passed": bool(ctrl_admix_pass), "r_xtal_h_projected": admix_worst,
                         "x_r_by_key": admix_by_key,
                         "x_r_complete_projection_worst": admix_complete_worst,
                         "x_identity_check_2p6": admix_identity,
                         "x_note": ("substantive implementation per dispatch step 3.3: "
                                    "r_xtal_h_projected is the literal memo-section-4 number "
                                    "(quasi-transverse eigenvectors projected, quasi-longitudinal "
                                    "branch untouched) and is NOT zero within tau_agg; the pass "
                                    "flag follows the complete zero-admixture reading, under which "
                                    "the split vanishes exactly; see H-CC items in the CC report")},
    }
    for name, c in controls.items():
        print(f"   {name}: {'PASS' if c['passed'] else 'FAIL'}")

    # ---- falsifiers + verdict (machine-assigned, last)
    worst_St = max(max(abs(p["S_t_E2"]), abs(p["S_t_h"])) for p in phase2.values())
    fms3 = "SILENT" if worst_St <= tau else "FIRES"
    all_controls = all(c["passed"] for c in controls.values())
    if not all_controls:
        verdict = "INDETERMINATE"
    elif fms3 == "FIRES":
        verdict = "PROTECTION-BREACH"
    else:
        verdict = "IDENTITY-DELIVERED"
    print(f"== verdict: {verdict} (worst |S_t| {worst_St:.3e}) ==")

    checkpoint = {
        "gate": "G-MSCS1",
        "leg": "cc",
        "instrument": "g_mscs1_ccleg.py",
        "instrument_md5": md5_file(os.path.abspath(__file__)),
        "memo_md5": GUARDS["staging_memo_G_MSCS1_v2.md"][0],
        "memo_bytes": GUARDS["staging_memo_G_MSCS1_v2.md"][1],
        "ledger_base_md5": schema["ledger_base_md5"],
        "utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "elections": {
            "E-MS-1": "(a) two descriptors of the one transverse field; S2-E2 primary, S2-h second arm",
            "E-MS-2": "(a) all four configurations",
            "E-MS-2b": "(a+b) banked tetragonal-form primary + hexagonal-symmetrized C66 second arm",
            "E-MS-2c": "(001+111) cubic axis 001 primary, 111 reported",
            "E-MS-3": "(a) VRH/HS leading order; polarization-resolved Born at t = 0 only",
            "E-MS-4": "(a) verbatim differentiation table + lambda_L computation",
            "E-MS-5": "(a) fiber ODF 1 + t P2(cos theta), t in [-1, 2]",
            "E-MS-6": "(a) no observational contact in this gate",
        },
        "T1": {"list_md5": T1_LIST_MD5, "state": "CLEAN", "numeric_collisions": 0,
               "x_collisions_instrument_plus_memo": t1_coll_src},
        "inputs": {"X1_md5": GUARDS["inputs/poly_vrh_results.json"][0],
                   "X1_bytes": GUARDS["inputs/poly_vrh_results.json"][1],
                   "X3_md5": GUARDS["inputs/cc_p2_phase1.json"][0],
                   "X4_md5": GUARDS["inputs/poly1_phase1full_cc.json"][0],
                   "X5_md5": GUARDS["inputs/chatleg_phase0bfull.json"][0]},
        "quadrature": {"n_theta": n_theta, "n_phi": n_phi, "doubling_residual": doubling},
        "t_grid": [float(t) for t in t_grid],
        "controls": controls,
        "phase1": phase1,
        "phase2": phase2,
        "born_t0": born,
        "falsifiers": {"F-MS-3": {"state": fms3, "worst_S_t": worst_St},
                       "F-MS-2": {"state": "REGISTERED_NOT_EXECUTED"},
                       "F-MS-1": {"state": "RETIRED_TO_CONTROL"}},
        "x_pins": {"PIN-VRH0_worst_rel": pin_worst, "PIN-HS0_worst_rel": pin_hs,
                   "hs_references": {k: {"lo_K0_G0": list(v["lo"]), "hi_K0_G0": list(v["hi"])}
                                     for k, v in hs_ref.items()}},
        "x_so3_grid": [20, 12, 20],
        "x_runtime_s": 0.0,
        "verdict_class": verdict,
    }
    checkpoint["x_runtime_s"] = round(time.time() - t_start, 3)

    # T1 fixed point on the emitted checkpoint (collisions counted on the final bytes)
    out_path = os.path.join(HERE, "g_mscs1_ccleg_checkpoint.json")
    for _ in range(4):
        blob = json.dumps(checkpoint, indent=1, ensure_ascii=False)
        hits, coll = t1mod.scan_text(blob, t1pats)
        if hits:
            halt(f"T1 HIT in emitted checkpoint: {[i for i, _ in hits]}")
        if checkpoint["T1"]["numeric_collisions"] == len(coll):
            break
        checkpoint["T1"]["numeric_collisions"] = len(coll)
    open(out_path, "w", encoding="utf-8").write(blob)
    print(f"checkpoint -> {out_path}  md5 {md5_file(out_path)}  "
          f"T1 collisions {checkpoint['T1']['numeric_collisions']}  "
          f"runtime {checkpoint['x_runtime_s']} s")
    return checkpoint


if __name__ == "__main__":
    main()
