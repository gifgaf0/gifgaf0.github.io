#!/usr/bin/env python3
"""Why the second leg's instrument gives c1 = 10.79 at g = 12.4 (table2_cc_rows.log) where the table has 7.36.

Plain-language summary: near the crystal's instability a gapped mode at these wavevectors carries more f-sum weight
than first sound, and the instrument's automatic labelling ("the even mode with the largest f-sum share among the
next three") picks it at the two largest wavevectors. Following first sound continuously in q instead gives
c1 = 7.35, against 7.36 in the table. Nothing else in the row is affected.

Same instrument, path and settings as table2_cc_rows.py (second_leg/cc2d.py, md5 e6da46ef; seeded continuation from
g = 13.0 at the second leg's tabulated a*). Not blind: run after the first leg's value was known.
Continuity rule (fixed before looking at the result): at the smallest wavevector the label is unambiguous (it is the
second even mode); at each larger wavevector take the even mode, other than the lowest (second sound), whose omega/q
is closest to the value at the previous wavevector. c1 is then the same least-squares slope the instrument uses."""
import sys, json, hashlib
import numpy as np
SP = "/tmp/claude-0/-home-claude-gifgaf0-github-io/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad"
sys.path.insert(0, SP)
assert hashlib.md5(open(SP + "/cc2d.py", "rb").read()).hexdigest() == "e6da46ef68bea7ede8de7dbefa0f9ada"
import cc2d as C

path = [(13.0, 1.5099592443626995), (12.9, 1.5109044165973526), (12.8, 1.5118912026209708), (12.7, 1.5129328893871443),
        (12.6, 1.5140526146768853), (12.5, 1.51529816851384), (12.45, 1.516002330056777), (12.4, 1.5168103105250197)]
seed = None
for g, a in path[:-1]:                       # the seeded continuation of table2_cc_rows.py (there 12.7 and 12.5 were
    seed = C.ground_state(C.hex_cell(a), C.Kernel("step", g), 64, 1.0, seed=seed)   # full run_point calls; the
g, a = path[-1]                                                                      # state is the same ground state)
res, st = C.run_point("step", g, a, seed=seed, N=64, stab_nq=0)
per = res["per_q_a1"]
rows, prev = [], None
for d in per:
    q = d["qabs"]
    even = [dict(m, v_over_q=m["omega"]/q) for m in d["next_even"]]
    if prev is None:
        assert d["label1_is_second_even"], "label at the smallest q is not the second even mode"
        pick = even[1]
    else:
        pick = min(even[1:], key=lambda m: abs(m["v_over_q"] - prev))
    prev = pick["v_over_q"]
    rows.append({"frac": d["frac"], "q": q, "label1_v_over_q": d["1"]["omega"]/q, "label1_F": d["1"]["F"],
                 "label1_is_second_even": d["label1_is_second_even"],
                 "continuity_v_over_q": pick["v_over_q"], "continuity_F": pick["F"],
                 "even_modes": [{"omega": m["omega"], "v_over_q": m["v_over_q"], "F": m["F"]} for m in even[:4]]})
qs = np.array([r["q"] for r in rows])
om_lab = np.array([r["label1_v_over_q"]*r["q"] for r in rows])
om_con = np.array([r["continuity_v_over_q"]*r["q"] for r in rows])
out = {"g": g, "a": a, "c1_instrument_label": float(np.sum(om_lab*qs)/np.sum(qs*qs)),
       "c1_continuity": float(np.sum(om_con*qs)/np.sum(qs*qs)), "c1_table": 7.36, "c1_first_leg_jobC": 7.357571037079829,
       "c2": res["c2"], "cT": res["cT"], "F2": res["F2"], "lowest_gapped_omega_per_q": res["lowest_gapped_omega_per_q"],
       "per_q": rows}
ref = json.load(open("table2_cc_rows.json"))["meta_g12.4"]          # same state as table2_cc_rows.py?
out["same_state_as_table2_cc_rows"] = {k: [res[k], ref[k], abs(res[k]/ref[k] - 1) < 1e-6] for k in ("c2", "cT", "F2", "c1")}
json.dump(C.jsonable(out), open("table2_cc_g124_modecheck.json", "w"), indent=1)
print("same state as table2_cc_rows.py (c2, cT, F2, c1 to 1e-6):", out["same_state_as_table2_cc_rows"])
for r in rows:
    print(f"frac {r['frac']:.3f}: label-1 v/q {r['label1_v_over_q']:.3f} (F {r['label1_F']:.4f}, second-even "
          f"{r['label1_is_second_even']}); continuity v/q {r['continuity_v_over_q']:.3f} (F {r['continuity_F']:.4f})")
print(f"c1: instrument label {out['c1_instrument_label']:.4f}; continuity {out['c1_continuity']:.4f}; "
      f"first leg {out['c1_first_leg_jobC']:.4f}; table 7.36")
print("lowest gapped omega per q:", [round(x, 3) for x in res["lowest_gapped_omega_per_q"]])
print("MODECHECK DONE")
