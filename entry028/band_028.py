"""band_028.py -- Entry 028 band definition and quadrature (shared by every prediction script).
Band [1.05e12, 2.05e12), M = 2000 strata of width 5e8; stratum r starts at s_r = y_r + U, U uniform on
[0, 1.0e8); a run is n + 1 = 12,500,001 kept consecutive primes (n = 1.25e7 lag-1 pairs).  The mean run
midpoint of stratum r is y_r + 5e7 + 0.5*n*log(y) ~ y_r + 2.24e8.
The model is evaluated at 4 Gauss-Legendre nodes fixed on [NODE_LO, NODE_HI] = [1.050215e12, 2.049715e12]
(placed for the first draft, n = 1e7; kept unchanged) and averaged with exact discrete stratum weights
computed from strata_mid() (make_pred_028.py), so the node placement does not affect the prediction
beyond the cubic interpolation (validated on c_216 to 1e-13).
c_hat is the unweighted mean over strata, so the prediction is the uniform-in-y average of the local
correlation over that range: Gauss-Legendre in log y with dy weight (Entry 026's random-arm convention)."""
import math, numpy as np
Y0, W, M = 1.05e12, 5e8, 2000
LO, HI = 1.050215e12, 2.049715e12          # NODE_LO, NODE_HI (node placement only)
NPER, OFFSET = 12_500_000, 100_000_000
def strata_mid(exact=True):
    y = Y0 + W * np.arange(M)
    return y + OFFSET / 2 + (0.5 * NPER * np.log(y + 2.24e8) if exact else 1.74e8)
def nodes(n=4, lo=LO, hi=HI):
    u, w = np.polynomial.legendre.leggauss(n)
    a, b = math.log(lo), math.log(hi)
    us = (b - a) / 2 * u + (a + b) / 2
    ws = w * np.exp(us); ws = ws / ws.sum()
    return [math.exp(x) for x in us], [float(x) for x in ws]
