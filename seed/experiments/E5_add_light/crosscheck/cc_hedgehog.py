"""E5 cross-check: hedgehog + electromagnetic static properties from the matrix Lagrangian.

Independent of the original E5 code.  Method:
  * profile: two-sided shooting (cc_profile), not a BVP collocation;
  * every density/current is obtained by numerically differentiating the matrix Lagrangian
    (Noether currents) or by evaluating the matrix baryon current, on a 3D quadrature grid;
  * the isoscalar magnetic moment is mu/J from the classical rotating hedgehog, with J computed as the
    Noether charge of spatial rotations (no rigid-body formula assumed);
  * the isovector magnetic moment uses <R_33> computed from explicit nucleon wavefunctions on S^3,
    with operator signs tied to the classical Noether charges by a numerical check at a generic A.
Run: NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 cc_hedgehog.py
Writes cc_hedgehog.json and cc_hedgehog_log.txt (also printed).
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import fsolve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cc_lib as L          # noqa: E402
import cc_profile as P      # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
HBARC = 197.3269804
MN_MAG = 939.0
T0 = time.time()
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def deltaV(U, b):
    """vector (isospin) variation i[tau_b/2, U]"""
    T = L.TAU[b] / 2
    return 1j * (T[None] @ U - U @ T[None])


def deltaA(U, b):
    """axial variation i{tau_b/2, U}"""
    T = L.TAU[b] / 2
    return 1j * (T[None] @ U + U @ T[None])


def eps3():
    e = np.zeros((3, 3, 3))
    e[0, 1, 2] = e[1, 2, 0] = e[2, 0, 1] = 1
    e[0, 2, 1] = e[2, 1, 0] = e[1, 0, 2] = -1
    return e


EPS3 = eps3()


# --------------------------------------------------------------------------------------------
def check_energy_density(pr):
    """matrix Lagrangian (static) vs the radial density used for the ODE."""
    rng = np.random.default_rng(1)
    xv = rng.normal(size=(50, 3)) * 1.5
    r = np.linalg.norm(xv, axis=1)
    F, Fp = pr(r)
    U, dUs = L.hedgehog(xv, F, Fp)
    dU = np.zeros((50, 4, 2, 2), dtype=complex)
    dU[:, 1:] = dUs
    for b2 in (0.0, 0.07):
        Lm = L.lagrangian(U, dU, b2)
        e = P.EDENS(r, F, Fp, b2) / r ** 2 / (4 * np.pi) * (4 * np.pi)   # e/x^2 per unit volume
        log(f'  energy density check beta2={b2}: max |(-L) - e/x^2| = {np.max(np.abs(-Lm - e)):.2e}')
    return float(np.max(np.abs(-Lm - e)))


def observables(pr, Xbig=400.0, nth=8, nph=10, beta2=0.0, tag=''):
    xr, wr = P.radial_grid(Xbig, 16)
    nS, wS = L.sphere_rule(nth, nph)
    Nr, Na = len(xr), len(wS)
    xv = (xr[:, None, None] * nS[None, :, :]).reshape(-1, 3)
    W = (wr[:, None] * xr[:, None] ** 2 * wS[None, :]).reshape(-1)     # d^3x weights
    F, Fp = pr(np.repeat(xr, Na))
    U, dUs = L.hedgehog(xv, F, Fp)
    N = len(W)
    dU = np.zeros((N, 4, 2, 2), dtype=complex)
    dU[:, 1:] = dUs
    out = {}
    rad = lambda dens: (dens.reshape(Nr, Na) * wS[None, :]).sum(1) * xr ** 2   # per dx

    # ---- static energy, virial, mass
    L2, L4, Lm = L.lagrangian(U, dU, beta2, parts=True)
    E2, E4, Em = -np.sum(W * L2), -np.sum(W * L4), -np.sum(W * Lm)
    # tails beyond Xbig: e ~ k/x^4 for L2 (massless); L4 decays ~x^-8
    eL2 = rad(-L2)
    k2 = eL2[-1] * xr[-1] ** 4
    E2 += k2 / (3 * Xbig ** 3) if beta2 == 0 else 0.0
    out['M'] = E2 + E4 + Em
    out['E2'], out['E4'], out['Em'] = E2, E4, Em
    out['virial_E2_minus_E4_plus_3Em_over_M'] = (E2 - E4 + 3 * Em) / out['M']   # Derrick: E2 - E4 + 3 Em = 0

    # ---- baryon current
    B = L.baryon_current(U, dU)
    sgnB = np.sign(np.sum(W * B[:, 0]))
    B0 = sgnB * B[:, 0]
    out['B_sign_raw'] = float(sgnB)
    out['B'] = np.sum(W * B0)
    rr2 = np.sum(xv ** 2, 1)
    out['R2'] = np.sum(W * B0 * rr2) / out['B']
    r4rad = rad(B0 * rr2 ** 2)
    k4 = r4rad[-1] * xr[-1] ** 3          # x^4 rho_B per dx ~ k4/x^3 (massless) -> tail k4/(2 X^2)
    out['R4'] = (np.sum(W * B0 * rr2 ** 2) + (k4 / (2 * Xbig ** 2) if beta2 == 0 else 0.0)) / out['B']
    out['R4_tail_added'] = k4 / (2 * Xbig ** 2) if beta2 == 0 else 0.0
    s, c = np.sin(F), np.cos(F)
    closed = -s ** 2 * Fp / (2 * np.pi ** 2 * rr2)
    out['B0_vs_-s2Fp/(2pi^2 r^2)_maxrel'] = float(np.max(np.abs(B0 - closed)) / np.max(np.abs(closed)))

    # ---- static isovector currents V^k_b, axial A^k_b
    V = np.zeros((N, 3, 3))   # [:, k, b]
    A = np.zeros((N, 3, 3))
    for b in range(3):
        Xv = deltaV(U, b)
        Xa = deltaA(U, b)
        for k in range(3):
            V[:, k, b] = L.noether(U, dU, k + 1, Xv, beta2)
            A[:, k, b] = L.noether(U, dU, k + 1, Xa, beta2)
    nvec = xv / np.sqrt(rr2)[:, None]
    g = 0.5 * np.einsum('kbl,nl,nkb->n', EPS3, nvec, V)
    Vform = np.einsum('kbl,nl->nkb', EPS3, nvec) * g[:, None, None]
    out['V_static_form_residual'] = float(np.max(np.abs(V - Vform)) / np.max(np.abs(V)))
    Mmat = 0.5 * np.einsum('ijk,nj,nkb,n->ib', EPS3, xv, V, W)
    # tail of M_33: integrand per dx ~ k/x^2
    integrand = 0.5 * (xv[:, 0] * V[:, 1, 2] - xv[:, 1] * V[:, 0, 2])          # (1/2)(x x V_3)_z
    r33 = rad(integrand)
    k33 = r33[-1] * xr[-1] ** 2
    out['M_ib'] = Mmat.tolist()
    out['M33'] = Mmat[2, 2] + (k33 / Xbig if beta2 == 0 else 0.0)
    out['M33_tail_added'] = k33 / Xbig if beta2 == 0 else 0.0
    out['int_r_g_d3x'] = 3 * out['M33']
    # axial
    Tr = np.einsum('nkk->n', A)
    nn = np.einsum('nk,nb,nkb->n', nvec, nvec, A)
    f1, f2 = 0.5 * (Tr - nn), 0.5 * (3 * nn - Tr)
    Aform = f1[:, None, None] * np.eye(3)[None] + f2[:, None, None] * np.einsum('nk,nb->nkb', nvec, nvec)
    out['A_static_form_residual'] = float(np.max(np.abs(A - Aform)) / np.max(np.abs(A)))
    Gmat = np.einsum('nkb,n->kb', A, W)
    out['G_ib'] = Gmat.tolist()
    # convergence of the sphere integral with the cutoff radius
    G33_rad = np.cumsum(wr * rad(A[:, 2, 2]))
    out['G33_cutoff'] = {f'{R:g}': float(np.interp(R, xr, G33_rad)) for R in (5, 10, 20, 50, 100, 200)}
    out['G33'] = Gmat[2, 2]
    # tail coefficients of f1, f2 (x^3 f) at x ~ 60 (inside the shooting-matched region)
    i60 = np.argmin(np.abs(xr - 60.0))
    sl = slice(i60 * Na, (i60 + 1) * Na)
    out['f1_x3_at_60'] = float(np.mean(f1[sl]) * xr[i60] ** 3)
    out['f2_x3_at_60'] = float(np.mean(f2[sl]) * xr[i60] ** 3)

    # ---- rotating hedgehog, Omega' = e3 in d_0 U = Omega'_b i[tau_b/2, U]
    dUr = dU.copy()
    dUr[:, 0] = deltaV(U, 2)
    V0 = np.zeros((N, 3))
    for a in range(3):
        V0[:, a] = L.noether(U, dUr, 0, deltaV(U, a), beta2)
    lam_rad = rad(V0[:, 2])
    klam = lam_rad[-1] * xr[-1] ** 2
    Lam = np.sum(W * V0[:, 2]) + (klam / Xbig if beta2 == 0 else 0.0)
    out['Lambda_tilde'] = Lam                       # = int V^0_3 d^3x for unit Omega'
    out['Lambda_tail_added'] = klam / Xbig if beta2 == 0 else 0.0
    out['V0_12_charges'] = [float(np.sum(W * V0[:, 0])), float(np.sum(W * V0[:, 1]))]
    out['lambda_density_x2_coeff_at_Xbig'] = klam
    # physical angular momentum J_z: Noether charge of the active rotation dU = -(e3 x x).grad U
    Xrot = -(xv[:, 0, None, None] * dU[:, 2] - xv[:, 1, None, None] * dU[:, 1])
    Jd = L.noether(U, dUr, 0, Xrot, beta2)
    J_rad = rad(Jd)
    kJ = J_rad[-1] * xr[-1] ** 2
    out['J_z'] = np.sum(W * Jd) + (kJ / Xbig if beta2 == 0 else 0.0)
    out['J_density_x2_coeff_at_Xbig'] = kJ
    # baryon current of the rotating hedgehog -> isoscalar magnetic moment (EM current B/2)
    Br = L.baryon_current(U, dUr) * sgnB
    out['Br0_minus_B0_max'] = float(np.max(np.abs(Br[:, 0] - B0)))
    muB = 0.5 * np.sum(W * 0.5 * (xv[:, 0] * Br[:, 2] - xv[:, 1] * Br[:, 1]))
    out['mu_isoscalar_tilde'] = muB
    # angular velocity of the baryon density: B^k = B0 (w x x)_k -> w_z = <(x B^y - y B^x)>/<(x^2+y^2)B0>
    out['omega_s_from_Bcurrent'] = float(np.sum(W * (xv[:, 0] * Br[:, 2] - xv[:, 1] * Br[:, 1])) /
                                         np.sum(W * (xv[:, 0] ** 2 + xv[:, 1] ** 2) * B0))
    # radial densities for charge distributions
    out['_xr'] = xr; out['_wr'] = wr
    out['_rhoB'] = rad(B0); out['_rholam'] = lam_rad
    out['_klam'] = klam
    return out


def radial_dens(pr, xs, beta2=0.0):
    """angle-integrated (per dx) baryon density and isospin (moment-of-inertia) density at radii xs,
    from the matrix baryon current and the matrix Noether charge (6x8 rule is exact for the angular part)."""
    nS, wS = L.sphere_rule(6, 8)
    Na = len(wS)
    xv = (xs[:, None, None] * nS[None]).reshape(-1, 3)
    U, dUs = L.hedgehog(xv, *pr(np.repeat(xs, Na)))
    dU = np.zeros((len(xv), 4, 2, 2), dtype=complex)
    dU[:, 1:] = dUs
    B0 = np.abs(L.baryon_current(U, dU)[:, 0])
    dU[:, 0] = deltaV(U, 2)
    V03 = L.noether(U, dU, 0, deltaV(U, 2), beta2)
    red = lambda d: (d.reshape(len(xs), Na) * wS[None]).sum(1) * xs ** 2
    return red(B0), red(V03)


def cut_integrals(pr, R, beta2=0.0):
    """int_0^R of rho_B, rho_lam, x^2 rho_lam (per dx) with R a panel edge (no interpolation)."""
    edges = np.concatenate([[0.0], np.geomspace(min(0.01, R / 2), R, 40)])
    xs, ws = P.gl_panels(edges, 16)
    rb, rl = radial_dens(pr, xs, beta2)
    return np.sum(ws * rb), np.sum(ws * rl), np.sum(ws * rl * xs ** 2)


def quantum_R33():
    """explicit nucleon wavefunctions psi = c.a on S^3."""
    QL = [L.generator_matrix('L', a) for a in range(3)]     # Noether isospin charges (delta U = i[tau/2,U])
    JR = [L.generator_matrix('R', a) for a in range(3)]     # angular momentum (active rotations)
    res = {}
    comm = lambda X, Y: X @ Y - Y @ X
    res['[J1,J2]-iJ3'] = float(np.max(np.abs(comm(JR[0], JR[1]) - 1j * JR[2])))
    res['[Q1,Q2]+iQ3'] = float(np.max(np.abs(comm(QL[0], QL[1]) + 1j * QL[2])))   # left action: opposite handedness
    res['J^2'] = np.real_if_close(np.linalg.eigvals(sum(j @ j for j in JR))).tolist()
    res['Q^2'] = np.real_if_close(np.linalg.eigvals(sum(q @ q for q in QL))).tolist()
    # joint eigenvectors of Q3, J3
    states = {}
    w, v = np.linalg.eig(QL[2])
    for q3 in (0.5, -0.5):
        sub = v[:, np.isclose(w, q3)]
        # restrict J3 to the subspace
        Jsub = np.linalg.lstsq(sub, JR[2] @ sub, rcond=None)[0]
        wj, vj = np.linalg.eig(Jsub)
        for k in range(len(wj)):
            states[(q3, round(float(np.real(wj[k])), 6))] = sub @ vj[:, k]
    K33 = L.quadform_of(lambda a: L.R_adj(L.su2_from_a(a))[2, 2])
    for key, cvec in states.items():
        res[f'<R33> Q3={key[0]:+} J3={key[1]:+}'] = L.s3_expect(cvec, K33)
    # classical-vs-quantum sign: operator identity Q_a = s * R_ab(A) J_b on linear functions?
    # compare (Q3 psi) with sum_b R_3b(A) (J_b psi) evaluated pointwise at random A (both linear in a after
    # applying J_b, R is quadratic, so compare as functions on random points)
    rng = np.random.default_rng(2)
    pts = rng.normal(size=(20, 4)); pts /= np.linalg.norm(pts, axis=1)[:, None]
    cvec = rng.normal(size=4) + 1j * rng.normal(size=4)
    lhs = np.array([(QL[2] @ cvec) @ p for p in pts])
    Rs = L.R_adj(L.su2_from_a(pts))
    rhs = np.array([sum(Rs[i, 2, b] * ((JR[b] @ cvec) @ pts[i]) for b in range(3)) for i in range(len(pts))])
    res['quantum Q3 = +R3b J_b residual'] = float(np.max(np.abs(lhs - rhs)))
    res['quantum Q3 = -R3b J_b residual'] = float(np.max(np.abs(lhs + rhs)))
    rhsT = np.array([sum(Rs[i, b, 2] * ((JR[b] @ cvec) @ pts[i]) for b in range(3)) for i in range(len(pts))])
    res['quantum Q3 = +R_b3 J_b residual'] = float(np.max(np.abs(lhs - rhsT)))
    res['quantum Q3 = -R_b3 J_b residual'] = float(np.max(np.abs(lhs + rhsT)))
    return res, states, K33


def classical_sign_check(pr):
    """classical Noether charges at a generic A: is Q_a = +R_ab(A) J_b or -R_ab J_b?"""
    xr, wr = P.radial_grid(60.0, 12)
    nS, wS = L.sphere_rule(8, 10)
    Na = len(wS)
    xv = (xr[:, None, None] * nS[None, :, :]).reshape(-1, 3)
    W = (wr[:, None] * xr[:, None] ** 2 * wS[None, :]).reshape(-1)
    F, Fp = pr(np.repeat(xr, Na))
    U0, dU0 = L.hedgehog(xv, F, Fp)
    rng = np.random.default_rng(5)
    a = rng.normal(size=4); a /= np.linalg.norm(a)
    A = L.su2_from_a(a)
    Om = np.array([0.3, -0.5, 0.8])
    Ad = L.dag(A)
    U = A[None] @ U0 @ Ad[None]
    N = len(W)
    dU = np.zeros((N, 4, 2, 2), dtype=complex)
    for i in range(3):
        dU[:, i + 1] = A[None] @ dU0[:, i] @ Ad[None]
    G = 1j * np.einsum('b,bij->ij', Om, L.TAU) / 2      # A-dot = G A
    dU[:, 0] = G[None] @ U - U @ G[None]
    Q = np.array([np.sum(W * L.noether(U, dU, 0, deltaV(U, k))) for k in range(3)])
    J = []
    for k in range(3):
        e = np.zeros(3); e[k] = 1
        ex = np.cross(e[None], xv)            # (e_k x x)
        Xrot = -np.einsum('ni,nijk->njk', ex, dU[:, 1:])
        J.append(np.sum(W * L.noether(U, dU, 0, Xrot)))
    J = np.array(J)
    R = L.R_adj(A)
    # also: V_a(A U0 A^+) = R_ab V_b(U0) pointwise for a static spatial current component
    dUs = dU.copy(); dUs[:, 0] = 0
    dU0s = np.zeros_like(dUs); dU0s[:, 1:] = dU0
    Vt = np.array([L.noether(U, dUs, 1, deltaV(U, b))[:50] for b in range(3)])
    V0t = np.array([L.noether(U0, dU0s, 1, deltaV(U0, b))[:50] for b in range(3)])
    # spatial-rotation equivalence: exp(i e tau3/2) U0(x) exp(-i e tau3/2) = U0(R_z(e)^{-1} x)
    ee = 0.37
    g = np.cos(ee / 2) * L.I2 + 1j * np.sin(ee / 2) * L.TAU[2]
    Rz = np.array([[np.cos(ee), -np.sin(ee), 0], [np.sin(ee), np.cos(ee), 0], [0, 0, 1]])
    xs = xv[:40]
    Fs, Fps = pr(np.linalg.norm(xs, axis=1))
    lhs = g[None] @ L.hedgehog(xs, Fs, Fps)[0] @ L.dag(g)[None]
    xr_ = xs @ Rz          # rows: (R^T x) = R^{-1} x
    Fr, Fpr = pr(np.linalg.norm(xr_, axis=1))
    rhs = L.hedgehog(xr_, Fr, Fpr)[0]
    return {'Q': Q.tolist(), 'J': J.tolist(), 'Q - R J': (Q - R @ J).tolist(), 'Q + R J': (Q + R @ J).tolist(),
            'Q - R^T J': (Q - R.T @ J).tolist(), 'Q + R^T J': (Q + R.T @ J).tolist(),
            'V(AU0A+) - R V(U0) max': float(np.max(np.abs(Vt - R @ V0t))),
            'isorotation_equals_active_spatial_rotation_residual': float(np.max(np.abs(lhs - rhs)))}


def su3_inertia(pr, Xbig=400.0):
    xr, wr = P.radial_grid(Xbig, 16)
    nS, wS = L.sphere_rule(6, 8)
    Na = len(wS)
    xv = (xr[:, None, None] * nS[None, :, :]).reshape(-1, 3)
    W = (wr[:, None] * xr[:, None] ** 2 * wS[None, :]).reshape(-1)
    F, Fp = pr(np.repeat(xr, Na))
    U2, dU2 = L.hedgehog(xv, F, Fp)
    U = L.embed3(U2)
    N = len(W)
    dU = np.zeros((N, 4, 3, 3), dtype=complex)
    for i in range(3):
        dU[:, i + 1] = L.embed3d(dU2[:, i])
    res = {}
    for k, name in ((0, 'I_11'), (3, 'I_44'), (7, 'I_88')):
        T = L.GELL[k] / 2
        X = 1j * (T[None] @ U - U @ T[None])
        d2 = dU.copy(); d2[:, 0] = X
        dens = L.noether(U, d2, 0, X)
        radd = (dens.reshape(len(xr), Na) * wS[None, :]).sum(1) * xr ** 2
        kk = radd[-1] * xr[-1] ** 2
        # I_44 density decays as (1-cos F) ~ F^2/2 ~ x^-4 times x^2 -> x^-2 per dx: tail k/X
        res[name] = float(np.sum(W * dens) + kk / Xbig)
    return res


def phys(o, Fpi, e, Mn=MN_MAG):
    eF = e * Fpi
    lam = o['Lambda_tilde'] / (e ** 3 * Fpi)        # MeV^-1
    M = Fpi / e * o['M']
    d = {'F_pi': Fpi, 'e': e, 'M_cl': M, 'M_N': M + 3 / (8 * lam), 'M_Delta': M + 15 / (8 * lam),
         'fm_per_x': HBARC / eF}
    d['r_I0_fm'] = np.sqrt(o['R2']) * HBARC / eF
    d['rM_I0_ANWdef_fm'] = np.sqrt(o['R4'] / o['R2']) * HBARC / eF
    d['rM_I0_Sachs_fm'] = np.sqrt(0.6 * o['R4'] / o['R2']) * HBARC / eF
    # isoscalar moment: mu/J from the classical rotation; J = 1/2.  mu_B = muB_tilde/(eF), J = J_tilde/e^2
    d['mu_I0'] = Mn * e * o['mu_isoscalar_tilde'] / (Fpi * o['J_z'])     # = 2 M_N * (mu/J) * 1/2
    d['mu_I1'] = 2 * Mn * o['R33_p'] * o['M33'] / (e ** 3 * Fpi)
    d['mu_p'] = d['mu_I0'] + d['mu_I1']
    d['mu_n'] = d['mu_I0'] - d['mu_I1']
    d['mu_p_over_mu_n'] = d['mu_p'] / d['mu_n']
    G = o['G33']
    d['gA_sphere'] = abs(2 * o['R33_p'] * G) / e ** 2          # g_A/2 = <R33> G / e^2
    d['gA_ANW_pole_removed'] = 1.5 * d['gA_sphere']
    d['gA_surface_2piC_over_3e2'] = 2 * np.pi * o['C'] / (3 * e ** 2) if o.get('C') else None
    d['g_piNN_GT'] = 2 * Mn * d['gA_ANW_pole_removed'] / Fpi
    return d


def fit_su2(o, MN=939.0, MD=1232.0):
    lam = 3 / (2 * (MD - MN))
    M = MN - 3 / (8 * lam)
    F_over_e = M / o['M']
    e3F = o['Lambda_tilde'] / lam
    e = (e3F / F_over_e) ** 0.25
    return F_over_e * e, e


def main():
    log('== E5 cross-check: hedgehog and EM static properties (independent code) ==')
    # ---------------------------------------------------------------- massless profile + convergence
    variants = [dict(X=40.0, xm=1.5), dict(X=80.0, xm=1.0), dict(X=25.0, xm=2.5),
                dict(X=40.0, xm=1.5, x0=3e-3), dict(X=40.0, xm=1.5, rtol=1e-11)]
    profs = []
    for v in variants:
        pr = P.solve_profile(**v)
        profs.append(pr)
        log(f"  shooting {v}: F'(0)={pr.a:.10f}  C={pr.C:.9f}  match residual={max(abs(np.array(pr.res))):.1e}")
    pr = profs[1]
    log(f'  inner series b(a) = {P.B_EXPR};  outer tail d = {P.D_EXPR}')
    err_e = check_energy_density(pr)

    t = time.time()
    o = observables(pr, Xbig=400.0)
    o['C'] = pr.C; o['Fprime0'] = pr.a
    log(f'  observables (X=400, 8x10 angular) in {time.time() - t:.1f}s')
    o2 = observables(profs[0], Xbig=200.0, nth=6, nph=8)
    o2['C'] = profs[0].C
    keys = ['M', 'B', 'R2', 'R4', 'Lambda_tilde', 'J_z', 'mu_isoscalar_tilde', 'M33', 'G33']
    conv = {k: abs(o[k] - o2[k]) / abs(o[k]) for k in keys}
    log('  grid/profile convergence (X=400 8x10 vs X=200 6x8 & other profile), rel. diff:',
        {k: f'{v:.1e}' for k, v in conv.items()})

    qres, states, K33 = quantum_R33()
    for k, v in qres.items():
        log(f'  quantum: {k}: {v}')
    csc = classical_sign_check(pr)
    log('  classical charges at generic A:', {k: (np.round(v, 6).tolist() if isinstance(v, list) else v) for k, v in csc.items()})
    # proton (s=+1 convention: J_em = B/2 + V_3, V the Noether current of i[tau/2,U]): Q3 = +1/2, J3 = +1/2
    o['R33_p'] = qres['<R33> Q3=+0.5 J3=+0.5']
    R33_alt = qres['<R33> Q3=-0.5 J3=+0.5']

    log('== massless hedgehog numbers (dimensionless) ==')
    for k in ['M', 'E2', 'E4', 'virial_E2_minus_E4_plus_3Em_over_M', 'B', 'B_sign_raw', 'R2', 'R4',
              'B0_vs_-s2Fp/(2pi^2 r^2)_maxrel', 'Lambda_tilde', 'Lambda_tail_added', 'J_z', 'V0_12_charges',
              'omega_s_from_Bcurrent', 'Br0_minus_B0_max', 'mu_isoscalar_tilde', 'V_static_form_residual',
              'M33', 'M33_tail_added', 'int_r_g_d3x', 'A_static_form_residual', 'G33', 'G33_cutoff',
              'f1_x3_at_60', 'f2_x3_at_60', 'C', 'Fprime0']:
        log(f'  {k:40s} {o[k]}')
    log(f"  M/(3pi^2) = {o['M'] / (3 * np.pi ** 2):.8f};  Lambda = Lambda_tilde/(2pi/3) = {o['Lambda_tilde'] / (2 * np.pi / 3):.6f}")
    log(f"  int r g d^3x / Lambda_tilde = {o['int_r_g_d3x'] / o['Lambda_tilde']:.9f}  (closed-form claim: 3/2)")
    log(f"  mu_isoscalar_tilde/J_z = {o['mu_isoscalar_tilde'] / o['J_z']:.9f}  vs <x^2>/(6 Lambda_tilde) = {o['R2'] / (6 * o['Lambda_tilde']):.9f}")
    log(f"  G33 = {o['G33']:.8f};  2 pi C/3 = {2 * np.pi * o['C'] / 3:.8f};  f1 x^3 -> -C/4 = {-o['C'] / 4:.5f}, f2 x^3 -> 3C/4 = {3 * o['C'] / 4:.5f}")

    res = {'conventions': 'L = (F^2/16)Tr dU dU+ + (1/32e^2)Tr[L,L]^2 (+(F^2 m^2/16)Tr(U+U+-2)); x = eF r; F_pi 186-MeV convention',
           'profile_variants': [{**{k: float(v) for k, v in var.items()}, 'Fprime0': p.a, 'C': p.C} for var, p in zip(variants, profs)],
           'energy_density_check_maxabs': err_e,
           'grid_convergence_reldiff': conv,
           'quantum': {k: (v if not isinstance(v, (np.floating, float)) else float(v)) for k, v in qres.items()},
           'classical_sign_check': csc}
    res['massless'] = {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in o.items() if not k.startswith('_')}

    # ---------------------------------------------------------------- physical numbers
    anw = phys(o, 129.0, 5.45)
    Ffit, efit = fit_su2(o)
    fit = phys(o, Ffit, efit)
    alt = phys({**o, 'R33_p': -R33_alt}, 129.0, 5.45)   # opposite convention: J_em = B/2 - V_3, proton Q3=-1/2
    log('== ANW parameters (F=129, e=5.45) ==')
    for k, v in anw.items():
        log(f'  {k:28s} {v}')
    log(f"  sign-convention independence: mu_I1 (s=+1) = {anw['mu_I1']:.10f}, (s=-1) = {alt['mu_I1']:.10f}")
    log(f'== own SU(2) refit: F={Ffit:.4f} e={efit:.5f} ==')
    for k in ['M_N', 'M_Delta', 'r_I0_fm', 'rM_I0_ANWdef_fm', 'mu_p', 'mu_n', 'mu_p_over_mu_n', 'gA_ANW_pole_removed', 'g_piNN_GT']:
        log(f'  {k:28s} {fit[k]}')
    res['ANW'] = anw; res['SU2_refit'] = fit

    # isovector radius with cutoff, enclosed charges
    xr, wr = o['_xr'], o['_wr']
    lam_cum = np.cumsum(wr * o['_rholam'])
    r2_cum = np.cumsum(wr * o['_rholam'] * xr ** 2)
    B_cum = np.cumsum(wr * o['_rhoB'])
    Lam = o['Lambda_tilde']
    cut = {}
    for R in (2, 5, 10, 20, 50, 100, 200):
        cut[str(R)] = float(cut_integrals(pr, float(R))[2] / Lam)
    slope = (cut['200'] - cut['100']) / 100.0
    log('  isovector <r^2>_{I=1}(R) [x^2], normalised to the full isovector charge:', {k: round(v, 3) for k, v in cut.items()},
        f' slope(100-200) = {slope:.5f};  C^2/Lambda = {o["C"] ** 2 / (Lam / (2 * np.pi / 3)):.5f}; '
        f'numerical density coefficient k/Lambda_tilde = {o["_klam"] / Lam:.5f}')
    fmx = anw['fm_per_x']
    enc = []
    for Rfm in (0.25, 0.5, 1.0, 2.0, 5.0, 10.0):
        Rx = Rfm / fmx
        cb, cl, _ = cut_integrals(pr, Rx)
        iso = 0.5 * cb
        ivec = 0.5 * cl / Lam
        enc.append({'R_fm': Rfm, 'Q_p': iso + ivec, 'Q_n': iso - ivec, 'iso': iso, 'ivec': ivec,
                    'ivec_outside': 0.5 - ivec, 'asym_C2_over_2Lambda_x': o['_klam'] / (2 * Lam * Rx)})
        log(f"  R={Rfm:5.2f} fm  Q_p(<R)={iso + ivec:.4f}  Q_n(<R)={iso - ivec:+.4f}   isovector outside {0.5 - ivec:.5f} (asymptotic {o['_klam'] / (2 * Lam * Rx):.5f})")
    res['isovector_r2_cutoff_x2'] = cut
    res['isovector_slope'] = slope
    res['isovector_r2_slope_fm_per_fm_ANW'] = slope * fmx
    res['enclosed_massless_ANW'] = enc

    # ---------------------------------------------------------------- SU(3): I2 and refit, pi0 at the fold's f
    s3 = su3_inertia(pr)
    log('  SU(3) embedded inertia (dimensionless, x 1/(e^3 F)):', s3, f" ; Lambda_tilde = {Lam:.5f}")
    I1t, I2t = Lam, s3['I_44']

    def su3_eqs(p):
        Fp_, e_ = p
        I1 = I1t / (e_ ** 3 * Fp_); I2 = I2t / (e_ ** 3 * Fp_); M = Fp_ / e_ * o['M']
        E8 = M + 3 / (8 * I1) + 3 / (4 * I2)
        E10 = M + 15 / (8 * I1) + 3 / (4 * I2)
        return [E8 - 1151.19, E10 - 1382.11]
    F3, e3 = fsolve(su3_eqs, [114.0, 5.25], xtol=1e-13)
    E10bar = F3 / e3 * o['M'] + 3 / (8 * I1t / (e3 ** 3 * F3)) + 3 / (4 * I2t / (e3 ** 3 * F3)) + 3 / (2 * I2t / (e3 ** 3 * F3))
    log(f'  SU(3) refit to 1151.19/1382.11: F={F3:.4f} MeV e={e3:.5f} f=F/2={F3 / 2:.4f} MeV; 10bar at {E10bar:.1f} MeV')
    res['SU3'] = {'I_tilde': s3, 'F': F3, 'e': e3, 'f': F3 / 2, 'E10bar': E10bar}
    res['f_values'] = {'ANW': 64.5, 'SU2_refit': Ffit / 2, 'SU3_refit': F3 / 2}

    # ---------------------------------------------------------------- massive pions (AN84)
    mpi = 138.0

    # quick mass/inertia for the fit (radial integrals of the matrix-validated density)
    def mass_inertia(beta):
        prm = P.solve_profile(beta=beta, X=50.0, xm=1.5)
        xr_, wr_ = P.radial_grid(60.0, 16)
        Fv, Fpv = prm(xr_)
        M = 4 * np.pi * np.sum(wr_ * P.EDENS(xr_, Fv, Fpv, beta ** 2))
        # inertia from the matrix Noether density on a small angular grid
        nS, wS = L.sphere_rule(4, 6)
        Na = len(wS)
        xv = (xr_[:, None, None] * nS[None]).reshape(-1, 3)
        Wt = (wr_[:, None] * xr_[:, None] ** 2 * wS[None]).reshape(-1)
        U, dUs = L.hedgehog(xv, *prm(np.repeat(xr_, Na)))
        dU = np.zeros((len(Wt), 4, 2, 2), dtype=complex); dU[:, 1:] = dUs; dU[:, 0] = deltaV(U, 2)
        lamt = np.sum(Wt * L.noether(U, dU, 0, deltaV(U, 2), beta ** 2))
        return M, lamt

    cache = {}

    def eqs(p):
        Fp_, e_ = p
        beta = mpi / (e_ * Fp_)
        key = round(beta, 12)
        if key not in cache:
            cache[key] = mass_inertia(beta)
        M, lamt = cache[key]
        lam = lamt / (e_ ** 3 * Fp_)
        return [Fp_ / e_ * M + 3 / (8 * lam) - 939.0, 3 / (2 * lam) - 293.0]
    Fm, em = fsolve(eqs, [108.0, 4.84], xtol=1e-10)
    log(f'  massive refit (m_pi=138, M_N=939, M_Delta=1232): F={Fm:.4f} MeV e={em:.5f} (AN84 quoted 108, 4.84)')
    beta = mpi / (4.84 * 108.0)
    prm = P.solve_profile(beta=beta, X=50.0, xm=1.5)
    om = observables(prm, Xbig=60.0, nth=8, nph=10, beta2=beta ** 2)
    om['R33_p'] = o['R33_p']; om['C'] = None
    am = phys(om, 108.0, 4.84)
    # isovector radius (finite)
    xr2, wr2 = om['_xr'], om['_wr']
    r2_I1 = np.sum(wr2 * om['_rholam'] * xr2 ** 2) / np.sum(wr2 * om['_rholam'])
    am['r_I1_fm'] = np.sqrt(r2_I1) * am['fm_per_x']
    am['r_p_fm'] = np.sqrt(0.5 * (am['r_I0_fm'] ** 2 + am['r_I1_fm'] ** 2))
    am['r2_n_fm2'] = 0.5 * (am['r_I0_fm'] ** 2 - am['r_I1_fm'] ** 2)
    am['beta'] = beta
    am['virial'] = om['virial_E2_minus_E4_plus_3Em_over_M']
    am['Lambda_tilde_matrix'] = om['Lambda_tilde']
    log('== massive pions, F=108, e=4.84, m=138 (no target) ==')
    for k in ['beta', 'M_N', 'M_Delta', 'r_I0_fm', 'r_I1_fm', 'r_p_fm', 'r2_n_fm2', 'mu_p', 'mu_n', 'gA_sphere',
              'gA_ANW_pole_removed', 'virial']:
        log(f'  {k:28s} {am[k]}')
    lam_cum2 = np.cumsum(wr2 * om['_rholam']); Lam2 = np.sum(wr2 * om['_rholam'])
    B_cum2 = np.cumsum(wr2 * om['_rhoB'])
    encm = []
    for Rfm in (0.25, 0.5, 1.0, 2.0, 5.0, 10.0):
        Rx = Rfm / am['fm_per_x']
        cb, cl, _ = cut_integrals(prm, Rx, beta ** 2)
        iso = 0.5 * cb; ivec = 0.5 * cl / Lam2
        encm.append({'R_fm': Rfm, 'Q_p': iso + ivec, 'Q_n': iso - ivec})
        log(f'  massive R={Rfm:4.2f} fm Q_p={iso + ivec:.4f} Q_n={iso - ivec:+.4f}')
    res['massive_refit'] = {'F': Fm, 'e': em}
    res['massive_AN84'] = am
    res['enclosed_massive_AN84'] = encm
    res['runtime_s'] = time.time() - T0
    log(f'done in {time.time() - T0:.1f} s')

    def clean(v):
        if isinstance(v, dict):
            return {str(k): clean(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [clean(x) for x in v]
        if isinstance(v, (np.floating,)):
            return float(v)
        if isinstance(v, np.ndarray):
            return clean(v.tolist())
        if isinstance(v, complex):
            return [v.real, v.imag]
        return v
    with open(os.path.join(HERE, 'cc_hedgehog.json'), 'w') as f:
        json.dump(clean(res), f, indent=1)
    with open(os.path.join(HERE, 'cc_hedgehog_log.txt'), 'w') as f:
        f.write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
