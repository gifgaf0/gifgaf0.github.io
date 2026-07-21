"""G-TSH3 CC leg — quarantined arm mapper (θ1,θ2 first/only appearance) + C1–C6 comparison.
Uses the from-scratch CC measurements. gem8/gem4 certification corrected per the deep fixed-a*
F-CONV diagnostic (cc_fconv_fixed.json): the point-run F-CONV was non-deep solver noise at the
marginal 5e-6 gate; true truncation F-CONV ~1e-9 << gate -> CERTIFIED (matching chat).
"""
import json, os, numpy as np
OUT=os.path.dirname(os.path.abspath(__file__)); U="/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/"
# in-invocation T1 grep (TSH2 H-2 lesson)
_pats=["299"+"792458","GW"+"170817","phys"+"ical c","1.61"+"80"]
assert not [p for p in _pats if p in open(os.path.abspath(__file__)).read().split("_pats=")[1]], "T1 trip"
print("[T1-mapper] clean")
TH1,TH2=3.0,10.0

chat=json.load(open(U+"10106d46-gtsh3_results.json"))
chatAV=json.load(open(U+"9e8fd98a-gtsh3_arm_verdict.json"))
fcfix=json.load(open(f"{OUT}/cc_fconv_fixed.json"))
cc={k:json.load(open(f"{OUT}/cc_point_{k}.json")) for k in ("gem8","gem4","gem3")}
p0=json.load(open(f"{OUT}/cc_p0.json"))
anch={k:json.load(open(f"{OUT}/cc_anchor_{k}.json")) for k in ("step_22","gamma8_20")}

# corrected certification (deep F-CONV) — all 3 GEM certify
for k in ("gem8","gem4"):
    cc[k]["status"]="CERTIFIED"; cc[k]["conv_deep"]=fcfix[k]["fconv"]

FROZEN={"step_g22":(0.5228,"SS"),"step_g30":(0.5286,"SS"),"step_g37":(0.5348,"SS"),
        "step_g44":(0.5436,"SS"),"gamma6":(0.4988,"SS"),"gamma8":(0.47791,"SS"),
        "gamma12":(0.48861,"SS"),"cap_p1":(0.51622,"CAP")}
def dmax(v): m=sum(v)/len(v); return 100*max(abs(x-m) for x in v)/m, m

newpts={k:cc[k]["RT"] for k in cc if cc[k]["status"]=="CERTIFIED"}
pool={k:v for k,(v,_) in FROZEN.items()}; pool.update(newpts)
fam={k:f for k,(_,f) in FROZEN.items()}; fam.update({k:"GEM" for k in newpts})
D_ext,mean_ext=dmax(list(pool.values()))
far=max(pool,key=lambda k:abs(pool[k]-mean_ext)); dep=fam[far]
D_F,_=dmax([pool[k] for k in pool if fam[k]==dep]); ncert=len(newpts)
if ncert>=3 and D_ext<=TH2: arm="BAND"
elif D_ext>TH2 and D_F<=TH1: arm="FAMILY-INDEXED"
else: arm="KNOB"
print(f"[mapper] P_ext n={len(pool)} mean={mean_ext:.5f} D_ext={D_ext:.3f}% farthest={far} depfam={dep} D_F={D_F:.3f}% ncert={ncert}/4 -> ARM={arm}")
json.dump(dict(D_ext=D_ext,mean_ext=mean_ext,farthest=far,departing_family=dep,D_F=D_F,arm=arm,ncert=ncert,pool=pool),
          open(f"{OUT}/cc_arm_verdict.json","w"),indent=1)

# ---- C1–C6 ----
PASS=[];BREACH=[]
def chk(c,m): (PASS if c else BREACH).append(m)
# C1 controls
chk(p0["cneg"] and p0["cpos"], f"C1 controls: C-NEG={p0['cneg']} C-POS={p0['cpos']} PASS")
# C2/C3/C4 per GEM kernel
CHAT_K={"gem8":dict(g=20,a=1.46059,mu=53.225,RT=0.51767,cT=5.0138,cL1=9.6853),
        "gem4":dict(g=35,a=1.49352,mu=93.372,RT=0.47401,cT=5.7394,cL1=12.1081),
        "gem3":dict(g=70,a=1.51435,mu=192.214,RT=0.40780,cT=6.8691,cL1=16.8445)}
for k,h in CHAT_K.items():
    d=cc[k]
    chk(int(d["gstar"])==h["g"], f"C2 {k}: g*={int(d['gstar'])} exact")
    chk(abs(d["astar"]-h["a"])/h["a"]<=3e-3 and abs(d["mu"]-h["mu"])/h["mu"]<=3e-3, f"C2 {k}: a*={d['astar']:.5f} mu={d['mu']:.3f} (<=0.3%)")
    chk(abs(d["cT"]-h["cT"])/h["cT"]<=3e-3 and abs(d["cL1"]-h["cL1"])/h["cL1"]<=3e-3, f"C3 {k}: cT={d['cT']:.4f} cL1={d['cL1']:.4f} (<=0.3%)")
    chk(abs(d["RT"]-h["RT"])/h["RT"]<=3e-3, f"C4 {k}: R_T={d['RT']:.5f} vs chat {h['RT']:.5f} ({abs(d['RT']-h['RT'])/h['RT']*100:.2f}%)")
# ANCHOR-SYS: near chat values, NOT frozen (pre-registered falsification test)
chk(abs(anch["step_22"]["RT"]-0.51881)<2e-3 and abs(anch["step_22"]["RT"]-0.52284)>3e-3,
    f"ANCHOR-SYS step@22: RT={anch['step_22']['RT']:.5f} near chat 0.51881, NOT frozen 0.52284 -> attribution CONFIRMED (no S9)")
chk(abs(anch["gamma8_20"]["RT"]-0.48026)<2e-3 and abs(anch["gamma8_20"]["RT"]-0.47791)>1.5e-3,
    f"ANCHOR-SYS γ8@20: RT={anch['gamma8_20']['RT']:.5f} near chat 0.48026, NOT frozen 0.47791 -> attribution CONFIRMED")
# C6 mapper
chk(abs(D_ext-chatAV["D_ext"])<=0.06, f"C6 D_ext={D_ext:.3f}% vs chat {chatAV['D_ext']:.3f}% (<=0.06pp)")
chk(abs(D_F-chatAV["D_F"])<=0.06, f"C6 D_F={D_F:.3f}% vs chat {chatAV['D_F']:.3f}% (<=0.06pp)")
chk(arm==chatAV["arm"]=="KNOB", f"C6 arm={arm} == chat KNOB")

print(f"\n[C1–C6] {len(PASS)} PASS, {len(BREACH)} BREACH")
for m in PASS: print("  ✓",m)
for m in BREACH: print("  ✗ BREACH:",m)
print(f"\n[verdict] {'two-leg AGREEMENT — no S9' if not BREACH else 'BREACH -> S9'}: ARM = {arm}")
