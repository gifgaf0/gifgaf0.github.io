"""
phase2_cell.py — GZ1 Phase 2 (REBUILD): oblique primitive cell, a* scan + polish
Targets (report §2): a* = 1.4576 ±0.5%, mu = 55.86 ±1%, residual <= 1e-2,
d_row = sqrt3 a*/2 ≈ 1.2623.
Protocol (prereg §2): 17-point scan over a of the energy density (fixed mean
density; the crystal picks its own a — scan window centred on the target-
independent big-box k_c estimate from phase1, ±10%), parabolic refine on the
best 3, then GP polish. Saves psi0_cell_n32.npy (pre-polish, downsampled) and
psi0_polished_n32.npy (polished, downsampled). -> phase2.json
"""
import json
import numpy as np
import gz1_core as core

N_SCAN = 64        # cell grid for the scan
N_POLISH = 64      # polish grid (downsampled to 32 for archive/BdG input)
SCAN_STEPS = 2500
POLISH_STEPS = 12000


def main():
    with open("phase1.json") as f:
        ph1 = json.load(f)
    a_centre = ph1["disk_fft_kernel"]["a_from_kc"]      # target-independent centre
    a_grid = np.linspace(0.9 * a_centre, 1.1 * a_centre, 17)

    es = []
    for a in a_grid:
        cell = core.Cell(a, N_SCAN)
        psi, mu, res = cell.relax(steps=SCAN_STEPS)
        e = cell.energy_density(psi)
        es.append(e)
        print(f"  a={a:.4f}  e/A={e:.6f}  mu={mu:.3f}  res={res:.1e}")
    es = np.array(es)
    i0 = int(np.argmin(es))
    # parabolic refine on the best 3
    if 0 < i0 < len(a_grid) - 1:
        x = a_grid[i0 - 1:i0 + 2]
        y = es[i0 - 1:i0 + 2]
        c = np.polyfit(x, y, 2)
        a_star = float(-c[1] / (2 * c[0]))
    else:
        a_star = float(a_grid[i0])

    # relax at a*, archive pre-polish state, then polish
    cell = core.Cell(a_star, N_POLISH)
    psi, mu_scan, res_scan = cell.relax(steps=SCAN_STEPS)
    np.save("psi0_cell_n32.npy", psi[::N_POLISH // 32, ::N_POLISH // 32].copy())
    psi, mu, res = cell.relax(steps=POLISH_STEPS, psi_init=psi, tol=1e-15)
    np.save("psi0_polished_n32.npy", psi[::N_POLISH // 32, ::N_POLISH // 32].copy())
    np.save("psi0_polished_n64.npy", psi)        # full-resolution polished state
    d_row = float(np.sqrt(3) * a_star / 2)

    out = dict(a_scan=[round(float(a), 5) for a in a_grid],
               e_scan=[round(float(e), 6) for e in es],
               a_star=round(a_star, 4),
               a_from_kc_phase1=a_centre,
               mu_cellrelax=round(mu_scan, 3),
               mu_polished=round(mu, 3),
               residual_polished=float(f"{res:.2e}"),
               d_row=round(d_row, 4),
               n_scan=N_SCAN, n_polish=N_POLISH)
    with open("phase2.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
