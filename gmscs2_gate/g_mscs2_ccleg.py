#!/usr/bin/env python3
"""g_mscs2_ccleg.py -- Gate G-MSCS2, CC leg instrument (blind build).

Built from staging_memo_G_MSCS2_v2.md (efdcabdc), G_MSCS2_LOCK_RECORD.md Addendum A-2
(49232d4c) with Addendum A-3 in force (activation flag "ACTIVATE: G-MSCS2-CC-LEG-1 WITH-A3"),
and g_mscs2_schema_v1_0.json (66f586d7) ONLY, before any quarantined chat artifact was
decoded. The G-MSCS1 instruments on main were read for the inherited descriptor definitions
(memo 2.2-2.4), not copied.

Method variation (lock record section 3; dispatch section 0):
  * SO(3) averages by the FIBER-AXIS ROUTE, not a ZYZ Euler product grid. Every ODF of this
    gate is a function of the fiber axis expressed in the crystal frame, n = g^-1 z. Writing
    g = R_z(psi) g0(n) with g0(n) n = z, the psi-average (the SO(2) coset average about the
    sample fiber axis) is done ANALYTICALLY: for rank-4 tensors it is the orthogonal
    projection onto the five-dimensional transversely-isotropic subspace (Mandel inner
    product); for the per-grain E2 weight it is the closed-form circular moment of a degree-4
    polynomial in the descriptor axis, which leaves a polynomial a0 + a2 x^2 + a4 x^4 in
    x = n_c . n (n_c the descriptor axis in the crystal frame). What remains is an S^2
    integral over n, done with Gauss-Legendre(cos theta) 16 x uniform phi 32 on a generically
    rotated node set (exact for polynomial degree <= 31 in n; the gate needs >= 12). A
    12-point uniform psi average is kept only as a selftest of the analytic projection.
  * The E2 fraction about an axis n is evaluated in the factorized closed form
    frac_E2 = (1 - (k.n)^2) (1 - (e_perp_hat . n)^2), derived from the m = +-2 projection
    formula of memo 2.2 (selftested against that formula).
  * Own HS reference optimizer (boundary-K0 bisection + nested grid refinement over G0),
    own branch labelling, own fits, own checkpoint layout.

Halt discipline: md5 + byte guards on the memo, the lock record, the schema, the T1 list, the
scanner, X-1 and both X-6 files before any computation; T1 self-scan (this file + the memo) at
every invocation with the frozen scanner rule; any hit halts (no override flag exists); any
Phase-0 pin/control failure -> INDETERMINATE by the schema rule (Phase 2 still computed and
written so the failure can be diagnosed, but the verdict says INDETERMINATE).

Addendum A-3 (in force):
  A-3.1 F-CTRL-L2NULL: the pure l = 2 clause covers the three tensors and r_agg; the mixed
        (t2, t4) clause covers the three tensors only; the mixed r_agg change is the reported
        diagnostic mixed_r_agg_change_A29 per cubic key.
  A-3.2 kappa24_richardson per key (h = 0.02, Richardson-extrapolated central cross
        difference) alongside the 7-term quadform.
  A-3.3 CC-DD reading for the cubic (t2, t4) form: (i) the INHERITED DESCRIPTOR-AXIS P2
        (the l = 2 family exactly as A-2.2 defines it, w = 1 + t2 P2(n_c . n)); the
        O_h-symmetrized reading (ii) is reported in extras for the record.
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
ACTIVATION_FLAG = "ACTIVATE: G-MSCS2-CC-LEG-1 WITH-A3"
A3_IN_FORCE = True

GUARDS = {
    "staging_memo_G_MSCS2_v2.md": ("efdcabdcd937cda4acb64f941dc4bb2b", 46053),
    "G_MSCS2_LOCK_RECORD.md": ("49232d4c42061c4536867eba14aae501", 11804),
    "g_mscs2_schema_v1_0.json": ("66f586d7b6c5e8228394222ddfda73f2", 5800),
    "tools/t1/T1_forbidden_G_MSCS2.txt": ("be921b8c29f7578e85ed92f1450c1956", 1695),
    "tools/t1/t1_scan.py": ("6b86290090a8c84f1b1a0a99ec0bf697", 1967),
    "inputs/poly_vrh_results.json": ("200e7a8b775577564369c6924d38a84c", 2767),
    "inputs/g_mscs1_chatleg_checkpoint.json": ("c04c0b8ea34cfe60f231aa06828e6ce4", 33289),
    "inputs/g_mscs1_ccleg_checkpoint.json": ("249e11dd53c4cb82f302b15d3c94c337", 24415),
}
MEMO = "staging_memo_G_MSCS2_v2.md"
T1_LIST = "tools/t1/T1_forbidden_G_MSCS2.txt"
T1_SCANNER = "tools/t1/t1_scan.py"

KEYS = ["hex_step|a", "hex_step|b", "hex_gem8|a", "hex_gem8|b",
        "cubic_step|001", "cubic_step|111", "cubic_gem8|001", "cubic_gem8|111"]
X6_CFG = {"hex_step": "step_hex", "hex_gem8": "gem8_hex",
          "cubic_step": "step_cubic", "cubic_gem8": "gem8_cubic"}
T4_GRID = np.array([-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0])
T2T4_GRID = np.array([-0.25, -0.125, 0.0, 0.125, 0.25])
ZHAT = np.array([0.0, 0.0, 1.0])
XHAT = np.array([1.0, 0.0, 0.0])
YHAT = np.array([0.0, 1.0, 0.0])
N111 = np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0)
SQ2 = math.sqrt(2.0)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_file(p):
    return md5_bytes(open(p, "rb").read())


def halt(msg):
    print("HALT: " + msg)
    sys.exit(1)


# ---------------------------------------------------------------- guards + T1
def guard_files():
    for rel, (want, nbytes) in GUARDS.items():
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            halt(f"guarded file missing: {rel}")
        b = open(p, "rb").read()
        got = md5_bytes(b)
        if got != want or len(b) != nbytes:
            halt(f"guard mismatch on {rel}: md5 {got} bytes {len(b)}")


def t1_load():
    """Load the frozen scanner module (md5-guarded above) and the gate list."""
    spec = importlib.util.spec_from_file_location("t1_scan", os.path.join(HERE, T1_SCANNER))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pats = mod.load(os.path.join(HERE, T1_LIST))
    if len(pats) != 36:
        halt(f"T1 gate list has {len(pats)} patterns, expected 36")
    return mod, pats


def t1_selfscan(mod, pats):
    out = {}
    for label, f in (("instrument", os.path.abspath(__file__)), ("memo", os.path.join(HERE, MEMO))):
        text = open(f, "rb").read().decode("utf-8", "replace")
        hits, coll = mod.scan_text(text, pats)
        if hits:
            halt(f"T1 HIT in {label}: pattern indices {[i for i, _ in hits]}")
        out[label] = "CLEAN"
        out[f"numeric_collisions_{label}"] = len(coll)
    return out


# ---------------------------------------------------------------- Mandel algebra
PAIRS = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
MF = np.array([1.0, 1.0, 1.0, SQ2, SQ2, SQ2])
MFF = np.outer(MF, MF)
_m6 = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
J6 = np.outer(_m6, _m6) / 3.0
KD6 = np.eye(6) - J6
# Mandel basis tensors E_B (symmetric 3x3 with unit Mandel component B)
EB = np.zeros((6, 3, 3))
for _b, (_i, _j) in enumerate(PAIRS):
    EB[_b, _i, _j] = EB[_b, _j, _i] = 1.0 / MF[_b]


def voigt_to_mandel(Cv):
    return np.asarray(Cv, dtype=float) * MFF


def mandel_to_voigt(M):
    return M / MFF


def sym2_to_mandel(S):
    """symmetric 3x3 (..., 3, 3) -> Mandel vector (..., 6)."""
    return np.stack([S[..., i, j] * MF[b] for b, (i, j) in enumerate(PAIRS)], axis=-1)


def mandel_to_full(M):
    Cv = mandel_to_voigt(M)
    C = np.zeros((3, 3, 3, 3))
    for a, (i, j) in enumerate(PAIRS):
        for b, (k, l) in enumerate(PAIRS):
            C[i, j, k, l] = C[j, i, k, l] = C[i, j, l, k] = C[j, i, l, k] = Cv[a, b]
    return C


def full_to_mandel(C):
    M = np.zeros((6, 6))
    for a, (i, j) in enumerate(PAIRS):
        for b, (k, l) in enumerate(PAIRS):
            M[a, b] = MF[a] * MF[b] * C[i, j, k, l]
    return M


def iso_KG(M):
    """Bulk and shear modulus of the isotropic (uniform-SO(3)) projection of M."""
    K = float(M[:3, :3].sum()) / 9.0
    G = (float(np.trace(M)) - 3.0 * K) / 10.0
    return K, G


def iso_M(K, G):
    return 3.0 * K * J6 + 2.0 * G * KD6


def iso_project(M):
    return iso_M(*iso_KG(M))


def hex_voigt(C11, C12, C13, C33, C44, C66):
    Cv = np.zeros((6, 6))
    Cv[0, 0] = Cv[1, 1] = C11
    Cv[2, 2] = C33
    Cv[0, 1] = Cv[1, 0] = C12
    Cv[0, 2] = Cv[2, 0] = Cv[1, 2] = Cv[2, 1] = C13
    Cv[3, 3] = Cv[4, 4] = C44
    Cv[5, 5] = C66
    return Cv


def cubic_voigt(C11, C12, C44):
    Cv = np.zeros((6, 6))
    for i in range(3):
        Cv[i, i] = C11
        for j in range(3):
            if i != j:
                Cv[i, j] = C12
    Cv[3, 3] = Cv[4, 4] = Cv[5, 5] = C44
    return Cv


def mandel_rotation(g):
    """6x6 orthogonal Mandel rotation matrices for a batch of 3x3 rotations g (..., 3, 3):
    column B = Mandel vector of g E_B g^T."""
    rotE = np.einsum("...ik,bkl,...jl->...bij", g, EB, g)
    Q = sym2_to_mandel(rotE)           # (..., 6 [B], 6 [A])
    return np.swapaxes(Q, -1, -2)      # (..., A, B)


def rotate_mandel(M, g):
    Q = mandel_rotation(g)
    return np.einsum("...ab,bc,...dc->...ad", Q, M, Q)


def rot_z(psi):
    c, s = math.cos(psi), math.sin(psi)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def rot_axis_angle(axis, ang):
    a = np.asarray(axis, dtype=float)
    a = a / np.linalg.norm(a)
    Kx = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * Kx + (1.0 - math.cos(ang)) * (Kx @ Kx)


def g0_to_z(n):
    """A rotation taking the unit vector n to z (any representative of the coset)."""
    nz = float(np.clip(n[2], -1.0, 1.0))
    axis = np.cross(n, ZHAT)
    s = np.linalg.norm(axis)
    if s < 1e-14:
        return np.eye(3) if nz > 0 else rot_axis_angle(XHAT, math.pi)
    return rot_axis_angle(axis / s, math.acos(nz))


# ---------------------------------------------------------------- TI projector (analytic SO(2) average)
def ti_projector():
    """Orthogonal projector (36x36, Mandel-flattened) onto the transversely-isotropic
    (about z) subspace = the SO(2)_z-fixed subspace of elasticity tensors."""
    basis = []
    for p in range(5):
        c = np.zeros(5)
        c[p] = 1.0
        C11, C12, C13, C33, C44 = c
        basis.append(voigt_to_mandel(hex_voigt(C11, C12, C13, C33, C44, 0.5 * (C11 - C12))).ravel())
    B = np.array(basis).T                       # (36, 5)
    Qb, _ = np.linalg.qr(B)
    return Qb @ Qb.T


TI_P = ti_projector()


def ti_average(Mrot):
    """Analytic SO(2)_z coset average of a batch of Mandel tensors (..., 6, 6)."""
    shp = Mrot.shape
    flat = Mrot.reshape(-1, 36) @ TI_P.T
    return flat.reshape(shp)


# ---------------------------------------------------------------- S^2 rules
def sphere_gl_uniform(n_theta, n_phi, rotation=None):
    """GL(cos theta) x uniform phi rule; weights sum to 1; optional rigid rotation of nodes."""
    x, w = np.polynomial.legendre.leggauss(n_theta)
    phi = 2.0 * np.pi * np.arange(n_phi) / n_phi
    ct = np.repeat(x, n_phi)
    st = np.sqrt(1.0 - ct * ct)
    ph = np.tile(phi, n_theta)
    pts = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=1)
    wts = np.repeat(w, n_phi) / (2.0 * n_phi)
    if rotation is not None:
        pts = pts @ rotation.T
    return pts, wts


# the fiber-axis (n) rule: generic rotation so that no node sits on a crystal symmetry axis
GEN_ROT = rot_axis_angle([0.3, -0.7, 0.55], 1.234567) @ rot_axis_angle([1.0, 0.2, -0.1], 0.789)
NFIB, WFIB = sphere_gl_uniform(16, 32, GEN_ROT)          # 512 nodes, exact to degree 31


# ---------------------------------------------------------------- ODF weight functions on n
def P2(x):
    return 1.5 * x * x - 0.5


def P4(x):
    return (35.0 * x ** 4 - 30.0 * x * x + 3.0) / 8.0


def P6(x):
    return (231.0 * x ** 6 - 315.0 * x ** 4 + 105.0 * x * x - 5.0) / 16.0


def K4_cubic(n):
    return 2.5 * (np.sum(n ** 4, axis=-1) - 0.6)


def K6_cubic_raw(n):
    return np.sum(n ** 6, axis=-1) - (15.0 / 11.0) * np.sum(n ** 4, axis=-1) + 30.0 / 77.0


_fine, _ = sphere_gl_uniform(200, 400)
K6_SCALE = float(np.max(np.abs(K6_cubic_raw(_fine))))
del _fine


def K6_cubic(n):
    return K6_cubic_raw(n) / K6_SCALE


class Config:
    """One configuration/arm key: symmetry, crystal tensor, descriptor axis, ODF family."""

    def __init__(self, key, sym, M, n_c):
        self.key, self.sym, self.M, self.n_c = key, sym, M, n_c
        self.x = NFIB @ n_c                       # n_c . n at the fiber nodes
        if sym == "hex":
            self.f2 = P2(NFIB[:, 2])
            self.f4 = P4(NFIB[:, 2])
            self.f6 = P6(NFIB[:, 2])
            self.c4 = 1.0
            self.c6 = 1.0
        else:
            self.f2 = P2(self.x)                  # inherited descriptor-axis l = 2 family (reading (i))
            self.f4 = K4_cubic(NFIB)
            self.f6 = K6_cubic(NFIB)
            self.c4 = float(K4_cubic(n_c[None, :])[0])
            self.c6 = float(K6_cubic(n_c[None, :])[0])
        self.c2 = 1.0                             # P2(n_c . n_c) = 1 on every key

    def odf(self, t2=0.0, t4=0.0, t6=0.0):
        return 1.0 + t2 * self.f2 + t4 * self.f4 + t6 * self.f6


# ---------------------------------------------------------------- fiber tables + ODF averages
G0_TAB = np.array([g0_to_z(n) for n in NFIB])           # (512, 3, 3)
Q0_TAB = mandel_rotation(G0_TAB)                        # (512, 6, 6)


def fiber_table(M):
    """T(n) = analytic psi-average of (R_z(psi) g0(n)) . M, for every fiber node n."""
    Mrot = np.einsum("nab,bc,ndc->nad", Q0_TAB, M, Q0_TAB)
    return ti_average(Mrot)


def odf_average(table, wvals):
    return np.einsum("n,nab->ab", WFIB * wvals, table)


# ---------------------------------------------------------------- k-sphere modes
def christoffel_modes(M, K):
    """Christoffel eigenmodes on directions K (Nk,3). Returns flattened per-mode arrays
    (Nk*3): v, lam, wEM, ehat (unit transverse polarization), plus per-direction (Nk,3) v."""
    C = mandel_to_full(M)
    G = np.einsum("ijkl,nj,nl->nik", C, K, K, optimize=True)
    G = 0.5 * (G + np.swapaxes(G, 1, 2))
    ev, evec = np.linalg.eigh(G)
    v = np.sqrt(np.maximum(ev, 0.0))                        # (Nk, 3) ascending
    E = np.swapaxes(evec, 1, 2)                              # (Nk, branch, comp)
    ke = np.einsum("ni,nbi->nb", K, E)
    lam = ke * ke
    eperp = E - ke[:, :, None] * K[:, None, :]
    wEM = np.einsum("nbi,nbi->nb", eperp, eperp)
    nrm = np.sqrt(np.maximum(wEM, 0.0))
    ehat = np.zeros_like(eperp)
    ok = nrm > 1e-13
    ehat[ok] = eperp[ok] / nrm[ok][:, None]
    return {"v": v, "lam": lam, "wEM": wEM, "ehat": ehat, "K": K, "E": E}


def frac_E2_fixed_axis(modes, axis):
    A = modes["K"] @ axis            # (Nk,)
    B = modes["ehat"] @ axis         # (Nk, 3)
    return (1.0 - A[:, None] ** 2) * (1.0 - B ** 2)


NHAT, WNHAT = sphere_gl_uniform(12, 24)                  # pinned descriptor-axis rule (A-2.5)
PL_NHAT = {0: np.ones(len(NHAT)), 2: P2(NHAT[:, 2]), 4: P4(NHAT[:, 2]), 6: P6(NHAT[:, 2])}


def e2_marginal_moments(modes):
    """F_l per mode (Nk, 3) for l = 0, 2, 4, 6: the P_l-weighted S^2 average over the
    descriptor axis of frac_E2, with the pinned GL 12 x 24 rule."""
    A = modes["K"] @ NHAT.T                                          # (Nk, Nn)
    B = np.einsum("nbi,mi->nbm", modes["ehat"], NHAT, optimize=True)  # (Nk, 3, Nn)
    frac = (1.0 - A[:, None, :] ** 2) * (1.0 - B ** 2)
    out = {}
    for l, pl in PL_NHAT.items():
        out[l] = frac @ (WNHAT * pl)
    return out


def e2_psi_coefficients(modes):
    """Closed-form SO(2) (psi) average of frac_E2 about a descriptor axis rotating on the cone
    of fixed z-component x: fbar = a0 + a2 x^2 + a4 x^4, per mode (Nk, 3)."""
    kz = modes["K"][:, 2][:, None] * np.ones_like(modes["lam"])
    ez = modes["ehat"][:, :, 2]
    kz2, ez2 = kz * kz, ez * ez
    A = (1.0 - kz2) * (1.0 - ez2) + 2.0 * kz2 * ez2
    B = kz2 + ez2 - 6.0 * kz2 * ez2
    a0 = 0.5 * kz2 + 0.5 * ez2 + A / 8.0
    a2 = 1.0 - 1.5 * (kz2 + ez2) - A / 4.0 + B / 2.0
    a4 = A / 8.0 - B / 2.0 + kz2 * ez2
    valid = modes["wEM"] > 1e-13
    a0[~valid] = a2[~valid] = a4[~valid] = 0.0
    return a0, a2, a4


def e2_direct_average(modes, cfg, wvals):
    """SO(3)-direct ODF average of the per-grain E2 weight (descriptor axis carried along),
    by the fiber-axis route: sum_n w(n) [a0 + a2 (n_c.n)^2 + a4 (n_c.n)^4]."""
    a0, a2, a4 = e2_psi_coefficients(modes)
    W0 = float(np.sum(WFIB * wvals))
    W2 = float(np.sum(WFIB * wvals * cfg.x ** 2))
    W4 = float(np.sum(WFIB * wvals * cfg.x ** 4))
    return a0 * W0 + a2 * W2 + a4 * W4


def descriptor_speeds(modes, wq, fbar):
    """<v>_EM, <v>_S2E2, <v>_S2h and the QT lambda statistics for one aggregate."""
    v, lam, wEM = modes["v"], modes["lam"], modes["wEM"]
    W = wq[:, None]
    wS2 = fbar * wEM
    wh = (1.0 - lam) / (1.0 + lam / 3.0)
    vEM = float(np.sum(W * wEM * v)) / float(np.sum(W * wEM))
    vS2 = float(np.sum(W * wS2 * v)) / float(np.sum(W * wS2))
    vh = float(np.sum(W * wh * v)) / float(np.sum(W * wh))
    qL = np.argmax(lam, axis=1)
    idx = np.arange(lam.shape[0])
    lam_qt = lam.copy()
    lam_qt[idx, qL] = np.nan
    lam_mean = float(np.nansum(W * lam_qt) / 2.0)
    lam_max = float(np.nanmax(lam_qt))
    return {"v_EM": vEM, "v_S2E2": vS2, "v_S2h": vh,
            "r_E2": vS2 / vEM - 1.0, "r_h": vh / vEM - 1.0,
            "lambda_mean": lam_mean, "lambda_max": lam_max}


# ---------------------------------------------------------------- HS bounds (Walpole form)
def cstar_iso(K0, G0):
    Ks = 4.0 * G0 / 3.0
    Gs = G0 * (9.0 * K0 + 8.0 * G0) / (6.0 * (K0 + 2.0 * G0))
    return iso_M(Ks, Gs)


def hs_from_P(P, Cs):
    return np.linalg.inv(P) - Cs


def G_hs_t0(M, K0, G0):
    Cs = cstar_iso(K0, G0)
    T = np.linalg.inv(M + Cs)
    return iso_KG(hs_from_P(iso_project(T), Cs))[1]


def hs_reference(M, side):
    """Isotropic reference (K0, G0) at t = 0: side 'hi' = minimal feasible majorant
    (C0 >= C_g) minimizing G_HS; side 'lo' = maximal feasible minorant maximizing G_HS."""
    K_g, G_g = iso_KG(M)
    scale = float(np.linalg.norm(M))
    sgn = 1.0 if side == "hi" else -1.0

    def feasible(K0, G0):
        return float(np.linalg.eigvalsh(sgn * (iso_M(K0, G0) - M))[0]) >= -1e-11 * scale

    def K0_boundary(G0):
        lo, hi = 1e-6 * K_g, 200.0 * K_g
        if side == "hi":
            if not feasible(hi, G0):
                return None
            if feasible(lo, G0):
                return lo
            for _ in range(200):          # smallest feasible K0
                mid = 0.5 * (lo + hi)
                if feasible(mid, G0):
                    hi = mid
                else:
                    lo = mid
            return hi
        if not feasible(lo, G0):
            return None
        if feasible(hi, G0):
            return hi
        for _ in range(200):              # largest feasible K0
            mid = 0.5 * (lo + hi)
            if feasible(mid, G0):
                lo = mid
            else:
                hi = mid
        return lo

    def objective(G0):
        K0 = K0_boundary(G0)
        if K0 is None:
            return math.inf, None
        g = G_hs_t0(M, K0, G0)
        return (g if side == "hi" else -g), K0

    grid = np.linspace(0.01 * G_g, 10.0 * G_g, 600)
    vals = np.array([objective(G0)[0] for G0 in grid])
    i = int(np.argmin(vals))
    centre, half = grid[i], grid[1] - grid[0]
    for _ in range(9):                    # nested refinement, 21 points per level
        g_grid = np.linspace(centre - half, centre + half, 21)
        v_grid = np.array([objective(G0)[0] for G0 in g_grid])
        centre = g_grid[int(np.argmin(v_grid))]
        half = g_grid[1] - g_grid[0]
    G0 = float(centre)
    _, K0 = objective(G0)
    return float(K0), G0, G_hs_t0(M, K0, G0)


# ---------------------------------------------------------------- fits
def fit_cubic_through_origin(t, r, window, inclusive=True):
    sel = (np.abs(t) <= window + 1e-12) if inclusive else (np.abs(t) < window - 1e-12)
    tt, rr = t[sel], r[sel]
    A = np.stack([tt, tt ** 2, tt ** 3], axis=1)
    c, *_ = np.linalg.lstsq(A, rr, rcond=None)
    return [float(x) for x in c], float(np.max(np.abs(A @ c - rr))), int(sel.sum())


def fit_quadform(t2, t4, r):
    A = np.stack([t2 ** 2, t2 * t4, t4 ** 2, t2 ** 3, t2 ** 2 * t4, t2 * t4 ** 2, t4 ** 3], axis=1)
    c, *_ = np.linalg.lstsq(A, r, rcond=None)
    return {"kappa22": float(c[0]), "kappa24": float(c[1]), "kappa44": float(c[2]),
            "residual": float(np.max(np.abs(A @ c - r))),
            "x_cubic_terms_discarded": [float(x) for x in c[3:]]}


# ---------------------------------------------------------------- selftests of the machinery
def selftests():
    rng = np.random.default_rng(2026)
    rep = {}
    # 1. Mandel rotation: orthogonality + agreement with the full-tensor rotation
    g = rot_axis_angle(rng.normal(size=3), 1.1)
    Q = mandel_rotation(g)
    A = rng.normal(size=(6, 6))
    M = A + A.T
    C4 = mandel_to_full(M)
    C4r = np.einsum("ia,jb,kc,ld,abcd->ijkl", g, g, g, g, C4)
    rep["mandel_rotation_dev"] = float(max(np.max(np.abs(Q @ Q.T - np.eye(6))),
                                           np.max(np.abs(rotate_mandel(M, g) - full_to_mandel(C4r)))))
    # 2. TI projector == 12-point uniform psi average, on random M
    psis = 2.0 * np.pi * np.arange(12) / 12.0
    avg = np.mean([rotate_mandel(M, rot_z(p)) for p in psis], axis=0)
    rep["ti_projector_vs_psi_average_dev"] = float(np.max(np.abs(ti_average(M[None])[0] - avg)))
    # 3. fiber rule: uniform average == closed-form isotropic projection
    tab = fiber_table(M)
    rep["fiber_rule_iso_dev"] = float(np.max(np.abs(odf_average(tab, np.ones(len(WFIB))) - iso_project(M))))
    # 4. harmonic normalizations on the fiber rule
    k4, p4, k6, p2 = K4_cubic(NFIB), P4(NFIB[:, 2]), K6_cubic(NFIB), P2(NFIB[:, 2])
    rep["K4_mean"] = float(np.sum(WFIB * k4))
    rep["K4_sq_mean_minus_4_21"] = float(np.sum(WFIB * k4 * k4) - 4.0 / 21.0)
    rep["P4_sq_mean_minus_1_9"] = float(np.sum(WFIB * p4 * p4) - 1.0 / 9.0)
    rep["K6_mean"] = float(np.sum(WFIB * k6))
    rep["K6_K4_overlap"] = float(np.sum(WFIB * k6 * k4))
    rep["P2_mean"] = float(np.sum(WFIB * p2))
    rep["K4_range"] = [float(k4.min()), float(k4.max())]
    # 5. frac_E2 closed form vs the m = +-2 projection formula of memo 2.2
    worst = 0.0
    for _ in range(200):
        k = rng.normal(size=3)
        k /= np.linalg.norm(k)
        e = rng.normal(size=3)
        e -= (e @ k) * k
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)
        S = 0.5 * (np.outer(k, e) + np.outer(e, k))
        s2 = float(np.sum(S * S))
        ref = 1.0 - 2.0 * float((S @ n) @ (S @ n)) / s2 + 0.5 * float(n @ S @ n) ** 2 / s2
        eh = e / np.linalg.norm(e)
        mine = (1.0 - float(k @ n) ** 2) * (1.0 - float(eh @ n) ** 2)
        worst = max(worst, abs(ref - mine))
    rep["fracE2_closed_form_dev"] = worst
    # 6. analytic psi moments of frac_E2 vs brute force (12-point psi) on random modes/cones
    worst = 0.0
    for _ in range(50):
        k = rng.normal(size=3)
        k /= np.linalg.norm(k)
        e = rng.normal(size=3)
        e -= (e @ k) * k
        eh = e / np.linalg.norm(e)
        x = rng.uniform(-1, 1)
        rho = math.sqrt(1 - x * x)
        m = {"K": k[None, :], "ehat": eh[None, None, :], "lam": np.zeros((1, 1)), "wEM": np.ones((1, 1))}
        a0, a2, a4 = e2_psi_coefficients(m)
        ana = float(a0[0, 0] + a2[0, 0] * x * x + a4[0, 0] * x ** 4)
        brute = np.mean([(1 - (k @ np.array([rho * math.cos(p), rho * math.sin(p), x])) ** 2)
                         * (1 - (eh @ np.array([rho * math.cos(p), rho * math.sin(p), x])) ** 2)
                         for p in psis])
        worst = max(worst, abs(ana - brute))
        worst = max(worst, abs(float(a0[0, 0] + a2[0, 0] / 3.0 + a4[0, 0] / 5.0) - 0.4))
    rep["psi_moment_closed_form_dev"] = worst
    # 7. the l = 4 harmonic tensor of z: Voigt entries of (1/3) T4(z) against the A-2.2 table
    T4 = harmonic_l4_tensor(ZHAT)
    Tv = mandel_to_voigt(full_to_mandel(T4)) / 3.0
    table = {(0, 0): 3, (1, 1): 3, (2, 2): 8, (0, 1): 1, (0, 2): -4, (1, 2): -4, (3, 3): -4, (4, 4): -4, (5, 5): 1}
    dev = 0.0
    for (a, b), val in table.items():
        dev = max(dev, abs(Tv[a, b] - val / 105.0), abs(Tv[b, a] - val / 105.0))
    for a in range(6):
        for b in range(6):
            if (a, b) not in table and (b, a) not in table:
                dev = max(dev, abs(Tv[a, b]))
    rep["T4_voigt_table_dev"] = float(dev)
    return rep


def harmonic_l4_tensor(n):
    """The l = 4 (traceless, fully symmetric) part of n x n x n x n."""
    d = np.eye(3)
    nn = np.outer(n, n)
    T = np.einsum("i,j,k,l->ijkl", n, n, n, n)
    T -= (np.einsum("ij,kl->ijkl", d, nn) + np.einsum("ik,jl->ijkl", d, nn) + np.einsum("il,jk->ijkl", d, nn)
          + np.einsum("jk,il->ijkl", d, nn) + np.einsum("jl,ik->ijkl", d, nn) + np.einsum("kl,ij->ijkl", d, nn)) / 7.0
    T += (np.einsum("ij,kl->ijkl", d, d) + np.einsum("ik,jl->ijkl", d, d) + np.einsum("il,jk->ijkl", d, d)) / 35.0
    return T


# ---------------------------------------------------------------- aggregate machinery per key
class Aggregate:
    """Textured Voigt / Reuss / Hill / HS tensors of one configuration via the fiber tables."""

    def __init__(self, cfg, hs_lo, hs_hi):
        self.cfg = cfg
        self.tabC = fiber_table(cfg.M)
        self.tabS = fiber_table(np.linalg.inv(cfg.M))
        self.hs = {}
        for side, (K0, G0, _) in (("lo", hs_lo), ("hi", hs_hi)):
            Cs = cstar_iso(K0, G0)
            self.hs[side] = (fiber_table(np.linalg.inv(cfg.M + Cs)), Cs)

    def tensors(self, wvals):
        V = odf_average(self.tabC, wvals)
        Sbar = odf_average(self.tabS, wvals)
        R = np.linalg.inv(Sbar)
        hs = {side: hs_from_P(odf_average(tab, wvals), Cs) for side, (tab, Cs) in self.hs.items()}
        return {"V": V, "Sbar": Sbar, "R": R, "Hill": 0.5 * (V + R),
                "HS_lo": hs["lo"], "HS_hi": hs["hi"], "HS": 0.5 * (hs["lo"] + hs["hi"])}


def r_on_tensor(M_agg, cfg, kq, wq, t2, t4, t6=0.0, want_modes=False):
    """Descriptor speeds on one aggregate tensor with the E2 weight marginal
    F0 + c2 t2 F2 + c4 t4 F4 + c6 t6 F6 (A-2.5)."""
    modes = christoffel_modes(M_agg, kq)
    F = e2_marginal_moments(modes)
    fbar = F[0] + cfg.c2 * t2 * F[2] + cfg.c4 * t4 * F[4] + cfg.c6 * t6 * F[6]
    out = descriptor_speeds(modes, wq, fbar)
    if want_modes:
        out["_modes"], out["_F"], out["_fbar"] = modes, F, fbar
    return out


def transverse_pair_along_x(M_agg):
    """qSH (e || y) and qSV (e || z) speeds for propagation along x (k perpendicular to the
    fiber axis), labelled by polarization."""
    modes = christoffel_modes(M_agg, XHAT[None, :])
    E, v = modes["E"][0], modes["v"][0]
    bSH = int(np.argmax(np.abs(E @ YHAT)))
    bSV = int(np.argmax(np.abs(E @ ZHAT)))
    if bSH == bSV:
        halt("transverse labelling along x degenerate")
    return float(v[bSH]), float(v[bSV]), float(abs(E[bSH] @ YHAT)), float(abs(E[bSV] @ ZHAT))


def rel_dev(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def tensor_rel_change(A, B):
    return float(np.max(np.abs(A - B)) / np.max(np.abs(B)))


# ---------------------------------------------------------------- main
def main():
    t_start = time.time()
    guard_files()
    t1mod, t1pats = t1_load()
    t1_state = t1_selfscan(t1mod, t1pats)
    schema = json.load(open(os.path.join(HERE, "g_mscs2_schema_v1_0.json"), encoding="utf-8"))
    tau = schema["tolerances"]["tau_agg"]
    kfloor = schema["tolerances"]["kappa_floor"]
    assert list(T4_GRID) == schema["t4_grid"] and list(T2T4_GRID) == schema["t2t4_grid"]
    assert KEYS == schema["keys"]
    print(f"activation: {ACTIVATION_FLAG}   (Addendum A-3 in force: {A3_IN_FORCE})")
    print(f"T1: instrument {t1_state['instrument']} memo {t1_state['memo']}")

    X1 = json.load(open(os.path.join(HERE, "inputs/poly_vrh_results.json"), encoding="utf-8"))
    X6c = json.load(open(os.path.join(HERE, "inputs/g_mscs1_chatleg_checkpoint.json"), encoding="utf-8"))
    X6cc = json.load(open(os.path.join(HERE, "inputs/g_mscs1_ccleg_checkpoint.json"), encoding="utf-8"))
    vrh = X1["vrh"]

    def hexM(tag, arm):
        c = vrh[tag]["C_over_rho"]
        C66 = c["C66"] if arm == "a" else 0.5 * (c["C11"] - c["C12"])
        return voigt_to_mandel(hex_voigt(c["C11"], c["C12"], c["C13"], c["C33"], c["C44"], C66))

    def cubM(tag):
        c = vrh[tag]["C_over_rho"]
        return voigt_to_mandel(cubic_voigt(c["C11"], c["C12"], c["C44"]))

    CFG = {
        "hex_step|a": Config("hex_step|a", "hex", hexM("hex:step", "a"), ZHAT),
        "hex_step|b": Config("hex_step|b", "hex", hexM("hex:step", "b"), ZHAT),
        "hex_gem8|a": Config("hex_gem8|a", "hex", hexM("hex:gem8", "a"), ZHAT),
        "hex_gem8|b": Config("hex_gem8|b", "hex", hexM("hex:gem8", "b"), ZHAT),
        "cubic_step|001": Config("cubic_step|001", "cubic", cubM("cubic:step"), ZHAT),
        "cubic_step|111": Config("cubic_step|111", "cubic", cubM("cubic:step"), N111),
        "cubic_gem8|001": Config("cubic_gem8|001", "cubic", cubM("cubic:gem8"), ZHAT),
        "cubic_gem8|111": Config("cubic_gem8|111", "cubic", cubM("cubic:gem8"), N111),
    }

    print("== selftests ==")
    st = selftests()
    for k, v in st.items():
        print(f"   {k}: {v}")
    for k in ("mandel_rotation_dev", "ti_projector_vs_psi_average_dev", "fracE2_closed_form_dev",
              "psi_moment_closed_form_dev", "T4_voigt_table_dev", "K4_mean", "K4_sq_mean_minus_4_21",
              "P4_sq_mean_minus_1_9", "K6_mean", "K6_K4_overlap", "P2_mean"):
        if abs(st[k]) > 1e-12:
            halt(f"selftest {k} = {st[k]}")
    if st["fiber_rule_iso_dev"] > 1e-12 * 10:
        halt("fiber rule iso dev")
    print(f"   marginal coefficients c4: 001 -> {CFG['cubic_step|001'].c4}, 111 -> {CFG['cubic_step|111'].c4}"
          f"   (c6: {CFG['cubic_step|001'].c6}, {CFG['cubic_step|111'].c6}; K6 scale {K6_SCALE})")
    if abs(CFG["cubic_step|001"].c4 - 1.0) > 1e-14 or abs(CFG["cubic_step|111"].c4 + 2.0 / 3.0) > 1e-14:
        halt("marginal c coefficients differ from A-2.5")

    kq, wq = sphere_gl_uniform(64, 128)
    kq2, wq2 = sphere_gl_uniform(128, 256)

    # ================================================================ Phase 1 (PIN-XTAL inputs)
    print("== Phase 1 (single crystal; PIN-XTAL inputs) ==")
    phase1 = {}
    for key, cfg in CFG.items():
        modes = christoffel_modes(cfg.M, kq)
        fr = frac_E2_fixed_axis(modes, cfg.n_c)
        d = descriptor_speeds(modes, wq, fr)
        phase1[key] = {k: d[k] for k in ("v_EM", "v_S2E2", "v_S2h", "r_E2", "r_h", "lambda_mean", "lambda_max")}
        phase1[key]["r_xtal_E2"] = phase1[key].pop("r_E2")
        phase1[key]["r_xtal_h"] = phase1[key].pop("r_h")
        print(f"   {key}: r_E2 {phase1[key]['r_xtal_E2']:+.6e} r_h {phase1[key]['r_xtal_h']:+.6e} "
              f"lam_mean {phase1[key]['lambda_mean']:.4e} lam_max {phase1[key]['lambda_max']:.4e}")

    def pin_worst(fields, mine, theirs):
        w = 0.0
        for f in fields:
            if f in theirs and theirs[f] is not None:
                w = max(w, rel_dev(mine[f], theirs[f]))
        return w

    pin_xtal = {"worst_rel": 0.0, "worst_rel_vs_cc": 0.0, "by_key": {}}
    for key in KEYS:
        a = pin_worst(("r_xtal_E2", "r_xtal_h", "lambda_mean", "lambda_max"), phase1[key], X6c["phase1"][key])
        b = pin_worst(("r_xtal_E2", "r_xtal_h", "lambda_mean", "lambda_max"), phase1[key], X6cc["phase1"][key])
        pin_xtal["by_key"][key] = a
        pin_xtal["worst_rel"] = max(pin_xtal["worst_rel"], a)
        pin_xtal["worst_rel_vs_cc"] = max(pin_xtal["worst_rel_vs_cc"], b)
    pin_xtal["passed"] = bool(pin_xtal["worst_rel"] <= 1e-8)
    print(f"   PIN-XTAL worst rel {pin_xtal['worst_rel']:.3e} (vs cc {pin_xtal['worst_rel_vs_cc']:.3e})")

    # ================================================================ HS references + t = 0 pins
    print("== HS references (optimized at t = 0, reused at every texture) ==")
    hs_ref = {}
    for key, cfg in CFG.items():
        base = key.split("|")[0]
        cache = base if cfg.sym == "cubic" or key.endswith("|a") else key
        if cache not in hs_ref:
            lo = hs_reference(cfg.M, "lo")
            hi = hs_reference(cfg.M, "hi")
            hs_ref[cache] = {"lo": lo, "hi": hi}
            print(f"   {cache}: lo (K0,G0)=({lo[0]:.6f},{lo[1]:.6f}) G_HS {lo[2]:.10f} | "
                  f"hi ({hi[0]:.6f},{hi[1]:.6f}) G_HS {hi[2]:.10f}")

    AGG = {}
    for key, cfg in CFG.items():
        base = key.split("|")[0]
        cache = base if cfg.sym == "cubic" or key.endswith("|a") else key
        AGG[key] = Aggregate(cfg, hs_ref[cache]["lo"], hs_ref[cache]["hi"])

    phase2 = {k: {} for k in KEYS}
    pin_vrh0 = {"worst_rel": 0.0, "worst_rel_vs_cc": 0.0}
    pin_hs0 = {"worst_rel": 0.0, "worst_rel_vs_cc": 0.0, "G_HS": {}}
    for key, cfg in CFG.items():
        T0 = AGG[key].tensors(cfg.odf())
        KV, GV = iso_KG(T0["V"])
        KR, GR = iso_KG(T0["R"])
        G_lo, G_hi = iso_KG(T0["HS_lo"])[1], iso_KG(T0["HS_hi"])[1]
        p = phase2[key]
        p["vT_V"], p["vT_R"], p["vT_VRH"] = math.sqrt(GV), math.sqrt(GR), math.sqrt(0.5 * (GV + GR))
        p["vT_HS_lo"], p["vT_HS_hi"] = math.sqrt(G_lo), math.sqrt(G_hi)
        p["x_KV_GV_KR_GR"] = [KV, GV, KR, GR]
        for src, acc in ((X6c, "worst_rel"), (X6cc, "worst_rel_vs_cc")):
            pin_vrh0[acc] = max(pin_vrh0[acc], pin_worst(("vT_VRH", "vT_V", "vT_R"), p, src["phase2"][key]))
            pin_hs0[acc] = max(pin_hs0[acc], pin_worst(("vT_HS_lo", "vT_HS_hi"), p, src["phase2"][key]))
        cfgx = X6_CFG[key.split("|")[0]]
        if cfgx in X6c.get("pins_vrh0", {}):
            ghs = X6c["pins_vrh0"][cfgx]["G_HS"]
            pin_hs0["worst_rel"] = max(pin_hs0["worst_rel"], rel_dev(G_lo, ghs[0]), rel_dev(G_hi, ghs[1]))
        pin_hs0["G_HS"][key] = [G_lo, G_hi]
    pin_vrh0["passed"] = bool(pin_vrh0["worst_rel"] <= 1e-8)
    pin_hs0["passed"] = bool(pin_hs0["worst_rel"] <= 1e-6)
    print(f"   PIN-VRH0 worst rel {pin_vrh0['worst_rel']:.3e} (vs cc {pin_vrh0['worst_rel_vs_cc']:.3e})")
    print(f"   PIN-HS0 worst rel {pin_hs0['worst_rel']:.3e} (vs cc {pin_hs0['worst_rel_vs_cc']:.3e})")

    # ================================================================ PIN-K2 (l = 2 family, t4 = 0)
    print("== PIN-K2 (the inherited l = 2 family, G-MSCS1 grid and window) ==")
    pin_k2 = {"worst_rel_hex_kappa2": 0.0, "worst_abs_cubic_kappa2": 0.0, "by_key": {}}
    so3_dev_all, so3_mean_t0 = 0.0, []
    for key, cfg in CFG.items():
        r2 = []
        for t in T4_GRID:
            T = AGG[key].tensors(cfg.odf(t2=t))
            d = r_on_tensor(T["Hill"], cfg, kq, wq, t2=t, t4=0.0, want_modes=(t == 0.0))
            r2.append(d["r_E2"])
            if t == 0.0:
                F0 = d["_F"][0]
                valid = d["_modes"]["wEM"] > 1e-6
                so3_dev_all = max(so3_dev_all, float(np.max(np.abs(F0[valid] - 0.4))))
                so3_mean_t0.append(float(np.mean(F0[valid])))
        (S2, k2, k3), resid, npts = fit_cubic_through_origin(T4_GRID, np.array(r2), 0.25)
        phase2[key]["kappa2_E2"] = k2
        phase2[key]["x_l2_family"] = {"S2_E2": S2, "kappa3_E2": k3, "fit_residual": resid, "r_agg_E2_VRH_l2": r2, "n_fit_points": npts}
        ref = X6c["phase2"][key]["kappa2_E2"]
        if cfg.sym == "hex":
            dev = rel_dev(k2, ref)
            pin_k2["worst_rel_hex_kappa2"] = max(pin_k2["worst_rel_hex_kappa2"], dev)
        else:
            dev = abs(k2)
            pin_k2["worst_abs_cubic_kappa2"] = max(pin_k2["worst_abs_cubic_kappa2"], dev)
        pin_k2["by_key"][key] = {"kappa2_E2": k2, "x6_chat": ref, "x6_cc": X6cc["phase2"][key]["kappa2_E2"], "dev": dev}
        print(f"   {key}: kappa2_E2 {k2:+.9e}  (X-6 chat {ref:+.9e})  dev {dev:.3e}")
    pin_k2["passed"] = bool(pin_k2["worst_rel_hex_kappa2"] <= 1e-4 and pin_k2["worst_abs_cubic_kappa2"] <= 1e-12)

    # ================================================================ Phase 2 (l = 4 families)
    print("== Phase 2 (l = 4 families; VRH and HS at every t4) ==")
    doubling = 0.0
    biref_identity = {}
    for key, cfg in CFG.items():
        p = phase2[key]
        arrays = {k: [] for k in ("r_agg_E2_VRH", "r_agg_h_VRH", "r_agg_E2_HS", "r_agg_E2_V", "r_agg_E2_R", "lambda_mean_t4",
                                  "x_vqSH_t4", "x_vqSV_t4", "x_r_agg_h_HS")}
        for t in T4_GRID:
            T = AGG[key].tensors(cfg.odf(t4=t))
            dH = r_on_tensor(T["Hill"], cfg, kq, wq, 0.0, t)
            dHS = r_on_tensor(T["HS"], cfg, kq, wq, 0.0, t)
            dV = r_on_tensor(T["V"], cfg, kq, wq, 0.0, t)
            dR = r_on_tensor(T["R"], cfg, kq, wq, 0.0, t)
            arrays["r_agg_E2_VRH"].append(dH["r_E2"])
            arrays["r_agg_h_VRH"].append(dH["r_h"])
            arrays["lambda_mean_t4"].append(dH["lambda_mean"])
            arrays["r_agg_E2_HS"].append(dHS["r_E2"])
            arrays["x_r_agg_h_HS"].append(dHS["r_h"])
            arrays["r_agg_E2_V"].append(dV["r_E2"])
            arrays["r_agg_E2_R"].append(dR["r_E2"])
            vsh, vsv, _, _ = transverse_pair_along_x(T["Hill"])
            arrays["x_vqSH_t4"].append(vsh)
            arrays["x_vqSV_t4"].append(vsv)
            if t == 0.25:
                d2 = r_on_tensor(T["Hill"], cfg, kq2, wq2, 0.0, t)
                doubling = max(doubling, abs(d2["r_E2"] - dH["r_E2"]))
        p.update(arrays)
        rE = np.array(arrays["r_agg_E2_VRH"])
        (S4, k44, k444), resid, n9 = fit_cubic_through_origin(T4_GRID, rE, 0.25)
        (_, k44h, _), _, n7 = fit_cubic_through_origin(T4_GRID, rE, 0.1)
        (S4h, k44_h, _), _, _ = fit_cubic_through_origin(T4_GRID, np.array(arrays["r_agg_h_VRH"]), 0.25)
        (_, k44_HS, _), _, _ = fit_cubic_through_origin(T4_GRID, np.array(arrays["r_agg_E2_HS"]), 0.25)
        (_, k44_s7, _), _, ns7 = fit_cubic_through_origin(T4_GRID, rE, 0.25, inclusive=False)
        (_, k44_s5, _), _, ns5 = fit_cubic_through_origin(T4_GRID, rE, 0.1, inclusive=False)
        p.update({"S4_E2": S4, "S4_h": S4h, "kappa44_E2": k44, "kappa444_E2": k444, "kappa44_h": k44_h,
                  "kappa44_E2_HS": k44_HS, "halving_dev_kappa44": abs(k44 - k44h), "fit_residual_E2": resid,
                  "x_fit_windows": {"n_points_0p25_inclusive": n9, "n_points_0p1_inclusive": n7,
                                    "kappa44_E2_strict_window_0p25": k44_s7, "n_strict_0p25": ns7,
                                    "kappa44_E2_strict_window_0p1": k44_s5, "n_strict_0p1": ns5,
                                    "halving_dev_strict": abs(k44_s7 - k44_s5)}})
        # birefringence (A-2.7): symmetric difference at +-0.05 on Hill, k = x, labelled by polarization
        dv = {}
        for t in (0.05, -0.05):
            T = AGG[key].tensors(cfg.odf(t4=t))
            vsh, vsv, aY, aZ = transverse_pair_along_x(T["Hill"])
            dv[t] = vsh - vsv
        p["biref_b1_VRH"] = (dv[0.05] - dv[-0.05]) / (0.1 * p["vT_VRH"])
        p["x_biref_polarization_overlap_min"] = min(aY, aZ)
        print(f"   {key}: S4 {S4:+.3e} kappa44_E2 {k44:+.9e} (HS {k44_HS:+.6e}, h {k44_h:+.3e}) "
              f"kappa444 {k444:+.3e} halving {abs(k44 - k44h):.3e} b1 {p['biref_b1_VRH']:+.6e}")

    # Voigt birefringence identity on the cubic keys (in-instrument check, extras)
    for key, cfg in CFG.items():
        if cfg.sym != "cubic":
            continue
        Cv = mandel_to_voigt(cfg.M)
        H = Cv[0, 0] - Cv[0, 1] - 2.0 * Cv[3, 3]
        T = AGG[key].tensors(cfg.odf(t4=0.05))
        vsh, vsv, _, _ = transverse_pair_along_x(T["V"])
        biref_identity[key] = {"vqSH2_minus_vqSV2_voigt": vsh ** 2 - vsv ** 2, "H_t4_over_21": H * 0.05 / 21.0,
                               "rel_residual": rel_dev(vsh ** 2 - vsv ** 2, H * 0.05 / 21.0)}

    # ================================================================ Phase 2 second arm: quadratic form
    print("== Phase 2 second arm: the (t2, t4) quadratic form on the 5 x 5 grid; A-3.2 Richardson ==")
    for key, cfg in CFG.items():
        t2s, t4s, rs = [], [], []
        pos_min = math.inf
        for t2 in T2T4_GRID:
            for t4 in T2T4_GRID:
                w = cfg.odf(t2=t2, t4=t4)
                pos_min = min(pos_min, float(w.min()))
                T = AGG[key].tensors(w)
                d = r_on_tensor(T["Hill"], cfg, kq, wq, t2, t4)
                t2s.append(t2)
                t4s.append(t4)
                rs.append(d["r_E2"])
        qf = fit_quadform(np.array(t2s), np.array(t4s), np.array(rs))
        qf["x_grid_r_agg_E2_VRH"] = rs
        qf["x_reading"] = "(i) inherited descriptor-axis P2 (A-3.3)" if cfg.sym == "cubic" else "hex two-parameter family"
        phase2[key]["quadform"] = qf
        phase2[key]["x_min_odf_weight_5x5"] = pos_min

        def r_mixed(t2, t4):
            T = AGG[key].tensors(cfg.odf(t2=t2, t4=t4))
            return r_on_tensor(T["Hill"], cfg, kq, wq, t2, t4)["r_E2"]

        def D(h):
            return (r_mixed(h, h) - r_mixed(h, -h) - r_mixed(-h, h) + r_mixed(-h, -h)) / (4.0 * h * h)

        Dh, Dh2 = D(0.02), D(0.01)
        phase2[key]["kappa24_richardson"] = (4.0 * Dh2 - Dh) / 3.0
        phase2[key]["x_kappa24_richardson_D"] = {"D_0p02": Dh, "D_0p01": Dh2}
        if cfg.sym == "cubic":
            # reading (ii): the O_h-symmetrized l = 2 term vanishes identically on cubic; the form
            # reduces to kappa44 t4^2 -- the same 7-term fit on r(t4) alone, for the record
            rs_ii = []
            for t2 in T2T4_GRID:
                for t4 in T2T4_GRID:
                    T = AGG[key].tensors(cfg.odf(t4=t4))
                    rs_ii.append(r_on_tensor(T["Hill"], cfg, kq, wq, 0.0, t4)["r_E2"])
            phase2[key]["x_quadform_reading_ii_Oh_symmetrized"] = fit_quadform(np.array(t2s), np.array(t4s), np.array(rs_ii))
        print(f"   {key}: kappa22 {qf['kappa22']:+.6e} kappa24 {qf['kappa24']:+.6e} kappa44 {qf['kappa44']:+.6e} "
              f"resid {qf['residual']:.2e} | kappa24_richardson {phase2[key]['kappa24_richardson']:+.6e}")

    # ================================================================ Phase 0 controls
    print("== Phase 0 controls ==")
    # F-CTRL-SO3 (hex_step|a at t = 0 is the stated control; evaluated on every key)
    i0 = int(np.where(T4_GRID == 0.0)[0][0])
    r0 = max(abs(phase2[k]["r_agg_E2_VRH"][i0]) for k in KEYS)
    ctrl_so3 = {"passed": bool(so3_dev_all <= 1e-10 and r0 <= 1e-6), "dev_from_0p4": so3_dev_all,
                "r_agg_0_abs": r0, "x_mean_F0_t0": float(np.mean(so3_mean_t0))}

    # F-CTRL-QUAD
    ctrl_quad = {"passed": bool(doubling <= 1e-10), "doubling_residual": doubling,
                 "x_k_rule": "GL(cos theta) 64 x uniform phi 128; doubling 128 x 256 at t4 = 0.25 on Hill/E2 per key",
                 "x_fiber_rule": "fiber-axis route: analytic SO(2) coset average x GL(cos theta) 16 x uniform phi 32 on a generically rotated node set (exact to degree 31)"}

    # F-CTRL-ISO: isotropic tensor through both paths
    K_iso, G_iso = 134.609, 70.881
    C11i, C12i = K_iso + 4.0 * G_iso / 3.0, K_iso - 2.0 * G_iso / 3.0
    iso_worst = 0.0
    iso_detail = {}
    for path in ("cubic", "hex"):
        if path == "cubic":
            cfg_i = Config("iso|cubic", "cubic", voigt_to_mandel(cubic_voigt(C11i, C12i, G_iso)), ZHAT)
        else:
            cfg_i = Config("iso|hex", "hex", voigt_to_mandel(hex_voigt(C11i, C12i, C12i, C11i, G_iso, G_iso)), ZHAT)
        lo, hi = hs_reference(cfg_i.M, "lo"), hs_reference(cfg_i.M, "hi")
        agg_i = Aggregate(cfg_i, lo, hi)
        m = christoffel_modes(cfg_i.M, kq)
        d = descriptor_speeds(m, wq, frac_E2_fixed_axis(m, ZHAT))
        w_x = max(abs(d["r_E2"]), abs(d["r_h"]))
        w_a = 0.0
        for t in T4_GRID:
            T = agg_i.tensors(cfg_i.odf(t4=t))
            for tens in ("Hill", "HS"):
                dd = r_on_tensor(T[tens], cfg_i, kq, wq, 0.0, t)
                w_a = max(w_a, abs(dd["r_E2"]), abs(dd["r_h"]))
        iso_detail[path] = {"r_xtal_worst": w_x, "r_agg_worst": w_a}
        iso_worst = max(iso_worst, w_x, w_a)
    ctrl_iso = {"passed": bool(iso_worst <= 1e-10), "worst_abs": iso_worst, "x_detail": iso_detail}

    # F-CTRL-POS: every ODF used, on the fiber nodes
    pos_min = math.inf
    used = []
    for key, cfg in CFG.items():
        for t in T4_GRID:
            used.append(cfg.odf(t4=t))
            used.append(cfg.odf(t2=t))
        for t2 in T2T4_GRID:
            for t4 in T2T4_GRID:
                used.append(cfg.odf(t2=t2, t4=t4))
        for h in (0.02, 0.01):
            for s1 in (1, -1):
                for s2 in (1, -1):
                    used.append(cfg.odf(t2=s1 * h, t4=s2 * h))
        used.append(cfg.odf(t2=1.0))
        used.append(cfg.odf(t4=0.25, t6=0.3))
        used.append(cfg.odf(t2=0.25, t4=0.25, t6=0.3))
        for t in (0.05, -0.05, 0.3, 0.6, 1.0):
            used.append(cfg.odf(t4=t))
    pos_min = float(min(w.min() for w in used))
    ctrl_pos = {"passed": bool(pos_min >= 0.0), "min_odf_weight": pos_min, "x_n_odfs_checked": len(used)}

    # F-CTRL-L2NULL (A-3.1 scope)
    l2_worst = 0.0
    l2_detail, mixed_diag = {}, {}
    for key, cfg in CFG.items():
        if cfg.sym != "cubic":
            continue
        T0 = AGG[key].tensors(cfg.odf())
        T1 = AGG[key].tensors(cfg.odf(t2=1.0))
        d0 = r_on_tensor(T0["Hill"], cfg, kq, wq, 0.0, 0.0)
        d1 = r_on_tensor(T1["Hill"], cfg, kq, wq, 1.0, 0.0)
        pure = {"V": tensor_rel_change(T1["V"], T0["V"]), "Sbar": tensor_rel_change(T1["Sbar"], T0["Sbar"]),
                "HS_lo": tensor_rel_change(T1["HS_lo"], T0["HS_lo"]), "HS_hi": tensor_rel_change(T1["HS_hi"], T0["HS_hi"]),
                "r_agg_E2": abs(d1["r_E2"] - d0["r_E2"]), "r_agg_h": abs(d1["r_h"] - d0["r_h"])}
        Ta = AGG[key].tensors(cfg.odf(t2=0.0, t4=0.25))
        Tb = AGG[key].tensors(cfg.odf(t2=0.25, t4=0.25))
        da = r_on_tensor(Ta["Hill"], cfg, kq, wq, 0.0, 0.25)
        db = r_on_tensor(Tb["Hill"], cfg, kq, wq, 0.25, 0.25)
        mixed_t = {"V": tensor_rel_change(Tb["V"], Ta["V"]), "Sbar": tensor_rel_change(Tb["Sbar"], Ta["Sbar"]),
                   "HS_lo": tensor_rel_change(Tb["HS_lo"], Ta["HS_lo"]), "HS_hi": tensor_rel_change(Tb["HS_hi"], Ta["HS_hi"])}
        mixed_r = db["r_E2"] - da["r_E2"]
        l2_detail[key] = {"pure_l2_t1": pure, "mixed_tensor_clauses": mixed_t, "mixed_r_agg_change_A29": mixed_r,
                          "x_mixed_r_agg_h_change": db["r_h"] - da["r_h"]}
        mixed_diag[key] = mixed_r
        l2_worst = max(l2_worst, *pure.values(), *mixed_t.values())
    literal_worst = max(l2_worst, max(abs(v) for v in mixed_diag.values()))
    ctrl_l2 = {"passed": bool(l2_worst <= 1e-12), "worst_abs": l2_worst, "mixed_r_agg_change_A29": mixed_diag,
               "x_scope": "A-3.1: pure l = 2 (tensors + r_agg) and mixed-term tensor clauses; mixed r_agg reported",
               "x_literal_A29_worst_abs": literal_worst, "x_literal_A29_would_pass": bool(literal_worst <= 1e-12),
               "x_detail": l2_detail}

    # F-CTRL-L4EXHAUST
    ex_t, ex_r = 0.0, 0.0
    ex_detail = {}
    for key, cfg in CFG.items():
        cases = [((0.0, 0.25), "t4=0.25")]
        if cfg.sym == "hex":
            cases.append(((0.25, 0.25), "t2=t4=0.25"))
        for (t2, t4), label in cases:
            Ta = AGG[key].tensors(cfg.odf(t2=t2, t4=t4))
            Tb = AGG[key].tensors(cfg.odf(t2=t2, t4=t4, t6=0.3))
            da = r_on_tensor(Ta["Hill"], cfg, kq, wq, t2, t4, 0.0)
            db = r_on_tensor(Tb["Hill"], cfg, kq, wq, t2, t4, 0.3)
            ha = r_on_tensor(Ta["HS"], cfg, kq, wq, t2, t4, 0.0)
            hb = r_on_tensor(Tb["HS"], cfg, kq, wq, t2, t4, 0.3)
            tens = max(tensor_rel_change(Tb["V"], Ta["V"]), tensor_rel_change(Tb["Sbar"], Ta["Sbar"]),
                       tensor_rel_change(Tb["HS_lo"], Ta["HS_lo"]), tensor_rel_change(Tb["HS_hi"], Ta["HS_hi"]))
            rr = max(abs(db["r_E2"] - da["r_E2"]), abs(db["r_h"] - da["r_h"]), abs(hb["r_E2"] - ha["r_E2"]))
            entry = {"tensor_rel": tens, "r_agg_abs": rr}
            if cfg.sym == "cubic":
                m = christoffel_modes(Ta["Hill"], kq)
                wa = e2_direct_average(m, cfg, cfg.odf(t2=t2, t4=t4))
                wb = e2_direct_average(m, cfg, cfg.odf(t2=t2, t4=t4, t6=0.3))
                entry["x_direct_E2_weight_change"] = float(np.max(np.abs(wb - wa)))
            ex_detail[f"{key} {label}"] = entry
            ex_t, ex_r = max(ex_t, tens), max(ex_r, rr)
    ctrl_ex = {"passed": bool(ex_t <= 1e-12 and ex_r <= 1e-12), "worst_rel_tensor": ex_t, "worst_abs_r_agg": ex_r,
               "x_t6": 0.3, "x_K6_normalization": f"max|K6| = 1 on the sphere (raw scale {K6_SCALE})", "x_detail": ex_detail}

    # F-CTRL-C4: exact closed forms and affinity on both cubic configurations; H = 0 tensor
    c4_cf, c4_aff = 0.0, 0.0
    c4_detail = {}
    T4z = harmonic_l4_tensor(ZHAT)
    for key in ("cubic_step|001", "cubic_gem8|001"):
        cfg = CFG[key]
        Cv = mandel_to_voigt(cfg.M)
        H = Cv[0, 0] - Cv[0, 1] - 2.0 * Cv[3, 3]
        Sfull = mandel_to_full(np.linalg.inv(cfg.M))
        HS_ = Sfull[0, 0, 0, 0] - Sfull[0, 0, 1, 1] - 2.0 * Sfull[0, 1, 0, 1]
        T = {t: AGG[key].tensors(cfg.odf(t4=t)) for t in (0.0, 0.3, 0.6)}
        Cmax = float(np.max(np.abs(mandel_to_voigt(T[0.0]["V"]))))
        Smax = float(np.max(np.abs(mandel_to_full(T[0.0]["Sbar"]))))
        dev_cf, dev_af = 0.0, 0.0
        for t in (0.3, 0.6):
            dCv = mandel_to_voigt(T[t]["V"] - T[0.0]["V"])
            pred = mandel_to_voigt(full_to_mandel(t * (H / 3.0) * T4z))
            dev_cf = max(dev_cf, float(np.max(np.abs(dCv - pred))) / Cmax)
            dS = mandel_to_full(T[t]["Sbar"] - T[0.0]["Sbar"])
            dev_cf = max(dev_cf, float(np.max(np.abs(dS - t * (HS_ / 3.0) * T4z))) / Smax)
        dev_af = max(float(np.max(np.abs((T[0.6]["V"] - T[0.0]["V"]) - 2.0 * (T[0.3]["V"] - T[0.0]["V"])))) / Cmax,
                     float(np.max(np.abs((T[0.6]["Sbar"] - T[0.0]["Sbar"]) - 2.0 * (T[0.3]["Sbar"] - T[0.0]["Sbar"])))) / Smax)
        c4_detail[key] = {"H": H, "H_S": HS_, "closed_form_rel": dev_cf, "affine_rel": dev_af,
                          "x_voigt_dC_t0p3": [[float(x) for x in row] for row in mandel_to_voigt(T[0.3]["V"] - T[0.0]["V"])]}
        c4_cf, c4_aff = max(c4_cf, dev_cf), max(c4_aff, dev_af)
    cfg_h0 = Config("h0|cubic", "cubic", voigt_to_mandel(cubic_voigt(C11i, C12i, G_iso)), ZHAT)
    tab0 = fiber_table(cfg_h0.M)
    V0, V3 = odf_average(tab0, cfg_h0.odf()), odf_average(tab0, cfg_h0.odf(t4=0.3))
    h0_eff = float(np.max(np.abs(V3 - V0)) / np.max(np.abs(V0)))
    ctrl_c4 = {"passed": bool(c4_cf <= 1e-12 and c4_aff <= 1e-12 and h0_eff <= 1e-12),
               "worst_rel_closed_form": c4_cf, "worst_rel_affine": c4_aff, "h0_effect_rel": h0_eff, "x_detail": c4_detail}

    # F-CTRL-MARG: SO(3)-direct vs marginal E2 weight average on the cubic keys, every mode
    marg_worst = 0.0
    marg_detail = {}
    for key, cfg in CFG.items():
        if cfg.sym != "cubic":
            continue
        for t4 in (0.5, -0.5):
            T = AGG[key].tensors(cfg.odf(t4=t4))
            d = r_on_tensor(T["Hill"], cfg, kq, wq, 0.0, t4, want_modes=True)
            direct = e2_direct_average(d["_modes"], cfg, cfg.odf(t4=t4))
            valid = d["_modes"]["wEM"] > 1e-13
            dev = float(np.max(np.abs(direct[valid] - d["_fbar"][valid])))
            marg_detail[f"{key} t4={t4}"] = dev
            marg_worst = max(marg_worst, dev)
    ctrl_marg = {"passed": bool(marg_worst <= 1e-12), "worst_abs": marg_worst,
                 "x_c_coefficients": {"001": CFG["cubic_step|001"].c4, "111": CFG["cubic_step|111"].c4}, "x_detail": marg_detail}

    # F-CTRL-TEX4
    cfg_t = Config("tex4|cubic", "cubic", voigt_to_mandel(cubic_voigt(300.0, 100.0, 40.0)), ZHAT)
    lo, hi = hs_reference(cfg_t.M, "lo"), hs_reference(cfg_t.M, "hi")
    agg_t = Aggregate(cfg_t, lo, hi)
    Tt = agg_t.tensors(cfg_t.odf(t4=1.0))
    dt = r_on_tensor(Tt["Hill"], cfg_t, kq, wq, 0.0, 1.0)
    ctrl_tex = {"passed": bool(abs(dt["r_E2"]) > 1e-6), "r_agg_t1_abs": abs(dt["r_E2"]), "x_r_agg_t1": dt["r_E2"], "x_H": 120.0}

    phase0 = {
        "PIN-XTAL": pin_xtal, "PIN-VRH0": pin_vrh0, "PIN-HS0": pin_hs0, "PIN-K2": pin_k2,
        "F-CTRL-ISO": ctrl_iso, "F-CTRL-SO3": ctrl_so3, "F-CTRL-POS": ctrl_pos, "F-CTRL-L2NULL": ctrl_l2,
        "F-CTRL-L4EXHAUST": ctrl_ex, "F-CTRL-C4": ctrl_c4, "F-CTRL-MARG": ctrl_marg, "F-CTRL-TEX4": ctrl_tex,
        "F-CTRL-QUAD": ctrl_quad,
    }
    assert list(phase0) == schema["phase0"]["items"]
    for name, c in phase0.items():
        floats = {k: c[k] for k in schema["phase0"]["float_rules"].get(name, {})}
        print(f"   {name}: {'PASS' if c['passed'] else 'FAIL'}  {floats}")

    # ================================================================ Phase 3 (verdict last, schema rule)
    worst_S4 = max(max(abs(phase2[k]["S4_E2"]), abs(phase2[k]["S4_h"])) for k in KEYS)
    all0 = all(c["passed"] for c in phase0.values())
    fm3 = "FIRES" if worst_S4 > tau else "SILENT"
    null_cubic = all(abs(phase2[k]["kappa44_E2"]) <= kfloor for k in schema["primary_cubic_keys"])
    fm4 = "FIRES" if null_cubic else "SILENT"
    if not all0:
        verdict = "INDETERMINATE"
    elif fm3 == "FIRES":
        verdict = "PROTECTION-BREACH"
    elif null_cubic:
        verdict = "L4-NULL"
    else:
        verdict = "IDENTITY-DELIVERED-L4"
    phase3 = {"verdict_class": verdict, "F-MS2-3": fm3, "F-MS2-4": fm4, "F-MS2-2": "REGISTERED_NOT_EXECUTED", "worst_S4": worst_S4}
    print(f"== verdict: {verdict}  (worst |S4| {worst_S4:.3e}; F-MS2-3 {fm3}; F-MS2-4 {fm4}) ==")

    checkpoint = {
        "gate": "G-MSCS2", "leg": "cc", "instrument": "g_mscs2_ccleg.py",
        "instrument_md5": md5_file(os.path.abspath(__file__)),
        "memo_lock_md5": GUARDS[MEMO][0], "memo_lock_bytes": GUARDS[MEMO][1],
        "ledger_base_md5": schema["ledger_base_md5"],
        "t1_list_md5": GUARDS[T1_LIST][0], "schema_md5": GUARDS["g_mscs2_schema_v1_0.json"][0],
        "x1_md5": GUARDS["inputs/poly_vrh_results.json"][0],
        "x6_chat_md5": GUARDS["inputs/g_mscs1_chatleg_checkpoint.json"][0],
        "x6_cc_md5": GUARDS["inputs/g_mscs1_ccleg_checkpoint.json"][0],
        "activation_flag": ACTIVATION_FLAG, "addendum_A3_in_force": A3_IN_FORCE,
        "utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "elections": dict(schema["elections"]),
        "t1_scan": t1_state,
        "phase0": phase0, "phase1": phase1, "phase2": phase2, "phase3": phase3,
        "extras": {
            "method": {
                "so3_route": "fiber-axis: analytic SO(2) coset average (TI projector for tensors; closed-form psi moments for the E2 weight) x S^2 rule GL(cos theta) 16 x uniform phi 32 over the crystal-frame fiber axis, node set rotated by a fixed generic rotation",
                "so3_exact_degree": 31, "n_fiber_nodes": int(len(WFIB)),
                "k_rule": "GL(cos theta) 64 x uniform phi 128 (pinned)", "n_rule": "GL 12 x 24 (pinned)",
                "fracE2": "(1 - (k.n)^2)(1 - (ehat_perp.n)^2)",
                "hs_optimizer": "boundary-K0 bisection + 600-point coarse scan + 9 nested 21-point refinements over G0",
                "fit_windows": "|t4| <= 0.25 (9 points) and |t4| <= 0.1 (7 points), inclusive (G-MSCS1 convention); strict-window fits in phase2[key].x_fit_windows",
                "cubic_two_parameter_reading": "(i) inherited descriptor-axis P2 (A-3.3); reading (ii) in phase2[key].x_quadform_reading_ii_Oh_symmetrized",
            },
            "selftests": st,
            "hs_references": {k: {"lo_K0_G0_GHS": list(v["lo"]), "hi_K0_G0_GHS": list(v["hi"])} for k, v in hs_ref.items()},
            "A3_diagnostics": {
                "A-3.1_mixed_r_agg_change_A29": mixed_diag,
                "A-3.2_kappa24_richardson": {k: phase2[k]["kappa24_richardson"] for k in KEYS},
                "A-3.3_reading": "(i) inherited descriptor-axis P2",
            },
            "biref_voigt_identity_cubic": biref_identity,
            "so3_control_mean_F0_by_key": so3_mean_t0,
            "elapsed_seconds": 0.0,
        },
    }
    checkpoint["extras"]["elapsed_seconds"] = round(time.time() - t_start, 3)

    def to_py(o):
        if isinstance(o, dict):
            return {str(k): to_py(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [to_py(v) for v in o]
        if isinstance(o, np.ndarray):
            return to_py(o.tolist())
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o

    checkpoint = to_py(checkpoint)
    out_path = os.path.join(HERE, "g_mscs2_ccleg_checkpoint.json")
    blob = json.dumps(checkpoint, indent=1, ensure_ascii=False)
    hits, coll = t1mod.scan_text(blob, t1pats)
    if hits:
        halt(f"T1 HIT in the emitted checkpoint: {[i for i, _ in hits]}")
    checkpoint["t1_scan"]["checkpoint_numeric_collisions"] = len(coll)
    blob = json.dumps(checkpoint, indent=1, ensure_ascii=False)
    hits, coll2 = t1mod.scan_text(blob, t1pats)
    if hits or len(coll2) != len(coll):
        halt("T1 fixed point on the emitted checkpoint failed")
    open(out_path, "w", encoding="utf-8").write(blob)
    print(f"checkpoint -> {out_path}  md5 {md5_file(out_path)}  runtime {checkpoint['extras']['elapsed_seconds']} s")


if __name__ == "__main__":
    main()
