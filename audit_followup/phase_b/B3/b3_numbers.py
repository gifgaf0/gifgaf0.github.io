#!/usr/bin/env python3
"""B3 numbers: the calculators' formulas against PDG 2024 (inputs as cited in B3_RESULT.md)."""
import json, math
phi = (1 + 5 ** 0.5) / 2
PHI = 2 * math.pi - phi ** 2 / (8 * math.pi ** 2)
m0 = 0.511 / math.exp(2 * math.pi / PHI)
xi = 100 * phi
def r_eff(L): return 1 + math.log(1 + L / xi)
def mass(A, Zf, L): return m0 * (A / Zf) * (math.exp(L / (PHI * r_eff(L))) if L else 1.0)
out = {"PHI": PHI, "m0": m0}
# electroweak
mW = m0 * phi ** 27
s2 = phi ** -3
mZ = mW / math.sqrt(1 - s2)
W24, sW24 = 80369.2, 13.3          # PDG 2024 average (particle listing)
W24n, sW24n = 80360.0, 12.0        # PDG 2024 EW review Eq. 10.63 (excluding CDF)
Z24, sZ24 = 91188.0, 2.0
s2_MSbar, ss2_MSbar = 0.23129, 0.00004
s2_OS, ss2_OS = 0.22348, 0.00010
s2_eff, ss2_eff = 0.23161, 0.00004
s2_0, ss2_0 = 0.23873, 0.00005
ew = {
 "mW_pred": mW, "mW_vs_PDG2024_pct": 100*(mW-W24)/W24, "mW_pull": (mW-W24)/sW24,
 "mW_vs_noCDF_pct": 100*(mW-W24n)/W24n, "mW_pull_noCDF": (mW-W24n)/sW24n,
 "sin2_pred": s2,
 "sin2_vs_MSbar_MZ_pct": 100*(s2-s2_MSbar)/s2_MSbar, "sin2_pull_MSbar": (s2-s2_MSbar)/ss2_MSbar,
 "sin2_vs_onshell_pct": 100*(s2-s2_OS)/s2_OS, "sin2_pull_onshell": (s2-s2_OS)/ss2_OS,
 "sin2_vs_eff_pct": 100*(s2-s2_eff)/s2_eff,
 "sin2_vs_Q0_pct": 100*(s2-s2_0)/s2_0,
 "mZ_pred": mZ, "mZ_vs_PDG2024_pct": 100*(mZ-Z24)/Z24, "mZ_pull": (mZ-Z24)/sZ24,
}
out["electroweak"] = ew
# mass table rows (calculator inputs) against PDG 2024
rows = {
 "e":   (1, 1, 2*math.pi, 0.51099895, None),
 "u":   (3, 3, 16.372, 2.16, 0.07),
 "d":   (11, 9, 21.04, 4.70, 0.07),
 "mu":  (1, 1/(2*math.pi), 2*PHI*phi**2, 105.6583755, None),
 "s":   (107, 12, 29.13, 93.5, 0.8),
 "c":   (5, 1/48, 23.60, 1273.0, 4.6),
 "tau": (3, 1/(2*math.pi), 3*PHI*phi**2, 1776.93, 0.09),
 "b":   (119, 0.75, 37.31, 4183.0, 7.0),
 "t":   (119, 1/(8*phi**4), 37.31, 172570.0, 290.0),
}
tab = {}
for k, (A, Zf, L, obs, s) in rows.items():
    p = mass(A, Zf, L)
    tab[k] = {"pred": round(p, 6), "pdg2024": obs, "pct": round(100*(p-obs)/obs, 3), "pull": (round((p-obs)/s, 1) if s else None)}
out["mass_rows"] = tab
# proton
def solve(m_target, A=20, Zf=6):
    lo, hi = 1.0, 200.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if mass(A, Zf, mid) < m_target else (lo, mid)
    return (lo + hi) / 2
out["proton"] = {"L_B_inverted": solve(938.272), "m_p_at_58_006": mass(20, 6, 58.006),
                 "m_p_at_58_0526": mass(20, 6, 48*math.atan(7**0.5)),
                 "pct_at_58_006": 100*(mass(20, 6, 58.006)-938.272)/938.272,
                 "m_p_A70_at_58_006": mass(70, 6, 58.006)}
for k, v in ew.items():
    print(f"{k:24s} {v:.6g}")
for k, v in tab.items():
    print(f"{k:4s} pred {v['pred']:.6g}  PDG2024 {v['pdg2024']}  {v['pct']:+.3f}%  pull {v['pull']}")
print({k: round(v, 4) for k, v in out["proton"].items()})
json.dump(out, open("b3_numbers.json", "w"), indent=1)
