"""G-TSH2 CC leg — PART 1: independent P4 arm-verdict + reduction-level audit of raw ω(k).
Shares NO ground-state/BdG machinery. Re-derives D_W/D_X/arm from the R_T pool with my own
max-from-mean, and re-reduces the chat's raw omT/omL1/ks arrays with my own zero-intercept LS +
log-log exponents to audit C3/C4/C6 at the reduction layer. Independent solver is PART 2.
"""
import json, numpy as np
CH="/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/1cc1dc77-gtsh2_results.json"
AV="/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/6ba89839-arm_verdict.json"
R=json.load(open(CH)); AVj=json.load(open(AV))
PASS=[]
def ok(c,m):
    assert c,"FAIL: "+m
    PASS.append(m)

# ---- independent zero-intercept LS speed + log-log exponent reducers ----
def cz(k,o,sl): k=np.asarray(k); o=np.asarray(o); return float(np.sum(o[sl]*k[sl])/np.sum(k[sl]**2))
def pex(k,o,sl): k=np.asarray(k); o=np.asarray(o); return float(np.polyfit(np.log(k[sl]),np.log(o[sl]),1)[0])
S26=slice(1,6); W1=slice(1,5); W2=slice(3,8)   # j=2..6, 2..5, 4..8 (locked estimators §7)

# ============ reduction audit per kernel (raw arrays -> c_T,c_L1,R_T,p,iso) ============
for K in ('K3','K4','K5','K6'):
    d=R['kernels'][K]; GM=d['raw']['GM']; GK=d['raw']['GK']
    cT_GM=cz(GM['ks'],GM['omT'],S26); cT_GK=cz(GK['ks'],GK['omT'],S26)
    cL_GM=cz(GM['ks'],GM['omL1'],S26); cL_GK=cz(GK['ks'],GK['omL1'],S26)
    ok(abs(cT_GM-d['cT_GM'])/d['cT_GM']<5e-3 and abs(cL_GM-d['cL1_GM'])/d['cL1_GM']<5e-3,
       f"{K}: c_T/c_L1 (GM) re-reduced independently match chat (<0.5%)")
    cT=0.5*(cT_GM+cT_GK); cL=0.5*(cL_GM+cL_GK); RT=cT/cL
    ok(abs(RT-d['R_T'])/max(d['R_T'],1e-9)<5e-3, f"{K}: R_T={RT:.5f} re-reduced vs chat {d['R_T']:.5f} (<0.5%)")
    isoT=abs(cT_GM-cT_GK)/(0.5*(cT_GM+cT_GK))*100
    ok(abs(isoT-d['iso_T_pct'])<0.05, f"{K}: iso_T={isoT:.3f}% matches chat {d['iso_T_pct']:.3f}%")
    # F-LIN independent check on L1 (the K3 exclusion driver)
    pL_GM=(pex(GM['ks'],GM['omL1'],W1),pex(GM['ks'],GM['omL1'],W2))
    pL_GK=(pex(GK['ks'],GK['omL1'],W1),pex(GK['ks'],GK['omL1'],W2))
    flin=any(not(0.90<=p<=1.10) for p in (*pL_GM,*pL_GK))
    fiso=(abs(cL_GM-cL_GK)/(0.5*(cL_GM+cL_GK))*100)>2.0
    if K=='K3':
        ok(flin, f"K3: F-LIN independently fires on L1 (p_W2={pL_GM[1]:.3f}/{pL_GK[1]:.3f}<0.90) -> exclusion driver")
        ok(fiso, f"K3: F-ISO independently fires on L1 (isoL={abs(cL_GM-cL_GK)/(0.5*(cL_GM+cL_GK))*100:.2f}%>2%)")
        ok(bool(d['excluded']), "K3: excluded=True in frozen results (matches independent falsifier state)")
    else:
        ok(not flin, f"{K}: F-LIN clean on L1 (all p in [0.90,1.10]) — no exclusion")

# ============ P4 arm verdict — independent max-from-mean ============
TH1,TH2=0.03,0.10
anch=R['anchors']; base=list(anch['step_RT'])+list(anch['gam6_RT'])
used=[K for K in ('K3','K4','K5') if not R['kernels'][K].get('excluded') and 'R_T' in R['kernels'][K]]
PW=base+[R['kernels'][K]['R_T'] for K in used]
K6=R['kernels']['K6']; PX=PW+[K6['R_T']] if not K6.get('excluded') else None
def D(pool):
    m=sum(pool)/len(pool); return max(abs(x-m)/m for x in pool), m
DW,mW=D(PW); DX,mX=D(PX)
ok(abs(DW-AVj['D_W'])<1e-6, f"D_W={DW*100:.3f}% (mean {mW:.5f}) matches arm_verdict {AVj['D_W']*100:.3f}%")
ok(abs(DX-AVj['D_X'])<1e-6, f"D_X={DX*100:.3f}% (mean {mX:.5f}) matches arm_verdict {AVj['D_X']*100:.3f}%")
if DW<=TH1 and DX<=TH1: arm='DERIVED-RATIO'
elif DW<=TH1 and DX>TH2: arm='KERNEL-CLASS-PINNED'
elif DW>TH2: arm='KNOB'
else: arm='UNDERDETERMINED-2'
ok(arm==AVj['arm']=='UNDERDETERMINED-2', f"ARM = {arm} (D_W,D_X both in dead-zone (3%,10%]) — matches chat")
ok(used==['K4','K5'] and AVj['excluded']==['K3'], "pool membership: K4,K5 in; K3 excluded — matches")

print(f"[PART 1] {len(PASS)} independent assertions PASSED\n")
for m in PASS: print("  ✓",m)
print(f"\n[summary] D_W={DW*100:.3f}% D_X={DX*100:.3f}% -> {arm}; K3 excluded (F-LIN+F-ISO indep-confirmed)")
