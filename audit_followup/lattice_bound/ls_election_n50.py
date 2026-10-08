#!/usr/bin/env python3
"""ls_election_n50.py -- consequences of the author's floor election N = 50 (October 7, 2026, 19:16 PDT).

Arithmetic on the two-leg numbers only (no new derivation): a_max(50) = d_max/50 on every arm and for the
combined bound, from BOTH legs' d_max values (agreement asserted); the EMPTY flags at N = 50 under the
pre-registered definitions (LS_PREREG §8); the declared chain's window (50·a_phys, d_max] per arm.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PINS = {"ls_leg1.json": "9fd7a9ea0b1a0027b036d4e30d511068",
        "leg2/ls_leg2.json": "1880f014d2fd00b468aa6af3a9ce9e8d",
        "ls_compare.json": "a672887a43e912ef1d77d00dc5a83d5a"}
for fn, want in PINS.items():
    got = hashlib.md5(open(os.path.join(HERE, fn), "rb").read()).hexdigest()
    if got != want:
        sys.exit("HALT: %s md5 %s != %s" % (fn, got, want))
L1 = json.load(open(os.path.join(HERE, "ls_leg1.json")))
L2 = json.load(open(os.path.join(HERE, "leg2/ls_leg2.json")))
N = 50
LP = 1.616255e-35
BAND = (1.899e-34, 7.588e-34)
DISP = L1["dispersion"]["record"]["m"]
assert abs(DISP - L2["dispersion_m"]["6.9e11GeV|GK"]) / DISP < 1e-12

out = {"N": N, "pins": PINS, "arms": {}}
for arm in L1["arms"]:
    d1, d2 = L1["arms"][arm]["record_union"], L2["arms"][arm]["record_union"]
    assert abs(d1 - d2) / d1 < 1e-12, arm
    a = min(d1 / N, DISP)
    out["arms"][arm] = {"d_max_m": d1, "leg_rel_dev": abs(d1 - d2) / d1, "a_max_m": a, "a_max_lP": a / LP,
                        "EMPTY_P": a < LP, "EMPTY_D": a < BAND[0],
                        "declared_chain_window_empty": N * BAND[0] >= d1,
                        "N_times_band_lo_over_d": N * BAND[0] / d1}
dc1, dc2 = L1["combined"]["d_comb"], L2["combined"]["d_comb"]
assert abs(dc1 - dc2) / dc1 < 1e-12 and L1["combined"]["decisive_arm"] == L2["combined"]["decisive_arm"]
a_c = min(dc1 / N, DISP)
r4 = L1["combined"]["R4_x10"]
out["combined"] = {"d_comb_m": dc1, "decisive_arm": L1["combined"]["decisive_arm"], "a_max_m": a_c, "a_max_lP": a_c / LP,
                   "R4_x10_a_max_m": r4 / N, "R4_x10_a_max_lP": r4 / N / LP,
                   "R4_x0p1_a_max_lP": L1["combined"]["R4_x0p1"] / N / LP,
                   "EMPTY_P": a_c < LP, "EMPTY_D": a_c < BAND[0],
                   "declared_chain_window_empty_every_arm": all(v["declared_chain_window_empty"] for v in out["arms"].values()),
                   "N_band": [N * BAND[0], N * BAND[1]], "binding": "attenuation" if dc1 / N < DISP else "dispersion"}
with open(os.path.join(HERE, "ls_election_n50.json"), "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)

print("Floor election N = %d: consequences from both legs' d_max (agreement asserted to 1e-12)" % N)
for arm, v in out["arms"].items():
    print("  %s d_max %.4e m -> a_max %.4e m = %.4f l_P | EMPTY_P %s EMPTY_D %s | declared chain: 50*a_lo/d_max = %.3f -> %s" %
          (arm, v["d_max_m"], v["a_max_m"], v["a_max_lP"], v["EMPTY_P"], v["EMPTY_D"], v["N_times_band_lo_over_d"],
           "window EMPTY" if v["declared_chain_window_empty"] else "window open"))
c = out["combined"]
print("  combined (%s): a_max %.4e m = %.4f l_P (binding: %s); tau x10: %.4e m = %.4f l_P; tau x0.1: %.4f l_P" %
      (c["decisive_arm"], c["a_max_m"], c["a_max_lP"], c["binding"], c["R4_x10_a_max_m"], c["R4_x10_a_max_lP"], c["R4_x0p1_a_max_lP"]))
print("  declared chain at N = 50: 50*a_phys in [%.4e, %.4e] m; window empty on every arm: %s" %
      (c["N_band"][0], c["N_band"][1], c["declared_chain_window_empty_every_arm"]))
