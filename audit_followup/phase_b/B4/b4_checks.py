#!/usr/bin/env python3
"""B4: the alpha-decay paper's numbers, re-read from its own AME2020 input, and the facts the retraction check needs.

Input: source/ame2020_qvalues.py (the project-store analysis script, md5 25ddfab78ff7348bffcbaef5c40fcdee); only its
literal mass-excess table ME and the 4He mass excess are read (via ast, nothing is executed).
Everything here is descriptive arithmetic on the paper's own data. No number here decides a verdict: the ledger
already records the three-regime finding as reduced on audit to one break (Preamble, M.CW instances, §3.A.3).
"""
import ast, json, math, statistics
from collections import defaultdict

src = open("source/ame2020_qvalues.py", encoding="utf-8").read()
tree = ast.parse(src)
ME, ME_He4 = None, None
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id == "ME":
            ME = ast.literal_eval(node.value)
        elif node.targets[0].id == "ME_He4":
            ME_He4 = ast.literal_eval(node.value)
assert ME and ME_He4
out = {}

# (1) Q_alpha of the lead isotopes: alpha decay is already exothermic at and below Pb-208
q = lambda Z, A: ME[(Z, A)] - ME[(Z - 2, A - 4)] - ME_He4      # keV
out["Q_alpha_keV"] = {f"Pb-{A}": round(q(82, A), 1) for A in (204, 206, 208)}

# (2) the step sample: all N vs N > 128 (the paper says 74 steps for N > 128)
qv = {}
for (Z, A) in ME:
    if Z >= 84 and Z % 2 == 0 and (A - Z) % 2 == 0 and (Z - 2, A - 4) in ME:
        Q = q(Z, A) / 1000
        if Q > 0:
            qv[(Z, A - Z)] = Q
byN = defaultdict(dict)
for (Z, N), Q in qv.items():
    byN[N][Z] = Q
steps = []                                                      # (N, U1, U2, dQ)
for N, zq in byN.items():
    for Z in zq:
        if Z + 2 in zq:
            steps.append((N, Z - 80, Z - 78, zq[Z + 2] - zq[Z]))
out["Q_values"] = len(qv)
out["steps_all_N"] = len(steps)
deformed = [s for s in steps if s[0] > 128]
out["steps_N_gt_128"] = len(deformed)

def regime(U2):
    return "I" if U2 <= 8 else ("II" if U2 <= 12 else "III")
def stats(vals):
    return {"n": len(vals), "mean": round(statistics.mean(vals), 4), "sd": round(statistics.stdev(vals), 4)}
for label, sample in (("all_N", steps), ("N_gt_128", deformed)):
    groups = defaultdict(list)
    for N, U1, U2, d in sample:
        groups[regime(U2)].append(d)
    out[f"regimes_{label}"] = {r: stats(groups[r]) for r in ("I", "II", "III")}

# (3) the paper's Welch t values from its own Table 1 (arithmetic check)
def welch(m1, s1, n1, m2, s2, n2):
    return (m2 - m1) / math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
out["welch_t_from_table1"] = {"I_vs_II": round(welch(0.308, 0.059, 7, 0.599, 0.179, 14), 2),
                              "II_vs_III": round(welch(0.599, 0.179, 14, 1.007, 0.302, 30), 2)}

# (4) the N composition of each regime, and the boundary steps compared at the same N (descriptive only)
out["N_range_by_regime_N_gt_128"] = {r: sorted({N for N, U1, U2, d in deformed if regime(U2) == r}) for r in ("I", "II", "III")}
def at_same_N(lo, hi):
    """dQ(hi boundary) - dQ(lo boundary) for every N that has both steps; boundaries named by U1."""
    rows = []
    for N in sorted(byN):
        if N <= 128:
            continue
        d = {U1: dq for (n, U1, U2, dq) in deformed if n == N}
        if lo in d and hi in d:
            rows.append((N, round(d[lo], 4), round(d[hi], 4), round(d[hi] - d[lo], 4)))
    return rows
out["Z88_break_same_N"] = {"steps": "Rn->Ra (U 6->8) vs Ra->Th (U 8->10)", "rows (N, lower, upper, diff)": at_same_N(6, 8)}
out["Z92_break_same_N"] = {"steps": "Th->U (U 10->12) vs U->Pu (U 12->14)", "rows (N, lower, upper, diff)": at_same_N(10, 12)}
out["N_trend_within_Th_to_U"] = [(N, round(d, 4)) for (N, U1, U2, d) in sorted(deformed) if U1 == 10]

# (5) the Cm test (paper §4.6)
for name, U1 in (("Pu->Cm", 14), ("Cm->Cf", 16)):
    vals = [d for (N, u1, u2, d) in deformed if u1 == U1]
    out[f"Cm_test_{name}"] = stats(vals)

# (6) the U -> theta map of paper §4.5: U = 2, 8, 12 at theta = 0, pi/8, pi/4
out["U_steps_per_pi_over_8"] = {"0 -> pi/8": 8 - 2, "pi/8 -> pi/4": 12 - 8}

json.dump(out, open("b4_checks.json", "w"), indent=1)
for k, v in out.items():
    print(f"{k}: {v}")
