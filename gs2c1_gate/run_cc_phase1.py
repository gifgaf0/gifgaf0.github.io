#!/usr/bin/env python3
# run_cc_phase1.py — G-S2C1 CC leg Phase 1: crystallize the gem8 p6m single crystal at
# FIXED mu = 53.225 by the own solver, at the three resolutions n in {24, 32, 40}.
# Reports <rho> (a prediction of the record tuple, not an input), grand energy per cell,
# spectral tail, residual, and lambda_min(L) at Gamma per resolution. Writes cc_phase1.json
# and cc_psi0_n{24,32,40}.npy.
import json
import numpy as np
import s2c1_cc_core as core

RES = [24, 32, 40]


def spectral_tail(cell, c):
    n = cell.n
    edge = (np.abs(cell.M1) == n // 2 - 1) | (np.abs(cell.M2) == n // 2 - 1)
    return float(np.max(np.abs(c[edge & cell.band])) / np.max(np.abs(c)))


def main():
    out = {"gate": "G-S2C1", "leg": "cc", "phase": 1, "mu_fixed": core.MU,
           "kernel": "U(r) = 20*exp(-r^8)", "a_star": core.A_STAR,
           "solver": "L-BFGS-B direct minimization + dense-Newton polish + exact p6m symmetrization",
           "resolutions": {}}
    prev = None
    for n in RES:
        cell = core.Cell(n)
        if prev is None:
            c, res, hist = core.crystallize(cell)
        else:
            seed = core.prolong(prev[0], cell, prev[1])
            c, res, hist = core.crystallize_from_seed(cell, seed)
        rho_hat, psip = cell.rho_hat_padded(c)
        mean_rho = float(rho_hat[0, 0].real)
        E, _ = cell.energy_grad(cell.grid(c).real)
        fl = core.Fluct(cell, c)
        L, X, _ = fl.matrices(0.0, 0.0)
        lamL = np.linalg.eigvalsh(L)
        entry = {
            "n": n, "dim_band": fl.d,
            "residual_rel": res,
            "residual_le_1e-10": bool(res <= 1e-10),
            "mean_rho": mean_rho,
            "rho_max": float(np.max(psip ** 2)), "rho_min": float(np.min(psip ** 2)),
            "grand_energy_per_cell": float(E),
            "spectral_tail": spectral_tail(cell, c),
            "lambda_min_L_Gamma": float(lamL[0]),
            "lambda_min_L_Gamma_ge_minus1e-12": bool(lamL[0] >= -1e-12),
            "solver_history": [[t, int(i), float(r)] for (t, i, r) in hist],
        }
        out["resolutions"][str(n)] = entry
        np.save("cc_psi0_n%d.npy" % n, c)
        print(json.dumps(entry, indent=1))
        prev = (cell, c)
    rec = out["resolutions"][str(RES[-1])]
    out["record"] = {"resolution_of_record": RES[-1],
                     "mean_rho": rec["mean_rho"],
                     "residual_rel": rec["residual_rel"],
                     "lambda_min_L_Gamma": rec["lambda_min_L_Gamma"]}
    json.dump(out, open("cc_phase1.json", "w"), indent=1)
    print("phase 1 complete; record:", json.dumps(out["record"]))

if __name__ == "__main__":
    main()
