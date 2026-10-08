#!/usr/bin/env python3
"""ls_compare.py -- the comparison, run last (LS_PREREG.md §8, §9).

Reads ls_leg1.json only. Evaluates, per arm and for the combined bound:
EMPTY_P(N) <=> a_max(N) < l_P; EMPTY_D(N) <=> a_max(N) < 1.899e-34 m (the declared band's
lower edge); N_P = d/l_P; N_D = d/1.899e-34 m; the declared band [1.899, 7.588]e-34 m
against a_max(N); the same for the R4 x10 variant; and the second-leg trigger.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEG1 = os.path.join(HERE, "ls_leg1.json")
LEG1_MD5 = "9fd7a9ea0b1a0027b036d4e30d511068"
got = hashlib.md5(open(LEG1, "rb").read()).hexdigest()
if got != LEG1_MD5:
    sys.exit("HALT: ls_leg1.json md5 %s != %s" % (got, LEG1_MD5))
L = json.load(open(LEG1))

LP = L["constants"]["l_P"]
BAND = (1.899e-34, 7.588e-34)
NS = [20, 100, 1000]


def assess(d):
    row = {"d_max_m": d, "N_P": d / LP, "N_D": d / BAND[0], "N_band_hi": d / BAND[1], "per_N": {}}
    for N in NS:
        a = d / N
        row["per_N"][str(N)] = {"a_max_m": a, "a_max_lP": a / LP,
                                "EMPTY_P": a < LP, "EMPTY_D": a < BAND[0],
                                "lP_over_a_max": LP / a, "band_lo_over_a_max": BAND[0] / a}
    return row


res = {"leg1_md5": LEG1_MD5, "l_P": LP, "band_m": BAND, "arms": {}}
for a, v in L["arms"].items():
    res["arms"][a] = assess(v["record_union"])
    res["arms"][a]["reference_reading"] = assess(v["reference_union"])
d_comb = L["combined"]["d_comb"]
res["combined"] = assess(d_comb)
res["combined"]["decisive_arm"] = L["combined"]["decisive_arm"]
res["combined_R4x10"] = assess(L["combined"]["R4_x10"])
# with the dispersion bound folded in (it is N-independent and far looser; checked, not assumed)
disp = L["dispersion"]["record"]["m"]
res["dispersion_record_m"] = disp
res["dispersion_EMPTY_P"] = disp < LP
res["dispersion_EMPTY_D"] = disp < BAND[0]
for N in NS:
    assert L["combined_a_max"][str(N)]["a_max_m"] == min(d_comb / N, disp)
    assert L["combined_a_max"][str(N)]["binding"] == "attenuation"

c20 = res["combined"]["per_N"]["20"]
res["second_leg_trigger"] = {"EMPTY_P_at_20": c20["EMPTY_P"], "EMPTY_D_at_20": c20["EMPTY_D"],
                             "fires": c20["EMPTY_P"] or c20["EMPTY_D"],
                             "literal_every_arm_every_N_ge_20_P": all(res["arms"][a]["per_N"]["20"]["EMPTY_P"] for a in res["arms"]),
                             "literal_every_arm_every_N_ge_20_D": all(res["arms"][a]["per_N"]["20"]["EMPTY_D"] for a in res["arms"])}
# where l_P falls: the largest N at a = l_P on each arm, and the a at which N cells fit
with open(os.path.join(HERE, "ls_compare.json"), "w") as f:
    json.dump(res, f, indent=1, sort_keys=True)

P = print
P("LS comparison (leg-1 json %s)" % LEG1_MD5)
P("declared band [%.3e, %.3e] m = [%.2f, %.2f] l_P" % (BAND[0], BAND[1], BAND[0] / LP, BAND[1] / LP))
P("%-10s %-12s %-9s %-9s | " % ("arm", "d_max (m)", "N_P", "N_D") +
  " | ".join("N=%d: a_max/l_P  EMPTY_P EMPTY_D" % N for N in NS))
rows = list(res["arms"].items()) + [("combined", res["combined"]), ("comb R4x10", res["combined_R4x10"])]
for a, r in rows:
    P("%-10s %-12.4e %-9.3f %-9.4f | " % (a, r["d_max_m"], r["N_P"], r["N_D"]) +
      " | ".join("%.4e %s %s" % (r["per_N"][str(N)]["a_max_lP"], r["per_N"][str(N)]["EMPTY_P"], r["per_N"][str(N)]["EMPTY_D"]) for N in NS))
P("reference readings (E_ref, D_ref):")
for a in res["arms"]:
    r = res["arms"][a]["reference_reading"]
    P("  %-4s d %.4e m  N_P %.3f  N_D %.4f" % (a, r["d_max_m"], r["N_P"], r["N_D"]))
P("dispersion bound %.4e m: EMPTY_P %s, EMPTY_D %s (not binding at any N)" % (disp, res["dispersion_EMPTY_P"], res["dispersion_EMPTY_D"]))
P("second-leg trigger: %s" % json.dumps(res["second_leg_trigger"]))
