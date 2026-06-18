"""
build_cache.py — GZ1 Phase 4a (REBUILD): relax the 16-row strip, cache state
Strip: Lx = a*, Ly = 16*d_row (8 rectangular cells), periodic both directions
(report §4). Relaxes the strip crystal and caches psi0/V/mu for solve_one.py.
-> strip_cache.npz
"""
import json
import numpy as np
import gz1_core as core


def main():
    with open("phase2.json") as f:
        ph2 = json.load(f)
    a_star = ph2["a_star"]
    strip = core.Strip(a_star, Nx=24, Ny=192, nrows=16)
    psi0, mu, res = strip.relax(steps=8000)
    print(f"strip relax: mu = {mu:.3f} (cell mu = {ph2['mu_polished']}),"
          f" residual = {res:.2e}")
    np.savez("strip_cache.npz", psi0=psi0, mu=mu, residual=res, a_star=a_star)
    print("strip_cache.npz written")


if __name__ == "__main__":
    main()
