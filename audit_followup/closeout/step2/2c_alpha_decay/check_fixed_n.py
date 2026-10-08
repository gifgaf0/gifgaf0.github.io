#!/usr/bin/env python3
"""Step 2c: an independent re-computation of the fixed-N numbers the corrected paper quotes (Table 2, Section 3.3).

It shares no code with phase_b/B4/b4_checks.py. It reads the literal AME2020 mass-excess table of the store script
(phase_b/B4/source/ame2020_qvalues.py) with ast, executing nothing. It recomputes, for N > 128:
  - the step counts;
  - the Table 1 group statistics;
  - the boundary comparisons at equal N;
  - the drift of the Th→U step.
It then asserts agreement with b4_checks.json to 1e-4 MeV.
"""
import ast, json, os, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../../../phase_b/B4/source/ame2020_qvalues.py")
REF = os.path.join(HERE, "../../../phase_b/B4/b4_checks.json")
mod = ast.parse(open(SRC, encoding="utf-8").read())
tab = {}
for st in mod.body:
    if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
        if st.targets[0].id in ("ME", "ME_He4"):
            tab[st.targets[0].id] = ast.literal_eval(st.value)
me, he = tab["ME"], tab["ME_He4"]
# Q_alpha in MeV for even-even parents with Z >= 84 whose daughter is tabulated and Q > 0
Q = {}
for (z, a), m in me.items():
    if z >= 84 and z % 2 == 0 and (a - z) % 2 == 0 and (z - 2, a - 4) in me:
        val = (m - me[(z - 2, a - 4)] - he) / 1000.0
        if val > 0:
            Q[(z, a - z)] = val
step = {(z, n): Q[(z + 2, n)] - Q[(z, n)] for (z, n) in Q if (z + 2, n) in Q}
deformed = {k: v for k, v in step.items() if k[1] > 128}
res = {"Q_values": len(Q), "steps_all_N": len(step), "steps_N_gt_128": len(deformed)}
grp = {"I": [], "II": [], "III": []}
for (z, n), d in deformed.items():
    up = z + 2
    grp["I" if up <= 88 else "II" if up <= 92 else "III"].append(d)
res["table1"] = {g: (len(v), round(statistics.mean(v), 4), round(statistics.stdev(v), 4)) for g, v in grp.items()}


def compare(z_lo):
    """step leaving z_lo+2 minus step arriving at z_lo+2, at every N with both."""
    out = []
    for n in sorted({n for (_, n) in deformed}):
        if (z_lo, n) in deformed and (z_lo + 2, n) in deformed:
            a, b = deformed[(z_lo, n)], deformed[(z_lo + 2, n)]
            out.append((n, round(a, 4), round(b, 4), round(b - a, 4)))
    return out


res["Z88"] = compare(86)        # Rn→Ra vs Ra→Th
res["Z92"] = compare(90)        # Th→U vs U→Pu
res["ThU_drift"] = [(n, round(d, 4)) for (z, n), d in sorted(deformed.items(), key=lambda kv: kv[0][1]) if z == 90]
ref = json.load(open(REF, encoding="utf-8"))
assert (res["Q_values"], res["steps_all_N"], res["steps_N_gt_128"]) == (96, 74, 51) == (
    ref["Q_values"], ref["steps_all_N"], ref["steps_N_gt_128"])
for g in ("I", "II", "III"):
    n, m, sd = res["table1"][g]
    r = ref["regimes_N_gt_128"][g]
    assert n == r["n"] and abs(m - r["mean"]) < 1e-4 and abs(sd - r["sd"]) < 1e-4, g
for mine, key in ((res["Z88"], "Z88_break_same_N"), (res["Z92"], "Z92_break_same_N")):
    theirs = ref[key]["rows (N, lower, upper, diff)"]
    assert len(mine) == len(theirs)
    for a, b in zip(mine, theirs):
        assert a[0] == b[0] and all(abs(x - y) < 1e-4 for x, y in zip(a[1:], b[1:])), (a, b)
assert [(n, d) for n, d in res["ThU_drift"]] == [tuple(x) for x in ref["N_trend_within_Th_to_U"]]
# full precision, for typesetting Table 2 of the corrected paper (rounded there to 3 decimals)
res["full"] = {
    "Z88": [(n, deformed[(86, n)], deformed[(88, n)]) for (n, *_r) in res["Z88"]],
    "Z92": [(n, deformed[(90, n)], deformed[(92, n)]) for (n, *_r) in res["Z92"]],
    "N_by_regime": {g: sorted({n for (z, n) in deformed if ("I" if z + 2 <= 88 else "II" if z + 2 <= 92 else "III") == g})
                    for g in ("I", "II", "III")},
}
json.dump(res, open(os.path.join(HERE, "check_fixed_n.json"), "w"), indent=1)
print(json.dumps(res, ensure_ascii=False))
print("independent re-computation agrees with b4_checks.json: PASS")
