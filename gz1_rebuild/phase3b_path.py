"""
phase3b_path.py — GZ1 Phase 3b (REBUILD): Gamma–M–K–Gamma path
Target (report §3): gaps A and B persist over the sampled 2D path; A2 is
normal-incidence only. -> phase3b.json
"""
import json
import numpy as np
import gz1_core as core

NBANDS = 24


def main():
    with open("phase2.json") as f:
        ph2 = json.load(f)
    with open("phase3a_line.json") as f:
        ph3a = json.load(f)
    a_star, mu = ph2["a_star"], ph2["mu_polished"]
    psi0 = np.load("psi0_polished_n64.npy")
    cell = core.Cell(a_star, psi0.shape[0])
    bdg = core.BdG(cell, psi0, mu, 32)

    M = cell.b2 / 2.0
    K = (cell.b1 + 2.0 * cell.b2) / 3.0
    seg = lambda p, q, n: [p + (q - p) * t for t in np.linspace(0, 1, n, endpoint=False)]
    kpath = seg(np.zeros(2), M, 16) + seg(M, K, 10) + seg(K, np.zeros(2), 16) \
        + [np.zeros(2)]
    bands = [bdg.omegas(k, NBANDS) for k in kpath]

    gaps_line = {name: tuple(g) for name, g in
                 zip(["A", "A2", "B"], ph3a["gaps"][:3])} if len(ph3a["gaps"]) >= 3 \
        else {}
    persistence = {}
    for name, (lo, hi) in gaps_line.items():
        # does any band sample fall strictly inside (lo, hi) anywhere on the path?
        inside = any(bool(np.any((b > lo + 1e-6) & (b < hi - 1e-6))) for b in bands)
        persistence[name] = "persists over path" if not inside \
            else "normal-incidence only (filled on path)"
        print(f"gap {name} ({lo:.3f},{hi:.3f}): {persistence[name]}")

    out = dict(gaps_line=ph3a["gaps"],
               persistence=persistence,
               bands=[[round(float(w), 4) for w in b] for b in bands])
    with open("phase3b.json", "w") as f:
        json.dump(out, f, indent=1)
    print("phase3b.json written")


if __name__ == "__main__":
    main()
