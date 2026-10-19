#!/usr/bin/env python3
"""
E3 part 3: inertia tensor of the embedded B = 1 hedgehog on all 14 directions of g2,
by direct 3D quadrature of the Skyrme Lagrangian (no radial formulas used).

U(x,t) = A(t) U0(x) A(t)^T,  Omega = A^T dA/dt = omega_a T_a  (B-orthonormal basis of g2)
L_0 = A (U0^T Omega U0 - Omega) A^T,   L_i = A U0^T d_i U0 A^T
Lagrangian with the (1/2) Tr_7 normalisation:
  T = (1/2) [ -(F^2/16) Tr_7(L_0 L_0) - (1/16 e^2) sum_i Tr_7([L_0, L_i]^2) ] = (1/2) I_ab omega_a omega_b
In x = e F r units, I_ab is in units of 1/(e^3 F):
  I_ab = int d^3x [ -(1/16) Tr_7(M_a M_b) - (1/16) sum_i Tr_7([M_a, l_i][M_b, l_i]) ],
  M_a = U0^T T_a U0 - T_a,  l_i = U0^T d_i U0.
Same for SU(3) (3x3, Tr_3) as a cross-check of the 8 su(3) directions.
Also: static energy and baryon number of hedgehogs in the long-root, short-root, index-4
and principal SU(2)s (B = Dynkin index), from the same quadrature.
Reads g2_basis.npz and profile_e3.npz.  Writes inertia_results.json.
"""
import json
import numpy as np
from scipy.interpolate import CubicHermiteSpline

alg = np.load("g2_basis.npz")
pr = np.load("profile_e3.npz")
basis, TL, TS, TG, TP, TSO3 = alg["basis"], alg["TL"], alg["TS"], alg["TG"], alg["TP"], alg["TSO3"]
spl = CubicHermiteSpline(pr["x"], pr["F"], pr["dF"])
dspl = CubicHermiteSpline(pr["x"], pr["dF"], pr["ddF"])
Xtab, Ctail = float(pr["X"]), float(pr["C"])


def profile(x):
    x = np.asarray(x, float)
    xi = np.minimum(x, Xtab)
    F, dF = spl(xi), dspl(xi)
    xo = np.maximum(x, Xtab)
    Fo = Ctail / xo**2 - Ctail**3 / (21 * xo**6)
    dFo = -2 * Ctail / xo**3 + 6 * Ctail**3 / (21 * xo**7)
    return np.where(x <= Xtab, F, Fo), np.where(x <= Xtab, dF, dFo)


def angular_grid(nmu, nphi):
    mu, wmu = np.polynomial.legendre.leggauss(nmu)
    phi = 2 * np.pi * np.arange(nphi) / nphi
    MU, PH = np.meshgrid(mu, phi, indexing='ij')
    st = np.sqrt(1 - MU**2)
    n = np.stack([st * np.cos(PH), st * np.sin(PH), MU], -1).reshape(-1, 3)
    w = (wmu[:, None] * np.full(nphi, 2 * np.pi / nphi)[None, :]).ravel()
    return n, w


def radial_grid(nr, c=2.0):
    t, wt = np.polynomial.legendre.leggauss(nr)
    t = 0.5 * (t + 1); wt = 0.5 * wt
    x = c * t / (1 - t)
    return x, wt * c / (1 - t)**2


def hedgehog_fields(Xgen, x, n):
    """U0 = exp(F n.X), d_i U0 for generators X_a (X = -2 T, so X acts as i sigma on doublets)."""
    F, dF = profile(x)
    K = np.einsum('pa,aij->pij', n, Xgen)
    # exp(F K) by eigen-decomposition of the (real antisymmetric or anti-Hermitian) K: exact for any spin content
    w_, V = np.linalg.eigh(1j * K)          # i K is Hermitian: K = V diag(-i w) V^+
    ev = -1j * w_
    E = np.exp(F * ev)
    Vi = np.conj(np.swapaxes(V, 1, 2))
    U = np.einsum('pij,pj,pjk->pik', V, E, Vi)
    # derivative: d_i exp(F K) = F' n_i K U + int_0^1 exp(sFK) F d_iK exp((1-s)FK) ds   (eigenbasis formula)
    dK = (Xgen[None, :, :, :] - n[:, :, None, None] * K[:, None, :, :]) / x      # (p, i, d, d)
    mu_i, mu_j = F * ev[:, :, None], F * ev[:, None, :]
    d = mu_i - mu_j
    small = np.abs(d) < 1e-4
    dsafe = np.where(small, 1.0, d)
    # (e^{mu_i} - e^{mu_j}) / (mu_i - mu_j), with a series for nearly equal arguments (no cancellation)
    phi = np.where(small, np.exp(mu_j) * (1 + d / 2 + d**2 / 6 + d**3 / 24 + d**4 / 120),
                   (np.exp(mu_i) - np.exp(mu_j)) / dsafe)
    dKe = np.einsum('pab,pibc,pcd->piad', Vi, dK, V)           # dK in eigenbasis
    dU_tan = np.einsum('pab,pibc,pcd->piad', V, F * phi[:, None, :, :] * dKe, Vi)
    dU = dF * n[:, :, None, None] * np.einsum('pij,pjk->pik', K, U)[:, None] + dU_tan
    if np.isrealobj(Xgen):
        U, dU = U.real, dU.real
    return U, dU


def tensors(Xgen, Tgen, nr=64, nmu=10, nphi=20, trnorm=0.5, want_inertia=True):
    """inertia tensor I_ab (1/(e^3F)), static energy (F/e), baryon number"""
    xs, wx = radial_grid(nr)
    n, wa = angular_grid(nmu, nphi)
    nT = len(Tgen)
    I = np.zeros((nT, nT))
    E2 = E4 = Bn = 0.0
    eps = np.zeros((3, 3, 3))
    for (a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        eps[a, b, c] = 1; eps[b, a, c] = -1
    for x, w in zip(xs, wx):
        U, dU = hedgehog_fields(Xgen, x, n)
        Ud = np.conj(np.swapaxes(U, 1, 2))
        l = np.einsum('pij,pkjl->pkil', Ud, dU)                         # l_i = U^+ d_i U
        meas = w * x**2
        tr = lambda A, B: np.einsum('...ij,...ji->...', A, B)
        # static energy (normalisation trnorm * Tr): -(1/16) Tr(l l) - (1/32) sum_ij Tr([l_i,l_j]^2)
        e2 = -(1 / 16) * trnorm * sum(tr(l[:, i], l[:, i]) for i in range(3))
        comm = lambda A, B: np.einsum('pij,pjk->pik', A, B) - np.einsum('pij,pjk->pik', B, A)
        e4 = 0.0
        for i in range(3):
            for j in range(3):
                if i != j:
                    cij = comm(l[:, i], l[:, j])
                    e4 = e4 - (1 / 32) * trnorm * tr(cij, cij)
        E2 += meas * np.sum(wa * np.real(e2))
        E4 += meas * np.sum(wa * np.real(e4))
        # baryon density  -(1/24 pi^2) eps_ijk trnorm Tr(l_i l_j l_k)
        bd = 0.0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if eps[i, j, k] != 0:
                        bd = bd + eps[i, j, k] * tr(np.einsum('pij,pjk->pik', l[:, i], l[:, j]), l[:, k])
        Bn += meas * np.sum(wa * np.real(-(1 / (24 * np.pi**2)) * trnorm * bd))
        if want_inertia:
            M = np.einsum('pij,ajk,pkl->pail', Ud, Tgen, U) - Tgen[None]
            t1 = -(1 / 16) * (2 * trnorm) * np.einsum('paij,pbji->pab', M, M)
            t2 = 0.0
            for i in range(3):
                C = np.einsum('paij,pjk->paik', M, l[:, i]) - np.einsum('pij,pajk->paik', l[:, i], M)
                t2 = t2 - (1 / 16) * (2 * trnorm) * np.einsum('paij,pbji->pab', C, C)
            I += meas * np.real(np.einsum('p,pab->ab', wa, t1 + t2))
    return dict(I=I, E2=E2, E4=E4, M=E2 + E4, B=Bn)


if __name__ == "__main__":
    hh = json.load(open("hedgehog_results.json"))["final"]
    res = {"radial_formulas": {"I1_(2pi/3)Lambda": hh["I1"], "I2_Kopeliovich": hh["I2_radial"], "M": hh["M"]}}
    XL = -2 * TL
    out = {}
    for tag, (nr, nmu, nphi) in {"coarse": (48, 8, 16), "fine": (96, 12, 24)}.items():
        r = tensors(XL, basis, nr, nmu, nphi)
        out[tag] = r
        ev = np.linalg.eigvalsh(r["I"])
        print(f"[{tag}] nr={nr} nmu={nmu} nphi={nphi}: M={r['M']:.8f} E2={r['E2']:.8f} E4={r['E4']:.8f} B={r['B']:.10f}")
        print("   eigenvalues of I_ab:", np.round(ev, 6))
    I = out["fine"]["I"]
    blocks = {"long (3)": I[0:3, 0:3], "short (3)": I[3:6, 3:6], "(2,4) (8)": I[6:, 6:]}
    offd = max(np.abs(I[0:3, 3:]).max(), np.abs(I[3:6, 6:]).max())
    I1n = np.mean(np.diag(I[0:3, 0:3]))
    I2n = np.mean(np.diag(I[6:, 6:]))
    I0n = np.abs(I[3:6, 3:6]).max()
    res["g2_inertia_tensor_fine"] = I.tolist()
    res["g2_inertia_eigenvalues_fine"] = np.linalg.eigvalsh(I).tolist()
    res["g2_inertia_eigenvalues_coarse"] = np.linalg.eigvalsh(out["coarse"]["I"]).tolist()
    res["I1_3d"] = I1n
    res["I2_3d"] = I2n
    res["short_block_max_abs"] = I0n
    res["max_offblock"] = offd
    res["spread_within_long_block"] = float(np.ptp(np.linalg.eigvalsh(I[0:3, 0:3])))
    res["spread_within_(2,4)_block"] = float(np.ptp(np.linalg.eigvalsh(I[6:, 6:])))
    res["coarse_vs_fine_max_diff"] = float(np.abs(out["coarse"]["I"] - I).max())
    res["static_3d"] = {k: out["fine"][k] for k in ("M", "E2", "E4", "B")}
    print(f"I1 (3D) = {I1n:.8f}   radial (2pi/3)Lambda = {hh['I1']:.8f}   rel diff {abs(I1n/hh['I1']-1):.2e}")
    print(f"I2 (3D) = {I2n:.8f}   radial Kopeliovich   = {hh['I2_radial']:.8f}   rel diff {abs(I2n/hh['I2_radial']-1):.2e}")
    print(f"short block max |I| = {I0n:.2e},  max off-block = {offd:.2e}")
    # SU(3) 3x3 cross-check with Tr_3
    lam = np.zeros((8, 3, 3), complex)
    lam[0][0, 1] = lam[0][1, 0] = 1
    lam[1][0, 1] = -1j; lam[1][1, 0] = 1j
    lam[2][0, 0] = 1; lam[2][1, 1] = -1
    lam[3][0, 2] = lam[3][2, 0] = 1
    lam[4][0, 2] = -1j; lam[4][2, 0] = 1j
    lam[5][1, 2] = lam[5][2, 1] = 1
    lam[6][1, 2] = -1j; lam[6][2, 1] = 1j
    lam[7] = np.diag([1, 1, -2]) / np.sqrt(3)
    T3x3 = -0.5j * lam
    r3 = tensors(-2 * T3x3[:3], T3x3, 96, 12, 24, trnorm=1.0)
    ev3 = np.linalg.eigvalsh(r3["I"])
    print("SU(3) (3x3, Tr_3) inertia eigenvalues:", np.round(ev3, 6), " M =", round(r3["M"], 8), " B =", round(r3["B"], 10))
    res["su3_inertia_eigenvalues"] = ev3.tolist()
    res["su3_inertia_diag"] = np.diag(r3["I"]).tolist()
    # the same 8 directions inside g2
    TGb = np.array([TG[k] for k in range(8)])
    rG = tensors(XL, TGb, 96, 12, 24)
    res["su3_directions_inside_g2_diag"] = np.diag(rG["I"]).tolist()
    res["su3_vs_g2_max_diff"] = float(np.abs(rG["I"] - r3["I"]).max())
    print("su(3) directions inside g2 (Tr_7/2):", np.round(np.diag(rG["I"]), 6), " max diff to 3x3:", f"{res['su3_vs_g2_max_diff']:.1e}")
    # hedgehogs in the other SU(2) subgroups: B and M should scale with the Dynkin index
    hed = {}
    for name, T in [("long_root", TL), ("short_root", TS), ("index4_diag", TL + TS), ("index4_SO3", TSO3), ("principal", TP)]:
        r = tensors(-2 * np.array(T), basis, 64, 14, 28, want_inertia=False)
        hed[name] = {"B": r["B"], "M_over_M1": r["M"] / out["fine"]["M"]}
        print(f"hedgehog in {name:12s}: B = {r['B']:.8f},  M/M_long = {r['M']/out['fine']['M']:.8f}")
    res["hedgehogs_in_su2_subgroups"] = hed
    # verdicts
    checks = {
        "I1 x3 equals SU(2) I1 (radial formula) to 1e-6": abs(I1n / hh["I1"] - 1) < 1e-6 and res["spread_within_long_block"] < 1e-8,
        "I2 x8 equals SU(3) strange I2 (radial formula) to 1e-6": abs(I2n / hh["I2_radial"] - 1) < 1e-6 and res["spread_within_(2,4)_block"] < 1e-8,
        "short-root block vanishes (<1e-10)": I0n < 1e-10,
        "tensor block-diagonal (<1e-10)": offd < 1e-10,
        "su(3) directions in g2 (Tr_7/2) = 3x3 SU(3) (Tr_3) to 1e-10": res["su3_vs_g2_max_diff"] < 1e-10,
        "static energy (3D) = radial M to 1e-6": abs(out["fine"]["M"] / hh["M"] - 1) < 1e-6,
        "B(long, short, index-4, principal) = 1, 3, 4, 28": np.allclose([hed[k]["B"] for k in ("long_root", "short_root", "index4_diag", "index4_SO3", "principal")], [1, 3, 4, 4, 28], atol=1e-6),
    }
    for k, v in checks.items():
        print(("PASS " if v else "FAIL ") + k)
    res["checks"] = {k: bool(v) for k, v in checks.items()}
    with open("inertia_results.json", "w") as fh:
        json.dump(res, fh, indent=1, default=float)
