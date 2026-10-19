"""
data_targets.py -- comparison data for E4, with sources.  Fixed before any fit was run.

NuFIT 6.0 (I. Esteban et al., arXiv:2410.05380v1, Table 1), variant "IC19 without SK atmospheric
data", normal ordering (read from the arXiv mirror PDF):
    sin^2 th12 = 0.307 +0.012 -0.011   3sigma 0.275 - 0.345
    sin^2 th23 = 0.561 +0.012 -0.015   3sigma 0.430 - 0.596
    sin^2 th13 = 0.02195 +0.00054 -0.00058   3sigma 0.02023 - 0.02376
    delta_CP   = 177 +19 -20 deg       3sigma 96 - 422 deg
    Dm21^2     = 7.49 +-0.19 e-5 eV^2
    Dm31^2     = +2.534 +0.025 -0.023 e-3 eV^2
  => r = Dm31^2/Dm21^2 = 33.83 +- 0.92 (1sigma errors in quadrature).
  Error convention for chi^2 (stated before fitting): for the angles and delta, one-sided sigma =
  (3sigma edge - best fit)/3 on each side.  This reproduces the 1sigma errors for th12 and th13
  and is deliberately looser for th23 (octant degeneracy: the lower 3sigma edge is 0.430) and
  delta.  r uses its Gaussian 1sigma.
  delta is periodic: its pull uses the representative delta + 360k with the smallest |pull|
  (reconciliation fix of the original [-3, 357) deg wrap; see pull_delta_deg).

UTfit 2022 (M. Bona et al., arXiv:2212.03894v1, Appendix Table "Full Fit"):
    lambda = 0.22519 +- 0.00083,  A = 0.828 +- 0.011,  rhobar = 0.1609 +- 0.0095,  etabar = 0.347 +- 0.010

Running masses at mu = M_Z, full SM (G.-y. Huang & S. Zhou, arXiv:2009.04851v2, Tables 2 and 3):
    mt 168.26(75) GeV, mb 2.839(26) GeV, mc 0.620(17) GeV, ms 53.16(4.61) MeV, md 2.67(19) MeV,
    mu 1.23(21) MeV;  mtau 1.72856 GeV, mmu 0.101766 GeV, me 0.48307 MeV.
  Mass ratios are fitted in log space with relative error max(propagated experimental, 10%).
  The 10% floor (stated before fitting) covers the scale ambiguity: quark ratios change by up to
  ~10% between M_Z and 10^12 GeV in the same tables (e.g. mc/mt 3.68e-3 -> 3.33e-3).
"""
import math

import numpy as np

from e4lib import angles_from_U, wolfenstein_from_V

NUFIT = {
    "source": "NuFIT 6.0, arXiv:2410.05380v1 Table 1, IC19 w/o SK-atm, normal ordering",
    "s12sq": (0.307, 0.307 - 0.275, 0.345 - 0.307),
    "s13sq": (0.02195, 0.02195 - 0.02023, 0.02376 - 0.02195),
    "s23sq": (0.561, 0.561 - 0.430, 0.596 - 0.561),
    "delta_deg": (177.0, 177.0 - 96.0, 422.0 - 177.0),
    "dm21sq": (7.49e-5, 0.19e-5),
    "dm31sq": (2.534e-3, 0.024e-3),
}
NUFIT_1SIGMA = {"s12sq": (0.011, 0.012), "s13sq": (0.00058, 0.00054), "s23sq": (0.015, 0.012),
                "delta_deg": (20.0, 19.0)}
R_ATM_SOL = NUFIT["dm31sq"][0] / NUFIT["dm21sq"][0]
R_ATM_SOL_ERR = R_ATM_SOL * math.hypot(NUFIT["dm21sq"][1] / NUFIT["dm21sq"][0],
                                       NUFIT["dm31sq"][1] / NUFIT["dm31sq"][0])
for k in ("s12sq", "s13sq", "s23sq", "delta_deg"):
    bf, lo, hi = NUFIT[k]
    NUFIT[k] = (bf, lo / 3, hi / 3)          # one-sided sigmas from the 3sigma range

UTFIT = {"source": "UTfit 2022, arXiv:2212.03894v1 Appendix (Full Fit)",
         "lambda": (0.22519, 0.00083), "A": (0.828, 0.011), "rhobar": (0.1609, 0.0095), "etabar": (0.347, 0.010)}

MZ = {"source": "Huang & Zhou arXiv:2009.04851v2 Tables 2-3, mu = M_Z, full SM",
      "mt": (168.26, 0.75), "mb": (2.839, 0.026), "mc": (0.620, 0.017), "ms": (53.16e-3, 4.61e-3),
      "md": (2.67e-3, 0.19e-3), "mu": (1.23e-3, 0.21e-3),
      "mtau": (1.72856, 0.00028), "mmu": (0.101766, 0.000023), "me": (0.48307e-3, 0.00045e-3)}
FLOOR = 0.10


def _ratio(a, b):
    va, ea = MZ[a]
    vb, eb = MZ[b]
    v = va / vb
    rel = math.hypot(ea / va, eb / vb)
    return v, max(rel, FLOOR)


RATIOS = {"me/mmu": _ratio("me", "mmu"), "mmu/mtau": _ratio("mmu", "mtau"),
          "mu/mc": _ratio("mu", "mc"), "mc/mt": _ratio("mc", "mt"),
          "md/ms": _ratio("md", "ms"), "ms/mb": _ratio("ms", "mb")}


def pull_asym(x, key, table=NUFIT):
    bf, lo, hi = table[key]
    d = x - bf
    return d / (hi if d > 0 else lo)


def pull_delta_deg(delta_deg):
    """One-sided pull of delta (deg).  delta is periodic, so the representative delta + 360 k with the
    smallest |pull| is used.  Reconciliation fix: the original wrapped delta into [bf-180, bf+180) =
    [-3, 357) deg, which is inconsistent with NuFIT's asymmetric 3sigma range 96..422 deg (delta = 0 =
    360 deg got pull -6.56 instead of +2.24, and chi2 jumped at delta = 357 deg).  With the one-sided
    sigmas (81.7 deg above, 27 deg below) the two branches cross at delta = 87.5 deg, inside the
    excluded window 62..96 deg."""
    bf, lo, hi = NUFIT["delta_deg"]
    d0 = (delta_deg - bf) % 360.0                   # in [0, 360)
    p_up, p_dn = d0 / hi, (d0 - 360.0) / lo
    return p_up if abs(p_up) <= abs(p_dn) else p_dn


def pull_delta_wrap_v1(delta_rad):
    """The original (pre-reconciliation) convention, kept only to reproduce old numbers."""
    bf, lo, hi = NUFIT["delta_deg"]
    d = (math.degrees(delta_rad) - bf + 180.0) % 360.0 - 180.0
    return d / (hi if d > 0 else lo)


def pull_delta(delta_rad):
    if delta_rad is None or not np.isfinite(delta_rad):
        return 0.0
    return pull_delta_deg(math.degrees(delta_rad))


def chi2_pmns(U, include_delta=True):
    s12sq, s13sq, s23sq, delta, J = angles_from_U(U)
    p = {"s12sq": pull_asym(s12sq, "s12sq"), "s13sq": pull_asym(s13sq, "s13sq"),
         "s23sq": pull_asym(s23sq, "s23sq")}
    if include_delta:
        p["delta"] = pull_delta(delta)
    c2 = sum(v * v for v in p.values())
    det = {"s12sq": float(s12sq), "s13sq": float(s13sq), "s23sq": float(s23sq),
           "delta_deg": float(math.degrees(delta)) if np.isfinite(delta) else float("nan"),
           "J": float(J), "pulls": {k: float(v) for k, v in p.items()}}
    return c2, det


def chi2_ckm(V):
    lam, A, rb, eb = wolfenstein_from_V(V)
    vals = {"lambda": lam, "A": A, "rhobar": rb, "etabar": eb}
    p = {}
    for k, v in vals.items():
        if not np.isfinite(v):
            p[k] = 1e3
        else:
            p[k] = (v - UTFIT[k][0]) / UTFIT[k][1]
    c2 = sum(min(v * v, 1e12) for v in p.values())
    det = {k: float(v) for k, v in vals.items()}
    det["pulls"] = {k: float(v) for k, v in p.items()}
    return c2, det
