"""A2 leg 2 -- Task 4: Watanabe-Murayama counting for the first-order (GP) dynamics.

rho_ab = psi^dagger [T_a, T_b] psi with T_a anti-Hermitian generators on C^8 (index 0 = e0, 1..7 = e1..e7).
n_BG = rank of the real-linear map T -> T psi;  n_B = rank(rho)/2;  n_A = n_BG - 2 n_B.

Independent check: the linearised GP (Bogoliubov) spectrum for an explicit potential with exactly the
stated symmetry; count gapless branches and fit their small-k exponent (1 = linear, 2 = quadratic).
"""
import itertools
import json
import numpy as np
import sympy as sp

import octonion_g2 as og


def E(i, j, n=8):
    M = np.zeros((n, n), dtype=complex)
    M[i, j] = 1.0
    return M


def gens_u8():
    G = []
    for i in range(8):
        G.append(1j * E(i, i))
    for i, j in itertools.combinations(range(8), 2):
        G.append(E(i, j) - E(j, i))
        G.append(1j * (E(i, j) + E(j, i)))
    return G


def gens_so7_u1_u1():
    G = [E(i, j) - E(j, i) for i, j in itertools.combinations(range(1, 8), 2)]  # so(7) on Im O
    G.append(1j * E(0, 0))                                                    # u(1)_psi0
    G.append(1j * sum(E(k, k) for k in range(1, 8)))                         # u(1)_7
    return G


def gens_g2(extra_u1_7=False):
    _, D7, _, _, _ = og.build_all()
    G = []
    for D in D7:
        M = np.zeros((8, 8), dtype=complex)
        M[1:, 1:] = np.array(D.tolist(), dtype=float)
        G.append(M)
    G.append(1j * E(0, 0))
    if extra_u1_7:
        G.append(1j * sum(E(k, k) for k in range(1, 8)))
    return G


def wm(G, psi, tol=1e-9):
    # check generators anti-Hermitian
    assert all(np.allclose(T.conj().T, -T) for T in G)
    Tpsi = np.array([np.concatenate([(T @ psi).real, (T @ psi).imag]) for T in G]).T  # 16 x dimG
    s = np.linalg.svd(Tpsi, compute_uv=False)
    nBG = int((s > tol * max(1, s.max())).sum())
    rho = np.array([[np.vdot(psi, (Ta @ Tb - Tb @ Ta) @ psi) for Tb in G] for Ta in G])
    assert np.allclose(rho.real, 0, atol=1e-12)  # purely imaginary
    r = rho.imag
    assert np.allclose(r, -r.T)
    sr = np.linalg.svd(r, compute_uv=False)
    rk = int((sr > tol * max(1, sr.max())).sum())
    return dict(dimG=len(G), n_BG=nBG, rank_rho=rk, n_B=rk // 2, n_A=nBG - rk, unbroken=len(G) - nBG)


def vacua(seed=5):
    rng = np.random.default_rng(seed)
    nhat = rng.normal(size=8) + 1j * rng.normal(size=8)
    nhat /= np.linalg.norm(nhat)
    e0 = np.zeros(8, dtype=complex); e0[0] = 1
    n = np.zeros(8); n[1:] = rng.normal(size=7); n /= np.linalg.norm(n)
    u = np.zeros(8); v = np.zeros(8)
    a = rng.normal(size=7); b = rng.normal(size=7)
    a /= np.linalg.norm(a); b -= a * (a @ b); b /= np.linalg.norm(b)
    u[1:] = a; v[1:] = b
    F7 = (u + 1j * v) / np.sqrt(2)
    return dict(P0=nhat, R=e0, P7=n.astype(complex), F7=F7)


# ---------------------------------------------------------------------------------------------
# Bogoliubov check in real coordinates phi = (x, y) in R^16, psi = x + i y.
# GP: i d_t psi = -(1/2) lap psi + dV/dpsi* - mu psi  <=>  phi_dot = (1/2) J grad E,  J = [[0,1],[-1,0]],
# linearised at wavevector k: d phi_dot = (1/2) J (k^2 1 + Hess e) d phi,  e = V - mu |phi|^2.
def bogoliubov(Vexpr, xs, ys, phibar, ks):
    allv = list(xs) + list(ys)
    grad = [sp.diff(Vexpr, v) for v in allv]
    hess = [[sp.diff(g, v) for v in allv] for g in grad]
    fg = sp.lambdify(allv, grad, "numpy")
    fh = sp.lambdify(allv, hess, "numpy")
    g = np.array(fg(*phibar), dtype=float)
    mu = g @ phibar / (2 * phibar @ phibar)
    stat = float(np.abs(g - 2 * mu * phibar).max())
    Hm = np.array(fh(*phibar), dtype=float) - 2 * mu * np.eye(16)
    J = np.block([[np.zeros((8, 8)), np.eye(8)], [-np.eye(8), np.zeros((8, 8))]])
    mineig_hess = float(np.linalg.eigvalsh(Hm).min())
    spec = []
    for k in ks:
        A = 0.5 * J @ (k ** 2 * np.eye(16) + Hm)
        w = np.linalg.eigvals(A)
        om = np.sort(np.abs(w.imag[w.imag > -1e-12]))[:8] if False else np.sort(np.abs(w.imag))[::2]
        assert np.abs(w.real).max() < 1e-7, "dynamical instability"
        spec.append(om)
    spec = np.array(spec)  # len(ks) x 8, sorted per k
    return mu, stat, mineig_hess, spec


def classify(spec, ks):
    """Exponent of each branch from two small k: p ~ 0 gapped, p ~ 1 linear, p ~ 2 quadratic."""
    out = {"linear": 0, "quadratic": 0, "gapped": 0, "exponents": [], "gaps": [], "linear_speeds": []}
    for b in range(spec.shape[1]):
        w0 = spec[0, b]; w1 = spec[1, b]
        p = np.log(w1 / w0) / np.log(ks[1] / ks[0])
        out["exponents"].append(round(float(p), 4))
        if abs(p) < 0.05:
            out["gapped"] += 1
            out["gaps"].append(round(float(w0), 6))
        elif abs(p - 1) < 0.05:
            out["linear"] += 1
            out["linear_speeds"].append(round(float(w0 / ks[0]), 6))
        elif abs(p - 2) < 0.05:
            out["quadratic"] += 1
    return out


def main():
    res = {}
    vac = vacua()
    G_u8 = gens_u8()
    G_acc = gens_so7_u1_u1()
    res["requested"] = {
        "P0 (U(8))": wm(G_u8, vac["P0"]),
        "R (SO7xU1psi0xU1_7)": wm(G_acc, vac["R"]),
        "P7 (SO7xU1psi0xU1_7)": wm(G_acc, vac["P7"]),
        "F7 (SO7xU1psi0xU1_7)": wm(G_acc, vac["F7"]),
    }
    # supplementary: the action's continuous group G2 x U(1)_psi0, and G2 x U(1)_psi0 x U(1)_7
    G_g2 = gens_g2(False)
    G_g2b = gens_g2(True)
    res["supplementary_G2xU1psi0"] = {k: wm(G_g2, vac[k]) for k in ("R", "P7", "F7")}
    res["supplementary_G2xU1psi0xU1_7"] = {k: wm(G_g2b, vac[k]) for k in ("R", "P7", "F7")}
    res["supplementary_P0_under_SO7xU1xU1(generic nhat)"] = wm(G_acc, vac["P0"])

    # Bogoliubov confirmation
    xs = sp.symbols("x0:8"); ys = sp.symbols("y0:8")
    psi = [xs[i] + sp.I * ys[i] for i in range(8)]
    rho = sum(xs[i] ** 2 + ys[i] ** 2 for i in range(8))
    r0 = xs[0] ** 2 + ys[0] ** 2
    N7 = sum(xs[i] ** 2 + ys[i] ** 2 for i in range(1, 8))
    Sre = sum(xs[i] ** 2 - ys[i] ** 2 for i in range(1, 8)); Sim = sum(2 * xs[i] * ys[i] for i in range(1, 8))
    absS2 = Sre ** 2 + Sim ** 2
    g, D, c = 1.0, 0.3, 0.2
    pots = {
        "P0": (g / 2 * rho ** 2, vac["P0"]),
        "R": (g / 2 * rho ** 2 + D * N7, vac["R"]),
        "P7": (g / 2 * rho ** 2 + D * r0 - c / 2 * absS2, vac["P7"]),
        "F7": (g / 2 * rho ** 2 + D * r0 + c / 2 * absS2, vac["F7"]),
    }
    ks = np.array([1e-4, 2e-4])
    bog = {}
    for name, (Vx, ps) in pots.items():
        phibar = np.concatenate([ps.real, ps.imag])
        mu, stat, mh, spec = bogoliubov(Vx, xs, ys, phibar, ks)
        cl = classify(spec, ks)
        bog[name] = dict(potential=str(Vx) if len(str(Vx)) < 80 else name + "-type quartic (see code)", mu=round(float(mu), 8),
                         stationarity_residual=stat, min_hessian_eig=round(mh, 8), **cl)
    res["bogoliubov_check"] = bog
    print(json.dumps(res, indent=1))
    with open("task4_results.json", "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
