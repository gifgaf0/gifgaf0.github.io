#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A1 polarization gate -- BLIND SECOND LEG (leg 2), independent derivation.

Question: what polarization class (tensor / vector / scalar, Eardley-Lee-Lightman-Wagoner-Will sense)
does a plane displacement wave u(x,t) = a f(t - k.x/c) of an isotropic elastic medium present to an
L-shaped interferometer, when the interferometer itself is built from the same medium?

  TASK 1  strain eps = sym(grad u); helicity decomposition about k; transverse-traceless (TT)
          projection Lambda(k) eps for arbitrary k and a (symbolic, sympy).
  TASK 2  six-basis decomposition eps = sum_A c_A e_A and short-arm response R = D:eps on the fixed
          grid, by independent routes:
            (a) tensor projection, linear solve, closed form;
            (b) direct integration of the displacement gradient along finite arms (complex-step
                derivative of u itself, Gauss-Legendre quadrature), then psi spin weight;
            (c) Fourier analysis of R in psi.
          Writes leg2_grid.json.
  TASK 3  the medium's own detector: first-order round-trip time of a short-wavelength transverse
          probe in the strained, moving medium, mirrors at (or offset from) material points, the most
          general isotropic linear acoustoelastic law; finite arms; psi-harmonic analysis.
  TASK 4  other possible helicity-2 sources: internal rotation scalars; anisotropic single crystal;
          detector motion through the medium; second order in the amplitude; (extra) multipath.

Conventions are the fixed ones of the leg-2 brief (k, m, n, p, q, e_A, D = (xx - yy)/2).
Run:  python3 leg2_derive.py      (prints every check; writes leg2_grid.json next to this file)
Exit status 0 iff every check passes.
"""
import os
import sys
import json
import math
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    import sympy as sp
except ImportError:  # vendored copy (pip --target ./_pylib) so nothing is written outside this dir
    sys.path.insert(0, os.path.join(HERE, "_pylib"))
    import sympy as sp
import numpy as np

PREREG = "/home/claude/gifgaf0.github.io/audit_followup/A1_polarization/A1_PREREG.md"
PREREG_MD5 = "d5f6aa3bd50743c5d69e54338494bb27"

RESULTS = []


def check(name, ok, detail=""):
    ok = bool(ok)
    RESULTS.append((name, ok, detail))
    print(("  [PASS] " if ok else "  [FAIL] ") + name + (("   :: " + detail) if detail else ""))
    return ok


def hdr(title):
    print("\n" + "=" * 104 + "\n" + title + "\n" + "=" * 104)


def sub(title):
    print("\n--- " + title)


_TRIG_ANGLES = []   # filled after the angle symbols are created
_TRIG_SC = {}


def _register_angles(*angles):
    for ang in angles:
        _TRIG_ANGLES.append(ang)
        _TRIG_SC[ang] = sp.symbols("S_%s C_%s" % (ang.name, ang.name), real=True)


def trig_zero(expr):
    """Rigorous identity test for polynomials in sin/cos of the registered angles (coefficients may contain other
    symbols, sqrt(2), I): expand multiple angles, map sin->S, cos->C, and reduce modulo the ideal {S^2 + C^2 - 1}.
    Those generators have pairwise coprime leading monomials, so they form a Groebner basis and the normal form is
    0 iff the expression vanishes identically."""
    e = sp.expand(sp.expand_trig(sp.expand(expr)))
    rep = {}
    for ang, (S_, C_) in _TRIG_SC.items():
        rep[sp.sin(ang)] = S_
        rep[sp.cos(ang)] = C_
    e = sp.expand(e.xreplace(rep))
    if e == 0:
        return True
    if any(e.has(sp.sin(ang)) or e.has(sp.cos(ang)) for ang in _TRIG_ANGLES):
        return sp.simplify(expr) == 0
    gens = [g for ang in _TRIG_ANGLES for g in _TRIG_SC[ang]]
    ideal = [_TRIG_SC[ang][0] ** 2 + _TRIG_SC[ang][1] ** 2 - 1 for ang in _TRIG_ANGLES]
    _, r = sp.reduced(e, ideal, *gens, order="lex")
    return sp.expand(r) == 0


def zero_expr(e):
    e = sp.sympify(e)
    if e == 0:
        return True
    if e.has(sp.Subs) or e.has(sp.Derivative) or e.atoms(sp.core.function.AppliedUndef):
        return sp.simplify(e) == 0          # expressions carrying the undefined waveform f
    return trig_zero(e)


def is_zero_matrix(M):
    return all(zero_expr(e) for e in M)


# ======================================================================================================
hdr("TASK 0  Provenance")
if os.path.exists(PREREG):
    with open(PREREG, "rb") as fh:
        md5 = hashlib.md5(fh.read()).hexdigest()
    print("  spec file:", PREREG)
    print("  md5      :", md5)
    check("0.1 locked spec md5 matches d5f6aa3bd50743c5d69e54338494bb27", md5 == PREREG_MD5)
else:
    print("  spec file not present on this machine; md5 check skipped (recorded in LEG2_REPORT.md)")
print("  python", sys.version.split()[0], " numpy", np.__version__, " sympy", sp.__version__)

# ======================================================================================================
hdr("TASK 1  Kinematics of a plane displacement wave (symbolic)")

t, c = sp.symbols("t c", positive=True)
X = sp.Matrix(sp.symbols("x1 x2 x3", real=True))
a1, a2, a3 = sp.symbols("a1 a2 a3", real=True)
Avec = sp.Matrix([a1, a2, a3])
th, ph, ps, chi, al = sp.symbols("theta phi psi chi alpha", real=True)
_register_angles(th, ph, ps, chi, al)
kS =sp.Matrix([sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)])
mS = sp.Matrix([sp.cos(th) * sp.cos(ph), sp.cos(th) * sp.sin(ph), -sp.sin(th)])
nS = sp.Matrix([-sp.sin(ph), sp.cos(ph), 0])
I3 = sp.eye(3)
Z3 = sp.zeros(3, 3)
fF = sp.Function("f")


def symS(M):
    return (M + M.T) / 2


def LamS(T, k):
    """TT projection Lambda(k) T = P T P - (1/2) P tr(P T), P = 1 - k k."""
    P = sp.eye(3) - k * k.T
    return P * T * P - P * (P * T).trace() / 2


sub("1.1 strain of u = a f(t - k.x/c)")
tau = t - (kS.T * X)[0] / c
U = Avec * fF(tau)
gradU = sp.Matrix(3, 3, lambda i, j: sp.diff(U[i], X[j]))  # (grad u)_ij = d_j u_i
eps_sym = symS(gradU)
fdot = sp.diff(fF(tau), t)  # = f'(t - k.x/c)
eps_pred = -(fdot / c) * symS(kS * Avec.T)
check("1.1a eps = sym(grad u) = -(f'/c) sym(k (x) a)  [exact; arbitrary a, k(theta,phi), f]",
      is_zero_matrix(eps_sym - eps_pred))
omega = sp.Matrix([sum(sp.LeviCivita(i, j, l) * sp.diff(U[l], X[j]) for j in range(3) for l in range(3)) / 2
                   for i in range(3)])
check("1.1b rotation omega = curl(u)/2 = -(f'/2c) k x a  (helicity +-1 transverse axial vector; no rank-2 content)",
      all(sp.simplify(e) == 0 for e in (omega - (-(fdot / (2 * c)) * kS.cross(Avec)))))
print("  eps_ij = -(f'/2c) (k_i a_j + a_i k_j);  a = a_par k + a_perp  ->  eps = -(f'/c)[a_par k k + sym(k (x) a_perp)]")

sub("1.2 TT projection Lambda(k) eps")
Lam_eps = LamS(eps_pred, kS)
check("1.2a Lambda(k) eps == 0 identically (spherical k(theta,phi), arbitrary a1,a2,a3, arbitrary f)",
      is_zero_matrix(Lam_eps))
# polynomial version: k = (k1,k2,k3) with only the constraint |k| = 1
k1, k2, k3 = sp.symbols("k1 k2 k3", real=True)
kP = sp.Matrix([k1, k2, k3])
gcon = k1 ** 2 + k2 ** 2 + k3 ** 2 - 1


def reduce_mod_unit(expr):
    expr = sp.expand(expr)
    if expr == 0:
        return 0
    _, r = sp.reduced(expr, [gcon], k3, k2, k1, order="lex")
    return sp.expand(r)


def tt_poly_zero(T):
    L = LamS(T, kP)
    return all(reduce_mod_unit(e) == 0 for e in L)


S_poly = symS(kP * Avec.T)
check("1.2b Lambda(k) sym(k (x) a) reduces to 0 modulo |k|^2 = 1 (polynomial ideal; no angle parametrisation)",
      tt_poly_zero(S_poly))
nonzero_without_constraint = any(sp.expand(e) != 0 for e in LamS(S_poly, kP))
print("      (as raw polynomials, without using |k| = 1, the entries are nonzero:", nonzero_without_constraint,
      "-> the identity uses only k.k = 1)")
b1, b2, b3 = sp.symbols("b1 b2 b3", real=True)
Vgen = sp.Matrix([b1, b2, b3])
check("1.2c Lambda(k) sym(k (x) v) == 0 for ANY vector v (covers any plane-wave vector field: mirror offsets, k x a, ...)",
      tt_poly_zero(symS(kP * Vgen.T)))
# Most general symmetric rank-2 tensor linear in a built from k, delta_ij, eps_ijk (isotropic, even hemitropic):
#   C_ijl(k) a_l with C symmetric in ij  ->  four structures
iso_structs = {
    "sym(k (x) a)": symS(kP * Avec.T),
    "(k.a) I": (kP.dot(Avec)) * I3,
    "(k.a) k k": (kP.dot(Avec)) * kP * kP.T,
    "sym(k (x) (k x a))  [hemitropic]": symS(kP * (kP.cross(Avec)).T),
}
for nm, T in iso_structs.items():
    check("1.2d Lambda(k)[" + nm + "] == 0 mod |k| = 1", tt_poly_zero(T))
print("      => any symmetric tensor linear in the amplitude of ONE plane wave, built with an isotropic (even chiral)")
print("         response, has zero TT part. Reason: k is invariant under rotations about k (helicity 0) and a carries")
print("         helicities 0, +-1 only, so nothing linear in a can carry helicity +-2.")

sub("1.3 helicity decomposition about k")
e_p = (mS - sp.I * nS) / sp.sqrt(2)  # helicity +1 under right-handed rotation about k
e_m = (mS + sp.I * nS) / sp.sqrt(2)  # helicity -1


def Rk(k, ang):
    K = sp.Matrix([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return sp.cos(ang) * sp.eye(3) + sp.sin(ang) * K + (1 - sp.cos(ang)) * k * k.T


Rka = Rk(kS, al)
check("1.3a rotation by alpha about k: e_(+-) -> exp(+-i alpha) e_(+-)",
      all(zero_expr(sp.expand_complex(e)) for e in (Rka * e_p - sp.exp(sp.I * al) * e_p)) and
      all(zero_expr(sp.expand_complex(e)) for e in (Rka * e_m - sp.exp(-sp.I * al) * e_m)))
Hb = {
    "+2": e_p * e_p.T,
    "-2": e_m * e_m.T,
    "+1": (kS * e_p.T + e_p * kS.T) / sp.sqrt(2),
    "-1": (kS * e_m.T + e_m * kS.T) / sp.sqrt(2),
    "0_l (k k)": kS * kS.T,
    "0_b (P/sqrt2)": (e_p * e_m.T + e_m * e_p.T) / sp.sqrt(2),
}
keys = list(Hb.keys())


def hdot(Am, Bm):  # <A,B> = sum conj(A_ij) B_ij
    return sum(sp.conjugate(Am[i, j]) * Bm[i, j] for i in range(3) for j in range(3))


gram_ok = True
for i, ki in enumerate(keys):
    for j, kj in enumerate(keys):
        if not zero_expr(sp.expand_complex(hdot(Hb[ki], Hb[kj])) - (1 if i == j else 0)):
            gram_ok = False
check("1.3b helicity basis {E_+2, E_-2, E_+1, E_-1, E_0l = kk, E_0b = P/sqrt2} is orthonormal (Hermitian)", gram_ok)
eps_unit = symS(kS * Avec.T)  # strain per unit (-f'/c)
comps = {kk_: sp.simplify(sp.expand_complex(hdot(Hb[kk_], eps_unit))) for kk_ in keys}
a_plus = sp.simplify(sp.expand_complex(sp.conjugate(e_p).dot(Avec)))
a_minus = sp.simplify(sp.expand_complex(sp.conjugate(e_m).dot(Avec)))
a_par = sp.simplify(kS.dot(Avec))
print("  components of sym(k (x) a) (multiply by -f'/c for eps):")
for kk_ in keys:
    print("     helicity %-14s : %s" % (kk_, comps[kk_]))
check("1.3c helicity +-2 components of eps vanish identically (arbitrary a, k)",
      zero_expr(comps["+2"]) and zero_expr(comps["-2"]))
check("1.3d helicity +-1 components = a_(+-)/sqrt2 with a_(+-) = conj(e_(+-)).a  (the transverse part of a)",
      zero_expr(comps["+1"] - a_plus / sp.sqrt(2)) and zero_expr(comps["-1"] - a_minus / sp.sqrt(2)))
check("1.3e helicity-0: k k component = k.a (longitudinal); transverse-trace (breathing) component = 0",
      zero_expr(comps["0_l (k k)"] - a_par) and zero_expr(comps["0_b (P/sqrt2)"]))
recon = sum((comps[kk_] * Hb[kk_] for kk_ in keys), sp.zeros(3, 3))
check("1.3f reconstruction sum_lambda h_lambda E_lambda = sym(k (x) a) (completeness)",
      all(zero_expr(sp.expand_complex(e)) for e in (recon - eps_unit)))
# spin weight via annihilators: rotate a about k by alpha, everything else fixed
eps_rot = symS(kS * (Rka * Avec).T)
ann1 = sp.diff(eps_rot, al, 3) + sp.diff(eps_rot, al)          # kills {1, cos a, sin a}
check("1.3g eps(R_k(alpha) a) satisfies (d^3/dalpha^3 + d/dalpha) eps = 0  -> harmonics in alpha only 0, +-1",
      is_zero_matrix(ann1))
b1s, b2s = sp.symbols("b1 b2", real=True)
aperp_gen = b1s * mS + b2s * nS                                 # general transverse amplitude
aa_rot = (Rka * aperp_gen) * (Rka * aperp_gen).T
ann1_aa = sp.diff(aa_rot, al, 3) + sp.diff(aa_rot, al)
ann2_aa = sp.diff(aa_rot, al, 3) + 4 * sp.diff(aa_rot, al)    # kills {1, cos 2a, sin 2a}
check("1.3h control: second-order a_perp(x)a_perp is NOT annihilated by the spin-1 operator but IS by the spin-2 one",
      (not is_zero_matrix(ann1_aa)) and is_zero_matrix(ann2_aa))
aa_gen = (Rka * Avec) * (Rka * Avec).T                          # general a: harmonics 0, +-1, +-2
ann12 = sp.diff(aa_gen, al, 5) + 5 * sp.diff(aa_gen, al, 3) + 4 * sp.diff(aa_gen, al)
check("1.3i control: general a(x)a is annihilated only by the {0,+-1,+-2} operator (d^5 + 5d^3 + 4d)",
      is_zero_matrix(ann12) and not is_zero_matrix(sp.diff(aa_gen, al, 3) + 4 * sp.diff(aa_gen, al)))

sub("1.4 the fixed six-tensor basis of the brief (symbolic in theta, phi, psi)")
pS = sp.cos(ps) * mS + sp.sin(ps) * nS
qS = -sp.sin(ps) * mS + sp.cos(ps) * nS
NAMES = ["plus", "cross", "x", "y", "b", "l"]
eS = {
    "plus": pS * pS.T - qS * qS.T,
    "cross": pS * qS.T + qS * pS.T,
    "x": pS * kS.T + kS * pS.T,
    "y": qS * kS.T + kS * qS.T,
    "b": pS * pS.T + qS * qS.T,
    "l": sp.sqrt(2) * kS * kS.T,
}
xh = sp.Matrix([1, 0, 0])
yh = sp.Matrix([0, 1, 0])
DS = (xh * xh.T - yh * yh.T) / 2


def ddS(Am, Bm):
    return sum(Am[i, j] * Bm[i, j] for i in range(3) for j in range(3))


gram_ok6 = all(zero_expr(ddS(eS[NAMES[i]], eS[NAMES[j]]) - (2 if i == j else 0)) for i in range(6) for j in range(6))
check("1.4a Gram matrix e_A : e_B = 2 delta_AB (orthogonal basis of symmetric 3x3 tensors)", gram_ok6)
check("1.4b Lambda(k) e_+ = e_+, Lambda(k) e_cross = e_cross; Lambda kills e_x, e_y, e_b, e_l",
      is_zero_matrix(LamS(eS["plus"], kS) - eS["plus"]) and is_zero_matrix(LamS(eS["cross"], kS) - eS["cross"]) and
      all(is_zero_matrix(LamS(eS[nm], kS)) for nm in ["x", "y", "b", "l"]))
aT = sp.cos(chi) * pS + sp.sin(chi) * qS
epsT = symS(kS * aT.T)
epsL = symS(kS * kS.T)
cT = {nm: sp.simplify(ddS(epsT, eS[nm]) / 2) for nm in NAMES}
cL = {nm: sp.simplify(ddS(epsL, eS[nm]) / 2) for nm in NAMES}
print("  transverse test wave a_T = cos(chi) p + sin(chi) q :", cT)
print("  longitudinal test wave a_L = k                     :", cL)
check("1.4c transverse: c_x = cos(chi)/2, c_y = sin(chi)/2, c_+ = c_cross = c_b = c_l = 0  (exact)",
      zero_expr(ddS(epsT, eS["x"]) / 2 - sp.cos(chi) / 2) and zero_expr(ddS(epsT, eS["y"]) / 2 - sp.sin(chi) / 2) and
      all(zero_expr(ddS(epsT, eS[nm])) for nm in ["plus", "cross", "b", "l"]))
check("1.4d longitudinal: c_l = 1/sqrt2, all others 0 (exact; note c_b = 0: no breathing content)",
      zero_expr(ddS(epsL, eS["l"]) / 2 - 1 / sp.sqrt(2)) and
      all(zero_expr(ddS(epsL, eS[nm])) for nm in ["plus", "cross", "x", "y", "b"]))
F_pred = {
    "plus": sp.Rational(1, 2) * (1 + sp.cos(th) ** 2) * sp.cos(2 * ph) * sp.cos(2 * ps) - sp.cos(th) * sp.sin(2 * ph) * sp.sin(2 * ps),
    "cross": -sp.Rational(1, 2) * (1 + sp.cos(th) ** 2) * sp.cos(2 * ph) * sp.sin(2 * ps) - sp.cos(th) * sp.sin(2 * ph) * sp.cos(2 * ps),
    "x": sp.sin(th) * (sp.cos(th) * sp.cos(2 * ph) * sp.cos(ps) - sp.sin(2 * ph) * sp.sin(ps)),
    "y": -sp.sin(th) * (sp.cos(th) * sp.cos(2 * ph) * sp.sin(ps) + sp.sin(2 * ph) * sp.cos(ps)),
    "b": -sp.Rational(1, 2) * sp.sin(th) ** 2 * sp.cos(2 * ph),
    "l": sp.sin(th) ** 2 * sp.cos(2 * ph) / sp.sqrt(2),
}
F_ok = all(zero_expr(ddS(DS, eS[nm]) - F_pred[nm]) for nm in NAMES)
check("1.4e antenna patterns F_A = D:e_A in closed form (F_+,F_cross ~ 2psi; F_x,F_y ~ psi; F_b,F_l psi-free; F_l = -sqrt2 F_b)",
      F_ok and zero_expr(F_pred["l"] + sp.sqrt(2) * F_pred["b"]))
for nm in NAMES:
    print("     F_%-5s = %s" % (nm, F_pred[nm]))
RT_pred = sp.sin(th) / 2 * (sp.cos(th) * sp.cos(2 * ph) * sp.cos(ps + chi) - sp.sin(2 * ph) * sp.sin(ps + chi))
RL_pred = sp.sin(th) ** 2 * sp.cos(2 * ph) / 2
check("1.4f R_T = D:eps_T = sum c_A F_A = (1/2) sin(th)[cos(th) cos(2ph) cos(psi+chi) - sin(2ph) sin(psi+chi)]  (spin weight 1)",
      zero_expr(ddS(DS, epsT) - RT_pred) and zero_expr(sum(cT[nm] * F_pred[nm] for nm in NAMES) - RT_pred))
check("1.4g R_L = D:eps_L = (1/2) sin(th)^2 cos(2ph)  (psi-independent: spin weight 0)",
      zero_expr(ddS(DS, epsL) - RL_pred))

# ======================================================================================================
hdr("TASK 2  Antenna mapping on the fixed grid (numerical, three routes + finite arms + psi-Fourier)")

SQ2 = math.sqrt(2.0)
XH, YH, ZH = np.eye(3)
DET = 0.5 * (np.outer(XH, XH) - np.outer(YH, YH))
THETAS = [0.3, 0.9, 1.5, 2.2, 2.9]
PHIS = [0.0, 0.7, 2.1, 4.0]
PSIS = [0.0, 0.4, 1.1]
CHIS = [0.0, 0.5, 1.3]


def frame(theta, phi, psi):
    st, ct, sph, cph = math.sin(theta), math.cos(theta), math.sin(phi), math.cos(phi)
    k = np.array([st * cph, st * sph, ct])
    m = np.array([ct * cph, ct * sph, -st])
    n = np.array([-sph, cph, 0.0])
    p = math.cos(psi) * m + math.sin(psi) * n
    q = -math.sin(psi) * m + math.cos(psi) * n
    return k, m, n, p, q


def basis6(k, p, q):
    o = np.outer
    return {"plus": o(p, p) - o(q, q), "cross": o(p, q) + o(q, p), "x": o(p, k) + o(k, p),
            "y": o(q, k) + o(k, q), "b": o(p, p) + o(q, q), "l": SQ2 * o(k, k)}


def dd(Am, Bm):
    return float(np.sum(Am * Bm))


def symo(u, v):
    return 0.5 * (np.outer(u, v) + np.outer(v, u))


def Lam(T, k):
    P = np.eye(3) - np.outer(k, k)
    return P @ T @ P - 0.5 * P * np.trace(P @ T)


def voigt(T):
    return np.array([T[0, 0], T[1, 1], T[2, 2], T[0, 1], T[0, 2], T[1, 2]])


def decompose(eps, E):
    """route A1: orthogonal projection; route A2: generic 6x6 linear solve (no orthogonality assumed)."""
    cA1 = {nm: dd(eps, E[nm]) / dd(E[nm], E[nm]) for nm in NAMES}
    M = np.column_stack([voigt(E[nm]) for nm in NAMES])
    sol = np.linalg.solve(M, voigt(eps))
    cA2 = {nm: float(sol[i]) for i, nm in enumerate(NAMES)}
    return cA1, cA2


def F_closed(theta, phi, psi):
    st, ct = math.sin(theta), math.cos(theta)
    c2p, s2p = math.cos(2 * phi), math.sin(2 * phi)
    return {"plus": 0.5 * (1 + ct * ct) * c2p * math.cos(2 * psi) - ct * s2p * math.sin(2 * psi),
            "cross": -0.5 * (1 + ct * ct) * c2p * math.sin(2 * psi) - ct * s2p * math.cos(2 * psi),
            "x": st * (ct * c2p * math.cos(psi) - s2p * math.sin(psi)),
            "y": -st * (ct * c2p * math.sin(psi) + s2p * math.cos(psi)),
            "b": -0.5 * st * st * c2p, "l": st * st * c2p / SQ2}


grid_T, grid_L = [], []
mx = {"cA1_vs_cA2": 0.0, "cA_vs_closed": 0.0, "R_sum_vs_DDeps": 0.0, "R_vs_closed": 0.0, "F_vs_closed": 0.0,
      "recon": 0.0, "T_tensor_coeffs": 0.0, "T_scalar_coeffs": 0.0, "L_nonl_coeffs": 0.0, "TT_norm": 0.0}
for theta in THETAS:
    for phi in PHIS:
        for psi in PSIS:
            k, m, n, p, q = frame(theta, phi, psi)
            E = basis6(k, p, q)
            F = {nm: dd(DET, E[nm]) for nm in NAMES}
            Fc = F_closed(theta, phi, psi)
            mx["F_vs_closed"] = max(mx["F_vs_closed"], max(abs(F[nm] - Fc[nm]) for nm in NAMES))
            for chv in CHIS:
                a = math.cos(chv) * p + math.sin(chv) * q
                eps = symo(k, a)
                cA1, cA2 = decompose(eps, E)
                closed = {"plus": 0.0, "cross": 0.0, "x": 0.5 * math.cos(chv), "y": 0.5 * math.sin(chv), "b": 0.0, "l": 0.0}
                R = sum(cA1[nm] * F[nm] for nm in NAMES)
                R_dd = dd(DET, eps)
                R_cl = 0.5 * math.sin(theta) * (math.cos(theta) * math.cos(2 * phi) * math.cos(psi + chv)
                                                - math.sin(2 * phi) * math.sin(psi + chv))
                mx["cA1_vs_cA2"] = max(mx["cA1_vs_cA2"], max(abs(cA1[nm] - cA2[nm]) for nm in NAMES))
                mx["cA_vs_closed"] = max(mx["cA_vs_closed"], max(abs(cA1[nm] - closed[nm]) for nm in NAMES))
                mx["R_sum_vs_DDeps"] = max(mx["R_sum_vs_DDeps"], abs(R - R_dd))
                mx["R_vs_closed"] = max(mx["R_vs_closed"], abs(R - R_cl))
                mx["recon"] = max(mx["recon"], np.abs(sum(cA1[nm] * E[nm] for nm in NAMES) - eps).max())
                mx["T_tensor_coeffs"] = max(mx["T_tensor_coeffs"], abs(cA1["plus"]), abs(cA1["cross"]))
                mx["T_scalar_coeffs"] = max(mx["T_scalar_coeffs"], abs(cA1["b"]), abs(cA1["l"]))
                mx["TT_norm"] = max(mx["TT_norm"], np.abs(Lam(eps, k)).max())
                grid_T.append({"theta": theta, "phi": phi, "psi": psi, "chi": chv,
                               "c_plus": cA1["plus"], "c_cross": cA1["cross"], "c_x": cA1["x"], "c_y": cA1["y"],
                               "c_b": cA1["b"], "c_l": cA1["l"], "R": R})
            epsL = np.outer(k, k)
            cA1, cA2 = decompose(epsL, E)
            R = sum(cA1[nm] * F[nm] for nm in NAMES)
            mx["cA1_vs_cA2"] = max(mx["cA1_vs_cA2"], max(abs(cA1[nm] - cA2[nm]) for nm in NAMES))
            mx["cA_vs_closed"] = max(mx["cA_vs_closed"], abs(cA1["l"] - 1 / SQ2))
            mx["L_nonl_coeffs"] = max(mx["L_nonl_coeffs"], max(abs(cA1[nm]) for nm in ["plus", "cross", "x", "y", "b"]))
            mx["R_sum_vs_DDeps"] = max(mx["R_sum_vs_DDeps"], abs(R - dd(DET, epsL)))
            mx["R_vs_closed"] = max(mx["R_vs_closed"], abs(R - 0.5 * math.sin(theta) ** 2 * math.cos(2 * phi)))
            mx["TT_norm"] = max(mx["TT_norm"], np.abs(Lam(epsL, k)).max())
            grid_L.append({"theta": theta, "phi": phi, "psi": psi,
                           "c_plus": cA1["plus"], "c_cross": cA1["cross"], "c_x": cA1["x"], "c_y": cA1["y"],
                           "c_b": cA1["b"], "c_l": cA1["l"], "R": R})

print("  grid: %d transverse points, %d longitudinal points" % (len(grid_T), len(grid_L)))
for kk_, v in mx.items():
    print("     max |%s| = %.3e" % (kk_, v))
check("2.1 route A1 (projection) == route A2 (6x6 solve) for all c_A to 1e-14", mx["cA1_vs_cA2"] < 1e-14)
check("2.2 numeric c_A == symbolic closed form (c_x = cos chi/2, c_y = sin chi/2; c_l = 1/sqrt2) to 1e-14",
      mx["cA_vs_closed"] < 1e-14)
check("2.3 R = sum_A c_A F_A == D:eps == closed form to 1e-14", mx["R_sum_vs_DDeps"] < 1e-14 and mx["R_vs_closed"] < 1e-14)
check("2.4 numeric F_A == closed forms of 1.4e to 1e-14; basis reconstruction exact", mx["F_vs_closed"] < 1e-14 and mx["recon"] < 1e-14)
check("2.5 transverse wave: |c_+|, |c_cross| <= 1e-15 and |c_b|, |c_l| <= 1e-15 at every grid point (pure x/y = vector)",
      mx["T_tensor_coeffs"] <= 1e-15 and mx["T_scalar_coeffs"] <= 1e-15)
check("2.6 longitudinal wave: only c_l nonzero (|others| <= 1e-15) (pure scalar, longitudinal)", mx["L_nonl_coeffs"] <= 1e-15)
check("2.7 Lambda(k) eps numerically ~0 at every grid point (max entry <= 1e-15)", mx["TT_norm"] <= 1e-15)

out_json = os.path.join(HERE, "leg2_grid.json")
with open(out_json, "w") as fh:
    json.dump({"transverse": grid_T, "longitudinal": grid_L}, fh, indent=1)
print("  wrote", out_json)

# ----------------------------------------------------------------------- route (b): finite arms, direct integration
sub("2.B finite arms: integrate the displacement gradient along each arm (complex-step derivative of u itself)")
GLX, GLW = np.polynomial.legendre.leggauss(64)
HCS = 1e-30  # complex-step size


class Field:
    """Generic displacement field; derivatives by complex step on u itself (no strain formula used)."""

    def u(self, xs, ts):  # xs (N,3) complex, ts (N,) complex  ->  (N,3) complex
        raise NotImplementedError

    def grad(self, xs, ts):  # (N,3,3) with [n,i,j] = d_j u_i
        G = np.empty((len(ts), 3, 3))
        for j in range(3):
            xc = xs.astype(complex)
            xc[:, j] += 1j * HCS
            G[:, :, j] = self.u(xc, ts.astype(complex)).imag / HCS
        return G

    def strain_velocity(self, xs, ts):
        G = self.grad(xs, ts)
        eps = 0.5 * (G + G.transpose(0, 2, 1))
        w = self.u(xs.astype(complex), ts.astype(complex) + 1j * HCS).imag / HCS
        return eps, w

    def disp(self, x, tt):
        return self.u(np.asarray(x, dtype=complex)[None, :], np.array([tt], dtype=complex))[0].real


def f_ramp(tau):
    return tau


def f_sine(tau, Om=2 * math.pi):  # lambda = 1 (c = 1); a generic two-tone waveform
    return np.sin(Om * tau) + 0.3 * np.cos(1.7 * Om * tau + 0.4)


class PlaneWave(Field):
    def __init__(self, k, a, f, cw=1.0):
        self.k, self.a, self.f, self.cw = np.asarray(k, float), np.asarray(a, float), f, cw

    def u(self, xs, ts):
        tau = ts - (xs @ self.k) / self.cw
        return self.f(tau)[:, None] * self.a[None, :]


def arm_length_change(field, uhat, L, tt):
    """delta L(t) = int_0^L uhat . d/ds u(s uhat, t) ds  (material arm, mirrors at material points)."""
    s = 0.5 * L * (GLX + 1.0)
    wq = 0.5 * L * GLW
    xs = s[:, None] * uhat[None, :]
    G = field.grad(xs, np.full(len(s), tt))
    integrand = np.einsum("i,nij,j->n", uhat, G, uhat)
    return float(wq @ integrand)


# (b1) uniform-strain limit: ramp waveform, compare with the grid R
mxb = 0.0
for e in grid_T:
    k, m, n, p, q = frame(e["theta"], e["phi"], e["psi"])
    a = math.cos(e["chi"]) * p + math.sin(e["chi"]) * q
    fld = PlaneWave(k, a, f_ramp)
    L = 0.7
    dL = arm_length_change(fld, XH, L, 0.3) - arm_length_change(fld, YH, L, 0.3)
    mxb = max(mxb, abs(-dL / (2 * L) - e["R"]))
for e in grid_L:
    k, m, n, p, q = frame(e["theta"], e["phi"], e["psi"])
    fld = PlaneWave(k, k, f_ramp)
    L = 0.7
    dL = arm_length_change(fld, XH, L, 0.3) - arm_length_change(fld, YH, L, 0.3)
    mxb = max(mxb, abs(-dL / (2 * L) - e["R"]))
check("2.B1 uniform strain (ramp f): -[dL_x - dL_y]/(2L) from direct arm integration == grid R (all 240 points) to 1e-13",
      mxb < 1e-13, "max diff %.2e" % mxb)

# (b2) finite arm L/lambda = 0.3, generic waveform: closed form and psi spin weight
NPSI = 32
PSIGRID = 2 * math.pi * np.arange(NPSI) / NPSI


def harm(vals):
    H = np.fft.fft(np.asarray(vals)) / len(vals)
    Nn = len(vals)
    return [max(abs(H[mm % Nn]), abs(H[(-mm) % Nn])) for mm in range(0, 6)]


def sky_points():
    for theta in THETAS:
        for phi in PHIS:
            yield theta, phi


Lfin = 0.3
mx_cf = 0.0
hT = np.zeros(6)
hL = np.zeros(6)
for theta, phi in sky_points():
    for chv in CHIS:
        for tt in (0.0, 0.37):
            vals = []
            for psi in PSIGRID:
                k, m, n, p, q = frame(theta, phi, psi)
                a = math.cos(chv) * p + math.sin(chv) * q
                fld = PlaneWave(k, a, f_sine)
                dLx = arm_length_change(fld, XH, Lfin, tt)
                dLy = arm_length_change(fld, YH, Lfin, tt)
                cfx = (XH @ a) * (f_sine(np.array([tt - Lfin * (k @ XH)]))[0] - f_sine(np.array([tt]))[0])
                cfy = (YH @ a) * (f_sine(np.array([tt - Lfin * (k @ YH)]))[0] - f_sine(np.array([tt]))[0])
                mx_cf = max(mx_cf, abs(dLx - cfx), abs(dLy - cfy))
                vals.append(dLx - dLy)
            hT = np.maximum(hT, harm(vals))
    for tt in (0.0, 0.37):
        vals = []
        for psi in PSIGRID:
            k, m, n, p, q = frame(theta, phi, psi)
            fld = PlaneWave(k, k, f_sine)
            vals.append(arm_length_change(fld, XH, Lfin, tt) - arm_length_change(fld, YH, Lfin, tt))
        hL = np.maximum(hL, harm(vals))
check("2.B2 finite arm: quadrature of grad u == closed form (u.a)[f(t - L k.u/c) - f(t)] to 1e-13", mx_cf < 1e-13,
      "max diff %.2e" % mx_cf)
print("  finite-arm (L/lambda = %.2f) differential length, max psi-harmonic amplitude |H_m| over sky x chi x t:" % Lfin)
print("     transverse  : " + "  ".join("m=%d: %.2e" % (mm, hT[mm]) for mm in range(6)))
print("     longitudinal: " + "  ".join("m=%d: %.2e" % (mm, hL[mm]) for mm in range(6)))
check("2.B3 transverse wave, finite arms: |H_m>=2| <= 1e-14 * |H_1|  (spin weight 1, not 2)",
      max(hT[2:]) <= 1e-14 * hT[1] and hT[1] > 1e-3, "H1=%.3e, max H>=2 = %.2e" % (hT[1], max(hT[2:])))
check("2.B4 longitudinal wave, finite arms: only m = 0 (spin weight 0)", max(hL[1:]) <= 1e-14 * hL[0] and hL[0] > 1e-3)


# positive control for route (b): a metric-type TT wave h = (h+ e+ + hx ex) f(t - k.x/c), dL = (1/2) int u.h.u ds
def tt_arm(k, p, q, hp, hx, uhat, L, tt):
    E = basis6(k, p, q)
    H = hp * E["plus"] + hx * E["cross"]
    s = 0.5 * L * (GLX + 1.0)
    wq = 0.5 * L * GLW
    fv = f_sine(tt - s * (k @ uhat))
    return float(wq @ (0.5 * (uhat @ H @ uhat) * fv))


hGR = np.zeros(6)
for theta, phi in sky_points():
    vals = []
    for psi in PSIGRID:
        k, m, n, p, q = frame(theta, phi, psi)
        vals.append(tt_arm(k, p, q, 1.0, 0.3, XH, Lfin, 0.2) - tt_arm(k, p, q, 1.0, 0.3, YH, Lfin, 0.2))
    hGR = np.maximum(hGR, harm(vals))
print("     GR control  : " + "  ".join("m=%d: %.2e" % (mm, hGR[mm]) for mm in range(6)))
check("2.B5 positive control: a TT (metric-type) wave through the same pipeline shows ONLY m = +-2",
      hGR[2] > 1e-3 and max(hGR[0], hGR[1], hGR[3], hGR[4], hGR[5]) <= 1e-14 * hGR[2])

# ----------------------------------------------------------------------- route (c): Fourier analysis of R in psi
sub("2.C Fourier analysis in psi of R = sum c_A F_A and of each F_A")
hR = np.zeros(6)
hRL = np.zeros(6)
hF = {nm: np.zeros(6) for nm in NAMES}
for theta, phi in sky_points():
    for chv in CHIS:
        vals = []
        for psi in PSIGRID:
            k, m, n, p, q = frame(theta, phi, psi)
            E = basis6(k, p, q)
            a = math.cos(chv) * p + math.sin(chv) * q
            cA1, _ = decompose(symo(k, a), E)
            vals.append(sum(cA1[nm] * dd(DET, E[nm]) for nm in NAMES))
        hR = np.maximum(hR, harm(vals))
    valsL = []
    Fv = {nm: [] for nm in NAMES}
    for psi in PSIGRID:
        k, m, n, p, q = frame(theta, phi, psi)
        E = basis6(k, p, q)
        valsL.append(dd(DET, np.outer(k, k)))
        for nm in NAMES:
            Fv[nm].append(dd(DET, E[nm]))
    hRL = np.maximum(hRL, harm(valsL))
    for nm in NAMES:
        hF[nm] = np.maximum(hF[nm], harm(Fv[nm]))
print("     R_T(psi)    : " + "  ".join("m=%d: %.2e" % (mm, hR[mm]) for mm in range(6)))
print("     R_L(psi)    : " + "  ".join("m=%d: %.2e" % (mm, hRL[mm]) for mm in range(6)))
for nm in NAMES:
    print("     F_%-5s     : " % nm + "  ".join("m=%d: %.2e" % (mm, hF[nm][mm]) for mm in range(6)))
check("2.C1 R_T(psi): only m = +-1 (no m=0, no m=+-2)", hR[1] > 1e-3 and max(hR[0], hR[2], hR[3], hR[4], hR[5]) <= 1e-14 * hR[1])
check("2.C2 R_L(psi): only m = 0", hRL[0] > 1e-3 and max(hRL[1:]) <= 1e-14 * hRL[0])
spin_expect = {"plus": 2, "cross": 2, "x": 1, "y": 1, "b": 0, "l": 0}
ok = True
for nm in NAMES:
    s_ = spin_expect[nm]
    others = [hF[nm][mm] for mm in range(6) if mm != s_]
    ok = ok and hF[nm][s_] > 1e-3 and max(others) <= 1e-14 * hF[nm][s_]
check("2.C3 method calibration: F_+,F_cross are spin 2; F_x,F_y spin 1; F_b,F_l spin 0", ok)

# ----------------------------------------------------------------------- sky averages (exact quadrature)
sub("2.D sky/polarisation averages (Gauss-Legendre in cos(theta) x uniform phi, psi, chi; exact for these trig polynomials)")
MU, MUW = np.polynomial.legendre.leggauss(24)
NPH = 16
PHQ = 2 * math.pi * np.arange(NPH) / NPH


def sky_average(func):
    tot = 0.0
    for mu, wmu in zip(MU, MUW):
        theta = math.acos(mu)
        for phi in PHQ:
            for psi in PHQ:
                tot += 0.5 * wmu * func(theta, phi, psi) / (NPH * NPH)
    return tot


F2 = {nm: sky_average(lambda th_, ph_, ps_, nm=nm: F_closed(th_, ph_, ps_)[nm] ** 2) for nm in NAMES}
print("     <F_A^2>: " + ", ".join("%s=%.15f" % (nm, F2[nm]) for nm in NAMES))
check("2.D1 <F_+^2>=<F_cross^2>=<F_x^2>=<F_y^2>=1/5, <F_b^2>=1/15, <F_l^2>=2/15",
      all(abs(F2[nm] - 0.2) < 1e-14 for nm in ["plus", "cross", "x", "y"]) and abs(F2["b"] - 1 / 15) < 1e-14
      and abs(F2["l"] - 2 / 15) < 1e-14)


def RT2_chi_avg(theta, phi, psi):
    tot = 0.0
    for chv in PHQ:
        tot += (0.5 * math.sin(theta) * (math.cos(theta) * math.cos(2 * phi) * math.cos(psi + chv)
                                         - math.sin(2 * phi) * math.sin(psi + chv))) ** 2
    return tot / NPH


RT2 = sky_average(RT2_chi_avg)
RL2 = sky_average(lambda th_, ph_, ps_: (0.5 * math.sin(th_) ** 2 * math.cos(2 * ph_)) ** 2)
print("     <R_T^2> = %.15f (expect 1/20), <R_L^2> = %.15f (expect 1/15); tensor part R_tensor = c_+ F_+ + c_cross F_cross = 0" % (RT2, RL2))
check("2.D2 <R_T^2> = 1/20, <R_L^2> = 1/15; tensor fraction f_T = <R_tensor^2>/<R^2> = 0 exactly (c_+ = c_cross = 0)",
      abs(RT2 - 0.05) < 1e-14 and abs(RL2 - 1 / 15) < 1e-14)

# ======================================================================================================
hdr("TASK 3  The medium's own detector (no metric assumed)")
print("""  Model (first order in the wave, eikonal along the unperturbed ray, c = c_T = 1):
    arm unit vector u, length L, BS at 0, end mirror at L u; probe polarisation e (e . u = 0);
    mirrors at material points: X_M(t) = X_M + u(X_M,t) [+ optional offset Delta(X_M,t)];
    probe speed relative to the local medium  c [1 + d],  d = alpha tr(eps) + beta u.eps.u + gamma e.eps.e
                                                         + zeta e.eps.(dir x e)   (zeta: hemitropic, odd in dir);
    probe advected by the local medium velocity w = du/dt (Galilean, first order).
    Round-trip time for detection at t (emission t0 = t - 2L/c):
      T - 2L/c = [2 u.U_E(t0+L/c) - u.U_B(t0) - u.U_B(t)]/c
                 - (1/c) int_0^L [d_fwd(s u, t0+s/c) + d_bwd(s u, t0+(2L-s)/c)] ds
                 - (1/c^2) int_0^L [u.w(s u, t0+s/c) - u.w(s u, t0+(2L-s)/c)] ds
    Differential signal  S = (T_x - T_y)  with probe polarisations e1 (x-arm), e2 (y-arm).""")


def roundtrip(field, uhat, ehat, t_det, L, co, offsets=None, cc=1.0):
    t0 = t_det - 2 * L / cc
    t1 = t0 + L / cc

    def mirror(xpos, tt, which):
        d_ = field.disp(xpos, tt)
        if offsets is not None:
            d_ = d_ + offsets(np.asarray(xpos, float), tt, which)
        return d_

    UE = mirror(L * uhat, t1, "END")
    UB0 = mirror(0 * uhat, t0, "BS")
    UB2 = mirror(0 * uhat, t_det, "BS")
    term_m = (2 * uhat @ UE - uhat @ UB0 - uhat @ UB2) / cc
    s = 0.5 * L * (GLX + 1.0)
    wq = 0.5 * L * GLW
    xs = s[:, None] * uhat[None, :]
    eps_f, w_f = field.strain_velocity(xs, t0 + s / cc)
    eps_b, w_b = field.strain_velocity(xs, t0 + (2 * L - s) / cc)

    def dspeed(eps, dvec):
        tr = np.trace(eps, axis1=1, axis2=2)
        uu = np.einsum("i,nij,j->n", uhat, eps, uhat)
        ee = np.einsum("i,nij,j->n", ehat, eps, ehat)
        ch = np.einsum("i,nij,j->n", ehat, eps, np.cross(dvec, ehat))
        return co["alpha"] * tr + co["beta"] * uu + co["gamma"] * ee + co["zeta"] * ch

    term_s = -(wq @ (dspeed(eps_f, uhat) + dspeed(eps_b, -uhat))) / cc
    term_a = -(wq @ (w_f @ uhat - w_b @ uhat)) / cc ** 2
    return term_m + term_s + term_a


def diff_signal(field, e1, e2, t_det, L, co, offsets=None):
    return roundtrip(field, XH, e1, t_det, L, co, offsets) - roundtrip(field, YH, e2, t_det, L, co, offsets)


COEF = {"alpha": 0.37, "beta": -0.81, "gamma": 1.23, "zeta": 0.58}  # arbitrary O(1) acoustoelastic constants
CONFIGS = {"V (e1 = e2 = z, vertical)": (ZH, ZH),
           "Hperp (e1 = y on x-arm, e2 = x on y-arm)": (YH, XH),
           "M (e1 = z, e2 = x; asymmetric control)": (ZH, XH)}
print("  acoustoelastic constants used:", COEF)


class StaticStrain(Field):
    def __init__(self, E):
        self.E = np.asarray(E, float)

    def u(self, xs, ts):
        return xs @ self.E.T + 0 * ts[:, None]


class Uniform(Field):  # rigid translation u = a f(t): no gradients at all
    def __init__(self, a, f):
        self.a, self.f = np.asarray(a, float), f

    def u(self, xs, ts):
        return self.f(ts)[:, None] * self.a[None, :] + 0 * xs


sub("3.1 rigid translation of medium + mirrors gives no signal (mirror motion and advection cancel exactly)")
mx_u = 0.0
for tt in (0.0, 0.21, 0.63):
    for a in (np.array([0.3, -0.7, 0.2]), np.array([1.0, 0.0, 0.0])):
        fld = Uniform(a, f_sine)
        for uhat in (XH, YH, ZH, np.array([0.6, 0.8, 0.0])):
            ehat = np.cross(uhat, np.array([0.1, 0.2, 0.97]))
            ehat /= np.linalg.norm(ehat)
            mx_u = max(mx_u, abs(roundtrip(fld, uhat, ehat, tt, 0.4, COEF)))
check("3.1 single-arm delay under u = a f(t) vanishes (finite L, generic f)", mx_u < 1e-14, "max %.2e" % mx_u)

sub("3.2 detector tensor G of the medium interferometer (long-wavelength), probed with static homogeneous strains")
basisE = []
for i in range(3):
    for j in range(i, 3):
        Eij = np.zeros((3, 3))
        Eij[i, j] = Eij[j, i] = 1.0 if i == j else 0.5
        basisE.append(((i, j), Eij))


def extract_G(e1, e2, L=0.5):
    G = np.zeros((3, 3))
    for (i, j), Eij in basisE:
        val = diff_signal(StaticStrain(Eij), e1, e2, 0.0, L, COEF) / (2 * L)  # S/T0 with T0 = 2L/c
        if i == j:
            G[i, i] = val
        else:
            G[i, j] = G[j, i] = val  # G:Eij = G_ij for the half-weighted off-diagonal basis element
    return G


Gs = {}
for nm, (e1, e2) in CONFIGS.items():
    G = extract_G(e1, e2)
    Gs[nm] = G
    pred = (1 - COEF["beta"]) * (np.outer(XH, XH) - np.outer(YH, YH)) - COEF["gamma"] * (np.outer(e1, e1) - np.outer(e2, e2))
    gD = dd(G, DET) / dd(DET, DET) / 2.0
    rest = G - 2 * gD * DET
    print("  %-44s G =\n%s" % (nm, np.array2string(G, precision=12, suppress_small=True)))
    print("      G = 2 B_eff D + G_rest with B_eff = %.12f, |G_rest| = %.2e, tr G = %.1e" % (gD, np.abs(rest).max(), np.trace(G)))
    check("3.2 [%s] G == (1-beta)(xx-yy) - gamma(e1e1 - e2e2) (alpha and zeta drop out); traceless" % nm.split()[0],
          np.abs(G - pred).max() < 1e-13 and abs(np.trace(G)) < 1e-13)
check("3.2b config V: G = 2(1-beta) D;  config Hperp: G = 2(1-beta+gamma) D  (standard L-shape detector tensor)",
      np.abs(Gs["V (e1 = e2 = z, vertical)"] - 2 * (1 - COEF["beta"]) * DET).max() < 1e-13 and
      np.abs(Gs["Hperp (e1 = y on x-arm, e2 = x on y-arm)"] - 2 * (1 - COEF["beta"] + COEF["gamma"]) * DET).max() < 1e-13)

sub("3.3 plane test waves, long-wavelength (ramp f -> uniform strain eps = -(1/c) sym(k (x) a)): reduce to standard patterns")
Beff = {"V (e1 = e2 = z, vertical)": 1 - COEF["beta"], "Hperp (e1 = y on x-arm, e2 = x on y-arm)": 1 - COEF["beta"] + COEF["gamma"]}
for nm, B in Beff.items():
    e1, e2 = CONFIGS[nm]
    mxd = 0.0
    L = 0.5
    for e in grid_T + grid_L:
        k, m, n, p, q = frame(e["theta"], e["phi"], e["psi"])
        a = (math.cos(e["chi"]) * p + math.sin(e["chi"]) * q) if "chi" in e else k
        S = diff_signal(PlaneWave(k, a, f_ramp), e1, e2, 0.3, L, COEF)
        # prediction: S/T0 = G:eps = 2 B D:(-sym(k a)) = -2 B R   ->   R_med := -S/(2 L * 2 B) must equal grid R
        mxd = max(mxd, abs(-S / (4 * L * B) - e["R"]))
    check("3.3 [%s] medium-detector signal = -(4L/c^2) B_eff * R_grid at all 240 grid points (B_eff = %.2f)" % (nm.split()[0], B),
          mxd < 1e-13, "max diff %.2e" % mxd)
print("  => transverse: S/T0 = -(f'/c) B_eff [cos(chi) F_x + sin(chi) F_y]   (vector patterns only)")
print("     longitudinal: S/T0 = -(f'/c) B_eff sin^2(theta) cos(2 phi) = -(f'/c) B_eff sqrt2 F_l = +(f'/c) 2 B_eff F_b (scalar)")

sub("3.4 finite arms (L/lambda = 0.3), generic waveform, all couplings on, + universal mirror offsets")
KAP = {"k1": 0.44, "k2": -0.29, "k3": 0.71}


def make_universal_offsets(k, a):
    kxa = np.cross(k, a)

    def off(xpos, tt, which):
        tau = np.array([tt - xpos @ k])
        fv = f_sine(tau)[0]
        fdv = (f_sine(tau.astype(complex) + 1j * HCS).imag / HCS)[0]
        return KAP["k1"] * a * fv + KAP["k2"] * (k @ a) * k * fdv + KAP["k3"] * kxa * fv
    return off


def make_nonuniversal_offsets(k, a, kB=0.9, kE=-0.35):
    def off(xpos, tt, which):
        fv = f_sine(np.array([tt - xpos @ k]))[0]
        return (kB if which == "BS" else kE) * a * fv
    return off


res34 = {}
for offname, maker in (("none", None), ("universal", make_universal_offsets), ("non-universal", make_nonuniversal_offsets)):
    for nm, (e1, e2) in CONFIGS.items():
        hTm = np.zeros(6)
        hLm = np.zeros(6)
        for theta, phi in sky_points():
            for chv in (0.0, 1.3):
                for tt in (0.0, 0.41):
                    vals = []
                    for psi in PSIGRID:
                        k, m, n, p, q = frame(theta, phi, psi)
                        a = math.cos(chv) * p + math.sin(chv) * q
                        off = maker(k, a) if maker else None
                        vals.append(diff_signal(PlaneWave(k, a, f_sine), e1, e2, tt, Lfin, COEF, off))
                    hTm = np.maximum(hTm, harm(vals))
            vals = []
            for psi in PSIGRID:
                k, m, n, p, q = frame(theta, phi, psi)
                off = maker(k, k) if maker else None
                vals.append(diff_signal(PlaneWave(k, k, f_sine), e1, e2, 0.41, Lfin, COEF, off))
            hLm = np.maximum(hLm, harm(vals))
        res34[(offname, nm)] = (hTm, hLm)
        print("  offsets=%-13s %-44s transverse |H_m|: %s" % (offname, nm, " ".join("%.1e" % v for v in hTm)))
        print("  %-27s %-44s longitud.  |H_m|: %s" % ("", "", " ".join("%.1e" % v for v in hLm)))
        check("3.4 [%s offsets, %s] transverse: |H_m>=2| <= 1e-13 |H_1|; longitudinal: only m=0" % (offname, nm.split()[0]),
              hTm[1] > 1e-4 and max(hTm[2:]) <= 1e-13 * hTm[1] and hLm[0] > 1e-5 and max(hLm[1:]) <= 1e-13 * hLm[0])
print("  => for every coupling, offset model and probe-polarisation choice the differential signal is linear in the")
print("     amplitude vector a; rotating a about k by psi can only produce harmonics 0, +-1. No helicity-2 term.")

# ======================================================================================================
hdr("TASK 4  Other possible sources of helicity 2")

sub("4a internal field components that are scalars under spatial rotation")
bsc1, bsc2 = sp.symbols("beta1 beta2", real=True)
T_int = bsc1 * I3 + bsc2 * kP * kP.T
check("4a.1 most general symmetric tensor linear in a rotation-scalar amplitude: beta1 I + beta2 k k ; Lambda(k) of it == 0",
      tt_poly_zero(T_int))
print("      rotation-scalars carry helicity 0 only (breathing/longitudinal patterns, psi-independent).")
print("      Only an internal field transforming as a spatial tensor of rank >= 2 (j >= 2) could carry +-2.")

sub("4b anisotropic single crystal (cubic 4th-rank response, strength eta) and its grain average")
rng = np.random.default_rng(20261006)


def rand_rot():
    qv = rng.normal(size=4)
    qv /= np.linalg.norm(qv)
    w, x, y, z = qv
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


d3 = np.eye(3)
QISO = (np.einsum("ij,kl->ijkl", d3, d3) + np.einsum("ik,jl->ijkl", d3, d3) + np.einsum("il,jk->ijkl", d3, d3)) / 5.0


def Qdev(Rc):
    Q = np.einsum("in,jn,kn,ln->ijkl", Rc, Rc, Rc, Rc)
    return Q - QISO


Rc0 = rand_rot()
Qd0 = Qdev(Rc0)
eta = 0.1
# the isotropic (orientation-averaged) part of the cubic tensor is exactly QISO:
Qavg_mc = sum(np.einsum("in,jn,kn,ln->ijkl", R_, R_, R_, R_) for R_ in (rand_rot() for _ in range(20000))) / 20000
check("4b.1 orientation average of sum_n c_n^(x4) -> (1/5)(dd+dd+dd) (Monte Carlo, 2e4 grains, tol 2e-2)",
      np.abs(Qavg_mc - QISO).max() < 2e-2, "max dev %.2e" % np.abs(Qavg_mc - QISO).max())
tt_ratio = []
hR4 = np.zeros(6)
hcp = np.zeros(6)
for theta, phi in sky_points():
    vals, cps = [], []
    for psi in PSIGRID:
        k, m, n, p, q = frame(theta, phi, psi)
        a = p
        S = symo(k, a)
        Teff = S + eta * np.einsum("ijkl,kl->ij", Qd0, S)
        tt_ratio.append(np.linalg.norm(Lam(Teff, k)) / np.linalg.norm(S))
        vals.append(dd(DET, Teff))
        cps.append(dd(Teff, basis6(k, p, q)["plus"]) / 2)
    hR4 = np.maximum(hR4, harm(vals))
    hcp = np.maximum(hcp, harm(cps))
print("     single crystal, eta = %.2f: |Lambda(k) T_eff| / |eps| ranges %.3e .. %.3e over the sky grid" % (eta, min(tt_ratio), max(tt_ratio)))
print("     R = D:T_eff psi-harmonics: " + " ".join("m=%d:%.1e" % (mm, hR4[mm]) for mm in range(6)))
print("     c_+(psi) of T_eff harmonics: " + " ".join("m=%d:%.1e" % (mm, hcp[mm]) for mm in range(6)))
check("4b.2 single crystal: Lambda(k) T_eff != 0 at O(eta) (tensor-pattern projection appears) ...", max(tt_ratio) > 0.1 * eta)
check("4b.3 ... but R(psi) stays spin-weight 1 (|H_m>=2| <= 1e-14 |H_1|): c_+, c_cross vary as psi, 3psi, not 2psi",
      max(hR4[2:]) <= 1e-14 * hR4[1] and hcp[2] <= 1e-14 * max(hcp) and hcp[1] > 0)
# exact isotropic average gives zero TT
mx_iso = 0.0
for theta, phi in sky_points():
    k, m, n, p, q = frame(theta, phi, 0.3)
    S = symo(k, p)
    Teff_iso = S + eta * np.einsum("ijkl,kl->ij", QISO, S)
    mx_iso = max(mx_iso, np.abs(Lam(Teff_iso, k)).max())
check("4b.4 untextured aggregate (exact orientation average): Lambda(k) T_eff == 0", mx_iso < 1e-15)
# (4a x 4b) an internal rotation-scalar amplitude seen through the same single-crystal map: T = beta k k + eta Qdev:(k k)
mx_sc_tt, hsc = 0.0, np.zeros(6)
for theta, phi in sky_points():
    vals = []
    for psi in PSIGRID:
        k, m, n, p, q = frame(theta, phi, psi)
        T = 0.3 * np.outer(k, k) + eta * np.einsum("ijkl,kl->ij", Qd0, np.outer(k, k))
        mx_sc_tt = max(mx_sc_tt, np.linalg.norm(Lam(T, k)))
        vals.append(dd(DET, T))
    hsc = np.maximum(hsc, harm(vals))
print("     rotation-scalar amplitude through the crystal map: max |Lambda(k) T| = %.3e, R(psi) harmonics m=0..2: %s"
      % (mx_sc_tt, " ".join("%.1e" % v for v in hsc[:3])))
check("4b.6 scalar amplitude x single-crystal map: TT projection O(eta) appears but R is psi-independent (spin 0)",
      mx_sc_tt > 1e-3 * eta and max(hsc[1:]) <= 1e-14 * hsc[0])
print("     N randomly oriented grains on the probe path (T_eff = eps + eta <Qdev>_N : eps):")
Ns = [1, 10, 100, 1000, 10000]
rms = []
for Ng in Ns:
    acc = []
    for rep in range(6):
        QN = sum(Qdev(rand_rot()) for _ in range(Ng)) / Ng
        for theta, phi in sky_points():
            k, m, n, p, q = frame(theta, phi, 0.0)
            S = symo(k, p)
            Teff = S + eta * np.einsum("ijkl,kl->ij", QN, S)
            acc.append((np.linalg.norm(Lam(Teff, k)) / np.linalg.norm(S)) ** 2)
    rms.append(math.sqrt(np.mean(acc)))
    print("        N = %6d   rms |TT|/|eps| = %.3e   (eta/sqrt(N) = %.3e)" % (Ng, rms[-1], eta / math.sqrt(Ng)))
slope = np.polyfit(np.log10(Ns), np.log10(rms), 1)[0]
check("4b.5 residual tensor projection of a textured average falls as N^(-1/2) (fitted slope %.3f)" % slope, abs(slope + 0.5) < 0.08)


MU12, MUW12 = np.polynomial.legendre.leggauss(12)


def fT_of(Tfun, axis=None):
    """f_T = <(D:Lambda(n) T)^2> / <(D:T)^2>, n = axis(k) (default n = k), averaged over the sky
    (12-pt Gauss-Legendre in cos theta x 8 phi) and over psi, chi (4 points each)."""
    num = den = 0.0
    for mu, wmu in zip(MU12, MUW12):
        theta = math.acos(mu)
        for phi in PHQ[::2]:
            for psi in PHQ[::4]:
                k, m, n, p, q = frame(theta, phi, psi)
                nax = k if axis is None else axis(k)
                for chv in PHQ[::4]:
                    a = math.cos(chv) * p + math.sin(chv) * q
                    T = Tfun(k, a)
                    num += wmu * dd(DET, Lam(T, nax)) ** 2
                    den += wmu * dd(DET, T) ** 2
    return num / den


fT_crys = np.mean([fT_of(lambda k, a, Qd=Qdev(rand_rot()): symo(k, a) + eta * np.einsum("ijkl,kl->ij", Qd, symo(k, a)))
                   for _ in range(8)])
print("     single-crystal tensor fraction (Lambda-projection definition): f_T ~ %.3e for eta = %.2f  (K = f_T/eta^2 = %.3f)"
      % (fT_crys, eta, fT_crys / eta ** 2))

sub("4c detector moving at V relative to the medium (Galilean-advection toy, quasi-static)")


def arm_delay_flow(uhat, W, w, eps):
    """first-order (in the wave) fractional round-trip delay of the probe in arm uhat with uniform medium flow W
    (detector frame), wave velocity field w and wave strain eps (mirrors follow the local medium displacement).
    Exact Galilean round trip: T = L/s+ + L/s-,  s+- = sqrt(c^2 - U_perp^2) +- U_par, U = W + lam w."""
    def T_of(lam):
        U = W + lam * w
        Upar = U @ uhat
        Uperp = U - Upar * uhat
        root = np.sqrt(1.0 - Uperp @ Uperp + 0j)
        return 1.0 / (root + Upar) + 1.0 / (root - Upar)
    T0 = T_of(0.0).real
    dT = T_of(1j * HCS).imag / HCS
    return uhat @ eps @ uhat + dT / T0


DIRS6 = [XH, YH, ZH, (XH + YH) / SQ2, (XH + ZH) / SQ2, (YH + ZH) / SQ2]


def Teff_from_arms(sig):
    T = np.zeros((3, 3))
    T[0, 0], T[1, 1], T[2, 2] = sig[0], sig[1], sig[2]
    T[0, 1] = T[1, 0] = sig[3] - 0.5 * (sig[0] + sig[1])
    T[0, 2] = T[2, 0] = sig[4] - 0.5 * (sig[0] + sig[2])
    T[1, 2] = T[2, 1] = sig[5] - 0.5 * (sig[1] + sig[2])
    return T


vmag = 1.2e-3
Vdir = np.array([0.31, -0.52, 0.795])
Vdir /= np.linalg.norm(Vdir)
Vvec = vmag * Vdir
mx_pred, mx_tilt, ttr = 0.0, 0.0, []
hV = np.zeros(6)
for theta, phi in sky_points():
    vals = []
    for psi in PSIGRID:
        k, m, n, p, q = frame(theta, phi, psi)
        a = p
        eps = -symo(k, a)  # f' = 1, c = 1
        sig = [arm_delay_flow(u_, -Vvec, a, eps) for u_ in DIRS6]
        Teff = Teff_from_arms(sig)
        vals.append(dd(DET, Teff))
        LT = Lam(Teff, k)
        mx_pred = max(mx_pred, np.abs(LT - (-Lam(symo(Vvec, a), k))).max() / vmag)
        ntilt = (k + Vvec) / np.linalg.norm(k + Vvec)
        mx_tilt = max(mx_tilt, np.abs(Lam(Teff, ntilt)).max())
        ttr.append(np.linalg.norm(LT) / np.linalg.norm(eps))
    hV = np.maximum(hV, harm(vals))
print("     |V|/c = %.1e: |Lambda(k) T_eff|/|eps| up to %.3e;  rel. deviation from -Lambda(k) sym(V (x) a)/c: %.1e"
      % (vmag, max(ttr), mx_pred))
print("     |Lambda(n_tilt) T_eff| with n_tilt = (k + V/c)/|k + V/c|: %.2e  (O(v^2))" % mx_tilt)
print("     R(psi) harmonics with V on: " + " ".join("m=%d:%.1e" % (mm, hV[mm]) for mm in range(6)))
check("4c.1 moving detector: Lambda(k) T_eff = -(1/c) Lambda(k) sym(V (x) a) + O(v^2) (tensor-pattern projection O(v/c))",
      mx_pred < 5e-3 and max(ttr) > 0.2 * vmag)
check("4c.2 ... equivalently a pure helicity-1 wave about the tilted axis k + V/c (residual O(v^2))", mx_tilt < 5 * vmag ** 2)
check("4c.3 ... and R(psi) is still spin-weight 1 (|H_m>=2| <= 1e-12 |H_1|)", max(hV[2:]) <= 1e-12 * hV[1])
# tensor fraction averaged over sky, psi, chi and V direction (Lambda-projection definition)
fTs, fTs_ray, fTs_tilt = [], [], []
for vd in (XH, YH, ZH, (XH + YH + ZH) / math.sqrt(3), Vdir, np.array([0.8, 0.0, -0.6])):
    Vv = vmag * vd / np.linalg.norm(vd)

    def Tflow(k, a, Vv=Vv):
        eps = -symo(k, a)
        return Teff_from_arms([arm_delay_flow(u_, -Vv, a, eps) for u_ in DIRS6])
    fTs.append(fT_of(Tflow))
    fTs_ray.append(fT_of(Tflow, axis=lambda k, Vv=Vv: (k - Vv) / np.linalg.norm(k - Vv)))
    fTs_tilt.append(fT_of(Tflow, axis=lambda k, Vv=Vv: (k + Vv) / np.linalg.norm(k + Vv)))
print("     f_T about the phase normal k, 6 V-directions: " + ", ".join("%.3e" % v for v in fTs))
print("     mean f_T(k)            = %.3e = %.3f (v/c)^2" % (np.mean(fTs), np.mean(fTs) / vmag ** 2))
print("     mean f_T(ray k - V/c)  = %.3e = %.3f (v/c)^2   (axis = detector-frame ray / apparent-source direction)"
      % (np.mean(fTs_ray), np.mean(fTs_ray) / vmag ** 2))
print("     mean f_T(tilt k + V/c) = %.3e                  (axis about which the toy response is pure helicity 1)"
      % np.mean(fTs_tilt))
check("4c.4 detector-motion tensor fraction is O((v/c)^2) ~ 1e-6 and depends on which O(v/c)-shifted axis defines 'k'",
      1e-7 < np.mean(fTs) < 1e-5 and 1e-7 < np.mean(fTs_ray) < 2e-5 and np.mean(fTs_tilt) < 1e-10)
# the same toy predicts an O(v^2) Michelson-Morley anisotropy of the unperturbed round trip
def T0_flow(uhat, W):
    Upar = W @ uhat
    Uperp = W - Upar * uhat
    root = math.sqrt(1.0 - Uperp @ Uperp)
    return 1.0 / (root + Upar) + 1.0 / (root - Upar)
mm_aniso = max(abs(T0_flow(XH, -vmag * vd) - T0_flow(YH, -vmag * vd)) / 2.0
               for vd in (XH, YH, (XH + ZH) / SQ2, Vdir))
print("     caveat: the same Galilean toy gives a Michelson-Morley round-trip anisotropy up to %.2e (~(v/c)^2/2);" % mm_aniso)
print("     modern MM/Kennedy-Thorndike bounds are many orders smaller, so a viable medium needs an emergent-Lorentz")
print("     compensation whose effect on the O(v/c) cross term is model-dependent (it can cancel it).")

sub("4d second order in the wave amplitude")
aa = Avec * Avec.T
# (grad u)(grad u)^T and (grad u)^T(grad u) for u = a f(t - k.x/c)
GG1 = sp.simplify(gradU * gradU.T - (fdot / c) ** 2 * Avec * Avec.T)
GG2 = sp.simplify(gradU.T * gradU - (fdot / c) ** 2 * Avec.dot(Avec) * kS * kS.T)
check("4d.1 (grad u)(grad u)^T = (f'/c)^2 a (x) a  [left Cauchy-Green];  (grad u)^T(grad u) = (f'/c)^2 |a|^2 k (x) k [Green-Lagrange]",
      is_zero_matrix(GG1) and is_zero_matrix(GG2))
aperp = sp.cos(al) * mS + sp.sin(al) * nS
LTaa = LamS(aperp * aperp.T, kS)
predaa = (sp.cos(2 * al) * (mS * mS.T - nS * nS.T) + sp.sin(2 * al) * (mS * nS.T + nS * mS.T)) / 2
check("4d.2 Lambda(k)(a (x) a) = (1/2)[cos(2 alpha) e+ + sin(2 alpha) e_cross] for transverse a: genuine helicity +-2 (spin weight 2)",
      is_zero_matrix(LTaa - predaa))
check("4d.3 Lambda(k)(k (x) k) == 0: the Green-Lagrange quadratic term is helicity 0 only", is_zero_matrix(LamS(kS * kS.T, kS)))
h_gw = 1e-21
print("     second-order tensor term / first-order vector term ~ |grad u| ~ h ~ %.0e  ->  f_T ~ h^2 ~ %.0e;" % (h_gw, h_gw ** 2))
print("     it oscillates at 2f (and 0), so it does not even share the linear waveform.")

sub("4e (extra) non-plane fields: superposed waves with directions differing by delta")
mx_lin = []
for delta in (1e-2, 1e-3, 1e-4):
    k, m, n, p, q = frame(0.9, 0.7, 0.0)
    k2 = math.cos(delta) * k + math.sin(delta) * m
    T = symo(k, p) + symo(k2, n)
    mx_lin.append(np.linalg.norm(Lam(T, k)) / delta)
print("     |Lambda(k)[sym(k a) + sym(k' a')]| / delta = " + ", ".join("%.4f" % v for v in mx_lin) + "  -> TT part ~ delta")
check("4e.1 TT part of a two-direction superposition scales linearly with the angle delta", np.ptp(mx_lin) < 1e-2 * mx_lin[0])
D_src = 40 * 3.0857e22          # m, ~40 Mpc (GW170817)
dt_coh = 0.01                   # s, ~1 cycle at 100 Hz: scattered paths must stay coherent with the template
delta_max = math.sqrt(2 * 2.998e8 * dt_coh / D_src)
print("     GW170817 scale: a mid-path deflection delta delays a path by D delta^2/(2c); coherence within ~%.0f ms over"
      " ~40 Mpc needs delta <~ %.1e rad -> TT amplitude fraction <~ %.0e, f_T <~ %.0e"
      % (dt_coh * 1e3, delta_max, delta_max, delta_max ** 2))

# ======================================================================================================
hdr("SUMMARY")
npass = sum(1 for r in RESULTS if r[1])
nfail = len(RESULTS) - npass
print("  checks: %d passed, %d failed" % (npass, nfail))
for r in RESULTS:
    if not r[1]:
        print("  FAILED:", r[0], r[2])
print("""
  CLASSIFICATION (isotropic medium, detector at rest in it, linear order):
    eps = -(f'/c) sym(k (x) a);  Lambda(k) eps == 0 identically (any k, any a).
    transverse wave  (a = cos chi p + sin chi q): c_x = cos(chi)/2, c_y = sin(chi)/2, all else 0 -> VECTOR (helicity +-1);
                     R = (1/2) sin(th)[cos(th) cos(2ph) cos(psi+chi) - sin(2ph) sin(psi+chi)], spin weight 1.
    longitudinal wave (a = k): c_l = 1/sqrt2, all else 0 (c_b = 0) -> SCALAR (helicity 0, longitudinal);
                     R = (1/2) sin^2(th) cos(2ph), spin weight 0.
    tensor content: none (c_+ = c_cross = 0; no 2psi harmonic), also for the medium's own interferometer.""")
sys.exit(0 if nfail == 0 else 1)
