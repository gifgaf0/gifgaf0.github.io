"""E1a: static kink mass, shape-mode frequency, integrator checks.

Targets (PLAN.md E1a): M_kink = 2 sqrt2/3, omega_s = sqrt(3/2), relative 1e-4.
Run:  NUMBA_NUM_THREADS=2 ... python e1a_static.py   (about 20 s)
Writes e1a_results.json.
"""
import json
import time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.integrate import quad
from phi4core import (SQ2, M_KINK, grid, energy, Sim, outer_zero)

t0 = time.time()
OMEGA_S = np.sqrt(1.5)
res = {"convention": "V=(1/4)(phi^2-1)^2, m=sqrt2, kink tanh(x/sqrt2)",
       "targets": {"M_kink": M_KINK, "omega_s": OMEGA_S, "rel_tol": 1e-4}}


def lap4_matrix(n, dx):
    """4th-order Laplacian with zero ghost values (used for perturbations)."""
    c = 1.0 / (12 * dx * dx)
    diags = [-1 * c * np.ones(n - 2), 16 * c * np.ones(n - 1), -30 * c * np.ones(n),
             16 * c * np.ones(n - 1), -1 * c * np.ones(n - 2)]
    return sp.diags(diags, [-2, -1, 0, 1, 2], format="csc")


def lattice_kink(dx, L=40.0):
    """Newton solve of the discrete static equation, kink BCs -1 / +1, in the
    antisymmetric subspace phi(-x) = -phi(x) (removes the translation mode)."""
    x = grid(L, dx)
    n = x.size
    ic = n // 2
    D = lap4_matrix(n, dx).tocsr()
    c = 1.0 / (12 * dx * dx)
    bvec = np.zeros(n)
    # ghost values: phi(-L-dx)=phi(-L-2dx)=-1, phi(L+dx)=phi(L+2dx)=+1
    bvec[0] = c * (16 * (-1.0) - (-1.0))
    bvec[1] = c * (-(-1.0))
    bvec[-1] = c * (16 * (1.0) - 1.0)
    bvec[-2] = c * (-(1.0))
    M = n - ic - 1                     # unknowns: phi at x_j > 0
    rows = []
    cols = []
    vals = []
    for j in range(M):
        rows += [ic + 1 + j, ic - 1 - j]
        cols += [j, j]
        vals += [1.0, -1.0]
    P = sp.csr_matrix((vals, (rows, cols)), shape=(n, M))
    h = np.tanh(x[ic + 1:] / SQ2)
    for it in range(40):
        phi = P @ h
        R = (D @ phi + bvec - phi * (phi ** 2 - 1))[ic + 1:]
        J = ((D - sp.diags(3 * phi ** 2 - 1)) @ P).tocsr()[ic + 1:, :]
        dh = spla.spsolve(J.tocsc(), -R)
        h += dh
        if np.max(np.abs(dh)) < 1e-14:
            break
    phi = P @ h
    R = D @ phi + bvec - phi * (phi ** 2 - 1)
    return x, phi, float(np.max(np.abs(R[2:-2])))


# ---- 1. kink mass
Ek_exact_quad = quad(lambda x: 0.25 / np.cosh(x / SQ2) ** 4 + 0.25 * (np.tanh(x / SQ2) ** 2 - 1) ** 2,
                     -40, 40, epsabs=1e-13, epsrel=1e-13, limit=200)[0]
mass = {"quadrature_of_tanh_profile": Ek_exact_quad}
for dx in (0.1, 0.05, 0.025):
    x = grid(40.0, dx)
    phi = np.tanh(x / SQ2)
    E_tanh = energy(phi, np.zeros_like(x), dx, -1.0, 1.0)
    xk, phik, resid = lattice_kink(dx)
    E_lat = energy(phik, np.zeros_like(xk), dx, -1.0, 1.0)
    mass[f"dx={dx}"] = {"E_tanh_on_grid": E_tanh, "E_relaxed_lattice_kink": E_lat,
                        "rel_err_tanh": (E_tanh - M_KINK) / M_KINK,
                        "rel_err_relaxed": (E_lat - M_KINK) / M_KINK,
                        "newton_residual": resid,
                        "max|phi_lattice - tanh|": float(np.max(np.abs(phik - np.tanh(xk / SQ2))))}
res["kink_mass"] = mass
print("M_kink target", M_KINK)
for k, v in mass.items():
    print(" ", k, v)

# ---- 2. fluctuation spectrum around the kink (eigenvalues of -d2 + 3phi^2 - 1)
spec = {}
for dx in (0.1, 0.05, 0.025):
    xk, phik, _ = lattice_kink(dx, L=40.0)
    n = xk.size
    H = -lap4_matrix(n, dx) + sp.diags(3 * phik ** 2 - 1)
    vals = spla.eigsh(H.tocsc(), k=4, sigma=-0.5, which="LM", return_eigenvectors=False)
    vals = np.sort(vals)
    spec[f"dx={dx}"] = {"omega2": vals.tolist(), "omega_s": float(np.sqrt(vals[1])),
                        "rel_err_omega_s": float((np.sqrt(vals[1]) - OMEGA_S) / OMEGA_S),
                        "zero_mode_omega2": float(vals[0])}
res["spectrum"] = spec
print("shape mode target", OMEGA_S)
for k, v in spec.items():
    print(" ", k, v)

# ---- 3. dynamical shape-mode frequency (integrator check)
dyn = {}
for dx, eps in ((0.05, 0.01), (0.05, 0.005), (0.025, 0.005)):
    dt = 0.4 * dx
    xk, phik, _ = lattice_kink(dx, L=150.0)
    eta = np.tanh(xk / SQ2) / np.cosh(xk / SQ2)
    sim = Sim(xk, phik + eps * eta, np.zeros_like(xk), dt, Lphys=100.0, W=40.0,
              gmax=1.0, bL=-1.0, bR=1.0)
    nsteps = int(round(400.0 / dt))
    stride = 10
    amps = []
    times = []
    norm = np.sum(eta * eta)
    for c in range(nsteps // stride):
        sim.run(stride)
        amps.append(np.sum(eta * (sim.phi - phik)) / norm)
        times.append(sim.t)
    a = np.array(amps)
    tt = np.array(times)
    # frequency from zero crossings of the projection (linear interpolation)
    zc = []
    for i in range(len(a) - 1):
        if a[i] > 0 >= a[i + 1] or a[i] < 0 <= a[i + 1]:
            zc.append(tt[i] - a[i] * (tt[i + 1] - tt[i]) / (a[i + 1] - a[i]))
    zc = np.array(zc)
    # least-squares slope of crossing time vs index: half period
    idx = np.arange(len(zc))
    half_T = np.polyfit(idx, zc, 1)[0]
    w = np.pi / half_T
    dyn[f"dx={dx},eps={eps}"] = {"omega_s_dynamic": float(w),
                                  "rel_err": float((w - OMEGA_S) / OMEGA_S),
                                  "n_crossings": int(len(zc))}
res["shape_mode_dynamic"] = dyn
print("dynamic shape mode")
for k, v in dyn.items():
    print(" ", k, v)

# ---- 4. moving kink: speed and energy, energy conservation (no sponge)
mv = {}
for v in (0.3, 0.6):
    dx = 0.05
    dt = 0.4 * dx
    x = grid(80.0, dx)
    g = 1 / np.sqrt(1 - v * v)
    phi = np.tanh(g * (x + 20) / SQ2)
    pi = -(g * v / SQ2) / np.cosh(g * (x + 20) / SQ2) ** 2
    sim = Sim(x, phi, pi, dt, Lphys=None, bL=-1.0, bR=1.0)
    E0 = sim.energy()
    # position: zero of phi
    def zpos(p):
        i = np.where((p[:-1] < 0) & (p[1:] >= 0))[0][0]
        return x[i] - p[i] * dx / (p[i + 1] - p[i])
    z0 = zpos(sim.phi)
    sim.run(int(round(50.0 / dt)))
    z1 = zpos(sim.phi)
    E1 = sim.energy()
    mv[f"v={v}"] = {"measured_speed": float((z1 - z0) / 50.0), "E0": E0,
                    "gamma*M_kink": float(g * M_KINK), "rel_err_E": float((E0 - g * M_KINK) / (g * M_KINK)),
                    "rel_energy_drift_50": float((E1 - E0) / E0)}
res["moving_kink"] = mv
print("moving kink", mv)

# ---- verdicts
best_mass = mass["dx=0.025"]["rel_err_relaxed"]
best_ws = spec["dx=0.025"]["rel_err_omega_s"]
res["verdict"] = {
    "M_kink": {"value": mass["dx=0.025"]["E_relaxed_lattice_kink"], "rel_err": best_mass,
               "verdict": "CALIBRATED" if abs(best_mass) < 1e-4 else "MISS"},
    "omega_s": {"value": spec["dx=0.025"]["omega_s"], "rel_err": best_ws,
                "verdict": "CALIBRATED" if abs(best_ws) < 1e-4 else "MISS"},
    "baseline_dx=0.05": {"M_rel_err": mass["dx=0.05"]["rel_err_relaxed"],
                         "omega_s_rel_err": spec["dx=0.05"]["rel_err_omega_s"]},
}
res["runtime_s"] = time.time() - t0
print("verdicts", res["verdict"])
json.dump(res, open("e1a_results.json", "w"), indent=1)
print("runtime %.1f s" % res["runtime_s"])
