#!/usr/bin/env python3
# g_2a_L1_reemit_cc_v1_1.py — S9 resolution run-2: re-emit the CC checkpoint
# under schema v1.1 (representation only; per the S9 mini-dispatch and
# activation_S9_G_2a_L1.json: RECOMPUTE=false, instrument c3bea9ee untouched).
# Every value is carried from the committed v1.0 checkpoint 47ae0b85; the two
# new C4 fields restate facts the v1.0 instrument run already asserted:
#   _PGL = 6  : "F2: unique size-6 order-2 class (transpositions)" (PGL(2,3))
#   _GL  = 12 : "F2: the involution preimages form one GL(2,3) class of size 12"
import json, hashlib

V1 = "g_2a_L1_cc_checkpoint.json"
parent_md5 = hashlib.md5(open(V1, "rb").read()).hexdigest()
assert parent_md5 == "47ae0b85eee85781cddc93cb208441a7", "v1.0 parent mismatch"
ck = json.load(open(V1, encoding="utf-8"))

ck["schema"] = "g2a_l1_checkpoint_v1_1"
# H-S4: declared as the SET of element orders of M+ (the per-class multiset
# [1,2,2,3,4] of v1.0 carries the same machine facts; class sizes unchanged)
ck["C2_M"]["Mplus_element_orders"] = sorted(set(ck["C2_M"]["Mplus_element_orders"]))
# H-S6: level-ambiguous field retired; both levels emitted, both from the
# v1.0 instrument's own assertions
del ck["C4_F2"]["GL23_transposition_class_size"]
ck["C4_F2"]["GL23_transposition_class_size_PGL"] = 6
ck["C4_F2"]["GL23_transposition_class_size_GL"] = 12
# arms unchanged (prereg §8); arm_sharpened unchanged (v1.1 reports, never compares)
ck["reemission"] = {
    "from_v1_checkpoint_md5": parent_md5,
    "instrument_unchanged": True,
    "changes": [
        "schema string",
        "Mplus_element_orders declared as SET (v1.0 per-class multiset [1,2,2,3,4] -> set; same verified facts, class sizes untouched)",
        "GL23_transposition_class_size (GL-level 12) split into _PGL=6 and _GL=12, both asserted by the v1.0 instrument run (unique size-6 order-2 PGL class; single size-12 GL involution class)",
    ],
    "note": "no value recomputed; arms and arm_sharpened byte-identical to v1.0",
}
out = "g_2a_L1_cc_checkpoint_v1_1.json"
with open(out, "w") as f:
    json.dump(ck, f, indent=1, sort_keys=True)
    f.write("\n")
print("re-emitted %s md5 %s (%d B) from parent %s"
      % (out, hashlib.md5(open(out, "rb").read()).hexdigest(),
         len(open(out, "rb").read()), parent_md5))
