#!/usr/bin/env python3
"""E2 -- derive/verify the radial formulas from the Skyrme Lagrangian with explicit SU(3) matrices.

Units F_pi = e = 1 (so x = r; masses in F_pi/e, inertia in 1/(e^3 F_pi), currents per 1/e^2).
Hedgehog embedded in the upper-left 2x2 block, U0 = diag(exp(i tau.n F), 1); rotated field
U = A(t) U0 A(t)^dag with A in SU(3), A^dag dA/dt = (i/2) lambda_a Omega_a. Then, exactly,
   L_0 = A (U0^dag w U0 - w) A^dag,  w = (i/2) lambda_a Omega_a,   L_i = A U0^dag d_i U0 A^dag,
and traces do not depend on A. From L = (1/16) Tr dU dU^dag + (1/32) Tr[L_mu,L_nu]^2:
   static energy density   e   = -(1/16) Tr L_i L_i - (1/32) Tr [L_i,L_j]^2
   rotational Lagrangian   l   = -(1/16) Tr L_0^2  - (1/16) sum_i Tr [L_0,L_i]^2 = (1/2) i_ab Omega_a Omega_b
   axial Noether current   A^a_j = dL/d(d_j eps^a) for dU = (i/2) eps^a (tau_a U + U tau_a)
                                   (normalised so that <0|A^a_mu|pi^b> = i f_pi p_mu, f_pi = F_pi/2)
   stress tensor           T_ij  = (d e/d(d_i U)) . d_j U - delta_ij e
The script checks, at random (x, F, F') and after exact angular quadrature, that these reproduce
   e                      = (1/8)(F'^2 + 2s^2/x^2) + (1/2)(s^2/x^2)(s^2/x^2 + 2F'^2)
   <i_aa>, a = 1,2,3      = (1/6) s^2 [1 + 4(F'^2 + s^2/x^2)]          -> I1 = (2pi/3) Lambda
   <i_aa>, a = 4..7       = (1/8) (1 - cos F)[1 + F'^2 + 2 s^2/x^2]      -> I2 = (pi/2) J2  (Kopeliovich 22c)
   <i_88> = 0, <i_ab> = 0 (a != b)
   <A^a_j>                = kappa delta_aj [F' + sin2F/x + 4(sin2F F'^2/x + 2 s^2 F'/x^2 + s^2 sin2F/x^3)]
                            FOUND: kappa = -1/12, so the volume integral of the current over a ball is
                            c_ball = -(pi/3) D (= -(2pi/3) C, a surface term, since d_i A_i = 0), and with
                            <p up|D_33|p up> = -1/3 the ball integral gives |g_A| = (2/3)(pi/3)|D|/e^2,
                            i.e. 2/3 of ANW's -(pi/(3e^2)) D.  The missing 3/2 is the massless-pion pole:
                            the q -> 0 limit of the transverse form factor (what g_A means) is 3/2 of the
                            ball average. Part (iii) shows this numerically with the Fourier transform.
   T_rr = (1/8)(F'^2 - 2s^2/x^2) + (s^2/(2x^2))(2F'^2 - s^2/x^2),   T_thth = -(1/8)F'^2 + s^4/(2x^4)
Then integrates the full 8x8 inertia tensor over the solved profile.
Writes out/verify.json. Deterministic (seed 20261018). Runtime ~20 s.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import skyrme_hedgehog as sh  # noqa: E402

OUT = os.path.join(HERE, "out")

# Gell-Mann matrices
lam = np.zeros((8, 3, 3), complex)
lam[0][0, 1] = lam[0][1, 0] = 1
lam[1][0, 1] = -1j; lam[1][1, 0] = 1j
lam[2][0, 0] = 1; lam[2][1, 1] = -1
lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2] = -1j; lam[4][2, 0] = 1j
lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2] = -1j; lam[6][2, 1] = 1j
lam[7] = np.diag([1, 1, -2]) / np.sqrt(3)
tau = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], complex)


def angular_grid(nmu=12, nphi=16):
    mu, wmu = np.polynomial.legendre.leggauss(nmu)
    phi = 2 * np.pi * np.arange(nphi) / nphi
    M, P = np.meshgrid(mu, phi, indexing="ij")
    W = np.outer(wmu, np.full(nphi, 2 * np.pi / nphi)) / (4 * np.pi)     # sums to 1
    st = np.sqrt(1 - M ** 2)
    n = np.stack([st * np.cos(P), st * np.sin(P), M], axis=-1).reshape(-1, 3)
    eth = np.stack([M * np.cos(P), M * np.sin(P), -st], axis=-1).reshape(-1, 3)
    return n, eth, W.ravel()


def comm(A, B):
    return A @ B - B @ A


def tr(A):
    return np.einsum("...ii->...", A)


def fields(x, F, Fp, n):
    """U (P,3,3) and L_i (3,P,3,3) at points x*n (n: (P,3))."""
    P = n.shape[0]
    ntau = np.einsum("pi,iab->pab", n, tau)
    s, c = np.sin(F), np.cos(F)
    u = c * np.eye(2)[None] + 1j * s * ntau
    U = np.zeros((P, 3, 3), complex)
    U[:, :2, :2] = u
    U[:, 2, 2] = 1.0
    dU = np.zeros((3, P, 3, 3), complex)
    for i in range(3):
        du = (-s * Fp * n[:, i])[:, None, None] * np.eye(2)[None] + 1j * (
            (c * Fp * n[:, i])[:, None, None] * ntau
            + (s / x) * (tau[i][None] - n[:, i][:, None, None] * ntau))
        dU[i, :, :2, :2] = du
    Ud = np.conj(np.transpose(U, (0, 2, 1)))
    L = np.einsum("pab,ipbc->ipac", Ud, dU)
    return U, Ud, L


def energy_density(L):
    e = -(1.0 / 16) * sum(tr(L[i] @ L[i]) for i in range(3))
    for i in range(3):
        for j in range(3):
            K = comm(L[i], L[j])
            e = e - (1.0 / 32) * tr(K @ K)
    return e.real


def inertia_density(U, Ud, L):
    """i_ab density (P,8,8)."""
    P = U.shape[0]
    L0 = np.empty((8, P, 3, 3), complex)
    for a in range(8):
        w = 0.5j * lam[a]
        L0[a] = Ud @ w[None] @ U - w[None]
    out = np.zeros((P, 8, 8))
    C = np.empty((8, 3, P, 3, 3), complex)
    for a in range(8):
        for i in range(3):
            C[a, i] = comm(L0[a], L[i])
    for a in range(8):
        for b in range(a, 8):
            v = -(1.0 / 8) * tr(L0[a] @ L0[b])
            for i in range(3):
                v = v - (1.0 / 8) * tr(C[a, i] @ C[b, i])
            out[:, a, b] = out[:, b, a] = v.real
    return out


def axial_current(U, Ud, L, h=1e-3):
    """A^a_j (P,3,3): a = isospin 1..3 (lambda_1..3), j = space. A = dL/d(d_j eps) = -d e/dh."""
    P = U.shape[0]
    A = np.zeros((P, 3, 3))
    for a in range(3):
        dL = 0.5j * (Ud @ lam[a][None] @ U + lam[a][None])       # U^dag dM, dM = (i/2)(lam U + U lam)
        for j in range(3):
            vals = []
            for k in (-2, -1, 1, 2):
                Lh = L.copy()
                Lh[j] = L[j] + k * h * dL
                vals.append(energy_density(Lh))
            de = (vals[0] - 8 * vals[1] + 8 * vals[2] - vals[3]) / (12 * h)
            A[:, a, j] = -de
    return A


def stress(L, h=1e-3):
    e0 = energy_density(L)
    P = L.shape[1]
    T = np.zeros((P, 3, 3))
    for i in range(3):
        for j in range(3):
            vals = []
            for k in (-2, -1, 1, 2):
                Lh = L.copy()
                Lh[i] = L[i] + k * h * L[j]
                vals.append(energy_density(Lh))
            T[:, i, j] = (vals[0] - 8 * vals[1] + 8 * vals[2] - vals[3]) / (12 * h) - (e0 if i == j else 0.0)
    return T


def formulas(x, F, Fp):
    s = np.sin(F); s2 = s * s; c = np.cos(F); s2F = np.sin(2 * F); q = s2 / x ** 2
    return {
        "e": 0.125 * (Fp ** 2 + 2 * q) + 0.5 * q * (q + 2 * Fp ** 2),
        "i1": (1.0 / 6) * s2 * (1 + 4 * (Fp ** 2 + q)),
        "i2": (1.0 / 8) * (1 - c) * (1 + Fp ** 2 + 2 * q),
        "gA": Fp + s2F / x + 4 * (s2F * Fp ** 2 / x + 2 * s2 * Fp / x ** 2 + s2 * s2F / x ** 3),
        "Trr": 0.125 * (Fp ** 2 - 2 * q) + 0.5 * q * (2 * Fp ** 2 - q),
        "Ttt": -0.125 * Fp ** 2 + 0.5 * q * q,
    }


def main():
    t0 = time.time()
    rng = np.random.default_rng(20261018)
    n, eth, W = angular_grid()
    print("E2 verification from explicit SU(3) matrices (units F_pi = e = 1)\n")
    print("pointwise identities at 12 random (x, F, F'), exact angular quadrature (12 x 16 points)")
    maxdev = {k: 0.0 for k in ["e", "i1", "i2", "i8", "offdiag", "gA_ratio", "A_offdiag", "Trr", "Ttt", "Trt", "Tsym"]}
    kappas = []
    for trial in range(12):
        x = rng.uniform(0.1, 5.0)
        F = rng.uniform(0.05, np.pi - 0.05)
        Fp = rng.uniform(-3.0, -0.01)
        U, Ud, L = fields(x, F, Fp, n)
        fo = formulas(x, F, Fp)
        e = energy_density(L)
        maxdev["e"] = max(maxdev["e"], np.max(np.abs(e - fo["e"])) / fo["e"])
        I = np.einsum("p,pab->ab", W, inertia_density(U, Ud, L))
        for a in range(3):
            maxdev["i1"] = max(maxdev["i1"], abs(I[a, a] / fo["i1"] - 1))
        for a in range(3, 7):
            maxdev["i2"] = max(maxdev["i2"], abs(I[a, a] / fo["i2"] - 1))
        maxdev["i8"] = max(maxdev["i8"], abs(I[7, 7]) / fo["i1"])
        off = I - np.diag(np.diag(I))
        maxdev["offdiag"] = max(maxdev["offdiag"], np.max(np.abs(off)) / fo["i1"])
        A = np.einsum("p,paj->aj", W, axial_current(U, Ud, L))
        kap = np.diag(A) / fo["gA"]
        kappas.extend(kap.tolist())
        maxdev["A_offdiag"] = max(maxdev["A_offdiag"], np.max(np.abs(A - np.diag(np.diag(A)))) / abs(fo["gA"]))
        T = stress(L)
        Trr = np.einsum("pi,pij,pj->p", n, T, n)
        Ttt = np.einsum("pi,pij,pj->p", eth, T, eth)
        Trt = np.einsum("pi,pij,pj->p", n, T, eth)
        sc = abs(fo["Trr"]) + abs(fo["Ttt"])
        maxdev["Trr"] = max(maxdev["Trr"], np.max(np.abs(Trr - fo["Trr"])) / sc)
        maxdev["Ttt"] = max(maxdev["Ttt"], np.max(np.abs(Ttt - fo["Ttt"])) / sc)
        maxdev["Trt"] = max(maxdev["Trt"], np.max(np.abs(Trt)) / sc)
        maxdev["Tsym"] = max(maxdev["Tsym"], np.max(np.abs(T - np.transpose(T, (0, 2, 1)))) / sc)
        if trial < 3:
            print(f"  x={x:.3f} F={F:.3f} F'={Fp:.3f}:  <i_11>/formula={I[0,0]/fo['i1']:.14f}  "
                  f"<i_44>/formula={I[3,3]/fo['i2']:.14f}  <i_88>={I[7,7]:.1e}  <A^3_3>/[gA bracket]={kap[2]:+.12f}")
    kappas = np.array(kappas)
    kappa = float(np.mean(kappas))
    maxdev["gA_ratio"] = float(np.max(np.abs(kappas - kappa)))
    for k, v in maxdev.items():
        print(f"  max relative deviation {k:10s}: {v:.2e}")
    print(f"  kappa = <A^a_a>/[ANW bracket] = {kappa:+.15f}   (1/12 -> ball integral = 2/3 of ANW's g_A; 1/8 would match it)")

    # ---------------------------------------------------------------- integrate over the profile
    sol = sh.solve_mapped(120, L=2.0)
    wb = sh.bary_weights(sol["N"])
    Xr = 40.0
    xr, wr = np.polynomial.legendre.leggauss(240)
    xr = 0.5 * Xr * (xr + 1)
    wr = 0.5 * Xr * wr
    tt = (xr - sol["L"]) / (xr + sol["L"])
    Fr = sh.bary_eval(sol["t"], sol["F"], wb, tt)
    Ftr = sh.bary_eval(sol["t"], sol["Ft"], wb, tt)
    Fpr = (1 - tt) ** 2 / (2 * sol["L"]) * Ftr
    n2, eth2, W2 = angular_grid(8, 10)
    Itot = np.zeros((8, 8))
    Etot = 0.0
    Atot = np.zeros((3, 3))
    for k in range(xr.size):
        U, Ud, L = fields(xr[k], Fr[k], Fpr[k], n2)
        wk = wr[k] * 4 * np.pi * xr[k] ** 2
        Itot += wk * np.einsum("p,pab->ab", W2, inertia_density(U, Ud, L))
        Etot += wk * np.dot(W2, energy_density(L))
        Atot += wk * np.einsum("p,paj->aj", W2, axial_current(U, Ud, L))
    fo = formulas(xr, Fr, Fpr)
    I1f = np.sum(wr * 4 * np.pi * xr ** 2 * fo["i1"])
    I2f = np.sum(wr * 4 * np.pi * xr ** 2 * fo["i2"])
    Ef = np.sum(wr * 4 * np.pi * xr ** 2 * fo["e"])
    gAf = np.sum(wr * xr ** 2 * fo["gA"])               # truncated-sphere D over [0, 40]
    print(f"\nprofile integrals over the ball x < {Xr:.0f} (same radial nodes for 3D and formula):")
    print("  diag I_ab (3D)  :", " ".join(f"{v:.9f}" for v in np.diag(Itot)))
    print(f"  formula I1, I2  : {I1f:.9f} {I2f:.9f}   max |offdiag| = {np.max(np.abs(Itot - np.diag(np.diag(Itot)))):.1e}")
    print(f"  energy 3D {Etot:.10f}  formula {Ef:.10f}")
    print(f"  int A^a_a d^3x (3D) = {np.diag(Atot)}  ;  4 pi kappa D_[0,40] = {4*np.pi*kappa*gAf:.10f}")

    # ---------------------------------------------------------------- (iii) axial form factor at small q
    # A_ai(x) = alpha(r) delta_ai + beta(r) n_a n_i. Read alpha, beta from the 3D current at n = z.
    nz = np.array([[0.0, 0.0, 1.0]])
    alpha = np.empty(xr.size); beta = np.empty(xr.size)
    for k in range(xr.size):
        U, Ud, L = fields(xr[k], Fr[k], Fpr[k], nz)
        A = axial_current(U, Ud, L)[0]
        alpha[k] = A[0, 0]
        beta[k] = A[2, 2] - A[0, 0]
    C = sol["C"]
    from scipy.special import spherical_jn as sjn
    from scipy.integrate import quad

    def j2_over_u_tail(u0):
        # int_{u0}^inf j2(u)/u du (split into pi-intervals to 4000, then asymptotic ~ -cos(u)/u^2)
        edges = np.concatenate([[u0], np.arange(np.ceil(u0 / np.pi) * np.pi, 4000.0, np.pi)])
        val = sum(quad(lambda u: sjn(2, u) / u, edges[i], edges[i + 1], epsabs=1e-14, epsrel=1e-12)[0]
                  for i in range(len(edges) - 1))
        return val
    # sign of the asymptotic current: alpha ~ sgn * C/(4 r^3), beta ~ -3 sgn C/(4 r^3)
    sgn = np.sign(alpha[-1] * xr[-1] ** 3 / C)
    ff = []
    for q in [0.2, 0.1, 0.05, 0.02, 0.01]:
        u = q * xr
        A11 = 4 * np.pi * np.sum(wr * xr ** 2 * (alpha * sjn(0, u) + beta * sjn(1, u) / u))
        A33 = 4 * np.pi * np.sum(wr * xr ** 2 * (alpha * sjn(0, u) + beta * (sjn(1, u) / u - sjn(2, u))))
        tl = j2_over_u_tail(q * Xr)
        A11 += sgn * (-np.pi * C * tl)
        A33 += sgn * (2 * np.pi * C * tl)
        ff.append((q, A11, A33))
    c_ball = float(np.diag(Atot).mean())
    U, Ud, L = fields(Xr, *[float(v) for v in (sh.bary_eval(sol["t"], sol["F"], wb, [(Xr - sol["L"]) / (Xr + sol["L"])])[0],
                                               (1 - (Xr - sol["L"]) / (Xr + sol["L"])) ** 2 / (2 * sol["L"]) *
                                               sh.bary_eval(sol["t"], sol["Ft"], wb, [(Xr - sol["L"]) / (Xr + sol["L"])])[0])], nz)
    AR = axial_current(U, Ud, L)[0]
    surf = 4 * np.pi / 3 * Xr ** 3 * AR[2, 2]          # (4pi/3) R^3 (alpha + beta)(R)
    print("\n(iii) axial form factor of the static hedgehog current, A~_ai(q) for q = q z (per 1/e^2):")
    print(f"  ball (R = {Xr:.0f}) integral c_ball = {c_ball:+.10f};  surface term (4pi/3) R^3 n.A.n at R: {surf:+.10f}"
          f";  R -> inf limit -(2pi/3) C sgn = {-sgn*2*np.pi/3*C:+.10f}")
    for q, A11, A33 in ff:
        print(f"  q = {q:5.2f}:  transverse A~_11 = {A11:+.9f} (ratio to c_ball {A11/c_ball:.7f})   longitudinal A~_33 = {A33:+.2e}")
    A11_0 = ff[-1][1]
    D_full = sol_D = sh.derived(sh.integrals_mapped(sol))["D_gA"]
    print(f"  D (whole space) = {D_full:.10f};  -2C = {-2*C:.10f}  (identity D = -2C from current conservation)")

    checks = {
        "energy_density": maxdev["e"] < 1e-12,
        "I1_density": maxdev["i1"] < 1e-12,
        "I2_density_Kopeliovich_22c": maxdev["i2"] < 1e-12,
        "I88_zero_offdiag_zero": maxdev["i8"] < 1e-12 and maxdev["offdiag"] < 1e-12,
        "axial_current_proportional_to_ANW_bracket_kappa_1/12": maxdev["gA_ratio"] < 1e-9 and abs(abs(kappa) - 1.0 / 12.0) < 1e-9 and maxdev["A_offdiag"] < 1e-9,
        "stress_tensor_Trr_Ttt": maxdev["Trr"] < 1e-9 and maxdev["Ttt"] < 1e-9 and maxdev["Trt"] < 1e-9 and maxdev["Tsym"] < 1e-9,
        "integrated_I_matches": abs(Itot[0, 0] / I1f - 1) < 1e-11 and abs(Itot[3, 3] / I2f - 1) < 1e-11 and abs(Itot[7, 7]) < 1e-10,
        "integrated_energy_matches": abs(Etot / Ef - 1) < 1e-11,
        "ball_integral_equals_surface_term": abs(c_ball / surf - 1) < 1e-9 and abs(c_ball / (-sgn * 2 * np.pi / 3 * C) - 1) < 1e-4,
        "longitudinal_form_factor_vanishes": max(abs(v[2]) for v in ff) < 1e-5 * abs(c_ball),
        "transverse_q0_is_3/2_of_ball": abs(A11_0 / c_ball - 1.5) < 1e-3,
        "identity_D_equals_-2C": abs(D_full / (-2 * C) - 1) < 1e-8,
    }
    print("\nCHECKS")
    for k, v in checks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    ok = all(checks.values())
    out = {
        "max_relative_deviations": {k: float(v) for k, v in maxdev.items()},
        "kappa_axial": float(kappa),
        "ball_X40": {"I_diag": np.diag(Itot).tolist(), "I1_formula": float(I1f), "I2_formula": float(I2f),
                     "I_offdiag_max": float(np.max(np.abs(Itot - np.diag(np.diag(Itot))))),
                     "E_3d": float(Etot), "E_formula": float(Ef)},
        "axial": {"c_ball_R40_per_e2": c_ball, "surface_term_R40": float(surf), "c_ball_Rinf": float(abs(2 * np.pi / 3 * C)), "C": float(C), "D_whole_space": float(D_full),
                  "transverse_FF": [[float(q), float(a), float(b)] for q, a, b in ff],
                  "gA_ball_times_e2": float(2.0 / 3.0 * abs(2 * np.pi / 3 * C)),
                  "gA_ANW_times_e2": float(np.pi / 3 * abs(D_full)),
                  "note": "ANW's g_A = -(pi/(3e^2)) D equals 3/2 of the ball-integral value; the 3/2 is the "
                          "q->0 transverse form factor of a conserved current with a massless pion pole"},
        "checks": {k: bool(v) for k, v in checks.items()}, "all_checks_pass": bool(ok), "runtime_s": time.time() - t0,
    }
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "verify.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nall checks pass: {ok};  runtime {time.time() - t0:.1f} s")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
