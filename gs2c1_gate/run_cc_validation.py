#!/usr/bin/env python3
# run_cc_validation.py — G-S2C1 CC leg: instrument validation BEFORE any framework quantity.
# V-1 finite-difference check of the energy gradient (n=16, deterministic perturbation)
# V-2 Hermiticity of the dense Bloch matrices at a generic k
# V-3 exact analytic control: uniform state at reduced mu; the Bloch spectrum from the
#     identical pipeline must match the closed Bogoliubov form
#     w2(q) = (q^2/2) * (q^2/2 + 2*rho*Uhat(q)),  q = |G + k|,
#     to near machine precision (this validates kernel table + operators + Hermitian form)
# V-4 fitter injection control at the harness level is run in Phase 4 (F-CTRL-INJ) on real
#     ladder data; here a synthetic pre-check of the same fitter code path.
import json
import numpy as np
import s2c1_cc_core as core


def v1_gradient():
    cell = core.Cell(16)
    rng = np.random.default_rng(20260903)
    y = 0.9 + 0.2 * rng.standard_normal((16, 16))
    E, g = cell.energy_grad(y)
    dy = rng.standard_normal((16, 16))
    dy /= np.linalg.norm(dy)
    errs = []
    for h in (1e-5, 1e-6):
        Ep, _ = cell.energy_grad(y + h * dy)
        Em, _ = cell.energy_grad(y - h * dy)
        fd = (Ep - Em) / (2 * h)
        an = float(np.sum(g * dy))
        errs.append(abs(fd - an) / max(abs(an), 1e-300))
    return {"rel_err": errs, "pass": bool(min(errs) < 1e-8)}


def v2_hermiticity():
    cell = core.Cell(24)
    c, res, _ = core.crystallize(cell, lbfgs_maxiter=1500, newton_iters=8)
    fl = core.Fluct(cell, c)
    k = 0.13 * core.direction_unit("GM") / core.A_STAR
    L, X, asym = fl.matrices(k[0], k[1])
    aL = float(np.linalg.norm(L - L.conj().T) / np.linalg.norm(L))
    return {"asym_X_presym": asym, "asym_L": aL, "crys_res": res,
            "pass": bool(asym < 1e-12 and aL < 1e-14)}


def v3_uniform_bogoliubov():
    # uniform state: mu_u = rho * Uhat(0); pick rho = 0.5 (uniform stationary by symmetry)
    n = 24
    cell = core.Cell(n)
    rho = 0.5
    u0 = float(core.uhat_radial(np.array([0.0]))[0])
    mu_save = core.MU
    core.MU = rho * u0
    try:
        c = np.zeros((n, n), complex)
        c[0, 0] = np.sqrt(rho)
        res, _ = cell.residual_rel(c)
        fl = core.Fluct(cell, c)
        errs = []
        for tag, ka in (("GK", 0.21), ("GM", 0.037)):
            k = ka * core.direction_unit(tag) / core.A_STAR
            out = fl.hermitian_spectrum(k[0], k[1], nlow=6)
            qx = fl.kvx + k[0]
            qy = fl.kvy + k[1]
            q = np.sqrt(qx ** 2 + qy ** 2)
            eps_k = 0.5 * q ** 2
            w2_exact = np.sort(eps_k * (eps_k + 2.0 * rho * core.uhat_radial(q)))[:6]
            w2_num = np.sort([m[0] for m in out["modes"]])
            errs.append(float(np.max(np.abs(w2_num - w2_exact) / np.maximum(np.abs(w2_exact), 1e-12))))
        return {"uniform_residual": res, "max_rel_err_w2": errs, "pass": bool(max(errs) < 1e-8)}
    finally:
        core.MU = mu_save


def joint_fit(ka_arr, y_arr):
    """Joint LSQ y = c (1 + a2 x + a4 x^2), x = (ka)^2 — the A-2 estimator's fitter."""
    x = np.asarray(ka_arr) ** 2
    V = np.vstack([np.ones_like(x), x, x * x]).T
    p, *_ = np.linalg.lstsq(V, np.asarray(y_arr), rcond=None)
    return float(p[0]), float(p[1] / p[0]), float(p[2] / p[0])


def v4_fitter_synthetic():
    ka = np.array([0.3, 0.15, 0.075, 0.0375])
    c_true, a2_true, a4_true = 8.5, 3.4e-3, -2.1e-2
    y = c_true * (1 + a2_true * ka ** 2 + a4_true * ka ** 4)
    c, a2, a4 = joint_fit(ka, y)
    return {"rel_err": [abs(c - c_true) / c_true, abs(a2 - a2_true) / abs(a2_true),
                        abs(a4 - a4_true) / abs(a4_true)],
            "pass": bool(abs(a2 - a2_true) / abs(a2_true) < 1e-9)}


def main():
    out = {"V1_gradient_fd": v1_gradient(),
           "V4_fitter_synthetic": v4_fitter_synthetic()}
    out["V2_hermiticity"] = v2_hermiticity()
    out["V3_uniform_bogoliubov"] = v3_uniform_bogoliubov()
    out["all_pass"] = all(out[k]["pass"] for k in out if k != "all_pass")
    json.dump(out, open("cc_instrument_validation.json", "w"), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
