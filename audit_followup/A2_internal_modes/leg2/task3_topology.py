"""A2 leg 2 -- Task 3: vacuum manifold on the polar stratum P7 (and a mixed stratum) under group (c),
(i) degree <= 4 potential, (ii) with the theta-dependent T-even degree-6 invariant Re(S^3).

The homotopy statements are derived analytically in LEG2_REPORT.md; this script supplies the numerical
facts they rest on: the minimum set of explicit potentials (random-start minimisation), the phase values
of the 7-sector on that set, the number of connected components, and the potential along the
half-quantum loop.
"""
import json
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(2026)


def unpack(x, with0):
    if with0:
        psi0 = x[0] + 1j * x[1]
        psi7 = x[2:9] + 1j * x[9:16]
    else:
        psi0 = 0j
        psi7 = x[0:7] + 1j * x[7:14]
    return psi0, psi7


def V(x, P, with0):
    psi0, psi7 = unpack(x, with0)
    N = np.vdot(psi7, psi7).real
    S = np.sum(psi7 * psi7)
    r0 = abs(psi0) ** 2
    v = (-P["mu0"] * r0 - P["mu7"] * N + 0.5 * P["g00"] * r0 ** 2 + P["g07"] * r0 * N + 0.5 * P["g77"] * N ** 2
         - 0.5 * P["c"] * abs(S) ** 2 + P.get("g6", 0.0) * N ** 3 + P["lam6"] * (S ** 3).real)
    if P.get("lock", 0.0):  # the (a)-allowed, (c)-FORBIDDEN term Re(psi0^2 S-bar) (only for the alternative reading)
        v += P["lock"] * (psi0 ** 2 * np.conj(S)).real
    return v


def minima(P, with0, nstart=300):
    dim = 16 if with0 else 14
    sols = []
    for _ in range(nstart):
        x0 = rng.normal(size=dim)
        r = minimize(V, x0, args=(P, with0), method="BFGS", options=dict(gtol=1e-11, maxiter=5000))
        sols.append((r.fun, r.x))
    vmin = min(s[0] for s in sols)
    good = [x for (f, x) in sols if f < vmin + 1e-9]
    rows = []
    for x in good:
        psi0, psi7 = unpack(x, with0)
        N = np.vdot(psi7, psi7).real
        S = np.sum(psi7 * psi7)
        theta = (np.angle(S) / 2) % np.pi           # 7-sector phase, defined mod pi on the polar orbit
        nvec = np.exp(-1j * theta) * psi7 / np.sqrt(N)
        rows.append(dict(N=N, s_over_N=abs(S) / N, theta_mod_pi=theta, imag_n=float(np.abs(nvec.imag).max()),
                         rho0=abs(psi0) ** 2, theta0=float(np.angle(psi0)) if abs(psi0) > 1e-6 else None))
    return vmin, len(good), len(sols), rows


def cluster(vals, period, tol=1e-4):
    vals = sorted(v % period for v in vals)
    cl = []
    for v in vals:
        if cl and min(abs(v - cl[-1][0]), period - abs(v - cl[-1][0])) < tol:
            cl[-1][1] += 1
        else:
            cl.append([v, 1])
    if len(cl) > 1 and min(abs(cl[0][0] - cl[-1][0]), period - abs(cl[0][0] - cl[-1][0])) < tol:
        cl[0][1] += cl[-1][1]
        cl.pop()
    return cl


def half_quantum_barrier(P, nvec, mvec, theta_star, Nst):
    """V along the half-quantum loop psi(s) = sqrt(N*) e^{i(theta*+pi s)} (cos(pi s) n + sin(pi s) m), s in [0,1],
    at the radial value N* of the minimum set."""
    vals = []
    for s in np.linspace(0, 1, 721):
        psi7 = np.sqrt(Nst) * np.exp(1j * (theta_star + np.pi * s)) * (np.cos(np.pi * s) * nvec + np.sin(np.pi * s) * mvec)
        x = np.concatenate([psi7.real, psi7.imag])
        vals.append(V(x, P, False))
    vals = np.array(vals)
    return float(vals.max() - vals.min())


def main():
    out = {}
    base = dict(mu0=0.0, mu7=1.0, g00=1.0, g07=0.0, g77=1.0, c=0.2, lam6=0.0)
    # ---- P7, case (i): degree <= 4 only (c > 0 favours the polar orbit |S| = N)
    Pi = dict(base)
    vmin, ng, ns, rows = minima(Pi, False)
    th = [r["theta_mod_pi"] for r in rows]
    Nst_i = float(np.mean([r["N"] for r in rows]))
    out["P7_case_i"] = dict(potential="-mu7 N + g77/2 N^2 - c/2 |S|^2", vmin=vmin, n_minima=ng, n_starts=ns,
                            max_dev_polar=float(max(abs(r["s_over_N"] - 1) for r in rows)),
                            max_imag_n=float(max(r["imag_n"] for r in rows)),
                            theta_clusters_mod_pi=len(cluster(th, np.pi, 1e-3)),
                            theta_spread=[float(min(th)), float(max(th))])
    # ---- P7, case (ii): add lam6 Re(S^3), both signs
    Nst_ii = {}
    for lam in (+0.05, -0.05):
        Pii = dict(base, lam6=lam, g6=0.1)
        vmin, ng, ns, rows = minima(Pii, False)
        Nst_ii[lam] = float(np.mean([r["N"] for r in rows]))
        th = [r["theta_mod_pi"] for r in rows]
        cl = cluster(th, np.pi, 1e-4)
        out[f"P7_case_ii_lam6={lam}"] = dict(potential="case (i) + g6 N^3 + lam6 Re(S^3), g6=0.1 (bounds V below)", vmin=vmin, n_minima=ng, n_starts=ns,
                                             max_dev_polar=float(max(abs(r["s_over_N"] - 1) for r in rows)),
                                             max_imag_n=float(max(r["imag_n"] for r in rows)),
                                             theta_clusters_mod_pi=[[round(c[0], 6), c[1]] for c in cl],
                                             n_components=len(cl),
                                             spacing_over_pi=[round((cl[(i + 1) % len(cl)][0] - cl[i][0]) % np.pi / np.pi, 6) for i in range(len(cl))])
    # ---- barrier along the half-quantum loop
    nvec = np.zeros(7); nvec[0] = 1.0
    mvec = np.zeros(7); mvec[1] = 1.0
    out["half_quantum_loop_barrier"] = {
        "case_i": half_quantum_barrier(Pi, nvec, mvec, 0.0, Nst_i),
        "case_ii(lam6=+0.05, start at a minimum theta*=pi/6)": half_quantum_barrier(dict(base, lam6=0.05, g6=0.1), nvec, mvec, np.pi / 6, Nst_ii[0.05]),
        "expected_case_ii_barrier_2*lam6*N*^3": 2 * 0.05 * Nst_ii[0.05] ** 3,
    }
    # ---- mixed stratum under group (c): psi0 != 0 and polar 7-sector
    Pm = dict(mu0=1.0, mu7=1.0, g00=1.0, g07=0.5, g77=1.0, c=0.2, lam6=0.0)
    for lam in (0.0, 0.05):
        P = dict(Pm, lam6=lam, g6=(0.1 if lam else 0.0))
        vmin, ng, ns, rows = minima(P, True)
        th = [r["theta_mod_pi"] for r in rows]
        th0 = [r["theta0"] for r in rows if r["theta0"] is not None]
        out[f"mixed_c_lam6={lam}"] = dict(vmin=vmin, n_minima=ng,
                                          rho0_range=[float(min(r["rho0"] for r in rows)), float(max(r["rho0"] for r in rows))],
                                          max_dev_polar=float(max(abs(r["s_over_N"] - 1) for r in rows)),
                                          theta7_clusters_mod_pi=len(cluster(th, np.pi, 1e-4)),
                                          theta0_spread=[float(min(th0)), float(max(th0))],
                                          relative_phase_clusters=len(cluster([(2 * (t0 - t7)) % (2 * np.pi) for t0, t7 in
                                                                               zip(th0, th)], 2 * np.pi, 1e-3)))
    # alternative reading: add the (a)-type locking term (forbidden under (c))
    P = dict(Pm, lock=-0.1)
    vmin, ng, ns, rows = minima(P, True)
    th = [r["theta_mod_pi"] for r in rows]
    th0 = [r["theta0"] for r in rows]
    rel = [(2 * (t0 - t7)) % (2 * np.pi) for t0, t7 in zip(th0, th)]
    out["mixed_with_(a)-locking_term_Re(psi0^2 Sbar)"] = {"vmin": vmin, "n_minima": ng,
                                                          "theta0_spread": [float(min(th0)), float(max(th0))],
                                                          "relative_phase_2(theta0-theta7)_clusters": [[round(c[0], 5), c[1]] for c in cluster(rel, 2 * np.pi, 1e-3)]}
    print(json.dumps(out, indent=1))
    with open("task3_results.json", "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
