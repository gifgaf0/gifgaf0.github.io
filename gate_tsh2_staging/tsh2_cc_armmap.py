"""G-TSH2 CC leg — P4 arm mapper (quarantined; thresholds appear ONLY here, run last) +
C1–C6 verdict-level comparison against the chat leg. A-2 semantics. θ1=3%, θ2=10% (locked §9).
"""
import json, os, numpy as np
OUT=os.path.dirname(os.path.abspath(__file__))
TH1,TH2=0.03,0.10
# read-only anchors (locked §1; from G-TSH1 — never re-measured here)
ANCH_W=[0.5228,0.5286,0.5348,0.5436]; ANCH_G6=[0.4988]
cc={K:json.load(open(f'{OUT}/cc_{K}.json')) for K in ('K3','K4','K5','K6')}
p0=json.load(open(f'{OUT}/cc_p0.json'))
chat=json.load(open('/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/1cc1dc77-gtsh2_results.json'))['kernels']
chatAV=json.load(open('/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/6ba89839-arm_verdict.json'))

# ---- P4: pools + D + arm (A-2) ----
PW=list(ANCH_W)+list(ANCH_G6)+[cc[K]['R_T'] for K in ('K3','K4','K5') if not cc[K].get('excluded')]
PX=PW+[cc['K6']['R_T']] if not cc['K6'].get('excluded') else None
def D(p): m=sum(p)/len(p); return max(abs(x-m)/m for x in p),m
DW,mW=D(PW); DX,mX=D(PX)
if DW<=TH1 and DX<=TH1: arm='DERIVED-RATIO'
elif DW<=TH1 and DX>TH2: arm='KERNEL-CLASS-PINNED'
elif DW>TH2: arm='KNOB'
else: arm='UNDERDETERMINED-2'
print(f"[P4] P_W({len(PW)})={[round(x,5) for x in PW]}  D_W={DW*100:.3f}%")
print(f"[P4] P_X({len(PX)})={[round(x,5) for x in PX]}  D_X={DX*100:.3f}%")
print(f"[P4] ARM = {arm}\n")
json.dump(dict(D_W=DW,D_X=DX,arm=arm,pool_W=PW,pool_X=PX,excluded=[K for K in cc if cc[K].get('excluded')]),
          open(f'{OUT}/cc_arm_verdict.json','w'),indent=1)

# ---- C1–C6 verdict-level comparison ----
PASS=[]; BREACH=[]
def chk(c,m): (PASS if c else BREACH).append(m)
for K in ('K3','K4','K5','K6'):
    d,h=cc[K],chat[K]
    chk(d['gstar']==h['gstar'], f"C1 {K}: g*={d['gstar']} exact grid match")
    chk(abs(d['astar']-h['astar'])/h['astar']<=3e-3, f"C2 {K}: a* {d['astar']:.5f} vs {h['astar']:.5f} (<0.3%)")
    chk(abs(d['mu']-h['mu'])/h['mu']<=3e-3, f"C2 {K}: mu {d['mu']:.4f} vs {h['mu']:.4f} (<0.3%)")
    chk(abs(d['cT']-h['cT'])/h['cT']<=5e-3, f"C3 {K}: cT {d['cT']:.4f} vs {h['cT']:.4f} (<0.5%)")
    chk(abs(d['cL1']-h['cL1'])/h['cL1']<=5e-3, f"C3 {K}: cL1 {d['cL1']:.4f} vs {h['cL1']:.4f} (<0.5%)")
    chk(abs(d['R_T']-h['R_T'])/h['R_T']<=5e-3, f"C4 {K}: R_T {d['R_T']:.5f} vs {h['R_T']:.5f} (<0.5%)")
    # C6 falsifier/flag state identity
    dfl=set(f for f in d['flags'] if f!='W-MU-BAND'); hfl=set(f for f in h['flags'] if f!='W-MU-BAND')
    chk(dfl==hfl and bool(d.get('excluded'))==bool(h.get('excluded')),
        f"C6 {K}: flag/exclusion state {sorted(dfl)} excl={d.get('excluded')} matches")
chk(abs(DW-chatAV['D_W'])<=3e-3, f"C5: D_W {DW*100:.3f}% vs chat {chatAV['D_W']*100:.3f}% (<0.3pp)")
chk(abs(DX-chatAV['D_X'])<=3e-3, f"C5: D_X {DX*100:.3f}% vs chat {chatAV['D_X']*100:.3f}% (<0.3pp)")
chk(arm==chatAV['arm'], f"C5: arm '{arm}' == chat '{chatAV['arm']}'")
chk(p0['cneg'] and p0['cpos'], f"C6: controls C-NEG={p0['cneg']} C-POS={p0['cpos']} (both PASS)")

print(f"[C1–C6] {len(PASS)} PASS, {len(BREACH)} BREACH")
for m in PASS: print("  ✓",m)
for m in BREACH: print("  ✗ BREACH:",m)
print(f"\n[verdict] two-leg {'AGREEMENT — no S9' if not BREACH else 'BREACH -> S9 required'}: ARM = {arm}")
