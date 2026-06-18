"""
phase3a_bands.py — GZ1 Phase 3a (REBUILD): plane-wave BdG, normal-incidence line
Targets (report §3): sanity gates (a) min eig L(Gamma) ≈ 0, eigvec = psi0
(overlap > 0.999); (b) three Goldstone zeros at Gamma (3 lowest < 0.5, 4th >= 5);
(c) cutoff stability n=32 vs n=40 (gap-edge shift <= 0.5%).
Acoustic density branch gapless 0 -> ~20.4. Gap edges within ±1%:
A (20.405, 22.248), A2 (25.225, 25.615), B (29.838, 33.291). -> phase3a_line.json
"""
import json
import numpy as np
import gz1_core as core

NKLINE = 61
NBANDS = 24


def band_line(bdg, cell, nk=NKLINE):
    My = cell.b2 / 2.0
    ss = np.linspace(0.0, 1.0, nk)
    return ss, [bdg.omegas(s * My, NBANDS) for s in ss]


def main():
    with open("phase2.json") as f:
        ph2 = json.load(f)
    a_star, mu = ph2["a_star"], ph2["mu_polished"]
    psi0 = np.load("psi0_polished_n64.npy")
    cell = core.Cell(a_star, psi0.shape[0])

    # n=32 basis
    bdg = core.BdG(cell, psi0, mu, 32)
    lmin, overlap = bdg.L_gamma_check(psi0)
    wG = bdg.omegas(np.zeros(2), NBANDS)
    gate_a = abs(lmin) < 1.0 and overlap > 0.999
    gate_b = bool(np.all(wG[:3] < 0.5) and wG[3] >= 5.0)
    print(f"sanity (a): min eig L(Gamma) = {lmin:+.4f}, overlap = {overlap:.6f}"
          f"  -> {'PASS' if gate_a else 'FAIL'}")
    print(f"sanity (b): Gamma omegas {np.round(wG[:5], 3)}"
          f"  -> {'PASS (3 Goldstones)' if gate_b else 'FAIL'}")

    ss, bands = band_line(bdg, cell)
    gaps = core.gaps_from_bands(bands)
    # acoustic/density channel is gapless from 0 up to the first stop band edge
    acoustic_max = float(gaps[0][0]) if gaps else float(max(b[-1] for b in bands))
    lowest_band_max = float(max(b[0] for b in bands))
    print(f"density channel gapless 0 -> {acoustic_max:.3f} (first gap edge); "
          f"lowest-band max {lowest_band_max:.3f}")
    print("normal-incidence stop bands:", [(round(l, 3), round(h, 3)) for l, h in gaps])

    # cutoff check n=40 at 21 points
    bdg40 = core.BdG(cell, psi0, mu, 40)
    ss40 = np.linspace(0.0, 1.0, 21)
    My = cell.b2 / 2.0
    bands40 = [bdg40.omegas(s * My, NBANDS) for s in ss40]
    gaps40 = core.gaps_from_bands(bands40)
    shifts = []
    for (l1, h1), (l2, h2) in zip(gaps[:len(gaps40)], gaps40):
        shifts += [abs(l2 - l1) / l1, abs(h2 - h1) / h1]
    max_shift = float(max(shifts)) if shifts else float("nan")
    gate_c = max_shift <= 0.005
    print(f"sanity (c): max gap-edge shift n32->n40 = {100*max_shift:.3f}%"
          f"  -> {'PASS' if gate_c else 'FAIL'}")

    out = dict(sanity=dict(L_gamma_min_eig=round(lmin, 4),
                           psi0_overlap=round(overlap, 6),
                           gamma_omegas=[round(float(w), 4) for w in wG[:6]],
                           gate_a=bool(gate_a), gate_b=bool(gate_b),
                           gate_c=bool(gate_c),
                           cutoff_max_shift=round(max_shift, 5)),
               acoustic_max=round(acoustic_max, 3),
               gaps=[[round(l, 3), round(h, 3)] for l, h in gaps],
               gaps_n40=[[round(l, 3), round(h, 3)] for l, h in gaps40],
               s_line=[round(float(s), 4) for s in ss],
               bands=[[round(float(w), 4) for w in b] for b in bands])
    with open("phase3a_line.json", "w") as f:
        json.dump(out, f, indent=1)
    print("phase3a_line.json written")


if __name__ == "__main__":
    main()
