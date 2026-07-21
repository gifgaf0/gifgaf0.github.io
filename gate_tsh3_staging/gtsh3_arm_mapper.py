"""G-TSH3 quarantined arm mapper. Written LAST, after all measurement phases.
First and only appearance of the thresholds theta1/theta2 anywhere in the leg.
Runs its own T1 self-grep in-invocation (TSH2 H-2 lesson).
Frozen anchors: copied verbatim from SQT_Master_Ledger_v4_69 section 2.91.J
(P_X 8-point set; D_X = 7.007%, mean 0.51392 reproduced below as a self-check).
Arm map per locked staging memo dab46b332b83997d34f9e4ca64c07a4d, section 7,
restated roles; BOUNDARY window per AUTH-INST-1.
"""
import json

FORBIDDEN = ("GW170817", "phys" + "ical c", "speed of " + "light",
             "2998" + "e5", "1370" + "36")
def t1():
    src = open(__file__, encoding="utf-8").read()
    tail = src.split("def t1", 1)[1]
    hits = [f for f in FORBIDDEN if f in tail]
    assert not hits, f"T1 mapper self-grep hit: {hits}"
    print("[T1-mapper] self-grep clean")
t1()

TH1, TH2 = 3.0, 10.0            # percent; only appearance in the leg
BOUNDARY = (9.0, 11.0)          # AUTH-INST-1 return-to-author window

FROZEN = {  # name: (RT, family)   -- read-only, ledger 2.91.I/J
    "step_g22": (0.5228, "SS"), "step_g30": (0.5286, "SS"),
    "step_g37": (0.5348, "SS"), "step_g44": (0.5436, "SS"),
    "gamma6":   (0.4988, "SS"), "gamma8":   (0.47791, "SS"),
    "gamma12":  (0.48861, "SS"), "cap_p1":  (0.51622, "CAP"),
}
NEW_FAMILY = {"gem3": "GEM", "gem4": "GEM", "gem8": "GEM", "cap_p2": "CAP"}

def dmax(vals):
    m = sum(vals)/len(vals)
    return 100.0*max(abs(v-m) for v in vals)/m, m

dx, mx = dmax([v for v, _ in FROZEN.values()])
assert abs(dx - 7.007) < 0.02 and abs(mx - 0.51392) < 5e-5, (dx, mx)
print(f"[mapper] frozen-set self-check: D_X={dx:.3f}% mean={mx:.5f} (ledger 7.007/0.51392)")

d = json.load(open("/home/claude/gtsh3_results.json"))
newpts, excl = {}, []
for k in ("gem8", "gem4", "gem3", "cap_p2"):
    p = d[f"P2_{k}"]
    if p["status"] == "CERTIFIED":
        newpts[k] = p["RT"]
    else:
        excl.append((k, p["notes"]))
ncert = len(newpts)
assert len(excl) < 2, f"two-exclusion return-to-author trigger: {excl}"

pool = {k: v for k, (v, _) in FROZEN.items()}
pool.update(newpts)
fam = {k: f for k, (_, f) in FROZEN.items()}
fam.update({k: NEW_FAMILY[k] for k in newpts})
D_ext, mean_ext = dmax(list(pool.values()))
far = max(pool, key=lambda k: abs(pool[k] - mean_ext))
dep_fam = fam[far]
fam_vals = [pool[k] for k in pool if fam[k] == dep_fam]
D_F, mean_F = dmax(fam_vals) if len(fam_vals) > 1 else (0.0, fam_vals[0])

boundary = BOUNDARY[0] <= D_ext <= BOUNDARY[1]
if ncert >= 3 and D_ext <= TH2:
    arm = "BAND"
elif D_ext > TH2 and D_F <= TH1:
    arm = "FAMILY-INDEXED"
else:
    arm = "KNOB"

wit = {}
for k in ("step", "gamma8", "gem8", "gem4", "gem3", "cap_p1", "cap_p2"):
    w = d.get(f"P3w_{k}", {})
    if w.get("reuse") or w.get("certified"):
        wit[k] = w["RT"]
D_C = dmax(list(wit.values()))[0] if len(wit) > 1 else None

out = dict(P_ext=pool, families=fam, D_ext=D_ext, mean_ext=mean_ext,
           ncert_new=ncert, exclusions=excl, farthest=far,
           departing_family=dep_fam, D_F=D_F, theta1=TH1, theta2=TH2,
           boundary_flag=boundary, arm=arm, witness_points=wit, D_C=D_C,
           witness_note=("witness sample collapsed to the step reuse point; "
                         "D_C degenerate; section-8 guide uninformative; "
                         "section-7 arm stands unqualified") if D_C is None else "")
json.dump(out, open("/home/claude/gtsh3_arm_verdict.json", "w"), indent=1)
print(f"[mapper] P_ext n={len(pool)}  mean={mean_ext:.5f}  D_ext={D_ext:.3f}%")
print(f"[mapper] farthest={far} ({pool[far]:.5f})  departing family={dep_fam}  "
      f"D_F={D_F:.3f}%  (theta1={TH1}%, theta2={TH2}%)")
print(f"[mapper] ncert_new={ncert}/4  exclusions={[e[0] for e in excl]}  boundary={boundary}")
print(f"[mapper] witness certified: {list(wit)}  D_C={D_C}")
print(f"[mapper] ARM = {arm}")
