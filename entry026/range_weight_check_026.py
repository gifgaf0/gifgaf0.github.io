# Source of the 3e-6 gap at 1e9-2e9 (mod-4 eps, 6-node Gauss in log y): range weight with or without the
# 1/(log y)^2 factor of the pair density, both computed with the archived los216.density.
import sys, os, math, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archive')); import los216
def eps(nodes, with_L2):
    x, wt = np.polynomial.legendre.leggauss(nodes); lo, hi = math.log(1e9), math.log(2e9)
    same = tot = 0.0
    for xi, wi in zip(x, wt):
        L = 0.5 * (hi - lo) * xi + 0.5 * (hi + lo); y = math.exp(L)
        units, tab = los216.pair_density_table(4, y)
        f = 1.0 if with_L2 else L ** 2          # undo the 1/L^2 inside los216.density
        s = sum(d for (a, b), d in tab.items() if a == b) * f; t = sum(tab.values()) * f
        same += wi * y * s; tot += wi * y * t
    return (0.5 - same / tot) / 2
for n in (6, 8, 24):
    print(f"nodes {n:2d}: eps with 1/(log y)^2 (true pair density) {eps(n, True):.10f}   without (pair_absorb's range weight) {eps(n, False):.10f}")
print("predict_026 (6 nodes, with 1/L^2): 0.0227317037;  pair_absorb / archived json: 0.0227285421;  frozen Entry 024 value: 0.022729")
