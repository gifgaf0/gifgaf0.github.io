"""G-TSH3 CC leg — PART 1: independent P4 mapper (D_ext/D_F/arm) + falsifier-logic audit.
No solver machinery shared. Reproduces the KNOB verdict from the R_T pool with my own
max-from-mean, and audits the F-LIN/F-CONV/F-ISO/F-CLS gate outcomes from the stored per-kernel
exponents/metrics. (Raw ω(q) arrays are NOT in the results JSON this gate — speed reproduction is
the from-scratch solver, PART 2.)
"""
import json, numpy as np
U="/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/"
R=json.load(open(U+"10106d46-gtsh3_results.json"))
AV=json.load(open(U+"9e8fd98a-gtsh3_arm_verdict.json"))
PASS=[];
def ok(c,m):
    assert c,"FAIL: "+m
    PASS.append(m)

TH1,TH2=3.0,10.0
FROZEN={"step_g22":(0.5228,"SS"),"step_g30":(0.5286,"SS"),"step_g37":(0.5348,"SS"),
        "step_g44":(0.5436,"SS"),"gamma6":(0.4988,"SS"),"gamma8":(0.47791,"SS"),
        "gamma12":(0.48861,"SS"),"cap_p1":(0.51622,"CAP")}
NEWFAM={"gem3":"GEM","gem4":"GEM","gem8":"GEM","cap_p2":"CAP"}

# frozen-set self-check (should reproduce ledger D_X=7.007%)
def dmax(v): m=sum(v)/len(v); return 100*max(abs(x-m) for x in v)/m, m
dx,mx=dmax([v for v,_ in FROZEN.values()])
ok(abs(dx-7.007)<0.02 and abs(mx-0.51392)<5e-5, f"frozen-set self-check D_X={dx:.3f}% mean={mx:.5f} (ledger 7.007/0.51392)")

# ---- falsifier-logic audit from stored per-kernel metrics ----
for k in ("gem8","gem4","gem3","cap_p2"):
    p=R[f"P2_{k}"]
    flin=(not all(0.95<=x<=1.05 for x in p["pT"])) or (not all(0.95<=x<=1.05 for x in p["pL1"]))
    fcls=p["fT"]<0.95; fiso=p["iso_T"]>0.02 or p["iso_L"]>0.02; fconv=p["conv"]>5e-6
    should_excl=flin or fcls or fiso or fconv or p["ward"]>5e-3
    if k=="cap_p2":
        ok(not all(0.95<=x<=1.05 for x in p["pL1"]) and p["status"]=="EXCLUDED",
           f"cap_p2: F-LIN L1 fires (pL1={[round(x,3) for x in p['pL1']]}, W2<0.95) -> EXCLUDED (independent)")
    else:
        ok(p["status"]=="CERTIFIED" and not should_excl,
           f"{k}: all falsifiers clean (pT/pL1 in [0.95,1.05], conv={p['conv']:.1e}<5e-6, fT={p['fT']:.3f}) -> CERTIFIED")

# ---- independent P4 mapper ----
newpts={k:R[f"P2_{k}"]["RT"] for k in ("gem8","gem4","gem3","cap_p2") if R[f"P2_{k}"]["status"]=="CERTIFIED"}
excl=[k for k in ("gem8","gem4","gem3","cap_p2") if R[f"P2_{k}"]["status"]=="EXCLUDED"]
ok(len(excl)<2, f"exclusions={excl} (<2, below return-to-author trigger)")
pool={k:v for k,(v,_) in FROZEN.items()}; pool.update(newpts)
fam={k:f for k,(_,f) in FROZEN.items()}; fam.update({k:NEWFAM[k] for k in newpts})
D_ext,mean_ext=dmax(list(pool.values()))
far=max(pool,key=lambda k:abs(pool[k]-mean_ext)); dep=fam[far]
famvals=[pool[k] for k in pool if fam[k]==dep]; D_F,_=dmax(famvals)
ncert=len(newpts)
if ncert>=3 and D_ext<=TH2: arm="BAND"
elif D_ext>TH2 and D_F<=TH1: arm="FAMILY-INDEXED"
else: arm="KNOB"
ok(abs(D_ext-AV["D_ext"])<0.02, f"D_ext={D_ext:.3f}% matches chat {AV['D_ext']:.3f}%")
ok(far=="gem3" and dep=="GEM", f"farthest={far}, departing family={dep} (matches)")
ok(abs(D_F-AV["D_F"])<0.02, f"D_F(GEM)={D_F:.3f}% matches chat {AV['D_F']:.3f}%")
ok(arm==AV["arm"]=="KNOB", f"ARM = {arm} (D_ext>θ2 and D_F>θ1) — matches chat")
ok(not (9.0<=D_ext<=11.0), f"D_ext={D_ext:.1f}% outside BOUNDARY window [9,11]% (no return-to-author)")

# ---- ANCHOR-SYS (chat's static-chain cross-era numbers, for context; PART-2 does the real test) ----
sb=R["P0b"]["computed"]; ok(abs(sb["RT"]-0.51881)<1e-3, f"chat step@22 at locked instrument RT={sb['RT']:.5f} (frozen 0.52284, dev {abs(sb['RT']-0.52284)/0.52284*100:.2f}%)")
gb=R["P0b_prime"]["computed"]; ok(abs(gb["RT"]-0.48026)<1e-3, f"chat γ8@20 at locked instrument RT={gb['RT']:.5f} (frozen 0.47791, dev {abs(gb['RT']-0.47791)/0.47791*100:.2f}%)")

# ---- R_T monotone in GEM softness (structural R2) ----
ok(newpts["gem3"]<newpts["gem4"]<newpts["gem8"], f"R_T monotone in GEM softness: gem3 {newpts['gem3']:.5f} < gem4 {newpts['gem4']:.5f} < gem8 {newpts['gem8']:.5f}")

print(f"[PART 1] {len(PASS)} independent assertions PASSED\n")
for m in PASS: print("  ✓",m)
print(f"\n[summary] D_ext={D_ext:.3f}% D_F(GEM)={D_F:.3f}% -> ARM = {arm}; cap_p2 EXCLUDED (F-LIN L1); "
      f"ANCHOR-SYS: instrument-dependence confirmed in chat data (PART 2 reproduces independently)")
